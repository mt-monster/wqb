# 提交执行包（2026-10-31）· GBR 15 + EUR 3 + IND 2 = 20 条

> **★ 两份执行包的分工（先读这段再动手）**
> - **本文件** = **上一轮**战役产出的 20 条（GBR 15 + EUR 3 + IND 2），跨 3 区。
> - 新战役（`tg_e0slvzlz2lmvv5lwqs`）GBR 未点亮塔深挖的 15 条 → 见 [`gbr_submit_execution_pack_campaign16_20261031.md`](gbr_submit_execution_pack_campaign16_20261031.md)（文件名含 `campaign16`，但已按 prod 终验定稿为 **15 条**）。
> - **两包互不覆盖**，但都涉及 GBR，提交前要合起来做**跨包篮内互相关**，不能只看包内。

> 全部 20 条：**RA 全过（`checks.fail` 空）· 对本区 OS 池 self-corr < 0.7 · 本地实测 prod < 0.7 · 篮内两两相关 < 0.7 · 配额纪律合规**。
> ⚠ 提交前对每条再跑 `check_correlation(refresh=True)` 当场终验 prod（本地值 2–3 天可漂移）。
> ⚠ **`checks.fail` 为空不等于过闸** —— 必须读 `ra.failed_ra_count == 0 && ra.failed_ppa_count == 0`（GBR 实测：卡项可能只出现在 `checks.warning` 里）。

## 1. 命名与标签映射（`set_alpha_properties` 直接用）

`name` 格式 `<REGION>_R_<family>_<NN>`（禁含 PROD 数值）。`tags` = `CH_REG` + `SRC_<数据集>` + `EXPRFAM_<族>`（≤5）。

| # | alpha | 区 | name | tags |
|---|---|---|---|---|
| 1 | `rKRQbPPE` | GBR | `GBR_R_fund_ebitda_ev_disp_252` | CH_REG, SRC_fundamental17, EXPRFAM_ev_valuation_disp |
| 2 | `MPYlNP8z` | GBR | `GBR_R_fund_ebit_ev_zscore_504` | CH_REG, SRC_fundamental17, EXPRFAM_ev_valuation_disp |
| 3 | `pwdQb78v` | GBR | `GBR_R_fund_ni_ev_disp_504` | CH_REG, SRC_fundamental17, EXPRFAM_ev_valuation_disp |
| 4 | `leAJn9e2` | GBR | `GBR_R_fund_ev_neut_volgate` | CH_REG, SRC_fundamental17, EXPRFAM_ev_valuation_disp |
| 5 | `rKRkL9QE` | GBR | `GBR_R_pvfund_capex_cap_disp` | CH_REG, SRC_fundamental6, EXPRFAM_capex_cap_displacement |
| 6 | `WjOkLGWx` | GBR | `GBR_R_pvfund_cheq_cap_disp` | CH_REG, SRC_fundamental6, EXPRFAM_capex_cap_displacement |
| 7 | `P0gvv5gE` | GBR | `GBR_R_model_epyield_disp` | CH_REG, SRC_predictive_starmine, EXPRFAM_eps_yield_displacement |
| 8 | `9qWwZ3go` | GBR | `GBR_R_model_mdl28_assetdrift` | CH_REG, SRC_model28, EXPRFAM_structural_drift |
| 9 | `6XKwmQgE` | GBR | `GBR_R_model_divyield_disp` | CH_REG, SRC_model109, EXPRFAM_dividend_yield_displacement |
| 10 | `leA6jmoe` | GBR | `GBR_R_news_eventrelevance_sum` | CH_REG, SRC_news17, EXPRFAM_event_intensity |
| 11 | `wpQwjWn6` | GBR | `GBR_R_news_relevance_count` | CH_REG, SRC_news17, EXPRFAM_arrival_rate |
| 12 | `6XdPedNJ` | GBR | `GBR_R_news_sse_count` | CH_REG, SRC_news18, EXPRFAM_sse_level |
| 13 | `9qxPX77V` | GBR | `GBR_R_news_sentiment_count` | CH_REG, SRC_news17, EXPRFAM_sentiment_arrival |
| 14 | `58E7jkaN` | GBR | `GBR_R_news_ssc_novelty` | CH_REG, SRC_news17, EXPRFAM_ssc_novelty |
| 15 | `akK2vpWW` | GBR | `GBR_R_shortinterest_txncount_mask` | CH_REG, SRC_shortinterest3, EXPRFAM_txn_count_mask |
| 16 | `omWVZ7lm` | EUR | `EUR_R_model_cassie_ocf_liab_delta` | CH_REG, SRC_quant_factor_lib, EXPRFAM_cassie_ratio_delta |
| 17 | `mL617YPx` | EUR | `EUR_R_fund_cfop_ratio_gate` | CH_REG, SRC_fundamental72, EXPRFAM_cf_quality_gate |
| 18 | `ZYAJZL93` | EUR | `EUR_R_analyst_epsrev_over_cv` | CH_REG, SRC_analyst_factor_signals, EXPRFAM_eps_revision_conf |
| 19 | `E5VNe67L` | IND | `IND_R_inst_disposed_ratio_regr` | CH_REG, SRC_institutions6, EXPRFAM_institutional_sellpressure |
| 20 | `pwv9eM76` | IND | `IND_R_analyst_flash_ebt_disp` | CH_REG, SRC_analyst_consensus, EXPRFAM_flash_estimate_disp |

