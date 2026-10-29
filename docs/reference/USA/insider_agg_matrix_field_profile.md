# `insider_agg_matrix` 字段画像与模板库（USA / D1）

> 用途：INSIDERS 塔（USA D1 **0/3，未点亮**）的首波数据集画像 + ≥10 模板库。
> 采集日期 2026-10-29，来源 = 平台 `get_datafields` + 本地 `fields` 台账。

---

## 1. 数据集级画像

| 项 | 值 | 判读 |
|---|---|---|
| dataset id | `insider_agg_matrix` | — |
| category | **INSIDERS** | 非 trio（非 PV/MODEL/OTHER）⇒ 单塔合规，不触塔混禁令 |
| data_type | **MATRIX** | 无需 `vec_*` 包裹 |
| 字段数 | **17** | 全部 MATRIX |
| 覆盖率 | **0.7716（17 个字段逐一相同）** | ⚠ 见 §4 零填充假设 |
| alphaCount | **8** | 全数据集仅 8 条已提交 alpha ⇒ 近乎未开采 |
| 已有回测行（本地库） | 16 | `best_s_in_dataset = null` ⇒ 历史尝试无一达标 |
| valueScore | **4.0** | 平台给的高价值评级 |
| pyramid_multiplier | **1.5** | 点塔 1.5× 加成 |
| userCount 范围 | 1–28 | 极低拥挤 |

**为什么选它**：INSIDERS 塔 0/3，且 `insider_agg_matrix` 的 alphaCount（8）比同 category 的 `insiders3`（33843）低 4 个数量级、比 `insiders4`（1422）低 2 个数量级。`insiders1` 已被判死（`registry_empirical` family_dead 名单），`insider_agg_matrix` 不在判死名单内。

---

## 2. 字段族：4 个"过滤器 × 序统计量"维度

17 个字段不是 17 个独立信号，而是 **`{sign 过滤} × {top 过滤} × {序统计量 1..4}`** 的笛卡尔积。理解这个结构是做模板的前提。

| 族 | 字段 | 语义 | useCount / alphaCount |
|---|---|---|---|
| **方向指示** | `directional_indicator_2` | enhanced insider 活动的**整体方向 / 偏置** | 11 / 13 |
| **有符号序统计** | `directional_significant_value_1..4` | directional significant 交易中**第 1..4 大**的值 | 18/22, 10/14, 3/4, 4/5 |
| **无符号序统计** | `significant_value_1..4` | significant 交易中**第 1..4 大**的值 | 28/37, 8/8, 9/13, 15/17 |
| **top ∩ 有符号** | `top_directional_significant_value_1..4` | top directional significant 中第 1..4 大 | 7/8, 3/3, 1/1, 3/3 |
| **top ∩ 无符号** | `top_significant_value_1..4` | top significant 中第 1..4 大 | 4/4, 3/3, 3/9, 6/6 |

三个可用的对比轴（这是本数据集最稀缺的结构优势）：

1. **有符号 vs 无符号**：`directional_significant_value_k` ÷ `significant_value_k` = "第 k 大交易的方向纯度"。若为负值 ⇒ 最大那笔是**卖出**；正值 ⇒ 买入。**这直接给出方向，无需依赖 `directional_indicator_2`。**
2. **top 过滤 vs 全量**：`top_*_k` ÷ 对应非 top 字段 = "顶级交易的相对主导度"。测"是否只有最大的那几笔才算信号"。
3. **序统计量阶梯 k=1→4**：`value_1 … value_4` 是同一批交易的**降序前四名**，天然可做集中度（HHI）、跨度（v1−v4）、衰减斜率。**这是 MATRIX 数据集里少见的"分布尾部可见"结构。**

---

## 3. 经济学机制（先验，来源为模型知识，未经在线核验）

> ⚠ `web_search` 当前不可用（402 余额用尽），以下文献结论凭模型知识给出，**未做在线核验**，仅作模板设计的方向先验，不作为证据。

| 机制 | 文献结论 | 对应模板 |
|---|---|---|
| 内部人**买入**强信息、**卖出**弱信息（卖出多为分散化/流动性需求） | Lakonishok & Lee (2001); Jeng, Metrick & Zeckhauser (2003) | 方向轴必须保留，不要用 `abs()` 抹平 |
| 只有**大额**内部人交易有预测力 | 同上；"significant" 阈值设计即源于此 | top 过滤轴 |
| **机会型**（opportunistic）交易预测、**常规型**（routine）不预测 | Cohen, Malloy & Pomorski (2012) | top vs 全量对比 ≈ 机会型代理 |
| 多内部人**聚集**交易（clustering）强于单笔 | Alldredge & Cicero (2015) | 序统计量阶梯（k=1..4 都存在 ⇒ 至少 4 笔） |
| 内部人交易后收益在 **1–6 个月**窗口兑现，非日频 | 同上 | 时序平滑窗 66–252，不要用 <22 |

**由此得出的核心设计约束**：本数据集是**低频、稀疏、事件驱动**的 ⇒ 任何日频翻转类骨架（`ts_delta(...,1)`、`ts_mean(...,5)`）必然 TO 爆表（波 170 在邮件数据上已实证这一失败形态）。默认平滑窗取 **66 / 252**，不用 5 / 22。

---

## 4. ⚠ 关键风险假设：序统计量可能零填充

**17 个字段覆盖率逐一等于 0.7716** —— 这在"第 2/3/4 大交易"上不可能自然发生：一只股票当天只有 1 笔内部人交易时，`significant_value_2/3/4` 本应缺失，覆盖率必须低于 `significant_value_1`。

