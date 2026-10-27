# USA · news_sentiment_transfer「新闻情绪迁移」字段画像与机制台账（2026-10-20）

> 数据集归属：**USA / D1 / SENTIMENT 塔（未点亮；本季 USA/D1 点亮的是 model=4 / analyst=5 / earnings=1）**。
> 选用理由：`get_datasets(category="sentiment")` 实测 **23 字段 / coverage 0.947 / alphaCount 180 / 0 条回测**，
> 是剩余未点亮池里「非判死 + 低拥挤 + 字段语义完整」的首选；同塔 `news_sentiment_dl`、`ai_news_scores`、
> `event_sentiment_signals`、`earningscall_embed`、`sentiment21`、`mmp_nlp_sentiment` 均已判死/判弱
> （见交付日志 §2 判死表），故本集**不能复用它们的「原始情绪水平」模板**，只做变化 / 分歧 / 关注度条件。
>
> 平台元数据（`get_datafields`，2026-10-20）：23/23 字段可见，`sharpe_filter_removed=0`；
> MATRIX 20 + VECTOR 3；全部字段 coverage = **0.947**。

## 1. 类别级定位（sentiment 塔，USA/D1）

| 数据集 | 字段 | cov | aC | 裁定 | 依据 |
|---|---:|---:|---:|---|---|
| `news_sentiment_transfer` | 23 | 0.947 | **180** | **★ 本波主攻** | 0 回测；语义覆盖「情绪水平 / 分歧 / 偏度 / 关注度」四类，字段池小而全 |
| `news_transformer_scores` | 315 | 0.7773 | 292 | 备选 | 字段池大但 cov 低，需先做覆盖筛选 |
| `other553`（Financial Opinion Mining） | 74 | 0.7386 | 525 | 备选 | 财报电话/新闻/社媒混合观点 |
| `sentiment22` / `sentiment23` | 210 / 210 | 0.999 | 525 / 934 | ⚠ 备选 | 同族 `sentiment21` 已判死 ⇒ 必须先 8 探针 |
| `sentiment26`（网站流量） | 36 | 0.8532 | 983 | 备选 | 另类数据，VECTOR 为主 |
| `news_sentiment_dl` / `ai_news_scores` / `event_sentiment_signals` / `earningscall_embed` / `sentiment21` / `mmp_nlp_sentiment` | — | — | — | ✗ 判死/判弱 | 见交付日志 §2 |

> 同塔判死证据的共性：**原始情绪水平（level）在 USA 没有全期截面 alpha**（max |S| 0.48–0.63）。
> 本集若重复 level 模板，预期同样死；本波的设计约束是「level 只作对照，主信号必须含变化 / 分歧 / 条件」。

## 2. 字段画像（23 字段全表）

> 列：字段 · 类型 · cov · uC · aC · 家族 · 含义。家族分类按 `brain-alpha-research-news-sentiment` §2
> 的 5 家族规则（direction / attention / dispersion / event_type / peer_context）；本集无 event_type / peer_context。

