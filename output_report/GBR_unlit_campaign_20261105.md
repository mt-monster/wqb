# GBR 未点亮塔战役报告（2026-11-05）

> 目标（用户裁定）：**严格只做未点亮塔**；验收口径 = **近闸候选池**（S≥1.2，或 S≥1.0 且机制清晰）。
> 口径：GBR / TOP700 / D1；设置 **FAST / decay15 / trunc0.05 / nanHandling ON / maxTrade OFF**（未点亮塔实证档）。
> 并发：**2 个 multisim 同时在飞**（`WQB_GLOBAL_SLOTS` 现行 cap=2），每批 8 条（GBR multi-sim 上限）。
> 所有平台取数经 MCP；无临时脚本直连。

---

## 1. 结论摘要

| 项 | 数 | 说明 |
|---|---:|---|
| 本战役提交回测 | **98 条**（12×8 + 2） | 成功产出 **90 条**；W12 的 8 条因 `vec_ir/vec_kurtosis/vec_skewness` 平台不可用整批 ERROR |
| **RA 全闸通过（本轮新增）** | **12 条** | 存量腿 5 条（`O0AA03E1` 1.73/1.10、`qMLL8lPV` 1.72/1.09、`QPvj9m0K` 1.71/1.06、`gJee6MRK` 1.58/1.05、`KPJJLQVj` 1.71/1.08）+ 笔数腿 7 条（`vR11n3xQ` 1.97/1.35、`vR11nwEa` 1.94/1.34、`zq33wKV1` 1.89/1.27、`9qxxPZnx` 1.86/1.26、`Jjee0MAW` 1.70/1.08、`d5WW8kNj` 1.70/1.07、`pwdd7Za6` 1.69/1.04） |
| 历史全闸（10-31，prod 已撞墙） | 1 条 | `leA23Jae` S1.72/F1.08（prod 0.7445，不可提） |
| **近闸候选（S≥1.0，含历史/克隆）** | **约 50 条** | 见 §3；其中 S≥1.2 约 38 条 |
| **独立腿（互相关 <0.7）** | **2 条可用 + 1 条不干净** | 存量腿 ↔ 笔数腿 = **0.2022**；CoV 腿对两者 0.17–0.70（0.7 下三条共存），但 CoV **10 年不干净** |
| 10 年数据校验 | 2 条独立腿通过 | 存量：`O0AA03E1`/`qMLL8lPV`/`gJee6MRK`/`QPvj9m0K`；笔数：`vR11n3xQ`/`9qxxPZnx`；CoV 三条均挂（2015/2017/2020 负） |
| prod / self | **未测** | `check_correlation` / `check_self_correlation` 连续 3 次在 MCP 客户端 30s 上限超时（平台相关性单并发队列）；**未测 ≠ 通过** |
| 可点亮塔 | **0 座新塔** | SHORTINTEREST 需 3 条 10 年干净的独立全闸腿；现有 2 条，第 3 条（CoV）10 年不干净 ⇒ 仍不可点 |

**★ 一句话**：GBR 的 shortinterest 类数据集**已全部看完**（`shortinterest3` 25/25 字段、`risk60` 5/5、`institutions25` 与 `model239` 字段级 cov=0）；shortinterest3 首次出现 **2 条 10 年干净的独立全闸腿（存量、笔数）**，第 3 条轴（CoV/分散度）结构上独立但 10 年不干净 ⇒ **塔仍差一条干净腿，但已不是「无路」**。

> **★ 互相关实测（2026-11-05，`compute_mutual_correlation`，1021 个交易日）**：
> 5 条 RA 全闸候选两两 **0.6635–0.9856**；最大对 `O0AA03E1 ↔ qMLL8lPV` = **0.9856**。
> 0.7 阈值下 `max_mutually_below_subset` = **2 条**（`qMLL8lPV` + `leA23Jae`，0.6966），
> 其余组合全部 >0.7。⇒ **4 条新全闸 + 1 条历史全闸，实际是 1–2 条独立腿**。

---

## 2. 波次明细

