# -*- coding: utf-8 -*-
"""Concept-first priors for GEM idea generation.

The old default dumped two full SKILL.md files and then asked the model to wrap
every field with rank/ts_zscore. That produces templates, not economic signals.
This module keeps the 8-question checklist from feature-engineering, but forces
mechanism → specific field ids → one implementation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATEGORY_PRIMITIVES = {
    "news": [
        "disagreement: primary vs secondary / source A vs source B sentiment",
        "intensity-weighted tone: sentiment scaled by item count or novelty",
        "revision of tone: ts_delta of backfilled sentiment, not the level",
        "skew / polarization: fat-tail of sentiment vs the mean",
    ],
    "analyst": [
        "revision surprise: change in FY1/FY2 vs the stale level",
        "dispersion: disagreement across estimates, not the consensus mean",
        "breadth vs magnitude: how many estimates moved, not how far the mean moved",
        "horizon gap: FY2 minus FY1 as a growth-expectation residual",
    ],
    "model": [
        "industry residual: group_zscore so the factor is not the sector bet",
        "quality minus yield: a slow fundamental residual, not the raw score",
        "invert only when the economic story is crowding or mean-reversion",
        "never ship a lone rank(model_score) as a concept",
    ],
    "pv": [
        "continuation vs reversal: short-horizon pattern vs longer mean",
        "intraday vs overnight: session-specific pressure",
        "volume-conditioned return: price move that happened on unusual volume",
        "this is the fast leg in a 0.4*slow + 0.6*fast mix",
    ],
    "fundamental": [
        "accrual / cash gap: earnings quality, not the earnings level",
        "leverage change: delta of debt or interest burden",
        "efficiency: turnover or incremental margin, not the stock of assets",
        "invert value only as a residual after industry neutralization",
    ],
    "institutions": [
        "owner change vs owner level: flow, not the stale holding",
        "concentration vs breadth of holders",
        "country/industry relative ownership, not a screening flag",
    ],
    "sentiment": [
        "disagreement and intensity, not the raw score",
        "change in sentiment after backfill, not the snapshot",
    ],
    "other": [
        "name the priced risk first; the operator is secondary",
    ],
}


def _load_priors_from_db(region: str | None) -> dict[str, Any]:
    """从 DB 读 priors 快照（assemble_priors --snapshot 写入的 priors_snapshot_<prefix>）。

    GEM 与 toolkit 解耦：不反向 import toolkit，而是通过 run_pipeline 的
    _wqb_campaign_store() 拿 CampaignStore（同一 workspace DB）。读不到/异常 → 返回 {}，
    由 load_priors 降级到 --priors-file。
    """
    if not region:
        return {}
    try:
        # 延迟导入，避免 economic_priors 被 run_pipeline 导入时形成循环依赖
        from run_pipeline import _wqb_campaign_store  # type: ignore
        st = _wqb_campaign_store()
        try:
            rec = st.get_ledger(region, f"priors_snapshot_{region.lower()}")
        finally:
            try:
                st.close()
            except Exception:
                pass
        if isinstance(rec, dict) and (rec.get("wins") or rec.get("dead_ends")):
            return rec
    except Exception:
        pass
    return {}


def load_priors(path: str | Path | None, region: str | None = None) -> dict[str, Any]:
    # 档 B：DB 优先（assemble-priors --snapshot 的单一事实源），文件降级。
    # region 非空且 DB 命中 priors_snapshot_<region> 时，不再依赖中间 JSON 文件。
    if region:
        data = _load_priors_from_db(region)
        if data:
            return data
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def primitives_for(category: str | None) -> list[str]:
    if not category:
        return CATEGORY_PRIMITIVES["other"]
    key = str(category).strip().lower()
    return CATEGORY_PRIMITIVES.get(key, CATEGORY_PRIMITIVES["other"])


def compact_priors_text(priors: dict[str, Any], category: str | None) -> str:
    lines = ["Economic primitives for this category:"]
    for item in primitives_for(category):
        lines.append(f"- {item}")
    
    # 区域特性上下文（新增：帮助 GEM 理解区域约束与机会）
    region_ctx = priors.get("region_context") or {}
    if region_ctx:
        lines.append("")
        lines.append("Region context (apply these constraints to your concepts):")
        if tier := region_ctx.get("tier"):
            lines.append(f"- Region tier: {tier}")
        if settings := region_ctx.get("settings_proven"):
            lines.append(f"- Proven settings: universe={settings.get('universe')}, delay={settings.get('delay')}, neutralization={settings.get('neutralization_default')}")
        if notes := region_ctx.get("key_notes"):
            for note in notes[:4]:  # 取前4条核心经验
                lines.append(f"- {note}")
    
    wins = priors.get("wins") or []
    if wins:
        lines.append("")
        lines.append("Win recipes (copy the MECHANISM, replace the legs with this dataset's fields):")
        for w in wins[:6]:
            if isinstance(w, dict):
                lines.append(f"- {w.get('id') or w.get('what')}: {w.get('key') or w}")
            else:
                lines.append(f"- {w}")
    dead = priors.get("dead_ends") or []
    if dead:
        lines.append("")
        lines.append("Do NOT emit concepts in these dead families:")
        for d in dead[:12]:
            if isinstance(d, dict):
                lines.append(f"- {d.get('family') or d.get('id')}: {d.get('reason') or d.get('rule') or ''}")
            else:
                lines.append(f"- {d}")

    # P3: 骨架×字段族有效性矩阵（正交优先调度）
    matrix = priors.get("skeleton_field_matrix") or {}
    if matrix:
        eff = matrix.get("effective") or []
        mdead = matrix.get("dead") or []
        hints = matrix.get("orthogonal_hints") or []
        if eff:
            lines.append("")
            lines.append("Skeleton x Field-family EFFECTIVE combos (prefer these shapes, swap in THIS dataset's fields):")
            for e in eff[:6]:
                lines.append(f"- [OK] {e.get('skeleton')} x {e.get('field_family')}: {e.get('evidence','')}")
        if mdead:
            lines.append("")
            lines.append("Skeleton x Field-family DEAD combos (structurally blocked, do not retry):")
            for e in mdead[:8]:
                lines.append(f"- [DEAD] {e.get('skeleton')} x {e.get('field_family')}: {e.get('reason','')}")
        if hints:
            lines.append("")
            lines.append("Orthogonal opportunities (proven skeleton, unexplored field family -> low-correlation direction):")
            for h in hints[:4]:
                lines.append(f"- {h}")

    # 2026-09-08：库存实证的条件过闸率（tools/build_gate_prior_from_inventory.py 产出）。
    # 样本源是本账户已回测的历史 alpha（万级），比 campaign registry（百级）大两个数量级，
    # 且同账户同设置习惯，外推风险低。
    gp = priors.get("gate_priors") or {}
    if gp:
        n = gp.get("sample_size")
        lines.append("")
        lines.append(
            f"MEASURED gate-pass rates in this region"
            + (f" (n={n} historical backtests)" if n else "")
            + " — these are measured, not guessed. Prefer the high-rate cells:"
        )
        for label, key in (("neutralization", "by_neutralization"),
                           ("universe", "by_universe"),
                           ("operator-count", "by_operator_count"),
                           ("decay", "by_decay"),
                           ("field family", "by_field_family")):
            cells = gp.get(key) or {}
            if not cells:
                continue
            ranked = sorted(cells.items(),
                            key=lambda kv: -(kv[1].get("rate", 0) if isinstance(kv[1], dict) else 0))
            parts = []
            for name, v in ranked[:6]:
                if isinstance(v, dict):
                    parts.append(f"{name}={v.get('rate', 0):.0%}(n={v.get('n', 0)})")
                else:
                    parts.append(f"{name}={v}")
            if parts:
                lines.append(f"- {label}: " + " | ".join(parts))
        if avoid := gp.get("avoid"):
            lines.append(f"- AVOID (measured near-zero pass rate): {', '.join(avoid[:8])}")
    return "\n".join(lines)


def shape_constraint_rules(data_profile: dict | None) -> str:
    """按数据集形状画像返回模板生成硬约束（形状为主、类别为辅）。

    data_profile: 数据集级画像（来自 field_profile 的 dataset_shape_summary /
                  ledger s1_profile_<dataset>），含 dominant_shape / sparse_ratio /
                  shape_counts。无画像或稠密 spread 主导时返回空串（不注入）。
    """
    if not data_profile:
        return ""
    dominant = data_profile.get("dominant_shape")
    sparse_ratio = float(data_profile.get("sparse_ratio") or 0.0)
    # 稀疏事件型主导（zero_inflated/point_mass 占比 ≥0.4）才注入事件型约束
    if dominant not in ("zero_inflated", "point_mass") and sparse_ratio < 0.4:
        return ""
    return """
