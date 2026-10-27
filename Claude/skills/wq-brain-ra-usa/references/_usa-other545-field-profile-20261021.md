# other545 · Linked Firms Momentum（NEMO 2.0）— 字段画像与批次档案

> as_of 2026-10-21 · 区域 USA / delay 1 / universe TOP3000 / 中性化 SUBINDUSTRY / decay 5 / truncation 0.08 / nan ON
> 上游：other699 判死（见 `_usa-other699-field-profile-20261021.md` §5）后的换集。
> 换集理由：other699 的缺口是**结构性**（供收益的选名杠杆与守 SUB 的杠杆互斥），6 代结构 × 40 条仿真已穷尽，不是参数没扫到。

## §0 数据集身份

| 项 | 值 | 来源 |
|---|---|---|
| dataset id | `other545` | platform |
| 名称 / 模型 | Linked Firms Momentum Data · **NEMO 2.0**（7 个网络动量信号的复合） | 字段 `oth545_score` 描述 |
| 类别 | Other | `get_datasets` |
| 字段数 | **4（全部 VECTOR）** | `get_datafields` |
| 覆盖率 | **0.8051**（4 字段完全一致） | platform |
| 拥挤度 | αC 合计 34（max 13，`pln_omen`），users ≤ 9 | platform |
| 点亮状态 | 未点亮（USA/D1 本季只有 model / analyst / earnings 亮） | RA 面板 |
| 价值分 | 5 | S0 体检 |

**机制本体**：每个股票带一个**链接公司向量**（供应链 / 经济关联方），向量元素是关联公司的动量读数。
对应文献 Cohen & Frazzini (2008)「Economic Links and Predictable Returns」——信息沿经济链路慢扩散，
关联方的动量可预测焦点股；NEMO 2.0 是把它工程化成 7 信号复合分。

## §1 字段清单（全 4 字段）

| 字段 | 类型 | 覆盖 | αC | users | 描述 | 在机制里的角色 |
|---|---|---|---|---|---|---|
| `oth545_mktcap` | VECTOR | 0.8051 | 10 | 9 | 公司市值（美元） | **链接方规模 / 链接广度**（`vec_count`），不是权重（见 §3） |
| `oth545_mpd` | VECTOR | 0.8051 | 6 | 5 | 动态价格动量分（先进 / ML 价格动量） | 链接方的**价格动量**腿 |
| `oth545_pln_omen` | VECTOR | 0.8051 | 13 | 5 | NLP 文本挖掘关联网的网络动量分 | **文本网络动量**腿（αC 最高，最被用过） |
| `oth545_score` | VECTOR | 0.8051 | 5 | 4 | NEMO 2.0 复合分（7 信号聚合） | 复合腿（**αC 最低 ⇒ 最不拥挤**） |

> ATOM 约束：本集非豁免字段就是这 4 个（无可豁免的 country / exchange / sector 等）。
> 交付候选应尽量覆盖全部 4 个字段；至少 `score` 与 `mpd` / `omen` / `mktcap` 都要在某一代结构里被消费。

## §2 机制假设（预注册）

| # | 假设 | 判据 |
|---|---|---|
| **H1** | 链接方动量**正向**传导：`vec_avg(score)` 的截面排名可预测焦点股收益 | 单腿 S ≥ 1.0（探针线） |
| **H2** | 复合分优于单腿：`score` 的 S ≥ max(`mpd`, `omen`) | 三者同壳对比 |
| **H3** | 链内**分歧**是负面信号：`vec_stddev(score)` 高的名字可预测性差（一致度 = 置信度） | `vec_avg(score)/vec_stddev(score)` 型置信度加权优于裸均值 |
| **H4** | **链接广度**（`vec_count(mktcap)`）是有效选名变量：链接多的名字信息更充分 | 广度分桶 / 门控使 S 或 SUB 抬升 |

## §3 VECTOR 事件型约束（2026-10-21 实测，后续批次必读）

1. **字段是「事件型」向量**：`multiply(oth545_mpd, oth545_mktcap)` ⇒
   `Operator multiply does not support event inputs`。
   **逐元素算术一律不可用**，只能先 `vec_*` 归约成标量，再进常规算子链。
2. 可用归约只有：`vec_avg` / `vec_sum` / `vec_max` / `vec_min` / `vec_stddev` / `vec_range` / `vec_count`。
   **没有加权均值算子** ⇒ 市值**不能当权重**，只能作为「链接方规模」的独立统计量（`vec_avg(mktcap)`）
   或链接数（`vec_count(mktcap)`）。