## 2. 配额核算（按区独立）

| 区 | 塔位 | 条数 | 组合 | 判定 |
|---|---|---:|---|---|
| GBR | PV+FUND | 3（`rKRkL9QE` / `WjOkLGWx` / `leAJn9e2`） | 单两塔组合 ≤3 | ✅ 恰好卡线 |
| GBR | FUND 单塔 | 4 | 不吃组合配额 | ✅ |
| GBR | MODEL 单塔 | 2 · ANALYST 单塔 1 · NEWS 单塔 5 · SHORTINTEREST 单塔 1 | 不吃 | ✅ |
| GBR | trio 内部互组 | **0**（PV/MODEL/OTHER 无两两组合） | — | ✅ 零违规 |
| EUR | FUND+PV 1 · ANALYST 单塔 1 · MODEL 单塔 1 | PV 参与组合 1 | ≤5 | ✅ |
| IND | INST+PV 1 · ANALYST 单塔 1 | PV 参与组合 1 | ≤5 | ✅ |

## 3. 塔位预测（提交后）

| 区 | 塔 | 现状 | 提交后 | 新点亮 |
|---|---|---:|---:|---|
| GBR | PV | 1 | 4 | ✅ |
| GBR | FUNDAMENTAL | 0 | 4 | ✅ |
| GBR | NEWS | 0 | 5 | ✅ |
| GBR | MODEL | 5 | 7 | — |
| GBR | ANALYST | 3 | 4 | — |
| GBR | SHORTINTEREST | 0 | 1 | —（需 3 条） |
| EUR | MODEL/FUND/PV/ANALYST | 3/3/2/7 | 4/4/3/8 | — |
| IND | INSTITUTIONS/PV/ANALYST | 1/9/3 | 2/10/4 | — |

**⇒ 新点亮 3 塔：GBR 的 PV / FUNDAMENTAL / NEWS。**

## 4. descriptions 三段式模板（英文，≤100 词，实际提交时逐条填）

```
Idea: <机制一句话>.
Rationale for data used: <字段语义 + 为什么它代表该机制>.
Rationale for operators used: <算子链的因果链>.
```

