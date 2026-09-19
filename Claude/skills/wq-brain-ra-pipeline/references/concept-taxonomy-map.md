# 三套概念分类学映射表（dfe 8 问 ↔ GEM 概念位 ↔ hypothesis 12 类）

> 2026-09-12 新增（全量精读 P2-10）。生成链上有三套概念分类学并存，本表建立对应关系，
> 避免同一字段被贴三个互不通气的标签。权威来源：各分类本体定义处。

| 生成问题 | dfe 8 问（brain-data-feature-engineering 第 3 步） | GEM 概念位（brain-make-some-gem 七槽配给） | hypothesis 12 类（brain-alpha-research-hypothesis-first） | 典型表达构造 |
|---|---|---|---|---|
| 不变量/稳定性 | 1 不变 | 稳定性/持续性概念槽 | `slow_diffusion`、`regime` | ts_zscore 长窗、变异系数 |
| 变化/动量 | 2 变化 | 变化率/加速度概念槽 | `propagation`、`urgency` | ts_delta、ts_returns |
| 异常/偏离 | 3 异常 | 异常检测概念槽 | `over_reaction`、`dispersion` | zscore 尾部、signed_power |
| 交互/组合 | 4 交互 | 组合腿（slow×fast spread） | `cross_dataset` | subtract(rank A, rank B) |
| 结构/构成 | 5 结构 | 结构性概念槽 | `information_asymmetry` | 比率、占比 |
| 累积/记忆 | 6 累积 | 累积效应概念槽 | `horizon_spread`、`slow_diffusion` | ts_sum 累积、decay |
| 相对/比较 | 7 相对 | 分组/排名概念槽 | `dispersion` | group_rank / group_zscore |
| 本质/第一性 | 8 本质 | 机制叙事（family 的 mechanism_premise） | `residual`、`regime` | ts_regression 残差、事件门控 |

## 使用规则

1. **一次生成只挂一套主分类**：dfe 产出 ideas 时给每个概念同时标 `dfe_question` 与
   `hypothesis_class`（若该概念将进入假设优先流程）；GEM 七槽消费时按槽位语义取用。
2. **hypothesis-first 切入时**（ra-pipeline 步 2 饱和路由），dfe 的 8 问标签是假设目录
   `hypothesis_class` 字段的候选来源——映射即本表第三、四列。
3. **判重与多样性**：批级 shape 判重（validator.check_batch）认形状签名不认分类学；
   分类学用于概念层多样性（≥3 Expected Exposure / ≥3 字段族）。

## 维护

- 新增假设类/概念槽时**必须**同步本表（三处本体定义 + 本表第 2-4 列）。
- 争议映射以各本体定义处的最新版本为准，本表只是桥。
