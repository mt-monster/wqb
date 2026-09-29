# 资格门：WebDataScope「Failed RA / Failed PPA」口径

> **用途 / 适用步骤**：步 8（提交判定）的**研究侧硬前置**——进入提交流程前，从 `is.checks` 算出 Failed RA / Failed PPA，非零就回步 7 修，不进入提交。步 1 的库存篮子敲定用同一口径。
> **实现只有一份**：`src/wqb/config.py::compute_webdata_failed_counts`（名单 `RA_CHECK_NAMES` 18 项 / `PPA_CHECK_NAMES` 7 项）。本文只写口径与边界，**名单以代码为准**——手工按本文数会漏项（RF-01：旧版名单缺 `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`，漏计时 23 条「零硬闸失败」候选里误放 3 条）。测试 `tests/unit/test_r3_failed_count_single_source.py` 断言 `world-quant-brain-mcp/mcp_core.py` 里 Docker 镜像用的冻结副本与它一致。
> 来源：平台插件 WebDataScope 的 `getAlphaCheckStates`（`config.py` 注释记的是 0.10.20；插件代码在仓外，无法在本仓库复核，以 `config.py` 注释为准）。

## 1. 口径

- **REGULAR 候选**：`Failed RA == 0`；**PPA 候选**：`Failed PPA == 0`。
- **一项 check 计入失败 ⇔ `result` 既不是 `PASS` 也不是 `PENDING`**（`WARNING` / `ERROR` / 缺失都算）。这比只看 `result == "FAIL"` 严格。
- **PPA 另计**：`LOW_SHARPE` 的 `value < 1` 计入 Failed PPA，不论它显示什么状态。RA 侧对 `LOW_SHARPE` **只认 `result`**，不看 `value`（RF-04）。
- 不得用用户临时给的指标阈值替代资格门：Sharpe / Fitness / 2Y / ProdCorr / SelfCorr 再漂亮，只要相关 failed 计数非零，候选就是无效的。
- 枚举每个被计入的项的 `name` / `limit` / `value`（`compute_webdata_failed_counts` 的 `ra_items` / `ppa_items` 已按此列出）；**未清零不得 `set_alpha_properties`**。

## 2. PENDING：`Failed == 0` 不等于「已通过」（RF-03）

`PENDING` 表示平台还没算完（典型是 SELF / PROD 相关性，或提交响应 ②「IS checks still computing」）。口径**不改**——PENDING 不计失败，与平台「PENDING 不挡提交」一致——但语义要说透：

| `Failed` | 名单内 `PENDING` | 含义 | 调用方动作 |
|---|---|---|---|
| = 0 | = 0 | **已通过** | 继续（仍要 prod 实测 + 用户确认，见提交链） |
| = 0 | > 0 | **暂无失败，待复查** | 重跑 `get_alpha_details` 等它算完；超时按**未决**处理——**不据此判死，也不据此放行** |
| > 0 | 任意 | 不合格 | 回步 7 修 |

输出里的 `pending_ra` / `pending_ppa`（数量）与 `ra_pending_names` / `ppa_pending_names`（名字）就是为此而设；`submit_verdict` 在有 PENDING 时会在说明里点明「不得据此放行」。**不要**一刀切把 PENDING 当失败——那与平台行为相反，会阻塞可提交候选。

**例**：某 REGULAR 候选 `is.checks` 里 `LOW_SHARPE` PASS、`LOW_ROBUST_UNIVERSE_SHARPE` PENDING、其余 PASS → `Failed RA = 0`、`pending_ra = 1`：待复查，不是通过。

## 3. 名单去哪看

```
python -c "from wqb.config import RA_CHECK_NAMES, PPA_CHECK_NAMES; print(sorted(RA_CHECK_NAMES)); print(sorted(PPA_CHECK_NAMES))"
```

（在仓库 `src/` 可导入的环境下运行；不要在文档里再抄一份名单。）RA 侧 `IS_LADDER_SHARPE` 对 ATOM alpha 豁免但**仍计**；`LOW_2Y_SHARPE` 与 `IS_LADDER_SHARPE` 是 2 年 sharpe 的两个读数位（`RA_2Y_NAMES`）。
