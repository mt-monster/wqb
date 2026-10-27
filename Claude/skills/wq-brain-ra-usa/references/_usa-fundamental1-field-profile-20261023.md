# USA / D1 / TOP3000 — `fundamental1` 董事会与高管数据字段画像（2026-10-23）

> 目标第 2 步交付件。取数：`get_datafields(dataset_id=fundamental1, region=USA, delay=1, universe=TOP3000)`。
> 平台字段数 **205**，sharpe 过滤移除 **26**，可用 **179**（`complete=true`, `pages_fetched=5`）。
> 全部字段类型 = **VECTOR**（0 个 MATRIX）⇒ 所有表达式必须先过 `vec_*` 聚合。

## 1. 数据集身份

| 项 | 值 |
|---|---|
| id / 名称 | `fundamental1` / Board & Executive Data（BoardEx 式披露） |
| 覆盖 / 可用字段 / 用户 | 0.412 / 179（平台 205） / 低（多数字段 userCount 0–6） |
| **数据集级 aC** | **359**（低拥挤前沿；与已交付 5 颗分析师族零共享字段） |
| 更新频率 | **年度**（`as of the selected annual report date`）：年报披露后才变，期间靠 `nan_handling=ON` / `ts_backfill` 延续 |
| 金字塔 | `USA/D1/FUNDAMENTAL`（未点亮，multiplier 1.1 / effective 1） |

## 2. 结构：三层 × 六个构造族

### 2.1 董事会级聚合（`fnd1_filtered_*` / `fnd1_board_characteristics_*`，覆盖最高 0.798–0.800）

| 族 | 代表字段 | 覆盖 | 语义 |
|---|---|---:|---|
| 规模 | `fnd1_filtered_numberdirectors` | 0.7984 | 执行董事人数 |
| 结构 | `fnd1_filtered_genderratio` | 0.7984 | 男性执行董事占比（越高 = 越不多元） |
| 结构 | `fnd1_filtered_stdevage` / `stdevnoquals` | 0.7981 / 0.7984 | 年龄 / 学历离散度 |
| 结构 | `fnd1_filtered_succession` | 0.7984 | 年龄向退休年龄聚集度（继任风险） |
| 任期 | `fnd1_board_characteristics_timebrd` | 0.7999 | 董事平均在职年数 |
| 任期 | `..._filtered_avgtimeothco` | 0.7984 | 在其他上市公司董事会的平均任职年数（外部经验） |
| 任期 | `..._filtered_timeretirement` | 0.7981 | 距退休时间 |
| 兼职 | `fnd1_board_characteristics_filtered_totnounlstdbrd` | 0.798 | 执行董事累计任职的**非上市**董事会数（注意力稀释） |
| 兼职 | `fnd1_board_characteristics_filtered_totnolstdbrd` | 0.7984 | 累计任职的上市董事会数（aC 0） |

> ⚠ **命名陷阱（2026-10-23 实测，代价 = 整批 10 臂全灭）**：`fnd1_filtered_*` 只有 **6 个**成员
> （`numberdirectors` / `genderratio` / `stdevage` / `stdevnoquals` / `succession` / `attrition3yr`）。
> 其余"filtered"字段挂在 **`fnd1_board_characteristics_filtered_*`**（董事会级）与
> **`fnd1_director_characteristics_filtered_*`**（个人级）下，两者前缀只差一个词、语义差一层聚合。
> 手写 `fnd1_filtered_noquals` / `fnd1_filtered_totnounlstdbrd` 这类"看着该存在"的名字，平台会回
> `Attempted to use unknown variable` 并 **CANCELLED 同批其余 8 条**（不是只废那一条）。
> ⇒ 发批前必须用 `get_datafields` 的 `id` 原样复制，禁止凭语义拼名。

### 2.2 流失 / 更替族（核心信号面）

| 字段 | 覆盖 | aC | 语义 |
|---|---:|---:|---|
| `fnd1_filtered_attrition3yr` | **0.6715** | **30** | 近 3 年离开的执行董事占比 |
| `director_attrition_ratio_3yr` | 0.6828 | 14 | 同构（另一 vendor 口径） |
| `director_attrition_ratio` | 0.5019 | 2 | **近 1 年**流失占比 |
| `fnd1_attrition3yr` / `fnd1_attrition` | 0.2772 / 0.2459 | 9 / 23 | 仅执行董事子集口径 |

### 2.3 个人级（`*_director_characteristics_*`，0.30–0.80）

单董事的任期 / 学历 / 兼职数。因是 VECTOR，`vec_avg` 给出"全体董事平均"，与 2.1 的董事会级聚合高度重叠 ⇒ **本波不重复使用**，只作后备。

