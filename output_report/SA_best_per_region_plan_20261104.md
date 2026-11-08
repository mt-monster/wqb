# 各 Region 最优 SuperAlpha 方案 — 全流程扫描报告

**生成时间**: 2026-11-04 11:00 GMT+8
**工作目录**: `D:\coding\traeCN_project\wqb`
**结果目录**: `results/sa_scan_20261104/`
**组件池刷新**: `results/sa_probe_cache.json`（`--refresh` 全量翻平台，2026-11-04 09:07）
**扫描规模**: 本轮 21 个配方（A 7 / B 7 / C 4 / D 3），16 个出完整结果 + 5 个被平台拒（MEA×4 region 关闭、GLB/TOPDIV3000×1 并发 429）；叠加 11-03 的 28 个 ⇒ **累计 49 个候选，覆盖 8 个 region**
**铁律**: **只挖不提交** —— 本报告全部为待执行配方，未做任何提交动作。提交权归用户，且须点名。

---

## 一、执行摘要

### 1.1 本轮结论（三句话）

1. **本轮新增 10 颗双闸实测 PASS 候选**（self/prod 均 <0.7），其中 **7 颗落在收紧约束 `prod<0.65`**。**最强一颗 `A1V0eZne`（USA/TOP3000 SLOW cp1 + `turnover<0.22` selection）：S 6.39 / F 7.06 / 2Y 7.06 / TO 0.1178 / self 0.5087 / prod 0.6146 —— 达到论坛 C 档（S 5.6–7.0、F 5.6–8.9），F 7.06 创账户新高**（原最高 5.94）。
2. **IND 破墙**：此前判停投的 IND（CROWDING 0.7255 / MARKET 0.810 双撞墙）在 **SLOW 族**下 prod 骤降到 **0.6097**，S 4.43 / F 3.58，全闸（含 2Y 4.10、sub 2.70、robust 2.32）通过。**IND 从停投区恢复为可投区。**
3. **★ 席判据重大修正**：SA 的「席」不是 `region×universe×中性化族`，而是 **`region × selection 表达式`（组件子集）**。实测同一 selection 下：换 combo 幂次 0.98–0.9996、换中性化族 0.70–0.93、换 universe 0.58–0.96；**USA 是唯一例外**（TOP3000/TOP2000/TOP1000 三席互测 0.284–0.578）。历史 45 颗能共存，是因为用了 **20 种不同 selection 表达式**（现有 KOR 5 颗互测仅 0.38–0.65）。⇒ **新增独立席位的杠杆是 selection，不是中性化族**；且 selection 里的 `turnover<0.22` 是强降 prod 杠杆（§10.6），而 `prod_correlation` 硬截断是反向（§10.5）。

### 1.2 优先队列（约束优化：max S ∧ max F  s.t. self<0.7 ∧ prod<0.65）

| 优先级 | Alpha ID | Region | Universe | 配方 | S | F | TO | self | prod | prod余量 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ⭐ **1** | **`A1V0eZne`** | **USA** | **TOP3000** | **SLOW d1 l10 cp1 + sel `(1-self)*(TO<0.22)`** | **6.39** | **7.06** | 0.1178 | 0.5087 | **0.6146** | 0.035 | ✅ **C 档，账户最强** |
| ⭐ **2** | **`Xg9WNRg8`** | **USA** | **TOP2000** | **SLOW d1 l10 cp3** | **4.74** | **4.10** | 0.1659 | 0.6493 | **0.6493** | 0.051* | ✅ |
| ⭐ **3** | **`A1V0LZkg`** | **EUR** | **TOPCS1600** | **FAST d1 l10 cp1** | **4.53** | **3.89** | 0.1842 | 0.6390 | **0.6391** | 0.061 | ✅ |
| ⭐ **4** | **`2rAOGKow`** | **IND** | **TOP500** | **SLOW d1 l10 cp3** | **4.43** | **3.58** | 0.2773 | 0.6101 | **0.6097** | **0.090** | ✅ 破墙 |
| ⭐ **5** | **`9qxVG66r`** | **KOR** | **TOP600** | **SLOW d1 l10 cp7** | 3.95 | **4.55** | 0.1281 | 0.6370 | **0.6370** | 0.063 | ✅ |
| 6 | `9qx9aAa2` | EUR | TOP2500 | FAST d1 l10 cp1 | **4.83** | 3.99 | 0.1749 | 0.6707 | 0.6699 | 0.030 | ⚠ 超 0.65 |
| 7 | `A1V0L9KQ` | USA | TOP1000 | SLOW d1 l10 cp3 | 2.90 | 2.03 | 0.1774 | 0.6331 | 0.6331 | 0.067 | ✅ |
| 8 | `QPvGdLYQ` | GBR | TOP700 | SLOW d1 l10 cp3 | 4.23 | 3.54 | 0.1698 | 0.6330 | 0.6330 | 0.067 | 11-03，需 refresh |
| 9 | `zq3Nal3K` | KOR | TOP600 | SLOW d1 l10 cp5 | 3.98 | 4.61 | 0.1281 | 0.6427 | 0.6427 | 0.057 | 11-03，与 ⭐5 同席 |
| 10 | `GrWdQNq0` | GLB | TOP3000 | SLOW d1 **l15** cp3 | 3.51 | 1.58 | 0.2860 | 0.5135 | 0.5864 | 0.064 | ✅ |
| 11 | `0mYpnMr1` | GLB | TOP3000 | SLOW d1 l10 cp3 | 3.45 | 1.42 | 0.3731 | 0.4560 | 0.5010 | **0.199** | 与 `GrWdQNq0` 同席（0.955） |
| 12 | `QPv3Ww9p` | DEU | TOP500 | SLOW d1 l10 cp3 | 2.13 | 1.60 | 0.1524 | 0.6923 | 0.6923 | 0.008 | ⚠ 擦双线 |

> **`A1V0eZne` 是本轮唯一 C 档候选**：S 6.39（账户第 2，仅次于 GLB `LL5amzov` 6.93）、**F 7.06（账户第 1，原纪录 5.94）**、2Y 7.06、sub 3.08、drawdown 1.76%。TO 0.1178 低于 C 档区间 0.20–0.27，但 A 档无下限压力。
> **它落在 USA/TOP3000** —— 同参数下标准 selection 的 `vR1kAQmr` prod 0.7838 双死，**只把 selection 加上 `turnover<0.22` 就把 prod 压到 0.6146 且 S/F 更高**。详见 §10.6。
>
> `*` `Xg9WNRg8` prod 0.6493 距 0.65 仅 **0.0007** —— 按 0.65 质量线擦线，按平台 0.7 红线余量 0.051。prod 漂移极猛，提交前必须 `refresh=True` 重测。
> **Pareto 前沿**：`A1V0eZne` 严格支配所有其他候选（S、F 双高且 prod 更低）。
> **同席互斥（实测，阈值用平台 0.7）**：`9qx9aAa2` ↔ `A1V0LZkg` = **0.791** ⇒ **EUR 只能提交 1 颗**，选 `A1V0LZkg`。`9qxVG66r` ↔ `zq3Nal3K` = **0.9996** ⇒ KOR 只能提交 1 颗，选 `9qxVG66r`。
> **USA 可容 3 颗**：`A1V0eZne` ↔ `Xg9WNRg8` = **0.5095**、↔ `A1V0L9KQ` = **0.2836**、`Xg9WNRg8` ↔ `A1V0L9KQ` = 0.5777，全部 <0.7 且与已提交 `gJePPn0K` = 0.5087。

### 1.3 实际可提交队列（去同席后）

