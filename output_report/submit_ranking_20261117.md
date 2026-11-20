# 近十日 alpha 全量值得提交排序清单（2026-11-17 16:3x 版）

> 窗口 2026-11-08 ~ 11-17 GMT+8。基线 = `candidate_inventory_20261115.json`（202 颗）+ 11-16/11-17 op-min/评估增量，
> OS 列表与塔计数均为今日 MCP 实读。**只挖不提交——提交权归用户。**
> **配额：ET 11-17 全新——REGULAR 0/4、SUPER 0/1**（`pwa8mYvV` SUPER 于 ET 11-16 19:10 提交，已用昨日 SUPER 档）。

## 0 相对 11-16 19:18 版的三处重大变化

1. **`j2a9moM5` 已提交 ACTIVE**（ET 11-16 06:59，KOR 概率腿−insd5 腿）→ ① KOR 概率腿族全部封死（`wpoJRxW5`↔j2a9moM5 **ρ.9942** ⇒ 死）；② **KOR/INSIDERS 塔 2→3 点亮兑现**（今晨塔计数实读）。
2. **昨日新增全闸件**：`VkNOJYnM`（DEU op-min 40→17 ops，S2.03/F1.73/2Y2.25，**prod .4489 全场最大余量**）。
3. **昨日判死**：`RReNkLv0`（16 条实测 S/F↔2Y 反向权衡到顶）；`blaoQ6Kq`（prod .9405 撞墙）；`blaoMOAq`（CW 结构性）。

## 1 判据与塔计数（今日 `get_pyramid_alphas` 显式季度日期，逐 region 块对齐）

**判序**：台账 REJECT → 硬闸（prod≥0.7 / self≥0.7 / RA 全闸 / 缓存>48h）→ 塔边际 → 六维 → 指标。
prod/self 读数为 11-16~17 权威缓存（24~48h 内），**提交前贴线件必须当刻 refresh**。

**塔当季计数**：
USA：EARNINGS **3(亮)** / OTHER **4(亮)** / MODEL 4 / ANALYST 6(亮) / RISK **3(亮)** / INSTITUTIONS 1 ｜
GBR：**OTHER 2**（唯一可点亮 2→3）/ MODEL 6(亮) / SHORTINTEREST 4(亮) / ANALYST 3 / NEWS 3 / PV 4 / SENTIMENT 0 ｜
IND：EARNINGS **3(亮)** / PV **12(亮)** / NEWS 4 / OTHER 4 / ANALYST 3 / SENTIMENT 1 / INSTITUTIONS 1 ｜
KOR：INSIDERS **3(亮 ← j2a9moM5)** / ANALYST 4(亮) / SHORTINTEREST 4(亮) / OTHER 2 / PV 2 / MODEL 3 ｜
EUR：OTHER 3(亮) / SENTIMENT 3(亮) / ANALYST 10(亮) ｜
DEU：ANALYST 6(亮) / SHORTINTEREST 5(亮) / MODEL 3(亮) / FUNDAMENTAL 3(亮) / OTHER 3 / INSIDERS 1 / SENTIMENT 1。

⇒ **全账号仅剩一个可点亮席位：GBR/D1/OTHER（2→3）**。

## 2 已提交（S0，排除）——近十日 ACTIVE（OS 实读 12 颗）

| id | ET 提交 | 类型 | 塔 |
|---|---|---|---|
| pwa8mYvV | 11-16 19:10 | **SUPER** | GBR（S5.05/F5.18） |
| j2a9moM5 | 11-16 06:59 | REGULAR | KOR/INSIDERS **点亮** + OTHER |
| wponnkmd | 11-16 04:06 | REGULAR | USA/EARNINGS **点亮** |
| Jj85OR7e | 11-16 00:00 | REGULAR | KOR/INSIDERS |
| 88N6OOP7 | 11-15 21:39 | REGULAR | USA/RISK+OTHER |
| akaWd90w | 11-15 21:35 | REGULAR | DEU/FUNDAMENTAL |
| O0Wkvqgd | 11-15 02:14 | REGULAR | IND/PV+EARNINGS **点亮** |
| KPg60XNp | 11-15 01:25 | SUPER | KOR |
| bla2k0Jq | 11-15 00:53 | REGULAR | USA/OTHER **点亮** |
| A1xJdOmg / pwaQ0bx3 / wpo8olA6 | 11-13~14 | REGULAR | 多区 |

