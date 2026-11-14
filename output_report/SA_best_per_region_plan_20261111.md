# 各 Region 最优 SuperAlpha 方案 · 2026-11-11

> 本轮窗口：GMT+8 2026-11-11 06:30 → 08:xx｜平台 ET 日 = **2026-11-10**（ET 22:3x 起跑）
> 数据来源：`tools/probe/probe_sa_candidates.py --refresh`（06:33，清 `api_cache` 后全量回源）+ 本地 `slot_scan_local.py` 离线档位重建 + MCP `check_correlation(refresh=True)` 逐颗双闸
> 数据目录：`results/sa_scan_20261111/`
> **本轮独立决策**（§0.7）：上一轮任何"预选 / 明日首交"表述一律作废，本文件全部结论由本轮实测重新推导。

---

## 0. 执行摘要 · 按边际价值排序的优先队列

**本轮排序第一 = `QPv88bJW`（ASI / MINVOL10M / COUNTRY d3 / l10）** —— 唯一可行的**零 SUPER 档**候选，双闸 prod **0.5023** / self **0.2926**，IS 12 项全 PASS，同时命中社区合格档（B 档：TO 0.2607 < 0.30 ∧ prod 0.5023 < 0.60）。

| 优先序 | ID | 档位 | 席位类型 | S / F / TO | prod / self | 本轮判定 |
|---|---|---|---|---|---|---|
| **1** | `QPv88bJW` | ASI/MINVOL10M | **零 SUPER 档** | 3.61 / 2.55 / 0.2607 | **0.5023 / 0.2926** | **已提交 → ACTIVE**（B 档双达标，prod 余量 0.198） |
| 2 | `e75avmq6` | USA/TOP2000 | 已占档异族（第 2 族） | 4.29 / 4.00 / 0.1034 | 0.6373 / 0.4871 | 过闸（prod 余量 0.043） |
| 3 | `2r5rA775` | DEU/TOP500 | 已占档异族（第 3 族） | 3.00 / 3.15 / 0.1340 | 0.6434 / 0.6436 | 过闸（prod 余量 0.037，**本轮新建**） |
| 4 | `npvEEWO8` | ASI/MINVOL1M | 已占档异族（第 3 族） | 4.30 / 3.12 / 0.2455 | 0.6593 / 0.6593 | 过闸但余量仅 0.021 |
| 5 | `A1VAAbWe` | ASI/MINVOL1M | 已占档异族（第 2 族） | 4.60 / 3.33 / 0.2458 | 0.6634 / 0.6633 | 过闸但余量仅 0.017 |
| 6 | `gJaJazPM` | GLB/MINVOL10M | 已占档异族（第 2 族） | 3.97 / 1.78 / 0.2736 | **0.6850 / 0.6845** | **本方案 0.68 硬闸不过**（余量 0.015，**本轮新建**） |
| — | `YPaP1vmA` | EUR/TOP1200 | 零 SUPER 档 | 1.40 / 0.61 / 0.1630 | 未测（IS 已 FAIL） | **IS 3 项 FAIL，淘汰** |

**本轮实际提交：`QPv88bJW`（见 §8）**。其余 4 颗只挖不提交。
**同区互斥提示**：`QPv88bJW` 与 `A1VAAbWe` / `npvEEWO8` 同属 ASI ⇒ 本 ET 日 ASI 配额一经 `QPv88bJW` 占用，后两颗当日作废（非指标原因）。

### 本轮三条关键增量（相对 2026-11-10）

1. **★ ASI/MINVOL10M 是全新可用席位（零 SUPER），且样本外独立性真实成立**：`QPv88bJW` self **0.2926**（top1 `rKjY5vGj` 0.2926），并非"换宇宙标签的同一颗"。此前"MINVOL10M 错配全面劣化 S3.61 vs 4.60"只说明 S 变差，**没有说明它不可用**——本轮双闸证明它是干净新席。
2. **★★ DEU/TOP500 解除封档，但杠杆不是换族而是"池涨"**：同一 CROWDING d1 配方，11-09 在池 16 时 prod **0.6918**，本轮池 **18** 时 prod **0.6434**（−0.048），S 2.86→3.00。⇒ 强化 11-09 记录的"prod = 自我拥挤"的反面：**池增确实能压低 prod，只是需要足够多的新增组件**。
3. **★ EUR 零 SUPER 三档第 5 次确认结构性死**：本轮新建 EUR/TOP1200 SLOW d1 → S **1.40** / F **0.61** / Ladder **0.98**，3 项 FAIL（S<1.58、F<1.0、IS_LADDER<1.58）。EUR 池虽从 19 涨到 25，**ZERO_OS 三档的失效原因是宇宙截断压 S，与 prod 无关**，扩池救不了。EUR 全域转入永久停投。

---

## 1. 数据基线

### 1.1 组件池 eligibility（ACTIVE 且已提交 REGULAR，`probe --refresh` 2026-11-11 06:33）

