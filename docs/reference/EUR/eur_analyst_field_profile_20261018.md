# EUR Analyst 类别 · 数据集全面扫描与字段画像（2026-10-18 修订版）

> 本档案**取代** `eur_analyst_field_profile_20261017.md` 第三章的字段画像部分（旧版仅覆盖前 300 字段）。
> 回测验证见本文 §7；旧版 §6.1–6.9 的战役记录仍然有效（针对 `analyst_factor_signals` 单一数据集）。
> Region：EUR｜universe TOPCS1600｜delay 1｜neutralization SUBINDUSTRY｜decay 1｜maxTrade OFF｜truncation 0.08

---

## 一、塔态核实（平台权威 `get_pyramid_alphas`，2026-10-18）

EUR / D1 塔计数：

| 已点亮（=1） | 未点亮（=0） |
|---|---|
| model、fundamental、analyst、other、risk | pv、news、sentiment、insiders、macro、earnings、institutions、socialmedia、imbalance |

⚠ **`analyst` 塔 = 1，来源是 PPA 通道的 `786pLKnb`，不是 RA 产出。**
⇒ 严格按「已点亮塔的数据集不纳入候选」的选集约束，Analyst 类别整体处于排除区。
本档案仍完整产出，因为它同时承担**纠错**职责：旧档案的「Analyst 结构性穷尽」结论建立在错误采样上（见 §二）。

---

## 二、关键纠错：旧画像只覆盖不足 30% 的字段

旧档案（`eur_analyst_field_profile_20261017.md` §3）记录的「实测字段数」与平台真实字段数严重不符：

| 数据集 | 旧档案记录 | **平台真实** | 覆盖率差 |
|---|---:|---:|---:|
| analyst_consensus | 300（297 V + 3 M） | **1929**（1911 V + **18 M**） | 15.6% |
| analyst15 | 297 MATRIX | **1744 MATRIX** | 17.0% |
| analyst7 | 299 MATRIX | **1111 MATRIX** | 26.9% |
| analyst10 | 294 | **961**（841 M + 120 V） | 30.6% |
| analyst69 | 297（247 V） | **813**（240 M + 573 V） | 36.5% |
| analyst4 | 264（134 V） | **776**（565 M + 211 V） | 34.0% |

**根因**：平台 `/data-fields` 接口 `limit ≤ 50` 且 `offset > 50` 返回空 ⇒ 旧画像按前缀分页抓取时静默截断。
**后果**：旧结论「Analyst 唯一有效原语 = eps_revision_magnitude ÷ 分歧度」只在被截断的子集内成立，**不可外推为类别穷尽**。
**新纪律**：任何「类别穷尽」声明前，必须先核对本地 `fields` 表计数与平台 `dataset.field_count` 一致。

---

## 三、Analyst 16 集真实规模（平台权威）

| 数据集 | 字段总数 | MATRIX | VECTOR | cov≥0.5 | 平台 alphaCount | 拥挤度 |
|---|---:|---:|---:|---:|---:|---|
| analyst_consensus | 1929 | **18** | 1911 | 1499 | 408 | 低 |
| analyst15 | 1744 | 1744 | 0 | 1744 | 15617 | 中 |
| analyst7 | 1111 | 1111 | 0 | 1111 | 27688 | 中 |
| analyst10 | 961 | 841 | 120 | 711 | 4780 | 低 |
| analyst69 | 813 | 240 | 573 | 805 | 167628 | 极高 |
| analyst4 | 776 | 565 | 211 | 521 | 2664 | 低 |
| analyst11 | 445 | 445 | 0 | 445 | 850 | 低 |
| analyst14 | 121 | 121 | 0 | 121 | 3200 | 低 |
| analyst9 | 111 | 5 | 106 | 104 | 251 | 极低 |
| analyst_factor_signals | 108 | 108 | 0 | 44 | 421 | 极低（已被 PPA 占腿） |
| analyst45 | 61 | 0 | 61 | 61 | 635 | 低 |
| analyst39 | 24 | 24 | 0 | 24 | 3959 | 低 |
| analyst40 | 22 | 20 | 2 | 0 | 63 | 极低（董事变动，TO 爆炸） |
| analyst_base_ref | 17 | 7 | 10 | 6 | 7 | 极低 |
| analyst81 | 5 | 5 | 0 | 0 | 37 | — |
| model52 | 3 | 3 | 0 | 0 | 40 | —（违约概率，cov 0.199） |

---

## 四、字段画像（按机制价值排序）

### 4.1 `analyst_consensus` —— 18 个 MATRIX 预测值字段（旧档案误判为「无预测值字段」）

| 字段 | 覆盖 | 平台 aCnt | 语义 |
|---|---:|---:|---|
| `mean_estimate_targetprice_annual12_tribes` | 0.9477 | 6 | 12 个月目标价一致预期均值 |
| `stddev_estimate_targetprice_annual12_tribes` | 0.9477 | **0** | 目标价预测**分歧度**（可作分母） |
| `median_estimate_targetprice_annual12_tribes` | 0.9477 | 2 | 中位数（抗异常值） |
| `max/min_estimate_targetprice_annual12_tribes` | 0.9477 | 0 / 1 | 极值（可构造极差分歧度） |
| `mean/stddev/max/min/median_estimate_fxadj_targetprice_annual12_tribes` | 0.9477 | 0–1 | 汇率/拆股调整版（**跨币种可比**） |
| `mean/stddev/max/min/median_estimate_eps_longterm` | 0.7809 | 0–1 | 长期 EPS 预测（LTG 口径） |
| `estimate_count_current_period_targetprice_annual12_tribes` | 0.9477 | 4 | 覆盖分析师家数（广度） |
| `estimate_currency_code_targetprice_annual12_tribes` | 0.9477 | 0 | 币种代码（**毒药字段，不可用**） |

**机制价值**：`mean/stddev` 成对 ⇒ 可直接构造 **targetprice 修正 ÷ 分歧度**（IND 已验证 S1.68/F1.30/2Y1.92/robust0.92 的现役最强骨架），且拥挤度 aCnt 仅 0–6，**与已锁死的 `eps_revision_magnitude` 机制完全正交**。
**更新频率**：季频一致预期，`ts_delta(·,66)` 或 3 个月快照差分口径。

### 4.2 `analyst7` —— 1111 MATRIX，**32 个指标具备完整四件套**（最高价值）

字段命名：`est_{12m|q}_{指标}_{统计}` + 快照后缀 `_4wks_ago` / `_3mth_ago` / `_28d`（无后缀 = 当前）。
统计量：`mean / median / high / low / std / num`。

**32 个四件套指标**（均具备 `mean` 当前 + `mean_3mth_ago` + `std` 当前 + `mean_4wks_ago`）：

| 期限 | 指标（经济含义） |
|---|---|
| 12m（23 个） | `cpx` 资本开支 ★、`fcf` 自由现金流 ★、`roa` 资产回报率 ★、`roe` 净资产回报率 ★、`tbv` 有形账面价值 ★、`nav` 净资产值 ★、`dps` 每股股息 ★、`sal` 营业收入 ★、`grm` 毛利率 ★、`opr` 营业利润、`ebi` EBIT、`ebt` 税前利润、`net` 净利润、`eps` 每股收益、`bps` 每股账面值、`cps` 每股现金流、`csh` 现金、`gps` 每股毛利、`pre` 税前、`prr`、`ner`、`ent`、`ndt` |
| q（9 个） | `eps`、`net`、`ebi`、`ebt`、`sal`、`gps`、`pre`、`prr`、`ner` |

**机制价值**：每套四件套 = 一个独立的「修正幅度 ÷ 分歧度」机制 ⇒ **最多 32 条正交腿**。
其中 `cpx`（资本开支预期）、`fcf`、`dps`、`tbv`、`nav`、`grm` 是旧战役**从未测过**的经济维度。
**覆盖**：全字段 cov = 0.5（半数股票无覆盖），需评估子宇宙持仓数。

### 4.3 `analyst15` —— 1744 MATRIX，**行业/板块级**分析师预测聚合（独立机制层）

字段命名：`anl15_{指标}_{层级}_{期限}_{统计}`
- 指标：`ebg`（EPS growth，289）、`ebt`（226）、`bps`（225）、`cps`（225）、`dps`（225）、`sal`（225）
- **层级**：`ind` 行业（471）/ `s` 板块（471）/ `gr` 集团（471）
- 期限：`fy1/fy2/fy3`（各 288）、`cal`（621）、`1m/3m/6m`（各 111）、`ltg`（36）、`12m/18m`
- 统计：`chg` 修正幅度（333）、`up/dn` 上下修家数（各 222）、`gro` 增速（132）、`mean`、`pe`、`total`、`cos` 公司数、`ests` 估计数、`dev` 离散度

**机制价值**：这是**行业景气度**信号层 —— 「整个行业的分析师在往哪个方向改预测」，与个股修正正交。
三种用法：① 直接信号（行业轮动）② 分组轴 `group_rank(个股信号, 行业景气桶)` ③ 门控 `trade_when(行业修正在改善, 个股信号, -1)`。

### 4.4 `analyst10` —— 961 字段，含**直接预测惊喜**与 SmartEstimate

