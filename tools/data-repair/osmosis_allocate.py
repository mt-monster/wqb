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
  python tools/data-repair/osmosis_allocate.py --source platform --prod-policy exclude --prod-max 0.695  # 平台权威源+实盘业绩加权（避 stale DB）
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

# ★ SA/RA 分池（2026-10-21）：RA 保底占比。
# 取论坛 DL61056（22赞）的 `REGULAR_MIN_POINT_SHARE = 0.65`。
# 作用：即使 --super-budget-share 填到 0.50，RA 也会被保到 65%
# ⇒ **SUPER 实际占比硬上限 = 1 - 0.65 = 35%**（与该帖 RA 保底分支等价）。
REGULAR_MIN_SHARE = 0.65

# ★ 单颗 SUPER 点数硬上限（2026-10-21）：取论坛 DL61056 的 `SUPER_MAX_POINTS_PER_ALPHA = 10_000`
# ⇒ 恰好 = 单 scope 预算（100k）的 10%。
# 动机（实证反例）：首版 --super-top-n 是**全局** topN，把 IND 的 SA 池压到 2 颗，
# 单颗吃到 11,704（11.7%），超本上限 17%。封顶后腾出的预算回流给同 scope 的 REGULAR。
SUPER_MAX_PTS = 10_000

# prod 相关性策略（与本项目提交闸 prod<0.7 一致）：
#   discount = 对 prod∈(PROD_MAX,1] 的质量递减打折（保留范围资格，仅挪权重）
#   exclude  = 剔除 prod>=PROD_MAX 的 alpha（含恰好阈值；含本地 prod 为 None 的保守剔除；可能令某范围掉到 <10 而失格）
#   ignore   = 不纳 prod（旧行为）
PROD_POLICY = "discount"
PROD_MAX = 0.70
PROD_PENALTY_FLOOR = 0.05    # prod=1.0 时质量保留的最低比例

# investability 加权（2026-10-13 定案）
#   平台 is.investabilityConstrained.sharpe = 实盘约束（maxtrade/maxpos）后的真实 Sharpe，
#   是本工具 quality() 的**首选**质量口径——IS sharpe 是纸面值，高换手 alpha 施加
#   investability 约束后常暴跌 60%+（官方 osmotic 文档：衰减≥60% 应剔除）。
#   ⚠ 该字段仅 platform 源可得（312 颗里 150 颗有）；DB alphas 表无此列 ⇒ 源=db 时全 None。
#   缺失时回退 (os_sharpe or sharpe) * INVEST_FALLBACK 作保守估计。
INVEST_FALLBACK = 0.65       # 缺失 investability 时按 IS 的这个比例保守折算


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
        # DB alphas 表无 investability 列 ⇒ 恒定 None，quality() 走 INVEST_FALLBACK 回退。
        # 想用真实 investability 请走 --source platform。
        d["investability_sharpe"] = None
        rows.append(d)
    con.close()
    return rows


