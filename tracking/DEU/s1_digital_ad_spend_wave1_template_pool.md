# digital_ad_spend S1 台账（DEU / TOP500 / D1）

> 日期：2026-11-03　数据集：`digital_ad_spend`（Digital Advertising Spend Intelligence）
> 平台元数据：12 fundamental 集中**唯一零挖掘**：9 字段 / userCount 0-2 / alphaCount 0-2 / valueScore 5.0 / coverage 0.0
> 选址依据：§3775 判据「alphaCount 极低 ⇒ 平台 prod 池无同源 alpha ⇒ prod 相关性天然低」，比饱和集换算子省力一个量级

## 一、字段画像（get_datafields 实证，9/9 complete）

| 字段 | 类型 | 语义 | 分族 | 可用性 |
|---|---|---|---|---|
| `advertising_spend_usd` | VECTOR | 美元广告支出（CPM 推断） | 规模族·主腿 | ✅ 主信号 |
| `estimated_ad_spend` | VECTOR | 总广告支出 USD（归一化） | 规模族·重复对 | ⚠️ 与上行近重复，仅做口径消融 |
| `advertising_spend_local_currency` | VECTOR | 本地货币支出 | 规模族·汇率对 | ⚠️ 与下行重复，仅做汇率维度 |
| `estimated_local_ad_spend` | VECTOR | 本地货币（未归一） | 规模族·汇率对 | ⚠️ 同上 |
| `estimated_ad_impressions` | VECTOR | 估计曝光次数 | 规模族·分母腿 | ✅ CPM/密度的分母 |
| `ad_display_count` | VECTOR | 曝光明细数 | 规模族·计数腿 | ✅ 密度比（曝光/展示）分母 |
| `ad_content_format` | VECTOR | 广告创意格式（枚举） | 枚举族 | ⛔ 非数值，不可作信号 |
| `ad_purchase_channel` | VECTOR | 媒体购买渠道（枚举） | 枚举族 | ⛔ 非数值，不可作信号 |
| `ad_sales_channel` | VECTOR | 广告库存销售渠道（枚举） | 枚举族 | ⛔ 非数值，不可作信号（唯一有 1 alpha 的字段） |

**硬约束**：9 字段全 VECTOR ⇒ 必须先 `vec_sum`/`vec_avg`/`vec_count` 聚合；**禁元素级 power/multiply/abs/sign**（event 型 VECTOR 会被平台拒）。
**分组轴限制**：三个枚举字段**不能**做 `group_rank` 的分组轴（平台只认 subindustry/sector/industry/country 等标准类别）⇒ 枚举族在本数据集实际不可用，可用字段只剩 6 个（规模族）。

## 二、论坛取证（24 赞帖 43691545212567《把广告支出变成信号？》）

| 要点 | 原文/摘要 | 对设计的约束 |
|---|---|---|
| 定位 | 基本面大类里偏「另类」，覆盖网站与社媒，含品牌/品类/渠道/创意类型/购买路径 | 确认是另类数据而非财报数据 |
| **核心价值** | **广告投放强度的变化通常是营销强度、品牌竞争、消费者参与度的先行指标，可能早于财务报表反映经营热度** | 支持「增长/变化率」作主机制，而非仅水平 |
| 难点 1 | **数据是估计值不是精确值**（CPM 模型推断） | 避免高精度构造（如二阶差分），优先比值与排名 |
| 难点 2 | **行业之间差异很大**：某些行业投放与收入关系紧密，另一些很弱 | 必须做 **subindustry 行业内相对**（group_rank 而非裸 rank） |
| **建议** | **更适合作为补充视角而不是主力信号**；可和财务数据交叉验证，或观察行业层面营销强度变化 | 本波先验证单塔能否独立成信号；若弱则转条件腿 |

## 三、论文取证

**Kim & McAlister (2011), Journal of Marketing 75(4):68-85 —《Stock market reaction to unexpected growth in marketing expenditure》**
- 核心发现：**非预期广告支出增长对市值的影响是条件性的（contingent）**——
  - 广告支出**低于**响应阈值的公司：非预期增长 → **负向**（费用侵蚀，纯会计成本）
  - 广告支出**高于**阈值的公司：非预期增长 → **正向**（品牌资产投资被市场认可）
- 销售队伍支出增长一律负向（本数据集无此字段，不适用）
- **分析师忽略该信息**（因条件关系难以观察）⇒ 定价不足 ⇒ alpha 机会
- 作者明言「广告支出被当作营销的代理变量」（因公司不公开营销支出）

**可操作推论**：广告支出**增长**信号必须与**支出水平**条件化配对 ⇒ 正好落成 `trade_when(水平 gate, 增长信号, -1)`，完全契合「交互臂一律 trade_when gate 形式」纪律，且不需要第二数据集（单塔内完成条件化）。

## 四、探针 P1-P6（已派发 adsp_probe_20261103, pid 74004）

| P | 形态 | 机制 | 先验方向 |
|---|---|---|---|
| P1 | `group_rank(ts_mean(vec_sum(spend_usd),22), subindustry)` | 营销强度水平（行业内相对） | 未知（无形资产正 / 成本负） |
| P2 | `group_rank(ts_delta(ts_mean(spend,22),66), subindustry)` | 季度投放增长（论文主机制，未条件化） | 论文：条件性 ⇒ 裸跑应接近 0 |
| P3 | `group_rank(divide(ts_mean(spend,22), ts_mean(impressions,22)), subindustry)` | **CPM 获客成本效率**（每次曝光花多少钱） | 高 CPM = 获客贵 → 负 |
| P4 | `group_rank(ts_mean(vec_sum(impressions),22), subindustry)` | 曝光规模（触达强度） | 未知 |
| P5 | `trade_when(水平>ts_quantile(水平,252), 增长, -1)` | **论文条件化·高支出组** | 正 |
| P6 | `trade_when(水平<ts_quantile(水平,252), -增长, -1)` | **论文条件化·低支出组取负** | 正（低支出组增长为负 ⇒ 取负） |

