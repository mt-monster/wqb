# DEU 逐数据集分析 · 2026-10-07

> **总量**：178 个数据集 → **46 个有高覆盖字段**（可用）→ **132 个零高覆盖**（结构性不可用）。
> 分四类：**A 已测有产出** / **B 已测无产出** / **C 未测有潜力** / **D 结构性不可用**。

---

## 〇 总览表（46 个可用数据集）

| 数据集 | category | 字段 | 高覆盖 | 状态 |
|---|---|---:|---:|---|
| `other455` | other | 1500 | **1500** | ❌ 已测（MATRIX 作信号全灭） |
| `predictive_starmine` | model | 631 | **583** | ✅ **产出 `58gkLAkk`（已提交）** |
| `pattern_scores` | pv | 504 | **504** | ❌ 已测（40 条全灭） |
| `analyst7` | analyst | 608 | **425** | ❌ 已测（计数类，2Y有S无） |
| `model26` | model | 548 | **398** | ❌ 已测（W94 全崩） |
| `model264` | model | 380 | **380** | ❌ 已测（单信号 S0.74） |
| `pv30` | pv | 285 | **180** | 🚫 全 GROUP，只能当轴 |
| `model25` | model | 217 | **108** | ❌ 已测（单信号 S1.18） |
| `analyst93` | analyst | 100 | **100** | ⚠️ **部分族是活的**（见 B4） |
| `news18` | news | 70 | **70** | ❓ **未系统测** |
| `dl_riskfree_returns` | other | 133 | 57 | 🚫 实为分位数桶标签，非信号 |
| `pv29` | pv | 50 | **50** | 🚫 全 GROUP，只能当轴 |
| `analyst_factor_signals` | analyst | 108 | **49** | ✅ **产出 `9qWX78vV`（就绪）** |
| `analyst44` | analyst | 72 | **48** | ❌ 已测（单信号 S0.74） |
| `news17` | news | 48 | **48** | ❓ 未测 |
| `news20` | news | 46 | **46** | ❓ 未测 |
| **`model216`** | model | 45 | **45** | ⚠️ **VECTOR 族！从未用正确包装测过** |
| `analyst_earnings_ibes` | model | 42 | **42** | ❌ 已测（`closing_price_dlr2` S0.95） |
| `fundamental6` | fundamental | 196 | **38** | ❌ 已测（7 族 70 条，最高 S1.03） |
| `news50` | news | 37 | **37** | ❓ 未测 |
| **`model28`** | model | 25 | **25** | ❓ **未测** |
| **`shortinterest3`** | shortinterest | 25 | **25** | ⚠️ 有历史高分（但为多腿） |
| **`model238`** | model | 22 | **22** | ❌ 刚测（天花板 S1.33） |
| **`model53`** | model | 22 | **22** | ❓ **未测** |
| `analyst9` | analyst | 51 | 20 | ❌ 历史换手爆表（0.73~1.47） |
| **`model36`** | model | 20 | **20** | ❓ **未测** |
| **`fund_holdings_panel`** | institutions | 18 | **18** | ❓ 未测 |
| **`sentiment27`** | sentiment | 18 | **18** | ❓ **未测** |
| `other250` | other | 12 | 12 | ❓ 未测 |
| **`institutions6`** | institutions | 11 | **11** | ❓ 未测 |
| `news104` | news | 11 | 11 | ❓ 未测 |
| `model30` | model | 14 | 10 | ❓ 未测 |
| `other47` | other | 18 | 9 | ❓ 未测 |
| `model106` | model | 14 | 8 | ❌ 历史换手爆表（0.80） |
| `other532` | other | 8 | 8 | ❓ 未测 |
| `analyst48` | analyst | 7 | 7 | ❓ 未测 |
| `risk60` | risk | 5 | 5 | ❓ 未测 |
| `model250` | model | 20 | 4 | ❌ 刚测（S1.33，2Y −0.38） |
| `sentiment7` | sentiment | 3 | 3 | ❓ 未测 |
| `insider_agg_matrix` | insiders | 34 | 2 | ❓ 未测 |
| `insider_matrix` / `insider_trx_matrix` | other | 33/33 | 1/1 | ❓ 未测 |
| `analyst47` | analyst | 5 | 1 | ❓ 未测 |
| `stock_cluster_dl` | other | 5 | 1 | ❓ 未测 |
| `fundamental22` / `risk88` | — | 1/1 | 1/1 | ❓ 未测 |

---

## A 已测有产出（2 个）

### A1 `predictive_starmine`（model，583 高覆盖）—— ✅ **1 颗已提交**

