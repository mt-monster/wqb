# shortinterest3（USA / TOP3000 / D1）十模板库

> **为什么有这份文档**：用户硬约束 —— 「使用模板时一定要保持模板多样性和数量（10 个模板），
> 可以查平台论坛和 ideas 和外部金融论文去补充」。
> 模板单一会把「骨架选错」误判成「字段没信号」，饱和数据集尤其致命。
> 本文件是波 144/145 的**可审计模板清单**：每个模板标注结构、经济机制、来源，收批后按模板归因。
>
> 塔位：`pyramid_short = shortinterest`（USA D1 本轮 **0/3 未点亮**），单塔 ⇒ ATOM 路径可用。
>
> 更新日期：2026-10-28

---

## 1. 字段族群（31 字段，全部 VECTOR ⇒ 必须 `vec_*` 聚合）

| 族群 | 字段 | 经济含义 |
|---|---|---|
| **费率族** | `mean_loan_rate` / `mean_loan_rate_main` / `max_loan_rate(_main)` / `min_loan_rate(_main)` / `loan_rate_volatility(_main)` | 做空成本；`_main` 一般指主交易所合并口径 |
| **数量族** | `available_share_count` / `loaned_share_count(_main/_r2/_r2_d1)` / `new_loaned_share_count(_d1)` / `loan_utilization_ratio(_d1)` / `available_market_value_usd` / `loaned_market_value_usd(_main)` | 券源供给与占用 |
| **评分族** | `shrt3_bar`（借券需求 1–10，userCount 604 / alphaCount 2028，最热）/ `shrt3_utilizationpercent_units` / `borrow_activity_score` | 厂商加工的需求/占用评分 |
| **辅助** | `average_loan_duration_days(_main)` / `transaction_count(_main)` / `rate_bin_lower_limit(_d1)` / `rate_bin_upper_limit(_d1)` | 合约期限、签约笔数、分箱边界（分组轴候选） |

### 合法 `vec_*` 聚合算子（平台实测，**只有 7 个**）
`vec_avg` / `vec_sum` / `vec_count` / `vec_max` / `vec_min` / `vec_range` / `vec_stddev`

> ⚠ **`vec_std` 不存在**（写它会报 `unknown_fields`，因为它不在算子表里）。正确名是 `vec_stddev`。
> `vec_range` = 合约间极差，可直接当离散度用。

---

## 2. 模板库（13 个，结构互异）

差异维度必须落在 **骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性变换** 上——只换窗口或换常数**不算**新模板。

| # | 编号 | 结构 | 经济机制 | 来源 | 状态 |
|---|---|---|---|---|---|
| 1 | **M1** | `reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main),vec_avg(mean_loan_rate_main),22), industry))` | 借券费率**风险溢价**：费率不确定性高的票未来跑输 | 论坛帖 A `43624312881943`（JX84394）迁移到 USA/industry | ✅ **S +1.81 / F +1.50 / 2Y +3.52 / eff 0.829** |
| 2 | **M1X** | 同 M1 但轴换 `exchange` | 制度边界分组（帖 A 原版轴） | 论坛帖 A 原版 | 未测（USA） |
| 3 | **M2** | `group_rank(winsorize(ts_av_diff(ts_backfill(vec_avg(loan_utilization_ratio),120),60), std=4), industry)` | **可借券异常收紧 → 接盘反转**（赚提供流动性的报酬，非逼空） | 论坛帖 B `43179452121495`（LJ34087），USA 实测 S +2.28（ILLIQUID_MINVOL1M） | 在飞 |
| 4 | **M3** | `group_zscore(vec_stddev(mean_loan_rate_main), industry)` | **自算合约间分歧 vs 厂商打包**：验证 `loan_rate_volatility_main` 是否只是它的别名 | 自建 | 在飞 |
| 5 | **M4** | `group_zscore(ts_mean(divide(vec_sum(loaned_share_count), vec_sum(available_share_count)),22), industry)` | 借券利用率 = 卖空需求 ÷ 可借供给（**同单位相除**，不需 ε） | 自建 | 在飞 |
| 6 | **M5** | `group_zscore(ts_rank(vec_avg(mean_loan_rate_main),252), industry)` | 费率相对自身一年分位 → 结构性极值（抓「贵到离谱」而非「贵了」） | 自建 | 在飞 |
| 7 | **M10** | `ts_decay_linear(<M1R>, 22)` | **平滑记忆杠杆**：降噪、延长信号有效期 | 自建（GBR 实证：该层是单次收益最大杠杆 S+0.21/F+0.26/2Y+0.62/TO−0.07） | 在飞 |
| 8 | **M6** | `group_zscore(divide(ts_delta(vec_avg(loan_utilization_ratio),22), ts_mean(vec_avg(loan_utilization_ratio),252)), industry)` | 利用率相对自身常态的**变化率**（同单位归一，非 ε 防零） | 自建 | 待发 |
| 9 | **M7** | `group_zscore(multiply(vec_avg(shrt3_bar), vec_avg(mean_loan_rate_main)), sector)` | **需求强度 × 成本**交互：强需求撞上高成本 = 逼空压力最紧；换 `sector` 轴 | 自建 | 待发 |
| 10 | **M8** | `group_zscore(ts_max(vec_avg(max_loan_rate_main),66), industry)` | **尾部极端合约**费率（`ts_max` 抓拥挤极点） | 自建 | 待发 |
| 11 | **M9** | `group_zscore(divide(vec_sum(available_share_count), ts_mean(vec_sum(available_share_count),252)), industry)` | **券源枯竭**：可借存量相对一年均值的衰减（供给侧独立于费率） | 自建 | 待发 |
| 12 | **M11** | `group_zscore(vec_range(mean_loan_rate_main), industry)` | 合约间费率**极差**（比 stddev 更抗中间合约噪声） | 自建 | 待发 |
| 13 | **M12** | `group_zscore(ts_av_diff(vec_sum(transaction_count_main),60), industry)` | **签约活动激增**：新借券合约签订量异常（事件型，非价格非存量） | 自建 | 待发（429 撞槽） |

