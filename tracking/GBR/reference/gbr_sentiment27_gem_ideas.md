# GBR delay1 sentiment27 GEM Ideas（TOP700 / SUBINDUSTRY / decay4）

**Dataset**: sentiment27
**Region**: GBR
**Delay**: 1

数据集：sentiment27（Tranco 网站流行度排名，18 字段）。**跨集辅助说明**：概念 5/6 使用 sentiment7 的 snt7_all_languages_views（DEU 获胜配方原料），字段名在 Implementation Example 中直接写全；若 GEM 字段池校验拒绝，则该两概念单独手工合批。六法在线评测 2026-11-14（S1 批 `vzlw1Cy4i3ckgzYyHosoD` @NONE/dec0/P0Y0M0D/nanOFF）：
- 覆盖（法1）：totaldomains **644/700**、relpopularity1 **644/700**、snt27_rank **657/700**（92-94%，元数据 cov 0.80 低估）→ 全宇宙级，**不需 ts_backfill**
- 非零率（法2）：与法1 计数相同 → 零值可忽略，**不需 trade_when**
- 频率（法3）：relpopularity1 N=22 变化计数 649 ≈ **日更**；totaldomains N=22 仅 57%、N=5 仅 31% → **月/季更慢变量**，窗口下限 120+，天然低换手轨道（TO 0.045 实证）
- 形态（法6）：`ts_zscore(td,252)>0` 仅 **36.6%**（参考 50%）⇒ **右偏**；`>2` 占 **5.4%**（参考 2.3%）⇒ **右尾厚 2.3 倍**，必须 group_rank（必要时 winsorize）
- 量纲（法4/5）：`td/ts_mean(td,252)>2` 仅 **1 只** ⇒ 域名翻倍是极端事件，不做该档；36.6% 高于自身 1 年均值 ⇒ 多数公司处存量平台期
- kurtosis 附加：lc/sc **40/488 极不对称**、有效覆盖 75% ⇒ 概念 7 已改对称形式（ts_zscore 相对化）

死路规避（机制预探 Z14 `1KlDPwaLU4gHcJNwzrzVPWZ`）：relpopularity1 Δ66 **正向为负**（-0.40）——人气变化做**反转**不做动量；relpopularity1 z252 水平双向均弱（±0.29）；topranking z252 弱（0.09）。risk60 借券费率族 |S|≤0.37 判弱，不入本文档。

文献锚：Merton (1987) 投资者认知（网站=认知渠道）；Da-Engelberg-Gao (2011) 注意力突增→短期价格压力→回落；Pyun (2024, Econ Letters) 浏览量变化→正收益；Chalamandaris (2026) 情绪水平不可交易、只有脉冲可交易；论坛 LC97552 DEU 获胜式（S 2.04/17 检查全 PASS）：`vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt7_all_languages_views),22),5),5),22),120), ts_backfill(vec_avg(snl27_relpopularity08),22))`。

VECTOR 字段一律 vec_avg 聚合后横截面运算。

**Concept**: 数字存在广度（digital presence breadth）
- **Mechanism**: 公司域名组合广度 = 数字化投入 + 消费者触达渠道 + Merton 投资者认知渠道；NTU 实证网站流量↑ ⇒ 权益成本/波动率/分析师分歧↓。慢结构变量，水平效应在 GBR 未被套利干净（预探 S 0.57 / 2Y 1.69 / TO 0.045）
- **Fields**: `snl27_totaldomains`
- **Implementation Example**: `group_rank(vec_avg({snl27_totaldomains}), sector)`
- **Direction**: 正
- **expected_exposure**: digital presence breadth（长期需求优势 + 认知溢价）

**Concept**: 国际触达广度（international footprint）
- **Mechanism**: ccTLD/区域域名数量 = 国际市场触达与多国收入敞口，全球品牌的公司质量溢价
- **Fields**: `snl27_totalcountrydomains`
- **Implementation Example**: `group_rank(vec_avg({snl27_totalcountrydomains}), sector)`
- **Direction**: 正
- **expected_exposure**: international revenue exposure

**Concept**: 人气水平（popularity level）
- **Mechanism**: Tranco 排名水平（1=最流行）高的公司 = 持续消费者注意力存量，基本面需求优势的慢代理；反向取负排名即做多流行股
- **Fields**: `snt27_rank`
- **Implementation Example**: `multiply(-1, group_rank(ts_zscore(vec_avg({snt27_rank}), 252), sector))`
- **Direction**: 负（排名值低=流行 → 买）
- **expected_exposure**: consumer attention stock（预探 +0.54 实证）

