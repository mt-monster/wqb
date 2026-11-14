# ★定稿：insiders1 ATOM 真实天花板 = S 1.30（13 颗实测）

日期：2026-11-12
用户指令：「锁定 insiders 挖掘 ATOM」
方法：从历史 36 个 insd1 族件中按「塔数=1」筛出真 ATOM，逐个读指标

## 一、13 颗真 ATOM 的完整排名（全部 REGULAR / 单塔 INSIDERS）

| alpha | S | F | Y2 | sub | 构造 |
|---|---:|---:|---:|---:|---|
| **O0WO22Vv** | **1.30** | 1.19 | 1.08 | 0.56 | A+B + ts_target_tvr_decay |
| **pwamppGx** | **1.30** | 1.19 | 1.08 | 0.55 | A+B + ts_target_tvr_hump |
| blaXKjkR | 1.15 | 1.02 | 1.26 | 0.36 | ts_ir(vec_stddev)+ts_ir(vec_avg) |
| xAvqEj6p | 1.08 | 0.91 | 1.08 | **0.61** | ts_ir(vec_sum)+ts_ir(vec_avg) |
| 1YWe2weM | 1.07 | 0.94 | 0.62 | 0.15 | ts_ir(vec_range) |
| 0mPqawO1 | 1.02 | 0.84 | 0.93 | 0.30 | ts_ir(vec_max) |
| ZYa617Pd | 1.02 | 0.83 | 0.96 | 0.59 | ts_ir(vec_sum) |
| leadNjdO | 0.99 | 0.80 | **1.44** | 0.30 | ts_ir(vec_min) |
| 88Nb20em | 0.90 | 0.52 | **2.01** | 0.52 | 短窗高 Y2 变体 |
| O0WO27OJ | 0.90 | 0.75 | 1.09 | -0.07 | ts_ir(vec_stddev) |
| qM78wj8P | 0.67 | 0.45 | 0.70 | 0.53 | ts_ir(vec_count) |
| e7amWzpg | 0.64 | 0.38 | 0.47 | 0.55 | vec_count + Delta |
| zqdZL8L1 | 0.56 | 0.29 | 0.30 | 0.50 | A + ts_corr 腿 |

**最高 S = 1.30，闸线 1.58 => 缺口 0.28。**

## 二、覆盖度说明（这不是「没试够」）

这 13 颗已覆盖：
- **7 种 vec_* 聚合**（avg / sum / max / min / range / count / stddev）
- **5 种时序形态**（Delta / ts_ir / lvl / ts_rank / ts_corr）
- **6 个字段**（holdings / valueeur / shares / price / tradesignificance / value）
- **平滑算子**（ts_target_tvr_hump / decay）
- **正交化**（vector_neut 得 1.33，但属跨形态故未列此表）

=> 算子层面已穷尽，天花板来自**信息量**：
- 6 个字段同源（同一条交易记录）
- 覆盖率 53.4%（可用标的约 267 只）
- 禁 `cap` 桶（否则失 ATOM）=> 失去市值分层中性化

## 三、禁止的提分手段（ATOM 硬约束）

| 手段 | 效果 | 为什么不能用 |
|---|---|---|
| 加 `bucket(rank(cap))` | sub 0.63->0.90 | **引入 PV 塔 => 非 ATOM** |
| 加 analyst 腿（starmine）| S 1.30->2.36 | 引入 MODEL 塔 => 非 ATOM |
| 跨 `insider_agg_matrix` 的 HHI | S 贡献 +0.3 | 第二数据集 => 非 ATOM |

## 四、结论

**在 DEU insiders1 上，ATOM 的 S 天花板 = 1.30，达不到平台 1.58 门槛。**

| 守什么 | 上限 |
|---|---:|
| 只守 ATOM | **1.30** |
| 放宽到跨数据集 | **2.36**（已实测，18 颗可交付）|

**这不是投入量问题，是结构性互斥。**

## 五、唯一残余可能：用高 Y2 换 S

表里有反相关：
- `88Nb20em`：S 0.90 但 **Y2 2.01**
- `leadNjdO`：S 0.99 但 **Y2 1.44**
- `O0WO22Vv`：S 1.30 但 Y2 1.08

=> 存在「低 S + 高 Y2」形态。若能把 S 从 0.90 提到 1.58 且保住 Y2>=1.58，就是 ATOM 成品。
但 S 从 0.90 到 1.58 需 +0.68，比从 1.30 到 1.58（+0.28）更难。
=> 除非找到**近两年强势且全期也强**的 insiders 机制，否则无解。