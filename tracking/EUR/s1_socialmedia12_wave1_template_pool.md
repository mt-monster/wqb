# s1_socialmedia12 wave1 模板池（EUR / TOP2500 / D1 · REGULAR ATOM）

> 目标：点亮 **SOCIALMEDIA 塔（EUR D1 0/3，全区唯一 0/3 且仅剩 1 个数据集未画像）**。
> 数据集：`socialmedia12`（cov 0.7836，aC 2471，uC 827）。均为单数据集 ATOM，不占任何两塔组合配额。
> 落盘时间：2026-11-06。

## 一、字段画像（MCP `get_datafields` 实测，4 个可见字段）

| 字段 | 类型 | cov | aC | 语义 | 定位 |
|---|---|---:|---:|---|---|
| `scl12_sentiment` | MATRIX | 0.85 | 912 | 社媒情绪水平 | **主信号** |
| `scl12_buzz` | MATRIX | 0.85 | 884 | 相对情绪**量/关注度** | **主信号（关注度轴）** |
| `entity_profile_summary` | VECTOR | 0.75 | 157 | 公司简介文本 | 元数据，不可用 |
| `entity_sector_name` | VECTOR | 0.75 | 151 | 行业文本分类 | 元数据，分组轴替代品 |

★ 二元结构 = **情绪（tone）× 关注度（volume）**，与 Barber-Odean 注意力、Da-Engelberg-Gao (FEARS)、Tetlock 媒体悲观三条文献主线一一对应。aC 884/912 属中高拥挤，但远低于 pv1(373943)/analyst69(184267)。

## 二、论坛 + 文献取证

**论坛 `41858767008279`（《SocialMedia数据集实战指南》，QW94165，2026-07-10，44 票，3 评论）** 七条可迁移结论：
1. ★ **SocialMedia 金字塔倍率 = 1.5（全区最高档之一，与 Sentiment / News 并列）** ⇒ 点亮它的积分效率是普通塔的 1.5 倍，战略优先级高于继续在同一塔内加件。
2. ★★ **社媒信号半衰期只有几天，`ts_rank(·,252)` 等价于慢趋势、会抹掉核心信号**；正解 = `ts_mean(·,5)` + `ts_decay_linear(·,10)`，作者报 **IC 约为 252 版本的 2 倍**。
3. **覆盖稀疏**：先 `ts_backfill` 回填再进时序算子；回填宽度是「覆盖 ↔ 陈旧信号」的两点权衡，不是越宽越好。
4. ★★★ 评论者 XZ17517：**跨数据集组合用加法/加权平均，不要用乘积**——「两个稀疏字段的乘积覆盖≈交集，覆盖会塌一半；加法至少保留单腿覆盖」。⇒ **本条独立佐证了我们 `add(multiply(k,rank A), rank B)` 合成配方的正确性**（§276 跨厂商合成成功的第三种解释）。
5. **符号风险**：社媒情绪可能是零售注意度的**滞后**指标，OS 上方向可能反转 ⇒ 上模拟前用新闻/价格做符号一致性确认。
6. 推荐设置：neutralization **Industry**、decay 3–10、truncation 偏低（0.01 档）、**D1 比 D0 干净**。
7. 噪音去极值：先 `winsorize` 或 `ts_zscore` 再 `rank`，不要直接 rank 原始情绪值（0 值与极端值会主导排序）。

**外部文献先验（前序轮已取证，复用不自造）**：
- Tetlock (2007, JF)：媒体悲观 → 短期下行压力 → 随后回归基本面 ⇒ 情绪方向系数**短多长空**。
- Da-Engelberg-Gao (FEARS)：异常关注度上升 → 短期上涨、随后 1–2 年反转 ⇒ **buzz 长窗异常度取反向**。
- 「社交搅动假说」（论坛 `29160454156567`，StockTwits + 家庭交易数据）：社会连结度高 ⇒ 新闻更快入价，但**意见分歧与过度交易**上升 ⇒ **buzz 的二阶矩（分歧度）取反向**。

## 三、12 个结构互异模板（骨架/算子几何/矩/分组轴/非线性五维互异，非同骨架换窗口）

时间窗全部取有意义值：**5 = 周、22 = 月、63 = 季、66 = 季（含缓冲）、252 = 年**。

