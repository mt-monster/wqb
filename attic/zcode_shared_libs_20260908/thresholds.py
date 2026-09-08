"""
BRAIN 提交硬门槛 — 单一事实源 (Single Source of Truth)
=======================================================

所有 skill 中出现的 Sharpe / Fitness / Turnover / 相关性 / 配额阈值一律
以本文件为准, 不得在 SKILL.md 中再复制数值。

维护纪律: 平台门槛变化时 **只改这里**, 然后 grep 各 SKILL.md 确认无残留旧值。

来源标注:
- [PLATFORM]  平台 AlphaTest / 提交检查实测 (2026-08-11 GBR 战役 / 2026-08-13 EUR 战役)
- [MCP-LOCAL] MCP main.py pre_submit_check 的本地启发式 (非平台判定)
- [CAMPAIGN]  战役级经验闸门 (playbook, 保守值, 非平台硬性)
- [DOCS]      官方文档 (alpha-submission / PPA 资格, 2026-07-23)
"""
from __future__ import annotations

from typing import Tuple

# ---------------------------------------------------------------------------
# 1. 区域门槛 (Sharpe / Fitness) — 提交时平台判定的硬值 [PLATFORM]
#    LOW_SHARPE / LOW_FITNESS 按 region×delay 不同。
# ---------------------------------------------------------------------------

# Delay-1 Sharpe 门槛 (绝大多数区域)
_REGION_SHARPE_D1 = {
    "EUR": 1.58, "KOR": 1.58, "GBR": 1.58, "DEU": 1.58,
    "IND": 1.58, "MEA": 1.58, "ASI": 1.58, "GLB": 1.58, "USA": 1.58,
    "HKG": 1.58, "JPN": 1.58,
    "CHN": 2.07,  # CHN 特殊: 实测 2.07
}

# 区域 × delay 覆盖 (特殊值只列异类, 其余回退默认)
REGION_SHARPE_OVERRIDES = {
    ("GBR", 0): 2.69,  # GBR D0: 1.9× 倍率区高门槛, 实测
    ("CHN", 1): 2.07,
}
DEFAULT_SHARPE_MIN = 1.58
# Delay-0 官方 AlphaTest 门槛 (平台文档: D0 Sharpe > 2.0) [DOCS]
DEFAULT_SHARPE_MIN_D0 = 2.0

# Fitness 门槛: Delay-1 = 1.0 (默认); Delay-0 = 1.3; GBR D0 = 1.5 [PLATFORM]
REGION_FITNESS_OVERRIDES = {
    ("GBR", 0): 1.5,
}
DEFAULT_FITNESS_MIN_D1 = 1.0
FITNESS_MIN_D0 = 1.3


def sharpe_min(region: str, delay: int = 1) -> float:
    """该区域×delay 的 LOW_SHARPE 门槛 (提交硬值)."""
    key = (region.upper(), int(delay))
    if key in REGION_SHARPE_OVERRIDES:
        return REGION_SHARPE_OVERRIDES[key]
    if int(delay) == 0:
        return DEFAULT_SHARPE_MIN_D0  # D0 官方门槛 2.0 (区域实测 override 优先)
    if region.upper() in _REGION_SHARPE_D1:
        return _REGION_SHARPE_D1[region.upper()]
    return DEFAULT_SHARPE_MIN


def fitness_min(region: str, delay: int = 1) -> float:
    """该区域×delay 的 LOW_FITNESS 门槛 (提交硬值)."""
    key = (region.upper(), int(delay))
    if key in REGION_FITNESS_OVERRIDES:
        return REGION_FITNESS_OVERRIDES[key]
    return FITNESS_MIN_D0 if int(delay) == 0 else DEFAULT_FITNESS_MIN_D1


# ---------------------------------------------------------------------------
# 2. 通用提交硬门槛 [PLATFORM]
# ---------------------------------------------------------------------------

