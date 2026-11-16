# 各 Region 最优 SuperAlpha 方案 · 2026-11-15

> 生成时间：2026-11-15 07:2x GMT+8（ET 2026-11-14 18:2x）
> 本轮口径：**只挖不提交**。全文仅为方案与建议，提交权归用户（2026-11-11 用户明令撤销自动提交）。
> 数据基线：`probe_sa_candidates --refresh` @ 2026-11-15T06:31:56+08:00（先清 `api_cache` 5 条 `user_alphas%`）
> 候选实测：14 颗全部 `check_correlation(refresh=True)` 逐颗回源（无一条缓存值入表）

---

## 0 执行摘要

**本轮唯一实质变化：DEU/TOP500 出现第三族可行点，且是全账户最干净的可交候选。**

| 项 | 数值 |
|---|---|
| 组件池（ACTIVE 已提交 REGULAR） | 9 区 GO + HKG BLOCKED，总计 253 颗（11-14 为 250） |
| ACTIVE SUPER | **56**（11-14 为 55，+1 = `Wjl6JJQO` EUR/TOP2500 SUBINDUSTRY，ET 11-13 20:48 提交） |
| 本轮新建档位 | 10 档（USA 5 / ASI 2 / EUR 1 / GLB 1 / DEU 0） |
| 本轮复测历史候选 | 4 颗（`refresh=True`） |
| 过 0.68 双闸 | **5 颗** |
| 真实独立席位 | **3 席**（DEU/TOP500 R&M、USA/TOP1000 CROWDING、EUR/TOP2500 R&M）+ 1 席近似（EUR/TOPCS1600 ρ .6509） |
| 本轮排序第一 | `RReX6k6a` DEU/TOP500 REVERSION_AND_MOMENTUM d1（**未提交，待用户指令**） |
| SUPER 配额（ET 2026-11-14） | **未用**（末次 `Wjl6JJQO` ET 11-13 20:48；重置 GMT+8 11-15 13:00） |

### 0.1 优先队列（按边际价值）

| # | ID | 档位 | 族 | prod/self | 席位 | 结论 |
|---|---|---|---|---|---|---|
| 1 | `RReX6k6a` | DEU/TOP500 | REVERSION_AND_MOMENTUM d1 | **.5514 / .5516** | 异族（席内 2 颗：STAT/FAST） | B 档双达标，余量 .1486 全轮最厚 |
| 2 | `wpo6bEJ5` | DEU/TOP500 | SLOW_AND_FAST d1 | .5720 / .5723 | **同 #1 同席（ρ .7392）** | B 档，但交 #1 即作废 |
| 3 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | .6011 / .6011 | 异族（席内 1 颗 STAT） | 独立席，prod 差 B 档 .0011 |
| 4 | `xAvMbRll` | EUR/TOP2500 | REVERSION_AND_MOMENTUM d1 | .6281 / .6282 | 异族（席内 4 颗） | 独立席，余量 .0519 |
| 5 | `78Y01lrZ` | EUR/TOPCS1600 | CROWDING d1 | .6605 / .5073 | 异族（席内 1 颗 STAT） | 与 #4 ρ **.6509**，近似替代品 |

---

## 1 数据基线

### 1.1 组件池 eligibility（`probe --refresh`）

| Region | ACTIVE 已提交 REGULAR | 变化 | IS 存量 | verdict | 可用 universe |
|---|---:|---|---:|---|---|
| USA | 48 | **+1** | 207 | GO | TOP3000/TOP2000/TOP1000/TOP500/TOP200/TOPSP500 |
| IND | 47 | 0 | 67 | GO | TOP500 |
| KOR | 35 | 0 | 0 | GO | TOP600 |
| GBR | 28 | 0 | 463 | GO | TOP700 |
| EUR | 28 | 0 | 13 | GO | TOP2500/TOP1200/TOP800/TOP400/TOPCS1600 |
| DEU | 21 | **+2** | 199 | GO | TOP500 |
| MEA | 19 | 0 | 0 | GO（但区域已下架） | TOP400 |
| GLB | 19 | 0 | 1 | GO | TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000 |
| ASI | 10 | 0 | 0 | GO | MINVOL1M/MINVOL10M/TOP500 |
| HKG | 7 | 0 | 0 | **BLOCKED** | TOP800/TOP500（<10 硬下限） |

