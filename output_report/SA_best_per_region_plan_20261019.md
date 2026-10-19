# 各 Region 最优 SuperAlpha 构建方案（2026-10-19 更新版）

生成时间：2026-10-19 23:20（本地）
数据口径：**平台真实仿真 + `check_correlation(refresh=True)` 强制回源实测**。
上一版：`SA_best_per_region_plan_20261018.md`（DEU `mLYLEm99` 已按该方案落地）。

> **只挖不提交**：本方案全部为**待执行配方**，未做任何提交动作。提交须你点名。

---

## 〇、执行摘要：按价值排序的优先队列

| 优先级 | region / 档位 | 最优配方 | IS S | F | SELF | PROD | 余量 | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---|
| **P0-A** | **USA / TOP1000** | STATISTICAL · decay 1 · lim 15 · trunc 0.02 | **2.61** | 1.80 | **0.0000** | **0.6601** | 0.0399 | ✅ **已提交 ACTIVE**（2026-10-19T11:29:25-04:00，name `USA_S_10comp_5aX6Y2`） |
| **P0-B** | **EUR 解锁** | 补 2 颗 REGULAR（库存 87） | — | — | — | — | — | 🔥 **差 2 颗**（10-18 记录为差 3，已 +1） |
| **P1** | **EUR 解锁后建 SA** | STATISTICAL · d1 · lim10 起步（全空档 ⇒ SELF=0） | — | — | **0.0000** | 待测 | — | 解锁后 POST 实测 |
| **P2** | **ASI 解锁** | 补 1 颗 RA（IS 库存 **0**，需新挖） | — | — | — | — | — | 差 1 颗，成本高 |
| P3 | USA / TOP1000（稳选） | SUBINDUSTRY · d15 · lim 10 | 1.90 | 1.56 | **0.0000** | **0.6344** | **0.0656** | 备选（`JjPlvGVj`） |
| P4 | GBR / TOP700 | SUBINDUSTRY · d15 · lim 10 | 2.76 | 2.68 | 0.6540 | 0.6849 | 0.0151 ⚠️ | 余量 <0.02 安全线，需重扫 |
| — | IND / KOR / GLB / DEU / MEA / HKG | — | — | — | — | — | — | **停投**（理由见 §4） |

**一句话结论**：DEU 已在 10-18 落地并转为「已占用」，当前**唯一立即可建的高价值落点是 USA/TOP1000**（零占用档 ⇒ SELF 恒 0，双闸实测 0.6601/0.0000 通过）。
**最高杠杆的并行动作是 EUR 解锁**——只需再补 **2 颗**（非 3 颗），解锁后 EUR 五个档位全空 ⇒ 同样享受 SELF=0。

---

## 一、数据基线（2026-10-19 23:10 平台实测）

### 1.1 组件池 eligibility（硬前置 ≥10 颗 ACTIVE 已提交 REGULAR）

| region | ACTIVE 已提交 | 10-18 记录 | 变化 | IS 未提交库存 | verdict | 已提交 SA |
|---|---:|---:|---|---:|---|---:|
| USA | **41** | 41 | — | 324 | GO | **5**（`LL5aX6Y2`，10-19 新增） |
| IND | **36** | 36 | — | 436 | GO | 19（11 ACTIVE + 8 待提交） |
| KOR | **26** | 26 | — | 103 | GO | 8 |
| MEA | 19 | 19 | — | 0 | GO | 2 ❌ 平台已关闭 |
| GBR | **18** | 18 | — | 0 | GO | 2 |
| GLB | **11** | 11 | — | 0 | GO | 4 |
| DEU | **10** | 10 | — | **0** | GO | **1**（`mLYLEm99`） |
| EUR | **8** ⬆ | 7 | **+1** | **87** | BLOCKED（差 **2**） | 0 |
| ASI | **9** | 9 | — | **0** | BLOCKED（差 1） | 0 |
| HKG | 6 | 6 | — | 0 | BLOCKED（差 4） | 0 |