**因此最可能的解释是：缺失的序统计量被填成 0**（而非 NaN）。

**若成立，两个模板会退化**：

| 模板 | 退化表现 | 后果 |
|---|---|---|
| I6 HHI2 = `v1²/(v1²+v2²)` | 绝大多数股票 `v2 = 0` ⇒ 比值 ≡ 1 | 截面无方差，rank 近乎常数 |
| I7 spread = `(v1−v4)/(|v1|+|v4|)` | 绝大多数股票 `v4 = 0` ⇒ 比值 ≡ 1 | 同上 |

**判定方法（本波已内置）**：波 171 批次 1 的 `I6_hhi2` 与 `I7_spread` 若返回 **Sharpe ≈ 0 且 longCount/shortCount 正常**（不是 0 持仓），即证伪"有方差"；若返回大量 NaN / 0 持仓，则证明零填充。

**若证伪，替代设计**（不依赖 v2..v4 的非零性）：
- 用 `ts_covariance(v1, v1, W)` 做 v1 自身的时间方差（`shortinterest3` 上验证有效的二阶矩骨架）；
- 用 `sign(directional_significant_value_1)` 类方向轴做条件，不用比值。

---

## 5. 12 模板库（结构互异，波 171）

差异必须落在**骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换**上，不是换窗口。

| # | 骨架 | 矩 | 信息来源 | 机制假设 |
|---|---|---|---|---|
| **I1** | `group_rank(b(D,66), industry)` | 水平 · 瞬时秩 | 自建（基线） | 内部人净偏置水平预测收益 |
| **I2** | `group_rank(ts_delta(b(D,22),22), industry)` | 一阶差分 | 自建 | 偏置的**变化**（加速）而非水平 |
| **I3** | `group_rank(ts_zscore(b(D,22),252), industry)` | 水平 · 长窗时序归一 | 波 168 E7 迁移（仅继承形状，不继承结论） | 去制度漂移后的偏置 |
| **I4** | `group_rank(ts_rank(b(D,66),504), industry)` | 水平 · 长窗秩趋势 | 波 168 E3（`RREXk770` 全闸骨架） | 偏置在两年分布中的位置 |
| **I5** | `group_rank(ts_mean(D_v1/sv_1,66), industry)` | 比值 · 方向纯度 | 自建（本数据集独有结构） | 最大那笔交易是买入还是卖出 |
| **I6** | `group_rank(ts_mean(v1²/(v1²+v2²),66), industry)` | 二阶 · 集中度 | 波 168 E1 迁移 | 最大交易相对第二大的主导度 |
| **I7** | `group_rank(ts_mean((v1−v4)/(\|v1\|+\|v4\|),66), industry)` | 一阶 · 序统计跨度 | 自建 | 尾部衰减速度 = 交易规模分布形状 |
| **I8** | `group_rank(ts_mean(tdv_1/dv_1,66), industry)` | 比值 · 过滤子集 | 自建 | top 级交易相对全量的主导度（机会型代理） |
| **I9** | `trade_when(rank(b(v1,66))>0.5, group_rank(ts_zscore(b(D,22),252), industry), -1)` | 条件化 | 波 168 E7 + 论坛模板 | 只在内部人活动显著的名字上交易 |
| **I10** | `group_rank(ts_delta(ts_mean(b(D,22),252),66), industry)` | 一阶差分 · 双重平滑 | 波 168 E8 迁移 | 慢制度漂移 |
| **I11** | `group_rank(signed_power(ts_zscore(b(D,22),252), 0.5), industry)` | 非线性 · 保号幂 | 论坛帖 `43620895448343` | 压缩尾部同时保号；**主要目的是降 prod 相关**（论坛实测 0.90→0.64） |
| **I12** | `group_rank(ts_mean(abs(ts_delta(b(D,1),5)),66), industry)` | 一阶差分取绝对值 · 无符号强度 | 波 167（短借绝对一阶矩活）+ 波 168（同形状死） | **对照实验**：活动强度是否含方向外信息 |

其中 `D` = `directional_indicator_2`，`b(f,W)` = `ts_backfill(f,W)`，`v_k` = `significant_value_k`，`dv_k` = `directional_significant_value_k`，`tdv_k` = `top_directional_significant_value_k`。

**模板来源分布**：自建 6 个（I1/I2/I5/I7/I8/I9 的一半）、跨数据集迁移 4 个（I3/I4/I6/I10）、论坛 1 个（I11）、对照实验 1 个（I12）。跨数据集迁移的**只继承骨架形状，不继承"这个形状有效"的结论**——波 168→170 已实证同骨架跨数据集得 S 0.38（vs 源数据集 1.63）。

---

## 6. 本数据集的判据（首波前定死，防事后找理由）

- **近十年覆盖闸**：任一批次出结果后立刻读 `get_alpha_yearly_stats`，**任一年 longCount = 0 ⇒ 该数据集判死**（平台 `coverage` 0.7716 不含时间轴信息，波 168 已实证 `sentiment27` 的 coverage 0.80 却是 2014–2018 全无数据）。
- **持仓数闸**：`longCount + shortCount < 1000` ⇒ 判死（`shortinterest29` 实证：coverage 0.75–1.0 但只 148 只持仓，CW/SUB/2Y 三项必挂）。
- **TO 闸**：任何模板 TO > 30% ⇒ 该模板结构判死，不加 decay 硬救（波 169 实证提/降换手在此类数据上只会砍 S）。
- **出货判据**：S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58 且 invest_ratio ≥ 0.70 且 fRA = 0 且 prod < 0.70。
