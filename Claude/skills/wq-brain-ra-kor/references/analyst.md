# KOR × analyst（组合分支）

> 回到 [KOR 区域流程](../SKILL.md) · [KOR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/KOR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region KOR --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst10、analyst14、analyst16、analyst44、analyst_consensus、analyst_factor_signals

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | KOR | 区域 settings.json |
| universe | TOP600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 175 | 13 | 2 | 2 | 10 | 0 |

主要数据集（回测数）：analyst10（105）、analyst44（42）、analyst16（15）、analyst14（8）、analyst_consensus（3）、analyst_factor_signals（2）

### S1 字段理解

- 分清 actual_*（已实现、事后）与 mean_estimate_* / flash（预测、前瞻）：IND analyst_consensus 前 16 条全灭的真因是用了 actual（DEC-77）
- VECTOR 先 vec_avg / vec_count 聚合；JPN 下 vec_* 外再套 ts_* 会报错
- 窗口（类别卡，均在白名单内）：monthly 22/66；quarterly 66/252

### S2 生成

- **用**：只作辅助腿 / 条件（KOR profile 绿榜改写，2026-10-04）
- **避**：analyst10 / 16 / 44 / consensus 作主信号撞 prod 墙（RULES §G）；不再上提 analyst 族作主数据集（KOR profile 步 2）
- **类别通用原语**（类别卡，跨区）：
  - revision surprise: change in FY1/FY2 vs the stale level
  - dispersion: disagreement across estimates, not the consensus mean
  - breadth vs magnitude: how many estimates moved, not how far the mean moved
  - horizon gap: FY2 minus FY1 as a growth-expectation residual
  - rating momentum: upgrade/downgrade frequency vs historical baseline
  - target price gap: current price vs consensus target (upside/downside)
  - estimate acceleration: second derivative of estimate revisions
- **跨区结论**（USA/GLB/HKG/KOR/EUR/DEU/GBR；negative）：flash / pretax 一致预期动量族只在 IND 有效，别的区 ／S／ 都在 1.07 以下（证据：waves probe_flash_eps_20260919 / probe_pretax_20260919：USA ≤0.09、GLB ≤0.08、HKG 0.64、KOR ≤1.07、EUR ≤0.96、DEU ≤0.72、GBR ≤0.54） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/USA/DEU；negative）：分析师主信号族普遍撞 prod 墙（证据：KOR analyst10/16/44/consensus（RULES §G）；USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL（E/P z prod 0.93）；DEU analyst93 prod 饱和） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(estimate)（必须 ts_delta 或 group_zscore）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize）入场（原举例 regression_neut / vector_neut 均已被平台移除，2026-10-10 op-lint 实测）
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region KOR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| KOR-ANALYST-FACTOR-SIGNALS-EPS-GROWTH-NOSIGNAL-20261004 | analyst_eps_growth_factors | 冷门数据集先 1-2 条裸探针验 IS 强度再投入完整波次；／S／<0.5 即判死，勿直接发 8 条完整波（d27 教训：8 条全灭 best S=0.56） | analyst_factor_signals | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANALYST14-DISAGREEMENT-NOSIGNAL-20261003 | analyst_estimate_dispersion | ★ 冷门 ≠ 有信号。白名单里 medAlphaCnt≈1 的数据集仍可能完全无预测力。『社区未占』只保证 prod 空间，不保证 IS 强度。选集应先做 1-2 条裸探针验 IS 强度，再投入完整波次。 | analyst14 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANALYST16-EST-PCT-DEAD | analyst16 | analyst16不再投任何变体 | analyst16 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANL10-INNOVATION-DEAD | innovation_score | analyst10 innovation_score 族（pre/sal/dps innovation_score + innovate_increase/decrease）判死，不再投任何变体 | analyst10 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANL16-EVENTSPARSE-WEAK | analyst | Do not reinvest in analyst16 raw event fields in KOR; only revisit if combined with ts_backfill+trade_when AND a fundame | analyst16 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANL16-MODEA-CEILING | analyst_estimate_modea | anl16_afterest_percentage 不再投 ModeA 变体 | analyst16 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANL44-ANALYST-DEAD | analyst_estimate | anl44_* 系列字段不再投任何变体 | analyst44 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANL44-EPSREVISION-PRODWALL | analyst-eps-revision | Do not submit any KOR eps_estimate revision momentum variant (prod>=0.7 invariant). Recipe kept for leg-swap research: i | analyst44 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANLCONS-EPSRATIO-DEAD | analyst_consensus.eps_revision | 禁止再用 4w_prior/当期 比率作为主信号；若再用一致预期需走意外值/分散度压缩等事件型结构 | analyst_consensus | payload | <!-- lint:const-ok 证据原文 -->
| KOR-ANLCONS-GROSSMARGIN-DEAD | analyst_consensus.grossmargin | 禁止再用 analyst_consensus 的 grossmargin 族字段构造信号；dividend 修正族仅微弱正向（≤0.39）不足以成线，低优先 | analyst_consensus | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-09~12 会话实证（100+ 条实验）：analyst 族的两层真相

**第一层（已确认）**：analyst **主信号**在 KOR 结构性不可用——与上文 10 条判死记录、台账三者一致。
台账实测：`analyst_consensus` 最高 **S 1.07**、`analyst14` 0.56、`analyst_factor_signals` 0.20；
唯一 S>1.58 的 `JjGwjd5E`(S1.70) 是**全局禁用的 `add` 混信号**且 **prod 0.8258**。

本会话独立复现（勿重试）：

| 结构 | 结果 |
|---|---|
| 单腿 `group_rank(eps_y2_estimate_change_3mo, sector)` | **S 1.07（天花板）** |
| × 价格反转腿 `multiply(rank(analyst), rank(-ts_rank(returns,N)))` | S 1.85–2.21 但 **2Y 0.28–1.21** ❌ |
| × 新闻情绪腿 `vec_avg(mws38_tone_score)` | **TO 1.2** ❌ |
| `group_zscore` 替 `group_rank` | **更差**（S 0.92 vs 1.05）⇒ 技能「group_zscore > group_rank」**在 analyst 族反向** |

**第二层（★ 本轮最大修正）**：**判死是「数据集级」，不是「类别级」。**
判死记录只覆盖 **6 个** dataset（analyst10/14/16/44/analyst_consensus/analyst_factor_signals），
而 KOR analyst 类共 **17 个**，另有 **11 个从未结构挖掘**：

| 数据集 | 字段/aCnt/vs/cov | 价值 |
|---|---|---|
| **`analyst9`** | 48 / 95 / vs4 / 0.567 | **修正广度**：`anl9_s_numup`/`anl9_s_numdn`/`anl9_s_numanalysts`（VECTOR cov 0.711，aCnt 5–14）⇒ 上调家数占比（`divide` 比率形态：分子 = up 笔数之和、分母 = up 与 dn 笔数之和）**，与 shortinterest38 已证有效的「流量比值」同构，对应类别原语 *breadth vs magnitude* |
| **`analyst_base_ref`** | 14 / 19 / vs5 / **0.732** | **意外+分歧**：`consensus_surprise_percentage`(aCnt 20)、`consensus_stddev_estimate`(**aCnt 0**)、`consensus_mean_estimate`、`num_estimates_consensus`/`reported_actual_value`(**aCnt 0**)，外加 **MATRIX 满覆盖** `last_close_price`/`number_of_issued_shares` ⇒ 可构造 **SUE** `divide(vec_avg(surprise), vec_avg(stddev))` 与 **分析师 E/P** `divide(vec_avg(mean_est), last_close_price)` |
| **`analyst11`** | 210 / 31 / **vs6** / 0.583 | **ESG 族**（`overall_sustainability_score` 等，aCnt 0–3）|
| `analyst81` | 5 / 10 / vs6 / 0.265 | **违约概率**（`anl81_probability_of_default_percent`）|
| 其余 | analyst39(0.895/cov 最高)、analyst46/45/48/25/4/15 | 未试 |

⇒ **选集指令修正**：上文「分析师全红灯」应读作 **「已试的 6 个 dataset 红」**；用户点名 analyst 时，
应先给出这 11 个未试集的清单，而不是直接判类别死。

### 2026-10-12 续：6 个未试集实测结果（★ analyst 是**类别级**上限）

按上表逐个实测 6 个未试数据集（d186–d192，共 48 条）：

| 数据集 | 用的机制/字段 | 最高 S | 关键观测 |
|---|---|---|---|
| **`analyst39`**（IBES 式基本面，43 字段 cov 0.90–0.998）| **E/P** `divide(anl39_ttmepsincx, close)` | **1.12** | 另有 **TPgap 2Y 1.53**、**TPdisp 2Y 1.44**（`anl39_tp_all_delay_1_*`）；B/P 0.20 |
| `analyst9`（修正广度）| 上调家数占比（`divide` 比率形态：分子 up 笔数之和、分母 up 与 dn 笔数之和）| 1.09 | **TO 仅 0.048**（余量 14×）|
| `analyst_base_ref`（意外+分歧）| SUE `surprise/stddev`、E/P | 0.63 | SUE 2Y 1.25–1.52 |
| `analyst46`（观点评分）| `anl46_indicator` / `anl46_sentiment` | 0.42 | 判死 |
| `analyst11`（**ESG**，210 字段）| 四支柱 | **0.01** | **判死**（S −0.19~0.01）|
| `analyst81`（违约概率）| — | 批失败 | 待补 |

**未探（5 个）**：`analyst45`(241/cov 0.253)、`analyst48`(70/0.441)、`analyst25`(207/0.5)、`analyst4`(308/0.633)、`analyst15`(304/0.526)。

**已证无效的抬 S 结构（勿重试）**：
- **多窗乘积** `multiply(rank(-ts_rank(X,a)), rank(-ts_rank(X,b)))` ⇒ S **−0.50~−0.57**（与 PV 族**相反**）。
- **跨集条件化/分组** `group_rank(sig1, bucket(rank(field2)))` / `trade_when` / `if_else` ⇒ 最高 0.92，`if_else` **−1.34**。
- **`ts_kurtosis` 三窗钥匙** ⇒ S **−1.25 / −1.18**（analyst 字段非收益分布型）。
- `ts_delta` / 覆盖度×广度 / `ts_zscore` 短窗 ⇒ 全负或 ≤0.68。

★ **判定：analyst 族 S 天花板 ≈1.1，现已 5 个数据集独立复现**
（analyst39 **1.12** > analyst9 1.09 > 台账 analyst_consensus 1.07 > analyst_base_ref 0.63 > analyst14 0.56）。
⇒ 与「数据频率」有关：analyst 信号 TO 天然 0.02–0.06（季度更新），信息量不足以越过 IS 1.58 闸；
**这是类别级结构上限，换数据集/换结构都无效**。若用户点名 analyst，应直接引本条做「死路出处」。

### 2026-10-12 再续：★ **「天花板 1.1」被推翻 —— `analyst4` 修正幅度 S 1.38**

**`analyst4`（300 字段巨型一致预期集）** 的 **分析师修正幅度**（当前 vs 上次估计，字段 cov **1.0**）：

```
REV = divide(subtract(vec_avg(anl4_fs_detail_estimate_af_v4_nd_estimate),
                      vec_avg(anl4_fs_detail_estimate_af_v4_nd_previosestimate)),
             add(abs(vec_avg(anl4_fs_detail_estimate_af_v4_nd_previosestimate)), 0.0001))
最佳形态 = quantile(group_rank(ts_backfill(ts_rank(REV, 462), 66), sector))   ⇒ S 1.38 / F 1.01 / TO 0.142 / 2Y 0.79
```
- **S 1.38 是 analyst 族历史最高**（此前天花板 1.12）⇒ **上文「类别级上限 ≈1.1」应修正为「已探结构上限 ≈1.1，`analyst4` 修正幅度可达 1.38」**。
- 同集其它：`EP4`(eps_mean/close) 2Y **1.41**、`DISP4`(eps_std/|eps_mean|) 2Y **1.40**、`DP4` 2Y 1.15 —— **2Y 普遍 1.1–1.4**。
- **多窗乘积 `REV_mw` 依旧反向（−0.46）**，与 analyst9 一致 —— 该结构在 analyst 族**系统性无效**。

**`analyst48`（股息预测集）= 天然高 2Y 的「防御轴」**（与 PV 的 `ts_kurtosis` 同角色但来源不同）：

| 字段 | S | **2Y** |
|---|---|---|
| `vec_avg(anl48_bbpsa)`（每股股息）| 0.44 | **1.84** |
| `vec_avg(anl48_bp3y_dg)`（3 年股息增速）| 0.20 | **1.64** |
| `vec_avg(anl48_bdvd_curr_dvd_health)`（股息健康度）| 0.24 | **1.55** |
| `bp12m_yld` / `equity_m21_dly_dvd_yqe` / `edg3yr_g` | 0.30–0.39 | 1.20–1.47 |

⇒ **S 与 2Y 反向**再次出现：`analyst4`(S 1.38/2Y 0.79) vs `analyst48`(S 0.44/2Y 1.84)。
⇒ **组合思路**：`analyst4` 修正幅度做主腿、`analyst48` 股息做 2Y 腿（须走条件/分组/残差形式）。

**未探（3 个）**：`analyst45`(241/cov 0.253)、`analyst25`(207/0.5)、`analyst15`(304/0.526)；`analyst81` 批失败待补。

### 跨族可迁移杠杆（本会话在 PV 塔实证，analyst 可参考；⚠ 效应族相关，禁外推）

- **`ts_kurtosis`（峰度）是 2Y 钥匙**：0 塔信号族 2Y 天花板 **1.15 → 1.59（+38%）**。
  形态 `multiply(rank(-ts_kurtosis(X,160)), rank(-ts_rank(X,132)), rank(-ts_rank(X,252)))`（同字段多窗 ⇒ 合规）。
  **仅对「日频收益/价量分布型」字段有效**（情绪/事件/结构类 4 个数据集全部失效）。
- **`MARKET` 是 KOR 唯一「F 与 2Y 兼顾」的中性化档**（同族：STATISTICAL F0.85/2Y1.51；INDUSTRY 1.10/1.20；SECTOR 1.09/1.50；**MARKET 1.03/1.59**）。
- **`LOW_INVESTABILITY_CONSTRAINED_SHARPE` 限 = 0.70×S** ⇒ 需保留率 ≥70%；**提 S 无用**（限同步抬）。
  KOR D1 **只有 `TOP600`**（`get_platform_setting_options` 实测）⇒ 无更偏大盘档位可换。
- **KOR 不可用算子**：`ts_ir`、`ts_target_tvr_hump`（整批连坐 FAIL 且**无报错**）；`ts_target_tvr_decay` 可用但压 TO 时**等比例杀 S**。
- **发批前三闸**：`ensure_safe_for_dispatch`（元数违规整批连坐）+ 新算子 2 条小批验存在性 + 字段 `get_datafields` 实名核对。
- **僵尸批次判据修正**：`children=0` 且 `progress` 非空（0.35/0.9）**只是慢，不是僵尸**——实测卡 0.35 约 25 分钟后自行 COMPLETE。
  按旧判据曾误删一个已到 0.9 的批次。multi-sim location 约 **24h 过期 ⇒ 当天收割**。
<!-- profiles:manual:end -->
