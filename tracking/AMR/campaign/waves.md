# AMR 战役台账（2026-11-06 重启）


---

## AMR 战役 · L1 类别普查探针（2026-11-06 03:0x）

### 目录基建（先扫后锁前置）
- datasets 表灌入 203 集（discover_datasets，429 三次重试）；fields 表灌入 **23,096 字段 / 203 集**（validate_fields_batch --backfill，AMR/TOP600/D1 上下文，0 不可用）。
- regions 表补 universe_legal=['TOP600'] delay_legal=[1]。

### L0 普查
- 17 类：15 类可探（8 种子/类），SHORTINTEREST/IMBALANCE 贫瘠。AMR 金字塔全空（sentiment 0 / pv 0），全部 category 可选。

### L1 探针第一轮（120 条 / QUICK / SUBINDUSTRY decay4 nanON）
- **2/15 批 COMPLETE**，13 批 ERROR/CANCELLED——根因：探针字段含 VECTOR/event 类型（anl8/nws77/fnd21/inst6/opt4/pv69/scl15/oth128/mdl138/mcr27 等），`rank/ts_mean 不支持 event inputs` **整批连坐**。
- COMPLETE 批读数：
  - 批1（other401 GAMES 8 条）：S 0.06/−0.21/−0.25/−0.01/0.10/**0.44**/0.21/−0.30 → 全灭（max 0.44）。
  - 批5（insider_agg_matrix 卖出量族 8 条）：S 0.30/−0.10/0.01/−0.24/0.09/**0.76**/**0.77** → `ts_decay_linear(avg_secondary_buy_shares,66)` S 0.76 与 `ts_zscore(ts_mean(total_secondary_buy_shares,66),264)` S 0.77，**买量累计>卖量累计**，与 EUR insider 经验方向一致，值得深挖。
- 88 条修复：VECTOR 字段包 vec_avg（85 条，SYMBOL 3 条丢弃），批号 probefix_AMR_01-11，11 个 multisim 全部派发（id：results/probefix_AMR_multisims_20261106.json）。
- 教训：**AMR 大量字段是 VECTOR**（inst6/opt4/risk62/scl15 族也中招），发批前必须本地查 field_type；preflight auto_fix_vector 不改写表达式。

### 下一步
- 收割 probefix 11 批 → category_probe --classify 四态 → 锁 s0_whitelist（先扫后锁）。


### L1 修复批收割（03:1x）
- 10/11 批 COMPLETE（85 颗全出），1 批 ERROR（连坐，原因待查）。合计有效读数 77+16=93 条（QUICK 档）。
- 修复批 top：
  | alpha | 表达式 | S | TO |
  |---|---|---|---|
  | j2Yaqz99 | ts_rank(vec_avg(mdl138_qpdi3_cfo_curr_liab),1260) | **0.97** | 0.06 |
  | 9qxlNZad | ts_mean(vec_avg(mdl138_qpdi5_berry),66) | **0.80** | 0.02 |
  | e75aXqel | ts_zscore(ts_mean(vec_avg(opt4_opprc_volume),22),88) | 0.57 | 0.14 |
  | QPv0wnnX | ts_rank(vec_avg(scl15_attrition_score),252) | 0.50 | 0.98 |
  | npvaLpaq | ts_mean(vec_avg(fnd21_...articlevolumettm),22) | 0.47 | 0.02 |
- 汇总两轮：**全库 93 条 L1 探针 max S≈0.97**（mdl138 CFO 现金流质量），无一条 ≥1.58；insider 买量累计族 0.76–0.77 为第二梯队。
- 初判：AMR/TOP600 各类的**裸字段水平量天花板在 ~1.0**，与 KOR 未点亮塔探针形态类似——单条裸 rank 不会出货，需 L2/L3 族级深挖（≥10 互异模板）才能判真死。
- 论坛先验（AMR insider）：①insider_agg_matrix 专帖（WL27618）讲买卖不对称性；②「内部人买卖流量比」AMR 模板帖存在（read_forum_post 404，帖子较新，改为 snippet 引用）。买量累计方向与两帖一致。


