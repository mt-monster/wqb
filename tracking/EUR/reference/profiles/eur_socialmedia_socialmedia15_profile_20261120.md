# EUR / socialmedia15 全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=socialmedia15, region=EUR, universe=TOP2500, delay=1)`：**45/45 字段，complete=True**（`sharpe_filter_applied=true` 但 removed=0）。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`；塔位实读 EUR/D1 **SOCIALMEDIA 0/3（唯一未开波塔）**，倍率 1.2。
> 数据源：社交媒体/新闻文本派生情绪分，两代字段——**新代 `scl15_*` 32 个**（2026-03-01 onboard，cov 0.3708，aC 0–9 极冷门）+ **d1 代 `scl15_d1_*` 13 个**（2022-07-01，cov 0.255–0.299，aC 29–140）。全部 VECTOR（须 vec_avg/vec_sum 降维）。

## 1. 字段全表（45 字段逐字段平台读数）

| 字段 | 类型 | cov | uC | aC | 语义/范围 | 可用性判定 |
|---|---|---:|---:|---:|---|---|
| `dividend_trend_score` | VECTOR | 0.3708 | 8 | 8 | 股息趋势 -1~1 | 主信号候选 |
| `scl15_analystrating` | VECTOR | 0.3708 | 3 | 3 | 分析师升降级 -1~1 | 主信号候选（低拥挤） |
| `scl15_anger` | VECTOR | 0.3708 | 1 | 1 | 愤怒 0~1 | 主信号候选（极冷） |
| `scl15_attrition_score` | VECTOR | 0.3708 | 4 | 4 | 裁员 0~1 | 主信号候选 |
| `scl15_buzz` | VECTOR | 0.3708 | 8 | 9 | 关注度 0~1 | 主信号候选 |
| `scl15_conflict` | VECTOR | 0.3708 | 5 | 6 | 分歧 -1~1 | 主信号候选 |
| `scl15_debt_score` | VECTOR | 0.3708 | 3 | 4 | 破产风险 0~1 | 主信号候选 |
| `scl15_earn_score` | VECTOR | 0.3708 | 1 | 1 | 盈利惊喜 -1~1 | 主信号候选（极冷） |
| `scl15_emotionvsfact` | VECTOR | 0.3708 | 1 | 1 | 情绪vs事实 -1~1 | 主信号候选 |
| `scl15_fear` | VECTOR | 0.3708 | 2 | 2 | 恐惧 0~1 | 主信号候选 |
| `scl15_fundamentalstrength` | VECTOR | 0.3708 | 8 | 8 | 基本面正面度 -1~1 | 主信号候选 |
| `scl15_gloom` | VECTOR | 0.3708 | 1 | 2 | 悲观 0~1 | 主信号候选 |
| `scl15_innovation` | VECTOR | 0.3708 | 1 | 1 | 创新 0~1 | 主信号候选 |
| `scl15_joy` | VECTOR | 0.3708 | 1 | 1 | 愉悦 0~1 | 主信号候选 |
| `scl15_litigation` | VECTOR | 0.3708 | 0 | 0 | 诉讼 0~1 | 主信号候选（零用户，需实证） |
| `scl15_longshort` | VECTOR | 0.3708 | 1 | 1 | 买卖情绪 -1~1 | 主信号候选 |
| `scl15_longshortforecast` | VECTOR | 0.3708 | 0 | 0 | 买卖预测 -1~1 | 主信号候选 |
| `scl15_lovehate` | VECTOR | 0.3708 | 2 | 2 | 爱憎 -1~1 | 主信号候选 |
| `scl15_managementchange` | VECTOR | 0.3708 | 0 | 0 | 管理层变动 -1~1 | 主信号候选 |
| `scl15_managementtrust` | VECTOR | 0.3708 | 1 | 1 | 管理层信任 -1~1 | 主信号候选 |
| `scl15_mergers` | VECTOR | 0.3708 | 3 | 6 | 并购 0~1 | 主信号候选 |
| `scl15_optimism` | VECTOR | 0.3708 | 1 | 2 | 乐观 -1~1 | 主信号候选 |
| `scl15_price_score` | VECTOR | 0.3708 | 1 | 1 | 价格预测 -1~1 | 主信号候选 |
| `scl15_pricedirection` | VECTOR | 0.3708 | 1 | 1 | 价格方向 -1~1 | 主信号候选 |
| `scl15_risk_score` | VECTOR | 0.3708 | 0 | 0 | 泡沫风险 -1~1 | 主信号候选 |
| `scl15_sentiment` | VECTOR | 0.3708 | 2 | 2 | 净情绪 -1~1 | 主信号候选 |
| `scl15_stress` | VECTOR | 0.3708 | 2 | 2 | 焦虑 0~1 | 主信号候选 |
| `scl15_timeurgency` | VECTOR | 0.3708 | 1 | 1 | 时效性 -1~1 | 主信号候选 |
| `scl15_trust` | VECTOR | 0.3708 | 1 | 1 | 可信度 -1~1 | 主信号候选 |
| `scl15_uncertainty` | VECTOR | 0.3708 | 0 | 0 | 不确定性 0~1 | 主信号候选 |
| `scl15_violence` | VECTOR | 0.3708 | 0 | 1 | 激烈反应 0~1 | 主信号候选 |
| `scl15_volatility` | VECTOR | 0.3708 | 1 | 1 | 波动感知 0~1 | 主信号候选 |
| `scl15_d1_buzz` | VECTOR | 0.2991 | 88 | 128 | 关注度 0~1 | d1 代主信号 |
| `scl15_d1_conflict` | VECTOR | 0.2779 | 100 | 140 | 分歧 -1~1 | d1 代主信号 |
| `scl15_d1_emotionvsfact` | VECTOR | 0.2936 | 71 | 94 | 情绪vs事实 -1~1 | d1 代主信号 |
| `scl15_d1_fundamentalstrength` | VECTOR | 0.2589 | 72 | 87 | 基本面正面度 -1~1 | d1 代主信号 |
| `scl15_d1_longshort` | VECTOR | 0.2671 | 37 | 49 | 买卖情绪 -1~1 | d1 代主信号 |
| `scl15_d1_optimism` | VECTOR | 0.2681 | 52 | 68 | 乐观 -1~1 | d1 代主信号 |
| `scl15_d1_pricedirection` | VECTOR | 0.2627 | 29 | 34 | 价格方向 -1~1 | d1 代主信号 |
| `scl15_d1_risk_score` | VECTOR | 0.2656 | 46 | 51 | 泡沫风险 -1~1 | d1 代主信号 |
| `scl15_d1_sentiment` | VECTOR | 0.2952 | 44 | 56 | 净情绪 -1~1 | d1 代主信号 |
| `scl15_d1_stress` | VECTOR | 0.2688 | 50 | 65 | 焦虑 0~1 | d1 代主信号 |
| `scl15_d1_timeurgency` | VECTOR | 0.2686 | 54 | 77 | 时效性 -1~1 | d1 代主信号 |
| `scl15_d1_trust` | VECTOR | 0.2552 | 52 | 64 | 可信度 -1~1 | d1 代主信号 |
| `scl15_d1_volatility` | VECTOR | 0.2635 | 48 | 57 | 波动感知 0~1 | d1 代主信号 |

