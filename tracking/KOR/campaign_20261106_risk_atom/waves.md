# waves · KOR × RISK × ATOM（2026-11-06 起）

> 设置档：KOR / TOP600 / Delay=1 / **decay 1** / **trunc 0.04** / unit VERIFY / nanHandling **ON** / pasteurization ON / maxTrade OFF
> 中性化：wave R1/R2 分两档（INDUSTRY 与 STATISTICAL）做对照；**每批内只动表达式，跨批才动设置**（保证可比）
> 模板：**P-ATOM-1**（KOR 已验证，shortinterest 实测 S 2.09）
> ```
> ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(F, {bf})), std={s}), {grp}), {p}), target_tvr=0.22)
> ```
> 并发纪律：`create_multi_simulation` 同时最多 **2 批在飞**（用户约束 5）
> prod 查法：`check_correlation(correlation_type="production", refresh=True)`；self 用本地 `check_self_correlation`

---

## Wave R1 · risk70 轴筛选（8 条，2 批 × 4）

**波次定位**：risk70 历史上 8 腿全打在 `srisk/srisku` IVOL 轴（上限 0.73）。
本波按 0.1 质量先验（头部 = `anlystsn` αC 2922）**换轴**，并用 P-ATOM-1 换模板 ⇒ 同时验证「头部轴」与「模板增益」两件事。

**候选（全部单数据集 ATOM，risk70）**

| 批 | 腿 | 核心 | 表达式骨架 |
|---|---|---|---|
| A | A1 | `anlystsn` **水平**（αC 2922，头部轴） | P-ATOM-1 / bf40 / std.24 / pow3.5 / sector |
| A | A2 | `anlystsn` **Δ66**（风格漂移 = 分析师修正代理） | 同上 + `ts_delta(F,66)` |
| A | A3 | `earnyild` 水平（αC 1795，第二轴） | 同上 |
| A | A4 | `btop` 水平（αC 794，价值轴） | 同上 |
| B | B1 | `hedge_fund_ownership_percentage` Δ66（对冲基金持股占比变化） | 同上 |
| B | B2 | `hedge_fund_number_owners` Δ66（持股家数变化） | 同上 |
| B | B3 | `sector_relative_momentum` 水平（行业内相对动量） | 同上 |
| B | B4 | `short_term_industry_country_factor` 水平 | 同上 |

**multisim**：A = `14h2s48nC4p1acUHHD1aBFt` · B = `3DYxK6g9l5aHbgdy62SXsbY`

### R1 实测（2026-11-06 收批，8/8 COMPLETE，0 error）

| 腿 | alpha | S | F | TO | 2Y | subU | RN | inv | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **A1 `anlystsn` 水平** | **`WjO36p5P`** | **1.11** | 0.67 | .1298 | **1.78** | 0.81 | **0.94** | 0.82 | LOW_SHARPE / LOW_FITNESS |
| A2 `anlystsn` Δ66 | `YP18Gpel` | 1.02 | 0.48 | .1975 | 0.79 | 0.92 | 0.85 | 0.47 | 4 项（含 2Y / inv） |
| A3 `earnyild` 水平 | `bl6J5Lwm` | 0.83 | 0.55 | .0705 | 0.71 | 0.51 | 0.72 | 0.56 | 3 项 |
| A4 `btop` 水平 | `LLMEAp0e` | 0.48 | 0.26 | .0610 | 0.22 | 0.49 | **0.01** | 0.45 | 3 项 |
| B1 `hedge_fund_ownership_pct` Δ66 | `0mYx0pmp` | −0.47 | −0.21 | .0829 | **−1.24** | −0.50 | −0.12 | −0.48 | 5 项 |
| B2 `hedge_fund_number_owners` Δ66 | `RRE9nmjn` | 0.24 | 0.08 | .0888 | 0.51 | 0.13 | 0.15 | 0.12 | 5 项 |
| B3 `sector_relative_momentum` | `88RVdp5a` | −0.27 | −0.12 | .0510 | −0.39 | −0.44 | −0.22 | −0.30 | 5 项 |
| B4 `short_term_industry_country_factor` | `MPYdoGMa` | −0.43 | −0.19 | .2138 | −0.06 | −0.35 | −1.44 | −0.25 | 4 项 |

### R1 读数

