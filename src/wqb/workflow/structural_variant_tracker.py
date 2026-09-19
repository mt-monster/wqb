# -*- coding: utf-8 -*-
"""structural_variant_tracker.py - 结构重构效果追踪与对比分析.

追踪结构重构变体的回测结果，与原始表达式对比，量化改进效果。

核心功能：
  1. 变体结果记录：将重构变体的回测结果与原始表达式关联
  2. 效果对比分析：sharpe/fitness/turnover/2Y 四维对比
  3. 策略有效性统计：哪种重构策略在哪种场景下最有效
  4. 台账集成：结果自动写入 wave_results 和 ledger_kv

用法:
    from wqb.workflow.structural_variant_tracker import StructuralVariantTracker

    tracker = StructuralVariantTracker(store)
    tracker.record_variant_result(
        wave=95,
        original_expr="add(rank(A), rank(B))",
        variant_expr="subtract(rank(A), rank(B))",
        strategy="geometric",
        alpha_id="abc123",
        metrics={"sharpe": 1.45, "fitness": 0.92, ...},
    )
    report = tracker.generate_comparison_report(wave=95)
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class VariantMetrics:
    """变体回测指标."""
    sharpe: Optional[float] = None
    fitness: Optional[float] = None
    turnover: Optional[float] = None
    two_year_sharpe: Optional[float] = None
    returns: Optional[float] = None
    margin: Optional[float] = None
    # 扩展指标
    max_drawdown: Optional[float] = None
    calmar: Optional[float] = None
    # 相关性
    prod_correlation: Optional[float] = None
    self_correlation: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "VariantMetrics":
        return cls(**{k: d.get(k) for k in cls.__dataclass_fields__})


@dataclass
class VariantResult:
    """单个变体的回测结果."""
    variant_id: str                    # 变体唯一标识
    original_expression: str           # 原始表达式
    variant_expression: str            # 变体表达式
    strategy: str                      # 重构策略
    alpha_id: Optional[str] = None     # 平台 alpha id
    metrics: VariantMetrics = field(default_factory=VariantMetrics)
    status: str = "pending"            # pending / complete / failed / cancelled
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    """原始 vs 变体对比结果."""
    original_alpha_id: Optional[str]
    original_metrics: VariantMetrics
    variants: List[VariantResult]
    best_variant: Optional[VariantResult]
    improvement: Dict[str, float]      # 各指标改进幅度
    verdict: str                       # IMPROVED / DEGRADED / MIXED / NO_DATA
    recommendation: str


class StructuralVariantTracker:
    """结构重构效果追踪器."""

    # 效果判定阈值
    SHARPE_IMPROVEMENT_THRESHOLD = 0.1    # sharpe 提升 0.1 视为有效
    FITNESS_IMPROVEMENT_THRESHOLD = 0.05  # fitness 提升 0.05 视为有效
    TURNOVER_REDUCTION_THRESHOLD = 0.1    # turnover 降低 10% 视为有效

    def __init__(self, store=None, db_path: Optional[str] = None):
        """初始化追踪器.

        Args:
            store: CampaignStore 实例（优先）
            db_path: 数据库路径（store 为 None 时使用）
        """
        self._store = store
        self._db_path = db_path
        self._ensure_table()

    def _get_conn(self):
        """获取数据库连接."""
        import sqlite3
        if self._store:
            return self._store._conn()
        elif self._db_path:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            return conn
        else:
            raise RuntimeError("需要 store 或 db_path")

    def _ensure_table(self):
        """确保追踪表存在."""
        conn = self._get_conn()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS structural_variant_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    region VARCHAR(50) NOT NULL,
                    wave_number INTEGER NOT NULL,
                    variant_id VARCHAR(100) NOT NULL,
                    original_expression TEXT NOT NULL,
                    variant_expression TEXT NOT NULL,
                    strategy VARCHAR(50) NOT NULL,
                    alpha_id VARCHAR(100),
                    metrics JSON,
                    status VARCHAR(20) DEFAULT 'pending',
                    error TEXT,
                    metadata JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(region, wave_number, variant_id)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sv_region_wave
                ON structural_variant_results(region, wave_number)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sv_strategy
                ON structural_variant_results(strategy)
            """)
            conn.commit()
        finally:
            conn.close()

    def record_variant_result(
        self,
        region: str,
        wave: int,
        variant_id: str,
        original_expr: str,
        variant_expr: str,
        strategy: str,
        alpha_id: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None,
        status: str = "pending",
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """记录变体回测结果（幂等）.

        Args:
            region: 区域代码
            wave: 波次号
            variant_id: 变体唯一标识（如 "geo_spread_rank"）
            original_expr: 原始表达式
            variant_expr: 变体表达式
            strategy: 重构策略
            alpha_id: 平台 alpha id
            metrics: 回测指标字典
            status: 状态
            error: 错误信息
            metadata: 额外元数据

        Returns:
            记录结果摘要
        """
        conn = self._get_conn()
        try:
            with conn:
                conn.execute("""
                    INSERT OR REPLACE INTO structural_variant_results
                    (region, wave_number, variant_id, original_expression, variant_expression,
                     strategy, alpha_id, metrics, status, error, metadata, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    region, wave, variant_id, original_expr, variant_expr,
                    strategy, alpha_id,
                    json.dumps(metrics or {}, ensure_ascii=False),
                    status, error,
                    json.dumps(metadata or {}, ensure_ascii=False),
                ))
        finally:
            conn.close()

        return {
            "region": region,
            "wave": wave,
            "variant_id": variant_id,
            "status": status,
            "recorded": True,
        }

    def get_wave_variants(self, region: str, wave: int) -> List[VariantResult]:
        """获取某波次的所有变体结果."""
        conn = self._get_conn()
        try:
            rows = conn.execute("""
                SELECT * FROM structural_variant_results
                WHERE region=? AND wave_number=?
                ORDER BY variant_id
            """, (region, wave)).fetchall()
        finally:
            conn.close()

        results = []
        for row in rows:
            results.append(VariantResult(
                variant_id=row["variant_id"],
                original_expression=row["original_expression"],
                variant_expression=row["variant_expression"],
                strategy=row["strategy"],
                alpha_id=row["alpha_id"],
                metrics=VariantMetrics.from_dict(json.loads(row["metrics"] or "{}")),
                status=row["status"],
                error=row["error"],
                created_at=row["created_at"],
                metadata=json.loads(row["metadata"] or "{}"),
            ))
        return results

    def compare_with_original(
        self,
        region: str,
        wave: int,
        original_alpha_id: Optional[str] = None,
        original_metrics: Optional[Dict[str, Any]] = None,
    ) -> ComparisonResult:
        """对比原始表达式与变体的效果.

        Args:
            region: 区域代码
            wave: 波次号
            original_alpha_id: 原始表达式的 alpha id（可选，用于从平台拉取）
            original_metrics: 原始表达式的指标（可选，直接提供）

        Returns:
            ComparisonResult: 对比结果
        """
        variants = self.get_wave_variants(region, wave)
        complete_variants = [v for v in variants if v.status == "complete" and v.metrics.sharpe is not None]

        # 获取原始指标
        orig_metrics = VariantMetrics()
        if original_metrics:
            orig_metrics = VariantMetrics.from_dict(original_metrics)
        elif original_alpha_id:
            # TODO: 从平台拉取原始 alpha 指标
            pass

        if not complete_variants:
            return ComparisonResult(
                original_alpha_id=original_alpha_id,
                original_metrics=orig_metrics,
                variants=variants,
                best_variant=None,
                improvement={},
                verdict="NO_DATA",
                recommendation="无完整变体结果，无法对比",
            )

        # 找最佳变体（综合 sharpe + fitness）
        def score(v: VariantResult) -> float:
            sharpe = v.metrics.sharpe or 0
            fitness = v.metrics.fitness or 0
            return sharpe * 0.6 + fitness * 0.4

        best = max(complete_variants, key=score)

        # 计算改进幅度
        improvement = {}
        if orig_metrics.sharpe is not None and best.metrics.sharpe is not None:
            improvement["sharpe"] = best.metrics.sharpe - orig_metrics.sharpe
        if orig_metrics.fitness is not None and best.metrics.fitness is not None:
            improvement["fitness"] = best.metrics.fitness - orig_metrics.fitness
        if orig_metrics.turnover is not None and best.metrics.turnover is not None:
            improvement["turnover"] = best.metrics.turnover - orig_metrics.turnover
        if orig_metrics.two_year_sharpe is not None and best.metrics.two_year_sharpe is not None:
            improvement["two_year_sharpe"] = best.metrics.two_year_sharpe - orig_metrics.two_year_sharpe

        # 判定效果
        verdict, recommendation = self._evaluate_improvement(improvement, orig_metrics, best)

        return ComparisonResult(
            original_alpha_id=original_alpha_id,
            original_metrics=orig_metrics,
            variants=variants,
            best_variant=best,
            improvement=improvement,
            verdict=verdict,
            recommendation=recommendation,
        )

    def _evaluate_improvement(
        self,
        improvement: Dict[str, float],
        original: VariantMetrics,
        best: VariantResult,
    ) -> Tuple[str, str]:
        """评估改进效果."""
        sharpe_imp = improvement.get("sharpe", 0)
        fitness_imp = improvement.get("fitness", 0)
        turnover_imp = improvement.get("turnover", 0)

        positive = []
        negative = []

        if sharpe_imp >= self.SHARPE_IMPROVEMENT_THRESHOLD:
            positive.append(f"sharpe +{sharpe_imp:.2f}")
        elif sharpe_imp <= -self.SHARPE_IMPROVEMENT_THRESHOLD:
            negative.append(f"sharpe {sharpe_imp:.2f}")

        if fitness_imp >= self.FITNESS_IMPROVEMENT_THRESHOLD:
            positive.append(f"fitness +{fitness_imp:.2f}")
        elif fitness_imp <= -self.FITNESS_IMPROVEMENT_THRESHOLD:
            negative.append(f"fitness {fitness_imp:.2f}")

        if turnover_imp <= -self.TURNOVER_REDUCTION_THRESHOLD:
            positive.append(f"turnover {turnover_imp:.1%}")
        elif turnover_imp >= self.TURNOVER_REDUCTION_THRESHOLD:
            negative.append(f"turnover +{turnover_imp:.1%}")

        if positive and not negative:
            verdict = "IMPROVED"
            recommendation = f"结构重构有效：{', '.join(positive)}。推荐采用 {best.strategy} 策略。"
        elif negative and not positive:
            verdict = "DEGRADED"
            recommendation = f"结构重构无效：{', '.join(negative)}。建议回退或尝试其他策略。"
        elif positive and negative:
            verdict = "MIXED"
            recommendation = f"效果混合：正向 {', '.join(positive)}；负向 {', '.join(negative)}。需权衡。"
        else:
            verdict = "NO_CHANGE"
            recommendation = "改进幅度不显著，建议观察更多样本。"

        return verdict, recommendation

    def get_strategy_stats(self, region: Optional[str] = None) -> Dict[str, Any]:
        """获取各策略的统计效果.

        Returns:
            按策略分组的统计：成功率、平均改进幅度等
        """
        conn = self._get_conn()
        try:
            sql = """
                SELECT strategy, status, metrics
                FROM structural_variant_results
                WHERE status = 'complete'
            """
            args = []
            if region:
                sql += " AND region=?"
                args.append(region)

            rows = conn.execute(sql, args).fetchall()
        finally:
            conn.close()

        stats = {}
        for row in rows:
            strategy = row["strategy"]
            metrics = json.loads(row["metrics"] or "{}")

            if strategy not in stats:
                stats[strategy] = {
                    "count": 0,
                    "sharpe_sum": 0,
                    "fitness_sum": 0,
                    "sharpe_count": 0,
                    "fitness_count": 0,
                }

            s = stats[strategy]
            s["count"] += 1
            if metrics.get("sharpe") is not None:
                s["sharpe_sum"] += metrics["sharpe"]
                s["sharpe_count"] += 1
            if metrics.get("fitness") is not None:
                s["fitness_sum"] += metrics["fitness"]
                s["fitness_count"] += 1

        # 计算平均值
        for strategy, s in stats.items():
            s["avg_sharpe"] = s["sharpe_sum"] / s["sharpe_count"] if s["sharpe_count"] else None
            s["avg_fitness"] = s["fitness_sum"] / s["fitness_count"] if s["fitness_count"] else None
            del s["sharpe_sum"]
            del s["fitness_sum"]
            del s["sharpe_count"]
            del s["fitness_count"]

        return stats

    def generate_comparison_report(self, region: str, wave: int) -> str:
        """生成对比报告（Markdown）."""
        comparison = self.compare_with_original(region, wave)

        lines = [
            f"# 结构重构效果对比报告",
            "",
            f"**区域**: {region} | **波次**: {wave}",
            "",
            f"**判定**: {comparison.verdict}",
            "",
            f"**建议**: {comparison.recommendation}",
            "",
            "## 指标对比",
            "",
            "| 指标 | 原始 | 最佳变体 | 改进 |",
            "|------|------|----------|------|",
        ]

        orig = comparison.original_metrics
        best = comparison.best_variant.metrics if comparison.best_variant else VariantMetrics()

        for metric, label in [
            ("sharpe", "Sharpe"),
            ("fitness", "Fitness"),
            ("turnover", "Turnover"),
            ("two_year_sharpe", "2Y Sharpe"),
        ]:
            orig_val = getattr(orig, metric, None)
            best_val = getattr(best, metric, None)
            imp = comparison.improvement.get(metric)

            orig_str = f"{orig_val:.2f}" if orig_val is not None else "-"
            best_str = f"{best_val:.2f}" if best_val is not None else "-"
            imp_str = f"{imp:+.2f}" if imp is not None else "-"

            lines.append(f"| {label} | {orig_str} | {best_str} | {imp_str} |")

        if comparison.best_variant:
            lines.extend([
                "",
                "## 最佳变体",
                "",
                f"- **策略**: {comparison.best_variant.strategy}",
                f"- **表达式**: `{comparison.best_variant.variant_expression[:60]}...`",
                f"- **Alpha ID**: {comparison.best_variant.alpha_id or 'N/A'}",
            ])

        lines.extend([
            "",
            "## 全部变体状态",
            "",
            "| 变体 ID | 策略 | 状态 | Sharpe | Fitness |",
            "|---------|------|------|--------|---------|",
        ])

        for v in comparison.variants:
            sharpe = f"{v.metrics.sharpe:.2f}" if v.metrics.sharpe else "-"
            fitness = f"{v.metrics.fitness:.2f}" if v.metrics.fitness else "-"
            lines.append(f"| {v.variant_id} | {v.strategy} | {v.status} | {sharpe} | {fitness} |")

        return "\n".join(lines)
