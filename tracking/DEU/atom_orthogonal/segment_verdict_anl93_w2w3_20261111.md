# DEU / analyst93 Wave 2 收割 + Wave 3 派发（2026-11-11）

## 一、Wave 2 收割（批次 3nUTO1fW74CZbCPfVDBCQUe，10/10 COMPLETE）

设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nan OFF / pasteur ON / unit VERIFY
底字段：`anl93_recprofitabilityprev_analyst_profitability2`（分析师历史推荐盈利能力，VECTOR）

| # | 杠杆 | alpha | S | F | 2Y | sub_u | TO | margin | dd | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| W2-9 | **双统计量 avg+max** | **2rAeP3bN** | **1.52** | **1.47** | **1.41** | **1.14** | 0.0914 | 0.002544 | **0.1329** | ★REVIEW |
| W2-1 | 裸信号+补NaN（消融基线） | omEZQxpE | 1.13 | 1.14 | 0.27 | 0.70 | 0.0629 | 0.004026 | 0.2174 | REVIEW |
| W2-2 | ts_mean 66 平滑 | 9qxkgNv2 | 1.17 | 1.04 | 0.93 | 0.71 | **0.0310** | **0.006332** | 0.1811 | REVIEW |
| W2-3 | 只补NaN不平滑 | KPJZxWdl | 1.22 | 1.10 | 0.70 | 0.73 | 0.0732 | 0.002763 | 0.2020 | REVIEW |
| W2-7 | 单调变换（假杠杆） | WjOJKv6Q | 1.22 | 1.10 | 0.70 | 0.73 | 0.0732 | 0.002763 | 0.2020 | REVIEW（与KPJZxWdl逐位相同）|
| W2-8 | ts_quantile 504 gaussian | Xg9MXd5l | 1.17 | 0.95 | **1.26** | 0.72 | 0.0995 | 0.001653 | **0.1179** | REVIEW |
| W2-4 | 换预测口径 profitabilityprev | e75EeXwJ | 0.94 | 0.74 | 0.35 | 0.60 | 0.0740 | 0.002103 | 0.2035 | REJECT |
| W2-5 | 120日视界 | GrW9EZAo | 0.86 | 0.60 | 0.06 | 0.63 | 0.0580 | 0.002103 | 0.1657 | REJECT |
| W2-10 | 20日视界 | A1VEqoMQ | 0.46 | 0.23 | -0.87 | 0.34 | 0.0810 | 0.000790 | 0.2413 | REJECT |
| W2-6 | profitability1（vs 上次预测） | O0AgKlPg | 0.09 | 0.02 | -0.41 | -0.13 | 0.0868 | 0.000157 | 0.1997 | REJECT |

prescreen：READY 0，REVIEW 6（KPJZxWdl / 9qxkgNv2 / omEZQxpE / WjOJKv6Q / Xg9MXd5l / 2rAeP3bN），REJECT 4。

## 二、三条可复用结论

### ★★★ 1. 均值+极值双统计量合成是 DEU analyst93 的最强杠杆（S +0.27 / 2Y +0.53 / dd -0.07）

同一字段同一轴，只把 `rank(vec_avg(x))` 换成 `add(rank(vec_avg(x)), rank(vec_max(x)))`：
- S 1.25 → **1.52**（+0.27）
- F 1.14 → **1.47**（+0.33）
- 2Y 0.88 → **1.41**（+0.53）
- sub_u 0.76 → **1.14**（+0.38）
- dd 0.2012 → **0.1329**（-0.07）

经济含义：`vec_avg` = 覆盖该股的分析师**群体平均**历史盈利能力（共识质量）；`vec_max` = 该股**最牛的一位**分析师盈利能力（明星背书）。
两者回答的不是同一个问题 —— 前者是「大家都靠谱吗」，后者是「有没有人特别靠谱」。并行叠加而非加权平均，所以是增益不是稀释。
这与 DEU 旧结论「双数据集组腿是稀释不是增益」不矛盾：那条讲的是**两个弱腿等权混合**；这里是**同一字段的两种截面统计量**，信息互补且都来自同源强信号。

### ★★★ 2. `group_rank` 之前套任何单调变换都是假杠杆（零效果）

`group_rank(signed_power(zscore(ts_backfill(x,66)), 0.5), sector)`（W2-7 = WjOJKv6Q）
与 `group_rank(ts_backfill(x,66), sector)`（W2-3 = KPJZxWdl）**全部指标逐位相同**：
S 1.22 / F 1.10 / 2Y 0.70 / sub_u 0.73 / TO 0.0732 / margin 0.002763 / dd 0.2020。

