"""
Wave 22 表达式生成 - 使用不同的字段组合（避免 SELF_CORRELATION）
目标：使用 short_hedge 和 long_term_r60，避免使用 short_term, event_5d, long_term
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 21 失败教训：
# - 所有 4 个 Fitness >= 1.0 的候选都因为 SELF_CORRELATION 过高而被 BLOCK
# - 这些候选使用了相同的字段组合（short_term + event_5d 或 short_term + long_term），仅权重不同
# - 即使使用 2腿组合，如果字段组合与已有 alpha 相似，SELF_CORRELATION 仍然会很高
# - 解决：使用不同的字段组合，避免使用 short_term, event_5d, long_term

expressions = [
    # 表达式 1: 2腿组合（short_hedge + long_term_r60，权重 0.5/0.5）
    # 使用不同的字段组合
    "rank(add(multiply(0.5, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.5, rank(ts_backfill(long_term_quantile5_r60_pred, 66)))))",
    
    # 表达式 2: 2腿组合（short_hedge + long_term_r60，权重 0.6/0.4）
    # 使用不同的字段组合
    "rank(add(multiply(0.6, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.4, rank(ts_backfill(long_term_quantile5_r60_pred, 66)))))",
    
    # 表达式 3: 2腿组合（short_hedge + long_term_r60，权重 0.4/0.6）
    # 使用不同的字段组合
    "rank(add(multiply(0.4, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.6, rank(ts_backfill(long_term_quantile5_r60_pred, 66)))))",
    
    # 表达式 4: 2腿组合（short_hedge + long_term_r60，权重 0.7/0.3）
    # 使用不同的字段组合
    "rank(add(multiply(0.7, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.3, rank(ts_backfill(long_term_quantile5_r60_pred, 66)))))",
    
    # 表达式 5: 2腿组合（short_hedge + long_term_r60，权重 0.3/0.7）
    # 使用不同的字段组合
    "rank(add(multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.7, rank(ts_backfill(long_term_quantile5_r60_pred, 66)))))",
    
    # 表达式 6: 单字段（short_hedge）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(short_hedge_quantile5_r60_pred, 66), subindustry))",
    
    # 表达式 7: 单字段（long_term_r60）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(ts_backfill(long_term_quantile5_r60_pred, 66), subindustry))",
    
    # 表达式 8: 2腿组合（short_hedge + long_term_r60，权重 0.5/0.5）+ group_zscore
    # 使用 group_zscore 算子，满足多样性闸门
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.5, rank(ts_backfill(long_term_quantile5_r60_pred, 66)))), subindustry))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '22'
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
print(f"[OK] 优化方向: 使用不同的字段组合（short_hedge, long_term_r60）")
