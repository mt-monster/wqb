# S1 · 非候选 Risk 数据集全字段画像（risk59 / risk60 / risk68 / risk71 / risk72）

> 采集：MCP `get_datafields(region=KOR, universe=TOP600, delay=1, filter_sharpe=false)`，逐个数据集全量拉取
> 用途：完成用户要求的「每个数据集全部字段梳理」，并给出**逐字段可用性裁定**（不进配额，但结论要可核）

---

## risk59 · Securities Lending & Short Market Dynamics（16 字段，**全部 VECTOR**）

cov **0.9806** · aC 564 · U 222 · MATRIX 0 / VECTOR 16 ⇒ **每字段必须先 `vec_avg`/`vec_max` 降维**

| # | field | 类 | cov | aC | 频率 | 形态 | 可用性 |
|---|---|---|---:|---:|---|---|---|
| 1 | `rsk59_bid_rate` | L1 借券价 | .9806 | 高 | 日 | 非负、右偏 | ✅ 可（水平；作同源比率分母） |
| 2 | `rsk59_offer_rate` | L1 借券价 | .9806 | 高 | 日 | 非负、右偏 | ✅ **已实测：level 族上界 1.04** |
| 3 | `rsk59_last_rate` | L1 成交价 | .9806 | **13（最不拥挤）** | 日 | 非负、右偏 | ✅ **本族最强（S 1.04 / 2Y 2.02）** |
| 4 | `rsk59_s3utilization` | L2 供给松紧 | .9806 | 67 | 日 | 0–1 | ⛔ 实测 S 0.09（无信号） |
| 5 | `rsk59_indicativeavailability` | L2 供给 | .9806 | 122 | 日 | 非负 | ⚠ 未测（作分母） |
| 6 | `rsk59_short_interest` | L3 空头存量 | .9806 | 中 | 日 | 非负 | ⛔ 水平量 = 规模代理（F-1） |
| 7 | `rsk59_shortinterestnotional` | L3 | .9806 | 中 | 日 | 非负 | ⛔ 美元量纲 |
| 8 | `rsk59_shortinterestpct` | L3（已归一） | .9806 | 25 | 日 | 0–1 | ⚠ 阴性对照（若单独出强信号 = 偷规模暴露） |
| 9 | `rsk59_daystocover10day` | L4 DTC | .9806 | 104 | 日 | 非负 | ⚠ 未测 |
| 10 | `rsk59_daystocover30day` | L4 | .9806 | 中 | 日 | 非负 | ⚠ 未测 |
| 11 | `rsk59_daystocover90day` | L4 | .9806 | 中 | 日 | 非负 | ⚠ 未测 |
| 12 | `rsk59_dtcdailychg` | L5 流量 | .9806 | 中 | 日 | 零中心 | ⛔ Δ 族已判死（ts_delta 安慰剂 0.04） |
| 13 | `rsk59_dtcweeklychg` | L5 | .9806 | 中 | 日 | 零中心 | ⛔ 同上 |
| 14 | `rsk59_short_momentum` | L5 | .9806 | **13** | 日 | 零中心 | ⚠ 未测 |
| 15 | `rsk59_crowded_score` | L6 黑盒 | .9806 | 中 | 日 | 有界 | ⛔ 供应商合成，不作主腿 |
| 16 | `rsk59_squeeze_risk` | L6 黑盒 | .9806 | 58 | 日 | 有界 | ⛔ 同上 |

**裁定**：三条形态轴（level 1.04 / variance 0.39 / delta 0.04）已全部实测完毕 ⇒ **上界 1.04**。
⚠ **2014 整年 `longCount=0`（数据自 2015 起，仅 9 年）** ⇒ **违反用户约束 6「近十年都要有数据」**。
⇒ 本战役**降级为备选**，只在 risk70/risk88 全部无计可施时回补，且交付须标注覆盖缺陷。
（详细实证见 [`../reference/datasets/risk59.md`](../reference/datasets/risk59.md)）

---

## risk60 · Securities Lending Insight（5 字段，**全部 VECTOR**）

cov **1.0** · aC 211 · U 83

| # | field | cov | aC | 频率 | 形态 | 可用性 |
|---|---|---|---:|---|---|---|
| 1 | `lending_fee_bid_rate` | 1.0 | **8（最不拥挤）** | 日 | 非负右偏 | ⚠ 未测；与 risk59 `bid_rate` 同源 |
| 2 | `rsk60_crowding` | 1.0 | 57 | 日 | 零中心有符号 | ⛔ 已判死（水平 −0.06 / ts_zscore −0.18） |
| 3 | `rsk60_datatime` | 1.0 | 62 | 日 | **时间戳 HHMMSS** | ⛔ 元数据，禁作信号 |
| 4 | `rsk60_last` | 1.0 | 89 | 日 | 非负右偏 | ⚠ 与 risk59 `last_rate` 同源（后者 S 1.04） |
| 5 | `rsk60_offer` | 1.0 | 55 | 日 | 非负右偏 | ⛔ 与 risk59 `offer_rate` 同源 |