| 族 | 数量 | 语义 |
|---|---:|---|
| `pred_det`（`*past_det*`） | 119 | 预测明细/元数据 |
| **`pred_surps`** | **111** | **预测盈利惊喜**（v0/v1/v2 三版本 × 多指标 × FY1/FY2） ★ |
| **`smart_ests`** | **111** | **SmartEstimate 自营预测值**（v0/v1/v2） ★ |
| `smun` | 64 | 样本/分析师家数 |
| `consensus` | 37 | 一致预期值 |
| `revise_ratio_to_close` / `to_consensus` | 62 | 修正幅度 ÷ 股价 / ÷ 一致预期（**天然无量纲**） |
| `innovate_increase/decrease` | 62 | 创新性修正家数（广度） |
| `normal_increase/decrease` | 59 | 常规修正家数 |

**机制价值**：`pred_surps` 是**直接输出惊喜预测**的字段（MEMORY 铁律「只认直接输出收益率/概率的字段」的合格对象）；`revise_ratio_to_*` 天然无量纲，**绕开本轮的单位陷阱**。

### 4.5 其余数据集速判

| 数据集 | 结构 | 判断 |
|---|---|---|
| `analyst69`（813） | 240 M + 573 V，aCnt 167628（**全库最挤**） | 拥挤度极高，prod 必爆，不作交付目标 |
| `analyst4`（776） | 565 M + 211 V，cov 0.66 | 待测；旧档案 S 0.65 且 TO 0.020 触下限 |
| `analyst11`（445 全 M） | 一致预期水平量 | 旧判死（S ≤0.21，breadth 无信号） |
| `analyst14`（121 全 M） | 一致预期 | 旧 S 0.48 / 2Y 负 |
| `analyst9`（111） | 106 VECTOR | 旧 S 0.45 |
| `analyst_factor_signals`（108） | 日频修正幅度 | ★ 唯一原语但 **prod 被 PPA `786pLKnb` 锁死 0.92+** |
| `analyst45`（61 V） | VECTOR 共识 | 旧 S 0.36 |
| `analyst39`（24 M） | — | 旧 S 0.19 |
| `analyst40`（22） | 董事变动事件 | TO 1.50–1.63 爆炸，判死 |
| `analyst_base_ref`（17） | 股数/价格参考 | 2Y −0.58，判死 |
| `analyst81` / `model52` | cov 0.24 / 0.20 | 覆盖过低，不测 |

---

## 五、机制设计矩阵（可出的正交腿数）

| 机制 | 数据集 | 字段 | 经济锚 | 正交性 |
|---|---|---|---|---|
| A. 目标价修正 ÷ 分歧度 | analyst_consensus | `mean/stddev_estimate_targetprice_annual12_tribes` | 卖方目标价 | 与 eps 修正正交 |
| B. 长期 EPS 修正 ÷ 分歧度 | analyst_consensus | `*_estimate_eps_longterm` | LTG | 与 A 部分重叠 |
| C1–C32. 分指标修正 ÷ 分歧度 | analyst7 | `est_{12m,q}_{cpx,fcf,roa,roe,tbv,nav,dps,sal,grm,...}_{mean,mean_3mth_ago,std}` | 各指标独立 | **32 条腿，互相经济含义不同** |
| D. 行业景气修正 | analyst15 | `anl15_{ebg,ebt,bps,cps,dps,sal}_{ind,s,gr}_{1m,3m,6m}_chg` | 行业层面 | 与个股层正交 |
| E. 预测惊喜 | analyst10 | `*_pred_surps_v{0,1,2}` | 分析师惊喜 | 与修正幅度不同（水平 vs 变化） |
| F. 无量纲修正比 | analyst10 | `*revise_ratio_to_close_*` | 修正/股价 | 天然无量纲，安全 |

---

## 六、本轮新增硬约束：单位兼容性

**实测（2026-10-18，wave588）**：`add(<TSPrice 单位的 stddev_*>, 0.01)` 在 EUR（`unitHandling=VERIFY`）下 **10/10 条整批判 WARNING 且无任何指标**：

```
Incompatible unit for input of "add" at index 1,
expected "Unit[TSPrice:1]", found "Unit[]"
```

⇒ **修正了此前「只产生 UNITS warning 不阻塞回测」的错误认知**。
**规则**：
1. 价格/股数单位的字段（`stddev_*targetprice*`、`*_tbv_*`、`*_eps_*` 等）**禁止与常数相加**。
2. 需要防零除时分母必须选**同单位字段**，或用 `divide(x, y)` 直除（零值由平台返回 null，`nanHandling=ON` 可处理）。
3. 比率类字段（ROA/ROE/毛利率/`revise_ratio_to_*`）本身无量纲，与常数相加安全。

---

## 七、回测验证

见 §7.1 起（本文件持续追加）。

### 7.1 wave588（targetprice，含单位错误，整批作废）

| 批次 | 条数 | 结果 |
|---|---:|---|
| `1Tt4ffgbQ4nF9lih2RKhxTP` | 10 | **10/10 WARNING**：`add(stddev, 0.01)` 单位不兼容，无指标 |

### 7.2 wave589 / wave590 —— 「快照差分 ÷ 分歧度」20 颗，**全部 2Y_DEAD**

设置：TOPCS1600 / SUBINDUSTRY / decay 1 / maxTrade OFF / truncation 0.08。

**wave590（直除版，无单位常数）**

| alpha | 机制 | S | F | TO | returns | 2Y |
|---|---|---:|---:|---:|---:|---:|
| `KPmkj7ag` | targetprice 修正÷std（sector） | 0.94 | 0.52 | 0.0926 | 0.0385 | **0.04** |
| `2rjJblkb` | 同上（industry） | 0.93 | 0.50 | 0.0984 | — | −0.14 |
| `RRAdn7Ld` | 同上（subindustry） | 0.97 | 0.50 | 0.0758 | — | −0.28 |
| `A1QkMldl` | 同上（delta 22 窗） | 0.54 | 0.19 | 0.1626 | — | −0.09 |
| `QPYEL7dg` | eps_longterm 修正÷std | 0.40 | 0.15 | 0.1123 | — | 0.82 |
| `0mjz0woq` | analyst7 cpx 修正÷std | 0.08 | 0.01 | 0.0651 | — | −0.56 |
| `npA3M70z` | analyst7 fcf | 0.18 | 0.04 | 0.0670 | — | 0.94 |
| `xA1R0jMl` | analyst7 roa | 0.09 | 0.02 | 0.0613 | — | −0.32 |
| `KPmkj7e1` | analyst7 sal | **1.29** | 0.76 | 0.0709 | 0.0403 | −0.26 |
| `pwv8AjQo` | analyst7 tbv | 0.27 | 0.08 | 0.0580 | — | 0.65 |

**wave589（同一 analyst7 结构，含 `add(std,0.01)`；analyst7 的 std 无量纲，未报单位错）**

| alpha | 机制 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `O0JoEZJY` | cpx | 0.04 | 0.00 | 0.0645 | −0.64 |
| `58jMoOjM` | fcf | 0.19 | 0.05 | 0.0669 | 0.94 |
| `npA3M2Aa` | roa | 0.14 | 0.03 | 0.0603 | −0.21 |
| `mLYZMbYW` | tbv | 0.30 | 0.10 | 0.0577 | 0.65 |
| `xA1R0krq` | dps | 0.94 | 0.45 | 0.0623 | −0.12 |
| `d5KdA0Wg` | sal | **1.36** | **0.82** | 0.0704 | −0.22 |
| `rKdAvlRo` | grm | 0.14 | 0.03 | 0.0597 | 0.12 |
| `P0Mvd3oM` | nav | 0.42 | 0.14 | 0.0642 | −0.63 |
| `YPxQG01J` | **eps** | **1.37** | **0.83** | 0.0757 | 0.35（sub_LOW） |
| `akVoqna6` | q_eps | 0.61 | 0.28 | 0.0896 | −0.24 |

**结论（三条）**
1. **`2Y_DEAD` 是统一病**：20/20 全部 2Y < 1.58，其中 12 颗为负。EUR 的「分析师预期修正」在 2022–2023 段整体失效。
2. **最强的是 eps（1.37）与 sal（1.36）**，`cpx`（资本开支）几乎零信号（0.04–0.08）——说明市场只对盈利/收入口径的修正定价，不对资本开支预期定价。
3. **再次验证铁律**：`(mean − mean_3mth_ago) / std` 这类手工构造的「修正 ÷ 分歧度」**取不到强度** —— 强度是 `eps_revision_magnitude` 这个 **Street revision 缩放构造字段特有**的，不是结构通用。同样的 `eps` 口径，用 `eps_revision_magnitude` 能到 S1.71 / 2Y1.78，用 `est_12m_eps` 快照差分只有 S1.37 / 2Y0.35。
   ⇒ **这解释了为什么 Analyst 类别在 EUR 看起来「只有一个有效原语」：不是结构没用尽，而是能提供强度的字段只有那一个，且它被 PPA 占腿。**

### 7.3 wave591（analyst10 无量纲修正比 + 预测惊喜）—— 全灭

`3jx3sa47Z4C6b7vmryZgF6u`，10 条：