### 矩矩阵探针（波 144，已收批 —— 用于定位「哪个字段的哪个矩有信号」）
这 6 条本身是同一模板族的**矩 × 字段**二维扫，不是 6 个独立模板，故不重复计入模板库。

| 探针 | 字段 | 矩 | 翻转后 S | F | TO | 2Y | eff | inv_ratio |
|---|---|---|---|---|---|---|---|---|
| T1 | `mean_loan_rate_main` | 二阶方差 | **+1.81** | +1.50 | 16.1% | **+3.52** | **0.829** | 0.81 |
| T5 | `loan_rate_volatility_main` | 厂商离散度 | +1.40 | +0.49 | 57.0% | +2.17 | 0.350 | 1.48 |
| T2 | `mean_loan_rate_main` | 一阶水平 | +1.26 | +0.43 | 52.0% | +1.69 | 0.341 | 1.20 |
| T3 | `loan_utilization_ratio` | 二阶方差 | +0.53 | +0.20 | 17.2% | +0.80 | 0.385 | **0.23** |
| T6 | `shrt3_bar` | 一阶水平 | +0.49 | +0.08 | 64.8% | +0.61 | 0.158 | 1.53 |
| T4 | `loan_utilization_ratio` | 一阶水平 | +0.30 | +0.06 | 27.0% | +0.45 | 0.204 | **0.33** |

---

## 3. 已证实的判读（来自波 144）

### 3.1 「二阶矩」不是普遍规律，是费率族专有
同一骨架 `ts_covariance` 下：费率 1.81 vs 利用率 **0.53**。
⇒ 机制不是「任意借券指标的波动都能预测」，而是**借券费率的不确定性 → 借券风险溢价**这一条具体的经济链条。
**含义**：不要指望把 M1 平移到 utilization / bar / duration 上复现强度；要换的是**经济机制**，不是字段名。

### 3.2 利用率族信号落在不可投资区
T3 / T4 的 `invest_S / S` 只有 **0.226 / 0.333**，远低于第 2 号硬闸 0.70。
而费率族 T1 是 **0.812**、T2 是 1.198。
⇒ 利用率在 USA/TOP3000 抓的是小票微观结构，一旦按可投资性加权就崩。
**含义**：利用率方向若要继续，必须同时解决 inv 覆盖率——这不是调骨架能修的。

### 3.3 水平 vs 二阶矩：费率族「二阶矩赢」，但水平也不弱
费率：方差 1.81 vs 水平 1.26（差 +0.55 S）
利用率：方差 0.53 vs 水平 0.30（差 +0.23 S）
⇒ 二阶矩相对水平有一致增益，但**增益幅度远小于字段之间的差异（1.81 vs 0.53）**。
**含义**：选字段比选矩重要。

