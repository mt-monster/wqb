# 近十日 alpha 全量值得提交排序清单（2026-11-16 19:18 刷新版）

> 窗口 2026-11-06 ~ 11-16 GMT+8。基线 = `candidate_inventory_20261115.json`（202 颗，11-15 13:20 快照），
> 叠加 11-15~16 的提交（OS 列表 MCP 实读）+ 今日 op-min/repair 新发现，按项目铁律重判。
> **只挖不提交**——本清单是提交建议，提交权归用户。数据源全走 MCP（get_user_alphas / batch_get_alpha_metrics / get_pyramid_alphas / check_correlation）。
>
> **【19:18 vs 17:10 三处变化】**
> ① `wponnkmd` 已 ACTIVE（ET 04:06），从 A 档移除；塔 `USA/D1/EARNINGS` 平台已刷新 **2→3 点亮兑现**。
> ② `blaoQ6Kq`（blaoMOAq 的 CW 修复件）点名提交时 **prod 0.9405 ≥0.7 撞墙，判死未交**——CW 修好但 prod 是终极硬闸。
> ③ `gJaR8e0J`（同族备选）prod 计算 inflight>7min 未完成，挂 pending。
> ④ ET 11-16 REGULAR 配额 **2/4（剩 2）**，未变。

## 0 判据与口径

**判序**：台账 REJECT → 硬闸（prod≥0.7 否决 / self≥0.7 / RA 全闸 / prod 缓存 >48h 作废）→ 塔边际 → 六维 → 指标。
- **塔边际**：点亮（2→3）> 未亮席加 1（1→2）> 已亮席（0）。混塔按木桶短板倍率。
- **六维**：T3/T4 新算子/新字段是硬收益；T1/T2 软成本。优先级 **塔 eligibility > 六维**。
- **prod 贴线**（余量 <0.05）标高危；清单 prod 多为 11-15 权威缓存（~30h，48h 内），提交前须当刻 refresh。

**塔计数（19:18 `get_pyramid_alphas` 显式季度日期实读，逐 region 块对齐）**：
USA: OTHER=4(亮) / EARNINGS=**3(亮 ← wponnkmd)** / MODEL=4 / ANALYST=6 / RISK=3(亮) / INSTITUTIONS=1 ｜
GBR: OTHER=2 / MODEL=6(亮) / SHORTINTEREST=4(亮) / ANALYST=3 / NEWS=3 / PV=4 / **SENTIMENT=0** ｜
IND: EARNINGS=3(亮) / PV=12(亮) / NEWS=4 / OTHER=4 / ANALYST=3 / SENTIMENT=1 / INSTITUTIONS=1 ｜
KOR: INSIDERS=2 / ANALYST=4(亮) / SHORTINTEREST=4(亮) / PV=2 / MODEL=3 ｜
EUR: OTHER=3(亮) / SENTIMENT=3(亮) / ANALYST=10(亮) / MODEL=3 / NEWS=3 ｜
DEU: ANALYST=6(亮) / SHORTINTEREST=5(亮) / MODEL=3 / FUNDAMENTAL=3。

## 1 已提交（S0，排除）—— 近十日 ACTIVE（OS 实读）

| id | ET 提交时间 | 塔 | 备注 |
|---|---|---|---|
| **wponnkmd** | 11-16 04:06 | USA/EARNINGS 3 点亮 | 本会话，塔已刷新兑现 |
| Jj85OR7e | 11-16 00:00 | KOR/INSIDERS 2（未亮） | 本会话 |
| 88N6OOP7 | 11-15 21:39 | — | 非本会话（2rAQ6mQN 孪生源） |
| akaWd90w | 11-15 21:35 | DEU/FUNDAMENTAL | 非本会话 |
| O0Wkvqgd | 11-15 02:14 | IND/EARNINGS 3 点亮 | 本会话 |
| KPg60XNp | 11-15 01:25 | KOR（SUPER） | 非本会话 |
| bla2k0Jq | 11-15 00:53 | USA/OTHER 3 点亮 | 本会话 |
| A1xJdOmg | 11-14 07:27 | USA | 非本会话（多条 self top） |
| pwaQ0bx3 / wpo8olA6 / Wjl6JJQO / P059RmzM / d5a2aO7v / e75avmq6 / E5Q7RGNR / XgaG2Vom / 9qlZLVNd / P0oolrZq / QPv88bJW / O0W0w3P7 / 78Yk8VR1 / E5QZ1NgJ / 0mY1QPEv / d5WGG5bg / rKRx2Alj / akK9ooZv / P0obGoQJ / 3qompGeZ / bl6KwjwK / RRE5Mwkn | 11-08~11-14 | 多区 | 非本会话，近十日 ACTIVE |

