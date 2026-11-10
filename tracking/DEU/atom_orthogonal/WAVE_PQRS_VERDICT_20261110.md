# DEU 第三席寻觅：波 P~R 归因 + 覆盖判据（2026-11-10 午后）

## 一、波 P / Q：snt7（Wikipedia）× snl27（Tranco）双腿 vector_neut

### 波 P（8 条，sim 3G9GC6dqI4Jq8GL146DORyb）
复刻 OS 已出货件 bl6OWZ2M 的完整骨架（`vector_neut(ts_quantile(ts_ir(ts_mean(snt7,5),22),252), snl27_relpopularity08)`）：

| 候选 | S | 2Y | 备注 |
|---|---:|---:|---|
| gJenJGMO | 1.22 | 1.52 | IS_LADDER_SHARPE FAIL |
| 1YNrYK7M | 1.18 | 1.53 | IS_LADDER_SHARPE FAIL |
| LLM0Lzp2 | 1.19 | 1.45 | IS_LADDER_SHARPE FAIL |
| VkxAkzPV / 6Xd5X09O / 0mY1mgEk / ZYQOYznY | 1.12~1.19 | 1.31~1.46 | 同上 |

⇒ **双腿 vector_neut 结构有效但强度不足**（对比波 O 单腿 S ≤ 0.77 且符号混乱）。
⇒ 判据：**腿间正交化本身贡献了大部分信号**，单腿拆测会误判为无信号。

### 波 Q（8 条，sim la1pb7n24Dlahi14KLjfOpu）—— 出货但有致命硬伤

| 候选 | S | F | 2Y | TO | 结论 |
|---|---:|---:|---:|---:|---|
| **wpQ0prQY** | **1.78** | 1.44 | 2.12 | 0.1381 | **四闸全过**，但见下 |
| 6Xd5XkdP | 1.32 | 0.86 | 1.36 | — | 强度不足 |
| 其余 6 条 | 1.13~1.21 | — | 1.31~1.49 | — | 强度不足 |

**wpQ0prQY 表达式**：`vector_neut(ts_quantile(ts_ir(ts_mean(ts_backfill(vec_avg(snt7_all_languages_views), 22), 5), 33), 252), ts_backfill(vec_avg(snl27_relpopularity08), 22))`
（相对波 P 只把 ts_ir 的 IR 窗口 22 → 33）

### ★ wpQ0prQY 的两个致命硬伤（不可提交）

**硬伤 1：连续五年空窗 —— 违反 goal「近十年都要有数据」**

| 年 | PnL | Sharpe | longCount |
|---|---:|---:|---:|
| **2014** | **0** | 0.0 | **0** |
| **2015** | **0** | 0.0 | **0** |
| **2016** | **0** | 0.0 | **0** |
 **2017** | **0** | 0.0 | **0** |
| **2018** | **0** | 0.0 | **0** |
| 2019 | 684,691 | 1.48 | 84 |
| 2020 | 239,343 | 0.47 | 116 |
| 2021 | 1,290,764 | 2.54 | 150 |
| 2022 | 1,465,068 | 2.85 | 161 |
| 2023 | 807,742 | 1.45 | 108 |

⇒ 排除理由写「**连续空窗 5 年（2014-2018）**」，不写「短历史」。
（且有效历史仅 5 年 ⇒ 近三年 CV 闸口径也不成立。）

**硬伤 2：self = 0.7412 与已提交件 bl6OWZ2M 撞车** ⇒ FAIL（阈值 0.7）

⇒ **wpQ0prQY 判死，不作为交付件。**

## 二、★ 波 R：覆盖探针 —— 定位空窗根因（关键判据 MJ）

5 条 snl27 单腿（`group_rank(ts_mean(ts_backfill(vec_avg(x),132),22), subindustry)`）：

| 候选 | 字段 | S | longCount | 2Y |
|---|---|---:|---:|---:|
| WjOv18kP | snl27_relpopularity1 | 0.60 | **157** | 1.05 |
| 9qxNZ0oq | snl27_relpopularity08 | 0.55 | **157** | 1.20 |
| RREGjWX0 | snl27_totaldomains | 0.50 | **155** | 1.47 |
| 78Le79Vv | snl27_avgranking | 0.17 | **157** | 0.11 |
| ZYQOPGZj | snt27_rank | 0.12 | **157** | 0.13 |

### 判据 MJ（★ 跨区通用，本轮最高价值的方法论修正）
**空窗根因是「数据源自身的起始年」，不是「算子结构」。**

- **snl27（Tranco 域名排名）：longCount 155~157 ⇒ 2014-2018 有数据**，
  所以用 snl27 做的件覆盖是满的（波 R 全部 longCount ≥ 155）。
- **snt7（Wikipedia 浏览量）：2019 年才起** ⇒ 与 snl27 组合后
  只要 snt7 参与运算，整个件的前 5 年被 snt7 的 NaN 拖死（wpQ0prQY longCount=0）。

⇒ **规则（覆盖前置校验）**：
1. 派发前必须确认**表达式里每个数据源的起始年**，而不只看字段画像的 cov（cov 是当期覆盖，不反映历史起点）。
2. **多腿表达式里只要有一腿起始年晚 ⇒ 整件受该腿拖累**，空窗无法靠 backfill 修复
   （backfill 只能向前填已有值，不能凭空造出历史上不存在的数据）。
3. 校验手段：`get_alpha_yearly_stats` 看 longCount 逐年；或先跑单腿探针波（本次波 R 5 条）
   用 longCount 反推各源的可用起始年。
4. **空窗是 goal 硬约束（近十年都要有数据）的直接杀手，比 S/F/2Y 更优先** ——
   S1.78 四闸全过的件照样因 5 年空窗而出局。

## 三、波 S（已派出）：snl27 × snl27 双腿

基于判据 MJ，把 snt7 腿完全替换为 snl27 内部第二字段
（relpopularity08 / relpopularity1 / avgranking / totaldomains / topranking / skewness / kurtosis），
保留波 Q 出货的 ts_ir 窗口 33 + ts_quantile 252 结构 ⇒ 目标是**保持 S 强度同时恢复满覆盖**。

## 四、本轮方法论增量（Agent Memory）

新增判据：
- **MG**：族级判死看符号一致性（全负=方向反 / 混合=真噪声）。
- **MF**：同机制已有已出货数据源时，新源直接判死。
- **MI**：事件型数据集必须先 ts_backfill 转面板，否则截面样本不足。
- **MJ（★）**：**覆盖空窗的根因是数据源起始年，不是算子结构**；多腿件只要一腿起始年晚就整件空窗；
  派发前先查每个源的起始年（单腿探针波 + longCount 逐年），cov 不反映历史起点。
- **MK**：复刻已出货骨架时不要拆腿单测（腿间正交化贡献大部分信号）。