| 字段 | 类型 | cov | uC | aC | 家族 | 含义 |
|---|---|---:|---:|---:|---|---|
| `news_article_count` | MATRIX | 0.947 | 20 | 50 | attention | 实体相关新闻文章总数 |
| `normalized_news_article_count` | MATRIX | 0.947 | 7 | 12 | attention | 跨实体可比的文章数（归一化） |
| `primary_sentiment_average` | MATRIX | 0.947 | 9 | 16 | direction | 主情绪分均值 |
| `primary_sentiment_maximum` | MATRIX | 0.947 | 5 | 5 | direction | 主情绪分最大值 |
| `primary_sentiment_middle_value` | MATRIX | 0.947 | 5 | 6 | direction | 主情绪分中位数 |
| `primary_sentiment_minimum` | MATRIX | 0.947 | 6 | 9 | direction | 主情绪分最小值（最负一篇） |
| `primary_sentiment_skewness_2` | MATRIX | 0.947 | 3 | 3 | dispersion | 主情绪分偏度 |
| `primary_sentiment_total_2` | MATRIX | 0.947 | 2 | 2 | direction | 主情绪分总和 |
| `secondary_sentiment_average` | MATRIX | 0.947 | 5 | 6 | direction | 副情绪分均值 |
| `secondary_sentiment_maximum` | MATRIX | 0.947 | 2 | 2 | direction | 副情绪分最大值 |
| `secondary_sentiment_middle_value` | MATRIX | 0.947 | 2 | 2 | direction | 副情绪分中位数 |
| `secondary_sentiment_minimum` | MATRIX | 0.947 | 2 | 13 | direction | 副情绪分最小值 |
| `secondary_sentiment_skewness_2` | MATRIX | 0.947 | 2 | 2 | dispersion | 副情绪分偏度 |
| `secondary_sentiment_total_2` | MATRIX | 0.947 | 3 | 25 | direction | 副情绪分总和 |
| `sentiment_distribution_skewness_2` | MATRIX | 0.947 | 3 | 3 | dispersion | 全部情绪分的分布偏度 |
| `sentiment_score_average` | MATRIX | 0.947 | **12** | **12** | direction | 综合情绪均分（本集主字段） |
| `sentiment_score_maximum` | MATRIX | 0.947 | 2 | 2 | direction | 综合情绪最高分 |
| `sentiment_score_median` | MATRIX | 0.947 | 2 | 2 | direction | 综合情绪中位数 |
| `sentiment_score_minimum` | MATRIX | 0.947 | 4 | 5 | direction | 综合情绪最低分 |
| `total_sentiment_score` | MATRIX | 0.947 | 3 | 8 | direction | 情绪分总和 |
| `news_sentiment_score` | VECTOR | 0.947 | 4 | 4 | direction | 文章级综合情绪值（需 `vec_*`） |
| `primary_sentiment_value` | VECTOR | 0.947 | 5 | 13 | direction | 文章级主情绪值（需 `vec_*`） |
| `secondary_sentiment_value` | VECTOR | 0.947 | 0 | **0** | direction | 文章级副情绪值；**零使用、零 alpha**，本波不用 |

**画像六问**

1. **是什么**：把新闻文章级情绪聚合成「实体-日」面板——主/副两套情绪模型 + 综合分 + 文章数；
   另保留 3 个文章级 VECTOR 供自定义聚合。
2. **类型**：20/16 为 MATRIX；3 个 VECTOR（本波锁定 MATRIX 主线，VECTOR 留作下一波）。
   情绪分是有界标量（按同类新闻集惯例为 [-1, 1] 或 [0, 1] 区间），文章数是计数量（右偏）。
3. **覆盖**：23/23 全为 **0.947**（同一实体掩码），远高于 `news_transformer_scores` 的 0.7773；
   不需要 backfill 才能过 CW。但新闻覆盖的「有新闻才有值」特性意味着**平静期可能是 NaN 而非 0**——
   必须用 `ts_backfill` 或 `nanHandling=ON`，不能把缺失当「中性 0」。
4. **更新**：日频（新闻流每日聚合）；`*_skewness_2` / `*_total_2` 在文章数少时抖动大。
5. **分布**：情绪均分近似有界对称；`maximum` / `minimum` 是极值统计（对单篇文章敏感）；
   `total_*` 随文章数缩放；`*_skewness_2` 无量纲但厚尾；`news_article_count` 强右偏。
   ⇒ 主信号只用**均分/中位数/极值差/偏度**，`total_*` 必须除以 count 才有跨股可比性。
6. **拥挤**：字段级 aC 2–50，全集中位 ~6；`sentiment_score_average` 最高 12，`news_article_count` 50。
   同塔判死集的 aC 远高于此，本集属**低拥挤白地**。但「低 aC」也可能是「没人挖出过」——用 8 探针验证，
   不因低 aC 直接扩批（交付日志 §2 的判死表已证明 aC 低 ≠ 有信号）。

## 3. 适用模板（按体征）

