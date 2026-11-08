# 各 Region 最优 SuperAlpha 方案 — 全流程扫描报告

**生成时间**: 2026-11-05 09:15 GMT+8
**工作目录**: `D:\coding\traeCN_project\wqb`
**结果目录**: `results/sa_scan_20261105/`
**组件池刷新**: `results/sa_probe_cache.json`（`--refresh` 全量翻平台，2026-11-05 07:44）
**扫描规模**: 本轮 18 个配方（A 6 / B 7 / C 5）→ **14 个出完整指标 + 4 个被平台拒**（全部为 `At least 10 component alphas are required`；另有 2 个出了指标但闸失败：`YP1xbMKw` 2Y 1.14、`pwdvRn8X` prod 0.7486）；叠加 11-04 的 16 个有效结果 ⇒ **累计 30 个有效候选，覆盖 7 个 region**
**铁律**: **只挖不提交** —— 本报告全部为待执行配方，未做任何提交动作。提交权归用户，且须点名。

> **★ 2026-11-05 09:31 更新：用户点名提交 `1YNjX03W` → 已受理并翻转 `status=ACTIVE`（全 8 项闸 PASS）。** 明细见 §1.3 与附录 C。其余 7 颗仍为待执行配方。

---

## 一、执行摘要

### 1.1 本轮三条结论

1. **找到真正的新席杠杆 = `turnover` 上限收紧到 0.10**。`(1-self)*(turnover<0.10)` 在 USA/TOP3000 造出 `1YNjX03W`（S 4.57 / F 4.44 / 2Y 4.23 / prod **0.6821** / self 0.5632），与已提交的 `A1V0eZne` **不同席**（若同席 self 会 ≈1.0）。而 `TO<0.18` 与 `TO<0.22` 选出**完全相同的组件子集**（`e7569r26` 与 `A1V0eZne` 逐位相同，self/prod 均为 1.0）⇒ **0.18 不是有效杠杆，0.10 才是**。
2. **DEU 破墙**：池 11→13 后，`P0oM2P8L`（SLOW + `TO<0.22`）prod **0.5522**（原 `QPv3Ww9p` 0.6923），self 0.5526，2Y 4.07。DEU 从「不建议」升为「可投」，且是全场 prod 余量第 2 厚。
3. **USA 可出 3 个互相独立的席位**：`1YNjX03W`(TOP3000) ↔ `xAr1Y5gg`(TOP1000) = **0.2606**、↔ `Xg9WNRg8`(TOP2000) = **0.2533**、`xAr1Y5gg` ↔ `Xg9WNRg8` = **0.4178**，全部远低于 0.7。这是本账户唯一能连续供颗的 region。

### 1.2 优先队列（**按平台收入口径重排**，2026-11-05 09:20 修订）

> **排序判据已从「max IS S」改为「预期平台收入」**。收入的乘数是 **OS 表现 × pyramid 倍率 × osmosis 点数**；本项目测得的 S/F 全部是 **IS 纯样本内**数字（见 §十），**OS 无法预览**（平台 `os` 段只回 `startDate`，无指标）。因此用三个可得代理加权排序：
> ① **2Y ladder Sharpe**（最近 2 年 IS，最接近未来的切片）② **margin**（费后每笔收益，OS 衰减最慢的项）③ **Fitness**（跨期稳定性）；再乘 **region D1 倍率**。
> 综合分 `Score = 2Y × F × margin × D1均值`（**仅作序数排序用，无绝对经济含义**）。

| 收入序 | Alpha ID | Region/Universe | S | F | **2Y** | **margin** | TO | D1 倍率 | **Score** | prod（实测） | 备查 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ⭐**1 ✅已提交** | **`1YNjX03W`** | USA/TOP3000 | 4.57 | 4.44 | 4.23 | **0.00328** | **0.072** | 1.16 | **0.0714** | 0.6821 | **2026-11-05 09:31 ACTIVE**；全表 margin 最高（3.3× 次优），TO 最低 |
| ⭐**2** | **`9qxVG66r`** | KOR/TOP600 | 3.95 | 4.55 | 3.09 | 0.00265 | 0.128 | **1.39** | **0.0518** | 0.6370 | F 最高 + KOR 倍率第 2 |
| ⭐**3** | **`Xg9WNRg8`** | USA/TOP2000 | 4.74 | 4.10 | **5.46** | 0.00150 | 0.166 | 1.16 | 0.0389 | 0.6493 | 2Y 全表最高 |
| 4 | `xAr1YZQb` | EUR/TOPCS1600 | 4.32 | 3.97 | 4.07 | 0.00169 | 0.149 | 1.20 | 0.0329 | 0.6007 | margin 第 3 |
| 5 | `2rAOGKow` | IND/TOP500 | 4.43 | 3.58 | 4.10 | 0.00131 | 0.277 | 1.14 | 0.0219 | 0.6097 | TO 偏高（0.277）拖累费后 |
| 6 | `P0oM2P8L` | DEU/TOP500 | 2.40 | 1.92 | 4.07 | 0.00128 | 0.152 | **1.62** | 0.0162 | 0.5522 | 倍率第 1，但 F/S 低 |
| 7 | `xAr1Y5gg` | USA/TOP1000 | 2.80 | 2.05 | 2.98 | 0.00108 | 0.146 | 1.16 | 0.0076 | 0.4777 | **prod 最安全，但收入序倒数第 2** |
| 8 | `GrWdQNq0` | GLB/TOP3000 | 3.51 | 1.58 | 2.43 | **0.00040** | 0.286 | 1.19 | 0.0018 | 0.5864 | margin 最低（0.0004），收入最差 |

> **`xAr1Y5gg` 从 #1 降到 #7**：它在 S/F/2Y/margin **四项全部垫底或次垫底**，唯一优势是 prod 0.4777。而 prod 余量只影响「能否提交成功」，**不影响拿到多少收入**（被 prod 闸拦下不消耗配额）。按收入口径它不该排前面。
> **`1YNjX03W` 的 margin 0.00328 是决定性优势**：TO 仅 0.072 ⇒ 每笔交易成本摊薄，费后收益是 `xAr1Y5gg` 的 **3.0 倍**。平台按 OS 费后表现付费，margin 是最直接的正向因子。
> **`9qxVG66r` 被 region 倍率抬高**：KOR D1 均值 1.39（vs USA 1.16），同样的 OS 表现多出 ~20% 塔位分；F 4.55 还是全表最高。
> **`GrWdQNq0` 应从队列剔除**：margin 0.0004（比次低者还低 2.7 倍）、TO 0.286、F 1.58 —— 三项都是收入口径最差。
> **`P0oM2P8L` 定位变化**：DEU 倍率 1.62 全场最高，但 S 2.40 / F 1.92 使 Score 只排第 6。**它是「低投入高产点」而非「高收入」**，适合在配额空档时投，不适合优先占用主配额。

### 1.3 实际可提交队列（去同席后 8 颗，**收入序**）

| 天序 | Alpha | Region | 收入理由 | 风险 |
|---|---|---|---|---|
| **Day 1 ✅完成** | `1YNjX03W` | USA/TOP3000 | margin 0.00328 + TO 0.072，费后最强 | ~~prod 0.6821~~ **已过闸提交，status=ACTIVE** |
| Day 2 | `9qxVG66r` | KOR/TOP600 | F 4.55 + KOR 倍率 1.39 | prod 0.6370 |
| Day 3 | `Xg9WNRg8` | USA/TOP2000 | 2Y 5.46 全表最高 | prod 0.6493 |
| Day 4 | `xAr1YZQb` | EUR | margin 0.00169，EUR 唯一席 | prod 0.6007 |
| Day 5 | `2rAOGKow` | IND | S/F 双高 | TO 0.277 拖费后 |
| Day 6 | `P0oM2P8L` | DEU | 倍率 1.62 最高 | S/F 偏低 |
| Day 7 | `xAr1Y5gg` | USA/TOP1000 | prod 最安全（0.4777） | **收入序倒数第 2** |
| Day 8 | `GrWdQNq0` | GLB/TOP3000 | — | **建议剔除**（margin 0.0004） |

