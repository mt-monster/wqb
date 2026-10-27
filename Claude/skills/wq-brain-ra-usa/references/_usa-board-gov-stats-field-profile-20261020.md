# board_gov_stats（US Board Governance）字段画像与首轮预注册（USA / D1 / TOP3000，2026-10-20）

> 用途：PV 塔三条主线（pv63 / pv103 / pv115）全部判弱封存后，USA 未点亮塔的下一条主线。
> 选它的理由不是「随便换数据集」，而是：**insiders 塔里唯一没有被判死覆盖的子域** ——
> 内幕交易侧已有三条 dead_end（`USA-INSIDER-MATRIX-SPARSE-EVENT-WALL`、`USA-INSIDERS1-DEU-CONVICTION-WEAK`、
> `USA-INSIDER-FEATS-DEAD`），而**董事会/管理层治理结构一条都没测过**。
> 本档按「字段画像 → 适用模板 → 回测结果及指标」组织，回测完成后回填 §5。**本档不含提交动作；任何提交都必须用户明确确认。**

---

## 0. 数据集坐标（`get_datasets` / `get_datafields` 2026-10-20 实测）

| 项 | 值 | 备注 |
|---|---|---|
| dataset id | `board_gov_stats` | "US Board Governance and Leadership Metrics" |
| 塔位 | USA / D1 / **insiders 塔未点亮**（`get_pyramid_alphas` insiders=0） | 符合「未点亮塔优先」 |
| 可见字段 | **46**（`sharpe_filter_applied=true`，`sharpe_filter_removed=0`） | 全部 **MATRIX** |
| 覆盖率 | 主体 **0.886–0.9482**；`surname_concentration_management` 仅 0.5948 | 覆盖中等，必须 backfill |
| 数据集 alphaCount | **499** | 低拥挤（对比 pv103 9679 / analyst_consensus 数万） |
| 字段 alphaCount | **2–95**（中位 ~10） | 全塔最冷的一批字段；`aggregate_external_connections` 38、`board_departure_rate_3m_management` 95 已是高位 |
| 金字塔乘数 | 1.1 | insiders 类 |
| 更新频率 | 治理结构为**事件/季度级**变化（任期、离职、加入、董事会构成） | D1 下靠 `ts_backfill` 前向填充；**LOW_TURNOVER 是本集第一风险** |

**为什么不是 institutions 塔**：inst18 的 `instownership_pct_held` 水平族已在 submit_ready 里实测
prod = **0.9394**（`leKLRA1N` / `JjQV5eO2` 两条同族都撞同一墙）⇒ 所有权水平是 PROD 饱和族；
institutions 塔的其它集留作后续测量面，不在本轮开批。

---

## 1. 字段画像（按机制分六族）

### 1.1 人员流动族（event-like，本集最像 alpha 的一组）

| 字段 | 含义 | cov | aC |
|---|---|---:|---:|
| `board_departure_rate_3m_management` | 过去 3 个月离开董事会的管理层比例 | 0.9234 | **95** |
| `board_departure_rate_1y_board` | 过去 1 年离开的董事比例 | 0.886 | 18 |
| `board_departure_rate_6m_management` | 过去 6 个月离开的管理层比例 | 0.912 | 31 |
| `management_departure_rate_3m/6m/1y_management` | 管理层自身 3m/6m/1y 离职率 | 0.8775–0.9149 | 8–12 |
| `personnel_departure_rate_3m/6m/1y_total` | 全部董事+高管 3m/6m/1y 离职率 | 0.886–0.9234 | 7–17 |
| `board_join_rate_3m_management` / `management_join_rate_3m_management` | 3 个月加入比例 | 0.9234/0.9149 | 61/6 |
| `personnel_join_rate_3m_total` | 全部人员 3 个月加入比例 | 0.9234 | 12 |

**经济含义**：这是**滚动事件强度**，不是静态结构 —— 离职率高 = 治理动荡/业绩压力/诉讼；
加入率高 = 扩张/换血。**本集唯一天然带「变化」的族**，最可能绕开「慢变量 TO <1%」的坑。