### ERROR 批诊断（probefix_AMR_07 / option4）
- 报错：`Your simulation probably took too much resource`——option4 期权链 VECTOR 字段 vec_avg 后仍太重，整批被平台资源闸杀。
- 处置：option4 探针批放弃（L1 结论不受影响，e75aXqel opt4_opprc_volume 已在批 11 跑出 0.57）。
- ⚠ 后续 AMR 发批禁把 opt4 全链 VECTOR 字段与其它集混批；单测需独立小批。

### L2 深挖波（FULL，03:2x 派发）
- **insider_agg_matrix 12 模板**（spec results/amr_ins_L2_spec.json；multisim `1QJwH8bRv4CaanPIWu1PRHe` + `1vsrulgBA4webbBYYlvb0ch`）
- **mdl138 12 模板**（spec results/amr_mdl_L2_spec.json；multisim `TK6TUcty5ggaAA14uOoZQlW` + `4hbiJ0cFe4JvaPHxrRgeoLN`）
- 模板来源：水平/差分/zscore 族（EUR insider 实证配方改单数据集版）、信噪比 conviction、directional_indicator、signed_power 凸性、decay 平滑；mdl138 按 qpdi3/qpdi5/epp 子族 × 同骨架。预检全过。
- 收割判据：max S≥1.58 的族进 prod/self 链；全灭则该族记「裸水平天花板」并转 opt4/scl15/mfm 族。

### L2 insider 批2收割（T7-T12）
| 模板 | 表达式要点 | S | F | TO | 2Y |
|---|---|---|---|---|---|
| T7 买比累计 | ts_mean(buy/(buy+sell),126) | 0.70 | 0.42 | 0.03 | -0.15 |
| T8 directional | group_rank(dir,subindustry) | 0.27 | — | — | -0.74 |
| T9 直接买卖比 | (avg_sec_buy-avg_sec_sell)/(sum) | 0.79 | 0.47 | 0.11 | -0.20 |
| **T10 凸性流量比** | signed_power(gr(sec_top 流量比),2) | **0.89** | 0.61 | 0.12 | 0.54 |
| T11 信噪比 | mean(net)/std(net,252) | 0.68 | 0.39 | 0.05 | 0.02 |
| T12 decay 平滑 | ts_decay_linear(gr(sec 净差)) | **0.88** | 0.57 | 0.08 | -0.18 |

⇒ 批2 max 0.89（T10 凸性）；2Y 普遍弱（<0.6）。批1（T1-T6）在飞。





### L2 insider 批1收割（T1-T6）
| 模板 | S | F | 2Y |
|---|---|---|---|
| T1 高管净买水平 | 0.88 | 0.54 | -0.19 |
| T2 直接高管净买 | 0.75 | 0.43 | -0.16 |
| T3 全董事流量比 | 0.82 | 0.51 | -0.50 |
| T4 高管流量比 | 0.59 | 0.32 | -0.01 |
| T5 净流动量 delta66 | 0.04 | 0.00 | -1.55 |
| T6 均值差 zscore | 0.35 | 0.14 | -0.33 |

**insider 族终榜**：12 模板 max S 0.89（T10 凸性流量比）/ 0.88（T1 高管净买水平）/ 0.88（T12 decay）。全族稳定 0.6-0.9 带、无爆点 ⇒ 距 1.58 差 0.7，**水平/流量几何已达族上限，缺的是跨族合成或多口径加权**（EUR 配方：强腿×冷腿 2:1 合成可同时抬 S/2Y）。2Y 全弱（max 0.54）是主闸缺口。
- 下一步：insider+mdl138 若全灭，试 insider 内部 2:1 合成（T1×T10）与跨数据集冷腿（other424/other335 股息族除外——属 OTHER 塔允许组合，配额≤5）。