**配额**：SUPER = **账号级 1/ET日（跨区共享）**，上述 8 颗需 8 个 ET 日；与 REGULAR 4/天/区独立计数。
**每颗提交前强制**：`check_correlation(alpha_id=..., correlation_type="production", refresh=True)` 重测；台账 48h 作废。
**被 prod 闸拦下不消耗配额**（fail-closed 发生在 POST 之前）⇒ 允许按收入序直接冲高，被拦再降级，不必为「稳」而提前降级。

---

## 二、数据基线

### 2.1 组件池 eligibility（ACTIVE 已提交 REGULAR，region 级）

| Region | ACTIVE 组件 | 未提交 IS 候选 | 可建性 | vs 11-04 |
|---|---|---|---|---|
| USA | **47** | 0 | GO | 持平 |
| IND | **45** | 0 | GO | 持平 |
| KOR | **30** | 0 | GO | 持平 |
| GBR | **24** | 30 | GO | 持平 |
| EUR | **20** | 201 | GO | 持平 |
| MEA | 19 | 0 | **BLOCKED（平台关闭）** | 持平 |
| GLB | **18** | 0 | GO | 持平 |
| DEU | **13** | 691 | GO | **+2** |
| ASI | 9 | 28 | **BLOCKED（差 1 颗）** | 持平 |
| HKG | 7 | 0 | **BLOCKED（差 3 颗）** | **+1** |

> **口径**：组件池按 **region 级**聚合（非 universe 级）。实测 USA/TOP1000 的 REGULAR 计数为 0，但仍能建 SA。
> **ASI 解锁路径最短**：池内有 28 条未提交 IS 候选，用户点名提交 1 颗 RA 即可 9→10 进入可建区。
> **HKG 需 3 颗**：REGULAR 配额 4/天/区，理论上 1 天可解锁。
> **注**：`probe_sa_candidates.py --json results/xxx.json` 存在路径拼接 bug（写成 `results/results/xxx.json` 而报 FileNotFoundError）；数据已完整落在主缓存 `results/sa_probe_cache.json`，不影响结论。

### 2.2 档位占用分类（46 颗 ACTIVE SUPER / 16 个 region×universe 档）

| 档位 | REGULAR | SUPER | 分类 | 已用中性化族（selLimit） |
|---|---|---|---|---|
| USA/TOP3000 | 38 | **5** | 双占用 | FAST10 / STAT30 / SUBINDUSTRY10 / MARKET1000 / **SLOW10（`A1V0eZne`，11-03 新提交）** |
| USA/TOP2000 | 5 | 1 | 双占用 | STAT15 |
| USA/TOP1000 | 0 | 1 | 仅 SA 占用 | STAT15 |
| USA/TOP500 | 0 | 1 | 仅 SA 占用 | CROWDING10 |
| USA/TOPSP500 | 0 | 1 | 仅 SA 占用 | STAT38 |
| IND/TOP500 | 45 | **11** | 双占用（最饱和） | INDUSTRY1 / STAT6 / SUBIND3 / R&M1 |
| KOR/TOP600 | 30 | **10** | 双占用 | STAT6 / SUBIND2 / CROWDING1 / R&M1 |
| GBR/TOP700 | 24 | 5 | 双占用 | SLOW / FAST / STAT×2 / R&M |
| GLB/MINVOL1M | 17 | 2 | 双占用 | STAT / SUBINDUSTRY |
| GLB/MINVOL10M | 0 | 1 | 仅 SA 占用 | SLOW |
| GLB/TOP3000 | 0 | 1 | 仅 SA 占用 | R&M |
| GLB/TOPDIV3000 | 1 | 1 | 双占用 | STAT15 |
| EUR/TOP2500 | 11 | 2 | 双占用 | CROWDING / STAT |
| EUR/TOPCS1600 | 9 | 1 | 双占用 | STAT10（trunc 0.08） |
| DEU/TOP500 | 13 | 1 | 双占用 | STAT10 |
| MEA/TOP400 | 19 | 2 | 双占用（平台关闭） | SUBINDUSTRY×2 |

**已占 selection 表达式（46 颗共 20 种）**：16 颗用默认 `(1-self)`，其余为 `(0.65~1.0 - prod_correlation)` × `self_correlation<0.45/0.48/0.55/0.65/0.7` 的各种组合。
**本轮首次引入的是两类表达式**：`(1-self)*(turnover<0.22)`（11-04 首测）与 `(1-self)*(turnover<0.10)`（本轮首测）。**`turnover` 在此之前从未出现在任何已提交 SA 的 selection 里。**

> **⚠ 分类口径修正（11-04 已证伪，本轮再次确认）**：`零 OS 档 ⇒ self 恒 0` 不成立。self 池按 **region** 聚合（USA 47 颗 REGULAR），`A1V0L9KQ` 在 REGULAR=0 的 USA/TOP1000 上 self 仍 0.6331。**「仅 SA 占用档」不等于安全档。**

### 2.3 Pyramid 倍率（本轮 MCP 复核，与 11-04 一致）

| Region | n 类别 | D1 均值 | D0 均值 | 最高 | 最低 |
|---|---|---|---|---|---|
| DEU | 16 | **1.62** | 1.85 | model/news/other 1.8 | imbalance 1.2 |
| CHN | 12 | 1.61 | 1.74 | other 1.9 | socialmedia 1.1 |
| AMR | 2 | 1.55 | 1.75 | sentiment 1.7 | pv 1.4 |
| GBR | 16 | **1.41** | 1.69 | sentiment 1.7 | imbalance 1.0 |
| HKG | 15 | 1.41 | — | analyst/model/other 1.7 | imbalance 1.0 |
| KOR | 15 | **1.39** | — | analyst/fundamental/model 1.6 | imbalance 1.0 |
| EUR | 14 | 1.20 | 1.40 | other 1.5 | risk/imbalance 1.0 |
| GLB | 13 | 1.19 | — | fundamental/analyst/sentiment 1.4 | pv/risk 1.0 |
| ASI | 16 | 1.18 | — | analyst 1.5 | imbalance/macro 1.0 |
| USA | 16 | **1.16** | 1.53 | other/sentiment 1.4 | institutions/imbalance 1.0 |
| IND | 15 | **1.14** | — | analyst 1.4 | risk/institutions 1.0 |

> 倍率决定**塔位分（产出）**，不决定可行性。DEU 倍率最高（1.62）但池最小；USA/IND 倍率最低但池最大 ⇒ **产出与可投性分离**。

### 2.4 现有 46 颗 SUPER 表现分布

- Sharpe：中位 ~3.9，最高 **6.93**（GLB `LL5amzov`），最低 1.82（`E567rQvR`）
- Fitness：中位 ~3.5，最高 **5.94**（KOR `RRA9EZKz`）
- 区域分布：IND 11 / KOR 10 / **USA 9**（本轮 +1，`A1V0eZne`）/ GBR 5 / GLB 5 / EUR 3 / MEA 2 / DEU 1
- 全部 `selectionHandling=POSITIVE`（论坛推荐的 Non-Zero 本账户未用过，POSITIVE 46/46 成功）

---

## 三、选点原则

1. **档位占用类型 > 组件池大小**
   - 「仅 SA 占用」档（REGULAR=0）在 self 上**没有豁免**（region 级池），实际价值只剩「prod 池更空」。
   - 「双占用」档必须靠**未占用的中性化族**或**未用过的 selection 子集**开新席。
2. **指标 = 约束优化**：`max S ∧ max F  s.t. self<0.7 ∧ prod<0.7`，优选 `prod<0.6 ∧ TO<0.30`（B 档）。
   - prod ≥ 0.7 = **合规红线，无豁免**（`super_build.py submit` fail-closed）。
   - **prod 余量 ≥ 0.02 才算安全**（本报告「prod 余量」列）。
3. **中性化族是 prod 杠杆，不是席杠杆**
   - SLOW 仍是最强通用族（IND / USA / KOR / GBR / GLB / DEU 六区全部最低或并列最低）。
   - 但同一 selection 下换族，日收益相关 **0.70–0.93**（11-04 实测 15 组）⇒ 换族不换席，只能降 prod 0.03–0.12。
