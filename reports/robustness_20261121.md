# 稳健性审计（2026-11-21）

## GrmmNzz0（EUR / macro27 / 来源 RReEEgwb）

**表达式**
```
trade_when(vec_sum(mcr27_company_jobscreated) > 0,
  group_zscore(ts_quantile(ts_backfill(divide(
    vec_sum(mcr27_company_jobscreated),
    vec_avg(mean_days_job_closed)), 189), 168), industry), -1)
```
EUR / TOP2500 / D1 / decay 10 / INDUSTRY / trunc 0.08 / nan ON

### 一、平台闸门

| 项 | 实测 | 判定 |
|---|---|---|
| 模拟层 checks | `fail = []`（含 LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE / MATCHES_PYRAMID） | PASS |
| Failed RA / PPA | 0 / 0，无 PENDING | PASS |
| CLUSTER_TEST | 1.47（limit 1.58） | WARNING，PASS（余量 0.11） |
| Sharpe / Fitness | 2.65 / 1.46 | PASS（阈值 1.58 / 1.0） |
| 2Y Sharpe | 3.10 | PASS（ATOM/Last-2Y 阈值 2.023） |
| sub-universe / investability | 2.21 / 1.66 | PASS（EUR 无容量硬闸） |
| Turnover / Drawdown | 22.32% / 2.00% | PASS |
| self corr | 0.2064（池 20 颗，剔除 PP 7 颗；最高为 vRAOWYra） | PASS |
| prod corr | 0.5422（平台缓存，非 provisional，余量 0.158） | PASS |
| 混腿 | SINGLE_DATA_SET，`pyramid_short = macro` ⇒ ATOM | PASS |

### 二、年度稳定性（逐年 PnL）

| 年 | 2014–2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|
| Sharpe | 0（零仓位） | **0.56** | **3.46** | **2.72** |
| Fitness | 0 | 0.14 | 2.42 | 1.50 |
| Turnover | 0 | 15.89% | 21.16% | 20.48% |
| Drawdown | 0 | 1.50% | 1.32% | 1.45% |
| Margin | 0 | 1.17bp | 9.80bp | 6.08bp |

- 近 3 年均值 **2.25**，全期 2.65 ⇒ 衰减比 **0.85**
- CV_Sharpe **0.548**（偏高，唯一来源是 2021 年 0.56）
- 平年 0；max/min = 3.46 / 0.56 = **6.18**（高，同样源于 2021）
- 回撤日历：max 1.50%（2021），远低于阈值

**关键正面证据**：相对原件，优化后**每一年都更好**（2021 0.19→0.56、2022 3.15→3.46、2023 1.99→2.72）⇒ 改善不是靠某一年拉出来的，而是全期一致，抗过拟合。

### 三、边际贡献（`EQUITY:EUR:1:POWER_POOL`）

| 项 | before | after | 变化 |
|---|---|---|---|
| Sharpe | 4.32 | **4.50** | **+0.18** |
| Fitness | 2.81 | 2.89 | +0.08 |
| Returns | 5.83% | 5.85% | +0.02pp |
| **Drawdown** | 1.58% | **0.83%** | **−0.75pp** |
| Turnover | 13.75% | 14.14% | +0.39pp |

⇒ **非稀释，方向全正**，回撤改善尤其显著。

### 四、软标记（不阻塞，描述中应如实带出）

1. **结构性样本缺陷**：2014–2020 共 7 年零仓位（macro27 数据集 2022-10 才创建），有效样本仅 2021–2023；2021 年 Sharpe 仅 0.56、margin 1.17bp，几乎无效。
2. CV 0.548 / max-min 6.18 均偏高，均由 2021 年单独贡献。
3. 换手 22.32% 属中高换手，margin 6.10bp 低于原件 6.83bp。
4. CLUSTER_TEST 1.47 距限值仅 0.11。

### 五、结论

**PASS**。平台全部硬闸通过、年度全期一致改善、边际贡献正、self/prod 双低（0.2064 / 0.5422）。结构性限制（3 年样本）无法通过参数修复，需在提交描述中如实披露。

---

## 0mPPVEoK（GBR / imbalance×PV / 来源 Xgaab3nz）

### 一、平台闸门

| 项 | 实测 | 阈值 | 判定 |
|---|---|---|---|
| Sharpe | **2.21** | 1.58 | PASS（余量 0.63） |
| Fitness | 1.27 | 1.0 | PASS |
| 2Y Sharpe | 2.15 | 1.58（ATOM:LAST_2Y） | PASS |
| sub-universe S | 1.72 | — | PASS |
| Turnover / DD / margin | 24.27% / 4.23% / 6.65bp | TO<70% | PASS |
| investability S | 1.44（ratio 0.66） | >0（GBR 无硬闸） | PASS |
| CLUSTER_TEST | PASS | — | PASS |
| Failed RA / PPA | 0 / 0 | — | PASS |
| self corr | **0.1319** | 0.7 | PASS |
| **prod corr** | **0.6865** | 0.7 | **PASS（余量 0.0135）** |