### 3.4 T5 揭示的正交性风险
`loan_rate_volatility_main`（厂商给的同日合约间标准差）翻转后 S +1.40、TO 57%。
它与 M1（时序方差）既有共同成分（都是「费率不确定性」）又不同（截面 vs 时序）。
⇒ **M3（自算 `vec_stddev`）大概率与 T5 同源**。M3 的真正价值不是强度，而是回答
「厂商 volatility 字段是否已经等价于自算离散度」——若等价则信息已被厂商打包，应转向别的维度。

### 3.5 效率标尺（USA 自校准）
`eff = F/S = sqrt(|R| / max(TO, 0.125))`。
USA 成功模板 band = **0.587–0.622**（TO > 12.5%），TO < 12.5% 时走下限 0.923。
T1 的 **0.829** 位于 band 之上 ⇒ 每单位换手的收益效率本次达标，瓶颈不在换手。

---

## 4. 禁区（论坛实证 + 本项目实测）

| 禁区 | 证据 |
|---|---|
| **二阶矩禁用 CV 归一化**（除以水平） | 帖 A：`ts_covariance` 除以费率水平后 S 1.89 → 0.61，信息在绝对量纲 |
| 二阶矩加 `reverse` 之外的符号修正 | 帖 A 的安慰剂 `ts_delta(x,22)` S=0.09、TO 98.7% ⇒ 一阶差分在**费率**上纯噪声（但利用率上有效，见 M2/M6，需分族判断） |
| `group_rank` 替代 `group_zscore` | 帖 A：group_rank 版 0.71 vs group_zscore 版 1.64，秩变换丢掉方差长尾 |
| `group_cartesian_product(country, exchange)` | 帖 A：与单 `exchange` 的 PnL 逐位相同 ⇒ 嵌套轴是死参数 |
| 用 `max_loan_rate_main` 做水平 | 帖 A：极端合约主导噪声，S 降到 1.21（JPN 0.64 挂） |
| 做除代替做差 | 帖 B：`offer ÷ 做空占比` S 1.14 ❌ vs `offer − bid` S 2.01 ✅；`offer ÷ 利用率` 1.16 ❌ vs `last − offer` 2.68 ✅ |
| `ILLIQUID_MINVOL1M` universe | `get_platform_setting_options` 权威：**USA 无此档**（只有 TOP3000/2000/1000/500/200/TOPSP500），帖 B 的低流动性杠杆只能靠分组近似 |
| 给带单位字段加无量纲常数 | 平台 `unitHandling=VERIFY` 直接 WARNING 失败；比值一律同单位相除 |

---

## 5. 价差结构族「价格歧视」（M17–M24，波 146–150 实证 —— 本项目 shortinterest3 最强产出）

**核心信号**：`spread = subtract(vec_max(min_loan_rate), vec_min(max_loan_rate))`
= 同一只票在出借市场上「最低可借费率」与「最高可借费率」之间的**极差**。
经济含义 = **出借人之间的价格歧视幅度**：价差越大，说明券源分散在报价差异极大的多方手里，
空头必须跨多个出借人才能建仓，边际借券成本陡增 ⇒ 挤压（squeeze）脆弱性。

> ⚠ 这不是「费率水平」，也不是「均值价差」。它是**分布宽度**。三条实证排除了替代写法（见下表）。

