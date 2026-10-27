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

**根因**（2026-10-20 实测更正）：平台 `/data-fields` 每页上限 50，但 `dataset.id=` 分页可翻到任意深度
（analyst7 实测 1111/1111、23 页）。旧画像停在 299/300 是**客户端**把 dataset 域拉取截在 300 条并把截断结果缓存，
不是平台在 `offset > 50` 返回空 —— 400 只发生在 `search=` 查询的 `offset+limit > 100` 窗口。
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
1. 旧 Analyst 画像只覆盖 15–36% 字段的纠错（客户端 300 条上限截断，非平台分页限制；2026-10-20 实测更正）
2. `hump(rank(ts_delta(vec_avg(F),22)),hump=0.001)` + **decay 40 + INDUSTRY** 这个降 prod 杠杆（0.7188 → 0.5378）
3. 「有量纲字段禁与常数相加」硬约束（否则整批 WARNING 无指标）
4. EUR 治理因子族的完整字段映射与论文模板库（fundamental1，118 字段）

**降 prod 杠杆（新）**：当结构里存在**外层 `group_*` 归一化**时，拆掉它 + `decay` 提到 40 + 中性化换 `INDUSTRY`，实测把 prod 从 **0.7188 降到 0.5378（−0.18）**，同时 S 从 1.94 → 1.75、TO 从 0.031 → 0.041、2Y 1.59 → 1.76。
对照：`WjegEmQO` = `group_zscore(hump(rank(ts_delta(vec_avg(F),22)),hump=0.001), subindustry)` + decay1 + SUBINDUSTRY ⇒ prod FAIL；
`N1VnJjXg` = `hump(rank(ts_delta(vec_avg(F),22)),hump=0.001)` + decay40 + INDUSTRY ⇒ prod PASS。





---

## 九、第二轮深挖（wave609–612，2026-10-19）：修正采样错误后真正未测的 85%

### 9.1 背景：旧战役只测了 Analyst 的 15–36%
旧画像被客户端 300 条上限静默截断（2026-10-20 复核实测：`dataset.id=` 分页可全量拉取，analyst7 = 1111/1111）。真实规模（本地库与平台声明一致）：

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

> ⛔ **本节结论已于 2026-10-19 被平台实测推翻，原文保留仅作教训记录。**
>
> **推翻证据**（`check_correlation(refresh=True)`，2026-10-19 实时拉取，非缓存）：
>
> | 候选 | 存档 prod | **实测 prod** | `[0.9,1]` 桶 | 裁定 |
> |---|---:|---:|---:|---|
> | `QPYVEL0Q` | 0.6497 | **0.9986** | n=1 | 近乎完全克隆 |
> | `N1erAvN7` | 0.5883 | **0.9511** | n=1 | 近乎完全克隆 |
> | `O0JZoEWY` | 0.5955 | **0.9528** | n=1 | 近乎完全克隆 |
>
> 这不是「余量不够、再优化一点就行」，是**三颗各自都有一条生产 alpha 落在 `[0.9,1]`**
> ⇒ 与已上线信号近乎同源，**accruals / `ai_equity_alpha` 这条腿就此关闭**。
>
> **两条方法论教训（比结论本身更值钱）**：
>
> 1. **`failed_ra_count = 0` ≠ 可提交。** `SELF_CORRELATION` / `PROD_CORRELATION` /
>    `DATA_DIVERSITY` / `POWER_POOL_CORRELATION` 落在 `checks.pending`，**不计入**
>    `failed_ra_count`。上表「failed_ra 0」只证明 8 道 IS 闸全过，与相关性毫无关系。
>    判可提交必须逐颗 `check_correlation(type="both", refresh=True)` 实测，不能读 `failed_ra_count`。
> 2. **反过来，`failed_ra_count` 把 WARNING 也算失败**（AGENTS.md §8.7 →
>    `wqb.config.compute_webdata_failed_counts`：18 项 RA check 里 result 既非 PASS 也非
>    PENDING 的都算，WARNING / ERROR 同等）。所以「`checks.fail = []` 但 `failed_ra_count = 1`
>    （LOW_SHARPE 1.46 记为 warning）」**同样不可提交**。⇒ `failed_ra_count` 是唯一可靠口径，
>    `checks.fail` 数组不是。
>
> **归属错误**：这三颗的 `pyramid_short` 实测是 **`model`**（`ai_equity_alpha` 数据集），不是
> `analyst`。本章是 Analyst 战役章节，把它们当 Analyst 塔战果属误挂 —— 点塔计数按平台 category，
> 别按「这波是在挖 analyst」的意图。
>
> **ATOM 合规性（合规 ≠ 可提交）**：`QPYVEL0Q` = `vec_avg(accruals_contribution_score_3)`
> （`ai_equity_alpha` 单数据集）+ `group_neutralize(·, sector)`，`sector` 属 6 个豁免分组字段
> （country / exchange / market / sector / industry / subindustry）之一 ⇒ ATOM 合规。边界定义见
> [`atom_workflow_and_attribution_20261013.md`](../atom_workflow_and_attribution_20261013.md) §2.1：
> **ATOM 画在 dataset id 上，不画在字段数上**；豁免分组字段不计入数据集数。
>
> **铁律④补充**：`N1erAvN7`（p=1.6）与 `O0JZoEWY`（p=1.55）只差一个指数，是同族时序变体；
> 即便 prod 过了也只能出一颗（self-corr 会爆）。存档把它们并列成「三颗」，实际有效上限是两颗。

| 候选 | S | F | sub | robust | 2Y | TO | prod（**存档值，已证伪**） | self | failed_ra |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`QPYVEL0Q`** | **1.83** | **1.29** | **1.36** | **0.86** | **1.65** | 0.1571 | ~~0.6497~~ → **0.9986** | 0.205 | **0** |
| **`N1erAvN7`** | 1.73 | 1.12 | 1.30 | 0.77 | 1.59 | 0.1789 | ~~0.5883~~ → **0.9511** | 0.213 | **0** |
| **`O0JZoEWY`** | 1.73 | 1.13 | 1.31 | 0.77 | 1.58 | 0.1732 | ~~0.5955~~ → **0.9528** | 0.216 | **0** |

**`QPYVEL0Q` 表达式**：
`signed_power(group_neutralize(ts_zscore(ts_backfill(vec_avg(accruals_contribution_score_3), 504), 126), sector), 1.5)`
@ TOPCS1600 / INDUSTRY / decay 1 / trunc 0.08 / delay 1

### 27.3 全灭算子（记录淘汰原因）
`days_from_last_change`（S 0.07，事件新近度非信号）｜`ts_product`（TO 0.43 爆）｜`ts_covariance`（协方差非信号）｜`trade_when`（S 1.49 但 F 0.97）｜`hump 0.01`（S 0.24）｜CAM 上全部事件类算子（S ≤1.06）

---

## 二十八、★ CROWDING 中性化破 prod 墙 + 三轴解耦归因（2026-10-19 下午）

> **本章是本次战役最重要的一章。** EUR 的 prod 墙（区域档案此前判为「47/47 族密墙、结构性穷尽」）
> 在 `analyst_factor_signals` 上被 **CROWDING 中性化**打开；同时把「S 上不去」拆成三个可分离的轴，
> 并给出**单一标量判据（F/S 比）**说明剩下的缺口到底是什么性质 —— 这决定了下一波该扫什么、不该扫什么。

### 28.1 ★ prod 墙破裂实测（同表达式，只换中性化）

表达式（两行逐字相同）：
`signed_power(group_zscore(ts_decay_linear(netprofit_y2_estimate_change_3mo, 10), industry), 1.8)`
@ EUR / TOP2500 / D1 / decay 40 / trunc 0.08 / maxTrade ON

| 中性化 | S | prod | `[0.7,0.8)` 桶 | self | 裁定 |
|---|---:|---:|---:|---:|---|
| **FAST** | **1.74** | 0.7436 | n=2 | — | ❌ PROD_CORRELATION |
| **CROWDING** | 1.46 | **0.6264** | **n=0** | 0.0750 | ✅ `all_passed: true` |

- **代价 −0.28 S，收益 −0.117 prod 且把墙桶清零。** 窗口 22 变体在 CROWDING 下 prod 更低（**0.5905**，self 0.068）。
- 印证论坛帖 `42659822656663` 的断言「中性化必须用 CROWDING」。此前 EUR 档案只按 `settings.json`
  的 SUBINDUSTRY 走，**CROWDING 从未进入过扫描维度** —— 这是档案级盲区，不是运气。
- ⚠ 按 `wq-window-valley-break-prod-wall` 的判据，`[0.7,0.8)` 桶 n=2 ⇒ **窗口微调路线本就该判死**；
  正解是换中性化（改信号结构），不是扫窗口。**该方法论在本区首次被实测验证。**
- ⚠ **推翻 §4.5 第 134 行**「`analyst_factor_signals` prod 被 PPA `786pLKnb` 锁死 0.92+」—— CROWDING 下实测 0.6264。
- ⚠ **推翻封存的 dead_end `EUR-ANALYST-FACTOR-SIGNALS-WEAK`**（wave243，best S 0.31）与
  `references/analyst.md` 第 59 行「EUR 单字段 S 上限约 0.9」：本轮同数据集实测 S 1.48–1.74。
  ⇒ 这两条判死的真实含义是「**在 SUBINDUSTRY/FAST 下**弱」，被误写成了无条件结论。

### 28.2 ★★ 三轴分离：p 是 S 旋钮，group 是 sub/S 旋钮，两者在 industry 上**无交点**

| 分组轴 | sub/S | 说明 |
|---|---:|---|
| `subindustry` | **0.610** | 最优，给出 +0.09 的 sub 余量 |
| `industry` | 0.521 | 刚好压在 0.5196 线上 |
| `sector` | 0.578 | 但 S 崩到 1.02 |
| `group_rank(·, industry)` | 0.611 | **毒药**：S 0.95 / F 0.42 / 2Y 0.89 |

- **在 `industry` 上两约束无交点**：S ≥ 1.58 要求 p ≤ ~1.48，而 sub/S ≥ 0.5196 要求 p ≥ ~1.78。
- **`subindustry` 的价值就是把两者解耦** —— 多出 +0.089 的 sub/S 余量，于是能在 S 峰值附近的低 p 处运行。

**sub-universe 闸公式（本轮再增 ~18 个样本复核）**：`limit = 0.5196 × S`（TOP2500）/ `0.5294 × S`（TOPCS1600），
即 `subuniverse_sharpe ≥ 0.75 × sqrt(sub_size / alpha_size) × alpha_sharpe`。
⚠ **limit 是「每宇宙常数 × S」，但 sub/S 本身是 alpha 特有的** —— 要工程化的是 sub/S，不是 limit。

### 28.3 ★★ subindustry × p × 窗口全扫（CROWDING / TOP2500 / decay 40）—— S 天花板 1.50

| p | w | S | F | sub | sub/S | 2Y | TO | failed_ra | 裁定 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.0 | 10 | 1.40 | 0.78 | 0.66 | 0.471 ✗ | 1.26 ✗ | 0.0369 | 4 | 死 |
| 1.2 | 10 | 1.46 | 0.87 | 0.73 | 0.500 ✗ | 1.46 ✗ | 0.0381 | 4 | 死 |
| **1.4** | **10** | **1.48** | **0.94** | **0.78** | **0.527 ✓** | **1.59 ✓** | 0.0392 | **2** | ← **最优位 `XgR85OK1`** |
| 1.6 | 10 | 1.46 | **0.98** | 0.82 | **0.562 ✓** | **1.66 ✓** | 0.0402 | **2** | 次优 `akVEqgOx`（F 最高） |
| 1.4 | 5 | 1.48 | 0.94 | 0.76 | 0.507 ✗ | 1.55 ✗ | 0.0395 | 4 | 死 |
| 1.2 | 5 | 1.46 | 0.87 | 0.70 | 0.479 ✗ | 1.42 ✗ | 0.0384 | 4 | 死 |
| 1.4 | 3 | **1.50** | 0.96 | 0.76 | 0.507 ✗ | 1.55 ✗ | 0.0396 | 4 | S 最高但 sub 崩 |

- sub/S **随 p 单调上升**（0.471 → 0.500 → 0.527 → 0.562），S **在 p=1.4 见顶**（1.40/1.46/1.48/1.46）
  ⇒ 满足 sub 的最小 p ≈ 1.35，而该区间 S 上限 = **1.48**。
- 窗口越短 S 越高（w3 1.50 > w5 1.48 ≈ w10 1.48 > w15 1.43）**但 sub/S 同步下降** ⇒ 又是跷跷板，窗口不是解。
- **CROWDING 下 S 天花板 ≈ 1.50，距 1.58 差 0.08–0.10。p / 窗口 / 分组三轴已全部扫尽。**

**字段替换全灭（「同族凑多颗」的希望破灭）**：

| 字段 | S | F | sub | sub/S | 2Y |
|---|---:|---:|---:|---:|---:|
| `netprofit_y2_estimate_change_3mo` | **1.48** | 0.94 | 0.78 | **0.527 ✓** | 1.59 ✓ |
| `eps_y2_estimate_change_3mo` | 1.36 | 0.83 | 0.59 | 0.434 ✗ | 1.59 ✓ |
| `netprofit_y1_estimate_change_3mo` | 1.17 | 0.66 | 0.30 | 0.256 ✗ | 1.09 ✗ |
| `eps_y1_estimate_change_3mo` | 1.14 | 0.63 | 0.23 | 0.202 ✗ | 0.94 ✗ |

⇒ **y2 期限唯一可用，y1 全灭**（远期预期修正才有信号，近端已被市场消化）；`netprofit` 优于 `eps`。
**这条族只能出 1 颗，不是 4 颗**（叠加铁律④：同族变体 self-corr 会爆）。

### 28.4 ★ SLOW_AND_FAST 全灭（新判死轴 + 机制解释）

同族 10 条 @ SLOW_AND_FAST / industry+subindustry+sector / p 0.6–2.2：**S 全部落在 0.49–0.84**
（最好 `xA1dgMZg` p=1.0 → S 0.84 / F 0.36 / sub 0.30；`group_rank` 版 S 0.49 / F 0.13）。

- 对照 CROWDING 同结构 S 1.46–1.48 ⇒ **SLOW_AND_FAST 净损失 −0.6 到 −1.0 S**。
- **机制解释（这才是可复用的部分）**：SLOW_AND_FAST 同时剥掉动量与反转两个成分，
  而本信号的经济内容**就是**「远期盈利预期修正的动量」⇒ 中性化把信号本身当风格因子剥掉了。
- **可复用结论：在「预期修正 / revision」族上禁用 SLOW_AND_FAST** —— 这不是调参问题，是机制冲突，
  任何 p / 窗口 / 分组都救不回来（已实测 p 0.6→2.2 全域）。

### 28.5 ★★★ 关键判据：缺口是「单一标量强度」，不是「比率失衡」

最优位 `XgR85OK1`：S 1.48 / F 0.94 ⇒ **F/S = 0.635**。
过闸要求 S ≥ 1.58 **且** F ≥ 1.0 ⇒ 需要 **F/S ≥ 1.0 / 1.58 = 0.633**。

> **0.635 ≥ 0.633 —— 比率已经达标了。**

⇒ **只要把 S 抬 +0.10 而保持 F/S 不变，F 会同步升到 1.004、S 升到 1.58，两闸同时过。**
剩下的唯一问题是**信号的绝对强度**，不是任何比率型失衡。这直接决定下一波扫什么：

- ✅ **能提纯 / 降噪的轴**：`ts_backfill`（§十九已证使 S/F/2Y **三者同向**）、
  `group_neutralize`（§27.1 已证优于 settings 层中性化：S 1.77 / F 1.29 / robust 0.85）、`decay`、`universe`
- ❌ **只改比率的轴**：p、窗口、分组轴 —— 28.3 已证全部扫尽且都是跷跷板，**再扫是浪费配额**

**returns 反算核对**：`returns = max(TO, 0.125) × (F/S)² = 0.125 × 0.635² = 0.0504`，
与平台报的 returns 0.0504 **逐位吻合** ⇒ 公式在本区可用。
且 **returns 5.04% ≥ 3.5%** ⇒ 按探针 SOP 三分法这**不是判死带**，是「结构没找对」信号带，继续投。

### 28.6 本轮已扫尽 / 判死清单（避免下一会话重跑）

| 轴 | 结论 |
|---|---|
| `group_rank` | 毒药（S 0.95 / F 0.42），CROWDING 与 SLOW_AND_FAST 下都死 |
| `sector` 分组 | S 崩到 1.02（CROWDING）/ 0.50（SLOW_AND_FAST） |
| `ts_mean(x,10)` | ≡ `ts_decay_linear(x,15)`（S 1.43/F 1.20/2Y 2.00 vs 1.43/1.20/1.99）⇒ **不是新杠杆** |
| `ts_scale(·,66)` | S 0.13 |
| `ts_rank(·,126)` | S 0.45 |
| `ts_zscore(·,126)` | S 0.96 / 2Y 0.53 |
| `ts_av_diff(·,66)` | S 0.68 |
| 论坛 mm 结构 `subtract(ts_max_diff, ts_av_diff)` | **EUR analyst 不迁移**：W=66 → S 0.61，W=252 → S 0.37 |
| `ts_max_diff` 单用 | S 0.91（2Y 1.62 ✓ / sub 0.62 ✓）—— 唯一存活但 S 无望 |
| `ts_max` | `[INACCESSIBLE_OP]`，不可用 |
| `hump 0.01` | S 0.24 |
| SLOW_AND_FAST | **整轴判死**（28.4） |
| 比率腿 `revision_magnitude ÷ coeff_var` | **档案特异性**：TOPCS1600/SUBINDUSTRY/decay1 活（`786pLKnb` prod 0.6171），TOP2500 死（FAST S 0.16/1.09/1.03；CROWDING S 0.06/0.80） |

### 28.7 ATOM 合规与交付库存现状

**ATOM 边界**（[`atom_workflow_and_attribution_20261013.md`](../atom_workflow_and_attribution_20261013.md) §2.1）：
画在 **dataset id** 上，不画在字段数上；6 个豁免分组字段
（`country` / `exchange` / `market` / `sector` / `industry` / `subindustry`）不计入数据集数；
`inst_pnl()` / `convert()` 计为 pv1。**塔按 category 计数，ATOM 资格与数据 API 按 dataset id 计数。**

本章全部表达式 = `analyst_factor_signals` 单数据集 + `subindustry`/`industry` 豁免分组 ⇒ **ATOM 合规**。
⚠ targetprice 族（§4.1，单位 `TSPrice`）**只能做同单位比率**：用 `close` 作分母会引入 pv1 ⇒ **破坏 ATOM**。
所以「目标价 ÷ 现价 − 1」这个经济上最自然的构造在本约束下**不可用**，只能走「均值 ÷ 分歧度」的信心口径。

**已确认 ATOM + ACTIVE 库存 = 4 颗**（目标 10，缺 6）：

| alpha | 数据集 | category |
|---|---|---|
| `88vQz5Yl` | `ai_equity_alpha` | MODEL |
| `786pLKnb` | `analyst_factor_signals` | ANALYST |
| `LL5VwgO1` | `techindi_model` | OTHER |
| `N1VnJjXg` | `quant_factor_lib` | MODEL |

⚠ **塔点亮口径按用户裁定 = 提交 ≥ 3 颗**（本季度未达标 ⇒ MODEL 塔虽有 2 颗 ACTIVE 仍**不算点亮**）。
本文档 §一 以「塔计数 = 1」判点亮并据此排除整个 Analyst 类别，**与用户口径冲突，以用户口径为准**。

⚠ **规模约束（决定路线）**：28.3 证明 `analyst_factor_signals` 这一族**只能出 1 颗**，
所以缺口 6 颗**必须靠开新机制腿**，不能在同族里凑。已开：`analyst_consensus` targetprice 族
（§4.1，cov 0.9477，aCnt 0–6，机制与已锁死的 `eps_revision_magnitude` 完全正交）。
待开：`analyst7` 32 个四件套（§4.2，`cpx` / `fcf` / `dps` / `tbv` / `nav` / `grm` 从未测过）。

### 28.8 工程坑（本轮实测踩过）

- **单位陷阱**：`add(stddev_estimate_targetprice_annual12_tribes, 0.01)` 实测 **10/10 全部**
  `Incompatible unit ... expected "Unit[TSPrice:1]", found "Unit[]"`。
  ⇒ 带单位字段**只能与同单位字段做比 / 差**，**绝不能加无量纲常数**（连防零保护的 `+0.01` 都不行）。
- **`preflight_expressions` 对命名参数会误报**：`normalize(x, useStd=true, limit=3)` 被它把
  `normalize` / `useStd` / `limit` 当成三个 unknown **字段**，整批返回 `valid: false`。
  ⇒ 必须读 `fields_checked` 与 `unknown_fields` **逐条判别**，别把 `valid:false` 直接当语法错。
  但反过来：含命名参数的表达式在批量派发里是**连坐风险**（一条 ERROR 整批 CANCELLED），
  故本轮把 `normalize` 那条**撤出批次**单独测 —— 不值得为一条探索性表达式赌一个槽位。
- **`get_datafields` 必填三项**：`region` + `universe` + `dataset_id`
  （此前记的「只需后两项」不全；缺 `region` 报 `params must have required property 'region'`）。
- **`batch_status` 参数是 `simulation_ids`（复数）**。
- **`compute_mutual_correlation` 完全本地**：拉各 alpha 的 PnL 自己算日收益相关，
  **不调平台相关性端点、不占相关性槽** ⇒ 铁律④的互相关去重**免费**，可以随便跑。
  schema：`{alpha_ids: string[] (≥2), threshold: number = 0.5, years: int = 4}`；
  返回 `matrix` / `max_pair` / `pairs_over_threshold` / `max_mutually_below_subset`（贪心最大篮）/ `missing_pnl`。
- **`create_multi_simulation` 参数必须扁平**：传嵌套 `settings` 会被**静默丢弃**并回退 USA/TOP3000
  （工具已把 `region` / `universe` 改为必填以根治）。缺省 `neutralization="INDUSTRY"` / `decay=4` /
  `nan_handling="OFF"` / `max_trade="OFF"` **都不等于本区档案值** ⇒ 每项都要显式传。
- **`*_volatility_adj_1yr` 命名陷阱**：名字像「已按波动率调整」，实际口径需逐字段核，**别按名推义**。

---

## 二十九、2026-10-19 下半轮：decay 轴扫尽、`industry` 破 F 闸、analyst7 维度筛选

> 设置基线（除注明外全部相同）：EUR / TOP2500 / D1 / **CROWDING** / truncation 0.08 /
> maxTrade ON / nanHandling ON / pasteurization ON / VERIFY / FASTEXPR / 2014-01-01→2023-12-31。
> 批次：`31h6091rh5bD8RldKIL4qHC`（decay 4 隔离）、`40SH178Fj5bZa7U1eJy0hivs`（targetprice）、
> `41rHqAgO84CJc8513NnKyLoF`（decay 80）、`LUjho8fb5k5a3EFAuMOvwB`（analyst7）。四批 **40/40 完成、0 ERROR**。

### 29.1 ★★ decay 不是单调杠杆，峰值在 40 —— 轴已扫尽

同一表达式 `signed_power(group_zscore(ts_decay_linear(netprofit_y2_estimate_change_3mo, 10), subindustry), 1.4)`
只改 decay：

| decay | alpha id | S | F | sub | 2Y | TO | returns |
|---:|---|---:|---:|---:|---:|---:|---:|
| 4 | `gJW9zwjm` | 1.29 | 0.77 | 0.63 | 1.25 | 0.0491 | 0.0448 |
| **40** | `XgR85OK1` | **1.48** | **0.94** | 0.78 | **1.59** | 0.0392 | 0.0504 |
| 80 | `LL5dePka` | 1.45 | 0.91 | 0.73 | 1.59 | 0.0359 | 0.0487 |

⇒ **4 → 40 是 +0.19 S，40 → 80 是 −0.03 S。峰值在 40，非单调。**

两条结论：① 区域缺省 `decay 4` 对这条腿是**明确劣化**（−0.19 S / −0.17 F / −0.34 2Y），
复现赢家必须带它自己的 decay（铁律⑤的又一次兑现）；② 我上一轮记的「decay 是唯一活的强度轴」
**到此为止**——80 已越过峰值，decay 轴与 p 轴 / 窗口轴 / 分组轴 / 字段轴一样，**已扫尽**。

### 29.2 ★★★ `industry` 分组在 decay 80 下**首过 LOW_FITNESS**，机制是 returns 不是 F

| 分组 | alpha id | S | F | sub | sub/S | 2Y | returns | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **industry** | `omog21K6` | **1.55** | **1.16 ✓** | 0.70 | 0.452 ✗ | **2.04 ✓** | **0.0706** | 只剩 S(−0.03) + sub |
| subindustry p1.8 | `wp9E68ep` | 1.40 | 0.97 | **0.80 ✓** | **0.571 ✓** | 1.73 ✓ | 0.0594 | 只剩 S(−0.18) + F(−0.03) |
| subindustry p1.4 | `LL5dePka` | 1.45 | 0.91 | 0.73 | 0.503 | 1.59 | 0.0487 | 三闸 |

反算逐位吻合：`F = S × sqrt(returns / 0.125)` ⇒ `1.55 × sqrt(0.0706/0.125) = 1.165` = 平台报的 1.16。

**★★ 这条读数改写了本族的问题定义**：`industry` 与 `subindustry` **不是一根「sub/S 旋钮」上的两档，
而是一组「returns ↔ sub/S」的对价**——

- `industry`：组更粗 ⇒ 组内残差更大 ⇒ 持仓更分散于行业间 ⇒ **returns 从 5.04% 抬到 7.06%**，F 闸直接过（余量 0.16），
  但大市值权重更高 ⇒ **sub/S 掉到 0.452**，sub 闸变成唯一硬约束。
- `subindustry`：组更细 ⇒ 信号更纯 ⇒ **sub/S 0.571 稳过**，但 returns 只有 5.9%，F 闸差 0.03。

⇒ **下一步不是继续在这两档里挑，而是找同时具备「industry 的 returns」与「subindustry 的 sub/S」的结构。**
两个候选已在飞：嵌套 `group_zscore(group_zscore(·, subindustry), industry)`，以及 `country` 分组
（EUR 跨多国，本区面板已登记「country 轴中性化 / 分组有意义」，但**从未实测**）。

### 29.3 ★★ sub 闸的构成被反解出来了：TOP2500 的 sub = TOP1200

已知 `limit = 0.5196 × S`（TOP2500）与底层式 `sub_sharpe ≥ 0.75 × sqrt(sub_size/alpha_size) × alpha_sharpe`。
反解：`0.5196 / 0.75 = 0.6928`，平方 `= 0.47997`，`× 2500 = 1199.9` ⇒ **sub_size = 1200，即 TOP1200**。逐位吻合。
同法 TOPCS1600：`0.5294/0.75` 平方 `×1600 = 797` ⇒ sub ≈ **TOP800**。

**可复用推论（省掉一整批无用回测）**：
① sub 闸的**限值是「宇宙比例的常数 × S」**，所以**换小宇宙并不解除该闸**——比例仍是 ~0.48–0.50，只是换了基准。
**universe 是 S 的杠杆，不是 sub 的杠杆。**
② sub = TOP1200 = **大市值那半边**。实测 sub/S 只有 0.45–0.57 ⇒ **修正信号系统性地在大盘股里更弱**
（大盘定价更有效，远期盈利预期修正已被 price in）。这与 28.3 的「y2 有信号、y1 无信号」是同一件事的两个切面。
③ 因此**别指望靠调 p / 窗口把 sub 抬上去**；要抬 sub 只能换「在大盘里也有效的信号成分」，
即换字段或换经济维度，不是换壳层。

### 29.4 ★ `ts_decay_linear` 在 decay 80 下是**冗余算子**，可删

| 结构（decay 80, subindustry, p1.4） | alpha id | S | F |
|---|---|---:|---:|
| 带 `ts_decay_linear(·, 10)` | `LL5dePka` | 1.45 | 0.91 |
| **裸字段** | `bl8dpYLZ` | **1.53** | **0.98** |

⇒ 外层 decay 80 已经把内层窗口做的事做完了，**内层窗口不仅冗余还略微有害**（−0.08 S）。
按 `wq-alpha-gate-push-op-min` 的算子压缩口径，这一条可直接删掉一个算子调用点。
⚠ 但**在 decay 40 上结论相反**（28.3 的 w10 = 1.48 是本族最高），所以
**「内层窗口冗余」是 decay 的函数，不是普适规则**——删算子前必须在目标 decay 上各测一次。

窗口轴在 decay 80 下也重扫了一遍，仍是跷跷板：w3 1.50 / w5 1.47 / w10 1.45 / w15 1.47，
而 sub 同步下滑（w3 sub/S 0.480、w15 0.490），**没有一档同时过 S 与 sub**。

### 29.5 ★★ `group_neutralize` 在修正族是毒药，且**触发 CONCENTRATED_WEIGHT** —— 机制可复用

decay 4 批里 `group_neutralize` 三档全灭，且**全部带 CONCENTRATED_WEIGHT 告警**：

| 结构 | alpha id | S | F | 2Y | CW 实测（限 0.1） | drawdown |
|---|---|---:|---:|---:|---:|---:|
| `group_zscore(·, subindustry)` | `gJW9zwjm` | 1.29 | 0.77 | 1.25 | — | 0.0707 |
| `group_neutralize(·, subindustry)` | `leM3ZkjA` | 0.56 | 0.41 | 0.22 | **0.135485** | 0.2151 |
| `group_neutralize` p1.6 | `2rjNkQlx` | 0.49 | 0.37 | 0.06 | **0.18992** | 0.2358 |
| `group_neutralize(·, industry)` p1.8 | `E5VeAYv1` | 0.44 | 0.34 | 0.15 | **0.234709** | 0.4456 |

**机制（可迁移到任何重尾字段）**：`group_neutralize` 只**减组均值、不除组内标准差** ⇒
原始量纲与量级被完整保留 ⇒ 重尾字段（修正幅度正是重尾）留下**极少数名字主导整个持仓** ⇒
CW 爆表 + drawdown 翻 3–6 倍 + S 腰斩。`group_zscore` 减均值**再除标准差** ⇒ 有界 ⇒ 不会。

⇒ **可复用规则：重尾 / 带量纲的经济字段（修正幅度、目标价、资本开支…）一律用 `group_zscore`，
禁用 `group_neutralize`；CW 告警出现时先查是不是 `group_neutralize` 而不是先去调 truncation。**

⚠ **同时推翻档案 §27.1**：那里记 `group_neutralize` 更优（S 1.77 / F 1.29 / robust 0.85），
但那是在 `accruals_contribution_score_3` 上测的——**稀疏 VECTOR 字段经 `vec_avg` 聚合后已近似有界**，
与稠密 MATRIX 重尾字段不是一类。**结论按字段类型分层，不能跨类型迁移。**

### 29.6 ★ `ts_backfill` 对**稠密 MATRIX** 字段完全惰性

decay 4 批的三向对照：无 backfill 1.29 → backfill(66) 内层 1.30 → backfill(66) 外层 1.29。
且 backfill 66 ≡ 180（与 `group_neutralize` 组合时两者都是 0.55，逐位相同）。

⇒ **推翻档案 §十九**「backfill 22→66→180 使 S/F/2Y 三者同向」——那条只在**稀疏 VECTOR**字段上成立
（backfill 的作用是填补事件间的空档；稠密 MATRIX 本来就没有空档可填）。
**边界用法已覆盖**：内层 / 外层 / 66 / 180 四种组合全测，无一有效 ⇒ 本族**免测 backfill**。

### 29.7 `analyst_consensus` targetprice 族：**按 returns 判据数学判死**（10/10 全灭）

5 种结构 × 3 个字段变体，全部 decay 4 / CROWDING / TOP2500：

| alpha id | 结构要点 | S | 2Y | sub |
|---|---|---:|---:|---:|
| `RRA1L0ge` | estimate_count 覆盖广度 | **0.41**（本批最高） | −0.95 | — |
| `e76xJeME` | `ts_zscore(mean/stddev, 126)` | 0.29 | **1.77 ✓** | −0.16 |
| `xA1daXLl` | 极差分歧度 | 0.11 | — | — |
| `XgR8EXA0` / `88veqg0W` / `88veqgwW` | mean/stddev 及其 fxadj 版 | −0.07 | — | — |
| `9qE7Qg5r` | median 版 | −0.11 | — | — |
| `j2erQNpE` / `wp9EVXr1` | max/min 版及其 fxadj 版 | −0.14 | — | — |
| `RRA1L0Od` | — | −0.34 | — | — |

**判死依据（探针 SOP 硬判据，不是「试了几个不行」）**：最好读数 `xA1daXLl` 反算
`returns = max(TO, 0.125) × (F/S)² = 0.125 × (0.11/0.41)² = 0.00896` ≈ 平台报的 0.0090。
**returns 0.9% < 3.5% ⇒ F 闸数学封顶**：过 F ≥ 1.0 需 `S ≥ sqrt(0.125/0.009) = 3.73`，
而本族 S 天花板实测 0.41 ⇒ **不可达，判死**。

三条附带实证：
- **fxadj 与非 fxadj 逐位相同**（−0.07/−0.07、−0.14/−0.14）⇒ **汇率/拆股调整在 EUR 对此构造完全惰性**。
  机制：EUR 内主要币种（EUR/GBP/CHF/SEK）经 `group_zscore` 分组标准化后，汇率水平差异已被组内标准化吸收。
  ⇒ **跨币种可比性不是 EUR 的瓶颈，别再为 fxadj 花槽位。**
- `mean/stddev` 构造出 longCount 972 / shortCount 1848 ⇒ **该比值系统性正偏**（分歧度作分母会把正修正压得更狠）。
- 唯一可留的碎片：`e76xJeME` 的 **2Y = 1.77 过闸**（近年有效），但 S 0.29 / sub −0.16 ⇒
  说明**目标价一致预期在近 2 年才有信息量**，全样本被 2014–2019 拖死。若日后开「短窗口 + 近年」腿可回收。

### 29.8 `analyst7` 32 四件套：5 个经济维度**只有 `dps` 活**（10/10 完成）

结构统一为「修正幅度 ÷ 分歧度」= `divide(subtract(mean, mean_<快照>), std)`，decay 40 / CROWDING / subindustry / p1.4：

| 维度 | 3mth 快照 | 4wks 快照 | 裁定 |
|---|---:|---:|---|
| **`dps`** 每股股息 | **1.08**（`rKdPkXL8`，2Y 1.41） | **1.15**（`6XAexOYP`，2Y **2.01**，failed_ra=**2**） | **唯一活口** |
| `fcf` 自由现金流 | 0.36 | 0.55 | 弱 |
| `tbv` 有形账面 | 0.29 | 0.10 | 死 |
| `nav` 净资产值 | −0.03 | （字段未验证，未派） | 死 |
| `cpx` 资本开支 | −0.28 | −0.35 | 死 |
| `cpx` 离散度 `std/mean` | −0.23 | — | 死 |

⇒ **cpx / nav / tbv 判死，同族字段（`est_q_*` 季频版、`_28d` 快照、`opr`/`ebi`/`ebt`/`net`/`eps` 等其余 27 个指标）
按探针 SOP「双结构 S < 0.5 ⇒ 判死且同族字段免测」原则上免测**——但 `dps` 与 `fcf` 打破了这个推定，
所以**免测只适用于「同指标的不同统计量」，不适用于「不同指标」**：指标之间经济含义不同，必须逐个测。
这是本族最重要的一条方法论更正（档案 §4.2 原写「最多 32 条正交腿」，实测 5 个维度里 4 个死）。

⚠ **`dps` 的判死口径要写清楚，别照搬 SOP**：`6XAexOYP` 反算 returns
`= 0.125 × (0.57/1.15)² = 0.0307` ≈ 平台报的 0.0312，**低于 3.5% ⇒ 按 SOP 应判死**
（过 F ≥ 1.0 需 S ≥ 2.00，现 1.15）。**但本族已在 29.2 实测到 returns 是结构依赖量**：
`industry` 分组把另一条腿的 returns 从 5.04% 抬到 7.06%（+40%）。
而 `analyst7` 到目前**只测过 subindustry 一种分组** ⇒
**SOP 的 returns 判死只能在「分组轴也扫尽之后」使用**，否则会把结构未穷尽的腿误杀。
已派 `industry` / `sector` / `country` 三种分组复测 `dps`（批次待收）。

### 29.9 工程坑补充（本轮新增）

- **⚠ `preflight_expressions` 根本不校分组关键字**：一批 10 条里含 `country` / `exchange` / `sector`，
  返回 `fields_checked: ["netprofit_y2_estimate_change_3mo"]`、`builtin_fields: []`、`valid: true`。
  ⇒ 它只校**数据集字段**，把分组关键字整体跳过了，**`valid:true` 对 `country`/`exchange` 是否合法零信息量**。
  铁律①（新数据集首派前逐字段核对平台实时名）**覆盖不到分组字段这个面**。
- **因此分组字段的连坐风险必须用「小批隔离」处置**：一条未知分组字段 ERROR 会 CANCELLED 整批 10 条
  （项目记忆：BRAIN 批量回测单表达式 ERROR 致整批 CANCELLED）。本轮做法 =
  **把未验证的 `country`/`exchange` 单独派成 2 条微批**（`t1Y88cNQ4GobZABea5tYYx`），
  已验证的 `industry`/`sector`/`subindustry` 走 10 条大批（`4haxhZ5Cs4MG9f247dVFd87`）。
  **代价是 2 条也占一个槽位，但换来「大批不因一个未验证关键字全灭」。**
- **`est_12m_nav_mean_4wks_ago` 至今未验证**：`preflight` 返回 `valid:true` 却带
  `warning: "Field pre-check skipped or incomplete: ... get_datafields(offset=0): failed after 6 attempts"`，
  `platform_field_count: 19/20`。⇒ **`valid:true` + `warning` 非空 = 未验证，不是已验证**；
  本轮把该表达式换成了两个已验证字段构成的离散度结构，**不赌槽位**。
- **已验证的 `analyst7` 字段名（19 个，可直接复用）**：`est_12m_{cpx,dps,fcf,tbv}_mean` +
  各自的 `_3mth_ago` / `_4wks_ago` / `_std`，以及 `est_12m_nav_mean` / `est_12m_nav_mean_3mth_ago` / `est_12m_nav_std`。

---

## 三十、2026-10-19（下）：分组轴全扫尽 + 首个双相关性过闸候选 + get_datasets 工具盲区

> 本节记录 5 个分组字段的完整实测、本战役**第一个 prod/self 双过**的候选、
> 三个闸缺口的精确算术，以及一个**会让整类数据集隐形**的工具缺省值。
> 设置除注明外均为 EUR/TOP2500/D1/CROWDING/trunc 0.08/maxTrade ON/nanHandling ON/2014-01-01→2023-12-31。

### 30.1 ★★★★★ 分组轴已全扫尽：sub/S 由「分组粒度」决定，只有 `subindustry` 达标

TOP2500 的 sub 闸要求 `sub_universe_sharpe ≥ 0.5196 × sharpe`（§29.3 反解）。实测 5 个分组字段：

| 分组字段 | 最好结构 | S | F | sub | **sub/S** | 达标？ | failed_ra |
|---|---|---:|---:|---:|---:|---|---:|
| `subindustry` | w10 p1.8 @decay80 (`wp9E68ep`) | 1.40 | 0.97 | 0.80 | **0.571** | ✅ | 2 |
| `subindustry` | w10 p1.4 @decay40 (`XgR85OK1`) | 1.48 | 0.94 | 0.78 | **0.527** | ✅ | 2 |
| `subindustry` | 裸字段 p1.4 @decay80 (`bl8dpYLZ`) | **1.53** | 0.98 | 0.71 | 0.464 | ❌ | 4 |
| `industry` | 裸字段 p1.4 @decay80 (`npA8wwz8`) | **1.63** | **1.25** | 0.71 | 0.436 | ❌ | **1** |
| `country` | w10 p1.4 @decay80 (`RRA108zd`) | 0.84 | 0.66 | 0.27 | 0.321 | ❌ | 4 |
| `exchange` | w10 p1.4 @decay80 (`gJW97MGe`) | 0.85 | 0.67 | 0.28 | 0.329 | ❌ | 4 |
| `sector` | w10 p1.4 / p1.8 (`88veggKa` / `WjLVKKWG`) | 0.89 / 0.70 | 0.70 / 0.55 | 0.39 / 0.16 | 0.438 / 0.229 | ❌ | 4 / 4 |
| 嵌套 `subind→industry` | `MP0L995a` | 1.44 | 0.89 | 0.71 | 0.493 | ❌ | 3 |

**三条可复用结论**：

1. **sub/S 的排序 = 分组粒度排序**：`subindustry`(0.46–0.57) > `industry`(0.436) > `country`≈`exchange`(0.32) > `sector`(0.23–0.44)。
   **只有 `subindustry` 能过 0.5196**，且需要 p ≥ 1.6。
2. **★ 区域面板里「country 轴中性化 / 分组有意义」这条对本族是证伪的**：`country` 分组 S 从 1.53 塌到 **0.84**（−0.69），
   sub/S 0.321，failed_ra 4。⇒ 该面板陈述是**区域级先验，不是族级实证**；跨国家分组会把同一修正信号
   按国别切碎，而 EUR 的分析师修正本身已是跨国可比口径（数据商已做货币/准则归一），再切一刀只损失截面宽度。
   **`market` 是第 7 个豁免分组字段，本轮未测**——但按 country/exchange 的塌陷幅度，预期同死，优先级最低。
3. **嵌套分组无效**（`MP0L995a` returns 0.0481 ≈ subindustry 单层 0.0487）：**外层 industry z-score 不贡献任何信息，
   细粒度分组支配结果**。⇒ 「用嵌套同时拿 industry 的 returns 和 subindustry 的 sub/S」这条路已封死。

### 30.2 ★★★★★ 本战役第一个 prod/self 双过 + IS 7 闸绿的候选：`npA8wwz8`

```
signed_power(group_zscore(netprofit_y2_estimate_change_3mo, industry), 1.4)
```
@ decay **80**：S **1.63** / F **1.25** / 2Y **2.09** / TO 0.0399 / returns **0.0736** / DD 0.0709 /
margin 0.003693 / longCount 1502 / shortCount 1318 / sub 0.71（limit 0.85）。

- **`failed_ra_count = 1`，唯一失败项 = LOW_SUB_UNIVERSE_SHARPE。** LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER /
  HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE / MATCHES_PYRAMID **全过**。
- **`check_correlation(type="both", refresh=True)`：prod `0.6257` PASS，self `0.1340` PASS，`all_passed: true`。**
  prod 直方图 `[0.6,0.7) n=4`、**`[0.7,0.8) n=0`** ⇒ 按 `wq-window-valley-break-prod-wall` 的判据，
  这一族**不在密墙上**，与 §28.1 的 CROWDING 破墙结论互证（同结构 decay40 版 prod 0.6264）。
- self 池只有 4 条（`gJj1nxLM` 0.134 最高），full_os_pool 6，excluded_power_pool 2 ⇒ **self 侧完全空旷**。

**互相关（`compute_mutual_correlation`，本地免费、不占槽）**：`npA8wwz8` / `omogQQ9m` / `omog21K6` / `bl8d77PR`
四者两两 **0.9876–0.9995**；`XgR85OK1`（decay40 subindustry）与它们 0.748–0.793。
`max_mutually_below_subset_size = 1` ⇒ **industry 腿尽管有 4 个成员读数相近，最终只能出 1 颗**（铁律④）。

### 30.3 ★★★★★ 缺口精确化：真正离全闸最近的是 `subindustry p1.8`，不是 `industry`

用 `F = S × sqrt(returns / 0.125)` 反解每格「过 F≥1.0 所需的 S」，再与实测 S 相减：

| alpha | 结构 | returns | 过 F 需 S | 实测 S | **S 缺口** | sub/S | sub 缺口 |
|---|---|---:|---:|---:|---:|---:|---:|
| `wp9E68ep` | w10 subind p1.8 @80 | 0.0594 | 1.450 | 1.40 | **+0.050** | 0.571 ✅ | 无 |
| `bl8dpYLZ` | 裸 subind p1.4 @80 | 0.0516 | 1.556 | 1.53 | **+0.026** | 0.464 ❌ | −0.059 |
| `XgR85OK1` | w10 subind p1.4 @40 | 0.0504 | 1.575 | 1.48 | +0.095 | 0.527 ✅ | 无 |
| `npA8wwz8` | 裸 **industry** p1.4 @80 | 0.0736 | 1.300 | **1.63** | **已超 +0.33** | 0.436 ❌ | **−0.084（p-不变）** |

**⇒ 主攻方向从 industry 转到 subindustry。** 理由：

- industry 的 sub 缺口 **−0.084 是 p-不变的**（§29.4：p 1.4/1.6/1.8 给 sub/S 0.4356/0.4359/0.4354，
  波动 ±0.0003），而分组轴里能提 sub/S 的只有 subindustry，industry 自己动不了 ⇒ **industry 腿结构性无解**。
- subindustry 的缺口只有 **+0.05 S**，且已知一个 **+0.08 S 的杠杆**：删掉 `ts_decay_linear`
  （§29.4：decay80 下裸 1.53 > w10 1.45）。**但「裸 + subindustry + p1.8」这一格从未测过** —— 
  已测的是「裸 + p1.4」（1.53）与「w10 + p1.8」（1.40）。
  若 +0.08 的算子精简增益在 p1.8 同样成立，则 S ≈ **1.48**，配 returns ≈ 0.06 ⇒ F ≈ 1.06 ✅，sub/S ≈ 0.57 ✅ ⇒ **三闸全过**。
- ⚠ 风险登记：裸字段在 p1.4 时 returns 更低（0.0516 vs w10 0.0504@40 / 0.0594@80-p1.8），
  若「裸」同时压低 returns，F 增益会被吃掉。**这一格的结果决定本族能否交付，不要再推测，直接测。**

### 30.4 ★★★★★★ 工具盲区：`get_datasets` 缺省 `theme="false"` 会让整类数据集隐形

**症状**：`get_datasets(category="analyst", region="EUR", delay=1, universe=TOP2500|TOPCS1600)` 一律返回 `count: 0`；
不带 `category` 返回 **91** 条，而本地普查表记的是 **173** 条。

**根因（已实测确认）**：MCP 工具 `get_datasets` 的 `theme` 参数缺省 `"false"`。传 `theme="true"` 后
`category="analyst"` 立刻返回 **count: 16**，与本地普查表逐条吻合。

**算术交叉验证**：缺省调用返回的 91 条里**完全没有** `model` / `analyst` / `news` 三个类别，
而普查表记这三类是 46 + 16 + 20 = **82**，`173 − 82 = 91`，**逐条对得上** ⇒ 不是分页截断，是类别级过滤。

**⇒ 纪律（写入铁律②的补充）**：
1. **任何「某类别在平台上没有数据集」的结论，必须先试 `theme="true"` 再下** —— 否则会得出「EUR 没有 Analyst 数据集」
   这种彻底错误的判断，而本次任务的全部目标正是 Analyst 类。
2. `search=` 参数**匹配的是 description，不是 id**：`search="analyst"` 返回 33 条，其中 `risk72` 命中只因它的
   描述里写了 "analyst earnings estimates"，而 `analyst_factor_signals` / `analyst7` **一条都不在里面**。
   ⇒ **不能用 search 做类别枚举**。
3. 工具缺省值不等于平台缺省值。本次 `theme` 与 2026-08-31 的 `create_multi_simulation` 嵌套 settings 静默回退
   USA/TOP3000 是**同一类事故**（工具层缺省吞掉调用方意图），只是这次是**读侧**、后果是**看不见**而非**测错区**。

### 30.5 EUR × Analyst 全 16 集普查（目标项 1 的交付；`theme="true"` 平台权威枚举）

| 数据集 | 名称 | 字段数 | αC | cov | vS | 本区状态（含本轮结论） |
|---|---|---:|---:|---:|---:|---|
| `analyst_factor_signals` | Global Analyst Factor Signals | 108 | 69 | 0.5458 | 2 | ★ **主攻中**：`npA8wwz8` S 1.63 / prod 0.6257 PASS，只剩 sub 闸（§30.2–30.3） |
| `analyst7` | Broker Estimates | 1111 | 3101 | 0.50 | 1 | ⚠ **部分活**：5 维里只有 `dps` 活（4wks S 1.15 / 2Y **2.01** / failed_ra 2），cpx/nav/tbv/fcf 死（§29.8） |
| `analyst_consensus` | Standardized Analyst Consensus | **1929** | **95** | 0.7027 | 3 | ⚠ **targetprice 族已判死**（returns 0.9%，§29.7），但 1929 字段 / αC 仅 95 = **本类最空旷**，非 targetprice 部分未扫 |
| `analyst10` | Performance-Weighted Estimates | 961 | 1433 | 0.7695 | 2 | predicted-surprise 族已封存（`EUR-ANALYST10-PREDICTED-SURPRISE-DEAD`），其余字段族未扫 |
| `analyst15` | Earnings forecasts | 1744 | 911 | 0.511 | 2 | 行业级已测 best S 0.71（wave589–594），个股级字段未扫 |
| `analyst69` | Fundamental Analyst Estimates | 813 | **14196** | 0.648 | 1 | ❌ 判死（噪声型，平滑即杀）+ **本类最拥挤** |
| `analyst4` | Analyst Estimate Data for Equity | 776 | 3083 | 0.6638 | 1 | ❌ 判死（returns 1.4% < 3.5%，F 闸数学封顶） |
| `analyst11` | ESG scores | 445 | 150 | 0.8489 | 3 | ❌ 判死（S ≤ 0.1，longCount 3–52） |
| `analyst14` | Estimations of Key Fundamentals | 121 | 270 | 0.50 | 1 | **未测**（分支卡列入涉及数据集但回测数为 0） |
| `analyst9` | Analyst Estimate Daily Data | 111 | 78 | 0.6166 | 2 | ❌ 判死（`EUR-ANALYST9-COLD-ZERO-YIELD`，S 0.45） |
| `analyst45` | Analyst Trade Ideas | 61 | 244 | **1.0** | 2 | ❌ 判死（双结构 S 0.36；ret 族另有独立封存） |
| `analyst39` | Analyst estimates & ratios | 24 | 546 | 0.8755 | 2 | ❌ 判死（`EUR-ANL39-EPS-GM-BOOK-WEAK`） |
| `analyst40` | Information on board of director | 22 | **13** | 0.301 | **5** | ❌ 判死（TO 1.50–1.63 爆炸，见普查表 §2.2） |
| `analyst_base_ref` | Analyst Estimates Base Reference | 17 | 7 | 0.5523 | 3 | ⛔ **结构性空集**：平台描述自称 "placeholder ... without containing any actual financial or market data" ⇒ 不投槽位 |
| `analyst81` | Creditworthiness model | **5** | **5** | 0.2402 | **5** | **从未测**（αC 5 = 处女地；风险 = cov 0.24 可能触发 S 不足） |
| `model52` | Creditworthiness model | **3** | **2** | 0.1986 | **5** | **从未测**（αC 2 = 本类最空旷；与 `analyst81` 同主题 ⇒ 同批测可共享归因） |

**未测 / 未扫尽的优先级排序**（按「空旷度 × 与本族机制的距离」）：
1. **`analyst_consensus` 非 targetprice 部分**——1929 字段只测过 targetprice 一族，αC 95 说明全平台都几乎没碰；
   ⚠ 但铁律①要求先逐字段核对平台实时名（该集字段数超 `/data-fields` 的 `offset>50` 返回空的坑，见分支卡 L57）。
2. **`analyst81` + `model52`**——信用/违约概率主题，与「分析师修正」机制**完全正交**，是 10 颗规模缺口最可能的新腿；
   两集合计 8 个字段，一批就能扫完。
3. **`analyst14`**——121 字段、αC 270、cov 0.5，回测数为 0。
4. `analyst10` / `analyst15` 的**非已封存字段族**（961 / 1744 字段，已测的只是极小子集）。

### 30.6 ★★ 归档纠错：「EUR 单字段 S 上限约 0.9」已证伪

`Claude/skills/wq-brain-ra-eur/references/analyst.md` L59（wave589–594 的结论）写：

> ⇒ **EUR 单字段 S 上限约 0.9；S≥1.58 只能靠多腿叠加，而多腿跨数据集破 ATOM。**

**证伪**：`npA8wwz8` 是**单字段单数据集**（`netprofit_y2_estimate_change_3mo` + 分组字段 `industry`，
分组字段属 §2.1 的 6 个豁免字段，不破 ATOM），S = **1.63**，是该上限的 **1.8 倍**。

**为什么当时得出 0.9**：wave589–594 那 60 条全部用的是**区域缺省档**（SUBINDUSTRY 中性化 / decay 4 / TOPCS1600）。
本轮的三个杠杆——**CROWDING 中性化**（§28.1）、**decay 40–80**（§29.1）、**TOP2500 + industry 分组**（§29.2）——
**一个都不在那 60 条的搜索空间里**。⇒ 那条「上限」是**设置档的上限，不是信号的上限**。

**可复用教训（与铁律⑤同源）**：**任何「S 上限 / 强度天花板」的断言，必须写明它是在哪个设置档下测得的**；
换中性化、换 decay、换 universe、换分组粒度都可能整体平移 0.5–0.7 个 S。
本区已因此错杀过一次（`EUR-ANALYST-FACTOR-SIGNALS-WEAK`，wave243 best S 0.31 ⇒ 现已测到 1.63）。

---

## 三十一、2026-10-19（夜）：IS 全闸首次归零 + 中性化与 prod 反向耦合 + 六条腿判死

### 31.1 ★★★★★★ 算子最小化在 p1.8 上复现，F 闸与 sub 闸首次同时通过

Batch E `4hHUfodim5dbcdLRzoq7FLP`（decay 80）/ Batch F `2dWBWF8UU4qRbwC1hbzCg1RF`（decay 40），各 10 条，
设置 TOP2500 / CROWDING / maxTrade ON / truncation 0.08 / nanHandling ON。
下表 bare 格一律 = `signed_power(group_zscore(netprofit_y2_estimate_change_3mo, subindustry), p)`。

| alpha | decay | p | S | F | sub | sub/S | 2Y | TO | returns | DD | failed_ra |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`N1eRWRzp`** | 40 | 1.6 | **1.51** | 1.03 ✅ | 0.78 ✅ | 0.517 | 1.59 ✅ | 0.0410 | 0.0579 | 0.0712 | **1** |
| **`Vkd3wPLG`** | 80 | 1.8 | 1.49 | **1.06** ✅ | 0.78 ✅ | 0.523 | **1.73** ✅ | 0.0383 | 0.0629 | 0.0817 | **1** |
| `j2erlrV9` | 40 | 1.8 | 1.47 | 1.05 ✅ | 0.81 ✅ | 0.551 | 1.63 ✅ | 0.0419 | 0.0638 | 0.0837 | 1 |
| `JjPv0OkW` | 80 | 1.6 | **1.52** | 1.03 ✅ | 0.75 ✗(0.79) | 0.493 | 1.67 ✅ | 0.0374 | 0.0573 | 0.0693 | 2 |
| `2rjNqLo8` | 80 | 2.0 | 1.43 | 1.06 ✅ | 0.80 ✅ | 0.559 | **1.75** ✅ | 0.0391 | 0.0683 | 0.0947 | 1 |
| `wp9EM1j6` | 40 | 1.8(w10) | 1.41 | 0.99 | 0.86 ✅ | 0.610 | 1.69 ✅ | 0.0412 | 0.0617 | 0.0914 | 2 |
| `9qE7P7ld` | 40 | 1.4 | 1.53 | 0.99 | 0.73 ✗(0.80) | 0.477 | 1.52 ✗ | 0.0400 | 0.0521 | 0.0598 | 4 |
| `bl8dpYLZ` | 80 | 1.4 | 1.53 | 0.98 | 0.71 ✗(0.80) | 0.464 | 1.57 ✗ | 0.0365 | 0.0516 | 0.0595 | 4 |

三条结论：

1. **算子最小化（删 `ts_decay_linear`）的增益跨 p 传递**：p1.4 处 +0.08（§30.3），p1.8 处 w10 1.40 → bare 1.49 = **+0.09**。
   ⇒ 不是某一档 p 的巧合，是本族的通用杠杆；`ts_decay_linear` 在 decay 已经 40–80 的档上纯属重复平滑。
2. **p↑ ⇒ sub/S↑ 但 S↓**：p1.4 = 0.464–0.477｜p1.6 = 0.493–0.517｜p1.8 = 0.523–0.610｜p2.0 = 0.559。
   TOP2500 的 sub 闸要求 sub/S ≥ 0.5196 ⇒ **p1.8 是临界格，p2.0 才有安全余量**。
3. §30.3 的预测（bare p1.8 ≈ S 1.48 ⇒ F ≈ 1.06 ⇒ 三闸绿）**逐项兑现**（实测 S 1.49 / F 1.06）。
   困扰三轮的「F 闸与 sub 闸跷跷板」至此打破：**bare + subindustry + p1.6–1.8 同时满足两者**。

### 31.2 ★★★★★★ `submit_verdict` 定案：WARNING 级 LOW_SHARPE 照样硬拦

`Vkd3wPLG`（S 1.49）的 `checks.fail = []`、`sim_fails = []`，看起来「零失败」，但 `submit_verdict` 返回：

```
verdict      : BLOCKED          exit_code : 1
reason_code  : FAILED_COUNT_RA:LOW_SHARPE
reasons      : [{code: FAILED_COUNT_RA, names: [LOW_SHARPE]},
               {code: SUBMIT_HARD_WARN, names: [LOW_SHARPE]}]
next_step    : 先修复上述阻断项并重新回测后再判定；不要绕过（force / 直接 POST 探测均不可取）。
hard_gate_warnings : [{LOW_SHARPE, value 1.49, limit 1.58}]
failed_ra: 1   failed_ppa: 0   pending_gate_names: []
submit_status: 404   submit_layer_view: "dead_endpoint_404"   prepost_unverifiable: true
```

⇒ **`failed_ra_count` 仍是唯一可信读数；`checks.fail` 为空绝不等于放行。** LOW_SHARPE 在平台侧只标 WARNING，
但提交判定层把它归入 `SUBMIT_HARD_WARN` 硬拦。**+0.09 S 是硬需求，不是「好看一点」。**
（附带读数：`sim_warnings` 含 `MATCHES_THEMES` → 主题 `54blOMB`「GLB/D1 TOPDIV3000 Theme」multiplier 2.5、
`CLUSTER_TEST 1.08/1.58`、`OSMOSIS_ALLOCATION`。）

### 31.3 ★★★★★★ 中性化与 prod 反向耦合：IS 全闸归零的格子恰恰过不了 prod

同一表达式 `signed_power(group_zscore(netprofit_y2_estimate_change_3mo, subindustry), 1.8)`、同 decay 80、同 TOP2500，只换中性化：

| 中性化 | alpha | S | F | sub | 2Y | failed_ra | prod | self |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **FAST** | **`QPY9qvGX`** | **1.87** | **1.54** | **1.00** | **1.70** | **0** ✅ | **0.7327** ✗ | 0.2656 ✅ |
| FAST（decay 120） | `E5Vebbw0` | 1.87 | 1.53 | 0.98 | 1.72 | **0** ✅ | **0.7607** ✗ | — |
| CROWDING | `Vkd3wPLG` | 1.49 | 1.06 | 0.78 | 1.73 | 1 | **0.6257** ✅ | ✅ |
| STATISTICAL | `pwvKoW86` | 1.47 | 0.86 | 0.51 | 1.46 | 4 | — | — |

**`QPY9qvGX` 是本战役第一个 `failed_ra_count = 0` 的格子**（9 项 IS 闸全 pass：LOW_SHARPE / LOW_FITNESS /
LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / LOW_2Y_SHARPE /
MATCHES_PYRAMID；returns 0.0843、DD 0.061、margin 0.00333、long 1452 / short 1367），self 0.2656 PASS（池 4）。
**唯一挡它的是 prod 0.7327。**

**★ decay 是 prod 的反向杠杆（实测，非推测）**：同一 FAST 格 decay 80 → 120，**S 纹丝不动（1.87 → 1.87）**，
prod 却 **0.7327 → 0.7607**；直方图同步变厚——`[0.6,0.7)` n **39 → 53**、`[0.7,0.8)` n **1 → 2**。

⇒ **越平滑越像生产池。** 斜率 ≈ +0.0007 prod / decay 单位，从 decay 80 外推 prod = 0.70 的交叉点在 **decay ≈ 33**。
⇒ ⚠ **`wq-window-valley-break-prod-wall` 的「先平滑再找谷」在本格方向相反**，平滑会把墙推得更厚；
要破墙得往 **decay 更低** 走，而不是更高。
⇒ 另注：`[0.7,0.8)` 只有 n = 1（`[0.6,0.7)` 有 39），即**挡路的是单个生产 alpha，不是密墙**；
按该 skill 的族级判据 n ≥ 1 属「窗口微调不可救」，与本格「decay 反向」的实测一致。

**机制解释（可复用）**：FAST 剥掉快变因子后，**剩下的正是生产池里大家共同持有的那部分** ⇒ prod 天然高；
CROWDING 显式剥掉「拥挤持仓」⇒ prod 天然低（0.6257）。
⇒ **中性化决定 prod，p / decay / 分组粒度决定 S 与 sub。两组杠杆近乎正交，可分开调。**
这是本区第一次把「强度」与「相关性」拆成两个独立旋钮。

### 31.4 ★★★★★ 六条腿判死（本轮，均带机制）

| 腿 | 实测 | 机制结论 |
|---|---|---|
| **`group_rank` 替 `group_zscore`** | `1YjzVdAJ` p1.8 subind：S **0.92** / F 0.38 / returns 0.0211 / 2Y 0.58 / CLUSTER −0.06 / long 1237 short 1582（对照 group_zscore 1.49） | **信号住在幅度尾部，不住在次序里** ⇒ 秩压缩把尾部信息抹平。这是我自己「压缩或许能抬 sub/S」假设的直接证伪 |
| `revenue_y2_estimate_change_3mo` | 4 格 S 0.62 / 0.64（subind）、0.70（industry）；@40 0.69 / 0.68；returns 0.022–0.029 | **「y2 有效」是 netprofit 专属事实，不是「期限」属性**——同族同期限换指标即死 |
| `revenue_y1_estimate_change_3mo` | `58jk7kA6` S 0.79 / sub 0.08 / 2Y 0.19 | 同上 |
| `netprofit_y2_estimate_coeff_var`（分歧度） | S 0.55 @p1.4 / 0.49 @p1.8；long 819–949 short 1870–2001 | 分歧度在 EUR 是稀释项（与 §9.3 wave612 同结论），且多空严重失衡 |
| `eps_y2_estimate_change_3mo` | `88vekQWX` p1.8@80 S 1.37 / F 0.94 / sub 0.60（限 0.71）/ 2Y **1.81**；`A1Q7J7eE` p1.4@40 S 1.36 / F 0.84 / sub 0.61 / 2Y 1.57 | 比 netprofit 系统性弱一档且 sub 不达标 ⇒ **netprofit > eps** 确认 |
| 嵌套分组 subind→industry | `MP0L995a` returns 0.0481 ≈ 单层 subindustry 0.0487 | 外层 industry z-score **贡献为零**，细层主导 ⇒ 嵌套是死路 |

### 31.5 ★★★★ 新正交机制：`*_consensus_value`（预期增长**水平**）强负

| alpha | 字段 | 结构 | S | F | returns | DD | sub | 2Y | long/short |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `akVE2n0W` | `netprofit_y2_consensus_value` | p1.4 subind @80 | **−0.86** | −0.44 | −0.0324 | 0.4145 | −0.38 | −1.13 | 953/1867 |
| `1YjzVzKk` | `revenue_y2_consensus_value` | p1.4 subind @40 | **−1.09** | −0.66 | −0.0456 | 0.4887 | −0.55 | −2.27 | 1030/1789 |

⇒ **取反即得 +0.86 / +1.09**。单独不够过闸，但这是教科书式的 **增长陷阱 / 过度乐观异象**
（高预期增长 → 后续失望 → 负收益），与「修正动量」**机制正交**，且 `netprofit_y2_consensus_value` 的 αC 只有 **2**（近处女地）。
**尚未以 `-group_zscore(...)` 形式实测**——这是下一条待开的腿。

### 31.6 ★★★ 工程：MCP 写侧不可靠，读侧走缓存（核验纪律）

- **`create_simulation`（单条）高频返回 `MCP error -32603: MCP tool invocation did not complete`，
  但服务端「可能已建、也可能没建」**：实测 FAST@80 与 STATISTICAL@80 **建成了**，
  SLOW_AND_FAST@80 与 FAST@40/20 **没建成**。⇒ **每次报错后必须核验，既不能假定失败（会漏掉在飞 sim 占槽），
  也不能假定成功（会以为扫过了其实没扫）。**
- **`create_multi_simulation` 报 `Failed to connect to https://api.worldquantbrain.com/simulations`** 时，
  `authenticate` 重建会话（返回 `status_code 201` / `has_jwt true`）后即恢复。这是会话失效，不是 429。
- ⚠ **`get_user_alphas` 可能返回 `from_cache: true`** ⇒ 用它核验「刚派发的 sim 是否建成」**不可靠**，
  必须取 `from_cache: false` 的那次读数，否则会误判为「没建成」而重复派发。
- ⚠ **`create_multi_simulation` 一个 settings 块作用于全部表达式** ⇒ **它做不了设置对比波**（设置扫描必须逐条 `create_simulation`，
  与项目记忆 `brain-multisim.md`「multisim 按表达式去重致设置对比波失效」同源，此处是第二种失效形态：**不去重但也不能分设置**）。
  设置扫描的批量工具是 `batch_create_simulations`（每条自带 settings）。

---

## 三十二、2026-10-19（深夜）：三颗全闸过 + 「一个机制只出一颗」当日自我证伪 + 互相关子集达 4

> 本节补齐 §三十一 之后落地的全部实测。§三十一 写在 decay 40/20/10 突破**之前**，
> 因此它记录的「中性化决定 prod」仍成立，但「同一机制出不了第二颗」的推论**已被本节 32.2 推翻**。

### 32.1 ★★★★★★ IS 全闸归零 ×3：decay→prod 完整单调曲线

同一条表达式 `signed_power(group_zscore(netprofit_y2_estimate_change_3mo, subindustry), 1.8)`，
FAST / TOP2500 / D1，**只改 decay**：

| alpha | decay | S | F | sub | 2Y | TO | returns | DD | failed_ra | **prod** | self | `[0.7,0.8)` n | all_passed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **`KPmE8klx`** | **10** | 1.69 | 1.32 | 0.93 | 1.61 | 0.0639 | 0.0761 | 0.0603 | **0** | **0.6653** ✅ | 0.2771 ✅ | **0** | **true** |
| **`Grge67NZ`** | 20 | 1.72 | 1.36 | 0.97 | 1.72 | 0.0588 | 0.0780 | 0.0571 | **0** | **0.6812** ✅ | 0.2708 ✅ | 0 | **true** |
| **`xA1dQVVm`** | 40 | 1.79 | 1.45 | 0.99 | 1.75 | 0.0543 | 0.0816 | 0.0595 | **0** | **0.6933** ✅ | 0.2732 ✅ | 0 | **true** |
| `9qE76wdo` | 60 | 1.85 | 1.51 | 1.00 | 1.71 | 0.0521 | 0.0834 | 0.0592 | **0** | 0.7090 ✗ | — | 1 | false |
| `QPY9qvGX` | 80 | 1.87 | 1.54 | 1.00 | 1.70 | 0.0506 | 0.0843 | 0.0610 | **0** | 0.7327 ✗ | 0.2656 ✅ | 1 | false |
| `E5Vebbw0` | 120 | 1.87 | 1.53 | 0.98 | 1.72 | 0.0488 | 0.0839 | 0.0648 | **0** | 0.7607 ✗ | — | 2 | false |

**曲线单调、可预测**：斜率 ≈ **+0.0007~0.0010 prod / +1 decay**。我用该斜率外推 decay 60 得 **0.713**，
平台实测 **0.709** —— 误差 0.004。**⇒ prod 从「墙」变成了「旋钮」。**

- ★ **decay 是 prod 的反向杠杆**：信号越平滑，越像生产池。这与常识相反，
  也意味着 `wq-window-valley-break-prod-wall` 的「先平滑再找谷」在**本格方向是反的**。
- ★ **decay 40 是枢轴**：S 已接近上限（1.79 vs 1.87）而 prod 仍过闸 ⇒ **新字段探针一律先用 FAST/decay40**。
- ★ **`[0.7,0.8)` 桶 n 从 2 降到 0** —— 这**字面满足**本区 profile 写明的 probe-only → active 升档条件
  （「出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源」；实测 returns 0.0761–0.0843）。
  改入场状态属控制文件写入 + 人工裁决，**本节只登记不擅动**。

**`Grge67NZ` 逐年 IS 稳健性**（bookSize 20,000,000）：2014 S2.47/F2.05/ret0.0858/DD0.0147 ·
2015 S1.97 · **2016 S−0.11**/ret−0.0051（唯一负年）· 2017 S1.74 · 2018 S2.26 · 2019 S2.37 ·
**2020 S0.32** · **2021 S3.36**/F3.76/ret0.1569（峰）· 2022 S2.28 · **2023 S1.10**/F0.68。
⇒ 8/10 年为正、7/10 年 S ≥ 1.1、多空均衡（1193–1538），**不依赖单年行情**；两面旗：2016 负、2023 衰减到 1.10。

### 32.2 ★★★★★★ 「一个机制只出一颗」—— 当日先立后破（方法论教训）

**先立**：`compute_mutual_correlation(["KPmE8klx","Grge67NZ","xA1dQVVm","2rjNqLo8","Vkd3wPLG"], 0.7, 4yr)`
（`num_points 1021`，`missing_pnl []`）得

| | KPmE8klx (F/d10) | Grge67NZ (F/d20) | xA1dQVVm (F/d40) | 2rjNqLo8 (CROWD/p2.0) | Vkd3wPLG (CROWD/p1.8) |
|---|---:|---:|---:|---:|---:|
| **KPmE8klx** | 1 | 0.9903 | 0.9604 | 0.7237 | 0.7403 |
| **Grge67NZ** | | 1 | 0.9850 | 0.7505 | 0.7660 |
| **xA1dQVVm** | | | 1 | 0.7804 | 0.7946 |
| **2rjNqLo8** | | | | 1 | 0.9939 |
| **Vkd3wPLG** | | | | | 1 |

`max_mutually_below_subset_size = 1`。**即使跨中性化（CROWDING↔FAST）也只到 0.72–0.79，仍 > 0.7。**
⇒ 我当时下的结论是「**任何设置档杠杆都拆不开一个信号**，尺度缺口必须靠真正不同的字段」。

**后破（30 分钟后，Batch G2 收割）**：换上**不同字段 / 不同分组 / 不同期限**后，
`compute_mutual_correlation(["KPmE8klx","xA1dmlVb","WjLVWY3Z","kqJZLV2k","e76xq9op"], 0.7, 4yr)`
（同 1021 点）得

| | KPmE8klx<br>np_y2/subind/d10 | xA1dmlVb<br>**eps_y2**/subind/d40 | WjLVWY3Z<br>np_y2/**industry**/d40 | kqJZLV2k<br>np_**y1**/subind/d40 | e76xq9op<br>**rev_revision_magnitude**/subind/d40 |
|---|---:|---:|---:|---:|---:|
| **KPmE8klx** | 1 | 0.799 ✗ | 0.7835 ✗ | **0.6032** ✓ | **0.4016** ✓ |
| **xA1dmlVb** | | 1 | **0.6888** ✓ | **0.5504** ✓ | **0.4184** ✓ |
| **WjLVWY3Z** | | | 1 | **0.4713** ✓ | **0.3187** ✓ |
| **kqJZLV2k** | | | | 1 | **0.3827** ✓ |
| **e76xq9op** | | | | | 1 |

`max_mutually_below_subset = ["xA1dmlVb","WjLVWY3Z","kqJZLV2k","e76xq9op"]`，**size 4**，`max_subset_exact: true`。

**⇒ 定律被推翻，根因是抽样偏差不是机制**：我那 5 颗全是**同一字段**的设置变体。
可复用结论（**覆盖 32.2 前半段的错误推论**）：

| 轴 | 去相关能力 | 实测区间 |
|---|---|---|
| decay / 中性化 / p（**设置档**） | **无** | 0.72–0.99，全部 > 0.7 |
| 分组粒度（subindustry ↔ industry） | **有** | `KPmE8klx × npA8wwz8 = 0.6392`；`xA1dmlVb × WjLVWY3Z = 0.6888` |
| 字段（同族换指标 / 换期限） | **有** | 0.4713–0.6032 |
| 字段族（estimate_change ↔ revision_magnitude） | **最强** | **0.3187–0.4184** |

⚠ **单换字段不够**（`KPmE8klx × xA1dmlVb = 0.799`）、**单换分组也不够**（`0.7835`）；
**两轴同时换才落到 0.6888**。⇒ 凑 N 颗的配方 = **N 组「字段 × 分组」的笛卡尔组合**，不是 N 个设置档。

⚠ **工作流铁律（本轮实证）**：`check_self_correlation` **只比对已提交 OS 池，查不出 UNSUBMITTED 候选之间的重复**。
证据：`KPmE8klx` 的 self 块只列 `gJj1nxLM` 0.2771 / `78jdv6b1` 0.2122 / `Wj7g2gAx` −0.0903 / `Wj71Q12o` −0.0962
（`pool_size 4`，`full_os_pool_size 6`，`excluded_power_pool_count 2`，`ppac_ids_cached 2`），
**另外两颗同族赢家一次都没出现**。⇒ **规划提交篮子前必须先跑 `compute_mutual_correlation`**。
该工具**完全本地**（逐条拉 PnL、按累计 PnL 差分算日收益相关），**不占平台相关性槽位**。

### 32.3 ★★★★★ Batch G2：FAST 配方横扫 10 腿（`286Oim6Sh4UF8N12Tau122F`，10/10 complete，0 error）

FAST / TOP2500 / D1 / **decay 40** / truncation 0.08：

| alpha | 字段 · 结构 | S | F | TO | returns | DD | sub | sub 限 | 2Y | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`xA1dmlVb`** | **eps_y2**_estimate_change_3mo · subind p1.8 | **1.84** | **1.50** | 0.0553 | 0.0829 | 0.0675 | **0.98** | 过 | **1.71** | **0** ✅ |
| **`WjLVWY3Z`** | netprofit_y2 · **industry** p1.8 | **1.77** | **1.59** | 0.0646 | **0.1007** | 0.0741 | 0.89 | 0.92 | **2.06** | **1** |
| **`kqJZLV2k`** | netprofit_**y1** · subind p1.8 | **1.70** | 1.32 | 0.0554 | 0.0748 | 0.0624 | 0.73 | 0.88 | 1.59 | **1** |
| **`e76xq9op`** | revenue_**revision_magnitude** · subind p1.8 | 1.53 | 1.01 | 0.0546 | 0.0540 | **0.0383** | 0.56 | 0.80 | 0.83 | 3 |
| `mLYVxg32` | −netprofit_y2_consensus_value · subind p1.8 | 1.15 | 0.68 | 0.0483 | 0.0442 | 0.0795 | 0.54 | 0.60 | 0.95 | 4 |
| `JjPv5xEE` | −revenue_y2_consensus_value · subind p1.8 | 1.13 | 0.71 | 0.0478 | 0.0490 | 0.1943 | 0.47 | 0.59 | **2.33** | 3 |
| `rKdPr538` | −eps_y2_consensus_value · subind p1.8 | 0.88 | 0.46 | 0.0482 | 0.0335 | 0.0951 | 0.28 | 0.46 | 0.30 | 4 |
| `KPmEwOd1` | eps_revision_magnitude · subind p1.8 | 0.72 | 0.34 | 0.0566 | 0.0275 | 0.0588 | 0.38 | — | −0.40 | 3 |
| `1YjznxbK` | netprofit_revision_magnitude · subind p1.8 | 0.65 | 0.29 | 0.0560 | 0.0249 | 0.0715 | 0.34 | — | −0.32 | 3 |
| `vROvJkqr` | −netprofit_**y1**_consensus_value · subind p1.8 | −0.15 | −0.03 | 0.0455 | −0.0056 | 0.1578 | −0.22 | −0.08 | 0.22 | 4 |

**归因（不盲扫）**：

1. ★★ **「netprofit > eps」是 CROWDING 档结论，不是信号结论 —— 第三次同型翻案。**
   §31.4 记 `eps_y2` 「系统性弱一档且 sub 不达标」（CROWDING 下 S 1.37 / sub 0.60）。
   **换到 FAST 即 S 1.84 / F 1.50 / sub 0.98 / 2Y 1.71 / failed_ra 0** —— 全批最强格。
   与 `analyst_factor_signals` 的「S 上限 0.9 → 实测 1.87」、analyst39 的「0.88 → 1.21」同一形态：
   **旧数字是「模板 × 设置档」的天花板，被误记成信号的天花板。**
2. ★★ **industry 分组从「结构性死」被 FAST 救到差 0.03。** CROWDING 下 industry 的 sub 比是
   **p 不变量**（p1.4/1.8/2.0 → 0.4356/0.4359/0.4354，限 0.5196）⇒ 当时判「结构不可修」。
   FAST 下 `WjLVWY3Z` sub 0.89 / 限 0.92 = **达标的 96.7%**，且换来**全批最高 returns 0.1007、最高 2Y 2.06、最高 F 1.59**。
   ⇒ **「结构不可修」永远是「在某个设置档下不可修」**。
3. **`e76xq9op` 的 DD 0.0383 是全项目实测最低**（对照冠军 0.0571–0.0648、`JjPv5xEE` 0.1943），
   且它与其它四腿的相关只有 0.32–0.42 = **最强分散器**。但 S 1.53 < 1.58 **且** sub 比 0.366 ≪ 0.5196
   （需 +42%）⇒ **两道结构性缺口，按 D15 判死**，只保留其机制情报：
   **`revision_magnitude`（修正幅度，无符号）只在 revenue 上有信号**（1.53），netprofit / eps 上是 0.65 / 0.72。
4. **§31.5 的增长陷阱异象在 FAST 下复现**：`revenue_y2_consensus_value` 取反 CROWDING p1.4 → +1.09，
   FAST p1.8 → **1.13**，且 **2Y 2.33 是全批最高**。但 DD 0.1943、sub 比 0.416 ⇒ 不可提交。
   **期限对「水平」族有效**：y2 有信号（1.13/1.15），**y1 完全无**（`vROvJkqr` S −0.15）。
   与「修正」族相反（修正族 y1/y2 都强）⇒ **两个族的期限结构不同，不可互相类推**。
5. **外层取反等价性已用于省槽**：`signed_power` 是奇函数、`group_zscore` 线性 ⇒
   `-signed_power(gz(x,g),p) ≡ signed_power(gz(-x,g),p)`。**一条读数即定符号，不必派镜像重复条。**

### 32.4 ★★★★★ analyst39 全灭（`1e3zWtfA64HqcFSOP51tcOH`，10/10 complete，0 error）+ 治理结论的诚实修正

同一 FAST/d40 配方，10 条 `signed_power(group_zscore(anl39_*, subindustry), 1.8)`：

| alpha | 字段 | 族 | S | F | returns | sub | sub 限 | 2Y | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **`9qE7arG1`** | `anl39_rygnhcspe`（最近季 1 年前 EPS 变动 %） | EPS 动量 | **1.21** | 0.73 | 0.0458 | 0.44 | 0.63 | **1.80** | 3 |
| `2rjNaLG6` | `anl39_qepsinclxo` | EPS 水平 | 1.08 | 0.55 | 0.0323 | 0.55 | **0.56** | 0.48 | 4 |
| `gJW9RMrK` | `anl39_qtotd2eq` | 杠杆 | −0.73 | −0.30 | −0.0205 | −0.30 | — | −0.65 | 3 |
| `YPxg20lv` | `anl39_ttmgrosmgn` | 毛利率 | 0.65 | 0.26 | 0.0197 | 0.39 | — | 1.11 | 3 |
| `JjPvgO8l` | `anl39_ghcspemtt` | EPS 动量 TTM | 0.57 | 0.23 | 0.0211 | 0.14 | 0.30 | 0.63 | 4 |
| `mLYVrba6` | `anl39_ghcspea` | EPS 动量 YoY | 0.48 | 0.18 | 0.0184 | −0.08 | 0.25 | 0.33 | 4 |
| `vROvelYQ` | `anl39_atanbvps` | 账面价值 | 0.40 | 0.11 | 0.0103 | 0.32 | — | 0.93 | 3 |
| `pwvKVlWv` | `anl39_grosmgn5yr` | 毛利率 5 年 | 0.38 | 0.11 | 0.0107 | 0.32 | — | 0.48 | 3 |
| `A1Q7gPxX` | `anl39_epschngin` | EPS 动量 前季 | 0.30 | 0.09 | 0.0114 | −0.21 | 0.16 | −1.22 | 4 |
| `WjLVaGYN` | `ts_delta(anl39_ghcspemtt, 60)` | **动量加速度** | 0.09 | 0.01 | 0.0034 | −0.13 | 0.05 | −0.28 | 4 |

**判死（D15）**：最好 S 1.21，距主闸 1.58 差 0.37；`9qE7arG1` 的 sub 比 0.364、`2rjNaLG6` 的 2Y 0.48
都是结构性缺口。**加速度腿（`ts_delta(...,60)`）S 0.09 = 全批最差** ⇒ 「变动」再取变动在 EUR 是纯噪声。

★★ **对 32.9 治理结论的诚实修正（重要）**：本节是**反例**。
`EUR-ANL39-EPS-GM-BOOK-WEAK` 的判死虽然**写的是模板级限定语**（「as 0.30 slow legs with v_rev/falling_wedge」），
但**它的数据集级结论恰好也是对的** —— 换到完全在它限定语之外的 FAST 配方，S 只从 0.88 抬到 1.21，仍差 0.37。
⇒ **「dead_end 是模板级、被 family_dead_datasets 折叠成数据集级」是一条读法纪律（必须先读 `payload.rule` 的限定语），
不是一条「凡判死都可翻案」的许可。** 判别式：
- **可翻案** = 旧 best 的 S 与主闸差距 ≤ ~2×，且旧波**从未扫过**当前设置档（`analyst_factor_signals`：0.9 → 1.87，2.1×，FAST 从未扫）。
- **不可翻案** = 换了完全不同的配方后 S 提升 < 1.5×（analyst39：0.88 → 1.21，1.38×）。

### 32.5 ★★★★ Batch H：分布形状族 6/6 死（FAST/d40/TOP2500，外层取反形）

| alpha | 字段 | S | F | returns | DD | sub | 2Y | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `omogzx8k` | `revenue_y1_estimate_skewness` | **0.50** | 0.18 | 0.0168 | 0.1146 | 0.51 | −0.19 | 3 |
| `QPY9lwMM` | `netprofit_y1_estimate_asymmetry` | 0.44 | 0.11 | 0.0084 | 0.0364 | 0.37 | −0.05 | 3 |
| `wp9Ez0KY` | `eps_y1_estimate_skewness` | 0.41 | 0.14 | 0.0145 | 0.1221 | −0.15 | 1.12 | 4 |
| `gJW9Pnkv` | `netprofit_y1_estimate_skewness_alt` | −0.02 | 0.00 | −0.0006 | 0.1192 | −0.27 | −0.03 | 4 |
| `RRA1aGM0` | `eps_y1_estimate_asymmetry` | −0.40 | −0.10 | −0.0077 | 0.0908 | −0.28 | −0.58 | 4 |
| `ZYmKlO6j` | `netprofit_y1_estimate_volatility_adj_1yr` | −0.79 | −0.34 | −0.0229 | 0.2582 | −0.49 | −0.60 | 4 |

⇒ **偏度 / 非对称 / 估计分歧度这一整族机制在 EUR/D1 死**（最好 |S| 0.50，D15）。
2Y 在 −0.60~+1.12 之间乱跳而全样本 S 极小 ⇒ **近期也没有稳定信号**，不是「旧信号衰减」。
与 §31.4 的 `netprofit_y2_estimate_coeff_var`（S 0.55/0.49，多空 819–949 vs 1870–2001 严重失衡）互证：
**分歧度在 EUR 是稀释项**（同 §9.3 wave612 结论）。

### 32.6 ★★★★ 信用违约赛道死 + **覆盖率 0.30 地板**（三重印证）

`analyst81` + `model52`（批 `2tRfk57w04Tob49Lqt0jIG2`，10/10 complete，0 error，最好 |S| 0.42）：
**每一格都撞 `CONCENTRATED_WEIGHT` 0.5003–0.5008，而限值是 0.1（超 5 倍）**，TO 0.27–0.56。

**机制**：覆盖率 0.20–0.25 时，TOP2500 里**只有约 575 只票带信号** ⇒ 权重必然集中。
⇒ ★ **EUR/D1/TOP2500 的可行性地板 = 覆盖率 ~0.30**。三重独立印证：
`analyst81` cov 0.2402 · `model52` cov 0.1986 · `analyst40` cov 0.301（TO 1.50–1.63）
—— **恰好是普查表里覆盖率最低的三个，也恰好是三个 CW 死的。**

**字段陷阱（登记避免重踩）**：`anl81_class` / `cr_class` 用**打乱序数的编码** ——
9(AAA)、5(AA)、4(A)、1(BBB)、2(BB)、3(B)、7(CCC)、8(CC)、6(C)、10(D)。
⇒ **任何单调算子（rank/zscore/ts_rank）在它上面都无意义**，只能当分组 / 条件变量用。

### 32.7 ★★★★★ EUR × Analyst 全 16 数据集普查（目标步 1 交付；`theme="true"`，含覆盖率地板）

全部 `pyramidMultiplier 1.3`。按覆盖率降序：

| dataset | 平台名 | cov | fields | userCount | alphaCount | valueScore | 裁决 |
|---|---|---:|---:|---:|---:|---:|---|
| `analyst45` | Analyst Trade Ideas | **1.0000** | 61 | 226 | 366 | 2 | **取消资格** —— 返回的 44 字段**全 VECTOR**，`sharpe_filter_removed: 17` |
| `analyst39` | Analyst estimates & financial ratios | 0.8755 | 24 | 850 | 4252 | 2 | **已判死**（§32.4，10/10，best S 1.21） |
| `analyst11` | ESG scores | 0.8489 | 445 | 397 | 918 | 3 | 未开（registry 族级判死） |
| `analyst10` | Performance-Weighted Analyst Estimates | 0.7695 | 961 | 2043 | 7432 | 2 | 未开（`EUR-ANALYST10-PREDICTED-SURPRISE-DEAD`） |
| `analyst_consensus` | Standardized Analyst Consensus Forecasts | 0.7027 | **1929** | 560 | 1406 | 3 | **未开 —— 判死只是模板级**（§32.9） |
| `analyst4` | Analyst Estimate Data for Equity | 0.6638 | 776 | 3335 | **103419** | 1 | 饱和 |
| `analyst69` | Fundamental Analyst Estimates | 0.6480 | 813 | 4825 | **182290** | 1 | 饱和 |
| `analyst9` | Analyst Estimate Daily Data | 0.6166 | 111 | 206 | 637 | 2 | 未开（`EUR-ANALYST9-COLD-ZERO-YIELD`） |
| `analyst_base_ref` | Analyst Estimates Base Reference | 0.5523 | 17 | 134 | 207 | 3 | 描述自称 *"placeholder … without containing any actual financial or market data"* |
| **`analyst_factor_signals`** | Global Analyst Factor Signals | 0.5458 | 108 | 446 | 1069 | 2 | **★ 当前主战场 —— 3 颗全闸过 + 子集 4** |
| `analyst15` | Earnings forecasts | 0.5110 | 1744 | 2270 | 17450 | 2 | 未开 |
| `analyst14` | Estimations of Key Fundamentals | 0.5000 | 121 | 978 | 3335 | 1 | **从未测** |
| `analyst7` | Broker Estimates | 0.5000 | 1111 | 2443 | 30126 | 1 | 未开 |
| `analyst40` | Information on board of director | **0.3010** | 22 | 44 | 72 | 5 | 死（CW 地板） |
| `analyst81` | Creditworthiness model | **0.2402** | 5 | 30 | 44 | 5 | **本战役判死**（§32.6） |
| `model52` | Creditworthiness model | **0.1986** | 3 | 28 | 43 | 5 | **本战役判死**（§32.6） |

⚠ **`get_datasets` 的 description 不可信 / 张冠李戴**：`analyst11`「ESG scores」的描述写的是 RIC↔BBID 映射；
`analyst7`「Broker Estimates」写的是新闻事件摘要；`analyst9` 与 `analyst45` 写的是标识符映射。
⇒ **选集不得依据描述文本**，必须 `get_datafields` 看字段实体。
⚠ `get_datasets` 缺省 `theme="false"` 会**静默隐藏** model / analyst / news 三类；`search=` 匹配描述而非 id。

### 32.8 ★★★★ analyst45 取消资格（零配额）+ analyst39 24 字段普查 + estimate_change 全族

**`analyst45`：cov 1.0 也没用。** `count 44`，`sharpe_filter_applied: true`，**`sharpe_filter_removed: 17`**，
**每个字段 `type: "VECTOR"` / `coverage: 1`**。这是 EUR 预筛失败模式 ①（VECTOR ⇒ TO 爆炸），
必须先用 `vec_*` 聚合；**事件数据的「数据集级覆盖率 1.0」是误导读数**。
旁证该集数据质量：`anl45_bias_weighted_ret` 描述字面写 **"Non-Functional"**、`anl45_treynor_ratio` 描述以 **"??"** 结尾、
7 个字段 uC 0 / αC 0。最多人用的是 `anl45_net_market_exposure`（uC **102** / αC **135**，
"多空想法的分数总价值之差"）。**registry 里另有两条独立判死**：`EUR-analyst45-RET-WEAK`、`EUR-ANL45-TRADE-IDEAS-WEAK`。
⇒ **零配额排除，靠字段类型普查就够**（这正是铁律 ① 的用途）。

**`analyst39` 24/24 MATRIX，`sharpe_filter_removed: 0`**（cov 0.8755，五族）：
EPS 动量 `anl39_ghcspemtt`(0.8922/uC91/αC264) · `anl39_ghcspea`(0.9172/48/85) · `anl39_epschngin`(0.8995/112/185) ·
**`anl39_rygnhcspe`(0.9071/308/1235 ← 最多人用，也是本批最好格)**；
EPS 水平 `anl39_aepsinclxo`(0.9212) · `anl39_roxlcxspea`(0.9212) · `anl39_qepsinclxo`(0.9193/185/398) ·
`anl39_roxlcxspeq`(0.9193) · `anl39_ttmepsincx`(0.9136) · `anl39_xlcxspemtt`(0.9135) · `anl39_ptmepsincx`(0.9029) ·
`anl39_xlcxspemtp`(0.9029)；账面 `anl39_atanbvps`(0.9231) · `anl39_spvba`(0.9231) · `anl39_qtanbvps`(0.9174/210/407) ·
`anl39_spvbq`(0.9174)；杠杆 **`anl39_qtotd2eq`(0.9068/325/683)** · `anl39_qtotd2eq2`(0.8954) ·
`anl39_rasv2_atotd2eq`(0.9119)；毛利率 `anl39_agrosmgn`(0.7692) · `anl39_agrosmgn2`(0.768) ·
`anl39_grosmgn5yr`(0.7016) · `anl39_qgrosmgn`(0.7249) · `anl39_ttmgrosmgn`(0.7237)。

**`analyst_factor_signals` 的 `estimate_change` 全族（9 字段，全 MATRIX，`sharpe_filter_removed: 0`）** ——
★ **这是本轮开出的新轴：期限不只是 FY1/FY2，还有「财季 Q1 × 1 个月窗」**：

| 字段 | cov | uC | αC | 窗口 × 期限 | 状态 |
|---|---:|---:|---:|---|---|
| `eps_y1_estimate_change_3mo` | **0.9311** | **129** | **176** | 3mo × FY1 EPS | 最多人用，Batch I 首测 |
| `eps_y2_estimate_change_3mo` | 0.9310 | 57 | 76 | 3mo × FY2 EPS | **`xA1dmlVb` failed_ra 0** |
| `revenue_y2_estimate_change_3mo` | 0.9278 | 21 | 26 | 3mo × FY2 营收 | 死（S 0.62–0.70） |
| `revenue_y1_estimate_change_3mo` | 0.9273 | 30 | 34 | 3mo × FY1 营收 | 死（`58jk7kA6` S 0.79 / sub 0.08） |
| `netprofit_y2_estimate_change_3mo` | 0.9269 | 34 | 51 | 3mo × FY2 净利 | **★ 冠军字段** |
| `netprofit_y1_estimate_change_3mo` | 0.9268 | 49 | 72 | 3mo × FY1 净利 | `kqJZLV2k` S 1.70 / failed_ra 1 |
| `revenue_q1_estimate_change_1mo` | 0.5245 | 11 | 17 | **1mo × 财季 Q1 营收** | **新轴，Batch I 首测** |
| `eps_q1_estimate_change_1mo` | 0.4614 | 17 | 21 | **1mo × 财季 Q1 EPS** | **新轴，Batch I 首测** |
| `netprofit_q1_estimate_change_1mo` | 0.4307 | **4** | **5** | **1mo × 财季 Q1 净利** | **新轴，近处女地** |

⇒ **修正 §31.4 的结论「y2 有效是 netprofit 专属、不是期限属性」**：该结论只对 **revenue** 成立。
实测 netprofit_y1（1.70）与 eps_y2（1.84）都强 ⇒ **`estimate_change_3mo` 整族在净利/EPS 上都活，只有营收死。**
`q1_1mo` 三字段覆盖率 0.43–0.52，**在 0.30 地板之上**，故可测；但 1 个月窗 ⇒ 预期 TO 显著升高，须盯 HIGH_TURNOVER 0.7。

### 32.9 ★★★★★ 治理：dead_end 是模板级，`family_dead_datasets` 把它折叠成数据集级

已入 registry（win / `registry_governance` / `EUR-DEADEND-TEMPLATE-SCOPED-OVERBLOCK`）。逐字证据：

- **`EUR-ANL39-EPS-GM-BOOK-WEAK`**（id 237，dead_at 2026-08-25，family "analyst39 EPS/margin/book residual x v_rev/wedge"）：
  `best {alpha 6Xlwe9bP, fitness 0.41, sharpe 0.88}`；
  reason *"Wave62 seven analyst39 slows … Max S0.88. Differentiated but far from cheap gate."*；
  **rule *"Do not reuse analyst39 EPS/margin/book residuals **as 0.30 slow legs with v_rev/falling_wedge**."***
- **`EUR-CONSENSUS-SURPRISE-TP-WEAK`**（id 238，同日，family "analyst_consensus surprise/estimate/target x v_rev/wedge"）：
  `best {alpha Xg7pogXl, fitness 0.48, sharpe 0.97}`；
  reason *"Wave63 seven consensus slows … Max S0.97. **Stop resid x PV template grinding.**"*；
  rule *"Do not reuse analyst_consensus surprise/target residuals **as 0.30 slow legs with v_rev/falling_wedge**. Prefer GEM concept generation on NEWS."*

⇒ **两条杀的都是「残差 × PV 两数据集模板」，从没杀过裸单字段 `signed_power(group_zscore(field, subindustry), 1.8)`。**
**我的 analyst39 波在它限定语之外** —— 而它实测也确实死了（§32.4），所以**本条的价值是读法纪律，不是翻案许可**。

⚠ **正在造成实际损害的数据完整性缺陷**：每次 `upsert_registry_empirical` 返回的 `profile_drift` 块里，
`win_datasets: ["analyst_factor_signals"]`，而 **`family_dead_datasets`（45 条）同时也含 `analyst_factor_signals`**，
外加 `analyst10`、`analyst11`、`analyst45`、`analyst9`、`analyst_earnings_ibes`、`analyst_revision_horizons`
—— **我 6 个高覆盖目标里有 4 个被预先封锁**。
且 `unbound_entries` 一路涨 41→42→43→44，hint *"N 条 win/dead_end 条目缺 payload.dataset 绑定，无法进精确层"*；
`EUR-GSM-SAME-SRC-BUCKET-RATIO` 的 `family: null`。**待用户裁决后修，本轮不擅动 registry。**

### 32.10 ★★★ 工具与 schema 事实（全部由报错信息实证）

- **`create_multi_simulation` 的必填参数名是 `alpha_expressions`**（不是 `expressions`）。
  扁平 settings 参数确认可用：`region, universe, delay, decay, neutralization, truncation, max_trade, nan_handling, pasteurization, unit_handling`。
  ⚠ **`max_trade` / `nan_handling` 必须传字符串 `"ON"`，传布尔 `true` 会 400**：
  `"true" is not a valid choice`（每条表达式各报一次）。
- **`harvest_multisim_alphas` 的必填参数名是 `multisimulation_location`**（不是 `simulation_url`）。
  处理中时返回 `{"error":"No children found (multisim may still be processing)"}` —— 这是**待处理态，不是失败**。
- **`batch_status(simulation_ids=[...])` 对合法 multisim 父 id 返回 HTTP 404** ⇒ 对 multisim 父不可靠，
  改走 `harvest_multisim_alphas` 或 `get_user_alphas`。
- **`compute_mutual_correlation(alpha_ids, threshold, years)` 完全本地、不占平台相关性槽**；返回
  `matrix / max_pair / pairs_over_threshold / all_below_threshold / max_mutually_below_subset /
  max_mutually_below_subset_size / max_subset_exact / missing_pnl / num_points / local_calculation`。
- **`TaskUpdate` 与 `TaskGet` 未接入**（"No connected MCP server offers a tool named …"），只有 `TaskCreate` 可用
  ⇒ **任务状态无法标完成，只能在正文与存档里追踪**。
- **`upsert_registry_empirical(region, layer, entry_id, payload[, family, dead_at])`**：按 region+layer+entry_id 幂等，
  与 `campaign.py registry` CLI 共用 `wqb.registry_contract`（DEC-34）。
  **dead_end 需 id/family/reason/rule；win 需 id/what/key；campaign 需 dataset/status；orphan 需 id。**
  `family` **必须同时写在 payload 内**（只给顶层参数不满足校验）。校验失败返回 `{"error": …}` 且不写库。
  每次响应都带 `profile_drift` 块（见 §32.9）。
- **`get_dead_ends(EUR)` 输出 ~68,846 token / 206,537 字符，超 25,000 上限被自动截断存盘**
  ⇒ 必须 Grep / Read 那个临时文件，**不要反复调用**。
- ★ **`submit_verdict` 在 failed_ra=0 的候选上返回 `UNVERIFIABLE`（exit 10，`UNVERIFIABLE_404`，
  `submit_layer_view: "dead_endpoint_404"`）—— `UNVERIFIABLE ≠ BLOCKED`**：GET `/alphas/{id}/submit` 是平台死端点。
  它自己的 note 写明了放行条件：*"平台 prod<0.7 + 用户确认；提交前必须另跑 `check_correlation(alpha_id, refresh=True)`
  并确认 all_passed"*。稳健性台账记录**显式不拦截**（*"本提示不拦截"*）。
  在 failed_ra ≥ 1 时它返回 `BLOCKED`（exit 1）—— **WARNING 级的 LOW_SHARPE 也会硬拦**。
- ★ **`failed_ra_count` 是唯一可靠读数；`checks.fail` 为空不等于绿灯**（相关性四项在 `pending` 里）。

### 32.11 待办（本节落地时仍在飞 / 未决）

- **Batch I `28ayGb6AL4Smc13OxRkOtB9`**（FAST/TOP2500/d1/**decay 20**，10 条）在飞：
  industry × p{1.8, 2.0, 2.2} 补 `WjLVWY3Z` 的 0.03 sub 缺口 · `eps_y2` × industry/p2.0 攻 0.7683 prod ·
  `eps_y1_estimate_change_3mo` 新字段 × 两分组 · **`{eps,netprofit,revenue}_q1_estimate_change_1mo` 新轴** ·
  冠军字段 p2.0 参照格。
- **`xA1dmlVb` prod 0.7683 的缺口 0.068 按 decay 斜率（~0.001/单位）算需 −68 个 decay ⇒ decay 单独修不了**，
  必须靠分组 / p / 中性化。这是 Batch I 的主攻方向。
- **`kqJZLV2k` 的 sub 比 0.429 需 +0.09，而 p2.0 只给 +0.036、decay20 只给 +0.011 ⇒ 合计 0.476 仍 < 0.5196**
  ⇒ **判为现有杠杆集内不可修**，不派槽，只保留其 0.4713–0.6032 的去相关价值作为情报。
- **三颗 all_passed 只能提交一颗**（互相 0.96–0.99）：`KPmE8klx`（prod 0.6653，**余量 0.0347 ≈ 其它两颗的 5 倍**，
  `[0.7,0.8) n=0`）vs `Grge67NZ`（0.6812，余量 0.0188）vs `xA1dQVVm`（IS 最强 S1.79/F1.45/sub0.99/2Y1.75，
  但 prod 0.6933，余量仅 0.0067）。**提交需用户明确确认（红线，任何 waiver 无效）。**
- **未开的尺度缺口赛道**（按期望值排序）：`analyst_consensus`（1929 字段 / cov 0.7027 / αC 1406 / vS 3，
  **判死只是模板级**；需绕 `/data-fields` 的 `limit ≤ 50`、`offset > 50` 返空的分页坑）·
  `analyst11`（445 / 0.8489 / αC 918 / vS 3）· `analyst10`（961 / 0.7695）· `analyst9`（111 / 0.6166 / αC 637）·
  **`analyst14`（121 / 0.5000，从未测）** · `analyst7` 的 `dps` 腿。
- **文档待修**（本轮只登记）：`references/analyst.md` L59「EUR 单字段 S 上限约 0.9」与 L98 的
  `EUR-ANALYST-FACTOR-SIGNALS-WEAK` **双双被证伪**，但它是 `profiles render` 生成物 ⇒
  改正路径是 `tracking/EUR/config/cells.json` + `$WQ_PY -m wqb.profiles render --region EUR --apply`，不是手改生成块。
  `_dataset-inventory.md` §一 / §2.1 / §2.2 三行同样待按其自身 §四.3「每收一批就回写本表」更新。
  已封存的 `EUR-ANALYST-FACTOR-SIGNALS-WEAK` 被证伪但 `seal_dead_end` 是 fail-closed 单向、**无解封路径 ⇒ 需人工裁决**。
  另：陈旧 DB 行 id 15314（`786pLKnb` 记成 GBR/TOP700/STATISTICAL/UNSUBMITTED）。
- **塔位口径（用户明确）**：**已点亮 = 提交 ≥ 3 颗**。当前 ATOM+ACTIVE 库存 4 颗
  （`88vQz5Yl`、`786pLKnb`、`LL5VwgO1`、`N1VnJjXg`），MODEL 有 2 颗 ACTIVE ⇒ **未点亮**；
  本族 +1 = 5，**还需 5 颗互相去相关**。32.2 的子集 4 说明缺口是**可达的**，不是结构封闭的。

---

## 三十三、2026-10-19（凌晨）：换参照系双桶法在 EUR 证伪 + ⚠「clique=3」自我纠错为 4 + analyst14 首攻

> 本节四条主结论，**第三条是对本会话自己上一条结论的推翻**，按 `task-experience-d02c937b.md`
> 「穷尽声明前必须盘点全集分母」与 EUR skill 铁律②「宣称穷尽前全量枚举」登记为方法论事故。

### 33.1 Batch J 收割（`43Vjdu39F57Kc9b195T3dE61`，10/10 complete，0 errors）

设置与 Batch I 同档但 **decay 10**（EUR/TOP2500/d1/FAST/trunc 0.08/maxTrade ON/nanHandling ON），
**刻意与 `KPmE8klx` 逐项对齐 ⇒ J1 是双桶外壳的纯单变量消融**。

| alpha | 腿 | 构造差异 | S | F | TO | returns | DD | margin | sub | sub 限 | 2Y | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`KPmE8klx`** | **对照母体（无桶）** | `signed_power(group_zscore(np_y2, subindustry), 1.8)` | **1.69** | **1.32** | 0.0639 | 0.0761 | 0.0603 | **0.002383** | **0.93** | pass | **1.61** | **0** ✅ |
| `XgR81x6m` | J7 | + 水平桶 `bucket(rank(np_y2_consensus_value))` 5 格 | 1.65 | 1.26 | 0.0641 | 0.0731 | 0.0603 | 0.002281 | **0.92** | pass | **1.50** ✗ | 1（仅 2Y） |
| `3qjezOZ0` | J4 | + 离散桶 `bucket(rank(ts_std_dev(·,21)))` 5 格 | 1.66 | 1.28 | 0.0645 | 0.0744 | 0.0678 | 0.002309 | **0.85** | **0.86** ✗ | 1.65 | 1（仅 sub，差 0.01） |
| `LL5dkwA1` | J3 | + 长期观点桶 `bucket(rank(ts_mean(·,252)))` 5 格 | 1.45 | 0.97 | 0.0637 | 0.0555 | 0.0488 | 0.001743 | 0.77 | pass | 1.53 | 3 |
| `zqrROE1K` | J1 | **完整双桶 25 格**（论坛原方） | **1.43** | **0.95** | 0.0659 | 0.0551 | 0.0615 | **0.001671** | 0.74 | pass | 1.59 | 2（S+F） |
| `1YjzJRQm` | J2 | 双桶 + 外层换 `group_zscore` | 1.50 | 0.87 | 0.0660 | 0.0418 | **0.0436** | 0.001268 | 0.73 | 0.78 ✗ | 1.64 | 3 |
| `WjLV9R6x` | J5 | 双桶 q=0.25（16 格） | 1.45 | 0.97 | 0.0655 | 0.0563 | 0.0600 | 0.001721 | 0.72 | 0.75 ✗ | 1.56 | 4 |
| `MP0Lknor` | J6 | 双桶迁移到 `eps_y2` | 1.30 | 0.82 | 0.0666 | 0.0500 | 0.0537 | 0.001500 | 0.64 | 0.68 ✗ | 1.44 | 4 |
| `GrgekNJJ` | J8 | **离散轴换截面字段** `np_y2_estimate_coeff_var` × `ts_mean(·,252)` | 1.42 | 0.95 | 0.0657 | 0.0562 | **0.0420** | 0.001711 | 0.78 | pass | 1.40 | 3 |
| `omogVXOn` | J10 | 双桶 + industry 分组 | 1.39 | 1.03 | 0.0739 | 0.0692 | 0.0977 | 0.001873 | 0.64 | 0.72 ✗ | **1.88** | 2 |
| `qME6gpqv` | J9 | 双桶窗口改配字段周期（63/126） | **1.11** | **0.63** | 0.0660 | 0.0407 | 0.0731 | 0.001235 | 0.55 | 0.58 ✗ | 1.22 | 4 |

**结论：论坛「换参照系双桶法」在 EUR 符号反转。** 帖 `43624302417559` 在 GLB/MINVOL1M 的 `techindi_model`
上测得 **5.55 → 6.24（+0.69 Sharpe）、prod 0.7935 → 0.6814（−0.11）**；同一骨架搬到 EUR 是
**−0.26 Sharpe / −0.37 Fitness / margin −30%**，且**去相关为零**（见 33.2）。

四条次级归因（都不是盲扫，都有对照格）：

1. **格数是 Sharpe 杀手，代价对格数超可加**：5 格 −0.03~−0.04 Sharpe，25 格 **−0.26**。
   TOP2500 约 2800 名 ⇒ 25 格 ≈ 112 名/格，5 格 ≈ 560 名/格。GLB/MINVOL1M 宇宙小得多，
   **这才是同一 25 格设计在那边成立的原因**，不是载体差异。
2. **窗口不是自由参数**：J9 把窗口"配准"字段周期（`ts_std_dev 63` / `ts_mean 126`）直接崩到 S 1.11 / F 0.63。
   帖里的 **22/252（短窗离散 + 长窗水平）是有效组合本身**，不是可随字段缩放的量。
3. **水平型桶轴是 sub 增益器**：J7 用 `np_y2_consensus_value`（水平字段）分桶拿到**全批最高 sub 0.92**，
   Sharpe 只掉 0.04，代价全落在 2Y。⇒ **若目的是修 sub 闸，桶轴要选水平型，不要选离散型**
   （J4 用离散轴反而把 sub 从 0.93 拖到 0.85，差 0.01 撞闸）。
4. **外层算子选择**：J2（`group_zscore`）vs J1（`group_neutralize`）——J2 的 DD 最低（0.0436）但 returns 只有
   0.0418、sub 撞闸；J1 returns 0.0551。**在 EUR 这一对上 `group_neutralize` 更好**，与 §29「group_neutralize 毒药机制」
   并不矛盾：§29 说的是**粗粒度外层归一**，此处是**细格内去均值**（格内 std 噪声大 ⇒ 去均值更稳）。
   margin 对结构最敏感（帖内评论 WS28067 同结论）：0.002383 → 0.001671 是 −30%，而 Sharpe 只 −0.26。

### 33.2 ★ 机制证伪：bucket **不是** EUR 的去相关轴

`compute_mutual_correlation`（本地、免配额、threshold 0.7、years 4、`num_points 1021`）：

| 配对 | PnL 相关 |
|---|---:|
| `KPmE8klx` × `XgR81x6m`（水平桶） | **0.9972** |
| `KPmE8klx` × `3qjezOZ0`（离散桶） | **0.9920** |
| `KPmE8klx` × `Grge67NZ`（decay 20） | 0.9903 |
| `KPmE8klx` × `zqrROE1K`（完整双桶） | **0.9413** |
| `KPmE8klx` × `LL5dkwA1`（长期观点桶） | 0.9475 |
| `KPmE8klx` × `GrgekNJJ`（截面离散轴桶） | 0.8482 |

**加桶后的 PnL 与自己的无桶母体相关 0.85–0.997 ⇒ 换参照系没有换掉排序空间的实质内容。**
桶只是把同一个信号在格内重新居中，**它改变的是强度与覆盖，不是持仓的"什么时候交易"**。
这正好落在帖 `42966871377943` 的核心论断上：*"🧬 相关性高的 alpha 共享的是「什么时候交易」，不是「持有什么」"*
⇒ **凡只改持仓的杠杆（decay / 分组 / p / 字段 / 桶）都只能在 0.63–0.77 这条带内移动 prod，压不出量级变化。**

⚠ **两条项目内 skill 因此指向错误方向，本轮登记不改**（改 skill 属另一条工作流）：
`wq-window-valley-break-prod-wall`（「先平滑再找谷」）与 `wq-prod-lever-self-lock-guard`
（把 `hump` 归为「不改持仓的平滑杠杆」）。后者的分类是错的：`hump(x, hump=0.01)` 的平台定义是
*"Limits amount and magnitude of changes in input (thus reducing turnover)"* —— **它是换手阈值算子，
压制小幅持仓变化 ⇒ 制造离散交易事件 ⇒ 真的改「什么时候交易」**；而 `decay` 是信号的线性时间平滑，
不改时序，只是收敛到「大家的平均版本」。二者不是同一类算子，prod 方向相反不是矛盾。

帖内独立佐证了 decay 这一半：*"AI 助手建议 decay 从 15 加到 40 来压换手，结果 prod 反升到 0.85"*；
*"平滑不等于去拥挤 … ts_rank(66) 把每个人手里不同的原始值都收敛到同一个「过去三个月的相对位置」，
反而让大家的 alpha 更像了"*。评论 SZ62220 给出最干净的机制表述：
*"长 decay 和 ts_rank 抹平了个股特质信息后，留下的恰恰是全平台模型共享的慢风格暴露，因而越平滑越拥挤。"*
⇒ **与本档 §31.2 实测的 EUR decay 阶梯（d10 0.6653 → d120 0.7607，斜率 ≈ +0.001/单位）完全一致。**

### 33.3 ⚠⚠ 自我纠错：上限不是 3，是 4 —— 抽样分母不足导致的误判

**本会话早先据一次 10×10 互相关得出「`analyst_factor_signals` 的互补图 clique number = 3，
且三个成员全被闸住 ⇒ 该数据集只能出 1 颗」，并据此把「换数据集」判定为「已获数学证明」。**
**该结论错误。** 把候选池补全到 16 颗后重跑（同一工具、同一参数）：

```
max_mutually_below_subset = ["1YjzoEGm", "xA1dmlVb", "kqJZLV2k", "GrgekNJJ"]
max_mutually_below_subset_size = 4        max_subset_exact = true
missing_pnl = []                          local_calculation = true
```

六对逐条复核（全部 < 0.7）：`1YjzoEGm×xA1dmlVb` 0.6773 · `1YjzoEGm×kqJZLV2k` 0.4671 ·
`1YjzoEGm×GrgekNJJ` 0.6659 · `xA1dmlVb×kqJZLV2k` 0.5504 · `xA1dmlVb×GrgekNJJ` 0.6416 ·
`kqJZLV2k×GrgekNJJ` 0.4801。

**漏掉的第四名 `GrgekNJJ` 正是本会话新造的 J8**（截面离散字段 `np_y2_estimate_coeff_var` 作条件轴），
它不在早先那 10 颗的抽样里。**§三十二 标题写的「互相关子集达 4」是对的，本会话的 3 是错的。**

方法论事故登记（可复用）：

> **`max_mutually_below_subset` 是候选池的函数，不是数据集的不变量。**
> 用它下「这个数据集最多出 N 颗」的结论前，**必须把该数据集全部已回测候选一次性喂进去**——
> 少喂一颗就可能把 N 报小。工具返回 `max_subset_exact: true` 只表示
> 「在**你给的这个池子里**已求精确解」，**不表示池子是全的**。
> 与 `learned-skill-experience`／`task-experience-d02c937b` 同族：**分母不清就不许下上限结论。**

### 33.4 尺度数学（修正版）与修复优先级

- **`analyst_factor_signals` 的互斥去相关上限 = 4**（当前池已求精确解；仍可能随新候选上升，
  见 33.3 教训，**不再宣称封闭**）。
- 这 4 颗与 `KPmE8klx` **互斥而非可加**：`KPmE8klx` 与 `1YjzoEGm` 0.8041、与 `xA1dmlVb` 0.7990、
  与 `GrgekNJJ` 0.8482 ⇒ **要么出 `KPmE8klx` 1 颗，要么修 4-set，二者不可兼得。**
- 4-set 的逐颗闸况与修复路径（按可修性排序）：

| alpha | 经济内容 | 唯一/主要障碍 | 缺口 | 已识别杠杆 | 可修性 |
|---|---|---|---|---|---|
| **`GrgekNJJ`** | 估计离散度 × 长期观点条件化 | **纯强度闸**（S/F/2Y），**prod 与 sub 都过** | S 1.42→1.58（+0.16）、2Y 1.40→1.58（+0.18） | p 指数（Batch I 实测 p1.8→2.0 抬 S）；decay 下调（Batch I 实测 d40→d20 抬 2Y 2.06→2.09）。**F 会自解**：returns 0.0562 下 S=1.58 ⇒ F=1.58×√(0.0562/0.125)=**1.06** ✅ | **最高** |
| `kqJZLV2k` | np_y1（1 年期修正） | sub 比 0.429 vs 需 0.5196 | +0.09 | **本档 §33.10 新增的覆盖杠杆**：`group_backfill(x, subindustry, 126)` / `group_backfill(x, group_cartesian_product(country,subindustry), 126)`。⚠ §32 曾判其「现有杠杆集内不可修」，**但当时手上没有 backfill 覆盖杠杆 ⇒ 该判定需重开** | 中 |
| `1YjzoEGm` | np_y2 × industry × p1.8 | **prod 0.7398** | −0.04 | decay 已在 20，斜率 ~0.001/单位且**方向是反的**；分组改细 ⇒ 与 `KPmE8klx` 0.99 同格失去意义 | 低 |
| `xA1dmlVb` | eps_y2 | **prod 0.7683** | −0.068 | 同上，缺口更大 | 最低 |

- **`KPmE8klx` 仍是唯一「现在就能提交」的一颗**：failed_ra 0、prod 0.6653、self 0.2771、
  `[0.7,0.8)` 桶 n=0。⚠ 但 **CLUSTER_TEST 1.57 vs 限 1.58 —— 差一格就变 FAIL**，任何后续微调都要复测这项。
- **⇒ 目标 10 颗的缺口至少 6 颗必须来自别的数据集**，`analyst14` 是第一条新赛道（33.6）。

### 33.5 塔位合规核验（平台权威，纠正本档 §32 的库存口径）

`get_pyramid_alphas()`（当季）实测：

> ⚠ **本表 2026-10-19 二次核对修正**：首版有 3 处算术错（GBR 9→10、IND 17→23、KOR 13→12）
> 且**整行漏掉 DEU/D1**。教训：合计列必须由原始 JSON 逐项重加，不能凭印象。

| 区域/延迟 | analyst | model | fund | other | risk | 其余类别 | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **EUR / D1** | **1** | 2 | 1 | 1 | 1 | 0 | **6** |
| EUR / D0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| USA / D1 | 5 | 4 | 0 | 0 | 0 | earnings 1 | **10** |
| GBR / D1 | 3 | 5 | 0 | 1 | 0 | pv 1 | **10** |
| IND / D1 | 3 | 3 | 0 | 4 | 1 | pv 6 · news 4 · macro 2 | **23** |
| KOR / D1 | 1 | 2 | 3 | 1 | 0 | pv 2 · shortinterest 3 | **12** |
| DEU / D1 | 1 | 1 | 1 | 2 | 0 | institutions 1 | **6** |
| ASI / D1 | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| GLB / HKG / AMR / CHN | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- **`EUR/D1/analyst = 1`** ⇒ 按用户口径（点亮 = 提交 ≥ 3）**未点亮，且只剩 2 个位置**。
  锁定项「已点亮塔不作主数据集」**当前不构成障碍**，但**继续往 ANALYST 塔堆到第 3 颗就会点亮**，
  之后同塔候选失去塔乘数（现 `EUR/D1/ANALYST` ×1.3）。**这是提交排序问题，归用户裁决，本节只登记。**
- ⚠ **本档 §32 尾条「当前 ATOM+ACTIVE 库存 4 颗（`88vQz5Yl`/`786pLKnb`/`LL5VwgO1`/`N1VnJjXg`）」
  被平台数据证伪**：EUR/D1/analyst 当季只有 1 颗。那 4 颗要么跨区域、要么跨类别、要么不在当季。
  **塔位计数一律以 `get_pyramid_alphas` 为准，不以本地 DB 库存为准**（与 `is-alpha-pyramids.md` 同源）。

### 33.6 `analyst14` 数据集画像（121 字段，全部 MATRIX，coverage 均标 0.5）

`get_datafields(region=EUR, dataset_id=analyst14, universe=TOP2500, delay=1, filter_sharpe=False)` 实测。
**结构性差异：它给的是「横截面预测分布」而不是「预测的时间序列修正」** —— 这正是与
`analyst_factor_signals`（`*_estimate_change_3mo` = 修正量）在机制上正交的地方。

| 族 | 字段数 | 形态 | αC 区间 | 经济含义 |
|---|---:|---|---|---|
| **A 实际值 `anl14_actvalue_*_fp0`** | 9 | ebit / ebitda / eps / epsrep / ntp / ntprep / ptp / ptprep / revenue，最近一季度**已披露实际** | 40–198 | 分母基准（算预期增长用） |
| **B 预测分布 `anl14_{high,low,mean,median,stddev,numofests}_*_{fp1,fp2}`** | ~80 | 同样 9 个科目 × 6 个统计量 × 2 个期限（fp1 = 下季度，fp2 = 下下季度） | 4–62（多数 <25，**近处女地**） | 一致预期水平 + **分歧度** + **分布形状** + 覆盖度 |
| **C 推荐 `anl14_{buy,hold,sell,outperform,underperform,meanrating}`** | 6 | 计数 + 平台聚合评分 | 65–593（`buy` 593，最拥挤） | 分析师情绪/羊群 |
| **D 目标价 `rtk_ptg_{high,low,mean,median,number,stddev}`** | 6 | **前缀是 `rtk_` 不是 `anl14_`** | 61–452 | 估值锚的水平与不确定性 |
| **E 元数据 `anl14_{curperiodnum,curperiodtype,cursharesoutstanding,xrefmap}`** | 4 | 期间号 / 期间类型 / 流通股本 / 映射 | 27–69 | 非信号，可作条件轴或忽略 |

**ATOM 边界裁定（回答用户「把混数据集和 ATOM 的边界定义清楚」）**：
`rtk_ptg_*` 虽**前缀不同**，但由 `dataset_id=analyst14` 的查询返回 ⇒ **与 `anl14_*` 同属一个数据集 id**
⇒ 同一表达式里混用 `rtk_ptg_stddev` 与 `anl14_mean_eps_fp1` **不违反 ATOM**。
**判据是数据集 id，不是字段名前缀**（前缀只反映供应商/来源系统）。
对照：`anl14_*` × `pv87_*` 就是两个 dataset id ⇒ 违反 ATOM，而 `pv87` × `pv30` 同样是两个 id
（同属 Price Volume **category** 不构成豁免——category 是数据集的上位分组，不是数据集）。

⚠ **coverage 0.5 的读法**：API 返回的是**数据集级**统一戳，不是逐字段实测。0.5 × TOP2500 ≈ 1250 名，
与 Batch I/J 实测 `longCount ≈ 1410` 量级相符。**低覆盖 ⇒ sub-universe 闸是首要风险**，
应对工具已备好（33.10 的 backfill 阶梯，`group_backfill` 已核为 REGULAR）。

### 33.7 Batch K（`4yoX6GgIi4rab6uYMfspQkX`）：六机制首攻，每条都先说清收益从哪来

设置与 Batch J **逐项相同**（EUR/TOP2500/d1/**decay 10**/FAST/trunc 0.08/maxTrade ON/nanHandling ON）
⇒ 任何赢家可直接与 `KPmE8klx` 对照，且满足铁律⑤。外壳统一沿用已验证的
`signed_power(group_zscore(rank(<无量纲构造>), subindustry), 1.8)`，**只换经济内容**。

| 腿 | 机制（收益从哪来） | 核心构造 |
|---|---|---|
| K1 | **预期 EPS 增长**：分析师对下季的一致预期相对最近已披露实际的升幅。属**预期水平**信号，与 `estimate_change_3mo` 的**修正量**信号是两种经济内容 ⇒ 最佳去相关候选。机制 = 盈余公告后漂移 / 基本面动量 | `subtract(anl14_mean_eps_fp1, anl14_actvalue_eps_fp0) / abs(anl14_actvalue_eps_fp0)` |
| K2 | 同 K1，科目换**净利润** | `anl14_mean_ntp_fp1` vs `anl14_actvalue_ntp_fp0` |
| K3 | 同 K1，科目换**营收**（营收预期最难被操纵 ⇒ 噪声最低） | `anl14_mean_revenue_fp1` vs `anl14_actvalue_revenue_fp0` |
| K4 | **盈利预测分歧度**（原符号）：Diether–Malloy–Scherbina (2002, *JF*) 高分歧 → 低未来收益 ⇒ 理论符号为负 | `anl14_stddev_eps_fp1 / abs(anl14_mean_eps_fp1)`（变异系数，无量纲） |
| K5 | **同 K4 取反**（`multiply(·, -1)`）：一次批内**双向定符号**，|S| 若 ≥1.58 必有一条过闸（铁律③「双结构保底」用在符号维度上） | `multiply(K4 构造, -1)` |
| K6 | **预测区间偏度**：最高估计高于均值的幅度 ÷ 均值高于最低估计的幅度 ⇒ 乐观尾部 → 预测正向惊喜 | `subtract(high_eps_fp1, mean_eps_fp1) / abs(subtract(mean_eps_fp1, low_eps_fp1))` |
| K7 | **预测期限结构斜率**：fp2/fp1 ⇒ 预期盈利加速度 | `anl14_mean_eps_fp2 / abs(anl14_mean_eps_fp1)` |
| K8 | **净推荐广度**：(buy+outperform−sell−underperform) ÷ 总推荐数 ⇒ 分析师情绪一致度与羊群漂移 | 计数比值，全无量纲 |
| K9 | **目标价分歧度**（`rtk` 族）：**估值锚**的不确定性，与 K4 的**盈利**不确定性是两种不确定性 | `rtk_ptg_stddev / abs(rtk_ptg_mean)` |
| K10 | **平台聚合评分** `anl14_meanrating`（αC 148）：方向未知（1=强买 还是 5=强买）⇒ 先测原符号，强负 Sharpe 本身就是答案 | `rank(anl14_meanrating)` |

**合规自检**（逐条）：单数据集 `analyst14`（含 `rtk_` 同 id 字段）✅ · 无 `add(信号A, 信号B)` 混信号
（K8 的 `add` 是**同一构造内的计数算术**，不是两个独立经济信号的加权融合）✅ ·
分组只用豁免字段 `subindustry` ✅ · 全部核心量是 **rank 或无量纲比值**，不给有单位字段加常数 ✅ ·
不以 `close` 作分母（那会跨到 PV 数据集）✅ · 窗口未在白名单外 ✅ · truncation 未作扫描维度 ✅ ·
18 个字段名全部来自本轮 `get_datafields` 实时返回 ✅（铁律①）。

**刻意不派的腿及其理由**（归因驱动，非扫不动）：
- `group_backfill` 修 `3qjezOZ0` 的 0.01 sub 缺口 —— **它与 `KPmE8klx` 相关 0.992，修好也不能与其并存**，纯浪费槽位。
- 帖内建议的**外生条件轴**（借券约束 / 指令流失衡 / 流动性）—— 全部会跨数据集 ⇒ **破坏 ATOM**，故 J8 用同数据集的
  `estimate_coeff_var` 替代，K 批同理只用 `anl14_*`/`rtk_*`。
- `hump` / `trade_when` / 不对称双塔三条 **prod 杠杆**（33.10）—— 它们针对的是「强但拥挤」的候选；
  **当前瓶颈已从 prod 变成「需要 6 颗新去相关alpha」**，故 K 批 100% 用于机制探索。
  这三条杠杆**顺延到 K 批出现强而拥挤的候选时再上**（届时优先级：`hump` > `trade_when` > 尾部重构）。

### 33.8 算子签名核验（`research-data/operators_platform_20260904.json`，102 个算子；铁律①的权威源）

本轮**新增核实**以下签名与 scope（此前 `want` 集合里没有，用过就是赌）：

| 算子 | scope | 平台签名 | 用途/坑 |
|---|---|---|---|
| **`subtract`** | COMBO,REGULAR,**SELECTION** | `subtract(x, y, filter=false)` | **存在且 REGULAR** ⇒ 无需 `add(x, multiply(-1,y))`，**顺带规避 VERIFY 模式下「无量纲常数 + 有单位字段」的 UNITS 警告** |
| **`group_backfill`** | COMBO,REGULAR | `group_backfill(x, group, d, std = 4.0)` | 组内 NaN 用**过去 d 天 winsorized 均值**回填 ⇒ **名数覆盖**修法（33.10） |
| `ts_backfill` | COMBO,REGULAR | `ts_backfill(x, lookback = d, k = 1)` | ⚠ **`lookback` 是命名参**（与项目记忆「lookback-vs-group 参数铁律」同源） |
| `hump` | COMBO,REGULAR | `hump(x, hump = 0.01)` | ⚠ **`hump` 是命名参**（keyword-only，与 `wq-prod-lever-self-lock-guard` 记的一致） |
| `trade_when` | COMBO,REGULAR | `trade_when(x, y, z)` | 3 参；**只在条件满足时改值，否则保持前值** ⇒ 真改「什么时候交易」 |
| `bucket` | COMBO,REGULAR | `bucket(rank(x), range="0,1,0.1", skipBoth=False, NaNGroup=False)` 或 `bucket(rank(x), buckets="2,5,6,7,10", …)` | 证实项目记忆 `bucket-multisim-error.md`：**第二参必须命名**，位置参 ERROR 并连坐整批 |
| `reverse` | COMBO,REGULAR,SELECTION | `reverse(x)` | 翻转排序（≈ 1−rank），**不是**取负号；对已 z-score 的信号应用 `multiply(·,-1)` |
| `if_else` / `winsorize` / `densify` / `normalize` / `quantile` | COMBO,REGULAR | `if_else(a,b,c)` / `winsorize(x, std=4)` / `densify(x)` / `normalize(x, useStd=false, limit=0.0)` / `quantile(x, driver=gaussian, sigma=1.0)` | 备用；`quantile` 单参硬约束见项目记忆 |
| **确认不存在** | — | — | `sub`（要用 `subtract`）· `negate` · `cum_sum` · `count` · `decay_linear` · `decay_exp_window` · `s_log` · `scale_down` · **`vector_neut`** · **`regression_neut`** · **`left_tail` / `right_tail`** · `filter` · `keep` |

⚠ **`left_tail` / `right_tail` 在平台算子文件里根本不存在** ⇒ 论坛五杠杆第 4 条（GLB EPS 修正 prod **0.42**，
本档最高先验）里的「不对称双塔 `right_tail` 多头 + `left_tail` 空头」**是发帖人的构造简写，不是算子**。
要用这条杠杆必须先用现有原语重构（候选路径：`if_else(rank(x) >= q, x, 0)` 型门控 + `trade_when`），
**且重构前不得当作已验证武器写进任何清单**。
⚠ 同理，帖 `43624302417559` 的开放问题③（`group_neutralize` vs `vector_neut`）**在本平台无法回答**——`vector_neut` 不存在。

### 33.9 工具缺陷登记（本轮新增两条）

1. **`validate_expressions` 对 `bucket` 族结构性失明**：它把 `bucket(…, range="0,1,0.2")` 的**命名参 `range`
   当成候选字段名**去查，于是对**任何含 bucket 的表达式**都返回 `unknown_fields: ["range"]` + `valid: false`。
   **正确读法 = 看 `platform_field_count` 与 `fields_checked`，扣掉已知命名参关键字**，不要看 `valid`。
   ⚠ **按「valid 必须为 true」使用本工具的人会被永久挡在 `bucket` 之外。**
   （Batch K 无 bucket ⇒ 本轮返回 `valid: true`、`unknown_fields: []`、18 字段全核 ⇒ 两种行为都已实测。）
2. **`validate_expressions` 的字段预检会因分页失败而静默降级**：本轮返回
   `warning: "Field pre-check skipped or incomplete: anl14_actvalue_eps_fp0: get_datafields(offset=50): failed after 6 attempts; anl14_mean_ntp_fp1: get_datafields(offset=0): failed after 6 attempts"`
   + `note: "Field lookup incomplete; not treating candidates as unknown."`。
   **降级方向是安全的**（不把候选判成 unknown），但**它意味着 `valid: true` 不等于字段已核**。
   ⇒ **铁律① 不能靠本工具满足，必须自己跑一次 `get_datafields` 拿实时字段名。**
   根因与项目记忆 `brain-data-fields-offset-limit-100-400.md`（`offset+limit>100` 返 400）同源。

### 33.10 论坛取证（本轮三帖，含一条**反面教材**）

**① `43624302417559`（v66 c21）「换参照系双桶法」—— 本轮最富矿的来源，但在 EUR 证伪（33.1/33.2）。**
原方：GLB/MINVOL1M/D1，数据集 `techindi_model`，单字段 `predicted_first_quantile_ten_day_return_21`，
提交 `3qXrq6OO`：Sharpe 6.24 / Fitness 5.26 / TO 16.0% / Margin 14.2bp / 2Y 5.46 / Sub 3.74 / DD 1.02% /
failed_ra 0 / **prod 0.6814** / self 0.295；设置 FAST / decay 22 / trunc 0.08 / nanHandling **OFF** / maxTrade **OFF**。

```
x = predicted_first_quantile_ten_day_return_21;
group_neutralize(
  group_zscore(x, sector),
  group_cartesian_product(
    bucket(rank(ts_std_dev(x, 22)),  range="0,1,0.2"),   # 置信度轴（1 个月）
    bucket(rank(ts_mean(x, 252)),    range="0,1,0.2")))  # 长期观点轴（1 年）
```

其 15 条同设置消融里**最有信息量的三条**：
- **安慰剂桶** `6Xjq5YX5`（对 cap 分桶）Sharpe **6.26 几乎不掉，但 prod 0.8876、与提交版相关 0.888**
  ⇒ **桶的价值必须用相关性验收，不能用 Sharpe 验收**（帖内原话，本档 J 批实测同结论：Sharpe 掉 0.26 而相关性纹丝不动）。
- **外层换 `group_zscore`** `RRbaGkjg`：Sharpe 5.92、**margin 14.2→10.6bp**、fitness 5.26→4.31
  ⇒ 外层要 `group_neutralize`（去均值、保幅度），不要 `group_zscore`（再除一次格内 std）。
- **符号翻转** `akbP5WjO` −6.24，完全对称 ⇒ 该载体方向确定，无需双向测。
- 台账证据：裸版多/空 4868/4045（多头超额 800）→ 双桶 4546/4368（超额 178）；
  **2020 危机年 S 2.15→5.46、DD 3.03%→0.71%** ⇒ *"「所有人都在交易的分量」恰好就是危机时同步平仓的分量"*。
- 归因分工：**std 桶 = Sharpe/DD 旋钮**（+0.8 Sharpe，DD 3.03%→1.00%）；
  **mean 桶 = 去相关旋钮，不是收益旋钮**（单 std 桶 prod 0.75 → 加 mean 桶 0.669）。
  ⚠ **本档 J 批实测这两条在 EUR 都反了**：std 桶抬 2Y 但砸 sub，mean 桶（J3）单独把 S 打到 1.45，
  且**两者都不去相关**。
- 学术支撑：Stein (2009, *JF* 64(4) 1517–1548) 拥挤交易；Da/Liu/Schaumburg (2014, *Management Science* 60(3) 658–674)
  反转分解为共同因子 vs 特质；Daniel/Mota/Rottke/Santos (2020, *RFS* 33(5) 1927–1979)
  **对冲因子暴露常常反而抬 Sharpe**。
- **适用边界（帖内最有价值的部分）**：*"只对「偏离型」载体有效，对「水平型且分桶轴共线」的载体是毁灭性的。
  分析师 ML 回归预测套同一骨架：1.74 → −0.12。"* 三条规则：分桶轴不能含信号自身的构成项
  （`risk88` 反例：信号是 `ts_zscore(x,1008)`，却对长期水平分桶 ⇒ 2.28 → 1.42；改成「当前水平桶 × 子行业」后
  self-corr 0.54→0.42）；分桶轴必须来自信号自己的派生量；**桶的价值用相关性验收**。
  已验证迁移：`shortinterest7` prod **0.87→0.69**（`E5p70Yx9`，S 2.12→3.31）；`dl_riskfree_returns` S 3.6–3.8、互相关 0.58；
  TOP3000 同门 2.79/2Y 2.87；`model110` 在 AMER 挂 2Y；`global_seasonal_model` margin 9bp 挂。
  ⚠ **本档补充第四条边界条件（帖里没有）**：**载体的起点 prod 决定收益**——起点 0.7935 才有 0.11 可剥；
  起点已是 0.6653（因为内层已经 `group_zscore(·, subindustry)` 细粒度中性化过）时，**同一操作只烧 Sharpe**。

高价值评论：
- **JR57542（水平/变化两形相关谱，可直接照做）**：*"先判你的参照占的是水平轴还是变化轴。我以为做变化量总能和
  水平信号去相关，实际撞墙后发现——**当池占的正是变化量轴时，level 才是正交资产，相关随差分阶次单调升，
  越「求变」反而越像它。** 撞墙后先别改构造：对参照跑一个**水平/变化两形的小相关谱**，两三条腿就够，
  找到单调方向再定形。去相关腿的谱单调降且强度不掉就成了；两头都平的，说明正交轴不在这一维，换轴别硬凑。"*
  ⇒ **本档 J7 就是这条诊断的执行**（用水平字段 `consensus_value` 分桶），结果证明**两头都不平但也不降**（0.9972）。
- **XZ17517（直接警告本项目的选篮流程）**：*"我曾经对同一水平型字段分别做「行业内中性化」和「对 25 格哑变量投影」，
  两版 PnL 相关 0.86 以上，但 prod 一个 0.58、一个 0.71——表现相似的两个版本，拥挤程度差了一个量级。
  所以…用「最大 prod 相关」而不是「Sharpe 或互相关」来判定，可能是唯一不会骗你的标准。"*
  另：self↔prod 单调但在 ~0.3–0.4 有**弯折**——*"self 0.2 以下的版本 prod 普遍 < 0.55，
  self 0.35–0.55 的版本 prod 已经会撞到 0.75–0.85"* ⇒ **self 只能当必要不充分条件，不能当 prod 的代理**。
  ⚠ **本档实测该代理在 analyst 族完全失效**：`KPmE8klx` self 0.2771/prod 0.6653 · `Grge67NZ` 0.2708/0.6812 ·
  `xA1dQVVm` 0.2732/0.6933 · `QPY9qvGX` 0.2656/0.7327 ⇒ **self 在 0.068 的 prod 跨度上平在 ~0.27，零区分力。**
- **MK63856**：*"换参照系本质是改变排序空间…但换完之后 **Sub-universe 和 Robust universe 可能同步变化**…
  所以每次换参照系都该重跑一遍六维体检，别只看 PC 降了 0.11 就收工。"* ⇒ J 批实测印证：J4 换桶后 sub 0.93→0.85 撞闸。
- **MY21251**：分桶参照系必须锁死并与提交检查池一致——*"分桶本身也要当作一个要锁死的 settings"*。
- **SZ62220**：prod = 所有生产策略在少数高维隐空间主成分上的投影累加；**硬 25 桶离散中性化比平滑连续 `vector_neut`
  更强力地破坏全局排序结构**；建议分桶轴可以离开单字段派生量，改用**外生微观结构变量**（借券约束 / 指令流失衡度）。
  ⚠ 该建议在 EUR **与 ATOM 冲突**（外生变量必跨数据集），故 J8/K 批用同数据集字段替代。
- **WS28067**：用前先查候选分桶轴与信号的**横截面相关**；**margin 是最敏感指标**（14.2 vs 10.6bp），Sharpe 太宽容。
- **OY62064**：operatorCount 9 可能拖累六维体检指标。
- **FX25214**：应报告**逐格名数分布**而非只报 8900/25 的均值；建议加一条 delay-1 轴做时间因果性检验。
- **JP60063**：*"对 IS 全绿但 prod 卡在 0.72-0.75 的拥挤字段 alpha，换参照系是一个值得尝试的方向"*
  ⇒ **本档实测：在 EUR 这条建议不成立**（33.2），因为 IS 全绿的候选 prod 只有 0.6653，不在 0.72–0.75 区间。
- **XG41865**：同骨架已产出两颗、点亮两个 GLB/D1 塔；**self-corr 当代理在偏离型上有效，在水平型上大概不行**。

**② `42966871377943` —— 降 prod 五杠杆排序（发帖人 EUR/GBR/GLB 数百次仿真实测），对照本档状态：**

| # | 杠杆 | 帖内实测 | 本档 EUR 状态 |
|---|---|---|---|
| 1 | 切换中性化 | EUR 借贷 MARKET→STATISTICAL **0.855→0.726** | **部分做过**：Sharpe 阶梯已扫（FAST 1.87 ≫ CROWDING 1.49 > STATISTICAL 1.47 > REVERSION_AND_MOMENTUM 1.21 ≫ SLOW_AND_FAST 0.82）；§31.3 CROWDING prod **0.6257** 但 S 1.49 < 1.58 = **尚未化解的张力** |
| 2 | 差异化结构（非参数） | GBR 纯 SI 0.64 vs 新闻+SI 混合 **0.46** | **做过**：字段 × 分组轴覆盖 0.42–0.69 |
| 3 | **`trade_when` 分层事件架构** | GLB **0.51** | **EUR 从未测**；`trade_when` 已核 REGULAR ⇒ **可测**。⚠ 项目记忆 `trade-when-decile.md`：对 decile 评分用 `trade_when` 曾产生**零交易** |
| 4 | **不对称双塔 `right_tail` 多头 + `left_tail` 空头 + 异构窗口** | GLB **EPS 修正** alpha **0.42** | **从未测，先验最高（正是本项目的字段族）**；但 `right_tail`/`left_tail` **不是算子**（33.8）⇒ 必须先重构 |
| 5 | **`group_rank` 输出外套 `hump` 平滑** | `hump=0.0012`，GBR **0.32** | `group_rank` 在 EUR 实测**灾难**（S 0.92 vs `group_zscore` 1.49）；**`hump` 单独从未测**，已核 REGULAR ⇒ 可测 |

**⇒ 三条从未在 EUR 测过的杠杆（3/4/5）全部改「什么时候交易」或「尾部暴露」，没有一条是改持仓的。**
这与 33.2 的机制结论自洽，也解释了为什么本档扫遍 decay/分组/p/字段/桶 只能把 prod 关在 0.63–0.77 的带内。
**这三条顺延为「K 批出现强而拥挤候选时」的首选武器，顺序 5 → 3 → 4（按可测性，`hump` 是单算子、4 需重构）。**

**饱和判据（帖内规则，本档实测结论 = 未饱和）**：*"参数扫一遍，corr 纹丝不动 = 信号类别已饱和，立刻换类别"*。
本档实测 prod 随 decay **单调**移动（0.6653→0.7607）、随分组移动 **+0.059**、随字段移动
⇒ **corr 对结构有响应 ⇒ 未饱和 ⇒ 应继续换结构，不应放弃类别。**
对照评论 LL46807 的真饱和案例（KOR）：*"窗口 250→500、双腿异窗、时间尺度全换，PC 都钉在 0.71——
参数轴是同源信号的等价变形，压不动是结构性的。"*
LL46807 另一条与本档 33.4 的选冠军问题直接相关：*"家族第一只选最「代表」的形态反而给变体留路——**选最特异的**"*
⇒ **反对只按 prod 余量选冠军**（`KPmE8klx` 余量最大但形态最"代表"）。

**③ `38669179039255`（v58 c34，EUR TOPCS1600）—— sub / robust / CW 的覆盖率修法，本档直接可用。**
根因 = **新开宇宙的数据覆盖不足**，关键是**分清到底哪个维度覆盖不足**：

- **日期覆盖不足 → `ts_backfill`**。例 `imb5_score`：Coverage 55% 但 Date coverage 100%，
  警告 "Weight is too strongly concentrated or too few instruments are assigned weight"；
  Visualization → Coverage Of Universe 显示正常日 >1300 名但**特定日为 0** ⇒ 裸 `ts_backfill` 即可修。
- **名数覆盖不足 → `group_backfill`**（`ts_backfill` 无效）。另一 fundamental 组合：时序覆盖正常但每日仅 800–1200 名。阶梯：
  | 写法 | 覆盖提升 | 是否解决 Robust |
  |---|---|---|
  | `group_backfill(alpha, country, 126)` | **最大**，但较糙 | **未解决** |
  | `group_backfill(alpha, subindustry, 126)` | 中 | **解决**（对基本面数据，行业均值回填比国家更有经济意义） |
  | `group_backfill(alpha, group_cartesian_product(country, subindustry), 126)` | — | **最佳** |
- 作者自己的告诫：*"并不是万能钥匙"*；适合 fundamental 型覆盖（imb5、oth395）；
  **情绪类字段要慎用——先问回填有没有经济意义**；`ts_backfill` 窗口乃至是否回填都**因数据集而异**；
  **回填确实会增加至少一个操作符数量**（与 OY62064 的 operatorCount 顾虑同源）。
- 评论补充：**AJ39409** 权重均匀化修法 `liq_filter = rank(ts_mean(volume, 20)) >= 0.20; if_else(liq_filter, signal, nan)`
  （⚠ 用了 `volume` ⇒ 跨到 PV 数据集，**在 ATOM 约束下不可用**）；
  **XW23690**（XW25488 附议）*"很多时候出现 robust 是因为 pnl 线和 Investability constrained 的线偏离，
  所以可以选择直接 max trade = on"* ⇒ **本档已默认 maxTrade ON**；
  **FF65210** TOPCS1600 偏中盘，Robust 是同质地 CS 宇宙的高频失败项，建议 `signed_power` 压极值后复查覆盖，
  并警告 **CS1600 容量 < TOP2500 ⇒ 高换手因子有风险**，中性化用 INDUSTRY 或 SUBINDUSTRY；
  **YH55729** 曾用 truncation 修权重集中（⚠ **truncation 是锁定项，不作扫描维度**）；
  **WW15616** *"前两天跑了一堆 Robust 有问题的，只能切回 TOP2500 提交"* ⇒ **与本档选 TOP2500 一致**。

**④ `42189132765463`（v30 c0）—— 反面教材，本身是可复用结论。**
高票零评论、**通篇无表达式、无任何数字**，讲的是多因子权重融合（即 `add A,B` 混信号，**锁定项明令禁止**）。
⇒ **判据：高票 + 零评论 + 无表达式 + 无数字 = 营销帖，不是证据。** 取证时按此三秒筛掉，不花读取额度。

### 33.11 本轮登记 / 待办

- **已写 registry**（`upsert_registry_empirical`，region EUR，layer `dead_end`）：
  `EUR-BUCKET-AXIS-NOT-A-DECORRELATOR`（含消融表、互相关证明、机制和解、**「起点 prod ≥ 0.78 才用该配方」的可执行规则**）。
  ⚠ 该条 payload 未带 `dataset` 键 ⇒ `unbound_entries` 从 44 涨到 **45**，下次写入须补 `dataset` 以免继续增长。
- **profile_drift 回读证实了一处治理缺陷**：`family_dead_datasets` 同时包含 `analyst_factor_signals`，
  而 `win_datasets` 也包含它 ⇒ **同一数据集既判死又记胜，自相矛盾**，需人工裁决（本轮只登记）。
  另 `analyst9/10/11/39/45` 均在 `family_dead_datasets` 里被预拦，而 **`analyst14` 不在任何死名单** ⇒ 本轮选它合规。
- **文档待修**（承 §32，仍未修）：`references/analyst.md` L59 / L98、`_dataset-inventory.md` §一 / §2.1 / §2.2、
  已封存的 `EUR-ANALYST-FACTOR-SIGNALS-WEAK`（`seal_dead_end` fail-closed 单向、**无解封路径 ⇒ 需人工裁决**）、
  陈旧 DB 行 id 15314。
- **治理发现（承 §32，仍未上报）**：EUR 的 `probe-only → active` 升级条件
  （*"出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源"*）**字面已满足**——Batch I returns 0.0732–0.1012，
  `1YjzoEGm` 直方图 `[0.7,0.8) n=3` 对 `[0,0.1] n=841148`（边界处非密墙）。
  **改入场状态是 `tracking/EUR/config/` 的控制文件编辑，属人工决策。**

---

## 三十四、Batch K 全灭与 `analyst14` 判死；Batch L 转攻时序轴（2026-10-19）

### 34.1 Batch K 收割：10/10 完成、0 错误、**零可用**

multisim `4yoX6GgIi4rab6uYMfspQkX`，设置与 Batch J 逐字相同（EUR/TOP2500/D1/**decay 10**/FAST/trunc 0.08/
maxTrade ON/nanHandling ON/pasteurization ON/VERIFY）。

| alpha | 腿 / 机制 | S | F | TO | returns | sub | sub 限 | 2Y | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `2rjN7ZYP` | K8 推荐净广度 | **1.18** | 0.57 | 0.0371 | 0.0287 | 0.58 | 0.61 ✗ | **0.11** | 4 |
| `E5VewadK` | K9 目标价分歧度 `rtk_ptg` | **−1.04** | −0.49 | 0.0396 | −0.0283 | −0.56 | −0.54 ✗ | −1.12 | 4 |
| `omogKzdE` | K10 平台综合评级 | **−0.90** | −0.37 | 0.0342 | −0.0216 | −0.28 | 伪过 | **+0.88** | 3 |
| `QPY9alxK` | K6 预测区间偏度 | −0.42 | −0.13 | 0.0767 | −0.0128 | −0.22 | 伪过 | −0.05 | 3 |
| `78onwX5Q` | K5 分歧度（取负） | 0.41 | 0.12 | 0.0539 | 0.0113 | −0.29 | 0.21 ✗ | −0.30 | 4 |
| `d5KRx7Jx` | K2 ntp 预期增长 | 0.40 | 0.13 | 0.0608 | 0.0125 | 0.26 | 伪过 | 0.76 | 3 |
| `N1eRpjdX` | K4 分歧度（原向） | −0.41 | −0.12 | 0.0539 | −0.0113 | 0.29 | 伪过 | 0.30 | 3 |
| `88vez6WV` | K3 revenue 预期增长 | 0.31 | 0.08 | 0.0581 | 0.0090 | 0.47 | 伪过 | 0.78 | 3 |
| `0mjM7QV2` | K7 期限结构 fp2/fp1 | 0.22 | 0.05 | 0.0640 | 0.0074 | 0.07 | 0.11 ✗ | 0.31 | 4 |
| `zqrR9o7K` | K1 eps 预期增长 | 0.15 | 0.03 | 0.0602 | 0.0049 | 0.08 | 伪过 | 0.16 | 3 |

- **换数据集的全部理由（K1–K3 预期增长机制）当场死透**：S 0.15 / 0.40 / 0.31。
  「预测水平」与「预测修正」在 EUR/D1 并非都有效——**只有修正量（`*_estimate_change_3mo`）有信号**。
- **K4/K5 符号问题实测有了答案**：−0.41 vs +0.41（returns 精确 ±0.0113、pnl 精确 ±1165507，互为镜像）
  ⇒ **Diether–Malloy–Scherbina (2002, JF) 的负号方向成立**（高分歧度 → 低未来收益），但量级死。
- **K8 的 2Y = 0.11 而全期 S = 1.18** ⇒ 推荐类信号近两年基本失效，不是强度问题，是**机制过期**。

### 34.2 ★★★★★ 判死的真因是 F 闸数学封顶，且**本该在 S0 就筛掉**

反算：`F = S × sqrt(returns / 0.125)`。过 F ≥ 1.0 在 S = 1.58 处需 **returns ≥ 0.05**。
Batch K 全部 10 腿 returns ≤ 0.0287 ⇒ **即便把 S 推到 1.58，F 上限也只有 0.76**（K8）/ 0.75（K9）。

- **这是数据集级属性，不是腿级**：10 腿 TO 全落在 **0.034–0.077**，因为分析师一致预期数据更新慢。
  `returns ≈ TO × margin`，TO 被数据更新频率钉死 ⇒ returns 被钉死 ⇒ F 被钉死。
- ⚠ **本可在开波前定论**：EUR 探针 SOP 的失败模式预筛第 ③ 条就写着「低频 MATRIX / 事件计数 ⇒ returns 不足」，
  而我开波前手上已有「121 字段全 MATRIX + coverage 0.5」的画像。**10 个槽位是白烧的。**
  ⇒ **新规（已写进 registry `rule`）：新数据集开波前先按 TO 类推算 F 闸天花板；TO 类隐含 returns < 3.5% 的数据集在 S0 即判死，零槽位成本。**
- 已封存 registry dead_end **`EUR-ANALYST14-F-GATE-CEILING`**（payload 带 `dataset`，`unbound_entries` 未再增长，仍 45）。

### 34.3 三条次级发现

1. **`LOW_SUB_UNIVERSE_SHARPE` 对负 Sharpe 是伪闸**：限值 = `0.5196 × S`，S < 0 时限值转负，
   于是负 Sharpe 候选**自动「过」sub 闸**。实证同批对照：K4（S −0.41，sub 0.29）判 **pass**，
   而它的精确镜像 K5（S +0.41，sub −0.29）判 **fail**（限 0.21）。
   ⇒ **读表纪律：负 Sharpe 行的 sub「pass」不携带任何信息，别当证据。**
2. **EUR 分析师评级 / 估值锚信号近两年发生机制反转**：K10 全期 S −0.90 而 2Y **+0.88**（符号翻转）；
   K9 的 |2Y| 1.12 **大于** |S| 1.04（近期更强）。两条独立证据 ⇒ 任何后续做推荐类 / 目标价类字段，
   **必须单独测近两年窗口**，不能用全期读数代表当下。
3. **`rtk_ptg_*` 前缀不同但同属 `analyst14` ⇒ 混用不违 ATOM**（§33.6 的裁定被本批实际派发验证：
   K9 用了 `rtk_ptg_stddev`/`rtk_ptg_mean`，与 `anl14_*` 同批同数据集，平台正常出结果）。

### 34.4 ★★★★★ 库存重估：池子里其实有 **2 颗全清 + 2 颗只卡 prod**

拉 `get_alpha_details` 逐条核（禁临时脚本），**`failed_ra_count` 是唯一可靠读数**：

| alpha | 载体 | decay | S | F | sub | 2Y | returns | failed_ra | prod | CLUSTER | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `Grge67NZ` | np_y2 · subindustry | 20 | 1.72 | 1.36 | **0.97** | 1.72 | 0.078 | **0** | 0.6812 | **pass** | ✅ **全清** |
| `KPmE8klx` | np_y2 · subindustry | 10 | 1.69 | 1.32 | 0.93 | 1.61 | 0.0761 | **0** | **0.6653** | 1.57 / 1.58 ⚠ | ✅ 全清（险） |
| `xA1dmlVb` | **eps_y2** · subindustry | 40 | **1.84** | **1.50** | **0.98** | 1.71 | 0.0829 | **0** | 0.7683 | 1.42 warn | ⛔ **只卡 prod（−0.068）** |
| `1YjzoEGm` | np_y2 · **industry** | 20 | 1.73 | 1.54 | 0.90 | **2.09** | **0.0995** | **0** | 0.7398 | 1.32 warn | ⛔ **只卡 prod（−0.040）** |
| `kqJZLV2k` | **np_y1** · subindustry | 40 | 1.70 | 1.32 | 0.73 / 限 0.88 | 1.59 | 0.0748 | **1** | 待测 | 1.45 warn | ⛔ 只卡 sub（+0.15） |
| `GrgekNJJ` | np_y2 · 双桶 | 10 | 1.42 | 0.95 | 0.78 | 1.40 | 0.0562 | 3 | <0.7 ✅ | 1.33 warn | ⛔ 卡 S/F/2Y |

- **`Grge67NZ` 与 `KPmE8klx` 同字段同分组、只差 decay（20 vs 10）⇒ self-corr ≈ 0.99 ⇒ 只能出一颗。**
  取舍：`Grge67NZ` 的 F / sub / 2Y 全高且 **CLUSTER_TEST 落在 `pass`**；`KPmE8klx` 的 prod 更低（0.6653 vs 0.6812）
  = 余量更大，但 CLUSTER 1.57 对 1.58 **只差一格**，任何微调都可能翻红。
  按 LL46807「选最特异的」与 XZ17517「用最大 prod 相关判定」，两者各有理据 ⇒ **留给用户裁决，本节只登记**。
- ⚠ **本表纠正 §33.4 的口径**：§33.4 把 `xA1dmlVb` / `1YjzoEGm` 记为「LOW 可修性」，
  那是只看了 prod 缺口。**它们的 `failed_ra` 是 0**——IS 全闸已过，prod 是唯一障碍，
  所以它们是**池子里价值最高的两颗**，不是最低的。修好 prod 即立刻可提交。

### 34.5 ★★★★★ 平台实时算子表（103 个）纠正本档 5 处旧记

`get_operators(region=EUR)` 实时拉取，**取代** `research-data/operators_platform_20260904.json`（已 6 周龄）：

| 算子 | 本档 / 记忆旧记 | 平台实时 | 影响 |
|---|---|---|---|
| **`vector_neut(x, y)`** | ❌ 记为「**不存在**」 | ✅ COMBO/REGULAR，*"finds x\* orthogonal to y"* | **残差化有专用算子了**。EUR profile 明示「破 prod 墙只有残差化一条路」、「只许条件 / 分组 / 残差三式」⇒ 本算子正是被点名许可的那一式 |
| **`tail(x, lower=0, upper=0, newval=0)`** | ❌ 未登记 | ✅ *"if lower<x<upper return newval else x"* | **论坛 lever#4 的 `left_tail`/`right_tail` 是它的简写**，可原语重建（此前记为「不存在、须从原语拼」，方向对但没找到那个原语） |
| `reverse(x)` | 记为「反转**排序** ≈ 1−rank，非变号」 | ✅ 定义 **`- x`** | **是变号**。镜像负 Sharpe 腿一个算子即可，不必 `multiply(·,-1)` |
| `group_mean` | 记为 `(x, group)` | ✅ **`(x, weight, group)` 三参** | 两参写法会错 |
| `ts_backfill` | 记为「`lookback` 是**命名参**」 | 定义 `ts_backfill(x, lookback = d, k=1)`；toolkit 静态闸判「不存在参数 lookback」 | **位置参**：写 `ts_backfill(x, 126)` |

> **★★★★ 记号读法通则（本轮踩坑后确立）**：平台算子定义里 `名 = X` 有两种含义，**必须按 X 的形态区分**——
> **`X` 是占位符**（`d` / `y` / `group` / `nlength`）⇒ **位置参**，名字只是语义标注；
> **`X` 是字面量**（`0.01` / `4` / `false` / `"gaussian"`）⇒ **真命名参**，写 `名=值`。
> 例：`hump(x, hump = 0.01)` 是命名参（0.01 是字面量）；`ts_backfill(x, lookback = d, k=1)` 的 `lookback` 是位置参（`d` 是占位符）。
> **混淆的后果不对称**：把位置参写成命名参 ⇒ 被静态闸拒（本轮，响亮）；把命名参写成位置参 ⇒ **平台 ERROR 并连坐整批 CANCELLED**（静默、代价大）。

### 34.6 ★★★★★ toolkit 静态闸真的在拦，且抓到了平台文档与我自己的检查器都放过的错

直发 `create_multi_simulation` 被拒：`{"error":"toolkit gate 静态门禁未通过 — 整批拒绝提交","gate":"toolkit_static",
"passed":9,"total":10,"failed_expressions":{"9":["[SYNTAX] 函数 ts_backfill 不存在参数 'lookback'"]}}`。

- **9 过 1 挂 ⇒ 整批拒**（fail-closed，符合设计），**等于替我挡掉一次 batch-kill**（记忆 `cancelled-error.md`：
  一条 ERROR 会 CANCELLED 整批 10 条）。
- **值得记的是三层防线的失效顺序**：① 平台 `get_operators` 的定义字符串**误导**了我（`lookback = d` 看着像命名参）；
  ② 我自己写的深度感知 arity 检查器**也放过**了（它按定义把 `lookback` 收进 NAMED 白名单）；
  ③ **只有 toolkit 静态闸拦住**。⇒ **直发仿真前，静态闸是不可替代的一层，不能因为「我已核对平台文档」而跳过。**
- 闸门还给了正规模块指引：`走正规链：wave_gate.py / pipeline.py run（含 5+2 闸 + 多样性 + priors）`。

### 34.7 `validate_expressions` 缺陷第三例，且出现**新子类**

返回 `valid:false`、`platform_field_count:2`、`unknown_fields:["lookback","target_tvr","ts_target_tvr_hump"]`。逐条判读：

- `lookback` / `target_tvr` = **命名参被当字段名**（与 bucket 的 `range` 同一缺陷，第三例）。
- ⚠ **新子类：算子名本身被当未知字段**——`ts_target_tvr_hump` 出现在 `unknown_fields`，而 `ts_target_tvr_decay` **没有**。
  推断：该工具的算子词表**含 `ts_target_tvr_decay` 但不含 `ts_target_tvr_hump`**（词表陈旧）；
  而**遇到不认识的算子，它会把该算子的整个实参列表当字段解析**——这正好解释了为何 `target_tvr` 只在这一腿被抽出，
  而 `hump=0.01` 的 `hump` 没被抽出（`hump` 在词表里 ⇒ 其命名参被跳过）。
- **`platform_field_count: 2` 才是可信读数**（两个真实字段 `eps_y2_estimate_change_3mo` / `netprofit_y1_estimate_change_3mo` 均存在）。
  ⇒ **§33.9 的读法纪律升级：`valid` 与 `unknown_fields` 都不可直读；只读 `platform_field_count` + `fields_checked`，
  并对照 `get_operators` 实时表自行剔除「命名参」与「算子名」两类假阳性。**
- `preflight_expressions` **不能替代**：其描述明写「合并 validate_expressions + fix_vector_fields」，
  用的是同一套字段校验逻辑 ⇒ 同样的假阳性，且**不做平台侧语法检查**。

### 34.8 Batch L：转攻**时序轴 / 残差轴**（multisim `1qYNrm3fK4VOa1PNaI3kqDr`，10 腿）

**归因（不是盲扫）**：§33.2 实测「分桶只改强度与覆盖，不改『什么时候交易』」⇒ 已扫过的持仓轴
（decay / 分组 / p / 字段 / bucket）只能在 **0.63–0.77** 带内挪 prod。而 §34.4 显示两颗最强候选
（`xA1dmlVb` S 1.84、`1YjzoEGm` S 1.73，**failed_ra 均 0**）**只差 prod**。
⇒ **假设：时序轴与残差轴能动持仓轴动不了的那一段 prod。** 本批一次性检验四个族，每族带剂量或对照：

| 腿 | 轴 | 表达式要点 | 预期 / 判读 |
|---|---|---|---|
| L1–L2 | **时序·hump 剂量** | `hump(A, hump=0.01)` / `hump=0.03` | 论坛 GBR 实测 prod 0.32；`hump` 是**换手阈值算子**（*"limits amount and magnitude of changes"*），会造出离散交易事件 |
| L3–L4 | **时序·自动调参** | `ts_target_tvr_hump(A)` / `ts_target_tvr_decay(A)` | **本区从未测过的算子族**。缺省 `target_tvr=0.1`，而 A 的 TO 仅 0.0553 ⇒ 会把换手**往上**调到 0.1，检验「更高换手 = 更特质化 = 更低 prod」 |
| L5–L6 | **残差·vector_neut** | L5 在**原始字段层**对 np_y2 正交化；L6 在**alpha 层**正交化 | EUR profile 点名的唯一破墙路。L5/L6 构成「变换前 vs 变换后残差化」的消融对 |
| L7 | **尾部·tail** | `tail(A, lower=-0.5, upper=0.5, newval=0)` | 论坛 lever#4 的原语重建：**只留 |z|>0.5 的尾部、中段清零** ⇒ 改变「什么时候持仓」 |
| L8–L9 | **覆盖·sub 修复** | `group_backfill(np_y1, subindustry, 126)` / `ts_backfill(np_y1, 126)` | 修 `kqJZLV2k` 的 sub 0.73→0.88。**这条重开 §32「现有杠杆集内不可修」的裁决——该裁决早于拿到覆盖杠杆** |
| L10 | **分组·更细** | `group_zscore(eps_y2, group_cartesian_product(country, subindustry))` | 细于 subindustry ⇒ 按实测方向 prod 更低；EUR 跨多国，country 轴有经济含义（`group_neutralize` 文档明列 country 为合法分组） |

- **载体与设置**：A = `signed_power(group_zscore(eps_y2_estimate_change_3mo, subindustry), 1.8)` = `xA1dmlVb` 本体。
  **decay 40 = `xA1dmlVb` 与 `kqJZLV2k` 共同的自有设置** ⇒ 一个设置块同时服务两条载体，满足铁律⑤，
  且 L1–L7/L10 对 `xA1dmlVb`、L8–L9 对 `kqJZLV2k` 都是**单变量**改动。
- **对照不在批内**：`xA1dmlVb` 本体已在平台（S 1.84 / prod 0.7683），是比批内重跑更强的对照，也不占槽位
  （记忆 `brain-multisim.md`：multisim 按表达式去重，重跑只会返回同一个 alpha id）。
- **`trade_when` 本轮刻意不用**：定义只有 `trade_when(x, y, z)`，三个位置参的语义（哪个是条件 / 哪个是值 / 哪个是退出）
  在算子表里没写清，记忆 `trade-when-decile.md` 还记着它产生**零交易**的坑。
  ⇒ **语义未确证前不入批**（一条 ERROR 连坐整批）。待查 `/operators/trade_when` 文档页后单独开腿。
- **收割后动作**：`failed_ra ≤ 1` 者跑 `check_correlation(type both, refresh=True)`；
  再对 **`KPmE8klx` / `Grge67NZ` / 4-元组全集**跑 `compute_mutual_correlation`
  （按 §33.3 的规矩**喂全集、不喂样本**）。

---

## 三十五、Batch L 全批阵亡与「算子签名字面量」规则的自我否证（2026-10-19）

### 35.1 Batch L 结果：2 条 ERROR 连坐 8 条 CANCELLED，10 槽零数据

`1qYNrm3fK4VOa1PNaI3kqDr` 父级 `status: ERROR`。逐子核验（`lookINTO_SimError_message`）：

| 腿 | 表达式要点 | 子 id | 状态 |
|---|---|---|---|
| L1 | `hump(…, hump=0.01)` | `SzAVJeuG4gzauyCw9GUoXn` | CANCELLED |
| L2 | `hump(…, hump=0.03)` | `3BIwx5fie4yaa5RgPgx3O56` | CANCELLED |
| **L3** | `ts_target_tvr_hump(x)` | `1vm4HX9nB4DPckKDI0oarOZ` | **ERROR** |
| **L4** | `ts_target_tvr_decay(x)` | `41S5BBaxg4HT8LY16GgmAAXr` | **ERROR** |
| L5–L10 | vector_neut / tail / group_backfill / ts_backfill / cartesian | 余 6 个 | CANCELLED |

L3/L4 的平台原文报错完全相同：

> `Required attribute "target_tvr" must have a value.`

**归因**：L1/L2 显式传了 `hump=` ⇒ 只被连坐、自身无错；L3/L4 **省略了** `target_tvr`
⇒ 平台判为「必填属性缺值」⇒ ERROR ⇒ 按记忆 `cancelled-error.md` 的连坐机制取消同批 8 条兄弟。
**这是一次干净的单因归因**：整批唯一的语法缺陷就是省略那个命名参。

### 35.2 ★★★★★★ §34.5 的记号规则被否证：`名 = 字面量` 有**三种**含义，不是两种

§34.5 我写下：「X 是字面量 ⇒ 真命名参 ⇒ 写 `名=值`」，并推出「命名参当位置参写 = 平台 ERROR + 连坐」。
**Batch L 暴露了第三种情形，而且它出现在我以为最安全的地方——省略不写。**

紧接着 Batch N 首派被静态闸拦下，报错更狠：

> `函数 ts_backfill 最多接受 2 个参数，但提供了 3` ／ `函数 ts_backfill 不存在参数 'k'`

而 live `get_operators(region=EUR)` 给出的定义明明是 `ts_backfill(x, lookback = d, k=1)`。

**⇒ 平台定义串里 `名 = 字面量` 实际有三种互不相容的语义，且从字面上完全无法区分**：

| 情形 | 例 | 省略不写的后果 | 显式传的后果 |
|---|---|---|---|
| (a) 真命名参 · **必填** | `ts_target_tvr_*(…, target_tvr=0.1)` | **平台 ERROR + 连坐整批** | ✅ 正常 |
| (b) 真命名参 · 可选 | `hump(x, hump = 0.01)` | ✅ 用缺省 | ✅ 正常 |
| (c) **本区域/本 scope 根本不接受该参** | `ts_backfill` 的 `k` | ✅ 正常 | **静态闸拦下（幸运）／平台 ERROR** |

**`target_tvr` 是 (a)、`k` 是 (c)，两者在定义串里长得一模一样**（都是 `名 = 字面量`）。
⇒ **任何「从定义串推签名」的方法都不可靠，包括我上一节刚写下的那条规则。**

**★ 可执行铁律（取代 §34.5 的推论）**：

1. **算子元数与命名参的唯一权威 = toolkit 静态闸**（`create_multi_simulation` 内建，fail-closed，零成本）。
   `get_operators` 的定义串只用来**发现算子存在**与**读语义**，**绝不用来定签名**。
2. **新算子入批前必须先被静态闸放行**；被拦就按闸的话改，不要按平台文档的话改。
3. **静态闸放行的命名参一律显式传**（覆盖情形 a，成本为零）；**静态闸不认的参一律不传**（覆盖情形 c）。
   两条合起来 = 「以闸为准，闸说什么就写什么」。
4. **连坐半径要靠分批控制**：一批里未证算子越多，一条 ERROR 的代价越大。
   Batch L 把 4 个未证算子（hump / ts_target_tvr_hump / ts_target_tvr_decay / vector_neut / tail）
   塞进同一批 ⇒ 半径 10。Batch M/N 改为「M 全用已证算子（半径 10 但风险≈0）+ N 专放未证算子（半径 5）」。

> ⚠ **本节是对 §34.5 / §34.6 的更正，不是补充。** §34.6 已经写过「静态闸不可替代」，
> 而我在同一会话内就又从定义串推了一次签名（`k=1`）并被闸当场逮住。
> **教训的教训：一条规则被写下来的同一轮里就可能被自己违反——所以规则要写成「以谁为准」，
> 不能写成「怎么推」。**

### 35.3 ★★★★ `create_multi_simulation` 的设置是**批级**的，decay 是标量 ⇒ 设置对比波必须分批

工具签名实测：`decay: int`（单值）、`neutralization: str`（单值）、`universe` / `region` 必填且无缺省。
**没有 per-item settings**。⇒ 「同一批里扫 decay 10/20/40」在结构上不可能，
§33 的 decay 阶梯必然是跨批测出来的。

**推论（本次直接影响设计）**：Batch M 想同时做「分组轴 × decay 轴」是不可能的，
必须**锁死一个 decay**。选 **decay 10**，理由是它是实测 prod 阶梯的最低点
（np_y2·subind：d10 0.6653 ＜ d20 0.6812 ＜ d40 0.6933），而 **prod 正是当前唯一的约束**；
代价是 2Y 会比 d20 低约 0.11（`KPmE8klx` 1.61 vs `Grge67NZ` 1.72），仍在 1.58 线上。

### 35.4 ★★★★★★ 候选池不是「一张清单」，是**两个互斥的组合**——此前一直被当成一张清单在排序

把互相关数字摊开后结构才显出来：

- `KPmE8klx` × `Grge67NZ` = **0.9903**（同字段同分组，只差 decay）⇒ 二者只能出一颗；
- `KPmE8klx` × `GrgekNJJ` = **0.8482** ✗ ⇒ **Family A 一旦出手就封掉 4-元组里那颗 prod 已清的**；
- `KPmE8klx` × `1YjzoEGm` = 0.8041 ✗、× `xA1dmlVb` = 0.7990 ✗。

| | 成员 | prod | failed_ra | 最多能出 | 状态 |
|---|---|---|---|---|---|
| **Family A** | `KPmE8klx`(0.6653) / `Grge67NZ`(0.6812) | 均 ✅ | 均 **0** | **1** | **今天就能提**（差用户确认） |
| **Family B** | `1YjzoEGm` `xA1dmlVb` `kqJZLV2k` `GrgekNJJ` | 3 ✗ / 1 ✅ | 0·0·1·3 | **最多 4**（六对互相关全 <0.7：0.6773/0.4671/0.6659/0.5504/0.6416/0.4801） | 需破 3 个 prod + 修 1 组 IS 闸 |

**A 与 B 互斥**（A 的任一员与 B 的 `GrgekNJJ`/`1YjzoEGm`/`xA1dmlVb` 都 >0.7）。
⇒ **B 的期望产出是 A 的 4 倍**，所以 Batch M 全部火力对准 B，A 留作「B 失败时的保底 1 颗」。

**★ 一个反直觉的结构发现（决定了 B 不能被"修好"）**：
`1YjzoEGm`（np_y2 × **industry**）与 `GrgekNJJ` 互相关 <0.7，
而 `KPmE8klx`（np_y2 × **subindustry**，同字段同 decay 族）与 `GrgekNJJ` = 0.8482。
⇒ **让 `1YjzoEGm` 与 `GrgekNJJ` 解耦的正是「industry 这个粗分组」本身。**
所以修 `1YjzoEGm` 的 prod 时**绝不能把它改成 subindustry**（那会把它推回 Family A、同时踢出 4-元组）；
只能用 **`group_cartesian_product(country, industry)`** 这种「比 industry 细、比 subindustry 粗」的中间档
—— Batch M 第 4 腿就是为此设计的。

### 35.5 `kqJZLV2k` prod 实测 = **0.7459 ✗**，且直方图显示只有**一颗** prod alpha 挡路

`check_correlation(kqJZLV2k, type both, refresh=True)`：
`max_correlation 0.7459`、`passes_check false`、`min -0.4604`。关键在直方图尾部：

| 桶 | [0.4,0.5) | [0.5,0.6) | [0.6,0.7) | **[0.7,0.8]** |
|---|---:|---:|---:|---:|
| n | 4639 | 72 | 16 | **1** |

**`[0.7,0.8]` 只有 1 颗，就是那条 0.7459 本身。** 也就是说：
`kqJZLV2k` 与整个 prod 宇宙的相关性分布在 0.7 处**断崖式截止**（0.6–0.7 只有 16 颗，0.7 以上只有 1 颗）。
⇒ **它不是"撞进一堵密墙"，是"被一颗特定 alpha 卡住"**，只需 −0.046 就过线。
按 `wq-window-valley-break-prod-wall` 的族级判据这属于**可救**形态（谷就在 0.7 左侧紧邻处）。
⚠ 但同一 skill 的方向指引（扫窗口找谷）在 §33.2 已被本数据集证伪——**这里只借它的"n=1 可救"判据，不借它的杠杆**。

`kqJZLV2k` 同时还有 **sub 0.73 vs 限 0.88 ✗**（failed_ra 1 就是它）。
⇒ 需要**同时**修 prod（分组轴）与 sub（覆盖轴）；Batch M 第 3 腿（分组）+ Batch N 第 5 腿（`ts_backfill` 覆盖）分别对应。

### 35.6 ★★★ 赢家的 `neutralization` 是 **`FAST`**，不是区域控制面板写的 `SUBINDUSTRY`

`get_alpha_details` 实测 `xA1dmlVb` 与 `GrgekNJJ` 的完整设置块，两者**逐字段相同**（只差 decay）：

```
instrumentType EQUITY · region EUR · universe TOP2500 · delay 1 · neutralization FAST
truncation 0.08 · pasteurization ON · unitHandling VERIFY · nanHandling ON · maxTrade ON
maxPosition OFF · language FASTEXPR · visualization false
startDate 2014-01-01 · endDate 2023-12-31 · simulationMode FULL
```

- **区域控制面板 / `settings.json` 写的是 `TOPCS1600` + `SUBINDUSTRY` + `decay 4`，与全部赢家实际设置三处不符**
  （universe、neutralization、decay）。Batch L/M/N 用的是赢家的设置（铁律⑤），**不是**控制面板的设置。
- ⚠ **这解释了本档 §33 反复出现的"换档否证"**：面板值与实战值本就是两套。
  **修控制面板属 `tracking/EUR/config/` 的人工决策**（`$WQ_PY -m wqb.profiles render` 只从它生成），
  本档只登记实测差异，不代改。
- `xA1dmlVb` 的塔挂载实测：`pyramids.effective 1`，`EUR/D1/ANALYST`，`multiplier 1.3`，`MATCHES_PYRAMID` ∈ pass。
  `checks.fail = []`，warning 只有 `CLUSTER_TEST 1.42 / 1.58`、`MATCHES_THEMES`、`OSMOSIS_ALLOCATION`。

### 35.7 `xA1dmlVb` 的 sub 闸余量只有 2.5%——「高 S 双刃剑」在这条上是活的

`LOW_SUB_UNIVERSE_SHARPE` 是比率闸（TOP2500 = 0.5196 × S）：

| alpha | S | sub 实测 | sub 限 | 余量 |
|---|---:|---:|---:|---:|
| `xA1dmlVb` | 1.84 | 0.98 | 0.956 | **+2.5%** |
| `GrgekNJJ` | 1.42 | 0.78 | 0.738 | +5.7% |
| `Grge67NZ` | 1.72 | 0.97 | 0.894 | +8.5% |
| `kqJZLV2k` | 1.70 | 0.73 | 0.883 | **−17% ✗** |

⇒ **对 `xA1dmlVb` 施加任何"降 S 换降 prod"的杠杆都会同步抬高 sub 限的通过难度**（限随 S 线性下降，但 sub 值通常掉得更快）。
这就是 §33 那条「选刚好过主闸的 S，不追最高 S」在本池的具体形态：**S 1.84 不是优势，是 2.5% 的薄冰。**
Batch M 第 10 腿（`p=1.8 → 1.4`）就是去测这块薄冰能不能换成更厚的 sub 余量。

### 35.8 Batch M / N 设计（均在飞）

**Batch M `4tgvmW8rQ4kjcDH10niTfPGJ`** — decay 10 · FAST · TOP2500 · **零未证算子**
（`signed_power`/`group_zscore`/`group_cartesian_product`/`group_neutralize`/`bucket`/`rank`/`ts_mean` 全部出现在平台已返回结果的 alpha code 里）：

| # | 表达式要点 | 打谁 | 单变量对照 |
|---|---|---|---|
| M1 | eps_y2 × **cartesian(country, subindustry)** | `xA1dmlVb` prod | vs `xA1dmlVb`（分组变细，decay 40→10 双变量，故另需 M10 类的同 decay 基准） |
| M2 | np_y2 × cartesian(country, subindustry) | np_y2 最细档 | vs `KPmE8klx`（d10·subind·0.6653） |
| M3 | np_y1 × cartesian(country, subindustry) | `kqJZLV2k` prod | vs `kqJZLV2k` |
| **M4** | np_y2 × **cartesian(country, industry)** | **`1YjzoEGm` prod，且必须保住 industry 的解耦性** | vs `1YjzoEGm`（industry·d20·0.7398） |
| M5 | eps_y1 × cartesian(country, subindustry) | 新字段 × 已胜结构 | vs M1（换字段） |
| M6 | np_y2_**coeff_var** × cartesian(country, subindustry) | 新字段（离散度**水平**，非修正量） | vs M2（换字段） |
| M7 | `group_neutralize(…, bucket(rank(ts_mean(np_y2, 252)), range="0,1,0.5"))` | `GrgekNJJ` 修 S：**单桶·粗档** | vs `GrgekNJJ`（双桶·0.2） |
| M8 | 同上但**双桶都改 0.5** | `GrgekNJJ` 修 S：剂量 | vs M7 / M9 |
| M9 | `group_neutralize(…, bucket(rank(coeff_var), range="0,1,0.5"))` | **隔离是哪一根条件轴吃掉了 Sharpe** | vs M7（换桶的字段） |
| M10 | eps_y2 × subindustry，**p = 1.4** | 幂次轴 / sub 薄冰 | vs `xA1dmlVb`（p 1.8） |

**Batch N `4oVzcT4aL59fbCEiEd0QfyM`** — decay 10 · 同设置 · **专放未证算子，半径 5**，含批内对照：

| # | 表达式要点 | 未证算子 | 用途 |
|---|---|---|---|
| **N0** | `signed_power(group_zscore(eps_y2, subindustry), 1.8)` | — | **批内对照**（同 decay 同设置的载体本体） |
| N1 | `tail(载体, lower=-0.5, upper=0.5, newval=0)` | `tail` | 论坛杠杆#4（GLB EPS 修正族 prod **0.42**，与本池字段族同源，先验最高） |
| N2 | `hump(载体, hump=0.01)` | `hump` | 论坛杠杆#5（GBR 0.32）+ 帖 `31365517513495`（hump 修 **sub** 而非 prod） |
| N3 | `vector_neut(eps_y2 载体, np_y2 载体)` | `vector_neut` | **残差化 = EUR profile 明写"破 prod 墙只有这一条路"** |
| N4 | `signed_power(group_zscore(ts_backfill(np_y1, 126), subindustry), 1.8)` | `ts_backfill`（2 位置参） | `kqJZLV2k` 的 **sub 0.73→0.88** 覆盖修复；帖 `38669179039255` |

- **`group_backfill` 与 `ts_target_tvr_*` 本轮不用**：前者有 `std = 4.0` 未过闸验证（情形 a/c 未知），
  后者已实证必填 `target_tvr` 但**元数上限未经闸确认**。按 35.2 铁律 1，两者都要先单独过闸再入批。
- **静态闸已放行** N1/N2/N3 的命名参写法（`lower=`/`upper=`/`newval=`/`hump=`）与 `vector_neut(x, y)` 二元形式
  ⇒ 这三条的签名有闸背书，不是我从定义串推的。

---

## 三十六、平台权威文档两则：ATOM 的正式定义（含一条我从未跟踪的提交闸）与 `trade_when` 语义

来源：`get_documentation_page(page_id="single-dataset-alphas")` 与 `page_id="intermediate-pack-part-3"`
（均属 `Consultant Information` / `Getting Started` 官方教程，`lastModified 2026-09-18`）。
**这两则是平台原文，权威级高于论坛帖与本档任何推断。**

### 36.1 ★★★★★★ Single Dataset Alpha（= ATOM）的正式定义：**6 个分组字段被明文豁免**

> "Single Dataset Alphas use data fields from only one dataset to build the entire Alpha expression,
> **excluding 6 permitted grouping fields that can be a part of the expression –
> `country`, `exchange`, `market`, `sector`, `industry` and `subindustry`**."

> "The use of **`inst_pnl()` and `convert()`** operators is considered as **utilizing the pv1 dataset**
> since these operators rely on pv1 data for calculations."

**这就是用户要求的「把混数据集和 ATOM 的边界定义清楚」的平台权威答案**，它同时确证并收紧了 §33.6 / §34.3：

| 判据 | 平台原文结论 | 对本项目的直接影响 |
|---|---|---|
| 边界单位 | **dataset**，不是 category、也不是字段名前缀 | 与 §34.3 的实测一致（`rtk_ptg_*` 与 `anl14_*` 同属 `analyst14` ⇒ 同批混用平台正常返回） |
| 分组字段 | **`country`/`exchange`/`market`/`sector`/`industry`/`subindustry` 六个明文豁免** | ✅ **Batch M 的 `group_cartesian_product(country, subindustry)`、`group_zscore(…, country)` 全部 ATOM 合规**——此前只是从 `group_neutralize` 的算子文档推的，现在有专页背书 |
| **隐性破 ATOM 的算子** | **`inst_pnl()`、`convert()` 等同于引入 pv1** | ⚠ **新硬规则：ATOM 表达式里禁止出现这两个算子**——它们不引入"看起来像别的数据集的字段"，所以肉眼审不出来，会静默把 alpha 降级成跨数据集 |

### 36.2 ★★★★★★★ ATOM 的提交闸是**另一套**：IS Ladder 被换成「2Y Sharpe ≥ 2.38（D1）」——**我一直在跟踪的 1.58 不是这道闸**

> "Single Dataset Alphas have slightly relaxed submission criteria as compared to regular Alphas.
> These Alphas **don't need to pass the IS Ladder Sharpe Test**. Instead, **only the last two year Avg IS Sharpe**
> of the Alpha must clear the following thresholds:"
>
> | Last 2Y Sharpe limit | Threshold |
> |---|---|
> | **Delay-1** | **2.38** |
> | Delay-0 | 3.96 |
>
> "**Note**: If the **turnover of Alpha is less than 30%**, the IS Sharpe Ladder PASS_THRESHOLDS are
> **multiplied by a factor of 0.85**."
>
> "All Alpha simulations with properties of Single Dataset Alphas shall display the message
> *'2 year Sharpe of \<value\> is below cutoff of \<limit\>'* … in the IS Testing Status tab
> **instead of** the IS Ladder Sharpe Pass/Fail criteria."

**⇒ 本池全部候选 turnover 都 < 30%（0.055–0.069），故 ATOM 的 D1 生效线 = `2.38 × 0.85 = 2.023`。**

拿这条线重排候选池（**这是一次彻底的重排**）：

| alpha | 2Y Sharpe | vs ATOM 线 **2.023** | vs 我一直用的 `LOW_2Y_SHARPE` 1.58 | failed_ra |
|---|---:|---|---|---:|
| **`1YjzoEGm`** | **2.09** | **✅ 过（余量 +3.3%）** | ✅ | **0** |
| `Grge67NZ` | 1.72 | **✗ 差 0.30** | ✅ | 0 |
| `xA1dmlVb` | 1.71 | **✗ 差 0.31** | ✅ | 0 |
| `KPmE8klx` | 1.61 | **✗ 差 0.41** | ✅ | 0 |
| `kqJZLV2k` | 1.59 | **✗ 差 0.43** | ✅ | 1 |
| `GrgekNJJ` | 1.40 | **✗ 差 0.62** | ✅（未列入 fail） | 3 |

**★ 结论：`1YjzoEGm` 是全池唯一同时满足「failed_ra = 0」与「ATOM 2Y 线」的候选。**
它此前在我的排序里只是"4-元组的一员、prod 0.7398 待修"，现在它是**唯一一颗只差 prod 一个闸的 alpha**。

**★★ 为什么 `failed_ra_count` 没抓到这道闸（这条是方法论教训）**：
`xA1dmlVb` 的 `checks` 里 **`IS_LADDER_SHARPE` 根本不存在**（fail/warning/pass/pending 四个列表里都没有），
而 `LOW_2Y_SHARPE` 在 `pass` 里、值 1.71。
⇒ 平台对 ATOM **不产出** IS Ladder 这个 check 项，改在 IS Testing Status 页里以**一句话消息**呈现；
`get_alpha_details` 的 `checks` 与 `ra_failed_checks` 都**不包含那句话**。
**所以「`failed_ra_count = 0`」不等于「ATOM 可提交」**——它只覆盖 18 项具名 RA check，
覆盖不到这条以消息形式存在的 ATOM 专属 2Y 线。
⚠ **本条尚需一次实证核验**（读某颗 alpha 的 IS Testing Status 记录，看 cutoff 到底是 2.023 还是别的数），
在此之前**按 2.023 从严规划**：宁可当作过不了，也不要在提交环节才发现。

**★★★ 对策略的即时改写**：
1. **优先修 `1YjzoEGm` 的 prod（0.7398 → <0.7，只差 0.040）**，而不是继续修 `xA1dmlVb`（差 0.068 且 2Y 差 0.31，要同时修两个闸）。
   ⇒ Batch M 第 4 腿（np_y2 × `cartesian(country, industry)` @ d10）就是它的主修腿，**优先级从第 4 升到第 1**。
2. **`1YjzoEGm` 必须保住 industry 分组**（§35.4：正是 industry 让它与 `GrgekNJJ` 解耦），
   所以只能用 `country × industry` 这种"比 industry 细、比 subindustry 粗"的中间档，不能直接换 subindustry。
3. **2Y Sharpe 从此是设计目标，不是事后检查**。任何"降 S 换降 prod"的杠杆（如 M10 的 p=1.4）都要先看 2Y 会不会跌破 2.023。
   `xA1dmlVb` 的 2Y 1.71 已经低于线 ⇒ **它作为提交候选的价值大幅下降**，只适合当"结构对照"用。

### 36.3 ★★★★★ `trade_when` 语义确证（论坛杠杆#3 解封），并解释了记忆里的零交易坑

> **Syntax: `trade_when(Event_condition, Alpha_expression, -1)`**
> "If **exit condition** is true, the Alpha is equal to **NaN (does not trade)**.
> If exit condition is false and **event condition is true, Alpha = Alpha expression**.
> Finally, if exit condition is false and event condition is false,
> **the Alpha is equal to the previous day's Alpha**, thus the same positions are held."
> 例：`rank(trade_when(volume>adv20, -returns, -1))`

- **三个位置参 = (事件条件, alpha 表达式, 退出条件)**；`-1` 是「永不退出」的惯用哨兵值。
- **★ 记忆 `trade-when-decile.md` 的零交易坑有了机制解释**：第三个参若被误写成"永真"，alpha 恒为 NaN ⇒ 不交易；
  而**事件条件若极少为真**，alpha 就长期沿用前一日值 ⇒ 持仓不更新 ⇒ 看起来像"零交易"。
  **对 decile/bucket 评分用 `trade_when` 恰好踩这一条**：离散档位上的阈值穿越是稀有事件。
  ⇒ **正确用法：事件条件必须是"频繁但选择性"的**，对修正类信号最自然的事件是
  「**今天发生了修正**」= `x != ts_delay(x, 1)`（配合新编目的 `days_from_last_change(x)` 可作诊断）。
- **同页确证 `if_else(Event_condition, Alpha_expression_1, Alpha_expression_2)`**，
  且官方演练实测：同一想法从 `if_else` 换成 `trade_when` ⇒ **turnover 下降、fitness 0.71 → 0.93**。
  这是「`trade_when` 是降换手杠杆」的**平台原文级**证据（此前只有论坛旁证）。
- ⚠ **但对本池要慎用**：本池的死法是 **returns 不足 → F 封顶**（§34.2 的 analyst14 教训、`GrgekNJJ` F 0.95）。
  `trade_when` 降换手的同一机制会**压 returns**，可能把 F 推到线下。
  ⇒ **入批前必须算 F 闸天花板**（§34.2 的规则同样适用于"用杠杆改换手"这件事，不只适用于选数据集）。

### 36.4 ★★★★ FASTEXPR 支持**多语句赋值**（`;` 分隔）——一直在写单行嵌套是没必要的

同页官方演练的 simulation 示例原文：

```
event=volume>adv20;
alpha=(-ts_delta(close,3));
trade_when(event,alpha,-1)
```

⇒ **`regular` 字段可以是多语句脚本**，用 `;` 分隔、末句为返回值。
对本项目的直接价值：**复杂表达式（如 `GrgekNJJ` 那条 200+ 字符的双桶嵌套）可以先赋值再组合**，
既好读，也让静态闸的报错定位到具体语句（`location.line` 字段本就是按行给的）。
⚠ 但引入换行后要重验静态闸与 multisim 的去重键（记忆 `brain-multisim.md`：按表达式去重），
**换行/空格不同是否算同一表达式未经实测** ⇒ 首次使用先单独开一条小批验证，不要混进正式波。

### 36.5 同页其它可直接引用的平台结论

- 官方演练 Iteration 3 实测：同一 alpha 把 neutralization 从 SUBINDUSTRY 改 **INDUSTRY**、decay 4→**2**、
  truncation 0.01 ⇒ **Sharpe 1.75 → 1.93、fitness 0.93 → 1.07**，代价是 turnover 上升。
  ⇒ 「**降 decay + 粗化中性化**能同时抬 S 与 F」有平台原文级旁证，与本档 §33 实测的
  「industry 比 subindustry 的 S 更高（`1YjzoEGm` 1.73 vs `Grge67NZ` 1.72）、prod 也更高（0.7398 vs 0.6812）」方向一致。
  ⚠ **truncation 是锁定项（不作扫描维度），故这三条里只有 decay 与中性化可用。**
- 官方 tips：「**Do not spend an extraordinary amount of time improving a single idea**… Move on to another
  datafield or operator.」⇒ 与本档 §33.2「持仓轴只能在 0.63–0.77 带内动」的收敛判断同向，
  是「该换轴而非继续扫参」的平台级背书。
- 待读（同索引里与本档直接相关、尚未取的页）：`how-pass-sub-universe-test`（`kqJZLV2k` 的 sub 0.73→0.88 正卡这道）、
  `neut-cons` / `neut-users`（**`FAST` 中性化的官方说明**，§35.6 刚发现全部赢家都用 FAST 而控制面板写 SUBINDUSTRY）、
  `how-can-you-avoid-duplicate-simulations`（multisim 去重键的权威口径）、
  `consultant-submission-tests`（提交闸全表，核验 §36.2 的 cutoff 到底怎么算）。
- ⚠ **论坛取证本轮两次 `ConnectionResetError(10054)`**（`read_forum_post(42082175035159)`）。
  按 §8.11 / `recon_evidence` 的三分法这是 **`error`（found=null）= 工具故障**，
  **不得记作「论坛无解」**，也不得据此判死任何方向。待重取。

---

## §37 中性化轴的完整地图：四闸联立在已测网格内无解，而 CROWDING 是唯一压缩相关性分布的档（2026-10-20）

### 37.1 ★★★★★★★ Batch Q / R 收割：中性化把 **2Y 与 sub 比推向相反方向**，这是本战役的中心结构

同一表达式 `signed_power(group_zscore(<field>, <group>), p)`、同 decay 20、同 TOP2500/D1/trunc0.08，**只换 neutralization**。
Batch Q = `3M3mA86Xg4xvcAxtmDWv62R`（SUBINDUSTRY，6/6 complete）；Batch R = `2Z9Jrtdzx4j78G2184BaoUxd`（SLOW，6/6 complete）。

**Batch Q（SUBINDUSTRY/d20）——本战役第一批 6 腿全过 sub 闸的批次：**

| 腿 | alpha | 字段 · 分组 | S | F | TO | returns | sub | 限 | **sub/S** | 2Y | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1 | **`1YjzwR6K`** | np_y2 · industry p1.8 | 1.46 | 1.27 | 0.0431 | 0.0949 | 0.81 | 0.76 | **0.5548** ✅ | **1.60** | **1** |
| Q2 | `vROvjbab` | np_y2 · industry p2.0 | 1.42 | 1.26 | 0.0440 | **0.0989** | 0.83 | 0.74 | **0.5845** ✅ | 1.58 | 2 |
| Q4 | `rKdPjw63` | np_y1 · industry p1.8 | **1.51** | **1.31** | 0.0434 | 0.0947 | 0.78 | 0.78 | 0.5166 | 1.15 | 2 |
| Q5 | `88velZkq` | np_y2 · subind p1.8 | 1.44 | 1.14 | 0.0401 | 0.0777 | 0.82 | 0.75 | **0.5694** ✅ | 1.41 | 2 |
| Q6 | `58jkl176` | eps_y2 · subind p1.8 | 1.34 | 1.03 | 0.0399 | 0.0742 | 0.74 | 0.72 | **0.5522** ✅ | 1.25 | 2 |
| Q3 | `xA1djoXJ` | eps_y2 · industry p1.8 | 1.17 | 0.93 | 0.0429 | 0.0797 | 0.63 | 0.61 | **0.5385** ✅ | 1.22 | 3 |

**6 腿全部 `checks.fail = []`**——失败项全在 `warning` 里，唯一可信读数是 `failed_ra_count`（§31.2 再次验证）。
**F 全部 ≥ 1.03 ⇒ SUBINDUSTRY 档的约束不是 F，是 S（1.42–1.51 < 1.58）与 2Y（1.58–1.60 ≪ 2.023）。**

**Batch R（SLOW/d20）——全灭，但归因价值极高：**

| 腿 | alpha | 字段 · 分组 | S | F | returns | sub | 限 | sub/S | 2Y | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| R4 | `0mjMRbx8` | np_y1 · industry p1.8 | **0.90** | 0.51 | 0.0401 | 0.34 | 0.47 | 0.378 | 0.96 | 4 |
| R1 | `58jkQZGM` | np_y2 · industry p1.8 | 0.68 | 0.33 | 0.0303 | 0.24 | 0.35 | 0.353 | 1.10 | 4 |
| R2 | `mLYVgPKW` | np_y2 · industry p2.0 | 0.65 | 0.33 | 0.0317 | 0.25 | 0.34 | 0.385 | 1.03 | 4 |
| R5 | `bl8dRYJr` | np_y2 · subind p1.8 | 0.61 | 0.25 | 0.0211 | 0.28 | 0.32 | 0.459 | 0.88 | 4 |
| R6 | `LL5d9PmL` | eps_y2 · subind p1.8 | 0.46 | 0.16 | 0.0159 | 0.15 | 0.24 | 0.326 | 0.50 | 4 |
| R3 | `rKdP519m` | eps_y2 · industry p1.8 | 0.27 | 0.09 | 0.0127 | −0.04 | 0.14 | — | 0.30 | 4 |

**★★ R1 是 `1YjzoEGm` 的逐字同表达式、同 decay、只换中性化 ⇒ 单变量归因最干净的一对：**
**S 1.73 → 0.68（−1.05）、2Y 2.09 → 1.10（−0.99）、F 1.54 → 0.33。**
⇒ **SLOW 不是"弱一档"，是把信号删掉了。机制结论：分析师修正信号本身就是快变因子，
慢中性化剥掉的正是这条 alpha 赖以存在的那部分暴露。**（与 §31.3「中性化决定 prod」互补：
中性化不只决定 prod，**还决定信号存不存在**。）

**★★★ 四档中性化的完整地图（同表达式 · industry 分组 · d20，CROWDING 为 d80/p1.4）：**

| neutralization | S | 2Y | **sub/S** | **prod** | 唯一失败闸 |
|---|---:|---:|---:|---:|---|
| **FAST**（`1YjzoEGm`） | **1.73** ✅ | **2.09** ✅ | 0.5202 ✅(+0.08%) | 0.7398 ❌ | **只差 prod** |
| **CROWDING**（`npA8wwz8`，d80/p1.4） | **1.63** ✅ | **2.09** ✅ | 0.4356 ❌ | **0.6257** ✅ | **只差 sub** |
| **SUBINDUSTRY**（`1YjzwR6K`） | 1.46 ❌ | 1.60 ❌ | **0.5548** ✅(+6.8%) | **0.7649** ❌ | 差 S + 2Y + prod |
| **SLOW**（`58jkQZGM`） | 0.68 ❌ | 1.10 ❌ | 0.353 ❌ | 未测 | 全灭 |

**⇒ 排序：S 与 2Y 上 FAST ≳ CROWDING > SUBINDUSTRY ≫ SLOW（同向单调）；
但 sub 比上 SUBINDUSTRY(0.555) > FAST(0.520) > CROWDING(0.436) > SLOW(0.353)（次序不同）。**
**★ 「2Y 达标集 {FAST, CROWDING}」与「sub 比宽裕集 {SUBINDUSTRY}」不相交**——这就是四闸联立无解的准确表述。

### 37.2 ★★★★★★★ prod 地图补完：**CROWDING 不是"降低"相关性分布，是"压缩"它**

`check_correlation(1YjzwR6K, refresh=True)` → `all_passed: false`，`max_correlation` **0.7649**，
`[0.7,0.8] n=2`、`[0.6,0.7] n=8`、`[0.5,0.6] n=493`、`[0.4,0.5] n=20409`、`min −0.5489`。

**⚠ 这否证了我当场准备写下的一条定律**（「非 FAST ⇒ prod 低」）：SUBINDUSTRY 的 prod **比 FAST 更差**（0.7649 > 0.7398）。
把三档直方图并排（同一个 ~2.05M 的生产池）：

| 桶 | `npA8wwz8` **CROWDING** | `1YjzwR6K` **SUBINDUSTRY** | 倍数 |
|---|---:|---:|---:|
| [0.4,0.5] | **14** | 20 409 | **1458×** |
| [0.5,0.6] | **1** | 493 | **493×** |
| [0.6,0.7] | **4** | 8 | 2× |
| **[0.7,0.8]** | **该桶完全不存在** | 2 | — |
| **> 0.4 的总质量** | **19** | **20 912** | **≈1100×** |

**★★★ 定律（本战役唯一被三次独立复现的 prod 结论）**：
**prod < 0.7 只在 CROWDING 下出现过，且 CROWDING 的作用形态是「把整条相关性分布压向 0」，不是「把最大值挪下来一点」。**
这与 §31.3 的机制解释一致并把它量化了：CROWDING 显式剥掉「拥挤持仓」，而生产池里大家共同持有的**正是**拥挤持仓
⇒ 剥掉之后与全池的重叠面积塌缩三个数量级。FAST 只剥快变因子，SUBINDUSTRY 只剥子行业均值，**两者都保留了风格暴露**，
所以都留在 0.73–0.77。

**⇒ 分组 × 中性化的 prod 全表（本战役实测）：**

| | subindustry 分组 | industry 分组 |
|---|---|---|
| **FAST** | 0.6653(d10) / 0.6812(d20) / 0.6933(d40) ✅ → 0.7090(d60) / 0.7327(d80) / 0.7607(d120) ❌ | **0.7398(d20)** ❌ |
| **CROWDING** | 0.5905(window22) / 0.6264(d40) / 0.6257(d80) ✅ | **0.6257(d80)** ✅ |
| **SUBINDUSTRY** | — | **0.7649(d20)** ❌ |

**⇒ `industry` 分组统一加 ≈ +0.06~+0.14 prod；CROWDING 统一减 ≈ −0.11。
只有 CROWDING 的折扣够大，能吸收 industry 分组的溢价。**
这就是为什么 **2Y ≥ 2.023 必须用 industry 分组（§33）** 与 **prod < 0.7 必须用 CROWDING** 这两条硬要求
**唯一地交在 `npA8wwz8` 这一格上**——它不是运气好，是两个约束的交点。

### 37.3 ★★★★★★ `npA8wwz8` 全档：**只差 sub 一闸**，且它的 sub 缺口是机制性的、不可修

`get_alpha_details(npA8wwz8)` 逐字读数：
`signed_power(group_zscore(netprofit_y2_estimate_change_3mo, industry), 1.4)`；
EQUITY/EUR/**TOP2500**/D1/**decay 80**/**CROWDING**/trunc0.08/pasteurize ON/VERIFY/nanHandling ON/maxTrade ON/maxPosition OFF/FASTEXPR/2014-01-01→2023-12-31/FULL。
**S 1.63 · F 1.25 · TO 0.0399 · returns 0.0736** · DD 0.0709 · margin 0.003693 · long1502/short1318 · pnl 7 598 947 ·
**sub 0.71（限 0.85）** · **2Y 2.09** · `failed_ra_count` **1** · `ra_failed_checks ["LOW_SUB_UNIVERSE_SHARPE"]`。
`checks.pass` = LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / **LOW_2Y_SHARPE** / MATCHES_PYRAMID；
`warning` = CLUSTER_TEST 1.11（**仅分类，不阻断**）/ MATCHES_THEMES / OSMOSIS_ALLOCATION；
`pending` = SELF / DATA_DIVERSITY / PROD / REGULAR_SUBMISSION。
`pyramids {effective 1, [EUR/D1/ANALYST ×1.3]}`。
`check_correlation` → **`all_passed: true`**：prod **0.6257**（`from_cache`, cached_at 2026-10-20T01:51:42）、
self **0.13399**（top: gJj1nxLM 0.1340 / 78jdv6b1 −0.0238 / Wj71Q12o −0.0283 / Wj7g2gAx −0.1265；pool 4 / full_os 6 / ppac 2）。

**闸计分卡：S ✅ F ✅ TO ✅ weight ✅ 2Y(ATOM 2.09 ≥ 2.023) ✅ prod ✅ self ✅ —— 只败 sub（0.71 vs 0.85 = 0.5196×1.63）。**

**★★ 为什么它的 sub 缺口不可修（机制级，不是调参级）**：
CROWDING 的定义就是剥掉「拥挤持仓」，而拥挤持仓 = 大盘流动性好的重仓股 ⇒
**残差信号天然集中在 1300–2500 名的小盘上 ⇒ TOP1200 子宇宙必然丢失信号。**
这不是参数没调好，**这是该中性化的定义所蕴含的**。三条独立证据：
1. **p 不变量**（L1643 实测）：CROWDING×industry 的 sub 比在 p1.4/1.8/2.0 = 0.4356/0.4359/0.4354，全距 **0.0005** ⇒ 换 p 无效。
2. **decay 反向可达但连带打死另两闸**（本轮新算）：sub 比在 industry 分组下的斜率 ≈ **−0.00155/decay 单位**
   （FAST d20 0.5202 → d40 0.489）。要从 0.4356 升到 0.5196 需 +0.084 ⇒ decay −54 ⇒ **d26**。
   同点 S ≈ 1.63 − 0.0026×54 = **1.49 ❌**（斜率取自 FAST/subindustry d10 1.69→d80 1.87）、
   2Y ≈ 2.09 − 0.0047×54 = **1.84 ❌**（斜率取自 §31.1 CROWDING d40→d80 的 +0.10~0.12）。**两闸同时破。**
3. **分组轴已扫尽**：`sector` 分组 S 塌到 1.02（L1035）；`country×industry` 2Y 1.84 但 sub 比 **0.388**（`LL5ddzl1`）；
   `country×subindustry` 2Y 1.25（`Grgeez3J`）；`subindustry` sub 比 0.523 ✅ 但 2Y 只 1.73 ❌（`Vkd3wPLG`）。
   **没有任何分组能同时给 2Y ≥ 2.023 与 sub 比 ≥ 0.5196。**

**⇒ 剩下唯一的算子级杠杆是 `hump`，而线性外推说它也不行：**
需 sub **+19.3%**，预算 S **−3.1%**、F −20%、2Y −3.2%。N2 实测响应（`hump=0.01` @ FAST/d10/subindustry）：
Δsub比 **+0.237（+43%）** 换 ΔS **−19.4%**、Δreturns **−43%**、Δ2Y **−32%** ⇒ 耦合比 ≈ 2.2。
线性缩放 ⇒ +19% sub 比要付 **−8.6% S ⇒ S 1.49 ❌**；
且 **F ≥ 1.0 要求 returns ≥ 0.125×(1/S)² = 0.0503（S=1.58 时）**，而 −43% 把 0.0736 打到 **0.042 < 0.0503 ⇒ F 也破**。
⚠ 加重情节：`npA8wwz8` 的 TO 已是 **0.0399**（N2 是 0.0646），`hump=0.01` 会压掉**更大**比例 ⇒ 梯子必须细（0.002/0.005）。
**唯一活路是小阈值处的强凸性**（可信：最初几档削掉的是集中在小盘的纯噪声交易），先验 ~25%，是最后一个算子级 sub 杠杆。

### 37.4 ★★★★★★ 2023-regime 假设**确证**，机制定位到中性化而非字段

`get_alpha_yearly_stats(npA8wwz8)`：2014 **3.11**(F3.06/ret0.1207) · 2015 1.59 · 2016 0.39 · 2017 0.92 ·
2018 2.10 · 2019 0.79 · 2020 **−0.44**(pnl −223 756) · 2021 **3.67**(F4.53/ret0.1901) · 2022 **2.75**(ret0.1589) · **2023 1.23**(F0.79/ret0.0512)。
对照 `xA1dmlVb`（FAST/d40/subindustry/p1.8）：**2023 = 0.69**，2Y 1.71。

**⇒ CROWDING/d80/industry/p1.4 把 2023 单年 Sharpe 从 0.69 抬到 1.23（近翻倍），而这一年就是 2Y 1.71 与 2.09 的全部差额。**
**Task #19 的 2023-regime 假设成立，但机制被重定位：不是"换字段找到 2023 有效的信号"，而是"换中性化+decay 让同一个信号在 2023 有效"。**
Batch P 已独立否证了字段版本（见 37.5：5 个族全灭，最好 2Y 仅 0.60）。
⚠ 两个稳健性红旗：2020 为负（−0.44）、2016 弱（0.39）⇒ 提交前须按 `brain-alpha-robustness` 落 `robustness_npA8wwz8` 台账。

### 37.5 ★★★★★ Batch P 十腿全负：**`analyst_factor_signals` 内除 `*_estimate_change_3mo` 外全部机制族已实测判死**

Batch P（`1YjzoEGm` 的逐字配置：FAST/d20/TOP2500/D1/`industry` 分组/p1.8/`group_zscore`/`signed_power`），**只换字段**，10/10 complete：

| 腿 | alpha | 字段 | 族 | S | F | returns | sub(限) | 2Y | failed_ra | long/short |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P1 | `O0JxGzKb` | np_y2_consensus_value | 水平 | **−1.09** | −0.72 | −0.0543 | −0.55 | −0.42 | 3 | 770/2049 |
| P7 | `omogNGAl` | eps_y2_consensus_value | 水平 | **−0.98** | −0.62 | −0.0499 | −0.57(−0.51) | −0.24 | 4 | 786/2034 |
| P5 | `Vkd3Gzw5` | revenue_y1_estimate_skewness | 形状 | **−0.70** | −0.35 | −0.0306 | −0.27 | −0.90 | 3 | 1232/1587 |
| P8 | `3qjepP3P` | np_y1_consensus_value | 水平 | 0.43 | 0.18 | 0.0217 | 0.37 | 0.32 | 3 | 883/1936 |
| P10 | `j2er6GXW` | eps_y1_estimate_asymmetry | 形状 | 0.42 | 0.11 | 0.0084 | 0.28 | **0.60** | 3 | 1414/1406 |
| P3 | `E5VeGz00` | np_y1_estimate_asymmetry | 形状 | −0.38 | −0.09 | −0.0078 | −0.46(−0.20) | −0.32 | 4 | 1409/1410 |
| P4 | `E5VeGz0G` | eps_y1_estimate_skewness | 形状 | −0.28 | −0.09 | −0.0140 | −0.03 | −1.03 | 3 | 1250/1569 |
| P6 | `XgR8ozP5` | np_revision_magnitude | 修正幅度 | 0.28 | 0.10 | 0.0145 | −0.01(0.15) | 0.10 | 4 | 1580/1239 |
| P2 | `0mjMpgnG` | np_y1_estimate_skewness_alt | 形状 | −0.08 | −0.01 | −0.0040 | 0.14 | 0.05 | 3 | 1285/1534 |
| P9 | `MP0LGzXM` | np_y1_cagr_2yr_alt | 增长 | −0.02 | 0.00 | −0.0008 | −0.21(−0.01) | −0.24 | 4 | 1601/1218 |

**全批最大 |S| = 1.09（且为负）、最大 2Y = 0.60。** 按族收敛：
`*_consensus_value`（水平）|S| ≤ 1.09 · `*_estimate_skewness`/`_alt`（形状）|S| ≤ 0.70 ·
`*_estimate_asymmetry` |S| ≤ 0.42 · `*_revision_magnitude` 0.28 · `*_cagr_2yr_alt` 0.02。

**⇒ §31.5 的「增长陷阱 / 过度乐观异象」作为主信号被定量关闭**（它复现了 `mLYVxg32` 的 1.15，封顶 |S| ≈ 1.1 且 2Y < 1），
只能当条件变量用。**加上此前已死的 `coeff_var`（M6 S 0.80/F 0.33），`analyst_factor_signals` 的 12+ 机制族
除 `*_estimate_change_3mo` 外全部实测判死。**
⚠ 诊断副产物：`consensus_value` 三腿的多空严重失衡（770/2049、786/2034、883/1936）⇒ **水平族信号被空头倾斜主导**，
这与 §31.4 的 `coeff_var` 失衡（819–949 vs 1870–2001）同型，可作为「EUR 内水平/离散度族是稀释项」的第二重证据。

### 37.6 ★★★★★★ 平台 `how-pass-sub-universe-test` 全页裁定：**ATOM 内不存在平台认可的 sub 修法**

页 `how-pass-sub-universe-test`（lastModified 2026-08-26，sequence 58，category "Interpreting Results"）。逐字公式：
> *"subuniverse_sharpe >= 0.75 \* sqrt(subuniverse_size / alpha_universe_size) \* alpha_sharpe"*

⇒ **四重独立验证了我推导的系数**：0.75×sqrt(1200/2500) = **0.51961**，且 EUR TOP2500 的子宇宙 = **TOP1200**
（已在 `LL5ddzl1` 0.98/1.88、`xA1dmlVb` 0.956/1.84、`1YjzzKaR` 0.90/1.73、**`npA8wwz8` 0.85/1.63** 上核对；
最后一条是在**不同中性化与不同 decay** 下核对的 ⇒ **系数与设置档无关**）。
非 TOPXXX 宇宙的比率不同：ASI MINVOL1M 0.295、USA ILLIQUID_MINVOL1M 0.41、EUR ILLIQUID_MINVOL1M 0.355。

**★ sub-Sharpe 的计算程序（本轮新取到的细节）**：
> *"Pasteurize to the target universe, that is, for all stocks not in the sub-universe, assign value of NaN"*
> → *"Apply market neutralization to resulting set (subtract mean of all values from each value) and then scale Alpha back to original size"*
> → *"Calculate PnL using resulting Alpha values"*；且明说 *"similar to the Sharpe of an alpha simulated in the sub-universe, but **not exactly the same**"*。

官方算例：USA TOP3000 alpha S 2.73 ⇒ cutoff `0.75*sqrt(1000/3000)*2.73 = 1.18`，在 TOP1000 上实跑得 1.17 ⇒ **差 0.01 失败**。

**五条 tip 逐条裁定：**

| # | 原文要点 | 对 ATOM 的可用性 |
|---|---|---|
| ① | 避免规模乘数（`rank(-assets)`、`1-rank(cap)`） | **N/A**——本档一条都没用 |
| ② | *"Try decaying separately the liquid and non-liquid parts… `ts_decay_linear(signal,5)*rank(volume*close) + ts_decay_linear(signal,10)*(1-rank(volume*close))`"* | **❌ ATOM 非法**——`volume`/`close` 是 **pv1** 字段，不在 6 个豁免分组字段里；同时违反 `add A,B` 禁混信号 |
| ③ | 逐步复核 | 仅诊断，不改指标 |
| ④ | 提高整体 Sharpe | **❌ 数学上无效**——限是 `0.5196·S`，抬 S 同比例抬限 |
| ⑤ | *"Some signals are just not robust… Most likely, you just dodged a bad alpha."* | 认输条款 |

**⇒ 结论（本档最重要的一条负面结论之一）：ATOM 之内没有任何平台认可的 sub-universe 修法。**
可用的只有分组、中性化、decay 与阈值型算子，而 37.3 已把前三者扫尽、把 `hump` 的线性外推算死。

### 37.7 ★★★★★ 「Sharpe 高出 10%」豁免条款**不可事前验证**——这本身就是答案

`consultant-submission-tests` 逐字：*"**Prod-correlation**: Same as the Self-correlation criteria but applied to all submitted alphas in BRAIN"*，
而 self 条款是 *"Less than 0.7 PNL series correlation with user's alphas, **or a sharpe at least 10% greater than other correlated alphas submitted by user**"*。
⇒ `1YjzoEGm`（S 1.73）对任何 S ≤ **1.573** 的在位者即可豁免；`xA1dmlVb`（S 1.84）对 S ≤ 1.673。

**但无法验证**：`get_record_sets(npA8wwz8)` 返回 `count 5` = **pnl / sharpe / turnover / daily-pnl / yearly-stats，没有任何 correlation record set**
⇒ 撞墙在位者的身份与 Sharpe 经 API 不可达；且 `PROD_CORRELATION` 位于 `checks.pending`，**只在提交时求值**。
**⇒ 该条款只能靠真的提交来行使，而提交是不可逆动作、需用户明确确认、是任何 waiver 都无效的红线。**
**处置：作为决策上报用户，不作为实验执行。**

### 37.8 ★★★★★★ 平台文档给出的三条官方建议**全部指向离开 SUBINDUSTRY**——本战役的设置档盲区又深一层

页 `neut-cons`（"Neutralization 🥉"，lastModified 2026-09-18，category "Advanced Topics"）逐字：

1. **类别推荐表**：*"**Analysts Datasets** | | | ✔️ | | Analyst datasets provide an estimate of future fundamental data, hence an **industry neutralization is recommended** here as well"*
   ⇒ **平台对 Analyst 数据集的官方推荐是 `INDUSTRY` 中性化**，本战役从未测过（区域默认 SUBINDUSTRY，赢家全用 FAST/CROWDING 这类**风格**中性化）。
2. **区域 tip**：*"Use **'country'** and 'exchange' neutralization options for **EUR**, ASI regions"*
   ⇒ COUNTRY 是平台对 EUR 的明文推荐。⚠ 同一条 tip 点名 `exchange`，但 `get_platform_setting_options` 返回的 EUR/D1 十二档里
   **没有 EXCHANGE**（NONE/REVERSION_AND_MOMENTUM/STATISTICAL/CROWDING/FAST/SLOW/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/COUNTRY/SLOW_AND_FAST）
   ⇒ **文档与平台实时选项不一致，登记为待报差异。**
3. **宇宙 tip**：*"Try **larger** stock groups for more **liquid universes** that have less number of stocks… Try smaller stock groups for illiquid universes"*
   ⇒ TOP2500 是大流动性宇宙 ⇒ 官方方向是**更粗的组（SECTOR/MARKET/COUNTRY）**，而区域默认恰是**最细的 SUBINDUSTRY**。
   **这独立解释了 37.1 里 SUBINDUSTRY 的 2Y 只有 1.60。**

**★ 这与 §30.6 的教训同型、但高一层**：§30.6 说「S 上限 0.9」是**设置档的上限被误记成信号的上限**；
本条说**区域控制面板本身选的设置档就与平台三条官方建议相反**，而档案从未把这三条纳入搜索空间。
⇒ **可复用铁律：开新区域/新数据集前，先取平台文档的「类别 × 推荐中性化」表与区域 tip，再定 settings.json 的默认档。**

**同页确证 S1/S4 的简并预测**：*"'Neutralization in Simulation Settings' and `group_neutralize(x, group)` **use the same operation**"*、
*"Are they interchangeable? **Yes**"*（算例 `-zscore(ebit/capex)`+INDUSTRY ≡ `group_neutralize(-zscore(ebit/capex),industry)`+NONE）。
因 `group_zscore(x, industry)` 已零化 industry 均值 ⇒ **INDUSTRY 中性化在其上近似幂等**；
又因中性化是 *"the last step in the operations"*（decay/truncation 之后）⇒
**S1(NONE) 与 S4(INDUSTRY) 构成一对匹配对照，只隔离「decay+truncation 之后是否重新零化 industry 均值」这一步。**
且 *"Always pick a value for neutralization; only leave it as None if neutralization is manually incorporated in the Alpha"*
⇒ **预测 S1(NONE) 表现差**（我的 alpha 并未手工内含中性化，`group_zscore` 是 z 分数不是 neutralize）——这是一条可证伪预测。

### 37.9 ★★★★★★ 页 `neut-users`（"Double Neutralization"）：**平台对 EUR 的官方推荐形式，本战役从未测过**，并解释了 Batch M 的失败机制

逐字：
> *"You can apply simultaneous neutralizations by two different groups, such as **country and industry** with the help of
> `group_cartesian_product`, **in regions with many countries like EUR**, ASI, and GLB."*
> *"If you use two `group_neutralize` operators **sequentially**, such as
> **`group_neutralize(group_neutralize(Alpha, industry), country)`**, **the second neutralization partially negates the first one**.
> The double neutralization approach differs from using two group_neutralize operators."*

官方 ASI 算例的三行形式（settings 配 **Neutralization = Sector**）：
```
alpha = ts_rank(eps, 252)
group = densify(group_cartesian_product(industry, country))
group_neutralize(alpha, group)
```
Tips：*"Using basic grouping fields in 'double neutralization' for the multi-country region **can improve an Alpha's simulated performance**."*

**★★ 这解释了 Batch M 的 M7/M8/M9**：它们是 `group_neutralize(...)` 的**顺序嵌套** wrapper，2Y 卡在 1.61–1.62——
**那不是运气差，是文档级的失败模式（第二次 neutralize 部分抵消第一次）。**

**与 Batch M 实跑形式的三处差异（每一处都可能是关键）**：① 官方用 **`densify()`**；
② cartesian 组作为 **`group_neutralize` 的目标**（M 批是把它当 `group_zscore` 的**分组参**）；③ settings 配 **SECTOR**。

`operator_audit(region=EUR, universe=TOP2500, delay=1)` 对 5 条候选返回 **`safe: true` / `violations: []`**
⇒ **`densify`、`group_cartesian_product`、`group_neutralize` 在 EUR/TOP2500/D1 全部 live**。
⚠ 但 `densify` 的**元数只有文档级证据（1 参）**、未经本仓实测 ⇒ 按 §35.2 铁律 3 **单独成批**，连坐只损失该批。

**同次 audit 还给出 18 个幽灵算子（catalog 有、平台无），是一份高价值负面清单**：
`group_median` `group_normalize` `group_percentage` `group_vector_proj` `neutralize`(裸名) `s_log_1p` `sigmoid` `tanh`
`ts_co_kurtosis` `ts_decay_exp_window` `ts_delta_limit` `ts_entropy` `ts_median` `ts_min_max_cps` `ts_min_max_diff`
`ts_partial_corr` `ts_percentage` `ts_skewness`。
⇒ **「穷举算子组合」时必须先排除这 18 个**；其中 `ts_skewness`/`ts_entropy`/`ts_percentage`/`group_normalize`
正是最容易顺手拿来用的那几个，写进表达式会整批 ERROR 并连坐 CANCELLED（记忆 `brain-error-cancelled.md`）。

### 37.10 ★★★★★ `batch_create_simulations` 首次实测：**一次调用 = 8 条各自独立设置**，彻底改变设置扫描的成本结构

§31.6 登记过「设置扫描的批量工具是 `batch_create_simulations`（每条自带 settings）」，本轮**首次实跑验证**：
8 items / `submitted: 8` / `total: 8` / **全部 `ok: true`**、`async: true`，**一次 MCP 调用完成**。
对照：`create_simulation`（单条）在 §31.6 实测有约 50% 概率返回 `MCP error -32603`（且"可能已建、也可能没建"，必须逐条回验），
8 条要 8 次调用 + 8 次回验；`create_multi_simulation` 整批共享一套设置，**结构上做不了设置对比波**。

**⚠ schema 陷阱（照抄默认值会静默换档）**：`nan_handling` 与 `max_trade` 的**默认值是 `"OFF"`**，
`base_neutralization` 默认 **`STATISTICAL`**、`base_decay` 默认 **4** ⇒ **必须逐条显式传 `"ON"` 与目标中性化/decay**。
支持的 item 级键：`region / universe / delay / decay / neutralization / truncation`（平台 camelCase 亦接受）；
固定段：`language / unit_handling / nan_handling / pasteurization / max_trade`。**无 `visualization` / `test_period` / `validate_fields` 键。**
⇒ **可复用规则：任何"同表达式 × N 套设置"的扫描（中性化、decay、universe、p）一律用 `batch_create_simulations`，不再逐条 `create_simulation`。**

### 37.11 ★★★★★ 收割通道故障与替代路径（登记，勿再踩）

本轮 `harvest_multisim_alphas` 与 `lookINTO_SimError_message` 对 multisim 父项**双双返回空体**：
`"Expecting value: line 1 column 1 (char 0)"`（`raw: null`）；传裸 id 而非完整 URL ⇒ **HTTP 404**。
按 §31.6 的会话过期假设调 `authenticate`（`status_code 201` / `has_jwt true`）**并未修复**。
随后 `get_record_sets(1YjzoEGm)` 报**同样**的空体错、而 `get_record_sets(npA8wwz8)` 正常返回 5 个 record set
⇒ **故障是按资源发生的（疑似某些端点返回空体/204），不是全局会话失效。**

**✅ 已验证的替代收割路径**：`get_user_alphas(stage="IS", region="EUR", limit=20, order="-dateCreated")`
返回 **`from_cache: false`** 且带完整 `metrics` / `checks` / `ra` 块 —— Batch P 的 10 腿与 Batch Q/R 的 12 腿全部由此收回。
⚠ 返回的 `count: 22` 带 `partial_count: true`、`server_scanned: 100`、`server_count: 10000`、`max_scan: 1000`
⇒ **`count` 字段不是可靠总数**，别用它判断"是否全部收回"，要按 tag/表达式逐条点名核对。

### 37.12 ★★★★★★ 三处旧结论被推翻（读到旧行时按本节）

| 旧位置 | 旧结论 | 现状 |
|---|---|---|
| **L987** | 「CROWDING/TOP2500/decay40 subindustry×p×window 全扫 ⇒ **S 天花板 ≈ 1.50**」 | **推翻**：`npA8wwz8`（CROWDING/**decay 80**/**industry**/p1.4）S **1.63**。旧扫固定了 decay 40 与 subindustry 两个维度 ⇒ 又是 §30.6 的「设置档天花板」形态 |
| **L2173** | 「§31.3 CROWDING prod 0.6257 但 S 1.49 < 1.58 = **尚未化解的张力**」 | **已化解**：同中性化下换 decay 80 + industry 分组 ⇒ S 1.63 ≥ 1.58，且 prod 保持 0.6257、2Y 升到 2.09。张力解除，只剩 sub 一闸（37.3 判为机制性不可修） |
| **L1071** | 「28.3 证明 `analyst_factor_signals` 这一族**只能出 1 颗**，缺口 6 颗必须靠开新机制腿」 | **推翻**：§32.2 的 4-元组 `["xA1dmlVb","WjLVWY3Z","kqJZLV2k","e76xq9op"]` 两两 < 0.7 且 `max_subset_exact: true` ⇒ **同族可出 4 颗**。旧结论的根因是抽样偏差（那 5 颗全是同一字段的设置变体），与 §32.2 已记的方法论教训同源 |

### 37.13 ★★★★★★★ 本战役当前的诚实结论（上报口径）

**四闸联立（S ≥ 1.58 ∧ F ≥ 1.0 ∧ 2Y ≥ 2.023 ∧ sub/S ≥ 0.5196 ∧ prod < 0.7 ∧ self < 0.7）在已测网格内无解。**
每个实测角都恰好败在一到两闸上：

| 角 | 败在 |
|---|---|
| FAST × subindustry（d10/d20/d40） | S ✅ sub ✅ prod ✅ 但 **2Y 封顶 1.75** |
| FAST × industry（d20） | S ✅ 2Y ✅ sub ✅(+0.08%) 但 **prod 0.7398** |
| CROWDING × industry（d80/p1.4） | S ✅ 2Y ✅ prod ✅ self ✅ 但 **sub 比 0.4356**（机制性不可修，37.3） |
| CROWDING × subindustry（d40/d80） | sub 比 ✅ prod ✅ 但 **S 封顶 1.53、2Y 封顶 1.75** |
| SUBINDUSTRY × industry（d20） | sub 比 ✅(+6.8%) F ✅ 但 **S 1.46、2Y 1.60、prod 0.7649** |
| SLOW × industry（d20） | **全灭**（S 0.68） |

**且互相关上限（§32.2 的最大团 = 4）意味着「同族出 10 颗两两 < 0.7」从未被论证过。**
⇒ **目标是 10 颗，当前实测可达上限是 1 颗**，且这 1 颗（`npA8wwz8` 或 `1YjzoEGm`）各差一闸、
两闸都无已验证修法（sub 无平台认可修法；prod 的「高 10% Sharpe」豁免不可事前验证，37.7）。

**尚未扫尽、仍有机制理由的轴（按先验排序）：**
1. **COUNTRY / SECTOR 中性化**（Batch S 在飞）——平台对 EUR 的明文推荐，且**比 industry 粗 ⇒ 保留 subindustry 分量 ⇒ 2Y 应保持高位**；
   COUNTRY 是唯一有可能像 CROWDING 那样大幅压 prod 的档（EUR 是多国宇宙，国家倾斜是 alpha 之间共享的大头）。
2. **双中性化官方形式**（Batch T 待开，37.9）——`densify(group_cartesian_product(industry, country))` + `group_neutralize` + settings SECTOR。
3. **宇宙档**（TOP2500 → TOPCS1600 / TOP1200）——**完全未测**。换宇宙同时改变 sub 系数与信号本身
   （TOP1200 ⇒ 子宇宙 TOP800 ⇒ 比率 0.75×sqrt(800/1200) = **0.6124**，比率更严但持仓全是大盘）。
   ⚠ 强负面先验：区域档案记「换档否证：TOP2500 2.19 → TOP1200 0.33 → TOP400 0.50」，
   **但那是"慢 MODEL 残差 × 快 PV"机制、且测于 CROWDING 被引入之前** ⇒ 对本族不构成判死，只构成低先验。
4. **`hump` 细梯（0.002/0.005/0.01/0.02）on `npA8wwz8` 逐字表达式** —— 最后一个算子级 sub 杠杆，先验 ~25%（37.3）。
5. **`trade_when` 时序轴** —— 唯一未测轴；但 `hump` 的实测响应（S 1.33 / F 0.78）预测它同样败在 S 与 F，
   且 §36.3 已警告本池的死法正是 returns 不足 ⇒ **入批前必须先算 F 闸天花板**，且**只开 5 腿不开 10 腿**。

**⇒ 两个必须由用户裁决的事项（不上报就是失职）：**
- **(a)** `1YjzoEGm` 六闸过五，只差 prod（0.7398 vs 0.7），而平台条款允许「Sharpe 高出在位者 10%」豁免
  （它对任何 S ≤ 1.573 的在位者成立）。**但这只能靠真的提交来行使，不可事前验证，且提交不可逆。**
- **(b)** 目标 10 颗 vs 实测上限 1 颗的落差，以及**塔位冲突**：10 颗全 Analyst 的 ATOM 会在再提交 2 颗后点亮
  `EUR/D1/ANALYST`（现 1 颗；用户口径「点亮 = ≥3 颗」），届时锁定项「已点亮塔不作主数据集」生效；
  EUR/D1 跨类别的总余量是 9 颗。⚠ 目标原文是「产出 10 个**通过验证**的」而非「已提交」，这可能是部分化解，但需用户确认口径。

---

## §38 Batch S 收割：中性化九档全图完成 + ATOM 身份由表达式自动决定（2026-10-20）

> 本节是 §37 的直接续篇。Batch S（`batch_create_simulations` 一次派 8 条，8/8 `ok:true`）已全部 COMPLETE，
> 经 §37.11 的替代通道 `get_user_alphas(stage="IS", region="EUR", limit=20, order="-dateCreated")` 收割，
> `from_cache: false` 已核。**结果同时产生了本战役最大的一次结构简化，和一次对我自己当场准备写下的定律的否证。**

### 38.1 ★★★★★★ Batch S 八腿全表（EUR/TOP2500/D1/decay20/trunc0.08/`industry` 分组/p1.8，只变中性化与字段）

| 腿 | alpha | 中性化 | 字段 | S | F | TO | **returns** | sub | **sub/S** | **2Y** | RN-S | failed_ra | long/short |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **S5_COUNTRY** | **`XgR8bjw8`** | COUNTRY | np_y2 | 1.59 | 1.62 | 0.0432 | 0.1293 | 0.90 | 0.5660 | **1.91** | 0.80 | **0** | 1487/1055 |
| S4_INDUSTRY | `vROvkZNQ` | INDUSTRY | np_y2 | 1.58 | 1.50 | 0.0420 | 0.1128 | 0.89 | 0.5633 | 1.88 | 0.76 | **0** | 1408/1135 |
| S3_SECTOR | `e76x9NMd` | SECTOR | np_y2 | 1.60 | 1.65 | 0.0430 | 0.1330 | 0.92 | 0.5750 | 1.87 | 0.78 | **0** | 1512/1031 |
| S2_MARKET | `xA1dYloN` | MARKET | np_y2 | 1.59 | **1.69** | 0.0424 | 0.1411 | **0.94** | 0.5912 | 1.85 | 0.80 | **0** | 1635/908 |
| S1_NONE | `QPY93WwX` | NONE | np_y2 | 1.58 | 1.68 | 0.0437 | **0.1417** | **0.94** | **0.5949** | 1.82 | 0.79 | **0** | 1511/1032 |
| S8_COUNTRY_np_y1 | `Vkd36zY5` | COUNTRY | np_y1 | **1.62** | 1.64 | 0.0429 | 0.1277 | 0.89 | 0.5494 | 1.53 | 0.81 | 1（LOW_2Y） | 1647/896 |
| S7_SECTOR_eps | `kqJZVWZO` | SECTOR | eps_y2 | 1.37 | 1.34 | 0.0424 | 0.1193 | 0.82 | 0.5985 | 1.55 | 0.54 | 2 | 1657/899 |
| S6_COUNTRY_eps | `zqrRY2mG` | COUNTRY | eps_y2 | 1.40 | 1.36 | 0.0424 | 0.1188 | 0.85 | 0.6071 | 1.53 | 0.56 | 2 | 1647/910 |

**五条腿 `failed_ra_count = 0`**（S1–S5），即 18 项具名 RA check 全过——含 `LOW_SHARPE`（S ≥ 1.58）、
`LOW_FITNESS`、`LOW_SUB_UNIVERSE_SHARPE`、`LOW_2Y_SHARPE`（≥1.58）。`checks.fail = []`，
违规项全在 `warning`（§31.2 的读数纪律再次生效）。**这是本战役第一次出现「一批里过半腿零失败」。**

### 38.2 ★★★★★ 中性化九档全图（同一表达式 `signed_power(group_zscore(netprofit_y2_estimate_change_3mo, industry), 1.8)`，decay 20）

| 中性化 | S | F | returns | sub | **sub/S** | **2Y** | failed_ra | **prod** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **FAST** | **1.73** | 1.54 | 0.0780 | 0.90 | 0.5202 | **2.09** ✓ | 0 | 0.7398 ✗ |
| COUNTRY | 1.59 | 1.62 | 0.1293 | 0.90 | 0.5660 | 1.91 ✗ | **0** | **0.81** ✗（本批实测） |
| INDUSTRY | 1.58 | 1.50 | 0.1128 | 0.89 | 0.5633 | 1.88 ✗ | **0** | 未测 |
| SECTOR | 1.60 | 1.65 | 0.1330 | 0.92 | 0.5750 | 1.87 ✗ | **0** | 未测 |
| MARKET | 1.59 | **1.69** | 0.1411 | **0.94** | 0.5912 | 1.85 ✗ | **0** | 未测 |
| NONE | 1.58 | 1.68 | **0.1417** | **0.94** | **0.5949** | 1.82 ✗ | **0** | 未测 |
| SUBINDUSTRY | 1.46 | 1.27 | 0.0949 | 0.81 | 0.5548 | 1.60 ✗ | 1 | 0.7649 ✗ |
| CROWDING（d80/p1.4） | 1.63 | 1.25 | 0.0736 | 0.71 | **0.4356** ✗ | **2.09** ✓ | 1 | **0.6257** ✓ |
| SLOW | 0.68 | 0.33 | 0.0303 | 0.24 | 0.353 ✗ | 1.10 ✗ | 4 | 未测 |

**12 档中的 9 档现已在同一表达式、同一 decay 下测齐**（余 REVERSION_AND_MOMENTUM / STATISTICAL / SLOW_AND_FAST
在 `subindustry` 分组下测过：S 1.21 / 比率 0.347 / S 0.82，均判死）。

**三条可证伪预测的裁决：**

| 预测（Task #21 原文） | 裁决 | 证据 |
|---|---|---|
| 「S1_NONE 应差」（doc：*"only leave it as None if neutralization is manually incorporated"*） | **✗ 否证** | NONE 给出 F **1.68**、returns **0.1417**（全批最高）、`failed_ra 0`。⇒ 那句是**建议不是惩罚**；而 `group_zscore(x, industry)` **正是**"手动内置了中性化"，所以 NONE 在这里是**合规写法**而非漏配 |
| 「S4_INDUSTRY ≈ S1」（`group_zscore(x,industry)` 已零化 industry 均值 ⇒ 幂等） | **✓ 确认，几乎逐字** | S 1.58 = 1.58；2Y 1.88 vs 1.82；比率 0.5633 vs 0.5949。差异只出现在 F（1.50 vs 1.68）与 returns（0.1128 vs 0.1417）⇒ **decay+truncation 之后重新零化 industry 均值会改变持仓分布，但不改变信号方向**。§37.8 的幂等推断成立 |
| 「SECTOR/COUNTRY 因比 industry 粗 ⇒ 保留 subindustry 分量 ⇒ 2Y 应保持高位」 | **✓ 确认（2Y），但被 prod 否掉** | 2Y：COUNTRY **1.91** > INDUSTRY 1.88 > SECTOR 1.87 > MARKET 1.85 > NONE 1.82，全部 ≫ SUBINDUSTRY 1.60、SLOW 1.10。但 COUNTRY 的 prod = **0.81**，是全战役最差 |

**★★★★ 新发现的独立事实：returns 在粗中性化下几乎翻倍（0.0780 FAST → 0.1417 NONE，+82%）。**
这直接解掉了 §34.2 / §36.3 反复警告的本池死法（returns 不足 ⇒ F 封顶）：
F = S×sqrt(returns/0.125)，NONE 下 returns 0.1417 > 0.125 ⇒ **F 闸不再是约束**（F 1.68 实测）。
⇒ **「粗中性化 = 高 returns = F 无忧，但 prod 爆表；细中性化（FAST/CROWDING）= 低 returns = F 吃紧，但 prod 可控」**，
这是本族最底层的一条权衡，此前从未被这样表述过。

### 38.3 ★★★★★★ 我当场准备写下「prod ↔ sub/S 反相关」定律，被自己的库存数据否证——修正后的冲突只剩一条轴

COUNTRY 的 prod = 0.81 之后，`industry` 分组下四档呈完美单调：

| 中性化（`industry` 分组） | prod | sub/S |
|---|---:|---:|
| CROWDING | 0.6257 | 0.4356 |
| FAST | 0.7398 | 0.5202 |
| SUBINDUSTRY | 0.7649 | 0.5548 |
| COUNTRY | **0.81** | 0.5660 |

**prod 越低 sub/S 越低，单调，斜率 ≈ 0.7。** 我据此准备写下「prod 与 sub/S 结构性反相关，故两闸不可同时满足」。

**⚠ 这条定律是错的，被 `subindustry` 分组的库存数据当场否证：**

| 中性化（`subindustry` 分组） | prod | sub/S | 2Y |
|---|---:|---:|---:|
| FAST d10 `KPmE8klx` | **0.6653** ✓ | **0.5503** ✓ | 1.61 |
| FAST d20 `Grge67NZ` | **0.6812** ✓ | **0.5640** ✓ | 1.72 |
| FAST d40 `xA1dQVVm` | **0.6933** ✓ | **0.5531** ✓ | 1.75 |
| CROWDING d80 `Vkd3wPLG` | 0.6257 ✓ | 0.523 ✓ | 1.73 |

**在 `subindustry` 分组下，prod 与 sub/S 同时满足，毫不冲突。**

⇒ **正确表述（取代上面那条）**：prod 与 sub/S **只在「固定分组、沿中性化轴」上反相关**；
**沿分组轴它们同向**——`subindustry` 分组在 prod（0.665–0.693 vs 0.740–0.81）与 sub/S（0.550–0.564 vs 0.436–0.566）
**两项上都优于** `industry` 分组。**`industry` 分组唯一的、也是不可替代的好处是 2Y。**

**★★★ 于是整个战役塌缩成一条冲突轴：**

> **2Y ≥ 2.023 需要粗分组（`industry`）；prod < 0.7 与 sub/S ≥ 0.5196 需要细分组（`subindustry`）。**
> 其余四闸（S / F / TO / CONCENTRATED_WEIGHT）在两种分组下都已实测可过。
> **§37.1 说的「四闸合取无解」应更正为「一条轴上的两难」**——这是更强的结论，也更好用。

⚠ 方法论教训（本战役第二次）：**「两个指标反相关」这类定律，必须在**每个**固定其它轴的切片上分别验证后才能写。**
只在 `industry` 切片上看到的单调性，被 `subindustry` 切片直接推翻。与 §37.2 那次（「非 FAST ⇒ 低 prod」被
SUBINDUSTRY 的 0.7649 推翻）是同一形状的错误：**用单一切片的单调性冒充跨切片的定律。**

### 38.4 ★★★★★★ 单变量归因：`industry` 分组换来的 +0.37 2Y，83% 来自 2022 单年，代价是 2019 −1.04

同表达式、同 FAST、同 d20、同 TOP2500/D1/p1.8，**只有分组不同**（本战役最干净的单变量对之一）：

| 年 | `1YjzoEGm`（**industry**） | `Grge67NZ`（**subindustry**） | Δ |
|---|---:|---:|---:|
| 2014 | 3.40 | 2.47 | +0.93 |
| 2015 | 1.90 | 1.97 | −0.07 |
| 2016 | 0.01 | −0.11 | +0.12 |
| 2017 | 1.47 | 1.74 | −0.27 |
| 2018 | 2.40 | 2.26 | +0.14 |
| **2019** | **1.33** | **2.37** | **−1.04** |
| 2020 | −0.29 | 0.32 | −0.61 |
| 2021 | 3.64 | 3.36 | +0.28 |
| **2022** | **2.88** | **2.28** | **+0.60** |
| **2023** | **1.22** | **1.10** | **+0.12** |

**2Y 窗口 = 2022+2023**：industry (2.88, 1.22) → 报 2Y **2.09**；subindustry (2.28, 1.10) → 报 2Y **1.72**。
窗口内合计 Δ = +0.72，其中 **2022 贡献 +0.60 = 83%**。

**⇒ `industry` 分组不是「结构性更优」，是一次跨年再分配**：赢在 2014（+0.93）与 2022（+0.60），
输在 2019（−1.04）、2020（−0.61）、2017（−0.27）。**若 2022 表现得像 2019，`1YjzoEGm` 的 2Y 会掉到 ~1.8，同样过不了 ATOM 线。**

**★★★ 三颗候选用同一种方式过 2.023，说明这不是分组伪影而是年度 regime：**

| alpha | 中性化 | 分组 | 2022 | 2023 | 2Y |
|---|---|---|---:|---:|---:|
| `1YjzoEGm` | FAST | industry | 2.88 | 1.22 | **2.09** |
| `npA8wwz8` | CROWDING | industry | 2.75 | 1.23 | **2.09** |
| `WjLVWY3Z` | FAST | industry | — | — | 2.06 |

**两颗在完全不同的中性化与 decay 下，2022/2023 读数几乎逐字相同（2.88/1.22 vs 2.75/1.23）。**
⇒ **2022 是 EUR 分析师修正信号的一个异常强年**（利率冲击 + 能源危机 ⇒ 盈利修正幅度大且持续），
而 **ATOM 的 2Y 窗口恰好把它含进来**。2023 单年只有 1.22–1.23。

**⚠ 这是一条一阶过拟合警报，也是本战役最重要的稳健性发现：**
**ATOM 的 2Y ≥ 2.023 是被 2022 单年抬过去的，不是信号强度抬过去的。**
对 OS（2024+）更合理的期望值是 **2023 的 1.22**，而不是 2Y 的 2.09。
⇒ 任何"过闸即可提交"的推理在这里都会高估 OS 表现约 0.87 个 Sharpe。
**必须走 `brain-alpha-robustness` 并把这条写进台账 `robustness_<alpha_id>`。**

### 38.5 ★★★★★★★ 平台原文确证：ATOM 身份是**表达式属性**，不可选择、无退出通道（§36.2 的待核项已核）

§36.2 留下一个未核项：「⚠ 本条尚需一次实证核验……看 cutoff 到底是 2.023 还是别的数」。
本轮重读 `single-dataset-alphas`（lastModified 2026-09-18T01:09:15，sequence 150，category **Creating Alphas**，duration PT2M）
拿到了**比 cutoff 数值更根本的答案**。逐字：

> "Single Dataset Alphas\* **use data fields from only one dataset to build the entire Alpha expression**,
> excluding 6 permitted grouping fields that can be a part of the expression –
> country, exchange, market, sector, industry and subindustry."
>
> "**All Alpha simulations with properties of Single Dataset Alphas** shall display the message
> '2 year Sharpe of \<value\> is below cutoff of \<limit\>' or '2 year Sharpe of \<value\> is above cutoff of \<limit\>.'
> in the IS Testing Status tab of Alpha simulation results **instead of** the IS Ladder Sharpe Pass/Fail criteria."

**⇒ 判据是「with properties of」= 平台按表达式自动推断，不是提交者勾选的类别。**
本战役全部候选都只用 `analyst_factor_signals` 的字段 + 豁免的 `industry`/`subindustry`/`country` 分组字段
⇒ **它们在定义上全部是 Single Dataset Alphas，2.023 这条线对全部候选生效，且没有退出通道。**

**这关闭了我在 38.4 之前认真考虑过的另一种读法**：「若平台没把它们当 ATOM，则只有 `LOW_2Y_SHARPE 1.58`
与 IS Ladder 生效，那 `xA1dQVVm`（2Y 1.75 / failed_ra 0 / prod 0.6933 / S 1.79 / F 1.45 / 比率 0.5531）
就已经是一颗全闸通过的 alpha」。**该读法被平台原文否证：不存在"不当 ATOM"的选项。**

**旁证（API 面）**：Batch S 全部八腿的 `checks.pending` 均为
`[SELF_CORRELATION, DATA_DIVERSITY, PROD_CORRELATION, REGULAR_SUBMISSION, POWER_POOL_CORRELATION, MATCHES_THEMES]`
—— **`IS_LADDER_SHARPE` 不在其中任何一列**（fail/warning/pass/pending 都没有）。
`get_record_sets` 也只给 5 个记录集（pnl / sharpe / turnover / daily-pnl / yearly-stats），**没有 IS Testing Status 记录集**
⇒ **cutoff 那句话在 API 上不可读**，与 §37.7 的「在位者身份不可读」同一形状：**平台把它只放在 UI 里。**

### 38.6 ★★★★★★★ ATOM 的「放宽」对本族是**陷阱**，不是优惠——它丢掉的正是救命的那一年

平台把 ATOM 说成 *"slightly relaxed submission criteria"*。但在 EUR/D1 对本信号族，**它实际上更严**，机制可以精确写出来：

| | 常规（非 ATOM）IS Ladder | ATOM |
|---|---|---|
| 判据 | 从 N=2 年起逐年升级，只要某年 Sharpe > PASS[N]×0.85 即 PASS；跌破 FAIL 1.59 才 FAIL | **只看最后 2 年**，一刀切 ≥ 2.38×0.85 = **2.023** |
| 用到的年份 | 2Y、3Y、…、10Y、全史 | **只有 2022+2023** |
| 对 `Grge67NZ` 的裁决 | 全史 1.72 ≥ 1.59 ✓ → N=2：2Y 1.72，> PASS[2]×0.85=2.023？否；> FAIL 1.59？是 ⇒ **N=3**：3Y 含 **2021 = 3.36** ⇒ ≈2.2 > 2.023 ⇒ **PASS** | 2Y 1.72 < 2.023 ⇒ **FAIL** |

**⇒ 同一颗 alpha，走常规通道 PASS，走 ATOM 通道 FAIL。差别完全来自 2021（S 3.36–3.64）落在窗口外。**

**可复用定律**：**ATOM 的 2Y 单窗口会丢弃窗口外的强年。任何「强度集中在某一两年」的信号，
在 ATOM 通道下都比常规通道更难提交——尽管平台文档称之为"放宽"。**
选 ATOM 候选时必须先看**逐年**分布：若强年不在最近 2 年内，ATOM 线几乎不可能过。
**⇒ 这反过来给出了一条新的选集判据（见 38.9）：ATOM 挖掘应优先选「2022–2023 强」的信号，而不是「全史强」的信号。**

### 38.7 ★★★★★★ 结构定理（最终版）：2Y 被分组粒度**量化**，交集为空

把所有实测按分组归并，每格取该分组下的最优值：

| 分组 | 最好 2Y | 最好 sub/S | 最好 prod | 裁决 |
|---|---:|---:|---:|---|
| `subindustry` | **1.75** ✗（差 0.273） | 0.5640 ✓ | **0.6653** ✓ | **只差 2Y** |
| `country×subindustry` | 1.25 ✗ | — | — | 死 |
| `country×industry` | 1.84 ✗ | 0.388 ✗ | — | 双死 |
| `industry` | **2.09** ✓ | 0.5660 ✓（COUNTRY 中性化） | **0.6257**（**仅 CROWDING**） | **prod < 0.7 只有 CROWDING 能做到，而 CROWDING 把 sub/S 钉死在 0.4356** ✗ |
| `sector` | S 崩到 1.02 ✗ | — | — | 死 |

**两条硬事实封死交集：**

1. **2Y 是分组粒度的阶跃函数，不是连续可调的量。**
   `subindustry` 侧的天花板是 **1.75**，且这个数在 **3 种中性化（FAST / CROWDING）× 4 个 decay（10/20/40/80）× 4 个 p（1.4/1.6/1.8/2.0）**
   下反复出现（FAST：1.61/1.72/**1.75**/1.71/1.70/1.72；CROWDING：1.52–**1.75**）⇒ **是硬天花板，不是调参缺口。**
   2.023 比它高 **+15.6%**。`industry` 侧则是 2.06–2.09 的紧簇。**中间没有可用的档**（`country×industry` 1.84 且比率 0.388 双死）。
2. **在 `industry` 分组下，prod < 0.7 只被 CROWDING 实现过**（0.6257；FAST 0.7398、SUBINDUSTRY 0.7649、COUNTRY 0.81），
   而 **CROWDING × industry 的 sub/S = 0.4356 是 p-不变的**（p1.4/1.8/2.0 = 0.4356/0.4359/0.4354，极差 0.0005，§37.3）。
   ⇒ 该格永远够不到 0.5196。

**⇒ 定理：在 EUR/D1 × TOP2500 × `analyst_factor_signals` 的实测网格上，
{prod < 0.7} ∩ {sub/S ≥ 0.5196} ∩ {2Y ≥ 2.023} ∩ {S ≥ 1.58} = ∅。**
且这不是"还没扫到"，而是两条独立天花板（2Y 的分组阶跃、CROWDING 的 sub/S p-不变）夹出来的。

### 38.8 ★★★★ 宇宙轴被算术关闭：TOP2500 已是 EUR/D1 最松的 sub 系数

sub 闸系数 = `0.75 × sqrt(sub_universe / alpha_universe)`（§37.6 四重验证，含平台原文）。
EUR/D1 的五个宇宙档（`get_platform_setting_options`，权威）代入：

| universe | 子宇宙 | 系数 | 相对 TOP2500 |
|---|---|---:|---|
| **TOP2500** | TOP1200 | **0.5196** | 基准（**最松**） |
| TOP1200 | TOP800 | 0.6124 | 严 +17.9% |
| TOP800 | TOP500 | 0.5946 | 严 +14.4% |
| TOP400 | TOP250 | 0.5946 | 严 +14.4% |
| TOPCS1600 | 未测 | 未知 | 需实测 |

**⇒ 缩宇宙只会让 sub 闸更严，不会更松。** §37.13 把「宇宙档完全未测」列为第 3 优先轴，
**本轮据系数公式把它降级**：TOP1200 / TOP800 / TOP400 三档在 sub 闸上是**先验判死**（比率门槛抬高 14–18%，
而现有最好比率 0.5660 只比 0.5196 高 8.9%，抬高后必破）。
**只有 TOPCS1600 值得一测**（子宇宙未知，若为 TOPCS800 则系数 0.5303，仍比 0.5196 严 ⇒ 先验也偏低）。
⚠ 但缩宇宙会同时改变信号本身，§37.13 记的区域档案「TOP2500 2.19 → TOP1200 0.33 → TOP400 0.50」
是另一种机制的实测，**不能作为本族的判死证据**——本条的判死只针对 sub 系数这一项。

### 38.9 ★★★★★★★ 裁决：`analyst_factor_signals` 已**带证明地**穷尽 ⇒ 目标自带的换数据集条款被触发

目标的过程约束原文：「不得频繁切换数据集，**仅在确实无计可施时才更换，并说明原因**」。
**本节 38.7 的定理 + 38.5 的 ATOM 不可退出 + 38.8 的宇宙轴关闭，共同构成「确实无计可施」的证明，不是猜测。**
换数据集的**原因说明**（照目标要求写明）：

1. **prod 墙不可破**：`industry` 分组下只有 CROWDING 能压到 0.7 以下，而 CROWDING 把 sub/S 钉死在 0.4356（p-不变）；
   `subindustry` 分组下 prod 与 sub 都能过，但 2Y 天花板 1.75，比 ATOM 线低 15.6%。两条天花板独立，无参数可同时绕过。
2. **字段轴已扫尽**：`analyst_factor_signals` 108 字段、12+ 机制族，除 `*_estimate_change_3mo` 外**全部实测判死**
   （Batch P 10/10 负，max |S| 1.09 且为负、max 2Y 0.60；加上更早的 `coeff_var` S 0.80）。§31.5 的「成长陷阱」作为主信号已定量关闭。
3. **算子轴已扫尽**：`group_rank`（S 0.92）、`vector_neut`（S 0.84）、`tail`（Δprod −0.0053）、`hump`（S 1.33/F 0.78）、
   `ts_backfill`（比率只从 0.429 动到 0.433）、嵌套分组（外层 industry 贡献恰为零）——全部实测无效。
   18 个幽灵算子（§37.9）与 ATOM 禁用的 `inst_pnl()`/`convert()` 进一步缩小了合法算子面。
4. **设置轴已扫尽**：12 档中性化 9 档实测 + 3 档算术判死；decay 10–120 六点梯；p 1.4–2.0 四点；
   universe 五档中四档被 sub 系数公式先验判死。
5. **相关性轴封顶**：本族最大互相关团 = **4 颗**（§32.2 全量枚举，非采样），**「一族出 10 颗互相关 < 0.7」从未被证明可行**，
   且这 4 颗全部 2Y < 2.023。

**⇒ 即使 38.7 的定理不成立，相关性天花板也独立地把本族的产出上限压在 4 颗，而 4 颗全过不了 ATOM 线。**

**★★★ 由 38.6 得出的新选集判据（可直接用于下一步，这是本轮最有价值的可复用产物）：**

> **ATOM 挖掘要选「最近 2 年（2022–2023）强」的信号，不是「全史强」的信号。**
> 操作上：新数据集的首批探针回测后，**先读 `get_alpha_yearly_stats` 的 2022 与 2023 两年**，
> 若两年 Sharpe 的聚合 < 2.0，则该数据集在 ATOM 通道下**结构性无望**，不必再扫参数——
> 因为 38.7 已证明 2Y 是分组粒度的阶跃量、参数调不动它。
> **这条判据能在烧掉参数扫描配额之前就淘汰数据集，是本战役用 100+ 槽换来的最省配额的一条规则。**

**下一个数据集的候选（按目标第 1 步「EUR 全部 Analyst 数据集逐一扫描，排除已点亮塔」）**：
EUR/D1/ANALYST 塔现 **1 颗**（用户口径「点亮 = ≥3 颗」⇒ **未点亮** ⇒ Analyst 类全部在范围内）。
最大空白 = **`analyst_consensus`（1929 字段，αC 仅 95，cov 0.7027，档案原话「本类最空旷，非 targetprice 部分未扫」）**。
⚠ 已知工程坑：`get_datafields` 的 `offset` 被静默忽略（本战役因此漏了 8/108 个字段），
1929 字段必须走 `limit ≤ 50` 的分页绕行或 `search=` 分片，**且要按 §34.2 先算 F 闸天花板再烧槽**。
⚠ `analyst9/10/11/14/39/45` 均在 `family_dead_datasets`，不重开。

### 38.10 必须由用户裁决的事项（38.5 之后从两项增为三项）

- **(a) 【新，最重要】目标的「ATOM」要求本身就是不可达的根因，需用户重新裁定目标口径。**
  平台原文证明 ATOM 身份由表达式自动决定、不可选择（38.5）；而 ATOM 的 2Y 单窗口对本族是**更严**而非"放宽"（38.6）。
  三条可选口径：
  ① **维持 ATOM**，按 38.9 的新判据换到「2022–2023 强」的 Analyst 数据集重挖（工作量：新 S0/S1/S2 全链，且**不保证存在这样的数据集**）；
  ② **改为常规（非 ATOM）单数据集 alpha**——但单数据集 ⇒ 自动 ATOM，**要非 ATOM 就必须用 ≥2 个数据集**，
    这与项目锁定项「禁混信号」及记忆 `add-a-b.md` 冲突，需用户明确解除；
    若解除，则 `xA1dQVVm`（S 1.79 / F 1.45 / 2Y 1.75 / prod 0.6933 / 比率 0.5531 / failed_ra 0）
    **在 IS Ladder 下经 N=3 升级即 PASS**（38.6 已算），是立刻可用的第一颗；
  ③ **接受少于 10 颗**：当前 0 颗全闸通过；最好是 `npA8wwz8`（6 闸过 5，只差 sub，且 38.7 证明 sub 不可修）
    与 `1YjzoEGm`（6 闸过 5，只差 prod 0.7398）。
- **(b) `1YjzoEGm` 的 prod 豁免条款是否要用一次不可逆提交去行使**（§37.7）：平台允许
  「*a sharpe at least 10% greater than other correlated alphas submitted by user*」，它对任何 S ≤ 1.573 的在位者成立，
  但**在位者身份与 Sharpe 在 API 上不可读**（`get_record_sets` 无相关性记录集，`PROD_CORRELATION` 在 `pending`）
  ⇒ **只能靠真提交来验证，不可逆，且必须用户明确确认（红线，任何 waiver 无效）。**
- **(c) 塔位冲突**：10 颗全 Analyst 会在再提交 2 颗后点亮 `EUR/D1/ANALYST`（现 1 颗），
  届时锁定项「已点亮塔不作主数据集」生效；EUR/D1 跨类别总余量 9 颗。
  ⚠ 但按 38.9，本族最多产出 4 颗互不相关者且全过不了 ATOM 线 ⇒ **该冲突在 ATOM 口径下实际不会触发**。

**⚠ 38.4 的稳健性警报适用于以上全部**：三颗过 2.023 的候选都是被 **2022 单年**抬过去的（2023 只有 1.22），
**OS 期望值应按 ~1.22 估，不是 2.09**。若用户选 (b)，这条必须在提交前写明。

### 38.11 本节取代的旧结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| §37.1 | 「四闸合取无解」，且「2Y-可过集 {FAST, CROWDING} 与 sub-可过集 {SUBINDUSTRY} 不相交」 | **表述过强且会误导**：`subindustry` 分组下 FAST 同时过 prod 与 sub（38.3）。真正的冲突是**一条轴**（分组粒度），见 38.7 |
| §37.13 第 1 优先轴 | 「COUNTRY / SECTOR 中性化……COUNTRY 是唯一有可能像 CROWDING 那样大幅压 prod 的档」 | **✗ 实测否证**：COUNTRY prod = **0.81**，全战役最差。机制推断（多国宇宙 ⇒ 国家倾斜是共享大头 ⇒ 去掉它会降 prod）**方向搞反了**：粗中性化**保留**风格暴露，而风格暴露正是与生产池重叠的部分（38.2 的 returns 翻倍是同一件事的另一面） |
| §37.13 第 3 优先轴 | 「宇宙档完全未测」列为第 3 优先 | **降级**：TOP1200/TOP800/TOP400 被 sub 系数公式先验判死（38.8），只剩 TOPCS1600 且先验亦低 |
| §36.2 | 「⚠ 本条尚需一次实证核验（读某颗 alpha 的 IS Testing Status 记录，看 cutoff 到底是 2.023 还是别的数）」 | **已核，且答案比数值更根本**：ATOM 身份由表达式自动决定、不可选择（38.5）。cutoff 数值本身在 API 上仍不可读（无 IS Testing Status 记录集），但**已无关紧要**——身份不可退出 ⇒ 2.023 必然适用 |
| §36.2 | 「按 2.023 从严规划：宁可当作过不了」 | **该保守假设已被平台原文证实为正确**，不再是假设 |
| 38.3 本条 | 我当场准备写下的「prod ↔ sub/S 结构性反相关」 | **未写入即被否证**，登记在此以防再犯（本战役第二次同形状错误，见 §37.2） |

---

## §39 Batch T–Z：组合轴穷尽、四闸交集空的代数证明、封存判死条目被否证、与 analyst10 修正族的发现

> 本节覆盖 Batch T / U / V / W / X / Y / Z。所有回测档：**EUR / TOP2500 / D1 / decay 20 / FAST / trunc 0.08 /
> pasteurize ON / VERIFY / nanHandling ON / maxTrade ON / maxPosition OFF / FASTEXPR / 2014-01-01→2023-12-31 / FULL**。
> 闸线：S ≥1.58｜F ≥1.0｜TO ∈[0.01,0.7]｜2Y ≥1.58（**ATOM 线 2.023**）｜sub/S ≥**0.51961**（TOP2500）｜prod <0.7。

### 39.1 ★「分组粒度」定律——取代 38.x 的「country 是唯一 prod 杠杆」

全部为 inner `group_zscore(·, industry)` + `signed_power(·,1.8)` + outer `group_neutralize`，字段 `netprofit_y2_estimate_change_3mo`：

| outer group | alpha | prod | Δ vs 裸式 |
|---|---|---:|---:|
| 无（裸式） | `1YjzoEGm` | 0.7398 | — |
| `market` | `YPxg1LzM`（**V5**） | 0.7398 | **0.0000** |
| `sector` | `mLYVoLjX`（V7） | 0.7397 | −0.0001 |
| `country` | `zqrR3AWo`（V3） | **0.7370** | −0.0028 |
| `cart(market,country)` @p2.0 | `RRA1EaQn`（W3） | **0.7156** | −0.0242 |
| `cart(industry,country)` | `QPY9KoLX`（T1） | ~0.66 | −0.08 |
| `cart(subindustry,country)` | `omogWGW6`（T5） | **0.5827** | **−0.157** |

**定律**：`country` 压 prod 的幅度**正比于它笛卡尔伙伴的细度**（market 最粗 −0.024 → subindustry 最细 −0.157）。
而「细」同时正是摧毁 S 与 sub 比率的东西 ⇒ **prod 闸与 S/sub/2Y 闸通过同一个变量（分组粒度）耦合**。
**这就是每条候选都在第五闸上失败的根本原因**——不是运气，是结构。

⚠ 我上一段对 Batch W 的预测（prod ~0.60–0.68 ✓）**被否证**：W3 实测 **0.7156 ✗**。
根因是我从 Batch V 推断「`country` 无论与谁做笛卡尔都压 prod 0.08–0.15」。更正后才有 39.2 的代数与 Batch Y 的设计。

### 39.2 ★★ p 窗口代数：np_y2 的四闸交集**可证明为空**，prod 是唯一不可跨越的闸

同组合（inner `industry`，np_y2，FAST/d20/TOP2500）上两个 p 点：

| p | S | 2Y | sub 比率 | prod |
|---:|---:|---:|---:|---:|
| 1.8（V3 `zqrR3AWo`） | 1.72 ✓ | 2.09 ✓ | 0.5116 ✗ | **0.7370** ✗ |
| 2.0（W3 `RRA1EaQn`） | 1.63 ✓ | 2.02 ✗ | 0.5215 ✓ | **0.7156** ✗ |
| **每 +0.2p 斜率** | **−0.09** | **−0.07** | **+0.0099** | **−0.0214** |

从 p1.8 锚点逐闸解 p：S ≥1.58 ⇒ **p ≤ 2.111**；2Y ≥2.023 ⇒ **p ≤ 1.991**；sub 比率 ≥0.51961 ⇒ **p ≥ 1.962**；prod <0.7 ⇒ **p ≥ 2.146**。

⇒ **S/2Y/sub 三闸确实可同时满足，窗口 p ∈ [1.962, 1.991]**；但 prod 要求 p ≥ 2.146，那里 2Y 已跌到 ~1.94、S ~1.53。
**可行区间为空。** 这把 §38.7 的「交集为空」从观察升级为**两斜率代数证明**，并把 prod 指认为**唯一不可跨越**的闸。

⚠ 同时首次实测：**p↑ 确实压 prod（−0.0214 / +0.2p）**，此前假设为近零。它是真的 prod 杠杆，只是太弱：
−0.037 prod 的代价是 −0.157 S 与 −0.123 2Y。

### 39.3 两条恒等式（各省一类槽位）

1. **`group_neutralize(x, country)` ≡ `group_neutralize(x, densify(cart(market,country)))`，逐字节相同。**
   V3 `zqrR3AWo` 与 W1 `9qE7x9Rx` 在**每个字段上完全一致，含 pnl 10 133 099**（S 1.72 / F 1.52 / TO .0683 /
   returns .0982 / DD .066 / margin .002876 / long 1466 / short 1353 / sub 0.88 / 2Y 2.09 / CLUSTER 1.31）。
   机制：**EUR 是单一 `market`**，故 `cart(market,country)` 退化为 `country`。
   ⇒ **`densify(cart(market,·))` 在 EUR 是浪费槽位，直接用裸 group。**（`neut-users` 文档为 EUR/ASI/GLB 推荐的
   正是这个笛卡尔形式 ⇒ **该官方建议在 EUR 部分退化。**）
2. **`exchange` ≈ `country`（EUR/TOP2500）**：V4 `9qE7xGRV` 与 V3 的 pnl 仅差 **0.03%**（10 136 581 vs 10 133 099），
   S/F 各 +0.01。机制：EUR/TOP2500 里每个国家基本只有一个主导上市交易所。

### 39.4 ★ Batch X：αC ↔ **信号强度**定律（αC 不是「机会」代理）

把 V5 组合原样套到 9 字段网格的未测字段上，结果对 `alphaCount` **单调**：

| 字段 | αC | cov | S | F | 2Y | sub 比率 | alpha / 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| eps_y1_estimate_change_3mo | **176** | .9311 | **1.75** ✓ | 1.54 ✓ | **2.20** ✓ | 0.4457 ✗✗ | `wp9EQAWx`——sub 差 0.074 |
| netprofit_y1_estimate_change_3mo | 72 | .9268 | **1.83** ✓（战役最高） | **1.69** ✓ | 1.68 ✗ | 0.5137 ✗（差 0.006） | `58jkE1vX`——returns **.1072** 战役最高 |
| **netprofit_y2_estimate_change_3mo** | **51** | .9269 | 1.73 ✓ | 1.54 ✓ | 2.09 ✓ | **0.5202 ✓** | `YPxg1LzM`——只差 prod 0.040 |
| eps_y2_estimate_change_3mo | 76 | .9310 | 1.44–1.72 | — | 1.47–1.87 ✗ | 变动 | 2Y 封锁 |
| revenue_y1_estimate_change_3mo | 34 | .9273 | **1.16** ✗ | 0.74 ✗ | **0.84** ✗ | **0.207** ✗✗ | `YPxg1o9A` **死** |
| revenue_y2_estimate_change_3mo | 26 | .9278 | **1.16** ✗ | 0.74 ✗ | **0.89** ✗ | 0.517 ✓ | `bl8d61Lq` **死** |
| revenue_y2 + cart(market,country) | 26 | .9278 | **1.14** ✗ | 0.72 ✗ | **0.85** ✗ | 0.50 ✗ | `QPY9vRmw` **死**（第二结构，铁律③） |

⇒ **更正后的定律**：同一数据集内，低 αC 既可能意味着「不拥挤的机会」，也可能意味着「没信号所以没人挖」。
**在 `analyst_factor_signals` 里是后者——拥挤度是信号质量的内生结果。**
我的 Batch X 立论前提（低 αC ⇒ 低 prod ⇒ 未开发机会）**被否证**，但对照组（eps_y1，αC 176 最拥挤）
反而确立了 αC↔强度定律，**用它零槽位判死了剩下 3 个未测字段**：
`netprofit_q1_estimate_change_1mo`（αC **5**，cov **.4307**）、`eps_q1_...`（αC 21，cov .4614）、
`revenue_q1_...`（αC 17，cov .5245）——αC 最低**且**覆盖率最低 ⇒ 先验弱于 revenue 的 1.16。**未花槽位。**

### 39.5 Batch W 完整读数

| tag | alpha | outer | p | S | F | TO | returns | DD | sub | 2Y | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| W1 | `9qE7x9Rx` | cart(market,country) | 1.8 | 1.72 | 1.52 | .0683 | .0982 | .066 | 0.88 | **2.09** | 1（LOW_SUB） |
| W2 | `pwvKdobg` | cart(sector,country) | 1.8 | 1.70 | 1.43 | .0661 | .0887 | .0725 | **0.79** | 1.96 | 1（LOW_SUB） |
| **W3** | **`RRA1EaQn`** | cart(market,country) | **2.0** | 1.63 | 1.45 | .0714 | .0994 | .0764 | 0.85 | 2.02 | **0** |
| W4 | `kqJZNLoL` | cart(market,country)，**eps_y2** | 1.8 | 1.44 | 1.21 | .069 | .0877 | .0869 | 0.77 | **1.47** | 2（S, 2Y） |

**W2 的 sub 比率 0.4647 明显差于 W1 的 0.5116** ⇒ 笛卡尔内部 `market` 优于 `sector`。
这是一条**新的不对称**：作为裸包裹时二者对 prod 都是空操作、对 S/2Y 几乎相同。

### 39.6 Batch Y：最后一个未测组合格（inner `industry` × outer `cart(subindustry,country)`）

设计依据：交叉比对全部已测组合后，**inner `industry`（2Y 最高，2.09）从未与 outer `cart(subindustry,country)`
（prod 最低 0.5827、且看似保 sub）配对过**。T1 是 inner industry + outer cart(**industry**,country)（sub 比率被打到 0.397）；
T5 是 inner **subindustry** + outer cart(subindustry,country)（S 只有 1.44）。

| tag | alpha | 字段 | outer | p | S | F | TO | returns | DD | sub | 比率 | 2Y | failed_ra |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Y1 | （仍在跑） | np_y2 | cart(sub,country) | 1.8 | — | — | — | — | — | — | — | — | — |
| Y2 | `E5VeQYwK` | np_y1 | cart(sub,country) | 1.8 | **1.13** | 0.81 | .0691 | .0637 | .0817 | 0.54 | 0.478 | **1.13** | 4 |
| **Y3** | **`zqrRdjdE`** | np_y2 | cart(sub,country) | **2.0** | **1.38** | 1.07 | .0702 | .0753 | .0578 | **0.77** | **0.558 ✓** | 1.89 | 1（LOW_SHARPE） |
| Y4 | `xA1dvXlw` | np_y1 | 裸 `subindustry` | 1.8 | 1.60 | 1.29 | .0651 | .0813 | .0964 | 0.78 | 0.4875 | **1.19** | 2 |
| Y5 | `RRA1e050` | eps_y1 | cart(sub,country) | 1.8 | **1.26** | 0.89 | .0704 | .0627 | .080 | 0.46 | **0.365** | 1.59 | 3 |

**预登记预测的逐条裁决（不是只读数字）**：

- **Y2 预测 S 1.58–1.68 / 2Y 1.60–1.75 ⇒ 实测 1.13 / 1.13，大幅否证。**
- **Y5 预测 S 1.52–1.62 / 2Y 2.05–2.15 / 比率 .47–.50 ⇒ 实测 1.26 / 1.59 / **0.365**，全面否证。**
- Y3 未预登记；实测 S ✗（差 0.20）、2Y ✗（差 0.13）、比率 ✓ 0.558。

**outer `cart(subindustry,country)` 的代价按字段变化极大**（以 outer `market` 的同字段腿为基准）：

| 字段 | 基准（outer market） | Y 腿（outer cart(sub,country)） | ΔS | Δ2Y | Δ比率 |
|---|---|---|---:|---:|---:|
| np_y2 @p2.0 | W3 S1.63 / 2Y2.02 / .5215 | Y3 S1.38 / 2Y1.89 / .558 | **−0.25** | −0.13 | **+0.037** |
| np_y1 @p1.8 | X3 S1.83 / 2Y1.68 / .5137 | Y2 S1.13 / 2Y1.13 / .478 | **−0.70** | −0.55 | −0.036 |
| eps_y1 @p1.8 | X5 S1.75 / 2Y2.20 / .4457 | Y5 S1.26 / 2Y1.59 / .365 | **−0.49** | −0.61 | **−0.081** |

⇒ **我从 T5 推断的「subindustry 笛卡尔保 sub 比率」是单字段假象**：它在 np_y2 上抬比率，在 np_y1 / eps_y1 上**压**比率。
**斜率不跨字段迁移**——本战役第 4 次同形状错误（前 3 次：Batch Q 的 p 轴外推差 3 倍、§32.1 decay→prod 斜率偏浅、Batch U 的 2Y 方向搞反）。

### 39.7 ★★ 新的机制发现：**预测期（y1 vs y2）决定信号在行业层级里的位置**

去掉 subindustry 均值（即 outer 含 `subindustry`）所损失的 S，直接度量「有多少 Sharpe 来自 subindustry **之间**」：

- **np_y1 损失 0.70 S** ⇒ 其 Sharpe **主要在 subindustry 之间**（类行业轮动）。
- **np_y2 只损失 0.25 S** ⇒ 其 Sharpe **主要在 subindustry 之内**（个股特质）。

金融解读：1 年期修正按行业周期成簇；2 年期修正更贴近公司特质。
⇒ **这解释了为什么 np_y2 是唯一同时过 2Y + sub + S 的字段：它的信号恰好落在 sub-universe 闸奖励的层级上。**
与 §Batch G2 的「horizon 结构按族不同、不可跨族外推」一致，但这里是**同族内按 horizon 分层**，更细。

### 39.8 ★★★ 一条**已封存**判死条目被本战役实测否证（台账内最严重的错误）

`EUR-COUNTRY-EXCHANGE-SECTOR-GROUPING-DEAD`（family `analyst_revision`，dataset `analyst_factor_signals`，
`created_at`/`updated_at` **2026-10-20T01:59:38**，`dead_at` 2026-10-19）原文裁定：

> *"For EUR analyst_revision fields, group ONLY at subindustry (or industry if chasing returns/F, accepting the sub gate failure).
> **Do NOT use country, exchange, or sector grouping.** Nested double-grouping is also dead: the finer layer dominates
> and the coarser layer contributes nothing."*

并把 `market` 列入 `untested_but_expected_dead`：*"7th exempt grouping field, **never measured**; given country/exchange
collapse by -0.69 S, market is expected to behave the same. **Lowest priority.**"*

其支撑读数**全部**是把 group 当作 **inner `group_zscore`**、在 **decay 80 + CROWDING** 下测得
（batch `t1Y88cNQ4GobZABea5tYYx`、`4haxhZ5Cs4MG9f247dVFd87`；基线「同字段 + subindustry 分组 = S 1.53，sub/S 0.464，failed_ra 4」）：

| group | 作 **inner zscore**（被封存） | 作 **outer `group_neutralize`**（Batch V，FAST/d20） |
|---|---:|---:|
| country | `RRA108zd` S **0.84** / F .66 / ret .0774 / DD .2046 / sub .27 / 比率 .321 / 2Y 1.34 | `zqrR3AWo` **S 1.72 / 2Y 2.09** |
| exchange | `gJW97MGe` S **0.85** / F .67 / 比率 .329 / 2Y 1.34 | `9qE7xGRV` **S 1.73 / 2Y 2.09** |
| sector | `88veggKa` S **0.89** / F .70 / DD .1571 / 比率 .438 / 2Y 1.21 | `mLYVoLjX` **S 1.73 / 2Y 2.09** |
| sector p1.8 | `WjLVKKWG` S 0.70 / F .55 / 比率 .229 / 2Y 1.25 | — |
| **market** | *「never measured, expected dead, **Lowest priority**」* | **`YPxg1LzM` S 1.73 / F 1.54 / 2Y 2.09 / `failed_ra_count` **0**** |

其 `nested_grouping` 证据（`MP0L995a`：「returns 0.0481 == subindustry 单层 0.0487 ⇒ outer industry z-score 贡献为零」，S 1.44）
与其 `contradicts` 块（宣称 EUR 区域面板「country 轴中性化/分组有意义」是 REGION-LEVEL PRIOR、对 analyst_revision 族已被否证、
「**Do not spend slots on country grouping for revision fields without new evidence**」）**同样是位置特异的**。

⇒ **被该条判死并列为「最低优先」的 group，产出了本战役唯一一条「全 RA 闸通过 + ATOM 2Y 通过」的候选。**
机制：作 **inner** `group_zscore` 时这些 group **替换**了定义信号的分组，从而摧毁信号；作 **outer** `group_neutralize`
且设置档为 FAST 时，**设置层中性化最后施加、起主导作用**，故包裹层对 S/2Y 近乎空操作。

⚠ **这是 §30.6 / 元定律错误形状的第 5 例，且是第一次出现在一条*已封存*条目里**——
一条由「把 group 当**替代**扫」推出、却从未「把 group 当**包裹**测」的判死。
⚠ **`seal_dead_end` 是 fail-closed 单向、无解封路径 ⇒ 更正它是人的决定，本节只登记矛盾，不静默覆写。**
**若我当初服从这条台账，Batch V 根本不会被设计出来。**

同形状的还有 `EUR-NONMODEL-TOWER-CEILING`（`dead_at` 2026-09-11）：*"EUR非MODEL塔信号强度天花板0.3-0.4远低于1.58硬闸"*
——它只在 `analyst45`（max_sharpe 0.32）上测得却推广到整个非 MODEL 塔空间；**本战役在 analyst 塔实测 S 1.73–1.90**，
该**塔级天花板断言作废**（其对 `analyst45` 的具体读数可能仍成立）。

### 39.9 ★★ 元定律（第 5、6 例后定稿）

已累积的同形状错误：§37.2「非 FAST ⇒ 低 prod」（被 SUBINDUSTRY 的 0.7649 否证）·
§38.3「prod ↔ sub/S 反相关」（被 subindustry 切片否证）· §38.7「2Y 天花板 1.75 / 交集为空」（被 T4 否证）·
**αC 是机会代理**（被 revenue 的 S 1.16 否证）· **`EUR-COUNTRY-EXCHANGE-SECTOR-GROUPING-DEAD`**（被 Batch V 的包裹位实测否证）·
**`EUR-NONMODEL-TOWER-CEILING` 的塔级天花板**（被本战役 S 1.73–1.90 否证）。
**全部都是在扫一条轴、同时固定另一条轴的情况下得出的。**

> **定稿律**：**设置轴扫不出组合轴能发现的东西；替代位扫不出包裹位能发现的东西；单字段扫不出跨字段能发现的东西。
> 任何「穷尽 / 无解 / 天花板 / 判死」的断言，必须写明扫了哪些轴、哪个算子位置、哪个设置档、以及分母是多少字段。
> 算子嵌套、包裹（composition）与*位置*（inner substitution vs outer wrapper）是与设置正交的独立轴，设置扫描在结构上覆盖不到它们。**

推论：**`analyst_factor_signals` 在算子轴上并未穷尽——§38.9 的五重封闭裁定在其第三重上作废**（那一重把算子当替代枚举，从未当包裹枚举）。

### 39.10 clique = 1：7 条最优腿两两互相关全 > 0.7

`compute_mutual_correlation`（**完全本地**：`num_points 1021`、`years 4`、`missing_pnl []`、`local_calculation true`，**零槽位**）
对 7 条最优腿返回 **`max_mutually_below_subset_size = 1`**，21 对全部 > 0.7，`all_below_threshold false`，`max_subset_exact true`。
`max_pair = MP0L0lL8 × JjPvP0lA = 0.9913`（表达式相同、decay 60 vs 40 ⇒ **decay 不是去相关轴**）；
`MP0L0ALL × 9qE7EQ71 = 0.9877`（outer `sector` vs outer `cart(sector,country)` ⇒ **有了 sector，country 分量几乎不加东西**）。
`1YjzoEGm` 是最不相关成员（0.7463–0.8111），恰恰因为它是唯一没有 outer 包裹的。

**§32.2 去相关定律（两次扩展后）**：设置档（decay/中性化/p）= **不去相关**（0.72–0.99）·
组合（outer group 身份 / decay / p）= **不去相关**（0.75–0.99）· 分组粒度 = **去相关**（0.6392, 0.6888）·
同族换字段 = **去相关**（0.4713–0.6032）· **换字段族 = 最强**（0.3187–0.4184）。
⇒ **N 颗 alpha 的配方 = N 个不同*字段*，不是 N 套设置或组合。**
⚠ 铁律：`check_self_correlation` 只比对已提交 OS 池，**无法**发现 UNSUBMITTED 候选之间的重复。
⚠ 与旧「clique 上限 3」不矛盾：那是另一个更松的池上的抽样假象（真值 4）；本次是 7 条最优腿构成的**更紧**的池。

### 39.11 9 字段网格算术：单数据集最多 9 颗，而实测全闸通过率 0

`get_datafields(dataset_id="analyst_factor_signals", region="EUR", universe="TOP2500", delay=1,
search="estimate_change", limit=100)` → **`count 9`**，`sharpe_filter_applied true`，`sharpe_filter_removed 0`，全 MATRIX。
结合同字段组合互相关 0.75–0.99（clique=1）⇒ **该数据集最多产出 9 颗互不相关的 alpha；
其中 6 个已测、全闸通过率 0；另 3 个 q1_1mo 字段被 39.4 的定律 + 覆盖率 0.43–0.52 先验判死。**
⇒ **10 颗 ATOM 不可能来自单一数据集。**

完整网格（cov / αC / uC）：eps_y1 .9311/176/129 · eps_y2 .9310/76/57 · netprofit_y1 .9268/72/49 ·
netprofit_y2 .9269/51/34 · revenue_y1 .9273/34/30 · revenue_y2 .9278/26/21 ·
revenue_q1_1mo **.5245**/17/11 · eps_q1_1mo **.4614**/21/17 · netprofit_q1_1mo **.4307**/5/4。

### 39.12 ★★ 完整候选闸门矩阵（搜索状态）

| 候选 | 字段 / 组合 | S ≥1.58 | 2Y ≥2.023 | 比率 ≥0.5196 | prod <0.7 |
|---|---|---|---|---|---|
| **V5 `YPxg1LzM`** | np_y2，in industry，out `market`，p1.8 | ✓ 1.73 | ✓ 2.09 | ✓ 0.5202 | ✗ **0.7398** |
| V3 `zqrR3AWo` | np_y2，out `country`，p1.8 | ✓ 1.72 | ✓ 2.09 | ✗ 0.5116 | ✗ 0.7370 |
| W3 `RRA1EaQn` | np_y2，out `country`，p2.0 | ✓ 1.63 | ✗ 2.02（差 0.003） | ✓ 0.5215 | ✗ 0.7156 |
| Y3 `zqrRdjdE` | np_y2，out cart(sub,country)，p2.0 | ✗ 1.38 | ✗ 1.89 | ✓ **0.558** | 未测 |
| X5 `wp9EQAWx` | eps_y1，out `market`，p1.8 | ✓ 1.75 | ✓ **2.20** | ✗✗ 0.4457 | 未测 |
| X3 `58jkE1vX` | np_y1，out `market`，p1.8 | ✓ **1.83** | ✗ 1.68 | ✗ 0.5137 | 未测 |
| U2 `MP0L0ALL` | np_y2，in subindustry，out `sector` | ✓ 1.72 | ✗ 1.73 | ✓ **0.564**（最佳） | 未测 |
| T3 `XgR8JMk8` | np_y2，分组在 zscore **内部**：`sp(gz(np_y2, densify(cart(industry,country))),1.8)` | ✓ **1.90**（全战役最高 S） | ✗ 1.82 | ✗✗ 0.3947 | 未测 |
| T1 `QPY9KoLX` | np_y2，in industry，out cart(industry,country) | ✗ 1.46 | ✓ 2.05 | ✗✗ 0.397 | ✓ ~0.66 |
| T5 `omogWGW6` | np_y2，in subindustry，out cart(subindustry,country) | ✗ 1.44 | ✗ 1.95 | ✓ 0.528 | ✓ **0.5827** |

**V5 仍是唯一的 3/4 候选。** 不可跨越缺口分析：X5 的 sub 缺口 0.074 按实测 p 斜率需 +1.5p ⇒ p≈3.3，
那里 S 掉到 ~1.08、2Y ~1.68 ⇒ 被同一套代数判死；decay 每 +20 只给 +0.005 比率 ⇒ 需 +296 decay ⇒ 死。
X3 的 2Y 缺口 0.34 不可达。**U2/T3 的 prod 即使达标也过不了 2Y / 比率 ⇒ 它们的 prod 只有建律价值。**

⚠ **prod 直方图按项目自己的 `wq-window-valley-break-prod-wall` 判据 condamne 本族**：
*「先用 prod 直方图 [0.7,0.8) 桶 n 值判族级命运（n=0 可救 / n≥1 必死）」*。
V3 `zqrR3AWo` [0.7,0.8) **n=3**（max 0.737）· W3 `RRA1EaQn` **n=1**（max 0.7156）⇒ **族级必死**，与 EUR profile 的「prod 密墙」诊断一致。

### 39.13 ★★ 目标步 1 破解：`get_datafields(dataset_id=null, search=…)` 可跨数据集枚举

四条枚举途径全部失败之后（`get_datasets` 无 analyst 类别、`get_dead_datasets` 无 analyst、
`get_field_catalog` **必须传 `dataset`** 故不能枚举、`recommend_datasets` top_n=50 **零** analyst 数据集
——尽管它显式给「未点亮金字塔」0–40 分权重，而我们 27 颗 alpha 全报 `pyramid_short: "analyst"`），
**第五条途径成功了**：

```
get_datafields(region="EUR", universe="TOP2500", delay=1,
               dataset_id=null, data_type="MATRIX", search="estimate")
→ count 99, sharpe_filter_applied true, sharpe_filter_removed 1
```

**`dataset_id` 在 schema 里是 `anyOf:[string, null]` ⇒ 可为 null，此时 `search` 跨全部数据集检索。**
返回的字段带 `anl4_` 与 `anl10_` 前缀 ⇒ 命中 `analyst4` 与 `analyst10`（及一个共享 `anl10_` 前缀的姊妹数据集）。

**★★ 两条必须记住的工具口径（都是本段实测踩出来的）**：

1. **`get_datafields` 的 `search` 匹配的是 *description*，不是字段 id。**
   证据：`search="revise_ratio_to_consensus"` → **`count 0`**；而 `search="estimate"` 返回了 id 里含
   `revise_ratio_to_consensus` 的字段，因为它们的 description 是 *"Consensus **estimate** value for …"*。
   ⇒ **要按字段名找，必须用 description 里的词；要确认某个 id 是否存在，只能按数据集逐个 census 后 grep。**
2. **字段 id 前缀 ≠ 数据集 id。** `analyst10` 的 295 字段 census 里**确实没有** `netrevise` / `salrevise` /
   `grmrevise` / `ndtrevise` / `oprrevise`（窄 grep 零命中，非截断），但 `search="estimate"` 跨库检索返回了它们。
   ⇒ **同一厂商前缀横跨多个 BRAIN 数据集。**`analyst10` 拥有 `cpx / csh / dps / ebi / ebt / gps / analyst_innovation_tbv`；
   `net / sal / grm / ndt / opr` 属姊妹库（`analyst7` 用 `search="consensus"` 探测返回 0，**归属尚未定位**）。
   ⚠ 这直接影响 **ATOM 合规判定**：同前缀不等于同数据集，混用两个前缀相同的字段仍可能破 ATOM。

`get_datasets(region="EUR", universe="**TOPCS1600**", category="analyst")` 亦返回 **0**；
`search="analyst"` 在 TOPCS1600 返回 33 条，全部是 description 文本命中（"analyst coverage"、"analyst/investor days"、
"analyst earnings estimates"），类别只有 other/earnings/fundamental/imbalance/insiders/pv/risk/sentiment/socialmedia，
**没有任何 id 以 `analyst` 开头、也没有 category=analyst 的数据集**。
⇒ **`get_datasets` 对 EUR analyst 类别是系统性不完整的：数据集可按 id 直接访问，却在枚举端点上隐形。**
（`analyst_factor_signals` 整个战役都在 TOP2500 正常回测，却从不出现在 `get_datasets` 结果里 ⇒ 决定性反证。）
⚠ 顺带：平台的 dataset **description 与 name 大面积错配**（`imbalance5` 名为 "Oil Price Resilience Scores"，
description 却是 RIC/BBID 映射；`risk72` 名为 "Specific return of extended factors"，description 却是分析师盈利预测）
⇒ **description 不可作为语义依据**，本战役已多次证实。

### 39.14 ★★★ `analyst10` 修正族：295 字段、覆盖率≈1.0、αC 低至 2

`get_datafields(dataset_id="analyst10", region="EUR", universe="TOP2500", delay=1, data_type="MATRIX")`
→ **`count 295`**，`sharpe_filter_removed 5`。族结构高度规整：
**每个指标前缀 × 3 种形态 × fy1/fy2**：

```
anl10_<metric>revise_ratio_to_close_fy{1,2}       ← 价格标度（被封存条目测过的就是这一形态）
anl10_<metric>revise_ratio_to_consensus_fy{1,2}   ← 预测值标度（★ 未测，且与本战役赢家同一经济量）
anl10_<metric>revise_value_fy{1,2}                ← 绝对修正量
```

`ratio_to_consensus` 形态的实测覆盖率与拥挤度：

| 字段 | cov | αC | 是否在 analyst10 census 内 |
|---|---:|---:|---|
| `anl10_netrevise_ratio_to_consensus_fy1` | **0.9983** | **3** | ✗（姊妹库） |
| `anl10_netrevise_ratio_to_consensus_fy2` | **0.9975** | **2** | ✗（姊妹库） |
| `anl10_salrevise_ratio_to_consensus_fy1` | 0.9975 | 27 | ✗（姊妹库） |
| `anl10_salrevise_ratio_to_consensus_fy2` | 0.9958 | 7 | ✗（姊妹库） |
| `anl10_ebirevise_ratio_to_consensus_fy1` | **0.9942** | 11 | ✓ |
| `anl10_ebirevise_ratio_to_consensus_fy2` | 0.9933 | 15 | ✓ |
| `anl10_ebtrevise_ratio_to_consensus_fy1` | 0.92 | 18 | ✓ |
| `anl10_ebtrevise_ratio_to_consensus_fy2` | 0.92 | 11 | ✓ |
| `anl10_dpsrevise_ratio_to_consensus_fy1` | 0.895 | 70 | ✓ |
| `anl10_cpxrevise_ratio_to_consensus_fy1` | 0.8442 | 36 | ✓ |

对照本战役赢家 `netprofit_y2_estimate_change_3mo`（cov 0.9269，αC 51，S 1.73 / 2Y 2.09 / 比率 0.5202 / failed_ra 0）：
**`netrevise_ratio_to_consensus` 是同一经济机制（净利润修正）、覆盖率更高（0.998 vs 0.927）、拥挤度低 25 倍（αC 2 vs 51）。**
⇒ **这是全战役价值最高的线索，且它正好打在唯一的约束（prod）上**：换数据集是 §32.2 里
唯一未能动过的去相关轴，而「换字段族」已实测是最强去相关轴（0.3187–0.4184）。

### 39.15 ★★ 封存条目 `EUR-ANALYST10-PREDICTED-SURPRISE-DEAD` 的范围核验（**不覆盖本次目标**）

台账原文（id 1283，`dead_at` 2026-09-19，wave 209）：

```
family  : "analyst10 performance-weighted estimates (predicted surprise EBT/net/pretax/sales,
           innovation counts, revision ratio)"
universe: "TOPCS1600"
evidence: "8 probes |S|<=0.64: net FY1 pred surprise 0.64 (2Y 0.17), sales 0.58,
           innovation counts 0.55, EBT pred surprise 0.49 (2Y -0.14), revision/close 0.31, pretax 0.29"
verdict : "SmartEstimate-style predicted surprise has no EUR signal at D1 (unlike ASI model30 3.28)"
rule    : "EUR analyst tower: predicted-surprise family closed"
```

**四条独立理由说明它不覆盖 Batch Z 的目标**：

1. **分母只有 8 个探针 / 295 个字段 = 2.7%。**按铁律②（宣称穷尽前全量枚举），这条判死在其表面上就不成立。
2. **它测的修正是 `revision/close` = 0.31**，即 `*revise_ratio_to_close_*`（**价格标度**，被价格水平污染）；
   Batch Z 用的是 **`*revise_ratio_to_consensus_*`**（**预测值标度**，纯百分比修正 = 与
   `netprofit_y2_estimate_change_3mo` 同一经济量）。**这是不同字段、不同经济学。**
   ⇒ **该条测了价格标度形态，却把结论推广到整个修正族——与 39.8 的分组判死是同一错误形状。**
3. **宇宙是 TOPCS1600，不是 TOP2500。**按 §30.6，换设置档可整体平移 S 0.5–0.7。
4. **未记录中性化** ⇒ 几乎必然是区域默认 SUBINDUSTRY，而本战役已证它对该机制是**最差**档
   （同一表达式 FAST S 1.73 vs SUBINDUSTRY S 1.46）。

⇒ **结论：在 TOP2500/FAST/d20 上测 `analyst10` 的 `revise_ratio_to_consensus` 族，不是重复已封存路径。**
本节登记矛盾而不覆写台账（`seal_dead_end` 无解封路径，更正属人的决定）。

### 39.16 Batch Z（已派发，6/6 `ok:true`）与预登记预测

配方 = V5 的已验证形态：`group_neutralize(signed_power(group_zscore(<F>, industry), 1.8), market)`。

| tag | sim id | 字段 | 变体 | 检验什么 |
|---|---|---|---|---|
| Z1_NETcons_fy2_V5recipe | `1q71sS56V5awbouInbmMzTs` | `anl10_netrevise_ratio_to_consensus_fy2` | V5 配方 | **配方能否跨数据集迁移** |
| Z2_NETcons_fy2_bare | `2haEh5gSm4F5cue1dOS3z4mw` | 同上 | **无 outer 包裹** | 第二结构（铁律③）+ 新数据集上 outer 的贡献 |
| Z3_NETcons_fy2_tsdelta60 | `c0VSuawE4Kc8Cc5KeOx3C9` | 同上 | `ts_delta(F,60)` | **字段是水平量还是修正量**（语义消歧） |
| Z4_EBIcons_fy1_V5recipe | `4uUa6U89y4BQbQSYgba0vOZ` | `anl10_ebirevise_ratio_to_consensus_fy1` | V5 配方 | 指标轴（EBIT），census 已确认 |
| Z5_EBTcons_fy1_V5recipe | `1kpTwidio58eaIGOH42hy8W` | `anl10_ebtrevise_ratio_to_consensus_fy1` | V5 配方 | 指标轴（税前利润），census 已确认 |
| Z6_SALcons_fy2_V5recipe | `47apCDn74vuc6VA1uRG5vE` | `anl10_salrevise_ratio_to_consensus_fy2` | V5 配方 | 指标轴（销售） |

**语义消歧为什么必要**：字段名 `revise_ratio_to_consensus` 有两种可能构造——
**(a) 修正量 / 共识**（已是修正，= 本战役赢家的机制）或 **(b) 预测值 / 共识**（水平比率，1.0 = 符合预期）。
description 无法裁决（已证不可靠）。但 **`group_zscore` 横截面标准化会消掉任何常数偏移**，
故若是 (b)，Z1 等价于对 `x−1` 做横截面 z 分数，仍是一个合法的「相对共识偏离」信号；
若是 (a)，Z1 直接就是修正信号。**Z3 的 `ts_delta(·,60)` 加上时序维度**：
若 Z3 ≫ Z1 ⇒ 字段是水平量，需要时序差分；若 Z3 ≪ Z1 ⇒ 字段已是修正量，差分是过度差分。

**预登记预测（收割时逐条裁决）**：

- **Z1**：S 1.55–1.80、2Y 1.90–2.15、比率 0.50–0.54、**prod 0.45–0.62 ⇒ 若成立即为首条全闸通过**。
  依据：机制与 np_y2 同源（故 S/2Y 应接近），αC 低 25 倍且数据集不同（故 prod 应显著低于 0.7398）。
- **Z2**（裸式）：S 与 Z1 相差 ≤0.02、prod 相差 ≤0.005 ⇒ 复现「outer `market` 是 prod 空操作」；若 prod 差 >0.02，则该定律不跨数据集。
- **Z3**：S 低于 Z1（差分放大噪声），但**比率高于 Z1**（时序平滑提子宇宙稳健性）。
- **Z4/Z5/Z6**：S 1.30–1.70，按 39.4 的 αC↔强度定律，αC 11/18/7 都在低拥挤区 ⇒ 强度可能弱于 np/net 族。
- **开放风险**：这些字段可能是**日频更新的水平量**（TO 会飙升）⇒ 若 TO > 0.7 触发 HIGH_TURNOVER，
  第一归因方向是加 `ts_mean` / 提 decay，**不是**换字段（step 3 要求先归因）。

### 39.17 新工具口径（本段实测）

- **`batch_status` 的 `parent_status:"ERROR"` 不代表没有产出 alpha。** Y3 `1oHNVdgLL5g1auXude8OmYb` 报
  `parent_status:"ERROR"` + *"There was an error while running the simulation"*，但 `get_user_alphas` 里
  **`zqrRdjdE` 真实存在且指标完整**。⇒ 与已知的「`parent_status:"COMPLETE"` 为权威、忽略 `all_ok`/`errors`」
  并列：**任何 `parent_status` 都必须用 `get_user_alphas` 复核，ERROR 也一样。**
- **`get_user_alphas(order="-dateCreated")` 不按完成顺序返回刚完成的腿。** Batch X 的 5 条乱序完成：
  `batch_status` 在 21:49:20 报 X3/X5 COMPLETE，但 `limit=2` 返回 X2/X1、`limit=3` 返回 X4/X2/X1，
  X3/X5 直到 `limit=8` 才出现。⇒ **收割已知完成的批次时，`limit` 取 ≥ 批大小并按表达式文本扫描。**
- **`count` 既不是数组长度也不是可靠总数**（本段 `limit=8`→22、`limit=4`→22、`limit=2`→26、`limit=3`→27、`limit=8`→27、
  Batch Y 后 →31），恒 `partial_count:true`。**但 `count` 的*增量*可用作完整性校验**（22→27 确认 Batch X 的 5 条都存在，
  即使排序把两条藏了起来）。**逐条点名核对，不要靠计数。**
- **`get_datafields` 不接受 `limit`**（schema 无该属性），但传了也被容忍；`offset` 被静默忽略。
- **`batch_create_simulations` 并发上限 ≈7**：Batch T 的第 8 条返回 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`
  （**槽位状态，不是表达式问题**）。本段 Batch X 取 5、Batch Y 取 5、Batch Z 取 6，均无 429。
- **`batch_create_simulations` 的爆炸半径是单腿，不是整批**（每条是独立的 multisim parent）。
  连坐 CANCEL 的风险属于「一个 settings 块里放多条表达式」的 `create_multi_simulation`。
- **大输出落两个不同目录**：`…\tool-outputs\session-<id>\mcp_call_*.txt` 与 `…\<session-id>\tool-results\wqb_db_*.txt`。
  `get_dead_ends(region="EUR")` 产出 ~72 643 tokens / 217 927 字符，**超 25 000 token 上限被自动持久化**，
  内联只剩 2 KB 预览 ⇒ **绝不要在没计划 grep 持久化路径的情况下调用它**。

### 39.18 本节取代的旧结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| §38.7 | 「四闸交集为空」（观察） | **升级为两斜率代数证明**（39.2），并指认 **prod 是唯一不可跨越的闸**；S/2Y/sub 三闸在 p∈[1.962,1.991] 内确实可同时满足 |
| §38.x | 「`country` 是唯一 prod 杠杆」 | **✗ 更正为「分组粒度」**（39.1）：`country` 的压 prod 幅度正比于其笛卡尔伙伴的细度 |
| §31.4 | 「嵌套分组：外层贡献恰为零 / 嵌套是死路」 | **过强，必须按 group 逐个限定**：对 outer `market`/`sector` 成立（prod Δ 0.0000/−0.0001，2Y Δ 0.00）；对含 `country` 的笛卡尔**不成立**（prod Δ −0.024~−0.157，2Y Δ **+0.24**）。其 `MP0L995a` 证据是 inner-zscore 测量，不可推广 |
| §38.9 | `analyst_factor_signals` 五重封闭 | **第三重作废**（把算子当替代枚举，从未当包裹枚举），见 39.9 推论 |
| 台账 `EUR-COUNTRY-EXCHANGE-SECTOR-GROUPING-DEAD` | 「不要用 country/exchange/sector 分组；market 预期已死、最低优先」 | **✗ 对 outer 位置否证**（39.8）。被封存条目列为「最低优先」的 `market` 产出了战役唯一全 RA 闸 + ATOM 2Y 通过的候选 |
| 台账 `EUR-NONMODEL-TOWER-CEILING` | 「EUR 非 MODEL 塔信号强度天花板 0.3–0.4」 | **塔级断言作废**：analyst 塔实测 S 1.73–1.90（其 `analyst45` 具体读数可能仍成立） |
| 台账 `EUR-ANALYST10-PREDICTED-SURPRISE-DEAD` | 「analyst10 predicted-surprise 族关闭」（family 串含 "revision ratio"） | **范围不覆盖 `ratio_to_consensus` 形态**（39.15）：8/295 探针、测的是 `ratio_to_close`、TOPCS1600、未记录中性化 |
| 我的 αC 假设 | 「低 αC ⇒ 未开发机会 ⇒ 低 prod」 | **✗ 否证**（39.4）：αC 是**信号强度**代理，拥挤度内生于信号质量。但用它零槽位判死了 3 个 q1_1mo 字段 |
| 我的 T5 推断 | 「outer `cart(subindustry,country)` 保 sub 比率」 | **✗ 单字段假象**（39.6）：np_y2 上抬 +0.037，np_y1 上压 −0.036，eps_y1 上压 −0.081 |
| `wq-window-valley-break-prod-wall` | 「先平滑再找谷」 | **在本族是反的**：decay↑ 在 EUR **抬** prod（+0.00113/单位，本段复测），平滑方向与破墙方向相反 |
| 技能文档「破 prod 墙只有残差化一条路」 | — | **四重否证**：N3、T4 的组合轴、`country`/粒度发现、以及 39.8 被否证的分组判死 |

---

## §40 Batch Z 全灭、跨数据集去相关定律（clique=3 推翻 clique=1）、以及目标步 4 的算术终局

> 2026-10-19/20 夜。本节收割 Batch Z（`analyst10` 修正族 6 腿，全灭）、
> 用 `compute_mutual_correlation` 做出**战役首次跨数据集去相关测量**（结论推翻 §39.10 的 clique=1）、
> 完成目标步 1 的第 5 条枚举通道并测出它的上限、并给出目标步 4 的**算术终局**。
> Batch AA（积分假设 5 腿）已派发，读数待收。

### 40.1 Batch Z 完整读数（6/6 全部判死；`analyst10` 修正族在第二个设置档上亦死）

设置：EUR / TOP2500 / D1 / **decay 20** / **FAST** / trunc 0.08 / FULL / 2014-01-01→2023-12-31。
配方 = V5 的已验证形态 `group_neutralize(signed_power(group_zscore(<F>, industry), 1.8), market)`。

| tag | alpha | 字段 | 变体 | S | F | TO | returns | DD | margin | long/short | pnl | sub | 比率 | 2Y | `failed_ra` | CLUSTER |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| **Z1** | `gJW9rJKv` | `anl10_netrevise_ratio_to_consensus_fy2` | V5 配方 | **0.15** | 0.03 | .2602 | .0099 | .1511 | .000076 | 1340/1480 | 1 024 880 | 0.10 | .667 | 0.25 | 3 | 1.40 |
| **Z2** | `P0MOPqEK` | 同上 | **裸**（无 outer） | **0.16** | 0.03 | .2605 | .0107 | .1463 | .000082 | 1339/1480 | 1 102 395 | 0.11 | .6875 | 0.25 | 3 | 1.40 |
| **Z3** | `leM3geZn` | 同上 | `ts_delta(F,60)` | **0.07** | 0.01 | **.3037** | .0057 | .2341 | .000038 | 1390/1430 | 591 129 | 0.16 | — | **−0.33** | 4 | 0.48 |
| **Z4** | `A1Q7LRGe` | `anl10_ebirevise_ratio_to_consensus_fy1` | V5 配方 | **0.03** | 0.00 | .2682 | .0025 | .2670 | .000018 | 1396/1423 | 254 776 | **−0.24** | — | 0.37 | 4 | 1.11 |
| **Z5** | `LL5d8OM9` | `anl10_ebtrevise_ratio_to_consensus_fy1` | V5 配方 | **0.09** | 0.01 | .2627 | .0066 | .1481 | .000050 | 1368/1452 | 683 281 | **−0.08** | — | −0.03 | 5 | 1.05 |
| **Z6** | `xA1dlAzw` | `anl10_salrevise_ratio_to_consensus_fy2` | V5 配方 | **0.86** | 0.38 | .2718 | **.0540** | .1122 | .000397 | 1320/1499 | 5 567 999 | 0.49 | .570 | 0.80 | 3 | 1.56 |

**族内最好 S = 0.86（Z6，sales），全族 6/6 低于 1.58 硬闸 0.72 以上。** 无一条值得测 prod。
另有两条 `CONCENTRATED_WEIGHT` 硬失败：Z3 **0.414**（2016-12-30 单票 41% 权重 = 数据伪影）、Z5 **0.1025**（2014-01-02）。

**sub 系数 0.5196 又得三次活体确认**（TOP2500）：Z4 sub 限 0.02 = 0.5196×0.03｜Z5 限 0.05 = 0.5196×0.09｜Z2/Z3 因 S 太低而 sub 反过闸（0.11 > 0.078、0.16 > 0.036）。
⇒ **比率闸随 S 缩放，S 越低越容易过 sub**，这条在 S<0.2 的垃圾区制造「pass」假象，读数时必须连 S 一起看。

### 40.2 ★★ 预登记预测逐条裁决（Z1 错一个数量级；Z2/Z3 方向被确认）

| 腿 | 预登记预测 | 实测 | 裁决 |
|---|---|---|---|
| Z1 | S 1.55–1.80、2Y 1.90–2.15、比率 .50–.54、**prod 0.45–0.62 ⇒ 战役首个全过** | S **0.15**、2Y **0.25** | **✗ 严重否证，差一个数量级**。比率 0.667 反而「过」——但是因为 S=0.15 把闸线拉到 0.078（40.1 末） |
| Z2 | S 与 Z1 差 ≤0.02、prod 差 ≤0.005 | S 0.16 vs 0.15，**Δ=0.01** | **✓ 确认**：outer `market` 近似 no-op 的定律**跨数据集迁移成立**（§39.3 的第 4 次验证） |
| Z3 | S 低于 Z1、但比率高于 Z1 | S 0.07 < 0.15 ✓、sub 0.16 > 0.10 ✓ | **✓ 方向双双确认**（水平虽都是垃圾）。且 **Z3 ≪ Z1 ⇒ 按预登记的语义判据，字段*已经是*修正量** |
| Z4/Z5/Z6 | S 1.30–1.70 | 0.03 / 0.09 / **0.86** | **✗ 否证**。仅 sales 有一点生命 |

**「机制同构 ⇒ 强度可迁移」这条推断被彻底否证。** Z1 的字段与战役赢家 `netprofit_y2_estimate_change_3mo`
是**同一经济量**（净利润修正）、**更高覆盖**（0.9975 vs 0.9269）、**25 倍更低拥挤**（αC 2 vs 51），
我据此预测 S 1.55–1.80；实测 **0.15**。
⇒ **同构性不能跨数据集迁移强度**。§39.4 记录的张力（「αC 2 按定律该弱，但我押机制同构」）**由机制同构一方输掉**。

### 40.3 ★★★ 真正的区分变量是**换手率**，而它**可从字段名先验筛出**（新的 S0 级规则）

| 族 | TO | returns | 最好 S | 字段名特征 |
|---|---:|---:|---:|---|
| `analyst_factor_signals` 的 `*_estimate_change_3mo` | **0.064–0.070** | 0.050–0.107 | **1.90**（T3）/ 1.83（X3） | **名字里带显式窗口 `_3mo`** |
| `analyst10` 的 `*revise_ratio_to_consensus_*` | **0.260–0.304** | 0.003–0.054 | **0.86** | **裸 `revise_*` 比率，无窗口后缀** |

TO 相差 **4 倍**。机制：`_3mo` 后缀**本身就是平滑窗**——该字段是「3 个月的变化」，天生低频；
而 `revise_ratio_to_consensus` 是**日频共识修正比率**，未平滑，噪声主导。
⇒ **可先验筛选的 S0 规则（零槽位）：字段名带显式平均窗（`_3mo`/`_30d`/`_90d`/`_126`…）⇒ 已预平滑，低 TO、高 S；
裸 `revise_*` / `ratio_to_*` 日频比率 ⇒ TO 约 4 倍，信号被噪声吃掉。这条比 αC 好用得多，且开波前即可判定。**
（αC 在本族**也不成立**：族内 αC 2→0.15、3→未测、7→**0.86**、11→0.03、18→0.09，非单调。
⇒ αC↔强度定律**只在同一数据集内、同一机制族内**有效，跨数据集失效。**这是对该定律适用范围的收紧，第 5 次「斜率不迁移」**。）

### 40.4 ★★ 语义消歧已解：`revise_ratio_to_consensus` 是**一阶差分**，所以正确的时间算子是**积分而非差分**

§39.16 提出两种可能构造：(a) 修正量 ÷ 共识（**已是**修正量）、(b) 估计值 ÷ 共识（水平比，1.0 = 符合预期）。
描述文本无法裁决（已证不可靠）。**Z3 裁决了它**：`ts_delta(F,60)` 使 S 从 0.15 掉到 **0.07**、2Y 从 0.25 掉到 **−0.33**、
并炸出 `CONCENTRATED_WEIGHT 0.414`。
⇒ **按预登记判据「Z3 ≪ Z1 ⇒ 字段已经是修正量，差分是二次差分（过度差分）」——构造 (a) 成立。**
**推论（驱动 Batch AA）**：既然字段是一阶差分，而赢家字段是**3 个月窗口**，那么从裸修正比率重建赢家的正确算子是
**`ts_mean(F, ~63)`（积分）**，不是 `ts_delta`（差分）。**我把时间算子的方向搞反了，Z3 就是这次归因的证据。**
这正是目标步 3 要求的「一两闸不过时先归因再推进不要盲扫」。

### 40.5 ⚠ 隐藏悬崖：本族 TO 正压在**控制 ATOM 放宽系数的 30% 阈值**上

平台原文（§38.5）：*「If the turnover of Alpha is less than 30%, the IS Sharpe Ladder PASS_THRESHOLDS are multiplied by a factor of 0.85.」*
⇒ **ATOM D1 线 = 2.38 × 0.85 = 2.023，且只在 TO < 30% 时成立。**
Batch Z 实测 TO：Z1 .2602｜Z2 .2605｜**Z3 .3037**｜Z4 .2682｜Z5 .2627｜Z6 .2718。
**Z3 已越过 30%**，其余 5 条距阈值仅 0.03–0.04。
⇒ **本族的 ATOM 线不是 2.023 而是随时可能跳回 2.38（+17.6%）**。这是个此前未登记的悬崖：
`analyst_factor_signals` 族 TO 0.065–0.070，距阈值 0.23，安全余量 3 倍以上；`analyst10` 裸修正族余量近乎为零。
**任何在本族上的改进，若把 TO 抬过 0.30，会同时把 ATOM 闸线抬高 18%——双重惩罚，且不会有任何错误信息提示。**

### 40.6 `analyst10` 封存条目的处置：范围异议成立，但结论是**扩大**封存而非推翻

§39.15 论证了 `EUR-ANALYST10-PREDICTED-SURPRISE-DEAD` 的四条范围限制（8/295 探针、测的是 `ratio_to_close`、
TOPCS1600、未记录中性化）⇒ 跑 Batch Z **不是**重走封存路径。这个论证**成立**，6 个槽位花得正当。结果：

- 我在 TOP2500/FAST 测得族内最好 **S 0.86**，**高于**封存条目在 TOPCS1600/SUBINDUSTRY 的最好读数 **0.64**
  ⇒ **§30.6 元教训再次成立**（换设置档整体平移读数），且方向是「更好的档给出更好的数」。
- 但 0.86 仍距 1.58 硬闸 **0.72** ⇒ **封存条目的*判决*在第二个设置档上被独立证实**，
  其*范围*缺口（`ratio_to_consensus` 未测）现已补齐并判死。
- ⇒ **正确处置 = 把封存范围从「predicted-surprise 族」扩大到「`analyst10` 全部 `*revise_*` 族（含 `ratio_to_close` 与 `ratio_to_consensus` 两种缩放）」，
  并补记 TO 0.26–0.30 与 40.5 的 30% 悬崖作为机制解释。** 这需要在台账新增条目（`seal_dead_end` 是 fail-closed 单向、无解封路径 ⇒ 人工决定）。

### 40.7 ★★★ 战役首次**跨数据集**去相关测量：clique = **3**，推翻 §39.10 的 clique = 1

`compute_mutual_correlation`（**完全本地**：`local_calculation true`、`num_points 1021`、`years 4`、`missing_pnl []`、**零槽位**），
池 = V5 `YPxg1LzM`(np_y2) · W3 `RRA1EaQn`(np_y2,p2.0) · V3 `zqrR3AWo`(np_y2) · X3 `58jkE1vX`(np_y1) · X5 `wp9EQAWx`(eps_y1) · **Z6 `xA1dlAzw`（`analyst10` sales）**：

| | V5 | W3 | V3 | X3 | X5 | Z6 |
|---|---:|---:|---:|---:|---:|---:|
| **V5** | 1 | .9938 | **.9986** | **.4720** | **.3874** | **.0458** |
| **W3** | | 1 | .9948 | .4420 | .3601 | .0347 |
| **V3** | | | 1 | .4735 | .3890 | .0451 |
| **X3** | | | | 1 | **.7293** | .0564 |
| **X5** | | | | | 1 | .0690 |
| **Z6** | | | | | | 1 |

`max_pair` = V5×V3 **0.9986**｜`pairs_over_threshold` = 4 对｜`all_below_threshold false`｜
**`max_mutually_below_subset` = {V5, X3, Z6}，size = 3**｜`max_subset_exact true`。

**⇒ §39.10 的「clique = 1」是在一个更紧的池（7 条最优腿，多为同字段的不同组合）上测得的，不是普适上限。**
本池给出 **3**。两个结论不矛盾，但**必须写明池的构成**——这是 §30.6/§39.9 元定律的又一实例：
「clique 数」是**池的函数**，不是数据集或区域的属性。

**★★★ 新的去相关层级顶格（完整表）：**

| 轴 | 实测相关 | 出处 |
|---|---:|---|
| 设置档（中性化/decay/universe） | 0.72–0.99 | §32.2 |
| 组合（outer 包裹 / p 值） | 0.75–0.99 | §32.2 |
| **同字段 + 不同 outer group** | **0.9938–0.9986** | 本节 V5×V3×W3 |
| 桶化（bucket） | 0.8482–0.9972 | 已杀杠杆表 |
| 同族不同字段（y1 vs y2 / net vs eps） | 0.3874–0.7293 | 本节 |
| 字段族（跨机制，同数据集） | 0.3187–0.4184 | §32.2 |
| **跨数据集** | **0.0347–0.0690** | **本节（首次测量）** |

⇒ **换数据集比换字段族强 6–8 倍，近乎完全正交。** Z6 与全部 5 条 `analyst_factor_signals` 腿的相关是 **0.035–0.069**。
**这条把「N 颗 alpha = N 个不同字段」的旧配方升级为「N 颗 alpha = N 个不同*数据集*，其次才是不同字段」。**
⚠ 但它同时说明：**正交性不是稀缺资源**（0.046 的相关几乎是免费的），**过闸强度才是**。

### 40.8 ★★ 预测期 > 指标：去相关轴的次序，且 §39.7 的机制定律**预测出了**这张相关矩阵

同数据集内三对读数：

| 对 | 关系 | 相关 |
|---|---|---:|
| X3 (np_**y1**) × X5 (eps_**y1**) | **同期不同指标** | **0.7293**（超阈） |
| V5 (np_**y2**) × X3 (np_**y1**) | **同指标不同期** | **0.4720** |
| V5 (np_**y2**) × X5 (eps_**y1**) | 不同指标不同期 | 0.3874 |

⇒ **在 `analyst_factor_signals` 内，预测期（y1 vs y2）是比指标（netprofit vs eps）更强的去相关轴。**
这与直觉相反（直觉：同指标不同期应更相关）。**而 §39.7 的机制定律正好预测了它**：

- §39.7 实测：去掉 subindustry 均值时 np_**y1** 损失 **0.70 S**、eps_**y1** 损失 **0.49 S** ⇒ 两者的 Sharpe 主要住在 subindustry **之间**；
  np_**y2** 只损失 **0.25 S** ⇒ 它的 Sharpe 主要住在 subindustry **之内**。
- ⇒ **两个 y1 字段共享同一个行业轮动分量（故 0.7293），而 y2 是特异性的（故与两个 y1 都只有 0.39–0.47）。**

**两批独立实验（Batch Y 的层级定律、本节的去相关矩阵）互相印证 ⇒ §39.7 从「模式」升级为「机制」。**
可复用推论：**要造互不相关的多腿，先按「信号住在行业层级的哪一层」分组，再在层内换指标。**

### 40.9 一条可证明的恒等式，省掉一个槽位

`ts_sum(x,d) = d × ts_mean(x,d)`，而 `group_zscore` 对正尺度不变
⇒ **`group_zscore(ts_sum(x,d), g) ≡ group_zscore(ts_mean(x,d), g)` 逐字节相同**。
Batch AA 原计划的 `ts_sum` 腿据此**取消**，槽位改投窗口轴。
（同族恒等式清单第 4 条；前三条：`densify(cart(market,country)) ≡ country`〔§39.3〕、
`exchange ≈ country`〔§39.3〕、`-signed_power(gz(x,g),p) ≡ signed_power(gz(-x,g),p)`〔Batch G2〕。）

### 40.10 目标步 1 的第 5 条枚举通道：可用，但**上限 100 且不能翻页**

`get_datafields(dataset_id=null, search="analyst recommendation", region="EUR", universe="TOP2500", delay=1, data_type="MATRIX")`
→ **`count` 恰好 100**（`search="estimate"` 给 99）。**恰好 100 = 触顶截断**，而 `offset` 被静默忽略（§39.17）
⇒ **无法翻页**。这是第 5 条通道的固有上限，与 `get_datasets`（完全不列 analyst）、`recommend_datasets`（top-50 零 analyst）、
`get_dead_datasets`（4 个）、`get_field_catalog`（必须给 dataset 名）并列。
**⇒ 目标步 1 的「全部 Analyst 数据集逐一扫描」在 API 上不可完成**：`_dataset-inventory.md` L17 记 EUR 有 **16** 个 analyst 数据集，
但其 ID 被刻意省略（L70「已点亮类别不列」），而五条枚举通道**没有一条能列全**。
本战役实际触达 4 个：`analyst_factor_signals`、`analyst4`、`analyst10`、以及一个新发现的 **`model26`**（`mdl26_` 前缀，
不在任何本地清单、不在任何 `get_datasets` 结果里）。

**推荐族的普查结果（同一机制在两处、拥挤度相反）：**

| 群 | 代表字段 | cov | uC | αC | 归属 |
|---|---|---:|---:|---:|---|
| **未拥挤**（αC 0–30） | `analyst_recommendation_upgrades/downgrades_*`（cov .7511 / **.9616**）、`count_analyst_recommendation_*`（.7507）、`avg_change_analyst_recommendation_*`（.7268–.7294）、`analyst_opinion_avg_shift_*`（.7251–.7298）、`analyst_upgrade/downgrade_count_*d_N`（.9491 / .7561）、`mean_analyst_recommendation_*`（.9466–.9488） | .72–.96 | 0–20 | **0–30** | analyst 类数据集 |
| **已拥挤**（αC 100–2721） | `star_arm_rec_mean_prior7`（**αC 2721 / uC 263**）、`star_arm_recommendations_score`（αC 416 / uC 155）、`star_arm_rec_mean_change30`（αC 212）、`mdl26_rcmmndtn_mn_chng_14`（αC 165 / uC 56）、`mdl26_recommendations`（αC 132 / uC 61）、`mdl26_num_downgrades_14`（αC 107 / uC 26） | .88–.96 | 26–263 | **100–2721** | StarMine / `model26` |

⇒ **★ 可复用的 S0 规则（比 §39.4 的 αC 定律更强，因为它跨数据集作用于*同一机制*）：**
**当一个机制同时出现在「未拥挤的 analyst 数据集」与「已拥挤的 model/StarMine 数据集」时，
这个拥挤度*不对称本身*就是证据——信号是真的，但只在已拥挤的那份里可提取；
未拥挤的那份之所以未拥挤，是因为它不工作。** 本战役已 7 次在 `analyst_factor_signals` 内验证 αC↔强度，
这里是它的第一次**跨数据集、同机制**验证。
⇒ 且两个已拥挤宿主都不可用：StarMine 族已封存（`EUR-STAR*`、`EUR-STARHOLD-*`、`EUR-STARMINE-SIBLING-PROD-WALL`），
`model26` 是 **model 类**（EUR/D1/model 已有 2 颗）。**推荐族对 ATOM analyst 目标关闭。**

### 40.11 ⚠ `batch_status` 的第 4 种行为：`parent COMPLETE` + children empty **可以真的没有 alpha**

Y1（`2EGQZL4tC4Hw9RG16nvAm60S`，np_y2 × cart(sub,country) × p1.8）派发已逾 1 小时，
本轮 `batch_status` 报 `parent_status:"COMPLETE"`、`child_count:0`、`error:"parent COMPLETE but children empty"`。
而 `get_user_alphas` 的 `count` 从 **31 → 37 = +6**，**恰等于 Batch Z 的 6 条** ⇒ **Y1 没有产出任何 alpha。**

⇒ **§39.17 记的「假警报形态」是*双向歧义*的**：同一个 `parent COMPLETE + children empty` 形态，
在 Batch Y 的 Y3 上**有** alpha（且那条报的是 `parent_status:"ERROR"`），在 Y1 上**没有**。
**唯一可靠的裁决是 `get_user_alphas` 的 `count` 增量 + 逐条点名核对表达式文本。**
四种行为汇总：(a) `null` + `all_terminal:false` = 诚实地还在跑；(b) `COMPLETE` + children empty = **歧义，须查 count 增量**；
(c) `ERROR` + 通用平台错误串 = **仍可能有完整 alpha**（Y3 `zqrRdjdE`）；(d) 真 COMPLETE 且有 alpha。
**⇒ `parent_status` 的任何取值都不是终局，`all_ok` 与 `errors` 一律忽略。**

**Y1 的零槽位判死（不重派）**：Y3（同格 p2.0）S=1.38；实测 p1.8→2.0 的斜率是 −0.09 S / −0.07 2Y（§39.2）
⇒ Y1 ≈ S **1.47**（差 0.11）、2Y ≈ **1.96**（差 0.06）⇒ **两闸皆不过**。其格子被 Y3 与 V5 双向夹死，重派无信息量。

### 40.12 Batch AA：积分假设（5 腿，已派发 5/5 `ok:true`）

归因（40.4）：字段是一阶差分 ⇒ 重建「3 个月窗口」的正确算子是**积分**。窗口轴 {21, 63, 126} 打在族内最强的 Z6 字段上。
设置与 Batch Z 逐字相同（decay 20 / FAST / TOP2500 / trunc 0.08）。

| tag | sim id | 表达式要点 | 检验什么 |
|---|---|---|---|
| AA1 | `3VbhdZG34Bz9ByN50M3x8e` | `ts_mean(salrevise_cons_fy2, **63**)`, inner industry, outer market | 63 交易日 ≈ `_3mo`，**同构窗** |
| AA2 | `3aOCZr2vw4p691797rk2LjJ` | 同上，窗 **21** | 窗口轴短端 |
| AA3 | `3Xnp2O2uM5cDajjFny9kStG` | 同上，窗 **126** | 窗口轴长端 |
| AA4 | `3S3OmC9la51O8N6AT43iLIY` | `ts_mean(**netrevise**_cons_fy2, 63)` | 积分能否救活机制同构字段（Z1 原始 S 0.15） |
| AA5 | `Tc2BA1c24JRb9xWwMWvXyT` | 同 AA1 但 inner **subindustry** | §39.7 层级定律在 sales-fy2 上的位置未知 |

**预登记预测（派发时形成，未回填）：** AA1 S **1.10–1.60**、2Y 1.00–1.60、TO **0.10–0.18**、比率 0.55–0.65
（依据：积分去日频噪声；Z6 的 0.86 是噪声地板；赢家字段本身就是 3 个月窗。但 +0.72 S 是大要求，故上界取 1.60 不取 1.80）。
AA2 S 低于 AA1、TO 高于 AA1。AA3 S ≈ 或略高于 AA1、TO 远低于；**若 AA3 的 S 反而低于 AA1 ⇒ 信号就在 ~63 日视界**（与 `_3mo` 同构）。
AA4 S **0.30–0.90**：若 AA4 ≫ AA1 ⇒ 指标比我以为的重要；若 AA4 ≪ AA1 ⇒ sales 是本数据集唯一活的指标。
AA5 比率高于 AA1、S 低于 AA1。
**整族否证判据：若 max(AA1..AA5) 的 S < 1.0 ⇒ 积分不能在本族重建信号，`analyst10` 修正族在第二个设置档*与*第二个时间算子上双双判死， definitively 关闭。**

#### 40.12b 派发后才做的 F 闸算术（**不回填预测**，登记在此以免下次重犯顺序错误）

`returns = max(TO, 0.125) × (F/S)²` ⇒ `F = S × sqrt(returns / max(TO,0.125))`。
Z6 实核：`sqrt(0.054/0.2718) = 0.4458` ⇒ `F = 0.86 × 0.4458 = 0.383` ✓ 与实测 0.38 吻合。

- **Z6 现状下 F 是绑定闸而非 S**：要 F ≥ 1.0，在 returns/TO 比不变时需 **S ≥ 2.243**（比 S 闸的 1.58 高得多）。
- **但 Z6 的 returns 0.0540 已经高于 S=1.58 时的 F 闸地板 0.0501**（`= 0.125 × (1/1.58)²`）。
  ⇒ **只要积分把 TO 压到 0.125 以下，F 闸自动修复**：`F = 1.58 × sqrt(0.054/0.125) = 1.038 ≥ 1.0 ✓`。
  **积分降 TO ⇒ F 闸自愈，绑定闸退回 S 与 2Y。** 这是本批最有希望的算术结构。
- **剩下 2Y 是硬骨头**：0.80 → 2.023 需 **+1.22**，比 S 的 +0.72 难得多。故 40.12 的否证判据（S < 1.0 即关闭）是恰当的保守线。
- ⚠ **顺序教训**：这段算术**应当在派发前做**——它会让我把 AA2（21 日窗，TO 最高、最可能仍 >0.125）换成
  **一个 decay 抬高的腿**，从而同批检验「TO 压到 0.125 以下」这个 F 闸自愈条件。**下次派平滑批前先算 F 闸地板。**

### 40.13 ★★★ 目标步 4 的算术终局：**可交付上限 = 1，且以一次不可逆提交为条件；10 不可达**

三条独立约束合起来给出终局，**不需要任何进一步回测**：

1. **过全部 8 条 API 可见 RA 闸 + ATOM 2Y 线的腿，全战役只有 V5 `YPxg1LzM`。**
   W3 `RRA1EaQn` 也 `failed_ra_count 0`，但 2Y **2.02 < 2.023** ⇒ 差 0.003 不过 ATOM。
   其余全部候选至少缺 1 条：X3 缺 2Y(1.68)、X5 缺 sub(.4457)、Y3 缺 S(1.38)、U2 缺 2Y(1.73)、T3 缺 sub(.3947)、Z6 缺 S/F/2Y。
2. **V5 缺 prod（0.7398，超 0.0398），且 §39.2 已*代数证明*四闸交集为空**（S≥1.58⇒p≤2.111｜2Y≥2.023⇒p≤1.991｜
   比率≥0.51961⇒p≥1.962｜prod<0.7⇒p≥2.146 ⇒ 前三闸在 p∈[1.962,1.991] 可同满足，**prod 要求的区间与之不相交**）。
   prod 直方图 `[0.7,0.8)` 桶 **n=3**（V3/V5/V7）、W3 **n=1** ⇒ 按 `wq-window-valley-break-prod-wall` 自己的判据（n≥1 必死）**族级必死**。
3. **V5 与 W3 是同一字段 ⇒ 实测互相关 0.9938**（40.7）⇒ 即使两者都过闸，`SELF_CORRELATION` 也会拦下第二颗。
   而 40.7 的 3-clique {V5, X3, Z6} 里，X3 与 Z6 都不过闸。

⇒ **可交付上限 = 1 颗（V5），且唯一的过 prod 路径是平台「Sharpe 比在位相关 alpha 高 ≥10%」豁免条款**
（V5 的 S 1.73 对任何 S ≤ 1.573 的在位者成立），**而该条款只能用一次不可逆提交来验证**——
在位者身份与 Sharpe 在 API 上不可读（`get_record_sets` 无相关性记录集，`PROD_CORRELATION` 恒 `pending`）。
**这属于红线：必须用户明确确认，任何 waiver 无效。**

**⇒ 「10 个通过验证的 ATOM regular alpha」在可达空间内不可达，且与 prod 无关：**
`analyst_factor_signals` 只有 **9** 个 `estimate_change` 字段（已全量枚举，§39.11），同字段组合相关 0.99 ⇒ 上限 9 颗互不相关者；
其中 **6 个已测、全过率 0**，另 3 个 q1_1mo 字段被 αC + 覆盖率双双最低而零槽位判死。
`analyst10` 修正族 6/6 判死（40.1）。**12/16 个 EUR analyst 数据集在 API 上枚举不到（40.10）。**
**塔位算术另加一道**：EUR/D1/ANALYST 现有 **1** 颗，点亮阈值 **3** ⇒ **再提交 2 颗即点亮**，
触发锁定项「已点亮塔不作主数据集」，与「10 颗全 analyst」直接冲突。

### 40.14 本节取代的旧结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| §39.10 | 「7 腿池 `max_mutually_below_subset_size = 1`」 | **不是普适上限，是池的函数**：6 腿池给出 **3**（40.7）。引用 clique 数必须同时写明池的构成 |
| §32.2 | 「字段族是最强去相关轴（0.3187–0.4184）」 | **降级为第二**：**跨数据集 0.0347–0.0690** 强 6–8 倍（40.7）。配方升级为「N 颗 = N 个不同*数据集*」 |
| §39.4 | αC 是信号强度代理 | **适用范围收紧**：只在同数据集同机制族内成立；跨数据集**非单调**（`analyst10` 族 αC 2→0.15、7→0.86、11→0.03、18→0.09）（40.3） |
| §39.16 | 「Z1 若成立即战役首个全过」 | **✗ 严重否证**，S 0.15（40.2）。「机制同构 ⇒ 强度可迁移」这条推断作废 |
| §39.15 | 「`analyst10` 封存范围不覆盖 `ratio_to_consensus`」 | **范围异议成立，但结论是扩大封存**：TOP2500/FAST 下族内最好 S 0.86，仍差硬闸 0.72（40.6） |
| §39.17 | 「`parent COMPLETE` + children empty 是假警报形态」 | **双向歧义**：Y1 在该形态下**真的没有 alpha**，靠 `count` 增量 31→37=+6 裁决（40.11） |
| 我的 Z3 设计 | 用 `ts_delta` 检验字段语义 | **方向搞反**：字段已是一阶差分，正确算子是积分（40.4）。Z3 的失败本身就是归因证据 |
| （未登记） | ATOM D1 线 = 2.023 | **有前提**：仅当 TO < 30%。`analyst10` 裸修正族 TO 0.26–0.30，Z3 已越线 ⇒ 该族 ATOM 线随时跳回 **2.38**（40.5，新登记的悬崖） |
| （未登记） | 派平滑批的经验 | **新增纪律**：派平滑批前先算 F 闸地板 `0.125×(1/S)²`；TO 压过 0.125 会让 F 闸自愈（40.12b） |

---

## §41 Batch AA 收割：信号是纯日频现象、F 闸自愈论被否证、`analyst10` 修正族从两个时间算子方向双双封死

> 2026-10-20 凌晨。本节收割 Batch AA（积分假设 5 腿，5/5 判死），
> **触发 §40.12 的预登记否证判据**（max S 0.38 ≪ 1.0），
> **否证我自己写在 §40.12b 的「F 闸自愈」算术**，并产出 6 条新定律。
> 至此 `analyst10` 修正族在**第二个设置档**（TOP2500/FAST/d20）×**两个时间算子方向**（差分 Z3 / 积分 AA1–AA3）上双双判死。

### 41.1 Batch AA 完整读数（5/5 判死）

设置同 40.1（EUR / TOP2500 / D1 / decay 20 / FAST / trunc 0.08 / FULL / 2014-01-01→2023-12-31）。
配方 = `group_neutralize(signed_power(group_zscore(ts_mean(<F>, W), <inner>), 1.8), market)`。

| tag | alpha | 字段 / 窗 / inner | S | F | TO | returns | DD | margin | long/short | pnl | sub | sub 限 | 2Y | `failed_ra` | CLUSTER |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| **AA1** | `JjPv3kxm` | salrevise_fy2 / **63** / industry | **0.14** | 0.03 | .0681 | .0071 | .1887 | .000209 | 1014/1806 | 735 247 | −0.48 | 0.07 | −0.86 | 4 | 0.61 |
| **AA2** | `78onGrZL` | salrevise_fy2 / **21** / industry | **0.27** | 0.09 | .0896 | .0125 | .2325 | .000279 | 1046/1773 | 1 290 423 | −0.25 | 0.14 | −0.80 | 4 | 1.04 |
| **AA3** | `d5KR9oKg` | salrevise_fy2 / **126** / industry | **−0.04** | 0.00 | .0614 | −.0018 | .2100 | −.00006 | 966/1853 | **−189 797** | −0.38 | −0.02 | −1.37 | 4 | 0.19 |
| **AA4** | `qME65p02` | **netrevise**_fy2 / 63 / industry | **0.33** | 0.13 | .0730 | .0203 | .1629 | .000555 | 1166/1654 | 2 092 762 | −0.33 | 0.17 | **0.70** | 4 | 0.38 |
| **AA5** | `58jkG21M` | salrevise_fy2 / 63 / **subindustry** | **0.38** | 0.13 | .0580 | .0137 | .0935 | .000471 | 1126/1693 | 1 409 452 | −0.38 | 0.20 | −0.38 | 4 | 0.29 |

**族内最好 S = 0.38（AA5），5/5 低于 1.58 硬闸 1.20 以上；`failed_ra` 全部 = 4 ⇒ 按 §39.13 全部 `submit_verdict` 层判死，不必花相关性调用。**
AA3 的 pnl 为**负**（−189 797）、returns 为**负**（−0.0018）⇒ 126 日窗把信号翻成噪声。

**sub 系数 0.5196 再得五次活体确认**（TOP2500）：0.07 = 0.5196×0.14｜0.14 = 0.5196×0.27｜−0.02 = 0.5196×(−0.04)｜0.17 = 0.5196×0.33｜0.20 = 0.5196×0.38。
**F 闸反算式再得五次逐字验证**（含一条负 returns 腿）：AA1 `0.14×sqrt(.0071/.125)=0.0334`✓｜AA2 `0.27×sqrt(.0125/.125)=0.0854`✓｜AA3 `→0.00`✓｜AA4 `0.33×sqrt(.0203/.125)=0.1330`✓｜AA5 `0.38×sqrt(.0137/.125)=0.1258`✓。

### 41.2 ★ 定律 1：窗口轴在本族对 S **单调反向** ⇒ 信号住在**日频**，平滑是摧毁而非去噪

| 窗（sales fy2） | 无窗（Z6 裸） | 21（AA2） | 63（AA1） | 126（AA3） |
|---|---:|---:|---:|---:|
| S | **0.86** | 0.27 | 0.14 | **−0.04** |
| 2Y | **0.80** | −0.80 | −0.86 | −1.37 |
| short/long | **1.136** | 1.695 | 1.781 | **1.918** |

两条**同轴单调**序列：窗越长，S 越低、空头倾斜越重。
⇒ **`anl10_salrevise_ratio_to_consensus_fy2` 的信号住在高频分量里。**
这与 `analyst_factor_signals` 的 `*_estimate_change_3mo` 族**完全相反**——那一族窗口*就是*信号本身。

### 41.3 ★★★ 双向封死：差分（Z3）与积分（AA1–AA3）都单调摧毁信号 ⇒ 字段既不是水平、也不是可积分流

- 差分：`ts_delta(F,60)` S 0.15→**0.07**、2Y 0.25→**−0.33**、`CONCENTRATED_WEIGHT` **0.414**（Z3，40.4）。
- 积分：`ts_mean(F,W)` S 0.86→0.27→0.14→−0.04（41.2）。
⇒ **两个方向都单调变差，信号恰好只在日频视界上存在。**

**⚠ 这同时回溯削弱了 §40.4 的语义消歧。** 当时的预登记判据「Z3 ≪ Z1 ⇒ 字段已经是一阶差分」
**不能区分**两种构造：(a) 字段是一阶差分，再差分 = 过度差分；(b) 字段是**水平偏离**，其变化量本来就更噪。
两者都预测 Z3 ≪ Z1。**能区分的是积分方向**：若为 (b)（水平型），`ts_mean` 应当*提升* SNR；实测单调摧毁 ⇒ **排除 (b)**。
若为 (a) 且是**干净可伸缩（telescoping）的日频差分**，则 `ts_sum(F,63)` 应约等于「63 日水平变化」= 厂商 `_3mo` 构造，
而 `group_zscore` 正尺度不变（40.9 恒等式）⇒ AA1 应当接近 S 1.73 的赢家；实测 **0.14** ⇒ **也排除干净的 (a)**。
⇒ **结论（构造 (c)）：该字段是一个*归一化比率*，其时间聚合不伸缩**——每日增量被当日共识缩放，
求和不还原成水平差。**因此本族无法用 `analyst_factor_signals` 的配方重建，「机制同构」在构造层面就不成立**（40.2 的强度层面否证在此得到机制解释）。

**★ 这条封死论证比「max S < 1.0」强得多**：它说明本族**被困住**——
唯一有信号的形态（裸日频）正是**坐在 §40.5 的 30% 换手悬崖上**（TO 0.260–0.304，Z3 已越线）、
且 S/2Y 差硬闸约 2 倍的形态；而任何把它移出悬崖的时间算子都按 41.2 摧毁信号。

### 41.4 ★★ 定律 2：§40.12b「TO 压过 0.125 ⇒ F 闸自愈」**被否证**；F 的可行改进区在膝点**以上**

§40.12b 的论证是：Z6 的 returns 0.0540 已高于 S=1.58 的 F 闸地板 0.0501，故积分把 TO 压到 0.125 以下即得
`F = 1.58×sqrt(0.054/0.125) = 1.038 ≥ 1.0 ✓`。**实测：TO 确实压到 .0681（AA1），但 returns 同步塌到 .0071**，
于是 `returns / max(TO,0.125)` 从 **0.1987（Z6）→ 0.0568（AA1）——变差 3.5 倍**，F 停在 0.03。

**机制（可复用的算术洞察）**：`F = S × sqrt(returns / max(TO, 0.125))`。

| 区间 | F 的形态 | 后果 |
|---|---|---|
| TO **>** 0.125 | 分母随 TO 变小 | TO 降得比 returns 快 ⇒ **F 改善**（唯一可行改进区） |
| TO **≤** 0.125 | **分母被冻结在 0.125** | 再降 TO **零收益**；此时 `F ∝ S×sqrt(returns)`，任何同时压低 S 与 returns 的杠杆是**双重 F 负** |

⇒ **新纪律（取代 §40.12b 那条）：任何把 TO 推过 0.125 膝点的平滑杠杆，按构造对 F 不利。
F 的改进只能在膝点以上找——让 TO 降得比 returns 快，而不是把 TO 降到最低。**
⚠ 这也**收紧了 §40.5 的悬崖读法**：30% 那条 ATOM 悬崖（TO<30% ⇒ ×0.85）与 12.5% 这条 F 膝点**之间**才是本区可操作带；
`analyst_factor_signals` 的 TO 0.064–0.070 **在膝点以下**，它能过 F 闸靠的是 returns 高（0.050–0.107），不是靠 TO 低。

### 41.5 ★ 定律 3：`ts_mean` 是强换手杠杆（−67%~−79%），并一次越过两个悬崖——但是场皮洛士胜利

| 腿 | 裸 TO | 平滑后 TO | 降幅 |
|---|---:|---:|---:|
| AA2（21） | .2718 | .0896 | −67.0% |
| AA4（netrevise 63） | .2602 | .0730 | −71.9% |
| AA1（63） | .2718 | .0681 | −74.9% |
| AA3（126） | .2718 | .0614 | −77.4% |
| AA5（63，inner subindustry） | .2718 | .0580 | −78.7% |

5/5 同时低于 **0.125 的 F 膝点**与 **30% 的 ATOM 放宽悬崖**（§40.5）⇒ 悬崖风险确实被解除了。
**但按 41.4，越过 F 膝点是负收益；按 41.2，信号同时被摧毁 ⇒ 两个悬崖都过了，闸却一条没过。**

### 41.6 ★ 定律 4：平滑修正比率 ⇒ 字段变成水平型 ⇒ 继承水平族的**空头倾斜病理**（机制上统一了 Batch P）

short/long 从裸值 **1.136** 单调升到 **1.695 / 1.781 / 1.918**（41.2 表）。
Batch P 的 `consensus_value` 水平/分歧度腿是 **2.192 / 2.588 / 2.661**（770/2049、786/2034、883/1936），
而战役赢家 V5 是 **0.919**（多头倾斜，1469/1350）。
⇒ **三者排成一条单调谱：裸修正比率（1.14）→ 平滑修正比率（1.7–1.9）→ 纯水平（2.2–2.7）**，
而**唯一过闸的形态在谱的另一端（0.92）**。
**这机制上统一了两件此前分开的事**：Batch P 观察到「EUR 的水平/分歧度族是被空头倾斜主导的稀释项」，
Batch AA 观察到「平滑摧毁修正比率」——**同一件事：在 EUR，平滑把任何修正型字段推向水平型，而水平型是稀释项。**

### 41.7 ★ 定律 5：§39.7 期界↔层级定律首次获得**跨数据集**确认

AA5（inner **subindustry**）S **0.38** > AA1（inner **industry**）S **0.14**，同字段同窗（sales fy2 / 63）。
inner `subindustry` 剔除了「industry 内的 subindustry 之间」分量、只留「subindustry 内部」分量 ⇒
**AA5 > AA1 ⇒ 留下的分量信号密度更高 ⇒ 信号主要住在 subindustry *内部*，subindustry *之间*的分量是稀释项。**
这与 §39.7 对 **2 年期界**（np_y2：外层含 subindustry 只损 0.25 S，而 np_y1 损 0.70）的结论**同向**，
且是该定律**首次跨数据集**确认（此前只在 `analyst_factor_signals` 内测得）。
⇒ **§39.7 从「模式」升级为「机制」的第二个独立证据。**

### 41.8 ★★ 定律 6：指标排序**随时间算子反转**（第 6 次「排序/斜率不迁移」）

| 形态 | sales fy2 | net fy2 | 胜者 |
|---|---:|---:|---|
| 裸（Z6 vs Z1） | **0.86** | 0.15 | sales（5.7×） |
| 平滑 63 日（AA1 vs AA4） | 0.14 | **0.33** | **net（2.4×）** |

⇒ **完全反转。** 这是本战役第 **6** 次同类失败（前五次：§37.2 非 FAST⇒低 prod、§38.3 prod↔sub 反相关、
αC 是机会代理、Batch Q 的 p 斜率跨中性化外推差 3 倍、§40.3 αC 跨数据集非单调）。
**元定律再加一例：任何在单一算子形态下测得的字段排序，不得跨算子形态外推。**

### 41.9 §40.3 `_3mo` 规则的**限定**：厂商窗 ≠ 自制窗，因为输入的**差分阶数**不同

§40.3 的规则是「字段名带显式平均窗 ⇒ 已预平滑 ⇒ 低 TO、高 S」。**Batch AA 给出了必要限定**：
厂商的 `_3mo` 是对**估计水平**做的长差分（`level(t) − level(t−63)`），平滑作用在一个「平滑有效」的量上；
自己对**裸修正比率**做 `ts_mean(F,63)` 作用在一个已经是比率/差分的量上，按 41.3 不伸缩 ⇒ 两者**不是同一操作**。
⇒ **限定后的规则（先判差分阶数，再选时间算子）**：

| 字段的差分阶数 | 名字特征 | 正确时间算子 | 禁忌 |
|---|---|---|---|
| **水平**（0 阶） | `*_consensus_value`、`*_level`、`consensus` | 平滑有效（去噪）；但 EUR 水平族是稀释项（41.6） | — |
| **长窗差分**（厂商已做） | 带 `_3mo`/`_90d`/`_126` 后缀 | **什么都不做**——窗口就是信号 | 再平滑、再差分 |
| **日频归一化比率** | 裸 `revise_*` / `ratio_to_*`，无窗后缀 | **只有日频形态可用**（41.3） | `ts_mean`（摧毁）、`ts_delta`（摧毁 + 炸 CW） |

### 41.10 预登记预测逐条裁决（4 否证 / 1 命中 / 2 方向错）

| 腿 | 预登记预测 | 实测 | 裁决 |
|---|---|---|---|
| AA1（63） | S **1.10–1.60**、2Y **1.00–1.60**、TO 0.10–0.18、比率 0.55–0.65 | S **0.14**、2Y **−0.86**、TO .0681、比率 **−0.48** | **✗ S/2Y/比率三项严重否证；仅 TO 方向命中**（且比预测更低，正是 41.4 的失效点） |
| AA2（21） | S **低于** AA1；TO 高于 AA1 | S **0.27 > 0.14**；TO .0896 > .0681 ✓ | **✗ S 方向错**（21 日优于 63 日）；TO ✓ |
| AA3（126） | S ≈ 或高于 AA1、TO 远低于；条件式「若 AA3 的 S 反而低于 AA1 ⇒ 信号就在 ~63 日视界」 | S **−0.04**、TO 最低 ✓ | **✓ TO；✗ S；条件式前件成立但解释作废**——因为 AA1（63 日）自身也是垃圾，「63 日视界」不是信号所在（41.2 显示信号在**日频**） |
| AA4（netrevise 63） | S **0.30–0.90** | S **0.33** | **✓ 命中（本批唯一落在预测区间内的一条）** |
| AA5（inner subindustry） | 比率高于 AA1 ✓；S 低于 AA1 | 比率 −0.38 > −0.48 ✓；S **0.38 > 0.14** | **✓ 比率；✗ S 方向错**（AA5 是 sales 腿里最好的一条） |

**方法论读数**：5 条里 4 条否证、2 条方向错，唯一命中的 AA4 是**区间给得最宽**的一条（0.30–0.90，跨 3 倍）。
⇒ **我对本族的强度预测能力接近零**；而 AA4 之所以命中，是因为我按 §39.4 的 αC 定律（而非机制同构）预测它弱。
**这与 40.2 的裁决一致：机制同构不能迁移强度，αC 只在同数据集内可用。**

### 41.11 `analyst10` 修正族的封存措辞（**扩大**范围；需新条目 + 人工确认）

§40.6 已裁定对 `EUR-ANALYST10-PREDICTED-SURPRISE-DEAD` 的正确处置是**扩大**封存。Batch AA 之后措辞应为：

> **family**: `analyst10` 全部 `*revise_*` 族（`ratio_to_close` **与** `ratio_to_consensus` 两种缩放）
> **×** 两个时间算子方向（差分 `ts_delta` / 积分 `ts_mean` 21·63·126）
> **×** 两个设置档（TOPCS1600/SUBINDUSTRY〔原封存〕、TOP2500/FAST/decay20〔本战役〕）。
> **evidence**: 11 腿（原 8 + Z1–Z6 中的 5 腿修正族 + AA1–AA5），最好 S **0.86**（裸 sales fy2，TOP2500/FAST），
> 平滑后最好 **0.38**；`failed_ra` 3–5；TO 裸 **0.260–0.304**（正压 30% ATOM 悬崖），平滑后 .058–.090（越过 12.5% F 膝点 ⇒ 41.4 双重 F 负）。
> **mechanism**: 信号是**纯日频**现象，两个时间算子都单调摧毁它（41.3）；字段是归一化比率、时间聚合不伸缩 ⇒ 无法用 `_3mo` 配方重建。
> **rule**: EUR analyst 塔 `analyst10` 修正族**关闭**；未测的 `*revise_value_fy{1,2}`（绝对修正量）按 41.9 的差分阶数表属「日频归一化比率」同类，**预期同死，不建议花槽位**。

⚠ **`seal_dead_end` 是 fail-closed 单向、无解封路径，且 `force_seal=True` / `require_forum_recon=False` 必须人工确认（§8.11）⇒ 本节只提供措辞，不自行写库。**

### 41.12 本节取代的旧结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| **§40.12b** | 「积分降 TO ⇒ F 闸自愈，绑定闸退回 S 与 2Y」 | **✗ 否证**。returns 与 TO 同步塌陷，`returns/max(TO,0.125)` 从 0.1987 → 0.0568（41.4）。**F 的可行改进区在膝点*以上*** |
| **§40.14 末行** | 「派平滑批前先算 F 闸地板；TO 压过 0.125 会让 F 闸自愈」 | **前半保留、后半作废**：算地板仍是对的，但结论相反——**压过 0.125 是 F 负**（41.4） |
| §40.4 | 「字段是一阶差分（构造 (a)）⇒ 正确算子是积分」 | **两个构造都被排除**：Z3 判据不能区分 (a)/(b)，积分结果排除 (b)，非伸缩性排除干净的 (a) ⇒ **构造 (c)：归一化比率，时间聚合不伸缩**（41.3） |
| §40.3 | 「带显式窗后缀 ⇒ 已预平滑 ⇒ 低 TO、高 S」（作为可照搬的配方） | **加限定**：厂商窗作用在水平上、自制窗作用在比率上，不是同一操作；**先判差分阶数再选时间算子**（41.9） |
| §40.12 | 预登记否证判据「max S < 1.0 ⇒ 整族关闭」 | **已触发**（max S **0.38**）。但更强的封死论证是 41.3 的双向单调性，不只是阈值 |
| Batch P 的独立观察 | 「EUR 的水平/分歧度族是被空头倾斜主导的稀释项」 | **升级为机制**：平滑把修正型推向水平型，short/long 排成 1.14 → 1.7–1.9 → 2.2–2.7 的单调谱，唯一过闸形态在另一端 0.92（41.6） |
| §39.7 | 期界↔层级定律（仅在 `analyst_factor_signals` 内测得） | **首次跨数据集确认**（AA5 > AA1，sales fy2）⇒ 从模式升为机制（41.7） |

---

## §42 V5 `YPxg1LzM` 稳健性终验：CONDITIONAL，但**近窗制度在本候选上恰好把两个制度年都包进窗口**，OS 中心估计 1.2–1.5

> 2026-10-20。按 `brain-alpha-robustness` 技能 Phase A–E 对**全战役唯一存活候选**跑完整闸门。
> 结论落两处：人读报告 [`reports/robustness_20261020.md`](../../../reports/robustness_20261020.md)（174 行）
> ＋ 机器读台账 `robustness_YPxg1LzM`（EUR，`checked_at 2026-10-20T06:42:00+08:00`）。
> **本节的价值不在判定本身，在于它把 §38.4 的一阶过拟合警报从「同族兄弟腿旁证」升级为「V5 自己的逐年证据」，
> 并暴露近窗制度（最近 3 个 IS 年）的一个结构性盲区：窗口可以恰好套住全部制度年。**

### 42.1 V5 完整逐年读数（`get_alpha_yearly_stats`，10 个 IS 年）

| 年 | pnl | S | F | returns | DD | margin | TO | long/short | L/S |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 1 596 960 | **3.40** | 3.77 | .1536 | .0273 | .003931 | .0781 | 1342/1277 | 1.051 |
| 2015 | 1 107 076 | 1.90 | 1.75 | .1064 | .0385 | .003190 | .0667 | 1403/1324 | 1.060 |
| 2016 | **4 538** | **0.01** | 0.00 | .0004 | .0613 | .000013 | .0667 | 1523/1201 | 1.268 |
| 2017 | 805 816 | 1.47 | 1.16 | .0775 | .0249 | .002327 | .0666 | 1477/1477 | 1.000 |
| 2018 | 1 257 111 | 2.40 | 2.36 | .1209 | .0317 | .003700 | .0653 | 1525/1406 | 1.085 |
| 2019 | 701 159 | 1.33 | 0.98 | .0674 | .0311 | .002035 | .0663 | 1691/1142 | **1.481** |
| 2020 | **−205 381** | **−0.30** | −0.12 | −.0215 | .0631 | −.000624 | .0688 | 1398/1368 | 1.022 |
| 2021 | **2 203 844** | **3.65** | **4.75** | .2119 | .0239 | .006341 | .0668 | 1380/**1587** | **0.870** |
| 2022 | 2 040 486 | **2.88** | 3.61 | .1962 | .0640 | .005347 | .0734 | 1510/1398 | 1.080 |
| 2023 | 758 090 | **1.22** | 0.93 | .0729 | .0419 | .002143 | .0680 | 1435/1325 | 1.083 |

自洽校验：逐年 pnl 合计 **10 269 699** vs 报告的总额 **10 269 828**，Δ129 = **0.001%**（日聚合舍入）⇒ 读数可信。

分布读数：均值 **1.796**｜中位数 **1.685**｜样本标准差 1.3249（CV **0.738**）｜总体标准差 1.2570（CV **0.6998**）。
**高于 1.58 提交线的年份 = 5/10**；低于 1.0 的 = 2/10（2016、2020）。
**TO 极稳（.0653–.0781，全距 0.0128）⇒ 无换手制度切换**（正面证据）。
最大年度 DD 0.0640 = 全期 DD，而「2× 全期均值」阈 = 0.128 ⇒ **无任何年份触发回撤警报**。

### 42.2 ★ 三条 Phase C 表格**没有格子**的结构性发现

| # | 发现 | 算术 |
|---|---|---|
| **1** | **PnL 年度集中** | top-1 年（2021）= **21.5%**｜top-2（+2022）= **41.3%**｜top-3（+2014）= **56.9%** ⇒ **30% 的年份贡献 57% 的 PnL**。Phase C 只有「个股集中度」格子，没有「年度集中度」格子 |
| **2** | ★★ **ATOM 2Y 通过是单年依赖，盈亏平衡余量仅 +0.054** | 平台 2Y ≈ 最近两年 Sharpe 均值（(2.88+1.22)/2 = **2.05** vs 平台报 **2.09**）。解 `(x + 1.22)/2 = 2.023` ⇒ **x = 2.826**；2022 实际 **2.88** ⇒ **2022 低 0.054 个 Sharpe，ATOM 闸即翻红**。若 2022 落在样本中位数 1.685，2Y ≈ **1.45** —— 同时不过 ATOM（差 0.57）**与** `LOW_2Y_SHARPE`（差 0.13） |
| **3** | ★ **2021 是唯一空头倾斜年（L/S 0.870），且是最好年（S 3.65 / F 4.75）**；其余 9 年全部多头倾斜（1.000–1.481） | ⇒ **最好一年的收益来自与其余样本相反的账面取向 = 取向级结构不稳定，不是水平漂移**。这条比 CV 更能说明问题：CV 只说「波动大」，这条说「赚钱的那年和别的年不是同一个策略」 |

### 42.3 Phase C 三态判定（硬 REJECT 触发数 = **0**）

| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed count | `failed_ra_count 0` / `failed_ppa_count 0`，`checks.fail []`，无名单内 PENDING | **PASS**（B.0 硬前置通过） |
| **Recent-3yr Sharpe（主判定）** | 2021/2022/2023 = 3.65/2.88/1.22，均值 **2.583 ≥ 1.58**，三年每年 > 0.3 | **PASS**（⚠ 见 42.4） |
| Recent-3yr CV_Sharpe | **0.481**（样本）/ **0.393**（总体）——跨在 0.40 边界两侧 | **CONDITIONAL** |
| 衰减比 | 1.22 / 1.73 = **0.705** | **PASS**（≥ 0.50） |
| 平年（近 3 年） | **0** | **PASS** |
| Recent-3yr max/min | 3.65 / 1.22 = **2.99**（阈 3） | **CONDITIONAL**（贴线） |
| 全历史早年疲软 | 全史 CV 0.70；2016 S 0.01、2020 S −0.30；**双峰字形**（峰在 2014 与 2021，非厂字形） | **软标记**（表内明示**绝不 REJECT**） |
| Sub-universe | 平台 PASS，但 **0.90 vs 限 0.8989 = 余量 +0.0011** | **CONDITIONAL**（贴线） |
| 算子数 | **3**（`group_zscore` / `signed_power` / `group_neutralize`） | **PASS**（软标记线 > 5） |
| Margin @ turnover | **28.98 bp** @ TO **6.87%** | **PASS** |
| Top-5 个股集中度 | 逐股 PnL **不可得**；以 `CONCENTRATED_WEIGHT = PASS` 为准 | **不可测** |
| 经济可解释性 | 一句话：「分析师对未来 2 年净利润共识预期的 3 个月渐进上修，市场反应不足」 | **PASS** |

⇒ **CONDITIONAL**（3 项贴线），`failed_checks = []`，8 条软标记。

### 42.4 ★★★ 判定的决定性限定：**近窗制度在本候选上恰好把两个制度年都包进了窗口**

近窗制度（用户指令 2026-06-20）用「最近 3 个 IS 年」作主判定，理由是「要求 10 年全强过严，会杀死活信号」。
**本候选的最近 3 年 = 2021 / 2022 / 2023，其中 2021（3.65）与 2022（2.88）正是全样本的两个峰。**

⇒ **「Recent-3yr PASS」是窗口选择的产物，不构成稳健性证据。** 三条独立佐证：① 10 年里只有 5 年过 1.58；
② 57% 的 PnL 来自 3 个年份；③ ATOM 2Y 的通过依赖 2022 单年、余量 +0.054。

**⇒ 可复用定律（登记）：近窗制度的窗口长度（3）必须与该 alpha 的「峰年间隔」对照使用。
若最近 3 年里含 ≥ 2 个峰年（判据：单年 pnl 占全期 > 15%），Recent-3yr PASS 应自动降级为软标记，
主判定改用「剔除峰年后的均值 / 全样本中位数 / 最近一个非峰年」三口径。
本例三口径全部指向同一个数：OS 中心 1.2–1.5。**

### 42.5 ★★ OS（2024+）理性中心估计 = **1.2–1.5**，三口径互相独立

| 口径 | 值 | 与 1.58 提交线 |
|---|---:|---|
| 最近一个非峰年（2023） | **1.22** | 低 0.36 |
| 剔除 2021+2022 两峰年后其余 8 年均值 | **1.429** | 低 0.15 |
| 全样本中位数 | **1.685** | 高 0.11 |

**三者中两者低于提交线。** ⇒ **「过了闸 ⇒ 可提交」在 OS 期望上高估约 0.5–0.9 个 Sharpe。**
这条与 §38.4 的一阶过拟合警报同向，但**此前只有同族兄弟腿的旁证**（`1YjzoEGm` / `Grge67NZ` 的 2022/2023 = 2.88/1.22 与 2.75/1.23），
**现在有了 V5 自己的逐年证据**——即过拟合警报的主体从「兄弟腿」变成「候选本体」。

### 42.6 `performance_comparison` 边际贡献（分区 `EQUITY:EUR:1:POWER_POOL`）：5/6 为正，**唯 Sharpe 为负**

| 指标 | 池（before） | 池+V5（after） | Δ |
|---|---:|---:|---:|
| **Sharpe** | **3.17** | **3.13** | **−0.04（−1.3%）** ⇒ 软标记 |
| Fitness | 2.01 | **2.17** | **+0.16（+8.0%）** |
| returns | .0502 | .0601 | +.0099 |
| drawdown | .0200 | **.0184** | −.0016（改善） |
| turnover | .1123 | .1036 | −.0087（改善） |
| pnl | 5 178 385 | 6 196 648 | +1 018 263 |
| long/short | 685/782 | 842/895 | +157/+113 |

⇒ 典型「让池更分散更平稳，但略微摊薄单位风险收益」形态。按 Phase C，边际贡献为负**只作软标记交用户终审**，不 REJECT。

### 42.7 ★ 新平台事实：**`submit_verdict` 的提交层恒 404 ⇒ 结论是 `UNVERIFIABLE`（exit 10），不是 `PASS`**

```
submit_verdict(alpha_id="YPxg1LzM") →
  verdict "UNVERIFIABLE" / exit_code 10 / reason_code "UNVERIFIABLE_404"
  submit_status 404 / submit_checks [] / submit_layer_view "dead_endpoint_404" / prepost_unverifiable true
  robustness {recorded true, verdict "CONDITIONAL", failed_checks [], checked_at "2026-10-20T06:42:00+08:00"}
  failed_ra 0 / failed_ppa 0 / sim_fails [] / hard_gate_warnings []
  next_step "…稳健性 CONDITIONAL：先 brain-alpha-repair 修复并重审（≤ 2 轮），再请用户确认；本提示不拦截。"
```

三条可复用结论：

1. **`GET /alphas/{id}/submit` 在本平台恒 404**（工具自述「该视图已定性为死端点」）⇒ **提交层永远不可验证**，
   `submit_verdict` 对 `failed_ra = 0` 的候选**只能返回 UNVERIFIABLE，不可能返回放行**。
   **含义**：本战役即便找到一颗全闸通过、prod < 0.7 的 alpha，`submit_verdict` 也**不会**给出 `PASS`；
   放行权威始终是「平台 prod < 0.7 实测 + 用户明确确认」（AGENTS.md §3.5）。**别把 UNVERIFIABLE 读成「差一点」。**
2. **稳健性台账确实被 `submit_verdict` 读到了**（`robustness.recorded/verdict/failed_checks/checked_at` 四项原样回显），
   且 `CONDITIONAL` **不改判、不拦截**，只在 `next_step` 追加修复提示 ⇒ 技能契约的「CONDITIONAL 不阻断」经端到端实测确认。
3. `sim_warnings` 里 `MATCHES_THEMES` 报的是 **`GLB/D1 TOPDIV3000 Theme`**（乘数 2.5）——**与 EUR alpha 无关的主题命中**，
   说明该 warning 的主题匹配不区分区域，**不能作为「本 alpha 匹配当期 PPA 主题」的证据**（Phase E 的 PPA 判定不能靠它）。

### 42.8 修复通道是**封闭的**，不是「还没试」

`CONDITIONAL` 的下游默认动作是 `brain-alpha-repair`（≤ 2 轮）。**本例该通道封闭**，三条论证：

1. **3 项 CONDITIONAL 全是刀刃形态**：CV 0.481（带界 0.40–0.60）、sub 余量 **+0.0011**、max/min **2.99**（阈 3）。
   刀刃不是「差得多需要修」，而是「一动就翻到另一边，且翻向不可控」。
2. **任何抬高 sub 余量的杠杆都同时压低 S 与 2Y**：§39.1 粒度定律（分组越细，S 与 sub-ratio 同时受损）＋
   §39.2 四闸交集为空的代数证明（prod 要求的 p 区间与前三闸的 p 区间**不相交**）。
   即 repair 的每一个可行方向都已被实测或代数封死，不是「没试过的招」。
3. **V5 真正的阻断项不是稳健性，是 prod 0.7398**（超限 0.0398），而 prod 直方图 `[0.7,0.8)` 桶 **n=3** ⇒
   按 `wq-window-valley-break-prod-wall` 自己的判据（n ≥ 1 必死）属**族级死亡**。

### 42.9 终审意见：**不建议提交**（交用户裁决；红线不可代答）

- **唯一过 prod 的路径**是平台豁免条款「Sharpe 比在位相关 alpha 高 ≥ 10%」（V5 的 1.73 对任何 S ≤ 1.573 的在位者成立），
  而**该条款只能用一次不可逆提交来验证**——在位者身份与 Sharpe 在 API 上不可读
  （`get_record_sets` 无相关性记录集，`PROD_CORRELATION` 恒 `pending`，提交层恒 404 §42.7）。
- **即使豁免通过、提交成功**：OS 中心估计 1.2–1.5 低于 1.58 提交线 ⇒ **大概率被 DECOMMISSION**。
- **⇒ 这是一笔「用一颗不可撤销的提交额度，去赌一个期望收益为负的豁免」的交易。** 按红线（AGENTS.md §7 / 技能设计边界），
  **提交前必须用户明确确认，任何 waiver 无效**，本档案与本报告均**不代为决定、不代为提交**。
- **塔位副作用**（§40.13）：EUR/D1/ANALYST 现有 1 颗、点亮阈 3 ⇒ 提交这 1 颗 + 再 1 颗即点亮，
  触发锁定项「已点亮塔不作主数据集」，与目标「10 颗全 analyst」**直接冲突**。

### 42.10 本节限定 / 新增的结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| §38.4 | 「一阶过拟合警报」（依据是同族兄弟腿的 2022/2023 读数） | **升级**：警报主体是候选本体，V5 自己的 10 年序列给出 5/10 过线、双峰字形、57% PnL 集中于 3 年（42.1–42.2） |
| §40.13 | 「可交付上限 = 1，且以一次不可逆提交为条件」 | **保留，并补一层**：这 1 颗的 OS 中心估计 1.2–1.5 ⇒ **上限 1 是「形式上限」，「期望上限」是 0**（42.5、42.9） |
| 近窗制度（Phase C 主判定） | 用最近 3 个 IS 年判稳健性 | **加限定**：窗口内含 ≥ 2 个峰年时 Recent-3yr PASS 自动降级为软标记，改用三口径（42.4）。**这是技能层的提案，需人审后才进 Phase C**（按 Phase A，论坛/新发现只作提案） |
| （未登记） | `submit_verdict` 会给出 `PASS` | **✗**：提交层恒 404 ⇒ 对 `failed_ra = 0` 只能返回 `UNVERIFIABLE`（exit 10）；放行权威 = prod 实测 + 用户确认（42.7） |
| （未登记） | `MATCHES_THEMES` 命中即「匹配当期主题」 | **✗**：EUR alpha 命中 `GLB/D1 TOPDIV3000 Theme`，该 warning 不区分区域，**不能作 PPA 主题证据**（42.7 第 3 条） |
| （未登记） | Phase C 有「个股集中度」格子即够 | **补格提案**：需增「年度 PnL 集中度」与「最佳年账面取向是否异于其余年份」两格——本例前者 56.9%、后者 L/S 0.870 vs 其余 1.000–1.481，**两格都指向不稳定，而现有 12 格一条都没抓到**（42.2） |

---

## §43 `analyst7` 复活：Batch AB 7/7 收批，**§29.8 对 `dps` 的 returns 判死被实测推翻**，并首次拿到 +0.225 的 sub 余量

> 起因：交付清单成型前重扫未封口路径，发现 `analyst7` **不在 `get_dead_datasets(EUR)` 名单里**
> （名单只有 `ml_factor_proj` / `model354` / `news36` / `news38`），档案 L1376 评它「⚠ **部分活**」，
> 且 §29.8 留了一条**从未收割的开放线**：「已派 `industry` / `sector` / `country` 三种分组复测 `dps`（批次待收）」。
> 该批**从未收割、从未记录**，而且用的是**旧设置档**（decay 40 / CROWDING / subindustry / p1.4），
> 不是产出本战役唯一存活者的 FAST / decay20 配方。⇒ 本节把这条线补上。
> 全部设置除注明外：EUR / TOP2500 / D1 / **FAST** / decay **20** / trunc 0.08 / maxTrade ON / nanHandling ON /
> pasteurization ON / unitHandling VERIFY / 2014-01-01→2023-12-31 / FULL。

记 `R4 = divide(subtract(est_12m_dps_mean, est_12m_dps_mean_4wks_ago), est_12m_dps_std)`。

### 43.1 Batch AB 全读数（7/7 完成，`get_user_alphas` count 42 → **49**，delta = +7 即完整性证明）

| tag | 表达式 | id | S | F | 2Y | returns | TO | sub | **sub/S** | DD | margin | L/S | pnl | fr |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **AB1** | `group_neutralize(signed_power(group_zscore(R4, industry), 1.8), market)` | **`RRA1lYrz`** | **1.28** | **0.85** | **1.78** | **.0549** | .0683 | **0.89** | **0.695** | .0568 | .001609 | 1364/1455 | 5 667 643 | **2** |
| AB2 | 同 AB1 但**无外层包裹** | `78onvaNO` | 1.27 | 0.84 | 1.78 | .0549 | .0683 | 0.89 | 0.701 | .0568 | .001609 | 1364/1455 | 5 666 622 | 2 |
| AB3 | W3 形态 `densify(cart(market,country))` **p2.0** | `pwvKMEZo` | 1.19 | 0.79 | 1.65 | .0552 | .0702 | 0.85 | 0.714 | .0623 | .001575 | 1350/1469 | 5 701 301 | 2 |
| AB4 | **横截面离散度** `divide(subtract(dps_high, dps_low), dps_mean)` | `zqrR2Ozd` | **−0.67** | −0.30 | −0.97 | −.0253 | .0489 | −0.28 | — | .2951 | −.001033 | 914/**1906** | **−2 607 393** | 3 |
| AB5 | **预测家数广度** `ts_delta(est_12m_dps_num, 21)` | `xA1d2zqq` | 0.39 | 0.11 | −0.43 | .0107 | .0829 | 0.30 | — | .0584 | .000259 | 1430/1389 | 1 106 016 | 3 |
| AB6 | 同 AB1 换 **`fcf`** | `JjPvW5zO` | 0.76 | 0.39 | 0.84 | .0326 | .0718 | 0.72 | — | .0669 | .000909 | 1538/1282 | 3 366 505 | 3 |
| AB7 | 同 AB1 但**去掉 `÷std`** | `WjLVoabo` | 0.65 | 0.32 | 0.51 | .0300 | .0660 | 0.92 | — | .1168 | .000909 | 1406/1414 | 3 095 156 | 3 |

### 43.2 ★★★★★ 推翻一：§29.8 对 `dps` 的 **returns 判死是错的**，错因正是它自己预警的那条

§29.8 反算 `6XAexOYP` 的 returns `= 0.125 × (0.57/1.15)² = 0.0307` ≈ 平台报的 0.0312，**< 3.5%**，
按探针 SOP 应判死（过 F ≥ 1.0 需 S ≥ 2.00，而实测只有 1.15）。§29.8 同时写下了自我预警：

> 「**SOP 的 returns 判死只能在「分组轴也扫尽之后」使用**，否则会把结构未穷尽的腿误杀。」

**实测：同一字段、同一构造，只换分组与中性化档，returns 从 0.0307 → 0.0549，+79%。**
这与 §29.2 早先在另一数据集上测到的 `industry` 分组把 returns 从 5.04% 抬到 7.06%（+40%）同向，
且**幅度更大**。⇒ **returns 不是字段的属性，是「字段 × 分组轴 × 中性化档」的属性；
探针 SOP 的 returns 判死门（3.5%）在单一分组下测得的值不具备判死资格。**

顺带的区域级后果：**AB1 的 returns 0.0549 ≥ 0.05**，正好触发 EUR region profile 的
「升 active 须出现 **returns ≥ 0.05** 且 prod 直方图不是密墙的新信号源」这一停止条件的**前半句**
（后半句 prod 尚 pending，见 43.6）。这是本战役第一次有 EUR 腿满足该 returns 门。

### 43.3 ★★★★★ 推翻二：AB1 拿到 **+0.225** 的 sub 余量，而 V5 只有 **+0.0006** ⇒ **p 轴对 V5 封闭、对 AB1 开放**

sub 是比率闸（TOP2500 限 = `0.5196 × S`）。逐条核算：

| 候选 | S | sub | 限 = 0.5196×S | **余量** |
|---|---:|---:|---:|---:|
| **AB1** `RRA1lYrz` | 1.28 | 0.89 | 0.665 | **+0.225** |
| AB2 | 1.27 | 0.89 | 0.660 | +0.230 |
| AB3 | 1.19 | 0.85 | 0.618 | +0.232 |
| V5 `YPxg1LzM` | 1.73 | 0.90 | 0.899 | **+0.0006**（§42.3 记 +0.0011，口径同） |
| W3 `RRA1EaQn` | 1.63 | 0.85 | 0.847 | +0.003 |

这条差异的**结构性含义**比数字大：§39.2 之所以能用代数证明「四闸交集为空」，
关键前提是 **prod 的 p 区间 [2.146, ∞) 与前三闸的 p 区间 [1.962, 1.991] 不相交**，
而 1.962 这个下界正是由「sub/S ≥ 0.5196」在 **p 的边际变化率**下推出来的。
**AB1 的 sub/S = 0.695 意味着它离那条约束很远，p 轴可以往下走（p↓ 抬 S）而不立刻撞 sub 闸。**
⇒ **§39.2 的「交集为空」结论只对 sub/S 贴线的族成立，不能外推到有余量的族。**（新增限定，见 43.7）

### 43.4 ★★★ 归因：两条独立缺口，不是三条（F 被 S 吸收）

AB1 报 `failed_ra = 2`（`LOW_SHARPE` + `LOW_FITNESS`），2Y 未过 ATOM 线但未进 `ra_failed_checks`
（ATOM 用 2Y 替换 IS_LADDER，见 §38/§39 的 ATOM 口径）。按 §41.4 的 F 拐点公式核算：

```
F = S × sqrt(returns / max(TO, 0.125))
AB1: 1.28 × sqrt(0.0549 / 0.125) = 1.28 × 0.6627 = 0.848 ≈ 0.85 ✓（平台报 0.85）
```

TO = 0.0683 **低于 12.5% 拐点** ⇒ 分母冻结在 0.125，降 TO 无收益（§41.4 定律 2）。
**反解：要 F ≥ 1.0 需 S ≥ 1.0/0.6627 = 1.509；要过 LOW_SHARPE 需 S ≥ 1.58。
而 S = 1.58 时 F = 1.58 × 0.6627 = 1.047 ≥ 1.0 自动成立。**

⇒ **AB1 的缺口只有两条独立的：`+0.30 S`（1.28→1.58）与 `+0.243 2Y`（1.78→2.023）。**
`LOW_FITNESS` 不是第三条缺口，它是 `LOW_SHARPE` 的函数。这条化简让后续批次的目标从「三闸」收成「两闸」。

### 43.5 ★★ 算子替换的边界用法：`÷std` 值 **+0.63 S**，两个未试构造直接判死

目标步 3 要求「算子使用要考虑算子能解决的场景全面替换测试避免遗漏边界用法」。本批把 `analyst7`
四件套的**归一化位**与**信号构造位**都做了替换：

| 构造 | 经济含义 | 读数 | 裁定 |
|---|---|---:|---|
| `divide(subtract(mean, mean_4wks), **std**)` | 修正幅度 ÷ 分歧度（**时序修正的横截面标准化**） | **S 1.28 / 2Y 1.78** | **唯一活口** |
| `subtract(mean, mean_4wks)`（**去掉 `÷std`**，AB7） | 裸修正幅度（带单位、受量纲与股价水平污染） | S 0.65 / 2Y 0.51 | **`÷std` 值 +0.63 S / +1.27 2Y** |
| `divide(subtract(**high, low**), mean)`（AB4，**§29.8 从未在 `dps` 上试过**） | 分析师**横截面分歧度**（不是修正） | **S −0.67**，pnl **−2 607 393**，L/S 914/**1906** | **判死**：EUR 的「分歧度」族是稀释项（与 Batch P 的 `consensus_value` 腿同形态：严重多空失衡） |
| `ts_delta(**est_12m_dps_num**, 21)`（AB5，**广度机制**，IND 已验证过） | 覆盖该股的**预测家数变化** | S 0.39 / 2Y −0.43 | **判死**：IND 的 breadth 机制在 EUR/D1/TOP2500 不复现（第 7 例「排名/斜率不跨区迁移」，见 43.7） |
| 同构造换指标 **`fcf`**（AB6） | 自由现金流修正 | S 0.76 / 2Y 0.84 | 弱，但**与 §29.8 的 0.55 相比 +0.21**，与 `dps` 的 +0.13 同量级 ⇒ **档位移是系统性的，但不足以让死指标复活** |

⇒ **`analyst7` 的活口仍然只有 `dps` 的「时序修正 ÷ 分歧度」这一个构造。**
`dps_high` / `dps_low` / `dps_num` 三个字段（αC 82 / 49 / 39，即有人挖过）**实测无信号**。

### 43.6 AB1 vs AB2 vs AB3：外层包裹与 p 的边际贡献（第 5 次确认「外层 `market` 是 no-op」）

| 对比 | ΔS | Δ2Y | Δreturns | Δsub/S | 结论 |
|---|---:|---:|---:|---:|---|
| AB1 − AB2（加外层 `group_neutralize(·, market)`） | **+0.01** | 0.00 | 0.0000 | −0.006 | **外层 `market` 完全无效**（第 5 例；前四例见 §39.1 / Z1 vs Z2 / §31.4） |
| AB3 − AB1（外层换 `cart(market,country)` 且 p1.8→2.0） | −0.09 | −0.13 | +0.0003 | +0.019 | p↑ 与 cartesian 一起**同时压低 S 与 2Y**，只换来 sub 比率 +0.019 ⇒ **在有余量的族上是纯亏损**（与 V5 族相反，那里 sub 贴线所以必须买） |

⇒ **AB2 与 AB1 逐字段几乎相同（pnl 差 1 021 / 5 667 643 = 0.018%）**，外层包裹可以永久省略；
AB1 之所以保留外层，只是因为它是与 V5 严格同构的对照腿。

### 43.7 Batch AC 的设计（7 条，已派，`ok:true` ×7，无 429）

**这不是盲扫，是一次变量分解**：旧档（CROWDING / subindustry / d40 / p1.4）拿到 **2Y 2.01**（距 ATOM 线仅 0.013）
但 S 只有 1.15；新档（FAST / industry / d20 / p1.8）拿到 **S 1.28** 但 2Y 1.78。
**两档之间有 4 个变量同时不同 ⇒ 必须逐个隔离**，否则无法判断该往哪边走。

| tag | 相对 AB1 的唯一改动 | 假设（含出处） | sim id |
|---|---|---|---|
| **AC1** | **decay 20 → 40** | §32.1 的 decay 梯子在另一数据集上测得 d20→d40：S +0.07、**2Y +0.03**、prod +0.012 ⇒ 预期小幅双升 | `3pRmtr4OR4UT9b26oBfGgFv` |
| **AC2** | **p 1.8 → 1.4** | 花掉 43.3 的 +0.225 sub 余量换 S；§38 的 p 轴在贴线族上「p↓ 抬 S 但破 sub」，**本族有余量所以值得试** | `ZIRCX6U04XFbOdSfQtT0ux` |
| **AC3** | **内层 `industry` → `subindustry`** | §41 定律 5（AA5 0.38 > AA1 0.14）：信号住在 subindustry 内；且旧档的 2Y 2.01 正是在 subindustry 下测得 | `1RkxIbKM4W8alDWAyBbfva` |
| **AC4** | **settings 中性化 FAST → CROWDING** | 隔离旧档剩下的那一个变量；9 路中性化图上 CROWDING(d80/p1.4) 的 2Y 与 FAST 同为 2.09 | `2pnK0P2nb4ITbjmlEVdoeRm` |
| **AC5** | **归一化位 `÷std` → `÷mean`**（百分比修正） | **全新构造**：无量纲的相对修正 %，§29.8 只试过 `÷std` 与 `cpx` 上的 `std/mean`；同单位相除 ⇒ VERIFY 安全 | `4v09hr1Rj5iVaB314DUZYXgq` |
| **AC6** | **快照 `4wks_ago` → `3mth_ago`** | 另一条活的快照轴，**只在旧档测过**（`rKdPkXL8` S 1.08 / 2Y 1.41）⇒ 按 §30.6 必须在新档重测 | `1BpBDYbfU58ccEg1aOUg5m5B` |
| **AC7** | **p1.4 + decay40** | 若 AC1 与 AC2 两个杠杆同向可加，这条是唯一可能同时越过 S 与 2Y 两线的组合 | `BBUA7b9G4sC96Sp1qUCmzd` |

**全部 7 条只用 §29.9 已验证的 4 个字段名**（`est_12m_dps_mean` / `_mean_4wks_ago` / `_mean_3mth_ago` / `_std`）
与已验证的分组关键字（`industry` / `subindustry` / `market`）⇒ **无 CANCELLED 连坐风险**（§29.9 的工程坑）。
**全批无任何常量加到带单位字段上** ⇒ 规避 `EUR-ANALYST-CONSENSUS-TARGETPRICE-DEAD` 记录的
`Incompatible unit expected Unit[TSPrice:1] found Unit[]` 陷阱。

### 43.8 ★★ 对「可交付上限」的影响：§40.13 的**分母**被换了

§40.13 的「上限 = 1」是**针对 `analyst_factor_signals` 算出来的**，其硬约束是
「该集**恰好只有 9 个** `estimate_change` 字段（§39.11 全量枚举）+ 同字段构造相关 0.99 ⇒ 天花板 9，
而 6 个实测全闸过率 = 0」。§42.10 又补了一层「期望上限 = 0」。

**`analyst7` 不在这个论证的分母里**：它有 **1111 个 MATRIX 字段 / 32 个指标各带四件套**（§4.2），
§29.8 只测了 **5 个指标**（dps / fcf / tbv / nav / cpx），且**只在 1 个分组 + 1 个设置档下测**。
按 §29.8 自己写下的方法论更正——

> 「**免测只适用于「同指标的不同统计量」，不适用于「不同指标」**：指标之间经济含义不同，必须逐个测。」

⇒ **剩余未测指标 = 27 个**。所以：

- **§40.13 / §42.10 的「上限 1 / 期望 0」继续对 `analyst_factor_signals` 成立，不能外推到 `analyst7`。**
- **`analyst7` 的可交付上限目前无证据支撑任何一个数字**：命中率 1/5 = 20%（且「活」= S > 1，不是 S > 1.58），
  线性外推 32 个指标 ⇒ 约 6 个「活」、**0–2 个可能过全闸**。这个外推的分母太小（5），只作量级参考。
- **AB6 的 `fcf` = 0.76 对 §29.8 的 0.55 是 +0.21，与 `dps` 的 +0.13 同量级** ⇒ **档位移是系统性的、
  但幅度不足以让 §29.8 判死的指标（tbv 0.29 / nav −0.03 / cpx −0.28）复活**。
  这是**对 27 个未测指标的第一条负面先验**：它们大概率也不会因为换档而复活。

### 43.9 本节限定 / 新增的结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| §29.8 | `dps` 的 returns 0.0307 < 3.5% ⇒ 按 SOP 应判死（并附自我预警） | **✗ 判死作废**：换分组/中性化档后 returns = **0.0549**（+79%）。**returns 不是字段属性，是「字段 × 分组轴 × 档」的属性；单档测得的 returns 不具备判死资格** |
| §39.2 | 四闸交集为空（代数证明，prod 的 p 区间与前三闸不相交） | **加限定**：该证明的前提是 sub/S **贴线**（V5 余量 +0.0006）。**对 sub/S 有余量的族（AB1 = +0.225）不成立**，p 轴在那类族上是开放的 |
| §40.13 / §42.10 | 可交付上限 = 1（形式）/ 0（期望） | **保留，但明确分母**：这两条只对 `analyst_factor_signals`（9 字段）成立。`analyst7`（1111 字段 / 27 个未测指标）**不在该论证覆盖范围内**（43.8） |
| §29.8 维度表 | `dps` 3mth 1.08 / 4wks **1.15** 是「唯一活口」 | **数值已过期**：4wks 在新档下 S **1.28** / F **0.85** / 2Y **1.78**（AB1）。旧数值是 CROWDING/d40/subind/p1.4 档的读数 |
| §4.2 / §29.8 | `dps_high` / `dps_low` 的横截面分歧度构造「从未试过」 | **已试并判死**（AB4，S **−0.67**、pnl 负、L/S 914/1906）⇒ EUR 的分歧度族是稀释项，与 Batch P 同形态 |
| （未登记） | `est_12m_dps_num` 广度机制（IND 已验证）可能在 EUR 复现 | **✗**（AB5，S 0.39 / 2Y −0.43）⇒ **第 7 例「排名与斜率不跨区迁移」**，与 §41 定律 6 同源 |
| （未登记） | 外层 `group_neutralize(·, market)` 可能有贡献 | **✗ 第 5 次确认无效**：AB1 − AB2 = ΔS **+0.01**、Δpnl **0.018%**（43.6） |
| （未登记） | 缺口是三条（S / F / 2Y） | **实为两条**：TO 0.0683 < 12.5% F 拐点 ⇒ F = S × 0.6627，**S ≥ 1.58 时 F = 1.047 自动过**（43.4） |

---

## §44 **prod 墙被打破：AD1 = 本战役首个 `failed_ra_count = 0` 的全通过 ATOM 候选（prod 0.497）**，Batch AC/AD 全收，`analyst7` 指标网格全量枚举

> 承接 §43。§43 结束时手上是 AB1（S 1.28 / 2Y 1.78，缺 +0.30 S）与「§39.2 的四闸交集为空」这条中心不可能性证明。
> 本节用 **Batch AC（7 腿变量分解）+ Batch AD（3 腿杠杆叠加）** 把 S 推到 **1.71**，并用 `check_correlation(refresh=True)`
> 实测出 **prod 0.4203 / 0.4232 / 0.4970**——**§39.2 的证明作废，EUR analyst 塔的 prod 密墙是数据集属性而非区域属性。**
> 收批完整性证明：`get_user_alphas` count **49（AB 后）→ 52（AC1/AC3/AC7）→ 59（AC 余 4 腿 + AD 3 腿）**，
> 与派发条数逐项相符（AC 7 + AD 3 = 10，49 + 10 = 59）。

### 44.1 Batch AC 全 7 腿收批（变量分解：OLD 档 ↔ NEW 档之间四个变量逐个隔离）

设计动机见 §43.7：OLD 档（CROWDING / subindustry / d40 / p1.4）拿到 2Y **2.01**（只差 ATOM 线 0.013）但 S 只有 1.15；
NEW 档（FAST / industry / d20 / p1.8）拿到 S 1.28 但 2Y 只有 1.78。**四个变量同时不同 ⇒ 一次只改一个。**

令 `R4 = divide(subtract(est_12m_dps_mean, est_12m_dps_mean_4wks_ago), est_12m_dps_std)`，
基准 **AB1** = `group_neutralize(signed_power(group_zscore(R4, industry), 1.8), market)` @ d20 / FAST，S **1.28** / F **0.85** / 2Y **1.78** / sub **0.89**（ratio 0.695）。

| 腿 | 相对 AB1 只改 | alpha id | S | F | 2Y | sub | ratio | ret | TO | DD | margin | L/S | pnl | fr |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **AC1** | decay 20 → **40** | `88veEEbv` | 1.30 | 0.86 | **1.91** | 0.85 | 0.654 | .0546 | .0630 | .0553 | .001734 | 1365/1455 | 5 633 817 | 2 |
| **AC2** | p 1.8 → **1.4** | `npA8erPl` | **1.51** | 0.98 | **2.05** | 0.96 | 0.636 | .0531 | .0631 | .0509 | .001683 | 1378/1442 | 5 477 049 | 2 |
| **AC3** | 内层 `industry` → **`subindustry`** | `9qE7dM1e` | **1.52** | 0.94 | **2.23** | 0.89 | 0.586 | .0474 | .0624 | .0594 | .001517 | 1400/1419 | 4 886 909 | 2 |
| **AC4** | settings FAST → **CROWDING** | `QPY9NoOM` | 0.91 | 0.55 | 1.40 | 0.66 | 0.725 | .0459 | .0500 | **.1026** | .001836 | 1403/1416 | 4 738 528 | 3 |
| **AC5** | 归一化 `÷std` → **`÷mean`** | `WjLVoxoP` | 0.81 | 0.45 | 0.67 | 0.39 | 0.481 | .0386 | .0695 | .0798 | .001112 | **1607/1213** | 3 986 825 | 4 |
| **AC6** | 快照 `4wks_ago` → **`3mth_ago`** | `Vkd3mRz8` | 1.43 | **1.00** | 1.55 | 0.76 | 0.531 | **.0612** | .0621 | .0647 | **.001969** | 1427/1393 | **6 313 082** | 2 |
| **AC7** | **p1.4 + decay 40**（组合腿） | `zqrR22VE` | **1.52** | **0.99** | **2.16** | 0.93 | 0.612 | .0528 | .0576 | .0478 | .001833 | 1377/1442 | 5 445 667 | 2 |

**杠杆隔离表（每条只由一对腿相减得到，全部实测，无外推）：**

| 杠杆 | 减法 | ΔS | Δ2Y | Δratio | 其它 | 结论 |
|---|---|---:|---:|---:|---|---|
| **内层 `subindustry`** | AC3 − AB1 | **+0.24** | **+0.45** | −0.109 | ret −.0075 | **最强单杠杆**。§41 定律 5（AA5 0.38 > AA1 0.14）跨数据集复现，且效应量放大 17 倍（那里 +0.24 S 在死族上，这里在活族上） |
| **p 1.8 → 1.4 @d20** | AC2 − AB1 | **+0.23** | **+0.27** | −0.059 | — | §43.3 的 sub 余量把 p 轴打开了；V5 族上 p1.4 会砸 sub，这里 ratio 仍 0.636 ✓ |
| **p 1.8 → 1.4 @d40** | AC7 − AC1 | +0.22 | +0.25 | −0.042 | DD −.0075 | 与 @d20 同量级 ⇒ **p 杠杆与 decay 正交** |
| **decay 20 → 40 @p1.8** | AC1 − AB1 | +0.02 | **+0.13** | −0.041 | — | **2Y 斜率是 §32.1（`analyst_factor_signals` 上 +0.03）的 4 倍** |
| **decay 20 → 40 @p1.4** | AC7 − AC2 | +0.01 | +0.11 | −0.024 | DD −.0031 | 同上，斜率与 p 无关 |
| **FAST → CROWDING** | AC4 − AB1 | **−0.37** | **−0.38** | +0.030 | **DD +.0458**（近 2 倍恶化） | **✗ 判死**，见 44.9 第 7 条：OLD 档的 2Y 2.01 不该记在 CROWDING 头上 |
| **`÷std` → `÷mean`** | AC5 − AB1 | **−0.47** | **−1.11** | −0.214 | **L/S 1607/1213 严重多头倾斜** | **✗ 判死**：不是「要不要归一化」，是**必须按分歧度归一化**（见 44.9 第 6 条） |
| **`4wks_ago` → `3mth_ago`** | AC6 − AB1 | +0.15 | **−0.23** | −0.164 | **ret +.0063、pnl +11%、margin 最高** | **半死**：慢快照抬 S 与 returns 但砸 2Y ⇒ 对 ATOM（2Y 线 2.023）不可用，对 REGULAR 常规通道可能可用 |

### 44.2 Batch AD：三条近可加杠杆叠加 ⇒ **AD1 全闸通过**

`R4s = divide(subtract(est_12m_dps_mean, est_12m_dps_mean_4wks_ago), est_12m_dps_std)`，内层换成 `subindustry`。

| 腿 | 表达式 | 设置 | alpha id | S | F | 2Y | sub | ratio | ret | TO | DD | margin | L/S | pnl | **fr** |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **AD1** | `group_neutralize(signed_power(group_zscore(R4s, subindustry), 1.4), market)` | **d40** / FAST | **`LL5dmv9a`** | **1.71** | **1.02** | **2.41** | 0.95 | **0.556** | .0449 | .0522 | **.0450** | .001721 | 1388/1431 | 4 634 507 | **0** ✅ |
| **AD2** | 同上 | **d20** / FAST | **`pwvKMb6q`** | **1.69** | **1.01** | **2.34** | 0.95 | **0.562** | .0445 | .0587 | .0527 | .001518 | 1392/1427 | 4 597 261 | **0** ✅ |
| AD3 | 同 AD1 但 **p1.8** | d40 / FAST | `j2erPkW5` | 1.55 | 0.96 | 2.34 | 0.89 | 0.574 | .0477 | .0560 | .0474 | .001703 | 1395/1424 | 4 918 629 | 2 |

**AD1 与 AD2 双双 `failed_ra_count = 0`、`ra_failed = false`、`checks.fail = []`，`LOW_SHARPE` 与 `LOW_FITNESS` 首次出现在 `pass` 列表里。**
这是 22 批、59 颗 EUR alpha 以来第一次。AD3 差 **0.03 S**（1.55 vs 1.58）——p1.8 在 subindustry 基座上仍不够。

**可加性检验（本节最重要的定量结论）**：
```
S:  AB1 1.28 + subind 0.24 + p1.4 0.23 + d40 0.02 = 预测 1.77   实测 1.71   ⇒ 93% 可加
2Y: AB1 1.78 + subind 0.45 + p1.4 0.27 + d40 0.13 = 预测 2.63   实测 2.41   ⇒ 87% 可加
```
⇒ **杠杆近似可加但有递减**（内层分组与 p 都在压极端 z-score 的放大，机制部分重叠：p1.4 在 industry 基座值 +0.23 S，在 subindustry 基座只值 **+0.16**（AD1−AD3））。
**可复用规则：多杠杆叠加外推时打 7–13% 折扣。** 若按 100% 可加设计，会误判「已经够了」而少发一腿。

**decay 在 subindustry+p1.4 基座上的读数（AD1 − AD2）**：d40 比 d20 **+0.02 S、+0.07 2Y、DD 更优（.0450 vs .0527）、margin 更优（.001721 vs .001518）**，代价是 ret/TO 略降。d40 全面占优 ⇒ 后续所有腿默认 d40。

#### 44.2.1 AD1 的约束几何与 V5 **完全相反**（工程含义最大的一条）

| 闸 | AD1 读数 | 线 | 余量 |
|---|---:|---:|---|
| **LOW_SHARPE** | 1.71 | 1.58 | **+8.2%** ← 最紧 |
| **LOW_FITNESS** | 1.02 | 1.0 | **+5.0%** ← 次紧（经 returns 传导：TO .0522 < 12.5% 拐点 ⇒ F = S×sqrt(ret/0.125)，需 ret ≥ 0.04275，实 .0449） |
| LOW_SUB_UNIVERSE_SHARPE | ratio 0.556 | 0.5196 | +7.0% |
| **ATOM 2Y** | **2.41** | 2.023 | **+19.1%** |
| **PROD_CORRELATION** | **0.497** | 0.7 | **+40.9%（最松）** |
| SELF_CORRELATION | 0.1706 | 0.7 | +75.6% |
| LOW/HIGH_TURNOVER | .0522 | .01 / .7 | 两侧都很松 |
| CONCENTRATED_WEIGHT | pass | 0.1 | DD .0450 是全战役最低之一 |

⇒ **V5 是 prod-bound**（prod 0.7398 ✗ 差 0.0398，其余全过）；**AD1 是 S/F-bound**（prod 有 0.203 空间，S 只有 0.13）。
**这个反转是本节最重要的工程指令：在 `analyst7` 上，后续一切优化都朝 S 与 returns 推，绝不再动 prod 杠杆**
（decay 上调、hump、tail、更细的 cartesian 分组）——那些在 `analyst_factor_signals` 上是必需品，在这里是**白丢 S**。
§32.1 的 decay→prod 斜率（+0.00113/unit）在本族上完全用不着：prod 基线 0.42–0.50，离墙 0.20–0.28。

⚠ **如实登记一条不利读数**：AD1 的 **returns 0.0449 < 0.05**，低于 EUR profile「升 active」的 returns 触发线。
但同族的 AB1（.0549）/ AC7（.0528）/ AC6（.0612）都过线 ⇒ **区域级触发条件由该族满足，AD1 本身不满足**，不挪用。

#### 44.2.2 AD1 prod 实测（`check_correlation(refresh=True)`，非缓存）

```
production: max_correlation 0.497   passes_check true
histogram_nonzero（最高三桶）: [0.3,0.4] n=16991 · [0.4,0.5] n=75 · 【[0.7,0.8) 桶不存在，n = 0】
max 0.497 / min −0.4716
self: max 0.1706 passes  top_correlated gJj1nxLM 0.1706 / 78jdv6b1 0.1223 / Wj71Q12o −0.1217 / Wj7g2gAx −0.1733
      pool_size 4 · full_os_pool_size 6 · excluded_power_pool_count 2 · ppac_ids_cached 2
all_passed: true
```
同族另两条实测：AC7 `zqrR22VE` prod **0.4203** / self 0.1444 / `all_passed true`；AC3 `9qE7dM1e` prod **0.4232** / self 0.1281 / `all_passed true`。
**三条腿、三种分组、两种 decay、两种 p ⇒ prod 全落在 0.42–0.50。这是 `analyst7` 的数据集级属性，不是构造巧合。**

### 44.3 §39.2 中心不可能性证明作废

§39.2 的代数是：prod 要求 p ≥ 2.146，而 S/2Y/sub 要求 p ∈ [1.962, 1.991]，两区间不相交 ⇒ 四闸交集为空。
其中 1.962 这个下界来自 `sub/S ≥ 0.5196`，而它之所以把 p 顶到 1.962，**只因为 V5 的 sub 余量是 +0.0006（贴线）**。

**AD1 是该证明的直接反例**：p = **1.4**（远在 2.146 之下）、sub ratio **0.556**（余量 +0.036）、prod **0.497**（余量 +0.203）、2Y **2.41**（余量 +0.387）、S **1.71**（余量 +0.13）——**四闸同时成立**。

⇒ **§39.2 的有效范围收窄为：「sub/S 贴线（余量 < 0.01）且 prod ≥ 0.70 的族」**。它从来不是 EUR analyst 塔的普适不可能性定理，
而是 **`analyst_factor_signals` × V5 构造**这一格上的算术事实。§43.3 已加过限定，本节给出反例本体。
**方法论教训（第 9 例，见 §39.9 元定律）：任何「交集为空」的代数证明，必须逐个写出它的前提数值来自哪一颗 alpha、哪个设置档。**
§39.2 写了 p 区间却没写「sub 余量 = +0.0006」这个隐含前提，于是被当成区域级结论沿用了 4 节。

### 44.4 EUR profile 的「升 active」停止条件已满足

区域控制面板原文：*"停止条件：EUR/D1 结构性穷尽（2026-10-02）——升 active 须出现 **returns ≥ 0.05** 且 **prod 直方图不是密墙**的新信号源"*。

| 判据 | 实测 | 满足 |
|---|---|---|
| returns ≥ 0.05 | AB1 **.0549** · AC6 **.0612** · AC7 **.0528** · AC2 .0531 · AC1 .0546 | ✅（5 条腿过线） |
| prod 直方图不是密墙 | `[0.7,0.8)` 桶 **n = 0**（三条腿全部如此）；AD1 最高桶是 `[0.4,0.5]` n=75 | ✅ |
| 新信号源 | `analyst7`（Broker Estimates，1111 字段），**不在任何 seal、不在 `get_dead_datasets(EUR)`、档案 L1376 评「部分活」** | ✅ |

⇒ **两半条件首次同时满足。EUR 自 2026-10-02 被判「结构性穷尽」以来第一次具备升 active 的实证依据。**
⚠ **但改 `tracking/EUR/config/` 的入场状态属于改控制文件**：按 §8.1.2，`stop_rules` 类闸门的 waiver **只有 user 能批准**（agent 不能自授），
且本战役全程是 `probe-only` 下用「探针批」名义跑的。⇒ **本节只登记条件已满足，不自行改 profile、不自行发 waiver，交用户裁定。**

### 44.5 团数 = 1：`dps` 族只能出 **1 颗**，10 颗目标必须换指标

`compute_mutual_correlation`（`local_calculation true`、`num_points 1021`、`years 4`、`missing_pnl []`、**零槽位成本**）：

| | AD1 `LL5dmv9a` | AD2 `pwvKMb6q` | AD3 `j2erPkW5` | AC3 `9qE7dM1e` | AC7 `zqrR22VE` |
|---|---:|---:|---:|---:|---:|
| **AD1**（subind p1.4 d40） | 1.000 | **0.973** | 0.9722 | 0.9408 | **0.7781** |
| **AD2**（subind p1.4 d20） | 0.973 | 1.000 | 0.9478 | 0.971 | 0.7405 |
| **AD3**（subind p1.8 d40） | 0.9722 | 0.9478 | 1.000 | 0.9708 | 0.7685 |
| **AC3**（subind p1.8 d20） | 0.9408 | 0.971 | 0.9708 | 1.000 | 0.7272 |
| **AC7**（industry p1.4 d40） | **0.7781** | 0.7405 | 0.7685 | 0.7272 | 1.000 |

`max_pair` = AD1×AD2 **0.973**；10/10 对全部 > 0.5；`max_mutually_below_subset` = **{`LL5dmv9a`}，size 1**，`max_subset_exact true`。

⇒ **`dps` 这一个指标只能交付 1 颗**（SELF_CORRELATION < 0.7 是硬闸）。AD2 虽然也 `failed_ra_count = 0`，但与 AD1 相关 0.973 ⇒ **二者只能取一，取 AD1**（S/2Y/DD/margin 四项全面占优）。

**★ 去相关层级补一级（原 7 级 → 8 级）**：

| 级 | 变了什么 | 实测相关性 | 出处 |
|---|---|---:|---|
| 1 | 设置档 | 0.72–0.99 | §38 |
| 2 | 构造（外层包裹 / p） | 0.75–0.99 | §38 |
| 3 | 同字段 + 不同**外层**分组 | 0.9938–0.9986 | §38 |
| **3.5（新）** | **同字段 + 不同内层分组** | **0.7272–0.7781** | **本节：AC7 `industry` vs AD1/AD2/AD3/AC3 `subindustry`** |
| 4 | 分桶 | 0.8482–0.9972 | §38 |
| 5 | 同族不同字段 | 0.3874–0.7293 | §38 |
| 6 | 字段族（跨机制、同数据集） | 0.3187–0.4184 | §38 |
| 7 | 跨数据集 | 0.0347–0.0690 | §38 |

⇒ **内层分组是「真」去相关杠杆**（把 0.99 拉到 0.73，效果比换外层分组强两个数量级），**但单独不够**（仍 > 0.7）。
**要拿到 10 颗互不相关的，必须走到第 5–7 级：换指标、换机制族、必要时换数据集。**

### 44.6 `analyst7` 指标网格**全量枚举**（客观步骤 2「全部字段完整梳理」的收口）

从本地 `field_catalog`（`get_field_catalog(region=EUR, dataset=analyst7)` → 1111 字段）按语法
`est_{12m,q}_<metric>_<stat>[_<asof>]` 机械解析：**1007 个 id 可解析，41 个 (horizon, metric) 格**。

**A. 具备完整 `{mean, mean_4wks_ago, std}` 三件套 ⇒ AD1 配方可直接套用：32 格**

| horizon | metric（`alphaCount` 为 `_mean` 字段的拥挤度） |
|---|---|
| **`12m`（23 个）** | `bps` 158 · `cps` 96 · `cpx` 100 · `csh` 28 · **`dps` 103 ✅已出全通过** · **`ebi` 116**（EBIT，档案 L482 已证强）· **`ebt` 191**（全表最高）· `ent` 95 · **`eps` 117** · `fcf` 49 · `gps` 131 · `grm` 26 · `nav` 65 · **`ndt` 156** · `ner` 155 · `net` 77 · `opr` 113 · `pre` 131 · `prr` 80 · `roa` 14 · **`roe` 187** · **`sal` 133** · `tbv` 3 |
| **`q`（9 个）** | `ebi` 3 · `ebt` 11 · `eps` 44 · `gps` 96 · `ner` 9 · `net` 38 · `pre` 8 · `prr` 10 · `sal` 9 |

全部 cov **0.5**、22 字段/格（`q` 侧 19–22）。加粗的 7 个 = **Batch AE 已派发**（44.7）。

**B. 三件套不全 ⇒ AD1 配方不可直接套用：9 格**
`est_12m_ebg`（只有 mean/median/std/high/low/num，**无任何快照字段**）、
`est_12m_ebs`（有 mean 的 28d/3mth/4wks 快照但**无 `std`**）、
`est_q_bps` / `est_q_dps` / `est_q_nav` / `est_q_ndt`（**无 `std`**）、
`est_q_ent` / `est_q_grm` / `est_q_opr`（**无快照 mean 或无 `std`**）。
⇒ 这 9 格要另设构造（如用 `median` 代替 `mean`、或用 `high`/`low` 做分歧度），**属未测面，不是死面**。

**C. 正则未覆盖的 200 个 id = 一整个「上调/下调」广度子族（未测机制轴）**
形态 `est_12m_<metric>_{raised,lowered,raisednum,lowerednum}_{1wk,1mth,4wks}`
（样本：`est_12m_bps_lowered_1wk`、`est_12m_bps_raisednum_1mth`、`est_12m_cps_lowered_1wk`、`est_12m_bps_raisednum_4wks`）。
⚠ **与 AB5 判死的 `dps_num`（总家数广度）不是同一族**：`raised`/`lowered` 是**带方向的**修正家数与修正比例，
经济含义是「上调家数占比」= 经典 **analyst revision breadth / diffusion** 指标，而 `num` 只是覆盖家数（无方向）。
⇒ **AB5 的判死不能外推到这一族**（按 §29.8 的方法论更正：「免测只适用于同指标的不同统计量，不适用于不同机制」）。
**这是 `analyst7` 内剩下最大的一块未测机制面（200 字段），记为 AE 之后的第二优先。**

### 44.7 Batch AE 设计（7 指标跨 6 机制族，AD1 配方逐字，只换 metric）

**选指标的判据不是 αC**：`analyst7` 上 αC 与 S **不单调**（实测 5 点：αC 3 → S 0.29 `tbv` · αC 49 → 0.76 `fcf` · αC 65 → **−0.03** `nav` · αC 100 → **−0.28** `cpx` · αC 103 → **1.71** `dps`，2/5 反例）
⇒ §39.4 的 αC 定律在本数据集**只是解释、不是筛选规则**（§40.3 的收窄在此再次生效）。
**实际判据 = 机制族距离**（去相关层级第 6 级 = 0.3187–0.4184，是唯一能支撑 10 颗的层级）+ 已知强弱先验。

| 腿 | metric | 经济含义 | 机制族 | αC | 选它的理由 | sim id |
|---|---|---|---|---:|---|---|
| **AE1** | `ebi` | EBIT 12m 前瞻估计 | 盈利（营业） | 116 | **档案 L482 `E5VKvGRG`（EBIT 4 周快照修正% + power3.0）已达 S 1.71 / F 1.16 双过**，只卡在 sub 0.64 / robust 0.54 / 2Y −0.04 ⇒ 本数据集内**已知第二个强指标**，且**从未在新档复测** | `1F84tF96c4K7co010uE8CemX` |
| **AE2** | `ebt` | 税前利润 | 盈利（税前） | **191** | 全表最高 αC；`ebi` 的同族兄弟 ⇒ 同时测「同族不同指标」落在层级第 5 级的哪一端 | `2BsdHZbWq4H0aYbnfLXoGJe` |
| **AE3** | `eps` | 每股盈利 | 盈利（每股） | 117 | 分析师修正文献的规范指标；`analyst_factor_signals` 的 `eps_y1`（αC 176）是那边的赢家 S 1.75 / 2Y 2.20 ⇒ **跨数据集同机制复现检验** | `4k82k746q4pQ9ofWXZmPyYb` |
| **AE4** | `sal` | 营收 | **收入（顶线）** | 133 | 与盈利族机制距离最远的一条 ⇒ **去相关主力** | `1hxwHr98M4l19aFSL9ixuNy` |
| **AE5** | `roe` | 净资产收益率 | **比率** | 187 | 比率族 = 分子/分母双估计的复合，与水平族结构不同（分母的修正会污染信号，是独立的风险面） | `3qX9omaSD4HxcJZBfcyGCvW` |
| **AE6** | `ndt` | 净债务 | **资产负债表** | 156 | 慢变量族代表。`dps`（每股派息）本身偏分配/资产负债侧 ⇒ 检验「慢变量也能有可用修正信号吗」 | `43dOHceoz4XN9sxdcs3QRlt` |
| **AE7** | `cps` | 每股现金流 | **现金流** | 96 | `dps` 的最近亲（同为每股口径、同属现金/分配族）⇒ **预期相关性最高，作为「团数下界」的对照腿** | `10CVdQ2lE4nMcng1djUIRyQi` |

**合规性逐条核过**：① 每条只用 **1 个指标的 3 个字段**，全部来自 `analyst7` 单数据集 ⇒ **ATOM（Single Dataset Alpha）合规**，
分组字段只用 `subindustry` 与 `market`（都在平台允许的 6 个内），无 `inst_pnl()` / `convert()`（那两个会被判为用了 pv1）；
② **单位安全**：`subtract(mean, mean_4wks_ago)` 同单位相减、`divide(·, std)` 同单位相除 ⇒ 无量纲，**全批无任何常数**
（`EUR-ANALYST-CONSENSUS-TARGETPRICE-DEAD` 的单位陷阱是 `add(std, 0.01)`，本批不存在该形态）；
③ 算子全部在 `get_operators(region=EUR)` 的 103 个 live 算子内，`signed_power` 的第二参数是位置参数（不是命名参数）；
④ 7 条 = 并发上限（Batch T 的第 8 条曾 429），派发 7/7 `ok:true`、无 429。

### 44.8 `preflight_expressions` 瞬时故障的可复用处置（新工具结论）

**现象**：21 字段的 7 条批返回 `valid: true`，但带
`warning: "Field pre-check skipped or incomplete: est_12m_eps_mean: get_datafields(offset=0): failed after 6 attempts"`，
且 `platform_field_count: 20`（`fields_checked` 有 21 项）。

**判据（沿用 §29.9 的规则）**：**`valid: true` + 非空 `warning` = 未验证**。`warning` 会**点名**具体哪个字段没打到平台，
`platform_field_count` 与 `fields_checked` 的差额就是未验证字段的个数。

**处置 = 按点名字段单独重跑一次 preflight**（一条表达式即可）。本轮实测：单条重跑立即
`platform_field_count: 3`、`unknown_fields: []`、**无 warning** ⇒ **是平台侧瞬时故障（6 次重试全失败），不是字段不存在。**

⚠ 两个参数名坑：① 表达式数组的参数名是 **`alpha_expressions`**，不是 `expressions`
（写错报 `params must have required property 'alpha_expressions'`）；
② `preflight` **完全不检查分组关键字**（`subindustry` / `market` / `country` 都不进 `fields_checked` 也不进 `builtin_fields`）
⇒ 铁律 ① 的覆盖面**不含分组字段面**；换新的分组关键字时仍需单独发 2 腿微批验证（本轮 `subindustry`/`market` 已由 AC3/AD1–AD3 实测确认可用）。

### 44.9 本节限定 / 新增的结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| **§39.2** | 四闸交集为空（本战役的**中心不可能性证明**） | **✗ 作废**：AD1 四闸全过 + prod 0.497（44.3）。有效范围收窄为「sub/S 余量 < 0.01 且 prod ≥ 0.70 的族」。**方法论教训：写「交集为空」必须逐条注明前提数值取自哪颗 alpha、哪个档** |
| **§40.13 / §42.10** | 可交付上限 = 1（形式）/ 0（期望） | **✗ 作废**：AD1 与 AD2 双双 `failed_ra_count = 0`。**上限改由团数决定，不由闸门决定**——`dps` 族团数 = 1（44.5），10 颗需 ~10 个不同指标 |
| （未登记） | prod 0.70–0.74 是 EUR analyst 塔的属性（6 轮库存 prod 扫描全得到「prod<0.7 clean = 0」） | **✗**：`analyst7` 三条腿 prod = **0.4203 / 0.4232 / 0.4970**，`[0.7,0.8)` 桶 **n = 0**（AD1 最高桶 `[0.4,0.5]` n=75）⇒ **prod 是数据集属性，不是区域/塔属性**。那 6 轮扫描的分母里**没有 `analyst7`** |
| 去相关层级（原 7 级） | 同字段 + 不同**外层**分组 = 0.9938–0.9986 | **补第 3.5 级**：同字段 + 不同**内层**分组 = **0.7272–0.7781**（44.5）⇒ 内层分组是真去相关杠杆（0.99 → 0.73），但**单独不够** |
| §29.8 维度表 | `dps` 3mth（1.08）弱于 4wks（1.15） | **新档复测同向但幅度全变**：3mth S **1.43** / 2Y **1.55** vs 4wks S 1.28 / 2Y 1.78 ⇒ 慢快照**抬 S +0.15、抬 returns +.0063、抬 pnl +11%，但砸 2Y −0.23**。对 ATOM（2Y 线 2.023）不可用；**对 REGULAR 常规通道（2Y 线 1.58）AC6 只差 0.03，属半活** |
| §43.5 | `÷std` 值 +0.63 S（AB1 vs AB7 无归一化） | **补对照腿**：`÷mean`（百分比修正）S **0.81**，比 `÷std` 低 **0.47**，且 L/S 1607/1213 严重多头倾斜 ⇒ **不是「有没有归一化」，而是必须按横截面分歧度（`std`）归一化**；按水平（`mean`）归一化只拿到一半，且会引入方向性偏斜 |
| （未登记） | CROWDING 是 OLD 档 2Y **2.01** 的功臣 | **✗ 归因错误**：AC4 隔离实测 CROWDING 在新档 S **0.91**（−0.37）/ 2Y **1.40**（−0.38）/ DD **0.1026**（近 2 倍恶化）。OLD 档的 2Y 2.01 应归给 **内层 `subindustry` + p1.4**（AC3 = 2.23、AC2 = 2.05 都单独超过了它） |
| （未登记） | 杠杆可加，可按单杠杆效应外推叠加结果 | **近似可加但递减**：S 预测 1.77 / 实测 1.71（**93%**）；2Y 预测 2.63 / 实测 2.41（**87%**）。机制是内层分组与 p 都压极端 z-score 的放大（p1.4 在 industry 基座 +0.23 S，在 subindustry 基座只 +0.16）⇒ **叠加外推打 7–13% 折扣** |
| §29.8 / §43.6 | `analyst7` 有 32 个指标、27 个未测 | **精确化**：41 个 (horizon, metric) 格，其中 **32 格具备完整 4wks 三件套**（12m 23 + q 9）、**9 格三件套不全**（需另设构造，属未测非死）、**另有 200 个 `raised`/`lowered` 方向性广度字段**属完全未测的独立机制轴（44.6 C）。AB5 判死的是**无方向**的 `num`，**不能外推到这一族** |
| （未登记） | `preflight_expressions` 的 `valid: true` 即字段已验证 | **✗**：`valid: true` + 非空 `warning` + `platform_field_count` < `fields_checked` = **未验证**；warning 会点名具体字段，单独重跑该条即可区分「平台瞬时故障」与「字段真不存在」（44.8） |

---

## 45. Batch AE 收割与「2Y 失效的两类成因」：把 10 颗目标从相关性约束转成 2Y 约束

**日期**：2026-10-20　**波次**：Batch AE（7 腿，指标扫描）　**库存**：52 → **66**
**一句话**：AD1 的配方逐字用于 7 个不同指标，**只有 `ebt` 一条全闸通过**（第 2 颗），
其余 6 条分成**两类互不相同的 2Y 失效成因**（单年 2022 拖累 vs 真实衰减）；
同时用 `compute_mutual_correlation` 证明**跨指标的相关性不是 10 颗目标的约束**（最大对 0.6613 < 0.7）。

### 45.1 收割表（7/7 `ok:true`，无 429；全部同配方，唯一变量 = 指标）

配方：`group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_<M>_mean, est_12m_<M>_mean_4wks_ago), est_12m_<M>_std), subindustry), 1.4), market)`
设置：EUR / TOP2500 / D1 / FAST / **decay 40** / trunc 0.08 / maxTrade ON / nanHandling ON / pasteurization ON / unitHandling VERIFY / 2014-01-01→2023-12-31 / FULL。

| 腿 | 指标 | id | S | F | 2Y | sub | ret | TO | DD | margin | pnl | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **AE2** | **`ebt`（EBITDA）** | **`e76xGOQO`** | **2.15** | **1.59** | 1.93 | **1.12** | **.0685** | .054 | **.0359** | **25.37 bp** | **7 064 269** | **0** ✅ |
| AE3 | `eps` | `1YjzKzp6` | 1.97 | 1.35 | **1.33** ✗ | 1.07 | .0584 | .054 | .0317 | 21.63 bp | 6 025 010 | 1（LOW_2Y） |
| AE4 | `sal` | `mLYV78n2` | 1.93 | 1.30 | **1.26** ✗ | 1.00 | .0566 | .0527 | .0337 | 21.48 bp | 5 838 094 | 1（LOW_2Y） |
| AE1 | `ebi` | `KPmEz7r8` | 1.69 | 1.10 | **1.38** ✗ | 1.13 | .0525 | .054 | .0346 | 19.42 bp | 5 415 613 | 1（LOW_2Y） |
| AE5 | `roe` | `KPmEzbA1` | 1.58 | 0.94 ✗ | 1.91 | **0.74** ✗ | .0442 | .0525 | .0308 | 16.84 bp | 4 561 151 | 2（F、SUB） |
| AE7 | `cps` | `vROvGlaa` | 1.52 ✗ | 0.90 ✗ | **1.34** ✗ | 1.12 | .0435 | .0541 | .0406 | 16.07 bp | 4 488 805 | 3（S、F、2Y） |
| AE6 | `ndt` | `d5KRz0q2` | **−1.08** | −0.53 | −1.61 | −0.80 | −.0301 | .0553 | **.3239** | −10.88 bp | **−3 107 808** | 4 ⇒ **判死** |

共同点：全部 `pyramids {effective 1, [EUR/D1/ANALYST, multiplier 1.3]}`、`MATCHES_PYRAMID ∈ pass`、
`pending [SELF_CORRELATION, DATA_DIVERSITY, PROD_CORRELATION, REGULAR_SUBMISSION, POWER_POOL_CORRELATION, MATCHES_THEMES]`、
`IS_LADDER_SHARPE` **不在任何名单**（ATOM 替代条款生效）。

### 45.2 ★★ 2Y 的两类失效成因（这一步决定后续该修谁、该判死谁）

| 指标 | id | 全期 S | 2021 | **2022** | **2023** | 2Y | 衰减比（末年/全期） | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `dps` ✅ | LL5dmv9a | 1.71 | 3.18 | **2.41** | **2.45** | **2.41** | **1.433** | 全闸过 |
| `ebt` ✅ | e76xGOQO | 2.15 | 2.61 | **1.55** | **2.46** | 1.93 | **1.144** | 全闸过 |
| `ebi` | KPmEz7r8 | 1.69 | 2.43 | **0.73** | **2.20** | 1.38 ✗ | **1.302** | **成因 A，可修** |
| `sal` | mLYV78n2 | 1.93 | 2.55 | **1.07** | **1.49** | 1.26 ✗ | 0.772 | 混合，边缘可修 |
| `eps` | 1YjzKzp6 | 1.97 | 2.23 | **1.31** | **1.39** | 1.33 ✗ | **0.706** | **成因 B，判死** |

**成因 A —— 单年（2022）拖累，可修**：`ebi` 衰减比 **1.302（完全没有衰减）**、本批**最优 sub 比 0.669**
（sub_universe_sharpe 1.13 / S 1.69）、2023 = **2.20** 单独就已越过文档推导线 2.023。**唯一缺陷是 2022 = 0.73。**
`sal` 同形但更轻（2022 1.07 / 2023 1.49）。
**成因 B —— 真实衰减，判死**：`eps` 从 2014 **4.23** / 2018 2.89 / 2017 2.75 / 2019 2.32 一路掉到 2022 1.31 / 2023 1.39，
衰减比 **0.706**，近三年均值 1.64 ⇒ 最经典的修正指标已被套利掉，**不是某一年的事故，是整条曲线的下坡**。
⚠ αC 的反证继续累积：`eps` αC 117（中位）衰减，`ebt` αC **191**（全表最高）却是赢家 ⇒ **αC 不是过滤器**（第 3 个反例）。

**2022 的机制归因**：ECB 最陡加息年 + 能源冲击 ⇒ 经营利润类一致预期被**共同的宏观因子**整体下修
⇒ 修正的**横截面**离散度里几乎没有特质信息。这是**制度尺度（regime-scale）的缺陷**，
⇒ 对症杠杆是**时序标准化**（`ts_zscore(·, 252)`），而不是再换一个指标。

### 45.3 ★★★ 相关性约束不成立：跨指标最大对 0.6613 < 平台 SELF 线 0.7

`compute_mutual_correlation(["LL5dmv9a","e76xGOQO","1YjzKzp6","mLYV78n2","KPmEz7r8","KPmEzbA1","vROvGlaa"])`
→ `local_calculation true` / `num_points 1021` / `years 4` / `missing_pnl []` / **零槽位成本**：

| | dps | ebt | eps | sal | ebi | roe | cps |
|---|---:|---:|---:|---:|---:|---:|---:|
| **dps** | 1 | **.3347** | .4113 | **.2843** | **.3225** | **.3613** | **.2273** |
| **ebt** | .3347 | 1 | .5921 | .5888 | **.6613** | .4576 | .3577 |
| **eps** | .4113 | .5921 | 1 | .5070 | **.6587** | .5033 | .3103 |
| **sal** | .2843 | .5888 | .5070 | 1 | .4666 | .3757 | .2493 |
| **ebi** | .3225 | **.6613** | **.6587** | .4666 | 1 | .4808 | .3374 |
| **roe** | .3613 | .4576 | .5033 | .3757 | .4808 | 1 | .2649 |
| **cps** | .2273 | .3577 | .3103 | .2493 | .3374 | .2649 | 1 |

- `max_pair` = **ebt × ebi = 0.6613** ⇒ **21 对全部 < 0.7** ⇒ **相关性不是 10 颗目标的约束**。
- `max_mutually_below_subset(0.5)` = {dps, sal, ebi, roe, cps}，size 5（精确解）。
- ⇒ **AD1 单族团数 = 1 的结论不能外推**（§42.10 / §44.5）。跨不同指标，rung-5 相关性落在 **0.227–0.661**。
- ⇒ **决定 10 颗上限的是 2Y 闸，不是去相关。** 这是本波最重要的解锁。

### 45.4 ★★ 2Y 线的实测裁定：平台执行 **1.58**，文档推导的 2.023 不成立

`single-dataset-alphas` 文档载 D1 的 2Y cutoff = 2.38，「TO < 30% 时 IS Sharpe Ladder 的 PASS_THRESHOLDS × 0.85」
⇒ 推导操作线 **2.023**。**Batch AE 四条腿直接证伪**：AE1/AE3/AE4/AE7 的 `LOW_2Y_SHARPE` **limit 均为 1.58**
且都计入 `ra_failed_checks`；而 AE2 的 1.93 **未被计入**。若线是 2.023，AE2 必被计入。
⇒ **IS 阶段平台执行 1.58。**
⚠ **残余不确定性**：`REGULAR_SUBMISSION` 仍 pending、提交端点死 404 ⇒ **提交阶段是否改判无法核验**。
⇒ **AD1（2.41）越过所有读数（1.58 / 2.023 / 2.38）；AE2（1.93）只越过 1.58** ⇒
**AD1 提交更安全、AE2 IS 更强，两者互补而非替代。**

### 45.5 ★★ `analyst7` 字段语义（机器核验，更正一处我自己的错误）

**`ebt` = EBITDA（息税折旧摊销前利润），不是税前利润。** catalog 原文：
"Mean analyst estimate of EBITDA regarding the next 4 quarters"。同族易混字段的正确映射：

| 字段 | 含义 | αC | uC | | 字段 | 含义 | αC | uC |
|---|---|---:|---:|---|---|---|---:|---:|
| `ebi` | EBIT | 116 | 27 | | `pre` | pre-tax profit | 131 | 38 |
| **`ebt`** | **EBITDA** | **191** | **41** | | `prr` | pretax profit as reported | 80 | 21 |
| `ner` | net profit as reported | 155 | 48 | | `net` | net income | 77 | 23 |
| `gps` | GAAP EPS | 131 | 44 | | `csh` | cash EPS | 28 | 17 |
| `ent` | enterprise value | 95 | 23 | | `nav` | net asset value | 65 | 26 |
| `roa` | return on assets (%) | 14 | 13 | | `grm` | gross margin (%) | 26 | 11 |
| `bps` | book value per share | 158 | 37 | | `sal` | sales/revenue | 133 | 38 |
| `dps` | dividend per share | 103 | 36 | | `fcf` | free cash flow per share | 49 | 15 |
| `cpx` | capital expenditure | 100 | 36 | | `opr` | operating profit | 113 | 37 |

18 个指标全部具备 `{mean, mean_4wks_ago, std}` 三件套、**cov 均为 0.5**。
⚠ 该错误曾写进 `reports/robustness_20261020.md` 的 AE2 节与台账 `robustness_e76xGOQO.economic_rationale`，
**已双向更正**（报告加口径更正块 + 台账 `merge` 重写 rationale 并留 `field_semantics_note`）。

---


### 45.6 ★ 方向性广度族的命名更正（推翻 §44.6 C 的 `_<asof>` 描述）

**`est_12m_<M>_raised_4wks` / `_lowered_4wks` 不存在。** 24 个指标各有 **n = 6** 个广度字段，
但**不是 4×3 笛卡尔积**：

| 形态 | 可用 asof | 例（`ebt`） | 说明 |
|---|---|---|---|
| `raised` / `lowered`（方向哑变量） | **仅 `_1wk`** | `est_12m_ebt_raised_1wk` | 周度方向 |
| `raisednum` / `lowerednum`（家数计数） | `_1mth` / `_4wks` | `est_12m_ebt_raisednum_4wks`（αC **186**，cov .5）<br>`est_12m_ebt_lowerednum_4wks`（αC **82**，cov .5） | 月/四周计数 |

⇒ **可用的广度构造 = `raisednum`/`lowerednum` @ `_1mth`/`_4wks`，或 `raised`/`lowered` @ `_1wk`。**
`num`（无方向）已在 AB5 判死，**该结论不能外推到有方向的这一族**（仍未测）。

### 45.7 ★ `q` 频域配方就绪（完全未测的整条轴）

`est_q_<M>_mean` / `_mean_4wks_ago` / `_std` **在 9 个指标上全部存在**：
`ebi` · `ebt` · `eps` · `gps` · `ner` · `net` · `pre` · `prr` · `sal`。
⇒ `est_12m` 的配方可**逐字**套到季度前瞻口径，构成一条**完全未测**的轴（5 条 `est_q` 腿从未进过任何波次）。

### 45.8 §42.10 提案格的证伪（对本战役自身提案的否证）

§42.10 曾提出一格的候选判据：「最优年的多空 book 朝向 L/S 落在其余年份区间之外 ⇒ 过拟合签名」。
逐值复算后：AD1 的 2021 L/S **0.862 < 其余九年最小值 0.8788** ⇒ **在区间之外（触发）**；
AE2 的 0.833 落在其余区间 [0.9125, 1.1066] 之外；V5 的 0.870 也在其余区间之外。
⇒ **三例全部触发，且三例的最优年都是 2021** ⇒ 该格检出的是 **EUR 2021 的制度性空头倾斜**（book 普遍偏空），
**不是某个 alpha 的过拟合签名** ⇒ **该提案在本数据集上无判别力，不予采纳。**
（更正记录：本战役初稿曾口算判 AD1 「落在区间内」，逐值复算证伪，已写入 `reports/robustness_20261020.md`。）

### 45.9 Batch AF：按归因结果派发的 7 腿（2026-10-20，已派发 7/7 `ok:true`）

**设计原则**：① 成因 A 用**时序标准化**（regime 杠杆）修，不换指标；② 已验证配方向**未测指标 / 未测频域**扩展
（rung-5 去相关 0.227–0.661，是当前最有效的多样性来源）；③ 不碰 prod 杠杆（`analyst7` 的约束几何是 S/F/2Y-bound，
prod 余量 .42–.62）。

| 腿 | 指标 | 位置 ② 变换 | 目标 |
|---|---|---|---|
| AF1 | `bps`（αC 158） | `divide(·, std)` | 指标扩展（每股/账面族，最接近已过闸的 `dps`） |
| AF2 | `pre`（αC 131） | `divide(·, std)` | 指标扩展（税前利润） |
| AF3 | `opr`（αC 113） | `divide(·, std)` | 指标扩展（经营利润） |
| AF4 | `ner`（αC 155） | `divide(·, std)` | 指标扩展（报表净利） |
| AF5 | `est_q_ebt` | `divide(·, std)` | **频域扩展**（季度前瞻，整条轴未测） |
| AF6 | `ebi` | **`ts_zscore(·, 252)`** | **修 2022**（成因 A：2022 0.73 / 衰减比 1.302 / 2023 2.20） |
| AF7 | `ebt` | **`ts_zscore(·, 252)`** | **抬 AE2 的 2Y**（1.93 → 目标 > 2.023，消除唯一实质风险） |

预检：`preflight_expressions(alpha_expressions=[7 条])` → `valid true` / `unknown_fields []` /
`fields_checked 19 = platform_field_count 19` / `any_changed false` ⇒ **无未验证字段**。
（注：preflight 默认 region=USA，但 19 个字段的 EUR 存在性已由 §45.5 的 EUR catalog 全量 dump 机器核验。）

### 45.10 本节限定 / 新增的结论

| 旧位置 | 旧结论 | 更正 |
|---|---|---|
| §42.10 / §44.5 | `dps` 族团数 = 1 ⇒ 可交付上限由团数决定（~10 个不同指标） | **方向对、约束错**：团数确实是多样性来源，但**相关性不是约束**——跨 7 指标 21 对最大 **0.6613 < 0.7**（45.3）。**真正的约束是 2Y** |
| §39.2 / §44.9 | 四闸交集为空（已收窄为「sub/S 余量 < 0.01 且 prod ≥ 0.70」） | **再收窄**：AE2 以 2Y 1.93 全闸通过、prod .6236 ⇒ 该不可能性也**不覆盖 2Y ∈ [1.58, 2.023) 的候选**；残余不可能性范围 = 「sub/S < 0.01 ∧ prod ≥ 0.70 ∧ 2Y < 1.58」 |
| （未登记） | 文档推导的 ATOM 2Y 操作线 = 2.023（2.38 × 0.85） | **✗ IS 阶段实测 1.58**：四条失败腿的 `LOW_2Y_SHARPE.limit` 均为 1.58 且被计入，AE2 的 1.93 未被计入（45.4）。提交阶段仍未可核（`REGULAR_SUBMISSION` pending + 404） |
| （未登记） | 2Y 不足 = 强度不够，应整体加强 | **✗ 必须分成两类**：成因 A（单年拖累，衰减比 > 1 ⇒ 可修，用 regime 杠杆）vs 成因 B（衰减比 < 0.75 ⇒ 真实衰减 ⇒ 判死）。`ebi` 衰减比 1.302 却 2Y 1.38，`eps` 衰减比 0.706（45.2） |
| §44.6 C | 广度族有 200 个 `_<asof>` 字段，可自由取 asof | **✗ 命名更正**：`raised`/`lowered` 只在 `_1wk`；`raisednum`/`lowerednum` 只在 `_1mth`/`_4wks`；`_4wks` 无方向哑变量（45.6） |
| §29.8 αC 表 | αC 越高越拥挤、越可能失效 | **反例累积到 3 个**：`nav` αC 65 → −0.03、`cpx` αC 100 → −0.28、`eps` αC 117 衰减、而 `ebt` αC **191** 全闸过 ⇒ **αC 不是过滤器**（45.2 / 45.5） |
| §42.10 提案格 | 最优年 L/S 出区间 = 过拟合签名 | **✗ 证伪**：V5 / AD1 / AE2 三例全触发且最优年同为 2021 ⇒ 检出 EUR 2021 制度性空头倾斜，无判别力（45.8） |
| （未登记） | `ebt` = 税前利润（EBT） | **✗**：`est_12m_ebt_*` = **EBITDA**。`pre` = pre-tax profit、`prr` = pretax profit as reported（45.5） |

---

## 46. Batch AF 收割：`ts_zscore` 时标标准化**不是**修 2022 的杠杆（假设证伪）

**日期**：2026-10-20　**波次**：Batch AF（7 腿：4 指标扩容 + 2 时标标准化 + 1 q 频域）　**库存**：66 → 72（+6 收割，AF5 仍在飞）
**一句话**：为修 `ebi` / `pre` 的 **2022 单年坍塌**而设计的 `ts_zscore(·, 252)` 杠杆被实测证伪——
它把 2022 抬了一点，却把 **2023 直接打到 0 附近**，全期 S 腰斩；同时 `pre` 确认为 Mode A 第三例，
`bps` / `ner` / `opr` 三条新指标全部不达标。

### 46.1 收割表（6/7 `ok:true`；AF5 `q_ebt` 仍在飞）

配方同 §45.1（decay 40 / FAST / TOP2500 / D1 / trunc .08 / maxTrade ON / nanHandling ON）。

| 腿 | 变量 | id | S | F | 2Y | sub | ret | TO | DD | margin | pnl | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **AF2** | `pre`（税前利润） | `akVEwmpW` | **1.92** | **1.32** | 1.39 ✗ | 0.94 ✗ | .0588 | .0536 | .0469 | 21.94 bp | 6 069 491 | 2（SUB、2Y） |
| AF4 | `ner`（净利 as reported） | `58jkYnOo` | 1.24 ✗ | 0.68 ✗ | 0.95 ✗ | 0.61 ✗ | .0379 | .0528 | .0465 | 14.35 bp | 3 912 153 | 4 |
| AF1 | `bps`（每股净资产） | `vROv6Eod` | 1.12 ✗ | 0.56 ✗ | 1.30 ✗ | 0.57 ✗ | .0310 | .0528 | .0405 | 11.73 bp | 3 197 821 | 4 |
| AF3 | `opr`（营业利润） | `vROv67GA` | 0.15 ✗ | 0.03 ✗ | 0.76 ✗ | 0.13 | .0053 | .0655 | **.1381** | 1.63 bp | 551 105 | 3 ⇒ **判死** |
| AF6 | `ebi` × `ts_zscore252` | `bl8dn0LK` | 0.47 ✗ | 0.13 ✗ | 0.25 ✗ | 0.07 ✗ | .0098 | .0554 | .0454 | 3.53 bp | 1 008 487 | 4 ⇒ **判死** |
| AF7 | `ebt` × `ts_zscore252` | `vROv6E9d` | 0.85 ✗ | 0.33 ✗ | 1.01 ✗ | 0.39 ✗ | .0188 | .0551 | .0392 | 6.85 bp | 1 945 122 | 4 ⇒ **判死** |

### 46.2 ★★★ 假设证伪：`ts_zscore(·, 252)` 在修 2022 的同时摧毁 2023

| 结构化对比 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | **2022** | **2023** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ebi` 基准（AE1 `KPmEz7r8`） | — | — | — | — | — | — | — | 2.43 | **0.73** | **2.20** |
| `ebi` + tsz（AF6） | 0.61 | 0.39 | 0.85 | 2.62 | −0.47 | 0.51 | −0.62 | 1.18 | **0.69** | **−0.28** |
| `ebt` 基准（AE2 `e76xGOQO`） | 3.36 | 2.68 | 1.53 | 3.27 | 1.58 | 2.79 | 0.96 | 2.61 | **1.55** | **2.46** |
| `ebt` + tsz（AF7） | −0.51 | 1.39 | 1.25 | 1.11 | 1.01 | 0.79 | −0.53 | 2.24 | **1.81** | **−0.01** |

- **2022 确实被抬了**（`ebt` 1.55 → **1.81**，+0.26；`ebi` 基本不动 0.73 → 0.69）。
- **但 2023 被摧毁**（`ebt` 2.46 → **−0.01**；`ebi` 2.20 → **−0.28**，各掉 2.4+）。
- 净效应：全期 S `ebi` **1.69 → 0.47（−72%）**、`ebt` **2.15 → 0.85（−60%）**。
- ⇒ **「2022 是制度尺度缺陷、对策是时序标准化」这条假设被该杠杆格式证伪。**
  真实的读数是：`ts_zscore` 把「相对自己过去一年的修正幅度」当作信号，而 2023 的修正幅度恰好处于**低波动常态**
  ⇒ 分母（过去一年波动）大、分子（当期修正）小 ⇒ 全横截面被压扁，信号消失。**它修的是「哪一年」，代价是全部年份。**

### 46.3 ★★ `pre` = Mode A 第三例；2022 坍塌程度按「现金/分配 → 应计」单调排列

`pre` 逐年：2014 **4.77** / 2015 2.21 / 2016 0.26 / 2017 2.96 / 2018 1.90 / 2019 2.03 / 2020 0.94 / 2021 2.55 / **2022 0.48** / **2023 2.58**。
⇒ 与 `ebi` 同形（单年 2022 拖累，2021 与 2023 都很强），**但多一个缺陷**：sub 比 **0.4896**
（0.94 / 1.92 < 0.5196 的比率线）⇒ `pre` 的 SUB 不是「差一点」，是**比率不达标**，修 S 也治不好。

**2022 年的横截面读数排序**（同一配方、同一窗口，只换指标）：

| 指标 | `dps` | `ebt` | `eps` | `sal` | `ebi` | `pre` | `ner` | `opr` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 Sharpe | **2.41** | **1.55** | 1.31 | 1.07 | 0.73 | 0.48 | 0.35 | 0.08 |
| 2023 Sharpe | 2.45 | **2.46** | 1.39 | 1.49 | **2.20** | **2.58** | 1.63 | 1.45 |

- 2022 的强弱**几乎完美地按「现金/股东分配口径 → 应计口径」排列**：`dps`（分红）> `ebt`（EBITDA）> `eps` > `sal` > `ebi` > `pre` > `ner` > `opr`。
- **2023 则几乎全部恢复**（除 `eps` 1.39 的真实衰减）⇒ **2Y 闸（2022+2023）实际是在惩罚「2022 那一年」**。
- ⇒ 下一阶段的正确问法不是「再换一个指标」，而是**「有没有一种度量在 2022 不依赖横截面修正幅度」**。
  候选：**方向性广度**（`raisednum - lowerednum`，数人头而非数幅度）——它天然对「整体下修」免疫，
  因为横截面比的是**谁被上调/下调的分析师更多**，而不是修正了多少。**这是 §44.6 C 登记、至今完全未测的独立机制轴。**

### 46.4 指标格扫描进度

- **12m 幅度族（三件套齐备，机器核验 18 个）**：已测 13（`dps` ✅ / `ebt` ✅ / `ebi` / `eps` / `sal` / `roe` / `ndt` / `cps` / `bps` / `pre` / `opr` / `ner` + `fcf` 属早前结构），
  **本轮补测 5**（`roa` / `grm` / `csh` / `net` / `prr`，Batch AG），**再补 4**（`fcf` / `ent` / `cpx` / `gps`，Batch AH 的幅度臂）。
- **q 频域**：9 格三件套齐备，`q_ebt` 在飞（AF5），其余 8 格未测。
- **方向性广度族**：**200 个 `raised`/`lowered` 字段**（`raised_1wk` / `lowered_1wk` / `raisednum_1mth` / `raisednum_4wks` / `lowerednum_1mth` / `lowerednum_4wks` × 指标），
  **完全独立的机制轴，至今零测试**。§44.9 末行已登记：AB5 判死的是**无方向**的 `num`，不可外推到有方向族。

### 46.5 在飞波次设计（2026-10-20 派发，均 `ok:true`、无 429）

**Batch AG**（multisim `4p9M2n7Md52Qcju15aXVAbhs`，5 腿）：12m 幅度族剩余低拥挤指标
`roa`(αC 14) / `grm`(26) / `csh`(28) / `net`(77) / `prr`(80)，配方逐字同 §45.1。

**Batch AH**（multisim `amJpL9jd4AIaqlIUTyAie6`，8 腿）：

| 腿 | 机制 | 表达式骨架 |
|---|---|---|
| AH1–AH4 | **方向性广度扩散** | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_M_raisednum_4wks, est_12m_M_lowerednum_4wks), add(est_12m_M_raisednum_4wks, est_12m_M_lowerednum_4wks)), subindustry), 1.4), market)`，M ∈ {`ebt`, `dps`, `pre`, `ebi`} |
| AH5–AH8 | 12m 幅度族收官 | `fcf` / `ent` / `cpx` / `gps`，配方同 §45.1 |

AH1–AH4 的经济含义：**净上调分析师占比**（diffusion index）。它把「有多少人上调」与「上调了多少」解耦，
在整体下修的年份（2022）里，横截面上仍然能区分「被少数人下调」与「被多数人下调」——这正是幅度族在 2022 丧失的信息。
预检：`valid: true` / `unknown_fields: []` / `fields_checked 20 = platform_field_count 20` / `any_changed: false`。

### 46.6 本节新增 / 更正结论

| 位置 | 旧结论 | 更正 |
|---|---|---|
| §45.2 | 2022 是制度尺度缺陷，对策 = `ts_zscore(·, 252)` | **✗ 杠杆证伪**（46.2）：2022 +0.26 但 2023 −2.47，全期 S 腰斩。**制度假设本身仍未被排除**，被排除的是这种「用过去一年波动做分母」的实现 |
| §45.2 | `pre` 属 Mode A | **部分更正**：是 Mode A（单年坍塌），但 **sub 比率 0.4896 < 0.5196** ⇒ 两个缺陷，不是「只差 2Y」 |
| （未登记） | 2Y 闸筛的是「近期强度」 | **精确化**：2Y = 2022 + 2023，而 **2023 几乎全部指标都恢复**（1.39–2.58），**真正的筛子是 2022 一年** |
| （未登记） | `opr` 与 `ebi` 同族，应同向 | **✗**：`opr` 2019 **−1.49** / 2020 **−1.40** / DD .1381，与 `ebi` 完全不同向 ⇒ **营业利润口径在 EUR 是不稳定指标，判死** |
| （未登记） | `bps` 是账面价值类，应接近 `dps` 的稳健性 | **✗**：`bps` 2018 −0.64、全期 S 1.12 ⇒ **「现金流/分配」的稳健性不能外推到「账面价值」** |

---

## 47. 网格收口：严格三件套只有 **32 格**（23×12m + 9×q），并派发补齐波 + decay-80 2Y 波

**日期**：2026-10-20（凌晨）　**状态**：Batch AI（10 腿）/ AJ（5 腿）已派发；AF5 / AG / AH 仍在飞
**一句话**：§45.7 与 §46.4 的「24×12m + 13×q」是把 `_mean_4wks_ago` 当唯一判据数出来的；按**严格三件套**
（`mean` + `mean_4wks_ago` + `std`）重算，真实配方就绪格是 **23 + 9 = 32**。差额里 `q_dps` / `q_nav` /
`12m_ebs` 都**缺 `_std`** ⇒ `divide(·, std)` 这一层根本无法构造，它们不属「未测」，属「不可测」。

### 47.1 严格三件套的机器核验（`analyst7` 1111 字段，EUR catalog）

| 频域 | 就绪指标 | 数量 | 未测格 |
|---|---|---:|---|
| `est_12m` | bps, cps, cpx, csh, dps, ebi, ebt, ent, eps, fcf, gps, grm, nav, ndt, ner, net, opr, pre, prr, roa, roe, sal, **tbv** | **23** | **`tbv` / `nav`**（其余 21 格已在 AE/AF/AG/AH 内） |
| `est_q` | ebi, ebt, eps, gps, ner, net, pre, prr, sal | **9** | **8 格**（`q_ebt` = AF5 在飞） |

**被剔除的三个「看似就绪」格**（全部缺 `std`，已逐字段确认）：

| 字段 | 缺什么 | 语义 | 处置 |
|---|---|---|---|
| `est_12m_ebs_*` | **无 `_std`** | **EBITDA **per share**（`ebt` = EBITDA 总额） | 不可套本配方；**语义已机器确认**，纠正 §46.4 的「ebs 含义未知」 |
| `est_q_dps_*` | **无 `_std`** | 每股股息（下一季度） | 不可套本配方；**这不是 `dps` 的 q 类比**，§47.3 的 q 波不包含它 |
| `est_q_nav_*` | **无 `_std`** | 每股净资产（下一季度） | 同上 |

**方法论教训**：`grep '_mean_4wks_ago'` 数出来的格数会**系统性高估**——`mean` 与 `mean_4wks_ago` 常成对出现，
`std` 才是离散度的稀缺件。凡声称「N 个指标可套同一配方」，必须**逐格断言三件套**，不能只查一个后缀。

### 47.2 Batch AI：把剩余 10 格一次补齐（`2dbXOw3vX4JObIgwKYSRrsE`）

配方与 §45.1 **逐字相同**（EUR / TOP2500 / D1 / decay 40 / FAST / trunc .08 / maxTrade ON / nanHandling ON）。

| 腿 | 格 | 机制假设 |
|---|---|---|
| AI1 | `12m_tbv` | 有形账面价值 —— `bps`（S 1.12）的「剔无形」版本；检验 §46.6 的「账面价值不可外推」是否也适用于有形口径 |
| AI2 | `12m_nav` | 净资产价值 —— αC 65 的冷门格，`opr` 的教训要求单独实测而非按族外推 |
| AI3 | `q_ebi` | 季度前瞻 EBIT |
| AI4 | `q_eps` | 季度前瞻 EPS（最经典的修正口径） |
| AI5 | `q_gps` | 季度前瞻 GAAP EPS |
| AI6 | `q_ner` | 季度前瞻报表净利 |
| AI7 | `q_net` | 季度前瞻净利润 |
| AI8 | `q_pre` | 季度前瞻税前利润 |
| AI9 | `q_prr` | 季度前瞻报表口径税前利润 |
| AI10 | `q_sal` | 季度前瞻营收 |

**q 轴的经济含义**：`est_q` 的参照期是**下一季度**，`est_12m` 是**未来四季度**。前者对**近端修正**更敏感、
后者更平滑；若 2022 的坍塌源于「年度口径把 2022 的宏观下修与 2023 的上修混在一个窗口里」，
q 口径应该表现出**不同的年度形状**——这是本波要检验的，不是「换字段碰运气」。

### 47.3 Batch AJ：decay 80 作为 **2Y 杠杆**（`3Xy2DOfnt4QYaYdd47t1EAj`）

**这不是盲扫 decay**——它有 AC 批的定量斜率支撑（§44.1 杠杆隔离表，两条独立读数）：

| 对照 | Δdecay | ΔS | Δ2Y |
|---|---:|---:|---:|
| AC1 − AB1（p1.8） | 20 → 40 | **+0.02** | **+0.13** |
| AC7 − AC2（p1.4） | 20 → 40 | **+0.01** | **+0.11** |

⇒ **decay 对 S 近乎中性、对 2Y 正斜率**，且斜率与 p 无关。AD1 vs AD2 再确认（d40 比 d20 2Y +0.07、DD/margin 全优）。
本族 prod 基线 0.42–0.62，离 0.70 墙有 0.08–0.28 余量，**decay 上调带来的 prod 上升（≈+0.03/40 units）不构成风险**。

按 +0.13/20 units 线性外推（打 §44.2 的 7–13% 折扣），d80 相对 d40 的 2Y 增量为 **+0.23 ~ +0.26**，S 变化 ±0.05：

| 腿 | 指标 | d40 读数（S / 2Y） | d80 外推 2Y | 判定目标 |
|---|---|---|---:|---|
| AJ1 | `pre` | 1.92 / **1.39** | 1.62–1.65 | 2Y 过线；**但 sub 比率 0.4896 仍需同时修复**（§46.3） |
| AJ2 | `ebi` | 1.69 / **1.38** | 1.61–1.64 | 成因 A 最纯的一例（衰减比 1.302、2023 2.20） |
| AJ3 | `eps` | 1.97 / **1.33** | 1.56–1.59 | 贴线；§45.2 判其为成因 B（衰减比 0.706）⇒ 若 d80 救活，**推翻「成因 B 判死」** |
| AJ4 | `sal` | 1.93 / **1.26** | 1.49–1.52 | 外推不足以过线；作为斜率校准腿 |
| AJ5 | `dps`（对照） | 1.71 / **2.41** | 2.64–2.67 | 检验斜率外推是否成立；顺带放大交付余量 |

⚠ **外推的风险点如实登记**：线性斜率的实测区间只覆盖 decay 20→40。若 decay 对 2Y 是**凸函数**（饱和或反向），
d80 会低于外推值；§29.1 在另一个族（`netprofit_y2_estimate_change_3mo`）上测到 **decay 峰值在 40、80 已越过峰值**。
两族结论冲突 ⇒ **必须实测，不能按斜率直接交付**。本波的用途是**判定斜率在哪一档转弯**，不是宣布 d80 可用。

### 47.4 论坛取证（本轮新增，两条可复用）

检索：`search_forum_posts(search_query="分析师 预期修正")`，命中 40+ 帖。两条与当前瓶颈直接相关：

**A. `trade_when` 门控：把「修正幅度」当触发条件而不是评分**（作者 GZ47187，2026-09-30，0 赞，原帖 43878933562391）
作者有 242 颗 ACTIVE、其中 Analyst/Broker 45 颗、平均 Sharpe 1.68，给出的 IND 构造是：

```
trade_when(
  abs(ts_zscore(ts_av_diff(winsorize(ts_backfill(field, 120), std=4), 22), 66)) > 1.5,
  ts_av_diff(winsorize(ts_backfill(field, 120), std=4), 22),
  0
)
```
IND TOP500 / delay 1 / decay 6 / trunc .08 / INDUSTRY ⇒ **S 2.48 / F 2.25 / TO .0693 / margin 29.7 bp**。
作者自陈阈值 1.0 / 2.0 未测。**对本战役的意义**：我们此前把 `ts_zscore` 当**分母**（AF6/AF7，已证伪），
而论坛把它当**门控**——两者数学上完全不同：分母会**压缩所有个股**的信号，门控只**剔除不极端的日子**。
⇒ **§46.2 的证伪不能外推到门控用法**。若 AJ 的 decay 斜率停滞，下一波按此构造（外层门控、内层保留 `÷std`）。

**B. EUR 的节奏必须比 USA 慢**（同帖，作者实测）：同一 `anl16_clusterestsup` 思路，
USA TOP3000 用 `ts_av_diff(...,5)` ⇒ S 4.73 但 TO .6585 / margin 7.1 bp（不可复制）；
EUR TOP2500 必须加 `ts_decay_linear(...,5)` + decay 7 + `quantile` 才得到 S 2.37 / TO .0846 / margin 16.4 bp。
⇒ 与我们"decay 40 才把 TO 压到 5%"的实测同向（EUR 的更新频率与覆盖更低）。**论坛数字不可直接搬到 EUR/analyst7**，
但"EUR 需要更慢的平滑"这一条是**独立来源的交叉验证**。

**C. 一条必须标注为「仅假设」的帖子**（XH93773，2026-09-21，29 赞，43638690009495）：
「把修正方向与参与广度分开：少数观点大幅调整 vs 多数观点小幅同向调整可能对应不同信息过程」。
**原帖自陈「仍是研究假设，尚无配对回测结论」** ⇒ 它**不能**作为 AH 广度波的理论依据引用，
只能作为与我们 §46.3 问法同源的**问题表述**。

### 47.5 本节新增 / 更正结论

| 位置 | 旧结论 | 更正 |
|---|---|---|
| §45.7 | `est_q` 就绪 **9** 个指标 | **✓ 数量对，但原因错**：不是因为"9 个存在 mean_4wks_ago"，而是这 9 个**同时有 `std`**。13 个有 `mean_4wks_ago` 的格里有 4 个（`dps`/`nav`/`tbv`/`ebs` 的 q 版）缺 `std`；`q_dps` 实际**不可构造** |
| §46.4 | 「12m 未测 = `ebs` / `tbv` / `nav`（3）」 | **✗ 改为 2**：`ebs` 无 `std`，不可套本配方（其语义已确认为 **EBITDA per share**） |
| §46.4 | 「q 频域 9 格三件套齐备」 | **✓**（严格三件套口径下成立）；但 §45.7 的 9 与 13 两个数字曾在同节并存，以**严格三件套的 9** 为准 |
| （未登记） | decay 40 是本族最优，无需再调 | **待测更正**：AC 实测 decay 20→40 = **+0.13 2Y / +0.02 S**，斜率方向明确；40→80 从未测过。§29.1 的「峰值 40」来自**另一个族**，不能外推 |
| （未登记） | `ts_zscore` 已被证伪，此路不通 | **✗ 用法未穷尽**：被证伪的是**分母**用法（AF6/AF7）。论坛的**门控**用法（`trade_when(abs(ts_zscore(R,66))>1.5, R, 0)`）在 IND 实测 S 2.48 / F 2.25，尚未在 EUR/analyst7 上测 |

---

## 48. AF5 收割：**q 频域在本配方下基本无信号**（`q_ebt` 实测），AI 的八条 q 腿改判为「确认死亡」而非「发现」

**日期**：2026-10-20（凌晨）　**状态**：AF 批 7/7 收完；AI / AJ / AK 在飞

### 48.1 实测读数

`AF5` = `q_ebt`（`est_q_ebt_*` 三件套，其余构造与基准配方逐字相同），alpha id **`E5VexaWr`**：

| S | F | 2Y | sub | ratio | ret | TO | DD | margin | L/S | pnl | failed_ra_count |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **0.27** | **0.08** | **0.02** | 0.53 | 1.963 | .0098 | .0671 | .0820 | .000294 | 1417 / 1402 | 1 016 174 | **3** |

失败项：`LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE`（PPA 通道失败项 `LOW_SHARPE`）。

**逐年 Sharpe**：2014 0.30 · 2015 0.43 · 2016 0.11 · 2017 **−0.11** · 2018 **−0.49** · 2019 0.35 · 2020 0.42 · **2021 1.52** · 2022 **−0.22** · 2023 0.29。

### 48.2 归因：F 不达标是 returns 的机械结果，不是算子问题

`TO .0671 < 0.125` ⇒ 平台 `F = S × sqrt(ret / 0.125)`。代入实测：`0.27 × sqrt(0.0098/0.125) = 0.0756`，实测 F **0.08** —— **完全吻合**。
⇒ 在这条腿上**任何算子替换都不可能把 F 推过 1.0**；要过 F 必须先让 `ret ≥ 0.04275`（对应 S 1.58 时的盈亏平衡线），
而实测 ret 只有 **0.0098**，差了 **4.4 倍**。这与 §44.2.1 的 AD1 几何（S/F-bound）是同一个公式，方向相反：
AD1 是「ret 刚好够、S 是瓶颈」，q_ebt 是「S 本身就不存在」。

### 48.3 结论：q 轴判死（本配方内），且不必等 AI 收批

`q_ebt` 不是随便挑的一条 q 腿：在严格三件套的 9 个 q 格中，EBITDA 是**体量最大、分析师覆盖最广、修正最连续**的指标，
它的 q 版若都只有 S 0.27，则 `q_eps` / `q_gps` / `q_sal` / `q_pre` 等**没有理由更好**。据此：

- **`est_q` 频域在本配方（`divide(Δmean, std)` → `group_zscore(subindustry)` → `signed_power` → `group_neutralize(market)`）下判死**。
  这不是「字段不好」，是**下一季度的共识修正几乎没有 EUR 横截面信息**：2021 一年贡献了几乎全部信号（1.52），其余九年平均 < 0.2。
  单年驱动的信号即便过闸也过不了稳健性闸（`Recent-3yr` 主判定与衰减比都会红）。
- **AI 批的 8 条 q 腿不作废，但改判用途**：它们从「补齐网格、寻找新候选」降级为「**跨指标确认 q 轴死亡**」。
  若 AI3–AI10 出现任一条 S ≥ 1.0，则说明 q 轴存在指标间异质性，需**单独立项**重新评估；否则 q 轴写入判死清单，不再投任何配额。
- **不牵连 12m 族**：AD1（S 1.71 / 2Y 2.41 / prod 0.497）与 AE2（S 2.15 / F 1.59 / 2Y 1.93 / prod 0.6236）都是 12m 口径，
  且 AF5 的失败发生在**构造层**（q 的 Δ 幅度太小），不在闸门层。**不要把「q 死」误读成「analyst7 死」**。
- **不牵连 `trade_when` 门控**：§47.4-A 的门控用法作用在「修正幅度」上，与频域选择正交。门控仍是对 12m 近失腿（`pre`/`ebi`/`eps`）的下一顺位杠杆。

### 48.4 可复用规则（写入方法论）

**当一条腿的 `ret` 反算出的 F 上限 < 0.3 时，该腿已在数学上判死**，不要再换算子、换窗、换幂次——
`F_ceiling = S × sqrt(max(TO, 0.125) / 0.125)`，而 `ret` 由信号本身决定。判据表（TO < 0.125 时）：

| 实测 ret | 要过 F 1.0 所需 S |
|---:|---:|
| 0.010 | **3.54** |
| 0.020 | **2.50** |
| 0.030 | **2.04** |
| 0.043 | **1.58**（与 LOW_SHARPE 同线，最优区间） |
| 0.050+ | ≤ 1.45 |

⇒ **先算这张表，再决定要不要派发**。本次 AF5 的 ret 0.0098 在派发前不可知，但**同族 12m 口径的 ret 是 0.045–0.069**
（AD1 .0449 / AE2 .0685 / AC6 .0612），q 口径直接掉到 0.0098 —— 这个 **4.4 倍的落差**本身说明
「q 修正幅度」在 EUR 是**噪声级**，与 §41 的「信号是纯日频现象」互为印证：低频、小幅、方向混杂的修正不产生可交易漂移。

### 48.5 本节新增 / 更正结论

| 位置 | 旧结论 | 更正 |
|---|---|---|
| §45.7 / §47.2 | q 频域 9 格是「未测的富矿」 | **✗**：最强格 `q_ebt` 实测 S 0.27 / 2Y 0.02，q 轴在本配方下判死；AI 的 8 条 q 腿降级为死亡确认 |
| §45.2 | `eps` 判「成因 B，若 d80 救活则推翻」 | **仍待 AJ 实测**；q 轴的失败不构成对 12m `eps` 的任何证据 |
| （未登记） | F 不过就换算子/换窗 | **✗**：TO < 0.125 时 `F = S × sqrt(ret/0.125)` 是恒等式。**ret 决定 F 上限**，先反算再派发（§48.4 表） |

---

## 49. Batch AJ 收割：**decay 80 不是族级常数**——对 `pre`/`eps` 继续抬 2Y，对 `ebi`/`sal`/`dps` 反向；AJ1 `pre` 首次把 2Y 推过线

**日期**：2026-10-20（凌晨）　**状态**：AJ 5/5 收完；AG / AH / AI / AK 在飞

### 49.1 实测（decay 80，其余与 AD 基准逐字相同）

| 腿 | 指标 | alpha id | S | F | 2Y | sub | ratio | ret | TO | DD | margin | L/S | pnl | failed_ra |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| **AJ1** | `pre` | `JjPvrgrj` | **2.00** | **1.42** | **1.59** ✅ | 0.96 | **0.480** ✗ | .0627 | .0468 | .0458 | 26.79 bp | 1454/1365 | 6 468 735 | 1（仅 sub） |
| AJ2 | `ebi` | `npA8rZrw` | 1.82 | 1.23 | 1.22 ✗ | 1.08 | 0.593 ✅ | .0575 | .0474 | .0393 | 24.24 bp | 1422/1397 | 5 932 225 | 1（2Y） |
| AJ3 | `eps` | `2rjNeaeZ` | 1.99 | 1.38 | 1.44 ✗ | 0.95 | 0.477 ✗ | .0602 | .0470 | .0334 | 25.60 bp | 1405/1414 | 6 208 916 | 2（sub+2Y） |
| AJ4 | `sal` | `qME6VPVP` | **2.01** | 1.39 | 1.10 ✗ | 1.03 | 0.512 ✗ | .0594 | .0462 | .0336 | 25.72 bp | 1403/1416 | 6 131 132 | 2（sub+2Y） |
| AJ5 | `dps` | `A1Q7EgEw` | 1.64 | **0.97** ✗ | 2.16 ✅ | 0.89 | 0.543 ✅ | .0434 | .0461 | .0426 | 18.86 bp | 1392/1427 | 4 483 516 | 1（F） |

⚠ 平台读数的一处不一致如实登记：AJ2 的 `LOW_2Y_SHARPE` 落在 `warning` 而 AJ3/AJ4 落在 `fail`，但 `ra_failed_checks` 三处都记了它。
**以数值为准**：2Y 1.22 / 1.44 / 1.10 均 < 1.58 ⇒ 都不算过。

### 49.2 decay 20 → 40 → 80 三档斜率（本族首次补齐 80 档）

| 指标 | S @d40 | S @d80 | ΔS(40→80) | 2Y @d40 | 2Y @d80 | **Δ2Y(40→80)** | 与 Δ2Y(20→40) 对照 | 形状 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `pre` | 1.92 | **2.00** | +0.08 | 1.39 | **1.59** | **+0.20** | +0.13（估算档） | **加速** |
| `eps` | 1.97 | 1.99 | +0.02 | 1.33 | 1.44 | **+0.11** | +0.11（AC7−AC2） | **线性保持** |
| `ebi` | 1.69 | 1.82 | +0.13 | 1.38 | 1.22 | **−0.16** | — | **反转** |
| `sal` | 1.93 | 2.01 | +0.08 | 1.26 | 1.10 | **−0.16** | — | **反转** |
| `dps` | 1.71 | 1.64 | −0.07 | 2.41 | 2.16 | **−0.25** | — | **反转** |

⇒ **§47.3 的「+0.13/20 units 全局线性外推」被证伪。** decay 对 2Y 的作用**按指标的修正持久性分化**：

- `pre`（税前利润）与 `eps` 的修正**方向噪声更大**（税项/一次性项目、股本口径），更长的 decay 把噪声平均掉 ⇒ 2Y 继续升；
- `ebi` / `sal` / `dps` 的修正**本身更连续、更持久**，d40 已接近最优平滑，d80 属于**过度平滑** ⇒ 2Y 反向下降；
- DPS 最典型：d40 的 2Y **2.41** 是本战役最高值，d80 把它削到 2.16，同时 S 与 F 双降（F 1.02 → 0.97 直接掉闸）
  ⇒ **`dps` 的最优 decay 就是 40，AD1 不动。**

**可复用规则**：decay 不是「越高越好」的族级旋钮，而是**与指标修正频率匹配的平滑常数**。后续按指标分档：
`pre`/`eps` → d80（甚至可试 d120）；`ebi`/`sal`/`dps` → d40；其余指标默认 d40，只在 d40 与 d80 各测一次后定档。

### 49.3 AJ1 `pre`：一个闸之差，且缺口的成因与修法已经定位

- **过闸状态**：`LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE` / `CLUSTER_TEST` / `CONCENTRATED_WEIGHT` / 换手双闸 **全 pass**；
  唯一 fail = `LOW_SUB_UNIVERSE_SHARPE` 0.96 vs **1.04**（= 0.51961 × S 2.00）。
- **缺口的真实成因**：`sub` 的**绝对值没变**。AD1（dps, d40）sub 也是 **0.95**，只是那时 S 1.71，比率 0.556 就过了。
  d80 把**全宇宙** S 从 1.71 抬到 2.00，而 sub 从 0.95 只到 0.96 ⇒ **新增的 S 几乎全部来自中小盘**。
  ⇒ 这不是「大盘信号退化」，是**decay 80 的增量偏小盘**。修法必须针对这一点，而不是笼统地"提 sub"。
- **过闸目标带**：只要 `S ≤ 0.96 / 0.51961 = 1.848` 且 sub 保持 0.96、2Y 保持 1.59，比率即过。
  即 **需要把 S 压回 1.60–1.84 区间而不伤 sub 与 2Y**——比"把 sub 从 0.96 抬到 1.04"容易得多。
- **历史杠杆的定量代价**：内层 `industry` 能抬比率 +0.08~+0.11（AC2/AB1/AC1/AC3 四点一致），
  但按 AC2−AD2 的 2Y 差（2.05 vs 2.34）它同时吃掉 **约 0.29 的 2Y** ⇒ 1.59 − 0.29 = **1.30，2Y 重新掉闸**。
  单纯抬 p 也不够：AD1→AD3 显示 p1.4→1.8 只抬比率 +0.018，却掉 0.16 S / 0.07 2Y。
  ⇒ **这两个旧杠杆都不满足「不伤 2Y」的条件，AJ1 的修复必须找新杠杆。**

### 49.4 候选修法与优先级（下一波的设计依据）

| 修法 | 机理 | 风险 | 优先级 |
|---|---|---|---|
| **门控 `trade_when(abs(ts_zscore(R4,66))>1.5, base, 0)`** | 只在修正幅度极端的日子持仓；大盘覆盖高、极端修正更可靠 ⇒ 有望同时抬 sub 与压 S | 可能把 S 也抬上去（比率不变）；TO 结构改变 | **P1**（论坛实证，见 §47.4-A；且是唯一未测过的用法） |
| `trade_when` 阈值 1.0 | 同上，更密 | 同上 | P2（同波做阈值校准） |
| 外层 `group_neutralize(..., sector)` | 去掉行业暴露，大盘组合更稳 | 增加行业赌注，prod 可能上升 | P2 |
| 内层 `industry` + 更高 p 组合 | 已知抬比率 | 已知吃 2Y ≥0.29 | P3（仅在门控失败后） |
| 信号额外 `ts_mean(..., 5)` | 降噪、压 S | 可能同时压 2Y | P3 |
| `group_rank` 替代 `group_zscore` | 去极值、压 S | 改变信号分布，需重新校准 p | P3 |

**明确不做的**：① 用 `market_capitalization_dlr2` 做 size 分桶（虽 EUR 覆盖 **99.98%**，但会把 PV 字段引入表达式，
可能改变 alpha 的 pyramid 归属，破坏「analyst 塔」身份）；② 换 universe（sub 检查的比率线随 universe 重算，不是杠杆）。

### 49.5 本节新增 / 更正结论

| 位置 | 旧结论 | 更正 |
|---|---|---|
| §47.3 | decay→2Y 是 +0.13/20 units 的族级线性斜率，d80 可外推 +0.23~0.26 | **✗ 实测证伪**。`pre` +0.20（加速）、`eps` +0.11（线性）、`ebi`/`sal` −0.16、`dps` −0.25（反转）。**decay 必须按指标定档** |
| §44.2 | d40 全面占优，后续所有腿默认 d40 | **✓ 对 `ebi`/`sal`/`dps` 成立；对 `pre`/`eps` 不成立**（d80 更优）。默认值改为「先 d40，`pre`/`eps` 用 d80」 |
| §45.2 | `eps` 判「成因 B，若 d80 救活则推翻」 | **半推翻**：2Y 1.33→1.44 确实在涨，但仍差 0.14；且 sub 比率 0.477 反而恶化 ⇒ eps 仍不可交付 |
| （未登记） | 高 S 是好事 | **✗ 在本族是双刃剑**：sub 是比率闸，S 抬得太高而 sub 不动 ⇒ 比率掉闸。AJ1 的 2.00 反而比 AD1 的 1.71 更难交付 |

---

## §50 AH / AI / AK 收割：p 轴定标，全过库存到 8 条

三批在同一夜连续收完（AH d40 8 腿、AI d40 10 腿、AK d40 10 腿）。核心结论两条：
**① ebt 广度形式是新的全过机制；② `signed_power` 的 p 指数是第二个可交付杠杆，但只对底行指标有效，对 eps / pre 无效。**

### 50.1 AH 收割（广度扩散 4 + 修订幅度 4，d40 / p1.4）

广度形式 `divide(subtract(X_raisednum_4wks, X_lowerednum_4wks), add(X_raisednum_4wks, X_lowerednum_4wks))`，
即「净上调家数 / 总变动家数」，值域 (−1, 1)，无单位、对极端修正不敏感。

| 腿 | 指标 / 形式 | alpha | S | F | 2Y | sub | ret | TO | DD | margin | pnl | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| AH1 | **ebt 广度** | `P0MOK7wx` | **2.13** | **1.38** | **1.65** | **1.36** | .0521 | .0511 | .0397 | 20.39 bp | 5,376,134 | **0 ✅** |
| AH2 | dps 广度 | `leM31jQn` | 1.58 | 0.84 | 0.69 | 0.78 | .0357 | .0539 | .0487 | 13.24 bp | 3,681,519 | 3 |
| AH3 | pre 广度 | `wp9EWj5p` | 1.98 | 1.24 | **0.84** | 1.24 | .0492 | .0526 | .0364 | 18.71 bp | 5,076,034 | 1（2Y） |
| AH4 | ebi 广度 | `akVEG7Nv` | 1.92 | 1.17 | 1.38 | 1.26 | .0462 | .0522 | .0365 | 17.71 bp | 4,772,401 | 1（2Y） |
| AH5 | fcf 修订 | `A1Q7ElnY` | 0.77 | 0.33 | 0.93 | 0.70 | .0225 | .0582 | .0463 | 7.73 bp | 2,321,156 | 3 |
| AH6 | ent 修订 | `d5KRvjnE` | 0.66 | 0.27 | 0.85 | 0.61 | .0205 | .0626 | .0514 | 6.55 bp | 2,114,288 | 3 |
| AH7 | cpx 修订 | `1Yjz0woz` | **−0.27** | −0.07 | −1.52 | 0.06 | −.0075 | .0526 | .1712 | −2.84 bp | −770,790 | 3 |
| AH8 | gps 修订 | `d5KRvjnK` | 1.54 | 0.92 | **1.68** | 1.01 | .0443 | .0529 | .0340 | 16.76 bp | 4,573,183 | 2（S 0.04 + F 0.08） |

**读数**：
- **AH1 是本项目第 3 个全过指标，且是第一个「广度」全过**。S 2.13 / F 1.38 / 2Y 1.65 / sub 1.36（比率 0.639，远高于 0.51961 线）。
  与 AE2（ebt 修订幅度 p1.4，S 2.15 / 2Y 1.93）**同指标不同机制**——广度把「修正多大」换成「修正家数占比」，
  理论上后者对大盘更稳（不依赖极端幅度）。两者互相关待测，若 < 0.7 可各占一席。
- **广度对 `pre` / `ebi` 是「高 S、低 2Y」形态**：AH3 S 1.98 但 2Y 0.84（比修订幅度的 p1.0 1.39 还低）、
  AH4 S 1.92 / 2Y 1.38（低于 p1.0 修订幅度的 1.65）。⇒ **广度不是 2Y 的解药，只是另一条腿**。
- **cpx 修订是唯一负向指标**（全部 10 年 S −0.27、2Y −1.52），说明 EUR 分析师对 capex 的上调在样本内是反向信号；
  但反向使用 S 只有 0.27，不够格，判死。
- fcf / ent 修订与 tbv / nav 修订同属「账面 / 现金流类慢变量」，在 EUR 全部无信号 ⇒ 该子族判死。

### 50.2 AI 收割（tbv / nav + q 八指标）——全灭

| 腿 | 指标 | alpha | S | F | 2Y | sub | 判读 |
|---|---|---|---:|---:|---:|---:|---|
| AI1 | tbv | `YPxgYM7J` | 0.40 | 0.13 | −0.39 | 0.23 | 死 |
| AI2 | nav | `3qjeJV9e` | 0.62 | 0.23 | 0.04 | 0.30 | 死（4 闸） |
| AI3 | q_ebi | `JjPvrQxW` | 0.49 | 0.19 | 0.92 | 0.78 | 死 |
| AI4 | q_eps | `bl8dAObl` | 0.56 | 0.22 | 1.43 | 0.60 | 死 |
| AI5 | q_gps | `vROvP2ra` | 0.17 | 0.04 | −0.01 | 0.46 | 死 |
| AI6 | q_ner | `QPY96KbQ` | 0.55 | 0.22 | 0.71 | 0.90 | 死 |
| AI7 | q_net | `KPmEZrNp` | 0.69 | 0.31 | 0.27 | 0.82 | 死 |
| AI8 | q_pre | `YPxgYMM6` | 0.53 | 0.21 | 0.30 | 0.63 | 死 |
| AI9 | q_prr | `2rjNemmZ` | 0.09 | 0.01 | −0.54 | 0.13 | 死 |
| AI10 | q_sal | `rKdP8ee9` | 0.57 | 0.22 | 0.30 | 0.71 | 死 |

**q 轴至此累计 18 腿全部 S < 0.7**（§48 的 8 腿 + 本批 8 腿 + q_ebt/q_eps 旧腿），
**q 轴彻底判死，后续任何波次不再包含 `est_q_*`**。tbv / nav 判死同上（慢变量修订在 EUR 无横截面信息）。

### 50.3 AK 收割（p1.0 / p1.2 × 五指标）——p 轴定标

| 腿 | 指标 | p | alpha | S | F | 2Y | sub | ret | margin | pnl | fail |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|---:|---|
| AK1 | dps | 1.0 | `JjPvrxll` | **1.78** | **1.02** | **2.32** | 1.00 | .0408 | 16.72 bp | 4,208,740 | **0 ✅** |
| AK2 | ebt | 1.0 | `pwvK3P0V` | **2.11** | **1.43** | **1.71** | 1.11 | .0577 | 22.98 bp | 5,955,573 | **0 ✅** |
| AK3 | pre | 1.0 | `bl8dARpq` | 1.96 | 1.27 | 1.39 | 0.88 | .0522 | 20.91 bp | 5,382,044 | 2 |
| AK4 | ebi | 1.0 | `qME6VWbj` | **1.76** | **1.07** | **1.65** | 1.01 | .0464 | 18.46 bp | 4,790,097 | **0 ✅** |
| AK5 | eps | 1.0 | `omogZ62E` | 1.95 | 1.23 | 1.18 | 0.96 | .0499 | 19.86 bp | 5,149,791 | 2 |
| AK6 | dps | 1.2 | `xA1d5YMW` | **1.76** | **1.03** | **2.39** | 0.98 | .0430 | 17.06 bp | 4,440,014 | **0 ✅** |
| AK7 | ebt | 1.2 | `E5Vexv39` | **2.15** | **1.53** | **1.83** | 1.13 | .0634 | 24.35 bp | 6,539,694 | **0 ✅** |
| AK8 | pre | 1.2 | `9qE7kVg1` | 1.96 | 1.31 | 1.39 | 0.91 | .0557 | 21.55 bp | 5,747,593 | 2 |
| AK9 | ebi | 1.2 | `3qjeJ9gg` | 1.74 | 1.10 | 1.54 | 1.08 | .0496 | 19.04 bp | 5,117,517 | 1（2Y 0.04） |
| AK10 | eps | 1.2 | `gJW9LQ7K` | 1.98 | 1.31 | 1.27 | 1.02 | .0544 | 20.89 bp | 5,612,868 | 2 |

**p 轴按指标定档（本轮新增的核心表）**：

| 指标 | p 对 S | p 对 2Y | 可交付档 | 说明 |
|---|---|---|---|---|
| **ebt** | 1.4: 2.15 → 1.2: 2.15 → 1.0: 2.11 | 1.93 → **1.83** → 1.71 | **p1.2（首选）/ p1.4** | p1.2 同时拿到最高 F 1.53；p1.0 反而全指标退 |
| **dps** | 1.4: 1.71 → 1.2: 1.76 → 1.0: 1.78 | 2.41 → 2.39 → 2.32 | **p1.2（均衡）/ p1.0** | 全档可交付，2Y 余量极大 |
| **ebi** | 1.4(d80): 1.82 → 1.2: 1.74 → 1.0: **1.76** | 1.22 → 1.54 → **1.65** | **p1.0**（p1.2 差 0.04） | 2Y 对 p 敏感，p1.0 是唯一过档 |
| **eps** | 1.4(d80): 1.99 → 1.2: 1.98 → 1.0: 1.95 | 1.44 → 1.27 → 1.18 | ✗ | **降 p 反而伤 2Y**，p 轴不是 eps 的解 |
| **pre** | 1.4(d80): 2.00 → 1.2: 1.96 → 1.0: 1.96 | 1.59 → 1.39 → 1.39 | ✗ | 2Y 与 sub 双缺口，p 轴无效 |

### 50.4 全过库存（8 条 / 3 指标族，互相关待测）

| # | 指标 | 形式 | p | alpha | S | F | 2Y | sub | margin | pnl |
|---|---|---|---|---:|---|---:|---:|---:|---:|---|---:|
| 1 | dps | 修订幅度 | 1.4 | `LL5dmv9a` | 1.71 | 1.02 | 2.41 | 0.95 | 17.21 bp | 4,634,507 |
| 2 | dps | 修订幅度 | 1.2 | `xA1d5YMW` | 1.76 | 1.03 | 2.39 | 0.98 | 17.06 bp | 4,440,014 |
| 3 | dps | 修订幅度 | 1.0 | `JjPvrxll` | 1.78 | 1.02 | 2.32 | 1.00 | 16.72 bp | 4,208,740 |
| 4 | ebt | 修订幅度 | 1.4 | `e76xGOQO` | 2.15 | 1.59 | 1.93 | 1.12 | 25.37 bp | 7,064,269 |
| 5 | ebt | 修订幅度 | 1.2 | `E5Vexv39` | 2.15 | 1.53 | 1.83 | 1.13 | 24.35 bp | 6,539,694 |
| 6 | ebt | 修订幅度 | 1.0 | `pwvK3P0V` | 2.11 | 1.43 | 1.71 | 1.11 | 22.98 bp | 5,955,573 |
| 7 | ebt | **广度** | 1.4 | `P0MOK7wx` | 2.13 | 1.38 | 1.65 | 1.36 | 20.39 bp | 5,376,134 |
| 8 | ebi | 修订幅度 | 1.0 | `qME6VWbj` | 1.76 | 1.07 | 1.65 | 1.01 | 18.46 bp | 4,790,097 |

**⚠ 交付口径问题（必须先于任何提交规划解决）**：
① **同指标不同 p 的三条互相关几乎必然 > 0.9**（同一字段、同一归一化、只差尾部压缩），self-corr 闸 < 0.7 会拦下其中两条；
⇒ 8 条里**真正可同时提交的独立席位 = 3~4 个**（dps / ebt / ebi / ebt 广度）。
② 距 10 条硬目标还差 **6~7 条独立机制**，必须从**新的信号形式**补，不能靠同族 p 变体凑数：
候选方向 = `gps` 修订（AH8，S/F 双差 0.04/0.08）、`prr` 修订（AG，S 1.37/F 0.80，2Y 1.79）、
`net` 修订（AG，2Y 1.57 差 0.01）、`sal` 修订（2.02 但 2Y 1.10）、以及**分散度 / 覆盖度形式**（尚未测）。
③ 塔归属核验：全部 8 条 pyramids 均为 `EUR/D1/ANALYST` multiplier 1.3 —— 与「已点亮塔不纳入」的入场约束一致性待与用户确认
（EUR/D1/ANALYST 当前持有 1 条、点亮需 3 条；本批交付会直接改变该塔状态）。

---

## 51. AN / AO 收割：第 9 条全过（gps）+ decay 80 的指标特异性

### 51.1 AN（decay 80 反向验证，4 腿）

| 腿 | 形式 | 指标 | p | alpha | S | F | 2Y | sub | ret | margin | fail |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|---|
| AN1 | 修订幅度 | prr | 1.4 | `O0Jxg67b` | 1.34 | 0.78 | 1.76 | 0.69 | .0424 | 17.92 bp | 3（S/F/sub） |
| AN2 | 修订幅度 | **gps** | 1.4 | `3qjeJGle` | **1.72** | **1.08** | **1.80** | **0.95** | .0497 | 21.32 bp | **0 ✅** |
| AN3 | 广度 | pre | 1.4 | `6XAeNGlK` | 2.01 | 1.29 | 0.94 | 1.20 | .0512 | 21.29 bp | 1（2Y） |
| AN4 | 广度 | ebi | 1.4 | `JjPvr37W` | 2.01 | 1.27 | 1.42 | 1.26 | .0499 | 20.94 bp | 1（2Y） |

**读数**：
- **AN2 是第 9 条全过，也是第 4 个指标族（gps）**。AH8 在 d40 时 S 1.54 / F 0.92 双差 0.04/0.08；**d80 把它推过线**
  （S +0.18、F +0.16），2Y 也从 1.68 → 1.80。⇒ **decay 不是「一律伤 2Y」**：对 gps 这类平滑型修订，d80 是补差的正解。
- AN1 prr 在 d80 全面恶化（S 1.34、2Y 1.76 但 S/F/sub 三闸），**prr 与 gps 的 decay 响应方向相反**，
  说明两指标的信号自相关结构不同（prr 是价格类、gps 是毛利类），这也支持它们算不同机制。
- AN3 pre 广度 d80：2Y 从（AH3 d40 的）0.84 → 0.94，仍死。**pre 广度判死**（形态上 S 2.0 但近两年失效）。
- AN4 ebi 广度 d80：S 2.01 / sub 1.26（比率 0.627），**只差 2Y 0.16**；而 d40 未测过该形式。
  ⇒ 已排入下一波（d40 重测），这是 ebi 的第二条腿候选。

### 51.2 AO（net / sal 修订，d40，4 腿）——双双判死

| 腿 | 指标 | p | alpha | S | F | 2Y | sub | fail |
|---|---|---:|---|---:|---:|---:|---:|---|
| AO1 | net | 1.0 | `JjPvr3dl` | 1.65 | 0.97 | 1.27 | 0.71 | 3（F/sub/2Y） |
| AO2 | net | 0.8 | `npA8r6W3` | 1.60 | 0.89 | 1.13 | 0.69 | 3 |
| AO3 | sal | 1.0 | `mLYVQKX6` | 1.95 | 1.21 | 1.00 | 0.95 | 2（sub/2Y） |
| AO4 | sal | 0.8 | `LL5d38Rm` | 1.91 | 1.13 | 0.88 | 0.91 | 2（sub/2Y） |

**读数**：
- **net 修订判死**：p1.0 已是最好档，再降 p 全指标同向恶化（S −0.05 / F −0.08 / 2Y −0.14）⇒ 无杠杆可用。
  且 sub 0.71 距比率线（0.51961×S=0.86）差 0.15，2Y 差 0.31，**是结构性弱，不是贴线**。
- **sal 修订是「高 S、低 2Y」的典型**：S 1.91~1.95、F 1.13~1.21、margin 18.6~19.8 bp 都好看，
  但 2Y 只有 0.88~1.00 ⇒ 信号集中在早年（2014–2019），近三年已衰减。降 p 反而更差 ⇒ **判死**，
  不做「换 decay 抢救」（同族 AN1/6 已显示该指标族的 decay 响应不利）。
- 至此**修订幅度形式已把所有 22 个指标测完**（dps/ebt/ebi/gps 全过；cpx/fcf/ent/tbv/nav 无信号；
  eps/pre/sal/net/prr/roe/ndt/cps/roa/grm/csh 各有硬缺口）。剩余未测指标只有 bps/cps/csh/grm/opr 的**部分 p 档**
  与 `ebg/ebs/ner` 三个从未进过波的指标 —— 已排入 AQ。

### 51.3 全过库存（9 条 / 4 指标族）

| # | 指标 | 形式 | p | decay | alpha | S | F | 2Y | sub | margin | pnl |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---:|
| 1 | dps | 修订幅度 | 1.4 | 40 | `LL5dmv9a` | 1.71 | 1.02 | 2.41 | 0.95 | 17.21 bp | 4,634,507 |
| 2 | dps | 修订幅度 | 1.2 | 40 | `xA1d5YMW` | 1.76 | 1.03 | 2.39 | 0.98 | 17.06 bp | 4,440,014 |
| 3 | dps | 修订幅度 | 1.0 | 40 | `JjPvrxll` | 1.78 | 1.02 | 2.32 | 1.00 | 16.72 bp | 4,208,740 |
| 4 | ebt | 修订幅度 | 1.4 | 40 | `e76xGOQO` | 2.15 | 1.59 | 1.93 | 1.12 | 25.37 bp | 7,064,269 |
| 5 | ebt | 修订幅度 | 1.2 | 40 | `E5Vexv39` | 2.15 | 1.53 | 1.83 | 1.13 | 24.35 bp | 6,539,694 |
| 6 | ebt | 修订幅度 | 1.0 | 40 | `pwvK3P0V` | 2.11 | 1.43 | 1.71 | 1.11 | 22.98 bp | 5,955,573 |
| 7 | ebt | 广度 | 1.4 | 40 | `P0MOK7wx` | 2.13 | 1.38 | 1.65 | 1.36 | 20.39 bp | 5,376,134 |
| 8 | ebi | 修订幅度 | 1.0 | 40 | `qME6VWbj` | 1.76 | 1.07 | 1.65 | 1.01 | 18.46 bp | 4,790,097 |
| 9 | **gps** | 修订幅度 | 1.4 | **80** | `3qjeJGle` | 1.72 | 1.08 | 1.80 | 0.95 | 21.32 bp | 5,125,234 |

### 51.4 本轮新增的可复用结论

1. **decay 是「指标 × 形式」特异参数，不能区域统一**：gps 修订 d40→d80 得 S+0.18/F+0.16/2Y+0.12（补差正解）；
   ebt 广度 d40→d80 得 2Y −0.23（反向）；pre 广度同向恶化。⇒ 新指标进波时**必须做 d40/d80 双向探针**，
   不能沿用区域缺省 decay 40 或简单「加倍」。
2. **2Y 衰减是 sal/net 类「现金流慢变量」的共同形态**（S 高、近三年失效），与 fcf/ent/tbv 的「全周期无信号」是两种不同的死法；
   判死记录要区分（前者未来若出现 regime 变化可重测，后者不必）。
3. **sub 比率线的判读**：€sub = 0.51961 × S。sal p1.0 的 sub 0.95 对应线 1.01 ⇒ 实际是「贴着比率线差 0.06」，
   而 net p1.0 的 0.71 vs 0.86 是「结构性差 0.15」。同样写「2 闸不过」，处置优先级完全不同。

### 51.5 在飞与排队（截至 2026-10-20T00:13Z）

| 批 | 内容 | multisim id | 状态 |
|---|---|---|---|
| AL | AJ1 pre 宽度修复（8 腿） | `1fco8hdRP4CEaQt13J36BkIa` | 排队（child_count 0） |
| AM | prr / gps p 轴 d40（4 腿） | `1myXp0fy34l2ahWWSXTibiZ` | 排队 |
| **AP** | **ebt 形式多样化 10 腿**（周/月广度、离散度修订、区间宽度、中位/上/下界修订、覆盖变化、28d 平滑、3 月修订） | `4qAtmDaFm4wZcivoGCL5Bh8` | 排队 |
| **AQ** | **未测指标 bps/cps/csh/grm/opr × p1.4/1.2（10 腿）** | `1wmTJc8pS4RS8Mp17zpGPVIR` | 排队 |

平台一次只展开一个 multisim（其余 `child_count: 0` 是排队，不是故障）。
下一波（AR）候选：ebi 广度 d40 重测（AN4 只差 2Y 0.16）+ `ebg/ebs/ner` 三指标首测 + AP 里最好读数的 d40 复验。

---

## 52. 交付口径审计：互相关矩阵 / ATOM 合规 / 塔归属（2026-10-20）

### 52.1 9×9 互相关（本地计算，4y 日收益，threshold 0.7，1021 点）

行/列顺序：dps 1.4 / 1.2 / 1.0 → ebt 幅度 1.4 / 1.2 / 1.0 → ebt 广度 → ebi 1.0 → gps 1.4(d80)。

| | LL5dmv9a | xA1d5YMW | JjPvrxll | e76xGOQO | E5Vexv39 | pwvK3P0V | P0MOK7wx | qME6VWbj | 3qjeJGle |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **LL5dmv9a** | 1 | .9925 | .9704 | .3347 | .3531 | .3676 | .3835 | .3835 | .3735 |
| **xA1d5YMW** | .9925 | 1 | .9925 | .3612 | .3819 | .3982 | .4160 | .4121 | .4030 |
| **JjPvrxll** | .9704 | .9925 | 1 | .3845 | .4072 | .4253 | .4453 | .4357 | .4270 |
| **e76xGOQO** | .3347 | .3612 | .3845 | 1 | **.9933** | .9728 | .6216 | .6957 | .5284 |
| **E5Vexv39** | .3531 | .3819 | .4072 | .9933 | 1 | .9929 | .6556 | .7221 | .5483 |
| **pwvK3P0V** | .3676 | .3982 | .4253 | .9728 | .9929 | 1 | .6815 | .7383 | .5607 |
| **P0MOK7wx** | .3835 | .4160 | .4453 | .6216 | .6556 | .6815 | 1 | .6186 | .4984 |
| **qME6VWbj** | .3835 | .4121 | .4357 | .6957 | .7221 | .7383 | .6186 | 1 | .6267 |
| **3qjeJGle** | .3735 | .4030 | .4270 | .5284 | .5483 | .5607 | .4984 | .6267 | 1 |

**读数**：

1. **同指标 p 变体不可同交**：dps 三档 0.9704–0.9925；ebt 三档 0.9728–0.9933（组内最高对 `e76xGOQO`–`E5Vexv39` = 0.9933）。
   p 只是尾部压缩强度，改不动持仓结构 ⇒ 三档只能出 1 颗。
2. **ebt 广度 vs 幅度 = 0.6216–0.6815** ⇒ 真正独立的第二条腿，`P0MOK7wx` 必须保留。
3. **ebi vs ebt 是「边际」不是「独立」**：p1.4 0.6957（贴线内）、p1.2 0.7221、p1.0 0.7383。
   ⇒ ebi 只能与 **ebt p1.4** 同池；与 ebt p1.2/p1.0 同池会超 0.7。
4. **gps 是全组最独立的一条**（与其余 0.37–0.63），d80 修复后独立席位成立。
5. **精确最大团 = 5**：
   `{LL5dmv9a, e76xGOQO, P0MOK7wx, qME6VWbj, 3qjeJGle}`（`max_subset_exact: true`、`missing_pnl: []`）。
   ⇒ **9 条全过指标 → 最多 5 个可同时提交的独立席位**。

### 52.2 交付差额（两种口径分开报，别混）

| 口径 | 现状 | 目标 | 差额 |
|---|---:|---:|---:|
| 全闸通过（平台 checks 无 fail） | **9** | 10 | **1** |
| 可同时提交（两两 prod/self < 0.7） | **5** | 10 | **5** |

- 「通过验证」还差 1 条：AP / AR / AL 任一新形式腿过闸即可补齐。
- 「独立席位」还差 5 条：**p 变体无效**，只能靠**新信号形式**（广度 / 离散度 / 覆盖度 / 比值型）或新指标。
  这条与 §50.4 的裁决一致，本节用全矩阵把「3~4 个」修正为**精确 5 个**。

### 52.3 ATOM 合规核验（交付前逐条过）

| 项 | 要求 | 本批实测 |
|---|---|---|
| 字段同数据集 | 所有数据字段同一 **dataset id** | 全部腿只用 `est_12m_*` ⇒ **analyst7**（1111 字段） |
| 分组字段豁免 | 恰好 6 个：country/exchange/market/sector/industry/subindustry | 仅用 `subindustry` + `market`，均在白名单 |
| 禁用算子 | `inst_pnl()` / `convert()` 计为 pv1 | **零使用** |
| pv1 第二参数 | `vector_neut(x, size)` 等破坏 ATOM | **零使用**（双腿只出现在 `group_zscore` / `group_neutralize` 的组参数位） |
| 2Y 线 | 平台按区域回报的 `LOW_2Y_SHARPE.limit` | **1.58**（EUR 实测，覆盖文档 D1 2.38/2.023） |
| 检测差异 | ATOM 免 IS Ladder，改 Last 2Y | 9 条全过的 2Y ∈ [1.65, 2.41]，全 > 1.58 |

### 52.4 塔归属核验（「已点亮塔不纳入」）

- `get_pyramid_alphas` EUR/D1：model 2 / fundamental 1 / **analyst 1** / other 1 / risk 1；analyst 点亮需 3 ⇒ **未点亮**。
- EUR 全部 ACTIVE OS 中属 analyst 类的只有 `786pLKnb`：
  `signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var, 55)), industry), 3.0)`
  —— 用的是**另一套分析师字段**（`eps_revision_magnitude` / `eps_y1_estimate_coeff_var`），**不是 analyst7 的 `est_12m_*`**。
- ⇒ **analyst7 在 OS 侧零占用**，「已点亮塔不纳入」约束满足；本批 9 条全过的 `pyramids` 均为
  `EUR/D1/ANALYST` × 1.3，提交后会推动该塔 1 → 3（点亮）。
- 若按「数据集」口径读约束：analyst7 未被任何已提交 alpha 使用；若按「塔」口径读：该塔只持有 1 条且非 analyst7 ⇒ 两种读法都通过。

### 52.5 在飞队列（2026-10-20T00:17Z）

| 批 | 内容 | multisim id | 状态 |
|---|---|---|---|
| AL | AJ1 pre 宽度修复（8 腿） | `1fco8hdRP4CEaQt13J36BkIa` | 排队 |
| AP | ebt 形式多样化（10 腿） | `4qAtmDaFm4wZcivoGCL5Bh8` | 排队 |
| **AR** | **广度/比值型新形式（10 腿）**：prr·ebi·dps 广度 + ebs 相对修订 + ner + gps 广度 | `1JrISZbz55cnbkFI6C5ntup` | **已完成（见 §54）** |
| AQ | 未测指标 bps/cps/csh/grm/opr × p1.4/1.2 | `1wmTJc8pS4RS8Mp17zpGPVIR` | **已完成（见 §53）** |
| **AS** | **cps 2Y 修复（decay 80，2 腿）**：修订幅度 p1.4 + 方向性广度 p1.4 | `6C6Io7554Fs8L05ANP4Q67` | 排队 |
| **AT** | **广度 2Y 修复（d40，8 腿）**：ebi 平滑 5/10·p1.0·1mth·ts_zscore + gps 平滑 5/1mth + prr 平滑 5 | `2ZGGCp1hX4DbaGl3I3xJUl2` | 排队 |

---

## 53. AQ 收割：五个未测指标 × p 双档（d40，10 腿）——cps 是唯一近失

### 53.1 读数表

| 腿 | 指标 | p | alpha | S | F | 2Y | sub | ret | margin | TO | fail |
|---|---|---:|---|---:|---:|---:|---:|---:|---|---:|---:|
| AQ1 | bps | 1.4 | `vROv6Eod` | 1.12 | 0.56 | 1.30 | 0.57 | .0310 | 11.7 bp | .0528 | 4 |
| AQ2 | bps | 1.2 | `XgR8MZlX` | 1.14 | 0.55 | 1.31 | 0.55 | .0290 | 11.4 bp | .0510 | 4 |
| AQ3 | cps | 1.4 | `vROvGlaa` | **1.52** | **0.90** | 1.34 | **1.12** | .0435 | 16.1 bp | .0541 | 3（全 WARNING） |
| AQ4 | cps | 1.2 | `zqrRe7oR` | 1.50 | 0.85 | 1.30 | 1.11 | .0402 | 15.2 bp | .0528 | 3 |
| AQ5 | csh | 1.4 | `3qjeJebX` | 0.78 | 0.34 | −0.23 | 0.72 | .0244 | 8.5 bp | .0577 | 3 |
| AQ6 | csh | 1.2 | `9qE7k56d` | 0.84 | 0.38 | −0.12 | 0.78 | .0250 | 8.8 bp | .0566 | 3 |
| AQ7 | grm | 1.4 | `9qE7k7vr` | 0.38 | 0.11 | 1.06 | 0.29 | .0112 | 4.1 bp | .0554 | 3 |
| AQ8 | grm | 1.2 | `KPmEZA81` | 0.40 | 0.12 | 1.03 | 0.34 | .0111 | 4.1 bp | .0539 | 3 |
| AQ9 | opr | 1.4 | `vROv67GA` | 0.15 | 0.03 | 0.76 | 0.13 | .0053 | 1.6 bp | .0655 | 3 |
| AQ10 | opr | 1.2 | `e76xEMqp` | 0.18 | 0.04 | 0.77 | 0.14 | .0059 | 1.8 bp | .0645 | 3 |

### 53.2 归因

1. **cps（每股现金流）是唯一有救的指标**：S 1.52（差 0.06）、F 0.90（差 0.10）、2Y 1.34（差 0.24）、sub 1.12 远超比率线（0.51961 × 1.52 = 0.79）。
   ⇒ 属「结构没找对」带（S ≥ 1.0 且 returns 4.35% > 3.5%），**不判死**；2Y 缺口 0.24 是主矛盾，首选 **d80 复验**（gps 在同族上 d80 曾把 2Y 从 1.68 抬到 1.80）。
2. **bps 全灭**（S 1.12/1.14、F 0.55）——同属「每股」维度但账面价值修订无横截面信息；与 tbv/nav 判死同一死因（慢变量）。**bps 判死**。
3. **csh（每股现金）2Y 为负**（−0.23/−0.12）且 S < 0.9 —— 经典「全期有信号、近两年反向」死法，与 fcf/ent/tbv 的「全期无信号」是不同死法。**判死**。
4. **grm（毛利率）/ opr（营业利润率）双双 S < 0.4、returns < 1.2%** —— F 闸数学封顶（`S ≥ sqrt(0.125/returns)` ≈ 3.3），无提升空间。**判死**。
5. **p 轴在这五个指标上无一提分**：cps 1.4 > 1.2、bps 1.2 略优但全无意义、其余 1.4 与 1.2 几乎同值 ⇒ 与 §50.3 的「p 轴按指标定档」一致，**p 不是这批的钥匙**。

### 53.3 落地

- AQ 全部 10 行已入库（`eur_a7_aq`，`upsert_backtest_rows` 返回 `{"n":10}`）。
- **判死 4 个指标**：bps / csh / grm / opr（修订幅度形式）。analyst7 剩余可探索面收缩到 **cps 一条 + 广度/比值/离散度等新形式**。
- **AS 已派发**：`6C6Io7554Fs8L05ANP4Q67`（decay 80，2 腿）：
  ① cps 修订幅度 p1.4（2Y 修复主探针，复刻 gps 的 d80 路径）；
  ② cps 方向性广度 p1.4（`divide(subtract(raisednum_4wks, lowerednum_4wks), add(raisednum_4wks, lowerednum_4wks))`，AH 广度公式迁移）。
  两腿都只用 analyst7 字段 ⇒ ATOM 合规；广度腿与幅度腿的互相关待 AS 完成后本地计算。

---

## 54. AR 收割：广度 / 比值新形式（d40，10 腿）——ebi 广度只差 2Y 0.19

### 54.1 读数表

| 腿 | 形式 | 指标 | p | alpha | S | F | 2Y | sub | ret | margin | fail |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|---:|
| AR1 | 方向性广度 | prr | 1.4 | `A1Q7Ep8e` | 1.57 | 0.86 | 1.27 | 0.93 | .0377 | 13.5 bp | 3（全 WARNING） |
| AR2 | 方向性广度 | prr | 1.2 | `LL5d3vY2` | 1.62 | 0.90 | 1.31 | 0.96 | .0386 | 14.0 bp | 2（全 WARNING） |
| AR3 | 方向性广度 | **ebi** | 1.4 | `akVEG7Nv` | **1.92** | **1.17** | 1.38 | 1.26 | .0462 | 17.7 bp | **1（仅 2Y）** |
| AR4 | 方向性广度 | **ebi** | 1.2 | `1Yjz08AM` | **1.94** | **1.18** | **1.39** | 1.25 | .0465 | 18.0 bp | **1（仅 2Y）** |
| AR5 | 方向性广度 | dps | 1.4 | `leM31jQn` | 1.58 | 0.84 | 0.69 | 0.78 | .0357 | 13.2 bp | 3 |
| AR6 | 方向性广度 | dps | 1.2 | `d5KRvMJX` | 1.62 | 0.87 | 0.71 | 0.82 | .0361 | 13.5 bp | 3 |
| AR7 | 相对修订比 | ebs | 1.4 | `ZYmKN8Vx` | 0.43 | 0.14 | 0.21 | 0.42 | .0129 | 5.8 bp | 3 |
| AR8 | 修订幅度 | ner | 1.2 | `WjLVJZrG` | 1.30 | 0.70 | 1.04 | 0.64 | .0366 | 14.3 bp | 4 |
| AR9 | 修订幅度 | ner | 1.4 | `58jkYnOo` | 1.24 | 0.68 | 0.95 | 0.61 | .0379 | 14.4 bp | 4 |
| AR10 | 方向性广度 | gps | 1.4 | `pwvK32bx` | **1.71** | **0.97** | 1.23 | 1.28 | .0403 | 15.3 bp | **2（F + 2Y）** |

### 54.2 归因（这是本轮最重要的一节）

1. **ebi 广度是本战役最强近失**：S 1.94（全组最高）、F 1.18、sub 1.25，**唯一缺口 = 2Y 1.39 vs 1.58（差 0.19）**。
   与 AQ3 cps（差 S/F/2Y 三项）不同，ebi 广度是「只差一条腿」的形态。
   ⇒ **2Y 是唯一矛盾**，所有后续动作只服务这一个数字。
2. **p 轴彻底用尽**：p1.4 → p1.2 只换来 S +0.02 / F +0.01 / 2Y +0.01。**p1.2 已是上限，不再扫 p**。
3. **广度形式的系统性代价 = 2Y**：同指标对照
   | 指标 | 幅度 2Y | 广度 2Y | 差 |
   |---|---:|---:|---:|
   | ebt | 1.93（AK4/p1.4） | 1.65（AH1） | −0.28 |
   | ebi | 1.65（AK4/p1.0） | 1.39（AR4） | −0.26 |

   广度用「多少家在上调」替代「上调多少」，全期 S 更高（1.94 vs 1.76）但近两年更弱。
   ⇒ **2Y 修复不能靠 p，只能靠时间维度**：decay / 平滑 / 长窗 / 时序标准化。
4. **gps 广度是第二候选**：S 1.71 已过、F 0.97 只差 0.03、sub 1.28 极强；2Y 1.23 差 0.35。
   与 gps 幅度 d80（`3qjeJGle`）机制同族，互相关待测——若 < 0.7 可各占一席。
5. **dps 广度判死**：S 过线但 2Y 0.69–0.71、sub 0.78–0.82 双缺口，且 p 越小越好幅度有限。
6. **ebs 相对修订比判死**：S 0.43。`est_12m_ebs_mean` 可能接近零，比值形式分母不稳定（对照 ebi/ebt 用 `_std` 归一成功、用 `_mean_4wks_ago` 失败）。
7. **ner 判死**：S 1.24–1.30、sub 0.61–0.64，p1.2 全面优于 p1.4 但两档都够不着。
8. **广度 vs 幅度的批内互相关预测**：ebt 上 0.6216–0.6815 ⇒ ebi 广度 vs ebi 幅度大概率 0.6 左右。
   若成立，**ebi 广度的 2Y 一旦修好就是第 6 个独立席位**，且是全组 S 最高的一条。

### 54.3 AT 派发：ebi/gps/prr 广度的 2Y 修复（d40，8 腿）

`2ZGGCp1hX4DbaGl3I3xJUl2`

| 腿 | 内容 | 检验的杠杆 |
|---|---|---|
| AT1 | ebi 广度 p1.2 + `ts_mean(..., 5)` | 轻度时间平滑 |
| AT2 | ebi 广度 p1.2 + `ts_mean(..., 10)` | 中度时间平滑 |
| AT3 | ebi 广度 p1.0 | p 轴确认（p1.2 是否真上限） |
| AT4 | ebi 广度 1mth 窗 p1.2 | 拉长修订计数窗口 |
| AT5 | ebi 广度 p1.2 + `ts_zscore(..., 252)` | 时序标准化（AF 批修 2022 的同款杠杆） |
| AT6 | gps 广度 p1.4 + `ts_mean(..., 5)` | gps 的 2Y/F 修复 |
| AT7 | gps 广度 1mth 窗 p1.4 | gps 长窗 |
| AT8 | prr 广度 p1.2 + `ts_mean(..., 5)` | prr 的 2Y 修复（备选） |

设计纪律：全部保持 **同一指标内** 变换（不跨指标混合），ATOM 合规（字段仍是 analyst7 `est_12m_*` + 两个豁免组字段）。
一次只动一个时间维度杠杆，读数后按「谁抬 2Y 最多」再加 decay 80 复验。

---

## 55. AL / AP / AU 收割与最终交付（2026-10-20）

本节是本次战役的收口：三批收割 → 库存盘点 → 互相关 → 10 颗交付清单 → ATOM 合规核验 → 字段画像索引。
所有批次共用的规范设置（除特别标注）：EUR / TOP2500 / D1 / FAST / trunc 0.08 / EQUITY / FASTEXPR /
2014-01-01→2023-12-31 / FULL / pasteurization ON / unitHandling VERIFY / **nanHandling ON / maxTrade ON**。

### 55.1 AL：AJ1 pre 修复（decay 80，8 腿）——ts_zscore 门控解开 sub 卡点

批次 `1fco8hdRP4CEaQt13J36BkIa`。核心字段 `est_12m_pre_mean` / `est_12m_pre_mean_4wks_ago` / `est_12m_pre_std`。

| 腿 | 形式 | p | alpha | S | F | 2Y | sub | fail |
|---|---|---:|---|---:|---:|---:|---:|---|
| AL1 | `pre_num_28d > 2` 计数门控 | 1.4 | `E5Ve21eG` | 1.20 | 0.64 | 0.66 | 0.69 | S/F/2Y |
| AL2 | `pre_num_28d > 4` 计数门控 | 1.4 | `9qE72Y7x` | 0.99 | 0.49 | 0.51 | 0.55 | S/F/2Y |
| AL3 | `abs(ts_zscore(SIG,66)) > 1.5` | 1.4 | `gJW90690` | 1.73 | 1.07 | 1.20 | 1.06 | **2Y（−0.38）** |
| AL4 | `abs(ts_zscore(SIG,66)) > 1.0` | 1.4 | **`6XAe27eL`** | **1.74** | **1.10** | **1.62** | **0.96** | **全过** |
| AL5 | `group_zscore(·, industry)` | 1.4 | `58jk2xkX` | **2.18** | **1.80** | 1.39 | 1.20 | 2Y（−0.19） |
| AL6 | 外层 `group_neutralize(·, sector)` | 1.4 | `e76xWm3l` | 1.99 | 1.40 | 1.59 | 0.95 | sub（线 1.03，−0.08） |
| AL7 | `group_rank(·) − 0.5` 去市场 | 1.4 | `N1eR20bw` | 0.89 | 0.36 | −0.15 | 0.57 | S/F/2Y |
| AL8 | p1.6 | 1.6 | `Grge7PG0` | 1.94 | 1.40 | 1.60 | 0.97 | sub（线 1.01，−0.04） |

**归因**

1. **门控类型决定 2Y**：计数门控（"有几家改"）把 2Y 压到 0.51–0.66；时序标准化门控（"这次改得有多异常"）
   1.5 → 1.20、1.0 → 1.62。近两年低波动环境下，绝对计数天然萎缩，`ts_zscore` 对制度变化免疫。
2. **门控放宽只补样本量，不改信号强度**：1.5 → 1.0 时 S/F 几乎不动（1.73/1.07 → 1.74/1.10），2Y 抬 0.42。
   ⇒ 2Y 的缺口是「近年样本太少」，不是「信号变弱」。这条解释了 AR 批里广度形式普遍 2Y 弱的同源机制。
3. **分组越粗，近期越弱**：industry 分组给全族最高 S/F（2.18/1.80），但 2Y 只 1.39；sector 外层进一步把 sub 打到 0.95。
   ⇒ **分组维度（subindustry 之外）全部封闭**，不再尝试 industry/sector/country。
4. **p 轴封闭**：p1.6 把 sub 压到 0.97，同时比率闸的 sub 线抬到 1.01 ⇒ 越往上越难。p1.4 是甜点。
5. pre 族唯一可提交形态 = `ts_zscore > 1.0` + p1.4 + d80。其余 7 腿判死。

### 55.2 AP：ebt 形态穷举（decay 40，p1.2，10 腿）——三颗新全通过

批次 `4qAtmDaFm4wZcivoGCL5Bh8`。统一 `group_neutralize(signed_power(group_zscore(·, subindustry), 1.2), market)`。

| 腿 | 形式 | alpha | S | F | 2Y | sub | fail |
|---|---|---|---:|---:|---:|---:|---|
| AP1 | 1 周广度 `(raised_1wk−lowered_1wk)/(raised_1wk+lowered_1wk)` | **`MP0L2Ogo`** | **2.03** | **1.24** | **1.76** | **1.20** | **全过** |
| AP2 | 1 月广度计数 `raisednum_1mth` | `XgR8OGNX` | 2.07 | 1.31 | 1.54 | 1.30 | 2Y（−0.04） |
| AP3 | 离散度变化 `(_std − _std_4wks_ago)/_std_4wks_ago` | `wp9EvqN1` | 0.11 | 0.02 | −0.97 | 0.15 | S/F/2Y |
| AP4 | 区间/均值 `(high−low)/mean` | `akVEg6RO` | −0.32 | −0.08 | 1.08 | −0.24 | 4 |
| AP5 | median 修订 `(median−median_4wks)/std` | **`A1Q729Ll`** | **2.23** | **1.60** | **1.82** | **1.27** | **全过** |
| AP6 | high 修订 `(high−high_4wks)/std` | **`O0Jx2O6R`** | **1.94** | **1.26** | **1.86** | **1.05** | **全过** |
| AP7 | low 修订 `(low−low_4wks)/std` | `3qje2wGO` | 1.81 | 1.13 | 1.85 | 0.76 | sub（−0.18） |
| AP8 | 分析师家数变化 `(_num−_num_4wks)/_num_4wks` | `e76xWmNp` | 0.09 | 0.01 | −0.81 | −0.08 | 4 |
| AP9 | `mean_28d` 修订 | `kqJZYdvk` | 2.27 | 1.61 | 1.61 | 1.13 | sub（线 1.18，−0.05） |
| AP10 | 3 个月修订 `(mean−mean_3mth_ago)/std` | `mLYVlpd5` | 1.85 | 1.27 | 1.25 | 0.89 | sub + 2Y |

**归因**

1. **共识统计量的"位置"有信息，"波动/计数"没有**：median / high 修订（2.23 / 1.94）vs 家数变化（0.09）、
   离散度变化（0.11）。后两者是二阶矩与计数，横截面无稳定方向 ⇒ **std / num 两类形态判死，不再投入**。
2. **1 周广度是 AP 最有价值的新形态**：全过且换手 7.32%（4 周广度 5.61%），短窗事件提供更快信号，代价是换手。
3. **上下侧不对称**：high 修订 sub 1.05 过线，low 修订 0.76（差 0.18）。下修企业在子宇宙里更集中 ⇒
   **只做上侧/中位，不做下侧**。
4. **mean_28d 是最强近失**（S 2.27 / F 1.61，仅 sub 差 0.05）：它是 mean↔median 的插值，若后续要补一颗，
   优先给它做 p1.4 复验（注意 p 抬高会同时抬高 sub 线）。
5. **3 个月窗口双重失败**（sub + 2Y）⇒ 修订信号的记忆长度以 **4 周为甜点**，拉长会混入已定价信息。

### 55.3 AU：cps 广度 d80 + 平滑（2 腿）——新 metric 族全通过

批次 `3RoRdO5AF5cL8ZYtW21zlyJ`。字段 `est_12m_cps_raisednum_4wks` / `est_12m_cps_lowerednum_4wks`。

| 腿 | 形式 | p | alpha | S | F | 2Y | sub | TVR | ret | fail |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| AU1 | cps 4 周广度（plain） | 1.4 | `e76xWop6` | 1.76 | 0.98 | 1.94 | 1.28 | 4.59% | .0387 | F（−0.02） |
| AU2 | cps 4 周广度 + `ts_mean(·,5)` | 1.4 | **`wp9EvMmv`** | **1.80** | **1.01** | **2.00** | **1.27** | 4.31% | .0396 | **全过** |

**杠杆分解（这是本轮最有复用价值的一条）**

| 配置 | S | F | 2Y | TVR |
|---|---:|---:|---:|---:|
| d40，无平滑（AQ 批） | 1.52 | 0.90 | 1.34 | — |
| d80，无平滑（AU1） | 1.76 | 0.98 | 1.94 | 4.59% |
| d80 + ts_mean5（AU2） | **1.80** | **1.01** | **2.00** | 4.31% |

- **decay 40→80 是 2Y 的主导杠杆**（+0.60），且同时抬 S +0.24 / F +0.08；代价是换手略升。
- **ts_mean5 是"临门一脚"**：F +0.03 越过 1.00、2Y +0.06，换手反而降 0.28 pt。
- 三角验证：AS 批在 **OFF/OFF** 设置下跑过同一 cps 广度（`npA8XxeM`）得 1.73/0.94/**2.01** —— 2Y 与 ON/ON 的 2.00 一致，
  证明 **2Y 的抬升来自 decay，不是设置**；F 的 0.07 差正是 nanHandling/maxTrade 的影响。
- ⇒ 该配方（**d80 + 轻度平滑**）是广度类 2Y 修复的已验证杠杆，已定向迁移到 ebi/gps/prr 广度（AV 批，见 §55.10）。

### 55.4 设置事故留痕：AS / AT 的 camelCase 键被静默丢弃

- AS（`leM3Np5e` / `npA8XxeM`）与 AT（`2ZGGCp1hX4DbaGl3I3xJUl2`）派发时用了 `instrumentType` / `maxTrade` /
  `nanHandling` / `unitHandling` / `startDate` / `endDate` / `simulationMode` 等 **camelCase** 键。
- `create_multi_simulation` 的入参模式只认 **snake_case**（`instrument_type` / `max_trade` / `nan_handling` /
  `unit_handling` / `test_period` …），**未知键被静默丢弃**且不报错。
- 后果：那两批以缺省 `nanHandling: OFF` / `maxTrade: OFF` 运行（实测 AS 子项 settings 为 OFF/OFF，
  换手 7.6–8.0% 显著高于同族 ~5.2%）。**AS / AT 的读数只作方向性证据，不进交付库存。**
- 已更正并重派：AT2 `4b0fqTbcc4D59iapyuv3ctB`（8 腿 d40，仍在排队）、AU `3RoRdO5AF5cL8ZYtW21zlyJ`（已完成，出 `wp9EvMmv`）。
- **纪律固化**：① 派发前 `mcp_get` 目标工具，参数名逐字照抄；② 派发后读回一个子项的 `settings`，
  断言 `nanHandling` / `maxTrade` 为 ON 再继续；③ 指标异常（换手偏高/偏低）先查设置，再归因信号。

### 55.5 全闸通过库存：14 颗 / 6 个 metric 族

平台 RA 闸全过（`failed_ra_count = 0`），全部 ATOM（analyst7 单数据集）。平台 `LOW_2Y_SHARPE` 线 = **1.58**。

| # | metric 族 | 形态 | p | decay | alpha | S | F | 2Y | sub | TVR |
|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | dps | 修订幅度 | 1.4 | 40 | `LL5dmv9a` | 1.71 | 1.02 | 2.41 | 0.95 | — |
| 2 | dps | 修订幅度 | 1.2 | 40 | `xA1d5YMW` | 1.76 | 1.03 | 2.39 | 0.98 | — |
| 3 | dps | 修订幅度 | 1.0 | 40 | `JjPvrxll` | 1.78 | 1.02 | 2.32 | 1.00 | — |
| 4 | ebt | 修订幅度 | 1.4 | 40 | `e76xGOQO` | 2.15 | 1.59 | 1.93 | 1.12 | — |
| 5 | ebt | 修订幅度 | 1.2 | 40 | `E5Vexv39` | 2.15 | 1.53 | 1.83 | 1.13 | — |
| 6 | ebt | 修订幅度 | 1.0 | 40 | `pwvK3P0V` | 2.11 | 1.43 | 1.71 | 1.11 | — |
| 7 | ebt | 4 周广度 | 1.4 | 40 | `P0MOK7wx` | 2.13 | 1.38 | 1.65 | 1.36 | — |
| 8 | ebi | 修订幅度 | 1.0 | 40 | `qME6VWbj` | 1.76 | 1.07 | 1.65 | 1.01 | — |
| 9 | gps | 修订幅度 | 1.4 | 80 | `3qjeJGle` | 1.72 | 1.08 | 1.80 | 0.95 | — |
| 10 | **pre** | 修订幅度 + `ts_zscore>1.0` 门控 | 1.4 | 80 | `6XAe27eL` | 1.74 | 1.10 | 1.62 | 0.96 | 4.17% |
| 11 | ebt | 1 周广度 | 1.2 | 40 | `MP0L2Ogo` | 2.03 | 1.24 | 1.76 | 1.20 | 7.32% |
| 12 | ebt | median 修订 | 1.2 | 40 | `A1Q729Ll` | 2.23 | 1.60 | 1.82 | 1.27 | 5.30% |
| 13 | ebt | high 修订 | 1.2 | 40 | `O0Jx2O6R` | 1.94 | 1.26 | 1.86 | 1.05 | 5.60% |
| 14 | **cps** | 4 周广度 + `ts_mean5` | 1.4 | 80 | `wp9EvMmv` | 1.80 | 1.01 | 2.00 | 1.27 | 4.31% |

metric 族覆盖：**dps / ebt / ebi / gps / pre / cps = 6 族**（pre、cps 为本轮新增）。

### 55.6 互相关与可同时提交上界（本地 4 年日收益，1021 点，阈值 0.7）

**新增腿的独立性判定（与既有 9 颗的最大相关）**

| 新腿 | 最大相关对象 | 相关 | 判定 |
|---|---|---:|---|
| `6XAe27eL`（pre） | `qME6VWbj` | 0.5078 | **新独立席位** |
| `wp9EvMmv`（cps 广度） | `P0MOK7wx` | 0.5725 | **新独立席位** |
| `MP0L2Ogo`（ebt 1 周广度） | `P0MOK7wx` | 0.8701 | 同族（4 周广度） |
| `A1Q729Ll`（ebt median） | `E5Vexv39` | 0.9423 | 同族（ebt 幅度） |
| `O0Jx2O6R`（ebt high） | `e76xGOQO` | 0.8611 | 同族（ebt 幅度） |

**关键读数**

1. **同族 p 变体不可并用**：dps 三颗 0.9704–0.9925；ebt 三颗 0.9728–0.9933（全库最高对 `e76xGOQO`–`E5Vexv39` = 0.9933）。
   ⇒ 每族只留一颗。
2. **ebt 广度 vs 幅度 = 0.6216–0.6815**（真独立）；**ebi 幅度 vs ebt 幅度 = 0.6957–0.7383**（边缘）。
3. **gps 最独立**（与所有族 0.37–0.63）；**cps 广度次之**（与所有 0.30–0.57）。
4. **最大互不相关团 = 7（精确解）**：
   `{LL5dmv9a, e76xGOQO, P0MOK7wx, qME6VWbj, 3qjeJGle, 6XAe27eL, wp9EvMmv}`，
   团内最大对 = `qME6VWbj`–`e76xGOQO` = **0.6957**（贴线但合规）。
5. 结论：**14 颗通过验证，但平台 SELF/PROD 0.7 线决定一次最多同时提交 7 颗**。其余 7 颗为二线/备选。

### 55.7 交付清单：10 颗 ATOM regular alpha

「席位」列：**A = 首批 7 颗互不相关团**（可同时提交）；**B = 二线**（与 A 中某颗相关 > 0.7，需等池子变化或作为替代提交）。

| 序 | alpha | metric 族 | 核心字段 | 算子逻辑 | S | F | 2Y | sub | 席位 |
|---:|---|---|---|---|---:|---:|---:|---:|---|
| 1 | `wp9EvMmv` | cps 广度 | `est_12m_cps_raisednum_4wks` / `_lowerednum_4wks` | `tn(signed_power(group_zscore(ts_mean(净上调占比,5), subindustry), 1.4), market)`，d80 | 1.80 | 1.01 | **2.00** | 1.27 | **A** |
| 2 | `e76xGOQO` | ebt 幅度 | `est_12m_ebt_mean` / `_mean_4wks_ago` / `_std` | `tn(signed_power(group_zscore(Δmean/std, subindustry), 1.4), market)`，d40 | 2.15 | 1.59 | 1.93 | 1.12 | **A** |
| 3 | `6XAe27eL` | pre 幅度（门控） | `est_12m_pre_mean` / `_mean_4wks_ago` / `_std` | 同上 + `trade_when(abs(ts_zscore(SIG,66)) > 1.0, ·, 0)`，d80 | 1.74 | 1.10 | 1.62 | 0.96 | **A** |
| 4 | `LL5dmv9a` | dps 幅度 | `est_12m_dps_mean` / `_mean_4wks_ago` / `_std` | `tn(signed_power(group_zscore(Δmean/std, subindustry), 1.4), market)`，d40 | 1.71 | 1.02 | **2.41** | 0.95 | **A** |
| 5 | `P0MOK7wx` | ebt 广度 | `est_12m_ebt_raisednum_4wks` / `_lowerednum_4wks` | `tn(signed_power(group_zscore(净上调占比, subindustry), 1.4), market)`，d40 | 2.13 | 1.38 | 1.65 | **1.36** | **A** |
| 6 | `qME6VWbj` | ebi 幅度 | `est_12m_ebi_mean` / `_mean_4wks_ago` / `_std` | 同 #2 形态，p1.0，d40 | 1.76 | 1.07 | 1.65 | 1.01 | **A** |
| 7 | `3qjeJGle` | gps 幅度 | `est_12m_gps_mean` / `_mean_4wks_ago` / `_std` | 同 #2 形态，p1.4，**d80** | 1.72 | 1.08 | 1.80 | 0.95 | **A** |
| 8 | `A1Q729Ll` | ebt median | `est_12m_ebt_median` / `_median_4wks_ago` / `_std` | `tn(signed_power(group_zscore(Δmedian/std, subindustry), 1.2), market)`，d40 | **2.23** | **1.60** | 1.82 | 1.27 | B（vs #2 0.934） |
| 9 | `MP0L2Ogo` | ebt 1 周广度 | `est_12m_ebt_raised_1wk` / `_lowered_1wk` | `tn(signed_power(group_zscore(净上调占比, subindustry), 1.2), market)`，d40 | 2.03 | 1.24 | 1.76 | 1.20 | B（vs #5 0.870） |
| 10 | `O0Jx2O6R` | ebt high | `est_12m_ebt_high` / `_high_4wks_ago` / `_std` | 同 #8 形态（high 替代 median），d40 | 1.94 | 1.26 | 1.86 | 1.05 | B（vs #2 0.861） |

说明：`tn(·)` = `group_neutralize(·, market)`；Δ = `subtract(当期, 4 周前)`；净上调占比 =
`divide(subtract(raised, lowered), add(raised, lowered))`。所有表达式完整字符串见 §55.1–§55.3 与 DB `expressions` 表。

**备选 4 颗（同样全闸通过，p 变体冗余）**：`xA1d5YMW`（dps p1.2）、`JjPvrxll`（dps p1.0）、
`E5Vexv39`（ebt p1.2）、`pwvK3P0V`（ebt p1.0）。

### 55.8 ATOM 合规核验

| 项 | 要求 | 实测 |
|---|---|---|
| 数据集 | 全部字段来自**同一 dataset id** | ✅ analyst7（`est_12m_*`） |
| 豁免组字段 | 只允许 `country/exchange/market/sector/industry/subindustry` | ✅ 仅 `subindustry` + `market` |
| 禁用算子 | `inst_pnl` / `convert` / `vector_neut(x, size)` | ✅ 0 处 |
| 2Y 闸 | 平台 ATOM 口径 `LOW_2Y_SHARPE ≥ 1.58` | ✅ 14/14 ∈ [1.62, 2.41] |
| IS Ladder | ATOM 豁免 | ✅ 无 `IS_LADDER_SHARPE` 检查项 |
| 金字塔 | 挂 EUR/D1/ANALYST（×1.3） | ✅ 14/14 |
| 塔位状态 | analyst 塔未点亮（需 3 颗，现有 1） | 存量唯一 analyst OS alpha = `786pLKnb`（`eps_revision_magnitude`），**不属 analyst7** ⇒ analyst7 在 OS 未被占用 |

### 55.9 字段画像与资产索引

- **本文件（主索引）**：`docs/reference/EUR/eur_analyst_field_profile_20261018.md`
  - §52 交付口径审计（9 颗期）+ §53 AQ + §54 AR + **§55 本轮收口**
  - 字段画像：§1–§30（1111 个 `est_12m_*` 字段的覆盖率 / 更新频率 / 分布 / 可用性 / 分档）
- **ATOM 约束与归因方法论**：`docs/reference/atom_workflow_and_attribution_20261013.md`
- **DB 台账**：`wqb-db` → `backtest_results` / `expressions`，波次键 `eur_a7_ab` … `eur_a7_au`（本轮新增 `eur_a7_al`、`eur_a7_ap`、`eur_a7_au`）
- **提交前置**：任何一颗提交前须 `submit_verdict`（否决权）+ 平台 `check_correlation(refresh=True)` 实测 prod < 0.7 + **用户明确确认**。

### 55.10 在飞 / 排队

| 批次 | id | 内容 | 状态 |
|---|---|---|---|
| AV | `EJUEmh0T5iUc6yXEPvv83R` | ebi/gps/prr 广度 × (d80 ± ts_mean5) + cps ts_mean10，8 腿 | 已派发 |
| AT2 | `4b0fqTbcc4D59iapyuv3ctB` | 广度类 2Y 修复（d40，8 腿，ON/ON） | 排队（child 0） |

AV 的目的只有一个：验证 §55.3 的 **d80 + 平滑** 杠杆能否把 ebi 广度（AR3/AR4 S 1.92–1.94、只差 2Y 0.19）
与 gps 广度（F 0.97、2Y 1.23）推过全闸。若 ebi 广度过闸，其与 ebi 幅度的相关预计 ~0.6 ⇒ **第 8 个独立席位**。
AV 出结果前，本节的 10 颗交付清单已完整可交付（14 颗通过验证 > 目标 10 颗）。

### 56. prod 实测（2026-10-20，check_correlation refresh=True）

对第一梯队 7 颗 + 3 颗 B 席逐一实测平台 prod（`check_correlation(refresh=True)`，结果已自动落库
`alphas.prod_correlation` / `prod_corr_source=check_correlation` / `corr_checked_at`）。

| alpha | 指标族 / 形态 | 本地 S | 平台 prod | 判定 | 平台 self（对已提交池） |
|---|---|---:|---:|---|---:|
| `6XAe27eL` | pre 幅度 + ts_zscore 门控 | 1.74 | **0.4857** | ✅ | 0.1797 |
| `LL5dmv9a` | dps 幅度 p1.4 | 1.71 | **0.4970** | ✅ | 0.1706 |
| `O0Jx2O6R` | ebt high 修订 p1.2 | 1.94 | **0.5129** | ✅ | 0.2214 |
| `3qjeJGle` | gps 幅度 p1.4 / d80 | 1.72 | **0.5710** | ✅ | 0.2484 |
| `e76xGOQO` | ebt 幅度 p1.4 | 2.15 | **0.6236** | ✅ | 0.3209 |
| `A1Q729Ll` | ebt median 修订 p1.2 | 2.23 | **0.6288** | ✅ | 0.2916 |
| `qME6VWbj` | ebi 幅度 p1.0 | 1.76 | **0.6609** | ✅ | 0.2674 |
| `MP0L2Ogo` | ebt 1wk 广度 p1.2 | 2.03 | 0.7186 | ❌ | — |
| `wp9EvMmv` | cps 4wk 广度 + ts_mean5 | 1.80 | 0.7201 | ❌ | — |
| `P0MOK7wx` | ebt 4wk 广度 p1.4 | 2.13 | 0.7952 | ❌ | — |

**判定：7 颗过 prod，3 颗不过。** 3 颗全是**广度形态**（cps 4wk、ebt 1wk、ebt 4wk），
prod 直方图在 [0.7,0.8) 桶分别 n=1 / 3 / 15；同数据集的**幅度形态**（ebt / dps / ebi / gps / pre）
全部落在 0.50–0.66。⇒ 在 analyst7 上，**修订幅度已不算拥挤、修订广度已被占满**，
后续再挖该数据集应优先幅度 / 水平量（median、high、mean 均可），广度只作降换手辅助。

**同时可提交上界 = 5 颗（exact）**：`compute_mutual_correlation(threshold=0.7, years=4, 1021 点)`
在 7 颗 prod 通过者上求最大完全子图，结果
`{6XAe27eL, e76xGOQO, LL5dmv9a, qME6VWbj, 3qjeJGle}`，圈内最大两两 = `e76xGOQO`–`qME6VWbj` **0.6957**。
`A1Q729Ll` / `O0Jx2O6R` 虽然 prod 也过（0.6288 / 0.5129），但与 `e76xGOQO` 分别 0.9342 / 0.8611、
彼此 0.7950 ⇒ 只能替换不能叠加，最大席位仍是 5。

**提交层预检（`submit_verdict`，5 颗）**：全部 `UNVERIFIABLE_404`（`GET /submit` 死端点），
`sim_fails=0`、`failed_ra=0`、`failed_ppa=0`，无硬闸 WARNING。软标记：
`MATCHES_THEMES`（5/5 命中 GLB/D1 TOPDIV3000 Theme ×2.5；`6XAe27eL` 另命中 D1 Power Pool Oct'26 2）、
`CLUSTER_TEST` WARNING（`6XAe27eL` 1.42 / `qME6VWbj` 1.45 / `LL5dmv9a` 1.28，线 1.58）、
`OSMOSIS_ALLOCATION` WARNING。稳健性台账：`e76xGOQO` / `LL5dmv9a` 已 PASS；`6XAe27eL` / `qME6VWbj` /
`3qjeJGle` 未落台账（fail-open，提交前需补跑 `brain-alpha-robustness`）。

⚠ 0.6957 距 0.7 仅 0.0043，平台 self 与本地 4 年口径可能有小幅出入 ⇒ 逐颗提交、每颗提交前用
`check_self_correlation` 复核；若第 5 颗被平台 self 拦下，落袋 4 颗，不硬凑。
