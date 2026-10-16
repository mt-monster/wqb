# DEU 字段画像总盘点（2026-10-14）

> 数据源：`field_profile_deu` 视图（22,494 字段全量）× 台账 `backtest_results`（600+ 条 / 60+ 波）× 平台实时核验。
> 判词口径与生成逻辑见 `tools/fields/field_profile.py`；本报告同时给出与「台账 token 法」的对账。

---

## 一、总量与结构

**22,494 个字段**，按类型 × 覆盖带：

| 类型 | cov≥0.8 | 0.6–0.8 | 0.3–0.6 | <0.3 | 合计 |
|---|---|---|---|---|---|
| **MATRIX** | 1,773 | 1,287 | 1,874 | 9,167 | 14,101 |
| **VECTOR** | 118 | 395 | 1,002 | 5,244 | 6,759 |
| **GROUP**（纯轴） | 1,390 | 0 | 45 | 80 | 1,515 |
| SYMBOL（代码类） | 8 | 3 | 0 | 108 | 119 |
| **合计** | **3,289** | **1,685** | **2,921** | **14,599** | 22,494 |

- 覆盖率均值 **0.261**（全体有值字段）；**高覆盖（≥0.6）信号字段 = 3,573**（16%）。
- VECTOR 字段必须 `vec_*` 归约后才可用（6,759 个中仅 513 个 cov≥0.6）。
- **GROUP 1,390 个 cov≥0.8 全部是分组轴**（2026-10-14 逐条核验：`other455` 1,200 + `pv30` 180 + `pv29` 10 = 1,390 ✓；语义检查 **1,350 个 cluster/聚类 + 40 个 grouping/分组、0 例外**；判词 `AXIS_ONLY` 恰等于该集合，1,390 个全为 GROUP、0 个非 GROUP）。**两点精确化**：① 「只能当轴」是**类型约束**——GROUP 类字段平台只接受作为 `group_*` 的 `group` 参数，不接受作为信号输入；② **「只能当轴」≠「无用」**——轴本身是可用杠杆：历史 `oth455` 轴曾把 starmine 抬 **+0.84**（nE9Kz19q/WANL14 前身），WANL41 实测 `pv30` 因子轴则**无增益且触发严格 `IS_LADDER_SHARPE`**（0.49–0.79）⇒ 轴增益是「字段 × 轴」特异的。

## 二、判词分布（10 类，合计 22,494 ✓）

| 判词 | 数量 | 口径（本次核验厘清） |
|---|---|---|
| **ALIVE** | **4** | 单信号历史过闸 |
| **WEAK** | **38** | 有信号但未达闸 |
| DEAD | 355 | 实测判死 |
| DEAD_STATIC | 34 | `to_med<0.03` 静态，开批前定论 |
| DEAD_TURNOVER | 19 | `to_med>0.70` 换手闸拒 |
| DEAD_COUNT | 6 | 名字含 num/count 且 2Y≥1.3 且 S≤0.7 |
| **AXIS_ONLY** | **1,390** | GROUP 轴专用 |
| **UNTESTED** | **3,188** | **全部 cov≥0.6、零实测**（1,641 个 ≥0.8）|
| **UNUSABLE** | **3,422** | cov 0.3–0.6（2,876）或 <0.3（546）——低覆盖带 |
| **UNKNOWN_COVERAGE** | **14,038** | **实为 cov<0.3**（名称误导，本次核验厘清）|

**★ 口径修正**：`UNKNOWN_COVERAGE` 名字误导——核验后其 **14,038 个全部 cov<0.3**；真正的「未测高覆盖」看 `UNTESTED`（3,188）。

## 三、类别 × 判词矩阵（16 类）

