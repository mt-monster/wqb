# GBR 数据集 + 字段画像 · 完整分析总结

> 区域：**GBR / EQUITY / D1 / TOP700**　｜　快照：**2026-10-08**
> 本文是 GBR 画像的**总纲**（独立可读）。细则见：
> - `GBR_field_profile_full_20261008.md`（verdict 层全表）
> - `GBR_field_semantic_profile_20261008.md`（语义层 + 全语义扫测 + 7 轮自审）
> - `GBR_10alpha_campaign_20261008.md`（战役执行与候选）
> 工具：`tools/fields/field_profile.py`（判**强不强**）＋ `tools/fields/field_semantic_type.py`（判**是什么量**）

---

## 一、一页速览

```
数据集：205 个（其中 177 个有字段目录，28 个本区不存在）
字段：15,522 个（平台可用数据集 100% 覆盖，缺口 = 0）
已测字段：285 个 ｜ 累计测试 ≈ 1,700+ 次
测试转化率：15,522 → 285 = 1.8%

【verdict 层】ALIVE 49 ｜ WEAK 34 ｜ DEAD 465 ｜ UNTESTED 2,578 ｜ USABLE 池 = 83
【语义层】19 类量型 ｜ 名字与 description 语义冲突 = 1,470（9.5%）
【关键结论】本区能出东西的量类型收敛为 ratio / percentile（有序号语义类中排前二）
【关键结论】非 MODEL 的 ALIVE 仅 20 个；MODEL 占 29 个但塔已点亮（锁定项）
【关键结论】非 MODEL 未测池 2,578 个：抽样扫测 62 条证明整体无信号（17 类全 ≤0.92）
```

---

## 二、方法：两层画像

| 层 | 工具 | 数据源 | 回答的问题 |
|---|---|---|---|
| **强度层** | `field_profile.py` → 表 `field_profile_perf` | `fields` LEFT JOIN `backtest_results` | 这个字段**测出来强不强**（verdict） |
| **语义层** | `field_semantic_type.py` → 表 `field_semantic_type` | `fields.description` | 这个字段**是什么量**（sem_type + 骨架建议） |

**为什么必须两层**：骨架选择完全取决于「是什么量」。强度层的 9 类 verdict 中**只有 `DEAD_COUNT` 是名字驱动**的，
其余都是 S/turnover 驱动。而名字会骗人 —— 全库 **9.5%** 的字段名与其 description 语义冲突。

---

## 三、字段画像 · 总量与分布

### 3.1 verdict 分布（强度层）

| verdict | 判据 | 字段数 | 占比 |
|---|---|---:|---:|
| `UNUSABLE` | coverage < 0.6 | 10,967 | 70.7% |
| `UNTESTED` | 过前两关且 n_tests = 0 | 2,578 | 16.6% |
| `AXIS_ONLY` | field_type = GROUP | 1,390 | 9.0% |
| `DEAD` | 已测 S < 1.10 | 464 | 3.0% |
| **`ALIVE`** | 单信号 S ≥ 1.58 | **49** | 0.3% |
| `WEAK` | 1.10 ≤ S < 1.58 | **34** | 0.2% |
| `DEAD_STATIC` / `DEAD_TURNOVER` / `DEAD_COUNT` | to_med<0.03 / >0.70 / 计数型「2Y有S无」 | 28 / 7 / 5 | 0.3% |

### 3.2 语义分布（语义层，19 类）

| sem_type | 字段数 | sem_type | 字段数 |
|---|---:|---|---:|
| `unknown`（须人工读描述） | 3,512 | `sentiment` | 537 |
| `score` | 1,921 | `estimate_level` | 467 |
| `count` | 1,813 | `dispersion` | 416 |
| `ratio` | 1,681 | `cluster_label`（只作轴） | 322 |
| `level_amount` | 1,346 | `identifier`（禁用） | 255 |
| `percentile` | 1,002 | `temporal_meta`（禁用） | 148 |
| `probability` | 893 | `indicator_name` | 119 |
| `revision_change` | 844 | `correlation` | 111 |
| | | `direction` 69 ｜ `novelty_time` 37 ｜ `text` 29 | |

