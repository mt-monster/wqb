# EUR/PV wave：intraday_pv_feats 日内微观结构面（EUR/D1/TOP2500）2026-11-06

> 定位：EUR/PV 塔当前 2/3（未点亮，差 1 颗即可点亮）。此前 EUR/PV 已判死的两个面是图表形态（continuation_score + pattern_scores，6 骨架全灭 max 0.84）与 techindi（self 锁死）。本波换第三条完全独立的机制面：**日内时段 × 价格类型的微观结构字段**。
> 数据集 intraday_pv_feats 在欧洲 585 字段全 MATRIX，cov 0.90-0.9993，**aC 绝大多数字段是 0-5**（最拥挤的 avg_vwap_to_last_price_ratio 也只 122）⇒ 全场最干净的处女地之一。

## 一、为什么选这个数据集（三条独立理由）
1. **塔位性价比**：EUR/PV = 2/3，只差 1 颗点亮；且 pv 不在「已点亮塔」之列。
2. **零拥挤**：585 字段里 aC=0 的字段成片存在（mean_low_price_return_60m_post_open / max_high_interval_last_ratio_daily / max_twap_vwap_ratio_daily / mean_ask_to_vwap_ratio_first_quarter_volumeclock），prod 相关性风险天然低。
3. **同数据集在 HKG 是唯一能稳定过 1.58 的面**（HKG 台账 W4/W7/W14/W15 实绩：S 2.17-2.42、全闸通过、逐年十年无空窗）。GBR 侧该面判死（复合结构），故欧洲是一次干净的第三方验证。

## 二、S1 字段画像（MCP get_datafields 实测，零仿真成本）
数据集结构 = **时段 × 价格类型 × 统计量** 三维笛卡尔积：
- **时段维**：post_open 30m/60m、pre_close 30m/60m、first/last_half_volume、first/last_quarter_volumeclock、daily、first/last_interval。
- **价格类型维**：vwap / last_trade / high / low / ask / bid / twap。
- **统计量维**：mean / max / min / std / skew / kurtosis / momentum(1,2,3) / return / 各类 ratio。

本波用到的 18 个字段（cov / aC 实测）：
| 字段 | cov | aC | 语义 |
|---|---:|---:|---|
| mean_vwap_return_60m_post_open | 0.9583 | 1 | 开盘后 60 分钟 VWAP 收益 |
| mean_vwap_return_60m_pre_close_2 | 0.9849 | 26 | 收盘前 60 分钟 VWAP 收益 |
| mean_vwap_return_30m_pre_close_2 | 0.9849 | 25 | 收盘前 30 分钟 VWAP 收益 |
| mean_high_price_return_60m_pre_close | 0.9853 | 8 | 收盘前 60 分钟最高价收益 |
| mean_low_price_return_60m_pre_close_2 | 0.9853 | 3 | 收盘前 60 分钟最低价收益 |
| mean_high_interval_last_ratio_daily | 0.9713 | 4 | 日最高价相对收盘的平均位置比 |
| mean_low_interval_last_ratio_daily | 0.9713 | 7 | 日最低价相对收盘的平均位置比 |
| skew_last_trade_price_interval | 0.9846 | 3 | 日内成交价序列偏度 |
| kurtosis_high_price_interval | 0.9713 | 5 | 日内最高价序列峰度 |
| mean_bid_to_ask_price_ratio_first_quarter_volumeclock | 0.9604 | 3 | 成交量前 1/4 时段买卖价差 |
| mean_bid_to_ask_price_ratio_last_quarter_volumeclock | 0.9095 | 2 | 成交量后 1/4 时段买卖价差 |
| mean_bid_ask_size_ratio_30m_post_open | 0.968 | 1 | 开盘后 30m 买卖挂单量比 |
| mean_bid_ask_size_ratio_30m_pre_close_2 | 0.9773 | 1 | 收盘前 30m 买卖挂单量比 |
| mean_twap_vwap_ratio_daily | 0.9709 | 11 | TWAP/VWAP 全天比 |
| momentum_vwap_last_half | 0.9377 | 3 | 后半场 VWAP 一阶动量 |
| momentum3_vwap_daily | 0.9628 | 15 | 全天 VWAP 三阶动量 |
| mean_trade_volume_60m_post_open | — | — | 开盘后 60m 平均成交量 |
| mean_trade_volume_60m_pre_close | — | — | 收盘前 60m 平均成交量 |

