# DEU 区域脚本（scripts/）

> **家规**（AGENTS §8.13）：skill 内 `scripts/` 只放**本 skill 的校验器 / 固定流程脚本**；
> 区域探针与一次性战役脚本的家是 `tracking/DEU/scripts/`。
> **as_of**：2026-10-18

## 当前清单

| 脚本 | 用途 | 归属 |
|---|---|---|
| `potential_scan.py` | （待补用途） | skill 级 |
| `sweep_unsampled.py` | （待补用途） | skill 级 |

## 不要放进来的东西

- 战役一次性脚本（属 `tracking/DEU/campaign_<date>/`）
- 可复用引擎（属仓库 `tools/`，进 skill 会形成第二份事实源）
- 任何需要凭据的脚本
