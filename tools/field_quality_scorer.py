# -*- coding: utf-8 -*-
"""field_quality_scorer.py - 字段质量预筛器.

为 GEM 管道提供字段质量评分，优先选择高质量字段.
评分维度：覆盖度、历史 Sharpe、更新频率、经济可解释性.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
from typing import Any, Dict, List, Optional


class FieldQualityScorer:
    """字段质量评分器."""
    
    # 经济可解释性关键词
    ECONOMIC_KEYWORDS = {
        "high": ["margin", "profit", "earnings", "growth", "return", "ratio", "yield"],
        "medium": ["revenue", "sales", "asset", "debt", "equity", "cash"],
        "low": ["price", "volume", "count", "number", "date"]
    }
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化.
        
        Args:
            db_path: wqb.db 路径，默认自动检测
        """
        if db_path is None:
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            db_path = os.path.join(wqb_root, "data", "wqb.db")
        self.db_path = db_path
        
    def score_fields(
        self,
        field_ids: List[str],
        dataset: str,
        region: str,
        descriptions: Optional[Dict[str, str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """评分字段质量.
        
        Args:
            field_ids: 字段 ID 列表
            dataset: 数据集 ID
            region: 区域
            descriptions: 字段描述 {field_id: description}
            
        Returns:
            {
                "field_id": {
                    "score": float (0-1),
                    "recommended": bool,
                    "coverage": float,
                    "historical_sharpe": float,
                    "frequency": str,
                    "economic_score": float,
                    "reasons": [...]
                }
            }
        """
        descriptions = descriptions or {}
        scores = {}
        
        for fid in field_ids:
            score_components = {}
            reasons = []
            
            # 1. 覆盖度评分 (30%)
            coverage = self._get_coverage(fid, dataset, region)
            cov_score = min(coverage / 0.6, 1.0) if coverage else 0.0
            score_components["coverage"] = cov_score * 0.3
            if coverage >= 0.6:
                reasons.append(f"高覆盖 {coverage:.0%}")
            elif coverage < 0.3:
                reasons.append(f"低覆盖 {coverage:.0%}")
            
            # 2. 历史 Sharpe 评分 (40%)
            hist_sharpe = self._get_historical_sharpe(fid, region)
            sharpe_score = min(hist_sharpe / 1.5, 1.0) if hist_sharpe else 0.0
            score_components["sharpe"] = sharpe_score * 0.4
            if hist_sharpe >= 1.5:
                reasons.append(f"历史 Sharpe {hist_sharpe:.1f} 优秀")
            elif hist_sharpe >= 1.0:
                reasons.append(f"历史 Sharpe {hist_sharpe:.1f} 良好")
            
            # 3. 更新频率评分 (20%)
            freq = self._infer_frequency(fid, descriptions.get(fid, ""))
            freq_score = {"daily": 1.0, "low_freq": 0.7, "event": 0.8}.get(freq, 0.5)
            score_components["frequency"] = freq_score * 0.2
            reasons.append(f"频率 {freq}")
            
            # 4. 经济可解释性评分 (10%)
            econ_score = self._economic_interpretability(fid, descriptions.get(fid, ""))
            score_components["economic"] = econ_score * 0.1
            if econ_score >= 0.7:
                reasons.append("经济含义明确")
            
            # 总分
            total_score = sum(score_components.values())
            
            scores[fid] = {
                "score": round(total_score, 3),
                "recommended": total_score >= 0.6,
                "coverage": coverage,
                "historical_sharpe": hist_sharpe,
                "frequency": freq,
                "economic_score": econ_score,
                "components": score_components,
                "reasons": reasons
            }
            
        return scores
    
    def _get_coverage(self, field_id: str, dataset: str, region: str) -> float:
        """获取字段覆盖度."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 从 field_catalog 查询
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
        
        # 默认返回中等覆盖
        return 0.5
    
    def _get_historical_sharpe(self, field_id: str, region: str) -> float:
        """获取字段历史 Sharpe（从 WebDataScope 或本地缓存）."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 从 field_catalog 查询历史表现
            cursor.execute("""
                SELECT avg_sharpe FROM field_catalog
                WHERE field_id = ? AND region = ?
            """, (field_id, region))
            
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0] is not None:
                return float(row[0])
        except Exception:
            pass
        
        # 默认返回 1.0
        return 1.0
    
    def _infer_frequency(self, field_id: str, description: str) -> str:
        """推断更新频率."""
        text = f"{field_id} {description}".lower()
        
        # 事件型
        if any(k in text for k in ["news", "announcement", "event", "alert"]):
            return "event"
        
        # 低频（季度/年度）
        if any(k in text for k in ["quarterly", "annual", "fiscal", "quarter", "year", "fy"]):
            return "low_freq"
        
        # 默认日频
        return "daily"
    
    def _economic_interpretability(self, field_id: str, description: str) -> float:
        """评估经济可解释性."""
        text = f"{field_id} {description}".lower()
        
        # 高可解释性
        if any(k in text for k in self.ECONOMIC_KEYWORDS["high"]):
            return 0.9
        
        # 中可解释性
        if any(k in text for k in self.ECONOMIC_KEYWORDS["medium"]):
            return 0.6
        
        # 低可解释性
        if any(k in text for k in self.ECONOMIC_KEYWORDS["low"]):
            return 0.3
        
        # 默认
        return 0.5
    
    def filter_recommended(
        self,
        field_ids: List[str],
        dataset: str,
        region: str,
        descriptions: Optional[Dict[str, str]] = None,
        min_score: float = 0.6,
        max_fields: Optional[int] = None
    ) -> List[str]:
        """筛选推荐字段.
        
        Returns:
            按质量排序的字段 ID 列表
        """
        scores = self.score_fields(field_ids, dataset, region, descriptions)
        
        # 过滤并排序
        recommended = [
            (fid, s["score"])
            for fid, s in scores.items()
            if s["score"] >= min_score
        ]
        recommended.sort(key=lambda x: -x[1])
        
        result = [fid for fid, _ in recommended]
        
        if max_fields:
            result = result[:max_fields]
            
        return result


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="字段质量预筛器")
    ap.add_argument("--dataset", required=True, help="数据集 ID")
    ap.add_argument("--region", required=True, help="区域")
    ap.add_argument("--fields", nargs="+", help="字段 ID 列表")
    ap.add_argument("--fields-file", help="字段列表文件（JSON）")
    ap.add_argument("--min-score", type=float, default=0.6, help="最低评分")
    ap.add_argument("--max-fields", type=int, help="最多返回字段数")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
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
    scorer = FieldQualityScorer()
    scores = scorer.score_fields(field_ids, args.dataset, args.region)
    
    # 筛选
    recommended = scorer.filter_recommended(
        field_ids, args.dataset, args.region,
        min_score=args.min_score,
        max_fields=args.max_fields
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
        print(f"\n{'='*60}")
        print(f"字段质量评分 - {args.dataset} ({args.region})")
        print(f"{'='*60}")
        print(f"总字段: {len(field_ids)}")
        print(f"推荐字段: {len(recommended)} (score >= {args.min_score})")
        print(f"\n推荐字段列表:")
        for i, fid in enumerate(recommended[:20], 1):
            s = scores[fid]
            print(f"{i:2d}. {fid:40s} score={s['score']:.2f} "
                  f"cov={s['coverage']:.0%} sharpe={s['historical_sharpe']:.1f}")
        if len(recommended) > 20:
            print(f"    ... 还有 {len(recommended) - 20} 个")
