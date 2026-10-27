# analyst_consensus · Forecast+Actual overlay 族（`mean_forecast_actual_combined_*`）字段画像 — USA / TOP3000 / D1

> as_of 2026-10-21。数据源：`get_datafields(dataset_id="analyst_consensus", region="USA", delay=1, universe="TOP3000")`
> （MATRIX 面 = 30 条 `complete=true`；`search="mean_forecast_actual"` 命中 63 条，`platform_count=3238`）。
> 用途：S1 字段理解 + 批次设计依据。回测结果自 §5 起追加。

## §1 数据集画像与一次重要的口径更正

| 维度 | 实测值 | 判读 |
|---|---|---|
| 所属塔 | analyst（USA/D1 multiplier **1.2**） | 已点亮塔，但本族字段几乎全部 `alphaCount = 0` |
| **平台字段总数** | **3238** | ⚠ 旧清单 `_usa-analyst-consensus-field-inventory-20261020.md` 的「300 VECTOR」是**工具截断**，不是平台事实 —— 与 analyst_factor_signals 的 922 同源（`max_fields=300`）。该清单只覆盖了前 10%，**本文件不继承它的完备性声明** |
| MATRIX 子集 | 30 条（targetprice 20 + longterm 10），`complete=true` | 目标价子族已判死（prod 0.90–0.999） |
| VECTOR 主体 | 3200+ 条 | 必须 `vec_*` 聚合后才能进标量算子 |
| 更新频率 | 日更（D1） | 基础序列按财报/修正事件跳变，日频承载「最新值」 |

**为什么重开这个数据集**：交付的 5 颗 ACTIVE 里，prod 余量最大的不是三颗 analyst_factor_signals，而是本数据集单点交付的
`e76xgXkM`（prod **0.5532**，self 0.4553，S1.89/F1.12/2Y1.76/SUB1.05）。它用的字段
`mean_forecast_actual_combined_fxadj_eps_annual12` 属于一条**从未被系统挖过**的族：
『预测 + 实际』叠加序列（Forecast+Actual overlay，下文 FA 族）。

## §2 命名解剖

```
mean_forecast_actual_combined_[fxadj_]{metric}_{horizon}[_N]
```

| 片段 | 取值 | 含义 |
|---|---|---|
| `mean_forecast_actual_combined` | 固定前缀 | 均值口径的「预测+实际」复合序列 |
| `fxadj` | 有 / 无 | 汇率（+拆股/regime）调整版；无后缀为原始口径 |
| `metric` | revenue / netprofit / ebit / ebitda / ebt / pretax / pretax_reported / netprofitreported / reportednet / eps / eps_reported / epsreported / gps / roe / roa / bvps / nav / cfo / fcf / capex / total_assets / currentassets / currentliabilities / taxprovision / goodwill / inventory / depreciation / dps / dividend / netdebt / enterprisevalue / operatingexpense / cogs / tangbookvalue | 报表科目线 |
| `horizon` | `annual12` / `quarterly16` | 年度 / 季度口径 |
| `_2` / `_3` | 重复列名消歧后缀 | 语义相同，**不是版本号** |

**经济含义（本族的核心）**：这是一条**连续的单序列**——财报未出时填一致预期，财报出后替换为实际值。
因此 `Δ` 同时承载两件事：① 分析师修正；② 实际值落地偏离预期。对同一条财报线，
它比「纯预期序列」多一段实际兑现的信息，比「纯实际序列」早一个季度。

## §3 可用性判读（覆盖率 ≥ 0.79 且 alphaCount ≤ 3）

| 科目线 | 字段 | cov | uc | ac | 机制读法 |
|---|---|---:|---:|---:|---|
| 营收 | `mean_forecast_actual_combined_fxadj_revenue_annual12` | **0.9751** | 0 | 0 | 顶线兑现 |
| 报告 EPS | `mean_forecast_actual_combined_fxadj_gps2` | **0.9659** | 0 | 0 | 摊薄后每股兑现 |
| EBIT（_2） | `mean_forecast_actual_combined_ebit_annual12_2` | **0.9632** | 0 | 0 | 经营利润兑现 |
| 报告净利 | `mean_forecast_actual_combined_fxadj_reportednet_annual12_2` | 0.9589 | 0 | 0 | 底线（reported 口径） |
| 净利润 | `mean_forecast_actual_combined_netprofit_annual12` | 0.9498 | 0 | 0 | 底线（调整口径） |
| 税前（reported） | `mean_forecast_actual_combined_fxadj_pretax_reported_annual12` | 0.9432 | 0 | 0 | 税前兑现 |
| 净利润（reported） | `mean_forecast_actual_combined_fxadj_netprofitreported_annual12` | 0.9369 | 0 | 0 | 与 reportednet 近似同源 |
| 税项 | `mean_forecast_actual_combined_fxadj_taxprovision_annual12_tribes` | 0.9279 | 0 | 0 | 税率/税务筹划 |
| NAV | `mean_forecast_actual_combined_fxadj_nav_annual12` | 0.9184 | 0 | 0 | 账面资产 |
| 总资产 | `mean_forecast_actual_combined_total_assets_annual12` | 0.8937 | 2 | 3 | 资产扩张（投资异象轴） |
| EBIT | `mean_forecast_actual_combined_ebit_annual12` | 0.9396 | 0 | 0 | 与 `_2` 同源 |
| EBITDA | `mean_forecast_actual_combined_ebitda_quarterly16` | 0.7905 | 0 | 0 | 季度经营 |
| ROE | `mean_forecast_actual_combined_roe_annual12_tribes` | 0.8592 | 2 | 2 | 无量纲质量 |
| CAPEX（_2） | `mean_forecast_actual_combined_fxadj_capex_annual12_2` | 0.8334 | 0 | 0 | 资本开支扩张 |
| CFO | `mean_forecast_actual_combined_cfo_annual12` | 0.7956 | 2 | 2 | 现金转化（应计轴） |
| FCF | `mean_forecast_actual_combined_fcf_annual12` | 0.7902 | 1 | 1 | 自由现金流 |

**拥挤度结论**：本族是当前 USA analyst 塔里**唯一 alphaCount 归零的高覆盖族**。对照同塔已被打穿的
`analyst_factor_signals` revision/skew/surprise 族（prod 直方图 [0.7,0.8) n = 7–880），本族的 ac=0
意味着「平台同族覆盖为零」——不是指标白空间，而是 **prod 白空间**，这才是当前真正的瓶颈资源。

## §4 与已交付 5 颗的正交性

| 已交付 | 机制 | 与本族的差异 |
|---|---|---|
| `omoK1A5m` | EPS q1 环比增速的 252 日均值变化 | 水平增速 vs 预期-实际叠加修正 |
| `akVnvzX5` | EPS y1 预期偏度（时序三阶矩） | 分布形状 vs 序列修正 |
| `gJWoaJqv` | EPS/营收背离度加速度 | 双腿价差 vs 单科目兑现 |
| `kqJLawqP` | 同背离度秩变换 CROWDING | 同上 |
| `e76xgXkM` | **FA 族 EPS 年线** | **同族同壳的母体**；本批其余科目线需与它比 self-corr |

⇒ 新增候选的 self 风险来自 `e76xgXkM`（同机制不同科目），其余 4 颗机制不同、风险低。
交付纪律：任何候选提交前必须实测 `check_self_correlation` 与 `check_correlation(refresh=True)`，两者均 < 0.7。

## §5 批次 1 设计（2026-10-21，multisim `4tHpoM9K74SG9uQnA1Am4D4`）

**设计原则**：冻结 `e76xgXkM` 的全套壳与设置（它是本族唯一已验证的配方），**只换经济科目线**。
理由：⑭.21/⑭.22 已实证「prod 相关性由信号内容决定，与持仓分组/壳微调无关」——想拿到 5 颗正交 alpha，
必须换内容（科目线），而不是磨算子。算子穷举留到本批出结果后，对过闸科目线单独做（§6）。

**固定壳**（与 `e76xgXkM` 逐字符一致）：

```text
quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(<FIELD>), 63), 252), std=4), 252), hump=0.01), industry))
```

设置：USA / TOP3000 / D1 / decay **20** / neutralization **REVERSION_AND_MOMENTUM** / truncation **0.08** /
pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF / FASTEXPR。

**机制假设（10 条，10 个不同经济读法，非 8 模板套用）**：

| # | 科目线 | 经济机制（收益从哪来） | 先验方向 |
|---:|---|---|---|
| 1 | 营收 revenue | 顶线兑现超预期 → 需求冲击未被价格完全吸收 | 正向 |
| 2 | 净利润 netprofit | 底线兑现（调整口径）→ 盈利质量重估 | 正向 |
| 3 | EBIT | 经营端兑现，剥离税/财务噪音 | 正向 |
| 4 | CFO | 现金转化领先利润确认（应计异象的镜像） | 正向 |
| 5 | 总资产 total_assets | 资产扩张过快 → 投资过度折价（Cooper-Gulen-Schill 资产增长异象） | **反向**（预期负） |
| 6 | CAPEX | 资本开支扩张 → 过度投资折价（Titman-Wei-Xie） | **反向**（预期负） |
| 7 | ROE | 无量纲盈利质量兑现，跨规模可比 | 正向 |
| 8 | 报告 EPS gps2 | 摊薄/一次性项后的每股兑现 | 正向 |
| 9 | NAV | 账面价值兑现 → 价值轴 | 正向 |
| 10 | 税前（reported） | 税前兑现，剔除税务噪音的底线 | 正向 |

> 5 / 6 两条是**方向性对照**：若「资产/资本开支扩张折价」成立，这两条的 S 应显著为正（壳内 `ts_av_diff` 取正
> 即做多扩张，若市场惩罚扩张则 S 为负）。它们同时充当「壳是否只对『向上修正』有效」的判别器。

**预注册判据（不满足即按 D0-P 诊断，不盲扫）**：

1. 任一候选 S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / SUB ≥ 0.81（SUB/S 线 0.51）→ 进 prod 实测；
2. 任一候选 S ≥ 1.25 但差 1–2 闸 → **先归因**（缺口在 2Y / SUB / F 哪一项），只对该科目线做一次定向杠杆，不整批重发；
3. 全批 S < 1.0 → 判本壳不跨科目（`ts_av_diff` 只对 EPS 年线有效），转 §6 的算子轴（`ts_delta` / `ts_rank` / 长短窗比），
   而不是换数据集；
4. 5 / 6 若出现「正向强、反向弱」或反之，按方向性证据记入机制库，不因符号不符判死。

## §6 批次 1 读数与归因（multisim `4tHpoM9K74SG9uQnA1Am4D4`，10 条全 COMPLETE）

读数于 2026-10-21 用 `get_alpha_details` 逐条直取（`batch_get_alpha_metrics` 对当批返回全 null，不可用）。
`e76xgXkM` 行作参照（同壳、`fxadj_eps_annual12`、已提交 ACTIVE、prod 0.5532）。

| # | 科目线 | alpha | S | F | TO | 2Y | SUB（闸值） | SUB/S | 失败项 |
|---:|---|---|---:|---:|---:|---:|---|---:|---|
| 0 | `fxadj_eps_annual12`（参照，已交付） | `e76xgXkM` | **1.89** | **1.12** | 3.29% | **1.76** | 1.05（0.81） | 0.56 | **全过** |
| 1 | `fxadj_revenue_annual12` | `akVElGGx` | 0.99 | 0.45 | 5.19% | **−0.10** | 0.41（0.43） | 0.41 | S/F/SUB/2Y |
| 2 | `netprofit_annual12` | `mLYYpKaW` | **1.82** | **1.05** | 3.40% | 1.20 | 0.51（0.79） | **0.28** | SUB/2Y |
| 3 | `ebit_annual12_2` | `2rjjMGG6` | 1.16 | 0.56 | 4.83% | 1.21 | 0.76 过 | 0.66 | S/F/2Y（全 WARNING） |
| 4 | `cfo_annual12` | `9qEEYG89` | 0.90 | 0.48 | 3.96% | 0.86 | 0.48 过 | 0.53 | S/F/2Y |
| 5 | `total_assets_annual12` | `N1ee0KL8` | 1.47 | 0.78 | 3.45% | **0.84** | 0.71 过 | 0.48 | S/F/2Y（全 WARNING） |
| 6 | `fxadj_capex_annual12_2` | `MP00Ogez` | 0.64 | 0.29 | 4.94% | 0.99 | 0.38 过 | 0.59 | S/F/2Y |
| 7 | `roe_annual12_tribes` | `zqrRjeLd` | 1.45 | 0.91 | 4.13% | 1.35 | 0.80 过 | 0.55 | S/F/2Y（全 WARNING） |
| 8 | `fxadj_gps2` | `vROO8YGa` | 1.06 | 0.50 | 5.07% | **1.88** | 0.55 过 | 0.52 | S/F |
| 9 | `fxadj_nav_annual12` | `9qEEYGMx` | 0.97 | 0.44 | 5.10% | 1.48 | **0.13**（0.42） | 0.13 | S/F/SUB/2Y |
| 10 | `fxadj_pretax_reported_annual12` | `GrggPQx0` | 0.66 | 0.25 | 5.00% | 0.45 | **0.02**（0.29） | 0.03 | S/F/SUB/2Y |

### 6.1 归因一：本壳**不跨科目**，但「跨」与「不跨」有清晰的经济分界

按 S 排成三档，分界不是随机的：

- **工作区（S 1.45–1.89）**：`eps`（参照 1.89）· `netprofit` 1.82 · `total_assets` 1.47 · `roe` 1.45
  —— 全部是**每股口径 / 底线口径 / 回报率口径**。这类科目的「一致预期 − 实际」序列在年度滚动时
  **有真实的重新定价事件**（EPS 摊薄口径切换、净利润含一次性项、ROE 分母变化）。
- **半衰区（S 1.06–1.16）**：`ebit` 1.16 · `gps2` 1.06 —— 经营性/报告口径，信息存在但被更上游的
  EPS 吸收（`gps2` 的 2Y 1.88 反而最高，说明它近年才起效，是全期被早年拖累）。
- **死区（S ≤ 0.99）**：`revenue` 0.99 · `nav` 0.97 · `cfo` 0.90 · `pretax` 0.66 · `capex` 0.64
  —— **顶线（营收）与慢流量/存量科目（现金流、账面值、资本开支、税前）**。经济读法：这些科目的
  年度预期在财年初就基本被公司自身指引「锁定」，其 Δ 主要是**年度滚动进位**（去年实际变今年基数），
  不是新信息；且顶线超预期的定价在季度内已被消化，年度口径看不到残留。

> **判别力证据**：同一壳、同一设置、同一批次，仅换字段，S 从 1.89 连续落到 0.64。
> 因此壳本身有效（不是壳坏了），**内容维度是唯一自变量**——与 ⑭.22「prod 由信号内容决定」同构，
> 这里进一步说明 **S 也由内容决定，且分界可先验预测**（见下条）。