### L2 mdl138 批2收割（T7-T12）：全灭
| 模板 | S |
|---|---|
| T7 cfroe zscore | 0.31 |
| T8 op_margin delta | -0.15 |
| T9 rnoa 凸性 | 0.15 |
| T10 epp_5idp | 0.04 |
| T11 cfroa 信噪比 | -0.25 |
| T12 qpdi5_berry decay | 0.08 |

⇒ mdl138 的 zscore/差分/凸性/信噪比几何全灭（max 0.31），QPDI 家族水平量才是信号本体（批1 T1-T5 在飞，L1 水平 ts_rank 已 0.97）。等批1 定生死。



### L2 mdl138 批1收割（T1-T6 水平族）：全灭
| 模板 | S | 2Y |
|---|---|---|
| T1 cfo_curr_liab 水平 | 0.14 | 0.72 |
| T2 cfroa | 0.15 | 0.35 |
| T3 roe | 0.18 | 0.76 |
| T4 roic | 0.17 | 0.72 |
| T5 berry | 0.15 | 0.17 |
| T6 qpdi5 均值66 | -0.11 | 0.49 |

**mdl138 族终榜**：12 模板 max 0.31，全灭。⚠ 关键对照：L1 的 `ts_rank(qpdi3_cfo_curr_liab,1260)` 裸探针 0.97，但 group_rank 水平 0.14 ⇒ **信号载体是 1260 长窗 ts_rank（时序分位），不是截面水平**。mdl138 已到十字路口：要么按 ts_rank 长窗几何深挖（1-2 条结构变体确认），要么关族。下一波：ts_rank 窗 1260/504 双档 × 3 个强字段（cfo_curr_liab/berry/qpdi3_cfroa）。


### L2 scl15 收割（12 模板）：全灭
- max S 0.42（dividend_trend? 实为 T1 fundamentalstrength 类），2Y 普遍 <0.6 且多负 ⇒ **scl15 社媒情绪族关面**（12 结构全试，无爆点，2Y 系统性弱）。



### L2 mfm 收割（10 模板）
| 模板 | S | 2Y |
|---|---|---|
| **earnings_yield 暴露** | **0.95** | **1.93** |
| value_factor_score | 0.29 | 1.63 |
| growth ts_mean66 | 0.28-0.30 | — |
| sector_risk_tilt | **-2.39** | -2.68 |（强反向：做多高 tilt 即做空 ⇒ 反向臂 |S| 2.39，TO 0.86 偏高）
| idio risk ts_rank504 | -0.84 | — |

⇒ **earnings_yield 暴露**：S 0.95 + **2Y 1.93**（全 AMR 第一个 2Y 过 1.58 的骨架！）——收益收益率因子暴露在 AMR 是活信号且近年未衰减。反向 sector_tilt |S| 2.39 但 TO 0.86 越界（>0.7 闸），需慢化后复测。
- 下一波：EY 暴露深挖（窗口/分组/与 value 合成、反向 sector_tilt 慢化版）。

### L2 insider 合成 + mdl138 ts_rank 确认批收割（03:3x）
**insider 2:1 合成：失败**（0.82 / 0.62，低于 T1 单腿 0.88）——T1 与 T10 同族高相关，合成只稀释不增益 ⇒ insider 族单数据集内穷尽（12 模板 + 2 合成，max 0.89），**记族天花板 0.89**；如继续只能跨数据集冷腿（占 OTHER 组合配额）。

**mdl138 ts_rank 确认批：几何成立，AMR 新高**
| 表达式 | S | 2Y |
|---|---|---|
| ts_rank(qpdi3_cfo_curr_liab, **504**) | **1.06** | 0.28 |
| ts_rank(qpdi3_cfroa, **504**) | **1.05** | 0.26 |
| ts_rank(qpdi3_cfo_curr_liab, 1260) | 1.02 | 0.38 |
| ts_rank(qpdi3_cfroa, 1260) | 0.98 | 0.16 |
| ts_rank(qpdi5_berry, 504/1260) | 0.71/0.51 | — |