## 3 ★ 值得提交排序

### A 档：塔边际正（唯一可点亮席）

| # | id | region | S/F/2Y/sub | prod | self | 塔六元组（席位｜倍率｜当季→交后｜点亮｜边际） | ops/fields | 判据 |
|---:|---|---|---|---|---|---|---|---|
| 1 | **omEdka3v** | GBR | 2.51/1.40/2.37/2.46 | .6026 | .4164 | GBR/OTHER｜1.6(短板1.2)｜2→3｜**点亮**｜**+1** | 8/2 | **全场唯一塔边际正件**；指标强、prod 余量 .097；混塔短板 1.2；ops 8 软线。**今日首推** |
| 2 | pwdLp9z6 | GBR | 2.26/1.19/2.09/2.19 | .6483 | .4754 | 同 GBR/OTHER 席｜2→3｜点亮｜+1 | 8/? | 与 #1 同席互斥二选一；F 余量薄，取 #1 |

### B 档：全闸通过、塔边际 0（按指标+prod 余量排序）

| # | id | region | S/F/2Y/sub | prod | self | 塔六元组（边际全 0） | 判据 |
|---:|---|---|---|---|---|---|---|
| 3 | **VkNOJYnM** | DEU | 2.03/1.73/2.25/1.34 | **.4489** | ≤.0865 | DEU/INSIDERS 1.6+ANALYST 1.8(亮)｜1→2 不点亮 | **prod 余量全场最大(.251)**；ops 17（已压缩 40→17）；TO 12.26%/DD 5.03%；备选 `1YWJEzZX`(decay4, margin+38%) |
| 4 | 6XdkW08J | GBR | 2.60/1.95/2.55/2.12 | .6267 | .3393 | SHORTINTEREST+MODEL 均亮 | 指标最强档；ops 8 软线 |
| 5 | rK7Qm6ld | IND | 2.15/1.20/**3.45**/1.19 | **.5634** | .2514 | SENTIMENT 1→2 不亮(×1.2)+PV 12 亮 | prod 余量 .137；2Y 全场最强 |
| 6 | MP69RYAk | IND | 2.98/2.25/2.79/1.64 | .6699 | .6585 | INSTITUTIONS 1→2 不亮 | self 贴线 |
| 7 | LL5Edbee | IND | 2.53/1.78/2.79/1.42 | .6327 | .6338 | INSTITUTIONS 1→2 不亮 | self 贴线 |
| 8 | mLaLllmK | EUR | **3.98**/2.21/1.93/2.22 | .6579 | .3014 | EUR/OTHER 亮 | S 最高；prod 贴线 |
| 9 | omExeqLb | GBR | 2.43/1.78/2.12/2.14 | .6143 | .4195 | MODEL 亮 | 稳 |
| 10 | rKRx7v6m | EUR | 3.22/2.14/2.07/1.84 | .6756 | .4279 | EUR 双亮 | prod 贴线 |
| 11 | 78LpqZYQ | KOR | 2.12/**2.09**/2.59/2.30 | **.697** | .477 | INSIDERS **3 已亮**→边际 0 | F2.09 全族最强；**prod 余量仅 .003**；昨日幸存但塔已点亮 |
| 12 | ZYa2xVKY | KOR | 1.71/1.13/2.77/1.51 | .5991 | .1201 | INSIDERS 已亮→0 | prod .20 余量；塔已亮 |
| 13 | 78YaAnYZ | KOR | 1.77/1.16/2.11/1.58 | .5797 | .1319 | INSIDERS 已亮→0 | T4+1 字段 |
| 14 | ZYQ116ln | KOR | 1.86/1.10/1.80/1.55 | .6981 | .2129 | 纯 PV 2 未亮→0 | prod 余量 .0019 极薄 |

