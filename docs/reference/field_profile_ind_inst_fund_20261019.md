# IND Institutions / Fundamental · 字段画像 / 适用模板 / 实测指标（2026-10-19）

> **用途**：`_fieldprofile-nonanalyst-20261018.md` 的续篇，专补 **institutions6 / fundamental94 / fundamental1** 三集，并**修正 earnings3 的误判**。
> **读法**：先看 §0 总表定位 → 跳到目标集的 ② 拿模板 → 用 ③ 的实测值判断值不值得发批。
> **上游**：`field_profile_ind` 视图（`data/wqb.db`，画像权威源）＋ 本轮实测（wave376–wave392，共 87 条）。
> **命名**：跨类别补充文档（`_` 前缀，非 cells.json 类别文件，否则 `test_profiles_layer.py` 判红）。

## §0 三集总表（实测裁决速查）

| 数据集 | 语义 | 类别 | 字段 | cov | 频率 | **实测裁决** | 本轮条数 |
|---|---|---|---|---|---|---|---:|
| **`institutions6`** | 13F 机构持仓（量/价/家数） | INSTITUTIONS | 11 | 0.992 | **季度** | **ALIVE×4**（S 3.18–3.45），同集残差化在测 | 40 |
| `fundamental94` | 标准季度财务报表 | FUNDAMENTAL | 38 | 0.876–0.996 | **季度** | S 到 **1.58**（ROE），但 **rob 0.43 封顶**（S↔rob 剪刀差） | 30 |
| `fundamental1` | 高管薪酬/董事会治理 | FUNDAMENTAL | 118 | 0.563 | **年度** | **判死**（44 条最高 S 0.51，周期错配） | 44 |

**⚠ 修正 1（earnings3 误判）**：SKILL 2026-10-17 已修正——`earnings3` 的 `*_interval`（间隔天数）是 **ALIVE**（`ern3_pre_interval` S **4.49** / F 3.25 / TO 0.337 / n=19；`ern3_next_interval` S **3.03** / F 1.91 / TO 0.209 / n=15），只有 `*_reptime`（timestamp）才是 DEAD。此前「整集毒药」是把两者混为一谈，**误判**。

**⚠ 修正 2（选类别已无区分度）**：IND 11 塔已全亮（2026-10-18 实测）⇒ 选类别不再带来塔位收益，ATOM 价值只在 alpha 收益 × multiplier。**「打未点亮塔」这个前提本身已失效。**

---

## §1 institutions6 —— 13F 机构持仓

### ① 字段画像

- **字段类型**：11 个全部 **MATRIX**（可直接 `ts_*`，无 VECTOR）。
- **覆盖率**：全部 **0.9915–0.9924**（全库最高档之一）。
- **更新频率**：**季度**（13F 披露，季内数值不变）⇒ 低频指纹，TO 天然 0.06–0.13。
- **分布特征**：绝对金额（美元）+ 家数（计数）；须构造无量纲比率或残差才有信号。
- **可用性**：aCnt 44–2499，拥挤度中等。
- **画像权威源判定**（`field_profile_ind`）：**ALIVE × 4 / WEAK × 1 / DEAD × 2 / UNTESTED × 4**。

