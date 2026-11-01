# GBR SHORTINTEREST 塔模板库 —— 借券费率 / 借券量 / 借券期限 / 需求评级

> 区域：**GBR / TOP700 / D1**（universe 唯一，无退路）
> 建立：2026-10-31
> 数据集：`shortinterest3`（证券借贷 / short borrow）
> 塔位：**SHORTINTEREST —— 本区 0 条已提交，需 3 条点亮**
> 目标：给出 **≥10 个结构互异**模板，差异落在骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性 / 窗口族上。

---

## §0 为什么挑这个数据集（选靶依据，不是感觉）

| 依据 | 数值 | 来源 |
|---|---|---|
| 塔位缺口 | SHORTINTEREST 塔 = **0 条**（点亮需 3 条） | 本会话塔位台账 |
| GBR 真实需求 | `shortinterest3` 在 GBR 有 **73 条已提交 alpha**，位列全榜第 14、非 MODEL/ANALYST 类第 2 | 论坛 `42587179348119`（87 赞）Part 2 热度榜 |
| 字段级覆盖 **当前有效** | 25 个字段 **全部** cov 0.8217–0.8719（不是 0） | `get_datafields(GBR/D1/TOP700)` 实测 2026-10-31 |
| 拥挤度分层 | 借券量族拥挤（`loaned_share_count_p5_d1` 288 条）／费率族宽松（`loan_rate_volatility` 16 条、`max_loan_rate` 20 条） | 同上 alphaCount |
| 类别合规 | `shortinterest` **不属于 trio**（PV/MODEL/OTHER）⇒ 单塔 alpha 无任何混塔禁令 | 用户硬约束 |

### ★ 反面教训（同批次实测，必须记住）

| 数据集 | 论坛热度（GBR 首周） | 实测字段级 coverage | 判定 |
|---|---:|---:|---|
| `institutions25` | 13 条 | **24/24 字段 = 0.0** | STRUCTURAL-DEAD（零仿真） |
| `imbalance5` | **163 条**（全榜第 10） | **2/2 字段 = 0.0** | STRUCTURAL-DEAD（零仿真） |
| `analyst48` | — | 7/7 VECTOR，全是**指数元数据**（除数/类型码/Bloomberg ID/字段数/返回码） | 语义闸跳过 |

**三条硬结论**：
1. **数据集级 `coverage > 0` ≠ 字段级 `coverage > 0`** —— 必须逐 `get_datafields` 看数值。
2. **论坛热度榜是 2026-08-09 首周快照，今天 10-31** —— 覆盖可能已被收回，`alphaCount` 是**全局跨区跨时**累计值，不能当本区可用性证据。
3. **`get_datasets` 的 coverage 也不可信**：`institutions25` / `imbalance5` 在数据集级有覆盖，字段级全零。

---

## §1 字段清单（25 个，**全 VECTOR**，须 `vec_*` 折叠）

**三档后缀**（覆盖密度递增）：无后缀 `0.8217` → `_main` `0.8512`（描述为 "primary key group"）→ `_p5_d1` `0.8719`。
**探针主力用 `_main`**（语义最清楚），`_p5_d1` 作为**聚合档变体**，无后缀档作为第三档。

| 族 | 字段 | 语义 | 单位 | alphaCount（裸/main/p5） |
|---|---|---|---:|---:|
| **费率水平** | `mean_loan_rate[_main/_p5_d1]` | 加权平均借券费率 | 费率 | 27 / 42 / 75 |
| 费率极值 | `max_loan_rate[_main/_p5_d1]` | 最高借券费率 | 费率 | 20 / 38 / 49 |
| 费率极值 | `min_loan_rate[_main/_p5_d1]` | 最低借券费率 | 费率 | 18 / 29 / 39 |
| **费率离散** | `loan_rate_volatility[_main/_p5_d1]` | 借券费率标准差 | 费率（**与均值同单位**） | 16 / 47 / 45 |
| **借券量** | `loaned_share_count[_main/_p5_d1]` | 出借股数 | 股 | 27 / 220 / 288 |
| 借券金额 | `loaned_market_value_usd[_main/_p5_d1]` | 出借市值 USD | USD | 67 / 124 / 249 |
| 借券活跃度 | `transaction_count[_main/_p5_d1]` | 借券成交笔数 | 笔 | 29 / 147 / 164 |
| **借券期限** | `average_loan_duration_days[_main/_p5_d1]` | 出借平均账龄（天） | 天 | 48 / 48 / 49 |
| **需求评级** | `shrt3_bar` | 借券需求评分 **1–10**（1=低需求，10=高） | 评分 | 109（**唯一档**，cov 0.8669） |

### 单位闸风险点（派发前必读）
- `divide(mean_loan_rate, loan_rate_volatility)`：两者都标"费率"，**同单位相除 → 无量纲**，理论合法。**若平台把 `_volatility` 标成不同 `Unit[...]` 会挂**，故把它排在探针第 7 位（先拿前 6 条的结果再决定要不要补）。
- `rank()` / `vec_avg()` 对带单位字段安全（不改量纲）。
- **禁止**：`greater(<带单位计数>, 常数)`、`add(<带单位>, 常数)`、`power(x,2)` 对带单位字段。

---

## §2 模板全表（12 个，结构互异）

统一记法：`F` = 主字段，`W ∈ {1,5,22,66,252,504,1008,1260}`。`N(·)` = 方向取负（`multiply(·, -1)`）——**不用 `reverse()`**，避开平台 `REVERSION_COMPONENT` 警告。

| # | 模板表达式 | 经济机制 | 矩 | 骨架结构 | 算子几何 | 非线性 | 方向 | 来源 |
|---|---|---|---|---|---|---|---|---|
| **T1** | `N(rank(vec_avg(mean_loan_rate_main)))` | 卖空约束价格 = 空头成本。高费率 = 空头拥挤 + 知情做空 | 水平 | 单字段 | `vec_avg` + `rank` | 截面秩 | − | 论文 Asquith-Pathak-Ritter 2005；Engelberg-Reed-Ringgenberg 2012（**fee 优于 interest 数量**） |
| **T2** | `N(rank(ts_zscore(vec_avg(mean_loan_rate_main), 252)))` | 相对自身 1 年历史的**异常**借券成本（事件型） | 水平·时序标准化 | 自比长窗 | `ts_zscore(252)` + `rank` | 标准化 + 秩 | − | 论坛 `43152032301591`（事件强度类信号锁 `ts_zscore`，`rank` 是毒药）+ 自建 |
| **T3** | `N(rank(ts_delta(vec_avg(loaned_share_count_main), 22)))` | 22 日**空头建仓流量**（知情做空） | **一阶差分** | 单字段差分 | `ts_delta(22)` + `rank` | 截面秩 | − | 论文 Boehmer-Jones-Zhang 2008（short sellers are informed）；Drechsler |
| **T4** | `N(rank(vec_avg(loan_rate_volatility_main)))` | 出借人对稀缺度的**分歧** → 估值不确定性 | **二阶（方差）** | 单字段 | `vec_avg` + `rank` | 截面秩 | − | 论文 Diether-Malloy-Scherbina 2002（分歧度）+ Zhang 2006（不确定性 ⇒ underreaction） |
| **T5** | `N(rank(vec_avg(shrt3_bar)))` | 借券需求**复合评级**（S3/IHS 类） | 水平·评级 | 单字段 | `vec_avg` + `rank` | 截面秩 | − | 论文 Asquith et al. 2005 的 ready-to-borrow 代理；数据集自述 |
| **T6** | `N(group_rank(vec_avg(mean_loan_rate_main), subindustry))` | 剥离**行业共同借券成本**，只留公司相对稀缺度 | 水平 + **分组轴** | 分组内秩 | `group_rank(subindustry)` | 组内秩 | − | 论坛 `43287696633239`（`group_rank(x, sector)` 剥行业景气）+ 自建 |
| **T7** | `rank(vec_avg(average_loan_duration_days_main))` | 空头持仓**账龄**：长期持有的空头信息已被价格吸收 ⇒ 后续反转向上 | 水平·时长 | 单字段 | `vec_avg` + `rank` | 截面秩 | **+（不取负）** | 论文 short-interest "stale" 效应；自建方向假设（**本表唯一正方向模板**，也是方向性对照） |
| **T8** | `N(rank(divide(vec_avg(mean_loan_rate_main), vec_avg(loan_rate_volatility_main))))` | **单位分歧下的借券成本** = 高信念做空（费率贵但拥挤度一致） | **复合比值** | 双字段同单位比 | `divide` + `rank` | 截面秩 | − | 自建（融合 T1 与 T4 的经济含义，**非混信号**：分子分母同一经济量的水平/离散） |
| **T9** | `N(rank(vec_avg(transaction_count_main)))` | 借券市场**活跃度** = 空头换手强度 | 水平·计数 | 单字段 | `vec_avg` + `rank` | 截面秩 | − | 论文 34891819291799 族（换手/流动性冲击）；数据集自述 |
| **T10** | `N(rank(ts_quantile(vec_avg(mean_loan_rate_main), 252)))` | 费率在**自身历史分布**中的位置（反 CDF） | 水平·时序分位 | 自比长窗 | `ts_quantile(252)` + `rank` | **时序分位反 CDF** | − | 本区已验证骨架（`template_library_gbr_pv_volume_volatility.md` T2/T3，`88Rg2zPV` / `e75eWObM` 实跑成功） |
| **T11** | `N(signed_power(subtract(rank(vec_avg(shrt3_bar)), 0.5), 3))` | 只押**极端借券需求**，中部稀释掉 | 水平 → 尾部放大 | 中心化 + 幂 | `subtract(0.5)` + `signed_power(3)` | **三次幂（尾部加权）** | − | 论坛 `43298855144855`（形态 Peak / `signed_power`；本区需整幂，ASI 的 0.1 分数幂在 GBR 是 no-op） |
| **T12** | `N(rank(subtract(ts_mean(vec_avg(mean_loan_rate_main), 22), ts_mean(vec_avg(mean_loan_rate_main), 252))))` | **费率曲线斜率**：短窗 vs 长窗（借券成本在加速还是回落） | **双窗差** | 同字段双尺度 | `ts_mean(22)` − `ts_mean(252)` | 截面秩 | − | 论坛 `39765287755415`（双窗比）+ 自建（**窗口族**：改为差而非比，避免除零） |

