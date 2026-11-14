# SuperAlpha 各 Region 最优方案 · 2026-11-12

> 执行时间：2026-11-12 06:33 → 07:4x（GMT+8）｜ET 时间 **2026-11-11 18:0x**（`wqb.timeutil.et_now()`）
> 扫描口径：`probe_sa_candidates --refresh`（先清 `api_cache` 中 `user_alphas%` 77 条旧条目）
> 闸门口径：`check_correlation(correlation_type="both", refresh=True)` 逐颗实测
> **本轮未提交任何 alpha。提交权完全归用户（2026-11-11 用户明令撤销自动提交）。**

---

## 一、执行摘要

### 1.1 本轮产能结论

| 结论 | 内容 |
|---|---|
| 零 SUPER 空档 | **已无可用空档**。唯一候选 `ASI/TOP500` 本轮首建即判死（S1.61 / **F0.62** / TO0.3250）⇒ universe 错配压死 S 与 F |
| 新增可用候选 | **1 颗**：`leaq3P9l`（DEU/TOP500 SLOW d1，prod 0.5951 / self 0.5954，IS 8 项全 PASS） |
| 存量复测淘汰 | 5 颗（`A1VAAbWe` / `npvEEWO8` / `gJaJazPM` / 部分被同席替代） |
| 产能来源 | 100% 来自「已占档换异族」（DEU/TOP500、USA/TOP2000、USA/TOP1000） |
| ★★ **EUR 突破（08:2x 追加实证）** | 裁掉池内 7 颗低 TO 同族变体（`FAST d40/d80`，TO 0.016–0.069）后，EUR/TOP2500 SLOW 从 **S2.97 跃到 S6.91 / 6.54**，双闸 prod 0.5731 / 0.5670、self 0.3522 / 0.3487 ⇒ **EUR 从「停投」改为「本轮最优产能」，S 全仓第 2**。根因不是池小，是 `--turnover-min` 默认 0.01 把同族 decay 梯度全收进组合，把 N_eff 压到 2.04 |

### 1.2 优先队列（按 §5.5 字典序，非按绝对指标）

> ★ **本节已被 08:2x 的 EUR 突破刷新**：新第 1 顺位为 `E5Q7RGNR`（EUR/TOP2500 SLOW d2 + TO 过滤），详见 §6.5。

| # | Alpha | 档位 | 族 | S / F / TO | prod / self | 质量档 | 席位类型 |
|---|---|---|---|---|---|---|---|
| **1** | **`E5Q7RGNR`** | **EUR/TOP2500** | **SLOW d2 + TO>0.095** | **6.54 / 4.54 / 0.2263** | **0.5670 / 0.3487** | **B 档 + S 达 C 档** | 已占档异族（第 3 族） |
| **2** | **`MP6W3xnr`** | **EUR/TOP2500** | **SLOW d1 + TO>0.095** | **6.91 / 4.40 / 0.2851** | **0.5731 / 0.3522** | **B 档 + S 达 C 档** | 与 #1 **同族**，二选一 |
| 3 | `leaq3P9l` | DEU/TOP500 | SLOW d1 | 2.60 / 2.11 / 0.1608 | **0.5951 / 0.5954** | **B 档** | 已占档异族（第 3 族） |
| 4 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 / 2.38 / 0.1341 | 0.6011 / 0.6011 | A 档 | 已占档异族（第 2 族） |
| 5 | `e75avmq6` | USA/TOP2000 | SLOW d1 | **4.29 / 4.00** / 0.1034 | 0.6373 / 0.4871 | A 档 | 已占档异族（第 2 族） |
| 6 | `2r5rA775` | DEU/TOP500 | CROWDING d1 | 3.00 / 3.15 / 0.1340 | 0.6434 / 0.6436 | A 档 | 已占档异族（与 #3 同档互斥） |
| 7 | `Xg9WNRg8` | USA/TOP2000 | SLOW d1 | **4.74 / 4.10** / 0.1659 | 0.6493 / 0.6493 | A 档 | 与 #5 **同族**，二选一 |

> 口径冲突已消解：`E5Q7RGNR` 同时满足「③ B 档双达标（TO<0.30 ∧ prod<0.60）」与「⑥ Eff 最高（7.86）」两个条件，字典序与质量口径**首次收敛**，§5.4 的张力仅对 #3–#7 仍然存在。

> ⚠ **排序口径说明（务必先读 §5.4「规则张力」）**：本表严格按任务 §5.5 的字典序（③ B 档双达标 优先于 ④ prod 余量、⑤ U）产出。
> 若目标改为「OS Sharpe / Fitness 最大化」，则 `Xg9WNRg8`（Eff 4.26）与 `e75avmq6`（Eff 3.63）显著优于 #1、#2，**两者不可兼得，取舍见 §10.2**。

---

## 二、数据基线（2026-11-12 06:35 刷新）

### 2.1 组件池 eligibility（硬前置 ≥10 颗 ACTIVE REGULAR）

| 区域 | ACTIVE 已提交 REGULAR | IS 未提交 | 总 REGULAR | verdict | μ̄（IS Sharpe 均值） |
|---|---|---|---|---|---|
| USA | 47 | 0 | 148 | GO | 1.9757 |
| IND | 47 | 0 | 51 | GO | 2.7302 |
| KOR | 35 | 0 | 37 | GO | 1.8586 |
| GBR | 28 | 0 | 28 | GO | 1.9064 |
| EUR | 27 | 72 | 105 | GO（但 prod 墙） | 2.0811 |
| MEA | 19 | 0 | 19 | GO（平台已下架，不可建） | 1.8847 |
| GLB | 19 | 0 | 19 | GO | 3.0321 |
| DEU | 18 | 878 | 896 | GO | 1.8356 |
| ASI | **10** | 0 | 10 | GO（刚好卡线） | 2.3080 |
| HKG | 7 | 0 | 7 | **BLOCKED（差 3）** | 1.9757 |