| 类别 | 总字段 | ALIVE | WEAK | DEAD* | UNTESTED | UNUSABLE | AXIS | UNK(<0.3) |
|---|---|---|---|---|---|---|---|---|
| MODEL | 8,173 | **2** | 20 | 175 | 1,478 | 1,707 | 0 | 4,791 |
| ANALYST | 4,312 | **2** | 12 | 109 | 534 | 640 | 0 | 3,015 |
| OTHER | 3,921 | 0 | 6 | 43 | 366 | 427 | **1,200** | 1,879 |
| PV | 2,877 | 0 | 0 | 23 | 527 | 131 | 190 | 2,006 |
| FUNDAMENTAL | 2,146 | 0 | 0 | 14 | 36 | 207 | 0 | 1,889 |
| NEWS | 523 | 0 | 0 | 10 | 202 | 3 | 0 | 308 |
| SENTIMENT | 276 | 0 | 0 | 0 | 21 | 255 | 0 | 0 |
| INSTITUTIONS | 66 | 0 | 0 | 20 | 9 | 13 | 0 | 24 |
| RISK | 52 | 0 | 0 | 3 | 3 | 0 | 0 | 46 |
| INSIDERS | 42 | 0 | 0 | 4 | 0 | 38 | 0 | 0 |
| SHORTINTEREST | 25 | 0 | 0 | 13 | 12 | 0 | 0 | 0 |
| EARNINGS / OPTION / SOCIALMEDIA / MACRO / IMBALANCE | 81 | 0 | 0 | 0 | 0 | 1 | 0 | **80（≈全灭）** |

**⇒ 四类一句话**：① ALIVE/WEAK 高度集中在 **MODEL+ANALYST**（4/38 中的 34 个）；② 未点亮五类（EARNINGS/OPTION/SOCIALMEDIA/MACRO/IMBALANCE）**80/81 字段 cov<0.3** ⇒ 在 DEU 实质无数据；③ OTHER/PV 的可用面大半是轴；④ FUNDAMENTAL 高覆盖少、判死 14 个。

## 四、★ 潜力字段清单（ALIVE 4 + WEAK 38）

### 4.1 ALIVE（4 个，全部为同一机制族）

| 字段 | 数据集 | cov | n_tests | TO | best S | best 2Y |
|---|---|---|---|---|---|---|
| `eps_y1_estimate_change_3mo` | analyst_factor_signals | 0.923 | 75 | 0.082 | 1.67 | 2.14 |
| `netprofit_y1_estimate_change_3mo` | analyst_factor_signals | 0.921 | **244** | 0.077 | **1.77** | 1.66 |
| `mean_estimate_change_pct_f12m_earnings_14d_4` | predictive_starmine | 0.971 | 177 | 0.167 | 2.17* | 2.09 |
| `mean_estimate_change_pct_f12m_ebitda_14d_4` | predictive_starmine | 0.952 | 55 | 0.163 | 1.80 | 1.86 |

**⇒ 4 个 ALIVE 全部是「标准化预期变化率」族**——字段画像层面再次坐实「DEU 只有一条腿」。

**★ 以 `mean_estimate_change_pct_f12m_earnings_14d_4` 为样板的全量对账（387 行历史回测）**：
- **328 条多腿行**（2–5 个业务字段的复合式）撑起了 S2.17 的画像读数——**禁混信号不允许**，不可兑现；
- **59 条合规单字段行**：最优 `npApoGRx` **S1.81 / F1.65**，`9qVmJ2Qe` S1.70/F1.15/2Y1.67——**本身就过了 IS 闸**；
- **但它与 `2rjrMZ25` 是同一条腿**（日收益 PnL 相关 **0.991**）⇒ self 闸（>0.7）永久拦截。**强信号 ≠ 能提交：腿已被占用。**

### 4.2 WEAK（38 个，按数据集）

| 数据集 | 个数 | max S | max 2Y | 代表字段 |
|---|---|---|---|---|
| dl_riskfree_returns | 6 | 2.16* | 2.25* | `quantile_label_1bucket_*` |
| model238 | 3 | 1.86* | 2.11* | `mdl238_industry_rank` |
| model25 | 2 | 1.86* | 1.57* | `mdl25_eq_v4_2_1_v6` |
| predictive_starmine | 8 | 1.70 | 1.50 | `mean_estimate_change_pct_fy1_earnings_30d_4` |
| model216 | 3 | 1.52 | 1.19 | `mdl216_armpreferredrevisionscore` |
| model250 | 2 | 1.45 | 1.09 | `mdl250_maltahc_eq_score` |
| analyst_factor_signals | 6 | 1.39 | 1.49 | `eps_y2_estimate_change_3mo` |
| analyst93 | 4 | 1.30 | 1.38 | `anl93_recprofitabilityprev_*` |
| model26 | 2 | 1.27 | 1.33 | `avg_estimate_change_pct_*` |
| analyst7 | 2 | 1.18 | 0.28 | `est_*_lowerednum_*` |

