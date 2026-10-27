# -*- coding: utf-8 -*-
"""仿真传输层：在飞槽位 / 派发 / 收割。**所有可能挂起的地方都集中在这里**。"""
import os
import sys
import json
import re
import asyncio
import sqlite3
import subprocess
import collections
import time
from datetime import datetime

from .config import *            # noqa: F401,F403
from .config import _WQB_SCRIPTS_DIR  # noqa: F401

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from campaign_semantics import (  # noqa: E402,F401
    LIT_THRESHOLD, VIRGIN_AC, VIRGIN_VS, VIRGIN_MIN_COV, VIRGIN_COV_FLOOR,
    is_virgin, all_datasets, exposure_profile,
    NAME_META, is_name_metadata, classify_desc,
    FORM_FAMILIES, GATED_CATS, GATE_Q, POSTPROC_Q, PER_DIM, MIN_FIELDS_TOTAL,
    FULL_FIELD_CAP, BLACKBOX_FAMILIES, field_tier,
    FAMILY_EXPOSURE, EXPOSURE_VOCAB, EXPR_EXPOSURE, field_exposure_hint,
    CONCEPT_FAMILIES, CONCEPT_ZH, field_concepts, concept_families,
    PP_VOCAB, parse_preprocessing, load_s1_preprocessing, apply_preprocessing,
    _DESC_NOISE, clean_desc, _load_form_overrides, _load_llm_tags, LLM_CONF_MIN,
    FORM_EVIDENCE, field_form, print_form_audit,
)
from . import bad_tokens as _bt
from .bad_tokens import filter_bad, norm_tpl, load_bad_tokens, note_bad_tokens
from .persist import beat


MAX_INFLIGHT = 7      # 用户设定（2026-10-23 上调 4→7）：平台并发上限约 10，留 3 个机动位


_TERMINAL = {"COMPLETE", "FAIL", "ERROR", "CANCELLED"}
GATE_TIMEOUT = 900    # 2026-10-25：2400 → 900。批次正常生命周期远短于此；旧值下


_FORCED_RELEASE = 0


def sims_terminal(sim_id):
    """该 multisim 的子任务是否全部终态（COMPLETE/FAIL/…）。用于限制在飞作业数。

    ★ 2026-10-25 修：改为**三态**返回值。
    旧实现 `except Exception: return False` 把「网络抖动 / 30s 超时 / JSON 解析失败」
    一律当成「还没跑完」，于是 `wait_slot` 会对一个**早已终态**的批次继续干等满 GATE_TIMEOUT。
    这是 model182 卡死 1839s 的直接机制（11 个模板族 → 批次首次超过 MAX_INFLIGHT=7
    → `wait_slot` 首次真正介入 → 撞上状态查询异常 → 静默死等）。
    现返回：True=全部终态 / False=确实还有在跑 / None=**查不到（异常）**，由调用方区别处理。
    """
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    async def _go():
        await brain_client.ensure_authenticated()
        resp = await brain_client._request(
            "GET", f"{brain_client.base_url}/simulations/{sim_id}")
        try:
            j = resp.json()
        except Exception:
            return None
        # ★ 2026-10-25 定位到的老 bug：平台对无效 sim id 会直接返回**字符串体**
        #   （如 "Invalid simulation id"），而旧代码直接 j.get(...) ⇒
        #   AttributeError: 'str' object has no attribute 'get'。
        #   表现就是日志里反复出现的「查 … 状态异常：AttributeError」（一直查不到根因）。
        if not isinstance(j, dict):
            return None
        # 父批已是终态 ⇒ 直接判定（省掉 N 次子查询）
        if str(j.get("status") or "").upper() in _TERMINAL:
            return True
        kids = j.get("children") or []
        if not kids:
            return False
        # ★ 2026-10-25 修（IND 开波实测）：平台返回的 `children` 是**子任务 id 字符串**
        #   （[loc1, loc2, ...]），不是 dict 列表。旧代码对字符串调 `.get` ⇒
        #   AttributeError ⇒ sims_terminal 恒返回 None ⇒ wait_slot 每 3 次就"强制放行"
        #   ⇒ `--max-inflight` 形同虚设。必须逐个子任务查状态（tools/batch_status.py 同口径）。
        for k in kids:
            if isinstance(k, dict):
                if str(k.get("status") or "").upper() not in _TERMINAL:
                    return False
                continue
            r2 = await brain_client._request(
                "GET", f"{brain_client.base_url}/simulations/{k}")
            try:
                j2 = r2.json()
            except Exception:
                return None
            if not isinstance(j2, dict):
                return None
            if str(j2.get("status") or "").upper() not in _TERMINAL:
                return False
        return True

    try:
        return asyncio.run(_go())
    except Exception as e:
        # 2026-10-25 修：原先只记 type，没法定位。带消息 + 首个栈帧。
        import traceback as _tb
        _frames = _tb.extract_tb(e.__traceback__)
        _where = f"{os.path.basename(_frames[-1].filename)}:{_frames[-1].lineno}" if _frames else "?"
        print(f"  [gate] 查 {str(sim_id)[:16]} 状态异常（按未知处理）："
              f"{type(e).__name__}: {str(e)[:120]} @ {_where}")
        return None


