# 库存可提交 alpha 盘点（2026-09-09）

> 口径：平台全量库存拉取（每区封顶 1000 条）+ 零成本本地相关性预筛 + 平台 detail 复核。
> 工具链：`build_gate_prior_from_inventory.py` → 去参数网格 → `select_ra_basket.py` → 点塔档位统计。

## 一、结论速览

| 项 | 结果 |
|---|---|
| 平台过闸(未提交)候选 | **865 条**（GLB 235 / IND 194 / EUR 154 / USA 117 / KOR 98 / GBR 53 / ASI 13 / HKG 1） |
| 去参数网格后独立信号 | **275 条**（压缩 3.1×，名义库存被 decay/权重网格虚高） |
| 与已提交 OS 池(201 条)撞车 | 检测 120 条中 **48 条撞车（40%）**——必卡 SELF_CORRELATION |
| **真正可提交篮子** | **12 条**（两两互相关 <0.7，均通过平台 detail checks 复核） |
| A 档点塔（2/3，一提即亮） | **0 条**——GBR/D1/MODEL、IND/D1/PV 共 6 条候选全部撞车（0.77–0.998） |
| 今日配额（ET 09-09） | **未使用**：REGULAR 4/4、SUPER 1/1 可用 |
| SA 组件池 | KOR 10 ✔ GO / IND 18 ✔ GO / USA 133 ✔ GO |

**一句话：库存还有货，但"能点亮新塔"的 A 档全灭；今天可安全提交 4 颗 REGULAR（都是 B/C 档推进）+ 1 颗 SUPER。**

## 二、可提交清单（12 条，按提交优先级排序）

| # | alpha | 区 | universe | 中性化 | sharpe | fitness | turnover | 2y | 本地maxCorr | 塔 | 档位 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `np8GxqVw` | GLB | MINVOL1M | STATISTICAL | 5.55 | 4.00 | 0.149 | 5.43 | 0.295 | GLB/D1/OTHER | **B(1/3)** |
| 2 | `QP9XRGjp` | USA | ILLIQUID_MINVOL1M | STATISTICAL | 3.15 | 2.51 | 0.112 | 3.46 | 0.511 | USA/D1/EARNINGS | **B(1/3)** |
| 3 | `leWpEJW2` | ASI | MINVOL1M | INDUSTRY | 2.82 | 2.06 | 0.126 | 1.64 | 0.330 | ASI/D1/OTHER | **B(1/3)** |
| 4 | `WjdLwJ8x` | GLB | MINVOL1M | MARKET | 2.35 | 1.80 | 0.049 | 2.34 | 0.404 | GLB/D1/MODEL | C(0/3) |
| 5 | `WjPEg2zd` | KOR | TOP600 | SECTOR | 1.78 | 1.64 | 0.119 | 2.08 | 0.433 | KOR/D1/PV + ANALYST | B(1/3) 副塔 |
| 6 | `MPGM3kkk` | ASI | MINVOL1M | SLOW | 2.94 | 1.76 | 0.084 | 1.76 | 0.330 | ASI/D1/IMBALANCE | C(0/3) |
| 7 | `KP6mqrQ1` | HKG | TOP800 | MARKET | 2.00 | 1.86 | 0.041 | 2.19 | 0.268 | HKG/D1/MODEL | C(0/3) |
| 8 | `QP98PoQW` | USA | TOP3000 | STATISTICAL | 2.22 | 2.40 | 0.087 | 4.13 | 0.498 | USA/D1/SHORTINTEREST | C(0/3) |
| 9 | `pwz8ZOP6` | IND | TOP500 | MARKET | 2.88 | 3.48 | 0.056 | 2.68 | 0.351 | IND/D1/MODEL | 已亮(10) |
| 10 | `gJjNlRMJ` | IND | TOP500 | STATISTICAL | 3.26 | 2.56 | 0.253 | 1.89 | 0.653 | IND/D1/RISK | 已亮(5) |
| 11 | `O0Gj6PqJ` | KOR | TOP600 | SECTOR | 2.83 | 3.39 | 0.091 | 2.48 | 0.297 | KOR/D1/OTHER | 已亮(5) |
| 12 | `QPG1d3xK` | EUR | TOP2500 | INDUSTRY | 2.69 | 2.08 | 0.117 | 2.21 | 0.365 | EUR/D1/MODEL | 已亮(5) |

