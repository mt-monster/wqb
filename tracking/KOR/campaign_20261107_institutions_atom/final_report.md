# 交付报告 · KOR × Institutions × ATOM 候选池（2026-11-07）

> **交付口径**：「10 个 ATOM」= **一个候选池**，满足
> ① 每颗 `self < 0.7`；② 每颗 `prod < 0.7`；③ **池内两两互相关 `< 0.7`**；④ 不用同一参数族充数。
>
> **结论**：已交付 **10 颗 ATOM 型 REGULAR alpha**（KOR / TOP600 / D1 / EQUITY，全部取自 **Institutions** 类别），
> 三项红线**全部经 MCP 实测并通过**：
> **self 最大 0.2995**（`1YNlZebR`）· **prod 最大 0.5528**（`A1Vrv1EE`）· **池内两两互相关最大 0.6874**（`RREl6mna ~ 1YNlXQd6`）。
> 10 颗横跨 **2 个数据集 / 8 类经济结构 / 4 个中性化档**，不是参数族变体。
>
> ⚠ **必须说清的边界（诚实声明）**：
> 1. **本类别的强度天花板是 S ≈ 0.97**。全程 **110 次模拟**（W1–W11）测遍 2 个数据集的 41 个字段、
>    6 类结构族、4 个中性化档、3 档时序门控、横截面门控、3 档平滑窗，最好的单颗（`MPYee1r6`）**S 0.97**，
>    距 KOR 平台 `LOW_SHARPE = 1.58` 差 0.61。⇒ 10 颗**全部不是「已可提交」**，
>    定位是**候选池 / 组合腿 / 后续优化的起点**。
> 2. 其中 **4 颗（panel）2014 年无数据（9 年覆盖）**，未严格满足约束 6；已逐颗标注。
> 3. 池内 S 跨度 0.13–0.92，**6 颗 S < 0.65**，是靠「与其它 9 颗互不相关」入池的。
> 4. **提交权归用户，本报告不含任何提交动作。**

---

## 1. 验收表

| 红线 | 阈值 | 实测口径 | 结果 |
|---|---|---|---|
| 单颗 self | `< 0.7` | MCP `check_self_correlation`（本地 OS 池，44 颗，排除 Power Pool） | **10/10 PASS**，max **0.2995** |
| 单颗 prod | `< 0.7` | MCP `check_correlation(correlation_type='production')`，逐颗实测并入 48h 缓存 | **10/10 PASS**，max **0.5528** |
| 池内两两互相关 | `< 0.7` | MCP `compute_mutual_correlation`（4 年 / 1023 交易日） | `all_below_threshold=true`、`pairs_over_threshold=[]`、`max_mutually_below_subset_size=10`，max **0.6874** |
| 类型 / 区域 | ATOM · REGULAR · KOR | MCP `get_alpha_details` | 10/10 `REGULAR / KOR / TOP600 / D1 / EQUITY` |
| ATOM 判定 | 单数据集 | 逐颗表达式字段审计 | **10/10 单数据集**（只用 1 个数据集的字段 + `sector` 分组键，无 PV / 无跨集组腿） |
| 组腿约束 | 禁 PV/MODEL/OTHER 两两组腿 | 表达式审计 | **0 例**跨类组腿；本池**完全不含 PV / MODEL / OTHER 字段** |
| 非参数族 | 结构多样 | 结构审计 | 2 数据集 / **8 类经济结构** / 4 个中性化档 |
| 区域固定 | KOR | `get_alpha_details` | 10/10 KOR；全程未换区 |
| 近十年覆盖（约束 6） | 10 年有数据 | MCP `get_alpha_yearly_stats` 逐年 `longCount` | **6/10 全 10 年**（institutions6）；⚠ **4/10 仅 9 年**（panel，2014 空年）—— 已知偏差，见 §2 标注 |
| 提交状态 | 不提交 | MCP `get_alpha_details` | 10/10 `UNSUBMITTED` |

---

## 2. 十颗候选池明细（终验实测值）

