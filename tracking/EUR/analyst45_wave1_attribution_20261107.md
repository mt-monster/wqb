# analyst45 第 1 波归因 · 稀疏 VECTOR 数据集的 nanHandling 陷阱

- 时间：2026-11-07｜数据集：`analyst45` (Analyst Trade Ideas)｜EUR / TOPCS1600 / D1
- 画像：`docs/reference/EUR/analyst45_field_profile_20261107.md`｜模板池：`tracking/EUR/s1_analyst45_wave1_template_pool.md`

## 1. 派发与读数

| alpha | 模板 | 表达式 | nanH | decay | S | F | TO | 2Y | sub | ret | 多/空 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ZYQXEzXZ` | T1 目标价存量溢价 | `group_rank(divide(vec_avg(target_prc), vec_avg(prc)), industry)` | ON | 4 | 0.11 | 0.01 | 57.3% | 1.08 | 0.00 | 0.60% | 170/807 |
| `6XdGp0GY` | T2 构想覆盖广度 | `-group_rank(ts_mean(vec_count(target_prc),22), industry)` | ON | 4 | 0.09 | 0.02 | 7.9% | 0.04 | 0.00 | 0.44% | 863/474 |
| `6XdGpJpG` | T3 目标价分歧度 | `-group_rank(divide(vec_stddev(target_prc), vec_avg(target_prc)), industry)` | ON | 4 | 0.12 | 0.01 | 54.9% | -0.23 | 0.19 | 0.67% | 807/186 |
| `MPYgGZGn` | T4 信念加仓比 | `group_rank(divide(vec_sum(current_inv), vec_sum(initial_inv)), industry)` | ON | 4 | 0.00 | 0.00 | 49.8% | -0.39 | 0.06 | 0.01% | — |
| `d5W9j2VK` | **T1 复跑（受控）** | 同 `ZYQXEzXZ` | **OFF** | 4 | **0.69** | 0.15 | **174.0%** | **1.88** | **0.61** | **8.13%** | 23/22 |
| `vR1YjKMb` | 健康检查 | `group_rank(vec_avg(net_market_exposure), industry)` | OFF | 4 | 0.38 | 0.06 | 154.6% | 1.15 | 0.29 | 4.26% | 53/45 |

## 2. 归因：稀疏 VECTOR × `nanHandling ON` = 零权重注入

### 证据链
1. **多空数镜像反推覆盖率**：T1（正值）170 多 / 807 空；T3（取负）807 多 / 186 空 —— 取负后完全镜像 ⇒ 「低覆盖」那侧恒被做空/做多，说明 807 那批是**同一批股票**，即**没有构想数据的股票**。
2. **T2 是反证**：`vec_count` 对空向量返回 **0（不是 NaN）**，所以 T2 多空比 863/474 均衡、换手仅 7.9% —— 说明失衡不是 `group_rank` 或中性化造成，而是 **NaN 造成**。
3. **单变量受控实验**：`ZYQXEzXZ` → `d5W9j2VK` 只改 `nan_handling` ON→OFF：**S 0.11→0.69（6.3×）、2Y 1.08→1.88、returns 0.60%→8.13%、sub 0→0.61**。持仓从 977 只收缩到 45 只。

### 机制解释
`analyst45` 每个股票-日只有约 **4–5%** 的股票存在活跃 trade idea（ON 版本 45 只有值 / 977 只有权重）。
`nanHandling ON` 把无覆盖股票的 NaN 填成 **0**，经横截面中性化后 0 低于组均值 ⇒ 变成**系统性空头**。
于是 alpha 的真实内容被替换成「有没有分析师覆盖」这个规模/流动性代理，原信号被稀释到只剩 15%。

## 3. 结论（可直接复用的平台口径）

- **稀疏 VECTOR 数据集的标准起手式 = `nan_handling: OFF`**。判据：跑 1 条正负对称的骨架，看 `longCount/shortCount` 是否严重失衡（如 1:5）；失衡 ⇒ 覆盖率注入，不是信号。
- 该结论与「`vec_count` 类算子不受影响」互为校验：如果只有 NaN 型字段失衡、count 型字段均衡，就锁定是 NaN 注入而非分组轴问题。
- **数据集健康检查模板**：拿该数据集里最拥挤的字段（本例 `net_market_exposure`，118 alpha / 86 user）跑一条最简骨架。读数是「这个数据集还剩多少可提取信息」的上界参考：本例 S 0.38 ⇒ 数据集中有信号但**并不肥**，T1 的 0.69 是目标价机制自己挣的。

## 4. 副作用与新的主矛盾

修好覆盖后 **换手率 174%**（闸线 0.05–0.3，硬闸 0.7），持仓仅 45 只 ⇒ 两个新瓶颈：
1. **换手**：根源是「构想开仓/平仓」导致持仓出现/消失，而不是信号翻转。
2. **集中度**：45 只持仓会卡 `CONCENTRATED_WEIGHT`，且 sub 宇宙闸不稳。
两者的共同解法 = **把稀疏序列在时间维上补/平滑**（`ts_backfill` 保持上次读数 / `ts_mean` 平均），见下一批。

## 5. 已确认正面事实

- **历史深度合格**：`ZYQXEzXZ` 逐年 2014–2023 **全部有数据**（longCount 108–216、shortCount 522–893、pnl 非零），满足「近十年都有数据」。
- **塔位登记正确**：`pyramids = [{name: "EUR/D1/ANALYST", multiplier: 1.3}]`，单数据集未破 ATOM、未触塔混禁令。
- **比值闸再证**：`LOW_SUB_UNIVERSE_SHARPE = 0/0.06`，0.06 ≈ 0.5303×0.11。


## 6. 缺口处理 A/B（第 2 波）与 universe / 中性化（第 3–4 波）

| alpha | 表达式骨架 | universe | 中性化 | S | F | TO | 2Y | sub | rob | 多/空 | fail |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `VkxM7Yn5` | `ts_backfill(<T1>,66)` | TOPCS1600 | SUBIND | 0.71 | 0.30 | 15.5% | 1.60 | 0.52 | — | 294/296 | 3 |
| **`e751zqel`** | `ts_mean(<T1>,22)` | TOPCS1600 | SUBIND | **1.01** | 0.56 | 14.5% | **1.87** | **0.88** | 0.34 | 213/214 | **1** |
| `qML5jxmK` | `ts_mean(<T1>,22)` | **TOP2500** | SUBIND | 0.88 | 0.43 | 14.1% | 0.86 | 0.51 | — | 390/390 | 4 |
| `vR1YjrJ3` | `ts_mean(<T1>,66)` | **TOP2500** | SUBIND | 0.51 | 0.20 | 6.2% | 0.56 | 0.24 | — | 537/537 | 5 |

### 结论 A：缺口处理「平均」优于「回填」
`ts_mean 22` > `ts_backfill 66`（S 1.01 vs 0.71，2Y 1.87 vs 1.60，sub 0.88 vs 0.52）。原因：`ts_backfill` 保持最后一次读数 ⇒ 陈旧构想的陈旧目标价被原样持有；`ts_mean` 让新旧构想按存在时长加权混合 ⇒ 自然老化。**两者都把换手从 174% 压到 15% 量级，但只有均值型改善了信噪比。**

### 结论 B：稀疏覆盖数据集**不能**靠扩 universe 提 S（与 EUR/OTHER 经验相反）
TOPCS1600 → TOP2500：S 1.01→0.88、2Y 1.87→**0.86**、sub 0.88→0.51，并**新增 `CONCENTRATED_WEIGHT` 硬闸**。
机制：本数据集只有约 4–5% 的股票有活跃 trade idea，且集中在大中盘；扩到 TOP2500 后新增的 ~900 只主要是**无构想覆盖**的标的，即便 nanHandling OFF 把它们排除在持仓外，`CONCENTRATED_WEIGHT` 仍被触发（权重分布相对更宽的候选池更尖），而 2Y 的塌陷说明新增标的里带的是噪声。
**判据**：`universe` 是 prod–S 平移旋钮这条经验**只对高覆盖率数据集成立**；遇到 cov 稀疏（有值股票占比 <10%）的数据集，先固定最小可用 universe，把 universe 扩容当作「引入未覆盖噪声」的负向杠杆。

### 结论 C：`e751zqel` 的唯一硬闸是 `LOW_ROBUST_UNIVERSE_SHARPE`
`checks.fail = [LOW_ROBUST_UNIVERSE_SHARPE=0.34/0.7]`；`LOW_SHARPE=1.01` 与 `LOW_FITNESS=0.56` 落在 `warning` 但按 REGULAR 口径同样阻断提交 ⇒ 需**同时**把 S 推到 ≥1.58、F 推到 ≥1.0、robust 推到 ≥0.7。
robust 宇宙（更严的子宇宙）只有 0.34 而全样本 1.01 ⇒ 信号在**大流动性端更弱**，这与「trade ideas 集中在大中盘」形成张力，是下一步的主要嫌疑点。
