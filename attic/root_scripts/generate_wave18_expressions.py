"""
Wave 18 表达式生成 - 基于 Wave 17 成功配方（1Ywx8ZpR）
目标：继续挖掘更多候选，尝试不同的字段组合和权重配置
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 17 成功配方分析：
# 1Ywx8ZpR: rank(add(multiply(0.4, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), 
#                     multiply(0.4, rank(ts_backfill(event_5d_single_quantile_pred, 66))), 
#                     multiply(0.2, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))
# - SELF_CORRELATION: 0.5906 < 0.7 (PASS)
# - Platform Submit OK: True
# - 成功原因：降低 long_term 权重（0.2），增加 short_term 和 event_5d 权重（0.4/0.4）

expressions = [
    # 表达式 1: 3腿组合（short_term + event_5d + long_term，权重 0.35/0.45/0.20）+ group_zscore
    # 基于 1Ywx8ZpR 微调权重，加入 group_zscore 算子
    "rank(add(multiply(0.35, group_zscore(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), subindustry)), multiply(0.45, group_zscore(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry)), multiply(0.20, group_zscore(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
    
    # 表达式 2: 3腿组合（short_term + event_5d + long_term，权重 0.45/0.35/0.20）+ group_zscore
    # 基于 1Ywx8ZpR 微调权重，加入 group_zscore 算子
    "rank(add(multiply(0.45, group_zscore(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), subindustry)), multiply(0.35, group_zscore(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry)), multiply(0.20, group_zscore(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
    
    # 表达式 3: 3腿组合（short_term + event_5d + short_hedge，权重 0.35/0.35/0.30）+ group_mean
    # 不使用 long_term，降低 SELF_CORRELATION，加入 group_mean 算子
    "rank(add(multiply(0.35, group_mean(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), subindustry)), multiply(0.35, group_mean(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry)), multiply(0.30, group_mean(rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)), subindustry))))",
    
    # 表达式 4: 3腿组合（short_term + event_5d + short_hedge，权重 0.40/0.30/0.30）+ group_mean
    # 不使用 long_term，降低 SELF_CORRELATION，加入 group_mean 算子
    "rank(add(multiply(0.40, group_mean(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), subindustry)), multiply(0.30, group_mean(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry)), multiply(0.30, group_mean(rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)), subindustry))))",
    
    # 表达式 5: 2腿组合（short_term + event_5d，权重 0.50/0.50）+ ts_arg_max
    # 简化策略，降低复杂度，加入 ts_arg_max 算子
    "rank(add(multiply(0.50, rank(ts_arg_max(ts_backfill(short_term_price_volume_based_return_5d, 66), 20))), multiply(0.50, rank(ts_arg_max(ts_backfill(event_5d_single_quantile_pred, 66), 20)))))",
    
    # 表达式 6: 2腿组合（short_term + event_5d，权重 0.60/0.40）+ ts_arg_min
    # 简化策略，降低复杂度，加入 ts_arg_min 算子
    "rank(add(multiply(0.60, rank(ts_arg_min(ts_backfill(short_term_price_volume_based_return_5d, 66), 20))), multiply(0.40, rank(ts_arg_min(ts_backfill(event_5d_single_quantile_pred, 66), 20)))))",
    
    # 表达式 7: 3腿组合（short_term + event_5d + long_term，使用 ts_zscore）+ group_std_dev
    # 尝试不同的预处理方法，加入 group_std_dev 算子
    "rank(add(multiply(0.40, ts_zscore(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), 20)), multiply(0.40, ts_zscore(rank(ts_backfill(event_5d_single_quantile_pred, 66)), 20)), multiply(0.20, group_std_dev(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
    
    # 表达式 8: 3腿组合（short_term + event_5d + long_term，使用 ts_rank）+ group_sum
    # 尝试不同的预处理方法，加入 group_sum 算子
    "rank(add(multiply(0.40, ts_rank(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), 20)), multiply(0.40, ts_rank(rank(ts_backfill(event_5d_single_quantile_pred, 66)), 20)), multiply(0.20, group_sum(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '18'
region = 'USA'

# 使用 upsert_expressions 批量写入
result = store.upsert_expressions(
    region=region,
    wave=wave,
    items=expressions,
    dataset='multifactor_return_pred',
    status='pending'
)
print(f"[OK] 批量写入完成: {result}")

print(f"\n[OK] Wave {wave} 共生成 {len(expressions)} 个表达式")
print(f"[OK] 区域: {region}")
print(f"[OK] 数据集: multifactor_return_pred")
print(f"[OK] 基础配方: Wave 17 成功配方（1Ywx8ZpR）")
print(f"[OK] 优化方向: 微调权重、尝试不同字段组合、尝试不同预处理方法")
