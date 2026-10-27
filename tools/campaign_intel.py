# -*- coding: utf-8 -*-
"""campaign_intel.py - 战役情报聚合工具（S0 选集增强 / 点塔进度 / 产出率先验 / S4 预筛）。

把分散在 MCP 侧的平台情报能力聚合成战役流水线可直接消费的命令，
替代「Agent 逐个调 MCP 再人工拼结论」的手工编排。零新算法——只做数据聚合与交叉。

子命令：
  s0-select     S0 选集增强：recommend_datasets（平台真实点塔）× mining_yield（历史产出率）
                × dead_datasets（判死清单）三方交叉 → 产出「未点亮塔 × 高产出 × 未判死」候选
  pyramid       点塔进度快照：get_pyramid_alphas + get_pyramid_multipliers → 各 catalog
                点亮状态/乘数/还差几颗（S6 回写时调，写 wave_result.key_findings）
  s4-prescreen  S4 预筛压缩：batch_get_alpha_metrics 一次拉全 → READY/REVIEW/REJECT 分层，
                REJECT 直接判死不进 S4 链（评审效率提升 ~8 倍）
  ghost-audit   幽灵算子硬闸：operator_audit 检测表达式是否含平台不认的算子
                （S2 产物入库后、wave_gate 前调，防整批 CANCELLED 连坐）
  prod-first    prod-first 探针（2026-09-19）：S3 收批后立刻对本波每个信号族最强的 1 条
                跑平台 PROD_CORRELATION（单并发排队，串行），把"先烧回测、最后才知道撞 prod"
                前移到扩批之前；结果写 alphas.prod_correlation（已有行）+ ledger prod_first_<wave>，
                并给出族级 EXPAND / STOP 建议（≥0.7 的族不再扩变体，换族）
  prod-probe    开波前族级 prod 探针（P0-1，2026-10-24）：对**待开波数据集**的全部历史回测行
                （跨所有波次）每信号族选最强 1 条探 prod（0 回测槽，只占 prod 队列），
                prod ≥--prod-max（缺省 0.75）⇒ 封族：写 probe=true 死路指纹（闸 PF 开波时
                enforced 拦截，不再花整波回测）+ ledger prod_probe_<region>_<dataset> 封族记录；
                退出码 2 = 有族被封（勿开该族整波）。区别于 prod-first：后者收批后探本波行。
  mark-saturated S6→S0 反馈（2026-09-29）：把被 prod 墙卡死的数据集写入 ledger saturated_datasets，
                S0 打分（score_datasets P2/P5）读取并降级；缺省 dry-run，--write-ledger 落库
  backlog-drop  积压波清理（缺省 dry-run，--apply 写库）
  atom-first    ATOM 优先候选单（2026-10-26）：读 backtest_results × expressions.atom_flag，
                单数据集排在前面、跨数据集只进备选区，绝不混排；零平台调用

用法:
  python tools/campaign_intel.py s0-select --region EUR --delay 1 --universe TOP2500
  python tools/campaign_intel.py pyramid --region EUR --delay 1
  python tools/campaign_intel.py s4-prescreen --alpha-ids id1 id2 id3
  python tools/campaign_intel.py ghost-audit --region EUR --exprs-file candidates.txt
  python tools/campaign_intel.py prod-first --region IND --wave 172 --top-k 3 --write-ledger
  python tools/campaign_intel.py prod-probe --region USA --dataset insider_matrix
  python tools/campaign_intel.py mark-saturated --region EUR --dataset model26 --reason "prod 墙 ≥0.9" --wave 12 --write-ledger
  python tools/campaign_intel.py atom-first --region IND --top 12

退出码: 0=成功，1=失败/有 BLOCK 项。
运行环境: 使用 MCP venv（$WQ_PY 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/MCP 目录解析（tools/_pyenv.py；2026-09-29 替换各脚本抄写的 Windows 盘符兜底）
import datetime
import time

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
# 2026-09-17 P0-4：ledger 契约归一的规范实现在 src/wqb（单一事实源）
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_DIR = os.path.join(_REPO_ROOT, "src")
if os.path.isdir(_SRC_DIR) and _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)


def _mcp_venv_python():
    return _pyenv.venv_python()


def _bootstrap():
    """路径引导：非 MCP venv 解释器时 re-exec 到 venv；把 MCP 目录与 src 加入 sys.path（跨平台）。"""
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    # wqb 规范核心包在 src/wqb（ghost-audit 依赖 wqb.expression）——bootstrap_paths 已注入


# ---------------------------------------------------------------------------
# xr-probe：跨区探针（2026-09-19 从 scratch 脚本升格）
#   把同一组表达式按各区战役 settings 发到多个 region，轮询到 terminal，收批入库
#   （expressions + backtest_results，wave=probe_<tag>），并写 GLOBAL/xr_probe_<tag> 台账。
#   用途：SOP 步 1「跨区先验」——一个机制在其它区是否也有信号，10 分钟出结论，避免整区开战役再发现移植失败。
# ---------------------------------------------------------------------------

_XR_SIM_KEYS = ("instrumentType", "region", "universe", "delay", "neutralization", "decay", "truncation",
                "pasteurization", "unitHandling", "nanHandling", "maxTrade", "language", "visualization")


def _xr_region_settings(region, overrides=None):
    """读 tracking/<R>/config/settings.json（缺省则用平台常见档）并只保留仿真键。"""
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(repo, "tracking", region, "config", "settings.json")
    base = {"instrumentType": "EQUITY", "region": region, "delay": 1, "decay": 4, "truncation": 0.08,
            "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "OFF", "maxTrade": "OFF",
            "language": "FASTEXPR", "visualization": False, "neutralization": "SUBINDUSTRY"}
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
        base.update({k: v for k, v in cfg.items() if k in _XR_SIM_KEYS})
    except Exception:
        pass
    base["region"] = region
    if overrides:
        base.update({k: v for k, v in overrides.items() if k in _XR_SIM_KEYS})
    if not base.get("universe"):  # 无战役目录的区域：缺省宇宙取 config.REGIONS（区域事实唯一来源，2026-10-04 收口）
        try:
            from wqb.config import default_universe
            base["universe"] = default_universe(region)
        except KeyError:
            base["universe"] = "TOP3000"
    return base


async def _cmd_xr_probe(a):
    import asyncio
    from brain_api import BrainApiClient  # noqa: F402
    import wqb_db_mcp as dbm  # 直接复用 store（与 MCP 同一实现）
    exprs = [ln.strip() for ln in open(a.exprs_file, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
    if not exprs:
        print("[xr-probe] 表达式文件为空", file=sys.stderr)
        return 2
    regions = [r.strip().upper() for r in a.regions.split(",") if r.strip()]
    overrides = {}
    for kv in a.set or []:
        k, _, v = kv.partition("=")
        overrides[k] = (int(v) if v.isdigit() else v)
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    tag = a.tag or datetime.date.today().strftime("%Y%m%d")
    wave = "probe_%s" % tag
    summary = {"tag": tag, "wave": wave, "exprs": exprs, "regions": {},
               "at": datetime.datetime.now().isoformat(timespec="seconds")}

    # ① 发批（每区一个 multisim；表达式 >10 时拆批）
    #    发批前按区校验字段存在性（tools_data._verify_fields_exist，带缓存）：含未知字段的式子不进该区批
    #    （2026-09-19 实证：pv103 字段只在 IND 有，混进 GLB/GBR/DEU/USA 批 → 连坐 4 批全 CANCELLED）
    try:
        import tools_data as _td  # world-quant-brain-mcp 包内
    except Exception:
        _td = None
    locs = {}
    resume = {}
    for kv in a.resume or []:  # --resume GLB=msid1 --resume USA=msid2：跳过发批，直接收批
        k, _, v = kv.partition("=")
        if k and v:
            resume.setdefault(k.strip().upper(), []).append(brain.base_url + "/simulations/" + v.strip())
    for region in regions:
        st = _xr_region_settings(region, overrides)
        if a.universe:
            st["universe"] = a.universe
        if region in resume:
            locs[region] = resume[region]
            summary["regions"][region] = {"settings": st, "resumed": True}
            continue
        region_exprs = list(exprs)
        if _td is not None and not a.no_field_check:
            try:
                cands = _td._extract_field_candidates(region_exprs)
                ver = await _td._verify_fields_exist(cands, region=region, universe=st.get("universe"),
                                                     delay=int(st.get("delay", 1)), client=brain)
                unknown = set(ver.get("unknown") or [])
                if unknown and not ver.get("skipped"):
                    keep = []
                    for e in region_exprs:
                        bad = [f for f in unknown if f in e]
                        if bad:
                            print("[xr-probe] %s 跳过（字段不存在 %s）: %s" % (region, bad, e[:80]))
                        else:
                            keep.append(e)
                    region_exprs = keep
                    summary["regions"].setdefault(region, {})["unknown_fields"] = sorted(unknown)
            except Exception as e:
                print("[xr-probe] %s 字段校验失败（照发）: %s" % (region, str(e)[:120]))
        if not region_exprs:
            summary["regions"].setdefault(region, {})["settings"] = st
            summary["regions"][region]["n"] = 0
            print("[xr-probe] %s 无可发表达式（字段全缺）" % region)
            continue
        chunks = [region_exprs[i:i + 10] for i in range(0, len(region_exprs), 10)]
        locs[region] = []
        summary["regions"][region] = {"settings": st}
        for ch in chunks:
            payload = [{"type": "REGULAR", "settings": st, "regular": e} for e in ch]
            body = payload[0] if len(payload) == 1 else payload
            try:
                r = await brain._request("POST", brain.base_url + "/simulations", json=body)
                if r.status_code >= 400:
                    msg = str(brain._response_payload(r))[:300]
                    print("[xr-probe] %s POST %s: %s" % (region, r.status_code, msg))
                    summary["regions"][region]["error"] = msg
                    continue
                loc = r.headers.get("Location", "")
                locs[region].append(loc)
                print("[xr-probe] %s/%s 已发 %d 条 -> %s" % (region, st.get("universe"), len(ch), loc.rstrip("/").split("/")[-1]))
            except Exception as e:
                summary["regions"][region]["error"] = str(e)[:300]

    # ② 轮询 + 收批
    deadline = time.time() + a.timeout_sec
    store = dbm._store()
    try:
        for region, ls in locs.items():
            rows_all = []
            for loc in ls:
                status, children = None, []
                while time.time() < deadline:
                    try:  # 瞬态网络/代理错误不杀轮询（2026-09-19 实证 ProxyError 中断收批）
                        r = await brain._request("GET", loc)
                        d = r.json() if r.status_code < 400 else {}
                    except Exception as e:
                        print("[xr-probe] poll %s 瞬态错误，%ss 后重试: %s" % (loc.rstrip("/").split("/")[-1], a.poll_sec, str(e)[:120]))
                        await asyncio.sleep(a.poll_sec)
                        continue
                    status = d.get("status")
                    children = d.get("children") or []
                    if status in ("COMPLETE", "ERROR", "CANCELLED", "FAIL"):
                        break
                    await asyncio.sleep(a.poll_sec)
                child_urls = []
                for c in children:
                    if isinstance(c, dict):
                        c = c.get("location") or c.get("id")
                    c = str(c)
                    child_urls.append(c if c.startswith("http") else brain.base_url + "/simulations/" + c)
                for cu in child_urls:
                    cd = None
                    for _try in range(3):
                        try:
                            cr = await brain._request("GET", cu)
                            cd = cr.json()
                            break
                        except Exception as e:
                            err = str(e)[:200]
                            await asyncio.sleep(a.poll_sec)
                    if cd is None:
                        rows_all.append({"error": err})
                        continue
                    aid = cd.get("alpha")
                    if not aid:
                        rows_all.append({"error": cd.get("message") or cd.get("status") or "no alpha"})
                        continue
                    try:
                        det = await brain.get_alpha_details(aid)
                    except Exception as e:
                        det = {"alpha_id": aid, "error": str(e)[:200]}
                    rows_all.append(det if isinstance(det, dict) else {"alpha_id": aid})
            flat = [dbm._flatten_platform_alpha(x) for x in rows_all if isinstance(x, dict) and not x.get("error")]
            errs = [x.get("error") for x in rows_all if isinstance(x, dict) and x.get("error")]
            if flat:
                store.upsert_expressions(
                    region, wave,
                    [{"expression": x.get("expression"), "status": "selected", "source": "xr_probe"}
                     for x in flat if x.get("expression")],
                    dataset=a.dataset)
                ids = {r_["expression"]: r_["id"] for r_ in store.list_expressions(region, wave)}
                bt = []
                for x in flat:
                    bt.append({"expression_id": ids.get(x.get("expression")), "alpha_id": x.get("alpha_id"),
                               "status": "COMPLETE", "sharpe": x.get("sharpe"), "fitness": x.get("fitness"),
                               "turnover": x.get("turnover"), "returns": x.get("returns"),
                               "drawdown": x.get("drawdown"), "margin": x.get("margin"),
                               "two_year_sharpe": x.get("two_year_sharpe"),
                               "sub_universe_sharpe": x.get("sub_universe_sharpe"),
                               "long_count": x.get("long_count"), "short_count": x.get("short_count"),
                               "robust_sharpe": x.get("robust_universe_sharpe"),
                               "ra_failed_checks": x.get("ra_failed_checks") or [], "code": x.get("expression")})
                store.save_backtest_results(region, wave, bt, dataset=a.dataset)
            best = max((abs(x.get("sharpe") or 0) for x in flat), default=None)
            summary["regions"][region].update({
                "n": len(flat), "errors": errs[:5], "max_abs_sharpe": best,
                "rows": [{"alpha_id": x.get("alpha_id"), "sharpe": x.get("sharpe"), "fitness": x.get("fitness"),
                          "turnover": x.get("turnover"), "two_year_sharpe": x.get("two_year_sharpe"),
                          "ra_failed_checks": x.get("ra_failed_checks"),
                          "expr": (x.get("expression") or "")[:120]} for x in flat]})
            print("[xr-probe] %s: n=%d max|S|=%s errors=%d" % (region, len(flat), best, len(errs)))
            for x in flat:
                print("    %s S=%s F=%s tvr=%s 2Y=%s fails=%s | %s" % (
                    x.get("alpha_id"), x.get("sharpe"), x.get("fitness"), x.get("turnover"),
                    x.get("two_year_sharpe"), x.get("ra_failed_checks"), (x.get("expression") or "")[:80]))
        if a.write_ledger:
            store.upsert_ledger("GLOBAL", "xr_probe_%s" % tag, summary)
            print("[xr-probe] ledger GLOBAL/xr_probe_%s 已写" % tag)
    finally:
        store.close()
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=1)
    return 0

# ---------------------------------------------------------------------------
# s0-select：S0 选集增强（三方交叉）
# ---------------------------------------------------------------------------


def _expr_counts_by_dataset(cur, region):
    """本区每个数据集已落库的表达式条数 {dataset: n}（只读 `expressions` 表，region 作用域）。

    s0-select 的「处女地」判据曾只看 `backtest_results`：GEM 生成 / 选波已落库、但还没关联回测的集会被当成
    「未测」。「未测」口径 = backtest_results ∪ expressions 并集（WorkBuddy 记忆 MEMORY §0.3）。
    """
    cur.execute(
        "SELECT dataset, COUNT(*) FROM expressions "
        "WHERE region=? AND dataset IS NOT NULL AND dataset<>'' GROUP BY dataset", (region,))
    return {ds: n for ds, n in cur.fetchall()}


def _s0_rank_key(x, xr_penalize=False):
    """s0-select 排序键（P1 2026-09-30 / P0-4 2026-10-24）：(判死沉底, 次沉, 机制层, -score)。

    实测（公平对照 ≥2 区共有数据集 n=154）：跨区弱先验 lift +1pp 在噪声内，
    无预测力；但作为 soft 第二键会把 17%（8/48）候选整体压到存活队尾被 top-n
    截断 ⇒ 纯系统性偏置。故**默认把 xr_penalized 移出排序键**；
    `--xr-penalize` 可复现旧行为（降权）。四层结构含义：
      key[0] = ledger_dead / proven_dead_by_yield / region_dead（判死沉底）
      key[1] = conditioning_only（字段数不足次沉；xr 仅在 flag 下并入）
      key[2] = 机制层（P0-4）：0=经典异象 / 1=未标注 / 2=明示非经典
               （来源 tracking/<REGION>/reference/<r>_dataset_mechanisms.md；
                未登记或过期一律 1，不清洗总分的原有次序）
      key[3] = -total_score（同层内按平台分降序）
    契约守护：tests/unit/08_forum_recon/test_campaign_intel_s0_rank_p1.py。
    """
    penalized = bool(x["ledger_dead"] or x["proven_dead_by_yield"]
                     or x.get("region_dead"))
    soft = bool(x["conditioning_only"] or (xr_penalize and x.get("xr_penalized")))
    mech = int(x.get("mechanism_tier", 1) or 0)
    return (penalized, soft, mech, -(x.get("total_score") or 0))


# ---------------------------------------------------------------------------
# P1-6 / P0-4（2026-10-24）：区域层选集规则文件
#   ① <region_lower>_dead_datasets.md  —— 已判死清单（S0 自动剔除，过期降 advisory）
#   ② <region_lower>_dataset_mechanisms.md —— 机制标注（排序键第三层）
# 为什么不用 ledger `*_dead` 键：那条写入路径受 seal_dead_end 的论坛取证闸管辖
# （AGENTS.md §8.11，故障/无证据不得判死），而区域文件允许人工复核、过期自降级。
# ---------------------------------------------------------------------------

_FENCED_JSON_RE = re.compile(r"```json\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)


def _read_fenced_json(path):
    """读 Markdown 里首个合法的 ```json 代码块 → (dict|None, error|None)。"""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        return None, f"{type(e).__name__}: {e}"
    last_err = "未找到合法的 ```json 代码块"
    for m in _FENCED_JSON_RE.finditer(text):
        try:
            obj = json.loads(m.group(1))
        except Exception as e:  # 坏块跳过，继续找下一块
            last_err = f"{type(e).__name__}: {e}"
            continue
        if isinstance(obj, dict):
            return obj, None
    return None, last_err