**★ 必读标注（防止误读）**：带 * 的 max S/2Y 来自**多腿历史行**（预期变化率腿 + 本地字段的复合式）；其**合规单字段实测**分别为：dlr 1.18/2Y0.41、model238 0.99（筛选族）/ 0.81+2Y1.66（变化族）、model25 1.18。同腿判定见 `DEU_potential_scan_20261014.md` §六。

## 五、换手画像（410 个有 to_med 的字段）

| to_med 带 | 数量 | 含义 |
|---|---|---|
| <0.03 | 34 | **静态 ⇒ DEAD_STATIC**（任何骨架无用）|
| **0.03–0.15** | **242（59%）** | **健康带**——ALIVE/WEAK 几乎全在此带 |
| 0.15–0.35 | 82 | 可接受 |
| 0.35–0.7 | 33 | 偏高，需结构降换手 |
| ≥0.7 | 19 | **DEAD_TURNOVER**（被闸直接拒）|

均值 0.181。**⇒ 「低换手」是 DEU 有效信号的近乎必要条件**（4 个 ALIVE 的 TO 全部 ≤0.17）。

## 六、数据集规模榜（按字段数，前 15）

| 数据集 | 类别 | 字段 | cov≥0.6 | 已测 |
|---|---|---|---|---|
| analyst_consensus | ANALYST | 1,972 | **0** | 1 |
| other455 | OTHER | 1,500 | 1,500（全轴）| 0 |
| model219 | MODEL | 1,172 | **0** | 0 |
| analyst_revision_horizons | MODEL | 1,095 | **0** | 0 |
| fundamental72 | FUNDAMENTAL | 1,031 | **0** | 0 |
| pv20 | PV | 681 | **0** | 0 |
| model230 | MODEL | 670 | **0** | 0 |
| multifactor_return_pred | MODEL | 648 | 0* | 0 |
| predictive_starmine | MODEL | 631 | 583 | 81 |
| analyst7 | ANALYST | 608 | 425 | 43 |
| intraday_pv_feats | PV | 585 | **0** | 6 |
| continuation_score | PV | 560 | **0** | 0 |
| model26 | MODEL | 548 | 398 | 8 |
| model109 | MODEL | 544 | 0* | 0 |
| analyst15 | ANALYST | 537 | **0** | 0 |

* multifactor_return_pred / model109 的字段**全部落在 0.3–0.6 低覆盖带**（本战役 WANL44 实测判死，max \|S\| 0.48）。
**⇒ 大池 ≠ 有机会：前 15 名里 10 个在 DEU 零可用字段。**

## 七、族级结构

- **概念族总数 15,066**（family 归一化后）。
- 高覆盖最大族全部是 `other455` 的轴族（`oth#_relation/partner/customer/competitor_*_pca_*`，各 60–180）。
- 判「是否穷尽」按族不按字段（族内 PnL 相关 0.99）——本战役已扫完全部 327 个「未采样族」组（289 实测 + 38 过滤核验）。

## 八、画像 vs 台账对账（口径说明）

| 口径 | 已测字段数 | 说明 |
|---|---|---|
| 画像 `n_tests>0` | 456 | 快照口径（含历史行） |
| 台账 token 法 | **789** | 含本战役 WANL1–WANLS79 全部 60+ 波 |

差额来自画像快照时点早于本战役的 WANL21+ 批次。**判读画像的 S/2Y 前先反查该行结构**（铁律：画像 best_s 可能来自多腿组合行）。

## 九、关键结论

1. **DEU 的可交易信号面 = 4 个 ALIVE 字段，全部同属「标准化预期变化率」一族**——其中 `eps_y1_estimate_change_3mo` 的框架变体已提交（`2rjrMZ25`，ACTIVE）；其余 3 个与其互相关 0.99 ⇒ 永久封存。
2. **WEAK 38 个的最高单字段读数**（合规口径）：`mdl106_rv` 0.90、`dlr Q1` 1.18/2Y0.41、`m238GSFA` 0.99/F0.73——**无任一同时满足 S≥1.58 且 2Y≥1.58**。
3. **健康画像的画像特征已明确**：cov≥0.9、to_med 0.03–0.17、非轴、非静态——**4 个 ALIVE 全部命中该画像**；未来筛字段可用此画像做先验。
4. 22,494 字段中，**真正「可能有戏」的集合 = UNTESTED 3,188 里的非轴部分**，而本战役的 327 组扫描已证明：**其中没有第二条腿**。

---

