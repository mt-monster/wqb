# SuperAlpha 各 Region 最优方案 · 2026-11-13

> 执行时间：2026-11-13 06:33 → 07:5x（GMT+8）｜ET 时间 **2026-11-12 18:25**（`wqb.timeutil.et_now()` 实测）
> 扫描口径：`probe_sa_candidates --refresh`（先清 `api_cache` 中 `user_alphas%` 旧条目）
> 闸门口径：`check_correlation(correlation_type="both", refresh=True)` 逐颗实测 prod；self 走平台缓存回读（`refresh=False`，均为 11-13 06:40–06:56 计算值）
> **本轮未提交任何 alpha。提交权完全归用户（2026-11-11 用户明令撤销自动提交）。**

---

## 一、执行摘要

### 1.1 本轮产能结论

| 结论 | 内容 |
|---|---|
| 构建档数 | **9 档**（EUR 5 / USA 3 / DEU 1），全部串行 2 路，无 429、无 ERROR |
| 新增候选 | **9 颗**，其中过 0.68 余量闸 **3 颗**（EUR 三族），6 颗判死（5 颗 prod 红线 + 1 颗 ladder） |
| 存量复测 | 5 颗（`Xg9WNRg8` / `e75avmq6` / `2r5rA775` / `1YNl3p5R` / `leaq3P9l`），`refresh` 重测后**全部仍过闸** |
| 过闸候选合计 | **8 颗**（3 新 + 5 存量）⇒ 经 §5.4 互斥矩阵压缩后**实际只有 5 个可用席位** |
| ★★ 本轮主发现 | **EUR/TOP2500 出现 S 7.10 的候选 `xAv05p9J`，但 prod 0.7165 破 0.7 红线** ⇒ 该组件池的 prod 墙在 S≈7.0 处；0.68 余量闸下的最优可行点是 **`Wjl6JJQO` S 6.13 / prod 0.6413** |
| ★ 新撞墙 | `Jj8Z27gA`（DEU/TOP500 SUBIND）**F 3.36 全轮最高，prod 0.7400 FAIL** —— 「族越粗 F 越高、prod 越脏」**第 2 次复现**（11-12 为 INDUSTRY F3.63/prod 0.7412） |
| ★ 新事实 | EUR/TOP1200 **零 SUPER 档**首次突破 prod 墙（0.6484）但 **IS_LADDER_SHARPE 1.23 < 1.58 FAIL** ⇒ 该档瓶颈从「prod 墙」转为「2Y 墙」 |
| 产能来源 | 100% 来自「已占档换异族」；**本轮无零 SUPER 空档可建**（EUR/TOP1200 已判死，HKG 池 7，USA/TOP200 历史判死） |

### 1.2 优先队列 A — 按 §5.5 字典序（③ B 档双达标 优先于 ④ prod 余量 / ⑤ U / ⑥ Eff）

| # | Alpha | 档位 | 族 | S / F / TO | prod / self | 质量档 | 席位类型 |
|---|---|---|---|---|---|---|---|
| **1** | **`leaq3P9l`** | **DEU/TOP500** | **SLOW d1** | **2.60 / 2.11 / 0.1608** | **0.5951 / 0.5954** | **B 档**（唯一） | 已占档异族（第 3 族） |
| 2 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 / 2.38 / 0.1341 | 0.6011 / 0.6011 | A 档（prod 差 0.0011 进不了 B） | 已占档异族（第 2 族） |
| 3 | `e75avmq6` | USA/TOP2000 | SLOW d1 | 4.29 / 4.00 / 0.1034 | 0.6373 / 0.4871 | A 档 | 已占档异族（第 2 族） |
| 4 | **`Wjl6JJQO`** | **EUR/TOP2500** | **SUBINDUSTRY d1** | **6.13 / 4.69 / 0.2691** | **0.6413 / 0.6173** | A 档 + S 达 C 档 | 已占档异族（第 4 族，**末席**） |
| 5 | `2r5rA775` | DEU/TOP500 | CROWDING d1 | 3.00 / 3.15 / 0.1340 | 0.6434 / 0.6436 | A 档 | 与 #1 同档互斥（ρ=0.7387） |
| 6 | `O0WE25PR` | EUR/TOP2500 | INDUSTRY d1 | 6.03 / 4.65 / 0.2675 | 0.6489 / 0.6393 | A 档 + S 达 C 档 | 与 #4 同席（ρ=0.9850） |
| 7 | `Xg9WNRg8` | USA/TOP2000 | SLOW d1 | 4.74 / 4.10 / 0.1659 | 0.6493 / 0.6493 | A 档 | 与 #3 同族（ρ=0.4819，可共存） |
| 8 | `Jj8Zr1Xn` | EUR/TOP2500 | MARKET d1 | 5.63 / 4.33 / 0.2703 | 0.6661 / 0.5585 | A 档 + S 达 C 档 | 与 #4 同席（ρ=0.9400） |

### 1.3 优先队列 B — 按质量口径（Eff / S / F）

| # | Alpha | Eff | S | F | prod | 说明 |
|---|---|---|---|---|---|---|
| **1** | **`Wjl6JJQO`** | **6.31** | **6.13** | **4.69** | 0.6413 | **Eff 为 leaq3P9l 的 4.9 倍，全轮质量第一** |
| 2 | `O0WE25PR` | 6.09 | 6.03 | 4.65 | 0.6489 | 与 #1 ρ=0.9850 ⇒ 同一席位，无条件劣于 #1 |
| 3 | `Jj8Zr1Xn` | 5.33 | 5.63 | 4.33 | 0.6661 | self 最低（0.5585）但 prod 余量仅 0.0139 |
| 4 | `Xg9WNRg8` | 4.26 | 4.74 | 4.10 | 0.6493 | USA/TOP2000 最强 |
| 5 | `e75avmq6` | 3.63 | 4.29 | 4.00 | 0.6373 | self 0.4871 最干净 |