| 区域 | ACTIVE REGULAR | 门槛 ≥10 | verdict | 相对 11-02 基线 |
|---|---|---|---|---|
| USA | 47 | ✅ | GO | +1 |
| IND | 47 | ✅ | GO | +2 |
| KOR | 35 | ✅ | GO | +5 |
| GBR | 28 | ✅ | GO | +7 |
| EUR | 25 | ✅ | GO | **+6** |
| MEA | 19 | ✅ | GO（**平台已下架，不可建**） | 0 |
| GLB | 18 | ✅ | GO | +1 |
| DEU | 18 | ✅ | GO | **+7** |
| ASI | 10 | ✅ | GO | +1 |
| HKG | 7 | ❌ 差 3 颗 | BLOCKED | 0 |

- 全账户 REGULAR ACTIVE 已提交 = **254** 颗（11-02 为 239）。
- 组件池口径 = **region × delay**（跨 universe 共享；11-06 实证 d0 池为 0 ⇒ 不能跨 delay 借池）。
- 本轮 `μ̄`（该区 ACTIVE 已提交 REGULAR 的 IS Sharpe 均值）用于 §5 五量：USA 1.9757｜IND 2.7302｜KOR 1.8586｜GBR 1.9064｜**EUR 2.0960**｜GLB 3.0089｜**DEU 1.8356**｜**ASI 2.3080**｜HKG 1.9757。

### 1.2 档位占用表（region × universe，52 颗 ACTIVE SUPER）

| 区域 | Universe | REGULAR | SUPER | 档内已有族的构成 | 分类 |
|---|---|---|---|---|---|
| ASI | **MINVOL10M** | 3 | **0** | — | **零 SUPER（本轮首选）** |
| ASI | MINVOL1M | 7 | 1 | STAT d2 | 已占（可试异族） |
| ASI | TOP500 | 0 | 0 | — | 零 OS（本区池 10 可建，未试） |
| DEU | TOP500 | 18 | 2 | STAT d1、FAST d1 | 已占（**本轮新增 CROWDING d1 已过闸**） |
| EUR | TOP2500 | 15 | 2 | STAT d1、CROWDING d1 | 已占 |
| EUR | TOPCS1600 | 10 | 1 | STAT d1 | 已占 |
| EUR | TOP1200 / TOP800 / TOP400 | 0 | 0 | — | 零 OS（**第 5 次确认 IS/结构性死**） |
| GBR | TOP700 | 28 | **6** | STAT×3(d1,d1,d5)、FAST、SLOW、REV&MOM | 饱和（≥5 ⇒ 换族失效） |
| GLB | MINVOL1M | 17 | 2 | SUBINDUSTRY d10、STAT d1 | 已占 |
| GLB | MINVOL10M | 0 | 1 | SLOW d1 | 已占（本区池 18 可试异族；本轮构建**仿真挂起未回**） |
| GLB | TOP3000 | 0 | 1 | REV&MOM d1 | 已占 |
| GLB | TOPDIV3000 | 1 | 1 | STAT d1 l15 | 已占（本轮 SLOW 构建 2 次 `Failed to create` ⇒ 探针档不可建） |
| IND | TOP500 | 47 | **12** | 全族谱 | 饱和 |
| KOR | TOP600 | 35 | **11** | 全族谱 | 饱和 |
| USA | TOP3000 | 38 | **6** | MARKET/SUBIND/STAT/FAST/SLOW×2 | 饱和（≥5） |
| USA | TOP2000 | 5 | 1 | STAT d1 l15 | 已占（**`e75avmq6` SLOW 异族已过闸**） |
| USA | TOP1000 | 0 | 1 | STAT d1 l15 | 已占（存量 SLOW/CROWDING 未本轮复测） |
| USA | TOP500 | 0 | 1 | CROWDING d1 | 已占（SLOW/FAST 历史 IS 失败） |
| USA | TOPSP500 | 0 | 1 | STAT d1 l38 | 已占（历史判死） |
| USA | TOP200 | 0 | 0 | — | 零 OS（2 颗存量 IS 均 FAIL，判死） |
| USA | ILLIQUID_MINVOL1M | 4 | 0 | — | **非法档位**（平台 400/500，见 §7） |
| MEA | TOP400 | 19 | 2 | SUBINDUSTRY×2 | **平台下架，不可建** |
| HKG | TOP800 | 7 | 0 | — | BLOCKED（池 7 < 10） |
| CHN/AMR | — | 0 | 0 | — | 池 0 |

**结构结论**：52 颗 SUPER 覆盖 17 个可用档；真正"零 SUPER 且池 ≥10"的只剩 **ASI/MINVOL10M**（EUR 三档与 USA/TOP200 已在 IS 层死）。本轮新增产能只可能来自 (a) 该零档，(b) 1–2 颗 SUPER 档的**异族**，(c) 池增长把已占档的 prod 压回线下（DEU 本轮实证）。

### 1.3 Pyramid 倍率与当季 lit（D1）

| 区域 | D1 均值倍率 | 当季已点亮类别（计数 ≥3） | 备注 |
|---|---|---|---|
| **DEU** | **1.61**（全账户最高） | analyst 6、model 3、shortinterest 3 | 倍率不当选塔理由 |
| GBR | 1.41 | model 6、pv 4、shortinterest 4、news 3、analyst 3、fundamental 3 | |
| KOR | 1.39 | analyst 4、shortinterest 4、fundamental 3、model 3、risk 3 | |
| EUR | 1.21 | analyst 10、model 3、fundamental 3、other 3、imbalance 3、sentiment 3 | |
| ASI | 1.18 | other 3 | |
| GLB | 1.18 | other 4、model 3 | |
| USA | 1.18 | analyst 6、model 4 | |
| IND | 1.14 | pv 11、news 4、other 4、analyst 3、model 3、fundamental 3、risk 3 | |
| HKG | 1.42 | pv 1 | 无 lit |