> DEU +2 / USA +1 来自 ET 11-13~11-14 的 REGULAR 提交（`pwaQ0bx3` 等）。池增长**没有**转化为新暴露：所有槽位仍被 SUPER 占用，零 SUPER 槽位仍为 0。

### 1.2 档位占用表（18 档，56 颗 ACTIVE SUPER）

| Region | Universe | SUPER 数 | 已占族（decay） | 本轮判定 |
|---|---|---:|---|---|
| USA | TOP3000 | 6 | MARKET(5)/SUBIND(5)/STAT(10)/FAST(1)/SLOW(1)×2 | 🔴 饱和，停扫 |
| USA | TOP2000 | 2 | STAT(1)、SLOW(1) | 🟡 本轮试 R&M/SLOW_AND_FAST/MARKET → 全死 |
| USA | TOP1000 | 1 | STAT(1, lim15) | 🟢 CROWDING 可交（`1YNl3p5R`） |
| USA | TOP500 | 1 | CROWDING(1) | 🔴 封档（同档全族已试） |
| USA | TOPSP500 | 1 | STAT(1, lim38) | 🔴 封档 |
| USA | TOP200 | 0 | — | ⚫ 无 REGULAR 池，历史判死 |
| IND | TOP500 | 12 | SUBIND×3/STAT×5/R&M/CROWDING… | 🔴 饱和，停扫 |
| KOR | TOP600 | 11 | STAT×6/SUBIND×2/R&M/SLOW/CROWDING | 🔴 饱和，停扫 |
| GBR | TOP700 | 6 | STAT×3/R&M/FAST/SLOW | 🔴 档内 6 颗，异族已失效 |
| EUR | TOP2500 | 4 | STAT/CROWDING/SLOW/SUBIND(新) | 🟢 R&M 可交（`xAvMbRll`） |
| EUR | TOPCS1600 | 1 | STAT | 🟢 CROWDING 可交（`78Y01lrZ`） |
| EUR | TOP1200/800/400 | 0 | — | ⚫ 结构性 prod 墙（第 6 次确认） |
| DEU | TOP500 | 2 | STAT(1)、FAST(1) | 🟢 **R&M 最优（`RReX6k6a`）** |
| GLB | MINVOL1M | 2 | SUBIND/.809、STAT/.610 | 🔴 停扫 |
| GLB | MINVOL10M | 1 | SLOW | 🔴 停扫（仿真 ~35 min，性价比低） |
| GLB | TOP3000 | 1 | R&M | 🟡 本轮 CROWDING → prod .7647 死 |
| GLB | TOPDIV3000 | 1 | STAT | ⚫ SLOW 建单必失败 |
| ASI | MINVOL1M | 1 | STAT(2) | 🟡 本轮 R&M → prod .6921 超闸 |
| ASI | MINVOL10M | 1 | COUNTRY(3) | 🔴 本轮 R&M → prod .8084，席已毒 |
| MEA | TOP400 | 2 | SUBIND | ⚫ 区域下架（新建 400） |

> **零 SUPER 槽位 = 0**。本轮所有产能只能来自「已占档的异族共存」，无新席位可用。

### 1.3 Pyramid 倍率（D1，仅记录，不作选塔理由）

| Region | D1 最高档（类别 / 倍率） | 中位 |
|---|---|---|
| DEU | model/news/other/analyst/fundamental/sentiment **1.8** | 1.6 |
| USA | other 1.4 / sentiment 1.4 / earnings 1.3 / option 1.3 / model 1.3 | 1.1 |
| EUR | other **1.5** / news 1.4 / sentiment 1.4 | 1.2 |
| ASI | analyst **1.5** / other 1.4 / sentiment 1.4 | 1.2 |
| GLB | fundamental/analyst 1.4 / news/model/sentiment 1.3 | 1.1 |

> 塔计数按季度重置，只认 `get_pyramid_alphas` 当季 ≥3；**SUPER 的 `is.checks` 无 `MATCHES_PYRAMID` ⇒ SA 不参与塔计数**，倍率不得当选塔/选区理由。

---

## 2 选点原则（本轮实际执行顺序）

