# DEU macro27 模板池（S1 发波前置产物，2026-11-02）

- 区域设置：EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay4 / trunc 0.08 / nanHandling OFF
- 数据集：macro27 Job records from job posting（MACRO category，**单塔 MACRO 合规**：全表达式只用 macro27 字段 + 分组轴（不算腿），零 PV 腿，trio×非trio 配额 5/5 已满不触碰）
- 字段：13 全 VECTOR（须 `vec_avg` 包裹；coverage 平台口径全 0.0，逐年覆盖以探针 yearly stats 为准）。三族：
  - **流量计数族** `num_jobs_created`(ac12)/`num_jobs_active`(ac28)/`num_jobs_removed`(ac10)/`mcr27_company_jobs{created,active,removed}`(ac19/13/10)——计数类，**水平用须 ts_rank(·,252) 去规模混淆；变化率自带去规模不用再 ts_rank**
  - **时长水平族** `mean_days_job_active`(ac42)/`mean_days_job_closed`(ac64)/`avg_days_job_posting_{active,closed}`——水平即信号，禁时序归一化
  - **事件旗标** `is_job_repost_flag`(ac28)——repost 率升=需求疲软
- 方向先验（两个矩别混）：**变化率/加速度→正向**（论坛 AK85882《hiring_trends USA》92 赞实证：INDUSTRY→SLOW 后 S 2.40 过 Ladder）；**空缺水平→负向**（Liu 2019 Labor-Based Asset Pricing, SSRN 3081364）；removed 激增→收缩负向；repost 率升→负向
- 时间窗白名单：22/66/252（论坛 21→22 归入白名单）
- 除零保护：比率族分母 `add(x, multiply(0.001, x))`；`tail` 四参必须全显式（lower/upper/newval）

## 模板池（12 个，结构互异；差异落点=骨架/算子几何/矩/分组轴/非线性）

| # | 模板 | 表达式骨架 | 机制 | 差异落点 | 来源 |
|---|---|---|---|---|---|
| M1 | 招聘变化率 | `group_rank(ts_delta(vec_avg(num_jobs_active), 22), subindustry)` | 招聘加速=扩张预期，正向 | 一阶差分×group_rank×计数族 | 论坛 AK85882（评论区简化等价式） |
| M2 | 空缺水平负向 | `subtract(0, group_rank(ts_rank(vec_avg(mcr27_company_jobsactive), 252), subindustry))` | 空缺水平高→未来收益低（水平矩） | ts_rank 水平分位×负向 | 论文 Liu 2019 |
| M3 | 净招聘流量 | `group_rank(ts_delta(subtract(vec_avg(mcr27_company_jobscreated), vec_avg(mcr27_company_jobsremoved)), 22), subindustry)` | 净增岗位加速=扩张 | 同机制净额合成（created−removed）×差分 | 自建（净额合成合规） |
| M4 | 招聘加速度 | `group_rank(ts_delta(ts_delta(vec_avg(mcr27_company_jobscreated), 22), 22), industry)` | 招聘二阶导=趋势强化 | 二阶差分×行业粗轴（轴粒度对照） | 自建（动量加速度迁移） |
| M5 | repost 疲软 | `subtract(0, group_rank(ts_mean(vec_avg(is_job_repost_flag), 66), subindustry))` | repost 率升=需求疲软，负向 | 事件旗标矩×平滑窗×负向 | 自建（旗标机制） |
| M6 | 挂牌时长水平 | `subtract(0, group_rank(ts_rank(vec_avg(mean_days_job_active), 252), subindustry))` | 挂得久=需求弱 | 时长水平族×ts_rank×负向 | 自建（时长=需求强度） |
| M7 | 删失时长变化 | `subtract(0, group_rank(ts_delta(vec_avg(mean_days_job_closed), 22), subindustry))` | 删失时长变长=清理僵尸岗=需求走弱 | 时长族一阶差分×负向 | 自建 |
| M8 | 删增比 | `subtract(0, group_rank(ts_mean(divide(vec_avg(mcr27_company_jobsremoved), add(vec_avg(mcr27_company_jobscreated), multiply(0.001, vec_avg(mcr27_company_jobscreated)))), 22), subindustry))` | 删除/新增比高=收缩 | 比率几何×ts_mean 平滑×除零保护 | 自建（比率型） |
| M9 | 双窗变化价差 | `group_rank(subtract(ts_delta(vec_avg(num_jobs_active), 22), ts_delta(vec_avg(num_jobs_active), 252)), subindustry)` | 短窗变化>长窗变化=加速确认 | 同字段双周期价差（合规） | 自建（双周期价差） |
| M10 | 原挂牌门控 | `trade_when(less(vec_avg(is_job_repost_flag), 0.5), group_rank(ts_delta(vec_avg(num_jobs_active), 22), subindustry), 0)` | 仅原挂牌期的变化信号可信 | trade_when 稀疏骨架（兼降 self/prod） | R 家族 trade_when 门槛经验迁移 |
| M11 | 扩张尾部截断 | `tail(group_rank(ts_delta(vec_avg(mcr27_company_jobscreated), 22), subindustry), lower=0, upper=0.85, newval=0)` | 只留 top15% 强扩张尾部 | tail 非线性截断（四参全显式） | 论坛 tail(group_zscore) 迁移 |
| M12 | 衰减加权变化 | `group_rank(ts_decay_linear(ts_delta(vec_avg(num_jobs_active), 22), 22), industry)` | 近期变化加权 | ts_decay_linear 时间加权几何×行业粗轴 | 自建（decay 几何） |