### 6.2 归因二：`SUB` 不是独立的一条线，而是 **0.43 × S** 的缩放线（**无绝对下限**）

本族 21 行 + 参照行暴露了平台口径（闸值列可反推），**十一个独立点逐点吻合**：

| S | SUB 闸值 | 闸值 / S |
|---:|---:|---:|
| 1.89 | 0.81 | 0.429 |
| 1.82 | 0.79 | 0.434 |
| 1.80 | 0.78 | 0.433 |
| 1.76 | 0.76 | 0.432 |
| 1.57 | 0.68 | 0.433 |
| 1.47 | 0.63 | 0.429 |
| 1.11 | 0.48 | 0.432 |
| 0.99 | 0.43 | 0.434 |
| 0.93 | **0.40** | 0.430 |
| 0.88 | 0.38 | 0.432 |
| 0.66 | 0.29 | 0.436 |

> ⚠ **口径更正（2026-10-21，批次 3 实测）**：本文早期版本写「S < 1.0 时退化为绝对 0.43 地板」——**已被证伪**。
> `O0JJPkb1` 的 S 0.93 对应闸值 **0.40**，不是 0.43；0.99→0.43 当初看着像"触地板"，
> 其实只是 0.43 × 0.99 = 0.426 的进位。**闸值 = 0.43 × S，全程线性，没有下限。**

**可复用结论**：`LOW_SUB_UNIVERSE_SHARPE` 实际考的是 **SUB/S ≥ 0.43**。
它不是「全市场赚钱但小盘不赚」的独立判据，而是**要求子宇宙与大宇宙同步**。因此
「S 很高但 SUB 挂」= 收益集中在小盘，**不能靠抬 S 解决**（抬 S 会同时抬闸值）——必须改**持仓广度**。
本批 `netprofit`（SUB/S 0.28）就是这一形态：S 1.82 漂亮，但边缘全在小盘。

### 6.3 归因三：2Y 是「报告/每股口径」与「顶线口径」的第二道分辨器

`gps2` 2Y **1.88** > 全期 1.06（早年失效、近年强）；`roe` 1.35、`nav` 1.48 也高于自身 S 档位；
而 `revenue` 2Y **−0.10**、`pretax` 0.45 —— 顶线/税前在近两年完全失效。这与 6.1 的经济读法互证：
**近年市场对「顶线超预期」的定价效率提高，对「每股/回报率口径的重新定价」仍有残余**。

### 6.4 方向性对照的证伪（批次 1 预留的判别器，已作答）

§5 第 5 / 6 行把 `total_assets` 与 `capex` 设为「资产扩张折价」的**反向**预期（壳内 `ts_av_diff` 取正
即做多扩张，若市场惩罚扩张则 S 应为负）。实测 **两条全为正**（1.47 / 0.64）。
⇒ **证伪**：本壳抓的不是「资产增长异象」，而是**预期修正方向**——资产预期被上调本身是信息，
不因「扩张=坏事」而反号。**记入机制库：不要在 forecast-revision 壳上叠加「增长异象」的反向先验。**

### 6.5 按预注册判据的处置

预注册判据 1（全闸）**0 命中**；判据 3（全批 S<1.0）不成立（best 1.82）。落在判据 2 的只有 3 条：

| 科目线 | 缺口 | 处置（一次定向杠杆，只对该线） |
|---|---|---|
| `netprofit` S1.82/F1.05 | **SUB/S 0.28**（硬伤）+ 2Y 1.20 | 病灶是持仓广度，不是 S。**decay 20→30** 是唯一不改内容又能加广度的杠杆（平滑换手、提高大盘参与），批次 3 |
| `roe` S1.45/F0.91/2Y1.35 | 三项均缺 ~8–15%，**均匀** | 均匀缺口说明是「强度不足」而非某段失效 ⇒ 同样走 decay 30；若 decay 无效则判本线 dead |
| `total_assets` S1.47/F0.78/2Y0.84 | **2Y 单点崩**（近两年） | 2Y 崩而全期尚可 ⇒ 病灶在近年；decay 30 若不动 2Y 即判死（不磨算子救单段） |

`ebit` / `gps2`（S 1.06–1.16）不救：S 距 1.58 差 0.4+，属机制强度不足，不是参数问题。

## §7 批次 2 设计（multisim `4l4U4ufzO4kvb6E3fFvNnov`，2026-10-21 派发）

两件事并行，都**不动批次 1 的结论**：

1. **延展已验证机制**（不救弱线，换新科目线）：季度口径 `quarterly16` 四条（eps / ebit / eps_reported /
   netprofit_reported）吃「更快的预期修正」；年线底线变体三条（`net2` / `netprofitreported` /
   `reportednet_2`）；非盈利机制三条（`interest_expense` / `bvps` / `dividend`）。
   —— 全部 `alphaCount ≈ 0`，机制读法各不相同（见 §7 表），不是同一概念换三个拼写。
2. **算子轴押后**：算子穷举只对批次 1 里 S ≥ 1.25 的线做，而这三条的首要病灶是 SUB/2Y（广度与近段），
   不是「形状不对」。先跑 decay（广度杠杆），再决定是否需要 `ts_delta` / `ts_rank` / 长短窗比。

**批次 2 预注册判据（与批次 1 同，不重复解释）**：任一候选 S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 /
SUB/S ≥ 0.43 → prod 实测；任一 S ≥ 1.25 但差 1–2 闸 → 先归因，一次定向杠杆；全批 S < 1.0 →
判本壳在**非盈利科目**上亦不跨（本批含 interest/bvps/dividend 三条非盈利线，正好是这条的检验器）。

## §8 批次 2 读数与机制律修正（multisim `4l4U4ufzO4kvb6E3fFvNnov`，10/10 COMPLETE）

| # | 科目线 | alpha | S | F | TO | 2Y | SUB（闸值） | SUB/S | 判读 |
|---:|---|---|---:|---:|---:|---:|---|---:|---|
| 1 | `fxadj_eps_quarterly16` | `Vkdd9dq0` | 0.95 | 0.44 | 5.55% | 1.30 | 0.19（0.41） | 0.20 | 死 |
| 2 | `fxadj_ebit_quarterly16_2` | `zqrrMrjX` | 0.94 | 0.45 | 5.89% | 1.12 | 0.40（0.41） | 0.43 | 死 |
| 3 | **`fxadj_eps_reported_quarterly16`** | `gJWWAWKe` | **1.80** | **1.11** | 4.18% | 1.35 | 0.68（0.78） | 0.38 | **近失（SUB+2Y）** |
| 4 | **`fxadj_netprofit_reported_quarterly16`** | `pwvvXvzq` | 1.52 | 0.87 | 4.37% | 1.16 | 0.65（0.66） | 0.43 | **近失（全项差 4%，SUB 差 0.01）** |
| 5 | `net2` | `d5KKXK7E` | 0.97 | 0.44 | 4.95% | 0.71 | 0.35（0.42） | 0.36 | 死 |
| 6 | `fxadj_netprofitreported_annual12` | `9qEEvE6d` | 1.54 | 0.83 | 3.51% | 1.43 | 0.39（0.67） | 0.25 | 近失但 SUB 硬伤 |
| 7 | `fxadj_reportednet_annual12_2` | `0mjMd5ak` | 0.80 | 0.33 | 4.89% | 1.39 | **−0.02** | neg | 死 |
| 8 | **`interest_expense_annual12`** | `N1eewe5o` | **1.53** | 0.86 | 3.61% | 1.13 | 0.48（0.66） | 0.31 | 近失（非盈利机制也起效） |
| 9 | `fxadj_bvps_annual12` | `rKdd3dr8` | 0.92 | 0.45 | 5.37% | 0.66 | 0.17（0.40） | 0.18 | 死 |
| 10 | `fxadj_dividend_annual12` | `YPxxrx2q` | 0.34 | 0.16 | 5.47% | 1.34 | 0.10（0.15） | 0.29 | 死（**DD 42.9%**） |

### 8.1 机制律修正：不是「每股口径」，而是「盈利兑现口径」

§6.1 把工作区归因为「每股 / 底线 / 回报率口径」，批次 2 把这条**收窄并纠正了两处**：

1. **`bvps` 0.92 与 `dividend` 0.34 否证了「凡每股皆可」**——账面值与分红也是每股口径，
   但它们的预期修正不含「盈利意外」信息。活跃的共性是 **earnings-based**（EPS / 净利润 / 息税前 / 利息费用），
   不是 per-share 这个形式本身。**记入机制库：FA overlay 的 α = 盈利兑现意外的定价残留，与「每股」无关。**
2. **`interest_expense`（1.53）证明机制不限于盈利科目**——利息费用预期下修意味着融资成本改善，
   是**利润率/资本结构**通道而非盈利意外通道。两条通道并存是本数据集可继续扩的理由。

### 8.2 期限结论修正：**年线优先，季度只在「reported」口径下可用**

§5 的设计假设是「季度口径更新鲜、修正更及时」，批次 2 **部分证伪**：

- 同一科目换季度：`eps` 1.89 → **0.95**（腰斩）、`ebit` 1.16 → 0.94。**年度优先。**
  经济读法：年度口径的 FA 序列跨越「去年实际 → 今年预期」的整段重定价，幅度大；
  季度口径里连续两个季度预期差都很小，信噪比低。
- 但 `eps_reported_quarterly16` 1.80 与 `eps_quarterly16` 0.95 **同期限、同壳，差 0.85** ——
  所以真正的主效应是 **reported（GAAP/未调整）vs adjusted（street 调整后）**，期限是二阶。
  **可复用判据：在本壳里，先挑 `reported` 口径，再挑年线；两个条件同时满足时最强**
  （`eps_reported_annual12` 正在批次 3 实测，正是这条判据的直测）。

### 8.3 强线（S ≥ 1.45）的共同病灶：SUB/S 只在 0.20–0.43，唯一例外是已交付的 `e76xgXkM`（0.56）

> 口径限定：本节只讲 S ≥ 1.45 的强线。全族 21 条的比值分布是 **0.03–0.66**，高比值（0.48–0.66）
> 确实存在但在低 S 线上 —— 那是 §8.6 的「另一象限」，不是本节反驳的例外。

10 条 + 参照行里，**8 条 S ≥ 1.45 的线全部因 SUB 或 2Y 落榜**，而 SUB 是主因：

| SUB/S 档 | 线 | 结论 |
|---|---|---|
| 0.56 | `eps_annual12`（已交付） | 唯一过 SUB 的强线 |
| 0.38–0.43 | `eps_reported_quarterly16`（0.38）· `netprofit_reported_quarterly16`（0.43）· `ebit_quarterly16_2`（0.43） | **可救区**：缺口 0.01–0.10 的绝对 SUB，靠广度杠杆 |
| 0.25–0.31 | `netprofitreported_annual12`（0.25）· `interest_expense`（0.31）· `netprofit_annual12`（0.28） | 需先抬 S 再谈 SUB，成本高 |
| < 0.20 | `eps_quarterly16` · `bvps` · `nav` · `pretax` | 收益全在小盘，**结构性不可救** |

> ⚠ 由 §6.2 的 `SUB 闸 = 0.43 × S` 可得一个反直觉推论：**对 SUB/S 不足的线，抬 S 会让闸值同步上移**，
> 所以「S 越高越难救 SUB」在数学上不成立——抬 S 抬高闸值的同时也抬高 SUB，净效果取决于边缘的规模分布。
> 本批实证：`eps_reported_quarterly16` S 1.80 的 SUB 0.68（缺口 0.10）反而比 S 1.52 的 0.65（缺口 0.01）更远。

### 8.4 批次 3（已派发）与批次 4 的靶子

批次 3 = 盈利兑现口径的直测（`eps_annual12_3` cov 0.9779 / `epsreported_annual12` / `gps_fq16` /
`netprofit_quarterly16` / `reportednet` / `ebitda_quarterly16` / `fcf_annual12`）+ 1 条算子轴诊断
（`ts_rank` 替 `ts_zscore`）。**批次 4 = 广度杠杆**：对上表「可救区」的三条线各一次，
按 §8.3 的档位选杠杆（`decay` 20→30 为首选，`winsorize(std=2)` 备选），一次只动一个杠杆。

> 未消除的算子轴（若批次 2 仍不足以补足交付数量再启用）：
> **A** `ts_delta(x, 63)` 替 `ts_av_diff(x, 63)`；**B** `ts_rank(x, 252)` 替 `ts_zscore(x, 252)`；
> **C** 长短比 `ts_mean(x, 22) / ts_mean(x, 252)`。非标窗口不引入；`winsorize` 必须具名 `std=`。

### 8.5 归因四：「持仓广度 = 字段覆盖率」被证伪（2026-10-21，21 条全族对照）

先立假设：SUB/S 低是因为**小盘股的覆盖更全、信号更强**，那么字段覆盖率（cov）应当与 SUB/S 正相关。
**实测直接否证**（21 条已测线，cov 与 SUB/S 的 Pearson r = **−0.116**）：

| 反例 | cov | S | SUB/S |
|---|---:|---:|---:|
| `revenue_annual12` | **0.975**（全族最高档） | 0.99 | 0.41 |
| `net2` | 0.974 | 0.97 | 0.36 |
| `eps_annual12`（已交付） | 0.952 | 1.89 | **0.56** |
| `netprofit_annual12` | 0.950 | 1.82 | **0.28** |
| `ebit_annual12_2` | 0.963 | 1.16 | **0.66**（全族最高） |
| `cfo_annual12` | **0.796**（全族最低档） | 0.90 | **0.53** |

三条同 cov≈0.95 的盈利线，SUB/S 横跨 0.28–0.56；而 cov 最低的 `cfo`（0.796）反而在 0.53。
**结论：SUB/S 不是「数据在哪些股票上存在」的问题，而是「信号在哪些股票上赚钱」的问题。**
⇒ 想修 SUB 只能换内容或换壳（`group` / 中性化 / 平滑），**扩覆盖类杠杆（`ts_backfill`、更长窗口）无效**，
这条与 §4「`ts_backfill` 对事件型字段是污染」同向。

### 8.6 归因五：SUB 与 S 是一对**可分离的两轴**，存在「高比值 / 低强度」象限

把 21 条按 (S, SUB/S) 摆开，最可救的不是 SUB 缺口最小的线，而是**比值已经过线、只欠强度**的线：

