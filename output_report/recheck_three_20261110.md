# 三颗评估复核：`qM7KxkQV` / `Jj8VQwoe` / `RREPm361`

> 2026-11-10 22:35｜全部读数本轮实测（非引用旧报告）｜塔计数取 `get_pyramid_alphas` 当季值

## 0 一句话结论

| alpha | 评估状态 | 判定 |
|---|---|---|
| **`qM7KxkQV`** | **已完整评估**（含 op-min：11→8，三颗压缩候选） | 稳健最好、prod 余量最大；但**原件的 11 算子不是最优交付形态** |
| **`Jj8VQwoe`** | **本轮才补齐**（此前 prod 从未取到、无稳健台账、无 ΔS） | **弃**：与今日交付件 `wpo8olA6` 的日收益 **ρ = 0.7372（同席）**，且各项被支配 |
| **`RREPm361`** | 评过，但缺三问与 op-min；本轮补 self/逐年/ΔS/互相关 | 唯一正交件（ρ ≈ 0.06），**但 prod 余量仅 .0119、换手 25%** |

## 1 并排读数（本轮实测）

| 项 | `qM7KxkQV` | `Jj8VQwoe` | `RREPm361` |
|---|---|---|---|
| 家族 | 借券 `shrt3` × 内部人 `insd1_holdings` | 借券 `shrt3` × 有机流量 `oth47` | 分析师盈余 `est_12m_ebi/ebt` |
| **算子** | 11 | 12 | **5** |
| 设置 | decay4 / SUBIND / nanON | decay4 / SUBIND / nanON | **decay0 / FAST / nanOFF** |
| S / F | 1.72 / 1.34 | 1.65 / 1.24 | **2.02** / 1.25 |
| 换手 / margin | 14.3% / 12.15bp | 14.7% / 11.31bp | **25.1%** / **7.64bp** |
| IS Ladder / 2Y | 2.43 / — | 2.42 / — | — / **1.82** |
| Sub-universe | **0.92** | 1.22 | 1.24 |
| CLUSTER | 1.04 | **0.91 ⚠WARNING** | 1.39 |
| **prod**（余量） | **0.5430**（.157） | 0.6124（用户给，.088） | **0.6881**（**.0119**） |
| **self** | 0.5429 | 0.5645 | **0.3275** |
| **ΔS** | **+0.08**（`EQUITY:DEU:1` 常规） | 未测（平台卡） | **+0.73**（`…:POWER_POOL`） |
| mix_audit | `two_leg` ⇒ **需三问** | 未测 | `two_leg` ⇒ **需三问** |
| 稳健 | **PASS** 十年无负年、近3升 1.82→2.27→2.69 | **CONDITIONAL** 2016 **−0.52** 负年 | PASS（台账）／**末段 3.01→2.26→1.29（−43%）** |
| 塔归属 | SHORTINTEREST + **INSIDERS** | SHORTINTEREST + OTHER | ANALYST |

## 2 ★ 当季塔计数（`get_pyramid_alphas`，非全历史）

DEU/D1 当期：**analyst 6（亮）｜model 3（亮）｜shortinterest 3（亮）｜other 2（未亮）｜insiders 0｜fundamental 1｜institutions 1｜sentiment 1**

| 提交对象 | 塔边际（当季） | 是否新点亮 |
|---|---|---|
| `qM7KxkQV` | SHORTINTEREST 3→4；**INSIDERS 0→1** | 否（INSIDERS 走到 1/3），塔增量 **0** |
| `Jj8VQwoe` | SHORTINTEREST 3→4；**OTHER 2→3** | **是（+1）** —— 但 `wpo8olA6` 已占同一席 |
| `RREPm361` | ANALYST 6→7 | 否（已亮），塔增量 **0** |

⚠ **纠正一份旧文档**：`DEU_OS_INVENTORY_AND_DELTA_20261111.md` 按 20 颗全历史 OS 反推塔位（称 OTHER 4 已亮、INSIDERS 1），与平台当季计数不符。塔计数按季度重置，只认 `get_pyramid_alphas`。

## 3 ★ 互相关矩阵（4 年日收益，本地计算，不占 prod 槽）

| | qM7KxkQV | Jj8VQwoe | RREPm361 | **wpo8olA6** |
|---|---:|---:|---:|---:|
| qM7KxkQV | 1 | 0.6292 | 0.0528 | 0.4832 |
| Jj8VQwoe | 0.6292 | 1 | 0.0626 | **0.7372 ✗** |
| RREPm361 | 0.0528 | 0.0626 | 1 | 0.0611 |
| wpo8olA6 | 0.4832 | **0.7372 ✗** | 0.0611 | 1 |