def _entry_stale(entry, review_after_days, today=None):
    """条目是否过期：as_of 缺失 / 不可解析 / 早于 review_after_days ⇒ 过期。

    用户 2026-10-23 纪律：过期证据不能作证。故过期条目只作 advisory，不参与剔除/排序。
    """
    raw = (entry or {}).get("as_of")
    if not raw:
        return True
    try:
        d = datetime.date.fromisoformat(str(raw))
    except ValueError:
        return True
    today = today or datetime.date.today()
    try:
        limit = int(review_after_days)
    except (TypeError, ValueError):
        limit = 120
    return (today - d).days > limit


def _load_region_rules(region, filename, root=None, today=None, default_review_days=120):
    """通用加载器：tracking/<REGION>/reference/<filename> 的 ```json 块 → dict。

    返回 {path, entries, live, stale, as_of, review_after_days, warning}。
    live = 未过期条目；stale = 过期条目（只打印不生效）。文件缺失不算告警。
    """
    repo = root or _REPO_ROOT
    path = os.path.join(repo, "tracking", region.upper(), "reference", filename)
    res = {"path": path, "entries": {}, "live": {}, "stale": {},
           "as_of": None, "review_after_days": default_review_days, "warning": None}
    if not os.path.exists(path):
        return res
    obj, err = _read_fenced_json(path)
    if obj is None:
        res["warning"] = f"区域规则文件无法解析（{err}）：{path}"
        print(f"[s0-select] ★{res['warning']}", file=sys.stderr)
        return res
    res["as_of"] = obj.get("as_of")
    try:
        res["review_after_days"] = int(obj.get("review_after_days") or default_review_days)
    except (TypeError, ValueError):
        res["review_after_days"] = default_review_days
    for e in (obj.get("datasets") or []):
        if not isinstance(e, dict):
            continue
        ds = str(e.get("dataset") or "").strip()
        if not ds:
            continue
        rec = dict(e)
        res["entries"][ds] = rec
        (res["stale"] if _entry_stale(rec, res["review_after_days"], today=today)
         else res["live"])[ds] = rec
    return res


def _load_region_dead_list(region, root=None, today=None):
    """P1-6：已判死数据集清单（tracking/<REGION>/reference/<r>_dead_datasets.md）。

    命中 live → 标 region_dead 并沉底剔除；命中 stale → 只打印告警、不剔除。
    """
    res = _load_region_rules(region, f"{region.lower()}_dead_datasets.md",
                             root=root, today=today, default_review_days=120)
    if res["stale"]:
        sample = ", ".join(sorted(res["stale"])[:8])
        more = " …" if len(res["stale"]) > 8 else ""
        print(f"[s0-select] ⚠区域判死清单 {len(res['stale'])} 条已过期"
              f"（>{res['review_after_days']} 天；as_of 缺失按过期处理）⇒ 只作 advisory、不剔除："
              f"{sample}{more}", file=sys.stderr)
    return res


def _load_region_mechanisms(region, root=None, today=None):
    """P0-4：数据集机制标注（tracking/<REGION>/reference/<r>_dataset_mechanisms.md）。

    过期条目不生效 ⇒ 该集回到「未标注」（tier 1），不清洗总分的原有次序。
    """
    res = _load_region_rules(region, f"{region.lower()}_dataset_mechanisms.md",
                             root=root, today=today, default_review_days=180)
    if res["stale"]:
        sample = ", ".join(sorted(res["stale"])[:8])
        more = " …" if len(res["stale"]) > 8 else ""
        print(f"[s0-select] ⚠机制标注 {len(res['stale'])} 条已过期"
              f"（>{res['review_after_days']} 天）⇒ 降为未标注（tier 1）：{sample}{more}",
              file=sys.stderr)
    return res


def _mechanism_tier(rec):
    """classic_anomaly=True → 0（优先）；未登记 → 1；False → 2（明示非经典，沉底）。"""
    if not rec:
        return 1
    v = rec.get("classic_anomaly")
    if v is True:
        return 0
    if v is False:
        return 2
    return 1



