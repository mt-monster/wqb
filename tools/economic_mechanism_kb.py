# -*- coding: utf-8 -*-
"""economic_mechanism_kb.py - 经济机制知识库.

为 GEM 管道提供有文献支撑的经济机制，替代静态通用的 CATEGORY_PRIMITIVES.
每个机制包含：经济逻辑、文献引用、最优条件、失败模式、区域适配.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


# 经济机制知识库
ECONOMIC_MECHANISM_KB: Dict[str, Dict[str, Any]] = {
    # ========== Analyst 分析师 ==========
    "analyst_revision": {
        "family": "analyst",
        "mechanism": "分析师盈利预测修正反映信息优势，修正方向预测未来收益",
        "citation": "Jegadeesh, Kim, Krische & Lee (2004) - Analyzing the Analysts: When Do Recommendations Add Value?",
        "economic_rationale": "分析师覆盖多的股票，其盈利预测修正包含私有信息，修正方向与未来收益正相关",
        "optimal_conditions": {
            "coverage_min": 0.6,
            "dispersion_min": 0.3,
            "revision_consistency": 0.7,
            "analyst_count_min": 5
        },
        "failure_modes": [
            "低覆盖度时噪声主导",
            "修正滞后于价格",
            "拥挤交易导致信号衰减",
            "分析师羊群效应"
        ],
        "region_adaptation": {
            "USA": {"coverage_threshold": 0.6, "note": "覆盖充分，标准条件"},
            "IND": {"coverage_threshold": 0.4, "note": "覆盖不足，需放宽阈值"},
            "KOR": {"coverage_threshold": 0.5, "note": "中等覆盖，关注大盘股"},
            "EUR": {"coverage_threshold": 0.55, "note": "覆盖良好，标准条件"}
        },
        "expected_sharpe_range": (1.2, 2.5),
        "expected_turnover": "medium",
        "correlation_with_common_factors": {"value": 0.3, "momentum": 0.5, "quality": 0.4},
        "implementation_hints": [
            "使用 revision 而非 level",
            "关注 breadth（修正家数）而非仅 magnitude",
            "结合 dispersion 过滤低置信度信号"
        ]
    },
    "analyst_dispersion": {
        "family": "analyst",
        "mechanism": "分析师预测离散度反映信息不确定性，高离散度股票未来收益更低",
        "citation": "Diether, Malloy & Scherbina (2002) - Differences of Opinion and the Cross Section of Stock Returns",
        "economic_rationale": "离散度高意味着信息不对称严重，悲观者无法做空，价格被乐观者推高，未来收益低",
        "optimal_conditions": {
            "dispersion_percentile": ">70%",
            "analyst_count_min": 3,
            "market_cap": "small_mid"
        },
        "failure_modes": [
            "小样本离散度噪声大",
            "行业特性导致离散度系统性差异"
        ],
        "region_adaptation": {
            "USA": {"note": "效果稳定，覆盖充分"},
            "IND": {"note": "覆盖不足，谨慎使用"}
        },
        "expected_sharpe_range": (0.8, 1.8),
        "expected_turnover": "low",
        "correlation_with_common_factors": {"value": -0.2, "volatility": 0.6}
    },
    
    # ========== Fundamental 基本面 ==========
    "fundamental_momentum": {
        "family": "fundamental",
        "mechanism": "基本面动量源于信息扩散缓慢，财报信息逐步反映到价格",
        "citation": "Novy-Marx (2013) - The Other Side of Value: The Gross Profitability Premium",
        "economic_rationale": "盈利质量高、增长稳定的公司，其基本面改善趋势会持续，形成动量",
        "optimal_conditions": {
            "earnings_quality": "high",
            "growth_stability": "consistent",
            "industry_diversification": True
        },
        "failure_modes": [
            "周期顶部反转",
            "价值陷阱",
            "会计操纵"
        ],
        "region_adaptation": {
            "USA": {"note": "效果稳定"},
            "IND": {"note": "财报质量参差，需筛选"}
        },
        "expected_sharpe_range": (1.0, 2.0),
        "expected_turnover": "low",
        "correlation_with_common_factors": {"value": 0.4, "quality": 0.7, "momentum": 0.3}
    },
    "earnings_quality": {
        "family": "fundamental",
        "mechanism": "应计利润与现金流的 gap 反映盈利质量，低质量盈利未来反转",
        "citation": "Sloan (1996) - Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?",
        "economic_rationale": "应计利润高而现金流低的公司，盈利质量差，未来收益低",
        "optimal_conditions": {
            "accrual_ratio": "extreme",
            "cash_flow_positive": True
        },
        "failure_modes": [
            "成长期公司应计高属正常",
            "行业特性差异"
        ],
        "expected_sharpe_range": (0.9, 1.6),
        "expected_turnover": "low",
        "correlation_with_common_factors": {"value": 0.5, "quality": 0.6}
    },
    
    # ========== News/Sentiment 新闻情绪 ==========
    "news_sentiment_momentum": {
        "family": "news",
        "mechanism": "新闻情绪反映投资者注意力与情绪，极端情绪预测反转",
        "citation": "Tetlock (2007) - Giving Content to Investor Sentiment: The Role of Media in the Stock Market",
        "economic_rationale": "极端乐观情绪后收益低，极端悲观后收益高，温和情绪预测动量",
        "optimal_conditions": {
            "sentiment_extremity": "high",
            "news_volume": "above_average",
            "stock_attention": "high"
        },
        "failure_modes": [
            "新闻覆盖不足",
            "情绪指标滞后",
            "噪声交易主导"
        ],
        "region_adaptation": {
            "USA": {"note": "覆盖充分，效果稳定"},
            "IND": {"note": "新闻覆盖不足，信号弱", "caution": True}
        },
        "expected_sharpe_range": (0.7, 1.5),
        "expected_turnover": "high",
        "correlation_with_common_factors": {"momentum": 0.4, "volatility": 0.5}
    },
    "news_disagreement": {
        "family": "news",
        "mechanism": "多源新闻情绪分歧反映信息不确定性，分歧大时未来收益低",
        "citation": "Gentzkow & Shapiro (2006) - Media Bias and Reputation",
        "economic_rationale": "不同来源情绪分歧大，说明信息不确定，投资者要求更高风险溢价",
        "optimal_conditions": {
            "source_count": ">=3",
            "disagreement_level": "high"
        },
        "failure_modes": ["小样本分歧噪声大"],
        "expected_sharpe_range": (0.6, 1.2),
        "expected_turnover": "medium"
    },
    
    # ========== PV 量价 ==========
    "price_momentum": {
        "family": "pv",
        "mechanism": "价格动量源于信息扩散缓慢和投资者反应不足",
        "citation": "Jegadeesh & Titman (1993) - Returns to Buying Winners and Selling Losers",
        "economic_rationale": "过去 3-12 个月赢家未来继续跑赢，输家继续跑输",
        "optimal_conditions": {
            "formation_period": "3-12 months",
            "skip_recent": "1 month"
        },
        "failure_modes": [
            "动量崩溃（momentum crash）",
            "高波动时期反转"
        ],
        "region_adaptation": {
            "USA": {"note": "效果稳定"},
            "IND": {"note": "波动大，需缩短周期"}
        },
        "expected_sharpe_range": (1.0, 2.0),
        "expected_turnover": "medium",
        "correlation_with_common_factors": {"momentum": 0.9}
    },
    "volume_price_divergence": {
        "family": "pv",
        "mechanism": "量价背离反映趋势可持续性，价涨量缩预示反转",
        "citation": "Llorente, Michaely, Saar & Wang (2002) - Dynamic Volume-Return Relation of Individual Stocks",
        "economic_rationale": "价格上涨但成交量萎缩，说明买盘力量减弱，趋势不可持续",
        "optimal_conditions": {
            "price_trend": "established",
            "volume_trend": "diverging"
        },
        "failure_modes": ["噪声交易干扰"],
        "expected_sharpe_range": (0.8, 1.4),
        "expected_turnover": "high"
    },
    
    # ========== Model 模型 ==========
    "quality_minus_yield": {
        "family": "model",
        "mechanism": "质量因子与价值因子的残差，捕捉纯粹的质量溢价",
        "citation": "Asness, Frazzini & Pedersen (2019) - Quality Minus Junk",
        "economic_rationale": "剥离价值暴露后的纯质量因子，风险调整后收益更稳定",
        "optimal_conditions": {
            "quality_metric": "composite",
            "value_neutralization": True
        },
        "failure_modes": ["质量拥挤"],
        "expected_sharpe_range": (1.2, 2.2),
        "expected_turnover": "low",
        "correlation_with_common_factors": {"quality": 0.8, "value": -0.3}
    },
    
    # ========== Institutions 机构 ==========
    "institutional_flow": {
        "family": "institutions",
        "mechanism": "机构持仓变化反映专业投资者信息优势",
        "citation": "Gompers & Metrick (2001) - Institutional Investors and Equity Prices",
        "economic_rationale": "机构增持的股票未来收益高，减持的未来收益低",
        "optimal_conditions": {
            "holding_change": "significant",
            "institution_type": "active"
        },
        "failure_modes": ["披露滞后", "拥挤交易"],
        "expected_sharpe_range": (0.9, 1.7),
        "expected_turnover": "low"
    }
}


def get_mechanism(mechanism_id: str) -> Optional[Dict[str, Any]]:
    """获取指定机制详情."""
    return ECONOMIC_MECHANISM_KB.get(mechanism_id)


def get_mechanisms_by_family(family: str) -> List[Dict[str, Any]]:
    """按字段族获取机制列表."""
    return [
        {"id": k, **v}
        for k, v in ECONOMIC_MECHANISM_KB.items()
        if v.get("family") == family
    ]


def validate_mechanism_fit(
    mechanism_id: str,
    region: str,
    coverage: float,
    dispersion: Optional[float] = None
) -> Dict[str, Any]:
    """校验机制在当前条件下的适配度.
    
    Returns:
        {
            "fit": bool,
            "score": float (0-1),
            "reasons": [...],
            "warnings": [...]
        }
    """
    mech = ECONOMIC_MECHANISM_KB.get(mechanism_id)
    if not mech:
        return {"fit": False, "score": 0.0, "reasons": ["mechanism not found"]}
    
    score = 1.0
    reasons = []
    warnings = []
    
    # 覆盖度校验
    region_adapt = mech.get("region_adaptation", {}).get(region, {})
    cov_threshold = region_adapt.get("coverage_threshold") or mech["optimal_conditions"].get("coverage_min", 0.5)
    
    if coverage < cov_threshold:
        score *= 0.5
        warnings.append(f"coverage {coverage:.1%} < threshold {cov_threshold:.1%}")
    else:
        reasons.append(f"coverage {coverage:.1%} >= threshold {cov_threshold:.1%}")
    
    # 离散度校验（如适用）
    if dispersion is not None and "dispersion_min" in mech["optimal_conditions"]:
        disp_min = mech["optimal_conditions"]["dispersion_min"]
        if dispersion < disp_min:
            score *= 0.7
            warnings.append(f"dispersion {dispersion:.2f} < min {disp_min}")
    
    # 区域警告
    if region_adapt.get("caution"):
        score *= 0.6
        warnings.append(f"region {region} caution: {region_adapt.get('note', '')}")
    
    return {
        "fit": score >= 0.5,
        "score": round(score, 2),
        "reasons": reasons,
        "warnings": warnings,
        "mechanism": mech["mechanism"],
        "citation": mech["citation"]
    }


def format_mechanism_for_prompt(mechanism_id: str, region: str) -> str:
    """格式化机制信息用于 GEM prompt."""
    mech = ECONOMIC_MECHANISM_KB.get(mechanism_id)
    if not mech:
        return ""
    
    lines = [
        f"**{mechanism_id}**: {mech['mechanism']}",
        f"- Citation: {mech['citation']}",
        f"- Expected Sharpe: {mech['expected_sharpe_range'][0]:.1f}-{mech['expected_sharpe_range'][1]:.1f}",
        f"- Optimal: {', '.join(f'{k}={v}' for k, v in mech['optimal_conditions'].items())}",
    ]
    
    region_adapt = mech.get("region_adaptation", {}).get(region)
    if region_adapt:
        lines.append(f"- Region {region}: {region_adapt.get('note', '')}")
    
    if mech.get("failure_modes"):
        lines.append(f"- Failure modes: {', '.join(mech['failure_modes'][:3])}")
    
    return "\n".join(lines)


# CLI 入口
if __name__ == "__main__":
    import argparse
    import json
    
    ap = argparse.ArgumentParser(description="经济机制知识库查询")
    ap.add_argument("--mechanism", help="机制 ID")
    ap.add_argument("--family", help="按字段族查询")
    ap.add_argument("--region", default="USA", help="区域")
    ap.add_argument("--coverage", type=float, help="覆盖度")
    ap.add_argument("--list", action="store_true", help="列出所有机制")
    args = ap.parse_args()
    
    if args.list:
        print(json.dumps(list(ECONOMIC_MECHANISM_KB.keys()), indent=2))
    elif args.mechanism:
        mech = get_mechanism(args.mechanism)
        if mech:
            print(json.dumps(mech, indent=2, ensure_ascii=False))
            if args.coverage:
                fit = validate_mechanism_fit(args.mechanism, args.region, args.coverage)
                print("\n适配度评估:")
                print(json.dumps(fit, indent=2, ensure_ascii=False))
        else:
            print(f"Mechanism not found: {args.mechanism}")
    elif args.family:
        mechs = get_mechanisms_by_family(args.family)
        print(json.dumps(mechs, indent=2, ensure_ascii=False))
    else:
        ap.print_help()
