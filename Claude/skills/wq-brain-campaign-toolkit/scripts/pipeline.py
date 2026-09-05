# -*- coding: utf-8 -*-
"""pipeline.py - 战役端到端编排器：gate -> submit -> poll -> review -> ledger。

带 checkpoint/resume（断点续跑纪律）。七槽填槽多轮即收即补（2026-08-25 更新：5→7）：
- 单轮模式（默认）：并行提交 N 批（N=min(7, 批数)），统一轮询，全提全收。
- 多轮模式（--max-rounds>1）：每轮并行提交 n_slots 批，轮询回收后空槽补新批，
  保持槽位常满直至全部批次处理完毕或达到最大轮次。
轮询退避+挂起熔断（_lib/poller）；提交前 ET 日历日配额闸（REGULAR 4/日 + SUPER 1/日，00:00 ET 重置）。

用法:
  python pipeline.py --campaign-dir <DIR> quota [--dry-run]
      ET 日历日提交配额（REGULAR 4/日 + SUPER 1/日；--dry-run 打印计算过程）
  python pipeline.py --campaign-dir <DIR> run --file candidates/x.json --dataset model219 --wave 01A
      默认只跑 gate 并打印提交计划（不烧配额）
  python pipeline.py --campaign-dir <DIR> run ... --submit [--max-batches 2] [--max-rounds 3] [--force]
      过闸后按批提交（七槽填槽模式）+ 轮询到 terminal（挂起熔断）
  python pipeline.py --campaign-dir <DIR> run ... --submit --review --write-ledger
      全链路：评审 + 回写台账
  恢复：重跑同一 --wave 自动从 checkpoint 续跑；--fresh 强制全新。
  --dry-run：不提交、checkpoint 写到 --checkpoint-dir（默认战役 results/；测试可指临时目录）。
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, atomic_write, load_credentials,
                         load_json, read_exprs_file, read_expr_items)
from _lib.api import Api, api_call
from _lib.poller import TERMINAL, poll_config, poll_until_terminal
from _lib.ledger import LedgerStore, make_ledger_store, today
from _lib import rules as rules_mod
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
    for cand in (r"D:\coding\traeCN_project\wqb",):
        if os.path.isdir(os.path.join(cand, "src", "wqb")):
            return cand
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


# ---------------- quota：ET 日历日提交配额（REGULAR 4/日 + SUPER 1/日，00:00 ET 重置） ----------------

# 2026-09-01 定案：提交配额从"48h 滚动窗口"改为"ET 日历日"模型。
#   - REGULAR 4 颗/ET 日历日，SUPER 1 颗/ET 日历日；00:00 ET（= 12:00 GMT+8）重置。
#   - 旧"48h 滚动"已证伪（08-12 一次 48h 内提交 6 颗全成功）。
#   - `get_submission_quota` MCP 工具已于 2026-08-25 移除；其旧 `hours_until_release` 语义有 bug，勿再依赖。
#   - 剩余额度从 submit 响应 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 的 value/limit 读（value 从 0 起计数）。
#   - 硬闸 FAIL 的提交不消耗配额（status 保持 UNSUBMITTED）。
# 本函数按 ET 日历日聚合 `/users/self/activities/submissions`（比 OS alphas 更贴近"已提交"语义），
# 无法取到 activities 时回退按 `dateSubmitted` 的 ET 日聚合 OS alphas。

def _et_day_bounds(now_utc):
    """返回当前 ET 日历日的 [start_utc, next_start_utc]。ET = UTC-5（EST）/ UTC-4（EDT）。
    简化口径：全年用 UTC-4（EDT）——与 `alphas.date_submitted` 落库时区（-04:00）一致，
    避免夏令时切换导致日界漂移。"""
    et_offset = datetime.timedelta(hours=4)
    et_now = now_utc - et_offset
    et_day_start = et_now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_start_utc = et_day_start + et_offset
    return day_start_utc, day_start_utc + datetime.timedelta(days=1)


def _count_submissions_by_et_day(submitted_ts_list):
    """按 ET 日历日（UTC-4 简化口径）统计当日已提交数。入参为 tz-aware datetime 列表。"""
    from collections import defaultdict
    et_offset = datetime.timedelta(hours=4)
    day_count = defaultdict(int)
    for t in submitted_ts_list:
        et = t - et_offset
        key = et.strftime("%Y-%m-%d")
        day_count[key] += 1
    return day_count


def _submitted_ts_from_activities(api):
    """从 /users/self/activities/submissions 取当日（及最近）提交时间戳；失败返回 None。"""
    try:
        j = json.load(api.get("/users/self/activities/submissions"))
    except Exception:
        return None
    out = []
    for item in j.get("results", j if isinstance(j, list) else []):
        ds = item.get("dateSubmitted") or item.get("createdAt") or item.get("date")
        if not ds:
            continue
        try:
            out.append(datetime.datetime.fromisoformat(ds.replace("Z", "+00:00")))
        except Exception:
            continue
    return out


def submission_quota(api, limit, window_h=None):
    """ET 日历日提交配额视图。limit=REGULAR 日上限（默认 4）；window_h 保留仅向后兼容，不再参与计算。"""
    now = datetime.datetime.now(datetime.timezone.utc)
    day_start, day_end = _et_day_bounds(now)

    submitted_ts = _submitted_ts_from_activities(api)
    fallback = submitted_ts is None
    if fallback:
        # 回退：按 OS alphas 的 dateSubmitted 聚合（可能高估，因含 SUPER/被拒但以提交记录为准）
        j = json.load(api.get("/users/self/alphas?stage=OS&limit=100&order=-dateSubmitted"))
        submitted_ts = []
        for a in j.get("results", []):
            ds = a.get("dateSubmitted")
            if not ds:
                continue
            try:
                submitted_ts.append(datetime.datetime.fromisoformat(ds.replace("Z", "+00:00")))
            except Exception:
                continue

    day_count = _count_submissions_by_et_day(submitted_ts)
    today_key = (now - datetime.timedelta(hours=4)).strftime("%Y-%m-%d")
    used = day_count.get(today_key, 0)
    remaining = max(0, limit - used)
    release = day_end.isoformat()
    return {"used": used, "remaining": remaining, "next_reset_utc": release,
            "limit": limit, "et_day": today_key, "source": "activities" if not fallback else "os_alphas_fallback",
            "_note": "ET 日历日配额（REGULAR 4/日 + SUPER 1/日，00:00 ET=12:00 GMT+8 重置）；"
                     "旧 48h 滚动口径已废止。硬闸 FAIL 提交不消耗配额。"}


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
    """提交单批并返回 (bi, msid, error)。供 ThreadPool 并行调用。"""
    try:
        msid = submit_batch(api, settings, batch)
        return bi, msid, None
    except Exception as e:
        return bi, None, str(e)[:200]


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
    """从 ERROR 的 multisim detail 提取子模拟错误。"""
    errs = []
    for c in detail.get("children", []):
        try:
            sim = json.load(api_call(api, "get", "/simulations/" + c))
            if sim.get("error"):
                errs.append({"child": c, "error": str(sim["error"])[:120]})
        except Exception:
            pass
    return errs


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


def _run_round(api, ctx, ck, round_batches, n_slots, pcfg, checkpoint_dir, round_idx):
    """执行单轮七槽填槽：并行提交+轮询 round_batches，返回 (completed, failed, results)。"""
    n_batches = len(round_batches)
    if n_batches == 0:
        return 0, 0, {}

    print(f"[round{round_idx}] 七槽填槽：{n_batches} 批分 {n_slots} 槽并行")

    # ---- Phase 1: 并行提交 ----
    submit_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_slots) as pool:
        futures = {
            pool.submit(_submit_single_batch, api, ctx.settings,
                        _resolve_batch_items(ck, batch), bi, n_batches): bi
            for bi, batch in enumerate(round_batches, 1)
        }
        for fut in concurrent.futures.as_completed(futures):
            bi, msid, err = fut.result()
            submit_results[bi] = (msid, err)
            if err:
                print(f"[submit] round{round_idx} batch{bi}/{n_batches} 失败: {err}")
                ck["batches"].append({"exprs": round_batches[bi-1], "status": "SUBMIT_FAIL", "error": err})
            else:
                print(f"[submit] round{round_idx} batch{bi}/{n_batches} multisim={msid} n={len(round_batches[bi-1])}")
                ck["batches"].append({
                    "exprs": round_batches[bi-1], "multisim": msid, "status": "RUNNING",
                    "submitted_at": datetime.datetime.now().isoformat(timespec="seconds")
                })
            ckpt_save(ctx, ck, checkpoint_dir)

    running = {bi: msid for bi, (msid, err) in submit_results.items() if not err}
    if not running:
        print(f"[round{round_idx}] 无成功提交批次")
        return 0, 0, {}

    # ---- Phase 2: 并行轮询 ----
    print(f"[poll] round{round_idx} 并行轮询 {len(running)} 个 multisim...")
    poll_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_slots) as pool:
        futures = {
            pool.submit(_poll_single_batch, api, msid, pcfg, bi): bi
            for bi, msid in running.items()
        }
        for fut in concurrent.futures.as_completed(futures):
            bi, status, detail = fut.result()
            poll_results[bi] = (status, detail)
            rec = _update_ck_batch(ck, bi, round_batches[bi-1], running[bi], status, detail, api)
            if status == "COMPLETE":
                print(f"[poll] round{round_idx} batch{bi} {running[bi]} COMPLETE alphas={len(rec.get('alphas', []))}")
            elif status == "ERROR":
                print(f"[poll] round{round_idx} batch{bi} {running[bi]} ERROR（{len(rec.get('errors', []))} 个子模拟错误）")
            else:
                print(f"[poll] round{round_idx} batch{bi} {running[bi]} -> {status}")
            ckpt_save(ctx, ck, checkpoint_dir)

    completed = sum(1 for s, _ in poll_results.values() if s == "COMPLETE")
    failed = sum(1 for s, _ in poll_results.values() if s in ("ERROR", "CANCELLED", "STALLED", "TIMEOUT"))
    print(f"[round{round_idx}] 回收：COMPLETE={completed} FAIL={failed} 利用率={len(running)}/{n_slots}")
    return completed, failed, poll_results


def stage_submit_poll(ctx, ck, passed, max_batches, force, checkpoint_dir=None,
                      max_rounds=1, serial=False):
    """七槽填槽多轮即收即补：max_rounds 轮，每轮并行提交 N 批、统一轮询、空槽补新批。
    serial=True 时每轮仅提 1 批并等其 terminal（单批在飞纪律，防平台并发取消）。"""
    api = Api(); api.login(*load_credentials())
    qc = quota_cfg(ctx)
    q = submission_quota(api, qc["limit"])
    print(f"[quota] used={q['used']} remaining={q['remaining']} reset={q['next_reset_utc']} enabled={qc.get('enabled', True)}")
    if qc.get("enabled", True) and q["remaining"] <= 0 and not force:
        print("[quota] 提交配额耗尽，中止（--force 强行继续）")
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
    n_slots = min(7, n_total) if not serial else 1
    pcfg = poll_config(ctx)

    mode = "串行单批" if serial else "七槽填槽多轮"
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

        completed, failed, _ = _run_round(
            api, ctx, ck, round_batches, n_use, pcfg, checkpoint_dir, round_idx
        )
        total_completed += completed
        total_failed += failed

        # 即收即补：如果还有剩余批次且有槽位空出（失败/完成），继续下一轮
        if pending_batches:
            print(f"[slot] 即收即补：剩余 {len(pending_batches)} 批进入下一轮")
        else:
            print(f"[slot] 全部批次处理完毕")

    print(f"[slot] 多轮汇总：{round_idx} 轮，COMPLETE={total_completed} FAIL={total_failed} 总批={n_total}")


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
    # ---- 回测结果入 backtest_results（必须成功；库为唯一持久化）----
    st = _get_store(ctx)
    try:
        n_saved = st.save_backtest_results(ctx.region, ck["wave"], rows)
        print(f"[db] backtest_results +{n_saved}/{len(rows)}（wave={ck['wave']}）")
    finally:
        st.close()
    candidates = [r for r in rows if review_mod.passes(r, t)]
    near = []
    for r in rows:
        if r not in candidates and r.get("sharpe") and r["sharpe"] > ctx.thresh("near")["sharpe_min"]:
            r["walls"] = review_mod.walls(r, t)
            near.append(r)
    # ---- wave_results 自动入库（波次结论 + near 池，替代 review JSON 文件）----
    try:
        from _lib.wave_results import WaveResultsStore
        wr = WaveResultsStore(ctx.region)
        ms_ids = [b.get("multisim") for b in ck.get("batches", []) if b.get("multisim")]
        out_wr = wr.auto_upsert_from_review(
            ck["wave"], rows, candidates, near,
            settings=ctx.settings, multisim_ids=ms_ids)
        if out_wr.get("skipped"):
            print(f"[wave_results] 跳过: {out_wr.get('reason')}")
        else:
            print(f"[wave_results] wave{out_wr['wave_number']} -> {out_wr['status']} "
                  f"(findings={out_wr['key_findings_n']} candidates={out_wr['candidates_n']})")
    except Exception as e:
        print(f"[wave_results] 自动入库异常（不阻断）: {e}")
    print(f"[review] total={len(rows)} candidates={len(candidates)} near={len(near)}")
    if write_ledger:
        store = make_ledger_store(ctx)

        def mut(d):
            sr = d.setdefault("submit_ready", [])
            for c in candidates:
                if not any((x.get("id") if isinstance(x, dict) else x) == c["id"] for x in sr):
                    sr.append({"id": c["id"], "note": f"pipeline {ck['wave']} 全门槛过",
                               "queued_at": today()})
        store.update(mut)
        print(f"[ledger] submit_ready +{len(candidates)}")
    ck["stages"]["review"] = {"done": True, "candidates": len(candidates), "near": len(near)}
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
    p.add_argument("--from-db", action="store_true", default=True, help="从数据库读取表达式（默认启用）")
    p.add_argument("--no-from-db", action="store_true",
                   help="禁用数据库模式，改用 --file（场景3 per-item settings 输入走此路）")
    p.add_argument("--dataset", required=True)
    p.add_argument("--datasets", default="",
                   help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix，与 gate.py --datasets 同语义）")
    p.add_argument("--wave", required=True)
    p.add_argument("--submit", action="store_true")
    p.add_argument("--review", action="store_true")
    p.add_argument("--write-ledger", action="store_true")
    p.add_argument("--neutralization", default=None,
                   help="覆盖 settings.neutralization（中性化 A/B 实验用；MARKET/SUBINDUSTRY/SECTOR）")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                   help="覆盖 settings 任意字段，可多次（如 --set maxTrade=ON --set startDate=2014-01-01）；复刻已知强 alpha 必需")
    p.add_argument("--max-batches", type=int, default=99)
    p.add_argument("--max-rounds", type=int, default=1,
                   help="七槽填槽最大轮次（默认 1=单轮全提全收；>1 启用多轮即收即补）")
    p.add_argument("--serial", action="store_true",
                   help="串行提交：一次只提 1 批，terminal 后再提下一批（单批在飞纪律，防多批并行被平台 CANCELLED）")
    p.add_argument("--batch-type", default="explore", choices=["explore", "repair"],
                   help="批次类型：explore=探索批（默认，受闸6 约束）；repair=修复/设置变体批（豁免）")
    p.add_argument("--skip-diversity-gate", action="store_true",
                   help="跳过闸6 批级多样性强制（逃生阀，需在台账记录原因）")
    p.add_argument("--sanity-all", action="store_true",
                   help="一次性跑闸 7+8（longCount 真实性 + EVENT 类型检测）")
    p.add_argument("--force", action="store_true")
    p.add_argument("--fresh", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="不提交，仅走 gate+编排框架")
    p.add_argument("--checkpoint-dir", default=None, help="checkpoint 重定向（测试用临时目录）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)

    if a.cmd == "quota":
        api = Api(); api.login(*load_credentials())
        qc = quota_cfg(ctx)
        res = submission_quota(api, qc["limit"])
        if a.dry_run:
            print(f"[dry-run] limit={qc['limit']}（REGULAR 日上限；SUPER 1/日由提交层单独把关）")
            print(f"[dry-run] ET 日={res['et_day']} 当日已提交={res['used']}")
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return

    ck = ckpt_load(ctx, a.wave, fresh=a.fresh, checkpoint_dir=a.checkpoint_dir)
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

    # ---- L3 规则硬门 1：universe 杠杆判死校验（OPT-2 修复）----
    intended_uni = ctx.settings.get("universe")
    uni_ok, uni_msgs = rules_mod.check_universe_lever(ctx, intended_uni)
    for m in uni_msgs:
        print(m)
    if not uni_ok and not a.force:
        print(f"[rules] universe={intended_uni} 命中判死规则，中止（--force 强行继续）")
        return

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

    # ---- S2 合规硬闸：特征工程文档校验（2026-08-26 新增）----
    # 防止跳过 brain-data-feature-engineering skill 直接手写候选池
    # 2026-09-01 dry-run 豁免：dry-run 不提交不烧配额，目的就是检查编排，
    # 缺合规记录时降级 WARN 继续展示计划，不要求 --force（force 语义是"强行烧配额"）。
    s2_compliance_ok, s2_msg = _check_s2_compliance(ctx, a.wave)
    if not s2_compliance_ok:
        print(f"[S2-COMPLIANCE] {s2_msg}")
        if a.dry_run:
            print("[S2-COMPLIANCE] dry-run 模式：降级 WARN 继续（不提交、不烧配额；正式 run 仍需合规或 --force）")
        else:
            print("[S2-COMPLIANCE] 中止：必须先完成特征工程 skill 并记录文档路径")
            print("[S2-COMPLIANCE] 逃生阀：--force 强行继续（需在台账记录原因）")
            if not a.force:
                return
            print("[S2-COMPLIANCE] --force 已启用，强行继续（请确保已补录台账）")
    else:
        print(f"[S2-COMPLIANCE] 通过: {s2_msg}")

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
            exprs = [e["expression"] for e in expressions_data if e.get("expression")]
            print(f"[db] 从数据库读取 {len(exprs)} 个表达式: {ctx.region}/{a.wave}")
            if not exprs:
                print(f"[error] 数据库中没有找到 wave={a.wave} 的表达式")
                print("[hint] 请先 GEM/build_wave --from-db 写入 expressions")
                print("[hint] 也可用 mcp__wqb-db__list_wave_results 查现有 wave 编号")
                return
        except Exception as e:
            print(f"[error] 从数据库读取失败: {e}")
            print("[hint] 请确保 data/wqb.db 可用（WQB_ROOT / WQB_DB_PATH）")
            return
    else:
        print("[warning] 文件模式仅用于 per-item settings 兼容")
        if not a.file:
            print("[error] --no-from-db 需要 --file")
            return
        exprs = read_expr_items(a.file)
    n_ov = sum(1 for it in exprs if item_settings(it))
    if n_ov:
        print(f"[items] 检测到 {n_ov}/{len(exprs)} 条带 per-item settings（场景3：各自设置覆盖基础设置）")
    
    passed = stage_gate(ctx, ck, exprs, a.dataset, a.checkpoint_dir, a.datasets)
    # ---- 批级闸（闸6 多样性契约 + 可选闸7/8 sanity）：自动批量防退化 ----
    # 仅真实提交（--submit 且非 dry-run）时消费契约（幂等）；dry-run/plan 只检查不消费
    ok_batch, _ = stage_batch_gates(
        ctx, ck, passed, a.dataset,
        batch_type=a.batch_type, skip_diversity=a.skip_diversity_gate,
        sanity_all=a.sanity_all, consume=(a.submit and not a.dry_run),
        checkpoint_dir=a.checkpoint_dir, datasets_extra=a.datasets)
    if not ok_batch:
        print("[gate] 批级闸未过，中止（--skip-diversity-gate 逃生，或补充多样性槽位后重跑）")
        return
    if a.dry_run:
        batch_size = ctx.batch_size()
        n_batches = (len(passed) + batch_size - 1) // batch_size
        n_slots = min(7, n_batches)
        print(f"[dry-run] gate 过 {len(passed)} 式，将分 {n_batches} 批（batch={batch_size}，"
              f"七槽填槽 n_slots={n_slots}）；未提交。checkpoint: {ckpt_path(ctx, a.wave, a.checkpoint_dir)}")
        return
    if not a.submit:
        print(f"[plan] gate 过 {len(passed)} 式；加 --submit 提交（七槽填槽 + 配额闸）")
        return
    stage_submit_poll(ctx, ck, passed, a.max_batches, a.force, a.checkpoint_dir,
                      max_rounds=a.max_rounds, serial=a.serial)
    if a.review:
        stage_review(ctx, ck, a.write_ledger, a.checkpoint_dir)
    print(f"[done] checkpoint: {ckpt_path(ctx, a.wave, a.checkpoint_dir)}")


if __name__ == "__main__":
    main()
