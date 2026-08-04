"""wqb.config - Global configuration for the WorldQuant BRAIN alpha mining toolkit.

This module centralises all static configuration data inferred from the 5
SKILL.md specification files:

* ``REGIONS`` – per-region search space (universes, neutralizations, delays,
  categories).
* ``neutralization_search_order(region)`` – the recommended full sweep order
  of neutralization options for a given region.
* ``OP_FAMILIES`` – operators grouped by semantic family, used for shape
  classification and diversity checks.
* ``GHOST_OPERATORS`` – operator names that were purged on 2026-04-23 because
  they never existed on the live platform.
* ``VERIFIED_SAFE_OPERATORS`` – operators confirmed present on the platform
  and therefore safe for dispatch.
"""

from __future__ import annotations

from typing import Dict, List, Set

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_REGION: str = "USA"
DEFAULT_UNIVERSE: str = "TOP3000"
DEFAULT_DELAY: int = 1
SUBMISSION_POLICY_MANUAL_REVIEW: str = "manual_review"

# ---------------------------------------------------------------------------
# Region configuration
# ---------------------------------------------------------------------------

# Full USA neutralization list (11 options, as documented in SKILL.md).
_USA_NEUTRALIZATIONS: List[str] = [
    "SLOW",
    "FAST",
    "STATISTICAL",
    "SLOW_AND_FAST",
    "SUBINDUSTRY",
    "INDUSTRY",
    "CROWDING",
    "NONE",
    "MARKET",
    "SECTOR",
    "REVERSION_AND_MOMENTUM",
]

# Common neutralization subsets shared by most non-USA regions.
_COMMON_NEUTRALIZATIONS: List[str] = [
    "SUBINDUSTRY",
    "INDUSTRY",
    "SECTOR",
    "MARKET",
    "NONE",
]