**备用**：`T13 = N(rank(ts_rank(vec_avg(mean_loan_rate_main), 120)))` —— 论坛 `43287696633239` 坑二（JPN 偏好时序形态，横截面 `rank` 弱于 `ts_rank(120)`）。GBR 未验证，留作窗口族补充。

### 结构互异性核验

| 维度 | 覆盖模板 |
|---|---|
| 矩 = 水平 | T1, T5, T6, T7, T9, T10 |
| 矩 = 一阶差分 | T3 |
| 矩 = 二阶（方差） | T4 |
| 矩 = 复合（比值 / 双窗差） | T8, T12 |
| 骨架 = 单字段 | T1, T2, T3, T4, T5, T7, T9, T10 |
| 骨架 = 分组轴 | T6 |
| 骨架 = 双字段 | T8 |
| 骨架 = 同字段双尺度 | T12 |
| 非线性 = 截面秩 | T1–T6, T8, T9, T12 |
| 非线性 = 时序标准化 / 分位 | T2, T10 |
| 非线性 = 幂（尾部） | T11 |
| 非线性 = 无（纯排序） | T7 |
| 方向 = 负（做空高借券成本） | T1–T6, T8–T12 |
| 方向 = 正（空头账龄反转） | **T7（方向性对照组）** |
| 分组轴 | T6（`subindustry`） |
| 窗口族 | T1(无) / T2(252) / T3(22) / T10(252) / T12(22 vs 252) / T13(120) |

---

## §3 探针计划（8 条，分 4 批 × 2 条）

**宗旨**：8 条覆盖 8 个不同机制，且必须包含一个**方向对照组（T7）**——若 T7 与 T1 同为负，说明方向假设错了，不是信号弱。

| 批 | # | 模板 | 表达式骨架 | 设置档 |
|---|---|---|---|---|
| 1 | P1 | T1 费率水平 | `N(rank(vec_avg(mean_loan_rate_main)))` | `INDUSTRY` / decay10 / trunc0.05 |
| 1 | P2 | T5 需求评级 | `N(rank(vec_avg(shrt3_bar)))` | `INDUSTRY` / decay10 / trunc0.05 |
| 2 | P3 | T3 建仓流量 | `N(rank(ts_delta(vec_avg(loaned_share_count_main), 22)))` | `INDUSTRY` / decay10 / trunc0.05 |
| 2 | P4 | T4 费率离散 | `N(rank(vec_avg(loan_rate_volatility_main)))` | `INDUSTRY` / decay10 / trunc0.05 |
| 3 | P5 | T7 **方向对照** | `rank(vec_avg(average_loan_duration_days_main))` | `INDUSTRY` / decay10 / trunc0.05 |
| 3 | P6 | T2 异常费率 | `N(rank(ts_zscore(vec_avg(mean_loan_rate_main), 252)))` | `SUBINDUSTRY` / decay4 / trunc0.08 |
| 4 | P7 | T10 时序分位 | `N(rank(ts_quantile(vec_avg(mean_loan_rate_main), 252)))` | `INDUSTRY` / decay10 / trunc0.05 |
| 4 | P8 | T6 行业相对 | `N(group_rank(vec_avg(mean_loan_rate_main), subindustry))` | `MARKET` / decay4 / trunc0.05（**必须非 INDUSTRY，否则 `group_rank` 是 no-op**） |

**未进首轮**（留作完整波的增量）：T8（单位风险）、T9、T11、T12、T13。

---

## §4 GBR 特有约束（决定设置档）

| 事实 | 数值 / 证据 | 对模板的影响 |
|---|---|---|
| **GBR 换手率 ↑ ⇒ 收益率 ↑ 显著（p<0.001）** | 论坛 `42587179348119` 按 TO 十等分 | **不要为压 TO 牺牲信号**；本会话此前「一律压 TO」的默认动作在 GBR 是错的 |
| GBR 已提交 alpha 的 margin 分布 | 中位 **11.9bp** / 均值 13.4bp / 75% 分位 **16.2bp** | margin < 11.9bp 的候选应视为低质，除非 S/F 极强 |
| `LOW_SUB_UNIVERSE_SHARPE` limit | **≈ 0.434 × S**（GBR TOP700，多次实测 0.431–0.438） | 比 ASI 的 robust 0.90×S 宽松一倍以上 ⇒ **纯单腿信号在 GBR 有机会**（论坛 `43287696633239` 说纯 analyst 腿在 ASI 卡 0.72–0.83） |
| D1 闸门 | S 1.58 / F 1.0 / 2Y 1.58（严格不等式）/ TO ≤0.70 / CW ≤0.1 | — |
| 本区已证伪中性化 | SLOW / CROWDING / SECTOR / SUBINDUSTRY | 主力用 `INDUSTRY`；`MARKET` / `FAST` / `NONE` / `SLOW_AND_FAST` 未测 |
| 本账号不可用算子 | `ts_max` / `ts_min` / `is_not_nan`（回测 ERROR 且级联整批 CANCELLED） | 本表 12 个模板**均不含**这三个 |
| `ts_target_tvr_decay` / `hump` / `vec_avg` | 已验证可用 | 若 T1 换手过高，先上平台层 `decay`，不写进表达式 |

---

## §5 判死口径（本数据集专用）

哪怕 8 探针全灭，也要按三档标签落台账：

- `PROBE-KILLED`：< 8 探针 —— **不得写进 dead_end**
- `CONFIRMED-DEAD`：≥8 探针 + ≥2 结构族 + ≥50% 字段覆盖（本集 25 字段，需覆盖 ≥13 个）
- `STRUCTURAL-DEAD`：额外需要「栖息地缺失」或跨区对照证据

**注意本集的特殊结构**：9 个字段族 × 3 档后缀 = 25 字段。若只测 `_main` 档，字段覆盖仅 8/25 = 32%，**不满足 ≥50%** ⇒ 判死前必须补 `_p5_d1` 档两条，或用「同族同度量」声明豁免（三档是同度量不同聚合，不是三个独立字段）。

---

## §6 探针实测账本（12 条，2026-10-31）

**全部为 REGULAR / GBR / TOP700 / D1 / FASTEXPR / `unit_handling=VERIFY` / `nan_handling=ON` / `max_trade=OFF` / `pasteurization=ON`。**

| # | 模板 | 字段族 | 表达式 | alpha | S | F | TO | 2Y | SUB | margin | invest_ratio | CW/判 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| P1 | T1 费率水平 | 费率水平 | `N(rank(vec_avg(mean_loan_rate_main)))` | `1YNVbQmR` | **0.01** | 0.00 | 11.37% | 0.06 | 0.35 | 0.13bp | 4.00* | ✗ |
| P2 | T5 需求评级 | 评分 | `N(rank(vec_avg(shrt3_bar)))` | `omEw5Mzb` | 0.23 | 0.07 | 12.57% | 0.34 | **0.79** | 2.10bp | 1.2174 | ✗ |
| P3 | T3 建仓流量 | 借券股数 | `N(rank(ts_delta(vec_avg(loaned_share_count_main), 22)))` | `d5W8VAPx` | −0.09 | −0.01 | 18.39% | −0.43 | 0.20 | −0.03bp | −1.6667 | ✗ |
| P4 | T4 费率离散 | 费率离散 | `N(rank(vec_avg(loan_rate_volatility_main)))` | `A1VJZM2Q` | **0.49** | 0.22 | 11.58% | 0.45 | 0.57 | 4.17bp | 0.7347 | ✗ |
| P5 | T7 期限对照 | 借券期限 | `rank(vec_avg(average_loan_duration_days_main))` | `O0AwPEdY` | 0.01 | 0.00 | 8.89% | **0.72** | 0.01 | 0.08bp | −9.00* | ✗ |
| P6 | T2 异常费率 | 费率水平 | `N(rank(ts_zscore(vec_avg(mean_loan_rate_main), 252)))` | `KPJYdaNp` | 0.13 | 0.02 | 28.91% | −0.56 | −0.04 | 0.03bp | −0.4615 | ✗ |
| P7 | T10 时序分位 | 费率水平 | `N(rank(ts_quantile(vec_avg(mean_loan_rate_main), 252)))` | `WjOwQ6rN` | −0.05 | −0.01 | 17.35% | −1.13 | −0.07 | −0.02bp | −0.60 | ✗ |
| P8 | T6 行业相对 | 费率水平 | `N(group_rank(vec_avg(mean_loan_rate_main), subindustry))` | `Xg9wQ6O8` | 0.41 | 0.12 | 18.15% | **0.80** | 0.30 | 1.73bp | 1.0000 | ✗ |
| **P9** | 费率极值（增量） | 费率极值 | `N(rank(vec_avg(max_loan_rate_main)))` | `d5W8V7r2` | 0.35 | 0.13 | 9.87% | 0.20 | **0.79** | 3.71bp | 1.0286 | ✗ |
| **P10** | ★★★ **成交笔数（增量）** | **计数** | `N(rank(vec_avg(transaction_count_main)))` | **`1YNVbmAQ`** | **0.88** | **0.57** | **6.15%** | 0.25 | **1.48** | **17.05bp** | **1.0341** | ✗（距离闸） |
| **P11** | ★★★ **异常借券活动（增量）** | **计数** | `N(rank(ts_zscore(vec_avg(transaction_count_main), 252)))` | **`1YNVbXXk`** | 0.81 | 0.37 | 10.29% | **1.60** ✅ | 1.19 | 5.17bp | 1.0741 | 3 fail（S/F/2Y 之外的都过） |
| **P12** | 后缀稳健性（增量） | **计数** | `N(rank(vec_avg(transaction_count_p5_d1)))` | **`88Rk9jjq`** | 0.86 | 0.55 | 6.14% | 0.30 | **1.50** | 16.58bp | 1.0349 | ✗ |

`N(x)` = `multiply(x, -1)`。`*` = `investability_ratio` 因 S 接近 0 而数值爆炸（0.04/0.01、−0.09/0.01），**不是真信号**。
设置：P1–P5/P7/P9/P10/P11/P12 = `INDUSTRY`/decay10/trunc0.05；P6 = `SUBINDUSTRY`/decay4/trunc0.08；P8 = `MARKET`/decay4/trunc0.05。
全部 `status=UNSUBMITTED`、`failed_ra_count` 3–5（P11 只有 3 个 fail，是本数据集最少的一个）。

### 6.1 ★★★★★ P10 是决定性突破：`transaction_count` 一个字段打出全会话最好的质量组合

