# 归因驱动的中性化修复：omoMKXbJ 一族（2026-10-15）

> 起因：对 `omoMKXbJ`（S1.53 / MARKET 档）做**时期归因**，发现 2Y 卡住不是参数问题而是**因子暴露问题**。
> 据此做**中性化档扫描**验证，结果把 `failed_ra_count` 从 **3 降到 2**，LOW_SHARPE 过闸。

---

## 一、时期归因（归因第 ④ 类）——发现根因

`get_alpha_yearly_stats(omoMKXbJ)`：

| 年份 | Sharpe | 年份 | Sharpe |
|---|---|---|---|
| 2014 | 3.27 | 2019 | 3.76 |
| 2015 | 1.28 | 2020 | 0.80 |
| 2016 | 2.60 | 2021 | 2.03 |
| 2017 | 1.11 | 2022 | 2.24 |
| 2018 | 0.91 | **2023** | **0.08** ← 塌陷 |

- 10/10 年全正，最大单年占比 18.4%（远低于论坛 70% 折扣线）⇒ 无单年依赖
- **但 2023 Sharpe 0.08**，2Y ladder 窗口正好覆盖 2021–2023 ⇒ **这才是 2Y=0.97 的直接原因**

## 二、★ 因子暴露归因（归因第 ① 类）——定位到「因子暴露」而非「信号衰减」

`get_alpha_pnl(omoMKXbJ)` 同时给三列：`pnl` / `risk-neutralized-pnl` / `investability-constrained-pnl`。
用年末快照拆逐年增量（`factor_contrib = raw_delta − RN_delta`）：

| 年份 | raw 增量 | RN(风险中性) 增量 | **因子暴露贡献** |
|---|---|---|---|
| 2019 | 2,490,146 | 1,174,259 | **+1,315,887** |
| 2020 | 866,807 | 767,795 | +99,012 |
| 2021 | 2,594,340 | 867,614 | **+1,726,726** |
| 2022 | 1,920,700 | 222,058 | **+1,698,642** |
| **2023** | **218,963** | **933,901** | **−714,938** ← 翻号 |

### ★★ 判读
- 2021–2022 因子暴露是 **+1.7M 的顺风**；2023 翻成 **−0.7M 的逆风** ⇒ **约 2.4M 的方向性翻转**。
- **2023 的风险中性 PnL 增量 = +934k，是样本 10 年里第 4 好**（仅次于 2019/2021/2022/2016）⇒
  **纯 alpha 在 2023 并未失效，失效的是「因子暴露」这一层。**
- ⇒ 论坛框架原话「若表现完全可被风险因子解释（α≈0）⇒ 收益来自风险补偿」在这里**反向成立**：
  **是负的因子暴露吃掉了正的 alpha。**
- ⇒ **修复方向 = 换中性化档（剥掉因子暴露），不是换字段、不是继续调 decay/window。**

## 三、★ 中性化档扫描（验证修复）——`failed_ra` 3 → 2

同一表达式，只改 neutralization（KOR 全区 11 档合法）：

| 中性化 | S | F | 2Y | subU | inv | **failed_ra** | failed_ppa | 判定 |
|---|---|---|---|---|---|---|---|---|
| MARKET（原档）| 1.53 | 0.94 | 0.97 | 1.39 | 1.14 | 3 | 0 | 基线 |
| **REVERSION_AND_MOMENTUM** | **1.68** | 0.92 | **1.44** | 1.35 | **1.21** | **2** ★ | **0** ★ | **最优** |
| FAST | **1.84** | 0.88 | **1.55** | 1.29 | 1.09 ⚠ | 3 | 1 | 2Y 最高但 INV 告警 |
| SLOW | **1.94** | 0.94 | 1.01 | 1.37 | 1.01 ⚠ | 3 | 1 | S 最高但 2Y 回落 |
| SLOW_AND_FAST | 1.73 | 0.73 | 1.31 | 1.19 | 0.88 ⚠ | 3 | 1 | — |
| STATISTICAL | 1.53 | 0.74 | 0.91 | 1.00 | 0.83 ⚠ | 4 | 1 | — |
| CROWDING | （待回）| — | — | — | — | — | — | — |

### 冠军：`REVERSION_AND_MOMENTUM`（alpha `kqJlRaRz`）
```
vector_neut(trade_when(greater(rank(adv20), 0.1),
  tail(group_rank(multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 140))),
                       rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 132))),
                       rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 252)))),
                   bucket(rank(cap), range="0,1,0.2")), lower=0.2, upper=0.8, newval=0.5), -1),
  power(rank(rsk68_weight_dadv), 0.5))
```
KOR/TOP600/D1 · decay4 · **REVERSION_AND_MOMENTUM** · trunc0.08