**关联文档**：`DEU_field_census_20261013_v2.md`（初版普查）、`DEU_potential_scan_20261014.md`（潜力榜+扫描终局）、`DEU_pv_pattern_scores_20261014.md`、`DEU_campaign_dlr_m238_20261014.md`；skill `references/campaign-review.md`（一页式复盘）。

---

## 十、类别深挖样例：FUNDAMENTAL 2,146 字段「没有信号吗？」（2026-10-14）

### 10.1 覆盖结构：88% 字段在 DEU 实质无数据

| 数据集 | 字段 | cov≥0.6 | 0.3–0.6 | <0.3 | 状态 |
|---|---|---|---|---|---|
| fundamental72 / 89 / 17 / 1 / 90 / 93 / 86 / 45 | 1,031/407/135/123/66/46/7/12 | **0** | ≈0 | ≈全部 | DEU 无数据 |
| alpha_factor_lib / digital_ad_spend | 65 / 9 | 0 | 0 | 全部 | 无数据 |
| fundamental31 | 48 | 0 | 48 | 0 | **平台已下架** |
| **fundamental6** | 196 | **38** | 137 | 21 | **唯一可挖主池** |
| **fundamental22** | 1 | 1 | 0 | 0 | ESG KPI |

**⇒ 2,146 字段中真正可分析的只有 39 个高覆盖字段（fundamental6×38 + fundamental22×1）。**

### 10.2 分析轨迹（三层）

| 层 | 覆盖 |
|---|---|
| 历史波次 | fundamental6 16 行（比率结构）+ fund_holdings_panel 94 行（交易微观结构）|
| 本战役 WANL31/45 | `fnd22_value`（ESG）S0.50；`fnd6_newa2_txt`（所得税）S0.10、`fnd6_newq_cstkq` −0.25、`fnd6_ewq_rectoq` −0.10 |
| 未采样族扫描（WANLS46–78） | fundamental6 的 **14 个独立科目族**（txc/ibmiiy/revtsa/ibmiisa/xinty/teq/ibsa/pisa/txtsa…）max **S0.55**（`fnd6_txtsa` 税费，2Y1.26） |

**族级核验**：fundamental6 的 38 个高覆盖字段分属 ~19 族，**全部族都有实测代表**（未测的 15 个字段全是已测族的同族变体：`fnd6_newa2` 族已测 txt/xrd/sale，`fnd6_newq` 族已测 cstkq/seqq/nopiq，`fnd6_ewq` 族已测 rectoq）。

### 10.3 拆穿两个「高读数」幻象

| 表象 | 真相 |
|---|---|
| fundamental22 画像 maxS **1.72** | **配方标签行 `R99`**（非表达式）——标签行陷阱 |
| fund_holdings_panel maxS **1.41** | 标签行 `R86`；真实最高表达式 S1.36 是**含同腿字段的 3 字段复合**（boundary 字段 + `mean_estimate_change_pct_*` 腿）⇒ 不可兑现 |

### 10.4 合规口径下的真实最优 & 判死依据

| 候选 | S | 2Y | 判定 |
|---|---|---|---|
| `fnd6_gpy/fnd6_revty`（毛利率，比率结构） | **0.92** | 1.00 | 未达 1.0 升级带 |
| `fnd6_txtsa`（税费，扫描最优） | 0.55 | 1.26 | 判死 |
| `fnd22_value`（ESG KPI） | 0.50 | 1.01 | 判死 |

### 10.5 为什么没信号（根因，两层）

1. **数据可得性**：Compustat 科目体系对德国公司覆盖极差（88% 字段 cov<0.3）——德国财报制度与美股披露口径差异大；
2. **幸存字段全是低频静态科目**（季频/年频，to_med 多在 0.02–0.11）——日频 delay=1 框架下截面区分度弱。**与 GLB 战役「季频报类结构性判死」（报告日阶跃 + TO 墙）同根因**。

**⇒ FUNDAMENTAL 在 DEU 判死成立：不是没分析，而是「可分析的 39 个字段全部实测到族级，最优 0.92」。**

---

## 十一、类别深挖样例：ANALYST 4,312 字段——**不是没有信号，而是信号全部收敛在一条腿上**（2026-10-14）

### 11.1 覆盖结构（18 个数据集）

