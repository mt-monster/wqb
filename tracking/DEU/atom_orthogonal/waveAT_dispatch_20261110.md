
---

## Wave AT dispatch（D1 event_sentiment_signals 十模板池，sim pEKXx6GI4Mlc1TltEl5T6X）2026-11-10 16:20
背景：D0 已按用户指令冻结；event_sentiment_signals 是 D1 唯一未判死的 sentiment 邻接族（探针 S0.74/2Y1.85/sub0.73，2020/21 双负旧弱新强）。
按判死前探针穷尽度硬约束：仅 2 条探针不满足判死条件，需十模板池全覆盖后才能终判（出活件或合规判死）。
模板池（cache/_waveAT_pool.json，早已预检 valid=true）：
| # | 模板 | 来源 |
|---|---|---|
| A1 | section_key_driver level sub | 探针冠军基线 |
| A2 | section_key_driver quantile-IR ind | OS 冠军几何 |
| A3 | pos-neg ts_covariance 252 sub | 论坛 52 赞模板 |
| A4 | key_factor_score delta66 ind | 论坛帖2（变化>水平） |
| A5 | −neg_score std_dev 252 sub | Mayew 不确定性溢价 |
| A6 | event_weight level ind | 事件强度 |
| A7 | word_count delta66 sub | 信息量变化 |
| A8 | section_score_d1 level ind | 次日截面分 |
| A9 | section_key_driver quantile(delta 132) | 非线性年变 |
| A10 | tvr_decay 双窗 on key driver | 借券族冠军几何 |
设置：DEU/TOP500/**D1**/decay4/SUBINDUSTRY/trunc0.08/nanON（delay=1 遵用户 D0 冻结指令）。
---

## Wave AT 判决（event_sentiment_signals 十模板池，sim pEKXx6GI4Mlc1TltEl5T6X，10/10 COMPLETE）

| # | 模板 | alpha | S | F | 2Y | TO | lc | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| A1 | key_driver level | 88RM0j9X | **0.70** | 0.34 | 1.97 | 0.034 | 126 | 0.64 |
| A8 | section_d1 level | E569jpAL | 0.59 | 0.28 | 0.93 | 0.037 | 131 | 0.74 |
| A9 | quantile(年变) | ZYQO8bZY | 0.59 | 0.27 | 1.44 | 0.055 | 117 | 0.65 |
| A5 | −neg vol | E569jpJL | 0.23 | — | — | — | 172 | — |
| A7 | word_count delta | npvLjdb8 | 0.06 | — | — | — | 71 | — |
| A4 | key_driver delta66 | 78Le5N9x | 0.00 | — | — | — | 71 | — |
| A2 | quantile-IR | omExbLMl | -0.03 | — | — | — | 35 CW | — |
| A6 | event_weight | WjOvZbmk | -0.10 | — | — | — | 74 | — |
| A3 | pos-neg covariance | WjOvZb6Z | -0.32 | — | — | — | 78 | — |
| A10 | tvr_decay | 0mY1VXok | -0.47 | — | — | — | 162 | — |

### 终判：event_sentiment_signals 族天花板 0.70 < 1.58 ⇒ 死（穷尽度合规：10 结构互异模板 = 水平/变化/波动/协方差/quantile/非线性/多轴全覆盖）
- 水平类（0.70/0.59/0.59）> 其余全灭，语调慢水平信号第三次验证；
- quantile-IR 再次 lc 崩塌（126→35，CW）——几何堆叠×事件稀疏第 4 次复现；
- **D1 sentiment 邻接宇宙就此全部关闭**（sentiment7/27/33、analyst10、ai_news_scores、news_sentiment_nlp、earningscall_sentiment、event_sentiment_signals、socialmedia12 弱、news20 全灭）。