注：9–12 号指标强但塔已亮，**提了不新增点塔价值**（除非为了 SA 池/多样性）。

**今日 4 颗建议**：`np8GxqVw` → `QP9XRGjp` → `leWpEJW2` → `WjdLwJ8x`（GLB 全域 0 亮，打地基；若想稳一点可换 `WjPEg2zd` 推 KOR/PV）。

## 三、A 档点塔机会：全灭

近 90 天 ACTIVE 统计出的 2/3 塔只有 `IND/D1/PV(2)`、`GBR/D1/MODEL(2)`（MEA 已禁用）。库存里落在这两塔的 6 条候选：

| alpha | 塔 | 撞车对象 | 本地互相关 |
|---|---|---|---|
| O0GrnVpp | GBR/D1/MODEL | vRNk56mz | 0.9108 |
| 2rpOvW7b | GBR/D1/MODEL | vRNk56mz | 0.9970 |
| A1lREYlR | GBR/D1/MODEL | GrlqxwKx | 0.9935 |
| A1GG3neY | GBR/D1/MODEL | WjAV89jG | 0.7736 |
| ZY7X0Jz8 | IND/D1/PV | Wj7YP5JN | 0.9978 |
| N1708Mr8 | IND/D1/PV+ANALYST | 1YzLbZzQ | 0.7831 |

→ **GBR 与 IND 新塔无法从现有库存点亮**，只能靠新挖不同质信号。这与既有结论一致：存量信号空间已被自己已提交的 book 吃满。

## 四、SUPER alpha 机会

| 区 | ACTIVE REGULAR 池 | 判定 |
|---|---|---|
| USA | 133 | GO |
| IND | 18 | GO |
| KOR | 10 | GO（刚达标） |

今日 SUPER 配额 1 颗未用。优先 USA（池最大，降相关空间最足）；注意 SA 的 `IS_LADDER_SHARPE` / `LOW_ROBUST_UNIVERSE_SHARPE` 死区与 selection 三参数（self-gate / turnover 区间 / prod-ceiling）需逐颗核对。

## 五、风险提示

- 本地互相关是**预测**（历史吻合度高，O0GWvzbp 本地 0.9524 → 平台 0.9522）。平台 SELF 会**高于**本地值（N1QMJ10q 本地 0.3972 → 平台 0.5463），故 maxCorr 接近 0.65 的（如 `gJjNlRMJ`）风险最高。
- 硬闸失败**零成本不耗配额**，可放心探测；但 PROD 的 FAIL/WARNING 判定不是纯 0.7 阈值，以实测为准。
- 提交前必补 ≥100 字三段式描述（Idea/Data/Operators），空描述会被网关静默丢弃（201 但停留 UNSUBMITTED）。

## 六、实际提交结果（当日实测）

| alpha | 区/塔 | 提交结果 | 判定原因 |
|---|---|---|---|
| `O0Gj6PqJ` | KOR/D1/OTHER | ✅ **ACTIVE** 04:42 ET | 命中当期主题，走 PPA 通道 |
| `WjPEg2zd` | KOR/D1/PV + ANALYST | ✅ **ACTIVE** 04:46 ET | PPAC>0.5 → 普通通道，指标过硬闸 |
| `np8GxqVw` | GLB/D1/OTHER | ❌ 201→UNSUBMITTED | `PURE_POWER_POOL_THEME FAIL`（区域不命中） |
| `QP9XRGjp` | USA/D1/EARNINGS | ❌ 201→UNSUBMITTED | 同上（PROD 0.7772 仅 WARNING，非拦因） |
| `leWpEJW2` | ASI/D1/OTHER | ❌ 201→UNSUBMITTED | 同上（PROD 0.8218 仅 WARNING） |
| `WjdLwJ8x` | GLB/D1/MODEL | ❌ 403 | SELF/PROD/PPAC 全 PENDING + `CLUSTER_TEST ERROR` |
| `mL5l7Yj9` | KOR/D1/MODEL | ❌ 201→UNSUBMITTED | **`POWER_POOL_SUBMISSION FAIL 1/1`**（当日 PPA 名额已用尽） |
| `wpaAzd25` | KOR/D1/MODEL | ❌ 201→UNSUBMITTED | 同上 |