def wait_slot(pending, timeout=None):
    """在飞数到上限时，等最早那批跑完腾出名额（pending 原地修改）。

    ★ 2026-10-25 修三处（model182 静默卡死 1839s 事故）：
    1. **加心跳**：每 4 次轮询（≈60s）打印一次在飞/累计等待，静默不可能超过 1 分钟
       —— 旧版全程静默，看门狗只能靠 mtime 判停滞，且人看日志完全看不出卡在哪。
    2. **异常不再当"在跑"**：连续 3 次 `sims_terminal` 返回 None（查不到状态）即强制放行。
       旧版把异常吞成 False，一个早已终态的批次会被无限等下去。
    3. **GATE_TIMEOUT 2400 → 900**：批次正常生命周期远短于此；宁可短暂超并发也不静默死等。
    """
    global _FORCED_RELEASE
    timeout = timeout or GATE_TIMEOUT
    while len(pending) >= MAX_INFLIGHT:
        sid = pending[0]
        t0 = time.time()
        done = False
        polls = 0
        unknown = 0
        while time.time() - t0 < timeout:
            if sid is None:
                done = True
                break
            st = sims_terminal(sid)
            if st is True:
                done = True
                break
            if st is None:
                unknown += 1
                if unknown >= 3:
                    print(f"  [gate] {str(sid)[:12]} 连续 {unknown} 次查不到状态 ⇒ "
                          f"按已放行处理（避免静默死等）")
                    done = True
                    break
            else:
                unknown = 0
            polls += 1
            if polls % 4 == 0:
                print(f"  [gate] 等 {str(sid)[:12]}｜已等 {int(time.time() - t0)}s"
                      f"｜在飞 {len(pending)}/{MAX_INFLIGHT}｜未知 {unknown}")
            time.sleep(15)
        pending.pop(0)
        if done:
            continue
        _FORCED_RELEASE += 1
        print(f"  [gate] {sid} 等待 {timeout}s 超时，强制放行"
              f"（累计超限放行 {_FORCED_RELEASE} 次，实际并发可能 >{MAX_INFLIGHT}）")


