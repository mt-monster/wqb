# USA 战役第10次多样性评估（波1-7, 批次 A→OO, ~26轮 × 8并发 ≈ 208条回测）

日期: 2026-08-16 | 范围: USA/TOP3000 D1 为主, option8 D0 试探

## 1. 探索率盘点

| 维度 | 已探索 | 池规模 | 探索率 | 结论 |
|---|---|---|---|---|
| 数据集 | 8 (option8/si3/model238/insiders3/snt21/transformer/snt22/option40) | 237候选 | 3.4% | 足够广, 但情绪类超配(3个) |
| 字段 | ~60 使用 | 541 白名单 | ~11% | 偏低, option40 新登记19字段待深挖 |
| 操作符 | ~16 (quantile/rank/group_zscore/group_rank/ts_decay_linear/ts_mean/ts_rank/ts_zscore/ts_delta/divide/subtract/signed_power/reverse/ts_product/if_else/or) | 102 白名单 | ~16% | ts_entropy/days_from_last_change/winsorize 未试 |
| 骨架 | 水平排名/反转/比率/zscore/复合decay/条件过滤 | — | 6类 | 条件激活(if_else+sigmoid)仅论坛见过未落地 |
| 风格 | 期权put-call/情绪反转/低波异象 | — | 3类 | 动量/盈余漂移/事件类未试 |

## 2. 收益来源归因（实证）

- **option8 put/call 水平族**: 信号强(2.19)但与全平台波动率因子高度重叠 → PROD 0.83-0.91 结构性墙。收益来源=大众低波异象, 已被挖尽。
- **情绪族 3 数据集 88 条**: 收益来源本身弱(新闻情绪半衰期短, D1 延迟后信息已price-in), 天花板 sharpe ~1.0。论坛佐证(scl12 ts_zscore 模板上限1.10)。
- **关键教训**: 信号强度上限由数据集信息含量决定, 骨架优化只能逼近上限不能突破。

## 3. 失效风险清单

1. 换手率-信号两难: ts_mean(20) 压 tv 至 13% 但信号腰斩(0.66); ts_decay 微效。**对策**: 优先选慢变字段(月度更新/长窗口), 而非事后平滑。
2. PROD 墙无法用骨架降(同数据集调参无效, ASI帖证实)。**对策**: 换蓝海数据集(userCount<1000)。
3. 方向假设必须实证: transformer reverse(neg)有效 vs snt22 正向有效, 完全相反。
4. group_vector_neut/hump 模板实证失效(顾问专属算子/信号被压平)。

## 4. Skills 优化动作（本轮落地）

1. ✅ 选数据集 SOP 升级: recommend_datasets + userCount<1000 + quality_score 优先 → 命中 option40(703用户)
2. ✅ 情绪族判死标准: 2个数据集同族全灭 + 论坛求证无新招 → 立即转向, 不再恋战
3. 待落地: ts_entropy 信息熵骨架(低PROD差异化工具, ASI帖策略三)
4. 待落地: days_from_last_change 换手控制(ASI帖策略)
5. 待落地: winsorize+ts_backfill+group_rank 稳健三件套(对RN测试有帮助)

## 5. 下10轮方向

- 主攻 option40 蓝海(波7 NN/OO 在飞), 若信号>1.3 则深挖其19字段
- 备选: macro38(Technical Ratings, 1371用户)、imbalance5(Oil Price Resilience)
- 禁用: 情绪族、option8红海、group_vector_neut/hump
