# GBR Wave 09 Batch 3 - pattern_scores 技术形态相似度数据集
# 策略风格: 技术形态识别 (reversal + breakout)
# 数据集: pattern_scores (alphaCount=65, pyramid=1.7, cov=0.9924)
# 设置: GBR/TOP700/D1/SUBINDUSTRY/decay=4/truncation=0.08/maxTrade=ON

expressions = [
    # 1. Falling wedge reversal (bullish pattern) - 高相似度预示底部反转
    "rank(ts_delta(falling_wedge_mean_simscore_lookback60, 5)) * -1",

    # 2. Rising wedge reversal (bearish pattern) - 高相似度预示顶部反转
    "rank(ts_delta(mean_similarity_rising_wedge, 5))",

    # 3. Ascending triangle breakout (bullish) - 高相似度预示突破
    "rank(ts_delta(asc_triangle_mean_simscore_lookback60, 5)) * -1",

    # 4. Descending triangle breakdown (bearish) - 高相似度预示下跌
    "rank(ts_delta(desc_triangle_mean_simscore_lookback60, 5))",

    # 5. Upward breakaway gap (bullish momentum)
    "rank(ts_delta(breakaway_gap_up_mean_simscore_lookback60, 5)) * -1",

    # 6. Downward breakaway gap (bearish momentum)
    "rank(ts_delta(breakaway_gap_down_mean_simscore_lookback60, 5))",

    # 7. V-bottom reversal (bullish)
    "rank(ts_delta(dynamic_similarity_reversal_v_bottom, 5)) * -1",

    # 8. Multi-pattern blend: falling wedge + ascending triangle + V-bottom (all bullish)
    "add(add(rank(ts_delta(falling_wedge_mean_simscore_lookback60, 5)), rank(ts_delta(asc_triangle_mean_simscore_lookback60, 5))), rank(ts_delta(dynamic_similarity_reversal_v_bottom, 5))) * -1",
]

# 写入文件
with open('tracking/GBR/candidates/gbr_w09_pattern_scores_batch3.txt', 'w') as f:
    for i, expr in enumerate(expressions, 1):
        f.write(f"# {i}. {expr}\n{expr}\n\n")

print(f"Generated {len(expressions)} expressions for GBR Wave 09 Batch 3 (pattern_scores)")
for i, expr in enumerate(expressions, 1):
    print(f"{i}. {expr}")