- **唯一超阈值对：`Jj8VQwoe` ↔ `wpo8olA6` = 0.7372** ⇒ 二者同席，只能取一。
- `max_mutually_below_subset` = {qM7KxkQV, Jj8VQwoe, RREPm361} 三颗（不含 `wpo8olA6`）；若把 `wpo8olA6` 计入，则须剔除 `Jj8VQwoe`。
- `RREPm361` 与全部三颗 **0.053–0.063**，是真正的正交增量件。

## 4 `Jj8VQwoe` 为什么弃：被 `wpo8olA6` 支配

同族（`shrt3_bar` × `oth47_organic_traffic`）、同塔（SHORT+OTHER）、ρ 0.737 ⇒ 抢同一席。

| 项 | `Jj8VQwoe` | **`wpo8olA6`（今日 op-min 交付件）** | 胜 |
|---|---|---|---|
| 算子 | 12 | **8** | wpo |
| S / F | 1.65 / 1.24 | 1.65 / **1.27** | wpo |
| Sub-universe | **1.22** | 1.02 | Jj8 |
| CLUSTER | **0.91 ⚠** | 1.15 | wpo |
| 稳健 | **CONDITIONAL**（2016 −0.52） | **PASS**（无负年，近3 2.07/CV .36） | wpo |
| prod | 0.6124 | 0.6306 | wpo |
| ΔS | 未测 | **+0.56** | wpo |

⇒ 六项中五项被压，唯一优势是 sub-universe 1.22。**在同一席上 `wpo8olA6` 是更优解**，`Jj8VQwoe` 标 `SUPERSEDED`。

## 5 顺位建议（若要在 ET 11-10 剩余 2 席里挑）

| 顺位 | 对象 | 理由 | 必须补的动作 |
|---:|---|---|---|
| **1** | **`RREPm361`** | 唯一正交（ρ≤.063）、算子最少（5）、S 最高（2.02）、self 最干净（.3275）、ΔS 最大（+.73） | ① prod `refresh=True` 终验（**.0119 余量，平台漂移即死**）② 三问（两腿：盈余水平 × 盈余修正）③ 接受 TO 25%／margin 7.6bp／末段 −43% 的代价 |
| **2** | **`qM7KxkQV`**（或它的 8 算子件） | 稳健最扎实（十年无负年、近三年递增）、prod 余量最大（.157）、与 `wpo8olA6` ρ .483 可共存 | ① 若要交，交 op-min 后的 **8 算子件**（`d5a2aO7v`），不是 11 算子原件 ② 该件 prod 未终验 ③ 三问 |
| — | `Jj8VQwoe` | 与 `wpo8olA6` 同席 ρ .737，且多数指标被支配 | 不交 |

**塔维度提醒**：这三颗**没有一颗**能在当季点亮新塔（`RREPm361`/`qM7KxkQV` 增量 0；`Jj8VQwoe` 唯一能点 OTHER，但那座塔已由 `wpo8olA6` 覆盖）。选它们是为了**组合正交性**，不是为了塔。

## 6 本轮补齐的记录

- `ledger_kv(DEU, robustness_qM7KxkQV)` = **PASS**（新建，含十年逐年）
- `ledger_kv(DEU, robustness_Jj8VQwoe)` = **CONDITIONAL**（新建，soft_flags: 2016 −0.52 / CLUSTER 0.91）
- `RREPm361` 台账原为 PASS 但 `checked_at`/`report_path` 为空、无 soft_flags —— **记录单薄**，未改动其 verdict，仅在本文补逐年与末段下滑事实
- self 三颗本轮实读：0.5429 / 0.5645 / 0.3275（均 < 0.70）
- ΔS：`qM7KxkQV` +0.08（`DEU:1`）、`RREPm361` +0.73（`…:POWER_POOL`）—— **两个分区，只各自看符号，禁横比**
- `Jj8VQwoe` prod：22:15 首触发 + 22:37 二次长窗口，共两轮（各 ~10 分钟、19–22 次探测）平台**全部返回 `pending`**，peek 亦恒空体；上一轮会话同样卡在此颗。⇒ 平台侧该件 prod 长期不落地，**0.6124 暂记为「用户提供、未实读」**，不写入 `alpha_corr_cache`（避免把未实读值伪装成实测）