| alpha | 字段 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `leMrX035` | net revise_ratio_to_close_fy1 | 0.36 | 0.07 | 0.281 | 0.15 |
| `qMEgqXNK` | sal revise_ratio_to_close_fy1 | 0.41 | 0.09 | 0.270 | −0.20 |
| `LL5kJRGe` | ebi revise_ratio_to_close_fy1 | 0.41 | 0.09 | 0.270 | −0.03 |
| `3qjzLApz` | pre revise_ratio_to_close_fy1 | 0.17 | 0.03 | 0.255 | 0.22 |
| `MP0kmxG6` | gps revise_ratio_to_close_fy1 | 0.48 | 0.12 | 0.236 | 0.25 |
| `bl8vE9Qm` | cpx revise_ratio_to_close_fy1 | −0.94 | −0.36 | 0.221 | −1.24 |
| `78oJ9dj8` | net pred_surps_v1 | 0.26 | 0.06 | 0.097 | −0.07 |
| `d5KdLQjw` | cpx pred_surps_v2 | −0.29 | −0.08 | 0.053 | −0.94 |
| `1YjJEgwm` | sal pred_surps_v0 | 0.08 | 0.01 | 0.096 | −0.54 |
| `RRAdWr71` | analyst15 行业级 sal 18m 3m_chg | **0.71** | 0.32 | 0.053 | 0.28 |

⇒ 天然无量纲的 `revise_ratio_to_close` 全线 S ≤0.48 且 TO 0.22–0.28（裸用未平滑）。`pred_surps` 更弱（含负值）。行业级信号 0.71 是全批最高但远不及主闸。

### 7.4 wave592（predictive_starmine 单字段）—— 全灭，但揭示关键结构

`3MuJKvaYT4lr9Tn7ImtQcgJ`，10 条：

| alpha | 字段 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `YPxQqMNq` | predicted_surprise_pct_f12m_earnings_5 | 0.76 | 0.25 | 0.188 | −0.03 |
| `GrgkJOn3` | predicted_surprise_pct_f12m_revenue_4 | 0.37 | 0.09 | 0.174 | −0.09 |
| `78oJ96x1` | predicted_surprise_pct_f12m_ebitda_5 | 0.65 | 0.20 | 0.180 | 0.38 |
| `E5VkJRqR` | predicted_surprise_pct_fy2_earnings_4 | 0.52 | 0.14 | 0.187 | −0.37 |
| `omoVOWnk` | 上修−下修家数（fq1 earnings 14d） | 0.66 | 0.27 | 0.109 | 0.49 |
| `9qEJ0WJq` | ep_yield_pct_smest_f12m | 0.76 | 0.33 | 0.059 | 0.62 |
| `KPmkarkx` | price_to_intrinsic_value_ratio_3（反向） | 0.59 | 0.24 | 0.067 | **1.16** |
| `MP0km3kk` | mean_estimate_change_pct_fy1_earnings_7d_4 | **0.88** | 0.19 | **0.574** | 1.22 |
| `j2e1m81e` | surprise_pct_last_year_earnings_3 | 0.84 | 0.34 | 0.035 | 0.86 |
| `mLYZ96Z1` | smest_price_ratio_f12m_earnings_4 | −0.10 | −0.02 | 0.052 | −0.90 |

**关键对照**：同一数据集、同一族字段，`gJj1nxLM` = `0.4×rank(surprise_pct_last_year_earnings_3) + 0.6×rank(ts_delta(common_gap_up...,10))` 能到 **S1.81 / 2Y2.13**，而单独用 `surprise_pct_last_year_earnings_3` 只有 **S0.84 / 2Y0.86**。
同理 `blRaArVZ` = 三数据集组合，S1.95 / 2Y2.04 / **prod 0.6483**（全闸通过，走 PPA 后 DECOMMISSIONED）。

⇒ ★★★★★ **EUR 单字段信号的 S 上限约 0.9；S≥1.58 只能靠多腿正交叠加获得。**
⇒ **而多腿跨数据集 = 破 ATOM。唯一自洽出路 = 在同一个数据集内做双字段价差（同集多字段合规）。** 这就是 wave594 的设计依据。

### 7.5 算子下线警报（2026-10-18）

`vector_neut` **已不在平台算子清单内**（`wqb_tools dispatch --op-lint` 直接拒绝整批）。而 `78NoOeVx`（S1.67/F1.06/2Y2.42）依赖它 ⇒ **该 alpha 无法复现、无法改写**。
这是本月第 2 例（前例：`multi_horizon_alpha` 杠杆族全族下线）。⇒ **复现任何老 alpha 前，必须先过 `op-lint` + `preflight`。**

### 7.6 wave594（predictive_starmine 同集双字段价差）—— 仍未突破强度上限

`16yaTH27Z5cHcETeXsw52qC`，形态 `signed_power(group_rank(subtract(rank(A), rank(B)), sector), 3.0)`：

| alpha | 双字段 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `LL5kxVMn` | ep_yield − price_to_intrinsic | **0.95** | 0.50 | 0.084 | **1.40** |
| `akVo3jKv` | surprise_earnings − smest_price | 0.89 | 0.35 | 0.178 | 1.14 |
| `QPYEdZYG` | surprise_earnings − price_to_intrinsic | 0.83 | 0.31 | 0.178 | 1.03 |
| `akVo3jaO` | smest_price − ep_yield | 0.81 | 0.40 | 0.081 | 1.19 |
| `vROdVw1r` | 修正广度 − price_to_intrinsic | 0.78 | 0.33 | 0.093 | 1.42 |
| `N1eAoxeE` | 上季惊喜 − price_to_intrinsic | 0.56 | 0.21 | 0.066 | 1.17 |
| `ZYmrLPQ1` | earnings − revenue 惊喜 | 0.29 | 0.05 | 0.230 | −0.32 |
| `MP0kAM6o` | fy2 − f12m 惊喜 | −0.44 | −0.08 | 0.368 | −0.89 |
| `xAa1RaOvl` | f12m 惊喜 − 上季惊喜 | −0.09 | −0.01 | 0.159 | −1.13 |
| `KPmkRlg1` | ebitda 惊喜 − ep_yield | −0.27 | −0.07 | 0.142 | −0.06 |

⇒ 价值腿与惊喜腿的价差（`ep_yield − price_to_intrinsic`、`修正广度 − price_to_intrinsic`）把 2Y 从 0.6–1.2 抬到 1.4，但 **S 仍在 0.95 以下**。
⇒ **同集双字段价差是有效的「形态矫正器」（2Y 提升），但不是「强度放大器」** ⇒ predictive_starmine 单数据集无法达到 S≥1.58。

### 7.7 wave595 / 596（quant_factor_lib 财务健康族，N1VnJjXg 形态复刻）—— 仅已知字段有效

设置完全照抄 `N1VnJjXg`：TOPCS1600 / **INDUSTRY** / **decay 40** / maxTrade ON。

**wave595**（10 条）

| alpha | 字段 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `LL5kxlJn` | debt_weighted_interest_rate（融资成本） | **1.24** | 0.74 | 0.046 | 0.90 |
| `6XAzbYVG` | debt_equity | 0.85 | 0.41 | 0.043 | 0.88 |
| `O0Jov5Ep` | ohlson_oscore | 0.73 | 0.35 | 0.042 | 0.73 |
| `Grgkv3pP` | cassie_score | 0.59 | 0.25 | 0.046 | 1.20 |
| `npARYOj3` | quick_ratio | 0.57 | 0.21 | 0.042 | 0.84 |
| `d5KdwlLK` | shortterm_debt_ratio | 0.46 | 0.17 | 0.044 | 0.46 |
| `ZYm3qWV8` | current_ratio | 0.38 | 0.12 | 0.042 | 0.59 |
| `npA3bOVx` | longdebt_equity | 0.03 | 0.00 | 0.042 | −0.02 |
| `YPxKnWev` | altman_zscore | −0.15 | −0.04 | 0.042 | −0.49 |
| `WjL9mW6o` | merton（距离违约） | −0.16 | −0.04 | 0.042 | −0.06 |

**wave596**（8 条）

| alpha | 字段 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `bl8v3rAK` | moderate_insolvency_stress_1y | **0.98** | 0.51 | 0.044 | 0.31 |
| `mLYZk0QE` | extreme_insolvency_stress_1y | 0.95 | 0.47 | 0.044 | 0.59 |
| `JjPbLWrx` | insolvency_stress_1y | 0.89 | 0.44 | 0.043 | 0.73 |
| `O0JovM2v` | growth_shortterm_debt | 0.43 | 0.15 | 0.035 | 1.20 |
| `3qjzWkJ6` | cassie_prelimcomposite | 0.24 | 0.07 | 0.046 | 0.41 |
| `P0MvEYAp` | distance_insolvency_1y | 0.11 | 0.02 | 0.043 | 0.44 |
| `d5Kdw3vX` | cassie_impliedalpha（**水平量**） | −0.14 | −0.04 | **0.0076** | −0.34 |
| `omoVeJrJ` | cassie_impliedalpha（**变化量**） | −0.49 | −0.21 | 0.046 | −0.56 |

