# GBR Wave 09 Batch 2 - model264 趋势预测模型数据集
# 策略风格: ML 趋势预测概率 (momentum + analyst revision)
# 数据集: model264 (alphaCount=38, pyramid=1.8, cov=0.9768)
# 设置: GBR/TOP700/D1/SUBINDUSTRY/decay=4/truncation=0.08/maxTrade=ON

expressions = [
    # 1. EPS revision momentum (1M) - 使用 move-up 概率
    "rank(mdl264_3l_m1r_1yf_spe_se) * -1",

    # 2. EPS diffusion momentum (1M) - 使用 move-up 概率
    "rank(mdl264_3l_m1d_1yf_spe_se) * -1",

    # 3. Recommendation revision momentum - 使用 move-up 概率
    "rank(mdl264_3l_m1r_cer_se) * -1",

    # 4. Target price revision momentum - 使用 move-up 概率
    "rank(mdl264_3l_m1r_pt_se) * -1",

    # 5. Long-term growth revision momentum - 使用 move-up 概率
    "rank(mdl264_3l_m1r_gtl_se) * -1",

    # 6. Bollinger Bands trend - 使用 move-up 概率
    "rank(mdl264_3l_bb) * -1",

    # 7. EPS Surprise with Decay - 使用 move-up 概率
    "rank(mdl264_3l_eps_sur_decay_l3) * -1",

    # 8. Multi-factor blend: EPS revision + Recommendation + Target price
    "add(add(rank(mdl264_3l_m1r_1yf_spe_se), rank(mdl264_3l_m1r_cer_se)), rank(mdl264_3l_m1r_pt_se)) * -1",
]

# 写入文件
with open('tracking/GBR/candidates/gbr_w09_model264_batch2.txt', 'w') as f:
    for i, expr in enumerate(expressions, 1):
        f.write(f"# {i}. {expr}\n{expr}\n\n")

print(f"Generated {len(expressions)} expressions for GBR Wave 09 Batch 2 (model264)")
for i, expr in enumerate(expressions, 1):
    print(f"{i}. {expr}")
