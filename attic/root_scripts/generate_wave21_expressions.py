"""
Wave 21 表达式生成 - 使用 2腿组合 + 简单预处理方法
目标：尝试不同的 2腿组合，仅使用 rank(ts_backfill(...)) 预处理方法
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 20 失败教训：
# - 添加额外的预处理方法和算子（ts_zscore, ts_rank 等）反而降低了信号质量
# - Sharpe < 1.58, Fitness < 1.0，远低于阈值
# - 解决：仅使用 rank(ts_backfill(...)) 预处理方法，尝试不同的 2腿组合

expressions = [
    # 表达式 1: 2腿组合（short_term + event_5d，权重 0.5/0.5）
    # 仅使用 rank(ts_backfill(...)) 预处理方法
    "rank(add(multiply(0.5, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.5, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 2腿组合（short_term + event_5d，权重 0.6/0.4）
    # 仅使用 rank(ts_backfill(...)) 预处理方法
    "rank(add(multiply(0.6, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.4, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 3: 2腿组合（short_term + long_term，权重 0.5/0.5）
    # 仅使用 rank(ts_backfill(...)) 预处理方法
    "rank(add(multiply(0.5, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))",
    
    # 表达式 4: 2腿组合（short_term + long_term，权重 0.6/0.4）
    # 仅使用 rank(ts_backfill(...)) 预处理方法
    "rank(add(multiply(0.6, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))",
    
    # 表达式 5: 2腿组合（event_5d + long_term，权重 0.5/0.5）
    # 仅使用 rank(ts_backfill(...)) 预处理方法
    "rank(add(multiply(0.5, rank(ts_backfill(event_5d_single_quantile_pred, 66))), multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))",
    
    # 表达式 6: 2腿组合（event_5d + long_term，权重 0.6/0.4）
    # 仅使用 rank(ts_backfill(...)) 预处理方法
    "rank(add(multiply(0.6, rank(ts_backfill(event_5d_single_quantile_pred, 66))), multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))",
    
    # 表达式 7: 单字段（short_term）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(short_term_price_volume_based_return_5d, 66), subindustry))",
    
    # 表达式 8: 单字段（event_5d）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(event_5d_single_quantile_pred, 66), subindustry))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '21'
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
print(f"[OK] 优化方向: 使用 2腿组合 + 简单预处理方法")