**模板来源统计**：论坛 2（M1/M11）+ 论文 1（M2）+ R 家族经验迁移 1（M10）+ 自建 8——差异落点覆盖：一阶差分/二阶差分/水平分位/比率/净额/双窗价差/旗标矩/门控/截断/衰减，10 类互异几何。

## 发波记录（2026-11-02）

- 两道预检全过：preflight `unknown_fields: []`（7 字段全存在）+ verify_expr.py 语法/元数 12/12 valid。
- 首次派发（batch_create_simulations 12 条整批）被 MCP 侧 120s wall_clock_exceeded 截断；补发前按表达式匹配 get_user_alphas 确认**无任何落地 alpha ⇒ 判定整批未入队**，全部走补发批（若后续同表达式重复落地，去重留一）。
- 补发批（小批 2-3 条）：第一轮 8/12 入队、4 条 429（CONCURRENT_SIMULATION_LIMIT_EXCEEDED）；等 90s 后第二轮 4/4 入队。**12/12 全部拿到 sim ID**：

| 模板 | sim ID | 模板 | sim ID |
|---|---|---|---|
| M1 | `2S4Zypczd4GWaLOzv5l82kk` | M7 | `4mNLsp2f4TMcCN14rWcsCTl` |
| M2 | `374yj24JB4xObg317kV8q2Ov` | M8 | `3U0cki7Se4Zu8JAOOiK7fx0` |
| M3 | `16Byyu8Vu4MaaRLFPUuGFel` | M9 | `13Pxzpc4R4up9t6qemTT4CP` |
| M4 | `sjGz15WF4lHcewXrNeCfbk` | M10 | `3xyI093kz4jxcdu8ZEvwSy9` |
| M5 | `4EgwwrgF85chaf6kydJBnY7` | M11 | `2OE8nudL64oMakR19VbYiNoO` |
| M6 | `46UE6H62G59saEq1aRpLtIVS` | M12 | `417DmE4ns5hAbvtBoFC1eHE` |

## 发波纪律