| 字段 | 语义 | cov | 画像 | best_s | best_2y | best_sub | best_f | TO |
|---|---|---|---|---|---|---|---|---|
| `aggregate_share_count_institutions` | 机构持股总股数 | 0.992 | **ALIVE** | **3.45** | 1.10 | 1.85 | 2.34 | 0.3307 |
| `count_institutional_buyers_security` | 买入机构家数 | 0.992 | **ALIVE** | **3.23** | 1.32 | 1.39 | 2.17 | 0.0842 |
| `quantity_institutional_shares_acquired` | 机构买入总股数 | 0.992 | **ALIVE** | **3.19** | 1.35 | 1.45 | 2.06 | 0.0915 |
| `count_institutional_holders_security` | 持有机构家数 | 0.992 | **ALIVE** | **3.18** | 0.61 | 1.44 | 2.00 | 0.0936 |
| `market_value_institutional_shares_acquired` | 机构买入总市值 | 0.992 | WEAK | 1.10 | 0.63 | — | 0.63 | 0.0931 |
| `aggregate_equity_value_institutions` | 机构持股市值 | 0.992 | DEAD | 0.88 | 0.81 | — | 0.43 | 0.0897 |
| `count_institutional_sellers_security` | 卖出机构家数 | 0.992 | DEAD | 0.32 | −0.15 | — | 0.12 | 0.0422 |
| `aggregate_equity_value_all_owners` | 全体持股市值 | 0.992 | UNTESTED | — | — | — | — | — |
| `aggregate_share_count_all_owners` | 全体持股股数 | 0.992 | UNTESTED | — | — | — | — | — |
| `market_value_institutional_shares_disposed` | 机构卖出总市值 | 0.9915 | UNTESTED | — | — | — | — | — |
| `quantity_institutional_shares_disposed` | 机构卖出总股数 | 0.992 | UNTESTED | — | — | — | — | — |

### ② 适用模板

```text
# T1 同集内残差化（ATOM 兼容，★本轮主推）
# 两个字段都来自 institutions6 ⇒ 不破 ATOM；SKILL 证明残差化族能过 prod 墙
rank(-ts_regression(ts_zscore(ts_backfill(<F1>, 120), 252),
                    ts_zscore(ts_backfill(<F2>, 120), 252), 252, rettype=0))   # decay=126
# 推荐配对：股数↔市值（量价背离）、买家↔卖家（净买入方向）、
#           买入股数↔买入市值（大单/小单结构）、机构↔全体（机构占比的时序残差）

# T2 季频变化（ts_delta 63 天 = 1 季，唯一有效的时序算子）
group_rank(ts_delta(<F>, 63), sector)

# T3 无量纲比率（横截面）
rank(divide(subtract(<buyers>, <sellers>), add(<buyers>, <sellers>)))    # 净买入强度
rank(divide(<机构>, <全体>))                                            # 机构占比

# T4 按规模分组（剥离市值暴露，提 robust）
group_rank(<F>, bucket(rank(aggregate_share_count_all_owners), range="0,1,0.2"))
```

### ③ 回测结果及指标

**本轮实测（wave376–378，30 条，全部 FAIL）**：裸量类 S ≤ 1.10｜`ts_delta(250)` **周期错配**（季频数据 250 天跨 2 季，多条 S=0.00 / TO 0.000）｜比率类 S ≤ 0.43｜长窗平滑 / subindustry 轴 / power 1.5 均无效。

**画像 best_s 3.18–3.45 的来源未明**（`skeleton_fams` 为空）⇒ 本轮 wave392 用**同集内残差化**（SKILL 证明能过 prod 墙的族）重测这 4 个 ALIVE 字段，结果待收。

**已排除**：`ts_delta(250)`（周期错配）、裸 `rank` 水平量、跨集残差（`returns` 属 PV ⇒ 破 ATOM）。

---

## §2 fundamental94 —— 标准季度财务报表

### ① 字段画像

- **字段类型**：38 个全部 **MATRIX**。
- **覆盖率**：0.698–0.9956（`qta` 0.9958 / `qttld` 0.9943 / `qqec` 0.9946 / `qtl` 0.9955 / `qol` 0.9952 最高；`qdrx` 0.698 最低）。
- **更新频率**：**季度**（前缀 `fnd94_q_`）⇒ 比 fundamental1 的年度高 4 倍，`ts_delta(63)` 有效。
- **分布特征**：**全部是绝对金额（水平量）**，必须构造无量纲比率。
- **可用性**：aCnt 44–609，不拥挤。

