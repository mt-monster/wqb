# Wave AR verdict + Wave AS dispatch — 2026-11-10 (sentiment 优先挖掘)

## Wave AR 探针判决（sim 29IEqCbwg4X3aKsb097Her1，10/10 COMPLETE，0 error）
| # | dataset | alpha | S | F | 2Y | TO | sub | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | ai_news_scores | 9qxNM2J2 neg level | 0.21 | 0.06 | -0.10 | 0.063 | 0.02 | 死 |
| 2 | ai_news_scores | mLoE7lXW pos-neg diff | 0.17 | 0.04 | -0.82 | 0.067 | 0.05 | 死 |
| 3 | earningscall_sentiment | j2YqGMZo profit_summary level | **1.02** | 0.61 | 1.37 | 0.026 | 0.43 | ★毕业 |
| 4 | earningscall_sentiment | 9qxNM2r9 leverage_pres level | 0.90 | 0.52 | 1.22 | 0.032 | 0.02 | 活 |
| 5 | earningscall_sentiment | wpQ0Gvld profit_answer level | 0.85 | 0.48 | 0.89 | 0.028 | 0.30 | 活 |
| 6 | event_sentiment_signals | 9qxNM279 key_factor_score | -0.05 | -0.01 | 0.33 | 0.022 | 0.55 | 弱 |
| 7 | event_sentiment_signals | N1NYz2R8 section_key_driver | 0.74 | 0.39 | 1.85 | 0.040 | 0.73 | 条件存活 |
| 8 | news_sentiment_nlp | akK5zg16 headline_sent_avg | 0.04 | 0.00 | -0.39 | 0.084 | 0.10 | 死 |
| 9 | socialmedia12 | omExGkNl sentiment_score | 0.43 | 0.19 | 1.47 | 0.037 | -0.08 | 弱(lc78) |
| 10 | socialmedia12 | 88RMJ2pX expected_price_chg | 0.54 | 0.29 | 0.79 | 0.022 | -0.10 | 弱(lc79) |

### 判定
- **earningscall_sentiment 毕业**：3 字段同向 0.85-1.02（全 10 年期！非单年探针），TO 0.026-0.032 极低（margin 友好）⇒ 升级全模板池波 AS
- ai_news_scores 死（RavenPack 家族第 4 次证实无定价力）；news_sentiment_nlp 死（headline TextBlob 无信号）
- socialmedia12 弱+低覆盖（lc 仅 78/79 vs 其他 114-130）；event_sentiment_signals 条件存活（0.74/2Y1.85/sub0.73）暂缓
- **sentiment 族清账**：sentiment7/sentiment27/sentiment33/analyst10/ai_news_scores/news_sentiment_nlp 全死；earningscall_sentiment 活；event_sent/socialmedia12 边缘

## 论坛+论文先验（派 AS 前已查，符合硬约束）
1. 论坛帖 43691920948759（WQ36745，17 赞）：**问答(qa)相对演讲稿(pr)情绪的变化量**比绝对值更有信息——"排演之外"的部分
2. 论坛帖 43691562191895（KK37637，24 赞）：**语调变化比水平更有意义**，文本派生数据适合事件窗口
3. 论坛帖 35294898626711（RM49262，52 赞）：**ts_covariance(neg,pos,63/252/504)** 慢窗口出货；情绪是慢共有因子（Baker-Wurgler）；情绪信息在变化量不在水平
4. 学术（Mayew & Venkatachalam 2012）：管理层声音不确定性 ⇒ 负溢价；Q&A 语气比 scripted 更有信息量

## Wave AS 已派发（earningscall_sentiment 十模板池）
sim_id: 1FmkxU4rV5cDbkk13CXQbIjW，settings 同 AR（DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON）
| # | 模板 | 结构 | 来源 |
|---|---|---|---|
| T1 | profit_summary level | group_rank+ts_mean level | 探针基线 |
| T2 | profit_summary quantile-IR | ts_quantile(ts_ir(ts_mean)) | OS 冠军几何 |
| T3 | profit_summary tvr_decay | 双窗 delta multiply | 借券族冠军几何 |
| T4 | answer − presentation 差值 | 问答-陈述 contrast | 论坛帖1+Mayew |
| T5 | profit_summary ts_delta 66 | 环比语调变化 | 论坛帖2 |
| T6 | −leverage_pres ts_std_dev 252 | 语调波动率（不确定性溢价） | Mayew |
| T7 | assetutil_question quantile-IR | 换主题字段×冠军几何 | 自建 |
| T8 | leverage_pres zscore 504 | 长窗水平 z | 自建 |
| T9 | ts_covariance(profit,lev,252) | 二阶联动 | 论坛帖3（52赞） |
| T10 | profit_answer quantile(delta 132) | 非线性年化变化 | 自建 |

算子数：T1=5 T2=6 T3=9 T4=6 T5=4 T6=4 T7=6 T8=5 T9=5 T10=5（全部 ≤12 ✓）