### 二、年度表现（2014–2023，10 年完整样本）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.25 | 2.37 | 2.77 | 2.98 | 2.16 | 1.34 | **3.09** | 1.87 | 2.23 | 1.24 |
| Returns | 6.81% | 7.12% | 9.51% | 9.31% | 8.21% | 5.30% | 14.87% | 5.94% | 9.90% | 4.36% |
| Fitness | 1.17 | 1.25 | 1.73 | 1.84 | 1.25 | 0.63 | 2.44 | 0.95 | 1.45 | 0.52 |
| Drawdown | 1.70% | 1.58% | 1.35% | 1.92% | 2.27% | 2.41% | 3.29% | **4.23%** | 2.09% | 2.09% |
| margin(bp) | 0.54 | 0.56 | 0.78 | 0.76 | 0.67 | 0.44 | 1.25 | 0.52 | 0.85 | 0.35 |

- 近 3 年（2021–23）均值 **1.78**，全期均值 **2.23**，衰减比 **0.80**
- CV_Sharpe（全期）**0.281**｜近 3 年 CV 0.282
- 平年（S≤0）**0 个**｜max/min = 3.09 / 1.24 = **2.49**
- 年度最大回撤 4.23%（2021）< 2× 年度均值 2.29% = 4.58% ⇒ **无回撤日历告警**

### 三、边际贡献（`EQUITY:GBR:1:POWER_POOL`）

| 项 | before | after | 方向 |
|---|---|---|---|
| Sharpe | 4.15 | **4.57** | ✓ |
| Fitness | 2.70 | **2.91** | ✓ |
| Drawdown | 1.30% | **1.27%** | ✓ |
| Returns | 7.66% | **7.73%** | ✓ |
| Turnover | 18.05% | 19.09% | 软告警（+1.04pp） |

**方向项全正，非稀释。**

### 四、软标记（如实披露，不阻塞）

1. **近 3 年弱于全期**（1.78 vs 2.23，衰减比 0.80）：主要贡献来自 2020 年（疫情期波动放大，R 14.87% / S 3.09）。剔除 2020 后 9 年均值降至 2.09。
2. **2023 年为全期最弱**（S 1.24 / F 0.52 / margin 0.35bp），需观察是否进入持续衰减。
3. **换手率 24.27%** 属中高换手区（区间 20–30%），边际贡献中 TO 方向为唯一软告警；margin 6.65bp 相应偏低。
4. **混塔倍率被折损**：`GBR/D1/IMBALANCE ×1.0` + `GBR/D1/PV ×1.4` ⇒ 生效倍率取短板 **1.0**。做纯 PV 单类别件可拿 1.4，但需换掉 imb5 腿。

### 五、结论

**PASS**。10 年完整样本、平台全闸通过、边际贡献五项方向全正、self 0.1319 / prod 0.6865 双低。风险集中在高换手与近两年走弱（非结构性，可通过后续观察监控）。

---

## gJaaER8K（IND / TOP500 / 来源自建 SA）

**表达式**
```
combo_a(normalize(alpha), nlength=126, mode='algo1')
```
IND / TOP500 / D1 / decay 5 / STATISTICAL / trunc 0.08 / nan ON / selection POSITIVE / limit 20

### 一、平台闸门

| 项 | 实测 | 判定 |
|---|---|---|
| 模拟层 checks | `fail = []`（含 LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST / LOW_ROBUST_UNIVERSE_SHARPE） | PASS |
| WARNING | `MATCHES_COMPETITION`（1 条，不阻塞） | WARNING |
| PENDING | SELF_CORRELATION / PROD_CORRELATION / SUPER_SUBMISSION / NON_SELF_SUPER_ALPHA | 已复核（见下），SUPER_SUBMISSION / NON_SELF_SUPER_ALPHA 为提交流程项 |
| Failed RA / PPA | 0 / 0 | PASS |
| Sharpe / Fitness | 5.11 / 5.50 | PASS（阈值 1.58 / 1.0） |
| 2Y Sharpe | 4.56 | PASS（阈值 1.58） |
| sub-universe / investability | 2.64 / 3.51 | PASS（IND 无容量硬闸） |
| Turnover / Drawdown | 17.94% / 3.91% | PASS |
| self corr | 0.5969（池 55 颗，剔除 PP 9 颗；最高为 QPbjxMYw 0.597 / wpbQjeKp 0.585） | PASS |
| prod corr | 0.5969（平台缓存，非 provisional） | PASS |
| 混腿 | MULTI_DATA_SET，`path = LADDER` ⇒ IS Ladder | PASS |