| 指标 | P10 实测 | GBR D1 闸门 | 差距 | 全会话地位 |
|---|---:|---:|---|---|
| **Sharpe** | **0.88** | 1.58 | 差 44% | ★ 本数据集最高（前最高 0.49，+80%） |
| **Fitness** | **0.57** | 1.0 | 差 43% | ★ 本数据集最高（前最高 0.22，+159%） |
| Turnover | 6.15% | ≤0.70 | ✅ 通过 | 极低 |
| 2Y Sharpe | 0.25 | 1.58 | ❌ 差 84% | **唯一硬短板** |
| **Sub-universe S** | **1.48** | ≈0.434×0.88 = 0.38 | ✅ **超额 3.9 倍** | ★ 全会话最高档 |
| **Margin** | **17.05 bp** | GBR 75% 分位 16.2bp | ✅ **超过 75% 分位** | ★ 全会话最高 |
| investability_ratio | 1.0341 | — | >1 | ✅ 信号在流动票里 |
| Returns | 5.24% | — | — | — |
| Drawdown | 12.14% | — | — | 相对温和 |

**这个质量组合不是病态的**：不像 `analyst9` 的 B2（SUB 0.80 但 2Y −0.03 / margin 2.35bp）或 C2（F 0.64 但 2Y 0.21 / TO 4.84% 靠 `ts_backfill` 强压）。P10 是**裸字段 + rank + 取负**，没有任何调参杠杆，TO 6.15% 是天然的、SUB 1.48 是天然的、margin 17bp 是天然的。**这是「字段方向对」的原生形态。**

### 6.2 ★★★★★ P11 vs P10：`ts_zscore` 是一个**真实但昂贵**的 2Y 修复杠杆

同一字段、同一方向、同一设置，只把 `rank(tc)` 换成 `rank(ts_zscore(tc, 252))`：

| 指标 | P10 水平 `rank(tc)` | P11 时序 z `rank(ts_zscore(tc,252))` | 变化 |
|---|---:|---:|---|
| **2Y Sharpe** | 0.25 ❌ | **1.60** ✅ | **+540%（修复！）** |
| Sharpe | **0.88** | 0.81 | −8% |
| Fitness | **0.57** | 0.37 | −35% |
| Returns | **5.24%** | 2.66% | **−49%（腰斩）** |
| Margin | **17.05bp** | 5.17bp | **−70%** |
| Turnover | 6.15% | 10.29% | +67% |
| **Drawdown** | 12.14% | **4.73%** | **−61%（大幅改善）** |
| Sub-universe S | 1.48 | 1.19 | −20% |
| failed_ra_count | 4 | **3** | −1 |

★ **这是「水平承载溢价、z-score 承载平稳性」的经典二分，而且代价高得惊人**：
- `ts_zscore` 把 2Y 从 0.25 拉到 **1.60（过闸）**，drawdown 砍掉 61%，但 **returns 腰斩、margin 掉 70%**。
- 机理：借券成交笔数的**绝对水平**才是经济含义（借券活跃度越高，未来跌得越多）；`ts_zscore` 只保留「相对自己历史的异常度」，丢掉了横截面水平差 ⇒ 剩余信息量少一半，但时间上平稳。
- **与 §6.1 的「零年是条件有效不是衰减」结论一致**：2018/2023 两年水平信号归零，但 z-score 在零年里仍有相对排序信息 ⇒ 2Y 被救起来。

★★★ **方法论定则（写入 sKill）**：
> `ts_zscore` 修 2Y 是**真实杠杆**（本轮 0.25→1.60，+540%），但它的定价是 **returns −50% / margin −70%**。
> **只在「S 已接近闸、只差 2Y」时才用**；当前 P11 的 S 0.81 离 1.58 差 95%，用 z-score 反而把 S 也拖下去了 ⇒ **本数据集应该走「把水平形态的 S 做上去」而不是「用 z-score 换 2Y」**。
> 如果未来出现 S≈1.5 但 2Y 弱的候选，`ts_zscore` 是第一顺位杠杆，且要同时复核 returns 是否被腰斩到 F 破闸。

### 6.3 ★★★ P12 = P10：`_main` 与 `_p5_d1` 两档后缀是同一条信息的重复载体

| 指标 | P10 `transaction_count_main` | P12 `transaction_count_p5_d1` | 差异 |
|---|---:|---:|---|
| S | 0.88 | 0.86 | −2% |
| F | 0.57 | 0.55 | −4% |
| TO | 6.15% | 6.14% | 0% |
| 2Y | 0.25 | 0.30 | 同档 |
| SUB | 1.48 | 1.50 | +1% |
| margin | 17.05bp | 16.58bp | −3% |

★ **逐位近似相同**。机理：`_p5_d1` 是对 `_main` 做 5 日位移+1 日延迟的版本，对月度/双周频的借券数据几乎不改变横截面排序。
★ **实践含义**：本数据集的 25 字段实际只有 **9 个独立信息**（9 个度量 × 3 档后缀 = 三份重复）。**不要为「补覆盖」去测其它字段的 `_p5_d1` 档——那是浪费仿真槽**。§8 的覆盖率豁免因此成立。

### 6.4 ★★★★★ P14 是全会话最好的候选：`group_rank + MARKET` 把三闸同时推到 1~10% 内

**表达式**：`multiply(group_rank(vec_avg(transaction_count_main), subindustry), -1)`
**设置**：`MARKET` / decay **4** / trunc 0.05（与 P10 不同）→ alpha **`O0AwP2mp`**

| 指标 | **P14 `O0AwP2mp`** | D1 闸门 | 差距 | vs P10 变化 |
|---|---:|---:|---|---|
| **Sharpe** | **1.42** | 1.58 | **差 10%** | 0.88 → 1.42（**+61%**） |
| **Fitness** | **0.99** | 1.00 | **差 1%** | 0.57 → 0.99（**+74%**） |
| **2Y Sharpe** | **1.48** | 1.58 | **差 6%** | 0.25 → 1.48（**+492%**） |
| Sub-universe S | **1.55** | ≈0.434×1.42 = 0.62 | ✅ 超额 2.5× | 1.48 → 1.55 |
| Turnover | 8.79% | ≤0.70 | ✅ | 6.15% → 8.79% |
| **Margin** | **13.94bp** | GBR 中位 11.9bp | ✅ | 17.05 → 13.94bp（−18%） |
| Returns | **6.12%** | — | — | 5.24% → 6.12%（**+17%**） |
| **Drawdown** | **7.65%** | — | — | 12.14% → 7.65%（**−37%**） |
| 持仓 | **440 / 471** | TOP700 | ✅ 满仓（P10 未测，但 P1 类只有 ~217） | — |
| investability_sharpe | **1.44** | — | ratio 1.014 | 信号在流动票里 |
| **risk_neutralized_sharpe** | **1.64 > S 1.42** | — | ★ 风格压制信号 | — |
| **failed_ppa_count** | **0** | — | ✅ PPA 全过 | — |
| `checks.fail` | **`[]`（空）** | — | 四项全在 `checks.warning` | — |

★★ 四个「失败项」全部落在 `checks.warning` 而非 `checks.fail`：`LOW_SHARPE` 1.42 / `LOW_FITNESS` 0.99 / `CONCENTRATED_WEIGHT`（无 value，疑似轻微超限）/ `LOW_2Y_SHARPE` 1.48。**这不是一条「差很远」的候选，是一条「三项各差 1~10%」的候选。**

#### ★★★★★ 最重要的方法论发现：修 2Y 应该用**横截面组归一化**，不是时序归一化

把 P10 / P11 / P14 三条摊开对比，这是同一字段、同一方向、三种归一化轴：

| 归一化轴 | alpha | 2Y | S | Returns | Margin | DD |
|---|---|---:|---:|---:|---:|---:|
| 无（裸 `rank`，跨全市场） | `1YNVbmAQ` (P10) | **0.25** | 0.88 | 5.24% | **17.05bp** | 12.14% |
| **时序**（`ts_zscore`, 252） | `1YNVbXXk` (P11) | **1.60** | 0.81 | **2.66%** | **5.17bp** | 4.73% |
| **横截面组**（`group_rank`, subindustry） | **`O0AwP2mp` (P14)** | **1.48** | **1.42** | **6.12%** | 13.94bp | **7.65%** |

> **定则（本会话最重要的单条发现之一）**：
> 两条路都能把 2Y 从 0.25 救到 1.5~1.6（+490%~+540%），但**代价完全相反**：
> - **时序归一化 `ts_zscore`**：丢掉横截面水平差 ⇒ **returns −49%、margin −70%、S 还跌**。用它等于「用信号强度换平稳性」。
> - **横截面组归一化 `group_rank(·, subindustry)`**：只换比较的**参照系**（从全市场换成同子行业同行）⇒ **returns +17%、S +61%、DD −37%，2Y 同样救起来**。**几乎零代价。**
>
> 机理：2Y 差往往不是「信号在近期衰减」，而是「**行业层面的共同暴露在近期反向**」（2018/2023 两个零年，全行业一起失效）。`ts_zscore` 只是在时间维上把失效年份压平；`group_rank` 是**从根上把行业共同暴露减掉**，只留选股 alpha ⇒ 行业轮动不再污染收益。

★★★ **与既有 memory 铁律的关系**：memory 记的是「事件强度类信号锁 `ts_zscore`」（来自 USA insider 域）。本数据集实证表明：**`ts_zscore` 应降为第二顺位；第一顺位是 `group_rank(·, subindustry) + 非 INDUSTRY 中性化`**，因为后者不牺牲收益。两条不矛盾——insider 域当时没试过 group_rank + MARKET 这个组合。**今后修 2Y 的动作顺序：①group_rank 换参照系 → ②decay/trunc 微调 → ③ts_zscore（最后手段，且必须复核 returns 是否腰斩）。**

#### 为什么 `group_rank + MARKET` 不是 no-op（与既有反例的区别）

memory 里有过反例：「`group_rank`/`group_neutralize` 加在已 INDUSTRY 中性化信号上是 no-op」。**本组合恰好绕开了那个陷阱**：

| 组合 | 是否 no-op | 效果 |
|---|---|---|
| `rank` + `INDUSTRY` 中性化 | — | 全市场排名后组内去均值 |
| `group_rank(subindustry)` + `INDUSTRY` 中性化 | ✅ **是 no-op**（组内排名被组内去均值抵消） | 等于什么都没做 |
| **`group_rank(subindustry)` + `MARKET` 中性化** | ❌ **不是** | 组内排名 → 全市场去均值 ⇒ **「相对同行强弱的全市场排序」**，这是新信息 |