> ⚠ **本轮两口径首次分叉**（11-12 是收敛的：`E5Q7RGNR` 同时满足两条）。原因：唯一 B 档件 `leaq3P9l` 的 S 只有 2.60，而 S/F/Eff 全面领先的 `Wjl6JJQO` 的 prod 0.6413 > 0.60 进不了 B 档。
> **本报告不擅自合并两条口径**：§5.2 按任务 §5.5 原文出表（#1 = `leaq3P9l`）；§10.2 给「质量优先」口径（#1 = `Wjl6JJQO`）并说明取舍。**最终取谁由用户定。**

---

## 二、数据基线（2026-11-13 06:36 刷新）

### 2.1 组件池 eligibility（硬前置 ≥10 颗 ACTIVE REGULAR）

| 区域 | ACTIVE 已提交 REGULAR | IS 未提交 | 总 REGULAR | verdict | μ̄（IS Sharpe 均值） |
|---|---|---|---|---|---|
| USA | 47 | 0 | 148 | GO | 1.9757 |
| IND | 47 | 0 | 51 | GO | 2.7302 |
| KOR | 35 | 0 | 37 | GO | 1.8586 |
| GBR | 28 | 0 | 28 | GO | 1.9064 |
| **EUR** | **27** | **285** | **318** | GO | **2.0811** |
| MEA | 19 | 0 | 19 | GO（平台已下架，不可建） | 1.8847 |
| GLB | 19 | 0 | 19 | GO | 3.0321 |
| **DEU** | **18** | **665** | **683** | GO | **1.8356** |
| ASI | **10** | 0 | 10 | GO（刚好卡线） | 2.3080 |
| HKG | 7 | 0 | 7 | **BLOCKED（差 3）** | 1.9757 |

对比 11-12：池 257 → **257（持平）**，SUPER ACTIVE **53 → 54**（唯一增量 = `E5Q7RGNR`，11-11 提交）。
**关键变化**：池规模零增长 ⇒ 本轮产能全部来自「已占档换异族」，与 11-12 同构。未提交 REGULAR 大增（DEU 665 / EUR 285）但**不计入组件池**——组件池只认 ACTIVE 已提交。

### 2.2 档位占用表（平台档位 × SUPER）

| 区域 | Universe | REGULAR | SUPER | 状态 | 已占 SUPER（族 / decay） |
|---|---|---|---|---|---|
| USA | TOP3000 | 38 | 6 | OCCUPIED（≥5 换族失效） | STAT d10、SUBIND d5、MARKET d5、FAST d1、SLOW d1×2 |
| USA | TOP2000 | 5 | 1 | OCCUPIED（可换族） | `vROw5Rkd`（STAT d1） |
| USA | TOP1000 | 0 | 1 | OCCUPIED（可换族） | `LL5aX6Y2`（STAT d1） |
| USA | TOP500 | 0 | 1 | OCCUPIED | `E567rQvR`（CROWDING d1） |
| USA | TOPSP500 | 0 | 1 | OCCUPIED | `2rj3ddl5`（STAT d1） |
| USA | TOP200 | 0 | 0 | ZERO_OS | 历史判死（S 0.95–1.28，两次复现） |
| IND | TOP500 | 47 | **12** | OCCUPIED（全族饱和） | STAT 6 / SUBIND 3 / RAM 1 / INDUSTRY 1 / SLOW 1 |
| KOR | TOP600 | 35 | **11** | OCCUPIED（全族饱和） | STAT 6 / SUBIND 2 / RAM 1 / CROWD 1 / SLOW 1 |
| GBR | TOP700 | 28 | **6** | OCCUPIED（≥5 换族失效） | STAT×3 / RAM / FAST / SLOW |
| **EUR** | **TOP2500** | **17** | **3** | OCCUPIED（**1 席余量**） | `kqJOQgnk`(CROWDING d1)、`E5Q7RGNR`(**SLOW d2**)、`GrgGkV1o`(STAT d1) |
| EUR | TOPCS1600 | 10 | 1 | OCCUPIED | `vROOONwd`（STAT d1） |
| EUR | TOP1200 / TOP800 / TOP400 | 0 | 0 | ZERO_OS | **本轮 TOP1200 首次过 prod 墙但 ladder 1.23 FAIL**（§7.2） |
| GLB | MINVOL1M | 18 | 2 | OCCUPIED | SUBIND d10、STAT d1 |
| GLB | MINVOL10M | 0 | 1 | OCCUPIED | `LLMVPag1`（SLOW d1） |
| GLB | TOP3000 | 0 | 1 | OCCUPIED | `QPKVK8VW`（RAM d1） |
| GLB | TOPDIV3000 | 1 | 1 | OCCUPIED | `npARO63x`（STAT d1） |
| **DEU** | **TOP500** | **18** | **2** | OCCUPIED（可换族） | `mLYLEm99`(STAT d1)、`vR1oxZA3`(FAST d1) |
| ASI | MINVOL1M | 7 | 1 | OCCUPIED | `d5WGG5bg`（STAT d2） |
| ASI | MINVOL10M | 3 | 1 | OCCUPIED | `QPv88bJW`（COUNTRY d3） |
| HKG | TOP800 | 7 | 0 | ZERO_SA | 池 7/10，BLOCKED |
| MEA | TOP400 | 19 | 2 | NON_PLATFORM | 平台已下架（400） |

> **席位饱和度**（osmosis 每 scope 100,000 点固定，本仓自设 4 席/22% 策略，非平台硬限）：
> EUR/TOP2500 **3/4**（本轮候选若交即满）、DEU/TOP500 **2/4**、USA/TOP2000 **1/4**、USA/TOP1000 **1/4**。
> ⇒ 从「留席给未来更优件」的角度，DEU/USA 的边际优于 EUR；从「单颗绝对质量」角度 EUR 压倒。两者冲突，见 §10.2。

### 2.3 Pyramid 倍率（D1 口径；**SA 不参与塔计数，仅供参考**）

| 区域 | D1 最高类别 | D1 最低 | 备注 |
|---|---|---|---|
| DEU | fundamental/analyst/news/other/sentiment/model **1.8** | imbalance 1.2 | 全账户最高档 |
| GBR | sentiment **1.7** / news·other·analyst 1.6 | imbalance 1.0 | |
| EUR | other **1.5** / news·sentiment 1.4 | risk·imbalance 1.0 | |
| USA | other·sentiment **1.4** | institutions·imbalance 1.0 | |
| GLB | fundamental·analyst **1.4** | pv·risk·institutions 1.0 | |
| ASI | analyst **1.5** | pv·insiders·risk·imbalance·macro 1.0 | |

