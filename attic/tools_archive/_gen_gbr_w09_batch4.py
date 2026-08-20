# GBR Wave 09 Batch 4 - news104 新闻情绪数据集
# 策略风格: 新闻情绪驱动 (sentiment momentum)
# 数据集: news104 (alphaCount=10, pyramid=1.8, cov=0.9695)
# 注意: VECTOR 字段需要 vec_* 聚合
# 设置: GBR/TOP700/D1/SUBINDUSTRY/decay=4/truncation=0.08/maxTrade=ON

expressions = [
    # 1. 正面情绪概率 - 反转策略（高正面情绪后反转）
    "rank(ts_delta(vec_avg(nws104_prob_pos), 5)) * -1",

    # 2. 负面情绪概率 - 动量策略（高负面情绪后继续下跌）
    "rank(ts_delta(vec_avg(nws104_prob_neg), 5))",

    # 3. 情绪差值 (pos - neg) - 反转
    "rank(ts_delta(vec_avg(nws104_prob_pos) - vec_avg(nws104_prob_neg), 5)) * -1",

    # 4. 市场影响分数 - 反转
    "rank(ts_delta(vec_avg(nws104_marketimpactscore), 5)) * -1",

    # 5. 情绪分类 - 反转
    "rank(ts_delta(vec_avg(nws104_sentiment), 5)) * -1",

    # 6. 情绪置信度加权 - 高置信度情绪更可靠
    "rank(ts_delta(vec_avg(nws104_prob_pos) * vec_avg(nws104_confidence), 5)) * -1",

    # 7. 新颖度加权情绪 - 新闻越新影响越大
    "rank(ts_delta(vec_avg(nws104_prob_pos) / vec_avg(nws104_novelty), 5)) * -1",

    # 8. 多因子混合: 情绪差值 + 市场影响
    "add(rank(ts_delta(vec_avg(nws104_prob_pos) - vec_avg(nws104_prob_neg), 5)), rank(ts_delta(vec_avg(nws104_marketimpactscore), 5))) * -1",
]

# 写入文件
with open('tracking/GBR/candidates/gbr_w09_news104_batch4.txt', 'w') as f:
    for i, expr in enumerate(expressions, 1):
        f.write(f"# {i}. {expr}\n{expr}\n\n")

print(f"Generated {len(expressions)} expressions for GBR Wave 09 Batch 4 (news104)")
for i, expr in enumerate(expressions, 1):
    print(f"{i}. {expr}")