**塔信息口径说明**：SUPER alpha 的 `is.checks` 里**不存在** `MATCHES_PYRAMID`（本轮 5 颗候选逐颗核对：仅有 LOW_SHARPE / LOW_FITNESS / … / CLUSTER_TEST / SELF_CORRELATION / PROD_CORRELATION / SUPER_SUBMISSION / NON_SELF_SUPER_ALPHA / MATCHES_COMPETITION）。⇒ **SA 不参与 pyramid 计数**，塔归属对本轮 SA 排序不构成判据（与 REGULAR 候选的 ★★★ 塔必列规则不同口径，特此标注避免误套）。倍率仅作区域侧重参考，**不作选塔理由**。

---

## 2. 选点原则

排序严格按 §0.6.1 四条读法：

1. **席位边际 > 指标边际** —— 零 SUPER 档优先级最高。
2. **同族=死、异族可共存**（11-10 实测推翻"同档=同席"）——同族（仅 limit/decay/trunc 变）预期 self >0.9 可直接跳过；异族必须实测。**但档内 SUPER ≥5 后换族不再分散**（GBR 6 / IND 12 / KOR 11 / USA/TOP3000 6 四档本轮直接不建）。
3. **区内 U / ρ_eff / N_eff 无独立信息** —— μ̄、N 恒定 ⇒ 三者严格单调于 S，只在跨区可比。
4. **ΔCAP% 已退化** —— 加一颗到 52 颗 SA 池仅 +0.010%–0.018%，不作排序主键。真正有区分力的只有 **Eff / 席位类型 / 同族异族**。

按 §5.5 字典序执行：`① IS 零 FAIL → ② 席位/族边际 → ③ B 档双达标(TO<0.30 ∧ prod<0.60) → ④ prod 余量大 → ⑤ U 降序 → ⑥ Eff 降序`。

---

## 3. 论坛指标标准（§0 固化，本轮不重复调研）

### 3.1 组成数量（Selection Limit）
- 平台硬下限 **10**（<10 直接 400 `Ensure this value is greater than or equal to 10`）。
- 78 赞帖建议 30–100 起测、≤500；LY43440 实测 IND 取 300。
- **实际生效数 = min(limit, 组件池)**；组件池为 **region×delay 级**⇒ SA 指标天花板由该区 ACTIVE REGULAR 数决定。
- 本工作区实测：**l10 是双闸综合最优**（limit↑ ⇒ self↑ 且 prod↑；KOR l10 0.673 → l14 0.935）。

### 3.2 指标三档
| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | 5.6–7.0 | 5.6–8.9（冲 >10） | 0.20–0.27 | <0.5 |

本轮 **C 档 0 颗**；B 档 **1 颗**（`QPv88bJW`）；A 档 5 颗（含被淘汰的 `YPaP1vmA` 不达 A）。

### 3.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`（官方建议 1–4）。
⚠ **筛选强度必须匹配池规模**：加严约束后组件 <10 ⇒ `At least 10 component alphas are required`。小池区（EUR/GLB/DEU/ASI）只能用宽松 selection `(1 - self_correlation)`。本轮 5 颗全部使用宽松 selection —— 与历史 52 颗一致。

### 3.4 中性化族规律
- Fitness 排序（IND 实测）：CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3。
- 选族规则：TO<0.10 → SLOW；TO>0.20 → FAST。
- 区域族基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（须逐区验证）。
- ⚠ **组件数↑ ⇒ self↓ 但 prod↑**（EUR l10 self0.33/prod0.56 → l12 0.29/0.61 → l30 0.28）⇒ **l10 双闸综合最优**。
- **decay 深化的代价 = 稳健闸**：ASI 实测 F 2.89(d1)→2.99(d2)→3.03(d3)→3.18(d4,FAIL)→3.36(d5,FAIL) ⇒ decay ≥4 掉 `LOW_ROBUST_UNIVERSE_RETURNS`。**本轮 DEU CROWDING 取 d1，ASI 候选沿用 d3（d4 起必 FAIL）。**

### 3.5 其他固化实证
- truncation 0.02 vs 0.08 对 SA 几乎无差异。
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区历史 52 颗 SA 全用 **POSITIVE** 且均成功 ⇒ 本轮沿用。
- **universe 必须与成分对齐**：ASI 成分 7/10 在 MINVOL1M，错配 MINVOL10M 得 S3.61 vs 4.60（已四区复现）。**本轮 `QPv88bJW` 正是这条口径下的错配件，S 确实掉到 3.61，但双闸全过 ⇒ 「对齐」是 S 优化项、不是可用性判据。**
- **`combo_power` 在 limit == 池 时是 no-op**（S ±0.02），不构成杠杆。

---

## 4. 边际收益五量（§0.6，逐颗实算）

公式口径：
`U = S/(μ̄·√N)`｜`N_eff = (S/μ̄)²`｜`ρ_eff = (N·μ̄²/S² − 1)/(N−1)`｜`Eff = (S−μ̄)/max(prod,self)`｜`ΔCAP% = √(52/(1+51ρ))/√(51/(1+50ρ)) − 1`，`ρ = max(prod,self)`，`N = min(selectionLimit, 池)`。