### 1.2 领导层任期族（慢变量）

`ceo_tenure_days`（aC 46 / cov 0.9334）、`chairman_tenure_days`（40 / 0.9364）、
`max/median/min_chief_officer_tenure_days`（29/16/8 / 0.9353）。
**经济含义**：任期长 = 经验与稳定；新任 = 战略变革期（风险与期权价值并存）。

### 1.3 权力结构族（0/1 或比例）

`ceo_chairman_duality_flag`（aC 16 / cov 0.9223）、`chief_officer_chairman_flag`（6 / 0.924）、
`multiple_ceo_indicator`（3 / 0.9482）、`independent_director_ratio`（14 / 0.9482）、
`board_member_count_2`（16 / 0.9482）、`management_team_size`（4 / 0.9411）。
**经济含义**：权力集中（兼任）通常负面；独立董事比例与治理质量正相关；
董事会规模大 = 决策惰性。哑变量直接 rank 只有两档 ⇒ 必须 `ts_mean` 平滑后再截面排序。

### 1.4 外部连接网络族（社会资本）

`aggregate_external_connections`（aC 38 / cov 0.9482）、`board_external_connection_count`（35 / 0.9482）、
`unique_external_company_union`（8 / 0.9482）/`_board`（8）/`_management`（10）、
`management_external_connection_count`（4 / 0.9411）。
**经济含义**：董事/高管在其它公司的席位 = 信息渠道与社会资本；过度连接 = 忙碌董事（busy board）负面。
单调方向不唯一，需成对测。

### 1.5 人口学/学历族（弱先验，仅作对照）

`male_ratio_board/management/total`、`doctorate_share_*`、`ceo_gender_flag`（aC 3–13）。
**经济含义**：多样性溢价在 USA 大市值已被定价，且易成为行业/规模代理。**首轮只放 1 条对照，不占主位。**

### 1.6 家族控制族

`surname_concentration_board`（aC **2** / cov 0.9482）、`_management`（3 / 0.5948）、`_total_personnel`（3 / 0.9482）。
**经济含义**：同姓董事比例的对数度量 ⇒ 家族/裙带控制代理。方向待定（长期主义 vs 任人唯亲）。

---

## 2. 适用模板（M01–M08）

| # | 机制 | 一句话 | 壳内 SIG | 预期符号 |
|---|---|---|---|---|
| M01 | 治理动荡 | 3 个月管理层离职率高 ⇒ 治理风险折价 | `board_departure_rate_3m_management` | 负 |
| M01b | M01 反向（成对） | 稳定董事会溢价 | `reverse(...)` | 正 |
| M02 | 净人员扩张 | 加入率 − 离职率 > 0 ⇒ 组织扩张 | `subtract(personnel_join_rate_3m_total, personnel_departure_rate_3m_total)` | 正 |
| M03 | 董事会独立性 | 独立董事占比高 ⇒ 治理质量 | `independent_director_ratio` | 正 |
| M04 | 新任 CEO | 任期短 ⇒ 变革期（期权价值） | `reverse(ceo_tenure_days)` | 正 |
| M05 | 外部连接 | 董事网络广度 ⇒ 信息优势 | `unique_external_company_union` | 正 |
| M06 | 权力集中 | CEO 兼任董事长 ⇒ 治理风险 | `ts_mean(ceo_chairman_duality_flag, 66)` | 负 |
| M07 | 家族控制 | 同姓集中度高 ⇒ 裙带折价 | `surname_concentration_board` | 负 |
| M08 | 董事会规模 | 规模大 ⇒ 决策惰性 | `board_member_count_2` | 负 |

**统一壳（本批 8 条完全相同，只换 SIG）**：

```
quantile(group_rank(ts_backfill(winsorize(<SIG>, std=4), 252), industry))
```