对比 11-11：池 254 → **257**（+3），SUPER ACTIVE **52 → 53**（唯一增量 = `QPv88bJW`，本账户 11-10 提交）。
**关键变化**：ASI 池 10（仍刚好卡线，无新增）；DEU 18（持平）；USA 47（持平）⇒ 本轮无「池增长带来新产能」的红利，产能全部来自异族换族。

### 2.2 档位占用表（平台档位 × SUPER）

| 区域 | Universe | REGULAR | SUPER | 状态 | 已占 SUPER（族 / decay） |
|---|---|---|---|---|---|
| USA | TOP3000 | 38 | 6 | OCCUPIED | STAT d10、SUBIND d5、MARKET d5、FAST d1、SLOW d1×2 |
| USA | TOP2000 | 5 | 1 | OCCUPIED | vROw5Rkd（STAT d1） |
| USA | TOP1000 | 0 | 1 | OCCUPIED | LL5aX6Y2（STAT d1） |
| USA | TOP500 | 0 | 1 | OCCUPIED | E567rQvR（CROWDING d1） |
| USA | TOPSP500 | 0 | 1 | OCCUPIED | 2rj3ddl5（STAT d1） |
| USA | TOP200 | 0 | 0 | ZERO_OS | —（历史判死：S 0.95–1.28） |
| IND | TOP500 | 47 | **12** | OCCUPIED | 全族饱和（STAT 6 / SUBIND 3 / RAM 1 / INDUSTRY 1 / SLOW 1） |
| KOR | TOP600 | 35 | **11** | OCCUPIED | STAT 6 / SUBIND 2 / RAM 1 / CROWD 1 / SLOW 1 |
| GBR | TOP700 | 28 | **6** | OCCUPIED（≥5 换族失效） | STAT×3 / RAM / FAST / SLOW |
| EUR | TOP2500 | 17 | 2 | OCCUPIED | STAT d1、CROWDING d1 |
| EUR | TOPCS1600 | 10 | 1 | OCCUPIED | STAT d1 |
| EUR | TOP1200 / TOP800 / TOP400 | 0 | 0 | ZERO_OS | —（结构性 prod 墙，5 次复现） |
| GLB | MINVOL1M | 18 | 2 | OCCUPIED | SUBIND d10、STAT d1 |
| GLB | MINVOL10M | 0 | 1 | OCCUPIED | LLMVPag1（SLOW d1） |
| GLB | TOP3000 | 0 | 1 | OCCUPIED | QPKVK8VW（RAM d1） |
| GLB | TOPDIV3000 | 1 | 1 | OCCUPIED | npARO63x（STAT d1） |
| DEU | TOP500 | 18 | **2** | OCCUPIED（可换族） | mLYLEm99（STAT d1）、vR1oxZA3（FAST d1） |
| ASI | MINVOL1M | 7 | 1 | OCCUPIED | d5WGG5bg（STAT d2） |
| ASI | MINVOL10M | 3 | 1 | OCCUPIED | QPv88bJW（COUNTRY d3） |
| ASI | TOP500 | 0 | 0 | ZERO_OS | —（本轮首建判死） |
| HKG | TOP800 | 7 | 0 | ZERO_SA | 池 7/10，BLOCKED |
| HKG | TOP500 / CHN / AMR | 0 | 0 | ZERO_OS | 池 0，不可建 |
| MEA | TOP400 | 19 | 2 | NON_PLATFORM | 平台已下架 |

### 2.3 Pyramid 倍率（D1 口径；**SA 不参与塔计数，仅供参考**）

| 区域 | D1 最高类别 | D1 最低 | 备注 |
|---|---|---|---|
| DEU | fundamental/analyst/news/other/sentiment **1.8** | shortinterest 1.3 | 全账户最高档 |
| GBR | sentiment 1.7 / news·other·analyst 1.6 | imbalance 1.0 | |
| EUR | other 1.5 / news·sentiment 1.4 | risk·imbalance 1.0 | |
| ASI | analyst 1.5 / other·sentiment 1.4 | pv·insiders·risk·imbalance·macro 1.0 | |
| USA | other·sentiment 1.4 | institutions·imbalance 1.0 | |
| GLB | fundamental·analyst 1.4 | pv·risk·institutions 1.0 | |

> §0.8：SUPER 的 `is.checks` 无 `MATCHES_PYRAMID` ⇒ SA 不进入 pyramid 计数，塔倍率不作为选点理由（仅记录）。

---

## 三、选点原则（本轮执行顺序）

1. **席位类型 > 同族/异族 > 边际指标 > 绝对指标**
2. 零 SUPER 档 = 最高优先（本轮两个候选：ASI/TOP500 已判死、USA/TOP200 = 历史判死，故本轮无零 SUPER 产能）
3. 已占档：档内 SUPER < 5 才建异族；同族（只改 limit/decay/truncation）预期 self>0.9，直接跳过
4. **prod ≥ 0.68 = 出局**（本方案自设余量闸，比平台 0.7 严 0.02；`npvEEWO8` 0.6817、`gJaJazPM` 0.6850 即被此闸拦下）
5. IS checks 零 FAIL，且 `LOW_FITNESS` 必须真 PASS（F ≥ 1.0，不能靠 WARNING 混过）

---

## 四、论坛指标标准（§0 固化，无需每轮重研）