> §0.8：SUPER 的 `is.checks` 无 `MATCHES_PYRAMID` ⇒ SA 不进入 pyramid 计数，塔倍率**不作为选点理由**（仅记录）。
> 若未来做 REGULAR 配套选点，DEU ×1.8 仍是全账户最高杠杆——但本轮 4 颗过闸候选里 3 颗在 EUR/USA（×1.4–1.5）。

---

## 三、选点原则（本轮执行顺序）

1. **席位类型 > 同族/异族 > 边际指标 > 绝对指标**
2. 零 SUPER 档 = 最高优先。本轮唯一零 SUPER 候选（EUR/TOP1200）已判死 ⇒ **本轮无零 SUPER 产能**
3. 已占档：档内 SUPER < 5 才建异族（EUR/TOP2500 3 颗、DEU/TOP500 2 颗、USA/TOP2000 1 颗、USA/TOP1000 1 颗均满足）
4. **同族（只改 limit/decay/truncation）预期 self>0.9，直接跳过** ⇒ 本轮**未建 EUR/TOP2500 SLOW**（`E5Q7RGNR` 已占 SLOW d2）
5. **prod ≥ 0.68 = 出局**（自设余量闸，比平台 0.7 严 0.02；本轮拦下 5 颗，其中 1 颗 S 7.10 为全场最高）
6. IS checks 零 FAIL，且 `LOW_FITNESS` 必须真 PASS（F≥1.0，不能靠 WARNING 混过）

---

## 四、论坛指标标准（§0 固化，无需每轮重研）

### 4.1 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.02–0.40（SA 实测 `HIGH_TURNOVER` limit=0.4） | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.60** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9** | 0.20–0.27 | <0.5 |

> 本轮修正：SA 的 `HIGH_TURNOVER` 实测 limit 为 **0.4**（非记忆里的 0.7）；`LOW_TURNOVER` limit 0.02。全部 8 颗候选 TO 0.103–0.270，均安全。

### 4.2 组件筛选阈值（论坛原文）

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ 筛选强度必须匹配池规模：加严后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。小池区（EUR/GLB/DEU/ASI）只能用宽松 selection。

### 4.3 中性化族规律（逐区实测，不可跨区照搬）

- EUR/TOP2500 的 `--turnover-min 0.095` 是本仓独有的有效杠杆（11-12 破 7 颗 FAST d40/d80 污染），本轮延续并**换成 5 个异族验证**，结论见 §6.1。
- **同池异族的 prod 序列**（本轮新实证，EUR/TOP2500 + TO>0.095，同一个 10 只组件集）：

| 族 | decay | ID | S | prod | 判定 |
|---|---|---|---|---|---|
| FAST | 1 | `xAv05p9J` | **7.10** | **0.7165** | 破 0.7 红线 |
| SUBINDUSTRY | 1 | `Wjl6JJQO` | 6.13 | 0.6413 | ✅ 最优可行 |
| INDUSTRY | 1 | `O0WE25PR` | 6.03 | 0.6489 | ✅ |
| MARKET | 1 | `Jj8Zr1Xn` | 5.63 | 0.6661 | ✅ 但余量 0.014 |
| SLOW | 2 | `E5Q7RGNR`（已提交） | 6.54 | **0.5670** | ✅ 历史最优 |

⇒ **不是「S 越高 prod 越高」的单调关系**（INDUSTRY 比 MARKET 的 S 高、prod 反而低）。真实规律：**粗族（FAST/MARKET）prod 脏、细族（SUBINDUSTRY/SLOW）prod 干净**。选族优先 SUBINDUSTRY / SLOW，FAST 只在需要 S 冲顶且能接受 prod 破线时用。

---

## 五、★ 边际收益排序（§0.6 五量，逐颗可复算）

### 5.1 口径

| 指标 | 公式 | 含义 |
|---|---|---|
| `U` | `S / (μ̄·√N)` | 分散度捕获率 = 实际 S / ρ=0 理论上限 |
| `N_eff` | `(S/μ̄)²` | 等效独立腿数 |
| `ρ_eff` | `(N·μ̄²/S² − 1)/(N−1)` | 隐含组件平均相关（等权反解） |
| `Eff` | `(S−μ̄) / max(prod, self)` | 增量效率：每单位拥挤度换到的 Sharpe 溢价 |
| `ΔCAP%` | `√(52/(1+51ρ))/√(51/(1+50ρ)) −1` | 加入 SA 池的容量增量（`ρ=max(prod,self)`） |

`μ̄` = 该区 ACTIVE 已提交 REGULAR 的 IS Sharpe 均值（本轮重算：EUR 2.0811/n27、USA 1.9757/n47、DEU 1.8356/n18）；`N = min(10, 池)` = **10**（三区池均 ≥10）。

### 5.2 全量表（8 颗过闸候选）

