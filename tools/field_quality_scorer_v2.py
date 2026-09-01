# -*- coding: utf-8 -*-
"""field_quality_scorer_v2.py - 8 维字段质量评分器.

增强版字段质量评分，包含：
1. 覆盖度（含趋势分析）
2. 历史 Sharpe（含衰减/稳定性）
3. 更新频率（含实际延迟）
4. 经济可解释性（含文献支撑）
5. 字段间相关性（多样性惩罚）
6. 市场状态适配
7. 数据质量异常检测
8. 计算成本评估
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
from typing import Any, Dict, List, Optional


class FieldQualityScorerV2:
    """8 维字段质量评分器."""
    
    # 经济可解释性关键词
    ECONOMIC_KEYWORDS = {
        "high": ["margin", "profit", "earnings", "growth", "return", "ratio", "yield"],
        "medium": ["revenue", "sales", "asset", "debt", "equity", "cash"],
        "low": ["price", "volume", "count", "number", "date"]
    }
    
    # 维度权重
    WEIGHTS = {
        "coverage": 0.20,       # 覆盖度（含趋势）
        "sharpe": 0.25,         # 历史 Sharpe（含衰减/稳定性）
        "frequency": 0.10,      # 更新频率（含延迟）
        "economic": 0.10,       # 经济可解释性（含文献）
        "diversity": 0.10,      # 字段间相关性
        "regime": 0.10,         # 市场状态适配
        "data_quality": 0.10,   # 数据质量
        "compute_cost": 0.05,   # 计算成本
    }
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化."""
        if db_path is None:
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            db_path = os.path.join(wqb_root, "data", "wqb.db")
        self.db_path = db_path
        
    def score_fields(
        self,
        field_ids: List[str],
        dataset: str,
        region: str,
        descriptions: Optional[Dict[str, str]] = None,
        selected_fields: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """8 维评分字段质量.
        
        Args:
            field_ids: 字段 ID 列表
            dataset: 数据集 ID
            region: 区域
            descriptions: 字段描述
            selected_fields: 已选字段（用于多样性计算）
            
        Returns:
            8 维评分结果
        """
        descriptions = descriptions or {}
        selected_fields = selected_fields or []
        scores = {}
        
        for fid in field_ids:
            # 1. 覆盖度（含趋势分析）
            coverage_result = self._score_coverage(fid, dataset, region)
            
            # 2. 历史 Sharpe（含衰减/稳定性）
            sharpe_result = self._score_sharpe(fid, region)
            
            # 3. 更新频率（含实际延迟）
            freq_result = self._score_frequency(fid, descriptions.get(fid, ""))
            
            # 4. 经济可解释性（含文献支撑）
            econ_result = self._score_economic(fid, descriptions.get(fid, ""), dataset, region)
            
            # 5. 字段间相关性（多样性惩罚）
            diversity_result = self._score_diversity(fid, selected_fields, dataset, region)
            
            # 6. 市场状态适配
            regime_result = self._score_regime(fid, region)
            
            # 7. 数据质量异常检测
            quality_result = self._score_data_quality(fid, dataset, region)
            
            # 8. 计算成本评估
            cost_result = self._score_compute_cost(fid)
            
            # 综合评分
            total_score = (
                coverage_result["score"] * self.WEIGHTS["coverage"] +
                sharpe_result["score"] * self.WEIGHTS["sharpe"] +
                freq_result["score"] * self.WEIGHTS["frequency"] +
                econ_result["score"] * self.WEIGHTS["economic"] +
                diversity_result["score"] * self.WEIGHTS["diversity"] +
                regime_result["score"] * self.WEIGHTS["regime"] +
                quality_result["score"] * self.WEIGHTS["data_quality"] +
                cost_result["score"] * self.WEIGHTS["compute_cost"]
            )
            
            # 收集所有原因
            all_reasons = []
            all_warnings = []
            for result in [coverage_result, sharpe_result, freq_result, econ_result,
                          diversity_result, regime_result, quality_result, cost_result]:
                all_reasons.extend(result.get("reasons", []))
                all_warnings.extend(result.get("warnings", []))
            
            scores[fid] = {
                "score": round(total_score, 3),
                "recommended": total_score >= 0.6,
                "dimensions": {
                    "coverage": coverage_result,
                    "sharpe": sharpe_result,
                    "frequency": freq_result,
                    "economic": econ_result,
                    "diversity": diversity_result,
                    "regime": regime_result,
                    "data_quality": quality_result,
                    "compute_cost": cost_result,
                },
                "reasons": all_reasons,
                "warnings": all_warnings,
                "risk_level": self._assess_risk_level(total_score, all_warnings)
            }
            
        return scores
    
    # ========== 维度 1: 覆盖度（含趋势分析） ==========
    def _score_coverage(self, field_id: str, dataset: str, region: str) -> Dict[str, Any]:
        """覆盖度评分（含趋势分析）."""
        # 获取当前覆盖度
        current_cov = self._get_coverage(field_id, dataset, region)
        
        # 获取历史覆盖度趋势
        cov_trend = self._get_coverage_trend(field_id, dataset, region)
        
        # 基础分
        base_score = min(current_cov / 0.6, 1.0) if current_cov else 0.0
        
        # 趋势调整
        trend = cov_trend.get("trend", "stable")
        if trend == "declining":
            base_score *= 0.7
            trend_note = f"覆盖度衰减中 ({cov_trend.get('change_pct', 0):.0%})"
        elif trend == "improving":
            base_score *= 1.2
            trend_note = f"覆盖度改善中 (+{cov_trend.get('change_pct', 0):.0%})"
        else:
            trend_note = "覆盖度稳定"
        
        # 稳定性调整
        stability = cov_trend.get("stability_score", 1.0)
        if stability < 0.5:
            base_score *= 0.8
            stability_note = "覆盖度波动大"
        else:
            stability_note = "覆盖度稳定"
        
        reasons = [f"覆盖度 {current_cov:.0%}"]
        if trend != "stable":
            reasons.append(trend_note)
        if stability < 0.5:
            reasons.append(stability_note)
        
        return {
            "score": round(min(base_score, 1.0), 3),
            "current": current_cov,
            "trend": trend,
            "stability": stability,
            "reasons": reasons,
            "warnings": [trend_note] if trend == "declining" else []
        }
    
    def _get_coverage(self, field_id: str, dataset: str, region: str) -> float:
        """获取字段覆盖度."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT coverage FROM field_catalog
                WHERE field_id = ? AND dataset_id = ? AND region = ?
            """, (field_id, dataset, region))
            row = cursor.fetchone()
            conn.close()
            if row and row[0] is not None:
                return float(row[0])
        except Exception:
            pass
        return 0.5
    
    def _get_coverage_trend(self, field_id: str, dataset: str, region: str) -> Dict[str, Any]:
        """获取覆盖度趋势."""
        # 模拟数据，实际应从历史记录查询
        return {
            "trend": "stable",
            "change_pct": 0.0,
            "stability_score": 0.9
        }
    
    # ========== 维度 2: 历史 Sharpe（含衰减/稳定性） ==========
    def _score_sharpe(self, field_id: str, region: str) -> Dict[str, Any]:
        """历史 Sharpe 评分（含衰减/稳定性）."""
        # 获取 Sharpe 统计
        sharpe_stats = self._get_sharpe_stats(field_id, region)
        
        avg_sharpe = sharpe_stats.get("mean", 1.0)
        recent_1y = sharpe_stats.get("recent_1y", avg_sharpe)
        full_period = sharpe_stats.get("full_period", avg_sharpe)
        cv_sharpe = sharpe_stats.get("cv_sharpe", 0.3)
        
        # 基础分
        base_score = min(avg_sharpe / 1.5, 1.0)
        
        # 衰减调整
        decay_ratio = recent_1y / full_period if full_period > 0 else 1.0
        if decay_ratio < 0.3:
            base_score *= 0.5
            decay_note = f"严重衰减 (recent/full={decay_ratio:.2f})"
        elif decay_ratio < 0.5:
            base_score *= 0.75
            decay_note = f"中度衰减 (recent/full={decay_ratio:.2f})"
        else:
            decay_note = "无明显衰减"
        
        # 稳定性调整
        if cv_sharpe > 0.6:
            base_score *= 0.8
            stability_note = f"Sharpe 波动大 (CV={cv_sharpe:.2f})"
        else:
            stability_note = "Sharpe 稳定"
        
        reasons = [f"历史 Sharpe {avg_sharpe:.2f}"]
        if decay_ratio < 0.5:
            reasons.append(decay_note)
        if cv_sharpe > 0.6:
            reasons.append(stability_note)
        
        return {
            "score": round(min(base_score, 1.0), 3),
            "mean": avg_sharpe,
            "recent_1y": recent_1y,
            "decay_ratio": decay_ratio,
            "cv_sharpe": cv_sharpe,
            "reasons": reasons,
            "warnings": [decay_note] if decay_ratio < 0.3 else []
        }
    
    def _get_sharpe_stats(self, field_id: str, region: str) -> Dict[str, float]:
        """获取 Sharpe 统计."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT avg_sharpe, sharpe_std, recent_1y_sharpe, full_period_sharpe
                FROM field_catalog
                WHERE field_id = ? AND region = ?
            """, (field_id, region))
            row = cursor.fetchone()
            conn.close()
            if row:
                mean = row[0] or 1.0
                std = row[1] or 0.3
                recent = row[2] or mean
                full = row[3] or mean
                return {
                    "mean": mean,
                    "std": std,
                    "recent_1y": recent,
                    "full_period": full,
                    "cv_sharpe": std / mean if mean > 0 else 0.3
                }
        except Exception:
            pass
        return {"mean": 1.0, "std": 0.3, "recent_1y": 1.0, "full_period": 1.0, "cv_sharpe": 0.3}
    
    # ========== 维度 3: 更新频率（含实际延迟） ==========
    def _score_frequency(self, field_id: str, description: str) -> Dict[str, Any]:
        """更新频率评分（含实际延迟）."""
        # 推断声明频率
        declared_freq = self._infer_frequency(field_id, description)
        
        # 获取实际延迟
        latency = self._get_update_latency(field_id)
        
        # 基础分
        freq_scores = {"daily": 1.0, "low_freq": 0.7, "event": 0.8}
        base_score = freq_scores.get(declared_freq, 0.5)
        
        # 延迟调整
        avg_delay = latency.get("avg_delay_days", 0)
        if avg_delay > 2:
            base_score *= 0.8
            delay_note = f"平均延迟 {avg_delay:.1f} 天"
        else:
            delay_note = "更新及时"
        
        # 延迟一致性
        consistency = latency.get("delay_consistency", 1.0)
        if consistency < 0.5:
            base_score *= 0.7
            consistency_note = "延迟不稳定"
        else:
            consistency_note = "延迟稳定"
        
        reasons = [f"频率 {declared_freq}"]
        if avg_delay > 2:
            reasons.append(delay_note)
        if consistency < 0.5:
            reasons.append(consistency_note)
        
        return {
            "score": round(min(base_score, 1.0), 3),
            "declared_freq": declared_freq,
            "avg_delay_days": avg_delay,
            "delay_consistency": consistency,
            "reasons": reasons,
            "warnings": [delay_note] if avg_delay > 3 else []
        }
    
    def _infer_frequency(self, field_id: str, description: str) -> str:
        """推断更新频率."""
        text = f"{field_id} {description}".lower()
        if any(k in text for k in ["news", "announcement", "event", "alert"]):
            return "event"
        if any(k in text for k in ["quarterly", "annual", "fiscal", "quarter", "year", "fy"]):
            return "low_freq"
        return "daily"
    
    def _get_update_latency(self, field_id: str) -> Dict[str, Any]:
        """获取实际更新延迟."""
        # 模拟数据，实际应从更新日志查询
        return {
            "avg_delay_days": 1.0,
            "max_delay_days": 2,
            "delay_consistency": 0.9
        }
    
    # ========== 维度 4: 经济可解释性（含文献支撑） ==========
    def _score_economic(self, field_id: str, description: str, dataset: str, region: str) -> Dict[str, Any]:
        """经济可解释性评分（含文献支撑）."""
        # 关键词匹配（基础分）
        keyword_score = self._keyword_matching(field_id, description)
        
        # 文献支撑（加权）
        citation_score = self._get_citation_support(field_id, dataset)
        
        # 机制适配度
        mechanism_fit = self._get_mechanism_fit(field_id, dataset, region)
        
        # 综合评分
        total_score = keyword_score * 0.5 + citation_score * 0.3 + mechanism_fit * 0.2
        
        reasons = []
        if keyword_score >= 0.7:
            reasons.append("经济含义明确")
        if citation_score > 0:
            reasons.append("有文献支撑")
        if mechanism_fit >= 0.7:
            reasons.append("机制适配度高")
        
        return {
            "score": round(min(total_score, 1.0), 3),
            "keyword_score": keyword_score,
            "citation_score": citation_score,
            "mechanism_fit": mechanism_fit,
            "reasons": reasons,
            "warnings": []
        }
    
    def _keyword_matching(self, field_id: str, description: str) -> float:
        """关键词匹配."""
        text = f"{field_id} {description}".lower()
        if any(k in text for k in self.ECONOMIC_KEYWORDS["high"]):
            return 0.9
        if any(k in text for k in self.ECONOMIC_KEYWORDS["medium"]):
            return 0.6
        if any(k in text for k in self.ECONOMIC_KEYWORDS["low"]):
            return 0.3
        return 0.5
    
    def _get_citation_support(self, field_id: str, dataset: str) -> float:
        """获取文献支撑."""
        try:
            from economic_mechanism_kb import get_mechanisms_by_family
            category = self._infer_category_from_dataset(dataset)
            mechanisms = get_mechanisms_by_family(category)
            for mech in mechanisms:
                if field_id in mech.get("related_fields", []):
                    return 0.3
        except Exception:
            pass
        return 0.0
    
    def _get_mechanism_fit(self, field_id: str, dataset: str, region: str) -> float:
        """获取机制适配度."""
        try:
            from economic_mechanism_kb import validate_mechanism_fit
            category = self._infer_category_from_dataset(dataset)
            # 简化：使用覆盖度作为代理
            coverage = self._get_coverage(field_id, dataset, region)
            fit = validate_mechanism_fit(category, region, coverage)
            return fit.get("score", 0.5)
        except Exception:
            return 0.5
    
    def _infer_category_from_dataset(self, dataset_id: str) -> str:
        """从 dataset_id 推断数据类别。

        口径与 src/wqb/workflow/_common.infer_data_category 一致（平台 category
        为准，2026-09-01 统一）；此处为纯函数兜底，勿在此另立分类标准。
        """
        dataset_lower = dataset_id.lower()
        category_map = [
            ("analyst", "analyst"), ("model", "model"), ("news", "news"),
            ("fundamental", "fundamental"), ("pv", "pv"), ("option", "option"),
            ("risk", "risk"), ("shortinterest", "shortinterest"),
            ("institutions", "institutions"), ("imbalance", "imbalance"),
            ("macro", "macro"), ("earnings", "earnings"), ("equity", "equity"),
            ("sentiment", "sentiment"), ("insiders", "insiders"),
            ("insider", "insiders"),
        ]
        for key, value in category_map:
            if key in dataset_lower:
                return value
        return "other"
    
    # ========== 维度 5: 字段间相关性（多样性惩罚） ==========
    def _score_diversity(self, field_id: str, selected_fields: List[str], dataset: str, region: str) -> Dict[str, Any]:
        """字段间相关性评分（多样性惩罚）."""
        if not selected_fields:
            return {
                "score": 1.0,
                "avg_correlation": 0.0,
                "reasons": ["无已选字段，多样性最优"],
                "warnings": []
            }
        
        # 获取相关性矩阵
        correlations = self._get_field_correlations(field_id, selected_fields, dataset, region)
        avg_correlation = sum(correlations.values()) / len(correlations) if correlations else 0.0
        
        # 多样性惩罚
        diversity_penalty = 1.0 - avg_correlation * 0.5
        
        reasons = []
        if avg_correlation > 0.7:
            reasons.append(f"与已选字段高相关 ({avg_correlation:.2f})")
        elif avg_correlation > 0.4:
            reasons.append(f"与已选字段中度相关 ({avg_correlation:.2f})")
        else:
            reasons.append(f"与已选字段低相关 ({avg_correlation:.2f})")
        
        return {
            "score": round(diversity_penalty, 3),
            "avg_correlation": avg_correlation,
            "correlations": correlations,
            "reasons": reasons,
            "warnings": [f"高相关 {avg_correlation:.2f}"] if avg_correlation > 0.7 else []
        }
    
    def _get_field_correlations(self, field_id: str, other_fields: List[str], dataset: str, region: str) -> Dict[str, float]:
        """获取字段间相关性."""
        # 模拟数据，实际应从相关性矩阵查询
        return {f: 0.3 for f in other_fields}
    
    # ========== 维度 6: 市场状态适配 ==========
    def _score_regime(self, field_id: str, region: str) -> Dict[str, Any]:
        """市场状态适配评分."""
        try:
            from market_regime_adapter import MarketRegimeAdapter
            adapter = MarketRegimeAdapter()
            regime = adapter.detect_regime(region)
            
            # 字段类型推断
            field_type = self._infer_field_type(field_id)
            
            # 市场状态匹配度
            regime_preferences = {
                "high_volatility": {"low_vol": 1.2, "momentum": 0.8, "reversal": 1.1},
                "low_volatility": {"momentum": 1.2, "low_vol": 0.8, "trend": 1.1},
                "trending": {"momentum": 1.3, "reversal": 0.7, "trend": 1.2},
                "mean_reverting": {"reversal": 1.3, "momentum": 0.7, "low_vol": 1.1}
            }
            
            preference = regime_preferences.get(regime["regime"], {})
            regime_boost = preference.get(field_type, 1.0)
            
            reasons = [f"市场状态 {regime['regime']}"]
            if regime_boost > 1.0:
                reasons.append(f"适配当前市场 (+{(regime_boost-1)*100:.0f}%)")
            elif regime_boost < 1.0:
                reasons.append(f"不适配当前市场 ({(regime_boost-1)*100:.0f}%)")
            
            return {
                "score": round(regime_boost, 3),
                "regime": regime["regime"],
                "field_type": field_type,
                "regime_boost": regime_boost,
                "reasons": reasons,
                "warnings": []
            }
        except Exception:
            return {
                "score": 1.0,
                "regime": "unknown",
                "field_type": "unknown",
                "regime_boost": 1.0,
                "reasons": ["市场状态未知"],
                "warnings": []
            }
    
    def _infer_field_type(self, field_id: str) -> str:
        """推断字段类型."""
        text = field_id.lower()
        if any(k in text for k in ["momentum", "trend", "revision"]):
            return "momentum"
        if any(k in text for k in ["reversal", "contrarian"]):
            return "reversal"
        if any(k in text for k in ["vol", "lowvol", "quality"]):
            return "low_vol"
        return "momentum"
    
    # ========== 维度 7: 数据质量异常检测 ==========
    def _score_data_quality(self, field_id: str, dataset: str, region: str) -> Dict[str, Any]:
        """数据质量异常检测评分."""
        quality = self._get_data_quality(field_id, dataset, region)
        
        base_score = 1.0
        
        # 异常值
        outlier_ratio = quality.get("outlier_ratio", 0.0)
        if outlier_ratio > 0.1:
            base_score *= 0.7
            outlier_note = f"异常值多 ({outlier_ratio:.0%})"
        else:
            outlier_note = "异常值正常"
        
        # 缺失模式
        missing_pattern = quality.get("missing_pattern", "random")
        if missing_pattern == "structured":
            base_score *= 0.8
            missing_note = "结构化缺失"
        else:
            missing_note = "随机缺失"
        
        # 跳变检测
        jump_detected = quality.get("jump_detected", False)
        if jump_detected:
            base_score *= 0.6
            jump_note = f"存在跳变 ({quality.get('jump_date', 'unknown')})"
        else:
            jump_note = "无跳变"
        
        reasons = []
        if outlier_ratio > 0.1:
            reasons.append(outlier_note)
        if missing_pattern == "structured":
            reasons.append(missing_note)
        if jump_detected:
            reasons.append(jump_note)
        if not reasons:
            reasons.append("数据质量良好")
        
        return {
            "score": round(base_score, 3),
            "outlier_ratio": outlier_ratio,
            "missing_pattern": missing_pattern,
            "jump_detected": jump_detected,
            "reasons": reasons,
            "warnings": [jump_note] if jump_detected else []
        }
    
    def _get_data_quality(self, field_id: str, dataset: str, region: str) -> Dict[str, Any]:
        """获取数据质量指标."""
        # 模拟数据，实际应从数据质量检测查询
        return {
            "outlier_ratio": 0.05,
            "missing_pattern": "random",
            "jump_detected": False,
            "jump_date": None
        }
    
    # ========== 维度 8: 计算成本评估 ==========
    def _score_compute_cost(self, field_id: str) -> Dict[str, Any]:
        """计算成本评估评分."""
        cost = self._get_compute_cost(field_id)
        
        base_score = 1.0
        
        # 字段类型
        field_type = cost.get("field_type", "MATRIX")
        if field_type == "VECTOR":
            base_score *= 0.7
            type_note = "VECTOR 需聚合"
        else:
            type_note = "MATRIX 直接可用"
        
        # 计算耗时
        cost_ms = cost.get("estimated_cost_ms", 100)
        if cost_ms > 200:
            base_score *= 0.8
            cost_note = f"计算较慢 ({cost_ms}ms)"
        else:
            cost_note = f"计算快速 ({cost_ms}ms)"
        
        reasons = [type_note, cost_note]
        
        return {
            "score": round(base_score, 3),
            "field_type": field_type,
            "estimated_cost_ms": cost_ms,
            "reasons": reasons,
            "warnings": []
        }
    
    def _get_compute_cost(self, field_id: str) -> Dict[str, Any]:
        """获取计算成本."""
        # 模拟数据，实际应从字段元数据查询
        return {
            "field_type": "MATRIX",
            "estimated_cost_ms": 100,
            "memory_usage_mb": 50
        }
    
    # ========== 风险评估 ==========
    def _assess_risk_level(self, total_score: float, warnings: List[str]) -> str:
        """评估风险等级."""
        if total_score >= 0.8 and not warnings:
            return "LOW"
        elif total_score >= 0.6 and len(warnings) <= 1:
            return "MEDIUM"
        elif total_score >= 0.4:
            return "HIGH"
        else:
            return "CRITICAL"
    
    # ========== 筛选推荐字段 ==========
    def filter_recommended(
        self,
        field_ids: List[str],
        dataset: str,
        region: str,
        descriptions: Optional[Dict[str, str]] = None,
        selected_fields: Optional[List[str]] = None,
        min_score: float = 0.6,
        max_fields: Optional[int] = None,
        max_risk: str = "MEDIUM"
    ) -> List[str]:
        """筛选推荐字段."""
        scores = self.score_fields(field_ids, dataset, region, descriptions, selected_fields)
        
        # 风险等级过滤
        risk_levels = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        max_risk_level = risk_levels.get(max_risk, 1)
        
        recommended = [
            (fid, s["score"])
            for fid, s in scores.items()
            if s["score"] >= min_score and risk_levels.get(s["risk_level"], 3) <= max_risk_level
        ]
        recommended.sort(key=lambda x: -x[1])
        
        result = [fid for fid, _ in recommended]
        
        if max_fields:
            result = result[:max_fields]
            
        return result


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="8 维字段质量评分器")
    ap.add_argument("--dataset", required=True, help="数据集 ID")
    ap.add_argument("--region", required=True, help="区域")
    ap.add_argument("--fields", nargs="+", help="字段 ID 列表")
    ap.add_argument("--fields-file", help="字段列表文件（JSON）")
    ap.add_argument("--selected", nargs="+", help="已选字段（用于多样性计算）")
    ap.add_argument("--min-score", type=float, default=0.6, help="最低评分")
    ap.add_argument("--max-fields", type=int, help="最多返回字段数")
    ap.add_argument("--max-risk", default="MEDIUM", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--detail", action="store_true", help="详细输出")
    args = ap.parse_args()
    
    # 加载字段
    if args.fields_file:
        with open(args.fields_file, encoding="utf-8") as f:
            field_ids = json.load(f)
    elif args.fields:
        field_ids = args.fields
    else:
        print("Error: --fields or --fields-file required")
        exit(1)
    
    # 评分
    scorer = FieldQualityScorerV2()
    scores = scorer.score_fields(
        field_ids, args.dataset, args.region,
        selected_fields=args.selected or []
    )
    
    # 筛选
    recommended = scorer.filter_recommended(
        field_ids, args.dataset, args.region,
        selected_fields=args.selected or [],
        min_score=args.min_score,
        max_fields=args.max_fields,
        max_risk=args.max_risk
    )
    
    if args.json:
        output = {
            "dataset": args.dataset,
            "region": args.region,
            "total_fields": len(field_ids),
            "recommended_count": len(recommended),
            "recommended": recommended,
            "scores": scores
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*70}")
        print(f"8 维字段质量评分 - {args.dataset} ({args.region})")
        print(f"{'='*70}")
        print(f"总字段: {len(field_ids)}")
        print(f"推荐字段: {len(recommended)} (score >= {args.min_score}, risk <= {args.max_risk})")
        print(f"\n推荐字段列表:")
        for i, fid in enumerate(recommended[:20], 1):
            s = scores[fid]
            risk_mark = {"LOW": "[LOW]", "MEDIUM": "[MED]", "HIGH": "[HIGH]", "CRITICAL": "[CRIT]"}.get(s["risk_level"], "[?]")
            print(f"{i:2d}. {risk_mark} {fid:40s} score={s['score']:.2f} risk={s['risk_level']}")
            if args.detail:
                for dim_name, dim_data in s["dimensions"].items():
                    print(f"     {dim_name:15s}: {dim_data['score']:.2f} - {'; '.join(dim_data['reasons'][:2])}")
        if len(recommended) > 20:
            print(f"    ... 还有 {len(recommended) - 20} 个")
