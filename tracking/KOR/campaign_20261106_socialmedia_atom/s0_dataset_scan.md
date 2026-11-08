# S0 数据集扫描 · KOR × SOCIAL MEDIA（2026-11-06）

> 区域固定：KOR / TOP600 / Delay=1。方向：用户确认切到 Social Media 从零开波。

## 塔点亮表（get_pyramid_alphas）

| 塔 | 已提交 | 状态 | 乘数 |
|---|---:|---|---:|
| socialmedia | 0/3 | **未点亮** | 1.0 |
| sentiment | 0/3 | 未点亮 | 1.6 |
| news | 0/3 | 未点亮 | 1.6 |
| other | 1/3 | 未点亮 | 1.6 |
| insiders | 1/3 | 未点亮（上一战役交付但未提交） | 1.2 |

已点亮（≥3）：analyst / fundamental / model / shortinterest —— 本轮不选。

## 严格 category=socialmedia

| dataset | fields | cov | aC | uC | 判定 |
|---|---:|---:|---:|---:|---|
| **socialmedia39** Investor views | 1 | 1.0 | 580 | 183 | ✅ 主候选（共搜注意力） |
| other100 Investor views | 1 | 1.0 | 400 | 154 | 同主题镜像，次选/对照 |

⚠ 严格 Social Media **只有 2 集、各 1 字段** —— 10 颗结构互异模板只能靠算子几何/矩/窗口，经济轴单一。

## social-adjacent（待用户确认是否准入）

| dataset | category | fields | cov | aC | 备注 |
|---|---|---:|---:|---:|---|
| equity_forum_data | other | 6 | 0.8948 | 16 | 股吧/论坛活跃与情绪，语义最近 |
| other553 | sentiment | 21 | 0.6243 | 100 | 意见挖掘（含社媒文本） |

## 已知死集（本向相关）

- dead ledger：sentiment21、news79
- wave216：sentiment26 判死
- wave288（今日）：news_sentiment_transfer 探针全负

## 选集决议（初稿）

1. 先锁 **socialmedia39** 做 ATOM 主战场（塔未点亮、严格匹配目标文本）。
2. 若 1 字段机制天花板到顶（同族高相关 / S 上不去 / prod 封盘），再按过程约束「确实无计可施」扩到 equity_forum_data，并写明原因。


## 选集决议（暂定 · 问卷超时自动选，用户可改）

- **主战场**：`equity_forum_data`（social-adjacent / category=other，6 VECTOR，cov 0.8948，aC 极低）
- **对照探针**：`socialmedia39`（严格 Social Media，唯一字段为共搜邻居 ticker ID 向量）
- **切换理由**：严格 Social Media 字段形态=仪器 ID 列表，无法直接作连续截面信号；论坛数值字段才有可定价经济量。
- **塔**：other 1/3 未点亮；socialmedia 0/3 未点亮。单数据集 ATOM。
- ⚠ 本决议来自 Goal 问卷 60s 超时自动推荐，**非用户显式确认**；发波前若用户改选则整改。
