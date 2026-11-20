# DEU / sentiment27 战役报告（2026-11-19）

数据集：sentiment27「Website Popularity Rankings」，DEU/TOP500/D1，coverage 0.9038 / 18 字段 / 平台 alphaCount 390（get_datasets 实读）。

## ① 回测的字段

10/11 个信号字段回测——**snl27_top50pctrankingavg 零臂未回测**（档案 §3.1 的 11 个信号字段含它，其计划臂 `rank(-vec_avg(...))` 未进本批 RESULTS）。两波共 25 臂（W1-01…W1-20、W2-01…W2-05），读数 S / F / TO / 2Y / RA fail：

**snl27_avgranking**（排名类，取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-01 | `rank(-vec_avg(snl27_avgranking))` SUBINDUSTRY | 0.13 | 0.03 | 0.0802 | -0.18 | 4 |
| W1-02 | `group_rank(-vec_avg(snl27_avgranking), sector)` SUBINDUSTRY | 0.20 | 0.06 | 0.0625 | -0.33 | 3 |
| W1-03 | `ts_delta(-vec_avg(snl27_avgranking), 5)` SUBINDUSTRY | 0.22 | 0.04 | 0.4334 | -0.03 | 4 |
| W2-05 | `group_rank(-vec_avg(snl27_avgranking), sector)` INDUSTRY | 0.13 | 0.03 | 0.0569 | -0.04 | 3 |
| W1-20 | `rank(-vec_avg(snl27_avgranking))` SUBINDUSTRY（W1-01 复跑对照） | 0.13 | 0.03 | 0.0713 | -0.16 | 4 |

**snl27_topranking**（排名类，取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-04 | `rank(-vec_avg(snl27_topranking))` SUBINDUSTRY | 0.48 | 0.27 | 0.0341 | 1.45 | 4 |
| W1-05 | `ts_zscore(-vec_avg(snl27_topranking), 22)` SUBINDUSTRY | 0.07 | 0.01 | 0.2192 | -0.42 | 4 |

**snl27_top50pctranking**（分位截断族，取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-06 | `rank(-vec_avg(snl27_top50pctranking))` SUBINDUSTRY | 0.18 | 0.05 | 0.0695 | 0.05 | 4 |

**snl27_top75pctranking**（分位截断族，取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-07 | `rank(-vec_avg(snl27_top75pctranking))` SUBINDUSTRY | 0.19 | 0.06 | 0.0957 | -0.44 | 4 |

**snl27_top75pctrankingavg**（分位内均值族，取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-08 | `rank(-vec_avg(snl27_top75pctrankingavg))` SUBINDUSTRY | 0.29 | 0.11 | 0.0642 | 0.19 | 4 |

**snl27_skewness**（矩类，禁止 !=0 变换）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-09 | `rank(vec_avg(snl27_skewness))` SUBINDUSTRY | 0.72 | 0.40 | 0.0910 | 0.65 | 4 |
| W1-10 | `ts_zscore(vec_avg(snl27_skewness), 22)` SUBINDUSTRY | 0.33 | 0.08 | 0.2741 | 0.08 | 4 |
| W2-03 | `rank(vec_avg(snl27_skewness))` INDUSTRY | 0.40 | 0.17 | 0.0863 | 0.27 | 4 |

**snl27_kurtosis**（矩类 slow，窗下限 66，禁止 !=0 变换）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-11 | `ts_zscore(vec_avg(snl27_kurtosis), 66)` SUBINDUSTRY | 0.43 | 0.14 | 0.2185 | 0.10 | 4 |
| W1-12 | `rank(vec_avg(snl27_kurtosis))` SUBINDUSTRY | 0.64 | 0.35 | 0.1005 | 0.61 | 4 |
| W2-04 | `rank(vec_avg(snl27_kurtosis))` INDUSTRY | 0.45 | 0.21 | 0.0950 | 0.56 | 5 |

