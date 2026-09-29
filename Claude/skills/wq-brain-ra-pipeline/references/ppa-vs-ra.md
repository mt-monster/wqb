# PPA 分支：与 RA 逐步的差异

> 主 SOP 见 [`../SKILL.md`](../SKILL.md)「PPA 分支」。PPA（Power Pool Alpha）**不另起编排器**：走同一条九步，只在下表标注的步骤改动。
> 不要把 [`wq-brain-ppa-mining`](../../wq-brain-ppa-mining/SKILL.md) 当编排器调用——它是 S0 体检的**方法论**与 PPA 主题核查（无编排、无提交）。方法论只有 ppa-mining 一个家；RA 侧仅留其没有的历史实证与「已作废旧说法」表，见 [`ppa-mining-experience.md`](ppa-mining-experience.md)。
> 判据数字（Sharpe ≥ 1.0、算子 ≤ 8、字段 ≤ 3、PPAC < 0.5）来自平台 Power Pool 规则的文档记载，**本环境未向平台复核**，以当期平台规则为准。

## 1. 两道主题门禁：不是两套政策，是两个时点

旧文的两句话（「PPA 主题不匹配则挖 RA」与「不匹配的达标候选标 YELLOW + WAIT_THEME_ROTATION」）被读成互相冲突。它们回答的是不同问题：

| 时点 | 门禁回答的问题 | 做法 |
|---|---|---|
| **挖矿期**（步 1） | 这个战役**要不要进 PPA 分支** | `get_messages(limit=30)` 实时扫当期 Power Pool 公告（**每次 S-PRE 重扫，禁止复用 settings 快照**）：主题的 region / delay / universe **匹配** → 走 PPA 分支；**不匹配 → 走 RA 分支**（不为不受理的主题烧配额） |
| **候选期**（步 7 之后） | 一颗**已达标**的候选**现在能不能走 PPA 通道** | 不在当期主题窗口 → 候选标 `YELLOW` + `WAIT_THEME_ROTATION`（`brain-alpha-judge` 用同名结果值，不返回 `READY`），**等主题轮转**；RA 常规提交**不受**主题限制 |
| **提交期**（步 8） | 走 MCP 还是 web UI | 见 [`ppa-handoff.md`](../../worldquant-submit-alpha/references/ppa-handoff.md)：满足本地预检可走 MCP，否则 agent **停下交接**人工在 web UI 提交 |

## 2. 逐步差异表

| 步 | RA | PPA 改动 |
|---|---|---|
| 1 S-PRE | 库存盘点 → 查表 → 跨区死路 | 增加 §1 挖矿期主题门禁；其余同 |
| 2 S0 | 体检为 tier 评分**软罚**（`dataset_health.mode="general"`） | `mode="ppa"`：平台实时体检三条**硬门槛**一票否决——coverage ≥ 0.85、alphaCount ≤ 50、fieldCount ≥ 10；tier1 中拥挤超标者降 tier2（实现 `score_datasets.py`；方法论 `wq-brain-ppa-mining` §1.0） |
| 3 S1 | typed catalog + 闸 SEM | 同 |
| 4 S2 | 概念优先 GEM | 表达式受 Power Pool 规则约束：算子 ≤ 8、字段 ≤ 3；主题若限定数据集类型（如单数据集 + PV / fundamental），以当期公告原文为准 |
| 5–6 | 门禁 / 回测 | 同 |
| 7 S4 | 资格 = `Failed RA == 0` | 资格 = **`Failed PPA == 0`**（`PPA_CHECK_NAMES` 7 项，口径 `compute_webdata_failed_counts`）；另须 PPAC < 0.5（本地 `brain-calculate-alpha-selfcorr-quick`）；Sharpe ≥ 1.0（低于 RA 的 1.58） |
| 8 提交 | REGULAR → `worldquant-submit-alpha` | 属性：color `PURPLE`、tags `CH_PPA` / `SRC_<数据集>` / `PowerPoolSelected`；**独立配额** `POWER_POOL_SUBMISSION` 1 / ET 日，不占 REGULAR 4 / 日；**渠道限制**见下 |
| 9 S6 | 回写 | 同；用户在 web UI 提交后 `python tools/ppa_handoff.py record --alpha-id <ID>` 核验并落账 |

## 3. 日循环与提交渠道（旧文缺的边界）

- **日循环停止闸**：submit-ready 队列 ≥ 4 颗即可停止挖矿（操作约定，无机检）。
- **当天优先提 PPA 那一颗**（独立配额、不占 REGULAR 额度）——**但 PPA 提交渠道有限制**：MCP 的 `workflow_submit_alpha` **不是 PPA 感知的**（本地预检不看 `PowerPoolSelected`，合法但指标较低的 PPA 会被拦）。所以：
  - 候选满足本地预检 → 可走 MCP，其余规则同 REGULAR（**不可逆，须用户明确确认**，见 [`submit-chain.md`](../../worldquant-submit-alpha/references/submit-chain.md)）；
  - 不满足 → **agent 停下并交接**（`python tools/ppa_handoff.py sheet --alpha-id <ID>` 生成交接单），用户在 web UI 提交；用户不在线时候选留在 `submit_ready`，**不改走 MCP 通道**。
- PPA 提交**永远**需要用户确认；agent 只产出候选清单与主题匹配证明。