**Concept**: 人气突增反转（attention spike reversal）
- **Mechanism**: Da-Engelberg-Gao：非新闻驱动的注意力突增 → 散户买入压力 → 短期价格高估 → 回落。GBR 预探 Δ66 正向 -0.40 / 反向 +0.40 双向实证。用 ts_ir 提相对突增强度（+100 次对 50 次/日公司是巨变、对 10000 次/日是噪声）
- **Fields**: `snl27_relpopularity1`
- **Implementation Example**: `multiply(-1, group_rank(ts_ir(ts_max(vec_avg({snl27_relpopularity1}), 5), 22), sector))`
- **Direction**: 负（突增 → 卖）
- **expected_exposure**: overattention reversal

**Concept**: Wikipedia 注意力脉冲（attention pulse，DEU 移植）
- **Mechanism**: LC97552 DEU 全 PASS 配方：查资料行为（维基浏览量）先于下单，信息在检索-消化-下单间存在时滞；ts_max(5) 提突增去周期基线，ts_ir(22) 相对强度归一。sentiment7 单独水平/动量在 GBR 弱（Z12 max 0.61），但脉冲形式未测过
- **Fields**: `snt7_all_languages_views`（跨集：sentiment7）
- **Implementation Example**: `group_rank(ts_ir(ts_max(ts_backfill(vec_avg(snt7_all_languages_views), 22), 5), 22), sector)`
- **Direction**: 正（突增 → 买，DEU 方向）
- **expected_exposure**: pre-order information search pulse

**Concept**: 脉冲去规模（pulse orthogonalized to popularity）
- **Mechanism**: DEU 获胜式完整移植：浏览量信号对 relpopularity08 做向量投影，剔「本身高人气公司浏览量系统性偏高」成分，保留纯注意力偏离
- **Fields**: `snt7_all_languages_views`（跨集）, `snl27_relpopularity08`
- **Implementation Example**: `group_rank(vector_neut(ts_ir(ts_max(ts_backfill(vec_avg(snt7_all_languages_views), 22), 5), 22), ts_backfill(vec_avg({snl27_relpopularity08}), 22)), sector)`
- **Direction**: 正
- **expected_exposure**: popularity-neutral attention deviation（6 ops ≤ 8）

**Concept**: 品牌聚焦结构（brand concentration，对称化修正）
- **Mechanism**: 域名排名分布的峰度 = 品牌聚焦度：厚尾（单一强势域名主导）vs 均匀（多域名分散触达）。⚠ 六法 S2 实测 `vec_avg(kurtosis)` **lc/sc = 40/488 极不对称**（多数公司峰度为负=分布扁平），裸 rank 量到的是结构性空头暴露（S -0.89 即此）⇒ 必须做**时序相对化**（减自身历史均值）后再横截面排序，得到"相对自身变尖/变平"的对称信号
- **Fields**: `snl27_kurtosis`
- **Implementation Example**: `group_rank(ts_zscore(vec_avg({snl27_kurtosis}), 252), sector)`
- **Direction**: 正（相对自身分布变尖 = 品牌聚焦强化）
- **expected_exposure**: brand focus change（对称化）

**Concept**: 需求趋势确认（demand trend，长短均线）
- **Mechanism**: 日更人气字段的长短均线交叉 = 需求趋势确认：短期均值持续高于长期均值 = 需求扩张通道（Pyun 浏览量变化→正收益），但须避开 22 日内突增反转窗 → 用 22/66 双标准窗比值
- **Fields**: `snl27_relpopularity1`
- **Implementation Example**: `group_rank(divide(ts_mean(vec_avg({snl27_relpopularity1}), 22), add(ts_mean(vec_avg({snl27_relpopularity1}), 66), 0.001)), sector)`
- **Direction**: 正
- **expected_exposure**: sustained demand expansion（避开脉冲窗的趋势版）

多样性自检：Expected Exposure 6 种（广度/国际/水平存量/反转/脉冲/结构）✓；字段族 3（snl27 计数族、snt27 排名族、snt7 浏览量族）✓；分组轴 sector 主 + market/subindustry 备 ✓；时间尺度 4（水平/5/22/66）✓；算子数 2-6 全部 ≤8 ✓。