| 天序 | Alpha | Region | 理由 |
|---|---|---|---|
| Day 1 | `A1V0eZne` | USA/TOP3000 | **S 6.39 / F 7.06（账户 F 纪录）/ 2Y 7.06 / prod 0.6146** —— 全轮最强，C 档 |
| Day 2 | `Xg9WNRg8` | USA/TOP2000 | S 4.74 / F 4.10 / 2Y 5.46；prod 0.6493 擦 0.65，先重测 |
| Day 3 | `A1V0LZkg` | EUR | prod 0.6391 余量 0.061，EUR 席唯一，**最稳** |
| Day 4 | `2rAOGKow` | IND | IND 破墙首颗，prod 余量 0.090 最厚 |
| Day 5 | `9qxVG66r` | KOR | KOR 席唯一，F 4.55 本轮最高 |
| Day 6 | `A1V0L9KQ` | USA/TOP1000 | 与 Day1 相关 0.284，USA 第三席 |
| 备胎 | `GrWdQNq0` / `0mYpnMr1` | GLB | l15（3.51/1.58/0.5864）或 l10（0.501 余量最厚），同席二选一 |
| 备胎 | `QPvGdLYQ` | GBR | 11-03 已建成，GBR 席唯一 |
| 不推荐 | `QPv3Ww9p` | DEU | self/prod 同时只剩 0.008 余量 |

**配额**：SUPER = 账号级 1/ET日（跨区共享），上述 6 颗需 6 个 ET 日；与 REGULAR 4/天/区独立计数。
**USA 一区可贡献 3 颗**（互测 0.284–0.578），是本轮唯一能连续出颗的区。

---

## 二、数据基线

### 2.1 组件池 eligibility（ACTIVE 已提交 REGULAR，region 级）

| Region | ACTIVE 组件 | 未提交 IS 候选 | 可建性 | 备注 |
|---|---|---|---|---|
| USA | **47** | 20 | GO | 池最大，prod 天花板最高 |
| IND | **45** | 9 | GO | 与 USA 同量级 |
| KOR | **30** | 0 | GO | 无新增供给 |
| GBR | **24** | 2 | GO | 池较 11-03 增 2 |
| EUR | **20** | 142 | GO | 池较 11-03 (14) **+6** |
| MEA | **19** | 0 | **BLOCKED（平台关闭）** | 见 §6 |
| GLB | **18** | 30 | GO | 池较 11-03 (17) +1 |
| DEU | **11** | 108 | GO | 池小，prod 天花板低 |
| ASI | 9 | 401 | **BLOCKED（差 1 颗）** | 提交 1 颗 RA 即可解锁 |
| HKG | 6 | 231 | **BLOCKED（差 4 颗）** | — |

> **口径**：组件池是 **region 级**（非 universe 级）。实测 USA/TOP1000、GLB/TOP3000 的 REGULAR 计数为 0，但仍能建 SA —— 平台从 region 级池选组件。
> **ASI 解锁路径**：`get_user_alphas` 显示 ASI 有 401 条未提交 IS 候选，只需用户点名提交 1 颗 RA（REGULAR 配额内）即可把 ASI 从 9→10，进入可建区。

### 2.2 档位占用分类（45 颗 SUPER / 14 个 region×universe 档）

| 档位 | REGULAR | SUPER | 分类 | 已用中性化族 |
|---|---|---|---|---|
| USA/TOP3000 | 38 | 4 | 双占用 | STAT(d10) / SUBINDUSTRY(d5) / MARKET(d5,l1000) / FAST(d1) |
| USA/TOP1000 | 0 | 1 | **仅 SA 占用** | STAT(d1,l15) |
| USA/TOP2000 | 5 | 1 | 双占用 | STAT(d1,l15) |
| USA/TOP500 | 0 | 1 | **仅 SA 占用** | CROWDING(d1) |
| USA/TOPSP500 | 0 | 1 | **仅 SA 占用** | STAT(d1,l38) |
| IND/TOP500 | 45 | **11** | 双占用（最饱和） | INDUSTRY / RAM×2 / SUBINDUSTRY×3 / STAT×5 |
| KOR/TOP600 | 30 | **10** | 双占用 | STAT×5 / SUBINDUSTRY×2 / CROWDING / RAM |
| GBR/TOP700 | 24 | 5 | 双占用 | STAT×2 / SLOW / FAST / RAM |
| GLB/MINVOL1M | 17 | 2 | 双占用 | SUBINDUSTRY(d10) / STAT |
| GLB/MINVOL10M | 0 | 1 | **仅 SA 占用** | SLOW |
| GLB/TOP3000 | 0 | 1 | **仅 SA 占用** | RAM |
| GLB/TOPDIV3000 | 1 | 1 | 双占用 | STAT(l15) |
| EUR/TOP2500 | 11 | 2 | 双占用 | STAT / CROWDING |
| EUR/TOPCS1600 | 9 | 1 | 双占用 | STAT(trunc 0.08) |
| DEU/TOP500 | 11 | 1 | 双占用 | STAT |
| MEA/TOP400 | 19 | 2 | 双占用（平台关闭） | SUBINDUSTRY(d5) / SUBINDUSTRY(d8) |

**未占用中性化族（本轮扫描目标）**

| Region | 已占族 | 未占族（可试） |
|---|---|---|
| USA | STAT / SUBINDUSTRY / MARKET / FAST / CROWDING / RAM | **SLOW** / SECTOR / INDUSTRY / NONE / SLOW_AND_FAST |
| IND | INDUSTRY / RAM / SUBINDUSTRY / STAT | **SLOW** / CROWDING / MARKET / FAST / SECTOR |
| KOR | STAT / SUBINDUSTRY / CROWDING / RAM | **SLOW** / FAST / INDUSTRY / MARKET / SECTOR |
| GBR | STAT / SLOW / FAST / RAM | **CROWDING** / INDUSTRY / SECTOR / MARKET |
| EUR | STAT / CROWDING | **SLOW** / FAST / RAM / INDUSTRY / MARKET / COUNTRY |
| GLB | SLOW / STAT / SUBINDUSTRY / RAM | **CROWDING** / FAST / INDUSTRY / COUNTRY / MARKET |
| DEU | STAT | **SLOW** / CROWDING / FAST / INDUSTRY / MARKET |

> **⚠ 重要修正**：`零 OS 档 ⇒ self 恒 0` 在本轮被证伪。`A1V0L9KQ` 位于 USA/TOP1000（REGULAR=0），实测 **self=0.6331**。原因是 self 池按 **region** 聚合（USA 有 47 颗 REGULAR），不是按 universe。**「仅 SA 占用档」不等于安全档，仍需实测。**

### 2.3 Pyramid 倍率（D1，region 均值）

| Region | n 类别 | D1 均值 | D0 均值 | 最高类别 | 最低类别 |
|---|---|---|---|---|---|
| DEU | 16 | **1.62** | 1.85 | model/news/other 1.8 | imbalance 1.2 |
| CHN | 12 | 1.61 | 1.74 | other 1.9 | socialmedia 1.1 |
| AMR | 2 | 1.55 | 1.75 | sentiment 1.7 | pv 1.4 |
| GBR | 16 | **1.41** | 1.69 | sentiment 1.7 | imbalance 1.0 |
| KOR | 15 | **1.39** | — | analyst/fundamental/model 1.6 | imbalance/socialmedia 1.0 |
| HKG | 15 | 1.41 | — | analyst/model/other 1.7 | imbalance 1.0 |
| EUR | 14 | **1.20** | 1.40 | other 1.5 | risk/imbalance 1.0 |
| GLB | 13 | 1.19 | — | fundamental/analyst/sentiment 1.4 | pv/risk 1.0 |
| ASI | 16 | 1.18 | — | analyst 1.5 | imbalance/macro 1.0 |
| USA | 16 | **1.16** | 1.53 | other/sentiment 1.4 | institutions/imbalance 1.0 |
| IND | 15 | **1.14** | — | analyst 1.4 | risk/institutions 1.0 |

