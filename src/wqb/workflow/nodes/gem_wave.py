# -*- coding: utf-8 -*-
"""gem_wave 节点：合并选波到 GEM 生成流程（S2 增强）.

合并选波到 GEM 生成流程：
1. GEM 生成候选 alpha 表达式
2. 自动去重
3. 自动分桶
4. 自动骨架配给
5. 自动选波
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from .._common import (
    REPO_ROOT,
    resolve_campaign_dir,
    resolve_db_path,
    resolve_tools_dir,
    wq_py,
)
from ...expression.skeleton import (
    dedup_by_skeleton,
    skeleton_distribution,
    structural_signature,
)

logger = logging.getLogger(__name__)

#: 写回 expressions 的列。**必须与 `src/wqb/store/_schema.py` 的实际列一致** ——
#: 2026-09-17 之前这里引用了 bucket/skeleton/selected 三个当时并不存在的列，
#: 导致本节点每次运行都在写回处 OperationalError、三项能力算完即丢弃。
#: 由 `tests/unit/test_gem_wave_writeback_p1p2.py` 机械守护（列名对不上即红）。
_WRITEBACK_COLUMNS = (
    "id", "region", "wave", "dataset", "expression", "status",
    "bucket", "skeleton", "selected", "source", "expected_exposure",
    "created_at", "updated_at",
)


def run(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_type: Optional[str] = None,
    wave: Optional[str] = None,
    auto_dedup: bool = True,
    auto_bucket: bool = True,
    auto_skeleton: bool = True,
    auto_select: bool = True,
    max_per_skeleton: int = 3,
    source: Optional[str] = None,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行合并选波到 GEM 生成流程.

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟
        universe: Universe
        data_type: 数据类型（可选）
        wave: 波次号（可选）
        auto_dedup: 是否自动去重（默认 True）
        auto_bucket: 是否自动分桶（默认 True）
        auto_skeleton: 是否自动骨架配给（默认 True）
        auto_select: 是否自动选波（默认 True）
        max_per_skeleton: 同一**结构骨架**在一批内的保留上限（默认 3）。
            用于抑制"同骨架换字段"的兄弟变体（这类变体 SELF 相关 0.9+）。
        source: 写回 `expressions.source` 的来源标签（缺省 `gem`）。上游可传更具体的
            值（如 `gem_phased` / `gem_skeleton` / `gem_single`）以便按生成模式回溯。
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "dataset_id": dataset_id,
        "delay": delay,
        "universe": universe,
        "wave": wave,
        "success": False,
        "steps": [],
    }

    # 步骤 1：GEM 生成
    result["steps"].append({
        "step": "gem_generate",
        "success": True,
        "description": "GEM 生成候选 alpha 表达式",
    })

    # 步骤 2：自动去重
    if auto_dedup:
        result["steps"].append({
            "step": "auto_dedup",
            "success": True,
            "description": "自动去重",
        })

    # 步骤 3：自动分桶
    if auto_bucket:
        result["steps"].append({
            "step": "auto_bucket",
            "success": True,
            "description": "自动分桶",
        })

    # 步骤 4：自动骨架配给
    if auto_skeleton:
        result["steps"].append({
            "step": "auto_skeleton",
            "success": True,
            "description": "自动骨架配给",
        })

    # 步骤 5：自动选波
    if auto_select:
        result["steps"].append({
            "step": "auto_select",
            "success": True,
            "description": "自动选波",
        })

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：合并选波到 GEM 生成流程已构建，未执行"
        return result

    # 执行合并选波到 GEM 生成流程
    try:
        # 调用 GEM 生成
        from . import gem
        gem_result = gem.run(
            region=region,
            dataset_id=dataset_id,
            delay=delay,
            universe=universe,
            data_type=data_type,
            _context=ctx,
        )

        if not gem_result.get("success"):
            result["error"] = f"GEM generation failed: {gem_result.get('error')}"
            return result

        result["steps"][0]["gem_result"] = gem_result

        # 从 DB 读取生成的表达式
        db_path = resolve_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT * FROM expressions WHERE region=? AND dataset=? AND status='gem'",
            (region, dataset_id),
        )
        expressions = [dict(r) for r in c.fetchall()]

        # 自动去重（内容级 + **骨架级**，2026-09-17 加骨架级）
        if auto_dedup:
            before = len(expressions)
            expressions = _auto_dedup(expressions)
            content_deduped = before - len(expressions)
            # 骨架级去重：抑制"同骨架换字段"的兄弟变体（实测近 3 天 89.2% 落在 ≥8 条大簇里，
            # 这类变体在平台 SELF 相关 0.9+，会自相残杀）。
            expressions, dropped_sib = dedup_by_skeleton(
                expressions, max_per_skeleton=max_per_skeleton,
            )
            result["steps"][1].update({
                "dedup_count": len(expressions),
                "content_deduped": content_deduped,
                "sibling_deduped": len(dropped_sib),
                "skeleton_stats": skeleton_distribution(expressions),
            })

        # 自动分桶
        if auto_bucket:
            expressions = _auto_bucket(expressions)
            result["steps"][2]["bucket_count"] = len(set(e.get("bucket") for e in expressions))

        # 自动骨架配给
        if auto_skeleton:
            expressions = _auto_skeleton(expressions)
            result["steps"][3]["skeleton_count"] = len(set(e.get("skeleton") for e in expressions))

        # 自动选波
        if auto_select and wave:
            expressions = _auto_select(expressions, wave)
            result["steps"][4]["selected_count"] = len([e for e in expressions if e.get("selected")])

        # 写回 DB
        # 2026-09-17 修复（两处，此前**每次运行都失败**）：
        # ① 原实现引用 bucket/skeleton/selected 三个**当时并不存在**的列 → OperationalError；
        # ② 原实现用 INSERT OR REPLACE —— 这些行是从 `SELECT * FROM expressions` 读出来的，
        #    语义上是"给已有行补属性"，而 REPLACE 会整行重写、且不提供 wave_id（NOT NULL）
        #    → 即便列存在也会 NOT NULL 失败。改为按 id UPDATE。
        # 并补上 source（此前全链路无人写 → GEM 产出不可辨识）与 expected_exposure（规则7/8 输入）。
        set_cols = [c for c in _WRITEBACK_COLUMNS if c != "id"]
        set_sql = ", ".join(f"{c}=?" for c in set_cols)
        now = datetime.now().isoformat(timespec="seconds")
        written = 0
        for expr in expressions:
            if not expr.get("id"):
                continue  # 没有主键的行无从 UPDATE（正常不会发生：行来自 SELECT *）
            vals = tuple(
                (expr.get("source") or source or "gem")
                if c == "source" else expr.get(c)
                for c in set_cols
            )
            c.execute(
                f"UPDATE expressions SET {set_sql} WHERE id=?",
                vals + (expr["id"],),
            )
            written += 1
        conn.commit()
        conn.close()

        result["success"] = True
        result["expression_count"] = len(expressions)
        result["written"] = written
        result["skeleton_stats"] = skeleton_distribution(expressions)
        result["message"] = f"GEM wave completed: {len(expressions)} expressions processed"

    except Exception as e:
        result["error"] = f"GEM wave failed: {e}"
        logger.exception("GEM wave failed")

    return result


def _auto_dedup(expressions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """自动去重."""
    seen = set()
    deduped = []
    for expr in expressions:
        expr_text = expr.get("expression", "")
        if expr_text not in seen:
            seen.add(expr_text)
            deduped.append(expr)
    return deduped


def _auto_bucket(expressions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """自动分桶."""
    for expr in expressions:
        # 根据表达式特征自动分桶
        expr_text = expr.get("expression", "").lower()
        if "rank" in expr_text:
            expr["bucket"] = "rank"
        elif "ts_" in expr_text:
            expr["bucket"] = "time_series"
        elif "group_" in expr_text:
            expr["bucket"] = "group"
        else:
            expr["bucket"] = "other"
    return expressions


def _auto_skeleton(expressions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """自动骨架配给（2026-09-17 改用结构签名）。

    原实现是 3 桶子串匹配（`rank`+`ts_` → "rank_ts"、`group_`+`rank` → "group_rank"、
    否则 "simple"），粒度太粗且与真实骨架无关 —— 既无法用于去重，也无法回答
    "这批有多少重复骨架"。现改用 `wqb.expression.skeleton.structural_signature`
    （字段→F、数字→N、算子按"后是否紧跟 `(`"识别，保留括号与逗号保存元数结构）。
    """
    for expr in expressions:
        expr["skeleton"] = structural_signature(expr.get("expression") or "")
    return expressions


def _auto_select(expressions: List[Dict[str, Any]], wave: str) -> List[Dict[str, Any]]:
    """自动选波."""
    # 按价值得分排序，选择前 N 个
    sorted_exprs = sorted(
        expressions,
        key=lambda e: e.get("value_score", 0),
        reverse=True,
    )

    # 选择前 30 个
    for i, expr in enumerate(sorted_exprs):
        expr["selected"] = i < 30
        expr["wave"] = wave

    return sorted_exprs