async def _cmd_s0_select(a):
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # ① 平台真实点塔优先推荐（recommend_datasets 已内含 pyramid 状态 + 质量 + 热度）
    rec = await brain.recommend_datasets(
        region=a.region, delay=a.delay, universe=a.universe, top_n=a.top_n * 3)
    if rec.get("error"):
        print(f"[s0-select] recommend_datasets 失败: {rec['error']}", file=sys.stderr)
        return 1
    recommendations = rec.get("recommendations") or []
    pyramid_status = rec.get("pyramid_status") or {}

    # 2026-10-24 P1-4：塔位快照并入 S0 产物（每波必带）。
    # 平台 recommend_datasets 已返回 pyramid_summary；这里整形为可直接引用的快照，
    # 不额外打平台请求（零配额）。
    _pyr = rec.get("pyramid_summary") or {}
    snapshot_rows = []
    for cat_id, item in (_pyr.items() if isinstance(_pyr, dict) else []):
        if not isinstance(item, dict):
            continue
        snapshot_rows.append({
            "category": cat_id,
            "category_name": item.get("category_name"),
            "alpha_count": item.get("alpha_count"),
            "need_to_light": item.get("need_to_light"),
            "lit": bool(item.get("lit")),
            "multiplier": item.get("multiplier"),
        })
    snapshot_rows.sort(key=lambda r: (r["lit"], -(r.get("need_to_light") or 0),
                                      -(r.get("multiplier") or 0)))
    pyramid_snapshot = {
        "region": a.region, "delay": a.delay,
        "as_of": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "recommend_datasets.pyramid_summary",
        "lit": [r["category"] for r in snapshot_rows if r["lit"]],
        "unlit": [r["category"] for r in snapshot_rows if not r["lit"]],
        "lit_count": sum(1 for r in snapshot_rows if r["lit"]),
        "total": len(snapshot_rows),
        "rows": snapshot_rows,
    }
    if not snapshot_rows:
        print("[s0-select] ⚠平台未返回 pyramid_summary —— 塔位快照只有 lit/unlit 计数，"
              "不足以逐类核对（下次选集重试或直接跑 pyramid 子命令）", file=sys.stderr)

    # 2026-10-24 P1-6 / P0-4：区域层规则（判死清单 + 机制标注）。
    region_dead = _load_region_dead_list(a.region)
    region_mech = _load_region_mechanisms(a.region)
    include_region_dead = bool(getattr(a, "include_region_dead", False))

    # ② 本地台账：历史产出率（mining_yield）+ 判死清单（dead_datasets）
    #    + 白名单/自动排名/座位模型（P1 可达性 & P4 覆盖审计）—— 走本地 sqlite
    yield_map = {}
    expr_map = {}        # 2026-10-04：本区每集已落库表达式数（「未测」= 回测 ∪ 表达式，不能只看 backtest_results）
    dead_set = set()
    xr_map = {}          # 2026-09-19：跨区先验 dataset -> {weak:[REG:maxS@bt], strong:[REG:n_ra_clean]}
    field_counts = {}    # 2026-09-19：dataset -> field_count（<min_fields 不进主攻）
    whitelist = {}       # P4：dataset -> 白名单候选 dict（含 override.reason 则视为已注记）
    ranking_tier = {}    # P4：dataset -> {tier, hard_excluded}（score_datasets 自动结论）
    seat_model = {}      # P1：dataset -> est_seats（独立可提交座位估计）
    seats_default = 2    # P1：无 seat_model 台账时的每集默认座位（占位，建议用台账精化）
    try:
        import sqlite3
        db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "data", "wqb.db")
        conn = db_connect(db)
        cur = conn.cursor()
        # 产出率：ra_clean/backtested per dataset（2026-09-19 严格口径，与 get_mining_yield(strict) 同源）
        # 旧口径只看 sharpe/fitness：IND 34% "产出率"实际可提交 0（robust/2Y/CW 在 ra_failed_checks，
        # prod 墙在 alphas 表）。这里 passed 保留旧口径对照，yield_rate 改用 ra_clean。
        ra_clean_sql = ("(ABS(COALESCE(b.sharpe,0))>=? AND COALESCE(b.fitness,0)>=? "
                        "AND COALESCE(TRIM(b.ra_failed_checks),'') IN ('', '[]'))")
        cur.execute(
            "SELECT b.dataset, COUNT(*) bt, "
            "SUM(CASE WHEN ABS(COALESCE(b.sharpe,0))>=? AND COALESCE(b.fitness,0)>=? "
            "THEN 1 ELSE 0 END) passed, "
            f"SUM(CASE WHEN {ra_clean_sql} THEN 1 ELSE 0 END) ra_clean, "
            f"SUM(CASE WHEN {ra_clean_sql} AND a.prod_correlation IS NOT NULL AND a.prod_correlation >= 0.7 "
            "THEN 1 ELSE 0 END) prod_blocked "
            "FROM backtest_results b LEFT JOIN alphas a ON a.alpha_id=b.alpha_id "
            "WHERE b.region=? AND b.dataset IS NOT NULL "
            "GROUP BY b.dataset",
            (a.sharpe_min, a.fitness_min, a.sharpe_min, a.fitness_min,
             a.sharpe_min, a.fitness_min, a.region),
        )
        for ds, bt, passed, ra_clean, prod_blocked in cur.fetchall():
            yield_map[ds] = {
                "backtested": bt,
                "passed": passed or 0,
                "ra_clean": ra_clean or 0,
                "prod_blocked": prod_blocked or 0,
                "yield_rate": round((ra_clean or 0) / bt, 4) if bt else None,
                "yield_rate_loose": round((passed or 0) / bt, 4) if bt else None,
            }
        # 本区每集历史最强 |sharpe|（信号存在性最直接的证据）
        cur.execute(
            "SELECT dataset, MAX(ABS(COALESCE(sharpe,0))) FROM backtest_results "
            "WHERE region=? AND dataset IS NOT NULL GROUP BY dataset", (a.region,))
        for ds, mx in cur.fetchall():
            yield_map.setdefault(ds, {})["max_sharpe"] = round(mx or 0, 3)
        # 2026-10-04：有表达式（GEM 生成 / 选波落库）但没关联回测的集不是「处女地」——
        # 「未测」口径 = backtest_results ∪ expressions 并集（单用前者会把它误判成未测，白名单交集漏判）。
        try:
            expr_map = _expr_counts_by_dataset(cur, a.region)
        except Exception as _e:  # 缺表 / 缺列：降级为只看回测，不阻断选集
            print(f"[s0-select] expressions 计数降级（{_e}）", file=sys.stderr)
        # 2026-09-19 跨区负先验：同一数据集在其它区域已测且弱（max|S| < xr_weak_sharpe，样本 ≥ xr_min_bt）
        # → 本区大概率同弱（news/sentiment 在 USA/EUR/IND 三区同型全灭实证）；反之其它区有 RA-clean
        # 则是"信号存在"的正证据。只做先验标注与排序降权，不判死。
        cur.execute(
            "SELECT region, dataset, COUNT(*) bt, MAX(ABS(COALESCE(sharpe,0))) mx, "
            "SUM(CASE WHEN ABS(COALESCE(sharpe,0))>=? AND COALESCE(fitness,0)>=? "
            "AND COALESCE(TRIM(ra_failed_checks),'') IN ('', '[]') THEN 1 ELSE 0 END) ra_clean "
            "FROM backtest_results WHERE region<>? AND dataset IS NOT NULL GROUP BY region, dataset",
            (a.sharpe_min, a.fitness_min, a.region))
        for reg, ds, bt, mx, rc in cur.fetchall():
            x = xr_map.setdefault(ds, {"weak": [], "strong": [], "regions": 0})
            x["regions"] += 1
            if (rc or 0) > 0:
                x["strong"].append(f"{reg}:{rc}")
            elif bt >= a.xr_min_bt and (mx or 0) < a.xr_weak_sharpe:
                x["weak"].append(f"{reg}:{(mx or 0):.2f}@{bt}")
        # 字段数（<min_fields 只能当条件腿/事件探针，不进主攻）
        cur.execute(
            "SELECT d.name, d.field_count FROM datasets d JOIN regions r ON r.id=d.region_id "
            "WHERE r.name=?", (a.region,))
        for ds, fc in cur.fetchall():
            if fc is not None:
                field_counts[ds] = int(fc)
        # 判死清单：ledger_kv 的 *_dead keys
        cur.execute(
            "SELECT key FROM ledger_kv WHERE region=? AND key LIKE '%_dead'", (a.region,))
        dead_set = {r[0][:-5] for r in cur.fetchall()}

        # P1/P4：读白名单 / 自动排名 / 座位模型三个台账键
        def _kv(key, raw=False):
            cur.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?",
                        (a.region, key))
            row = cur.fetchone()
            if not row:
                return (None if raw else {})
            v = row[0]
            if raw:
                return v
            if isinstance(v, (str, bytes, bytearray)):
                try:
                    return json.loads(v) or {}
                except Exception:
                    return {}
            return v or {}

        # 2026-09-17 P0-4：白名单改用**容错归一**（覆盖 candidates/whitelist/datasets/
        # 推断/损坏抢救 共 5 种历史形态），解析失败显式告警而非静默空集。
        # 旧实现只认 `wl["candidates"][]`，实测仅 4/13 区命中（CHN/DEU/EUR/KOR）；
        # 其余 9 区白名单被当作空集 → override-gap 审计与白名单报表降级为"无数据"。
        try:
            from wqb.ledger_whitelist import normalize as _norm_wl
            _wl_rec = _norm_wl(_kv("s0_whitelist", raw=True))
        except Exception as _e:
            _wl_rec = {"ok": False, "schema": "import_error", "datasets": [], "entries": [],
                       "reason": f"{type(_e).__name__}: {_e}"}
        if not _wl_rec.get("ok"):
            print(f"[s0-select] ★s0_whitelist 无法解析（{_wl_rec.get('reason')}）"
                  f"——白名单相关审计将不完整", file=sys.stderr)
        elif _wl_rec.get("schema") in ("inferred", "recovered"):
            print(f"[s0-select] ⚠s0_whitelist 形态={_wl_rec['schema']}"
                  f"（{_wl_rec.get('reason')}）", file=sys.stderr)
        for _ds in (_wl_rec.get("datasets") or []):
            whitelist.setdefault(_ds, {"dataset": _ds})
        for _c in (_wl_rec.get("entries") or []):
            if isinstance(_c, dict) and _c.get("dataset"):
                whitelist[_c["dataset"]] = _c   # 保留 override 等审计字段

        rk = _kv("s0_ranking")
        sm = _kv("seat_model")
        # 2026-09-17 P3-9：把「缺 s0_ranking」由静默降级改为显式告警。
        # 实况（2026-09-17 实测）：10 区有非空 ranking[]（ASI/CHN/DEU/EUR/GBR/GLB/HKG/
        # JPN/KOR/USA），而 **IND 完全没有该行**（MEA 亦无）。原先 `rk.get("ranking") or []`
        # 让"排名缺失"与"无数据集有 tier"无法区分 → 三方交叉悄悄退化为两方，
        # 且 tier / hard_excluded 全部丢失却无人察觉。
        _rk_rows = [r for r in (rk.get("ranking") or [])
                    if isinstance(r, dict) and r.get("id")]
        if not _rk_rows:
            print(f"[s0-select] ★ 台账缺 s0_ranking（region={a.region}）—— "
                  f"tier/hard_excluded 不可用，本次三方交叉已降级为两方。"
                  f"补建：python Claude/skills/wq-brain-campaign-toolkit/scripts/"
                  f"score_datasets.py --campaign-dir tracking/{a.region}",
                  file=sys.stderr)
        for r in _rk_rows:
            ranking_tier[r["id"]] = {
                "tier": r.get("tier"), "hard_excluded": r.get("hard_excluded")}
        seat_model = sm.get("seats") or {}
        seats_default = int(sm.get("seats_per_dataset_default", 2) or 2)
        conn.close()
    except Exception as e:
        print(f"[s0-select] 本地 DB 读取降级（{e}），仅用平台推荐", file=sys.stderr)

    # ③ 三方交叉：未点亮塔优先，剔除判死，标注产出率先验
    out = []
    for r in recommendations:
        ds_id = r.get("dataset_id")
        y = yield_map.get(ds_id, {})
        yr = y.get("yield_rate")
        bt = y.get("backtested", 0)
        is_dead = ds_id in dead_set
        # 产出率硬闸：样本足够（>=a.min_samples）且产出率为 0 → 判死候选，降权到底部
        proven_dead = (bt >= a.min_samples and (yr or 0) == 0)
        xr = xr_map.get(ds_id, {})
        xr_weak = bool(xr.get("weak")) and not xr.get("strong")
        fc = field_counts.get(ds_id)
        conditioning_only = fc is not None and fc < a.min_fields
        # 2026-10-24 P1-6：区域判死清单（live 才剔除；stale 只告警，见 _load_region_dead_list）
        rd = region_dead["live"].get(ds_id)
        rd_stale = region_dead["stale"].get(ds_id)
        # 2026-10-24 P0-4：机制标注（tier 0 经典 / 1 未标注 / 2 明示非经典）
        mech = region_mech["live"].get(ds_id) or {}
        out.append({
            "dataset_id": ds_id,
            "dataset_name": r.get("dataset_name"),
            "category": r.get("category"),
            "category_lit": r.get("category_lit"),
            "category_need_to_light": r.get("category_need_to_light"),
            "pyramid_multiplier": r.get("pyramid_multiplier"),
            "total_score": r.get("total_score"),
            "os_is_sharpe": r.get("os_is_sharpe"),
            "dataset_alpha_count": r.get("dataset_alpha_count"),
            "dataset_user_count": r.get("dataset_user_count"),
            # 本地先验
            "hist_backtested": bt,
            "hist_expressions": expr_map.get(ds_id, 0),
            "hist_yield_rate": yr,
            "hist_max_sharpe": y.get("max_sharpe"),
            "ledger_dead": is_dead,
            "proven_dead_by_yield": proven_dead,
            # 2026-09-19 先验
            "field_count": fc,
            "conditioning_only": conditioning_only,
            "xr_weak": xr.get("weak") or [],
            "xr_strong": xr.get("strong") or [],
            "xr_penalized": xr_weak,
            "est_seats": int(seat_model.get(ds_id, seats_default) or 0),  # P1：独立座位估计
            # 2026-10-24 P1-6 / P0-4
            "region_dead": bool(rd) and not include_region_dead,
            "region_dead_verdict": (rd or {}).get("verdict"),
            "region_dead_reason": (rd or {}).get("reason"),
            "region_dead_stale": bool(rd_stale),
            "region_dead_stale_reason": (rd_stale or {}).get("reason"),
            "mechanism": mech.get("mechanism"),
            "classic_anomaly": mech.get("classic_anomaly"),
            "mechanism_tier": _mechanism_tier(mech),
            "mechanism_evidence": mech.get("evidence"),
        })


    # 排序：判死（ledger / 产出率证伪 / 区域清单）沉底；字段<min_fields 次沉；
    #       机制层（P0-4：经典异象 > 未标注 > 明示非经典）；同层按 total_score 降序
    # （2026-09-19：此前只按未点亮塔分排序，把 earnings3/insiders1/macro63/shortinterest5 这类
    #   结构性弱集推到前排，7 集 197 条回测 0 候选）
    # （2026-09-30 P1：跨区弱移出排序键（无预测力且压尾截断），--xr-penalize 复现旧行为）
    out.sort(key=lambda x: _s0_rank_key(
        x, xr_penalize=bool(getattr(a, "xr_penalize", False))))

    # 2026-09-19 用户硬规则：已点亮塔（当季 ACTIVE >= 3）的数据集不开战役，只作组腿 —— 默认剔除
    lit_excluded = []
    if not getattr(a, "include_lit", False):
        lit_excluded = [x for x in out if x.get("category_lit")]
        out = [x for x in out if not x.get("category_lit")]
    alive = [x for x in out if not (x["ledger_dead"] or x["proven_dead_by_yield"]
                                    or x.get("region_dead"))]
    dead = [x for x in out if (x["ledger_dead"] or x["proven_dead_by_yield"]
                               or x.get("region_dead"))]

    print(f"=== S0 选集增强 {a.region}/D{a.delay}/{a.universe} ===")
    print(f"点塔状态: {pyramid_status.get('lit_categories')}/{pyramid_status.get('total_categories')} "
          f"已点亮；未点亮塔: {', '.join(pyramid_status.get('unlit_category_ids') or [])}")
    print(f"[塔位快照 P1-4] {pyramid_snapshot['lit_count']}/{pyramid_snapshot['total']} 已点亮"
          f"（as_of {pyramid_snapshot['as_of']}；逐类明细写入 --json 产物）")
    print(f"候选: 平台推荐 {len(recommendations)} → 剔除已点亮塔 {len(lit_excluded)}（用户规则，--include-lit 可保留）"
          f" → 剔除判死 {len(dead)} → 存活 {len(alive)}")
    if region_dead["entries"]:
        print(f"[区域判死清单 P1-6] {len(region_dead['live'])} 条生效 / "
              f"{len(region_dead['stale'])} 条过期（只 advisory）"
              f"（{os.path.relpath(region_dead['path'], _REPO_ROOT)}）"
              + ("；--include-region-dead 已开（不剔除）" if include_region_dead else ""))
    if region_mech["entries"]:
        print(f"[机制标注 P0-4] {len(region_mech['live'])} 条生效 / "
              f"{len(region_mech['stale'])} 条过期；排序层 = 经典异象 > 未标注 > 明示非经典"
              f"（{os.path.relpath(region_mech['path'], _REPO_ROOT)}）")

    print(f"\n{'rank':>4} {'score':>7} {'yield':>7} {'bt':>4} {'maxS':>5} {'fld':>4} {'ac':>6} {'usr':>5} {'cat':13s} {'lit':>3}  dataset  [先验]")
    for i, x in enumerate(alive[:a.top_n], 1):
        yr_s = f"{x['hist_yield_rate']:.3f}" if x["hist_yield_rate"] is not None else "  -  "
        ms = f"{x['hist_max_sharpe']:.2f}" if x.get("hist_max_sharpe") is not None else "  - "
        fc_s = str(x["field_count"]) if x.get("field_count") is not None else "-"
        # P5（2026-09-25）：竞争度表面化——伪白空间教训（bt=0 ≠ 平台 alphaCount=0）
        ac = x.get("dataset_alpha_count")
        usr = x.get("dataset_user_count")
        ac_s = str(ac) if ac is not None else "-"
        usr_s = str(usr) if usr is not None else "-"
        tags = []
        if ac is not None:
            if ac <= 50:
                tags.append("低竞争")
            elif ac > 1000:
                tags.append(f"拥挤:ac={ac}(prod墙风险)")
        if x["conditioning_only"]:
            tags.append(f"fields<{a.min_fields}:仅条件腿")
        if not x["hist_backtested"] and x.get("hist_expressions"):
            tags.append(f"已有表达式{x['hist_expressions']}条未回测:非处女地")
        if x["xr_weak"]:
            tags.append("跨区弱:" + ",".join(x["xr_weak"][:3]))
        if x["xr_strong"]:
            tags.append("跨区RA-clean:" + ",".join(x["xr_strong"][:3]))
        if x.get("mechanism_tier") == 0:
            tags.append("机制:经典异象")
        elif x.get("mechanism_tier") == 2:
            tags.append("机制:非经典(慎)")
        if x.get("region_dead_stale"):
            tags.append("区域判死(过期,advisory)")
        print(f"{i:>4} {x['total_score']:>7.2f} {yr_s:>7} {x['hist_backtested']:>4} {ms:>5} {fc_s:>4} "
              f"{ac_s:>6} {usr_s:>5} {str(x['category']):13s} {'Y' if x['category_lit'] else 'N':>3}  "
              f"{x['dataset_id']} ({x['dataset_name']})" + (f"  [{'; '.join(tags)}]" if tags else ""))
    print("[强度×竞争度双查 P5] 开波准入 = 强度证据（maxS≥1.25 或 yield>0）× 竞争度（ac 列；"
          "≤50 低竞争 / >1000 拥挤→prod 墙风险）；缺强度证据不开波（零竞争≠有信号）。")
    print("[机制优先 P0-4] 排序第三层 = 机制是否经典异象（0 经典 > 1 未标注 > 2 明示非经典）；"
          "机制层只决定先试谁，开波前仍须 prod-probe（P0-1）。")
    if dead:
        print(f"\n[判死沉底 {len(dead)} 个]")
        for x in dead[:10]:
            reason = []
            if x["ledger_dead"]:
                reason.append("ledger_dead")
            if x["proven_dead_by_yield"]:
                reason.append(f"yield=0@{x['hist_backtested']}bt")
            if x.get("region_dead"):
                reason.append(f"region_dead:{(x.get('region_dead_verdict') or 'dead')}")
            print(f"  {x['dataset_id']:28s} cat={x['category']} ({'+'.join(reason)})"
                  + (f"  {x['region_dead_reason']}" if x.get("region_dead_reason") else ""))


    # P1（2026-09-14）：座位可达性预警。同族候选互相关高 → 一族只算 1 独立座位；
    #     Σest_seats（存活 top-n）< target 即「结构性不可达」，提示扩集/换区而非继续打磨。
    top_alive = alive[:a.top_n]
    total_seats = sum(int(x.get("est_seats") or 0) for x in top_alive)
    seat_src = "seat_model 台账" if seat_model else f"默认 {seats_default}/集（占位）"
    if a.target:
        print(f"\n[座位可达性 P1] target={a.target} 颗独立座位；存活 top{len(top_alive)} "
              f"Σest_seats={total_seats}（座位模型：{seat_src}）")
        if total_seats < a.target:
            print(f"  [WARN] 结构性不可达：即使每个存活候选都兑现其估计座位，总独立座位 "
                  f"{total_seats} 仍 < 目标 {a.target}（缺口 {a.target - total_seats}）。"
                  f"建议扩候选集 / 换区域 / 降同族相关，而非在已耗尽的池子里继续打磨。",
                  file=sys.stderr)
        else:
            print(f"  座位预算充足（Σest_seats {total_seats} >= target {a.target}）。")

    # P4（2026-09-14）：手工覆盖审计。白名单里被自动评分判 excluded/hard_excluded 却无
    #     override.reason 的条目 = 不可审计的人工覆盖，标 override-gap 提醒补注记。
    override_gaps = []
    for ds_id, cand in whitelist.items():
        rt = ranking_tier.get(ds_id)
        if not rt:
            continue
        auto_excluded = (rt.get("tier") == "excluded") or rt.get("hard_excluded")
        ov = cand.get("override")
        has_override = isinstance(ov, dict) and ov.get("reason")
        if auto_excluded and not has_override:
            override_gaps.append((ds_id, rt))
    if whitelist:
        print(f"\n[覆盖审计 P4] 白名单 {len(whitelist)} 集 × 自动排名交叉：")
        if override_gaps:
            print(f"  [WARN] {len(override_gaps)} 个 override-gap（被自动判 excluded/hard_excluded "
                  f"却手工纳入、且无 override.reason）：", file=sys.stderr)
            for ds_id, rt in override_gaps:
                why = "hard_excluded" if rt.get("hard_excluded") else f"tier={rt.get('tier')}"
                print(f"    - {ds_id:28s} 自动结论={why}；请在 s0_whitelist.candidates[].override "
                      f"补 {{reason, auto_tier, auto_excluded_by}} 使覆盖可审计", file=sys.stderr)
        else:
            print(f"  无 override-gap（白名单与自动评分一致，或覆盖均已注记 reason）。")

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump({
            "region": a.region, "delay": a.delay, "universe": a.universe,
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "pyramid_status": pyramid_status,
            "pyramid_snapshot": pyramid_snapshot,   # P1-4：每波 S0 产物必带塔位快照
            "candidates": out, "alive_count": len(alive), "dead_count": len(dead),
            # build_wave --max-size-auto 读这个键（Σest_seats × 2）；此前缺失导致该开关静默无效
            "est_seats": [int(x.get("est_seats") or 0) for x in alive[:a.top_n]],
            "seat_reachability": {  # P1
                "target": a.target, "total_est_seats": total_seats,
                "top_n_alive": len(top_alive), "seat_model_source": seat_src,
                "reachable": (total_seats >= a.target) if a.target else None,
            },
            "region_dead_list": {   # P1-6
                "path": os.path.relpath(region_dead["path"], _REPO_ROOT).replace("\\", "/"),
                "as_of": region_dead["as_of"],
                "review_after_days": region_dead["review_after_days"],
                "live": sorted(region_dead["live"]),
                "stale": sorted(region_dead["stale"]),
                "applied": not include_region_dead,
                "warning": region_dead["warning"],
            },
            "mechanism_map": {      # P0-4
                "path": os.path.relpath(region_mech["path"], _REPO_ROOT).replace("\\", "/"),
                "as_of": region_mech["as_of"],
                "review_after_days": region_mech["review_after_days"],
                "annotated": sorted(region_mech["live"]),
                "stale": sorted(region_mech["stale"]),
                "tiers": {x["dataset_id"]: x.get("mechanism_tier") for x in out},
                "warning": region_mech["warning"],
            },
            "override_gaps": [  # P4
                {"dataset": ds_id, "auto_tier": rt.get("tier"),
                 "auto_hard_excluded": rt.get("hard_excluded")}
                for ds_id, rt in override_gaps
            ],
        }, open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"\n[out] {a.json_out}")
    return 0


