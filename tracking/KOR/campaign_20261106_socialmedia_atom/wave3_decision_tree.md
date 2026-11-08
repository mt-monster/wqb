# Wave3 决策树（等 Wave2 other553 收割后执行）

> 铁律 F：无归因不得发波。本文件是收割后动作表，**不预派发**。
> 前置：Wave1 forum 全灭（maxS0.38）+ Wave1b REJECT → 已切 other553。

## KOR 塔快照（收割前刷新）
- sentiment **0/3** · news **0/3** · socialmedia **0/3** · other 1/3
- 已点亮勿选：analyst / fundamental / model / shortinterest
- dead ledger 相关：`sentiment21`、`news79`；S0 另记 `news_sentiment_transfer`、`sentiment26` 判死

## Wave2 other553 读数 → 动作

| other553 读数 | 下一刀 |
|---|---|
| S≥1.58 且 2Y≥1.58 | 收窄 ≤1/3：窗口谷 / group 轴 / 单调变换破闸；查十年覆盖；self+prod 用 MCP |
| 有 S≥1.0 但 <1.58 | 先归因 yearly；非尖峰 → 同式换 R&M；试倒数/industry；**不换集** |
| max|S| < 0.5 全灭 或 意见/估计轴零仓 | **无计可施再换集** → Wave3 首选 `news20`（Web Sources News Sentiment，news 塔 0/3，cov0.51，aC157）或 `news66`（Webpage View Stats，注意力代理，2 字段） |
| 仅反臂活 | 保留反臂，扩同向字段（ptg/rec/est） |

## Wave3 换集优先序（仅 other553 全灭时）
1. **news20** — Web Sources News Sentiment（语义：网页新闻情绪；未死；recommend 靠前）
2. **news66** — Webpage View Statistics（注意力计数，2 字段；社交相邻）
3. **news54** — Key Developments（事件密度；cov0.69；aC 低）
4. 备选：`sentiment27`（Website Popularity，aC1879 拥挤，末选）

## 明确不选
- `news79` / `sentiment21` / `news_sentiment_transfer` / `sentiment26`（已判死）
- `institutions6`（dead ledger；虽 recommend 高分）
- 已点亮塔数据集
- 禁混集合内互组（本战役保持单集 ATOM）

## 并发
create_multi_simulation ≤2；收割释放槽后再发。


## 修订（2026-11-06 夜 · 论坛先验）
- news20 首灭后 **不立即切 news66**：插入 Wave3b decay=10 同骨架/注意力加权批（`wave3b_news20_decay_payload.md`）。
- 理由：论坛明确新闻 decay 必须调大；decay=4 可能系统性压死时效信号。
