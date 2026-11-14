# 交付台账 v3：14 颗（两颗主力全部压缩到位）

日期：2026-11-12

## 一、最终 14 颗（互相关全对 <0.7，最大独立集 14）

| # | alpha | 状态 | S | F | 2Y | sub | **ops** | 塔 | eff | 说明 |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---|
| 1 | vR1oxZA3 | ✅ACTIVE | **3.27** | 3.09 | 4.39 | — | — | （无标记）| — | 存量 |
| 2 | **d5apW38x** | 🆕待授权 | **2.36** | **2.04** | 2.67 | **1.54** | **27** | INSIDERS+MODEL | 2 | insiders×analyst（原46→27）|
| 3 | **WjlMlWJd** | 🆕待授权 | **2.21** | 1.84 | 2.40 | **1.43** | **26** | PV+INSIDERS+ANALYST | 0 | insiders×cap×analyst（原44→26）|
| 4 | RREPm361 | 🟡待授权 | 2.02 | 1.25 | 1.82 | — | — | ANALYST | — | 存量 |
| 5 | zq3eb7No | ✅ACTIVE | 2.01 | 1.28 | 1.64 | — | — | ANALYST | — | 存量 |
| 6 | rKRx2Alj | ✅ACTIVE | 1.95 | 1.80 | 2.23 | — | — | MODEL+ANALYST | — | 存量 |
| 7 | 9qlz29Oe | 🟡待授权 | 1.86 | 1.34 | 2.02 | — | — | SHORT+NEWS | — | 存量 |
| 8 | npa9PKWw | 🆕待授权 | **1.74** | **1.52** | 2.66 | 0.94 | **37** | INSIDERS+OTHER | 2 | insiders×other455长窗132 |
| 9 | qM7KxkQV | 🟡待授权 | 1.72 | 1.34 | 2.43 | — | — | SHORT+INSIDERS | — | 存量 |
| 10 | 78Yk8VR1 | ✅ACTIVE | 1.68 | 1.21 | 2.27 | — | — | SHORTINTEREST | — | 存量 |
| 11 | Jj8VQwoe | 🟡待授权 | 1.65 | 1.24 | 2.42 | — | — | SHORT+OTHER | — | 存量 |
| 12 | GrW9OxmG | ✅ACTIVE | 1.62 | 1.56 | 1.93 | — | — | ANALYST | — | 存量 |
| 13 | bl6AvMkN | ✅ACTIVE | 1.61 | 1.36 | 2.15 | — | — | MODEL+ANALYST | — | 存量 |
| 14 | d5a2vxzY | 🟡待授权 | 1.60 | 1.08 | 2.05 | — | — | SHORTINTEREST | — | 存量 |

**互相关**：全对 <0.7，最大独立集 **14**
**合规**：每颗 trio 成员 ≤1 ✓
**算子**：本战役新件 27 / 26 / 37（原为 46 / 44 / 37）

## 二、算子压缩成果汇总（本轮）

| 件 | 压缩前 ops | 压缩后 ops | 降幅 | S 变化 |
|---|---:|---:|---|---|
| d5apW38x（原 XgaGb3J1）| 46 | **27** | **−41%** | 2.36 → 2.36（持平）|
| WjlMlWJd（原 vRA8O57w）| 44 | **26** | **−41%** | 2.14 → **2.21**（+0.07）|

两件都是用同一套手法：**变量赋值去重 + n 元 add + 删外层 signed_power**。

## 三、第二轮压缩的额外发现

`vRA8O57w` 压缩时出现了新现象：**去幂次后 S 不降反升（2.14 → 2.21）**。
而第一轮 `XgaGb3J1` 去幂次是持平的（2.36 → 2.36）。

原因：`vRA8O57w` 外层是**双层 group_zscore**（`group_zscore(group_zscore(x,sector),market)`），
此时 `signed_power(·,1.3)` 再叠加会让尾部过重；去掉后分布更规整，S 反而更好。

同时实测 **`group_zscore(group_zscore(x,sector),market)` 的外层 market 层也是冗余的**：
c1（含外层）与 c2（去外层）指标完全相同（S 2.21 / F 1.84 / 2Y 2.40 / sub 1.43），
但 c2 少 1 个算子。

⇒ **新增规则 R4：双层 `group_zscore(group_zscore(x,g1),g2)` 若外层 g2 是 market，可删（零损失）。**

## 四、缺口 6 颗

| 已判死的新信息源 | 最好 S |
|---|---:|
| model264（380 字段 ML 趋势概率）| 0.74 |
| pattern_scores（504 字段 K 线形态）| 0.56 |

在跑：BE159（pv29 聚类分组轴）、BE160（starmine 新维度 + news18）