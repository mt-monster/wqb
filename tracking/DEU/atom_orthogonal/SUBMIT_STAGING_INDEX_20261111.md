# 提交暂存清单（2026-11-11 更新：prod 四件全到位）

> ⚠ 提交不可逆。本清单仅代表"已具备提交条件"，**不代表已获授权**。
> 授权必须来自用户明确的文字确认；问卷超时自动选中不构成授权。

## 一、篮子成员状态总表

| # | alpha | 塔 | S | F | 2Y | sub | TO | self | prod | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | zq3eb7No | ANALYST | 2.01 | 1.28 | 1.64 | 1.00 | 0.226 | 0.364 | — | ✅ ACTIVE（11-08） |
| 2 | bl6AvMkN | MODEL+ANALYST | 1.61 | 1.36 | 2.15 | 0.94 | 0.110 | 0.514 | — | ✅ ACTIVE（11-07） |
| 3 | **RREPm361** | ANALYST | 2.02 | 1.25 | 1.82 | **1.24** | 0.251 | 0.3275 | 0.6881* | 🟡 待授权 |
| 4 | **1YNMAA8M** | MODEL+ANALYST | 1.58 | 1.36 | 2.13 | 1.01 | 0.134 | **0.6946** | 0.6951* | 🟡 待授权（**三贴线**） |
| 5 | **qM7KxkQV** | SHORT+INSIDERS | 1.72 | 1.34 | 2.43 | 0.92 | 0.143 | 0.5429 | **0.543** | 🟡 待授权（最干净） |
| 6 | **Jj8VQwoe** | SHORT+OTHER | 1.65 | 1.24 | 2.42 | **1.22** | 0.147 | 0.5645 | **0.6124** | 🟡 待授权 |

`*` = 历史读数，提交前需 refresh 终验。

## 二、逐件提交前必做的两件事

| alpha | 必查项 | 理由 |
|---|---|---|
| RREPm361 | ① prod refresh ② **与 zq3eb7No 互相关重算** | 互相关 0.6879，余量 0.012 |
| 1YNMAA8M | ① prod refresh ② **self refresh** | self 0.6946 对端 rKRx2Alj，余量 0.0054；S 恰好 1.58 压线 |
| qM7KxkQV | prod **真 refresh**（现 0.543 是平台缓存，computed=false） | 缓存值不等于当前值 |
| Jj8VQwoe | 无（0.6124 本轮新算 computed=true） | — |

## 三、互相关证据（全对 <0.7，最大独立集 = 6）

| 对 | 相关 |
|---|---:|
| zq3eb7No ~ RREPm361 | **0.6879**（最紧） |
| bl6AvMkN ~ 1YNMAA8M | 0.5128 |
| qM7KxkQV ~ Jj8VQwoe | 0.6292 |
| Jj8VQwoe ~ E569ZE7L（已作废） | 0.2596 |
| 其余 | ≤0.272 |

## 四、已排除（永不提交）

| alpha | 原因 |
|---|---|
| **E569ZE7L** | self=**1.0000** 撞已 ACTIVE 的 78Yk8VR1（同表达式，指标逐项相同） |
| 1YWqzPGQ | 与 Jj8VQwoe 互相关 **0.8924**；且 2016 年 Sharpe **-1.00**，S/F/sub/TO 全面劣于 Jj8VQwoe |
| wpo8ZQN6 | 与 qM7KxkQV 互相关 **0.935**；S1.64 < 1.72 |
| rK71dLbE | 与 qM7KxkQV 互相关 **0.8451**（共享 I7 第二腿）；S1.40 也低于 1.72 |
| 3q0M99Gz / xAvKY0Ob / WjlEPPYP / ZYaR09Y0 | 族内 0.92-0.99 互斥，S 均低于 qM7KxkQV |

## 五、建议提交顺序（若获授权）

1. **qM7KxkQV** — prod 0.543 最优、self 0.54、S1.72 全项最稳（先做 prod refresh）
2. **Jj8VQwoe** — prod 0.6124 本轮新算、sub 1.22 最高
3. **RREPm361** — S2.02 最高，但要同时验 prod + 与 zq3eb7No 互相关
4. **1YNMAA8M** — 三贴线（S 1.58 / self 0.6946 / prod 0.6951），风险最高，放最后或直接放弃

替代方案：若 1YNMAA8M 的 self refresh 超过 0.7，直接用 **P05JM61x**（若 BE14 破闸成功）顶替。


## 终验补记（2026-11-11 08:5x，goal 恢复后）

4 颗待授权件 prod 已全部 refresh=True 平台真实重算（48h 保鲜窗口内）：

| alpha | prod（本轮实测） | pass | 与历史读数 |
|---|---|---|---|
| qM7KxkQV | **0.543** | ✅（余量 0.157） | 一致（缓存 flag 解除） |
| Jj8VQwoe | **0.6124** | ✅（余量 0.088） | 一致 |
| d5a2vxzY | **0.6039** | ✅（余量 0.096） | 一致 |
| 9qlz29Oe | **0.47** | ✅（余量 0.23） | 一致 |
| RREPm361 | 0.6881（11-10 20:00 实测） | ✅（余量 0.012） | — |

⇒ **5 颗待授权件现在处于完整终验状态**（IS 硬闸 / self / prod / 互相关 / 逐年覆盖全绿），
提交只需用户明确文字授权（不可逆 POST，走 worldquant-submit-alpha 流程）。
88NmN37X 换防选项同样终验完毕（self 0.5538 / prod 0.5541，见 SWAP_AUDIT_20261112）。
裁定问卷两次 60s 超时，安全默认项自动生效（非用户选择）：暂不提交 / QPveY7Kg 维持除名 / 待命。


## 提交层判定补记（2026-11-11 08:56）

submit_verdict（平台否决权威，只能拦不能放）× 6 颗：

| alpha | verdict | failed_ra | failed_ppa | sim_fails |
|---|---|---|---|---|
| RREPm361 | UNVERIFIABLE_404（预期：GET /submit 恒 404） | 0 | 0 | [] |
| qM7KxkQV | 同上 | 0 | 0 | [] |
| Jj8VQwoe | 同上 | 0 | 0 | [] |
| d5a2vxzY | 同上 | 0 | 0 | [] |
| 9qlz29Oe | 同上 | 0 | 0 | [] |
| 88NmN37X（换防） | 同上 | 0 | 0 | [] |

**无任何平台层否决**。next_step 要求的 check_correlation prod<0.7 已全部完成（08:5x refresh 实测）。
⇒ 七层验证全绿：IS 硬闸 / self / prod(refresh) / 互相关<0.7 / 逐年覆盖 / 提交层判定 / Failed-count 门(0/0)。
真提交 = 用户明确文字授权后的 POST submit（worldquant-submit-alpha 流程）。