| 象限 | 线 | 处置 |
|---|---|---|
| 比值过线 + 强度不足 | `ebit_annual12_2`（S1.16 / 比率 **0.66**）· `roe_annual12_tribes`（S1.45 / **0.55**）· `total_assets_annual12`（S1.47 / 0.48）· `cfo_annual12`（S0.90 / 0.53） | **抬 S 即可**，SUB 会随 S 同步抬而比值不变 ⇒ 结构性可行 |
| 强度过线 + 比值不足 | `netprofit_annual12`（S1.82 / 0.28）· `eps_reported_quarterly16`（S1.80 / 0.38）· `netprofit_reported_quarterly16`（S1.52 / 0.43） | 需改壳（广度杠杆），批次 4 测 |

其中 **`roe_annual12_tribes` 是全族最接近全闸的一条**：S 1.45（差 0.13）/ F 0.91（差 0.09）/
2Y 1.35（差 0.23）**三项同时差 8–15%**，而 SUB 0.80 早已过线。批次 4 的广度臂没有它
（靶子选错：只按 SUB 缺口选，未按「三项同时近失」选）——**批次 5 必须补上它的强度杠杆臂**。

> 归档：全族 147 条字段（92 个不同指标，含覆盖率 / alphaCount / 已测读数 / 未测候选按经济通道分组）
> → [`_usa-analyst-consensus-fa-overlay-field-inventory-20261021.md`](_usa-analyst-consensus-fa-overlay-field-inventory-20261021.md)。

## §9 批次 3 / 4 读数与归因六–八（2026-10-21，21 条实测的终局）

### 9.1 批次 3（8 条，multisim `2eRfha86u4yc8G4KDahyFUg`，全 COMPLETE）

| # | 字段 | alpha | S | F | TO | 2Y | SUB（限） | 判决 |
|---|---|---|---:|---:|---:|---:|---|---|
| 1 | **`fxadj_epsreported_annual12`** | **`0mjj3deK`** | **1.76** | **1.00** | 3.36% | **1.73** | **0.76（0.76）** | **全闸过**（SUB/S=0.432 压线） |
| 2 | `eps_annual12_3` | `O0JJPkb1` | 0.93 | 0.41 | 5.20% | 1.32 | 0.63（0.40） | 死 |
| 3 | `gps_fq16` | `2rjjzRa5` | 1.11 | 0.56 | 5.62% | 1.52 | 0.56（0.48） | S/F 死 |
| 4 | `netprofit_quarterly16` | `9qEE1K9q` | 1.57 | 0.91 | 4.26% | **0.85** | 0.68（0.68） | 2Y 致命 |
| 5 | `reportednet` | `0mjj3dAK` | 0.81 | 0.37 | 6.03% | 1.05 | 0.15（0.35） | 死 |
| 6 | `ebitda_quarterly16` | `omoo5vnk` | 1.01 | 0.56 | 4.42% | **0.09** | 0.28（0.44） | 死 |
| 7 | `fcf_annual12` | `d5KKVmdw` | 0.88 | 0.47 | 3.99% | 0.78 | 0.31（0.38） | 死 |
| 8 | `eps_annual12` + `ts_rank` 轴 B | `e766wKL6` | 1.80 | 1.02 | 3.29% | 1.25 | **0.42（0.78）** | **轴 B 摧毁广度**（比值 0.56→0.42） |

三条可复用读数：

1. **`_3` / `_2` 数字后缀不是"变体"，是另一条更弱的序列**。`eps_annual12_3` S 0.93 vs `eps_annual12` 1.89
   （同壳同批），`ebitda_annual12` 0.86 vs `ebit_annual12` 1.16。**字段目录里带尾号的先按独立弱线处理**，
   不要把 `_3` 当作"第 3 个版本"去凑数。
2. **`ts_rank` 归一轴（轴 B）是广度杀手**：同字段 S 1.89→1.80（−0.09），但 SUB 比值 0.56→0.42（−0.14）
   ⇒ 把"有界化"当成修 SUB 的手段是反的：`ts_rank` 抹掉了跨股绝对强度，恰好抹掉了大盘股的贡献。
3. **全闸通过可以卡在 0.000 余量**：`0mjj3deK` SUB 0.76 对闸值 0.76（0.43×1.76=0.7568→0.76 进位）。
   平台按显示值比较，所以「压线」是真实状态，不是四舍五入的错觉。

### 9.2 批次 4（9 条，multisim `1kyXsI7sh4Nw9Gh1jlwoJuE`，全 COMPLETE）＝ 广度杠杆三臂

每条都附**同字段基线**的差值，这是本批的重点（基线 = 批次 1/2 的冻壳 decay 20 / std 4 / hump 0.01）：

| 臂 | 字段 | alpha | S | F | 2Y | SUB（限） | SUB/S | Δ2Y | ΔSUB |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| 基线 | `netprofit_annual12` | `mLYYpKaW` | 1.82 | 1.05 | 1.20 | 0.51（0.79） | 0.28 | — | — |
| A decay30 | `netprofit_annual12` | `WjLLQQKk` | 1.83 | 1.06 | **1.17** | 0.46（0.79） | 0.251 | −0.03 | −0.05 |
| B std=2 | `netprofit_annual12` | `XgRRQQPa` | 1.84 | 1.07 | 1.21 | 0.48（0.80） | 0.261 | +0.01 | −0.03 |
| C hump.005 | `netprofit_annual12` | `omoo55vv` | 1.81 | 1.05 | **1.33** | 0.44（0.78） | 0.243 | **+0.13** | −0.07 |
| 基线 | `fxadj_eps_reported_quarterly16` | `gJWWAWKe` | 1.80 | 1.11 | 1.35 | 0.68（0.78） | 0.378 | — | — |
| A decay30 | `fxadj_eps_reported_quarterly16` | `vROOMMaG` | 1.78 | 1.10 | **1.48** | 0.58（0.77） | 0.326 | **+0.13** | **−0.10** |
| B std=2 | `fxadj_eps_reported_quarterly16` | `78oobb05` | 1.81 | 1.12 | **1.42** | 0.65（0.78） | 0.359 | +0.07 | −0.03 |
| C hump.005 | `fxadj_eps_reported_quarterly16` | `P0MMaa6x` | 1.81 | 1.13 | 1.40 | 0.63（0.78） | 0.348 | +0.05 | −0.05 |
| A decay30 | `fxadj_netprofit_reported_quarterly16` | `O0JJPPwv` | 1.46 | 0.82 | 1.25 | 0.50（0.63） | 0.342 | — | — |
| A decay30 | `fxadj_netprofitreported_annual12` | `pwvvrrJx` | 1.44 | 0.75 | 1.41 | 0.27（0.62） | 0.188 | — | — |
| A decay30 | `interest_expense_annual12` | `gJWWOOwm` | 1.58 | 0.91 | 1.05 | 0.49（0.68） | 0.310 | — | — |

### 9.3 归因六：`decay` / `hump` 是 2Y 杠杆，**且与 SUB 直接对抗**

同一条线（`fxadj_eps_reported_quarterly16`）四个档位给出整齐的反向配对：
`d30` Δ2Y **+0.13** ↔ ΔSUB **−0.10**；`winsorize std=2` +0.07 ↔ −0.03；`hump 0.005` +0.05 ↔ −0.05。
`netprofit` 上同样成立（hump 0.005：Δ2Y +0.13 ↔ ΔSUB −0.07）。

**机制**：慢化（更长 decay / 更强 hump）= 持仓更粘 = 近两年收益更稳，但同一时点覆盖的票更少 ⇒ 子宇宙 Sharpe 下降。
**推论**：这条线需要 **2Y +0.16 且 SUB +0.13**，两个缺口在杠杆上是**互斥**的（每个杠杆都在修一个的同时弄坏另一个）
⇒ `fxadj_eps_reported_quarterly16` **结构性不可达，判死**。
这条同时否证了 §8.4 的「批次 4 = 广度杠杆能救」这一预设——**它不是广度问题，是广度与近端稳定性的取舍**。

### 9.4 归因七：壳层杠杆对本族 S 是**零位移**（跨 3 批 25 条复证）

- `netprofit` 四个壳：S **1.81–1.84**（极差 0.03）；`fxadj_eps_reported_quarterly16` 四个壳：**1.78–1.81**。
- 对比 1.58 的闸与 0.13 的缺口 ⇒ **微调壳层在统计上无法把任何一条线送过闸**。
- 唯一真正能动 S 的两件事：**换字段**（0.81–1.84，跨 1.0）与 **换归一轴**（`ts_rank` 反降 0.09）。
- 推论：`roe_annual12_tribes`（1.45）/ `total_assets_annual12`（1.47）的强度缺口**不靠 decay/winsorize/hump 补**；
  本族唯一还没测过的 S 杠杆是 **`group_rank` 的分组粒度**（industry → subindustry），批次 5 用它作最后的判据。

### 9.5 归因八（终局判据）：S 与 SUB/S 必须**同时**过线，21 条里只有 2 条做到

| 条件 | 含义 | 线 |
|---|---|---|
| S ≥ 1.58 且 比值 ≥ 0.43 | **可交付** | `e76xgXkM`（已交付）· `0mjj3deK`（prod 0.7204 / self 0.7206 双卡） |
| S ≥ 1.58 且 比值 < 0.43 | 广度缺陷，杠杆互斥 | `netprofit` 0.28 · `eps_rep_q16` 0.38 · `netprofit_rep_q16` 0.43 · `eps_rep_q16_2` 等 |
| S < 1.58 且 比值 ≥ 0.43 | 强度缺陷，壳层无效 | `ebit_annual12_2` 0.66 · `roe_tribes` 0.55 · `total_assets` 0.48 · `cfo` 0.53 |
| 两者皆 < | 死 | 其余 13 条 |

### 9.6 一条顺带核实的外部读数：**prod 数值会漂移，入库值不等于现值**

交付清单里的 `pw5RbrYX` / `leKKGb9l` 在 DB 里的 prod 是 **0.5857 / 0.5896**（2026-10-17 写入），
但 2026-10-21 实测已到 **0.9000 / 0.9014**；`58gp1wdz`（目标价 tribes 壳，S1.89/F1.18/2Y1.72/SUB0.94）
DB 里 3 小时前的 prod 是 **0.6738**，本次 `refresh=True` 复测 **0.9868**（直方图 `[0.9,1]` n=1）。

⇒ **可复用纪律**：`get_submit_ready` / `alphas.prod_correlation` 里的值只作线索，**任何候选在进入交付表之前必须
`check_correlation(refresh=True)` 复测**；同一天内数小时就能从 0.67 漂到 0.99（当天有新 alpha 落地就会推高全池）。
`58gp1wdz` 因此判死，本族不再考虑目标价巷（该巷当日已整体饱和）。

---

## 10. 批次 5（group_rank 粒度）× D0-P 结构尝试（2026-10-21）

### 10.1 批次 5：把 `group_rank` 从 industry 换到 subindustry

设置其余全冻结（decay 20 / REVERSION_AND_MOMENTUM / trunc 0.08 / TOP3000 / D1）。

| 臂 | 字段 | alpha | S | F | TO | 2Y | SUB（限） | SUB/S | 判 |
|---|---|---|---|---|---|---|---|---|---|
| roe × subindustry | `roe_annual12_tribes` | `j2eeb5QQ` | 1.41 | 0.83 | 3.83% | 1.29 | **0.73**（0.61） | **0.518** | 三闸皆缺，S 反而降 |
| roe × decay30 | 同上（industry） | `RRAAnJLz` | 1.38 | 0.85 | 4.16% | 1.30 | 0.63（0.59） | 0.457 | decay 不抬 2Y |
| **assets × subindustry** | `total_assets_annual12` | **`gJWWEYvJ`** | **1.71** | 0.94 | 3.20% | 1.31 | **1.01**（0.74） | **0.591** | **仅缺 F 与 2Y** |
| grossmargin | `grossmargin_annual12` | `2rjjb1EN` | 0.60 | 0.28 | 4.66% | 0.35 | 0.47 | 0.78 | 判死 |
| opex | `operatingexpense_annual12` | `d5KKA2qY` | 1.17 | 0.58 | 3.82% | 0.61 | 0.27（0.51） | 0.231 | 判死 |
| shares | `sharesoutstanding_annual12` | `gJWWEY7J` | 1.35 | 0.69 | 3.40% | 0.44 | 0.19（0.58） | 0.141 | 判死（稀释无持续性） |
| netdebt | `netdebt_annual12` | `pwvvAqQV` | 0.76 | 0.38 | 4.97% | 0.56 | 0.36 | 0.474 | 判死 |
| cfps | `cfps_annual12` | `omooM1QE` | 0.67 | 0.29 | 4.75% | 0.76 | 0.34 | 0.507 | 判死 |

### 10.2 归因九：`group_rank` 粒度是**第三条轴**，它不只是广度杠杆，也可能同时抬 S

对比同一字段的 industry 版（批次 1）与 subindustry 版：

| 字段 | industry S / SUB(限) / 比值 | subindustry S / SUB(限) / 比值 | Δ |
|---|---|---|---|
| `total_assets_annual12` | 1.47 / 0.70（0.63）/ **0.48** | **1.71** / **1.01**（0.74）/ **0.591** | S +0.24、比值 +0.11 |
| `roe_annual12_tribes` | 1.45 / 0.80（0.62）/ 0.55 | 1.41 / 0.73（0.61）/ 0.518 | S −0.04、比值 −0.03 |

⇒ **粒度效应是字段特定的，不是通用杠杆**：对「规模 / 资产负债表」类字段，行业内的相对扩张才是信号
（同业可比是这类比率的天然分母）；对 roe 这类已在行业内标准化的字段，再切一层只是把样本摊薄。

**机制命名（可复用）**：`total_assets_annual12` = 「预测 + 实际」资产负债表规模的叠加单序列，
其 63 日变化 = **分析师对扩张规模的预期修正**（capacity expansion revision），不是资产增长异象的反向。
符号为正说明市场对「公司要变大」的预期修正存在**反应不足**（后续 drift 向上），而不是 Cooper-Gulen-Schill 的
高资产增长折价——后者是**已实现**资产增长，方向相反。两条线同字段不同口径，别混用。

### 10.3 D0-P 唯一结构尝试：`0mjj3deK` 换中性化 → **判死**

`0mjj3deK`（`fxadj_epsreported_annual12`，S1.76 / F1.00 / 2Y1.73 / SUB0.76 压线；prod 0.7204 / self 0.7206）
按 D0-P 0.70–0.75 档做一次带诊断的结构尝试：只把 `neutralization` 从 REVERSION_AND_MOMENTUM 换成 SUBINDUSTRY
（`N1eev0gE`，单条仿真，其余冻结）。

| 指标 | `0mjj3deK`（原） | `N1eev0gE`（SUBINDUSTRY） | 判定 |
|---|---|---|---|
| Sharpe | 1.76 | 1.62 | 仍过 |
| Fitness | **1.00** | **0.85** | ✗ 破 |
| Turnover | 3.36% | **0.93%** | ✗ 破 1% 地板 |
| 2Y | 1.73 | **1.98** | 大幅改善 |
| SUB（限） | 0.76（0.76） | **0.60（0.70）** | ✗ 反而恶化 |
| risk_neutralized_sharpe | — | 1.13 | 非纯风格 |