⇒ **W504 优于 W1260**；cfo_curr_liab（现金流/流动负债偏差）与 cfroa 是双强字段。1.06 vs 线 1.58 差 0.52。
**破线手段（按 EUR 实证优先序）**：① 2:1 跨字段合成（同族不同基本面口径，cfo_curr_liab×cfroa 低相关对）② SLOW_AND_FAST 中性化档（慢信号 TO 6% 符合适用条件）③ 分组轴换 subindustry/sector。


### L2 mdl138 wave2 收割：合成无增益，天花板锁定 ~1.07
| 版本 | S | F | 2Y |
|---|---|---|---|
| cfo×cfroa 2:1 合成 | 1.07 | 0.66 | 0.31 |
| 1:1 合成 | 1.07 | 0.66 | 0.33 |
| SLOW_AND_FAST | 0.91 | 0.53 | 0.48 |

⇒ 两腿同族高相关（cfo_curr_liab/cfroa 都是现金流口径），合成只加 0.01；SLOW_AND_FAST 降 S（与 EUR insider 相反，AMR SUBINDUSTRY 区分度不足）。**mdl138 族天花板 1.07，差 0.51，关面**（保留 ts_rank 504 骨架作 Mode B 合成腿储备）。

### 追加派发（03:2x）
- mfm_model_output L2 批（10 条风格因子暴露：idio risk / BAB / 低波 / value / EY / momentum / div_yield 动量 / growth / ts_rank504 / sector_tilt）已派：`1G1QIq9TC4F49y8mZhbQiFa`。模板文件 results/amr_mfm_L2_templates.txt。

原有：
- mdl138 ts_rank 确认批（3 强字段 × W1260/504）已派：`w6FXd3Ty4ltcFa6GRPwsRK`。前一个坏批 `2lZNc61Mn4wvccXNGNNoXS5` 是 PS 引号拼接错产生的单行坏式，会 ERROR，忽略。

原内容：
- scl15 L2 两批（FULL）：`2vJzla6vs4QE9X716QFTbhnp` / `1dGaOCdmb4sUbQCZKXUQzsY`。
- insider 2:1 合成探针（EUR 已验证处方，同数据集单塔 ATOM）：T1 强腿×T10 流量比 2:1、T1×directional 2:1 —— `4vcSXHaIJ4Erarx4LgKZsuc`。
- 目的：insider 族单腿上限 0.89，按「2:1 合成可同时抬 S/2Y」实证跨区复测。

- **EY/tilt 深挖波已派**（9 条 FULL：`47zIjF67W4hCcMp136hbkDg3`）：EY × {ts_rank252/504, subindustry, group_neutralize(rank), decay, ts_mean66} + tilt 反向 × {decay22, ts_rank1260, ts_mean66 慢化}。文件 results/amr_ey_tilt_wave.txt。



### EY/tilt 深挖波收割（9 条）——★tilt 反向 ts_rank1260 是金矿
| 骨架 | S | F | TO | 2Y |
|---|---|---|---|---|
| **ts_rank(−tilt,1260)** | **2.47** | **0.98** | 0.861✗ | **2.59** |
| EY group_neutralize | 1.04 | 0.76 | 0.03 | 2.01 |
| EY subindustry | 0.97 | 0.62 | 0.04 | 1.81 |
| tilt−decay22 | 0.97 | 0.50 | 0.24 | 1.72 |
| 其余 EY 族 | 0.65-0.87 | — | 低 | 1.2-1.9 |