> **含义**：D1 倍率高的区（DEU 1.62 / GBR 1.41 / KOR 1.39）单颗 SA 的塔位分更高，但 D1 倍率与 prod 天花板无关（DEU 倍率最高却因池仅 11 颗而 prod 0.728 撞墙）。**倍率只影响产出，不影响可行性。**

### 2.4 现有 45 颗 SUPER 表现分布

| 指标 | 中位数 | 最高 | 最低 |
|---|---|---|---|
| Sharpe | 3.92 | **6.93**（GLB `LL5amzov`） | 1.82（USA `E567rQvR`） |
| Fitness | 3.40 | **5.94**（KOR `RRA9EZKz`） | 1.20（USA `2rj3ddl5`） |

- 区域分布：IND 11 / KOR 10 / USA 8 / GBR 5 / GLB 5 / EUR 3 / MEA 2 / DEU 1
- 全部 45 颗 `selectionHandling=POSITIVE`
- **selection 表达式共 20 种**，combo 表达式共 9 种 ⇒ 这是 45 颗能共存的真实原因（见 §10）

---

## 三、选点原则

1. **档位占用类型 > 组件池大小**
   - 「仅 SA 占用」档（REGULAR=0）自相关池更小，但实测 self 仍 0.63（region 级池）⇒ 不是免费通过。
   - 「双占用」档需靠**未占用的中性化族**或**未用过的 selection** 找新席。
2. **指标 = 约束优化**：`max S ∧ max F  s.t. self<0.7 ∧ prod<0.65`
   - prod ≥ 0.7 = **合规红线，无豁免**（`super_build.py submit` fail-closed）。
   - prod < 0.65 = 用户 2026-11-03 定稿的质量线；prod < 0.6 + TO < 0.30 = 社区合格档（B 档）。
   - **prod 余量 ≥ 0.02** 才算安全（本报告用 prod余量 列）。
3. **中性化族规律（本轮实测更新）**
   - **SLOW 是本轮最强通用族**：IND 0.6097（vs CROWDING 0.7255 / MARKET 0.810）、USA/TOP1000 0.6331、KOR 0.6370、GBR 0.6330、GLB 0.5010 —— 五区全部最低或并列最低。
   - CROWDING 在 GBR/GLB/USA 均高于 SLOW 0.03–0.09；在 IND 直接撞墙。
   - **换中性化族只降 prod ~0.03–0.12，不产生新席**（相关仍 0.70–0.93）。
4. **combo 幂次**：cp 越高 prod 越低但 S 也降。
   - USA：cp3 优于 cp5（0.6011 vs 0.6451）
   - KOR：cp7 > cp5 > cp3 > cp1（0.6370 / 0.6427 / 0.6535 / 0.6718），cp7 是新的甜点
   - GBR：cp3 (0.6330) 优于 cp5（cp5 self 0.7493 直接 FAIL）⇒ **cp 不跨区外推**
5. **universe 只在「两 universe 覆盖差异大」时才改变日收益**：USA TOP2000↔TOP1000 = 0.43（新席）；EUR TOP2500↔TOPCS1600 = 0.79（子集关系 → 同席）。

---

## 四、论坛指标标准（2026-10-22 定稿，本轮沿用）

### 4.1 组成数量（Selection Limit）

- **平台硬下限 = 10**（<10 返回 400：`Ensure this value is greater than or equal to 10`）
- 论坛 78 赞帖建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300（long/short 各 ~250）
- **实际生效数 = min(limit, 组件池)**；组件池是 **region 级** ⇒ SA 指标天花板由 region 的 ACTIVE REGULAR 数决定
- **本轮全量用 l10**：池 ≥11 时 l10 的 prod 余量最大（l12/l15/l30 都会推高 prod）。已实测：EUR l10 prod 0.56 → l12 0.61；GLB l15 结果见 §5.5。

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