★ **口径**：`group_rank(·, G)` 必须配**不包含 G 的中性化**。`subindustry ⊂ industry ⊂ market` ⇒ 只能配 `MARKET` / `NONE` / `STATISTICAL` / `SLOW*` / `FAST` / `CROWDING`，**不能配 `INDUSTRY` / `SECTOR` / `SUBINDUSTRY`**。

#### 三条已经写在牌面上的续攻方向

1. **`risk_neutralized_sharpe` 1.64 > S 1.42** ⇒ 按既有铁律「risk_neut > S = 真实信号被风格压制」，应换风险模型中性化（`STATISTICAL` / `SLOW_AND_FAST` / `FAST`）把被压的部分释放出来。⚠️ GBR 已证 `SLOW` 在该区反向（另一族 S 2.13→1.27），需实测。
2. **decay 4 → 10**：TO 仅 8.79%，提高 decay 主要作用是平滑信号噪声，可能同时抬 S 与 2Y。
3. **`CONCENTRATED_WEIGHT` 请复核**：`checks.warning` 里该项无 `value`，需 `get_alpha_details` 的完整 `checks` 或降低 truncation 复测才知道超限多少。

★ 因为 **F = S × √(returns/max(TO,0.125))**，在 returns 6.12% / TO 8.79% 下 `√(0.0612/0.125) = 0.6997` ⇒ **只要 S 提到 1.58，F 自动变成 1.105 ✅**。**所以唯一真正的目标是「把 S 从 1.42 抬 11%、2Y 抬 7%」，F 不用单独管。**

### 6.5 ★★★★★ 设置扫描：`decay` 是有效杠杆、`STATISTICAL` 反向 → 只剩两个真闸

**固定表达式** `multiply(group_rank(vec_avg(transaction_count_main), subindustry), -1)`，单因子改设置：

| alpha | 中性化 | decay | 算子变体 | **S** | **F** | TO | **2Y** | SUB | **margin** | returns | DD | failed | 备注 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `O0AwP2mp` | MARKET | 4 | group_rank | 1.42 | 0.99 | 8.79% | **1.48** | 1.55 | 13.94bp | 6.12% | 7.65% | 4 | 基线 |
| **`WjOw6QMZ`** | **MARKET** | **10** | group_rank | **1.46** | **1.04** ✅ | 5.17% | 1.44 | 1.54 | 24.53bp | **6.34%** | 7.85% | **2** | ★★★ **2Y 与 S 的最优折中** |
| `3qoYZ6lN` | MARKET | **16** | group_rank | **1.46** | **1.04** ✅ | **4.03%** | 1.43 | 1.53 | **31.61bp** | 6.36% | 7.73% | **2** | ★ **S 在此到顶**，margin 还在涨 |
| `1YNVQQbQ` | **STATISTICAL** | 4 | group_rank | 1.28 | 0.62 | 13.16% | 1.16 | 0.77 | 4.69bp | 3.09% | 3.29% | 4 | ❌ 全面变差 |
| `ZYQwelV1` | MARKET | 10 | **group_zscore** | 1.23 | 0.85 | 6.01% | **0.73** | 1.44 | 19.83bp | 5.96% | 9.56% | 4 | ❌ **2Y 崩到 0.73** |

★★★ **四条关键结论**：

**⓪ `group_zscore` 明确劣于 `group_rank`，且崩在 2Y（1.44 → 0.73）。** 机理：`group_zscore` 保留幅度信息，而 `transaction_count` 的幅度（是 1 笔还是 50 笔）含大量噪声——**一只股票某天借券放量 50 笔往往是一次性事件，不预示未来**；`group_rank` 只保留序关系，天然抗这种离群。
★ **定则：计数类（笔数、次数、人数）字段必须用 `rank`/`group_rank`，不要用保留幅度的 `zscore`。** 这与「金额族要用 zscore」正好相反——**因为计数是重尾离散量，金额是连续量。**

**① `decay` 是本族最强、且「顺带修好别的闸」的杠杆。** decay 4 → 10：

| 指标 | 变化 | 判读 |
|---|---|---|
| Fitness | 0.99 → **1.04** | ✅ **F 闸从「差 1%」变成「过闸」** |
| Margin | 13.94 → **24.53bp** | **+76%**，远超 GBR 75% 分位 16.2bp |
| failed_ra_count | 4 → **2** | 只剩 S / 2Y |
| **CONCENTRATED_WEIGHT** | `warning` → **`pass`** ✅ | ★ **decay 平滑顺带把集中度修好了**（不需要降 truncation） |
| Turnover | 8.79% → 5.17% | −41% |
| Returns | 6.12% → **6.34%** | **+4%（收益没被牺牲）** |
| Sharpe | 1.42 → 1.46 | +3% |
| 2Y | 1.48 → **1.44** | ⚠️ **−3%（唯一变差的项）** |

★ **与 memory 铁律的呼应**：memory 记「平台 decay 是换手治理的正确层」。本例进一步证明 **decay 不只治换手，还会顺带提升 F / margin / 集中度** —— 因为平滑减少了「同一天全仓换手」造成的权重突跳。**今后拿到「F 差 1~5%、CW 轻微超限、TO 尚可」的候选，第一动作应是 `decay ×2.5`，而不是动 truncation。**

**② `STATISTICAL` 中性化在 GBR 本族上显著反向**（S −13%、2Y −22%、margin −66%、F −40%）。**这补上了 memory 里「GBR 中性化 11 档」的又一格**：

| 中性化 | GBR 本会话实测结论 |
|---|---|
| `INDUSTRY` | 与 `group_rank` 组合是 **no-op**（见 §6.4） |
| `MARKET` | ★★★ **本族最优** |
| `SUBINDUSTRY` | 已证反向（`LLMO3l7n` 族 prod 更差） |
| `SLOW` | 已证反向（另一族 S 2.13→1.27） |
| `CROWDING` | 已证破坏 IS |
| `SECTOR` | 已证伪 |
| **`STATISTICAL`** | ★ **本族反向**（1.46→1.28）；但 `analyst7` / `pv47` 族曾正向 ⇒ **族属性，不可外推** |
| `FAST` / `NONE` / `SLOW_AND_FAST` / `REVERSION_AND_MOMENTUM` | 未测 |