**刻意不带 `hump`**：pv103 批 2 已实测 `hump(0.01)` 把 TO 从 29–49% 压到 0.9%（B2-1/B2-2），
是本仓目前最强的低通滤波器；本集字段本身已是慢变量，**再加 hump 必踩 LOW_TURNOVER**。

---

## 3. 判死先验与外部证据（开批前必读）

1. **内幕交易侧三条 dead_end 不覆盖本集**：`USA-INSIDER-MATRIX-SPARSE-EVENT-WALL`（insider_agg_matrix 买卖金额稀疏）、
   `USA-INSIDERS1-DEU-CONVICTION-WEAK`（信念强度 max S 0.78）、`USA-INSIDER-FEATS-DEAD`（买卖比 |S|<0.5）
   —— 测的都是**交易行为**，本集测的是**治理结构**，字段不重叠。
2. **慢变量 TO 风险**：治理字段季度更新，D1 下截面排序稳定 ⇒ TO 可能 <1%。缓解：不带 hump；
   若仍 <1%，改用 3m join/departure 这类滚动事件率（M01/M02）而非静态结构（M03–M08）。
3. **质量因子饱和**：`independent_director_ratio` 正向本质是治理质量，USA 的 value/quality/book 已高度饱和
   （`USA-VALUE-PRODCORR`：book 145 ACTIVE）⇒ **M03 一旦 IS 过闸，必须立刻查 prod**，不先调参。
4. **家族/人口学字段是行业代理**：姓氏集中度、性别/学历比例在 industry 内 rank 后仍可能剩行业残差，
   风险中性化后 <0.3 即判风格暴露，不进交付。
5. **ATOM 合规**：8 条全部只引用 board_gov_stats 字段；`industry` 分组属豁免。

---

## 4. 批 1 预注册（8 探针，写死）

> 设置：EQUITY / USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / truncation 0.08 /
> nanHandling ON / unitHandling VERIFY / pasteurization ON / maxTrade OFF / FASTEXPR。
> 区间平台缺省（2014-01-01 → 2023-12-31，与历史批次可比）。全部套 §2 统一壳。

| # | 机制 | 壳内 SIG | 备注 |
|---|---|---|---|
| G1 | M01 治理动荡 | `board_departure_rate_3m_management` | 最高 aC（95）的事件率字段 |
| G2 | M01b 反向 | `reverse(board_departure_rate_3m_management)` | 与 G1 成对，防方向误判 |
| G3 | M02 净扩张 | `subtract(personnel_join_rate_3m_total, personnel_departure_rate_3m_total)` | 唯一「差分型」构造 |
| G4 | M03 独立性 | `independent_director_ratio` | 质量先验，prod 风险最高 |
| G5 | M04 新任 CEO | `reverse(ceo_tenure_days)` | 慢变量，测 TO 下限 |
| G6 | M05 外部连接 | `unique_external_company_union` | aC 8，最冷的结构字段之一 |
| G7 | M06 权力集中 | `ts_mean(ceo_chairman_duality_flag, 66)` | 哑变量先平滑 |
| G8 | M07 家族控制 | `surname_concentration_board` | aC 2，全塔最冷 |

**预注册判据**：

- 任一 `S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB PASS` 且 `fail=0` ⇒ 立即 `check_correlation(refresh=True)`；
  prod ≥0.75 或踩线失败 ⇒ 按决策表 D0-P 判 `dead_end`，**不做同族磨参数**。
- **G1 与 G2 严格镜像且 |S| 均 <0.8** ⇒ 治理动荡无信息，M01 判弱，不再补方向变体。
- **全批 TO <1%** ⇒ 判「治理结构是纯静态慢变量」，批 2 只允许 M01/M02 的滚动事件率（3m/6m 两档），
  静态结构族（M03–M08）全部判弱封存。
- **TO 健康但全 |S|<0.8** ⇒ 与 pv115 同型（真零信号），本集判弱，不再补批。
- **M03 / M07 任一 S≥1.2** ⇒ 先查 risk-neut：<0.3 判风格代理（质量/行业），不进交付。
- **全部 8 条 fail≥3** ⇒ 本集判弱封存，登记 insiders 塔「治理结构亦弱」，转 institutions 塔。