机理：`zscore` 单调、`signed_power(·, 0.5)` 保号单调 ⇒ 复合仍严格单调 ⇒ `group_rank` 后完全等价。
**推论：想在 rank 类分组算子前做非线性尾巴压缩/拉伸，必须先破坏单调性（换成乘法交互、条件门控、或跨字段差值），否则纯浪费算子预算。**

### ★★ 3. profitability2 的唯一有效视界是默认档；profitability1 完全无效

| 口径 | S |
|---|---:|
| profitability2（默认） | 1.13 |
| profitability2_120d | 0.86 |
| profitability2_20d | 0.46 |
| profitability1（默认） | **0.09** |
| profitabilityprev 口径（族切换） | 0.94 |

⇒ `profitability1` 与 `profitability2` 不是同族不同视界，是**不同质量口径**，只有 2 有效。
⇒ 该族不要再试 _20d/_60d/_120d 后缀。

## 三、`2rAeP3bN` 全闸体检

表达式（6 算子）：
```
group_rank(add(rank(vec_avg(anl93_recprofitabilityprev_analyst_profitability2)), rank(vec_max(anl93_recprofitabilityprev_analyst_profitability2))), sector)
```

| 闸 | 值 | 门槛 | 状态 |
|---|---:|---:|---|
| LOW_SHARPE | 1.52 | 1.58 | ✗ 差 0.06 |
| LOW_2Y_SHARPE | 1.41 | 1.58 | ✗ 差 0.17 |
| CONCENTRATED_WEIGHT | — | — | ✗ WARNING |
| LOW_FITNESS | 1.47 | 1.0 | ✓ |
| LOW_SUB_UNIVERSE_SHARPE | 1.14 | 0.72（=0.474×1.52） | ✓ |
| LOW_TURNOVER / HIGH_TURNOVER | 0.0914 | 0.01–0.7 | ✓ |
| CLUSTER_TEST | — | — | ✓ |
| MATCHES_PYRAMID | DEU/D1/ANALYST ×1.8 | — | ✓ |
| SELF_CORRELATION | **0.2659** | 0.7 | ✓（对池 13 个）|
| PROD_CORRELATION | **0.7507** | 0.7 | ✗ 超 0.05 |

### ★★★ prod 撞墙但是「浅钉子」——按纪律可破不能判死

prod 直方图（n 为生产池 alpha 数）：

| 区间 | n |
|---|---:|
| [0.6, 0.7) | **5** |
| [0.7, 0.8) | **1** |
| [0.5, 0.6) | 8 |
| [0.4, 0.5) | 43 |

判据（用户 2026-11-02 纪律）：max < 0.8 + [0.5,0.7) 未成片 ⇒ 浅钉，先归因后定向破墙。
本件：**max 0.7507（超 0.05）+ [0.7,0.8) 桶 n=1 + [0.2,0.4) 仅 542 颗（池体量大）⇒ 典型浅钉**。

## 四、Wave 3 派发（批次 jIVF4064hCcLw11FJDMgT2，10 条）

设计逻辑：Wave 2 揭示 **双统计量 +S/2Y** 与 **时序标准化 +2Y** 两条独立杠杆，Wave 3 = 两者叠加 + 窗口谷网格（一次同时搜 S / 2Y / prod）。

| # | 模板 | 结构 | 算子 |
|---|---|---|---:|
| W3-1 | 双统计量 + ts_quantile 504 | `group_rank(ts_quantile(add(rank(vec_avg),rank(vec_max)),504,gaussian),sector)` | 7 |
| W3-2 | 双统计量 + ts_mean 66 | `group_rank(ts_mean(add(...),66),sector)` | 6 |
| W3-3 | 双统计量 + ts_quantile 252 | 同上换 252 | 7 |
| W3-4 | 双统计量 + ts_mean 22 | 同上换 22 | 6 |
| W3-5 | 先平滑 avg 再合成 | `add(rank(ts_mean(vec_avg,22)), rank(vec_max))` | 6 |
| W3-6 | 三统计量 avg+max+min | `add(add(rank(avg),rank(max)),rank(min))` | 8 |
| W3-7 | 三统计量 avg−stddev+max | 离散度作减项 | 8 |
| W3-8 | max 加权 2 倍 | `add(rank(avg), multiply(2,rank(max)))` | 7 |
| W3-9 | avg 加权 2 倍 | 反向加权 | 7 |
| W3-10 | 双 ts_backfill 后合成 | 各自补 NaN 再合成 | 7 |