## 三、论坛 / 外部论文取证（用机制前先查，2026-11-06 本轮实做）
### 外部论文（均在线核实存在）
- **[P1] Heston, Korajczyk & Sadka (2010)**, "Intraday Patterns in the Cross-Section of Stock Returns", *Journal of Finance* 65(4):1369-1407（SSRN 1509466 / arXiv:1005.3535 双向核实）。核心结论：**横截面上日内半小时收益存在周期性**，同一时段跨日的收益可预测。⇒ 支撑把「同一时段跨日的 ts_mean」作为信号本体（T01/T02/T03/T13 的共同底座）。
- **[P2] Bogousslavsky (2021)**, *Journal of Financial Economics*（经论坛帖转引，本轮未直接打开原文）：**日内不同时段的收益在横截面上有各自独立的定价含义，收盘前时段与隔夜/开盘时段的信号方向甚至相反**。⇒ 支撑「时段分歧」（post_open 减 pre_close_2）这一几何，以及必须分时段定号。
- **[P3] "Intraday time series momentum: Global evidence and links to market characteristics"**, *Journal of Financial Markets*（ScienceDirect S138641812100001X，本轮在线命中）：日内动量在全球市场普遍存在，且与市场特征（流动性/波动）相关。⇒ 支撑动量期限结构与 SNR 归一化（T11/T12）。
- **[P4] Cushing & Madhavan (2000)**（HKG 台账已引）：收盘竞价是流动性补偿而非信息，⇒ 收盘段收益应**反转**。这就是 T13 取 reverse 的依据。
### 论坛（search_forum_posts 本轮实做，48 条命中里取 6 条最相关）
- **[F1]「收盘前 30 分钟追高的人，半年后都在给你送钱：GLB 尾盘高点反转因子（高点反转、低点却不反转的意外发现）」** —— 与本波 T03 同机制同字段族；其「高点反转、低点不反转」的非对称实测直接支撑 T03 与 T04 的单侧设计，并提示 low 腿需要单独定号。
- **[F2]「把公式里的 close 换成 open，符号就翻了——MEA 市场一次日内买压反转的机制证伪」** —— close/vwap 衡量的是**成交重心落在哪一段**而非涨跌幅；换时段即换符号。⇒ 支撑必须分时段做正反号对照，不能跨市场照搬符号。
- **[F3]「关于 PV 字段因子 Turnover 高的原因分析及解决方案」** —— 明确指出 intraday_pv_feats 是日内频、信号每天剧烈变化、原始字段换手高，正确解法是 ts 平滑 + decay 而非硬压。⇒ 本波全部模板都套了 ts_mean(66/126/252) 平滑，并用 EUR 的 decay 8。
- **[F4]「不看幅度看显著性：一个信噪比（SNR）模板在 USA/GLB/EUR 三个市场的因子化尝试」** —— SNR 模板在 **EUR** 有实测先例；分母的噪声度量会随市场状态伸缩、等于内嵌波动率择时。⇒ 支撑 T01/T03/T10 的信息比率几何，同时提示 2022 高波动年会被分母惩罚（HKG 实证 2Y 谷形）。
- **[F5]「日内上下行波动不对称溢价：低波动异象的相对结构版本」** —— 日内向上探索幅度与向下探索幅度是两个对称量。⇒ 支撑 T04 的 high-low 振幅腿。
- **[F6]「开盘后执行滑点（Slippage）的非线性偏度特征构造」** —— 滑点与其二次方的协偏度能捕捉交易成本联合分布的非对称性。⇒ 本波未直接用（HKG W16 已判滑点族全灭），登记为备靶。

## 四、塔混 / ATOM 纯净检查
- 13 个模板**全部只含 intraday_pv_feats 单数据集字段**，不含 returns / close / volume 等 PV 基础字段腿，也无第二个数据集 ⇒ **纯净单数据集 ATOM，不占任何两塔组合配额、不触碰「集合内两两禁混」**。
- 注意反向风险：PV 属于禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL}，若后续把 returns/volume 加进来就变成 PV+PV（集合内互组，**禁止**），因此本波任何扩展都必须留在 intraday_pv_feats 内部。