def load_candidates_platform() -> List[Dict[str, Any]]:
    """平台权威候选（避本地 DB stale）：拉 OS 池全量，过滤 ACTIVE + type∈{REGULAR,SUPER}。

    ★ 2026-10-21 修正（用户发现 UI 超线）：平台 Genius Status 页的 scope 点数和
    = REGULAR + SUPER 之和（UI 截图 KOR 126,148 / IND 111,359 = REGULAR 100k +
    SUPER 残留 26k/11k 逐颗吻合）。此前只过滤 REGULAR 导致 SUPER 的 47,593 点
    历史残留游离在管理之外 ⇒ KOR/IND 不满足 exactly-100k。
    官方明确支持分配 SuperAlpha，故纳入统一管理。

    抽取 region/delay/IS(sharpe,turnover)/OS(sharpe)/prod，键名与 load_candidates 对齐，
    使 quality()/build_plan() 无需改动即可复用。prod 优先 is.prodCorrelation，回退顶层 prod。
    """
    async def _fetch() -> List[Dict[str, Any]]:
        from brain_api import brain_client
        rows: List[Dict[str, Any]] = []
        off = 0
        for _ in range(200):
            r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
            pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
            res = pl.get("results", []) or []
            if not res:
                break
            rows.extend(res)
            if not pl.get("next"):
                break
            off += 100
        return rows
    pool = asyncio.run(_fetch())
    out: List[Dict[str, Any]] = []
    for a in pool:
        if a.get("status") != "ACTIVE" or a.get("type") not in ("REGULAR", "SUPER"):
            continue
        st = a.get("settings") or {}
        isd = a.get("is") or {}
        osd = a.get("os") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = a.get("prod")
        # investability 口径：平台 is.investabilityConstrained.sharpe
        # （= MCP HTTP 源 metrics.investability_sharpe，两者同值；150/312 颗有）
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
        out.append({
            "investability_sharpe": inv,
            "alpha_id": a.get("id"),
            "region": st.get("region"),
            "delay": st.get("delay"),
            "sharpe": isd.get("sharpe"),
            "os_sharpe": osd.get("sharpe"),
            "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"),
            "margin": isd.get("margin"),
            "two_year_sharpe": isd.get("twoYearSharpe"),
            "stage": a.get("stage"),
            "platform_status": a.get("status"),
            "alpha_type": a.get("type"),
            "prod": prod,
        })
    # 合并 DB 的 os_sharpe（sync 已落库，比平台列表 os 段更完整）：平台无则用 DB。
    # 这样 prod/status/存在性 走平台权威，实盘业绩权重走最完整的 OS sharpe。
    try:
        from wqb.db_conn import connect as _db_connect
        con = _db_connect(readonly=True, row_factory=sqlite3.Row)
        db_os = {r["alpha_id"]: r["os_sharpe"] for r in con.execute(
            "SELECT alpha_id, os_sharpe FROM alphas WHERE os_sharpe IS NOT NULL").fetchall()}
        con.close()
        merged = 0
        for rec in out:
            if rec.get("os_sharpe") is None and rec["alpha_id"] in db_os:
                rec["os_sharpe"] = db_os[rec["alpha_id"]]
                merged += 1
        if merged:
            print(f"  [platform] 合并 DB os_sharpe: {merged} 颗 (平台列表 os 段缺，用 sync 落库值)",
                  file=sys.stderr)
    except Exception as e:  # noqa: BLE001
        print(f"  [platform] DB os_sharpe 合并失败(忽略，退 IS): {e}", file=sys.stderr)
    return out


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
    """质量 = 优先 investability_sharpe，缺失回退 (OS|IS)×INVEST_FALLBACK，再乘 prod 折扣。

    2026-10-13 改：原实现直接用 IS sharpe 加权，是**纸面质量**——高换手 alpha 施加
    investability 约束（maxtrade/maxpos）后 Sharpe 常暴跌 60%+，却仍按 IS 拿满权重，
    导致权重与真实质量严重错配（实测：IND/1 占 43% 权重但 investability 衰减 51%）。

    ★ 不再额外惩罚高换手：官方《High Turnover Alphas》文档明确**鼓励** TO>20% 的 alpha
      （"less correlated with traditional lower-turnover ideas"，提供正交收益源），
      且 investability_sharpe 本身已含成本与约束，再人工打折会误伤真正稳健的高换手 alpha
      （实测反例：d5bnE8jJ GLB TO=0.446 但 investability=3.19，极稳健）。
      原实现的 `pen = 0.6 if to < 0.05` 只惩罚**超低**换手（疑似僵尸信号），予以保留。
    """
    inv = a.get("investability_sharpe")
    if inv is not None:
        v = float(inv)
    else:
        base = a.get("os_sharpe") if a.get("os_sharpe") is not None else a.get("sharpe")
        if base is None:
            return 0.0
        v = float(base) * INVEST_FALLBACK
    to = a.get("turnover") or 0
    pen = 0.6 if to < 0.05 else 1.0
    q = max(v, 0.0) * pen
    return q * prod_penalty(a.get("prod"), PROD_POLICY, PROD_MAX)


