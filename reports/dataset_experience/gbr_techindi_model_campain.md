# GBR D1 techindi_model 挖掘经验（`tm_16` / `tm_17` 时序预测族 · prod 饱和）

范围：2026-10-30。GBR/TOP700/D1 的 `techindi_model`。本文件记录该集 **`tm_16` / `tm_17`
两族（合计 399 字段）的 prod 饱和实证**；不外推为 techindi_model 全数据集（1830 字段）结论。

数据集画像（DB `datasets` 表实读，id=579）：category **`OTHER`**、`field_count 1830`、
`coverage 0.973`（本区最高档）、`alpha_count 495`、`value_score 5`、
`pyramid_multiplier 1.4`、`tier STANDARD`、`delay 1`。

★ 早先的判死记录曾写「`techindi_model` 只有三个字段同一条腿」——**那是错的**。
实读 1830 字段，其中 `tm_16_*` + `tm_17_*` 合计 399 个，是**本区字段体量最大**的族。

## 判死结论（registry：`GBR-TECHINDI-TM16-TM17-PRODSAT`，2026-10-30）

判死依据是 **prod 相关性饱和**，不是 IS 指标不行（IS 侧该集很能打）：

本地 `backtest_results` 实读（`region='GBR' AND dataset='techindi_model'`）：
**180 行、26 个波次、max Sharpe 1.91、max 2Y 2.08、TO 区间 3.86%–25.46%**。
→ 也就是说这是**「指标够、生产池撞墙」**的典型形态。

两族的具体墙：

| 族 | 墙的形态 | 实测 |
|---|---|---|
| `tm_16_*` | **self 自锁** —— 被自家已 ACTIVE 的 `3qVP6pNO` 占位 | self **0.87–1.0** |
| `tm_17_*` | **prod 饱和** —— 19+ 条全闸通过但 prod 全线超阈 | prod **0.7343–1.0**（`N1NogQ87` 0.8439、`O0Av1nZd` 0.8…） |

`9qxQamje`（`ts_backfill(tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q1,126)`）平台 `MATCHES_PYRAMID`
实读 `effective=1`、塔位 **`OTHER`**（倍率 1.5）—— 与 `rKRkL9QE` 同属 `dataset_id=291`
槽位但塔位不同，是「`dataset_id` 不可推断塔位」的第二个反例。

## ★ 为什么这是「判死」而不是「再调调看」

- **self 与 prod 回答两个不同问题**：`tm_16` 撞的是 self（自家池），`tm_17` 撞的是
  prod（整个生产池）。两个方向都撞满，没有第三个可用维度。
- 唯一低 prod 的样例来自**换机制**（`tm_16` 与 `tm_17` 的差），不是换窗口/换分组轴。
- 时序预测字段（`tm_*`）是「日频重新预测」类，相邻两日预测自相关低 ⇒ 换手是**字段生成
  方式**决定的；本集 TO 已被压到 3.86%（`ts_*` 长窗 + decay），说明换手侧不是瓶颈，
  真正的墙在**拥挤度**。
- `OTHER` 塔在 GBR D1 当时只有 1 颗（`get_pyramid_alphas` 实读），**塔位价值高但容量已被
  生产池吃满** —— 这是「塔没点亮 ≠ 有空间」的最佳反例。

## 后续边界

- **不再在 `tm_16` / `tm_17` 上派任何新回测**。这两族已确认 prod 饱和，继续挖只是在
  烧仿真并发与 prod 时隙。
- 若要用 `techindi_model`，必须落在**非 `tm_16`/`tm_17` 的其余 1400+ 字段**上，且换
  完全不同的机制（例如技术指标合成而非时序预测），并**先测一颗族代表 prod** 再决定量产。
- 本集 `coverage 0.973` 是「覆盖高 ≠ 有超额」的实例：覆盖率只保证回测不因缺数据失败，
  不保证信号独立于生产池。
- 本地 `alphas.dataset_id` 与 `backtest_results.dataset` **两处口径不同**
  （前者把这族记成 `291`，后者记成 `techindi_model`）⇒ 归集时以 `backtest_results.dataset`
  或表达式字段名为准。

## 证据落点

- 判死条目：`registry_empirical` → `GBR-TECHINDI-TM16-TM17-PRODSAT`
- 回测台账：`backtest_results`（`region='GBR' AND dataset='techindi_model'`，180 行 / 26 波）
- 塔位指纹：`alpha_pyramids` 表
- prod 读法纪律：`Claude/skills/wq-prod-corr-read/SKILL.md`（族代表预判 + 排队顺序）
- self ≠ prod 机理：`Claude/skills/wq-prod-lever-self-lock-guard/SKILL.md`
