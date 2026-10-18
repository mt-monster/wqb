# KOR 数据集扫描与字段画像（2026-10-15 战役）

> 区域锁定 **KOR / TOP600 / D1**。已点亮数据集（≥3 颗提交）= `shortinterest38`(5)、`other466`(5) ⇒ **本轮全程排除**。
> 全量 87 个数据集，2 已点亮、22 已判死/已分诊、**63 个候选**。本文给出候选排序 + 入选数据集的完整字段画像。

---

## 一、S0 数据集全量扫描

评分模型（`tracking/KOR/scripts/kor_s0_scan.py`）：
`score = 2×valueScore + 覆盖甜蜜区(0.35–0.97 +1.5) + 字段富集度(≥20 +2.0 / ≥8 +1.5) + 拥挤度反向(alphaCount≤20 +4 … >3000 −3) + 冷门度(userCount≤10 +2)`

**关键先验（KOR 实证）**：KOR 的支配性障碍是 **prod 墙**不是 IS 闸；`alphaCount` 是 prod 墙密度最可靠的单因子代理
（d219–d232 战役：5 个数据集造出 IS 全闸候选，prod 仅 `shortinterest38` 过关）。⇒ **低 alphaCount 是选集第一优先**。

### 1.1 前 20 名（按机制多样性排序，非纯分数）

| rank | 数据集 | 类别 | 分数 | 字段数 | alphaCount | valueScore | 机制族 | 判定 |
|---|---|---|---|---|---|---|---|---|
| 1 | **fundamental90** | fundamental | 17.0 | 39 | 153 | 5.0 | 会计质量/舞弊评分 | **★入选** |
| 2 | **other395** | fundamental | 17.0 | 368 | 146 | 5.0 | 应计比率网格 | **★入选** |
| 3 | **fundamental44** | fundamental | 11.0 | 12 | 505 | 3.0 | 会计舞弊检测模型 | **★入选** |
| 4 | **other452** | fundamental | 18.0 | 46 | 40 | 5.0 | 税务应计/递延税 | **★入选** |
| 5 | **other401** | fundamental | 13.5 | 57 | 356 | 4.0 | GAME 治理会计 | **★入选** |
| 6 | **fundamental93** | fundamental | 16.0 | 46 | 63 | 4.0 | 税负比率 | 备选（同 other452 机制） |
| 7 | acquisition_model | other | 14.5 | 15 | 106 | 5.0 | M&A 被并购概率 | 备选（VECTOR 需 vec_avg） |
| 8 | other327 | other | 16.0 | 3 | 31 | 5.0 | 利率敏感度 beta | 备选（仅 1 字段可用） |
| 9 | pv70 | pv | 17.0 | 33 | 15 | 6.0 | 分析师预期汇总 | 备选 |
| 10 | fundamental21 | fundamental | 13.5 | 153 | 445 | 4.0 | ESG 评分 | 备选 |
| 11 | other553 | sentiment | 17.0 | 21 | 88 | 5.0 | 财务观点挖掘 | 备选 |
| 12 | sentiment21 | sentiment | 18.0 | 138 | 93 | 6.0 | AI 情绪分 | 备选 |
| 13 | mmp_nlp_sentiment | other | 20.0 | 521 | 68 | 6.0 | 多语言 NLP 情绪 | 备选 |
| 14 | other496 | other | 12.5 | 104 | 840 | 4.0 | 日内 FX 汇率 | 备选 |
| 15 | fundamental89 | fundamental | 15.0 | 368 | 148 | 4.0 | 应计盈利模型 | 备选（与 other395 同源） |
| 16 | other571 | other | 13.5 | 23 | 62 | 5.0 | Wikipedia 浏览量 | 备选 |
| 17 | model56 | fundamental | 12.5 | 9 | 158 | 3.0 | 券商研报评级 | 备选 |
| 18 | other315 | other | 11.5 | 32 | 471 | 4.0 | 股票互换 | 备选 |
| 19 | insiders1 | insiders | 9.0 | 9 | 544 | 3.0 | 内部人交易 | 备选 |
| 20 | pv103 | pv | 9.0 | 7 | 160 | 3.0 | 日内订单簿统计 | 备选 |

### 1.2 排除清单（附理由，避免重复劳动）

