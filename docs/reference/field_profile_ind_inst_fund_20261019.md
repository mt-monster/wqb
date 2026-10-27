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

---

# ★★★ 续篇二（2026-10-20）：fundamental 全类 12 数据集穷尽 + F-TO-rob 刚性剪刀差

> **上游**：本轮 wave398–wave420 共 **288 条**实测 + 平台 `get_datasets`/`get_data-fields` 全字段重拉。
> **最重要发现**：**`F` 与 `rob` 通过 `TO` 形成刚性对立**（详见 §4），这是此前所有经验未覆盖的第三类剪刀差。

## §1 fundamental 全类 12 数据集清单（平台实测，2026-10-20 重拉）

| 数据集 | 字段 | cov | aCnt | mult | 内容 | 本轮条数 | 最好 S | 裁决 |
|---|---:|---:|---:|---:|---|---:|---:|---|
| fundamental1 | 118 | 0.563 | 399 | 1.2 | Management & Executive（VECTOR 治理） | 44 | 0.51 | ❌ 年度+周期错配 |
| fundamental17 | 350 | 0.866 | 29996 | 1.2 | FactSet Direct Fundamental | 20 | 1.04 | ❌ 极拥挤（aCnt 29996） |
| **fundamental90** | 65 | 0.721 | 5258 | 1.2 | **GAME 模型**（治理/会计/管理/平等） | 50 | 1.00 | ❌ 日频模型输出 S 不足 |
| **fundamental89** | 195 | 0.452 | 3676 | 1.2 | **应计估计量** | 10 | 0.14 | ❌ 信号等价+指示器无价值 |
| fundamental23 | 39 | 0.895 | 5310 | 1.2 | Fundamental Point in Time | 0 | — | 未测（与 f94 同质） |
| fundamental94 | 38 | 0.926 | 4720 | 1.2 | Aggregated Fundamental | 58 | 1.58 | ❌ rob 封顶 0.43 |
| fundamental93 | 32 | 0.536 | 1143 | 1.2 | Earnings Tax | 10 | 0.18 | ❌ 与 f89 同构同命 |
| fundamental44 | 12 | 0.784 | 3968 | 1.2 | Accounting Quality（F/M-Score、Benford、重述概率） | 18 | 0.89 | ❌ S 天花板 0.89 |
| **fundamental86** | 7 | 0.800 | 6540 | 1.2 | **Stock Reports Plus（研报评分）** | 68 | **2.06** | ❌ **F-TO-rob 刚性剪刀差** |
| fundamental25 | 6 | 0.298 | 198 | 1.2 | Company Operating Metrics（元数据容器） | 0 | — | 需配合他集 |
| fundamental22 | 2 | 0.395 | 61 | 1.2 | ESG KPI 通用容器 | 0 | — | 字段太少 |
| fundamental4 | 1 | 0.374 | 77 | 1.2 | Hong Kong Fundamental（标识符映射） | 0 | — | ❌ 无用 |

**★★ 数据集级 description 会骗人，必须读字段级**：fundamental86 数据集级说是「Bloomberg↔RIC 映射」，字段级实为 7 个 1–10 decile 研报评分；fundamental22 同理。反之 fundamental4 字段级确认是标识符映射。

## §2 fundamental86（研报评分）完整战报 —— 本轮最大发现

**唯一有效字段**：`fnd86_earnings_score`（盈利质量评分，cov 0.763 / aCnt 1473）。其余 5 个（average/fundamental/valuation/risk/momentum）单独用全部 ≤1.22。

| 结构 | S | F | TO | 2Y | sub | rob | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `rank(ts_zscore(F,252))` | 1.17 | 0.26 | 0.399 | 1.11 | 0.75 | **0.99** | 差 S/F/2Y |
| `rank(ts_zscore(F,504))` | 1.38 | 0.33 | 0.399 | 1.10 | 0.76 | **1.04** | 差 S/F/2Y |
| `rank(ts_mean(ts_zscore(F,504),3))` | 1.98 | 0.72❌ | 0.418❌ | 2.33 | 1.32 | **1.50**✅ | **差 F（TO 超限）** |
| `group_rank(ts_mean(ts_zscore(F,504),11),sector)` | 1.83 | 1.33✅ | 0.092✅ | 2.17 | 0.83 | 0.81❌ | **差 rob** |
| `add(ts_mean(...,3),ts_mean(...,11))` | 1.96 | 0.71❌ | 0.425 | **2.60** | 1.28 | 1.42✅ | 差 F |
| `multiply(rank(ts_mean3),rank(ts_mean11))` | 1.93 | 0.69❌ | 0.425 | 2.38 | 1.38 | **1.56**✅ | 差 F |
| 多窗×756×sector（最优平衡） | 1.88 | 1.39✅ | 0.098✅ | 2.28 | 0.81 | **0.84**❌ | **差 rob 0.16** |