1. **⭐ `anlystsn` 水平 = 1.11 / 2Y 1.78**，是 KOR risk 塔**史上第一颗 S>1.0 且 2Y 过闸**的腿（前纪录 0.73 / 1.04）。
   失败闸只剩 **LOW_SHARPE（1.11 vs 1.58）** 与 **LOW_FITNESS（0.67 vs 1.0）**，其余 5 闸全 PASS
   （含 `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE` / `LOW_INVESTABILITY_CONSTRAINED_SHARPE`）。
2. **水平 > 变化率**（anlystsn 1.11 vs 0.68 的 Δ66 版 1.02 **但 2Y 崩到 0.79**）⇒ 该轴的信息在**存量水平**，
   不在漂移。这与 `risk70.md` 的 F-1 定律（「只有变化量有信号」）**相反**，是**载荷类字段与基本面字段的分野**：
   载荷本身就是「个股对因子的敏感度」这一结构量，其水平即有效信息。
3. **价值轴在 KOR/INDUSTRY 下几乎被完全中性化**：`btop` 的 **RN sharpe = 0.01**（raw 0.48 几乎全部由风险因子解释）
   ⇒ 铁律 E 的「RN ≪ raw ⇒ 因子暴露拖累」实证。`earnyild` RN 0.72（部分存活），`anlystsn` RN **0.94**（几乎全是纯 alpha）。
   ⇒ **`anlystsn` 是本集唯一「raw 与 RN 同步走强」的轴**，符合「信号真实但强度不足」档。
4. **8 个非载荷经济字段基本全灭**：`hedge_fund_*`（−0.47 / 0.24）· `sector_relative_momentum`（−0.27）·
   `short_term_industry_country_factor`（−0.43）。唯一可留意：B1 反向为 **+0.47 / +1.24**（对冲基金持股上升 ⇒ 后续跑输），
   量级不足且与 `institutions6` 判死同构 ⇒ **本波不追**。
5. **论坛交叉印证**（post `43621466539671`，30 赞）：「单字段直用基本没信号…加载类字段的价值在组合，不在单点」
   ——HKG 实测 `ts_min(ts_backfill(anlystsn,252),66)` 仅 S 0.41。本波用 P-ATOM-1 把同一字段抬到 **1.11**（+171%）
   ⇒ **模板才是本轮的增量来源**，与论坛结论不矛盾（论坛用的是裸 `ts_min`）。

### R1 归因（铁律 F，`get_alpha_yearly_stats` on `WjO36p5P`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 1.09 | **0.41** | 1.53 | 1.60 | **0.40** | 1.54 | **−0.22** | 1.46 | **3.46** | **0.66** |
| PnL | 41.0万 | 20.2万 | 53.6万 | 54.0万 | 18.3万 | 63.2万 | −10.4万 | 70.7万 | 143.5万 | 39.3万 |
| longCount | 245 | 254 | 251 | 265 | 271 | 278 | 267 | 268 | 273 | 270 |
| TO | .148 | .148 | .139 | .127 | .135 | .130 | .119 | .128 | .117 | .107 |

| 判据 | 读数 | 结论 |
|---|---|---|
| **十年覆盖（用户约束 6）** | longCount **245–278**，2014–2023 **无空年** | ✅ **PASS**（唯一满足约束 6 的 risk 候选） |
| **S<1.0 年份占比** | **4/10 = 40%**（2015/2018/2020/2023） | ⚠ 超 3 成线；**但 2Y 实测 1.78 已过 1.58 闸** ⇒ 决策表的「2Y 结构性不可达」前提**不成立**，不得据此停扫 |
| **单年占正收益** | 2022 = 143.5 / 503.4 = **28.5%**（< 30%） | ✅ 未触发过拟合指纹 |
| **曲线形态** | 9 正 1 负（2020 −10.4 万）；无尖峰暴涨、无 ≥3 段停滞 | ✅ 阶梯健康 |
| **RN vs raw** | raw 1.11 / RN 0.94（差 15%） | ✅ 因子暴露贡献小 ⇒ **信号自身衰减不是主因** |