| 模板 | 骨架 | S | F | TO | 2Y | SUB | fRA | 判读 |
|---|---|---|---|---|---|---|---|---|
| **M17** 原始 | `reverse(group_zscore(spread, industry))` | 1.95 | 0.91 | 49.29% | 2.73 | — | 4 | 基线（未翻转 −1.95）；换手过高 |
| **M24** 水平 | `reverse(group_zscore(subtract(vec_avg(max_loan_rate), vec_avg(min_loan_rate)), industry))` | 1.53 | 0.58 | 52.82% | 2.39 | 0.71 | 3 | ❌ **均值价差替代极差即崩** |
| **M18** 二阶矩 | `reverse(group_zscore(ts_covariance(spread, spread, 22), industry))` | 2.15 | 1.95 | 16.84% | **3.61** | 1.20 | **0** | 2Y 最高；无平滑 |
| **M19** 一阶矩+平滑22 | `reverse(ts_decay_linear(group_zscore(spread, industry), 22))` | 2.29 | 2.25 | 13.96% | 2.82 | 0.98 | 2 | CW + SUB 差 0.01 |
| **M20** 一阶矩+平滑66 | 同上窗口 66 | 2.35 | 2.42 | 12.90% | 2.86 | 1.09 | 1 | 仅卡 CW |
| **M21** ★★**最优** | `reverse(ts_decay_linear(group_zscore(ts_covariance(spread, spread, 22), industry), 66))` | **2.35** | **2.59** | **11.32%** | **3.34** | **1.29** | **0** | **全场最强 + 全闸** |
| **M22** 交叉 | cov22 + 平滑22 | 2.24 | 2.42 | 12.32% | 3.14 | 1.17 | 0 | 平滑 22 弱于 66 |
| **M23** cov66 无平滑 | `reverse(group_zscore(ts_covariance(spread, spread, 66), industry))` | 2.33 | 2.51 | 12.96% | 3.03 | 1.28 | 0 | inv_ratio 0.7124 贴下限 |
| **M25** cov126 | cov 窗口 126 | 1.98 | 1.98 | 11.97% | 2.44 | 1.21 | 0 | 窗口过长衰减 |

### 5.1 CW（CONCENTRATED_WEIGHT）破解配方 —— 根因是算子顺序

**症状**：M19/M20（一阶矩 + 平滑）稳定卡 CW，且 `checks.fail = []` 只有 `warning` 含 CW，但 `ra.failed_ra_count = 1`。
**已排除的三条错误破法**：
| 破法 | 结果 |
|---|---|
| `truncation` 0.08 → 0.05 → 0.03 | 指标**逐位完全相同**。持仓 3095 只 ⇒ 单票权重 0.032% 远低于阈值 ⇒ **截断从不触发** |
| `winsorize(std=4)` 包在 group_zscore 外 | fRA 仍 1（S 2.21 / F 1.96 / 2Y 3.64）⇒ 不是尾部极值 |
| `neutralization` SLOW → SUBINDUSTRY | fRA 仍 1，F 2.88 但 **DD 32.76%**（基线 7.62%）⇒ 换来的 F 是分母锁死假象（TO 5.96% < 12.5%） |

**正确解法（实测 fRA 1 → 0）**：把**横截面标准化挪到最外层**，内层只做时序运算。
```
错：ts_decay_linear( group_zscore( spread, industry ), 66 )        ← 先截面标准化，再平滑 z 值 ⇒ CW
对：group_zscore( ts_decay_linear( ts_covariance(spread,spread,22), 66 ), industry )  ← 内层时序，外层截面 ⇒ fRA 0
```
机理：平滑作用在 z 值上时，某些票的 z 值长期同号 ⇒ 平滑后权重持续偏高 ⇒ 集中度告警。
平滑作用在原始时序量（cov）上则不会，因为分布形状不被截面标准化固定住。
**代价**：0 —— M21 的 S/F/2Y/SUB 全部优于 M20，且 TO 更低（11.32% vs 12.90%）。

### 5.2 该族的其它禁区（每条都做过单因素对比）

| 禁区 | 证据 |
|---|---|
| **费率水平归一化** | `divide(spread, vec_avg(mean_loan_rate_main))` ⇒ S 1.95→0.94、TO 49%→77%、inv 0.33。绝对值承载「券源紧张程度」的横截面信息 |
| **均值价差替代极差** | `vec_avg(max)−vec_avg(min)` ⇒ S 1.53/F 0.58/TO 52.8%（M24）。**极差才是信号** |
| **`sector` 轴替代 `industry`** | TO 14.00%→40.72%、S 2.29→2.05、F 2.25→1.41。sector ≈ 11 组太粗，组内异质性推高换手 |
| **`group_rank` 替代 `group_zscore`** | S **0.95**（第 3 次复现）。秩变换丢弃价差幅度 |
| **cov 与 decay 合并成单层窗口** | M23（只有 cov66）S 2.33/2Y 3.03 < M21（cov22+decay66）S 2.35/2Y 3.34。两层职责不同：cov 窗口管二阶矩统计稳定性，decay 管输出平滑降换手 |

### 5.3 族内与跨族互相关（4y / 986pt）

