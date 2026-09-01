# -*- coding: utf-8 -*-
"""economic_mechanism_templates.py - 经济学机制模板库.

基于经济学意义生成复杂 alpha 表达式模板，每个机制都有文献支撑.
"""
from __future__ import annotations

from typing import Any, Dict, List


# ============================================================================
# P0 机制：高优先级经济学机制
# ============================================================================

ECONOMIC_MECHANISM_TEMPLATES: Dict[str, Dict[str, Any]] = {
    
    # ========== P0-1: 分析师分歧机制 ==========
    "analyst_dispersion": {
        "mechanism_id": "analyst_dispersion",
        "priority": "P0",
        "category": "analyst",
        "economic_meaning": "分析师预测分歧反映信息不确定性，高分歧股票未来收益低",
        "citation": "Diether, Malloy & Scherbina (2002) - Differences of Opinion and the Cross Section of Stock Returns",
        "expected_sharpe": (1.5, 2.5),
        "operators": ["vec_stddev", "vec_avg", "vec_count", "rank", "trade_when", "greater"],
        "templates": [
            {
                "name": "纯分析师分歧",
                "expression": "rank(vec_stddev(analyst_estimates))",
                "description": "直接使用分析师预测分歧作为信号",
                "economic_logic": "分歧越大，信息不确定性越高，未来收益越低",
            },
            {
                "name": "分歧 × 修正方向（复杂经济学模板）",
                "expression": "add(multiply(0.6, rank(vec_avg(analyst_revision))), multiply(0.4, rank(vec_stddev(analyst_estimates))))",
                "description": "修正方向（慢变量）× 分歧度（快变量）",
                "economic_logic": "修正方向明确但分歧大的股票，未来收益更高",
            },
            {
                "name": "分歧 × 覆盖度（门控机制）",
                "expression": "trade_when(greater(vec_count(analyst_estimates), 5), rank(vec_stddev(analyst_estimates)), 0)",
                "description": "覆盖度 > 5 时才交易分歧信号",
                "economic_logic": "覆盖不足时分歧信号不可靠",
            },
        ],
    },
    
    # ========== P0-2: 信息衰减机制 ==========
    "information_decay": {
        "mechanism_id": "information_decay",
        "priority": "P0",
        "category": "analyst",
        "economic_meaning": "分析师修正后的信息会随时间衰减，新鲜修正比陈旧修正更有预测力",
        "citation": "Tetlock (2007) - Giving Content to Investor Sentiment",
        "expected_sharpe": (1.3, 2.2),
        "operators": ["days_from_last_change", "ts_delta", "rank", "trade_when", "less", "add", "multiply"],
        "templates": [
            {
                "name": "纯信息新鲜度",
                "expression": "rank(days_from_last_change(analyst_revision))",
                "description": "距上次修正天数越短，信号越强",
                "economic_logic": "新鲜修正比陈旧修正更有预测力",
            },
            {
                "name": "新鲜度 × 修正幅度（复杂经济学模板）",
                "expression": "add(multiply(0.7, rank(ts_delta(analyst_revision, 5))), multiply(0.3, rank(days_from_last_change(analyst_revision))))",
                "description": "修正幅度（70%）× 新鲜度（30%）",
                "economic_logic": "新鲜且幅度大的修正，预测力最强",
            },
            {
                "name": "新鲜度门控（复杂经济学模板）",
                "expression": "trade_when(less(days_from_last_change(analyst_revision), 10), rank(ts_delta(analyst_revision, 5)), 0)",
                "description": "10 天内的修正才交易",
                "economic_logic": "陈旧修正不交易，避免信息衰减",
            },
        ],
    },
    
    # ========== P0-3: 尾部风险机制 ==========
    "tail_risk": {
        "mechanism_id": "tail_risk",
        "priority": "P0",
        "category": "analyst",
        "economic_meaning": "分析师修正的峰度反映极端波动风险，高峰度股票未来收益低",
        "citation": "Harvey & Siddique (2000) - Conditional Skewness in Asset Pricing Tests",
        "expected_sharpe": (1.2, 2.0),
        "operators": ["ts_kurtosis", "ts_delta", "rank", "trade_when", "less", "add", "multiply"],
        "templates": [
            {
                "name": "纯尾部风险",
                "expression": "rank(ts_kurtosis(analyst_revision, 20))",
                "description": "修正峰度越高，尾部风险越大",
                "economic_logic": "高峰度股票未来收益低",
            },
            {
                "name": "尾部风险 × 修正方向（复杂经济学模板）",
                "expression": "add(multiply(0.6, rank(ts_delta(analyst_revision, 5))), multiply(-0.4, rank(ts_kurtosis(analyst_revision, 20))))",
                "description": "修正方向（正权重）× 尾部风险（负权重）",
                "economic_logic": "修正方向明确但峰度低的股票，未来收益更高",
            },
            {
                "name": "尾部风险门控（复杂经济学模板）",
                "expression": "trade_when(less(ts_kurtosis(analyst_revision, 20), 3), rank(ts_delta(analyst_revision, 5)), 0)",
                "description": "峰度 < 3 时才交易",
                "economic_logic": "高峰度不交易，避免极端风险",
            },
        ],
    },
    
    # ========== P1-1: 行业离散度机制 ==========
    "industry_dispersion": {
        "mechanism_id": "industry_dispersion",
        "priority": "P1",
        "category": "model",
        "economic_meaning": "行业内部分化程度反映行业轮动机会，高离散度行业未来收益高",
        "citation": "Moskowitz & Grinblatt (1999) - Do Industries Explain Momentum?",
        "expected_sharpe": (1.0, 1.8),
        "operators": ["group_std_dev", "group_mean", "subtract", "rank", "trade_when", "greater", "add", "multiply"],
        "templates": [
            {
                "name": "纯行业离散度",
                "expression": "rank(group_std_dev(returns, industry))",
                "description": "行业离散度越高，轮动机会越大",
                "economic_logic": "高离散度行业未来收益高",
            },
            {
                "name": "行业离散度 × 个股相对强度（复杂经济学模板）",
                "expression": "add(multiply(0.5, rank(subtract(returns, group_mean(returns, industry)))), multiply(0.5, rank(group_std_dev(returns, industry))))",
                "description": "个股相对强度（50%）× 行业离散度（50%）",
                "economic_logic": "行业离散度高且个股相对强度大的股票，未来收益更高",
            },
            {
                "name": "行业离散度门控（复杂经济学模板）",
                "expression": "trade_when(greater(group_std_dev(returns, industry), 0.02), rank(subtract(returns, group_mean(returns, industry))), 0)",
                "description": "离散度 > 2% 时才交易",
                "economic_logic": "低离散度不交易，避免无效信号",
            },
        ],
    },
    
    # ========== P1-2: 量价协同机制 ==========
    "volume_price_coherence": {
        "mechanism_id": "volume_price_coherence",
        "priority": "P1",
        "category": "pv",
        "economic_meaning": "量价协同反映趋势可持续性，价涨量增的股票未来收益高",
        "citation": "Llorente, Michaely, Saar & Wang (2002) - Dynamic Volume-Return Relation",
        "expected_sharpe": (1.2, 2.0),
        "operators": ["ts_covariance", "ts_delta", "rank", "trade_when", "greater", "add", "multiply"],
        "templates": [
            {
                "name": "纯量价协同",
                "expression": "rank(ts_covariance(volume, returns, 20))",
                "description": "量价协方差越大，协同越强",
                "economic_logic": "价涨量增的股票未来收益高",
            },
            {
                "name": "量价协同 × 价格动量（复杂经济学模板）",
                "expression": "add(multiply(0.6, rank(ts_delta(close, 20))), multiply(0.4, rank(ts_covariance(volume, returns, 20))))",
                "description": "价格动量（60%）× 量价协同（40%）",
                "economic_logic": "价格上涨且量价协同的股票，趋势更可持续",
            },
            {
                "name": "量价协同门控（复杂经济学模板）",
                "expression": "trade_when(greater(ts_covariance(volume, returns, 20), 0), rank(ts_delta(close, 20)), 0)",
                "description": "正协同时才交易",
                "economic_logic": "负协同不交易，避免趋势反转",
            },
        ],
    },

    # ========== P0-4: 短期反转机制 ==========
    "short_term_reversal": {
        "mechanism_id": "short_term_reversal",
        "priority": "P0",
        "category": "pv",
        "economic_meaning": "短期（5-20 天）涨幅过大的股票未来收益低，存在反转效应",
        "citation": "Jegadeesh (1990) - Evidence of Predictable Behavior of Security Returns; Lehmann (1990) - Fads, Martingales, and Market Efficiency",
        "expected_sharpe": (1.4, 2.3),
        "operators": ["ts_delta", "ts_returns", "rank", "multiply", "trade_when", "greater", "subtract"],
        "templates": [
            {
                "name": "纯短期反转",
                "expression": "multiply(-1, rank(ts_returns(close, 10)))",
                "description": "10 日收益取负，做多输家做空赢家",
                "economic_logic": "短期涨幅过大的股票未来反转，收益低",
            },
            {
                "name": "反转 × 成交量确认（复杂经济学模板）",
                "expression": "add(multiply(-0.7, rank(ts_returns(close, 10))), multiply(0.3, rank(ts_delta(volume, 10))))",
                "description": "反转信号（70%）× 成交量放大（30%）",
                "economic_logic": "放量上涨后的反转更强烈",
            },
            {
                "name": "反转门控（复杂经济学模板）",
                "expression": "trade_when(greater(ts_returns(close, 10), 0.05), multiply(-1, rank(ts_returns(close, 10))), 0)",
                "description": "10 日涨幅 > 5% 才做反转",
                "economic_logic": "小幅波动不交易，只在过度反应时做反转",
            },
        ],
    },

    # ========== P0-5: 低波动异象机制 ==========
    "low_volatility_anomaly": {
        "mechanism_id": "low_volatility_anomaly",
        "priority": "P0",
        "category": "pv",
        "economic_meaning": "低波动股票的风险调整后收益高于高波动股票，违背 CAPM 预测",
        "citation": "Baker, Bradley & Wurgler (2011) - Benchmarks as Limits to Arbitrage: Understanding the Low-Volatility Anomaly",
        "expected_sharpe": (1.3, 2.1),
        "operators": ["ts_std_dev", "ts_returns", "rank", "multiply", "trade_when", "less", "divide"],
        "templates": [
            {
                "name": "纯低波动",
                "expression": "multiply(-1, rank(ts_std_dev(returns, 20)))",
                "description": "20 日波动率取负，做多低波动股票",
                "economic_logic": "低波动股票风险调整后收益更高",
            },
            {
                "name": "低波动 × 质量（复杂经济学模板）",
                "expression": "add(multiply(-0.6, rank(ts_std_dev(returns, 20))), multiply(0.4, rank(fundamental_field)))",
                "description": "低波动（60%）× 基本面质量（40%）",
                "economic_logic": "低波动且质量高的股票，收益更稳定",
            },
            {
                "name": "波动率门控（复杂经济学模板）",
                "expression": "trade_when(less(ts_std_dev(returns, 20), 0.02), rank(ts_returns(close, 60)), 0)",
                "description": "波动率 < 2% 才做中期动量",
                "economic_logic": "高波动时不交易，避免噪声",
            },
        ],
    },

    # ========== P1-3: 质量因子机制 ==========
    "quality_factor": {
        "mechanism_id": "quality_factor",
        "priority": "P1",
        "category": "fundamental",
        "economic_meaning": "高盈利能力（ROE/毛利率）股票未来收益高，质量溢价长期存在",
        "citation": "Novy-Marx (2013) - The Other Side of Value: The Gross Profitability Premium; Fama & French (2015) - A Five-Factor Asset Pricing Model",
        "expected_sharpe": (1.1, 1.9),
        "operators": ["rank", "divide", "add", "multiply", "trade_when", "greater", "group_zscore"],
        "templates": [
            {
                "name": "纯质量（盈利能力）",
                "expression": "rank(fundamental_field)",
                "description": "盈利能力指标（ROE/毛利率）排名",
                "economic_logic": "高盈利股票未来收益高",
            },
            {
                "name": "质量 × 价值（复杂经济学模板，QMJ）",
                "expression": "add(multiply(0.5, rank(fundamental_field)), multiply(0.5, rank(value_field)))",
                "description": "质量（50%）× 价值（50%），Quality Minus Junk",
                "economic_logic": "高质量且低估值的股票，收益最高",
            },
            {
                "name": "质量行业内中性化（复杂经济学模板）",
                "expression": "rank(group_zscore(fundamental_field, industry))",
                "description": "行业内质量 z-score，剔除行业效应",
                "economic_logic": "行业内相对质量高的股票，收益更纯粹",
            },
        ],
    },

    # ========== P1-4: 流动性溢价机制 ==========
    "liquidity_premium": {
        "mechanism_id": "liquidity_premium",
        "priority": "P1",
        "category": "pv",
        "economic_meaning": "低流动性股票需要更高收益补偿流动性风险，存在流动性溢价",
        "citation": "Amihud (2002) - Illiquidity and Stock Returns: Cross-Section and Time-Series Effects",
        "expected_sharpe": (1.0, 1.8),
        "operators": ["divide", "ts_mean", "rank", "multiply", "trade_when", "greater", "abs"],
        "templates": [
            {
                "name": "纯非流动性（Amihud）",
                "expression": "rank(ts_mean(divide(abs(returns), volume), 20))",
                "description": "Amihud 非流动性指标：|收益|/成交量 的 20 日均值",
                "economic_logic": "非流动性高的股票，未来收益高（流动性溢价）",
            },
            {
                "name": "流动性 × 反转（复杂经济学模板）",
                "expression": "add(multiply(0.5, rank(ts_mean(divide(abs(returns), volume), 20))), multiply(-0.5, rank(ts_returns(close, 10))))",
                "description": "非流动性（50%）× 短期反转（50%）",
                "economic_logic": "低流动性股票的反转效应更强",
            },
            {
                "name": "流动性门控（复杂经济学模板）",
                "expression": "trade_when(greater(ts_mean(volume, 20), 1000000), rank(ts_returns(close, 60)), 0)",
                "description": "成交量 > 100 万才做动量",
                "economic_logic": "低流动性股票不做动量，避免冲击成本",
            },
        ],
    },
}


