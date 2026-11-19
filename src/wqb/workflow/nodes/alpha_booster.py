# -*- coding: utf-8 -*-
"""alpha_booster 节点：通用 Alpha 短板提升能力（S4 增强）.

基于论坛实证方案，自动诊断 Alpha 短板指标并生成改进表达式变体：

短板诊断维度：
- 2y_sharpe：长期稳健性不足（年际波动大、近期失效）
- sub_universe_sharpe：子宇宙一致性不足（小市值/流动性差股票拖累）
- turnover：换手率过高/过低
- fitness：综合健康度不足
- rn_fitness：风险中性化后表现差

后处理算子库（论坛实证，按票数排序）：
- hump：截断极端 rank 值，提升 sub_universe（48 票）
- signed_power：压缩极端值，提升 2y_sharpe（6 票）
- ts_mean/ts_decay_linear：平滑信号，提升 2y_sharpe 和降低 turnover
- 更换 neutralization：SUBINDUSTRY→INDUSTRY，提升 sub_universe（34 票）

论坛实时刷新（2026-09-18 新增）：
- 变体生成前可选实时查询论坛，获取最新方案
- 从帖子标题/摘要提取算子名，动态合并到算子库
- 缓存机制：同一短板维度 24h 内不重复查询

集成点：auto_review 节点 walls 诊断之后，自动推荐并生成改进变体。
"""

import hashlib
import json
import logging
import re
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .._common import resolve_db_path

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
logger = logging.getLogger(__name__)


#: 后处理算子库：基于论坛实证，按短板维度组织
BOOSTER_LIBRARY = {
    "2y_sharpe": {
        "description": "提升 2 年夏普比率（长期稳健性）",
        "operators": [
            {
                "name": "ts_mean",
                "template": "ts_mean({expr}, {window})",
                "params": {"window": [5, 10, 20]},
                "mechanism": "平滑信号，降低年际波动",
                "forum_votes": 0,
                "risk": "可能降低整体 sharpe",
            },
            {
                "name": "ts_decay_linear",
                "template": "ts_decay_linear({expr}, {window})",
                "params": {"window": [5, 10, 20]},
                "mechanism": "线性衰减平滑，保留近期信息",
                "forum_votes": 0,
                "risk": "可能降低整体 sharpe",
            },
            {
                "name": "signed_power",
                "template": "signed_power({expr}, {exp})",
                "params": {"exp": [0.5, 0.7]},
                "mechanism": "压缩极端值、拉大中段区分度",
                "forum_votes": 6,
                "risk": "可能改变信号分布",
            },
        ],
        "settings_override": {
            "decay": [3, 5, 7],  # 增大 decay 提升长期稳健性
        },
    },
    "sub_universe_sharpe": {
        "description": "提升子宇宙夏普比率（小市值股票稳健性）",
        "operators": [
            {
                "name": "hump",
                "template": "hump({expr}, hump={hump})",
                "params": {"hump": [0.01, 0.02, 0.05]},
                "mechanism": "截断极端 rank 值，抑制尾部收益波动",
                "forum_votes": 48,
                "risk": "可能降低 return",
            },
            {
                "name": "ts_zscore",
                "template": "ts_zscore({expr}, {window})",
                "params": {"window": [20, 60]},
                "mechanism": "时序标准化，提升跨期一致性",
                "forum_votes": 0,
                "risk": "可能引入时序噪声",
            },
        ],
        "settings_override": {
            "neutralization": ["INDUSTRY", "SECTOR"],  # 更换中性化
            "truncation": [0.05, 0.1],  # 降低截断阈值
        },
    },
    "turnover": {
        "description": "降低换手率",
        "operators": [
            {
                "name": "ts_mean",
                "template": "ts_mean({expr}, {window})",
                "params": {"window": [5, 10, 20]},
                "mechanism": "平滑信号，降低交易频率",
                "forum_votes": 0,
                "risk": "可能降低信号灵敏度",
            },
        ],
        "settings_override": {
            "decay": [5, 10],  # 增大 decay 降低换手
        },
    },
    "fitness": {
        "description": "提升综合健康度",
        "operators": [
            {
                "name": "rank",
                "template": "rank({expr})",
                "params": {},
                "mechanism": "截面归一化，改善权重分布",
                "forum_votes": 0,
                "risk": "可能降低 return",
            },
        ],
        "settings_override": {},
    },
}


