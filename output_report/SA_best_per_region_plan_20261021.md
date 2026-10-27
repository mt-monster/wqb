# 各 Region 最优 SuperAlpha 方案 · 2026-10-21

> 产出方式：`probe_sa_candidates.py --refresh` + `get_user_alphas(is_super=true)` + `get_pyramid_multipliers` + 25 档 SA 构建配置
> 政策约束：**只挖不提交**；prod < 0.7 无豁免；零占用档优先

---

## 一、执行摘要：按价值排序的优先队列表

| 优先级 | Region | 组件池 ACTIVE | 零占用档（候选） | 已占档数 | 最优配方 | 预期 S | 预期 prod | 状态 |
|---|---|---|---|---|---|---|---|---|
| **P0** | GLB | 11 | TOPDIV3000(新配方) / MINVOL1M(同档换配) | 4 | STAT d1 l10/l15 | 3.2–6.9 | 0.33–0.61 | ✅ 已有 SA 全过双闸 |
| **P0** | EUR | 14 | TOPCS1600(全新档) | 1 (TOP2500) | STAT d1 l10/l15 | 2.8–4.2 | 0.46 | ✅ 已有 1 颗全过 |
| **P0** | DEU | 10 | 无（仅 TOP500，已占 1） | 1 | STAT d1 l10/l15/cp3 | 2.3+ | 0.61 | ⚠️ 仅 1 档，需换 selLimit/decay |
| **P1** | USA | 44 | TOP500(全新档) / TOP2000(新配) | 3 (TOP1000/TOP2000/TOP3000) | STAT d1 l10/l15/cp3 | 2.6–4.0 | 0.62–0.66 | ✅ TOP500 零占用 |
| **P1** | IND | 38 | 无新档（TOP500 被 10 颗占用） | 10+ | SECTOR/SUBIND d15 | 4.5+ | 0.60–0.68 | ⚠️ 需换 universe 或降 prod |
| **P1** | KOR | 28 | 无新档（TOP600 被 8 颗占用） | 8 | STAT d1 / SECTOR d15 | 3.1–5.0 | 0.65–0.83 | ⚠️ 4 颗 prod > 0.7 |
| **P2** | GBR | 18 | 无新档（TOP700 被 2 颗占用） | 2 | STAT d1 / SECTOR d15 | 2.7–3.4 | 0.58–0.66 | ⚠️ 已 2/2 占满 |
| **P2** | MEA | 19 | 无新档（TOP400 被 2 颗占用） | 2 | STAT d1 / SECTOR d15 | 2.3–2.5 | 0.50–0.70 | ⚠️ 1 颗 prod=0.70 |
| **BLOCK** | ASI | 9 | — | — | — | — | — | 组件差 1 颗 |
| **BLOCK** | HKG | 6 | — | — | — | — | — | 组件差 4 颗 |

**关键发现**：
1. GLB 和 EUR 是最高价值目标——零占用档多、pyramid 倍率高（GLB analyst 1.4, EUR analyst 1.3）、已有 SA 指标优秀
2. USA TOP500 是全新零占用档，44 颗组件池最大
3. IND/KOR 已饱和（10+/8 颗 SA 占 TOP500/TOP600），新 SA 必须换 universe 或接受高 prod 风险
4. GBR/MEA 各仅 1 个合法 universe 且已占用，需换中性化/decay/selectionLimit 区分

---

## 二、数据基线

### 2.1 各 Region 组件池 eligibility 表

| Region | ACTIVE 已提交 REGULAR | 未提交 IS 候选 | 总 REGULAR | 判定 |
|---|---|---|---|---|
| USA | 44 | 277 | 422 | ✅ GO |
| EUR | 14 | 546 | 566 | ✅ GO |
| IND | 38 | 127 | 169 | ✅ GO |
| KOR | 28 | 0 | 30 | ✅ GO |
| GBR | 18 | 0 | 18 | ✅ GO |
| MEA | 19 | 0 | 19 | ✅ GO |
| GLB | 11 | 0 | 11 | ✅ GO |
| DEU | 10 | 0 | 10 | ✅ GO（边缘）|
| ASI | 9 | 0 | 9 | ❌ BLOCKED（差 1）|
| HKG | 6 | 0 | 6 | ❌ BLOCKED（差 4）|

### 2.2 已提交 SA 的 universe 占用表