**裁定**：`KOR-RISK60-CROWDING-NOSIGNAL` 继承，**不重开**。唯一残留价值 = `rsk60_last` 与 risk59 `last_rate` 的
**同源交叉验证**（若两者读数一致，说明跨集不可提供独立腿）。**本战役 0 槽。**

---

## risk68 · Forecast Data（5 字段，全 MATRIX）

cov .9914 · aC 770 · U 347

| # | field | cov | aC | 频率 | 形态 | 可用性 |
|---|---|---|---:|---|---|---|
| 1 | `rsk68_weight_volatility_short` | **1.0** | **503（全库最拥挤之一）** | 日 | 单边恒正右偏 | ⛔ 水平已被 258 users 占满；短长比已实测 −0.50/+0.18 |
| 2 | `rsk68_residual_return` | .9569 | 178 | 日 | 零中心 | ⛔ 继承 `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD` |
| 3 | `rsk68_weight_edadv` | 1.0 | 98 | 日 | 非负美元 | ⛔ 权重，非信号 |
| 4 | `rsk68_weight_dadv` | 1.0 | 94 | 日 | 非负美元 | ⛔ 权重，非信号 |
| 5 | `rsk68_beta` | 1.0 | 73 | 日（约 504 窗） | 近正态 | ⛔ `ts_delta(beta,66)` 实测 0.09 |

**裁定**：4/4 全灭 max\|S\| 0.50、2Y 6/10 年 <1.0 ⇒ **不重开**。

---

## risk71 · Daily Specific Return Profiling（7 字段，全 MATRIX）

cov .6658 · aC 349 · U 152 ⇒ **全部是 MFM2 特异收益在不同宇宙的拷贝**

| # | field | cov | aC | 宇宙口径 |
|---|---|---|---:|---|
| 1 | `asi_top1000_liquidity_dsrt` | .3785 | 8 | ASI TOP1000（流动性调整） |
| 2 | `asi_top1500_liquidity_dsrt` | .5879 | 21 | ASI TOP1500 |
| 3 | `residualized_return_asia_minvol1m` | **.908** | 37 | EQY_ASI_MinVol1M |
| 4 | `residualized_return_asia_top1100_liquid` | .3601 | 5 | ASI TOP1100 |
| 5 | `residualized_return_exjapan_minvol1m` | **.908** | 35 | XJPCI MinVol1M |
| 6 | `rsk71_eqy_asi_supported_minvol1m_dsrt` | .7592 | **158** | MINVOL1M |
| 7 | `rsk71_…`（第 7 个，同族） | — | — | — |

**裁定**：`KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`（2Y 修法九种全灭、全族 2Y ≤0.16）⇒ **不重开**。
形态：日频流量、零中心、厚尾；不可作水平、不可作反转（已证伪）。

---

## risk72 · Specific return of extended factors（5 字段，全 MATRIX）

cov .6246 · aC 402 · U 164

| # | field | cov | aC | 宇宙口径 |
|---|---|---|---:|---|
| 1 | `rsk72_eqy_asi_supported_minvol1m_dsrt` | **.7592** | 89 | ASI MinVol1M |
| 2 | `rsk72_eqy_xjpci_supported_minvol1m_dsrt` | **.7592** | 92 | XJPCI MinVol1M |
| 3 | `rsk72_asi_top2000_eqy_dsrt` | .7085 | **131** | ASI TOP2000 |
| 4 | `rsk72_asi_top1500_eqy_dsrt` | .5426 | 82 | ASI TOP1500 |
| 5 | `rsk72_asi_top1000_eqy_dsrt` | .3534 | 89 | ASI TOP1000 |

**裁定**：**5 条 description 逐字相同**（Daily reproducible specific returns in % units），
**唯一差别是宇宙** ⇒ 同一机制的 5 个快照，**不是 5 个信号**（两两组合必撞 self-corr）。
机制与 risk71 同一量、已判死；最短档 cov .35 十年覆盖也不达标 ⇒ **0 槽**。

---

## 五集合计裁定

| 数据集 | 字段 | 已测形态 | 上界 | 十年覆盖 | 本轮 |
|---|---:|---|---:|---|---|
| risk59 | 16 | level / variance / delta | 1.04 | ❌ 9 年（2014 空） | ⚠ 备选 |
| risk60 | 5 | 水平 / ts_zscore | 0.18 | 待查 | ✗ |
| risk68 | 5 | 短长比 / beta 漂移 / 门控 | 0.66 | ✅ | ✗ |
| risk71 | 7 | 残差反转九种修法 | 2Y 0.16 | ⚠ cov .66 | ✗ |
| risk72 | 5 | 0 槽（判「不投」） | — | ❌ cov .35–.76 | ✗ |

⇒ **本战役主攻 risk70（96 字段）+ risk88（64 字段）**，其余五集仅作对照与覆盖约束说明。