## 2. 六维画像

- **类型**：全 VECTOR（45/45），须 `vec_avg`/`vec_sum` 降维；**禁 vec_count 直接作信号**（语义为条数≠情绪）。
- **覆盖率**：新代 cov 0.3708、d1 代 0.255–0.299——均 <0.85，按 insiders1 教训**不凭 cov 判死**，用 `ts_backfill(...,60~120)` 实测 sub/TO 闸。
- **更新频率**：文本派生日频分，但只有情绪事件日有值 ⇒ 事件型稀疏，须回填。
- **分布特征**：`0~1` 有界概率（anger/fear/uncertainty）与 `-1~1` 有界打分（sentiment/optimism/conflict）两类——按 EUR earnings_sent_matrix 实证，**有界概率/打分 → `ts_zscore(ts_backfill(...,60),250)` 有效**；矩类字段禁 `!=0`。
- **可用性**：新代 aC 0–9（**极冷门，prod 友好**），d1 代 aC 29–140（较拥挤）；零用户字段（litigation/managementchange/risk_score/uncertainty）需实证是否有信号。
- **适用性**：主信号 = 有界情绪分（sentiment/optimism/fear/anger/longshort/price_score）；辅助 = 关注度类（buzz 作 presence 门控）；排除 = 纯元数据（无，本集全为分）。

