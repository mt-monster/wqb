import sqlite3
import hashlib

# Wave 14: Mode B 想法层优化（提高子宇宙 Sharpe）
# 基于 multifactor_return_pred 数据集，使用更多样化的字段组合

expressions = [
    # 表达式 1: 平衡权重组合（减少 long_term 权重，增加其他字段权重）
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 使用 ts_zscore 替代 rank（可能在某些子宇宙中表现更稳定）
    "rank(add(ts_zscore(ts_backfill(long_term_quantile5_r120_pred, 66), 20), ts_zscore(ts_backfill(short_hedge_quantile5_r60_pred, 66), 20)))",
    
    # 表达式 3: 使用 ts_mean 平滑（减少噪声）
    "rank(add(rank(ts_mean(ts_backfill(long_term_quantile5_r120_pred, 66), 5)), rank(ts_mean(ts_backfill(short_hedge_quantile5_r60_pred, 66), 5))))",
    
    # 表达式 4: 3 腿组合（long_term + short_hedge + event_5d）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 5: 3 腿组合（long_term + short_term + event_5d）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 6: 2 腿组合（long_term + short_hedge，平衡权重）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.5, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)))))",
    
    # 表达式 7: 2 腿组合（long_term + event_5d，平衡权重）
    "rank(add(multiply(0.5, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.5, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 8: 单字段（long_term，使用 ts_mean 平滑）
    "rank(ts_mean(ts_backfill(long_term_quantile5_r120_pred, 66), 10))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 14
region = 'USA'
dataset = 'multifactor_return_pred'

# 删除旧的 wave 14 表达式
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