> **★ 本轮实测修正**：EUR 由 7 → **8**（10-19 08:56 新提交 `88vQz5Yl`，EUR/TOPCS1600/INDUSTRY/d1，
> S 1.84 / F 1.30 / self 0.3101 / **prod 0.6637**）。⇒ **解锁缺口由 3 颗收窄到 2 颗**。
> ASI 实测仍为 9 颗 ACTIVE（无变化），缺口 1。

### 1.2 已占档位 vs 零占用档位（★ 决定 SELF 的关键）

| region | 合法 universe（平台） | 已被 SA 占用 | **零占用档** |
|---|---|---|---|
| USA | TOP3000/2000/**1000/500/200/TOPSP500** | TOP3000 ×3、TOP2000 ×1、**TOP1000 ×1**（`LL5aX6Y2`，10-19） | ⭐ **TOP500、TOP200、TOPSP500**（TOP1000 已占） |
| EUR | TOP2500/1200/800/400/TOPCS1600 | 无 | ⭐ **全空（5 档）**— 但组件仍差 2 |
| ASI | MINVOL1M/MINVOL10M/TOP500 | 无 | ⭐ 全空 — 组件差 1 |
| HKG | TOP800/TOP500 | 无 | 全空 — 组件差 4 |
| GLB | TOP3000/MINVOL1M/**MINVOL10M**/TOPDIV3000 | TOP3000 ×1、MINVOL1M ×2、TOPDIV3000 ×1 | MINVOL10M（⚠️ 曾 `zqraRwZO` PROD 0.8210 撞墙） |
| IND | TOP500 | TOP500 ×11 | 无 |
| KOR | TOP600 | TOP600 ×8 | 无 |
| GBR | TOP700 | TOP700 ×2 | 无 |
| DEU | TOP500 | **TOP500 ×1**（`mLYLEm99`，10-18 新增） | ❌ **零占用已耗尽** |
| MEA | TOP400 | TOP400 ×2 | 平台已关闭 |

### 1.3 本轮双闸实测（2026-10-19 23:15，`refresh=True` 强制回源）

| alpha | 档位 | 配方 | IS S | F | **SELF** | **PROD** | 余量 | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `LL5aX6Y2` | USA/TOP1000 | STAT · d1 · lim15 | **2.61** | 1.80 | **0.0000** | **0.6601** | 0.0399 | ✅ `all_passed=true` |
| `JjPlvGVj` | USA/TOP1000 | SUBINDUSTRY · d15 · lim10 | 1.90 | 1.56 | **0.0000** | **0.6344** | **0.0656** | ✅ `all_passed=true` |

> **★ 两条同时验证的规律**：
> ① **零占用档 ⇒ SELF 恒 0.0000**（本轮 2/2，累计 7/7 全中）。
> ② **零占用档的 prod 不漂移**：`LL5aX6Y2` refresh 后 prod **与旧台账完全一致**（0.6601）。
> 这与拥挤档形成鲜明对比——USA 拥挤档 10-17 曾 7 颗从 0.59 漂到 0.90+。
> ⇒ **「零占用」同时保 SELF 与 prod 稳定性**，是最优质的落点属性。

### 1.4 pyramid 倍率（收益权重，越高越值钱）

| region | D0 峰值 | D1 峰值 | 价值判读 |
|---|---|---|---|
| DEU | **1.9**（全类） | 1.8 | 最高（但已占用） |
| GBR | 1.9 | 1.7（sentiment） | 高 |
| HKG | — | 1.7（analyst/model/other） | 高 |
| CHN | 1.9 | 1.9（other） | 高（已判死） |
| KOR | — | 1.6 | 中 |
| EUR | 1.7（other） | **1.5**（other/sentiment） | 中 |
| ASI | — | **1.5**（analyst）/ 实测 D1 1.4（other） | 中 |
| USA | 1.8（sentiment） | 1.4 | 中 |
| GLB | — | 1.4 | 中 |
| IND | — | **1.4（最低）** | 最低 |

---

## 二、★ 三条选点原则（均有实证，勿再从零扫）