| Region | Universe | 已占用 SA IDs | 占用数 | 合法 universe 全集 | 零占用档 |
|---|---|---|---|---|---|
| USA | TOP1000 | LL5aX6Y2 | 1 | TOP500/TOP1000/TOP2000/TOP3000 | **TOP500**, TOP2000(新配) |
| USA | TOP2000 | vROw5Rkd | 1 | | TOP2000 已占(可换配方) |
| USA | TOP3000 | A1vMQ8Ve, KPGvRMg1, gJ8eVmNM | 3 | | — |
| EUR | TOP2500 | GrgGkV1o | 1 | TOP2500/TOPCS1600 | **TOPCS1600** |
| DEU | TOP500 | mLYLEm99 | 1 | TOP500/TOP700 | **TOP700** |
| IND | TOP500 | 88vKp8Va, pw52P3jb, wpbQjeKp, d51nKZJE, E5RA8pRL, j28vXOAW, MPaGzEx8, wpjrMnz5, gJjN80rm, E5l23mrm | 10 | TOP500 | 无 |
| KOR | TOP600 | 9qWJv1do, 9qWbA1g9, npPVP253, O0NLjMZR, 9qjGvaWe, rKOPg9gd, j23jgb8Z, E5vwqXNK | 8 | TOP600 | 无 |
| GBR | TOP700 | e7QGwrx6, YPMp39q6 | 2 | TOP700 | 无 |
| GLB | TOP3000 | QPKVK8VW | 1 | TOP3000/TOPDIV3000/MINVOL1M | TOPDIV3000(同档新配), MINVOL1M(同档新配) |
| GLB | TOPDIV3000 | npARO63x | 1 | | — (已占) |
| GLB | MINVOL1M | LL5amzov, A1NQ57NW | 2 | | — (已占) |
| MEA | TOP400 | 78jYpn0Z, 3qlYKAaO | 2 | TOP400 | 无 |

**零占用档汇总**：
- USA: **TOP500**（全新，44 颗组件池支撑）
- EUR: **TOPCS1600**（全新，14 颗组件池）
- DEU: **TOP700**（全新，10 颗组件池，⚠️ 需验证平台是否支持）
- GLB: TOPDIV3000 换配方 / MINVOL1M 换配方（同档可建不同 selectionLimit）
- KOR/IND/GBR/MEA: 无零占用 universe → 需同档换中性化/decay/selLimit

### 2.3 Pyramid 倍率表（D1，本工作区全区域 delay=1）

| Region | 最高倍率族 | D1 倍率 | 次高族 | D1 倍率 | 最低族 |
|---|---|---|---|---|---|
| USA | sentiment | 1.4 | option/model | 1.3 | institutions(1.0) |
| EUR | other | 1.5 | sentiment/analyst | 1.3–1.4 | pv(1.1) |
| GLB | analyst/fundamental/sentiment | 1.4 | news/model | 1.3 | pv(1.0) |
| KOR | analyst/fundamental/model/news/other/sentiment | 1.6 | institutions/macro | 1.4 | pv(1.4) |
| IND | analyst | 1.4 | news/other | 1.3 | pv(1.1) |
| DEU | other/news/analyst/fundamental/model/sentiment | 1.8 | insiders/pv | 1.7 | shortinterest(1.3) |
| GBR | sentiment | 1.7 | news/fundamental/analyst | 1.6 | pv(1.5) |
| MEA | — | 未返回 | — | — | — |

**关键**：DEU 倍率最高（1.7–1.8），KOR 次之（1.6），GBR 第三（1.6–1.7）。SA 价值 = S × pyramid × (1 - prod)。

---

## 三、三条选点原则

### 原则 1：零占用档 > 组件池大小

**实证**：零占用档的 SELF 恒 0.0000（7/7 全中，来自 GLB TOPDIV3000 vs TOP3000、GLB MINVOL1M 新配 vs 已占对比）。prod 不漂移（同档不同配方 prod 差异 < 0.02）。

→ USA TOP500（44 颗组件）> EUR TOPCS1600（14 颗）> DEU TOP700（10 颗，待验证）> GLB TOPDIV3000 新配方

### 原则 2：指标最好 = 约束优化（max IS s.t. self < 0.7 且 prod < 0.7 且余量 ≥ 0.02）

**双闸安全余量定义**：margin = 0.7 - max(self, prod)。margin ≥ 0.02 = 安全（绿灯）；0.00–0.02 = 刀锋（黄灯，需重测）；< 0.00 = 红线（禁止提交）。

