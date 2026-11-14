# GBR delay1 other250 GEM Ideas（TOP700 / SUBINDUSTRY / decay4）

**Dataset**: other250
**Region**: GBR
**Delay**: 1

数据集：other250（电商商品数据，12 字段）。六法在线评测 2026-11-14（批 `1GZQUp6D94v3b3V8oveUlyv` @NONE/dec0/nanOFF）：
- 法1 覆盖：item_rating **325/700**、review_count 325、oth250_rank / sales_position_rank **342/700**、display_price 326
- 法2 非零：`divide(review_count, review_count)` 325 = 覆盖同数 ⇒ 零值可忽略
- 法3 频率：review_count N=22 变化 **386/329 ≈ 100%** ⇒ **日更**
- 法6 形态：`ts_zscore(item_rating,252) > 0` 占 **176/325 = 54%**（对 50% 参考）⇒ 轻度右偏，接近对称
- ★关键读数警示：**八字段裸读数全部 0.70-0.79 且 lc/sc 一律 325/0 单边**（rating 0.75 / review 0.70 / rank 0.74 / **price 0.79**）⇒ 高度同源，本质是**「电商规模/热度」单边暴露**（大公司 SKU 多、评论多、价格高）。可交付信号必须在行业中性化后看。

死路规避（矩阵 A-F 实证处方 + 本集特性）：
- 不做 sign/sqrt/tail/hump 压缩（矩阵 C：压缩即毁 40-50%）
- 不用 group_sum/group_std_dev/group_count（矩阵 F：TO 0.77-0.82 爆 0.70 闸）
- **不用裸 NONE 档读数**（本条最关键：325/0 单边，必须行业中性化）
- 不把 price 当选股信号（price 是最强的规模代理 0.79，会与中性化直接冲突）

文献锚：
- **《Online reviews can predict long-term returns of individual stocks》**（1800 万条京东评论 / 102 家上市公司）：消费者评论可预测**8 周（长期）**个股收益，比传统技术指标强 14%；机制 = 自愿性消费者反馈作为**品牌权益与长期公司价值**的代理（crowd wisdom）。⇒ **窗口要用长窗（66-252），不要短窗**。
- MDPI (2025) 媒体情绪与股票表现：社交媒体情绪影响成交量与波动。
- 消费者需求类另类数据的经典风险：与规模、动量高度相关 ⇒ 中性化必须做。

**Concept**: 消费者评价水平（consumer rating level）
- **Mechanism**: 产品星级高 = 品牌权益与消费者满意度强（文献：消费者反馈是长期公司价值代理）；行业中性化剔除「大公司评论多」的规模效应
- **Fields**: `oth250_item_rating`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth250_item_rating}), 66), industry)`
- **Direction**: 正
- **expected_exposure**: consumer brand equity

**Concept**: 评价热度（review volume）
- **Mechanism**: 评论数 = 消费者参与度与产品需求强度（销量代理）；长窗平滑（文献 8 周效应）
- **Fields**: `oth250_item_review_count`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth250_item_review_count}), 66), industry)`
- **Direction**: 正
- **expected_exposure**: product demand intensity

**Concept**: 畅销排名强度（bestseller rank strength）
- **Mechanism**: 排名数字小 = 畅销；反向取负排名即做多畅销品公司（需求强）；行业内相对化
- **Fields**: `oth250_rank`
- **Implementation Example**: `multiply(-1, group_rank(ts_mean(vec_avg({oth250_rank}), 66), industry))`
- **Direction**: 负（排名低 = 畅销 → 买）
- **expected_exposure**: bestseller strength

**Concept**: 评价动量（rating momentum）
- **Mechanism**: 星级**改善** = 品牌权益边际提升（慢变量，用 66 日变化）；区别于水平（水平已被规模污染）
- **Fields**: `oth250_item_rating`
- **Implementation Example**: `group_rank(ts_delta(ts_mean(vec_avg({oth250_item_rating}), 22), 66), industry)`
- **Direction**: 正
- **expected_exposure**: brand equity improvement

**Concept**: 评价质量与热度背离（rating vs volume divergence）
- **Mechanism**: 星级（质量）相对评论数（热度）超配 = 高质量小众品牌 vs 高热度低质（促销驱动）；对偶价差形式，不用加权相加
- **Fields**: `oth250_item_rating`, `oth250_item_review_count`
- **Implementation Example**: `group_rank(subtract(group_rank(ts_mean(vec_avg({oth250_item_rating}), 66), industry), group_rank(ts_mean(vec_avg({oth250_item_review_count}), 66), industry)), industry)`
- **Direction**: 正（质量优先于热度）
- **expected_exposure**: quality-over-hype

**Concept**: 畅销排名改善（rank improvement）
- **Mechanism**: 排名数字下降 = 销售爬升（需求加速）；用长窗变化捕捉趋势而非噪声
- **Fields**: `oth250_rank`
- **Implementation Example**: `multiply(-1, group_rank(ts_delta(ts_mean(vec_avg({oth250_rank}), 66), 66), industry))`
- **Direction**: 负（排名数字下降 = 向好）
- **expected_exposure**: sales rank improvement

**Concept**: 价格带定位（price tier，结构对照臂）
- **Mechanism**: 商品价格带 = 高端 vs 低价定位（品牌溢价 vs 走量）；⚠ 六法显示 price 是最强规模代理（0.79），此处**作为对照臂**检验中性化是否能剥离
- **Fields**: `oth250_item_display_price`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth250_item_display_price}), 66), industry)`
- **Direction**: 正（对照）
- **expected_exposure**: price tier positioning（规模污染对照）

多样性自检：Expected Exposure 6 种 ✓；字段族 3（rating、review_count、rank/price）✓；分组轴 industry 主 + sector/subindustry 备 ✓；时间尺度 22/66 ✓（按文献用长窗）；算子数 3-6 全部 ≤8 ✓。
⚠ 强制检查：①每臂 lc/sc 必须 ≥150（本集真实覆盖 325-342）；②deliverable 必须 INDUSTRY 或 SUBINDUSTRY 中性化，NONE 档读数不作数。