**裁决（按发波决策表末行）**：「阶梯健康 + 停滞段少 + 单年 <30%」⇒ ⭐ **允许做强度杠杆扫描**（本轮唯一被授权的档位）。
**准入（禁碰）**：`srisk/srisku/resvol/dsrt` 四支（判死）；`hedge_fund_*` / `sector_relative_momentum` /
`short_term_industry_country_factor`（本波实测 <0.5）；`truncation` 扫描（平台锁定）；`universe` 扫描（唯一 TOP600）；
`decay` 单独扫（死轴，只在与中性化交叉时才有意义）。
**继承给 R2**：核心 = `anlystsn` 水平 + P-ATOM-1；唯一目标 = **S 1.11 → 1.58（+42%）**，F 随 S 机械跟随。
**收窄**：8 → 4（每批 4 条，只做单变量突变）。

---

## Wave R2 · `anlystsn` 强度推进 × 中性化档对照（4 突变 × 2 档）

**波次三问（铁律 G）**
1. **继承**：R1 的 `anlystsn` 水平壳冻结；IVOL 轴、经济字段轴、变化率轴全部列入禁碰。
2. **准入**：禁新增字段（除 `resvol` 作为 `vector_neut` 的正交化控制量，**不新增信号腿**）；
   禁 `add` 加权；禁 `truncation`/`universe` 扫描。
3. **收窄**：8 → **4**（比值 0.5 ≤ 1/3 不满足？本波是「8 腿筛选 → 4 腿定向突变」，其中 3 条只动 1 个参数、1 条只动正交化 ⇒ 搜索空间实际从「8 个未知轴」收成「1 个赢家的 4 个邻域」，**维度**收窄成立）。

**4 个单变量突变（相对 `WjO36p5P`）**

| 腿 | 突变 | 表达式差异 | 假设 |
|---|---|---|---|
| **C1** | 幂次 3.5 → **5.0** | `signed_power(...,5.0)` | 更极端的尾部集中 ⇒ 提高 S（P-ATOM-1 的 pow 在 4.0 后 S 开始掉，5.0 是越界检验） |
| **C2** | winsorize std 0.24 → **0.30** | `std=0.30` | 文档实证「std ↑ ⇒ S 与 prod 同向升」 |
| **C3** | 内层分组 sector → **industry** | `group_rank(...,industry)` | 行业内相对排序更纯；同时检验「外层 INDUSTRY 是否已把内层 sector 的差异吃掉」 |
| **C4** | `rank(F)` → **`vector_neut(rank(F), rank(resvol))`** | 正交化特异波动暴露 | 剥掉「高波动=高关注」的混杂，只留纯分析师情绪载荷 |

**两档中性化**（同 4 条表达式，唯一差异是设置）
- 批 C：`INDUSTRY`（R1 基线档）
- 批 D：`STATISTICAL`（区域默认档；用于验证「载荷类信号是否被统计因子剥离」）

**multisim**：C = `3J8rd0fdX4vccqQpswVbPMn`（INDUSTRY）· D = `4EGAoG8ub54W8I68QMuWm94`（STATISTICAL）

**预注册判读**
- 任一腿 S ≥ 1.58 且 2Y ≥ 1.58 ⇒ 直接进 S5（prod/self 实测）→ 提交判定；
- S 1.3–1.58 ⇒ 该突变记为正贡献，下一波只在该腿上再突变一处；
- 两档都 ≤1.2 ⇒ `anlystsn` 单轴上限 ≈1.2，转 R3「载荷组合」（论坛 5 组组合：反转期限结构 / 价值质量差分 / 对冲基金集中度 / 情感源背离）。

### R2-D 实测（STATISTICAL 档，`4EGAoG8ub54W8I68QMuWm94`，4/4 COMPLETE）

| 腿 | alpha | S | F | TO | 2Y | subU | inv | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| D1 pow 5.0 | `1YNOEv6K` | 0.79 | 0.34 | .1556 | 1.02 | 0.53 | 0.39 | 4 项 |
| D2 std 0.30 | `JjeoKl0E` | 0.76 | 0.32 | .1493 | 1.11 | 0.47 | 0.33 | 4 项 |
| D3 内层 industry | `2rA9dEqJ` | 0.66 | 0.24 | .1800 | 0.55 | 0.44 | 0.30 | 4 项 |
| D4 vector_neut(resvol) | `RRE9WXZe` | 0.88 | 0.44 | .1448 | **1.73** | 0.68 | 0.57 | 3 项 |