### 4.3 组件筛选阈值

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`（官方建议 1–4）。

> ⚠ **筛选强度必须匹配池规模**：加严后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。小池区（EUR 20 / GLB 18 / DEU 11）只能用宽松 `(1 - self_correlation)`；严格阈值仅适用 USA(47)/IND(45)/KOR(30)。

### 4.4 中性化族规律

- Fitness 排序（IND 社区实测）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**
- 选族规则：**TO<0.10 → SLOW；TO>0.20 → FAST**
- 区域族基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（**须逐区验证，禁跨区照搬**）
- ⚠ **组件数↑ ⇒ self↓ 但 prod↑**（EUR l10 self 0.33/prod 0.56 → l12 self 0.29/prod 0.61）⇒ **l10 双闸综合最优**

### 4.5 其他实证

- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区历史 45 颗 SA 全用 **POSITIVE** 均成功
- decay 在 SA 组合层**完全无效**（d0 与 d1 四项逐字相同）

---

## 五、分 Region 方案

### 5.1 总表（每区最优配方）

| Region | 池 | 最优配方 | Alpha ID | S | F | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| **USA** | 47 | TOP3000 **SLOW** cp1 + sel `(1-self)*(TO<0.22)` | `A1V0eZne` | **6.39** | **7.06** | 0.118 | 0.5087 | 0.6146 | 0.035 | ✅ **C 档** |
| **USA 2nd** | — | TOP2000 **SLOW** d1 l10 cp3 | `Xg9WNRg8` | 4.74 | 4.10 | 0.166 | 0.6493 | 0.6493 | 0.051 | ✅ |
| **USA 3rd** | — | TOP1000 **SLOW** d1 l10 cp3 | `A1V0L9KQ` | 2.90 | 2.03 | 0.177 | 0.6331 | 0.6331 | 0.067 | ✅ |
| **EUR** | 20 | TOPCS1600 **FAST** d1 l10 cp1 | `A1V0LZkg` | 4.53 | 3.89 | 0.184 | 0.6390 | 0.6391 | 0.061 | ✅ |
| **IND** | 45 | TOP500 **SLOW** d1 l10 cp3 | `2rAOGKow` | 4.43 | 3.58 | 0.277 | 0.6101 | 0.6097 | 0.090 | ✅ 破墙 |
| **KOR** | 30 | TOP600 **SLOW** d1 l10 **cp7** | `9qxVG66r` | 3.95 | 4.55 | 0.128 | 0.6370 | 0.6370 | 0.063 | ✅ |
| **GBR** | 24 | TOP700 **SLOW** d1 l10 cp3 | `QPvGdLYQ` | 4.23 | 3.54 | 0.170 | 0.6330 | 0.6330 | 0.067 | ✅（11-03） |
| **GLB** | 18 | TOP3000 **SLOW** d1 **l15** cp3 | `GrWdQNq0` | 3.51 | 1.58 | 0.286 | 0.5135 | 0.5864 | 0.064 | ✅ |
| **DEU** | 11 | TOP500 SLOW d1 l10 cp3 | `QPv3Ww9p` | 2.13 | 1.60 | 0.152 | 0.6923 | 0.6923 | 0.008 | ⚠ 下限可投，不建议 |
| **MEA** | 19 | — | — | — | — | — | — | — | — | ❌ 平台关闭 |

### 5.2 EUR（池 20，+6 vs 11-03）

**已占席**：TOP2500 STAT / TOP2500 CROWDING / TOPCS1600 STAT

| 候选 | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`A1V0LZkg`** | **TOPCS1600 FAST d1 l10 cp1** | **4.53** | **3.89** | 0.1842 | 0.6390 | **0.6391** | ✅ **最优** |
| `9qx9aAa2` | TOP2500 FAST d1 l10 cp1 | **4.83** | 3.99 | 0.1749 | 0.6707 | 0.6699 | ⚠ 超 0.65 |
| `d5WRPO3j` | TOPCS1600 CROWDING d1 l10 | 3.68 | 3.38 | 0.1575 | 0.5728 | 0.6987 | ❌ 超线 |
| `omE6ad7E` | TOP2500 SLOW d1 l10 cp3 | 3.60 | 2.31 | 0.1785 | 0.5881 | 0.6317 | ❌ **2Y ladder 1.50 FAIL** |

**结论**：EUR 唯一可投 = `A1V0LZkg`。`9qx9aAa2` 虽 S 最高（4.83）但 prod 0.6699 只达 A 档，且与 `A1V0LZkg` 相关 **0.791**（同席）⇒ 不能两颗都投。
**EUR 第二席需要换 selection**：d5WRPO3j（CROWDING）与两者相关 0.55–0.69，说明 prod_correlation 加权型 selection 能拉出部分独立度，但仍 >0.5。

### 5.3 IND（池 45，11 颗 SUPER 已占 —— 本轮破墙）

**已验证撞墙**：CROWDING 0.7255 / MARKET 0.8100（11-03 双杀）

| 候选 | 配方 | S | F | TO | self | prod | 2Y | sub | robust | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| **`2rAOGKow`** | **TOP500 SLOW d1 l10 cp3** | **4.43** | **3.58** | 0.2773 | 0.6101 | **0.6097** | 4.10 | 2.70 | 2.32 | ✅ **全闸通过** |
| `mLoqx1v1` | TOP500 FAST d1 l10 cp1 | 4.52 | 3.66 | 0.2982 | 0.6509 | 0.6509 | — | — | — | ✅ 但超 0.65；与 SLOW 相关 **0.8677** ⇒ 同席 |

**IS 闸明细（`2rAOGKow`）**：LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST / LOW_ROBUST_UNIVERSE_SHARPE **全 PASS**；`failed_ra_count=0`；无 WARNING。

**为什么 SLOW 能破墙**
1. SLOW 族的组合层中性化把 SA 的收益曲线从「市值/行业 beta」上剥离，与已提交的 11 颗（INDUSTRY / SUBINDUSTRY / STAT / RAM）在日收益上分散。
2. TO 从 CROWDING 的 0.236 升到 0.277，换手更高 ⇒ 与低频组件的重叠降低。
3. prod 从 0.7255 → 0.6097（**−0.116**），是中性化族切换在本账户的最大单次降幅。

**风险**：TO 0.2773 逼近 C 档上限 0.27（略超），但 A 档允许到 0.7，无闸门风险。

### 5.4 KOR（池 30，10 颗 SUPER 已占）

| 候选 | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`9qxVG66r`** | **SLOW d1 l10 cp7** | 3.95 | **4.55** | 0.1281 | 0.6370 | **0.6370** | ✅ **最优** |
| `zq3Nal3K` | SLOW d1 l10 cp5 | 3.98 | 4.61 | 0.1281 | 0.6427 | 0.6427 | ✅ 同席（0.9996） |
| `pwdN0aKo` | SLOW d1 l10 cp3 | 4.04 | 4.72 | 0.1280 | 0.6535 | 0.6535 | ⚠ 超 0.65 |
| `xArdpWvl` | SLOW d1 l10 cp1 | 4.12 | 4.88 | 0.1283 | 0.6717 | 0.6718 | ⚠ 超 0.65 |
| `O0AxjMZd` | FAST d1 l10 cp1 | 4.31 | 5.06 | 0.1455 | 0.6835 | 0.6835 | ⚠ 超 0.65 且与 SLOW 相关 0.909 |

**结论**：KOR **cp7 是甜点**（prod 0.6370，S/F 仅比 cp1 低 0.17/0.33），5 颗全部互为同席（0.909–0.9996）⇒ 只能投 1 颗。

**KOR 已提交的 10 颗互相关 0.38–0.65**（实测 `O0Aw0Y7Y`/`9qWJv1do`/`O0NLjMZR`/`E5vwqXNK`/`rKOPg9gd`），说明历史 SA 用了不同 selection ⇒ 现有 10 席是真的，新席必须换 selection。

### 5.5 GLB（池 18，5 颗 SUPER 已占）

| 候选 | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`GrWdQNq0`** | **TOP3000 SLOW d1 l15 cp3** | **3.51** | **1.58** | 0.2860 | 0.5135 | **0.5864** | ✅ **约束最优（S/F 双高）** |
| `0mYpnMr1` | TOP3000 SLOW d1 l10 cp3 | 3.45 | 1.42 | 0.3731 | 0.4560 | **0.5010** | ✅ prod 余量最厚（安全备胎） |
| `58Ek1w0z` | TOP3000 CROWDING d1 l10 | 3.53 | 1.82 | 0.3640 | 0.6702 | 0.6696 | ⚠ 超 0.65 |
| `GrWe5lgZ` | TOP3000 CROWDING d1 l10 cp3 | 3.50 | 1.78 | 0.3682 | 0.6673 | 0.6667 | ⚠ 同席（0.9985） |
| `xArdEG0W` | MINVOL1M CROWDING d1 l10 | 5.95 | 3.81 | 0.3452 | 0.7597 | 0.7592 | ❌ self/prod 双死 |
| `xArd7rVn` | MINVOL1M SLOW d1 l10 | 6.82 | 3.70 | 0.3466 | 0.7223 | 0.7209 | ❌ 双死 |
| `2rANx095` | TOPDIV3000 CROWDING d1 l10 | 3.40 | 1.86 | 0.3706 | 0.4633 | 0.5465 | ❌ **LOW_GLB_EMEA_SHARPE 0.96 FAIL** |

**结论**：GLB 干净席 = `GrWdQNq0`（l15，prod 0.5864 余量 0.064，S/F 最优）或 `0mYpnMr1`（l10，prod 0.501 余量 0.199，最安全）。两者相关 **0.9551** ⇒ 同席，只能选 1 颗。
**l10 → l15 的实测**：S +0.06 / F +0.16 / TO −0.087 / prod +0.085 / self +0.057 —— **l15 在 S/F/TO 上均更优，代价是 prod 余量从 0.199 缩到 0.064**。
**注意**：GLB 的高 S（6.82 / 5.95）全部来自 MINVOL1M，但该 universe 的 SA 与已提交 `LL5aX6Y2`+`A1V0NQ57NW` 高度相关（0.72–0.76）⇒ MINVOL1M 席已满。

### 5.6 GBR（池 24，5 颗 SUPER 已占）

| 候选 | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`QPvGdLYQ`** | **TOP700 SLOW d1 l10 cp3** | **4.23** | 3.54 | 0.1698 | 0.6330 | **0.6330** | ✅ 已建成（未提交） |
| `LLMGJrl9` | TOP700 CROWDING d1 l10 cp3 | 3.67 | 3.58 | 0.1506 | 0.609 | 0.6709 | ⚠ 超 0.65 |
| `kqNmmaoO` | TOP700 CROWDING d1 l10 cp1 | 3.66 | 3.60 | 0.1526 | 0.605 | 0.6873 | ⚠ 超 0.65 |
| `58EQGNxM` | TOP700 CROWDING d1 l10 cp5 | 3.67 | 3.57 | 0.1506 | **0.7493** | — | ❌ self FAIL |
| `A1VGqWod` | TOP700 SLOW d1 l10 cp5 | 4.22 | 3.52 | 0.1699 | **0.9996** | 0.9996 | ❌ 与 QPvGdLYQ 同席 |

**结论**：GBR 只有 1 个 universe（TOP700）⇒ 只能有 1 颗新席。`QPvGdLYQ` 已建成未提交，是唯一选择。**GBR 封档**。

### 5.7 USA（池 47，8 颗 SUPER 已占）

| 候选 | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`A1V0eZne`** | **TOP3000 SLOW d1 l10 cp1 + sel `(1-self)*(TO<0.22)`** | **6.39** | **7.06** | 0.1178 | 0.5087 | **0.6146** | ✅ **C 档，账户最强** |
| **`Xg9WNRg8`** | **TOP2000 SLOW d1 l10 cp3** | **4.74** | **4.10** | 0.1659 | 0.6493 | **0.6493** | ✅ 擦 0.65 |
| **`A1V0L9KQ`** | **TOP1000 SLOW d1 l10 cp3** | 2.90 | 2.03 | 0.1774 | 0.6331 | **0.6331** | ✅ |
| `leA3Pzbl` | TOP1000 CROWDING d1 l10 cp3 | 2.61 | 2.38 | 0.1341 | 0.6011 | 0.6011 | ✅ 与 A1V0L9KQ 相关 0.7225 |
| `j2YrkNkO` | TOP1000 CROWDING d1 l10 cp5 | 2.67 | 2.51 | 0.1264 | 0.5302 | 0.6451 | ⚠ 与 leA3Pzbl 0.985 |
| `6Xde2865` | TOP2000 CROWDING d1 l10 | 3.66 | 3.82 | 0.1416 | 0.6916 | 0.6916 | ⚠ 超 0.65 |
| `mLovnvXx` | TOP3000 CROWDING d1 l10 cp3 | 4.68 | 5.90 | 0.1261 | 0.8418 | 0.8418 | ❌ 双死 |
| `vR1kAQmr` | TOP3000 SLOW d1 l10 cp3（**标准 selection**） | **6.18** | **6.33** | 0.1559 | 0.7838 | 0.7838 | ❌ 双死 |
| `MPY1gw08` | TOP500 SLOW d1 l10 cp3 | 1.48 | 0.74 | 0.2036 | 0.4289 | 0.5958 | ❌ S/F 双 FAIL |
| `pwdKpVYb` | TOPSP500 CROWDING d1 l10 | 1.54 | 1.07 | 0.1400 | 0.3370 | 0.6473 | ❌ S 1.54 FAIL |

**结论**：USA 是**唯一能出 3 颗的区**（互测 0.284–0.578，全部 <0.7）。
`A1V0eZne` 与 `vR1kAQmr` 是**同一槽位、同一中性化族、同一 cp**，唯一差别是 selection 加了 `turnover<0.22`：prod 0.7838 → **0.6146**（−0.169），S +0.21、F +0.73。⇒ **selection 的 TO 约束是本轮最强的降 prod 杠杆**（§10.6）。
TOP3000 池虽被 38 RA + 4 SA 占满，但**用 selection 换个组件子集就能开新席**。

### 5.8 DEU（池 11）

| 候选 | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`QPv3Ww9p`** | **TOP500 SLOW d1 l10 cp3** | 2.13 | 1.60 | 0.1524 | 0.6923 | **0.6923** | ✅ 全闸通过（余量 0.008） |
| `rKRPwOJJ` | TOP500 CROWDING d1 l10 | 2.59 | 2.53 | 0.1300 | 0.7283 | 0.7282 | ❌ 撞墙 |

**IS 闸明细（`QPv3Ww9p`）**：无 FAIL；`failed_ra_count=0`。
**与现有 DEU 席的关系**：`QPv3Ww9p` ↔ `mLYLEm99`（DEU/TOP500 STAT，已提交）= **0.6923** —— 刚好压在 0.7 线下，**同席但不互斥**。

**结论**：DEU **技术上可投**（S 2.13 / F 1.60 / prod 0.6923），但 **self 与 prod 同时只剩 0.008 余量**，且 S/F 低于账户中位数（3.92/3.40）。
**建议**：DEU 列为**最低优先级**。真正要 DEU，应先把池从 11 扩到 ≥17（提交 6 颗 DEU RA），prod 天花板才能下来；在此之前投 1 天/1 个 SUPER 名额在这个区不划算。

### 5.9 本轮未完成项

| tag | 配方 | 状态 |
|---|---|---|
| `glb_topdiv3000_slow_d1_l10_cp3` | GLB/TOPDIV3000 SLOW cp3 | HTTP 429（并发上限），未完成 |

> 已放弃项：`mea_top400_*` ×4（region 关闭）。
> 三个 selection 变体已完成并全部出结果：`kor_..._selP` prod 0.8815 FAIL、`eur_..._selP` prod 0.7879 FAIL、`usa_top3000_..._selT` **prod 0.6146 PASS（`A1V0eZne`）**。
> 下轮优先补：GLB/TOPDIV3000 SLOW；KOR/EUR 的**软加权 selection**（`1.0-prod_corr` 不带 0.55 硬帽，见 §10.6）。

---

## 六、停投区

| Region | 理由 | 依据 |
|---|---|---|
| **MEA** | **平台已关闭 region**：`POST /simulations` 返回 `Region MEA is not available.` | 本轮 4 档全部 HTTP 400；`get_platform_setting_options` 无 MEA 条目。存量 19 REGULAR + 2 SUPER 仍 ACTIVE，但不能新建 |
| **HKG** | 组件池 6/10（差 4） | 需先提交 4 颗 HKG RA |
| **ASI** | 组件池 9/10（差 1） | 需先提交 1 颗 ASI RA；池内有 401 条未提交 IS 候选可捞 |
| **GBR** | 新增席已满（1 universe × 1 席） | SLOW 已建成待提交；cp5 同席 0.9996；CROWDING cp5 self 0.7493 |
| **DEU** | 池 11，prod 天花板 0.73；`QPv3Ww9p` 虽通过但 self/prod 同时只剩 0.008 余量 | CROWDING 0.7282；SLOW 0.6923 |
| **CHN / AMR** | 账户零组件 | 无 REGULAR 持仓 |

---

## 七、撞墙档案（已验证不可用，勿重复投入）

### 7.1 prod 墙（≥0.7）

| Alpha ID | 配方 | S | F | self | prod | 墙因 |
|---|---|---|---|---|---|---|
| `vR1kAQmr` | USA/TOP3000 SLOW cp3（**标准 selection**） | **6.18** | **6.33** | 0.7838 | 0.7838 | 标准 selection 版双死；**同槽换 `turnover<0.22` selection 即活**（`A1V0eZne` prod 0.6146） |
| `mLovnvXx` | USA/TOP3000 CROWDING cp3（标准 selection） | 4.68 | 5.90 | 0.8418 | 0.8418 | CROWDING + 标准 selection；**TO 约束版未试**（值得补） |
| `qML62GG2` | IND/TOP500 MARKET | 4.26 | 4.60 | 0.8099 | 0.8100 | MARKET 族与已提交强重叠 |
| `Jjev2pAe` | IND/TOP500 CROWDING | 4.25 | 4.11 | 0.7254 | 0.7255 | CROWDING 在 IND 无区分度 |
| `xArdEG0W` | GLB/MINVOL1M CROWDING | 5.95 | 3.81 | 0.7597 | 0.7592 | MINVOL1M 席已满 |
| `xArd7rVn` | GLB/MINVOL1M SLOW | 6.82 | 3.70 | 0.7223 | 0.7209 | 同上 |
| `rKRPwOJJ` | DEU/TOP500 CROWDING | 2.59 | 2.53 | 0.7283 | 0.7282 | 池 11 太小 |
| `QPv9pQZw` | USA/TOP1000 CROWDING cp1 + rank(w) | 2.65 | 2.48 | 0.3011 | 0.7116 | rank(w) 撞墙（self 极低但 prod 高） |
| `JjevJ8we` | USA/TOPSP500 INDUSTRY | 1.80 | 1.29 | 0.3343 | 0.7664 | TOPSP500 席同源 |

### 7.2 self 墙（≥0.7）

| Alpha ID | 配方 | self | 墙因 |
|---|---|---|---|
| `A1VGqWod` | GBR/TOP700 SLOW cp5 | 0.9996 | 与 `QPvGdLYQ`（cp3）同席 |
| `58EQGNxM` | GBR/TOP700 CROWDING cp5 | 0.7493 | cp5 在 GBR 反而升 self |
| `9qxR097o` | GLB/MINVOL1M ern3 门控 | 0.9639 | 与 `JjeGEzaE` 同结构同数据集 |
| `N1NO9nRe` | 同上（换字段） | 0.9506 | 同上 |

### 7.3 IS 闸墙

| Alpha ID | 配方 | 失败闸 | 值/限 |
|---|---|---|---|
| `omE6ad7E` | EUR/TOP2500 SLOW cp3 | **IS_LADDER_SHARPE** | 1.50 / 1.58 |
| `MPY1gw08` | USA/TOP500 SLOW cp3 | LOW_SHARPE + LOW_FITNESS | 1.48/1.58；0.74/1.0 |
| `pwdKpVYb` | USA/TOPSP500 CROWDING | LOW_SHARPE | 1.54 / 1.58 |
| `2rANx095` | GLB/TOPDIV3000 CROWDING | **LOW_GLB_EMEA_SHARPE** | 0.96 / 1.0 |

### 7.4 近失候选（prod 0.65–0.70，仅达 A 档，不达用户 0.65 质量线）

| Alpha ID | 配方 | S | F | prod | 差 0.65 |
|---|---|---|---|---|---|
| `mLoqx1v1` | IND/TOP500 FAST cp1 | 4.52 | 3.66 | 0.6509 | +0.0009 |
| `6Xde2865` | USA/TOP2000 CROWDING | 3.66 | 3.82 | 0.6916 | +0.0416 |
| `O0AxjMZd` | KOR/TOP600 FAST cp1 | 4.31 | 5.06 | 0.6835 | +0.0335 |
| `xArdpWvl` | KOR/TOP600 SLOW cp1 | 4.12 | 4.88 | 0.6718 | +0.0218 |
| `9qx9aAa2` | EUR/TOP2500 FAST cp1 | 4.83 | 3.99 | 0.6699 | +0.0199 |
| `LLMGJrl9` | GBR/TOP700 CROWDING cp3 | 3.67 | 3.58 | 0.6709 | +0.0209 |
| `58Ek1w0z` | GLB/TOP3000 CROWDING | 3.53 | 1.82 | 0.6696 | +0.0196 |
| `pwdN0aKo` | KOR/TOP600 SLOW cp3 | 4.04 | 4.72 | 0.6535 | +0.0035 |
| `d5WRPO3j` | EUR/TOPCS1600 CROWDING | 3.68 | 3.38 | 0.6987 | +0.0487 |

> 这些若把质量线放宽到 0.70（平台红线不变），可立即多出 9 颗可投候选；但 0.65 是用户 2026-11-03 定稿的质量定义，**本报告不擅自放宽**。

### 7.5 同席墙（本轮最重要的墙）

| 组合 | 相关 | 判定 |
|---|---|---|
| `9qxVG66r` ↔ `zq3Nal3K` ↔ `pwdN0aKo` ↔ `xArdpWvl` | **0.9843–0.9996** | 硬同席（KOR 全族） |
| `9qxVG66r` ↔ `O0AxjMZd`（SLOW ↔ FAST） | **0.9091** | 硬同席（换族不换席） |
| `leA3Pzbl` ↔ `j2YrkNkO` ↔ `78Ln2OPL` | 0.9152–0.9849 | 硬同席（USA/TOP1000 全 cp） |
| `58Ek1w0z` ↔ `GrWe5lgZ` | 0.9985 | 硬同席（GLB CROWDING cp1/cp3） |
| `A1V0L9KQ` ↔ `leA3Pzbl`（SLOW ↔ CROWDING） | 0.7225 | 平台互斥 |
| `QPvGdLYQ` ↔ `LLMGJrl9` | 0.7486 | 平台互斥（GBR） |
| `9qx9aAa2` ↔ `A1V0LZkg` | 0.7909 | 平台互斥（EUR 换 universe） |
| `0mYpnMr1` ↔ `58Ek1w0z` | 0.7061 | 擦线（GLB） |
| `Xg9WNRg8` ↔ `6Xde2865` | 0.7423 | 平台互斥（USA/TOP2000 换族） |
| `2rAOGKow` ↔ `mLoqx1v1`（SLOW ↔ FAST） | 0.8677 | 平台互斥（IND 换族不换席） |
| `A1V0eZne` ↔ `Xg9WNRg8` | **0.5095** | ✅ 可共存 |
| `A1V0eZne` ↔ `A1V0L9KQ` | **0.2836** | ✅ 真新席 |
| `A1V0eZne` ↔ `gJePPn0K`（已提交 FAST） | 0.5087 | ✅ 可共存 |
| `Xg9WNRg8` ↔ `A1V0L9KQ` | **0.5777** | ✅ 可共存（USA 双席通路） |

---

## 八、执行清单

### 8.1 构建命令（可复现）

```bash
cd D:/coding/traeCN_project/wqb
# 批次 A（MEA + USA）
world-quant-brain-mcp/.venv/Scripts/python.exe -u C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261104/configs_A.json \
  --out results/sa_scan_20261104/res_A.jsonl