# ---------------------------------------------------------------------------
# pyramid：点塔进度快照
# ---------------------------------------------------------------------------

async def _cmd_pyramid(a):
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    alphas, mults = await asyncio.gather(
        brain.get_pyramid_alphas(),
        brain.get_pyramid_multipliers(),
    )

    # 平台原始返回是 {"pyramids": [{region, delay, category:{id}, alphaCount/multiplier}]}
    # 列表结构（MCP 层的嵌套 dict 是 _slim_pyramids 重塑后的）。此处直接解析列表。
    def _extract(payload, val_key):
        out = {}
        for p in (payload.get("pyramids") or []):
            if not isinstance(p, dict):
                continue
            if p.get("region") != a.region or int(p.get("delay", -1)) != a.delay:
                continue
            cat = p.get("category")
            cat_id = cat.get("id") if isinstance(cat, dict) else cat
            if cat_id:
                out[cat_id] = p.get(val_key)
        return out

    region_alphas = _extract(alphas, "alphaCount")
    region_mults = _extract(mults, "multiplier")

    cats = sorted(set(region_alphas) | set(region_mults))
    lit, unlit = [], []
    rows = []
    for cat in cats:
        n = region_alphas.get(cat, 0)
        m = region_mults.get(cat, 1.0)
        is_lit = n >= 3
        need = max(0, 3 - n)
        (lit if is_lit else unlit).append(cat)
        rows.append({"category": cat, "alpha_count": n, "multiplier": m,
                     "lit": is_lit, "need_to_light": need})
    # 未点亮优先（need 降序），点亮按乘数降序
    rows.sort(key=lambda r: (r["lit"], -r["need_to_light"], -r["multiplier"]))

    print(f"=== 点塔进度 {a.region}/D{a.delay} ===")
    print(f"已点亮 {len(lit)}/{len(cats)}: {', '.join(lit) or '(无)'}")
    print(f"未点亮 {len(unlit)}: {', '.join(unlit) or '(无)'}")
    print(f"\n{'cat':15s} {'alphas':>6} {'need':>4} {'mult':>5}  status")
    for r in rows:
        status = "LIT" if r["lit"] else f"差{r['need_to_light']}"
        print(f"{r['category']:15s} {r['alpha_count']:>6} {r['need_to_light']:>4} "
              f"{r['multiplier']:>5.1f}  {status}")

    payload = {"region": a.region, "delay": a.delay, "lit": lit, "unlit": unlit,
               "lit_count": len(lit), "total": len(cats), "rows": rows}
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(payload, open(a.json_out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"\n[out] {a.json_out}")
    # 机器可读单行（供 S6 key_findings 直接嵌入）
    print(f"\n[key_findings] {a.region}/D{a.delay} 点塔 {len(lit)}/{len(cats)} "
          f"已点亮({','.join(lit) or '无'}) 未点亮({','.join(unlit) or '无'})")
    return 0


# ---------------------------------------------------------------------------
# s4-prescreen：S4 预筛压缩（batch_get_alpha_metrics 分层）
# ---------------------------------------------------------------------------

async def _cmd_s4_prescreen(a):
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    alpha_ids = a.alpha_ids
    if a.ids_file:
        with open(a.ids_file, encoding="utf-8") as f:
            alpha_ids = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    if not alpha_ids:
        print("[s4-prescreen] 无 alpha_id 输入", file=sys.stderr)
        return 1

    # 逐条拉详情并分层（复刻 tools_alpha.batch_get_alpha_metrics 的分层逻辑，
    # 直接调 brain_client.get_alpha_details，不依赖 MCP 工具层包装）。
    # 硬闸口径与 judge 节点一致：sharpe>=1.58 / fitness>=1.0 / 2Y>=1.58 /
    # prod<=0.7 / self<=0.7 / turnover 0.04~0.40。
    SHARPE_MIN, FITNESS_MIN, TWO_Y_MIN = 1.58, 1.0, 1.58
    PROD_MAX, SELF_MAX = 0.7, 0.7
    TVR_LO, TVR_HI = 0.04, 0.40

    all_results, prescreen = [], {"READY": [], "REVIEW": [], "REJECT": []}
    for aid in alpha_ids:
        try:
            d = await brain.get_alpha_details(aid)
            m = d.get("metrics", {})
            item = {
                "alpha_id": aid,
                "sharpe": m.get("sharpe"), "fitness": m.get("fitness"),
                "turnover": m.get("turnover"), "two_year_sharpe": m.get("two_year_sharpe"),
                "robust_universe_sharpe": m.get("robust_universe_sharpe"),
                "sub_universe_sharpe": m.get("sub_universe_sharpe"),
                "margin": m.get("margin"), "returns": m.get("returns"),
                "drawdown": m.get("drawdown"),
                "self_correlation": m.get("selfCorrelation"),
                "prod_correlation": m.get("prodCorrelation"),
                "status": d.get("status"), "error": None,
            }
        except Exception as e:
            item = {"alpha_id": aid, "error": str(e)}
            all_results.append(item)
            prescreen["REJECT"].append(aid)
            continue
        all_results.append(item)

        sharpe = item["sharpe"] or 0
        fitness = item["fitness"] or 0
        two_year = item["two_year_sharpe"] or 0
        prod = item["prod_correlation"] if item["prod_correlation"] is not None else 0
        selfc = item["self_correlation"] if item["self_correlation"] is not None else 0
        tvr = item["turnover"] or 0
        hard_pass = (sharpe >= SHARPE_MIN and fitness >= FITNESS_MIN
                     and two_year >= TWO_Y_MIN and prod <= PROD_MAX and selfc <= SELF_MAX)
        any_signal = sharpe >= 1.0 or fitness >= 0.5
        tvr_ok = TVR_LO <= tvr <= TVR_HI
        if hard_pass and tvr_ok:
            prescreen["READY"].append(aid)
        elif any_signal:
            prescreen["REVIEW"].append(aid)
        else:
            prescreen["REJECT"].append(aid)

    print(f"=== S4 预筛 {len(alpha_ids)} 个 alpha ===")
    print(f"READY {len(prescreen['READY'])} / REVIEW {len(prescreen['REVIEW'])} / "
          f"REJECT {len(prescreen['REJECT'])}")
    print(f"\n[READY] 全硬闸通过 → 进 S4 完整评审链:")
    for rid in prescreen["READY"]:
        print(f"  {rid}")
    print(f"\n[REVIEW] 部分达标 → 进 S4 链但标注短板:")
    for rid in prescreen["REVIEW"]:
        print(f"  {rid}")
    print(f"\n[REJECT] 全灭 → 直接判死，不进 S4 链（省评审配额）:")
    for r in all_results:
        if r.get("alpha_id") in set(prescreen["REJECT"]):
            print(f"  {r.get('alpha_id')}  sharpe={r.get('sharpe')} fitness={r.get('fitness')} "
                  f"turnover={r.get('turnover')}")

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump({"total": len(alpha_ids), "prescreen": prescreen, "results": all_results},
                  open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"\n[out] {a.json_out}")
    # REJECT 非空时退出码 1（有判死项），供 pipeline 感知
    return 0


# ---------------------------------------------------------------------------
# prod-first：收批后族级 prod 探针（2026-09-19）
# ---------------------------------------------------------------------------
# 背景：全区绑定约束是 PROD_CORRELATION（2026-09-18 库存 22/22 撞墙 0.80-0.99；IND 已测 104 条
# 中 73% 撞墙），而流水线把 prod 检查排在最后一步（平台单并发排队）→ 先烧满回测槽位、最后才知道
# 整族不可提交。SOP "每槽先 1-2 条骨架查 prod_corr；≥0.7 停扩换腿" 此前只是口头纪律。
# 本命令把它做成收批后的固定动作：每个信号族（字段集合）取最强 1 条串行探 prod，族级给 EXPAND/STOP。

_PF_OPS = set("""
rank add multiply subtract divide group_rank group_zscore group_neutralize group_mean group_sum
group_count group_scale group_std_dev group_backfill ts_mean ts_delta ts_zscore ts_rank ts_backfill
ts_decay_linear ts_std_dev ts_sum ts_max ts_min ts_corr ts_covariance ts_regression ts_av_diff
ts_arg_max ts_arg_min ts_product ts_quantile ts_count_nans ts_scale ts_step ts_returns ts_ir
ts_delay ts_kurtosis ts_max_diff vec_avg vec_sum vec_max vec_min vec_stddev vec_count vec_range
winsorize scale normalize signed_power quantile power reverse zscore abs log sign sqrt inverse
densify pasteurize hump kth_element trade_when if_else bucket greater less equal and or not is_nan
not_equal less_equal greater_equal max min days_from_last_change last_diff_value vector_neut tail
industry sector subindustry market country exchange std range rettype driver buckets
""".split())


def _pf_family(code):
    """信号族 = 表达式里的字段集合（去算子/常数）。同族只探最强一条。"""
    import re
    toks = {t for t in re.findall(r"[a-z][a-z0-9_]{3,}", code or "") if t not in _PF_OPS}
    return "+".join(sorted(toks)) or "?"


def _pf_ra_clean(row):
    rf = (row.get("ra_failed_checks") or "").strip()
    return rf in ("", "[]")


def _pf_pick_probes(rows, top_k, min_sharpe, sharpe_min, fitness_min):
    """纯函数（单测用）：RA-clean 优先、其次 |S|≥min_sharpe；同族只留最强；最多 top_k 个族。"""
    def _rank_key(r):
        s = abs(r.get("sharpe") or 0)
        clean = _pf_ra_clean(r) and s >= sharpe_min and (r.get("fitness") or 0) >= fitness_min
        return (0 if clean else 1, -s)
    pool = [r for r in rows if abs(r.get("sharpe") or 0) >= min_sharpe]
    pool.sort(key=_rank_key)
    seen, probes = set(), []
    for r in pool:
        fam = _pf_family(r.get("code"))
        if fam in seen:
            continue
        seen.add(fam)
        probes.append(dict(r, family=fam))
        if len(probes) >= top_k:
            break
    return probes


def _pf_verdict(prod, status, prod_max):
    if prod is None:
        return f"UNKNOWN({status})"
    return ("STOP(prod>=%.2f)" % prod_max) if prod >= prod_max else "EXPAND"


async def _pf_probe_one(brain, aid, a):
    """单条 alpha 的 prod 探测循环（pending/busy 重试 + 单条硬超时）。返回 (prod, status)。

    prod-first / prod-probe 共用（2026-10-24 P0-1 抽自 `_cmd_prod_first`，行为逐字不变）。
    走 `brain.check_correlation` ⇒ 自动继承账号级 correlation 泳道锁与 48h 已决缓存。
    """
    prod, status, tries = None, None, 0
    while tries < a.max_tries:
        tries += 1
        try:
            res = await asyncio.wait_for(
                brain.check_correlation(aid, correlation_type="production",
                                        threshold=a.prod_max, refresh=a.refresh),
                timeout=a.probe_timeout)
        except asyncio.TimeoutError:
            status = f"timeout({a.probe_timeout}s)"
            print(f"  {aid}: 平台 PC 数据 {a.probe_timeout}s 未就绪，跳过（下次 --refresh 重查）")
            break
        except Exception as e:
            status = f"error: {str(e)[:120]}"
            break
        chk = (res.get("checks") or {}).get("production") or {}
        status = res.get("status") or chk.get("status") or (
            "ok" if chk.get("max_correlation") is not None else "unknown")
        if chk.get("max_correlation") is not None:
            prod = float(chk["max_correlation"])
            break
        if status in ("pending", "correlation_busy"):
            wait = int(chk.get("retry_after") or a.poll_sec)
            print(f"  {aid}: {status}，{wait}s 后重试（{tries}/{a.max_tries}）")
            time.sleep(wait)
            continue
        break
    return prod, status


async def _cmd_prod_first(a):
    import sqlite3
    import time
    from brain_api import BrainApiClient  # noqa: F402

    db = os.path.join(_REPO_ROOT, "data", "wqb.db")
    conn = db_connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT alpha_id, sharpe, fitness, turnover, two_year_sharpe, ra_failed_checks, code, dataset "
        "FROM backtest_results WHERE region=? AND wave=? AND alpha_id IS NOT NULL AND alpha_id<>''",
        (a.region, str(a.wave)))
    rows = [dict(r) for r in cur.fetchall()]
    if not rows:
        print(f"[prod-first] {a.region} wave={a.wave} 无回测行", file=sys.stderr)
        return 1

    probes = _pf_pick_probes(rows, a.top_k, a.min_sharpe, a.sharpe_min, a.fitness_min)
    if not probes:
        print(f"[prod-first] 本波无 |sharpe|>={a.min_sharpe} 的候选，无需探 prod（全灭波）")
        return 0

    # 2026-09-19：平台 prod 计算单并发；两个 prod-first 进程并跑只会互相排队（IND w178 实证：
    # 第一次查询后卡住 >10 分钟）。进程锁 + 单条硬超时（--probe-timeout，缺省 600s）。
    lock = _pf_acquire_lock()
    if lock is None and not getattr(a, "no_lock", False):
        print("[prod-first] 另一个 prod-first 进程正在跑（锁文件 data/.prod_first.lock），本次退出；"
              "--no-lock 可强行并跑", file=sys.stderr)
        return 3
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    results = []
    print(f"=== prod-first {a.region} wave={a.wave}：{len(probes)} 个信号族各探 1 条（平台单并发，串行）===")
    for r in probes:
        aid = r["alpha_id"]
        prod, status = await _pf_probe_one(brain, aid, a)
        verdict = _pf_verdict(prod, status, a.prod_max)
        results.append({"alpha_id": aid, "family": r["family"], "dataset": r.get("dataset"),
                        "sharpe": r.get("sharpe"), "fitness": r.get("fitness"),
                        "ra_clean": _pf_ra_clean(r), "prod_correlation": prod, "status": status,
                        "verdict": verdict})
        prod_s = f"{prod:.4f}" if prod is not None else "-"
        print(f"  {aid:10s} S={r.get('sharpe') or 0:5.2f} F={r.get('fitness') or 0:5.2f} "
              f"ra_clean={str(_pf_ra_clean(r)):5s} prod={prod_s:>7} -> {verdict}  [{r['family'][:70]}]")
        # 已有 alphas 行则回写（不新建行：alphas 需要 region_id/dataset_id 外键）
        if prod is not None:
            cur.execute("UPDATE alphas SET prod_correlation=?, prod_corr_source='prod_first', "
                        "corr_checked_at=CURRENT_TIMESTAMP WHERE alpha_id=?", (prod, aid))
    conn.commit()
    summary_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    # 2026-09-25 P1：骨架指纹自学习 —— 把每条探针的骨架指纹 + prod 结果回写 ledger_kv，
    # 让闸 PF（wave_gate._load_prod_wall_families）下次跑时直接读到最新证据，
    # 不再只依赖 alphas 表的稀疏记录（全库 prod 覆盖率仅 4.4%）。
    try:
        import sys as _sys_pf, os as _os_pf
        _tools_dir = _os_pf.path.dirname(_os_pf.path.abspath(__file__))
        if _tools_dir not in _sys_pf.path:
            _sys_pf.path.insert(0, _tools_dir)
        from wave_gate import _pf_family as _skel_fp
        n_fp = 0
        for x in results:
            if x.get("prod_correlation") is None:
                continue
            fam = _skel_fp(x.get("code") or x.get("expression") or "")
            if not fam or fam == "?":
                continue
            key = f"prod_family_{a.region}_{fam}"
            cur.execute("INSERT INTO ledger_kv(region, key, value) VALUES(?,?,?) "
                        "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
                        "updated_at=CURRENT_TIMESTAMP",
                        (a.region, key, json.dumps(
                            {"prod_corr": x["prod_correlation"], "at": summary_at,
                             "alpha_id": x["alpha_id"], "n": 1}, ensure_ascii=False)))
            n_fp += 1
        conn.commit()
        print(f"[ledger] 骨架指纹自学习：{n_fp} 个 prod_family_* 键已写")
    except Exception as _e_fp:
        print(f"[ledger] 骨架指纹回写失败（不阻断）: {_e_fp}", file=sys.stderr)

    n_stop = sum(1 for x in results if x["verdict"].startswith("STOP"))
    n_expand = sum(1 for x in results if x["verdict"] == "EXPAND")
    summary_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    summary = {"region": a.region, "wave": str(a.wave), "probed": len(results),
               "stop": n_stop, "expand": n_expand,
               "unknown": len(results) - n_stop - n_expand, "prod_max": a.prod_max,
               "results": results, "at": summary_at}
    print(f"\n[prod-first] 族级结论：EXPAND={n_expand} STOP={n_stop} UNKNOWN={summary['unknown']}")
    if n_stop and not n_expand:
        print("[prod-first] 本波全部探针撞 prod 墙：该数据集/信号族对生产池同质，"
              "下一波换族/换集（决策表 D0：撞 prod-corr 墙 → 换白名单不同数据集 regenerate，勿磨同腿变体）")
    if a.write_ledger:
        try:
            # ledger_kv.region 存区域名（VARCHAR），不是 regions.id
            key = f"prod_first_{a.wave}"
            cur.execute("INSERT INTO ledger_kv(region, key, value) VALUES(?,?,?) "
                        "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
                        "updated_at=CURRENT_TIMESTAMP",
                        (a.region, key, json.dumps(summary, ensure_ascii=False)))
            conn.commit()
            print(f"[ledger] {a.region}/{key} 已写")
        except Exception as e:
            print(f"[ledger] 写入失败（不阻断）: {e}")
    conn.close()
    _pf_release_lock(lock)
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(summary, open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"[out] {a.json_out}")
    return 0