| ID | 档位 | 席位类型 | N | μ̄ | S | F | TO | prod | self | **U** | N_eff | ρ_eff | **Eff** | ΔCAP% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `QPv88bJW` | ASI/MINVOL10M | **零 SUPER** | 10 | 2.3080 | 3.61 | 2.55 | 0.2607 | 0.5023 | 0.2926 | **0.4946** | 2.446 | 0.3431 | **2.592** | +0.0183% |
| `e75avmq6` | USA/TOP2000 | 异族（2nd） | 10 | 1.9757 | 4.29 | 4.00 | 0.1034 | 0.6373 | 0.4871 | 0.6867 | 4.715 | 0.1245 | **3.631** | +0.0106% |
| `2r5rA775` | DEU/TOP500 | 异族（3rd） | 10 | 1.8356 | 3.00 | 3.15 | 0.1340 | 0.6434 | 0.6436 | 0.5168 | 2.671 | 0.3049 | 1.809 | +0.0103% |
| `A1VAAbWe` | ASI/MINVOL1M | 异族（2nd） | 10 | 2.3080 | 4.60 | 3.33 | 0.2458 | 0.6634 | 0.6633 | 0.6303 | 3.972 | 0.1686 | 3.455 | +0.0095% |
| `npvEEWO8` | ASI/MINVOL1M | 异族（3rd） | 10 | 2.3080 | 4.30 | 3.12 | 0.2455 | 0.6593 | 0.6593 | 0.5892 | 3.471 | 0.2090 | 3.021 | +0.0096% |
| `gJaJazPM` | GLB/MINVOL10M | 异族（2nd） | 10 | 3.0089 | 3.97 | 1.78 | 0.2736 | 0.6850 | 0.6845 | 0.4174 | 1.741 | 0.4950 | 1.094 | +0.0080% |
| `YPaP1vmA` | EUR/TOP1200 | 零 SUPER | 10 | 2.0960 | 1.40 | 0.61 | 0.1630 | — | — | （0.2112） | （0.446） | — | — | — |

双闸实测时间：`QPv88bJW` 06:52｜`e75avmq6` 07:05｜`2r5rA775` 07:00｜`A1VAAbWe` 06:58｜`npvEEWO8` 07:02，全部 `refresh=True`（ET 2026-11-10 18:5x–19:0x）。

### 4.1 读法校验（必须遵守）
- **U / ρ_eff / N_eff 区内无独立信息**：ASI 三颗按 S 排序 ≡ 按 U 排序（4.60 > 4.30 > 3.61）；跨区不可直接比（μ̄ 不同）。
- **ΔCAP% 已退化**：最优 `QPv88bJW` +0.0183%，最差 `A1VAAbWe` +0.0095%，差距 <0.01 个百分点 ⇒ **不作排序主键**（本轮仅作记录）。
- **Eff 有区分力但不含席位信息**：`e75avmq6` Eff 3.631 最高，但它是**已占档的异族**；`QPv88bJW` Eff 2.592 虽低，却是**零 SUPER 新席**。按 §0.6.1-1「席位边际 > 指标边际」，`QPv88bJW` 优先。
- **`QPv88bJW` 的 ρ_eff 0.3431 是全部可交候选里唯一同时满足「零席 + prod<0.60 + TO<0.30」的一颗**。

---

## 5. 本轮边际收益排序表（§5.5，本轮提交唯一依据）

| 名次 | ID | ① IS 零 FAIL | ② 席位边际 | ③ B 档双达标 | ④ prod 余量 | ⑤ U | ⑥ Eff | 结论 |
|---|---|---|---|---|---|---|---|---|
| **1** | `QPv88bJW` | ✅ 12 PASS / 0 FAIL（1 WARNING: MATCHES_COMPETITION） | **零 SUPER（最高）** | ✅ TO 0.2607<0.30 ∧ prod 0.5023<0.60 | **0.198** | 0.4946 | 2.592 | **提交** |
| 2 | `e75avmq6` | ✅ 10 PASS / 0 FAIL | 异族 2nd | ❌ prod 0.6373 ≥ 0.60 | 0.043 | 0.6867 | 3.631 | 不交 |
| 3 | `2r5rA775` | ✅ 10 PASS / 0 FAIL | 异族 3rd | ❌ prod 0.6434 ≥ 0.60 | 0.037 | 0.5168 | 1.809 | 不交 |
| 4 | `npvEEWO8` | ✅ 11 PASS / 0 FAIL | 异族 3rd | ❌ prod 0.6593 ≥ 0.60 | 0.021 | 0.5892 | 3.021 | 不交 |
| 5 | `A1VAAbWe` | ✅ 11 PASS / 0 FAIL | 异族 2nd | ❌ prod 0.6634 ≥ 0.60 | 0.017 | 0.6303 | 3.455 | 不交 |
| 6 | `gJaJazPM` | ✅ 12 PASS / 0 FAIL（1 WARNING: CLUSTER_TEST 1.45/1.58） | 异族 2nd | ❌ prod 0.6850 ≥ 0.60 | **0.015（< 0.02 红线）** | 0.4174 | 1.094 | **不交（prod 硬闸 0.68 不过）** |
| ✗ | `YPaP1vmA` | ❌ 3 FAIL（S 1.40 / F 0.61 / Ladder 0.98） | 零 SUPER | — | — | — | — | 淘汰 |

