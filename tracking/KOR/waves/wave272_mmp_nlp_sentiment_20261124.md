# Wave 272 · mmp_nlp_sentiment 白空间筛查（2026-11-24）

## 波次三问（发波前）

1. **继承**：Insiders/Institutions 线关闭（塔满/机制穷尽）；KOR 唯一有先验的 news 轴是 revision/surprise，情绪水平轴已全区证伪（≤0.41）。
2. **准入**：本波只测 OTHER 单集 ATOM；禁 PV/MODEL/OTHER 组腿；禁情绪水平裸 rank（已知死）；不扫 decay 单独轴 / truncation / universe（KOR 死轴）。
3. **收窄**：首批 8 探针（revision/surprise 轴为主 + 2 条水平对照）；胜出者才进梯度层。

## 设置

KOR / TOP600 / D1 / STATISTICAL / decay 4 / trunc 0.08 / nanHandling OFF / pasteurization ON / unitHandling VERIFY。
平台硬窗 2014-2023（test_period 缺省）。

## 批次台账

| 批次 | multisim id | 臂数 | 内容 | 状态 |
|---|---|---|---|---|
| B1 | `31bWcI2Fh5cL95z1a2Dj7Cm3` | 2 | 情绪水平对照 | **死批**：progress 冻结 0.15 / children=0 约 45min；auth+quota 均正常 ⇒ 判平台队列死批，按 playbook 重派 |
| B1' | `4eix316ew59GcdSGK8alAlJ` | 8 | 合并 B1+B2：bullish/bearish/downgrade/raise_pt×2/buy-sell 价差/ts_delta×2 | 在飞（ETA ~5min） |

## 探针读数

### B1-diag（干净 2 臂，成功收割；确认「堆叠批次=资源争抢→全批 ERROR」）

| 臂 | 字段/形态 | alpha id | S | F | 2Y | subU | TO | raF | verdict |
|---|---|---|---|---|---|---|---|---|---|
| L1 | `group_rank(avg_bullish_topic_score, sector)` | d5aMoEzj | **0.05** | 0.00 | **−0.54** | 0.22 | **1.4132** | 5 | REJECT（CW 1.0 + 高 TO + 稀疏 ~115 名）|
| L2 | `group_rank(bearish_topic_sum_bbgnews, sector)` | 58Jmea5X | **0.04** | 0.00 | 0.32 | 0.16 | 0.3873 | 3 | REJECT |

**结论**：情绪/话题**水平轴**在 KOR 完全无定价力（S≈0），与 KOR 既有 prior「news 情绪水平四集 ≤0.41、
sentiment26 max|S| 0.20」一致；且 cov 1.0 的字段实际横截面只有 ~115/199+416 名 ⇒
「声明覆盖 ≠ 有效截面」再次复现（同 macro63 / 区域命名字段陷阱）。**水平轴整族关闭，不再投。**

### 工程教训（重要）

同时派发 4 个 multisim（违反 ≤1-in-flight）直接导致：3 批冻结 progress 0.15 / children=0，
1 批 8 臂全 ERROR（"error while running the simulation"）；改为单批 2 臂后立即成功收割。
⇒ **队列拥塞的根因是自身超发，不是平台或表达式**；已按用户「每批≤8、一批收完再派下一批」执行。

### B2（revision/surprise 8 臂，在飞 `2elshh2095hs8AjFjK7Ks96`）

收割后填。

## 梯度 Δ 表（胜出后填）

按 `tools/research/operator_swap_matrix.py` 逐层同类别全替换；KOR 禁 `ts_ir` / `ts_target_tvr_hump`。

## 归因（胜出后填）

`get_alpha_yearly_stats`（逐年 S、S<1.0 年份占比、top1 年占比）+ `get_alpha_pnl`（阶梯 vs 尖峰、停滞段）。
