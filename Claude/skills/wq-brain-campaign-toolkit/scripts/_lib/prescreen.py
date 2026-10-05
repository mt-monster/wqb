# -*- coding: utf-8 -*-
"""S4 预筛唯一口径（2026-10-02 P1）。

背景：同一批候选此前存在**三套互不一致**的预筛判据（2026-10-02 实测）：
  ① `tools/campaign_intel.py s4-prescreen`（在线，打平台 `get_alpha_details`）
     硬闸 = sharpe≥1.58 / fitness≥1.0 / 2Y≥1.58 / prod≤0.7 / self≤0.7 + tvr∈[0.04,0.40]
  ② `src/wqb/workflow/nodes/auto_review.py _prescreen`（离线，只读 backtest_results）
     同硬闸但**无 prod/self**（该表无这两列）+ tvr∈[0.04,0.40]
  ③ `review_wave.walls()` 的 sharpe_min **取各区 thresholds.json**（USA=1.25，其余 1.58）

后果：GBR `s2_institutions6_d1` 77 条在 ② 口径下**全判 REJECT**，在 ③ 口径下会产出候选；
同一批数据三种结论。更糟的是 ①② 均用 `x or 0` 把**指标缺失当 0**（全库 1200 行
`two_year_sharpe IS NULL`，其中 222 行 sharpe≥1.58 且 fitness≥1.0 被静默判死），
而 ③ 的 `walls()` 同列缺失走 `*_UNKNOWN`（不判败）——**方向相反**。

本模块把口径收敛为一处，规则：
  - **阈值可注入**：`thresholds` 传入即用（各区差异化）；不传用 DEFAULT。
  - **NULL 不判败**：任一关键指标缺失 → 该闸记 `*_UNKNOWN`，走 REVIEW 而非 REJECT
    （与 `review_wave.walls()` 同语义）。
  - **prod/self 可选**：离线场景（表里没有）传 None，不参与判定，但**不因此判败**。

## 与 `review_wave.passes()` 的边界（2026-10-02 定案，勿合并）

两者**语义不同，不得互相替代**：
  - 本模块 = **进场分层**（READY/REVIEW/REJECT），判据是"够不够格进评审链"，
    看 sharpe/fitness/2Y/prod/self/turnover；
  - `review_wave.passes()` = **达标判定**（是否过全部评审闸），除上述外还查
    `margin > margin_min*1e4`、`not failed_checks`、`not rn_exposure`。

强行合并会改变 `review_wave` 语义（它已被 `pipeline.stage_review` 共用，是"达标"的
唯一权威）。故口径收敛目标 = **两处**：① 本模块（分层，三处调用方统一）；
② `review_wave.passes/walls`（达标，本已统一）。
"""
from __future__ import annotations

#: 缺省硬闸（与平台提交层一致；各区可覆盖）。
#: 注意 sharpe_min 在 review_wave 走 thresholds.json（USA=1.25），本缺省 1.58 是
#: ELIGIBILITY 口径（judge/s4-prescreen 用的平台线），调用方按场景传 override。
DEFAULT_THRESHOLDS = {
    "sharpe_min": 1.58,
    "fitness_min": 1.0,
    "two_year_min": 1.58,
    "prod_corr_max": 0.7,
    "self_corr_max": 0.7,
    "turnover_min": 0.04,
    "turnover_max": 0.40,
}

#: REVIEW 兜底线：无一条硬闸通过时，够这些线即留观（否则 REJECT）。
REVIEW_FLOOR = {"sharpe": 1.0, "fitness": 0.5}

READY, REVIEW, REJECT = "READY", "REVIEW", "REJECT"


def _f(v):
    """安全转 float；None / 非数值 -> None（**不**转 0——0 会把缺失误判为不达标）。"""
    if v is None or isinstance(v, bool):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def prescreen_row(row, thresholds=None):
    """单行分层（纯函数，单测主入口）。返回 (tier, reasons)：

      tier ∈ {READY, REVIEW, REJECT}
      reasons = 未通过的闸名列表；缺失指标记 `<闸>_UNKNOWN`（不判败）
    """
    t = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        t.update({k: v for k, v in thresholds.items() if v is not None})
    if not isinstance(row, dict):
        return REJECT, ["NOT_A_ROW"]
    # ERROR 行（回测失败）直接判死——与 auto_review 一致
    if str(row.get("status") or "").upper() == "ERROR":
        return REJECT, ["STATUS_ERROR"]

    sh = _f(row.get("sharpe"))
    fit = _f(row.get("fitness"))
    ty = _f(row.get("two_year_sharpe"))
    tvr = _f(row.get("turnover"))
    prod = _f(row.get("prod_correlation", row.get("prod_corr")))
    selfc = _f(row.get("self_correlation", row.get("self_corr")))

    # sharpe 缺失 => 无任何信号，直接 REJECT（唯一"缺失即死"的闸：没有 sharpe 无从判断）
    if sh is None:
        return REJECT, ["NO_SHARPE"]

    reasons = []
    hard_ok = True

    # ---- sharpe ----
    if sh < t["sharpe_min"]:
        reasons.append("SHARPE")
        hard_ok = False
    # ---- fitness（缺失 -> UNKNOWN，不判败）----
    if fit is None:
        reasons.append("FITNESS_UNKNOWN")
    elif fit < t["fitness_min"]:
        reasons.append("FITNESS")
        hard_ok = False
    # ---- 2Y（缺失 -> UNKNOWN，不判败）----
    if ty is None:
        reasons.append("2Y_UNKNOWN")
    elif ty < t["two_year_min"]:
        reasons.append("2Y")
        hard_ok = False
    # ---- turnover（缺失 -> UNKNOWN；区间外 -> TVR）----
    if tvr is None:
        reasons.append("TVR_UNKNOWN")
    elif not (t["turnover_min"] <= tvr <= t["turnover_max"]):
        reasons.append("TVR")
        hard_ok = False
    # ---- prod / self（可选；仅在**传入了数值**时判）----
    if prod is not None and prod > t["prod_corr_max"]:
        reasons.append("PROD")
        hard_ok = False
    if selfc is not None and selfc > t["self_corr_max"]:
        reasons.append("SELF")
        hard_ok = False

    if hard_ok:
        return READY, reasons
    # 兜底：有信号强度即留观
    if sh >= REVIEW_FLOOR["sharpe"] or (fit is not None and fit >= REVIEW_FLOOR["fitness"]):
        return REVIEW, reasons
    return REJECT, reasons


def prescreen(rows, thresholds=None):
    """批量分层。返回 {"READY": [id...], "REVIEW": [...], "REJECT": [...],
                     "reasons": {id: [闸...]}, "by_id": {id: tier}}（纯函数）。"""
    out = {READY: [], REVIEW: [], REJECT: [], "reasons": {}, "by_id": {}}
    for r in rows or []:
        if not isinstance(r, dict):
            continue
        aid = r.get("alpha_id") or r.get("id")
        tier, reasons = prescreen_row(r, thresholds)
        if aid:
            out[tier].append(aid)
            out["reasons"][aid] = reasons
            out["by_id"][aid] = tier
        else:
            out[tier].append(None)
    return out
