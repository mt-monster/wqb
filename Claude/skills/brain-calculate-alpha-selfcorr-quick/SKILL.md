---
last_verified: 2026-09-28
name: brain-calculate-alpha-selfcorr-quick
description: "在本地计算 WorldQuant BRAIN alpha 的自相关与 PPAC（Power Pool Alpha Correlation），比通过 MCP 查询平台快得多。 当用户需要计算 alpha 相关性、核对 PPAC 时使用。"
layer: L4
allowed-tools:
  - Read
  - Bash
---







# Alpha 自相关与 PPAC 相关性计算器

## 职责边界

- **本 skill 负责**：**本地**快筛 self-correlation / PPAC（不占平台相关性配额）
- **本 skill 不做**：**不替代平台实测** —— 提交前必须实测平台值；不作提交判定；不改 alpha
- **上游 / 下游**：上游 = 候选 PnL；下游 = S4 预筛（再进 `check_correlation` / `correlations/prod`）



本 skill 用于计算 alpha 的自相关与 PPAC。
用法与参数详情参见 [reference.md](reference.md)。

## 使用本 skill 的场景
- 无需等待平台，快速评估 alpha 自相关与 Power Pool Alpha Correlation（PPAC）。

## ★★ 本地 SELF 判定规则表（2026-09-11 实证，务必先读）

**本地 SELF 基于 `downloads/os_pnl_pool.pkl`（OS 样本外 PnL 池）计算；刚提交的 alpha 尚无 OS PnL，
不在池中 → 对「近期提交的孪生体」结构性失明，会给出严重低估的假阴性。**

实证：`vRkAO9Xd` 本地 `check_self_correlation` = **0.229**，平台提交实测 `SELF_CORRELATION` = **0.8392**
（差 0.61）。原因：当日新 ACTIVE 的 `blRaArVZ` 与其近孪生，但本地池看不见它。
（源码：`world-quant-brain-mcp/brain_mixin_correlation.py` 的 `get_self_correlation` docstring：
"OS alpha PnL is considered static and cached on disk; only newly-submitted OS alphas are downloaded"。）

| 本地 SELF 结果 | 判定 | 动作 |
|---|---|---|
| **高**（>0.7） | 可信（保守方向安全） | 可据此否决候选，无需再查平台 |
| **低**（<0.7） | **不可据此放行**（本地低 ≠ 平台低） | 若候选同族/孪生体是近期提交的，本地值不可信；提交前仍须平台实测 |

**同族连测场景（「同族只留最优 1 颗」）不要依赖本地 SELF 判活**——改用零成本实测。
提交探测协议（`POST /alphas/{id}/submit` 读 `is.checks` 各 check 的 `value/limit`、`GET /submit` 恒 404、
硬闸阻断不消耗配额等）的**唯一权威 = `brain-alpha-robustness` Phase E**，本 skill 只做本地快筛，不重复该探测逻辑。

## 工具脚本
执行计算时，运行 `scripts` 目录下的 `skill.py` 脚本。

示例：
```bash
$WQ_PY <SKILL_ROOT>/brain-calculate-alpha-selfcorr-quick/scripts/skill.py --start-date 01-10 --end-date 01-11 --region IND
```

**脚本三要素**：
- **region 合法值**：平台 region 代码（如 `IND` / `USA` / `EUR` / `CHN` / `JPN` / `KOR` 等）；`--region` 必须与候选 alpha 的 `settings.region` 一致，否则查询结果为空。默认 `IND`。
- **输出路径**：结果 `.xlsx` 写到**当前工作目录**，默认文件名 `alpha_results_{start_date}_{region}.xlsx`（如 `alpha_results_01-10_IND.xlsx`）；可用 `--output` 覆盖。缓存 pickle（`os_alpha_ids` / `os_alpha_pnls` / `ppac_alpha_ids`）也落在当前目录。
- **依赖安装**：先装 `<SKILL_ROOT>/brain-calculate-alpha-selfcorr-quick/scripts/requirements.txt`（requests/pandas/numpy/tqdm/openpyxl）；用 MCP venv（`$WQ_PY`）执行，勿用系统 Python。

## 衔接协议
- **上游**：`wq-brain-alpha-optimization-v1`（Mode B/A 优化产出的候选）。
- **本 skill 角色**：S4 链第三步——本地快筛 self-corr/PPAC（快于平台查询；self-corr>0.7 可直接判死，无需再查生产相关性）。
- **下游**：`brain-explain-alphas`（收益来源归因）→ **`brain-alpha-robustness`**（过拟合/稳健性必经闸，S4→S5）→ `tools/submit_verdict.py`（提交层权威判定；`brain-alpha-judge` 仅作可选参考评审）。