- **族内 5 颗（M18/M21/M22/M23/M25）互相关 0.71–0.96** ⇒ `max_mutually_below_subset_size = 1`，**只能提交 1 颗**（选 M21）。
- **本族 ↔ A 家族（借贷利用率 `gJezNxjg`/`E56AnWgP`）= 0.5677–0.6375 < 0.7** ⇒ 可各取 1 组成 2 颗提交篮。
- A 家族内部 `gJezNxjg` ↔ `E56AnWgP` = 0.9336 ⇒ 也只能取 1 颗。

---

## 6. 待验证的模板（保持多样性储备）

以下模板尚未进入波次，按需启用（每个都必须配单因素对比，不能一次上多个变量）：

- **M13 期限结构**：`group_zscore(vec_avg(average_loan_duration_days_main), industry)` —— 借券期限越长 = 空头越笃定。
- **M14 期限 × 费率**：`group_zscore(multiply(vec_avg(average_loan_duration_days_main), vec_avg(mean_loan_rate_main)), industry)`。
- **M15 分箱边界作分组轴**：`group_rank(<信号>, bucket(rank(vec_avg(rate_bin_upper_limit)), range="0,1,0.2"))` —— 借券成本档位内的相对信号。（`bucket` 已验证非幽灵算子，但参数签名未实测。）
- **M16 存量-流量背离**：`group_zscore(divide(vec_sum(new_loaned_share_count), vec_sum(loaned_share_count)), industry)` —— 新增借券占存量的比例（同单位）。
- **M17 事件门控**：`trade_when(<触发>, <信号>, -1)` —— 仅在费率突变日建仓。

---

## 7. 复现命令

```powershell
# 以下命令均在仓库根目录执行（仓库根 = 本仓 wqb 目录）
$env:PYTHONPATH='src;tools'
$env:PYTHONIOENCODING='utf-8'
# 字段画像（手工确认后的口径文档）
python 'tools\fields\profile_dataset_fields.py' --region USA --dataset shortinterest3 --input tracking/USA/reports/field_profiles/shortinterest3_raw.json --out docs/reference/USA/shortinterest3_field_profile.md --top 25
```

MCP 预检（派发前必做）：
```
preflight_expressions({alpha_expressions, region:"USA", universe:"TOP3000", delay:1,
                       dataset_id:"shortinterest3", auto_fix_vector:false})
operator_audit({expressions, region:"USA", universe:"TOP3000", delay:1})
```

---

## 8. 数量与时间维度族（M26–M31，波 154）

### 8.1 为什么必须开这个族

族 B（价差 `spread = vec_max(min_loan_rate) − vec_min(max_loan_rate)`）与族 C（`vec_avg(mean_loan_rate_main)` 的时序方差）
**都是费率价格维度**。shortinterest3 的 31 字段里还有两类完全正交的经济量，实测 alphaCount 极低：

| 维度 | 字段 | 用户 / alpha | 说明 |
|---|---|---|---|
| **时间** | `average_loan_duration_days_main` | **20 / 26** | 加权平均贷款账龄（天） |
| **流量** | `new_loaned_share_count` | 41 / 53 | 新增借券股数（CSShare） |
| | `loaned_share_count` | 27 / 34 | 存量借券股数（CSShare） |
| **深度** | `transaction_count_main` | 29 / 63 | 交易笔数 |
| **需求** | `borrow_activity_score` | 55 / 75 | 借券需求评分 1–10 |
| 对照（红海） | `shrt3_bar` | 604 / 2028 | — |
| 对照（红海） | `mean_loan_rate` | 150 / 241 | — |

### 8.2 六个模板（骨架互异，非只换窗口）

| 模板 | 骨架 | 算子几何 | 经济假设 |
|---|---|---|---|
| **M26** | `reverse(group_zscore(ts_decay_linear(vec_avg(average_loan_duration_days_main), 22), industry))` | 平滑 → 截面 z | 账龄短 = 空头快速换手/平仓压力大 |
| **M27** | M26 去 `reverse` | 同上 | **方向配对**，一次性定死账龄方向先验 |
| **M28** | `reverse(group_zscore(ts_zscore(vec_avg(average_loan_duration_days_main), 252), industry))` | 时序 z（相对自身 1 年历史） | 账龄的历史分位，剥离个股水平差异 |
| **M29** | `reverse(group_zscore(ts_decay_linear(divide(vec_sum(new_loaned_share_count), vec_sum(loaned_share_count)), 22), industry))` | 同单位相除 → 平滑 → 截面 z | 新增/存量 = 空头**边际**进场速度（流量 vs 存量） |
| **M30** | `reverse(group_zscore(ts_rank(vec_avg(transaction_count_main), 252), industry))` | 时序分位 → 截面 z | 券源市场深度 / 参与方数量 |
| **M31** | `reverse(group_zscore(ts_delta(vec_avg(borrow_activity_score), 22), industry))` | 一阶差分 → 截面 z | 借券需求评分的变化率（需求动量） |