| 波 | 数据集 | 条数 | 最好 S | 全闸 | 近闸（≥1.2） | 判定 |
|---|---|---:|---:|---:|---:|---|
| W1 | shortinterest3 | 8 | 1.53（存量水平） | 0 | 1 | PARTIAL |
| W1 | institutions6 | 8 | 0.95（卖家广度） | 0 | 0 | FAIL |
| W2 | risk60 | 8 | 0.80（做空拥挤度） | 0 | 0 | FAIL |
| W3 | shortinterest3 | 8 | **1.73（平滑存量）** | **2** | 6 | PASS |
| W4 | shortinterest3 | 8 | 1.40（平滑市值分母） | 0 | 6 | PARTIAL |
| W5 | shortinterest3 | 8 | **1.72（平滑 _main）** | **2** | 5 | PASS |
| W6 | institutions6 | 8 | 0.94（winsorize 卖家） | 0 | 0 | FAIL |
| W7 | insiders1 | 8 | 0.76（仓位变化比） | 0 | 0 | FAIL |
| W8 | insider_agg_matrix | 8 | 0.73（卖出笔数/笔均） | 0 | 0 | FAIL |

---

## 3. 近闸候选池（约 45 条，S≥1.0；核心 11 条全闸 + 2 条独立腿）

> `RA0` = `ra.failed_ra_count == 0`；`2Y` 为平台 `two_year_sharpe` / `is_ladder_sharpe`；
> `塔`：SI=SHORTINTEREST，RISK，FUND=FUNDAMENTAL，PV；`族` 见 §4；`克隆` = 与同族代表同持仓的概率高（未算互相关）。

### 3.1 全闸（RA0）

| # | alpha | 表达式（简） | S | F | 2Y | TO | SUB | 塔 | 10y |
|---:|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | **O0AA03E1** | `-rank(ts_mean(ts_rank(ts_backfill(vec_sum(loaned_share_count_p5_d1),120),504),22))` | **1.73** | **1.10** | 2.43 | 7.57% | 1.62 | SI | ✅ |
| 2 | **qMLL8lPV** | 同上，`loaned_share_count_main` | **1.72** | **1.09** | 2.54 | 7.59% | 1.60 | SI | ✅ |
| 3 | **QPvj9m0K** | `-rank(ts_rank(ts_backfill(divide(vec_sum(loaned_share_count_p5_d1),ts_mean(volume,126)),120),504))` | **1.71** | **1.06** | 2.73 | 9.16% | 1.80 | SI+PV | ✅ |
| 4 | **gJee6MRK** | `-rank(ts_mean(ts_rank(ts_backfill(divide(vec_sum(loaned_market_value_usd_p5_d1),current_enterprise_value),120),504),22))` | **1.58** | **1.05** | 2.18 | 8.54% | 1.48 | SI+FUND | ✅ |
| 5 | leA23Jae（10-31） | `-rank(ts_rank(ts_backfill(divide(vec_sum(loaned_share_count_p5_d1),ts_mean(volume,22)),120),504))` | 1.72 | 1.08 | 2.60 | 9.95% | 1.79 | SI+PV | 未逐条 |

### 3.2 近闸 S≥1.2（本轮新增，19 条）