## 五、模板池（13 个，结构互异；来源 [P]论文 / [F]论坛 / [S]自建）
| # | 来源 | 信息维度 / 结构轴 | 几何 | 算子 | 表达式 |
|---|---|---|---|---:|---|
| T01 | P1/P2/F4 | 时段分歧（开盘段延续 vs 收盘段反转） | 信息比率 + group_zscore(industry) | 6 | group_zscore(divide(ts_mean(subtract(POv,PCv),126),ts_std_dev(subtract(POv,PCv),126)),industry) |
| T02 | P1/S | 同上但换「相对自身历史位置」 | ts_rank(252) + group_rank(subindustry) | 3 | group_rank(ts_rank(subtract(POv,PCv),252),subindustry) |
| T03 | P2/F1 | 价格类型溢价（最高价相对 VWAP） | 信息比率 + group_zscore(industry) | 6 | group_zscore(divide(ts_mean(subtract(POh,PCv),126),ts_std_dev(subtract(POh,PCv),126)),industry) |
| T04 | F5 | 日内振幅（上下行不对称） | ts_mean(66) + group_rank(sector) | 3 | group_rank(ts_mean(subtract(POh,PCl),66),sector) |
| T05 | S | 日内路径偏度（三阶矩） | ts_zscore(66) + group_zscore(industry) | 2 | group_zscore(ts_zscore(skew_last_trade_price_interval,66),industry) |
| T06 | S | 跳跃强度（四阶矩相对自身） | 比值几何 + group_rank(industry) | 3 | group_rank(divide(kurtosis_high_price_interval,ts_mean(kurtosis_high_price_interval,252)),industry) |
| T07 | F2 | 极值出现位置（高低点相对收盘） | 差分 + ts_mean(66) + group_zscore(sector) | 3 | group_zscore(ts_mean(subtract(mean_high_interval_last_ratio_daily,mean_low_interval_last_ratio_daily),66),sector) |
| T08 | S | 买卖价差时段演化（流动性提供模式） | 差分 + ts_mean(66) + group_rank(industry) | 4 | group_rank(ts_mean(subtract(bid_ask_last_q,bid_ask_first_q),66),industry) |
| T09 | S | 挂单厚度时段演化（尾盘买压积累） | 差分 + ts_mean(126) + group_zscore(subindustry) | 4 | group_zscore(ts_mean(subtract(bas_pre_close,bas_post_open),126),subindustry) |
| T10 | P3/S | TWAP-VWAP 偏离（成交分布形状 / 大单承接位） | 信息比率 + group_zscore(industry) | 4 | group_zscore(divide(ts_mean(mean_twap_vwap_ratio_daily,126),ts_std_dev(mean_twap_vwap_ratio_daily,126)),industry) |
| T11 | P3 | 动量期限结构（一阶 vs 三阶之差） | 差分 + group_rank(sector) | 2 | group_rank(subtract(momentum_vwap_last_half,momentum3_vwap_daily),sector) |
| T12 | P3 | 成交量时段后置（U 形分布） | 比值 + 双 ts_mean(66) + group_zscore(industry) | 5 | group_zscore(divide(ts_mean(vol_pre_close,66),ts_mean(add(vol_post_open,vol_pre_close),66)),industry) |
| T13 | P4/HKG | 收盘段单独反转 | reverse + 信息比率 + group_zscore(industry) | 5 | reverse(group_zscore(divide(ts_mean(mean_vwap_return_30m_pre_close_2,126),ts_std_dev(mean_vwap_return_30m_pre_close_2,126)),industry)) |

**结构互异核对**（不是换窗口/换常数）：覆盖 **水平·一阶差分·二阶矩·三阶矩（偏度）·四阶矩（峰度）·比值·位置** 七类矩；几何覆盖 **信息比率 / ts_rank 时序分位 / ts_zscore / 纯比值 / 直接差分** 五类；分组轴覆盖 **industry / sector / subindustry** 三档；信息维度覆盖 **时段分歧 / 价格类型溢价 / 振幅 / 路径偏度 / 跳跃 / 极值位置 / 价差演化 / 挂单演化 / 成交分布形状 / 动量期限 / 成交量时间分布 / 单段反转** 十二个互不重叠的经济面。≥10 达标。

## 六、窗口口径
只用有意义窗口：66（季度）用于 ts_mean/ts_zscore 平滑；126（半年 = 2 个季度）用于信息比率的长窗均值与标准差；252（年）用于 ts_rank 时序分位与峰度的长期基准。未使用任何非标准数值。

## 七、派发实绩
- 2026-11-06 批 A：T01（时段分歧信息比率）+ T03（最高价相对 VWAP 溢价），multisim **1Lo6SLgtW4Keb6LhCDGejSH**。
  - 为什么是这两条：它们是 HKG 侧两个已过全闸的最强机制（W7 G4 时段分歧 S 2.41 / F 2.51；W7 G1 high-vwap 溢价 S 1.80 / F 1.50），先验证「机制在 EUR 是否成立」这一最根本问题，再决定是否展开其余 11 个结构。
  - 欧洲设置档：EUR/TOP2500/D1、decay 8、SLOW_AND_FAST、trunc 0.08、unit VERIFY、nan ON、pasteurization ON、maxTrade ON。
  - 预检：13/13 valid=true、unknown_fields=[]、platform_field_count=18、算子 2-6 全 ≤12。