**多样性检查**：5 种不同算子几何（decay 平滑 / 时序 z / 同单位相除 / ts_rank 分位 / ts_delta 差分），
覆盖 4 个互异字段，4 种经济机制（时间 / 流量 / 深度 / 需求）。不是「只换窗口或常数」。

**单位安全**：`average_loan_duration_days_main` 带「天」单位 ⇒ `group_zscore` 移到最后一步（无量纲化出口）。
M29 两腿同单位（CSShare）相除天然无量纲，不需要加 ε。

---

## 9. `short_interest_pred` 判死（波 153，6 条实测）

**结论：全族判死，不再投波。** 这是 SHORTINTEREST 类别第 5 个判死数据集。

| tag | alpha | S | F | TO | 2Y | margin |
|---|---|---|---|---|---|---|
| Z1 `surprise_value` 反向 | `vR108blA` | −0.39 | −0.04 | 151.31% | −3.45 | −0.000018 |
| Z2 `surprise_value` 正向 | `O0AeO66Y` | 0.39 | 0.04 | 151.31% | **+3.45** | 0.000018 |
| Z3 `surprise_ratio` 反向 | `gJev6W8e` | 0.61 | 0.07 | 142.56% | −1.95 | 0.000024 |
| Z4 修订（current − prior） | `zq3aZGpV` | −0.35 | −0.04 | 127.49% | 0.46 | −0.000026 |
| Z5 `predicted_change` 反向 | `YP1Z6JYW` | **0.99** | 0.14 | 131.69% | 2.55 | 0.000042 |
| Z6 `surprise_ratio` ts_rank+平滑 | `KPJe3vmx` | −0.18 | −0.02 | 41.66% | −2.47 | −0.000020 |

四条判据：

1. **eff 标尺**：eff = F/S = **0.103 / 0.115 / 0.114 / 0.111 / 0.141**，全在 0.10–0.14；
   USA 成功 band = 0.587–0.622 ⇒ **低 4–6 倍**。与 shortinterest43（0.15–0.41）同档甚至更差 ⇒ 字段无收益承载能力。
2. **margin**：最高 0.000042 vs `Xg9qjVOz` 的 0.002682 ⇒ **差 64 倍**。
3. **TO**：全部 127–151%（Z6 用重度平滑压到 41.7%，代价是 S 转负 −0.18）。
   ⇒ **「双周发布 = 事件驱动 = 天然低换手」假设被推翻**，平台按日频更新展开。
4. **样本期风险**：Z2 正向 2Y **+3.45** 但全期 S 仅 **0.39** ⇒ 2014–2021 完全无效、2022–2023 才成立。
   这是样本外失效风险最高的形态（近两年单边拟合），即使 prod 过关也不应提交。

**Z1/Z2 是精确镜像**：S ±0.39、2Y ∓3.45、TO **逐位相同** 151.31% ⇒ 第 4 次验证「符号翻转是精确动作」。

**意外度修订假设证伪**：Z4 = `current − prior` S −0.35 ⇒ `prior_*` 字段不带来增量，「意外的加速度」无预测力。

**族内最强不可用**：Z5 `predicted_change` 反向 S 0.99 / 2Y 2.55 / DD 仅 8.96%，但 TO 131.69% + margin 0.000042
⇒ 收益被交易成本吃光。该字段同时是族内最拥挤（119 用户 / 240 alpha）。

**SHORTINTEREST 剩余数据集状态**：
| dataset | 状态 |
|---|---|
| `shortinterest3` | **唯一活路**（本库，族 B/C 已出 2 颗全闸候选，第 8 章 M26–M31 待验证） |
| `shortinterest43` | 判死（波 151+152，12 条） |
| `short_interest_pred` | 判死（波 153，6 条） |
| `shortinterest29` | 判死 |
| `shortinterest24` | 覆盖 0.2573，不可用 |
| `us_short_sale` | 4 字段，与 shortinterest43 A 族同机理（SVO 日频流量比）⇒ 优先级最低 |
