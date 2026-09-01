# -*- coding: utf-8 -*-
"""operator_economic_analyzer.py - 算子经济学意义分析器.

从经济学角度分析算子的适用场景、经济学含义和组合逻辑.
"""
from __future__ import annotations

from typing import Any, Dict, List


# 算子经济学意义知识库
OPERATOR_ECONOMIC_KB: Dict[str, Dict[str, Any]] = {
    # ========== TS 类（时序算子） ==========
    "ts_backfill": {
        "category": "ts",
        "economic_meaning": "用历史数据填充缺失值，假设信息持续有效",
        "economic_scenario": "低频基本面数据（季度/年度）需要日频化",
        "economic_risk": "过度回填导致信息滞后，信号陈旧",
        "optimal_conditions": "季度财报数据回填 66 天",
        "failure_modes": ["信息衰减", "回填过度导致信号平滑"],
        "citation": "Novy-Marx (2013) - 基本面信息扩散缓慢",
        "alternative_operators": ["group_backfill", "ts_mean", "ts_quantile"],
        "overuse_risk": "高（当前使用 29.9%）",
    },
    "ts_zscore": {
        "category": "ts",
        "economic_meaning": "时序标准化，捕捉异常偏离",
        "economic_scenario": "检测字段相对自身历史的异常波动",
        "economic_risk": "对噪声敏感，可能捕捉无意义波动",
        "optimal_conditions": "高波动字段，窗口 20-60 天",
        "failure_modes": ["均值回归假设失效", "趋势市场中信号反向"],
        "citation": "Jegadeesh & Titman (1993) - 动量与反转",
    },
    "ts_delta": {
        "category": "ts",
        "economic_meaning": "时序差分，捕捉边际变化",
        "economic_scenario": "分析师修正、盈利变化等边际信息",
        "economic_risk": "对短期噪声敏感",
        "optimal_conditions": "事件驱动型字段（修正、公告）",
        "failure_modes": ["噪声主导", "滞后于价格"],
        "citation": "Jegadeesh et al. (2004) - 分析师修正的信息含量",
    },
    "ts_kurtosis": {
        "category": "ts",
        "economic_meaning": "时序峰度，捕捉尾部风险",
        "economic_scenario": "检测收益率分布的肥尾特征，预测极端风险",
        "economic_risk": "小样本峰度估计不稳定",
        "optimal_conditions": "高波动股票，窗口 20-60 天",
        "failure_modes": ["小样本噪声", "峰度与收益关系不稳定"],
        "citation": "Harvey & Siddique (2000) - 条件偏度与峰度",
        "unused_reason": "对数据质量要求高，IND 市场数据可能不足",
    },
    "ts_covariance": {
        "category": "ts",
        "economic_meaning": "时序协方差，捕捉字段间动态关系",
        "economic_scenario": "两个字段的协同变化（如量价关系）",
        "economic_risk": "协方差不等于因果关系",
        "optimal_conditions": "有经济学逻辑支撑的字段对",
        "failure_modes": ["伪相关", "关系不稳定"],
        "citation": "Llorente et al. (2002) - 量价关系",
        "unused_reason": "需要明确的字段对假设，GEM 生成较少",
    },
    "ts_arg_max": {
        "category": "ts",
        "economic_meaning": "时序最大值位置，捕捉拐点",
        "economic_scenario": "检测字段何时达到峰值（动量拐点）",
        "economic_risk": "拐点预测难度大",
        "optimal_conditions": "周期性明显的字段",
        "failure_modes": ["拐点滞后", "假拐点"],
        "citation": "Novy-Marx (2012) - 动量拐点",
        "unused_reason": "经济学含义较复杂，LLM 较少使用",
    },
    "days_from_last_change": {
        "category": "ts",
        "economic_meaning": "距上次变化天数，捕捉事件新鲜度",
        "economic_scenario": "分析师修正、新闻事件后的信息衰减",
        "economic_risk": "事件定义主观",
        "optimal_conditions": "事件驱动型字段",
        "failure_modes": ["事件定义模糊", "衰减速度不一致"],
        "citation": "Tetlock (2007) - 新闻情绪衰减",
        "unused_reason": "需要事件检测逻辑，GEM 模板较少",
    },
    
    # ========== Group 类（分组算子） ==========
    "group_rank": {
        "category": "group",
        "economic_meaning": "组内排名，剔除行业/市值效应",
        "economic_scenario": "行业中性化，捕捉纯粹个股 alpha",
        "economic_risk": "行业定义主观，可能剔除真实信号",
        "optimal_conditions": "行业间差异大的市场",
        "failure_modes": ["行业定义不合理", "过度中性化"],
        "citation": "Fama & French (1997) - 行业效应",
    },
    "group_neutralize": {
        "category": "group",
        "economic_meaning": "组内中性化，回归剔除组效应",
        "economic_scenario": "更严格的行业中性化（回归方法）",
        "economic_risk": "计算复杂，可能过度拟合",
        "optimal_conditions": "需要严格中性化的场景",
        "failure_modes": ["过度拟合", "计算成本高"],
        "citation": "Asness et al. (2019) - 质量减去垃圾",
    },
    "group_mean": {
        "category": "group",
        "economic_meaning": "组内均值，行业基准",
        "economic_scenario": "计算行业平均水平，作为相对比较基准",
        "economic_risk": "均值受极值影响",
        "optimal_conditions": "行业内股票数量充足",
        "failure_modes": ["小行业均值不稳定", "极值影响"],
        "citation": "Fama & French (1997) - 行业组合",
        "unused_reason": "group_rank 更常用，group_mean 被忽视",
    },
    "group_std_dev": {
        "category": "group",
        "economic_meaning": "组内标准差，行业离散度",
        "economic_scenario": "衡量行业内部分化程度，预测行业轮动",
        "economic_risk": "离散度与收益关系不稳定",
        "optimal_conditions": "行业分化明显的时期",
        "failure_modes": ["离散度与收益关系弱", "行业定义影响"],
        "citation": "Moskowitz & Grinblatt (1999) - 行业动量",
        "unused_reason": "经济学含义较间接，LLM 较少使用",
    },
    "group_vector_neut": {
        "category": "group",
        "economic_meaning": "多因子向量中性化，同时剔除多个因子效应",
        "economic_scenario": "剥离价值、动量、规模等多个因子后的纯 alpha",
        "economic_risk": "计算复杂，可能过度中性化",
        "optimal_conditions": "多因子模型框架",
        "failure_modes": ["过度中性化", "计算成本高"],
        "citation": "Fama & French (2015) - 五因子模型",
        "unused_reason": "需要多因子框架，GEM 模板较少",
    },
    
    # ========== Math 类（数学算子） ==========
    "rank": {
        "category": "math",
        "economic_meaning": "截面排名，消除量纲和分布影响",
        "economic_scenario": "将字段转换为 0-1 排名，便于比较",
        "economic_risk": "丢失原始数值信息",
        "optimal_conditions": "几乎所有场景",
        "failure_modes": ["排名后信息丢失", "对极值不敏感"],
        "citation": "Fama & French (1992) - 截面分析",
    },
    "signed_power": {
        "category": "math",
        "economic_meaning": "保留符号的幂变换，非线性调整",
        "economic_scenario": "对字段进行非线性变换（如平方根、平方）",
        "economic_risk": "幂次选择主观",
        "optimal_conditions": "字段分布偏态明显",
        "failure_modes": ["幂次选择不当", "过度变换"],
        "citation": "Harvey & Siddique (2000) - 偏度调整",
    },
    "log": {
        "category": "math",
        "economic_meaning": "对数变换，压缩右尾",
        "economic_scenario": "处理右偏分布（如市值、成交量）",
        "economic_risk": "要求字段为正",
        "optimal_conditions": "右偏分布字段",
        "failure_modes": ["负值无法处理", "零值需加 1"],
        "citation": "Fama & French (1992) - 规模效应",
        "unused_reason": "需要确保字段为正，GEM 较少使用",
    },
    "kth_element": {
        "category": "math",
        "economic_meaning": "第 K 大元素，分位数计算",
        "economic_scenario": "计算字段在组内的分位数位置",
        "economic_risk": "K 值选择主观",
        "optimal_conditions": "需要精确分位数的场景",
        "failure_modes": ["K 值选择不当", "小样本不稳定"],
        "citation": "Fama & French (1992) - 分位数组合",
        "unused_reason": "quantile 更常用，kth_element 被忽视",
    },
    "hump": {
        "category": "math",
        "economic_meaning": "驼峰函数，区间筛选",
        "economic_scenario": "筛选字段在特定区间的股票（如 0.2-0.8）",
        "economic_risk": "区间选择主观",
        "optimal_conditions": "需要排除极端值的场景",
        "failure_modes": ["区间选择不当", "信号丢失"],
        "citation": "Fama & French (1992) - 极端值处理",
        "unused_reason": "经济学含义较复杂，LLM 较少使用",
    },
    
    # ========== Cond 类（条件算子） ==========
    "trade_when": {
        "category": "cond",
        "economic_meaning": "条件交易，满足条件才持有",
        "economic_scenario": "只在信号强烈时交易（如 rank > 0.7）",
        "economic_risk": "条件设置主观，可能错过机会",
        "optimal_conditions": "信号质量参差不齐",
        "failure_modes": ["条件过严错过机会", "条件过松噪声多"],
        "citation": "Jegadeesh & Titman (1993) - 动量组合构建",
    },
    "tail": {
        "category": "cond",
        "economic_meaning": "尾部截取，极端值处理",
        "economic_scenario": "只保留字段的尾部值（如前 5%）",
        "economic_risk": "尾部定义主观",
        "optimal_conditions": "极端值有特殊含义",
        "failure_modes": ["尾部定义不当", "样本量不足"],
        "citation": "Fama & French (1992) - 极端组合",
        "unused_reason": "经济学含义较复杂，LLM 较少使用",
    },
    
    # ========== Vec 类（向量算子） ==========
    "vec_avg": {
        "category": "vec",
        "economic_meaning": "向量平均，多值字段聚合",
        "economic_scenario": "将 VECTOR 字段（如多个分析师预测）聚合为单值",
        "economic_risk": "平均可能掩盖分歧",
        "optimal_conditions": "VECTOR 字段必须聚合",
        "failure_modes": ["平均掩盖分歧", "权重不合理"],
        "citation": "Jegadeesh et al. (2004) - 分析师一致预期",
    },
    "vec_stddev": {
        "category": "vec",
        "economic_meaning": "向量标准差，多值字段离散度",
        "economic_scenario": "衡量 VECTOR 字段的内部分歧（如分析师预测分歧）",
        "economic_risk": "小样本离散度不稳定",
        "optimal_conditions": "VECTOR 字段，样本量充足",
        "failure_modes": ["小样本不稳定", "离散度与收益关系弱"],
        "citation": "Diether et al. (2002) - 分析师分歧",
        "unused_reason": "需要 VECTOR 字段，GEM 较少使用",
    },
}