⇒ **中性化换挡对本族是负向的**：它把持仓摊平到同行业内，换手跌穿地板，同时 sub-universe 反而更差
（说明原壳的超额来自**行业间**配置，subindustry 中性化正好抹掉它）。D0-P 触发条件成立（尝试失败）
⇒ `0mjj3deK` 记 **dead_end**，本族 eps 年线支路关闭。

### 10.4 批次 7（已收，读数见 §11.2）：用 assets 的 SUB 余量换 2Y 与 F

`gJWWEYvJ` 的 SUB 1.01 对限 0.74，**余量 0.27**，是 21 条线里唯一能「花 SUB 买 2Y」的位置。
按定律 16 的对抗关系设计两批（同表达式跨批不触发去重）：

- 批 A（decay 20，`3zsYot2oZ4Mbbr2WChyDTit`，5 条）：`winsorize std=2` / `hump=0.005` / 两者叠加 /
  `ts_zscore` 窗口 252→126 / `ts_av_diff` 窗口 63→22。
- 批 B（decay 30，`3NSufh4oe5bCbHa18DJZf1m4`，4 条）：裸壳 / std2 / hump5 / std2+hump5。

判据：F ≥ 1.0 且 2Y ≥ 1.58 且 SUB ≥ 0.43×S。窗口臂（A4/A5）是**换内容**不是调平滑，
若二者之一同时抬高 F 与 2Y，则本族从「平滑杠杆」转回「信号时效」轴。

---

## 11. 批次 6 / 7 读数与**三条终局定律**（2026-10-21，14 条实测）

### 11.1 批次 6：level 轴（去掉 `ts_av_diff`）——**F 富、2Y 穷**

壳层只换一个项：`ts_zscore(ts_av_diff(vec_avg(F),63),252)` → `ts_zscore(vec_avg(F),252)`，
其余（quantile / group_rank industry / hump / backfill / winsorize std=4 / decay 20 / RM 中性化）全冻结。
multisim `1j9SJfqL4CHcw3hYcqClUU`，5/5 COMPLETE：

| 臂 | 字段（`mean_forecast_actual_combined_*`） | alpha | S | F | TO | RET | 2Y | SUB（限） | 判 |
|---|---|---|---|---|---|---|---|---|---|
| epsrep | `fxadj_epsreported_annual12` | **`P0MMd7G7`** | 1.74 | **1.09** | 3.74% | **4.91%** | **1.37** | **0.83（0.75）PASS** | **只缺 2Y** |
| netprofit | `netprofit_annual12` | `j2eebj6k` | **1.92** | **1.25** | 3.73% | **5.34%** | **1.48** | 0.55（0.83） | 缺 2Y + SUB |
| roe | `roe_annual12_tribes` | `3qjjZllz` | 1.40 | 0.91 | 4.40% | 5.25% | 0.66 | 0.56（0.61） | 判死 |
| grossmargin | `grossmargin_annual12` | `wp99Mjjv` | 0.62 | 0.27 | 4.46% | 2.41% | 0.49 | 0.26（0.27） | 判死 |
| cfps | `cfps_annual12` | `E5VVXlvJ` | 0.75 | 0.36 | 4.76% | 2.91% | 1.15 | 0.07（0.32） | 判死 |

**归因十（level 轴的第二面）**：§8.3 记「change 轴 SUB 贫、2Y 富」，level 轴正好相反 ——
`P0MMd7G7` SUB 比值 0.83/1.74 = **0.477**（change 轴 21 条只有 2 条过 0.43），
但 2Y 只有 1.37。两条轴**各自缺一条不同的腿**，且互不互补（同字段不能同时走两条轴相加，
那是混信号）。level 轴的真正收获是 **RET**：4.9–5.3%，是 change 轴（3.6–3.8%）的 1.4 倍，
这一条直接决定了 F —— 见 §11.3。

`P0MMd7G7` 的处置：**平台侧全绿**（唯一非 PASS 项是 `LOW_2Y_SHARPE` 的 WARNING，2Y 1.37），
但内部 `review.two_year_sharpe_min = 1.6` 未达。2Y 的可行杠杆只有 decay / 长窗 / level↔change，
全部在 §9.3 / §11.2 实测为「S 中性或负、且伤 SUB」。**0.21 的 2Y 缺口没有可用杠杆**
⇒ 不投 D0-P 结构尝试（prod 0.7435、直方图 [0.7,0.8) 有 **n=25**，0.70–0.75 档只能做一次，
留给真有结构空间的位置才是对的用法）⇒ 记 **dead_end**。

### 11.2 批次 7：用 assets 的 SUB 余量买 2Y —— **买不到，且把 S 卖了**

multisim `3zsYot2oZ4Mbbr2WChyDTit`（A，decay 20）+ `3NSufh4oe5bCbHa18DJZf1m4`（B，decay 30），9/9 COMPLETE。
基线 = 批次 5 的 `gJWWEYvJ`：S1.71 / F0.94 / TO3.20% / RET3.76% / 2Y1.31 / SUB1.01（0.74）。

| 臂 | 改动 | alpha | S | F | TO | RET | 2Y | SUB（限） |
|---|---|---|---|---|---|---|---|---|
| **基线** | 裸壳 subindustry | `gJWWEYvJ` | **1.71** | **0.94** | 3.20% | 3.76% | 1.31 | 1.01（0.74） |
| A1 | `winsorize std=2` | `88vvdjlo` | 1.67 | 0.91 | 3.20% | 3.69% | 1.32 | 1.07（0.72） |
| A2 | `hump=0.005` | `leMMbvj7` | 1.65 | 0.89 | 3.31% | 3.64% | 1.15 | 0.84（0.71） |
| A3 | std2 + hump5 | `qMEEoxjE` | 1.66 | 0.89 | 3.20% | 3.63% | 1.31 | 1.04（0.72） |
| A4 | `ts_zscore` 252→126 | `9qEELjXe` | 1.64 | 0.88 | 3.28% | 3.63% | **1.06** | 0.88（0.71） |
| A5 | `ts_av_diff` 63→22 | `0mjj0XRk` | 1.73 | **0.95** | 3.27% | 3.75% | **1.16** | 0.91（0.75） |
| B1 | 裸壳 decay30 | `VkddgPN8` | 1.63 | 0.87 | 3.24% | 3.56% | 1.36 | **1.03**（0.71） |
| B2 | std2 + decay30 | `XgRR5naz` | 1.59 | 0.84 | 3.24% | 3.51% | **1.38** | 1.05（0.69） |
| B3 | hump5 + decay30 | `mLYYMbKp` | 1.62 | 0.87 | 3.32% | 3.59% | 1.35 | 0.87（0.70） |
| B4 | std2+hump5 + decay30 | `ZYmmenXj` | 1.65 | 0.88 | 3.23% | 3.59% | 1.37 | 1.02（0.71） |

**归因十一：定律 16 的「decay↔SUB 对抗」不普适**。B1 vs 基线（只差 decay 20→30）：
2Y 1.31→**1.36**、SUB 1.01→**1.03** —— 两个都涨，对抗关系在此消失。真实代价在 **S：1.71→1.63**，
于是 F 0.94→0.87。**decay 是「S 换 2Y」的兑换，不是免费杠杆**，兑换率 0.08 S : 0.05 2Y 明显不划算。

窗口臂反向：`ts_zscore` 252→126 把 2Y 打到 **1.06**、`ts_av_diff` 63→22 打到 **1.16** ——
两个窗口都是**长窗支持 2Y**（与 A4/A5 的「换内容」假设相反）。故 assets 支路的两条轴都堵死：
买 2Y 的唯一有效杠杆（decay）同时卖 S，而 S 一旦掉到 1.65 以下 F 必破（§11.3）。

⇒ **assets 支路终局**：F ≤ 0.95、2Y ≤ 1.38，距双线（F≥1.0 / 2Y≥1.6）分别差 0.05 / 0.22，
9 个杠杆臂全部同向变差。记 **dead_end**。

### 11.3 定律 17：**Fitness 是 S 与 RET 的导出量，不是独立旋钮**

用本族 5 个独立臂做数值核验，公式（TO < 12.5% 时）为：

```
F = S · sqrt( |RET| / max(TO, 0.125) )        # TO 以小数计；本族 TO 3.2–4.8% 全部 < 12.5%
  ⇒ F ≥ 1  ⇔  RET ≥ 0.125 / S²
```

| alpha | S | RET | TO | 公式算 F | 平台 F |
|---|---|---|---|---|---|
| `88vvdjlo` | 1.67 | 3.69% | 3.20% | 0.907 | **0.91** |
| `0mjj0XRk` | 1.73 | 3.75% | 3.27% | 0.948 | **0.95** |
| `XgRR5naz` | 1.59 | 3.51% | 3.24% | 0.843 | **0.84** |
| `P0MMd7G7` | 1.74 | 4.91% | 3.74% | 1.091 | **1.09** |
| `j2eebj6k` | 1.92 | 5.34% | 3.73% | 1.255 | **1.25** |

**用法（选波阶段就能算，零仿真成本）**：
- 低换手族（TO < 12.5%）里 **F 只有两个自由度：S 与 RET**。调 decay / hump / winsorize 改的是
  TO（进而微调 RET），对 F 的净效应通常是负的（§11.2 实测）。
- **先算这条族能不能过 F**：本族 change 轴 RET 3.6–3.8% ⇒ 想过 F 必须 **S ≥ 1.82**；
  而 change 轴 21 条的 S 上限是 1.71 ⇒ **F 在结构上就过不去**，不是「再调调」的问题。
  level 轴 RET 4.9–5.3% ⇒ S ≥ 1.55 即可过 F，实测 1.74/1.92 全过 —— 与读数一致。
- 因此选字段时 **RET（单位夏普的收益厚度）与 S 并列为一等指标**；只看 S 会整批撞在 F 上。
  这条替换掉 §9.3 里「F 是 S 的函数，只能靠提 S」的粗口径：F 是 (S, RET) 的函数，
  而 RET 由**信号形态**（level vs change、报告口径 vs 预测口径）决定，改壳改不出来。

### 11.4 族级终局与转向判据（同数据集，换机制）

7 批 67 条实测后，本族（`mean_forecast_actual_combined_*` 叠加单序列）的账：

| 类别 | 条数 | 明细 |
|---|---|---|
| 交付 ACTIVE | 1 | `e76xgXkM`（`fxadj_eps_annual12` change） |
| 过 IS、卡 prod | 2 | `0mjj3deK` 0.7204（中性化尝试失败 ⇒ dead_end）、`P0MMd7G7` 0.7435（2Y 无杠杆 ⇒ dead_end） |
| 其余 | 64 | 全部至少缺 1 条硬线（S/F/2Y/SUB） |

**判据**：族内「形态学」（字段 × 轴 × 粒度 × 平滑 × 窗口）已穷尽，任何新增臂都落在
已实测过的同一张 (RET, S, SUB/S) 曲面内 ⇒ **不再在本族扩臂**。
转向**同数据集内的新机制**（`analyst_consensus` 本身有 3424 字段，已用的只是
`mean_forecast_actual_combined_*` 一个前缀族）：分歧度（`stddev_estimate_*`，384 字段）、
覆盖度（`estimate_count_*`，cov 0.978）、意外（`mean_surprise_value_*`）、
厂商快照修正（`*_three_months_prior_*` / `*_four_weeks_prior_*`）。
这些字段**不经过「实际值叠加」**，是与已交付 5 颗不同的单序列，机制与口径都正交。

### 11.5 批次 8（已收，读数见 §12）：新机制 × 同一冻结壳

multisim `3xVeuC6TU4sNbTmK4o8bIW`（A：D1/D2/D3/D5/R1）+ `3Sov1ZbWj4rzbNT1hAp3QpM`（B：R2/C1/C2/S1/S2），
10 臂，全部 industry / decay 20 / RM / trunc 0.08 / TOP3000 / D1：

| 臂 | 机制 | 核心构造（`change` 壳 = 外层再套 `ts_zscore(…,252)`） |
|---|---|---|
| D1 | 分歧（4 周） | `vec_avg(stddev_estimate_fxadj_eps_annual12) / (vec_avg(stddev_four_weeks_prior_fxadj_eps_annual12_3)+1e-6) - 1` |
| D2 | 分歧（3 月） | 同上换 `three_months_prior` |
| D3 | 分歧（营收 3 月） | 营收口径同 D2 |
| D5 | 分歧水平（CV） | `vec_avg(stddev_estimate_fxadj_eps_annual12) / (abs(vec_avg(median_estimate_fxadj_eps_annual12))+1e-4)`，**level 壳** |
| R1 | 修正（EPS 3 月） | `vec_avg(mean_estimate_fxadj_eps_annual12) / (abs(vec_avg(mean_estimate_three_months_prior_fxadj_eps_annual12_3))+1e-4) - 1` |
| R2 | 修正（营收 3 月） | 营收口径同 R1 |
| C1 | 覆盖（EPS 3 月） | `vec_avg(estimate_count_current_period_eps_annual12_3) / (vec_avg(estimate_count_three_months_prior_eps_annual12_3)+1e-4) - 1` |
| C2 | 覆盖（营收 3 月） | 营收口径同 C1 |
| S1 | 意外（EPS，PEAD） | `ts_mean(vec_avg(mean_surprise_value_fxadj_eps_annual12) / (abs(vec_avg(actual_value_fxadj_eps_annual12))+1e-4), 504)` |
| S2 | 意外（营收，PEAD） | 营收口径同 S1 |

设计要点：
1. **单位自消**：分歧与覆盖全部用「当期 / 历史快照 − 1」，分子分母同量纲，不存在市值/股价污染；
   修正用 `abs(历史)+1e-4` 归一，避免 EPS 近零爆炸（外层的 `winsorize std=4` 兜底）。
2. **不混信号**：每条只用一个机制；D5 是「分歧 / 共识水平」的变异系数（一个量），不是两条腿相加。
3. **`preflight_expressions` 只报 `std` 为 unknown**（`winsorize(..., std=4)` 的具名参数被误读成字段），
   18 个真实字段全部 recognized ⇒ 已知误报，不阻塞。
4. 按 §11.3 预判 F：分歧/覆盖/修正三类若 RET 落在 3.5–4% 区间，需 S ≥ 1.79 才过 F；
   S1/S2 的 `ts_mean(…,504)` 是慢变量，若 RET 够厚则 F 不构成瓶颈。**读数先看 RET/S 比值再看闸**。


---

## 12. 批次 8 读数：新机制四类，两条只差 SUB（2026-10-21）

### 12.1 读数表（10 臂，冻结壳，industry / decay 20 / RM）