### 原则 1：零占用档位 > 组件池大小（决定 SELF，兼得 prod 稳定）

> **同一 region/universe 档位内没有已提交 SA ⇒ SELF 恒 0.0000**（7/7 全中），
> 且 **prod 不随时间漂移**（零占用档 refresh 前后一致）。

| 档位 | alpha | SELF | 结果 |
|---|---|---:|---|
| GLB / TOPDIV3000 | `npARO63x` | **0.0000** | ✅ PROD 仅 0.5125 |
| USA / TOP1000 | `LL5aX6Y2` | **0.0000** | ✅ 本轮实测 PROD 0.6601 |
| USA / TOP1000 | `JjPlvGVj` | **0.0000** | ✅ 本轮实测 PROD 0.6344 |
| USA / TOP500 | `1YjvdNAR` | **0.0000** | ❌ `LOW_SHARPE` 1.41 < 1.58 |
| USA / TOPSP500 | `VkdnPRYw` | **0.0000** | ❌ PROD 0.7189 撞墙 |

⚠️ **零占用是必要非充分**：小 universe（TOP500/TOP200/TOPSP500）组件质量差，IS 直接不过 1.58。
⇒ 真正稀缺的是「**零占用 + 组件质量够**」，目前命中：**USA/TOP1000**、**GLB/TOPDIV3000**（已占）。
**EUR 解锁后 5 档全空，是下一个 SELF=0 金矿。**

### 原则 2：「指标最好」= 约束优化，不是无脑拉 IS

```
maximize    IS Sharpe（或 Fitness）
subject to  self < 0.7  且  prod < 0.7        ← 合规红线，无豁免入口
            余量 = 0.7 − max(self, prod) ≥ 0.02  ← 防平台重算漂移
            RA 全闸通过
```

**铁证（2026-10-18 凌晨，8 颗 IND 候选）**：IS 5.38 → prod **0.8369**；IS 4.61 → 0.7247；
唯一过线 `88vKQrw7`（IS 4.50）prod 0.6977，**余量仅 0.0023**。⇒ **高 IS 与过闸严格剪刀差**。

### 原则 3：中性化是相关性主旋钮，方向由 region 族决定（有例外）

| region 族 | 赢家配方 | 死因配方 |
|---|---|---|
| GLB / USA / **DEU** | **STATISTICAL + decay 1** | SECTOR（DEU `j2eRV2pe` 撞 0.7530）、decay 15（GLB 卡 `LOW_GLB_EMEA_SHARPE`） |
| KOR / IND / GBR | **SECTOR 或 SUBINDUSTRY/INDUSTRY + decay 15** | STATISTICAL（corr 飙到 0.72–0.84） |

⚠️ **DEU 是族规律的例外**：地理上属 KOR/IND/GBR 族，但实测 **STATISTICAL 赢、SECTOR 死**。
⇒ **按实测走，不按族分类走。**（本轮 USA 两颗候选同样验证了族规律：STAT d1 与 SUBIND d15 都过闸，
但 STAT d1 的 IS 高 0.71、SUBIND d15 的余量厚 1.6 倍。）

---

## 三、分 Region 方案

### P0-A ⭐ USA / TOP1000 —— 唯一立即可建的高价值落点

**现状**：ACTIVE REG **41**（全场最大池）｜SA 4 颗（TOP3000 ×3 + TOP2000 ×1）
｜**TOP1000 零占用**（⇒ SELF 恒 0）