**读数**：STATISTICAL 全档 **0.66–0.88**，显著低于 INDUSTRY 档基线 **1.11**（R1 `WjO36p5P`）
⇒ 与 KOR 既有实证一致（`STATISTICAL` ret .0569 < `CROWDING` ret .0615）——
**统计因子中性化把「风格载荷」这一类信号本身剥掉了**（载荷正是统计因子的构成原料）。
⚠ 本批同时说明：**中性化档是本塔第一杠杆**，且方向 = **离开 STATISTICAL**。
唯一在 STATISTICAL 下存活的变体是 **D4 `vector_neut(resvol)`（0.88 / 2Y 1.73）**
⇒ 正交化掉特异波动后，信号对统计因子的暴露下降（这正是 `vector_neut` 的设计目的）。

### R2-C 实测（INDUSTRY 档，`3J8rd0fdX4vccqQpswVbPMn`，4/4 COMPLETE）

| 腿 | alpha | S | F | TO | 2Y | subU | RN | inv | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| C1 pow 5.0 | `LLMEJ9p6` | 1.13 | 0.69 | .1342 | 1.74 | 0.84 | 0.92 | 0.87 | 2 项 |
| **C2 std 0.30** | **`P0ox9ZpM`** | **1.14** | 0.70 | .1284 | 1.77 | 0.84 | 0.88 | 0.88 | 2 项 |
| C3 内层 industry | `YP18q5pJ` | 1.00 | 0.58 | .1290 | 1.68 | 0.76 | 0.86 | 0.75 | 2 项 |
| C4 vector_neut(resvol) | `j2Yom305` | 1.02 | 0.70 | **.1216** | 1.61 | 0.82 | 0.82 | 0.83 | 2 项 |
| （R1 基线） | `WjO36p5P` | 1.11 | 0.67 | .1298 | 1.78 | 0.81 | 0.94 | 0.82 | 2 项 |

**读数**：4 个单变量突变**全部在 1.00–1.14 的窄带内**（基线 1.11）
⇒ ⛔ **`anlystsn` 单轴在 INDUSTRY 档的天花板 ≈1.14**，参数级微调已榨干（pow / std / 内层轴 / 正交化四个轴加起来只值 ±0.03）。
`vector_neut` 在 INDUSTRY 下略降 S 但把 TO 压到 .1216（**F 0.70 与最优并列**）⇒ 其价值在换手/F 而非 S。
⇒ 触发预注册条款「两档 ≤1.2 ⇒ 转 R3」。

### R3-E 实测（CROWDING 档，`16ehFY3oe4kYcozALwoJKNB`，2/2 COMPLETE）★ 突破

| 腿 | alpha | S | F | TO | 2Y | subU | inv | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| E1 基线 | `xArVg2ww` | 1.06 | 0.62 | .1094 | 1.80 | 0.83 | 0.78 | LOW_SHARPE / LOW_FITNESS |
| **E2 `vector_neut(resvol)`** | **`1YNOElVX`** | **1.23** | **0.86** | .1098 | **2.13** | **1.09** | **1.05** | LOW_SHARPE / LOW_FITNESS |

**★ 本轮最佳件 = `1YNOElVX`（CROWDING + vector_neut）**
- S **1.23**（较 INDUSTRY 基线 +11%）· F **0.86**（+28%）· 2Y **2.13** · subU **1.09** · inv **1.05** · TO .1098
- **除 LOW_SHARPE（1.23 vs 1.58）与 LOW_FITNESS（0.86 vs 1.0）外，全部 5 项 RA 检查 PASS**，
  且 subU / inv 均 >1 有充足余量 ⇒ **缺口只剩强度，不是结构**
- 中性化档效应量：CROWDING **+0.17 S / +0.19 F**（vs INDUSTRY 的 vector_neut 版 1.02/0.70）
  ⇒ **「结构 × 中性化档」的交互真实存在**（同一 `vector_neut` 变体在 INDUSTRY 下降、在 CROWDING 下升）
- 机理：CROWDING 中性化剥离「拥挤交易」暴露（`anlystsn` 622 users = 极拥挤），
  再把 `resvol` 方向正交化 ⇒ 剩下的是「**未被拥挤交易定价的分析师情绪暴露**」


---

## Wave R3 · 中性化档外推（离开 STATISTICAL / INDUSTRY）