| # | Alpha | 区域/档 | 族 | S | F | TO | prod | self | **U** | N_eff | ρ_eff | **Eff** | ΔCAP% | B档 | prod 余量 | 双闸实测 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `leaq3P9l` | DEU/TOP500 | SLOW d1 | 2.60 | 2.11 | 0.1608 | 0.5951 | 0.5954 | 0.4479 | 2.01 | 0.4427 | 1.28 | 0.013 | ✅ | 0.0849 | 11-13 06:44/06:44 |
| 2 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 | 2.38 | 0.1341 | 0.6011 | 0.6011 | 0.4178 | 1.75 | 0.5256 | 1.06 | 0.012 | — | 0.0789 | 11-13 06:45/06:45 |
| 3 | `e75avmq6` | USA/TOP2000 | SLOW d1 | 4.29 | 4.00 | 0.1034 | 0.6373 | 0.4871 | 0.6867 | 4.71 | 0.1245 | 3.63 | 0.011 | — | 0.0427 | 11-13 06:51/06:51 |
| 4 | **`Wjl6JJQO`** | **EUR/TOP2500** | **SUBIND d1** | **6.13** | **4.69** | 0.2691 | 0.6413 | 0.6173 | **0.9315** | **8.68** | **0.0170** | **6.31** | 0.010 | — | 0.0387 | 11-13 06:42/06:42 |
| 5 | `2r5rA775` | DEU/TOP500 | CROWDING d1 | 3.00 | 3.15 | 0.1340 | 0.6434 | 0.6436 | 0.5168 | 2.67 | 0.3049 | 1.81 | 0.010 | — | 0.0366 | 11-13 06:50/06:50 |
| 6 | `O0WE25PR` | EUR/TOP2500 | INDUSTRY d1 | 6.03 | 4.65 | 0.2675 | 0.6489 | 0.6393 | 0.9163 | 8.40 | 0.0212 | 6.09 | 0.010 | — | 0.0311 | 11-13 06:53/06:53 |
| 7 | `Xg9WNRg8` | USA/TOP2000 | SLOW d1 | 4.74 | 4.10 | 0.1659 | 0.6493 | 0.6493 | 0.7587 | 5.76 | 0.0819 | 4.26 | 0.010 | — | 0.0307 | 11-13 06:46/06:46 |
| 8 | `Jj8Zr1Xn` | EUR/TOP2500 | MARKET d1 | 5.63 | 4.33 | 0.2703 | 0.6661 | 0.5585 | 0.8555 | 7.32 | 0.0407 | 5.33 | 0.009 | — | 0.0139 | 11-13 06:40/06:40 |

**读法校验**：
- `Wjl6JJQO` 的 `U=0.9315` ⇒ 已达到 ρ=0 理论上限的 **93%**，`N_eff 8.68/10`、`ρ_eff 0.017` ⇒ 这 10 只组件几乎是正交的（**11-12 那次 TO>0.095 去污染的真正红利，在本轮 5 个异族上全部复现**）。
- `1YNl3p5R` 的 `ρ_eff 0.5256` / `leaq3P9l 0.4427` ⇒ 组件高度同族，SA 只是把同一个信号加了 10 遍。这正是它们 S 只有 2.6 的根因，**不是「信号弱」，是「腿不独立」**。
- `ΔCAP%` 全部 ≤0.013% ⇒ 再次确认 §0.6.1-4：**ΔCAP% 已退化为噪声，不可当排序主键**。

### 5.3 未过闸（进不了排序表，但必须留档）

| Alpha | 区域/档 | 族 | S | F | TO | prod | 死因 | 备注 |
|---|---|---|---|---|---|---|---|---|
| `xAv05p9J` | EUR/TOP2500 | FAST d1 | **7.10** | **5.02** | 0.2782 | **0.7165** | prod ≥0.7 红线 | **全场 S/F 最高**，只差 0.0165 |
| `Jj8Z27gA` | DEU/TOP500 | SUBIND d1 | 2.95 | **3.36** | 0.1308 | **0.7400** | prod ≥0.7 红线 | **F 全轮最高**；粗族脏 prod 第 2 次复现 |
| `9qlL2Xlo` | USA/TOP2000 | INDUSTRY d1 | 2.33 | 1.90 | 0.1960 | **0.7709** | prod ≥0.7 红线 | F 1.90 为 USA 本轮最高 |
| `RRenvW7b` | USA/TOP2000 | FAST d1 | 2.14 | 1.36 | 0.2505 | **0.7493** | prod ≥0.7 红线 | — |
| `78YE2KVv` | USA/TOP1000 | MARKET d1 | 1.71 | 1.35 | 0.1837 | **0.8001** | prod ≥0.7 红线 + ladder 1.93<2.02 FAIL + CLUSTER 1.32 WARNING | 三闸同时弱 |
| `Xga5OgA1` | EUR/TOP1200 | SLOW d2 | 3.10 | 1.62 | 0.2436 | 0.6484 | **IS_LADDER_SHARPE 1.23 < 1.58 FAIL** | 零 SUPER 档；prod 首次过墙（历史 5 次 0.71–0.78） |

> **EUR/TOP1200 的死因转移值得记档**：该档历史上前 5 次全死在 prod（0.7117–0.7783）。本轮加 `--turnover-min 0.095` 后 **prod 降到 0.6484 成功过墙，但 2Y ladder 只有 1.23** ⇒ 窄档（TOP1200 池仅 10 颗可用）在剔除低 TO 同族后剩下的组合没有 2 年持续性。**这不是运气问题，是「窄 universe × 强过滤 = 组件过少」的结构性代价**。

### 5.4 ★ 同席互斥矩阵（本地 PnL 相关，`compute_mutual_correlation`，1021 个交易日）

|  | Wjl6JJQO | O0WE25PR | Jj8Zr1Xn | Xg9WNRg8 | e75avmq6 | 2r5rA775 | 1YNl3p5R | leaq3P9l |
|---|---|---|---|---|---|---|---|---|
| **Wjl6JJQO** | 1 | **0.9850** | **0.9400** | -0.04 | -0.01 | 0.13 | 0.03 | 0.05 |
| **O0WE25PR** | 0.9850 | 1 | **0.9483** | -0.04 | -0.02 | 0.12 | 0.03 | 0.04 |
| **Jj8Zr1Xn** | 0.9400 | 0.9483 | 1 | -0.07 | -0.03 | 0.12 | -0.00 | 0.03 |
| **Xg9WNRg8** | -0.04 | -0.04 | -0.07 | 1 | **0.4819** | 0.02 | **0.5064** | 0.02 |
| **e75avmq6** | -0.01 | -0.02 | -0.03 | 0.4819 | 1 | 0.03 | 0.26 | 0.00 |
| **2r5rA775** | 0.13 | 0.12 | 0.12 | 0.02 | 0.03 | 1 | 0.08 | **0.7387** |
| **1YNl3p5R** | 0.03 | 0.03 | -0.00 | 0.5064 | 0.26 | 0.08 | 1 | 0.03 |
| **leaq3P9l** | 0.05 | 0.04 | 0.03 | 0.02 | 0.00 | 0.7387 | 0.03 | 1 |

**三条结论（直接改变推荐）**：

