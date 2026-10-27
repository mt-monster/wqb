# USA / D1 · `fundamental93`（税务 / 递延税 / 应计）字段画像与首波设计

> 数据集：`fundamental93`｜类别 `fundamental`｜塔 `USA/D1/FUNDAMENTAL`（**未点亮**，本季提交 0）
> 平台字段数 **46**，本次拉回 **44**（`sharpe_filter_removed=2`，平台侧按 sharpe 预筛剔除，非覆盖缺失）。
> 数据结构：**全 MATRIX，无 VECTOR**（不存在 event 输入限制，可用全部矩阵算子）。
> 选入理由与拥挤度：数据集级 `alphaCount = 85`（`logs/_tmp_usa_ds_map.json` §H 表），
> 属 USA/D1 低拥挤前沿（fnd6 数千 / option 族 1.9 万–20 万）；机制 = **税务与应计**，
> 与已交付 5 颗（分析师预期修正）在**数据源与经济学上都正交**。
> 入队时点：2026-10-23（波 85）。判据与预注册见文末 §6。

---

## 1. 四族全景（44 字段，全部 MATRIX）

| 族 | 字段数 | 覆盖率区间 | 载体 | 经济含义 |
|---|---:|---|---|---|
| A. **应计（accruals）** | 7 | 0.338 – 0.927 | `fnd93_accruals_d1_*`、`fnd93_accrualsratio_d1_asset_change` | 权责发生制与现金制的差额；Sloan(1996) 应计异象的 LTM 形态 |
| B. **递延税费用（deferred tax expense）** | 12 | 0.583 – 0.916 | `fnd93_deferred_tax_expense_*`、`fnd93_expense_d1_*` | 会计利润与应税利润的时间性差异的费用端 |
| C. **递延税负债（deferred tax liability）** | 15 | 0.544 – 0.927 | `fnd93_deferred_tax_liability_*`、`fnd93_liability_d1_*` | 未来应税义务的存量端；资本开支/加速折旧的镜像 |
| D. **税务应计（tax accruals）** | 9 | 0.316 – 0.415 | `fnd93_tax_accruals_XX` | `(tax expense − cash tax paid) / 分母`：税负的“未付现”部分 |

> ⚠ **`_XX` 后缀不是新机制**：`_11/_12/_13/_21/…/_51` 的 XX 是**分母编号**（同一分子的不同
> 规模归一）。⇒ 字段数看着多，**独立构念只有 A/B/C/D 四个**，加 4 个形态算子
> （`current_t`=本期 z、`dts`=LTM 标准差、`max/min/mean`=LTM 窗统计、`length`=观测数）。
> 后续任何“穷尽字段”的波次都不得把 `_11` 与 `_21` 当作两个机制去数独立性。

## 2. 形态字段的语义（决定算子，不是噪声）

| 形态 | 含义 | 正确的算子用法 |
|---|---|---|
| `*_current_t` | 本期比率相对**自身 LTM 窗口**的 z 分 `(current − mean)/std` | 直接当“意外/偏离”用，**不要再套 `ts_zscore`**（会二次标准化，把截面差异压平） |
| `*_dts` | 该比率在 LTM 窗内的**标准差** | 盈余质量 / 税负稳定性；方向一律“高波动 ⇒ 折价” |
| `*_max` / `*_min` / `*_mean` | LTM 窗统计 | `max−min` 是窗内离散度；`mean` 是水平值 |
| `*_length` | LTM 窗内**可得观测数**（覆盖 0.92–0.93） | **数据质量门控**，不作信号本身；`length ≥ 6` ≈ 至少 6 个季度可比 |
| `*_asset_change` | 最新总资产 / 12 月前总资产 | Cooper-Gulen-Schill(2008) 资产增长异象；覆盖最高 0.89–0.90 |

## 3. 覆盖率分层与可用性（决定哪些臂能上 TOP3000）