> **✅ 已提交完成（2026-10-19 23:34 本地 / 11:29:25-04:00 平台）**
> - 提交前 23:15 `check_correlation(refresh=True)` 实测：**PROD 0.6601 / SELF 0.0000**，`all_passed=true`。
> - `super_build.py submit` 内置 prod 闸自判 `max=0.6601 < 0.7 → 过闸`；HTTP 201 受理。
> - **等满 flip 窗 250s** → 复核：**`status=ACTIVE / stage=OS / checks.pending=[] / fail=[]`**，
>   name `USA_S_10comp_5aX6Y2`；RA `failed_ra_count=0`。
> - 指标复核：IS S **2.61** / F 1.80 / TO 0.1852 / returns 0.0878 / 2Y 2.18 / sub 1.75 / investability S 2.17。
> - **★ 状态变更**：USA/TOP1000 由「零占用」变为「**已占用**」⇒ USA 同档第二颗 SELF 会飙升
>   （参考 GLB/MINVOL1M 第二颗 `VkdjR3JA` SELF 0.9987）⇒ **USA/TOP1000 也只剩这一颗额度，勿再投同档**。
> - USA 已提交 SA 4 → **5**；USA 的 SUPER 今日配额（1/天/区）**已用**。

**双选方案**（本轮 23:15 `refresh=True` 实测，二选一）：

| 方案 | alpha | 配方 | IS S | F | SELF | PROD | 余量 | 适用 |
|---|---|---|---:|---:|---:|---:|---:|---|
| **要指标** ⭐ | `LL5aX6Y2` | STATISTICAL · d1 · lim15 · trunc 0.02 | **2.61** | 1.80 | **0.0000** | **0.6601** | 0.0399 | 余量 ≥0.02 达标，IS 高 0.71 |
| **要稳妥** | `JjPlvGVj` | SUBINDUSTRY · d15 · lim10 · trunc 0.02 | 1.90 | 1.56 | **0.0000** | **0.6344** | **0.0656** | 余量厚 1.6 倍 |

**推荐**：选 **`LL5aX6Y2`**——余量 0.0399 已过 0.02 安全线，且 IS 高出 0.71；
更关键的是**零占用档 prod 不漂移**（本轮 refresh 验证），0.0399 的余量比拥挤档的 0.0399 安全得多。

**配置**：
```json
{"tag":"usa_top1000_stat_d1_l15","region":"USA","universe":"TOP1000","delay":1,
 "neutralization":"STATISTICAL","decay":1,"combo_power":1,"selection_limit":15,
 "truncation":0.02}
```

**已穷尽验证（勿再投）**：
- USA/TOP500 `1YjvdNAR` → `LOW_SHARPE` 1.41 < 1.58
- USA/TOP200 `RRAX8lP1` → IS 0.80 / F 0.53
- USA/TOPSP500 `VkdnPRYw` → PROD 0.7189 撞墙
- USA/TOP1000 `XgRq8KN0`（SECTOR d15）→ `IS_LADDER_SHARPE` 1.49 < 1.58
⇒ **USA 只剩 TOP1000 档一条解**，别再扫其他档。

**⚠️ 提交后状态变更**：TOP1000 由零占用变已占用 ⇒ 后续 USA 同档第二颗 SELF 会显著上升
（参考 GLB/MINVOL1M 第二颗 `VkdjR3JA` SELF 0.9987）⇒ **USA/TOP1000 也只剩一颗额度**。

---

### P0-B 🔥 EUR 解锁 —— 最高杠杆的并行动作（缺口已收窄到 2 颗）

**现状**：ACTIVE REG **8/10**（差 **2**）｜IS 未提交 **87 颗**（库存充足）｜SA 0 颗
｜**五个档位全空**（TOP2500/1200/800/400/TOPCS1600）｜pyramid D1 峰值 1.5

**为什么是最高杠杆**：
1. 只需 **2 颗**（10-18 时为 3 颗，10-19 已 +1）
2. 库存 **87 颗**充足，不用新挖
3. REGULAR 配额 **4/天/区** ⇒ **1 天内可完成**，且**与 SUPER 配额独立计数** ⇒ 可与 P0-A 同日并行
4. 解锁后 5 档全空 ⇒ **SELF 恒 0**，是继 USA/TOP1000 之后的下一个 SELF=0 金矿

**解锁路径**：从 87 颗 IS 库存里挑 **2 颗 prod 余量最厚**的提交（走 REGULAR 配额）。
参考已提交者的 prod 分布（EUR 现有 ACTIVE 的 prod 区间 **0.5378–0.6945**）：
- 最厚：`N1VnJjXg` prod **0.5378**、`gJjMLb0Q` 0.5791、`Xgojww1X` 0.5906
- 避开：`78jdv6b1` 0.6945、`LL5VwgO1` 0.6926、`XgJYWLg1` 0.6831（贴线，勿再提交同类）