**排序第一 `QPv88bJW` 在 ② 与 ③ 两项同时领先 ⇒ 名次不依赖 ④⑤⑥ 的取舍，结论稳健。**

---

## 6. 分 Region 方案

### 6.1 ASI —— 本轮唯一产能区（10 颗池，2 档）

| 档 | SUPER | 本轮动作 | 最优配方 | 预期 | 双闸实测 | 余量 | 结论 |
|---|---|---|---|---|---|---|---|
| **MINVOL10M** | 0 → **1（本轮提交）** | 存量复测（11-10 建的 `QPv88bJW`） | COUNTRY d3 l10 trunc 0.08 POSITIVE | S~3.6 / F~2.5 / TO~0.26 | prod **0.5023** / self **0.2926** | 0.198 / 0.407 | **✅ 已提交 → ACTIVE** |
| MINVOL1M | 1（STAT d2） | 存量复测 2 颗 | COUNTRY d3 l10 | S~4.6 | prod 0.6634 / self 0.6633 | 0.017 | 过闸但薄；同区互斥当日作废 |
| MINVOL1M | — | 同上 | SECTOR d3 l10 | S~4.3 | prod 0.6593 / self 0.6593 | 0.021 | 过闸但薄；同上 |
| TOP500 | 0 | 未建（本轮资源优先给零 SUPER 的 MINVOL10M） | — | — | — | — | 下轮可试（零 OS + 池 10 达标） |

**族封档**：ASI/MINVOL1M 已试 STAT d1/d2/d3/d5、SLOW d1、FAST d1、COUNTRY d1/d3/d4、CROWD d1/d3/d5、SECTOR d1/d2/d3、SUBIND d1 ⇒ decay ≥4 全 FAIL（`LOW_ROBUST_UNIVERSE_RETURNS`/`WITH_RATIO`），FAST d1 亦 FAIL。**只剩 INDUSTRY / MARKET / REV&MOM 三族未试，预期收益低。**

### 6.2 DEU —— 本轮唯一"因池增而解封"的区（18 颗池）

| 档 | SUPER | 配方 | S / F / TO | prod / self | 余量 | 结论 |
|---|---|---|---|---|---|---|
| TOP500 | 2（STAT d1、FAST d1） | **CROWDING d1 l10**（本轮新建 `2r5rA775`） | 3.00 / 3.15 / 0.1340 | **0.6434 / 0.6436** | 0.037 | ✅ 过闸，可作下轮备选 |
| TOP500 | — | STAT d1（`mLYLEm99`，10-18） | 2.27 / 1.67 / 0.1667 | 已 ACTIVE | — | 已占 |
| TOP500 | — | FAST d1（`vR1oxZA3`，11-07） | 3.27 / 3.09 / 0.1828 | 已 ACTIVE | — | 已占 |

**对照实证**：同一 CROWDING d1 配方 11-09（池 16）prod **0.6918**、11-11（池 18）prod **0.6434**。⇒ **池增 +2 颗压掉 0.048 prod**，DEU 从"封档"回到"可交"。仍有 SECTOR 0.7701 / MARKET 0.7708 两颗历史死档未复测（判粗族恒高 prod，可不复测）。

### 6.3 USA —— 存量异族可用，但本轮不交（同区/名次原因）

| 档 | SUPER | 候选 | S / F / TO | prod / self | 结论 |
|---|---|---|---|---|---|
| TOP2000 | 1（STAT d1 l15） | `e75avmq6` **SLOW d1 l10** | 4.29 / 4.00 / 0.1034 | 0.6373 / 0.4871 | 名次 2，只挖不提交 |
| TOP1000 | 1（STAT d1 l15） | 存量 SLOW / CROWDING 未本轮复测 | ~2.9 / ~2.0 / ~0.177 | 上轮 CROWDING prod 0.6011 | 下轮可复测 |
| TOP500 / TOPSP500 / TOP200 / TOP3000 | 1 / 1 / 0 / 6 | — | — | — | SLOW·FAST IS 失败 / 判死 / 饱和 |

**USA 全域矛盾**：TOP2000 与 TOP1000 是仅剩的两个 1-SUPER 档，但 `e75avmq6` 的 0.6373 prod 说明它撞的是自己 USA 池的拥挤，**再交一颗 USA 会把 TOP1000 一并毒化** —— 这也是本轮把它排到第 2 而非第 1 的实质理由。

### 6.4 GLB —— 4 档全占；本轮新建 1 颗（异族）刚好卡在 0.68 硬闸外

| 档 | SUPER | 本轮动作 | 结果 |
|---|---|---|---|
| MINVOL1M | 2（SUBIND d10、STAT d1） | 未建（11-09 已证第 3 族死：SLOW d1 → 0.7209） | — |
| **MINVOL10M** | 1（SLOW d1） | **建 STATISTICAL d1 l10 → `gJaJazPM`** | S **3.97** / F **1.78** / TO 0.2736，IS 12 PASS / 0 FAIL（CLUSTER 1.45 WARNING）；**prod 0.6850 / self 0.6845（top1 `LLMVPag1` 0.6845）** ⇒ 平台 0.7 能过，但**本方案 0.68 硬闸不过**，余量仅 0.015。⚠ 该档仿真耗时 ~35 min（universe 内 REGULAR=0，组件选取极慢），非挂起 |
| TOPDIV3000 | 1（STAT d1 l15） | 建 SLOW d1 l10 | **2 次 `[error] Failed to create simulation / None`**（非 429，单并发下复现）⇒ 该档 SLOW 配方不可建 |
| TOP3000 | 1（REV&MOM d1） | 未建 | 上轮 CROWDING+rank(w) self 0.6623/prod 0.6617 余量不足 |

