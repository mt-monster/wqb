# earnings_risk「财报事件风险」字段画像与战役档案（2026-10-20）

> 区域口径：USA / TOP3000 / Delay 1 / ATOM（所有非豁免字段均来自 earnings_risk；分组字段 industry 属豁免）。
> 本档按「字段画像 → 适用模板与机制 → 回测结果 → 归因 → 决策」组织；每批结论只在收齐后写入。
> 判死口径沿用 USA 纪律：S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB/|S|≥0.43（动态门限约 0.43×S）/ TO∈[1%,70%]；
> 交付前必须 `check_correlation` 实测 prod/self 均 <0.7，且用户明确确认（本档不含提交动作）。 <!-- from config.prod_corr_max -->

## 0. 选集理由（2026-10-20）

- 前序 `workforce_flow_skills` 批 1 的 4 条全闸/近全闸候选 prod 实测 0.8408–0.9255，
  按 D0-P 封存交付路径（慢劳动力基本面整体重叠已提交池）⇒ 必须换到**事件 / 期权风险**轴。
- `get_dead_ends(region=USA)` 未判死；数据集 aC 0–1、uC 0–1（极端低拥挤），
  与已交付 7 颗（全部分析师一致预期）以及已封的 option3（水平 IV / OI / 成交量结构）机制不同：
  本集是**围绕财报事件的隐含波动结构**，不是期权持仓水平。
- 已知结构性风险：覆盖率仅 0.279–0.307（约七成股票无期权数据）⇒ 全部构造先 `ts_backfill(...,66)`；
  VECTOR 按行权价维度聚合，用 `vec_avg`（波动/价差为强度量，不用 `vec_sum`）。
- 机制可陈述：IV skew（Cremers & Weinbaum 2010 的 call-put IV spread 异象）、
  财报波动率风险溢价（implied − realized）、财报后漂移（PEAD）、事件不确定性溢价。

## 1. 字段画像

`get_datafields(region=USA, universe=TOP3000, delay=1, dataset_id=earnings_risk)` 实测 9 个 VECTOR 字段：

| 族 | 字段 | 覆盖率 | userCount | alphaCount | 语义 |
|---|---|---:|---:|---:|---|
| IV skew | `atm_call_put_iv_spread` | 0.3068 | 1 | 1 | ATM call 与 put 的隐含波动率之差 |
| IV skew（归一） | `iv_spread_to_atm_volatility_ratio` | 0.3068 | 1 | 1 | 上述价差 ÷ ATM 波动水平 |
| 波动率风险溢价 | `earnings_volatility_risk_premium` | 0.3049 | 1 | 1 | 隐含财报波动 − 已实现波动（期权贵/便宜） |
| 隐含波动（水平） | `implied_earnings_volatility_estimate` | 0.3048 | 0 | 0 | 未到期财报事件的隐含波动水平 |
| 隐含波动（平滑） | `five_day_ma_earnings_volatility` | 0.3046 | 1 | 1 | 上述的 5 日均值 |
| 已实现波动 | `five_day_realized_volatility` | 0.307 | 0 | 0 | 近 5 日已实现波动 |
| 预测涨跌 | `predicted_earnings_related_price_move` | 0.3048 | 1 | 1 | 模型预测的财报事件价格变动幅度 |
| 上季财报涨跌 | `last_quarter_earnings_price_move` | 0.2904 | 1 | 1 | 最近一次财报日的实际价格变动 |
| 三年均值涨跌 | `three_year_avg_earnings_move` | 0.2792 | 0 | 0 | 过去三年财报日平均实际涨跌幅 |

画像判据：

- **VECTOR 先聚合**：全部用 `vec_avg`（跨行权价/期限的平均强度）；`vec_max/vec_min` 留作批 2 的尾部对照。
- **覆盖率 ~0.30**：必须 `ts_backfill(...,66)`；不做 `group_backfill`（避免把同行无期权股票硬填成同值）。
- **事件型更新**：字段在财报事件附近更新，`ts_backfill` 后可用 22/66 窗测量；短窗（1/5）无意义。
- **量纲**：全部是波动率/价格变动（无量纲或百分比），可直接比较；不需要 `ts_zscore` 归一（pv47 先验：
  时序去均值会毁横截面）。