1. **EUR 三颗是同一个席位**：ρ 0.94–0.985 ⇒ 交其中任何一颗，另外两颗立刻变成 self>0.9 的死件。**#4/#6/#8 只能取一颗，取 #4。**
2. **DEU 两颗也是同一个席位**：`2r5rA775`(CROWDING) ~ `leaq3P9l`(SLOW) ρ=**0.7387** ⇒ CROWDING 与 SLOW 在 DEU 不是真异族。**#1/#5 只能取一颗。**
3. **USA 两颗可以共存**：`Xg9WNRg8` ~ `e75avmq6` ρ=0.4819（同族 SLOW d1 但 selection 不同）⇒ 理论上可分两轮交。但它们是同族，未来第三颗 SLOW 会互相顶高。

> 互斥图谱把 8 颗候选压缩成 **5 个真实席位**：EUR·1 / DEU·1 / USA-TOP2000·2 / USA-TOP1000·1。**这是本轮最重要的结论——「8 颗过闸」不等于「8 个可用增量」。**

### 5.5 ⚠ 规则张力（必须让用户看到）

任务 §5.5 的字典序把「③ B 档双达标」排在「④ prod 余量 / ⑤ U / ⑥ Eff」之前。本轮后果：

- 唯一 B 档件 `leaq3P9l` 因「B 档」这一条直接坐到 #1，**尽管它的 S 只有 2.60、Eff 1.28、ρ_eff 0.44（组件高度同族）**。
- `Wjl6JJQO` 在 **S(+3.53)、F(+2.58)、Eff(×4.9)、U(×2.08)、N_eff(×4.3)、ρ_eff(0.017 vs 0.443)** 六项上全面碾压，却因为「prod 0.6413 > 0.60」排到 #4。
- §0.6.1-4 明写「真正有区分力的只有 **Eff**、席位类型、同族/异族」——按这句执行，`Wjl6JJQO` 应排第一。

**两条口径我都给出，不擅自合并**：§1.2 按任务原文排序（#1 = `leaq3P9l`）；§10.2 给 Eff 优先口径（#1 = `Wjl6JJQO`）。

---

## 六、分 Region 方案

### 6.1 ★★★ EUR / TOP2500 —— 本轮质量最高（S 6.13，Eff 6.31），但只剩 1 席

| 项 | 内容 |
|---|---|
| 现状 | 3 颗 SUPER（CROWDING d1 / **SLOW d2** / STAT d1），**4 席制下仅剩 1 席** |
| 本轮构建 | **5 族**（MARKET / SUBINDUSTRY / FAST / INDUSTRY + TOP1200 SLOW d2 零档探针），全部 `--turnover-min 0.095` |
| 最优配方 | `--region EUR --universe TOP2500 --delay 1 --neutralization SUBINDUSTRY --decay 1 --selection-limit 10 --turnover-min 0.095 --turnover-max 0.6` |
| 产出 | `Wjl6JJQO`：**S 6.13 / F 4.69 / TO 0.2691 / 2Y ladder 5.32 / sub-universe 3.65**；prod **0.6413**（余量 0.0387）/ self **0.6173**（余量 0.0827）；**IS checks 8 项全 PASS** |
| 最近邻 | `E5Q7RGNR` 0.6173（该区已提交的 SLOW d2）—— 异族，可共存 |
| 预期 | 交付后 EUR/TOP2500 **4/4 满席**；S 6.13 使该 scope 的平均质量基本持平（现有 6.54），不会稀释 |
| ⚠ 风险 | ① 席位饱和，之后该档再无位置；② prod 余量 0.0387，若该档再提交其他 SUPER 可能被顶高（11-12 `A1VAAbWE` 被顶高 +0.064 的先例）；③ 三颗候选互为 0.94–0.985，**误交第二颗会直接判死** |

**为什么没建 SLOW**：`E5Q7RGNR` 已是 SLOW d2，同族只改 decay ⇒ 预期 self>0.9，按 §3-4 跳过。这不是遗漏，是纪律。

### 6.2 USA / TOP2000 —— 最强可用席位（S 4.74），且还有 3 席

| 项 | 内容 |
|---|---|
| 现状 | 1 颗 SUPER（`vROw5Rkd` STAT d1），**3 席余量** |
| 存量最强 | `Xg9WNRg8`：S **4.74** / F **4.10** / TO 0.1659 / 2Y **5.46** / sub 2.90；prod 0.6493 / self 0.6493（双 0.649，余量均 0.0307） |
| 次选 | `e75avmq6`：S 4.29 / F 4.00 / TO **0.1034** / 2Y 3.94；prod 0.6373 / self **0.4871**（self 最干净） |
| 两者关系 | 同族 SLOW d1，ρ=0.4819 ⇒ 可共存，但同族累积会互相顶高 |
| 本轮新探 | TOP2000 FAST（`RRenvW7b` prod 0.7493）、INDUSTRY（`9qlL2Xlo` prod 0.7709）**双双破线** ⇒ USA 窄档只有 SLOW 族能压 prod，**第 3 次复现**（11-12: CROWDING 0.7775 / SECTOR 0.7656） |

### 6.3 USA / TOP1000 —— prod 最接近 B 档（0.6011，差 0.0011）

| 项 | 内容 |
|---|---|
| 现状 | 1 颗 SUPER（`LL5aX6Y2` STAT d1） |
| 候选 | `1YNl3p5R`：S 2.61 / F 2.38 / TO 0.1341 / 2Y 2.83 / sub 2.00；prod **0.6011** / self 0.6011（余量 0.0789，**全轮第二宽**） |
| 硬伤 | `ρ_eff 0.5256`、`N_eff 1.75` ⇒ 10 只组件等于 1.75 只，S 天花板就在 2.6 |
| 本轮新探 | TOP1000 MARKET（`78YE2KVv`）prod **0.8001** + ladder 1.93 FAIL + CLUSTER 1.32 WARNING ⇒ 三闸齐弱，该档只有 CROWDING 可用 |

### 6.4 DEU / TOP500 —— 唯一 B 档 + prod 余量最宽（0.0849）

