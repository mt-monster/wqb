# Wave P4 预案：news50（news 塔 · 未点亮 · 拥挤度≈0）10 模板

## 为什么转场（对硬约束「不得频繁切换数据集」的说明）
dl_riskfree 已跑满 14 个结构互异变体 + P1/P2/P3 三个机制面，prod 全部落 0.75–0.85。
实测证据：prod 池约 470 颗 KOR alpha，价格/ML 概率类信号的最大相关被其中单颗 alphas 锁定在 0.75+，
而三颗成功交付件（risk70 载荷 / analyst 惊喜 / insiders 离散度）都是**特异型**信号。
⇒ 继续在概率场加参数属于「盲扫」，转场到**未点亮 + 零拥挤**的 news 塔是唯一有 prod 空间的方向。

## 数据集选择依据（MCP get_datasets）
| 数据集 | 字段 | 用户 | alphaCount | 覆盖 | 判定 |
|---|---:|---:|---:|---:|---|
| **news50** | 71 | 56 | 113 | 0.6254 | ✅ 选中：覆盖可接受 + 拥挤度低 + 字段语义丰富（情感/新颖度/相关性） |
| news38 | 36 | 89 | 228 | 0.7971 | 备选（覆盖最好，拥挤度次低） |
| news29 | 12 | 14 | 29 | 0.467 | 备选（最冷门，覆盖偏低） |
| news46 | 44 | 57 | 126 | 0.3418 | 备选 |
| institutions6 / earnings3 | – | – | 1013 / 2624 | – | ✗ 拥挤度太高 |

## 字段画像
见 `s1_field_profile_news50.md`（71 字段全 VECTOR，cov 0.6528，aC 0–1）。
⚠ 全 VECTOR ⇒ 进标量算子前必须 vec_* 聚合（否则 `divide does not support event inputs` 整批 ERROR）。

## 10 个结构互异模板（全部自建；来源标注）

| # | 经济机制 | 结构 | 模板 | 来源 |
|---|---|---|---|---|
| 1 | 新闻语调水平 → 情绪溢价 | 一阶矩 | group_rank(vec_avg(tone), subindustry) | 自建 + 论坛《论文合集》情感类 |
| 2 | 报道语调分歧 → dispersion anomaly | 二阶矩 | group_rank(vec_stddev(tone), subindustry) | 自建 + Diether 分歧度文献 |
| 3 | 新闻强度/关注度 → 注意力效应 | 计数 | group_rank(vec_count(tone), subindustry) | 自建 + Barber-Odean 注意力 |
| 4 | 语调动量 → 反应不足 | 一阶差分 | group_rank(ts_delta(vec_avg(tone),5), subindustry) | 自建 |
| 5 | 相关性加权语调 → 信号纯度 | 加权矩 | group_rank(divide(vec_sum(tone*relevance), vec_sum(relevance)), subindustry) | 自建（新闻独有结构） |
| 6 | 事件新颖度 → 未定价信息 | 水平 | group_rank(vec_avg(event_novelty), subindustry) | 自建 + 未定价信息文献 |
| 7 | 跨题材语调分歧（财报 vs 公司行动） | 截面差 | group_rank(vec_avg(earnings_eval) − vec_avg(corporate_action), subindustry) | 自建 |
| 8 | 语调 × 新颖度 合取 → 高信息含量正面新闻 | 合取 | multiply(group_rank(vec_avg(tone)), group_rank(vec_avg(novelty))) | 自建 |
| 9 | 语调波动率 → 叙事不稳定 | 时序方差 | group_rank(ts_std_dev(vec_avg(tone),22), subindustry) | 自建 |
| 10 | 分析师推荐变化情感 → 修正传导 | 平滑水平 | group_rank(ts_mean(vec_avg(analyst_rec_change),22), subindustry) | 自建 |

中性化一律 **subindustry**（粒度最细 ⇒ 最大化 idio 成分，per memory 粒度律：sub/S 比值 subindustry 最优）。
算子数 3–6，全部 ≤12。preflight 已过（valid=true / unknown_fields=[] / any_changed=false）。

## 判读预案
- 先看**能否出 S≥1.58 且 raFail=0**；任一达标 ⇒ 立刻 self（零成本）→ prod（约 5s，未拥塞时）。
- 若整批 S 全 <1.0 ⇒ news50 无信号，换 news38 / news29 复测同模板（模板已冻结，只换数据集）。
- 若出活口但 prod >0.70 ⇒ 记入 prod 阶梯；本塔若能出 1 颗 prod 合格件，则按同法在 news38/29 复制。