1. **IS 全 PASS**（`is.checks.fail == []`）。注意 `LOW_FITNESS` 在 F<1.0 时是真 FAIL（本轮 `xAv9kzrN` F .69、`O0WqZo2J` F .93 即被拦）。
2. **席位类型**：零 SUPER > 异族共存 > 同族。本轮零 SUPER = 0，全走异族。
3. **同族/异族实测**：同族（只改 limit/decay/truncation）预期 >0.9 直接跳过；异族必须 `self` 实测。
4. **B 档双达标**（TO<0.30 ∧ prod<0.60）。
5. **prod 余量**（0.68 − prod）降序。
6. **U / Eff** 降序（跨区可比，区内无独立信息）。

**本轮判序落地**：先按 1→4 分层，B 档层内按余量排，非 B 档层内按余量排。质量口径（Eff）复核后第 1 名一致，未出现 11-13/11-12 那种双口径分叉。

---

## 3 论坛指标标准（固化，引用 §0，本轮无需重调研）

### 3.1 组成数量
- 平台硬下限 **10**（<10 → 400 `Ensure this value is greater than or equal to 10`）
- 社区建议 30–100 起测、≤500（78 赞帖）；实际生效 = `min(limit, 组件池)`
- 本仓实测：**l10 双闸综合最优**，l12/l14 会同时推高 self 与 prod（KOR l14 self .935 判例）

### 3.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.4（`HIGH_TURNOVER` 实测 limit 0.4） | <0.7 |
| B 社区合格 | — | — | **<0.30** | **<0.60** |
| C 比赛优秀 | 5.6–7.0 | 5.6–8.9 | 0.20–0.27 | <0.5 |

### 3.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown 1–4`。
⚠ 加严后组件 <10 直接 ERROR；小池区只能用宽松 selection。**`author_*` 在自有池恒为常数 ⇒ 论坛 author_fitness 阈值不可消费**（11-06 定案）。

---

## 4 ★ 边际收益排序（§0.6 五量全表）

口径：`μ̄` = 该区 ACTIVE 已提交 REGULAR 的 IS Sharpe 均值（本轮重算：USA 1.9746 / DEU 1.8071 / EUR 2.0764 / ASI 2.3080 / GLB 3.0321 / IND 2.7302 / KOR 1.8586 / GBR 1.9064 / MEA 1.8847 / HKG 1.9757）；`N = min(selectionLimit, 池)` = 10（全部候选）。

| # | ID | 档位 | 族 | S | F | TO | prod | self | **U** | N_eff | ρ_eff | **Eff** | ΔCAP% | 席位 | 同/异族 | 双闸实测 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | `RReX6k6a` | DEU/TOP500 | R&M d1 | 2.92 | 2.91 | .1381 | **.5514** | **.5516** | **.5110** | 2.611 | +.3144 | **2.018** | +0.015% | 异族（2 颗） | 异 | 11-15 07:03 |
| 2 | `wpo6bEJ5` | DEU/TOP500 | SLOW_AND_FAST d1 | 2.81 | 2.14 | .1909 | .5720 | .5723 | .4917 | 2.418 | +.3484 | 1.752 | +0.014% | 异族 | **同 #1（ρ .7392）** | 11-15 07:06 |
| 3 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 | 2.38 | .1341 | .6011 | .6011 | .4180 | 1.747 | +.5249 | 1.057 | +0.012% | 异族（1 颗） | 异 | 11-15 07:12 |
| 4 | `xAvMbRll` | EUR/TOP2500 | R&M d1 | 3.17 | 2.45 | .1090 | .6281 | .6282 | .4828 | 2.331 | +.3656 | 1.741 | +0.011% | 异族（4 颗） | 异 | 11-15 07:09 |
| 5 | `78Y01lrZ` | EUR/TOPCS1600 | CROWDING d1 | 2.77 | 2.22 | .0959 | .6605 | .5073 | .4219 | 1.780 | +.5132 | 1.050 | +0.012% | 异族（1 颗） | 异（但与 #4 ρ .6509） | 11-15 07:19 |

### 4.1 被闸门拦下的候选（本轮实测，供复盘）