| # | 结构轴 | 表达式 | 算子数 | 经济含义 |
|---|---|---|---:|---|
| T01 | 水平·慢基线异常度 | `group_rank(ts_zscore(ts_backfill(scl12_sentiment,22),252),industry)` | 3 | 情绪相对自身年度基线的偏离 |
| T02 | 快几何·短平滑+线性衰减（论坛结论 2 直译） | `ts_decay_linear(group_rank(ts_mean(ts_backfill(scl12_sentiment,22),5),industry),10)` | 4 | 5 日情绪均值，10 日线性衰减保留「快」 |
| T03 | 一阶差分·关注度冲击 | `group_rank(ts_delta(ts_backfill(scl12_buzz,22),5),industry)` | 3 | 周度 buzz 突增 = 注意力事件 |
| T04 | 一阶差分反向·注意力反转（FEARS 直译） | `-group_rank(ts_zscore(ts_backfill(scl12_buzz,22),252),industry)` | 3 | 年度异常高关注 → 后续反转下行 |
| T05 | 双字段同号加成（加法，非乘积） | `add(group_rank(ts_zscore(ts_backfill(scl12_sentiment,22),252),industry),group_rank(ts_zscore(ts_backfill(scl12_buzz,22),252),industry))` | 6 | 情绪与关注度同时抬升的「热点共振」 |
| T06 | 快慢错配（同字段双窗差） | `group_rank(subtract(ts_mean(ts_backfill(scl12_sentiment,22),5),ts_mean(ts_backfill(scl12_sentiment,22),66)),industry)` | 6 | 短期情绪相对季度基线的突变 |
| T07 | 二阶矩·意见分歧（社交搅动假说直译） | `-group_rank(ts_std_dev(ts_backfill(scl12_buzz,22),22),industry)` | 3 | buzz 波动 = 分歧度 → 过度定价 → 做空 |
| T08 | 比率·单位关注度的情绪浓度 | `group_rank(divide(ts_mean(ts_backfill(scl12_sentiment,22),22),ts_mean(ts_backfill(scl12_buzz,22),22)),industry)` | 6 | 排除「量」只看「浓度」，天然抗 buzz 规模漂移 |
| T09 | 非线性·符号保留压缩 | `signed_power(group_rank(ts_zscore(ts_backfill(scl12_sentiment,22),252),industry),0.5)` | 4 | 平方根压缩极值，治 CONCENTRATED_WEIGHT |
| T10 | 时序分位（秩形式，非 z-score） | `group_rank(ts_rank(ts_backfill(scl12_sentiment,22),63),industry)` | 3 | 季度内情绪分位，抗分布漂移 |
| T11 | 事件门控（`trade_when`） | `trade_when(ts_delta(scl12_buzz,5)>1,group_rank(ts_zscore(ts_backfill(scl12_sentiment,22),66),industry),-1)` | 4 | 仅在 buzz 突增日调仓，其余日持有 |
| T12 | 分组轴替换（更细粒度） | `group_rank(ts_zscore(ts_backfill(scl12_buzz,22),66),subindustry)` | 3 | buzz 异常度的子行业内相对位置 |

全部算子数 **3–6 ≤ 12**；无禁用字段、无 vector 算子（两主字段为 MATRIX）。

## 四、设置档（论坛推荐 vs 本项目已验证）
- 论坛推荐：neutralization **Industry**、decay 3–10、trunc 0.01、D1。
- 本项目第 1 批实际派发（`GV1W3ea4huaos1aQ9qnuKp`）：**SLOW_AND_FAST / decay 8 / trunc 0.08 / maxTrade ON / nan ON / pasteurization ON / unit VERIFY** —— 沿用 §276 出货档，作为**基线**。
- ⇒ 下一批起做**单变量对照**：只把 neutralization 换成 `INDUSTRY`、trunc 降到 `0.01`，验证论坛「Industry + 低 trunc」是否优于基线。

## 五、执行进度
| 批次 | multisim | 模板 | 状态 |
|---|---|---|---|
| 第 1 批 | `GV1W3ea4huaos1aQ9qnuKp` | T01（情绪水平异常度）+ T03（buzz 冲击） | 在飞 |

## 六、纪律
- 每批恰好 2 条、批级设置单一、过三闸（validate / 字段存在性 / 算子 ≤12）后派发。
- 判死须「同一面 ≥6 个结构互异模板全灭」；当前 0/12 已测，不得提前判 socialmedia12。
- 按模板编号归因，不按单条归因。
- SOCIALMEDIA 塔 0/3 ⇒ 需要 3 颗合格件才点亮，属中长期目标；但 1.5× 倍率使其**积分效率最高**，值得持续投入。