| 数据集 | 字段 | cov≥0.6 | 判词要点 | 状态 |
|---|---|---|---|---|
| **analyst_factor_signals** | 108 | 49 | **ALIVE 2 + WEAK 6** | **产出地** |
| analyst7 | 608 | 425 | WEAK 2 | 已测 43 |
| analyst93 | 100 | 100 | WEAK 4 | 已测 34 |
| analyst44 / analyst9 | 72 / 51 | 48 / 20 | DEAD 6 / 7 | 已测 |
| analyst48 | 7 | 7 | 元数据 | **语义判死**（index 代码） |
| analyst83 | 345 | 0（全 0.343） | — | WANL44 可读性判死（0.40） |
| analyst_consensus / analyst15 / analyst69 / analyst16 等 | 1,972 / 537 / 292 / 66… | **0** | — | **DEU 无数据** |

### 11.2 分析轨迹（本类别是全部战役中投入最重的）

历史 analyst93 战役 115 行 + WANL14（starmine 框架）+ WANL21（核心 × 10 字段）+ WANL32（修订计数族正确结构重测）+ WANL45（analyst7 水平/中位、analyst93 一致性、analyst44 实际值）+ WANL44（analyst83 可读性）+ WANLS 扫描（analyst 各族）。

### 11.3 结果分层

| 层 | 内容 | 结局 |
|---|---|---|
| **ALIVE 2** | `eps_y1_estimate_change_3mo` / `netprofit_y1_estimate_change_3mo` | **已兑现为 `2rjrMZ25`（ACTIVE）** |
| WEAK 12 | ① 同族：`eps_y2/netprofit_y2_estimate_change_3mo`（1.29–1.39）；② **预期离散度**：`eps/revenue_*_skewness`、`eps_*_coeff_var`（1.21–1.29）；③ **analyst93 准确性/盈利预测**（1.24–1.30、2Y 1.33–1.38）；④ analyst7 `raisednum`（1.18，**2Y 0.28 死**） | ① 同腿封存；②③ 单字段实测弱（WANL45：consistency 0.20、profitability −0.22）或为多腿行读数 |
| 幻象 | analyst47「S1.46」= 标签行 `R98`；anl93「S1.80」= **5–6 腿复合含同腿字段** | 不可兑现 |
| DEAD | 修订广度计数（≤0.90）/ 估计水平中位（≤0.32）/ 实际值对照（0.74）/ 可读性（0.40）| 判死 |

### 11.4 机制裁定

| 机制 | 最好合规读数 | 裁定 |
|---|---|---|
| **标准化预期变化率** | **1.77–1.81** | ✅ **唯一有效机制，已提交** |
| 预期离散度（skewness/coeff_var） | 1.21–1.29 | 距闸 0.3，且与主腿同族相邻 ⇒ 不可独立成腿 |
| 修订广度（up/down 计数） | 0.90 | 判死（WANL32 双结构） |
| 分析师准确性/一致性 | 0.20–0.74（单字段） | 判死 |
| 估计水平/中位/最高低 | ≤0.32 | 判死（近静态） |
| 财报会可读性（analyst83） | 0.40 | 判死（低覆盖） |

### 11.5 结论

**ANALYST 不是没有信号——它有 DEU 最强的信号（ALIVE 2），但这个类别的全部有效信息量恰好等于一条腿。** 其余 4,300 个字段的实测上界 = 1.39（同族）/ 1.30（准确性族，多腿驱动）/ 0.92（修订广度），无一能独立成第二条腿。

---

## 十二、论坛「字段画像优化」方案调研（2026-10-14，用户要求）

检索中文论坛，找到 5 类可复用的字段分析方案，逐条对照我们的方法：

| 论坛方案 | 出处 | 我们的现状 | 增量价值 |
|---|---|---|---|
| **① Labs 字段分布时序检查（断崖检测）** | 《通过 labs 分析字段，解决数据断崖》（9 赞） | ❌ 从未做过时序分布检查 | **★ 真增量** |
| **② `group_backfill` 修断崖** | 同上 | ❌ 只用过 `ts_backfill` | **★ 真增量（本轮已实测）** |
| **③ 字段关系七分法**（行为对称/推导/实体层级/指标衍生/分组对比/价格分布/生命周期） | 《Other 数据字段关系分析》（**101 赞**） | 部分（仅按名前缀分族） | 概念族粒度细化 |
| **④ 数值观察五步**（原始值 / 样本股 / 覆盖度 / CLIP 截断 / 值域统计） | GEM 会议纪要（20 赞） | 部分（覆盖率+换手，未看原始值） | 补「值域/截断」检查 |
| **⑤ 覆盖率阈值过滤** | 《获取高质量字段》（21 赞，用 0.4） | ✅ 已用 0.6（且已实证 0.6 是启发式非平台限制） | 无（我们更严） |