| 臂 | 机制 | alpha | S | F | TO | RET | 2Y | SUB（限） | 比值 | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | 分歧 eps 4 周 | `LL55J5G9` | 1.36 | 0.78 | 5.08% | 4.10% | **0.75** | 0.11（0.59） | 0.081 | S F SUB 2Y |
| D2 | 分歧 eps 3 月 | `3qjjLjpP` | 1.56 | 1.01 | 5.14% | 5.24% | 1.51 | 0.63（0.68） | 0.404 | S SUB 2Y |
| D3 | 分歧 营收 3 月 | `YPxxqx76` | 1.53 | 0.99 | 5.40% | 5.20% | **1.70** | 0.61（0.66） | 0.399 | S F SUB |
| D5 | 分歧水平（CV） | `LL55J579` | 1.46 | 0.86 | 4.28% | 4.38% | **1.77** | 0.41（0.63） | 0.281 | S F SUB |
| **R1** | **修正 eps 3 月** | **`bl88E8jM`** | **1.71** | **1.15** | 5.20% | **5.62%** | **1.66** | **0.67（0.74）** | **0.392** | **仅 SUB** |
| R2 | 修正 营收 3 月 | `O0JJaRWp` | 0.85 | 0.39 | 5.28% | 2.65% | 1.39 | 0.48（0.37） | 0.565 | S F 2Y |
| C1 | 覆盖 eps 3 月 | `P0MM9xPJ` | 0.53 | 0.17 | 5.03% | 1.36% | −0.28 | 0.19（0.23） | 0.358 | 判死 |
| C2 | 覆盖 营收 3 月 | `pwvvOxWo` | 0.57 | 0.19 | 5.00% | 1.46% | 0.20 | 0.22（0.25） | 0.386 | 判死 |
| **S1** | **意外 eps（PEAD）** | **`omooORP6`** | **1.62** | **1.21** | 4.73% | **6.93%** | **1.96** | **0.52（0.70）** | **0.321** | **仅 SUB** |
| S2 | 意外 营收（PEAD） | `3qjjL1GO` | 1.15 | 0.77 | 4.89% | 5.62% | **1.97** | **0.55（0.50）** | 0.478 | S F |

**⚠ 子任务顺序 ≠ payload 顺序**：`bl88E8jM` 是 R1（修正）、`LL55J579` 是 D5（分歧水平），
初版读数按 payload 顺序错记过一次，已按 `GET /alphas/{id}` 的 `regular.code` 逐条核回。

### 12.2 归因十二：四类新机制的族内排序与三条结构事实

1. **EPS 口径全面优于营收**：修正 1.71 vs 0.85、意外 1.62 vs 1.15；分歧两者相当（1.56 / 1.53）。
   与论坛「营收 surprise 更干净（EPS 可被一次性项目/税/回购操纵）」的结论**相反**——
   注意本集的营收口径混用了不同后缀族（`*_revenue_annual12_tribes` 与无 `_3` 的 prior 快照），
   口径不齐可能是主因，不能据此否定论坛结论。
2. **覆盖（estimate_count）判死**：S 0.53 / 0.57、2Y 负值或近零。分析师数量变化不是信号，
   只能当**质量筛选条件**（论坛同结论：覆盖稀疏 = 噪声大），不能当主腿。C1/C2 记 dead_end。
3. **分歧窗口越长越好**：4 周 2Y 0.75 → 3 月 1.51（eps）/ 1.70（营收）。与论坛报告
   「分歧在公告后 1–2 个月逐步收敛」的时标一致，3 个月窗口把收敛过程完整装进去。
   分歧**符号**：本族四条都是「分歧上升 → 正 rank」且 S 为正，与论坛/东方证券报告
   「收敛为正（`conv_rate = -ts_delta(dispersion, 10)`）」**方向相反**。S 只有 1.5 上下、
   且 SUB 全灭，不足以判定谁对；符号翻转作为未验证假设留在 §12.4，不占用本族剩余预算。
4. **RET 与机制强度排序**：意外 6.93% > 修正 5.62% > 分歧 5.2% > 覆盖 1.4%。
   按 §11.3 的 F 定律（TO < 12.5% 时 F ≥ 1 ⇔ RET ≥ 0.125/S²）：意外线在 S1.62 时阈值 4.76%
   ⇒ **F 1.21 富余**；修正线在 S1.71 时阈值 4.27% ⇒ **F 1.15 富余**。
   **两条线都不再是「F 结构性不可达」**——上一族（FA-overlay 变化量）RET 3.6–3.8% 的死结，
   在新机制里被 RET 厚度打开了。
5. **SUB 成为唯一剩闸，且两线缺口不同**：R1 比值 0.392（差 10%）、S1 比值 0.321（差 34%）。
   同一机制内营收版 SUB 表现更好（S2 比值 0.478 过闸而 S1 不过），说明 EPS 意外的超额集中在
   大市值 / 少数名字，sub-universe 里被稀释——这是**组合广度**问题，不是信号方向问题。

### 12.3 论坛取证（两条，均已全文读取）

- **帖子 35650057943959**（ZW71478，2025-10-15，14 赞，转述东方证券研报）：
  以 `spread = high − low`、`dispersion = spread / ts_mean(mean, 20)`、`conv_rate = -ts_delta(dispersion, 10)`
  → `group_zscore(zscore(conv_rate), industry)`。**把归一窗 20→30、收敛窗 10→30 后，Sharpe / Returns /
  Fitness 三者同时上升**（作者仍卡 Fitness）。可复用点是**分母去噪**：用 `ts_mean(level, 30)`
  平滑后再做分歧率，而不是直接 `stddev / |median|`（本集 D5 的写法，SUB 只有 0.41）。
- **帖子 42827593886487**（WL27618，2026-08-19，30 赞）：**水平不重要、变化才重要**；
  修正漂移是经典用法；**营收 surprise 比 EPS 干净**；**分歧越大未来回报越差**（⇒ 分歧水平应取负向）；
  季度低频更新天然低换手；**覆盖数可当质量过滤器**；排名前先 winsorize。
  评论补充：分析师修正族在 KOR/日本结构性偏弱；**分歧类构造对分组粒度敏感，industry 优于全局排名**。

**与本批实证的对照**：①「变化 > 水平」被证实（D5 水平线 SUB 0.41 最差、S 1.46 最低）；
②「覆盖当过滤器」被证实（C1/C2 当主腿判死）；③「industry 优于全局」与本族壳一致（沿用）；
④「营收优于 EPS」在本集**未被证实**（口径不齐，见 §12.2 第 1 条），暂不改写。

### 12.4 批次 9（已发，进行中）：只修 SUB，两条线各一张卡

multisim `Bu3Zg85M4KUc8m1eIudV8Id`（R1）+ `13ZdPAfb955s93NOArtVS0c`（S1），全部冻结壳、decay 20 / RM 除注明：

| 臂 | 核心 | 变更 | 依据 |
|---|---|---|---|
| A1 | R1 | `group=subindustry` | 资产线实测：粒度细分把 SUB 比值 0.48→0.591 |
| A2 | R1 | `group=subindustry` + `hump=0.005` | 平滑更浅，测是否保住广度 |
| A3 | S1 | `group=subindustry` | 同上 |
| A4 | S1 | `group=subindustry` + `hump=0.005` | 同上 |
| A5 | S1 | `group=subindustry` + `ts_mean` 504→252 | 意外线缩短记忆，测 RET/S 是否更厚 |
| B1 | R1 | `neutralization=SUBINDUSTRY` | 直接换中性化域（USA 11 档全开） |
| B2 | S1 | `neutralization=SUBINDUSTRY` | 同上 |
| B3 | R1 | `neutralization=STATISTICAL` | 风险模型中性化，可能抬高 sub-universe 比率 |
| B4 | S1 | `neutralization=STATISTICAL` | 同上 |
| B5 | R1 | `group=subindustry` + decay 30 | decay→SUB 在资产线是小幅正向（+0.02） |

**判据（预注册）**：S ≥ 1.58 / F ≥ 1.0 / **SUB/S ≥ 0.43** / 2Y ≥ 1.6。
任一条全过即进 prod 实测（`check_correlation(refresh=True)` 必须 < 0.70）；
若两条线的最好臂 SUB 比值仍 < 0.43，则「冻结壳 + 单一机制」在本集不再有 SUB 解，
处置按 D0-P：R1 与 S1 都记「IS 可过、SUB 结构性不可达」的 dead_end，本集收官转下一数据集。

---

## 13. 纯预期族字段台账（`mean_estimate_*` / `mean_surprise_value_*` / `actual_value_*`）

平台 `analyst_consensus` 共 **3424 字段**（VECTOR 3394 / MATRIX 30）。其中「纯预期」三族
（不含实际值叠加）合计约 **700 条**，是本族唯一还有正交余量的部分。按科目汇总（`coverage` 取平台值）：

| 科目（annual12 口径） | 当期均值 | 3 月前快照 | 4 周前快照 | 可做 revision | cov |
|---|---|---|---|---|---|
| eps（`fxadj_eps_annual12_3`） | 0.9779 | **0.9607** | 0.9699 | 是 | 最高 |
| eps（`fxadj_eps_annual12`，R1 用） | 0.9521 | 0.9607（`_3` 口径） | — | 是 | 高 |
| **epsreported** | 0.9433 | **无** | **无** | **否** | 高 |
| **reportednet_annual12_2** | 0.9589 | **0.9367** | 0.9465 | **是（GAAP）** | 高 |
| **pretax_reported_annual12** | 0.9432 | **0.9160** | 0.9268 | **是（GAAP）** | 高 |
| pretax_annual12 | 0.9665 | 0.9463 | 0.9563 | 是 | 高 |
| ebit_annual12_2 | 0.9632 | 0.9426 | 0.9527 | 是 | 高 |
| ebit_quarterly16 | 0.9191 | 0.8888 | 0.9039 | 是 | 中高 |
| net2 | 0.9742 | 0.9560 | 0.9654 | 是 | 高 |
| revenue_annual12 | 0.9751 | 0.9565 | 0.9656 | 是 | 最高 |
| ebt_annual12 | 0.8808 | 0.8555 | 0.8667 | 是 | 中高 |
| roe_annual12 | 0.8705 | 0.8358 | 0.8475 | 是 | 中 |
| dividend_annual12 | 0.8591 | 0.8197（`_2`） | 0.8291 | 是 | 中 |
| **ebitda_annual12** | 0.8636 | **无** | **无** | **否**（仅 `quarterly16` 有） | 中 |
| cfps_annual12 | 0.7331 | 0.6987 | 0.7110 | 是 | 中低 |
| bvps_annual12 | 0.8278 | 0.7856 | 0.7991 | 是 | 中低 |
| capex_annual12_2 | 0.8334 | 0.7930 | 0.8045 | 是 | 中 |
| grossmargin_annual12 | 0.7607 | 0.7282 | 0.7379 | 是 | 中低 |
| fcf_quarterly16 | 0.3887 | 0.3515 | 0.3679 | 是（但 cov 太低） | 低 |

**surprise 族覆盖率对照**（决定 PEAD 腿能否自救）：

| 字段 | cov | 备注 |
|---|---|---|
| `mean_surprise_value_fxadj_eps_annual12`（S1 用） | ≈0.70（`mean_surprise_value` 基口径 0.6964） | 已跑出 RET 6.93% |
| **`avg_surprise_net_income`（/`_fxadj`）** | **0.9228** | 覆盖最广的 surprise，尚未试 |
| `average_forecast_surprise_noshareout_qtr` | 0.8924 | 季度口径，未试 |
| `ebitda_rep_mean_surprise` | 0.5283 | 覆盖太低 |
| `mean_surprise_value_bvps_annual12` | 0.7683 | 未试 |

### 13.1 一条被数据否掉的假设（省下一批仿真）

原假设：「EPS 两条线的 SUB 缺口来自**数据覆盖不足**（只有 95% 有估计值 ⇒ 持仓集中在小票/大票）」。
**实测否证**：四条臂的多空持仓数完全同量级 —— R1 1542/1583、S1 1525/1600、D5 1563/1563、S2 1520/1605，
**已交付且 SUB 过闸的 `e76xgXkM` 是 1554/1572**（SUB 比值 0.556 对 R1 的 0.392）。
⇒ 持仓广度与 SUB 过闸**无关**；SUB 差异来自「收益在哪些科目/口径上更均匀」，是**内容问题**不是覆盖问题。
这条否证把「先补 coverage 再谈 SUB」整条支路删掉，也解释了为什么 `ts_backfill` 在这族从来不是 SUB 杠杆。

### 13.2 下一步的内容轴（等批次 9 的杠杆读数后择一组合）

1. **GAAP 口径 revision**：`reportednet_annual12_2` / `pretax_reported_annual12` 都有 3 月前快照
   ⇒ 可直接复用 R1 的壳与机制，只换科目。依据是定律 15（reported > adjusted，`eps_reported` 1.80 vs
   `eps` 0.95）与 `e76xgXkM`（reported 合并序列）是唯一 SUB 富余的已交付线。
2. **广覆盖 surprise**：`avg_surprise_net_income`（cov 0.923，对比 S1 的 0.70）——同机制换科目。
3. **不可做**：`epsreported` 无 prior（做不了 revision）；`ebitda_annual12` 无 prior。

## 14. 批次 9 读数：中性化域是唯一动过 SUB 的杠杆，但代价是换手塌到地板下

两个 multisim（A `Bu3Zg85M4KUc8m1eIudV8Id` / B `13ZdPAfb955s93NOArtVS0c`），10 臂全部 COMPLETE。
**映射已用 `regular.code` 逐条核过**（4 条关键臂，`KPmmRalz` / `9qEEQQg2` / `j2eeQQlZ` 已确认，其余按 RET/2Y 指纹归属）：

