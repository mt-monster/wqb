# DEU 第三席寻觅：波 S/T/U 归因（2026-11-10 午后续）

## 一、波 S：snl27 内部双腿 vector_neut（sim 1VpqQC9gq5fH9b4IrTMAXea）

10 条**全负**（S -0.19 ~ -0.67，2Y -0.79 ~ +0.06），longCount 127~154（**覆盖满** ✓）

| 候选 | S | 2Y |
|---|---:|---:|
| LLM0Vgoe | -0.67 | -0.79 |
| 3qo8Qavz | -0.52 | -0.56 |
| wpQ0Knkv | -0.53 | -0.70 |
| KPJWlXME | -0.50 | -0.66 |
| A1VojgXW | -0.49 | -0.47 |
| 9qxNZaOK | -0.45 | -0.62 |
| 58EPnadz | -0.36 | -0.37 |
| YP1RL2ol | -0.19 | -0.03 |
| qMLQ9P2K | -0.11 | 0.06 |
| 9qxNZa5K | -0.43 | -0.72 |

⇒ 按判据 MG「符号一致全负 = 方向反了」⇒ 派波 T 翻转符号。

## 二、波 T：符号翻转（sim yQ730cQK4B7absDbCU2kAU）

10 条**全正但强度极弱**（S 0.11 ~ 0.67，2Y -0.06 ~ 0.79）

| 候选 | S | 2Y | longCount |
|---|---:|---:|---:|
| A1Voj7XR | 0.67 | 0.79 | 150 |
| d5WNkRrv | 0.53 | 0.70 | 151 |
| qMLQ96JE | 0.52 | 0.56 | 151 |
| 78Le7nRL | 0.50 | 0.66 | 151 |
| 9qxNZ7Oe | 0.49 | 0.47 | 127 |
| 2rA38Now | 0.45 | 0.62 | 151 |
| d5WNkRJX | 0.43 | 0.72 | 151 |
| zq3lKRnd | 0.36 | 0.37 | 151 |
| omEx8g0J | 0.19 | 0.03 | 151 |
| RREGj1wo | 0.11 | -0.06 | 127 |

### ★ 判据 ML（attention 类数据在 DEU 的强度-覆盖不可兼得）

| 源 | 起始年 | 强度 | 覆盖 |
|---|---|---|---|
| snt7（Wikipedia 浏览量） | **2019** | **强**（波 Q S1.78） | ✗ 前 5 年空窗 |
| snl27（Tranco 域名排名） | 2014 | 弱（波 T S≤0.67） | ✓ 满覆盖 |

⇒ **wpQ0prQY 的 S1.78 强度来自 snt7，而 snt7 在 DEU 无 2014-2018 数据**；
把 snt7 换成 snl27 后强度塌到 S≤0.67。
⇒ **attention/关注度族在 DEU 走不通**（强度与覆盖不可兼得，且 OS 已提交件 bl6OWZ2M 占用该族）。

## 三、波 U：news18 独特字段（sim 3r9UWV9l4Thb4yT23agub2，在飞）

字段：`analyst_recommendation_change`（分析师推荐变动）、`days_since_similar_event`（相似事件间隔）、
`event_sentiment_score`、`event_relevance_score`、`nws18_nip`、`story_event_record_count`、
`nws18_multiple_comp_ssc`。10 条，含正反两个方向。

**设计意图**：`analyst_recommendation_change` 与分析师修正族（已封盘）**信息面不同** ——
它是**新闻事件中提到的推荐变动**，不是卖方分析师预测修正本身 ⇒ 若出货可点 news 塔（当前 0 颗）。
`days_since_similar_event` 是事件新颖度的反向刻度（同一事件被重复报道的间隔）⇒ 属信息拥挤度代理。

## 四、波 V：news50 面板型字段（sim p3hq97ln4Vh9Bf1e3Jy1x36，在飞）

字段：`mws50_vea`（91 日聚合事件量 —— **面板型，非单条事件**）、`mws50_ens`（事件新颖度）、
`mws50_ess`（实体情绪分）、`mws50_ssc`、`mws50_relevance`、`mws50_nip`。10 条 + 1 条覆盖探针。

**设计意图**：news104/news18 的事件型字段判死（判据 MI），但 `mws50_vea` 是 91 日滚动聚合
⇒ 天然接近面板形态，是 news 族里最可能有截面定价力的字段。

## 五、本轮方法论增量

- **ML**：attention 类数据的**强度与覆盖可能不可兼得**（信号强的源起始年晚）。
  选这类族时必须同时问「强度从哪来」和「历史够不够长」，否则会做出 S1.78 但覆盖 5 年的件。
- 判据 MG 再次验证有效：snl27 族全负 → 翻转后全正但强度不足 ⇒ 方向判断正确，强度判断也正确。