4. **席位 = `region × selection 子集`**；换 universe 只在覆盖差异大时算半个新席（USA TOP2000↔TOP1000 = 0.4178 可共存；EUR TOP2500⊃TOPCS1600 = 0.79 同席）。
5. **combo 权重口径（cp 幂次 / `reduce_*`）不换席**：本轮 `reduce_avg` 版 self **0.9938**，cp 也从未产生 <0.9 的相关 ⇒ 只当 prod 微调旋钮。
6. **组件数 ↑ ⇒ self ↓ 但 prod ↑**：EUR l10→l12 prod 0.6007→0.6821；GLB l10/l15 均可用但 **l12 直接打穿 2Y（1.14 < 1.58）** ⇒ l12 是 GLB 的死档，不是梯度上的一个点。

---

## 四、论坛指标标准（2026-10-22 定稿，本轮沿用并实测校验）

### 4.1 组成数量（Selection Limit）

- **平台硬下限 = 10**（<10 直接 400：`Ensure this value is greater than or equal to 10`）
- 论坛 78 赞帖建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300
- **实际生效数 = min(limit, 组件池)**；池是 region 级
- **本账户实测结论：l10 双闸综合最优**，l12/l15/l30 一律推高 prod 或打穿 2Y。本轮 18 个配方中 l12 两个（EUR 0.6821 / GLB 2Y 1.14），均劣于 l10。

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9** | 0.20–0.27 | <0.5 |

本轮 **B 档 3 颗**：`xAr1Y5gg`(0.4777) / `P0oM2P8L`(0.5522) / `GrWdQNq0`(0.5864)。
本轮 **C 档 0 颗**：`omEo6o5J`（S 6.49 / F 7.17）达 C 档指标，但 self/prod 均 0.9938 —— 与已提交 `A1V0eZne` 同席，不可再用。

### 4.3 组件筛选阈值

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。

> **★ 本轮实测：`author_fitness≥2` 在 USA 47 颗池上也直接报 `At least 10 component alphas are required`。**
> 说明该字段的实际分布远低于 2（或平台对 SUPER 组件的 author_fitness 口径不同）。
> ⇒ **论坛这套筛选阈值在本账户不可用，只保留 turnover 一类约束**。
> 同一错误也发生在 `TO<0.10` 上：IND(45) / KOR(30) / GLB(18) 三区全部不足 10 颗组件，**只有 USA 的池深度能承受 0.10 的收紧**。

### 4.4 中性化族规律

- Fitness 排序（IND 社区实测）：CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3
- 选族规则：**TO<0.10 → SLOW；TO>0.20 → FAST**
- 区域族基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（**须逐区验证**）
- **本账户实测反例**：IND 的 CROWDING 直接撞墙（0.7255），RAM 也高；**SLOW 才是 IND 的真解**。社区排序不可照搬。

### 4.5 其他实证

- truncation 0.02 vs 0.08 对 SA 几乎无差异（历史 S 3.74 vs 3.73）；本轮全用 0.02
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区 46 颗 SA 全用 **POSITIVE** 均成功
- decay 在 SA 组合层**完全无效**（d0 与 d1 逐字相同）；本轮全用 d1

---

## 五、分 Region 方案

### 5.1 总表

| Region | 池 | 最优配方 | Alpha ID | S | F | 2Y | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **USA** | 47 | TOP1000 SLOW l10 cp3 + `TO<0.22` | `xAr1Y5gg` | 2.80 | 2.05 | 2.98 | 0.146 | 0.3295 | **0.4777** | **0.222** | ✅ B 档 |
| USA 2nd | — | TOP2000 SLOW l10 cp3（DEF） | `Xg9WNRg8` | 4.74 | 4.10 | 5.46 | 0.166 | 0.6493 | 0.6493 | 0.051 | ✅ A |
| USA 3rd | — | TOP3000 SLOW l10 cp1 + `TO<0.10` | `1YNjX03W` | 4.57 | 4.44 | 4.23 | 0.072 | 0.5632 | 0.6821 | 0.018 | ✅ A（薄） |
| **DEU** | 13 | TOP500 SLOW l10 cp3 + `TO<0.22` | `P0oM2P8L` | 2.40 | 1.92 | 4.07 | 0.152 | 0.5526 | **0.5522** | 0.148 | ✅ B 档 |
| **IND** | 45 | TOP500 SLOW l10 cp3（DEF） | `2rAOGKow` | 4.43 | 3.58 | 4.10 | 0.277 | 0.6101 | 0.6097 | 0.090 | ✅ A |
| **EUR** | 20 | TOPCS1600 FAST l10 cp1 + `TO<0.22` | `xAr1YZQb` | 4.32 | 3.97 | 4.07 | 0.149 | 0.6007 | 0.6007 | 0.099 | ✅ B 边界 |
| **KOR** | 30 | TOP600 SLOW l10 cp7（DEF） | `9qxVG66r` | 3.95 | 4.55 | 3.09 | 0.128 | 0.6370 | 0.6370 | 0.063 | ✅ A |
| **GLB** | 18 | TOP3000 SLOW **l15** cp3（DEF） | `GrWdQNq0` | 3.51 | 1.58 | 2.43 | 0.286 | 0.5135 | 0.5864 | 0.114 | ✅ B 档（F 薄） |
| **GBR** | 24 | 无新增席 | — | — | — | — | — | — | — | — | ❌ 停投 |
| **MEA** | 19 | — | — | — | — | — | — | — | — | — | ❌ 平台关闭 |

### 5.2 USA（池 47，9 颗 SUPER 已占）