# ============================================================================
# ts_backfill 替代方案模板库
# ============================================================================

BACKFILL_ALTERNATIVE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    
    "group_backfill": {
        "operator": "group_backfill",
        "economic_advantage": "用同行业股票的信息回填，比用自身历史回填更有经济学逻辑",
        "economic_logic": "同行业公司的基本面信息更相关，用行业均值回填比用自身历史回填更合理",
        "citation": "Fama & French (1997) - 行业效应",
        "templates": [
            {
                "name": "行业回填",
                "expression": "rank(group_backfill(fundamental_field, industry))",
                "description": "用行业均值回填缺失值",
                "use_case": "基本面字段缺失值处理",
            },
            {
                "name": "行业回填 + 个股偏离",
                "expression": "rank(subtract(fundamental_field, group_backfill(fundamental_field, industry)))",
                "description": "个股相对行业均值的偏离",
                "use_case": "捕捉个股相对行业的异常",
            },
        ],
    },
    
    "ts_mean": {
        "operator": "ts_mean",
        "economic_advantage": "均值比回填更平滑，减少噪声",
        "economic_logic": "基本面信息的均值比单点值更稳定，减少噪声",
        "citation": "Novy-Marx (2013) - 基本面信息扩散缓慢",
        "templates": [
            {
                "name": "时序均值",
                "expression": "rank(ts_mean(fundamental_field, 66))",
                "description": "66 天均值，平滑噪声",
                "use_case": "基本面字段平滑",
            },
            {
                "name": "均值偏离",
                "expression": "rank(subtract(fundamental_field, ts_mean(fundamental_field, 66)))",
                "description": "当前值相对均值的偏离",
                "use_case": "捕捉基本面变化",
            },
        ],
    },
    
    "ts_quantile": {
        "operator": "ts_quantile",
        "economic_advantage": "分位数比回填更稳健，不受极值影响",
        "economic_logic": "基本面信息的中位数比单点值更稳健，不受极值影响",
        "citation": "Fama & French (1992) - 分位数组合",
        "templates": [
            {
                "name": "时序中位数",
                "expression": "rank(ts_quantile(fundamental_field, 66, 0.5))",
                "description": "66 天中位数，稳健估计",
                "use_case": "基本面字段稳健估计",
            },
            {
                "name": "中位数偏离",
                "expression": "rank(subtract(fundamental_field, ts_quantile(fundamental_field, 66, 0.5)))",
                "description": "当前值相对中位数的偏离",
                "use_case": "捕捉基本面异常",
            },
        ],
    },
}