### 4.1 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.60** |
| C 比赛/优秀档 | 5.6–7.0 | 5.6–8.9 | 0.20–0.27 | <0.5 |

本轮唯一 B 档 = `leaq3P9l`；无 C 档候选（账户历史 C 档仅 `A1V0eZne` S6.39/F7.06）。

### 4.2 组件筛选阈值（论坛原文）

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。

**本仓适用性**：`author_*` 是作者级聚合量 ⇒ 自有池内恒为常数（11-06 实证），阈值不可消费；且小池区（EUR/GLB/DEU/ASI）加严后组件 <10 会直接 `sim ERROR: At least 10 component alphas are required`。故本轮统一使用宽松 selection 模板：

```
(1 + 0 * (prod_correlation > 0)) * (1.0 - prod_correlation) *
(self_correlation < 0.7) * (turnover > 0.01) * (turnover < 0.6)
```

⚠ `(prod_correlation>0)` 前的 `1 + 0 * (...)` 是 USA 区 pydantic 强校验的必需包装（否则抛 ValidationError，日志无 `[error]` 行）。

### 4.3 中性化族规律（逐区实测，不可跨区照搬）

- DEU/TOP500 族谱（本轮补全）：**INDUSTRY 3.14 / CROWDING 3.00 / SLOW 2.60**（S），但 prod：**SLOW 0.5951 < CROWDING 0.6434 < INDUSTRY 0.7412(FAIL)** ⇒ 族越粗 S 越高、prod 越脏，与 11-09 结论一致。
- USA/TOP2000 族谱（本轮补全）：SLOW 4.29（prod 0.6373）≫ SECTOR 2.33（0.7656）> CROWDING 2.17（0.7775）⇒ **USA 窄档只有 SLOW 干净**。
- USA/TOP1000：CROWDING 2.61（0.6011）> SLOW 1.63（F 0.85 直接 FAIL）。

---

## 五、★ 边际收益排序（§0.6 五量，逐颗可复算）

### 5.1 口径

`μ̄` = 该区 ACTIVE 已提交 REGULAR 的 IS Sharpe 均值｜`N = min(selectionLimit, 池)`

| 量 | 公式 | 本轮取值 |
|---|---|---|
| `U` | `S/(μ̄·√N)` | USA: μ̄=1.9757, N=10 → 分母 6.2475｜DEU: 1.8356 → 5.8052｜GLB: 3.0321 → 9.5883｜ASI: 2.3080 → 7.2980 |
| `N_eff` | `(S/μ̄)²` | — |
| `ρ_eff` | `(N·μ̄²/S² − 1)/(N−1)` | 等权反解 |
| `Eff` | `(S−μ̄)/max(prod,self)` | 每单位拥挤度换到的 Sharpe 溢价 |
| `ΔCAP%` | `√(52/(1+51ρ))/√(51/(1+50ρ)) −1` | ρ=max(prod,self) |

### 5.2 全量表（5 颗过闸候选）

| # | Alpha | 区域/档 | 族 | S | F | TO | prod | self | **U** | N_eff | ρ_eff | **Eff** | ΔCAP% | B档 | prod 余量 | 双闸实测 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `leaq3P9l` | DEU/TOP500 | SLOW d1 | 2.60 | 2.11 | 0.1608 | 0.5951 | 0.5954 | 0.448 | 2.01 | 0.443 | 1.28 | +0.013% | **Y** | 0.0849 | 11-12 07:1x |
| 2 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 | 2.38 | 0.1341 | 0.6011 | 0.6011 | 0.418 | 1.75 | 0.526 | 1.05 | +0.012% | - | 0.0789 | 11-12 07:0x |
| 3 | `e75avmq6` | USA/TOP2000 | SLOW d1 | 4.29 | 4.00 | 0.1034 | 0.6373 | 0.4871 | 0.687 | 4.72 | 0.125 | **3.63** | +0.011% | - | 0.0427 | 11-12 06:5x |
| 4 | `2r5rA775` | DEU/TOP500 | CROWDING d1 | 3.00 | 3.15 | 0.1340 | 0.6434 | 0.6436 | 0.517 | 2.67 | 0.305 | 1.81 | +0.010% | - | 0.0366 | 11-12 06:5x |
| 5 | `Xg9WNRg8` | USA/TOP2000 | SLOW d1 | 4.74 | 4.10 | 0.1659 | 0.6493 | 0.6493 | **0.759** | 5.76 | 0.082 | **4.26** | +0.010% | - | 0.0307 | 11-12 07:0x |

### 5.3 未过闸（进不了排序表，但必须留档）

| Alpha | 档 | 族 | S/F/TO | prod | 否决原因 |
|---|---|---|---|---|---|
| `npvEEWO8` | ASI/MINVOL1M | SECTOR d3 | 4.30/3.12/0.2455 | **0.6817** | 超 0.68 余量闸（差 0.0017）；self 0.6593 |
| `gJaJazPM` | GLB/MINVOL10M | STAT d1 | 3.97/1.78/0.2736 | **0.6850** | 超 0.68 余量闸（平台 0.7 可过，本方案拒交） |
| `A1VAAbWe` | ASI/MINVOL1M | COUNTRY d3 | 4.60/3.33/0.2458 | **0.7275** | **prod FAIL**（11-11 时测 0.6634，`QPv88bJW` 提交后 +0.064） |
| `vRAqNV9b` | USA/TOP2000 | CROWDING d1 | 2.17/1.79/0.1831 | 0.7775 | prod FAIL（本轮新建） |
| `E5Q7GKg0` | USA/TOP2000 | SECTOR d1 | 2.33/1.98/0.1854 | 0.7656 | prod FAIL（本轮新建） |
| `qM71NjZO` | DEU/TOP500 | INDUSTRY d1 | 3.14/3.63/0.1296 | 0.7412 | prod FAIL（本轮新建；F 3.63 全轮最高但 prod 最脏） |
| `mLa3VnW5` | ASI/TOP500 | STAT d2 | 1.61/**0.62**/0.3250 | — | IS：F<1.0 + TO>0.30（本轮新建，零 SUPER 档首探即死） |
| `vRAqNaxa` | USA/TOP1000 | SLOW d1 | 1.63/**0.85**/0.2600 | — | IS：F<1.0 |

