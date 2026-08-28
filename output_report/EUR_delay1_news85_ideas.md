# EUR D1 news85 特征工程（S1 standalone）

**Dataset**: news85
**Region**: EUR
**Delay**: 1


- region: EUR · universe: TOP2500 · delay: 1
- dataset: `news85`（News Sentiment Analysis using DNN）
- 白名单校验：在 `s0_whitelist` tier1（score 0.7412，cov 0.823，23 字段，ac=253）
- data_type：MATRIX 众数（20 MATRIX + 3 VECTOR）；VECTOR 必须先 `vec_*`
- 生成设置主轨：COUNTRY / decay 6 / truncation 0.08 / maxTrade ON
- 正交动机：EUR/D1/MODEL（starhold/m238/FCF-to-price）prod 墙 0.85–0.94；本集是新闻 DNN 情绪，不是 IBES 价格面板，也不是 emotion 标签族

## 1. 数据集理解

平台描述：用神经网络把一套新闻情绪（tr_trna_eq 标题）迁移到另一套标题（ravenpack_web_v2）。EUR 上同时给出：

- **日度 MATRIX 聚合**：覆盖率 0.8387，已按实体把事件压成截面（总量/均值/极值/偏度/标题数）
- **事件级 VECTOR 原分**：覆盖率 0.7182，一条新闻一行，必须 `vec_avg`/`vec_sum` 再进常规算子

要点：

1. 名字像 analyst，实际是 **新闻情绪迁移**，与 `analyst_earnings_ibes`（该集在 EUR 实为 OHLC/回报面板，returns 反转族 prod 0.95 墙）无关。
2. `news_sentiment_nlp` / `news_sentiment_dl` 已 RED（TOP800 探针 |S|<0.3）。本集有 **MATRIX 聚合层**，不是再挖同一 NLP 裸探针。
3. 覆盖 0.72–0.84：生成必须 `ts_backfill(66)` 或 `ts_backfill(120)`，禁止裸 winsorize 稀疏事件。
4. 情绪分有界，计数为非负整数：有界跳过 winsorize；整数用 rank/bucket，不用 `ts_mean`。
5. 跨区铁律 `GLB-EMOTION-DEAD` 针对 emotion 标签前缀，不自动判死 news85；但仍禁止再磨拥挤的「裸 rank(情绪均值)」。

## 2. 字段解构

### 2.1 MATRIX 聚合（cov≈0.8387）

| 字段 | 测什么 | 预处理 |
|---|---|---|
| `aggregate_sentiment_total` | 窗口内情绪分之和（流量×极性） | backfill+rank |
| `sentiment_overall_average` | 窗口内平均极性 | backfill+rank（有界，禁 winsorize） |
| `sentiment_overall_median` | 中位极性，抗单条爆文 | backfill+rank |
| `sentiment_overall_minimum` | 最差一条（左尾风险） | backfill+rank |
| `peak_sentiment_value` | 最好一条（右尾） | backfill+rank |
| `sentiment_distribution_skewness` | 极性分布不对称 | backfill+rank |
| `headline_item_count` | 标题条数（注意力） | backfill+rank/bucket |
| `normalized_headline_count` | 相对常态的注意力 | backfill+rank |
| `sentiment1_*` | 第一套情绪（总量/均/偏/高/低/中位） | 同族，选均/偏/尾，勿 6 字段全堆 |
| `sentiment2_*` | 第二套迁移情绪 | 与 sentiment1 互补；`sentiment2_lowest_score` 竞争最高（ac=26） |

### 2.2 VECTOR 原分（cov≈0.7182）

| 字段 | 测什么 | 预处理 |
|---|---|---|
| `mws85_sentiment` | 单条新闻情绪 | `vec_avg` → backfill+rank |
| `sentiment1_raw_score` | 第一套原始分 | 同上 |
| `sentiment2_raw_score` | 第二套原始分 | 同上 |

时间戳/标题文本不进 FASTEXPR。

## 3. 问题驱动特征

### 3.1 不变（稳定性）
- **共识稳定**：`ts_std(ts_backfill(sentiment_overall_median, 66), 66)` 低 = 叙事稳定。实现：`rank(subtract(0, ts_std(ts_backfill(sentiment_overall_median, 66), 66)))`

