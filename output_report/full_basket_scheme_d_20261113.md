# 全篮子 · 方案 D（分层 + 配对）评估（2026-11-13 20:14 GMT+8）

> **只读评估，未提交任何 alpha。** 判据唯一事实源 = `src/wqb/workflow/nodes/submit_alpha.py` 的 `_marginal_contribution` / `MARGINAL_*`（§7 定案方案 D）；逐颗 `performance_comparison` 于本轮重新实测，不复用上午快照。

## 0 一句话结论

**47 颗活跃候选 → 46 颗端点可读 → 方案 D 放行 31 颗 / 阻断 15 颗 / 1 颗 fail-open；叠加原有 prod·self·台账·ΔS·mix 硬闸后 28 颗双通过，去同席后 26 颗可执行，本轮最多点亮 3 座新塔（原 4 座）。**

| 层 | 数量 | 说明 |
|---|---:|---|
| 全篮子活跃候选 | 47 | 11-13 12:20 全量盘子，全部 UNSUBMITTED |
| `performance_comparison` 可读 | 46 | `d5a2aO7v` 400 ⇒ `available=False`，按规则 fail-open（且本就被旧硬闸排除） |
| 方案 D 放行 | 31 | 其中 11 颗为「ΔRet<0 但成本同步降」的分散化补偿放行 |
| 方案 D 阻断 | **15** | 命中项可叠加：ΔS<0 **7 颗**、ΔF<0 **5 颗**（互相重叠 4）、配对判据 **9 颗**（其中 2 颗同时净效果为负） |
| 旧 36 颗无硬闸 → 被新标准拿掉 | **8** | 详见 §3；其中 `6XMmE0EL` 是旧 ΔS 闸抓不到的 ΔF<0 |
| 双通过（旧硬闸 ∧ 方案 D） | **28** | |
| 去同席后可执行 | **26** | 让位 `pwdLp9z6`(ρ=.8619)、`xAvK73Qg`(ρ=.7409) |
| 可新点亮塔 | **3 座** | GBR/D1/OTHER、DEU/D1/OTHER、EUR/D1/RISK；**KOR/D1/PV 本轮失守** |

**推荐顺位（综合，与 §7 定案一致）**：`omEdka3v` → `wpo8olA6` → `6XdkW08J`；若以「最少提交点亮最多塔」为目标，第三席改 `zq3Yrb3G`。**闸放行 ≠ 推荐提交**，提交权仍归用户点名。

## 1 判据（方案 D，三层）

| 层 | 判定 | 处置 |
|---|---|---|
| 1 净效果（唯一硬闸） | `ΔSharpe ≥ 0` 且 `ΔFitness ≥ 0` | 任一为负 ⇒ 阻断，`force` 不豁免 |
| 2 配对（仅 ΔRet<0 时启用） | `ΔRet<0` 且 (`ΔTO>0` 或 `ΔDD>0`) | 双重恶化 ⇒ 追加阻断；成本同步降 ⇒ 分散化补偿放行 |
| 3 归因（纯软告警） | `ΔTO` / `ΔDD` 单独变差 | 只写 `soft_warnings`，不设闸 |

`available=False`（端点空体/400/异常）fail-open；`ΔS` 只在**同一分区**内可比，本报告 8 个分区并列展示、不跨区横比。

## 2 全篮子逐颗裁决（47 颗，含逐颗塔信息）

### 2.1 原 36 颗「无旧硬闸」候选（28 放行 / 8 新阻断）