**snl27_relpopularity08**（复合关注度，越高越好，不取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-13 | `rank(vec_avg(snl27_relpopularity08))` SUBINDUSTRY | 0.64 | 0.40 | 0.0325 | 1.79 | 3 |
| W1-14 | `ts_delta(vec_avg(snl27_relpopularity08), 5)` SUBINDUSTRY | -0.16 | -0.04 | 0.3232 | -0.56 | 5 |
| W1-15 | `group_rank(vec_avg(snl27_relpopularity08), sector)` SUBINDUSTRY | 0.71 | 0.45 | 0.0201 | 1.41 | 4 |
| W1-19 | `rank(vec_avg(snl27_relpopularity08))` SUBINDUSTRY（W1-13 复跑对照） | 0.64 | 0.40 | 0.0317 | 1.79 | 3 |
| W2-01 | `group_rank(vec_avg(snl27_relpopularity08), sector)` INDUSTRY | 0.52 | 0.30 | 0.0177 | 1.28 | 4 |
| W2-02 | `rank(vec_avg(snl27_relpopularity08))` INDUSTRY | 0.35 | 0.17 | 0.0313 | 1.39 | 4 |

**snl27_relpopularity1**（复合关注度参数版，不取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-16 | `rank(vec_avg(snl27_relpopularity1))` SUBINDUSTRY | 0.63 | 0.40 | 0.0326 | 1.73 | 3 |

**snt27_rank**（单域名排名，取负）
| 臂 | 表达式 | S | F | TO | 2Y | RA fail |
|---|---|---|---|---|---|---|
| W1-17 | `rank(-vec_avg(snt27_rank))` SUBINDUSTRY | 0.24 | 0.08 | 0.0949 | -0.13 | 4 |
| W1-18 | `ts_delta(-vec_avg(snt27_rank), 5)` SUBINDUSTRY | 0.09 | 0.01 | 0.4486 | -0.53 | 4 |

## ② 字段画像

画像档案：`tracking/DEU/reference/datasets/sentiment27.md`（机械闸 field_profile_completeness_gate.py exit 0，全表 18 行带实测读数）。

- **9 个排名/复合字段**（avgranking / topranking / top50pct* / top75pct* / relpopularity* / snt27_rank）：实测覆盖 0.756–0.762（378–381/500，平台声明 0.9022/0.9118，实际分母≈419，推断未核验）；daily，窗下限 5；非零膨胀；无 !=0 陷阱。
- **snl27_skewness**：覆盖 0.558（显著低于声明，形状字段更稀疏）；daily，窗下限 5；**equalsTrap=true**——法1(225L/54S)→法2(280L/0S) 多空反号翻转，禁止任何 !=0 / 抹负值变换；无界矩须 rank/zscore 后用。
- **snl27_kurtosis**：覆盖 0.632；**本集唯一 slow 字段，窗下限 66**（n5=0.835×cov、n22=0.870×cov 不达 0.9；法3 覆盖随窗变宽单调恢复 264→275→286）；**equalsTrap=true**——法1(31L/285S, S−0.86)→法2(316L/0S, S+0.92) 完全反号翻转。
- 方向约定：9 个排名类「越低越好」须取负；2 个 relpopularity「越高越好」不取负。
- 排除字段：snl27_totaldomains / snl27_totalcountrydomains（无界正计数须去规模，不在 signalFields）；snl27_wq_pit（平台明写 not an analytical metric）；4 个 SYMBOL 日期戳（元数据）。zeroInflated 全 false ⇒ trade_when 零值门控无对象，全部排除。

## ③ 匹配的机制

单机制数据集：Tranco 网站排名（网络关注度），单集内无两条独立腿。论坛证据引用（forum 44887744717335、forum 44636553257495、search_forum_posts_local scanned=800/matched=0）**出处待核**——本轮全仓 grep 无任何可对出处；PLANS/READINGS 读数以画像档案为准。

- **横截面注意力溢价**：`rank(±vec_avg(field))`——排名取负 / 复合得分直接 rank。全字段主力骨架。
- **行业中性注意力**：`group_rank(±vec_avg(field), sector)`——avgranking、relpopularity08 两字段部署。
- **关注度动量/结构变化**：`ts_delta(±vec_avg(field), 5)`——avgranking（W1-03）、relpopularity08（W1-14）、snt27_rank（W1-18）；`ts_zscore(…, 22/66)`——topranking（W1-05）、skewness（W1-10）、kurtosis（W1-11，66=窗下限）。
- skewness/kurtosis 用原值 rank/zscore，负样本完整保留（equalsTrap 排除全部 !=0 变换）。

## ④ 调优过程

