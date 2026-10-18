# USA 区域脚本（scripts/）

> **家规**（AGENTS §8.13）：skill 内 `scripts/` 只放**该 skill 的校验器/固定流程脚本**；
> **区域探针与一次性战役脚本的家是 `tracking/USA/scripts/`**，不要往这里堆。
> **as_of**：2026-10-18

## 当前清单

| 脚本 | 用途 | 状态 |
|---|---|---|
| （暂无） | — | 本区 skill 级脚本为空 |

## 为什么现在为空

2026-10 两战役（`campaign_20261014` / `campaign_20261017`）的脚本都是**一次性**的：

- 批次派发与收割 → 走 MCP `create_multi_simulation` / `harvest_multisim_alphas`，无需本地脚本
- prod/self 相关性 → 走 MCP `check_correlation(refresh=True)`，本地复现反而更慢
- 提交链路 → `submit_alpha` 节点（`wqb.workflow.nodes.submit_alpha`），已由 skill 化，不需要每区一份

⇒ **无值得固化的 skill 级脚本**。若日后出现「本区特有、每次都要跑」的流程（例如 USA 专属的
prod 漂移巡检或塔点亮快照刷新），落在这里并在 [`../config/region_view.json`](../config/region_view.json)
登记；纯战役脚本落 `tracking/USA/scripts/`，用完随战役目录归档。

## 不要放进来的东西

- 战役一次性脚本（属 `tracking/<R>/campaign_<date>/`）
- 可复用引擎（属仓库 `tools/`，进 skill 会形成第二份事实源）
- 任何需要凭据的脚本（凭据三级链见 `RULES.md`，禁入 skill）