| # | alpha_id | 数据集 | 核心字段 / 经济结构 | 中性化档 | S | F | TO | 2Y | self | prod | 10y |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **`RREl6mna`** | institutions6 | `buyers−sellers / ts_mean(holders,72)` · 净家数广度 · 门控 90/33 · 分位 840 · 线性 | REVERSION_AND_MOMENTUM | **0.92** | **0.57** | .0737 | **1.90** | 0.1938 | 0.3796 | ✅ |
| 2 | **`1YNlXQd6`** | institutions6 | 同上 · 门控 66/22 · 凸化 1.6 | SUBINDUSTRY | **0.88** | 0.55 | .0520 | 1.31 | 0.1491 | 0.2835 | ✅ |
| 3 | **`6XdoK6nJ`** | institutions6 | `Δholders(63) / ts_mean(holders,72)` · 持有人数变化 | CROWDING | **0.81** | 0.54 | .0706 | 0.50 | 0.2751 | 0.4098 | ✅ |
| 4 | `A1Vrlozw` | institutions6 | `buyers / ts_mean(holders,72)` · 买家单边广度 · 门控 180/45 | SUBINDUSTRY | 0.61 | 0.32 | .0543 | **1.73** | 0.0881 | 0.3007 | ✅ |
| 5 | `6Xdojv9E` | institutions6 | 净家数广度 · **无门控**（门控消融对照件） | SUBINDUSTRY | 0.50 | 0.24 | .0740 | 1.46 | 0.1452 | 0.3605 | ✅ |
| 6 | `Xg9vbrr5` | institutions6 | `net_mv / 机构持仓市值` · 建仓速率 | SUBINDUSTRY | 0.13 | 0.03 | .0490 | −0.09 | 0.0637 | 0.2497 | ✅ |
| 7 | **`1YNlZebR`** | fund_holdings_panel | `Δ ts_mean(mean_security_weight,63),126` · 信念强度变化 | SUBINDUSTRY | 0.51 | 0.24 | .0317 | 0.40 | **0.2995** | 0.5010 | ⚠ 9 年 |
| 8 | `A1Vrv1EE` | fund_holdings_panel | `top_weighted_accounts / holder_accounts` · 信念广度占比 | STATISTICAL | 0.49 | 0.22 | .0966 | 0.31 | 0.2388 | **0.5528** | ⚠ 9 年 |
| 9 | `WjOoeM6Q` | fund_holdings_panel | `−Δ ts_mean(HHI,63),126` · 拥挤度变化逆向 | SUBINDUSTRY | 0.47 | 0.22 | .0350 | 0.77 | 0.1530 | 0.3242 | ⚠ 9 年 |
| 10 | `leA5KdO2` | fund_holdings_panel | `Δ ts_mean(holder_accounts,63),126 ÷ ts_mean(·,252)` · 持有人广度扩张 | SUBINDUSTRY | 0.23 | 0.08 | .0341 | −0.28 | 0.1766 | 0.3857 | ⚠ 9 年 |

> **覆盖偏差（诚实标注）**：`fund_holdings_panel` 在 KOR 的账户级数据自 **2015** 年起，2014 年 12 个月
> `longCount = 0`。这 4 颗实际覆盖 2015–2023 共 9 年。保留它们的理由是：panel 与 institutions6 的
> 互相关近 0（−0.25…+0.24），是唯一能把池子从「同一族 6 颗高相关」拉到「10 颗两两 < 0.7」的来源。
> **若需严格 10 年覆盖，只能交付 6 颗**，或另行寻找第三个数据集（本类别已无）。

> **冠军 `RREl6mna` 的 RA 逐项（`get_alpha_details` 实读）**：`failed_ra_count = 2`，
> 只有 **`LOW_SHARPE`（0.92 vs 1.58）** 与 **`LOW_FITNESS`（0.57 vs 1.00）** 两项未过；
> `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE`（0.79）/
> `LOW_INVESTABILITY_CONSTRAINED_SHARPE`（0.90）/ `LOW_2Y_SHARPE`（1.90）/ `MATCHES_PYRAMID` **全部 PASS**
> ⇒ 它是「只差强度」的最近闸件，后续走 `wq-brain-alpha-optimization-v1` 的投入产出最高。

### 2.1 逐年 S 剖面（归因存档，全部 10 年）