| # | alpha | 表达式（简） | S | F | 2Y | TO | SUB | 塔 | 族 |
|---:|---|---|---:|---:|---:|---:|---:|---|---|
| 6 | 1YNNYMbk | `txn_count ÷ ADV22`，ts_rank504 | 1.62 | 0.97 | 2.48 | 10.11% | 1.65 | SI+PV | C |
| 7 | rKRRYlrm | 平滑 `loaned_market_value` 水平 | 1.61 | 0.96 | 2.40 | 7.63% | 1.46 | SI | B |
| 8 | 9qxxYr91 | 平滑 `loaned_market_value_main` 水平 | 1.60 | 0.96 | 2.55 | 7.66% | 1.44 | SI | B |
| 9 | Xg9Ln5ox | `loaned_share_count` 水平（未平滑） | 1.53 | 0.92 | 2.42 | 9.18% | 1.62 | SI | A |
| 10 | zq33ZmJE | 平滑 `loaned_value ÷ market_cap` | 1.52 | 0.90 | 2.17 | 7.59% | 1.52 | SI+RISK | D |
| 11 | O0AA03Eq | `loaned_share_count_main` 水平 | 1.52 | 0.91 | 2.59 | 9.22% | 1.61 | SI | A |
| 12 | leAAdlR8 | 平滑 `transaction_count` 水平 | 1.49 | 0.86 | 1.97 | 7.54% | 1.39 | SI | C |
| 13 | E56blbEP | `loaned_share_count ÷ sharesout` | 1.46 | 0.85 | 2.38 | 9.17% | 1.56 | SI+PV | F |
| 14 | npvvpEJd | `loaned_value ÷ EV` | 1.43 | 0.91 | 2.26 | 10.14% | 1.46 | SI+FUND | E |
| 15 | qMLLMRrO | `-group_rank(ts_rank(level,504), subindustry)` | 1.40 | 0.76 | 2.61 | 9.64% | 1.42 | SI | G |
| 16 | 0mYYOL0G | 平滑 66 `value ÷ market_cap` | 1.40 | 0.80 | **1.56** | 7.00% | 1.37 | SI+RISK | D |
| 17 | mLoA5789 | `loaned_market_value` 水平 | 1.37 | 0.76 | 2.29 | 9.39% | 1.49 | SI | B |
| 18 | ZYQQP9en | `-group_rank(ts_rank(value÷mcap,504), sector)` | 1.36 | 0.77 | 2.41 | 9.09% | 1.63 | SI+RISK | G |
| 19 | qMLdNGgV | `transaction_count` 水平 | 1.35 | 0.75 | 2.10 | 9.17% | 1.46 | SI | C |
| 20 | leAAdlQ8 | 平滑 `loaned_share ÷ EV` | 1.35 | 0.86 | **1.51** | 8.59% | 1.19 | SI+FUND | E |
| 21 | npvvpRoM | `loaned_value ÷ market_cap` | 1.31 | 0.73 | 2.10 | 9.30% | 1.54 | SI+RISK | D |
| 22 | npvvxlME | winsorize `value ÷ market_cap` | 1.31 | 0.73 | 2.10 | 9.30% | 1.54 | SI+RISK | D |
| 23 | mLoowN99 | `value_main ÷ market_cap` | 1.31 | 0.73 | 2.25 | 9.33% | 1.52 | SI+RISK | D |
| 24 | YP11PeKA | `loaned_share ÷ EV` | 1.28 | 0.80 | **1.45** | 10.10% | 1.20 | SI+FUND | E |

### 3.3 近闸 1.0 ≤ S < 1.2（本轮新增，2 条）

| # | alpha | 表达式（简） | S | F | 2Y | TO | 塔 | 族 |
|---:|---|---|---:|---:|---:|---:|---|---|
| 25 | O0AAOZbY | 平滑 `loaned_share ÷ market_cap` | 1.19 | 0.70 | 1.52 | 7.80% | SI+RISK | D |
| 26 | rKRRKgEd | `loaned_share ÷ market_cap` | 1.12 | 0.63 | 1.48 | 9.42% | SI+RISK | D |

### 3.4 历史近闸（10-31 台账，5 条）

| # | alpha | 机制 | S | 备注 |
|---:|---|---|---:|---|
| 27 | leA2lm92 | DTC66 | 1.62 | 同族与 leA23Jae/QPvj9m0K 互相关 ≈0.85 |
| 28 | pwdElM0v | DTC22 + ts_zscore(252) | 1.57 | 同族；ts_rank504 版本更强 |
| 29 | 1YNLorgM | 借券存量水平 + ts_zscore(252) | 1.25 | 未平滑版；本轮平滑版 1.73 |
| 30 | QPvj9gbM | 借贷集中度 CoV + ts_rank504 | 1.18 | 独立机制（VECTOR 内 std/avg） |
| 31 | 6Xd19vpK | 借贷集中度 CoV + ts_zscore(252) | 1.00 | 同族弱版 |