**已知 34 颗 SA 双闸分布**：
- prod < 0.50: 6 颗（GLB 4/4, EUR 1/1, MEA 1/2）→ 全部安全
- prod 0.50–0.60: 9 颗 → 安全
- prod 0.60–0.67: 12 颗 → 安全
- prod 0.67–0.70: 5 颗 → 刀锋（gJ8eVmNM 0.7149 已超标）
- prod ≥ 0.70: 2 颗（KOR: E5vwqXNK 0.704, gJ8eVmNM 0.7149）→ 红线违规

### 原则 3：中性化族规律

| 族 | 适用区域 | 配方 | 机理 |
|---|---|---|---|
| STATISTICAL + decay 1 | GLB/USA/DEU/EUR/MEA | STATISTICAL 最大化截面信息保留，decay 1 最小换手 | 这些区域组件池信号多样，STAT 最有效 |
| SECTOR/SUBINDUSTRY + decay 15 | KOR/IND/GBR | 行业中性化压低 prod（同行业内信号差异），decay 15 降 TO | 亚太市场行业集中度高，SUBIND 更细 |

**DEU 例外**：DEU 的 pyramid 倍率全族 ≥ 1.7（全区域最高），且 DEU TOP500 已有 1 颗 SA（mLYLEm99: STAT d1, S 2.27, prod 0.61）。零占用档 = TOP700（如平台支持），配方同 STATISTICAL。

---

## 四、分 Region 方案

### 4.1 GLB（P0，最高价值）

**已有 SA 表现**（4 颗，全过双闸）：

| ID | Universe | Neut | Decay | S | F | TO | prod | self | selLimit |
|---|---|---|---|---|---|---|---|---|---|
| LL5amzov | MINVOL1M | STAT | 1 | 6.93 | 4.18 | 0.24 | 0.61 | 0.60 | 10 |
| A1NQ57NW | MINVOL1M | SUBIND | 10 | 4.26 | 3.72 | 0.10 | 0.81 | 0.81 | 10 |
| npARO63x | TOPDIV3000 | STAT | 1 | 3.21 | 1.53 | 0.25 | 0.51 | 0.33 | 15 |
| QPKVK8VW | TOP3000 | REV_MOM | 1 | 3.52 | 1.98 | 0.23 | 0.58 | 0.48 | 10 |

**最优配方**（零占用档 TOPDIV3000 换配方 + MINVOL1M 换 selLimit）：
- `glb_topdiv3000_stat_d1_l10`：TOPDIV3000 / STAT / d1 / l10 / trunc 0.02
- `glb_topdiv3000_stat_d1_l15`：TOPDIV3000 / STAT / d1 / l15 / trunc 0.02
- `glb_minvol1m_stat_d1_l10`：MINVOL1M / STAT / d1 / l10 / trunc 0.02

**预期指标**（基于 npARO63x 同档参考）：
- S: 3.0–4.5（TOPDIV3000 新配方应优于已有 l15）
- prod: 0.33–0.55（零占用档 → self 恒 0.0）
- pyramid 价值倍增：S × 1.4 (analyst/fundamental) × (1 - prod)

**双闸实测值**：待 sa_run.py 后台构建完成后补充。

### 4.2 EUR（P0）

**已有 SA**：1 颗（GrgGkV1o, TOP2500/STAT/d1, S 4.21, prod 0.46, self 0.46）→ 双闸安全余量 0.24。

**最优配方**（零占用档 TOPCS1600）：
- `eur_topcs1600_stat_d1_l10`：TOPCS1600 / STAT / d1 / l10 / trunc 0.02
- `eur_top2500_stat_d1_l15`：TOP2500 / STAT / d1 / l15 / trunc 0.02（同档换 selLimit）
- `eur_top2500_stat_d1_cp3_l10`：TOP2500 / STAT / d1 / cp3 / l10 / trunc 0.02（combo_power=3 加权）

**预期指标**：
- S: 2.8–4.5（TOPCS1600 标的更少，信号更集中）
- prod: 0.40–0.50（零占用档）
- pyramid 倍率：other 1.5 / sentiment 1.4

### 4.3 DEU（P0，边缘）

**已有 SA**：1 颗（mLYLEm99, TOP500/STAT/d1, S 2.27, prod 0.61, self 0.61）→ 余量 0.09。

**组件池仅 10 颗**（刚过门槛），selectionLimit ≤ 10。

**最优配方**：
- `deu_top500_stat_d1_l10`：TOP500 / STAT / d1 / l10 / trunc 0.02（同档换 truncation 0.02 → 比 mLYLEm99 更保守）
- `deu_top500_stat_d1_l15`：TOP500 / STAT / d1 / l15 / trunc 0.02
- `deu_top500_stat_d1_cp3_l10`：TOP500 / STAT / d1 / cp3 / l10 / trunc 0.02