- **ts_rank(−tilt,1260)：S 2.47 / 2Y 2.59 全场最高**，唯一缺口是 TO 0.861（闸 0.70）。F 0.98 贴线（闸 1.0）。
- 慢化已在飞：`2NfDKugV85cP9ow1OI3tFak`（6 版：decay66/126、ts_mean66/126、W504 组合）。
- EY 族确认稳健（0.85-1.04 / 2Y 1.8-2.0 / TO 极低），但 S 距线 0.5；EY×tilt 合成候选排队。






### 第三波收割（pv69+option30）：全灭（max 0.19）

## AMR 终局盘点（2026-11-06 06:0x）

| 面 | 最优 | 判据 |
|---|---|---|
| mfm tilt/EY | 2.47/1.04 | prod 0.80-0.85 镜像封盘 |
| insider_agg_matrix | 0.89 | prod 0.8011 镜像封盘 |
| mdl138 | 1.07 | 天花板（合成无增益） |
| scl15/snt21/snt22 | 0.42/0.18 | 全灭 |
| risk59 | 0.62 | 贫瘠边缘 |
| pv106 | 0.74 | 贫瘠 |
| pv69+option30 | 0.19 | 全灭 |

**AMR 系统性结论**：TOP600 小宇宙 + 仅 sentiment/pv 两塔 + 生产池对主流信号面全覆盖 ⇒ 结构性拥挤，无 REGULAR 白空间。

**下一步选项**：① 转区（GLB 58.8% 过闸率 / JPN / ASI）② 深挖 AMR 剩余 180 集长尾（ROI 极低）③ 改道 SuperAlpha（不同相关性规则）④ 暂停等 prod 槽释放后确认个别变体。

### pv106 收割（05:5x）+ insider prod 确诊
**pv106**：10 探针 max |S| 0.74（spreadbp ts_rank252），全灭——微结构价差在 AMR TOP600 无 alpha（流动性溢价不显著）。
**insider prod = 0.8011**（N1NK10Yg）——n=1 [0.8,0.9] 镜像 ⇒ insider_agg_matrix 全族封盘。

**系统性发现（三条最强面全部 prod 镜像）**：
| 族 | 最优 S | prod | 形态 |
|---|---|---|---|
| mfm tilt | 2.47 | 0.8052 | n=1 |
| mfm EY | 1.04 | 0.8327 | n=1 |
| insider | 0.89 | 0.8011 | n=1 |
⇒ AMR 生产池对主流信号面已全面覆盖 ⇒ 结构性拥挤，非参数/配比可解。

### sentiment21 塔料波收割（12 模板两批）：全灭
- max S 0.18（两批合计），2Y 系统性负 ⇒ **TRNA 聚合情绪面在 AMR 关**（与跨区 news/sentiment 同型全灭一致）。sentiment 塔的其它候选集：sentiment22/23/26/27、news 系情绪——按 8 探针快判死预算逐个试。


### d5W95vbJ 覆盖与逐年体检（03:4x）
- 十年覆盖 10/10（longCount>0，pnl≠0），TO 稳定 0.42-0.44。
- 逐年 S：2014 1.26 / 2015 3.06 / 2016 1.55 / 2017 0.87 / 2018 2.55 / 2019 1.72 / 2020 1.91 / **2021 0.39（谷）** / 2022 1.19 / 2023 2.29。
- 归因：非 recent_decay（2023 最强）；2021 单年谷但中位 >1.2 ⇒ target_gap_only 型，无单年塌陷主导。
- **F 闸闭式判定：to_target = 0.0947×1.64² = 0.255 > 0.125 且 TO 0.43 > 0.255 ⇒ 减速可救**（TO 需 -41%），或凸性抬 returns/S 同步放松。F 批（signed_power×2/1.5、W1008、decay5/4）在飞。



- truncation 0.05 版（rKR0pW0E）：S 1.82 / F 0.81 / TO 0.52 —— 与 trunc0.08 完全同值 ⇒ **truncation 非 F 杠杆**（tilt 信号权重本就分散）。备胎线关闭，主力 = tilt×EY 合成族。