| 闸 | MARKET（原）| **REVERSION_AND_MOMENTUM** |
|---|---|---|
| LOW_SHARPE | 1.53 ❌ | **1.68 ✅ 过闸** |
| LOW_FITNESS | 0.94 ❌ | 0.92 ❌（差 0.08）|
| IS_LADDER | 0.97 ❌ | **1.44 ❌（差 0.14）** |
| sub-universe | 1.39 ✅ | 1.35 ✅ |
| investability | 1.14 ✅ | **1.21 ✅** |
| CLUSTER_TEST | 0.97 ✅ | ✅ |
| **failed_ra_count** | **3** | **2** ★ |
| **failed_ppa_count** | 0 | **0** ✅ |

**改进量**：LOW_SHARPE 由 ❌→✅；IS_LADDER 0.97→**1.44（+0.47）**；`failed_ra` 3→**2**；investability 从贴线变干净。

## 四、结论与铁律

### ★ 新铁律 E：**报告期塌陷先做「raw vs risk-neutralized」分解，再决定修什么**
`get_alpha_pnl` 自带 `risk-neutralized-pnl` 列，**零额外成本**。
- 若 `RN 增量 ≫ raw 增量`（差值为负）⇒ **是因子暴露拖累，换中性化档**；
- 若两者同步走弱 ⇒ 才是信号本身衰减（需换字段/换结构）。
**本题属前者**：一次中性化扫描即把 2Y 抬 +0.47。

### ★ 修正：**中性化最优档是「字段族特异」的**
- KOR 旧结论「MARKET 是唯一 F 与 2Y 兼顾档」**只在 `oth695` 贸易流族成立**；
- 在 `pv47` 峰度/防御族，**`REVERSION_AND_MOMENTUM` / `FAST` 明显优于 MARKET**（2Y 0.97→1.44/1.55）。
⇒ **换数据集/换机制族时必须重扫中性化档**（与「结构最优性逐字段实测」同源）。

### ★ `performance_comparison` 工具的正确认知（用户提问）
- 实现 = `GET /{users/self|teams/{id}|competitions/{id}}/alphas/{alpha_id}/before-and-after-performance`
- docstring 明写 **「merged performance check」** ⇒ 它是 **SuperAlpha 合并前后对比**用的，**不是风险因子回归工具**。
- 对普通 IS alpha 返回空 ⇒ 会走 `Cant get performance comparison` 分支并报错（本次 6 次重试失败即此原因）。
- ⇒ **风险因子暴露归因不能靠它**；正确做法 = 用 `get_alpha_pnl` 的 `risk-neutralized-pnl` 列自行分解（本节方法）。

### ★ 相关 skill
| skill | 关系 |
|---|---|
| **`brain-alpha-robustness`** | **主 skill**。Phase B 归因（B.1–B.5）+ Phase C 反过拟合闸（Recent-3yr 制度 / CV_Sharpe / 衰减比 / 平年 / max-min 比）|
| `brain-how-to-pass-alpha-test` | 子宇宙相对公式等平台闸线 |
| `wq-brain-ra-pipeline` | 步 8 调用 robustness；`prod-corr-avoidance.md` |
| `brain-alpha-repair` | `CONDITIONAL` 后的修复轮换 |
| `wq-backtest-monitor` | 提交后核对 / OS 复盘 |

⚠ **按 `brain-alpha-robustness` Phase C 现档计算，`omoMKXbJ`(MARKET) 会被判 REJECT**：
Recent-3yr CV_Sharpe = **0.82**（≥0.60 即 REJECT）、衰减比 = **0.05**（<0.30 即 REJECT）、max/min Sharpe 比 = **28**（>5 即 REJECT）。
⇒ **不宜再按「差一口气」看待**；换中性化后应重跑 Phase C。

## 五、下一步

1. 补齐 `CROWDING` 档结果；
2. 对 `REVERSION_AND_MOMENTUM` 冠军（`kqJlRaRz`）跑 Phase C 完整闸（CV/衰减比/平年/max-min）；
3. 缺口只剩 **F 0.92→1.0（+0.08）与 2Y 1.44→1.58（+0.14）**，量级已从「差 0.61」缩到「差 0.14」⇒ 值得再推一轮（decay/窗口/桶粒度微调 + FAST×REVERSION 折中）。