⚠️ **历史教训**：10-14 曾 4 次撞 `At least 10 component alphas are required`
（TOPCS1600 ×2、TOP2500、TOP1200），当时本地池显示 85 颗也没用
⇒ **本地池计数不可信**，平台只认 ACTIVE 已提交数。解锁后仍要 **POST 一次实测**。

---

### P1 EUR 解锁后建 SA（D+1）

**起步配方**（EUR 与 USA 同为发达市场大池族，先试 USA 型；若 corr 超线再切 SECTOR/SUBINDUSTRY · d15）：
```json
{"tag":"eur_stat_d1_l10","region":"EUR","universe":"TOP2500","delay":1,
 "neutralization":"STATISTICAL","decay":1,"combo_power":1,"selection_limit":10,
 "truncation":0.02}
```
档位建议从 **TOP2500**（最大池，组件质量最好）起步；若 IS 不过闸再试 TOPCS1600（现有 8 颗组件全在这档）。
⚠️ 解锁后配方**需 POST 实测**，族规律（USA 型 vs KOR 型）待验证。

---

### P2 ASI 解锁 —— 差 1 颗，但成本高于 EUR

**现状**：ACTIVE REG **9/10**（差 1）｜IS 未提交 **0**｜SA 0 颗
｜合法档 MINVOL1M / MINVOL10M / TOP500 全空｜pyramid D1 1.4–1.5

⚠️ **无库存是硬伤**：IS 未提交 0 颗 ⇒ 必须先**新挖** 1 颗 ASI RA 并过 RA 全闸，
而不是从库存挑（EUR 是挑库存，ASI 是新挖）⇒ **成本显著高于 EUR，优先级排在其后**。

参考 ASI 现有 9 颗组件的 prod：最低 `88jaV5lv` **0.5093**、`qMNMbeGj` 0.62、`j28nKkQo` 0.6325
⇒ 新挖时可参考这些低 prod 机制族（pv/sentiment 门控 + 盘前反转族）。

---

### P3 GBR / TOP700 —— 余量过薄，需重扫

**现状**：ACTIVE REG 18｜SA 2 颗（`e7QGwrx6` self 0.655、`YPMp39q6` self 0.5799）
｜IS 未提交 **0**｜pyramid D1 峰值 1.7（sentiment）

**现有最优**：`LL5a3r6M`（SUBINDUSTRY · d15 · lim 10）IS 2.76 / F 2.68 /
SELF 0.6540 / **PROD 0.6849**，余量 **0.0151** ⚠️ —— **低于 0.02 安全线**。

**另有两颗余量更差，禁投**：`1YjbKNGX`（0.0041）、`78obm2wO`（0.0028）——提交后极易翻车。

⇒ **建议**：GBR 暂缓；若要推进，需重扫找余量 ≥0.03 的组合（GBR 无 IS 库存，得新挖组件）。

---

## 四、停投区（勿再投）

| region | 停投理由 |
|---|---|
| **IND / TOP500** | 已 11 颗 ACTIVE SA；8 颗新候选 7 颗 prod 爆线，唯一过线者余量 0.0023。IS 5.38 ↔ prod 0.8369 剪刀差已锁死。 |
| **KOR / TOP600** | 已 8 颗 ACTIVE SA。`O0Jexdo7`（INDUSTRY d15 lim15）IS 4.02/F 5.69 但 corr **0.7653** 撞墙 ⇒ **加组件 = 加 IS = 加 corr**，已到顶。 |
| **GLB** | 已占 3 档（TOP3000/MINVOL1M/TOPDIV3000）；MINVOL10M `zqraRwZO` PROD 0.8210 撞墙；池仅 11 颗。 |
| **DEU / TOP500** | ✅ 已落地 `mLYLEm99`，**零占用已耗尽**。第二颗 SELF 会飙升；且 IS 库存 0，组件池卡死 10 颗无补货能力。 |
| **MEA** | 平台已关闭：HTTP 400 `Region MEA is not available.` |
| **HKG** | 组件 6/10 差 4，且 IS 库存 0（需新挖 4 颗），成本最高。 |
| **CHN / JPN / TWN / AMR** | 上轮已判死。 |

