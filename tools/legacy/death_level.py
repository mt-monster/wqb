"""Death level classification for dataset dead ends.

三级判死：
- DEAD_PERMANENT: S<0.5 且 2Y<0.5，无任何信号
- DEAD_CONDITIONAL: S 在 floor-1.58 之间，有信号但不够强（允许 1 次翻案批）
- DEAD_WALL: S>=1.58 但 robust/prod 墙（允许 PPA 路径）
"""

DEATH_LEVELS = {
    "DEAD_PERMANENT": {
        "description": "无任何信号，永久封存",
        "allow_retrial": False,
        "allow_ppa": False,
    },
    "DEAD_CONDITIONAL": {
        "description": "有信号但不够强，允许 1 次翻案批（4条，必须用新策略）",
        "allow_retrial": True,
        "retrial_size": 4,
        "allow_ppa": False,
    },
    "DEAD_WALL": {
        "description": "信号强但 robust/prod 墙，允许 PPA 路径",
        "allow_retrial": False,
        "allow_ppa": True,
    },
}


def classify_death_level(best_sharpe, best_fitness, best_2y, robust_sharpe=None, prod_corr=None, signal_floor=0.9):
    """Classify death level based on best achieved metrics.

    Args:
        best_sharpe: 最佳 |sharpe|
        best_fitness: 最佳 fitness
        best_2y: 最佳 2Y sharpe
        robust_sharpe: robust universe sharpe（可选）
        prod_corr: production correlation（可选）
        signal_floor: 区域 signal_floor 阈值

    Returns:
        (death_level, rationale)
    """
    s = abs(best_sharpe) if best_sharpe is not None else 0
    f = best_fitness or 0
    y2 = best_2y or 0

    # DEAD_WALL: S >= 1.58 但 robust/prod 墙
    if s >= 1.58:
        wall_reasons = []
        if robust_sharpe is not None and robust_sharpe < 1.0:
            wall_reasons.append(f"robust={robust_sharpe:.2f}<1.0")
        if prod_corr is not None and prod_corr > 0.7:
            wall_reasons.append(f"prod={prod_corr:.2f}>0.7")
        if wall_reasons:
            return "DEAD_WALL", f"S={s:.2f}>=1.58 但 {'+'.join(wall_reasons)}"
        # S>=1.58 且无墙 —— 不应判死
        return None, f"S={s:.2f}>=1.58 且无墙，不应判死"

    # DEAD_PERMANENT: 无任何信号
    if s < 0.5 and y2 < 0.5:
        return "DEAD_PERMANENT", f"S={s:.2f}<0.5 且 2Y={y2:.2f}<0.5，无任何信号"

    # DEAD_CONDITIONAL: 有信号但不够强
    if s >= signal_floor:
        return "DEAD_CONDITIONAL", (
            f"S={s:.2f} 在 [{signal_floor}, 1.58) 区间，有信号但不够强；"
            f"F={f:.2f}, 2Y={y2:.2f}"
        )

    # S < signal_floor —— 接近永久死
    if s < signal_floor and y2 < 1.0:
        return "DEAD_PERMANENT", f"S={s:.2f}<{signal_floor} 且 2Y={y2:.2f}<1.0"

    # S < signal_floor 但 2Y 强 —— 条件死
    return "DEAD_CONDITIONAL", f"S={s:.2f}<{signal_floor} 但 2Y={y2:.2f}>=1.0"


def should_allow_retrial(death_level, retrial_count=0):
    """Check if a retrial batch is allowed."""
    if death_level != "DEAD_CONDITIONAL":
        return False, f"death_level={death_level} 不允许翻案"
    if retrial_count >= 1:
        return False, "翻案批已用完（每数据集限 1 次）"
    return True, "允许翻案批"


def should_allow_ppa(death_level):
    """Check if PPA path is allowed."""
    return death_level == "DEAD_WALL", f"death_level={death_level}"