| 臂 | alpha | S | F | TO | RET | 2Y | SUB(闸) | SUB/S | 失败项 |
|---|---|---|---|---|---|---|---|---|---|
| A1 R1·grp=subind·hump.01·d20 | `KPmmRalz` | 1.56 | 0.94 | 4.57% | 4.51% | 1.87 | 0.50 (0.68) | 0.321 | S/F/SUB |
| A2 R1·grp=subind·hump.005·d20 | `omooeO7n` | 1.59 | 0.96 | 4.63% | 4.59% | 1.95 | 0.56 (0.69) | 0.352 | F/SUB |
| A3 S1·grp=subind·hump.01·d20 | `QPYYdXMK` | 1.53 | 1.06 | 4.32% | 5.96% | 1.68 | 0.51 (0.66) | 0.333 | S/SUB |
| A4 S1·grp=subind·hump.005·d20 | `VkddoJVA` | 1.52 | 1.05 | 4.32% | 5.97% | 1.69 | 0.51 (0.66) | 0.335 | S/SUB |
| A5 S1·grp=subind·w252·d20 | `GrggvJao` | 1.54 | 1.06 | 4.35% | 5.95% | 1.98 | 0.48 (0.67) | 0.312 | S/SUB |
| **B1 R1·neut=SUBIND·d20** | **`9qEEQQg2`** | **1.73** | **1.08** | **0.90%** | **4.83%** | **2.29** | **0.72 (0.75)** | **0.416** | **TO/SUB** |
| B2 S1·neut=SUBIND·d20 | `j2eeQQlZ` | 1.65 | 1.14 | 0.88% | 5.99% | 1.74 | 0.39 (0.71) | 0.236 | TO/SUB |
| B3 R1·neut=STAT | `1Yjj55VR` | 1.41 | 0.68 | 3.38% | 2.95% | 1.79 | 0.40 (0.61) | 0.284 | S/F/SUB |
| B4 S1·neut=STAT | `LL55xxqL` | 1.40 | 0.69 | 3.73% | 3.05% | 0.99 | 0.02 (0.61) | 0.014 | S/F/SUB/2Y |
| B5 R1·grp=subind·d30 | `WjLLmmnN` | 1.52 | 0.91 | 4.60% | 4.50% | 1.91 | 0.58 (0.66) | 0.382 | S/F/SUB |

**归因十四**：
1. **`group=subindustry` 是 SUB 负杠杆**：R1 从 industry 的 0.392 掉到 0.321，S 也从 1.71 → 1.56。
   原因与 SUB 的定义一致 —— 分组越细，权重越被剥掉行业/子行业内共同变动，小票池里剩下的独立信号越薄。
2. **`neutralization=SUBINDUSTRY` 是唯一真正改变 SUB 行为的旋钮**（R1 0.392 → 0.416，本族历史最好），
   但**代价是换手从 5.20% 塌到 0.90%**：子行业内去均值把大部分日间漂移抵掉了，组合几乎不再换手。
   ⇒ 这一臂的 SUB 读数（0.72）是在 0.9% 换手上算出来的，**样本效率低、且踩 LOW_TURNOVER 地板**，
   不能当作「机制在子票池有效」的干净证据。
3. **同域换机制会反向**：SUBINDUSTRY 对 R1 是加分（0.392→0.416），对 S1 是**减分**（0.321→0.236）。
   ⇒ 中性化域不是「越好越好的旋钮」，它与机制强交互，必须在同一机制上单独测（本批正是这样做）。
4. **`STATISTICAL` 是本族的毁灭域**：R1 1.73→1.41、S1 1.65→1.40，其中 S1 的 2Y 直接掉到 0.99。
   统计风险中性化会吃掉「修正/意外」这类横截面信息的慢成分。
5. **`decay=30` 无增益**（1.52/0.91 对 d20 的 1.56/0.94）⇒ 时间维度的平滑在本族已饱和。
6. **`9qEEQQg2` 的 `rns = 1.26`** 是本族最高（对比 R1 未中性化、S1、已交付四条的 0.8–1.1），
   说明「EPS 修正」的收益不是规模/行业风格 beta —— 这是把「机制有效性」与「闸门可达性」分开的两个问题，
   SUB 卡住不代表机制假。

**处置（按 §12.4 预注册）**：最好臂 `9qEEQQg2` 的 SUB/S = **0.416 < 0.43**，且同时踩 TO 地板 ⇒
「冻结壳 + 单一机制」在本集仍无 SUB 解。但 **0.416 距 0.43 只差 3.5%、且 TO 失败说明该读数本身不可信**，
故按 D0-P 给**最后一次结构尝试**（批次 10，已发）：只动「换手轴」（decay 20→10、去掉/减半 hump），
不动信号与中性化域；若任一臂 TO ≥ 1.0% 且 SUB ≥ 0.43×S，则进 prod 实测；否则 R1 与 S1 双双记
`USA-ANLST-FA-REVISION-SUB-DEADEND` / `USA-ANLST-FA-SURPRISE-SUB-DEADEND`，本集收官。

**批次 10 预注册表**（中性化固定 `SUBINDUSTRY`，壳其余冻结）：

| 臂 | 表达式差异 | decay | 判据 |
|---|---|---|---|
| A1 | R1 无 hump | 20 | S≥1.58 / F≥1.0 / **TO≥1.0%** / **SUB≥0.43×S** / 2Y≥1.6 |
| A2 | R1 hump=0.005 | 20 | 同上 |
| B1 | R1 hump=0.01 | 10 | 同上 |
| B2 | R1 hump=0.005 | 10 | 同上 |
| B3 | R1 无 hump | 10 | 同上 |

## 15. 批次 10 读数：hump 在本机制里是「阶跃检测器」不是平滑器 —— 这是本族最重要的机制发现

| 臂（中性化固定 SUBINDUSTRY） | alpha | S | F | TO | RET | 2Y | SUB(闸) | SUB/S | 失败项 |
|---|---|---|---|---|---|---|---|---|---|
| A1 R1·无 hump·d20 | `QPYYrev5` | 1.04 | 0.58 | 3.39% | 3.84% | 1.88 | 0.32 (0.45) | 0.308 | S/F/SUB |
| **A2 R1·hump.005·d20** | **`kqJJkRNO`** | **1.81** | **1.14** | **0.93%** | **5.00%** | **2.42** | **0.77 (0.78)** | **0.4255** | **TO/SUB** |
| B1 R1·hump.01·d10 | `YPxxwnmM` | 1.80 | 1.12 | 0.93% | 4.81% | 2.46 | 0.64 (0.78) | 0.356 | TO/SUB |
| B2 R1·hump.005·d10 | `E5VV0Ya1` | 1.79 | 1.11 | 0.96% | 4.84% | 2.47 | 0.70 (0.78) | 0.391 | TO/SUB |
| B3 R1·无 hump·d10 | `O0JJwqmp` | 1.04 | 0.57 | 4.09% | 3.79% | 1.84 | 0.34 (0.45) | 0.327 | S/F/SUB |

**归因十五**：
1. **去掉 `hump` 不是「放开换手」，是把信号换掉了**：TO 0.93% → 3.4~4.1%（+3.5×），但 S **1.81 → 1.04**、
   SUB 0.77 → 0.32。两条无 hump 臂（d20 / d10）逐位同形，不是噪声。
2. 机制解释：`ts_zscore(修正率, 252)` 的日间变化绝大部分来自 **252 日窗口滚动漂移**（微小、无信息），
   真正的信息只在**修正跳变日**。`hump(h)` 的死区把漂移挡在门外、只让超过 h 的跳变通过
   ⇒ 它是**高通/阶跃检测器**。去掉它就等于把「慢漂移」当成主信号，收益结构整个换掉。
   ⚠ 这与「hump = 压换手的平滑器」的通行理解相反，也与定律 9（快信号上 hump 会毁信号）合起来给出完整图景：
   **hump 只在「信息是跳变、噪声是漂移」的序列上是增益项，其余场合是破坏项。**
3. **decay 不动换手**（0.93% vs 0.93~0.96%）：换手由 hump 阈值决定，decay 只影响 SUB
   （d20 的 0.77 vs d10 的 0.70）⇒ 想抬换手只能动 hump 阈值或 z-score 窗口，这是批次 11 的唯一轴。
4. **最好臂 `kqJJkRNO` 已把两条线的差值压到极限**：TO 差 **0.07pp**（0.93% vs 1.0%）、
   SUB 差 **0.01**（0.77 vs 0.78），S/F/2Y 全绿且是全族新高（S1.81 / F1.14 / 2Y2.42）。
   这已经不是「机制不行」，是**参数在两个阈值之间只差一线**。

**批次 11 预注册**（单 multisim `4kdbCl3uz4GMc29p53nPrFP`，5 臂，设置全同：SUBINDUSTRY / d20）：

| 臂 | hump | ts_zscore 窗 | 目的 |
|---|---|---|---|
| H004_z252 | 0.004 | 252 | 死区略缩 → 期望 TO 抬过 1.0%，S 守住 1.58 |
| H003_z252 | 0.003 | 252 | 同上更激进 |
| H002_z252 | 0.002 | 252 | 边界探测（距「无 hump 悬崖」还有多远） |
| H003_z126 | 0.003 | 126 | 换第二条换手轴：缩短 z-score 窗（更快吸收跳变） |
| H002_z126 | 0.002 | 126 | 两轴叠加 |

判据：**TO ≥ 1.0% 且 S ≥ 1.58 且 F ≥ 1.0 且 SUB ≥ 0.43×S 且 2Y ≥ 1.6**。
若 0.004~0.002 全梯队都无法在 S ≥ 1.58 下把 TO 抬过 1.0%，则「EPS 修正 × 冻结壳」在本集记
`USA-ANLST-FA-REVISION-DEADEND`（换手地板与信号频率结构性冲突），R1 收官；S1 已在批次 9 记死。

---

## 16. 批次 11 读数：IS 四臂全过（本族首次），但 prod 三读全封 —— 「SUB↑ 与 prod↑ 同源」

multisim `4kdbCl3uz4GMc29p53nPrFP`，5 臂全部 R1 核 / SUBINDUSTRY / decay 20 / industry 分组。
读取方式：MCP `get_alpha_details`（映射用 `regular.code` 逐条核，`LL55qPoe` / `RRAAqJw0` 已确认）。

| 臂 | alpha | S | F | TO | RET | DD | 2Y | SUB(limit) | 比值 | rns | IS 判 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H004_z252 | `RRAAqJw0` | 1.85 | 1.20 | **1.00%** | 5.23% | 3.45% | 2.49 | 0.94(0.80) | 0.508 | 1.45 | **全过** |
| H003_z252 | `e766glZ6` | 1.69 | 1.12 | 1.10% | 5.45% | — | 2.04 | 0.99(0.73) | 0.586 | — | **全过** |
| H002_z252 | `2rjjQ1oY` | 1.50 | 0.99 | 1.41% | 5.42% | — | 1.76 | 0.75(0.65) | 0.500 | — | S/F |
| H003_z126 | `LL55qPoe` | 1.76 | 1.19 | 1.27% | 5.74% | 5.81% | 2.06 | 0.86(0.76) | 0.489 | **1.54** | **全过** |
| H002_z126 | `E5VVYZnK` | 1.62 | 1.10 | 1.84% | 5.80% | — | 1.93 | 0.79(0.70) | 0.488 | — | **全过** |

**这是本族 7 批 67 条里第一次有臂同时过 S / F / 2Y / TO / SUB 五条线，且一次四臂。**
壳的完整形态（批次 9+10+11 合并得出的结论）：`hump` 死区把换手压到 1% 量级而不毁信号（定律 21），
`neutralization=SUBINDUSTRY` 剥掉行业共同分量把 SUB 比值从 0.39 抬到 0.49–0.53，
两者叠加才让「低换手 + 高 SUB」同时成立。

### 16.1 prod 实测（`check_correlation(refresh=True)`，三条）

| alpha | max prod | `[0.7,0.8)` n | `[0.8,0.9)` n | 判 |
|---|---|---|---|---|
| `LL55qPoe` | **0.8463** | 4,776 | 132 | ≥0.75 ⇒ dead |
| `RRAAqJw0` | **0.7868** | 1,004 | 0 | ≥0.75 ⇒ dead |
| `e766glZ6` | **0.8459** | 4,283 | 88 | ≥0.75 ⇒ dead |
| `E5VVYZnK` | **0.8562** | 5,010 | 166 | ≥0.75 ⇒ dead |

**四条全闸臂全部实测**（最快的 `E5VVYZnK` TO 1.84% 也没有更低的 prod），读数 0.7868–0.8562，
`[0.7,0.8)` 桶 n 均 ≥1004 ⇒ 按 `wq-window-valley-break-prod-wall` 的规则（该 skill 属**用户级安装位**，不在本仓库 `Claude/skills/` 下，故不给相对链接——写相对链接会因路径不存在被 `test_docs_consistency` 判死链）
的族级判据（n=0 可救 / **n≥1 必死**），**窗口微调这条路不授权**。D0-P 直接判 `dead_end`。

### 16.2 归因十六：SUB 与 prod 是**同一个动作的两面**

批次 9 记的定律是「SUB 是内容问题，只有中性化域动得了它」；批次 11 补上了另一半：
**把 SUB 搬过线的那两个旋钮（`hump` 死区 + `SUBINDUSTRY` 中性化），同时把组合缩减到人群已经在交易的同一批事件上。**
证据链：SUB 比值 0.392（批次 8 冻结壳）→ 0.416（批次 9 只换中性化）→ 0.489–0.586（批次 11 两者叠加），
而 prod 从「本族未测」→ 0.7868–0.8463。低换手不是「更分散」，是**只在少数跳变日下注**，
这与平台现存修正类 alpha 的持仓高度重合 ⇒ 相关性必然随之升高。

⇒ **对本信号族，壳层旋钮买不到 SUB 而不付 prod。** 唯一出口是换机制（新信号 = 新 prod 指纹）。
EPS 3 月修正（R1）这条线记 `USA-ANLST-FA-REVISION-PROD-SEAL`（判死依据 = 上述三读），
不再在本机制上扩臂；S1（意外）已在批次 9 记死。

### 16.3 批次 12（已发）：冠军壳 × 新机制

保留批次 11 的壳（`hump` + `ts_zscore 252` + `SUBINDUSTRY` + `decay 20` + industry 分组），
只换核 —— 全部来自 §13 已登记、覆盖率 ≥0.92 且未试过的单序列：

| 臂 | 机制 | 核心字段 | hump |
|---|---|---|---|
| G1 | GAAP 净利润 3 月修正 | `mean_estimate_reportednet_annual12_2` / `..._three_months_prior_reportednet_annual12_2` | 0.003（+0.002 保险位） |
| G2 | GAAP 税前利润 3 月修正 | `mean_estimate_pretax_reported_annual12_2` / `..._three_months_prior_pretax_reported_annual12` | 0.003 |
| G3 | EBIT 3 月修正 | `mean_estimate_ebit_annual12_2` / `..._three_months_prior_ebit_annual12_2` | 0.003 |
| S3 | 净利润意外 PEAD（cov 0.923） | `avg_surprise_net_income`（`ts_mean(...,504)`） | 0.003 |

字段名已用 `preflight_expressions` 逐条核（7/7 recognized，只有 `std` 是已知误报）。
预注册判据同批次 11，另加 **prod < 0.70**（IS 全过之后才测，按 D0-P 处置）。

### 16.4 批次 13 候选字段名的机械核验（`preflight_expressions`，2026-10-21）

§13 的表只记了「有 prior」，没记**确切字段名**。逐条 preflight 后（`unknown_fields` 即不存在）：