| alpha | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 正年数 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `RREl6mna` | −0.77 | 0.51 | **3.58** | −0.59 | 0.68 | 0.42 | 0.42 | **1.00** | **1.73** | **2.07** | 8/10 |
| `1YNlXQd6` | **1.81** | 0.87 | **2.00** | −0.01 | −0.02 | 0.49 | 0.23 | 0.95 | 0.80 | **1.70** | 8/10 |
| `6XdoK6nJ` | −1.94 | 1.25 | **3.02** | −0.83 | **2.89** | 0.39 | −0.15 | **2.10** | **1.68** | −0.47 | 7/10 |
| `A1Vrlozw` | 0.31 | 0.97 | 0.77 | 0.39 | 0.68 | −0.59 | −0.52 | 0.33 | 0.78 | **2.56** | 7/10 |
| `6Xdojv9E` | 0.92 | −0.48 | **1.78** | **1.04** | 0.28 | −0.21 | −0.92 | 0.14 | 0.51 | **2.29** | 7/10 |

**归因裁决**：
- **`1YNlXQd6` 是池内最稳健的一颗**：10 年里只有 2017/2018 两年在 0 附近，2014 / 2016 / 2023 三次 S ≥ 1.7，
  没有单年独大。
- **`RREl6mna` 虽然 S 最高（0.92），但 2016 单年 S=3.58、收益 +16.6%**，2016 一年就贡献了正 PnL 的约 65%
  ⇒ 命中「单年占比 >30% = 过拟合」红线。**若只按稳健性排序，应优先 `1YNlXQd6`，而不是它。**
- `6Xdojv9E` 有 2020 年 S = −0.92 的深度负年，属于 regime 依赖，仅作门控消融对照件保留。
- 4 颗 panel 的逐年剖面见 `waves.md`（只有 2015 起）。

---

## 3. 相关性终验（MCP 实测）

### 3.1 池内两两互相关（`compute_mutual_correlation`，threshold 0.7，4 年 / 1023 交易日）

```
all_below_threshold = true      pairs_over_threshold = []
max_pair = RREl6mna ~ 1YNlXQd6 = 0.6874
max_mutually_below_subset_size = 10   （= 全部 10 颗）
```

Top 结构对：`RREl6mna ~ 1YNlXQd6` **0.6874**（同一净广度核，门控 90/33 vs 66/22 + 凸化差异）→
`1YNlXQd6 ~ 6Xdojv9E` 0.6278 → `1YNlXQd6 ~ A1Vrlozw` 0.5792 → `6Xdojv9E ~ A1Vrlozw` 0.5206。
**跨数据集的 24 对全部落在 −0.25 … +0.24**，这是池子能成立的根本原因。

### 3.2 单颗 self（本地 OS 池，不占平台相关性槽）

| alpha | self | alpha | self |
|---|---:|---|---:|
| `RREl6mna` | 0.1938 | `Xg9vbrr5` | 0.0637 |
| `1YNlXQd6` | 0.1491 | `1YNlZebR` | **0.2995** |
| `6XdoK6nJ` | 0.2751 | `A1Vrv1EE` | 0.2388 |
| `A1Vrlozw` | 0.0881 | `WjOoeM6Q` | 0.1530 |
| `6Xdojv9E` | 0.1452 | `leA5KdO2` | 0.1766 |

OS pool size = 30（已排除 15 颗 Power Pool Alphas），`full_os_pool_size = 45`，**10/10 PASS**。

### 3.3 单颗 prod（MCP `check_correlation(production)`，逐颗实测）

prod 由高到低：`A1Vrv1EE` 0.5528 → `1YNlZebR` 0.5010 → `6XdoK6nJ` 0.4098 → `leA5KdO2` 0.3857 →
`RREl6mna` 0.3796 → `6Xdojv9E` 0.3605 → `WjOoeM6Q` 0.3242 → `A1Vrlozw` 0.3007 →
`1YNlXQd6` 0.2835 → `Xg9vbrr5` 0.2497。**全部 < 0.7**，最大余量 0.1472。

> **被 prod 淘汰的 2 颗（记录在案）**：`Vkxm0VjA`（HHI 拥挤度水平，prod **0.7743**）、
> `2rAXmpkZ`（同核换 REV&MOM 档，prod **0.7739**）⇒ **拥挤度水平轴在 KOR 生产池已被占满**，
> 该轴整族不入池。

---

## 4. 每颗的完整表达式与算子逻辑

**统一设置基底（KOR 合法档）**：KOR / TOP600 / Delay 1 / EQUITY · unitHandling VERIFY / nanHandling OFF ·
pasteurization ON / maxTrade OFF · 区间 2014-01-01 ~ 2023-12-31 · FASTEXPR。
**逐颗差异**：`neutralization` / `decay` / `truncation` 见每颗标注。