### C 档：贴线/双贴线，不占配额

| id | prod | self | 排除原因 |
|---|---|---|---|
| **XgaGb3J1** | .6784 | .6784 | **双贴线**（各余 .0216）；T4+4 新字段六维强，但塔 DEU/INSIDERS 1→2 不亮 |
| 58J72oQN / MP6l68aa | .6897 | .2966 | prod 余量 .0103 + USA/OTHER 已亮 4 |
| zqrgna91 | .6877 | .3541 | prod + 2Y 1.68 双贴线 + MODEL 亮 |
| N1eLE1de | .6916 | .2804 | prod 余量 .0084 + MODEL 亮 |

### D 档：判死（本轮及昨日实测）

| id | 判定 | 原因 |
|---|---|---|
| **wpoJRxW5** | DEAD_TWIN（新增） | 与 11-16 已提交 `j2a9moM5` ρ**.9942**（KOR 概率腿族封死） |
| blaoQ6Kq | REJECT_PROD | prod **.9405** 撞墙（单点）；CW 已修但 prod 硬闸 |
| gJaR8e0J | PROD_PENDING | 平台槽挂起未决 |
| blaoMOAq | REJECT_STRUCTURAL_CW | 原件 CW 结构性；修复件即 blaoQ6Kq 又撞 prod |
| RReNkLv0 | REJECT_STRUCTURAL | 16 条实测 S/F↔2Y 反向权衡到顶（最优 qM7govkP 仍 S1.42/F0.86 FAIL） |
| e7adKz7g / VkN22b9G 族 | SUPERSEDED | wponnkmd 已交，同骨架 >0.99 |
| MP65Lx5k / O0W5x9mR 族 | DEAD_TWIN | Jj85OR7e 已交 ρ .696~.998 |
| 2rAQ6mQN | DEAD_TWIN | 与 88N6OOP7 ρ .9969 |
| kqNb1g5d | 三重高危 | prod .6972+self .6835+investability −0.5 |
| 1YWLbqMQ | REJECT_STRUCTURAL | 门控与 TO/sub 硬耦合，9 ops 仍超偏好 |
| kqNRX1ZP | DEAD_TWIN | 与 11-04 ACTIVE `bl6OWZ2M` self .7936 |

## 4 一篮最优提交建议（ET 11-17 全新配额：REGULAR 0/4、SUPER 0/1）

1. **`omEdka3v`** → 点亮 GBR/OTHER（2→3，全场唯一塔边际正）——**今日首推**。
2. **`VkNOJYnM`** → DEU（塔边际 0 但 prod .4489 余量 .25 全场最大、ops 17、六维 T1 +0.0143 软成本可控）——第二席机动。
3. SUPER 档：昨日 SA 扫描 GBR 最优停 2/3（缺口 .0048 账户级最小），**本轮无 SUPER 建议**。

⚠ 提交前必做：① `omEdka3v`/`VkNOJYnM` prod 当刻 refresh（两者缓存 24~48h）；② 稳健审计（VkNOJYnM 无台账、omEdka3v 无台账）；③ 方案 D；④ 同席互相关（omEdka3v vs pwdLp9z6 已二选一）；⑤ ET 配额复核。

## 5 全量附录

202 颗完整分档见 `results/candidate_inventory_20261115.json`；11-16~17 增量评估见
`eval_screenshot_11_kor_20261116.md`（KOR 族）、`eval_seven_candidates_20261116.md`（7 颗）、
`opmin_blaoMOAq_20261116.md`（CW 修复+prod 撞墙）、`opmin_RReNkLv0_20261117.md`（判死）、
`output_report/opmin_3q0wVPgz_20261117.md`（VkNOJYnM 40→17 ops）、`submit_ranking_20261116.md`（前版）。
逐颗塔六元组+六维口径见 §1/§3；全部排除项已列 §3C/D。