_PF_LOCK = os.path.join(_REPO_ROOT, "data", ".prod_first.lock")


def _pid_alive(pid):
    try:
        if os.name == "nt":
            import ctypes
            h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
            if not h:
                return False
            try:
                code = ctypes.c_ulong()
                ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
                return bool(ok) and code.value == 259
            finally:
                ctypes.windll.kernel32.CloseHandle(h)
        os.kill(int(pid), 0)
        return True
    except Exception:
        return False


def _pf_acquire_lock():
    """prod-first 进程锁：锁文件存 pid；持锁进程已死则回收。返回锁路径或 None（被占）。"""
    try:
        if os.path.exists(_PF_LOCK):
            try:
                pid = int(open(_PF_LOCK, encoding="utf-8").read().strip() or 0)
            except Exception:
                pid = 0
            if pid and pid != os.getpid() and _pid_alive(pid):
                return None
        with open(_PF_LOCK, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
        return _PF_LOCK
    except Exception:
        return _PF_LOCK  # 锁不可用时不阻断


def _pf_release_lock(lock):
    if lock:
        try:
            os.remove(lock)
        except OSError:
            pass


async def _cmd_prod_probe(a):
    """开波前族级 prod 探针（P0-1，2026-10-24；报告 reports/usa_mining_history_review_20261023.md §10）。

    与 prod-first 的差别在**时机与探针源**：
      prod-first = 收批后对本波行探（`WHERE region=? AND wave=?`），产出「本波族级 STOP/EXPAND」；
      prod-probe = 开波前对本集**全部历史**行探（跨所有波次），产出「封族清单」——
                   命中 prod ≥ --prod-max（缺省 0.75，= 闸 PF 的 `PROBE_SEAL_THRESHOLD`）的
                   信号族写带 `probe: true` 的死路指纹，闸 PF 下次跑即 enforced 拦截，
                   不再花整波回测槽才发现撞墙（USA 实测 13/110 波投在事后撞墙族）。
    取证口径：每族只花 1 颗探针的 prod 额度（只占平台 prod 队列，不占回测槽）；
    走 `BrainApiClient.check_correlation`（继承 correlation 泳道锁 + 48h 已决缓存）。

    新集无历史时无从取材 → 打印提示并 exit 0（该场景走 P1-1 首波裸探针）。
    退出码：0=探针完成且无族被封 / 2=有族被封（勿开该族整波）/ 3=锁被占。
    """
    import sqlite3

    db = db_connect(os.path.join(_REPO_ROOT, "data", "wqb.db"))
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        "SELECT alpha_id, sharpe, fitness, turnover, two_year_sharpe, ra_failed_checks, code, wave "
        "FROM backtest_results WHERE region=? AND dataset=? AND alpha_id IS NOT NULL AND alpha_id<>''",
        (a.region, a.dataset))
    rows = [dict(r) for r in cur.fetchall()]
    if not rows:
        print(f"[prod-probe] {a.region}/{a.dataset} 无历史回测行（新集）：prod 探针无从取材；"
              f"按 P1-1 先发 1 条裸探针验强度，首波收批后由 prod-first 补指纹", file=sys.stderr)
        db.close()
        return 0

    probes = _pf_pick_probes(rows, a.top_k, a.min_sharpe, a.sharpe_min, a.fitness_min)
    if not probes:
        print(f"[prod-probe] {a.region}/{a.dataset} 历史 {len(rows)} 行但无 |S|≥{a.min_sharpe} 候选："
              f"整族无强度证据，先发裸探针（P1-1）再谈 prod", file=sys.stderr)
        db.close()
        return 0

    if a.dry_run:
        print(f"[prod-probe] dry-run：拟探 {len(probes)} 个族（不联网、不写库）")
        for r in probes:
            print(f"  {r['alpha_id']:10s} S={r.get('sharpe') or 0:5.2f} wave={r.get('wave')}  "
                  f"[{r['family'][:70]}]")
        db.close()
        return 0

    # 与 prod-first 共用同一把进程锁（平台 prod 单并发；并跑只会互相排队，IND w178 实证）
    lock = _pf_acquire_lock()
    if lock is None and not getattr(a, "no_lock", False):
        print("[prod-probe] 另一个 prod 探针进程（prod-first / prod-probe）正在跑"
              "（锁文件 data/.prod_first.lock），本次退出；--no-lock 可强行并跑", file=sys.stderr)
        db.close()
        return 3
    # 延迟到真正要联网才导入 MCP 栈：早退路径（新集 / 无强度 / --dry-run / 锁被占）
    # 因此完全不依赖 world-quant-brain-mcp 环境（与仓内 dry-run 契约一致）。
    from brain_api import BrainApiClient  # noqa: F402

    brain = BrainApiClient()
    await brain.ensure_authenticated()
    results = []
    started_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"=== prod-probe {a.region}/{a.dataset}（开波前）：{len(probes)} 个信号族各探 1 条"
          f"（历史全波次最强，平台单并发串行）===")
    for r in probes:
        aid = r["alpha_id"]
        prod, status = await _pf_probe_one(brain, aid, a)
        sealed = prod is not None and prod >= a.prod_max
        verdict = "SEAL" if sealed else _pf_verdict(prod, status, a.prod_max)
        results.append({"alpha_id": aid, "family": r["family"], "wave": r.get("wave"),
                        "sharpe": r.get("sharpe"), "fitness": r.get("fitness"),
                        "ra_clean": _pf_ra_clean(r), "prod_correlation": prod, "status": status,
                        "sealed": sealed, "verdict": verdict, "code": r.get("code")})
        prod_s = f"{prod:.4f}" if prod is not None else "-"
        print(f"  {aid:10s} S={r.get('sharpe') or 0:5.2f} F={r.get('fitness') or 0:5.2f} "
              f"ra_clean={str(_pf_ra_clean(r)):5s} prod={prod_s:>7} -> {verdict}  [{r['family'][:70]}]")
        # 已有 alphas 行则回写（不新建行：alphas 需要 region_id/dataset_id 外键）
        if prod is not None:
            cur.execute("UPDATE alphas SET prod_correlation=?, prod_corr_source='prod_probe', "
                        "corr_checked_at=CURRENT_TIMESTAMP WHERE alpha_id=?", (prod, aid))
    db.commit()

    # 骨架指纹自学习（带 probe 标记）：闸 PF（wave_gate_pkg.gates_pf._load_prod_wall_families）
    # 读到 probe=true 且 prod_max ≥ PROBE_SEAL_THRESHOLD 的族即 enforced 拦截——这是「封族」的
    # 代码级落点，与 prod-first 的指纹同一存储面（prod_family_<region>_<骨架>）。
    n_fp, n_sealed_fp = 0, 0
    probe_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        import sys as _sys_pf, os as _os_pf
        _tools_dir = _os_pf.path.dirname(_os_pf.path.abspath(__file__))
        if _tools_dir not in _sys_pf.path:
            _sys_pf.path.insert(0, _tools_dir)
        from wave_gate import _pf_family as _skel_fp
        for x in results:
            if x.get("prod_correlation") is None:
                continue
            fam = _skel_fp(x.get("code") or x.get("expression") or "")
            if not fam or fam == "?":
                continue
            key = f"prod_family_{a.region}_{fam}"
            cur.execute("INSERT INTO ledger_kv(region, key, value) VALUES(?,?,?) "
                        "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
                        "updated_at=CURRENT_TIMESTAMP",
                        (a.region, key, json.dumps(
                            {"prod_corr": x["prod_correlation"], "at": probe_at,
                             "alpha_id": x["alpha_id"], "n": 1, "probe": True,
                             "sealed": x["sealed"], "dataset": a.dataset},
                            ensure_ascii=False)))
            n_fp += 1
            if x["sealed"]:
                n_sealed_fp += 1
        db.commit()
        print(f"[ledger] 骨架指纹自学习：{n_fp} 个 prod_family_* 键已写（其中封族 {n_sealed_fp}）")
    except Exception as _e_fp:
        print(f"[ledger] 骨架指纹回写失败（不阻断）: {_e_fp}", file=sys.stderr)

    sealed_rows = [x for x in results if x["sealed"]]
    clean_rows = [x for x in results if x["prod_correlation"] is not None and not x["sealed"]]
    summary = {"region": a.region, "dataset": a.dataset, "probed": len(results),
               "sealed": len(sealed_rows), "clean": len(clean_rows),
               "unknown": len(results) - len(sealed_rows) - len(clean_rows),
               "prod_max": a.prod_max, "started_at": started_at, "at": probe_at,
               "sealed_families": [{"family": x["family"], "alpha_id": x["alpha_id"],
                                    "prod_corr": x["prod_correlation"]} for x in sealed_rows],
               "results": results}
    print(f"\n[prod-probe] 族级结论：SEAL={len(sealed_rows)} CLEAN={len(clean_rows)} "
          f"UNKNOWN={summary['unknown']}（探测→封族耗时 {started_at} → {probe_at}）")
    if sealed_rows:
        print("[prod-probe] 封族清单（勿开整波；换正交概念/换族/换集）：")
        for x in sealed_rows:
            print(f"  · {x['family'][:80]}  probe={x['prod_correlation']:.4f}")
    try:
        key = f"prod_probe_{a.region}_{a.dataset}"
        cur.execute("INSERT INTO ledger_kv(region, key, value) VALUES(?,?,?) "
                    "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
                    "updated_at=CURRENT_TIMESTAMP",
                    (a.region, key, json.dumps(summary, ensure_ascii=False)))
        db.commit()
        print(f"[ledger] {a.region}/{key} 已写")
    except Exception as e:
        print(f"[ledger] 写入失败（不阻断）: {e}")
    db.close()
    _pf_release_lock(lock)
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(summary, open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"[out] {a.json_out}")
    return 2 if sealed_rows else 0