| # | alpha | 区/分 | 分区 | ΔS | ΔF | ΔRet | ΔTO | ΔDD | D 裁决 | 命中层 | 软告警 | 塔归属→现值→交后→是否新点亮 | 塔边际增量 |
|---:|---|---|---|---:|---:|---:|---:|---:|:---:|---|---|---|:---:|
| 1 | `omEdka3v` | GBR/92 | GBR:1:POWER_POOL | +0.59 | +0.25 | +0.0028 | +0.0252 | +0.0033 | **放行** | 通过 | turnover,drawdown | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | +1 |
| 2 | `wpo8olA6` | DEU/88 | DEU:1:POWER_POOL | +0.56 | +0.42 | +0.0015 | +0.0063 | -0.0164 | **放行** | 通过 | turnover | SHORTINTEREST 3→4 否 / OTHER 2→3 点亮 | +1 |
| 3 | `pwdLp9z6` | GBR/82 | GBR:1:POWER_POOL | +0.46 | +0.13 | +0.0016 | +0.0282 | +0.0025 | **放行** | 通过 | turnover,drawdown | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | —（未进可执行集） |
| 4 | `ZYQ116ln` | KOR/75 | KOR:1:POWER_POOL | +0.24 | +0.10 | -0.0026 | +0.0035 | -0.0026 | **阻断** | ΔRet+成本 | turnover | PV 2→3 点亮 | —（未进可执行集） |
| 5 | `leAmmre8` | GBR/72 | GBR:1:POWER_POOL | +0.69 | +0.19 | +0.0007 | +0.0382 | -0.0019 | **放行** | 通过 | turnover | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | 0 |
| 6 | `6XdkW08J` | GBR/71 | GBR:1:POWER_POOL | +0.42 | +0.34 | +0.0020 | -0.0014 | -0.0008 | **放行** | 通过 | — | SHORTINTEREST 4→5 否 / MODEL 6→7 否 | 0 |
| 7 | `xAvK73Qg` | DEU/71 | DEU:1 | +0.08 | +0.08 | +0.0002 | +0.0000 | -0.0010 | **放行** | 通过 | — | SHORTINTEREST 3→4 否 / OTHER 2→3 点亮 | —（未进可执行集） |
| 8 | `Jj8VQwoe` | DEU/64 | DEU:1 | +0.04 | +0.02 | -0.0009 | +0.0003 | -0.0008 | **阻断** | ΔRet+成本 | turnover | SHORTINTEREST 3→4 否 / OTHER 2→3 点亮 | —（未进可执行集） |
| 9 | `O0A6Qz7p` | GBR/64 | GBR:1 | +0.09 | +0.07 | -0.0004 | -0.0011 | -0.0005 | **放行** | 补偿放行 | returns | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | 0 |
| 10 | `88NmN37X` | DEU/62 | DEU:1:POWER_POOL | +0.74 | +0.68 | +0.0058 | -0.0179 | -0.0314 | **放行** | 通过 | — | SHORTINTEREST 3→4 否 / INSIDERS 0→1 否 | 0 |
| 11 | `JjeNJ00O` | EUR/62 | EUR:1 | +0.02 | +0.01 | -0.0002 | +0.0023 | -0.0003 | **阻断** | ΔRet+成本 | turnover | RISK 2→3 点亮 / IMBALANCE 3→4 否 | —（未进可执行集） |
| 12 | `YP1baJrv` | EUR/62 | EUR:1 | +0.02 | +0.01 | -0.0001 | +0.0022 | +0.0003 | **阻断** | ΔRet+成本 | turnover,drawdown | RISK 2→3 点亮 / OTHER 3→4 否 | —（未进可执行集） |
| 13 | `qM7KxkQV` | DEU/61 | DEU:1 | +0.05 | +0.04 | -0.0007 | +0.0001 | -0.0008 | **阻断** | ΔRet+成本 | turnover | SHORTINTEREST 3→4 否 / INSIDERS 0→1 否 | —（未进可执行集） |
| 14 | `zq3Yrb3G` | EUR/61 | EUR:1 | +0.02 | +0.02 | +0.0000 | +0.0019 | -0.0001 | **放行** | 通过 | turnover | RISK 2→3 点亮 / ANALYST 10→11 否 / SENTIMENT 3→4 否 | +1 |
| 15 | `Xg9dPpp0` | GBR/60 | GBR:1:POWER_POOL | +0.42 | +0.33 | +0.0013 | -0.0013 | -0.0015 | **放行** | 通过 | — | SHORTINTEREST 4→5 否 / RISK 0→1 否 / FUNDAMENTAL 3→4 否 | 0 |
| 16 | `mLaLllmK` | EUR/60 | EUR:1:POWER_POOL | +0.84 | +0.41 | +0.0053 | +0.0256 | -0.0025 | **放行** | 通过 | turnover | OTHER 3→4 否 | 0 |
| 17 | `omExeqLb` | GBR/59 | GBR:1:POWER_POOL | +0.52 | +0.40 | +0.0036 | +0.0028 | -0.0005 | **放行** | 通过 | turnover | SHORTINTEREST 4→5 否 / MODEL 6→7 否 | 0 |
| 18 | `6XMmE0EL` | EUR/58 | EUR:1:POWER_POOL | +0.33 | -0.06 | +0.0005 | +0.0312 | -0.0033 | **阻断** | ΔF | turnover | OTHER 3→4 否 | —（未进可执行集） |
| 19 | `WjOeNE6O` | EUR/56 | EUR:1:POWER_POOL | +0.54 | +0.38 | -0.0012 | -0.0051 | -0.0031 | **放行** | 补偿放行 | returns | IMBALANCE 3→4 否 / OTHER 3→4 否 | 0 |
| 20 | `RREGX1kd` | GBR/54 | GBR:1:POWER_POOL | +0.33 | +0.21 | -0.0017 | -0.0013 | -0.0001 | **放行** | 补偿放行 | returns | SHORTINTEREST 4→5 否 / ANALYST 3→4 否 | 0 |
| 21 | `Jje6mrpO` | GBR/53 | GBR:1 | +0.09 | +0.06 | +0.0003 | +0.0011 | -0.0003 | **放行** | 通过 | turnover | SHORTINTEREST 4→5 否 / RISK 0→1 否 / FUNDAMENTAL 3→4 否 | 0 |
| 22 | `LLM0e20m` | GBR/53 | GBR:1 | +0.08 | +0.06 | -0.0005 | -0.0010 | -0.0001 | **放行** | 补偿放行 | returns | SHORTINTEREST 4→5 否 / NEWS 3→4 否 | 0 |
| 23 | `rKRRjM51` | IND/53 | IND:1:POWER_POOL | +0.38 | +0.29 | +0.0070 | +0.0122 | -0.0025 | **放行** | 通过 | turnover | INSTITUTIONS 1→2 否 / PV 11→12 否 | 0 |
| 24 | `pwdd7Za6` | GBR/52 | GBR:1:POWER_POOL | +0.30 | +0.20 | -0.0052 | -0.0102 | -0.0007 | **放行** | 补偿放行 | returns | SHORTINTEREST 4→5 否 / PV 4→5 否 | 0 |
| 25 | `rKRx7v6m` | EUR/52 | EUR:1:POWER_POOL | +0.39 | +0.27 | +0.0042 | +0.0086 | -0.0041 | **放行** | 通过 | turnover | SENTIMENT 3→4 否 / OTHER 3→4 否 | 0 |
| 26 | `9qlz29Oe` | DEU/50 | DEU:1 | +0.07 | +0.04 | -0.0006 | +0.0015 | -0.0010 | **阻断** | ΔRet+成本 | turnover | SHORTINTEREST 3→4 否 / NEWS 0→1 否 | —（未进可执行集） |
| 27 | `RREPm361` | DEU/49 | DEU:1:POWER_POOL | +0.73 | +0.31 | +0.0080 | +0.0619 | -0.0326 | **放行** | 通过 | turnover | ANALYST 6→7 否 | 0 |
| 28 | `ZYa6x531` | EUR/49 | EUR:1:POWER_POOL | +0.20 | +0.14 | -0.0026 | -0.0069 | -0.0023 | **放行** | 补偿放行 | returns | EARNINGS 1→2 否 | 0 |
| 29 | `1YNMAA8M` | DEU/48 | DEU:1:POWER_POOL | +0.43 | +0.42 | +0.0098 | +0.0033 | -0.0174 | **放行** | 通过 | turnover | MODEL 3→4 否 / ANALYST 6→7 否 | 0 |
| 30 | `rKRx0M2m` | GBR/48 | GBR:1 | +0.01 | +0.01 | -0.0002 | -0.0002 | -0.0001 | **放行** | 补偿放行 | returns | SHORTINTEREST 4→5 否 / RISK 0→1 否 | 0 |
| 31 | `2r5MqmVJ` | EUR/45 | EUR:1:POWER_POOL | +0.15 | +0.13 | -0.0025 | -0.0082 | -0.0016 | **放行** | 补偿放行 | returns | EARNINGS 1→2 否 | 0 |
| 32 | `Jj8qXO5m` | EUR/45 | EUR:1:POWER_POOL | +0.14 | +0.12 | -0.0024 | -0.0084 | -0.0013 | **放行** | 补偿放行 | returns | EARNINGS 1→2 否 | 0 |
| 33 | `78L5GaeZ` | EUR/43 | EUR:1 | +0.04 | +0.05 | +0.0006 | +0.0007 | +0.0004 | **放行** | 通过 | turnover,drawdown | ANALYST 10→11 否 / OTHER 3→4 否 | 0 |
| 34 | `E56GgqLL` | EUR/43 | EUR:1 | +0.00 | +0.00 | +0.0000 | -0.0013 | +0.0001 | **放行** | 通过 | drawdown | FUNDAMENTAL 3→4 否 / OTHER 3→4 否 | 0 |
| 35 | `d5apEYRx` | EUR/41 | EUR:1:POWER_POOL | +0.17 | +0.14 | -0.0024 | -0.0080 | -0.0017 | **放行** | 补偿放行 | returns | EARNINGS 1→2 否 | 0 |
| 36 | `d5a2vxzY` | DEU/36 | DEU:1 | +0.06 | +0.02 | -0.0010 | +0.0020 | -0.0006 | **阻断** | ΔRet+成本 | turnover | SHORTINTEREST 3→4 否 | —（未进可执行集） |