## 6 ★ VkNOJYnM 六维核实（2026-11-17 16:3x，用户质询）

**两级口径必须分开（用户质询的正是这个混淆点）**：

| 口径 | 数值 | 来源 | 进六维吗 |
|---|---|---|---|
| **平台 `regular.operatorCount`** | **17**（算子**调用次数**，含重复、变量赋值不计） | 平台 API 权威值 | **否**——这是 PPA 通道上限口径（≤8），REGULAR 不看 |
| **六维 T1「Avg distinct Operators/Alpha」** | distinct **10** 个（add/days_from_last_change/divide/group_rank/group_zscore/multiply/subtract/ts_ir/ts_mean/vec_avg） | 本地 genius_tiebreak 解析 | **是** |
| 六维 T2「Avg distinct Fields/Alpha」 | distinct **7** 个字段 | 同上 | **是** |

**对六维绩效的实际影响**（基线 N=377 · T1=4.6074 · T2=1.8488 · T3=57 · T4=481）：

| 维 | 基线 | 交后 | Δ | 方向 | 定性 |
|---|---:|---:|---:|---|---|
| T1 平均 distinct ops | 4.6074 | 4.6217 | **+0.0143** | 越低越好 ⇒ **变差** | 软成本（单颗权重 1/(N+1)=1/378） |
| T2 平均 distinct fields | 1.8488 | 1.8624 | **+0.0136** | 越低越好 ⇒ **变差** | 软成本 |
| T3 总 distinct 算子 | 57 | 58 | **+1**（`days_from_last_change` 账户新算子） | 越高越好 ⇒ **改善** | 硬收益（57→58 ≈ +1.75%） |
| T4 总 distinct 字段 | 481 | 487 | **+6**（est_12m_ebi_lowerednum/raisednum_4wks + significant_value_1~4 全新） | 越高越好 ⇒ **改善** | **硬收益（+6 ≈ +10.5%）** |

**官方口径（Brain Genius 文档原文，MCP get_documentation_page 实读）**：
1. Tie-breaker 第 1 项 "Avg distinct **Operators**/Alpha (Lower is better)"、第 3 项 "Total distinct Operators* (Higher is better)"，**脚注 `* ts_backfill and group_backfill are not counted`**——本件无 backfill 算子，不受影响。
2. 官方只说 **distinct**（去重），从未定义「算子调用次数」进六维——17 次调用 vs 10 distinct 的差异是平台通道口径（PPA ≤8）与六维口径的分离，**官方文档无任何「提交高调用数 alpha 会惩罚六维」的说法**。
3. Tie-breaker 仅在「超过档位名额时」排序用（"If more consultants meet the base criteria... a tiebreaker criterion is used"），Eligibility 本身不看它。

**论坛检索**：forum search 两次关键词零命中（无相关讨论帖）；第三方中文资料（ima 知识库）确认六维方向「单个 alpha 用到的 fields/operator 越少越好，总 distinct 越多越好」，与官方文档一致。

**结论**：提交 `VkNOJYnM` 对六维是**净正**——T1/T2 各付出 +0.0143/+0.0136 的软成本（单颗摊薄后对季末排名影响 ≈ 忽略），换来 T3 +1 新算子、**T4 +6 新字段的确定性硬收益**。17 次调用本身**不进任何官方指标**，唯一的口径限制是 PPA 通道（本件走 REGULAR，不受 ≤8 约束）。若要进一步压 T1/T2，唯一通道是把 10 个 distinct 压到 ≤8（如去 `group_zscore`/`ts_ir` 之一），但昨日 op-min 已实测删任一会掉闸——17/10 就是该骨架的帕累托前沿。