# ============================================================================
# 工具函数
# ============================================================================

def get_mechanism_templates(mechanism_id: str) -> List[Dict[str, Any]]:
    """获取指定机制的模板列表."""
    mechanism = ECONOMIC_MECHANISM_TEMPLATES.get(mechanism_id)
    if mechanism:
        return mechanism.get("templates", [])
    return []


def get_all_p0_templates() -> List[Dict[str, Any]]:
    """获取所有 P0 机制的模板."""
    templates = []
    for mech_id, mech in ECONOMIC_MECHANISM_TEMPLATES.items():
        if mech.get("priority") == "P0":
            templates.extend(mech.get("templates", []))
    return templates


def get_all_p1_templates() -> List[Dict[str, Any]]:
    """获取所有 P1 机制的模板."""
    templates = []
    for mech_id, mech in ECONOMIC_MECHANISM_TEMPLATES.items():
        if mech.get("priority") == "P1":
            templates.extend(mech.get("templates", []))
    return templates


def get_backfill_alternatives() -> List[Dict[str, Any]]:
    """获取所有 ts_backfill 替代方案."""
    alternatives = []
    for alt_id, alt in BACKFILL_ALTERNATIVE_TEMPLATES.items():
        alternatives.extend(alt.get("templates", []))
    return alternatives