---

## 5. 回测结果及指标

**批 1（multisim `1aQpDZ2J4Y19a31hPT7UTHK`，8/8 COMPLETE）**
设置：EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / maxTrade OFF；
平台缺省区间（2014-01-01 → 2023-12-31）。**8 条全部 `fail≥2`，无一条全闸通过。**

| # | alpha | 机制 | S | F | 2Y | SUB（limit） | TO | returns | DD | risk-neut | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| G1 | `vROvL1PQ` | 3m 管理层离任率（正向） | 0.35 | 0.11 | 0.86 | 0.30 | 3.55% | 1.17% | 12.6% | −0.56 | 3 |
| G2 | `ZYmKpQ1n` | 反向（稳定性溢价） | **1.56** | **1.02** | **2.55** | **0.64(0.68)** | 3.48% | **5.31%** | 4.8% | **1.12** | 2 |
| G3 | `JjPvpe2W` | 加入−离任 | 0.88 | 0.40 | 1.52 | 0.18(0.38) | 3.93% | 2.64% | 7.9% | 0.31 | 4 |
| G4 | `zqrR93E1` | 独董比例 | 0.93 | 0.54 | 1.08 | 0.38(0.40) | 1.42% | 4.18% | 8.0% | **0.00** | 4 |
| G5 | `P0MOpobM` | 反向 CEO 任期 | −0.37 | −0.11 | −0.96 | −0.23 | 1.55% | −1.20% | 23.2% | −0.10 | 4 |
| G6 | `npA8gvlE` | 外部连接公司数 | 1.20 | 0.67 | 1.53 | 0.43(0.52) | 5.94% | 3.93% | 5.0% | 0.67 | 4 |
| G7 | `d5KRxWrg` | CEO/董事长兼任 66d 均值 | 0.97 | 0.42 | 1.67 | 0.08(0.42) | 1.34% | 2.30% | 3.7% | 0.94 | 3 |
| G8 | `d5KRxWrj` | 董事会姓氏集中度 | 0.81 | 0.40 | 2.04 | −0.04(0.35) | 1.45% | 3.12% | 11.2% | 0.73 | 3 |

**G2 的 prod 实测**：`check_correlation(ZYmKpQ1n)` → production.max_correlation = **0.8508**（`passes_check=false`），
直方图 `[0.8,0.9]` 桶 **n=1** ⇒ 按 `wq-window-valley-break-prod-wall` 与决策表 D0-P 的「n≥1 必死」，
**判 prod 墙、封存，不做同族磨参数**。G2 的 IS 面只差 LOW_SHARPE 0.02 与 SUB 0.04，但 prod 已先否决。

**归因（七条，决定批 2 不再开）**：

1. **G1/G2 非对称是结构性的**：同一字段的正向 0.35 / 反向 1.56，差 1.21 ⇒ **「治理动荡折价」不存在，
   只有「治理稳定溢价」有效**。这与 board_gov_stats 的经济含义一致：离任率高不是坏事（正常换届），
   但**低离任率是高质量信号**；因此该字段只有右尾（稳定）有 alpha，左尾是噪声。
   ⚠ 该非对称同时说明：把 G2 当「反向事件因子」做更多变体没有意义，信号信息几乎全在分布的一端。
2. **TO 全批健康（1.34–5.94%）**：治理变量虽是季度/事件级更新，但 3m/6m 滚动率本身每日漂移，
   不需要 hump / 长平滑 —— 与 pv103「hump 本身就是信号载体」形成对照：**慢变量不等于需要低通滤波**。
3. **G4 risk-neut = 0.00**：独董比例 S0.93 但收益 100% 来自风格暴露（质量/规模），**纯风格 beta**，
   按 `risk_neutralized_sharpe < 0.3 ⇒ 风格代理` 判弱，不进任何后续批。