### 3.3 字段类型分布

| field_type | 数量 | 占比 | 处置 |
|---|---:|---:|---|
| MATRIX | 9,160 | 59.0% | 可直接套 `ts_*` |
| **VECTOR** | **4,782** | **30.8%** | **必须先 `vec_*` 聚合（7 种：avg/sum/min/max/stddev/range/count）** |
| GROUP | 1,470 | 9.5% | 只作分组轴 |
| SYMBOL | 110 | 0.7% | 非数值 |

---

## 四、数据集级画像（按活/弱字段数降序）

| dataset | category | 字段 | **ALIVE** | WEAK | UNTESTED | DEAD | UNUSABLE | AXIS | 数据集 aCnt |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **analyst7** | ANALYST | 502 | **11** | 11 | 296 | 56 | 128 | 0 | 5,823 |
| **predictive_starmine** | MODEL | 631 | **10** | 3 | 419 | 34 | 165 | 0 | 1,589 |
| **model38** | MODEL | 71 | **9** | 0 | 0 | 5 | 57 | 0 | **10,407** |
| model28 | MODEL | 25 | 3 | 5 | 4 | 9 | 4 | 0 | 3 |
| analyst_earnings_ibes | MODEL | 42 | 3 | 3 | 26 | 10 | 0 | 0 | 475 |
| analyst47 | ANALYST | 5 | **3** | 1 | 0 | 1 | 0 | 0 | 3 |
| analyst_factor_signals | ANALYST | 96 | 2 | 1 | 17 | 12 | 64 | 0 | 870 |
| **pv47** | PV | 2 | **2** | 0 | 0 | 0 | 0 | 0 | 7 |
| fund_holdings_panel | INSTITUTIONS | 18 | 0 | 2 | 2 | 14 | 0 | 0 | 0 |
| model53 | MODEL | 22 | 1 | 3 | 7 | 11 | 0 | 0 | 0 |
| model109 | MODEL | 542 | 1 | 0 | 0 | 27 | 514 | 0 | 304 |
| pattern_scores | PV | 504 | 1 | 0 | **471** | 32 | 0 | 0 | 480 |
| model264 | MODEL | 380 | 1 | 0 | 359 | 20 | 0 | 0 | 174 |
| model25 | MODEL | 97 | 1 | 0 | 75 | 9 | 12 | 0 | 6,097 |
| analyst9 | ANALYST | 51 | 1 | 0 | 44 | 6 | 0 | 0 | 0 |
| dl_riskfree_returns | OTHER | 133 | 0 | 1 | 43 | 13 | 76 | 0 | 344 |
| news18 | NEWS | 70 | 0 | 1 | 56 | 13 | 0 | 0 | 5 |
| model250 | MODEL | 20 | 0 | 1 | 4 | 5 | 10 | 0 | 94 |
| sentiment27 | SENTIMENT | 18 | 0 | 1 | 5 | 12 | 0 | 0 | 295 |
| other335 | OTHER | 10 | 0 | 1 | 0 | 4 | 5 | 0 | 72 |
| other455 | OTHER | 1,500 | 0 | 0 | 300 | 0 | 0 | **1,200** | 88 |
| analyst_revision_horizons | MODEL | 855 | 0 | 0 | 0 | 8 | 847 | 0 | 1,244 |
| multifactor_return_pred | MODEL | 648 | 0 | 0 | 0 | 0 | 648 | 0 | 83 |
| intraday_pv_feats | PV | 585 | 0 | 0 | 0 | 17 | 568 | 0 | 175 |
| fundamental72 | FUNDAMENTAL | 552 | 0 | 0 | 0 | 25 | 527 | 0 | 132 |

**关键读数**：
1. **产出高度集中**：前 8 个数据集贡献了 **43/49 的 ALIVE（88%）**。
2. **`model38` 的 aCnt = 10,407**（全平台被用过 1 万+ 次）—— **极度拥挤**，其 9 个 ALIVE 无实际价值。
3. **`analyst7` 是本区最有价值的数据集**（11 ALIVE + 11 WEAK + 296 未测，aCnt 5,823 亦很高 ⇒ 拥挤）。
4. **`pv47` 只有 2 个字段，却 2 个全 ALIVE** —— 效率最高，但已挖尽（无未测）。
5. **大量数据集"字段多但全不可用"**：`other455` 1,500 字段中 1,200 是 GROUP（轴）、300 未测；
   `analyst_revision_horizons` 855 中 847 不可用。