| 类型 | 数据集 | 理由 |
|---|---|---|
| **已点亮** | `shortinterest38`、`other466` | 各 5 颗提交，本轮排除 |
| 字段数不足 | `macro63`/`other100`/`socialmedia39`/`univ1`/`pv14`/`pv149`/`fundamental4`/`imbalance5` | 1–2 字段，无法建多腿正交组合 |
| 结构性退化 | `other106`(KOSPI 成分，cov 0.404 近静态)、`shortinterest5`(涨跌停，KOR 不适用→常量)、`pv29`(估值金字塔重复) | d233–d235 实测 S≤0 |
| 已知死族 | `pattern_scores`、`continuation_score` | 图表形态族三连死（RULES §G） |
| 饱和 | `pv1`(87k)、`fundamental23`(7.5k)、`dl_riskfree_returns`(7k)、`risk70`(7.9k) | alphaCount > 3000，prod 密墙 |
| 低频近静态 | `insiders5`(TO<0.31)、`fund_holdings_panel`(TO<0.1)、`pv37` | KOR 日频活跃信号源极少 |
| 已试双构型全灭 | `sentiment27`、`pv30` | d233–d235 |

---

## 二、入选数据集的字段画像

### 2.1 `fundamental90` — Governance, Accounting, Management, and Equality（fundamental）

**机制定位**：ML 模型集成（robust linear regression + modified xgBoost）输出的**治理/会计质量评分**。全部 MATRIX。
**画像价值**：**字段级 alphaCount 极低（多数 0–7）** ⇒ prod 墙密度低，是本轮最有希望的白空间。

| 机制子族 | 字段 | cov | aCnt | 语义方向 | 推荐模板 |
|---|---|---|---|---|---|
| **舞弊/破产评分**（高=风险） | `fnd90_qes_gamef_ohlson` | 0.798 | 29 | Ohlson 破产概率↑=风险 | `reverse(ts_backfill(F,252))` |
| | `fnd90_qes_gamef_mohanram` | 0.861 | 7 | Mohanram G-score（成长股舞弊） | `reverse(...)` |
| | `fnd90_qes_gamef_cscore` | 0.861 | 4 | Montier C-score 会计操纵 | `reverse(...)` |
| | `fnd90_qes_gamef_chs_default` | 0.781 | 5 | CHS 标准化破产 z-score | `reverse(...)` |
| **盈利能力**（高=好） | `fnd90_qes_gamef_grossprofit_asset` | 0.778 | **30** | 毛利/总资产 | 直取（不加 reverse） |
| | `fnd90_qes_gamef_icfroe_1y/3y/5y` | 0.73/0.68/0.63 | 2/1/0 | 增量现金流 ROE 1/3/5 年 | 直取，**5y 版 aCnt=0 最白** |
| **应计波动**（高=低质量） | `fnd90_game_accruals_vol` | 0.683 | 4 | 应计波动率 | `reverse(...)` |
| | `fnd90_game_eps_vol` | 0.614 | 1 | EPS 波动率 | `reverse(...)` |
| | `fnd90_qes_gamef_earn_var` | 0.772 | 1 | 盈利可变性 | `reverse(...)` |
| **现金流质量** | `fnd90_game_cash_flow_coverage` | 0.759 | 10 | 经营现金流覆盖债务 | 直取 |
| | `fnd90_game_inc_cash_tax` | 0.776 | 1 | 所得税费用/实缴现金税 | `reverse(...)`（税激进） |
| **资产结构** | `fnd90_game_noa` | 0.809 | 0 | 净经营资产 | 直取（acc=0 白空间） |
| | `fnd90_game_serial_special` | 0.801 | 1 | 特殊项/销售额 | `reverse(...)` |
| | `nonliquid_asset_ratio` | 0.824 | 0 | 非流动资产占比 | 直取 |
| | `fnd90_game_pension_ev` | 0.731 | 1 | 养老金义务/TEV | `reverse(...)` |
| | `fnd90_game_short_term_debt` | 0.676 | 0 | 短债占比 | `reverse(...)` |
| | `fnd90_game_tax_rate` | 0.798 | 0 | 有效税率 | `reverse(...)`（低税率=激进） |
| **营运效率（账龄）** | `fnd90_game_receivable_days` | 0.800 | 1 | 应收账款周转天数 | `reverse(...)` |
| | `fnd90_game_inventory_days` | 0.713 | 1 | 存货周转天数 | `reverse(...)` |
| | `fnd90_game_payble_days` | 0.734 | 0 | 应付账款天数 | 直取（占用上游资金=强势） |
| **成长/变动** | `fnd90_game_gma_chg` | 0.766 | 12 | 毛利率变动 | 直取 |
| | `fnd90_game_total_debt_chg` | 0.649 | 0 | 总债务变动 | `reverse(...)` |
| | `fnd90_game_depreciation_chg` | 0.757 | 3 | 折旧率变动 | `reverse(...)`（会计估计变更=操纵） |
| | `fnd90_game_inventory_chg` | 0.713 | 1 | 存货变动 | 直取 |
| | `fnd90_game_capex_dep` | 0.785 | 2 | 资本开支/折旧 | 直取 |
| **分析师乐观度** | `fnd90_game_optimism_gma` | 0.633 | 1 | 分析师乐观（毛利） | `reverse(...)` |
| | `fnd90_game_optimism_sale` | 0.650 | 6 | 分析师乐观（销售） | `reverse(...)` |
| **其他** | `fnd90_game_non_oper_inc` | 0.750 | 1 | 非经营收益/EBITDA | `reverse(...)` |
| | `fnd90_game_interest_investment_inc` | 0.779 | 4 | 利息投资收益 | 直取 |
| | `fnd90_game_minority_interest` | 0.630 | 1 | 少数股东权益占比 | `reverse(...)` |
| | `fnd90_qes_gamef_negative_earnings` | 0.848 | 5 | 负盈利次数 | `reverse(...)` |
| | `fnd90_qes_gamef_earnigs_timeliness` | 0.550 | 0 | 盈利及时性 z-score | 直取 |
| | `fnd90_game_sg_a_cost_ratio`/`_sg_a_vol`/`_debt_convertible` | — | 2/0/0 | SG&A 成本比/波动/可转债占比 | 见方向 |

