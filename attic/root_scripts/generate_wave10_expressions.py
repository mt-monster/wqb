import sqlite3
import hashlib

# Mode A 参数层优化：调整权重和 ts_backfill 窗口
# 基于 Top 1 候选表达式（KP7OJWbE）进行优化

expressions = [
    # 表达式 1: 调整权重（增加 long_term 权重）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_120d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.1, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 调整权重（增加 short_hedge 权重）
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_120d_quantile5_pred, 66))), multiply(0.4, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.1, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 3: 调整 ts_backfill 窗口（long_term 使用 132）
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_120d_quantile5_pred, 132))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 4: 调整 ts_backfill 窗口（所有字段使用 132）
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_120d_quantile5_pred, 132))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 132))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 132))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 132)))))",
    
    # 表达式 5: 调整 ts_backfill 窗口（所有字段使用 22）
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_120d_quantile5_pred, 22))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 22))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 22))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 22)))))",
    
    # 表达式 6: 使用 ts_mean 平滑（减少 Turnover）
    "rank(add(multiply(0.3, rank(ts_mean(ts_backfill(long_term_120d_quantile5_pred, 66), 5))), multiply(0.3, rank(ts_mean(ts_backfill(short_hedge_quantile5_r60_pred, 66), 5))), multiply(0.2, rank(ts_mean(ts_backfill(short_term_price_volume_based_return_5d, 66), 5))), multiply(0.2, rank(ts_mean(ts_backfill(event_5d_single_quantile_pred, 66), 5)))))",
    
    # 表达式 7: 使用 ts_decay_linear 平滑（减少 Turnover）
    "rank(add(multiply(0.3, rank(ts_decay_linear(ts_backfill(long_term_120d_quantile5_pred, 66), 5))), multiply(0.3, rank(ts_decay_linear(ts_backfill(short_hedge_quantile5_r60_pred, 66), 5))), multiply(0.2, rank(ts_decay_linear(ts_backfill(short_term_price_volume_based_return_5d, 66), 5))), multiply(0.2, rank(ts_decay_linear(ts_backfill(event_5d_single_quantile_pred, 66), 5)))))",
    
    # 表达式 8: 3 腿组合（去掉 event_5d，增加其他权重）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_120d_quantile5_pred, 66))), multiply(0.4, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 66)))))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 10
region = 'USA'
dataset = 'multifactor_return_pred'

# 删除旧的 wave 10 表达式
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
