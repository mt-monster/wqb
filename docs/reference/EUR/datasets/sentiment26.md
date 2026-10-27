# sentiment26 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `sentiment26` |
| 名称 | Website Popularity Ranking Dataset |
| 类别 | SENTIMENT |
| 数据字段数(平台) | 19 |
| 覆盖率 | 0.7528 |
| 平台已有 alpha | 462 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.4 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive ranking of internet domains based on passive DNS traffic, capturing the relative activity of websites across a global network. Unlike traditional site ranking models that focus on browser-based traffic, this dataset measures the number of unique client IPs interacting with each domain, offering a protocol-agnostic view of internet engagement. Aggregated metrics such as top percentile rankings, skewness, and kurtosis help identify domains with unusual or concentrated activity. By tracking changes in domain activity and popularity, analysts can detect emerging trends, shifts in user behavior, and potential catalysts that may influence the price movements of companies associated with these domains.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **19** |
| 类型分布 | VECTOR×19 |
| 平均覆盖率 | **0.753** |
| 覆盖率区间 | 0.58 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 1 | 5.3% |
| 中 (0.70–0.90) | 17 | 89.5% |
| 低 (0.50–0.70) | 1 | 5.3% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 18 | 94.7% |
| UNUSABLE | 1 | 5.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 18 / UNUSABLE 1 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 13 | 0.74 | snt26_avgranking、snt26_kurtosis、snt26_skewness |
| 宏观与行业 | 2 | 0.87 | snt26_dltcc、snt26_totalcountrydomains |
| 情绪与新闻 | 2 | 0.75 | snt26_relpopularity08、snt26_relpopularity1 |
| 搜索与替代数据 | 2 | 0.75 | snt26_totaldomains、snt26_wq_pit |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `snt26_dltcc` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country code top-level domain |
| 2 | `snt26_avgranking` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean DNS popularity rank across all mapped domains for the issuer on the observation date; lower means more popular over |
| 3 | `snt26_kurtosis` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Kurtosis of the issuer’s domain rank distribution on the observation date |
| 4 | `snt26_relpopularity08` | VECTOR | 0.748 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite attention metric approximately equal to the sum over domains of 1/rank^0.8 (alpha=0.8); reduces dominance of t |
| 5 | `snt26_relpopularity1` | VECTOR | 0.748 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite attention breadth score, approximately the sum over domains of 1/rank (alpha=1); higher indicates broader/stro |
| 6 | `snt26_skewness` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Skewness of the issuer’s domain rank distribution on the observation date |
| 7 | `snt26_top10pctranking` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Rank threshold (cutpoint) below which the top 10% best-ranked mapped domains for the issuer fall on the observation date |
| 8 | `snt26_top10pctrankingavg` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Average rank among the top 10% best-ranked mapped domains for the issuer on the observation date; lower values indicate |
| 9 | `snt26_top25pctranking` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Rank threshold (cutpoint) for the top 25% best-ranked mapped domains for the issuer on the observation date; lower is mo |
| 10 | `snt26_top25pctrankingavg` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Average rank among the top 25% best-ranked mapped domains for the issuer on the observation date; lower values indicate |
| 11 | `snt26_top50pctranking` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Rank threshold (cutpoint) for the top 50% best-ranked mapped domains for the issuer on the observation date; lower is mo |
| 12 | `snt26_top50pctrankingavg` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Average rank among the top 50% best-ranked mapped domains for the issuer on the observation date; lower values indicate |
| 13 | `snt26_top75pctranking` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Rank threshold (cutpoint) for the top 75% best-ranked mapped domains for the issuer on the observation date; lower is mo |
| 14 | `snt26_top75pctrankingavg` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Average rank among the top 75% best-ranked mapped domains for the issuer on the observation date; lower values indicate |
| 15 | `snt26_topranking` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Best (lowest) DNS popularity rank among all mapped domains for the issuer on the observation date |
| 16 | `snt26_totalcountrydomains` | VECTOR | 0.748 | 宏观与行业 | 0 | — | — | — | UNTESTED | Count of mapped domains with country-code TLDs (ccTLDs) for the issuer on the observation date; excludes generic TLDs li |
| 17 | `snt26_totaldomains` | VECTOR | 0.748 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total count of mapped domains for the issuer on the observation date |
| 18 | `snt26_wq_pit` | VECTOR | 0.748 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | For ongoing data it is wq_append_time, for history data it simulated from PIT simulation field in the MCD input settings |
| 19 | `snt26_rank` | VECTOR | 0.584 | 风险与质量 | 0 | — | — | — | UNUSABLE | Cisco Umbrella DNS popularity rank for the domain on data_date (lower means more popular) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-SNT26-ATTENTION-FITNESS-CEILING`（None）family=sentiment26 网站流行度/投资者注意力族：{"dataset": "sentiment26", "evidence": {"LL9d1JO9": "注意力水平 relpopularity08：S0.90/F0.45/2Y1.75 PASS/TVR0.0929/returns0.0319/longCount1061，仅 2 项 FAIL", "N1QRr0YE": "注意力广度动量 totaldomains：S0.09 无信号", "ZY0Kn563": "top10% 集中度：S-0.84（镜像后 +0.84 仍不达线）"}, "math_proof": "turnover 0.0929 已低于公式下限 0.125，分母钉死 → Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.90*0.505 = 0.455，实测 0.45 已贴天花板。即使 Sharpe 达 1.