- 模板池 12 ≥ 10 ✓；归因按模板族统计。
- 覆盖口径：发波后逐条 `get_alpha_yearly_stats` 查 longCount>0 && pnl≠0；2019 前若连续多年空窗→标 leading-gap（裁定未决，暂保留但入篮前再审）。
- 设置对照实验（objective④）：M1 出信号后做 SUBINDUSTRY vs SLOW 中性化对照（论坛实测 SLOW 大幅提升，单变量对照）。
- 预检两道：preflight 字段存在性 + verify_expr.py 语法/元数。

## 波 1 收批 + 全景归因（2026-11-02，12/12 COMPLETE）

| 模板 | alpha | S | F | TO | 2Y | margin | ra | 逐年覆盖 | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| M1 变化率 | WjOGJvvo | 0.54 | 0.20 | 21.2% | 0.97 | 2.8bp | 5 | **全 10 年**（25→109 票） | 信号弱但干净 |
| M2 水平负向 | pwdlpwQj | 0.74 | 0.26 | **83.2%** | −0.59 | 2.4bp | 5 | 2016 起、早年 longCount=2 | TO 炸+2Y 负 |
| M3 净招聘流 | 1YNd26om | −0.52 | −0.13 | **135.2%** | −0.38 | −1.2bp | 6 | — | 方向反+TO 炸 |
| M4 加速度 | 78L1l5Zx | **−0.74** | −0.23 | **117.5%** | −0.42 | −1.9bp | 6 | — | 方向反（加速=利空） |
| M5 repost 负向 | QPvVo1Pg | −0.59 | −0.41 | 3.2% | −0.64 | −36.8bp | 5 | — | 方向先验反 |
| M6 时长水平 | 3qoR2aN6 | 0.17 | 0.02 | **104.8%** | 0.26 | 0.2bp | 6 | — | 弱 |
| M7 删失时长变化 | 0mYEamxq | **0.94** | 0.20 | **141.7%** | 0.78 | 0.9bp | 6 | **2021 起，前 7 年全空窗** | S 最高但 TO 炸+leading-gap 最重 |
| M8 删增比 | RRE8vRlg | 0.30 | 0.13 | 7.2% | 0.49 | 6.2bp | 5 | — | 弱、方向对 |
| M9 双窗价差 | gJeM0PWO | 0.07 | 0.02 | 9.7% | −0.46 | 1.7bp | 4 | — | 死 |
| M10 原挂牌门控 | bl6qKWzR | 0.44 | 0.16 | 18.1% | **1.14** | 2.7bp | 5 | **全 10 年**（24→121 票） | 2Y 最强（2022 1.16/2023 1.12） |
| M11 扩张尾部 | WjOGxN6d | **−0.84** | −0.26 | **133.6%** | 0.29 | −1.9bp | 6 | — | 方向反（扩张尖峰=利空） |
| M12 衰减加权 | kqN0YQAd | 0.13 | 0.03 | 11.7% | 0.24 | 1.2bp | 5 | — | 死 |

### 归因（6 条）

1. **方向先验双确认**：M1 变化率正向 S 0.54 ✓（论坛）+ M2 水平负向 S 0.74 ✓（Liu 2019）——两个矩的方向在 DEU 都成立。
2. **DEU 特有翻转：招聘激增=过热=利空**。M3 净流 −0.52 / M4 加速度 −0.74 / M11 扩张尾部 −0.84——三条「扩张正向」先验全反，与 Liu 水平负向自洽（高空缺=负收益，DEU 连变化的**尖峰**也是负的）。⇒ 修复轮按「尖峰利空」翻向。
3. **M5 repost 先验反了**：S −0.59，repost 率升在 DEU 不是需求疲软信号。
4. **换手指纹证实「日频计数先平滑」铁律**：不平滑模板 TO 全炸（83–142%）；M1/M10 用 22 日差分自带部分平滑（TO 18–21% 可用）。
5. **覆盖分层**：`num_jobs_*` 聚合族全 10 年（M1/M10）；`mcr27_company_*` 2016 起且早年 longCount=2；`mean_days_job_closed`（M7）**2021 起、前 7 年彻底空窗**（leading-gap 最重一例，裁定前不入篮）。
6. **M10 两年最强**：2Y 1.14（2022 1.16 / 2023 1.12），门控版近两年持续——SLOW 设置对照（论坛 S 1.57→2.40）首选载体。

