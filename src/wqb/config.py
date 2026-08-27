"""wqb.config — region search space, operator families and gate helpers.

Single source of truth for region configuration (aligned with the platform
catalog as of 2026-08-13), operator family classification, ghost-operator
blacklist and WebDataScope gate accounting.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Set

REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Region search space
# ---------------------------------------------------------------------------

# Full USA neutralization sweep (11 options) — platform-supported order.
_USA_NEUTRALIZATIONS = [
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

REGIONS: Dict[str, dict] = {
    "USA": {
        "universes": ["TOP3000", "TOP2000", "TOP1000", "TOP500", "TOP200"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst",
                       "option", "short_interest", "model", "earnings", "event"],
        "default_universe": "TOP3000",
    },
    "EUR": {
        "universes": ["TOP2500", "TOPCS1600", "TOP1200", "TOP800", "TOP400",
                      "ILLIQUID_MINVOL1M"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst",
                       "option", "short_interest", "model", "earnings"],
        "default_universe": "TOP2500",
    },
    "CHN": {
        "universes": ["TOP2000U", "TOP1000", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst",
                       "short_interest", "model"],
        "default_universe": "TOP2000U",
    },
    "ASI": {
        "universes": ["TOP2000", "TOP1000", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst"],
        "default_universe": "TOP2000",
    },
    "GLB": {
        "universes": ["MINVOL10M", "TOPDIV3000", "TOP3000", "TOP2000"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst",
                       "model"],
        "default_universe": "TOP3000",
    },
    "JPN": {
        "universes": ["TOP2000", "TOP1000", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst"],
        "default_universe": "TOP2000",
    },
    "KOR": {
        "universes": ["TOP3000", "TOP1000", "TOP500"],
        # KOR campaigns start from SECTOR (empirical conclusion 2026-07).
        "neutralizations": ["SECTOR"] + [n for n in _USA_NEUTRALIZATIONS if n != "SECTOR"],
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news", "analyst"],
        "default_universe": "TOP3000",
    },
    "AMR": {
        "universes": ["TOP2000", "TOP1000", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment", "news"],
        "default_universe": "TOP2000",
    },
    "TWN": {
        "universes": ["TOP1000", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment"],
        "default_universe": "TOP1000",
    },
    "GBR": {
        "universes": ["TOP700", "TOP350"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [0, 1],  # GBR D0 threshold 2.69 measured
        "categories": ["equity", "fundamental", "sentiment", "news"],
        "default_universe": "TOP700",
    },
    "DEU": {
        "universes": ["TOP500", "TOP300"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment"],
        "default_universe": "TOP500",
    },
    "IND": {
        "universes": ["TOP500", "TOP300"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental", "sentiment"],
        "default_universe": "TOP500",
    },
    "MEA": {
        "universes": ["TOP400", "TOP200"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental"],
        "default_universe": "TOP400",
    },
    "HKG": {
        "universes": ["TOP800", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": ["equity", "fundamental"],
        "default_universe": "TOP800",
    },
}

# Campaign conclusions: best measured neutralization per region (None = no data).
_NEUTRALIZATION_BEST: Dict[str, Optional[str]] = {
    "EUR": "REVERSION_AND_MOMENTUM",
    "GBR": "INDUSTRY",
    "IND": "STATISTICAL",
}


def neutralization_search_order(region: str) -> List[str]:
    """Return the full neutralization sweep order for a region.

    Case-insensitive on the region code; raises ``KeyError`` for unknown
    regions.
    """
    return list(REGIONS[region.upper()]["neutralizations"])


def neutralization_best(region: str) -> Optional[str]:
    """Return the best measured neutralization for a region, or None."""
    return _NEUTRALIZATION_BEST.get(region.upper())


def default_universe(region: str) -> str:
    """Return the default universe for a region (KeyError if unknown)."""
    return REGIONS[region.upper()]["default_universe"]


def default_delay(region: str) -> int:
    """Return the default (first) delay for a region (KeyError if unknown)."""
    return REGIONS[region.upper()]["delays"][0]


def get_categories(region: str) -> List[str]:
    """Return the supported data categories for a region (KeyError if unknown)."""
    return list(REGIONS[region.upper()]["categories"])


# ---------------------------------------------------------------------------
# Operator families
# ---------------------------------------------------------------------------

OP_FAMILIES: Dict[str, List[str]] = {
    "TS_RANK": ["ts_rank"],
    "TS_WINDOW": ["ts_min", "ts_max", "ts_mean", "ts_sum", "ts_std_dev",
                  "ts_av_diff", "ts_delta", "ts_product", "ts_scale",
                  "ts_zscore", "ts_step", "ts_kurtosis", "ts_skewness",
                  "ts_arg_max", "ts_arg_min", "ts_corr", "ts_covariance",
                  "ts_decay_exp_window", "ts_decay_linear", "ts_regression",
                  "ts_percentage", "ts_moment"],
    "TS_FILL": ["ts_backfill", "ts_fill", "ts_last", "ts_first", "ts_index"],
    "TS_SHIFT": ["ts_delay", "ts_diff", "ts_return", "ts_ir", "ts_min_max_cps"],
    "GROUP": ["group_neutralize", "group_rank", "group_zscore", "group_mean",
              "group_sum", "group_max", "group_min", "group_scale",
              "group_median", "group_count", "group_first", "group_last",
              "group_percentage", "group_std_dev", "group_kurtosis",
              "group_skewness", "group_regression", "group_arg_max",
              "group_arg_min"],
    "MATH": ["abs", "multiply", "divide", "add", "subtract", "power", "log",
              "sign", "signed_power", "sqrt", "ceiling", "floor", "fraction",
              "truncate", "exp", "inverse", "max", "min", "bucket", "reverse"],
    "RANK": ["rank"],
    "SCALE": ["scale", "normalize", "vector_norm", "step", "sigmoid",
              "filter", "keep", "pasteurize", "winsorize"],
    "REDUCE": ["reduce_ir"],
    "VECTOR": ["vec_avg", "vec_max", "vec_min", "vec_sum", "vec_std_dev",
               "vec_norm", "vec_count", "vec_ir", "vec_skew", "vec_kurt",
               "vec_same_as_prev", "vec_avg_day", "vec_avg_week",
               "vec_percentage", "vec_is_nan"],
    "TIME": ["tick", "day", "week", "month", "year", "quarter"],
    "COND": ["ternary", "is_nan"],
    "LOGIC": ["if_else", "greater", "less", "equal", "not_equal",
               "less_equal", "greater_equal", "and", "or", "not"],
}

_OP_TO_FAMILY: Dict[str, str] = {
    op: family for family, ops in OP_FAMILIES.items() for op in ops
}


def get_operator_family(op: str) -> str:
    """Classify an operator into its family; unknown operators → 'NONE'."""
    return _OP_TO_FAMILY.get(op, "NONE")


# ---------------------------------------------------------------------------
# Operator verification state (catalog vs live platform)
# ---------------------------------------------------------------------------

# Ghost operators: declared in the catalog but absent from the live platform.
# Base list synced from data/operators_verified.json (known_ghosts); the
# platform catalog has no `neutralize` expression operator either.
_OPERATORS_STATE_PATH = REPO_ROOT / "data" / "operators_verified.json"


def _load_operators_state() -> dict:
    try:
        with open(_OPERATORS_STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


_STATE = _load_operators_state()

VERIFIED_SAFE_OPERATORS: List[str] = list(_STATE.get("verified", []))

GHOST_OPERATORS: Set[str] = set(_STATE.get("known_ghosts", [])) | {"neutralize"}

# Sanity guard: verified and ghost sets must stay disjoint.
GHOST_OPERATORS -= set(VERIFIED_SAFE_OPERATORS)


def is_news_dataset(name: str, category: Optional[str] = None) -> bool:
    """Detect news/sentiment datasets by prefix or category."""
    if category == "news":
        return True
    prefix = name.lower()
    return prefix.startswith("news") or prefix.startswith("snt")


# ---------------------------------------------------------------------------
# WebDataScope gate accounting
# ---------------------------------------------------------------------------

RA_CHECK_NAMES: List[str] = [
    "LOW_FITNESS",
    "LOW_SHARPE",
    "HIGH_TURNOVER",
    "LOW_TURNOVER",
    "CONCENTRATED_WEIGHT",
    "HIGH_DRAWDOWN",
    "LOW_SELFCORR",
    "LOW_PNL",
]

PPA_CHECK_NAMES: List[str] = ["LOW_SHARPE", "LOW_FITNESS"]


def compute_webdata_failed_counts(checks: List[dict]) -> dict:
    """Classify WebDataScope quality checks into RA vs PPA failures.

    Returns ``{"failed_ra": int, "failed_ppa": int, "details": [...]}``.
    A LOW_SHARPE failure with value < 1 counts as a PPA failure.
    """
    failed_ra = 0
    failed_ppa = 0
    details: List[dict] = []
    for check in checks:
        name = check.get("name", "")
        if check.get("result") != "FAIL":
            continue
        details.append({k: v for k, v in check.items()})
        if name in RA_CHECK_NAMES:
            failed_ra += 1
        if name == "LOW_SHARPE" and check.get("value", 1.0) < 1:
            failed_ppa += 1
    return {"failed_ra": failed_ra, "failed_ppa": failed_ppa, "details": details}


# ---------------------------------------------------------------------------
# Search constants
# ---------------------------------------------------------------------------

BATCH_SIZE = 4
PRODCORR_CEILING = 0.70
SHAPE_CLASSES = {"S1", "S4", "S5", "S9"}


# ---------------------------------------------------------------------------
# 闸门阶梯与并发口径（唯一事实源）
#
# skills / tools / tracking 一律引用本节，禁止在各自文档或脚本中复写数字。
# 背景：2026-08-23 审计实测 Sharpe 门槛在 skills 中并存 1.58/1.5/1.28/1.1 四个取值，
# Fitness 并存 1.0/0.75/1.6，并发槽位并存 5/8/6/4/3，判定结果取决于加载了哪份文档。
# ---------------------------------------------------------------------------

#: 内部严线——研究仿真阶段即要求，用于省配额的本地预筛。
GATES_INTERNAL: Dict[str, object] = {
    "sharpe_min": 1.58,
    "fitness_min": 1.0,
    "turnover_range": (0.05, 0.20),
    "margin_bp_min": 10.0,
    "returns_min": 0.05,
    "self_corr_max": 0.50,
}

#: 平台硬线——提交阶段平台实际判定口径，比内部线宽。
GATES_PLATFORM: Dict[str, object] = {
    "sharpe_min": 1.58,
    "fitness_min": 1.0,
    "turnover_range": (0.01, 0.70),
    "self_corr_max": 0.70,
    "prod_corr_max": PRODCORR_CEILING,
}

GATES: Dict[str, Dict[str, object]] = {
    "internal": GATES_INTERNAL,
    "platform": GATES_PLATFORM,
}

#: 七槽填槽并发模式（2026-08-25 更新：5→7，基于 Token-Bucket 模型 C≈7 实测）。旧「单批在飞串行」与固定槽位模型已废弃。
CONCURRENCY: Dict[str, object] = {
    "slots": 7,
    "burst_capacity": 7,
    "safe_instant_submits": 6,
    "min_batch_interval_sec": 45,
    "refill_sec_per_token": (20, 40),
}

# ---------------------------------------------------------------------------
# 选波 / S0 金字塔配额（2026-08-24 EUR Wave35–40 复盘）
#
# 根因：S0 的 category_weight + pyramidMultiplier 把 MODEL 打到 tier1，
# PV/NEWS 整座金字塔被挤出 generate 池；六波纯 MODEL 近闸全撞 prod≥0.7。
# 唯一 OS ACTIVE（Wj71Q12o）是 0.40 慢 MODEL × 0.60 快 PV，双金字塔。
# skills / toolkit / tracking thresholds 一律引用本节，禁止各写一套数字。
# ---------------------------------------------------------------------------

MINING: Dict[str, object] = {
    "pyramid_quota_enable": True,
    "pyramid_quota_non_model_min": 2,
    "category_weight_floor": 0.9,
    "category_weight_cap": 1.15,
    "cross_pyramid_slots_min": 2,
    "win_replay_slots_min": 1,
    "weak_probe_slots_max": 1,
    "prod_first_skeletons_per_slot": 2,
    "slow_fast_mix": {"slow_weight": 0.40, "fast_weight": 0.60},
    "follow_win_settings": True,
}


def gate_thresholds(stage: str = "internal") -> Dict[str, object]:
    """返回指定阶段的闸门阈值。stage ∈ {'internal', 'platform'}。"""
    try:
        return GATES[stage]
    except KeyError:
        raise ValueError(
            "unknown gate stage %r (expected 'internal' or 'platform')" % stage
        ) from None

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

REGION_PRIORITY: Dict[str, int] = {
    "USA": 3,
    "EUR": 2,
    "KOR": 2,
    "GLB": 2,
    "CHN": 1,
    "ASI": 1,
    "JPN": 1,
    "AMR": 1,
    "TWN": 1,
    "GBR": 1,
    "DEU": 1,
    "IND": 1,
    "MEA": 1,
    "HKG": 1,
}