### 2.2 原 11 颗「已有旧硬闸」候选（方案 D 只作复核，不改变排除结论）

| alpha | 原排除原因 | D 裁决 | 命中层 | ΔS / ΔF / ΔRet | 塔归属→现值→交后→是否新点亮 | 塔边际增量 |
|---|---|:---:|---|---|---|:---:|
| `ZYQv7j2Q` | prod 0.8159 超线；self 0.816 超线 | **放行** | 通过 | +0.55 / +0.27 / +0.0056 | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | 0（已排除） |
| `LLMv6joe` | prod 未闭环 | **放行** | 补偿放行 | +0.07 / +0.05 / -0.0018 | SHORTINTEREST 3→4 否 | 0（已排除） |
| `d5a2aO7v` | prod 未闭环 | **数据缺失** | — | — / — / — | SHORTINTEREST 3→4 否 / INSIDERS 0→1 否 | 0（已排除） |
| `zqdvb0YE` | prod 未闭环 | **放行** | 通过 | +0.68 / +0.52 / +0.0034 | SHORTINTEREST 3→4 否 / INSIDERS 0→1 否 | 0（已排除） |
| `mL617YPx` | 稳健台账 REJECT（submit_gate 硬拦）；稳健台账 REJECT | **阻断** | ΔS | -0.01 / +0.00 / +0.0000 | FUNDAMENTAL 3→4 否 / PV 2→3 点亮 | 0（已排除） |
| `WjOAJWxd` | ΔS=-0.01 硬闸 | **阻断** | ΔS | -0.01 / +0.00 / +0.0000 | ANALYST 10→11 否 / SENTIMENT 3→4 否 | 0（已排除） |
| `qME6VWbj` | ΔS=-0.03 硬闸 | **阻断** | ΔS+ΔRet+成本 | -0.03 / +0.07 / -0.0020 | ANALYST 10→11 否 | 0（已排除） |
| `xArjE96W` | ΔS=-0.03 硬闸 | **阻断** | ΔS+ΔF | -0.03 / -0.02 / -0.0002 | RISK 2→3 点亮 / ANALYST 10→11 否 / SENTIMENT 3→4 否 | 0（已排除） |
| `VkxWmpYG` | ΔS=-0.04 硬闸 | **阻断** | ΔS+ΔF | -0.04 / -0.02 / +0.0002 | ANALYST 10→11 否 / NEWS 3→4 否 / OTHER 3→4 否 | 0（已排除） |
| `N1P02YwL` | ΔS=-0.05 硬闸 | **阻断** | ΔS+ΔF | -0.05 / -0.02 / +0.0002 | RISK 2→3 点亮 / MODEL 3→4 否 | 0（已排除） |
| `N1NGbddg` | ΔS=-0.12 硬闸 | **阻断** | ΔS+ΔF+ΔRet+成本 | -0.12 / -0.09 / -0.0003 | INSTITUTIONS 0→1 否 / ANALYST 10→11 否 | 0（已排除） |