> ⚠ 已提交件的同骨架未提交变体全部封死（self≥0.99）：MP65Lx5k/O0W5x9mR/KPg...（Jj85OR7e 族）、O0Wkvqgd 的 12 个消融、bla2k0Jq 的孪生、`e7adKz7g`/`VkN22b9G`（wponnkmd 族，SUPERSEDED）。

## 2 ★ 值得提交排序（A/B/C 档）

### A 档：塔边际正 + 全闸通过（优先交）

| # | id | region | S/F/2Y/sub | prod | self | 塔六元组（席位｜倍率｜当季→交后｜点亮｜边际） | ops/fields | 判据 |
|---:|---|---|---|---|---|---|---|---|
| 1 | **omEdka3v** | GBR | 2.51/1.40/2.37/2.46 | .6026 | .4164 | GBR/OTHER｜1.6(短板1.2)｜2→3｜**点亮**｜**+1** | 8/2 | 现 A 档第一；指标强、prod 余量足；混塔短板 1.2；ops 8 软线。下一顺位 |
| 2 | **pwdLp9z6** | GBR | 2.26/1.19/2.09/2.19 | .6483 | .4754 | GBR/OTHER｜1.6(短板1.2)｜2→3｜点亮｜+1 | 8/? | 与 #1 同席互斥，二选一；F 余量薄 |

> A 档原第 1 `wponnkmd` 已提交移除。GBR/OTHER 是唯一仍可点亮（2→3）的席位；`omEdka3v` 优于 `pwdLp9z6`（S/F 更高、prod 余量更大），优先前者。

### B 档：全闸通过但塔边际 0（指标强，机动备选）

| # | id | region | S/F/2Y/sub | prod | self | 塔六元组 | 六维 / 判据 |
|---:|---|---|---|---|---|---|---|
| 3 | 6XdkW08J | GBR | 2.60/1.95/2.55/2.12 | .6267 | .3393 | GBR/SHORTINTEREST 4 亮 + MODEL 6 亮 → 边际 0 | 指标最强档之一；ops 8 软线 |
| 4 | rK7Qm6ld | IND | 2.15/1.20/3.45/1.19 | .5634 | .2514 | IND/SENTIMENT 1→2 未亮(×1.2) + PV 12 亮(短板×1.1) → 边际 0 | prod 余量最大(.137)；2Y 3.45 极强 |
| 5 | mLaLllmK | EUR | 3.98/2.21/1.93/2.22 | .6579 | .3014 | EUR/OTHER 3 亮 → 边际 0 | S 最高；prod 贴线 |
| 6 | omExeqLb | GBR | 2.43/1.78/2.12/2.14 | .6143 | .4195 | GBR/MODEL 6 亮 → 边际 0 | 稳；ops 8 软线 |
| 7 | LL5Edbee | IND | 2.53/1.78/2.79/1.42 | .6327 | .6338 | IND/INSTITUTIONS 1→2 未亮 → 边际 0 | self .6338 贴软线 .55 |
| 8 | rKRx7v6m | EUR | 3.22/2.14/2.07/1.84 | .6756 | .4279 | EUR/SENTIMENT+OTHER 均亮 → 边际 0 | prod 贴线 |
| 9 | MP69RYAk | IND | 2.98/2.25/2.79/1.64 | .6699 | .6585 | IND/INSTITUTIONS 1→2 未亮 → 边际 0 | self .6585 贴线 |

### C 档：prod/self 贴线或撞墙，不占配额

| id | region | S/F | prod | self | 排除原因 |
|---|---|---|---|---|---|
| **blaoQ6Kq** | GBR | 1.65/1.15 | **.9405** | .1548 | **prod 撞墙 ≥0.7**（0.9405，单点）；CW 已修复但 prod 硬闸否决，判死 |
| **gJaR8e0J** | GBR | 1.63/1.13 | pending | .1548 | 同族备选，prod inflight>7min 未完成，挂起；若 ≥0.7 则 snl27 族判死 |
| 58J72oQN | USA | 2.20/1.28 | .6897 | .2966 | prod 余量 .0103；USA/OTHER 已亮至 4，塔边际 0 |
| 3qj1eYdz | IND | 2.76/1.97 | .6962 | .6976 | prod+self 双贴线 |
| RREPm361 | DEU | 2.02/1.25 | .6881 | .3275 | prod 贴线；DEU/ANALYST 已亮 |
| 1YNMAA8M | DEU | 1.58/1.36 | .6951 | .6946 | prod+self 双贴线 |

### D 档：结构性判死（op-min 实证，不可交）

