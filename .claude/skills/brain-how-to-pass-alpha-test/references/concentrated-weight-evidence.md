# CONCENTRATED_WEIGHT 实测证据（IND / TOP500 分析师修正族，2026-09-01）

> 主文见 [`../SKILL.md`](../SKILL.md) §4。本页只放逐例证据，**其中只有第 4 行是可复制的合规式样**；前三行含已被闸 5 禁止的加权混合写法（2026-09-13「路线 A」起全量 block），仅作历史记录，**不得照抄**。
> **适用范围 / 置信度**：证据只来自 **IND / TOP500 的分析师修正族**，n = 4（2 例 FAIL、2 例 PASS）；其它区域、其它信号类型**未验证**。原始记录**未留 alpha id**，可追溯性弱，待补。

## 现象

本闸没有 value / limit，IS 阶段只显示 `WARNING` 或 `PASS`，**提交后才判 FAIL（403）**。`WARNING` 计入 Failed RA（口径见 RA `webdatascope-failed-gates.md`）。硬闸失败的提交不消耗配额。

## 逐例

| # | 构造（U / D = 上调 / 下调计数字段；RES = 残差字段） | 本闸（IS 阶段） | 提交结果 |
|---|---|---|---|
| 1 | <!-- lint:counterexample -->`add(0.6*rank(subtract(U30,D30)), 0.4*(-rank(ts_mean(RES,10))))`（A 项瞬时；**已被闸 5 禁止的加权混合**） | WARNING | FAIL（记录里的 4.26 / 3.97 也照拦；原记录未标注是哪个指标） |
| 2 | <!-- lint:counterexample -->`add(0.6*rank(subtract(U14,D14)), 0.4*(-rank(ts_mean(RES,10))))`（A 项瞬时；**已被闸 5 禁止**） | WARNING | FAIL |
| 3 | <!-- lint:counterexample -->`add(0.6*rank(ts_mean(subtract(U14,D14),10)), 0.4*(-rank(ts_mean(RES,10))))`（A 项平滑；**已被闸 5 禁止**） | **PASS** | 成功（记录里的 3.70 / 3.19；原记录未标注指标） |
| 4 | `rank(ts_mean(subtract(U30,D30),10))`（单信号平滑；**可复制的合规式样**） | **PASS** | 已 ACTIVE |

**可继承的结论只有一条：时间平滑治 CW。** 落地取第 4 行的单信号平滑形（`ts_mean` / `ts_decay_linear`），或用 `subtract(rank(短窗), rank(长窗))` 这类**同源**结构交互（见 optimization-v1 形态库的「同源价差」判据）。

## 平滑窗口

原实验窗口是 **10**，**不在标准窗口白名单**（`[1, 5, 22, 66, 252, 504, 1008, 1260]`；`window_whitelist_enforce = false` 时只 warn，但 CLAUDE.md 要求非标窗口给出解释与实测）。复用本结论时取 **5 或 22**，并复验 CW 状态；本页不把 10 当作推荐值。

## 参数层无效（别再试）

- 换 neutralization（MARKET / SECTOR / INDUSTRY / SUBINDUSTRY 四档）仍 `WARNING`；
- truncation 0.08 → 0.02 / 0.01 仍 `WARNING`；
- 末端再套 `rank(...)` **反而变 FAIL**（反直觉；只有这一句记录，**无案例 id**——复现前把它当假设而非结论）；
- `scale(x, 1)` 语法错（`scale` 只收 1 个输入）。

## 结论

事件 / 计数类字段（分析师评级变动、新闻计数、财报事件等）构造时**默认加时间平滑**，不要直接 rank 瞬时值。