### 6.5 EUR —— 第 5 次结构性死，转永久停投

| 档 | SUPER | 本轮动作 | S / F / Ladder | 判定 |
|---|---|---|---|---|
| TOP2500 | 2（STAT、CROWDING） | — | — | 已占，prod 墙历史 0.7337+ |
| TOPCS1600 | 1（STAT） | — | — | 已占 |
| **TOP1200** | 0 | **新建 SLOW d1 l10（`YPaP1vmA`）** | **1.40 / 0.61 / 0.98** → 3 FAIL | **IS 死，非 prod 问题** |
| TOP800 / TOP400 | 0 | 未建（历史 SLOW 1.47 / CROWDING 0.7117 / 0.7783） | — | 死 |

**结论**：EUR 零 OS 三档的失效机理是**宇宙截断压 S**（S 1.23–2.06，远低于 1.58），不是 prod 拥挤；池 19→25 对 S 无改善。**EUR 全域永久停投，不再派建。**

### 6.6 GBR / IND / KOR —— 档内 SUPER ≥5，换族失效，本轮不建

| 区 | 档 | SUPER | 已占族 | 理由 |
|---|---|---|---|---|
| GBR | TOP700 | **6** | STAT×3、FAST、SLOW、REV&MOM | 11-10 实测 INDUSTRY d1 prod **0.717**（第 6 颗后失效） |
| IND | TOP500 | **12** | 全族谱 | 唯一 universe；11-10 全族谱 0.72+ 双超 |
| KOR | TOP600 | **11** | 全族谱 | l14 self 0.935；CROWDING 0.7332/0.7333 双撞 |

### 6.7 MEA / HKG / CHN / AMR —— 结构性不可建

- **MEA**：平台 `Region MEA is not available`（11-02 / 11-04 / 11-24 三次复现），历史 2 颗仍 ACTIVE 但不可新建。
- **HKG**：池 7 < 10，差 3 颗；D1 倍率 1.42 但零 lit。
- **CHN / AMR**：池 0。

---

## 7. 停投区 + 撞墙档案

### 7.1 停投区（本轮更新）

| 区域/档 | 停投理由 | 首次判定 → 本轮确认 |
|---|---|---|
| **EUR 全域（含 TOP1200/800/400）** | ZERO_OS 三档 S 1.23–2.06 结构性不足；TOP2500 prod 墙 | 10-23 → **11-11 第 5 次** |
| **MEA 全域** | 平台下架（`Region MEA is not available`） | 10-24 → 11-11 第 4 次 |
| **IND / KOR** | 档内 SUPER 12 / 11，全族谱已占，self/prod 双 0.72+ | 10-28 → 11-11 第 6 次 |
| **GBR/TOP700** | 档内 6 颗，INDUSTRY 0.717 失效 | 11-10 → 11-11 |
| **USA/TOP3000** | 档内 6 颗（≥5） | 11-07 → 11-11 |
| **USA/TOP500** | SLOW 1.35 / FAST 1.63 IS 失败 | 10-27 → 11-11 |
| **USA/TOPSP500** | 历史 2Y 1.50–1.55 贴线，S 1.54 | 10-25 → 11-11 |
| **USA/TOP200** | 2 颗存量 IS 0 FAIL=0（S 0.94–1.28） | 10-27 → 11-11 |
| **GLB 全域** | 4 档全占；MINVOL10M 构建挂起、TOPDIV3000 建单失败 | 11-09 → 11-11（本轮新增 GLB/MINVOL10M **仿真挂起**） |
| **HKG / CHN / AMR** | 池 <10 / =0 | 10-21 → 11-11 |
| **ASI/TOP500** | 未建（非判死，仅本轮未派） | — |

### 7.2 本轮新增撞墙

| 档 | 配方 | 撞的点 |
|---|---|---|
| EUR/TOP1200 | SLOW d1 l10（`YPaP1vmA`） | S **1.40**（<1.58）、F **0.61**（<1.0）、IS_LADDER **0.98**（<1.58），CLUSTER 0.51 WARNING |
| GLB/TOPDIV3000 | SLOW d1 l10 | 建单失败 ×2（`Failed to create simulation / None`，单并发下复现，非 429） |
| GLB/MINVOL10M | STATISTICAL d1 l10（`gJaJazPM`） | prod **0.6850** / self 0.6845 ⇒ 平台 0.7 可过，**本方案 0.68 硬闸不过**（余量 0.015）；仿真耗时 ~35 min（universe 内 REGULAR=0） |
| USA/ILLIQUID_MINVOL1M | STATISTICAL d1 l10 | **非法档位**：`USA 合法 universe = ['TOP3000','TOP2000','TOP1000','TOP500','TOP200','TOPSP500']`，平台回 HTTP 500 |

---