| 分层 | 字段 | 覆盖率 | 结论 |
|---|---|---:|---|
| **高（≥0.70）** | `accruals_d1_length` 0.927、`liability_d1_length` 0.927、`expense_d1_length` 0.916、`expense_d1_asset_change` 0.895、`accrualsratio_d1_asset_change` 0.901、`deferred_tax_expense_11` 0.848、`expense_d1_max/min/mean` 0.784、`liability_d1_mean/max/min` 0.742、`expense_d1_21` 0.731、`expense_d1_22` 0.725、`liability_d1_length` 0.927、`liability_d1_dts` 0.716、`deferred_tax_liability_11/12` 0.715、`liability_d1_max/min` 0.742 | 0.716–0.927 | **首选**：TOP3000 上单票权重可控（≈700–2700 只），CW 风险低 |
| **中（0.55–0.70）** | `expense_d1_current_t` 0.583、`liability_d1_current_t` 0.545、`expense_d1_41` 0.612、`liability_21/22` 0.609–0.611、`liability_23` 0.569、`liability_41/51` 0.559–0.574、`deferred_tax_liability_13` 0.698 | 0.545–0.698 | 可测，需 `ts_backfill(…,252)` + 盯 CW |
| **低（<0.50）** | 全部 `tax_accruals_*` 0.316–0.415、`accruals_d1_dts` 0.436、`accruals_d1_mean/max/min` 0.457、`accruals_d1_current_t` 0.338、`accrualsratio_d1_asset_change` 0.901（例外） | 0.316–0.457 | **先验最弱**（单票权重可能 >10%）；`tax_accruals` 是理论上最纯的 Sloan 税版，但覆盖只 40% ⇒ 首波只给它 1 臂作探针，不连着发第 2 臂 |

> `ts_backfill(…, 252)` 是本集的**必需前置**：季频字段在两次财报之间是 NaN，不 backfill 会让
> 有效截面在报告季之间塌到 1/60。所有臂统一 252。

## 4. 更新频率与分布（实测 / 推断边界）

- **更新频率**：季频（字段描述明确写 `trailing twelve-month` / `e.g., Asset_2018Q3 / Asset_2017Q3`）。
  塔内同类（fnd6/fnd3）经验：**~63 个交易日一个信息台阶**，日间变化只在报告日。
- **分布**：本画像**未做 Labs 原始分布测量**（不在本次预算内），只按构造给先验——
  A/D 族是**比率**且分母可为小值 ⇒ 右尾长、有极端值；B/C 族是**分母归一后的比率** ⇒ 同一问题。
  ⇒ **首波壳统一用 `group_rank`（截面秩变换，天然有界、对尾部免疫）**，不裸用水平值进 `rank`
  之外的算子；`multiply(-1, ·)` 只管方向。
- **方向先验**（首波统一取“坏方向做空”）：应计高 ⇒ 未来收益低（Sloan）；应计/税负波动高 ⇒
  盈余质量折价；递延税费用意外为正（本期税率相对自身历史跳升）⇒ 税负恶化；资产增长高 ⇒
  未来收益低（Cooper）；税务应计高 ⇒ 未付现税负累积、盈利质量差。
  **递延税负债水平方向不做先验假设**（既是“未来应税义务”也是“资本密集/加速折旧”的代理），
  故 C 族水平值改用**自身 2 年 z 分**的偏离形态，避免把水平值当方向赌注。

## 5. 首波（波 85）十臂设计 —— 一臂一机制，单数据集 ATOM

设置冻结：`USA / TOP3000 / D1`、`decay 10`、`truncation 0.08`、`neutralization INDUSTRY`、
`nanHandling ON`、`pasteurization ON`、`unitHandling VERIFY`、`maxTrade OFF`、`FASTEXPR`。
multisim `10B8Bba0H5jy95RYWO6cVeQ`（10 臂），表达式文件 `tracking/USA/runs/usa_fnd93_w85.txt`。

| # | 机制 | 字段 | 覆盖率 | 表达式核 |
|---:|---|---|---:|---|
| 1 | 税务应计异常（Sloan 税版） | `tax_accruals_11` | 0.415 | `-rank(backfill(x,252))` |
| 2 | 应计水平（LTM 均值） | `accruals_d1_mean` | 0.457 | 同上 |
| 3 | 应计波动（盈余质量） | `accruals_d1_dts` | 0.436 | 同上 |
| 4 | 应计**意外**（本期 vs 自身 LTM） | `accruals_d1_current_t` | 0.338 | 同上（**不再套 zscore**） |
| 5 | 递延税费用**意外** | `expense_d1_current_t` | 0.583 | 同上 |
| 6 | 递延税费用波动 | `expense_d1_dts` | 0.688 | 同上 |
| 7 | 递延税负债**偏离**（自身 2 年 z） | `liability_d1_mean` | 0.742 | `-rank(ts_zscore(backfill(x,252),504))` |
| 8 | 递延税负债波动 | `liability_d1_dts` | 0.716 | `-rank(backfill(x,252))` |
| 9 | 资产增长异象（Cooper） | `expense_d1_asset_change` | 0.895 | `-rank(backfill(x,252))` |
| 10 | 递延税费用**窗内离散度** | `expense_d1_max − min` | 0.784 | `-rank(backfill(subtract(max,min),252))` |