| 机制 | 字段 / 构造 | 结果 |
|---|---|---|
| **M1 变化率水平** | **`mean_estimate_change_pct_f12m_earnings_14d_4`** + 4 轴重框架 @decay8/gran0.1 | ✅ **S1.75 / 2Y2.07 → `58gkLAkk` 已提交 ACTIVE** |
| M1 同族兄弟 | `_7d_4` / `_30d_5` / `_60d_4`（cov 均 0.97） | ❌ S1.08~1.19 |
| M1 换指标 | `_f12m_ebitda_14d_4` | ⚠️ 轻框架峰值 S1.41（距闸 0.17） |
| M12 时点 | `ts_arg_min/max` | ❌ S≤0.69 |
| M13 自相关 | `ts_corr(x, ts_delay(x,22), 252)` | ❌ 最好 S1.50（2 闸） |
| ARM 族 | `analyst_revisions_score_2` / `arm_score_change_30d_4` | ❌ 0.54 / 0.11 |
| 财报时点 | `days_since_last_report_3` | ❌ 0.30 |

**★★ 审计**：该数据集的历史 413 条记录里 **205 条（50%）是多腿等权 `add` 组合**（合规禁用）—— S1.9~2.2 全是它们的产物。

### A2 `analyst_factor_signals`（analyst，49 高覆盖）—— ✅ **1 颗就绪**

| 机制 | 字段族（数量） | 结果 |
|---|---|---|
| **M1 变化率** | **`eps_y1_estimate_change_3mo`** | ✅ **S1.65 / F1.47 / 0 失败 → `9qWX78vV`（塔 DEU/D1/ANALYST）** |
| M1 同族 | `eps_y2` / `netprofit_y1,y2` / `revenue_y1,y2`（7 个） | ❌ 最高 S1.35 |
| M2 修正广度 | `*_raisednum`/`*_lowerednum`（44 组） | ❌ S0.68 |
| M3 幅度 | `*_revision_magnitude`（3） | ❌ S0.78 |
| **M4 分歧收敛** | `*_{skewness,asymmetry,coeff_var}`（**17 个，最大类**） | ❌ ≈0（有研报依据仍全灭） |
| M5 水平偏离 | `*_consensus_value`（6） | ❌ <0 |

**★ 结论**：49 个字段分 7 类，**只有「变化率」一类携带信号**。

---

## B 已测无产出（8 个）

### B1 `pattern_scores`（pv，504 全高覆盖）—— ❌ 40 条全灭
形态相似度：`<形态名>_<统计量>_simscore_lookback{60,120}`。测过 M9 过延伸差形 / 水平形 / pv30 GROUP 轴 / 时序归一 / 桶粒度 / decay。
**最好 S0.46。** 换手 0.14~0.29（快信号，延长 decay 会抹平）。

### B2 `analyst7`（analyst，425 高覆盖）—— ❌ 计数/修正类
命名 `est_12m_<指标>_<统计>`。测过 `_num` / `_raised_1wk` / `_lowered_1wk` 等。
**症状：2Y 有信号（1.59~1.67）、S 极低（0.53~0.65）** ⇒ 计数类判死形态。

### B3 `model26` / `model264` / `model25`（model，各 ~400/380/108）—— ❌
- `model26`：W94 十个机制全崩
- `model264`：单信号最好 S0.74（`mdl264_amihud_class`），且历史高分全为多腿
- `model25`：单信号最好 S1.18（`mdl25_eq_v4_2_1_v6`）

### B4 `analyst93`（analyst，100 **全 VECTOR**）—— ⚠️ **部分族是活的（重要修正）**
- 测过 `accuracy` / `consistency` / `correv` / `estimator` 族 × 7 种 `vec_*` 聚合 → **S ≤0.43**，且换手 0.019~0.029（静态属性）
- **★ 但有活的族**：`anl93_recprofitabilityprev_*_profitability2`（**换手 0.0795 正常，历史单信号 S1.30，n=19**）
  - 我用获胜配方实测仅 S0.84 ⇒ **需按轴深/窗长扫描找它的最优框架**
- **⇒ 修正**：不能说"analyst93 整体是死的"，只能说"`accuracy`/`consistency`/`correv`/`estimator` 这 4 族是静态的"

### B5 `fundamental6`（fundamental，38 高覆盖）—— ❌ 最高 S1.03
7 个机制族 × 70 条：内部比率（0.37）/ **价值收益率（0.89，最强）** / 规模化改善（0.60）/ PEAD 事件门控（1.03，CW 互斥）/ 回归残差（0.33）/ 变化构造（0.46）。
**平台无 `regression_neut`**（只有 `group_neutralize` / `ts_regression`）。