4. **G6 外部连接网络是本批第二强**（S1.20 / 2Y1.53 / risk-neut 0.67 / TO 5.94%），但 SUB 0.43 vs limit 0.52；
   信号真实存在（risk-neut>0.6 排除纯风格），弱在**小盘段斜率不足**。按方法论 §10（SUB 真解 = 测量口径）
   本应优先试 `ts_zscore` 自波动归一；但同族 G6 与 G2 机制不同、而 G2 已撞 prod 墙 0.85，
   本集最高 S 仅 1.56 ⇒ **整集上限低于交付线**，不值得为 G6 单独开批。
5. **G7 / G8 是「2Y 幻觉」**：2Y 1.67 / 2.04 看着很好，但全期 S 0.97 / 0.81、SUB 0.08 / −0.04 —— 
   典型「近两年有效、全期与小盘段无效」的 regime 依赖。与 pv63 的 yearly 诊断同型。
6. **G5 为负**：反向 CEO 任期在 USA 无信息（S−0.37，DD 23.2%）⇒ 任期长度不是 alpha 维度。
7. **交叉印证并行 campaign**：同一数据集另有一轮 4 批 32 条（台账 §2 board_gov_stats 行，`3qjezndX` S1.38/SUB0.66 PASS、
   `Vkd3X00M` S1.54/SUB0.41），结论同向：**最高 S≈1.5、SUB 或 TO 至少一闸结构性卡死，整集封存**。
   本轮 G2 补上了「即使 IS 面最强的那条，prod 也 0.85」这条独立证据 ⇒ 封存理由从「指标不够」升级为
   **「IS 与 prod 双墙」**，后续不得因 aC 低而复活。
8. **`3qjezndX` prod 实测（2026-10-20 补）**：`check_correlation(3qjezndX, refresh=True)` →
   production.max_correlation = **0.9137**（`[0.9,1]` n=5、`[0.8,0.9]` n=1482），risk-neut 0.98 也救不了。
   ⇒ 本集**所有形态**（G2 反向 3m 0.8508、M1 ts_rank504 0.9137）都落在同一片 prod 饱和区，
   证实「治理/任职变动」整体是已定价风格 ⇒ `USA-BOARD-GOV-STABILITY-PROD-WALL` 升为**硬判死**，
   不再以「IS 差一闸」为理由重开。

**批 2 决策**：不开。本集封存，登记 `USA-BOARD-GOV-STABILITY-PROD-WALL`（本档为证据索引）。

---

## 6. 风险与预判

- **数据历史长度未知**：cov 0.92 是当前覆盖；若 2014–2016 缺治理数据，2Y 会虚高（同 `chart_return_model` 陷阱）。
  收割后先 `get_alpha_yearly_stats` 看逐年，再判死。
- **字段 alphaCount 极低（2–95）既是蓝海也是警告**：可能是「没人挖」也可能是「挖过没声音」。
  本批同时给出 8 个机制，若全部 <0.8，基本可确定是后者。
- **量化数据供应商的治理快照存在回溯修订**（董事会成员更正），D1 下用 `ts_backfill` 会引入前视修正；
  这是本集无法用设置消除的风险，判死时须计入。
- **哑变量与比例字段的 winsorize**：`ceo_chairman_duality_flag` 只有 0/1 两值，winsorize std=4 无副作用，
  但必须先 `ts_mean(…,66)` 再 rank，否则只有两档持仓 → `CONCENTRATED_WEIGHT` 风险。

---

## 7. prod 可剥离性归因（2026-10-21 追加；回答「有没有机会降 prod」）

> 起因：G2 的 IS 面只差 LOW_SHARPE 0.02 / SUB 0.04，而 prod 0.8508 先否决。若共享暴露是**可剥离**的，
> 本应还有一条路；本节用逐年 PnL + prod 直方图把「可剥离 / 不可剥离」判到底。

### 7.1 逐年 PnL 归因（`get_alpha_yearly_stats`，两条同集不同机制）