- **拥挤度极低但不可当优势**：workforce 的低 aC/uC 仍撞 prod 墙 ⇒ 本集拥挤度只作参考，
  第一条全闸候选就实测 prod。

## 2. 适用模板与机制

### 2.1 经济机制

| # | 机制 | 文献/逻辑 | 方向先验 |
|---|---|---|---|
| E1 | IV skew（call−put） | Cremers & Weinbaum (2010)：偏离 put-call parity 的 call-put IV spread 正向预测收益（知情交易者买 call） | **正向** |
| E2 | 财报波动率风险溢价 | 隐含财报波动高于已实现 = 期权昂贵 ⇒ 未来收益低（波动率卖方溢价） | **负向** |
| E3 | 财报后漂移（PEAD） | 上季财报实际涨跌延续（信息扩散缓慢） | **正向**（延续） |
| E4 | 事件不确定性溢价 | 高预期涨跌幅 = 高不确定性 ⇒ 风险补偿为负（低波动异象） | **负向** |
| E5 | 历史事件波动记忆 | 三年平均财报涨跌幅（长期不确定性代理） | **负向** |

### 2.2 通用壳与测量面

```
quantile(group_rank(winsorize(<SIG>, std=4), industry))
```

- `<SIG>` 一律先 `ts_backfill(vec_avg(...), 66)`；
- 水平面直接 `ts_backfill`；变化面 `ts_delta(...,22)`；平滑面 `ts_mean(...,66)`；
- 分组用豁免字段 `industry`；`winsorize(std=4)` 具名、`quantile` 单参数。

### 2.3 模板族

| 模板 | 结构 | 诊断目的 |
|---|---|---|
| U1 IV skew 水平 | `ts_backfill(vec_avg(atm_call_put_iv_spread),66)` | E1 主假设 |
| U2 IV skew 季度变化 | `ts_delta(ts_backfill(...),22)` | E1 的「修正」面 |
| U3 归一化 skew | `ts_backfill(vec_avg(iv_spread_to_atm_volatility_ratio),66)` | 剔除波动水平后的纯偏斜 |
| U4 波动率风险溢价水平 | `-ts_mean(ts_backfill(vec_avg(earnings_volatility_risk_premium),66),66)` | E2 主假设 |
| U5 波动率风险溢价变化 | `-ts_delta(ts_backfill(...),22)` | E2 的「重新定价」面 |
| U6 上季财报涨跌 | `ts_backfill(vec_avg(last_quarter_earnings_price_move),66)` | E3 延续 |
| U7 预测涨跌 | `-ts_mean(ts_backfill(vec_avg(predicted_earnings_related_price_move),66),66)` | E4 |
| U8 三年均值涨跌 | `-ts_mean(ts_backfill(vec_avg(three_year_avg_earnings_move),66),66)` | E5 |

### 2.4 论坛与文献取证（2026-10-20，`search_forum_posts` 实检）

| 来源 | 关键内容 | 对本集的用法 |
|---|---|---|
| 【Alpha模板】Earnings 模板分享（低相关、横向点塔） | 明确「针对 Earnings 类型数据，模板使用 `ts_backfill` 回填」，形如 `<time_series_operator>(ts_backfill(<data_field>, …))` | 直接支持本批「全部字段先 `ts_backfill 66`」的选择；也印证事件型字段裸用会缺口 |
| 为什么 `implied_volatility_call_120 / parkinson_volatility_120` 调整后就能过（YZ84314，2025-01-11，14 赞） | 教程 19-alpha 示例 1 = IV ÷ 已实现波动；裸比值不易过，需调整 | E2 的事件窗版本就是 `earnings_volatility_risk_premium`（隐含 − 已实现）；**印证 VRP 是期权族第一主机制** |
| 【Alpha灵感】Improved Version of "Attention: Implied Volatility Spreads and Stock Return" | call−put IV spread 只在**高关注度**股票上显著（知情交易者买 call） | E1 在本集可能被截断：ATOM 不能跨数据集借 attention 字段 ⇒ 用 industry 分组当弱化版同侪条件；若 U1 弱而 U3 强，说明波动水平才是主因 |
| 【Alpha灵感】Individual Option Volatility Smirk | `iv_call_10 − iv_put_10` 直接构造，但「考虑覆盖率问题」需处理 | 与本集 cov 0.28–0.31 同构；不 backfill 会因样本集中挂 CW |
| AI 期权 alpha 策略的探究过程 | `rank((IV_mean_30 − HV_30)/HV_180) * sign(IV_skew_30)` | VRP 与 skew **相乘**是论坛常见组合；本批先用加性/单独面定位，再考虑 U3×U5 的乘积面（同一数据集内合法） |
| 如何优化 Sub-universe Sharpe？ | `group_zscore(ts_mean(winsorize(ts_backfill(IV_call_180/IV_mean_180,120),std=4),22),densify(market))` | 期权族的 SUB 修复先例是「比值归一 + 长 backfill」；若 U1–U3 SUB 破闸，用 U3 的比值面代替 U1 |
| 【2个月提交220个RA】HKG（EARNINGS+PV 实战） | 「earnings3 单数据集信号结构性不足」⇒ 该区靠 EARNINGS+PV 跨类别组合 | **ATOM 禁跨数据集** ⇒ 单数据集 earnings 塔只能靠事件条件化（`trade_when`）与多测量面，不能指望复制 HKG 的 PV 组合 |
| 10 个 ARC/GLB 模板帖 / IND RA 入门帖 | earnings、insiders、option 三类「难但值得试」；出货率低于 fundamental/imbalance/institutions | 与本轮「慢基本面全撞 prod、转事件/期权风险」的路线一致 |