**W1（20 臂，全部 SUBINDUSTRY）**：首发 10 字段 × 横截面/动量/分组骨架（top50pctrankingavg 未派臂）。
- 读数：全场无臂过 S 1.58。最佳三臂 W1-15（S 0.71 / F 0.45 / 2Y 1.41）、W1-09（S 0.72 / F 0.40 / 2Y 0.65）、W1-13/W1-16/W1-19（S 0.63–0.64 / F 0.40 / 2Y 1.73–1.79）。排名/动量类全灭（S 0.07–0.48，动量臂 TO 0.32–0.45 且 2Y 全负）；CONCENTRATED_WEIGHT 在 18/20 臂出现（仅 W1-02、W1-15 无）。
- 处方：只动中性化一维换 INDUSTRY，复测五个相对最强臂（relpopularity08 的 rank 与 group_rank、skewness rank、kurtosis rank、avgranking group_rank——后者为同骨架分组轴对照，非最强臂），不动骨架。

**W2（5 臂，全部 INDUSTRY）**：
- 臂表：W2-01 group_rank relpopularity08 / W2-02 rank relpopularity08 / W2-03 rank skewness / W2-04 rank kurtosis / W2-05 group_rank avgranking。
- 读数：全面劣于 W1 的 SUBINDUSTRY 版本——W2-01 S 0.52（vs W1-15 的 0.71）、W2-02 S 0.35（vs 0.64）、W2-03 S 0.40（vs 0.72）、W2-04 S 0.45（vs 0.64）、W2-05 S 0.13。INDUSTRY 方向证伪。
- 止损判据：未触发（停手线 `signal_floor.max_sharpe_floor=0.5`，两波最佳 0.72 / 0.52 均高于它，与 STOP「未触发停手」一致）；但两波后最佳臂 S 距 1.58 闸线缺口 0.86（1.58−0.72）且中性化维已双向试尽，无剩余可动维度，停止加注。

## ⑤ 下结论的判据

闸线：S 1.58 / F 1.0 / 2Y 1.58 / TO 0.7 / prod 0.7 / self 0.7。

最佳臂逐闸对照（W1-09 `rank(vec_avg(snl27_skewness))` SUBINDUSTRY，两波最高 S）：

| 闸 | 读数 | 线 | 判 |
|---|---|---|---|
| S | 0.72 | 1.58 | ✗ |
| F | 0.40 | 1.0 | ✗ |
| 2Y | 0.65 | 1.58 | ✗ |
| TO | 0.0910 | ≤0.7 | ✓ |
| RA | 4 fail（LOW_SHARPE / LOW_FITNESS / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE） | — | ✗ |
| SUB_UNIVERSE | 未单列（W1-15 的第四闸是 LOW_SUB_UNIVERSE_SHARPE 0.1<0.34，与 W1-09 的 CONCENTRATED_WEIGHT 不同闸） | — | 按臂而异 |
| prod / self | 未测（无候选进入相关性阶段，CORR 为空） | 0.7 / 0.7 | 未跑 |

次佳 W1-15（group_rank relpopularity08）：S 0.71 / F 0.45 / TO 0.0201 / 2Y 1.41 / RA 4 fail（LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE），同样卡在 S/F 主闸。

**卡在哪**：所有 25 臂 S∈[-0.16, 0.72]，距 1.58 全线不过；F 最高 0.45 距 1.0 不过；2Y 有三臂已过闸线（W1-13/W1-19 的 1.79、W1-16 的 1.73——blockedBy 无 LOW_2Y_SHARPE 即为证），但 S/F 拖死。卡点不是换手层（全臂 TO 0.0177–0.4486，均在 [0.01, 0.7] 带内）也不是配置层（SUBINDUSTRY/INDUSTRY 双向已测，SUBINDUSTRY 全面占优），是信号层：Tranco 排名的横截面注意力溢价在 DEU TOP500 定价能力不足。

**下一步**：字段维未穷尽——top50pctrankingavg 零臂，补测属新增臂而非「已试尽」；已回测的 10 字段上横截面/动量/分组/中性化四维已试尽，两波最佳 S 0.72→0.52 无改善。本集单机制（单一 Tranco 排名，无第二条独立腿）。按 §7.7，若继续只余配置档变维（宇宙/decay）与 §7.6 六维穷尽举证后按「信号层死 / 配置层死」分档记录；本报告不下判死结论（证据不足只记 PROVISIONAL）。
