# Wave1 forum 收割归因（equity_forum_data）

- multisim: `16wGRu3Ko5629k914xORiRcV` COMPLETE 8/8
- 设置：KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08
- Wave1b 对照：已 REJECT（max S 0.94）

## 读数表

| tag | alpha_id | S | 2Y | Fitness | TO | 备注 |
|---|---|---:|---:|---:|---:|---|
| T01_attn_lvl | QPvNnKvM | 0.21 | 0.82 | 0.07 | 0.110 | 弱正 |
| T02_attn_delta | P0oYngo7 | 0.04 | 0.26 | 0.00 | 0.342 | 死 + CW |
| T03_attn_std | omEJnWa5 | **0.38** | 1.27 | 0.16 | 0.113 | 本批最强仍 <0.5 |
| T04_sell | WjOoNelP | 0 | — | — | 0 | **零仓/零 PnL**（字段空或常量） |
| T05_buy | wpQ25bov | 0 | — | — | 0 | **零仓/零 PnL** |
| T06_net | 9qxd9WGK | 0 | — | — | 0 | **零仓/零 PnL**（buy−sell） |
| T01_rev | rKRNbe0d | −0.39 | −1.14 | −0.17 | 0.110 | T01 反臂更差 |
| T08_breadth | e75VnQ1M | 0.17 | 0.79 | 0.05 | 0.110 | 弱正 |

## 归因
1. **max|S|=0.38 < 0.5** → 决策树「论坛注意力/意见轴在 KOR 弱」分支触发。
2. 意见字段（buy/sell/net）整族 **TO=0 / PnL=0**：KOR 上 `aggregate_*_opinion_score` 无有效截面，不是闸门问题。
3. 注意力族（comment_volume / participants / std）有极弱正号，但远低于 REGULAR 1.58；反臂更差 → 无方向翻转可救。
4. Wave1b scl39 未出奇强 → 不走 ID 向量伪信号分支。
5. **不发批 B R&M**：换中性化救不了 max S 0.38 与意见字段空仓。

## 决策
**无计可施换集** → 启用 `other553` 应急批（sentiment，塔 0/3；载荷已 preflight）。
换集原因：严格 SM=ID 向量不可用 + equity_forum_data social-adjacent 全灭（意见轴空、注意力轴 |S|<0.5）。
