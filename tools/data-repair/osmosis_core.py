# -*- coding: utf-8 -*-
"""osmosis_core.py — Osmosis 分配共享层（数据 / 质量 / 写平台）。

2026-11-05 由 `osmosis_allocate.py`（v1，已归档到 `attic/osmosis_v1_20261105/`）
抽出的**非分配逻辑**部分，供 `osmosis_plan_v2.py` 与只读诊断工具复用：

- 常量（TOTAL_BUDGET / MIN_PER_SCOPE / 投资约束回退系数 / prod 策略）
- `load_candidates_platform()`：平台 OS 池 → 统一行结构（含 inv 覆盖映射合并）
- `build_scopes()`：按 (region, delay) 分组
- `prod_penalty()` / `quality()`：质量分（inv 优先，缺失按 maxTrade 决定是否折算）
- `load_ckpt()` / `save_ckpt()`：断点续跑
- `apply_plan()` / `zero_others()`：PATCH 点数 / 以 null 清零非计划 alpha

⚠ **不含任何分配算法**（v1 的 `build_plan` / `replan` 已删除）。分配一律走
`osmosis_plan_v2.py`：相关性剪枝 + inv 衰减闸 + 每 scope ≤20 颗 + SA/RA 分池 + 单颗封顶。

⚠ v1 文档里「SuperAlpha 不可分配」的结论是**错的**：平台自 2026-10 起支持给 SUPER 配点，
本仓库从 2026-10-21 起把 SUPER 纳入统一管理（SA 22% 预算 + 每 scope top4 + 单颗 ≤10k）。
"""
from __future__ import annotations

import asyncio
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --- 区域权重口径（单源登记；分配脚本内禁止写 region 字面量比较）---
# USA 是唯一有真实 OS 池的区域，权重改用 os.sharpe；其余区用 quality(inv)。
# 消费方：osmosis_plan_v2.plan_scope / base_weight。
OS_SHARPE_REGIONS = frozenset({"USA"})

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
# investability 覆盖映射（2026-11-02）：maxTrade=ON 的 alpha 平台不下发
# is.investabilityConstrained（约束已内嵌进 is.*），分配时用同表达式 + OFF 的
# 孪生 IS 模拟实测 inv 补齐。文件存在即自动加载，避免每晚定时任务漏传参。
INV_OVERRIDE_PATH = os.path.join(RESULTS, "osmosis_inv_override.json")
# main() 按 --inv-override 注入；None = 用缺省路径（文件存在即自动加载）。
INV_OVERRIDE_SRC: Optional[str] = None

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
# investability 覆盖映射（maxTrade=ON 的 alpha 用孪生实测 inv 补齐）
# --------------------------------------------------------------------------- #
def load_inv_override(path: Optional[str] = None) -> Dict[str, float]:
    """读取 `{alpha_id: investability_sharpe}` 覆盖映射（键 `_` 开头视为元数据跳过）。

    支持两种值写法：裸数值，或 `{"investability_sharpe": value, ...}` 子对象。
    文件不存在/读取失败一律返回空 dict（静默降级，不阻断分配）。
    """
    p = path or INV_OVERRIDE_SRC or INV_OVERRIDE_PATH
    if not p or not os.path.exists(p):
        return {}
    try:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"[inv-override] 读取失败({p}): {e}", file=sys.stderr)
        return {}
    out: Dict[str, float] = {}
    for k, v in (data or {}).items():
        if not isinstance(k, str) or k.startswith("_"):
            continue
        if isinstance(v, dict):
            v = v.get("investability_sharpe")
        if v is None:
            continue
        try:
            out[k] = float(v)
        except (TypeError, ValueError):
            print(f"[inv-override] 跳过非法值 {k}={v!r}", file=sys.stderr)
    return out


# --------------------------------------------------------------------------- #
# DB 读：范围覆盖（只读；必须走 `wqb.db_conn` 规范工厂，禁裸 sqlite3.connect）
def _apply_inv_override(rows: List[Dict[str, Any]],
                        path: Optional[str] = None) -> int:
    """把覆盖映射写入行的 investability_sharpe（仅覆盖非 None 的映射值）。返回命中数。"""
    ov = load_inv_override(path)
    if not ov:
        return 0
    n = 0
    for r in rows:
        v = ov.get(str(r.get("alpha_id")))
        if v is not None:
            r["investability_sharpe"] = v
            n += 1
    if n:
        print(f"[inv-override] 命中 {n} 颗 (来源 {path or INV_OVERRIDE_PATH})", file=sys.stderr)
    return n


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
            # maxTrade：ON 时 is.sharpe 已内嵌换手帽约束（RULES.md §N），
            # quality() 据此决定缺失 inv 时是否还需乘 INVEST_FALLBACK。
            "max_trade": st.get("maxTrade"),
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
    _apply_inv_override(out)
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
        # ★ maxTrade=ON 的 alpha，其 IS sharpe 已内嵌换手帽约束（RULES.md §N）
        #   ⇒ 不应再乘 INVEST_FALLBACK，否则是重复打折（实测 15 颗 ON 的 S 与
        #   同表达式 OFF 孪生的 inv 多数相等，如 2.28=2.28 / 2.68=2.68）。
        #   OFF 且无 inv 者仍按 INVEST_FALLBACK 保守折算。
        fb = 1.0 if a.get("max_trade") == "ON" else INVEST_FALLBACK
        v = float(base) * fb
    to = a.get("turnover") or 0
    pen = 0.6 if to < 0.05 else 1.0
    q = max(v, 0.0) * pen
    return q * prod_penalty(a.get("prod"), PROD_POLICY, PROD_MAX)


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