双预检：verify_expr 6/6 valid；preflight `valid:true` / `unknown_fields:[]`。

## 五、正式波 T1-T12 设计草稿（≥10 结构互异，待探针定向）

| T | 骨架 | 结构差异点 | 来源 |
|---|---|---|---|
| T1 | `group_rank(ts_rank(ts_mean(spend,22),252), subindustry)` | 水平×长窗时序分位 | 自建（news29 W3 同构成功面） |
| T2 | `group_rank(ts_delta(ts_delta(ts_mean(spend,22),66),66), subindustry)` | **二阶差分＝增长加速度**（论坛难点1：估计值噪声大，风险项） | 自建 |
| T3 | `group_rank(ts_delta(divide(spend,impressions),66), subindustry)` | **CPM 变化率**（成本趋势而非水平） | 自建 |
| T4 | `group_rank(divide(ts_mean(impressions,22), ts_mean(display_count,22)), subindustry)` | **曝光密度**（每次展示触达效率，全新构造） | 自建 |
| T5 | `trade_when(水平>ts_quantile(水平,504), 长窗增长, -1)` | 论文条件化·高支出组 × 长窗 gate | Kim & McAlister 2011 |
| T6 | `trade_when(水平<ts_quantile(水平,504), -长窗增长, -1)` | 论文条件化·低支出组 | Kim & McAlister 2011 |
| T7 | `group_rank(divide(subtract(ts_mean(spend,22), ts_mean(spend,504)), ts_std_dev(ts_mean(spend,22),504)), subindustry)` | **zscore 自身基线**（检验 oth699 金型是否跨集，已有两次证伪） | oth699 金型迁移测试 |
| T8 | `group_rank(ts_zscore(divide(spend,impressions),252), subindustry)` | **CPM 异常度**（标准化成本偏离） | 自建 |
| T9 | `group_rank(ts_delta(ts_mean(spend,252),126), subindustry)` | 年度趋势（**126 非白名单** ⇒ 需实测证据，或改 66/252） | 自建 |
| T10 | `group_rank(divide(ts_sum(spend), ts_sum(impressions)), subindustry)` | **口径消融**：ts_sum vs ts_mean（NaN 语义，复现 news29 vec_count 经验） | news29 口径经验 |
| T11 | `group_rank(divide(spend_usd, spend_local), subindustry)` | **汇率维度**（美元/本币背离＝海外投放占比） | 重复对设计 |
| T12 | `group_rank(ts_rank(divide(spend,impressions),504), subindustry)` | CPM 长窗分位（低换手版） | 自建 |

**注**：T9 的 126 不在白名单（1/5/22/66/252/504/1008/1260），实施时改为 `ts_delta(ts_mean(spend,252),66)` 或提供实测证据；T11 的 usd/local 需确认两字段非恒等（汇率波动）。

## 六、★★★ 覆盖率实证判死（2026-11-03，探针 P1 逐年 longCount 核查）

用 `get_alpha_yearly_stats(alpha_id=gJe8R2wm)`（P1 支出水平臂）查逐年多头持仓：

| 年份 | longCount | pnl | sharpe | TO |
|---|---:|---:|---:|---:|
| 2014 | **1** | 423,865 | 0.18 | 6.1% |
| 2015 | **6** | 3,087,044 | 1.88 | 8.2% |
| 2016 | **9** | -1,020,895 | -0.98 | 7.3% |
| 2017 | **12** | 684,748 | 0.85 | 7.5% |
| 2018 | **11** | -1,244,196 | -1.32 | 5.4% |
| 2019 | 23 | 1,589,697 | 2.04 | 6.1% |
| 2020 | 26 | 925,835 | 1.05 | 5.7% |
| 2021 | 26 | 1,144,973 | 1.30 | 6.6% |
| 2022 | 31 | -1,463,634 | -1.59 | 5.2% |
| 2023 | 31 | 177,472 | 0.24 | 2.7% |

**判读**：
1. **无空窗**（10 年 longCount 全 >0、pnl 全 ≠0）⇒ 按用户的「连续空窗」判据**不排除**；
2. 但**宽度致命**：TOP500 里多头最多只有 **31 只**（≈6% 覆盖），2014 年仅 **1 只** ⇒ 这是 1–31 只股票的「组合」，CW 集中度必 FAIL、不可交易——与 `risk72` 当年「持仓 19/19 太窄，仅作取证」同一类判死理由；
3. ⇒ **P1 0.36 / P4 0.49 不是「弱信号」，而是「几乎没股票有数据」**。这解释了平台为何该集只有 0–2 个 alpha：不是没人发现，是**数据宽度不支持**。

**结论：`digital_ad_spend` 判死（数据宽度不足）**，P5/P6 剩余 2 臂跑完仅作取证记录，不进入正式波。

## 七、风险登记

1. **覆盖率是最大风险**：平台 coverage=0.0，帖子明言「覆盖范围有限」。DEU/TOP500 是德国大公司，若广告投放数据只覆盖部分股票 ⇒ 前 3 条探针须核验逐年 longCount。
2. **估计值噪声**：CPM 模型推断而非真实支出 ⇒ 二阶差分/高频构造易被噪声淹没。
3. **行业异质性**：已用 subindustry 行业内相对缓解；若仍弱，考虑改 sector（更粗分组、样本更足）。
4. **VECTOR 全字段**：任何未聚合的裸字段会直接报错。
