# 各 Region 最优 SuperAlpha 构建方案

生成时间：2026-10-18 23:05（本地）
数据口径：**全部基于平台真实仿真 + 平台双闸实测**（组件池盘点为 2026-10-18 23:04 强制 `--refresh` 拉取；
双闸读数为平台 `check_correlation` 实测值，非本地估算）。

> **只挖不提交**：本方案全部为**待执行配方**，未做任何提交动作。提交须你点名。

---

## 〇、执行摘要：按价值排序的优先队列

| 优先级 | region / 档位 | 最优配方 | 预期 IS S | F | SELF | PROD | 余量 | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---|
| **P0** | **DEU / TOP500** | STATISTICAL · decay 1 · lim 10 · trunc 0.02 | 2.27 | 1.67 | 0.6110 | 0.6108 | **0.0890** | ✅ **已提交 ACTIVE**（2026-10-18T11:20:12-04:00，name `DEU_S_10comp_YLEm99`） |
| **P1** | **USA / TOP1000** | STATISTICAL · decay 1 · lim 15 | 2.61 | 1.80 | **0.0000** | 0.6601 | 0.0399 | 待提交（`LL5aX6Y2`）<br>稳选 `JjPlvGVj` 余量 0.0656 |
| **P2** | **EUR**（差 3 颗解锁） | 先补 3 颗 RA → STATISTICAL · d1 | — | — | — | — | — | 解锁后实测 |
| **P3** | **ASI**（差 1 颗解锁） | 先补 1 颗 RA → 实测 | — | — | — | — | — | 解锁后实测 |
| P4 | GBR / TOP700 | SUBINDUSTRY · decay 15 · lim 10 | 2.76 | 2.68 | 0.6540 | 0.6849 | 0.0151 ⚠️ | 余量过薄，需重扫 |
| — | IND / KOR / GLB | — | — | — | — | — | — | **已饱和，停投** |

**一句话结论**：新 SA 的唯一高价值落点是 **DEU/TOP500**——它是唯一同时满足
「零占用（0 颗已提交 SA）+ 组件池刚达标（10/10）+ pyramid 倍率全场最高（D0 全类 1.9）」的区域。
USA/TOP1000 是次优（零占用档 ⇒ SELF 恒 0）。IND/KOR/GLB 已到顶，再投只是撞墙。

---

## 一、数据基线（2026-10-18 23:04 平台实测）

### 1.1 组件池 eligibility（硬前置 ≥10 颗 ACTIVE 已提交 REGULAR）

| region | ACTIVE 已提交 | IS 未提交库存 | verdict | 已提交 SA | 判读 |
|---|---:|---:|---|---:|---|
| USA | **41** | 324 | GO | 4 | 池最大，可补组件 |
| IND | **36** | 436 | GO | 19（11 ACTIVE + 8 待提交） | 池大但已饱和 |
| KOR | **26** | 103 | GO | 8 | 已到顶 |
| GBR | **18** | 0 | GO | 2 | 池够，无补货能力 |
| MEA | 19 | 0 | GO | 2 | ❌ **平台已不支持**（400 `Region MEA is not available`） |
| GLB | **11** | 0 | GO | 4 | 四档全占，已到顶 |
| DEU | **10** | **0** | GO | **1**（`mLYLEm99`，2026-10-18） | ✅ 已落地；刚达标，**无补货能力**（IS 库存 0） |
| EUR | 7 | **87** | BLOCKED（差 3） | 0 | 库存足，待解锁 |
| ASI | 9 | 0 | BLOCKED（差 1） | 0 | 差 1 颗，无库存 |
| HKG | 6 | 0 | BLOCKED（差 4） | 0 | 差 4 颗，无库存 |

### 1.2 已占档位 vs 零占用档位（★ 决定 SELF 的关键）