## 探针冠军逐年健康度（AR 收割后补查，判据：连续空窗=0、负年结构）
### j2YqGMZo（earningscall profit_summary level，S1.02）
2014:2.10 / 2015:0.98 / 2016:0.50 / 2017:-1.32 / 2018:2.59 / 2019:1.05 / 2020:0.90 / 2021:0.28 / 2022:1.31 / 2023:1.45
- 负年仅 2017 一年（-1.32）；10 年零空窗；近三年 0.90/0.28/1.31 偏软但为正 ⇒ 近3年 CV 风险中等，需 AS 模板池里找更强者
### N1NYz2R8（event_sentiment section_key_driver level，S0.74）
2014:1.85 / 2015:0.82 / 2016:0.47 / 2017:0.16 / 2018:0.77 / 2019:1.48 / 2020:-1.16 / 2021:-1.13 / 2022:1.78 / 2023:1.92
- 2020/2021 双负（疫情+复苏期语调信号反转），近两年 1.78/1.92 强 ⇒ 典型"旧弱新强"，条件存活的证据加一分

---

## Wave AS 十模板池判决（sim 1FmkxU4rV5cDbkk13CXQbIjW，10/10 COMPLETE，0 error）
| # | 模板 | alpha | S | F | 2Y | TO | sub | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| T1 | profit_summary level sub | j2YqGMZo | **1.02** | 0.61 | 1.37 | 0.026 | 0.43 | 族冠 |
| T2 | quantile-IR ind | QPvw6ZzK | -0.13 | -0.03 | -0.23 | 0.198 | -0.41 | 死（lc仅36，IR几何在季度级字段上退化为噪声+CW） |
| T3 | tvr_decay 双窗 delta | 6Xd5NmJ7 | -0.17 | -0.04 | -1.17 | 0.032 | 0.07 | 死（符号反：季度级字段的 ts_delta 264/132 噪声主导） |
| T4 | 问答-陈述差值 | GrWZ91xo | -0.17 | -0.05 | 0.14 | 0.029 | -0.33 | 死（符号负 ⇒ 若翻转或有机会，但 sub -0.33 结构弱） |
| T5 | ts_delta 66 ind | LLM03Vrm | 0.67 | 0.34 | 1.38 | 0.055 | 0.43 | 活（变化量>水平，论坛帖2先验方向正确但强度不够） |
| T6 | −leverage 语调波动率 | P0okKQKW | 0.29 | 0.09 | -0.40 | 0.020 | 0.24 | 弱（方向对但幅度小） |
| T7 | assetutil quantile-IR | kqNz9E9L | -0.15 | -0.04 | -0.85 | 0.178 | -0.65 | 死（同 T2：IR 几何×季度级字段 = lc 崩塌 31） |
| T8 | leverage zscore 504 | zq3leKe8 | 0.51 | 0.22 | 1.17 | 0.033 | 0.09 | 边缘 |
| T9 | ts_covariance(profit,lev) | LLM03V2L | -0.02 | -0.00 | 0.01 | 0.021 | -0.04 | 死（两主题语调正交，协方差无信息） |
| T10 | quantile(delta 132) | N1NY8x27 | 0.29 | 0.09 | 0.79 | 0.046 | 0.13 | 弱 |

### AS 归因（按模板族，不按单条）
1. **水平类几何（T1/T8）> 变化类（T5/T10）> 二阶/IR 类（T2/T7/T9）**。earningscall 语调是**慢水平信号**：探针 level S1.02 就是天花板附近，没有哪条模板能把它推到 1.58。
2. **quantile-IR/OS 冠军几何在季度级稀疏字段上系统性失效**（lc 116→31/36，CW 连坐）——与 sentiment33 的 CW 死因同构（事件稀疏 × 几何堆叠）。
3. **族天花板 = 1.02**（T1），距 S1.58 差 0.56；最强变化模板 T5 也只有 0.67。**earningscall_sentiment 单数据集判死**（REGULAR 线不可达）。
4. 论坛先验部分应验（变化>水平：T5>T2；差值无增益：T4 死）但强度远不足以过线。

### sentiment 优先挖掘总账（用户指令闭环）
| 数据集 | 探针/波 | 终判 |
|---|---|---|
| sentiment7 | 批 Vl0pSdjo | 死 S≤0.77 |
| sentiment27 | 批 32qm4XaV | 死 S≤0.64（仅可作正交腿） |
| sentiment33 | 波 AQ | 死 CW 结构性 |
| analyst10 | 波 AP | 死 |
| ai_news_scores | 波 AR | 死 S≤0.21 |
| news_sentiment_nlp | 波 AR | 死 S≤0.04 |
| socialmedia12 | 波 AR | 弱 S≤0.54（lc78 低覆盖） |
| event_sentiment_signals | 波 AR | 边缘 S0.74（旧弱新强 2020/21 双负） |
| **earningscall_sentiment** | **波 AR→AS** | **族天花板 1.02，判死** |

**⇒ DEU sentiment 全族终判：无一可达 REGULAR 1.58 线。sentiment 方向关闭。**
（下一优先级建议：news 塔未测集 news20/news38 —— cov 0.92/0.60，塔未点亮；或按用户裁定放开 region）