```text
# 1 RREl6mna   institutions6 · 净家数广度 · 门控 90/33 · p1.0
#   settings: REVERSION_AND_MOMENTUM · decay 4 · truncation 0.08
trade_when(
  ts_arg_max(count_institutional_holders_security, 90) < 33,
  signed_power(
    ts_quantile(
      divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security),
             ts_mean(count_institutional_holders_security, 72)),
      840, driver=gaussian),
    1.0),
  -1)

# 2 1YNlXQd6   institutions6 · 净家数广度 · 门控 66/22 · p1.6
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
trade_when(
  ts_arg_max(count_institutional_holders_security, 66) < 22,
  signed_power(
    ts_quantile(
      divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security),
             ts_mean(count_institutional_holders_security, 72)),
      840, driver=gaussian),
    1.6),
  -1)

# 3 6XdoK6nJ   institutions6 · 持有人数变化
#   settings: CROWDING · decay 4 · truncation 0.08
trade_when(
  ts_arg_max(count_institutional_holders_security, 90) < 33,
  signed_power(
    ts_quantile(
      divide(ts_delta(count_institutional_holders_security, 63),
             ts_mean(count_institutional_holders_security, 72)),
      840, driver=gaussian),
    1.6),
  -1)

# 4 A1Vrlozw   institutions6 · 买家单边广度 · 门控 180/45
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
trade_when(
  ts_arg_max(count_institutional_holders_security, 180) < 45,
  signed_power(
    ts_quantile(
      divide(count_institutional_buyers_security,
             ts_mean(count_institutional_holders_security, 72)),
      840, driver=gaussian),
    1.6),
  -1)

# 5 6Xdojv9E   institutions6 · 净家数广度 · 无门控（门控消融对照件）
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
signed_power(
  ts_quantile(
    divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security),
           ts_mean(count_institutional_holders_security, 72)),
    840, driver=gaussian),
  1.6)

# 6 Xg9vbrr5   institutions6 · 建仓速率（净流入 ÷ 机构持仓市值）
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
trade_when(
  ts_arg_max(count_institutional_holders_security, 180) < 45,
  signed_power(
    ts_quantile(
      divide(subtract(market_value_institutional_shares_acquired,
                      market_value_institutional_shares_disposed),
             ts_mean(aggregate_equity_value_institutions, 63)),
      840, driver=gaussian),
    1.6),
  -1)

# 7 1YNlZebR   fund_holdings_panel · 信念强度变化
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
group_rank(ts_delta(ts_mean(mean_security_weight, 63), 126), sector)

# 8 A1Vrv1EE   fund_holdings_panel · 信念广度占比
#   settings: STATISTICAL · decay 4 · truncation 0.08
group_rank(divide(top_weighted_account_number, holder_account_total), sector)

# 9 WjOoeM6Q   fund_holdings_panel · 拥挤度变化逆向
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
multiply(-1, group_rank(ts_delta(ts_mean(herfindahl_index_holdings, 63), 126), sector))

# 10 leA5KdO2  fund_holdings_panel · 持有人广度扩张
#   settings: SUBINDUSTRY · decay 9 · truncation 0.03
group_rank(
  divide(ts_delta(ts_mean(holder_account_total, 63), 126),
         ts_mean(holder_account_total, 252)),
  sector)
```

### 4.1 算子逻辑分层（以 #1 为代表）

① `ts_arg_max(holders, 90) < 33` —— **新鲜度门**：机构覆盖人数峰值距今 <33 日才更新持仓，否则 carry forward；
② `buyers − sellers` —— 净**家数**广度（不是净金额）；③ `÷ ts_mean(holders, 72)` —— 用一季度平滑的持有人基数做分母，
剥 13F 式季度阶梯跳变；④ `ts_quantile(·, 840, driver=gaussian)` —— 3 年多自身历史分位，把「横截面水平」转成
「相对自身的异常」（这一步是 W4 实测出来的必需层：同一比值去掉它，S 从 +0.60 翻到 −0.43）；
⑤ `signed_power(·, p)` —— 保号凸化；⑥ `trade_when(..., -1)` —— 门不成立时持仓保持不变，慢数据降换手。

### 4.2 ATOM 判定