def dispatch(exprs, ds, label, on_batch=None, settings=None):
    """模板优先派发：每个模板单独分批（≤10/批）→ [(sim_id, template, batch_idx)]。

    ⚠ 2026-10-22 实测：n=1 的批次提交后必为 ``COMPLETE children=0``，结果永远收不到
    （用已知有效表达式复现同样如此）。故分批改为**均分**，杜绝出现单条批：
    11 条 → 6+5 而不是 10+1。

    ★ 2026-10-22 用户设定：同时最多 MAX_INFLIGHT=4 个作业在跑。
    ★ 2026-10-23 修复：
      - `settings` 可覆写设置（设置轴扫描用：universe / neutralization / decay / truncation）；
      - 派发前按 BAD_TOKENS 过滤（一条坏式会毒死整批，实测 4 次）；
      - wait_slot 超时提到 2400s，并发上限真正生效。
    """
    exprs, n_bad = filter_bad(exprs)
    if n_bad:
        print(f"  [preflight] {ds}/{label}: 丢弃 {n_bad} 条"
              f"（命中平台黑名单 {sorted(_bt.BAD_TOKENS)}）")
    # 区域缺省设置（EUR=TOPCS1600/FAST/ON；IND=TOP500/STATISTICAL/OFF×2）
    st = {k: str(v) for k, v in REGION_SETTINGS.items()}
    st = {"universe": st["universe"], "decay": st["decay"],
          "neutralization": st["neutralization"], "truncation": st["truncation"],
          "nan_handling": st["nan_handling"], "max_trade": st["max_trade"]}
    if settings:
        st.update({k: str(v) for k, v in settings.items()})
    by_tpl = collections.defaultdict(list)
    for tpl, e in exprs:
        by_tpl[tpl].append(e)
    sims = []
    pending = []
    for tpl, elist in by_tpl.items():
        n = len(elist)
        nb = max(1, -(-n // 10))                   # ceil 批数（每批 ≤10）
        base, rem = divmod(n, nb)                  # 均分：rem 批 base+1，其余 base
        sizes = [base + 1] * rem + [base] * (nb - rem)
        batches, pos = [], 0
        for s in sizes:
            batches.append(elist[pos:pos + s])
            pos += s
        for bi, b in enumerate(batches):
            wait_slot(pending)                     # ★ 在飞上限 4：满了先等最早那批终态
            fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{tpl}_{bi}.txt")
            with open(fn, "w", encoding="utf-8") as fh:
                fh.write("\n".join(b) + "\n")
            cmd = [VENV_PY, WQB_TOOLS, "dispatch", fn,
                   "--label", f"camp_{ds}_{label}_{tpl}_{bi}",
                   "--region", REGION, "--universe", st["universe"], "--decay", st["decay"],
                   "--neutralization", st["neutralization"], "--truncation", st["truncation"],
                   "--nan-handling", st["nan_handling"], "--max-trade", st["max_trade"],
                   # ⚠ 2026-10-22 撤回 QUICK：实测 QUICK↔FULL 失真不可预测（-0.18~+0.87，
                   # E5VmWRnL QUICK 1.60→FULL 0.73），连相对排序都不可信 ⇒ 回退 FULL。
                   "--simulation-mode", "FULL",
                   "--force", "--allow-probe-repeat"]
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout
                m = re.search(r'"sim_id": "([^"]+)"', out)
                sims.append((m.group(1) if m else None, tpl, bi))
            except Exception as e:
                sims.append((None, tpl, bi))
                print(f"  [dispatch] {tpl}_{bi} error: {e}")
            pending.append(sims[-1][0])
            # 每批落一次断点：进程被杀时已派发的批次不会丢（否则重启会整集重派，
            # 2026-10-22 news_sentiment_dl 因此重复派发 216 条）
            if on_batch:
                try:
                    on_batch(list(sims))
                except Exception:
                    pass
    return sims


def harvest(sim_id, ds):
    """收割一个批次 → 返回 (rows, errors, state)

    rows : [(alpha_id, S, F, 2Y, sub)]
    errors: 子任务错误消息（用于分类）
    state: ok      = COMPLETE 且 rows 覆盖全部 children
           partial = COMPLETE 但有 children 没收到（平台限流/详情查询失败）→ 可重试补齐
           running = 还没跑完
           empty   = COMPLETE 且 children=0（结构性空批，等也没用）
           error   = 查询本身失败（429/网络）
    """
    cmd = [VENV_PY, os.path.join(ROOT, "cache", "_harvest_safe.py"), sim_id, ds, "camp"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout
    except Exception:
        # 四元组契约：调用方统一 `got, errs, state, nch = harvest(...)`
        return None, [], "error", None
    rows, errors = [], []
    for line in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=([-\d.]+)\s+F=([-\d.]+).*?2Y=([-\d.]+)\s+sub=([-\d.]+)", line)
        if m:
            rows.append((m.group(1), float(m.group(2)), float(m.group(3)),
                         float(m.group(4)), float(m.group(5))))
            continue
        me = re.match(r"\s*x\s+\S+\s+.*?msg=(.+)$", line)
        if me:
            errors.append(me.group(1).strip()[:100])

    # ⚠ 三类空结果必须区分（2026-10-22 实测）：
    #   ① running：/simulations/{id} 只返回 {"progress":0.35}，脚本打成 status=None children=0
    #   ② empty  ：status=COMPLETE 且 children=0（单条批）—— 再等也没用
    #   ③ partial：COMPLETE 且 children>0 但 rows 少 —— 平台对 alpha 详情端点限流，
    #              整批会被打成 0 行，若当成 running 会白等 4 分钟、若当成空批就永久丢结果
    md = re.search(r"status=(\w+) children=(\d+)", out)
    if not md:
        return rows or None, errors, "error", None
    st, nch = md.group(1), int(md.group(2))
    # ERROR/FAIL 是终态：整批表达式在平台侧跑不起来（如该数据集的字段/设置不兼容）。
    # 若当成 running 会白等 8×3min/批（2026-10-22 price_signal_dl 实测：22 批要耗 8 小时）。
    if st in ("ERROR", "FAIL"):
        return rows or None, errors, "fail", nch
    if st != "COMPLETE":
        return None, errors, "running", nch
    if nch == 0:
        return None, errors, "empty", 0
    if len(rows) < nch:
        return (rows or None), errors, "partial", nch
    return rows, errors, "ok", nch


PARTIAL_TRIES = 3     # partial（限流缺子任务）最多重试轮数，之后接受已收结果
WAIT_TRIES = 8        # running/error 最多等待轮数（约 8×3min）


def _harvest_until_done_impl(sim_id, ds, tag=""):
    """反复收割一批直到拿全子任务结果 → (rows, errs, state)。

    设计要点（2026-10-22 实测教训）：
    - partial 只重试 PARTIAL_TRIES 轮：若某个子任务本身没有 alpha，无限重试会拖死整轮；
    - 每轮结果按 alpha id 跨轮合并：partial 每轮缺的未必是同一条；
    - running/error 用 3 分钟退避，给平台排队时间。
    """
    rows, errs, state, nch = None, [], None, None
    part = waited = 0
    delay = 0
    while True:
        if delay:
            time.sleep(delay)
        got, errs, state, nch = harvest(sim_id, ds)
        if got:
            seen = {r[0] for r in (rows or [])}
            rows = list(rows or []) + [r for r in got if r[0] not in seen]
        if state in ("ok", "empty", "fail"):
            return rows, errs, state
        if state == "partial" and nch and len(rows or []) >= nch:
            return rows, errs, "ok"
        if state == "partial":
            part += 1
            if part >= PARTIAL_TRIES:
                return rows, errs, "partial"
            delay = 20
        else:
            waited += 1
            if waited >= WAIT_TRIES:
                return rows, errs, state
            delay = 180
        print(f"  [harvest] {tag} {state}（已收 {len(rows or [])}/{nch}）第 {part + waited} 次重试")


HARVEST_TIMEOUT = 900          # 单批收割墙钟上限（秒）


def harvest_until_done(sim_id, ds, tag=""):
    """带墙钟超时的收割外壳：超时返回 ([], [], "timeout")，调用方按空结果处理。"""
    import concurrent.futures as _cf
    ex = _cf.ThreadPoolExecutor(max_workers=1)
    fut = ex.submit(_harvest_until_done_impl, sim_id, ds, tag)
    try:
        return fut.result(timeout=HARVEST_TIMEOUT)
    except _cf.TimeoutError:
        print(f"  [harvest-timeout] {tag or sim_id} 超 {HARVEST_TIMEOUT}s，"
              f"放弃该批继续（不计入 DEAD）")
        return [], [], "timeout"
    except Exception as e:
        print(f"  [harvest-error] {tag or sim_id} {type(e).__name__}: {e}")
        return [], [], "error"
    finally:
        ex.shutdown(wait=False)