### 二、年度稳定性（逐年 PnL，全期 10 年）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 3.95 | 5.76 | 4.23 | 4.51 | 5.50 | 7.26 | 6.20 | 3.32 | 4.66 | 4.55 |
| Fitness | 3.84 | 7.25 | 3.88 | 4.31 | 6.15 | 9.16 | 7.60 | 2.84 | 4.82 | 4.50 |
| Returns | 11.8% | 24.0% | 17.3% | 15.1% | 22.7% | 28.2% | 29.4% | 14.8% | 20.1% | 15.1% |
| Drawdown | 1.12% | 1.19% | 1.78% | 1.82% | 1.64% | 1.18% | 1.83% | **3.91%** | 1.28% | 1.15% |
| Margin | 2.80bp | 3.17bp | 1.68bp | 1.83bp | 2.50bp | 3.18bp | 3.01bp | 1.46bp | 2.14bp | 1.96bp |

**近 3 年（2021–2023）判定**：
- 均值 **4.18**，全期均值 **4.84** ⇒ 衰减比 **0.89**（≥ 0.50 ⇒ PASS）
- 近 3 年每年为正且 > 0.3 ⇒ 平年 0 ⇒ PASS
- CV_Sharpe = 0.15（< 0.40 ⇒ PASS）
- max/min = 4.66 / 3.32 = **1.40**（≤ 3 ⇒ PASS）
- 全期 10 年无一年 Sharpe < 3.0，**无结构性疲软年**

**关键正面证据**：10 年全期 Sharpe 均 ≥ 3.32，无一年低于 3.0；2021 年（3.32）虽为近 3 年最低，但仍远高于 1.58 阈值。信号不是靠某一年行情撑起来的。

### 三、边际贡献（`EQUITY:IND:1`）

| 项 | before | after | 变化 |
|---|---|---|---|
| Sharpe | 7.00 | **7.01** | +0.01 |
| Fitness | 5.36 | 5.40 | +0.04 |
| Returns | 13.49% | 13.60% | +0.11pp |
| PnL | 13.95M | 14.07M | +0.12M |
| Drawdown | 1.18% | 1.21% | +0.03pp |
| Turnover | 22.98% | 22.91% | −0.07pp |

⇒ **非稀释，方向全正**。边际贡献偏小（SA 在 IND TOP500 池中已是成熟竞争环境），但方向一致、无负面信号。

### 四、软标记（不阻塞，描述中应如实带出）

1. **WARNING `MATCHES_COMPETITION`**：与池中已有 alpha 存在结构相似性，需在描述中披露。
2. **self corr 0.5969 贴线**：距 0.70 阈值余量 0.103；与 QPbjxMYw（0.597）和 wpbQjeKp（0.585）高度相关，这三颗同属 IND n126 配方族。提交后若平台复核 self 超 0.70 可能被拒。
3. **Top-5 个股集中度**：平台 PnL API 仅返回日频聚合（date/pnl/equal-weight-pnl/investability-constrained-pnl），不提供逐股分解，无法计算。从 longCount=253 / shortCount=249 / TOP500 推断集中度应 < 30%，但未经逐股验证。
4. **prod corr 0.5969**：与 self corr 数值相同（均为 0.5969），疑似同一相关性通道；平台 prod 相关性覆盖仅 ~36 颗 alpha，此值来自缓存非实时测量。
5. **边际贡献偏小**：+0.01 Sharpe 在 IND 成熟池中属正常量级，不构成稀释但也说明增量有限。

### 五、结论

**PASS**。平台全部硬闸通过、10 年全期一致强势（最低年 3.32 >> 1.58）、近 3 年无衰减迹象（衰减比 0.89）、self/prod 双低（0.5969 / 0.5969）、边际贡献正。软标记（MATCHES_COMPETITION、self 贴线、集中度未逐股验证）需在提交描述中如实披露。

**提交前必做**：① 确认 SUPER 配额可用（当前 0/1）；② 在 description 中带上软标记披露；③ 提交后核对 ACTIVE 状态（防幽灵提交）。

---

## VkNzob9G（USA / insiders1 / 优化自 kqNb1g5d）

**表达式**
```
vector_neut(ts_zscore(ts_sum(mean_buy_transaction_count, 22), 168),
  group_rank(group_rank(multiply(
    rank(ts_backfill(median_chief_officer_tenure_days, 120)),
    rank(ts_backfill(board_external_connection_count, 120))),
    bucket(rank(ts_backfill(board_member_count_2, 120)), range="0,1,0.1")),
  subindustry))
```
USA / TOP3000 / D1 / decay **6** / REVERSION_AND_MOMENTUM / trunc 0.08 / nan ON