各条机制句：
1. `rKRQbPPE` — EBITDA/EV 的 252 日自身偏离分位；EV 是 fundamental17 集内市场量口径，不引入 PV 字段 ⇒ 纯基本面塔。
2. `MPYlNP8z` — EBIT/EV 的 504 日 z-score 偏离（与 #1 同族不同几何/分子）。
3. `pwdQb78v` — 净利润/EV 的 252→504 日分位（净利润口径含杠杆与税后效应）。
4. `leAJn9e2` — EV 估值位移在成交量门控下的残差化版本（`returns` 波动率门控）。
5. `rKRkL9QE` — capex/市值 的 252 日位移 + 84 日分位（Novy-Marx 资本开支投资率族）。
6. `WjOkLGWx` — 普通股权益/市值 的同族位移（换分位口径 + 行业轴）。
7. `P0gvv5gE` — 盈利收益率（EPS yield）的 500 日位移。
8. `9qWwZ3go` — 结构性信用资产漂移的 250 日位移。
9. `6XKwmQgE` — 预期股息率的 500 日位移。
10. `leA6jmoe` — 新闻事件相关度的事件强度求和（注意力→短期反转，Da-Engelberg-Gao）。
11. `wpQwjWn6` — 新闻相关度的事件到达率。
12. `6XdPedNJ` — news18 事件情绪极性的到达率。
13. `9qxPX77V` — 事件情绪分到达率。
14. `58E7jkaN` — 情绪复合分 × 事件新颖度（乘子位放置信度，信号位放强度）。
15. `akK2vpWW` — 交易笔数的行业内排序，极端笔数区掩码（借券/换手族）。
16. `omWVZ7lm` — 经营现金流/流动负债（CASSIE 信用质量比）的 22 日位移。
17. `mL617YPx` — EBITDA/净利润门槛下的经营现金流/总资产质量比（`trade_when` 门控）。
18. `ZYAJZL93` — EPS 修正幅度 ÷ 预期系数变异（修正幅度相对置信度）。
19. `E5VNe67L` — 机构卖压占机构总持股比，对收益的时序回归残差（反向）。
20. `pwv9eM76` — 闪估 EBT 相对自身 252 日均值的偏离（行业内排序）。

## 5. 提交顺序建议

先提 **GBR 15 条**（点 3 塔、产出最快）→ 平台当场判 prod，撞墙的非破坏性 → 再提 EUR 3 + IND 2。
---

## 6. 替补池（2 条，USA）—— 主篮 prod 撞墙时顶上

> 理由：本地 prod 是**筛选器不是终验**（平台 prod 池 2–3 天可从 0.58 漂到 0.98）。
> 提交时若有条目 prod 越线，平台会拒收（**非破坏性**：alpha 保持未提交，不消耗塔位与配额）⇒ 用替补顶上，保证实际提交数达标。

| alpha | 区 | 塔位 | S | F | 2Y | SUB | prod | self | name | tags |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `9qxP0JbV` | USA | INSTITUTIONS + RISK | 2.45 | 1.74 | 2.76 | 1.87 | 0.5263 | 0.1032 | `USA_R_inst_shortpos_displ` | CH_REG, SRC_shortinterest, EXPRFAM_short_position_disp |
| `O0Jgd7Y7` | USA | OTHER 单塔 | 2.27 | 2.03 | 3.09 | 1.22 | 0.5655 | −0.0049 | `USA_R_other_buycount_zscore` | CH_REG, SRC_insider_trx_matrix, EXPRFAM_buy_count_zscore |

- 两条 `checks.fail` **均空**（平台实读），`failed_ra_count = 0`。
- 与主篮 20 条的互相关：7 条矩阵（USA 2 + EUR 3 + IND 2）**全部 < 0.7，最大 0.1824** ⇒ 零冲突。
- 塔位均**不含 trio 内部互组**（USA/D1/INSTITUTIONS+RISK、USA/D1/OTHER 单塔）⇒ 合规。
- ⚠ `zqbvOmOR`（USA，S **4.30**）**已被否**：`checks.fail = [HIGH_TURNOVER 1.7685 / CONCENTRATED_WEIGHT 0.5 / LOW_SUB_UNIVERSE_SHARPE 1.12<1.86]` ⇒ **S 再高也要读 `checks.fail`**，本地库的 failed_ra_count 是旧快照。