**机制族小结**：**舞弊评分（4）+ 盈利质量（5）+ 现金流质量（2）+ 资产结构（6）+ 营运账龄（3）+ 成长变动（5）+ 分析师乐观（2）= 7 个正交子族** ⇒ 天然支持 3 腿正交组合。

---

### 2.2 `other395` — Accrual based Earnings Model（fundamental，368 字段）

**机制定位**：**应计比率（accruals ratio）的巨型网格**。全部 MATRIX，cov 0.34–0.81。
**画像价值**：**几乎全部字段 `alphaCount` 0–6**（300 个字段里 >90% aCnt ≤ 3）⇒ **KOR 全区最白的数据集**。

**命名结构解密**（这是画像的核心，名字会骗人，必须按 description 读）：
- `oth395_asset_{41..64}_{11..31}`：**资产类型 × 应计口径**
  - 前段 `41/42/43`=流动资产应计、`51`–`58`=非流动资产应计、`61`–`64`=金融资产应计
  - 后段 `11`=应计/总资产、`12`=应计/时序均值总资产1、`13`=…2、`21`=应计/流动资产、`31`=应计/销售额
- `oth395_jones_accrual_*`：Jones 模型应计（时序口径）
- `oth395_jones_accrual_pct_*`：可自由裁量应计**占比**
- `oth395_jones_accrual_r2_*`：回归 R²（拟合优度）
- `oth395_jones_nondiscretionary_*`：非自由裁量应计
- `oth395_csjones_all_*`：横截面标准化版本
- `oth395_best11/21_*`：应计比率的历史统计（`_current_t` 当前 t 值、`_dts` 标准差、`_mean/_max/_min/_length`、`_accum_4q` 四季累加）
- `oth395_fixed1313_*` / `fixed1513_*`：固定窗口版本