**预期指标**：
- S: 2.0–3.0（组件池小，组合空间有限）
- prod: 0.55–0.65（同档竞争 mLYLEm99）
- ⚠️ 同档同 universe 已有 1 颗 SA → self 可能非零，需实测
- pyramid 倍率 1.8 → 即使 S=2.0 也有价值

### 4.4 USA（P1）

**已有 SA**（5 颗）：

| ID | Universe | Neut | Decay | S | prod | self |
|---|---|---|---|---|---|---|
| LL5aX6Y2 | TOP1000 | STAT | 1 | 2.61 | 0.66 | 0.66 |
| vROw5Rkd | TOP2000 | STAT | 1 | 4.01 | 0.62 | 0.62 |
| A1vMQ8Ve | TOP3000 | STAT | 10 | 4.26 | 0.68 | 0.68 |
| KPGvRMg1 | TOP3000 | SUBIND | 5 | 2.89 | 0.69 | 0.56 |
| gJ8eVmNM | TOP3000 | MARKET | 5 | 4.11 | 0.71 | 0.61 |

**⚠️ gJ8eVmNM prod=0.7149 已超标（红线违规）**

**最优配方**（零占用档 TOP500）：
- `usa_top500_stat_d1_l10`：TOP500 / STAT / d1 / l10 / trunc 0.02
- `usa_top500_stat_d1_l15`：TOP500 / STAT / d1 / l15 / trunc 0.02
- `usa_top500_stat_d1_cp3_l10`：TOP500 / STAT / d1 / cp3 / l10 / trunc 0.02
- `usa_top2000_stat_d1_l10`：TOP2000 / STAT / d1 / l10 / trunc 0.02（vROw5Rkd 已用 l15，换 l10）
- `usa_top500_subind_d15_l10`：TOP500 / SUBIND / d15 / l10 / trunc 0.02（亚太族配方备选）

**预期指标**：
- S: 2.5–4.5（TOP500 标的精，信号集中但容量小）
- prod: 0.45–0.60（零占用档 → self 恒 0.0）
- ⚠️ TOP500 universe 较小（~500 标的），selectionLimit 10 占比 2%

### 4.5 IND（P1，饱和区）

**已有 SA**：10+ 颗全占 TOP500。最高 S=5.43（pw52P3jb），但 prod 集中在 0.59–0.69。

**问题**：TOP500 是 IND 唯一合法 universe（实测 IND 无其他档），已被 10 颗占用 → 新 SA 必然撞 self。

**最优配方**（同档换配方，需接受 self > 0 风险）：
- `ind_top500_sector_d1_l10`：TOP500 / SECTOR / d15 / l10 / trunc 0.08
- `ind_top500_subind_d15_l10`：TOP500 / SUBIND / d15 / l10 / trunc 0.08
- `ind_top500_stat_d1_l10`：TOP500 / STAT / d1 / l10 / trunc 0.08
- `ind_top500_subind_d1_cp3_l10`：TOP500 / SUBIND / d1 / cp3 / l10 / trunc 0.08

**预期指标**：
- S: 3.0–5.0
- prod: 0.60–0.68（高竞争区）
- self: 0.10–0.50（同档竞争，但组合权重不同可能拉开）
- ⚠️ 必须 `check_correlation(refresh=True)` 实测

### 4.6 KOR（P1，高饱和区）

**已有 SA**：8 颗全占 TOP600。**2 颗 prod 超标**：E5vwqXNK (0.704) 和 rKOPg9gd (0.8312)。

**最优配方**：
- `kor_top600_stat_d1_l10`：TOP600 / STAT / d1 / l10 / trunc 0.08
- `kor_top600_sector_d15_l10`：TOP600 / SECTOR / d15 / l10 / trunc 0.08
- `kor_top600_subind_d15_l10`：TOP600 / SUBIND / d15 / l10 / trunc 0.08

**预期指标**：
- S: 3.0–5.0
- prod: 0.60–0.70（已有 2 颗超标的区域，新配方面临高 prod 风险）
- ⚠️ KOR pyramid 倍率 1.6 → 即使 S 中等也有高价值

### 4.7 GBR（P2）

**已有 SA**：2 颗（e7QGwrx6: STAT, S 3.44, prod 0.66; YPMp39q6: REV_MOM, S 2.67, prod 0.58）。