**③ 只剩两个真闸，且都是「差 8~10%」的量级**：
`WjOw6QMZ` 的 `checks.fail = []`、`pass` 列表含 `LOW_FITNESS` / `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `CLUSTER_TEST` / `MATCHES_PYRAMID`，**`ra_failed_checks` 只有 `["LOW_SHARPE", "LOW_2Y_SHARPE"]`**，`failed_ppa_count = 0`。
- `LOW_SHARPE` 1.46 / 1.58 ⇒ **差 8.2%**
- `LOW_2Y_SHARPE` 1.44 / 1.58 ⇒ **差 9.7%**
- ⚠️ `risk_neutralized_sharpe` **1.70 > S 1.46** ⇒ 风险因子暴露仍在拖累；但 `STATISTICAL` 反向证明「换中性化」这条路在本族走不通。

**④ `decay` 的 S 曲线在 10 处到顶（1.42 → 1.46 → 1.46），但 margin 一路涨（13.94 → 24.53 → 31.61bp）。**
⇒ decay 已经把「可压的噪声」压完了。**S 从 1.46 往 1.58 的这 8% 不可能靠参数拿到，必须在结构层找新信息。**
⇒ 同时注意 **decay 与 2Y 反向**（4→1.48 / 10→1.44 / 16→1.43）：decay 越高，2Y 越差。
★★ **因此推荐的提交配置是 `decay 10`**（S/F 最优、margin 24.5bp 富余、2Y 只让 0.04）；**`decay 4` 只在「2Y 是唯一缺口」时才有意义**。
★ **`decay 16` 的 margin 31.61bp 极诱人但无意义**——margin 早已超过闸门要求，边际收益应投给 S / 2Y。

### 6.6 结构层续攻（参数层用尽后）

| 优先 | 假设 | 骨架 | 理由 |
|---|---|---|---|
| **P20** | **分组太细导致 rank 分辨率不足** | `group_rank(·, industry)` 替代 `subindustry` | GBR TOP700 下 `subindustry` 每组仅 5–15 只 ⇒ `group_rank` 输出量化为粗档位（0 / 0.11 / … / 1）⇒ **丢信息**。换 `industry`（更大组）提高 rank 分辨率 |
| **P19** | **NaN 缺口让部分股票缺席** | `group_rank(ts_backfill(vec_avg(tc), 22), subindustry)` | 借券记录非每日齐全；`ts_backfill` 补连续性可提高有效持仓数与时序稳定性 |
| P22 | 组轴再粗一档 | `group_rank(·, sector)` | 若 P20 证明「组越大越好」，继续放大 |
| P23 | 两个同源计数等权合成 | `add(rank(tc), rank(share))` 取负 | ⚠️ **须显式声明为「同概念合成」**（权重恒 1、不扫描）。P13 相消证明两者同源同向 ⇒ 合用理论上提 S；但相关性极高，预期增益只有 +2~8% |
| P24 | 平均单笔规模 | `rank(divide(vec_avg(tc), vec_avg(share)))` 取负 | 新经济量（每单位股数的成交笔数 = 拆单细度）；⚠️ 单位闸风险 |

### 6.7 ★★★★★ P21–P28：掩码（`if_else` 极端分位剔除）是本族唯一能推动**全期 S 过闸**的结构杠杆

#### 6.7.1 全账本（设置统一：GBR / TOP700 / D1 / `MARKET` / decay 10 / trunc 0.05 / nanHandling ON / maxTrade OFF）

| # | alpha | 骨架 | S | F | TO | 2Y | SUB | margin | returns | DD | failed | 结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P21 | **`O0AwERLd`** | `multiply(group_rank(ts_mean(vec_avg(tc),5), subindustry), -1)` | 1.49 | 1.06 | 4.10% | 1.34 | 1.55 | **31.16bp** | 6.38% | 7.41% | 2 | `ts_mean(·,5)` 平滑 = 净增益 |
| P23 | `WjOw6orQ` | 同上但 `loaned_share_count` 水平 | 1.17 | 0.80 | 4.36% | 0.73 | 1.39 | 26.60bp | 5.80% | 4.97% | 3 | 股数水平确认弱 |
| P24 | `gJeqpOAv` | `multiply(group_zscore(ts_covariance(v,v,22), subindustry), -1)` | 1.30 | 0.88 | 6.30% | **0.53** | 1.61 | 18.32bp | 5.77% | 6.88% | 3 | 时序二阶矩在全期偏弱 |
| **P25** | **`Xg9w6QQz`** | `if_else(greater(rank(ts_mean(v,5)), 0.9), nan, <P21>)` | **1.60** | **1.17** | 5.42% | 1.40 | **1.60** | 24.56bp | 6.66% | **4.83%** | **1** | ★★★ **全期 S 首次过闸** |
| P26 | `P0or9qmp` | 掩码 5 + 信号 `ts_mean(·,22)` | 1.55 | 1.10 | 4.00% | 1.34 | 1.62 | **31.77bp** | 6.35% | **4.08%** | 2 | 22 日过度平滑，2Y 反降 |
| **P27** | **`9qxP0K8V`** | **掩码 5 + 信号不平滑** | **1.56** | **1.14** | 6.64% | **1.51** | 1.59 | 19.97bp | 6.63% | 5.19% | 2 | ★★★ **双闸同时最接近（差 1.3% / 4.4%）** |
| P28 | `O0Awaog7` | 掩码改用**利用率代理** `rank(divide(vec_avg(share), cap))` | **1.21** | 0.75 | 5.99% | 1.16 | 1.19 | 16.13bp | 4.83% | 5.84% | 3 | ❌ **换字段做掩码暴跌 −24%** |
| P30 | `zq3wp8zK` | = P27 但 decay **4** | 1.54 | 1.11 | **10.59%** | **1.55** | 1.62 | **12.20bp** | 6.46% | 4.91% | 3 | 2Y 最优但 TO 翻倍 / margin 腰斩 |
| **P31** | `npvkVARw` | = P27 但掩码阈值 **0.8** | **1.36** | **0.93** | 7.81% | 1.39 | 1.33 | 15.07bp | 5.89% | **3.60%** | 3 | ❌ **收紧掩码全面崩** |
| P32 | 在飞 | = P27 但中性化 `REVERSION_AND_MOMENTUM` | — | — | — | — | — | — | — | — | — | 剔动量暴露（轧空年即极端动量年） |
| P33 | 在飞 | = P27 但中性化 `FAST` | — | — | — | — | — | — | — | — | — | 补全 GBR 中性化 11 档台账 |

★★★ **掩码强度曲线（唯一变量：`greater(rank(ts_mean(tc,5)), θ)`）：最优点精确落在 θ = 0.9**

| θ（砍掉分位） | alpha | S | F | 2Y | 判决 |
|---|---|---:|---:|---:|---|
| 无掩码 | `WjOw6QMZ` | 1.46 | 1.04 | 1.44 | 基准 |
| **0.9（砍 top 10%）** | **`9qxP0K8V`** | **1.56** | **1.14** | **1.51** | ★★★ **最优** |
| 0.8（砍 top 20%） | `npvkVARw` | 1.36 | 0.93 | 1.39 | ❌ 崩 |

⇒ **掩码是「窄带有效」杠杆**：砍 10% 恰好剔除轧空靶子而保留信号主体；砍 20% 就把信号本身削掉了（`group_rank` 的取值域被压到 [0,0.8] 再重新铺满 ⇒ 剩下的股票被迫承担全部权重，噪声股被放大）。**0.9 不是随便取的，是实测最优。**

★★ **decay 与 2Y 的权衡在本族已精确定量**（同掩码 0.9 + 不平滑）：

| decay | alpha | S | F | TO | 2Y | margin | failed |
|---|---|---:|---:|---:|---:|---:|---:|
| 4 | `zq3wp8zK` | 1.54 | 1.11 | **10.59%** | **1.55** | 12.20bp | 3 |
| **10** | **`9qxP0K8V`** | **1.56** | **1.14** | 6.64% | 1.51 | **19.97bp** | **2** |
| 16（早前测于平滑版） | — | 1.46 | — | — | 1.43 | 31.61bp | — |

⇒ **decay 4 能把 2Y 顶到 1.55（差 1.9%），但 S 掉到 1.54（差 2.5%）⇒ 变成「两闸各差一点」，比 decay 10 的单闸差 4.4% 更难。**
⇒ **decay 10 是本族的帕累托点**（S 最高、margin 富余、TO 健康、failed 最少）。

★★★ **参数层总判决：θ=0.9 与 decay=10 都已是最优，S 1.56 / 2Y 1.51 是「参数层可达的天花板」。** 剩余 1.3% / 4.4% 必须来自**中性化档位**（P32/P33 = GBR 11 档里唯二未测的 `REVERSION_AND_MOMENTUM` 与 `FAST`）。

#### 6.7.6 ★★★★★ 战略价值：`9qxP0K8V` 与现有 5 条篮子**完全正交**

`compute_mutual_correlation`（零配额，1021 点，years=4）：

| 对 | 相关 |
|---|---|
| `9qxP0K8V` ↔ `O0AKLMKq` | **−0.1114** |
| `9qxP0K8V` ↔ `vR1aEpa3` | **−0.0632** |
| `9qxP0K8V` ↔ `E56onL5r` | **+0.1729** |
| `9qxP0K8V` ↔ `j2YNnKOQ` | **−0.0754** |
| `9qxP0K8V` ↔ `d51O1kOX` | **+0.0279** |

`all_below_threshold: true`、`max_mutually_below_subset_size = 6`（含全部六条）、`max_pair = vR1aEpa3 ↔ E56onL5r 0.6954`。

★★★ **这条候选的价值远超「多一条 alpha」**：
1. 它与篮子的最大相关只有 **0.173**，是真正的**零相关新维度**（篮子内部已有 0.6954 的紧对，它比篮子内任何一条都更独立）。
2. 它是 **GBR/D1/SHORTINTEREST 塔的第一条**——过闸即点亮一座**全新塔位**（当前 `shortinterest = 0`）。
3. 它的信息源（借券笔数的参与广度 + 掩码剔除拥挤空头）与篮子（基本面会计 / 分析师修正 / 价量）**经济机制完全不同**。

⇒ **值得为它单独争取那 4.4% 的 2Y 缺口**，而不是转去开挖新的处女集。这是本会话「单位投入回报」最高的一条线。

★★★ **P28 反例（重要定则）：掩码字段必须与信号字段同源。**
同字段掩码（`rank(ts_mean(tc,5)) > 0.9` 砍笔数最高的 10%）→ S **1.60**；
换字段掩码（`rank(divide(share, cap)) > 0.9` 砍借出占比最高的 10%）→ S **1.21**，F 0.75，`failed_ra_count` 3。
机理：**同源掩码是对信号分布本身做非线性截尾**（砍掉信号最强的那一档，等于把「物极必反」直接刻进信号几何）；**异源掩码是在另一个维度上丢样本**，会连带丢掉有效信号——两个字段高度重叠但边界不同，被砍的股票既不是信号的极端档、又恰好是信号强的票。
⇒ **论坛帖 `43636685645975` 说的「利用率 ≥90% ⇒ 做空动能衰竭」若要用，必须让信号本身就是利用率，而不是拿它当别人的掩码。** 这条留给 T5 的第二形态（信号 = 利用率，掩码 = 同字段利用率），而不是 P28 这种「信号 = 笔数、掩码 = 利用率」。

★ **`Xg9w6QQz` 闸明细**：`checks.fail = [{LOW_2Y_SHARPE, 1.40/1.58}]` **仅此一项**；`checks.pass` 8 项含 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `CLUSTER_TEST` / `MATCHES_PYRAMID`；`failed_ppa_count = 0`；`risk_neutralized_sharpe 1.85 > S 1.60`；longCount 418 / shortCount 416；`pyramids = [{GBR/D1/SHORTINTEREST, 1.2}]`。

★★★ **`9qxP0K8V` 闸明细揭示平台判定分档**：`checks.fail = []`（**空**），但 `warning` 里仍有 `{LOW_SHARPE, 1.56/1.58}` 与 `{LOW_2Y_SHARPE, 1.51/1.58}`，`failed_ra_count = 2`。
⇒ **差距大才进 `fail`，差距小降级为 `warning` —— 但两者都计入 `failed_ra_count`，都拦提交。** 判「是否可提交」**只能看 `failed_ra_count == 0`**，不能看 `checks.fail` 是否为空。`risk_neutralized_sharpe 1.83 > S 1.56`。

★★ **平滑窗的单因子结论（同掩码 0.9，唯一变量是信号平滑窗）**：

| 信号窗 | alpha | S | F | 2Y | margin | DD |
|---|---|---:|---:|---:|---:|---:|
| 不平滑 | `9qxP0K8V` | 1.56 | 1.14 | **1.51** | 19.97bp | 5.19% |
| **5 日** | `Xg9w6QQz` | **1.60** | **1.17** | 1.40 | **24.56bp** | **4.83%** |
| 22 日 | `P0or9qmp` | 1.55 | 1.10 | 1.34 | 31.77bp | 4.08% |

⇒ **2Y 随平滑单调变差（1.51 → 1.40 → 1.34），S 在 5 日到顶（1.60），margin/DD 随平滑单调变好。**
⇒ **`ts_mean(·,5)` 是「S 与 margin 最优」，不平滑是「2Y 最优」**——两者不可兼得，只能按缺口选。**当前 2Y 是唯一缺口 ⇒ 选不平滑。**

#### 6.7.2 ★★★★★ 掩码的因果归因：救了 2016 轧空负年，代价是 2017

逐年对照（`O0AwERLd` 无掩码 → `Xg9w6QQz` 掩码 0.9）：

| 年 | 无掩码 | 掩码 0.9 | Δ | 判读 |
|---|---:|---:|---:|---|
| 2014 | 2.31 | 1.98 | −0.33 | 代价 |
| 2015 | 2.30 | 2.77 | **+0.47** | 收益 |
| **2016** | **−0.23** | **+0.45** | **+0.68** | ★★★ **轧空负年被治好** |
| 2017 | 2.11 | 1.14 | **−0.97** | ★★ 最大代价 |
| 2018 | 1.11 | 1.62 | +0.51 | 收益 |
| 2019 | 1.06 | 1.23 | +0.17 | 小收益 |
| 2020 | 2.06 | 2.06 | 0.00 | 中性 |
| 2021 | 2.31 | 2.16 | −0.15 | 小代价 |
| **2022** | 1.70 | 1.62 | −0.08 | 2Y 前半 |
| **2023** | **0.96** | **1.16** | **+0.20** | ★ 2Y 后半改善 |

★★★ **掩码设计意图被完全验证**：2016 从 **−0.23 → +0.45**（唯一负年翻正），DD 7.41% → **4.83%**。机理正是论坛帖「物极必反」——把「借券笔数最高 10%」（做空最拥挤、轧空靶子）踢出组合。
★★ **但最大代价在 2017（2.11 → 1.14）**，且 2022 略降 0.08 ⇒ 净效应仍是 S 1.49→1.60 / 2Y 1.34→1.40。
★ **2Y 缺口根因收敛到 2023 的 1.16**（2022 的 1.62 已接近闸）。要 2Y ≥ 1.58 需 2023 单年提到 **1.5+**。

#### 6.7.3 正交性实测（`compute_mutual_correlation`，零配额，1021 点）

| 对 | 相关 |
|---|---|
| `Xg9w6QQz` ↔ `O0AwERLd` / `WjOw6QMZ` / `3qoYZ6lN` / `O0AwP2mp` / `qMLko6b2` | **0.9086–0.9226** |
| `gJeqpOAv`（时序方差）↔ 上述六条 | **0.3772–0.6072** |

★ **掩码把同族相关从 0.985–0.999 压到 0.909–0.923**（−8 个百分点），方向正确但**仍 >0.7** ⇒ 与基础版只能取一条。
★★★ **`gJeqpOAv`（`ts_covariance` 时序二阶矩）与整个水平族完全正交（0.377–0.607）** ⇒ **这是本数据集上唯一被证实的独立第二维度**，只是单独用 S 只有 1.30 / 2Y 0.53，必须叠掩码才有资格。**P29 待派：方差信号 + 掩码。**

#### 6.7.4 ★★★★★ 论坛帖 `43624312881943` 的六条结论在 GBR 本族的复核结果

| # | 论坛（ASI/MINVOL1M）结论 | GBR 实测 | 判决 |
|---|---|---|---|
| 1 | `ts_delta(x,22)` 安慰剂 ≈ 0.09（纯噪声） | 本族 `ts_delta(loaned_share_count)` = **−0.09** | ✅ **跨数据集、跨字段完全一致** ⇒ 升级为借券域定则 |
| 2 | 卖方给的 `*_volatility` 是**截面**离散，**不是**时序波动 | 本族 `loan_rate_volatility` 5 结构最高 0.49 | ✅ 吻合（价内已含的维度弱） |
| 3 | 时序二阶矩要**自己做**（`ts_covariance(x,x,W)`），无分组 S 1.36 → 加 `exchange` 1.89 | 本族 `ts_covariance` = 1.30（无掩码） | ⚠️ **方向一致但强度不足**；GBR 无 `exchange` 字段，只能用 `subindustry` |
| 4 | `group_rank` 会丢二阶矩长尾，要用 `group_zscore` | 已按此办（P24 用 `group_zscore`） | ✅ 遵循 |
| 5 | `ts_covariance` vs `ts_std_dev` 在 robust 比例闸上一过一拦 | 本族两闸均未触发（`LOW_ROBUST_UNIVERSE_SHARPE` 在 pass 列表） | ⊘ **GBR TOP700 无 robust 闸** ⇒ 该结论不适用 |
| 6 | 嵌套分组轴（`country` 嵌在 `exchange` 内）是死参数 | 未测（GBR 无 `country` 字段） | ⊘ 不适用 |

★★ **第 1 条是本轮最有价值的跨数据集复核**：同一「变化率是噪声」定则，在 **ASI 的 `mean_loan_rate`** 与 **GBR 的 `loaned_share_count`** 上分别独立成立 ⇒ **§7.4「水平 vs 变化率」铁律从个案升级为借券域通用**。

#### 6.7.5 模板库 V2（结构互异 ≥10，按纪律标注来源）

| # | 模板 | 骨架 | 来源 | 状态 |
|---|---|---|---|---|
| T1 | 时序二阶矩 | `multiply(group_zscore(ts_covariance(v,v,22), subindustry), -1)` | forum `43624312881943` §3.1 | ✅ P24 = 1.30 / 2Y 0.53 |
| T2 | 时序二阶矩（std 对照） | `multiply(group_zscore(ts_std_dev(v,22), subindustry), -1)` | forum 同上 §5.2 | 待派 |
| **T3b** | **极端分位掩码（物极必反）** | `if_else(greater(rank(ts_mean(v,5)),0.9), nan, <T0>)` | forum `43636685645975` | ★★★ **P25 = 1.60 / 仅差 2Y** |
| T3a | 凸/凹曲率 | `multiply(signed_power(subtract(multiply(group_rank(v,subindustry),2),1), k), -1)` | forum 同上 §5.6 | 待派（`signed_power` 在 rank 后已证 no-op，风险高） |
| T4 | 「空头停止做空」 | `group_rank(divide(ts_sum(v,22), ts_sum(v,252)), subindustry)` | forum `43668758984983` / SSRN 4826241 | 待派 |
| **T5** | **利用率代理** | `if_else(greater(rank(divide(vec_avg(share),cap)),0.9), nan, <T0>)` | forum `43668003` | 🔄 **P28 在飞** |
| T6 | 单笔规模 | `multiply(group_rank(divide(vec_avg(value_usd), vec_avg(tc)), subindustry), -1)` | 自建（同单位相除） | 待派 |
| T7 | 出借账龄（平仓天数） | `multiply(group_rank(ts_mean(vec_avg(duration),22), subindustry), -1)` | forum `43636668` | 待派（水平已判死 0.01，22 日平滑后未测） |
| T8 | 线性加权平滑 | `multiply(group_rank(ts_decay_linear(vec_avg(tc),22), subindustry), -1)` | 自建（vs 等权 `ts_mean`） | 待派 |
| T9 | 最小费率 | `multiply(group_rank(ts_mean(vec_avg(min_loan_rate_main),22), subindustry), -1)` | 自建（唯一未测费率档） | 待派 |
| T10 | 双尺度双矩合成 | `multiply(group_rank(add(rank(tc), rank(ts_std_dev(tc,22))), subindustry), -1)` | 自建 | 待派（须声明「同概念合成」） |
| T11 | 参与度 × 时距 | `multiply(group_rank(multiply(vec_avg(tc), vec_avg(duration)), subindustry), -1)` | forum `43289952570903` | 待派（乘法量纲风险） |
| **T12** | **掩码 × 信号双尺度解耦** | 掩码 5 / 信号 22 | 自建 | ❌ P26 = 1.55 / 2Y 1.34（过度平滑） |

---

### 6.8 ★★★★★ P32/P33：**中性化 `FAST` 一次补齐双闸 —— 本会话首个 `failed_ra_count = 0` 的候选**

> 时间：2026-10-31 收官批。前置：P21–P31 已把「掩码 θ / decay / 平滑窗」三个参数层全部扫尽，
> 判定「S 1.56 / 2Y 1.51 是参数层天花板」，最后只剩两档中性化未测（`FAST` / `REVERSION_AND_MOMENTUM`）。

#### 6.8.1 单变量实验：同表达式，只换中性化

表达式（P27 原封不动）：
`if_else(greater(rank(ts_mean(vec_avg(transaction_count_main), 5)), 0.9), nan, multiply(group_rank(vec_avg(transaction_count_main), subindustry), -1))`

| # | alpha | 中性化 | S | F | TO | **2Y** | SUB | margin | returns | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P27 | `9qxP0K8V` | `MARKET` | 1.56 | 1.14 | 6.64% | 1.51 | 1.59 | 19.97bp | 6.63% | 5.19% | **2** |
| P32 | `e758RYgz` | `REVERSION_AND_MOMENTUM` | 1.67 | 1.18 | 8.92% | 1.60 | 1.49 | 13.88bp | 6.19% | 3.42% | **0** ✅ |
| **P33** | **`akK2vpWW`** | **`FAST`** | **1.95** | **1.33** | 11.79% | **1.96** | **1.62** | 9.91bp | 5.84% | **2.84%** | **0** ✅ |

★★★ **`FAST` 相对 `MARKET`：S +0.39（+25%）、2Y +0.45（+30%）、DD −2.35pp。**
两档未测中性化全部把 `failed_ra_count` 从 2 拉到 **0**。

`akK2vpWW` 的 `checks` 完整形态：
- `fail = []`
- **`pass` 9 项含 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_TURNOVER` / `HIGH_TURNOVER` / `CLUSTER_TEST` / `MATCHES_PYRAMID`**
- `warning` 只剩 `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`（非指标闸）
- `pending` = `SELF_CORRELATION` / `DATA_DIVERSITY` / `PROD_CORRELATION` / `REGULAR_SUBMISSION` / `POWER_POOL_CORRELATION`
- `ra.failed_ra_count = 0`、`ra.failed_ppa_count = 0`、`pyramid_short = "shortinterest"`
- `pyramids.list = [{name: "GBR/D1/SHORTINTEREST", multiplier: 1.2}]` ⇒ **SHORTINTEREST 塔从 0 → 1 的首条**