## 7. 执行顺序（建议）

1. **先提 GBR 15 条** —— 点 3 塔（PV 1→4 / FUNDAMENTAL 0→4 / NEWS 0→5），产出最快。
2. 逐条当场观察平台 prod 判定；**撞墙的当场用 USA 替补顶上**（互相关零冲突）。
3. 再提 EUR 3 条 + IND 2 条 —— 加固 MODEL / FUND / PV / ANALYST / INSTITUTIONS 塔。
4. 每条提交前：`check_correlation(refresh=True)` 终验 prod → `set_alpha_properties`（按 §1 的 name/tags + §4 的三段式描述）→ `workflow_submit_alpha(confirm_submit=True)`（**须用户确认，不可逆**）。
---

## 8. ★ v2 修订（2026-10-31 15:35）：近十年硬门槛复核后 —— 最终 **21 条**

### 8.1 十年逐年核查（`get_alpha_yearly_stats`，全部 22 条逐条实读）

**⇒ 3 条因「近十年数据不满」被剔除**（objective 第 4 条硬门槛）：

| alpha | 区 | 问题 |
|---|---|---|
| `omWVZ7lm` | EUR | **2014–2019 六年 longCount=0 / shortCount=0 / pnl=0** ⇒ `qfl_cassie`（`quant_factor_lib`）在 EUR 早期无覆盖 |
| `9qxP0JbV` | USA | **2014–2018 五年 longCount=0** ⇒ 空头持仓因子早期无覆盖 |
| `pwv9eM76` | IND | **2015 年 S = −0.26、pnl 为负** ⇒ 非十年全正 |

★ **这三条的 IS 全期指标都很好**（S 1.66–1.75 / prod 0.5378–0.5501 / self 0.19–0.50）⇒ **只看全期指标会把「数据不满十年」的 alpha 误当成优质候选。**

### 8.2 替补池扩到 3 条（全部合规）

| alpha | 区 | 塔位 | S | F | 2Y | SUB | prod | self | 十年 S |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `d5KPPrxx` | USA | OTHER 单塔 | **3.13** | **2.46** | **4.10** | 1.36 | 0.6737 | 0.1092 | 1.87–4.51 ✅ |
| `88vJ1YKa` | USA | OTHER 单塔 | **2.94** | 1.42 | 2.45 | 1.28 | 0.6933 | 0.2409 | 1.60–4.97 ✅ |
| `O0Jgd7Y7` | USA | OTHER 单塔 | 2.27 | 2.03 | 3.09 | 1.22 | 0.5655 | −0.0049 | 0.90–4.26 ✅ |

6 条矩阵（USA 3 + EUR 2 + IND 1）**全部 < 0.7，最大 0.3194** ⇒ 零冲突。

### 8.3 ★ 最终提交清单（21 条，五道闸全过）

| 区 | 条数 | 明细 | 塔位 |
|---|---:|---|---|
| **GBR** | **15** | `rKRQbPPE` `MPYlNP8z` `pwdQb78v` · `rKRkL9QE` `WjOkLGWx` `leAJn9e2` · `P0gvv5gE` `9qWwZ3go` `6XKwmQgE` · `leA6jmoe` `wpQwjWn6` `6XdPedNJ` `9qxPX77V` `58E7jkaN` · `akK2vpWW` | FUND 单塔 3 · **PV+FUND 3（≤3 恰好卡线）** · MODEL 2 · ANALYST 1 · NEWS 5 · SHORTINTEREST 1 |
| **EUR** | **2** | `mL617YPx` · `ZYAJZL93` | FUND+PV 1 · ANALYST 单塔 1 |
| **IND** | **1** | `E5VNe67L` | INST+PV 1（逐年 S **1.70–6.80**，2014 年 6.80） |
| **USA** | **3** | `d5KPPrxx` · `88vJ1YKa` · `O0Jgd7Y7` | OTHER 单塔 3 |

