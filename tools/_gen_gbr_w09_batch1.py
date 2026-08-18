# GBR Wave 09 - other455 Node2Vec 嵌入数据集
# 策略风格: 关系网络嵌入因子 (reversal + momentum blend)
# 数据集: other455 (alphaCount=11, pyramid=1.8, cov=0.9381)
# 设置: GBR/TOP700/D1/SUBINDUSTRY/decay=4/truncation=0.08/maxTrade=ON

# Batch 1: Relation N2V PCA factors - reversal style
# 使用 relation_n2v 的 PCA factor 1/2/3，w1-w5 窗口

expressions = [
    # 1. Relation PCA fact1 reversal (w1)
    "rank(ts_delta(oth455_relation_n2v_p10_q200_w1_pca_fact1_value, 5)) * -1",

    # 2. Relation PCA fact2 reversal (w1)
    "rank(ts_delta(oth455_relation_n2v_p10_q200_w1_pca_fact2_value, 5)) * -1",

    # 3. Relation PCA fact3 reversal (w2)
    "rank(ts_delta(oth455_relation_n2v_p10_q200_w2_pca_fact3_value, 5)) * -1",

    # 4. Relation PCA fact1 momentum blend (w1 + w2)
    "add(rank(ts_delta(oth455_relation_n2v_p10_q200_w1_pca_fact1_value, 5)), rank(ts_delta(oth455_relation_n2v_p10_q200_w2_pca_fact1_value, 5))) * -1",

    # 5. Competitor PCA fact1 reversal (w1)
    "rank(ts_delta(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 5)) * -1",

    # 6. Customer PCA fact1 reversal (w1)
    "rank(ts_delta(oth455_customer_n2v_p10_q200_w1_pca_fact1_value, 5)) * -1",

    # 7. Partner PCA fact1 reversal (w1)
    "rank(ts_delta(oth455_partner_n2v_p10_q200_w1_pca_fact1_value, 5)) * -1",

    # 8. Multi-relation blend: competitor + customer + partner
    "add(add(rank(ts_delta(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 5)), rank(ts_delta(oth455_customer_n2v_p10_q200_w1_pca_fact1_value, 5))), rank(ts_delta(oth455_partner_n2v_p10_q200_w1_pca_fact1_value, 5))) * -1",
]

# 写入文件
with open('tracking/GBR/candidates/gbr_w09_other455_batch1.txt', 'w') as f:
    for i, expr in enumerate(expressions, 1):
        f.write(f"# {i}. {expr}\n{expr}\n\n")

print(f"Generated {len(expressions)} expressions for GBR Wave 09 Batch 1")
for i, expr in enumerate(expressions, 1):
    print(f"{i}. {expr[:80]}...")
