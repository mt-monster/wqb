---
last_verified: 2026-09-11
name: brain-calculate-alpha-selfcorr-quick
description: "在本地计算 WorldQuant BRAIN alpha 的自相关与 PPAC（Power Pool Alpha Correlation），比通过 MCP 查询平台快得多。 当用户需要计算 alpha 相关性、核对 PPAC 时使用。"
layer: L4
allowed-tools:
  - Read
  - Bash
---







# Alpha 自相关与 PPAC 相关性计算器

本 skill 用于计算 alpha 的自相关与 PPAC。
用法与参数详情参见 [reference.md](reference.md)。

## 使用本 skill 的场景
- 无需等待平台，快速评估 alpha 自相关与 PowerPool Alpha Correlation（PPAC）。
- 若 self-corr 高于 0.7，甚至无需再向平台查询生产相关性 —— 因为平台结果同样会高于 0.7，无法通过提交测试。

## ★★ 已知结构性盲区（2026-09-11 实证，务必先读）

**本地 SELF 基于 `downloads/os_pnl_pool.pkl`（OS 样本外 PnL 池）计算；刚提交的 alpha 尚无 OS PnL，
不在池中 → 对「近期提交的孪生体」结构性失明，会给出严重低估的假阴性。**

实证：`vRkAO9Xd` 本地 `check_self_correlation` = **0.229**，平台提交实测 `SELF_CORRELATION` = **0.8392**
（差 0.61）。原因：当日新 ACTIVE 的 `blRaArVZ` 与其近孪生，但本地池看不见它。
（源码：`world-quant-brain-mcp/brain_mixin_correlation.py` 的 `get_self_correlation` docstring：
"OS alpha PnL is considered static and cached on disk; only newly-submitted OS alphas are downloaded"。）

**因此：**
1. 本地值**高**（>0.7）→ 可信，可据此否决候选（保守方向安全）。
2. 本地值**低** ≠ 平台会低。**若候选的同族/孪生体是近期提交的，本地值不可信**。
3. 同族连测场景（「同族只留最优 1 颗」）**不要依赖本地 SELF 判活**，改用零成本实测：
   `GET /alphas/{id}/submit` → **403 = BLOCKED**，响应体带各 check 的 `value/limit`
   （比 `is.checks` 的 PENDING 更早拿到平台实测 PROD/SELF）；或 POST 后回读 status。
   注：硬闸阻断的提交**不消耗配额**（`dateSubmitted` 保持 None、activities 不变）。

## 工具脚本
执行计算时，运行 `scripts` 目录下的 `skill.py` 脚本。

示例：
```bash
python <SKILL_ROOT>/brain-calculate-alpha-selfcorr-quick/scripts/skill.py --start-date 01-10 --end-date 01-11 --region IND
```

请确保已安装 `<SKILL_ROOT>/brain-calculate-alpha-selfcorr-quick/scripts/requirements.txt` 中的依赖。

## 衔接协议
- **上游**：`wq-brain-alpha-optimization-v1`（Mode B/A 优化产出的候选）。
- **本 skill 角色**：S4 链第三步——本地快筛 self-corr/PPAC（快于平台查询；self-corr>0.7 可直接判死，无需再查生产相关性）。
- **下游**：`brain-explain-alphas`（收益来源归因）→ 过拟合/稳健性测试（见 `wq-brain-alpha-optimization-v1`）→ `brain-alpha-judge`（S5 评审）。
