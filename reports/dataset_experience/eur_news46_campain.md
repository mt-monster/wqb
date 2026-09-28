# EUR · news46 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：EUR / news46；波次 245；去重后 5 条已完成回测，5 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=245,246,247,248,249,250。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOPCS1600 | SUBINDUSTRY | 4 | 0.08 | 2014-01-01 | 2023-12-31 |

最高 Sharpe 候选：`KPNmK6ON`，Sharpe=0.42，同条 Fitness=0.13，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `mws46_ravenpack_mean_ens` | MATRIX / 0.6975 / 1 | Mean Event Novelty Score (0–100) indicating how new or unique the news is within a 24-hour window across stories in the  | 2 | -0.01 / 0 (`omLo1v62`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `mws46_ravenpack_mean_ess` | MATRIX / 0.6975 / 16 | Mean Event Sentiment Score (0–100) measuring news sentiment for the entity based on proxies sampled from news; values ab | 1 | -0.46 / -0.15 (`wpZ981Yd`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `mws46_ravenpack_mean_nip` | MATRIX / 0.9081 / 12 | Mean News Impact Projections score (0–100) estimating the short-term market impact of associated news over the next two  | 1 | -0.19 / -0.04 (`vRrOK9ra`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `mws46_ravenpack_mean_relevance` | MATRIX / 0.9081 / 10 | Mean relevance score (0–100) indicating how central the entity is to the news; 100 means the entity is a primary focus | 1 | 0.33 / 0.1 (`LLN5P6N9`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `mws46_ravenpack_mean_ssc` | MATRIX / 0.9081 / 9 | Mean Composite Sentiment Score (0–100) summarizing the overall news tone for the entity by combining multiple sentiment  | 3 | 0.42 / 0.13 (`KPNmK6ON`) | 仅为所列搭配中的结果；不能推断独立贡献 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 245 | `KPNmK6ON` | 0.42 | 0.13 | 0.36 | 10.46 | 0.42 | 0.26 | 未核实 | 未核实 |
| 245 | `LLN5P6N9` | 0.33 | 0.1 | 0.96 | 7.63 | 0.72 | 0.52 | 未核实 | 未核实 |
| 245 | `omLo1v62` | -0.01 | 0 | -0.45 | 7.76 | 0.19 | 0.17 | 未核实 | 未核实 |
| 245 | `vRrOK9ra` | -0.19 | -0.04 | 0.6 | 8.29 | -0.4 | -0.24 | 未核实 | 未核实 |
| 245 | `wpZ981Yd` | -0.46 | -0.15 | -1.04 | 6.03 | -0.54 | -0.32 | 未核实 | 未核实 |

### 原式与局部失败证据

**KPNmK6ON（wave 245）**

```text
rank(ts_delta(ts_backfill(mws46_ravenpack_mean_ssc,252),252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**LLN5P6N9（wave 245）**

```text
subtract(rank(ts_backfill(mws46_ravenpack_mean_ssc,252)),rank(ts_backfill(mws46_ravenpack_mean_relevance,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**omLo1v62（wave 245）**

```text
rank(ts_delta(ts_backfill(mws46_ravenpack_mean_ens,252),252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**vRrOK9ra（wave 245）**

```text
subtract(rank(ts_backfill(mws46_ravenpack_mean_nip,252)),rank(ts_backfill(mws46_ravenpack_mean_ssc,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**wpZ981Yd（wave 245）**

```text
subtract(rank(ts_backfill(mws46_ravenpack_mean_ens,252)),rank(ts_backfill(mws46_ravenpack_mean_ess,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

复盘日期：2026-09-24。范围是本任务新增 wave245，不能代表整个 news46 的全部可能性。5 条全部完成，0 个合格 Regular；已把本轮机制写入 `EUR-W245-news46-mechanisms-D1`，未判死整套数据。

### 输入、处理和输出

S0/S1 扫描 30 字段（19 VECTOR、11 MATRIX），本轮实际使用表中的 5 个 MATRIX 均值字段。固定 EUR / TOPCS1600 / D1 / SUBINDUSTRY / decay4 / truncation0.08 / maxTrade ON / nanHandling ON，FULL 2014–2023。coverage/users 是本次 S1 目录快照，不是永久属性。

现有画像约束促使本轮使用 252 日回填和年度变化；这只是本轮预处理选择，不代表新闻的最佳预测周期。GEM 原式 5 条通过语法、类型和体检门后实际回测。初始概念文档还有 3 个 sum 字段门控比率，没有进入这 5 条回测，不能据本轮给它们判失败。

| 字段或组合 | 本轮检验的经济问题 | 实测结论 | 可复用经验 |
|---|---|---|---|
| `mean_ssc` 年度变化 | 综合语气改善是否缓慢反映到股价 | S .42 / F .13 / 2Y .36 | 本轮最强仍远低于 Mode B 资格；不继续扫 decay/窗口 |
| `mean_ssc` − `mean_relevance` 的排序差 | 相对新闻关注程度的语气是否包含额外信息 | S .33 / F .10；Sub .72 但 Robust .52 | 一个子宇宙指标较高不能补救整体弱信号；相关度与情绪是不同量纲，排序差只是待验证机制 |
| `mean_ens` 年度变化 | 新颖度变化是否标记新的信息状态 | S −.01 / F 0 | users=1 只说明使用少，不能推断有收益 |
| `mean_nip` − `mean_ssc` | 预计影响与综合语气是否背离 | S −.19 / F −.04 | 影响大小不是方向；直接相减在本设置中不成立 |
| `mean_ens` − `mean_ess` | 高新颖度、较低乐观语气是否提供未兑现信息 | S −.46 / F −.15 | 方向与原假设相反且绝对强度不足；不能凭翻转就视为强候选 |

### 失败边界与下一次决策

本波 max Sharpe=.42、max |Sharpe|=.46，没有任何候选达到 S≥1.25 且 F≥.8 的继续优化资格。因此停止这五种结构，不放入救援增强波，不花相关性配额为弱信号背书。Prod/Self 没有核实，不能写成“低相关”。

**推论，尚未证实**：年度回填可能使短期新闻信息变旧，跨故事均值也可能掩盖事件差异。但本轮没有短周期对照和原始事件归因，不能把失败归因成确定的“新闻已失效”。重新开启需新的事件时点/更新频率证据和不同机制；此前未回测的 sum 字段仍要独立做类型、事件门控与覆盖核查。

### 生成与复用注意

- MATRIX 与 VECTOR 不能按相似后缀互换；名字相近不等于相同时间含义。
- 初轮自动表达式存在语义误绑定和低频字段短窗口问题，已剔除；自动附加模板不是新的经济概念。
- 仅保留已测原式和上述有限结论，下一轮不得把这份文档当作整个 news46 的永久黑名单。

来源：DB `review_245`、`s6_verdict_245`、`catalog_news46`、wave245；机制原稿见 `reports/eur_d1_20260924_news46_mechanisms.md`。