# ---------------------------------------------------------------------------
# backlog-drop：积压波清理（2026-09-19）
# ---------------------------------------------------------------------------
# 背景：wave-key-check / wave-ttl-check 长期报 300+ 活跃波 / 18k 表达式积压（JPN s2_* 模板池 7.5k 等），
# 既没人回测也没人 dropped，每次开 store 都刷 WARN。本命令把「超 N 天未动、无任何回测行、
# 无 gate_results」的 pending/gated 波整体标 dropped（表达式 status=dropped，波 status=dropped），
# 默认 dry-run 只列清单；--apply 才写库。已回测过的波（有 backtest_results）一律不动。

async def _cmd_backlog_drop(a):
    import sqlite3
    db = os.path.join(_REPO_ROOT, "data", "wqb.db")
    conn = db_connect(db, timeout=30)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    regions = [r.strip().upper() for r in (a.region or "").split(",") if r.strip()]
    cur.execute(
        """
        SELECT w.id AS wid, w.wave_number AS wave, r.name AS region, w.status AS wstatus,
               COUNT(e.id) AS n_expr, MAX(COALESCE(e.updated_at, e.created_at)) AS last_touch,
               (SELECT COUNT(*) FROM backtest_results b WHERE b.region=r.name AND b.wave=w.wave_number) AS n_bt,
               (SELECT COUNT(*) FROM gate_results g WHERE g.region=r.name AND g.wave=w.wave_number) AS n_gate,
               (SELECT g2.all_pass FROM gate_results g2 WHERE g2.region=r.name AND g2.wave=w.wave_number
                  ORDER BY g2.id DESC LIMIT 1) AS gate_all_pass
        FROM waves w JOIN regions r ON r.id=w.region_id
        LEFT JOIN expressions e ON e.wave_id=w.id AND e.status NOT IN ('superseded','dropped')
        WHERE w.status IN ('pending','gated')
        GROUP BY w.id
        ORDER BY n_expr DESC
        """)
    rows = [dict(r) for r in cur.fetchall()]
    import datetime as _dt
    cutoff = (_dt.datetime.now() - _dt.timedelta(days=a.older_than_days)).strftime("%Y-%m-%dT%H:%M:%S")
    todo = []
    for r in rows:
        if r["n_expr"] == 0 and not a.drop_zero_expr:
            # 零活表达式死波：无候选可清，默认跳过（保持原契约）；
            # --drop-zero-expr 时才把这类波一起标 dropped，清掉 stale 统计噪声。
            continue
        if regions and r["region"] not in regions:
            continue
        if r["n_bt"] > 0 and not a.include_backtested:
            continue
        if r["n_gate"] > 0 and not a.include_gated:
            continue
        if a.drop_gate_fail_only and r.get("gate_all_pass") == 1:
            # 只清最新 gate_results.all_pass=1 之外的波（闸未判死的空壳波 all_pass=None 一并清，
            # all_pass=0 已判死的波可配 --include-gated 才清）；
            # 仅保护 all_pass=1 的活波（如 KOR 97/98/101），不会误清。
            continue
        lt = (r["last_touch"] or "").replace(" ", "T")
        if lt and lt > cutoff:
            continue
        if a.pattern and a.pattern not in str(r["wave"]):
            continue
        todo.append(r)
    n_expr = sum(r["n_expr"] for r in todo)
    print(f"=== backlog-drop：{'APPLY' if a.apply else 'DRY-RUN'}  阈值 >{a.older_than_days} 天未动、无回测"
          f"{'' if a.include_gated else '、无 gate_results'}  → 命中 {len(todo)} 波 / {n_expr} 条表达式 ===")
    for r in todo[:a.show]:
        print(f"  {r['region']:4s} {str(r['wave']):40s} {r['n_expr']:6d} 条  last={str(r['last_touch'])[:10]}  gate={r['n_gate']} bt={r['n_bt']}")
    if len(todo) > a.show:
        print(f"  ... 另 {len(todo) - a.show} 波")
    if a.apply and todo:
        n_e = 0
        for r in todo:
            cur.execute("UPDATE expressions SET status='dropped', updated_at=CURRENT_TIMESTAMP "
                        "WHERE wave_id=? AND status NOT IN ('superseded','dropped')", (r["wid"],))
            n_e += cur.rowcount
            cur.execute("UPDATE waves SET status='dropped' WHERE id=?", (r["wid"],))
        conn.commit()
        print(f"[backlog-drop] 已标 dropped：{len(todo)} 波 / {n_e} 条表达式（可用 SQL 按 wave 恢复）")
    # ---- 已回测却仍 pending/gated 的波：状态卫生（旧版 pipeline 不翻 waves.status）----
    if a.close_backtested:
        cur.execute(
            """
            SELECT w.id AS wid, w.wave_number AS wave, r.name AS region,
                   SUM(CASE WHEN e.id IS NOT NULL AND (e.alpha_id IS NULL OR e.alpha_id='')
                            THEN 1 ELSE 0 END) AS n_unrun,
                   COUNT(e.id) AS n_expr, MAX(COALESCE(e.updated_at, e.created_at)) AS last_touch
            FROM waves w JOIN regions r ON r.id=w.region_id
            LEFT JOIN expressions e ON e.wave_id=w.id AND e.status NOT IN ('superseded','dropped')
            WHERE w.status IN ('pending','gated')
              AND EXISTS (SELECT 1 FROM backtest_results b WHERE b.region=r.name AND b.wave=w.wave_number)
            GROUP BY w.id
            """)
        closable = []
        for r in cur.fetchall():
            r = dict(r)
            if regions and r["region"] not in regions:
                continue
            lt = (r["last_touch"] or "").replace(" ", "T")
            # 2026-09-25 修复：n_unrun 在无活表达式时为 NULL，NULL==0 为 False
            # 使"全已回测、无残留表达式"的波永远进不了 closable。改为 not n_unrun
            # 覆盖 NULL 与 0 两种情形。
            if not r["n_unrun"] or (lt and lt <= cutoff):
                closable.append(r)
        n_unrun = sum(r["n_unrun"] for r in closable)
        print(f"[backlog-drop] 已回测但仍 pending/gated 的波：{len(closable)} 波可 closed"
              f"（其中 {n_unrun} 条从未回测的残留表达式将标 dropped）")
        if a.apply and closable:
            n_e = 0
            for r in closable:
                cur.execute("UPDATE expressions SET status='dropped', updated_at=CURRENT_TIMESTAMP "
                            "WHERE wave_id=? AND (alpha_id IS NULL OR alpha_id='') "
                            "AND status NOT IN ('superseded','dropped')", (r["wid"],))
                n_e += cur.rowcount
                cur.execute("UPDATE waves SET status='closed' WHERE id=?", (r["wid"],))
            conn.commit()
            print(f"[backlog-drop] 已 closed {len(closable)} 波，dropped 残留 {n_e} 条")
    conn.close()
    return 0

# ---------------------------------------------------------------------------
# mark-saturated：S6→S0 饱和反馈的写入口（2026-09-29，skills 审查 RA-113 / IX-20）
#   S0 打分（score_datasets.apply_saturation_demotion / P5 拍平 model）读 ledger `saturated_datasets`，
#   此前全仓库没有任何写入方；S6 文档教写的 `submit_ready_blocked` 只被 step_funnel 计数，反馈永远不生效。
# ---------------------------------------------------------------------------

_SATURATED_KEY = "saturated_datasets"