### 5.4 ⚠ 规则张力（必须让用户看到）

任务 §5.5 的字典序把「③ B 档双达标」排在「④ prod 余量大 / ⑤ U / ⑥ Eff」之前。本轮后果：

- **`leaq3P9l` 之所以是 #1，唯一原因是它是全场唯一 B 档**（TO 0.1608 + prod 0.5951）。它的 S 2.60 / F 2.11 是 5 颗里最低。
- **`Xg9WNRg8` / `e75avmq6` 在绝对指标上碾压**：S +1.6~+2.1、F +1.7~+2.0、Eff 2.8~3.3 倍，且 prod 仍 <0.7（0.6493 / 0.6373）。但它们 prod >0.60 ⇒ 落不进 B 档。
- §0.6.1-4 明写「真正有区分力的只有 **Eff**、席位类型、同族/异族」——若按这句执行，`Xg9WNRg8` 与 `e75avmq6` 应排在前面。

**两条口径我都给出，不擅自合并**：本表按任务 §5.5 原文排序（#1 = `leaq3P9l`）；§10.2 另给「Eff 优先」口径下的首选。**最终取谁由用户定。**

---

## 六、分 Region 方案

### 6.1 DEU / TOP500 —— 本轮唯一新增产能（首选区）

| 项 | 内容 |
|---|---|
| 已有 SUPER | 2 颗：`mLYLEm99`(STAT d1, S2.27)、`vR1oxZA3`(FAST d1, S3.27) |
| 档内余量 | 3 个未被占的族可用（CROWDING / SLOW / INDUSTRY） |
| 最优配方 | **SLOW d1 l10 trunc 0.08**（`leaq3P9l`）／**CROWDING d1 l10**（`2r5rA775`） |
| 预期指标 | S 2.60–3.00 / F 2.11–3.15 / TO 0.134–0.161 |
| 双闸实测 | SLOW 0.5951/0.5954｜CROWDING 0.6434/0.6436（均 11-12 实测） |
| 余量 | SLOW 0.0849/0.0846｜CROWDING 0.0366/0.0364 |
| **互斥关系** | 两颗同档**只能交 1 颗**；交任一颗后另一颗 self 会跳升（同区新 ACTIVE 顶高邻近候选，11-12 `A1VAAbWe` 已实证 +0.064） |
| 弃用族 | INDUSTRY（prod 0.7412 FAIL）、SECTOR（历史 0.7701）、MARKET（历史 0.7708） |

### 6.2 USA / TOP2000 —— 绝对指标最强（次选区）

| 项 | 内容 |
|---|---|
| 已有 SUPER | 1 颗：`vROw5Rkd`(STAT d1, S4.01) |
| 最优配方 | **SLOW d1 l10**，两个历史件：`Xg9WNRg8`（trunc 0.02，第 2 批池）/ `e75avmq6`（trunc 0.02，第 1 批池） |
| 双闸实测 | Xg9WNRg8 0.6493/0.6493（top1=vROw5Rkd 0.6493）｜e75avmq6 0.6373/0.4871（top1=O08EjLVp 0.4871，**非本档 SUPER**） |
| 关键差异 | `e75avmq6` 的 self 来源是跨档的 `O08EjLVp`，与本档 SUPER 仅 0.2956 ⇒ 若先交 `e75avmq6`，`Xg9WNRg8` 会被顶死；反之亦然 |
| 弃用族 | CROWDING（0.7775 FAIL）、SECTOR（0.7656 FAIL） |

### 6.3 USA / TOP1000 —— prod 最干净（保守备选）

| 项 | 内容 |
|---|---|
| 已有 SUPER | 1 颗：`LL5aX6Y2`(STAT d1, S2.61) |
| 最优配方 | **CROWDING d1 l10**（`1YNl3p5R`，本轮复测 0.6011/0.6011，与 11-07 逐位一致） |
| 短板 | self ≡ prod ≡ 0.6011（pool_size=1，全部来自 `LL5aX6Y2`）⇒ **这是「同档换族的极限值」**，难以下压 |
| 弃用族 | SLOW（`vRAqNaxa` F 0.85 FAIL） |

### 6.4 ASI —— 从「唯一新增产能」退回「饱和」

| 项 | 内容 |
|---|---|
| 现状 | 2 颗 SUPER：`d5WGG5bg`(MINVOL1M STAT d2)、`QPv88bJW`(MINVOL10M COUNTRY d3)；池刚好 10 |
| 本轮首探零 SUPER 档 | **ASI/TOP500 STAT d2 → `mLa3VnW5` S1.61 / F0.62 / TO0.3250 判死**（universe 错配：10 颗成分 7 在 MINVOL1M、3 在 MINVOL10M） |
| 存量复测 | `A1VAAbWe` prod 0.6634→**0.7275 FAIL**（被 `QPv88bJW` 毒化）；`npvEEWO8` 0.6593→**0.6817 超闸** |
| 结论 | **ASI 全域停投**。`QPv88bJW` 提交后同区 COUNTRY/SECTOR 族被顶高 0.06，MINVOL10M 的 SLOW/STAT 未试但同区 prod 基数已抬升 |

