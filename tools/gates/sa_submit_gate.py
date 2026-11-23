# -*- coding: utf-8 -*-
r"""SA 提交前双评估闸（2026-11-22 用户明令）。

用户原话：「后面提交 sa 前都要评估它能拿到的 base 值，提交后对 sa 池是否有正向增益」

## 本工具能算什么、不能算什么（先读，别当黑箱）

| 项 | 可算性 | 依据 |
|---|---|---|
| base **档位**（553 / 三5 / 双5 / BELOW） | ✅ 确定 | SA 自身 S/F/PC，社区实证阶梯 |
| base **乘数链** | ✅ 精确 | `(Theme + Pyramid − 1) × (1 + OsmosisRank)` |
| base **金额** | ⚠️ 区间，且**必须按账户标定** | `--profile self`（默认）= 本账户 58 颗实证，SA 增量 $0–0.5/日 |
| SA 池 **均值方向** | ✅ 确定 | `Δmean = (x − mean) / (n+1)` |
| SA 池 **均值幅度** | ⚠️ 极小 | n=58 ⇒ 即使 x=0 也只降 0.0107 ⇒ 增益是**方向性**不是量级性 |
| 池 **组合 Sharpe 增益** | ❌ 不可算 | 需池内全量 PnL 协方差矩阵，平台不提供 |

> ⚠ **本账户最重要的实证（`11_sa_maxbase_strategy.md` §9.3）**：58 颗 SA，
> 含 OS 0.75 当天的双5（`pwa8mYvV` 5.05/5.18/.6548）与最强双5（`KPg60XNp` 5.96/7.50/.5475），
> **日 base 从未突破 $1.94** ⇒ 论坛「553 吃满 $60」在本账户**未兑现**。
> 故默认 `--profile self` 给"不可分辨"区间，论坛锚点须显式 `--profile community` 才启用。

## 判据来源（全部可追溯）

- 档位阶梯：论坛 post 45145860787095（VF 0.96 实测）
  「双5 → 三5 → 553；OS<0.5 时只有 553 才能 50+，OS 0.9+ 时双5 也能 50+」
- RA/SA 独立计费、单日上限各 $60：论坛 post 45116178392727（81 天实测）
- 最终乘数公式：同上帖 9 例单交对照（`(Theme+Pyramid−1)×(1+OS)`）
- 池均值指标口径：`get_leaderboard().superAlphaMeanProdCorrelation`
  / `superAlphaMeanSelfCorrelation` / `superAlphaSubmissionsCount`
- 孪生封死线：ACTIVE 后同骨架变体 self≥0.99 全族死（本仓台账实证）

## 判定分层（顺序不可换）

1. **REDLINE**（硬拦，退出码 3）：`prod ≥ 0.70` 或 `checks FAIL` 或 `mutual_corr ≥ 0.70`
2. **★边际论前置**（退出码 1）：`--perf-comp-delta < 0`（本 SA 拉低地区组合）⇒ HOLD，
   即使档位达标。**看边际不看单件绝对**：fit1.03/self.1 提升组合 > fit1.98/self.68 降低组合（论坛实证）
3. **UNDETERMINED**（退出码 4）：prod / self / mutual 任一缺失
4. **BELOW_TIER**（退出码 1）：S<5 或 F<5 ⇒ 档位不到双5 ⇒ base 量级 ≤$3，不建议交
5. **GO**（退出码 0）：档位 ≥ 双5 ∧ 池双向改善（PC↓ self↓）
6. **HOLD**（退出码 1）：档位达标但池改善只满足一项，或乘数过低（<4）

## 官方收入框架信号（2026-11-23 取证，全部可选、不阻断）

- `AggregateFactor = f(QualityScaled + QuantityScaled, SelfGrowth, ValueFactor)`；Daily Limit=前4 RA+前1 SA。
- **VF 主导**（`--vf`）：VF 0.5→$1.2–6｜0.97→$35｜0.99→$60–80｜1.0→$104.91（0.02 差近翻倍＝非线性台阶）。
  VF<0.90 时打印「先养 VF」提示——SA 的 PC/S/F 优化是次要杠杆。
- **SelfGrowth**（`--subs-7d` / `--quality-trend`）：官方 `f(CurQty,CurQual,PastQty,PastQual)`，
  断更或质量环比倒退 ⇒ 受损。只是提示，不阻断。
- **Quality 六维**（`--quality-dims`）：MCorrelation/MRegion/MUniverse/MFitness/MDelay/MTheme（theme 是六维之一）。
  只披露覆盖缺口，MRegion/MUniverse/MDelay 属账户区池选择、非单颗 SA 可调。

## 用法

    # 单颗快速评估（数值直接给）
    $PY tools/gates/sa_submit_gate.py --alpha gJaaER8K \
        --sharpe 5.2 --fitness 5.3 --prod 0.5969 --self 0.41 \
        --theme-mult 1.0 --pyramid-mult 1.1 --os-rank 0.85 --vf 0.73

    # 从 get_alpha_details 的 JSON 读指标 + 官方框架四维（边际论/SelfGrowth/六维/VF）
    $PY tools/gates/sa_submit_gate.py --alpha <id> --details results/sa_detail.json \
        --theme-mult 1.0 --pyramid-mult 1.1 --os-rank 0.85 --vf 0.73 \
        --perf-comp-delta 0.12 --subs-7d 5 --quality-trend up \
        --quality-dims MCorrelation,MFitness,MTheme

    # 批量：JSON 列表，每项含 alpha/sharpe/fitness/prod/self/...
    $PY tools/gates/sa_submit_gate.py --input results/sa_candidates.json \
        --os-rank 0.85 --vf 0.73 --md out.md

退出码：0=GO｜1=HOLD/BELOW_TIER（可交但标注）｜3=BLOCK｜4=UNDETERMINED
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------- 阈值（集中管理）
REDLINE_PROD = 0.70          # 平台红线，无豁免
REDLINE_MUTUAL = 0.70        # 孪生封死线（self 闸）
TIER_S = 5.0                 # 双5 门槛
TIER_F = 5.0
PC_553 = 0.30                # 553 档
PC_35 = 0.50                 # 三5 档
MULT_MIN = 4.0               # 乘数下限：低于此档位再高也吃不到量级
VF_REF = 0.90                # 论坛锚点表的 VF 参照值

# 池基线（调用方应传最新读数；缺省用 2026-11-22 账户实测）
POOL_N_DEFAULT = 58
POOL_PC_DEFAULT = 0.6301
POOL_SELF_DEFAULT = 0.5976

# 金额锚点表 —— **必须按账户标定，禁跨账户搬运**
#
# `self`（默认）：本账户 MT38799 实证锚点，来自 `11_sa_maxbase_strategy.md` §9.3
#   2026-11-16 OS 0.75 + pwa8mYvV 双5(5.05/5.18/.6548) → 当日总 base $1.68
#   2026-11-15 OS 0.10 + KPg60XNp 双5(5.96/7.50/.5475) → 当日总 base $1.75
#   2026-11-03 A1V0eZne(6.39/7.06/.6146)              → 当日总 base $1.59
#   58 颗 SA 全期均值 S4.05/F3.71/PC.6301               → 日 base $1.20–1.94
#   ⇒ 本账户 SA **档位与 OS 均未兑现**，SA 增量估 $0–0.5/日（含 553）
#   故 self 档区间给"不可分辨"下界 0，上界只作方向提示
#
# `community`：论坛多人锚点（post 45145860787095 / 45116178392727 / 44701402752279）
#   其 VF 多在 0.89–0.96、账户历史不同 ⇒ 只能作外部上限参考
ANCHOR = {
    "self": {
        "553": (0.0, 2.0),
        "三5": (0.0, 1.5),
        "双5": (0.0, 1.0),
        "BELOW": (0.0, 0.2),
    },
    "community": {
        "553": (40.0, 60.0),
        "三5": (18.0, 40.0),
        "双5": (8.0, 20.0),
        "BELOW": (0.5, 3.0),
    },
}

VERDICT_ORDER = {"REDLINE": 0, "UNDETERMINED": 1, "BELOW_TIER": 2, "HOLD": 3, "GO": 4}

# ---------------------------------------------------------------- 官方收入框架（2026-11-23 取证落地）
# India/Kenya 2022 Base Fee 文档 + 三篇顾问论坛实证。四项均**不改档位/金额锚点**，
# 只在 evaluate 里附加 signal / 在边际为负时前置压为 HOLD（新参数缺省时零影响）。
QUALITY_DIMS = ("MCorrelation", "MRegion", "MUniverse", "MFitness", "MDelay", "MTheme")
VF_DOMINANT = 0.90              # 论坛：VF 0.97→$35/日、0.99→$60–80（0.02 差近翻倍＝非线性台阶）
VF_PEAK = 0.99
VF_HIGH = 0.97
SELF_GROWTH_MIN_SUBS = 1        # 近 7 日提交数下限：0 ⇒ SelfGrowth 掉（f(CurQty,...,PastQty,...)）
PERF_COMP_PRIMARY = True        # performance_comparison 边际论前置为首要判据（看边际不看单件绝对）


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def tier_of(S: float | None, F: float | None, PC: float | None) -> str:
    """SA 自身三指标定档。PC 未知 ⇒ 最高只能判到 双5 的下一档，标注 UNKNOWN_PC。"""
    if S is None or F is None or S < TIER_S or F < TIER_F:
        return "BELOW"
    if PC is None:
        return "双5"
    if PC < PC_553:
        return "553"
    if PC < PC_35:
        return "三5"
    return "双5"


def final_mult(theme: float | None, pyramid: float | None, os_rank: float | None) -> float | None:
    """(Theme + Pyramid − 1) × (1 + OsmosisRank)。任一项缺失 ⇒ None。"""
    if theme is None or pyramid is None or os_rank is None:
        return None
    return (theme + pyramid - 1.0) * (1.0 + os_rank)


def base_band(tier: str, mult: float | None, vf: float | None,
              profile: str = "self") -> tuple[float, float, str]:
    """档位锚点 × VF 缩放。返回 (low, high, note)。**只作量级判断，不作报价。**"""
    lo, hi = ANCHOR[profile][tier]
    tag = "本账户实证" if profile == "self" else "论坛外部锚点"
    note = f"[{tag}]"
    if profile == "self":
        # 本账户 SA 增量不可分辨，乘数/VF 缩放无意义，只作方向
        if tier == "BELOW":
            note += " 档位未达双5 ⇒ 预期无增量"
        else:
            note += " 58 颗实证未兑现档位差异 ⇒ SA 增量 $0–0.5/日，区间仅方向上界"
        return lo, hi, note

    scale = 1.0
    if vf is not None:
        scale *= max(0.3, min(1.6, vf / VF_REF))
        note += f" VF {vf:.2f} 缩放 ×{scale:.2f}"
    else:
        note += " VF 未知 ⇒ 未缩放，上限可能高估 2–3 倍（补 --vf 再读）"
    if mult is not None:
        ms = max(0.4, min(1.8, mult / 6.0))
        scale *= ms
        note += f"｜乘数 {mult:.2f}/6.0 缩放 ×{ms:.2f}"
    if tier == "BELOW":
        note += "｜档位未达双5，金额不随乘数放大"
        return lo, hi, note
    return lo * scale, hi * scale, note


def vf_signal(vf: float | None) -> dict:
    """VF 主导信号（2026-11-23 取证）：VF 是收入唯一强相关变量，非线性台阶。
    vf<0.90 ⇒ SA 档位收益被压制，提示「先养 VF 再谈 SA 档位」。不阻断。"""
    if vf is None:
        return {"level": "UNKNOWN", "note": "VF 未知 ⇒ 无法判断 SA 收益天花板（补 --vf）"}
    if vf >= VF_PEAK:
        lvl, note = "PEAK", f"VF {vf:.2f} ≥ {VF_PEAK} ⇒ SA 收割窗口（论坛 $60–100/日）"
    elif vf >= VF_HIGH:
        lvl, note = "HIGH", f"VF {vf:.2f} ≥ {VF_HIGH} ⇒ SA 稳定赚钱区（论坛 ~$35/日）"
    elif vf >= VF_DOMINANT:
        lvl, note = "OK", f"VF {vf:.2f} ≥ {VF_DOMINANT} ⇒ 达门槛"
    else:
        lvl, note = "LOW", (f"VF {vf:.2f} < {VF_DOMINANT} ⇒ **SA 档位收益被 VF 压制**，"
                           "边际杠杆在 RA 数量×质量×地区均衡，不在 SA 的 PC/S/F")
    return {"level": lvl, "value": vf, "note": note}


def self_growth_signal(subs_7d: int | None, quality_trend: str | None) -> dict:
    """SelfGrowthFactor 代理（官方 f(CurQty,CurQual,PastQty,PastQual)）：断更或质量倒退 ⇒ 掉。
    两个入参都可选；缺任一则 UNKNOWN。不阻断，只提示。"""
    if subs_7d is None and quality_trend is None:
        return {"level": "UNKNOWN", "note": "未传近7日提交数/质量趋势 ⇒ SelfGrowth 未评估"}
    bits, bad = [], []
    if subs_7d is not None:
        bits.append(f"近7日提交 {subs_7d}")
        if subs_7d < SELF_GROWTH_MIN_SUBS:
            bad.append("断更")
    if quality_trend is not None:
        bits.append(f"质量趋势 {quality_trend}")
        if str(quality_trend).lower() in ("down", "downward", "倒退", "下降"):
            bad.append("质量环比倒退")
    if bad:
        return {"level": "REGRESS", "note": "＋".join(bits) + " ⇒ **SelfGrowth 受损**（" + "、".join(bad) + "）"}
    return {"level": "OK", "note": "＋".join(bits) + " ⇒ SelfGrowth 稳定"}


def quality_dim_coverage(covered: str | None) -> dict:
    """官方 Quality Factor 六维覆盖信息（MCorrelation/MRegion/MUniverse/MFitness/MDelay/MTheme）。
    --quality-dims 传逗号分隔的已覆盖维度名；只做披露，不阻断、不改档位。"""
    if not covered:
        return {"covered": [], "missing": list(QUALITY_DIMS), "note": "未传 --quality-dims ⇒ 六维覆盖未披露"}
    have = {x.strip() for x in covered.split(",") if x.strip()}
    missing = [d for d in QUALITY_DIMS if d not in have]
    note = f"覆盖 {len(QUALITY_DIMS)-len(missing)}/{len(QUALITY_DIMS)} 维"
    if missing:
        note += f"；缺口 {','.join(missing)}（MRegion/MUniverse/MDelay 属账户区池选择，非单颗 SA 可调）"
    return {"covered": [d for d in QUALITY_DIMS if d in have], "missing": missing, "note": note}


def pool_effect(PC: float | None, SELF: float | None,
                n: int, mean_pc: float, mean_self: float) -> dict:
    """池均值方向与幅度。Δmean = (x − mean)/(n+1)。"""
    out: dict = {"n": n, "mean_pc": mean_pc, "mean_self": mean_self}
    if PC is not None:
        out["d_pc"] = (PC - mean_pc) / (n + 1)
        out["pc_better"] = PC < mean_pc
    if SELF is not None:
        out["d_self"] = (SELF - mean_self) / (n + 1)
        out["self_better"] = SELF < mean_self
    return out


def evaluate(row: dict, pool: dict, mult_inputs: dict, profile: str = "self",
             perf_comp_delta: float | None = None, subs_7d: int | None = None,
             quality_trend: str | None = None, quality_dims: str | None = None) -> dict:
    aid = row.get("alpha") or row.get("id") or "-"
    S, F = _f(row.get("sharpe")), _f(row.get("fitness"))
    PC, SELF = _f(row.get("prod")), _f(row.get("self"))
    mutual = _f(row.get("mutual"))
    fails = row.get("fails") or []

    tier = tier_of(S, F, PC)
    mult = final_mult(mult_inputs.get("theme"), mult_inputs.get("pyramid"), mult_inputs.get("os_rank"))
    lo, hi, note = base_band(tier, mult, mult_inputs.get("vf"), profile)
    pe = pool_effect(PC, SELF, pool["n"], pool["mean_pc"], pool["mean_self"])

    # 官方框架信号（全部可选入参；不传 ⇒ UNKNOWN，不影响任何 verdict）
    vsig = vf_signal(mult_inputs.get("vf"))
    gsig = self_growth_signal(subs_7d, quality_trend)
    qdim = quality_dim_coverage(quality_dims)
    pcd = _f(perf_comp_delta) if perf_comp_delta is not None else None

    # ---- 判定（顺序不可换）----
    # ★ 2026-11-23 前置：performance_comparison 边际论为首要判据（看边际不看单件绝对）。
    #   边际为负 ⇒ 即使档位达标也压为 HOLD；此闸在 REDLINE 之后、其余之前，
    #   仅在显式传 --perf-comp-delta<0 时生效（不传零影响，向后兼容）。
    if fails:
        verdict, why = "REDLINE", f"IS checks FAIL: {','.join(map(str, list(fails)[:3]))}"
    elif PC is not None and PC >= REDLINE_PROD:
        verdict, why = "REDLINE", f"prod {PC:.4f} ≥ {REDLINE_PROD}（平台红线，无豁免）"
    elif mutual is not None and mutual >= REDLINE_MUTUAL:
        verdict, why = "REDLINE", f"mutual {mutual:.4f} ≥ {REDLINE_MUTUAL}（孪生封死）"
    elif PERF_COMP_PRIMARY and pcd is not None and pcd < 0:
        verdict, why = "HOLD", (f"**组合边际为负**（Δ地区组合 {pcd:+.3f}）⇒ 前置拦："
                                "单件 S/F 再高，拉低地区组合则 VF 受损（论坛边际论）")
    elif PC is None or SELF is None or mutual is None:
        missing = [k for k, v in (("prod", PC), ("self", SELF), ("mutual", mutual)) if v is None]
        verdict, why = "UNDETERMINED", f"缺 {','.join(missing)}（先跑 check_correlation / compute_mutual_correlation）"
    elif tier == "BELOW":
        verdict, why = "BELOW_TIER", f"S {S:.2f}/F {F:.2f} 未达双5（S≥5 ∧ F≥5）⇒ base 量级 ≤$3"
    else:
        gain = pe.get("pc_better", False) + pe.get("self_better", False)
        if gain >= 2 and (mult is None or mult >= MULT_MIN):
            verdict, why = "GO", f"{tier} 档 ∧ 池双向改善（PC {PC:.4f}<{pool['mean_pc']:.4f}, self {SELF:.4f}<{pool['mean_self']:.4f}）"
        else:
            bits = []
            if gain < 2:
                bad = []
                if not pe.get("pc_better", False):
                    bad.append(f"PC {PC:.4f} ≥ 池均值 {pool['mean_pc']:.4f}")
                if not pe.get("self_better", False):
                    bad.append(f"self {SELF:.4f} ≥ 池均值 {pool['mean_self']:.4f}")
                bits.append("池改善不足（" + "；".join(bad) + "）")
            if mult is not None and mult < MULT_MIN:
                bits.append(f"乘数 {mult:.2f} < {MULT_MIN}")
            verdict, why = "HOLD", f"{tier} 档但 " + "＋".join(bits)

    return {
        "alpha": aid, "S": S, "F": F, "prod": PC, "self": SELF, "mutual": mutual,
        "tier": tier, "mult": mult, "base_low": round(lo, 2), "base_high": round(hi, 2),
        "base_note": note, "pool": pe, "verdict": verdict, "reason": why,
        "vf_signal": vsig, "self_growth": gsig, "quality_dims": qdim,
        "perf_comp_delta": pcd,
    }


def render_md(results: list[dict]) -> str:
    lines = [
        "| id | S | F | prod | self | mutual | 档位 | 乘数 | base 区间 | Δ池PC | Δ池self | 判定 | 依据 |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        fmt = lambda v, n=2: "-" if v is None else f"{v:.{n}f}"
        pe = r["pool"]
        lines.append(
            f"| `{r['alpha']}` | {fmt(r['S'])} | {fmt(r['F'])} | {fmt(r['prod'], 4)} | {fmt(r['self'], 4)} | "
            f"{fmt(r['mutual'], 4)} | **{r['tier']}** | {fmt(r['mult'])} | "
            f"${r['base_low']:.1f}–{r['base_high']:.1f} | "
            f"{fmt(pe.get('d_pc'), 5)} | {fmt(pe.get('d_self'), 5)} | **{r['verdict']}** | {r['reason']} |"
        )
    return "\n".join(lines)


def _row_from_details(payload: dict, aid: str) -> dict:
    """兼容 get_alpha_details 原始返回。"""
    j = payload.get("is") or payload
    m = j.get("metrics") or {}
    checks = payload.get("is", {}).get("checks") or []
    fails = [c.get("name") for c in checks if isinstance(c, dict) and c.get("result") == "FAIL"]
    return {
        "alpha": payload.get("id") or aid,
        "sharpe": m.get("sharpe"),
        "fitness": m.get("fitness"),
        "prod": (payload.get("is", {}).get("prodCorrelation")
                 or payload.get("prod_correlation") or payload.get("prod")),
        "self": (m.get("selfCorrelation") or payload.get("self_correlation") or payload.get("self")),
        "mutual": payload.get("mutual"),
        "fails": fails,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="SA 提交前双评估（base 档位 + SA 池增益）")
    ap.add_argument("--alpha", help="alpha id（单颗）")
    ap.add_argument("--input", help="批量 JSON：list[dict] 或 batch_get_alpha_metrics 返回")
    ap.add_argument("--details", help="get_alpha_details 原始 JSON（配合 --alpha）")
    ap.add_argument("--sharpe"); ap.add_argument("--fitness")
    ap.add_argument("--prod"); ap.add_argument("--self", dest="self_corr")
    ap.add_argument("--mutual", help="与 SA 池的最大互相关（compute_mutual_correlation）")
    ap.add_argument("--theme-mult", help="当期主题倍率；无主题填 1.0")
    ap.add_argument("--pyramid-mult", help="塔倍率（混类取木桶短板）")
    ap.add_argument("--os-rank", help="Daily Osmosis Rank")
    ap.add_argument("--vf", help="Value Factor（金额缩放 + VF 主导信号用）")
    ap.add_argument("--perf-comp-delta", type=float,
                    help="★边际论首要判据：本 SA 对所在地区组合的边际 ΔSharpe/Fitness（performance_comparison）。<0 前置压 HOLD")
    ap.add_argument("--subs-7d", type=int, help="近 7 日提交数（SelfGrowth 代理，断更⇒受损）")
    ap.add_argument("--quality-trend", help="质量环比趋势 up/down/flat（SelfGrowth 代理，down⇒受损）")
    ap.add_argument("--quality-dims", help="已覆盖的官方六维，逗号分隔：MCorrelation,MRegion,MUniverse,MFitness,MDelay,MTheme（只披露不阻断）")
    ap.add_argument("--pool-n", type=int, default=POOL_N_DEFAULT)
    ap.add_argument("--pool-pc", type=float, default=POOL_PC_DEFAULT)
    ap.add_argument("--pool-self", type=float, default=POOL_SELF_DEFAULT)
    ap.add_argument("--profile", choices=("self", "community"), default="self",
                    help="金额锚点：self=本账户实证（默认，SA 增量 $0–0.5）｜community=论坛外部上限")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--md", dest="md_out")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    pool = {"n": args.pool_n, "mean_pc": args.pool_pc, "mean_self": args.pool_self}
    mult_inputs = {
        "theme": _f(args.theme_mult), "pyramid": _f(args.pyramid_mult),
        "os_rank": _f(args.os_rank), "vf": _f(args.vf),
    }

    rows: list[dict] = []
    if args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        rows = payload.get("results") if isinstance(payload, dict) else payload
        rows = [r for r in (rows or []) if isinstance(r, dict)]
    elif args.alpha:
        if args.details:
            rows = [_row_from_details(json.loads(Path(args.details).read_text(encoding="utf-8")), args.alpha)]
        else:
            rows = [{
                "alpha": args.alpha, "sharpe": args.sharpe, "fitness": args.fitness,
                "prod": args.prod, "self": args.self_corr, "mutual": args.mutual,
            }]
    else:
        ap.error("需要 --alpha 或 --input")

    # CLI 显式值覆盖批量行
    if len(rows) == 1:
        for k, v in (("sharpe", args.sharpe), ("fitness", args.fitness), ("prod", args.prod),
                     ("self", args.self_corr), ("mutual", args.mutual)):
            if v is not None:
                rows[0][k] = v

    results = [evaluate(r, pool, mult_inputs, args.profile,
                        args.perf_comp_delta, args.subs_7d, args.quality_trend, args.quality_dims)
               for r in rows]
    results.sort(key=lambda r: (VERDICT_ORDER[r["verdict"]], -(r["S"] or 0)))

    print("判据: REDLINE prod>=.70|mutual>=.70|checks FAIL ｜ ★边际论首要判据 perf-comp-delta<0⇒HOLD ｜ "
          f"档位 553(PC<.30)/三5(PC<.50)/双5 ｜ GO=档位≥双5 ∧ 池PC↓self↓ ∧ 乘数≥{MULT_MIN:g}")
    print(f"池基线: n={pool['n']} meanPC={pool['mean_pc']:.4f} meanSelf={pool['mean_self']:.4f}")
    for r in results:
        mult_s = "-" if r["mult"] is None else f"{r['mult']:.2f}"
        print(f"[{r['verdict']:12}] {r['alpha']:12} {r['tier']:5} mult={mult_s} "
              f"base=${r['base_low']:.1f}-{r['base_high']:.1f}  {r['reason']}")
        print(f"{'':15}↳ {r['base_note']}")
        print(f"{'':15}↳ VF[{r['vf_signal']['level']}] {r['vf_signal']['note']}")
        if r["vf_signal"]["level"] == "LOW":
            print(f"{'':15}↳ ★优先级：先养 VF（RA 数量×质量×地区均衡），SA 档位优化是次要杠杆")
        print(f"{'':15}↳ SelfGrowth[{r['self_growth']['level']}] {r['self_growth']['note']}")
        print(f"{'':15}↳ Quality六维 {r['quality_dims']['note']}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    md = render_md(results)
    if args.md_out:
        Path(args.md_out).write_text(md + "\n", encoding="utf-8")

    worst = min(VERDICT_ORDER[r["verdict"]] for r in results) if results else 1
    return {0: 3, 1: 4, 2: 1, 3: 1, 4: 0}[worst]


if __name__ == "__main__":
    raise SystemExit(main())