| 科目 | 当期字段 | 3 月前快照 | 可用 |
|---|---|---|---|
| revenue | `mean_estimate_revenue_annual12` | `mean_estimate_three_months_prior_revenue_annual12` | ✅ |
| ebt | `mean_estimate_ebt_annual12` | `mean_estimate_three_months_prior_ebt_annual12` | ✅ |
| bvps | `mean_estimate_bvps_annual12` | `mean_estimate_three_months_prior_bvps_annual12` | ✅ |
| cfps | `mean_estimate_cfps_annual12` | `mean_estimate_three_months_prior_cfps_annual12` | ✅ |
| capex | `mean_estimate_capex_annual12_2` | **无**（`..._prior_capex_annual12_2` 不存在） | ❌ 做不了 revision |
| pretax（非 GAAP） | **无**（`mean_estimate_pretax_annual12` 不存在） | 有 `..._prior_pretax_annual12` | ❌ 缺分母 |
| pretax_reported（GAAP） | `mean_estimate_pretax_reported_annual12_2` | `..._prior_pretax_reported_annual12` | ✅（批次 12 G2） |
| reportednet（GAAP） | `mean_estimate_reportednet_annual12_2` | `..._prior_reportednet_annual12_2` | ✅（批次 12 G1） |
| ebit | `mean_estimate_ebit_annual12_2` | `..._prior_ebit_annual12_2` | ✅（批次 12 G3） |
| surprise | `average_forecast_surprise_noshareout_qtr` / `mean_surprise_value_bvps_annual12` / `avg_surprise_net_income(_fxadj)` | — | ✅（未试） |

⇒ **批次 13 的可用 revision 菜单**：revenue / ebt / bvps / cfps 四科目（外加批次 12 的 GAAP 三科目）。
`capex` 与 `pretax` 两条按上表排除，不再试错。

---

## 17. 批次 12–13 读数：壳层不是机制中性的；D2 分歧是唯一 SUB/2Y/TO 全过的机制（2026-10-21）

### 17.1 批次 12（冠军壳 × 新核，A `25nKMIblu4MUadALodsZKto` / B `lq7bPgC54G8cqs1gJYIEdyB`）

全部 SUBINDUSTRY / decay 20 / industry / hump 0.003（G1 另有 0.002）。

| 臂 | 机制 | alpha | S | F | TO | RET | 2Y | SUB（限） | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|
| G1 | GAAP 净利 3 月修正 h0.003 | `KPmmqpeg` | 0.84 | 0.40 | 1.15% | 2.89% | 1.62 | −0.03（0.36） | S F SUB |
| G1b | 同上 h0.002 | `MP00qnwn` | 1.02 | 0.54 | 1.49% | 3.45% | 1.90 | 0.20（0.44） | S F SUB |
| G2 | GAAP 税前 3 月修正 | `npAAYlwx` | 0.81 | 0.37 | 1.15% | 2.64% | 1.50 | 0.13（0.35） | S F SUB 2Y |
| G3 | EBIT 3 月修正 | `wp99OA32` | 1.14 | 0.59 | 1.14% | 3.37% | 2.30 | 0.63（0.49） | S F |
| S3 | 净利意外 PEAD | `E5VVYM81` | 1.24 | 0.66 | 0.88% | 3.49% | 1.38 | 0.52（0.54） | S F TO SUB 2Y |

**归因十七：冠军壳不是机制中性的。** 同一套壳（hump 0.004 / SUBINDUSTRY / industry / z252）在 R1
EPS 修正上给出 S1.85，在 GAAP/EBIT 修正上只有 0.81–1.14。壳能买 SUB（EBIT 比值 0.55 过线）却买不到 S：
hump 死区 + SUBINDUSTRY 中性化把平滑的会计科目修正里的截面离散度削掉了。**只有"跳变型"的核**
（EPS 修正、分歧变化、意外）带得动 S；G1/G2/G3 这类"平滑漂移"核在裸壳（RM + h0.01）下也从未超过 1.1
（批次 8 R2 营收修正 0.85），属**核自身强度不足**，不是壳的问题 ⇒ GAAP 三科目修正记 `dead_end`。

### 17.2 批次 13（D2/D3/S1 × 冠军壳，A `N48ukdxi59P8Da1dGkMjCpS` / B `40a85f8S653o9dgIUh0XCTQ`）

全部 SUBINDUSTRY / decay 20 / industry / z252，hump 见下表；5 臂全为 `UNITS` WARNING（分母 epsilon 无量纲），不影响读数。

| 臂 | alpha | S | F | TO | RET | 2Y | SUB（限） | 比值 | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|
| E1 D2 h0.003 | `wp991z21` | 1.41 | 0.91 | 1.14% | 5.19% | 1.85 | 0.72（0.61） | 0.51 | S F |
| **E2 D2 h0.004** | `1YjjLmlK` | **1.47** | **0.89** | **1.00%** | 4.63% | **2.03** | **0.78（0.63）** | **0.53** | **S F** |
| E3 D2 反号 h0.003 | `WjLLdXzd` | 1.28 | 0.67 | 1.26% | 3.45% | 0.90 | 0.51（0.55） | 0.40 | S F SUB 2Y |
| E4 S1 意外 h0.003 | `j2eeXlqk` | **1.67** | **1.16** | 0.90% | 6.04% | 1.61 | 0.35（0.72） | 0.21 | TO SUB |
| E5 D3 营收分歧 h0.003 | `d5KKmg2w` | 1.00 | 0.56 | 1.20% | 3.91% | 1.63 | 0.44（0.43） | 0.44 | S F |

**归因十八：本集的机制分工已经清楚 —— D2 管 SUB/2Y/TO，S1 管 S/F，两者不可兼得。**

1. **D2 是唯一 SUB/2Y/TO 三条全过的机制**（比值 0.51–0.53，线为 0.43），只缺 S（−0.11）与 F（−0.11）。
   反号臂全面崩（S1.28 / 2Y0.90）⇒ **分歧上升 → 正 rank 的方向确认**，§12.2 第 3 条留的"反向假设"关闭。
2. **E4（S1 意外）S/F 过、SUB 只有 0.21** —— 意外是"慢变量 + 长窗"（`ts_mean(...,504)`），
   信号集中在中小盘，子宇宙 Sharpe 结构性低位；TO 0.90% 也贴地板。**S/F 与 SUB 在本集是两条反向轴，
   同一个核无法同时满足** ⇒ 「S1 × 冠军壳」记 `dead_end`。
3. **营收口径在冠军壳下崩盘**：D3 同壳同窗从批次 8 的 S1.53 掉到 1.00。分歧机制对口径敏感，
   营收分歧的截面结构被 SUBINDUSTRY 中性化吃掉 ⇒ 营收分歧不再扩臂。
4. **壳层拆解（把批次 8 的 `3qjjLjpP` 调出来逐字对照才看清）**：批次 8 D2 = **RM 中性化 + hump 0.01**，
   TO 5.14% / S1.56 / 2Y1.51 / SUB0.63（比值 0.404）；批次 13 = **SUBINDUSTRY + hump 0.004**，
   TO 1.00% / S1.47 / 2Y2.03 / SUB0.78（比值 0.53）。**TO 的 5 倍差来自中性化、不是 hump**；
   SUBINDUSTRY 相对 RM 用 −0.09 S 换来 +0.52 2Y 与 +0.13 比值 ⇒ **中性化档是 D2 的正确杠杆**。
5. **⚠ 新的硬边界：hump 抬到 0.004 时 TO 恰好 1.00%（地板 1.0%）**。E1(h0.003) TO 1.14% → E2(h0.004) 1.00%，
   斜率约 −14bp/0.001 ⇒ **h0.005 必触 LOW_TURNOVER**。**D2 的 S 不能靠抬 hump 拿**，
   这是本批最重要的一条操作约束（此前在修正族上 hump 是提 S 的主杠杆，方向到 D2 就反了）。

### 17.3 批次 14 设计（已发）：D2 × 五个不压换手的杠杆

预注册判据：S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / TO ≥ 1.0% / SUB ≥ 0.43×S；全过后才测 prod（D0-P）。

| 臂 | 杠杆 | 依据 |
|---|---|---|
| F1 | `ts_zscore` 窗 252 → **126** | 快窗提 TO 余量，可能提 S；D2 是 3 月变化，快 z 不破坏机制 |
| F2 | `ts_zscore` 窗 252 → **504** | 慢基线更稳，分批 8→13 的 2Y 改善方向 |
| F3 | **decay 20 → 40** | 已在案：decay 不动 TO（Law 21），只平滑持仓 |
| F4 | **中性化 SUBINDUSTRY → INDUSTRY** | 落 RM(2Y1.51) 与 SUBIND(2Y2.03) 之间，找 S/2Y 交点 |
| F5 | **decay 20 → 60** | F3 的加倍点，看 decay 是否单调 |

A 组 = F1/F2/F3，B 组 = F4/F5。若 F1–F5 无一过 S ≥ 1.58，则 D2 在本集记 `S 墙`：
五条壳层杠杆全穷尽后仍差 ≥ 0.05，按 §11.5 的同一条判据不再扩臂，转核（新数据集）。

### 17.4 批次 14 读数（2026-10-21，A `mcxsB3Um4ZDbuLXAhVUIqM` / B `20V8BRgHL4r18AHNOOXzN8i`）

| 臂 | 杠杆 | alpha | S | F | TO | RET | 2Y | SUB（限） | 比值 | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|---|
| **F1** | **z126** | `mLYYAlMW` | **1.53** | **0.95** | **1.03%** | 4.84% | **2.08** | 0.79（0.66） | 0.516 | S F |
| F2 | z504 | `9qEEK201` | 1.41 | 0.86 | 0.99% | 4.63% | 1.89 | 0.78（0.61） | 0.553 | S F TO |
| F3 | decay 40 | `e766KWRO` | 1.52 | 0.95 | 0.96% | 4.86% | 2.08 | 0.79（0.65） | 0.520 | S F TO |
| F4 | INDUSTRY 中性化 | `0mjjd1kr` | 1.36 | 0.86 | 0.93% | 4.98% | 1.67 | 0.73（0.58） | 0.537 | S F TO |
| F5 | decay 60 | `bl88Me2m` | 1.48 | 0.93 | 0.95% | 4.95% | 1.97 | 0.84（0.64） | 0.568 | S F TO |

**归因十九：三条壳层事实（两条推翻旧律）。**

1. **`ts_zscore` 窗 252 → 126 是本族唯一"双正向"杠杆**：S +0.06（1.47→1.53）**且** TO +0.03pp（1.00→1.03%），
   2Y 2.03→2.08，F 0.89→0.95。窗 504 两头都变差（S1.41 / TO 破线）⇒ **z 窗在 D2 上是单调的，越快越好**，
   与修正族"长窗更稳"的经验相反（D2 是 3 月变化率，快窗才是同频）。
2. **⚠ 更正 Law 21 的第二半句**：原记「decay 不动换手」。在 D2 上 **decay 40/60 把 TO 从 1.00% 压到 0.96%/0.95%，
   直接破 1.0% 地板**（decay 30 的估计值也贴线）。修正口径：**decay 对 TO 的影响随核的持续性而定**——
   跳变型核（修正）上 decay 不动 TO，慢变型核（分歧 3 月）上 decay 会压低 TO。D2 的 decay 通道因此关闭。
3. **中性化 INDUSTRY 在 D2 上单向变差**（S 1.47→1.36、2Y 2.03→1.67、TO 破线）：D2 的有效截面是
   subindustry 内部，放宽到 industry 后截面噪声进场。⇒ **SUBINDUSTRY 是 D2 的唯一起点**，
   批次 15 不再测中性化档位（原 I1–I5 梯子作废）。

⇒ 批次 15 改为「z126 基座 × 提覆盖/提信号」：backfill 504 / backfill 756（交付冠军 `e76xgXkM` 用 756 的实证）、
z63、group=subindustry、group=market。

### 17.5 批次 15 读数：z126 基座 × 覆盖/分组，第一条 IS 全过（2026-10-21，A `2ub3Nq70y4Tnao1196isnqQe` / B `4npAzccAz5dZbCu12yrQFfEs`）

| 臂 | 杠杆 | alpha | S | F | TO | RET | 2Y | SUB（限） | 比值 | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|---|
| J1 | backfill 504 | `88vv6VMl` | 1.50 | 0.93 | 1.03% | 4.77% | 2.08 | 0.74（0.65） | 0.493 | S F |
| J2 | backfill 756 | `2rjjZX18` | 1.50 | 0.93 | 1.03% | 4.77% | 2.13 | 0.75（0.65） | 0.500 | S F |
| J3 | **z63** | `vROOzpKa` | **1.58** | 0.96 | **1.15%** | 4.63% | 1.72 | **0.89（0.68）** | **0.563** | **仅 F** |
| J4 | group=subindustry | `mLYYz5L5` | 1.37 | 0.77 | 0.97% | 3.96% | 1.88 | 0.69（0.59） | 0.504 | S F TO |
| **J5** | **group=market** | **`E5VVaG5P`** | **1.60** | **1.03** | **1.01%** | **5.16%** | **2.13** | **0.82（0.69）** | **0.512** | **无** |

**归因二十：三条事实。**

1. **`group=market` 是本族第二个"双正向"杠杆**：同 z126 基座下 group industry→market，
   S 1.53→1.60（+0.07）、F 0.95→1.03（+0.08）、RET 4.84→5.16%（+0.32pp）、2Y 2.08→2.13、TO 1.03→1.01%，
   **九道 RA 检查零失败、`failed_ra_count: 0`** —— 8 批 / 75 条里的第一条 IS 全过。
   机制解释：D2 度量的是「分析师分歧相对 3 月前的变化」，这个量在**全市场截面**上才有可比性；
   压在 industry 内（每行业 ~30 只）时组内样本太少、rank 粒度粗，噪声吃掉 0.07 S。
   这与 J4（压到 subindustry，S 1.37 / TO 破线）同向且更极端 —— **分组粒度越粗越好，直到 market**。
2. **z63 是第三条正向杠杆但代价明确**：S 1.58 刚好擦线、SUB 比值 0.563（全族最高）、TO 1.15%（离地板最远），
   但 2Y 从 2.08 掉到 1.72、F 0.96 差 0.04。z63 与 group=market **尚未交叉**（J3 是 z63+industry）。
3. **backfill 504/756 完全无效**（J1/J2 与 F1 逐位相同：S1.50/TO1.03%/RET4.77%）：
   D2 的覆盖缺口不在时间维（`ts_backfill` 已在壳内 252 天），加长无新数据。该通道关闭。

### 17.6 `E5VVaG5P` 的 prod 实测：0.8312，IS 全过也判死（2026-10-21）

`check_correlation(refresh=True)` → production `max_correlation = 0.8312`、`passes_check: false`；
直方图 `[0.7,0.8)` n=**3930**、`[0.8,0.9)` n=**44**。按 `wq-window-valley-break-prod-wall`
（n ≥ 1 ⇒ 族级必死，窗口微调不授权）与 D0-P（prod ≥ 0.75 ⇒ dead_end），`E5VVaG5P` 记 `dead_end`。

