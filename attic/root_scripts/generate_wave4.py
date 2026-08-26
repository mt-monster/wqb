import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 基于 3 个候选表达式生成优化版本
optimized_exprs = [
    # 候选 1: rank(average_positive_sentiment_score_3 - average_negative_sentiment_score_3)
    # 优化：添加 ts_mean 平滑降低 turnover
    "rank(ts_mean(average_positive_sentiment_score_3 - average_negative_sentiment_score_3, 5))",
    "rank(ts_mean(average_positive_sentiment_score_3 - average_negative_sentiment_score_3, 10))",
    "rank(ts_mean(average_positive_sentiment_score_3 - average_negative_sentiment_score_3, 20))",
    
    # 候选 2: rank(average_positive_sentiment_score_3 / (average_positive_sentiment_score_3 + average_negative_sentiment_score_3 + ...))
    # 优化：添加 ts_mean 平滑降低 turnover
    "rank(ts_mean(average_positive_sentiment_score_3 / (average_positive_sentiment_score_3 + average_negative_sentiment_score_3 + average_neutral_sentiment_score_3 + 0.001), 5))",
    "rank(ts_mean(average_positive_sentiment_score_3 / (average_positive_sentiment_score_3 + average_negative_sentiment_score_3 + average_neutral_sentiment_score_3 + 0.001), 10))",
    "rank(ts_mean(average_positive_sentiment_score_3 / (average_positive_sentiment_score_3 + average_negative_sentiment_score_3 + average_neutral_sentiment_score_3 + 0.001), 20))",
    
    # 候选 3: rank(average_positive_sentiment_score_1 - average_positive_sentiment_score_5)
    # 优化：添加 ts_mean 平滑降低 turnover
    "rank(ts_mean(average_positive_sentiment_score_1 - average_positive_sentiment_score_5, 5))",
    "rank(ts_mean(average_positive_sentiment_score_1 - average_positive_sentiment_score_5, 10))",
    "rank(ts_mean(average_positive_sentiment_score_1 - average_positive_sentiment_score_5, 20))",
]

# 写入数据库 wave 4
wave = '4'
wave_id = 4
region = 'USA'
created_at = datetime.now().isoformat()

count = 0
for expr in optimized_exprs:
    cursor.execute('''
        INSERT INTO expressions (wave_id, expression, region, wave, dataset, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (wave_id, expr, region, wave, 'finnews_nlp_scores', 'mode_a', created_at, created_at))
    count += 1

conn.commit()
print(f'已写入 {count} 个优化表达式到 wave {wave}')

# 验证
cursor.execute('''
    SELECT COUNT(*)
    FROM expressions
    WHERE region=? AND wave=?
''', (region, wave))

total = cursor.fetchone()[0]
print(f'Wave {wave} 总表达式数: {total}')

conn.close()