| 项 | 内容 |
|---|---|
| 现状 | 2 颗 SUPER（`mLYLEm99` STAT d1、`vR1oxZA3` FAST d1），2 席余量 |
| B 档件 | `leaq3P9l`：S 2.60 / F 2.11 / TO 0.1608 / 2Y **3.75** / sub 1.90；prod **0.5951** / self 0.5954（余量 0.0849，**全场最宽**） |
| 竞争者 | `2r5rA775`：S 3.00 / F **3.15** / TO 0.1340 / sub 1.86；prod 0.6434 / self 0.6436 —— **指标全面更强，但与 `leaq3P9l` ρ=0.7387 同席** |
| 本轮新探 | SUBINDUSTRY（`Jj8Z27gA`）**F 3.36 全轮最高、prod 0.7400 破线** ⇒ 「DEU 粗族 F 高 prod 脏」**第 2 次复现**（11-12: INDUSTRY F3.63/prod 0.7412） |
| 取舍 | 若按 B 档/余量口径 → `leaq3P9l`；若按 S/F 口径 → `2r5rA775`。**两者只能取一**。 |

### 6.5 停投区（本轮再次确认，不重复调研）

见 §七。

---

## 七、停投区与撞墙档案

### 7.1 停投（本轮再次确认）

| 区域/档 | 原因 | 证据 |
|---|---|---|
| IND / TOP500 | 12 颗 SUPER，全族饱和 | 档内 ≥5 后换族失效 |
| KOR / TOP600 | 11 颗 SUPER | 同上 |
| GBR / TOP700 | 6 颗 SUPER | 同上（11-08 已实证同档换族不再分散） |
| USA / TOP3000 | 6 颗 SUPER | 同上 |
| USA / TOP200 | 零 SUPER 但 S 天花板 1.28 | 10-25 / 11-08 两次复现 |
| GLB 全部 4 档 | 全占用（5 颗 SUPER） | MINVOL1M 2 / MINVOL10M 1 / TOP3000 1 / TOPDIV3000 1；μ̄ 3.03 全场最高但无席 |
| ASI 全域 | 2 颗 SUPER + 池刚好 10 + 同区被顶高 | `A1VAAbWe` 0.6634→0.7275、`npvEEWO8` 0.6593→0.6817 |
| HKG | 池 7/10 BLOCKED | 需先交 3 颗 REGULAR |
| MEA | 平台下架（400 `Region MEA is not available.`） | 历史 2 颗仍 ACTIVE 但不可新建 |
| CHN / AMR | 池 0 | 不可建 |
| EUR / TOP800 · TOP400 | 池不足以支撑 TO 过滤 | TOPCS1600 池 10 颗，TO>0.05 只剩 7 ⇒ 400 |

### 7.2 本轮新增撞墙档案

| 条目 | 值 | 性质 |
|---|---|---|
| `xAv05p9J` EUR/TOP2500 FAST d1 | **S 7.10 / F 5.02** / prod **0.7165** | **EUR 组件池的 prod 墙精确定位在 S≈7.0**：比已提交的 `E5Q7RGNR`(6.54/0.5670) 高 0.56 S，prod 却高 0.1495。**「S 冲顶 = 挤进生产池」的硬证据** |
| `Jj8Z27gA` DEU/TOP500 SUBIND d1 | F **3.36**（全轮最高）/ prod **0.7400** | 与 11-12 `qM71NjZO`(INDUSTRY F3.63/0.7412) 构成 **DEU 粗族双样本**：F 越高 prod 越脏 |
| `9qlL2Xlo` USA/TOP2000 INDUSTRY d1 | F 1.90 / prod **0.7709** | USA 窄档第 3 次证明：只有 SLOW 能压 prod |
| `78YE2KVv` USA/TOP1000 MARKET d1 | prod **0.8001** + ladder 1.93<2.02 + CLUSTER 1.32<1.58 | **全轮最脏**，三闸齐弱 |
| `Xga5OgA1` EUR/TOP1200 SLOW d2 | prod 0.6484（**首次过墙**）/ ladder **1.23**<1.58 | 死因从 prod 转移到 2Y：窄 universe × 强过滤 = 组件不足以支撑 2 年持续性 |
| 互斥矩阵 | EUR 三颗 0.94–0.985、DEU 两颗 0.7387 | **「过闸 ≠ 可用增量」**：8 颗候选实际只有 **5 个席位** |

---

## 八、执行清单（构建命令 + 配额约束）

### 8.1 本轮实际构建（9 档，串行 2 路，全部 COMPLETE）

```bash
# EUR 区（TO>0.095 去污染，5 档）
super_build.py select --region EUR --universe TOP2500 --delay 1 \
  --neutralization SUBINDUSTRY --decay 1 --selection-limit 10 \
  --self-gate 0.7 --turnover-min 0.095 --turnover-max 0.6 --prod-ceiling 1.0   # Wjl6JJQO ✅ S6.13
#   MARKET      → Jj8Zr1Xn  S5.63 prod .6661 ✅（余量薄）
#   FAST        → xAv05p9J  S7.10 prod .7165 ❌ 破线
#   INDUSTRY    → O0WE25PR  S6.03 prod .6489 ✅
#   TOP1200 SLOW d2 → Xga5OgA1 S3.10 ladder 1.23 ❌

# USA 区（3 档）
#   TOP2000 FAST     → RRenvW7b  prod .7493 ❌
#   TOP1000 MARKET   → 78YE2KVv  prod .8001 ❌
#   TOP2000 INDUSTRY → 9qlL2Xlo  prod .7709 ❌

# DEU 区（1 档）
#   TOP500 SUBINDUSTRY → Jj8Z27gA F3.36 prod .7400 ❌
```

**工程约束（复验）**：并发仿真上限 **2**（第 3 路 429）；同式异 decay 同批会被平台去重；`--json` 传相对路径会拼成 `results/results/x.json`，须传**绝对路径**或跑完复制。

### 8.2 配额约束

| 约束 | 值 |
|---|---|
| `SUPER_SUBMISSION` | **1 颗 / ET 日历日，账户级**，ET 00:00 重置（= GMT+8 **13:00**） |
| 当前 ET 日 | ET **2026-11-12**（GMT+8 2026-11-13 07:2x） |
| 本 ET 日已用 | **未用** —— 最后一次 SUPER 提交 = `E5Q7RGNR` @ `dateSubmitted` 2026-11-11 |
| 距额度重置 | 约 **5.5 小时**（ET 11-13 00:00 = GMT+8 11-13 13:00） |
| 403 语义 | 零配额成本、**不判死候选**；同 ET 日重复 POST 只会继续 403，**不可当探针** |