---

## 五、category 级画像（16 类）

| category | 字段 | **ALIVE** | WEAK | UNTESTED | 主语义 | ALIVE 的语义 | 未测池主语义 |
|---|---:|---:|---:|---:|---|---|---|
| **MODEL** | 5,335 | **29** | 15 | 1,087 | ratio 1105 / pctile 758 / count 629 | **ratio 17, pctile 7** | count 264 / ratio 237 / prob 227 |
| **ANALYST** | 2,239 | **17** | 13 | 387 | count 591 / est_level 338 | **count 10**, est_level 3 | **count 202 / est_level 111** |
| **PV** | 2,165 | 3 | 0 | 511 | score 675 / unknown 519 | score 1 / ratio 1 | score 329 / dispersion 71 |
| OTHER | 3,515 | 0 | 2 | 350 | **unknown 1375** / prob 417 | — | score 145 / level 108 |
| FUNDAMENTAL | 1,238 | 0 | 0 | 40 | **unknown 587** / level 209 | — | unknown 36 |
| NEWS | 491 | 0 | 1 | 180 | unknown 100 / sentiment 83 | — | temporal 43 / sentiment 43 |
| SENTIMENT | 276 | 0 | 1 | 5 | **count 134** / sentiment 60 | — | — |
| INSTITUTIONS | 66 | 0 | 2 | 3 | **count 35** / level 12 | — | — |
| INSIDERS | 50 | 0 | 0 | 0 | level 24 / unknown 19 | — | — |
| RISK / SHORTINTEREST / EARNINGS / OPTION / SOCIALMEDIA / MACRO / IMBALANCE | 40/25/25/22/20/13/2 | 0 | 0 | 3/12/0/0/0/0/0 | — | — | — |

**关键读数**：
1. **ALIVE 的 59%（29/49）在 MODEL** —— 而 MODEL 塔已点亮，受「已点亮塔不作主数据集」锁定。
2. **非 MODEL 的 ALIVE 只有 20 个**（ANALYST 17 + PV 3）。
3. **`unknown`（领域专有复合量）集中在 OTHER(1,375) / FUNDAMENTAL(587) / PV(519)** —— 这些类**必须先解决「读描述定骨架」才能开波**，这也解释了它们长期做不出东西的原因。

---

## 六、ALIVE / WEAK 全表（description 确认语义）

### 6.1 ALIVE 49 个（按 S 降序，节选非 MODEL 全部 + MODEL 代表）