### 6.5 ★★★ EUR / TOP2500 —— 08:2x 追加实证：从「停投」翻转为「本轮最优」（S 6.91，全仓第 2）

**触发**：用户追问「EUR 组不出高质量 SA？」。原方案把 EUR 列为停投（已有 3 颗、池 27 颗、换族 S 掉到 1.4–2.2）。

**实验链（同一档 TOP2500/SLOW/d1，只改 selection 的 turnover 下限）**：

| 变体 | turnover_min | ID | S | F | TO | 结论 |
|---|---|---|---|---|---|---|
| 默认模板（原方案口径） | 0.01 | `pwaX5Vrg` | 2.97 | 1.96 | 0.1175 | 只是「够格」，弱于已有 `GrgGkV1o`(4.21) |
| 打分加 sharpe 权重 | `*sharpe` | — | — | — | — | ❌ 平台 400：`Attempted to use unknown variable "sharpe"` |
| **裁掉低 TO 变体** | **0.095** | **`MP6W3xnr`** | **6.91** | **4.40** | 0.2851 | ✅ **EUR 史上最高 S，全仓第 2** |
| 同上 + decay 2（稳健性） | 0.095 | **`E5Q7RGNR`** | **6.54** | **4.54** | **0.2263** | ✅ 稳健，非单点过拟合 |

**根因（不是池小，是池被污染）**：EUR 池 27 颗里有 **7 颗 `FAST d40/d80` 低 TO 变体**（TO 0.016–0.069，S 仅 1.64–2.23），它们是同一信号族按 decay 拉长的产物、彼此高度相关。默认 `--turnover-min 0.01` 把它们全收进组合（selection 打分 `1−prod_correlation` 不惩罚低 TO），于是「一个信号占了 7 席」：

| 指标 | 默认（27 颗全收） | TO>0.095（恰好 10 颗） | 变化 |
|---|---|---|---|
| 入选池 μ̄ | 2.081 | **2.471** | +18.7% |
| 组合 S | 2.97 | **6.91** | **+133%** |
| `N_eff` = (S/μ̄)² | 2.04 | **7.82**（按入选池 μ̄）/ 11.0（按全区 μ̄） | ×3.8 |
| `ρ_eff` | 0.371 | **0.279** / −0.010 | 显著下降 |

⇒ S 的跃升 **只有 19% 来自均值提升，81% 来自分散度修复**（同族变体被裁）。这是教科书级的 `N_eff` 修复案例。

**TO>0.095 的 10 颗入选组件**（μ̄ 2.471）：`0mY1QPEv`(CROWDING,3.76) `LLM5eAMn`(FAST,3.48) `O0AJ3NEd`(FAST,2.91) `O0W0w3P7`(MARKET,2.72) `LL5VwgO1`(SUBIND,2.64) `9qlZLVNd`(MARKET,2.04) `88vQz5Yl`(INDUSTRY,1.84) `gJj1nxLM`(SUBIND,1.81) `Xgojww1X`(INDUSTRY,1.80) `786pLKnb`(SUBIND,1.71) —— 族分布覆盖 5 族，真正异质。

**双闸实测（refresh=True，2026-11-12 08:2x）**：

| ID | S / F / TO | returns / DD | prod（余量） | self（余量） | 最近邻 | IS checks |
|---|---|---|---|---|---|---|
| **`E5Q7RGNR`** | **6.54 / 4.54 / 0.2263** | 11.0% / **0.62%** | **0.5670（0.1130）** | **0.3487（0.3213）** | `GrgGkV1o` 0.349 | 8 项全 PASS |
| `MP6W3xnr` | 6.91 / 4.40 / 0.2851 | 11.6% / 0.68% | 0.5731（0.1069） | 0.3522（0.3178） | `GrgGkV1o` 0.352 | 8 项全 PASS |
| （对照）`pwaX5Vrg` | 2.97 / 1.96 / 0.1175 | 5.5% / 1.55% | 0.6714（0.0086） | 0.6717（0.0083） | `GrgGkV1o` 0.672 | 0 FAIL |

> 两颗 EUR 新件的 prod 与 self **双双降到 0.57 / 0.35**，余量是原方案全部候选（余量 0.007–0.085）的 **2–15 倍**。低 TO 变体被裁后，组合既更分散、也更不拥挤 —— 两个维度同时改善，这与「分散度↑ ⇒ prod↑」的常见权衡相反（因为被裁的正是 prod 也不低的同族件）。

**为什么只有 EUR 受益（跨区对照）**：

| 区 | 池 | μ̄（全池） | 最佳 TO 阈值 | μ̄（该阈值） | 增益 |
|---|---|---|---|---|---|
| **EUR** | 27 | 2.081 | **>0.095**（剩 10） | **2.471** | **+18.7%** |
| USA | 47 | 1.976 | >0.05（剩 27） | 2.190 | +10.8%（但 >0.095 反落到 2.009） |
| IND | 47 | 2.730 | >0.12（剩 40） | 2.882 | +5.6% |
| GBR | 28 | 1.906 | >0.12（剩 19） | 1.917 | +0.6% |
| KOR | 35 | 1.859 | >0.12（剩 22） | 1.890 | +1.7% |
| DEU | 18 | 1.836 | >0.12（剩 12） | 1.903 | +3.6% |
| GLB | 19 | 3.032 | 无（全 TO>0.095） | — | — |

⇒ EUR 的池污染是**独家**的（7 颗 d40/d80 FAST 变体集中在 EUR），其他区无此结构。