### 2.4 薪酬 / 期权族（覆盖 0.16–0.32，多数 aC = 0）

| 字段 | 覆盖 | 语义 |
|---|---:|---|
| `wealth_sensitivity_to_stock` | **0.1952** | 股价每变动 1% 时董事财富变动额（**pay-for-performance delta**） |
| `equity_linked_compensation_ratio_2` | 0.1784 | 权益薪酬占比 |
| `compensation_change_percent_2` | 0.1775 | 总薪酬同比变化 |
| `total_director_cash_comp` | 0.2078 | 现金薪酬总额 |
| 期权明细（`option_*` / `unexercisable_*` / `exercisable_*`） | 0.001–0.30 | 多数 `<0.05` 且 aC 0，**不可用** |

**结论**：薪酬/期权族只有 `wealth_sensitivity_to_stock` 一个字段值得测（构念独特），其余是**覆盖率陷阱** —— aC 0 且覆盖率个位数百分比，`group_rank` 后只剩少数标的，必挂 CW / SUB。

### 2.5 标识符族（`*_id`，覆盖 0.317）——**不可用**：纯 ID，无经济含义。

## 3. 硬约束：VECTOR 算子面只有 7 个

平台实测（`get_operators`，103 算子）Vector 类 = `vec_avg / vec_sum / vec_max / vec_min / vec_stddev / vec_range / vec_count`。
**没有 `vec_last`** ⇒ 无法只取"最新一期年报"，所有信号都是**缓冲级聚合**（多年平均）。
对年度数据这不是折扣而是**平滑**：`vec_avg` 把多年董事会状态平均后，信号更慢、更稳，但也更可能与规模/行业共线。

⚠ 论坛帖（43789987978263）列出的 `vec_ir / vec_skewness / vec_kurtosis / vec_percentage / vec_powersum`
在平台**只以 COMBO-only 的 `reduce_*` 存在**，REGULAR 拿不到（波 86 §8.3 已实测确认）。

## 4. 分布特征：**未实测**（诚实标注）

未跑 Labs ⇒ 没有分布形态 / 离群 / 非零率实测。已知先验：
- 计数类（董事人数、兼职数）是小整数，`group_rank` 会有**大量并列**（同组内同值）；不影响方向，但会影响换手与极端权重。
- 比率类（attrition、genderratio）预期 0–1。
- `wealth_sensitivity_to_stock` 是**美元量纲且右偏**（大公司/大股东更高）⇒ 与规模强共线，`group_rank` 只能去掉单调部分，**不能去掉规模的非线性部分**；若最强，必须先做规模中性化对照。

## 5. 可用性与 ATOM 判定

- **ATOM 合格**：全部 179 字段同属一个数据集。
- **首选面 = 流失族**（aC 30/14/2，覆盖 0.50–0.68）与**董事会结构族**（覆盖 0.80）。
- **避坑**：期权明细族（覆盖 <0.05）；ID 族；`*_2` 后缀的重复口径（同构字段，选一个即可，避免同波内互为近似复制品）。

## 6. 波 87 设计（10 臂，一臂一机制；每臂一个待答问题）

设置：USA / TOP3000 / D1，**decay 0**（年度数据换手天然低，decay>0 会击穿 LOW_TURNOVER 0.01），truncation 0.08，INDUSTRY，nanHandling ON，pasteurization ON，unitHandling VERIFY，maxTrade OFF，2014-01-01→2023-12-31。

| # | 字段 | 构念（文献） | 符号 | 待答问题 |
|---|---|---|---|---|
| 1 | `fnd1_filtered_numberdirectors` | 董事会规模（Yermack 1996：小董事会估值更高） | − | 大董事会是否折价 |
| 2 | `fnd1_filtered_attrition3yr` | 3 年高管流失（组织不稳定） | − | 长期流失是否负向 |
| 3 | `director_attrition_ratio` | 1 年高管流失 | − | **短周期流失是否更有效**（与 #2 对照） |
| 4 | `fnd1_filtered_succession` | 继任风险（年龄向退休聚集） | − | 关键人风险是否被定价 |
| 5 | `fnd1_board_characteristics_timebrd` | 董事任期（Vafeas 2003：超长任期 = 堑壕） | − | 堑壕效应 vs 经验效应，谁主导 |
| 6 | `fnd1_board_characteristics_filtered_avgtimeothco` | 外部董事会经验深度 | − | 外部任职是经验（+）还是分心（−） |
| 7 | `fnd1_filtered_genderratio` | 董事会性别多元化（男性占比） | − | 多元化溢价是否存在 |
| 8 | `fnd1_board_characteristics_filtered_totnounlstdbrd` | 忙碌董事（Fich–Shivdasani 2006：忙碌董事会监督弱） | − | 注意力稀释是否折价 |
| 9 | `fnd1_board_characteristics_filtered_noquals` | 董事学历总量（人力资本） | + | 人力资本是否可交易 |
| 10 | `wealth_sensitivity_to_stock` | 薪酬-业绩敏感性 delta（Core–Guay 1999；Coles et al. 2006） | + | **覆盖率 0.195 的构念是否可达**（覆盖臂） |

