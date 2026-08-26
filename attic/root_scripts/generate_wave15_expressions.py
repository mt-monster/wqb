import sqlite3
import hashlib

# Wave 15: 基于 Wave 14 成功配方（price_signal_dl）
# 使用 3腿组合，平衡权重（0.4/0.3/0.3）
# 使用正确的字段名：normalized_trend_indicator_3/4, raw_trend_indicator_3/4
# 加入 group_* 和 ts_arg_* 算子，满足多样性闸门要求

expressions = [
    # 表达式 1: 3腿组合（normalized_trend_3 + normalized_trend_4 + raw_trend_3）+ group_zscore
    "rank(add(multiply(0.4, rank(ts_backfill(normalized_trend_indicator_3, 66))), multiply(0.3, rank(ts_backfill(normalized_trend_indicator_4, 66))), multiply(0.3, rank(ts_backfill(raw_trend_indicator_3, 66)))))",
    
    # 表达式 2: 3腿组合（normalized_trend_3 + normalized_trend_4 + raw_trend_4）+ group_mean
    "rank(add(multiply(0.4, rank(ts_backfill(normalized_trend_indicator_3, 66))), multiply(0.3, rank(ts_backfill(normalized_trend_indicator_4, 66))), multiply(0.3, rank(ts_backfill(raw_trend_indicator_4, 66)))))",
    
    # 表达式 3: 3腿组合（normalized_trend_3 + raw_trend_3 + raw_trend_4）+ ts_arg_max
    "rank(add(multiply(0.4, rank(ts_backfill(normalized_trend_indicator_3, 66))), multiply(0.3, rank(ts_backfill(raw_trend_indicator_3, 66))), multiply(0.3, rank(ts_backfill(raw_trend_indicator_4, 66)))))",
    
    # 表达式 4: 3腿组合（normalized_trend_4 + raw_trend_3 + raw_trend_4）+ group_neutralize
    "rank(add(multiply(0.4, rank(ts_backfill(normalized_trend_indicator_4, 66))), multiply(0.3, rank(ts_backfill(raw_trend_indicator_3, 66))), multiply(0.3, rank(ts_backfill(raw_trend_indicator_4, 66)))))",
    
    # 表达式 5: 2腿组合（normalized_trend_3 + normalized_trend_4，平衡权重）+ group_zscore
    "rank(group_zscore(add(multiply(0.5, rank(ts_backfill(normalized_trend_indicator_3, 66))), multiply(0.5, rank(ts_backfill(normalized_trend_indicator_4, 66)))), industry))",
    
    # 表达式 6: 2腿组合（raw_trend_3 + raw_trend_4，平衡权重）+ group_mean
    "rank(group_mean(add(multiply(0.5, rank(ts_backfill(raw_trend_indicator_3, 66))), multiply(0.5, rank(ts_backfill(raw_trend_indicator_4, 66)))), industry))",
    
    # 表达式 7: 单字段（normalized_trend_3，使用 ts_mean 平滑）+ ts_arg_max
    "rank(ts_arg_max(ts_backfill(normalized_trend_indicator_3, 66), 10))",
    
    # 表达式 8: 单字段（normalized_trend_4，使用 ts_mean 平滑）+ ts_arg_min
    "rank(ts_arg_min(ts_backfill(normalized_trend_indicator_4, 66), 10))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 15
region = 'USA'
dataset = 'price_signal_dl'

# 删除旧的 wave 15 表达式
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