| 报表 | 字段（摘） | 构造的因子 |
|---|---|---|
| 资产 | `qta`(总资产) `actq_q`(流动资产) `cheq_q`(现金) `rectq_q`(应收) `qtvni`(存货) `ppentq_q`(固定资产净) `qlwdg`(商誉) | 周转率 / 现金比率 |
| 负债 | `qtl`(总负债) `qtcl`(流动负债) `qcld`(短期债务) `qttld`(长期债务) `qpa`(应付) | 杠杆率 |
| 权益 | `qqec`(普通股权益) `qer`(留存收益) | ROE / 留存收益比 |
| 利润 | `saleq_q`(销售) `cogsq_q`(销货成本) `qpdaio`(营业利润) `qin`(净利润) `qdrx`(研发) `qpd`(折旧) | 毛利率 / 营业利润率 / ROA / 研发强度 |

### ② 适用模板

```text
# T1 盈利能力（S 最高，但 rob 是死穴）
rank(divide(fnd94_q_q_qin, fnd94_q_q_qqec))                       # ROE，S 1.46
winsorize(rank(divide(fnd94_q_q_qin, fnd94_q_q_qqec)), std=0.2)   # ★ S 1.46→1.58
rank(ts_zscore(divide(fnd94_q_q_qin, fnd94_q_q_qqec), 252))       # ★ 2Y 1.26→2.57

# T2 盈利动量
rank(ts_delta(divide(fnd94_q_q_qin, fnd94_q_q_qta), 63))          # ROA 变化，2Y 1.79

# T3 规模中性化（唯一能提 rob 的手段，但触发 S↔rob 剪刀差）
group_rank(<因子>, bucket(rank(fnd94_q_q_qta), range="0,1,0.2"))   # rob −0.06→0.43，S 1.58→1.37
vector_neut(rank(<因子>), rank(fnd94_q_q_qta))                     # 正交化剥离规模
```

### ③ 回测结果及指标

| 结构 | S | 2Y | sub | **rob** | 裁决 |
|---|---:|---:|---:|---:|---|
| `rank(ROE)` | 1.46 | 1.26 | 0.53 | −0.06 | S/rob=24 |
| `winsorize(rank(ROE), std=0.2)` | **1.58** | 1.05 | 0.51 | −0.06 | S 达闸线 |
| `rank(ts_zscore(ROE,252))` | 1.27 | **2.57** | 0.69 | 0.20 | 2Y 翻倍 |
| ROE 按总资产 5 档 | 1.40 | 1.46 | 0.43 | −0.10 | 剪刀差 |
| ROE 按总资产分组（最优） | 1.37 | **2.47** | **1.16** | **0.43** | **rob 封顶 0.43** |
| ROA | 1.19 | 0.92 | 0.32 | −0.19 | — |
| ROA 变化 | 0.97 | 1.79 | 0.54 | 0.19 | 2Y 过闸 |

**★ 核心结论**：`winsorize(std=0.2)` 与 `ts_zscore(252)` 是两个独立杠杆（分别管 S 和 2Y），但**换轴对 rob 完全无效**（与 analyst 族上 sector 提 rob +0.21 相反）。规模中性化能把 rob 提到 0.43（塔最高）、sub 提到 1.16，但 S 同步降到 1.37 ⇒ **按趋势外推 rob 到 1.0 需 S≈1.0，与 S 闸 1.58 冲突 ⇒ ROE 机制在 IND 结构性不可达**。

---

## §3 fundamental1 —— 高管薪酬/董事会治理（判死）

### ① 字段画像

- **字段类型**：118 个**全部 VECTOR**（必须 `vec_avg`，裸用秒拒）。
- **覆盖率**：0.5621–0.5632（**43% 缺失**，全库最低档）。
- **更新频率**：**年度报告**（字段一年只变一次）。
- **分布特征**：薪酬金额、任职年数、学历数、年龄、离散度（`stdev*` 族）。
- **可用性**：aCnt **0–25**（真空区，但低 aCnt ≠ 有信号）。
- **画像权威源**：**UNUSABLE × 118**（SKILL 早已记录，本轮实测确认）。