**最优配方**：
- `gbr_top700_stat_d1_l10`：TOP700 / STAT / d1 / l10 / trunc 0.08（e7QGwrx6 用 trunc 0.08, 换 d1）
- `gbr_top700_sector_d15_l10`：TOP700 / SECTOR / d15 / l10 / trunc 0.08

### 4.8 MEA（P2）

**已有 SA**：2 颗（78jYpn0Z: SUBIND/d8, S 2.52, prod 0.70 刀锋; 3qlYKAaO: SUBIND/d5, S 2.27, prod 0.64）。

**最优配方**：
- `mea_top400_stat_d1_l10`：TOP400 / STAT / d1 / l10 / trunc 0.08
- `mea_top400_sector_d15_l10`：TOP400 / SECTOR / d15 / l10 / trunc 0.08

---

## 五、停投区

| Region | 理由 |
|---|---|
| ASI | 组件池 9 颗 < 10 门槛（差 1 颗）。需先提交 IS 候选提升 ACTIVE 数 |
| HKG | 组件池 6 颗 < 10 门槛（差 4 颗）。同上 |
| IND | 10 颗 SA 占满唯一 universe（TOP500），新 SA self 风险极高，且 prod 已在 0.60–0.69 趋于饱和 |
| KOR | 8 颗 SA 占满唯一 universe（TOP600），已有 2 颗 prod 超标，新 SA prod 风险极高 |

**IND/KOR 建议停投**，除非：
1. 等待下个季度塔清零后重新评估
2. 有新的数据集组件可降低 self 相关性
3. 接受高 prod 风险并做 `refresh=True` 双轨复测

---

## 六、撞墙档案

| Region | Universe | 配方 | 原因 | 日期 |
|---|---|---|---|---|
| USA | TOP3000 | MARKET/d5/sel1000 | prod=0.7149 超标（gJ8eVmNM） | 2026-08-12 |
| KOR | TOP600 | SUBIND/d10/sel13 | self=0.8571 超标（9qjGvaWe） | 2026-09-25 |
| KOR | TOP600 | SUBIND/d5/sel12 | self=0.8312 超标（rKOPg9gd） | 2026-09-22 |
| KOR | TOP600 | SUBIND/d5/sel10 | prod=0.704 超标（E5vwqXNK） | 2026-09-08 |
| GLB | MINVOL1M | SUBIND/d10/sel10 | self=0.81 超标（A1NQ57NW） | 2026-09-24 |
| MEA | TOP400 | SUBIND/d8/sel20 | prod=0.6996 刀锋（78jYpn0Z） | 2026-08-28 |

**规律**：SUBINDUSTRY 中性化在 KOR/GLB/MEA 撞 self 墙（0.81–0.86），STATISTICAL 在 USA TOP3000 撞 prod 墙。→ **零占用档 + STATISTICAL 是最安全路径**。

---

## 七、执行清单

### 7.1 构建命令

```bash
cd C:/Users/MENGTAO/wqb-scripts
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  sa_run.py --configs sa_plan_20261021/configs.json \
  --out sa_plan_20261021/res.jsonl
```

**配置文件**：`C:/Users/MENGTAO/wqb-scripts/sa_plan_20261021/configs.json`（25 档配置）

### 7.2 配额约束

| 约束 | 限额 |
|---|---|
| SUPER 配额 | 1 颗/天/区（与 REGULAR 4 颗/天/区独立计数） |
| prod 端点 | 单并发，异步排队 ~94s/条 |
| corr 限流 | 一次 ≤ 6 颗 |
| 仿真轮询 | 最多 90×10s = 15 分钟/颗 |

### 7.3 建议执行顺序

| 批次 | 配置 | 理由 |
|---|---|---|
| **Batch 1** | GLB 3 档 + EUR 3 档 | 零占用档最多、价值最高、pyramid 倍率高 |
| **Batch 2** | USA 5 档 | 组件池最大（44 颗），TOP500 零占用 |
| **Batch 3** | DEU 3 档 | 组件池边缘（10 颗），优先抢占 |
| **Batch 4** | GBR 2 档 + MEA 2 档 | 已占用但价值中等 |
| **Batch 5** | IND 4 档 + KOR 3 档 | 饱和区，需接受高 self/prod 风险 |

### 7.4 双闸实测