> **池子结构**：31 条里 **24 条来自 shortinterest3 的 4 个字段族**（存量/市值/笔数/集中度），
> 分母族（market cap/EV/sharesout/ADV）只是同一信号的标准化变体。**互相关实测**：
> 5 条 RA 全闸两两 0.6635–0.9856（最大 `O0AA03E1↔qMLL8lPV` 0.9856；`QPvj9m0K↔leA23Jae` 0.8469）；
> 0.7 阈值下只有 `qMLL8lPV + leA23Jae`（0.6966）可共存 ⇒ **全闸集合实际只有 1–2 条独立腿**。
> 由此外推，31 条近闸池的独立腿约 **2 条**，不是 31 条。
> 其中 0mYYOL0G（2Y 1.56）、leAAdlQ8（1.51）、YP11PeKA（1.45）**2Y 未过 ladder**，只能算近闸、不能直接提。

### 3.5 `transaction_count` 族（W9/W10 新增，第二条独立腿）

| # | alpha | 表达式（简） | S | F | 2Y | TO | SUB | 10y |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 32 | **vR11n3xQ** | `if_else(rank(ts_mean(vec_avg(transaction_count_main),5))>0.9, nan, -group_rank(vec_avg(transaction_count_main), subindustry))` | **1.97** | **1.35** | 1.96 | 10.85% | 1.62 | ✅ |
| 33 | **vR11nwEa** | 同上，`_p5_d1` | **1.94** | **1.34** | 2.01 | 11.18% | 1.60 | 未逐条 |
| 34 | **zq33wKV1** | 同上，mask 0.95 | **1.89** | **1.27** | 1.76 | 10.06% | 1.56 | 未逐条 |
| 35 | **9qxxPZnx** | 无 mask：`-group_rank(vec_avg(transaction_count_main), subindustry)` | **1.86** | **1.26** | 1.75 | 9.06% | 1.57 | ✅ |
| 36 | **Jjee0MAW** | mask 0.8 | **1.70** | **1.08** | 1.73 | 12.26% | 1.24 | 未逐条 |
| 37 | d5WW8kNj | 存量 `ts_decay_linear(...,22)` | **1.70** | **1.07** | 2.49 | 7.78% | 1.62 | 未逐条 |

**互相关（MCP 实测，1021 日）**：`vR11n3xQ` ↔ `O0AA03E1` = **0.2022**，↔ `QPvj9m0K` = 0.1994，
↔ `d5WW8kNj` = 0.206；族内（1.97/1.94/1.86）两两 **0.88–0.96**。
⇒ **`transaction_count` 是与 `loaned_share_count` 真正独立的第二条腿**；0.7 阈值下
`max_mutually_below_subset = [vR11n3xQ, O0AA03E1]`（2 条）。

### 3.6 CoV / 分散度族（W11/W12，第三条独立轴）

| alpha | 表达式（简） | S | F | 2Y | TO | 10y |
|---|---|---:|---:|---:|---:|---|
| LLMMqLwv | `vec_stddev(loaned_market_value)/vec_avg` + ts_rank504 | 1.34 | 0.66 | 2.46 | 15.69% | ❌ 2017 −92,913 / 2020 −46,042 |
| kqNNbqMP | `vec_stddev(loaned_share_count)/vec_avg` + 平滑 22 | 1.32 | 0.70 | 2.11 | 7.95% | ❌ 2017 −105,499 / 2020 −182,903 |
| e755g7Z6 | `vec_stddev(transaction_count)/vec_avg` | 1.31 | 0.70 | 2.06 | 12.77% | 未逐条（族同型） |
| d5WWg5PJ | `vec_stddev(loaned_share_count)/vec_avg` | 1.23 | 0.58 | 2.48 | 15.52% | ❌ 2015 −73,211 / 2017 −108,705 / 2020 −201,751 |

