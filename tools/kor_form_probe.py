# -*- coding: utf-8 -*-
"""kor_form_probe — 数据集「信号潜力」形态探针 v2（2026-10-26）。

与 `kor_year_probe.py` 的分工
------------------------------
`kor_year_probe` 回答 **数据可用性**：该数据集是否十年逐年有数据（PASS_10Y）。
表达式固定 `rank(ts_backfill(F,22))`，S 只是附带信息。

本脚本回答 **信号潜力**：在正确的形态骨架下，该集能不能出信号，且信号是否**形态稳健**。

为什么需要 v2（2026-10-26 实测教训）
------------------------------------
1. **单形态会系统性误判**：KOR Analyst 类 13 个已探集里 9 个裸 rank S 为负（最低 −0.70）。
   原因是 Analyst 字段多为修正量/比率，水平值均值回复 ⇒ `rank(level)` 测错方向。
2. **单一 max|S| 会被巧合骗**：`analyst11` 探针 S=0.63 排全类第一，但五种形态全部
   `CONCENTRATED_WEIGHT=1.0`（持仓坍缩单票，数据稀疏）⇒ 真实可用性为 0。
   ⇒ **必须同时记录 CW，并引入「形态广度」判据。**

七形态电池（每形态回答一个独立问题，避免漏信号）
------------------------------------------------
| 代号 | 形态 | 表达式 | 回答什么 |
|---|---|---|---|
| `L` | 水平 | `rank(ts_backfill(F,22))` | 绝对水平有无截面区分力 |
| `S` | 平滑水平 | `rank(ts_mean(ts_backfill(F,22),63))` | 去噪后的慢因子是否更强 |
| `C` | 季度变化 | `rank(ts_delta(ts_backfill(F,22),66))` | 季度修正的**方向** |
| `A` | 加速度 | `rank(ts_delta(ts_delta(ts_backfill(F,22),66),66))` | 修正的**二阶变化**（拐点） |
| `R` | 相对自身均值 | `rank(divide(ts_backfill(F,22), ts_mean(ts_backfill(F,22),252)))` | scale-free 比率 |
| `Z` | 年度 zscore | `rank(ts_zscore(ts_backfill(F,22),252))` | 相对自身历史的标准分 |
| `T` | 历史分位 | `rank(ts_rank(ts_backfill(F,22),252))` | 时间序列分位（抗异常值） |

判据（两级，缺一不可）
--------------------
- ``potential = max_forms |S|``      —— 有没有信号
- ``form_breadth = #{forms: |S| >= BREADTH_S}`` —— 信号是不是形态稳健
- ``STRONG``    : breadth >= 3（多形态同时成立 ⇒ 真信号，优先上结构）
- ``PROMISING`` : potential >= 0.8 但 breadth <= 2（单形态，警惕巧合，需复核）
- ``WEAK``      : potential < 0.8
- ``REJECT_SPARSE`` : 任一形态 CW=FAIL 且 potential < 0.8（数据稀疏）

★ 负 S 也要记录：平台要求 S 为正，负 S 只需把表达式取负即可，
  因此 ``potential`` 用 |S|，同时记 ``best_sign`` 供后续构造直接用。

两阶段（控成本）
----------------
- Stage A：1 个字段（coverage 最高）× 全部形态 × 全部数据集 —— 广度筛查
- Stage B：对 Stage A 中 ``potential >= 0.8`` 的数据集，换第 2 个字段（aCnt 最低）
  × 前 3 个形态 —— 深度确认（字段维度也要稳健）

断点续跑（仓库硬约定）
----------------------
`results/kor_form_probe.jsonl` 每完成一条原子追加（append + fsync）。
启动时载入已完成 ``(dataset, form, field)`` 三元组跳过；只把**拿到 alpha id** 的记完成。

用法::

    python tools/kor_form_probe.py --category Analyst --stage A
    python tools/kor_form_probe.py --category Analyst --stage B
    python tools/kor_form_probe.py --dataset analyst11 --forms L,C,Z
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))

CKPT = os.path.join(_ROOT, "results", "kor_form_probe.jsonl")
DS_CACHE = os.path.join(_ROOT, "results", "kor_datasets_cache.json")

#: 形态 → 表达式模板（``{F}`` 为字段，VECTOR 已在 wrap() 里包好 vec_avg）
FORMS: Dict[str, str] = {
    "L": "rank(ts_backfill({F},22))",
    "S": "rank(ts_mean(ts_backfill({F},22),63))",
    "C": "rank(ts_delta(ts_backfill({F},22),66))",
    "A": "rank(ts_delta(ts_delta(ts_backfill({F},22),66),66))",
    "R": "rank(divide(ts_backfill({F},22), ts_mean(ts_backfill({F},22),252)))",
    "Z": "rank(ts_zscore(ts_backfill({F},22),252))",
    "T": "rank(ts_rank(ts_backfill({F},22),252))",
}

FORM_NOTE = {
    "L": "水平量",
    "S": "平滑水平(63d)",
    "C": "季度变化(66d)",
    "A": "加速度(二阶变化)",
    "R": "相对自身年均值",
    "Z": "年度zscore(252d)",
    "T": "年度时序分位(252d)",
}

#: 判据阈值
STRONG_S = 0.8      # 单形态算「有信号」的门槛
BREADTH_S = 0.8     # 计入形态广度的门槛（同 STRONG_S，单独列出便于调）
STRONG_BREADTH = 3  # 广度达到多少算 STRONG
POTENTIAL_MIN = 0.8 # Stage B 入选门槛


def load_done() -> set:
    done = set()
    if not os.path.exists(CKPT):
        return done
    with open(CKPT, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("alpha_id"):
                done.add((r["dataset"], r["form"], r["field"]))
    return done


def load_records() -> Dict[Tuple[str, str, str], Dict[str, Any]]:
    latest: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    if not os.path.exists(CKPT):
        return latest
    with open(CKPT, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("alpha_id"):
                latest[(r["dataset"], r["form"], r["field"])] = r
    return latest


def append_record(rec: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CKPT), exist_ok=True)
    with open(CKPT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


#: 元数据/映射类字段的黑名单片段（2026-10-26 实测教训）
#: `analyst16` 的 max-coverage 字段是 `basedata_instrument_to_ticker_map` —— 纯证券代码
#: 映射表，无时间变化 ⇒ C/A/R/Z 四形态全部 S=0.0 / F=None（退化）。同类字段必须先剔除，
#: 否则「形态探针」实际在探一张映射表。
META_PATTERNS = (
    "basedata_", "instrument_to_ticker", "_to_ticker", "_ticker_map",
    "security_master", "_reference_data", "identifier", "sedol", "isin",
)

#: ★ 核心设计语义关键词（2026-10-26 新增硬规则）。
#:
#: 教训：`analyst10` 有 640 字段，其中 **90 个含 `innovation`**（aCnt 0–2）——
#: 厂商预计算的「相对正常水平的偏离（surprise）」，正是文献与论坛同时指向的正确形态。
#: 而按 max(coverage) 选字段选中了 `actual_update_flag_ebi`（一个 flag），
#: **把数据集的核心设计全漏了**。
#:
#: ⇒ 规则：选集后必须先扫字段名/description 的语义关键词，把「核心设计字段」优先纳入探针，
#:    **不能用 coverage / aCnt 代理**。覆盖率最高或最冷门的字段，往往都不是设计者想让你用的那个。
SEMANTIC_KEYWORDS = (
    "innovation", "surprise", "dispersion", "disagree", "revision",
    "drift", "momentum", "conviction", "breadth", "consensus",
)


def semantic_score(f: Dict[str, Any]) -> int:
    """核心设计字段打分：id / description 里命中多少个语义关键词。"""
    text = (str(f.get("id") or "") + " " + str(f.get("description") or "")).lower()
    return sum(1 for k in SEMANTIC_KEYWORDS if k in text)


def is_metadata_field(f: Dict[str, Any]) -> bool:
    """按 id + description 判断是否为元数据/映射类字段（无时变，不能当信号）。"""
    fid = str(f.get("id") or "").lower()
    desc = str(f.get("description") or "").lower()
    if any(p in fid for p in META_PATTERNS):
        return True
    meta_words = ("unique identifier", "mapping", "maps the", "identifier for",
                  "ticker symbol", "sedol", "isin code")
    return any(w in desc for w in meta_words)


def pick_fields(fields: List[Dict[str, Any]], order: str = "semantic",
                contains: Optional[str] = None) -> List[Dict[str, Any]]:
    """返回按优先级的字段列表。

    ``order='semantic'``（默认）：**核心设计语义关键词命中数优先**，其次 coverage
    ``order='cov'``：coverage 最高优先
    ``order='acnt'``：alphaCount 最低优先（找低拥挤）

    ``contains``：只保留 id 含该子串的字段（如 ``"innovation"``）。
    元数据/映射字段一律剔除；若全被剔除则原样返回，避免空集。

    ⚠ 默认用 semantic 而不是 cov：coverage 最高的往往是元数据或大类水平量，
    会漏掉厂商预计算的核心设计字段（`analyst10` 的 90 个 innovation 字段即例）。
    """
    if not fields:
        return []
    pool = [f for f in fields if not is_metadata_field(f)] or fields
    if contains:
        sub = [f for f in pool if contains.lower() in str(f.get("id") or "").lower()]
        # ★ 显式空集：指定了过滤词却零命中时必须报空，不能静默回退到全量字段
        # （否则调用方会以为在探 innovation 字段，实际在探全表任意字段）。
        if not sub:
            return []
        pool = sub
    if order == "acnt":
        return sorted(pool, key=lambda f: (f.get("alphaCount") or 10**9))
    if order == "cov":
        return sorted(pool, key=lambda f: -(f.get("coverage") or 0))
    # semantic（默认）
    return sorted(pool, key=lambda f: (-semantic_score(f), -(f.get("coverage") or 0)))


def wrap(field_id: str, ftype: Optional[str]) -> str:
    if str(ftype).upper() == "VECTOR":
        return f"vec_avg({field_id})"
    return field_id


async def probe_one(client, dataset: str, field: Dict[str, Any], form: str,
                    max_attempts: int = 5) -> Dict[str, Any]:
    from brain_api import SimulationData, SimulationSettings

    fid = field["id"]
    expr = FORMS[form].replace("{F}", wrap(fid, field.get("type")))
    st = SimulationSettings(
        region="KOR", universe="TOP600", delay=1, decay=4,
        neutralization="STATISTICAL", truncation=0.08,
        nanHandling="OFF", visualization=False,
    )
    rec: Dict[str, Any] = {
        "dataset": dataset, "field": fid, "field_type": field.get("type"),
        "field_cov": field.get("coverage"), "field_aCnt": field.get("alphaCount"),
        "form": form, "form_note": FORM_NOTE[form], "expr": expr,
    }

    # ★ 2026-10-26：429 退避重试。
    # 首轮 Stage A 有 99/101 条失败是 HTTP 429（create_simulation 限流），
    # 因为脚本没有退避就连续打。429 属**可重试**错误，绝不能记成失败记录
    # 污染 checkpoint；必须原地等待后重试同一条。
    last_err: Optional[str] = None
    for attempt in range(1, max_attempts + 1):
        try:
            a = await client.create_simulation(
                SimulationData(type="REGULAR", settings=st, regular=expr))
        except Exception as ex:  # noqa: BLE001
            msg = f"{type(ex).__name__}: {str(ex)[:160]}"
            last_err = msg
            limited = "429" in msg
            if limited and attempt < max_attempts:
                wait = min(60 * attempt, 300)
                print(f"    ↻ 429 限流，退避 {wait}s 后重试（{attempt}/{max_attempts}）",
                      flush=True)
                await asyncio.sleep(wait)
                continue
            rec.update({"alpha_id": None, "error": msg})
            return rec

        aid = a.get("id")
        if not aid:
            body = str(a)[:200]
            last_err = body
            if "429" in body and attempt < max_attempts:
                wait = min(60 * attempt, 300)
                print(f"    ↻ 429 限流(body)，退避 {wait}s 后重试（{attempt}/{max_attempts}）",
                      flush=True)
                await asyncio.sleep(wait)
                continue
            rec.update({"alpha_id": None, "error": body})
            return rec

        # 成功
        is_ = a.get("is") or {}
        m = is_.get("metrics") or is_
        checks = {c.get("name"): c for c in (is_.get("checks") or [])}

        def cv(name):
            return (checks.get(name) or {}).get("value")

        try:
            sharpe = float(m.get("sharpe")) if m.get("sharpe") is not None else None
        except (TypeError, ValueError):
            sharpe = None

        rec.update({
            "alpha_id": aid,
            "sharpe": sharpe,
            "sign": (1 if (sharpe or 0) > 0 else (-1 if (sharpe or 0) < 0 else 0)),
            "fitness": m.get("fitness"),
            "turnover": m.get("turnover"),
            "two_year": cv("LOW_2Y_SHARPE"),
            "sub_universe": cv("LOW_SUB_UNIVERSE_SHARPE"),
            "concentrated_weight": (checks.get("CONCENTRATED_WEIGHT") or {}).get("result"),
            "drawdown": m.get("drawdown"),
            "attempts": attempt,
        })
        return rec

    rec.update({"alpha_id": None, "error": f"retries_exhausted: {last_err}"})
    return rec


def is_degenerate(r: Dict[str, Any]) -> bool:
    """判定退化结果：S 恰为 0 且 fitness 为空。

    实测样本：`analyst16` 的元数据字段 `basedata_instrument_to_ticker_map` 在
    C/A/R/Z 四形态下全部 S=0.0 / F=None —— 字段无时间变化 ⇒ 信号恒为常数，
    此类结果不构成「无信号」的证据，只是字段不可用，必须排除在形态广度之外。
    """
    s = r.get("sharpe")
    if s is None:
        return True
    return abs(float(s)) < 1e-9 and r.get("fitness") is None


def build_regular_payload(settings, expr: str) -> Dict[str, Any]:
    """构造 REGULAR 仿真的 POST /simulations 载荷。

    ★ 必须与 `brain_mixin_simulation.create_simulation` 内部逻辑**完全一致**，
    否则平台会报 `lookback may not be null` / `selectionHandling ...`：
    1. `model_dump()` 后 **pop 掉 SUPER 专用字段**（selectionHandling/selectionLimit/componentActivation）
    2. **过滤掉所有 None 值**
    2026-10-26 踩坑：手搓 payload 时漏了这两步，并行派发 7 条全部 400。
    """
    sd = settings.model_dump() if hasattr(settings, "model_dump") else settings.dict()
    for k in ("selectionHandling", "selectionLimit", "componentActivation"):
        sd.pop(k, None)
    sd = {k: v for k, v in sd.items() if v is not None}
    payload = {"type": "REGULAR", "settings": sd, "regular": expr}
    return {k: v for k, v in payload.items() if v is not None}


async def run_parallel(client, plan, args, done) -> None:
    """并行模式：批量派发 + 统一轮询（2026-10-26 新增）。

    为什么需要：`E1`/`analyst10` 这类稀疏数据集单条仿真要 **25–30 分钟**（平台端
    `progress` 长期停在 0.35 是粗粒度读数，不是卡死）。串行「派发→阻塞等待」下
    7 形态要 3.5 小时；批量派发后统一轮询，总时长≈单条时长（~30–40 分钟）。

    ⚠ 这只是**吞吐**问题，与「进程是否脱离 Agent 的 Job 对象」无关 ——
    本地进程全程存活（实测跨数小时、checkpoint 正常增长），瓶颈在平台端算力。
    """
    from brain_api import SimulationData, SimulationSettings

    # 1) 构建 payload
    payloads: List[Dict[str, Any]] = []
    meta: List[Tuple[str, str, Dict[str, Any]]] = []
    for ds, form, order in plan:
        resp = await client.get_datafields(
            region="KOR", universe="TOP600", delay=1,
            dataset_id=ds, filter_sharpe=False)
        fields = resp.get("results") or []
        if not fields:
            continue
        ordered = pick_fields(fields, order=order, contains=args.field_filter)
        field = None
        for cand in ordered:
            if (ds, form, cand["id"]) not in done:
                field = cand
                break
        if field is None:
            if not ordered:
                print(f"[parallel] {ds:22s} NO_FIELD_MATCH filter={args.field_filter!r}",
                      flush=True)
            continue
        expr = FORMS[form].replace("{F}", wrap(field["id"], field.get("type")))
        st = SimulationSettings(
            region="KOR", universe="TOP600", delay=1, decay=4,
            neutralization="STATISTICAL", truncation=0.08,
            nanHandling="OFF", visualization=False)
        payloads.append(build_regular_payload(st, expr))
        meta.append((ds, form, field))
        await asyncio.sleep(0.4)

    if not payloads:
        print("[parallel] 无可派发条目", flush=True)
        return

    print(f"[parallel] 批量派发 {len(payloads)} 条…", flush=True)
    sub = await client.batch_create_simulations(payloads)
    print(f"[parallel] 派发结果 {sub.get('submitted')}/{sub.get('total')}", flush=True)

    # 2) 构建 index → simulation_id；被并发上限拒绝的进重试队列
    idx2sim: Dict[int, str] = {}
    retry_queue: List[int] = []
    for r in (sub.get("results") or []):
        i = int(r.get("index") or -1)
        if r.get("ok") and r.get("simulation_id"):
            idx2sim[i] = r["simulation_id"]
        elif 0 <= i < len(meta):
            err = str(r.get("error") or "")
            # ★ CONCURRENT_SIMULATION_LIMIT_EXCEEDED：账号并发上限（实测 ~4 条）。
            # 这不是失败，是「排队」——必须等有槽位再派，不能反复重试（会继续 429）。
            if "CONCURRENT_SIMULATION_LIMIT" in err or "429" in err:
                retry_queue.append(i)
                print(f"[parallel] {meta[i][0]:20s} {meta[i][1]} 排队（并发上限）", flush=True)
            else:
                print(f"[parallel] {meta[i][0]:20s} {meta[i][1]} 派发失败: {err[:90]}",
                      flush=True)

    # 3) 统一轮询
    pending = dict(idx2sim)
    deadline = asyncio.get_event_loop().time() + args.timeout
    rounds = 0
    while (pending or retry_queue) and asyncio.get_event_loop().time() < deadline:
        rounds += 1
        for i in list(pending.keys()):
            sid = pending[i]
            ds, form, field = meta[i]
            try:
                j = (await client._request("GET", f"/simulations/{sid}")).json()
            except Exception as ex:  # noqa: BLE001
                print(f"[parallel] {ds:20s} {form} 轮询异常 {type(ex).__name__}", flush=True)
                continue
            status = str(j.get("status") or "").upper()
            if status not in ("COMPLETE", "ERROR", "FAIL", "WARNING"):
                continue
            aid = j.get("alpha")
            rec = {
                "dataset": ds, "field": field["id"], "field_type": field.get("type"),
                "field_cov": field.get("coverage"), "field_aCnt": field.get("alphaCount"),
                "form": form, "form_note": FORM_NOTE[form],
                "alpha_id": aid,
            }
            if aid:
                try:
                    a = (await client._request("GET", f"/alphas/{aid}")).json()
                    is_ = a.get("is") or {}
                    m = is_.get("metrics") or is_
                    checks = {c.get("name"): c for c in (is_.get("checks") or [])}
                    try:
                        sh = float(m.get("sharpe")) if m.get("sharpe") is not None else None
                    except (TypeError, ValueError):
                        sh = None
                    rec.update({
                        "sharpe": sh,
                        "sign": 1 if (sh or 0) > 0 else (-1 if (sh or 0) < 0 else 0),
                        "fitness": m.get("fitness"),
                        "turnover": m.get("turnover"),
                        "two_year": (checks.get("LOW_2Y_SHARPE") or {}).get("value"),
                        "sub_universe": (checks.get("LOW_SUB_UNIVERSE_SHARPE") or {}).get("value"),
                        "concentrated_weight": (checks.get("CONCENTRATED_WEIGHT") or {}).get("result"),
                        "drawdown": m.get("drawdown"),
                    })
                except Exception as ex:  # noqa: BLE001
                    rec["error"] = f"alpha_fetch: {type(ex).__name__}"
            else:
                rec["error"] = f"sim status={status} 无 alpha"
            append_record(rec)
            if rec.get("alpha_id"):
                done.add((ds, form, field["id"]))
                print(f"{ds:20s} {form} {field['id'][:30]:30s} {rec['alpha_id']} "
                      f"S={rec.get('sharpe')} F={rec.get('fitness')} "
                      f"2Y={rec.get('two_year')} CW={rec.get('concentrated_weight')}",
                      flush=True)
            else:
                print(f"{ds:20s} {form} {field['id'][:30]:30s} {rec.get('error')}", flush=True)
            pending.pop(i, None)
        # 有空槽就补派排队中的条目（槽位感知，避免反复撞 CONCURRENT_SIMULATION_LIMIT）
        while retry_queue and len(pending) < args.max_concurrent:
            k = retry_queue.pop(0)
            ds, form, field = meta[k]
            expr = FORMS[form].replace("{F}", wrap(field["id"], field.get("type")))
            p = build_regular_payload(
                SimulationSettings(
                    region="KOR", universe="TOP600", delay=1, decay=4,
                    neutralization="STATISTICAL", truncation=0.08,
                    nanHandling="OFF", visualization=False),
                expr)
            try:
                resp = await client._request("POST", f"{client.base_url}/simulations", json=p)
                loc = resp.headers.get("Location", "")
                sid = loc.rstrip("/").split("/")[-1] if loc else None
                if resp.status_code < 400 and sid:
                    pending[k] = sid
                    print(f"[parallel] {ds:20s} {form} 补派成功 {sid}", flush=True)
                else:
                    retry_queue.append(k)
                    break
            except Exception:  # noqa: BLE001
                retry_queue.append(k)
                break
            await asyncio.sleep(1.0)
        # ★ 必须无条件 sleep：若只在 `pending` 非空时睡，则「pending 空 + retry_queue 非空」
        # 会进入无 sleep 的紧循环（实测几秒内空转 380 轮，并持续打平台接口）。
        if pending or retry_queue:
            print(f"[parallel] 轮询第 {rounds} 轮，剩余 {len(pending)} 条"
                  f"（排队 {len(retry_queue)}）", flush=True)
            await asyncio.sleep(args.poll)

    if pending or retry_queue:
        print(f"[parallel] 超时，仍有 {len(pending)} 条在飞、{len(retry_queue)} 条排队"
              f"（可重跑续上）", flush=True)


def aggregate(latest: Dict[Tuple[str, str, str], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """按 **字段** 汇总形态剖面，再按数据集取最优字段。

    ★ 2026-10-26 修正（方法论缺陷）：形态比较必须在**同一字段**内进行。
    初版按 dataset 汇总，导致不同字段的 S 被放在同一条「形态序列」里比，
    把「形态效应」与「字段效应」混为一谈（analyst11 的 L 在两次运行间
    从 0.63 变 0.22，仅仅因为换了字段）。

    现在分两层：
    1. ``by_field[(dataset, field)]`` → 该字段的 power/breadth
    2. 数据集层取 power 最高的字段作为代表，但**同时报告有几成字段也达标**
       （``field_breadth``）—— 字段维度也要稳健。
    """
    # 第 1 层：按 (dataset, field) 分组
    by_field: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for (_ds, _form, _f), r in latest.items():
        # 元数据字段的历史记录直接忽略（修复前采集的，探的是映射表不是信号）
        if is_metadata_field({"id": r.get("field"), "description": r.get("field_desc")}):
            continue
        by_field.setdefault((r["dataset"], r["field"]), []).append(r)

    field_stats: List[Dict[str, Any]] = []
    for (ds, fid), rs in by_field.items():
        scored = [r for r in rs if isinstance(r.get("sharpe"), (int, float))]
        if not scored:
            continue
        usable = [r for r in scored if r.get("concentrated_weight") != "FAIL"
                  and not is_degenerate(r)]
        if not usable:
            continue
        best = max(usable, key=lambda r: abs(r["sharpe"]))
        field_stats.append({
            "dataset": ds, "field": fid,
            "potential": abs(best["sharpe"]),
            "form_breadth": sum(1 for r in usable if abs(r["sharpe"]) >= BREADTH_S),
            "best_form": best["form"], "best_sign": best.get("sign"),
            "best_s": best["sharpe"], "best_2y": best.get("two_year"),
            "n_forms": len(scored), "n_usable": len(usable),
            "forms": {r["form"]: r.get("sharpe") for r in scored},
            "usable_forms": [r["form"] for r in usable],
        })

    # 第 2 层：按数据集取最优字段
    by_ds: Dict[str, List[Dict[str, Any]]] = {}
    for st in field_stats:
        by_ds.setdefault(st["dataset"], []).append(st)

    out: List[Dict[str, Any]] = []
    for ds, sts in by_ds.items():
        best = max(sts, key=lambda s: (s["form_breadth"], s["potential"]))
        # 字段广度：有多少个字段的 potential 也 >= 门槛
        field_breadth = sum(1 for s in sts if s["potential"] >= BREADTH_S)
        if best["form_breadth"] >= STRONG_BREADTH:
            verdict = "STRONG"
        elif best["potential"] >= STRONG_S:
            verdict = "PROMISING"
        else:
            verdict = "WEAK"
        # 全字段全形态 CW 都失败 ⇒ 稀疏
        all_fail = all(r.get("concentrated_weight") == "FAIL"
                       for s in sts for r in
                       [x for x in by_field[(ds, s["field"])]
                        if isinstance(x.get("sharpe"), (int, float))])
        if all_fail:
            verdict = "REJECT_SPARSE"
        out.append({
            "dataset": ds,
            "potential": best["potential"],
            "form_breadth": best["form_breadth"],
            "field_breadth": field_breadth,
            "n_fields": len(sts),
            "best_field": best["field"],
            "best_form": best["best_form"],
            "best_sign": best["best_sign"],
            "best_s": best["best_s"],
            "best_2y": best["best_2y"],
            "verdict": verdict,
            "forms": best["forms"],          # 代表字段的形态剖面
            "usable_forms": best["usable_forms"],
        })
    return sorted(out, key=lambda x: (-x["form_breadth"], -x["potential"]))


async def run(args) -> None:
    from brain_api import BrainApiClient

    client = BrainApiClient()
    await client.ensure_authenticated()

    # 1) 数据集清单
    if args.dataset:
        datasets = [args.dataset]
    else:
        with open(DS_CACHE, encoding="utf-8") as f:
            all_ds = json.load(f)

        def cat(d):
            c = d.get("category")
            return c.get("name") if isinstance(c, dict) else c

        datasets = [d["id"] for d in all_ds if cat(d) == args.category]
        print(f"[form-probe] 类别 {args.category} 共 {len(datasets)} 个数据集", flush=True)

    forms = [x.strip().upper() for x in args.forms.split(",") if x.strip()]
    bad = [f for f in forms if f not in FORMS]
    if bad:
        raise SystemExit(f"未知形态 {bad}，可用 {list(FORMS)}")

    latest = load_records()
    done = load_done()

    # Stage B：只对 Stage A 表现好的集，换低拥挤字段 × 胜出形态
    if args.stage == "B":
        agg = aggregate(latest)
        chosen = [a for a in agg if a["potential"] >= POTENTIAL_MIN and a["dataset"] in datasets]
        if not chosen:
            print("[form-probe] Stage B：无潜力达标的集，跳过", flush=True)
            return
        print(f"[form-probe] Stage B 入选 {len(chosen)} 集："
              f"{[a['dataset'] for a in chosen]}", flush=True)
        plan: List[Tuple[str, str, str]] = []  # (dataset, form, field_order)
        for a in chosen:
            top = sorted(((f, abs(s)) for f, s in (a.get("forms") or {}).items()
                          if isinstance(s, (int, float))), key=lambda x: -x[1])[:3]
            for f, _ in top:
                plan.append((a["dataset"], f, "acnt"))
    else:
        # ★ Stage A 默认 semantic（核心设计关键词优先），不再用 cov。
        # 教训：按 coverage 选会漏掉 analyst10 的 90 个 innovation 字段（aCnt 0–2）。
        plan = [(ds, f, args.field_order) for ds in datasets for f in forms]

    print(f"[form-probe] stage={args.stage} 计划 {len(plan)} 条"
          f"（已完成 {len(done)} 条，自动跳过）"
          f" field_order={plan[0][2] if plan else '-'}"
          f" filter={args.field_filter or '-'}"
          f" parallel={args.parallel}", flush=True)

    # ★ 并行模式：批量派发 + 统一轮询。稀疏数据集（analyst10/analyst11 等）
    # 单条要 25–30 分钟，串行 7 形态 = 3.5 小时；并行后总时长≈单条时长。
    if args.parallel:
        await run_parallel(client, plan, args, done)
        agg = aggregate(load_records())
        print("\n=== 信号潜力 / 形态广度 汇总 ===")
        for a in agg:
            fs = ",".join(f"{k}:{round(v, 2)}" for k, v in
                          sorted((a.get("forms") or {}).items())
                          if isinstance(v, (int, float)))
            print(f"{a['dataset']:20s} pot={a['potential']:.2f} brd={a['form_breadth']} "
                  f"fld={a.get('field_breadth')} {a['verdict']:>10s} "
                  f"best={a.get('best_form')} sign={a.get('best_sign')} | {fs}")
        return

    for i, (ds, form, order) in enumerate(plan, 1):
        resp = await client.get_datafields(
            region="KOR", universe="TOP600", delay=1,
            dataset_id=ds, filter_sharpe=False)
        fields = resp.get("results") or []
        if not fields:
            print(f"[{i}/{len(plan)}] {ds:24s} REJECT_NO_FIELDS", flush=True)
            continue
        ordered = pick_fields(fields, order=order, contains=args.field_filter)
        field = None
        for cand in ordered:
            if (ds, form, cand["id"]) not in done:
                field = cand
                break
        if field is None:
            # 过滤词零命中（ordered 为空）时明确报出，避免「跑完了但什么都没查」的静默失败
            if not ordered:
                print(f"[{i}/{len(plan)}] {ds:24s} NO_FIELD_MATCH "
                      f"filter={args.field_filter!r}", flush=True)
            continue
        key = (ds, form, field["id"])
        if key in done:
            continue

        rec = await probe_one(client, ds, field, form)
        if rec.get("alpha_id"):
            append_record(rec)
            done.add(key)
            latest[key] = rec
            print(f"[{i}/{len(plan)}] {ds:22s} {form} {field['id'][:32]:32s} "
                  f"{rec['alpha_id']} S={rec.get('sharpe')} F={rec.get('fitness')} "
                  f"2Y={rec.get('two_year')} CW={rec.get('concentrated_weight')}", flush=True)
            # 轻微间隔，降低 429 概率（首轮 99/101 失败即因无间隔连续打）
            await asyncio.sleep(args.pace)
        else:
            # 失败不写主 checkpoint（否则 124 行里 101 行是噪声），另记错误日志
            err_path = CKPT.replace(".jsonl", "_errors.jsonl")
            with open(err_path, "a", encoding="utf-8") as ef:
                ef.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"[{i}/{len(plan)}] {ds:22s} {form} {field['id'][:32]:32s} "
                  f"FAIL {str(rec.get('error'))[:80]}", flush=True)

    # 2) 汇总
    agg = aggregate(load_records())
    print("\n=== 信号潜力 / 形态广度 汇总 ===")
    print(f"{'dataset':24s} {'pot':>5s} {'brd':>4s} {'verdict':>14s} "
          f"{'best':>5s} {'sign':>5s} {'field':32s} forms")
    for a in agg:
        fs = ",".join(f"{k}:{round(v,2)}" for k, v in sorted((a.get('forms') or {}).items())
                      if isinstance(v, (int, float)))
        print(f"{a['dataset']:24s} {a['potential']:5.2f} {a['form_breadth']:4d} "
              f"{a['verdict']:>14s} {str(a.get('best_form') or '-'):>5s} "
              f"{str(a.get('best_sign') or '-'):>5s} "
              f"{str(a.get('best_field') or '-')[:32]:32s} {fs}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", default="Analyst", help="数据集类别")
    ap.add_argument("--dataset", help="只跑单个数据集")
    ap.add_argument("--stage", default="A", choices=["A", "B"], help="A=广度 B=深度")
    ap.add_argument("--forms", default="L,S,C,A,R,Z,T", help="形态子集，逗号分隔")
    ap.add_argument("--pace", type=float, default=4.0,
                    help="每条成功仿真后的间隔秒数，防 429（默认 4s）")
    ap.add_argument("--field-order", default="semantic",
                    choices=["semantic", "cov", "acnt"],
                    help="字段优先级：semantic=核心设计关键词(默认) / cov=覆盖率 / acnt=低拥挤")
    ap.add_argument("--field-filter", default=None,
                    help="只探 id 含该子串的字段（如 innovation）")
    ap.add_argument("--parallel", action="store_true",
                    help="批量派发 + 统一轮询（稀疏数据集建议开，7 条约 30 分钟而非 3.5 小时）")
    ap.add_argument("--poll", type=float, default=30.0, help="并行模式轮询间隔秒数")
    ap.add_argument("--timeout", type=float, default=5400.0, help="并行模式总超时秒数")
    ap.add_argument("--max-concurrent", type=int, default=4,
                    help="同时最多在飞的仿真数（平台账号并发上限，实测约 4）")
    args = ap.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
