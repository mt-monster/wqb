"""wqb.config — region search space, operator families and gate helpers.

Single source of truth for region configuration (aligned with the platform
catalog as of 2026-08-13), operator family classification, ghost-operator
blacklist and WebDataScope gate accounting.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Optional, Set

REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Region search space
# ---------------------------------------------------------------------------

# 平台 dataset category 全集（2026-09-01 统一口径：以平台 get_datasets 的
# category 字段为准，勿按内容语义/描述推断——如 model50 内容为下行风险评估打分，
# 但平台分类为 model。来源：IND/TOP500/D1 实测 by_category 15 类 + 平台已知
# 合法类别 equity/event。区域差异由 S0 体检实测决定，不在本表裁剪。)
PLATFORM_CATEGORIES: List[str] = [
    "equity", "fundamental", "sentiment", "news", "analyst", "option",
    "shortinterest", "model", "earnings", "event", "pv", "risk",
    "insiders", "institutions", "imbalance", "macro", "other",
]

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

# S0 数据集白名单两阶段策略（2026-09-01 落地，实证依据：6 区 catalog 分布对比——
# cov 中位 0.666(EUR)~0.848(USA)、alphaCount 中位 12(CHN)~334(USA)，统一阈值对各区域
# 松紧不一且卡点维度不同，故"区域差异化"以两阶段分层实现而非每区自由阈值）：
#   阶段① 全局绝对底线（硬闸，不分区域）：见 DATASET_HEALTH_FLOOR，
#          保数据可用性质量底线，跨区可比、可复现；
#   阶段② 区域自适应相对排序（软）：各区域按自身 catalog 分位取 tier1/tier2 带，
#          参数落 tracking/<REGION>/config/thresholds.json 的 dataset_health
#          （tier_method=quantile + tier1/tier2_score_pct），由 toolkit
#          score_datasets.py 消费；结构性全灭类目（如 IND risk 4 集字段数不足）
#          在区域配置中显式标注，避免每波重查。
DATASET_HEALTH_FLOOR: Dict[str, float] = {
    "coverage_hard_min": 0.5,    # 低于此覆盖视为不可用数据，任何区域不放行
    "field_count_hard_min": 5,   # 低于此字段数无组合空间，任何区域不放行
}

# S0 评分目标对齐默认（2026-09-14 白名单机制 review 落地，P0/P2/P5）。
# 背景：原评分只优化「数据干净 + 低拥挤」，在 EUR 这种空 OS 池 + prod 极厚的饱和区
# 跑偏——它选出的冷门正交集（other296 天花板 S0.79）过不了 1.58 硬闸，而唯一真信号
# （continuation 族）又被生产池近同款吸收归零。以下默认全部 OFF/中性，保证未 opt-in
# 的区域逐条行为不变；区域在 tracking/<REGION>/config/thresholds.json 的 dataset_health
# 显式开启（EUR 已 opt-in）。toolkit score_datasets.py 消费，此处为唯一规范默认值来源。
DATASET_HEALTH_SCORING: Dict[str, object] = {
    # P0 经验强度先验：score 加 w×天花板比(best_sharpe/gate_sharpe)，把目标拉向「能过闸概率」。
    #   数据源 = calibrate 写入的 ledger dataset_empirical_prior.priors。0.0=关闭（旧行为）。
    "empirical_weight": 0.0,
    "empirical_prior_neutral": 0.5,   # 无历史数据时的中性先验（不奖不罚处女地）
    # P5 饱和区拍平 model 权重：区域进入饱和态（saturated_datasets 台账非空）时，
    #   model 类不再 ×category_weight 助推（拍平至 <=1.0），把排序交给 P0 经验项。
    "flatten_model_when_saturated": True,
    # P2 prod 饱和再验证：命中 saturated_datasets 台账的数据集自动降 excluded（防保底带复活）。
    #   仅在台账存在时生效，无台账零影响。
    "saturation_demotion_enable": True,
}

REGIONS: Dict[str, dict] = {
    "USA": {
        # ILLIQUID_MINVOL1M 已从平台档位表移除（2026-09-22 get_platform_setting_options 实测）。
        "universes": ["TOP3000", "TOP2000", "TOP1000", "TOP500", "TOP200", "TOPSP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP3000",
    },
    "EUR": {
        # 2026-09-22 实测：simulations 对 ILLIQUID_MINVOL1M 返回
        # "Universe ILLIQUID_MINVOL1M is not available."，故从档位表删除（旧值会误导选池）。
        "universes": ["TOP2500", "TOPCS1600", "TOP1200", "TOP800", "TOP400"],
        "_note": "EUR/D1 universe 档位以 get_platform_setting_options 为准（TOP2500/TOPCS1600/"\
                 "TOP1200/TOP800/TOP400）；实测 IS 强度集中在 TOP2500，换窄档塔陷（见 ledger "\
                 "EUR/universe_prod_isolation_probe_20260922）。",
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP2500",
    },
    "CHN": {
        "universes": ["TOP2000U"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP2000U",
    },
    "ASI": {
        # 平台 ASI/D1 仅提供 MINVOL1M/MINVOL10M/TOP500（2026-09-22 实测）。
        "universes": ["MINVOL1M", "MINVOL10M", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "MINVOL1M",
    },
    "GLB": {
        "universes": ["TOP3000", "MINVOL1M", "MINVOL10M", "TOPDIV3000"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP3000",
    },
    "JPN": {
        "universes": ["TOP1600", "TOP1200"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP1600",
        "_note": "平台 get_platform_setting_options 实测（2026-09-15）：仅 TOP1600/TOP1200；delay 0/1 均可用。",
    },
    "KOR": {
        "universes": ["TOP600"],
        # KOR campaigns start from SECTOR (empirical conclusion 2026-07).
        "neutralizations": ["SECTOR"] + [n for n in _USA_NEUTRALIZATIONS if n != "SECTOR"],
        "delays": [1],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP600",
        # 只给「新建战役目录」兜底（nodes/campaign._ensure_campaign_config）；建好后以 settings.json 为准。
        "default_neutralization": "STATISTICAL",
    },
    "AMR": {
        # 2026-09-22 get_platform_setting_options：AMR EQUITY D0/D1 均仅 TOP600。
        "universes": ["TOP600"],
        "neutralizations": ["NONE", "STATISTICAL", "MARKET", "SECTOR", "INDUSTRY",
                            "SUBINDUSTRY", "COUNTRY"],
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP600",
        "_note": "平台 get_platform_setting_options 实测（2026-09-22）：仅 TOP600；"
                 "neutralization 集合比 USA 少（无 CROWDING/FAST/SLOW 等）。",
    },
    "TWN": {
        "universes": ["TOP1000", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP1000",
        "_note": "平台 get_platform_setting_options 未列出，需确认是否仍可用",
    },
    "GBR": {
        "universes": ["TOP700"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [0, 1],  # GBR D0 threshold 2.69 measured
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP700",
    },
    "DEU": {
        "universes": ["TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP500",
    },
    "IND": {
        "universes": ["TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP500",
        "default_neutralization": "STATISTICAL",   # 同 KOR：只给新建战役目录兜底
    },
    "MEA": {
        "universes": ["TOP400", "TOP200"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP400",
        "_note": "平台 get_platform_setting_options 未列出，需确认是否仍可用",
    },
    "HKG": {
        "universes": ["TOP800", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP800",
    },
}

# 2026-10-04：删除 `_NEUTRALIZATION_BEST` / `neutralization_best()`。它零调用方，取值（EUR
# REVERSION_AND_MOMENTUM、GBR INDUSTRY）又与各区 settings.json 的实测档（都是 SUBINDUSTRY）相反，
# 是中性化「7 处来源」之一。区域缺省中性化以 tracking/<R>/config/settings.json 为准，组合级覆盖见
# tracking/<R>/config/cells.json（wqb.profiles 解析）。

#: 区域宇宙是否跨多个国家（平台区域定义的物理事实，不是实证结论）。
#: 用途：country 轴中性化 / 分组只在跨国宇宙里有意义——单一国家宇宙按 country 中性化等于按全市场中性化。
#: 此前 `structural_variants` 把 DEU / GBR（单一国家）和 EUR 一起写死成「优先 country 中性化」。
REGION_COUNTRY_SCOPE: Dict[str, str] = {
    "USA": "single", "EUR": "multi", "CHN": "single", "ASI": "multi", "GLB": "multi",
    "JPN": "single", "KOR": "single", "AMR": "multi", "TWN": "single", "GBR": "single",
    "DEU": "single", "IND": "single", "MEA": "multi", "HKG": "single",
}


def is_multi_country(region: Optional[str]) -> bool:
    """区域宇宙是否跨多个国家（未知区域按 False 处理）。"""
    return REGION_COUNTRY_SCOPE.get(str(region or "").upper()) == "multi"


def neutralization_search_order(region: str) -> List[str]:
    """Return the full neutralization sweep order for a region.

    Case-insensitive on the region code; raises ``KeyError`` for unknown
    regions.
    """
    return list(REGIONS[region.upper()]["neutralizations"])


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
        # 干净克隆下 data/operators_verified.json 被 gitignore 排除。回退到被追踪的
        # 平台目录快照 docs/reference/operators_catalog.json（get_operators 权威快照，
        # 103 个算子），否则 VERIFIED_SAFE_OPERATORS 为空 → op_arity/gate 守卫形同虚设。
        # 已验证 KNOWN_GHOST_SEED 与 catalog 零交集，差集不会清空幽灵黑名单。
        try:
            with open(REPO_ROOT / "docs" / "reference" / "operators_catalog.json",
                      "r", encoding="utf-8") as f:
                catalog = json.load(f)
            return {"verified": [r["name"] for r in catalog["results"]]}
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            return {}


_STATE = _load_operators_state()

VERIFIED_SAFE_OPERATORS: List[str] = list(_STATE.get("verified", []))

#: 常驻幽灵算子种子（2026-09-06 从代码固化，不再依赖审计产物）。
#:
#: 为什么必须写在代码里：operator_audit 的 library = verified ∪ ghost，两者都读
#: operators_verified.json —— 一旦某次审计把 ghost 写空，library 就退化成 verified，
#: 下一次 `ghost = library - live` 恒为空集，黑名单再也回不来。这是个自擦除棘轮。
#: 2026-09-04 的审计（probe_mode=submit-then-cancel，只探平台已有的 102 个算子、
#: total_not_found=0）正是这样把 17 个幽灵清成 0 的，GHOST_OPERATORS 随之塌到
#: 只剩硬编码的 neutralize，ensure_safe_for_dispatch 形同虚设。
#:
#: 这些名字在论坛帖与旧笔记里满天飞，但平台上不存在；"平台没有" 不会因为某次
#: 探针没去探它就变成 "平台有了"。审计可以往这个集合里 **增补**，但不能删减 ——
#: 唯一的移除路径是它出现在 verified 里（下方求差集），即平台真的上线了该算子。
#: 替换映射表见 docs/reference/community_tpl_library_sequel.md §十八。
KNOWN_GHOST_SEED: Set[str] = {
    "group_median",
    "group_normalize",
    "group_percentage",
    "group_vector_proj",
    "s_log_1p",
    "sigmoid",
    "tanh",
    "ts_co_kurtosis",
    "ts_decay_exp_window",
    "ts_delta_limit",
    "ts_entropy",
    "ts_median",
    "ts_min_max_cps",
    "ts_min_max_diff",
    "ts_partial_corr",
    "ts_percentage",
    "ts_skewness",
    # 2026-10-22 平台实测新增：论坛骨架 `to_nan(x, value=0, reverse=true)` 在 REGULAR
    # FASTEXPR 上被平台拒为 "Attempted to use inaccessible or unknown operator"。
    # 平台只有 is_nan / if_else，没有 to_nan。归档时它不在 catalog 里，当时
    # op_arity 对未知算子一律放行（arity 通过 ≠ 平台可用），只能靠 gate.py 的幽灵闸拦。
    # 2026-10-23 起 op_arity 本身 fail-closed（目录外的算子直接报 [UNKNOWN_OP]），
    # 本集合的作用变成：给已知幽灵一个**带替代建议**的 [GHOST] 专属报错。
    "to_nan",
}

# 2026-09-01 兼容：operators_verified.json 的幽灵键存在两代 schema
# （旧 known_ghosts / 新 ghost，operator-audit 工具已切新键），双读防漂移。
GHOST_OPERATORS: Set[str] = (
    KNOWN_GHOST_SEED
    | set(_STATE.get("known_ghosts", []))
    | set(_STATE.get("ghost", []))
    | {"neutralize"}
)

# Sanity guard: verified and ghost sets must stay disjoint.
GHOST_OPERATORS -= set(VERIFIED_SAFE_OPERATORS)


def is_news_dataset(name: str, category: Optional[str] = None) -> bool:
    """Detect news/sentiment datasets by prefix or category."""
    if category == "news":
        return True
    prefix = name.lower()
    return prefix.startswith("news") or prefix.startswith("snt")


# ---------------------------------------------------------------------------
# WebDataScope gate accounting（RA / PPA 资格门失败计数）—— 唯一实现
# ---------------------------------------------------------------------------
# 口径 = WebDataScope-0.10.20 src/scripts/background.js::getAlphaCheckStates（平台插件）：
#   * 一项 check 计入失败 ⇔ result 既不是 PASS 也不是 PENDING（WARNING / ERROR 都算）；
#   * RA 计下列 18 项（IS_LADDER_SHARPE 对 ATOM 豁免但仍计；.WITH_RATIO 变体 2026-09-08 补入——
#     平台同样以 FAIL 拦 REGULAR 提交，漏计时 23 条"零硬闸失败"候选里误放 3 条）；
#   * PPA 计下列 7 项，外加 LOW_SHARPE 的 value < 1。
#
# 2026-09-27 R3（审计 N3）：此前本模块另有一份口径相反的分叉实现——8 项、只数 FAIL、
# 含平台不存在的 HIGH_DRAWDOWN / LOW_SELFCORR / LOW_PNL，同一组 checks 生产口径
# failed_ra=3、这里给 0；而 AGENTS.md 把本模块定为唯一事实源，照规范引用就会踩中。
# 现 world-quant-brain-mcp/mcp_core.py（`_slim_checks`）与 tools/build_gate_prior_from_inventory.py
# 都引用这里；mcp_core 另留一份 Docker 镜像（只打包 MCP 目录、没有 src/）用的冻结副本，
# 与本段的一致性由 tests/unit/05_submit_quota/test_r3_failed_count_single_source.py 断言。

#: 2 年 sharpe 读数所在的两个 check（值即 two_year_sharpe）
RA_2Y_NAMES = ("LOW_2Y_SHARPE", "IS_LADDER_SHARPE")

RA_CHECK_NAMES: FrozenSet[str] = frozenset([
    "HIGH_TURNOVER", "LOW_TURNOVER", "LOW_FITNESS", "LOW_RETURNS", "LOW_SHARPE",
    "LOW_GLB_AMER_SHARPE", "LOW_GLB_APAC_SHARPE", "LOW_GLB_EMEA_SHARPE", "LOW_ASI_JPN_SHARPE",
    "IS_LADDER_SHARPE",
    "LOW_2Y_SHARPE", "LOW_SUB_UNIVERSE_SHARPE", "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE", "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
    "LOW_ROBUST_UNIVERSE_RETURNS", "CONCENTRATED_WEIGHT",
    "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO",
])

PPA_CHECK_NAMES: FrozenSet[str] = frozenset([
    "LOW_TURNOVER", "HIGH_TURNOVER", "LOW_SUB_UNIVERSE_SHARPE", "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO", "LOW_ROBUST_UNIVERSE_RETURNS",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
])


def check_counts_as_failed(result: Any) -> bool:
    """WebDataScope 口径：result 既非 PASS 也非 PENDING 即计入失败（WARNING / ERROR / 缺失都算）。"""
    return result != "PASS" and result != "PENDING"


def compute_webdata_failed_counts(checks: Optional[Iterable[Any]]) -> Dict[str, Any]:
    """按 WebDataScope 口径统计 alpha ``is.checks`` 的 RA / PPA 资格门失败项。

    返回 ``{"failed_ra", "failed_ppa", "ra_failed_names", "ppa_failed_names", "details",
    "ra_items", "ppa_items", "pending_ra", "pending_ppa", "ra_pending_names", "ppa_pending_names"}``：
    两个计数、按 checks 原顺序的失败项名，计入任一失败的 check 原文（details），以及按 RA / PPA 分开的
    逐条 ``{name,result,value,limit}``（``ra_items`` / ``ppa_items``；2026-09-29 增，供 submit_verdict
    逐条列名，避免另抄一份口径）。非 dict 的条目跳过。

    ``pending_*``（2026-09-29 增，skills 审查 RF-03）：**名单内**检查仍为 PENDING 的个数与名字。口径不变
    （PENDING 不计失败，与平台「不挡提交」一致），但 ``failed_ra == 0`` 在 ``pending_ra > 0`` 时只表示
    「暂无失败」而非「已通过」——调用方须等其算完再判，不得据此放行。
    """
    failed_ra = failed_ppa = 0
    ra_names: List[str] = []
    ppa_names: List[str] = []
    ra_pending: List[str] = []
    ppa_pending: List[str] = []
    details: List[dict] = []
    ra_items: List[dict] = []
    ppa_items: List[dict] = []
    for check in checks or []:
        if not isinstance(check, dict):
            continue
        name, res, val = check.get("name"), check.get("result"), check.get("value")
        if res == "PENDING":
            if name in RA_CHECK_NAMES:
                ra_pending.append(name)
            if name in PPA_CHECK_NAMES:
                ppa_pending.append(name)
        bad = check_counts_as_failed(res)
        ra_hit = name in RA_CHECK_NAMES and bad
        ppa_hit = (name in PPA_CHECK_NAMES and bad) or (
            name == "LOW_SHARPE" and isinstance(val, (int, float)) and val < 1)
        item = {"name": name, "result": res, "value": val, "limit": check.get("limit")}
        if ra_hit:
            failed_ra += 1
            ra_names.append(name)
            ra_items.append(dict(item))
        if ppa_hit:
            failed_ppa += 1
            ppa_names.append(name)
            ppa_items.append(dict(item))
        if ra_hit or ppa_hit:
            details.append(dict(check))
    return {"failed_ra": failed_ra, "failed_ppa": failed_ppa,
            "ra_failed_names": ra_names, "ppa_failed_names": ppa_names, "details": details,
            "ra_items": ra_items, "ppa_items": ppa_items,
            "pending_ra": len(ra_pending), "pending_ppa": len(ppa_pending),
            "ra_pending_names": ra_pending, "ppa_pending_names": ppa_pending}


def merge_failed_items(counts: Dict[str, Any], *, ppa_bonus: bool = False) -> Dict[str, Any]:
    """RA ∪ PPA 失败项并集（fail-closed 判定用；2026-10-27 P0）。

    **为什么不能只按某一通道计数**：``PPA_CHECK_NAMES ⊂ RA_CHECK_NAMES``，且 PPA 额外把
    ``LOW_SHARPE < 1`` 记为失败 ⇒ 两个集合**只有 PPA 独有项，没有 RA 独有项**。因此
    「按 PPA 计数」等于只数了一个更小的子集：``LOW_FITNESS`` / ``LOW_2Y_SHARPE`` /
    ``IS_LADDER_SHARPE`` / ``LOW_GLB_*_SHARPE`` 等**只在 RA 名单里**的失败会被整片漏掉。

    平台会给 **REGULAR 提交成功**的 alpha 自动打 ``PowerPoolSelected`` 标签
    （2026-10-27 JjeMlmXA 实证），``is_ppa_alpha`` 据此判 PPA ⇒ 提交闸/判定层会去看
    ``failed_ppa``，从而放过 ``Failed RA>0`` 的候选。故一律以 RA 项为**下界**：

    - 基础集 = ``ra_items``（RA 名单内的真实失败，任何通道都必须拦）；
    - ``ppa_bonus=True``（确属 PPA 通道）时并入 ``ppa_items`` 的额外项
      （即 ``LOW_SHARPE`` 结果 PASS 但 value<1 这类 PPA 专有规则）。

    返回 ``{"count", "names", "items"}``，``items`` 按 checks 原顺序且按 name 去重。
    """
    merged: Dict[str, dict] = {}
    for it in counts.get("ra_items") or []:
        if isinstance(it, dict) and it.get("name") is not None:
            merged.setdefault(str(it["name"]), it)
    if ppa_bonus:
        for it in counts.get("ppa_items") or []:
            if isinstance(it, dict) and it.get("name") is not None:
                merged.setdefault(str(it["name"]), it)
    items = list(merged.values())
    return {"count": len(items), "names": list(merged), "items": items}


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
    # 2026-11-16 用户指令：prod 内部严线 0.65（平台硬线仍 0.70，见 PRODCORR_CEILING）。
    # 留 0.05 缓冲，挡住「提交时贴线过、48h 后池漂移翻闸」的件（实证 78LpqZYQ 0.697）。
    "prod_corr_max": 0.65,
}

#: 平台各检查的**官方线**（how-to-pass 参考文档；Delay-1 / Delay-0），按检查名分开登记
#: （skills 审查 X-11，2026-09-29）。此前把它们揉成一个 ``sharpe_min=1.58``，导致 IS Sharpe（1.25）与
#: 2Y Sharpe（1.58）两条不同检查在文档里互相顶替。``low_2y_sharpe_min`` 取自仓库对
#: LOW_2Y_SHARPE / IS_LADDER_SHARPE 的实测 limit。
PLATFORM_CHECK_LINES: Dict[str, object] = {
    "low_sharpe_min": {"delay1": 1.25, "delay0": 2.0},      # LOW_SHARPE
    "low_fitness_min": {"delay1": 1.0, "delay0": 1.3},      # LOW_FITNESS
    "turnover_range": (0.01, 0.70),                          # LOW_TURNOVER / HIGH_TURNOVER
    "low_2y_sharpe_min": 1.58,                               # LOW_2Y_SHARPE / IS_LADDER_SHARPE
}

#: 提交准入线（库存 / submit_queue / region_rotation / judge 共用）。命名沿用「平台硬线」，但注意语义：
#: ``sharpe_min`` = 平台 2Y 线（1.58），**不是**平台 LOW_SHARPE 线（Delay-1 为 1.25，见 PLATFORM_CHECK_LINES）；
#: 实际约束的是 2Y 线，IS Sharpe 1.25–1.58 之间的候选多半死在 LOW_2Y_SHARPE。
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

#: 篮子两两互相关上限（唯一事实源）。2026-11-09 由 0.5 放宽到 0.7：平台 self/prod 硬线均 0.7，
#: 论坛社区篮子去重亦「先 0.7 看簇结构、再决定是否加严」（阈值拧太紧→短名单空了）。
#: 0.5 过严会误伤真·不同机制的跨集组合（KOR E56jA0AP S1.58/2Y2.15/fRA0 因与 analyst10/insiders5
#: ATOM 互相关 0.61/0.66 被挡）。防同源充数改靠 basket_diversity_gate 的簇识别 + 结构多样性审查，
#: 而非一味压低本阈值。select_ra_basket / basket_diversity_gate 引用本值；--threshold 可覆盖。
BASKET_MUTUAL_CORR_MAX: float = 0.7

#: 篮内同一数据集过度集中警戒线：超过该颗数触发结构多样性 WARN（防同源充数）。
#: 放宽互相关阈值后，同数据集兄弟可能 0.6x 相关仍过阈，用本警戒点名而非硬禁。
BASKET_DATASET_CONCENTRATION_WARN: int = 2


# ---------------------------------------------------------------------------
# 梯度扫描纪律（2026-11-23 落地；用户「三、优化空间 全部落地」裁定）
#
# 背景：insiders1 在 11-06~11-08 跑完 30+ 臂（窗口/幅度/设置轴）后写下「全轴穷尽」，
# 复审核对平台读回的真实表达式后发现 **4 个算子类别轴一格未扫**（L1 vec 折叠 /
# L4 时序 / L5·L8 外层 group / 分组轴）。补齐 45 臂后 S 不动但 2Y +0.15 / sub +0.05 /
# robust +0.08，并证伪两条跨集外推律。
#
# 三处落点：
#   ① 本节常量 = 扫描顺序 / 参数层 / no-op 律 / 批级设置（唯一事实源）
#   ② `tools/research/gradient_coverage.py` = 覆盖率审计 + 缺臂计划 + 算子 lint
#   ③ `docs/experience/02_signal_patterns.md` §19 = 人看版纪律
# ---------------------------------------------------------------------------

#: 层扫描顺序 = **杠杆量级降序**（实测类内 ΔS，见 `tracking/EUR/reference/datasets/insiders1.md` §11.1）。
#: 语义层（类内 ΔS > 0.30）必须全类替换；参数层（ΔS < 0.05）一轮即可，禁止精调。
GRADIENT_SCAN_ORDER: tuple = (
    "L1_vector_fold",      # vec_* 折叠 —— ΔS 0.40（sum≡avg > max > min ≫ stddev≈range）
    "L2_arithmetic",       # add/subtract/multiply/divide —— 结构固定，只查量纲坑
    "L3_logical",          # greater/less/if_else 条件
    "L4_time_series",      # ts_* —— ΔS 1.40（最大杠杆；稀疏事件流 ts_sum 不可换）
    "L5_group_inner",      # 内层 group_* —— ΔS 0.77
    "L6_cross_sectional",  # rank/winsorize/quantile/normalize
    "L7_transform",        # tail/bucket/trade_when
    "L8_group_outer",      # 外层 group_*
    "L9_grouping_axis",    # industry/sector/market/subindustry/country/exchange —— ΔS 0.11 / Δ2Y 0.20
    "L10_window",          # 窗口 —— 半语义（S↔2Y 跷跷板，须报双指标）
    "L11_amplitude",       # winsorize std / signed_power / quantile —— 参数层
    "L12_tail_q",          # tail(lower,upper) —— 参数层
    "L13_settings",        # decay / truncation / universe / 中性化 —— 批级参数，一值一批
)

#: 参数层（类内 ΔS < 0.05）：一轮扫描即可，**禁止在参数层反复精调**。
GRADIENT_PARAM_LAYERS: frozenset = frozenset({"L11_amplitude", "L12_tail_q", "L13_settings"})

#: 分组轴候选（EUR 全集实测序：sector > market > industry > subindustry > country ≡ exchange；
#: 跨区必须先实测再排序，本元组只定义"要扫哪些"，不定义优劣）。
GRADIENT_GROUPING_AXES: tuple = (
    "industry", "sector", "market", "subindustry", "country", "exchange",
)

#: 窗口探针（跨越 1 月/季/半年/年/两年）；窗口是半语义层，须同时报 S 与 2Y（常见严格跷跷板）。
GRADIENT_WINDOW_PROBES: tuple = (22, 44, 66, 88, 126, 252)

#: 参数层探针（一轮即可）
GRADIENT_TAIL_Q_PROBES: tuple = ((0.15, 0.85), (0.25, 0.75), (0.35, 0.65))
GRADIENT_AMPLITUDE_PROBES: dict = {"winsorize_std": (2, 3, 4)}

#: 批级设置：属于 `create_multi_simulation` 的**批级**参数，同批内所有臂共享
#: ⇒ **不能在批内做梯度**，必须一值一批（2026-11-23 实测因同批放同码臂白烧 1 个臂位）。
GRADIENT_BATCH_LEVEL_SETTINGS: tuple = (
    "decay",
    "truncation",
    "universe",
    "neutralization",
    "nan_handling",
    "max_trade",
    "pasteurization",
    "delay",
)

#: 已确认的 no-op 律（换上去读数逐位相同 ⇒ 不必再花臂位）。工具按层/结构触发提示。
GRADIENT_NOOP_LAWS: dict = {
    "monotone_before_group_rank": (
        "group_rank 之前的任何单调变换（constant/quantile/signed_power/winsorize）数学上是空操作"
    ),
    "vec_sum_equiv_vec_avg": (
        "下游有 rank/group_rank 吸收尺度时 vec_sum ≡ vec_avg（risk60 + insiders1 两集复现）"
    ),
    "truncation_after_rank": (
        "最终层是 rank()/group_rank()/quantile() 时 truncation 是结构性 no-op"
        "（insiders1 trunc 0.05 与 0.08 三臂读数逐位相同）"
    ),
    "inner_backfill_makes_group_backfill_noop": (
        "内层已有 ts_backfill ⇒ 外层 group_backfill 不改变任何读数（risk60 实证）"
    ),
    # ── 2026-11-23 用户「三、优化空间 全部落地」补入（insider_agg_matrix 163 臂 + risk60 实证）──
    "zscore_on_already_standardized_field": (
        "字段本身已是无量纲 0/±1 指示器（如 directional_indicator）时再 ts_zscore ⇒ 近似常数"
        "⇒ 实测 TO 0.00 / S 0.00（insiders N7 整臂归零）"
    ),
    "signed_power_on_positive_rank_shell": (
        "正值核 + group_rank 壳上 signed_power(·,2) 是 no-op（读数逐位相同；rank 只吃序，平方不改序）。"
        "同一条杠杆在别的核上可能是最强杠杆 —— 见 GRADIENT_NONPORTABLE_LEVERS"
    ),
    "decay_noop_when_turnover_already_low": (
        "TO 已低于 ~2% 时提高 decay 是 no-op（无平滑对象）：risk60 T2 的 d4/d8/d16 三臂"
        "读数逐位相同（0.77/1.02/1.62/0.94）。decay 只对 TO 尚在正常区间的核有效"
    ),
    "group_aggregator_always_collapses": (
        "group_sum / group_std_dev 这类聚合型外层算子一律崩：TO 70%+ / RA 5–6"
        "（risk60/68 与 insiders 合计 10 次复现）⇒ 结构型死因，不必再试"
    ),
}

#: **跨核不可移植的杠杆登记表**（2026-11-23 用户「三、优化空间」#2 落地）。
#:
#: 教训：同一个杠杆在不同核上可以是「最强杠杆 / 纯损害 / no-op」三种完全相反的结论
#: （本轮踩 4 次、约 60 臂）。因此**杠杆结论必须带「核指纹」登记，禁止跨核继承**；
#: 换核后必须重测该杠杆再引用。消费点：`tools/gates/gradient_stop_gate.py` 的 D1/D2
#: 与 `tools/research/gradient_coverage.py` 的 noop 告警可读本表打印提示。
GRADIENT_NONPORTABLE_LEVERS: dict = {
    "signed_power_2": {
        "strong_on": {
            "kernel": "risk60 T2 cost-curve（vec_avg(offer)-vec_min）的 group_neutralize 壳",
            "delta": {"S": "+0.11", "F": "+0.36"},
        },
        "harmful_on": {
            "kernel": "risk60 T3 spread-ratio 的 group_zscore 壳",
            "delta": {"sub": "0.69 → 0.57", "RA": "3 → 5"},
        },
        "noop_on": {
            "kernel": "insiders N1 total_buy/avg_buy 的 group_rank 壳（正值核）",
            "delta": "读数逐位相同",
        },
    },
    "ts_mean_smoothing": {
        "harmful_on": {
            "kernel": "insiders N1 参与广度（变动型：人数每日变）",
            "delta": {"S": "0.66 → 0.20"},
        },
        "near_free_on": {
            "kernel": "risk60 T4 双残差 add（水平型）与 insiders N2 角色分歧（水平型）",
            "delta": {"S": "1.25 → 1.24（risk60）/ +0.01（N2）", "TO": "N2 0.547 → 0.109（−44pp）"},
        },
        "harmful_on_flow_kernel": {
            "kernel": "PV1 四腿（volume / ts_corr / 换手 / 波动，流量型）—— 2026-11-23 双尺度移植批",
            "delta": {
                "S": "1.39 → 1.15（共尺度）/ 1.06（双尺度慢66）/ 0.80（双尺度慢252）",
                "TO": "11.9% → 8.6% / 6.6% / 6.7%",
            },
            "note": (
                "★ 双尺度比纯平滑更差（1.06 < 1.15）⇒「慢腿+快腿相加能救平滑」只在水平型核成立"
                "（risk60 双尺度 1.34 > 慢腿单独 1.24），流量型核上慢腿平滑掉的正是信号本身"
            ),
        },
    },
    "raise_decay": {
        "effective_on": {
            "kernel": "insiders N2 ts_zscore(role,252)（TO 54.7%）",
            "delta": {"TO": "−44pp", "S": "+0.01"},
        },
        "noop_on": {
            "kernel": "risk60 T2 cost-curve（TO 已 1.3%）",
            "delta": "d4/d8/d16 逐位相同",
        },
    },
    "lower_truncation": {
        "noop_on": {
            "kernel": "risk60 T1 ts_max_diff 与 T3 spread-ratio 的 rank/gz 壳",
            "delta": "0.02/0.04/0.08 逐位相同",
        },
        "harmful_on": {
            "kernel": "risk60 T2 cost-curve 的 SECTOR 轴",
            "delta": {"F": "1.03 → 0.85", "2Y": "1.62 → 1.48", "RA": "2 → 4"},
        },
    },
    "vector_fold_choice": {
        "max_over_avg": {
            "kernel": "KOR 全 VECTOR 数据集（尾部摩擦最强的折叠基）",
            "delta": {"2Y": "vec_max 1.70 过闸，vec_avg 未过"},
        },
        "harmful_on": {
            "kernel": "DEU sentiment7 snt7_all_languages_views（向量维 = 语言 × 访问类型）",
            "delta": {"S": "vec_avg 2.03 → vec_max 1.41", "F": "1.61 → 0.94", "RA": "0 → 4（含 IS_LADDER 第4年）"},
            "note": (
                "★ vec_max 取到「最热单一语言页」这一噪声最大的分量 ⇒ 「max > avg」不是通用律，"
                "归约选择须逐核实测；向量维若本身是「同一量的分项拆分」，avg 才是聚合、max 是抽取极值"
            ),
        },
    },
}

#: 全局提交闸（**fail-closed**）：`=1` 才允许 workflow 提交 alpha——它只解除闸门，
#: **不等于自动提交**：真正提交仍需 `confirm_submit=True` + 用户明确确认（AGENTS.md §7）。
#: ⚠ 本模块唯一的 `os.environ` 读取点，且是文档已承诺的口径：`docs/env_registry.json` 把
#:    `WQB_ALLOW_ALPHA_SUBMIT` 的读取方登记为 `src/wqb/config.py` + `mcp/main.py`；
#:    `world-quant-brain-mcp/main.py` 按仓库根 `setdefault("WQB_ALLOW_ALPHA_SUBMIT", "1")`
#:    （HTTP 常驻模式下客户端不起进程、无人注入 env，服务端自带兜底）。
#:    读取时机 = 导入时，所以只对当次进程生效（与 submit_alpha 节点的说明一致）。
#:    ⚠ 消费点：`wqb.workflow.nodes.submit_alpha` 在文件头导入它——名字缺失时 registry
#:    只打 WARNING 就跳过注册 ⇒ `submit_alpha` 节点**静默消失**（2026-10-06 实测：
#:    HEAD 自带这个断链，`workflow_list_nodes` 返 19 个而非 20，提交链不可用）。
ALLOW_ALPHA_SUBMIT: bool = os.environ.get("WQB_ALLOW_ALPHA_SUBMIT", "") == "1"

#: 等待 / 退避 / 卡住阈值（**唯一来源**，skills 审查 X-15，2026-09-29）。
#: 文档（poll-and-quota.md 的阈值表、submit-alpha、super-alpha、monitor）只按键名引用，不再抄数字；
#: 与代码常量的一致性由 tests/unit/07_docs_skills/test_wait_thresholds.py 守护。
WAIT_THRESHOLDS: Dict[str, object] = {
    # POST /submit 返回 201/202（异步受理）后，等 alpha 状态离开 UNSUBMITTED 的窗口。平台翻转实测 2–3 min；
    # 窗口内未翻 → re-POST 补发一次（幂等）→ 再等一个窗口 → 仍未翻记 ASYNC_STUCK 并知会用户。
    "submit_flip_wait_s": 240,
    "submit_flip_poll_s": 5,           # 状态轮询间隔（get_alpha_details）
    "submit_repost_max": 1,            # 窗口内未翻转时 re-POST 的最大次数
    # check_correlation（prod/self 相关性）阻塞轮询：账号级单并发，忙时立即返回 correlation_busy
    "prod_corr_poll_s": 30,
    # 2026-10-22：**3600 → 900**（P0-1：60 分钟轮询把平台单并发槽堵死一小时）。
    # 账号级单并发下，一个卡住的 alpha 按 60 min 占槽 ⇒ 整账号的相关性查询全部空转
    # （实测：另一会话的 prod 队列脚本卡住时，本会话空转 800s+ 才出数；杀掉后同一条
    # 1499s 才拿到值）。超时按 `pending` 返回（不缓存、不判死），调用方隔段时间重查。
    # 跨进程互斥（logs/_dblock/correlation.lock.json）见 brain_mixin_transport。
    # 2026-10-26：900 → 120。**动机仍成立**：本地锁覆盖整个轮询窗口，窗口多长，
    # 单次调用就占账号级单槽多久（900s = 15 分钟，其他会话/战役全部 busy）。
    # ⚠ 2026-10-28 修正**取值**：120s 短于平台正常耗时。用户口径「一次 prod 正常
    # 查询 180–200 s」。当初定 120 用的「实测 94s/条」是 2026-10-06 在 900s 窗口下的
    # 旧观测；2026-10-28 那次 14h 取证里的「成功耗时最大 117s」是**被 120s 窗口截断的
    # 样本**——超过窗口的计算一律记 pending，永远进不了"成功耗时"（幸存者偏差），
    # 不能用它反证 120s 够。现取 240 = 正常上限 200 + 一个 30s 慢轮询台阶 + 抖动余量：
    # 正常计算能在**一次调用内**拿到值；120s 下每条真实计算都必然 pending → 195s 冷却
    # → 再查，端到端 ~300s 且多绕一轮。卡住的 alpha 至多堵 4 分钟（仍远小于 900s）。
    "prod_corr_timeout_s": 240,
    # 在飞回测的卡住判定（toolkit poller）：progress 连续 stall_min 无变化判 STALLED；总时长超 timeout_min 判超时
    "sim_stall_min": 60,
    "sim_timeout_min": 360,
}

#: 回测并发口径。**2026-10-06 用户定案：7 → 2**。
#: 背景：账户级实测容量 C≈7（2026-08-25 由 5→7，基于 Token-Bucket 模型），但那是“能跑”的
#: 上限而非安全水位：多条流水线 / 并行会话共用同一账号槽位，跑满会频繁 429 + 退避，
#: 总吞吐反而下降；7 槽也直接诱发过 2026-10-02 的 pipeline 主线程自锁（见
#: `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/slots.py`，现已用
#: `acquire(nonblock=True)` 修掉，cap=2 是叠加的第二重保险）。
#: 临时提高可用环境变量 `WQB_GLOBAL_SLOTS=<n>`（不改动本常量）。
#: 旧「单批在飞串行」与固定槽位模型已废弃。
CONCURRENCY: Dict[str, object] = {
    "slots": 2,
    "burst_capacity": 2,
    "safe_instant_submits": 2,
    "min_batch_interval_sec": 45,
    "refill_sec_per_token": (20, 40),
}

# ---------------------------------------------------------------------------
# 选波 / S0 金字塔配额（2026-08-24 EUR Wave35–40 复盘）
#
# 根因：S0 的 category_weight + pyramidMultiplier 把 MODEL 打到 tier1，
# PV/NEWS 整座金字塔被挤出 generate 池；六波纯 MODEL 近闸全撞 prod≥0.7。
# 唯一 OS ACTIVE（Wj71Q12o）是 0.40 慢 MODEL × 0.60 快 PV，双金字塔。
# ⚠ 该「加权混合」形态自 2026-09-13「路线 A」起已废止（gate 闸5 block）：可继承的
#   只有其跨数据集补腿意图，落地须改写为结构交互（ts_corr / divide / 条件 / 分组）。
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
    # ⚠ 历史参数，已废止：仅存作相关性估算/历史归档，**禁止用于生成表达式**
    #    （闸5 毒模式 weighted_signal_mix / weighted_leg_mix_func_* 全量拦截）
    "slow_fast_mix": {"slow_weight": 0.40, "fast_weight": 0.60},
    "_slow_fast_mix_status": "deprecated_20260913_route_a",
    "follow_win_settings": True,
}

#: 标准时间窗口白名单（2026-09-17 新增）。
#: SOP 两处（`wq-brain-ra-pipeline` 步 4 / `brain-make-some-gem`）都要求"只用标准窗口；
#: 其他窗口须给出解释或实测证据"，但此前**只写在散文里、零机械守护** ——
#: 实测全库 23% 用了非白名单窗口，Top 恰为 20/10/120/60，与 toolkit
#: `_lib/operator_coverage.py::_DEFAULT_WINDOWS` 的旧默认值 `[20,60,120,5,10,252]`
#: 完全吻合（该默认值已同轮对齐，见其注释）。
#: 本常量与 `wq-brain-campaign-toolkit/config/platform_constraints.json::window_whitelist`
#: 同源，由 `tests/unit/06_wave_pipeline/test_window_whitelist_p4.py` 守护两边一致。
STANDARD_WINDOWS: List[int] = [1, 5, 22, 66, 252, 504, 1008, 1260]


# ---------------------------------------------------------------------------
# 伪 alpha 字段黑名单（2026-09-26 落地，P1.2 / 评估去污染）
#
# 实证依据（2026-09-26 字段分类→GEM 收益评估）：`dl_riskfree_returns`（无风险
# 收益率）这类字段做信号本质是做多/做空无风险利率——sharpe 虚高（实测 avg 4.16）
# 但无 alpha 价值，prod_corr 必爆。同类的基准收益 / raw beta / 市场指数同理：
# 它们是 beta/carry，不是选股能力。用于评估时会把机制收益污染成正收益，
# 用于生成时会产出过不了 prod 墙的废品。
#
# 用法（单源，勿在他处复写）：
#   - 评估侧：tools/field_pool_ab.py 剔除命中字段/数据集后再对比
#   - 生成侧：GEM 字段池构建时剔除（防污染候选池）
# 匹配口径：大小写不敏感的子串命中（字段名或数据集 id）。
# ---------------------------------------------------------------------------

#: 伪 alpha 字段/数据集关键词（命中即视为非选股 alpha，评估剔除 + 生成拒绝）。
PSEUDO_ALPHA_PATTERNS: List[str] = [
    "riskfree", "risk_free", "risk_free_rate", "rf_rate", "_rf_", "rf_",
    "benchmark", "market_return", "market_ret", "mkt_return", "mkt_ret",
    "index_return", "index_ret", "index_price",
    "beta", "raw_beta",
]


def is_pseudo_alpha(name: str) -> bool:
    """字段名/数据集 id 是否属伪 alpha（riskfree/beta/基准收益类）。

    大小写不敏感子串匹配 PSEUDO_ALPHA_PATTERNS。评估/生成两侧共用。
    """
    if not name:
        return False
    low = str(name).lower()
    return any(p in low for p in PSEUDO_ALPHA_PATTERNS)



# ---------------------------------------------------------------------------
# 数据集名形状（2026-11-06 落地，防 `datasets` 表伪数据集行复发）
#
# 背景：`CampaignStore._ensure_dataset(region, name)` 会按传入的**任意字符串**
# 现建 `datasets` 行，而 `_ensure_wave` / `_backtest` 把**塔位组合标签**
# （`risk/model`、`pv/model/other`）、**表达式描述**（`fundamental44|institutions6`）、
# **region 名**（`KOR`）原样透传进去 ⇒ 实测 82 行从来不是数据集的行落进表里，
# 污染任何以该表为基础的统计（按集数排名、按 category 分组、覆盖度分母…）。
#
# 历史清理 = `tools/db/datasets_phantom_repair.py`；写入口守卫 = `_ensure_dataset`。
# 两侧共用本函数（单源，勿在他处复写）。
# ---------------------------------------------------------------------------

#: 平台 `/data-sets` 的 dataset id 形状：小写字母开头，仅小写字母/数字/下划线。
DATASET_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")

#: store 刻意使用的「未知数据集」哨兵名（`_backtest` / `_alphas` 硬编码）。
#: 它不是平台数据集，但形状上被本函数放行 —— 语义是「不知道」，不是假名。
DATASET_SENTINEL: str = "_unknown"


def is_phantom_dataset_name(name: Optional[str]) -> bool:
    """`datasets.name` 是否是伪数据集名（不可能是平台 dataset id）。

    口径 = **形状**：平台 dataset id 形如 `fnd6` / `anl4` / `other455`，恒为
    小写字母开头 + `[a-z0-9_]`。塔位组合标签（`pv/model/other`）、表达式描述、
    region 名（`KOR`）、带空格/中文/斜杠/竖线/逗号的串一律不合形。

    `DATASET_SENTINEL`（`_unknown`）放行；**空 / None 视为伪名**（调用方无法
    表达「无名数据集」，历史脏行里确有 region 名被当成空串透传的情形）。

    注意：本函数只判**形状**。id 形的假名（例：把 region 名写成小写）需要平台
    目录才能识破，走 `tools/gates/category_coverage_audit.py --show-extra-local`
    （其 `extra_local` = 「本地有、平台无」的差集）。
    """
    n = (name or "").strip()
    if not n:
        return True
    if n == DATASET_SENTINEL:
        return False
    return DATASET_NAME_RE.match(n) is None


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