def generate_mechanism_prompt(mechanism_id: str) -> str:
    """生成机制的 prompt 文本."""
    mechanism = ECONOMIC_MECHANISM_TEMPLATES.get(mechanism_id)
    if not mechanism:
        return ""
    
    lines = [
        f"## {mechanism['economic_meaning']}",
        f"",
        f"**文献支撑**: {mechanism['citation']}",
        f"**预期 Sharpe**: {mechanism['expected_sharpe'][0]:.1f} - {mechanism['expected_sharpe'][1]:.1f}",
        f"",
        f"**模板示例**:",
    ]
    
    for i, tmpl in enumerate(mechanism.get("templates", []), 1):
        lines.append(f"{i}. {tmpl['name']}")
        lines.append(f"   表达式: `{tmpl['expression']}`")
        lines.append(f"   逻辑: {tmpl['economic_logic']}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    """CLI 入口."""
    import argparse
    import json
    
    ap = argparse.ArgumentParser(description="经济学机制模板库")
    ap.add_argument("--mechanism", help="查询指定机制")
    ap.add_argument("--priority", choices=["P0", "P1"], help="按优先级过滤")
    ap.add_argument("--backfill-alternatives", action="store_true", help="显示 ts_backfill 替代方案")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()
    
    if args.mechanism:
        mechanism = ECONOMIC_MECHANISM_TEMPLATES.get(args.mechanism)
        if args.json:
            print(json.dumps(mechanism, indent=2, ensure_ascii=False))
        else:
            print(generate_mechanism_prompt(args.mechanism))
    
    elif args.backfill_alternatives:
        alternatives = get_backfill_alternatives()
        if args.json:
            print(json.dumps(alternatives, indent=2, ensure_ascii=False))
        else:
            print("\n" + "="*70)
            print("ts_backfill 替代方案")
            print("="*70)
            for i, alt in enumerate(alternatives, 1):
                print(f"\n{i}. {alt['name']}")
                print(f"   表达式: {alt['expression']}")
                print(f"   说明: {alt['description']}")
    
    elif args.priority:
        if args.priority == "P0":
            templates = get_all_p0_templates()
        else:
            templates = get_all_p1_templates()
        
        if args.json:
            print(json.dumps(templates, indent=2, ensure_ascii=False))
        else:
            print(f"\n" + "="*70)
            print(f"{args.priority} 机制模板 ({len(templates)} 个)")
            print("="*70)
            for i, tmpl in enumerate(templates, 1):
                print(f"\n{i}. {tmpl['name']}")
                print(f"   表达式: {tmpl['expression']}")
                print(f"   逻辑: {tmpl['economic_logic']}")
    
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
