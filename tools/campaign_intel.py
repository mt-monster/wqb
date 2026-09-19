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

用法:
  python tools/campaign_intel.py s0-select --region EUR --delay 1 --universe TOP2500
  python tools/campaign_intel.py pyramid --region EUR --delay 1
  python tools/campaign_intel.py s4-prescreen --alpha-ids id1 id2 id3
  python tools/campaign_intel.py ghost-audit --region EUR --exprs-file candidates.txt
  python tools/campaign_intel.py prod-first --region IND --wave 172 --top-k 3 --write-ledger

退出码: 0=成功，1=失败/有 BLOCK 项。
运行环境: 使用 MCP venv（$WQ_PY 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import sys
import datetime
import time

# 2026-09-17 P0-4：ledger 契约归一的规范实现在 src/wqb（单一事实源）
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_DIR = os.path.join(_REPO_ROOT, "src")
if os.path.isdir(_SRC_DIR) and _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap():
    py = _mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)
    mcp = os.environ.get("WQ_MCP_DIR", r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp")
    if mcp not in sys.path:
        sys.path.insert(0, mcp)
    # wqb 规范核心包在 src/wqb（ghost-audit 依赖 wqb.expression）
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(repo, "src")
    for p in (repo, src):
        if p not in sys.path:
            sys.path.insert(0, p)



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
    if not base.get("universe"):  # 无战役目录的区域：平台档位实测缺省（2026-09-19 get_platform_setting_options）
        base["universe"] = {"USA": "TOP3000", "GLB": "TOP3000", "EUR": "TOPCS1600", "ASI": "MINVOL1M",
                            "CHN": "TOP2000U", "KOR": "TOP600", "HKG": "TOP800", "JPN": "TOP1600",
                            "IND": "TOP500", "DEU": "TOP500", "GBR": "TOP700", "TWN": "TOP500",
                            "MEA": "TOP400", "AMR": "TOP600"}.get(region, "TOP3000")
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

    # ② 本地台账：历史产出率（mining_yield）+ 判死清单（dead_datasets）
    #    + 白名单/自动排名/座位模型（P1 可达性 & P4 覆盖审计）—— 走本地 sqlite
    yield_map = {}
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
        conn = sqlite3.connect(db)
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
        })

    # 排序：判死（ledger 或产出率证伪）沉底；跨区弱 / 字段<min_fields 次沉；其余按 total_score 降序
    # （2026-09-19：此前只按未点亮塔分排序，把 earnings3/insiders1/macro63/shortinterest5 这类
    #   结构性弱集推到前排，7 集 197 条回测 0 候选）
    def _rank(x):
        penalized = x["ledger_dead"] or x["proven_dead_by_yield"]
        soft = x["xr_penalized"] or x["conditioning_only"]
        return (penalized, soft, -(x["total_score"] or 0))
    out.sort(key=_rank)

    # 2026-09-19 用户硬规则：已点亮塔（当季 ACTIVE >= 3）的数据集不开战役，只作组腿 —— 默认剔除
    lit_excluded = []
    if not getattr(a, "include_lit", False):
        lit_excluded = [x for x in out if x.get("category_lit")]
        out = [x for x in out if not x.get("category_lit")]
    alive = [x for x in out if not (x["ledger_dead"] or x["proven_dead_by_yield"])]
    dead = [x for x in out if x["ledger_dead"] or x["proven_dead_by_yield"]]

    print(f"=== S0 选集增强 {a.region}/D{a.delay}/{a.universe} ===")
    print(f"点塔状态: {pyramid_status.get('lit_categories')}/{pyramid_status.get('total_categories')} "
          f"已点亮；未点亮塔: {', '.join(pyramid_status.get('unlit_category_ids') or [])}")
    print(f"候选: 平台推荐 {len(recommendations)} → 剔除已点亮塔 {len(lit_excluded)}（用户规则，--include-lit 可保留）"
          f" → 剔除判死 {len(dead)} → 存活 {len(alive)}")
    print(f"\n{'rank':>4} {'score':>7} {'yield':>7} {'bt':>4} {'maxS':>5} {'fld':>4} {'cat':13s} {'lit':>3}  dataset  [先验]")
    for i, x in enumerate(alive[:a.top_n], 1):
        yr_s = f"{x['hist_yield_rate']:.3f}" if x["hist_yield_rate"] is not None else "  -  "
        ms = f"{x['hist_max_sharpe']:.2f}" if x.get("hist_max_sharpe") is not None else "  - "
        fc_s = str(x["field_count"]) if x.get("field_count") is not None else "-"
        tags = []
        if x["conditioning_only"]:
            tags.append(f"fields<{a.min_fields}:仅条件腿")
        if x["xr_weak"]:
            tags.append("跨区弱:" + ",".join(x["xr_weak"][:3]))
        if x["xr_strong"]:
            tags.append("跨区RA-clean:" + ",".join(x["xr_strong"][:3]))
        print(f"{i:>4} {x['total_score']:>7.2f} {yr_s:>7} {x['hist_backtested']:>4} {ms:>5} {fc_s:>4} "
              f"{str(x['category']):13s} {'Y' if x['category_lit'] else 'N':>3}  "
              f"{x['dataset_id']} ({x['dataset_name']})" + (f"  [{'; '.join(tags)}]" if tags else ""))
    if dead:
        print(f"\n[判死沉底 {len(dead)} 个]")
        for x in dead[:10]:
            reason = []
            if x["ledger_dead"]:
                reason.append("ledger_dead")
            if x["proven_dead_by_yield"]:
                reason.append(f"yield=0@{x['hist_backtested']}bt")
            print(f"  {x['dataset_id']:28s} cat={x['category']} ({'+'.join(reason)})")

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
            "pyramid_status": pyramid_status,
            "candidates": out, "alive_count": len(alive), "dead_count": len(dead),
            "seat_reachability": {  # P1
                "target": a.target, "total_est_seats": total_seats,
                "top_n_alive": len(top_alive), "seat_model_source": seat_src,
                "reachable": (total_seats >= a.target) if a.target else None,
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


async def _cmd_prod_first(a):
    import sqlite3
    import time
    from brain_api import BrainApiClient  # noqa: F402

    db = os.path.join(_REPO_ROOT, "data", "wqb.db")
    conn = sqlite3.connect(db)
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

    n_stop = sum(1 for x in results if x["verdict"].startswith("STOP"))
    n_expand = sum(1 for x in results if x["verdict"] == "EXPAND")
    summary = {"region": a.region, "wave": str(a.wave), "probed": len(results),
               "stop": n_stop, "expand": n_expand,
               "unknown": len(results) - n_stop - n_expand, "prod_max": a.prod_max,
               "results": results, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
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
    conn = sqlite3.connect(db, timeout=30)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    regions = [r.strip().upper() for r in (a.region or "").split(",") if r.strip()]
    cur.execute(
        """
        SELECT w.id AS wid, w.wave_number AS wave, r.name AS region, w.status AS wstatus,
               COUNT(e.id) AS n_expr, MAX(COALESCE(e.updated_at, e.created_at)) AS last_touch,
               (SELECT COUNT(*) FROM backtest_results b WHERE b.region=r.name AND b.wave=w.wave_number) AS n_bt,
               (SELECT COUNT(*) FROM gate_results g WHERE g.region=r.name AND g.wave=w.wave_number) AS n_gate
        FROM waves w JOIN regions r ON r.id=w.region_id
        LEFT JOIN expressions e ON e.wave_id=w.id AND e.status NOT IN ('superseded','dropped')
        WHERE w.status IN ('pending','gated')
        GROUP BY w.id HAVING n_expr > 0
        ORDER BY n_expr DESC
        """)
    rows = [dict(r) for r in cur.fetchall()]
    import datetime as _dt
    cutoff = (_dt.datetime.now() - _dt.timedelta(days=a.older_than_days)).strftime("%Y-%m-%dT%H:%M:%S")
    todo = []
    for r in rows:
        if regions and r["region"] not in regions:
            continue
        if r["n_bt"] > 0 and not a.include_backtested:
            continue
        if r["n_gate"] > 0 and not a.include_gated:
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
                   SUM(CASE WHEN e.alpha_id IS NULL OR e.alpha_id='' THEN 1 ELSE 0 END) AS n_unrun,
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
            if r["n_unrun"] == 0 or (lt and lt <= cutoff):
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
# main
# ---------------------------------------------------------------------------

def main():
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

    pb = sub.add_parser("backlog-drop", help="积压波清理：超 N 天未动且无回测的 pending/gated 波标 dropped（默认 dry-run）")
    pb.add_argument("--region", default=None, help="逗号分隔区域过滤（缺省全部）")
    pb.add_argument("--older-than-days", type=int, default=7)
    pb.add_argument("--pattern", default=None, help="只处理波号含此子串的波（如 s2_）")
    pb.add_argument("--include-gated", action="store_true", help="连有 gate_results 但未回测的波一起清")
    pb.add_argument("--include-backtested", action="store_true", help="连已有回测行的波一起清（不推荐）")
    pb.add_argument("--show", type=int, default=25)
    pb.add_argument("--close-backtested", action="store_true",
                    help="已有回测行却仍 pending/gated 的波标 closed（残留未回测表达式标 dropped）")
    pb.add_argument("--apply", action="store_true", help="真正写库（缺省 dry-run）")

    pg = sub.add_parser("ghost-audit", help="幽灵算子硬闸（S2 产物入库后）")
    pg.add_argument("--region", required=True)
    pg.add_argument("--delay", type=int, default=1)
    pg.add_argument("--universe", default="TOP3000")
    pg.add_argument("--exprs", nargs="*", default=[])
    pg.add_argument("--exprs-file", help="每行一条表达式的文件")
    pg.add_argument("--json", dest="json_out")

    a = ap.parse_args()
    _bootstrap()

    coro = {"s0-select": _cmd_s0_select, "pyramid": _cmd_pyramid,
            "s4-prescreen": _cmd_s4_prescreen, "ghost-audit": _cmd_ghost_audit,
            "prod-first": _cmd_prod_first, "xr-probe": _cmd_xr_probe,
            "backlog-drop": _cmd_backlog_drop}[a.cmd](a)
    sys.exit(asyncio.run(coro))


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()
