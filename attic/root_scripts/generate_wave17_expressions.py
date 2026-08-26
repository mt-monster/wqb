import sqlite3
import hashlib

# Wave 17: 基于 Wave 16 失败教训（SELF_CORRELATION FAIL）
# 尝试降低 SELF_CORRELATION，使用不同的字段组合和权重配置

expressions = [
    # 表达式 1: 3腿组合（short_term + event_5d + short_hedge，不使用 long_term）
    "rank(add(multiply(0.4, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)))))",
    
    # 表达式 2: 3腿组合（short_term + event_5d + long_term，降低 long_term 权重）
    "rank(add(multiply(0.4, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.4, rank(ts_backfill(event_5d_single_quantile_pred, 66))), multiply(0.2, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))",
    
    # 表达式 3: 2腿组合（short_term + event_5d，平衡权重）
    "rank(add(multiply(0.5, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.5, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 4: 2腿组合（short_hedge + event_5d，平衡权重）
    "rank(add(multiply(0.5, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.5, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 5: 2腿组合（short_term + short_hedge，平衡权重）+ group_zscore
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.5, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)))), industry))",
    
    # 表达式 6: 单字段（short_term，使用 ts_zscore）
    "rank(ts_zscore(ts_backfill(short_term_price_volume_based_return_5d, 66), 20))",
    
    # 表达式 7: 单字段（event_5d，使用 ts_rank）
    "rank(ts_rank(ts_backfill(event_5d_single_quantile_pred, 66), 20))",
    
    # 表达式 8: 单字段（short_hedge，使用 ts_zscore）
    "rank(ts_zscore(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 17
region = 'USA'
dataset = 'multifactor_return_pred'

# 删除旧的 wave 17 表达式
cursor.execute("DELETE FROM expressions WHERE region=? AND wave=?", (region, str(wave_id)))

# 插入新表达式
for i, expr in enumerate(expressions, 1):
    # 生成 fingerprint
    fingerprint = hashlib.md5(expr.encode()).hexdigest()[:16]
    
    cursor.execute("""
        INSERT INTO expressions (wave_id, region, wave, expression, dataset, fingerprint, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', datetime('now'))
    """, (wave_id, region, str(wave_id), expr, dataset, fingerprint))

conn.commit()

print(f'[OK] 已写入 {len(expressions)} 个表达式到数据库 (wave={wave_id})')
for i, expr in enumerate(expressions, 1):
    print(f'\n{i}. {expr}')

conn.close()