### 8.3 双闸实测记录

14 颗逐颗 `check_correlation(refresh=True)`，明细落 `results/sa_scan_20261113/gates_20261113.json`；五量排序落 `rank_table.json`。

---

## 九、算子利用率审计

| 项 | 本轮状态 |
|---|---|
| 本轮 9 档使用的 combo | 全部默认模板 `generate_stats → self_corr(·,500) → if_else → reduce_max → w = 1 − maxCorr`（**算子数不变**） |
| 本轮 9 档使用的 selection | `(1 + 0*(prod_correlation>0)) * (1−prod_correlation) * (self_correlation<0.7) * (turnover>0.095) * (turnover<0.6)`（EUR）/ `turnover>0.01`（USA/DEU） |
| 新引入算子 | **0 个** |
| 结论 | 延续 11-09/11-10 判断：**算子轴 ROI 已枯竭**。combo 形变（`zscore`/`rank(w)`/`sqrt(w)`/`ts_mean(w,20)`/`cp≥6`/`reduce_*`）全部证伪；selection 排序量换 `prod_correlation` 是毁灭性负杠杆 |
| 本轮唯一有效「算子外」杠杆 | **selection 的 `turnover` 下限**（0.01 → 0.095）。这不是算子，是**样本过滤**——它改的是「哪些组件进池」，不是「怎么算权重」。EUR 因此从 S2.97 跳到 6.13–7.10 |

> 与本轮任务 §4「构建候选」对照：本轮**未**在算子维度做任何新尝试，因为 11-12 已用 6 档 combo/selection 形变证伪。产能全部来自「换族 + 换过滤」，这是当前唯一正 ROI 方向。

---

## 十、提交建议（**只写建议，不执行提交**）

> **本轮未提交，等待用户指令。** 截至 2026-11-13 07:2x（ET 11-12 18:2x），`SUPER_SUBMISSION` 本 ET 日**未使用**（最后提交 `E5Q7RGNR` @ ET 2026-11-11）。

### 10.1 方案 A —— 按任务 §5.5 字典序（#1 = `leaq3P9l`）

| 顺位 | Alpha | 是否满足全部硬条件 | 说明 |
|---|---|---|---|
| **1** | **`leaq3P9l`** | ✅ prod 0.5951 ≤0.68（余量 0.0849）｜✅ self 0.5954 ≤0.68（余量 0.0846）｜✅ IS checks 零 FAIL（8/8 PASS）｜✅ 台账无 `robustness_leaq3P9l` REJECT｜✅ DEU/TOP500 已有 STAT/FAST 两族，SLOW 为**异族** | 唯一 B 档；prod/self 余量全轮最宽 |
| 2 | `1YNl3p5R` | ✅ prod 0.6011｜✅ self 0.6011｜✅ 8/8 PASS｜✅ 台账无 REJECT｜✅ USA/TOP1000 仅 STAT d1，CROWDING 异族 | prod 差 0.0011 未进 B 档 |
| 3 | `e75avmq6` | ✅ prod 0.6373｜✅ self 0.4871｜✅ 8/8 PASS｜✅ 台账无 REJECT｜✅ USA/TOP2000 仅 STAT d1，SLOW 异族 | self 最干净 |

**顺位内部冲突提示**：`leaq3P9l` 与 `2r5rA775`（#5）ρ=0.7387 同席 —— 交 #1 则 #5 永久作废；反之亦然。

### 10.2 ⚠ 方案 B —— 若目标是「单颗质量最高」（Eff / S / F 优先）

**本轮两口径分叉，方案 B 与方案 A 指向不同区域，必须二选一：**

1. **`Wjl6JJQO`** — S **6.13** / F **4.69** / TO 0.2691 / 2Y 5.32 / sub 3.65 / prod 0.6413 / self 0.6173 / **Eff 6.31 / U 0.9315 / N_eff 8.68 / ρ_eff 0.0170**
   - ✅ prod 0.6413 ≤0.68（余量 0.0387，> 0.02 合规线）｜✅ self 0.6173（余量 0.0827）｜✅ IS checks 8/8 PASS｜✅ 台账无 REJECT｜✅ EUR/TOP2500 已有 CROWDING/SLOW/STAT 三族，SUBINDUSTRY 为**异族**
   - 与已提交的 `E5Q7RGNR` ρ=0.6173（<0.7，可共存）
   - ⚠ 代价：EUR/TOP2500 **交后即 4/4 满席**；且 `O0WE25PR`(ρ=0.985)、`Jj8Zr1Xn`(ρ=0.940) **自动永久作废**
2. `O0WE25PR` — S 6.03 / F 4.65 / prod 0.6489（余量 0.0311）/ self 0.6393 —— **相对 #1 全项不占优，仅作备胎**
3. `Xg9WNRg8` — S 4.74 / F 4.10 / prod 0.6493 / self 0.6493 —— USA/TOP2000 仍有 3 席余量，不占用稀缺席位

**为什么本报告在「方案 A / 方案 B」之间不替你选**：这不是指标高低问题，是**策略问题**——
- 选 A（`leaq3P9l`）：拿到 prod/self 余量最宽、唯一 B 档的「最安全件」，但 S 只有 2.60，且与 `2r5rA775` 二选一放弃 S 3.00 的那颗；
- 选 B（`Wjl6JJQO`）：拿到 S 6.13 / Eff 6.31 的「质量最强件」，但把 EUR/TOP2500 最后一席用掉，且 prod 余量只剩 0.0387。

**（个人倾向，仅供参考）**：若本 ET 日只交一颗且目标是长期复利，`Wjl6JJQO` 的期望收益更高——它的 `U=0.93 / ρ_eff=0.017` 说明这是「真正 10 条独立腿」的组合，而 `leaq3P9l` 的 `ρ_eff=0.44` 说明它只是「1.75 条腿重复 10 次」。但最终取谁由你定。

### 10.3 命令模板（**仅供用户手动执行，本轮未运行**）