SPARSE-EVENT DATASET RULES (本数据集为稀疏事件型, sparse_ratio=%.2f, dominant=%s):
- 事件累加用 ts_sum(signal, window)，禁止 ts_mean —— ts_mean 只在非NaN日求均值，
  会除掉"窗口内事件发生几次"的频率信息（频率本身含"机会型vs例行"信息）。
- nanHandling=ON 会制造"并列质量"：无事件股票填0 → ts_sum后仍为0 → group_rank并列，
  rank 中段是"没有信息"而非"信念中等"。生成模板时考虑
  tail(winsorize(group_rank(ts_sum(...),group),std=2), lower=q, upper=1-q, newval=0.5)
  掐掉中段，只交易有真实事件的两端。winsorize 与 tail 必须成对（先压缩才能让并列块落进带内）。
- 时间窗口必须有经济含义（申报周期/信息半衰期，如季度=66），禁止把窗口当自由参数扫。
- 比值信号优先 流量÷(存量+ε)：ε 是信号定义的一部分（处理清仓/归零），不可省。
- 反向腿(卖出侧)应显著弱于正向腿；若双侧同强，疑似拟合，放弃该概念。
""" % (sparse_ratio, dominant)


def concept_first_rules(data_profile: dict | None = None) -> str:
    base = """You design WorldQuant BRAIN Regular Alpha CONCEPTS, not field×operator wrappers.