## 8. 执行清单

### 8.1 本轮构建（5 次派发 / 4 次成功）

| # | 命令核心 | alpha id | 结果 |
|---|---|---|---|
| 1 | `select --region EUR --universe TOP1200 --delay 1 --neutralization SLOW --decay 1 --selection-limit 10` | `YPaP1vmA` | S1.40/F0.61 → **IS 3 FAIL** |
| 2 | `select --region DEU --universe TOP500 --delay 1 --neutralization CROWDING --decay 1 --selection-limit 10` | `2r5rA775` | S3.00/F3.15 → **全 PASS，prod 0.6434** |
| 3 | `select --region GLB --universe MINVOL10M --delay 1 --neutralization STATISTICAL --decay 1 --selection-limit 10` | `gJaJazPM` | S3.97/F1.78 → **全 PASS，但 prod 0.6850 超 0.68 硬闸**（耗时 ~35 min） |
| 4–5 | `select --region GLB --universe TOPDIV3000 --delay 1 --neutralization SLOW --decay 1 --selection-limit 10` | — | **建单失败 ×2** |
| ✗ | `select --region USA --universe ILLIQUID_MINVOL1M …` | — | **非法档位，本地前置拦截** |

全部统一参数：`--self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0`，`selectionHandling=POSITIVE`，`truncation 0.08`。

### 8.2 配额约束

- **SUPER 配额 = 1 / 天 / 区**（平台强制，历史零违规）。
- ET 当前日 **2026-11-10**；本账户当日 SUPER 提交数 = **0**（最近一颗 `d5WGG5bg` 为 ET 2026-11-09）⇒ **ASI / USA / DEU 当日配额全部可用**。
- 并行上限：仿真 **2 路**（第 3 路必 429）；prod 相关性 **1 路**（`correlation_busy` 需等待，不重派）。

### 8.3 ★ 本轮提交判定（方案落盘后才执行）

**提交对象：`QPv88bJW`（ASI / MINVOL10M / COUNTRY d3 / l10）** —— 逐条核对 §7 五道硬闸：

| # | 硬闸 | 实测值 | 判定 |
|---|---|---|---|
| 1 | `prod < 0.68` 且 `self < 0.68`（本轮 `refresh=True`） | prod **0.5023** / self **0.2926** | ✅ 余量 0.198 / 0.407 |
| 2 | IS checks **零 FAIL** | 12 PASS / 0 FAIL / 1 WARNING(MATCHES_COMPETITION) | ✅ |
| 3 | 该 region 当日 SUPER 配额未用 | ASI 最近提交 ET 2026-11-09，当日 0 颗 | ✅ |
| 4 | 同档已有 SUPER 时须异族且 self<0.68 | 该档 SUPER = **0**（零 SUPER 档，无需异族论证） | ✅ |
| 5 | `robustness_QPv88bJW` 台账无 REJECT | 台账无该条记录（非 REJECT） | ✅ |

**执行记录**：见 §8.4（提交后回填）。

### 8.4 提交结果

**`QPv88bJW` 已提交 → `status=ACTIVE`**（name `ASI_S_10comp_v88bJW`，region ASI，POST 201，`dateSubmitted` = **ET 2026-11-10 17:49:56**；旧记的 22:5x 实为 **UTC**，见 §8.5 时区坑）

| 项 | 值 |
|---|---|
| 提交前 prod（probe） | **0.5023** |
| `submit` 内置 prod 闸轮询 | attempts=2 → max **0.5023** < 0.7 → 过闸 |
| POST 回执 | HTTP **201** success=True reason=`Accepted (async); IS checks still computing` |
| flip 窗复核（~250s 后） | **`status=ACTIVE`**，IS 12 PASS / 0 FAIL / 1 WARNING |
| 提交后 prod 复核 | **0.5023**（`provisional=false`，cache 06:35）⇒ Δ = **0.0000** < 0.005 ✅ 无漂移 |
| self | 0.2926（top1 `rKjY5vGj`） |
| 配额 | ASI 本 ET 日（2026-11-10）由 0/1 → **1/1 用满** |
| 性质 | 用户 2026-11-10 明令授权「每轮自动提交排序第一」⇒ 合规提交，非 agent 自作主张 |

**连带影响（写进下轮前置条件）**：
1. **ASI 当日配额已用尽** ⇒ `A1VAAbWe` / `npvEEWO8` 本 ET 日作废；下一 ET 日两者仍在池且 prod 可能被新 ACTIVE 顶高，**必须重测**。
2. **ASI/MINVOL10M 由"零 SUPER"翻为 1 颗 SUPER** ⇒ 该档下一轮起降级为"已占档"，只能按异族评估。
3. **ASI 全域 2 颗 ACTIVE SUPER（MINVOL1M + MINVOL10M）**，本账户 SUPER 总数 52 → **53**。

### 8.5 用户指令追加提交 `e75avmq6`（USA/TOP2000）—— 被 `SUPER_SUBMISSION` 日配额挡下

用户 2026-11-11 08:45（GMT+8）指令「提交 e75」。执行 `super_build.py submit --alpha-id e75avmq6 --region USA`，结果 **BLOCKED**：