#### 6.8.2 ★★★★★ 十年覆盖（`get_alpha_yearly_stats`，逐年核 pnl / longCount / shortCount）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sharpe | 2.00 | **3.09** | 1.18 | **0.96** | 1.73 | 1.91 | 2.48 | 2.10 | 2.49 | 1.35 |
| pnl（万） | 56.8 | 88.7 | 35.3 | 20.0 | 54.9 | 54.9 | 88.7 | 66.8 | 95.8 | 41.0 |
| longCount | 453 | 502 | 503 | 527 | 492 | 464 | 434 | 437 | 462 | 447 |
| shortCount | 402 | 471 | 480 | 517 | 468 | 459 | 410 | 391 | 399 | 369 |

★★ **十年全部正 sharpe、无负年、无空年**，最弱 2017 的 0.96（且那一年 pnl 仍为正 20.0 万）。
对比 `MARKET` 版（`9qxP0K8V`）的 2016 = 0.37 / 2023 = 1.24，`FAST` 版把最弱两年抬到 1.18 / 1.35
⇒ **`FAST` 不是「把某一年拉爆换来的高 S」，而是把全曲线整体抬升**。

#### 6.8.3 ★★★★★ 篮子正交性：5 → **6**（`compute_mutual_correlation`，零配额，1021 点）

| 对 | r |
|---|---:|
| `akK2vpWW` ↔ `O0AKLMKq` | −0.0422 |
| `akK2vpWW` ↔ `vR1aEpa3` | −0.0158 |
| `akK2vpWW` ↔ `E56onL5r` | +0.2061 |
| `akK2vpWW` ↔ `j2YNnKOQ` | +0.0002 |
| `akK2vpWW` ↔ `d51O1kOX` | −0.0316 |

