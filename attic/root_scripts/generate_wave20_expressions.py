"""
Wave 20 表达式生成 - 使用已验证字段组合 + 不同预处理方法/算子
目标：继续使用 short_term + event_5d + long_term 字段组合（已验证有效），但尝试不同的预处理方法和算子
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 19 失败教训：
# - 使用完全不同的字段组合（short_hedge + event_5d 或 short_hedge + long_term）导致信号质量下降
# - Sharpe < 1.0, Fitness < 0.5，远低于阈值
# - 解决：继续使用已验证的字段组合（short_term + event_5d + long_term），但尝试不同的预处理方法和算子

expressions = [
    # 表达式 1: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ ts_zscore
    # 使用已验证的字段组合和权重，加入 ts_zscore 预处理方法
    "rank(add(multiply(0.4, ts_zscore(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), 20)), multiply(0.4, ts_zscore(rank(ts_backfill(event_5d_single_quantile_pred, 66)), 20)), multiply(0.2, ts_zscore(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), 20))))",
    
    # 表达式 2: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ ts_rank
    # 使用已验证的字段组合和权重，加入 ts_rank 预处理方法
    "rank(add(multiply(0.4, ts_rank(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), 20)), multiply(0.4, ts_rank(rank(ts_backfill(event_5d_single_quantile_pred, 66)), 20)), multiply(0.2, ts_rank(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), 20))))",
    
    # 表达式 3: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ group_zscore
    # 使用已验证的字段组合和权重，加入 group_zscore 算子
    "rank(add(multiply(0.4, group_zscore(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), subindustry)), multiply(0.4, group_zscore(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry)), multiply(0.2, group_zscore(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
    
    # 表达式 4: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ ts_arg_max
    # 使用已验证的字段组合和权重，加入 ts_arg_max 算子
    "rank(add(multiply(0.4, rank(ts_arg_max(ts_backfill(short_term_price_volume_based_return_5d, 66), 20))), multiply(0.4, rank(ts_arg_max(ts_backfill(event_5d_single_quantile_pred, 66), 20))), multiply(0.2, rank(ts_arg_max(ts_backfill(long_term_quantile5_r120_pred, 66), 20)))))",
    
    # 表达式 5: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ ts_arg_min
    # 使用已验证的字段组合和权重，加入 ts_arg_min 算子
    "rank(add(multiply(0.4, rank(ts_arg_min(ts_backfill(short_term_price_volume_based_return_5d, 66), 20))), multiply(0.4, rank(ts_arg_min(ts_backfill(event_5d_single_quantile_pred, 66), 20))), multiply(0.2, rank(ts_arg_min(ts_backfill(long_term_quantile5_r120_pred, 66), 20)))))",
    
    # 表达式 6: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ ts_av_diff
    # 使用已验证的字段组合和权重，加入 ts_av_diff 算子
    "rank(add(multiply(0.4, rank(ts_av_diff(ts_backfill(short_term_price_volume_based_return_5d, 66), 5))), multiply(0.4, rank(ts_av_diff(ts_backfill(event_5d_single_quantile_pred, 66), 5))), multiply(0.2, rank(ts_av_diff(ts_backfill(long_term_quantile5_r120_pred, 66), 5)))))",
    
    # 表达式 7: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ ts_delta
    # 使用已验证的字段组合和权重，加入 ts_delta 算子
    "rank(add(multiply(0.4, rank(ts_delta(ts_backfill(short_term_price_volume_based_return_5d, 66), 3))), multiply(0.4, rank(ts_delta(ts_backfill(event_5d_single_quantile_pred, 66), 3))), multiply(0.2, rank(ts_delta(ts_backfill(long_term_quantile5_r120_pred, 66), 3)))))",
    
    # 表达式 8: 3腿组合（short_term + event_5d + long_term，权重 0.4/0.4/0.2）+ group_std_dev
    # 使用已验证的字段组合和权重，加入 group_std_dev 算子
    "rank(add(multiply(0.4, group_std_dev(rank(ts_backfill(short_term_price_volume_based_return_5d, 66)), subindustry)), multiply(0.4, group_std_dev(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry)), multiply(0.2, group_std_dev(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '20'
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
print(f"[OK] 优化方向: 使用已验证字段组合 + 不同预处理方法/算子")