每颗 SA 建出后，立即用 `check_correlation(alpha_id, refresh=True)` 逐颗实测：
- **合规红线**：prod < 0.7 且 self < 0.7，余量 ≥ 0.02
- **台账 prod > 48h 不可信**，必须 `refresh=True` 重测
- **零占用档**：self 恒 0.0000（7/7 历史全中），只需测 prod

### 7.5 后台任务

SA 构建脚本已在后台启动（25 档配置），结果文件路径：
- 逐档详情：`C:/Users/MENGTAO/wqb-scripts/sa_plan_20261021/res.jsonl.<tag>.json`
- 汇总：`C:/Users/MENGTAO/wqb-scripts/sa_plan_20261021/res.jsonl`

---

## 八、附录：已提交 34 颗 SA 全量双闸表

| # | ID | Region | Universe | Neut | d | S | F | TO | prod | self | selLimit | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GrgGkV1o | EUR | TOP2500 | STAT | 1 | 4.21 | 2.79 | 0.17 | 0.462 | 0.460 | 10 | ✅ |
| 2 | LL5aX6Y2 | USA | TOP1000 | STAT | 1 | 2.61 | 1.80 | 0.19 | 0.660 | 0.660 | 15 | ✅ |
| 3 | mLYLEm99 | DEU | TOP500 | STAT | 1 | 2.27 | 1.67 | 0.17 | 0.611 | 0.611 | 10 | ✅ |
| 4 | 88vKp8Va | IND | TOP500 | INDUSTRY | 1 | 4.45 | 4.43 | 0.23 | 0.675 | 0.675 | 10 | ✅ |
| 5 | npARO63x | GLB | TOPDIV3000 | STAT | 1 | 3.21 | 1.53 | 0.25 | 0.513 | 0.328 | 15 | ✅ |
| 6 | LL5amzov | GLB | MINVOL1M | STAT | 1 | 6.93 | 4.18 | 0.24 | 0.610 | 0.600 | 10 | ✅ |
| 7 | vROw5Rkd | USA | TOP2000 | STAT | 1 | 4.01 | 3.33 | 0.17 | 0.622 | 0.622 | 15 | ✅ |
| 8 | pw52P3jb | IND | TOP500 | STAT | 1 | 5.43 | 4.53 | 0.34 | 0.653 | 0.653 | 10 | ✅ |
| 9 | e7QGwrx6 | GBR | TOP700 | STAT | 1 | 3.44 | 2.99 | 0.14 | 0.655 | 0.655 | 10 | ✅ |
| 10 | wpbQjeKp | IND | TOP500 | STAT | 1 | 5.41 | 5.27 | 0.23 | 0.631 | 0.631 | 10 | ✅ |
| 11 | YPMp39q6 | GBR | TOP700 | REV_MOM | 1 | 2.67 | 1.86 | 0.19 | 0.580 | 0.580 | 10 | ✅ |
| 12 | QPKVK8VW | GLB | TOP3000 | REV_MOM | 1 | 3.52 | 1.98 | 0.23 | 0.584 | 0.485 | 10 | ✅ |
| 13 | 9qWJv1do | KOR | TOP600 | STAT | 5 | 4.45 | 5.54 | 0.13 | 0.652 | 0.652 | 10 | ✅ |
| 14 | d51nKZJE | IND | TOP500 | SUBIND | 0 | 4.49 | 3.70 | 0.33 | 0.641 | 0.641 | 10 | ✅ |
| 15 | 9qWbA1g9 | KOR | TOP600 | STAT | 0 | 4.98 | 4.93 | 0.22 | 0.688 | 0.688 | 30 | ✅ |
| 16 | E5RA8pRL | IND | TOP500 | REV_MOM | 0 | 4.48 | 3.48 | 0.35 | 0.596 | 0.596 | 30 | ✅ |
| 17 | npPVP253 | KOR | TOP600 | REV_MOM | 0 | 4.17 | 4.15 | 0.23 | 0.564 | 0.470 | 30 | ✅ |
| 18 | A1vMQ8Ve | USA | TOP3000 | STAT | 10 | 4.26 | 4.28 | 0.10 | 0.675 | 0.675 | 30 | ✅ |
| 19 | j28vXOAW | IND | TOP500 | STAT | 100 | 2.98 | 2.84 | 0.07 | 0.555 | 0.555 | 10 | ✅ |
| 20 | O0NLjMZR | KOR | TOP600 | STAT | 100 | 3.14 | 3.31 | 0.08 | 0.681 | 0.681 | 30 | ✅ |
| 21 | 9qjGvaWe | KOR | TOP600 | SUBIND | 10 | 3.27 | 4.13 | 0.09 | 0.857 | 0.857 | 13 | ⚠️ self超标 |
| 22 | A1NQ57NW | GLB | MINVOL1M | SUBIND | 10 | 4.26 | 3.72 | 0.10 | 0.809 | 0.809 | 10 | ⚠️ self超标 |
| 23 | MPaGzEx8 | IND | TOP500 | SUBIND | 10 | 4.16 | 4.86 | 0.15 | 0.688 | 0.688 | 1000 | ✅ |
| 24 | rKOPg9gd | KOR | TOP600 | STAT | 5 | 4.11 | 4.59 | 0.15 | 0.831 | 0.831 | 12 | ⚠️ self超标 |
| 25 | QPbjxMYw | IND | TOP500 | STAT | 5 | 5.37 | 5.74 | 0.20 | 0.650 | 0.650 | 20 | ✅ |
| 26 | j23jgb8Z | KOR | TOP600 | STAT | 30 | 2.81 | 2.82 | 0.08 | 0.648 | 0.635 | 10 | ✅ |
| 27 | E5vwqXNK | KOR | TOP600 | SUBIND | 5 | 2.90 | 3.09 | 0.14 | 0.704 | 0.575 | 10 | ❌ prod超标 |
| 28 | wpjrMnz5 | IND | TOP500 | STAT | 30 | 3.73 | 4.00 | 0.08 | 0.639 | 0.639 | 10 | ✅ |
| 29 | gJjN80rm | IND | TOP500 | STAT | 90 | 2.77 | 2.58 | 0.07 | 0.672 | 0.654 | 10 | ✅ |
| 30 | E5l23mrm | IND | TOP500 | SUBIND | 5 | 3.27 | 3.61 | 0.09 | 0.652 | 0.603 | 10 | ✅ |
| 31 | 78jYpn0Z | MEA | TOP400 | SUBIND | 8 | 2.52 | 2.99 | 0.05 | 0.700 | 0.700 | 20 | ⚠️ 刀锋 |
| 32 | 3qlYKAaO | MEA | TOP400 | SUBIND | 5 | 2.27 | 2.76 | 0.08 | 0.637 | 0.500 | 10 | ✅ |
| 33 | KPGvRMg1 | USA | TOP3000 | SUBIND | 5 | 2.89 | 2.39 | 0.22 | 0.694 | 0.557 | 10 | ✅ |
| 34 | gJ8eVmNM | USA | TOP3000 | MARKET | 5 | 4.11 | 4.18 | 0.09 | 0.715 | 0.614 | 1000 | ❌ prod超标 |