## 3. 机制假设（三路证据后）

- 论文（20 篇/18 作者多样闸，题录级）：*Social-Media Sentiment, Limited Attention, and Stock Returns*(2019)、*Media tone and expected stock returns*(2020)、*The Sum of All FEARS Investor Sentiment and Asset Prices*(2014, RFS)——**媒体负面语调/恐惧情绪预测低收益**。
- 论坛（post 44654147837719）：text_alt 族（news/opinion/sentiment）是独立第 3 生产安全族；post 44865552906135：`ts_zscore` 窗口边界效应须查旧极值移出。
- 模板：`ts_zscore(ts_backfill(vec_avg(<field>),60),250)` + 截面 rank/分组，方向按「恐惧/愤怒/诉讼/悲观→负，乐观/盈利惊喜/基本面正面→正」先验，用方向对照实证。

## 4. 30 臂实测与结构诊断（2026-11-20）

按三段式：段0 无历史跳过 → 段1 {TOP2500,CS1600}×INDUSTRY 16 臂 → 方向对照 8 臂 → 形态验证（delta/vec_sum/掩码/短窗/buzz）6 臂，**共 30 臂全 REJECT**。

- **系统性负 S**：段1 16 臂中 15 臂 S<0（−0.48~0.25），唯一正项 = buzz 门控（S0.25）。最优接近 0，无近闸候选 ⇒ 按 A/B/C 三分支均不触发，**不进段2/段3**。
- **方向对照否证「方向反了」**：8 臂取反后仍全负（optimism 正 0.37→反 0.59 绝对值近似，fear 正 0.25→反 0.43）——**不是方向问题**。
- **逐年诊断揭示真因（get_alpha_yearly_stats, j2a8W87k）**：2014–2023 longCount/shortCount **全年份>0**（数据不缺年份），但**long:short ≈ 1:8**（278/2220 起，2023 666/2086）——cov 0.37 下仅 1/3 股票有情绪值，`ts_backfill` 后非覆盖股恒 0，`group_rank` 把全市场压成「有覆盖 vs 无覆盖」哑变量，**取反产生另一个哑变量，两者都弱**。这是数据覆盖结构性缺陷，非年份缺失、非方向、非设置。
- **形态验证全灭**：ts_delta(22) / vec_sum / `!=0` 掩码 / 短窗66 / buzz长窗 6 臂 S−0.30~−0.48 ⇒ 模板空间已穷尽。
- **判定**：SOCIALMEDIA 塔（0/3）**不可经 socialmedia15 点亮**，PROVISIONAL/族级（不判数据集死——零用户新字段可能随覆盖提升变可用）；insiders1 教训再次验证：低 cov 事件型字段 `ts_backfill` 能救 sub/TO 闸，但救不了「rank 变哑变量」的结构缺陷。
- 唯一线索（若将来复攻）：buzz 作 presence 门控（唯一正 S 臂）——只在有情绪事件日持仓，绕开了「恒 0 哑变量」问题。