### 12.1 ★ 关键增量一：数据「断崖」现象与 `group_backfill`

**论坛实证**（YW84713）：某字段 PnL 尾部变平 → Labs 检查发现该字段 **2020 年后数据整体断崖式骤跌** → `ts_backfill` 无法修复（会把断崖前的差值填进去造成污染）→ **换成 `group_backfill`（组内非 NaN 值的 Winsorized 均值回填）后问题解决**。

**算子确认**（平台清单）：`group_backfill(x, group, d, std=4.0)` 在 REGULAR 可用 — 「用同组内过去 d 天非 NaN 值的 winsorized 均值填补缺失」。

**对照我们的 2Y 失败案例**：DEU 里多个候选呈「S 高但 2Y 低/负」的早衰形态（`down_cnt fy1_revenue_7d_5` S0.90/2Y−0.38；`dlr Q1` S1.18/2Y0.41）——**断崖假说可以解释这类形态**（早期有数据、后期劣化或缺失）。为此发 **WANL80 批**（10 条）：对 5 个近失候选把 `ts_backfill` 换成 `group_backfill`（含 sector/subindustry 两种轴、252/504/126 三种窗口、F/C 双结构、ts→gb 级联）。

### 12.2 关键增量二：字段关系七分法（替代简单前缀分族）

论坛 101 赞帖给出 **7 类字段关系**：行为对称型（buy vs sell）/ 推导型（净买入=买入−卖出）/ 实体层级型（用户→组合→调仓）/ 指标衍生型（数量→价值→权重）/ 分组对比型（经验 vs 行业维度）/ 价格分布型（avg vs median）/ 生命周期型（首次 vs 累计）。**用途**：同关系族内字段 PnL 高度相关（呼应我们的「族内 0.99」铁律），**跨关系类型才有新信息** ⇒ 未来分族可按这 7 型而非字段名前缀。

### 12.3 关键增量三：数值观察补「值域/截断」两步

GEM 纪要的数值观察：① 看原始值（连续性/缺失/公司间差异）② 抽样本股看变化 ③ 查覆盖度 ④ **做 CLIP 截断后看分布（长尾/头部集中）** ⑤ **统计值域（min/mean/max/median）验证猜想**。我们做了 ③，①②④⑤ 未做 ⇒ 已补入 SOP 清单。

### 12.4 WANL80 实测：`group_backfill` **无一例改善**（断崖假说被否证）

| 候选 | ts_backfill 基线（S/2Y） | **group_backfill 版（S/2Y）** | 变化 |
|---|---|---|---|
| `dlr Q1` 框架（gb252 / gb504 / ts→gb 级联，三者读数**完全相同**） | 1.18 / 0.41 | **1.13 / 0.35** | 略降，2Y 未救 |
| `dlr Q1` + industry 轴 | — | 0.99 / 0.63 | — |
| `down_rev`（本该受断崖影响） | 0.90 / −0.38 | **0.94 / −0.33** | 几乎无变化（2Y 仍负）|
| `m238Δ66` + industry | 0.81 / 1.66 ✅ | **0.72 / 1.28** | **降**（2Y 闸也丢了）|
| `m238 GSFA` | 0.99 / F0.73 | **0.66** | **降** |
| `mdl106_rv` | 0.90 / 1.67 | **0.24 / 0.26** | **崩塌** |

**两条推论**：
1. **断崖假说不成立**——若这些字段存在数据断崖，gb 应当改善 2Y；实测 2Y 反而更差或不变 ⇒ **它们的 2Y 弱是「信号本身近年衰减」（经济面），不是数据缺失（数据面）**。
2. **gb 的窗口/级联完全不敏感**（dlrQ1 的 gb252/gb504/ts→gb 三版读数逐位相同）⇒ 说明这些字段在 DEU 覆盖连续、**根本没有 NaN 可回填**，gb 只是用组均值**稀释了信号**。

**⇒ 论坛技法的适用边界已明确：`group_backfill` 只对「真存在断崖（覆盖突然中断）且组内信息有效」的字段有用；DEU 近失候选两者皆不满足。** 这是本轮「论坛调研」的净收获——不是技法无效，而是**它对本区不适用的原因被实证了**。