| 机制子族 | 代表字段 | cov | aCnt | 语义 | 推荐模板 |
|---|---|---|---|---|---|
| **总应计水平**（高=低质量，**经典异象**） | `oth395_asset_41_11`（流动/总资产） | 0.613 | 2 | Sloan 应计异象主腿 | `reverse(ts_backfill(F,252))` |
| | `oth395_asset_61_11`（金融/总资产） | 0.653 | 1 | 金融资产应计占比 | `reverse(...)` |
| | `oth395_asset_51_11`（非流动/总资产） | 0.616 | **0** | 长周期应计 | `reverse(...)` |
| **应计 t 统计量**（当期偏离历史均值） | `oth395_best11_d1_current_t` | 0.519 | 1 | 当前应计的 t 值 | **直取，已自带标准化** |
| | `oth395_best21_d1_current_t` | 0.552 | 0 | 同上变体 | 直取 |
| **应计波动** | `oth395_best11_d1_dts` | 0.604 | **0** | 应计比率历史标准差 | `reverse(...)` |
| **应计持续性** | `oth395_best11_d1_accum_4q` | 0.543 | 1 | 四季应计累加（持续性） | `reverse(...)` |
| **资产扩张**（经典异象） | `oth395_best11_d1_asset_double_history` | 0.805 | 4 | 资产是否翻倍 | `reverse(...)` |
| | `oth395_best11_d1_asset_half_history` | 0.805 | 1 | 资产是否腰斩 | 直取 |
| | `oth395_asset_d1_asset_change` | 0.670 | 1 | 最新资产/ltm 资产 | `reverse(...)` |
| **可自由裁量应计占比**（舞弊核心） | `oth395_jones_accrual_pct_other_12`（经营） | 0.399 | **0** | 自由裁量应计/总应计 | `reverse(...)` |
| | `oth395_jones_accrual_pct_other_14`（营运） | 0.384 | **0** | 营运资本自由裁量 | `reverse(...)` |
| **回归 R²**（盈余管理代理） | `oth395_jones_accrual_r2_other_12` | 0.382 | **0** | Jones 回归拟合度 | `reverse(...)` |
| **横截面标准化** | `oth395_csjones_all_other_12` | 0.511 | **0** | 全市场标准化经营应计 | `reverse(...)` |
| **行业中性化版** | `oth395_csjonesindustry*_*` | 0.46–0.52 | 0–2 | 行业内标准化 | `reverse(...)` |
| **非自由裁量应计** | `oth395_jones_nondiscretionary_accrual_other_12` | 0.399 | **0** | 非裁量部分 | 直取 |

**机制族小结**：**总应计水平 + t 统计量 + 应计波动 + 应计持续性 + 资产扩张 + 自由裁量占比 + R² 拟合度 = 7 个正交子族**。
**注意**：`jones_*` / `csjones_*` 段 cov 只有 0.34–0.51（多为小盘/老股），`asset_*` 段 cov 0.52–0.65，`best11/21_*` 段 cov 0.80（覆盖最好）。

---

### 2.3 `fundamental44` — Accounting Quality Models（fundamental，12 字段）

**机制定位**：**舞弊/重述检测模型**。cov 全部 0.898（覆盖极好），但 aCnt 36–118（本轮里拥挤度中等）。

| 字段 | cov | aCnt | 语义 | 方向 |
|---|---|---|---|---|
| `fnd44_cashflow_accruals` | 0.898 | 67 | 经营现金流 vs 会计盈利差额/总资产 | **reverse**（高应计=低质量） |
| `fnd44_perc_accruals` | 0.898 | 58 | 净应计/百分比应计 | **reverse** |
| `fnd44_working_capital_accruals` | 0.898 | 63 | 营运资本应计/总资产 | **reverse** |
| `fnd44_yoon_wc_accruals` | 0.898 | 63 | Yoon 模型营运应计 | **reverse** |
| `fnd44_jones_cf_accruals` | 0.898 | 36 | Jones 模型现金流应计 | **reverse** |
| `fnd44_modified_jones_cf_accruals` | 0.898 | 53 | 修正 Jones（仅信用销售可裁量） | **reverse** |
| `fnd44_mscore` | 0.898 | 65 | Beneish M-Score 舞弊概率 | **reverse** |
| `fnd44_fscore` | 0.898 | 118 | F-Score 错报概率（低=健康） | **reverse** |
| `fnd44_factor_benford` | 0.898 | 116 | Benford 法则偏离（法证） | **reverse** |
| `fnd44_probability_restatement` | 0.898 | 52 | ML 重述概率（美国训练） | **reverse** |
| `fnd44_probability_restatement_global` | 0.898 | 62 | 区域调整版重述概率 | **reverse** |
| `fnd44_score` | 0.898 | 78 | 综合会计质量分（wolf_csi） | 直取 |