| 年 | G2 `ZYmKpQ1n`（反向 3m 离任率）PnL / S | M1 `3qjezndX`（ts_rank504）PnL / S |
|---|---:|---:|
| 2014 | 412,868 / 1.97 | 488,547 / 2.09 |
| 2015 | 368,676 / 1.45 | 496,671 / 1.74 |
| 2016 | 121,594 / 0.50 | 179,323 / 0.70 |
| 2017 | 112,753 / 0.43 | 45,647 / 0.23 |
| 2018 | 257,662 / 0.87 | 413,674 / 1.53 |
| 2019 | 315,378 / 1.09 | 574,771 / 2.08 |
| 2020 | **−111,008 / −0.33** | **−498,108 / −1.55** |
| 2021 | **1,733,296 / 3.20** | **1,800,689 / 2.74** |
| 2022 | **1,696,234 / 3.68** | **2,268,172 / 3.05** |
| 2023 | 332,563 / 0.98 | −297,734 / −0.90 |
| **合计** | 5,240,016 | 5,471,652 |

**结论 1：两条不同机制的收益来自同一段时间。** 2021+2022 占 G2 的 **65.4%**、占 M1 的 **74.4%**；
两条在 2020 同时亏（−0.11M / −0.50M）。这不是两个独立信号，而是**同一次 2021–22 行情**的两种表达。

### 7.2 剔除最肥两年后的残余强度

G2 剔除 2021–2022：剩 8 年 PnL 1,810,486（年均 returns 2.24%），逐年 S 均值 **0.87**（最高 1.97，最低 −0.33）。
且平台的 `two_year_sharpe` 覆盖 **2022–2023** ⇒ 剔掉 2022 后 2Y 闸从 2.55 塌到 2023 单年的 0.98。

⇒ **交付所依赖的两个指标（S 1.56 / 2Y 2.55）与 prod 拥挤的来源是同一个对象。**
去掉拥挤 = 去掉交付资格，二者不可分离。

### 7.3 prod 直方图：墙是「一条带」不是「一根针」

| 桶 | G2 `ZYmKpQ1n` | M1 `3qjezndX` |
|---|---:|---:|
| [0.6, 0.7) | 6,732 | 38,223 |
| [0.7, 0.8) | **286** | 10,271 |
| [0.8, 0.9) | **1** | 1,482 |
| [0.9, 1] | 0 | 5 |
| max | 0.8508 | 0.9137 |

G2 的 max 之上只有 **1** 颗生产 alpha，但 max 之下 **[0.7,0.8) 有 286 颗、[0.6,0.7) 有 6732 颗**。
要把 0.8508 压到 <0.70，等于**穿过 286 颗同族**——窗口微调的量级是 ±0.05（`wq-window-valley-break-prod-wall`
的适用前提是「[0.7,0.8) 桶 n=0」，本处 n=286，前提不成立）。

### 7.4 风格中性化救不了：共享暴露不是风格

G2 的 `risk_neutralized_sharpe` = **1.12**，对原始 S 1.56 的保留率 **72%**（M1 为 0.98/1.60 ≈ 61%）。
⇒ 共享暴露**不是**平台的风格/风险因子（若是，rns 会大幅塌陷），而是**同向的同一笔交易**。
风格中性化最多移除 28%，且恰好移不到拥挤的那部分。

### 7.5 裁定

**prod 不可降**，理由是可量化的三条：① 65–74% 的 PnL 集中在同两年；② 剔除该两年后 S≈0.87、2Y 塌到 0.98；
③ 墙是 286 颗的**带**而非单颗，微调量级不够；④ 非风格（rns 72% 保留），风格中性化无效。
⇒ 维持 `USA-BOARD-GOV-STABILITY-PROD-WALL` 封存；**任何「再调调算子/窗口」的复活动议都应被本节直接否决**。

> 唯一真正的出路是**换经济内容**（Mode B），而不是在本形态上降相关——后者不存在可操作的杠杆。