**依据**：R2-D 证明 STATISTICAL 是本塔最差档；论坛帖 `36064174250519`（20 赞）实证
「**SLOW 风格中性化下 RISK 数据集出货率很高**，ASI 池内相关性普遍 <0.6」；
KOR 既有实证「`CROWDING` returns 最高（.0615）但压 2Y；`FAST` 提 2Y」。
KOR 合法 11 档：NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST。

**设计**：同 2 条表达式（基线 `anlystsn` 核心 + `vector_neut(resvol)` 变体），逐档外推。
每档一个 multisim（设置不同 ⇒ 不可同批）。

| 批 | 中性化 | multisim | 备注 |
|---|---|---|---|
| E | **CROWDING** | `16ehFY3oe4kYcozALwoJKNB` | returns 最高档（KOR 实证） |
| F | **SLOW** | 待发 | 论坛实证 RISK 出货档 |
| G | **SLOW_AND_FAST** | 待发 | SLOW 的加密版 |
| H | **REVERSION_AND_MOMENTUM** | 待发 | KOR 峰度族最优档 |
| I | **FAST** | 待发 | 提 2Y 档 |

**预注册**：任一档 S ≥ 1.58 ⇒ 冻结该档进 S5；最优档确定后，用该档做**全载荷轴扫**（R4）与**组合腿**（R5）。

### R3 中性化档扫描汇总（同一核心表达式族）

| 档 | 基线 S | `vector_neut` 版 S | TO | 2Y | 判定 |
|---|---:|---:|---:|---:|---|
| STATISTICAL | 0.79（pow5） | 0.88 | .145 | 1.73 | ⛔ 最差（载荷被统计因子剥离） |
| SLOW | 0.97 | 1.04 | .210 | 1.54 | ⛔ 换手翻倍且更弱（论坛结论不迁移 KOR） |
| INDUSTRY | 1.11 | 1.02 | .122 | 1.61 | ✅ 基线 |
| **CROWDING** | 1.06 | **1.23** | .110 | **2.13** | ⭐ **最优** |

⇒ 冻结 **CROWDING**。⚠ 论坛帖 `36064174250519` 的「SLOW 下 RISK 出货率高」在 KOR **不成立**（0.97–1.04）
——又一个「跨区照搬结构配方失效」实证。

### R4 实测（CROWDING 强度突变，`1GkJPX8xF4WHa3MIdpDNSr7`，4/4）

| 腿 | alpha | S | F | TO | R | 2Y | subU | inv |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| R4-1 幂次 4.5 | `j2YoLPVE` | 1.22 | 0.84 | .1142 | .0598 | 2.15 | 1.07 | 1.03 |
| R4-2 双重正交（+size） | `RRE9Xl5d` | 1.06 | 0.68 | .1081 | .0514 | 1.58 | 0.91 | 0.86 |
| R4-3 `anlystsn − newssent` | `0mYxoNG6` | 1.09 | 0.61 | .1370 | .0428 | 1.91 | 0.76 | 0.75 |
| R4-4 R4-3 + 正交 | `omER2JRv` | 1.04 | 0.56 | .1391 | .0406 | 1.87 | 0.71 | 0.73 |

**读数**：幂次 3.5→4.5 **无增益**（1.23 vs 1.22）；双重正交与情感源价差**均劣于基线**
⇒ ⛔ 「`anlystsn` 单轴 + 单次 `vector_neut(resvol)` + pow 3.5」已是最优几何，**参数与组合两轴同时见顶**。

### R5 实测（CROWDING，其它载荷轴，`hNlyD7fG4qFazHOTFMb5Xt`，4/4）

| 腿 | alpha | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `earnyild` + vect | `78L3OvQ8` | 0.57 | 0.32 | .0666 | 1.28 |
| `growth` + vect | `O0AReMkq` | 0.69 | 0.36 | .0496 | 1.22 |
| `invsqlty` + vect | `WjO3kodP` | 0.17 | 0.05 | .0489 | 0.72 |
| `profit` + vect | `Xg9VqvLz` | 0.33 | 0.13 | .0539 | 1.45 |

**读数**：其余 26 支风格载荷在**同一最优档 + 同一几何**下全部 ≤0.69
⇒ **`anlystsn` 不是「载荷族的代表」，而是本集唯一有可交易残余的轴**（与 αC 2922 的头部地位一致，但不因拥挤而失效 ⇒ 说明 CROWDING 中性化正好把它洗干净）。