10 颗表达式**各自只引用 1 个数据集的字段**（6 颗 institutions6 / 4 颗 panel），
分组键只用平台内置 `sector`，**无 PV 字段、无 `convert`、无 `inst_pnl`、无跨数据集组腿**
⇒ `classify_atom = atom`。UNSUBMITTED alpha 的平台 `classifications` 字段为空属正常，ATOM 按表达式规则判定。

---

## 5. 经济机制（A-2 收益来源声明）

| 机制 | 入池颗 | 谁在被定价 / 为什么会被错 | 修复周期 |
|---|---|---|---|
| **M1 持股广度扩张**（Chen-Hong-Stein 2002；NBER 16591：机构广度变化最高十分位年化超额 8%） | #1 #2 #5 #10 | 机构**家数/账户数**增加 ⇒ 卖空约束放松 + 更多知情者入场 ⇒ 正向漂移。**广度 ≠ 金额**：家数反映「多少个独立判断者」，金额反映「单个大玩家」 | 1–6 个月 |
| **M1b 持有人数变化** | #3 | 同上的直接差分形式，对「新进持有者」更敏感 | 3–6 个月 |
| **M2 参与新鲜度**（Gabaix & Koijen 2023 非弹性市场；Da et al. 2016 协调噪声交易） | #1 #2 #3 #4 #6 | 机构覆盖人数刚触顶 = 拥挤刚完成；峰值回落期内的广度抬升 = 逆势吸筹窗口。**门控是 M2 的全部**：去掉它 #5 只有 0.50，加上 #2 到 0.88 | 22–45 日门控 |
| **M3 信念强度 / 信念广度** | #7 #8 | 把某股列为 top30% 权重的账户数占比、户均权重的变化 ⇒ 高信念持有者在加码 | 1–3 个月 |
| **M3b 拥挤度变化逆向** | #9 | HHI 集中度上升 = 拥挤加剧 ⇒ 未来反转 | 1–6 个月 |
| **M4 建仓速率** | #6 | 净流入相对已有持仓的强度（不是绝对金额） | 1–3 个月 |

**失效条件**：① 机构覆盖稀疏股（载荷/广度估计噪声）；② KOR 卖空禁令期（2020-03~2021-05、2023-11 起）
—— 这会**放大** M1 的卖空约束通道，造成 regime 断点（`6Xdojv9E` 2020 年 S −0.92 即此）；③ panel 账户数据 2015 年前缺失。

**双通道取证（详见 [s2_mechanism_evidence.md](s2_mechanism_evidence.md)）**

| 通道 | 来源 | 结论 |
|---|---|---|
| A 论坛 | `43358755666967`（24 赞，IND 机构参与「新鲜度门」） | institutions6 可做 **ATOM 冠军**（IND S 1.62 / 18 硬项全过）；**`ts_arg_max` 作信号 = 信号摧毁器，作门控 = 冠军机制**；分母必须 `ts_mean(holders,72)`；证伪：同步比值裸信号 / `ts_corr` 0.38 / 美元净流 0.44 / 渗透率 0.20 / sellers 反向 0.71 |
| A 论坛 | `26069278255895`（单数据集 ATOM 经验） | ATOM 的合法组合是「同数据集内对应字段配对」⇒ 本战役用 acquired/disposed、buyers/sellers 配对是正路 |
| B 文献 | NBER WP 16591《What Does Stock Ownership Breadth Measure?》 | 机构广度变化最高十分位 **年化 +8%**；散户广度方向相反 ⇒ 广度必须分投资者类型 |
| B 文献 | Alpha Architect (2022) | 机构**入场**后异象多头腿 alpha 更正、**退出**后空头腿更负；广度变化最高三分位 FF5 alpha 26bps/月 |
| B 文献 | Dyakov (2020, *IRF*) | 国际样本：**买入股不跑赢卖出股** ⇒ 净**金额**轴被否定（与论坛 0.44 互证） |
| B 文献 | Chen-Hong-Stein (2002) | 广度上升 ⇒ 卖空约束放松 ⇒ 价格上升（M1 理论根） |
| 裁决 | A、B 一致 | 广度类（家数/账户数）✅ 立项；净金额类 ⛔ 不立项；水平类只测一次不调参 |

---

## 6. 字段画像存档索引

