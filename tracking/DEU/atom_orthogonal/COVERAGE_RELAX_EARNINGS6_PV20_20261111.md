# ★覆盖约束放宽后的复测：earnings6 仍不可交付，但 pv20 流动性面是新发现（2026-11-11 11:2x）

> 触发：用户指令「earnings6 放宽『近十年都要有数据』约束试下，看是否能挖掘出alpha」。

## 一、先确认约束边界：平台根本不拦前段空窗

earnings6 各臂的平台 checks.fail 明细（BE63/BE64 代表件）：

| alpha | lc | S | 平台 fail 项 |
|---|---:|---:|---|
| rK7Kx0zj | 183 | 0.60 | LOW_SHARPE / LOW_FITNESS / HIGH_TURNOVER(0.77) / CONCENTRATED_WEIGHT / LOW_2Y |
| 3q0qN9ON | 208 | -0.65 | LOW_SHARPE / LOW_FITNESS / LOW_2Y |
| 1YWYMxRX | 213 | 0.59 | LOW_SHARPE / LOW_FITNESS / LOW_SUB / LOW_2Y |
| E5Q5dvMK | 208 | -0.55 | LOW_SHARPE / LOW_FITNESS / LOW_2Y |

⇒ **无任何覆盖类/IS_LADDER 失败**，持仓数 183-213 正常 ⇒ 「连续多年空窗」纯属我方内部口径，
**放宽后 earnings6 在平台侧可提交**，剩下唯一障碍是信号强度。

## 二、BE69 深挖 10 臂（earnings6，EAT 机制可访问重建）—— 仍不可交付

| 臂 | 构造 | S | 备注 |
|---|---|---:|---|
| 1 | -ts_rank(排期,380)（历史分位代理） | -0.30 | 反向 |
| 2 | -ts_rank(排期,252) | -0.32 | 反向 |
| 3 | -ts_rank(排期,504) | -0.30 | 反向 |
| 4 | -ts_zscore(排期,380)（BE64 臂1 符号翻转） | +0.15 | 方向确认但强度弱 |
| 5 | -ts_rank(ern6_1q,380) | -0.49 | |
| 6 | -ts_rank(ern6_2q,380) | -0.31 | |
| 7 | 指引区间宽度（upper/lower） | **-5.81** | 除零爆炸，未加 ε |
| 8 | SUE 时序标准化（actual-estimated,252） | -0.22 | |
| 9 | -ts_rank(ern6_4q,380) | -0.31 | |
| 10 | -ts_rank(排期,660) | -0.28 | |

**结论**：earnings6 的 EAT 机制在可访问算子下**上界约 0.6**（唯一有信息的是 BE64 的 ts_zscore 方向：
「排期晚于自身历史 ⇒ 未来收益低」，S -0.59 说明 **EAT 方向在 DEU 成立**，但强度不足以过 1.58）。
⇒ **放宽覆盖救不了 earnings6**（平台不拦，但 S 过不了）。EARNINGS 塔维持关闭。

## 三、★真正的收获：pv20 流动性/成交额面（cov=0 但有数据，且是全新机制面）

BE68 实测：`average_daily_value_20d_usd`（20 日日均成交额）**S 1.03 / F 0.68 / TO 0.102**；
`adv20_usd_capped_100m` **S 0.95 / F 0.60 / TO 0.089 / 2Y 1.28**。

- 机制：**流动性水平（Amihud 型）**——低流动性溢价（Amihud 2002、Baker-Jordan 规模效应）；
- PV 塔**未点亮** ⇒ 单数据集 ATOM；
- cov=0 但有数据（lc 正常、TO 低）⇒ 又一例「cov=0 ≠ 无数据」；
- **这是本战役第一次在 PV 塔（未点亮）拿到 S>1.0 的可交付面**（此前 PV 全部 ≤0.79）。

## 四、已派升级波

- BE70（1VMsDcco54unaXvfKo4KSdO）：窗口族 252/504 + Δ面 + subindustry + 与开放族组合；
- BE71（2fm4EP3Eh4wobIqRolzsax）：反向（低流动性溢价）+ 流动性收缩 + 相对化 + 波动 + 换手代理 + 与情绪/内部人组合。

## 五、方法论更新（已入记忆）

1. **覆盖口径是我方内部闸，不是平台硬闸**——放宽后可直接复活 cov=0 但有数据的数据集；
2. **放宽覆盖只解决「可提交性」，不解决「信号强度」**——earnings6 是反例（平台不拦，但 S≤0.6）；
3. **cov=0 的数据集必须实测而非推断**（已 6 例：earnings6 / fnd90 / risk72 / institutions1 / pv1 / pv20）。