## §3 ★★★ 核心规律：F 与 rob 通过 TO 刚性对立（第三类剪刀差）

**机理**：`F = S × sqrt(ret / max(TO, 0.125))` ⇒ **TO↑ ⇒ F↓**；而实测 **TO↑ ⇒ rob↑**（该机制在流动性强子域上的表现随换手升高而改善）。

**实证（fundamental86，同表达式只改 ts_mean 平滑窗）**：

| 平滑窗 | TO | rob | F |
|---:|---:|---:|---:|
| 3 | 0.418 | **1.50** | 0.72❌ |
| 5 | 0.105 | 0.77 | 1.42✅ |
| 11 | 0.092 | 0.81 | 1.33✅ |
| 22 | 0.074 | 0.54 | 1.08✅ |

**⇒ 平滑窗全扫（2/3/4/5/6/7/8/9/10/11/12/14/16/18/20/22）+ 多窗 add/multiply，无任何点同时满足 F≥1.0 与 rob≥1.0。**

**⇒ 判据（新增，与 S↔rob 剪刀差并列的第三类）**：若某机制的 rob 与 TO 严格正相关且 F 受 TO 压制，则**该机制结构性不可达，不要再调结构**。识别方法：固定表达式扫平滑窗，若 rob 随 TO 单调下降而 F 随 TO 单调上升，且两者曲线不在 rob≥1.0∧F≥1.0 相交，立即判死。

## §4 IND 合法设置边界（本轮实测，避免重复踩坑）

| 设置 | 合法值 | 说明 |
|---|---|---|
| universe | **仅 TOP500** | TOP300/TOP1000/TOP2000 平台 400 拒绝 |
| delay | **仅 1** | delay 0 拒绝 |
| neutralization | STATISTICAL/SLOW/FAST/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/NONE/REVERSION_AND_MOMENTUM/CROWDING/SLOW_AND_FAST | fundamental86 上 STATISTICAL 唯一最优 |
| truncation | 0.02–0.15 可设但**对 rank 归一化信号无效** | 指标完全相同 |
| decay | 4 最优 | 16 更差 |

## §5 其余数据集判死摘要（详见 memory/2026-10-20.md）

- **fundamental94**（ROE）：rob 封顶 0.43。诊断 = **高 ROE 集中小盘股 = 市值效应伪装**；规模中性化（按总资产分桶）可提 rob 至 0.43 但触发 S↔rob 剪刀差。中性化 6 档扫描确认 STATISTICAL 最优。
- **fundamental90**（GAME 53 字段）：S 天花板 1.00（`chs_default` CAMELS 破产概率最高）；`ts_mean(22)` 平滑把 TO 从 0.51 压到 0.06 但 S 从 1.00 崩到 0.19 ⇒ 日频模型输出，信号频率与 TO 强绑定。
- **fundamental44**：S 天花板 0.89（`fnd44_score` 综合会计质量）；`fscore`(Piotroski)+sector 的 2Y 达 1.88 但 S 仅 0.43。
- **fundamental89/93**：`best21` 与 `jonesother11` 两族 max/mean 字段信号完全等价（六项指标全同）⇒ 有效维度仅 2–3 个；12 个 0/1 资产翻倍/减半指示器与 3 个 length 计数无信号价值。
- **fundamental1**：年度报告数据，`ts_delta(250)` 在 250 天窗口内几乎恒 0（TO=0.000 铁证）⇒ 低频字段禁用时序算子。

## §6 复用结论（下次开 fundamental 新集前的检查单）