def analyze_operator_economics(operator: str) -> Dict[str, Any]:
    """分析算子的经济学意义."""
    return OPERATOR_ECONOMIC_KB.get(operator, {
        "category": "unknown",
        "economic_meaning": "未知",
        "economic_scenario": "未知",
        "economic_risk": "未知",
    })


def get_unused_operators_with_economics(unused_ops: List[str]) -> List[Dict[str, Any]]:
    """获取未使用算子的经济学分析."""
    result = []
    for op in unused_ops:
        econ = analyze_operator_economics(op)
        result.append({
            "operator": op,
            **econ
        })
    return result


def generate_economic_recommendations(
    unused_ops: List[str],
    overused_ops: List[str],
    dataset_category: str
) -> List[Dict[str, Any]]:
    """基于经济学意义生成优化建议."""
    recommendations = []
    
    # 分析未使用算子的经济学价值
    for op in unused_ops:
        econ = analyze_operator_economics(op)
        
        # 判断是否与数据集类别匹配
        if econ.get("category") == "ts" and dataset_category in ["analyst", "fundamental"]:
            recommendations.append({
                "operator": op,
                "priority": "P0",
                "reason": f"{op} 适用于 {dataset_category} 数据集，经济学含义：{econ['economic_meaning']}",
                "economic_scenario": econ["economic_scenario"],
                "citation": econ.get("citation", ""),
                "template": generate_economic_template(op, dataset_category),
            })
        elif econ.get("category") == "group" and dataset_category in ["model", "fundamental"]:
            recommendations.append({
                "operator": op,
                "priority": "P1",
                "reason": f"{op} 适用于 {dataset_category} 数据集，经济学含义：{econ['economic_meaning']}",
                "economic_scenario": econ["economic_scenario"],
                "citation": econ.get("citation", ""),
                "template": generate_economic_template(op, dataset_category),
            })
    
    # 分析过度使用算子的替代方案
    for op in overused_ops:
        econ = analyze_operator_economics(op)
        if "alternative_operators" in econ:
            recommendations.append({
                "operator": op,
                "priority": "P0",
                "reason": f"{op} 过度使用（{econ.get('overuse_risk', '高')}），建议替换为 {econ['alternative_operators']}",
                "economic_risk": econ["economic_risk"],
                "alternatives": econ["alternative_operators"],
            })
    
    return recommendations