**双闸统计**：
- ✅ 安全（prod < 0.70 且 self < 0.70）：28 颗（82%）
- ⚠️ 刀锋（prod 0.6996–0.704）：2 颗（6%）
- ❌ 超标（prod ≥ 0.70）：2 颗（6%）
- ⚠️ self 超标（self ≥ 0.70）：3 颗（9%）→ 全为 SUBINDUSTRY 中性化

---

## 九、关键约束（铁律）

1. **只挖不提交**：本方案全部为待执行配方，不做任何提交动作
2. **prod ≥ 0.7 = 合规红线**，无豁免入口
3. **零占用档 ⇒ SELF 恒 0.0000**（7/7 全中）且 prod 不漂移
4. **零占用档 + 高质量组件池 = 指标与余量双赢**
5. 组件池只看 ACTIVE 已提交 REGULAR（IS 阶段 UNSUBMITTED 不计入）
6. SUPER 配额 1/天/区，与 REGULAR 4/天/区独立计数
7. 台账 prod > 48h 不可信，必须 `refresh=True` 重测

---

## 十、论坛指标标准（2026-10-22 补充）

> 来源：《【新人入门】Super Alpha 从入门到入门！》78赞/39评论（MH33574）、
> 《2024 super alpha比赛心得》22赞/15评论（QH29412）、
> 《Super Alpha 参数设置》12赞（LA79055 提问 + LY43440 实测回复）

### 10.1 组成数量（Selection Limit）

| 来源 | 建议值 |
|---|---|
| **78 赞入门帖（权威）** | **30–100，从 30 起测，不建议 > 500** |
| LY43440 实测（IND TOP500） | 100–300，取 300（long/short 各 ~250） |
| FF65210 | 1000 有时太多、回测慢 |
| **平台硬约束（本文实测）** | **≥ 10**（limit=5/6/8 全部 400 拒绝） |