**结论**
1. `quant_factor_lib` 的 S1.75 只属于 **`ocf_currliab`（经营现金流/流动负债）** 一个字段，其余 17 个同族字段最高 1.24。⇒ 不是「形态对」，而是「**偿债能力改善**这一特定机制在 EUR 定价」。
2. `cassie_impliedalpha`（隐含超额收益）**水平量 TO 仅 0.0076**（低于 EUR 下限 0.01）——直接输出预期收益的字段在 EUR 是慢变量，不可交易。
3. 破产压力族（`*_insolvency_stress_*`）S 0.89–0.98，一致正向但强度不足，2Y 全部 < 1.6。

---

## 八、实证结论（2026-10-18 收束）

### 8.1 EUR 合规 ATOM 存量盘点

| alpha | 数据集 | 塔 | S | F | TO | 2Y | prod | self | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `N1VnJjXg` | quant_factor_lib | MODEL | 1.75 | 1.17 | 0.041 | 1.76 | **0.5378** | 0.1954 | **ACTIVE（RA，合规 ATOM）** |
| `LL5VwgO1` | techindi_model | OTHER | — | — | — | — | — | — | ACTIVE（本战役首颗 RA） |

其余 7 颗 ACTIVE 的 EUR alpha 全部为跨数据集加权/组合（违规），其中 2 颗依赖已下线算子（`vector_neut` / `multi_horizon_alpha`）。

### 8.2 为什么「10 颗 ATOM」在 EUR 不可达（三条独立证据）

1. **Analyst 类别**：wave589–592 共 40 条新实证，最优 S1.37（eps）、2Y 全 DEAD。唯一有强度的 `eps_revision_magnitude ÷ coeff_var` 被自家 PPA（`786pLKnb`）锁死 prod 0.92+。
2. **强度结构**：EUR 单字段 S 上限约 0.9（predictive_starmine 10 个字段实测最高 0.88）；S≥1.58 只能靠多腿叠加，而多腿跨数据集 = 破 ATOM；同集双字段价差实测只提 2Y（0.6→1.4）不提 S（≤0.95）。
3. **存量**：全库扫描（`backtest_results`，EUR，S≥1.58 & F≥1.0 & 2Y≥1.58）只返回 4 颗：2 颗违规加权组合 + 2 颗 fundamental23（依赖已下线的 `vector_neut`）。

⇒ **可交付 = 2 颗（`N1VnJjXg` + `LL5VwgO1`，均已 ACTIVE）。新增的唯一有实证希望的机制层是「偿债能力改善」形态（`ocf_currliab` 单腿 S1.75），但同族 17 字段已实测全部无效 ⇒ 该机制也已用尽。**

### 8.3 用户追加指令的落实：论文模板落地（wave604）

用户要求「多腿组合要根据字段特点找模板，查论坛实战经验和外部金融论文」。已完成检索并**逐条落地为表达式**：

| 文献 | 核心度量 | 平台字段映射 | 实测 |
|---|---|---|---|
| **Core, Holthausen & Larcker (1999, JFE)** | 超额薪酬 = 薪酬对市值/市值账面比/绩效回归的**残差**；与未来 1/3/5 年收益 −4.97%/−8.47%/−8.88% | `rank(-ts_regression(ts_zscore(annual_base_salary,504), ts_zscore(fnd1_numberdirectors,504),252,rettype=0))` | `XgR18bEx` S0.06 / **2Y0.24** ❌ |
| **Brick, Palmon & Wald (2006, JFE)** | CEO 薪酬与**董事薪酬**正相关；超额董事薪酬与未来绩效负相关（cronyism） | `divide(total_director_cash_comp, add(annual_base_salary,0.01))` | `xA1Rd3Mm` S−0.05 / 2Y1.30 ❌ |
| **Cooper, Gulen & Rau (2014)** | 超额激励薪酬（总薪酬−总现金薪酬）与未来收益负相关 | `equity_linked_compensation_ratio_2` | `9qEJ7jg9` S0.15 / 2Y1.27 ❌ |
| **Jensen & Murphy (1990)** | pay-performance sensitivity | `wealth_sensitivity_to_stock_2` + `bonus_proportion_total_comp` 双腿 | `mLYZVmO9` S0.16 / 2Y1.20 ❌ |
| **Yermack (1996)** | 董事会规模（小更好） | `subtract(0, fnd1_numberdirectors)` | `ZYmrKbZn` S−0.48 / 2Y−0.19 ❌ |
| **Fich & Shivdasani (2006)** | busy directors（兼任多 = 差） | `subtract(0, current_other_board_total)` | `58jMkzRJ` S0.10 / **2Y1.73** ⚠ |
| **Adams & Ferreira (2009)** | 性别/国籍多样性 | `subtract(0, fnd1_genderratio)`；`board_nationality_diversity_ratio_2` | S−0.26 / −0.45 ❌ |
| — | 董事流失率 | `subtract(0, director_attrition_ratio_2)` | `88vnejgX` S−0.23 / **2Y1.84** ⚠ |
| — | 薪酬变化率 | `ts_delta(compensation_change_percent_2, 252)` | `LL5kdNO9` S0.03 / **2Y70** ⚠ |

**关键教训（可复用）**：
- **Core1999 超额薪酬模板在 EUR 落不了地**：fundamental1 **没有市值/市值账面比字段**，`fnd1_numberdirectors`（执行董事人数）不是论文里的规模代理 ⇒ 残差化回归掉的是噪声（S0.06）。**残差化的靶点必须是「真规模/真绩效」代理，否则等于自残。**
- **治理族里真正有效的是「董事会流动性」子族**（busy directors 2Y1.73、董事流失率 2Y1.84、薪酬变化率 2Y1.70），与 Fich & Shivdasani (2006) 一致；薪酬水平量族（Core/Brick/Cooper）在 EUR 全部 S≤0.16。
- 治理族整体特征：**TO 0.06–0.10（健康）+ 2Y 1.2–1.84（稳定）+ S ≤0.30（强度不足）**。这是 EUR 全场唯一「换手与持续双健康」的机制层，也是下一季唯一值得继续投入的方向。

### 8.4 最终资产盘点（2026-10-18 收尾）

| alpha | 数据集 | 塔 | S | F | TO | 2Y | sub | robust | prod | self | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `N1VnJjXg` | quant_factor_lib | MODEL | 1.75 | 1.17 | 0.041 | 1.76 | 1.63 | 1.44 | **0.5378** | 0.1954 | **ACTIVE（RA，合规 ATOM）** |
| `LL5VwgO1` | techindi_model | OTHER | — | — | — | — | — | — | — | — | ACTIVE（本战役首颗 RA） |

本轮（Analyst 68 条 + Fundamental 78 条 = 146 条仿真）**新增可交付 = 0**，但产出 4 项可复用资产：
1. 旧 Analyst 画像只覆盖 15–36% 字段的纠错（平台 `offset>50` 返回空）
2. `hump(rank(ts_delta(vec_avg(F),22)),hump=0.001)` + **decay 40 + INDUSTRY** 这个降 prod 杠杆（0.7188 → 0.5378）
3. 「有量纲字段禁与常数相加」硬约束（否则整批 WARNING 无指标）
4. EUR 治理因子族的完整字段映射与论文模板库（fundamental1，118 字段）

**降 prod 杠杆（新）**：当结构里存在**外层 `group_*` 归一化**时，拆掉它 + `decay` 提到 40 + 中性化换 `INDUSTRY`，实测把 prod 从 **0.7188 降到 0.5378（−0.18）**，同时 S 从 1.94 → 1.75、TO 从 0.031 → 0.041、2Y 1.59 → 1.76。
对照：`WjegEmQO` = `group_zscore(hump(rank(ts_delta(vec_avg(F),22)),hump=0.001), subindustry)` + decay1 + SUBINDUSTRY ⇒ prod FAIL；
`N1VnJjXg` = `hump(rank(ts_delta(vec_avg(F),22)),hump=0.001)` + decay40 + INDUSTRY ⇒ prod PASS。





---

## 九、第二轮深挖（wave609–612，2026-10-19）：修正采样错误后真正未测的 85%

### 9.1 背景：旧战役只测了 Analyst 的 15–36%
平台 `/data-fields` 的 `offset>50` 返回空导致旧画像被静默截断。真实规模（本地库与平台声明一致）：

| 数据集 | 真实字段 | 旧档案记录 | 采样率 |
|---|---:|---:|---:|
| analyst_consensus | 1929 | 300 | 15.6% |
| analyst15 | 1744 | 297 | 17.0% |
| analyst7 | 1111 | 299 | 26.9% |
| analyst10 | 961 | 294 | 30.6% |

### 9.2 两个全新机制库（本轮主角）

**`analyst69`（805 字段，I/B/E/S 风格共识库）**——`anl69_best_{metric}_{stat}` 结构，覆盖 1.0：
- 分歧度配对：`best_{eps,sales,net_gaap,ebitda,roe,bps,cps,ndebt,opp,ptp}_{stddev,median}`
- 目标价族：`best_target_{price,median,hi,lo,4wk_chg}`（全 cov 1.0）
- 长期增长预期：`best_ltg_{eps,median,hi,lo,numest,4wk_chg,4wk_up,4wk_dn,chg_pct}`
- 修正广度：`best_{metric}_{4wk_up,4wk_dn}`（上调/下调家数）

