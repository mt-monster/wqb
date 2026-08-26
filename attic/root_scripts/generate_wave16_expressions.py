import sqlite3
import hashlib

# Wave 16: 基于 Wave 14 成功配方（multifactor_return_pred）
# 使用 3腿组合，平衡权重（0.4/0.3/0.3）
# 尝试不同的字段组合，提高多样性

expressions = [
    # 表达式 1: 3腿组合（long_term + short_term + event_5d）- Wave 14 成功配方
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 3腿组合（long_term + short_hedge + event_5d）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 3: 3腿组合（long_term + short_term + short_hedge）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)))))",
    
    # 表达式 4: 3腿组合（long_term + short_hedge + event_5d，不同权重）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 5: 3腿组合（long_term + short_term + event_5d，不同权重）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 6: 2腿组合（long_term + short_term，平衡权重）+ group_zscore
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.5, rank(ts_backfill(short_term_price_volume_based_return_5d, 66)))), industry))",
    
    # 表达式 7: 2腿组合（long_term + event_5d，平衡权重）+ group_zscore
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.5, rank(ts_backfill(event_5d_single_quantile_pred, 66)))), industry))",
    
    # 表达式 8: 单字段（long_term，使用 ts_arg_max 平滑）
    "rank(ts_arg_max(ts_backfill(long_term_quantile5_r120_pred, 66), 10))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 16
region = 'USA'
dataset = 'multifactor_return_pred'

# 删除旧的 wave 16 表达式
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
