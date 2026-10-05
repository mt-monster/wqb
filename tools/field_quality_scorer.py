# -*- coding: utf-8 -*-
"""field_quality_scorer.py - 字段质量预筛器.

为 GEM 管道提供字段质量评分，优先选择高质量字段.
评分维度：覆盖度、历史 Sharpe、更新频率、经济可解释性.
"""
from __future__ import annotations
import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）

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
            wqb_root = (os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT")
                        or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(wqb_root, "data", "wqb.db")
        self.db_path = db_path
        #: score_fields 期间的批量预取缓存（避免逐字段打库）
        self._stats_cache: Dict[str, Dict[str, Any]] = {}
        
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
        # 一次批量预取真实统计（覆盖度 / alphaCount / userCount）
        self._stats_cache = self._prefetch_field_stats(dataset, region, field_ids)
        scores = {}
        
        for fid in field_ids:
            score_components = {}
            reasons = []
            st = self._stats_cache.get(fid) or {}
            alpha_count = st.get("alpha_count")
            
            # 1. 覆盖度评分 (30%)
            coverage = self._get_coverage(fid, dataset, region)
            cov_score = min(coverage / 0.6, 1.0) if coverage else 0.0
            score_components["coverage"] = cov_score * 0.3
            if coverage >= 0.6:
                reasons.append(f"高覆盖 {coverage:.0%}")
            elif coverage < 0.3:
                reasons.append(f"低覆盖 {coverage:.0%}")
            
            # 2. 历史 Sharpe 评分 (30%)（无字段级数据源时走中性 0.5）
            hist_sharpe = self._get_historical_sharpe(fid, region)
            if hist_sharpe is None:
                sharpe_score = 0.5                      # 中性，不凭空送分
            else:
                sharpe_score = min(hist_sharpe / 1.5, 1.0) if hist_sharpe else 0.0
                if hist_sharpe >= 1.5:
                    reasons.append(f"历史 Sharpe {hist_sharpe:.1f} 优秀")
                elif hist_sharpe >= 1.0:
                    reasons.append(f"历史 Sharpe {hist_sharpe:.1f} 良好")
            score_components["sharpe"] = sharpe_score * 0.3
            
            # 3. 更新频率评分 (15%)
            freq = self._infer_frequency(fid, descriptions.get(fid, ""))
            freq_score = {"daily": 1.0, "low_freq": 0.7, "event": 0.8}.get(freq, 0.5)
            score_components["frequency"] = freq_score * 0.15
            reasons.append(f"频率 {freq}")
            
            # 4. 经济可解释性评分 (10%)
            econ_score = self._economic_interpretability(fid, descriptions.get(fid, ""))
            score_components["economic"] = econ_score * 0.1
            if econ_score >= 0.7:
                reasons.append("经济含义明确")
            
            # 5. 白空间评分 (15%)：alphaCount 低 = 未被挖掘
            uncrowded = self._uncrowded_score(alpha_count)
            score_components["uncrowded"] = uncrowded * 0.15
            if alpha_count is not None:
                if coverage >= 0.6 and int(alpha_count) <= 3:
                    reasons.append(f"★白空间 覆盖{coverage:.0%}×alphaCount{int(alpha_count)}")
                elif int(alpha_count) > 1000:
                    reasons.append(f"极度拥挤 alphaCount{int(alpha_count)}")
            
            # 总分
            total_score = sum(score_components.values())
            
            scores[fid] = {
                "score": round(total_score, 3),
                "recommended": total_score >= 0.6,
                "coverage": coverage,
                "alpha_count": alpha_count,
                "historical_sharpe": hist_sharpe,
                "sharpe_available": hist_sharpe is not None,
                "frequency": freq,
                "economic_score": econ_score,
                "uncrowded_score": uncrowded,
                "components": score_components,
                "reasons": reasons
            }
            
        self._stats_cache = {}
        return scores
    
    def _prefetch_field_stats(self, dataset: str, region: str,
                              field_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """批量预取字段真实统计（一次查询，避免逐字段打库）。

        数据链：`fields.dataset_id`(int FK) ← `datasets.id`(name + region) ←
        `regions.id`(name)。真实表是 `fields`，**不是** `field_catalog`
        （该表在本库不存在，旧实现的查询一直静默失败 → coverage 恒 0.5）。

        Returns: {field_name: {"coverage": float, "alpha_count": int, "user_count": int}}
        """
        out: Dict[str, Dict[str, Any]] = {}
        if not field_ids:
            return out
        try:
            conn = db_connect(self.db_path)
            cur = conn.cursor()
            ph = ",".join("?" * len(field_ids))
            rows = cur.execute(
                f"""
                SELECT f.field_name, f.coverage, f.alpha_count, f.user_count
                FROM fields f
                JOIN datasets d ON d.id = f.dataset_id
                JOIN regions rg ON rg.id = d.region_id
                WHERE d.name = ? AND rg.name = ? AND f.field_name IN ({ph})
                """,
                [dataset, (region or "").upper(), *field_ids],
            ).fetchall()
            conn.close()
            for name, cov, ac, uc in rows:
                out[str(name)] = {"coverage": cov, "alpha_count": ac, "user_count": uc}
        except Exception:                                 # noqa: BLE001
            pass
        return out

    @staticmethod
    def _uncrowded_score(alpha_count) -> float:
        """白空间（未被挖掘）评分：alphaCount 越低越可能是空白区。

        依据论坛实证（2026-10-02）：翻字段目录时重点找「高覆盖率 × 低
        alphaCount(0–3)」的字段——未被挖掘的高覆盖字段是典型空白区。
        """
        if alpha_count is None:
            return 0.5                       # 未知 → 中性，不奖励也不惩罚
        try:
            ac = int(alpha_count)
        except (TypeError, ValueError):
            return 0.5
        if ac <= 3:
            return 1.0                       # 白空间
        if ac <= 20:
            return 0.8
        if ac <= 100:
            return 0.5
        if ac <= 1000:
            return 0.3
        return 0.1                           # 极度拥挤

    def _get_coverage(self, field_id: str, dataset: str, region: str) -> float:
        """获取字段覆盖度（真实表 `fields`；查不到才回退 0.5）。"""
        st = (self._stats_cache or {}).get(field_id)
        if st and st.get("coverage") is not None:
            try:
                return float(st["coverage"])
            except (TypeError, ValueError):
                pass
        try:
            pref = self._prefetch_field_stats(dataset, region, [field_id])
            if field_id in pref and pref[field_id].get("coverage") is not None:
                return float(pref[field_id]["coverage"])
        except Exception:                                 # noqa: BLE001
            pass
        return 0.5

    def _get_historical_sharpe(self, field_id: str, region: str) -> float:
        """获取字段历史 Sharpe。

        ⚠ 本库**没有字段级 Sharpe 数据源**（`registry_empirical` 是数据集级、
        `expressions` 是表达式级）。旧实现回退 1.0 等于凭空送分（1.0/1.5=0.67），
        导致所有字段都被标 [RECOMMENDED]。现改为回退 None → 调用方走中性分。
        """
        return None
    
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