**已占席**：TOP3000 五族（FAST/STAT/SUBIND/MARKET/**SLOW**）+ TOP2000 STAT + TOP1000 STAT + TOP500 CROWDING + TOPSP500 STAT

本轮 8 档实测：

| 配方 | ID | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| TOP1000 SLOW l10 cp3 + `TO<0.22` | `xAr1Y5gg` | 2.80 | 2.05 | 0.146 | 0.3295 | **0.4777** | ✅ **最优** |
| TOP3000 SLOW l10 cp1 + `TO<0.10` | `1YNjX03W` | 4.57 | 4.44 | 0.072 | 0.5632 | 0.6821 | ✅ 新席 |
| TOP1000 SLOW l10 cp3 + `TO<0.10` | `kqNJo6wz` | 2.29 | 1.69 | 0.100 | 0.3119 | 0.5477 | ✅（被 `xAr1Y5gg` 支配：同席相关 0.4602，S/F 更低） |
| TOP2000 SLOW l10 cp3 + `TO<0.22` | `YP1x5lzA` | 4.76 | 4.51 | 0.130 | 0.3530 | **0.7077** | ❌ prod 超线 0.0077 |
| TOP3000 SLOW l10 cp1 + `TO<0.18` | `e7569r26` | 6.39 | 7.06 | 0.118 | **1.0** | **1.0** | ❌ 与 `A1V0eZne` 逐位同席 |
| TOP3000 SLOW cp1 + `reduce_avg` 权重 | `omEo6o5J` | 6.49 | 7.17 | 0.119 | 0.9938 | 0.9938 | ❌ 同席（S/F 略优于 `A1V0eZne`，但无席可放） |
| TOP3000 CROWDING l10 cp3 + `TO<0.22` | `qMLEWjrP` | 4.42 | 5.47 | 0.096 | 0.6726 | 0.7708 | ❌ CROWDING 在 USA 无区分度（标准版 0.8418 → 加 TO 只降到 0.7708） |
| TOP3000 SLOW l10 + `author_fitness≥2` | — | — | — | — | — | — | ❌ 组件 <10，平台拒 |

> **USA 的核心发现**：`TO<0.22` 的降 prod 效应**不跨 universe 外推**。同一条 selection，在 TOP3000 把 prod 从 0.784 压到 0.615（11-04），在 TOP2000 却从 0.649 抬到 0.708（本轮）。原因是两 universe 的组件集合不同，被 `turnover` 筛掉的组件在两边的 prod 贡献方向相反。**每换一个 universe 必须重测，不能继承结论。**

### 5.3 DEU（池 13，+2）

| 配方 | ID | S | F | 2Y | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|---|
| SLOW l10 cp3 + `TO<0.22` | `P0oM2P8L` | 2.40 | 1.92 | 4.07 | 0.152 | 0.5526 | **0.5522** | ✅ **破墙** |
| SLOW l10 cp3（DEF，11-04） | `QPv3Ww9p` | 2.13 | 1.60 | 3.38 | 0.152 | 0.6923 | 0.6923 | ⚠ 擦双线 |
| CROWDING（11-04） | `rKRPwOJJ` | 2.59 | 2.53 | — | — | 0.7283 | 0.7282 | ❌ |

> 池从 11 → 13 只加 2 颗，prod 就掉 0.14。**DEU 的天花板确实由池深决定**，此前「池 11 太小、不值得投」的判断在池 13 时已不成立。
> 唯一注意：F 1.92 虽过 1.0 底线，但 S 2.40 使 DEU 的边际贡献偏低；若当日只能投 1 颗，优先级低于 USA/EUR。

### 5.4 IND（池 45，11 颗 SUPER 已占 —— 最饱和）

| 配方 | ID | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| SLOW l10 cp3（DEF，11-04） | `2rAOGKow` | **4.43** | **3.58** | 0.277 | 0.6101 | 0.6097 | ✅ 首选 |
| SLOW l10 cp3 + `TO<0.22` | `vR1OrVb3` | 2.92 | 2.48 | 0.156 | 0.5007 | **0.5170** | ✅ 备选（余量更厚） |
| SLOW l10 cp3 + `TO<0.10` | — | — | — | — | — | — | ❌ 组件 <10 |

- `2rAOGKow` ↔ `vR1OrVb3` = **0.7245** ⇒ 只能出 1 颗。
- 选择：**`2rAOGKow`**（S/F 高 1.5 倍，prod 0.6097 仍在 0.65 质量线内）；若用户更看重余量则换 `vR1OrVb3`（0.5170，但 S 只有 2.92）。
- IND 已有 11 颗 SUPER，**新增席位的边际价值低于 USA**，但 IND 的 D1 倍率 1.14 是全区最低 ⇒ 产出最低，排 Day 3 之后。

### 5.5 EUR（池 20，3 颗 SUPER 已占）

| 配方 | ID | S | F | 2Y | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|---|
| TOPCS1600 FAST l10 cp1 + `TO<0.22` | `xAr1YZQb` | 4.32 | 3.97 | 4.07 | 0.149 | 0.6007 | **0.6007** | ✅ **首选** |
| TOP2500 FAST l12 + `TO<0.22` | `leAMvqQe` | **4.75** | **4.52** | 3.99 | 0.129 | 0.6546 | 0.6821 | ⚠ 指标最优但 prod 薄 |
| TOPCS1600 FAST l10（DEF，11-04） | `A1V0LZkg` | 4.53 | 3.89 | 4.33 | 0.184 | 0.6390 | 0.6391 | ✅ 同席 |

- 三者互测 **0.7366–0.9655**（`xAr1YZQb`↔`A1V0LZkg` = 0.9655）⇒ **EUR 只能出 1 颗**。
- 选择建议：**`xAr1YZQb`**（prod 最低 0.6007）。若用户接受 0.68 的薄余量换取 S 4.75 / F 4.52，则用 `leAMvqQe`。
- **l10 → l12 的代价**：prod 0.6007 → 0.6821，S 却只涨 0.43 ⇒ **l12 不划算**，再次印证 l10 甜点。

### 5.6 KOR（池 30，10 颗 SUPER 已占）

| 配方 | ID | S | F | 2Y | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|---|
| SLOW l10 cp7（DEF，11-04） | `9qxVG66r` | 3.95 | **4.55** | 3.09 | 0.128 | 0.6370 | 0.6370 | ✅ 唯一席 |
| SLOW l10 cp7 + `TO<0.22` | `Xg9RblQb` | 3.95 | 4.55 | 3.09 | 0.128 | 0.6370 | 0.6370 | ❌ **与上逐位相同** |
| SLOW l10 cp7 + `TO<0.10` | — | — | — | — | — | — | — | ❌ 组件 <10 |

> **KOR 是「排除法」的最佳证据**：`Xg9RblQb` 与 `9qxVG66r` 在 S/F/2Y/TO/self/prod/margin/returns/drawdown 九个字段上**逐位相同** ⇒ KOR 组件的 turnover 全部 <0.22，`turnover` 过滤在 KOR 上**非约束**，不产生任何新子集。
> KOR 已 10 颗 SUPER，**后续只在池扩到 35+ 时才有新席**。

### 5.7 GLB（池 18，5 颗 SUPER 已占）

| 配方 | ID | S | F | 2Y | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|---|
| TOP3000 SLOW **l15** cp3（11-04） | `GrWdQNq0` | 3.51 | 1.58 | 2.43 | 0.286 | 0.5135 | **0.5864** | ✅ 首选 |
| TOP3000 SLOW l10 cp3（11-04） | `0mYpnMr1` | 3.45 | 1.42 | 2.39 | 0.373 | 0.4560 | **0.5010** | ✅ 同席（0.9551） |
| TOP3000 SLOW **l12** cp3 + `TO<0.22` | `YP1xbMKw` | 2.79 | 1.43 | **1.14** | 0.161 | 0.5376 | 0.6369 | ❌ **2Y 1.14 < 1.58** |
| TOP3000 SLOW l10 + `TO<0.10` | — | — | — | — | — | — | — | ❌ 组件 <10 |

> **GLB 的 l12 是死档**：l10（TO 0.373）与 l15（TO 0.286）都过，唯独 l12 的 2Y 掉到 1.14。不是单调梯度，**不能靠外推选 limit**。
> `GrWdQNq0` 与 `0mYpnMr1` 同席（0.9551），选 `GrWdQNq0`（S 3.51 > 3.45、F 1.58 > 1.42），但 `0mYpnMr1` 的 prod 0.5010 更安全 —— **若只求过闸，`0mYpnMr1` 余量 0.199 更稳**。

### 5.8 GBR（池 24，5 颗 SUPER 已占）— 本轮新增席为 0

| 配方 | ID | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| TOP700 SLOW l10（11-02，**已提交**） | `QPvGdLYQ` | 4.23 | 3.54 | 0.170 | 0.6330 | 0.6330 | ✅ ACTIVE |
| TOP700 CROWDING l10 cp3 + `TO<0.22` | `pwdvRn8X` | 3.67 | 3.58 | 0.151 | **0.7486** | 0.7486 | ❌ 与已提交 SLOW 同席 |

> GBR 只有 1 个 universe（TOP700）⇒ 按「席 = region × selection 子集」，GBR 的第 2 席只能来自不同 selection。CROWDING 已被证死（0.7486）。**GBR 停投，直到池扩到 30+ 或找到新 selection 类型。**

### 5.9 MEA / ASI / HKG

| Region | 状态 | 依据 |
|---|---|---|
| MEA | **平台关闭** | `POST /simulations` 返回 `Region MEA is not available.`；`get_platform_setting_options` 无该区。存量 19 REGULAR + 2 SUPER 仍 ACTIVE |
| ASI | 组件 9/10 | 差 1 颗；池内 28 条未提交 IS 候选可捞，**用户点名提交 1 颗 RA 即解锁** |
| HKG | 组件 7/10 | 差 3 颗；本轮从 6→7（+1），需再提交 3 颗 RA |

---

## 六、停投区

| Region | 理由 | 依据 |
|---|---|---|
| **MEA** | 平台关闭，无法新建 | 11-04 四档全 400 |
| **GBR** | 新增席 = 0 | 唯一 universe，SLOW 已占（`QPvGdLYQ` ACTIVE），CROWDING 0.7486 撞墙 |
| **HKG** | 组件 7/10 | 差 3 颗 RA |
| **ASI** | 组件 9/10 | 差 1 颗 RA（解锁成本最低，优先做） |
| **CHN / AMR** | 账户零组件 | 无 REGULAR 持仓 |
| **IND / KOR / EUR** | 已有席饱和（新增仅 1 席/区） | IND 11 / KOR 10 颗 SUPER；EUR 三颗候选互测 0.74–0.97 |
| **DEU** | ~~停投~~ → **恢复可投** | 池 13，prod 0.5522（本轮） |

---

## 七、撞墙档案（已验证不可用，勿重复投入）

### 7.1 同席墙（本轮最重要）

| 组合 | 相关 | 判定 |
|---|---|---|
| `e7569r26` ↔ `A1V0eZne` | **1.0000** | `TO<0.18` 与 `TO<0.22` **选同一子集** —— 阈值收紧到 0.18 无效 |
| `omEo6o5J` ↔ `A1V0eZne` | **0.9938** | `reduce_avg` 权重不换席 |
| `Xg9RblQb` ↔ `9qxVG66r` | **逐位相同** | KOR 的 `turnover` 过滤非约束 |
| `xAr1YZQb` ↔ `A1V0LZkg` | 0.9655 | EUR 同席（TOPCS1600 FAST） |
| `GrWdQNq0` ↔ `0mYpnMr1` | 0.9551 | GLB 同席（TOP3000 SLOW 换 limit 不换席） |
| `xAr1Y5gg` ↔ `A1V0L9KQ` | **0.8081** | USA/TOP1000 同席 ⇒ 取 `xAr1Y5gg` |
| `2rAOGKow` ↔ `vR1OrVb3` | 0.7245 | IND 同席，二选一 |
| `xAr1YZQb` ↔ `leAMvqQe` | 0.7642 | EUR 跨 universe 仍同席 |

### 7.2 prod 墙（≥0.7）

| ID | 配方 | S | F | self | prod | 墙因 |
|---|---|---|---|---|---|---|
| `qMLEWjrP` | USA/TOP3000 CROWDING cp3 + `TO<0.22` | 4.42 | 5.47 | 0.6726 | **0.7708** | CROWDING 在 USA 与生产池强重叠（标准版 0.8418，TO 约束只降到 0.77） |
| `YP1x5lzA` | USA/TOP2000 SLOW cp3 + `TO<0.22` | 4.76 | 4.51 | 0.3530 | **0.7077** | **`TO<0.22` 在 TOP2000 反而升 prod**（标准版 0.6493 → 0.7077），差 0.0077 落线 |
| `pwdvRn8X` | GBR/TOP700 CROWDING cp3 + `TO<0.22` | 3.67 | 3.58 | 0.7486 | 0.7486 | 与已提交 `QPvGdLYQ`（SLOW）同席 |
| `vR1kAQmr` | USA/TOP3000 SLOW cp3（DEF sel，11-04） | 6.18 | 6.33 | 0.7838 | 0.7838 | 同槽已由 `A1V0eZne`（TO<0.22）取代 |
| `mLovnvXx` | USA/TOP3000 CROWDING cp3（DEF，11-04） | 4.68 | 5.90 | 0.8418 | 0.8418 | 本轮补测 TO 约束版仍 0.7708 |

### 7.3 IS 闸墙

| ID | 配方 | 失败闸 | 值/限 |
|---|---|---|---|
| `YP1xbMKw` | GLB/TOP3000 SLOW **l12** cp3 + `TO<0.22` | **IS_LADDER_SHARPE** | **1.14 / 1.58** |
| `omE6ad7E` | EUR/TOP2500 SLOW cp3（11-04） | IS_LADDER_SHARPE | 1.50 / 1.58 |
| `MPY1gw08` | USA/TOP500 SLOW cp3（11-04） | LOW_SHARPE + LOW_FITNESS | 1.48/1.58；0.74/1.0 |

### 7.4 组件不足墙（本轮 4 例，全部 `At least 10 component alphas are required`）

| 配方 | 提出区池深 | 说明 |
|---|---|---|
| USA/TOP3000 `author_fitness≥2` | 47 | **论坛 §0.3 的 author 阈值在本账户不可用** |
| IND/TOP500 `TO<0.10` | 45 | 池够深但低换手组件不足 10 颗 |
| KOR/TOP600 `TO<0.10` | 30 | 同上（且 KOR 本就全员低 TO） |
| GLB/TOP3000 `TO<0.10` | 18 | 同上 |

> **规律**：`TO<0.10` 只在 **USA（47 颗、且 universe 覆盖 TOP3000 大盘）** 成立。其余区一律 <10 组件。

### 7.5 近失候选（prod 0.65–0.70，达 A 档但不达 0.65 质量线）

| ID | 配方 | S | F | prod | 差 0.65 |
|---|---|---|---|---|---|
| `YP1x5lzA` | USA/TOP2000 SLOW cp3 + `TO<0.22` | 4.76 | 4.51 | 0.7077 | +0.0577（且已破 0.70 红线） |
| `leAMvqQe` | EUR/TOP2500 FAST l12 + `TO<0.22` | 4.75 | 4.52 | 0.6821 | +0.0321 |
| `1YNjX03W` | USA/TOP3000 SLOW l10 + `TO<0.10` | 4.57 | 4.44 | 0.6821 | +0.0321（新席，值这个价） |
| `QPv3Ww9p` | DEU/TOP500 SLOW（11-04） | 2.13 | 1.60 | 0.6923 | +0.0423 |

---

## 八、执行清单

### 8.1 构建命令（可复现）

```bash
cd D:/coding/traeCN_project/wqb
# 批次 A（USA 新席探索 6 档）
world-quant-brain-mcp/.venv/Scripts/python.exe -u C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261105/configs_A.json \
  --out results/sa_scan_20261105/res_A.jsonl
# 批次 B（EUR/IND/KOR/GBR/GLB/DEU 7 档）
... --configs results/sa_scan_20261105/configs_B.json --out results/sa_scan_20261105/res_B.jsonl
# 批次 C（TO<0.10 新子集实验 5 档）
... --configs results/sa_scan_20261105/configs_C.json --out results/sa_scan_20261105/res_C.jsonl
```

**配方原文**（下轮可直接复用）：

```
selection(TO<0.22) = (1 + 0 * (prod_correlation > 0)) * (1 - self_correlation) * (turnover < 0.22)
selection(TO<0.10) = (1 + 0 * (prod_correlation > 0)) * (1 - self_correlation) * (turnover < 0.10)
selection(DEF)     = (1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)
combo(cp1)         = stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500);
                     ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic);
                     w = 1 - maxCorr; w
settings           = d1 / truncation 0.02 / POSITIVE / componentActivation IS / maxTrade OFF
```

### 8.2 配额约束

| 项 | 限制 | 影响 |
|---|---|---|
| SUPER 提交 | **账号级 1/ET日（跨区共享）** | 8 颗候选 = 8 天 |
| REGULAR 提交 | 4/天/区（与 SUPER 独立） | 解锁 ASI（+1）/ HKG（+3）不受影响 |
| prod 相关性检查 | 账号级单并发 | 并发会返回 `correlation_busy`，需按 `retry_after` 重试（本轮实测 1.4–1.9s） |
| 仿真并发 | 平台限流 429 | `sa_run.py` 已内置耐心轮询 90×10s |

### 8.3 建议执行顺序（**收入序，见 §1.3 / §10**）

1. `1YNjX03W`（USA/TOP3000，margin 0.00328 / TO 0.072，费后最强；prod 0.6821 需当日复测）
2. `9qxVG66r`（KOR，F 4.55 + 倍率 1.39）
3. `Xg9WNRg8`（USA/TOP2000，2Y 5.46 全表最高）
4. `xAr1YZQb`（EUR，margin 0.00169，EUR 唯一席）
5. `2rAOGKow`（IND，S/F 双高，但 TO 0.277 拖费后）
6. `P0oM2P8L`（DEU，倍率 1.62 最高，适合空档投）
7. `xAr1Y5gg`（USA/TOP1000，prod 最安全但收入序倒数第 2）
8. `GrWdQNq0`（GLB，**建议剔除**：margin 0.0004 / TO 0.286 / F 1.58）

**每颗提交前强制动作**：
- `check_correlation(alpha_id=..., correlation_type="production", refresh=True)`（台账 48h 作废）
- 停掉后台 `sa_run.py` 批次（并发会导致 `_probe_prod_max` ProxyError）
- 等满 flip 窗 ~250s 后 `tools/super_build.py status --alpha-id <id>` 确认 `status=ACTIVE`

### 8.4 提交命令（仅在用户点名后执行）

```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id <ID> --region <REGION>
```

---

## 九、算子充分利用审查

### 9.1 平台算子作用域

| 作用域 | 算子数 | 说明 |
|---|---|---|
| **全部** | **103** | `get_operators` |
| **COMBO** | **101** | 仅 `in` / `universe_size` 不可用 |
| **SELECTION** | **27** | `add multiply sign subtract log max abs divide min signed_power inverse sqrt reverse power or and not is_nan less equal greater if_else not_equal less_equal greater_equal in universe_size` |
| REGULAR | 84 | 普通 alpha 表达式 |

### 9.2 本轮实际利用率

| 维度 | 本轮用到的算子 | 用量 | 利用率 |
|---|---|---|---|
| combo | `generate_stats` `self_corr` `if_else` `reduce_max` `reduce_avg` `subtract` `multiply` | **7 / 101** | **6.9%** |
| selection | `add` `multiply` `greater` `subtract` `less` | **5 / 27** | **18.5%** |
| **合计去重** | 上述 10 个（无重叠） | **10 / 103** | **9.7%** |
| 对比 11-04 | +`reduce_avg` +`less` | 10 → 10（换掉 2 个） | 持平 |

### 9.3 未用能力（按 ROI 排序，附本轮实证校正）

| 优先级 | 算子/字段 | 作用 | 本轮/历史实证 |
|---|---|---|---|
| ~~⭐×3~~ | ~~selection 的 `prod_correlation` 加权~~ | — | **已证伪（11-04）**：硬截断把分散组件筛掉，prod 反升 0.79–0.88 |
| ⭐×3 | `reduce_ir` / `reduce_norm` / `reduce_skewness` / `reduce_stddev` / `reduce_range` / `reduce_percentage` 等余下 10 个 | 权重压缩替代方式 | **本轮 `reduce_avg` 实测 self 0.9938 ⇒ 不支持「换 reduce_* 能换席」**。它们只能当 prod 微调（±0.03 量级），**不是开席杠杆** |
| ⭐×2 | selection 的 `author_sharpe` / `author_returns_to_drawdown` | 组件质量筛选 | **未测**。`author_fitness≥2` 已确认组件不足 10 颗；这两个字段分布未知，**下一轮值得单测**（成本 1 槽） |
| ⭐×2 | selection 的 `datasets` / `category` | 按数据集/类别选组件子集 | **未测**。理论上是最能改变子集结构的字段 ⇒ **最可能产生真新席**，优先于 `reduce_*` |
| ⭐×2 | selection 的 `neutralization`（已提交 SA 用过 `neutralization == "COUNTRY"`） | 按组件中性化族筛选 | 已被 MEA 的 `78jYpn0Z` 用过一次，说明语法可行；**未在本账户主区试过** |
| ⭐ | `combo_a(alpha, nlength, mode)` | 平台内置组合器 algo1/2/3 | 历史 4 颗用过；本轮未试 |
| ⭐ | `ts_target_tvr_decay` / `ts_target_tvr_hump` / `hump` | 把换手打到目标区间 | C 档要 TO 0.20–0.27，本轮候选 0.07–0.29（`1YNjX03W` 只 0.072）⇒ 有定向空间 |
| ⭐ | `vector_neut` / `winsorize` / `tail` / `quantile` | 权重整形 / 正交 | `rank(w)` 已撞墙（11-04 prod 0.7116）；`winsorize(w,0.01,0.99)` 未试 |

### 9.4 结论

**本轮组建仍未充分利用平台算子：10/103 = 9.7%。** 但**「多用一个算子」本身不产生价值**，本轮已经把「算子多样性 → 新席」这条假设证伪了两条：

1. `reduce_avg`（新算子）→ self 0.9938，**同席**；
2. `TO<0.18`（新阈值）→ self 1.0000，**同席**。

**真正有效的开席杠杆只有三条**（按实测强度）：
① **改 selection 的筛选字段/阈值到「结构不同」的位置**（`turnover` 0.22 → 0.10 有效；0.22 → 0.18 无效）；
② **换 universe**（USA TOP3000/TOP2000/TOP1000 = 0.26–0.42，可容 3 席）；
③ **扩池**（DEU 11→13 使 prod 0.6923→0.5522）。

下轮最高 ROI 的单条实验：**selection 加 `datasets` 或 `category` 过滤**（唯一还没被试过的「改变组件构成」的字段），目标区 IND/TOP500 与 USA/TOP3000。

---

## 十、★ 收入口径：SUPER 到底能拿多少钱，该怎么排序

### 10.1 账户当前收入结构（`get_daily_and_quarterly_payment` 实测，2026-11-05）

| 项 | 数值 |
|---|---|
| 昨日 base payment | **$1.59** |
| 本季（2026-11-01 ~ 12-31）累计 | $4.50 |
| 上季（2026-09-01 ~ 10-31） | **$85.32** |
| YTD（2026-01-01 ~ 11-03） | **$136.69** |
| 全部累计（2025-08-05 起） | $142.20 |
| other_payments（竞赛/季度/推荐） | **$0.00** |

- 日 base payment 在 **$1.20–1.94** 区间波动（近 90 个交易日），τ 中位约 $1.6/日。
- 该金额是**账号级合计**，API 不给单颗 alpha 拆分 ⇒ **无法直接回归「哪颗 SA 赚了多少」**。
- 参照量级：46 颗 SUPER + 229 颗 ACTIVE REGULAR ⇒ 平均每颗 OS alpha 约 **$0.006/日**。**一颗新 SUPER 的边际日收入是「分级」量级，不是「美元」量级。**

### 10.2 收入的三个乘数（可查、可操作）

| 乘数 | 机制 | 本账户现状 | 能否在 IS 阶段优化 |
|---|---|---|---|
| **① OS 表现** | 平台按**样本外**费后表现计费 | **完全不可预览**（见 §10.3） | 只能靠 IS 代理 |
| **② pyramid 倍率** | 区域 × 类别 × delay 倍率直接乘收入 | DEU 1.62 / GBR 1.41 / KOR 1.39 / EUR 1.20 / GLB 1.19 / USA 1.16 / IND 1.14（D1 均值） | ✅ 选点时可算 |
| **③ osmosis 点数** | **每 scope（region×delay）独立 100,000 点**，非共享池 | 当前 **6 个 scope × 100,000 = 600,000**，129 颗（SUPER 21 颗 ≈88k / REGULAR 108 颗 ≈512k），全部精确对齐 ✓ | ✅ 提交后可调（周锁） |

> **★★★ 修正（2026-11-05 10:00 平台文档复核）**：osmosis **不是**「全局 500k 共享池」。真实规则是**每个 scope（region × delay）各自必须恰好 100,000 点**，至少 3 个 scope。账户 11-04 09:25 测得 500k = 当时 5 个 scope；11-04 23:12 扩到 6 个 scope（+USA）= 600k。**新增 scope 会真的增加总暴露**，新增 SA 只是 scope 内部的重新分配。
> **点数周锁**：每周日 23:59 EST 锁定，**7 天后**用于每日组合计算（例：11-08 周日锁 → 11-15~11-21 生效）。有约 10 天延迟，**不要频繁大改**。
> **收入路径**：① 每日 base payment 的 theme multiplier；② **Daily Osmosis Rank**（各 scope 当日 PNL 在全体顾问中排名 → 取已分配 scope 的平均 → **质量乘数 1–2，逐日更新**）；③ Combined Osmosis Performance（季度支付 + Genius 资格，需 3 个月内 ≥6 周正确分配）。
> **组合 PNL 用的是「2 年前开始的 out-sample」窗口** ⇒ **近期表现不影响 rank，历史稳健性主导**。这与 SA 选点看 2Y IS 的逻辑不同，别混用。
> ⇒ **收入最大化的第一杠杆是「scope 选择」而不是「sa 分层」**：rank 只平均已分配的 scope，加一个排名差的 scope 会**拉低**整体乘数。

### 10.3 OS 表现不可预览 —— 两条实测证据

1. **`GET /alphas/{id}` 的 `os` 段只有 `startDate`**（实测 `KPGvRMg1`：`"os": {"startDate": "2024-01-01"}`），**没有任何 OS Sharpe / turnover / margin**。`batch_get_alpha_metrics` 同理。⇒ 无法对历史 46 颗做「IS→OS 衰减」回归。
2. **`componentActivation=OS` 在默认窗口下不可用**：本轮 8 颗全部改 OS 激活后，首条（`0mYjjPl8`，USA/TOP1000）返回 **S 0.0 / TO 0.0 / self 0.0**。原因：组件 OS 起点为 **2024-01-01**，而 SA 仿真窗口是 **2014-01-01 ~ 2023-12-31** ⇒ **OS 区间完全落在窗口外，无重叠数据**。
   ⚠ **平台文档推荐的「切 OS 激活做 reality check」在本账户不成立**（除非 SA 设置能把窗口推到 2024+，当前 `sa_run.py` 的 payload 无此字段）。**这条别再试了**。

### 10.4 可用的收入代理（按与 OS 的相关性排序）

| 代理 | 为什么更接近 OS | 本表谁占优 |
|---|---|---|
| **2Y ladder Sharpe** | 最近 2 年 IS 切片，是全部可得指标里离未来最近的一段 | `Xg9WNRg8` 5.46 |
| **margin** | 费后每笔收益，OS 阶段衰减最慢；高 TO + 低 margin 的组合在 OS 最先失效 | `1YNjX03W` 0.00328 |
| **Fitness** | 已内含 S 与 returns/TO 的权衡，比裸 S 抗噪 | `9qxVG66r` 4.55 |
| region D1 倍率 | 直接乘收入 | `P0oM2P8L`（DEU 1.62） |
| ~~裸 S~~ | 最易被单一行情段撑起；组件在 IS 期被高权重叠加（平台文档明示的 feedback loop） | 不作主判据 |

**排序式（序数用）**：`Score = 2Y × F × margin × D1均值`，结果见 §1.2。

### 10.5 实操建议（收入最大化的动作顺序）

1. **先按收入序提交**（§1.3），被 prod 闸拦下不消耗配额，直接降级到下一颗。
2. **提交后 30 天内盯 OS**：平台不提供预览，但提交后有 `os` 段（仍只有 startDate）⇒ 只能从 **日 base payment 的变化**反推（提交前后各记一次 `get_daily_and_quarterly_payment` 的 7 日均值）。
3. **点数再分配才是收入主杠杆**：新 SA 的 10,000 点上限要从低效 alpha 身上挪。当前 SUPER 均 2,178 点、REGULAR 均 1,756 点 ⇒ 优先把点数集中到 **2Y 高 + margin 高** 的那几颗（本表 `Xg9WNRg8` / `1YNjX03W` / `9qxVG66r`）。
4. **不要为「收入」牺牲 RA 主线**：新增一颗 SA 的边际日收入是分级量级，而 RA 的 4/天/区配额和金字塔塔位才是主产出。

---

## 十一、Osmosis 现状与收入最大化（2026-11-05 10:00 复核）

### 11.1 平台硬规则（`osmosis-allocation-guide-consultants` 原文，7 条）

| # | 规则 | 细节 |
|---|---|---|
| 1 | **scope = region × delay** | 只能选 Genius 等级允许的组合 |
| 2 | **每 scope 恰好 100,000 点** | 不是「上限」，是「必须等于」；差 1 点即无效 |
| 3 | **每 scope ≥10 颗 alpha** | 单颗无下限 ⇒ 10 颗可以 90,001 + 9×1,111 |
| 4 | **≥3 个 scope** | 少于 3 个不参与 |
| 5 | **周锁** | 周日 23:59 EST 锁定 → **7 天后**用于每日组合计算（≈10 天生效延迟） |
| 6 | **组合 PNL 窗口 = 2 年前的 out-sample** | **近期表现不参与排名**，历史稳健性主导 |
| 7 | 可分配对象 | REGULAR / ATOM / POWER_POOL / **SUPER** 均可；任意提交日期 |

**三种收入路径**：
1. **daily base payment 的 theme multiplier**（组合 PNL 表现 → 乘到日付）；
2. **Daily Osmosis Rank**：各 scope 当日 PNL 在全体顾问中排名 → 取**已分配 scope 的平均** → **质量乘数 1–2**，逐日更新；
3. **Combined Osmosis Performance**：季度支付 + Genius 资格（需 3 个月内 ≥6 周正确分配）。

> **规则 2 与规则「rank 只平均已分配 scope」合起来给出核心结论**：
> - 加 scope = 真增加 100k 暴露，但**同时**把自己的平均排名往该 scope 的排名拉 ⇒ **只有「该 scope 排名能进前列」才值得加**。
> - scope 内部是零和的（固定 100k），调点数**不改变总暴露**，只改变「这个 scope 押在谁身上」。

### 11.2 现状（平台实测，`balance_osmosis.py` 只读复核 2026-11-05 10:05）

| scope | 颗数 | 实际点数 | 达标 | 构成 |
|---|---|---|---|---|
| USAD1 | 24 | 100,000 | ✓ | SA 4 颗 22,000 + RA 20 颗 78,000 |
| INDD1 | 24 | 100,000 | ✓ | SA 4 / 22,000 + RA 20 / 78,001 |
| KORD1 | 24 | 100,000 | ✓ | SA 4 / 22,000 + RA 20 / 78,000 |
| GBRD1 | 24 | 100,000 | ✓ | SA 4 / 22,000 + RA 20 / 78,000 |
| GLBD1 | 19 | 100,000 | ✓ | SA 4 / 22,001 + RA 15 / 77,999 |
| DEUD1 | 14 | 100,000 | ✓ | SA 1 / 10,000 + RA 13 / 90,000 |
| **合计** | **129** | **600,000** | **6/6 ✓** | SUPER 21 颗 ≈88k（14.7%）/ REGULAR 108 颗 ≈512k |

**未启用 scope**：

| scope | ACTIVE 可用 | 未启用原因 | 价值判断 |
|---|---|---|---|
| EURD1 | **21** | 上轮未纳入 | 唯一「池够深却没启用」的 scope ⇒ **最大未开发项** |
| MEAD1 | 19 | 平台已关闭该 region，新建受阻（存量 alpha 仍可用） | 可配点但无法补新血，长期退化 |
| ASID1 | 9 | 差 1 颗到 10 | 提交 1 颗 ASI RA 即可开 |
| HKGD1 | 7 | 差 3 颗 | 提交 3 颗 HKG RA 即可开 |

**新提交未分配**：`1YNjX03W`（USA/TOP3000，2026-11-05 提交）当前 **0 点**；USA 已有 4 颗 SA 占 22,000，需重新切分或替换。

### 11.3 现行分配算法（`osmosis_plan_v2.py`，2026-11-04 23:12 应用参数）

| 环节 | 规则 |
|---|---|
| 候选 | ACTIVE REGULAR（+ 每 scope topN SUPER） |
| 硬闸 | `inv < 1.0` 剔｜`(is-inv)/is ≥ 60%` 剔（投研约束下衰减过多）｜`TO > 20%` 且 `inv < 1.5` 剔 |
| SA 池 | 每 scope 按 inv 取 **top4**；预算 **22%**；单颗 ≤ **10,000**（占 scope 10%，仓库策略非平台明规） |
| 相关性剪枝 | 池内日收益 `ρ ≥ 0.70` 丢弃；`0.60 ≤ ρ < 0.70` 保留但权重 ×0.5（PnL 20h 缓存） |
| 容量 | 每 scope ≤ 20 RA + 4 SA；不足 10 颗时回补被丢者（权重 ×0.25，标记 forced） |
| 收尾 | `trim` 到恰好 100,000；`balance_osmosis.py` 复核差额 |

### 11.4 与官方最佳实践的 3 个差距

| # | 官方建议 | 现状 | 影响 |
|---|---|---|---|
| 1 | `Diversify across scopes: use more than the bare minimum of 3` | 已 6 个（好），但 **EUR 21 颗未启用** | 少一个可能的正贡献 scope；但若 EUR 排名差，加了反而拉低平均 ⇒ **需先估排名** |
| 2 | `Exclude Alphas whose Sharpe declines ≥60% after investability` | v2 已执行 ✓ | — |
| 3 | `Classify by turnover <10% / 10–20% / >20%; avoid >20% unless inv robust` | v2 剔了 `TO>20% ∧ inv<1.5`，但 `TO>20% ∧ inv≥1.5` 仍全量保留 | 高换手 alpha 在 2 年前 OS 窗口里的费后表现会被高估 ⇒ 排名虚高、实盘衰减 |
| 4 | `Diversify across datasets / operators / neutralizations` | v2 只做 PnL 相关剪枝，**未按数据集/中性化分桶配额** | 相关剪枝只能去掉数值冗余，去不掉「同一数据集+同一算子」的共因风险 |

### 11.5 最大化方案（按 ROI 排序）

| 优先 | 动作 | 预期收益 | 成本/风险 |
|---|---|---|---|
| **A** | **启用 EURD1 第 7 个 scope**（21 颗可用） | +100k 暴露；若 EUR 组合排名进入前 1/2，直接抬 Daily Osmosis Rank | 若 EUR 排名在后 1/2，**拉低平均乘数**。**判据**：先用 USD/IND 同类「2 年前 OS」口径做一次内部估算，或小步试配 3 周看 rank 变化 |
| **B** | **USA scope 内部重切，让 `1YNjX03W` 进池** | 它 margin 0.00328 / TO 0.072 是全池最优费后项之一 ⇒ 提升 USA 组合费后 Sharpe | 必须从现有 4 颗 SA 或 20 颗 RA 里挤 10k；**USA 是 6 个 scope 里最可能排名靠前的**，改动要保守 |
| **C** | **高 TO（>20%）alpha 降权**（仅保留 inv≥1.5 的少数） | 修正「2 年前 OS 窗口里高换手被高估」的系统偏差 | 会减少可选颗数；EUR/USA 池深无碍，DEU(13) 可能跌破 10 颗 ⇒ **DEU 不能动** |
| **D** | ASI 补 1 颗 RA / HKG 补 3 颗 RA | 各开一个 100k scope | ASI/HKG 池太浅（9/7），10 颗里 9 颗都是低质量 ⇒ **大概率拉低平均，不建议只为「多一个 scope」而开** |

**执行节奏**：osmosis **周锁（周日 23:59 EST）+ 7 天生效** ⇒ 现在改 → 11-08 锁 → **11-15 起生效**。一次只动 1 个 scope、观察 2–3 周，官方明确反对「frequent radical reshuffles」。

### 11.6 待用户决策

1. **EURD1 要不要开**（A）—— 需要一次约 20–30 分钟的估算（用 2 年前 OS 窗口内部比排名）。
2. **`1YNjX03W` 在 USA scope 拿多少点**（B）—— 建议 8,000–10,000，从 USA 现有 4 颗 SA 里各削 2,000–2,500（保留 ≥10 颗 RA 不动）。
3. **是否执行 C**（高 TO 降权）—— 只影响 USA/IND/KOR/GBR/GLB，DEU 例外。

---

## 附录 A：本轮扫描日志索引

| 文件 | 内容 |
|---|---|
| `results/sa_probe_cache.json` | 组件池 + 46 SUPER 全量（2026-11-05 07:44 refresh） |
| `results/sa_scan_20261105/configs_A~C.json` | 本轮 18 个配方 |
| `results/sa_scan_20261105/res_A~C.jsonl` | 逐条指标 + 双闸 |
| `results/sa_scan_20261105/run_A~C.log` | 完整仿真/探针日志 |
| `results/sa_scan_20261104/*` | 11-04 的 16 个有效结果（本报告引用的 `Xg9WNRg8`/`A1V0L9KQ`/`2rAOGKow`/`9qxVG66r`/`GrWdQNq0`/`0mYpnMr1`/`QPv3Ww9p`/`A1V0LZkg` 均出于此） |

## 附录 B：与 11-04 方案的差异

| 项 | 11-04 | 11-05（本轮） | 变化原因 |
|---|---|---|---|
| 首选 | `A1V0eZne`（USA/TOP3000, S 6.39/F 7.06） | **`xAr1Y5gg`（USA/TOP1000, prod 0.4777）** | `A1V0eZne` 已于 11-03 提交 ACTIVE，该席关闭 |
| USA 席数 | 3（候选） | **3（全部互测 0.26–0.42）** | `1YNjX03W` 用 `TO<0.10` 新开 TOP3000 席 |
| DEU | 停投（prod 0.6923，余量 0.008） | **可投（0.5522，余量 0.148）** | 池 11→13 + `TO<0.22` |
| GBR | 可投（`QPvGdLYQ` 待提交） | **停投** | `QPvGdLYQ` 已 ACTIVE，CROWDING 0.7486 无第二席 |
| EUR 首选 | `A1V0LZkg`（prod 0.6391） | **`xAr1YZQb`（prod 0.6007）** | 加 `TO<0.22`，S −0.21 / prod −0.038 |
| GLB | l15（prod 0.5864） | l15（不变），**l12 判死（2Y 1.14）** | 首次试 l12 |
| KOR | cp7（0.6370） | cp7（不变），**`TO<0.22` 判无效** | 逐位相同 |
| 降 prod 杠杆 | `TO<0.22`（−0.169） | **`TO<0.10`（换席，+0.07 prod @USA/TOP3000）** | 0.10 换子集，0.18 不换 |
| 开席判据 | region × selection | 不变，**但 selection 阈值必须跨过「组件 TO 分布」的断点** | 本轮 4 组同席证据 |

---

## 附录 C：提交记录

### C.1 `1YNjX03W` — USA/TOP3000（2026-11-05 09:31 GMT+8 提交成功）

| 项 | 值 |
|---|---|
| 配方 | SLOW d1 l10 cp1 + selection `(1-self)*(turnover<0.10)` |
| 名称（自动） | `USA_S_10comp_NjX03W` |
| prod 闸（提交前实时 probe） | **0.6821** < 0.7 → 过闸（attempts=2，空体后第 2 次出数） |
| 提交层 precheck | HTTP 404（非 403 ⇒ 无 BLOCKED） |
| POST 结果 | **HTTP 201 Accepted (async)** |
| 翻转确认 | **`status=ACTIVE`**（~250s 后复核） |
| 提交后全闸 | `LOW_SHARPE` 4.57/1.58 ✅｜`LOW_FITNESS` 4.44/1.0 ✅｜`LOW_TURNOVER` 0.072/0.02 ✅｜`HIGH_TURNOVER` 0.072/0.4 ✅｜`CONCENTRATED_WEIGHT` PASS ✅｜`LOW_SUB_UNIVERSE_SHARPE` 2.16/1.98 ✅｜`IS_LADDER_SHARPE` 4.23/2.02 ✅｜`CLUSTER_TEST` 2.68/1.58 ✅ |

命令（可复现）：

```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe -u \
  tools/super_build.py submit --alpha-id 1YNjX03W --region USA \
  --selection-limit 10 --neutralization SLOW
# 等 ~250s 翻转窗后复核：
... tools/super_build.py status --alpha-id 1YNjX03W
```

> ⚠ **它是 USA/TOP3000 的 `TO<0.10` 新席**，与已提交的 `A1V0eZne`（`TO<0.22`，SLOW）不同席 —— 提交前 self 实测 0.5632。该槽位现共 6 颗 SUPER。
> ⚠ **osmosis 点数未动**：新 SA 默认 0 点，需另行分配（SUPER 单颗上限 10,000，池 500,000）。**收入要真正落地，这一步必须做**（见 §10.2 / §10.5）。

---

**报告结束。除 `1YNjX03W`（用户点名）外，其余 7 颗为待执行配方，未提交。**