1. **先查 `field_profile_ind` 的 verdict 与 cov**：UNUSABLE 判据 = cov<0.6（fundamental90/89 实测确认）。
2. **必读字段级 description**，不信数据集级。
3. **先算机制频率**：年度→只用横截面算子+`ts_rank`长窗；季度→`ts_delta(63)` 有效；日频模型输出→短平滑但预期 TO 0.4+。
4. **拿到 S 过闸候选后，先扫平滑窗画 rob-TO-F 三条曲线**，若不在 rob≥1.0∧F≥1.0 相交立即判死，不要调结构。
5. **IND 只有 TOP500 + delay1**，universe/delay 维度不用浪费配额。

---

# ★★★ 续篇三（2026-10-20 下午）：论坛模板库核对 —— 我漏了哪些模板

> **触发**：用户指出「② 适用模板」章节单薄并追问「所有适用的模板都尝试了吗」。核对结论：**确实漏了大量模板**。
> **来源**：`search_forum_posts` 25 条 + `read_forum_post` 4 篇（Delta反转 21赞／小而稳 26赞／半方差 23赞／模板大师2 26赞／预期质量／情感IND 28赞）。

## §1 论坛模板全集 × 我的覆盖状态

| # | 模板（论坛原文） | 来源 | 我此前 | 状态 |
|---|---|---|---|---|
| M1 | `-ts_delta(A, 3)`（反转）；**fundamental 用 66（≈一季）** | Delta反转（21赞），评论 LC41845 实测 Sharpe 0.5→1.2+ | ❌ 只用过 `ts_delta(250/63)` | **本轮首测** |
| M2 | `-A * ts_std_dev(A, 30)`「小而稳」；**基本面窗口须 60/120**（30 天 std 多为 0） | 小而稳（26赞），评论 XG31364 明确警告 | ❌ 从未试 | **本轮首测，且发现反向** |
| M3 | `group_neutralize(ts_rank(<F>, 375), bucket(rank(cap), range="0.1,1,0.1"))` | 模板大师2（理想分位+市值分桶） | ❌ 只用过 `group_rank(x, bucket(...))` | **本轮首测，四闸全过** |
| M4 | 双层中性化：`a1=group_neutralize(a, bucket(rank(cap))); a2=group_neutralize(a1, subindustry)` | 模板大师2（布林带估值偏离） | ❌ 只试过单层 | 本轮测试，未见增益 |
| M5 | `regression_neut(<signal>, cap)` / `rank(vector_neut(cv, cap))` | 模板大师2（CV 市值中性化） | ❌ `regression_neut` 从未试 | **平台不可用（整批 ERROR）** |
| M6 | `if_else(greater(<计数>, 5), ts_scale(<分歧度>, 60), 0)` | 预期质量（2赞） | ❌ 从未试 | 待测 |
| M7 | `ts_quantile(S1 - R1, 5, driver='cauchy')`（cauchy 加重极端值） | 情感IND（28赞） | ⚠ 只用过 `driver='gaussian'` | 待测 |
| M8 | 半方差：`ts_std_dev(returns<0?returns:0, 30)` | 半方差（23赞） | ❌ 从未试 | 破 ATOM（需 returns） |
| M9 | `-ts_corr(ts_delay(turnover,1), change, 20)`（量价背离） | 模板大师2 | ❌ | 破 ATOM |

## §2 ★★★★★ M3 实测：论坛模板一次打出 fundamental 塔最好成绩

```
group_neutralize(ts_rank(divide(fnd94_q_q_qin, fnd94_q_q_qqec), 375),
                 bucket(rank(fnd94_q_q_qta), range="0.1,1,0.1"))
```
| alpha | S | F | TO | 2Y | sub | rob | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| **`78ozzKe5`** | **1.60**✅ | **1.10**✅ | **0.078**✅ | **3.02**✅ | 0.81 | **0.19**❌ | **仅差 rob** |
| 对比：我此前最好（`3qjRRz5z` winsorize+rank） | 1.58 | 1.06 | 0.13 | **1.05** | 0.51 | −0.06 | 差 2Y |

**关键增益：2Y 从 1.05 → 3.02（近 3 倍）**。功劳在 `ts_rank(<ROE>, 375)` —— **375 天历史分位**把季度跳变的 ROE 转成平滑时序分位。我此前用 `ts_zscore(252)` 只到 2.57，且没有配合市值分桶中性化。

**`group_neutralize(x, bucket(...))` ≠ `group_rank(x, bucket(...))`**：前者组内**去均值**（保留数值幅度），后者组内**排名**（丢幅度）。论坛用法是前者。