| ID | 档位 | 族 | S | F | TO | prod | self | 死因 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| `LLKq1dKL` | ASI/MINVOL1M | R&M d1 | 4.78 | 2.98 | .3320 | **.6921** | .6921 | 平台 0.7 可过，**本方案 0.68 余量闸拒**（余量 .0079）。U .6549 / Eff 3.572 全轮最高，唯一可惜件 |
| `npaY2R1M` | USA/TOP2000 | R&M d1 | 2.03 | 1.43 | .2204 | **.7646** | — | prod 红线 |
| `MP6qQLn8` | USA/TOP1000 | INDUSTRY d1 | 1.80 | 1.34 | .2052 | **.8078** | — | prod 红线 |
| `ZYaqKYEd` | USA/TOP2000 | MARKET d1 | 2.33 | 2.07 | .1757 | **.7677** | — | prod 红线 |
| `WjlnGbPx` | ASI/MINVOL10M | R&M d1 | 3.48 | 2.03 | .3547 | **.8084** | — | prod 红线（席已被 `QPv88bJW` 毒） |
| `zqdQmnKK` | GLB/TOP3000 | CROWDING d1 | 3.19 | 1.67 | .2434 | **.7647** | — | prod 红线 |
| `78Y01Az2` | USA/TOP1000 | R&M d1 | 1.55 | 0.96 | .2333 | — | — | IS FAIL ×3（LOW_SHARPE / LOW_FITNESS / IS_LADDER） |
| `xAv9kzrN` | USA/TOP1000 | SLOW_AND_FAST d1 | 1.52 | 0.69 | .2860 | — | — | IS FAIL ×3 |
| `O0WqZo2J` | USA/TOP2000 | SLOW_AND_FAST d1 | 1.84 | 0.93 | .2614 | — | — | IS FAIL（LOW_FITNESS） |

### 4.2 四条读法（本轮复核）

1. **席位边际 > 指标边际**：`LLKq1dKL` 指标全轮最强（U .6549 / Eff 3.572）却是唯一被 0.68 闸拒的过闸件 —— 席位（ASI/MINVOL1M 已被 `d5WGG5bg` 占）压倒了指标。
2. **同族 = 死、异族可共存**：`wpo6bEJ5` 与 `RReX6k6a` 同档异族仍 ρ **.7392** ⇒ 已越过 0.5 的"可共存"线，实际是**同席**。反过来 `xAvMbRll`（EUR/TOP2500 R&M）与 11-13 新交的 `Wjl6JJQO`（SUBIND）self top1 仍是 `GrgGkV1o`(STAT .6282)，说明新提交**没有**毒化异族 —— 11-14 的"未定向毒化"结论本轮再证。
3. **区内 U/ρ_eff/N_eff 无独立信息**：同一区内三者严格单调于 S（`1YNl3p5R` U .4180 最低正因为 S 最低），只在跨区可比。
4. **ΔCAP% 已退化**：全部候选 ΔCAP 落在 +0.011%~+0.015%，与 50+ 颗 SA 池的边际一致 —— 不可当排序主键。真正有区分力的仍是 **Eff、席位类型、同族/异族**。

---

## 5 分 Region 方案

### 5.1 DEU / TOP500 — 本轮最优（R&M 族）

| 项 | 值 |
|---|---|
| 配方 | `selectionLimit=10`, `POSITIVE`, `neutralization=REVERSION_AND_MOMENTUM`, `decay=1`, `truncation=0.08` |
| 指标 | S **2.92** / F **2.91** / TO **.1381** / 2Y **3.44** / sub **1.89** / margin .001982 |
| 双闸 | prod **.5514** / self **.5516**（refresh=True 11-15 07:03） |
| 余量 | prod .1486、self .1484 |
| 档内 | 2 颗（STAT `mLYLEm99` .610、FAST `vR1oxZA3` .598）；R&M 为**第三族**，self top1 = `vR1oxZA3` .5516 |
| IS checks | 8 PASS / 0 FAIL，warning 仅 `MATCHES_COMPETITION` |
| 判定 | **B 档双达标**（TO<.30 ∧ prod<.60），本轮唯一 |