| category | dataset.field | sem_type | S | 2Y | F | 备注 |
|---|---|---|---:|---:|---:|---|
| MODEL | model38.star_val_region_rank | percentile | **2.61** | 2.06 | 2.31 | aCnt 10,407 极拥挤 |
| MODEL | analyst_earnings_ibes.five_day_total_return_dlr2 | ratio | 2.07 | 2.31 | 1.87 | n=95 最密 |
| MODEL | predictive_starmine.ep_yield_pct_smest_fy2_3 | ratio | 2.02 | 1.62 | 1.31 | |
| **ANALYST** | **analyst47.anl47_rawsentiment** | ratio | **1.96** | 1.84 | **0.97** | **F 卡闸** |
| **ANALYST** | **analyst7.est_12m_pre_raisednum_4wks** | count | **1.96** | 2.05 | 1.31 | **已提交腿** |
| **ANALYST** | **analyst7.est_12m_pre_low** | level_amount | **1.90** | **2.72** | 1.38 | **已提交腿** |
| **ANALYST** | **analyst7.est_12m_pre_raised_1wk** | count | 1.84 | 2.08 | 1.12 | 新腿 |
| **ANALYST** | **analyst7.est_12m_pre_raisednum_1mth** | count | 1.82 | 1.68 | 1.15 | 新腿 |
| **ANALYST** | analyst7.est_12m_net_raisednum_4wks | count | 1.80 | 1.18 | 1.12 | 2Y 弱 |
| **ANALYST** | analyst47.anl47_indicator | ratio | 1.78 | 1.53 | 0.76 | F/2Y 双卡 |
| **PV** | **pv47.pv47_spret** | ratio | **1.77** | **2.25** | 1.06 | **战役主力** |
| **ANALYST** | analyst47.anl47_totalrawsignal | level_amount | 1.75 | 2.02 | 0.79 | F 卡 |
| **PV** | pv47.pv47_for_statssimple_only_spret | ratio | 1.73 | 2.12 | 1.12 | 已挖尽 |
| **ANALYST** | analyst9.anl9_s_numup | count | 1.69 | 1.19 | 1.19 | 2Y 卡 |
| **ANALYST** | **analyst7.est_12m_pre_mean** | estimate_level | 1.66 | **2.15** | 1.20 | 新腿 |
| **ANALYST** | analyst_factor_signals.revenue_y1_estimate_change_3mo | revision_change | 1.62 | **0.76** | 1.02 | 2Y 卡 |
| **ANALYST** | analyst_factor_signals.revenue_revision_magnitude | ratio | 1.61 | **0.99** | 1.01 | 2Y 卡 |
| **PV** | pattern_scores.breakaway_gap_up_mean_simscore_lookback60 | score | 1.61 | 1.64 | 1.13 | |
| **ANALYST** | analyst7.est_12m_net_low | level_amount | 1.59 | 1.84 | 1.06 | |

### 6.2 WEAK 34 个（节选非 MODEL 全部）

| dataset.field | sem_type | S | 2Y | 备注 |
|---|---|---:|---:|---|
| analyst7.est_12m_sal_raisednum_4wks | count | 1.54 | 0.82 | 2Y 弱 |
| analyst7.est_12m_pre_median | estimate_level | 1.45 | **2.03** | **2Y 健康，S 差 0.13 ⇒ 值得 1 波** |
| analyst7.est_12m_gps_raisednum_4wks | count | 1.40 | 1.01 | |
| analyst47.anl47_rawalphadecay | ratio | 1.39 | 0.17 | 2Y 死 |
| analyst7.est_12m_ebt_mean | estimate_level | 1.38 | 1.34 | |
| analyst7.est_12m_dps_low / ebt_raisednum_4wks / ebi_low / ebt_low / gps_low / cps_low | 各异 | 1.14–1.35 | 0.44–1.77 | 多数 2Y 弱 |
| analyst7.rec_raisednum_4wks | count | 1.16 | 0.70 | |
| analyst_factor_signals.netprofit_y2_estimate_change_3mo | revision_change | 1.27 | 1.18 | |
| **fund_holdings_panel.boundary_transaction_total** | count | 1.26 | 1.38 | F 仅 0.32 |
| **fund_holdings_panel.stable_boundary_trade_count_21d** | count | 1.24 | 1.49 | TO 0.54 |
| other335.oth335_combined_all_region_mind | score | 1.13 | 0.96 | |
| **sentiment27.snl27_totaldomains** | count | 1.12 | **2.00** | 2Y 健康、F 0.62 |
| **news18.nws18_multiple_comp_ssc** | count | 1.10 | **1.65** | 2Y 健康、F 0.49 |

---

## 七、未测池（2,578）与**语义抽样扫测**结论

### 7.1 未测池分布（非 MODEL 1,491）

| dataset | 未测数 | | dataset | 未测数 |
|---|---:|---|---|---:|
| pattern_scores | 471 | | news18/17/20/50 | 56/45/39/32 |
| other455 | 300 | | analyst9 | 44 |
| **analyst7** | **296** | | dl_riskfree_returns | 43 |
| | | | pv29 | 40（实为 GROUP 标签） |

### 7.2 ★★ 抽样扫测（62 条 / 8 波 / 17 类，每类配**匹配骨架**）

