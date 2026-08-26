import sqlite3
import hashlib

# 基于 MEA 成功案例的骨架模式生成表达式
# 骨架: rank(field1/field1_lag-1) + rank(field2/field2_lag-1)
# 关键特征: 使用 ratio 变化率，Turnover 非常低

# 在 multifactor_return_pred 数据集中，我们可以使用：
# - long_term_60d_quantile5_pred / long_term_60d_quantile5_pred_3mth_ago - 1
# - short_hedge_quantile5_r60_pred / short_hedge_quantile5_r60_pred_3mth_ago - 1

# 但是 multifactor_return_pred 数据集没有 3mth_ago 字段
# 我们可以使用 ts_delta 或 ts_backfill 来模拟变化率

expressions = [
    # 表达式 1: 使用 ts_delta 模拟变化率（2 腿组合）
    "rank(add(rank(ts_delta(ts_backfill(long_term_60d_quantile5_pred, 66), 60)), rank(ts_delta(ts_backfill(short_hedge_quantile5_r60_pred, 66), 60))))",
    
    # 表达式 2: 使用 ts_delta 模拟变化率（3 腿组合）
    "rank(add(rank(ts_delta(ts_backfill(long_term_60d_quantile5_pred, 66), 60)), rank(ts_delta(ts_backfill(short_hedge_quantile5_r60_pred, 66), 60)), rank(ts_delta(ts_backfill(short_term_price_volume_based_return_5d, 66), 60))))",
    
    # 表达式 3: 使用 ts_delta 模拟变化率（4 腿组合）
    "rank(add(rank(ts_delta(ts_backfill(long_term_60d_quantile5_pred, 66), 60)), rank(ts_delta(ts_backfill(short_hedge_quantile5_r60_pred, 66), 60)), rank(ts_delta(ts_backfill(short_term_price_volume_based_return_5d, 66), 60)), rank(ts_delta(ts_backfill(event_5d_single_quantile_pred, 66), 60))))",
    
    # 表达式 4: 使用 ratio 变化率（2 腿组合）
    "rank(add(rank(divide(ts_backfill(long_term_60d_quantile5_pred, 66), ts_backfill(long_term_60d_quantile5_pred, 126))), rank(divide(ts_backfill(short_hedge_quantile5_r60_pred, 66), ts_backfill(short_hedge_quantile5_r60_pred, 126)))))",
    
    # 表达式 5: 使用 ratio 变化率（3 腿组合）
    "rank(add(rank(divide(ts_backfill(long_term_60d_quantile5_pred, 66), ts_backfill(long_term_60d_quantile5_pred, 126))), rank(divide(ts_backfill(short_hedge_quantile5_r60_pred, 66), ts_backfill(short_hedge_quantile5_r60_pred, 126))), rank(divide(ts_backfill(short_term_price_volume_based_return_5d, 66), ts_backfill(short_term_price_volume_based_return_5d, 126)))))",
    
    # 表达式 6: 使用 ts_mean 平滑（减少 Turnover）
    "rank(add(rank(ts_mean(ts_backfill(long_term_60d_quantile5_pred, 66), 20)), rank(ts_mean(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20))))",
    
    # 表达式 7: 使用 ts_mean 平滑（3 腿组合）
    "rank(add(rank(ts_mean(ts_backfill(long_term_60d_quantile5_pred, 66), 20)), rank(ts_mean(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20)), rank(ts_mean(ts_backfill(short_term_price_volume_based_return_5d, 66), 20))))",
    
    # 表达式 8: 使用 ts_mean 平滑（4 腿组合）
    "rank(add(rank(ts_mean(ts_backfill(long_term_60d_quantile5_pred, 66), 20)), rank(ts_mean(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20)), rank(ts_mean(ts_backfill(short_term_price_volume_based_return_5d, 66), 20)), rank(ts_mean(ts_backfill(event_5d_single_quantile_pred, 66), 20))))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 11
region = 'USA'
dataset = 'multifactor_return_pred'

# 删除旧的 wave 11 表达式
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