其中 `ZYQv7j2Q` / `LLMv6joe` / `zqdvb0YE` 方案 D 放行，但仍分别被 prod+self 双超线、prod 未闭环、prod 未闭环 + qM7 同族 ρ=1.0 拦住；`d5a2aO7v` 端点 400，判为数据缺失（fail-open，不因「无法证明有害」而放行）。

### 2.3 不在 47 池、但同属本轮方案 D 样本的 2 颗（沿用 19:2x 实测，未重测）

| alpha | ΔS / ΔF / ΔRet / ΔTO / ΔDD | 方案 D | 塔边际增量 | 说明 |
|---|---|:---:|:---:|---|
| `vRAgNK3w` | +0.28 / +0.22 / -0.0040 / -0.0160 / -0.0019 | 放行（补偿） | 不适用 | 调研件，未纳入 12:20 全篮子 47 池，故未做塔核算 |
| `Wjl8Z20O` | +0.31 / +0.25 / -0.0038 / -0.0146 / -0.0020 | 放行（补偿） | 不适用 | 调研件，未纳入 12:20 全篮子 47 池，故未做塔核算 |

另 `P059RmzM` 已于 17:44 ACTIVE，属新闸生效前的历史提交，不追溯、不进池。

## 3 新标准带来的 8 颗变化（旧「可交」→ 现「阻断」）