| 环节 | 结果 |
|---|---|
| 全局禁提交闸 | `WQB_ALLOW_ALPHA_SUBMIT=1` 放行（用户本条指令即授权；闸本身无豁免，靠 env 开启） |
| prod 闸（轮询 900s 窗口） | attempts=2 → max **0.6373** < 0.7 → **过闸**（与本轮 `refresh=True` 实测一致，无漂移） |
| IS 零 FAIL 复查 | ✅ 8 PASS（LOW_SHARPE 4.29 / LOW_FITNESS 4.00 / TO 0.1034 / SUBUNIV 2.60 / LADDER 3.94 / CLUSTER 2.65）+ 4 PENDING + 1 WARNING |
| 属性写入 | ✅ name `USA_S_10comp_5avmq6`（按 alpha_id 尾 6 位）；selection 197 词 / combo 152 词 |
| 提交层预检 `GET /submit` | HTTP 404（SUPER 上恒 404，不作判据） |
| **POST `/submit`** | **HTTP 403**，唯一 FAIL = **`SUPER_SUBMISSION` value=1 / limit=1** |

**根因（时区误判，非候选缺陷）**：真实 ET 时间为 **2026-11-10 19:45 EST**，本 ET 日的 1 颗 SUPER 配额已被 `QPv88bJW`（ET 11-10 17:49）用掉，间隔仅 **1.93 h**。`SUPER_SUBMISSION` 是 **1 颗 / ET 日历日、00:00 ET 重置**（`pipeline.py` 与 skill 口径一致，历史反例 11-07 22:48 → 11-08 22:37 仅隔 23h49m 仍成功，证伪"48h 滚动"）。重置点 = **ET 2026-11-11 00:00 = GMT+8 今天 13:00**。

**★ 工程坑（本轮新增，务必复用）**：Git Bash 里 `TZ=America/New_York date` **在本机不生效**，它返回的是 **UTC**（本轮第一次读成 "ET 2026-11-11 00:43"，据此一度误判"已跨 ET 日、USA 配额空闲"）。唯一可信读法是 `wqb.timeutil.et_now() / et_today / et_day_bounds_utc`（或 Python `zoneinfo` + `datetime.now(timezone.utc).astimezone(ZoneInfo('America/New_York'))`）。Run 17 记忆里的 "ET 22:5x" 同样是 UTC 换算错误，已校正为 17:49。

**代价与状态**：403 **不消耗配额**（`value` 未增加）、**不判死候选**。`e75avmq6` 仍 `stage=IS / status=UNSUBMITTED`，属性已就绪，**该 ET 日重置后重跑即可**，无需重建、无需重测双闸（prod 0.6373 / self 0.4871 本轮实测仍有效）。

---

## 9. 算子利用率审计（官方 Combo/Selection 清单 vs 本仓实际）

| 维度 | 官方可用 | 本仓已用 | 利用率 | 本轮新增 |
|---|---|---|---|---|
| COMBO 算子 | 160（《SuperAlpha Operators》附录） | 5：`generate_stats` / `if_else` / `reduce_max` / `self_corr` / `ts_ir`(1 次) | **3.1%** | **0** |
| SELECTION 算子 | 43 | 1：`(1 - self_correlation)` | **2.3%** | **0** |

- 全部 44 颗已构建 SA 的 combo 模板逐字相同：`stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); w = 1 - maxCorr; w`。
- 已证负向、不可再用：`zscore(w)`（中心化致半数反向，S −1.14）、`rank(w)^3`（Ladder FAIL）、`sqrt(w)`/`ts_mean(w,20)`（撞同席 0.99）、`combo_power≥6`（Ladder 恰好 1.58 FAIL）、`reduce_avg`/`reduce_percentage`（Ladder FAIL）。
- **结论**：算子轴 ROI 已枯竭（本轮新增 0，与 11-09/11-10 一致）。产能只来自 **席位（零 SUPER 档）** 与 **池增长**，不是算子组合。

---

## 10. 下轮（ET 2026-11-11 起）唯一正确顺序

1. 刷池 → 档位表 → 复测双闸 → **本轮新排序表** → 落盘 → 按新第 1 名提交（**不得沿用本轮 `QPv88bJW` 已交的事实做任何预选**）。
2. 优先探针：**ASI/TOP500**（零 OS + 池 10 达标，唯一未试探的零 SUPER 档）。
3. **`gJaJazPM`（GLB/MINVOL10M）是最接近线的存量异族**（prod 0.6850 / self 0.6845）：若 GLB 池继续增长（18→≥20）可复测，**否则不派**。GLB/TOPDIV3000 SLOW 已证建单不可行，不再派。
4. 备选池（只挖不提交）：`e75avmq6`（USA/TOP2000，最优余量 0.043）、`2r5rA775`（DEU/TOP500）、`gJaJazPM`（GLB，需池增）、`A1VAAbWe`/`npvEEWO8`（ASI/MINVOL1M，**须重测**：`QPv88bJW` 已 ACTIVE，同区 prod 会被顶高）。
5. 不派：EUR 全域、MEA、IND、KOR、GBR、USA/TOP3000·TOP500·TOPSP500·TOP200、GLB 其余三档、HKG、CHN、AMR、USA/ILLIQUID_MINVOL1M（非法）。
6. ⚠ 工程：GLB/MINVOL10M 这类"universe 内 REGULAR=0"的档仿真需 **~35 min**，勿按 8 min 判挂起（本轮误判一次，实际成功）。