**⚠ 唯一天然限制**：`EUR/TOPCS1600` 池仅 10 颗，TO>0.05 只剩 7 颗 ⇒ **该 universe 无法用同法**（会 400 `At least 10 component alphas are required`）。TO 过滤只在 `TOP2500`（17 颗基数）可用。

### 6.6 GLB / GBR / IND / KOR / DEU / MEA / HKG —— 停投

见 §七。

---

## 七、停投区与撞墙档案

### 7.1 停投（本轮再次确认）

| 区域/档 | 原因 | 证据 |
|---|---|---|
| ~~EUR 全域~~ → **仅 TOP1200/800/400 停投** | **08:2x 撤销主档停投**：TOP2500 用 TO>0.095 过滤后出 S6.91/6.54 | 见 §6.5；残留三零档 prod 0.7117–0.7783 仍未破 |
| IND / TOP500 | 12 颗 SUPER，全族饱和 | 池 47 但档内 ≥5 后换族失效 |
| KOR / TOP600 | 11 颗 SUPER | 同上 |
| GBR / TOP700 | 6 颗 SUPER | 档内 ≥5 |
| USA / TOP3000 | 6 颗 SUPER | 同上 |
| USA / TOP200 | 零 SUPER 但 S 天花板 1.28 | 10-25/11-08 两次复现 |
| GLB 全部 4 档 | 全占用（5 颗 SUPER） | MINVOL1M 2 / MINVOL10M 1 / TOP3000 1 / TOPDIV3000 1 |
| ASI 全域 | 本轮新判（见 6.4） | `A1VAAbWe` / `npvEEWO8` 被顶高 |
| HKG | 池 7/10 BLOCKED | 需先交 3 颗 REGULAR |
| MEA | 平台下架（400 `Region MEA is not available.`） | 历史 2 颗仍 ACTIVE 但不可新建 |
| CHN / AMR | 池 0 | 不可建 |

### 7.2 本轮新增撞墙档案

| 条目 | 值 | 性质 |
|---|---|---|
| `mLa3VnW5` ASI/TOP500 STAT d2 | S1.61 / **F0.62** / TO 0.3250 | **universe 错配压死 F** — 与 `QPv88bJW`（MINVOL10M 错配仍得 F2.55）不同：TOP500 成分覆盖更差，S 直接掉到 1.61 |
| `qM71NjZO` DEU/TOP500 INDUSTRY d1 | S3.14 / **F3.63** / prod **0.7412** | **族越粗 F 越高、prod 越脏**的极端样本；F 3.63 为全轮最高但直接 FAIL |
| `vRAqNV9b` / `E5Q7GKg0` USA/TOP2000 CROWDING/SECTOR | prod 0.7775 / 0.7656 | USA 窄档只有 SLOW 族能压 prod |
| `vRAqNaxa` USA/TOP1000 SLOW | F0.85（<1.0） | 同区 CROWDING 2.61 vs SLOW 1.63，族不可换 |
| `A1VAAbWe` ASI COUNTRY d3 | prod 0.6634 → **0.7275** | **同区新 ACTIVE 顶高邻近候选 +0.064** 的硬证据（`QPv88bJW` 11-10 提交） |
| `gJaJazPM` GLB/MINVOL10M STAT | prod 0.6850（与 11-11 逐位一致） | 0.68 余量闸第 2 次拦下平台可过候选 |

---

## 八、执行清单（构建命令 + 配额约束）

### 8.1 本轮实际构建（6 档，全部串行 2 路）

```bash
# 1) ASI/TOP500 零 SUPER 首探 → 判死
super_build.py select --region ASI --universe TOP500 --delay 1 \
  --neutralization STATISTICAL --decay 2 --selection-limit 10 \
  --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0

# 2) DEU/TOP500 SLOW → leaq3P9l（本轮唯一新增可用）
super_build.py select --region DEU --universe TOP500 --delay 1 \
  --neutralization SLOW --decay 1 --selection-limit 10 \
  --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0

# 3) USA/TOP2000 CROWDING → prod 0.7775 FAIL
# 4) USA/TOP1000 SLOW → F0.85 FAIL
# 5) USA/TOP2000 SECTOR → prod 0.7656 FAIL
# 6) DEU/TOP500 INDUSTRY → prod 0.7412 FAIL（F3.63 最高）
```

