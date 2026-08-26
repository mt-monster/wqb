import sqlite3
import hashlib

# 基于 MEA 成功案例的骨架模式，使用 analyst_earnings_ibes 数据集
# 骨架: rank(field1/field1_lag-1) + rank(field2/field2_lag-1)
# 关键特征: 使用 ratio 变化率，Turnover 非常低

# analyst_earnings_ibes 数据集有 42 个字段，包括：
# - est_q_eps_mean
# - est_q_eps_mean_3mth_ago
# - est_q_net_mean
# - est_q_net_mean_3mth_ago

expressions = [
    # 表达式 1: MEA 成功案例的精确复制（EPS + Net 变化率）
    "rank(add(rank(divide(vec_avg(est_q_eps_mean), vec_avg(est_q_eps_mean_3mth_ago))), rank(divide(vec_avg(est_q_net_mean), vec_avg(est_q_net_mean_3mth_ago)))))",
    
    # 表达式 2: EPS 变化率 + Net 变化率（减去 1）
    "rank(add(rank(subtract(divide(vec_avg(est_q_eps_mean), vec_avg(est_q_eps_mean_3mth_ago)), 1)), rank(subtract(divide(vec_avg(est_q_net_mean), vec_avg(est_q_net_mean_3mth_ago)), 1))))",
    
    # 表达式 3: EPS 变化率（单字段）
    "rank(subtract(divide(vec_avg(est_q_eps_mean), vec_avg(est_q_eps_mean_3mth_ago)), 1))",
    
    # 表达式 4: Net 变化率（单字段）
    "rank(subtract(divide(vec_avg(est_q_net_mean), vec_avg(est_q_net_mean_3mth_ago)), 1))",
    
    # 表达式 5: EPS + Net + PT 变化率（3 腿组合）
    "rank(add(rank(subtract(divide(vec_avg(est_q_eps_mean), vec_avg(est_q_eps_mean_3mth_ago)), 1)), rank(subtract(divide(vec_avg(est_q_net_mean), vec_avg(est_q_net_mean_3mth_ago)), 1)), rank(subtract(divide(vec_avg(est_q_pt_mean), vec_avg(est_q_pt_mean_3mth_ago)), 1))))",
    
    # 表达式 6: EPS 变化率 + Net 变化率（使用 ts_mean 平滑）
    "rank(add(rank(ts_mean(subtract(divide(vec_avg(est_q_eps_mean), vec_avg(est_q_eps_mean_3mth_ago)), 1), 5)), rank(ts_mean(subtract(divide(vec_avg(est_q_net_mean), vec_avg(est_q_net_mean_3mth_ago)), 1), 5))))",
    
    # 表达式 7: EPS 变化率 + Net 变化率（使用 ts_backfill 预处理）
    "rank(add(rank(subtract(divide(ts_backfill(vec_avg(est_q_eps_mean), 66), ts_backfill(vec_avg(est_q_eps_mean_3mth_ago), 66)), 1)), rank(subtract(divide(ts_backfill(vec_avg(est_q_net_mean), 66), ts_backfill(vec_avg(est_q_net_mean_3mth_ago), 66)), 1))))",
    
    # 表达式 8: EPS 变化率 + Net 变化率（使用 ts_backfill + ts_mean 平滑）
    "rank(add(rank(ts_mean(subtract(divide(ts_backfill(vec_avg(est_q_eps_mean), 66), ts_backfill(vec_avg(est_q_eps_mean_3mth_ago), 66)), 1), 5)), rank(ts_mean(subtract(divide(ts_backfill(vec_avg(est_q_net_mean), 66), ts_backfill(vec_avg(est_q_net_mean_3mth_ago), 66)), 1), 5))))",
]

# 写入数据库
conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

wave_id = 12
region = 'USA'
dataset = 'analyst_earnings_ibes'

# 删除旧的 wave 12 表达式
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
