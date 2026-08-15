# 经济含义 Alpha 模板库（Economic Alpha Template Library）

> 用途：为 BRAIN alpha 挖掘提供**经济学含义驱动**的表达式骨架，替代"薄模板"（单字段 rank/动量堆砌）。
> 来源：
> - Kakushadze《101 Formulaic Alphas》原文（KB: `reference/101_formulaic_alphas_kb.md`）——101 个 WorldQuant 生产级 alpha 的算子规律与 7 类模板
> - Tulchinsky《寻找Alpha：量化交易策略》内容体系（该书为纯扫描版无法提取文本，采用其公开内容框架：信号分类学 + 收益来源归因 + 衰减规律）
> - 本战役 KOR/D1 实证（multi_source_model/chart_cnn_alpha 等 11 个数据集的成败记录）
>
> 核心原则：**每个表达式必须能回答三问**——谁在交易？为什么 edge 存在且持续？信号衰减周期多长？答不上来的模板不提交。

---

## 一、经济学主题 × 表达式骨架（12 类）

### T1 均值回归 / 短期反转（价格压力是暂时的）
- **经济逻辑**：流动性冲击/散户过度反应造成价格偏离基本面，做市商与套利者推动回归；持仓期 1-5 天。
- **骨架**：`reverse(ts_delta(field, n))`、`reverse(ts_rank(field, n))`、放量日反向 `multiply(sign(ts_delta(volume,1)), reverse(ts_delta(close,1)))`（101 #12）
- **适用**：量价数据集（returns/close/volume 字段）。注意 KOR D1 下模型类慢信号用动量/逆向全死（chart_cnn 实证），反转只适用于高频更新的量价字段。

### T2 动量 / 信息扩散（信息逐步被定价）
- **经济逻辑**：信息在投资者间扩散需要时间，机构调仓也分步执行 → 趋势延续；持仓期 5-60 天。
- **骨架**：`ts_delta(ts_backfill(F,66),22)`、条件动量 `trade_when(x, greater(斜率, 阈值), 0)`（101 #46/49）
- **实证警告**：KOR 模型预测类数据集（chart_cnn/multi_source_model）动量腿全死——模型输出本身已含动量信息，二次动量是噪声。动量只用在原始量价/基本面字段。

### T3 量价背离（拥挤度反向，101 最强主题）
- **经济逻辑**：价量同向放大=散户追涨拥挤=未来反转；101 中 10/101 个 alpha 用 `-1×corr(price,volume)`，平均相关性最低、Sharpe 中位最高。
- **骨架**：`reverse(ts_corr(rank(price), rank(volume), 5~10))`、`reverse(ts_covariance(...))`
- **算子**：ts_corr / ts_covariance（此前未用，本主题核心）
- **适用**：任何含 price+volume 的数据集；KOR 白名单中 multi_source_model 的 price_volume 族因 PROD 墙不可用，留作其他 region。

### T4 波动率风险溢价 / 低波动异象
- **经济逻辑**：投资者偏好"彩票型"高波动股 → 高波动被高估、低波动被低估（低波动异象）；或反向：波动本身携带信息（101 #22/40 用 stddev 与量价交互）。
- **骨架**：`divide(rank(F), add(ts_std_dev(F,22),0.1))`（噪声惩罚=信号IR思想）、`multiply(reverse(rank(ts_std_dev(close,20))), ts_corr(high,volume,5))`
- **算子**：ts_std_dev / ts_ir（均值/波动=稳定性，预测越稳越可信）

### T5 流动性溢价（Amihud 非流动性）
- **经济逻辑**：持有低流动性资产需要补偿 → 非流动性溢价；流动性冲击后价格过度偏离。
- **骨架**：`rank(divide(abs(returns), volume))`（Amihud ILLIQ）、`reverse(rank(volume/adv20))` 活跃度反向
- **适用**：量价数据集；注意 KOR TOP600 大盘流动性普遍好，区分度可能弱。

### T6 基本面 / 盈利修正（盈余惊喜持续漂移 PEAD）
- **经济逻辑**：盈利公告后市场对好消息反应不足 → 漂移 60-90 天；分析师评级修正同理。
- **骨架**：`rank(change_*_revision)`、`subtract(rank(surprise), rank(uncertainty))`
- **KOR 实证**：ml_factor_proj rating_revision 上限 sh0.85（TVR 结构性 3-4% 不达标）→ 此类信号在 KOR D1 慢设置下 sharpe 天花板低，勿再投入配额。

### T7 情绪 / 关注度（情绪衰减）
- **经济逻辑**：散户情绪推高价格后衰减；新闻情绪半衰期 3-10 天。
- **骨架**：`rank(sentiment)` 水平、`ts_decay_linear(rank(sentiment),5)` 衰减加权
- **KOR 实证**：news_sentiment_transfer 判死（稀疏覆盖+CONCENTRATED_WEIGHT）。

### T8 事件驱动（可预期事件的定价偏差）
- **经济逻辑**：指数调仓/财报日/季节性事件的系统性定价偏差。
- **骨架**：`days_from_last_change(F)`（信息新鲜度：刚变化的信号信息量大）、`last_diff_value(F)`
- **算子**：days_from_last_change / last_diff_value（此前未用）

### T9 预期修正 / 预测共识（模型预测类数据集专用，当前 chart_cnn 主力）
- **经济逻辑**：把模型预测字段当作"分析师预期"处理——
  1. **多期限共识**：短期(40d)/中期(60d)/长期(100d)预测一致看涨 → 信念更强（等价于多分析师一致上调）；
  2. **置信度加权**：高概率 × 高置信度 = 期望收益，低置信度的高概率不可信；
  3. **预期利差**：最高分位概率 - 最低分位概率 = 预测分布的看涨偏度；
  4. **期限结构修正**：短期预测 rank - 长期预测 rank = 预期改善加速度（注意：这是截面结构差，不是时序动量，不违反"动量死"结论）。
