# -*- coding: utf-8 -*-
"""market_regime_adapter.py - 市场状态适配器.

为 GEM 管道提供市场状态检测，动态推荐信号方向（sign=±1）.
基于波动率、趋势强度、市场情绪等指标判断市场状态.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, Optional


class MarketRegimeAdapter:
    """市场状态适配器."""
    
    # 市场状态定义
    REGIMES = {
        "high_volatility": {
            "description": "高波动市场",
            "volatility_threshold": 0.25,
            "preferred_strategies": ["reversal", "defensive"],
            "preferred_sign": -1
        },
        "low_volatility": {
            "description": "低波动市场",
            "volatility_threshold": 0.15,
            "preferred_strategies": ["momentum", "trend"],
            "preferred_sign": 1
        },
        "trending": {
            "description": "趋势市场",
            "trend_threshold": 0.6,
            "preferred_strategies": ["momentum"],
            "preferred_sign": 1
        },
        "mean_reverting": {
            "description": "均值回归市场",
            "trend_threshold": 0.3,
            "preferred_strategies": ["reversal"],
            "preferred_sign": -1
        }
    }
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化."""
        if db_path is None:
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            db_path = os.path.join(wqb_root, "data", "wqb.db")
        self.db_path = db_path
        
    def detect_regime(self, region: str, lookback_days: int = 20) -> Dict[str, Any]:
        """检测市场状态.
        
        Args:
            region: 区域
            lookback_days: 回望天数
            
        Returns:
            {
                "regime": str,
                "volatility": float,
                "trend_strength": float,
                "confidence": float,
                "preferred_sign": int,
                "reason": str
            }
        """
        # 计算市场指标
        volatility = self._calculate_volatility(region, lookback_days)
        trend_strength = self._calculate_trend_strength(region, lookback_days)
        
        # 判断状态
        if volatility > 0.25:
            regime = "high_volatility"
            preferred_sign = -1
            reason = f"高波动 ({volatility:.1%})，反转策略更优"
        elif volatility < 0.15:
            regime = "low_volatility"
            preferred_sign = 1
            reason = f"低波动 ({volatility:.1%})，动量策略更优"
        elif trend_strength > 0.6:
            regime = "trending"
            preferred_sign = 1
            reason = f"趋势强 ({trend_strength:.1%})，动量策略更优"
        elif trend_strength < 0.3:
            regime = "mean_reverting"
            preferred_sign = -1
            reason = f"趋势弱 ({trend_strength:.1%})，反转策略更优"
        else:
            regime = "neutral"
            preferred_sign = 1
            reason = "中性市场，默认动量"
        
        # 置信度
        confidence = self._calculate_confidence(volatility, trend_strength)
        
        return {
            "regime": regime,
            "volatility": round(volatility, 3),
            "trend_strength": round(trend_strength, 3),
            "confidence": round(confidence, 2),
            "preferred_sign": preferred_sign,
            "reason": reason,
            "lookback_days": lookback_days,
            "detected_at": datetime.now().isoformat()
        }
    
    def _calculate_volatility(self, region: str, days: int) -> float:
        """计算市场波动率."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 从市场数据表查询（如有）
            # 这里使用模拟数据，实际应从平台或本地缓存获取
            cursor.execute("""
                SELECT volatility FROM market_regime
                WHERE region = ? AND date >= date('now', '-{} days')
                ORDER BY date DESC LIMIT 1
            """.format(days), (region,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0] is not None:
                return float(row[0])
        except Exception:
            pass
        
        # 默认返回中等波动
        return 0.20
    
    def _calculate_trend_strength(self, region: str, days: int) -> float:
        """计算趋势强度."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT trend_strength FROM market_regime
                WHERE region = ? AND date >= date('now', '-{} days')
                ORDER BY date DESC LIMIT 1
            """.format(days), (region,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0] is not None:
                return float(row[0])
        except Exception:
            pass
        
        # 默认返回中等趋势
        return 0.5
    
    def _calculate_confidence(self, volatility: float, trend_strength: float) -> float:
        """计算状态判断置信度."""
        # 波动率极端时置信度高
        vol_confidence = abs(volatility - 0.20) / 0.20
        
        # 趋势极端时置信度高
        trend_confidence = abs(trend_strength - 0.5) / 0.5
        
        # 综合置信度
        return min((vol_confidence + trend_confidence) / 2, 1.0)
    
    def get_sign_recommendation(
        self,
        field_family: str,
        region: str,
        mechanism_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取信号方向推荐.
        
        Args:
            field_family: 字段族
            region: 区域
            mechanism_id: 经济机制 ID（可选）
            
        Returns:
            {
                "recommended_sign": int (1 or -1),
                "confidence": float,
                "regime": str,
                "reason": str,
                "alternative_sign": int,
                "alternative_reason": str
            }
        """
        regime = self.detect_regime(region)
        
        # 基于市场状态的推荐
        base_sign = regime["preferred_sign"]
        
        # 基于字段族的调整
        family_adjustments = {
            "pv": {"momentum": 1, "reversal": -1},
            "analyst": {"revision": 1, "dispersion": -1},
            "news": {"sentiment": -1, "disagreement": -1},
            "fundamental": {"momentum": 1, "value": -1}
        }
        
        # 如果指定了机制，使用机制特定的方向偏好
        if mechanism_id:
            mech_sign = self._get_mechanism_sign(mechanism_id, regime["regime"])
            if mech_sign:
                return {
                    "recommended_sign": mech_sign,
                    "confidence": regime["confidence"] * 0.9,
                    "regime": regime["regime"],
                    "reason": f"{regime['reason']}，机制 {mechanism_id} 适配",
                    "alternative_sign": -mech_sign,
                    "alternative_reason": "反向假设（需验证）"
                }
        
        return {
            "recommended_sign": base_sign,
            "confidence": regime["confidence"],
            "regime": regime["regime"],
            "reason": regime["reason"],
            "alternative_sign": -base_sign,
            "alternative_reason": "反向假设（需验证）"
        }
    
    def _get_mechanism_sign(self, mechanism_id: str, regime: str) -> Optional[int]:
        """获取机制在特定市场状态下的方向偏好."""
        # 机制特定规则
        mechanism_rules = {
            "price_momentum": {
                "trending": 1,
                "high_volatility": -1,
                "mean_reverting": -1
            },
            "news_sentiment_momentum": {
                "high_volatility": -1,
                "low_volatility": 1
            },
            "analyst_revision": {
                "trending": 1,
                "mean_reverting": -1
            }
        }
        
        rules = mechanism_rules.get(mechanism_id)
        if rules:
            return rules.get(regime)
        
        return None


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="市场状态适配器")
    ap.add_argument("--region", required=True, help="区域")
    ap.add_argument("--family", help="字段族")
    ap.add_argument("--mechanism", help="经济机制 ID")
    ap.add_argument("--lookback", type=int, default=20, help="回望天数")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()
    
    adapter = MarketRegimeAdapter()
    
    # 检测市场状态
    regime = adapter.detect_regime(args.region, args.lookback)
    
    if args.json:
        output = {"regime": regime}
        
        if args.family:
            sign_rec = adapter.get_sign_recommendation(
                args.family, args.region, args.mechanism
            )
            output["sign_recommendation"] = sign_rec
        
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"市场状态检测 - {args.region}")
        print(f"{'='*60}")
        print(f"状态: {regime['regime']}")
        print(f"波动率: {regime['volatility']:.1%}")
        print(f"趋势强度: {regime['trend_strength']:.1%}")
        print(f"置信度: {regime['confidence']:.0%}")
        print(f"推荐方向: {'+' if regime['preferred_sign'] > 0 else '-'}1")
        print(f"原因: {regime['reason']}")
        
        if args.family:
            sign_rec = adapter.get_sign_recommendation(
                args.family, args.region, args.mechanism
            )
            print(f"\n信号方向推荐 ({args.family}):")
            print(f"  推荐: {'+' if sign_rec['recommended_sign'] > 0 else '-'}1 "
                  f"(置信度 {sign_rec['confidence']:.0%})")
            print(f"  原因: {sign_rec['reason']}")