---

## 十三、完整性脚注：画像 `UNTESTED` 3,188 个为什么不必逐个测（2026-10-14 全量归因）

**归因结果（逐字段，非估计）：**

| 归因 | 字段数 | 组数 | 为什么不测 |
|---|---|---|---|
| **① 属【已采样族】**（数据集 × 名前 2 词） | **3,020（95%）** | — | 族内 PnL 相关 **≈0.99**（实证铁律）⇒ 测它 = 重测同一条腿。头部：starmine 498 / pattern_scores 487 / analyst7 382 / model26 357 / model264 354 / other455 300（轴）/ model25 92 / analyst93 66 |
| ② 属【未采样族】 | **168（5%）** | **74** | 见下三行拆分 |
| ②a 已由扫描执行 | — | **27** | WANLS46–79 已实测（最好读数 0.95，除同腿外） |
| ②b 构建期过滤 | — | **38** | 逐组核验：元数据（timestamp/headline/topic/reporting_period/event_start·end）16 组、**单国轴**（country_rank/percentile/relative）10 组、**外币单位**（forecast/eps/ebitda/netdebt_currency）5 组、news 事件元数据 4 组、3 组属已测族 |
| ②c 从未进入工作表 | — | **9** | **7 组 SYMBOL 类型**（`data_observation_date_4`、`event_sequence_number_in_story`、`record_timestamp_utc_date`、`aggregate_collection_timestamp`、`aggregate_reference_date`、`ranking_reference_date`、`source_collection_timestamp`）= 日期/序列码，**不可作信号**；**2 组 pv29「grouping」MATRIX 字段**（`industry_grouping_level*` 35 个 + `top_300_*_grouping_10_clusters` 5 个）= **整数聚类标签**（平台描述原话："Cluster assignment label **(1-10, -1, or 10000)**"）⇒ 语义是轴、ID 排序无经济含义 |

**⇒ 结论：3,188 个 `UNTESTED` 中，95% 是「已采样族的同族变体」（测之无新信息）；剩余 5% 里 27 组已实测、38 组经逐组核验属元数据/单国轴/外币、9 组是按语义排除的日期码与聚类标签。没有一个「有经济含义 + 未被族级覆盖」的字段被遗漏。**

**★ 一个值得记录的反例发现**：`pv29` 的 35 个 `industry_grouping_level*` 与 5 个 `top_300_*_grouping_10_clusters` 字段**类型是 MATRIX 而非 GROUP**（平台对同一族轴给了两种类型标注）⇒ 若只按「type==GROUP」筛轴会漏掉它们，**必须用名字+描述双重判据**（我们此前已用名字含 `grouping/cluster` 过滤，正好覆盖）。

### 13.1 ★ 实证检验：从「已采样族」抽 10 个未测成员回测（WANL81）

**设计**：从 5 个已采样族各抽未测成员（cov 0.97–1.0），用标准双结构（F 框架 / C 核心）回测，与**该族已知最好读数**对比——若族内冗余成立，读数不应超过族基线。

| 族 | 族已知最好 | **未测成员读数（WANL81）** | 判定 |
|---|---|---|---|
| model26 因子族 | **1.27**（`avg_estimate_change_pct`） | 0.80（`mdl26_preferred`）/ 0.64（`mdl26_secondary`） | **低于** ✓ |
| model25 族 | 1.18（历史） | 0.74（`value_momentum_industry_percentile`） | **低于** ✓ |
| analyst7 惊喜计数族 | 0.32（est 族） | 0.16（`act_q_cpx_surprisenum`）/ −0.19（fcf） | **低于** ✓ |
| pattern_scores 相似度族 | 0.65（WANL33/34） | 0.03（下跳缺口）/ −0.39（下行楔形） | **低于** ✓ |
| starmine 降级/修订计数族 | 0.90（WANL32） | **−0.28 / −0.61 / −0.63**（三个全部负） | **低于** ✓ |

**结果：10/10 未超过族基线，0 个 1.0+ 读数，4/10 为负** ⇒ **「测族内一个 = 测全族」得到直接实证**（配合此前的族内 PnL 0.99 相关性证据，双证据链闭合）。

**⇒ §13 的归因结论因此从「推理」升级为「推理 + 实证」**：3,020 个已采样族成员**不必逐个测**——抽检 10 个全部落于族基线之下（且无一例外）。