| alpha | 分区 | 命中层 | 五量要点 | 对原排序的影响 |
|---|---|---|---|---|
| `ZYQ116ln` | KOR:1:POWER_POOL | ΔRet+成本 | S+0.24 F+0.10 Ret-0.0026 TO+0.0035 DD-0.0026 | 原第 3 席 / KOR·PV 点亮者 ⇒ 出局，KOR/D1/PV 本轮无替代 |
| `Jj8VQwoe` | DEU:1 | ΔRet+成本 | S+0.04 F+0.02 Ret-0.0009 TO+0.0003 DD-0.0008 | 同席让位件，现已直接阻断 |
| `JjeNJ00O` | EUR:1 | ΔRet+成本 | S+0.02 F+0.01 Ret-0.0002 TO+0.0023 DD-0.0003 | 原第 8 席 / EUR·RISK 点亮者 ⇒ 出局，改由 `zq3Yrb3G` 接棒 |
| `YP1baJrv` | EUR:1 | ΔRet+成本 | S+0.02 F+0.01 Ret-0.0001 TO+0.0022 DD+0.0003 | prod .6999 差 .0001 本就建议弃，现双重恶化坐实 |
| `qM7KxkQV` | DEU:1 | ΔRet+成本 | S+0.05 F+0.04 Ret-0.0007 TO+0.0001 DD-0.0008 | qM7 族与原 `88NmN37X` 同席，现已直接阻断 |
| `6XMmE0EL` | EUR:1:POWER_POOL | ΔF | S+0.33 F-0.06 Ret+0.0005 TO+0.0312 DD-0.0033 | **旧 ΔS 闸抓不到**：ΔS +0.33 但 ΔF −0.06、ΔTO +0.0312 |
| `9qlz29Oe` | DEU:1 | ΔRet+成本 | S+0.07 F+0.04 Ret-0.0006 TO+0.0015 DD-0.0010 | ΔRet −0.0006 + ΔTO +0.0015 双重恶化 |
| `d5a2vxzY` | DEU:1 | ΔRet+成本 | S+0.06 F+0.02 Ret-0.0010 TO+0.0020 DD-0.0006 | 三闸零余量件，ΔRet −0.0010 + ΔTO +0.0020 |

**净效果层在全篮子终于有区分度**（§7 曾标注「16 颗样本 ΔS/ΔF 全 ≥0，无区分度」这一局限）：46 颗可读件里 ΔS<0 **7 颗**、ΔF<0 **5 颗**、重叠 4 颗；其中 `6XMmE0EL` 是**唯一 ΔS≥0 但 ΔF<0** 的件，正是「ΔTO 上升吃掉收益改善」的典型，旧版只看 ΔS 会误放行。