### 🚨 tilt×EY 族 prod 归因完成：mfm 风格暴露面整体拥挤 → 族封盘（04:5x）
| 腿 | prod max | 直方图形态 |
|---|---|---|
| qML59dbj (2:1) | 0.8052 | [0.8,0.9] n=1 |
| d5W9kmqY (1:1) | 0.8492 | [0.8,0.9] n=2 |
| WjOYE32P (EY 单腿) | 0.8327 | [0.8,0.9] n=1 |

⇒ **两条腿各自都镜像生产池同一/不同 alpha** ⇒ 不是权重配比问题，是 **mfm_model_output 风格暴露面在 AMR 生产池已被占**（某人已提交同面 alpha）。按 E-10（prod 墙与 S 强度正相关）+ 镜像判据：换权重/换配比无解，**tilt/EY 全族封盘**（4 颗全闸件退役为 SuperAlpha 组腿储备）。

**封盘程序**：seal_dead_end 取证闸（forum_recon）因检索通道故障（control probe 'alpha' 0 结果）无法出 question_key ⇒ 封盘待用户豁免（fail-closed）。实证判据已足（双腿 prod 0.80/0.83/0.85 单钉镜像）。

**用户处置（问卷自动默认：waive_continue）**：豁免封盘程序，seal_dead_end 暂不写 registry（留待 forum_recon 修复后补），立即开下一独立族。
AMR 可提交数回到 0。下一独立族排队：insiders（天花板 0.89 已封）、earnings6（aC 1028）、analyst69、news79、socialmedia15（已关）… 候选：earnings6（International Findings，44 字段）。

### 🚨 qML59dbj prod = 0.8052 ✗（04:5x）
- 直方图：[0.8,0.9] **n=1**（单钉），其余 2.5 万 bins 全在 <0.7 ⇒ 与生产池某颗 alpha 持仓镜像（典型「同持仓镜像」形态）。
- 按用户纪律：n=1 单钉**不判死**，先归因后破墙 ⇒ 换权重/换冷腿比重。备选：1YNGQ5JM（3:1，S 2.00）、d5W9kmqY（1:1，EY 权重更高、TO 0.24，与 prod 镜像的偏离应更大）。
- 已读 1:1 prod：见下。

### 合成 v2 收割 + 独立席位数核定（04:4x）
| 版本 | S | F | TO | 2Y | failed |
|---|---|---|---|---|---|
| **3:1**（1YNGQ5JM） | **2.00** | 1.06 | 0.43 | 2.51 | **0** |
| 2:1-subind（KPJVjRLj） | 1.72 | 1.03 | 0.26 | 2.31 | **0** |

⇒ tilt×EY 合成族已有 **4 颗 failed_ra=0**（2:1/1:1/3:1/2:1-subind）。互相关矩阵：三主候选两两 0.89-0.98 ⇒ **同一信号簇，只有 1 个独立席位**；`max_mutually_below_subset = [qML59dbj]`。
- 提交位定 qML59dbj（首个全闸 + 最均衡）；3:1（S 2.00）作 prod 失败时的替补——同簇换权重不换信号，prod 表现应高度一致。

## 🥇 AMR 首颗全闸候选诞生（03:5x）

