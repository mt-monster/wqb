# BE102 终判：news3/news21 词频情绪面判死（2026-11-12 深夜）

> 派发史：四连派（1x 幽灵 ×3 轮、1x 全 FAIL、1x 拆批重派成功）。全 FAIL 根因：news21 字段是 **MATRIX**，被 vec_avg 包裹 ⇒ 类型错连坐整批（wq-batch-dispatch-safety 又一实证）。修正后拆两批（news3 仅 VECTOR 7 臂 / news21 直接裸用 MATRIX 3 臂）。

## news3（词频归一化情绪，19 字段，7 臂 VECTOR）

| 臂 | 字段 | S | TO |
|---|---|---:|---:|
| fear 66 | nws3_scores_fearnormscr | 0.09 | 7.0% |
| finup 66 | nws3_scores_finupnormscr | 0.62 | 7.9% |
| finhype 66 | nws3_scores_finhypenormscr | 0.26 | 8.2% |
| uncertainty 66 | nws3_scores_uncertaintynormscr | 0.14 | 7.9% |
| findown 66 | nws3_scores_findownnormscr | **−0.45** | 7.6% |
| certainty 66 | nws3_scores_certaintynormscr | 0.33 | 8.0% |
| fear Δ66 | fearpartnormscr | 0.03 | 8.4% |

## news21（词频语气 MATRIX，3 臂直接裸用）

| 臂 | 字段 | S | 2Y |
|---|---|---:|---:|
| tone 66 | nws21_tone_tone_sc | 0.15 | 0.25 |
| pos 66 | nws21_pos_sc | 0.26 | 0.79 |
| neg 66 | nws21_neg_sc | 0.27 | 0.90 |

## 判死证书

- max |S| **0.62**（finup），无一带近线。news3 七个情绪维度读数分散（−0.45 ~ +0.62）⇒ 无一致方向。
- news21 词频三臂 0.15-0.27，2Y 0.25-0.90，弱且无梯度。
- **NEWS 塔第四面（词频面）关闭**：情绪/语义（BE38/BE43B）+ 流量计数（BE98）+ 词频（本波）三面证书齐备。news29/54/76 已零成本否决（元数据/deprecated）。
- 机制笔记：findown（财务悲观）是唯一 |S|>0.4 的臂且为负号（悲观→跌？反向 −0.45 即悲观低者涨）——量级不足以支撑定向补（<1.0）。
