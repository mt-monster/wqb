---
last_verified: 2026-08-22
name: brain-calculate-alpha-selfcorrQuick
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

## 工具脚本
执行计算时，运行 `scripts` 目录下的 `skill.py` 脚本。

示例：
```bash
python .qoder-cn/skills/brain-calculate-alpha-selfcorrQuick/scripts/skill.py --start-date 01-10 --end-date 01-11 --region IND
```

请确保已安装 `.qoder-cn/skills/brain-calculate-alpha-selfcorrQuick/scripts/requirements.txt` 中的依赖。

## 衔接协议
- **上游**：`wq-brain-alpha-optimization-v1`（Mode B/A 优化产出的候选）。
- **本 skill 角色**：S4 链第三步——本地快筛 self-corr/PPAC（快于平台查询；self-corr>0.7 可直接判死，无需再查生产相关性）。
- **下游**：`brain-explain-alphas`（收益来源归因）→ 过拟合/稳健性测试（见 `wq-brain-alpha-optimization-v1`）→ `brain-alpha-judge`（S5 评审）。