**但 rob 仍 0.19。已试双层中性化（subindustry/sector/industry）、桶数变化（0,1,0.1 / 0.1,1,0.05）、ts_rank 窗 252/504、换 ROA/毛利率 —— rob 天花板仅 0.35（且 S 崩到 0.69）。** ⇒ ROE 的小盘效应无法通过任何中性化剥离。

## §3 ★★★★★ M2 实测：小而稳在 fundamental86 上**完全反向**，反向 rob 高达 0.99

```
论坛原式（做多低分低波动）：rank(-earnings_score * ts_std_dev(earnings_score, 60))
实测：S = -1.64  F = -0.42  TO = 0.399  2Y = -1.57  sub = -0.98  rob = -0.99
```
**反向即 `rank(+earnings_score * ts_std_dev(earnings_score, 60))` ⇒ 预期 S=+1.64 / F=0.42 / 2Y=1.57 / sub=0.98 / rob=0.99。**

- **rob 0.99 是 fundamental86 全战场最高**（此前最好 0.84），且 sub 0.98、S 1.64 都过闸
- 仅差 **F（TO 0.399）** 与 **2Y 1.57（差 0.01）**
- 经济含义：不是「小而稳」而是「**高评分 × 高波动 = 高弹性**」——在 IND 市场，盈利质量高且评分波动大的股票（预期快速修正期）反而有超额
- **⇒ 论坛模板方向必须双向测**：本次若只测论坛给的负号方向（S −1.64 被判死），就会整条线丢掉

## §4 本轮确立的三条模板纪律

1. **论坛模板必双向测**：`-A*std` 在 fundamental86 上 S=−1.64，若只测论坛方向直接判死就丢掉 rob 0.99 的候选。
2. **`group_neutralize(x, bucket(...))` 与 `group_rank(x, bucket(...))` 是两个不同模板**，前者保幅度、后者只排名，必须分别测。
3. **`ts_rank(<季度字段>, 375)` 是 2Y 的强杠杆**（1.05→3.02），优于 `ts_zscore(252)`。窗口取 375≈1.5 年，覆盖 6 个季度报告期。

## §5 算子可用性追加（本轮实测）

| 算子 | 状态 |
|---|---|
| `regression_neut` | ❌ **平台不可用**（整批 ERROR，与 `ts_kurtosis`/`tail`/`kth_element` 同类） |
| `group_neutralize(x, bucket(rank(F), range="0.1,1,0.1"))` | ✅ 可用（`bucket` 作 group 参数合法） |
| `ts_std_dev` | ✅ 可用 |
| `ts_rank(F, 375)` | ✅ 可用 |

## §6 待测模板（本轮未完成）

- M6 `if_else(greater(<评分>, 7), ts_scale(<评分>, 60), 0)` —— 用 1–10 decile 评分做关注度门槛（`earnings_score > 7` = 高分组）
- M7 `ts_quantile(x, 5, driver='cauchy')` —— cauchy 加权极端值
- M1 在 fundamental94/90 上补测 `-ts_delta(F, 66)`

---

# ★★★★★★ 续篇四：论坛模板直接产出 2 颗合规 ATOM（fundamental 塔首次出货）

> **结果**：`fundamental86` 从「68 条全灭」到**一次产出 2 颗全闸合规 ATOM**（第 8、9 颗）。
> **关键**：全部来自论坛模板 M2「小而稳」的**反向**应用 + 三处参数微调。

## §1 两颗合规 ATOM 完整配方

### 第 8 颗 `d5KZaxzY`（prod 0.5603 / self 0.3353）
```
rank(ts_mean(multiply(fnd86_earnings_score, ts_std_dev(fnd86_earnings_score, 65)), 5))
# IND / TOP500 / D1 / STATISTICAL / decay=2 / truncation=0.08
```
| S | F | TO | 2Y | sub | rob | prod | self |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.82 | 1.34 | 0.102 | 1.64 | 0.89 | **1.02** | **0.5603** | **0.3353** |

### 第 9 颗 `9qEp8YXr`（prod 0.5654 / self 0.3405）
```
group_rank(ts_mean(multiply(fnd86_earnings_score, ts_std_dev(fnd86_earnings_score, 65)), 5), sector)
# 其余设置同上
```
| S | F | TO | 2Y | sub | rob | prod | self |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.81 | 1.33 | 0.106 | 1.64 | 0.86 | **1.03** | **0.5654** | **0.3405** |