| region | 合法 universe（平台） | 已被 SA 占用 | **零占用档** |
|---|---|---|---|
| USA | TOP3000/2000/**1000/500/200/TOPSP500** | TOP3000 ×3、TOP2000 ×1 | **TOP1000、TOP500、TOP200、TOPSP500** |
| GLB | TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000 | **全 4 档已占** | 无 |
| IND | TOP500 | TOP500 ×11 | 无 |
| KOR | TOP600 | TOP600 ×8 | 无 |
| GBR | TOP700 | TOP700 ×2 | 无 |
| ~~DEU~~ | TOP500 | ~~无~~ → **TOP500 ×1**（`mLYLEm99` 2026-10-18） | ❌ **零占用已耗尽，短期勿再投** |
| EUR | TOP2500/1200/800/400/TOPCS1600 | 无 | 全空（但组件不足） |
| ASI | MINVOL1M/MINVOL10M/TOP500 | 无 | 全空（组件差 1） |
| HKG | TOP800/TOP500 | 无 | 全空（组件差 4） |

### 1.3 pyramid 倍率（收益权重，越高越值钱）

| region | D0 峰值 | D1 峰值 | 价值判读 |
|---|---|---|---|
| **DEU** | **1.9**（model/news/other/pv/earnings/insiders/analyst/sentiment/fundamental 全 1.9） | 1.8 | ⭐ **全场最高** |
| GBR | 1.9 | 1.7（sentiment） | 高 |
| HKG | — | 1.7（analyst/model/other） | 高 |
| CHN | 1.9 | 1.9（other） | 高（但已判死） |
| KOR | — | 1.6（analyst/fundamental/model/news/other/sentiment） | 中 |
| EUR | 1.7（other） | 1.5（other/sentiment） | 中 |
| ASI | — | 1.5（analyst） | 中 |
| USA | 1.8（sentiment） | 1.4（other/sentiment） | 中 |
| GLB | — | 1.4（fundamental/analyst/sentiment） | 中 |
| IND | — | **1.4（analyst）** | **最低** |

> **DEU 是收益倍率最高的空白区**：D0 几乎全类 1.9，等于同指标 SA 在 DEU 的计分权重
> 比 IND（1.4）高约 **36%**。这是把 DEU 排 P0 的第二个理由（第一个是零占用）。

---

## 二、★ 三条选点原则（本轮全部有实证，勿再从零扫）

### 原则 1：零占用档位 > 组件池大小（决定 SELF）

> **同一 region/universe 档位内没有已提交 SA ⇒ SELF 恒为 0.0000**（5/5 全中）。

| 档位 | alpha | SELF | 结果 |
|---|---|---:|---|
| GLB / TOPDIV3000 | `npARO63x` | **0.0000** | ✅ 过闸（PROD 仅 0.5125，余量 0.1875） |
| USA / TOP1000 | `LL5aX6Y2` | **0.0000** | ✅ 过闸 |
| USA / TOP1000 | `JjPlvGVj` | **0.0000** | ✅ 过闸 |
| USA / TOP500 | `1YjvdNAR` | **0.0000** | ❌ `LOW_SHARPE` 1.41 < 1.58 |
| USA / TOPSP500 | `VkdnPRYw` | **0.0000** | ❌ PROD 0.7189 撞墙 |

⚠️ **零占用只保 SELF、救不了 IS 和 PROD**：小 universe（TOP500/TOP200/TOPSP500）的组件
质量太差，IS 直接不过 1.58。⇒ **零占用是必要非充分条件**，真正稀缺的是
「零占用 **+** 组件质量够」，目前只有 GLB/TOPDIV3000、USA/TOP1000 命中。

### 原则 2：「指标最好」= 约束优化，不是无脑拉 IS

**IS Sharpe 与 corr 严格正相关**（20+ 次实证）。形式化：

```
maximize    IS Sharpe（或 Fitness）
subject to  self < 0.7  且  prod < 0.7        ← 合规红线，无豁免
            余量 = 0.7 − max(self, prod) ≥ 0.02  ← 防平台重算漂移
            RA 全闸通过
```

**最新铁证（2026-10-18 凌晨实测，8 颗 IND 未提交 SA 候选）**：

| alpha | IS Sharpe | F | lim | **PROD** | 判定 |
|---|---:|---:|---:|---:|---|
| `omo9g1qn` | **5.38** | 5.10 | 10 | **0.8369** | ❌ 最高 IS = 最爆线 |
| `Grg3eoJO` | 4.61 | 5.00 | 15 | 0.7247 | ❌ |
| `KPmwEz0l` | 4.60 | 4.73 | 20 | 0.7016 | ❌ |
| `88vKQrw7` | 4.50 | 4.68 | 10 | **0.6977** | ✅ 唯一过线（余量仅 **0.0023** ⚠️） |
| `d5Kl0zxg` | 4.46 | 4.61 | 10 | 0.7013 | ❌ 差 0.0013 |
| `omo9oaov` | 4.49 | 4.51 | 10 | 未测 | 待测 |
| `QPY5VGGK` | 4.47 | 4.63 | 10 | 0.7002 | ❌ 差 0.0002 |
| `KPmwGwdl` | 3.53 | 4.15 | 10 | 0.7137 | ❌ |

⇒ **IND/TOP500 已彻底到顶**：IS 5.38 的候选 prod 0.8369，唯一过线的余量 0.0023
（按「prod 每月上漂 ~0.10」的经验，两周内必翻车）。**IND 停投。**

### 原则 3：中性化是相关性主旋钮，但方向由 region 族决定

| region 族 | 赢家配方 | 死因配方 |
|---|---|---|
| GLB / USA / **DEU** | **STATISTICAL + decay 1** | SECTOR（DEU `j2eRV2pe` 撞 0.7530）、decay 15（GLB 卡 `LOW_GLB_EMEA_SHARPE`） |
| KOR / IND / GBR | **SECTOR 或 SUBINDUSTRY/INDUSTRY + decay 15** | STATISTICAL（corr 飙到 0.72–0.84） |

⚠️ **DEU 是这条规律的例外**：DEU 属「KOR/IND/GBR 族」的地理分类，但实测
**STATISTICAL 赢、SECTOR 死**（`j2eRV2pe` SECTOR 0.7530 撞墙）。
⇒ **按实测走，不按族分类走。**

---

## 三、分 Region 方案

### P0 ⭐ DEU / TOP500 —— 本轮唯一高价值落点（✅ 已于 2026-10-18 落地）

**现状（提交前）**：ACTIVE REG 10/10（刚达标）｜SA **0 颗**（完全空白）｜pyramid D0 全类 **1.9**
｜IS 未提交库存 **0**（⇒ 组件池卡死在 10，无补货能力，lim 加大会失效）

> **✅ 已提交完成（2026-10-18 23:20 本地 / 11:20:12-04:00 平台）**
> - 提交前 `check_correlation(refresh=True)` 强制回源实测：**PROD 0.6108 / SELF 0.6110**，余量 0.0890。
>   注：refresh 后与 10-16 台账**完全一致** ⇒ DEU 这个零占用档**未发生漂移**。
> - 内置 prod 闸自判过闸 → HTTP 201 受理 → **等满 flip 窗 250s** → 复核
>   **`status=ACTIVE / stage=OS / checks.pending=[] / fail=[] warning=[]`**，name `DEU_S_10comp_YLEm99`。
> - **★ 状态变更**：DEU/TOP500 由「零占用」变为「**已占用**」⇒ 后续 DEU 同档第二颗 SELF 会显著上升
>   （参考 GLB/MINVOL1M 第二颗 `VkdjR3JA` SELF 0.9987）⇒ **DEU 短期勿再投同档**。

**推荐配方**（实证 PASS，余量全场第二厚）：

```json
{"tag":"deu_stat_d1_l10","region":"DEU","universe":"TOP500","delay":1,
 "neutralization":"STATISTICAL","decay":1,"combo_power":1,"selection_limit":10,
 "truncation":0.02}
```

**预期指标**（`mLYLEm99`，2026-10-16 实测）：

| IS Sharpe | Fitness | Turnover | SELF | PROD | 余量 |
|---:|---:|---:|---:|---:|---:|
| 2.27 | 1.67 | 0.1667 | 0.6110 | 0.6108 | **0.0890** |

**备选**：
- `j2eLrEMj`（STATISTICAL · decay 15 · cp3 · lim10）：IS 1.87 / F 1.44，余量 **0.1063**
  —— 余量更厚但 IS 低 0.40，**弃 IS 换余量不划算**，作保底方案。
- `kqJrL9ld`（同配方 lim 15）：指标与 `mLYLEm99` **一字不差** ⇒ DEU 池只有 10 颗，
  **lim 加到 15 无效**，lim 10 即可，别浪费仿真。

**已穷尽验证（勿再投）**：DEU/SECTOR（`j2eRV2pe`）撞墙 0.7530。

**执行清单**：
1. 复用 `mLYLEm99`（已建，直接走提交）；若需重建则用上面 configs。
2. **提交前必须 `check_correlation(refresh=True)` 重测 PROD**（台账读数超过 48h 即不可信）。
3. `super_build.py submit --alpha-id mLYLEm99 --region DEU`（内置 prod 闸，fail-closed）。

---

### P1 USA / TOP1000 —— 零占用档，SELF 恒 0

**现状**：ACTIVE REG **41**（全场最大池）｜SA 4 颗（TOP3000 ×3 + TOP2000 ×1）
｜TOP1000/500/200/TOPSP500 **全零占用**

**双选方案**（按你的风险偏好二选一）：

| 方案 | alpha | 配方 | IS S | F | SELF | PROD | 余量 | 适用 |
|---|---|---|---:|---:|---:|---:|---:|---|
| **要指标** | `LL5aX6Y2` | STATISTICAL · d1 · lim 15 | **2.61** | 1.80 | **0.0000** | 0.6601 | 0.0399 | 余量仍 ≥0.02，IS 高 0.71 |
| **要稳妥** | `JjPlvGVj` | SUBINDUSTRY · d15 · lim 10 | 1.90 | 1.56 | **0.0000** | **0.6344** | **0.0656** | 余量厚 1.6 倍 |

**推荐**：选 **`LL5aX6Y2`**（余量 0.0399 达标，IS 高 0.71），但**必须 48h 内提交**
（余量 0.04 扛不住一个月的漂移）。若拖延则改用 `JjPlvGVj`。

**已穷尽验证（勿再投）**：
- USA/TOP500 `1YjvdNAR` → `LOW_SHARPE` 1.41 < 1.58
- USA/TOP200 `RRAX8lP1` → IS 0.80 / F 0.53
- USA/TOPSP500 `VkdnPRYw` → PROD 0.7189 撞墙
- USA/TOP1000 `XgRq8KN0`（SECTOR d15）→ `IS_LADDER_SHARPE` 1.49 < 1.58
⇒ **USA 只剩 TOP1000 档一条解**，别再扫其他档。

---

### P2 EUR —— 差 3 颗解锁，库存 87 颗（最高杠杆的解锁动作）

**现状**：ACTIVE REG **7/10**（差 3）｜IS 未提交 **87 颗**（库存充足）｜SA 0 颗
｜pyramid D1 峰值 1.5（other/sentiment）

**解锁路径**：提交 **3 颗 EUR 的 RA**（REGULAR 配额 4/天/区 ⇒ **1 天内可完成**），
ACTIVE 组件 7 → 10 即解锁。从 87 颗 IS 库存里挑 prod 余量最厚的 3 颗。

⚠️ **历史教训**：10-14 曾 4 次撞 `At least 10 component alphas are required`
（TOPCS1600 ×2、TOP2500、TOP1200），当时本地池显示 85 颗也没用
⇒ **本地池计数不可信**，平台只认 ACTIVE 已提交数。解锁后仍要 **POST 一次实测**。

**解锁后配方建议**：先试 STATISTICAL · d1 · lim10（EUR 与 USA 同为发达市场大池族），
若 corr 超线再切 SECTOR/SUBINDUSTRY · d15。

---

### P3 ASI —— 差 1 颗解锁（成本最低）

**现状**：ACTIVE REG **9/10**（差 1）｜IS 未提交 **0**｜SA 0 颗
｜pyramid D1 峰值 1.5（analyst）｜合法档 MINVOL1M / MINVOL10M / TOP500

⚠️ **无库存是硬伤**：IS 未提交 0 颗 ⇒ 必须先**新挖** 1 颗 ASI RA 并过 RA 全闸，
而不是从库存挑。成本显著高于 EUR。

---

### P4 GBR / TOP700 —— 余量过薄，需重扫

**现状**：ACTIVE REG 18｜SA 2 颗（`e7QGwrx6` self 0.655、`YPMp39q6` self 0.5799）
｜IS 未提交 **0**｜pyramid D1 峰值 1.7（sentiment）

**现有最优**：`LL5a3r6M`（SUBINDUSTRY · d15 · lim 10）IS 2.76 / F 2.68 /
SELF 0.6540 / **PROD 0.6849**，余量 **0.0151** ⚠️ —— 低于 0.02 安全线。

**另有两颗余量更差，禁投**：`1YjbKNGX`（0.0041）、`78obm2wO`（0.0028）——
**提交后极易翻车**。

⇒ **建议**：GBR 暂缓，先做 P0/P1/P2；若要推进，需重扫 GBR 找余量 ≥0.03 的组合
（GBR 无 IS 库存，得新挖组件）。

---

### 停投区：IND / KOR / GLB

| region | 停投理由 |
|---|---|
| **IND / TOP500** | 已 11 颗 ACTIVE SA；8 颗新候选 7 颗 prod 爆线，唯一过线者余量 0.0023。IS 5.38 ↔ prod 0.8369 的剪刀差已锁死。 |
| **KOR / TOP600** | 已 8 颗 ACTIVE SA。`O0Jexdo7`（INDUSTRY d15 lim15）把 IS 推到 4.02/F 5.69，但 corr 直接 **0.7653** 撞墙 ⇒ **加组件 = 加 IS = 加 corr**，已到顶。 |
| **GLB** | 四档全占；MINVOL10M `zqraRwZO` PROD 0.8210 撞墙；池仅 11 颗。零占用已耗尽。 |
| **MEA** | 平台已关闭：HTTP 400 `Region MEA is not available.` + `Neutralization STATISTICAL is not available ... region MEA`。 |
| **CHN / JPN / TWN / AMR** | 上轮已判死，勿再投。 |

---

## 四、撞墙档案（勿重复投）

| alpha | 档位 | IS S | SELF | PROD | 死因 |
|---|---|---:|---:|---:|---|
| `VkdjR3JA` | GLB/MINVOL1M | 6.89 | **0.9987** | 0.6091 | 同档第二颗，SELF 爆表 |
| `omo9g1qn` | IND/TOP500 | **5.38** | — | 0.8369 | 最高 IS = 最爆 prod |
| `rKdmGg1j` | KOR/TOP600 | 4.87 | 0.7400 | 0.7400 | 双闸同撞 |
| `Vkdjzndb` | USA/TOP3000 | 4.73 | 0.7418 | 0.7422 | corr + `LOW_SUB_UNIVERSE_SHARPE` 2.00<2.05 |
| `omo5Eqzl` | IND/TOP500 | 5.39 | 0.8316 | 0.8316 | corr 严重 |
| `E5VWmNXK` | GBR/TOP700 | 4.25 | 0.8413 | 0.8412 | corr 严重 |
| `O0Jexdo7` | KOR/TOP600 | 4.02 | 0.7655 | 0.7653 | INDUSTRY d15 lim15，IS↑corr↑ |
| `j2eRV2pe` | DEU/TOP500 | 2.32 | 0.7530 | 0.7529 | SECTOR 撞墙 |
| `1Yjvdllm` | USA/TOP3000 | 3.24 | 0.7209 | 0.7707 | SUBINDUSTRY 撞墙 |
| `gJWvMd1M` / `O0JeZ6mv` | IND/TOP500 | 4.16 / 4.17 | 0.7003 / 0.7010 | 0.7005 / 0.7011 | **差 0.0005 撞墙** |
| `9qEorzmK` / `78oO1bq1` / `leMxlzAN` | GLB/TOPDIV3000 | 2.70 / 2.67 / 2.65 | 0.0 | 0.62 | `LOW_GLB_EMEA_SHARPE` 0.91/0.85/0.89 < 1 |
| `XgRq8KN0` | USA/TOP1000 | 1.84 | 0.0000 | 0.6782 | `IS_LADDER_SHARPE` 1.49 < 1.58 |
| `VkdnPRYw` | USA/TOPSP500 | 1.28 | 0.0000 | 0.7189 | PROD 撞墙 |

---

## 五、执行清单

### 5.1 通用构建命令

```bash
# 1) 构建（configs.json 见各区配方）
python C:/Users/MENGTAO/wqb-scripts/sa_run.py --configs configs.json --out res.jsonl
#    续跑：已存在 <out>.<tag>.json 且含 alpha id 的项自动跳过
#    ⚠️ 进度看逐配置落盘的 res.<tag>.json，不要看 stdout（后台跑时管道全缓冲）

# 2) 双闸实测（提交前必做，台账 >48h 一律重测）
#    prod 平台端点为单并发异步排队，单条 ~94s，一次 ≤6 颗 + 间隔（防限流）

# 3) 提交（内置 prod 闸，fail-closed，无豁免入口）
python tools/super_build.py submit --alpha-id <ID> --region <REGION>
#    提交后必须复核：get_alpha_details 的 status + dateSubmitted（回执不可信）
```

### 5.2 配额约束

| 项 | 额度 |
|---|---|
| REGULAR 提交 | 4 / 天 / 区 |
| SUPER 提交 | **1 / 天 / 区** |

⇒ P0（DEU）+ P1（USA）**同一天可各提交 1 颗**；EUR 解锁可在同日并行
（用 REGULAR 配额，与 SUPER 独立计数）。

### 5.3 建议执行顺序

1. ✅ **已完成（2026-10-18）**：提交 DEU `mLYLEm99` → ACTIVE。
2. **下一步**：USA `LL5aX6Y2`（TOP1000 仍是零占用档，SELF 恒 0；余量 0.0399 ⇒ **必须 48h 内提交**，否则改稳选 `JjPlvGVj` 余量 0.0656）。
   ⚠️ SUPER 配额 1/天/区 ⇒ USA 须**次日**才能提交（DEU 当日额度已用）。
3. **D+0 并行**：从 EUR 87 颗 IS 库存里挑 3 颗 prod 余量最厚的提交，解锁 EUR（走 REGULAR 配额，与 SUPER 独立计数）。
4. **D+1**：EUR 解锁后 POST 一次实测建 SA（STATISTICAL · d1 · lim10 起步）。
5. **后续**：ASI 需新挖 1 颗 RA 才解锁，优先级低于 EUR；GBR 待重扫。

---

## 六、待实测项（本方案未覆盖，需真仿真补）

| 项 | 说明 |
|---|---|
| `omo9oaov`（IND） | 8 颗候选中唯一无 prod 缓存者，需 `check_correlation` 补测 |
| 8 颗 IND 候选的 **SELF** | 全部为 None（只测了 prod），如需提交须补测 self |
| DEU `mLYLEm99` 的当前 prod | 台账 0.6108 为 10-16 读数，**提交前必须 refresh 重测** |
| EUR 解锁后的 SA 配方 | 需 POST 实测，族规律（USA 型 vs KOR 型）待验证 |
| ASI 解锁所需 RA | IS 库存 0，需新挖 |

---

## 七、产物路径

- 组件池盘点：`results/sa_candidates_20261018-230440.json`（+ 主缓存 `results/sa_probe_cache.json`）
- 上一轮候选汇总：`output_report/SA_all_region_candidates_20261016.md`（18 颗真 PASS 全表）
- 构建脚本：`C:\Users\MENGTAO\wqb-scripts\sa_run.py`、`tools/super_build.py`、`sa_pool_review.py`
- 记忆：`D:\coding\traeCN_project\wqb\.workbuddy\memory\2026-10-18.md`