def run(
    region: str,
    wave: str,
    dataset: Optional[str] = None,
    alpha_id: Optional[str] = None,
    max_variants_per_alpha: int = 6,
    auto_insert: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 Alpha 短板提升.

    论坛检索已于 2026-11-18 统一到 `tools/forum_recon.py` / `tools/lib/forum_mcp.py`；
    本节点不再自建论坛通道（旧 `forum_refresh` 参数已删除）。

    Args:
        region: 区域代码
        wave: 波次号
        dataset: 数据集 ID（可选）
        alpha_id: 指定单个 alpha（可选，默认处理整波）
        max_variants_per_alpha: 每个 alpha 最多生成变体数
        auto_insert: 是否自动写入 expressions 表
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "wave": wave,
        "dataset": dataset,
        "success": False,
        "steps": [],
        "diagnosed": 0,
        "variants_generated": 0,
        "variants_inserted": 0,
    }

    # dry-run 模式：走完零成本前置——构建真实请求计划（judge/submit_alpha 同模式）→ 到此为止。
    # 不 subprocess、不写库、不发起论坛网络请求（禁止假 dry-run：不构建计划却报 success）。
    if ctx.get("dry_run"):
        result["plan"] = {
            "region": region, "wave": wave, "dataset": dataset, "alpha_id": alpha_id,
            "calls": [
                "SELECT * FROM backtest_results WHERE region=? [AND wave=?] [AND alpha_id=?]",
                "_diagnose_shortfalls(bt) → 2y_sharpe/sub_universe_sharpe/turnover_high/turnover_low/fitness",
                "_generate_variants(diagnosed, max_variants_per_alpha)",
                "auto_insert ? _insert_variants(...) into expressions (status=pending)",
            ],
            "booster_dimensions": list(BOOSTER_LIBRARY.keys()),
            "operator_counts": {k: len(v["operators"]) for k, v in BOOSTER_LIBRARY.items()},
            "max_variants_per_alpha": max_variants_per_alpha,
            "auto_insert": auto_insert,
        }
        result["steps"].append({
            "step": "build_plan", "success": True,
            "booster_dimensions": list(BOOSTER_LIBRARY.keys()),
        })
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：请求计划已构建，未写库、未发网络请求"
        return result

    try:
        db_path = resolve_db_path()
        conn = db_connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # 读取回测结果
        if alpha_id:
            c.execute(
                "SELECT * FROM backtest_results WHERE region=? AND wave=? AND alpha_id=?",
                (region, wave, alpha_id),
            )
        else:
            c.execute(
                "SELECT * FROM backtest_results WHERE region=? AND wave=?",
                (region, wave),
            )
        backtest_results = [dict(r) for r in c.fetchall()]

        if not backtest_results:
            result["error"] = f"No backtest results found: {region}/{wave}"
            conn.close()
            return result

        # 步骤 1：短板诊断
        diagnosed = []
        for bt in backtest_results:
            walls = _diagnose_shortfalls(bt)
            if walls:
                diagnosed.append({
                    "alpha_id": bt.get("alpha_id"),
                    "expression": bt.get("expression", ""),
                    "settings": _parse_settings(bt.get("settings", "{}")),
                    "walls": walls,
                    "metrics": {
                        "sharpe": bt.get("sharpe"),
                        "fitness": bt.get("fitness"),
                        "two_year_sharpe": bt.get("two_year_sharpe"),
                        "sub_universe_sharpe": bt.get("sub_universe_sharpe"),
                        "turnover": bt.get("turnover"),
                    },
                })

        result["diagnosed"] = len(diagnosed)
        result["steps"].append({
            "step": "diagnose_shortfalls",
            "success": True,
            "diagnosed_count": len(diagnosed),
        })

        # 步骤 2：生成改进变体
        all_variants = []
        for d in diagnosed:
            variants = _generate_variants(d, max_variants_per_alpha)
            all_variants.extend(variants)

        result["variants_generated"] = len(all_variants)
        result["steps"].append({
            "step": "generate_variants",
            "success": True,
            "variants_count": len(all_variants),
        })

        # 步骤 3：写入 expressions 表
        if auto_insert and all_variants:
            inserted = _insert_variants(conn, region, wave, dataset, all_variants)
            result["variants_inserted"] = inserted
            result["steps"].append({
                "step": "insert_variants",
                "success": True,
                "inserted_count": inserted,
            })
            conn.commit()

        conn.close()

        result["success"] = True
        result["message"] = (
            f"Alpha booster completed: {len(diagnosed)} diagnosed, "
            f"{len(all_variants)} variants generated, {result['variants_inserted']} inserted"
        )

    except Exception as e:
        result["error"] = f"Alpha booster failed: {e}"
        logger.exception("Alpha booster failed")

    return result


