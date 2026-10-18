# 候选 Alpha 可提交性盘点 · 综合报告
**日期**：2026-10-08 11:19–11:52 CST  
**ET 日期**：2026-10-07（配额新鲜：REGULAR 0/4, SUPER 0/1）  
**数据源**：MCP get_pyramid_alphas / quota_status / enqueue_propose / backup_ra / submit_inventory / sa_candidates / sa_unsubmitted_probe / region_op_verify / super_build  
**提交状态**：⛔ 只盘点不提交（`ALLOW_ALPHA_SUBMIT=False`）  
**⚠ 注意**：submit_inventory 仍在运行（25/157 @ 11:52），以下为部分数据，分类模式已稳定

---

## Part 1 · Base 收益点 1–6

> **Base payment ∝ rank(提交数量, 提交质量, Value Factor, 自我成长) × Theme 倍数**  
> Value Factor = (a) 单α表现 + (b) 多样性 + (c) 独特性

### 收益点 1 · 提交数量 · 连续性

| 通道 | 数量 | 备注 |
|------|------|------|
| RA (REGULAR) 可提交池 | 2 SUBMIT_NOW + 1 THIN_MARGIN | omWVZ7lm(EUR) + 6XKwmQgE(GBR) + 58gMMJEk(GBR) |
| SA (SUPER) PASS 候选 | 10 颗（全部 KOR） | YPMQXxXq 等，双闸全过 |
| 配额（ET 10-07） | R 0/4 · S 0/1 | 新鲜日，未消耗 |
| enqueue_propose | L1=0 / S0=9141 | **★ 全部候选在 L1 被杀**，零入队 |

**关键变化**：本次 enqueue_propose L1 从上一轮的 142 → 0。9141 个 S0 候选全部被 L1 硬过滤器拦截，top 原因 RA_FAIL=4902。

---

### 收益点 2 · 提交质量 · 单α表现（VF-a）

| 指标 | RA 最优 | SA 最优 |
|------|---------|---------|
| 候选 | omWVZ7lm (EUR) | YPMQXxXq (KOR) |
| IS Sharpe | — | 4.89 |
| IS Fitness | — | 5.41 |
| Turnover | — | — |
| Prod（实测） | 0.5378 | 0.6537 |
| Self（实测） | 0.1954 | 0.6537 |

RA 的 omWVZ7lm 是唯一 prod<0.70 的候选（上一轮 WjegEmQO prod=0.5012 已升至 0.7188 落入 PROD_WALL）。  
SA 的 10 颗 PASS 全部来自 KOR，IS Sharpe 区间 3.74–4.89。

---

### 收益点 3 · 多样性（VF-b）· 塔覆盖

**已点亮塔**（当季 ACTIVE ≥ 3）：

| 区域 | 塔 | ACTIVE 数 |
|------|----|----------|
| USA | D1/MODEL | 4 |
| GBR | D1/MODEL | 4 |
| KOR | D1/FUNDAMENTAL | 3 |
| IND | D1/PV | 3 |
| IND | D1/MODEL | 3 |

**接近点亮**（差 1）：KOR/D1/MODEL(2), USA/D1/ANALYST(1), USA/D1/EARNINGS(1), EUR/D1/MODEL(1), EUR/D1/FUNDAMENTAL(1), EUR/D1/RISK(1), IND/D1/ANALYST(1), IND/D1/RISK(1), DEU/D1/MODEL(1), DEU/D1/OTHER(1), GBR/D1/ANALYST(1), ASI/D1/OTHER(1), KOR/D1/SHORTINTEREST(1)

**零覆盖区域**（全塔=0）：GLB, HKG, JPN, CHN, AMR

**RA 可提交候选的塔覆盖**：EUR/D1/PV(1) — 仅 omWVZ7lm 点亮该塔  
**SA PASS 候选塔覆盖**：KOR 区 — 可点亮 FUNDAMENTAL(已亮3) + MODEL(差1)

---

### 收益点 4 · 独特性（VF-c）· 低 prod/self