REGIONS: Dict[str, Dict] = {
    "USA": {
        "universes": [
            "TOP3000",
            "TOP1000",
            "TOP500",
            "TOP200",
            "TOPSP500",
            "ILLIQUID_MINVOL1M",
        ],
        "neutralizations": _USA_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment", "option", "analyst"],
        "default_universe": "TOP3000",
    },
    "EUR": {
        "universes": ["TOP1200", "TOP800", "TOP400", "TOP200", "ILLIQUID_MINVOL1M"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment", "analyst"],
        "default_universe": "TOP1200",
    },
    "CHN": {
        "universes": ["TOP2000U", "TOP1600", "TOP800", "TOP400", "TOP200"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment"],
        "default_universe": "TOP2000U",
    },
    "ASI": {
        "universes": ["TOP500", "TOP200", "TOP100", "TOP50"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment", "analyst"],
        "default_universe": "TOP500",
    },
    "GLB": {
        "universes": ["TOP3000", "TOP1200", "TOP800", "TOP400"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment", "option"],
        "default_universe": "TOP3000",
    },
    "JPN": {
        "universes": ["TOP1600", "TOP1200", "TOP800", "TOP400", "TOP200"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment"],
        "default_universe": "TOP1600",
    },
    "KOR": {
        "universes": ["TOP600", "TOP200", "TOP100"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental"],
        "default_universe": "TOP600",
    },
    "AMR": {
        "universes": ["TOP3000", "TOP1000", "TOP500"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental", "sentiment"],
        "default_universe": "TOP3000",
    },
    "TWN": {
        "universes": ["TOP500", "TOP200", "TOP100"],
        "neutralizations": _COMMON_NEUTRALIZATIONS,
        "delays": [0, 1],
        "categories": ["equity", "fundamental"],
        "default_universe": "TOP500",
    },
}

# ---------------------------------------------------------------------------
# Neutralization search order
# ---------------------------------------------------------------------------

# USA global reference ordering (most → least productive, per SKILL.md).
_NEUTRALIZATION_ORDER_USA: List[str] = [
    "STATISTICAL",
    "SUBINDUSTRY",
    "INDUSTRY",
    "FAST",
    "SLOW",
    "CROWDING",
    "NONE",
    "MARKET",
    "SECTOR",
    "REVERSION_AND_MOMENTUM",
    "SLOW_AND_FAST",
]

# Default ordering for regions without a bespoke sweep order — falls back to
# the region's declared neutralization list.
_NEUTRALIZATION_ORDER_DEFAULT: List[str] = [
    "SUBINDUSTRY",
    "INDUSTRY",
    "SECTOR",
    "MARKET",
    "NONE",
]

# Per-region override of the recommended sweep order.
# KOR: WebDataScope 数据包实测 (2026-02, KOR_1, 规则 19):
# SECTOR(0.562) > MARKET(0.473) > SUBINDUSTRY(0.308) > INDUSTRY(0.257) > NONE(0.192)
# 与 USA 的 STATISTICAL 最优完全不同, 勿照搬默认顺序
_NEUTRALIZATION_ORDER_KOR: List[str] = [
    "SECTOR",
    "MARKET",
    "SUBINDUSTRY",
    "INDUSTRY",
    "NONE",
]

# Per-region override of the recommended sweep order.
_NEUTRALIZATION_ORDER_OVERRIDES: Dict[str, List[str]] = {
    "USA": _NEUTRALIZATION_ORDER_USA,
    "KOR": _NEUTRALIZATION_ORDER_KOR,
}


def neutralization_search_order(region: str) -> List[str]:
    """Return the full neutralization sweep order for *region*.

    For USA the ordering follows the global reference sequence documented in
    SKILL.md::

        STATISTICAL > SUBINDUSTRY > INDUSTRY > FAST > SLOW > CROWDING
        > NONE > MARKET > SECTOR > REVERSION_AND_MOMENTUM > SLOW_AND_FAST

    For other regions the function returns the intersection of the default
    sweep order with that region's supported neutralizations, preserving
    reference priority.

    Parameters
    ----------
    region:
        Region code (e.g. ``"USA"``, ``"EUR"``).

    Returns
    -------
    list[str]
        Ordered list of neutralization names to try.

    Raises
    ------
    KeyError
        If *region* is not a known region in :data:`REGIONS`.
    """
    region = region.upper()
    if region not in REGIONS:
        raise KeyError(
            f"Unknown region '{region}'. "
            f"Known regions: {sorted(REGIONS.keys())}"
        )

    if region in _NEUTRALIZATION_ORDER_OVERRIDES:
        return list(_NEUTRALIZATION_ORDER_OVERRIDES[region])

    # For non-USA regions: intersect default order with supported set,
    # then append any supported neutralisations not in the default order.
    supported = set(REGIONS[region]["neutralizations"])
    ordered = [n for n in _NEUTRALIZATION_ORDER_DEFAULT if n in supported]
    remaining = [n for n in REGIONS[region]["neutralizations"] if n not in set(ordered)]
    ordered.extend(remaining)
    return ordered


# ---------------------------------------------------------------------------
# Operator families
# ---------------------------------------------------------------------------

OP_FAMILIES: Dict[str, List[str]] = {
    "RANK": ["rank", "zscore", "rank_by_side", "winsorize", "normalize", "quantile", "scale"],
    "TS_RANK": ["ts_rank", "ts_zscore", "ts_quantile", "ts_av_diff", "ts_arg_max", "ts_arg_min"],
    "MOMENT": ["ts_delay", "ts_delta", "ts_returns", "ts_mean", "ts_std_dev", "ts_product", "ts_sum", "ts_scale"],
    "INFO": ["ts_decay_linear", "ts_ir", "ts_regression", "ts_corr", "ts_covariance"],
    "GROUP": [
        "group_rank", "group_zscore", "group_neutralize", "group_mean",
        "group_max", "group_min", "group_backfill", "group_scale",
        "group_count", "group_sum", "group_std_dev", "group_cartesian_product",
    ],
    "MATH": ["abs", "log", "sign", "sqrt", "signed_power", "power", "reverse", "inverse"],
    "FILTER": ["hump", "trade_when", "bucket", "densify", "jump_decay", "nan_mask", "if_else", "tail"],
    "NEUT": ["neutralize"],
    "LOGICAL": ["or", "and", "not", "is_nan"],
    "VECTOR": ["vec_sum", "vec_avg", "vec_max", "vec_min", "vec_norm", "vec_choose", "vec_count", "vec_stddev", "vec_range"],
    "DISTRIBUTIONAL": ["ts_kurtosis", "ts_co_skewness", "ts_count_nans", "kth_element"],
    "TVR": ["ts_target_tvr_decay", "ts_target_tvr_hump"],
    "UTILITY": ["pasteurize", "ts_step", "last_diff_value", "days_from_last_change", "ts_max_diff"],
}


def get_operator_family(op_name: str) -> str:
    """Return the family name for *op_name*, or ``"NONE"`` if not classified.

    Parameters
    ----------
    op_name:
        Lower-case operator name (e.g. ``"ts_rank"``).

    Returns
    -------
    str
        Family key from :data:`OP_FAMILIES` or ``"NONE"``.
    """
    for family, ops in OP_FAMILIES.items():
        if op_name in ops:
            return family
    return "NONE"


# ---------------------------------------------------------------------------
# Ghost operators (purged 2026-04-23 — never existed on the live platform)
# ---------------------------------------------------------------------------

GHOST_OPERATORS: Set[str] = {
    "ts_entropy",
    "ts_percentage",
    "ts_skewness",
    "ts_median",
    "ts_min_max_diff",
    "ts_min_max_cps",
    "ts_partial_corr",
    "ts_co_kurtosis",
    "ts_delta_limit",
    "group_normalize",
    "group_median",
    "group_percentage",
    "group_vector_proj",
    "tanh",
    "sigmoid",
    "s_log_1p",
    "ts_decay_exp_window",
}


# ---------------------------------------------------------------------------
# Verified-safe operators (confirmed present on the platform)
# ---------------------------------------------------------------------------

VERIFIED_SAFE_OPERATORS: List[str] = [
    # --- Original verified-safe operators ---
    "ts_kurtosis",
    "ts_co_skewness",
    "ts_delay",
    "group_max",
    "group_min",
    "nan_mask",
    "hump",
    "trade_when",
    "bucket",
    "densify",
    "jump_decay",
    "ts_decay_linear",
    "ts_quantile",
    "ts_ir",
    "ts_av_diff",
    "ts_max_diff",
    "last_diff_value",
    "days_from_last_change",
    # --- Added 2026-08-02: base-level operators confirmed on platform (operator audit) ---
    "reverse",
    "inverse",
    "winsorize",
    "normalize",
    "quantile",
    "scale",
    "is_nan",
    "not",
    "ts_step",
    "or",
    "and",
    "ts_product",
    "ts_scale",
    "ts_arg_max",
    "ts_arg_min",
    "ts_count_nans",
    "group_scale",
    "if_else",
    "kth_element",
    # --- Genius-level (confirmed on platform but require genius account) ---
    "pasteurize",
    "vec_count",
    "vec_stddev",
    "vec_range",
    "group_count",
    "group_sum",
    "group_std_dev",
    "group_cartesian_product",
    "tail",
    "ts_target_tvr_decay",
    "ts_target_tvr_hump",
]


# ---------------------------------------------------------------------------
# Aliases and additional exports used by scheduler / cli / news_loop
# ---------------------------------------------------------------------------

#: Alias for the USA default universe (used by scheduler and cli).
USA_DEFAULT_UNIVERSE: str = DEFAULT_UNIVERSE

#: Alias for the full USA neutralization sweep (11 options).
USA_NEUTRALIZATION_SWEEP: List[str] = _USA_NEUTRALIZATIONS

#: Region priority for budget allocation (higher = more budget).
REGION_PRIORITY: Dict[str, int] = {
    "USA": 3,
    "GLB": 2,
    "EUR": 2,
    "ASI": 2,
    "CHN": 1,
    "JPN": 1,
    "KOR": 1,
    "AMR": 2,
    "TWN": 1,
}

#: Paradigm names (P1–P13), matching the Paradigm enum in expression.paradigms.
PARADIGMS: List[str] = [
    "P1_SPREAD",
    "P2_RATIO",
    "P3_MOMENTUM",
    "P4_MEAN_REVERSION",
    "P5_GROUP_NEUTRAL",
    "P6_PAIR_TRADE",
    "P7_VOLATILITY",
    "P8_CARRY",
    "P9_INFORMATION",
    "P10_NORM_REG",
    "P11_RESIDUAL_STRIP",
    "P12_DISTRIBUTIONAL",
    "P13_BUCKET_NEUT",
]

#: News / sentiment categories that trigger the 6-bucket framework.
NEWS_CATEGORIES: Set[str] = {"news", "sentiment", "socialmedia"}

#: Dataset-ID prefixes that identify news/sentiment datasets.
NEWS_DATASET_PREFIXES: tuple = ("news", "nws", "sentiment", "snt")

#: ProdCorr ceiling for submission.
PRODCORR_CEILING: float = 0.70

#: Minimum batch size for create_multi_simulation.
BATCH_SIZE: int = 4

#: Shape classes tracked by the validator.
SHAPE_CLASSES: List[str] = ["S1", "S4", "S5", "S9"]


# --- WebDataScope failed-count gate check names ---

RA_CHECK_NAMES: Set[str] = {
    "HIGH_TURNOVER",
    "LOW_TURNOVER",
    "LOW_FITNESS",
    "LOW_RETURNS",
    "LOW_SHARPE",
    "LOW_GLB_AMER_SHARPE",
    "LOW_GLB_APAC_SHARPE",
    "LOW_GLB_EMEA_SHARPE",
    "LOW_ASI_JPN_SHARPE",
    "IS_LADDER_SHARPE",
    "LOW_2Y_SHARPE",
    "LOW_SUB_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
    "LOW_ROBUST_UNIVERSE_RETURNS",
    "CONCENTRATED_WEIGHT",
}

PPA_CHECK_NAMES: Set[str] = {
    "LOW_TURNOVER",
    "HIGH_TURNOVER",
    "LOW_SUB_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO",
    "LOW_ROBUST_UNIVERSE_RETURNS",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
}

PASS_STATES: Set[str] = {"PASS", "PENDING"}

# Robustness decision thresholds (robustness SKILL Phase C table).
DECAY_RATIO_REJECT: float = 0.30
DECAY_RATIO_CONDITIONAL: float = 0.50
RECENT_CV_SHARPE_REJECT: float = 0.60
RECENT_CV_SHARPE_CONDITIONAL: float = 0.40
FLAT_YEAR_THRESHOLD: float = 0.30
MAX_MIN_RATIO_REJECT: float = 5.0
MAX_MIN_RATIO_CONDITIONAL: float = 3.0
TOP5_CONCENTRATION_REJECT: float = 0.50
TOP5_CONCENTRATION_CONDITIONAL: float = 0.30
OPERATOR_COUNT_REJECT: int = 8
OPERATOR_COUNT_CONDITIONAL: int = 6


# ---------------------------------------------------------------------------
# Convenience functions (used by scheduler / cli / news_loop)
# ---------------------------------------------------------------------------

def default_universe(region: str) -> str:
    """Return the default universe for *region*.

    For USA REGULAR mining this is always ``"TOP3000"``.
    """
    region = region.upper()
    if region not in REGIONS:
        raise KeyError(f"Unknown region: {region!r}")
    return REGIONS[region].get("default_universe", DEFAULT_UNIVERSE)


def default_delay(region: str) -> int:
    """Return the default delay for *region*."""
    region = region.upper()
    if region not in REGIONS:
        raise KeyError(f"Unknown region: {region!r}")
    delays = REGIONS[region].get("delays", [1])
    return delays[-1] if delays else DEFAULT_DELAY


def get_categories(region: str) -> List[str]:
    """Return the list of searchable categories for *region*."""
    region = region.upper()
    if region not in REGIONS:
        raise KeyError(f"Unknown region: {region!r}")
    return list(REGIONS[region].get("categories", []))


def is_news_dataset(dataset_id: str, category: str = "") -> bool:
    """Check whether a dataset belongs to the news/sentiment/socialmedia space."""
    if category and category.lower() in NEWS_CATEGORIES:
        return True
    lower_id = dataset_id.lower()
    return lower_id.startswith(NEWS_DATASET_PREFIXES)


def compute_webdata_failed_counts(is_checks: list) -> dict:
    """Compute WebDataScope failed-count gates from ``is.checks`` array.

    Returns a dict with ``failed_ra`` and ``failed_ppa`` integer counts plus
    a ``details`` list enumerating each counted check.
    """
    details: list = []
    failed_ra = 0
    failed_ppa = 0
    for check in is_checks:
        name = check.get("name", "")
        result = check.get("result")
        value = check.get("value", 0)

        if name in RA_CHECK_NAMES and result not in PASS_STATES:
            failed_ra += 1
            details.append({
                "gate": "RA",
                "name": name,
                "result": result,
                "limit": check.get("limit"),
                "value": value,
            })

        is_ppa_fail = (
            name in PPA_CHECK_NAMES and result not in PASS_STATES
        ) or (
            name == "LOW_SHARPE" and value < 1
        )
        if is_ppa_fail:
            failed_ppa += 1
            details.append({
                "gate": "PPA",
                "name": name,
                "result": result,
                "limit": check.get("limit"),
                "value": value,
            })

    return {"failed_ra": failed_ra, "failed_ppa": failed_ppa, "details": details}