def _diagnose_shortfalls(bt: Dict[str, Any]) -> List[str]:
    """诊断 Alpha 短板维度.

    Returns:
        短板维度列表，如 ["2y_sharpe", "sub_universe_sharpe"]
    """
    walls = []

    # 2y_sharpe 短板
    two_year = bt.get("two_year_sharpe")
    sharpe = bt.get("sharpe")
    if two_year is not None and sharpe is not None:
        if two_year < 1.58 and sharpe >= 1.58:
            walls.append("2y_sharpe")
        elif two_year < 1.0:
            walls.append("2y_sharpe")

    # sub_universe_sharpe 短板
    sub_univ = bt.get("sub_universe_sharpe")
    if sub_univ is not None and sub_univ < 1.0:
        walls.append("sub_universe_sharpe")

    # turnover 短板
    turnover = bt.get("turnover")
    if turnover is not None:
        if turnover > 0.7:
            walls.append("turnover_high")
        elif turnover < 0.01:
            walls.append("turnover_low")

    # fitness 短板
    fitness = bt.get("fitness")
    if fitness is not None and fitness < 1.0 and sharpe is not None and sharpe >= 1.58:
        walls.append("fitness")

    return walls


def _generate_variants(
    diagnosed: Dict[str, Any],
    max_variants: int,
) -> List[Dict[str, Any]]:
    """生成改进表达式变体.

    Args:
        diagnosed: 诊断结果（含 expression, settings, walls）
        max_variants: 最大变体数

    Returns:
        变体列表
    """
    variants = []
    expr = diagnosed.get("expression", "")
    settings = diagnosed.get("settings", {})
    walls = diagnosed.get("walls", [])

    if not expr:
        return variants

    # 只用静态实证算子库；论坛检索已统一到 tools/forum_recon.py（本节点不再自建通道）
    for wall in walls:
        if wall not in BOOSTER_LIBRARY:
            continue

        booster = BOOSTER_LIBRARY[wall]

        # 算子变体
        for op in booster["operators"]:
            template = op["template"]
            params = op["params"]

            # 生成参数组合
            param_combos = _generate_param_combos(params)
            for combo in param_combos[:2]:  # 每个算子最多 2 个参数组合
                new_expr = template.format(expr=expr, **combo)
                variants.append({
                    "expression": new_expr,
                    "source": f"booster_{wall}_{op['name']}",
                    "base_alpha_id": diagnosed.get("alpha_id"),
                    "target_wall": wall,
                    "operator": op["name"],
                    "mechanism": op["mechanism"],
                    "settings": _override_settings(settings, booster.get("settings_override", {})),
                })

        # settings 变体（不换表达式，只改设置）
        for key, values in booster.get("settings_override", {}).items():
            for val in values[:2]:  # 每个设置最多 2 个值
                new_settings = dict(settings)
                new_settings[key] = val
                variants.append({
                    "expression": expr,  # 原表达式
                    "source": f"booster_{wall}_settings_{key}",
                    "base_alpha_id": diagnosed.get("alpha_id"),
                    "target_wall": wall,
                    "operator": f"settings.{key}",
                    "mechanism": f"调整设置 {key}={val}",
                    "settings": new_settings,
                })

    # 去重（按 expression + settings hash）
    seen = set()
    unique_variants = []
    for v in variants:
        key = f"{v['expression']}|{json.dumps(v['settings'], sort_keys=True)}"
        if key not in seen:
            seen.add(key)
            unique_variants.append(v)

    return unique_variants[:max_variants]


def _generate_param_combos(params: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """生成参数组合."""
    if not params:
        return [{}]

    combos = [{}]
    for key, values in params.items():
        new_combos = []
        for combo in combos:
            for val in values:
                new_combo = dict(combo)
                new_combo[key] = val
                new_combos.append(new_combo)
        combos = new_combos

    return combos


def _override_settings(
    base: Dict[str, Any],
    override: Dict[str, List[Any]],
) -> Dict[str, Any]:
    """覆盖设置（取第一个值）."""
    settings = dict(base)
    for key, values in override.items():
        if values:
            settings[key] = values[0]
    return settings


def _parse_settings(settings_str: str) -> Dict[str, Any]:
    """解析 settings JSON 字符串."""
    if isinstance(settings_str, dict):
        return settings_str
    try:
        return json.loads(settings_str)
    except (json.JSONDecodeError, TypeError):
        return {}


def _insert_variants(
    conn: sqlite3.Connection,
    region: str,
    wave: str,
    dataset: Optional[str],
    variants: List[Dict[str, Any]],
) -> int:
    """写入 expressions 表."""
    c = conn.cursor()
    inserted = 0

    for v in variants:
        expr_id = f"booster_{region}_{wave}_{hash(v['expression']) % 100000:05d}"
        try:
            c.execute(
                """INSERT OR REPLACE INTO expressions
                   (id, region, wave, dataset, expression, status, source,
                    created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 'pending', ?, ?, ?)""",
                (
                    expr_id,
                    region,
                    wave,
                    dataset or "",
                    v["expression"],
                    v["source"],
                    datetime.now().isoformat(timespec="seconds"),
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            inserted += 1
        except sqlite3.Error as e:
            logger.warning(f"Failed to insert variant {expr_id}: {e}")

    return inserted


def get_booster_library() -> Dict[str, Any]:
    """获取后处理算子库（供外部查询）."""
    return BOOSTER_LIBRARY