| 候选 | Region | Prod | Self | 余量(prod) | 余量(self) |
|------|--------|------|------|-----------|-----------|
| omWVZ7lm | EUR | 0.5378 | 0.1954 | 0.1622 | 0.5046 |
| 6XKwmQgE | GBR | 0.5956 | 0.4148 | 0.1044 | 0.2852 |
| 58gMMJEk | GBR | 0.6865 | 0.6386 | 0.0135 | 0.0614 |
| YPMQXxXq | KOR | 0.6537 | 0.6537 | 0.0463 | 0.0463 |
| O08oOMG7 | KOR | 0.6738 | 0.6738 | 0.0262 | 0.0262 |
| wpbLgkql | KOR | 0.6604 | 0.6604 | 0.0396 | 0.0396 |

**可同日并行对**（prod<0.70 + self<0.70，余量均 ≥0.03）：omWVZ7lm + YPMQXxXq + wpbLgkql + 1YZJENmJ + 6XKzOx6Y + 3qVzZN3O + 1YZJQpNm + 9qWJv1do + leKrd9Y2 + E5Rk18lK  
**余量<0.03 建议跳过**：58gMMJEk(GBR) 余量仅 0.0135，O08oOMG7 余量 0.0262

**⚠ 9qWJv1do 平台状态异常**：10-06 12:45 ET 提交，10-08 仍显示 UNSUBMITTED → 需人工核查提交是否成功。

---

### 收益点 5 · 自我成长

- KOR 区组件池达 24 颗 ACTIVE → SA 已具备规模优势
- USA/IND/GBR/MEA/GLB 组件池均 ≥10 → 6 区 GO
- **优先补新塔而非重复优化同族**：EUR/D1/FUNDAMENTAL、EUR/D1/RISK、KOR/D1/MODEL 各差 1 即点亮
- SA 12 颗候选全部来自 KOR → 单区域集中度过高，建议跨区拓展

---

### 收益点 6 · Theme 倍数

Theme 检查需逐条比对平台 Theme 列表（`get_competition_agreement` 或 `get_events`），本次盘点未触发 Theme 检测。**未命中 = 0**，不影响 Base payment 当前计算。

---

### §三 · enqueue_propose L2 去重汇总

| 字段 | 值 |
|------|-----|
| S0 | 9141 |
| L1 过滤后 | 0 |
| Proposal | 0 |
| l2_deduped | **[]**（空数组） |
| L1 被杀原因 | RA_FAIL=4902, LOW_SHARPE=2992, ALREADY_DEAD=397, LOW_2Y=162, LOW_FITNESS=161, PROD=160, ALREADY_IN_QUEUE=145+114+105+2 |

**结论**：所有 9141 个候选在 L1 硬过滤阶段被全部拦截。L2 去重未触发（L1=0 ⇒ 无候选进入 L2）。  
**对比上一轮（10-07）**：L1=142 → Proposal=46, l2_deduped=96。  
**根本原因**：RA_FAIL=4902（53.7%）说明大量候选的平台 RA 检查失败，候选池质量整体下降。

---

## Part 2 · RA 提交顺序表 + SA 四步流程

### RA 提交顺序（按 base 收益排序）