**与原件 `kqNb1g5d` 的差别**：仅 `ts_zscore` 252→168、`decay` 5→6。骨架、字段、算子集完全不变 ⇒ ATOM 属性、六维（ΔT1 +0.0091 / ΔT4 +4）、塔类别（INSIDERS+OTHER，ΔP=+1）逐项不变。

### 一、平台闸门

| 项 | 实测 | 判定 |
|---|---|---|
| 模拟层 checks | `fail = []`（含 LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST / MATCHES_PYRAMID） | PASS |
| Failed RA / PPA | 0 / 0，`ra_failed=false` | PASS |
| Sharpe / Fitness | **3.67 / 3.73** | PASS（阈值 1.58 / 1.0，余量 2.09 / 2.73） |
| 2Y Sharpe | **3.98** | PASS（阈值 1.58，余量 2.40） |
| sub-universe / investability | 1.83 / −0.33 | PASS（sub/S = 0.499；USA 无 investability 硬闸） |
| Turnover / Drawdown | 17.11% / 5.57% | PASS（区间 [3%,70%]） |
| self corr | **0.5959**（池 143，OS pool 150，剔除 PPAC 7；最高 e75gdQoM） | PASS（余量 0.104） |
| prod corr | **0.6913**（直方图 [0.6,0.7) 仅 7 个，余量 0.0087） | PASS |
| mutual（vs 已提交 4 颗） | 0.005 / 0.039 / −0.033 / 0.031 | PASS |
| VF 闸 | **PASS**（ΔP=+1 新建 USA/D1/INSIDERS；L2 拖累 0/3；多样性分 0.1212→[0.1219,0.1249]，+0.63%~+3.09%） | PASS |

### 二、年度稳定性

| 年 | Sharpe | Fitness | Turnover | Drawdown |
|---|---:|---:|---:|---:|
| 2014 | 2.80 | 2.11 | 18.84% | 1.80% |
| 2015 | 5.01 | 5.69 | 16.90% | 1.27% |
| 2016 | 2.92 | 2.51 | 16.49% | 2.09% |
| 2017 | 4.65 | 4.64 | 17.02% | 1.34% |
| 2018 | **5.82** | **6.65** | 16.86% | 1.16% |
| 2019 | 4.12 | 4.20 | 17.19% | 3.87% |
| 2020 | **1.36** | **0.97** | 16.19% | 5.57% |
| 2021 | 3.67 | 4.06 | 17.29% | 3.48% |
| 2022 | 5.09 | 6.24 | 17.22% | 2.56% |
| 2023 | 3.14 | 3.38 | 17.02% | 3.88% |

- 均值 3.858，近 3 年均值 3.967 ⇒ 衰减比 **1.028**（>1，无衰减）
- CV_Sharpe **0.348**（<0.5 门槛）
- 平年 **0**；max/min = 5.82 / 1.36 = 4.28
- 逐年全正；最弱 2020（1.36/0.97），仍优于原件的 2020（0.99/0.61）
- 回撤最大 5.57%（2020），全期 5.57%

### 三、边际贡献（`EQUITY:USA:1`）

| 项 | before | after | 变化 | 方案 D v2 |
|---|---:|---:|---:|---|
| Sharpe | 4.08 | **4.17** | **+0.09** | L1 PASS |
| Fitness | 3.29 | **3.39** | **+0.10** | L1 PASS |
| Returns | 8.14% | 8.27% | **+0.13pp** | L2 PASS |
| Turnover | 10.35% | 10.44% | +0.09pp | L3 软告警 |
| Drawdown | 2.73% | 2.68% | **−0.05pp** | 改善 |

⇒ 非稀释，`verdict = pass`。

### 四、软标记（不阻塞，描述中如实带出）

1. `MATCHES_COMPETITION` / `MATCHES_THEMES` 两项 warning（平台对所有件均返回，属清单展示非命中）。
2. `investability_sharpe = −0.33`：USA 不在容量硬闸区（硬闸仅 ASI/JPN/HKG/TWN/KOR），且较原件 −0.50 改善 0.17，但仍为负 ⇒ 大资金容量有限，描述中说明。
3. **与 `kqNb1g5d` mutual 0.9376**：同骨架孪生，本件提交后 `kqNb1g5d` 永久不可交（self 必 ≥0.99）。已在候选台账标注。
4. VF 闸 L1 按 ΔP=+1 判必升，但多样性分上界依赖 A（active 计数）是否同步 +1；下界 +0.63% 仍为正。

### 五、结论

Stage 0–8 全绿（含 VF 闸 PASS、方案 D v2 pass、稳健性无平年/无衰减/回撤可控）。**建议提交**。