| 判读 | sem_type（中位 S） |
|---|---|
| **有效语义（有序号语义）** | **`ratio` 0.50 > `percentile` 0.23 > `revision_change` 0.11 > `estimate_level` 0.10 > `count` 0.08 > `sentiment` 0.05** |
| **spurious（无序号语义 ⇒ 分数无意义）** | `identifier` 0.65 ｜ `text` 0.45 ｜ `cluster_label` 0.30 ｜ `temporal_meta` 0.06 |
| **反效** | `dispersion` −0.41 ｜ `probability` −0.51 ｜ `level_amount` −0.59 |

**62 条中 S≥1.58 = 0 个；|S|≥1.0 = 2 个（均负）。**

**⇒ 用 8 波（而非盲挖的 ≈322 波）证明：GBR 非 MODEL 未测池整体无信号。**

---

## 八、名字会骗人：names ≠ description（1,470 个 = 9.5%）

| 字段名 | description 实为 | 危害 |
|---|---|---|
| `short_term_price_change` | **Williams %R** | 按名字选骨架必错 |
| `cumulative_money_flow_volume_adjusted` | **Relative Strength (RSI)** | 同上 |
| `liquidity_money_flow_alignment` | **Relative Turnover (RTN63D)** | 同上 |
| `mdl28_..._pd_pct`（像 ratio） | **probability of default** | 骨架错配 |
| `..._prob_..._quantile_...`（像 percentile） | **Log-probability** | 骨架错配 |
| `est_12m_gps_raisednum_4wks`（像 count） | 描述 "Number of ... **per share**" ⇒ 主量仍是 **count** | **规则顺序 bug 的受害者** |
| `smest_price_ratio_*`（8 个，含 4 ALIVE） | "**price-to**-revenue **ratio**" ⇒ 主量词在**词尾** | **复合名词 bug 的受害者** |

**⇒ 纪律：类型/机制归类必须读 `description`；名字只是线索。关键词出现 ≠ 语义成立。**

---

## 九、GBR 出口封死：六类形态（每类均有实测证据）

| 形态 | 判据 | GBR 实例 | 实测证据 |
|---|---|---|---|
| **A prod 墙** | IS 全过、**prod > 0.70** | `analyst7` 家数族、`pv47` 反转族 | **15 颗 IS 全闸候选全部 prod 0.756–0.856** |
| **B 2Y 塌** | IS 强、2Y ≪ 1.58 | `analyst_factor_signals`、`analyst9` | 换骨架 / `ts_decay_linear` / 压 TO 均无效（2Y 反降） |
| **C 低于闸线** | S/F 不足 | `analyst47`（F 0.96–0.97） | `ts_decay_linear`/`hump`/`ts_mean`/`ts_target_tvr_decay`/幂次/裁剪 **全部无法破线** |
| **D「2Y 稳、S 弱」** | 2Y ≥ 1.58、S ≤ 1.0 | `nws18_bee`(2Y1.83)、`nws20_ber`(2Y1.75)、`oth47_organic_traffic`(2Y1.61)、`aggregate_equity_value_all_owners`(2Y1.74) | 换骨架后仍 ≤ 0.88 |
| **E 同 sem_type 反向** | 同量型同骨架、方向翻转 | `ent`（企业价值）vs `pre`（税前利润）净修正家数 | `ent` 8/8 同向为负（−0.95~−1.03） |
| **F 未测池无信号** | 抽样扫测全不过 | 62 条覆盖 17 类 | S 全 ≤0.92，0 个过闸 |

**附加约束**：**GBR 只有 TOP700 一个 universe**（TOP500/2000/3000 均被平台拒）⇒
**「换 universe = 换持仓 = 降 prod」这条 playbook 杠杆在本区不存在。**

---

## 十、方法学沉淀（7 轮自审 + 3 条硬纪律）

### 10.1 七轮自我审查（每轮都改了代码或结论）