**工程约束**：并发仿真上限 = **2**（第 3 路必 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`）；同式异 decay 同批会被平台去重；`--json` 必须传**绝对路径**（传 `results/x.json` 会拼成 `results/results/x.json`）。

### 8.2 配额约束

| 约束 | 值 |
|---|---|
| `SUPER_SUBMISSION` | **1 颗 / ET 日历日，账户级**，ET 00:00 重置（= GMT+8 13:00） |
| 当前 ET 日 | ET **2026-11-11**（GMT+8 2026-11-12 07:0x） |
| 本 ET 日已用 | **未用** — 最后一次 SUPER 提交 = `QPv88bJW` @ ET 2026-11-10 17:49:56 |
| 距额度重置 | 约 6 小时（ET 00:00 = GMT+8 今天 13:00） |
| 403 语义 | 零配额成本、**不判死候选**；同 ET 日重复 POST 只会继续 403，不可当探针 |

### 8.3 双闸实测记录

全部经 `check_correlation(correlation_type="both", refresh=True)`，明细见 `results/sa_scan_20261112/gates_20261112.json`（13 颗）。

---

## 九、算子利用率审计

| 维度 | 平台可用 | 本仓已用 | 利用率 | 本轮新增 |
|---|---|---|---|---|
| COMBO 算子 | 160（官方《SuperAlpha Operators》） | 14 | 8.8% | **0** |
| SELECTION 变量 | 43 | 6 | 14.0% | **0** |

本轮 6 档全部使用默认模板（`cp1` combo + 宽松 selection），**未引入任何新算子**。结论延续 11-09/11-10：**算子轴 ROI 已枯竭**——combo 形变（`zscore`/`rank(w)`/`sqrt(w)`/`ts_mean(w,20)`/`cp≥6`/`reduce_*`）全部证伪，selection 排序量换 `prod_correlation` 是毁灭性负杠杆。产能只能来自席位（新档或异族），不是算子。

---

## 十、提交建议（**只写建议，不执行提交**）

> **本轮未提交任何 alpha，等待用户指令。**

### 10.1 按 §5.5 字典序的建议（#1 顺位）

> ✅ **#1 已于 2026-11-11 19:37 ET 提交成功并 ACTIVE**（用户点名授权）：`stage=OS`、8 PASS / 0 FAIL / pending 空、`ra_failed=false`、self 0.3748 / prod 0.5670。本节以下内容保留为提交时的判定记录。

> ★ **08:2x EUR 突破后更新**：#1 改为 `E5Q7RGNR`，原 #1 `leaq3P9l` 降为 #3。

**#1 `E5Q7RGNR`**（EUR/TOP2500 SLOW d2 l10 trunc 0.02，selection `turnover > 0.095`）

| 闸 | 实测（refresh=True 2026-11-12 08:2x） | 结论 |
|---|---|---|
| prod ≤ 0.68 | **0.5670** | ✅ 余量 **0.1130**（全场最厚） |
| self ≤ 0.68 | **0.3487** | ✅ 余量 **0.3213**（全场最厚） |
| IS checks 零 FAIL | 8 PASS / 0 FAIL / 1 WARNING(`MATCHES_COMPETITION`) | ✅ |
| B 档双达标 | TO 0.2263 < 0.30 ∧ prod 0.5670 < 0.60 | ✅ |
| C 档（比赛级） | S 6.54 ∈ [5.6,7.0] ∧ TO 0.2263 ∈ [0.20,0.27] | ✅ **S 与 TO 双命中**（F 4.54 < 5.6 未命中） |
| 台账 `robustness_E5Q7RGNR` | 无记录（无 REJECT） | ✅ |
| 同档已有 SUPER 属异族 | EUR/TOP2500 现有 STAT d1(`GrgGkV1o`)/CROWDING d1(`kqJOQgnk`)，本颗 SLOW d2 | ✅ 异族，self 仅 **0.349** |

**#2 `MP6W3xnr`**（EUR/TOP2500 SLOW d1，同一 selection）：prod 0.5731 / self 0.3522，S **6.91** / F 4.40 / TO 0.2851。
⚠ 与 #1 **同族（只差 decay 1 vs 2）**，二者互相关预期 >0.95，**只能择一**。

**decay 梯度完整扫描（同一 selection `turnover > 0.095`，三档全部 0 FAIL）**：

| decay | ID | S | F | TO | dd | margin | IS_LADDER | SUB_UNIV | prod / self |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `MP6W3xnr` | **6.91** | 4.40 | 0.2851 | 0.68% | 8.11bp | **4.47** | **3.93** | 0.5731 / 0.3522 |
| **2** | **`E5Q7RGNR`** | 6.54 | **4.54** | **0.2263** | 0.70% | 9.64bp | 4.23 | 3.70 | **0.5670 / 0.3487** |
| 3 | `O0WY8dw1` | 6.22 | **4.54** | 0.1941 | 0.72% | **10.67bp** | 4.02 | 3.50 | 未测（同族，选了 d2 即作废） |

⇒ **F 在 d2 见顶（4.54），S 随 decay 单调下降**。三档中只有 d2 的 TO（0.2263）落在 C 档理想区间 [0.20, 0.27]（d1 超上界 5.6%、d3 低于下界）。**d2 是「F 峰值 × TO 区间 × prod 余量」的联合最优点**，d1 的 S 优势（+5.7%）被 TO 高 21% / margin 低 19% / prod 余量薄 0.006 抵消。d4 未跑（F 已在 d2/d3 持平，S 只会继续降）。

**取舍：`E5Q7RGNR` 在 F(+0.14)、TO(−0.059，进 C 档区间)、prod(−0.006)、self(−0.004) 上全胜，仅 S 低 0.37；`MP6W3xnr` 是 EUR 历史最高 S。**

**#3 `leaq3P9l`**（DEU/TOP500 SLOW d1 l10 trunc 0.08）

| 闸 | 实测（refresh=True） | 结论 |
|---|---|---|
| prod ≤ 0.68 | **0.5951** | ✅ 余量 0.0849 |
| self ≤ 0.68 | **0.5954** | ✅ 余量 0.0846 |
| IS checks 零 FAIL | 8 PASS / 0 FAIL / 1 WARNING(`MATCHES_COMPETITION`) | ✅ |
| B 档双达标 | TO 0.1608 < 0.30 ∧ prod 0.5951 < 0.60 | ✅ |
| 台账 `robustness_leaq3P9l` | 无记录（无 REJECT） | ✅ |
| 同档已有 SUPER 属异族 | DEU/TOP500 现有 STAT d1 / FAST d1，本品 SLOW d1 | ✅ 异族，self 0.5954 < 0.68 |

**#4 `1YNl3p5R`**（USA/TOP1000 CROWDING d1）：prod/self 0.6011/0.6011，余量 0.0789；A 档（prod 0.6011 差 0.0011 进不了 B 档）。
**#5 `e75avmq6`**（USA/TOP2000 SLOW d1）：prod 0.6373 / self 0.4871，S4.29 / F4.00。

### 10.2 ⚠ 若目标是「质量最好的那一颗」（Eff / S / F 优先）

EUR 突破后**两个口径已收敛到同一颗**：`E5Q7RGNR` 的 Eff **7.86** 全场第一（原第一 `Xg9WNRg8` 为 4.26），且同时是 B 档双达标 —— §5.4 记录的规则张力**仅对 #3 及以后仍然存在**。

1. **`E5Q7RGNR`** — S6.54 / F4.54 / TO0.2263 / prod 0.5670 / self 0.3487 / **Eff 7.86**
2. `MP6W3xnr` — S6.91 / F4.40 / TO0.2851 / prod 0.5731 / self 0.3522 / **Eff 8.43**（Eff 更高但 TO 出 C 档，且与 #1 同族）
3. `Xg9WNRg8` — Eff 4.26（已降至第 3）
4. `e75avmq6` — Eff 3.63

### 10.3 命令模板（**仅供用户手动执行，本轮未运行**）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 \
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit \
  --alpha-id <id> --region <REGION>
```