## 八、收批时的判读纪律（预先写死，防事后找理由）
1. **方向不照搬 HKG**：EUR/USA/MEA 都出现过换市场符号翻转（论坛 F2）。若两条都给出镜像强信号，直接翻号即可，不算判死。
2. **F 与 vol 先算**：vol = ret/S。日内微观结构预期 vol 偏高（8% 量级），F 门槛相对宽松；但若实测 vol ≤2% 则按 F = S^1.5×sqrt(vol/0.125) 反推所需 S，>2.0 直接换族。
3. **2Y 谷形**：HKG 实证窗口 126 恰好落在 2Y 谷底（2022 弱），破法是把 126 → 180/252（长窗平滑单独修 2Y 而不牺牲 S）。本波 T01/T03 起步就用 126，若只卡 2Y 先试 T02（252 分位）。
4. **判死门槛**：同一面 ≥6 个结构互异骨架全灭才判死。当前已测 0 个。

## 九、备靶（未入主池）
- 滑点协偏度（论坛 F6）——HKG W16 已判滑点水平/差分全灭，故只登记不派。
- momentum2_* 日内二阶动量族（HKG W4 P8 S 1.02）——优先度低于主池。
- mean_price_modulo_10_ratio_daily 价格聚集（散户/心理定价代理）——语义弱，仅登记。
## 十、收批实绩与判决（2026-11-06）

### 批 A（multisim 1Lo6SLgtW4Keb6LhCDGejSH）
| alpha | 模板 | S | F | TO | 2Y | sub | ret | vol=ret/S | fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rKR0ALAE` | T01 时段分歧·信息比率 | −0.09 | −0.01 | 4.64% | −0.34 | 0.25 | −0.16% | 1.78% | 3 |
| `VkxMOEOY` | T03 最高价相对 VWAP 溢价 | 0.11 | 0.01 | 4.44% | −0.58 | 0.35 | 0.19% | 1.73% | 3 |

### 批 B（multisim 2P953A2lq55s9ZQ5TGa6xdW）
| alpha | 模板 | S | F | TO | 2Y | sub | ret | vol=ret/S | fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `A1VLkPxQ` | T04 日内振幅 high−low | −0.51 | −0.14 | 4.67% | −1.40 | −0.54 | −0.98% | 1.92% | 4 |
| `xArlRkvW` | T05 日内路径偏度 | −0.28 | −0.04 | 19.77% | −0.58 | −0.12 | −0.48% | 1.71% | 3 |

### 判决：EUR/PV intraday_pv_feats 面判死（两条独立杀因）

1. **信号杀**：4 个结构互异骨架（时段分歧 / 价格类型溢价 / 日内振幅 / 路径偏度）全部 3–4 闸失败，**max |S| = 0.51**。特别是批 A 两条用的是 HKG 侧已过全闸且最强的两个机制（HKG W7：ZYQ716j1 S 2.41 / MPY18MVr S 2.34 / RRE7vM2e S 1.80，同一个数据集的同一批字段），在 EUR 上直接塌到 |S| ≈ 0.1 —— 这不是参数问题，是**机制不迁移**。
2. **F 数学杀**：四条实测 vol = 1.71% / 1.73% / 1.78% / 1.92%（高度一致，说明是该数据集字段固有属性）。按 F = S^1.5 × sqrt(vol/0.125)，要 F = 1 需 S ≥ 1.9；而信号天花板只有 0.51。即使后面某个模板偶然把 S 拉到 1.2，F 也只有 0.36。**在 vol ≤2% 的数据集上，S < 1.5 就等于封盘**。

**为什么提前收口（诚实标注）**：本面只测了 4 个骨架，未达「同一面 ≥6 个结构互异骨架全灭」的一般判死门槛。提前收口依据的是本项目已固化的第二条判据：**vol ≤2% 且骨架最强 S <1.5 ⇒ 立即封盘，不必凑满 6 个模板**（该判据曾在 EUR/PV 图表形态面被独立验证过：那次 6 骨架全灭、vol ≈1.9-2.0%，与本次数值几乎重合）。

**EUR/PV 第三个已死机制面**：图表形态（continuation_score + pattern_scores）❌｜techindi（self 锁死）❌｜日内微观结构（本波）❌。EUR/PV 仍停在 2/3，本区已无低成本点亮路径。

### 可迁移结论（写入 Agent Memory 候选）
- **跨区域的机制迁移性必须先测，不能照搬**：同一个数据集、同一批字段、同一骨架，HKG 给 S 2.34–2.42 全闸通过，EUR 给 |S| 0.1。差异的候选解释是市场结构（HKG 散户/集中、EUR 宽基流动性高、日内微观结构已被 HFT 套利）。⇒ 任何跨区搬配方，首批必须包含一条「原区最强骨架」作为标尺，其 S 直接反映该机制在该区的存活率。
- **vol 是数据集的固有属性、可先验测**：本数据集四条独立构造的 vol 全落在 1.71–1.92%，一致性极高。⇒ 用 1–2 条探针拿到 vol 后即可反算该数据集达 F=1 所需的 S 门槛，避免无谓扩面。