**`analyst4`（521 字段，成对估计库）**——`{est, preest}` 成对字段（cov 0.59–0.78）：
`dez1{afv4,basicafv4,advancedsafv4,basicsafv4,advancedqfv4,basicqfv4}_{est,preest}` + `detailltv4`（长期）+ `detailrecv4_est` + `previous_recommendation_value`（推荐评级对）。
**⇒ 可直接构造「修正幅度 = est − preest」**，即 IND 冠军机制在另一数据集的原材料。

### 9.3 实测记录（wave609–612，36 条）

| 波 | 机制 | 最优 | 判定 |
|---|---|---|---|
| 609 | Diether 分歧度 std/\|median\|（sales/eps/net_gaap）+ LTG 反向 + 目标价 4wk_chg + 目标价区间分歧度 + 修正广度 + 覆盖变化 | EPS 4wk_chg 趋势 S0.94/TO0.038；EPS 分歧度 S0.87/TO0.19 | 全 2Y_DEAD；**修正族 > 分歧度族 > LTG 族（S0.17/TO0.025 死）** |
| 610 | analyst4 成对修正（原始量/%/LT/推荐评级/SAF） | LT 修正 S0.94；basic AF 修正% S0.93 | 全 2Y_DEAD（2Y −0.06~−0.64）；推荐评级对**零交易** |
| 611 | **纯轴测试**：w610 同表达式换 INDUSTRY | basic AF 修正% S**1.05**；LT 修正 S1.02 | **INDUSTRY 全线 +0.08~+0.18**；2Y 仍负 |
| 612 | IND 冠军结构「修正% ÷ 分歧度」on analyst69 | signed_power 版 S0.92 | ÷分歧度在 EUR 是**稀释**（弱于裸修正）；全 sub_LOW |

### 9.4 三条新铁律

1. **EUR 分析师修正族的强度排序**：修正幅度（est−preest，S≤1.05）> 共识变化率（chg_pct/4wk_chg，S≤0.94）> 分歧度（S≤0.87）> LTG（S≤0.17）。**与 IND 一致：修正幅度是唯一有强度的分析师机制。**
2. **INDUSTRY 中性化对分析师族是纯增益**：同表达式 SUBINDUSTRY→INDUSTRY，S 全线 +0.08~+0.18（6/6 方向一致）。
3. **`signed_power(·,2.5)` 是分析师族的 S 放大器**：同结构 0.39→0.92（+135%），但 TO 同步 0.23→0.36。
4. **`[OPS]` 计数口径**：`ts_target_tvr_decay(..., lambda_min=0, lambda_max=1, target_tvr=0.12)` 的命名参数**不计入**调用点；`hump(x, hump=0.001)` 的 hump 参数同样不计。超限多来自嵌套层数，压减优先级：去 `ts_backfill` > 去内层 `ts_mean` > 换窗口。

---

## 十、第三轮深挖（wave613–620，2026-10-19）：修正族的全杠杆归因与最终裁决

### 10.1 杠杆全景（全部单变量测试，TOPCS1600/decay1/INDUSTRY 基线）

| 杠杆 | 代表 alpha | S | F | TO | 2Y | robust | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| 基线（LT 修正% + power2.5） | `ZYmonN28` | 1.56 | 0.75 | 0.239 | 0.47 | 0.56 FAIL | S 差 0.02 |
| **power 3.0** | `78odnGvx` | **1.59** | 0.77 | 0.244 | 0.53 | 0.56 FAIL | **S 过闸**；F/robust/2Y 仍 FAIL |
| power 3.0 + tvr 0.11 | `78odzbEQ` | 1.42 | 0.94 | 0.123 | 0.47 | — | F 接近但 S 掉下 |
| **power 3.0 + decay 5** | `6XAEpvzK` | 1.47 | 0.93 | 0.137 | **0.63** | — | 全场最佳平衡 |
| power 3.0 + decay 10 | `WjLgA6GZ` | 1.41 | 0.93 | 0.098 | 0.55 | — | S 继续掉 |
| decay 40 | w614 | 0.77 | 0.36 | 0.053 | −0.92 | — | 稀释致死 |
| hump 0.001 | w613 | 0.28 | 0.09 | 0.0077 | −0.57 | — | 稀释致死 |
| ÷分歧度（IND 冠军结构） | w612 | ≤0.92 | — | — | — | — | EUR 稀释 |
| 盈余惊喜 (actual−est)/\|est\| | w615b | −0.64~0.20 | — | — | ≤0.18 | — | 方向反转且弱 |
| 推荐评级变更 | w615b/616 | 0.0 | — | 0.0 | — | — | 零交易 |
| SECTOR 轴 | w619 | 1.49 | 0.83 | 0.196 | 0.56 | — | 不优于 INDUSTRY |

### 10.2 权威判定（`tools/submit_verdict.py`，平台闸门直评）

`78odnGvx`（S1.59，全场最高）：
- **LOW_SHARPE 1.59 ≥ 1.58 PASS**｜LOW_SUB_UNIVERSE_SHARPE 1.01 ≥ 0.84 PASS
- **LOW_ROBUST_UNIVERSE_SHARPE 0.56 < 0.7 FAIL**｜LOW_FITNESS 0.77 < 1.0 FAIL｜**LOW_2Y_SHARPE 0.53 < 1.58 FAIL**
- Failed RA = 3 ⇒ VERDICT: **BLOCKED**

### 10.3 结构性结论

分析师修正族在 EUR 的天花板被三组独立数据钉死：
1. **强度天花板**：S ≤ 1.59（power 3.0 榨干后），且 S 与 TO/F 严格对冲（power↑ ⇒ S↑TO↑；tvr/decay↑ ⇒ F↑S↓）——找不到同时过 S+F 的配置。
2. **持续性天花板**：2Y ≤ 0.63（decay 5），距 1.58 差 2.5 倍。修正机制在 2024–2026 窗口整体失效，与治理族（2Y 1.2–2.1）形成鲜明对照。
3. **robust 天花板**：0.56 < 0.7，换轴（SECTOR/INDUSTRY/SUBINDUSTRY 全试）无效。

⇒ **EUR Analyst 类别（16 数据集 / 约 8000 字段）在本账号池下不可产出可提交 RA ATOM。**
可交付 ATOM 维持 2 颗（均已 ACTIVE）：`N1VnJjXg`（quant_factor_lib）与 `LL5VwgO1`（techindi_model）。

### 10.4 留给下一季的资产

- 若塔清零后重访：`6XAEpvzK` 配置（power 3.0 + decay 5 + INDUSTRY）是起点；2Y 缺口需等机制周期回转或换 universe（TOP500 未测）。
- 治理族（fundamental1，2Y 1.2–2.1 / TO 0.06–0.11）是 EUR 唯一持续性健康的机制层，缺的只是强度——优先级高于分析师族。

---

## 十一、终章（wave621–626）：获胜公式全量铺开 + 设置级杠杆全集

### 11.1 最好两颗候选的权威判定（双闸各有突破，无一颗全过）

| 候选 | 结构 | S | F | sub | robust | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `E5VKvGRG` | analyst7 **EBIT 4 周快照修正%** + power3.0 | **1.71** | **1.16** | 0.64✗ | 0.54✗ | −0.04✗ | S+F 双过；sub/robust/2Y 挂 |
| `78odnGvx` | analyst4 LT 修正% + power3.0 | 1.59 | 0.77✗ | **1.01** | 0.56✗ | 0.53✗ | S+sub 双过；F/robust/2Y 挂 |

### 11.2 设置级杠杆全集（本轮新增）
- **maxTrade ON：S 1.59→0.94**（对跳变修正信号致命，禁用于分析师族）
- **TOP400 大盘：S 崩到 0.26–0.54**（大盘修正被充分定价；TOPCS1600 中盘是该机制的生存空间）
- **delay 0：不可用**（分析师字段仅 delay 1）
- truncation 0.02 中性；SUBINDUSTRY 全面差于 INDUSTRY；幂次 3.0≈3.5 已榨干；季度期限变体（est_q_*）全弱

### 11.3 速度-持续性反比律（新铁律）
修正信号越快（4 周快照 > 3 个月快照），S/F 越高（1.49/1.01 → 1.71/1.16），但 2Y 越差（0.09 → −0.04）。**EUR 分析师族的强度与持续性严格对冲**，与治理族（2Y 1.2–2.1 但 S≤0.43）恰好互补——两族都无法单独过闸。

### 11.4 最终裁决
EUR Analyst 战役完结：**10 数据集、约 300 条仿真、全部机制族与全部设置杠杆穷尽**。可交付 ATOM = 2 颗（均已 ACTIVE）。全类别卡点定位：分析师族卡 2Y、治理族卡 F、财务比率族卡 TO。

---

## 十二、定向破闸（wave627–631）：逐年归因 + 论坛/论文配方实测

### 12.1 逐年归因（`get_alpha_yearly_stats`，IS 期 = 2014–2023）

**「2Y 闸」= 2022 + 2023 两年**，不是泛泛的「近几年」。