**互相关**：CoV 族 vs `vR11n3xQ` = **0.17–0.20**；vs `O0AA03E1` = **0.596–0.695**（贴线 <0.7）；
族内 0.79–0.96。0.7 阈值下 `max_mutually_below_subset = [d5WWg5PJ, vR11n3xQ, O0AA03E1]` = **3 条**。
⇒ **结构上确实存在第 3 条独立轴，但该族 2015/2017/2020 三年负 pnl，不过「近十年每年 pnl>0」**，
按用户约束**不能作为点塔腿**。

补充（W13）：`vec_range` 可用，`vec_range/vec_avg` 版 `LLMM6E52` S1.28/F0.67/2Y2.64、
`Xg99LV91` S1.31/F0.70/2Y2.68，与 CoV 同族、同为 near-gate；`vec_ir` / `vec_kurtosis` / `vec_skewness`
平台报 `inaccessible or unknown operator`（W12 整批 ERROR）⇒ 高阶矩方向不可用。

补充（W14 · regime 门控）：用同数据集内的 regime 变量做 `if_else` 门控（市场 SI 水平 / 交易活跃度 /
分散度 66d vs 252d / 费率水平 / 22d vs 252d），8 条最好 `WjOONrZd` **S1.50/F0.93，但 2Y0.98**；
`pwddnb2j` 1.46/0.90（2Y1.39）、`ZYQQjVJ3` 1.39/0.79（2Y2.52）、其余 0.38–1.29。
⇒ **门控不能把 CoV 推过全闸，反而普遍降 S；第三腿封盘**。
**最终裁定**：SHORTINTEREST 塔在「近十年每年 pnl>0」约束下只有 **2 条干净独立全闸腿**
（存量腿 + 笔数腿）；第 3 条轴（CoV/分散度）结构独立但 10 年不干净且门控修不动 ⇒ **塔仍不可点亮**。

### 3.8 算子变换（W15，论坛/ideas 取证）

**论坛/ideas 来源**（`search_forum_posts` 实读）：
- `signed_power` 操作符完全指南（post `41172652474519`）：`signed_power(x,0.5)` 约 +10%，但过度使用有过拟合风险；
- HKG PV 三重组合（post `41553665016983`）：`rank(winsorize) + ts_quantile(252) + signed_power(0.5)`；
- `ts_target_tvr_decay` 深度解析（post `41718984534551`）：控换手不伤方向，`target_tvr=0.05, lambda_min=0, lambda_max=1~5`；
- shortinterest3 欧洲札记（post `43636685645975`）：券池利用率 >90% 的做空动能衰竭；
- “When Short Sellers Do Not Short”（SSRN 4826241，post `43668758984983`）：看空头**停止**而非水平。

**应用到近闸候选的结果（7 条）**：

| 变换 | 基式（S/F） | 结果 | 判定 |
|---|---|---|---|
| `signed_power(x,0.5)` | CoV 分散度 1.34/0.66 | `d5WWQoWv` **1.45/0.82** | +0.11 S，仍 near-gate |
| `ts_target_tvr_decay(0.05)` | CoV 分散度 | `KPJJLQgj` 1.32/0.70 | 无增益 |
| `quantile` | CoV 分散度 | `e755rvag` **1.45/0.84/2Y2.18** | +0.11 S，仍 near-gate |
| **`signed_power(x,0.5)`** | txn÷ADV 1.62/0.97 | **`pwdd7Za6` 1.69/1.04/2Y2.49/RA0** | ✅ **全闸，10 年全过** |
| `ts_target_tvr_decay(0.05)` | value _main 1.60/0.96 | `zq33W0dd` 1.57/0.93 | 无增益 |
| `signed_power(x,0.5)` | value _main 1.60/0.96 | `9qxxRmle` 1.60/0.97 | F 仍差 0.03 |
| `ts_target_tvr_decay(0.05)` | loan count 1.73/1.10 | `KPJJLQVj` **1.71/1.08/2Y2.41/RA0** | ✅ 全闸（等价于 `ts_mean(22)`） |

