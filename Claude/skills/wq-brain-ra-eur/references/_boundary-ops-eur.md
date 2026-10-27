---
name: _boundary-ops-eur
kind: 专题（边界算子清单）
region: EUR
last_verified: 2026-10-20
owner: wq-brain-ra-eur
status: active
---

# EUR 边界算子清单（回测近闸必备）

## 这是什么

EUR 2026-10-20 起废止"探针式"挖矿、改走**全量覆盖**。三道覆盖闸里的第三道（边界算子闸）依赖本清单：**回测一条表达式前必须逐族核对所有边界算子的档位已穷举、且当前表达式的参数落在合法档内**——不允许"用了 decay 但只试过 4"这类"用了一次没试边界"的偷懒。

三道覆盖闸（详见 `tools/full_coverage_gate.py`）：

1. **字段全量覆盖闸**：数据集内每个字段至少出现在 1 条候选表达式里（`field_coverage=1.0`）。
2. **模板族全量闸**：本数据集至少试跑 3 个模板族（`template_families.json` 里被字段画像命中的族）。
3. **边界算子穷举闸**：本波表达式里出现的每个算子，其参数必须落在**本清单列出的合法档**内；近闸候选（过 cheap gate 但没过 RA 的）必须已试完该算子全部档。

本清单是闸 3 的白名单来源，也是文档——不写进这里 = 该档算子不允许出现。

## 为什么要有

2026-08–10 的 EUR 战役反复栽同一个坑：**只测一个"直觉值"的参数**（decay=4、winsorize std=2、ts_mean 252），一次未近闸就换方向、或者只调 decay 从 2 到 5 就判"decay 无用"。实测同一结构在不同参数下 Sharpe 差异常达 0.5–1.5（见 `tracking/EUR/reference/methodology_rules.json` 里的 combo_first_fill 案例），"没扫边界就换方向" = 把可近闸的候选扔进判死池。

## 白名单（EUR 已实测合法档）

以下档位是 EUR 战役**至少跑过一次、且平台接受**的参数。任何表达式里出现下列算子时，参数必须落在档内；不在此表内的档需要**先补一次实测**、把档加进本表后再用。

### 时间序列算子

| 算子 | 合法档位 | 经济语义 | 近闸候选必测档 |
|---|---|---|---|
| `ts_mean` | [1, 2, 3, 5, 12, 22, 66, 132, 252, 504] | 短窗=日内/交易级噪声；中窗=周级；长窗=季/半年级基本面 | 短/中/长 各 1 档 |
| `ts_decay_linear` | [1, 2, 3, 5, 12, 30, 66, 252] | 越短衰减越狠；4–5 是 EUR TOPCS1600 的中位档 | 短 (3) / 中 (30) / 长 (66) |
| `ts_regression` | windows: [252, 504]；rettype: [0] | EUR 季频 13F/财报残差化标配（MEMORY §2） | 两个窗都试 |
| `ts_corr` | [5, 12, 22, 66, 252] | 短=动量；中=季度共振；长=结构性相关 | 短/中 |
| `ts_zscore` | [22, 66, 252, 504] | 归一化窗——见 MEMORY §2 "放大 zscore 窗是破 robust 第二杠杆" | 中/长 各 1 档 |
| `ts_std_dev` | [5, 12, 22, 66] | 短=波动性；中=季度波动 | 短/中 |
| `ts_quantile` | windows: [22, 66]；q: [0.1, 0.25, 0.5, 0.75] | 尾部量化——破 CW 集中墙 | 中窗 + q=0.25/0.75 |
| `ts_rank` | [22, 66, 252] | 相对位置；配合 signed_power | 中/长 |
| `ts_min` / `ts_max` | [5, 12, 22, 66] | 极值 | 短/中 |

### 横截面算子

