# GBR `other169`（CDS Dataset）模板库与实战记录

> 区域固定：**GBR / TOP700 / delay 1**。本文件记录信用违约互换（CDS）数据集的字段画像、已测几何、**几何维度选择的教训**、KMV-Merton 模板族与残值判断。
> 关联文档：`template_library_gbr_fundamental_cap_scaled.md`（估值位移族主战场）、`template_library_gbr_other567_employee_reviews.md`（OTHER 塔另一地基）。

---

## 1. 数据集画像

| 项 | 值 |
|---|---|
| 数据集 id | `other169` |
| 名称 | CDS dataset（信用违约互换） |
| 字段数 | **22，全部 VECTOR** |
| 平台 users / alphas | 28 users / 44 alphas |
| valueScore | 6.0 |
| category | OTHER |
| 塔位 | **OTHER 单塔**（实测 `pyramids.list = [{GBR/D1/OTHER, 1.6}]`） |
| 时效性 | 日频（`oth169_dailycontributors` / `oth169_dailycontributedquotes` 为日度更新） |

### 1.1 ★ GBR 覆盖约 30%，这是本数据集的结构上限

`zq3XRdbo` 实读：`longCount = 102` + `shortCount = 105` = **207 只持仓**。

⇒ **只有约 207 / 700 家英国公司有 CDS 报价**（合理：CDS 市场只覆盖大公司/有债券发行的公司）。这个覆盖率的后果：
- 空头可能被迫在**无 CDS 数据的股票**上建仓（表达式返回 NaN 时平台的处理），或全组合只在 207 只里选 ⇒ 子宇宙统计天然不稳。
- 实测 `LOW_SUB_UNIVERSE_SHARPE` 的 **limit 只有 0.02**（由 `limit ≈ 0.434 × sharpe` 推出）⇒ 只要 S 起来，SUB 闸就跟着抬，**这与 GBR 无 universe 退路的限制叠加**。

---

## 2. 字段全清单（22 个，`get_datafields` 实读 `complete: true`）

### 2.1 信用风险核心

| 字段 | users / alphas | 语义 |
|---|---|---|
| `mid_par_spread_basis_points` | 4 / 7 | **CDS 中间价 par spread（bp）—— 信用风险主信号** |
| `bid_par_spread_basis_points` | — | 买价 par spread |
| `oth169_parspreadoffer` | — | 卖价 par spread |
| `bid_price_percent_of_notional` | — | 买价（面值百分比） |
| `oth169_percentofparoffer` | — | 卖价（面值百分比） |
| `oth169_recrisk` | 6 / 8 | 回收风险 |
| `oth169_recoveryrate` | — | 回收率 |
| `isda_assumed_recovery_percent` | 16 / 27 | ISDA 假定回收率（**使用最广的字段**） |
| `bid_upfront_payment_percent` | — | 买价预付比例 |
| `offer_upfront_payment_percent` | — | 卖价预付比例 |
| `oth169_coupon` | — | 票息 |

### 2.2 流动性 / 报价质量

| 字段 | users / alphas | 语义 |
|---|---|---|
| `mid_quote_spread_basis_points` | 3 / 7 | **中间价报价价差 —— 流动性维度** |
| `bid_quote_spread_basis_points` | — | 买价报价价差 |
| `oth169_quotespreadoffer` | — | 卖价报价价差 |
| `highest_mid_value_contributed` | — | 当日贡献的最高中间价 |
| `lowest_mid_value_contributed` | — | 当日贡献的最低中间价 |

### 2.3 覆盖广度 / 数据质量

| 字段 | users / alphas | 语义 |
|---|---|---|
| `oth169_dailycontributors` | — | 当日贡献报价的机构数（**覆盖广度**） |
| `oth169_dailycontributedquotes` | — | 当日贡献的报价条数 |
| `oth169_monthlyobservationscore` | — | 月度观测质量分（**1–4，分类量**） |

### 2.4 期限 / 宏观 / 元数据

| 字段 | users / alphas | 语义 |
|---|---|---|
| `oth169_tenor` | — | 期限（**`vec_avg` 会把不同 tenor 混在一起，是本数据集最大的处理陷阱**） |
| `interest_rate_curve_parallel_shift_impact` | 1 / 1 | 利率曲线平行移动冲击 |
| `instrument_currency_code` | — | 货币代码（**元数据，排除**） |

### 2.5 ★ 两个主信号字段在 GBR 实质等价

`mid_par_spread_basis_points`（信用风险）与 `mid_quote_spread_basis_points`（流动性）在经济含义上完全不同，但批 14 实测：

| alpha | 字段 | S | TO | 2Y | drawdown |
|---|---|---:|---:|---:|---:|
| `zq3XRdbo` | par spread | 0.05 | **2.96%** | 0.15 | 0.1075 |
| `xArXdvbN` | quote spread | 0.06 | **2.96%** | 0.15 | 0.1087 |