| id | 判定 | 原因 |
|---|---|---|
| blaoMOAq | REJECT_STRUCTURAL_CW | CONCENTRATED_WEIGHT 与骨架同源（原件）；修复件 blaoQ6Kq 又撞 prod |
| e7adKz7g / VkN22b9G 等 | SUPERSEDED | wponnkmd 已提交，同骨架 self≥0.99 |
| MP65Lx5k / O0W5x9mR / KPgwvOdp 等 | DEAD_TWIN | Jj85OR7e 已提交，同骨架互相关 .696~.998 |
| 2rAQ6mQN | DEAD_TWIN | 与 88N6OOP7 互相关 .9969 |
| kqNb1g5d | 三重高危 | prod .6972(余 .0028)+self .6835+investability −0.5 |
| 1YWLbqMQ | REJECT_STRUCTURAL | 门控与换手/sub 硬耦合，10→9 ops 仍 >8 |

## 2b ★ 补充：截图 11 颗（KOR 内部人×价量同族，19:2x 新增评估）

用户截图 11 个 id 并入评估，详见 `output_report/eval_screenshot_11_kor_20261116.md`。
**全族 = KOR「价量/概率腿 − insd5 内部人腿」双腿差分矩阵，全 Ra=0、全 UNSUBMITTED、prod 全有当天权威缓存（4.9h 内），与已提交 Jj85OR7e 全部 <0.7（无封死）。族内高度抱团，最多交 3 颗互不冲突。**

| id | S/F/2Y/sub | prod(时龄) | self | 塔六元组（席位｜倍率｜当季→交后｜点亮｜边际） | ops/fields | 判定 |
|---|---|---|---|---|---|---|
| **wpoJRxW5** | 2.04/1.15/2.55/1.95 | **.504**(4.8h) | .4399 | INSIDERS 1.2+OTHER 1.6 短板1.2｜2→3 **点亮**｜+1 | 5/3(**T4+1字段**) | **族内首选**：prod 余量 .196 最大；与 A1xOPqGE ρ.993 取本件 |
| **ZYa2xVKY** | 1.71/1.13/2.77/1.51 | .5991(0.2h) | .1201 | INSIDERS 1.2+PV 1.4 短板1.2｜2→3 点亮｜+1 | 4/2 | self 最低；与 N1Pg6ERg/QP02J90p 孪生，取本件 |
| **78YaAnYZ** | 1.77/1.16/2.11/1.58 | .5797(3.3h) | .1319 | INSIDERS 1.2+PV 1.4 短板1.2｜2→3 点亮｜+1 | 4/2(**T4+1字段**) | T4 新字段；与 78YaQPnL 孪生取本件 |
| 78LpqZYQ | 2.12/**2.09**/2.59/2.30 | **.697**(4.9h) | .477 | INSIDERS 1.2+ANALYST 1.6亮 短板1.2｜2→3 点亮｜+1 | 5/2 | **F2.09 全族最强**但 prod 余量 .003 贴线；与 wpoJRxW5 同席 |
| ZYQ116ln | 1.86/1.10/1.80/1.55 | **.6981**(4.9h) | .2129 | 纯 PV 1.4（PV=2未亮）｜边际 0 | 3/1 | prod 贴线 + 塔边际 0，不占配额 |
| A1xOPqGE / N1Pg6ERg / QP02J90p / QP02jR9w / 78YaQPnL / 9qlav7E2 | — | .51~.62 | — | 同上族 | — | 与上表 ρ .80~.99 互斥，二选一后不交；78YaQPnL 另有 CLUSTER_TEST WARNING |

**并入一篮建议**：这 11 颗**同抢 KOR/INSIDERS 2→3 一席，塔只能点亮一次**——真正最优是仅交 `wpoJRxW5`（prod 余量最大、塔点亮、T4 新字段），其余降为备选。若追求极致指标可用 `78LpqZYQ`（F2.09）替换但 prod 贴线。与 §4 的 GBR/IND 一篮不冲突（不同区不同席）。

## 2c ★ 补充：截图 4 颗（19:29，17:1x 已深度评估，全部不交）

用户再截图 4 个 id（`kqNb1g5d`/`N1eLE1de`/`MP6l68aa`/`zqrgna91`，其中 MP6168aa 实为小写 l）。这 4 颗在 17:1x 的 7 颗评估中已实测 prod/self/塔/互相关，结论全部不交，详见 `output_report/eval_seven_candidates_20261116.md`。19:29 复核状态无漂移，正式并入。