**配对判据记为分散化补偿 12 颗**（ΔRet<0 且成本同步降）：11 颗最终放行、1 颗 `xArjE96W` 因净效果层 ΔS/ΔF 双负仍被拦；其中 10 颗在 36 池内：`O0A6Qz7p`、`WjOeNE6O`、`RREGX1kd`、`LLM0e20m`、`pwdd7Za6`、`ZYa6x531`、`rKRx0M2m`、`2r5MqmVJ`、`Jj8qXO5m`、`d5apEYRx`。典型 `pwdd7Za6`（ΔRet −0.0052 / ΔTO −0.0102 / ΔDD −0.0007 / ΔS +0.30 / ΔF +0.20）——收益摊薄是等权叠加的机械结果，不是信号变差。

## 4 重排后的可执行顺位（26 颗）

塔边际增量按**新顺位贪心**重算：同塔已被前序候选点亮则为 0。

| # | alpha | 区 | 分 | S/F | ops | prod | self | ΔS / ΔF / ΔRet | 塔归属→现值→交后→是否新点亮 | 塔边际增量 | 待办 |
|---:|---|---|---:|---|---:|---:|---:|---|---|:---:|---|
| 1 | `omEdka3v` | GBR | 92 | 2.51/1.40 | 8 | 0.6026 | 0.492 | +0.59 / +0.25 / +0.0028 | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | **+1** OTHER | 三问 |
| 2 | `wpo8olA6` | DEU | 88 | 1.65/1.27 | 8 | 0.6306 | — | +0.56 / +0.42 / +0.0015 | SHORTINTEREST 3→4 否 / OTHER 2→3 点亮 | **+1** OTHER | — |
| 3 | `leAmmre8` | GBR | 72 | 2.97/1.40 | 9 | 0.6887 | 0.450 | +0.69 / +0.19 / +0.0007 | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | 0 | 三问,prod贴线 |
| 4 | `6XdkW08J` | GBR | 71 | 2.60/1.95 | 8 | 0.6267 | 0.340 | +0.42 / +0.34 / +0.0020 | SHORTINTEREST 4→5 否 / MODEL 6→7 否 | 0 | 三问 |
| 5 | `O0A6Qz7p` | GBR | 64 | 2.18/1.52 | 10 | 0.6984 | — | +0.09 / +0.07 / -0.0004 | SHORTINTEREST 4→5 否 / OTHER 2→3 点亮 | 0 | 三问,prod刷新,prod贴线 |
| 6 | `88NmN37X` | DEU | 62 | 1.79/1.53 | 9 | 0.5541 | — | +0.74 / +0.68 / +0.0058 | SHORTINTEREST 3→4 否 / INSIDERS 0→1 否 | 0 | prod刷新 |
| 7 | `zq3Yrb3G` | EUR | 61 | 2.87/1.65 | 15 | 0.6872 | — | +0.02 / +0.02 / +0.0000 | RISK 2→3 点亮 / ANALYST 10→11 否 / SENTIMENT 3→4 否 | **+1** RISK | 三问,prod贴线 |
| 8 | `Xg9dPpp0` | GBR | 60 | 1.97/1.44 | 9 | 0.4000 | — | +0.42 / +0.33 / +0.0013 | SHORTINTEREST 4→5 否 / RISK 0→1 否 / FUNDAMENTAL 3→4 否 | 0 | 三问,prod刷新 |
| 9 | `mLaLllmK` | EUR | 60 | 3.98/2.21 | 5 | 0.6579 | 0.301 | +0.84 / +0.41 / +0.0053 | OTHER 3→4 否 | 0 | — |
| 10 | `omExeqLb` | GBR | 59 | 2.43/1.78 | 8 | 0.6143 | 0.419 | +0.52 / +0.40 / +0.0036 | SHORTINTEREST 4→5 否 / MODEL 6→7 否 | 0 | 三问 |
| 11 | `WjOeNE6O` | EUR | 56 | 2.90/1.85 | 5 | 0.6411 | 0.641 | +0.54 / +0.38 / -0.0012 | IMBALANCE 3→4 否 / OTHER 3→4 否 | 0 | 三问,prod刷新 |
| 12 | `RREGX1kd` | GBR | 54 | 1.65/1.09 | 9 | 0.5940 | — | +0.33 / +0.21 / -0.0017 | SHORTINTEREST 4→5 否 / ANALYST 3→4 否 | 0 | 三问,prod刷新 |
| 13 | `Jje6mrpO` | GBR | 53 | 2.37/1.58 | 10 | 0.5565 | — | +0.09 / +0.06 / +0.0003 | SHORTINTEREST 4→5 否 / RISK 0→1 否 / FUNDAMENTAL 3→4 否 | 0 | 三问,prod刷新 |
| 14 | `LLM0e20m` | GBR | 53 | 1.75/1.17 | 11 | 0.5386 | — | +0.08 / +0.06 / -0.0005 | SHORTINTEREST 4→5 否 / NEWS 3→4 否 | 0 | 三问,prod刷新 |
| 15 | `rKRRjM51` | IND | 53 | 3.34/2.65 | 7 | 0.6752 | 0.652 | +0.38 / +0.29 / +0.0070 | INSTITUTIONS 1→2 否 / PV 11→12 否 | 0 | prod刷新 |
| 16 | `pwdd7Za6` | GBR | 52 | 1.69/1.04 | 8 | 0.6238 | — | +0.30 / +0.20 / -0.0052 | SHORTINTEREST 4→5 否 / PV 4→5 否 | 0 | prod刷新 |
| 17 | `rKRx7v6m` | EUR | 52 | 3.22/2.14 | 7 | 0.6756 | 0.428 | +0.39 / +0.27 / +0.0042 | SENTIMENT 3→4 否 / OTHER 3→4 否 | 0 | 三问 |
| 18 | `RREPm361` | DEU | 49 | 2.02/1.25 | 5 | 0.6881 | 0.328 | +0.73 / +0.31 / +0.0080 | ANALYST 6→7 否 | 0 | 三问,prod贴线 |
| 19 | `ZYa6x531` | EUR | 49 | 1.74/1.01 | 8 | 0.6964 | — | +0.20 / +0.14 / -0.0026 | EARNINGS 1→2 否 | 0 | 三问,prod贴线 |
| 20 | `1YNMAA8M` | DEU | 48 | 1.58/1.36 | 8 | 0.6951 | — | +0.43 / +0.42 / +0.0098 | MODEL 3→4 否 / ANALYST 6→7 否 | 0 | prod刷新,prod贴线 |
| 21 | `rKRx0M2m` | GBR | 48 | 2.29/1.56 | 11 | 0.6232 | 0.443 | +0.01 / +0.01 / -0.0002 | SHORTINTEREST 4→5 否 / RISK 0→1 否 | 0 | 三问 |
| 22 | `2r5MqmVJ` | EUR | 45 | 1.74/1.03 | 8 | 0.6740 | — | +0.15 / +0.13 / -0.0025 | EARNINGS 1→2 否 | 0 | 三问 |
| 23 | `Jj8qXO5m` | EUR | 45 | 1.74/1.03 | 8 | 0.6663 | — | +0.14 / +0.12 / -0.0024 | EARNINGS 1→2 否 | 0 | 三问 |
| 24 | `78L5GaeZ` | EUR | 43 | 3.02/2.35 | 10 | 0.6662 | — | +0.04 / +0.05 / +0.0006 | ANALYST 10→11 否 / OTHER 3→4 否 | 0 | 三问 |
| 25 | `E56GgqLL` | EUR | 43 | 1.68/1.17 | 24 | 0.5524 | — | +0.00 / +0.00 / +0.0000 | FUNDAMENTAL 3→4 否 / OTHER 3→4 否 | 0 | — |
| 26 | `d5apEYRx` | EUR | 41 | 1.77/1.05 | 8 | 0.6887 | — | +0.17 / +0.14 / -0.0024 | EARNINGS 1→2 否 | 0 | 三问,prod贴线 |