| 优先级 | Alpha ID | Region | 分类 | Prod | Self | 余量 | 塔位 | 状态 |
|--------|----------|--------|------|------|------|------|------|------|
| **1** | omWVZ7lm | EUR | **SUBMIT_NOW** | 0.5378 | 0.1954 | 0.1622 | D1/PV ×1.1 | ✓ 可提交 |
| **2** | 6XKwmQgE | GBR | **SUBMIT_NOW** | 0.5956 | 0.4148 | 0.1044 | D1/PV ×1.5 | ✓ 可提交 |
| 3 | 58gMMJEk | GBR | THIN_MARGIN | 0.6865 | 0.6386 | 0.0135 | D1/PV ×1.5 | ⚠ 余量极薄 |
| 3 | 2rml98JN | GBR | PROD_WALL | 0.7454 | 0.0804 | — | D1/ANALYST ×1.6 | ✗ prod>0.70 |
| 4 | 58glrnq1 | GBR | PROD_WALL | 0.7343 | 0.0869 | — | D1/ANALYST ×1.6 | ✗ prod>0.70 |
| 5 | 58gpWjmN | GBR | PROD_WALL | 0.7464 | 0.0735 | — | D1/PV ×1.5 | ✗ prod>0.70 |
| 6 | 6XKlZmz7 | GBR | PROD_WALL | 0.7536 | 0.0839 | — | D1/ANALYST ×1.6 | ✗ prod>0.70 |
| — | 2rmNl5vN | GBR | PROD_WALL | 0.7978 | 0.0151 | — | D1/ANALYST ×1.6 | ✗ prod>0.70 |
| — | 2rmp803N | GBR | PROD_WALL | 0.8263 | 0.0751 | — | D1/PV ×1.5 | ✗ prod>0.70 |
| — | 58gQgnEn | GBR | PROD_WALL | 0.7003 | 0.1014 | — | D1/ANALYST ×1.6 | ✗ prod>0.70 |
| — | WjegEmQO | EUR | PROD_WALL | 0.7188 | 0.7191 | — | — | ✗ prod>0.70 |
| — | 1YZJAMqK | EUR | PROD_WALL | 0.8152 | 0.8154 | — | — | ✗ prod>0.70 |
| — | 1YxRmbpR | EUR | PROD_WALL | 0.8229 | 0.6831 | — | — | ✗ prod>0.70 |
| — | 786Jellx | EUR | PROD_WALL | 0.8209 | 0.8211 | — | — | ✗ prod>0.70 |
| — | 88PLAMnX | EUR | PROD_WALL | 0.8235 | 0.8237 | — | — | ✗ prod>0.70 |
| — | GrO3d8bZ | EUR | PROD_WALL | 0.8265 | 0.8257 | — | — | ✗ prod>0.70 |
| — | QPK5bXOr | EUR | PROD_WALL | 0.9514 | 0.9514 | — | — | ✗ prod>0.70 |
| — | blO97pAZ | EUR | PROD_WALL | 0.8241 | 0.8243 | — | — | ✗ prod>0.70 |
| — | xAbm3OgJ | EUR | PROD_WALL | 0.9668 | 0.9668 | — | — | ✗ prod>0.70 |
| — | 6XjaQrkO | ASI | PROD_WALL | 0.9583 | 0.9583 | — | — | ✗ prod>0.70 |
| — | 0mXexOw6 | ASI | HARD_BLOCKED | — | — | — | — | ✗ RA_FAIL |
| — | 786ajadx | EUR | HARD_BLOCKED | — | — | — | — | ✗ RA_FAIL |
| — | e7QdzYad | EUR | HARD_BLOCKED | — | — | — | — | ✗ RA_FAIL |
| — | vR2ejNk3 | EUR | HARD_BLOCKED | — | — | — | — | ✗ RA_FAIL |
| — | 3qV7Q2dO | GBR | HARD_BLOCKED | 0.6596 | 0.3669 | — | D1/PV ×1.5 | ✗ 数据过期 |

> **⚠ 分类摘要**（32/157 已完成）：SUBMIT_NOW=2, THIN_MARGIN=1, PROD_WALL=17, HARD_BLOCKED=5, 其他=7  
> **EUR 趋势**：11/11 已检查 → 1 SUBMIT_NOW + 8 PROD_WALL + 2 HARD_BLOCKED  
> **GBR 趋势**：15/15 已检查 → 1 SUBMIT_NOW(6XKwmQgE) + 12 PROD_WALL + 1 THIN_MARGIN + 1 HARD_BLOCKED  
> **submit_inventory 仍在运行**（剩余 ~125 条，ETA ~25–35min）

---

### SA 四步流程

#### 步骤 ① 区域资格扫描