### 修复轮设计（单杠杆/探针，验收预锁 2Y≥1.58+RA=0+S≥1.58）

- P1 M7s 平滑（杠杆=ts_mean 平滑）：`subtract(0, group_rank(ts_delta(ts_mean(vec_avg(mean_days_job_closed), 22), 22), subindustry))`
- P2 M2s 平滑（杠杆=ts_mean 平滑）：`subtract(0, group_rank(ts_rank(ts_mean(vec_avg(mcr27_company_jobsactive), 22), 252), subindustry))`
- P3 M4f 翻向（杠杆=符号，方向探针）：`subtract(0, group_rank(ts_delta(ts_delta(vec_avg(mcr27_company_jobscreated), 22), 22), industry))`
- P4 M1-SLOW（杠杆=neutralization 设置，论坛配方对照）：M1 式 @ SLOW
- P5 M10-SLOW（杠杆=neutralization 设置）：M10 式 @ SLOW

### 修复轮收批（2026-11-02）

| 探针 | 杠杆 | alpha | S | F | TO | 2Y | margin | 判定 |
|---|---|---|---|---|---|---|---|---|
| P1 M7s 平滑 | ts_mean(22) 平滑 | **LLM1wMM9** | **1.35** | 0.90 | **14.6%** | **1.53** | 8.8bp | ★平滑大成功（S 0.94→1.35 / TO 142%→14.6% / 2Y 0.78→1.53）；但**2014-2020 七年全空窗**（2021 起，leading-gap 最重一例），2Y 1.53 距闸 0.05 在噪声带内 |
| P2 M2s 平滑 | ts_mean(22) 平滑 | kqN0MppL | −0.09 | −0.02 | 8.6% | −0.49 | −2.2bp | ✗ 平滑杀信号——M2 靠噪声驱动，判死 |
| P3 M4f 翻向 | 符号翻转 | 78L1Rmqv | **0.74** | 0.23 | **117.5%** | 0.42 | 1.9bp | ★方向实锤：M4 正向 −0.74 → 负向 +0.74 完美翻转（**招聘加速度=利空**）；但 TO 炸待平滑 |
| P3s M4fs 平滑 | ts_mean+翻向 | MPYQv66r | 0.14 | 0.04 | 20.4% | −0.08 | 1.6bp | ✗ **平滑杀翻向信号**（TO 修好但信号没了） |
| P4 M1 @SLOW | neutralization | omEl02bn | 0.27 | 0.06 | 25.0% | 0.46 | 0.8bp | ✗ **论坛 SLOW 配方不迁移 DEU**（M1@SUBIND 0.54 > 0.27），设置对照判死 |
| P5 M10 @SLOW | neutralization | 弃 | — | — | — | — | — | P4 已判死 SLOW 杠杆，弃发省槽 |
| Q1 M1s 平滑 | ts_mean 迁移 | kqN0wrLP | 0.06 | 0.01 | 8.2% | −0.38 | 0.9bp | ✗ **平滑杀 M1 信号**（0.54→0.06） |
| Q2 M1 industry 轴 | 论坛原方轴 | MPYQEa6M | **0.68** | 0.28 | 22.0% | **1.00** | 3.5bp | ✓ 论坛 industry 轴优于 subindustry（S 0.54→0.68 / 2Y 0.97→1.00） |

### 修复轮终局归因（3 条）