读数几乎逐位相同 ⇒ **在 GBR/TOP700 上这两个字段承载的是同一批公司的同一个横截面结构，不能当两条独立腿使用**。若要用流动性维度，必须显式做成**比率**（`par / quote`）而不是取另一个字段的水平。

---

## 3. 批 14：截面秩几何（错误几何）—— 双灭

multisim `ql79Tdpx4pK9pBgZ7fAbUt`，设置 `GBR/TOP700/D1 · INDUSTRY · decay10 · trunc0.05 · nanHandling OFF · maxTrade OFF`。

| alpha | 表达式 | S | F | TO | 2Y | SUB | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `zq3XRdbo` | `rank(ts_backfill(vec_avg(mid_par_spread_basis_points), 22))` | 0.05 | 0.01 | 2.96% | 0.15 | −0.24 | 4 |
| `xArXdvbN` | `rank(ts_backfill(vec_avg(mid_quote_spread_basis_points), 22))` | 0.06 | 0.01 | 2.96% | 0.15 | −0.23 | 4 |

其他实读：`checks.pass` 含 `CONCENTRATED_WEIGHT`（**无 CW 墙**）；`risk_neutralized_sharpe = +0.57`（远高于 S 0.05 ⇒ 风险中性化后仍有微弱结构，提示信号存在但被市场 beta 盖住）；`investability_sharpe = −0.02`。

**★ 自省（本轮最重要的方法论修正）**：批 14 的问题不是字段选错，而是**几何选错**。forum 铁律①（「自身基线异常度」是唯一存活形态）与 KMV-Merton 模板用的都是**时序**秩 / zscore，我却用了**横截面**秩 `rank(...)`。一个「自身相对历史才有意义」的时序变量在错误几何下读数为零，**不构成机制证伪**。

---

## 4. 批 15：时序几何（正确几何）—— 同一个字段，读数 ×11

multisim `3brIrUdEX5dZ9mP1so4afgx`，设置同批 14。

| alpha | 表达式 | S | F | TO | 2Y | SUB | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| `zq3XNwlX` | `-rank(ts_av_diff(ts_backfill(vec_avg(mid_par_spread_basis_points), 22), 252))` | 0.12 | 0.03 | 7.72% | 0.07 | −0.36 | 1.93bp |
| **`ZYQkEwO0`** | `-rank(ts_zscore(ts_backfill(vec_avg(mid_par_spread_basis_points), 22), 252))` | **0.66** | 0.34 | 10.18% | 0.67 | −0.32 | **6.70bp** |

### 4.1 三条可迁移结论

1. **`ts_zscore` ≫ `ts_av_diff` ≫ `rank`（0.66 / 0.12 / 0.05）** —— 与 forum `43152032301591` 铁律②「zscore（保留幅度）≫ rank」在**跨数据集、跨区域**上再次复现：同字段、同设置，仅换几何，读数差 **11 倍**。
2. **margin 同步放大 3.5×**（批 14 约 1.9bp → 批 15 的 6.70bp），说明这不是噪声被放大，而是**真实信号被正确度量**。GBR 区 margin 中位 11.9bp（forum `42587179348119`）⇒ 6.70bp 仍偏薄。
3. **SUB 从 −0.24 恶化到 −0.36** ⇒ 信号集中在非子宇宙（小票方向的暴露），而 GBR 只有 TOP700 一个 universe，**没有 forum 铁律⑤「换宇宙救 SUB」这条路**。

### 4.2 定论（不判死，留作备选）

- **不判死 CDS**：完整 KMV-Merton 模板（`winsorize(std=4)` + 信号自身分桶中性化轴 + `ts_weighted_decay`）尚未测；几何杠杆已被证明是**×11 量级**，说明该数据集确有时间维度与信息量。
- **但也不追加投入**：最佳读数 0.66 距 `LOW_SHARPE` 门槛 1.58 差 **2.4 倍**，而 SUB 为负、覆盖仅 30%。按「点塔均匀」准则，同等槽位投给已验证骨架（历史产出率约 50%）远优于继续在 CDS 上迭代。
- **残值**：`ZYQkEwO0`（S 0.66 / 2Y 0.67 / TO 10.18%）满足「2Y ≥ S」且换手极低，若将来需要**低换手正交腿**做组合层补强，可作为候选。

---

## 5. 十个结构互异模板（T1–T10，标注已测/待测与来源）

> 差异落在**骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性变换**上，不是换窗口。