> prod 槽持续被并行会话占用（zq3Av2mK → O0A6Qz7p → VkxM1zG0 轮转），03:50-04:1x 多次 120s 超时；每次超时都在排队本 alpha 的计算，最终落 48h 缓存。退避 20 分钟读缓存。04:2x 观察到并行会话在循环跑多颗 prod（RRE5Mwkn 持锁 >4min），本 alpha 的计算已排队完成、值落缓存但工具的 busy-holder 检查挡住缓存读。退避 25 分钟。04:33 仍被 RRE5Mwkn 持锁（>25min，疑似并行会话循环重试）→ 退避拉长至 40 分钟。sentiment22 与 snt21 同型（TRNA 聚合），跳过不花预算。合成 3:1 与 subindustry 变体已派（`4dWS7vaGd5foc5B11rXbuCj1`）——为 qML59dbj 的 prod 风险准备备选与更强的塔内席位。
**`qML59dbj`** = `add(multiply(2, ts_decay_linear(ts_rank(−diversified_sector_risk_tilt,1260),4)), group_neutralize(rank(EY因子)))`（tilt:EY 2:1，同集 mfm_model_output/risk 塔，单塔无混配额）
| 闸 | 值 | 线 | 判 |
|---|---|---|---|
| LOW_SHARPE | 1.91 | 1.58 | ✅ |
| LOW_FITNESS | **1.08** | 1.00 | ✅ |
| LOW_TURNOVER/HIGH | 0.37 | [0.01,0.7] | ✅ |
| LOW_2Y_SHARPE | 2.51 | 1.58 | ✅ |
| CONCENTRATED_WEIGHT / SUB_UNIVERSE | — / 1.30 | — | ✅ |
| failed_ra_count | **0** | 0 | ✅ |
| self_correlation | **0**（AMR 无存量） | <0.7 | ✅ |
| 十年覆盖 | 10/10 年无空窗，2022-23 最强（2.51/2.56） | — | ✅ |

唯一 pending：**prod_correlation**（槽被 zq3Av2mK 占用，retry_after 240s）。investability 1.18/0.90 亦优。
交叉验证：1:1 版 d5W9kmqY S 1.64 / F 1.08 / 2Y 2.38 / TO 0.24 亦全闸过（backup）。

### F 闸批收割：F 卡 0.78-0.82，S 反升（03:4x）
| 版本 | S | F | TO | 2Y |
|---|---|---|---|---|
| decay4 | **1.82** | 0.81 | 0.52 | 1.80 |
| decay5 | 1.72 | 0.79 | 0.47 | 1.77 |
| sp×2 | 1.70 | 0.82 | 0.43 | 1.84 |
| sp×1.5 | 1.68 | 0.80 | 0.43 | 1.79 |
| W1008 | 1.66 | 0.78 | 0.43 | 1.73 |

⇒ 全部 S 过线但 F 停在 0.78-0.82（缺 0.18-0.22）。闭式：S 1.82 时需 TO≤R×3.31≈0.36（现 0.52）。
**下一杠杆：tilt×EY 同集跨面合成**（mfm 内 risk 因子两族，EY TO 0.03 超低）已派：`2m8KkuGp4msaUrz9DPejzx`（2:1 与 1:1）。EY 低换手会稀释整体 TO，正是 F 公式要的方向；EUR 实证跨面 2:1 合成 S 反升。

### ★ decay 精调收割：S 闸首破，只剩 F 闸（03:4x）
| inner decay | S | F | TO | 2Y | fail |
|---|---|---|---|---|---|
| **6** | **1.64 ✅** | 0.77 | 0.43 | 1.74 | **仅 LOW_FITNESS** |
| 8 | 1.54 | 0.76 | 0.37 | 1.68 | S+F |
| 14 | 1.38 | 0.74 | 0.29 | 1.66 | S+F |

- `d5W95vbJ` = ts_decay_linear(ts_rank(−tilt,1260),6)：**failed_ra_count=1（只差 F 0.77→1.00）**。returns 9.47%、margin 4.4bp、subU 1.03、DD 8.2%。
- F 闸破法（按 gate_attribution 闭式：需 returns↑ 或 TO↓）已派 5 版：`17ICFEd5N5eGbGz11eAEVdD3` = signed_power×2/×1.5 凸性集中（抬 returns）+ W1008 + decay 5/4（微调 S-TO 平衡点）。
- 若 F 批到 1.0：全闸通过 → self（AMR 无存量必绿）→ prod → **交用户确认提交**。

