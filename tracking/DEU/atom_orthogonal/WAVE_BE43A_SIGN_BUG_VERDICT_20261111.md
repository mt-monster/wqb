# BE43a 判决：符号事故定性 + 差值几何证伪（2026-11-11）

## 一、8 臂结果（sim 28xKtQ3dj4hQa7j1aVK5tr0A，complete=8）

| 臂 | 变体 | S | F | TO | y2 | sub |
|---|---|---:|---:|---:|---:|---:|
| vRAR0Qmz | Δ44 | 0.54 | 0.18 | 0.25 | 0.91 | 0.08 |
| d5a5qGQK | nip×ssc | 0.68 | 0.23 | 0.30 | 0.70 | 0.56 |
| rK7KkxW8 | ssc | 0.71 | 0.25 | 0.30 | 1.37 | 0.14 |
| 1YWYvMgz | Δ88 | 0.35 | 0.10 | 0.23 | 0.54 | -0.19 |
| gJaJv23l | relevance 加权 | 0.19 | 0.04 | 0.23 | 0.46 | 0.09 |
| Wjljk5pj | backfill66 | 0.31 | 0.08 | 0.24 | 0.34 | 0.00 |
| e7a7AjOp | I7 rank504 | 0.22 | 0.05 | 0.24 | 0.41 | 0.02 |
| N1P1MZpo | group_rank+mean8 杂交 | 0.24 | 0.07 | 0.14 | 0.92 | 0.04 |

## 二、★根因：新闻腿符号错误（派发事故，非机制结论）

对照 P05JM61x 平台原始表达式（get_alpha_details.code）：
`group_zscore(add(group_rank(ts_delta(ts_backfill(vec_avg(nws20_multiple_comp_event_sentiment_score),132),66),sector), I7), market)`
——新闻腿是 **正号**。BE13 派发档案的符号约定「新闻正面情绪取正」与此一致。

本波 8 臂全部写成 `add(-news, I7)`。注意 **add(-A,B) 不是 add(A,B) 的翻号**：
- add(A,B) = 求和几何（I7 + news）
- add(-A,B) = 差值几何（I7 − news）
两者是不同信号（当 var(A)≈var(B) 时近似正交），所以塌到 0.2-0.7 不等于「救援线死了」，
只证明 **差值几何弱**。BE14 记录的 S 1.46-1.52 仍有效。

## 三、教训（派发前必查）

**组腿符号必须从存量 alpha 的平台原始表达式核实**（get_alpha_details → code 字段），
不能从波次表格的简写（「Δ66 × I7」）推断符号。本次事故成本 = 1 个 multisim（8 臂）。

## 四、补救

BE43b 已重派（sim 1deDcm33t5k4awe15y26MWm6，8 臂）：全部同变体换正号，
另加 Δ55 窗口谷；中性化对照批（STATISTICAL/INDUSTRY/FAST × P05JM61x 基线几何）3 件同步在飞。

## 五、中性化四点曲线（news_stat/news_industry/news_fast 对照批，P05JM61x 基线几何）

| 中性化 | alpha | S | F | TO | y2 | sub | fail |
|---|---|---:|---:|---:|---:|---:|---|
| SUBINDUSTRY（基线） | P05JM61x | **1.46** | 0.79 | 0.236 | 1.36 | 0.61 | 4 |
| STATISTICAL | A1x1qvNg | 1.38 | 0.63 | 0.245 | 1.38 | 0.64 | 4 |
| INDUSTRY | 78Y8g3j1 | 1.37 | 0.72 | 0.222 | **1.52** | **0.79** | 3 |
| FAST | qM7Me39j | 1.32 | — | — | — | — | — |

**结论**：S 维度 SUBINDUSTRY 最优（与 fnd45 四点曲线同构，STATISTICAL 非普适杠杆）；
INDUSTRY 以 S−0.09 换 sub+0.18/y2+0.16，若 BE43b 某臂 S 破 1.58 但卡 sub，可用 INDUSTRY 档微调。
D6（配置轴：4 档中性化 × TOP500/D1 唯一组合）就此补齐——NEWS 线判死穷尽度六维全覆盖。