**让位 2 颗**：`pwdLp9z6`（同席 ρ=0.8619）、`xAvK73Qg`（同席 ρ=0.7409）。这两颗方案 D 均放行，仅因同席 ρ≥0.7 让位，不是被新标准否定。

### 塔点亮总账（当季计数 ≥3 才算点亮）

| 塔 | 现值→交后 | 点亮者（新顺位） | 结论 |
|---|---|---|---|
| DEU/D1/OTHER | 2→3 | `wpo8olA6` | 本轮新点亮 |
| EUR/D1/RISK | 2→3 | `zq3Yrb3G` | 本轮新点亮 |
| GBR/D1/OTHER | 2→3 | `omEdka3v` | 本轮新点亮 |
| KOR/D1/PV | 2→3 | — | **失守**：唯一候选 `ZYQ116ln` 被配对判据拦下 |

原报告 4 座塔减为 **3 座**；EUR/D1/RISK 未丢失，只是点亮者从 `JjeNJ00O`（被拦）换成 `zq3Yrb3G`（15 ops / prod .6872 贴线 / 需三问 / ΔRet 0.0000）。

## 5 推荐（两套口径）

| 口径 | 顺位 | 理由 |
|---|---|---|
| 质量分优先（默认） | **`omEdka3v` → `wpo8olA6` → `6XdkW08J`** | `omEdka3v` ΔS +0.59 / ΔF +0.25 / ΔRet +0.0028、prod .6026、self .492、8 ops、点亮 GBR/OTHER；`wpo8olA6` ΔS +0.56 / ΔF +0.42、prod .6306、mix=none 免三问、点亮 DEU/OTHER；`6XdkW08J` 五项全达标（ΔTO −0.0014 / ΔDD −0.0008）、ΔF +0.34、self .3398、prod .6267 有余量 |
| 塔边际优先 | **`omEdka3v` → `wpo8olA6` → `zq3Yrb3G`** | 3 颗覆盖 GBR/OTHER、DEU/OTHER、EUR/RISK 三座不同塔，彼此 ρ < 0.7；代价是第三席 15 ops、prod 贴线、需 refresh 终验 |