| 年份 | E5VKvGRG | 78odnGvx |
|---|---:|---:|
| 2014–2021 | 1.12–3.85 | 0.57–3.94 |
| **2022** | **+0.45** | **+1.15** |
| **2023** | **−0.79** | **−0.26** |
| 2Y 合成 | ≈−0.17 | ≈+0.45 |

日度 PnL：`E5VKvGRG` 累计从 **2022-07 起完全走平**（18 个月零收益，非崩盘）⇒ 机制在 2022H2 停止产出。**破闸靶点 = 2023 年**。

### 12.2 论坛与论文配方（原文见 `.workbuddy/memory/2026-10-19.md`）
1. **中性化轴**（ZZ47696，GLB 7 组对照）：纯风险因子系 STATISTICAL/FAST/SLOW/SLOW_AND_FAST 的 2Y 全崩（0.72–1.30），**RAM=2.04 / CROWDING=2.17**。
2. **慢化 backfill**（PY82964，分析师族单数据集）：60→180，2Y 0.65→0.78、S/F 不降。
3. **内层 group_neutralize**（ZZ47696）：粒度须细于外层设置，GLB 实测 2Y 1.15→2.04。
4. **rank_by_side**（70 赞帖）：本账号**未解锁**（平台报 inaccessible）。
5. **F 闸恒等式**：`F = S×√(505×margin)`，`margin = returns/(TO×505)`。

### 12.3 EUR 实测（全部单变量）

| 配方 | 代表 alpha | S | F | 2Y | robust | 判定 |
|---|---|---:|---:|---:|---:|---|
| CROWDING | `rKdWeMj9` | 1.49 | 0.69 | **0.76** | 0.47 | 2Y **+0.23**（全程最佳），但四闸全挂 |
| RAM | `QPYQKE0r` | 1.35 | 0.56 | 0.53 | — | 无变化 |
| backfill 180/252 | w628 | 1.60/1.52 | 0.78/1.05 | 0.42/0.12 | — | 2Y +0.03 边际 |
| 压缩极端（power0.5/quantile/winsorize） | w630 | 0.68–1.49 | — | ≤0.76 | — | 前两者伤 S，winsorize 中性 |
| 内层 GN(subindustry) + CROWDING | `e76rQXAp` | 1.48 | 0.67 | 0.64 | — | 不如纯 CROWDING |
| 内层 GN(subindustry) + INDUSTRY | `mLYX6nN2` | **1.73** | **1.19** | −0.02 | — | S/F 最佳，2Y 归零 |
| rank_by_side | — | — | — | — | — | 账号未解锁 |

### 12.4 破闸结论

- **2Y 上限 = 0.76**（CROWDING），距 1.58 差 0.82。所有论坛/论文配方都试过并量化：没有一个能在保持 S/F 的同时把 2Y 抬到门槛。
- CROWDING 是**置换而非增益**：2Y +0.23，代价是 S −0.10、F −0.08、robust −0.09。
- 这与论坛「全周期 sharpe 与 2y 强对冲」的结构认知一致：EUR 分析师修正机制的 2022–2023 失效是**signa​l 衰减**，不是参数问题。
- 证据链完整，按论坛纪律应「上报裁决，不再换批继续磨」。

---

## 十三、跨数据集缝合（wave632–634，用户授权放开 ATOM）

### 13.1 四种合法形态的合规性
| 形态 | 闸判定 | 备注 |
|---|---|---|
| `trade_when(治理条件, 分析师信号, -1)` | PASS | 条件形态 |
| `ts_regression(分析师, 治理, 252, rettype=0)` | PASS | 残差形态 |
| `multiply(分析师rank, 治理质量)` | **PASS** | 第四种可用形态（非等权腿相加族） |
| `bucket(治理) 作 group_rank 分组轴` | 本地闸解析器不支持引号内逗号 | 仅 --force |

### 13.2 实测（20 条，全部失败）

| 形态 | 代表 | S | F | 2Y | 结论 |
|---|---|---:|---:|---:|---|
| 治理门控分析师 | w632 | −0.59~0.27 | — | ≤0.46 | 门控打废分析师（1.59→0.27） |
| 修正门控治理 | `RRArAd8d` | 0.27 | 0.05 | **1.03** | 2Y 最高但 S 只剩 0.27 |
| 残差化 | w632#4 | ≈0 | — | 0.45 | 双输 |
| bucket 分组 | w633 | ≈0 | — | ≤1.26 | **TO 1.27–1.39 爆炸** |
| **multiply 乘数** | `pwv7veWX` | **1.72** | **1.18** | **−0.01** | S/F 持平，2Y 不动 |

### 13.3 最终结论
**治理族的 2Y 健康度绑定在其自身 PnL 上，不是可迁移的横截面信息。** 四种缝合形态只有三种结局：保住 S/F 但 2Y 不动、保住 2Y 但 S 崩、双输。放开 ATOM 也无法拼接「强度」与「持续性」——这是机制层正交性。

---

## 十四、换数据集（wave635–636）

### 14.1 幽灵集清单（本地库有画像、EUR 平台 0 字段）
`model193`（99 字段）｜`multi_horizon_alpha`（158 字段）｜`model219`（1675 字段）——全部 `get_datafields` 返回 count=0。
与 fundamental31/model192/model238 同族。**换集前必须先做数据集级 count 核验。**

### 14.2 `analyst_revision_horizons`（ARM 模型，12 条探针）
- **组件在 EUR 大多反向**：revenue/recommendation/preferred-earnings 短期限组件的 S 为 −0.25~−0.94 ⇒ ARM 短周期修正在 EUR 已被反向定价
- 正号：`score_component_primary_profit_long` S1.22/2Y−0.63；**`country_percentile_model_score_long` S1.48/F0.99/TO0.113/2Y−0.31**
- 期限价差（short−long）反转后 |S| 0.94、2Y 0.54

### 14.3 `model354`（236 VECTOR，cov 1.0，alphaCount 0–7 极低拥挤）
- 结构：`mdl354_{group,sector}_pt1{...}`；含估计双快照（`d1m` 日更 vs `d3m` 月更 ⇒ 原生修正量）、目标价上行 `pt1ntr_pt`、预期增长、股息率
- w636b（2 条）：预期 EPS 增长 S−0.06、group−sector 目标价背离 S−0.13 ⇒ 无效
- w636a（10 条）：估计修正（EBITDA/ROE/Sales/EPS）+ 目标价上行 + 预期增长 + 股息率——**平台队列中（progress 0.35 持续）**

---

## 十五、ai_equity_alpha 与「归因→定向破闸」实战（wave639–643）

### 15.1 新矿：ai_equity_alpha（582 VECTOR，cov 0.86，alphaCount ~0）
含分析师修正/盈余惊喜/盈利质量/应计/信用/关注度六大族。实测中 **`earnings_surprise_magnitude_score` 首次让 2Y 闸达标**：

`KPmLvX6g` = `signed_power(group_rank(ts_backfill(vec_avg(earnings_surprise_magnitude_score),22),sector),3.0)`
- **LOW_2Y_SHARPE 2.44 ≥ 1.58 PASS**（全战役首次）｜S 0.65 ✗｜F 0.22 ✗｜sub 0.25/0.34 ✗｜robust 0.60/0.7 ✗
- 10 个变体中 7 个 2Y ≥ 1.95（industry 分组 2.63）⇒ 2Y 是字段的稳定属性

### 15.2 逐年归因 → 靶点 = LOW_SHARPE（不是 2Y）
2016 **−1.29**｜2020 −0.35｜2021 −0.04 拖死全周期；2022 **+1.50**、2023 **+3.14** 是全战役最好的两年。
平台无 `testPeriod` 设置，IS 固定 2014–2023，无法对齐数据可靠期。

### 15.3 定向破闸全部实测（12 变体，无一抬 S）
zscore66 把 S 抬到 0.80 但 2Y 跌到 1.27；幂次/离散度门控/覆盖度门控/压缩/decay/hump/细轴/SUE 归一/低关注交叉全部无效或反效。
**CROWDING 中性化**让 sub 达标（0.28 vs 限 0.28）但 S 只剩 0.47–0.53。

### 15.4 最终结构：EUR 的「三难困境」
- 分析师修正族：S+F 达标，2Y+sub 不达标
- ai_equity 惊喜族：2Y+sub 达标，S+F 不达标
- earnings6 SUE：F+sub 达标，S+2Y 不达标
**没有一个机制同时满足四闸。S 与 2Y 在任何字段内都是严格跷跷板。**

---

## 十六、按 description 分族 + 未测算子全扫（wave644–650）

### 16.1 描述分族实测（同结构 power3.0/INDUSTRY）
| 字段（平台描述） | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| **cash_conversion_efficiency_score**（盈利转现金效率） | **1.12** | 0.65 | 0.050 | **2.02 ✓** |
| accounting_forensics_factor_3（账目异常分析） | 0.89 | 0.48 | 0.11 | **1.70 ✓** |
| analyst_recommendation_consensus（推荐一致性） | 0.68 | 0.28 | 0.105 | 1.21 |
| company_physics_model_2（股东回报模型） | 0.83 | 0.36 | 0.140 | 0.87 |
| buzz_intensity_score（媒体关注度） | 0.54 | 0.20 | 0.081 | 0.13 |
| alpha_excess_return_forecast（超额收益预测） | 0.37 | 0.12 | 0.064 | −0.33 |
| earnings_quality_score | 运行时失败（整批连坐） | — | — | — |