### ② 适用模板（已试，均无效）

```text
# 全部 44 条实测的结构族：
rank(ts_mean(ts_backfill(vec_avg(<F>), 120), 22))      # 水平量 → S ≤ 0.49
rank(ts_delta(ts_backfill(vec_avg(<F>), 250), 250))    # 年度周期错配 → 多条 S=0.00/TO=0.000
group_rank(..., sector)                                 # 横截面 → S ≤ 0.34
divide(vec_avg(<F>), vec_avg(<stdev>))                  # 分歧度分母 → S ≤ 0.09
log / sqrt / sign / ts_ir / ts_scale / ts_sum           # 算子族 → 全部退化
ts_corr / group_mean / group_sum / group_count          # 算子族 → S ≤ 0.51
```

### ③ 回测结果及指标

| 批次 | 结构 | 最好 S | 淘汰原因 |
|---|---|---:|---|
| wave380 探针 | 水平量 ×10 | 0.49 | 水平量无信号（符合铁律） |
| wave381 结构 | `ts_delta(250)`+薪酬+比率 | 0.12 | **周期错配**：年度字段 250 天内 delta≈0（TO 0.000 铁证） |
| wave383 算子B | `ts_corr`/`group_mean`/`log`/`sqrt`/`sign` | 0.51 | 年度恒定值上算子退化为常数 |
| wave384 横截面 | `group_rank(sector)`+分歧度分母 | 0.34 | 横截面也无超额 |

**★ 可复用规律**：**年度/季度低频数据 + 时序算子 = 死路**。低频字段只有三类手法有效：①`days_from_last_change`（距上次变化天数，但该算子在 IND 不可用）②`ts_rank` 长窗（≥756）③**纯横截面算子**。若横截面也无信号（如 fundamental1），则该集结构性无解。

---

## §4 算子可用性（本轮新增实测，IND）

| 算子 | 可用性 | 备注 |
|---|---|---|
| `ts_ir` / `ts_scale` / `ts_sum` / `trade_when` | ✅ | 语法注意见下 |
| `ts_corr` / `ts_covariance` / `ts_delay` | ✅ | 双年度字段上稀疏 |
| `group_mean` / `group_sum` / `group_count` | ✅ | `group_mean(x, weight, group)` 三参数 |
| `group_backfill` | ✅ | **group 参数必须用内置 `sector`**，不接受 `bucket(...)`（报 `Unit[Group:1]`） |
| `log` / `sqrt` / `sign` | ✅ | 年度恒定值上退化为常数 |
| `ts_kurtosis` / `tail` / `kth_element` / `days_from_last_change` / `ts_arg_max` | ❌ **平台不可用** | 三次整批 ERROR 隔离后判定；`get_operators` 中 `level` 为 null |
| `trade_when` 第三参数 | ⚠ | **必须是条件表达式**（如 `less(x,-1)`），写常量 `-1` 会整批 ERROR |
| `hump` 第二参数 | ⚠ | 必须命名 `hump=0.05` |
| `normalize` | ⚠ | 无 `useStd` 参数 |

**累计已验证算子：38 / 103。**

---

## §5 earnings3 —— 财报日历 interval（本轮实测，含画像复现校准）

### ① 字段画像（`field_profile_ind`）

| 字段 | 语义 | type | cov | 画像 verdict | 画像 best_s | 画像 best_2y | **本轮实测 S** |
|---|---|---|---|---|---|---|---|
| `ern3_pre_interval` | 距上次财报天数 | MATRIX | 0.8721 | ALIVE | **4.49** | 1.48 | **0.70**（复现成功） |
| `ern3_next_interval` | 距下次财报天数 | MATRIX | 0.7094 | ALIVE | **3.03** | 1.08 | 负 |
| `ern3_pre_reptime` | 上次财报**时间戳** | MATRIX | 0.8721 | DEAD | 0.86 | 0.42 | 0.86（历史） |
| `ern3_all_delay_1_pre_interval` | delay1 版 pre | MATRIX | 0.872 | DEAD | 0.58 | 0.35 | — |
| `ern3_next_reptime` / `ern3_all_delay_1_next_reptime` | 时间戳 | MATRIX | 0.709 | DEAD | 0.40 / 0.45 | | — |
| `ern3_all_delay_1_next_interval` / `ern3_all_delay_1_pre_reptime` | — | MATRIX | 0.709 / 0.872 | DEAD | 0.01 / −0.20 | | — |