For EACH concept, answer in this order before writing a template:
1. Mechanism: who vs who / what surprise / what risk is priced
2. Why it should predict next-period returns in THIS region
3. Exact field ids from the provided list (2–3 fields, not a suffix token)
4. Direction: high value means long or short
5. Failure mode: when this collapses into a crowded residual
6. Expected Exposure: which return driver this captures (value / momentum / quality / lowvol / liquidity / sentiment / growth / profitability / ...)
7. Expected Turnover Band: low (<0.15) / medium (0.15-0.30) / high (>0.30)
8. Expected Coverage Band: narrow (<200 stocks) / medium (200-500) / wide (>500)

FORBIDDEN:
- rank({field}) or ts_zscore({field}, N) as a standalone concept
- "for each field, wrap with an operator"
- placeholders that are only the last token of every field
- inventing field ids
- emitting multiple concepts with the SAME Expected Exposure + same field family (this is pseudo-diversity; backtest will show high correlation)

COMPLEXITY BUDGET (empirical, measured on 859 alphas that PASS the IS hard gates,
drawn from 7608 historical backtests on this account, 2026-09-08):
- Operator-count distribution of PASSING alphas:
  p10=2, p25=3, MEDIAN=5, p75=8, p90=12. 46% of passers use <= 4 operators.
- DEFAULT to 2-5 operators. A single-field atom with one time-series transform
  and one cross-sectional wrapper is a FIRST-CLASS concept, not a placeholder.
  Worked example that passes every hard gate:
      ts_rank(mdl39_price_mo_short_term_component, 1000)
      -> sharpe 2.14 / fitness 1.42 / 2Y 2.75, one field, two operators.
- Of the 8 concepts, AT LEAST 3 MUST use <= 4 operators.
- Every ADDITIONAL leg beyond the second must name the SPECIFIC gate it fixes
  (sub_universe_sharpe / 2Y_sharpe / concentrated_weight). "More signal" is NOT
  a justification. Adding legs dilutes directionality and depresses
  sub_universe_sharpe and 2Y sharpe - the two gates that block most candidates.
- Empirically favourable settings among passers: neutralization STATISTICAL (25%)
  or SUBINDUSTRY (22%); decay 4; truncation 0.08; turnover band 0.10-0.12
  (do NOT deliberately push turnover down to 0.03-0.05).

REQUIRED (at least 8 concepts, of which at least 2 are multi-field):
- disagreement / residual / change-vs-level / intensity-weighted
- If a win recipe is provided, emit 1 concept that follows that mix shape
  using THIS dataset's fields as one leg (still {placeholder} syntax)
- At least 3 DISTINCT Expected Exposure values across the 8 concepts (e.g. 3 value + 3 momentum + 2 quality, NOT 8 value)

SKELETON DIVERSITY (2026-09-03 新增硬约束，防止全部用 quantile 包裹):
- Use DIVERSE outer wrappers across concepts: rank(), ts_zscore(), group_rank(), winsorize(), quantile(), ts_rank(), ts_quantile()
- Max 30% of concepts may share the same outer wrapper (e.g. if 8 concepts, max 2-3 may use quantile)
- FORBIDDEN: wrapping ALL concepts with quantile(..., driver="gaussian") — this creates pseudo-diversity and fails the diversity gate
- Prefer rank() for cross-sectional ranking, ts_zscore() for time-series normalization, group_rank() for intra-group ranking