**画像要点**：**12 个字段全部是「高=低质量」同向语义** ⇒ 单腿不会产生强横截面区分（都是同一个方向），
**必须靠「模型分歧」造信号**：不同模型对同一家公司的打分差异（`subtract(rank(A), rank(B))`，**同源同数据集 ⇒ 合规**）
是本数据集独有的正交维度。`fscore` 是「低=健康」的反向计分 ⇒ 与 mscore 方向相反，天然对冲。

---

### 2.4 `other452` — Earnings Tax Data（fundamental，46 字段）

**机制定位**：**税务应计 + 递延税 + 费用/负债的时序统计**。aCnt 0–5（极白）。

| 机制子族 | 代表字段 | cov | aCnt | 语义 | 方向 |
|---|---|---|---|---|---|
| **税务应计** | `oth452_tax_accruals_11` … `_51` | 0.47–0.63 | **0** | 税务应计（9 个口径变体） | **reverse** |
| **递延所得税费用** | `oth452_deferred_tax_expense_11` … `_51` | 0.44–0.54 | 0–5 | 递延税费用（5 口径） | **reverse** |
| **递延所得税负债** | `oth452_deferred_tax_liability_11` … `_51` | 0.49–0.72 | 0–2 | 递延税负债（6 口径） | **reverse** |
| **应计时序统计** | `oth452_accruals_d1_current_t` | 0.485 | 2 | 应计当前 t 值 | 直取（已标准化） |
| | `oth452_accruals_d1_dts` | 0.584 | **0** | 应计标准差 | **reverse** |
| | `oth452_accruals_d1_max/_mean/_min/_length` | 0.52–0.70 | 0–3 | 应计历史统计 | 见方向 |
| **费用/资产变化** | `oth452_expense_d1_asset_change` | 0.890 | 1 | 费用/资产变化 | **reverse** |
| | `oth452_liability_d1_asset_change` | 0.899 | 4 | 负债/资产变化 | 直取 |
| | `oth452_accrualsratio_d1_asset_change` | 0.901 | 2 | 应计率/资产变化 | **reverse** |
| **费用/负债时序统计** | `oth452_expense_d1_current_t` / `liability_d1_current_t` | 0.36/0.44 | 0–1 | t 值 | 直取 |

**画像要点**：cov 0.90+ 的三个 `_d1_asset_change` 字段是本数据集**覆盖最好的开波槽位**；
`_current_t` 字段已自带时序标准化，**不需要再套 ts_zscore**（重复标准化会杀信号）。

---

### 2.5 `other401` — Governance, Accounting, Management（fundamental，57 字段）

**机制定位**：GAME 模型的治理/会计/管理层因子（与 `fundamental90` **同源不同版**，cov 略低 0.27–0.74）。

**独有字段（`fundamental90` 没有的 ⇒ 真正的增量）**：

| 字段 | cov | aCnt | 语义 | 方向 |
|---|---|---|---|---|
| `oth401_qes_gamef_pscore` | 0.739 | 10 | **Piotroski F-score**（财务健康，**高=好**） | 直取 ★ |
| `oth401_game_earning_smooth` | 0.651 | 13 | **盈余平滑度**（管理层粉饰） | **reverse** ★ |
| `oth401_game_relative_rtn_vol` | 0.739 | 5 | 相对波动率 | **reverse** |
| `oth401_qes_gamef_cashflow_var` | 0.653 | 5 | 现金流可变性 | **reverse** |
| `oth401_game_gross_margin_vol` | 0.593 | 2 | 毛利率波动 | **reverse** |
| `oth401_game_an_cov_chng` | 0.269 | 8 | 分析师覆盖变化 | 直取 |
| `oth401_game_eps_sur_vol` | 0.488 | 3 | 分析师预测误差 | **reverse** |
| `oth401_game_deferred_tax_asset_chg` | 0.577 | 17 | 递延税资产变动 | **reverse** |
| `oth401_game_non_production_asset` | 0.618 | 12 | 非生产性资产 | **reverse** |
| `oth401_game_sg_a_inefficiency` | 0.688 | 13 | SG&A 无效率 | **reverse** |
| `oth401_game_finished_goods` | 0.587 | 13 | 产成品/存货 | 直取 |
| `oth401_game_equity_dilution` | 0.340 | 5 | 股权稀释 | **reverse** |
| `oth401_game_deferred_sal_chg` | 0.362 | 4 | 递延收入变动 | 直取 |
| `oth401_game_eff_interest_rate` | 0.535 | 4 | 有效利率 | **reverse** |
| `oth401_game_asset_turnover_chg` | 0.674 | 15 | 资产周转变动 | 直取 |

