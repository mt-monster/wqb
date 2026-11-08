# S1 字段画像 · news20 Web Sources News Sentiment（KOR / TOP600 / D1）

> Wave3 首选应急集（仅 Wave2 other553 全灭后启用）。category=news，塔 0/3，乘数 1.6。
> 全部 VECTOR。论坛：「信息洪流里捞金：news20 网页舆情降噪」+「别再用裸 sentiment —— relevance 加权 + 新颖度」。

## 核心可用字段

| 字段 | cov | aC | 语义 | 角色 |
|---|---:|---:|---|---|
| nws20_ssc | 0.66 | 15 | 综合情绪 -1~+1 | 主信号 |
| nws20_relevance | 0.60 | 2 | 实体相关度 0-100 | 门控/加权 |
| nws20_nip | 0.60 | 17 | 市场冲击估计 | 主信号 |
| nws20_event_sentiment_score | 0.41 | 2 | 事件情绪 | 主信号 |
| nws20_event_similarity_days | 0.37 | 10 | 距同类事件天数（新颖度） | 新颖度 |
| nws20_rp_story_event_count | 0.66 | 13 | 故事事件数 | 注意力密度 |
| nws20_qmb | 0.60 | 24 | M&A 情绪 | 专题 |
| nws20_qep | 0.66 | 15 | 正负措辞分 | 主信号 |
| nws20_acb / bee / bam / ber | 0.60–0.66 | 10–22 | 分类器专题情绪 | 辅 |
| nws20_ghc_lna | 0.66 | 1 | 语气变化 | 辅（白） |

## 不宜裸用
- `headline` / `event_text` / `*_time_utc` / `country_code`：文本或元数据，不可连续定价。
- 裸 `ssc` 多噪声（论坛共识）；优先 relevance 加权。

## 论文先验
- Tetlock / RavenPack 系：CSS×REL 加权、ENS 新颖度过滤；负向情绪往往更可预测。
- 亚洲银行研究同构：WCSS = (CSS-50)×REL/100。
