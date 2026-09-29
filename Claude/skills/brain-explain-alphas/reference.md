# Alpha 表达式解释工作流（详细版）

> 主 SOP 见 [SKILL.md](SKILL.md)（含真实工具签名、`filter_sharpe=False`、第 7 步概念重叠检查）。本页给成品示例、检索技巧与情景卡。

## 检索技巧（第 2 步展开）

示例调用（**没有 `instrument_type` 参数**；`dataset_id` 必传，未知就传 `None`）：

```
mcp__wq-brain-http__get_datafields(region="ASI", dataset_id=None, universe="MINVOL1M", delay=1, data_type="VECTOR", search="shrt3_bar", filter_sharpe=False)
```

- **尽量给全已知信息**：`region`、`universe`、`delay`、`data_type`；`search` 用完整 field id。
- **迭代检索**：没找到就换参数组合。区域可能有多个 universe（ASI 例：`MINVOL1M`；可用 universe 以 `get_platform_setting_options` / `wqb.config.REGIONS` 为准，不要凭记忆写）。
- **核对数据类型**：MATRIX（每只股票每天一个值）还是 VECTOR（每只股票每天多个值）——决定要不要 `vec_*`。
- **`filter_sharpe=False`**：解释既有 alpha 时必开，否则 Sharpe < 0 的字段被静默过滤（见 SKILL 第 2 步）。

## 成品示例（第 6 步四段）

对 `quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))`（ASI）：

**字段（事实，取自数据集描述）**

| 字段 | 类型 / 数据集 | 描述文字给出的含义 |
|---|---|---|
| `oth423_find` | MATRIX · "Fundamental Income and Dividend Model" | "Find score" |
| `shrt3_bar` | VECTOR · "Securities Lending Files Data" | 评级向量（1–10），表示借入某只股票的意愿强度 |

**解释**

- **思路（Idea）**：（推测）取「个股基本面吸引力」中**不能被卖空需求加权的全国均值解释**的那部分，做横截面分位。
- **数据理由（Rationale for data）**：`oth423_find` 是基本面打分（事实）；`shrt3_bar` 是借券需求评级，常被当作卖空兴趣的代理（事实 + 领域常识）。把两者放在一起，是想让「卖空拥挤度」参与基准的构造（推测）。VECTOR 字段必须先 `vec_max` 聚合（每股每天取最强的一条评级）。
- **算子理由（Rationale for operators）**：`vec_max` 把 VECTOR 聚合成矩阵值 → `group_mean(x, weight, group)` 以该权重在 `country` 内求加权均值，得到「借券需求加权的国家层基准」→ `ts_regression(y, x, 90)` 用 90 日窗口把个股得分对该基准回归（默认取残差，以平台算子文档为准）→ `quantile` 变成横截面分位。
- **进一步启发（结构化 3 栏）**：

| 新概念名 | 候选字段 | 预计与 book 的正交性 |
|---|---|---|
| 「拥挤度残差」：把基本面打分对卖空拥挤基准回归取残差 | 同数据集内其它借券字段（如 `shrt3_*` 系列）；换 group 轴（`subindustry`） | 中——同用 `shrt3_bar`，与 book 内已有借券类 alpha 可能同族，先跑第 7 步 |

**收益来源证据**：写之前先取 `get_alpha_yearly_stats`（哪几年贡献了收益）与 `get_alpha_pnl`（曲线形状）；long / short 侧与行业集中度没有直接接口，写「未核验」。**注意**：`country` 作 group 在部分区域无效（`region_invalid_group_fields`，如 JPN 的 sector / subindustry / industry），换区域复用这个例子前先核对。

## 情景卡

### 卡 EX-1　Mode B 换概念前查概念重叠

- **前置状态**：本区 book 有 3 颗 ACTIVE alpha——A1 `rank(ts_zscore(snt21_pos_mean, 66))`、A2 `group_rank(ts_delta(fnd28_ebit, 22), industry)`、A3 `rank(ts_zscore(divide(snt21_pos_mean, snt21_pos_max), 22))`；想换成的新概念是 `rank(ts_zscore(snt21_pos_max, 252))`。
- **步骤**：`$WQ_PY tools/concept_overlap.py --region <REGION> --expr "rank(ts_zscore(snt21_pos_max, 252))"`（book 取自 `alphas` 表 ACTIVE 行；库空 / 不可读就改用 `--book-json`）。
- **预期**：`verdict: HIGH`——A3 与新概念**同骨架**（`rank→ts_zscore`）且字段 Jaccard = 0.5（共享 `snt21_pos_max`）；A1、A2 无共享字段不出现。建议 = 换概念。
- **分支**：`MEDIUM`（例：把新概念换成 `rank(ts_rank(snt21_pos_max, 66))`——骨架不同、Jaccard 仍 0.5）→ 可继续，但优先换字段 / 骨架，提交前必测 SELF / PROD；`CLEAR` → 概念基本不同，仍须实测相关性。
- **完成定义**：给出 `verdict` 与重叠清单，并把「继续 / 换概念」写进本轮日志。
- **反例**：把 `HIGH` 当成 SELF / PROD 一定超线的证据（它只是启发式）；把 `CLEAR` 当成可以跳过相关性实测。

### 卡 EX-2　战略级候选提交前确认收益来源

- **前置状态**：候选已过 `Failed RA == 0`，用户要在提交前确认「收益从哪来」。
- **步骤**：按第 6 步四段写解释；证据取 `get_alpha_yearly_stats`（逐年）与 `get_alpha_pnl`（曲线）；把下面三条**警示信号**逐条对照并如实写「命中 / 未命中 / 未核验」：① 收益集中在某 1 个行业（无直接接口 → 多半「未核验」）；② 收益集中在某 1 年（逐年 Sharpe 一年独大）；③ 收益集中在 1 侧（long 或 short，无直接接口 → 多半「未核验」）。
- **分支**：② 命中 → 交 `brain-alpha-robustness`（其 Phase C 近窗判据才是判定，本卡只提示）；「未核验」项不得被写成「通过」。
- **完成定义**：三条警示信号各有状态，且每个「命中」附证据来源（工具 + 数据）。
- **反例**：靠自由发挥的叙事替代证据；把解释当作提交理由（解释不构成放行）。

## 故障排查

- **SSL 错误**：跑访问互联网的脚本时若遇到 `CERTIFICATE_VERIFY_FAILED`，先检查代理 / CA 设置（云端环境见其网络策略说明），**不要**关闭 TLS 校验。
- **`get_datafields` 返回空**：先确认 `filter_sharpe=False`，再按 SKILL 第 2 步的排查顺序走。

## 附录 A：理解 Vector 数据

Vector 数据是特殊的数据字段类型：每个工具每天记录的事件数量可以变化，与 matrix 数据（每个工具每天只有一个值）相对。例如新闻情绪通常是 vector——一只股票一天可能有多篇新闻。要在大多数算子中使用，必须先经 vector 算子聚合成单一值（`vec_avg` / `vec_sum` / `vec_max` …，全集见 SKILL 附录）。