**画像要点**：**`pscore`（Piotroski，高=好）是唯一「正向计分」的治理分** ⇒ 与 mscore/ohlson 反向腿天然正交，
是本区最有价值的「模型分歧」腿。

---

## 三、机制 → 模板映射（画像的落地口径）

| 字段形态 | 判据 | 模板 | 依据 |
|---|---|---|---|
| **已自带时序标准化** | desc 含 `t-statistic` / `current_t` / `percentile` | **裸 `group_rank(reverse?(F), 轴)`**，不套 ts_zscore | 重复标准化杀信号 |
| **慢变水平比率** | cov 高、季频 | `ts_backfill(F, 252)` + cap 连续桶分组 | d219–d232 实证：季频字段必须回填否则 NaN 过多 |
| **离散评分**（0–1 / z-score / 概率） | desc 含 `score`/`probability` | **禁 `winsorize` / `signed_power`**（无连续尾部，零效果） | 项目铁律 |
| **同向语义多模型**（fundamental44） | 全部「高=低质量」 | `subtract(rank(A), rank(B))` **同源减法造分歧** | 同数据集 ⇒ 合规（价差腿不带系数） |
| **正/反向计分对**（mscore vs pscore） | 方向相反 | `add(rank(A), rank(B))` 等权 rank 叠加 | d274c 实证：rank 组合 S +56% |
| **单字段不足 3 腿** | — | 跨数据集**机制正交**组合（现金流质量 × 舞弊评分 × 应计波动） | 估值腿会稀释 S（d274b C1/C3 实证） |

**统一壳层（已验证破 prod 墙三段链）**：
```
trade_when(greater(rank(adv20), 0.6),
  tail(group_rank(reverse?(ts_backfill(F, 252)), bucket(rank(cap), range="0,1,0.2")),
       lower=0.2, upper=0.8, newval=0.5), -1)
```
KOR/TOP600/D1 · **MARKET**（第 4 次实证 MARKET 是 2Y 钥匙）· decay4 · trunc 0.08

---

## 四、开波设计（d276-A，18 结构）

| 槽 | 数据集 | 字段 | 机制族 | 方向 |
|---|---|---|---|---|
| A1–A4 | fundamental44 | `cashflow_accruals` / `perc_accruals` / `working_capital_accruals` / `yoon_wc_accruals` | 应计水平 | reverse |
| A5–A8 | fundamental44 | `mscore` / `factor_benford` / `probability_restatement` / `jones_cf_accruals` | 舞弊检测 | reverse |
| A9–A12 | fundamental90 | `ohlson` / `mohanram` / `cscore` / `chs_default` | 舞弊/破产评分 | reverse |
| A13–A14 | other395 | `best11_d1_accum_4q` / `asset_41_11` | 应计持续性 / 总应计 | reverse |
| A15–A16 | other401 | `pscore` / `earning_smooth` | **正向治理分** / 盈余平滑 | 直取 / reverse |
| A17–A18 | other452 | `tax_accruals_11` / `deferred_tax_liability_11` | 税务异象 | reverse |

**设计原则**：① 一次覆盖 **5 个机制族**（应计/舞弊/破产/治理/税务）而非单族深挖；② 同一壳层便于横向比较；
③ 每族含至少一个**正向计分腿**（A15 pscore）以验证「方向假设」而非只测 reverse。

---

*文档生成：`tracking/KOR/scripts/kor_s0_scan.py`（数据集评分）+ MCP `get_datasets` / `get_datafields` 实时拉取（2026-10-15）*