# --------------------------------------------------------------------------- #
# 计划生成（质量比例 + 范围保底 + rescale 到预算）
# --------------------------------------------------------------------------- #
def build_plan(scopes: Dict[Tuple[str, int], List[Dict[str, Any]]],
               eligible_only: bool = True,
               per_scope_budget: bool = False,
               super_budget_share: Optional[float] = None,
               super_max_pts: Optional[int] = None) -> List[Dict[str, Any]]:
    """按质量比例分配 TOTAL_BUDGET 到点。

    eligible_only=True 时只在 (n>=10) 的范围里分配；若达标范围 <3，退化为取质量最高的
    前 3 个范围（平台仍不计数，但至少把点数设上去，便于用户后续补到 ≥3）。

    ★ per_scope_budget=True（2026-10-19 修正）：按官方《Osmosis Allocation Guide》
    「Within each scope, you need to allocate **exactly 100k points** to at least 10 Alphas」，
    **每个 eligible scope 独立分配 100k**（不是总 100k 按比例拆）。否则平台判
    "did not meet the eligibility criteria"。此模式下 scope 间不再共享预算、不再
    按 scope_q 比例拆分；每 scope 内部仍按 quality 等比分配 100k。

    ★ super_budget_share（2026-10-21 新增，SA/RA 分池）：论坛实证方案（DL61056，22赞）
    的做法是 **REGULAR 与 SUPER 分开评分、分开预算**，理由：SUPER 的 Fitness/Sharpe
    是**组合层面**指标，尺度天然高于单 alpha（论坛 LY43440 评论），同池排序会碾压 REGULAR。
    本参数 = 每 scope 内 SUPER 预算占比；None = 不分池（旧行为，两类型同池按 quality 分配）。
    实际生效值会被 RA 保底 `REGULAR_MIN_SHARE` 压住：
        share = min(super_budget_share, 1 - REGULAR_MIN_SHARE)   # 即 SA 有效硬上限 35%
    与 DL61056 的 `SUPER_POINT_SHARE=0.22` + `REGULAR_MIN_POINT_SHARE=0.65` 一致。
    某一类型在该 scope 为空时，预算整体流转到另一类型（同 SP74109 的 `pool_ra += pool_sa`）。

    ★ super_max_pts（2026-10-21 新增，单颗 SA 硬上限）：对齐论坛 DL61056 的
    `SUPER_MAX_POINTS_PER_ALPHA = 10_000`（即单 scope 预算的 10%）。
    动机（实证反例）：2026-10-21 首版 `--super-top-n` 是**全局** topN，而 IND 的 11 颗 SUPER
    inv 集中在 2.15~3.98 的窄带里，全局门槛线（inv 3.12）正好切在带子中间 ⇒ IND 只剩 2 颗 SA，
    22k 预算由 2 颗分，单颗 11,704（**11.7%，超论坛上限 17%**）。
    封顶后**腾出的预算回流 RA**（同 SP74109 的 `pool_ra += pool_sa` 思路），
    不浪费、也不改变 SA 池的选股。
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

    if per_scope_budget:
        # 每 scope 独立 100k（官方 eligibility 要求 exactly 100k per scope）
        plan: List[Dict[str, Any]] = []
        for s in cand:
            key = (s["region"], s["delay"])
            al = sorted(scopes[key], key=quality, reverse=True)
            scope_budget = TOTAL_BUDGET  # 每 scope 各 100k

            if super_budget_share is not None:
                # ★ SA/RA 分池：两个池各自在池内按 quality 归一化分配预算。
                sa = [a for a in al if a.get("alpha_type") == "SUPER"]
                ra = [a for a in al if a.get("alpha_type") != "SUPER"]
                share = max(0.0, min(float(super_budget_share),
                                     1.0 - REGULAR_MIN_SHARE))
                # —— 第一步：SA 池（带单颗上限）——
                # 必须先算 SA 实际落点，才能把「封顶腾出的预算」准确回流给 RA。
                sa_alloc: Dict[str, int] = {}
                if sa:
                    sq_sa = sum(quality(a) for a in sa) or 1.0
                    if ra:
                        sa_b = int(round(scope_budget * share))
                        for a in sa:
                            pts = int(round(sa_b * quality(a) / sq_sa))
                            if super_max_pts is not None:
                                pts = min(pts, int(super_max_pts))
                            sa_alloc[a["alpha_id"]] = max(MIN_PTS, min(MAX_PTS, pts))
                    else:
                        # 无 RA 可承接回流 ⇒ 不封顶，否则剩余预算会凭空蒸发
                        for a in sa:
                            pts = int(round(scope_budget * quality(a) / sq_sa))
                            sa_alloc[a["alpha_id"]] = max(MIN_PTS, min(MAX_PTS, pts))
                # —— 第二步：RA 拿「scope 预算 − SA 实际占用」——
                ra_budget = scope_budget - sum(sa_alloc.values())
                pools = [([a for a in sa if a["alpha_id"] in sa_alloc], None, "SA"),
                         (ra, ra_budget, "RA")]
            else:
                pools = [(al, scope_budget, "-")]

            for pool, budget, tag in pools:
                if not pool:
                    continue
                if tag == "SA":
                    # SA 点数已在第一步算好（受 super_max_pts 约束），此处直接落计划
                    for a in pool:
                        plan.append({"region": key[0], "delay": key[1],
                                     "alpha_id": a["alpha_id"],
                                     "points": sa_alloc[a["alpha_id"]],
                                     "prod": a.get("prod"),
                                     "alpha_type": a.get("alpha_type"),
                                     "pool": tag})
                    continue
                sq = sum(quality(a) for a in pool) or 1.0
                for a in pool:
                    pts = int(round(budget * quality(a) / sq))
                    pts = max(MIN_PTS, min(MAX_PTS, pts))
                    plan.append({"region": key[0], "delay": key[1],
                                 "alpha_id": a["alpha_id"], "points": pts,
                                 "prod": a.get("prod"),
                                 "alpha_type": a.get("alpha_type"),
                                 "pool": tag})
        _trim_per_scope(plan)
        return plan

    # 旧逻辑（总 100k 按 scope_q 比例拆）—— 保留向后兼容，但不再用于 eligibility
    scope_q: Dict[Tuple[str, int], float] = {}
    for s in cand:
        key = (s["region"], s["delay"])
        scope_q[key] = sum(quality(a) for a in scopes[key]) or 0.0
    tot_q = sum(scope_q.values()) or 1.0
    budgets = {k: max(SCOPE_FLOOR, v / tot_q) for k, v in scope_q.items()}
    sf = sum(budgets.values()) or 1.0
    budgets = {k: v / sf for k, v in budgets.items()}

    plan = []
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


def _trim_per_scope(plan: List[Dict[str, Any]]) -> None:
    """每 scope 独立 trim 到 exactly 100k：超出则从大项扣回，不足则补到最大项。

    ★ 2026-10-21 修正：平台 eligibility 是「每 scope exactly 100k」逐项校验
    （UI 只有点数精确=100,000 的 scope 有左侧达标徽章）。此前四舍五入后只减不补，
    导致 GLB 100,001 / DEU 99,999 差 1。
    """
    agg: Dict[Tuple[str, int], List[int]] = defaultdict(list)
    idx_by_scope: Dict[Tuple[str, int], List[int]] = defaultdict(list)
    for i, e in enumerate(plan):
        k = (e["region"], e["delay"])
        agg[k].append(e["points"])
        idx_by_scope[k].append(i)
    for k, pts in agg.items():
        total = sum(pts)
        excess = total - TOTAL_BUDGET
        if excess < 0:
            # 补足：差额全部加到该 scope 最大项（不影响其他项的相对比例）
            top = max(idx_by_scope[k], key=lambda i: plan[i]["points"])
            plan[top]["points"] = min(MAX_PTS, plan[top]["points"] + (-excess))
            continue
        if excess == 0:
            continue
        # 按 points 降序，扣到 MIN_PTS
        order = sorted(idx_by_scope[k], key=lambda i: -plan[i]["points"])
        for i in order:
            if excess <= 0:
                break
            reducible = plan[i]["points"] - MIN_PTS
            if reducible <= 0:
                continue
            cut = min(reducible, excess)
            plan[i]["points"] -= cut
            excess -= cut


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
#
# ★ 2026-10-21 修正（实测）：清零点必须发 JSON **null**，不能发 0。
#   - PATCH {"osmosisPoints": 0}    -> HTTP 400（"greater than or equal to 1"）
#   - PATCH {"osmosisPoints": null} -> HTTP 200，回读 osmosisPoints=None（真正清零）
#   旧实现发 0、失败后回退到 1，导致每个 scope 实际点数和 = 100,000 + 计划外颗数
#   （实测 IND/KOR 各 +12、GBR +3、GLB +2、DEU +1），只能靠 balance_osmosis.py 事后扣回。
#   现改为优先发 null，1 仅作极端兜底。
#   来源：论坛帖 DL61056 评论区 CM59456（2026-09-21）实证 + 本仓库 verify_zero_null.py 复现。
# --------------------------------------------------------------------------- #
async def zero_others(all_rows: List[Dict[str, Any]], plan: List[Dict[str, Any]],
                      dry_run: bool) -> Tuple[int, int, int]:
    """PATCH 所有「候选池内但不在最终 plan」的 alpha 清零。
    返回 (ok_zero_null, fallback_1, fail)。"""
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
            # ★ 首选 null（平台唯一可真正清零的写法）
            resp = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                               json={"osmosisPoints": None})
            if resp.status_code < 400:
                ok += 1
            elif resp.status_code == 400 and (
                "non-compensated" in (getattr(resp, "text", "") or "").lower()
            ):
                # 非补偿池 alpha 本身不可写点，跳过即失败（不影响合计）
                err += 1
                print(f"  [zero] SKIP {aid} non-compensated", file=sys.stderr)
            else:
                # 极端兜底：老接口/异常分支下回退到最小值 1（近似零暴露）
                r2 = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                                 json={"osmosisPoints": 1})
                if r2.status_code < 400:
                    fb += 1
                    print(f"  [zero] {aid}: null 被拒({resp.status_code})，回退到 1",
                          file=sys.stderr)
                else:
                    err += 1
                    print(f"  [zero] FAIL(回退) {aid} {r2.status_code}: "
                          f"{(getattr(r2,'text','') or '')[:160]}", file=sys.stderr)
        except Exception as ex:  # noqa: BLE001
            err += 1
            print(f"  [zero] ERR {aid}: {ex}", file=sys.stderr)
    print(f"\n[zero] 非计划 alpha 零化: 成功(null)={ok}  回退(1)={fb}  失败={err}  共 {len(other)} 颗",
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
    ap.add_argument("--sync", action="store_true", help="review 前先拉平台 OS 指标改善权重（仅 source=db 生效）")
    ap.add_argument("--source", choices=["db", "platform"], default="db",
                   help="候选来源：db=本地 alphas 表(默认)；platform=直接拉平台 OS 池(权威，避 stale DB)")
    ap.add_argument("--exclude-region", default=None,
                   help="排除某区不参与分配(逗号分隔，如 USA)；该区 alpha 仍会被零化。其余区 rescale 到 10 万")
    ap.add_argument("--apply", action="store_true", help="写入平台（默认仅 review+写本地 plan）")
    ap.add_argument("--dry-run", action="store_true", help="与 --apply 同用：只预览 PATCH 不真正写")
    ap.add_argument("--region", default=None, help="范围覆盖统计/分配限区（写平台仍为全量 plan）")
    ap.add_argument("--max-replan", type=int, default=5, help="apply 失败自动 replan 最大轮数")
    ap.add_argument("--prod-policy", choices=["ignore", "discount", "exclude"], default="discount",
                   help="prod 相关性策略：discount=质量递减打折(默认)；exclude=剔除 prod>阈值；ignore=不纳 prod")
    ap.add_argument("--prod-max", type=float, default=0.70, help="prod 阈值（默认 0.70，与提交闸一致）")
    ap.add_argument("--force-repatch", action="store_true",
                   help="apply 前清空 checkpoint，强制重新 PATCH 全部 alpha（用于**更新已分配 alpha 的点数**）。"
                        "默认保留 checkpoint 作断点续跑；不清则已分配过的 alpha 会被 skip、点数不更新。")
    ap.add_argument("--drop-invest-decay", type=float, default=None,
                   help="剔除 investability 后 Sharpe 衰减≥该比例的 alpha（官方建议 0.6，"
                        "如 `--drop-invest-decay 0.6`）；默认 None=不剔除（剔除可能令范围掉到 <10 失格）。"
                        "仅对 investability 数据可得的 alpha 生效；需 --source platform。")
    ap.add_argument("--drop-inv-below", type=float, default=None,
                   help="剔除 investability 约束后 Sharpe **绝对值**低于该阈值的 alpha（如 `--drop-inv-below 1.0`"
                        " 剔除 inv<1.0 的硬伤 alpha）。与 --drop-invest-decay 的区别：后者按**衰减比例**剔除"
                        "（会把 IS 4.4→inv 1.36 这种仍可用的也剔掉），本参数只看约束后的绝对水平，更保守。"
                        "仅对 investability 数据可得者生效；需 --source platform。")
    ap.add_argument("--super-top-n", type=int, default=None, metavar="N",
                   help="★ 每 scope 只纳入 investability Sharpe 最高的 N 颗 SUPER（SuperAlpha），其余清零。"
                        "SUPER 的 Sharpe/inv 是组合层面指标，天然高于单 alpha，且其组件池就是该区 "
                        "REGULAR ⇒ 全纳入会造成「同一批信号重复押注 + 少数组合吃走大额权重」。"
                        "⚠ 2026-10-21 修正：原实现是**全局** topN，实测把 IND 的 SA 池压到 2 颗、"
                        "单颗占 11.7%%（超论坛上限），故改为**按 scope 各取 topN**。需 --source platform。")
    ap.add_argument("--super-max-pts", type=int, default=10_000, metavar="PTS",
                   help="★ 单颗 SUPER 的点数硬上限（默认 10000 = 单 scope 预算的 10%%），"
                        "对齐论坛 DL61056 的 SUPER_MAX_POINTS_PER_ALPHA。"
                        "封顶腾出的预算**回流给同 scope 的 REGULAR 池**。传 0 或负数 = 不封顶。")
    ap.add_argument("--per-scope-budget", action="store_true",
                   help="★ 官方 eligibility 模式（2026-10-19）：每 eligible scope 独立分配 100k 点"
                        "（官方要求 exactly 100k per scope, not total 100k）。"
                        "不加此 flag 则用旧的「总 100k 按 scope 比例拆」逻辑（会导致 not eligible）。")
    ap.add_argument("--super-budget-share", type=float, default=None, metavar="SHARE",
                   help="★ SA/RA 分池（2026-10-21）：每 scope 内 SUPER 预算占比，如 0.22。"
                        "论坛 DL61056（22赞）实证做法：REGULAR 与 SUPER 分开评分、分开预算，"
                        "避免 SUPER 的组合层面高数值碾压单 alpha。"
                        "实际生效 = min(SHARE, 1-REGULAR_MIN_SHARE)，即 SA 硬上限 35%%；"
                        "某类型为空时预算整体流转给对方。不给此参数 = 不分池（旧行为）。")
    a = ap.parse_args()

    if a.super_budget_share is not None:
        if not (0.0 <= a.super_budget_share <= 0.50):
            print(f"[error] --super-budget-share 必须在 0~0.50，收到 {a.super_budget_share}",
                  file=sys.stderr)
            return 2
        if a.super_budget_share > 1 - REGULAR_MIN_SHARE + 1e-9:
            print(f"[warn] --super-budget-share={a.super_budget_share} 超过 RA 保底允许的上限，"
                  f"实际生效值将被压到 {1 - REGULAR_MIN_SHARE:.2f}", file=sys.stderr)

    global PROD_POLICY, PROD_MAX
    PROD_POLICY = a.prod_policy
    PROD_MAX = a.prod_max

    try:
        if a.source == "platform":
            rows = load_candidates_platform()
        else:
            rows = load_candidates(a.region)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 3

    # 零化非计划 alpha 用的「完整候选池」快照（过滤前的最新全量，含被 exclude 剔除的 prod≥阈值 alpha）
    all_rows = list(rows)
    if a.source == "platform" and a.region:
        # platform 源：all_rows 保留全量（零化用），分配只限区
        rows = [r for r in rows if r["region"] == a.region]
    if a.exclude_region:
        # 排除某区：从分配集剔除，但 all_rows 仍含该区（zero_others 会把它零化）
        _excl = {x.strip().upper() for x in a.exclude_region.split(",") if x.strip()}
        rows = [r for r in rows if (r.get("region") or "").upper() not in _excl]

    # exclude 模式：剔除 prod>=阈值 的 alpha（含恰好阈值；可能令某范围掉到 <10 而失格）。
    # ★ 保守硬规则：本地 prod 为 None（无数据）也一并剔除——"不知道是否干净"时不应分配，
    #   否则会像 JjGwjd5E 那样把平台 prod>0.7 的 alpha 漏放进分配。
    if PROD_POLICY == "exclude":
        before = len(rows)
        none_ct = sum(1 for r in rows if r.get("prod") is None)
        rows = [r for r in rows if not (r.get("prod") is None or r["prod"] >= PROD_MAX)]
        print(f"[exclude] 剔除 prod>={PROD_MAX} 或 未知(None) 的 alpha: {before} -> {len(rows)} 颗 "
              f"(其中 None-prod {none_ct} 颗因本地无 prod 数据被保守剔除)", file=sys.stderr)

    # 可选：剔除 investability 后 Sharpe 衰减≥阈值的 alpha。
    # 依据：官方《Osmosis Allocation Guide》"Exclude Alphas whose Sharpe ratio declines by
    #   approximately 60% or more after investability constraints are applied"。
    # ⚠ 默认 None（不剔除）——剔除可能令某范围掉到 <10 而失格，故须用户显式开启。
    # ⚠ 仅对 investability_sharpe 可得者生效；缺失（DB 源或老 alpha）不剔除（不冤枉）。
    if a.drop_invest_decay is not None:
        thr = a.drop_invest_decay

        def _decayed(r: Dict[str, Any]) -> bool:
            inv = r.get("investability_sharpe")
            sv = r.get("sharpe")
            if inv is None or sv is None or sv <= 0:
                return False
            return inv < sv * (1.0 - thr)

        before = len(rows)
        rows = [r for r in rows if not _decayed(r)]
        print(f"[drop-invest] 剔除 investability 衰减≥{thr:.0%} 的 alpha: "
              f"{before} -> {len(rows)} 颗", file=sys.stderr)

    # 可选：剔除 investability 约束后 Sharpe 绝对值低于阈值的 alpha（方案 A，2026-10-21）。
    # 与 --drop-invest-decay 的区别：本参数只看约束后的**绝对水平**（inv<1.0 = 加约束后
    # Sharpe 不到 1，属硬伤），不惩罚「IS 很高但衰减大、约束后仍 >1」的 alpha。
    if a.drop_inv_below is not None:
        thr = a.drop_inv_below

        def _weak(r: Dict[str, Any]) -> bool:
            inv = r.get("investability_sharpe")
            return inv is not None and inv < thr

        before = len(rows)
        dropped = [r for r in rows if _weak(r)]
        rows = [r for r in rows if not _weak(r)]
        print(f"[drop-inv] 剔除 investability<{thr} 的 alpha: {before} -> {len(rows)} 颗",
              file=sys.stderr)
        for r in sorted(dropped, key=lambda x: (x.get("investability_sharpe") or 0)):
            print(f"   - {r['alpha_id']}  {r['region']}D{r.get('delay')}  "
                  f"IS={r.get('sharpe')}  inv={r.get('investability_sharpe'):.3f}",
                  file=sys.stderr)

    # ★ SUPER 限额（2026-10-21 修正为**每 scope** topN，用户同日确认）：
    # 理由：SUPER 的 Sharpe/inv 是组合层面（天然高于单 alpha），且组件池就是本区 REGULAR
    # ⇒ 全纳入 = 同一批信号重复押注 + 少数组合吃掉过大权重。取 top N 作点缀即可。
    # ⚠ 原实现是**全局** topN，实测踩坑：IND 的 11 颗 SUPER inv 集中在 2.15~3.98 窄带，
    #   全局门槛线（inv 3.12）恰好切在带子中间 ⇒ IND 只剩 2 颗 SA，22k 预算由 2 颗分，
    #   单颗 11,704 = **11.7%**（突破论坛 DL61056 的 SUPER_MAX_POINTS_PER_ALPHA=10,000 上限 17%）。
    #   改成按 scope 各取 topN 后，IND/KOR/GLB 各 4 颗，单颗降到 ~5,500（5.5%）。
    if a.super_top_n is not None:
        supers = [r for r in rows if r.get("alpha_type") == "SUPER"]
        others = [r for r in rows if r.get("alpha_type") != "SUPER"]
        by_scope: Dict[Tuple[str, Any], List[Dict[str, Any]]] = defaultdict(list)
        for r in supers:
            by_scope[(r.get("region"), r.get("delay"))].append(r)
        keep: List[Dict[str, Any]] = []
        drop: List[Dict[str, Any]] = []
        print(f"[super-top] SUPER 按 inv 保留**每 scope** top{a.super_top_n}（共 "
              f"{len(by_scope)} 个 scope）:", file=sys.stderr)
        for k in sorted(by_scope, key=lambda k: (str(k[0]), str(k[1]))):
            grp = sorted(by_scope[k],
                         key=lambda r: (r.get("investability_sharpe") or 0.0),
                         reverse=True)
            kept = grp[:a.super_top_n]
            keep.extend(kept)
            drop.extend(grp[a.super_top_n:])
            print(f"   [{k[0]}D{k[1]}] {len(grp)} -> {len(kept)} 颗", file=sys.stderr)
            for r in kept:
                print(f"      + {r['alpha_id']}  inv={r.get('investability_sharpe'):.3f}"
                      f"  IS={r.get('sharpe')}", file=sys.stderr)
            for r in grp[a.super_top_n:]:
                print(f"      x {r['alpha_id']}  inv={r.get('investability_sharpe'):.3f}"
                      f"  IS={r.get('sharpe')}", file=sys.stderr)
        rows = others + keep
        print(f"[super-top] 合计: {len(supers)} -> {len(keep)} 颗（剔除 {len(drop)} 颗）",
              file=sys.stderr)
        for r in keep:
            print(f"   + {r['alpha_id']}  {r['region']}D{r.get('delay')}  "
                  f"inv={r.get('investability_sharpe'):.3f}  IS={r.get('sharpe')}", file=sys.stderr)
        for r in drop:
            print(f"   x {r['alpha_id']}  {r['region']}D{r.get('delay')}  "
                  f"inv={r.get('investability_sharpe'):.3f}  IS={r.get('sharpe')}", file=sys.stderr)

    if a.sync and a.source != "platform":
        st = sync_os()
        print(f"[sync] 结果: {st}", file=sys.stderr)
        # sync 后重新读（OS 指标已落库），并刷新快照（仍为过滤前全量）
        rows = load_candidates(a.region)
        all_rows = list(rows)
        if PROD_POLICY == "exclude":
            # 与主线 exclude 一致：None-prod 也一并保守剔除
            rows = [r for r in rows if not (r.get("prod") is None or r["prod"] >= PROD_MAX)]

    scopes = build_scopes(rows)
    _smp = a.super_max_pts if (a.super_max_pts and a.super_max_pts > 0) else None
    plan = build_plan(scopes, per_scope_budget=a.per_scope_budget,
                      super_budget_share=a.super_budget_share,
                      super_max_pts=_smp)
    save_plan(plan)
    # met 标记仅用于展示；build_plan 内部已决定退化
    eligible = sum(1 for (reg, d), al in scopes.items() if len(al) >= MIN_PER_SCOPE)
    met = eligible >= MIN_SCOPES
    print_review(rows, scopes, plan, met)

    if not a.apply:
        print("\n[review-only] 已写 plan ->", PLAN_PATH, "；加 --apply 写入平台。")
        return 0

    # ---- apply 阶段：PATCH + 自动 replan 闭环 ----
    # ★ 2026-10-13：checkpoint 是**断点续跑**机制（用户铁律：脚本必须可 resume），不能删。
    #   副作用：已分配过的 alpha 在 apply_plan 里被 `if aid in applied: skip` 跳过，
    #   ⇒ 重跑分配时这些 alpha 的点数**不会更新**（仍保持上一次的值）。
    #   故提供 --force-repatch 显式清 checkpoint；不清则只补新 alpha、不动旧点数。
    if a.force_repatch and not a.dry_run:
        save_ckpt(set())
        print("[force-repatch] 已清 checkpoint，本轮强制重新 PATCH 全部 alpha（更新点数）",
              file=sys.stderr)
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