### B6 `other455`（other，1500 高覆盖）—— ❌ MATRIX 作信号全灭
- **1200 个 GROUP**（关系聚类）→ 只能当轴（我们一直在用）
- **300 个 MATRIX**（`*_value` 关系图节点嵌入）→ 作信号全灭（**换手 0.012，是静态结构特征**）
- **⇒ 正确用法**：当连续分组轴，不是信号

### B7 `analyst44`（analyst，48）—— ❌ 单信号 S0.74（`anl44_2_eps_value`），且该族历史换手爆表 1.64

### B8 `model238`（model，22）—— ❌ 天花板 S1.33
11 个 cov=1.0 的 `*_rank` 字段。三阶段推进（轻探针/轴深/双窗）最好 **S1.33 / sub0.54** ⇒ 候选为真但**不够强**。

---

## C 未测有潜力（**16 个数据集，共 ~330 个高覆盖字段**）

**按优先级排序（高覆盖字段数 × 机制新颖度）：**

| 优先 | 数据集 | cat | 高覆盖 | 为什么值得先测 |
|---|---|---|---|---|
| **1** | **`model28`** | model | **25** | 唯一产出过 alpha 的 category，且**从未碰过** |
| **2** | **`model53`** | model | **22** | 同上 |
| **3** | **`model36`** | model | **20** | 同上 |
| **4** | **`model216`** ⚠️ | model | **45** | **VECTOR 族**！历史单信号 S1.45，**从未用正确 `vec_avg` 包装测过** |
| **5** | **`news18`** | news | **70** | 全新机制（新闻供给） |
| **6** | **`news17`/`news20`/`news50`/`news104`** | news | **142** | 同上 |
| **7** | **`sentiment27`/`sentiment7`** | sentiment | **21** | 全新机制（情绪） |
| **8** | **`shortinterest3`** | shortinterest | **25** | 做空行为；有历史高分（多腿） |
| **9** | **`fund_holdings_panel`/`institutions6`** | institutions | **29** | 机构持仓（全新机制 M18） |
| **10** | `model30`/`model106`/`model250` | model | 22 | model106 换手爆表，model250 刚测 S1.33 |
| **11** | `other250`/`other47`/`other532`/`stock_cluster_dl` | other | 30 | 小池，但 other 有 oth455 之外的族 |
| **12** | `analyst48`/`analyst47`/`analyst9` | analyst | 28 | analyst9 换手爆表 |
| **13** | `insider_agg_matrix`/`insider_matrix`/`insider_trx_matrix` | insiders | 4 | 内部人交易（全新机制） |
| **14** | `risk60`/`risk88` | risk | 6 | 风险因子 |
| **15** | `analyst_earnings_ibes` | model | 42 | 已测 1 个字段（S0.95），未系统测 |
| **16** | `dl_riskfree_returns` | other | 57 | **实为分位数桶标签，非信号** ⇒ 不建议 |

---

## D 结构性不可用（132 个数据集，零高覆盖）

**代表**：`analyst_consensus`（历史换手 1.36 爆表）/ `fundamental72`（1031 字段但高覆盖 0）/ `fundamental89`（407/0）/ `pv20`（681/0）/ `intraday_pv_feats`（585/0）/ `continuation_score`（560/0）/ `ai_news_scores` / `earningscall_sentiment` / `order_book_imbalance` / `techindi_model` / `chart_cnn_alpha` …

**⇒ 这 132 个数据集在本区（DEU）覆盖率不足 0.6，**不必投入**。

---

## 结论：下一步的最优路径

**DEU 的可用面已经画清楚了：46 个数据集里，2 个有产出，8 个已判死，16 个未测（~330 字段），132 个不可用。**

**⇒ 最高优先级 = 按顺序打 C 类的 1~7 号**：

1. **`model28` / `model53` / `model36`（model，67 个高覆盖字段）** —— 唯一产出过 alpha 的 category 里**三个完全未碰的数据集**
2. **`model216`（45，VECTOR）** —— 用**正确的 `vec_avg` 包装**重测（此前白测）
3. **`news18` 等 5 个 news 数据集（212 个）** —— 全新机制，且论坛指出**未被大量 Alpha 使用**（prod 墙压力小）
4. **`sentiment27`（18）** —— 全新机制
5. **`shortinterest3`（25）/ `fund_holdings_panel`（18）/ `institutions6`（11）** —— M18 机制的载体

**每开一个池的流程（已验证）**：
```
1. get_datafields 拉权威字段清单（含 type）→ 按机制分类
2. 查换手边界（TO<0.03 剔除 / >0.7 剔除）
3. 查历史记录：只取"合规单信号"的最佳值（多腿全部剔除）
4. 轻框架探针 1 批 → 判断有无信号
5. 有信号 → 轴深扫描 + 窗长扫描（**找该字段的最优框架**）
6. 再推进过闸
```
