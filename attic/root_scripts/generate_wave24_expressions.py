"""
Wave 24 表达式生成 - 使用 pv_tech_indicators 数据集
目标：使用技术指标相关的字段，避免 multifactor_return_pred 数据集的 SELF_CORRELATION 问题
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 21-23 失败教训：
# - multifactor_return_pred 数据集的 SELF_CORRELATION 问题难以解决
# - 已验证的字段组合信号质量好，但 SELF_CORRELATION 过高（0.77-0.97）
# - 不同的字段组合信号质量差，无法通过硬闸（Sharpe < 1.58, Fitness < 1.0）
# - analyst_consensus 数据集的 MATRIX 字段信号质量非常差
# - 解决：尝试 pv_tech_indicators 数据集，使用技术指标相关的字段

expressions = [
    # 表达式 1: 单字段（momentum_shift_indicator）+ rank
    # 使用动量转换指标（MATRIX 字段）
    "rank(ts_backfill(momentum_shift_indicator, 66))",
    
    # 表达式 2: 单字段（price_reversal_signal）+ rank
    # 使用价格反转信号（MATRIX 字段）
    "rank(ts_backfill(price_reversal_signal, 66))",
    
    # 表达式 3: 2腿组合（momentum_shift_indicator + price_acceleration_factor，权重 0.5/0.5）
    # 使用动量转换指标和价格加速因子（MATRIX 字段）
    "rank(add(multiply(0.5, rank(ts_backfill(momentum_shift_indicator, 66))), multiply(0.5, rank(ts_backfill(price_acceleration_factor, 66)))))",
    
    # 表达式 4: 2腿组合（momentum_shift_indicator + volume_spike_score，权重 0.6/0.4）
    # 使用动量转换指标和成交量突增分数（MATRIX 字段）
    "rank(add(multiply(0.6, rank(ts_backfill(momentum_shift_indicator, 66))), multiply(0.4, rank(ts_backfill(volume_spike_score, 66)))))",
    
    # 表达式 5: 单字段（momentum_shift_indicator）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(momentum_shift_indicator, 66), subindustry))",
    
    # 表达式 6: 单字段（price_reversal_signal）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(price_reversal_signal, 66), subindustry))",
    
    # 表达式 7: 2腿组合（momentum_shift_indicator + price_acceleration_factor，权重 0.5/0.5）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(momentum_shift_indicator, 66))), multiply(0.5, rank(ts_backfill(price_acceleration_factor, 66)))), subindustry))",
    
    # 表达式 8: 单字段（price_trend_score）+ rank
    # 使用价格趋势分数（MATRIX 字段）
    "rank(ts_backfill(price_trend_score, 66))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '24'
region = 'USA'

# 使用 upsert_expressions 批量写入
result = store.upsert_expressions(
    region=region,
    wave=wave,
    items=expressions,
    dataset='pv_tech_indicators',
    status='pending'
)
print(f"[OK] 批量写入完成: {result}")

print(f"\n[OK] Wave {wave} 共生成 {len(expressions)} 个表达式")
print(f"[OK] 区域: {region}")
print(f"[OK] 数据集: pv_tech_indicators")
print(f"[OK] 优化方向: 使用技术指标相关的字段（momentum, price, volume）")