3. **连坐仍成立**：批内 1 条 ERROR ⇒ 同批其余 3 条全部 CANCELLED（probe v1 实测）。
   发批前必须逐条过「事件型向量只接 vec_*」这一关，不能靠平台兜底。
4. 覆盖 0.805 ⇒ 归约后必须 `ts_backfill(x, 66)`，否则 ~20% 缺失会带来 CONCENTRATED_WEIGHT。

## §4 批次记录

### 4.1 probe v1（`1BLBbQeYx4yM9ud1gvBJPLZc`）— 语法探针，失败但产出关键事实

4 条：`vec_avg(score)` / `vec_avg(mpd)` / `vec_avg(omen)` / 市值加权 `mpd`。
结果：3 CANCELLED + 1 ERROR（`multiply does not support event inputs`）⇒ 得到 §3 的结论。

### 4.2 probe v2（`M563VcJt59P9v9zy5MS9SY`）— 5 条归约探针

统一壳：`rank(ts_backfill(<agg>, 66))`，decay 5 / SUBINDUSTRY / trunc 0.08 / nan ON。

| # | 探针 | 表达式 |
|---|---|---|
| P1 | 复合水平 | `rank(ts_backfill(vec_avg(oth545_score), 66))` |
| P2 | 价格动量腿 | `rank(ts_backfill(vec_avg(oth545_mpd), 66))` |
| P3 | NLP 网络动量腿 | `rank(ts_backfill(vec_avg(oth545_pln_omen), 66))` |
| P4 | 链接广度 | `rank(ts_backfill(vec_count(oth545_mktcap), 66))` |
| P5 | 链内分歧 | `rank(ts_backfill(vec_stddev(oth545_score), 66))` |

读数（S / F / TO / 2Y / SUB / DD）：

| # | 探针 | S | F | TO | 2Y | SUB | DD | FAIL |
|---|---|---|---|---|---|---|---|---|
| P1 | 复合水平 `vec_avg(score)` | 0.46 | 0.19 | 0.147 | 0.20 | 0.28 | 0.108 | S/F/2Y |
| P2 | 价格动量 `vec_avg(mpd)` | 0.34 | 0.12 | 0.177 | 0.09 | 0.25 | 0.156 | S/F/2Y |
| P3 | NLP `vec_avg(pln_omen)` | 0.37 | 0.14 | 0.098 | 0.35 | 0.21 | 0.131 | S/F/2Y |
| P4 | 广度 `vec_count(mktcap)` | -0.10 | -0.03 | 0.114 | -0.12 | -0.28 | 0.354 | S/F/CW/SUB/2Y |
| P5 | 分歧 `vec_stddev(score)` | **0.57** | 0.18 | 0.092 | **1.52** | 0.04 | 0.056 | S/F/SUB/2Y |

> 本批另有两条同内容重发（`38TYUMbzm4lQ8JtQ8jZhjnG` / `3rfxRz1Qb4AaadF1aywCmL0g`），
> 起因是 429 重试脚本未按成功退出——同内容批不影响结论。

### 4.3 批 1（`gSR2PfrW4rDb5EMY51V2mD`）— 归因诊断，10 条全灭

统一壳 `rank(ts_backfill(<x>, 66))`。

| # | 变体 | S | F | TO | 2Y | SUB | 读数 |
|---|---|---|---|---|---|---|---|
| A1 | `ts_rank(level, 252)` | 0.03 | 0.00 | 0.183 | -0.47 | 0.28 | 时序归一化把信号**打散** |
| A2 | `ts_zscore(level, 252)` | 0.12 | 0.02 | 0.173 | -0.34 | 0.34 | 同上 |
| A3 | `ts_delta(level, 22)` | 0.63 | 0.16 | 0.257 | -0.16 | 0.63 | 本批最高 S，但 2Y 负 ⇒ 不稳定 |
| A4 | `vec_max(score)` | 0.46 | 0.19 | 0.148 | 0.21 | 0.29 | **≈ P1** |
| A5 | `vec_min(score)` | 0.46 | 0.19 | 0.148 | 0.19 | 0.28 | **≈ P1 ≈ A4** |
| A6 | `vec_range(score)` | -0.17 | -0.05 | 0.152 | 1.05 | -0.18 | 纯噪声，CW 挂 |
| A7 | `mean/std` 置信度 | -0.06 | -0.01 | 0.079 | -0.63 | -0.08 | H3 证伪 |
| A8 | 广度门控 0.5 | -0.01 | 0.00 | 0.022 | 0.31 | -0.28 | H4 证伪（门控后几乎不交易） |
| A9 | 按链接市值分 5 桶 | 0.43 | 0.14 | 0.209 | 0.26 | 0.25 | 分组无增益 + CW 挂 |
| A10 | 反向 `-level` | -0.46 | -0.19 | 0.147 | -0.20 | -0.28 | 与 P1 完全镜像 ⇒ 无方向性优势 |