**族谱（DEU/TOP500 全 10 族，跨 10-24~11-15 累计）**
R&M **.5514** < SLOW_AND_FAST .5720 < SLOW .5951 < FAST .5987(已占) < STAT .610(已占) < CROWDING .6434 < SUBIND .7400 < INDUSTRY .7412 < SECTOR .7701 < MARKET .7708。
> 推翻 11-12「DEU 族谱 S 与 prod 同向」的普遍性：该结论只对粗族（SECTOR/MARKET/INDUSTRY）成立；R&M 是 S 与 prod 同步最优的例外。

**增量价值**：DEU/TOP500 从 2 席 → 3 席，R&M 与现有两族 ρ≤.5516，是真实新席。交一颗即该席满（`wpo6bEJ5` 作废）。

### 5.2 USA / TOP1000 — CROWDING（唯一可交的 USA 窄档）

| 项 | 值 |
|---|---|
| ID | `1YNl3p5R`（历史件，本轮 refresh 复测） |
| 配方 | TOP1000 / d1 / **CROWDING** / l10 |
| 指标 | S **2.61** / F **2.38** / TO **.1341** / 2Y 2.83 |
| 双闸 | prod **.6011** / self **.6011**（11-15 07:12） |
| 档内 | 1 颗 STAT `LL5aX6Y2`（lim15, .660）；self top1 = 它，.6011 |
| 判定 | 过 0.68，但 prod .6011 **差 B 档 .0011** |

**本轮该档 4 族全灭**：R&M（IS FAIL）、SLOW_AND_FAST（IS FAIL）、INDUSTRY（prod .8078）、以及既有 SLOW/FAST/SUBIND 历史死。⇒ USA/TOP1000 只剩 CROWDING 一族。

### 5.3 EUR / TOP2500 — R&M（末席）

| 项 | 值 |
|---|---|
| ID | `xAvMbRll` |
| 配方 | TOP2500 / d1 / **REVERSION_AND_MOMENTUM** / l10 |
| 指标 | S **3.17** / F **2.45** / TO **.1090** / 2Y 3.32 / sub 1.78 |
| 双闸 | prod **.6281** / self **.6282**（11-15 07:09） |
| 档内 | 4 颗 STAT(.462)/CROWDING(.654)/SLOW(.567)/SUBIND(.641 新) |
| IS | 0 FAIL，warning `CLUSTER_TEST` 1.31（<1.58）+ `MATCHES_COMPETITION` |
| 判定 | 过闸，余量 .0519（抗漂移一般） |

### 5.4 EUR / TOPCS1600 — CROWDING（新建，独立度好但 prod 高）

| 项 | 值 |
|---|---|
| ID | `78Y01lrZ`（本轮新建） |
| 指标 | S **2.77** / F **2.22** / TO **.0959** |
| 双闸 | prod **.6605** / self **.5073** |
| 档内 | 1 颗 STAT `vROOONwd`（.559）；self top1 = 它，.5073 |
| 判定 | 过 0.68（余量 .0195，贴线）；与 `xAvMbRll` ρ **.6509** ⇒ 与 5.3 近似同席，二选一 |

### 5.5 其余区域（无可建产能）

| Region/档 | 状态 | 依据 |
|---|---|---|
| USA/TOP3000 (6)、TOP500 (1)、TOPSP500 (1) | 🔴 停投 | 全族已扫，prod 墙 + 同席碰撞 |
| USA/TOP2000 (2) | 🔴 停投 | 本轮 R&M .7646 / MARKET .7677 / SLOW_AND_FAST IS FAIL，剩余族无意义 |
| USA/TOP200 | ⚫ 判死 | 无 REGULAR 池 + 历史 S/F 不达标 |
| IND/TOP500 (12)、KOR/TOP600 (11) | 🔴 饱和 | 档内 ≥5 颗后异族亦失效 |
| GBR/TOP700 (6) | 🔴 封档 | 档内 6 颗，CROWDING 双撞 .7332 |
| GLB 四档 (1/2/1/1) | 🔴 停扫 | MINVOL1M SUBIND prod .809 已占；MINVOL10M 仿真 35 min；TOPDIV3000+SLOW 建单必失败 |
| ASI 两档 (1/1) | 🔴 本轮封 | MINVOL10M R&M .8084；MINVOL1M R&M .6921 超闸 |
| EUR/TOP1200·800·400 | ⚫ 永久停投 | 结构性 prod 墙（第 6 次确认） |
| MEA 全域 | ⚫ 下架 | 新建 400 `Region MEA is not available` |
| HKG / CHN / AMR / JPN / TWN | ⚫ 池不足 | HKG 7/10，其余 0 |

