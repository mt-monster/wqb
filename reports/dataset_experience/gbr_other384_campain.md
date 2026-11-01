# GBR D1 other384 挖掘经验（电话会议 Q&A 类 · 判死）

范围：2026-10-30。GBR/TOP700/D1 的 `other384`。**6 个结构互异模板 + 1 条 E11 变体全部未达闸**。
本集是「同源语言数据三集」中模板覆盖最完整的一个，因此它的判死证据强度最高。

数据集画像（DB `datasets` 表实读，id=497）：category **`OTHER`**、`field_count 33`、
`coverage 0.8204`、`alpha_count 112`、`value_score 3`、`pyramid_multiplier 1.7`、
`tier STANDARD`、`delay 1`。

★ 注意 `tier STANDARD`（不是 EXCLUDED）、`coverage 0.8204`（偏高）、
`pyramid_multiplier 1.7`（高位）—— **三个「看起来该挖」的信号同时成立，但实测全灭**。
这正是本文件的价值：证明这三个先验**都不能替代回测**。

## 判死结论（registry：`GBR-OTHER384-EARNINGSCALL-DEAD`，2026-10-30）

6 个结构互异模板 + 1 条 E11 变体，共 7 条，全部未达硬闸。完整模板清单、逐条指标与
骨架原文见
[模板库文档](../../docs/reference/template_library_other384_earningscall_gbr_20261030.md)。

与同源两集的合并证据：`analyst83`（6 模板）+ `fundamental45`（2 探针）+
`other384`（6 模板 + 1 变体）= **16 条回测 0 达标**。

## 为什么判死落在「机制族」而不是「数据集」

三集都指向同一个结论：**电话会议语言数据在 GBR/TOP700/D1 没有跨截面超额**。
理由链条：

1. **GBR TOP700 的电话会议覆盖稀疏且同质** —— 700 只大盘股的财报电话会议在
   语调/结构上高度相似，跨股票截面差异小，tone 类字段天然缺乏区分度。
2. **信息已进价格**：覆盖度高的大盘股，电话会议内容被卖方快速消化（
   论坛 `43907846056599` 也指出 tone 的水平信息弱、变化项反转向）。
3. **三集失败方向一致**：水平弱（最好 S 0.29）、一阶变化更弱（0.07）、
   分歧度与覆盖度转负 ⇒ 不是某一集的字段质量差，而是机制不成立。

## 后续边界

- **不再在 `other384` 上新增模板**，也不在 `analyst83` / `fundamental45` 上新增。
  三集已构成完整的机制族判死。
- 若将来重启 transcript 机制，必须换区（如 USA / EUR 这类电话会议样本更丰富、
  截面更异质的市场），并重跑 ≥10 个结构互异模板 —— 不要把 GBR 的判死结论外推到
  大盘股池更大/更异质的区，也不要反过来拿别区的成功当 GBR 可行的证据。
- `coverage 0.8204` + `tier STANDARD` + 倍率 1.7 的组合**不构成可行理由**：
  覆盖率只保证回测不因缺数据失败；`tier` 是 S0 先验；倍率只放大已成立的信号。
- 本集回测**未入 `backtest_results` 表**（`region='GBR' AND dataset='other384'` 实读 0 行），
  证据仅存于模板库文档与 registry payload。

## 证据落点

- 判死条目：`registry_empirical` → `GBR-OTHER384-EARNINGSCALL-DEAD`
- 7 条模板全表：[`template_library_other384_earningscall_gbr_20261030.md`](../../docs/reference/template_library_other384_earningscall_gbr_20261030.md)
- 同源姊妹集：`gbr_analyst83_campain.md`、`gbr_fundamental45_campain.md`
- 论坛模板：`43907846056599`（earnings-call tone 权威实证，3 赞）
- 外部文献（设计模板用）：Larcker & Zakolyukina 2012 JAR 50(2)、
  Matsumoto-Pronk-Roelofsen 2011 TAR 86(4)、Hollander-Pronk-Roelofsen 2010 JAR 48(3)