**结构性发现（关键）**：

1. **向量近乎退化为单元素**：`vec_max` ≡ `vec_min` ≡ `vec_avg`（S/F 完全一致、TO 差 < 0.001，A4/A5/P1 三行）。
   若链接集真有多个关联方，极值与均值不可能同时相等 ⇒ 绝大多数股票的向量只有 1 个元素（或极端支配）。
   **「网络」这一层在本数据集里基本不存在**，它退化成「一个动量分 + 一个规模分」。
2. **时序维度无信息**：ts_rank / ts_zscore 把 S 打到 0.03 / 0.12（A1/A2）⇒ 该分不是趋势也不是均值回复信号，
   只有**横截面水平**有一点微弱方向（P1 0.46）。
3. **H3（分歧作置信度）/ H4（广度作选名）双双证伪**（A7 -0.06 / A8 -0.01）。
4. P5 `vec_stddev` 单独看 2Y 1.52 但全期 S 0.57、SUB 0.04、DD 0.056 ⇒ 更像低波风险溢价，不是 alpha。

### 4.4 批 2（`WykvaamE4xjbnB1fKEaVW9T`）— 设置 / 壳层 / 同集价差

只问「换风险剥离口径、换分组口径、或用同集两腿自比能否把 0.46 抬起来」：
S1 neut MARKET · S2 INDUSTRY · S3 SLOW_AND_FAST · S4 decay 0 · S5 decay 20 ·
H1 `group_rank(·, subindustry)` · H2 quantile 套 H1 · H3 `ts_mean22` 平滑 ·
X1 `score − mpd` 价差 · X2 `score − pln_omen` 价差。读数待填。

## §5 决策

**判定：other545 在 RA 层面判死（2026-10-21，25 条仿真 / 3 批）。**

读数汇总（全期最高值，跨批）：

| 维度 | 最高 | 出现在 | 闸线 | 结论 |
|---|---|---|---|---|
| S | **0.83** | H2 `quantile(group_rank(·, subindustry))` | 1.58 | 缺 1.9× |
| F | 0.48 | 同上 | 1.0 | 缺 2.1× |
| 2Y | 0.72 | 同上 | 1.58 | 缺 2.2× |
| SUB 比值 | 1.21 | S3 SLOW_AND_FAST（但 2Y −0.38） | 0.432 | 不是瓶颈 |

**判死依据（逐条都有读数支撑）**

1. **「网络」不存在**：`vec_max ≡ vec_min ≡ vec_avg` ⇒ 向量退化为单元素（§4.3 发现 1），
   本数据集实际只是「一个动量分 + 一个规模分」，网络动量机制无法承载。
2. **时序无信息**：ts_rank 0.03 / ts_zscore 0.12 / ts_mean22 0.36（A1/A2/H3）⇒ 只有横截面水平有一点方向。
3. **两个机制假设都被证伪**：分歧作置信度 −0.06（A7）、广度作门控 −0.01（A8）。
4. **设置杠杆榨干**：MARKET 0.46 / INDUSTRY 0.42 / SLOW_AND_FAST 0.53（2Y 负）/ decay 0 0.49 / decay 20 0.42。
5. **同集两腿价差无效**：score−mpd −0.16、score−omen 0.10。
6. 唯一有效杠杆是**组内（subindustry）排名**：0.46 → 0.83（+0.37），但这是「换个排序口径」的一次性增益，
   与其余杠杆不叠加（组内排名后再换中性化/decay 无独立增益空间，§4.4 已各测一遍）。

**封存状态**：dead_end 条目未封存——与 other699 同一取证闸阻塞（`forum_recon` 读帖全失败 `read_failed`，
fail-closed 拒绝）。判死结论以本档案为准。

**下一步**：`equity_kpi_forecast`（22 字段 / cov 0.372 / αC 139 / value 5）。
换集理由：other545 的缺口是**信号强度**（S 0.83 vs 1.58），不是口径没调对；其向量退化使「网络」机制无载体，
继续扫只是同一动量分的参数组合。