def generate_economic_template(operator: str, dataset_category: str) -> str:
    """基于经济学意义生成表达式模板."""
    templates = {
        "ts_kurtosis": {
            "analyst": "rank(ts_kurtosis(analyst_revision, 20))",
            "fundamental": "rank(ts_kurtosis(earnings_change, 60))",
            "description": "捕捉分析师修正/盈利变化的尾部风险",
        },
        "ts_covariance": {
            "pv": "rank(ts_covariance(volume, returns, 20))",
            "description": "捕捉量价协同关系",
        },
        "days_from_last_change": {
            "analyst": "rank(days_from_last_change(analyst_revision))",
            "news": "rank(days_from_last_change(news_sentiment))",
            "description": "捕捉事件新鲜度（信息衰减）",
        },
        "group_mean": {
            "model": "rank(subtract(field, group_mean(field, industry)))",
            "fundamental": "rank(subtract(field, group_mean(field, industry)))",
            "description": "行业中性化（剔除行业均值）",
        },
        "group_std_dev": {
            "model": "rank(divide(field, group_std_dev(field, industry)))",
            "description": "行业离散度调整",
        },
        "log": {
            "pv": "rank(log(add(volume, 1)))",
            "description": "成交量对数变换（压缩右尾）",
        },
        "vec_stddev": {
            "analyst": "rank(vec_stddev(analyst_estimates))",
            "description": "分析师预测分歧",
        },
    }
    
    tmpl = templates.get(operator, {}).get(dataset_category)
    if tmpl:
        return tmpl
    
    return f"rank({operator}(field, ...))  # 需根据经济学含义调整"