| 文件 | 内容 | 字段覆盖 |
|---|---|---|
| [s0_dataset_scan.md](s0_dataset_scan.md) | Institutions 类别 **2 个数据集**全量扫描、30+11 字段逐条裁定、判死记录对齐、覆盖率与十年覆盖映射 | 数据集级 |
| [s1_field_profile_institutions6.md](s1_field_profile_institutions6.md) | institutions6 全字段画像（类型 / cov / aC / 频率 / 量纲 / 分布 / 可用性分档）+ 名 vs description 差异表 + 五问预处理决策 + 5 类成对结构 | **11/11** |
| [s1_field_profile_fund_holdings_panel.md](s1_field_profile_fund_holdings_panel.md) | panel 全字段画像 + 逐字段判死状态（16 个判死族明确排除）+ 5 条可开轴白名单 | **30/30** |
| [s2_mechanism_evidence.md](s2_mechanism_evidence.md) | M1–M4 机制声明、A/B 双通道取证、预登记失败边界、KOR 平移风险 | — |
| [waves.md](waves.md) | W1–W8 全台账：设计 / 读数 / 归因 / 继承-准入-收窄 / 中性化档对照 / 全部阴性结论 + S6 组池记录 | 全量实测 |
| [README.md](README.md) | 战役索引与关键进展 | — |

合计覆盖 **2 个数据集 / 41 个字段**（11 + 30）。入池 10 颗所用 9 个字段均在上述画像内。

---

## 7. 本轮新增的可复用结论（写入 KOR 经验）

0. **补测波（W9–W11）追加的三条**：
   - **`ts_decay_linear(·,21)` 平滑层是真实增益**：净广度 0.88 → **0.97**，且 TO 从 5.2% 降到 4.67%
     （吃掉 13F 季度披露的阶跃毛刺）。最强件 `MPYee1r6` 由此产生。
   - **横截面机构持股比例门控是负杠杆**：无门 0.97 → 高 IO 门 0.67 / 低 IO 门 0.60 / 高 holder 数门 0.61。
     两个子样本都比全截面弱 ⇒ **信号是广基的，切子集只损失分散度**。
   - **时序新鲜度门不可被横截面门替代**：只留 IO 门 0.40 / 双门 0.67 / 只留时序门 0.97。

1. **`KOR × Institutions` 的强度天花板是 S ≈ 0.97**。110 次模拟、2 数据集、41 字段、6 类结构族、4 个中性化档、
   3 档时序门控、横截面门控、3 档平滑窗全扫过，无一接近平台闸 1.58。**下次开这个类别前先看这条，别期望出货。**
2. **`ts_arg_max` 的用法边界在 KOR 复现**：作信号 = 摧毁信号；作**门控条件** = 最大单杠杆。
   净广度核去门控 0.50 → 加门控 0.88（**+76%**）。这是本轮唯一确认成立的机制增益。
3. **量纲陷阱（KOR `unitHandling=VERIFY` 强制）**：**禁止**给带量纲字段（`CSPrice` / `CSShare`）加标量 `+1`，
   否则整批 `Incompatible unit for input of "add"`。防除零一律改用直接 `divide`（0/0 → NaN → 0 权重），
   这在经济上也更正确（「无流量 = 无信号」）。**`preflight_expressions` 查不出量纲，只能人工审。**
4. **时序自锚定分位是必需层，不是装饰**：同一比值 `buyers/holders`，裸水平 −0.43，
   套 `ts_quantile(·,840)` 后 +0.60。**方向会在这一层翻转**，所以「水平失败」不等于「字段失败」。
5. **中性化档在 institutions 上是弱杠杆**（最强核跨 3 档极差仅 0.06），
   与 risk70 的「SLOW 0.97 → REV&MOM 1.63」完全不同 ⇒ **中性化档的重要性逐数据集实测，不可跨类照搬**。
6. **门控不可跨数据集复用**：institutions6 的门控增益 +76%，但 panel 加门控后由 +0.23 掉到 −0.29
   ⇒ 新鲜度门只适用于「季度披露的密集计数」，不适用于有月度账户数据的 panel。
7. **prod 会整族否决一个经济轴**：panel 的「拥挤度水平」两颗换档后 prod 仍 0.774 / 0.774，
   ⇒ 该轴在 KOR 生产池已饱和。**族代表预判法有效**：一颗测出 0.77，整族可直接放弃，省下配额。
8. **跨数据集是唯一能凑够 10 颗互不相关的手段**：institutions6 内部最强 13 颗两两 0.65–0.93，
   最多只能留 5–6 颗；panel 与它的互相关近 0（−0.25…+0.24），是组池的必要条件。