---

## 6 执行清单（候选构建命令，可复现）

```bash
cd D:/coding/traeCN_project/wqb
PY=world-quant-brain-mcp/.venv/Scripts/python.exe
D=results/sa_scan_20261115

# 本轮 10 档（照抄即复现；同式异 decay 同批会被平台去重 ⇒ 分两波）
$PY tools/super_build.py select --region USA --universe TOP1000 --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t1000_revmom_d1.json
$PY tools/super_build.py select --region USA --universe TOP2000 --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t2000_revmom_d1.json
$PY tools/super_build.py select --region USA --universe TOP1000 --delay 1 --neutralization SLOW_AND_FAST --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t1000_slowfast_d1.json
$PY tools/super_build.py select --region USA --universe TOP2000 --delay 1 --neutralization SLOW_AND_FAST --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t2000_slowfast_d1.json
$PY tools/super_build.py select --region USA --universe TOP1000 --delay 1 --neutralization INDUSTRY --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t1000_industry_d1.json
$PY tools/super_build.py select --region USA --universe TOP2000 --delay 1 --neutralization MARKET --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t2000_market_d1.json
$PY tools/super_build.py select --region ASI --universe MINVOL1M --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_asi_minvol1m_revmom_d1.json
$PY tools/super_build.py select --region ASI --universe MINVOL10M --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_asi_minvol10m_revmom_d1.json
$PY tools/super_build.py select --region EUR --universe TOPCS1600 --delay 1 --neutralization CROWDING --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_eur_tcs1600_crowding_d1.json
$PY tools/super_build.py select --region GLB --universe TOP3000 --delay 1 --neutralization CROWDING --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_glb_top3000_crowding_d1.json
```

**约束**：并发仿真上限 2（第 3 路 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`）；每档 6–10 min，GLB/MINVOL10M 类空 universe 档 ~35 min；prod 相关性账号级单并发（`correlation_busy` 按 `retry_after` 重查，勿重触发）。

---

## 7 提交建议（**本轮未提交，等待用户指令**）

### 7.1 建议对象

**第 1 顺位：`RReX6k6a` — DEU/TOP500 / REVERSION_AND_MOMENTUM / decay 1 / limit 10**

| 硬闸项 | 要求 | 实测 | 判定 |
|---|---|---|---|
| prod | ≤ 0.68（本方案余量闸） | **0.5514** | ✅ 余量 .1486 |
| self | ≤ 0.68 | **0.5516** | ✅ 余量 .1484 |
| IS checks | 零 FAIL | 8 PASS / 0 FAIL | ✅ |
| 台账 `robustness_RReX6k6a` | 无 REJECT | 无记录（未跑稳健性 → 无 REJECT） | ✅ |
| 同档族位 | 异族（同族预期 self>.9） | 异族，self top1 `vR1oxZA3` .5516 | ✅ |

**第 2 顺位：`1YNl3p5R` — USA/TOP1000 / CROWDING / l10**（prod .6011 / self .6011，余量 .0989；USA 窄档唯一可交件）
**第 3 顺位：`xAvMbRll` — EUR/TOP2500 / R&M / d1**（prod .6281 / self .6282，余量 .0519，抗漂移偏薄）

> ⚠ `wpo6bEJ5` 与 `RReX6k6a` 互测 ρ **.7392** 属同席 —— 交 `RReX6k6a` 即封该席，`wpo6bEJ5` 同日作废。
> ⚠ `78Y01lrZ` 与 `xAvMbRll` ρ **.6509** —— 二者近似替代，不要连交。

### 7.2 配额提示

- `SUPER_SUBMISSION` = **1 颗 / ET 日历日，账户级**，00:00 ET 重置（= GMT+8 13:00）。
- **当前 ET 日 = 2026-11-14（ET 18:2x），未用**：末次 SUPER 提交为 `Wjl6JJQO` @ ET 2026-11-13 20:48。⇒ 本 ET 日仍有 1 颗额度，重置点距现在约 **6 小时**（GMT+8 11-15 13:00）。
- 403 = 零配额成本、不判死候选；**不要用"试提"当探针**。

### 7.3 命令模板（**仅供用户手动执行，本轮未运行**）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit --alpha-id RReX6k6a --region DEU
```