`max_mutually_below_subset` = **`[akK2vpWW, O0AKLMKq, vR1aEpa3, E56onL5r, j2YNnKOQ, d51O1kOX]`**
`max_mutually_below_subset_size = 6`、`max_subset_exact: true`、`max_pair` 仍是 `vR1aEpa3↔E56onL5r = 0.6954`（未变）
⇒ **篮子从 5 条无损扩到 6 条，加入者把最弱一环从 0.6954 之外再拉开一个负相关维度。**

★★ **三版同表达式（只换中性化）互相高度相关，只能取一条**：
`e758RYgz ↔ 9qxP0K8V = 0.9563`、`akK2vpWW ↔ e758RYgz = 0.8403`、`akK2vpWW ↔ 9qxP0K8V = 0.8160`。
⇒ 取指标最好的 `akK2vpWW`（`FAST`），另两条归档。

#### 6.8.4 ★★★★★ 新定则：`FAST` 中性化在 GBR 借券族上是**数量级杠杆**，不是微调

**跨数据集独立复核**：论坛帖 `43644505975959`（DEU/TOP500 分析师修正族）明确写
「中性化 `FAST` 最优（`SECTOR`/`MARKET` 略降，`SLOW_AND_FAST`/`SUBINDUSTRY` 明显恶化）」。
本次在 **GBR / TOP700 / shortinterest3 / 借券笔数** 上，`FAST` 同样优于 `MARKET` +0.39 S / +0.45 2Y
⇒ **「`FAST` 是慢变量计数/预期类信号的默认中性化」这一先验跨区域、跨 category、跨数据集成立。**

**机理**：`FAST` 剔除的是**快变风格因子**（短期反转、短期动量、短期波动）暴露。
借券笔数是**慢变量**（月度量级的供需），其截面排序里混入了大量「近期涨跌 → 借券活跃度」的快变量噪声；
`FAST` 把这层代谢掉，剩下的才是真信号。
`REVERSION_AND_MOMENTUM` 只剔反转+动量两项，太窄 ⇒ 效果介于 `MARKET` 与 `FAST` 之间，符合预期。

**应用纪律（新增）**：
1. 以后 GBR 上任何「**慢变量计数 / 预期 / 供需量**」族的候选卡在 S 或 2Y，**第一动作是换 `FAST`**，不是继续扫 decay/窗口。
2. `MARKET` / `INDUSTRY` / `SUBINDUSTRY` 是「行业/市场」维度的粗中性化；`FAST` 是「风格因子」维度的中性化，**维度不同，不能当作同一梯队比较**。
3. 反例边界仍有效：`STATISTICAL` 在本族**反向**（S 1.46→1.28）、`SLOW` / `CROWDING` / `SECTOR` 已证伪 ⇒ **不能推广成「换个中性化就能救」，只有 `FAST` 这一档被两次独立验证为正向。**

---

## §7 ★★★ 结论一：`The Loan Fee Anomaly` 在 GBR TOP700 不可复现 —— 但机制迁移成功

### 7.1 费率族全面失效（T1/T2/T6/T10 四个结构全灭）

论文（Engelberg-Reed-Ringgenberg, *Management Science*）宣称极端分位多空组合月毛收益 **1.17%**（2006–2019，剔除 $5 以下）。但用四个结构互异的模板测 `mean_loan_rate`：

| 结构 | alpha | S |
|---|---|---:|
| 水平 `rank` 取负（T1） | `1YNVbQmR` | **0.01** |
| 时序 z-score 取负（T2） | `KPJYdaNp` | 0.13 |
| 时序分位取负（T10） | `WjOwQ6rN` | −0.05 |
| 行业相对 `group_rank` 取负（T6） | `Xg9wQ6O8` | 0.41 |
| 费率极值 `max_loan_rate`（增量） | `d5W8V7r2` | 0.35 |

**五个结构，最高 S 0.41。**

**失效机理（不是「论文错」，是「栖息地不匹配」）**：论文的借券费率异象集中在**做空受限的小盘股**——Boehmer-Jones-Zhang 2008、Asquith-Pathak-Ritter 2005 全都是小盘效应。**GBR TOP700 是英国最大 700 只流动性股**，这些股票的借券市场深度极高、费率接近一般抵押利率 ⇒ **横截面方差被压塌，没有信息**。

★ 这与 `other545`（SUB 0.70/0.71 但主 S 负）是同一个失败模式：**信号栖息地 ≠ 投资域**。GBR 只有 TOP700 一个 universe，**无退路**。

### 7.2 ★★★★★ 但同一数据集里，**计数族**打出全会话最好的质量组合

| 字段族 | 代表字段 | 最佳 alpha | S | 判定 |
|---|---|---|---:|---|
| **计数（笔数）** | `transaction_count` | **`1YNVbmAQ`** | **0.88** | ★★★ **唯一有生命力的族** |
| 计数（评分序数） | `shrt3_bar` | `omEw5Mzb` | 0.23 | 弱但有 SUB 0.79 |
| 计数（股数） | `loaned_share_count` | `d5W8VAPx` | −0.09 | 无信号（**股数 ≠ 笔数**） |
| 费率极值 | `max_loan_rate` | `d5W8V7r2` | 0.35 | 弱 |
| 费率离散 | `loan_rate_volatility` | `A1VJZM2Q` | 0.49 | 弱（本族最高） |
| 费率水平 | `mean_loan_rate` | 五结构最高 0.41 | ≤0.41 | 判死 |
| 借券期限 | `average_loan_duration_days` | `O0AwPEdY` | 0.01 | 无信号 |

### 7.3 ★★★★★ 跨数据集铁律升级（第三次独立验证 → 收敛为定则）

此前在内部人领域两次验证「**金额族无信号、计数族有信号**」（USA wave237 `insider_trx_matrix` 价值族天花板 S 0.82 → 判死；计数族产出 `O0Jgd7Y7` S 2.27 / `88vJ1YKa` S 2.94 三颗全闸；USA wave238 `insider_agg_matrix` 价值族天花板 0.70 → 判死）。**现在在 SHORTINTEREST category 上第三次验证成功。**

★ 但本轮把这条铁律**精确化了一层**——「计数」本身还要再分：

| 计量 | 字段 | 语义 | S | 结论 |
|---|---|---|---:|---|
| **笔数 / 成交次数** | `transaction_count` | 借券成交笔数 | **0.88** | ★★★ **有信号** |
| 股数 / 规模量 | `loaned_share_count` | 出借股数 | −0.09 | ❌ 无信号 |
| 金额 | `loaned_market_value_usd` | 出借市值 USD | **未测**（本轮判死前未覆盖，见 §8） | 按铁律预期无信号 |
| 评分 / 序数 | `shrt3_bar` | 借券需求评分 1–10 | 0.23 | 弱 |
| 费率（价格） | `mean_loan_rate` | 费率 | 0.01 | ❌ 无信号 |

★★★ **修正后的铁律表述**：
> **「参与广度」有信号，「规模量」无信号。**
> 笔数（多少人/多少次参与）反映**广度**，天然分散、单笔噪声互相抵消；
> 股数 / 金额 / 市值反映**规模**，被少数大额参与者主导，持仓集中 ⇒ SUB 为负且信号无效。
> 费率 / 价格是**价格维度**，在流动性充分的市场（如 GBR TOP700）横截面方差被压塌。

★ 这与论坛帖 `43287696633239`（XC78928）的「**幅度 vs 广度**」论点完全同构：「幅度被单家机构噪音污染，广度是共识方向投票，单家噪音互相抵消」。**两条独立证据链在三个不同 category 上收敛到同一条定则。**

---

## §7.4 ★★★ P13 反向修正：铁律要加限定词 —— 「规模量的**水平**」也有信号，只有「**变化率**」无信号

P13 的表达式是 `subtract(rank(vec_avg(transaction_count_main)), rank(vec_avg(loaned_share_count_main)))`，即「笔数排位 − 股数排位」，`INDUSTRY`/decay10/trunc0.05。实测 **S −0.07 / F −0.01 / 2Y −0.45 / SUB −0.42 / margin −11.3bp**，全灭。

**这个「零」是极其重要的证据**（不是噪声，是**完全相消**）：

| 已知事实 | 数值 | 推论 |
|---|---|---|
| `rank(tc)` 单独（未取负） | S **−0.88** | 笔数排位与未来收益强烈负相关 |
| `rank(tc) − rank(share)` | S **−0.07** | 两者相减后几乎归零 |
| ⇒ 反推 `rank(share)` 单独 | ≈ **−0.81**（同向、同强度） | **股数的「水平」携带与笔数几乎等同的信号** |
| 对照：`ts_delta(share, 22)` 单独 | S −0.09（P3） | **股数的「变化率」无信号** |

★★★ **这是本数据集最反直觉的一条**：`loaned_share_count` 在 §7.3 表格里被我按「股数 = 规模量 ⇒ 无信号」判了，**但那个判断只测了它的 `ts_delta` 形态（P3），从没测过水平形态**。P13 的相消反推证明**水平形态很可能有 S ≈ 0.8 的信号**。

**修正后的铁律表述（第三版，以此为准）**：
> 区分「广度 vs 规模」还不够，必须再加一维「**水平 vs 变化率**」：
>
> | | 水平（level） | 变化率（delta / 差分） |
> |---|---|---|
> | **参与广度（笔数）** | ✅ 有信号（`tc` S 0.88） | 未测 |
> | **规模量（股数）** | ⚠️ **很可能有信号（反推 S≈0.81）** | ❌ 无信号（`share` Δ S −0.09） |
> | **金额（USD）** | 未测 | 未测 |
>
> **真正的分水岭不是「广度 vs 规模」，而是「水平 vs 变化率」。**
> 借券数据的**存量水平**（现在有多少股被借出、成交了多少笔）反映当前做空压力，有预测力；
> 而**流量变化**（这 22 天增了多少股）是噪声主导，无预测力。
> ⇒ 这与「价格水平 vs 价格变化」的经典区分同构：**水平 = 状态变量（state），变化率 = 噪声变量（noise）**。

★ **为什么 P13 的相消反而证明了两者都是真信号**：如果 `rank(share)` 是纯噪声，`rank(tc) − noise` 应当保留大部分 S ≈ −0.8；实测归零说明两者**高度共线且同向**。**相消是一种「同源探测」——两条腿打平意味着它们量的是同一件事。**