文献锚（与 E1–E5 对应）：Cremers & Weinbaum (2010) call-put IV spread；Bollerslev, Tauchen & Zhou (2009) 波动率风险溢价；Bernard & Thomas (1989/1990) PEAD；Ang, Hodrick, Xing & Zhang (2006) 高特质波动低收益。

## 3. 回测结果

### 3.1 批 1（multisim `447mrZe5S4rMbplrCmM0QnY`，8/8 COMPLETE，0 error）

设置：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF。

| # | alpha | 构造 | S | F | 2Y | SUB | TO | returns | DD | rns | 失败闸 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| U1 | `bl8djZ16` | IV skew 水平 | 0.53 | 0.27 | 0.98 | 0.45 | 5.88% | 3.31% | 20.77% | −0.07 | S/F/2Y |
| U2 | `qME6jrJO` | IV skew Δ22 | 0.52 | 0.27 | 0.98 | 0.43 | 7.65% | 3.25% | 21.49% | −0.05 | S/F/2Y |
| U3 | `A1Q7lZ8E` | 归一化 skew | 0.52 | 0.27 | 0.95 | 0.46 | 6.02% | 3.29% | 21.18% | −0.07 | S/F/2Y |
| U4 | `E5VelWPP` | 波动率风险溢价水平（负向） | 0.54 | 0.28 | 0.99 | 0.41 | 1.49% | 3.36% | 20.99% | −0.07 | S/F/2Y |
| U5 | `9qE7X15q` | 波动率风险溢价 Δ22（负向） | **0.58** | **0.31** | **1.17** | **0.53** | 7.87% | 3.64% | 20.40% | 0.08 | S/F/2Y |
| U6 | `d5KRjVJw` | 上季财报涨跌 | 0.57 | 0.30 | 1.08 | **0.55** | 1.45% | 3.41% | **17.07%** | 0.02 | S/F/2Y |
| U7 | `O0Jx7Pdq` | 预测涨跌（负向） | 0.44 | 0.23 | 0.87 | 0.33 | 1.23% | 3.27% | 26.79% | 0.02 | S/F/2Y |
| U8 | `3qjelrmz` | 三年均值涨跌（负向） | 0.44 | 0.22 | 0.89 | 0.33 | **0.67%** | 3.23% | 27.08% | −0.13 | S/F/**TO**/2Y |

补充读数：8 条 `risk_neutralized_sharpe` 全在 **−0.13 … 0.08**；`CLUSTER_TEST` 警告值 0.37–0.58（限 1.58，远未拥挤）；
long/short 计数 **881–968 / 2011–2085**（覆盖率 0.30 的直接体现）；`pyramids` = `USA/D1/OTHER` multiplier 1.4（other 塔未点亮）。

## 4. 归因

1. **剥离风险后信号归零（最硬的一条）**：8 条 `rns` 全在 −0.13…0.08，而同为「慢变量」的 workforce 批 1 是 1.13–2.12。
   说明这 8 条不是「信号弱」，而是**几乎没有特异信息**——PnL 基本由风格暴露承载。任何参数层修复（decay / 窗口 / 中性化）
   都作用在同一个零成分上，不构成补批理由。