**五道闸全过**：① `checks.fail` 空 + `failed_ra_count = 0` ② 逐年 10/10 全正且每年 longCount>0、shortCount>0、pnl>0 ③ 对本区 OS 池 self-corr < 0.7 ④ 篮内两两相关 < 0.7 ⑤ 塔位无 trio 内部互组、单两塔组合 ≤3、trio×非trio ≤5。

**⇒ 塔位预测**：GBR **PV 1→4 / FUNDAMENTAL 0→4 / NEWS 0→5 ⇒ 点亮 3 塔**；USA OTHER 1→4；EUR MODEL 3→4 / FUND 3→4 / PV 2→3 / ANALYST 7→8；IND INSTITUTIONS 1→2 / PV 9→10 / ANALYST 3→4。

### 8.4 备选（47 条合格替补池，未纳入主篮）

`results/backup_screen_20261031.json` —— 47 条通过「checks.fail 空 + 十年满」，16 条被拒（10 条因某年 pnl<0、3 条因零持仓年、3 条因挂闸）。
⇒ 若主篮某条在提交时 prod 撞墙，可从该池按「族不同 + 塔位合规」挑替补（IND institutions6 回归族 29 条、USA 11 条、EUR 8 条）。
---

## 9. ★ 归因分析与失效风险（objective 第 2 条「回测时一定要做好归因分析和对比实验」）

**完整表**：`results/attribution_20261031.md`（逐条逐年 S 序列 + 收益集中度 + 压力年表现 + 风险分级）。
**数据源**：`get_alpha_yearly_stats` 平台实读（`results/yearly_stats_batch_20261031.json`）。**压力年** = 2019（贸易摩擦）/ 2020（疫情）/ 2022（加息）。

### 9.1 归因口径

| 指标 | 含义 | 阈值 |
|---|---|---|
| **最弱年 S** | 十年中最差年份的 Sharpe | < 1.0 ⇒ 该年几乎不赚钱 |
| **单年收益占比** | max\|pnl\| / Σpnl | ≥ 40% ⇒ 收益集中在单年 ⇒ 过拟合/行情依赖风险 |
| **压力年最弱 S** | 2019 / 2020 / 2022 三年的最低 Sharpe | ≤ 1.0 ⇒ 抗压性弱 |
| **负 pnl 年数** | pnl ≤ 0 的年份数 | > 0 ⇒ 十年非全正（硬门槛不合格） |

### 9.2 三条结论

1. **★ 21 条主篮无单年行情依赖**：单年收益占比 **16%–30%**（阈值 40%），负 pnl 年数 **全部为 0** ⇒ 收益分散在多年，**不是「撞上某一年」拟合出来的**。
2. **★ 压力年分化明显（这是提交排序的真依据）**：
   - 抗压强（压力年最弱 S > 1.5）：`E5VNe67L` **2.57** · `WjOkLGWx` 2.01 · `akK2vpWW` 1.91 · `6XKwmQgE` 1.90 · `9qWwZ3go` 1.73 · `6XdPedNJ` 1.56
   - 抗压中（1.0–1.5）：`leAJn9e2` 1.37 · `ZYAJZL93` 1.03 · `MPYlNP8z` 0.99 · `rKRQbPPE` 1.13 · `pwdQb78v` 0.86
   - **抗压弱（< 1.0，建议排在后面或替换）**：`9qxPX77V` **0.14**（2020 疫情几乎归零）· `mL617YPx` **0.41** · `58E7jkaN` 0.51 · `P0gvv5gE` 0.57 · `O0Jgd7Y7` 0.90 · `leA6jmoe` 0.74 · `wpQwjWn6` 0.36 · `rKRkL9QE` 0.71
   ⇒ **NEWS 族整体弱于 2020**（注意力机制在无新闻冲击的年份衰减）⇒ 提交顺序建议 **FUND/MODEL/INSTITUTIONS 族在前、NEWS 族在后**。