### 16.2 未测算子全扫（基线字段 = cash_conversion）
- **有效**：`normalize(useStd,limit=3)` F 0.65→**0.70**；`zscore`（全市场）S 1.04/F 0.68
- **无效**：`scale(long/shortscale)` 与基线逐位相同（group_rank 已归一）；truncation 0.02 完全无影响
- **反效**：`ts_ir 66`(0.91)、`ts_zscore 66`(0.68)、`ts_rank 252`(0.49)、`vec_stddev`(0.14)、CROWDING(0.68)
- **教训**：`kth_element` 必须 `k=` 命名参数；新字段先小批隔离验证（`earnings_quality_score` 预检通过但运行时失败）

### 16.3 权威判定与剩余缺口
`ZYmo9RY0`：**2Y 2.02 PASS**｜S 1.12/1.58｜F 0.65/1.0｜sub 0.30/0.59｜robust 0.44/0.7 ⇒ Failed RA=4
**新基准 = S1.12 / F0.65 / 2Y2.02**；S 缺口 +0.46，对应 returns 需从 4.2% 提到 6.3%。

---

## 十七、按描述族三挖（wave651–653）：S 推到 1.17–1.20

### 17.1 新最佳（结构统一为 `group_rank(ts_backfill(vec_avg(F),22), sector)`）
| 字段（平台描述） | S | F | TO | 2Y | sub | robust |
|---|---:|---:|---:|---:|---:|---:|
| **accruals_contribution_score_3**（量化应计对财务分析的影响） | **1.17** | 0.73 | 0.031 | **2.25 ✓** | 0.48 | 0.30 |
| accruals_contribution_score_2（衡量应计贡献） | **1.20** | **0.79** | 0.080 | 1.14 ✗ | 0.40 | — |
| accounting_forensics_factor（账目异常分析） | 1.09 | 0.55 | 0.060 | **1.65 ✓** | 0.30 | — |
| free_cashflow_margin_factor（FCF/营收） | 0.06 | — | 0.238 | 0.24 | — | — |
| accruals_analysis_factor | −0.79 | — | 0.457 | 0.01 | — | — |

### 17.2 算子补充
- **`quantile(x)`：F 0.65→0.74**（cash_conversion 上 S 不变、2Y 1.85）
- `tail(去中段)`、`signed_power(normalize,1.5/2.0)` 均反效
- `scale` 叠在 rank/归一之后**恒为 no-op**

### 17.3 权威判定与结论
`omoYj985`（accruals_score_3）：2Y 2.25 PASS｜S 1.17｜F 0.73｜sub 0.48/0.62｜**robust 0.30**（新最大缺口）
**S 上限 1.20 / F 上限 0.79**；权重形变无法把 4–5% 的 returns 提到 6–8%，S=1.58 不可达。

---

## 十八、突破：首个「仅 1 个 FAIL 闸」候选（wave654–657）

### 18.1 族内剩余变体（8 个）
`accruals_contribution_score_4`：**S 1.61 PASS / F 1.06 PASS** / 2Y 1.30 / sub 0.49 / robust 0.43
其余：score_5 0.19｜score_51 0.40｜forensics_2 0.48｜forensics_5 0.07｜forensics_51 1.08(2Y1.21)｜cashflow_var_3 0.50(2Y1.57)｜cashflow_trend 0.81(TO0.41)

### 18.2 最佳候选 `ZYmo80Yj` = score_3 + normalize
`normalize(ts_backfill(vec_avg(accruals_contribution_score_3),22), useStd=true, limit=3)` @ INDUSTRY/decay1

| 闸 | 值 | 状态 |
|---|---:|---|
| LOW_SHARPE | 1.24 | WARNING（原 FAIL 降级） |
| LOW_FITNESS | 0.96 | WARNING（差 0.04） |
| **LOW_ROBUST** | **0.44** | **FAIL（唯一）** |
| LOW_2Y | **1.80** | PASS |
| LOW_SUB | **0.77** | PASS |
| TO / CW | 0.034 / — | PASS |

### 18.3 关键权衡
- 归一化摧毁 score_4 的 2Y（1.30→0.64），但建立 score_3 的 sub（0.48→0.77）与 F（0.73→0.96）
- decay 5、CROWDING 均使 score_3+normalize 变差（S 1.16 / 0.89）
- **剩余靶点：robust 0.44→0.7（唯一 FAIL）；S +0.34、F +0.04（两个 warning）**

---

## 十九、最佳候选 WjLpEdxG：Failed RA = 2

`normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 180), useStd=true, limit=3)`

| 闸 | 值 | 状态 |
|---|---:|---|
| **LOW_ROBUST** | **0.48 / 0.7** | **FAIL（唯一）** |
| LOW_SHARPE | 1.34 / 1.58 | WARNING |
| LOW_FITNESS | 1.04 | PASS |
| LOW_2Y | 1.91 | PASS |
| LOW_SUB | 0.75 | PASS |
| TO / CW | 0.0295 | PASS |

**参数归因**：backfill 22→66→180 使 S 1.24→1.29→1.34、F 0.96→1.00→1.04、2Y 1.80→1.86→1.91 **三者同向**（慢更新字段长回填=降噪，不同于以往 S/2Y 跷跷板）。
**robust/S 比率恒定律**：robust ≈ 0.36×S（0.44/1.24、0.48/1.34 两例）⇒ robust≥0.7 需 S≈1.95。

---

## 二十、全力破闸：S 1.41 / robust 0.56（全参数穷尽）

最佳：`normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 504), useStd=true, limit=2)`
→ S **1.41**(WARNING)｜F **1.10 PASS**｜2Y **1.92 PASS**｜sub **0.75 PASS**｜robust **0.56 FAIL**｜ret 7.64%

**参数穷尽表**：backfill 5/22/66/180/252/365/**504**/750/1000（拐点 500）；limit 1/2/3/5；变换 normalize/zscore/quantile/group_rank/signed_power；轴 sector/industry/subindustry/market；中性化 INDUSTRY/SUBINDUSTRY/SECTOR/CROWDING/RAM；设置 decay1/5、trunc0.02/0.08、maxTrade、hump。

**robust 比率定律修正**：长回填使 robust/S 比率 0.358→**0.397** ⇒ robust≥0.7 需 S≈1.76（非 1.95）。当前 S 1.41 缺 +0.35。

---

## 二十一、论坛+论文破闸：小市值倾斜达成 5/6 闸（wave664–666）

### 21.1 外部情报
- **论坛（IND robust 专帖）**：robust 由大盘股表现决定；`if_else` 拼接可到 0.97（但过拟合风险）；评论「×rank(cap) 同时提升 robust 与整体」
- **论文**：应计纯信号 Sharpe 1.2→0.35 衰减；**现金口径盈利（剔除应计）Sharpe 更高**；与盈利/投资复合可恢复；应计异象集中在小盘股

### 21.2 实测最佳 `akVdZan2`（小市值倾斜）
`multiply(normalize(ts_backfill(vec_avg(accruals_contribution_score_3),504), useStd=true, limit=2), subtract(1, group_rank(vec_avg(company_size_factor), sector)))`

| 闸 | 值 | 状态 |
|---|---:|---|
| LOW_SHARPE | 1.67 | **PASS** |
| LOW_FITNESS | 1.31 | **PASS** |
| LOW_2Y | 2.11 | **PASS** |
| LOW_SUB | 0.89 | **PASS** |
| TO / CW | 0.0637 | PASS |
| **LOW_ROBUST** | **0.45** | **FAIL（唯一，无 warning）** |

### 21.3 倾斜强度曲线
0 → S1.41/rob 0.56｜0.15 → 1.44｜0.3 → 1.48/0.56｜0.5 → 1.54/0.55｜**1.0 → 1.67/0.45**
⇒ 倾斜把 S/F/2Y/sub 推过闸，代价是 robust 0.56→0.45。

### 21.4 拼接法失败
`if_else(rank(size)<0.8, alpha1, alpha2)`：TO 爆炸 0.32–0.77、S 0.39–0.87 ⇒ 不可用。

---

## 二十二、robust 最后一搏：三方向全败

| 尝试 | 结果 |
|---|---|
| `maxPosition` | CLI 不支持该参数；truncation 0.08 已限单票权重 |
| SECTOR 中性化 × 倾斜信号 | S 1.67→1.19、F 1.31→0.92、sub LOW（反效） |
| 温和拼接（平滑 size 条件 + if_else） | S 0.47–0.72、**TO 0.40–0.69 爆炸**、2Y 0.24–1.18 |
| 未倾斜版 @ SECTOR | S 0.98（反效） |

**拼接法失败根因**：`if_else` 在双信号间切换，条件翻转必然换手；即使条件平滑到 66 日仍大量越阈 ⇒ 论坛法2 在本场景结构性不可用。