2. **IV skew 三面同值 ⇒ 归一化无效、且不是偏斜**：U1（水平 0.53）/ U2（Δ22 0.52）/ U3（归一 0.52）差 ≤0.01。
   若真为 call−put 偏斜，分母（ATM 波动）应当改变截面排序；完全不变的读数说明本集 `atm_call_put_iv_spread`
   的截面变异被**波动水平**主导。论坛取证（Improved Version of “Attention: Implied Volatility Spreads”）指出
   IV spread 只在**高关注度**股票上显著，而 ATOM 禁跨数据集借 attention 字段 ⇒ 该机制的放大器在本约束下不可用。
3. **VRP 是唯一有微弱梯度的方向，但梯度太小**：U5（Δ22）0.58 / 2Y 1.17 是全批最优；U4（水平）0.54 / 2Y 0.99。
   差闸线 1.00，而本季实测单自由度杠杆最大收益约 +0.2（pv103）到 +0.4（board_gov 的字段替换）⇒ 结构性不可达。
   U5 的 2Y > 全期（1.17 vs 0.58）也只说明近年略有效，不是可交付的全期 alpha。
4. **事件类「记忆型」字段全面弱且高回撤**：U7 预测涨跌、U8 三年均值涨跌同为 0.44，DD 26.8% / 27.1%（全批最差）。
   与 E4/E5 的低波动异象先验一致（高预期波动 → 低收益），但幅度不足以覆盖成本；U8 还额外踩 LOW_TURNOVER 0.67%。
5. **上季财报涨跌（E3/PEAD）是唯一低回撤方向**：U6 DD 17.1%（比 U5 低 3.3pt）、S 0.57、2Y 1.08、TO 1.45%。
   PEAD 在本集存在但幅度弱：论坛 HKG 经验（earnings 单数据集结构性不足）与本集实测一致。
6. **覆盖率 0.30 的代价不是 SUB，而是样本结构**：SUB 8/8 全过（0.33–0.55），说明子宇宙不是瓶颈；
   但 long/short 计数约 900/2050 表明只有约 1/3 股票可交易，且 backfill 66 天会把过期事件值带进面板
   ⇒ 「日频 backfill 面板」并不等于「事件窗口信号」，论坛 Earnings 模板（`ts_backfill` + time-series operator）
   在本集只解决了覆盖率，没解决信噪比。
7. **不补批（预注册偏离留痕）**：本集 8 探针覆盖 7 个字段 × 水平/变化/归一三面，max|S| 0.58 < 1.0 且 rns≈0。
   按纪律可直接判弱；原本设想的批 2（VRP×skew 乘积、`vec_max` 聚合、STATISTICAL 中性化）只能改变**形态**，
   不能制造 rns 里不存在的特异成分 ⇒ 不发批 2，避免重演 pv103 / dl_volume_pred 的无效补批。

## 5. 决策

- **判弱封存**：登记 `USA-EARNINGS-RISK-WEAK`（1 批 / 8 条，`447mrZe5S4rMbplrCmM0QnY`）。
  不换 universe、不发第 2 批、不把 `vec_max` / STATISTICAL 当救援（rns≈0 是构造层失败，不是设置层）。
- **可复用结论**（供后续期权/事件集参考）：
  ① 期权类字段在 USA/D1 的截面变异主要由**波动水平**承载，skew 必须配 attention / 流动性条件才有增量；
  ② **`risk_neutralized_sharpe ≈ 0` 应作为判弱的一级证据**，优先于 S 的大小（S 0.58 看似「差一点」，rns 0 才是真结论）；
  ③ 覆盖率 0.30 的事件字段用 66 天 backfill 后，信号退化为慢变量，与 workforce / board 等慢基本面同命；
  ④ 事件族里 **PEAD（上季涨跌）回撤最低**，若未来在未点亮塔做组合腿，它是最稳的一条。
- **残值**：无。8 条中无一条接近全闸（最好 U5 差 S 1.00 / F 0.69 / 2Y 0.41），不登记 salvage 池。
- **下一站**：回到未点亮 other 塔的剩余候选（`cre_exposure_model` 等），或按数据集扫描重新找**高字段数、未尝试**的集；
  详见交付台账「剩余未点亮塔可选池」。
