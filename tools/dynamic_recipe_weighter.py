# -*- coding: utf-8 -*-
"""dynamic_recipe_weighter.py - 成功配方动态权重.

为 GEM 管道提供成功配方的动态权重调整.
基于时间衰减、区域适配、多样性保障计算配方权重.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional


class DynamicRecipeWeighter:
    """成功配方动态权重器."""
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化."""
        if db_path is None:
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            db_path = os.path.join(wqb_root, "data", "wqb.db")
        self.db_path = db_path
        
    def weight_recipes(
        self,
        wins: List[Dict[str, Any]],
        region: str,
        current_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """计算配方动态权重.
        
        Args:
            wins: 成功配方列表
            region: 目标区域
            current_date: 当前日期（默认今天）
            
        Returns:
            按权重排序的配方列表，每个配方添加：
            - dynamic_weight: 动态权重 (0-1)
            - time_decay: 时间衰减因子
            - region_boost: 区域适配因子
            - diversity_penalty: 多样性惩罚因子
            - recommended_usage: 是否推荐使用
        """
        if current_date is None:
            current_date = datetime.now()
        
        weighted = []
        
        for w in wins:
            # 1. 时间衰减（近期成功配方权重更高）
            time_decay = self._calculate_time_decay(w, current_date)
            
            # 2. 区域适配（同区域配方权重更高）
            region_boost = self._calculate_region_boost(w, region)
            
            # 3. 多样性惩罚（避免单一配方主导）
            diversity_penalty = self._calculate_diversity_penalty(w, wins)
            
            # 4. 成功率加权
            success_rate = w.get("success_rate", 0.5)
            success_boost = 0.5 + success_rate * 0.5  # 0.5-1.0
            
            # 综合权重
            dynamic_weight = time_decay * region_boost * diversity_penalty * success_boost
            
            weighted.append({
                **w,
                "dynamic_weight": round(dynamic_weight, 3),
                "time_decay": round(time_decay, 3),
                "region_boost": round(region_boost, 3),
                "diversity_penalty": round(diversity_penalty, 3),
                "success_boost": round(success_boost, 3),
                "recommended_usage": dynamic_weight >= 0.5
            })
        
        # 按权重排序
        weighted.sort(key=lambda x: -x["dynamic_weight"])
        
        return weighted
    
    def _calculate_time_decay(
        self,
        recipe: Dict[str, Any],
        current_date: datetime
    ) -> float:
        """计算时间衰减因子.
        
        使用指数衰减：0.95^(days/30)
        - 30 天前：0.95
        - 90 天前：0.86
        - 180 天前：0.74
        - 365 天前：0.54
        """
        date_str = recipe.get("date") or recipe.get("created_at")
        if not date_str:
            return 0.8  # 无日期信息，默认中等权重
        
        try:
            if isinstance(date_str, str):
                recipe_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                recipe_date = date_str
            
            days_ago = (current_date - recipe_date).days
            decay = 0.95 ** (days_ago / 30)
            
            return max(decay, 0.3)  # 最低 0.3
            
        except Exception:
            return 0.8
    
    def _calculate_region_boost(
        self,
        recipe: Dict[str, Any],
        target_region: str
    ) -> float:
        """计算区域适配因子.
        
        - 同区域：1.2
        - 相似区域（同 tier）：1.1
        - 其他区域：1.0
        """
        recipe_region = recipe.get("region", "")
        
        if recipe_region == target_region:
            return 1.2
        
        # 区域 tier 映射
        region_tiers = {
            "USA": "developed",
            "EUR": "developed",
            "GBR": "developed",
            "DEU": "developed",
            "KOR": "emerging",
            "IND": "emerging",
            "CHN": "emerging",
            "JPN": "developed",
            "ASI": "emerging",
            "GLB": "global"
        }
        
        recipe_tier = region_tiers.get(recipe_region, "unknown")
        target_tier = region_tiers.get(target_region, "unknown")
        
        if recipe_tier == target_tier and recipe_tier != "unknown":
            return 1.1
        
        return 1.0
    
    def _calculate_diversity_penalty(
        self,
        recipe: Dict[str, Any],
        all_recipes: List[Dict[str, Any]]
    ) -> float:
        """计算多样性惩罚因子.
        
        避免单一配方主导：
        - 使用次数越多，惩罚越重
        - 同族配方越多，惩罚越重
        """
        # 使用次数惩罚
        usage_count = recipe.get("usage_count", 0)
        usage_penalty = 1.0 / (1 + usage_count * 0.1)
        
        # 同族配方惩罚
        recipe_family = recipe.get("family") or recipe.get("category", "")
        same_family_count = sum(
            1 for r in all_recipes
            if (r.get("family") or r.get("category", "")) == recipe_family
        )
        family_penalty = 1.0 / (1 + same_family_count * 0.05)
        
        return usage_penalty * family_penalty
    
    def get_recommended_recipes(
        self,
        wins: List[Dict[str, Any]],
        region: str,
        max_recipes: int = 5,
        min_weight: float = 0.5
    ) -> List[Dict[str, Any]]:
        """获取推荐配方.
        
        Returns:
            权重 >= min_weight 的前 max_recipes 个配方
        """
        weighted = self.weight_recipes(wins, region)
        
        recommended = [
            w for w in weighted
            if w["dynamic_weight"] >= min_weight
        ]
        
        return recommended[:max_recipes]
    
    def format_recipes_for_prompt(
        self,
        wins: List[Dict[str, Any]],
        region: str,
        max_recipes: int = 5
    ) -> str:
        """格式化配方信息用于 GEM prompt."""
        recommended = self.get_recommended_recipes(wins, region, max_recipes)
        
        if not recommended:
            return ""
        
        lines = ["**Recommended Win Recipes** (dynamically weighted):"]
        
        for i, w in enumerate(recommended, 1):
            lines.append(
                f"{i}. **{w.get('id', 'unknown')}** "
                f"(weight={w['dynamic_weight']:.2f}, "
                f"region={w.get('region', 'N/A')}, "
                f"sharpe={w.get('avg_sharpe', 'N/A')})"
            )
            lines.append(f"   Mechanism: {w.get('mechanism', w.get('key', 'N/A'))}")
            lines.append(f"   Fields: {w.get('fields', 'N/A')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def record_recipe_usage(
        self,
        recipe_id: str,
        region: str,
        success: bool,
        sharpe: Optional[float] = None
    ) -> None:
        """记录配方使用情况（用于后续权重调整）."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 更新使用次数
            cursor.execute("""
                INSERT INTO recipe_usage (recipe_id, region, usage_count, last_used, success_count, total_sharpe)
                VALUES (?, ?, 1, ?, ?, ?)
                ON CONFLICT(recipe_id, region) DO UPDATE SET
                    usage_count = usage_count + 1,
                    last_used = ?,
                    success_count = success_count + ?,
                    total_sharpe = total_sharpe + ?
            """, (
                recipe_id, region,
                datetime.now().isoformat(),
                1 if success else 0,
                sharpe or 0,
                datetime.now().isoformat(),
                1 if success else 0,
                sharpe or 0
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            # 静默失败，不影响主流程
            pass


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="成功配方动态权重")
    ap.add_argument("--region", required=True, help="目标区域")
    ap.add_argument("--wins-file", help="成功配方文件（JSON）")
    ap.add_argument("--max-recipes", type=int, default=5, help="最多推荐配方数")
    ap.add_argument("--min-weight", type=float, default=0.5, help="最低权重")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()
    
    # 加载配方
    if args.wins_file:
        with open(args.wins_file, encoding="utf-8") as f:
            wins = json.load(f)
    else:
        # 示例配方
        wins = [
            {
                "id": "IND-ANALYST-FUNDAMENTAL-WIN",
                "region": "IND",
                "family": "analyst",
                "mechanism": "analyst_revision + fundamental",
                "fields": ["analyst_revision_percentile_score_long_4", "fnd86_earnings_score"],
                "avg_sharpe": 2.17,
                "success_rate": 0.75,
                "date": "2026-08-30",
                "usage_count": 3
            },
            {
                "id": "USA-QUALITY-MOMENTUM-WIN",
                "region": "USA",
                "family": "model",
                "mechanism": "quality_minus_yield",
                "fields": ["quality_score", "momentum_12m"],
                "avg_sharpe": 1.85,
                "success_rate": 0.68,
                "date": "2026-08-15",
                "usage_count": 5
            }
        ]
    
    # 计算权重
    weighter = DynamicRecipeWeighter()
    weighted = weighter.weight_recipes(wins, args.region)
    recommended = weighter.get_recommended_recipes(
        wins, args.region, args.max_recipes, args.min_weight
    )
    
    if args.json:
        output = {
            "region": args.region,
            "total_recipes": len(wins),
            "recommended_count": len(recommended),
            "recommended": recommended
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"成功配方动态权重 - {args.region}")
        print(f"{'='*60}")
        print(f"总配方: {len(wins)}")
        print(f"推荐配方: {len(recommended)} (weight >= {args.min_weight})")
        print(f"\n推荐配方列表:")
        for i, w in enumerate(recommended, 1):
            print(f"{i}. {w['id']}")
            print(f"   权重: {w['dynamic_weight']:.2f} "
                  f"(time={w['time_decay']:.2f}, "
                  f"region={w['region_boost']:.2f}, "
                  f"diversity={w['diversity_penalty']:.2f})")
            print(f"   机制: {w.get('mechanism', 'N/A')}")
            print(f"   字段: {w.get('fields', 'N/A')}")
            print()
