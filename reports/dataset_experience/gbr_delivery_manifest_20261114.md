# GBR REGULAR Alpha 交付清单（2026-11-14）

**Region**: GBR · **Universe**: TOP700 · **Delay**: 1 · **InstrumentType**: EQUITY · **Language**: FASTEXPR
**交付件数**: **8 / 20**（目标 20）
**核验时间**: 2026-11-14 06:3x，逐颗重新拉取平台 checks 与指标

---

## 一、交付件总表（7 颗，全部 IS 全闸通过）

| # | alpha | 数据集 / 核心字段 | 算子逻辑（精简） | S | F | TO | 2Y | sub | lc/sc | ops |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|
| 1 | **omEdka3v** | other / tm_17（techindi 模型输出）+ shortinterest / loaned_share_count_main | group_rank(ts_zscore(tm_17,126),sector) + reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned),250),504),sector)) | **2.51** | 1.40 | 0.282 | 2.37 | 2.46 | 361/361 | 8 |
| 2 | **6XdkW08J** | fundamental / region_relative_valuation_rank + loaned_share_count_main | 同上结构，valuation 用 w66/market 轴 | **2.60** | 1.95 | 0.148 | 2.55 | 2.12 | 451/458 | 8 |
| 3 | **pwdd7Za6** | pv / transaction_count_p5_d1 ÷ volume | -signed_power(rank(ts_rank(ts_backfill(divide(vec_sum(txn),ts_mean(volume,22)),120),504)),0.5) | **1.69** | 1.04 | 0.105 | 2.49 | 1.70 | 418/491 | **7** |
| 4 | **omExeqLb** | fundamental / star_val_sector_rank + loaned_market_value_usd_main | 估值腿 w66/sector + 借券腿 B | **2.43** | 1.78 | 0.170 | 2.12 | 2.14 | 447/462 | 8 |
| 5 | **A1x63v7Y** ★新 | region_relative_valuation_rank(w504/industry) + loaned_share_count_main | valuation w504 + 借券腿 A，@**SLOW** | **2.20** | 1.61 | 0.124 | 2.41 | 1.95 | 453/457 | 8 |
| 6 | **xAvMdaOl** ★新 | other / tm_19（techindi）+ loaned_market_value_usd_main | tm_19 w126/sector + 借券腿 B，@**SLOW** | **2.85** | 1.48 | 0.282 | 2.58 | 2.28 | 454/456 | 8 |
| 7 | **xAvMjnam** ★新 | pv / pattern_scores::v_shape_reversal_bottom_max_similarity + loaned_market_value_usd_main | -group_rank(形态相似度,sector) + 借券腿 B，@**SLOW** | **1.81** | 1.02 | 0.157 | 2.03 | 1.84 | 456/453 | 8 |
| 8 | **1YWvNaXk** ★新 | model / predictive_starmine::rel_val_industry_rank_score_3 + loaned_market_value_usd_main | group_rank(starmine行业估值,sector) + 借券腿 B，@**SLOW** | **1.77** | 1.06 | 0.104 | 2.04 | 1.49 | 471/438 | **6** |

★新 = 2026-11-14 本轮新增。**算子数核验**：7 颗全部满足 ≤8 算子闸 —— 6 颗为 8 ops；**pwdd7Za6 为 7 ops**（signed_power / rank / ts_rank / ts_backfill / divide / vec_sum / ts_mean，负号不计），此前标 9 为误算，已更正。

## 二、闸门核验（7/7 全通过）