DIVERSITY — enforced on SEMANTICS, not on operator names
(2026-09-08 revision. The previous rule demanded >=3 operator CATEGORIES and
>=1 Logical operator per wave. Measured against 859 gate-passing alphas that
rule was counterproductive: if_else appears in only 5.1% of passers, and
trade_when / bucket / ts_corr / ts_kurtosis do not reach the top-22 operators
at all, while group_rank appears in 32.0% and vec_avg in 12.6%. Forcing a
Logical operator into every wave forced at least one slot into a structurally
low-pass-rate region. Operator variety must be a CONSEQUENCE of semantic
variety, never a target in itself.)

Across the 8 concepts require:
- >= 3 distinct Expected Exposure values
- >= 3 distinct field families (different dataset prefixes, or clearly
  different economic quantities within one dataset)
- >= 2 distinct grouping axes wherever group_* is used
  (industry / subindustry / a pca_* cluster field / a bucket of a continuous
  auxiliary field) — a single grouping axis across all concepts is the real
  homogeneity failure, and it IS gated
- >= 2 distinct time-window scales (fast <= 22 vs slow >= 252)
- FORBIDDEN: 8 concepts that differ only by operator while sharing one field
  family and one grouping axis — that is pseudo-diversity and will show up as
  high mutual correlation in backtest.

Logical operators (if_else / trade_when) are APPROPRIATE only when the dataset
carries a genuine event timestamp (earnings date, announcement, insider
transaction, rating change). On continuous panels (lending rates, valuation
levels, model scores) an event gate is just a noise filter and measurably
destroys sharpe. Use them where the economics call for them, not to satisfy a
quota.

OPERATOR USAGE SCENARIOS (2026-09-04 新增教学示例，指导算子选择):
- if_else(condition, x, y): conditional combination (e.g. if_else(ts_delta(x, 5) > 0, rank(x), rank(reverse(x))))
- ts_corr(x, y, 22): correlation interaction (e.g. ts_corr(surprise, sentiment, 22) instead of multiply(surprise, sentiment))
- group_zscore(x, industry): intra-industry normalization (e.g. group_zscore(surprise, industry) instead of rank(surprise))
- trade_when(condition, x, -x): event-gated signal (e.g. trade_when(ts_count_nans(x, 22) < 5, rank(x), NaN))
- ts_arg_max(x, 22): momentum turning point (e.g. ts_arg_max(surprise, 22) to capture peak timing)
- ts_count_nans(x, 22): data quality gate (e.g. ts_count_nans(sentiment, 22) to filter low-coverage periods)
- group_neutralize(x, industry): industry mean neutralization (e.g. group_neutralize(surprise, industry) to remove industry effect)
- vec_stddev(x): VECTOR field internal dispersion (e.g. vec_stddev(sentiment_scores) to capture disagreement)

EXPOSURE CLAIMS ARE VERIFIED (2026-09-08):
Your Expected Exposure claim WILL be checked after backtest against the
platform metric `risk_neutralized_sharpe`. If risk_neutralized_sharpe collapses
to ~0 or goes negative while raw sharpe is high, the concept WAS the exposure
itself, not alpha on top of it — it will be marked a dead end and no amount of
parameter tuning will rescue it. Design so the signal SURVIVES removal of its
own stated exposure. Observed example: a HKG securities-lending wave produced
six alphas with risk_neutralized_sharpe of -0.33 to -0.57 while raw sharpe
looked non-zero; all were pure factor exposure.

OUTPUT each idea as:
**Concept**: <mechanism name>
- **Mechanism**: <1–2 sentences>
- **Fields**: `field_id_1`, `field_id_2`
- **Implementation Example**: `rank(subtract(ts_backfill({field_suffix_1}, 66), ts_backfill({field_suffix_2}, 66)))`
- **Direction**: ...
- **Expected Exposure**: value | momentum | quality | lowvol | liquidity | sentiment | growth | profitability | ...
- **Expected Turnover Band**: low | medium | high
- **Expected Coverage Band**: narrow | medium | wide
- **Why not crowded**: ...

Implementation Example MUST be a Python format template using {variable}.
{variable} should be the distinctive suffix of the intended field (or the full id
if short). Do not emit a generic {score}/{value}/{field} that matches everything.
"""
    return base + shape_constraint_rules(data_profile)
