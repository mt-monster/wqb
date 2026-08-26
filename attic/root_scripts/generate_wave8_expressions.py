import sqlite3
import json
import hashlib
from datetime import datetime

# 基于成功案例 USA-MFP-4LEG-WIN 的骨架模式生成表达式
# 骨架: rank(add(multiply(w1, rank(ts_backfill(field1, 66))), multiply(w2, rank(ts_backfill(field2, 66))), ...))

# 根据成功案例和字段搜索，选择以下字段组合：
# - long_term: long_term_60d_quantile5_pred
# - short_hedge2: short_hedge_quantile5_r60_pred
# - pv: price_volume_quantile5_r5_pred (需要查找)
# - event_5d: event_5d_single_quantile_pred

# 生成 4 腿组合表达式（基于成功案例）
expressions = [
    # 表达式 1: 成功案例的精确复制
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(price_volume_quantile5_r5_pred, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 2: 调整权重
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(price_volume_quantile5_r5_pred, 66))), multiply(0.1, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 3: 3 腿组合（去掉 event_5d）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.3, rank(ts_backfill(price_volume_quantile5_r5_pred, 66)))))",
    
    # 表达式 4: 3 腿组合（去掉 pv）
    "rank(add(multiply(0.4, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.4, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 5: 2 腿组合（long_term + short_hedge）
    "rank(add(multiply(0.6, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.4, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66)))))",
    
    # 表达式 6: 2 腿组合（long_term + pv）
    "rank(add(multiply(0.6, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.4, rank(ts_backfill(price_volume_quantile5_r5_pred, 66)))))",
    
    # 表达式 7: 使用 120d 长期预测
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_120d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(price_volume_quantile5_r5_pred, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
    
    # 表达式 8: 使用不同的 short_hedge 字段
    "rank(add(multiply(0.3, rank(ts_backfill(long_term_60d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_60d_quantile5_pred, 66))), multiply(0.2, rank(ts_backfill(price_volume_quantile5_r5_pred, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 8
region = 'USA'
dataset = 'multifactor_return_pred'

# 删除旧的 wave 8 表达式
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