| 体征 | 模板 | 字段 | 说明 |
|---|---|---|---|
| 有界情绪标量 | **变化**：`ts_av_diff(x, 22)` / `ts_delta(x, 22)` | `sentiment_score_average` / `primary_*_average` / `secondary_*_average` | 主信号；level 只作对照 |
| 有界情绪标量 | **意外**：`ts_zscore(x, 252)` | 同上 | 相对自身历史的标准化；与 analyst #7 的 SUB 修法同源 |
| 极值统计 | **分歧**：`maximum − minimum` → 负向 | `sentiment_score_*` / `primary_*` | Miller (1977)：分歧大 → 未来收益低 |
| 偏度 | **尾部不对称**：`−1 * skewness` | `sentiment_distribution_skewness_2` / `primary_*_skewness_2` | 正偏 = 乐观尾部 → 彩票偏好，负向 |
| 计数 | **关注度冲击**：`ts_delta(count, 22)` → 负向 | `news_article_count` / `normalized_*` | Barber & Odean (2008)：注意力 → 过度定价 |
| 两套情绪模型 | **模型分歧**：`primary − secondary` → 负向 | `primary_sentiment_average` / `secondary_sentiment_average` | 测量分歧 = 不确定性 |
| 均值/中位数 | **右尾偏斜**：`average − median` → 负向 | `sentiment_score_average` / `sentiment_score_median` | 少数极端正新闻主导 |
| 极值下尾 | **坏消息尾部**：`minimum` 正向 | `sentiment_score_minimum` | 最负一篇不极端 = 尾部风险低 |
| 关注度 × 方向 | **事件条件**：`trade_when(attention 异常, direction, …)` | attention + direction | 需先验证 attention 字段有截面差异；本波未上 |

**禁用**：裸情绪水平（同塔六次判死已证）；`total_*` 不除 count；`secondary_sentiment_value`（0 用户 0 alpha，
信息不可用）；把 `maximum`/`minimum` 当稳健信号（单篇文章驱动）。

## 4. 机制台账（批 1：N01–N08）

设置：**EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / maxTrade OFF /
pasteurization ON / unitHandling VERIFY / nanHandling ON / language FASTEXPR**（同 option3 批次，可比）。