### ② 适用模板（★ 唯一有效的构造 = 二阶 delta 事件加速度）

```text
# 历史最优（本地库 blbproEK：S 0.70 / F 0.24 / 2Y 1.48 / TO 0.4717 / rob 0.30）
(-1) * (rank(ts_delta(ts_delta(ern3_pre_interval, 5), 5)))

# 机理：ern3_pre_interval 每日递减 1 ⇒ 一阶 delta 恒为 −1（常数，无信号）；
#       只有财报日跳变（重置为大值）⇒ 二阶 delta 精确捕捉「财报事件」本身。
# 变体：group_rank(..., sector)｜winsorize(rank(...), std=0.2)｜窗 10/21｜ts_zscore(63)
```

### ③ 回测结果及指标（本轮 30 条）

| 结构族 | 最好 S | 淘汰原因 |
|---|---:|---|
| `ts_mean(22)` + `ts_backfill(120)` 平滑（wave393） | 0.03 | **过度平滑**：TO 仅 0.091–0.137（画像 TO_med 0.3374），事件时钟被抹平 |
| 裸值 / `ts_delta(5)` / `ts_rank(63)` / 时钟差 / 时钟进度比（wave394） | 0.08 | 阶跃计数横截面差异不足 |
| **二阶 delta 族**（wave395，10 条变体） | **0.70** | 复现历史成功，但 S 远低于闸线；TO 0.472 触发 HIGH_TURNOVER |

**★ 核心结论（可复用校准）**：**`field_profile_ind` 的 `best_s` 不可尽信，必须本地复现验证。** `ern3_pre_interval` 画像记 `best_s=4.49`，但本地库历史最高仅 0.86、本轮 30 条实测最高 0.70 ⇒ 画像该值可能来自不同 universe/settings 或记录口径差异。**判死前用 `backtest_results` 交叉验证画像 best_s。**

**★ earnings3 累计 30 条判死**：interval 字段实际可用强度 S ≈ 0.70–0.86，距闸线 1.58 太远。

---

## §6 本轮战场总账（Institutions / Fundamental / Earnings）

| 数据集 | 类别 | 条数 | 最好 S | 结论 |
|---|---|---:|---:|---|
| `institutions6` | INSTITUTIONS | 87 | 1.10 | **判死**（同集内残差化 S 0.41） |
| `fundamental1` | FUNDAMENTAL | 44 | 0.51 | **判死**（年度周期错配；画像 UNUSABLE×118） |
| `fundamental94` | FUNDAMENTAL | 40 | 1.58 | **判死**（rob 封顶 0.43，S↔rob 剪刀差） |
| `earnings3` | EARNINGS | 30 | 0.70 | **判死**（二阶 delta 复现 S 0.70） |

**★ 未点亮塔可用性尽调**：`option`（`option1`/`option30` description 实为 RIC↔BBGID 映射，cov 0.36–0.40）｜`insiders`（`insiders5` 是韩国公司数据，`insiders1` 是标识符映射 cov 0.388）｜`shortinterest`（`shortinterest5` 是沪深港涨跌停数据，非印度）⇒ **这三类的数据集在 IND 实质不可用**，非挖掘能力问题。

**★ 低频数据规律**：年度/季度字段 + 时序算子 = 死路（周期错配，TO 0.000 为铁证）；低频字段只有 `days_from_last_change`（IND 不可用）/ `ts_rank` 长窗 / 纯横截面算子三类手法，若横截面也无信号则结构性无解。