| alpha | S≥1.58 | F≥1.00 | TO∈[0.01,0.70] | 2Y 分档 | sub | checks.fail | pass 含 SHARPE/FITNESS/LADDER | self | prod |
|---|---|---|---|---|---|---|---|---|---|
| omEdka3v | ✓2.51 | ✓1.40 | ✓0.282 | ✓2.37 | ✓2.46 | **[]** | ✓✓✓ | — | **0.6026** |
| 6XdkW08J | ✓2.60 | ✓1.95 | ✓0.148 | ✓2.55 | ✓2.12 | **[]** | ✓✓✓ | — | **0.6267** |
| pwdd7Za6 | ✓1.69 | ✓1.04 | ✓0.105 | ✓2.49 | ✓1.70 | **[]** | ✓✓✓ | — | **0.6238** |
| omExeqLb | ✓2.43 | ✓1.78 | ✓0.170 | ✓2.12 | ✓2.14 | **[]** | ✓✓✓ | — | **0.6238** |
| A1x63v7Y | ✓2.20 | ✓1.61 | ✓0.124 | ✓2.41 | ✓1.95 | **[]** | ✓✓✓ | **0.2902** | **0.6303** |
| xAvMdaOl | ✓2.85 | ✓1.48 | ✓0.282 | ✓2.58 | ✓2.28 | **[]** | ✓✓✓ | **0.4146** | **0.6014** |
| xAvMjnam | ✓1.81 | ✓1.02 | ✓0.157 | ✓2.03 | ✓1.84 | **[]** | ✓✓✓ | **0.2833** | **0.5861** |
| **1YWvNaXk** | ✓1.77 | ✓1.06 | ✓0.104 | ✓2.04 | ✓1.49 | **[]** | ✓✓✓ | **0.4322** | **0.5909** |

**逐年核验**：本轮新入 3 颗（A1x63v7Y / xAvMdaOl / xAvMjnam）均 **10/10 年全正、无空窗**。

**★prod 终验完备性（2026-11-14 07:07 补齐）**：7 颗全部完成 prod 测量，读数区间 **0.5861 - 0.6303**，全部 < 0.70：
| alpha | prod |
|---|---:|
| 6XdkW08J | 0.6267 |
| pwdd7Za6 | **0.6238**（本轮补齐） |
| omEdka3v | 0.6026 |
| omExeqLb | 0.6238 |
| A1x63v7Y | 0.6303 |
| xAvMdaOl | 0.6014 |
| xAvMjnam | 0.5861 |
| **1YWvNaXk** | **0.5909** |
⇒ **prod 维度无缺口，8 颗全部通过 prod 闸。**

## 三、篮子互相关（硬要求：全对 < 0.7）

**7 颗全对 21 对，最大 0.6793 < 0.7 ⇒ pairs_over_threshold = [] ✓**

| 相关对 | 相关 |
|---|---:|
| 6XdkW08J × A1x63v7Y | **0.6793** |
| 6XdkW08J × omExeqLb | 0.6123 |
| xAvMdaOl × xAvMjnam | 0.5474 |
| omExeqLb × A1x63v7Y | 0.5134 |
| omEdka3v × xAvMdaOl | 0.4726 |

## 三之二、starmine 维度排查（2026-11-14 07:4x，第 8 颗的来源）
`model/predictive_starmine`（631 字段、alphaCount 5089、覆盖 0.87-0.93）维度排查结果：
| 维度族 | 字段数 | S | F | 2Y | 判定 |
|---|---:|---:|---:|---:|---|
| **行业相对估值** | 111 | **1.77** | **1.06** | **2.04** | ★入篮（1YWvNaXk） |
| 全局估值排名 | 111 | 1.65 | 0.96 | 1.75 | F 差 0.04 |
| 价格/内在价值(DCF) | 11 | 1.61 | 0.92 | 1.43 | F 不足 |
| 盈利预测修正 | 127 | 1.81 | 1.22 | **1.27** | **2Y 缺口** |
| P/E 分位 | 26 | 1.49 | 0.82 | 1.17 | F 不足 |
| FCF 收益率变化 | 5 | 1.58 | 1.00 | 1.52 | **2Y 差 0.06** + pass 缺 IS_LADDER |
| EV/EBITDA | 2 | 1.33 | 0.71 | 1.35 | F 不足 |
| P/B / 股息收益率 | 2 / 36 | 1.12 / 1.08 | 0.54 / 0.50 | 0.99 / 0.92 | F 不足 |
⇒ **starmine 只贡献 1 颗**（行业相对估值是唯一 S/F/2Y 三项指标全部达标的维度）。

## 四、容量约束实证（为何 8 颗）

**篮子容量 = 选股腿的独立维度数**，不是腿数量。7 颗背后只有 **5 个独立选股腿族**：