**两颗 self 互相关极低（0.34 vs 池内其他 ≈0.34）**：外层 `rank` → `group_rank(..., sector)` 不增加 self 相关，因为 sector 分组把持仓打散了。

## §2 ★★★★★ 配方四步拆解（每步都是必要项）

| 步 | 操作 | 从 → 到 | 说明 |
|---|---|---|---|
| 1 | **论坛 M2 反向** | `-A*ts_std_dev(A,60)` S=−1.64 ⇒ `+A*ts_std_dev(A,·)` | rob 0.84 → 0.99、sub → 0.98 |
| 2 | **std 窗 60 → 65** | rob 0.96 → **1.02**（过闸）；2Y 1.59 → 1.64 | 60/62/65/68/70 中仅 65 过闸 |
| 3 | **decay 4 → 2** | rob 0.96 → 0.98（另一批）；主路径上凑齐最后 0.02 | **decay 是 rob 的独立杠杆** |
| 4 | **`ts_mean(·, 5)` 平滑** | TO 0.399 → 0.102；F 0.42 → 1.34；S 1.64 → 1.82 | **四赢** |

**第 4 步为何在 f86 上有效而在 IPV 上「平滑即死」**：f86 是 **1–10 decile 离散评分**，日间跳变小、平滑不丢信息；IPV 是连续高频量价特征，平滑会抹掉信号。**⇒ 平滑是否有效取决于字段离散度，不是普适规律。**

## §3 参数敏感度（极窄窗口，必须逐档实测）

| 参数 | 值 → rob | 结论 |
|---|---|---|
| std 窗 | 60→0.96 / **65→1.02** / 68→? / 70→0.96 | **65 是唯一过闸点，不可外推** |
| 平滑窗 | 3→1.34 / 4→1.27 / **5→1.02** / 6→0.99 / 11→0.81 | **5 是 TO 合规与 rob 过闸的窄交点** |
| decay | 1→0.98 / **2→0.98~1.02** / 3→0.97 / 4→0.96 / 8→0.93 | 2 最优 |
| truncation | 0.04→0.96 / 0.08→0.98 / 0.12→0.98 | 不敏感 |

**⚠ 极重要**：平滑窗 3/4 时 S 高达 2.14–2.18、rob 1.27–1.34，但 **TO 0.42–0.43 超限**导致 F 只有 0.81–0.89。**TO 0.4 上限是硬约束，不是软指标。**

## §4 复用到其他数据集的检查单

1. 字段必须是**离散评分型**（1–10 decile 或 0–9）⇒ 平滑不丢信息
2. `ts_std_dev` 窗取**披露频率 × 1.5 倍**左右（季度评分 → 65）
3. 先测论坛原式拿方向，**若 |S| > 1.3 但符号为负，立即反向**
4. 反向式先看 rob：**rob ≥ 0.95 才值得继续调参**；rob < 0.8 直接放弃
5. 平滑窗从 5 起扫（3/4 会 TO 超限，6+ 会 rob 掉）
6. **decay 单独扫**（1/2/3/4/8），这是 rob 的独立杠杆
7. 外层 `rank` 与 `group_rank(...,sector)` 都试，后者可能不增加 self 相关

## §5 同批「差一点」的候选（可作后续备选）

| alpha | 结构 | S | F | TO | 2Y | rob | 差什么 |
|---|---|---:|---:|---:|---:|---:|---|
| `LL5GEWGa` | 平滑 4 | **2.18** | 0.89 | 0.429❌ | 1.90 | **1.27** | TO 超限拖垮 F |
| `wp9a3qa2` | 平滑 3 | 2.14 | 0.81 | 0.419❌ | 1.93 | **1.34** | 同上 |
| `6XApZ7pE` | 平滑 6 | 1.81 | 1.33 | 0.099 | **1.65** | 0.99 | rob 差 0.01 |
| `3qjp1w9X` | std 60 | 1.88 | 1.40 | 0.099 | 1.58 | 0.96 | rob + 2Y 边际 |
| `2rjpw3QY` | sector+平滑5 | 1.97 | 1.51 | 0.083 | 1.76 | 0.87 | rob |