**不推荐 `leAmmre8`（纯分数第 3，72 分）**：虽 ΔS +0.69 最高之一，但 ΔF 仅 +0.19、ΔTO **+0.0382** 软告警、prod .6887 贴线、塔增量 0（GBR/OTHER 已被 `omEdka3v` 点亮）、需三问 —— 综合不如 `6XdkW08J`。

⚠ **闸放行 ≠ 推荐提交**：26 颗只是「新旧两套闸都放行」，仍受 prod 缓存 48h 时效、三问签核、当期 themes 资格、REGULAR 每日配额与「只挖不提交」纪律约束；提交由用户点名。

## 6 边界与局限

- `ΔS` 只在**同一分区**内可比：本轮 8 个分区（EUR:1 11 / GBR:1:PP 9 / EUR:1:PP 9 / DEU:1 6 / DEU:1:PP 5 / GBR:1 4 / IND:1:PP 1 / KOR:1:PP 1），表内 ΔS 仅供各分区内部参考，不用于跨区排序。
- `before/after` 是**等权叠加到分区已提交组合**的结果，不是候选自身指标；ΔRet<0 常为机械摊薄。
- 1 颗 `d5a2aO7v` 端点 400 ⇒ `available=False`（fail-open）；它本就被 prod 未闭环 + qM7 同族 ρ=1.0 排除，不影响 26 颗结论。
- 本轮为**只读** `performance_comparison` 实测，未跑 `submit_gate` 完整链路，也未做任何 set_properties / POST；prod/self/稳健/塔计数沿用 12:20 快照，正式提交前须 `refresh=True` 终验。
- 16 颗样本中与 47 池重合的 **14 颗**复测数值逐位一致（无漂移）；`vRAgNK3w` / `Wjl8Z20O` 不在 47 池，见 §2.3，未重测。
- `self` 采用 11-13 重测值覆盖旧缓存：`RREPm361` **.3275**（旧 .6879）、`qM7KxkQV` .5429、`d5a2vxzY` .6038；其余沿用 12:20 快照。
- 塔边际增量按新顺位贪心扣重；未进可执行集的候选标「—（未进可执行集）」，不代表其塔归属为空。

## 7 产物

- 机读逐颗裁决：`results/full_basket_marginal_d_20261113.json`（47 颗 / before / after / Δ五量 / hard_blocked / pair_rule / soft_warnings）
- 本报告重排结果：`results/full_basket_scheme_d_20261113.json`
- 批量实测脚本（带断点续跑、原子写）：`results/_full_basket_marginal_d_20261113.py`
- 报告生成脚本：`results/_full_basket_scheme_d_report_20261113.py`
- 对照基线：`output_report/full_basket_ranking_20261113.md`、`output_report/marginal_gate_v2_20261113.md` §7
