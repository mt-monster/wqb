# -*- coding: utf-8 -*-
"""pipeline.py - 战役端到端编排器：gate -> submit -> poll -> review -> ledger。

带 checkpoint/resume（断点续跑纪律）。填槽多轮即收即补（2026-08-25 5→7；2026-10-06 定案 7→2，槽位数唯一来源 = wqb.config.CONCURRENCY['slots']）：
- 单轮模式（默认）：并行提交 N 批（N=min(2, 批数)），统一轮询，全提全收。
- 多轮模式（--max-rounds>1）：每轮并行提交 n_slots 批，轮询回收后空槽补新批，
  保持槽位常满直至全部批次处理完毕或达到最大轮次。
轮询退避+挂起熔断（_lib/poller）；提交前 ET 日历日配额闸（REGULAR 4/日 + SUPER 1/日，00:00 ET 重置）。

用法:
  python pipeline.py --campaign-dir <DIR> quota [--dry-run]
      ET 日历日提交配额（REGULAR 4/日 + SUPER 1/日；--dry-run 打印计算过程）
  python pipeline.py --campaign-dir <DIR> run --file candidates/x.json --dataset model219 --wave 01A
      默认只跑 gate 并打印提交计划（不烧配额）
  python pipeline.py --campaign-dir <DIR> run ... --submit [--max-batches 2] [--max-rounds 3] [--force]
      过闸后按批提交（填槽模式）+ 轮询到 terminal（挂起熔断）
  python pipeline.py --campaign-dir <DIR> run ... --submit --review --write-ledger
      全链路：评审 + 回写台账
  恢复：重跑同一 --wave 自动从 checkpoint 续跑；--fresh 强制全新。
  --dry-run：不提交、checkpoint 写到 --checkpoint-dir（默认战役 results/；测试可指临时目录）。
  设置层先验（2026-09-15）：装载 settings 后按 region_kb.gate_priors 实测过闸率改写 decay/neutralization
  （--set / --neutralization / 组合 cells.json 钉住的维度不动；--no-settings-prior 关闭）；--review 收批后自动刷新 region_kb。
  退出码：0 正常；2 中止/前置不满足（此前恒 0，detached 启动器把中止当成功）。
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, add_campaign_arg, atomic_write, load_credentials, load_json, read_expr_items
from _lib.api import Api, api_call
from _lib.poller import TERMINAL, poll_config, poll_until_terminal
from _lib.ledger import make_ledger_store, today
from _lib import rules as rules_mod
from _lib import region_kb as region_kb_mod
from _lib import slots as slots_mod
import gate as gate_mod
import metrics_cache
import review_wave as review_mod


# P1-1 (2026-08-31): 中性化×数据集缓存表——复用工作区 tools/neut_cache.py 的
# query_top（WebDataScope 数据包回填的 SQLite neut_cache 表）。
# 用户未显式 --neutralization 时按缓存推荐最优中性化；不可达则降级跳过。
def _load_neut_cache():
    """尝试导入工作区 tools/neut_cache.py 的 query_top，不可达返回 None。"""
    cands = []
    env_root = os.environ.get("WQB_WORKSPACE_ROOT")
    if env_root:
        cands.append(env_root)
    here = os.path.dirname(os.path.abspath(__file__))
    cands.append(os.path.normpath(os.path.join(here, "..", "..", "..", "..", "..")))
    for root in cands:
        tools_dir = os.path.join(root, "tools")
        if os.path.isfile(os.path.join(tools_dir, "neut_cache.py")):
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            try:
                from neut_cache import query_top
                return query_top
            except Exception:
                return None
    return None

_neut_query_top = _load_neut_cache()


def _check_s2_compliance(ctx, wave):
    """S2 合规校验：检查特征工程文档是否存在且记录完整。
    
    校验逻辑：
    1. 检查 ledger_kv 中是否存在 feature_engineering_doc 记录
    2. 检查文档路径是否有效（文件存在）
    3. 检查文档是否包含必要章节（字段分类/特征工程建议）
    
    返回: (ok: bool, msg: str)
    """
    try:
        st = _get_store(ctx)
        try:
            # 从 ledger_kv 读取 S2 合规记录
            key = f"s2_compliance_w{wave}"
            record = st.get_ledger(ctx.region, key)
            if not record:
                return False, f"未找到 wave={wave} 的 S2 合规记录（ledger_kv key={key}）"
            
            doc_path = record.get("feature_engineering_doc")
            if not doc_path:
                return False, "S2 合规记录缺失 feature_engineering_doc 字段"
            
            # 检查文档是否存在
            if not os.path.exists(doc_path):
                return False, f"特征工程文档不存在: {doc_path}"
            
            # 检查文档内容是否包含必要章节
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            required_sections = ["字段", "特征", "建议"]
            missing = [s for s in required_sections if s not in content]
            if missing:
                return False, f"特征工程文档缺少必要章节: {missing}"
            
            # 检查候选池来源标记
            if record.get("candidate_pool_source") != "skill":
                return False, f"候选池来源标记异常: {record.get('candidate_pool_source')}（应为 'skill'）"
            
            return True, f"文档={os.path.basename(doc_path)}, 来源=skill, 章节完整"
            
        finally:
            st.close()
    except Exception as e:
        return False, f"S2 合规校验异常: {type(e).__name__}: {e}"


def _find_workspace_root():
    """探测工作区根（含 src/wqb）：优先 $WQB_ROOT，其次已知安装位置。"""
    env = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT")
    if env and os.path.isdir(os.path.join(env, "src", "wqb")):
        return env
    # 从本文件向上找含 src/wqb 的仓库根（从仓库内运行时无需环境变量；跨平台）
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(here, "src", "wqb")):
            return here
        here = os.path.dirname(here)
    return None


def _get_store(ctx=None):
    from _lib.wqb_store import get_store
    return get_store(ctx)


def _wave_aliases(ctx, a, st):
    """wave 别名候选（2026-09-01）：GEM 标签格式与战役编号互转。

    生成顺序（调用方按序尝试，命中即停）：
    1. GEM 标签 s2_<ds>_d<delay> / <ds>_<region>_d<delay> → 库里实际存在的同 wave 数值
    2. 反向：数值 wave → GEM 标签
    实现上直接查库：列出该 region 全部 distinct wave，与目标做启发式匹配。
    """
    try:
        cur = st.connection.cursor()
        rows = cur.execute(
            "SELECT DISTINCT wave FROM expressions WHERE region=? AND wave IS NOT NULL",
            (ctx.region,),
        ).fetchall()
    except Exception:
        return []
    have = {str(r[0]) for r in rows}
    target = str(a.wave)
    import re as _re
    out = []
    # 1) 目标是 GEM 标签（含字母/下划线）→ 库里可能存的是纯数字编号（同 dataset 最新）
    if _re.search(r"[a-zA-Z]", target):
        ds = getattr(a, "dataset", None)
        if ds:
            out += sorted(w for w in have if w.isdigit())
        else:
            out += sorted(w for w in have if w.isdigit())
    # 2) 目标是纯数字 → 库里可能存的是 GEM 标签（含该 dataset 的）
    else:
        ds = getattr(a, "dataset", None)
        if ds:
            out += sorted(w for w in have if ds in w)
        out += sorted(w for w in have if _re.search(r"[a-zA-Z]", w))
    return [w for w in out if w != target]


# ---------------- quota：ET 日历日提交配额（REGULAR 4/日 + SUPER 1/日 + PPA 1/日，00:00 ET 重置） ----------------

# 2026-09-01 定案：提交配额从"48h 滚动窗口"改为"ET 日历日"模型（旧"48h 滚动"已证伪：08-12 一次 48h 内提交 6 颗全成功）。
#   - 剩余额度从 submit 响应 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 的 value/limit 读（value 从 0 起计数）。
#   - 硬闸 FAIL 的提交不消耗配额（status 保持 UNSUBMITTED）。
# 2026-09-29 整改（skills 审查 T0-14）：
#   1) 只按 OS 池 `dateSubmitted` 的 ET 日聚合——与 tools/quota_status.py 同口径。此前优先读
#      `/users/self/activities/submissions`：该端点只有 {yesterday,current,previous,ytd} 快照、没有 today、
#      也没有 `results` 列表，解析出空列表 → 被当成"今日 0 提交"，配额永远显示满额（2026-09-21 事故同源）。
#   2) ET 日界用 wqb.timeutil（America/New_York，含夏令时）；此前写死 UTC-4，2026-11-01 起日界漂移 1 小时。

def _timeutil():
    """wqb.timeutil（ET 日界唯一实现）。toolkit 可能从安装位运行：先把工作区 src 放进 sys.path。"""
    try:
        import wqb.timeutil as T
        return T
    except ImportError:
        root = _find_workspace_root()
        if root:
            sys.path.insert(0, os.path.join(root, "src"))
        import wqb.timeutil as T
        return T


def _parse_submitted_ts(results):
    out = []
    for a in results or []:
        ds = a.get("dateSubmitted")
        if not ds:
            continue
        try:
            out.append(datetime.datetime.fromisoformat(ds.replace("Z", "+00:00")))
        except Exception:
            continue
    return out


def submission_quota(api, limit, window_h=None, now=None):
    """ET 日历日提交配额视图。limit=REGULAR 日上限（默认 4）；window_h 保留仅向后兼容，不再参与计算；
    now 仅供测试注入（tz-aware UTC）。"""
    T = _timeutil()
    now = now or datetime.datetime.now(datetime.timezone.utc)
    _, day_end = T.et_day_bounds_utc(now)
    j = json.load(api.get("/users/self/alphas?stage=OS&limit=100&order=-dateSubmitted"))
    submitted_ts = _parse_submitted_ts(j.get("results", []))
    et_day = T.et_today(now)
    used = sum(1 for t in submitted_ts if T.et_date(t) == et_day)
    remaining = max(0, limit - used)
    return {"used": used, "remaining": remaining, "next_reset_utc": day_end.isoformat(),
            "limit": limit, "et_day": et_day, "source": "os_alphas",
            "_note": "ET 日历日配额（REGULAR 4/日 + SUPER 1/日 + PPA 1/日；00:00 ET 重置，"
                     f"现为 {T.et_reset_hour_gmt8(now)}:00 GMT+8，夏/冬令时不同）；"
                     "数 OS 池今日提交总数，不区分类型；旧 48h 滚动与 activities 口径已废止。"
                     "硬闸 FAIL 提交不消耗配额。"}


def quota_cfg(ctx):
    # 2026-08-26 用户指令：不要配额检查，默认关闭（enabled=False 永不中止提交）。
    # limit=REGULAR 日上限 4；SUPER 的 1/日上限由提交层（submit_verdict/提交响应）单独把关，本闸只看 REGULAR。
    q = {"limit": 4, "enabled": False}
    q.update(ctx.thresh("submit_quota", {}))
    return q


# ---------------- checkpoint ----------------

def ckpt_path(ctx, wave, checkpoint_dir=None):
    """仅 --checkpoint-dir 测试路径仍写文件；默认走 ledger_kv ckpt_w<W>。"""
    if checkpoint_dir:
        return os.path.join(checkpoint_dir, f"pipeline_{wave}_checkpoint.json")
    return f"db:ledger_kv/{ctx.region}/ckpt_w{wave}"


def ckpt_load(ctx, wave, fresh=False, checkpoint_dir=None):
    if fresh:
        return {"wave": wave, "stages": {}, "batches": []}
    if checkpoint_dir:
        p = ckpt_path(ctx, wave, checkpoint_dir)
        if not os.path.exists(p):
            return {"wave": wave, "stages": {}, "batches": []}
        return load_json(p)
    try:
        st = _get_store(ctx)
        try:
            ck = st.get_checkpoint(ctx.region, str(wave))
        finally:
            st.close()
        if ck:
            return ck
    except Exception as e:
        print(f"[ckpt] DB 读取失败，新建: {e}")
    return {"wave": wave, "stages": {}, "batches": []}


def ckpt_save(ctx, ck, checkpoint_dir=None):
    if checkpoint_dir:
        atomic_write(ckpt_path(ctx, ck["wave"], checkpoint_dir), ck)
        return
    st = _get_store(ctx)
    try:
        # L3 写库互斥（2026-09-20）：checkpoint 写 ledger_kv，与其他写者排队（短锁）
        from _lib.dblock import write_lock as _wlock
        with _wlock(tag="dbwrite_ckpt", ttl_sec=120, wait_timeout=60):
            st.upsert_checkpoint(ctx.region, str(ck["wave"]), ck)
    finally:
        st.close()


# ---------------- 各阶段 ----------------

def stage_gate(ctx, ck, exprs, dataset, checkpoint_dir=None, datasets_extra=None):
    if ck["stages"].get("gate", {}).get("done"):
        print(f"[gate] 已完成（checkpoint），跳过。passed={len(ck['stages']['gate']['passed'])}")
        return ck["stages"]["gate"]["passed"]
    ds_all = [dataset] + [x.strip() for x in (datasets_extra or "").split(",") if x.strip()]
    wl = (gate_mod.merge_whitelists(ctx, ds_all) if len(ds_all) > 1
          else gate_mod.load_whitelist(ctx, dataset))
    from _lib.common import load_platform_constraints
    pc = load_platform_constraints()
    poison = list(pc.get("poison_patterns", []))
    cons_path = ctx.constraints_path()
    if os.path.exists(cons_path):
        poison += load_json(cons_path).get("poison_patterns", [])
    passed, failed = [], []
    for item in exprs:
        e = item_expr(item) or item
        r = gate_mod.check_one(e, wl, dataset, poison, pc)
        if r["pass"]:
            ov = item_settings(item)
            passed.append({"expr": e, **({"settings": ov} if ov else {})})
        else:
            failed.append({"expr": e, "issues": r["issues"]})
    ck["stages"]["gate"] = {"done": True, "total": len(exprs),
                            "passed": passed, "failed": failed,
                            "at": datetime.datetime.now().isoformat(timespec="seconds")}
    ckpt_save(ctx, ck, checkpoint_dir)
    print(f"[gate] total={len(exprs)} passed={len(passed)} failed={len(failed)}")
    for f in failed[:5]:
        print(f"  FAIL: {f['expr'][:70]} -> {f['issues'][0][:90]}")
    return passed


def stage_batch_gates(ctx, ck, passed, dataset, batch_type="explore",
                      skip_diversity=False, sanity_all=False, consume=False,
                      checkpoint_dir=None, datasets_extra=None):
    """批级闸（闸6 多样性契约 + 可选闸7/8 sanity）：与手动 CLI gate 对齐。

    整批粒度：对 passed 全量检查（与 CLI --file 整文件一批语义一致，
    勿按 batch_size 分批，否则契约消费计数翻倍提前耗尽 expires_after_batches）。
    consume=True 且全过时回写契约消费（幂等，digest 去重；dry-run 不消费）。
    返回 (ok, issues)。
    """
    prev = ck["stages"].get("batch_gates")
    if prev and prev.get("done"):
        print(f"[batch_gates] 已完成（checkpoint），跳过。ok={prev.get('ok')}")
        return prev.get("ok", False), prev.get("issues", [])
    issues = []
    exprs = [p["expr"] for p in passed]
    if not exprs:
        print("[batch_gates] 无表达式通过闸1-5，跳过批级闸")
    else:
        # 闸7/8 sanity（--sanity-all；对提交列表 passed 全量）
        if sanity_all:
            try:
                ds_all = [dataset] + [x.strip() for x in (datasets_extra or "").split(",") if x.strip()]
                wl = (gate_mod.merge_whitelists(ctx, ds_all) if len(ds_all) > 1
                      else gate_mod.load_whitelist(ctx, dataset))
                _, _dt, field_types, _ = wl
                issues.extend(gate_mod.check_sanity_longcount(ctx, dataset, exprs, field_types))
                issues.extend(gate_mod.check_sanity_event_type(ctx, dataset, exprs, field_types))
            except Exception as e:
                issues.append(f"[SANITY] 预检异常（不阻断提交，需人工核查）: {e}")
        # 闸6 批级多样性契约（整批粒度；契约缺失/过期自动豁免）
        dissues, consume_ref = gate_mod.check_batch_diversity(
            exprs, ctx, batch_type=batch_type, skip=skip_diversity, dataset=dataset)
        issues.extend(dissues)
        if consume and not issues and consume_ref is not None:
            gate_mod.consume_diversity(ctx, consume_ref)
    ok = not issues
    ck["stages"]["batch_gates"] = {"done": True, "ok": ok, "issues": issues,
                                    "at": datetime.datetime.now().isoformat(timespec="seconds")}
    ckpt_save(ctx, ck, checkpoint_dir)
    for it in issues:
        print(f"  BATCH-FAIL: {it}")
    print(f"[batch_gates] ok={ok} issues={len(issues)}（batch_type={batch_type}，"
          f"sanity_all={sanity_all}，consume={consume}）")
    return ok, issues


def item_expr(item):
    """表达式条目归一：纯字符串 或 {expr|expression|regular, settings?} dict -> 表达式串。
    兼容 neutralization_sweep.py 产物（{"type":"REGULAR","settings":...,"regular":expr}）。"""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return item.get("expr") or item.get("expression") or item.get("regular") or ""
    return ""


_SIM_SETTING_KEYS = ("decay", "neutralization", "truncation", "universe", "delay", "pasteurization",
                     "nanHandling", "unitHandling", "maxTrade", "region", "instrumentType", "language",
                     "visualization", "testPeriod", "startDate", "endDate")


def _sim_settings_only(settings):
    """从 expressions.settings_json 里只取平台仿真设置键（note/status_change/来源标签等一律剔除）。"""
    if not isinstance(settings, dict):
        return None
    ov = {k: v for k, v in settings.items() if k in _SIM_SETTING_KEYS and v is not None}
    return ov or None


def item_settings(item):
    """提取 per-item settings（场景3：N 表达式×各自设置）；无则返回 None。"""
    if isinstance(item, dict) and isinstance(item.get("settings"), dict):
        return item["settings"]
    return None


def submit_batch(api, settings, exprs):
    """提交单批：expr 可为纯字符串或带 per-item settings 的 dict（覆盖基础设置）。"""
    payloads = []
    for e in exprs:
        s = {k: v for k, v in settings.items() if not k.startswith("_")}
        ov = item_settings(e)
        if ov:
            s.update(ov)
        payloads.append({"type": "REGULAR", "settings": s, "regular": item_expr(e)})
    body = payloads[0] if len(payloads) == 1 else payloads
    r = api_call(api, "post", "/simulations", body)
    loc = r.headers.get("Location") or ""
    return loc.rstrip("/").split("/")[-1]


def _submit_single_batch(api, settings, batch, bi, n_batches):
    """提交单批并返回 (bi, msid, error, slot_token)。供 ThreadPool 并行调用。

    2026-09-19：提交前先拿账户级槽位 token（_lib/slots，跨进程仲裁，cap 缺省 7；
    WQB_GLOBAL_SLOTS=0 关闭），提交失败即释放；成功则由轮询侧 terminal 后释放。"""
    token = slots_mod.acquire(label=f"pending-b{bi}")
    try:
        msid = submit_batch(api, settings, batch)
        slots_mod.relabel(token, msid)
        return bi, msid, None, token
    except Exception as e:
        slots_mod.release(token)
        return bi, None, str(e)[:200], None


def _resolve_batch_items(ck, batch):
    """batch 条目解析回提交项：命中 item_overrides 的还原为带 per-item settings 的 dict。"""
    ov = ck.get("item_overrides") or {}
    return [{"expr": e, "settings": ov[e]} if e in ov else e for e in batch]


def _poll_single_batch(api, msid, pcfg, bi):
    """轮询单批至 terminal，返回 (bi, status, detail)。供 ThreadPool 并行调用。"""
    status, detail = poll_until_terminal(api, msid, pcfg)
    return bi, status, detail


def _harvest_batch_alphas(api, detail):
    """从 COMPLETE 的 multisim detail 提取全部 alpha id。"""
    alphas = []
    if detail.get("alpha"):
        alphas.append(detail["alpha"])
    for c in (detail.get("children") or []):
        try:
            sim = json.load(api_call(api, "get", "/simulations/" + c))
            if sim.get("alpha"):
                alphas.append(sim["alpha"])
        except Exception:
            pass
    return alphas


def _harvest_batch_errors(api, detail):
    """从 ERROR 的 multisim detail 提取子模拟错误。

    2026-09-19 补：同时带回子模拟的表达式（`regular`）与状态，供 `_isolate_error_batch`
    区分「真正报错的坏式」与「被连坐 CANCELLED 的无辜兄弟」。平台的错误正文在
    `message`（如 "Invalid data field close." / "At least one of buckets/range is required."），
    旧字段名 `error` 一并兼容。
    """
    errs = []
    for idx, c in enumerate(detail.get("children", [])):
        try:
            sim = json.load(api_call(api, "get", "/simulations/" + c))
            msg = sim.get("message") or sim.get("error")
            st = sim.get("status")
            if msg or st in ("ERROR", "CANCELLED"):
                errs.append({
                    "child": c,
                    "idx": idx,                      # 子模拟在 multisim children 里的序号 = 提交顺序
                    "status": st,
                    "error": str(msg or st)[:160],
                    "expr": item_expr(sim.get("regular") or sim.get("expression") or ""),
                })
        except Exception:
            pass
    return errs


#: 连坐隔离：被平台判为「坏式」的子模拟状态（CANCELLED 是无辜兄弟，不算坏式）
_CULPRIT_STATUSES = ("ERROR",)


def _isolate_error_batch(batch_exprs, errs):
    """把 ERROR 批拆成 (culprits, survivors)。

    2026-09-19（JPN w7/w8 实证：一条 `bucket()` 缺 range / 一个平台不认的字段，
    整批 8 条连坐 CANCELLED，10 批丢 8 批 64 条）。平台 multisim 语义：任一子模拟
    ERROR → 同批其余子模拟 CANCELLED。此前 SOP 只写成人工协议（"隔离不确定算子到
    独立小批次"），pipeline 自身不处理 → 每个坏式吃掉 7 条无辜表达式。

    规则：
      - culprit = 子模拟状态在 _CULPRIT_STATUSES 且能按表达式原文匹配回本批的条目；
      - survivors = 本批其余表达式（含 CANCELLED 与匹配失败者），保持原序；
      - 若一条 culprit 都匹配不到（如平台没回 `regular`），无法定位坏式 → 返回 ([], [])
        由调用方按"整批失败"处理，不盲目重发（重发只会再连坐一次）。
    返回: (culprits: [{"expr","error"}], survivors: [expr])
    """
    by_expr = {}
    by_idx = {}
    for e in errs or []:
        if e.get("status") not in _CULPRIT_STATUSES:
            continue
        ex = (e.get("expr") or "").strip()
        if ex:
            by_expr[ex] = e.get("error") or e.get("status")
        elif e.get("idx") is not None:
            by_idx[int(e["idx"])] = e.get("error") or e.get("status")
    # 2026-09-19 实测（JPN isotest2）：子模拟 GET 不回 `regular`，只能按 **children 顺序 = 提交顺序**
    # 映射；仅当 errs 覆盖了整批（子模拟数 == 本批表达式数）才可信，否则不猜。
    if by_idx and len(errs or []) == len(batch_exprs):
        for i, e in enumerate(batch_exprs):
            if i in by_idx:
                by_expr.setdefault(item_expr(e).strip(), by_idx[i])
    if not by_expr:
        return [], []
    culprits, survivors = [], []
    for e in batch_exprs:
        ex = item_expr(e).strip()
        if ex in by_expr:
            culprits.append({"expr": ex, "error": by_expr[ex]})
        else:
            survivors.append(e)
    if not culprits:
        return [], []
    return culprits, survivors


def _mark_culprits_in_db(ctx, wave, culprits):
    """坏式回写 expressions.status='fail'（reason=平台错误正文），让 build_wave/去重不再重选。
    失败不阻断（库只是审计面，不影响本波继续）。"""
    if not culprits:
        return 0
    try:
        st = _get_store(ctx)
    except Exception as e:  # pragma: no cover - 环境缺库
        print(f"[isolate] 坏式回写跳过（无 store）: {e}")
        return 0
    n = 0
    try:
        rows = st.list_expressions(ctx.region, str(wave))
        id_by_expr = {}
        for r in rows:
            ex = (r.get("expression") or "").strip()
            if ex and r.get("id") is not None:
                id_by_expr.setdefault(ex, int(r["id"]))
        for c in culprits:
            eid = id_by_expr.get(c["expr"])
            if eid is None:
                continue
            try:
                res = st.set_expression_status(
                    ctx.region, str(wave), "fail", ids=[eid],
                    reason=f"platform ERROR: {c['error'][:120]}")
                n += int(res.get("n_updated") or 0)
            except Exception as e:
                print(f"[isolate] 坏式 id={eid} 回写失败: {e}")
    finally:
        try:
            st.close()
        except Exception:
            pass
    return n


def _update_ck_batch(ck, bi, batch, msid, status, detail, api):
    """更新 checkpoint 中批次记录（COMPLETE/ERROR/其他）。"""
    rec = next((b for b in ck["batches"] if b.get("multisim") == msid), None)
    if not rec:
        rec = {"exprs": batch, "multisim": msid}
        ck["batches"].append(rec)
    rec["status"] = status
    if status == "COMPLETE":
        alphas = _harvest_batch_alphas(api, detail)
        rec["alphas"] = alphas
    elif status == "ERROR":
        errs = _harvest_batch_errors(api, detail)
        rec["errors"] = errs
    return rec


#: 提交期失败的重发上限（2026-10-02 P0）。429/瞬时网络错误是账户级限速或抖动，
#: 重发通常能过；但若平台持续拒绝，无限重发会烧光整轮时间。故按"批内容"计数，
#: 达到上限即落 SUBMIT_FAIL 终态（可由下一次跨轮重跑续命——SUBMIT_FAIL 不在 TERMINAL）。
MAX_SUBMIT_RETRY = 2

#: 在飞已空、账户级槽位被外部进程占满时的最长等待秒数（2026-10-02 死锁修复配套）。
#: 超过即放弃剩余队列并正常收尾（不静默丢失则打印放弃条数）。
_EXTERNAL_SLOT_WAIT_SEC = 1800


def _is_retryable_submit_error(err):
    """判断提交期异常是否值得重发（2026-10-02 P0）。

    可重发：HTTP 429（账户级限速）/ 5xx / 网络类（超时、连接重置/断开、SSL、URLError）。
    不可重发：4xx 其余（400 载荷非法、403 无权限等）——重发只会烧时间与配额。
    """
    if not err:
        return False
    s = str(err).lower()
    if "429" in s or "too many requests" in s:
        return True
    if " 50" in s or "503" in s or "502" in s or "504" in s:  # 5xx
        return True
    transient = ("timeout", "timed out", "connection reset", "connection aborted",
                 "remote end closed", "ssl", "urlopen error", "temporary failure",
                 "bad gateway", "service unavailable", "incompleteread",
                 "remotedisconnected", "connectionrefused")
    return any(t in s for t in transient)


def _batch_key(batch):
    """批次内容指纹：用于跨补批/重发跟踪已尝试次数（顺序敏感，同批同文本才同 key）。"""
    return "\x1f".join(batch)


def _run_round(api, ctx, ck, round_batches, n_slots, pcfg, checkpoint_dir, round_idx,
               pending_batches=None, isolate_errors=True, max_submit_retry=MAX_SUBMIT_RETRY):
    """执行单轮填槽（事件驱动即收即补，2026-09-17 P0 优化）。

    此前：两个独立 ThreadPoolExecutor（提交+轮询），全部完成后才返回进下一轮。
    问题：早完成的槽位空闲等待（如 1 批 5 分钟 COMPLETE，其余 6 批 15 分钟，
    该槽位空闲 10 分钟）。

    现改为：提交阶段不变（几秒完成）；轮询阶段每完成一批立即回收并补新批，
    保持槽位常满。pending_batches 为待补批次队列（引用传递，函数内会 pop）。

    2026-09-19 连坐隔离（isolate_errors，默认开）：某批 ERROR 时解析子模拟错误，
    定位坏式 → 坏式回写 expressions.status='fail' → 其余无辜表达式作为「重发批」
    **优先于** pending 队列在下一个空槽重发；重发批再 ERROR 不再重发（防死循环）。

    2026-10-02 P0 提交期失败重发：此前 Phase 1 提交抛异常（429/网络）即写
    SUBMIT_FAIL 后**永久丢弃**（不进 _retry_queue，同一次 run 内不再补），实测全库
    42 批 = 330 条表达式静默丢失（GBR s2_institutions6_d1 gate=93 却只入库 83）。
    现改为：可重发的提交失败（_is_retryable_submit_error）进入同一 _retry_queue
    （优先于 pending），按批内容指纹计数，重发至多 max_submit_retry 次；超限或
    不可重发的错误才落 SUBMIT_FAIL 终态。_refill 内的补批提交失败同规则。
    """
    n_batches = len(round_batches)
    if n_batches == 0:
        return 0, 0, {}

    print(f"[round{round_idx}] 填槽（即收即补）：{n_batches} 批分 {n_slots} 槽并行")

    # ---- Phase 1: 并行提交（不变，几秒完成）----
    # 2026-10-02 P0：重发队列与尝试计数在提交前建立，提交期失败即可入队。
    _retry_queue = []          # [(batch, origin_label, kind)]，重发优先于 pending；kind ∈ {isolation, submit}
    _retry_origin = {}         # new_bi -> origin（仅记录重发来源，便于排障）
    _isolation_retry = set()   # new_bi 集合：连坐隔离产生的重发批（再 ERROR 不重发，防死循环）
    _submit_attempts = {}      # batch 指纹 -> 已尝试次数（跨 Phase1/_refill 统一计数）
    _pending = pending_batches if pending_batches is not None else []
    _next_bi = n_batches + 1   # 补新批时的批次编号
    # 批次编号 → 该批表达式（round_batches 只存 ≤ n_batches 的首轮批；补批/重发批也要能反查）
    _batch_by_bi = {bi: round_batches[bi - 1] for bi in range(1, n_batches + 1)}
    submit_results = {}
    _slot_tokens = {}   # bi -> 账户级槽位 token（terminal 后释放）

    def _queue_retry_or_fail(batch, err, origin=None):
        """提交期失败处置（2026-10-02 P0）：可重发且未达上限 → 入重发队列；否则落 SUBMIT_FAIL。"""
        key = _batch_key(batch)
        tried = _submit_attempts.get(key, 0)
        if _is_retryable_submit_error(err) and tried < max_submit_retry:
            _submit_attempts[key] = tried + 1
            _retry_queue.append((batch, origin, "submit"))
            print(f"[submit] 提交失败可重发（第 {tried + 1}/{max_submit_retry} 次）: {err}")
            return
        rec = {"exprs": batch, "status": "SUBMIT_FAIL", "error": err}
        if origin:
            rec["retry_of"] = origin
        ck["batches"].append(rec)
        if _is_retryable_submit_error(err):
            print(f"[submit] 提交失败已达重发上限({max_submit_retry})，落 SUBMIT_FAIL: {err}")
        else:
            print(f"[submit] 提交失败（不可重发）: {err}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_slots) as pool:
        futures = {
            pool.submit(_submit_single_batch, api, ctx.settings,
                        _resolve_batch_items(ck, batch), bi, n_batches): bi
            for bi, batch in enumerate(round_batches, 1)
        }
        for fut in concurrent.futures.as_completed(futures):
            bi, msid, err, _tok = fut.result()
            submit_results[bi] = (msid, err)
            if _tok:
                _slot_tokens[bi] = _tok
            if err:
                print(f"[submit] round{round_idx} batch{bi}/{n_batches} 失败: {err}")
                _queue_retry_or_fail(round_batches[bi-1], err)
            else:
                print(f"[submit] round{round_idx} batch{bi}/{n_batches} multisim={msid} n={len(round_batches[bi-1])}")
                ck["batches"].append({
                    "exprs": round_batches[bi-1], "multisim": msid, "status": "RUNNING",
                    "submitted_at": datetime.datetime.now().isoformat(timespec="seconds")
                })
            ckpt_save(ctx, ck, checkpoint_dir)

    running = {bi: msid for bi, (msid, err) in submit_results.items() if not err}
    # 2026-10-02 P0：Phase 1 全军覆没但重发队列非空时，不能直接返回——交给 Phase 2 补发。
    if not running and not _retry_queue:
        print(f"[round{round_idx}] 无成功提交批次")
        return 0, 0, {}

    # ---- Phase 2: 事件驱动轮询+即收即补（P0 核心改动）----
    if running:
        print(f"[poll] round{round_idx} 事件驱动轮询 {len(running)} 个 multisim（即收即补）...")
    else:
        print(f"[poll] round{round_idx} 首轮全部提交失败，改为重发队列驱动（{len(_retry_queue)} 批）")
    poll_results = {}
    n_batch_retry = len(_retry_queue)   # 提交期失败入队数（统计用）
    isolated_total = 0
    resubmitted_total = 0

    def _refill(pool, futures):
        """槽位空出时补一批：重发批优先，其次 pending。返回是否补了。

        重发队列元素为三元组 (batch, origin, kind)：kind ∈ {"isolation", "submit"}。
        isolation = 连坐隔离的无辜兄弟（再 ERROR 不再重发）；submit = 提交期失败重发。
        """
        nonlocal _next_bi, resubmitted_total
        origin = None
        kind = "pending"
        if _retry_queue:
            new_batch, origin, kind = _retry_queue.pop(0)
        elif _pending:
            new_batch = _pending.pop(0)
        else:
            return False
        new_bi = _next_bi
        _next_bi += 1
        # 2026-10-02 死锁修复：补批路径在主线程，必须在飞满时**非阻塞放弃**本次补批，
        # 让主线程回去轮询回收 future（否则 7 token 全被本进程未轮询批次持有 = 自锁）。
        _tok = slots_mod.acquire(label=f"pending-b{new_bi}", nonblock=True)
        # acquire 返回 None 有两种相反的含义：真·槽位已满 vs 不仲裁（cap<=0 / 目录不可用）。
        # 只有「仲裁开着且在飞已满」才跳过补批；不仲裁时照常提交（token=None，release / relabel 对 None 安全）。
        # 2026-10-04：此前把任何 None 都当「满」，WQB_GLOBAL_SLOTS=0 下重发 / 补批永远提交不出去、空等 30 分钟。
        if _tok is None and slots_mod.is_full():
            # 未拿到槽位：回滚批次编号，把该批放回队列头，等下一轮回收后再补。
            _next_bi -= 1
            if kind == "pending":
                _pending.insert(0, new_batch)
            else:
                _retry_queue.insert(0, (new_batch, origin, kind))
            return False
        try:
            new_msid = submit_batch(api, ctx.settings, _resolve_batch_items(ck, new_batch))
            slots_mod.relabel(_tok, new_msid)
            _slot_tokens[new_bi] = _tok
            running[new_bi] = new_msid
            _batch_by_bi[new_bi] = new_batch
            entry = {
                "exprs": new_batch, "multisim": new_msid, "status": "RUNNING",
                "submitted_at": datetime.datetime.now().isoformat(timespec="seconds"),
            }
            if origin:
                entry["retry_of"] = origin
                _retry_origin[new_bi] = origin
                resubmitted_total += 1
            if kind == "isolation":
                _isolation_retry.add(new_bi)   # 连坐重发批：再 ERROR 不再重发
            ck["batches"].append(entry)
            new_fut = pool.submit(_poll_single_batch, api, new_msid, pcfg, new_bi)
            futures[new_fut] = new_bi
            if kind == "isolation":
                tag = f"连坐重发(源 {origin})"
            elif kind == "submit":
                tag = "提交失败重发"
            else:
                tag = "即收即补"
            print(f"[poll] round{round_idx} {tag}：batch{new_bi} multisim={new_msid} n={len(new_batch)}（槽位常满）")
        except Exception as e:
            slots_mod.release(_tok)
            # 2026-10-02 P0：补批提交失败同样按可重发规则处理（回队或落 SUBMIT_FAIL）
            print(f"[poll] round{round_idx} 即收即补失败: {e}")
            _queue_retry_or_fail(new_batch, str(e)[:200], origin=origin)
        ckpt_save(ctx, ck, checkpoint_dir)
        return True

    def _fill_slots(pool, futures):
        """把在飞数补到 n_slots（重发队列优先于 pending）；返回本轮是否补了。

        2026-10-02 P0：重发/补批的**提交**也在此发生，故提交失败会再次入队或被落
        SUBMIT_FAIL——因此必须在主循环里反复调用，直到队列与在飞都空。

        2026-10-02 死锁修复：_refill 内 acquire 走 nonblock；在飞满时本函数立即
        返回 False（不阻塞主线程），主循环据此转入 futures.wait() 回收。"""
        filled = False
        while len(futures) < n_slots:
            if not _retry_queue and not _pending:
                break
            if not _refill(pool, futures):
                break
            filled = True
        return filled

    _slot_wait_deadline = {"t": None}

    def _wait_external_slot(deadline_sec=_EXTERNAL_SLOT_WAIT_SEC):
        """在飞已空、仅剩外部进程占槽时，短暂休眠等待其释放。返回是否应继续重试。"""
        if _slot_wait_deadline["t"] is None:
            _slot_wait_deadline["t"] = time.time() + deadline_sec
        if time.time() > _slot_wait_deadline["t"]:
            return False
        time.sleep(10.0)
        return True

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_slots) as pool:
        # 初始提交所有 running 批次
        futures = {
            pool.submit(_poll_single_batch, api, msid, pcfg, bi): bi
            for bi, msid in running.items()
        }
        # 引导：Phase 1 全失败（futures 空）时，用重发队列把槽位填起来。
        _fill_slots(pool, futures)
        # 事件驱动：只要还有在飞 future，或还有重发/待补批（其提交会失败重入队或落库），就继续。
        # 旧写法 `while futures:` 在「引导补批全部提交失败」时退出，导致队列里剩余的重发被静默丢弃。
        while futures or _retry_queue or _pending:
            if not futures:
                # 在飞空但队列非空：补批。
                if _fill_slots(pool, futures):
                    continue
                # 补不进批 = 账户级槽位被外部进程占满（非本进程自锁，本进程在飞已空）。
                # 2026-10-02：此处**不可 break**（否则静默丢弃队列中剩余批）——
                # 改为短暂等待外部释放后重试；超时（默认 30min）才降级放弃。
                if not _wait_external_slot(deadline_sec=_EXTERNAL_SLOT_WAIT_SEC):
                    print(f"[poll] round{round_idx} 等待账户级槽位超时，放弃剩余 {len(_retry_queue) + len(_pending)} 批")
                    break
                continue
            # 等待任意一个 future 完成（不等待全部）
            done, _ = concurrent.futures.wait(
                futures.keys(), return_when=concurrent.futures.FIRST_COMPLETED
            )
            for fut in done:
                bi = futures.pop(fut)
                status, detail = fut.result()[1], fut.result()[2]
                poll_results[bi] = (status, detail)
                slots_mod.release(_slot_tokens.pop(bi, None))   # terminal：释放账户级槽位
                batch_exprs = _batch_by_bi.get(bi, [])
                rec = _update_ck_batch(ck, bi, batch_exprs, running.get(bi, ""), status, detail, api)
                if status == "COMPLETE":
                    print(f"[poll] round{round_idx} batch{bi} {running.get(bi, '')} COMPLETE alphas={len(rec.get('alphas', []))}")
                elif status == "ERROR":
                    errs = rec.get("errors", [])
                    n_bad = sum(1 for e in errs if e.get("status") in _CULPRIT_STATUSES)
                    print(f"[poll] round{round_idx} batch{bi} {running.get(bi, '')} ERROR"
                          f"（{n_bad} 个子模拟报错，{len(errs) - n_bad} 个连坐 CANCELLED）")
                    # ---- 连坐隔离：定位坏式 → 回写 fail → 无辜兄弟重发一次 ----
                    # 只有「连坐隔离产生的重发批」再 ERROR 才不再重发（防死循环）；
                    # 提交期失败重发批首次 ERROR 仍应走隔离（它此前根本没跑起来）。
                    if isolate_errors and bi not in _isolation_retry:
                        culprits, survivors = _isolate_error_batch(batch_exprs, errs)
                        if culprits:
                            rec["isolated_culprits"] = culprits
                            isolated_total += len(culprits)
                            for c in culprits:
                                print(f"[isolate] 坏式: {c['expr'][:90]} <- {c['error'][:80]}")
                            _mark_culprits_in_db(ctx, ck.get("wave"), culprits)
                            if survivors:
                                _retry_queue.append((survivors, running.get(bi, ""), "isolation"))
                                print(f"[isolate] {len(survivors)} 条无辜表达式排入重发队列（源 {running.get(bi, '')}）")
                        else:
                            print("[isolate] 无法从子模拟定位坏式（平台未回表达式），本批按整批失败处理，不重发")
                    elif isolate_errors:
                        print(f"[isolate] batch{bi} 是重发批（源 {_retry_origin.get(bi, '?')}）再次 ERROR，不再重发")
                else:
                    print(f"[poll] round{round_idx} batch{bi} {running.get(bi, '')} -> {status}")
                ckpt_save(ctx, ck, checkpoint_dir)

            # 即收即补：本轮所有完成项处理后，把槽位补满（重发批优先；提交失败会在队列/落库间自处理）
            _fill_slots(pool, futures)

    completed = sum(1 for s, _ in poll_results.values() if s == "COMPLETE")
    failed = sum(1 for s, _ in poll_results.values() if s in ("ERROR", "CANCELLED", "STALLED", "TIMEOUT"))
    # 提交期仍落在 SUBMIT_FAIL 的批次（重发上限耗尽/不可重发）——列出条数便于对齐 §6.5 完成定义
    n_submit_fail = sum(1 for b in ck.get("batches", [])
                        if isinstance(b, dict) and b.get("status") == "SUBMIT_FAIL")
    extra = f" 隔离坏式={isolated_total} 重发批={resubmitted_total}" if isolate_errors else ""
    if n_batch_retry:
        extra += f" 提交失败重发={n_batch_retry}"
    warn = f" ⚠ SUBMIT_FAIL 累计={n_submit_fail} 批（重发上限耗尽/不可重发，完成度不达标）" if n_submit_fail else ""
    print(f"[round{round_idx}] 回收：COMPLETE={completed} FAIL={failed} 补新批={_next_bi - n_batches - 1}{extra}{warn}")
    return completed, failed, poll_results


def stage_submit_poll(ctx, ck, passed, max_batches, force, checkpoint_dir=None,
                      max_rounds=1, serial=False, isolate_errors=True):
    """填槽多轮即收即补：max_rounds 轮，每轮并行提交 N 批、统一轮询、空槽补新批。
    serial=True 时每轮仅提 1 批并等其 terminal（单批在飞纪律，防平台并发取消）。"""
    api = Api(); api.login(*load_credentials())
    qc = quota_cfg(ctx)
    q = submission_quota(api, qc["limit"])
    print(f"[quota] used={q['used']} remaining={q['remaining']} reset={q['next_reset_utc']} enabled={qc.get('enabled', True)}")
    if qc.get("enabled", True) and q["remaining"] <= 0 and not force:
        print("[quota] 提交配额耗尽，中止回测发起（thresholds.submit_quota.enabled=true 才有此闸；--force 强行继续）")
        return

    exprs = [p["expr"] for p in passed]
    # per-item settings 附在 checkpoint（batch 中 expr 保持纯字符串，去重/续跑兼容）
    ov = ck.setdefault("item_overrides", {})
    for p in passed:
        if p.get("settings"):
            ov[p["expr"]] = p["settings"]
    done_exprs = {e for b in ck["batches"] if b.get("status") in TERMINAL
                  for e in b.get("exprs", [])}
    todo = [e for e in exprs if e not in done_exprs]
    if not todo:
        print("[submit] 全部批次已 terminal（checkpoint），跳过")
        return

    batch_size = ctx.batch_size()
    all_batches = [todo[i:i + batch_size] for i in range(0, len(todo), batch_size)]
    all_batches = all_batches[:max_batches]
    n_total = len(all_batches)
    n_slots = min(2, n_total) if not serial else 1
    pcfg = poll_config(ctx)

    mode = "串行单批" if serial else "填槽多轮"
    print(f"[slot] {mode}：总 {n_total} 批，{n_slots} 槽，最多 {max_rounds} 轮")

    total_completed = 0
    total_failed = 0
    round_idx = 0
    pending_batches = list(all_batches)  # 待提交批次队列

    while pending_batches and round_idx < max_rounds:
        round_idx += 1
        # 本轮取前 n_slots 批（或剩余全部）；串行模式每轮仅 1 批（单批在飞）
        round_batches = pending_batches[:n_slots]
        pending_batches = pending_batches[len(round_batches):]
        n_use = min(n_slots, len(round_batches))

        # P0 优化：传入 pending_batches 引用，_run_round 内部即收即补
        completed, failed, _ = _run_round(
            api, ctx, ck, round_batches, n_use, pcfg, checkpoint_dir, round_idx,
            pending_batches=pending_batches, isolate_errors=isolate_errors
        )
        total_completed += completed
        total_failed += failed

        # 即收即补：如果还有剩余批次且有槽位空出（失败/完成），继续下一轮
        if pending_batches:
            print(f"[slot] 即收即补：剩余 {len(pending_batches)} 批进入下一轮")
        else:
            print(f"[slot] 全部批次处理完毕")

    # 2026-10-02 P0：终局仍带 SUBMIT_FAIL 的批次（重发上限耗尽/不可重发）显式告警——
    # 这些批次的表达式没进 backtest_results，§6.5 完成度不达标，需重跑本波补齐。
    n_submit_fail_total = sum(1 for b in ck.get("batches", [])
                              if isinstance(b, dict) and b.get("status") == "SUBMIT_FAIL")
    print(f"[slot] 多轮汇总：{round_idx} 轮，COMPLETE={total_completed} FAIL={total_failed} 总批={n_total}")
    if n_submit_fail_total:
        print(f"[slot] ⚠ SUBMIT_FAIL 累计 {n_submit_fail_total} 批未入回测（提交期失败且重发上限耗尽）"
              f"——重跑本波可补齐（SUBMIT_FAIL 不在 TERMINAL，todo 会自动重取）")



def _submit_ready_list(d):
    """取台账 submit_ready 的可追加列表。历史形态两种：list（pipeline 原生）与 dict
    （select_ra_basket / 人工写入：{valid:[...], blocked:[...], updated, basket_mutual_corr}，
    IND/MEA/DEU 实存）。dict 形态追加进 valid，缺 valid 则建；其它类型重建为 list。
    2026-09-19 IND w182 首个候选落台账时 'dict' object has no attribute 'append' 实证。"""
    sr = d.get("submit_ready")
    if isinstance(sr, list):
        return sr
    if isinstance(sr, dict):
        v = sr.get("valid")
        if not isinstance(v, list):
            v = sr["valid"] = []
        return v
    d["submit_ready"] = []
    return d["submit_ready"]

#: 完成度闸容差（2026-10-02 P1）：planned - saved 超过该值即 WARN（默认 0 = 严格对齐 §6.5）。
#: 之所以允许配置：平台偶发「同 alpha 重复入库被 alpha_id 唯一键合并」会让 saved 略小于 planned，
#: 属正常收敛；真正的丢批（SUBMIT_FAIL 未重发）缺口是整批量级（≥ batch_size）。
COMPLETENESS_TOLERANCE = 0


def check_backtest_completeness(ck, n_saved, tolerance=COMPLETENESS_TOLERANCE):
    """波末完成度自检（2026-10-02 P1，对齐 step6-backtest.md §6.5）。

    §6.5 定义「backtest_results 行数 = 波内表达式数」，但此前**无任何代码校验**——
    提交期失败（429 等）落 SUBMIT_FAIL 的批次会被静默丢弃，波仍写 wave_results 判为
    完成（GBR s2_institutions6_d1 实证：gate=93 却只入库 83，零告警）。

    本函数比对 planned（= 闸 5 通过数）与 n_saved（= 本波 backtest_results 行数），
    返回 {planned, saved, missing, submit_fail_batches, ok, warn}。缺口 > tolerance 即
    warn=True（调用方决定打印/阻断）。**纯函数，不写库、不阻断**——是否升级为硬闸由调用方定。
    """
    planned = len((ck.get("stages", {}).get("gate", {}) or {}).get("passed") or [])
    batches = ck.get("batches") or []
    fail_batches = [b for b in batches if isinstance(b, dict) and b.get("status") == "SUBMIT_FAIL"]
    missing = max(0, planned - int(n_saved or 0))
    return {
        "planned": planned,
        "saved": int(n_saved or 0),
        "missing": missing,
        "submit_fail_batches": len(fail_batches),
        "ok": planned == 0 or missing <= tolerance,
        "warn": planned > 0 and missing > tolerance,
    }


def _count_wave_backtest_rows(ctx, wave):
    """查本波 backtest_results 现况行数（2026-10-02 P1）。库不可达返回 None（降级跳过）。"""
    try:
        st = _get_store(ctx)
        try:
            cur = st.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM backtest_results WHERE wave=?", (str(wave),))
            return int(cur.fetchone()[0])
        finally:
            st.close()
    except Exception as e:
        print(f"[complete] 行数查询失败，跳过完成度闸: {e}")
        return None


def _report_completeness(ctx, ck, n_saved, tolerance=COMPLETENESS_TOLERANCE):
    """波末完成度自检并打印（2026-10-02 P1）。以库里本波实际行数为准（非本次 upsert 数）。

    返回 result dict；n_saved 仅作 upsert 计数展示（库里可能有既往行或同 alpha 合并）。
    """
    live = _count_wave_backtest_rows(ctx, ck["wave"])
    result = check_backtest_completeness(ck, live if live is not None else n_saved, tolerance)
    result["live_rows"] = live
    result["upserted"] = int(n_saved or 0)
    if result["warn"]:
        print(f"[complete] ⚠ 完成度不达标：planned={result['planned']} 入库={result['saved']} "
              f"缺={result['missing']}（SUBMIT_FAIL 批={result['submit_fail_batches']}）"
              f"——核对 step6-backtest.md §6.5，缺批多为提交期 429 未重发，应重跑本波补齐")
    else:
        print(f"[complete] 完成度 OK：planned={result['planned']} 入库={result['saved']}"
              f"（本轮 upsert={result['upserted']}）")
    return result


# ---------------------------------------------------------------------------
# 步 7 P0（2026-10-02）：s4_walls 结构化写盘
# ---------------------------------------------------------------------------
# 断流实证：`s4_walls_<region>_<wave>` 此前唯一写者是 campaign.py:715，而它只在
# `workflow_campaign(stage="S4")` 路径上执行。SOP 主路径 `pipeline.py --review`
# 只把 walls 塞进 wave_results，**从不写该键** → 近 21 天 25 个 s2_ 波 0 个有该键，
# `step_eval.py:350` 的 S4 质量指标 `walls_coverage` 实测恒为 0。
# 更糟的是 campaign.py 的写者靠**关键词扫描子进程 stdout**（_extract_walls_summary），
# 实测会漏报（全 PASS 输出 → None）与误报（含 "structural" 字样的告警行 → 假墙）。
# 本函数用**已算好的结构化 r["walls"]** 聚合，不经任何文本解析。

def build_s4_walls_payload(region, wave, rows, reviewed_at=None):
    """把评审行的 `walls` 聚合成结构化 s4_walls payload（纯函数，单测用）。

    rows: 每行 dict（须已由 review_mod.walls() 填好 `walls` 列表；无 walls 者视为达标）。
    返回 {"walls": {墙名: 命中条数}, "n_rows", "n_candidates", "per_alpha": {...},
         "reviewed_at", "region", "wave"}。
    与 campaign.py 的**旧**关键词产物（{structural: True, ...}）格式不同：旧值是 bool、
    新值是计数；下游 step_eval 只数键数，两种都兼容，但新格式可读性显著更高。
    """
    import datetime as _dt
    per_alpha = {}
    wall_count = {}
    n_cand = 0
    for r in rows or []:
        if not isinstance(r, dict):
            continue
        aid = r.get("id") or r.get("alpha_id")
        ws = [w for w in (r.get("walls") or []) if w]
        if not ws:
            n_cand += 1
        for w in ws:
            wall_count[w] = wall_count.get(w, 0) + 1
        if aid:
            per_alpha[aid] = ws
    # 按命中数降序，便于人读（dict 保序）
    ordered = {k: wall_count[k] for k in sorted(wall_count, key=lambda x: -wall_count[x])}
    return {
        "walls": ordered,
        "n_rows": len([r for r in (rows or []) if isinstance(r, dict)]),
        "n_candidates": n_cand,
        "per_alpha": per_alpha,
        "reviewed_at": reviewed_at or _dt.datetime.now().isoformat(timespec="seconds"),
        "region": region,
        "wave": str(wave),
    }


def _write_s4_walls(ctx, ck, rows, reviewed_at=None):
    """写结构化 `s4_walls_<region>_<wave>` 到 ledger（2026-10-02 P0）。失败不阻断。

    键名与 campaign.py 保持 `s4_walls_<region>_<wave>` 一致（step_eval 按
    `key LIKE 's4_walls_%_%'` 统计），值换成结构化 payload。
    """
    try:
        payload = build_s4_walls_payload(ctx.region, ck["wave"], rows, reviewed_at)
        store = make_ledger_store(ctx)

        def mut(d):
            d[f"s4_walls_{ctx.region}_{ck['wave']}"] = payload
        store.update(mut)
        print(f"[s4_walls] 已写结构化墙摘要：{len(payload['walls'])} 类墙 / "
              f"{payload['n_rows']} 行（{len(payload['per_alpha'])} 条 per-alpha 明细）")
        return payload
    except Exception as e:  # noqa: BLE001 — 台账写入失败不阻断评审
        print(f"[s4_walls] 写入失败（不阻断）: {e}")
        return None


def stage_review(ctx, ck, write_ledger, checkpoint_dir=None, out=None):
    if ck["stages"].get("review", {}).get("done"):
        print("[review] 已完成（checkpoint），跳过")
        return
    alphas = [a for b in ck["batches"] for a in b.get("alphas", [])]
    if not alphas:
        print("[review] 无 alpha 可评审")
        return
    t = ctx.thresh("review")
    rows = metrics_cache.fetch_rows(ctx, alphas)
    # 2026-09-17 优化：无候选时跳过 walls 诊断（对判死波次无价值）。
    # 先快速检查是否有任何候选可能（max|sharpe| >= near 阈值），无则直接入库并返回。
    _near_thresh = ctx.thresh("near")["sharpe_min"]
    _has_potential = any(
        r.get("sharpe") and abs(r["sharpe"]) >= _near_thresh for r in rows
    )
    if not _has_potential:
        # 全灭波次：直接入库 backtest_results + wave_results，跳过 walls 诊断
        st = _get_store(ctx)
        try:
            # L3 写库互斥（2026-09-20）：收批批量入库排队（短锁）
            from _lib.dblock import write_lock as _wlock
            with _wlock(tag="dbwrite_pipeline_save", ttl_sec=300, wait_timeout=120):
                n_saved = st.save_backtest_results(ctx.region, ck["wave"], rows, dataset=ck.get("dataset"))
            print(f"[db] backtest_results +{n_saved}/{len(rows)}（wave={ck['wave']}，全灭快速入库）")
        finally:
            st.close()
        # 2026-10-02 P1：完成度自检（全灭通道同样要查——丢批与是否全灭无关）
        completeness = _report_completeness(ctx, ck, n_saved)
        try:
            from _lib.wave_results import WaveResultsStore
            wr = WaveResultsStore(ctx.region, ctx=ctx)
            ms_ids = [b.get("multisim") for b in ck.get("batches", []) if b.get("multisim")]
            wr.auto_upsert_from_review(
                ck["wave"], rows, [], [],
                settings=ctx.settings, multisim_ids=ms_ids)
        except (Exception, SystemExit) as e:
            print(f"[wave_results] 自动入库异常（不阻断）: {e}")
        try:
            region_kb_mod.refresh_after_wave(
                ctx, ck["wave"], rows, [], [], verdict="FAIL", dataset=ck.get("dataset"))
        except (Exception, SystemExit) as e:
            print(f"[region_kb] 刷新异常（不阻断）: {e}")
        print(f"[review] total={len(rows)} candidates=0 near=0（全灭快速通道）")
        # 2026-10-02 P0：全灭通道也要写 s4_walls——否则"整波撞同一堵墙"这一最需要留档的
        # 场景反而无键可查（step_eval walls_coverage 会把这类波记成未覆盖）。
        # 全灭通道此前刻意跳过 walls 诊断（对判死波无价值），但**记账**成本极低（纯计算不调 API），
        # 且正是停止规则 B（连续 3 波 FAIL）判据的依据来源，故此处补算 walls。
        for _r in rows:
            if _r.get("sharpe") is not None and not _r.get("walls"):
                _r["walls"] = review_mod.walls(_r, t)
        _write_s4_walls(ctx, ck, rows)
        ck["stages"]["review"] = {"done": True, "candidates": 0, "near": 0,
                                  "completeness": completeness}
        ckpt_save(ctx, ck, checkpoint_dir)
        return
    # ---- 回测结果入 backtest_results（必须成功；库为唯一持久化）----
    st = _get_store(ctx)
    try:
        # L3 写库互斥（2026-09-20）：收批批量入库排队（短锁）
        from _lib.dblock import write_lock as _wlock
        with _wlock(tag="dbwrite_pipeline_save", ttl_sec=300, wait_timeout=120):
            n_saved = st.save_backtest_results(ctx.region, ck["wave"], rows, dataset=ck.get("dataset"))
        print(f"[db] backtest_results +{n_saved}/{len(rows)}（wave={ck['wave']}）")
    finally:
        st.close()
    # 2026-10-02 P1：完成度自检（防提交期丢批被当"完成"）
    completeness = _report_completeness(ctx, ck, n_saved)
    candidates = [r for r in rows if review_mod.passes(r, t)]
    near = []
    t_near = ctx.thresh("near")
    excluded = {}
    for r in rows:
        if r in candidates or not r.get("sharpe"):
            continue
        if r["sharpe"] > t_near["sharpe_min"]:
            r["walls"] = review_mod.walls(r, t)
            # 结构性死信号（2026-09-19）与 RN_EXPOSURE（2026-09-27 R4）不入 near：与 review_wave
            # 同一判据，否则全灭波被记成 PARTIAL，停止规则 B 永不触发
            blocked = review_mod.near_block_wall(r, t, t_near)
            if blocked:
                if blocked not in r["walls"]:
                    r["walls"].append(blocked)
                excluded[blocked] = excluded.get(blocked, 0) + 1
                continue
            near.append(r)
    review_mod.report_near_exclusions(excluded, t, t_near)
    # ---- wave_results 自动入库（波次结论 + near 池，替代 review JSON 文件）----
    try:
        from _lib.wave_results import WaveResultsStore
        wr = WaveResultsStore(ctx.region, ctx=ctx)
        ms_ids = [b.get("multisim") for b in ck.get("batches", []) if b.get("multisim")]
        out_wr = wr.auto_upsert_from_review(
            ck["wave"], rows, candidates, near,
            settings=ctx.settings, multisim_ids=ms_ids)
        if out_wr.get("skipped"):
            print(f"[wave_results] 跳过: {out_wr.get('reason')}")
        else:
            print(f"[wave_results] wave={out_wr['wave_number']} -> {out_wr['status']} "
                  f"(findings={out_wr['key_findings_n']} candidates={out_wr['candidates_n']})")
    except (Exception, SystemExit) as e:
        # SystemExit 不继承 Exception，而 _lib/wave_results.upsert 的契约校验
        # （wave_number / status / verdict 三态）用的正是 raise SystemExit。只写
        # except Exception 会让「不阻断」名不副实——2026-09-08 实测回测落库后
        # pipeline 静默死在这里，review checkpoint 不落、台账不写、下游全断。
        print(f"[wave_results] 自动入库异常（不阻断）: {e}")
    # ---- region_kb 波后自动刷新（2026-09-15 ③）：recent_waves + gate_priors_local + updated_at ----
    # 此前回路只写 wave_results，不回 KB：GBR 三波关闭后 region_kb.updated_at 仍停在 09-12，
    # 下一波 S2 先验（assemble-priors 读 region_kb）与 S3 设置先验读到的都是旧知识。
    try:
        _verdict = "PASS" if candidates else ("PARTIAL" if near else "FAIL")
        region_kb_mod.refresh_after_wave(
            ctx, ck["wave"], rows, candidates, near,
            verdict=_verdict, dataset=ck.get("dataset"))
    except (Exception, SystemExit) as e:
        print(f"[region_kb] 刷新异常（不阻断）: {e}")
    print(f"[review] total={len(rows)} candidates={len(candidates)} near={len(near)}")
    # 2026-10-02 P0：写结构化 s4_walls（消除「SOP 主路径不写该键」断流；见 build_s4_walls_payload 注释）
    _write_s4_walls(ctx, ck, rows)
    if write_ledger:
        store = make_ledger_store(ctx)

        def mut(d):
            sr = _submit_ready_list(d)
            for c in candidates:
                if not any((x.get("id") if isinstance(x, dict) else x) == c["id"] for x in sr):
                    sr.append({"id": c["id"], "note": f"pipeline {ck['wave']} 全门槛过",
                               "queued_at": today()})
        store.update(mut)
        print(f"[ledger] submit_ready +{len(candidates)}")
    ck["stages"]["review"] = {"done": True, "candidates": len(candidates), "near": len(near),
                              "completeness": completeness}
    ckpt_save(ctx, ck, checkpoint_dir)

    # ---- L1 采集：收割后自动提取方法论信号 -> 候选规则 ----
    wave_meta = {"region": ctx.region, "universe": ctx.settings.get("universe"),
                 "wave": ck["wave"]}
    try:
        signals = rules_mod.extract_signals(rows, wave_meta)
        if signals:
            store = rules_mod.RuleStore(ctx.dir)
            for sig in signals:
                store.upsert(sig)
                print(f"[rules][L1] 提取信号 -> {sig['rule_id']} ({sig['type']}, "
                      f"conf={sig.get('confidence')}, status={sig.get('status')})")
    except Exception as e:
        print(f"[rules][L1] 信号提取异常（不阻断）: {e}")

    # ---- L4 验证：用本次收割数据校验已有规则（证伪/强化）----
    try:
        vrep = rules_mod.validate_rules(ctx, rows, wave_meta)
        if vrep["validated"]:
            print(f"[rules][L4] 校验 {vrep['validated']} 条："
                  f"强化={len(vrep['reinforced'])} 降级={len(vrep['degraded'])} "
                  f"证伪={len(vrep['falsified'])}")
            for rid in vrep["falsified"]:
                print(f"[rules][L4] 证伪 -> {rid}（已标 contested，触发翻案批复核）")
    except Exception as e:
        print(f"[rules][L4] 规则校验异常（不阻断）: {e}")


def main():
    ap = argparse.ArgumentParser(description="战役端到端编排器")
    add_campaign_arg(ap)
    # 2026-09-12 修复（方案B）：--from-db / --no-from-db 提升为顶层全局参数。
    # 根因：二者原是 run 子命令局部参数，argparse subparsers 只认"子命令之后"的
    # 局部 flag —— 一旦被放到 run 之前（extra_args 误排 / 手写命令），顶层解析器
    # 不认识即抛 unrecognized arguments，且 detached 模式下被吞成 success。
    # 提升到顶层后，run 前后位置均合法；子命令侧用 SUPPRESS 避免默认值覆盖顶层。
    ap.add_argument("--from-db", action="store_true", default=True,
                    help="从数据库读取表达式（默认启用；顶层全局参数，run 前后均可）")
    ap.add_argument("--no-from-db", action="store_true", default=False,
                    help="禁用数据库模式，改用 --file（场景3 per-item settings 输入走此路）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _sub_campaign_arg(sp):
        # 子命令后也可传 --campaign-dir；SUPPRESS 防子命令默认值覆盖顶层已传值
        sp.add_argument("--campaign-dir", dest="campaign_dir",
                        default=argparse.SUPPRESS,
                        help="战役目录路径（缺省=当前工作目录；也可放子命令前）")

    q = sub.add_parser("quota")
    _sub_campaign_arg(q)
    q.add_argument("--dry-run", action="store_true", help="打印计算过程")
    p = sub.add_parser("run")
    _sub_campaign_arg(p)
    p.add_argument("--file", help="表达式文件路径（JSON 格式，已废弃，请使用 --from-db）")
    # --from-db / --no-from-db 已提升为顶层参数（见上）。此处用 SUPPRESS 保留子命令
    # 位置的兼容性（老命令 `run --from-db` 仍合法），SUPPRESS 使未显式传时不产出
    # 属性、不覆盖顶层已解析的值；显式传时与顶层同 dest，正常生效。
    p.add_argument("--from-db", action="store_true", default=argparse.SUPPRESS,
                   help="从数据库读取表达式（默认启用；同顶层全局参数）")
    p.add_argument("--no-from-db", action="store_true", default=argparse.SUPPRESS,
                   help="禁用数据库模式，改用 --file（同顶层全局参数）")
    p.add_argument("--dataset", required=True)
    p.add_argument("--datasets", default="",
                   help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix，与 gate.py --datasets 同语义）")
    p.add_argument("--wave", required=True)
    p.add_argument("--submit", action="store_true")
    p.add_argument("--review", action="store_true")
    p.add_argument("--write-ledger", action="store_true")
    p.add_argument("--prod-first", action="store_true",
                   help="评审后自动跑 tools/campaign_intel.py prod-first（每信号族最强 1 条探 prod；"
                        "SOP 步 5b：新族第二波前必查）")
    p.add_argument("--prod-first-top-k", type=int, default=2)
    p.add_argument("--prod-first-min-sharpe", type=float, default=1.0)
    p.add_argument("--forum-recon", action="store_true",
                   help="评审后自动跑 tools/forum_recon_wave.py（波级默认取证：对本波共同卡住的墙问一次论坛，每波 ≤ 1 次，"
                        "结果落 ledger；只读、不阻断，工具故障不占本波额度）")
    p.add_argument("--neutralization", default=None,
                   help="覆盖 settings.neutralization（中性化 A/B 实验用；MARKET/SUBINDUSTRY/SECTOR）")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                   help="覆盖 settings 任意字段，可多次（如 --set maxTrade=ON --set startDate=2014-01-01）；复刻已知强 alpha 必需")
    p.add_argument("--max-batches", type=int, default=99)
    p.add_argument("--max-rounds", type=int, default=1,
                   help="填槽最大轮次（默认 1=单轮全提全收；>1 启用多轮即收即补）")
    p.add_argument("--no-isolate-errors", action="store_true",
                   help="关闭连坐隔离（默认开：ERROR 批解析坏式→回写 fail→无辜兄弟重发一次）")
    p.add_argument("--serial", action="store_true",
                   help="串行提交：一次只提 1 批，terminal 后再提下一批（单批在飞纪律，防多批并行被平台 CANCELLED）")
    p.add_argument("--batch-type", default="explore", choices=["explore", "repair", "probe"],
                   help="批次类型：explore=探索批（默认，受闸6 约束）；repair=修复/设置变体批（豁免）")
    p.add_argument("--skip-diversity-gate", action="store_true",
                   help="跳过闸6 批级多样性强制（逃生阀，需在台账记录原因）")
    p.add_argument("--sanity-all", action="store_true",
                   help="一次性跑闸 7+8（longCount 真实性 + EVENT 类型检测）")
    p.add_argument("--force", action="store_true",
                   help="越过两道可选的中止：① universe 命中判死规则；② 提交配额耗尽——②只在区域 "
                        "thresholds.submit_quota.enabled=true 时才存在（缺省关闭）。不提交 alpha、不消耗配额，"
                        "只是不中止回测发起。")
    p.add_argument("--fresh", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="不提交，仅走 gate+编排框架")
    p.add_argument("--checkpoint-dir", default=None, help="checkpoint 重定向（测试用临时目录）")
    p.add_argument("--no-settings-prior", action="store_true",
                   help="不按 region_kb.gate_priors 实测过闸率改写 decay/neutralization（默认启用；"
                        "显式 --set/--neutralization 的维度本就不会被改）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    rc = _cmd_main(a, ctx)
    if rc:
        # 2026-09-15 ⑥：中止路径一律非零退出。此前所有 `return` 都是 rc=0，
        # detached 启动器/节点只看退出码 → "启动成功"却什么都没跑（S2-COMPLIANCE 中止实证）。
        sys.exit(rc)


def _cmd_main(a, ctx):
    """run/quota 主体；返回退出码（0=正常，2=中止/前置不满足）。"""

    if a.cmd == "quota":
        api = Api(); api.login(*load_credentials())
        qc = quota_cfg(ctx)
        res = submission_quota(api, qc["limit"])
        if a.dry_run:
            print(f"[dry-run] limit={qc['limit']}（REGULAR 日上限；SUPER 1/日由提交层单独把关）")
            print(f"[dry-run] ET 日={res['et_day']} 当日已提交={res['used']}")
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0

    ck = ckpt_load(ctx, a.wave, fresh=a.fresh, checkpoint_dir=a.checkpoint_dir)
    if getattr(a, "dataset", None):
        ck["dataset"] = a.dataset  # region_kb.recent_waves 需要数据集归属
    if a.neutralization:
        ctx.settings["neutralization"] = a.neutralization
        print(f"[neut] 覆盖 neutralization={a.neutralization}（本轮 wave={a.wave}）")
    elif _neut_query_top is not None and a.dataset:
        # P1-1 (2026-08-31): 用户未显式指定中性化时，按 neut_cache 推荐最优
        # （WebDataScope 数据包回填的 dataset×neutralization 历史 sharpe 排名）。
        # 仅当缓存有该数据集记录时推荐，否则保持 settings 默认（不阻断）。
        try:
            _delay = ctx.settings.get("delay", 1)
            _top = _neut_query_top(ctx.region, _delay, a.dataset, top=1)
            if _top:
                _rec_neut = _top[0].get("neutralization")
                _rec_sr = _top[0].get("sharpe_ratio")
                if _rec_neut and _rec_neut != ctx.settings.get("neutralization"):
                    print(f"[neut][P1-1] 缓存推荐 neutralization={_rec_neut} "
                          f"（dataset={a.dataset} 历史 sharpe={_rec_sr:.3f}），"
                          f"当前 settings={ctx.settings.get('neutralization')}；"
                          f"如需采纳请显式 --neutralization {_rec_neut}")
        except Exception as _e:
            print(f"[neut][P1-1] 缓存查询异常（不阻断）: {_e}")
    for kv in a.set:
        k, _, v = kv.partition("=")
        if not k:
            continue
        # 类型强制：decay=6 -> int 6；truncation=0.08 -> float；maxTrade=ON -> 字符串（平台字段类型匹配）
        if v in ("true", "false"):
            ctx.settings[k] = (v == "true")
        else:
            try:
                ctx.settings[k] = int(v)
            except ValueError:
                try:
                    ctx.settings[k] = float(v)
                except ValueError:
                    ctx.settings[k] = v
        print(f"[set] 覆盖 settings.{k}={ctx.settings[k]!r}（本轮 wave={a.wave}）")

    # ---- 区域 × 类别组合（2026-10-04）：config/cells.json 的回测 / 阈值覆盖 ----
    # 直跑 CLI 也吃组合覆盖（workflow_batch_track 已把它们以 --set 传进来，这里看到的是已钉住的维度，不会重复改）。
    # 显式 --set / --neutralization 优先于组合；被组合改写的维度记进 ctx.cell_pinned，下面的设置先验不再动它。
    _cli_pinned = {kv.partition("=")[0] for kv in a.set if kv.partition("=")[0]}
    if a.neutralization:
        _cli_pinned.add("neutralization")
    try:
        ctx.bind_cell(getattr(a, "dataset", None), pinned=_cli_pinned)
    except Exception as _e:
        print(f"[cell] 组合绑定异常（不阻断，按区域配置跑）: {_e}")

    # ---- 设置层先验（2026-09-15 ①）：region_kb.gate_priors 的 decay/neutralization 实测过闸率 ----
    # 此前这两个维度只被渲染成文本进 GEM prompt（LLM 改不了仿真设置），S3 永远用 settings.json
    # 固定值。现按证据改写本轮设置；显式 --set / --neutralization 钉住的维度不动。
    if not a.no_settings_prior:
        try:
            region_kb_mod.apply_settings_prior(ctx, pinned=_cli_pinned, cfg=ctx.thresh("settings_prior"))
        except Exception as _e:
            print(f"[settings-prior] 异常（不阻断）: {_e}")

    # ---- L3 规则硬门 1：universe 杠杆判死校验（OPT-2 修复）----
    intended_uni = ctx.settings.get("universe")
    uni_ok, uni_msgs = rules_mod.check_universe_lever(ctx, intended_uni)
    for m in uni_msgs:
        print(m)
    if not uni_ok and not a.force:
        print(f"[rules] universe={intended_uni} 命中判死规则，中止（--force 强行继续）")
        return 2

    # ---- L3 规则硬门 2：settings 快照防呆（settings_wave_lock_v1）----
    # 启动时快照实际生效的 universe/neutralization 进 checkpoint，防外部并发改导致误跑
    ck.setdefault("settings_snapshot", {})
    snap = {"universe": intended_uni,
            "neutralization": ctx.settings.get("neutralization"),
            "at": datetime.datetime.now().isoformat(timespec="seconds")}
    prev = ck["settings_snapshot"]
    if prev and prev.get("universe") != snap["universe"]:
        print(f"[rules] 警告：本次 universe={snap['universe']} 与 checkpoint 快照 "
              f"{prev.get('universe')} 不一致（wave={a.wave}），疑似外部并发改 settings")
    ck["settings_snapshot"] = snap
    ckpt_save(ctx, ck, a.checkpoint_dir)

    # ---- L3 规则提示：命中当前上下文的 strategy/diagnosis 规则 ----
    for r in rules_mod.apply_rules(ctx, "strategy",
                                   {"region": ctx.region, "universe": intended_uni}):
        print(f"[rules][strategy:{r['rule_id']}] {r.get('action', {}).get('message', '')}")

    # ---- S2 合规记录：仅提示，不再中止（2026-09-15 ⑥ 降级）----
    # 2026-08-26 起这里是硬闸：没有 s2_compliance_w<wave>（特征工程文档路径）就 return，
    # 且退出码 0。审计实证：它只检查"有条 ledger 指向一份文档"，不验内容；而文档本身是
    # 确定性模板渲染（8 问框架），对表达式质量零贡献；Mode B 手工批还得 --force 绕过。
    # 真正保障闸 2/3 的是 typed catalog（下方 stage_gate 缺目录会 FAIL），不是这条记录。
    s2_compliance_ok, s2_msg = _check_s2_compliance(ctx, a.wave)
    if s2_compliance_ok:
        print(f"[S2-COMPLIANCE] 记录存在: {s2_msg}")
    else:
        print(f"[S2-COMPLIANCE] 无合规记录（仅提示，不阻断）: {s2_msg}")

    # 读取表达式（默认从数据库；--no-from-db + --file 仅兼容 per-item settings）
    if a.from_db and not a.no_from_db:
        try:
            st = _get_store(ctx)
            try:
                expressions_data = st.load_wave_expressions(ctx.region, a.wave)
                if not expressions_data:
                    # 2026-09-01 wave 别名解析：GEM 标签格式（如 s2_model50_d1 /
                    # model50_IND_d1）与战役编号（如 72）是两套体系；
                    # 精确匹配失败时按候选别名自动解析，避免"有表达式却查不到"。
                    for alias in _wave_aliases(ctx, a, st):
                        expressions_data = st.load_wave_expressions(ctx.region, alias)
                        if expressions_data:
                            print(f"[wave-alias] wave={a.wave} 未命中，自动解析为 {alias}"
                                  f"（命中 {len(expressions_data)} 条）")
                            a.wave = alias
                            break
            finally:
                st.close()
            # 2026-09-19：DB 行的 settings（expressions.settings_json）只保留仿真设置键并作为
            # per-item override 带入提交（此前被丢弃 → w177 decay=12 变体静默跑成基线，平台回同一 alpha）。
            exprs = []
            for e in expressions_data:
                if not e.get("expression"):
                    continue
                ov = _sim_settings_only(e.get("settings"))
                exprs.append({"expr": e["expression"], "settings": ov} if ov else e["expression"])
            print(f"[db] 从数据库读取 {len(exprs)} 个表达式: {ctx.region}/{a.wave}")
            if not exprs:
                print(f"[error] 数据库中没有找到 wave={a.wave} 的表达式")
                print("[hint] 请先 GEM/build_wave --from-db 写入 expressions")
                print("[hint] 也可用 mcp__wqb-db__list_wave_results 查现有 wave 编号")
                return 2
        except Exception as e:
            print(f"[error] 从数据库读取失败: {e}")
            print("[hint] 请确保 data/wqb.db 可用（WQB_ROOT / WQB_DB_PATH）")
            return 2
    else:
        print("[warning] 文件模式仅用于 per-item settings 兼容")
        if not a.file:
            print("[error] --no-from-db 需要 --file")
            return 2
        exprs = read_expr_items(a.file)
    n_ov = sum(1 for it in exprs if item_settings(it))
    if n_ov:
        print(f"[items] 检测到 {n_ov}/{len(exprs)} 条带 per-item settings（场景3：各自设置覆盖基础设置）")
    
    passed = stage_gate(ctx, ck, exprs, a.dataset, a.checkpoint_dir, a.datasets)
    # ---- 批级闸（闸6 多样性契约 + 可选闸7/8 sanity）：自动批量防退化 ----
    # 仅真实提交（--submit 且非 dry-run）时消费契约（幂等）；dry-run/plan 只检查不消费
    # 探针批（batch_type=probe）语义即豁免闸6：单骨架裸测用于归因，骨架多样性会污染归因。
    # 依据 diversity_gate_is_portfolio_level_not_per_wave_v1（2026-10-04 KOR 818 波次实证）。
    # 与 --skip-diversity-gate 等价但语义自解释——探针波应优先用 --batch-type probe 而非手动逃生阀。
    _skip_div = a.skip_diversity_gate or a.batch_type == "probe"
    if a.batch_type == "probe" and not a.skip_diversity_gate:
        print("[gate] batch_type=probe（探针批）→ 自动豁免闸6 骨架多样性"
              "（依据 diversity_gate_is_portfolio_level_not_per_wave_v1）")
    ok_batch, _ = stage_batch_gates(
        ctx, ck, passed, a.dataset,
        batch_type=a.batch_type, skip_diversity=_skip_div,
        sanity_all=a.sanity_all, consume=(a.submit and not a.dry_run),
        checkpoint_dir=a.checkpoint_dir, datasets_extra=a.datasets)
    if not ok_batch:
        print("[gate] 批级闸未过，中止（--skip-diversity-gate 逃生，或补充多样性槽位后重跑）")
        return 2
    if a.dry_run:
        batch_size = ctx.batch_size()
        n_batches = (len(passed) + batch_size - 1) // batch_size
        n_slots = min(2, n_batches)
        print(f"[dry-run] gate 过 {len(passed)} 式，将分 {n_batches} 批（batch={batch_size}，"
              f"填槽 n_slots={n_slots}）；未提交。checkpoint: {ckpt_path(ctx, a.wave, a.checkpoint_dir)}")
        return 0
    if not a.submit:
        print(f"[plan] gate 过 {len(passed)} 式；加 --submit 提交（填槽 + 配额闸）")
        return 0
    stage_submit_poll(ctx, ck, passed, a.max_batches, a.force, a.checkpoint_dir,
                      max_rounds=a.max_rounds, serial=a.serial,
                      isolate_errors=not getattr(a, "no_isolate_errors", False))
    if a.review:
        stage_review(ctx, ck, a.write_ledger, a.checkpoint_dir)
    if getattr(a, "prod_first", False):
        stage_prod_first(ctx, a)
    if getattr(a, "forum_recon", False):
        stage_forum_recon(ctx, a)                    # 放在 prod-first 之后：prod 相关性写回后，prod 墙才看得见
    print(f"[done] checkpoint: {ckpt_path(ctx, a.wave, a.checkpoint_dir)}")
    return 0


def stage_prod_first(ctx, a):
    """2026-09-19 SOP 步 5b 自动化：收批评审后立刻对本波每个信号族最强 1 条探 prod（子进程调
    tools/campaign_intel.py prod-first，同一 venv）。prod ≥ 0.7 的族在台账 prod_first_<wave> 标 STOP，
    下一波不得再投该族变体（IND intraday_pv_feats 3 波 24 条全 IS 过才发现 prod 0.79-0.92 的教训）。"""
    import subprocess
    repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
    for cand in (os.environ.get("WQB_ROOT"), repo):
        if cand and os.path.isfile(os.path.join(cand, "tools", "campaign_intel.py")):
            repo = cand
            break
    tool = os.path.join(repo, "tools", "campaign_intel.py")
    if not os.path.isfile(tool):
        print("[prod-first] tools/campaign_intel.py 不存在，跳过")
        return
    out_json = os.path.join(repo, "logs", f"prod_first_{ctx.region}_{a.wave}.json")
    cmd = [sys.executable, tool, "prod-first", "--region", ctx.region, "--wave", str(a.wave),
           "--top-k", str(a.prod_first_top_k), "--min-sharpe", str(a.prod_first_min_sharpe),
           "--write-ledger", "--json", out_json]
    print(f"[prod-first] 收批后族级 prod 探针：{' '.join(cmd[2:])}")
    try:
        r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=3600)
        for line in (r.stdout or "").splitlines():
            if line.startswith(("=== prod-first", "  ", "[prod-first]", "[ledger]", "[out]")):
                print(line)
        if r.returncode not in (0, 3):
            print(f"[prod-first] 退出码 {r.returncode}: {(r.stderr or '')[-300:]}")
    except Exception as e:
        print(f"[prod-first] 执行异常（不阻断）: {e}")


def stage_forum_recon(ctx, a):
    """波级默认取证（2026-09-30）：收批评审后，对本波共同卡住的墙（全灭时为「有无解法」）问一次论坛——子进程调
    tools/forum_recon_wave.py（同一 venv）。每波 ≤ 1 次，结果落 ledger：`forum_recon_<qkey>` 有解 /
    `forum_recon_negative_<qkey>` 无解 / `forum_recon_error_<qkey>` 故障，另留完成标记 `forum_recon_wave_<wave>`。
    **只读、不阻断**：论坛不可达 / 缺凭据只打印（故障 ≠ 无解，也不占本波额度），收批结论不受影响。"""
    import json
    import subprocess
    repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
    for cand in (os.environ.get("WQB_ROOT"), repo):
        if cand and os.path.isfile(os.path.join(cand, "tools", "forum_recon_wave.py")):
            repo = cand
            break
    tool = os.path.join(repo, "tools", "forum_recon_wave.py")
    if not os.path.isfile(tool):
        print("[forum-recon] tools/forum_recon_wave.py 不存在，跳过")
        return
    cmd = [sys.executable, tool, "--region", ctx.region, "--wave", str(a.wave), "--dataset", str(a.dataset)]
    try:
        timeout = int(os.environ.get("WQB_FORUM_RECON_TIMEOUT_SEC") or 900)
    except ValueError:
        timeout = 900
    print(f"[forum-recon] 收批后波级取证：{' '.join(cmd[2:])}")
    try:
        r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=timeout)
        summary = None
        for line in reversed((r.stdout or "").splitlines()):
            if line.startswith('{"tool": "forum_recon_wave"'):
                try:
                    summary = json.loads(line)
                except ValueError:
                    pass
                break
        if r.returncode not in (0, 2):                # 1 = 工具故障（不是「论坛无解」）；不阻断收批
            print(f"[forum-recon] 工具故障（退出码 {r.returncode}，不是「论坛无解」，不占本波额度）："
                  f"{((summary or {}).get('error') or r.stderr or '')[-300:]}")
        elif summary and summary.get("skipped"):
            print(f"[forum-recon] 未查（{summary.get('reason')}）：{summary.get('note') or ''}")
        elif summary:
            print(f"[forum-recon] {summary.get('kind')}/{summary.get('wall') or '-'} found={summary.get('found')} "
                  f"status={summary.get('status')} → {summary.get('sink') or summary.get('marker')}：{summary.get('question')}")
    except Exception as e:
        print(f"[forum-recon] 执行异常（不阻断）: {e}")


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()