3. **★ 被剔的 3 条正好是集中度最高 + 有负年的**：`omWVZ7lm` 集中度 **46%** + 6 个零持仓年 · `9qxP0JbV` 30% + 5 个零持仓年 · `pwv9eM76` 19% + **2015 负 pnl** ⇒ 近十年门槛与集中度判据**互相印证**（不是重复检查同一件事）。

### 9.3 各机制族的最弱年画像（供「换机制」参考）

| 族 | 最弱年集中出现 | 解读 |
|---|---|---|
| NEWS（到达率 / 强度 / 情绪） | **2019 / 2020** | 注意力机制在无新闻冲击年衰减 |
| FUNDAMENTAL（估值偏离） | **2019**（`rKRQbPPE` 1.13）/ **2017**（`pwdQb78v` 0.29） | 财报季节奏驱动，年度分布不均 |
| MODEL（结构漂移 / 股息率 / EPS 收益率） | **2015**（`6XKwmQgE` 0.26 / `9qWwZ3go` 0.01） | 集中在 2015 宏观冲击 |
| INSTITUTIONS（机构卖压回归） | **2015** 1.70，但 **2014 高达 6.80** | 十年最稳、最强 ⇒ 建议优先提交 |
| SHORTINTEREST（笔数） | **2017** 0.96 | 借券机制在 2017 收紧期最弱 |
---

## 10. ★★★ 旧包 GBR 清单 prod 终验收口（2026-10-31 补测，覆盖 §8.3 的 GBR 15 条）

> **§8.3「GBR 15 条五道闸全过」的 prod 口径已作废**——当时「全 prod < 0.7」的读数失真严重。2026-10-31 对全部 8 条旧包独有 GBR 候选逐条 `check_correlation(production)` 终验（4 条补测 + 4 条复核）：

| alpha | §8.3 声称 | 2026-10-31 终验 prod | 判定 |
|---|---|---:|---|
| `58E7jkaN` | 待提交 | 0.5611 | **已提交（OS/ACTIVE，2026-10-30）** |
| `leAJn9e2` | 待提交 | **0.5507** | ✅ 存活（但与新包 `O0AKLMKq` 互相关 0.8493，二选一） |
| `leA6jmoe` | 待提交 | **0.7077** | ❌ 撞墙 |
| `rKRQbPPE` | 待提交 | **0.8141** | ❌ 撞墙 |
| `wpQwjWn6` | 待提交 | **1.0000** | ❌ 生产池完全克隆（n(0.9,1.0]=1） |
| `6XdPedNJ` | 待提交 | **1.0000** | ❌ 生产池完全克隆（n(0.9,1.0]=1） |
| `9qxPX77V` | 待提交 | **0.9399** | ❌ 撞墙（n(0.7,0.8)=1 且 n(0.9,1.0]=1） |
| `akK2vpWW` | 待提交 | **0.8774** | ❌ 撞墙（n(0.7,0.8)=2、n(0.8,0.9)=1） |

**⇒ 旧包 GBR 可提从 15 条收缩到 1 条（`leAJn9e2`）**，且它与新包 `O0AKLMKq`（0.8493）互斥。本包 GBR 部分**退役为历史记录**，实际提交以 `docs/reference/gbr_submit_execution_pack_campaign16_20261031.md`（新包 15 条）为准。

**教训（已入记忆）**：历史 prod 数字只能作排序参考——本例 0.55→1.0 级别的失真证明「旧读数 + 48h 保鲜」双重不可信；提交前必须逐条 `check_correlation(refresh=True)` 当场终验。`wpQwjWn6` / `6XdPedNJ` 的 prod=1.0 表明它们与生产池某条是**完全克隆**，这类候选连窗口救援的必要都没有。