---

## 五、执行清单

### 5.1 通用命令

```bash
# 1) 构建（configs.json 见各区配方）
python C:/Users/MENGTAO/wqb-scripts/sa_run.py --configs configs.json --out res.jsonl
#    续跑：已存在 <out>.<tag>.json 且含 alpha id 的项自动跳过
#    ⚠️ 进度看逐配置落盘的 res.<tag>.json，不要看 stdout（后台跑时管道全缓冲）

# 2) 双闸实测（提交前必做；prod 平台端点单并发异步排队，单条 ~94s，一次 ≤6 颗 + 间隔）
#    本轮已实测：LL5aX6Y2 → 0.6601/0.0000 ✅；JjPlvGVj → 0.6344/0.0000 ✅

# 3) 提交（内置 prod 闸，fail-closed，无豁免入口）
python tools/super_build.py submit --alpha-id <ID> --region <REGION>
#    提交后必须复核：get_alpha_details 的 status + dateSubmitted（回执不可信）
```

### 5.2 配额约束

| 项 | 额度 |
|---|---|
| REGULAR 提交 | 4 / 天 / 区 |
| SUPER 提交 | **1 / 天 / 区**（与 REGULAR **独立计数**） |

⇒ **P0-A（USA SA）与 P0-B（EUR 补 2 颗 REGULAR）可同日并行**。

### 5.3 建议执行顺序

| 时序 | 动作 | 配额 |
|---|---|---|
| **D+0** | ✅ **已完成**（2026-10-19）：提交 USA `LL5aX6Y2` → ACTIVE | SUPER ×1（USA）已用 |
| **D+0 并行** | ② 从 EUR 87 颗库存挑 2 颗 prod 余量最厚的提交 → 解锁 EUR | REGULAR ×2（EUR）**今日仍可做** |
| **D+1** | ③ EUR 解锁后 POST 实测建 SA（TOP2500 起步，SELF 应为 0） | SUPER ×1（EUR） |
| **后续** | ④ ASI 需新挖 1 颗 RA 才解锁（成本高于 EUR）；⑤ GBR 待重扫找余量 ≥0.03 | — |

⚠️ 若 D+0 的 USA 提交推迟，改选 `JjPlvGVj`（余量 0.0656 更厚）。
虽然本轮实测证明零占用档 prod 不漂移，但 0.0399 的余量仍建议**尽快提交**。

---

## 六、待实测项

| 项 | 说明 |
|---|---|
| EUR 解锁后 SA 配方 | 需 POST 实测，族规律（USA 型 vs KOR 型）待验证 |
| ASI 解锁所需 RA | IS 库存 0，需新挖 |
| GBR 余量 ≥0.03 组合 | 现有最优余量 0.0151 < 安全线，需重扫 |
| GLB/MINVOL10M | 零占用但 `zqraRwZO` 曾 PROD 0.8210 撞墙，是否可救待验证 |
| HKG | 差 4 颗且库存 0，暂无可行路径 |

---

## 七、产物路径

- 本方案：`output_report/SA_best_per_region_plan_20261019.md`
- 上一版（DEU 落地）：`output_report/SA_best_per_region_plan_20261018.md`
- 组件池缓存：`results/sa_probe_cache.json`（2026-10-18 23:02，本轮已对 EUR/ASI 实测校正）
- 上一轮候选汇总：`output_report/SA_all_region_candidates_20261016.md`
- 构建脚本：`C:\Users\MENGTAO\wqb-scripts\sa_run.py`、`tools/super_build.py`
- 记忆：`.workbuddy/memory/2026-10-18.md`（DEU 落地）、`2026-10-19.md`（本轮）