def main():
    """CLI 入口."""
    import argparse
    import json
    
    ap = argparse.ArgumentParser(description="算子经济学意义分析器")
    ap.add_argument("--operator", help="分析特定算子")
    ap.add_argument("--unused", nargs="+", help="未使用算子列表")
    ap.add_argument("--overused", nargs="+", help="过度使用算子列表")
    ap.add_argument("--dataset-category", default="analyst", help="数据集类别")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()
    
    if args.operator:
        # 分析单个算子
        econ = analyze_operator_economics(args.operator)
        if args.json:
            print(json.dumps(econ, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*70}")
            print(f"算子经济学分析： {args.operator}")
            print(f"{'='*70}")
            for key, value in econ.items():
                print(f"{key:20s}: {value}")
    
    elif args.unused:
        # 分析未使用算子
        recommendations = generate_economic_recommendations(
            args.unused, args.overused or [], args.dataset_category
        )
        
        if args.json:
            print(json.dumps(recommendations, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*70}")
            print(f"未使用算子的经济学优化建议 ({args.dataset_category})")
            print(f"{'='*70}")
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['operator']} ({rec['priority']})")
                print(f"   原因： {rec['reason']}")
                if "economic_scenario" in rec:
                    print(f"   场景： {rec['economic_scenario']}")
                if "citation" in rec:
                    print(f"   文献： {rec['citation']}")
                if "template" in rec:
                    print(f"   模板： {rec['template']}")
    
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
