# Alpha 自相关与 PPAC 相关性计算器 — 参数与产物

> 主 SOP、SELF/PROD 区别、结构性盲区与判读决策表见 [SKILL.md](SKILL.md)。本页只写脚本 `scripts/skill.py` 的参数、产物、依赖与注意事项。
> 脚本把两套本地相关性算法合成一个入口：**SelfCorr**（对比池 = 已提交且**不含** Power Pool 的 OS alpha）与 **PPAC**（对比池 = 仅 Power Pool alpha）。

## 参数

| 参数 | 含义 | 缺省 |
|---|---|---|
| `--start-date` / `--end-date` | 候选的**创建日期**区间，`MM-DD`，年份取**当年**（美东时间）。被测对象 = 你自己 `UNSUBMITTED` / `IS_FAIL` 的 alpha（非 SUPER、非隐藏），**不是**已提交池 | `01-10` / `01-11` |
| `--region` | 市场区域（如 `IND` / `USA` / `EUR`） | `IND` |
| `--sharpe-threshold` / `--fitness-threshold` | 候选的 `is.sharpe` / `is.fitness` **下限**（`>`）。缺省 `-1.0` = **实际不过滤**（先取全部，再由下面的 `Check OK` 判定筛） | `-1.0` |
| `--alpha-num` | 最多取回多少个候选（每页 100 个） | `100` |
| `--max-workers` | 相关性计算并发数 | `5` |
| `--out-dir` | 缓存池与 Excel 的目录 | `$WQ_SELFCORR_OUT_DIR` → 仓库内 `data/selfcorr_quick/` |
| `--output` | Excel 文件名（不带目录时落在 `--out-dir`） | `alpha_results_<start>_<region>.xlsx` |
| （旧）命令行邮箱 / 口令参数 | 仅为兼容旧用法保留，**口令那个不推荐**（进进程列表 / shell 历史，使用时脚本会告警）。凭据请走环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（旧别名 `BRAIN_USERNAME` / `BRAIN_PASSWORD` 仍认） | — |

## 运行

```bash
$WQ_PY -m pip install -r Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/requirements.txt   # 一次性
$WQ_PY Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py --start-date 09-28 --end-date 09-29 --region KOR
```

`$WQ_PY` 是 MCP venv 的解释器（`python tools/_pyenv.py` 打印其路径）。缺依赖时脚本在非交互环境**只打印**可复制的 `pip install` 命令并退出，不会自己安装、也不会等键盘输入。

## 脚本做了什么

1. 用环境变量里的凭据登录 BRAIN API；
2. 按日期区间 / 区域 / 阈值取回**候选**（`UNSUBMITTED` / `IS_FAIL`），只保留 `Check OK` 者（平台 `is.checks` 无 FAIL 且 `longCount + shortCount > 100`）；
3. 增量下载 / 读取**已提交（OS）alpha 的 PnL 池**（缓存在 `--out-dir`；首次运行下载历史数据，之后每次只补最近的）；
4. 逐个候选计算 SELF（对 SelfCorr 池）与 PPAC（对 Power Pool 池）相关性；
5. 写 Excel 与终端摘要，并给出池新鲜度与（本地 SELF 偏低时的）盲区警告。

## 产物

- **`Alpha Results` sheet**：`alpha_id`、`exp`（表达式）、`check_status`（`Check OK`：平台检查无 FAIL 且 long+short > 100——**不是**相关性结论）、`Rank`（按 Sharpe）、`sharpe`、`self_correlation`、`ppac_correlation`、`turnover`、`fitness`、`margin`、`dateCreated`、`longCount`、`shortCount`、`decay`、`neutralization`、`neutralization_name`。
- **`Meta` sheet**：`pool_last_refreshed`（缓存池文件最后刷新时间）、`pool_alpha_count`（池内 alpha 数）、`generated_at`、`region`、日期区间与盲区提示。
- **终端**：前 10 个结果、SELF / PPAC 的均值 / 最大 / 最小、中性化设置分布；本批本地 SELF 最大值 < 0.7 时打印 `[盲区警告]`。

## 依赖

`requests`、`pandas`、`numpy`、`tqdm`、`openpyxl`（写 `.xlsx` 需要）；版本下限见 `scripts/requirements.txt`。`tqdm` 缺失时脚本仍能运行（无进度条）。

## 注意

1. 日期格式 `MM-DD`，年份取当年；
2. 缓存池与 Excel 在**固定目录**（见上），不再随 CWD 走；旧版留在别处的 `*.pickle` 不会被读取，首次运行会重新下载一次；
3. 长时间运行有进度条；
4. SELF 与 PPAC 分别对各自的池计算，两个结论**不能互相推导**；
5. 本页的相关性是**本地估算**：低值不可当作放行依据（SKILL 的「结构性盲区」），提交前必须平台实测。
