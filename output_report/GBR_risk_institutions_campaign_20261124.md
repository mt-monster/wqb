# GBR 战役报告 · risk/institutions 未亮塔（2026-11-24）

> 目标（用户 2026-11-24）：GBR 固定区，按 `wq-brain-ra-gbr` SOP，交付 10 个通过验证的 regular alpha（ATOM 优先）。
> 本报告为**过程底稿**：只写已实测事实；未完成项明确标「未完成」，不把 near 当交付。

---

## 1. 区域与塔位（平台实时，2026-11-24）

GBR D1 塔位（`get_pyramid_alphas`）：

| 塔 | 已提交 | 状态 | 本波可否投入 |
|---|---:|---|---|
| model | 6 | 已点亮 | 否 |
| pv | 5 | 已点亮 | 否 |
| shortinterest | 5 | 已点亮 | 否 |
| news / other / analyst / fundamental | 3 / 3 / 3 / 3 | 已点亮 | 否 |
| earnings | 2 | 未点亮（剩 1 席） | 数据层受限 |
| **institutions** | **1** | **未点亮（剩 2 席）** | **是** |
| **insiders** | **0** | **未点亮（3 席）** | **是** |
| **risk** | **0** | **未点亮（3 席）** | **是** |
| imbalance | 1 | 未点亮（剩 2 席） | PV 组腿受限 |
| sentiment / option / macro / socialmedia | 0 | 未点亮 | sentiment/option/macro 已死；socialmedia 未测 |

---

## 2. 库存收割（零仿真，本地台账 + 平台复核）

| 候选 | 数据集 | 平台指标 | 逐年 | self | prod | 判定 |
|---|---|---|---|---|---|---|
| **WjlOZZnd** | risk72 + risk68 | S1.76 / F1.42 / **2Y2.14** / TO9.96% / RA fails=0 / sub1.08 / inv1.46 | **10/10 年 lc+sc>0 且 pnl>0** | **0.5796 PASS** | **0.7987 FAIL** | **全闸 IS，唯一缺口 prod** |
| **1YW0Oa2W** | institutions25 | S1.23 / F0.71 / **2Y1.93** / TO9.35% / RA fails=2（LOW_SHARPE/LOW_FITNESS）/ sub1.02 | **10/10 年正** | **0.166 PASS** | **0.331 PASS** | near：仅 S/F 差，相关头寸极干净 |
| Xga1Ae00 | imbalance5+PV | S2.15 / F1.17 / 2Y1.86 / RA0 | 10/10 正 | 0.7613 FAIL | 0.7614 FAIL | 双墙；且含 PV 腿 |
| P0gbMLz7 / A1v5QXmg | earnings6 | S1.77/1.72, 2Y2.06/1.67 | **2014–2018 连续 5 年零持仓** | — | — | **数据层排除** |
| omEPQrLE / zq3AX08o / d5W9eobx | shortinterest | S1.82/1.80/1.75, 2Y3.03/2.96/2.98 | — | — | — | 塔已 5/3 点亮 ⇒ 不可投入 |
| 1YWlbQb6 / 1YWOGvmQ / N1PLLxjw | imbalance5+PV | S3.16/3.03/2.49, prod0.5732/0.5523/0.6232 | — | — | — | 含 `ts_rank(volume)` PV 腿；GBR 旧规禁、新指令限 5 组 |

**关键篮内事实**：`WjlOZZnd` × `1YW0Oa2W` 互相关 **−0.1812**（risk × institutions，天然对冲，可同篮且分属两塔）。

---

## 3. 全字段画像（归档）

| 数据集 | 字段数 | 档案 | 完整性闸 |
|---|---:|---|---|
| risk72 | 23（MATRIX16/VECTOR7） | `tracking/GBR/reference/datasets/risk72.md` | ✅ PASS |
| risk71 | 6（MATRIX6） | `tracking/GBR/reference/datasets/risk71.md` | ✅ PASS |
| insiders1 | 9（VECTOR9） | `tracking/GBR/reference/datasets/insiders1.md` | ✅ PASS |
| socialmedia12 | 6（MATRIX2/VECTOR4） | `tracking/GBR/reference/datasets/socialmedia12.md` | ✅ PASS |
| socialmedia5 | 13（VECTOR13） | `tracking/GBR/reference/datasets/socialmedia5.md` | ✅ PASS |

> 闸：`python tools/gates/field_profile_completeness_gate.py --profile <path>`，5/5 PASS（分母逐字段、无通配）。
> 已有档案：institutions6 / institutions25 / insiders12 / risk60 / risk68 / imbalance5。
> **探针（longCount/shortCount）**：批 A `gxvmf3pu4JkbByS64694P2` 在飞（risk72 前 10 字段）；批 B/C（risk72 后 13 + risk71 6）按 **≤8 臂/批** 待发。