def _merge_saturated(existing, datasets, reason=None, wave=None, prod_corr=None, remove=False, now=None):
    """纯函数：把 datasets 并入（或 remove=True 时移出）`saturated_datasets` 台账值。

    返回 (新值, 变更清单[(action, dataset)])。台账形状固定为 `{"datasets": {ds: {reason, updated, ...}}}`
    （score_datasets.apply_saturation_demotion 读取 reason；其余键仅作审计）。
    """
    val = dict(existing) if isinstance(existing, dict) else {}
    cur = val.get("datasets")
    dss = dict(cur) if isinstance(cur, dict) else {}
    changed = []
    for ds in datasets:
        if remove:
            if ds in dss:
                dss.pop(ds)
                changed.append(("removed", ds))
            continue
        rec = {"reason": reason, "updated": now}
        if wave is not None:
            rec["source_wave"] = str(wave)
        if prod_corr is not None:
            rec["prod_corr"] = prod_corr
        changed.append(("updated" if ds in dss else "added", ds))
        dss[ds] = rec
    val["datasets"] = dss
    return val, changed


async def _cmd_mark_saturated(a):
    datasets = [d.strip() for d in (a.dataset or []) if d and d.strip()]
    if not datasets:
        print("[mark-saturated] 需要至少一个 --dataset", file=sys.stderr)
        return 1
    if not a.remove and not (a.reason or "").strip():
        print("[mark-saturated] 登记饱和须给 --reason（供 S0 tier_note 与人工复核）；撤销请用 --remove", file=sys.stderr)
        return 1
    conn = db_connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT value FROM ledger_kv WHERE region=? AND key='saturated_datasets'", (a.region,))
        row = cur.fetchone()
        try:
            existing = json.loads(row[0]) if row and row[0] else {}
        except (TypeError, ValueError):
            existing = {}
        now = time.strftime("%Y-%m-%dT%H:%M:%S")
        new, changed = _merge_saturated(existing, datasets, (a.reason or "").strip(), a.wave,
                                        a.prod_corr, a.remove, now)
        if not changed:
            print(f"[mark-saturated] {a.region}/{_SATURATED_KEY}：无变更")
            return 0
        for act, ds in changed:
            print(f"[mark-saturated] {a.region}: {ds} → {act}")
        if not a.write_ledger:
            print("[mark-saturated] dry-run（加 --write-ledger 落库；S0 下一次打分即读取）")
            return 0
        cur.execute("INSERT INTO ledger_kv(region, key, value) VALUES(?, 'saturated_datasets', ?) "
                    "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
                    "updated_at=CURRENT_TIMESTAMP",
                    (a.region, json.dumps(new, ensure_ascii=False)))
        conn.commit()
        print(f"[ledger] {a.region}/{_SATURATED_KEY} 已写（{len(new['datasets'])} 个数据集处于饱和态）")
        return 0
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# ghost-audit：幽灵算子硬闸
# ---------------------------------------------------------------------------

async def _cmd_ghost_audit(a):
    # 幽灵算子检测是纯本地操作（wqb.expression.operator_audit 的 ghost 集合 +
    # grammar.extract_identifiers），无需 brain_client / 平台调用。
    exprs = a.exprs or []
    if a.exprs_file:
        with open(a.exprs_file, encoding="utf-8") as f:
            exprs.extend(l.strip() for l in f if l.strip() and not l.startswith("#"))
    if not exprs:
        print("[ghost-audit] 无表达式输入", file=sys.stderr)
        return 1

    try:
        from wqb.expression.operator_audit import get_ghost_operators
        from wqb.expression.grammar import extract_identifiers
    except ImportError as e:
        print(f"[ghost-audit] wqb.expression 不可用: {e}", file=sys.stderr)
        return 1

    ghosts = get_ghost_operators()
    violations = []
    for expr in exprs:
        used = extract_identifiers(expr)
        bad = sorted(used & ghosts)
        if bad:
            violations.append({"expression": expr, "ghost_ops": bad})

    print(f"=== 幽灵算子审计 {len(exprs)} 条表达式 ({a.region}/D{a.delay}) ===")
    if not violations:
        print("PASS：无幽灵算子")
        return 0
    print(f"FAIL：{len(violations)} 条含幽灵算子（dispatch 前硬闸拦截）")
    for v in violations:
        print(f"  {v.get('expression')}")
        print(f"    ghost_ops: {v.get('ghost_ops')}")
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump({"safe": False, "total_expressions": len(exprs),
                   "violations": violations, "ghost_operators": sorted(ghosts)},
                  open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"\n[out] {a.json_out}")
    return 1


# ---------------------------------------------------------------------------
# atom-first：ATOM 优先候选单（2026-10-26 用户指令「ATOM 优先，其他只作备选」）
# ---------------------------------------------------------------------------

#: 判据单一口径源是 `wqb.expression.atom.classify_atom`；这里只消费落库的 atom_flag。
ATOM_RULE_TEXT = (
    "ATOM = 单数据集（平台文档 single-dataset-alphas）：非豁免字段的 dataset id 必须唯一；"
    "基础行情属 pv1；inst_pnl()/convert() 视为引用 pv1；豁免分组键恰好 6 个"
    "（country/exchange/market/sector/industry/subindustry）。"
)


#: 平台 `failed_checks` 名 → 本工具五闸维度。用于把「平台已经判 FAIL」的行拉回真实状态：
#: 只按 config 的宽线（TO≤0.70）筛会把 IND 这类区域**平台线更严**（HIGH_TURNOVER 0.40）的行
#: 误报成「全过」——实测 `A1NJVm3e` TO 0.4722、本地「全过」，平台 checks 里是 HIGH_TURNOVER FAIL。
PLAT_FAIL_TO_DIM = {
    "LOW_SHARPE": "S",
    "LOW_FITNESS": "F",
    "LOW_2Y_SHARPE": "2Y",
    "IS_LADDER_SHARPE": "2Y",
    "LOW_SUB_UNIVERSE_SHARPE": "sub",
    "LOW_TURNOVER": "TO",
    "HIGH_TURNOVER": "TO",
}


def _atom_gate_flags(sharpe, fitness, two_year, sub, turnover, delay=1, turnover_max=None):
    """返回 (未过闸名单, 过闸数)。线全部来自 config，避免本工具自创阈值。

    ``turnover_max`` 可覆盖上限（如 IND/D1 平台 HIGH_TURNOVER 实际线是 0.40，
    config 的 0.70 只是全局宽线）。
    """
    from wqb.config import PLATFORM_CHECK_LINES

    ls = PLATFORM_CHECK_LINES["low_sharpe_min"]
    lf = PLATFORM_CHECK_LINES["low_fitness_min"]
    sharpe_line = float(ls["delay0"] if delay == 0 else ls["delay1"])
    fit_line = float(lf["delay0"] if delay == 0 else lf["delay1"])
    y2_line = float(PLATFORM_CHECK_LINES["low_2y_sharpe_min"])
    to_lo, to_hi = PLATFORM_CHECK_LINES["turnover_range"]
    if turnover_max is not None:
        to_hi = float(turnover_max)

    failed = []
    if sharpe is None or sharpe < sharpe_line:
        failed.append("S")
    if fitness is None or fitness < fit_line:
        failed.append("F")
    if two_year is None or two_year < y2_line:
        failed.append("2Y")
    if sub is None or sub < 1.0:
        failed.append("sub")
    if turnover is None or not (to_lo <= turnover <= to_hi):
        failed.append("TO")
    return failed, 5 - len(failed)


def _merge_platform_failures(failed, names):
    """把平台 failed_checks 并入五闸名单；认不出的名字进 extras（如 CONCENTRATED_WEIGHT）。"""
    extras = []
    for name in names or []:
        dim = PLAT_FAIL_TO_DIM.get(name)
        if dim:
            if dim not in failed:
                failed.append(dim)
        elif name not in extras:
            extras.append(name)
    return failed, extras


def _payload_failed_checks(raw):
    """从回测行 payload 里取平台自己的失败名单（三种存放形态都认）。"""
    if not raw:
        return []
    try:
        d = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return []
    if not isinstance(d, dict):
        return []
    names = d.get("failed_checks")
    if isinstance(names, list):
        return [str(x) for x in names if x]
    # 精简结构：{"is": {"checks": [...]}} / {"checks": {"fail": [...]}}
    checks = d.get("checks")
    if isinstance(checks, dict):
        out = []
        for bucket in ("fail", "failed", "FAIL"):
            for c in checks.get(bucket) or []:
                if isinstance(c, dict) and c.get("name"):
                    out.append(str(c["name"]))
        return out
    is_ = d.get("is")
    if isinstance(is_, dict):
        return [str(c.get("name")) for c in (is_.get("checks") or [])
                if isinstance(c, dict) and c.get("result") == "FAIL" and c.get("name")]
    return []