| 算子 | 合法档位 | 经济语义 | 近闸候选必测档 |
|---|---|---|---|
| `rank` | — (无参数) | 主排名轴 | 默认 |
| `group_rank` | axes: [industry, sector, subindustry, market] | EUR 主轴 = SUBINDUSTRY（settings.json）；换轴降 prod 0.02–0.07 | SUBINDUSTRY / INDUSTRY 必测 |
| `group_zscore` | axes: [industry, sector, subindustry, market, **country**] | 归一后 rank；**country 轴为 other401 pscore 族实测甜点**（`group_zscore(hump(rank(pscore),0.001),country)` → S1.73 F1.26 2Y1.81 T0.0219 prod0.745，该族最接近交付的骨架）；EUR 跨多国（`config.REGION_COUNTRY_SCOPE`）⇒ country 轴有经济含义 | SUBINDUSTRY / INDUSTRY / **country** |
| `group_neutralize` | axes: [industry, sector, subindustry, market, **country**] | 破集中墙 | SUBINDUSTRY / country |
| `bucket` | axes: [industry, sector]；bins: [5, 10, 20] | 离散化（EUR 常用 5） | sector+bins=5 |
| `quantile` | bins: [3, 5, 10, 20] | 分位数离散化 | 5 / 20 |
| `normalize` | axis: [0, 1] | 归一 | 默认 |

### 幂/形变算子（**破 prod 墙核心**）

| 算子 | 合法档位 | 经济语义 | 近闸候选必测档 |
|---|---|---|---|
| `signed_power` | exponents: [1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0] | **MEMORY §2.1 头号破 prod 算子**；1.0–1.4 为 analyst7 修订族甜点（14 颗全过），1.6 起 sub 比率线抬升（sub 0.97 < 线 1.01） | 2.0 / 2.5 / 3.0；本族形态另测 1.0 / 1.2 / 1.4 |
| `power` | exponents: [2, 3] | 无符号幂 | 2 |
| `sqrt` | — | 压尾部 | — |
| `tail` | lower/upper q ∈ [0.1, 0.2, 0.25, 0.3]；newval ∈ [0, 0.5, 1] | 掐中段（宽平台） | q=0.25 / newval=0.5 |
| `winsorize` | std: [0.15, 0.25, 0.3, 0.35, 0.4, 0.5, 0.65, 0.8, 1.5, 2.0, 2.5, 4.0] | EUR 常用 2；MEMORY §2 说 std 越大越保守。**0.15–0.8 为 other401 pscore 族实测档**（2026-10-20：45 颗外层 `winsorize(hump(rank(F),H),std=W)` 全部出有效平台读数）；**std 越大 2Y 越低**（W=0.15→2Y 1.32，W=0.8→2Y 1.22），⇒ 这层是「降 prod / 压 2Y」的双刃，不是纯增益 | 1.5 / 2 / 4；本族另测 0.15 / 0.25 / 0.4 / 0.8 |
| `hump` | thresholds: [0.001, 0.0015, 0.002, 0.0025, 0.003, 0.004, 0.01, 0.02, 0.05] | 掐两端；**必须写命名参数 `hump=k`**（`hump(vec_avg(x), …)` 会 FAIL）。**0.001–0.004 为 other401 pscore 族实测档**，且存在明确权衡：**hump↑ ⇒ prod↓ 但 2Y↓**（0.001→2Y 1.53–1.81 / prod 0.730–0.745；0.002→prod 0.669–0.700 / 2Y 1.36–1.41）；0.01/0.02/0.05 为通用档 | 0.02；本族另测 0.001 / 0.0015 / 0.002 / 0.003 |
| `abs` | — | 绝对值 | — |
| `sign` | — | 符号 | — |

### 事件/条件算子