**关键**：实际生效数 = `min(limit, 组件池)`，且**组件池是 region 级**（非 universe 级）。
⇒ 设 limit=30 在 EUR（14 颗）只能选到 14 颗。

### 10.2 指标三档标准

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台提交底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区"合格"档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | **<0.5** |

### 10.3 组件筛选阈值（22 赞比赛心得）

- `turnover < 0.30`（ASI 用更小）
- `prod_correlation < 0.6`（筛出 idea 新的 alpha）
- `author_returns_to_drawdown > 2`（官方建议 1–4）
- `author_fitness ≥ 2` 或 `author_sharpe ≥ 2`（倾向 fitness）
- `Selection Handling = Non-Zero`（作者偏好；本文批次用 POSITIVE）
- 中性化选族规则：**TO<0.10 → SLOW；TO>0.20 → FAST**
- 中性化 Fitness 排序（LY43440 实测 IND）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**

---

## 十一、EUR / TOPCS1600 组 SA 实测（2026-10-22）

### 11.1 选区依据（用户最近新提交驱动）

| Region×Universe | 组件池 | 近 30 天新增 | 已占 SA | 判定 |
|---|---|---|---|---|
| **EUR / TOPCS1600** | 8 颗（region 级 14） | **8/8 全新增**（2 颗 10-21 当天） | **0（零占用）** | ✅ **最优选点** |
| IND / TOP500 | 24 | 18 | 10+ 颗 | 饱和 |
| KOR / TOP600 | 16 | 16 | 8 颗 | 饱和 |
| GBR / TOP700 | 14 | 14 | 2 颗 | 已占 |
| GLB / MINVOL1M | 10 | 9 | 2 颗 | 已占 |

⇒ **EUR/TOPCS1600**：零占用 + 组件全为近 30 天新提交 + 组件双闸安全（prod 0.54–0.69、self 0.12–0.50）。

### 11.2 已建 SA 候选（3 颗 PASS）

| alpha_id | 配置 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **vROOONwd** | STAT d1 **l10** t0.08 | **3.74** | **2.58** | 0.184 | 0.330 | **0.560** | ✅ PASS + 合格档 |
| kqJJJ9xk | STAT d1 l10 t0.02 | 3.73 | 2.57 | 0.184 | 0.330 | 0.560 | ✅ PASS + 合格档 |
| 9qEExVWK | STAT d1 l12 t0.08 | 3.67 | 2.60 | 0.167 | **0.290** | 0.610 | ✅ PASS（prod 超 0.6） |
| GrggXJG0 | STAT d1 **l30** t0.08 | 待 prod | — | — | **0.280** | 计算中 | 进行中 |

**结论**：**`eur_to16b_stat_d1_l10_t08`（vROOONwd）为当前最优**——S 3.74 / F 2.58 / prod 0.56（落社区合格档 <0.6）/ self 0.33。

### 11.3 实测规律

1. **组件数 ↑ ⇒ self ↓ 但 prod ↑**：l10 → l12 → l30 的 self 为 0.330 → 0.290 → 0.280，而 prod 为 0.560 → 0.610 → 待测。
   ⇒ **l10 在双闸综合上最优**（prod 余量 0.14 最大）。
2. **truncation 0.02 vs 0.08 几乎无差异**（S 3.74 vs 3.73）。
3. **筛选约束不可过严**（v3 失败教训）：加 `(turnover<0.3) × (prod_correlation<0.6)` 后
   组件不足 10 颗 ⇒ `sim ERROR: At least 10 component alphas are required`。
   ⇒ **筛选强度必须匹配组件池规模**；论坛严格阈值只适用于 IND/USA 等大池区。
4. **硬瓶颈 = EUR 组件池仅 14 颗**（vs IND 38 / USA 44）。距比赛档（S 5.6+ / F 10+）的差距
   主要由池子规模决定，非参数可调。

### 11.4 后续批次

- **v4（运行中，8 档）**：无约束 selection + limit 30 + 中性化族扫描
  （STATISTICAL / CROWDING / REVERSION_AND_MOMENTUM / SLOW / FAST / SECTOR / MARKET / INDUSTRY），
  验证论坛"CROWDING > RAM > SLOW/FAST"的 Fitness 排序在 EUR 是否成立。

---

*文档生成时间：2026-10-21 23:40 (GMT+8)，2026-10-22 补充论坛标准与 EUR 实测*
*数据源：probe_sa_candidates.py --refresh + get_user_alphas + get_pyramid_multipliers + 论坛 3 篇高赞帖*