★★ **这给出两条可立即执行的动作**：
1. **`N(rank(vec_avg(loaned_share_count_main)))` 应当补测**（此前从未测过它的水平形态）——如果 S ≈ 0.8，它是一条与 P14 高度相关但**独立的信息源**，可作扩量候选或做 `vector_neut` 正交化的分母。
2. **`N(rank(vec_avg(loaned_market_value_usd_main)))`（金额水平）也应补测** —— 按同逻辑很可能也有信号。
3. ❌ **不要再做「笔数 − 股数」这类相减**：两条腿同源，相减必然归零。**这是本数据集上的固定反面模式。**

★★★ **对跨数据集铁律（§7.3）的最终影响**：`insider` 域的两次判死（价值族天花板 0.82 / 0.70）测的都是**金额的水平形态**，所以那条结论**依然成立**（金额水平在 insider 域确实弱）。但**不能外推成「股数水平也无信号」** —— 本数据集的反推证据正好相反。**两域的区别在「谁在卖」：insider 的 USD 金额被个别高管巨额单笔主导；借券股数是市场-wide 的机构行为，天然分散。**

---

## §8 待办与判死状态

### 8.1 本数据集当前状态：**未判死，转入 `transaction_count` 深度挖掘**

10 条探针、8 个结构、字段覆盖 `_main` 档 6 个不同字段（`mean_loan_rate` / `shrt3_bar` / `loaned_share_count` / `loan_rate_volatility` / `average_loan_duration_days` / `max_loan_rate` / `transaction_count` = **7 个**）。按 §5「同族同度量」豁免（三档后缀是同度量不同聚合），覆盖率 = 7 / 9 族 = **78%** ✅ 满足 ≥50%。

但**不判死**——P10 的 S 0.88 / F 0.57 / SUB 1.48 / margin 17.05bp 是一条活线索，只是 2Y 0.25 卡住。**判死与继续挖掘的分野在于能否把 2Y 拉起来。**

### 8.2 围绕 `transaction_count` 的增量计划（按优先级，含实测结果）

| 优先 | 骨架 | 表达式 | 状态 | 结果 |
|---|---|---|---|---|
| ~~P11~~ | 异常借券活动（时序 z） | `N(rank(ts_zscore(vec_avg(transaction_count_main), 252)))` | ✅ 已测 | `1YNVbXXk` S 0.81 / F 0.37 / **2Y 1.60 ✅** / DD 4.73% —— **2Y 修好了但 returns 腰斩**，见 §6.2 |
| ~~P12~~ | 后缀稳健性 | `N(rank(vec_avg(transaction_count_p5_d1)))` | ✅ 已测 | `88Rk9jjq` S 0.86 / F 0.55 / 2Y 0.30 —— **与 P10 逐位同档**，见 §6.3 |
| **P13** | ★ 广度减规模残差 | `subtract(rank(vec_avg(transaction_count_main)), rank(vec_avg(loaned_share_count_main)))` | ✅ 已测，**判死** | `KPJYj3vz` **S −0.07 / F −0.01 / 2Y −0.45 / SUB −0.42** ⇒ 相减把信号抵消掉了，见下方 §7.4 |
| **P14** | ★★★★★ **组内排名（最优字段 × 最优结构）** | `N(group_rank(vec_avg(transaction_count_main), subindustry))`（`MARKET`/decay4/trunc0.05） | ✅ **已测，全会话最佳** | **`O0AwP2mp` S 1.42 / F 0.99 / 2Y 1.48 / SUB 1.55 / margin 13.94bp / DD 7.65%，三闸各差 1~10%** —— 见 §6.4 |
| **P15** | decay 单因子（4→10） | 同 P14，`MARKET`/decay**10**/trunc0.05 | 🔄 在飞 `45bXkuf0…` | 平滑信号噪声，抬 S 与 2Y |
| **P16** | 中性化单因子（风险模型） | 同 P14，`STATISTICAL`/decay4/trunc0.05 | 🔄 在飞 `2eGDEjc7…` | ★ `risk_neut 1.64 > S 1.42` ⇒ 释放被风格压制的部分 |
| P17 | 时序分位 | `N(rank(ts_quantile(vec_avg(transaction_count_main), 252)))` | 待派 | 反 CDF 骨架 |
| P18 | 平均单笔规模倒数 | `N(rank(divide(vec_avg(loaned_share_count_main), vec_avg(transaction_count_main))))` | 待派 | 大单 vs 碎单；⚠️ 单位闸风险（股/笔） |
| P19 | 金额族对照 | `N(rank(vec_avg(loaned_market_value_usd_main)))` | 低优先 | 按 §7.3 铁律预期无信号，只作铁律第 4 次验证 |
| P20 | 尾部加权 | `N(rank(signed_power(vec_avg(transaction_count_main), 3)))` | 低优先 | 论文「异象集中在极端分位」；P14 已是更优解 |
| P21 | 裸档后缀梯度 | `N(rank(vec_avg(transaction_count)))` | **取消** | §6.3 已证后缀同源，无信息增量 |

★★★ **优先级已被 P14 完全重排**：P14 之后唯一的任务是「**把 S 从 1.42 抬到 1.58、2Y 从 1.48 抬到 1.58**」，F 会自动跟随（见 §6.4 末段公式）。**所有与「提升 S」无关的骨架（P17–P21）全部降级或取消。** P13 若结果好，可作第二条独立候选（扩量用），但不再作为主线。

### 8.3 已判死（**不要重测**）

- **`mean_loan_rate` 全族**（水平 / 时序 z / 时序分位 / 行业相对 / 极值）= 5 个结构最高 S 0.41
- **`average_loan_duration_days`**（S 0.01，2Y 0.72 但全期零信号 = 时间非平稳）
- **`loaned_share_count` 的 `ts_delta` 形态**（S −0.09）
- **`loan_rate_volatility`** 本族最高 0.49，但离闸 68% ⇒ 低优先，不主动加仓

### 8.4 ★ 方法论沉淀：`investability_ratio` 在 S≈0 时是陷阱

P1 的 `investability_ratio = 4.00`、P5 的 `−9.00` —— 看起来惊人，实际是 `invest_S / S` 在 S≈0 时（0.04/0.01、−0.09/0.01）分母坍塌。
★ **判据修正：`investability_ratio` 只在 `|S| > 0.5` 时才可解读。** 否则只看 `investability_sharpe` 的绝对水平（P1 的 0.04 / P5 的 −0.09 都接近零，说明信号在流动票里同样是零）。

### 8.5 ★★★★★ 塔位可达性终局判决：SHORTINTEREST 塔**结构上无法点亮**（2026-10-31 实证）

**判据不是「还差 2 条 alpha」，而是「能不能产出 3 条互相关 < 0.7 的 alpha」。答案是否。**

**证据一：25 个字段里只有 1 个活。**
`get_datafields(GBR/TOP700/D1, dataset_id="shortinterest3")` 实测 25 字段，但按后缀 `_main` / `_p5_d1` / 裸名分档后，实际只有 **9 个语义字段**：

| 语义字段 | 状态 | 依据 |
|---|---|---|
| **`transaction_count`** | ✅ **唯一活字段** | `akK2vpWW` S 1.95 / `O0AwP2mp` S 1.42 |
| `mean_loan_rate` | ❌ 全族死 | §8.3，5 结构最高 S 0.41（Loan Fee Anomaly GBR 不可复现） |
| `average_loan_duration_days` | ❌ 死 | §8.3 S 0.01；**本轮 2026-10-31 用 `if_else` 掩码 + `group_rank` 骨架重测 `O0Awrdev` 仍只有 S 0.70 / 2Y 0.52 / SUB 0.28 / failed_ra 4** |
| `loan_rate_volatility` | ❌ 死 | §8.3 最高 0.49 |
| `loaned_share_count` | ⚠️ 只 `ts_delta` 形态死 | 水平形态与 `transaction_count` 同族（都是借券活动规模） |
| `loaned_market_value_usd` | ⚠️ 金额族 | 按 §7.3 铁律预期无信号 |
| `max_loan_rate` / `min_loan_rate` | ⚠️ `mean_loan_rate` 的极值分支 | 同族 |
| `shrt3_bar` | ⚠️ 未充分测 | 1–10 借券需求评级，本质是**拥挤度代理**，与 `transaction_count` 同机制 |

**证据二：同一活字段、换骨架也无法去相关 —— `corr = 0.7611`。**

| 对 | 骨架差异 | 4 年窗互相关 |
|---|---|---:|
| `akK2vpWW` ↔ `O0AwP2mp` | 前者 `if_else(greater(rank(ts_mean(·,5)),0.9), nan, -group_rank(·,subindustry))` + FAST/decay10；后者 `group_rank(·,subindustry)` + MARKET/decay4 | **0.7611** ❌ |

`compute_mutual_correlation` 输出 `all_below_threshold = false` / `max_mutually_below_subset_size = 1`。
⇒ 掩码、组内排名、中性化、decay 全换过，仍是同一条信号。

**证据三：本数据集无兄弟数据集可换。**
`get_datasets(category="shortinterest", GBR/TOP700)` 返回 **只有 `shortinterest3` 一个**。而决策 #70（★★★★★「去相关唯一有效的维度是换数据集」）在此彻底失效 —— 没有第二个数据集可换。

**⇒ 终局判决：SHORTINTEREST 塔（倍率 1.2）最多贡献 1 条 alpha（`akK2vpWW`），塔位永远停在 1/3。不要再为「点亮 SHORTINTEREST」投入任何批位。**

**方法论沉淀（可跨区迁移）：判断某塔能否点亮，正确的问题顺序是**
1. 该 category 下有**几个**有覆盖的数据集？（GBR shortinterest = 1 ⇒ 已是危险信号）
2. 该数据集有**几个**语义上互不相同的活字段？（shortinterest3 = 1）
3. 若活字段数 < 3 且无兄弟数据集 ⇒ **结构不可达，直接放弃该塔**，不要先算「还差几条」。

**本条与 news 塔成功的对照**：NEWS 塔能出 4 条，靠的正是「**2 个数据集（news17 + news18）× 各自多个活字段**」。news17 一个数据集就出了 3 条（`vec_sum(event_relevance)` / `vec_count(relevance)` / `vec_count(event_sentiment_score)`），因为它的多实体族是条件性填充，换字段即换子集（决策 #79）。**shortinterest3 是 MATRIX→VECTOR 的完整填充结构，没有这个性质。**