---

## 4. 证据闸（S2）

- 论坛：`44639524994583`（GBR/TOP700 `residualized_return_nogroup` + 52 日窗 t 值 + 三子窗门控，S1.77/F1.01/TO15.8%，**prodCorr 0.648**；作者结论「换表达，不是调参数」）；`45235010628247`（Risk Neutralization 六档 + `vector_neut`/`regression_neut` 先剥因子）；`44557078934039`（F 换手下限 12.5%，慢腿推高 prod）。
- 论文：`tools/research/paper_search.py --diverse` → **5/5 篇、5/3 作者**（特质波动/收益反转，DOI 见台账）。
- 留痕：ledger `forum_recon_risk72_20261124` + `forum_paper_recon_risk72_20261124`。

---

## 5. 批次状态（终态，2026-11-24 01:0x）

| 批 | 内容 | multi-sim id | 臂数 | 状态 |
|---|---|---|---:|---|
| A | risk72 前 10 字段探针（@NONE/decay0/trunc0/nanOFF） | `gxvmf3pu4JkbByS64694P2` | 10 | **平台停摆，未出 children** |
| D | 模板筛选：`top2500_..._nogroup` × 8 时序核 + 2 轴 | `14ilgZ4314FkaBm1coXIevo8` | 10 | **平台停摆，未出 children** |
| 诊断 | `ts_ir`/`ts_zscore` 2 臂最小批 | `L7iiL3Wy5dw8Ik19tRB4KA4` | 2 | **平台停摆，未出 children** |

> **判定**：三批均 ≥20 分钟停在 `progress=0.15 / children=0`（最小 2 臂批同态）⇒ 平台仿真服务本时段停摆/队列冻结（美东午间高峰）。已停止重发避免堆积死批。平台恢复后先 `batch_status`/`harvest_multisim_alphas` 收割上述三个 id，再按 ≤8 臂续跑批 G/H/F。
> 用户 2026-11-24 追加约束：**每批最多 8 臂**（A/D 为约束前派发）。

## 5b. 本时段已确认成果（零仿真）

1. S-PRE 塔位/库存复查（§1/§2）。
2. 全字段画像 5 份新归档 + 完整性闸 5/5（§3）。
3. 论坛/论文证据与 ledger 留痕（§4）。
4. 指标级核验：`WjlOZZnd`（risk，全闸 IS，唯一缺口 prod 0.7987）、`1YW0Oa2W`（institutions，prod 0.331/self 0.166，仅 S/F 差）；两者互相关 −0.1812，可同篮、分属两塔。
5. 已预检待发（8 臂，全字段 valid）：批 G（WjlOZZnd 降 prod 结构扫）、批 H（insiders12 反向）、批 F（institutions×risk gating/residual）。

---

## 6. 结构性阻塞（必须如实记录）

1. **10 颗目标在当前 GBR 面内不可达**：未亮塔仅 institutions(2)/insiders(3)/risk(3)/imbalance(2)/earnings(1)/socialmedia(3) 共 14 席理论值，但
   - earnings6/insider_matrix 等数据窗口 2019+ 或覆盖 14–24 只 ⇒ 数据层排除；
   - imbalance5 全闸件均含 PV 腿（旧规禁；新指令限 5 组）；
   - 已点亮塔（model/pv/shortinterest/news/other/analyst/fundamental）的海量高 S 件一律不可投入（3c）；
   - 库存中唯一「全闸 IS」件 WjlOZZnd 卡 prod 0.7987；1YW0Oa2W 卡 S/F。
2. **混腿禁令**把库存里 S2.2–2.5 的多条 add 件（risk72+loaned 等）全部作废——这不是信号问题，是组合形态合规问题。
3. **平台队列**：2026-11-24 00:2x（北京时间）≈ 美东午间，两批 10 分钟内均停在 progress 0.15（children=0），属平台侧排队，不是表达式错误。

---

## 7. 下一步（按价值排序）

1. 收批 D：若某时序核 S≥1.58 且 prod<0.70 ⇒ 直接进验证链（逐年→IS→self/prod→互相关）。
2. 收批 A/B/C：补齐 risk72/risk71 全字段探针读数，回填画像 §10.1。
3. 8 臂批 F：institutions25 × risk72 的 **gating/residual** 五形态（禁 add），目标把 1YW0Oa2W 的 S/F 抬过闸且保持 prod<0.70。
4. 8 臂批 G：WjlOZZnd 的 field/axis/neut 变体（降 prod 0.7987→<0.70）。
5. 8 臂批 H：insiders12 反向模板（现天花板 ≈0.70，需换表达验证）。
6. 8 臂批 I：socialmedia12/5 注意力/情绪首测（塔 0/3，全新面）。

**交付纪律**：任何一颗提交前必须用户明确确认；当前**已确认可交付 0 颗**。