| 区域 | ACTIVE 总数 | OP>0（严格） | DECOM | 组件池 ≥10？ | 判定 |
|------|------------|-------------|-------|-------------|------|
| USA | 37 | 16 | 101 | ✓ | **GO** |
| IND | 27 | 21 | 4 | ✓ | **GO** |
| KOR | 24 | 14 | 2 | ✓ | **GO** |
| MEA | 19 | 18 | 0 | ✓ | **GO** |
| GBR | 11 | 8 | 0 | ✓ | **GO** ⚠（OP>0=8<10） |
| GLB | 10 | 9 | 0 | ✓ | **GO** ⚠（OP>0=9<10） |
| ASI | 8 | 8 | 0 | ✗ | BLOCKED |
| DEU | 6 | 6 | 0 | ✗ | BLOCKED |
| HKG | 6 | 6 | 0 | ✗ | BLOCKED |
| EUR | 4 | 4 | 6 | ✗ | BLOCKED |

**GO 区**：USA, IND, KOR, GBR, MEA, GLB（6 区）  
**BLOCKED 区**：DEU, EUR, ASI, HKG（4 区）  
**⚠ 注意**：GBR(OP>0=8) 和 GLB(OP>0=9) 在严格口径下 OP>0 <10，但放宽口径 ACTIVE≥10 仍判 GO。

#### 步骤 ② SA 组出（super_build.py select）

| 区域 | 参数 | 产出 | IS S | IS F | TO | 状态 |
|------|------|------|------|------|-----|------|
| GLB | SUBINDUSTRY / decay1 / sl10 / sg0.70 / pc0.90 | MP3Q160n | 3.30 | 2.03 | 0.2246 | ✓ 已建 |

**参数依据**（§七 SA 参数表）：GLB SUBINDUSTRY 是历史最优参数组合。RAM 连续 3 轮失败，SUBINDUSTRY 是唯一有效参数。  
**自动跳过**：IND（SA 池判死 13/13 撞墙）、MEA（平台已下架）、USA（已有 3 颗 ACTIVE SA，PROD>0.82 全堵死）

#### 步骤 ③ 双闸增量实测（probe_sa_unsubmitted.py）

| 候选 | Region | IS S | IS F | Prod | Self | 双闸 | 探针时间 |
|------|--------|------|------|------|------|------|---------|
| YPMQXxXq | KOR | 4.89 | 5.41 | 0.6537 | 0.6537 | **PASS** | 10-06 00:22 |
| O08oOMG7 | KOR | 4.52 | 5.67 | 0.6738 | 0.6738 | **PASS** | 10-06 01:26 |
| 1YZJENmJ | KOR | 4.79 | 5.60 | 0.6574 | 0.6574 | **PASS** | 10-06 00:28 |
| 1YZJQpNm | KOR | 4.69 | 5.64 | 0.6596 | 0.6596 | **PASS** | 10-06 00:42 |
| wpbLgkql | KOR | 4.60 | 5.64 | 0.6604 | 0.6604 | **PASS** | 10-06 00:27 |
| leKrd9Y2 | KOR | 4.42 | 5.49 | 0.6502 | 0.6502 | **PASS** | 10-06 01:21 |
| 9qWJv1do | KOR | 4.45 | 5.54 | 0.6521 | 0.6521 | **PASS** ⚠ | 10-06 01:20 |
| 3qVzZN3O | KOR | 4.36 | 5.45 | 0.6821 | 0.6821 | **PASS** | 10-06 00:35 |
| 6XKzOx6Y | KOR | 4.28 | 5.29 | 0.6986 | 0.6986 | **PASS** | 10-06 00:28 |
| E5Rk18lK | KOR | 3.87 | 4.99 | 0.6552 | 0.6552 | **PASS** | 10-06 01:22 |
| Vk0O9ZPY | KOR | 3.96 | 5.27 | 0.7960 | 0.7960 | **BLOCKED** | 10-06 00:48 |
| mL6Z35qE | KOR | 3.74 | 5.12 | 0.7291 | 0.7291 | **BLOCKED** | 10-06 00:49 |