通用壳：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`。

| # | 机制 | 字段 | 方向 | SIG | 经济含义 / 文献 |
|---:|---|---|---|---|---|
| N01 | 情绪动量（1M 变化） | `sentiment_score_average` | 正 | `ts_av_diff(sentiment_score_average, 22)` | Tetlock (2007)：语气改善 → 短期正漂移 |
| N02 | 情绪水平位置（252 日 z） | `sentiment_score_average` | 正 | `ts_zscore(sentiment_score_average, 252)` | 水平对照 + 自归一；若 level 族死，本条的 2Y 会分化 |
| N03 | 情绪分歧（极差） | `sentiment_score_maximum − minimum` | 负 | `-1 * (maximum - minimum)` | Miller (1977)：分歧 → 高估 → 低收益 |
| N04 | 情绪分布偏度 | `sentiment_distribution_skewness_2` | 负 | `-1 * skewness_2` | 正偏 = 乐观尾部/彩票偏好 → 负 |
| N05 | 关注度冲击（文章数 Δ22） | `news_article_count` | 负 | `-1 * ts_delta(news_article_count, 22)` | Barber & Odean (2008)：注意力驱动的净买入 → 后续低收益 |
| N06 | 主/副模型分歧 | `primary_sentiment_average − secondary_sentiment_average` | 负 | `-1 * (primary - secondary)` | 测量分歧 = 不确定性折价 |
| N07 | 均值−中位数（右尾） | `sentiment_score_average − sentiment_score_median` | 负 | `-1 * (average - median)` | 少数极端正新闻主导 → 乐观尾部 |
| N08 | 负向尾部（最负一篇） | `sentiment_score_minimum` | 正 | `sentiment_score_minimum` | 尾部风险：最负一篇越不极端，未来收益越高 |

**正交性**：N01/N02 同字段（变化 vs 水平 z，互为对照，不同时进最终交付）；N03 极差、N04 分布偏度、
N05 关注度、N06 双模型、N07 均值中位数、N08 负尾——六种不同几何。N02 与 N07 都涉及平均值但参照不同
（自身历史 vs 中位数），仍属不同机制。
**同族配额**：direction 6 条、attention 1 条、dispersion 2 条（N03 用 direction 字段构造，归 dispersion 桶）；
下一批补 VECTOR 聚合与 attention 条件，不重复本批字段。
**机制模板不封顶 8 个**：本批只是 multisim 容量；N09–N14 已登记待测（见 §4.1）。

### 4.1 待测机制（N09–N14，后续批）

| # | 机制 | 字段 | 先验 |
|---:|---|---|---|
| N09 | 副情绪动量 | `secondary_sentiment_average` Δ22 | 与 N01 独立模型；若 N01 有信号而 N09 无，说明主模型独有 |
| N10 | 关注度加权情绪 | `sentiment_score_average * ts_rank(news_article_count, 252)` | 事件条件：高关注日情绪更定价 |
| N11 | 主情绪偏度 | `−primary_sentiment_skewness_2` | 与 N04 对照（主模型 vs 综合） |
| N12 | 副情绪负尾 | `secondary_sentiment_minimum` | 与 N08 对照 |
| N13 | VECTOR 聚合动量 | `vec_avg(news_sentiment_score)` Δ22 | 文章级原始值 vs 预聚合均分 |
| N14 | 文章级分歧 | `vec_stddev(primary_sentiment_value)` | 直接测文章间分歧（比 max−min 稳） |

**发批规则**：每批只取未测机制的代表字段；N01/N02 二选一作主线后再扩批，不把 8 条当机制上限。

## 5. 回测结果及指标（批 1）

**发批**：multisim `3guqcK8Mc4RzbyvKSCwD26z`（8 条，设置同上；2026-10-20 发批，8/8 COMPLETE，0 error）。

| # | 机制 | alpha | S | F | 2Y | SUB | TO | 收益 | risk-neut | 判读 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| N01 | 情绪动量 Δ22 | 3qjeaNPe | 0.23 | 0.05 | −0.73 | 0.44 | 1.02% | 0.71% | −0.23 | 动量无信号 |
| N02 | 水平 z252 | MP0LKrzz | 0.50 | 0.16 | −0.47 | 0.66 | **0.98% fail** | 1.36% | 0.03 | 水平对照也弱，且 TO 挂 |
| N03 | 极差分歧 | mLYVrv19 | −0.30 | −0.10 | −0.95 | −0.29 | 1.14% | −1.42% | −0.17 | 反向更差（方向反了） |
| N04 | 分布偏度 | RRA12gKa | −0.33 | −0.10 | −0.96 | −0.02 | 1.18% | −1.23% | −0.34 | 反号后仍无信息（残差负） |
| N05 | 关注度 Δ22 | WjLVa50O | 0.41 | 0.12 | 0.22 | 0.57 | 2.32% | 1.07% | −0.35 | 关注度最弱家族 |
| N06 | 双模型分歧 | kqJZ1AO6 | 0.49 | 0.16 | 0.17 | 0.38 | **0.98% fail** | 1.37% | 0.03 | 与 N02 几乎同收益 ⇒ 信息同源 |
| N07 | 均值−中位数 | qME6PRV1 | 0.34 | 0.09 | 0.64 | **0.98 PASS** | **0.96% fail** | 0.92% | 0.12 | SUB 好但 TO 挂、S 低 |
| N08 | 负向尾部 | xA1dPZ5m | −0.38 | −0.14 | −1.32 | −0.23 | 1.06% | −1.82% | −0.36 | 尾部方向反（越负越好） |

**批 1 归因（四条）**：

1. **全族无 S≥0.5**：8 条覆盖 direction 变化 / level / dispersion / attention 六个几何，最高 N02=0.50，
   且 2Y 有 4 条为负 ⇒ 不是「某个机制没调好」，而是本集的日频新闻情绪在 USA 全期**没有截面 alpha**。
2. **反号检验已隐含**：N03/N04/N08 原方向为负 S，说明正向（不取负）会更差（N08 正向 S=−0.38 ⇒ 原负向构造
   也是 −0.38，二者对称），即这些几何**双向都无信息**，不是方向写反。
3. **TO 陷阱显形**：N02/N06/N07 的 TO 0.96–0.98% 全部卡 LOW_TURNOVER（<1%）。日频情绪聚合经 252 backfill
   后几乎静态——与 §7 预判一致，不是可磨的壳问题。
4. **N06 ≡ N02 信息同源**：双模型分歧收益 1.37% ≈ 水平 z 的 1.36%，说明 primary/secondary 两套模型高度相关，
   该字段不提供独立维度。

**批 2（已收，2026-10-20）**：multisim `1rQhNb3h34r7brsxRPofznq`，8 条，设置同批 1，8/8 COMPLETE。

| # | 构造 | alpha | S | F | 2Y | SUB | TO | 收益 | risk-neut |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| N13-1 | `ts_av_diff(vec_avg(news_sentiment_score),22)` | `rKdPbLw3` | 0.23 | 0.05 | −0.73 | 0.44 | 1.02% | 0.70% | −0.23 |
| N13-2 | `ts_zscore(vec_avg(news_sentiment_score),252)` | `6XAeR1QP` | 0.50 | 0.16 | −0.47 | 0.66 | **0.98% fail** | 1.36% | 0.03 |
| N14-1 | `−vec_stddev(primary_sentiment_value)` | `N1eRn6Gp` | −0.36 | −0.12 | −1.07 | −0.21 | 1.12% | −1.42% | −0.30 |
| N14-2 | `−vec_stddev(news_sentiment_score)` | `npA8nold` | −0.38 | −0.13 | −1.10 | −0.22 | 1.12% | −1.48% | −0.28 |
| N14-3 | `−ts_av_diff(vec_stddev(primary_sentiment_value),22)` | `mLYVqAN1` | 0.06 | 0.01 | −0.60 | 0.21 | 1.02% | 0.16% | −0.24 |
| N10-1 | `trade_when(ts_rank(count,252)>0.8, ts_av_diff(avg,22), −1)` | `LL5dn6wv` | −0.04 | 0.00 | −0.51 | 0.15 | **0.89% fail** | −0.10% | −0.47 |
| N10-2 | `ts_rank(avg,252)*ts_rank(count,252)` | `rKdPbLM3` | 0.19 | 0.04 | −0.60 | 0.44 | 1.00% | 0.58% | −0.09 |
| N10-3 | `−ts_rank(max−min,252)*ts_rank(count,252)` | `6XAeR1LP` | 0.33 | 0.09 | 0.05 | 0.15 | 1.00% | 0.88% | −0.18 |

**批 2 归因（写死）**：

1. **全部 8 条 S<1.0（最高 0.50）⇒ 命中预注册止损：本集封存，不再投第 3 批。**
   16 条探针（8+8）跨 direction 水平/变化/分歧、VECTOR 文章级聚合、attention 门控五种测量面，
   S 上限 0.50，且 **2Y 有 6 条为负** ⇒ 日频新闻情绪在 USA 全期与近期都没有截面 alpha。
2. **VECTOR 聚合与预聚合完全等价**：N13-1≡N01（0.23/0.23）、N13-2≡N02（0.50/0.50）、
   N14-1≈N03（−0.36/−0.30）⇒ `vec_avg`/`vec_stddev` 只是同一信息的另一种聚合，
   **VECTOR 不是新的信息维度**。这条可复用到同塔其它数据集：先看预聚合字段是否已覆盖，再决定是否上 vec_*。
3. **attention 门控无效且伤 TO**：N10-1 用 `trade_when` 把 TO 压到 0.89%（挂 LOW_TURNOVER）且 S=−0.04；
   N10-2/N10-3 的秩乘积也只是把 S 拉到 0.19/0.33 ⇒ 关注度在 USA 不提供条件 alpha。
4. **risk-neut 全为负或≈0**：即使最强的两条（N13-2 0.03、N10-2 −0.09）也没有非风格收益
   ⇒ 按 `risk_neutralized_sharpe<0.3` 判死口径，本集**连风格 beta 都不值得占用仿真配额**。

**§5.1 封存结论（2026-10-20）**：`news_sentiment_transfer` 判 **weak / 封存**，
`seal_dead_end` 建议 entry_id `USA-NEWS-SENTIMENT-TRANSFER-WEAK`；
证据 = 16 probes / max S 0.50 / 2Y 6 条为负 / risk-neut ≤0.03。
同塔已有 5 个判死集（`news_sentiment_dl` / `ai_news_scores` / `sentiment21` / `event_sentiment_signals` / `earningscall_embed`）
⇒ **情绪类“文本分数”家族在 USA/D1 结构性无 alpha**，后续 sentiment 塔只应考虑 `sentiment26`（网站流量，非文本分数）
与 `board_gov_stats`/`insiders4` 这类非文本集；`news_transformer_scores` / `other553` 同属文本分数，**降级为不再优先**。

**预注册判据（写死）**：

- 任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 且 fail=0 ⇒ 立即 `check_correlation(refresh=True)` 做 prod/self 双端点（<0.7）。 <!-- from config.prod_corr_max -->
- 只过 1–2 闸 ⇒ 先按家族归因（direction 变化 / dispersion / attention 分组看 S 排序），再决定批 2 方向；不得直接换字段。
- **全部 S<1.0 ⇒ 判「本集水平/变化族无截面 alpha」**，批 2 转 VECTOR 文章级分歧（N13/N14）与 attention 条件（N10）；
  若批 2 仍 <1.0 且总量价也无 ≥1.2 ⇒ 判本集弱，按止损换集（候选：`news_transformer_scores` / `board_gov_stats`）。
- TO<1% 的候选先跑去壳诊断批确认非静态，再谈判死（新闻信号的常见陷阱）。

## 6. 论坛/文献证据（可复用）

1. **Tetlock (2007), Giving Content to Investor Sentiment**：媒体语气对个股收益有短期预测力，
   但**水平**信号衰减快、易被定价；应以**变化/意外**为主。
2. **Tetlock, Saar-Tsechansky & Macskassy (2008)**：负面词汇比例对盈利与收益有增量信息；
   负向尾部（N08）比均值更稳。
3. **Miller (1977)**：意见分歧 + 卖空约束 → 高估 → 未来低收益；N03/N06/N14 的分歧机制来源。
4. **Barber & Odean (2008)**：注意力驱动的买入 → 短期过度定价；N05/N10 的来源。
5. **Baker & Wurgler (2006)**：情绪在横截面上有条件效应，不是无条件水平 alpha；支持「条件/分歧」而非裸水平。
6. **同塔内部证据（必读）**：`news_sentiment_dl`（10 probes max 0.63）、`ai_news_scores`（8 probes max |S| 0.48）、
   `sentiment21`（max |S| 0.58 + HIGH_TURNOVER 1.44–1.58）、`mmp_nlp_sentiment`（24 回测 0 ra_clean）
   ⇒ **本集不得重复「原始情绪水平」模板**；本波把 level 只作 N02 对照。

## 7. 风险与预判

- **同塔判死阴影**：六次 level 模板失败 ⇒ 若 N01/N02 都 <1.0，优先怀疑「本集只是另一套情绪 level」，
  按 §5 的止损路径转 VECTOR/attention，不磨壳。
- **稀疏新闻日**：coverage 0.947 是实体掩码，不代表每天有新闻；`ts_backfill(252)` 必要，
  但会把平静期信号拉平 → 若 TO<1%，先确认是不是 backfill 造成静态。
- **极值字段不稳**：`maximum`/`minimum`/`skewness_2` 由单篇/少数文章驱动，`winsorize(std=4)` 必须保留；
  不建议对它们做长窗 mean。
- **ATOM 合规**：本批 8 条全部只引用本数据集字段；分组轴 `industry` 属六豁免字段，合规。
- **拥挤**：aC 2–50 很低，但低 aC 不等于有 alpha（同塔反例）；按预注册判据走，不因低 aC 扩批。
- **机制上限**：本集 23 字段、8 条只是第一轮；N09–N14 与 VECTOR 两段式聚合尚未测，
  不得在批 1 后就宣称「数据集挖尽」。