**归因二十一（本族 prod 墙的结构性来源 —— 与交付表的对照）**：

| 集合 | 中性化 |
|---|---|
| 已交付 5 颗 ACTIVE（`omoK1A5m`/`akVnvzX5`/`gJWoaJqv`/`kqJLawqP`/`e76xgXkM`） | REVERSION_AND_MOMENTUM（3）、CROWDING（1）、STATISTICAL（1）… **零 SUBINDUSTRY** |
| 本会话全部 prod 卡墙臂（0.79–0.86，含 `E5VVaG5P` 0.8312） | **全部 SUBINDUSTRY** |

Law 22 已证「hump deadband + SUBINDUSTRY 同时抬 SUB 与 prod」；这里得到它的区域级版本：
**SUBINDUSTRY 把 alpha 压进 subindustry 内的相对定价，而平台存量 alpha 池在同一个空间里最拥挤**。
交付表里 5 颗 ACTIVE 用的是 RM / CROWDING —— 那是**把风格与拥挤度先扣掉**的中性化，留下的残差更独特。

⇒ 批次 16 的唯一授权结构尝试：**冻结 J5 的表达式（z126 + group=market，IS 九闸零失败），
只换中性化档**到 RM / CROWDING / STATISTICAL / SLOW，并带上 J3 的 z63 几何作第二条身份。
预登记：`S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / TO ≥ 1.0% / SUB ≥ 0.43×S`；**全过后才测 prod**（D0-P）。

### 17.7 交付表反查：prod 友好的壳层族长什么样（2026-10-21）

对已交付两颗 ACTIVE 拉 `get_alpha_details`，与本会话的卡墙壳逐项对照：

| alpha | 壳层 | 中性化 / decay | TO | RET | prod |
|---|---|---|---|---|---|
| `gJWoaJqv`（ACTIVE 0.6978） | `group_rank(hump(`**`ts_delta(ts_av_diff(核, 504), 252)`**`, 0.01), market)` | RM / 20 | **10.14%** | 6.71% | **0.6978** |
| `kqJLawqP`（ACTIVE 0.6757） | `group_rank(hump(`**`ts_av_diff(核, 756)`**`, 0.01), market)` | CROWDING / 10 | **9.61%** | 5.98% | **0.6757** |
| 本会话全部卡墙臂 | `group_rank(hump(ts_backfill(winsorize(ts_zscore(核, 126)), std=4), 252), 0.004), market)` | **SUBINDUSTRY** / 20 | **1.01%** | 5.16% | **0.8312** |

四处系统性差异，**同一方向上叠加**：

1. **归一化算子**：交付用 `ts_av_diff`（相对 504/756 日均值的偏离，分子是原始差值）；
   我用 `ts_zscore`（除以滚动标准差）。前者对**分母爆炸免疫**（分歧/修正类核心的分母是「3 月前快照」，
   本身就可能接近零），后者在核心近零时段产出巨值 —— 这正是全批 `UNITS` 警告与极端值同源的地方，
   也是 `winsorize(std=4)` 被反复需要的原因。**`ts_av_diff` 是这族核心更合适的归一化**（USA override 早有此条，
   但在 D2 上从未实测）。
2. **hump 档**：交付 0.01，我用 0.004。hump 0.004 是为把 TO 拉过 1.0% 地板而压的，属于**为过闸反向优化**。
3. **换手量级**：交付 9.6–10.1%，我 1.0%。十倍差来自 `ts_zscore` 的慢变 vs `ts_av_diff` 的滚动均值漂移；
   而 prod 墙恰在**换手高的那一侧**不存在 —— 说明「快照相近」不是 prod 的来源，**归一化方式**才是。
4. **中性化**：交付 RM / CROWDING，我 SUBINDUSTRY（见 §17.6 归因二十一）。

⇒ **批次 17 预登记**（批次 16 跑完后发，账户只有 2 槽）：核不动，换成交付壳层族，2×2×2：
核 ∈ {D2 分歧变化, R1 修正} × 壳 ∈ {`ts_av_diff(·,504)`, `ts_delta(ts_av_diff(·,504),252)`} × 中性化 ∈ {RM/20, CROWDING/10}，
另加 D2×`ts_av_diff(·,756)`×CROWDING 一条。hump 一律 0.01、group 一律 market。
闸线同前：`S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / TO ≥ 1.0% / SUB ≥ 0.43×S`；**全过后才测 prod**。
R1 值得同批的理由：它原读数 S 1.71 / F 1.15 / 2Y 1.66 / TO 5.20% 只差 SUB 0.07（比值 0.392 vs 0.43），
是**全族离全闸最近的一条**，且它的壳从未在 `ts_av_diff` 下测过。

### 17.8 批次 16 读数：换中性化被证伪 —— SUBINDUSTRY 是 D2 的承重墙，不是 prod 负债（2026-10-21）

冻结 `E5VVaG5P` 的表达式（z126 + group=market），只换中性化/decay，8 臂
（A `AMMyz8LA4uN9YF5atAtA8X` / B `4h9qPS5VD4O88Gr18R9j8ah7`）：

| 臂 | 中性化 / decay | alpha | S | F | TO | RET | 2Y | SUB（限） | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|
| K1 | RM / 20 | `vROOJA3r` | 1.41 | 0.94 | 5.67% | 5.55% | **1.28** | 0.70（0.61） | S F 2Y |
| K2 | CROWDING / 20 | `JjPP58KE` | 1.43 | 1.02 | 1.11% | 6.32% | **1.44** | **0.84（0.62）** | S 2Y |
| K3 | STATISTICAL / 20 | `kqJJLalk` | 1.12 | 0.50 | 3.83% | 2.52% | 1.40 | 0.27（0.48） | S F SUB 2Y |
| K4 | SLOW / 20 | `akVVWavO` | 1.22 | 0.56 | 4.23% | 2.63% | 1.18 | 0.36（0.53） | S F SUB 2Y |
| K5 | RM / 1 | `YPxxWa7W` | 1.46 | 0.98 | 5.71% | 5.66% | 1.34 | 0.71（0.63） | S F 2Y |
| **K6** | **CROWDING / 10** | `A1QQOxle` | **1.46** | **1.05** | 1.12% | **6.44%** | **1.49** | **0.86（0.63）** | **S 2Y** |
| K7 | RM / 20 + z63 | `QPYY507w` | 1.46 | 0.94 | 5.62% | 5.16% | 1.22 | 0.74（0.63） | S F 2Y |
| K8 | CROWDING / 20 + z63 | `leMMRa87` | 1.50 | 1.03 | 1.16% | 5.94% | 1.41 | **0.91（0.65）** | S 2Y |

**对照基准**：同表达式在 SUBINDUSTRY/20 下 = S 1.60 / F 1.03 / TO 1.01% / RET 5.16% / **2Y 2.13** / SUB 0.82（E5VVaG5P）。

**归因二十二：§17.6 的「SUBINDUSTRY 是 prod 负债」在 IS 层被证伪。**

1. **八臂全部 2Y 崩塌**：2.13 → 1.18–1.49，**没有一臂守住 1.58**。S 也从 1.60 掉到 1.12–1.50。
   ⇒ **SUBINDUSTRY 不是可替换的中性化偏好，它是这个信号的承重结构**：D2 度量的分歧变化
   只在 subindustry 内的相对定价上有稳定 2Y；一旦放开到 RM/CROWDING/STATISTICAL/SLOW 的截面，
   2022–2023 段的收益就被扣掉。§17.6 的归因二十一（"交付用 RM/CROWDING ⇒ 我们也该用"）
   **只对交付族成立、对 D2 不成立** —— 记录为反例，防止后续再按"中性化对齐交付"推理。
2. **但 CROWDING 在其它四项上全面更优**：SUB 比值 **1.31–1.40**（全族最高，交付两颗也只有 0.49/0.50）、
   RET 5.94–6.44%（vs 5.16%）、F 1.02–1.05、TO 1.11–1.16%。它**只差 S 0.12 和 2Y 0.09–0.14**。
   ⇒ 「CROWDING + 更高的 S/2Y」是唯一还没试过的组合方向，而 S/2Y 的来源只能靠**换壳**（批次 17）。
3. **RM 的 TO 从 1.01% 跳到 5.67%**（5.6 倍），2Y 却仍只有 1.28–1.34：RM 把持仓打散了但没换到持续性。
   STATISTICAL/SLOW 直接判死（S 1.12/1.22、SUB 0.27/0.36、RET 2.5%）。
4. **decay 1 vs 20 在 RM 上几乎无差**（1.41/1.28 vs 1.46/1.34），在 CROWDING 上亦然（1.43/1.44 vs 1.46/1.49）：
   **decay 不是这族的杠杆**（第三次确认，前两次见 Law 21 与 §17.4 第 2 条）。

⇒ 批次 17 按 §17.7 已发：换成交付壳层族（`ts_av_diff` / `ts_delta(ts_av_diff)`）承载 S 与 2Y，
中性化保留 RM 与 CROWDING 两档，8 臂（D2 四条 + R1 四条）。

### 17.9 批次 17 读数：交付壳层族把 IS 打通（两条全过），但 prod 同为 0.83 ⇒ D2 族判死（2026-10-21）

A `ysL8SbJW4BP9VX18gy0NjgN` / B `2Eu7QReGF4mQbMW179aE20Fs`，8 臂，hump 0.01 / group market：

| 臂 | 核 × 壳 × 中性化 | alpha | S | F | TO | RET | 2Y | SUB（限） | 缺闸 |
|---|---|---|---|---|---|---|---|---|---|
| L1 | D2 · avdiff504 · RM/20 | `3qjjEVRz` | 1.66 | 1.13 | 5.56% | 5.78% | 1.94 | 0.65（0.72） | SUB |
| **L2** | **D2 · avdiff504 · CROWD/10** | **`2rjjvmLY`** | **1.64** | **1.17** | 1.07% | 6.34% | **2.11** | **0.75（0.71）** | **无** |
| L3 | D2 · delta(avdiff504,252) · RM/20 | `1YjjoZzm` | 1.53 | 1.16 | 6.00% | **7.14%** | 1.47 | 0.74（0.66） | S 2Y |
| **L4** | **D2 · avdiff756 · CROWD/10** | **`MP00b3Lr`** | **1.71** | **1.26** | 1.08% | **6.81%** | **2.20** | **0.74（0.74）** | **无** |
| L5 | R1 · avdiff504 · RM/20 | `LL55nMMv` | 1.69 | 1.14 | 5.52% | 5.72% | 1.62 | 0.51（0.73） | SUB |
| L6 | R1 · delta(avdiff504,252) · RM/20 | `WjLLNOld` | 1.49 | 1.06 | 5.76% | 6.32% | 1.38 | 0.58（0.65） | S SUB 2Y |
| L7 | R1 · avdiff504 · CROWD/10 | `akVVNKaR` | 1.60 | 1.10 | 1.14% | 5.96% | 1.53 | 0.50（0.69） | SUB 2Y |
| L8 | R1 · delta(avdiff504,252) · CROWD/10 | `ZYmmjQX3` | 1.41 | 1.06 | 1.13% | 7.13% | 1.27 | 0.68（0.61） | S 2Y |

**归因二十三：壳层假设成立（S/2Y 被 `ts_av_diff` 打通），但核的 prod 是死的。**

1. **`ts_av_diff` 确实是 S/2Y 的载体**：同一 CROWDING 档，zscore 壳 2Y 1.44 / S 1.43
   → avdiff504 壳 **2Y 2.11 / S 1.64** → avdiff756 壳 **2Y 2.20 / S 1.71**。
   这是本会话第一次在不换核的情况下把 2Y 抬过 1.58 并保住 SUB（0.75/0.71、0.74/0.74）。
   窗口越长越好（504→756：S +0.07 / 2Y +0.09 / RET +0.47pp），与 §17.4「z 窗越快越好」相反 ——
   **两个壳走的是不同方向**：zscore 是「短期内相对自身波动」，avdiff 是「相对两年均值的水平偏移」。
2. **R1 在交付壳下被 SUB 判死**（0.51/0.50，比值 0.30/0.31）：修正族的 sub-universe 脆弱性是核属性，
   壳换不动它。R1 族的 SUB 通道彻底关闭。
3. **prod 三连 0.83**：`E5VVaG5P`（zscore/SUBIND）0.8312、`2rjjvmLY`（avdiff504/CROWD）**0.8359**、
   `MP00b3Lr`（avdiff756/CROWD）**0.8379**。三条表达式互不相同、中性化不同、壳不同、TO 差 5–10 倍，
   prod 却锁在 0.83±0.004 ⇒ **相关的是 «分析师 EPS 分歧变化» 这个核本身，不是任何一种实现**。
   直方图 `[0.7,0.8)` n=3463/2882、`[0.8,0.9)` n=36/29，按 `wq-window-valley-break-prod-wall`
   **n ≥ 1 ⇒ 族级必死、窗口微调不授权**；按 D0-P（prod ≥ 0.75）⇒ **D2 分歧族判 `dead_end`**。

### 17.10 本数据集机制穷尽表（2026-10-21 结项）

| 机制 | 代表臂 | 最好读数 | 裁决 |
|---|---|---|---|
| 实际值叠加（`mean_forecast_actual_combined_*`） | `e76xgXkM` | S/F/2Y/SUB 全过，prod 0.5532 | **交付 ACTIVE** |
| 分歧变化（`stddev_estimate_*`） | `MP00b3Lr` / `2rjjvmLY` | S 1.71 / F 1.26 / 2Y 2.20 / SUB 擦线 | **IS 全过、prod 0.83 ⇒ dead_end** |
| 修正（`mean_estimate_*` 3 月比） | `LL55nMMv` | S 1.69 / F 1.14 / 2Y 1.62 | SUB 0.51（比 0.30）⇒ dead_end |
| 覆盖（`estimate_count_*`） | `P0MM9xPJ` / `pwvvOxWo` | S 0.53 / 0.57 | dead_end |
| 意外（`mean_surprise_value_*`） | `omooORP6` | S 1.62 / F 1.21 / RET 6.93% | SUB 比 0.21 ⇒ dead_end |
| 分歧水平 CV（D5） | `LL55J579` | S 1.46 / 2Y 1.77 | S/F/SUB 三缺 ⇒ dead_end |

⇒ 本数据集（`analyst_consensus` fa overlay，3424 字段）**在不混信号、不换 region 的前提下机制已穷尽**，
唯一的正向产出是既有交付 `e76xgXkM`。**下一步按目标约束第 2 条换数据集**（理由：五个机制全部有明确死因，
且最后两条 IS 全过的身份被同一个 prod 0.83 结构锁死，继续在本集扩臂只会重复同一张曲面）。