**结论**：
1. **`signed_power(0.5)` 是可靠的外层放大器**：在 txn÷ADV 近闸上 +0.07 S / +0.07 F，直接过全闸；在 CoV 上 +0.11 S，但不够；
2. **`ts_target_tvr_decay` 对低换手（TO 7–10%）没有增益**——它解决的是高换手问题，本区候选 TO 已在 7–10%，不适用；
3. **`quantile` 与 `signed_power` 对 CoV 的增益同量级（+0.11 S）**，但 CoV 的 10 年问题不是权重形状问题，变换救不动；
4. **verifier 算子表不含 `ts_quantile` / `ts_max_diff` / `ts_decay_linear`**（报“表达式不完整”），
   且 `tools_sim.py` 的 `failed_expressions` 键是 **1-based**（`str(i+1)`）——排查时别按 0-based 读错位。

### 3.7 shortinterest 类数据集全集（2026-11-05 实读）

| 数据集 | 类别 | 字段数 | GBR/TOP700 字段覆盖 | 结论 |
|---|---|---:|---|---|
| **shortinterest3** | shortinterest | 25 | 0.8217–0.8719 | ✅ 唯一有数据、唯一产出 |
| **risk60** | risk | 5 | 0.6694 | ✅ 已测（W2，上限 0.80） |
| institutions25（Fund Short Selling） | institutions | 24 | **0.0（逐字段）** | ❌ 无覆盖 |
| model239（Short Selling Model） | model | 29 | **0.0（逐字段）** | ❌ 无覆盖 |

**shortinterest3 的 25 个字段已全部测过**（三套变体裸名/`_main`/`_p5_d1`）：
- 借券存量 / 借券市值 / 借贷笔数 → **前两条独立腿**（S1.35–1.97，全闸）；
- 借贷久期、费率水平（mean/max/min）、费率波动、max−min 价差 → **全弱（−0.66 ~ 0.58）**；
- `shrt3_bar` 评级 → **0.05**（判死）；
- 借贷集中度 CoV / 分散度（`vec_stddev`、`vec_range`、`vec_ir`、`vec_kurtosis`、`vec_skewness`）→ **第三条轴，S1.23–1.34，但 10 年不干净**。

---

## 4. 机制归因（本轮最重要的可迁移结论）

### 4.1 ★★★ 平滑结构：`ts_mean(ts_rank(x,504), 22)` 是未点亮塔的通用放大器

同一字段，只加一层 `ts_mean(...,22)`：

| 字段 | 未平滑 S/F/TO | 平滑后 S/F/TO | Δ |
|---|---|---|---|
| `loaned_share_count`（存量） | 1.53 / 0.92 / 9.18% | **1.73 / 1.10 / 7.57%** | **+0.20 / +0.18 / −1.6pp** |
| `loaned_share_count_main` | 1.52 / 0.91 / 9.22% | **1.72 / 1.09 / 7.59%** | +0.20 / +0.18 / −1.6pp |
| `loaned_market_value` | 1.37 / 0.76 / 9.39% | **1.61 / 0.96 / 7.63%** | +0.24 / +0.20 / −1.8pp |
| `transaction_count` | 1.35 / 0.75 / 9.17% | 1.49 / 0.86 / 7.54% | +0.14 / +0.11 / −1.6pp |
| `value ÷ market_cap` | 1.31 / 0.73 / 9.30% | 1.52 / 0.90 / 7.59% | +0.21 / +0.17 / −1.7pp |
| `value ÷ EV` | 1.43 / 0.91 / 10.14% | **1.58 / 1.05 / 8.54%** | +0.15 / +0.14 / −1.6pp |

**机理**：`ts_rank(…,504)` 是重尾、有结构断点的借贷数据的稳健标准化，但逐日仍会跳；
`ts_mean(…,22)` 把「日度排序」变成「月内平均排序」，**降换手、提 fit、不牺牲 S**。
与 10-31 的「`ts_rank(504)` 只放大不创造」互补：**平滑是第二个独立放大器**。

**边界**：`ts_mean(...,66)` 对 `value ÷ market_cap` 只到 1.40 且 2Y 1.56（差 ladder 0.02）⇒ **22 优于 66**；
对 institutions6 的季度字段，平滑 66 反而从 0.95 降到 0.86 ⇒ **平滑窗必须匹配字段更新频率**，不能跨集照搬。