### 7.4 两个已知坑

1. **提交前停后台批次**：并发仿真会让 `_probe_prod_max` 抛 ProxyError。本轮全部仿真已于 07:2x 结束，当前无 inflight。
2. **prod 槽 195s 冷却**：`logs/_dblock/correlation.cooldown.json`，未过期时提交会 fail-fast。本轮最后一次 prod 查询在 07:19，若立即提交需确认冷却已过。

---

## 8 算子利用率审计（官方 Combo / Selection 清单 vs 本仓实际）

| 维度 | 官方可用 | 本轮新用 | 累计使用 | 利用率 | 备注 |
|---|---:|---:|---:|---:|---|
| COMBO 算子 | 160 | **0** | 4（`generate_stats`/`self_corr`/`reduce_max`/`if_else`） | 2.5% | 全部候选走默认模板 `w = 1 - reduce_max(self_corr(returns,500))` |
| SELECTION 函数算子 | 43 | **0** | 0 | 0% | 全部走默认模板 `(1+0*(prod_correlation>0))*(1-prod_correlation)*(self<0.7)*(TO 区间)` |
| 中性化族 | 11（+COUNTRY 于 GLB/EUR/ASI） | 1（R&M 首次用于 ASI） | 10/11（仅 `NONE` 未用） | 91% | **本轮唯一真实杠杆仍在族轴** |

**结论**：算子轴连续多轮零新增，ROI 已枯竭；`combo` 整形（sqrt/rank/zscore/ts_mean/signed_power）与 `combo_power≥6` 历史上全部证伪。迭代收益只能来自中性化族轴 + 池增长。

---

## 9 本轮撞墙档案（新增，累积入库）

| 档位 | 配方 | 结果 | 性质 |
|---|---|---|---|
| USA/TOP1000 | R&M d1 l10 | S1.55/F0.96，LOW_SHARPE+LOW_FITNESS+LADDER 三 FAIL | 族否决 |
| USA/TOP1000 | SLOW_AND_FAST d1 l10 | S1.52/F0.69，三 FAIL | 族否决 |
| USA/TOP1000 | INDUSTRY d1 l10 | S1.80/F1.34，prod **.8078** | prod 红线 |
| USA/TOP2000 | R&M d1 l10 | S2.03/F1.43，prod **.7646** | prod 红线 |
| USA/TOP2000 | SLOW_AND_FAST d1 l10 | S1.84/F0.93，LOW_FITNESS | 族否决 |
| USA/TOP2000 | MARKET d1 l10 | S2.33/F2.07，prod **.7677** | prod 红线 |
| ASI/MINVOL1M | R&M d1 l10 | S4.78/F2.98/TO.332，prod/self **.6921** | 超 0.68 余量闸（平台可过） |
| ASI/MINVOL10M | R&M d1 l10 | S3.48/F2.03，prod **.8084** | 席被 `QPv88bJW` 毒 |
| GLB/TOP3000 | CROWDING d1 l10 | S3.19/F1.67，prod **.7647** | prod 红线 |

---

## 10 附：本轮文件清单

| 文件 | 内容 |
|---|---|
| `results/sa_scan_20261115/super_list.json` | 56 颗 ACTIVE SUPER 全字段（含 universe/neut/decay/prod/self） |
| `results/sa_scan_20261115/mu_bar.json` | 10 区 μ̄ 重算（含缺失校验，本轮 0 缺失） |
| `results/sa_scan_20261115/five_metrics.json` | 5 颗过闸候选的五量计算明细 |
| `results/sa_scan_20261115/res_*.json` + `log_*.log` | 10 档新建结果与日志（逐档独立） |
| `results/sa_scan_20261115/build_a.sh` / `build_bc.sh` / `build_d.sh` | 分波派发脚本（2 路串行） |

---

**本轮未提交任何 alpha。以上排序与建议仅作决策输入，提交权与提交时点完全归用户。**