### R6 实测（CROWDING，decay 档扫描 + 未测轴）

| 批 | decay | 腿 | alpha | S | F | TO | 2Y | 备注 |
|---|---:|---|---|---:|---:|---:|---:|---|
| `1LKJ9FfX84R4bWWhfu1aCeM` | **0** | leader（anlystsn+vect） | `88RVgp5X` | **1.23** | 0.86 | .1098 | **2.13** | ⛔ S 差 0.35；2Y 全族最高 |
| 同上 | 0 | 基线 anlystsn | `MPYd9GOM` | 1.06 | 0.62 | .1094 | 1.80 | ⛔ 去掉 vector_neut 反而更弱 |
| 同上 | 0 | `ts_rank(anlystsn,252)` + vect | `j2YoN6vW` | 0.74 | 0.38 | .1388 | 1.40 | ⛔ 时序分位口径崩 |
| 同上 | 0 | `srtindcnt`(αC 1431) + vect | `vR1ZaN8v` | **-0.31** | -0.10 | .2282 | 0.87 | ⛔ 高占用轴负向，符号需反转才可用 |
| `17TNFg6nb4QybD01cKVRY1fd` | **2** | leader | — | — | — | — | — | ⚠ **空批**：child_count=0，平台未展开，已重派 |
| `2ZUIKQaho4kjbCVVvu6e1nB`（重派） | **2** | leader（anlystsn+vect） | `1YNO60qR` | 1.17 | 0.81 | .0912 | **2.06** | ⛔ 比 decay0 的 1.23 更低 |
| 同上 | 2 | 基线 anlystsn | `3qo1gJqg` | 0.98 | 0.55 | .0912 | 1.75 | ⛔ |
| 同上 | 2 | `season`(αC 703) + vect | `58ErNY8M` | 0.25 | 0.07 | .1896 | 1.20 | ⛔ 崩（TO 翻倍） |
| 同上 | 2 | `earnvar`(αC 607) + vect | `npvmwrpa` | 0.29 | 0.10 | .0572 | 0.52 | ⛔ 崩（2Y 也破） |

**R6 终判（decay 轴关闭）**：decay 0（1.23）→ decay 2（1.17）**单调下降**，与文档「decay↓ ⇒ S↑」方向一致但幅度不够破局；
两个未测头部轴 `season` / `earnvar` 在最优几何下直接崩到 0.25 / 0.29。
⇒ **rsk70 的 S 天花板 ≈ 1.2，单轴见顶**；leader（`anlystsn` + `vector_neut(resvol)`）是全族唯一有效残余，2Y 2.06–2.13 说明近两年强但全样本撑不到 1.58。

### ⚠ 工具坑（本轮踩到，影响所有轮询）
`batch_status` 对已完成的 multisim **会返回 `child_count=0 / terminal=0 / parent_status=null / all_terminal=false`** 的假空批状态，
看起来像「还在排队」，实际批早已跑完（首批 4 条实测 **约 2 分钟**完成，不是 40 分钟）。
**权威读数源 = `harvest_multisim_alphas({multisimulation_location})`**（假 location 已验证返回 404，说明它确实按 location 取数，不会回落）。
⇒ 以后轮询一律：`batch_status` 疑似排队时，直接 harvest 兜底，别干等。


**R6 decay=0 档结论**：`decay 0` 虽按文档应抬 S，实测最高仅 **1.23**（leader），且去掉 `vector_neut(resvol)` 掉到 1.06、
`ts_rank` 几何掉到 0.74、高占用轴 `srtindcnt` 直接负向（-0.31、TO 0.228 翻倍）。
⇒ decay 不是本族瓶颈，**几何与载荷轴才是**：`vector_neut(anlystsn, resvol)` 是本族唯一有效残余；
2Y 2.13 说明近两年确实有信号，但全样本 S 撑不到 1.58 ⇒ 除非 decay=2 档能同时抬 S 与 2Y，否则 rsk70 单轴见顶。

---

## Wave R10 · leader 邻域终扫（CROWDING，`3tuXdy8C4oabA7TGwGT1we`，4/4）