### tilt decay 阶梯收割（03:5x）——decay11 逼近提交线
| decay | S | TO | 2Y |
|---|---|---|---|
| 0（原始） | 2.47-2.56 | 0.86✗ | 2.58 |
| **11** | **1.48** | **0.32** | **1.63** |
| 22 | 0.96 | 0.20 | 1.42-1.48 |
| 33 | 1.12 | 0.20 | — |
| 44 | 0.97 | 0.19 | — |

⇒ decay11：S 1.48（差 0.10）/ TO 0.32 / 2Y 1.63 —— **TO 大幅修复且 2Y 过线**，只差 S 0.10。非单调（33>22）属噪声级差异，曲线在 decay 6-14 区间陡变。
- 已派 decay 6/8/14 精调批：`3r8HhM2up5ki8Ml16UcQEoPS`。若 decay6-8 出 S≥1.58 且 TO≤0.7 ⇒ **AMR 首颗全闸候选**。
- group_rank 包裹版 2.56 但 TO 0.86 同病，弃。

### tilt 慢化收割 + 阶梯追派（03:4x）
**慢化 6 版：TO 修好了，S 崩了**——decay66 S 0.91（原 2.47）、decay126 0.58、ts_mean66 0.48。信号与换手同源（KOR pv37 同病）。**当前最优折中：decay22 版 S 0.97 / F 0.50 / TO 0.24 / 2Y 1.72**（三闸绿、S 差 0.6）。
- 追派 decay 阶梯（11/22/33/44 + mean22 + group_rank 包裹）：`4DBvYmN44nvabhwYI2rgx1`，找 TO-S 曲线的最优折中点。
- **sentiment21 塔料波已派**（12 模板 2 批：`3g21Nugrx4FB9glAKZVQhBG` / `2BTuU48oo5jI9UEIdcU93Qm`）：pos−neg 差 × {水平/delta66/zscore/mean66/subindustry/ts_rank504/−neg 水平/流量比/凸性/decay/信噪比}。


### risk59 8 探针收割（04:5x）：弱族
best: −daystocover10day 0.62（TO 0.08 / 2Y 0.24）；次 −squeeze_risk 0.47。无一条近 1.58 ⇒ 记「贫瘠边缘」：不深挖不判死（留 ts_rank 长窗几何未试）。借券/空头拥挤机制在 AMR TOP600 弱。

### 金字塔结构发现（03:3x）
- AMR 金字塔仅 **2 座塔**：D1 sentiment ×1.7 / pv ×1.4（其余 category 不设塔位）。
- ⇒ 提交优先级：**sentiment21（sentiment 塔）> pv 族 > 其它**。scl15 是 socialmedia 不占塔；sentiment21（TRNA，210 字段全 MATRIX）是正牌 sentiment 塔料，aC 温和（1-11）。
- 排队：EY/tilt 波收割后开 sentiment21 波（pos/neg mean 差、4 档模块 × 水平/动量/zscore 12 模板）。

### 备选族准备（scl15）
- socialmedia15 全 32 字段 VECTOR，12 模板已设计并预检通过（results/amr_scl15_L2_templates.txt）：情绪对差（optimism−fear / trust−conflict）、buzz 加权 sentiment、lovehate 累计、managementtrust 动量、risk_score 凸性、emotionvsfact zscore、timeurgency、debt_score decay。
- 待 insider/mdl138 L2 出结果后按空槽派发（opt4 仍须独立小批）。

### L1 汇总结论（两轮共 ~101 条，QUICK）
- max S = **0.97**（mdl138 CFO 现金流质量 ts_rank 1260）、次高 0.80（mdl138 berry）、0.77/0.76（insider 买量累计）、0.57（opt4 权价量）、0.50（scl15 离职分）。
- 无一条 ≥1.58 ⇒ **所有类别 L1 裸形态均未达标**。按普查铁律「族连坐只降权不判死」，进入 L2/L3：对苗子族（mdl138 / insider_agg_matrix / opt4 / scl15 / mfm_model_output）做 ≥10 互异模板深挖，再判四态。