| # | 模板 | 表达式骨架 | 机制 | 来源 | 状态 |
|---|---|---|---|---|---|
| **T1** | 横截面水平秩 | `rank(ts_backfill(vec_avg(<spread>), 22))` | 高利差 = 高风险 ⇒ 做空 | 自建基线 | ✅ 已测 0.05 |
| **T2** | 自身基线 zscore | `-rank(ts_zscore(ts_backfill(vec_avg(<spread>), 22), 252))` | 偏离一年基线 | forum `43152032301591` 铁律② | ✅ **已测 0.66（最佳）** |
| **T3** | 自身变化 av_diff | `-rank(ts_av_diff(ts_backfill(vec_avg(<spread>), 22), 252))` | 信用利差一年变化 | 自建（与成功骨架同算子） | ✅ 已测 0.12 |
| **T4** | 时序分位高斯化 | `-rank(ts_quantile(ts_av_diff(ts_backfill(vec_avg(<spread>), 22), 252), 22, driver=gaussian))` | 上述 + 高斯分位（在 fundamental17 上贡献过 ×10） | `template_library_gbr_fundamental_cap_scaled.md` §6.5 | ⏳ 待测 |
| **T5** | 信用-流动性分离（比率） | `-rank(ts_av_diff(divide(vec_avg(mid_par_spread_basis_points), vec_avg(mid_quote_spread_basis_points)), 252))` | 单位信用风险 vs 流动性溢价的相对扩张 | 自建（**同单位相除，规避单位闸**） | ⏳ 待测 |
| **T6** | 信息比率（信号/自身波动） | `-rank(divide(ts_mean(<spread>, 66), ts_std_dev(<spread>, 66)))` | 利差水平的稳定性 = 信用质量 | forum `37117908343831` TPL 系 | ⏳ 待测 |
| **T7** | 违约损失率（LGD）维度 | `rank(ts_av_diff(isda_assumed_recovery_percent, 252))` | 回收率变化 ⇒ 预期损失变化 | Merton 1974 / ISDA 口径 | ⏳ 待测 |
| **T8** | 覆盖广度（信息密度） | `rank(ts_av_diff(ts_backfill(vec_avg(oth169_dailycontributors), 22), 66))` | 报价机构数变化 = 市场关注度 | 自建（替代数据「关注度」族） | ⏳ 待测 |
| **T9** | 信号自身分桶中性化 | `-rank(group_neutralize(ts_weighted_decay(signal, k=0.5), bucket(rank(ts_delay(signal,1), rate=0), range="0.2,1,0.2")))` | 用**信号自身分位**做中性化轴（补 GBR「sector 轴无效」盲区） | ★ forum `29155767547543` KMV-Merton（28 赞 / 约 1 万次回测产出 6 个可提交 alpha）+ FF56620 TPL-009 | ⏳ **待测（最高优先级）** |
| **T10** | 标准化回填 + 时序秩 | `-rank(ts_rank(winsorize(ts_backfill(<spread>, 120), std=4), 60))` | 截尾去极值后再取时序秩 | forum `37117908343831` TPL-008 | ⏳ 待测 |

### 5.1 未验证的算子（本账号）

`bucket(...)` 与 `ts_weighted_decay(...)` **本会话尚未在 GBR 实测**。T9 落地前必须先跑一次 1 条的小批验证，避免「语法合法但回测 ERROR 并级联整批 CANCELLED」（本项目已在 `ts_max` / `ts_min` 上踩过这个坑）。

---

## 6. 处理规约（CDS 专属）

1. **全部 22 字段是 VECTOR**，必须先用 `vec_avg` / `vec_sum` / `vec_stddev` 折叠成标量。
2. **`vec_avg` 会混同一公司的多个 tenor**（1Y / 3Y / 5Y / 10Y）—— 这是本数据集最隐蔽的失真源。若信号要区分期限结构，必须用 `group_rank(<spread>, <tenor>)` 之类显式按 tenor 分组，或改用 `vec_max` / `vec_min` 取极端期限。
3. **`vec_avg` 在稀疏场景会被单一高值主导**（forum `41420742165527`）⇒ CDS 只有 207 家有数据、单日贡献报价机构可能极少（`oth169_dailycontributors` 低），此风险实测存在。
4. `oth169_monthlyobservationscore` 是 **1–4 分类量**，不可直接做算术；适合做**门控**（`greater(rank(...), 0.5)`）或分组轴。
5. `instrument_currency_code` 是元数据，排除。
6. 任何「带 bp 单位」字段与无量纲常数比较必挂单位闸 ⇒ 比值一律**同单位相除**，门控一律 `greater(rank(x), 0.5)`。

---

## 7. 对 GBR OTHER 塔的战略含义

OTHER 塔当前 **1 / 3**（需 2 个新增）。本数据集给不出（最佳 0.66），`other567`（Employee Review，月度面板）首探双灭（S 0.11 / −0.24）。

⇒ **OTHER 塔的下一个候选应当是 `event_ml_signals`（ML Company Event Signals，104 字段 / **12 users** / 108 alphas / **valueScore 7.0**）或 `other546` / `other128`**，而不是继续在 CDS 与员工评论上迭代。选 `event_ml_signals` 的理由：users 只有 12（极低拥挤）、valueScore 满分 7.0、alphas 108（说明真出过东西）。