| # | 发现 | 影响面 | 处置 |
|---|---|---|---|
| #0 | `DEAD_COUNT` 是**名字驱动**；`count` 无词边界误匹配 `country`/`accounts`；`*_surprisenum` 语义实为「参与家数」 | 判级错误 | 改 description 驱动（DEAD_COUNT 4→5） |
| **#0b** | **我自己第一版修错**：只加 `\bcount\b` ⇒ `count_50bps`/`_numup` 失配，**4→0 是假象** | 差点留下更差版本 | 复核时发现并改对 |
| #1 | 固定规则优先级 ≠ 语义主次（"**Number of** … per share"） | **~1,000 字段重归类** | 改「取描述中最靠前主量词」 |
| #2 | earliest-match 对**复合名词**失效（"price-to-revenue **ratio**"） | 8 个字段（含 4 ALIVE）误判 | 新增复合表述优先层 |
| #3 | `expected` 过泛（"Expected annualized **percent change**"） | 语义错判 | 收紧正则 |
| #4/#5 | `unknown` 3,601 **全部有描述** ⇒ 规则缺口；暴露 `indicator_name`/`direction` 两类 | 覆盖率 | 新增两类规则 |
| #6/#7 | **两次 selection bias**：被 `score` 的**未测数量**误导；被 `count` 的**已测命中率**误导 | **两条错误建议** | 见 §10.2 硬纪律 |

### 10.2 三条硬纪律（已写入 skill `_field-profile-playbook.md`）

> **① 类型/机制归类必须读 `description`，名字只是线索。**（关键词出现 ≠ 语义成立；反向也要查）
>
> **② 已测字段的命中率不得用于预测未测字段** —— 已测集合是**被优选过的样本**（selection bias）。
> 估计未测池产出率的唯一可靠做法 = **直接测未测字段（配匹配骨架）**。
>
> **③ 判「区域无信号」前先验证数据链路完整性。**（本区曾因 `harvest --persist` 漏写 `backtest_results`，
> 使画像把 ALIVE 少报 30 个：19 vs 49。）

### 10.3 新增能力（可跨区复用）

| 能力 | 载体 | 用途 |
|---|---|---|
| 强度层画像 | `tools/fields/field_profile.py` | verdict 九类 |
| **语义层画像** | `tools/fields/field_semantic_type.py`（新） | 19 类量型 + 骨架建议 + 名字冲突检测 |
| **语义抽样扫测** | `semtype_scan.py`（新，仓库外） | **新区域第 0 步**：8 波探明语义产出率 |
| 发批六闸 | `wqb_tools.py dispatch` | 值型/元数/算子实集合/字段存在性/VECTOR/探针位 |

---

## 十一、行动建议

### 11.1 本区（GBR）
**结论：在「不跨区 + 不放开 MODEL」约束下，可提交产出上限 = 0。**
- 15 颗 IS 全闸候选（ANALYST 6 + PV 10）**全部被 prod 挡**；
- 六类出口（A–F）**逐类实测封死**；
- 唯一未试的是 **WEAK 里 `est_12m_pre_median`（S1.45 / 2Y2.03）** 与 D 类形态的换量纲复访 —— 期望低。

### 11.2 可选动作（按 EV 排序）
| 优先 | 动作 | 依据 |
|---|---|---|
| **1** | **把这套方法迁到下一个区** | `ratio`/`percentile` 命中率在别区更高，且无本方腿占据 |
| 2 | 放开 MODEL（**48 颗同类全闸 alpha 待提交**） | 需你裁决：本区 MODEL 塔已点亮 |
| 3 | GBR 的 WORK 池：`analyst7.est_12m_pre_median`（2Y2.03）+ D 类换量纲 | 期望低（≤1 颗） |

### 11.3 方法论迁移清单（新区域开打顺序）
1. **第 0 步**：`field_semantic_type.py --build` 建语义层 → `semtype_scan.py gen/run` 花 8 波探明语义产出率；
2. **第 1 步**：只在**有序号语义 + 实测产出率 > 0** 的语义上开波（GBR 实测 = `ratio` / `percentile`）；
3. **第 2 步**：每条腿提交 1 颗后立刻测同腿变体 prod（防「一条腿只产 1 颗」被打破）；
4. **第 3 步**：卡住时按 **A→F 六类形态**定位（改持仓 / 2Y 塌 / F 卡 / 换量纲 / 换指标 / 换区），不要盲调参数。
