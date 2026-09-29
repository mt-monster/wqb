# 三套概念分类学映射表（dfe 8 问 ↔ GEM 概念位 ↔ hypothesis 12 类）

> 2026-09-12 新增，2026-09-29 补全（skills 审查 RT-01 ~ RT-05）。生成链上有三套概念分类学并存，本表建立对应关系，
> 避免同一字段被贴三个互不通气的标签。权威来源：各分类本体定义处；本表只是桥。
> **一致性有测试守**：`tests/unit/test_concept_taxonomy_map.py` 断言 hypothesis-first 的 12 个类名都出现在本表里（新增类必须同步本表）。

| 生成问题 | dfe 8 问（brain-data-feature-engineering 第 3 步） | GEM 概念位（brain-make-some-gem；旧称「七槽配给」——与**波内配额**、**并发令牌**是三个东西） | hypothesis 12 类（brain-alpha-research-hypothesis-first） | 典型表达构造 |
|---|---|---|---|---|
| 不变量 / 稳定性 | 1 不变 | 稳定性 / 持续性概念位 | `slow_diffusion`、`regime` | `ts_zscore` 长窗、变异系数 |
| 变化 / 动量 | 2 变化 | 变化率 / 加速度概念位 | `propagation`、`urgency`、`under_reaction` | `ts_delta`、`ts_returns` |
| 异常 / 偏离 | 3 异常 | 异常检测概念位 | `over_reaction`、`dispersion` | zscore 尾部、`signed_power` |
| 条件 / 分组 / 对偶价差（**不是腿相加**） | 4 交互 | 条件 / 分组概念位（旧称「组合腿」） | `cross_dataset`、`event_conditional` | `trade_when(慢开关, …)`、`group_rank` 分组、**同源**对偶价差 `subtract`（见下） |
| 结构 / 构成 | 5 结构 | 结构性概念位 | `information_asymmetry` | 比率、占比 |
| 累积 / 记忆 | 6 累积 | 累积效应概念位 | `horizon_spread`、`slow_diffusion` | `ts_sum` 累积、`decay` |
| 相对 / 比较 | 7 相对 | 分组 / 排名概念位 | `dispersion` | `group_rank` / `group_zscore` |
| 本质 / 第一性 | 8 本质 | 机制叙事（family 的 `mechanism_premise`） | `residual`、`regime` | `ts_regression` 残差、事件门控 |

> **第 4 行的落地边界（RT-04）**：「交互 / 组合」概念位**只能落成条件 / 分组 / 对偶价差**——第二个数据集只能提供**条件、分组或残差**，不得作为并列信号项相加（CLAUDE.md「禁止混信号调参」；允许形态与辅助腿入场三式见 [`step7-diagnose.md`](step7-diagnose.md) §7.7）。`subtract` 仅在两腿是**同一经济量的对偶两侧且同数据集**时才算价差；跨集 `subtract` 被闸 5 `spread_cross_dataset` 拦。
> `under_reaction`（反应不足 → 漂移 / 动量延续）放在「变化 / 动量」行；`event_conditional`（事件条件）放在第 4 行——它的落地就是 `trade_when` 门控。

## 使用规则

1. **一次生成只挂一套主分类**：dfe 产出 ideas 时以 `dfe_question` 为**主分类**；`hypothesis_class` 作**副标签**（仅当该概念将进入假设优先流程）。GEM 消费时按概念位语义取用。
2. **hypothesis-first 切入时**（饱和数据集路由，见 [`step2-s0.md`](step2-s0.md)），dfe 的 8 问标签是假设目录 `hypothesis_class` 字段的候选来源——映射即本表第三、四列。
3. **判重与多样性**：批级判重的执行口径是 gate.py **闸 6** `check_batch_diversity`（见 [`step5-gates.md`](step5-gates.md) §5.4），它认形状 / exposure，不认分类学；分类学用于概念层多样性（≥ 3 个 Expected Exposure / ≥ 3 个字段族）。`wqb.expression.validator.check_batch` 只作方法论参考（零调用方），**不构成判重机制**。

## 维护

- 新增假设类 / 概念位 / 8 问时**必须**同步本表（三处本体定义 + 本表第 2–4 列）；`tests/unit/test_concept_taxonomy_map.py` 只守「hypothesis-first 的类名 ⊆ 本表」这一条，其余靠人。
- 争议映射以各本体定义处的最新版本为准。