**当日配额消耗**：`REGULAR_SUBMISSION` 2/4，`POWER_POOL_SUBMISSION` 1/1（均不因失败而消耗）。

### 两条新硬规则（本次实测得出）
1. **PPA 通道有独立日配额 1 颗**（`POWER_POOL_SUBMISSION` limit=1），与 REGULAR 4 颗并行但独立。
   每天**至多 1 颗 PPA**（宽松闸）+ 若干普通通道（PPAC>0.5 且 PROD<0.7 硬）。排当日提交顺序时先提 PPA 那颗。
2. **当期主题命中的是「区域」不是「数据集类别」**：09-01~09-08 全部命中 alpha 均属 **KOR TOP600 / HKG TOP800**
   （ANALYST、SHORTINTEREST、PV+ANALYST 各类别都命中），GLB/USA/ASI 的 PURE-OTHER 候选全灭。
   另：**未提交 alpha 的 `themes` 字段恒空**，无法预判主题，只能零成本实测。

### 下一步（09-10 起）——已按「已点亮塔不重复提交」重排

- **09-10 第一颗（PPA 名额）：`zqYaZ2gO`**（KOR/D1/PV + ANALYST，anl25 目标价族）。
  已零成本验完：SELF 0.3645 PASS、PROD 0.8201 仅 WARNING、PPAC 0.4808（PPA 通道）、
  `MATCHES_THEMES PASS`（命中主题）、IS_LADDER 2.08/2.02 PASS；唯一拦因是当日
  `POWER_POOL_SUBMISSION 1/1` 用尽。**描述已补齐，明日可直接提交 → 点亮 KOR/D1/PV（2/3→3/3）。**
- 剩余 REGULAR 配额**当日不可再用**（PPA 日限已尽，普通通道需 PROD<0.7，库存候选 PROD 0.78+）。
- **SUPER：USA 五变体全废**（详见下表），短期不再试 USA SA。

#### SA 五变体（USA TOP3000/D1，combo-power 5）

| 变体 | 配置 | sh/fit | SELF | PROD | 判定 |
|---|---|---|---|---|---|
| O0r756Zg | INDUSTRY d30 self0.7 | 1.99/2.00 | 0.780 | 0.857 | BLOCKED |
| WjP7aKMP | INDUSTRY d90 self0.5 prodceil0.7 | 1.77/1.49 | 0.744 | 0.844 | BLOCKED |
| O0r7bzVd | STATISTICAL d30 self0.55 to.01-.5 | 1.60/1.19 | 0.7070 | 0.7073 | BLOCKED（差 0.007） |
| 3q9lEgYX | STATISTICAL d90 | 1.17/0.68 | — | — | fitness<1.0 指标崩 |
| E5vlqw91 | STATISTICAL d60 | 1.24/0.73 | — | — | fitness<1.0 指标崩 |

→ USA SA 与既有 2 颗（KPGvRMg1 SUBINDUSTRY d5 / gJ8eVmNM MARKET d5）及生产池同质，
能降双闸的 decay≥60+STATISTICAL 又把 fitness 打到 <1.0。**USA SA 判饱和。**

#### 已排除（违反「不重复点亮」的候选）
`pwz8ZOP6`(IND/MODEL 已亮 10)、`gJjNlRMJ`(IND/RISK 已亮 5)、`O0Gj6PqJ`(KOR/OTHER 已亮 6，已提属浪费)、
`QPG1d3xK`(EUR/MODEL 已亮 5) —— 今后不再往这些塔投入。

- `cache/inventory_candidates_20260909.json`（865 条）
- `cache/inventory_dedup_20260909.json`（275 条独立信号）
- `cache/basket_20260909.json`（12 条可提交篮子）
- `cache/active_pyramids_20260909.json`（77 条近 90 天 ACTIVE 的塔归属）
- `research-data/platform_alphas_snapshot_20260909.json`（平台快照，与本地库 77/77 一致，无需同步）