| id | S/F/2Y/sub | prod(权威缓存) | self | 塔六元组（席位｜倍率｜当季→交后｜点亮｜边际） | inv | 判定 |
|---|---|---|---|---|---|---|
| kqNb1g5d | 3.32/3.29/3.65/1.76 | **.6972**(19:21) | .6835 | INSIDERS 0 + OTHER 已亮 → 边际 0 | **−0.5** | **三重高危**：prod 余量 .0028、self 贴线、investability 负 ⇒ 死 |
| MP6l68aa | 2.20/1.28/3.17/1.22 | .6897(11-15 08:21，35h) | .2966 | USA/OTHER 已亮 4 → 边际 0 | 0.99 | prod 余量 .0103 + 塔边际 0 ⇒ 不占配额 |
| zqrgna91 | 2.67/1.66/1.68/1.47 | .6877(11-14 23:22，≈44h) | .3541 | USA/MODEL 已亮 4 → 边际 0 | 2.7 | prod 贴线 + 2Y 1.68 贴线 + 塔边际 0 ⇒ 次选不交 |
| N1eLE1de | 2.63/1.54/2.07/1.66 | .6916(11-14 23:22，≈44h) | .2804 | USA/MODEL 已亮 4 → 边际 0 | 2.5 | prod 余量 .0084 + 塔边际 0 ⇒ 次选不交 |

- **解耦确认**：4 颗与今日全部 ACTIVE（wponnkmd/bla2k0Jq/88N6OOP7/Jj85OR7e）互相关全 <0.11；zqrgna91↔N1eLE1de 0.4289（不互斥）——排除原因是 **prod 贴线 + 塔边际 0**，非相关性。
- 六维：4 颗 T4 均 +2 新字段（硬收益），但不足以抵消 prod 贴线与塔边际 0。
- 若坚持从这 4 颗选：`MP6l68aa` 相对最优（2Y 3.17 最强、prod 缓存最新、self 安全、六维正），但须当刻 refresh prod 确认未漂过 0.7。

## 3 S2 待补测档（数据不足，非否决）

约 25 颗 S2 缺 self 或完整指标（如 ZYQmolVx prod .5276、rKRPAWv9 prod .3998 都很低），
但 self/方案 D 未测 ⇒ 不进 A/B 档。需补 `check_self_correlation` + `performance_comparison` 后重排。

## 4 一篮最优提交建议（互不冲突）

ET 剩 2 席，塔点亮优先：
1. `omEdka3v` → 点亮 GBR/OTHER（2→3），本轮唯一塔边际正件。
2. `rK7Qm6ld` → IND/SENTIMENT（1→2，未点亮但 prod 余量最大、2Y 3.45 最强，作为机动第二席）。

⚠ 前两条提交必做：① 当刻 `check_correlation(refresh=True)` 复核 prod（GBR 槽昨夜熔断，实测前需冷却）② 稳健审计（多数无记录）③ 方案 D ④ 同席互相关（omEdka3v vs pwdLp9z6 二选一）⑤ ET 配额复核。

## 5 全量附录

202 颗完整分档见 `results/candidate_inventory_20261115.json`（机读，含逐颗 blockers/todos/塔/缓存龄）；
本清单叠加的 23 颗已提交 + 今日 op-min/repair 新发现已在 §1~§2 列明。逐颗塔六元组与六维口径见 §0。

## 2d ★ 补充：截图 4 颗（DEU，22:2x 评估）

用户再截图 4 id（`XgaGb3J1`/`d5aE63Ew`/`gJaR5gov`/`LLKnekRL`，均 DEU/TOP500）。

| id | S/F/2Y/sub | prod | self | 塔六元组 | 判定 |
|---|---|---|---|---|---|
| **XgaGb3J1** | 2.36/2.02/2.71/1.51 | **.6784**(17:18，余.0216贴线) | **.6784**(贴线，当日ACTIVE复核.06) | DEU/INSIDERS×1.6 + MODEL×1.8 双亮(MODEL=3亮/INSIDERS=1)→边际0 | **可交但双贴线**；ops 12/fields 9，**T3 better + T4+4 新字段**（significant_value_1~4）六维硬收益大 |
| d5aE63Ew | 0.89/0.63/0.92/0.26 | — | — | — | Ra=4 FAIL，排除 |
| gJaR5gov | 0.78/0.51/1.08/0.18 | — | — | — | Ra=5 FAIL，排除 |
| LLKnekRL | 0.89/0.67/0.86/−0.11 | — | — | — | Ra=4 FAIL + sub 负，排除 |

- `XgaGb3J1`：指标全过、**六维是本批最强**（T3 新算子 + T4 新增 4 字段 significant_value_1~4），但 prod/self 双贴线（各余 .02）+ 塔边际 0（DEU/INSIDERS 当季 1→2 不点亮、MODEL 3 已亮）。交前须当刻 refresh prod/self 双复核；若任一漂过 0.7 即死。
- 塔口径核对：DEU/D1/INSIDERS 当季=1、MODEL=3（已亮），混塔短板 1.6，提交后 INSIDERS 1→2 不点亮 ⇒ 塔边际 0。