| 算子 | 合法档位 | 经济语义 | 近闸候选必测档 |
|---|---|---|---|
| `trade_when` | guards: ① 稀疏保护 `returns<thr` / `volume<thr` / `is_nan(cond)`；② **信号体制闸 `abs(ts_zscore(<单字段水平值或原信号>, 66)) > {1.0, 1.5}`** | ① EUR 稀疏数据（13F 季频、财报）必备——`trade_when(returns>0.05, signal, last_value)`；② 修 2Y/CV 弱年：只在「信号异常」时持仓（`Grge2lN3` 2022 年 Sharpe 1.39→2.09、CV .436→.366；`6XAe27eL` 2Y 1.62） | ① 至少 1 次阈值型；② 近闸候选测 1.0 / 1.5 两档（**门槛量必须是单字段水平值**，重复整个 CORE 会顶到 10 算子触发闸 1b-2） |
| `ts_backfill` | windows: [5, 20, 66] | 稀疏数据插值（**MEMORY §2 优先**降 TO 三赢） | 5 / 20 |
| `densify` | window: [3, 5] | 类似 backfill | 3 |
| `if_else` | 条件: any | 硬切换 | — |
| `bucket(rank(x))` | 见 `bucket` | rank 后 bucket | sector |

### 组合算子（**MEMORY 禁用的红线在此**）

| 算子 | 合法用法 | 禁用用法 |
|---|---|---|
| `add` | ① 同源单信号多窗 `add(ts_mean(x,22), ts_mean(x,66))`；② 单腿 + 门控 `add(signal, trade_when(...))` | ⛔ 禁止 `add(multiply(w1,A), multiply(w2,B))` 跨数据集加权相加（`POISON:equal_weight_leg_add`）|
| `subtract` | 同源价差 `subtract(rank(A), rank(B))`（同数据集内、有经济含义） | ⛔ 跨数据集 subtract（`spread_cross_dataset`） |
| `divide` | `divide({flow}, add({stock}, eps))` 事件-信念强度（分母是同一事件的存量+常数，不是两条信号腿）<!-- lint:counterexample --> | ⛔ 除零保护缺失 |
| `multiply` | 单点门控 `multiply(signal, gate_flag)`；单信号内窗加权 | ⛔ 加权腿相加（同 add 禁令） |

## 边界穷举判定（闸 3 的口径）

近闸候选（cheap gate 已过、RA 至少 1 项 FAIL）必须先做完以下"边界扫"才允许判死：

1. **主算子**（表达式里最先出现的那一个）：本清单里该算子全部档已试过至少 2 个（含当前最优）。
2. **时间窗**（`ts_*` 系列）：短/中/长至少 2 档，且**必须包含一个 ≥66d 的长窗**（EUR 数据多为季频/低频）。
3. **中性化轴**（`group_*` 系列）：SUBINDUSTRY + INDUSTRY 至少 2 档（MEMORY §2.1 里 neutralization 换档是**唯一可量化的定向降 prod 手段**，虽不普适但必须实测）。
4. **decay / 衰减**（`ts_decay_linear`）：短 (3) + 中 (30) + 长 (66) 至少 2 档。
5. **形变**（signed_power / tail / winsorize）：至少 2 档；若候选已近 RA 闸，则**必须穷举**本表所有档（这是 prod 破墙的关键动作）。

**违反即闸 3 FAIL**。示例：`rank(ts_decay_linear(x, 4))` 只试过 4 一档就换方向 ⇒ FAIL。合法：`rank(ts_decay_linear(x, {3, 30, 66}))` 三档都跑过。

## 与其它闸的关系

- 闸 1（字段全量覆盖）管"有没有覆盖到"；
- 闸 2（模板族全量）管"覆盖到的方式够不够多样"；
- **闸 3（本清单）管"每种方式的边界有没有穷尽"**。

三道闸共同构成"不允许用探针"的硬语义——单数据集必须做尽，任何一闸不过 = 该数据集当前批次不允许关波。

## 维护

新增算子或档位：
1. 先在 `tracking/EUR/scripts/` 里跑一次实测；
2. 把档加进本表（含 Sharpe/fitness 实测值作 evidence）；
3. 同步 `wq-brain-campaign-toolkit/config/operator_semantics.json`（如需）。

删除档位：仅在实证该档 EUR 全域失效后（≥3 数据集、≥10 波次实测均 |Sharpe|<0.5），并在本表注 `removed_at: YYYY-MM-DD` + 理由。
