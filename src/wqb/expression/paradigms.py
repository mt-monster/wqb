"""wqb.expression.paradigms - Alpha expression paradigms, templates, and rendering.

This module defines the 13 mining paradigms (P1–P13) and a registry of
renderable :class:`Template` objects.  Each template is a parametrised BRAIN
expression with placeholders for fields (``{a}``, ``{b}``), windows
(``{wa}``, ``{wb}``), and group variables (``{group}``).

Asymmetric templates (``asymmetric=True``) additionally contain literal
``pre_op_a`` / ``pre_op_b`` tokens that are replaced by concrete operator
names at render time via the *pre_op* argument.

Paradigm overview
------------------
* **P1_SPREAD** – cross-sectional spread between two fields.
* **P2_RATIO** – ratio of two fields.
* **P3_MOMENTUM** – momentum / delta-based signal.
* **P4_MEAN_REVERSION** – mean-reversion around a moving average.
* **P5_GROUP_NEUTRAL** – group-neutralised spread.
* **P6_PAIR_TRADE** – pair-trading residual.
* **P7_VOLATILITY** – volatility-normalised signal.
* **P8_CARRY** – carry-style signal.
* **P9_INFORMATION** – information-decay weighted spread.
* **P10_NORM_REG** – normalised regression (z-score difference).
* **P11_RESIDUAL_STRIP** – residual after regression.
* **P12_DISTRIBUTIONAL** – distributional (ts_zscore) difference.
* **P13_BUCKET_NEUT** – bucket-neutralised rank.

Default rotation paradigms: P1, P2, P4, P5.
Forum-mining additions: P9–P13.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Paradigm enum
# ---------------------------------------------------------------------------

class Paradigm(Enum):
    """The 13 alpha expression paradigms."""

    P1_SPREAD = "P1_SPREAD"
    P2_RATIO = "P2_RATIO"
    P3_MOMENTUM = "P3_MOMENTUM"
    P4_MEAN_REVERSION = "P4_MEAN_REVERSION"
    P5_GROUP_NEUTRAL = "P5_GROUP_NEUTRAL"
    P6_PAIR_TRADE = "P6_PAIR_TRADE"
    P7_VOLATILITY = "P7_VOLATILITY"
    P8_CARRY = "P8_CARRY"
    P9_INFORMATION = "P9_INFORMATION"
    P10_NORM_REG = "P10_NORM_REG"
    P11_RESIDUAL_STRIP = "P11_RESIDUAL_STRIP"
    P12_DISTRIBUTIONAL = "P12_DISTRIBUTIONAL"
    P13_BUCKET_NEUT = "P13_BUCKET_NEUT"


# Default rotation set (per SKILL.md, expanded 2026-08-02 to include P3/P6/P7/P8).
DEFAULT_ROTATION: List[Paradigm] = [
    Paradigm.P1_SPREAD,
    Paradigm.P2_RATIO,
    Paradigm.P3_MOMENTUM,
    Paradigm.P4_MEAN_REVERSION,
    Paradigm.P5_GROUP_NEUTRAL,
    Paradigm.P6_PAIR_TRADE,
    Paradigm.P7_VOLATILITY,
    Paradigm.P8_CARRY,
]

# Forum-mining additions.
FORUM_ADDITIONS: List[Paradigm] = [
    Paradigm.P9_INFORMATION,
    Paradigm.P10_NORM_REG,
    Paradigm.P11_RESIDUAL_STRIP,
    Paradigm.P12_DISTRIBUTIONAL,
    Paradigm.P13_BUCKET_NEUT,
]


# ---------------------------------------------------------------------------
# Pre-processing operator pools
# ---------------------------------------------------------------------------

#: Operators that require a window parameter, e.g. ``ts_rank(x, 5)``.
PRE_OPS_WINDOWED: List[str] = [
    "ts_rank",
    "ts_zscore",
    "ts_quantile",
    "ts_mean",
    "ts_std_dev",
    "ts_decay_linear",
    "ts_delta",
    "ts_returns",
    "ts_delay",
    "ts_av_diff",
    "ts_ir",
    # --- Added 2026-08-02: expand windowed pre-op pool (operator audit) ---
    "ts_corr",
    "ts_covariance",
    "ts_sum",
    "ts_product",
    "ts_scale",
    "ts_arg_max",
    "ts_arg_min",
    "ts_count_nans",
    "ts_kurtosis",
    "ts_co_skewness",
    "ts_max_diff",
    "last_diff_value",
    "ts_regression",
]

#: Operators that do **not** require a window, e.g. ``rank(x)``.
PRE_OPS_WINDOWLESS: List[str] = [
    "rank",
    "zscore",
    "sign",
    "abs",
    "log",
    "sqrt",
    "group_rank",
    "group_zscore",
    # --- Added 2026-08-02: expand windowless pre-op pool (operator audit) ---
    "winsorize",
    "normalize",
    "quantile",
    "scale",
    "reverse",
    "inverse",
    "neutralize",
    "rank_by_side",
    "nan_mask",
    "hump",
    "bucket",
    "jump_decay",
    "group_neutralize",
    "group_mean",
    "is_nan",
    "not",
]


# ---------------------------------------------------------------------------
# Template dataclass
# ---------------------------------------------------------------------------

@dataclass
class Template:
    """A renderable alpha expression template.

    Attributes
    ----------
    paradigm:
        The paradigm this template belongs to.
    name:
        Human-readable template name (unique within the registry).
    expression:
        Template string with placeholders.  Standard placeholders are
        ``{a}``, ``{b}`` (fields), ``{wa}``, ``{wb}`` (windows), and
        ``{group}`` (group variable).  Asymmetric templates also contain
        literal ``pre_op_a`` and ``pre_op_b`` operator-name tokens.
    asymmetric:
        If ``True``, the template contains ``pre_op_a`` / ``pre_op_b``
        placeholders that must be resolved via the *pre_op* argument of
        :func:`render`.
    pre_op_pool_a:
        Pool of allowed pre-processing operators for the A side.
    pre_op_pool_b:
        Pool of allowed pre-processing operators for the B side.
    """

    paradigm: Paradigm
    name: str
    expression: str
    asymmetric: bool = False
    pre_op_pool_a: Optional[List[str]] = None
    pre_op_pool_b: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# Template registry
# ---------------------------------------------------------------------------

#: Combined pool of all pre-processing operators (windowed + windowless).
_ALL_PRE_OPS: List[str] = PRE_OPS_WINDOWED + PRE_OPS_WINDOWLESS

# Subset pools used by asymmetric variants.
_TS_RANK_POOL: List[str] = ["ts_rank", "ts_zscore", "ts_quantile"]
_MOMENT_POOL: List[str] = ["ts_mean", "ts_std_dev"]
_INFO_POOL: List[str] = ["ts_decay_linear", "ts_ir"]
_RANK_POOL: List[str] = ["rank", "zscore"]
_GROUP_POOL: List[str] = ["group_rank", "group_zscore"]
# --- Added 2026-08-02: new subset pools for expanded operator coverage ---
_MOMENT_FULL_POOL: List[str] = ["ts_mean", "ts_std_dev", "ts_delta", "ts_returns", "ts_sum", "ts_product", "ts_scale"]
_INFO_FULL_POOL: List[str] = ["ts_decay_linear", "ts_ir", "ts_corr", "ts_covariance", "ts_regression"]
_DIST_POOL: List[str] = ["ts_kurtosis", "ts_co_skewness", "ts_arg_max", "ts_arg_min", "ts_count_nans"]
_RANK_FULL_POOL: List[str] = ["rank", "zscore", "winsorize", "normalize", "quantile", "scale"]
_GROUP_FULL_POOL: List[str] = ["group_rank", "group_zscore", "group_neutralize", "group_mean", "group_scale"]
_MATH_POOL: List[str] = ["sign", "abs", "log", "sqrt", "reverse", "inverse"]
_FILTER_POOL: List[str] = ["hump", "bucket", "jump_decay", "nan_mask"]


TEMPLATES: List[Template] = [
    # ---- P1_SPREAD (basic + asymmetric) ----
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="p1_spread",
        expression="subtract({a}, {b})",
        asymmetric=False,
    ),
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="p1_spread_asym",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_ALL_PRE_OPS,
        pre_op_pool_b=_ALL_PRE_OPS,
    ),

    # ---- P2_RATIO ----
    Template(
        paradigm=Paradigm.P2_RATIO,
        name="p2_ratio",
        expression="divide({a}, {b})",
        asymmetric=False,
    ),

    # ---- P4_MEAN_REVERSION ----
    Template(
        paradigm=Paradigm.P4_MEAN_REVERSION,
        name="p4_mean_reversion",
        expression="multiply(subtract(ts_mean({a}, {wa}), {a}), sign(subtract({a}, {b})))",
        asymmetric=False,
    ),

    # ---- P5_GROUP_NEUTRAL ----
    Template(
        paradigm=Paradigm.P5_GROUP_NEUTRAL,
        name="p5_group_neutral",
        expression="group_neutralize(subtract({a}, {b}), {group})",
        asymmetric=False,
    ),

    # ---- P9_INFORMATION ----
    Template(
        paradigm=Paradigm.P9_INFORMATION,
        name="p9_information",
        expression="ts_decay_linear(subtract({a}, {b}), {wa})",
        asymmetric=False,
    ),

    # ---- P10_NORM_REG ----
    Template(
        paradigm=Paradigm.P10_NORM_REG,
        name="p10_norm_reg",
        expression="subtract(zscore({a}), zscore({b}))",
        asymmetric=False,
    ),

    # ---- P11_RESIDUAL_STRIP ----
    Template(
        paradigm=Paradigm.P11_RESIDUAL_STRIP,
        name="p11_residual_strip",
        expression="subtract({a}, ts_regression({a}, {b}, {wa}, 1))",
        asymmetric=False,
    ),

    # ---- P12_DISTRIBUTIONAL ----
    Template(
        paradigm=Paradigm.P12_DISTRIBUTIONAL,
        name="p12_distributional",
        expression="subtract(ts_zscore({a}, {wa}), ts_zscore({b}, {wb}))",
        asymmetric=False,
    ),

    # ---- P13_BUCKET_NEUT ----
    Template(
        paradigm=Paradigm.P13_BUCKET_NEUT,
        name="p13_bucket_neut",
        expression="group_neutralize(rank({a}), bucket({b}))",
        asymmetric=False,
    ),

    # ---- P3_MOMENTUM (added 2026-08-02: was missing entirely) ----
    Template(
        paradigm=Paradigm.P3_MOMENTUM,
        name="p3_momentum",
        expression="rank(ts_delta({a}, {wa}))",
        asymmetric=False,
    ),
    Template(
        paradigm=Paradigm.P3_MOMENTUM,
        name="p3_momentum_returns",
        expression="rank(ts_returns({a}, {wa}))",
        asymmetric=False,
    ),
    Template(
        paradigm=Paradigm.P3_MOMENTUM,
        name="p3_momentum_asym",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_MOMENT_FULL_POOL,
        pre_op_pool_b=_MOMENT_FULL_POOL,
    ),

    # ---- P6_PAIR_TRADE (added 2026-08-02: uses ts_corr/ts_regression) ----
    Template(
        paradigm=Paradigm.P6_PAIR_TRADE,
        name="p6_pair_trade_corr",
        expression="rank(ts_corr({a}, {b}, {wa}))",
        asymmetric=False,
    ),
    Template(
        paradigm=Paradigm.P6_PAIR_TRADE,
        name="p6_pair_trade_residual",
        expression="rank(subtract({a}, ts_regression({a}, {b}, {wa})))",
        asymmetric=False,
    ),

    # ---- P7_VOLATILITY (added 2026-08-02: uses ts_std_dev/divide) ----
    Template(
        paradigm=Paradigm.P7_VOLATILITY,
        name="p7_vol_ratio",
        expression="rank(divide(ts_std_dev({a}, {wa}), ts_std_dev({b}, {wb})))",
        asymmetric=False,
    ),
    Template(
        paradigm=Paradigm.P7_VOLATILITY,
        name="p7_vol_neut",
        expression="group_neutralize(rank(divide(ts_std_dev({a}, {wa}), ts_std_dev({b}, {wb}))), {group})",
        asymmetric=False,
    ),

    # ---- P8_CARRY (added 2026-08-02: uses divide/ts_mean) ----
    Template(
        paradigm=Paradigm.P8_CARRY,
        name="p8_carry",
        expression="rank(divide({a}, {b}))",
        asymmetric=False,
    ),
    Template(
        paradigm=Paradigm.P8_CARRY,
        name="p8_carry_smoothed",
        expression="rank(ts_mean(divide({a}, {b}), {wa}))",
        asymmetric=False,
    ),

    # ---- New templates leveraging previously unused operators (2026-08-02) ----

    # P1 with ts_corr (information-rich spread)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="p1_spread_corr",
        expression="rank(ts_corr({a}, {b}, {wa}))",
        asymmetric=False,
    ),
    # P1 with winsorize (outlier-robust spread)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="p1_spread_winsorized",
        expression="subtract(winsorize({a}), winsorize({b}))",
        asymmetric=False,
    ),
    # P5 with group_neutralize + ts_delta (momentum-neutralized group signal)
    Template(
        paradigm=Paradigm.P5_GROUP_NEUTRAL,
        name="p5_group_neut_momentum",
        expression="group_neutralize(rank(ts_delta({a}, {wa})), {group})",
        asymmetric=False,
    ),
    # P9 with ts_ir (information ratio decay)
    Template(
        paradigm=Paradigm.P9_INFORMATION,
        name="p9_info_ratio",
        expression="ts_decay_linear(rank(ts_ir({a}, {wa})), {wa})",
        asymmetric=False,
    ),
    # P10 with normalize (normalized regression)
    Template(
        paradigm=Paradigm.P10_NORM_REG,
        expression="subtract(normalize({a}), normalize({b}))",
        name="p10_norm_reg_full",
        asymmetric=False,
    ),
    # P12 with ts_arg_max (distributional timing signal)
    Template(
        paradigm=Paradigm.P12_DISTRIBUTIONAL,
        name="p12_dist_timing",
        expression="subtract(ts_arg_max({a}, {wa}), ts_arg_min({b}, {wb}))",
        asymmetric=False,
    ),
    # P13 with trade_when (event-conditioned bucket)
    Template(
        paradigm=Paradigm.P13_BUCKET_NEUT,
        name="p13_event_bucket",
        expression="trade_when(ts_delta({a}, {wa}), group_neutralize(rank({b}), bucket({a})), -1)",
        asymmetric=False,
    ),

    # ---- 12 asymmetric (asym_*) variant templates ----

    # 1. P1: rank vs zscore (both windowless)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_rank_zscore",
        expression="subtract(pre_op_a({a}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_RANK_POOL,
        pre_op_pool_b=_RANK_POOL,
    ),
    # 2. P1: ts_rank (windowed) vs rank (windowless)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_tsrank_rank",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_TS_RANK_POOL,
        pre_op_pool_b=_RANK_POOL,
    ),
    # 3. P1: rank (windowless) vs ts_rank (windowed)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_rank_tsrank",
        expression="subtract(pre_op_a({a}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_RANK_POOL,
        pre_op_pool_b=_TS_RANK_POOL,
    ),
    # 4. P1: ts_rank vs ts_zscore (both windowed, different ops)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_tsrank_tszscore",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=["ts_rank", "ts_quantile"],
        pre_op_pool_b=["ts_zscore", "ts_av_diff"],
    ),
    # 5. P1: ts_mean (moment) vs ts_rank (ts_rank family)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_tsmean_tsrank",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_MOMENT_POOL,
        pre_op_pool_b=_TS_RANK_POOL,
    ),
    # 6. P1: rank vs group_rank (cross-layer)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_rank_grouprank",
        expression="subtract(pre_op_a({a}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_RANK_POOL,
        pre_op_pool_b=_GROUP_POOL,
    ),
    # 7. P2: rank vs zscore ratio (both windowless)
    Template(
        paradigm=Paradigm.P2_RATIO,
        name="asym_p2_rank_zscore",
        expression="divide(pre_op_a({a}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_RANK_POOL,
        pre_op_pool_b=_RANK_POOL,
    ),
    # 8. P9: ts_rank vs rank inside information decay
    Template(
        paradigm=Paradigm.P9_INFORMATION,
        name="asym_p9_tsrank_rank",
        expression="ts_decay_linear(subtract(pre_op_a({a}, {wa}), pre_op_b({b})), {wa})",
        asymmetric=True,
        pre_op_pool_a=_TS_RANK_POOL,
        pre_op_pool_b=_RANK_POOL,
    ),
    # 9. P10: ts_rank (windowed) vs zscore (windowless) norm-reg
    Template(
        paradigm=Paradigm.P10_NORM_REG,
        name="asym_p10_tsrank_zscore",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_TS_RANK_POOL,
        pre_op_pool_b=_RANK_POOL,
    ),
    # 10. P12: ts_rank vs rank distributional
    Template(
        paradigm=Paradigm.P12_DISTRIBUTIONAL,
        name="asym_p12_tsrank_rank",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_TS_RANK_POOL,
        pre_op_pool_b=_RANK_POOL,
    ),
    # 11. P1: zscore (windowless) vs ts_decay_linear (info, windowed)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_zscore_tsdecay",
        expression="subtract(pre_op_a({a}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_RANK_POOL,
        pre_op_pool_b=_INFO_POOL,
    ),
    # 12. P1: ts_decay_linear (info, windowed) vs ts_rank (ts_rank, windowed)
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_tsdecay_tsrank",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_INFO_POOL,
        pre_op_pool_b=_TS_RANK_POOL,
    ),

    # ---- Added 2026-08-02: 8 new asymmetric variants leveraging expanded pools ----

    # 13. P3: ts_delta (moment) vs ts_returns (moment) — momentum asym
    Template(
        paradigm=Paradigm.P3_MOMENTUM,
        name="asym_p3_delta_returns",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_MOMENT_FULL_POOL,
        pre_op_pool_b=_MOMENT_FULL_POOL,
    ),
    # 14. P6: ts_decay_linear (info) vs ts_ir (info) — pair-trade asym
    Template(
        paradigm=Paradigm.P6_PAIR_TRADE,
        name="asym_p6_decay_ir",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_INFO_FULL_POOL,
        pre_op_pool_b=_INFO_FULL_POOL,
    ),
    # 15. P7: ts_std_dev (moment) vs ts_std_dev (moment) — vol asym
    Template(
        paradigm=Paradigm.P7_VOLATILITY,
        name="asym_p7_vol_spread",
        expression="divide(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_MOMENT_FULL_POOL,
        pre_op_pool_b=_MOMENT_FULL_POOL,
    ),
    # 16. P1: winsorize (rank) vs normalize (rank) — robust spread
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_winsorize_normalize",
        expression="subtract(pre_op_a({a}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_RANK_FULL_POOL,
        pre_op_pool_b=_RANK_FULL_POOL,
    ),
    # 17. P1: ts_decay_linear (info) vs winsorize (rank) — cross-layer robust
    Template(
        paradigm=Paradigm.P1_SPREAD,
        name="asym_p1_decay_winsorize",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}))",
        asymmetric=True,
        pre_op_pool_a=_INFO_FULL_POOL,
        pre_op_pool_b=_RANK_FULL_POOL,
    ),
    # 18. P5: rank (rank) vs zscore (rank) inside group neutralize
    Template(
        paradigm=Paradigm.P5_GROUP_NEUTRAL,
        name="asym_p5_group_neutralized",
        expression="group_neutralize(subtract(pre_op_a({a}), pre_op_b({b})), {group})",
        asymmetric=True,
        pre_op_pool_a=_RANK_FULL_POOL,
        pre_op_pool_b=_RANK_FULL_POOL,
    ),
    # 19. P9: ts_ir (info) vs ts_arg_max (dist) — info-timing asym
    Template(
        paradigm=Paradigm.P9_INFORMATION,
        name="asym_p9_ir_argmax",
        expression="ts_decay_linear(subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb})), {wa})",
        asymmetric=True,
        pre_op_pool_a=_INFO_FULL_POOL,
        pre_op_pool_b=_DIST_POOL,
    ),
    # 20. P12: ts_kurtosis (dist) vs ts_co_skewness (dist) — distributional asym
    Template(
        paradigm=Paradigm.P12_DISTRIBUTIONAL,
        name="asym_p12_kurt_skew",
        expression="subtract(pre_op_a({a}, {wa}), pre_op_b({b}, {wb}))",
        asymmetric=True,
        pre_op_pool_a=_DIST_POOL,
        pre_op_pool_b=_DIST_POOL,
    ),
]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

# Regex patterns for replacing pre_op placeholders.
_PRE_OP_A_WINDOWED_RE = re.compile(r"pre_op_a\(\s*\{a\}\s*,\s*\{wa\}\s*\)")
_PRE_OP_A_PLAIN_RE = re.compile(r"pre_op_a\(\s*\{a\}\s*\)")
_PRE_OP_B_WINDOWED_RE = re.compile(r"pre_op_b\(\s*\{b\}\s*,\s*\{wb\}\s*\)")
_PRE_OP_B_PLAIN_RE = re.compile(r"pre_op_b\(\s*\{b\}\s*\)")

_DEFAULT_WA = 5
_DEFAULT_WB = 10


def _replace_pre_op(
    expr: str,
    patterns: tuple,
    op_name: str,
    field_ph: str,
    window_ph: str,
    window_val: str,
) -> str:
    """Replace a pre_op placeholder, handling windowed vs windowless operators.

    Parameters
    ----------
    expr:
        The template expression string.
    patterns:
        A ``(windowed_re, plain_re)`` tuple of compiled regexes.
    op_name:
        The concrete operator name to substitute.
    field_ph:
        The field placeholder (``"{a}"`` or ``"{b}"``).
    window_ph:
        The window placeholder (``"{wa}"`` or ``"{wb}"``).
    window_val:
        The window value as a string (e.g. ``"5"``).
    """
    windowed_re, plain_re = patterns

    if op_name in PRE_OPS_WINDOWED:
        # Windowed operator: keep the window argument
        replacement = f"{op_name}({field_ph}, {window_val})"
        expr = windowed_re.sub(replacement, expr)
        # Also handle plain pattern (in case the template only had plain form)
        expr = plain_re.sub(f"{op_name}({field_ph})", expr)
    else:
        # Windowless operator: drop the window argument
        expr = windowed_re.sub(f"{op_name}({field_ph})", expr)
        expr = plain_re.sub(f"{op_name}({field_ph})", expr)

    return expr


def render(
    tpl: Template,
    a: str,
    b: str,
    pre_op: Optional[Dict[str, str]] = None,
    window: Optional[Dict[str, int]] = None,
    group: Optional[str] = None,
) -> str:
    """Render a :class:`Template` into a concrete BRAIN expression.

    Parameters
    ----------
    tpl:
        The template to render.
    a:
        Field name for the A side.
    b:
        Field name for the B side.
    pre_op:
        Mapping with keys ``"a"`` and ``"b"`` whose values are operator
        names.  Required for asymmetric templates; ignored otherwise.
        If ``None`` for an asymmetric template, defaults to ``"rank"`` for
        both sides.
    window:
        Mapping with keys ``"a"`` and ``"b"`` whose values are window
        lengths.  Defaults to ``{"a": 5, "b": 10}`` if not provided.
    group:
        Group variable name (e.g. ``"market"``, ``"sector"``).  Required
        for templates containing ``{group}``.

    Returns
    -------
    str
        A concrete, dispatch-ready BRAIN expression.

    Examples
    --------
    >>> from wqb.expression.paradigms import TEMPLATES, render
    >>> tpl = TEMPLATES[0]  # p1_spread
    >>> render(tpl, a="close", b="volume")
    'subtract(close, volume)'

    >>> tpl = TEMPLATES[1]  # p1_spread_asym
    >>> render(tpl, a="close", b="volume",
    ...        pre_op={"a": "ts_rank", "b": "rank"},
    ...        window={"a": 5, "b": 10})
    'subtract(ts_rank(close, 5), rank(volume))'
    """
    wa = str((window or {}).get("a", _DEFAULT_WA))
    wb = str((window or {}).get("b", _DEFAULT_WB))

    expr = tpl.expression

    if tpl.asymmetric:
        op_a = (pre_op or {}).get("a", "rank")
        op_b = (pre_op or {}).get("b", "rank")

        # Replace A-side pre_op placeholder
        expr = _replace_pre_op(
            expr,
            (_PRE_OP_A_WINDOWED_RE, _PRE_OP_A_PLAIN_RE),
            op_a,
            "{a}",
            "{wa}",
            wa,
        )
        # Replace B-side pre_op placeholder
        expr = _replace_pre_op(
            expr,
            (_PRE_OP_B_WINDOWED_RE, _PRE_OP_B_PLAIN_RE),
            op_b,
            "{b}",
            "{wb}",
            wb,
        )

    # Replace standard field placeholders
    expr = expr.replace("{a}", a)
    expr = expr.replace("{b}", b)

    # Replace remaining window placeholders (non-asymmetric templates or
    # windowed operators whose {wa}/{wb} survived the regex substitution)
    expr = expr.replace("{wa}", wa)
    expr = expr.replace("{wb}", wb)

    # Replace group placeholder
    if group is not None:
        expr = expr.replace("{group}", group)

    return expr


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def get_templates_by_paradigm(paradigm: Paradigm) -> List[Template]:
    """Return all templates belonging to *paradigm*.

    Parameters
    ----------
    paradigm:
        A member of :class:`Paradigm`.

    Returns
    -------
    list[Template]
        All registered templates for the given paradigm.  May be empty if
        no templates are defined for that paradigm.
    """
    return [t for t in TEMPLATES if t.paradigm == paradigm]


def get_all_paradigms() -> List[Paradigm]:
    """Return all 13 paradigms in definition order.

    Returns
    -------
    list[Paradigm]
        The complete list of paradigm enum members.
    """
    return list(Paradigm)


def get_template_by_name(name: str) -> Optional[Template]:
    """Look up a template by its unique *name*.

    Parameters
    ----------
    name:
        Template name (e.g. ``"p1_spread"``, ``"asym_p1_rank_zscore"``).

    Returns
    -------
    Template or None
        The matching template, or ``None`` if not found.
    """
    for t in TEMPLATES:
        if t.name == name:
            return t
    return None