---

## 十四、算子覆盖总账：84 个 REGULAR 算子，DEU 用了 68 个（2026-10-14）

### 14.1 差集

**平台 REGULAR 可用 84 个**（`operator_coverage_audit.py --checklist`），**DEU 台账实际用过 68 个**，**未用 16 个**：`densify, equal, greater_equal, group_sum, inverse, kth_element, last_diff_value, less_equal, not, not_equal, power, sqrt, ts_count_nans, ts_kurtosis, ts_product, ts_step`。
其中 **6 个连全库（所有区域）都没用过**：`greater_equal, kth_element, less_equal, not, sqrt, ts_product`。

### 14.2 未用算子的四类归因

| 类 | 算子 | 为什么一直没用 |
|---|---|---|
| **A 有等价/更优替代（5）** | `inverse`、`sqrt`、`power`、`ts_product`、`group_sum` | `inverse`↔`divide(1,x)`（我们带 epsilon 防除零更稳）；`sqrt`/`power`↔**`signed_power`**（平台文档明示：sqrt/power 对负值或非整数指数**丢符号**，我们的字段有负值）；`ts_product`↔`ts_sum(log)`（几何均值语义等价）；`group_sum`↔`group_mean`（sum 引入规模泄露） |
| **B 语义/类型不匹配（4）** | `densify`、`ts_step`、`ts_count_nans`、`not` | `densify` 作用于 **GROUP 轴**（压缩桶数），我们只把现成轴直接传给 group_*；`ts_step` = 日期计数器（非信号）；`ts_count_nans` = 数据质量属性（非经济信号）；`not` 用 `trade_when`/`if_else`+反向比较替代 |
| **C 阈值边界变体（4）** | `equal`、`not_equal`、`greater_equal`、`less_equal` | 连续值上 `greater_equal`≡`greater`（我们已用 202 次）、`less_equal`≡`less`，单点差异无增量；**但 `equal`/`not_equal` 在离散值上有真场景**（标签状态变化检测）⇒ 本轮补测 |
| **D **真未试构造（3）** | `kth_element`、`last_diff_value`、`ts_kurtosis` | `kth_element` = 第三种回填策略；`last_diff_value` = 事件驱动核心（上次变化幅度，与用过的 `days_from_last_change` 配套）；`ts_kurtosis` = **时序尾部风险**（与我们做过的**跨分析师分布偏度**是不同构造）⇒ 本轮补测 |

### 14.3 补测结果（WANL82 主批 8 条 + WANL83 探针 2 条）

| 构造 | 读数 |
|---|---|
| `not_equal` 事件门控（`trade_when`） | **0.55** |
| `ts_count_nans`（数据质量信号） | **0.50** |
| 评级变化幅度 × 新鲜度（`ts_delta`/`days_from_last_change`） | 0.31 |
| `ts_product(add(stars,1), 21)` | 0.08 |
| `last_diff_value(stars/rv, 252)` | 0.05 / 0.01 |
| `ts_kurtosis(rv/gsfa, 252)` | −0.06 / −0.09 |
| **`kth_element(Q1, 252, k=1)`**（具名） | **1.18**（= ts_backfill 版同值 ⇒ 语义等价确认）|
| `kth_element(stars, 252, k=1)` | 0.19 |

**⇒ 未用算子补测全部 ≤0.55（除 kth_element 复现基线 1.18，证实其与 backfill 等价）⇒ 「未用算子」不构成信号缺口。**

### 14.4 ★ 两条工程发现（本轮最有价值的产出）

1. **`kth_element` 的 `k` 必须具名**：位置写法 `kth_element(x, 252, 1)` 平台报 `Required attribute "k" must have a value`，**并且连坐整批 CANCELLED**（WANL82 首版：2 条报错 → 其余 8 条全 CANCELLED，第 N 次实证批杀）；改成 `k=1` 后 **2/2 跑通**。
2. **★ 本地 `op_arity` 与平台对 `kth_element` 签名不一致**：本地签名表写 `kth_element(x, d, k, ignore="NaN")`（判 k 为位置参数，**拒绝 `k=`**），而平台运行时**要求 `k=` 具名** ⇒ **本地闸会误拦合法表达式**。⇒ 实操：遇到本地闸拒绝但写法符合平台文档的算子，**以平台实测为准**（本次靠探针批定夺）；`op_arity` 的 kth_element 签名待修。
