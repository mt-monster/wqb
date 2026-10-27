# IND 区域脚本（scripts/）

> **家规**（AGENTS §8.13）：skill 内 `scripts/` 只放**本 skill 的校验器 / 固定流程脚本**；
> 区域探针与一次性战役脚本的家是 `tracking/IND/scripts/`。
> **as_of**：2026-10-25

## 当前清单

| 脚本 | 用途 | 归属 |
|---|---|---|
| `ind_campaign/ind_runner.py` | IND campaign 托管器（看门狗；region 硬钉 IND，并发默认 2） | 区域自带 |
| `ind_campaign/ind_main.py` | IND 流水线薄入口（读 `_IND` 断点续跑） | 区域自带 |
| `ind_campaign/campaign_semantics.py` | 引擎的语义映射模块（顶层 import，必须与 `ind_main.py` 同目录） | 区域自带快照 |
| `ind_campaign/wqb_campaign/` | 流水线引擎（与 EUR 副本逐字相同；编排模块改名 `pipeline_ind.py` 以避开 S6 同名分叉） | 区域自带快照 |
| `run_ind.cmd` | Windows 启动器（7 类别 + 十年硬要求 + 并发 2） | 区域自带 |

> **⚠ 旧入口已归档（2026-10-25）**：`run_ind_campaign.py` / `run_campaign_bg.cmd` /
> `ind_campaign/campaign_supervisor.py` / `ind_campaign/full_template_campaign.py` /
> `ind_campaign/state/` / `ind_campaign/.wqb_root` 已移入仓库
> `attic/ind_legacy_launchers_20261025/`（旧 supervisor 不认 `InstanceLock`，且断点落在
> 另一套 `state/` 目录，被误启动会另起一场并行战役烧配额）。
> 计划任务 **`WQB_IND_CAMPAIGN` 仍是 Disabled 且指向已移走的 `run_campaign_bg.cmd`**——
> 不要重新启用；要开机自启请改指向 `run_ind.cmd` 并确认只启一个实例。

> **为什么这里有一份可复用引擎**（2026-10-25 用户裁定）：此前 IND 借用
> `wq-brain-ra-eur/scripts/eur_runner.py`（靠 `WQB_CAMPAIGN_REGION=IND`），代码归属与
> 运行区域不一致，容易串。现改为**每个在用区域自带一份**；引擎仍以“逐字相同”为前提，
> S6 漂移闸只放行完全相同的副本（WARN），**一旦分叉即 FAIL**——所以它拦的是漂移，
> 代价是改动必须多份同步。

## 不要放进来的东西

- 战役一次性脚本（属 `tracking/IND/campaign_<date>/`）
- 与区域无关的通用工具（属仓库 `tools/`）
- 任何需要凭据的脚本
