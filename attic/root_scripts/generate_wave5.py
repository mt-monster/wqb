import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 基于成功案例 USA-MFP-4LEG-WIN 的骨架模式，重新设计表达式
# 骨架：rank(add(multiply(w1, rank(ts_backfill(field1, 66))), multiply(w2, rank(ts_backfill(field2, 66))), ...))

redesigned_exprs = [
    # 2腿组合：positive_sentiment_3 + negative_sentiment_3
    "rank(add(multiply(0.6, rank(ts_backfill(average_positive_sentiment_score_3, 66))), multiply(-0.4, rank(ts_backfill(average_negative_sentiment_score_3, 66)))))",
    
    # 2腿组合：positive_sentiment_1 + positive_sentiment_5
    "rank(add(multiply(0.7, rank(ts_backfill(average_positive_sentiment_score_1, 66))), multiply(-0.3, rank(ts_backfill(average_positive_sentiment_score_5, 66)))))",
    
    # 3腿组合：positive_sentiment_3 + negative_sentiment_3 + neutral_sentiment_3
    "rank(add(multiply(0.5, rank(ts_backfill(average_positive_sentiment_score_3, 66))), multiply(-0.3, rank(ts_backfill(average_negative_sentiment_score_3, 66))), multiply(-0.2, rank(ts_backfill(average_neutral_sentiment_score_3, 66)))))",
    
    # 2腿组合：positive_sentiment_3 + positive_sentiment_1
    "rank(add(multiply(0.6, rank(ts_backfill(average_positive_sentiment_score_3, 66))), multiply(0.4, rank(ts_backfill(average_positive_sentiment_score_1, 66)))))",
    
    # 2腿组合：negative_sentiment_3 + negative_sentiment_1
    "rank(add(multiply(-0.6, rank(ts_backfill(average_negative_sentiment_score_3, 66))), multiply(-0.4, rank(ts_backfill(average_negative_sentiment_score_1, 66)))))",
    
    # 3腿组合：positive_sentiment_1 + positive_sentiment_3 + positive_sentiment_5
    "rank(add(multiply(0.5, rank(ts_backfill(average_positive_sentiment_score_1, 66))), multiply(0.3, rank(ts_backfill(average_positive_sentiment_score_3, 66))), multiply(-0.2, rank(ts_backfill(average_positive_sentiment_score_5, 66)))))",
    
    # 2腿组合：positive_sentiment_3 + negative_sentiment_1
    "rank(add(multiply(0.7, rank(ts_backfill(average_positive_sentiment_score_3, 66))), multiply(-0.3, rank(ts_backfill(average_negative_sentiment_score_1, 66)))))",
    
    # 2腿组合：positive_sentiment_1 + negative_sentiment_3
    "rank(add(multiply(0.6, rank(ts_backfill(average_positive_sentiment_score_1, 66))), multiply(-0.4, rank(ts_backfill(average_negative_sentiment_score_3, 66)))))",
    
    # 4腿组合：positive_sentiment_1 + positive_sentiment_3 + negative_sentiment_1 + negative_sentiment_3
    "rank(add(multiply(0.4, rank(ts_backfill(average_positive_sentiment_score_1, 66))), multiply(0.3, rank(ts_backfill(average_positive_sentiment_score_3, 66))), multiply(-0.2, rank(ts_backfill(average_negative_sentiment_score_1, 66))), multiply(-0.1, rank(ts_backfill(average_negative_sentiment_score_3, 66)))))",
]

# 写入数据库 wave 5
wave = '5'
wave_id = 5
region = 'USA'
created_at = datetime.now().isoformat()

count = 0
for expr in redesigned_exprs:
    cursor.execute('''
        INSERT INTO expressions (wave_id, expression, region, wave, dataset, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (wave_id, expr, region, wave, 'finnews_nlp_scores', 'mode_b', created_at, created_at))
    count += 1

conn.commit()
print(f'已写入 {count} 个重新设计的表达式到 wave {wave}')

# 验证
cursor.execute('''
    SELECT COUNT(*)
    FROM expressions
    WHERE region=? AND wave=?
''', (region, wave))

total = cursor.fetchone()[0]
print(f'Wave {wave} 总表达式数: {total}')

conn.close()