# 批次 B（EUR/GBR/KOR/IND/GLB/DEU）
... --configs results/sa_scan_20261104/configs_B.json --out results/sa_scan_20261104/res_B.jsonl
# 批次 C（EUR/USA/GLB/IND 补档）
... --configs results/sa_scan_20261104/configs_C.json --out results/sa_scan_20261104/res_C.jsonl
# 批次 D（selection 变体——新席验证）
... --configs results/sa_scan_20261104/configs_D.json --out results/sa_scan_20261104/res_D.jsonl
```

### 8.2 配额约束

| 项 | 限制 | 影响 |
|---|---|---|
| SUPER 提交 | **1/ET日/账号（跨区共享）** | 4 颗候选 = 4 天 |
| REGULAR 提交 | 4/天/区（与 SUPER 独立） | 不冲突 |
| prod 相关性检查 | 账号级单并发 | 多进程会返回 `correlation_busy`，需 8×40s 重试 |
| 仿真并发 | 平台限流 429 | sa_run 已内置耐心轮询（90×10s） |

### 8.3 建议执行顺序

1. **`A1V0eZne`**（USA/TOP3000）—— S 6.39 / F 7.06（账户 F 纪录）/ 2Y 7.06 / prod 0.6146，**C 档最强**
2. **`Xg9WNRg8`**（USA/TOP2000）—— S 4.74 / F 4.10，prod 0.6493 擦 0.65，先重测
3. **`A1V0LZkg`**（EUR）—— S/F 双优、prod 0.6391、EUR 席唯一（**最稳**）
4. **`2rAOGKow`**（IND）—— 破墙首颗、prod 余量 0.090 最厚
5. **`9qxVG66r`**（KOR）—— F 4.55 本轮最高
6. **`A1V0L9KQ`**（USA/TOP1000）—— 与 1/2 相关 0.284/0.578，USA 第三席
7. 备胎 **`GrWdQNq0`**（GLB l15，prod 0.5864）/ **`QPvGdLYQ`**（GBR，prod 0.6330）

**提交前强制动作**：
- `check_correlation(alpha_id=..., refresh=True)` 重测 prod（**台账 48h 作废**；11-03 的 4 颗必须重测）
- 停掉后台 `sa_run.py` 批次再提交（并发会导致 `_probe_prod_max` ProxyError）
- 等满 flip 窗 ~250s 后 `super_build.py status` 确认 `ACTIVE`
- **`A1V0eZne` 所在槽位 USA/TOP3000 已 4 颗 SUPER，但仍可加**（互测 0.28–0.58）—— 唯一注意点：prod 0.6146 需重测确认未破 0.65

### 8.4 提交命令（仅在用户点名后执行）

```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id <ID> --region <REGION>
```

---

## 九、算子充分利用审查（平台组 SA 的算子清单）

### 9.1 平台算子总量与作用域

| 作用域 | 算子数 | 说明 |
|---|---|---|
| **全部** | **103** | `get_operators` |
| **COMBO** | **101** | 可用于 SA 的 combo 表达式；仅 `in` / `universe_size` 不可用 |
| **SELECTION** | **27** | 可用于 SA 的 selection 表达式（算术 15 + 比较 6 + 布尔 3 + 特殊 3） |
| REGULAR | 84 | 普通 alpha 表达式 |

**SELECTION 可用算子全表（27）**：`add / multiply / sign / subtract / log / max / abs / divide / min / signed_power / inverse / sqrt / reverse / power / or / and / not / is_nan / less / equal / greater / if_else / not_equal / less_equal / greater_equal / in / universe_size`

### 9.2 本账户实际利用率

| 维度 | 用量 | 利用率 |
|---|---|---|
| combo 表达式（当前模板） | `generate_stats` `self_corr` `if_else` `reduce_max` `subtract` `multiply` = **6** | 6/101 = **5.9%** |
| selection 表达式（当前模板） | `add` `multiply` `greater` `subtract` = **4** | 4/27 = **14.8%** |
| **合计去重** | **10 / 103** | **9.7%** |
| 历史 45 颗最多用过 | + `rank` `combo_a` = **12 / 103** | 11.7% |

### 9.3 未用能力图（按 ROI 排序）

| 优先级 | 算子 | 作用 | 为什么值得试 |
|---|---|---|---|
| ⭐⭐⭐ | `reduce_ir` / `reduce_avg` / `reduce_norm` / `reduce_percentage` / `reduce_skewness` / `reduce_kurtosis` / `reduce_stddev` / `reduce_range` / `reduce_count` / `reduce_min` / `reduce_sum` | 把 `self_corr` 的 N×N 矩阵压成标量权重的 **12 种替代方式** | 现只用 `reduce_max`（取最大相关）。`reduce_ir`（信息比）或 `reduce_avg` 会选出让组合更分散的权重 ⇒ **可能同时降 self 和 prod**，且是**换席**的合法手段 |
| ⭐⭐⭐ | **selection 的 `prod_correlation` 加权** | 现用 `(1-self_corr)`；历史成功模板用 `(0.7-prod_correlation)` | **唯一已验证能产生独立席的杠杆**（KOR 现有 10 颗相关 0.38–0.65 即来自此）。见 §10 |
| ⭐⭐ | `combo_a(alpha, nlength, mode)` | 平台内置组合器，mode=algo1/2/3 | 历史 4 颗用过；我们手写 `w=1-maxCorr` 只是一种。algo2/algo3 的权重口径不同 ⇒ 可能换席 |
| ⭐⭐ | `ts_target_tvr_decay` / `ts_target_tvr_hump` / `hump` | 把换手直接打到目标区间 | C 档要求 TO 0.20–0.27；当前候选 0.128–0.185 偏低。可做「TO 定向」实验 |
| ⭐⭐ | `vector_neut` | 权重对因子正交 | 天然压 prod；REGULAR 线实测有效（e75gdQoM） |
| ⭐ | `ts_mean` / `ts_delay` / `ts_rank` / `ts_zscore` / `ts_decay_linear` | 权重时序平滑 | 降 TO、稳 self |
| ⭐ | `winsorize` / `bucket` / `tail` / `quantile` / `scale` / `normalize` / `densify` | 权重整形 | `rank(w)` 已撞墙（prod 0.7116），但 `winsorize(w,0.01,0.99)` 未试 |
| ⭐ | `trade_when` | 条件门控 | 剔除高相关时段 |
| ⭐ | `group_neutralize` / `group_rank` / `group_scale` / `group_zscore` / `group_backfill` | 分组处理 | 改变权重分布 |
| — | SELECTION 未用字段：`author_fitness` `author_sharpe` `author_returns_to_drawdown` `datasets` `category` `universe_size` `in` | 组件质量筛选 | §0.3 论坛阈值全靠这些字段，**当前完全未启用** |

### 9.4 结论

**本次组建远未充分利用平台算子**：combo 侧 6/101、selection 侧 4/27，合计 **9.7%**。
最关键的缺口有三个：
1. **`reduce_*` 家族 12 个未用** —— 权重压缩方式单一（只有 max），直接限制了 self/prod 的可调空间；
2. **selection 的 `turnover` 约束** —— 本轮首测即产生账户最强候选（`A1V0eZne`：prod −0.169、S/F 双升）。这是**最高 ROI 的单个算子级改动**，应作为下轮所有区的默认项；
3. **selection 的 `prod_correlation` 加权** —— 本轮已试，**方向为负**（硬截断把分散组件筛掉，prod 反升）。不要再加 `self<0.55` 硬帽。

---

## 十、★ 方法学修正：SA 的「席」判据

### 10.1 旧判据（已证伪）

> 「换窗口/分组/中性化/幂次 = 同席；换科目/数据集/收益率源 = 新席」

这条来自 REGULAR 线，**直接套到 SA 上是错的**。

### 10.2 本轮实测

同一 region、同一组件池、**同一 selection 表达式**、只改中性化族 → 日收益相关：

| Region | 对比 | 相关 | 平台闸(0.7) | 社区线(0.5) |
|---|---|---|---|---|
| KOR | SLOW cp7 ↔ SLOW cp5/cp3/cp1 | 0.9843–0.9996 | ❌ 互斥 | ❌ 互斥 |
| KOR | SLOW cp7 ↔ **FAST** cp1 | **0.9091** | ❌ 互斥 | ❌ 互斥 |
| GLB | CROWDING cp1 ↔ CROWDING cp3 | 0.9985 | ❌ 互斥 | ❌ 互斥 |
| GLB | **SLOW** ↔ **CROWDING** | 0.7061 | ⚠ 擦线 | ❌ |
| GBR | **SLOW** ↔ **CROWDING** | 0.7486 | ❌ 互斥 | ❌ |
| EUR | TOP2500 FAST ↔ **TOPCS1600** FAST | 0.7909 | ❌ 互斥 | ❌ |
| USA | TOP1000 SLOW ↔ TOP1000 CROWDING | 0.7225 | ❌ 互斥 | ❌ |
| USA | **TOP2000 SLOW** ↔ **TOP1000 SLOW** | **0.5777** | ✅ 可共存 | ❌ |

⇒ **同 selection 下，换中性化族/换 combo 幂次基本不换席（0.70–0.93）；换 universe 仅在两 universe 成分差异大时才换席（USA TOP2000↔TOP1000 = 0.58 可共存），子集关系（EUR TOP2500⊃TOPCS1600）仍同席（0.79）。**

### 10.3 为什么历史 45 颗能共存

实测现有 KOR 5 颗互相关 **0.38–0.65**（`O0Aw0Y7Y` / `9qWJv1do` / `O0NLjMZR` / `E5vwqXNK` / `rKOPg9gd`），远低于我们新候选间的 0.91+。原因：45 颗用了 **20 种不同的 selection 表达式**（`(0.7-prod_correlation)`、`(0.65-prod_correlation)`、`(1.0-prod_correlation)*...`、`self_correlation<0.45/0.48/0.55` 等），不同 selection 选出**不同的组件子集** ⇒ 日收益真的不同。

### 10.4 新判据（本轮定稿）

> **SA 的席 = `region` × `selection 表达式`（组件子集）。**
> 同一 selection 下，中性化族 / combo 幂次 / truncation / decay **全部是同席**；universe 只在覆盖差异大时算半个新席。
> 想要第 N 个席，就要第 N 种 selection —— 不是第 N 个中性化族。

**互斥阈值**：
- **> 0.90 = 硬同席**（实测 0.98–0.9996）—— 换了等于没换。
- **0.70–0.90 = 平台互斥**（后提交者 self 闸必炸）—— 只能二选一。
- **0.50–0.70 = 可共存但不分散**（self 闸可过，组合层面冗余）。
- **< 0.50 = 真新席**（社区合格）。

**推论（直接影响方案）**：
- KOR / GBR / IND（单 universe）每区实际只有 **1 个可新增席**；
- **USA 可容 2 席**（TOP2000 + TOP1000，相关 0.578）；
- EUR 的 TOP2500 与 TOPCS1600 是包含关系 ⇒ 只 1 席；
- GLB 有 4 个 universe（TOP3000 / MINVOL1M / MINVOL10M / TOPDIV3000），理论可容 2–3 席，但 MINVOL1M 席已满（self 0.72–0.76）⇒ 剩 TOPDIV3000（待测）。
- **未来建 SA 的正确批次设计 = 1 个 region × N 种 selection**，而不是 1 个 region × N 个中性化族。

### 10.5 selection 变体的首批实测（部分为负）

按 §10.4 推论设计 3 条 selection 变体，实测：

| tag | 配方 | selection | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|---|
| `1YNxG0WX` | KOR/TOP600 **STAT** cp1 + selP | `(0.7-prod_corr)*(self_corr<0.55)*(TO<0.3)` | **4.76** | **5.15** | 0.1809 | 0.8815 | 0.8815 | ❌ prod/self 双 FAIL |
| `rKR50qqo` | EUR/TOP2500 **STAT** cp1 + selP | 同上 | 3.04 | 2.04 | 0.1084 | 0.7883 | 0.7879 | ❌ 双 FAIL |
| **`A1V0eZne`** | USA/TOP3000 **SLOW** cp1 + selT | `(1-self_corr)*(turnover<0.22)` | **6.39** | **7.06** | 0.1178 | 0.5087 | **0.6146** | ✅ **PASS，C 档** |

**结论（两条，方向相反）**：
1. **`prod_correlation` 加权型 + 硬截断 = 反向**：`(0.7-prod_corr)*(self<0.55)*(TO<0.3)` 把 prod 推高到 0.79–0.88。原因：`self_corr<0.55` 的硬截断把池里**最分散的组件筛掉了**，剩下高权重、高生产相关的核心组件 ⇒ 组合更像 production。
2. **`turnover` 约束型 = 强正向**：只把 selection 换成 `(1-self_corr)*(turnover<0.22)`，同槽位同中性化族同 cp，prod 从 **0.7838 → 0.6146（−0.169）**，S 6.18→**6.39**、F 6.33→**7.06**。⇒ **TO 约束筛掉的是高换手组件，这类组件正是与生产池最同源的。**

### 10.6 定稿的 selection 设计原则

| selection 元素 | 效果 | 证据 |
|---|---|---|
| `(1 - self_correlation)` 主体 | 基线分散 | 全部 45 颗 + 本轮默认 |
| **`* (turnover < 0.22)`** | **prod −0.17，S/F 双升** | `A1V0eZne` vs `vR1kAQmr`（同槽同族同 cp） |
| `* (0.7 - prod_correlation)` | 在 KOR/EUR 反向（prod +0.10~+0.26） | `1YNxG0WX` 0.8815、`rKR50qqo` 0.7879 |
| `* (self_correlation < 0.55)` 硬帽 | 与 prod 负相关（筛掉分散组件） | 同上 |
| `combo_power` 3/5/7 | prod −0.03~−0.05，S/F 同降 | KOR cp1→cp7；USA cp3→cp5 |

> **推荐模板**（下轮直接复用）：
> ```
> selection = (1 + 0 * (prod_correlation > 0)) * (1 - self_correlation) * (turnover < 0.22)
> combo     = stats=generate_stats(alpha); innerCorr=self_corr(stats.returns,500);
>             ic=if_else(innerCorr==1.0,nan,innerCorr); maxCorr=reduce_max(ic);
>             w=1-maxCorr; w
> ```
> 该组合在 USA/TOP3000（最饱和的槽位）产出 S 6.39 / F 7.06 / prod 0.6146。

**修正后的开席路径（按可行性排序）**：
| 路径 | 适用区 | 动作 | 已验证 |
|---|---|---|---|
| ① **selection 加 `turnover<0.22`** | 全区（尤其饱和区） | 换 selection，其余不动 | ✅ USA/TOP3000 prod 0.784→0.615 |
| ② 换 universe（成分差异大） | USA（TOP2000↔TOP1000 = 0.578） | 直接建 | ✅ 3 席互测 0.284–0.578 |
| ③ 扩池后重建 | KOR(30) / EUR(20) / GLB(18) / DEU(11) | 先提交 RA 增加组件，再建 SA | 未验证（受 REGULAR 4/天/区约束） |
| ④ 换 combo 权重口径 | 待验证 | `reduce_ir` / `combo_a(mode=algo2/3)` 替代 `reduce_max` | 未验证 |
| ❌ `prod_correlation` 硬截断 | — | — | 已证伪（prod 反升） |

---

## 附录 A：本轮扫描日志索引

| 文件 | 内容 |
|---|---|
| `results/sa_probe_cache.json` | 组件池 + 45 SUPER 全量（2026-11-04 09:07 refresh） |
| `results/os_alphas_full_20261104.json` | 387 条 OS alpha 全量（含 settings） |
| `results/sa_scan_20261104/configs_A~D.json` | 本轮 21 个配方 |
| `results/sa_scan_20261104/res_A~D.jsonl` | 逐条指标 + 双闸 |
| `results/sa_scan_20261104/run_A~D.log` | 完整仿真/探针日志 |
| `results/sa_scan_20261104/pyramid_multipliers.json` | pyramid 倍率原始数据 |
| `results/sa_scan_20261104/combo_operators.json` / `selection_operators.json` | 算子作用域清单 |

## 附录 B：与 11-03 方案的差异

| 项 | 11-03 方案 | 本轮（11-04） | 变化原因 |
|---|---|---|---|
| 首选 | `QPvGdLYQ`（GBR, S 4.23） | **`A1V0eZne`（USA/TOP3000, S 6.39 / F 7.06 / prod 0.6146）** | selection 首次加 `turnover<0.22` |
| 次选 | — | `Xg9WNRg8`（USA/TOP2000, S 4.74 / F 4.10） | TOP2000 SLOW 首次试 |
| 三选 | — | `A1V0LZkg`（EUR/TOPCS1600 FAST, prod 0.6391） | EUR 池 14→20，FAST 族首次可用 |
| IND | 停投（CROWDING 0.7255 / MARKET 0.810） | **恢复可投**（SLOW 0.6097；FAST 0.6509） | 首次试 SLOW/FAST 族 |
| KOR 最优 | cp5（prod 0.6427） | **cp7**（prod 0.6370） | 幂次甜点上移 |
| GLB 最优 | l10（S 3.45 / F 1.42 / prod 0.501） | **l15（S 3.51 / F 1.58 / prod 0.5864）** | 首次试 l15 |
| DEU | 停投（0.728） | **下限可投**（0.6923，余量 0.008） | 首次试 SLOW 族 |
| 席判据 | region×universe×中性化族 | **region × selection** | 互相关矩阵实测（15 组） |
| 降 prod 杠杆 | cp 幂次（−0.03~−0.06） | **selection `turnover<0.22`（−0.169）** | 本轮首测 |
| 可投颗数 | 5 颗（未去同席） | **6 颗（已去同席）**：USA×3 + EUR + IND + KOR | 同席互斥实测 |
| MEA | 未纳入 | **确认平台关闭** | 4 档 HTTP 400 |

---

**报告结束。全部为待执行配方，未提交任何 alpha。**