leader = `ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(ts_backfill(anlystsn,bf)), rank(ts_backfill(momentum,22))), std=0.24), sector), p), target_tvr=0.22)`

| 腿 | 突变 | alpha | S | F | TO | R | 2Y | subU | inv |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| bf 40→55 | `2rA9Rnmx` | 1.29 | 0.91 | .1228 | .0628 | 2.29 | 1.12 | 1.02 |
| bf 40→22 | `vR1Z9JOz` | 1.29 | 0.91 | .1228 | .0628 | 2.29 | 1.12 | 1.02 |
| 内层 sector→subindustry | `VkxZEYd0` | 1.11 | 0.68 | .1367 | .0513 | 1.91 | 0.71 | 0.89 |
| **pow 3.5→2.5** | **`58Er9qj5`** | **1.30** | **0.93** | .1187 | .0641 | **2.30** | 1.13 | 1.03 |

**读数**：
- **bf 22 / 40 / 55 三档逐位相同**（1.29/0.91/.1228）⇒ `anlystsn` 覆盖足够稠密，`ts_backfill` 窗口是 no-op（省一个扫描轴）。
- 分组轴：sector **1.30** > subindustry 1.11（与 risk59 的「轴越细越弱」一致，第 3 次复现）。
- **pow 2.5 → S 1.30 / F 0.93 / 2Y 2.30** 是本战役全期最佳读数（仅比 3.5 高 0.01，属同一水平带）。

## Wave R11 · 剩余载荷轴复测（momentum 正交，CROWDING，`3uZHDt2a4YNbbV1gaA7p5hv`，4/4）

| 腿 | alpha | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `newssent`(aC 93) | `kqNvXnxd` | 0.09 | 0.02 | .1535 | 0.65 |
| `divyild`(274) | `E56NbqZK` | 0.37 | 0.14 | .0711 | 0.18 |
| `midcap`(414) | `gJeXKmYg` | 0.26 | 0.11 | .0692 | 1.08 |
| `earnqlty`(255) | `Xg9VLkgm` | 0.37 | 0.14 | .0668 | 0.73 |

**读数**：全部 ≤0.37。至此 **risk70 的 27 支风格载荷中已测 21 支**（anlystsn / earnyild / btop / growth / invsqlty / profit / momentum / ltrevrsl / strevrsl / divyild / shortint / season / earnvar / earnqlty / indmom / midcap / size / beta / resvol / srtindcnt / newssent），
**只有 `anlystsn` 越过 1.0**。剩余未测 6 支（leverage / cnt_kor / cntadj / indadj / market / primaryindustry）属结构性共线或哑变量，按 ②.c 不作信号。

## Wave R12 · 中性化档补测（REVERSION_AND_MOMENTUM / FAST）

| 批 | 档 | multisim | 结果 |
|---|---|---|---|
| `2wT3K87TH4mF8D6j6oJVoPk` | REVERSION_AND_MOMENTUM | 待 | |
| `2VH0Od1D04lYcq818MO9RnlB` | FAST | 待 | |

---

## Wave R12 实测（中性化档补测）

| 批 | 档 | alpha | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| `2wT3K87TH4mF8D6j6oJVoPk` | **REVERSION_AND_MOMENTUM**（pow 2.5） | `zq3goOb1` | **1.49** | **1.08** | .1320 | 2.15 |
| 同上 | REVERSION_AND_MOMENTUM（pow 3.5） | `QPvOlEKQ` | 1.47 | 1.03 | .1361 | 2.14 |
| `2VH0Od1D04lYcq818MO9RnlB` | FAST（pow 2.5） | `E56NaQkm` | 1.07 | 0.54 | .1887 | 1.31 |
| 同上 | FAST（pow 3.5） | `bl6JPa9q` | — | — | — | — |

★ **REVERSION_AND_MOMENTUM = 1.49 / F 1.08**：**FITNESS 首次过闸**（1.08 > 1.0），距 S 闸仅差 0.09。
中性化档终排序（本族）：**REVERSION_AND_MOMENTUM 1.63 > CROWDING 1.30 > INDUSTRY 1.14 > FAST 1.07 > SLOW 1.04 > STATISTICAL 0.88**。

## Wave R13 · `winsorize std` 扫描（REVERSION_AND_MOMENTUM，momentum 正交，pow 2.5）

