# 论坛 Alpha 模板库（2026-08-04 沉淀）

来源：BRAIN-CN 论坛实证帖（日期 + 帖子 ID 标注）。所有模板在使用前必须过 `get_operators` 签名验证（本库已标注平台签名坑）。

## A. 设计模式 4 模板（forum 41379941061143, 2026-06-21）

| # | 模板 | 经济含义 | 适用 |
|---|---|---|---|
| A1 | `zscore(winsorize(pasteurize(F), std=4.0))` | 鲁棒标准化输入：去噪声→去极值→横截面均匀 | 原始噪声大/厚尾字段 |
| A2 | `group_neutralize(winsorize(F), group)` | 横截面相对价值：剔除行业/板块风险留特质超额 | 行业因子、板块联动强字段 |
| A3 | `ts_decay_linear(F, d, dense=true) - ts_delay(F, d)` | 智能加权趋势：线性衰减近期权重 vs 简单滞后，捕捉趋势加速 | 趋势/动量类 |
| A4 | `ts_zscore(F, d)` | 波动率调整均值回归：偏离历史均值的标准化 | 均值回归类 |

**签名坑**：A1 的 `winsorize` 第二参为命名参数 `std=`（位置传参平台报错，2026-08-03 实测）；A3 的 `dense` 为命名参数。

## B. 算子分类模板体系（forum 大模板拆分帖, 2025-12-09）

将 TS 算子按职能分类后组合，每个模板有明确经济含义（原文 8000 空间 → 1240 有义空间）：

| 模板 | 结构 | 经济含义 |
|---|---|---|
| B1 动量加速 | `{diff}({diff}(F, d1), d2)` | 趋势加速/减速 |
| B2 标准化动量 | `{norm}({diff}(F, d1), d2)` | 对动量信号排序/标准化 |
| B3 聚合信号 | `{agg}({norm}(F, d1), d2)` | 对标准化信号平滑/时间衰减 |
| B4 位置信号 | `{pos}({inner}(F, d1), d2)` | 极端值相对聚合信号的位置 |

- diff（差分/变动）：`ts_delta`、`ts_av_diff`
- norm（归一化/排序）：`ts_rank`、`ts_zscore`、`ts_std_dev`
- agg（窗口聚合）：`ts_sum`、`ts_decay_linear`
- pos（位置/索引）：`ts_arg_min`、`ts_arg_max`、`ts_delay`

**反模式（无意义组合，勿用）**：
- `ts_arg_min(ts_arg_max(...))` — timing-of-timing 无意义
- `ts_rank(ts_zscore(...))` — 重复标准化
- `ts_corr` 单参 — 需要两个序列（平台签名：ts_corr(x, y, d)）

## C. 变异系数模板（forum 35243125531671, 2025-09-27）

`1/ts_ir(x, d)` — 变异系数（std/mean）的无量纲离散度，用 ts_ir 间接实现。
适用：低频更新数据（analyst/fundamental）的波动稳定性信号。注意低频数据 CV 不稳定。

## D. 动量/反转模板（forum 35771635460247, 2025-10-21，出信号率非常高）

`(+/-)ts_max_diff/ts_av_diff(<norm>(F), day)`

- `+` 动量：势头好→延续；`-` 反转：势头过好→逆转
- 与过去窗口最大值/均值比较判断势头
- norm 可选：log/signed_power（算术）、ts_zscore/ts_mean（平滑）、rank/quantile（横截面）
- 在 analyst/fundamental/model 数据集均验证有效（基本面/收益/量价指标信号明显）
- 扩展：比较 std_dev/ir/delta 而非原始值
- **已知痛点**：高 turnover 低 margin（与本项目 KOR/GLB 实测一致——需 decay/长窗修正）

## E. 双数据集混信号模板（forum IND 情感帖, 2025-12-09）

双数据集信号混合（论坛称"混信号"）：适合新手/断粮/点塔场景。
与本项目 KOR 实测呼应：跨数据集 blend（add/subtract）在 KOR 上产出达标候选（JjGwjd5E = analyst39×pv106），前提是两腿正交（不同类别）；同数据集族内 blend 无效（pv106 族内全灭）。

## 使用规则

1. 每个模板代入字段前，先本地 `check_batch` 校验 + 确认算子签名（命名参数坑：winsorize std=、ts_decay_linear dense=、hump hump=、ts_backfill lookback=）
2. B 体系模板空间大（1240+），优先按经济含义定向生成，不要全空间枚举
3. D 模板高 turnover 信号必须配 decay≥12 或长窗（本项目 GLB 实测 decay16+250 窗解决 margin）
4. 模板与数据集匹配度：先查 WebDataScope 数据体检（分布形状/频率）再选模板族