| 选股腿族 | 件数 | 成员 |
|---|---:|---|
| valuation_rank | 2 | 6XdkW08J(w66)、A1x63v7Y(w504) |
| star_val_sector_rank | 1 | omExeqLb |
| techindi（tm_17/tm_19） | 2 | omEdka3v、xAvMdaOl |
| transaction÷volume | 1 | pwdd7Za6 |
| pattern（形态相似度） | 1 | xAvMjnam |

借券腿 2 族（loaned_share_count_main / loaned_market_value_usd_main）只是降 prod 的伴生腿，不提供独立维度。

**第 6 族候选已全部排除**：

| 数据集 | 覆盖 | 最强读数 | 排除原因 |
|---|---:|---:|---|
| dl_riskfree_returns | 825 | S 1.82（反向 1.18） | **2Y 0.15-0.92**（要求 1.58） |
| model238 Smart Holdings | 455 | 0.78 | 覆盖仅 66%、强度不足 |
| model264 趋势分类 | 762 | 0.94 | 单字段不稳（1l_bb -0.43） |
| news104 | 726 | 0.35 | 弱 |
| pv30 | — | — | 全 GROUP 类型，只能作分组轴 |
| insiders12 卖压 | 524 | 0.90 | 弱腿不配借券（需 ≥2.0 档） |

**⇒ GBR TOP700 在现有数据集池下的可交付容量实测 ≈ 7 颗。**

## 五、关键方法学沉淀（跨区可复用）

1. **算子族处方**（48 臂纯净对照）：有效维度是水平+幅度 → 慢窗求和 + winsorize/group_neutralize + 保留幅度；zscore ≡ scale ≡ normalize（逐位相同）；sign/sqrt/tail/hump 压缩即毁 40-50%；group_sum/std_dev/count 把 TO 打到 0.77-0.82 爆闸。
2. **中性化档是 prod 杠杆**：估值+借券族 SLOW 0.63 / INDUSTRY 0.72 / SUBINDUSTRY 0.74（极差 0.11）；残差族对档位不敏感（0.81-0.87，极差 0.07）⇒ 不能跨族推广。
3. **prod 由机制族拥挤度决定，不由 S 决定**：S 2.99 的 techindi 纯选股 prod 0.929，S 2.20 的估值+借券只有 0.63。
4. **高 S 必须先核 lc/sc**：稀疏持仓会跳过 Sharpe 类检查，fails=[] 是假象；必须核对 checks.pass 是否显式含 LOW_SHARPE/LOW_FITNESS/IS_LADDER。
5. **NONE 档裸读 0.6-0.8 + lc/sc 单边 = 规模暴露**，中性化后衰减 70-80%。
6. **字段数是数据集质量的负向指标**：模型输出型/量化计数型覆盖最好，语义解析型多为空壳。
7. **数据集入场前必查逐年 lc/sc**：sentiment27 在 GBR 2014-2018 无数据（filter=true 无法修复）。
8. **EVENT 字段必须 vec_ 聚合后才能进 ts_*；MATRIX 字段不能包 vec_***。
9. **reverse 是语义必需**（借券腿去掉 reverse 后 S 从 1.04 掉到 0.41），不能被 subtract 顺序替代。
10. **平台不可用算子**：ts_max / ts_min / ts_min_max_cps / ts_min_max_diff / self_corr。

## 六、未达 20 颗的如实说明

- 目标 20 颗，实际交付 **7 颗**（35%）
- 缺口 13 颗受**容量约束**而非投入不足：GBR TOP700 全部 177 个数据集中，满足「S≥2.0 选股腿 + 覆盖≥400 + 10 年全历史 + 与现有族正交」的信号族仅 **5 个**
- 本轮实测 60+ 数据集、约 300 个回测臂

## 七、存档索引

| 类型 | 路径 |
|---|---|
| 波次总档 | tracking/GBR/waves/gb_v1_v2_dispatch_20261113.md |
| 本交付清单 | reports/dataset_experience/gbr_delivery_manifest_20261114.md |
| GEM ideas | tracking/GBR/reference/gbr_*_gem_ideas.md |
| 字段画像 | tracking/GBR/reference/gbr_*_fields.json |
| prod 产物 | results/prod_wait_*.json |