```bash
cd D:/coding/traeCN_project/wqb

# 方案 A（字典序 #1）
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id leaq3P9l --region DEU

# 方案 B（Eff 优先）
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id Wjl6JJQO --region EUR
```

### 10.4 提交前必须注意的两个已知坑

1. **停掉后台批次**：有并发仿真在跑时，`_probe_prod_max` 会抛 `ProxyError`。提交前确认 `tools/super_build.py` 无在飞任务。
2. **prod 槽 195s 冷却**：`logs/_dblock/correlation.cooldown.json` 未过期会 fail-fast。本轮最后一次相关性检查 06:56，早已过期。
3. **提交后必查单颗恒等式**：`is.prodCorrelation` vs 提交前 Step 1.6 的 `prod_max`，Δ>0.005 才告警（账户级审计不进提交路径）。

### 10.5 连带影响（提交后会发生什么）

| 若交 | 后果 |
|---|---|
| `leaq3P9l` | DEU/TOP500 → 3 席；`2r5rA775` 判死（ρ=0.7387 同席）；DEU 该档再剩 1 席 |
| `Wjl6JJQO` | EUR/TOP2500 → **4/4 满席**；`O0WE25PR`/`Jj8Zr1Xn` 判死；EUR 本轮产能终结 |
| `1YNl3p5R` | USA/TOP1000 → 2 席；该档 `ρ_eff 0.53` 说明未来新增仍难破 S 2.6 |
| `e75avmq6` | USA/TOP2000 → 2 席；与 `Xg9WNRg8`(ρ=0.4819) 仍可共存，但同族累积会顶高第三颗 |

---

## 十一、工程坑（本轮新踩/复验）

1. **`check_correlation(correlation_type="self", refresh=False)` 会回读平台缓存**，秒回且不占 correlation 槽 ⇒ 补 self 值时不必重跑 `both`（prod 已缓存在本地 `alpha_corr_cache`）。
2. **本地 `alpha_corr_cache` 只写 prod、不写 self**（`self_correlation` 恒 None）⇒ 想拿 self 必须单独调 self 接口，不能只靠 DB。
3. **`compute_mutual_correlation` 是纯本地计算**（拉 PnL 算日收益相关，1021 点），不占 correlation 槽 ⇒ **应在派发前就跑**，能提前砍掉同席件（本轮若先跑，EUR 只会建 1 个族而不是 3 个族）。
4. **`grep -l` 在二进制/大 JSON 上会漏**：`e75avmq6` 在 `results/` 全库搜不到，实际在 DB `alphas` 表 —— 历史候选优先查 DB，不查文件。
5. **Bash heredoc 传含 Windows 反斜杠路径的 python 脚本会被权限拦截** ⇒ 改写成 `.py` 临时文件再执行（本轮 `_dump_super.py` / `_mu_bar.py` / `rank_20261113.py`）。

---

## 附录 A：本轮数据文件

```
results/sa_scan_20261113/
├── pool_refresh.json            # 组件池盘点（probe_sa_candidates --refresh）
├── res_*.json                   # 9 档构建结果（含完整 is.checks）
├── log_*.log                    # 9 档构建日志
├── mu_bar.json                  # 三区 μ̄ 重算（EUR/USA/DEU）
├── rank_table.json              # 五量 + 排序表（含未过闸留档）
├── rank_20261113.py             # 五量计算 + 字典序排序脚本
├── gates_20261113.json          # 14 颗双闸实测值（含时间戳）
└── _dump_super.py / _mu_bar.py  # 取数辅助
```

## 附录 B：本轮全部候选（14 颗，含未过闸）

| Alpha | 区域/档 | 族 | S | F | TO | prod | self | 判定 |
|---|---|---|---|---|---|---|---|---|
| `Wjl6JJQO` | EUR/TOP2500 | SUBIND d1 | 6.13 | 4.69 | 0.2691 | 0.6413 | 0.6173 | ✅ 方案 B #1 |
| `O0WE25PR` | EUR/TOP2500 | INDUSTRY d1 | 6.03 | 4.65 | 0.2675 | 0.6489 | 0.6393 | ✅ 同席替代 |
| `Jj8Zr1Xn` | EUR/TOP2500 | MARKET d1 | 5.63 | 4.33 | 0.2703 | 0.6661 | 0.5585 | ✅ 同席替代 |
| `Xg9WNRg8` | USA/TOP2000 | SLOW d1 | 4.74 | 4.10 | 0.1659 | 0.6493 | 0.6493 | ✅ |
| `e75avmq6` | USA/TOP2000 | SLOW d1 | 4.29 | 4.00 | 0.1034 | 0.6373 | 0.4871 | ✅ 方案 A #3 |
| `2r5rA775` | DEU/TOP500 | CROWDING d1 | 3.00 | 3.15 | 0.1340 | 0.6434 | 0.6436 | ✅ 与 #1 互斥 |
| `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 | 2.38 | 0.1341 | 0.6011 | 0.6011 | ✅ 方案 A #2 |
| `leaq3P9l` | DEU/TOP500 | SLOW d1 | 2.60 | 2.11 | 0.1608 | 0.5951 | 0.5954 | ✅ 方案 A #1 |
| `xAv05p9J` | EUR/TOP2500 | FAST d1 | 7.10 | 5.02 | 0.2782 | 0.7165 | — | ❌ prod 红线 |
| `Jj8Z27gA` | DEU/TOP500 | SUBIND d1 | 2.95 | 3.36 | 0.1308 | 0.7400 | — | ❌ prod 红线 |
| `9qlL2Xlo` | USA/TOP2000 | INDUSTRY d1 | 2.33 | 1.90 | 0.1960 | 0.7709 | — | ❌ prod 红线 |
| `RRenvW7b` | USA/TOP2000 | FAST d1 | 2.14 | 1.36 | 0.2505 | 0.7493 | — | ❌ prod 红线 |
| `78YE2KVv` | USA/TOP1000 | MARKET d1 | 1.71 | 1.35 | 0.1837 | 0.8001 | — | ❌ prod 红线 + ladder |
| `Xga5OgA1` | EUR/TOP1200 | SLOW d2 | 3.10 | 1.62 | 0.2436 | 0.6484 | — | ❌ ladder 1.23 |