- **骨架**：
  ```
  add(add(multiply(rank(F_40d),0.33),multiply(rank(F_60d),0.34)),multiply(rank(F_100d),0.33))
  multiply(rank(prob_high),rank(confidence))
  subtract(rank(prob_q5_bucket4),rank(prob_q2_bucket0))
  subtract(rank(F_short_horizon),rank(F_long_horizon))
  ```
- **KOR 实证基线**：单腿 rank(q4_bucket2_60d) SECTOR d6 t0.06 sh1.36/fit1.00；本主题目标 sh≥1.58。

### T10 行业相对 / 中性骨架（相对强度）
- **经济逻辑**：绝对水平含行业 beta；行业内相对预期/动量才是选股信息（101 #48-#100 一半以上用 indneutralize）。
- **骨架**：`group_rank(F, sector)`（行业内相对强度）、`group_neutralize(F, industry)`、行业相对溢价 = 字段层减行业均值
- **注意**：group_* 只接受裸字段，不接受嵌套表达式（wave10 v2 实证）
- **KOR 实证**：SECTOR 中性化设置对 chart_cnn 必需（STATISTICAL 全灭）；但表达式内 subindustry 细中性化退化（sh 1.36→1.19），用设置层中性化而非表达式层。

### T11 多因子加权集成（Alpha#36 范式 + 分散化提 Sharpe）
- **经济逻辑**：弱相关信号等权/加权组合 → 组合 Sharpe ≈ 单腿 × √N（分散化红利）；论文实证波动-收益 slope 0.76 → 适当保留组合波动。
- **骨架**：`add(multiply(rank(A),w1),add(multiply(rank(B),w2),multiply(rank(C),w3)))`，A/B/C 必须来自**不同信号源/不同期限/不同模型**（如 cnn + img + probability_rank 三源共识）。
- **禁忌**：`rank(add(...))` 会触发 CONCENTRATED_WEIGHT；组合腿之间相关>0.8 时等于单腿，无分散红利。

### T12 条件交易（regime switch）
- **经济逻辑**：信号只在特定状态有效（如只在置信度高时持仓、只在趋势确认后跟随）→ 减少无效交易提 Sharpe。
- **骨架**：`trade_when(x, greater(condition_field, threshold), 0)`、`if_else`
- **算子**：trade_when / if_else / greater / and / or（此前未用）；注意 TVR 下限 5%，条件太严会低于下限。

---

## 二、未用算子 × 经济用途速查（针对 16.9% 探索率的整改清单）

| 算子 | 经济用途 | 对应主题 |
|---|---|---|
| ts_corr / ts_covariance | 量价背离、信号一致性 | T3 |
| ts_std_dev | 噪声惩罚、波动因子 | T4 |
| ts_ir | 信号信息比（稳定性） | T4/T9 |
| ts_scale | 相对自身历史峰值位置 | T9 |
| ts_arg_max / ts_arg_min | 极值时点（新高距今=动量新鲜度） | T2/T8 |
| ts_sum / ts_product | 累积压力、复合收益 | T1/T2 |
| ts_quantile / ts_regression | 历史分位、趋势斜率 | T2/T9 |
| bucket | 离散分层降噪（整数化防权重集中） | T9 |
| trade_when / if_else | 条件交易 | T12 |
| group_rank / group_mean / group_zscore | 行业相对强度 | T10 |
| days_from_last_change / last_diff_value | 信息新鲜度 | T8 |
| sqrt / log / inverse | 非线性压缩/反转（bounded 字段慎用 inverse） | 通用 |
| winsorize / zscore / normalize / scale | 截面整形（bounded 字段跳过 winsorize） | 通用 |
| sign / abs / max / min | 方向提取、包络（101 #71-99 max/min 双 decay 因子） | T1/T4 |
| vec_* 系列 | VECTOR 数据集聚合（ai_equity_alpha 专用） | — |

## 三、KOR/D1 白名单 × 主题适用表（截至 2026-08-14）

| 数据集 | 状态 | 适用主题 |
|---|---|---|
| chart_cnn_alpha | **主攻中**（wave11/12） | T9 预期共识/置信加权、T10、T11、T12 |
| multi_source_model | PROD 墙死（PC 0.79-0.87） | 勿用 |
| ml_factor_proj / pattern_scores / price_signal_dl / ai_factor_transfer / predictive_starmine / news_sentiment_transfer / ai_equity_alpha / acquisition_model | 判死 | 勿用 |
| 白名单其余未探数据集 | 待探 | 先健康检查再按本库选主题 |

## 四、模板设计自查清单（提交前）

1. 能一句话说清经济逻辑吗？（谁在交易/为什么 edge 持续）
2. 字段是 bounded 概率值吗？→ 跳过 winsorize/log 负值风险，优先 rank/quantile/bucket
3. 慢信号（模型预测）吗？→ 禁用时序动量腿，用截面结构与多期限组合
4. 组合腿相关性估计 <0.8 吗？（同源同期限=假分散）
5. 新算子引入一次最多 2-3 个，变量隔离便于归因
6. 设置层中性化优先于表达式层（chart_cnn 实证）

---
*创建 2026-08-14，KOR/D1 战役 wave12；随每 10 轮多样性评估迭代本库*