# LOW_2Y_SHARPE / IS_LADDER_SHARPE: 严格大于 (1.58 恰好 FAIL!) [GBR 战役实测]
SHARPE_2Y_MIN = 1.58  # strict >

# Turnover: 平台 AlphaTest 检查窗口 [PLATFORM]
TURNOVER_PLATFORM_MIN = 0.01
TURNOVER_PLATFORM_MAX = 0.70

# Turnover: MCP pre_submit_check 本地启发式 (2026-08-13 起 margin 已降级为 warning,
# 但 turnover 仍是本地 hard fail) [MCP-LOCAL]
TURNOVER_LOCAL_MIN = 0.04
TURNOVER_LOCAL_MAX = 0.40

# Turnover: 战役级廉价闸门 (playbook 保守值, 低于此区间易 CW FAIL / 高于则换手惩罚) [CAMPAIGN]
TURNOVER_CHEAP_GATE = (0.05, 0.20)

# Weight Test: 单股票最大权重 [PLATFORM]
WEIGHT_MAX = 0.10

# Sub-universe Test: 子域 Sharpe 下限系数 [PLATFORM]
SUB_UNIVERSE_FACTOR = 0.75

# Margin: 平台 **不检查** [2026-08-13 EUR 实测: 平台 verdict 里没有 margin 项],
# 以下仅为本地推荐值 [MCP-LOCAL]
MARGIN_RECOMMEND_USA_BP = 5.0    # USA > 5bp
MARGIN_RECOMMEND_BP = 15.0       # 其他区域 > 15bp
MARGIN_FLOOR_BP = 8.0            # 硬底 8bp (仅本地 warning)

# Returns / Drawdown 本地启发式 [MCP-LOCAL]
RETURNS_LOCAL_MIN = 0.04


# ---------------------------------------------------------------------------
# 3. 相关性门槛 [PLATFORM]
# ---------------------------------------------------------------------------

SELF_CORR_MAX = 0.70          # 提交时实时查 OS 池 [GBR 战役实测]
PROD_CORR_MAX = 0.70          # 用户绝对红线 (生产池相关, 提交时异步判定)
PPA_SELF_CORR_MAX = 0.50      # PPA 资格官方标准 [DOCS alpha-submission 2026-07-23]

# 异步检查名 (提交后 PENDING, 必须轮询到非 PENDING 才能判定) [EUR 战役实测]
ASYNC_CHECK_NAMES = frozenset({
    "SELF_CORRELATION",
    "PROD_CORRELATION",
    "POWER_POOL_CORRELATION",
    "DATA_DIVERSITY",
    "REGULAR_SUBMISSION",
    "D0_SUBMISSION",
})


# ---------------------------------------------------------------------------
# 4. PPA 资格 [DOCS alpha-submission 2026-07-23]
# ---------------------------------------------------------------------------

PPA_UNIQUE_OPS_MAX = 8      # 去重后算子种类 ≤ 8 (硬门槛)
PPA_UNIQUE_FIELDS_MAX = 3   # unique data fields ≤ 3 (排除 grouping)
# 常规 RA 提交 **无** operatorCount 限制


def is_ppa_eligible(unique_ops: int, unique_fields: int) -> Tuple[bool, str]:
    """PPA 资格判定 (unique operators ≤ 8 是硬门槛)."""
    if unique_ops > PPA_UNIQUE_OPS_MAX:
        return False, (
            f"unique operators {unique_ops} > {PPA_UNIQUE_OPS_MAX} — PPA 不可达, "
            "仅可作为常规 RA 提交"
        )
    if unique_fields > PPA_UNIQUE_FIELDS_MAX:
        return False, (
            f"unique fields {unique_fields} > {PPA_UNIQUE_FIELDS_MAX} (排除 grouping) — PPA 资格不足"
        )
    return True, "PPA 资格 OK"