壳层统一 `group_rank(<signal>, subindustry)`，信号外层 `ts_backfill(..., 252)`。
**十条全部单字段 ATOM**，无跨数据集组合、无加权混合。

## 7. 预注册判据（回测前写死，事后不得改口）

1. 任一臂 **S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58 且 SUB ≥ 平台 line 且 TO ∈ [0.01, 0.70]** ⇒ 进 prod 队列（`check_correlation(refresh=True)`）。
2. **十臂最高 S < 1.2** ⇒ 判 `USA-FND1-GOVERNANCE-WEAK`，**不发第 2 批**。
3. **覆盖 < 0.50 的臂（#10）即使 S 最高也不单独晋级**：先修 CW / 覆盖，再谈方向。
4. **TO 专属条款**：若某臂**唯一**失败闸是 `LOW_TURNOVER` 且其余指标接近线，只允许一次设置层修复
   （缩短 `ts_backfill` 窗口 / 调整中性化），**不得换概念重试**；修不过判 TO 墙。
5. **符号一致性条款**：若 ≥ 7/10 臂 S 为负（系统性反号），允许**恰好一批**全臂翻号的符号检验
   （原样披露、不调参、不增删臂）。少于 7 条不翻号，直接判弱。
6. 若最强臂来自**结构族**（#1/#5/#7/#9）而流失族全灭 ⇒ 载荷是"公司规模/成熟度"而非治理，
   与 `fundamental6` 的规模腿同源 ⇒ 封存，不做 Mode B。

## 8. 波 87 实测结果与封存裁决（2026-10-23）：`USA-FND1-GOVERNANCE-WEAK`

设置冻结：USA / TOP3000 / D1、**decay 0**、trunc 0.08、INDUSTRY、nanHandling ON、
unitHandling VERIFY、pasteurization ON、maxTrade OFF、2014-01-01→2023-12-31。
multisim `303PNc7ln4Y28RjYlWZhQrg`，**10/10 COMPLETE**。

| # | alpha | 臂（构造） | S | F | TO | 2Y | SUB | RN | 判 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `XgRVnEam` | 董事人数（−） | −0.10 | −0.02 | 0.0297 | −0.54 | −0.24 | +0.14 | 四闸挂 |
| 2 | `QPYOVd0K` | **3 年流失率（−）** | **1.17** | **0.69** | 0.0224 | **1.92** | 0.63 | **0.81** | **两闸挂（S/F），十臂最高** |
| 3 | `P0Mx3EPW` | 1 年流失率（−） | 0.75 | 0.31 | 0.0207 | 1.26 | 0.22 | 0.08 | 四闸挂（SUB 限 0.32） |
| 4 | `zqrgmzA8` | 继任风险（−） | 0.78 | 0.38 | 0.0277 | 1.20 | 0.23 | 0.28 | 四闸挂（SUB 限 0.34） |
| 5 | `88vVQqVm` | 董事平均任期（−） | −0.31 | −0.11 | 0.0249 | −1.01 | −0.07 | −0.02 | 三闸挂 |
| 6 | `9qE8rQM1` | 外部董事会任职（−） | −0.42 | −0.14 | 0.0257 | −1.56 | −0.22 | +0.15 | 四闸挂 |
| 7 | `JjPoOLzO` | 男性占比（−） | 0.64 | 0.23 | 0.0274 | 0.32 | 0.03 | −0.03 | 四闸挂 |
| 8 | `GrgXLvzQ` | 非上市董事数（−） | 0.02 | 0.00 | 0.0260 | 0.43 | −0.05 | −0.38 | 四闸挂 |
| 9 | `omoRleGb` | 学历总量（+） | 0.72 | 0.25 | 0.0259 | 0.79 | 0.42 | 0.28 | 三闸挂 |
| 10 | `9qE8rQm1` | 薪酬-业绩敏感（+） | 0.38 | 0.17 | **0.0096** | 0.65 | 0.34 | 0.27 | 四闸挂（**TO 地板** + 多空 567:2519 退化） |

