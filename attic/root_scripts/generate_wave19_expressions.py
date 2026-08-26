"""
Wave 19 表达式生成 - 使用完全不同的字段组合，降低 SELF_CORRELATION
目标：避免与已有 alpha 的字段组合重复，降低 SELF_CORRELATION
"""
import json
import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore

# Wave 18 失败教训：
# - RR7bJJre (SELF_CORR=0.9941): 权重 0.45/0.35/0.2，字段组合 short_term + event_5d + long_term
# - 1Ywx8ZpR (SELF_CORR=0.5906): 权重 0.4/0.4/0.2，字段组合 short_term + event_5d + long_term
# - 问题：字段组合完全相同，仅权重不同，导致 SELF_CORRELATION 非常高
# - 解决：使用完全不同的字段组合

expressions = [
    # 表达式 1: 2腿组合（short_hedge + event_5d，权重 0.6/0.4）
    # 不使用 short_term 和 long_term，降低 SELF_CORRELATION
    "rank(add(multiply(0.6, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.4, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 2腿组合（short_hedge + long_term，权重 0.5/0.5）
    # 不使用 short_term 和 event_5d，降低 SELF_CORRELATION
    "rank(add(multiply(0.5, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))",
    
    # 表达式 3: 单字段（short_hedge）+ ts_zscore
    # 使用完全不同的字段和预处理方法
    "rank(ts_zscore(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20))",
    
    # 表达式 4: 单字段（event_5d）+ ts_rank
    # 使用完全不同的字段和预处理方法
    "rank(ts_rank(ts_backfill(event_5d_single_quantile_pred, 66), 20))",
    
    # 表达式 5: 2腿组合（short_hedge + event_5d，权重 0.7/0.3）+ group_zscore
    # 不使用 short_term 和 long_term，加入 group_zscore 算子
    "rank(add(multiply(0.7, group_zscore(rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)), subindustry)), multiply(0.3, group_zscore(rank(ts_backfill(event_5d_single_quantile_pred, 66)), subindustry))))",
    
    # 表达式 6: 2腿组合（short_hedge + long_term，权重 0.6/0.4）+ group_mean
    # 不使用 short_term 和 event_5d，加入 group_mean 算子
    "rank(add(multiply(0.6, group_mean(rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)), subindustry)), multiply(0.4, group_mean(rank(ts_backfill(long_term_quantile5_r120_pred, 66)), subindustry))))",
    
    # 表达式 7: 单字段（short_hedge）+ ts_arg_max
    # 使用完全不同的字段和预处理方法
    "rank(ts_arg_max(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20))",
    
    # 表达式 8: 单字段（event_5d）+ ts_arg_min
    # 使用完全不同的字段和预处理方法
    "rank(ts_arg_min(ts_backfill(event_5d_single_quantile_pred, 66), 20))",
]

# 写入数据库
store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')
wave = '19'
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
print(f"[OK] 优化方向: 使用完全不同的字段组合，降低 SELF_CORRELATION")