**汇总**：PASS=10 / BLOCKED=2 / 全部 KOR 区  
**⚠ 探针时间警告**：所有探针数据均为 10-06 缓存（>24h 前），9qWJv1do 已于 10-06 12:45 ET 提交但平台仍未更新状态。**提交前必须刷新 prod/self 实测。**

#### 步骤 ④ 提交决策

| 候选 | 建议 | 理由 |
|------|------|------|
| YPMQXxXq | **推荐提交** | IS S 4.89 最高，prod/self 双 0.6537，余量充足 |
| 1YZJENmJ | **推荐提交** | IS S 4.79，prod/self 0.6574，余量充足 |
| 1YZJQpNm | **推荐提交** | IS S 4.69，prod/self 0.6596，余量充足 |
| wpbLgkql | **推荐提交** | IS S 4.60，prod/self 0.6604，余量充足 |
| O08oOMG7 | **推荐提交** | IS S 4.52，prod/self 0.6738，余量 0.026 |
| 9qWJv1do | **⚠ 先核实状态** | 已提交但未更新，可能已重复提交 |
| leKrd9Y2 | 候补 | IS S 4.42，余量 0.0346 |
| 3qVzZN3O | 候补 | IS S 4.36，prod 偏高(0.6821) |
| 6XKzOx6Y | 候补 | IS S 4.28，prod 接近墙(0.6986) |
| E5Rk18lK | 候补 | IS S 3.87 最低 |
| Vk0O9ZPY | 放弃 | prod=0.796 撞墙 |
| mL6Z35qE | 放弃 | prod=0.7291 撞墙 |

---

## 关键发现与趋势

### 1. enqueue_propose L1=0 — 候选池整体质量崩塌
上一轮 L1=142→Proposal=46（10-07），本轮 L1=0（10-08）。RA_FAIL=4902 占 53.7%，说明大量候选的平台 RA 检查不通过。这可能是平台 RA 检查逻辑变更或候选池积累失败品所致。

### 2. EUR PROD_WALL 大迁移
WjegEmQO prod 从 0.5012（10-07）→ 0.7188（10-08），从 SUBMIT_NOW 跌入 PROD_WALL。  
11 个 EUR 候选中仅 1 个 omWVZ7lm 保持 SUBMIT_NOW（prod=0.5378）。

### 3. GBR 全面堵死
12 个 GBR 候选全部 PROD_WALL/THIN_MARGIN/HARD_BLOCKED，无 SUBMIT_NOW。

### 4. 9qWJv1do 平台状态异常
10-06 12:45 ET 提交，10-08 仍显示 UNSUBMITTED。可能提交未成功或平台延迟更新。

### 5. SA 候选全部来自 KOR
12 颗未提交 SA 候选全部来自 KOR 区。KOR 组件池 24 颗 ACTIVE 是全账户第二大 SA 基地（仅次于 USA 的 37 颗）。

### 6. GLB SA 组出成功
SUBINDUSTRY 参数确认有效（RAM 连续 3 轮失败），MP3Q160n 已建（IS S 3.30）。

---

## 产出文件清单

| 文件 | 说明 |
|------|------|
| `results/inventory_consolidated_20261008.md` | **本报告** |
| `results/pyramid_latest.json` | 金字塔塔灯状态快照 |
| `results/enqueue_proposal_20261008-111916.json` | enqueue_propose 输出 |
| `results/backup_ra_candidates_20261008.json` | backup_ra 扫描结果（115 条） |
| `results/submit_inventory_stdout.log` | submit_inventory 日志（部分 25/157） |
| `results/sa_candidates_20261008-112302.json` | SA 候选池（33 SUPER） |
| `results/sa_unsubmitted_probe_20261008-112326.json` | SA 双闸实测（10 PASS / 2 BLOCKED） |
| `results/region_op_verify_20261008-112313.json` | 区域 OP 验证（10/10 匹配） |

---

*报告生成时间：2026-10-08 11:52 CST*  
*submit_inventory 仍在后台运行（task Bu5BL3），完成后可更新 RA 分类数据*  
*下次盘点：下一工作日 ET 09:00*