**裁决**：`max S = 1.17 < 1.2` ⇒ 触发预注册判据 2，判 **`USA-FND1-GOVERNANCE-WEAK`**，**不发第 2 批**。
判据 6 的封存条款不适用（最强臂来自流失族而非结构族），但判据 2 已先行拦下；判据 5 不适用
（仅 3/10 臂 S 为负，未达 7 条门槛，不授权翻号批）；判据 3 被证据正面证实（见下 #10）。

**归因（四组，不是扫参失败）**：

1. **结构族全线无效**：#1 董事人数 −0.10、#5 平均任期 −0.31、#6 外部董事会任职 −0.42、
   #8 非上市董事数 +0.02。四个构念方向各异且全部落在 ±0.5 内 ⇒ 在 INDUSTRY 中性化后，
   **董事会"长什么样"不携带 USA 横截面收益信息**。这与文献一致：结构变量的预测力集中在
   事件窗口（IPO/并购/危机），不在常态面板。
2. **只有"人走了多少"这一族有幅度**：#2 3 年流失 1.17 > #3 1 年流失 0.75、#4 继任风险 0.78，
   且 #2 的 RN 0.81 与 2Y 1.92 说明它不是风险暴露伪装。**信号随平滑窗口变长而变强**
   （3 年 >> 1 年）是该构念为"慢性治理劣化"而非"事件交易"的直接证据。
3. **多元化/人力资本是 2014–2021 的行情，不是可交易 alpha**：#7 男性占比 S 0.64 但 2Y 0.32，
   #9 学历总量 S 0.72 但 2Y 0.79 ⇒ 前八年有效、近两年衰减。ESG 类横截面溢价在 2022 后反转，
   与 `fundamental21` 被降级为"新闻/文本评分族"的判断互证。
4. **覆盖臂按预注册判据 3 失败**：#10 名义 S 0.38，TO 0.0096 击穿 0.01 地板，且
   **longCount 567 / shortCount 2519** —— 覆盖率 0.195 的字段在 TOP3000 上只能一侧建仓，
   方向已被结构锁死。判据 3「覆盖 <0.50 不得单独晋级」写对了。

**两条工程事实**：

- **字段名拼错 = 整批连坐，不是废一条**。首派 `1nPbmEfUU4tScKcNQGH63VV` 用了两个"看着该存在"
  的名字（`fnd1_filtered_totnounlstdbrd` / `fnd1_filtered_noquals`），平台回
  `Attempted to use unknown variable` ⇒ **2 ERROR + 8 CANCELLED**，八条正确表达式一条没跑。
  修正为 `fnd1_board_characteristics_filtered_*` 后重发即 10/10 COMPLETE。
  本节 §2.1 末的"命名陷阱"框就是从这次事故写下的。
  ⇒ 算子闸（`op_arity`）查不出字段名；发批前必须把字段 id 从 `get_datafields` 原样复制，
  不能凭语义拼。`validate_fields=true` 也不会在派发前拦下整批。
- **低换手会把 Fitness 天花板压死**。平台 `fitness ≈ sharpe × sqrt(|returns| / max(TO, 0.125))`：
  TO < 12.5% 时换手不再进入分母，F 完全由 S×√returns 决定。#2 实测
  `1.17 × sqrt(0.0438/0.125) = 0.69`，与平台值逐位吻合。⇒ 要 F ≥ 1.0 且 S = 1.58，
  年化收益必须 ≥ **5.0%**；#2 现有 4.38%。**慢速 fundamental 信号的瓶颈在收益幅度，不在换手或中性化**，
  所以本条不适用判据 4 的"一次设置层修复"（设置改不动 returns 的量级）。

**为什么不在 1.17 上再抢救一轮**：本仓 `Mode B` 资格线是 S ≥ 1.25 **且** F ≥ 0.8，
#2 两条都不够（1.17 / 0.69）。把 S 从 1.17 抬到 1.58 需要 +35%，对一条十年面板信号而言，
这等于要求真实 Sharpe ≈ 1.6 —— 证据不支持，靠窗口/中性化微调只会过拟合。
判据 2 的 1.2 线本就写在看到结果之前，此时改口就是事后调参。

**可复用的第四层 S0 先验（接波 85 的"按机制计拥挤度"、波 86 的"独特构念未必可表达"）**：
**治理类数据集的可交易载荷只在"人员流动率"，不在"结构/画像"**。BoardEx 型数据集字段数往往
上百（本集 179 可用），但按构念归并后真正有横截面预测力的只有 1 个族（流失），其余是
控制变量或事件研究变量。⇒ 拿到 governance 数据集时，**先测流失/更替族，结构族只留 1–2 条对照臂**，
不要把十臂预算平摊到"董事会长什么样"上。
