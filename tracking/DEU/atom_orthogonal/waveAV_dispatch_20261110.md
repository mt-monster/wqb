# Wave AV dispatch — other47 SEMrush 网络关注度探针（OTHER 塔 2/3，差 1 颗点亮）2026-11-10 15:50

sim_id: 4wqRoD3Be4j39wK17RiGLHhB（try 1 无 429）
背景：sentiment 全族判死、news20 判死、risk 族先验极低（risk60/68 死、risk71/72=Barra 残差族死、risk88=市值族）。
塔位（get_pyramid_alphas DEU/D1 实测）：model 3=点亮、analyst 6=点亮、**other 2（差 1 颗点亮）**、sentiment 1、shortinterest 2、risk 0、news 0。
⇒ OTHER 塔是「点塔均匀」目标下的最优未点亮方向；other47 = SEMrush 网络流量（DEU TOP500 德企数字足迹）。
先验：论坛 21149732774039（Earnings Uncertainty and Attention：低关注→反应不足→PEAD）+ 23936470549527（注意力溢出，ts_corr 结构）；本仓库 mLox6Mg2 双关注度正交残差机制同族。

探针 8 条：
1. oth47_organic_traffic level sub（uc30/ac54 主字段）
2. oth47_organic_traffic delta66 sub
3. −oth47_rank level sub（rank 越小流量越大）
4. oth47_organic_keywords level ind（关键词广度）
5. organic − paid 对比（earned vs 买量注意力）
6. oth545_score level sub（NEMO 2.0 综合分）
7. oth545_pln_omen delta66 ind（NLP 网络动量）
8. average_star_score level sub（other250 电商星级）
设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON，preflight valid=true unknown=[]

---

## Wave AV 判决（other47/other545/other250 关注度探针，sim 4wqRoD3Be4j39wK17RiGLHhB，8/8 COMPLETE）
| # | 模板 | alpha | S | F | 2Y | TO | lc | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AV1 | traffic level | 3qo82P2z | 0.45 | 0.20 | 0.76 | 0.012 | 116 | -0.27 |
| **AV2** | **traffic delta66** | **npvLXqXl** | **0.64** | 0.30 | **1.94** | 0.070 | 115 | **0.61** |
| AV3 | −rank level | O0Al2zjq | **-0.80** | -0.42 | -0.86 | 0.013 | 167 | -1.04 |
| AV4 | keywords level | 3qo82PO0 | 0.58 | 0.30 | 0.85 | 0.013 | 120 | 0.00 |
| AV5 | org−paid | leAoNGPe | 0.56 | 0.29 | 0.78 | 0.012 | 119 | -0.02 |
| AV6 | nemo score | omExkG0n | -0.09 | -0.02 | -0.62 | 0.025 | 88 | 0.13 |
| AV7 | pln_omen delta | 9qxN2MOV | 0.12 | 0.04 | 0.21 | 0.083 | 27 | 0.59 |
| AV8 | star score | ZYQO1zvQ | -0.10 | -0.02 | 0.59 | 0.032 | 108 | -0.47 |

### 归因
- **other47 活**：4/5 模板 S 0.45~0.64 同向。**变化量 > 水平**（AV2 0.64/2Y1.94/sub0.61 vs AV1 0.45）——与 sentiment33/论坛帖 P2 结论一致。
- **AV3 符号重大发现**：S=−0.80 ⇒ 翻转后 +0.80 且逐年健康（2014 +2.65，10 年仅 2 负年，lc 167 高覆盖）。**经济机制 = 反关注度**：SEMrush rank 数字越大（流量越小）⇒ 未来收益越好——小流量票被低关注低估（P1 论文"低关注→反应不足"直接应验）。
- other545 死（NEMO 综合分 lc88/S-0.09）、other250 死（星级 S-0.10，B2C 覆盖薄）。
- ⇒ **other47 毕业，Wave AW 十模板池已派**（sim 2iDe8kc1T4jX93kRXrv4GEH）：反关注 rank 水平（AV3 翻转）+ 关注度变化（AV2 冠军）+ quantile-IR(变化) + tvr_decay 双窗 + 关键词广度变化 + rank zscore504 + rank 年变 quantile + org−paid 动量 + 变化×水平交互 + 流量波动率空头。全部 ≤10 算子。

---

## Wave AW 判决（other47 十模板池，sim 2iDe8kc1T4jX93kRXrv4GEH，10/10 COMPLETE）
| # | 模板 | alpha | S | F | 2Y | TO | lc | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| W1 | rank level 反关注 | WjOvR6nQ | **0.80** | 0.42 | 0.86 | 0.013 | 117 | 1.04 |
| W3 | quantile-IR(traffic delta) | qMLQpovj | 0.78 | 0.42 | 1.73 | 0.072 | 115 | 0.83 |
| W5 | keywords delta | j2YqJbXZ | 0.77 | 0.42 | 1.41 | 0.049 | 117 | 0.83 |
| W8 | org−paid delta | qMLQpozV | 0.71 | 0.37 | 1.92 | 0.076 | 117 | 0.65 |
| W2 | traffic delta66 | npvLXqXl | 0.64 | 0.30 | 1.94 | 0.070 | 115 | 0.61 |
| W9 | delta×rank 交互 | 1YNrRQnQ | 0.55 | 0.26 | 1.45 | 0.070 | 95 | 0.85 |
| W6 | rank zscore504 | E569MXb9 | -0.04 | — | — | — | 119 | — |
| W7 | rank 年变 quantile | Jje6kZXO | -0.10 | — | — | — | 113 | — |
| W10 | −traffic vol | 6Xd5QvYY | -0.44 | — | — | — | 167 | — |
| W4 | tvr_decay | rKRZwvEa | -0.85（翻转+0.85 边缘） | — | — | — | 172 | — |

### 判定：other47 单数据集天花板 ≈ 0.80~0.85 < 1.58 ⇒ REGULAR 线不可达，单数据集判死
- 6/10 模板 S 0.55~0.80 同向 —— 族机制真实存在（反关注度 + 关注度变化），但强度天花板远低于 earningscall(1.02) 更低于 1.58。
- W1 反关注 rank：S0.80、10 年仅 2 负（2.65/2.27/…/1.90）、sub 1.04 —— **族内最稳骨架**，保留作未来 OTHER×集合外 组合腿的候选主腿（两塔组合候选 ≤3 配额内）。
- W3/W5/W8 三个变化类模板 2Y 1.4~1.9 且 sub 0.6~0.8 —— 新近年强，若未来放开组合腿，优先选变化类做腿。

### 本轮（AR→AS→AU→AV→AW）DEU 单数据集 ATOM 选集终账
| 数据集 | 波 | 终判 |
|---|---|---|
| sentiment 全族（7/27/33）+ analyst10 | 历史波 | 死 |
| ai_news_scores / news_sentiment_nlp | AR | 死 |
| socialmedia12 / event_sentiment_signals | AR | 边缘（0.54/0.74） |
| earningscall_sentiment | AS | 死（天花板 1.02） |
| news20 | AU | 死 |
| risk60/68/71/72/88 | 台账 | 不派（先验极低） |
| other545 / other250 / stock_cluster_dl | AV | 死 / 死 / 非信号 |
| **other47** | **AV→AW** | **死（天花板 0.80，但 W1 骨架保留作组合腿候选）** |

**⇒ DEU 未点亮塔的单数据集 ATOM 矿已穷尽。要继续产出必须：① 组合腿（OTHER×集合外，5 类配额内，非 ATOM）② 放开 region 约束（需用户裁定）③ 等波 AN 破墙后借券族第二席。**


