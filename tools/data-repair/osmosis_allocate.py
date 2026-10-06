# -*- coding: utf-8 -*-
"""osmosis_allocate.py — WorldQuant BRAIN Osmosis points 分配工具（单文件、正式）。

背景与机制（2026-10-06 定案，纠正此前"Osmosis 非标准术语"误判）
  Osmosis 是 2026-02 全球会议新模块：把总预算 **100,000 点** 分配到各「范围」
  (scope = region + delay 组合)。规则：
    - 每范围 **≥10 个** alpha 才计入该范围；
    - 整体须覆盖 **≥3 个范围** 才达 eligibility（否则平台提醒
      "did not meet eligibility criteria"，不计 Daily Osmosis Rank）；
    - 点数是**置信权重**（"Osmosis 本质是 Alpha 组合配置，点数是权重，只改变暴露
      不创造信号质量"），按范围组合平均回报排名 → 作 ×每日奖金乘数 + 纳入季度 Genius 等级；
    - 时效：每周日 23:59 EST 采样 → 周三展示 → 7 天滞后影响 Daily Osmosis Rank；点数周内不过期。
    - **SuperAlpha 不可分配**（论坛实锤 "Cannot update Osmosis points for Super Alpha"）；
      本工具只碰 REGULAR（含 untyped）alpha。

硬约束（首轮实测踩坑，已内置）
  平台 PATCH `osmosisPoints` 只接受 **active 且 compensated（在奖金池）** 的 alpha；
  本地 `platform_status='ACTIVE'` ≠ 平台 compensated。返回：
    - `Cannot update Osmosis points for inactive alpha.`            (8 颗)
    - `Cannot update Osmosis points for non-compensated alpha.`     (17 颗)
  首轮 116 OK / 25 FAIL，经手动 replan（弃 EUR D1 + 丢弃失败颗，剩余 6 范围 rescale
  到 100k）重跑得 111 OK / 0 FAIL。本工具把这套「apply → 失败 → 自动 replan → 重 apply」
  闭环内置为单次命令，无需手工拼装。

落点合规
  本文件落在 `tools/data-repair/`（S11「tools 顶层只减不增」；新增单文件工具须进此子目录）。
  读库走规范工厂 `wqb.db_conn.connect(readonly=True)`（**不得裸 `sqlite3.connect`**）。
  ⚠ 2026-10-06 修正本段原注释：它写的是「与同目录 `backfill_alpha_metrics_from_platform.py`
  同约定（raw sqlite3）」——那个前提不成立。守卫
  `tests/unit/01_store_db/test_db_write_guards.py::test_no_naked_connect_outside_whitelist`
  的豁免按**文件名前缀**（`backfill_`/`migrate_`/`triage_`/`fix_`/`_db_` …）而非目录，
  `backfill_*` 因名字免检，`osmosis_*` 不沾 ⇒ 同目录不等于同豁免。
  写平台走 MCP venv 的 `brain_api.brain_client`（与 `sync_platform_alphas.py` 同约定）。

用法
  python tools/data-repair/osmosis_allocate.py                 # review：读范围覆盖 + 写 plan（不写平台）
  python tools/data-repair/osmosis_allocate.py --sync          # review 前先拉平台 OS 指标改善权重
  python tools/data-repair/osmosis_allocate.py --region USA    # 只针对某区（范围覆盖统计仍全量）
  python tools/data-repair/osmosis_allocate.py --apply         # ★ 写入平台（PATCH osmosisPoints，带断点续跑 + 自动 replan）
  python tools/data-repair/osmosis_allocate.py --apply --dry-run   # 预览 PATCH（不真正写）
  python tools/data-repair/osmosis_allocate.py --apply --max-replan 3  # 限制 replan 轮数
  python tools/data-repair/osmosis_allocate.py --prod-policy exclude    # 严格：剔除 prod>=阈值 的 alpha（含恰好 0.70；含本地 prod 为 None 的保守剔除；可能令某范围掉到 <10 失格）
  python tools/data-repair/osmosis_allocate.py --prod-policy ignore     # 旧行为：不纳 prod
  # prod 策略默认 discount：对 prod∈(阈值,1] 的质量递减打折（保留范围资格，仅挪权重）；阈值默认 0.70（与提交闸一致）

注意：写平台属"改属性"非"提交 alpha"，受"只挖不提交"策略允许；但会改动平台状态，
  须显式 --apply 且用户确认。默认（无 --apply）只读 + 写本地 plan。
  --apply 采用「替换式分配」：先 PATCH 计划内 alpha 的新点数，再 PATCH 所有候选池内
  但不在计划的 alpha 为 0（平台拒 0 时回退最小值 1），以清除上一轮残留分配。
退出码: 0=正常  3=DB/平台失败  4=eligibility 不足且无法收敛
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# --- 路径：向上探双标记，**与文件所在层数无关**（AGENTS.md §8.13 禁新增层数硬编码）----
# 原写法是 dirname 连剥三层（data-repair -> tools -> 根），本文件再下沉一层就会静默
# 指错仓库根（DB / results / plan 路径全错）。改为与 `wqb.paths.find_repo_root` 同口径的探测。
_THIS = os.path.abspath(__file__)
_REPO_ROOT = None
for _p in Path(_THIS).resolve().parents:
    if (_p / "pyproject.toml").exists() and (_p / "src" / "wqb").is_dir():
        _REPO_ROOT = str(_p)
        break
if _REPO_ROOT is None:
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")
_TOOLS = os.path.dirname(_THIS)              # .../tools/data-repair
for _p in (_TOOLS, os.path.dirname(_TOOLS), _REPO_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# apply 阶段需要 brain_api（在 world-quant-brain-mcp）；与 sync_platform_alphas 同约定
MCP_DIR = os.path.join(_REPO_ROOT, "world-quant-brain-mcp")
for _p in (MCP_DIR, os.path.join(_REPO_ROOT, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

DB = os.path.join(_REPO_ROOT, "data", "wqb.db")
RESULTS = os.path.join(_REPO_ROOT, "results")
PLAN_PATH = os.path.join(RESULTS, "osmosis_plan.json")
CKPT_PATH = os.path.join(RESULTS, "osmosis_applied.json")

TOTAL_BUDGET = 100_000
SCOPE_FLOOR = 0.08            # 每范围保底占比（确保 ≥3 范围都有意义暴露）
MIN_PER_SCOPE = 10           # 平台每范围最低 alpha 数
MIN_SCOPES = 3               # 平台 eligibility 最低范围数
MIN_PTS = 1
MAX_PTS = 100_000

# prod 相关性策略（与本项目提交闸 prod<0.7 一致）：
#   discount = 对 prod∈(PROD_MAX,1] 的质量递减打折（保留范围资格，仅挪权重）
#   exclude  = 剔除 prod>=PROD_MAX 的 alpha（含恰好阈值；含本地 prod 为 None 的保守剔除；可能令某范围掉到 <10 而失格）
#   ignore   = 不纳 prod（旧行为）
PROD_POLICY = "discount"
PROD_MAX = 0.70
PROD_PENALTY_FLOOR = 0.05    # prod=1.0 时质量保留的最低比例


# --------------------------------------------------------------------------- #
# venv reexec（必须在 import brain_api 之前）
# --------------------------------------------------------------------------- #
try:
    import _pyenv  # type: ignore
    _pyenv.reexec_under_venv()
except Exception:
    pass


# --------------------------------------------------------------------------- #
# DB 读：范围覆盖（只读；必须走 `wqb.db_conn` 规范工厂，禁裸 sqlite3.connect）
# --------------------------------------------------------------------------- #
def load_candidates(region: Optional[str] = None) -> List[Dict[str, Any]]:
    """读取 ACTIVE REGULAR/untyped alpha（SuperAlpha 排除）。返回行列表。"""
    if not os.path.exists(DB):
        raise FileNotFoundError(f"DB 不存在: {DB}")
    # 惰性导入：本文件顶部先做 venv reexec，不能在那之前依赖 src 包。
    # 工厂自带 WAL / busy_timeout=60s / foreign_keys 口径；`readonly=True` 以 mode=ro
    # 打开并**跳过 PRAGMA journal_mode=WAL**（WAL 是库级持久属性，即使不写行也会改库文件字节）。
    from wqb.db_conn import connect as _db_connect
    con = _db_connect(readonly=True, row_factory=sqlite3.Row)
    sql = (
        "SELECT a.alpha_id, r.name AS region, a.delay, a.sharpe, a.os_sharpe, "
        "a.fitness, a.turnover, a.margin, a.two_year_sharpe, a.stage, "
        "a.platform_status, a.alpha_type, "
        "a.prod_correlation AS prod_a, c.prod_correlation AS prod_cache "
        "FROM alphas a JOIN regions r ON a.region_id = r.id "
        "LEFT JOIN alpha_corr_cache c ON c.alpha_id = a.alpha_id "
        "WHERE a.platform_status='ACTIVE' "
        "AND (a.alpha_type='REGULAR' OR a.alpha_type IS NULL)"
    )
    params: List[Any] = []
    if region:
        sql += " AND r.name=?"
        params.append(region)
    rows = []
    for r in con.execute(sql, params).fetchall():
        d = dict(r)
        # 权威优先缓存（与 search_alphas_by_sharpe.merge_corr_cache 同口径）
        d["prod"] = d["prod_cache"] if d.get("prod_cache") is not None else d.get("prod_a")
        rows.append(d)
    con.close()
    return rows


def build_scopes(rows: List[Dict[str, Any]]) -> Dict[Tuple[str, int], List[Dict[str, Any]]]:
    scopes: Dict[Tuple[str, int], List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        d = r["delay"] if r["delay"] is not None else -1
        scopes[(r["region"], d)].append(r)
    return scopes


def prod_penalty(prod: Optional[float], policy: str, prod_max: float) -> float:
    """prod 折扣因子：ignore/NULL/≤阈值 → 1.0；exclude 且 >阈值 → 0.0；
    discount：prod∈(阈值,1] 线性递减到 PROD_PENALTY_FLOOR。"""
    if policy == "ignore" or prod is None or prod <= prod_max:
        return 1.0
    if policy == "exclude":
        return 0.0
    t = min(1.0, (prod - prod_max) / (1.0 - prod_max))
    return max(PROD_PENALTY_FLOOR, 1.0 - t * (1.0 - PROD_PENALTY_FLOOR))


def quality(a: Dict[str, Any]) -> float:
    """质量 = 优先 OS、缺失回退 IS、超低频换手打 0.6 折，再乘 prod 折扣。"""
    v = a["os_sharpe"] if a["os_sharpe"] is not None else a["sharpe"]
    if v is None:
        return 0.0
    to = a["turnover"] or 0
    pen = 0.6 if to < 0.05 else 1.0
    q = max(float(v), 0.0) * pen
    return q * prod_penalty(a.get("prod"), PROD_POLICY, PROD_MAX)


# --------------------------------------------------------------------------- #
# 计划生成（质量比例 + 范围保底 + rescale 到预算）
# --------------------------------------------------------------------------- #
def build_plan(scopes: Dict[Tuple[str, int], List[Dict[str, Any]]],
               eligible_only: bool = True) -> List[Dict[str, Any]]:
    """按质量比例分配 TOTAL_BUDGET 到点。

    eligible_only=True 时只在 (n>=10) 的范围里分配；若达标范围 <3，退化为取质量最高的
    前 3 个范围（平台仍不计数，但至少把点数设上去，便于用户后续补到 ≥3）。
    """
    scope_stats = []
    for (reg, d), al in scopes.items():
        os_vals = [a["os_sharpe"] for a in al if a["os_sharpe"] is not None]
        is_vals = [a["sharpe"] for a in al if a["sharpe"] is not None]
        scope_stats.append({
            "region": reg, "delay": d, "n": len(al),
            "n_os": len(os_vals),
            "avg_os": (sum(os_vals) / len(os_vals)) if os_vals else None,
            "avg_is": (sum(is_vals) / len(is_vals)) if is_vals else None,
        })

    eligible = [s for s in scope_stats if s["n"] >= MIN_PER_SCOPE]
    eligible.sort(key=lambda s: (s["avg_os"] if s["avg_os"] is not None else (s["avg_is"] or 0)),
                  reverse=True)
    if len(eligible) >= MIN_SCOPES:
        cand = eligible
        met = True
    else:
        # 退化：取质量最高的前 3 范围，标记未达标
        scope_stats.sort(key=lambda s: (s["n"] >= MIN_PER_SCOPE,
                                         s["avg_os"] if s["avg_os"] is not None else (s["avg_is"] or 0)),
                          reverse=True)
        cand = scope_stats[:MIN_SCOPES]
        met = False

    # 范围预算 = 范围内质量之和，带保底，再归一
    scope_q: Dict[Tuple[str, int], float] = {}
    for s in cand:
        key = (s["region"], s["delay"])
        scope_q[key] = sum(quality(a) for a in scopes[key]) or 0.0
    tot_q = sum(scope_q.values()) or 1.0
    budgets = {k: max(SCOPE_FLOOR, v / tot_q) for k, v in scope_q.items()}
    sf = sum(budgets.values()) or 1.0
    budgets = {k: v / sf for k, v in budgets.items()}

    plan: List[Dict[str, Any]] = []
    for s in cand:
        key = (s["region"], s["delay"])
        al = sorted(scopes[key], key=quality, reverse=True)
        scope_budget = TOTAL_BUDGET * budgets[key]
        sq = sum(quality(a) for a in al) or 1.0
        for a in al:
            pts = int(round(scope_budget * quality(a) / sq))
            pts = max(MIN_PTS, min(MAX_PTS, pts))
            plan.append({"region": key[0], "delay": key[1],
                         "alpha_id": a["alpha_id"], "points": pts,
                         "prod": a.get("prod")})
    _trim_to_budget(plan)
    return plan


def _trim_to_budget(plan: List[Dict[str, Any]]) -> None:
    """总点数若因 MIN_PTS 钳制超出预算，从最大分配项扣回，保证总和 == TOTAL_BUDGET。"""
    total = sum(e["points"] for e in plan)
    if total <= TOTAL_BUDGET:
        return
    excess = total - TOTAL_BUDGET
    # 从大到小扣，单项不低于 MIN_PTS
    for e in sorted(plan, key=lambda x: -x["points"]):
        if excess <= 0:
            break
        reducible = e["points"] - MIN_PTS
        if reducible <= 0:
            continue
        cut = min(reducible, excess)
        e["points"] -= cut
        excess -= cut
    # 极端情形（颗数过多无法扣回）下仍可能 >预算；此时不再强求（平台按权重处理）


def plan_scope_summary(plan: List[Dict[str, Any]]) -> List[Tuple[Tuple[str, int], int, int]]:
    agg: Dict[Tuple[str, int], List[int]] = defaultdict(list)
    for e in plan:
        agg[(e["region"], e["delay"])].append(e["points"])
    out = []
    for k, pts in sorted(agg.items(), key=lambda kv: -sum(kv[1])):
        out.append((k, len(pts), sum(pts)))
    return out


# --------------------------------------------------------------------------- #
# 可选 --sync：拉平台 OS 指标改善权重（复用 sync_platform_alphas 的抽数逻辑）
# --------------------------------------------------------------------------- #
def sync_os() -> Dict[str, int]:
    """拉平台 OS 池并回填本地 alphas（只补 OS 指标，不改 IS）。返回计数。"""
    import sync_platform_alphas as sy  # tools/ 已在 sys.path
    from wqb.store import CampaignStore

    print("[sync] 拉取平台 OS 池 ...", file=sys.stderr)
    pool = asyncio.run(sy.fetch_os_pool(limit=100))
    print(f"[sync] 平台 OS 池: {len(pool)} 个", file=sys.stderr)
    store = CampaignStore(path=DB)
    cur = store.connection.cursor()
    cur.execute("SELECT alpha_id FROM alphas WHERE date_submitted IS NOT NULL")
    local_ids = {r[0] for r in cur.fetchall()}
    stats: Dict[str, int] = defaultdict(int)
    for a in pool:
        payload = sy.to_store_payload(a)
        os_data = payload.pop("os_data")
        aid = payload.get("alpha_id")
        if not aid or aid not in local_ids:
            continue
        try:
            r = store.upsert_alpha_os_metrics(
                aid, os_data, region=payload.get("region"),
                submitted_info={"platform_status": payload.get("platform_status"),
                                "stage": payload.get("stage"),
                                "alpha_type": payload.get("alpha_type"),
                                "date_submitted": payload.get("date_submitted"),
                                "expression": payload.get("expression")},
            )
            stats[f"os_{r.get('action')}"] += 1
        except Exception as e:  # noqa: BLE001
            stats["error"] += 1
            print(f"  [sync error] {aid}: {e}", file=sys.stderr)
    return dict(stats)


# --------------------------------------------------------------------------- #
# 断点续跑 checkpoint
# --------------------------------------------------------------------------- #
def load_ckpt() -> set:
    if os.path.exists(CKPT_PATH):
        try:
            return set(json.load(open(CKPT_PATH, encoding="utf-8")).get("applied", []))
        except Exception:
            return set()
    return set()


def save_ckpt(applied: set) -> None:
    os.makedirs(RESULTS, exist_ok=True)
    tmp = CKPT_PATH + ".tmp"
    json.dump({"applied": sorted(applied)}, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CKPT_PATH)


def load_plan() -> List[Dict[str, Any]]:
    return json.load(open(PLAN_PATH, encoding="utf-8"))


def save_plan(plan: List[Dict[str, Any]]) -> None:
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(plan, open(PLAN_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
# 写平台（PATCH osmosisPoints）— 带断点续跑 + 失败分类
# --------------------------------------------------------------------------- #
def classify_failure(status_code: int, body: str) -> str:
    b = (body or "").lower()
    if "inactive" in b:
        return "inactive"
    if "non-compensated" in b or "compensated" in b:
        return "non_compensated"
    if status_code == 400 and "between 1 and 100000" in b:
        return "range"
    return "other"


async def apply_plan(plan: List[Dict[str, Any]], dry_run: bool
                     ) -> Tuple[int, int, int, Dict[str, List[str]], set]:
    """PATCH 计划。返回 (ok, skip, fail, failures_by_reason, applied_this_round)。

    applied_this_round = 本轮成功写入的 alpha_id（含续跑跳过的也返回已应用全集由调用方并）。
    """
    applied = load_ckpt()
    ok = skip = fail = 0
    failures: Dict[str, List[str]] = defaultdict(list)

    if dry_run:
        print("[dry-run] 不写平台（不鉴权）；预览如下（前 30）:", file=sys.stderr)
        for e in plan[:30]:
            print(f"  {e['region']} D{e['delay']} {e['alpha_id']} -> {e['points']}", file=sys.stderr)
        return 0, len(plan), 0, failures, applied

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    base = brain_client.base_url

    total = len(plan)
    for i, e in enumerate(plan, 1):
        aid = e["alpha_id"]
        pts = int(e["points"])
        if aid in applied:
            skip += 1
            continue
        if not (MIN_PTS <= pts <= MAX_PTS):
            failures["range"].append(aid)
            fail += 1
            print(f"  [{i}/{total}] RANGE {aid} pts={pts}", file=sys.stderr)
            continue
        try:
            r = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                             json={"osmosisPoints": pts})
            if r.status_code >= 400:
                reason = classify_failure(r.status_code, getattr(r, "text", "") or "")
                failures[reason].append(aid)
                fail += 1
                print(f"  [{i}/{total}] FAIL({reason}) {aid} {r.status_code}: "
                      f"{(getattr(r,'text','') or '')[:160]}", file=sys.stderr)
            else:
                ok += 1
                applied.add(aid)
                if ok % 10 == 0:
                    save_ckpt(applied)
                print(f"  [{i}/{total}] OK {aid} -> {pts}", file=sys.stderr)
        except Exception as ex:  # noqa: BLE001
            failures["err"].append(aid)
            fail += 1
            print(f"  [{i}/{total}] ERR {aid}: {ex}", file=sys.stderr)

    save_ckpt(applied)
    return ok, skip, fail, failures, applied


# --------------------------------------------------------------------------- #
# 自动 replan：丢弃失败 + 丢弃 <10 的范围，剩余 rescale 到 100k
# --------------------------------------------------------------------------- #
def replan(plan: List[Dict[str, Any]], applied: set, failed_ids: set
           ) -> Tuple[List[Dict[str, Any]], List[Tuple[str, int]]]:
    """返回 (new_plan, dropped_scopes)。

    - 失败（inactive/non_compensated/range/err）的 alpha 直接丢弃；
    - 剩余范围内 <10 个的整范围丢弃（不计入 eligibility，其已写点数因 <10 而惰性）；
    - 剩余范围点数 rescale 到 TOTAL_BUDGET。
    """
    kept = [e for e in plan if e["alpha_id"] in applied and e["alpha_id"] not in failed_ids]
    # 统计每范围剩余数
    cnt: Dict[Tuple[str, int], int] = defaultdict(int)
    for e in kept:
        cnt[(e["region"], e["delay"])] += 1
    dropped_scopes = [k for k, n in cnt.items() if n < MIN_PER_SCOPE]
    kept = [e for e in kept if (e["region"], e["delay"]) not in set(dropped_scopes)]

    by_scope: Dict[Tuple[str, int], float] = defaultdict(float)
    for e in kept:
        by_scope[(e["region"], e["delay"])] += e["points"]
    tot_now = sum(by_scope.values()) or 1.0
    scale = TOTAL_BUDGET / tot_now

    new_plan: List[Dict[str, Any]] = []
    for e in kept:
        new_pts = int(round(e["points"] * scale))
        new_pts = max(MIN_PTS, min(MAX_PTS, new_pts))
        # 保留 prod 标签（供最终 plan 落盘审计；exclude 已在行级完成，这里仅透传）
        new_plan.append({"region": e["region"], "delay": e["delay"],
                         "alpha_id": e["alpha_id"], "points": new_pts,
                         "prod": e.get("prod")})
    return new_plan, dropped_scopes


# --------------------------------------------------------------------------- #
# 零化非计划 alpha（"替换式分配"语义）：计划外的候选一律清零，避免旧分配残留
# 与本次分配冲突（尤其 prod≥0.7 被剔除的、以及上一轮已写过点的 GLB 等范围）。
# 平台 osmosisPoints 范围 1–100000；若 0 被拒则回退到最小值 1（近似零暴露）。
# --------------------------------------------------------------------------- #
async def zero_others(all_rows: List[Dict[str, Any]], plan: List[Dict[str, Any]],
                      dry_run: bool) -> Tuple[int, int, int]:
    """PATCH 所有「候选池内但不在最终 plan」的 alpha 为 0。返回 (ok_zero, fallback_1, fail)。"""
    if dry_run:
        print("[dry-run] 零化非计划 alpha 跳过（未真正写）", file=sys.stderr)
        return 0, 0, 0
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    base = brain_client.base_url
    plan_ids = {e["alpha_id"] for e in plan}
    other = [r for r in all_rows if r["alpha_id"] not in plan_ids]
    ok = fb = err = 0
    for r in other:
        aid = r["alpha_id"]
        try:
            resp = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                               json={"osmosisPoints": 0})
            if resp.status_code < 400:
                ok += 1
            elif resp.status_code == 400 and (
                "greater than or equal to 1" in (getattr(resp, "text", "") or "")
                or "between 1 and 100000" in (getattr(resp, "text", "") or "")
            ):
                # 平台最小值就是 1（osmosisPoints=0 被拒），回退到最小值 1 = 近似零暴露
                r2 = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                                 json={"osmosisPoints": 1})
                if r2.status_code < 400:
                    fb += 1
                    print(f"  [zero] {aid}: 0 被拒，回退到最小值 1", file=sys.stderr)
                else:
                    err += 1
                    print(f"  [zero] FAIL(回退) {aid} {r2.status_code}: "
                          f"{(getattr(r2,'text','') or '')[:160]}", file=sys.stderr)
            else:
                err += 1
                print(f"  [zero] FAIL {aid} {resp.status_code}: "
                      f"{(getattr(resp,'text','') or '')[:160]}", file=sys.stderr)
        except Exception as ex:  # noqa: BLE001
            err += 1
            print(f"  [zero] ERR {aid}: {ex}", file=sys.stderr)
    print(f"\n[zero] 非计划 alpha 零化: 成功(0)={ok}  回退(1)={fb}  失败={err}  共 {len(other)} 颗",
          file=sys.stderr)
    return ok, fb, err


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def print_review(rows: List[Dict[str, Any]], scopes: Dict[Tuple[str, int], List[Dict[str, Any]]],
                 plan: List[Dict[str, Any]], met: bool) -> None:
    print(f"\n=== 候选池: {len(rows)} 颗 ACTIVE REGULAR/untyped ===")
    print(f"{'scope':<12} {'n':>4} {'n_os':>5} {'avgIS':>7} {'avgOS':>7} -> {'状态'}")
    stats = []
    for (reg, d), al in sorted(scopes.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        osv = [a["os_sharpe"] for a in al if a["os_sharpe"] is not None]
        isv = [a["sharpe"] for a in al if a["sharpe"] is not None]
        stats.append((reg, d, len(al), len(osv),
                      (sum(isv)/len(isv)) if isv else None,
                      (sum(osv)/len(osv)) if osv else None))
    eligible = sum(1 for s in stats if s[2] >= MIN_PER_SCOPE)
    for s in sorted(stats, key=lambda x: (x[2] < MIN_PER_SCOPE, x[5] or x[4] or 0), reverse=True):
        flag = "ELIG" if s[2] >= MIN_PER_SCOPE else "short"
        print(f"  {s[0]:<5} D{s[1]!s:<3} {s[2]:>4} {s[3]:>5} "
              f"{str(round(s[4],3)) if s[4] else '-':>7} "
              f"{str(round(s[5],3)) if s[5] else '-':>7} -> {flag}")
    print(f"\n达标范围 (≥{MIN_PER_SCOPE}): {eligible}  "
          f"eligibility(≥{MIN_SCOPES}范围): {'YES' if met else 'NO（将退化取前 3 范围）'}")

    print(f"\n=== 计划: {len(plan)} 颗, 总点数 {sum(e['points'] for e in plan)} (预算 {TOTAL_BUDGET}) ===")
    for (k, n, pts) in plan_scope_summary(plan):
        print(f"  {k[0]:<5} D{k[1]!s:<3} n={n:>3} 点数={pts:>7}")

    # prod 透明度：列出计划内 prod>=PROD_MAX 的 alpha 及其分配点数（discount 下应趋近 0）
    hot = [(e["prod"], e["region"], e["delay"], e["alpha_id"], e["points"])
           for e in plan if e.get("prod") is not None and e["prod"] >= PROD_MAX]
    hot_pts = sum(e[4] for e in hot)
    if hot:
        print(f"\n⚠ 计划内 prod≥{PROD_MAX}: {len(hot)} 颗, 共 {hot_pts} 点 "
              f"({hot_pts/TOTAL_BUDGET*100:.1f}% 预算) [policy={PROD_POLICY}]")
        for v, reg, d, aid, p in sorted(hot, key=lambda x: -x[0]):
            print(f"    prod={v:.3f}  {reg} D{d}  {aid}  pts={p}")
    else:
        print(f"\n✓ 计划内无 prod≥{PROD_MAX} 的 alpha 获得权重 [policy={PROD_POLICY}]")


def main() -> int:
    ap = argparse.ArgumentParser(description="WorldQuant BRAIN Osmosis points 分配（review+apply+自动replan）")
    ap.add_argument("--sync", action="store_true", help="review 前先拉平台 OS 指标改善权重")
    ap.add_argument("--apply", action="store_true", help="写入平台（默认仅 review+写本地 plan）")
    ap.add_argument("--dry-run", action="store_true", help="与 --apply 同用：只预览 PATCH 不真正写")
    ap.add_argument("--region", default=None, help="范围覆盖统计/分配限区（写平台仍为全量 plan）")
    ap.add_argument("--max-replan", type=int, default=5, help="apply 失败自动 replan 最大轮数")
    ap.add_argument("--prod-policy", choices=["ignore", "discount", "exclude"], default="discount",
                   help="prod 相关性策略：discount=质量递减打折(默认)；exclude=剔除 prod>阈值；ignore=不纳 prod")
    ap.add_argument("--prod-max", type=float, default=0.70, help="prod 阈值（默认 0.70，与提交闸一致）")
    a = ap.parse_args()

    global PROD_POLICY, PROD_MAX
    PROD_POLICY = a.prod_policy
    PROD_MAX = a.prod_max

    try:
        rows = load_candidates(a.region)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 3

    # 零化非计划 alpha 用的「完整候选池」快照（过滤前的最新全量，含被 exclude 剔除的 prod≥阈值 alpha）
    all_rows = list(rows)

    # exclude 模式：剔除 prod>=阈值 的 alpha（含恰好阈值；可能令某范围掉到 <10 而失格）。
    # ★ 保守硬规则：本地 prod 为 None（无数据）也一并剔除——"不知道是否干净"时不应分配，
    #   否则会像 JjGwjd5E 那样把平台 prod>0.7 的 alpha 漏放进分配。
    if PROD_POLICY == "exclude":
        before = len(rows)
        none_ct = sum(1 for r in rows if r.get("prod") is None)
        rows = [r for r in rows if not (r.get("prod") is None or r["prod"] >= PROD_MAX)]
        print(f"[exclude] 剔除 prod>={PROD_MAX} 或 未知(None) 的 alpha: {before} -> {len(rows)} 颗 "
              f"(其中 None-prod {none_ct} 颗因本地无 prod 数据被保守剔除)", file=sys.stderr)

    if a.sync:
        st = sync_os()
        print(f"[sync] 结果: {st}", file=sys.stderr)
        # sync 后重新读（OS 指标已落库），并刷新快照（仍为过滤前全量）
        rows = load_candidates(a.region)
        all_rows = list(rows)
        if PROD_POLICY == "exclude":
            # 与主线 exclude 一致：None-prod 也一并保守剔除
            rows = [r for r in rows if not (r.get("prod") is None or r["prod"] >= PROD_MAX)]

    scopes = build_scopes(rows)
    plan = build_plan(scopes)
    save_plan(plan)
    # met 标记仅用于展示；build_plan 内部已决定退化
    eligible = sum(1 for (reg, d), al in scopes.items() if len(al) >= MIN_PER_SCOPE)
    met = eligible >= MIN_SCOPES
    print_review(rows, scopes, plan, met)

    if not a.apply:
        print("\n[review-only] 已写 plan ->", PLAN_PATH, "；加 --apply 写入平台。")
        return 0

    # ---- apply 阶段：PATCH + 自动 replan 闭环 ----
    dry = a.dry_run
    attempt = 0
    last_plan_sig = None
    while True:
        ok, skip, fail, failures, applied = asyncio.run(apply_plan(plan, dry))
        print(f"\n=== 轮 {attempt}: OK={ok} 跳过={skip} 失败={fail} ===", file=sys.stderr)
        for reason, ids in failures.items():
            print(f"  失败[{reason}]: {len(ids)} 颗", file=sys.stderr)
        if not fail:
            break
        if dry:
            print("[dry-run] 不执行 replan（未真正写平台）。", file=sys.stderr)
            break
        failed_ids = set()
        for ids in failures.values():
            failed_ids.update(ids)
        new_plan, dropped = replan(plan, applied, failed_ids)
        sig = json.dumps(new_plan, sort_keys=True)
        if not new_plan or sig == last_plan_sig:
            print("[replan] 无法继续收敛，停止。", file=sys.stderr)
            break
        # 剩余达标范围数
        rem_scopes = set((e["region"], e["delay"]) for e in new_plan)
        if len(rem_scopes) < MIN_SCOPES:
            print(f"[replan] 剩余达标范围 {len(rem_scopes)} < {MIN_SCOPES}，eligibility 不足；"
                  f"仍写平台（点数惰性）。", file=sys.stderr)
        print(f"[replan] 丢弃范围: {dropped}；新 plan {len(new_plan)} 颗，"
              f"总点数 {sum(e['points'] for e in new_plan)}", file=sys.stderr)
        save_plan(new_plan)
        save_ckpt(set())  # 清 checkpoint，重 apply（rescale 后已写点数需更新）
        plan = new_plan
        last_plan_sig = sig
        attempt += 1
        if attempt >= a.max_replan:
            print(f"[replan] 达最大轮数 {a.max_replan}，停止。", file=sys.stderr)
            break

    final = load_plan()
    print(f"\n=== 最终 plan: {len(final)} 颗, 总点数 {sum(e['points'] for e in final)} ===")
    for (k, n, pts) in plan_scope_summary(final):
        print(f"  {k[0]:<5} D{k[1]!s:<3} n={n:>3} 点数={pts:>7}")
    print(f"\nplan -> {PLAN_PATH}  checkpoint -> {CKPT_PATH}")

    # 零化非计划 alpha（替换式分配：清掉旧分配里残留的计划外 alpha，
    # 特别是被 exclude 剔除的 prod>=阈值 的 8 颗，以及上一轮已写过点的 GLB 等范围）
    if not dry:
        z_ok, z_fb, z_err = asyncio.run(zero_others(all_rows, final, dry))
        print(f"[zero] 零化小结: 成功(0)={z_ok}  回退(1)={z_fb}  失败={z_err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