### 4.2 分母必须与字段类型匹配（续 10-31 结论）

| 分母 | 代表 | S | 解释 |
|---|---|---:|---|
| ADV（含交易活跃度） | QPvj9m0K / 1YNNYMbk | **1.71 / 1.62** | 「几天能平仓」有物理意义 |
| market cap（规模） | npvvpRoM | 1.31 | 只有「占市值比例」，弱于 DTC |
| EV（估值） | npvvpEJd / gJee6MRK | 1.43 / **1.58** | EV 分母 + 平滑可全闸，且不占 PV 配额 |
| sharesout（股本） | E56blbEP | 1.46 | 真 SIR，弱于 DTC |
| 笔数/存量（集内比率） | E5665WbK | −0.68 | 单笔规模是噪声，不是信号 |

### 4.3 institutions6：天花板 0.94，结构性不可达 1.0

本轮 16 条 institutions6（8 机制 + 8 结构轴）全部 ≤0.95：
纯 sellers 0.95 / zscore 0.89 / winsorize 0.94 / 平滑 0.86 / 窗口 252 0.79 / group_rank 0.24 / holders 0.19 / buyers −0.14。
⇒ **卖家家数广度是真实机制（2Y 2.17），但强度上限就在 0.95**；任何结构/窗口/分组都不能把它推过 1.0。
**结论**：institutions 塔在本区不可点亮，后续不要再投。

### 4.4 risk60：`rsk60_crowding` 是有效但弱的负向机制

| 表达式 | S | 2Y |
|---|---:|---:|
| `-crowding`（做空拥挤度） | 0.80 | 0.22 |
| `+crowding`（符号对照） | **−0.80** | −0.22 |
| `crowding ÷ offer` | 0.80 | 0.22 |
| `offer` 水平 | 0.58 | 0.48 |
| `offer − bid`（dealer 价差） | 0.53 | 0.51 |
| `offer ÷ bid` | −0.74 | −1.08 |
| `ts_std_dev(offer,66)` | −0.15 | −0.93 |

⇒ 符号完美镜像，机制真实；但**费率/价差/波动率全弱**，最大 0.80，**无近闸候选**。
**结论**：risk60 只能作为门控腿/对照，不能作主信号。

### 4.5 insiders：两集全灭，上限 0.76

- `insiders1`（本轮首次实测，9 字段）：仓位变化比 0.76 / 金额强度 0.71 / 平滑 0.59 / 显著性加权 0.54 / 持股变化 0.26 / 总股数 0.25 / 显著性水平 −0.04。
- `insider_agg_matrix`（34 字段，8 机制）：卖出笔数/笔均 0.73 / 卖买比 0.67 / 高管卖买比 0.64 / 董事直接卖买比 0.62 / 买买比 0.44 / 方向指标 0.30 / 显著交易集中度 −0.52 / 净买入比 −0.59（符号反）。
⇒ **INSIDERS 塔在 GBR 结构性不可达**，与 10-31 的 0.51 上限一致。

### 4.6 sentiment：三集全灭（沿用 10-31）

sentiment27 / sentiment7 / sentiment33 在 10-31 已全判死；本轮未再投主预算。

---

## 5. 约束遵守情况

| 约束 | 执行 |
|---|---|
| 只用未点亮塔 | ✅ 全部 9 塔 / 17 集；无一条已点亮塔主信号（分母 current_enterprise_value=fundamental、alternative_market_cap_usd=risk 均为未点亮塔/非 PV-MODEL-OTHER） |
| PV/MODEL/OTHER 两两组腿禁令 | ✅ 无 PV+PV / MODEL+MODEL / OTHER+OTHER / PV+MODEL / PV+OTHER / MODEL+OTHER |
| PV+其它 category ≤5 | ✅ 本轮用了 **3 条**：`txn÷ADV`（1YNNYMbk）、`share÷sharesout`（E56blbEP）、`DTC126`（QPvj9m0K）；剩余 2 个配额留给后续 DTC22/66 |
| ATOM（单数据集） | 31 条中 **14 条纯 shortinterest3 单集**；其余为 SI+RISK / SI+FUND / SI+PV 双塔（非 ATOM，但均在禁令之外） |
| 近 10 年数据 | 4 条全闸逐条 `get_alpha_yearly_stats` 全过；其余近闸候选**尚未逐条校验**（见 §6） |
| 并发 ≤2 | ✅ 2 个 multisim 同时在飞，8 条/批 |
| prod 用 MCP | ⚠ 已调用 `check_correlation` 3 次，均在 30s 客户端上限超时；**未取到值，不记通过** |