# ---------------------------------------------------------------------------
# 5. 平台数据集体检门槛 (战役白名单, 第 0 步门3 / PPA 挖掘 §1.0) [CAMPAIGN]
# ---------------------------------------------------------------------------

DATASET_GATE = {
    "coverage_min": 0.85,     # 覆盖率硬门槛
    "alpha_count_max": 50,    # 竞争度上限 (低竞争白空间)
    "field_count_min": 10,    # 字段数下限 (可挖掘性)
    "note": "白名单排序: pyramidMultiplier↓ → valueScore↓ → alphaCount↑",
}

# ---------------------------------------------------------------------------
# 6. 提交配额 [PLATFORM 2026-08-13 实测]
# ---------------------------------------------------------------------------

QUOTA = {
    "regular_submission": {
        "limit": 4,          # 每 rolling 窗口上限
        "window_hours": 48,  # rolling 窗口
        "shared": True,      # RA 与 PPA 共享同一池
        "note": "D0 有独立 D0_SUBMISSION check",
    },
}

# 提交判定语义 (tri-state) [GBR 2026-08-11 + EUR 2026-08-13 实测]
SUBMIT_SEMANTICS = {
    "post_201": "受理成功 (异步检查 pending) — 不是最终结果",
    "get_200": "最终成功 (必须无 FAIL 且无 PENDING async 检查)",
    "get_403": "拒绝 (body 含 FAIL check 列表)",
    "get_404": "提交记录被清 (此前 201 受理但异步被拒)",
    "reliable_signal": "OS 池出现 status=ACTIVE — 唯一可靠验证",
}


def region_gate_table() -> str:
    """生成区域门槛速查表 (与 mining-system-map.md §7.5 对齐)."""
    lines = [
        "| 区域 | delay | Sharpe 门槛 | Fitness 门槛 |",
        "|---|---|---|---|",
    ]
    for region in sorted(_REGION_SHARPE_D1):
        s = sharpe_min(region, 1)
        f = fitness_min(region, 1)
        lines.append(f"| {region} | 1 | {s} | {f} |")
    lines.append("| GBR | 0 | 2.69 | 1.5 |")
    return "\n".join(lines)


if __name__ == "__main__":
    # 冒烟: 打印速查表
    print("== 区域门槛速查 ==")
    print(region_gate_table())
    print(f"\nSHARPE_2Y_MIN (strict >): {SHARPE_2Y_MIN}")
    print(f"TURNOVER platform: ({TURNOVER_PLATFORM_MIN}, {TURNOVER_PLATFORM_MAX})")
    print(f"TURNOVER local pre-check: ({TURNOVER_LOCAL_MIN}, {TURNOVER_LOCAL_MAX})")
    print(f"SELF/PROD corr max: {SELF_CORR_MAX} / {PROD_CORR_MAX} (PPA self: {PPA_SELF_CORR_MAX})")
    print(f"PPA ops ≤ {PPA_UNIQUE_OPS_MAX}, fields ≤ {PPA_UNIQUE_FIELDS_MAX}")
    print(f"QUOTA: limit={QUOTA['regular_submission']['limit']} / "
          f"rolling {QUOTA['regular_submission']['window_hours']}h")
    print(f"DATASET_GATE: cov≥{DATASET_GATE['coverage_min']} / "
          f"alpha≤{DATASET_GATE['alpha_count_max']} / fields≥{DATASET_GATE['field_count_min']}")
    print(f"is_ppa_eligible(8, 3) -> {is_ppa_eligible(8, 3)}")
    print(f"is_ppa_eligible(9, 3) -> {is_ppa_eligible(9, 3)}")
    print(f"sharpe_min('CHN', 1)={sharpe_min('CHN', 1)}, sharpe_min('GBR', 0)={sharpe_min('GBR', 0)}, "
          f"sharpe_min('EUR', 1)={sharpe_min('EUR', 1)}, sharpe_min('USA', 0)={sharpe_min('USA', 0)}")