全部壳 = `group_rank(multiply(-1, …), subindustry)`（#7 的 `-1` 在 z 分外）。
**合规自检**：无 `add A,B` 混信号（#10 的 `subtract(max,min)` 是同族窗内离散度，非两个信号腿相加）；
无 `ts_max/ts_min`（不可访问算子）；无命名参数误用。

## 6. 预注册判据（先写后测，事后不调）

1. **任一臂** S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58 且 `SUB ≥ 0.43×S` 且 TO ∈ [0.01, 0.70]
   ⇒ 进 prod 队列（`check_correlation(refresh=True)`），prod ≥ 0.70 按 D0-P 处置。
2. **十臂最高 S < 1.2** ⇒ 判 `USA-FND93-TAX-WEAK`，**不发第 2 批**（与
   `creator_signal_perf`/`finnews_nlp_scores` 同处置：低拥挤 ≠ 有信号）。
3. **max S ∈ [1.2, 1.58)** ⇒ 先归因（是方向、覆盖、还是形态错配），只按归因结论发第 2 批，
   且**只动被点名的那一维**（不整批换壳扫参）。
4. **覆盖 <0.50 的臂即使 S 最高也不单独晋级**：先看 CW 与 `*_length` 门控版能否在同壳下过 CW；
   过不了就按“低覆盖不可交付”封存，不拿它当数据集判据。
5. 若 #9（资产增长，覆盖 0.895）显著强于其余九臂 ⇒ 说明本集的主要载荷是**资产增长**而非税，
   **必须在 prod 前先跟自己 book 的 `fnd6_mrcta` 类腿比一次 self**（§B 已证 `WjLekJQO` self 0.7718
   就是被 fnd6 规模/资本开支代理吸收的），corr ≥ 0.7 直接放弃该臂，不换壳重试。

## 7. 与既有结论的关系（不重复踩）

- `fundamental` 塔本季 0 提交 ⇒ **未点亮，可测**（`analyst` 6 / `model` 4 才停测）。
- 与已交付 5 颗（analyst_factor_signals / analyst44 / analyst_consensus）**零共享字段、零共享构念**；
  但 §B 的教训是“数据源正交 ≠ PnL 正交”，故第 5 条判据要求#9 先测 fnd6 相关。
- 文本/新闻面（aC 29–49）三个数据集已实测判死（wave 56 / 62 + creator），**本波不走文本**：
  重复第四次测同类文本机制属盲扫。

## 8. 波 85 实测结果与封存（2026-10-23）

十臂全终态（multisim `10B8Bba0H5jy95RYWO6cVeQ`），完整表、逐族归因与工程事实见
交付日志 [附录 AP §E](_usa-atom-delivery-log-20261020.md)。

| 族 | 臂数 | S 区间 | 结论 |
|---|---:|---|---|
| A 应计（LTM 均值/波动/本期意外/税务应计 11） | 4 | 0.57–0.64 | 一致偏弱，方向对但幅度只有线的一半 |
| B 递延税费用（本期意外/波动/离散度） | 3 | 0.44–0.93 | 本集最有信息的一族（意外臂 0.93 / 2Y 1.24），F 与 SUB 不够 |
| C 递延税负债（偏离/波动） | 2 | 0.63–0.66 | 与 A 同量级 |
| D 资产增长（非税族） | 1 | **1.11** | 十臂最高，仍四闸全挂；与 fnd6 规模腿同源 |

**裁决：`USA-FND93-TAX-WEAK`**（预注册判据 2：`max S = 1.11 < 1.2`）。不发第 2 批。

**为什么封存而不是继续修**：距 SHARPE 线差 0.47、FITNESS 线差 0.45、2Y 线差 0.45，
且唯一最强臂是不属税族的资产增长。修壳/换中性化/加 decay 都只能动 ±0.1 量级，不改变结论。

**新增的选集先验（写进后续 S0）**：**数据集 aC 低 ≠ 构造不拥挤**。应计是跨数据集共享的
论文级构造，在主 fundamentals 集（aC ≥ 10⁴）里可直接表达 ⇒ 小众同义集里也不会有残余 alpha。
选集第二步要问「这个构造在饱和集里能不能直接算」，能算就直接排除。