示例（未执行）：
```bash
# 方案 A（表内 #1）
... submit --alpha-id leaq3P9l --region DEU
# 方案 B（Eff 优先）
... submit --alpha-id e75avmq6 --region USA
```

### 10.4 提交前必须注意的两个已知坑

1. **停掉后台批次**：提交前确认无并发仿真/相关性子进程，否则 `_probe_prod_max` 抛 `ProxyError` 直接 fail-closed。
2. **prod 槽 195s 冷却**：`logs/_dblock/correlation.cooldown.json` 未过期会 fail-fast（非 prod 超标）。当前 cooldown 文件时间 11-12 01:08，已过期；但若刚跑过 `refresh=True`（本轮 07:0x 密集跑过 13 颗），需等冷却归零再提。

### 10.5 连带影响（提交后会发生什么）

- 交 `leaq3P9l` ⇒ **DEU/TOP500 第 3 族占用**，`2r5rA775` 的 self 预计从 0.6436 跳至 ≈0.9（同档兄弟 48h 内毒化，11-08 实证 +0.175/+0.233）⇒ **`2r5rA775` 立即作废**。
- 交 `e75avmq6`（或 `Xg9WNRg8`）⇒ 另一颗 self → ≈1.0 作废；`1YNl3p5R` 不受影响（不同 universe、不同区）。
- `npvEEWO8`（0.6817）与 `gJaJazPM`（0.6850）本条不推荐：即便平台能过，余量 <0.02，prod 漂移一天即可能超线。

---

## 十一、工程坑（本轮新踩/复验）

| 坑 | 现象 | 处置 |
|---|---|---|
| `--json` 相对路径 | `results/x.json` → `results/results/x.json` FileNotFoundError；纯文件名被静默忽略 | 传**绝对路径**（本轮全部用 `D:/.../results/...`，全部成功落盘） |
| `api_cache` 过期 | `--refresh` 仍读 600s TTL 内旧条目，漏掉当日提交的 SA | 先 `DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'`（本轮清掉 77 条） |
| 并发仿真上限 2 | 第 3 路 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`，脚本只印 `[error] ... / None` | 2 路串行 + 10s 错峰 |
| prod 单并发 | `correlation_busy` 返回 None（非报错） | 隔 1s 重查，不重派；`inflight=true` 时禁重新触发 |
| GLB/MINVOL10M 类档 | universe 内 REGULAR=0，仿真 ~35min | 勿按 8min 判挂起（本轮 ASI/TOP500 同属此类，实测 ~9min） |

---

## 附录 A：本轮数据文件

```
results/sa_scan_20261112/
├── probe_refresh.log                 # 池盘点（257 REGULAR / 53 SUPER ACTIVE）
├── slot_scan_local.py / slots_local.json  # 档位表 + 53 颗 SUPER 配方
├── rank_20261112.py / rank_table.json     # 五量与排序表
├── gates_20261112.json               # 13 颗双闸实测（refresh=True）
├── log_asi_t500_stat_d2.log          # 6 条构建日志
├── log_deu_t500_slow_d1.log
├── log_deu_t500_industry_d1.log
├── log_usa_t2000_crowd_d1.log
├── log_usa_t2000_sector_d1.log
├── log_usa_t1000_slow_d1.log
└── res_*.json                        # 各档原始返回
```

## 附录 B：本轮全量构建结果（6 档）

| 档位 | 族 | ID | S | F | TO | prod | 判定 |
|---|---|---|---|---|---|---|---|
| ASI/TOP500 | STAT d2 | `mLa3VnW5` | 1.61 | 0.62 | 0.3250 | — | ❌ F<1.0 / TO>0.30 |
| DEU/TOP500 | **SLOW d1** | **`leaq3P9l`** | 2.60 | 2.11 | 0.1608 | **0.5951** | ✅ **B 档** |
| DEU/TOP500 | INDUSTRY d1 | `qM71NjZO` | 3.14 | 3.63 | 0.1296 | 0.7412 | ❌ prod |
| USA/TOP2000 | CROWDING d1 | `vRAqNV9b` | 2.17 | 1.79 | 0.1831 | 0.7775 | ❌ prod |
| USA/TOP2000 | SECTOR d1 | `E5Q7GKg0` | 2.33 | 1.98 | 0.1854 | 0.7656 | ❌ prod |
| USA/TOP1000 | SLOW d1 | `vRAqNaxa` | 1.63 | 0.85 | 0.2600 | — | ❌ F<1.0 |