1. **★★ 平滑杠杆是字段级选择性，不是公理**：M7 时长族平滑大成功（S 0.94→1.35 / TO 142%→14.6%，低频信号被去噪放大）；但 M1/M2/M4f 三个变化率族同杠杆**全杀信号**（0.54→0.06 / 0.74→−0.09 / 0.74→0.14）——变化率信号住在**高频分量**里，先平滑再差分=把信号洗掉。⇒ 水平位使用（ts_rank/排序）照旧必平滑；**ts_delta 位使用先单杠杆实测**：时长族适用、计数变化族禁用。
2. **SLOW 中性化配方不迁移**：论坛 USA 的 S 1.57→2.40 在 DEU 反向（0.54→0.27）。跨区搬设置杠杆前必须本地单变量对照。
3. **industry 轴 > subindustry 轴**（M1 同式 0.54→0.68）：宏观招聘信号在行业层聚合比子行业层有效（招聘数据行业聚集性强）。

### macro27 现状与下一步

- **机制成立**：方向先验双确认（变化率正向/水平负向）+ DEU 特有「加速/尖峰=利空」翻转实锤。
- **最佳载体 LLM1wMM9**（M7s：S 1.35 / F 0.90 / TO 14.6% / 2Y 1.53 / RA 4）卡在 **2014-2020 七年全空窗**（leading-gap 最重一例）⇒ **裁定前不入篮**。
- 下一步备选：① M10 门控×industry 轴组合（单杠杆=组轴位移）；② LLM1wMM9 破闸轮（若 leading-gap 裁定保留）；③ 转 earnings_sent_matrix。
### 全覆盖字段探针（2026-11-02 第二轮修复，P6-P8）

| 探针 | 杠杆 | alpha | S | F | TO | 2Y | margin | 判定 |
|---|---|---|---|---|---|---|---|---|
| P6 M10×industry 轴 | 组轴位移 | d5W0NAJv | 0.53 | 0.21 | 18.9% | **0.80** | 3.2bp | ✗ S 微升（0.44→0.53）但 **2Y 反跌（1.14→0.80）**——industry 轴优势只在裸 M1 上成立，门控版不复现 |
| P7 加速度利空×num_jobs_active | 翻向+换字段 | rKRlZjAo | −0.08 | −0.01 | 27.8% | −1.29 | −0.3bp | ✗ 尖峰利空**只活在 company 级字段**，聚合字段不复现 |
| P8 尖峰尾部利空×num_jobs_active | 翻向+换字段 | leAlo397 | −0.68 | −0.29 | 23.2% | −0.52 | −3.6bp | ✗ 同上，且方向都不稳 |

**覆盖判据补充（关键）**：时长族（`mean_days_job_active`/`mean_days_job_closed`）全线 2021 起（前 7 年空窗）；company 级字段 2016-2020 longCount=1（事实空窗）⇒ **macro27 真正全覆盖的只有 `num_jobs_*` 聚合族**（M1/M10 系）。

### macro27 终局盘点（26 条 sim：波1 12 + 修复 14）

- **唯一有希望的载体：LLM1wMM9**（M7s，S 1.35 / 2Y 1.53 / TO 14.6% / F 0.90）——但字段属时长族，2014-2020 七年全空窗，**leading-gap 裁定前不可入篮**。若裁定保留 ⇒ 直接进破闸轮（差 2Y 0.05）；若除名 ⇒ macro27 剩余可挖面（num_jobs 族）最高 S 仅 0.68，转下一矿脉。
- num_jobs 族天花板实测：M1@industry（0.68/2Y 1.00）为该族最优，距闸 1.58 差 2.3 倍 ⇒ **不值得再投参数扫**。
- 方法论产出 3 条已沉淀：平滑字段级选择性 / SLOW 不迁移 / industry 轴仅裸信号有效。


**P1 逐年（get_alpha_yearly_stats）**：2014-2020 全 0；2021 long53/S 0.32；2022 long120/S 1.59；2023 long119/S 1.48。近两年一致性好，但前 7 年彻底空窗 ⇒ leading-gap 裁定前不入篮。


