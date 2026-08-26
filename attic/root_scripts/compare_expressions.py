# 成功案例的表达式（从 registry 中获取）
win_expression = "rank(add(multiply(w1, rank(ts_backfill(long_term, 66))), multiply(w2, rank(ts_backfill(short_hedge2, 66))), multiply(w3, rank(ts_backfill(pv, 66))), multiply(w4, rank(ts_backfill(event_5d, 66)))))"

# 我们的 Top 1 候选表达式
our_expression = "rank(add(multiply(0.3, rank(ts_backfill(long_term_120d_quantile5_pred, 66))), multiply(0.3, rank(ts_backfill(short_hedge_quantile5_r60_pred, 66))), multiply(0.2, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.2, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))"

print('成功案例的表达式:')
print(win_expression)
print('\n我们的 Top 1 候选表达式:')
print(our_expression)

print('\n\n差异分析:')
print('1. 字段名称:')
print('   - 成功案例: long_term, short_hedge2, pv, event_5d')
print('   - 我们的: long_term_120d_quantile5_pred, short_hedge_quantile5_r60_pred, short_term_price_volume_based_return_5d, event_5d_single_quantile_pred')
print('\n2. 权重:')
print('   - 成功案例: w1, w2, w3, w4 (未知具体值)')
print('   - 我们的: 0.3, 0.3, 0.2, 0.2')
print('\n3. 性能指标:')
print('   - 成功案例: Sharpe=2.02, Fitness=1.01, Turnover=0.2359')
print('   - 我们的: Sharpe=1.88, Fitness=0.98, Turnover=0.248')
print('\n4. 差距:')
print('   - Sharpe 差距: 2.02 - 1.88 = 0.14')
print('   - Fitness 差距: 1.01 - 0.98 = 0.03')
print('   - Turnover 差距: 0.248 - 0.2359 = 0.0121')