验收目标（三轴交集）：S ≥ 1.58 且 2Y ≥ 1.58 且 prod < 0.70。
若 10 条全落 S<1.58 或 prod≥0.7，则 analyst93 容量锁 1 颗（`2rAeP3bN` 作「准交付」保留）。

## 五、analyst48 判死（概念性，未回测）

`analyst48`：cov 0.7879 / 7 字段 / ac 4 / uc 7。7 字段全为**指数层面元数据**：

| 字段 | 含义 | 为何不可用 |
|---|---|---|
| anl48_bbpdiip | 指数点数计价的预计股息 | 指数层，非个股截面 |
| anl48_bulk_count_index_members | 指数成分股数 | 同上 |
| anl48_bulk_idivisor | 指数除数 | 同上 |
| anl48_bulk_indx_typ | 指数类型代码 | 类别码，无经济方向 |
| anl48_index_bulk_ibc | Bloomberg 标识符 | 纯 ID，无经济含义 |
| anl48_index_bulk_nfields | 记录字段数 | 元数据 |
| anl48_index_bulk_return_code | 取数状态码 | 元数据 |

⇒ 无一可构造有方向的个股多空信号。**判死，不占回测预算。**

## 六、analyst47 画像 + Wave 1 就绪（未派发）

`analyst47`：cov 0.6234 / 5 字段全 MATRIX / ac 112 / uc 83。
**众包投资观点**数据集（博主/独立投资人 idea 聚合），与卖方分析师族（anl93/anl9）信息源正交。

| 字段 | cov | ac | 含义 |
|---|---:|---:|---|
| anl47_indicator | **1.0** | 51 | 综合 alpha 指标 1–10 分（越高=买入共识越强）|
| anl47_rawsentiment | 0.5293 | 33 | 原始情绪分量：多/空 idea 计数 + 开平仓状态 |
| anl47_totalrawsignal | 0.5293 | 45 | raw 分量之和 = sentiment + decay + earnings + experts |
| anl47_rawexperts | 0.5293 | 7 | 作者历史表现贡献（最冷门，uc 7）|
| anl47_rawalphadecay | 0.5293 | 9 | idea 年龄/衰减影响 |

**独立信息维度只有 2 个**：`totalrawsignal = rawsentiment + rawalphadecay + rawearnings + rawexperts`（构成恒等式），
外加 `indicator`（独立综合评分）。其余 3 个 raw 分量是 total 的分解项。

10 模板已预检通过（`valid:true` / `unknown_fields:[]` / `platform_field_count=5`）：

| # | 模板 | 算子 |
|---|---|---:|
| 1 | 综合评分裸水平 `group_rank(anl47_indicator,sector)` | 2 |
| 2 | 平滑阶梯 `group_rank(ts_mean(anl47_indicator,22),sector)`（破 1–10 离散并列）| 3 |
| 3 | 原始信号和裸水平 | 2 |
| 4 | 观点方向 `rawsentiment` | 2 |
| 5 | 作者质量 `rawexperts` | 2 |
| 6 | 时效衰减反向 `-group_rank(rawalphadecay)` | 2 |
| 7 | 方向 × 质量交互（multiply） | 5 |
| 8 | 观点改善速度 `ts_delta(ts_backfill(total,22),22)` | 4 |
| 9 | 综合分与原始分背离 `subtract(rank(indicator),rank(total))` | 6 |
| 10 | 门控：只看强买入共识 `trade_when(rank(indicator)>0.7, ...)` | 6 |

## 七、cumulative 状态

- 已判死有数据数据集累计 **32 个**（本轮新增 analyst48；另 analyst46 等属 cov=0 清单）
- 全闸通过 5 颗（未提交）：mLox6Mg2 / E56pROb9 / QPvzNNGG / LLMzYrZe / MPY9VNY9
- 严格单数据集 ATOM 3 颗（QPvzNNGG / LLMzYrZe / MPY9VNY9）
- **准交付 1 颗：`2rAeP3bN`（S1.52/F1.47/2Y1.41/sub_u1.14/dd0.1329/self0.2659，仅差 S 0.06 + 2Y 0.17 + prod 0.05）**
- 在飞 2 批：analyst93 Wave 3（jIVF4064hCcLw11FJDMgT2）+ analyst9 Wave 1（4BxzWUdgB4juc7Sd55dOh5H）

