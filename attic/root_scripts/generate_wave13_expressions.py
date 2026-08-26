import sqlite3
import hashlib

# 基于 lej3ozml 的骨架模式进行 Mode A 参数层优化
# lej3ozml: Sharpe=1.900, Fitness=0.990, Turnover=0.212
# 骨架: rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))

expressions = [
    # 表达式 1: 调整权重（增加 long_term 权重）
    "rank(add(multiply(0.6, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.4, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 调整权重（增加 event_5d 权重）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.6, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 3: 调整 ts_backfill 窗口（long_term 使用 132）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 132))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 4: 调整 ts_backfill 窗口（event_5d 使用 132）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 132)))))",
    
    # 表达式 5: 调整 ts_backfill 窗口（所有字段使用 132）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 132))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 132)))))",
    
    # 表达式 6: 使用 ts_mean 平滑（减少 Turnover）
    "rank(add(multiply(0.5, rank(ts_mean(ts_backfill(long_term_quantile5_r120_pred, 66), 5))), multiply(0.3, rank(ts_mean(ts_backfill(event_5d_single_quantile_pred, 66), 5)))))",
    
    # 表达式 7: 使用 ts_decay_linear 平滑（减少 Turnover）
    "rank(add(multiply(0.5, rank(ts_decay_linear(ts_backfill(long_term_quantile5_r120_pred, 66), 5))), multiply(0.3, rank(ts_decay_linear(ts_backfill(event_5d_single_quantile_pred, 66), 5)))))",
    
    # 表达式 8: 3 腿组合（添加 short_hedge）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 13
region = 'USA'
dataset = 'analyst_earnings_ibes'

# 删除旧的 wave 13 表达式
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