async def _cmd_atom_first(a):
    """零平台调用：从 backtest_results × expressions.atom_flag 出 ATOM 优先候选单。

    排序 = 过闸数降序 → Sharpe 降序；ATOM 区在前，非 ATOM 备选区在后，绝不混排。
    平台侧最终确认仍需 `get_alpha_details` 的 checks（出现 `LOW_2Y_SHARPE` 且无
    `IS_LADDER_SHARPE`）——本命令只作本地初筛，不替代那一步。
    """
    from wqb.config import PLATFORM_CHECK_LINES

    conn = db_connect()
    try:
        where = ["b.region = ?", "e.atom_flag IS NOT NULL", "b.sharpe IS NOT NULL",
                 "ABS(b.sharpe) >= ?"]
        params = [a.region, a.min_sharpe]
        if a.wave:
            where.append("b.wave = ?")
            params.append(a.wave)
        if a.dataset:
            where.append("b.dataset IN (%s)" % ",".join("?" * len(a.dataset)))
            params.extend(a.dataset)
        if not a.include_submitted:
            where.append("(al.status IS NULL OR al.status NOT IN "
                         "('ACTIVE','SUBMITTED','DECOMMISSIONED'))")
        sql = """
            SELECT b.alpha_id, COALESCE(b.dataset,''), COALESCE(b.wave,''),
                   e.atom_flag, e.atom_n_datasets,
                   b.sharpe, b.fitness, b.two_year_sharpe,
                   b.sub_universe_sharpe, b.turnover,
                   COALESCE(al.status,''), al.prod_correlation, b.payload_json
            FROM backtest_results b
            JOIN expressions e ON e.id = b.expression_id
            LEFT JOIN alphas al ON al.alpha_id = b.alpha_id
            WHERE %s
            ORDER BY b.sharpe DESC
        """ % " AND ".join(where)
        rows = conn.execute(sql, params).fetchall()
    finally:
        conn.close()

    best = {}
    for (aid, ds, wave, flag, nds, s, f, y2, sub, tov, st, pc, payload) in rows:
        failed, npass = _atom_gate_flags(s, f, y2, sub, tov, a.delay,
                                         turnover_max=a.turnover_max)
        # 平台自己的失败名单优先：补进五闸维度，认不出的（如 CONCENTRATED_WEIGHT）单列 extras
        failed, extras = _merge_platform_failures(failed, _payload_failed_checks(payload))
        npass = 5 - len(failed)
        warns = []
        if pc is not None and pc >= 0.7:
            warns.append("prod %.2f" % pc)
        item = {"alpha_id": aid, "dataset": ds, "wave": wave, "atom_flag": flag,
                "n_datasets": nds, "sharpe": s, "fitness": f, "two_year": y2,
                "sub_universe": sub, "turnover": tov, "status": st,
                "prod_correlation": pc,
                "failed": failed, "platform_extra": extras,
                "warns": warns, "n_pass": npass}
        prev = best.get(aid)
        if prev is None or (npass, s or -9) > (prev["n_pass"], prev["sharpe"] or -9):
            best[aid] = item

    def _order(it):
        # 平台额外 FAIL（如 CONCENTRATED_WEIGHT）直接压到同组末尾
        return (-it["n_pass"], 1 if it["platform_extra"] else 0, -(it["sharpe"] or -9))

    atom = sorted((v for v in best.values() if v["atom_flag"] == "atom"), key=_order)
    other = sorted((v for v in best.values() if v["atom_flag"] != "atom"), key=_order)
    atom, other = atom[:a.top], other[:a.top]

    print("=== ATOM 优先候选单｜%s｜delay=%d｜ATOM %d 颗 / 非 ATOM %d 颗（各取前 %d）==="
          % (a.region, a.delay, len(atom), len(other), a.top))
    print(ATOM_RULE_TEXT)
    to_hi = a.turnover_max if a.turnover_max is not None else \
        PLATFORM_CHECK_LINES["turnover_range"][1]
    print("闸线取自 config：S≥%.2f、F≥%.2f、2Y≥%.2f、sub≥1.0、TO∈[%.2f,%.2f]"
          "（平台 failed_checks 一并并入）"
          % (PLATFORM_CHECK_LINES["low_sharpe_min"]["delay0" if a.delay == 0 else "delay1"],
             PLATFORM_CHECK_LINES["low_fitness_min"]["delay0" if a.delay == 0 else "delay1"],
             PLATFORM_CHECK_LINES["low_2y_sharpe_min"],
             PLATFORM_CHECK_LINES["turnover_range"][0], to_hi))

    def _print_block(title, items):
        print("\n[%s]" % title)
        if not items:
            print("  （无）")
            return
        print("  #  alpha        dataset        wave   S     F     2Y    sub    TO     未过 / 状态")
        for i, it in enumerate(items, 1):
            flags = ",".join(it["failed"]) or "全过"
            if it["platform_extra"]:
                flags += " ⛔ " + ",".join(it["platform_extra"])
            if it["warns"]:
                flags += " ⚠ " + ", ".join(it["warns"])
            print("  %-2d %-12s %-14s %-5s %5.2f %5.2f %5.2f %6.2f %6.3f  %s%s"
                  % (i, it["alpha_id"], it["dataset"] or "-", it["wave"] or "-",
                     it["sharpe"] or 0, it["fitness"] or 0, it["two_year"] or 0,
                     it["sub_universe"] or 0, it["turnover"] or 0,
                     flags,
                     ("  [%s]" % it["status"]) if it["status"] else ""))

    _print_block("ATOM（单数据集，优先交付）", atom)
    _print_block("非 ATOM 备选（跨数据集/含 pv1 引用，不得与上区混排）", other)

    best_by_ds = {}
    for it in atom:
        ds = it["dataset"] or "-"
        cur = best_by_ds.get(ds)
        if cur is None or it["n_pass"] > cur["n_pass"] or (
                it["n_pass"] == cur["n_pass"] and (it["sharpe"] or 0) > (cur["sharpe"] or 0)):
            best_by_ds[ds] = it
    if best_by_ds:
        print("\n[ds] 各数据集最佳 ATOM：")
        for ds, it in sorted(best_by_ds.items(), key=lambda kv: -kv[1]["n_pass"]):
            print("  %-14s %s  S%.2f/F%.2f/2Y%.2f 过%d/5"
                  % (ds, it["alpha_id"], it["sharpe"] or 0, it["fitness"] or 0,
                     it["two_year"] or 0, it["n_pass"]))

    if a.json_out:
        payload = {"region": a.region, "delay": a.delay, "rule": ATOM_RULE_TEXT,
                   "atom": atom, "non_atom": other}
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        with open(a.json_out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("\n[out] %s" % a.json_out)
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_parser():
    """构建 CLI（供 main 与单测读取参数缺省）。

    ⚠ prod-probe 的 `--prod-max` 缺省（0.75）必须与 `wave_gate_pkg.gates_pf.PROBE_SEAL_THRESHOLD`
    一致——守护测试 `tests/unit/08_forum_recon/test_campaign_intel_prod_probe.py` 比对两者。
    """
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p0 = sub.add_parser("s0-select", help="S0 选集增强（点塔×产出率×判死三方交叉）")
    p0.add_argument("--region", required=True)
    p0.add_argument("--delay", type=int, default=1)
    p0.add_argument("--universe", default="TOP3000")
    p0.add_argument("--top-n", type=int, default=15)
    p0.add_argument("--sharpe-min", type=float, default=1.58)
    p0.add_argument("--fitness-min", type=float, default=1.0)
    p0.add_argument("--min-samples", type=int, default=8,
                    help="产出率判死的最小回测样本量（默认 8）")
    p0.add_argument("--target", type=int, default=None,
                    help="P1 目标独立座位数（提交目标）；Σest_seats<target 即报结构性不可达")
    p0.add_argument("--min-fields", type=int, default=5,
                    help="字段数低于此值的集只能作条件腿/事件探针，主攻榜次沉（默认 5）")
    p0.add_argument("--xr-weak-sharpe", type=float, default=1.0,
                    help="跨区负先验：其它区该集 max|S| 低于此值且样本≥--xr-min-bt 视为弱（默认 1.0）")
    p0.add_argument("--xr-min-bt", type=int, default=16,
                    help="跨区负先验的最小样本量（默认 16）")
    p0.add_argument("--include-lit", action="store_true",
                    help="保留已点亮塔的数据集（默认剔除：用户规则 2026-09-19，已点亮塔只作组腿不开战役）")
    p0.add_argument("--include-region-dead", action="store_true",
                    help="保留区域判死清单（tracking/<REGION>/reference/<r>_dead_datasets.md）命中的数据集；"
                         "默认剔除。只用于复核清单，不用于长期绕过")
    p0.add_argument("--xr-penalize", action="store_true",
                    help="把「跨区弱」重新计入降权（旧行为复现；默认不降权——P1 实测该先验无预测力）")
    p0.add_argument("--json", dest="json_out")

    px = sub.add_parser("xr-probe", help="跨区探针：同一组表达式按各区 settings 发批→收批入库→GLOBAL/xr_probe_<tag> 台账")
    px.add_argument("--exprs-file", required=True)
    px.add_argument("--regions", required=True, help="逗号分隔，如 USA,GLB,HKG")
    px.add_argument("--dataset", default=None)
    px.add_argument("--universe", default=None, help="统一覆盖 universe（缺省各区 settings.json）")
    px.add_argument("--set", action="append", default=[], help="覆盖仿真键，如 --set decay=10 --set neutralization=SECTOR")
    px.add_argument("--tag", default=None, help="波标签后缀（缺省当天日期）→ wave=probe_<tag>")
    px.add_argument("--timeout-sec", type=int, default=1500)
    px.add_argument("--poll-sec", type=int, default=30)
    px.add_argument("--write-ledger", action="store_true")
    px.add_argument("--no-field-check", action="store_true", help="跳过按区字段存在性校验（缺省校验，避免连坐）")
    px.add_argument("--resume", action="append", default=[], help="REGION=multisim_id：跳过发批直接收批（网络中断续跑）")
    px.add_argument("--json", dest="json_out")

    pp = sub.add_parser("pyramid", help="点塔进度快照（S6 回写用）")
    pp.add_argument("--region", required=True)
    pp.add_argument("--delay", type=int, default=1)
    pp.add_argument("--json", dest="json_out")

    p4 = sub.add_parser("s4-prescreen", help="S4 预筛压缩（batch 分层 READY/REVIEW/REJECT）")
    p4.add_argument("--alpha-ids", nargs="*", default=[])
    p4.add_argument("--ids-file", help="每行一个 alpha_id 的文件")
    p4.add_argument("--json", dest="json_out")

    pf = sub.add_parser("prod-first", help="收批后族级 prod 探针（≥0.7 的族 STOP 不再扩变体）")
    pf.add_argument("--region", required=True)
    pf.add_argument("--wave", required=True)
    pf.add_argument("--top-k", type=int, default=3, help="最多探几个信号族（每族最强 1 条，默认 3）")
    pf.add_argument("--min-sharpe", type=float, default=1.0, help="进入探针池的 |sharpe| 下限（默认 1.0）")
    pf.add_argument("--sharpe-min", type=float, default=1.58)
    pf.add_argument("--fitness-min", type=float, default=1.0)
    pf.add_argument("--prod-max", type=float, default=0.7)
    pf.add_argument("--max-tries", type=int, default=8, help="pending/busy 重试次数（默认 8）")
    pf.add_argument("--poll-sec", type=int, default=45, help="pending/busy 重试间隔秒（默认 45）")
    pf.add_argument("--refresh", action="store_true", help="强制回源平台（跳过 7 天缓存）")
    pf.add_argument("--write-ledger", action="store_true", help="写 ledger prod_first_<wave>")
    pf.add_argument("--probe-timeout", type=int, default=600,
                    help="单条 check_correlation 硬超时秒（默认 600；平台 PC 排队超时即跳过）")
    pf.add_argument("--no-lock", action="store_true", help="忽略进程锁强行并跑（不推荐：平台 prod 单并发）")
    pf.add_argument("--json", dest="json_out", help="结果 JSON 输出路径（需要文件路径）")

    # 2026-10-24 P0-1：开波前族级 prod 探针。--prod-max 缺省 0.75 必须与
    # wave_gate_pkg.gates_pf.PROBE_SEAL_THRESHOLD 一致（守护测试比对两者，见 build_parser docstring）。
    ppb = sub.add_parser("prod-probe", help="开波前族级 prod 探针（P0-1）：每族 1 条，≥--prod-max 封族（exit 2）")
    ppb.add_argument("--region", required=True)
    ppb.add_argument("--dataset", required=True, help="待开波数据集（历史回测行跨全部波次取材）")
    ppb.add_argument("--top-k", type=int, default=3, help="最多探几个信号族（每族最强 1 条，默认 3）")
    ppb.add_argument("--min-sharpe", type=float, default=1.0, help="进入探针池的 |sharpe| 下限（默认 1.0）")
    ppb.add_argument("--sharpe-min", type=float, default=1.58)
    ppb.add_argument("--fitness-min", type=float, default=1.0)
    ppb.add_argument("--prod-max", type=float, default=0.75,
                     help="封族线（默认 0.75，与闸 PF 的 PROBE_SEAL_THRESHOLD 一致；≥ 即封族）")
    ppb.add_argument("--max-tries", type=int, default=8, help="pending/busy 重试次数（默认 8）")
    ppb.add_argument("--poll-sec", type=int, default=45, help="pending/busy 重试间隔秒（默认 45）")
    ppb.add_argument("--refresh", action="store_true", help="强制回源平台（跳过 48h 已决缓存）")
    ppb.add_argument("--probe-timeout", type=int, default=600,
                     help="单条 check_correlation 硬超时秒（默认 600；平台 PC 排队超时即跳过）")
    ppb.add_argument("--no-lock", action="store_true", help="忽略进程锁强行并跑（不推荐：平台 prod 单并发）")
    ppb.add_argument("--dry-run", action="store_true", help="只列拟探探针，不联网、不写库")
    ppb.add_argument("--json", dest="json_out", help="结果 JSON 输出路径（需要文件路径）")

    pb = sub.add_parser("backlog-drop", help="积压波清理：超 N 天未动且无回测的 pending/gated 波标 dropped（默认 dry-run）")
    pb.add_argument("--region", default=None, help="逗号分隔区域过滤（缺省全部）")
    pb.add_argument("--older-than-days", type=int, default=7)
    pb.add_argument("--pattern", default=None, help="只处理波号含此子串的波（如 s2_）")
    pb.add_argument("--drop-gate-fail-only", action="store_true",
                    help="只清最新 gate_results.all_pass!=1 的波（含 all_pass=0 判死波与 all_pass=NULL 空壳波）；保护 all_pass=1 的活波，可配合 --include-gated 使用")
    pb.add_argument("--drop-zero-expr", action="store_true",
                    help="连 live_expr=0 的零活表达式死波一起标 dropped（清 stale 统计噪声；无候选可回测）")
    pb.add_argument("--include-gated", action="store_true", help="连有 gate_results 但未回测的波一起清")
    pb.add_argument("--include-backtested", action="store_true", help="连已有回测行的波一起清（不推荐）")
    pb.add_argument("--show", type=int, default=25)
    pb.add_argument("--close-backtested", action="store_true",
                    help="已有回测行却仍 pending/gated 的波标 closed（残留未回测表达式标 dropped）")
    pb.add_argument("--apply", action="store_true", help="真正写库（缺省 dry-run）")

    pm = sub.add_parser("mark-saturated",
                        help="S6→S0 反馈：把被 prod 墙卡死的数据集记入台账 saturated_datasets（默认 dry-run；--write-ledger 落库）")
    pm.add_argument("--region", required=True)
    pm.add_argument("--dataset", action="append", default=[], help="数据集 id，可重复")
    pm.add_argument("--reason", default=None, help="饱和原因（写入 S0 的 tier_note；--remove 时可省）")
    pm.add_argument("--wave", default=None, help="证据来源波号（审计用）")
    pm.add_argument("--prod-corr", type=float, default=None, help="触发饱和的实测 prod 相关性（审计用）")
    pm.add_argument("--remove", action="store_true", help="撤销登记（饱和已解除时）")
    pm.add_argument("--write-ledger", action="store_true", help="写 ledger saturated_datasets（缺省只预览）")

    pg = sub.add_parser("ghost-audit", help="幽灵算子硬闸（S2 产物入库后）")
    pg.add_argument("--region", required=True)
    pg.add_argument("--delay", type=int, default=1)
    pg.add_argument("--universe", default="TOP3000")
    pg.add_argument("--exprs", nargs="*", default=[])
    pg.add_argument("--exprs-file", help="每行一条表达式的文件")
    pg.add_argument("--json", dest="json_out")

    # 2026-10-26 用户指令：「因子挖出来后优先给 ATOM，其他只作备选」。
    # 零平台调用，只读本地库的 atom_flag（判据源 wqb.expression.atom）。
    pa = sub.add_parser("atom-first",
                        help="ATOM 优先候选单：单数据集在前、跨数据集备选在后（零平台调用）")
    pa.add_argument("--region", required=True)
    pa.add_argument("--delay", type=int, default=1, choices=[0, 1])
    pa.add_argument("--wave", default=None, help="只看某一波（缺省跨全部波次）")
    pa.add_argument("--dataset", action="append", default=[], help="数据集 id，可重复")
    pa.add_argument("--min-sharpe", type=float, default=0.8,
                    help="入库候选的 |sharpe| 下限（默认 0.8，近闸池放宽用）")
    pa.add_argument("--top", type=int, default=20, help="每个区最多展示几颗（默认 20）")
    pa.add_argument("--turnover-max", type=float, default=None,
                    help="覆盖换手上限（缺省取 config 的 0.70 宽线；IND/D1 平台 HIGH_TURNOVER "
                         "实际线是 0.40，建议显式传 0.4）")
    pa.add_argument("--include-submitted", action="store_true",
                    help="把已 ACTIVE/SUBMITTED/DECOMMISSIONED 的 alpha 也算进来（缺省排除）")
    pa.add_argument("--json", dest="json_out", help="结果 JSON 输出路径")
    return ap


def main():
    ap = build_parser()
    a = ap.parse_args()
    _bootstrap()

    coro = {"s0-select": _cmd_s0_select, "pyramid": _cmd_pyramid,
            "s4-prescreen": _cmd_s4_prescreen, "ghost-audit": _cmd_ghost_audit,
            "prod-first": _cmd_prod_first, "prod-probe": _cmd_prod_probe,
            "xr-probe": _cmd_xr_probe,
            "backlog-drop": _cmd_backlog_drop,
            "mark-saturated": _cmd_mark_saturated,
            "atom-first": _cmd_atom_first}[a.cmd](a)
    sys.exit(asyncio.run(coro))


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()