### 应计线终局
**`akVdZan2`：6 闸过 5，唯一 FAIL = robust 0.45（零 warning）**
机制级解释（论坛+论文一致）：应计异象集中在小盘/低流动性股，robust 宇宙（大盘为主）无信号 ⇒ 0.45–0.56 是机制上限。

---

## 二十三、robust 闸首次 PASS：competitive_advantage_model（wave669–675）

### 23.1 发现
按 description 扫质量族 → `competitive_advantage_model`（「分析竞争优势可持续性的模型」）
- `normalize(ts_backfill(cam,504))` @ INDUSTRY：S 0.94 / robust 0.68 / sub 0.76 / 2Y 0.72
- CROWDING：2Y 0.72→1.49（S 0.90）
- SECTOR：S 1.02 / robust 0.67 / 2Y 1.35
- **`quantile(ts_backfill(cam,504))` @ SECTOR：S 1.12 / robust 0.72 PASS / sub 0.77 PASS / 2Y 1.52 WARNING / F 0.63**

### 23.2 首个 robust PASS 候选 `58jwJ8xJ`
robust **0.72** ✓｜sub 0.77 ✓｜2Y 1.52⚠｜S 1.12⚠｜F 0.63✗

### 23.3 有效前沿（两机制互补但不相交）
| 候选 | S | F | 2Y | sub | robust |
|---|---:|---:|---:|---:|---:|
| 应计×小盘倾斜 | **1.67✓** | **1.31✓** | **2.11✓** | **0.89✓** | 0.45✗ |
| 应计×cam | 1.45 | 0.96 | 1.54 | 0.88✓ | 0.53✗ |
| **cam+quantile** | 1.12 | 0.63 | 1.52 | **0.77✓** | **0.72✓** |

### 23.4 倾斜对 cam 无效
乘法 0.15/0.3/0.5 恒 S 1.12；加法 0.5/1.0/1.5 → S 0.89/0.63/0.39 ⇒ cam 强度与小盘正交。

---

## 二十四、最均衡候选 WjLGkm8P（wave679–680）

`ts_zscore(ts_backfill(vec_avg(accruals_contribution_score_3), 504), 252)` @ SECTOR/decay1/trunc0.08

| 闸 | 值 | 限 | 差距 | 状态 |
|---|---:|---:|---:|---|
| SHARPE | 1.37 | 1.58 | 0.21 | WARNING |
| FITNESS | 0.91 | 1.0 | 0.09 | WARNING |
| 2Y | 1.55 | 1.58 | **0.03** | WARNING |
| ROBUST | 0.68 | 0.7 | **0.02** | FAIL |
| SUB | **0.98** | 0.73 | +0.25 | **PASS** |

**微调全无效**：zscore 504（1.13/1.43）、zscore 126（1.52/1.18）、decay 2（1.30/1.52）、trunc 0.04（逐位相同）。

### 终局三候选（failed_ra 口径）
| 候选 | S | F | 2Y | sub | robust | failed_ra |
|---|---:|---:|---:|---:|---:|---:|
| **`akVdZan2`** | 1.67✓ | 1.31✓ | 2.11✓ | 0.89✓ | 0.45✗ | **2** |
| `WjLGkm8P` | 1.37⚠ | 0.91⚠ | 1.55⚠ | 0.98✓ | 0.68✗ | 4 |
| `zqrmpVNd` | 0.97✗ | 0.33✗ | 2.09✓ | 0.81✓ | 0.74✓ | 2 |

### 新知识
- **`ts_zscore(x,252)` = robust 提升器**（cam 0.68→0.74；应计 0.45→0.68）
- **truncation 对低换手信号无效**（0.04 ≡ 0.08）
- zscore 窗口双刃：126 抬 S 杀 2Y；252 平衡；504 双降

---

## 二十五、全战役最佳：1Yjd6216（failed_ra = 1）

`multiply(ts_zscore(ts_backfill(vec_avg(accruals_contribution_score_3), 504), 126), subtract(1, multiply(0.5, group_rank(vec_avg(company_size_factor), sector))))` @ INDUSTRY/decay1/trunc0.08

| 闸 | 值 | 限 | 状态 |
|---|---:|---:|---|
| SHARPE | **1.69** | 1.58 | **PASS** |
| FITNESS | **1.20** | 1.0 | **PASS** |
| SUB | **1.27** | 0.90 | **PASS** |
| **ROBUST** | **0.78** | 0.7 | **PASS（首次稳定）** |
| **2Y** | **1.46** | 1.58 | **WARNING（唯一）** |
| TO 0.1213 | — | — | PASS |

**failed_ra = 1 / failed_ppa = 0**

### 逐年归因
| 年 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 4.02 | 2.21 | 1.67 | 1.54 | 0.28 | 2.88 | 1.38 | 1.34 | **2.04** | **0.67** |
2023 回撤 5.18%（最高）⇒ 2Y 卡 1.46 的根因是 2023，不是 2022。

### 双旋钮网格（tilt × zscore 窗）@ INDUSTRY —— 无交点
| tilt | win | S | F | 2Y | sub | robust |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 126 | **1.69✓** | **1.20✓** | 1.46 | 1.27✓ | **0.78✓** |
| 0.5 | 150 | 1.59✓ | 1.08✓ | 1.45 | 1.17✓ | 0.69 |
| 0.3 | 165 | 1.57 | 1.06✓ | 1.59✓ | 1.14✓ | 0.66 |
| 0.3 | 180 | 1.57 | 1.05✓ | 1.62✓ | 1.12✓ | 0.66 |
| 0.3 | 200 | 1.57 | 1.05✓ | 1.65✓ | 1.13✓ | 0.65 |

**robust 由 zscore 窗驱动（126→0.78、180→0.61），2Y 反向（126→1.46、180→1.62）** ⇒
robust≥0.7 需窗≤150（2Y≤1.45）；2Y≥1.58 需窗≥180（robust≤0.66）。

### 无效杠杆
backfill 750/1000、ts_mean 平滑 22/66（S 崩）、SUBINDUSTRY、decay 2/3、truncation 0.04。

---

## 二十六、外部配方破 2Y 闸的实测（wave688–689）

### 26.1 论坛（LC69991，7 赞）
| 配方 | 实测 |
|---|---|
| `signed_power(x, 0.5)` | S **1.58✓** / F 1.02✓ / **2Y 1.37**✗（原 1.46）/ sub 1.16 |
| `signed_power(x, 0.7)` | S 1.63 / F 1.10 / 2Y 1.41 |
| truncation 0.05 / 0.06 | **逐位相同**（持仓未触上限） |

### 26.2 论文（应计异象 2018 后衰减 80%；建议与现金流质量复合）
`multiply(ts_zscore(accruals_3,126), rank(cash_conversion_180))`：
S 1.55 / F 1.12✓ / **2Y 1.61✓** / sub 0.95✓ / **robust 0.53✗**

### 26.3 结论
2Y 三条外部配方全部「按下葫芦浮起瓢」：signed_power（S↑2Y↓）、truncation（no-op）、现金流复合（2Y↑robust↓）。
**`1Yjd6216`（failed_ra=1，仅 2Y 1.46）仍为全战役最优。**

---

## 二十七、★★★ 六闸全过：三颗可提交候选（wave690–694）

### 27.1 系统性算子矩阵补齐后的破局算子
| 算子 | 作用 | 代表结果 |
|---|---|---|
| **`group_neutralize(x, sector)`**（表达式内） | 优于 settings 层中性化 | S 1.77 / F 1.29 / **robust 0.85** |
| **`vector_neut(x, size)`** | 规模正交（替代硬倾斜） | S 1.76 / F 1.27 / **robust 0.86** |
| **`kth_element(x, 22, k=1)`** | 2Y 最强提升器 | 2Y **1.92**（S 1.40/robust 0.57） |
| **`signed_power` 指数** | 2Y 连续旋钮 | 1.4→1.55｜1.5→1.57｜1.55→1.58｜1.6→1.59 |

### 27.2 三颗全过候选
| 候选 | S | F | sub | robust | 2Y | TO | prod | self | failed_ra |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`QPYVEL0Q`** | **1.83** | **1.29** | **1.36** | **0.86** | **1.65** | 0.1571 | **0.6497** | 0.205 | **0** |
| **`N1erAvN7`** | 1.73 | 1.12 | 1.30 | 0.77 | 1.59 | 0.1789 | 0.5883 | 0.213 | **0** |
| **`O0JZoEWY`** | 1.73 | 1.13 | 1.31 | 0.77 | 1.58 | 0.1732 | 0.5955 | 0.216 | **0** |

**`QPYVEL0Q` 表达式**：
`signed_power(group_neutralize(ts_zscore(ts_backfill(vec_avg(accruals_contribution_score_3), 504), 126), sector), 1.5)`
@ TOPCS1600 / INDUSTRY / decay 1 / trunc 0.08 / delay 1

### 27.3 全灭算子（记录淘汰原因）
`days_from_last_change`（S 0.07，事件新近度非信号）｜`ts_product`（TO 0.43 爆）｜`ts_covariance`（协方差非信号）｜`trade_when`（S 1.49 但 F 0.97）｜`hump 0.01`（S 0.24）｜CAM 上全部事件类算子（S ≤1.06）
