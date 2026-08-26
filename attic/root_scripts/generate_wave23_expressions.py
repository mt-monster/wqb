"""
Wave 23 表达式生成 - 使用 analyst_consensus 数据集（MATRIX 字段）
目标：使用分析师预期相关的 MATRIX 字段，避免 VECTOR 字段的 vec_* 聚合要求
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 21-22 失败教训：
# - multifactor_return_pred 数据集的 SELF_CORRELATION 问题难以解决
# - 已验证的字段组合信号质量好，但 SELF_CORRELATION 过高（0.77-0.97）
# - 不同的字段组合信号质量差，无法通过硬闸（Sharpe < 1.58, Fitness < 1.0）
# - 解决：尝试其他数据集（analyst_consensus），使用分析师预期相关的 MATRIX 字段
# - 注意：VECTOR 字段必须经 vec_* 聚合，MATRIX 字段不需要

expressions = [
    # 表达式 1: 单字段（mean_estimate_eps_longterm）+ rank
    # 使用分析师预期 EPS 长期数据（MATRIX 字段）
    "rank(ts_backfill(mean_estimate_eps_longterm, 66))",
    
    # 表达式 2: 单字段（mean_estimate_targetprice_annual12_tribes）+ rank
    # 使用分析师预期目标价年度数据（MATRIX 字段）
    "rank(ts_backfill(mean_estimate_targetprice_annual12_tribes, 66))",
    
    # 表达式 3: 2腿组合（mean_estimate_eps_longterm + mean_estimate_targetprice_annual12_tribes，权重 0.5/0.5）
    # 使用分析师预期 EPS 长期数据和目标价年度数据（MATRIX 字段）
    "rank(add(multiply(0.5, rank(ts_backfill(mean_estimate_eps_longterm, 66))), multiply(0.5, rank(ts_backfill(mean_estimate_targetprice_annual12_tribes, 66)))))",
    
    # 表达式 4: 2腿组合（mean_estimate_eps_longterm + mean_estimate_targetprice_annual12_tribes，权重 0.6/0.4）
    # 使用分析师预期 EPS 长期数据和目标价年度数据（MATRIX 字段）
    "rank(add(multiply(0.6, rank(ts_backfill(mean_estimate_eps_longterm, 66))), multiply(0.4, rank(ts_backfill(mean_estimate_targetprice_annual12_tribes, 66)))))",
    
    # 表达式 5: 单字段（mean_estimate_eps_longterm）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(mean_estimate_eps_longterm, 66), subindustry))",
    
    # 表达式 6: 单字段（mean_estimate_targetprice_annual12_tribes）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(mean_estimate_targetprice_annual12_tribes, 66), subindustry))",
    
    # 表达式 7: 2腿组合（mean_estimate_eps_longterm + mean_estimate_targetprice_annual12_tribes，权重 0.5/0.5）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(mean_estimate_eps_longterm, 66))), multiply(0.5, rank(ts_backfill(mean_estimate_targetprice_annual12_tribes, 66)))), subindustry))",
    
    # 表达式 8: 单字段（stddev_estimate_eps_longterm）+ rank
    # 使用分析师预期 EPS 标准差长期数据（MATRIX 字段）
    "rank(ts_backfill(stddev_estimate_eps_longterm, 66))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '23'
region = 'USA'

# 使用 upsert_expressions 批量写入
result = store.upsert_expressions(
    region=region,
    wave=wave,
    items=expressions,
    dataset='analyst_consensus',
    status='pending'
)
print(f"[OK] 批量写入完成: {result}")

print(f"\n[OK] Wave {wave} 共生成 {len(expressions)} 个表达式")
print(f"[OK] 区域: {region}")
print(f"[OK] 数据集: analyst_consensus")
print(f"[OK] 优化方向: 使用分析师预期相关的 MATRIX 字段（mean_estimate_eps_longterm, mean_estimate_targetprice_annual12_tribes）")