---

## 6. 未完成 / 风险

1. **prod/self 未测**：`check_correlation` 与 `check_self_correlation` 在 MCP 客户端 30s 上限超时（平台相关性单并发队列 + 本地 OS 池计算）。
   按 10-31 教训，**prod 未测 = 未定**；4 条全闸候选可能撞生产池（同族 `leA23Jae` 已实测 0.7445）。
   **下一步**：队列空闲时对 4 条逐条 `check_correlation(refresh=True)`；不要并发。
2. **同族克隆（已实测）**：5 条 RA 全闸两两 0.6635–0.9856，0.7 阈值下 `max_mutually_below_subset` 只有 2 条
   （`qMLL8lPV` + `leA23Jae` 0.6966）；`O0AA03E1↔qMLL8lPV` 0.9856、`QPvj9m0K↔leA23Jae` 0.8469。
   31 条近闸里 24 条来自同一数据集的 4 个字段族 ⇒ **可提独立的只有 1–2 颗**；
   进入提交前必须按 `compute_mutual_correlation` 的结果去重，**一个机制族最多取 1 颗**。
3. **2Y 卡线**：0mYYOL0G（1.56）、leAAdlQ8（1.51）、YP11PeKA（1.45）未过 ladder；只能作为「近闸」，不能直接提。
4. **2020 年近零 PnL**：qMLL8lPV 2020 年 pnl 仅 1,380（其余年份均正）；10 年校验形式上通过，但**该年几乎不赚钱**，稳健性审计时要单独看。
5. **institutions / risk / insiders / sentiment 判死**：本轮用 64 条新证据再次确认；后续不要再派发这些集的探针（除非平台数据更新）。

---

## 7. 后续建议（按 ROI 排序）

1. **先做 prod 终验**（4 条全闸，串行）：`O0AA03E1` / `qMLL8lPV` / `gJee6MRK` / `QPvj9m0K`。
   若 `O0AA03E1`/`qMLL8lPV` prod <0.7，它们就是本战役唯一可提篮（同族只取 1 颗）。
2. **同族去重**：`compute_mutual_correlation([4 条 + leA23Jae], 0.7)`，取 `max_mutually_below_subset`。
3. **补 2 条 PV 配额**：若需要第二条 DTC 轴，用 `DTC22`（leA23Jae 已测 1.72）与 `DTC66`（leA2lm92 1.62），
   但同族只能提 1 颗，**不建议再花配额**。
4. **不重开**：institutions6 / risk60 / insiders1 / insider_agg_matrix / sentiment27 / sentiment7 / sentiment33 /
   earnings6 / option1 / macro27 / socialmedia12 / socialmedia5 / risk68 / risk71 / risk72 / imbalance5。
5. **可迁移经验**（写进下一区）：
   - 「水平值 + `ts_rank(504)` + `ts_mean(22)`」是稀疏借贷/持仓类字段的通用三段式；
   - 平滑窗必须匹配字段更新频率（日频 22、季频 66 反而伤）；
   - 分母必须含交易活跃度（ADV）或估值（EV），纯规模分母（market cap/sharesout）次之；
   - 家数类字段（institutions6）是拥挤度代理，上限低；内部人字段在 GBR 无方向性。

---

*生成：2026-11-05；数据源：`mcp__wq-brain-http__*` 平台实读 + `mcp__wqb-db__*` 台账；回测设置见文首。*