| std | alpha | S | F | TO | 2Y | subU | inv | RA 失败 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.24 | `58ErqxJN` | 1.49 | 1.08 | .1320 | 2.15 | 1.16 | 1.14 | 1 |
| 0.28 | `xArVmr1W` | 1.51 | 1.11 | .1319 | 2.29 | 1.19 | 1.17 | 1 |
| **0.32** | **`VkxZYxxw`** | **1.59** | **1.20** | .1319 | 2.21 | 1.29 | 1.23 | **0 ✅** |
| **0.34** | **`N1NLnxgX`** | **1.58** | **1.19** | .1318 | 2.15 | 1.29 | 1.23 | **0 ✅** |
| **0.36** | **`vR1ZeaWr`** | **1.61** | **1.22** | .1320 | 2.21 | 1.30 | 1.23 | **0 ✅** |
| **0.38** | **`omERn83n`** | **1.62** | **1.23** | .1319 | 2.27 | 1.31 | 1.25 | **0 ✅** |
| **0.40** | **`58Era7Zn`** | **1.58** | **1.18** | .1322 | 2.24 | 1.26 | 1.24 | **0 ✅** |
| **0.42** | **`ZYQgjP2Q`** | **1.58** | **1.19** | .1321 | 2.35 | 1.25 | 1.23 | **0 ✅** |
| 0.46 | `58ErLna1` | 1.50 | 1.10 | .1320 | 2.21 | 1.24 | 1.20 | 1 |

★ **`winsorize std` 是本族 S 主杠杆**：单峰，甜区 **0.32–0.42**（std 0.24→0.36 使 S +0.12、F +0.14）。

## Wave R14 · pow 扫描（REVERSION_AND_MOMENTUM，std 0.36~0.40）

| pow | std | alpha | S | F | 2Y | RA 失败 |
|---:|---:|---|---:|---:|---:|---:|
| **1.5** | 0.40 | **`d5WYd8RX`** | **1.61** | **1.25** | 2.26 | **0 ✅** |
| **2.0** | 0.40 | **`78L3xxY8`** | **1.60** | **1.22** | 2.25 | **0 ✅** |
| **2.0** | 0.36 | **`E56Nk0wL`** | **1.63** | **1.25** | 2.23 | **0 ✅** |
| 2.0 | 0.44 | `YP18Qw0W` | 1.56 | 1.18 | 2.25 | 1 |
| **3.0** | 0.36 | **`zq3gOwmd`** | **1.60** | **1.19** | 2.20 | **0 ✅** |
| 3.0 | 0.40 | `O0ARnnWq` | 1.55 | 1.14 | 2.23 | 1 |
| 4.0 | 0.40 | `gJeXmmag` | 1.50 | 1.06 | 2.20 | 1 |
| 3.5 | 0.40 | `LLMEnnK1` | 1.50 | 1.00 | 2.17 | 1 |

★ pow 甜区 **1.5–3.0**（与 CROWDING 档不同：那里 pow 3.5–5.0 才有 1.29）
⇒ **pow 甜区随中性化档漂移**，换档必须重扫幂次（本轮最重要的工程结论之一）。

## R13/R14 波次产物（10 颗 RA 全过参数变体，历史记录）

全族最佳 = `E56Nk0wL`（S 1.63 / F 1.25 / 2Y 2.23 / TO .1310 / subU 1.31 / inv 1.26）。
⚠ 这 10 颗是**同一 `anlystsn` 参数族**（族内互相关 >0.95，且 `E56Nk0wL` prod 0.7002 FAIL），
按用户澄清的「候选池」口径**不构成最终交付**（见 [`final_report.md`](final_report.md) 附录 B）。
**最终交付 = [`final_report.md`](final_report.md) 的 10 颗 ATOM 候选池**（self<0.7 / prod<0.7 / 两两互相关<0.7）。

### 相关性
- `E56Nk0wL` self **0.426 PASS**；`VkxZYxxw` self **0.417 PASS**
- `wpQ3wP8Y`（同核心、CROWDING 档）prod **0.62 PASS**（直方图 `[0.7,0.8)` n=0 ⇒ 非密墙）
- `VkxZYxxw` prod：查询时账号 prod 单并发槽被其它会话占用（holder=`kqNv1xRk`，非本轮 alpha），按 retry 重查
