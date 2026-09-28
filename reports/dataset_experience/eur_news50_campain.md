# EUR · news50 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：EUR / news50；波次 246；去重后 8 条已完成回测，11 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=245,246,247,248,249,250。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOPCS1600 | SUBINDUSTRY | 4 | 0.08 | 2014-01-01 | 2023-12-31 |

最高 Sharpe 候选：`O0NJ152b`，Sharpe=0.32，同条 Fitness=0.08，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `mws50_acb` | VECTOR / 0.7863 / 5 | Score representing sentiment according to the corporate actions classifier | 1 | 0.15 / 0.03 (`kqoJxLY6`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_aes` | VECTOR / 0.7863 / 6 | Score from 0 to 100 measuring the ratio of positive to total non-neutral events over a rolling 91-day window within the  | 1 | 0.32 / 0.08 (`O0NJ152b`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_bam` | VECTOR / 0.7863 / 3 | Score representing sentiment according to the mergers and acquisitions classifier | 1 | 0.16 / 0.03 (`WjbLEWxO`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_bee` | VECTOR / 0.7863 / 0 | Earnings evaluations sentiment score from the BEE classifier | 1 | 0.22 / 0.05 (`RRbAJkoa`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_ber` | VECTOR / 0.7863 / 0 | Earnings releases sentiment score from the BER classifier specialized in earnings release news | 1 | 0.22 / 0.05 (`RRbAJkoa`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_ess` | VECTOR / 0.7863 / 5 | Granular sentiment score from 0 to 100 for the entity in the story; higher values indicate more positive short-term fina | 1 | -0.52 / -0.17 (`e7b6lqZl`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_ghc_lna` | VECTOR / 0.7863 / 0 | Score representing changes in analyst recommendations | 1 | -0.42 / -0.14 (`9qjEzA3x`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_nip` | VECTOR / 0.7863 / 0 | News Impact Projections score (0–100) estimating market impact over the following two hours, conditional on time of arri | 1 | -0.52 / -0.17 (`e7b6lqZl`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_qcm` | VECTOR / 0.7863 / 1 | Multi-classifier for equities sentiment score combining outputs from BMQ, BEE, BCA, and ANL-CHG, applied to the most rel | 1 | -0.5 / -0.18 (`npdA1O5w`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_ssc` | VECTOR / 0.7863 / 4 | Composite sentiment score from 0 to 100 representing overall story sentiment | 3 | 0.31 / 0.08 (`rKOd1rM9`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mws50_vea` | VECTOR / 0.7863 / 1 | Aggregate Event Volume over the past 91 days for an entity, counting non-neutral events (ESS ≠ 50) from qualifying news  | 1 | 0.31 / 0.08 (`rKOd1rM9`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 246 | `O0NJ152b` | 0.32 | 0.08 | -0.74 | 4.18 | 0.26 | -0.1 | 未核实 | 未核实 |
| 246 | `rKOd1rM9` | 0.31 | 0.08 | 1.05 | 6.78 | 0.25 | 0.11 | 未核实 | 未核实 |
| 246 | `RRbAJkoa` | 0.22 | 0.05 | 0.62 | 12.76 | -0.1 | -0.07 | 未核实 | 未核实 |
| 246 | `WjbLEWxO` | 0.16 | 0.03 | -0.24 | 7.88 | 0.01 | -0.41 | 未核实 | 未核实 |
| 246 | `kqoJxLY6` | 0.15 | 0.03 | 1.01 | 12.73 | 0.09 | -0.09 | 未核实 | 未核实 |
| 246 | `9qjEzA3x` | -0.42 | -0.14 | -1.19 | 9.29 | -0.58 | -0.1 | 未核实 | 未核实 |
| 246 | `npdA1O5w` | -0.5 | -0.18 | -1.43 | 9.73 | -0.45 | 0.02 | 未核实 | 未核实 |
| 246 | `e7b6lqZl` | -0.52 | -0.17 | 0.61 | 8.57 | -0.5 | -0.89 | 未核实 | 未核实 |

### 原式与局部失败证据

**O0NJ152b（wave 246）**

```text
group_rank(ts_backfill(vec_avg(mws50_aes),252),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**rKOd1rM9（wave 246）**

```text
trade_when(greater(ts_delta(ts_backfill(vec_avg(mws50_vea),252),252),0),rank(ts_backfill(vec_avg(mws50_ssc),252)),-1)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**RRbAJkoa（wave 246）**

```text
subtract(rank(ts_backfill(vec_avg(mws50_bee),252)),rank(ts_backfill(vec_avg(mws50_ber),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**WjbLEWxO（wave 246）**

```text
group_rank(ts_backfill(vec_avg(mws50_bam),252),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**kqoJxLY6（wave 246）**

```text
rank(ts_delta(ts_backfill(vec_avg(mws50_acb),252),252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**9qjEzA3x（wave 246）**

```text
subtract(rank(ts_backfill(vec_avg(mws50_ghc_lna),252)),rank(ts_backfill(vec_avg(mws50_ssc),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**npdA1O5w（wave 246）**

```text
subtract(rank(ts_backfill(vec_avg(mws50_qcm),252)),rank(ts_backfill(vec_avg(mws50_ssc),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**e7b6lqZl（wave 246）**

```text
subtract(rank(ts_backfill(vec_avg(mws50_nip),252)),rank(ts_backfill(vec_avg(mws50_ess),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

复盘日期：2026-09-24。范围是本任务新增 wave246；8 条全部完成，0 个合格 Regular。已封存本轮机制 `EUR-W246-news50-mechanisms-D1`，未判死整个数据集。

### 输入、处理和输出

S1 扫描 37 个字段，全部 VECTOR；实际使用 11 个字段，users 均≤9。统一先 `vec_avg` 转成 MATRIX，再 252 日回填；这会丢失向量内部离散度，本轮没有验证离散度信号。settings 为 EUR / TOPCS1600 / D1 / SUBINDUSTRY / decay4 / truncation0.08 / maxTrade ON / nanHandling ON，FULL 2014–2023。

有完整本地体检包，8/8 原式通过本轮语法、类型及画像门，体检违规为0；这证明输入合规，不证明有 alpha。

| 字段或组合 | 机制与字段角色 | 实测 S / F / 2Y | 字段级经验 |
|---|---|---|---|
| `mws50_aes` | 91 日滚动正面/非中性事件比例，行业内排序 | .32 / .08 / −.74 | 正面事件比例的“状态”不是瞬时新闻；全样本略正不代表近两年有效 |
| `mws50_vea` → `mws50_ssc` | 91 日事件量年度增加为更新条件，综合语气为主信号 | .31 / .08 / 1.05 | 门控比裸方向多一层条件，但没有达到增强资格；不能继续堆条件 |
| `mws50_bee` − `mws50_ber` | 盈利评价与盈利发布的分类器排序差 | .22 / .05 / .62 | 两个 users=0 字段也未带来有效预测；冷门仅是搜索先验 |
| `mws50_bam` | 并购情绪分类器行业内排序 | .16 / .03 / −.24 | 特定事件类别并不自动形成独立 alpha；此简单状态结构淘汰 |
| `mws50_acb` | 公司行动分类器年度变化 | .15 / .03 / 1.01 | 原稿称季度修订，但实际是252日变化；经验以实际表达式为准 |
| `mws50_ghc_lna` − `mws50_ssc` | 分析师评级变动新闻与综合语气差 | −.42 / −.14 / −1.19 | 同向改善的假设未成立；并未证明评级修订字段整体无效 |
| `mws50_qcm` − `mws50_ssc` | 股票多分类器与综合语气差 | −.50 / −.18 / −1.43 | 分类器可能共享信息，排序差未显示有效增量；共享程度尚未做原始数据检验 |
| `mws50_nip` − `mws50_ess` | 预计市场影响与细粒度语气差 | −.52 / −.17 / .61 | NIP 描述指未来两小时影响，当前 D1＋慢窗口存在时间尺度疑问；这是研究线索而非已证实原因 |

### 失败边界与下一次决策

max Sharpe=.32、max |Sharpe|=.52，8条无一达到 S≥1.25 且 F≥.8，因此不进入 Mode B、参数扫描或组合救援。Prod/Self 未测，不得把缺失当成通过。

若重启，应先拿到事件时间、VECTOR 内部结构和实际更新频率的证据，检验“哪些事件被均值聚合抹去”，再定义不同机制。当前用户仅允许 D1；不能把 D0 试验当作本任务的修复方案。没有新证据时跳过这八种结构。

### 可复用的工程经验

- `vec_avg` 是本轮类型转换，不等于最佳聚合；不可把向量字段直接喂给 MATRIX 算子。
- 编号、标签、时间、类别字段不能因为是数字就作为经济信号。
- 冷门预算、多样性和画像门都通过，仍可能整波弱；先看同条候选的强度，再决定后续成本。
- 初始自动模板及短窗错配已经剔除，不计入8条实际实验。

来源：DB `review_246`、`s6_verdict_246`、`catalog_news50`、wave246；机制原稿见 `reports/eur_d1_20260924_news50_mechanisms.md`。