### 3.2 变化（一阶）
- **情绪动量**：`ts_delta(ts_backfill(sentiment_overall_average, 66), 22)`。EUR 慢变量差分可能反向，必须原始+镜像分批。
- **注意力加速**：`ts_delta(ts_backfill(normalized_headline_count, 66), 5)` 作快腿。

### 3.3 异常（尾部）
- **坏消息冲击**：`sentiment_overall_minimum` 或 `sentiment2_lowest_score` 相对行业：`group_zscore(ts_backfill(sentiment2_lowest_score, 66), industry)`
- **好消息拥挤**：`peak_sentiment_value` 高且 `headline_item_count` 高 → 可能已定价，作反向门控。

### 3.4 交互
- **质量加权注意力**：`multiply(rank(ts_backfill(sentiment_overall_average, 66)), rank(ts_backfill(normalized_headline_count, 66)))`（两腿都强才乘）
- **双源分歧**：`subtract(ts_backfill(sentiment1_average_value, 66), ts_backfill(sentiment2_average_value, 66))` — 两套迁移不一致=信息摩擦
- **慢×快（D11 配方）**：慢腿 MH 非 FCF 价值残差（已有 |S|≈1.0）× 快腿 news85 情绪动量；加法 `add(0.65*rank(慢), 0.35*rank(快))`，禁止 FCF/starhold screening 主导

### 3.5 结构
- **总量 vs 均值**：`aggregate_sentiment_total` 含流量，均值去流量。残差：`subtract(rank(aggregate_sentiment_total), rank(headline_item_count))` 近似「条数中性的净极性」

### 3.6 累积
- **衰减记忆**：`ts_sum(ts_backfill(sentiment_overall_average, 66), 22)` vs 120 日 — 短窗快、长窗慢，禁止同周期互混当「新信号」

### 3.7 相对
- **国家/行业相对**：主轨 `group_zscore(..., industry)` 或 `group_neutralize(..., country)`；设置层已 COUNTRY，表达式层再做 industry 相对，避免与 PROD 池国家暴露重叠

### 3.8 本质
- 本集本质是 **「市场对新闻叙事的迁移极性」**，不是盈利、不是估值。可交易假设：未被宽基 MODEL 因子吸收的叙事冲击。因此禁止再包一层 `rank(close)` / returns 反转。

## 4. 实现约束

- VECTOR：`vec_avg(mws85_sentiment)` 后再 `ts_backfill`；禁止裸 VECTOR 进 `ts_*`
- 低覆盖：一律 `ts_backfill(66)`，更稀用 120
- 有界情绪：rank / group_zscore，禁 winsorize
- 计数字段：rank/bucket，禁 `ts_mean`
- 首批：1 槽 8 条早停（D11 弱探针上限）；有 |S|≥1.0 再转复杂模板，不做第二轮裸探针
- 禁止字段：价格/回报（不属于本集）；`analyst_earnings_ibes` 的 `*_dlr*` 回报
- 镜像：出现 sh≤-1.0 则下一批 `subtract(0, rank(...))`，不判死
- 跨集相关：与 `Wj71Q12o` 及 MH 价值腿互相关必须 <0.4 才允许并列提交

## 5. 推荐首探 8 条（S2/S3 输入，单槽）

1. `rank(ts_backfill(sentiment_overall_average, 66))`
2. `subtract(0, rank(ts_backfill(sentiment_overall_average, 66)))`
3. `group_zscore(ts_backfill(sentiment2_lowest_score, 66), industry)`
4. `rank(ts_delta(ts_backfill(sentiment_overall_average, 66), 22))`
5. `rank(subtract(ts_backfill(sentiment1_average_value, 66), ts_backfill(sentiment2_average_value, 66)))`
6. `rank(ts_backfill(normalized_headline_count, 66))`
7. `rank(vec_avg(mws85_sentiment))`（VECTOR 可用性探针，独立小批防连坐）
8. `add(0.5*rank(ts_backfill(sentiment_overall_median, 66)), 0.5*rank(ts_backfill(normalized_headline_count, 66)))`

## 6. 待探索问题

- sentiment1 与 sentiment2 在 EUR 是否近似共线？
- MATRIX 聚合是否已吸收 VECTOR 信息，还是事件日仍有增量？
- 与 MH `long_term_deep_value_europe_rank` 残差的互相关是否真的低？