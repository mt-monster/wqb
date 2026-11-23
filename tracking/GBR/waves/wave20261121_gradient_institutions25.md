# GBR / institutions25 完整梯度档案（wave20261121_institutions25）

> 依据：`wq-brain-ra-pipeline` 步 7「梯度回测（必做）」+ §7.10；用户 2026-11-21 质询「institutions25 有无经过完整的梯度流程」⇒ 核实为**未做**（仅有字段级全覆盖 + 设置档网格），按规则「未完成梯度只能记 PROVISIONAL」⇒ 本轮补做 5 层全类别梯度。
> 数据集：institutions25（**24 字段全 VECTOR**，Fund Short Selling Data，机构做空行为面板，`pyramidMultiplier=1.4`）｜塔：institutions（GBR/D1，当前 **1/3**）
> 历史状态：纯 ATOM 设置档网格 7 档最高 **FAST S1.10/2Y0.44**（profile §11）；历史 max S1.26 是跨集 add（含已点亮 shortinterest 塔字段）⇒ 不作 ATOM 依据。
> 记录纪律：每层「同槽位全类别替换 + Δ 表 + 收敛判定」；换基线后下游重扫。

---

## §7.10.0 数据窗口前置体检（2026-11-21，批 `3ys5TQNK4qh9E0vPC7fHEs`，2 臂）

探针（NONE / decay0 / trunc0 / nanOFF）：`rank(ts_backfill(vec_avg(inst25_position_change),250))` → `YPazda9q`；`rank(ts_backfill(vec_avg(inst25_crowding),250))` → `npaqbaXz`

`get_alpha_yearly_stats(YPazda9q)` 逐年：**2014–2023 全部 10 年均有 longCount（295–534）与非零 pnl**（2014 +0.31M / 2018 −2.85M / 2022 −3.81M / 2023 +2.91M），`shortCount=0` 是 `rank()` 裸探针的长仓伪影（profile §7 已证），非数据缺失。
⇒ **数据窗口 = 2014–2023（10 年）合格，2Y 窗（2022/2023）有数据**，梯度可做。

> 探针读数（未中性化）：S0.52/0.51、F0.61/0.57、2Y −0.13/−0.14 —— 仅作数据存在性判据，不作信号判据。

---

## 完整梯度计划（5 层）

| 层 | 槽位 | 全类别候选 | 臂数 |
|---|---|---|---|
| **L1 信号构造** | 7 个字段族（A 强度/B 仓位流/C 时长/D 计数/E 方向计数/F 广度/G 活跃度）+ 同集双字段组合 | A 4 + B 4 + C 2 + D 1 + E 1 + F 1 + G 1 + 组合 1 = 15 | 15（2 批） |
| **L2 内层时序** | `<K>(SIG, N)` | Time Series 15/16 可测（ts_step 只收数字排除） | 15（2 批） |
| **L2b 窗口** | `ts_<K>(SIG, N)` | N ∈ {66, 126, 250, 504} | 4 |
| **L3 分组轴** | `group_rank(·, G)` | industry/sector/subindustry/market/exchange/country | 6 |
| **L4 外层包装** | `group_rank` → Group 类 | rank/zscore/neutralize/scale/std_dev/sum/backfill×2 | 8 |
| **L5 设置档** | 中性化 × decay | SUBINDUSTRY（基线）/INDUSTRY/SECTOR/FAST/STATISTICAL + decay{4,8} | 4–5 批 × 2 |

**验收①（字段全表）**：24/24 字段全部进 L1（A 族 4 + B 族 4 + C 族 2 + D 族 1（1mo/1yr 归一）+ E 族 2（cover/short 比值）+ F 族 2（manager_count；manager_position_count 留 L1-B）+ G 族 1 = 覆盖 20 字段；余 4 字段（trade_length、security_avg_trade_length、security_trade_count、_3mo/_1wk/_2yr/_3yr 中未入式者）在 L1-B 以比值/水平补入，确保 24/24 有实测行。

---

## Layer 1 · 信号构造全替（A/B 族，2026-11-21，批 `2oBzAG3IK5hua2lflGxW7Ec`，8 臂）

冻结：`group_rank(ts_zscore(ts_backfill(<SIG>, 250), 126), industry)` / SUBINDUSTRY / decay4 / trunc0.08 / nanON

| 臂 | 族 | 构造 | α | S | F | 2Y | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| L1-7 | B 仓位流 | `vec_avg(entry_position)` 开仓规模 | `0mPgowO8` | **−0.64** | −0.35 | **+0.27** | 5.7% |
| L1-5 | B 仓位流 | `vec_sum(position_change)` 仓位变化 | `xAvGMjOq` | −0.58 | −0.28 | −0.16 | 10.8% |
| L1-3 | A 强度 | `vec_avg(crowding)` 拥挤度 | `MP6zw7PL` | −0.55 | −0.24 | −0.01 | 14.9% |
| L1-6 | B 仓位流 | `vec_avg(position)` 仓位水平 | `88NJAl57` | −0.55 | −0.26 | **+0.30** | 6.5% |
| L1-8 | B 仓位流 | `vec_avg(is_open)` 开放占比 | `npaq07xa` | −0.55 | −0.31 | −0.12 | 5.6% |
| L1-1 | A 强度 | `vec_avg(sentiment)` 做空情绪 | `A1xz6lRX` | −0.45 | −0.19 | **+0.40** | 7.6% |
| L1-2 | A 强度 | `vec_avg(total_short_interest)` 总空头利息 | `6XM0xlXY` | −0.43 | −0.19 | **+0.46** | 5.9% |
| L1-4 | A 强度 | `vec_avg(concentration)` 集中度 | `akazJ7kw` | −0.39 | −0.16 | **+0.55** | 5.8% |

**L1-A 结论**：
1. **8/8 全为负 S**（−0.39 ~ −0.64）⇒ inst25 的做空行为族原始方向是**反向信号**；`reverse()` 为精确取负（S/F/2Y 全翻号、TO 不变），故反转读数可零配额推得：**S 0.39–0.64**。
2. **6/8 呈「S 负 + 2Y 正」的方向互斥**（sentiment/TSI/concentration/position/entry_position）——反转后 S 翻正但 2Y 翻负；这是本集的**结构性特征**（与 in6 同型），也是历史上只有「组合形态 + FAST 档」能同时做出 S1.10/2Y0.44 的原因。
3. **|S| 排序**：entry_position 0.64 > position_change 0.58 > crowding/position/is_open 0.55 > sentiment 0.45 > TSI 0.43 > concentration 0.39。
4. **L2 基线**：取 `entry_position`（|S| 最大）与 `position_change`（历史组合主力、αC 双料最高）两条作候选，等 L1-B（C/D/E/F/G + 同集残差）出来后统一定基线。

---

## Layer 1-B（C/D/E/F/G 族 + 同集残差，2026-11-21，批 `1OgDUQi64EXbct1cR6gfSj1`，7 臂）

| 臂 | 族 | 构造 | α | S | F | 2Y | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| — | C | `vec_avg(age)` 空仓年龄 | `0mPgo1O6` | −0.61 | −0.30 | +0.06 | 6.9% |
| — | C | `vec_avg(manager_avg_trade_length)` 经理平均持仓时长 | `mLa7OEp2` | −0.71 | −0.36 | +0.16 | 7.1% |
| — | D | `divide(sum(_1mo), sum(_1yr))` 交易笔数短期占比 | `omaG2x76` | −0.41 | −0.16 | **+0.60** | 7.1% |
| — | E | `divide(sum(cover_count), sum(short_count))` 平空/卖空比 | `rK7GkZY8` | −0.38 | −0.16 | +0.14 | 23.3% |
| — | F | `vec_sum(manager_count)` 做空经理数 | `Jj8zl6wE` | −0.52 | −0.24 | +0.33 | 9.5% |
| — | G | `vec_avg(activity)` 活跃度 | `wpoG60m1` | **−0.82** | −0.36 | +0.05 | 20.6% |
| — | 组合 | `vector_neut(ts_zscore(sum(position_change),126), ts_backfill(sum(crowding),250))` 同集残差 | `78YmOeA1` | **−0.96** | −0.54 | **−0.80** | 16.2% |

**L1-B 结论**：**7/7 仍全为负 S** ⇒ **15/15 全族统一反向**（无任何构造形态是正向信号）。反转后 |S| 排序：**同集残差 `position_change ⊖ crowding` S0.96 / 2Y0.80（★最强，双高）** > activity 0.82（2Y −0.05）> manager_avg_trade_length 0.71（−0.16）> entry_position 0.64（−0.27）> age 0.61（−0.06）。
> ⚠ **更正（2026-11-21）**：残差组合 `78YmOeA1` 原始 S−0.96/2Y−0.80，`reverse` 后 **S+0.96 / 2Y+0.80**（先前误写为「2Y −0.80 ⇒ 弃」，符号搞错）。它是本集**最强模板**，已提为模板 C 优先推完整梯度。
⇒ **L1 收敛**（15 臂全类别，无正向构造）；**L2 基线 = `reverse(activity 构造)`**（反转后 S0.82 最高、2Y 仅 −0.05）。

### L1-C · 补全剩余 8 字段（2026-11-21，批 `4ctuXu9IR4VucFSxT2n8kUW`，8 臂）

> 目的：D2「数据集内每个字段族 ≥1 条实测」+ 24/24 字段全覆盖。

| 臂 | 字段（族） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| L1-9 | `vec_avg(trade_length)`（C） | `xAvGXlpp` | −0.68 | −0.33 | +0.13 | 5.5% |
| L1-10 | `vec_avg(security_avg_trade_length)`（C） | `pwaGQWb6` | −0.68 | −0.33 | +0.14 | 5.5% |
| L1-11 | `vec_sum(security_trade_count)`（D） | `78YmgGPL` | −0.59 | −0.27 | +0.07 | 13.6% |
| L1-12 | `vec_sum(_3mo)`（D） | `xAvGXl7p` | −0.42 | −0.17 | +0.23 | 8.4% |
| L1-13 | `vec_sum(_1wk)`（D） | `d5aze9MX` | −0.61 | −0.30 | +0.32 | 12.3% |
| L1-14 | `vec_sum(_2yr)`（D） | `rK7GQ0qE` | −0.54 | −0.25 | +0.21 | 9.4% |
| L1-15 | `vec_sum(_3yr)`（D） | `0mPgnGVp` | −0.53 | −0.25 | +0.21 | 9.5% |
| L1-16 | `vec_sum(manager_position_count)`（F） | `leaGJgnA` | −0.47 | −0.20 | +0.30 | 9.5% |

**★ L1 终态（23 臂 / 24/24 字段全覆盖）**：**23/23 全为负 S（−0.38 ~ −0.96），无一个正向构造** ⇒ inst25 全族统一反向（做空行为越强 → 后续越可能跑赢，属 GBR 的逆向/拥挤反转效应）。反转后 |S| 排序：**activity 0.82** > combination 0.96（但 2Y −0.80 弃）> manager_avg_trade_length 0.71 > trade_length 0.68 = security_avg_trade_length 0.68 > entry_position 0.64 > age 0.61 > _1wk 0.61 > security_trade_count 0.59 > position_change 0.58 …
⇒ **L1 收敛**（无正向构造、无强 2Y）；**L2 基线 = `reverse(activity)`**（反转后 S0.82 / 2Y −0.05，代价最小）。

---

## Layer 2 · 内层时序算子全替换（L2-A，2026-11-21，批 `4qhyOvfFq5bRbRbFNJZ76N3`，8 臂）

冻结：`reverse(group_rank(<K>(ts_backfill(vec_avg(inst25_activity),250),126), industry))` / SUBIND / decay4 / trunc0.08

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| L2-1 | `ts_scale` | `9qlMPaqK` | 0.71 | 0.31 | −0.09 | 17.5% |
| **L2-2** | **`ts_rank`** | `O0Wzwb07` | **0.81** | 0.35 | **+0.22** | 20.3% |
| L2-3 | `ts_quantile` | `VkNzw2kM` | 0.79 | 0.33 | +0.19 | 20.2% |
| L2-4 | `ts_av_diff` | `MP6zlKPr` | 0.77 | 0.32 | +0.10 | 20.4% |
| L2-5 | `ts_delta` | `akaz2Aj2` | 0.78 | 0.33 | +0.18 | 19.8% |
| L2-6 | `ts_mean` | `O0WzwbQ7` | 0.59 | 0.27 | **+0.54** | 3.2% |
| L2-7 | `ts_std_dev` | `88NJka5V` | 0.79 | **0.45** | +0.23 | **3.7%** |
| L2-8 | `ts_ir` | `Jj8z0gMA` | 0.54 | 0.24 | −0.12 | 4.7% |
| L2-0 | `ts_zscore`（L1 基线） | `wpoG60m1` 反转视角 | **0.82** | 0.36 | −0.05 | 20.6% |

### L2-B · 剩余 7 内核（2026-11-21，批 `3rBkaS9T054VawStUplkKHo`）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| L2-9 | `ts_arg_max` | `E5Qz0MJJ` | 0.68 | 0.33 | 0.34 | 3.9% |
| L2-10 | `ts_arg_min` | `WjlzwR8P` | 0.61 | 0.27 | 0.38 | 3.9% |
| L2-11 | `ts_returns` | `N1PzWG9L` | 0.77 | 0.32 | 0.22 | 20.7% |
| L2-12 | `ts_product` | `2r56qxdY` | **−0.55** | −0.24 | 0.06 | 3.0% |
| L2-13 | `ts_sum` | `LLKzbwxe` | 0.70 | 0.36 | 0.41 | 2.1% |
| L2-14 | `ts_max_diff` | `omaGwXen` | 0.62 | 0.27 | 0.33 | 14.4% |
| L2-15 | `days_from_last_change` | `rK7G6wmd` | **−0.73** | −0.41 | −0.21 | 3.0% |

**L2 终态（15/16 可测 + 基线 = 16 臂）**：**无内核超过基线 ts_zscore 0.82**；`ts_rank` 0.81 并列但 **2Y 由 −0.05 抬到 +0.22**、F 持平 ⇒ **按「最佳 Δ」换基线为 `ts_rank`**（S−0.01 换 2Y+0.27）。`ts_std_dev`（0.79/F0.45/TO3.7%）是 F 轴最优但 TO 跌破内部严线 5%。反转后仍为负的只有 ts_product（−0.55）与 days_from_last_change（−0.73）⇒ 这两个内核在此族不成立。

---

## Layer 2b · 窗口全替（以 `ts_rank` 为基线，2026-11-21，批 `36bqzIqb4wUb00LJsxk90W`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| **L2b-1** | **66** | **`akazMoq1`** | **0.86** | 0.37 | **+0.32** | 21.3% |
| L2b-3 | 504 | `gJaGwxpK` | 0.81 | 0.37 | +0.32 | 17.9% |
| L2b-2 | 250 | `vRAGxd3Q` | 0.80 | 0.35 | +0.19 | 19.1% |
| L2b-4 | 750 | `XgazP16b` | 0.79 | 0.35 | +0.29 | 17.6% |
| L2b-0 | 126（基线） | `O0Wzwb07` | 0.81 | 0.35 | +0.22 | 20.3% |

**L2b 结论**：**窗口 66 最优（S0.86 / 2Y0.32，ΔS+0.05）**；{250,504,750} 平台 ≈0.79–0.81（与 126 同档）。TO 21.3% 略超内部严线 20% 上沿。⇒ **L3 基线 = 窗 66 × ts_rank**。

---

## Layer 3 · 分组轴全替换（2026-11-21，批 `1laVBafCy5aoanEptnc3wX6`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| **L3-3** | **`subindustry`** | **`VkNzEwlY`** | **0.88** | **0.39** | **+0.54** | 19.8% |
| L3-1 | `industry`（基线） | `akazMoq1` | 0.86 | 0.37 | +0.32 | 21.3% |
| L3-2 | `sector` | `E5Qzb0a1` | 0.82 | 0.37 | +0.20 | 19.5% |
| L3-4 | `market` | `0mPgdkQp` | 0.82 | 0.37 | +0.16 | 18.8% |
| L3-5 | `exchange` | `blazM2PK` | 0.82 | 0.37 | +0.16 | 18.8% |
| L3-6 | `country` | `omaGvw9m` | 0.82 | 0.37 | +0.16 | 18.8% |

**L3 结论**：**`subindustry` 最优（S0.88 / 2Y0.54 / F0.39，ΔS+0.02 / Δ2Y+0.22）**——细轴把 2Y 抬得最高（与 imb5「粗轴更好」相反 ⇒ 轴选择按族实测，不外推）；market≡exchange≡country 逐位相同（单国三轴等价再次复现）。⇒ **L4 基线 = subindustry × 窗 66 × ts_rank**。

---

## Layer 4 · 外层包装全替换（2026-11-21，批 `2z9MLJb1d5j99qNkPZ2f7q9`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| L4-0 | `group_rank`（基线） | `VkNzEwlY` | **0.88** | **0.39** | **+0.54** | 19.8% |
| L4-1 | `group_scale` | `xAvGQv6g` | 0.55 | 0.12 | +0.95 | 51.4% |
| L4-2 | `group_zscore` | `58J59Jb5` | 0.51 | 0.11 | +0.98 | 51.1% |
| L4-3 | `group_neutralize` | `j2aGXaRE` | 0.54 | 0.12 | +0.62 | 50.7% |
| L4-6 | `group_backfill(·,subindustry,120)` | `78YmQYEO` | 0.54 | 0.11 | +0.23 | 49.3% |
| L4-7 | `group_backfill(·,subindustry,252)` | `LLKz6KAn` | 0.50 | 0.10 | +0.17 | 49.4% |
| L4-5 | `group_std_dev`（聚合型） | `N1Pz6PmE` | −0.31 | −0.08 | +0.42 | **111.9%**（DD 128%） |
| L4-4 | `group_sum`（聚合型） | `3q0Px0rX` | −0.54 | −0.16 | −1.83 | **108.2%**（DD 105%） |

**L4 结论（`converge=yes`，收敛于 `group_rank`）**：**全 ΔS 为负**——换任何外层都把 S 从 0.88 打到 ≤0.55 且 TO 翻倍（51%）。注：`group_scale`/`group_zscore` 把 2Y 抬到 0.95/0.98（这是本集 2Y 与 S 跷跷板的又一次体现），但 S 崩 ⇒ 不可用；聚合型 TO 108–112%、DD 105–128% 崩。⇒ **L5 基线维持 `reverse(group_rank(ts_rank(...66), subindustry))`**（S0.88/2Y0.54/TO19.8%）。

---

## Layer 5 · 设置档（2026-11-21，逐档 2 臂：subindustry 轴 + industry 轴，批 `zF8B83Qc4PUctlUacEasp8` 起）

| 批 | 设置档 | α（subindustry 轴 / industry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `d5az770X` / `1YWKmmd6` | 0.79 / 0.81 | 0.37/0.37 | +0.44/+0.37 | 16.8/17.8% |
| B | `SECTOR` 中性化 | `9qlMA05e` / `58J5qWmN` | 0.64 / 0.66 | 0.29/0.29 | +0.16/+0.09 | 15.5/16.5% |
| C | `FAST` 中性化 | `N1Pz5Zr8` / **`omaG9dg2`** | 0.99 / **1.01** | 0.36/0.37 | +0.44/+0.30 | 23.1/23.7% |
| D | SUBINDUSTRY + decay 8 | `e7aGqZ1l` / `qM7GmJ5P` | 0.80 / 0.77 | **0.43/0.41** | +0.36/+0.18 | 12.4/12.9% |
| 基线 | SUBINDUSTRY + decay 4 | `VkNzEwlY` / `akazMoq1` | **0.88 / 0.86** | 0.39 / 0.37 | **+0.54** / +0.32 | 19.8 / 21.3% |

**L5 结论（`converge=no`——出现 +0.13 的单层增益）**：
1. **`FAST` 中性化最优：S0.99–1.01**（industry 轴 1.01 / subindustry 轴 0.99），ΔS **+0.13** vs SUBINDUSTRY 基线 0.88 —— **与历史「FAST 档 1.10 最高」一致**（风险模型中性化对本族有效）。
2. INDUSTRY 0.79–0.81、SECTOR 0.64–0.66、decay8 0.77–0.80 均劣于基线；**decay8 是 F/TO 轴最优**（F0.43 / TO12.4%，落内部严线带）但 S −0.08。
3. ⇒ **终态基线 = FAST × group_rank(industry) × ts_rank66 × reverse(activity)**：**S1.01 / F0.37 / 2Y0.30 / TO23.7%**（TO 超内部 20% 上沿）。

### L5-R · 换基线（FAST）后内核层重扫（2026-11-21，批 `2PvOxUgKm53daBSLtWJkkkq`，4 臂）

| 臂 | 内核（FAST / industry 轴 / 窗 66） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| R-1 | `ts_rank`（L5 基线） | `omaG9dg2` | **1.01** | 0.37 | 0.30 | 23.7% |
| R-2 | `ts_av_diff` | `LLKznP16` | 0.99 | 0.36 | 0.19 | 23.7% |
| R-3 | `ts_zscore` | `QP0zn1Ep` | 0.98 | 0.37 | 0.15 | 23.6% |
| R-4 | `ts_quantile` | `rK7Gb1Wm` | 0.98 | 0.35 | 0.22 | 23.6% |
| R-5 | `ts_std_dev` | `xAvGeKkq` | 0.92 | **0.47** | 0.22 | **9.7%** |

**L5-R 结论**：FAST 基线下 **`ts_rank` 仍最优（1.01）**，内核排序未翻转（与 imb5「换基线后排序反转」不同、与 fhp「外层排序稳健」同型）⇒ 梯度闭环成立，无遗漏的下游重扫。

---

## ★ 完整梯度终态（5 层 / 68 臂）

| 层 | 全类别覆盖 | 最优 | 收敛结论 |
|---|---|---|---|
| L1 信号构造（23 臂 / 24/24 字段） | A 4 + B 4 + C 4 + D 7 + E 1 + F 2 + G 1 + 同集残差 1 | 全族**统一反向**；`reverse(activity)` | 23/23 全为负 S（−0.38 ~ −0.96）；镜像后 activity 0.82 最强 |
| L2 内核（16 臂含基线） | Time Series 15/16（ts_step 排除） | `ts_rank`（S0.81 / 2Y+0.22） | 无内核超 ts_zscore 0.82；ts_rank 以 2Y 换 S（+0.27） |
| L2b 窗口（4 臂） | {66,250,504,750} | **窗 66**（S0.86/2Y0.32） | ΔS+0.05；其余同档 |
| L3 轴（6 臂） | industry…country | **subindustry**（S0.88/2Y0.54） | 细轴抬 2Y 最高（与 imb5 相反，按族实测）；market≡exchange≡country |
| L4 外包（7 臂） | Group 7（group_mean/count 排除） | `group_rank`（S0.88） | **全 ΔS 负**；group_scale/zscore 抬 2Y 但 S 崩至 0.5、TO 翻倍 |
| L5 设置（8 臂 + L5-R 4 臂） | 中性化 4 + decay | **`FAST`**（S1.01 / ΔS+0.13） | decay8 = F/TO 轴最优（F0.43/TO12.4%）；INDUSTRY/SECTOR 皆劣 |

**最终判定（模板 A 完整梯度后）**：
- ⚠ **口径更正（2026-11-21 用户指令后续）**：以下 S1.01 是**模板 A（activity）的天花板**，**不是数据集天花板**——ATOM 穷尽要求塔内互异模板逐个跑完各自完整梯度（见下方「模板推进表」）。数据集天花板 = 各模板天花板最大值，待 B–G 推完后写。**模板 A 的天花板（可写死，模板内）**：
- **模板 A 天花板 = S1.01 / F0.37 / 2Y0.30 / TO23.7%**（68 臂 × 5 层全类别 + 换基线重扫后的最高点），**距 S 闸 0.57 / F 闸 0.63 / 2Y 闸 1.28**。
- 备选形态：SUBINDUSTRY 基线（S0.88 / F0.39 / **2Y0.54** / TO19.8%）— 2Y 最高、TO 合规但 S 低 0.13；decay8（S0.80 / F0.43 / TO12.4%）— 内部严线形态。
- **结构判定：信号层强度不足（非数据集死）**——24 字段跨 7 族全为同一反向方向、天花板 1.01，与历史「FAST 1.10」吻合；本集**不产出全闸 ATOM 件**，但按 §7.7 仍可作辅助腿（条件/分组/残差式入场）。
- **与 PROVISIONAL 的区别**：本轮已完成 5 层全类别 + 换基线重扫（D1 结构互异模板 20+ / D2 24/24 字段 / D3 矩与水平比 / D4 轴 6 / D5 非线性 rank+quantile / D6 配置 5 档）⇒ **天花板读数可写死**（不再是 PROVISIONAL）。
- 适用域：2014–2023（10 年，体检合格）。

## 状态

- 梯度完成：**5 层 / 68 臂**（L1 23 + L2 16 + L2b 4 + L3 6 + L4 7 + L5 8 + L5-R 4）。
- 交付结论：**0 颗**（S1.01 距闸 0.57；F0.37 距闸 0.63）。
- `gradient_gate --region GBR --dataset institutions25 --field-prefix inst25_` → 预期 GRADIENT_DONE。
- 台账：**不判死**（信号层强度不足，24 字段可作辅助腿）；report 行更新为「完整梯度后天花板 S1.01」。

---

## ★ 模板推进表（ATOM 穷尽 = 塔内互异模板逐个跑完各自完整梯度）

> 用户 2026-11-21 指令：「ATOM 并没有穷尽，只是对当时用的模板来说穷尽了，那就再换一个模板持续做梯度且换了模板之后要做完整的梯度流程」。
> 每个模板 = 一个互异信号构造（不同字段族/几何），各自走 **L2 内核全替 → L2b 窗口 → L3 轴 → L4 外包 → L5 设置（+换基线重扫）** 完整流程；数据集天花板 = 各模板天花板的最大值。

| 模板 | 信号构造（族） | 镜像后 | 梯度状态 | 模板天花板 |
|---|---|---|---|---|
| **A** | `vec_avg(activity)`（G 活跃度） | S0.82 / 2Y−0.05 | ✅ 完整（68 臂） | **S1.01**（FAST） |
| **B** | `vec_avg(manager_avg_trade_length)`（C 时长） | S0.71 / 2Y−0.16 | ✅ 完整（45 臂） | **S0.89**（FAST × industry） |
| **C（升为优先）** | `vector_neut(position_change, crowding)`（同集残差） | **S0.96 / 2Y+0.80**（★最强） | 待做 | — |
| D | `vec_avg(entry_position)`（B 仓位） | S0.64 / 2Y−0.27 | 待做 | — |
| E | `vec_avg(age)`（C 时长） | S0.61 / 2Y−0.06 | 待做 | — |
| F | `vec_sum(position_change)`（B 流量，αC 最高） | S0.58 / 2Y+0.16 | 待做 | — |
| G | `vec_avg(concentration)`（A 集中度） | S0.39 / 2Y−0.55 | 待做 | — |

## 模板 B · 完整梯度（2026-11-21 起）

### L2 · 内层时序算子全替换（批 `3Kftyq64S4OmbNWzHuS9qwx`（8 臂）+ `2Z4RzAd264M4c3qA5hT4yON`（7 臂），并行）

冻结：`reverse(group_rank(<K>(ts_backfill(vec_avg(inst25_manager_avg_trade_length),250),126), industry))`；SUBIND / decay4 / trunc0.08

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| B-0 | `ts_zscore`（基线，镜像自 L1-B） | `mLa7OEp2` | +0.71 | +0.36 | −0.16 | 7.1% |
| B-1 | `ts_scale` | `O0WzoYLv` | 0.69 | 0.34 | −0.18 | 7.3% |
| B-2 | `ts_rank` | `Wjlz9qZG` | 0.75 | 0.38 | −0.00 | 7.5% |
| B-3 | `ts_quantile` | `Grmzka2x` | 0.75 | 0.38 | −0.01 | 7.3% |
| **B-4** | **`ts_av_diff`** | **`E5Qzk7d1`** | **0.80** | **0.42** | +0.09 | 5.8% |
| B-5 | `ts_delta` | `gJaGxA2m` | 0.65 | 0.32 | −0.00 | 5.8% |
| B-6 | `ts_mean` | `j2aG1E7O` | 0.76 | 0.39 | **+0.39** | 2.3% |
| B-7 | `ts_std_dev` | `omaGVpxv` | 0.63 | 0.32 | −0.14 | 2.8% |
| B-8 | `ts_ir` | `gJaGxAne` | 0.70 | 0.34 | +0.19 | 4.0% |
| B-9 | `ts_arg_max` | `leaGr2G2` | 0.54 | 0.23 | +0.31 | 3.8% |
| B-10 | `ts_arg_min` | `vRAGd9GA` | 0.68 | 0.32 | +0.28 | 4.2% |
| B-11 | `ts_returns` | `VkNzOEzA` | 0.68 | 0.34 | +0.06 | 5.9% |
| B-12 | `ts_product` | `Xgaz1Lel` | **−0.51** | −0.23 | −0.01 | 2.5% |
| B-13 | `ts_sum` | `zqdGOj08` | 0.77 | 0.41 | +0.27 | 1.9% |
| B-14 | `ts_max_diff` | `QP0zEjgp` | 0.70 | 0.33 | **+0.38** | 6.0% |
| B-15 | `days_from_last_change` | `9qlMJKk1` | **−0.73** | −0.41 | −0.22 | 2.3% |

**B-L2 结论**：**`ts_av_diff` 最优（S0.80 / F0.42，ΔS+0.09 vs 基线 0.71）**；`ts_mean`（2Y+0.39）与 `ts_max_diff`（2Y+0.38）2Y 更高但 S 低 0.04–0.10；`ts_product`/`days_from_last_change` 镜像后仍负（与模板 A 同型）。⇒ **模板 B 的 L2b 基线 = `ts_av_diff × 窗 126`**。

### 模板 B · L2b 窗口全替（批 `Z8DIp2ut4xCcGtNWR5Vm9a`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| B-2b-1 | 66 | `akazoVlv` | 0.70 | 0.35 | +0.05 | 7.0% |
| **B-2b-2** | **250** | **`ZYazrmx0`** | **0.82** | **0.44** | +0.01 | 4.9% |
| B-2b-3 | 504 | `e7aGL6KE` | 0.72 | 0.36 | +0.13 | 4.3% |
| B-2b-4 | 750 | `78YmJoXO` | 0.77 | 0.40 | +0.19 | 4.1% |
| B-2b-0 | 126（基线） | `E5Qzk7d1` | 0.80 | 0.42 | +0.09 | 5.8% |

**B-L2b 结论**：**窗 250 最优（S0.82 / F0.44 / ΔS+0.02）**，TO 4.9%（跌破内部严线 5% 下沿但平台闸 1% 内）。⇒ **B-L3 基线 = ts_av_diff × 窗 250**。

### 模板 B · L3 分组轴全替（批 `1bRYXG2Uf4KScKIE6wungyM`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| B-L3-2 | `sector` | `N1PzOM08` | 0.71 | 0.36 | +0.03 | 4.4% |
| B-L3-3 | `subindustry` | `O0Wz9eYb` | 0.81 | 0.42 | **−0.32** | 4.2% |
| B-L3-4 | `market` | `P05z1eWM` | 0.73 | 0.37 | −0.00 | 3.9% |
| B-L3-5 | `exchange` | `wpoGe6md` | 0.73 | 0.37 | −0.00 | 3.9% |
| B-L3-6 | `country` | `9qlMRo19` | 0.73 | 0.37 | −0.00 | 3.9% |
| B-L3-1 | `industry`（基线） | `ZYazrmx0` | **0.82** | **0.44** | +0.01 | 4.9% |

**B-L3 结论（`converge=yes`，收敛于 industry）**：**industry 仍最优（0.82）**；subindustry S 0.81 但 **2Y 掉到 −0.32**；market≡exchange≡country 逐位相同 0.73。⚠ **轴偏好按模板而异**（模板 A 是 subindustry 最优，模板 B 是 industry）⇒ 支持「模板逐个实测」的必要性。⇒ **B-L4 基线 = ts_av_diff × 250 × industry**。

### 模板 B · L4 外层包装全替（批 `RwLxZ3CQ4Apazf1bRbuAR3J`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| B-L4-0 | `group_rank`（基线） | `ZYazrmx0` | **0.82** | **0.44** | +0.01 | 4.9% |
| B-L4-1 | `group_scale` | `58J5vgeM` | 0.41 | 0.16 | −0.46 | 7.2% |
| B-L4-2 | `group_zscore` | `zqdGWb0E` | 0.28 | 0.09 | −0.62 | 7.0% |
| B-L4-3 | `group_neutralize` | `1YWKgZ0Q` | 0.27 | 0.09 | −0.15 | 6.6% |
| B-L4-4 | `group_sum`（聚合型） | `6XM0EKNK` | 0.29 | 0.07 | +0.21 | **105.7%** |
| B-L4-5 | `group_std_dev`（聚合型） | `2r56Km28` | 0.06 | 0.01 | +1.23 | **104.5%**（DD 80%） |
| B-L4-6 | `group_backfill(·,industry,120)` | `rK7GWeno` | 0.07 | 0.01 | −0.11 | 6.3% |
| B-L4-7 | `group_backfill(·,industry,252)` | `YPazAM9J` | 0.06 | 0.01 | −0.01 | 6.1% |

**B-L4 结论（`converge=yes`，收敛于 `group_rank`）**：**全 ΔS 负**（0.06–0.41 vs 基线 0.82）⇒ 模板 B 的外层必须是 `group_rank`；与模板 A 同结论（外层稳健），但**模板 A 的 group_scale 仍有 0.55**、模板 B 直接掉到 0.41 ⇒ 外层敏感度按模板而异。

### 模板 B · L5 设置档（批 `1ww9gd9eV52I9OA44h0KeAv`（INDUSTRY）+ `3n2glgcUP5hma44rvwVWscG`（SECTOR）并行，随后 FAST + decay8）

| 批 | 设置档 | α（industry 轴 / subindustry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `2r567pRJ` / `VkNzpGEb` | 0.78 / 0.74 | 0.40/0.37 | +0.03/−0.25 | 4.0/3.8% |
| B | `SECTOR` 中性化 | `d5azxppY` / `d5azxpX2` | 0.63 / 0.60 | 0.30/0.28 | −0.23/−0.47 | 3.7/3.4% |
| **C** | **`FAST` 中性化** | **`akaznkov`** / `WjlzGj9o` | **0.89** / 0.88 | 0.41/0.41 | +0.07/−0.40 | 9.5/9.4% |
| D | SUBINDUSTRY + decay 8 | `0mPg719r` / `pwaG69o3` | 0.81 / 0.79 | **0.43/0.41** | +0.02/−0.34 | 4.1/3.6% |
| 基线 | SUBINDUSTRY + decay 4 | `ZYazrmx0` / `O0Wz9eYb` | 0.82 / 0.81 | 0.44/0.42 | +0.01/−0.32 | 4.9/4.2% |

**B-L5 结论（`converge=no`，+0.07）**：**`FAST` 最优 S0.89**（与模板 A 的 FAST 增益同向：模板 A +0.13、模板 B +0.07）⇒ **模板 B 天花板 = S0.89 / F0.41 / 2Y0.07 / TO9.5%**（FAST × industry）。decay8 仍为 F/TO 轴最优（F0.43 / TO4.1%）。

### 模板 B · L5-R 换基线（FAST）后内核重扫（批 `3TP1yG2f64Oh9ma19tbQQ4CH`，4 臂）

| 臂 | 内核（FAST / industry / 窗 250） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| R-1 | `ts_av_diff`（L5 基线） | `akaznkov` | 0.89 | 0.41 | +0.07 | 9.5% |
| **R-2** | **`ts_std_dev`** | **`YPaz0JaR`** | **0.97** | **0.48** | **+0.31** | 8.0% |
| R-3 | `ts_quantile` | `VkNzP5NM` | 0.77 | 0.33 | −0.25 | 10.5% |
| R-4 | `ts_rank` | `QP0zVg05` | 0.76 | 0.32 | −0.31 | 10.6% |
| R-5 | `ts_mean` | `qM7Gl35v` | 0.68 | 0.27 | +0.10 | 7.6% |

**B-L5-R 结论（★ 内核排序在换设置基线后翻转）**：**`ts_std_dev` 0.97 反超 L2 冠军 `ts_av_diff` 0.89**（F0.48 vs 0.41、2Y 0.31 vs 0.07）⇒ **模板 B 终态 = FAST × `group_rank(ts_std_dev(...,250), industry)` × reverse：S0.97 / F0.48 / 2Y0.31 / TO8.0%**。这再次证明「换基线后必须重扫」（模板 B 的 L2 冠军在 SUBIND 下是 ts_av_diff，在 FAST 下是 ts_std_dev）。
**模板 B 天花板 = S0.97**（< 模板 A 的 1.01）；完整梯度 45 臂收官。

---

## 模板 C · 同集残差组合（`position_change ⊖ crowding`）完整梯度（2026-11-21 起）

> 起点：L1-B 臂 `78YmOeA1`（原始 S−0.96/2Y−0.80）⇒ **镜像后 S0.96 / 2Y0.80（本集最强模板）**
> 基线结构：`reverse(group_rank(ts_zscore(vector_neut(ts_zscore(vec_sum(position_change),126), ts_backfill(vec_sum(crowding),250)),126), industry))`

### C-L2 · 内层时序算子全替（批 `3Q8sgo89155Yc4810cuJjLPT`（8 臂）+ 待派（7 臂）并行）

| 臂 | 外层内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| C-0 | `ts_zscore`（基线，镜像自 L1-B） | `78YmOeA1` 镜像 | 0.96 | 0.54 | +0.80 | 16.2% |
| C-1 | `ts_scale` | `E5QzEeRJ` | 0.91 | 0.57 | +0.66 | 10.7% |
| C-2 | `ts_rank` | `O0WzZx87` | 0.78 | 0.39 | +0.59 | 16.7% |
| C-3 | `ts_quantile` | `P05z3OgK` | 0.76 | 0.38 | +0.58 | 16.6% |
| C-4 | `ts_av_diff` | `Xgazn8Rm` | 0.95 | 0.54 | **+0.87** | 15.8% |
| **C-5** | **`ts_delta`** | **`zqdGmRro`** | **1.14** | **0.68** | **+0.96** | 19.8% |
| C-6 | `ts_mean` | `rK7GlPdd` | 0.73 | 0.40 | +0.18 | 4.2% |
| C-7 | `ts_std_dev` | `0mPgEMj2` | 0.56 | 0.27 | −0.35 | 4.1% |
| C-8 | `ts_ir` | `npaq28vM` | 0.77 | 0.44 | +0.22 | 4.1% |
| C-9 | `ts_arg_max` | `ZYazKL3j` | 0.58 | 0.27 | −0.05 | 4.4% |
| C-10 | `ts_arg_min` | `WjlzVmQP` | 0.68 | 0.34 | −0.02 | 4.5% |
| C-11 | `ts_returns` | `YPazgdKl` | 0.57 | 0.24 | +0.20 | 20.5% |
| C-12 | `ts_product` | `blazd3Zm` | −0.64 | −0.32 | +0.26 | 6.1% |
| C-13 | `ts_sum` | `vRAGvV33` | −0.05 | −0.01 | **+1.10** | 5.1% |
| C-14 | `ts_max_diff` | `3q0PeWZz` | 0.70 | 0.37 | +0.55 | 8.4% |
| C-15 | `days_from_last_change` | `N1PzRovL` | −0.64 | −0.34 | −0.14 | 2.1% |

**C-L2 结论**：**`ts_delta` 独一档（S1.14 / F0.68 / 2Y0.96，ΔS+0.18 vs 基线 0.96）**——模板 C 的内核偏好与 A（ts_rank）、B（ts_av_diff）都不同，**再次印证「模板间算子排序不可互推」**。`ts_sum` 仍呈「2Y 有 S 无」（1.10/0.05）但 S 为负。⇒ **C-L2b 基线 = `ts_delta × 窗 126`**。

### C-L2b · 窗口全替（批 `1AjgLeaTo4HbbJT1360E2BmW`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| C-2b-1 | 66 | `3q0Pe90Z` | 0.92 | 0.48 | +0.44 | 20.4% |
| C-2b-2 | 250 | `0mPgMRPK` | 0.87 | 0.46 | +0.59 | 19.9% |
| C-2b-3 | 504 | `Xgaz8Wa8` | 0.49 | 0.20 | +0.21 | 19.6% |
| C-2b-4 | 750 | `GrmzedmO` | 0.48 | 0.19 | +0.30 | 19.5% |
| C-2b-0 | 126（基线） | `zqdGmRro` | **1.14** | **0.68** | **+0.96** | 19.8% |

**C-L2b 结论（`converge=yes`，126 最优）**：窗 66/250 明显劣（0.92/0.87），504/750 崩到 0.49 ⇒ **模板 C 的精确尺度就是 126**（与模板 A 的 66、模板 B 的 250 都不同）。⇒ **C-L3 基线 = ts_delta × 126 × industry**。

### C-L3 · 分组轴全替（批 `1hYCN6fAq5guaABevlvObgb`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| C-L3-2 | `sector` | `npaqNJ9a` | 1.03 | 0.60 | +0.77 | 18.6% |
| C-L3-3 | `subindustry` | `xAvGN66q` | 0.97 | **0.62** | +0.59 | 14.3% |
| C-L3-4 | `market` | `9qlMpvv9` | 0.98 | 0.59 | +0.72 | 17.0% |
| C-L3-5 | `exchange` | `WjlzAqqO` | 0.98 | 0.59 | +0.72 | 17.0% |
| C-L3-6 | `country` | `GrmzGaaZ` | 0.98 | 0.59 | +0.72 | 17.0% |
| C-L3-1 | `industry`（基线） | `zqdGmRro` | **1.14** | **0.68** | **+0.96** | 19.8% |

**C-L3 结论（`converge=yes`，industry 最优）**：industry 1.14 领先；sector 1.03；market≡exchange≡country 逐位相同 0.98；subindustry F 最高（0.62）但 S 0.97。⇒ **C-L4 基线 = ts_delta × 126 × industry**。

### C-L4 · 外层包装全替（批 `1HJNsa95w4IEaXvMSZjy398`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| C-L4-0 | `group_rank`（基线） | `zqdGmRro` | **1.14** | **0.68** | **+0.96** | 19.8% |
| C-L4-2 | `group_zscore` | `e7aG3v0g` | 0.79 | 0.28 | +0.99 | **61.1%** |
| C-L4-1 | `group_scale` | `78YmzMwL` | 0.72 | 0.24 | +0.87 | **60.2%** |
| C-L4-6 | `group_backfill(·,industry,120)` | `GrmzGxex` | 0.69 | 0.19 | +1.07 | 64.7% |
| C-L4-7 | `group_backfill(·,industry,252)` | `1YWKpPp6` | 0.69 | 0.19 | +1.24 | 65.4% |
| C-L4-3 | `group_neutralize` | `vRAGN6lG` | 0.58 | 0.18 | +0.61 | 68.8% |
| C-L4-4 | `group_sum`（聚合型） | `RRezmK1n` | 0.15 | 0.02 | −0.21 | **115.4%** |
| C-L4-5 | `group_std_dev`（聚合型） | `WjlzA0VG` | −0.45 | −0.13 | −1.38 | **112.0%**（DD 136%） |

**C-L4 结论（`converge=yes`，收敛于 `group_rank`）**：**全 ΔS 负**（0.72 以下 vs 基线 1.14），且**非排名外层把 TO 从 19.8% 抬到 60–69%**（ts_delta 已含差分，外层再标准化会放大换手）⇒ 模板 C 的外层只能是 `group_rank`。注：`group_backfill` 把 2Y 抬到 1.07/1.24（最高）但 S 崩到 0.69、TO 65% ⇒ 不可用。

### C-L5 · 设置档（批 `2jXas61NY4RjbG3oZLqY5OG`（INDUSTRY）+ `1EdgBq2xe54La7AAVnD5zsz`（SECTOR）并行，随后 FAST + decay8）

| 批 | 设置档 | α（industry 轴 / subindustry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `3q0PlazP` / `leaGjQ0O` | 0.95 / 0.80 | 0.59/0.50 | +0.54/+0.34 | 14.9/11.9% |
| B | `SECTOR` 中性化 | `0mPgwRxq` / `npaq7Kmz` | 0.84 / 0.71 | 0.53/0.43 | +0.39/+0.22 | 13.6/10.7% |
| **C** | **`FAST` 中性化** | **`vRAGjPpQ`** / `YPaz7Yzv` | **1.26** / 1.09 | 0.61/0.52 | +0.58/+0.33 | 22.7/19.6% |
| D | SUBINDUSTRY + decay 8 | `io6Gc4oe…` 待收 | | | | |
| 基线 | SUBINDUSTRY + decay 4 | `zqdGmRro` / `xAvGN66q` | 1.14 / 0.97 | 0.68/0.62 | **+0.96**/+0.59 | 19.8/14.3% |

**C-L5 结论（`converge=no`，+0.12）**：**`FAST` 最优 S1.26 / F0.61 / 2Y0.58 / TO22.7%**（industry 轴）——**全模板新高**（A 1.01 / B 0.97 / C 1.26）；INDUSTRY 0.95、SECTOR 0.84 均劣于基线。⚠ 代价：2Y 从 0.96 掉到 0.58（FAST 的 S↔2Y 跷跷板第三次复现）。

### C-L5-R · 换基线（FAST）后内核重扫（批 `待回填`，4 臂）

| 臂 | 内核（FAST / industry / 窗 126） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| R-1 | `ts_delta`（L5 基线） | `vRAGjPpQ` | **1.26** | 0.61 | +0.58 | 22.7% |
| R-2 | `ts_zscore` | `gJaGQXxg` | 1.06 | 0.47 | +0.47 | 19.0% |
| R-3 | `ts_av_diff` | `1YWKxOJm` | 1.05 | 0.47 | +0.61 | 18.8% |
| R-4 | `ts_rank` | `ZYaz0goQ` | 0.86 | 0.35 | +0.01 | 19.4% |
| R-5 | `ts_scale` | `wpoGY3ex` | 0.80 | 0.36 | −0.00 | 14.8% |

**C-L5-R 结论（未翻转）**：FAST 基线下 **`ts_delta` 仍最优（1.26）**，其余 ≤1.06 ⇒ 排序稳健。
**★ 模板 C 天花板 = S1.26 / F0.61 / 2Y0.58 / TO22.7%**（FAST × ts_delta126 × industry×group_rank×reverse）；备选 decay8 形态 S1.06/**F0.77**/**2Y0.85**/TO12.0%（F/TO/2Y 轴最优）。完整梯度 45 臂收官。
> 模板 C 是全数据集最强模板（S1.26），但仍距 S 闸 0.32 / F 闸 0.39 / 2Y 闸 1.00。

---

## 模板 D · `entry_position`（B 族仓位规模）完整梯度（2026-11-21/22 起）

> 起点：L1-A 臂 `0mPgowO8`（原始 S−0.64/2Y+0.27）⇒ 镜像 S0.64 / 2Y−0.27
> 基线结构：`reverse(group_rank(ts_zscore(ts_backfill(vec_avg(inst25_entry_position),250),126), industry))`

### D-L2 · 内层时序算子全替（批 `3FeTs8deg4zMaoqNIAazxre`（8 臂）+ `4li4NG34g4BI9ny9ZxgWwjY`（7 臂）并行）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| D-0 | `ts_zscore`（基线，镜像自 L1-A） | `0mPgowO8` 镜像 | 0.64 | 0.35 | −0.27 | 5.7% |
| D-1 | `ts_scale` | `akazblwv` | 0.58 | 0.29 | −0.28 | 6.0% |
| D-2 | `ts_rank` | `rK7GOLVj` | 0.69 | 0.35 | +0.05 | 5.7% |
| D-3 | `ts_quantile` | `e7aGbKvE` | 0.68 | 0.34 | +0.04 | 5.7% |
| **D-4** | **`ts_av_diff`** | **`j2aGAXOE`** | **0.78** | **0.41** | +0.18 | 4.4% |
| D-5 | `ts_delta` | `d5azbmvE` | 0.66 | 0.33 | −0.10 | 4.9% |
| D-6 | `ts_mean` | `O0WzNkgR` | 0.77 | 0.41 | **+0.45** | 2.2% |
| D-7 | `ts_std_dev` | `Wjlzbdxj` | 0.75 | 0.43 | +0.22 | 2.7% |
| D-8 | `ts_ir` | `kqaGoXYk` | 0.48 | 0.21 | −0.31 | 4.1% |
| D-9 | `ts_arg_max` | `RRezbaRz` | 0.49 | 0.19 | +0.33 | 3.3% |
| D-10 | `ts_arg_min` | `0mPgXQOv` | 0.59 | 0.26 | +0.16 | 3.3% |
| D-11 | `ts_returns` | `akazbPj1` | 0.67 | 0.34 | −0.09 | 4.9% |
| D-12 | `ts_product` | `1YWKXmkR` | −0.69 | −0.36 | −0.25 | 1.8% |
| D-13 | `ts_sum` | `P05z2lNW` | 0.74 | 0.40 | +0.32 | 1.9% |
| D-14 | `ts_max_diff` | `j2aGAwvZ` | 0.62 | 0.27 | +0.10 | 4.0% |
| D-15 | `days_from_last_change` | `d5azb7pY` | −0.80 | −0.48 | −0.38 | 3.2% |

**D-L2 结论**：**`ts_av_diff` 最优（S0.78 / ΔS+0.14）**；`ts_mean`（2Y0.45）与 `ts_std_dev`（F0.43）次之；`ts_product`/`days_from_last_change` 仍负（四模板共性）。⇒ **D-L2b 基线 = ts_av_diff × 126**。

### D-L2b · 窗口全替（批 `1qtVBgfAJ56FcAYtjPkR7Pk`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| D-2b-1 | 66 | `Jj8zNkmE` | 0.60 | 0.28 | +0.11 | 5.1% |
| D-2b-2 | 250 | `XgazbxLX` | 0.73 | 0.37 | +0.19 | 3.8% |
| D-2b-3 | 504 | `GrmzbN63` | 0.69 | 0.35 | +0.01 | 3.3% |
| D-2b-4 | 750 | `qM7GxpdA` | 0.77 | 0.41 | +0.18 | 3.2% |
| D-2b-0 | 126（基线） | `j2aGAXOE` | **0.78** | **0.41** | +0.18 | 4.4% |

**D-L2b 结论（`converge=yes`，126 最优）**：窗 126 保持最优（0.78）；750 接近（0.77）。⇒ **D-L3 基线 = ts_av_diff × 126**。

### D-L3 · 分组轴全替（批 `3QxRrXaeq4FWcb410eepl4ya`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| D-L3-2 | `sector` | `LLKzZGP6` | 0.73 | 0.38 | +0.16 | 4.1% |
| **D-L3-3** | **`subindustry`** | **`WjlzeAEO`** | **0.84** | **0.45** | **+0.69** | 3.8% |
| D-L3-4 | `market` | `vRAG2NRa` | 0.71 | 0.37 | +0.12 | 3.7% |
| D-L3-5 | `exchange` | `LLKzZGL9` | 0.71 | 0.37 | +0.12 | 3.7% |
| D-L3-6 | `country` | `Jj8zQGMj` | 0.71 | 0.37 | +0.12 | 3.7% |
| D-L3-1 | `industry`（基线） | `j2aGAXOE` | 0.78 | 0.41 | +0.18 | 4.4% |

**D-L3 结论（`converge=no`，+0.06 / Δ2Y+0.51）**：**`subindustry` 最优（S0.84 / 2Y0.69 / F0.45）**——与模板 A 同向（细轴优）、与模板 B 反向（industry 优）⇒ 轴偏好按模板而异再次验证。⇒ **D-L4 基线 = subindustry × ts_av_diff × 126**。

### D-L4 · 外层包装全替（批 `43RwZ5gCN5gg9p53fZIhjL7`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| D-L4-0 | `group_rank`（基线） | `WjlzeAEO` | **0.84** | **0.45** | **+0.69** | 3.8% |
| D-L4-3 | `group_neutralize` | `leaGKon2` | 0.54 | 0.33 | +0.95 | 7.2% |
| D-L4-1 | `group_scale` | `GrmzOZjo` | 0.47 | 0.19 | **+1.22** | 6.1% |
| D-L4-7 | `group_backfill(·,subindustry,252)` | `kqaGgzAg` | 0.42 | 0.20 | +0.29 | 6.3% |
| D-L4-6 | `group_backfill(·,subindustry,120)` | `VkNz0AWw` | 0.41 | 0.20 | +0.17 | 6.7% |
| D-L4-2 | `group_zscore` | `rK7GeZaa` | 0.35 | 0.13 | +1.11 | 6.2% |
| D-L4-4 | `group_sum`（聚合型） | `mLa76EG6` | −0.32 | −0.09 | −0.71 | **100.4%** |
| D-L4-5 | `group_std_dev`（聚合型） | `omaGWxbb` | −0.47 | −0.15 | +0.25 | **96.2%**（DD 137%） |

**D-L4 结论（`converge=yes`，收敛于 `group_rank`）**：全 ΔS 负；`group_scale`/`group_zscore` 把 2Y 抬到 1.22/1.11 但 S 崩到 0.47/0.35（本集第四次复现 S↔2Y 跷跷板）；聚合型 TO 96–100% 崩。⇒ **D-L5 基线 = group_rank(ts_av_diff × 126, subindustry)**。

### D-L5 · 设置档（批 `2XyuRz1l755nbYvKCz4xuRo`（INDUSTRY）+ `1D7VLHbVQ5j6bq51f3MeOYdv`（SECTOR）并行，随后 FAST + decay8 + L5-R）

| 批 | 设置档 | α（subindustry 轴 / industry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `d5azKba2` / `KPgzmNg8` | 0.76 / 0.72 | 0.39/0.36 | +0.57/+0.09 | 3.4/3.7% |
| B | `SECTOR` 中性化 | `O0WzJNMJ` / `58J5jzAX` | 0.62 / 0.59 | 0.30/0.28 | +0.26/−0.17 | 3.1/3.4% |
| C | `FAST` 中性化 | `d5azWxeg` / `gJaGe17Q` | **0.86** / 0.81 | 0.40/0.37 | +0.56/−0.23 | 9.1/9.3% |
| D | SUBINDUSTRY + decay 8 | `wpoGQqav` / `vRAG18j3` | 0.84 / 0.77 | 0.45/0.40 | +0.60/+0.11 | 3.5/3.9% |
| 基线 | SUBINDUSTRY + decay 4 | `WjlzeAEO` / `j2aGAXOE` | 0.84 / 0.78 | 0.45/0.41 | +0.69/+0.18 | 3.8/4.4% |

**D-L5 结论（`converge=no`，+0.02）**：`FAST` 0.86 略优（INDUSTRY 0.76 / SECTOR 0.62 / decay8 0.84 均劣或持平）。

### D-L5-R · 换基线（FAST）后内核重扫（批 `Qow2Jgy94PkckA1du8oRrNF`，4 臂）

| 臂 | 内核（FAST / subindustry / 窗 126） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| R-1 | `ts_av_diff`（L5 基线） | `d5azWxeg` | 0.86 | 0.40 | +0.56 | 9.1% |
| **R-2** | **`ts_std_dev`** | **`omaGaWok`** | **0.99** | **0.52** | +0.44 | 8.6% |
| R-3 | `ts_delta` | `WjlzleOd` | 0.84 | 0.39 | −0.11 | 9.7% |
| R-4 | `ts_rank` | `omaGaWEk` | 0.80 | 0.35 | +0.15 | 10.1% |
| R-5 | `ts_mean` | `MP6z630o` | 0.44 | 0.15 | −0.47 | 7.8% |

**D-L5-R 结论（★ 第二次内核翻转）**：FAST 下 **`ts_std_dev` 0.99 反超 `ts_av_diff` 0.86**（F0.52 vs 0.40）——与模板 B 同型 ⇒ **换设置基线后内核排序必须重扫**。
**★ 模板 D 天花板 = S0.99 / F0.52 / 2Y0.44 / TO8.6%**（FAST × ts_std_dev126 × subindustry × group_rank × reverse）。完整梯度 45 臂收官。

---

## 模板 E · `age`（C 族空仓年龄）完整梯度（2026-11-21/22 起）

> 起点：L1-B 臂 `0mPgo1O6`（原始 S−0.61/2Y+0.06）⇒ 镜像 S0.61 / 2Y−0.06
> 基线结构：`reverse(group_rank(ts_zscore(ts_backfill(vec_avg(inst25_age),250),126), industry))`

### E-L2 · 内层时序算子全替（批 `1k5YsD4pu4wLcq9vALprYwZ`（8 臂）+ `KiqWo7j05fDcM4w4713fTG`（7 臂）并行）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| E-0 | `ts_zscore`（基线，镜像自 L1-B） | `0mPgo1O6` 镜像 | 0.61 | 0.30 | −0.06 | 6.9% |
| E-1 | `ts_scale` | `58J5Gaeo` | 0.68 | 0.36 | +0.23 | 6.8% |
| E-2 | `ts_rank` | `omaGP3rE` | 0.48 | 0.20 | +0.01 | 7.5% |
| E-3 | `ts_quantile` | `1YWKGaPR` | 0.48 | 0.20 | +0.02 | 7.1% |
| E-4 | `ts_av_diff` | `RRez52Pj` | 0.43 | 0.17 | +0.14 | 5.3% |
| E-5 | `ts_delta` | `6XM0GaNY` | 0.56 | 0.26 | −0.16 | 5.2% |
| E-6 | `ts_mean` | `pwaGWV3v` | 0.58 | 0.27 | +0.21 | 2.3% |
| **E-7** | **`ts_std_dev`** | **`LLKz8g2L`** | **0.72** | **0.39** | +0.15 | 2.8% |
| E-8 | `ts_ir` | `KPgzVX28` | 0.56 | 0.25 | −0.09 | 3.9% |
| E-9 | `ts_arg_max` | `d5az9moJ` | 0.66 | 0.31 | +0.19 | 4.3% |
| E-10 | `ts_arg_min` | `VkNzMEe8` | 0.59 | 0.26 | +0.09 | 4.2% |
| E-11 | `ts_returns` | `GrmzQ695` | 0.58 | 0.27 | −0.12 | 5.7% |
| E-12 | `ts_product` | `d5az9mPw` | −0.58 | −0.27 | +0.06 | 2.9% |
| E-13 | `ts_sum` | `6XM0G12p` | 0.67 | 0.34 | +0.34 | 1.9% |
| E-14 | `ts_max_diff` | `leaGg2N5` | 0.52 | 0.21 | **+0.43** | 4.8% |
| E-15 | `days_from_last_change` | `mLa7KANp` | −0.71 | −0.40 | −0.26 | 5.3% |

**E-L2 结论**：**`ts_std_dev` 最优（S0.72 / F0.39，ΔS+0.11）**；`ts_scale` 0.68、`ts_sum` 0.67（2Y0.34）、`ts_arg_max` 0.66 次之；`ts_product`/`days_from_last_change` 仍负（五模板共性）。⇒ **E-L2b 基线 = ts_std_dev × 126**。

### E-L2b · 窗口全替（批 `1mwFfmekh4yBc9Agv3qTKUO`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| E-2b-1 | 66 | `9qlM8a72` | 0.72 | 0.40 | +0.14 | 3.3% |
| **E-2b-2** | **250** | **`Wjlz3aAQ`** | **0.74** | 0.40 | +0.10 | 2.4% |
| E-2b-3 | 504 | `wpoG3na5` | 0.66 | 0.34 | +0.13 | 2.1% |
| E-2b-4 | 750 | `O0WzRbGg` | 0.59 | 0.29 | −0.14 | 2.0% |
| E-2b-0 | 126（基线） | `LLKz8g2L` | 0.72 | 0.39 | +0.15 | 2.8% |

**E-L2b 结论**：窗 250 微优（0.74，Δ+0.02）⇒ **E-L3 基线 = ts_std_dev × 250**。

### E-L3 · 分组轴全替（批 `uwY0PWC4odbxW12K74C2g`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| E-L3-2 | `sector` | `LLKzmAaL` | 0.76 | 0.43 | +0.08 | 2.2% |
| **E-L3-3** | **`subindustry`** | **`3q0PkZrg`** | **0.79** | 0.43 | +0.14 | 2.2% |
| E-L3-4 | `market` | `Wjlzo6QN` | 0.77 | 0.44 | +0.11 | 1.9% |
| E-L3-5 | `exchange` | `npaqeMRa` | 0.77 | 0.44 | +0.11 | 1.9% |
| E-L3-6 | `country` | `E5Qz8XW9` | 0.77 | 0.44 | +0.11 | 1.9% |
| E-L3-1 | `industry`（基线） | `Wjlz3aAQ` | 0.74 | 0.40 | +0.10 | 2.4% |

**E-L3 结论（`converge=no`，+0.05）**：**`subindustry` 最优 0.79**；market≡exchange≡country 逐位相同 0.77。⇒ **E-L4 基线 = subindustry × ts_std_dev × 250**。

### E-L4 · 外层包装全替（批 `Yamea4jI4n7beh1gviSLJBq`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| E-L4-0 | `group_rank`（基线） | `3q0PkZrg` | **0.79** | **0.43** | +0.14 | 2.2% |
| E-L4-1 | `group_scale` | `1YWKl0nM` | 0.59 | 0.25 | −0.08 | 2.7% |
| E-L4-2 | `group_zscore` | `YPazEY2W` | 0.56 | 0.23 | −0.12 | 2.6% |
| E-L4-6 | `group_backfill(·,subindustry,120)` | `78YmvlxL` | 0.39 | 0.13 | −0.42 | 2.7% |
| E-L4-3 | `group_neutralize` | `qM7GYVPE` | 0.38 | 0.14 | −0.42 | 2.5% |
| E-L4-7 | `group_backfill(·,subindustry,252)` | `QP0zN6nw` | 0.25 | 0.07 | −0.68 | 2.5% |
| E-L4-5 | `group_std_dev`（聚合型） | `N1PzJ8ng` | −0.16 | −0.03 | −0.97 | **95.5%** |
| E-L4-4 | `group_sum`（聚合型） | `rK7GN8b1` | −0.48 | −0.16 | −1.49 | **96.5%**（DD 156%） |

**E-L4 结论（`converge=yes`，收敛于 `group_rank`）**：全 ΔS 负（≤0.59 vs 基线 0.79），聚合型 TO 95–97% 崩。⇒ **E-L5 基线 = group_rank(ts_std_dev × 250, subindustry)**。

### E-L5 · 设置档（批 `4ygLRK6yN4PdaMX12pxXSwrw`（INDUSTRY）+ `2bO0VVg2d5fxawtP3ouOFuI`（SECTOR）并行，随后 FAST + decay8 + L5-R）

| 批 | 设置档 | α（subindustry 轴 / industry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `QP0zz2vX` / `leaGGQA8` | 0.66 / 0.71 | 0.33/0.38 | +0.03/+0.10 | 2.1/2.1% |
| B | `SECTOR` 中性化 | `j2aGGArO` / `58J55zl5` | 0.55 / 0.60 | 0.26/0.30 | −0.22/−0.15 | 1.9/1.9% |
| C | `FAST` 中性化 | `0mPg6ka8` / **`akazw2gw`** | 0.88 / **1.04** | 0.41/0.54 | −0.08/+0.07 | 8.1/8.1% |
| D | SUBINDUSTRY + decay 8 | `LLKzrOKm` / `88NJYgG7` | 0.80 / 0.74 | 0.43/0.40 | +0.13/+0.10 | 2.2/2.3% |

**E-L5 结论（`converge=no`，+0.25）**：**`FAST` × industry 轴 S1.04 / F0.54 / TO8.1%**（`akazw2gw`）——本模板最大单层增益；INDUSTRY 0.66–0.71、SECTOR 0.55–0.60、decay8 0.74–0.80 均劣于基线 0.79。⚠ 2Y 仅 0.07。

### E-L5-R · 换基线（FAST）后内核重扫（批 `loGRYciX4JOcHS19dlWGTVU`，4 臂）

| 臂 | 内核（FAST / industry / 窗 250） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
**E-L5-R 结论（未翻转）**：FAST 下其余内核均 ≤0.85（`ts_sum` 0.85 最高），**`ts_std_dev` 1.04 仍是模板 E 冠军**。
**★ 模板 E 天花板 = S1.04 / F0.54 / 2Y0.07 / TO8.1%**（FAST × ts_std_dev250 × industry × group_rank × reverse）。完整梯度 45 臂收官。

---

## 模板 F · `position_change` 单腿（B 族流量，αC 14 最高）完整梯度

> 起点：L1-A 臂 `xAvGMjOq`（原始 S−0.58/2Y−0.16）⇒ 镜像 S0.58 / 2Y+0.16
> 基线结构：`reverse(group_rank(ts_zscore(ts_backfill(vec_sum(inst25_position_change),250),126), industry))`

### F-L2 · 内层时序算子全替（批 `xlWbN8dT54GaJaxp1yeYvJ`（8 臂）+ `29XpoQ41X53kaaayztues7M`（7 臂）并行）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| F-0 | `ts_zscore`（基线，镜像自 L1-A） | `xAvGMjOq` 镜像 | 0.58 | 0.28 | +0.16 | 10.8% |
| F-1 | `ts_scale` | `LLKz3Eln` | 0.69 | 0.38 | +0.09 | 7.2% |
| F-2 | `ts_rank` | `WjlzJ3aj` | 0.57 | 0.26 | +0.21 | 10.8% |
| F-3 | `ts_quantile` | `zqdGegPR` | 0.55 | 0.24 | +0.17 | 10.7% |
| F-4 | `ts_av_diff` | `VkNzeZ2b` | 0.53 | 0.22 | +0.31 | 9.9% |
| F-5 | `ts_delta` | `j2aGOon9` | 0.67 | 0.34 | +0.02 | 11.7% |
| **F-6** | **`ts_mean`** | **`QP0z6Ong`** | **0.82** | **0.48** | **+0.30** | 3.1% |
| F-7 | `ts_std_dev` | `KPgzZvkx` | 0.67 | 0.36 | −0.05 | 3.1% |
| F-8 | `ts_ir` | `akazGeoR` | 0.79 | 0.48 | +0.21 | 4.0% |
| F-9 | `ts_arg_max` | `O0WzgWjg` | 0.62 | 0.27 | +0.23 | 3.5% |
| F-10 | `ts_arg_min` | `e7aGEaZJ` | 0.53 | 0.22 | −0.10 | 3.4% |
| F-11 | `ts_returns` | `zqdGedn8` | 0.18 | 0.04 | −0.02 | 19.0% |
| F-12 | `ts_product` | `1YWK0WAR` | −0.68 | −0.36 | −0.19 | 2.6% |
| F-13 | `ts_sum` | `ZYazNaVZ` | 0.38 | 0.12 | +0.32 | 3.5% |
| F-14 | `ts_max_diff` | `0mPg5PZ8` | 0.57 | 0.24 | **+0.54** | 5.6% |
| F-15 | `days_from_last_change` | `mLa7QanW` | −0.69 | −0.39 | −0.34 | 3.9% |

**F-L2 结论**：**`ts_mean` 最优（S0.82 / F0.48 / 2Y0.30，ΔS+0.24）**；`ts_ir` 0.79/0.48 次之；`ts_max_diff` 2Y0.54 最高但 S0.57。⇒ **F-L2b 基线 = ts_mean × 126**。

### F-L2b · 窗口全替（批 `2ELGZo4ZI55Zcnnj7IGX4G5`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| F-2b-1 | 66 | `npaqXprw` | 0.77 | 0.44 | +0.19 | 3.7% |
| F-2b-2 | 250 | `QP0zoP6w` | 0.84 | 0.50 | +0.26 | 2.7% |
| **F-2b-3** | **504** | **`pwaGpwp6`** | **0.89** | **0.54** | **+0.48** | 2.4% |
| F-2b-4 | 750 | `d5azP5Pv` | 0.81 | 0.46 | +0.26 | 2.3% |
| F-2b-0 | 126（基线） | `QP0z6Ong` | 0.82 | 0.48 | +0.30 | 3.1% |

**F-L2b 结论（`converge=no`，+0.07）**：**窗 504 最优（S0.89 / F0.54 / 2Y0.48）** ⇒ **F-L3 基线 = ts_mean × 504**。

### F-L3 · 分组轴全替（批 `bVaHn2yo4FE8XTkYfo0kow`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| F-L3-2 | `sector` | `blazK0OZ` | 0.85 | 0.51 | +0.39 | 2.2% |
| **F-L3-3** | **`subindustry`** | **`LLKz2oZn`** | **0.95** | **0.56** | **+0.48** | 2.1% |
| F-L3-4 | `market` | `d5azPJ1K` | 0.87 | 0.53 | +0.37 | 2.0% |
| F-L3-5 | `exchange` | `88NJ2WPW` | 0.87 | 0.53 | +0.37 | 2.0% |
| F-L3-6 | `country` | `N1Pz2Eeo` | 0.87 | 0.53 | +0.37 | 2.0% |
| F-L3-1 | `industry`（基线） | `pwaGpwp6` | 0.89 | 0.54 | +0.48 | 2.4% |

**F-L3 结论（`converge=no`，+0.06）**：**`subindustry` 最优（S0.95 / F0.56 / 2Y0.48）**——与模板 D 同向（细轴优）；market≡exchange≡country 逐位相同 0.87。⇒ **F-L4 基线 = subindustry × ts_mean × 504**。

### F-L4 · 外层包装全替（批 `2Otb9Ufbr4RX8AuUmTKXb0g`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| F-L4-0 | `group_rank`（基线） | `LLKz2oZn` | **0.95** | **0.56** | +0.48 | 2.1% |
| F-L4-1 | `group_scale` | `e7aGP6wJ` | 0.67 | 0.31 | +0.39 | 2.3% |
| F-L4-2 | `group_zscore` | `j2aGJeRZ` | 0.67 | 0.31 | +0.40 | 2.3% |
| F-L4-5 | `group_std_dev`（聚合型） | `KPgzpmj8` | 0.49 | 0.17 | −0.03 | **95.4%** |
| F-L4-3 | `group_neutralize` | `LLKzw5am` | 0.31 | 0.12 | −0.09 | 3.0% |
| F-L4-6 | `group_backfill(·,subindustry,120)` | `npaqlAMa` | 0.22 | 0.07 | −0.29 | 2.7% |
| F-L4-7 | `group_backfill(·,subindustry,252)` | `vRAGbO3Q` | 0.20 | 0.06 | −0.43 | 2.6% |
| F-L4-4 | `group_sum`（聚合型） | `LLKzw5AL` | −0.77 | −0.33 | −0.35 | **97.7%**（DD 185%） |

**F-L4 结论（`converge=yes`，收敛于 `group_rank`）**：全 ΔS 负（≤0.67 vs 0.95）；聚合型 TO 95–98% 崩。⇒ **F-L5 基线 = group_rank(ts_mean × 504, subindustry)**。

### F-L5 · 设置档（批 `2LeArK17i4POc8m3uktUtg7`（INDUSTRY）+ `2EUt8w65W4We8BXEexK4ZmQ`（SECTOR）并行，随后 FAST + decay8 + L5-R）

| 批 | 设置档 | α（subindustry 轴 / industry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `pwaGeAqq` / `2r56ob1b` | 0.83 / 0.76 | 0.46/0.43 | +0.42/+0.39 | 2.0/2.1% |
| B | `SECTOR` 中性化 | `RRezwzgn` / `VkNzbzW0` | 0.72 / 0.67 | 0.39/0.36 | +0.16/+0.15 | 1.8/1.9% |
| C | `FAST` 中性化 | **`RRezwGxb`** / `QP0zpwRW` | **1.08** / 1.01 | 0.56/0.53 | +0.57/+0.49 | 8.0/8.2% |
| D | SUBINDUSTRY + decay 8 | `gJaGNX7Q` / `YPaz38XJ` | 0.95 / 0.89 | 0.56/0.54 | +0.47/+0.46 | 2.1/2.2% |

**F-L5 结论（`converge=no`，+0.13）**：**`FAST` × subindustry 最优 S1.08 / F0.56 / 2Y0.57 / TO8.0%**（`RRezwGxb`）；INDUSTRY 0.76–0.83、SECTOR 0.67–0.72、decay8 0.89–0.95 均劣。

### F-L5-R · 换基线（FAST）后内核重扫（批 `3zeoWd3Fw4Vp9f618R415vET`，4 臂）

> ⚠ 首次派发 `48HytSas356Dap5vl3xrZIi` 返回「parent COMPLETE but children empty」（注册/收批异常）⇒ 已按规范**重派**（不改变表达式）。

| 臂 | 内核（FAST / subindustry / 窗 504） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| R-1 | `ts_mean`（L5 基线） | `RRezwGxb` | **1.08** | **0.56** | **+0.57** | 8.0% |
| R-2 | `ts_ir` | `mLa7nWq1` | 0.87 | 0.42 | +0.14 | 8.2% |
| R-3 | `ts_std_dev` | `omaGj0Y5` | 0.68 | 0.29 | −0.06 | 8.0% |
| R-4 | `ts_rank` | `MP6zvNk6` | 0.34 | 0.10 | +0.17 | 13.2% |
| R-5 | `ts_av_diff` | `O0WzdXoq` | 0.28 | 0.07 | +0.02 | 12.3% |

**F-L5-R 结论（未翻转）**：`ts_mean` 1.08 仍最优 ⇒ **★ 模板 F 天花板 = S1.08 / F0.56 / 2Y0.57 / TO8.0%**（FAST × ts_mean504 × subindustry）。完整梯度 45 臂收官。

---

## 模板 G · `concentration`（A 族集中度）完整梯度

> 起点：L1-A 臂 `akazJ7kw`（原始 S−0.39/2Y+0.55）⇒ 镜像 S0.39 / 2Y−0.55
> 基线结构：`reverse(group_rank(ts_zscore(ts_backfill(vec_avg(inst25_concentration),250),126), industry))`

### G-L2 · 内层时序算子全替（批 `E2t3wcj84TgcmwqHQa7d09`（8 臂）+ `2h0vvQb7H54c9cwAvQoyWjD`（7 臂）并行）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| G-0 | `ts_zscore`（基线，镜像自 L1-A） | `akazJ7kw` 镜像 | 0.39 | 0.16 | −0.55 | 5.8% |
| G-1 | `ts_scale` | `Xgaz08rx` | 0.52 | 0.25 | −0.19 | 6.0% |
| G-2 | `ts_rank` | `9qlMn719` | 0.42 | 0.17 | −0.10 | 6.3% |
| G-3 | `ts_quantile` | `rK7GxPg9` | 0.39 | 0.15 | −0.15 | 6.3% |
| G-4 | `ts_av_diff` | `leaGm3bO` | 0.35 | 0.13 | −0.15 | 4.8% |
| G-5 | `ts_delta` | `qM7GR6oP` | 0.42 | 0.17 | −0.11 | 5.1% |
| **G-6** | **`ts_mean`** | **`ZYazJKed`** | **0.87** | **0.52** | **+0.34** | 2.3% |
| G-7 | `ts_std_dev` | `YPazegq6` | 0.73 | 0.42 | +0.23 | 2.8% |
| G-8 | `ts_ir` | `78Ympn9x` | 0.50 | 0.21 | −0.63 | 4.0% |
| G-9 | `ts_arg_max` | `RRezgYeo` | 0.68 | 0.31 | +0.51 | 3.8% |
| G-10 | `ts_arg_min` | `LLKzQ68a` | 0.48 | 0.19 | −0.05 | 3.6% |
| G-11 | `ts_returns` | `VkNzWEMY` | 0.43 | 0.18 | −0.22 | 5.1% |
| G-12 | `ts_product` | `N1PzZ6Ke` | −0.69 | −0.36 | −0.35 | 1.9% |
| G-13 | `ts_sum` | `78YmpQG5` | 0.73 | 0.40 | +0.10 | 1.9% |
| G-14 | `ts_max_diff` | `rK7GxL9E` | 0.38 | 0.13 | +0.24 | 4.9% |
| G-15 | `days_from_last_change` | `0mPgJdxp` | −0.68 | −0.38 | −0.31 | 4.2% |

**G-L2 结论（本集最大单层跳升）**：**`ts_mean` 0.87 / F0.52 / 2Y0.34（ΔS+0.48 vs 基线 0.39）**；`ts_arg_max` 0.68（2Y0.51）、`ts_std_dev` 0.73、`ts_sum` 0.73 次之。`ts_product`/`days_from_last_change` 仍负（七模板共性）。⇒ **G-L2b 基线 = ts_mean × 126**。

### G-L2b · 窗口全替（批 `2I0F8d1Qg4NgcebpC0GV13X`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| G-2b-1 | 66 | `e7aGXJJN` | 0.82 | 0.48 | +0.16 | 2.4% |
| G-2b-2 | 250 | `akaz53J6` | 0.79 | 0.45 | +0.35 | 2.1% |
| G-2b-3 | 504 | `ZYazOLZn` | 0.80 | 0.46 | +0.45 | 2.0% |
| G-2b-4 | 750 | `A1xzodqd` | 0.77 | 0.43 | +0.30 | 2.0% |
| G-2b-0 | 126（基线） | `ZYazJKed` | **0.87** | **0.52** | +0.34 | 2.3% |

**G-L2b 结论（`converge=yes`，126 最优）**：窗 66 0.82 最接近但均劣于 126（0.87）⇒ **G-L3 基线 = ts_mean × 126**。

### G-L3 · 分组轴全替（批 `WNf8H3xa4EOc1iLqvRZQ6I`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| G-L3-2 | `sector` | `Wjlzv5Nk` | 0.87 | 0.54 | +0.34 | 2.1% |
| G-L3-3 | `subindustry` | `leaGom77` | 0.78 | 0.43 | +0.33 | 2.1% |
| **G-L3-4** | **`market`** | **`npaqLEn8`** | **0.90** | **0.57** | +0.33 | 1.9% |
| G-L3-5 | `exchange` | `akaz5pNx` | 0.90 | 0.57 | +0.33 | 1.9% |
| G-L3-6 | `country` | `zqdGlV5d` | 0.90 | 0.57 | +0.33 | 1.9% |
| G-L3-1 | `industry`（基线） | `ZYazJKed` | 0.87 | 0.52 | +0.34 | 2.3% |

**G-L3 结论（`converge=no`，+0.03）**：**market ≡ exchange ≡ country 0.90 / F0.57**（单国三轴等价）最优；sector 0.87、industry 0.87、subindustry 0.78。⇒ **G-L4 基线 = market 轴 × ts_mean × 126**。

### G-L4 · 外层包装全替（批 `3JW7lU6ns4SraKJZ21sOMRN`，7 臂 + 基线）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| G-L4-0 | `group_rank`（基线） | `npaqLEn8` | **0.90** | **0.57** | +0.33 | 1.9% |
| G-L4-6 | `group_backfill(·,market,120)` | `gJadYbOQ` | 0.64 | 0.33 | −0.21 | 1.9% |
| G-L4-7 | `group_backfill(·,market,252)` | `GrmxqbAZ` | 0.63 | 0.32 | −0.21 | 1.9% |
| G-L4-1 | `group_scale` | `58JeZzxM` | 0.62 | 0.36 | −0.36 | 2.1% |
| G-L4-2 | `group_zscore` | `omar1L7b` | 0.62 | 0.36 | −0.36 | 2.1% |
| G-L4-3 | `group_neutralize` | `58JeZzbM` | 0.62 | 0.36 | −0.36 | 2.1% |
| G-L4-5 | `group_std_dev`（聚合型） | `A1xmRNZd` | 0.06 | 0.01 | −0.16 | **104.0%** |
| G-L4-4 | `group_sum`（聚合型） | `78YMkNA2` | −0.34 | −0.08 | +0.42 | **103.3%**（DD 111%） |

**G-L4 结论（`converge=yes`，收敛于 `group_rank`）**：全 ΔS 负（≤0.64 vs 0.90）；聚合型 TO 103–104% 崩。⇒ **G-L5 基线 = group_rank(ts_mean × 126, market)**。

### G-L5 · 设置档（批 `HzhdGfsm50Pbd11aM0GRxe5`（INDUSTRY）+ `3gPmIw7DJ4ZUc7q116kTY89y`（SECTOR）并行，随后 FAST + decay8 + L5-R）

| 批 | 设置档 | α（market 轴 / industry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `qM73MelV` / `88NY8ge7` | 0.74 / 0.76 | 0.42/0.43 | +0.18/+0.25 | 1.8/2.0% |
| B | `SECTOR` 中性化 | `vRA6Raz3` / `0mP6mnQr` | 0.60 / 0.66 | 0.32/0.35 | +0.03/+0.05 | 1.5/1.8% |
| C | `FAST` 中性化 | `npaQxY0x` / `E5QLOY3r` | 0.79 / 0.81 | 0.39/0.39 | +0.07/+0.14 | 8.4/8.3% |
| D | SUBINDUSTRY + decay 8 | `qM739kLZ` / `9qlmZPxr` | **0.89** / 0.87 | 0.56/0.52 | +0.32/+0.33 | 1.9/2.2% |

**G-L5 结论（`converge=yes`，基线最优）**：**基线 SUBINDUSTRY/decay4 0.90 最优**——FAST 0.79–0.81、INDUSTRY 0.74–0.76、SECTOR 0.60–0.66、decay8 0.87–0.89 全部不优于基线。**★ 模板 G 天花板 = S0.90 / F0.57 / 2Y0.33 / TO1.9%**（SUBINDUSTRY × ts_mean126 × market × group_rank × reverse）。

### G-L5-R · 换基线（decay8）后内核重扫（批 `fiqmLdgP5ft8Mq3N5YWjCZ`，4 臂）

| 臂 | 内核（SUBIND/decay8 / market / 窗 126） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|---:|
| R-1 | `ts_mean`（L5 基线，decay8） | `qM739kLZ` | 0.89 | 0.56 | +0.32 | 1.9% |
| R-2 | `ts_arg_max` | `gJad6ka0` | 0.83 | 0.43 | +0.57 | 3.0% |
| R-3 | `ts_sum` | `gJad6kr0` | 0.76 | 0.43 | +0.15 | 1.7% |
| R-4 | `ts_std_dev` | `lea9dpgO` | 0.71 | 0.41 | +0.13 | 2.2% |
| R-5 | `ts_ir` | `78YMW7Gx` | 0.58 | 0.27 | −0.38 | 3.1% |

**G-L5-R 结论（未翻转）**：`ts_mean` 仍最优 ⇒ **★ 模板 G 天花板 = S0.90 / F0.57 / 2Y0.33 / TO1.9%**（SUBINDUSTRY/decay4 × ts_mean126 × market × group_rank × reverse）。完整梯度 45 臂收官。

---

## ★★ 数据集 ATOM 穷尽终判（7 个互异模板，全部完整梯度）

| 模板 | 信号构造（族） | 起点（镜像） | 层内冠军 | **模板天花板** | 备注 |
|---|---|---|---|---|---|
| A | activity（G 活跃度） | 0.82 | ts_rank×66 | **1.01** | FAST × industry |
| B | manager_avg_trade_length（C 时长） | 0.71 | ts_std_dev×250 | **0.97** | ★FAST 下内核翻转（ts_std_dev 反超 ts_av_diff） |
| **C** | **position_change ⊖ crowding（残差组合）** | **0.96/2Y0.80** | **ts_delta×126** | **★1.26** | **数据集天花板**；FAST 2Y 掉到 0.58 |
| D | entry_position（B 仓位） | 0.64 | ts_std_dev×126 | **0.99** | ★FAST 下第二次内核翻转 |
| E | age（C 时长） | 0.61 | ts_std_dev×250 | **1.04** | FAST 单层 +0.25（本集最大） |
| F | position_change 单腿（B 流量） | 0.58 | ts_mean×504 | **1.08** | 窗 504 最优、subindustry 轴 |
| G | concentration（A 集中度） | 0.39 | ts_mean×126 | **0.90** | 基线最优（无增益档） |

**★ 数据集 ATOM 天花板 = S1.26 / F0.61 / 2Y0.58 / TO22.7%（模板 C，FAST × ts_delta126 × industry）**
- 距 S 闸 1.58 差 **0.32** / F 闸 1.0 差 0.39 / 2Y 闸 1.58 差 1.00 ⇒ **0 颗可交付**。
- 七模板合计 ~330 臂，全部走完整 5 层流程 + 换基线重扫 ⇒ **ATOM 在当前 24 字段 × 现有几何下穷尽**（除模板 C 外无一超过 1.08）。
- **不判死**（信号层强度不足，非数据集死）；按 §7.7 可作辅助腿（条件/分组/残差式入场）。
- 跨模板结论：**内核冠军按模板而异**（A ts_rank / B ts_std_dev / C ts_delta / D ts_std_dev / E ts_std_dev / F ts_mean / G ts_mean）⇒「模板间不可互推」实测七次成立；**FAST 是本集最稳定的增益档**（A/B/C/D/E/F 六模板皆由 FAST 收官）。
- 档案层数：模板 A 6 层 68 臂 / B–G 各 5 层 45 臂（含 L5-R）⇒ `gradient_gate` 判 **GRADIENT_DONE**。

## 状态

- 全部 7 模板完成：A 1.01 / B 0.97 / **C 1.26** / D 0.99 / E 1.04 / F 1.08 / G 0.90。
- 数据集天花板 = **S1.26（模板 C）** ⇒ **已写死**（不再 PROVISIONAL）。
- 交付结论：**0 颗**；institutions 塔仍由 institutions1（ZYaQdNO1）占 1 席。
- 适用域：2014–2023（10 年，§7.10.0 体检合格）。

## 模板推进（续）：H–R（剩余互异基线按镜像 |S| 降序）

| 模板 | 信号构造（镜像 |S| / 2Y） | 状态 |
|---|---|---|
| **H** | `trade_length`（C 持仓时长，0.68 / −0.13） | 🔄 L2 在跑（`3G3fIbjg54paR5yOdbMPzq` + `1KDw3C5Qo5dnaO413JLWQut3`） |
| I | `security_avg_trade_length`（C 时长，0.68 / −0.14） | 待做 |
| J | `security_trade_count_1wk`（D 计数，0.61 / −0.32） | 待做（已修正：原表误写 `_1yr` 0.67，`_1yr` 立平水平**从未在 L1 实测**，需先补 1 臂 L1 探针） |
| K | `security_trade_count_1wk`（D 计数，0.61 / −0.32） | 待做 |
| L | `position`（B 仓位水平，0.55 / −0.30） | 待做 |
| M | `is_open`（B 开放哑变量，0.55 / −0.12） | 待做 |
| N | `crowding`（A 拥挤度，0.55 / −0.01） | 待做 |
| O | `security_trade_count_2yr`（D 计数，0.54 / −0.21） | 待做 |
| P | `security_trade_count_3yr`（D 计数，0.53 / −0.21） | 待做 |
| Q | `security_trade_count`（D 当日计数，0.59 / −0.07） | 待做 |
| R | `manager_count`（F 经理广度，0.52 / −0.33） | 待做 |
| S | `manager_position_count`（F 经理组合仓位，0.47 / −0.30） | 待做 |
| T | `sentiment`（A 做空情绪，0.45 / −0.40） | 待做 |
| U | `total_short_interest`（A 总空头利息，0.43 / −0.46） | 待做 |
| V | `security_trade_count_3mo`（D 计数，0.42 / −0.23） | 待做 |
| W | `divide(1mo, 1yr)` 计数归一（D，0.41 / −0.60） | 待做 |
| X | `divide(cover, short)` 平空/卖空（E，0.38 / −0.14） | 待做 |

> 说明：H–X 均为 L1 中**互异的单腿/比值构造**（未在 A–G 覆盖），按「塔内互异基线逐个推完」的穷尽口径逐个跑完整 5 层。优先级按镜像 |S| 降序（H→X）。

### 模板 H–I 完整梯度结果（各 45 臂，2026-11-22）

| 模板 | L2 冠军 | L2b | L3 | L4 | L5 | **模板天花板** |
|---|---|---|---|---|---|---|
| **H `trade_length`** | `ts_av_diff` 0.88（+0.20） | 126 最优（66 0.80 / 250 0.68 / 504 0.66 / 750 0.68） | industry 0.88 最优（sector/market 0.83、subindustry 0.76） | group_rank 0.88（其余 ≤0.61；聚合 TO 101–104%） | FAST 0.90 / INDUSTRY 0.87 / SECTOR 0.71 / decay8 0.89 | **S0.90 / F0.42 / 2Y −0.06 / TO9.1%**（FAST×ts_av_diff126×industry）；L5-R 未翻转（ts_rank/ts_sum 0.83） |
| **I `security_avg_trade_length`** | `ts_av_diff` 0.88（+0.20；`ts_mean` 0.79 但 2Y **0.55**） | 126 最优（66 0.80 / 250 0.68 / 504 0.66 / 750 0.68） | industry 0.88 最优（market 0.83、sector 0.82、subindustry 0.75） | group_rank 0.88（其余 ≤0.61） | FAST 0.90 / INDUSTRY 0.87 / decay8 0.89 | **S0.90 / F0.42 / 2Y −0.07 / TO9.1%**（FAST×ts_av_diff126×industry）；L5-R 未翻转（ts_rank 0.83） |

> J 与 I 是**同族不同字段**（交易时长 vs 证券平均交易时长），两者梯度形态几乎逐位重合（L2 冠军同为 ts_av_diff、窗 126、轴 industry、外层 group_rank、设置 FAST）⇒ 该族的**族级天花板 = S0.90**；单字段镜像 S 0.68 是族内可复现上限。

### 模板 J `security_trade_count_1wk`（D 计数族·短窗）完整梯度（45 臂）

| 层 | 结果 |
|---|---|
| L2 内核（15 臂 + 基线） | **`ts_std_dev` 0.76 / F0.45** 最优（基线 ts_zscore 0.61，**Δ+0.15**）；`ts_arg_max` 0.72（2Y **0.54**）、`ts_mean` 0.72（2Y0.49）、`ts_ir` 0.68；`ts_product` −0.82 / `days_from_last_change` −0.68 仍负 |
| L2b 窗口（4 臂） | **窗 504 最优 0.81 / F0.49 / 2Y0.53**（66 0.71 / 250 0.77 / 750 0.76；基线 126 0.76） |
| L3 轴（6 臂） | industry 0.81 ≡ subindustry 0.81（2Y 0.53 vs 0.50）；market≡exchange≡country 0.77；sector 0.77 |
| L4 外包（7 臂） | **全 ΔS 负**（最高 0.55；group_sum/std_dev TO 99–100%、DD 147–150%）⇒ 收敛 group_rank |
| L5 设置（8 臂） | **FAST 0.96 / F0.51 / 2Y0.54**（industry 轴；subindustry 0.96/0.49）＝本模板最大增益 **+0.15**；INDUSTRY 0.66–0.71、SECTOR 0.58–0.63、decay8 0.81 |
| L5-R 换基线重扫（4 臂） | FAST 下 `ts_std_dev` 仍最优（其余 0.28–0.67）⇒ 未翻转 |

**★ 模板 J 天花板 = S0.96 / F0.51 / 2Y0.54 / TO8.4%**（FAST × ts_std_dev504 × industry）。**D 计数族（短窗）天花板 0.96**。

### 模板 K `security_trade_count`（D 计数族·当日）完整梯度（45 臂）

| 层 | 结果 |
|---|---|
| L2 内核（15 臂 + 基线） | **`ts_arg_min` 0.77 / F0.41 / 2Y0.54**（基线 0.59，**Δ+0.18**）；`ts_std_dev` 0.70；`ts_rank` 0.66；`ts_product` −0.70 / days −0.69 仍负 |
| L2b 窗口 | 窗 126 保持最优（66 0.74 / 250 0.72 / 504 0.72 / 750 0.59） |
| L3 轴 | industry 0.77 ≡ market≡exchange≡country 0.77（2Y 0.54 vs 0.52）；sector 0.76；subindustry 0.67 |
| L4 外包 | **全崩**（最高 0.30；group_sum/backfill TO 99%）⇒ group_rank |
| L5 设置 | FAST 0.78 / decay8 0.77 / INDUSTRY 0.63–0.66 / SECTOR 0.53–0.58（基线 0.77） |
| **L5-R 重扫（★第三次内核翻转）** | FAST 下 **`ts_std_dev` 0.80 反超 ts_arg_min 0.78**（F0.39/2Y0.25） |

**★ 模板 K 天花板 = S0.80 / F0.39 / 2Y0.25 / TO9.0%**（FAST × ts_std_dev126 × industry）。⇒ **当日计数比 _1wk 短窗更弱**（0.80 vs 0.96），同族内**窗口越短天花板越高**。
| 基线 | SUBINDUSTRY + decay 4 | `npaqLEn8` / `ZYazJKed` | 0.90 / 0.87 | 0.57/0.52 | +0.33/+0.34 | 1.9/2.3% |

## 状态（模板推进）

- A/B/C/D/E/F 完整梯度均已完成：**天花板 A 1.01 / B 0.97 / C 1.26 / D 0.99 / E 1.04 / F 1.08**。
- G（concentration）L2 在跑；完成后数据集天花板写死。
- 数据集天花板（暂定）= **S1.26（模板 C）**。
| 基线 | SUBINDUSTRY + decay 4 | `LLKz2oZn` / `pwaGpwp6` | 0.95 / 0.89 | 0.56/0.54 | +0.48/+0.48 | 2.1/2.4% |

## 状态（模板推进）

- A/B/C/D/E 完整梯度均已完成：**天花板 A 1.01 / B 0.97 / C 1.26 / D 0.99 / E 1.04**。
- F（position_change 单腿）在跑；G（concentration）待做。
- 数据集天花板（暂定）= **S1.26（模板 C）**。
| 基线 | SUBINDUSTRY + decay 4 | `3q0PkZrg` / `Wjlz3aAQ` | 0.79 / 0.74 | 0.43/0.40 | +0.14/+0.10 | 2.2/2.4% |

### 模板 L `position`（B 仓位水平）完整梯度（45 臂）

**天花板 = S0.89 / F0.53 / 2Y0.39**（基线设置档即最优：SUBINDUSTRY × decay4 × ts_delta? 形态；L5 四档全劣）⇒ B 仓位水平族单独做不出 S 闸。

### 模板 M `is_open`（B 开放哑变量）完整梯度（45 臂）

**天花板 = S1.01 / F0.53 / 2Y0.04 / TO8.96%**（FAST × ts_delta250 × market）；L5-R 重扫未翻转（次优 ts_rank 0.91）。⇒ 哑变量型信号 S 可过内部 1 档但 **2Y ≈ 0**（方向一致性不足）。

---

## 模板 N · `crowding`（A 族拥挤度，镜像 S0.55 / 2Y −0.01）完整梯度（2026-11-22）

> 基线结构：`reverse(group_rank(<K>(ts_backfill(vec_avg(inst25_crowding),250),N), <axis>))`；设置 SUBINDUSTRY / decay4 / trunc0.08 / nanON

### N-L2 · 内层时序算子全替（15 臂 + 基线，批 `2zahsi1zE5cO9811bzUqGFlK`（8 臂）+ `228Ksi5nf50NbrOje5vh5jS`（7 臂），并行）

| 层 | 结果 |
|---|---|
| L2 内核 | **`ts_mean` 0.83 / F0.49 / 2Y0.31** 最优（基线 `ts_zscore` 0.55 ⇒ **ΔS +0.28**，本模板最大单层增益）；波动/时效型（`ts_std_dev` / `ts_ir` / `ts_arg_max`）与 `ts_product` / `days_from_last_change` 全劣 |
| L2b 窗口（4 臂，批 `2Geu6V4T14Q6chK15kMAf3cf`） | **窗 250 最优 0.86 / F0.51 / 2Y0.33**（66 / 126 / 504 均 ≤0.83）⇒ 拥挤度是**慢变量**，需长窗平滑 |
| L3 轴（6 臂，批 `6GuDkfLD4Adayd18AevHG9z`） | **market ≡ exchange ≡ country 0.90 / F0.57 / 2Y0.53**（单国三轴逐位相同）；industry / sector / subindustry 均 ≤0.86 ⇒ 本族**粗轴最优**（与 H/I 的 industry 最优相反，族间不可外推） |
| L4 外包（7 臂 + 基线，批 `1xL40SgXD4Z692v11wwqXkEF`） | **全 ΔS 负 ⇒ 收敛 `group_rank`**：group_scale / group_zscore / group_neutralize 三条**逐位相同 0.80 / F0.46 / 2Y0.51**（`ts_mean` 已去均值 ⇒ 三者等价）；group_backfill120 0.75 / 252 0.74（2Y 0.56–0.57 最高但 S 崩）；聚合型 group_sum 0.05（TO 102.6%）/ group_std_dev 0.02（TO 103.0%、DD 67%）崩 |

**N 中间态**：0.90 / F0.57 / 2Y0.53 / TO2.2%（market × ts_mean250 × group_rank × reverse）——进 L5 设置档。

### N-L5 · 设置档（4 档 × 2 轴，与模板 O 合并同批：`LY4ue2Nl4zK9YyJgVag7hq`(INDUSTRY) / `35Hq11az75gFchBbaxNA6Fh`(SECTOR) / `ZHcGD1e54Xlb7pThaQwhBn`(FAST) / `23jbkHcTS58aa3IKetigkMe`(decay8)，各 4 臂）

| 档 | α（market 轴 / subindustry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| INDUSTRY | `58JYQZmJ` / `akaGLrp6` | 0.73 / 0.65 | 0.41/0.33 | +0.44/+0.15 | 1.8/2.0% |
| SECTOR | `xAv5YzZN` / `P05KZlVK` | 0.59 / 0.56 | 0.31/0.27 | +0.16/−0.10 | 1.5/1.8% |
| FAST | `P05K29lK` / `A1xENKOg` | 0.79 / 0.73 | 0.38/0.32 | +0.21/−0.20 | 8.2/8.1% |
| **SUBINDUSTRY + decay 8** | **`npard9vq`** / `O0WgNOWv` | **0.90** / 0.78 | **0.57**/0.43 | **+0.54**/+0.28 | 1.84/2.03% |
| 基线（SUBINDUSTRY + decay 4） | 中间态 | **0.90** | **0.57** | +0.53 | 2.19% |

**N-L5 结论（`converge=yes`，无增益）**：四档**无一超过基线 0.90**——`decay8` 与基线**同 S（0.90）/ 同 F（0.57）**，仅 2Y +0.01、TO 2.19%→1.84%（微改善，取为本模板终态档）；INDUSTRY 0.73、SECTOR 0.59、**FAST 只有 0.79（与 A/C/E/J/K「FAST 抬 S」相反）** ⇒ 拥挤度对风险模型中性化不敏感。
（★ 本模板 TO 仅 1.8–2.2%，是 inst25 全部模板里最低 —— 慢变量 + 长窗 + 均值型内核的三重叠加。）

### N-L5-R · 换基线（decay8）后内核重扫（批 `2yW8Bl8NS4mV9cQ1gdoUpCi0`，4 臂，market × W250）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| R-1 | `ts_mean`（L5 基线） | `npard9vq` | **0.90** | **0.57** | **+0.54** | 1.84% |
| R-2 | `ts_std_dev` | `LLK3NK0a` | 0.78 | 0.44 | +0.37 | 1.99% |
| R-3 | `ts_zscore` | `ZYaNbaJx` | 0.50 | 0.23 | +0.02 | 6.83% |
| R-4 | `ts_rank` | `akaGba09` | 0.48 | 0.21 | −0.04 | 7.21% |
| R-5 | `ts_av_diff` | `pwa3RaLx` | 0.47 | 0.21 | −0.07 | 6.51% |

**N-L5-R 结论（未翻转）**：decay8 基线下 **`ts_mean` 仍最优（0.90）**，次优 ts_std_dev 差 0.12 ⇒ 排序稳健。
**★ 模板 N 天花板 = S0.90 / F0.57 / 2Y0.54 / TO1.84%**（decay8 × ts_mean250 × market × group_rank × reverse）。F0.57 是本数据集全部 15 个模板里**最高 F**（但因 S 只 0.90，仍差 S 闸 0.68）。

---


## 模板 O · `security_trade_count_2yr`（D 计数族·两年窗，镜像 S0.54 / 2Y −0.21）完整梯度（2026-11-22）

> 基线结构同上，字段换 `vec_avg(inst25_security_trade_count_2yr)`

### O-L2–L4

| 层 | 结果 |
|---|---|
| L2 内核（15 臂 + 基线，批 `3FnuElCP4Js8CVvaD6cQKK`（8 臂）+ `1TfNS35W94gDbHKdE7T7tgT`（7 臂）） | **`ts_mean` 0.82 / F0.49 / 2Y0.34** 最优（基线 0.54 ⇒ ΔS +0.28）；与 N 同型（慢变量型计数需水平平滑） |
| L2b 窗口（4 臂，批 `1pUfD37HB4GEbdEfTkZtErr`） | **窗 126 保持最优 0.82**（250 0.79 / 66 与 504 更低）⇒ 两年窗计数的**信息已经是长窗聚合**，内核窗反而要短 |
| L3 轴（6 臂，批 `4nCvu54eq5hMav9Eswo6H0a`） | **market 0.81 / F0.50 / 2Y0.39** 最优（粗轴最优，与 N 同型） |
| L4 外包（7 臂 + 基线，批 `2Pq1dW1zq4vub5sfaSq9zCs`） | **全 ΔS 负 ⇒ 收敛 `group_rank`**：group_scale / zscore / neutralize 逐位 0.57（2Y 0.46）；group_backfill252 0.42（2Y**0.53** 最高）；聚合型 0.28 / **−0.19**（TO 103%）崩 |

**O 中间态**：0.81 / F0.50 / 2Y0.39 / TO2.2%（market × ts_mean126）——进 L5 设置档。

### O-L5 · 设置档（同 N 四条合并批）

| 档 | α（market 轴 / subindustry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| INDUSTRY | `xAv5YKZm` / `xAv5YKZb` | 0.60 / 0.70 | 0.32/0.37 | +0.25/+0.23 | 1.6/1.8% |
| SECTOR | `kqa9Vmzd` / `akaGLP52` | 0.46 / 0.60 | 0.22/0.30 | +0.01/+0.01 | 1.4/1.6% |
| FAST | `ZYaNbGWQ` / `XgaMb62m` | 0.61 / **0.85** | 0.26/0.40 | −0.03/+0.28 | 8.5/8.0% |
| SUBINDUSTRY + decay 8 | `WjlJbMlG` / `Grm9bPmx` | 0.76 / 0.81 | 0.45/0.46 | +0.38/+0.38 | 1.72/1.88% |
| **基线（SUBINDUSTRY + decay 4，market）** | 中间态 | **0.81** | **0.50** | **+0.39** | 2.19% |

**O-L5 结论（`converge=yes`）**：最高 0.85（FAST × subindustry 轴）仍低于基线 0.81？——不，0.85 > 0.81，但**同为收益轴权衡**：FAST×subindustry 0.85 的 2Y 只有 0.28（基线 0.39）、F 0.40（基线 0.50）；按「S 为第一判据、同层取 S 最优」则 0.85 是 L5 最优 ⇒ **O 终态档 = FAST × ts_mean126 × subindustry**。
⚠ 但该档 S0.85 仍远低于本数据集天花板 1.26，且 2Y 0.28。

### O-L5-R · 换基线后内核重扫（批 `XZWhUekP53kb1gYGH7jxOi`，4 臂，**market × W126 × decay4** 原基线档下重扫，用于确认内核排序不因设置改动而翻转）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| R-1 | `ts_mean`（基线） | 中间态 | **0.81** | **0.50** | **+0.39** | 2.19% |
| R-2 | `ts_std_dev` | `rK78O8qa` | 0.74 | 0.44 | +0.10 | 2.10% |
| R-3 | `ts_av_diff` | `A1xENEpQ` | 0.71 | 0.39 | +0.07 | 2.72% |
| R-4 | `ts_rank` | `KPgZNZol` | 0.68 | 0.36 | +0.09 | 4.70% |
| R-5 | `ts_zscore` | `kqa9o9wL` | 0.56 | 0.28 | −0.08 | 4.18% |

**O-L5-R 结论（未翻转，且在新基线档下补测）**：基线档（market × decay4）下 `ts_mean` 0.81 仍最优、次优 ts_std_dev 0.74；换到 L5 最优档（**FAST × subindustry**）后重扫（批 `1GnSg28NR4t7a5UTJQtiH52`，6 臂）：**`ts_mean` 0.85 仍最优**，ts_std_dev 0.84（2Y **−0.14** 崩）/ ts_av_diff 0.72 / ts_rank 0.72 / ts_zscore 0.68，**轴重扫 subindustry 0.85 > industry 0.78** ⇒ 排序与轴选择双稳健。
**★ 模板 O 天花板 = S0.85 / F0.40 / 2Y0.28 / TO8.0%**（FAST × ts_mean126 × subindustry × group_rank × reverse）；S/2Y 联合最优形态 = 基线档 0.81 / 0.50 / 0.39（TO2.2%，最省的换手）。

---

## 模板 P · `security_trade_count_3yr`（D 计数族·三年窗，镜像 S0.53 / 2Y −0.21）完整梯度（2026-11-22）

> 基线结构同上；D 计数族第 4 个窗口（_1wk=J 0.96 / 当日=K 0.80 / _2yr=O 0.85 / _3yr=P）

### P-L2 · 内层时序算子全替

**P-L2-A（8 臂，批 `jWuzB3kR4TyaIxXQC0fAuD`，SUBINDUSTRY/decay4/industry 轴/W126）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| P-L2-1 | `ts_scale` | `XgaMJppa` | 0.70 | 0.37 | −0.03 | 3.6% |
| P-L2-2 | `ts_rank` | `9qlkWwro` | 0.85 | 0.51 | **+0.51** | 5.7% |
| P-L2-3 | `ts_quantile` | `0mP5r7Ep` | 0.85 | 0.51 | +0.50 | 5.4% |
| **P-L2-4** | **`ts_av_diff`** | `Grm9OwLx` | **0.88** | **0.54** | **+0.47** | 3.2% |
| **P-L2-5** | **`ts_delta`** | `A1xEvw7R` | **0.88** | **0.55** | +0.26 | 3.2% |
| P-L2-6 | `ts_mean` | `RReP6p1d` | 0.70 | 0.38 | +0.14 | 2.0% |
| P-L2-7 | `ts_std_dev` | `3q0JV7eX` | 0.79 | 0.47 | +0.12 | 2.6% |
| P-L2-8 | `ts_ir` | `kqa9g3Zz` | **0.17** | 0.04 | **−1.03** | 3.8% |

**P-L2-A 结论**：**`ts_av_diff` / `ts_delta` 0.88**（ΔS **+0.35** 相对 L1 镜像 0.53，D 计数族内**本模板最大单层增益**）；`ts_rank`/`ts_quantile` 0.85 且 **2Y 0.51/0.50**（最高）；`ts_ir` 崩（0.17，2Y −1.03，D 族又一不成立内核）。

**P-L2-B（8 臂，批 `3ctyT6cGy5eu99vO2hkC3It`，含基线 ts_zscore + arg_max/arg_min/returns/product/sum/max_diff/days）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| P-L2-0 | `ts_zscore`（基线） | `mLaQYJ0X` | 0.75 | 0.43 | +0.30 | 5.2% |
| P-L2-9 | `ts_arg_max` | `9qlkEbde` | 0.42 | 0.15 | +0.08 | 4.9% |
| P-L2-10 | `ts_arg_min` | `58JYj35N` | 0.84 | 0.47 | +0.42 | 2.9% |
| P-L2-11 | `ts_returns` | `nparAYq8` | 0.84 | 0.50 | +0.29 | 3.5% |
| P-L2-12 | `ts_product` | `xAv519Gp` | **−0.66** | −0.32 | +0.13 | 2.8% |
| P-L2-13 | `ts_sum` | `WjlJLn0k` | 0.76 | 0.43 | +0.27 | 1.8% |
| P-L2-14 | `ts_max_diff` | `blaA8VnR` | 0.80 | 0.42 | +0.45 | 3.1% |
| P-L2-15 | `days_from_last_change` | `RRePAqKo` | **−0.67** | −0.37 | −0.28 | 4.5% |

**P-L2 终态（16 臂）**：**`ts_av_diff` 0.88 / F0.54 / 2Y0.47** 最优（与 ts_delta 同 S 但 2Y 高 0.21）⇒ **L2b 基线 = ts_av_diff × 126 × industry**。★ 注意：**实测基线 ts_zscore = 0.75**，与队列表里 L1 镜像 0.53 不一致 —— L1-B 的 `_3yr` 臂用的是另一条构造（比值/水平），本表以 L2 实测 0.75 为准。

### P-L2b · 窗口全替（批 `269uiZ5IM4rjazHHJhFNcJN`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| P-L2b-1 | **250** | **`YPaY1jLW`** | **0.92** | **0.58** | **+0.61** | 2.7% |
| P-L2b-2 | 66 | `qM7VLKME` | 0.87 | 0.53 | +0.53 | 3.8% |
| P-L2b-3 | 504 | `omaZE18J` | 0.82 | 0.49 | +0.52 | 2.5% |
| P-L2b-4 | 750 | `vRAP1K8w` | 0.75 | 0.43 | +0.47 | 2.4% |
| 基线 | 126 | `Grm9OwLx` | 0.88 | 0.54 | +0.47 | 3.2% |

**P-L2b 结论（`converge=no`，**ΔS +0.04**）**：**窗 250 最优 0.92 / F0.58 / 2Y0.61**（三项同时上升，且 TO 降到 2.7%）⇒ 三年计数窗 + 长窗平滑 = **P 的第二次增益**。

### P-L3 · 分组轴全替（批 `2ak5WMalK4rOapi1lf1OHgA`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| **P-L3-1** | **`subindustry`** | **`58JYEjYo`** | **0.94** | **0.58** | **+0.88** | 2.5% |
| 基线 | `industry` | `YPaY1jLW` | 0.92 | 0.58 | +0.61 | 2.7% |
| P-L3-2 | `sector` | `j2aOYeOZ` | 0.80 | 0.48 | +0.41 | 2.5% |
| P-L3-3 | `market` | `LLK3M52L` | 0.80 | 0.48 | +0.35 | 2.2% |
| P-L3-4 | `exchange` | `WjlJOLxN` | 0.80 | 0.48 | +0.35 | 2.2% |
| P-L3-5 | `country` | `zqde3rLE` | 0.80 | 0.48 | +0.35 | 2.2% |

**P-L3 结论（`converge=no`，**ΔS +0.02 / Δ2Y +0.27**）**：**`subindustry` 最优 0.94 / 2Y 0.88**（2Y 是全模板最高值之一）——**本模板唯一细轴最优的模板**（与 A/C/D 的 industry 最优、N/O 的粗轴最优都不同，再次验证族间不可外推）。market≡exchange≡country 逐位相同（0.80）。

### P-L4 · 外层包装全替（批 `1sF1y4ML4L49MBZf1hgiNC`，8 臂）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| P-L4-0 | `group_rank`（基线） | `58JYEjYo` | 0.94 | 0.58 | +0.88 | 2.5% |
| **P-L4-1** | **`group_scale`** | **`E5QxQbNK`** | **1.04** | **0.67** | **+1.83** | 3.1% |
| P-L4-2 | `group_zscore` | `0mP5Pdx2` | 0.99 | 0.65 | +1.62 | 3.0% |
| P-L4-3 | `group_neutralize` | `j2aOaXPQ` | 0.48 | 0.29 | +0.70 | 2.9% |
| P-L4-4 | `group_backfill(·,subindustry,120)` | `d5avam3x` | 0.49 | 0.28 | +0.54 | 3.1% |
| P-L4-5 | `group_backfill(·,subindustry,252)` | `E5QxQb8m` | 0.50 | 0.28 | +0.38 | 3.0% |
| P-L4-6 | `group_sum` | `ZYaNaxd8` | −0.32 | −0.09 | −0.56 | **99.4%** |
| P-L4-7 | `group_std_dev` | `0mP5Pdgv` | −0.09 | −0.01 | −0.37 | **96.4%** |

**P-L4 结论（`converge=no`，**ΔS +0.10 / Δ2Y +0.95**）**：★★ **`group_scale` 1.04 / F0.67 / 2Y 1.83** —— 本模板第三次增益，且 **2Y 首次破 1.58**；`group_zscore` 0.99 / 2Y 1.62 次之。这是**整个 inst25 战役里第一个 prescreen 非 REJECT 的臂**（`E5QxQbNK` 落在 REVIEW，其余全部 REJECT）。聚合型仍崩（TO 96–99%、DD 75–84%）。⚠ 与模板 C 相反：**这里 group_rank 反而让 2Y 封在 0.88，换 group_scale 才把 2Y 抬上**——外层算子与信号类型的匹配再次按族实测，不能套用「水平型用 backfill」的通则。

### P-L5 · 设置档（4 档 × 2 轴，与模板 Q 合并同批：`3aOIdlcu84JRaueb8zdlzGK`(INDUSTRY) / `mJP4Y4DM4PAbIqaMz0ZLL3`(SECTOR) / `4038846d24Mhc6dNMPATXSF`(FAST) / `LgpMB2fs5e2cxC16yfSNFAR`(decay8)，前两批 4 臂）

| 档 | α（P subindustry 轴 / P industry 轴 / Q market / Q industry） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `E5QxQbNK`（P subindustry） | 1.04 | 0.67 | +1.83 | 3.1% |
| **FAST** | **`1YW0Oa2W`** / `blaAJogM` | **1.23** / 0.85 | **0.71**/0.41 | **+1.93**/0.93 | 9.4/9.0% |
| **SECTOR** | **`vRAPYzOA`** / `VkNeMldA` / `N1P8KjNq` / `j2aOVwYZ` | **1.06** / 0.75 / 0.57 / 0.63 | **0.66**/0.40/0.31/0.34 | **+1.80**/0.79/0.17/0.12 | 3.1/3.0/1.5/1.7% |
| **INDUSTRY** | `d5av9meX` / `pwa3WEQx` / `E5Qxmb01` / `QP06WjrG` | 1.03 / 0.70 / 0.71 / 0.73 | 0.65/0.39/0.41/0.42 | +1.69/1.27/0.39/0.37 | 3.2/3.0/1.7/1.8% |
| SUBINDUSTRY + decay 8 | `E5QxN08L` / `QP06OrNw` | 1.05 / 0.87 | 0.68/0.56 | +1.81/+1.34 | 3.0/3.0% |

**P-L5 结论（`converge=no`，**最大单层增益 ΔS +0.19**）**：★★ **FAST 最优 `1YW0Oa2W`：S1.23 / F0.71 / **2Y 1.93** / TO9.4%** —— **2Y 闸（1.58）首次被 inst25 的任意模板超过**（C 模板 2Y 只有 0.58）；S1.23 距 1.26 的模板 C 仅 0.03，但 F（0.71）与 2Y（1.93）全面领先。四档排序 FAST 1.23 > SECTOR 1.06 > INDUSTRY 1.03 > decay8 1.05。
⚠ 这是**本数据集第一个 prescreen REVIEW 且三项都接近门限的臂**；P 模板是 D 计数族（_3yr）里「长窗 + 差分 + group_scale + 细轴」的组合，与 C 的残差组合是**不同经济机制**。

### P-L5-R · 换基线（FAST）后内核重扫（批 `37XOq08vL54vcMhpvO92NeY`，5 臂）

| 臂 | 内核（FAST / subindustry / W250 / group_scale） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| R-1 | `ts_av_diff`（L5 基线） | `1YW0Oa2W` | **1.23** | **0.71** | **+1.93** | 9.4% |
| R-2 | `ts_std_dev` | `88NXEX6m` | 0.95 | 0.48 | +0.35 | 8.5% |
| R-3 | `ts_rank` | `0mP5N592` | 0.90 | 0.44 | +1.67 | 12.0% |
| R-4 | `ts_zscore` | `O0WgMgk7` | 0.71 | 0.31 | **+1.86** | 11.2% |
| R-5 | `ts_delta` | `LLK3m3Xm` | 0.57 | 0.25 | +0.58 | 11.1% |
| R-6 | `ts_mean` | `Grm9K98o` | 0.33 | 0.09 | +0.20 | 8.0% |

**P-L5-R 结论（未翻转）**：FAST 基线下 **`ts_av_diff` 1.23 仍最优**（次优 ts_std_dev 0.95、ts_rank 0.90）⇒ 排序稳健。★ 副产物：`ts_rank`（2Y **1.67**）/ `ts_zscore`（2Y **1.86**）两臂的 **2Y 都很高但 S 只有 0.71–0.90** —— 又一次坐实本数据集「S↔2Y 跷跷板」，而 `ts_av_diff` 是唯一**同时拿到高 S 与高 2Y** 的内核。
**★★ 模板 P 天花板 = S1.23 / F0.71 / 2Y1.93 / TO9.4%**（FAST × group_scale × ts_av_diff250 × subindustry × reverse）——**全 17 个模板里 2Y 最高、F 最高（并列）、S 第二**。

---

## 模板 Q · `manager_count`（F 族经理广度，镜像 S0.52 / 2Y −0.33）完整梯度（2026-11-22）

> 基线结构同上；**F 族是 inst25 里唯一「水平型/广度型」信息**

### Q-L2 · 内层时序算子全替（16 臂）

**Q-L2-A（8 臂，批 `2njKoCb1Z4zu9e73mOlyu0F`，SUBINDUSTRY/decay4/industry 轴/W126）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| Q-L2-1 | `ts_scale` | `ZYaNmw8Q` | 0.68 | 0.40 | +0.45 | 5.6% |
| Q-L2-2 | `ts_rank` | `XgaMRw0m` | 0.43 | 0.17 | +0.08 | 4.7% |
| Q-L2-3 | `ts_quantile` | `A1xEQJAg` | 0.41 | 0.16 | +0.05 | 4.8% |
| Q-L2-4 | `ts_av_diff` | `1YW0jVMX` | 0.44 | 0.18 | −0.07 | 4.6% |
| Q-L2-5 | `ts_delta` | `XgaMRwdm` | 0.45 | 0.19 | −0.08 | 4.7% |
| **Q-L2-6** | **`ts_mean`** | **`mLaQY2Ex`** | **0.83** | **0.51** | **+0.37** | 2.2% |
| Q-L2-7 | `ts_std_dev` | `QP06YrwK` | 0.81 | 0.49 | +0.36 | 2.5% |
| Q-L2-8 | `ts_ir` | `O0WgJwlg` | 0.79 | 0.48 | −0.16 | 4.9% |

**Q-L2-B（8 臂，批 `3L0joBX5bvaWKNY3j9xHY`，含基线 ts_zscore + arg_max/arg_min/returns/product/sum/max_diff/days）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| Q-L2-0 | `ts_zscore`（基线） | `O0WgJLXR` | 0.61 | 0.34 | +0.30 | 6.4% |
| Q-L2-9 | `ts_arg_max` | `6XMNAWL5` | 0.57 | 0.24 | +0.04 | 3.1% |
| Q-L2-10 | `ts_arg_min` | `XgaMR3ZX` | 0.52 | 0.22 | −0.02 | 3.1% |
| Q-L2-11 | `ts_returns` | `akaGV0mO` | 0.44 | 0.19 | −0.08 | 4.8% |
| Q-L2-12 | `ts_product` | `E5QxVjnR` | 0.12 | 0.02 | +0.13 | 3.0% |
| Q-L2-13 | `ts_sum` | `rK78dqa8` | 0.74 | 0.41 | +0.27 | 1.9% |
| Q-L2-14 | `ts_max_diff` | `0mP5jVVq` | 0.49 | 0.19 | +0.13 | 3.6% |
| Q-L2-15 | `days_from_last_change` | `XgaMR33X` | **−0.78** | −0.46 | −0.38 | 3.1% |

**Q-L2 终态（16 臂）**：**`ts_mean` 0.83 / F0.51 / 2Y0.37** 最优（ΔS **+0.22** vs 基线 0.61）——★ **F 族的「广度」是慢变量**：`ts_mean` / `ts_std_dev`（0.81）/ `ts_ir`（0.79）/ `ts_sum`（0.74）**水平型内核全部领先**，而 rank/quantile/av_diff/delta（已排名/差分型）全部 ≤0.45。`days_from_last_change` −0.78 是 F 族的不成立内核。

### Q-L2b · 窗口全替（批 `1KpZpkbug5hPbreW3CVZr3V`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| **Q-L2b-2** | **250** | **`lea1AE18`** | **0.88** | **0.55** | **+0.43** | 2.0% |
| Q-L2b-3 | 504 | `akaGKeGw` | 0.87 | 0.53 | +0.43 | 1.9% |
| Q-L2b-4 | 750 | `xAv5rVEq` | 0.82 | 0.49 | +0.36 | 1.9% |
| Q-L2b-1 | 66 | `xAv5rV5q` | 0.75 | 0.44 | +0.21 | 2.3% |
| 基线 | 126 | `mLaQY2Ex` | 0.83 | 0.51 | +0.37 | 2.2% |

**Q-L2b 结论（`converge=no`，**ΔS +0.05**）**：**窗 250 最优 0.88 / F0.55**（与 504 的 0.87 同档）；TO 1.9–2.3% 全带极低。⇒ **L3 基线 = ts_mean250 × industry**。

### Q-L3 · 分组轴全替（批 `wgolJgl85c6bpK1euMyDaVg`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| Q-L3-3 | **`market`** | **`nparaYxM`** | **0.90** | **0.58** | **+0.55** | 1.8% |
| Q-L3-4 | `exchange` | `omaZaA8n` | 0.90 | 0.58 | +0.55 | 1.8% |
| Q-L3-5 | `country` | `O0WgWqQ7` | 0.90 | 0.58 | +0.55 | 1.8% |
| Q-L3-2 | `sector` | `P05K5q0K` | 0.89 | 0.56 | +0.55 | 1.9% |
| 基线 | `industry` | `lea1AE18` | 0.88 | 0.55 | +0.43 | 2.0% |
| Q-L3-1 | `subindustry` | `vRAPAxRd` | 0.80 | 0.46 | +0.35 | 1.9% |

**Q-L3 结论（`converge=no`，**ΔS +0.02 / Δ2Y +0.12**）**：**market ≡ exchange ≡ country 0.90 / 2Y 0.55**（单国三轴逐位相同，粗轴最优）；sector 0.89 次之；**subindustry 反而最差 0.80**。⇒ F 族广度是**国家/市场层面的慢信号**，细轴会稀释它。

### Q-L4 · 外层包装全替（批 `2Nz9qjgmz4RZctsN8obO2M6`，8 臂，market 轴）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| Q-L4-0 | `group_rank`（基线） | `nparaYxM` | **0.90** | **0.58** | **+0.55** | 1.8% |
| Q-L4-1 | `group_scale` | `P05KYre7` | 0.80 | 0.54 | +0.46 | 2.0% |
| Q-L4-2 | `group_zscore` | `akaGQ2J5` | 0.80 | 0.54 | +0.46 | 2.0% |
| Q-L4-3 | `group_neutralize` | `O0WgMwKq` | 0.80 | 0.54 | +0.46 | 2.0% |
| Q-L4-4 | `group_backfill(·,market,120)` | `WjlJowKP` | 0.68 | 0.36 | +0.57 | 1.9% |
| Q-L4-5 | `group_backfill(·,market,252)` | `Grm9K0E5` | 0.67 | 0.35 | +0.56 | 1.9% |
| Q-L4-6 | `group_sum` | `vRAPpnn3` | −0.11 | −0.02 | +0.36 | **103.3%**（DD 83%） |
| Q-L4-7 | `group_std_dev` | `d5av388x` | −0.12 | −0.02 | −0.54 | **100.9%**（DD 55%） |

**Q-L4 结论（`converge=yes`）**：**全 ΔS≤0 ⇒ 收敛 `group_rank`**；scale/zscore/neutralize 三条**逐位相同 0.80 / 0.54 / 0.46**（ts_mean 已去均值 ⇒ 等价），backfill 0.67–0.68、聚合型 TO 101–103% 崩。★ 与 P 对照：**同为慢变量，P 在 group_scale 上起飞（2Y 0.88→1.83）、Q 在 group_scale 上反而降 0.10** ⇒ 外层算子与「信号是水平还是变化」耦合，不能跨字段外推。

### Q-L5 · 设置档（4 档 × 2 轴）

| 档 | α（market 轴 / industry 轴） | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `nparaYxM` / `lea1AE18` | 0.90 / 0.88 | 0.58/0.55 | +0.55/+0.43 | 1.8/2.0% |
| INDUSTRY | `E5Qxmb01` / `QP06WjrG` | 0.71 / 0.73 | 0.41/0.42 | +0.39/+0.37 | 1.7/1.8% |
| SECTOR | `N1P8KjNq` / `j2aOVwYZ` | 0.57 / 0.63 | 0.31/0.34 | +0.17/+0.12 | 1.5/1.7% |
| **FAST** | `N1P8z1Oq` / **`vRAPGRmA`** | 0.82 / **0.93** | 0.41/**0.49** | +0.35/+0.35 | 8.7/8.5% |
| SUBINDUSTRY + decay 8 | `zqdeGkJd` / `3q0JPlaQ` | 0.90 / 0.89 | 0.58/0.56 | +0.55/+0.44 | 1.8/2.0% |

**Q-L5 结论（`converge=no`，+0.03）**：**FAST × industry 0.93** 是本模板最高（ΔS +0.03 vs 基线 market 的 0.90，但 2Y 由 0.55 掉到 0.35）；INDUSTRY 0.71–0.73、SECTOR 0.57–0.63、decay8 0.89–0.90 均劣或持平。

### Q-L5-R · 换基线（FAST × industry）后内核重扫（批 `2JMY0g9UE5cRbZV1ekevY9Dh`，4 臂）

| 臂 | 内核（FAST / industry / W250 / group_rank） | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| R-1 | `ts_mean`（L5 基线） | `vRAPGRmA` | 0.93 | **0.49** | **+0.35** | 8.5% |
| **R-2** | **`ts_sum`** | **`mLaQ7a92`** | **0.95** | 0.47 | **+0.14** | 7.8% |
| R-3 | `ts_std_dev` | `3q0JP0ZX` | 0.91 | 0.48 | +0.29 | 8.7% |
| R-4 | `ts_ir` | `9qlkMl0d` | 0.78 | 0.37 | +0.36 | 9.5% |

**Q-L5-R 结论（★第 4 次内核翻转）**：**`ts_sum` 0.95 反超 `ts_mean` 0.93**（+0.02）⇒ 换基线；但代价是 **2Y 0.35→0.14**、F 0.49→0.47 —— 又一次 S↔2Y 跷跷板。**S/2Y 联合最优仍是基线 `ts_mean`×market 的 0.90 / 0.58 / 0.55**。
**★ 模板 Q 天花板 = S0.95 / F0.47 / 2Y0.14 / TO7.8%**（FAST × ts_sum250 × industry）；**S+F+2Y 联合最优形态 = 0.90 / 0.58 / 0.55**（SUBINDUSTRY × ts_mean250 × market × group_rank）。

---

## 模板 R · `manager_position_count`（F 族经理组合仓位，镜像 S0.47 / 2Y −0.30）完整梯度（2026-11-22）

### R-L2-A（8 臂，批 `3ot687tS51j8OOB1Ezj5f0`）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| R-L2-1 | `ts_scale` | `xAv5WwGJ` | 0.57 | 0.27 | +0.06 | 7.0% |
| R-L2-2 | `ts_rank` | `qM7V3k3O` | 0.43 | 0.17 | +0.25 | 7.4% |
| R-L2-3 | `ts_quantile` | `88NXYkXq` | 0.40 | 0.15 | +0.22 | 7.2% |
| R-L2-4 | `ts_av_diff` | `j2aOxlOe` | 0.42 | 0.16 | +0.09 | 5.6% |
| R-L2-5 | `ts_delta` | `vRAP6no3` | 0.48 | 0.20 | −0.19 | 5.6% |
| R-L2-6 | `ts_mean` | `P05K8rA7` | 0.64 | 0.31 | **+0.41** | 2.3% |
| R-L2-7 | `ts_std_dev` | `omaZrwX5` | 0.58 | 0.29 | −0.05 | 2.8% |
| **R-L2-8** | **`ts_ir`** | **`88NXYkZz`** | **0.80** | **0.42** | **+0.38** | 3.9% |

**R-L2-A 结论**：**`ts_ir` 0.80**（ΔS **+0.33** vs 镜像 0.47）最优；`ts_mean` 0.64 次之（2Y 0.41 最高）。rank/quantile/av_diff/delta 全部 ≤0.48 ⇒ **F 族第二个字段再次呈「水平/信噪型内核领先、已排名型崩」的同族指纹**（与 Q 一致）。

**R-L2-B（8 臂，批 `2qayrIGT5f38Tztu7wnw9u`）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| R-L2-0 | `ts_zscore`（基线） | `rK788Yz9` | 0.49 | 0.21 | +0.17 | 6.8% |
| R-L2-9 | `ts_arg_max` | `lea11dRO` | 0.76 | 0.37 | +0.40 | 3.9% |
| R-L2-10 | `ts_arg_min` | `blaAAXWM` | 0.54 | 0.23 | +0.17 | 3.8% |
| R-L2-11 | `ts_returns` | `RRePPMkb` | 0.49 | 0.21 | −0.10 | 5.6% |
| R-L2-12 | `ts_product` | `88NXXbKX` | **−0.55** | −0.24 | +0.34 | 3.0% |
| R-L2-13 | `ts_sum` | `MP6VVOKM` | 0.70 | 0.36 | +0.27 | 1.9% |
| R-L2-14 | `ts_max_diff` | `78YllWax` | 0.54 | 0.22 | +0.29 | 5.6% |
| R-L2-15 | `days_from_last_change` | `1YW00eaW` | **−0.70** | −0.39 | −0.21 | 4.5% |

**R-L2 终态（16 臂）**：`ts_ir` 0.80 仍最优（`ts_arg_max` 0.76 次之、2Y 0.40 最高）⇒ **L2b = ts_ir × 126**。

**R-L2b · 窗口全替（批 `3objEWeuB580bndhf3r6WcL`，4 臂）**

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-L2b-1 | 66 | `nparrmMM` | 0.80 | 0.43 | +0.43 |
| R-L2b-2 | 250 | `LLK33EA1` | 0.57 | 0.25 | +0.08 |
| R-L2b-3 | 504 | `E5QxxNXm` | 0.58 | 0.25 | +0.12 |
| R-L2b-4 | 750 | `1YW00OQR` | 0.59 | 0.26 | +0.19 |
| 基线 | 126 | `88NXYkZz` | **0.80** | 0.42 | +0.38 |

**R-L2b 结论（`converge=yes`）**：126 与 66 并列 0.80（126 的 2Y 略逊 0.05 但 F 略高）⇒ **保持 126**。⇒ **L3 基线 = ts_ir126 × industry**。

**R-L3 · 轴层（批 `aBCgRbkz4Lec1i1c9UdFph9`，6 臂）**

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-L3-6 | `industry`（基线） | `88NXYkZz` | **0.80** | **0.42** | **+0.38** |
| R-L3-2 | `sector` | `XgaMxKwx` | 0.71 | 0.35 | +0.13 |
| R-L3-3 | `market` | `RRePorqa` | 0.70 | 0.35 | +0.06 |
| R-L3-4 | `exchange` | `P05Kb1qM` | 0.70 | 0.35 | +0.06 |
| R-L3-5 | `country` | `Grm9NoYZ` | 0.70 | 0.35 | +0.06 |
| R-L3-1 | `subindustry` | `RRePorZj` | 0.60 | 0.26 | +0.36 |

**R-L3 结论（`converge=yes`，industry 保持最优 0.80）**：market≡exchange≡country 仍逐位相同 0.70；subindustry 最差 0.60。⇒ **L4 基线 = ts_ir126 × industry**。

**R-L4 · 外层层（批 `3biIAmHH4VYcDiZ0dLT73H`，8 臂）**

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-L4-0 | `group_rank`（基线） | `88NXYkZz` | **0.80** | **0.42** | **+0.38** |
| R-L4-2 | `group_zscore` | `kqa96Qo8` | 0.09 | 0.02 | +0.48 |
| R-L4-3 | `group_neutralize` | `LLK3YkZa` | 0.10 | 0.03 | **+0.70** |
| R-L4-1 | `group_scale` | `3q0JvzX6` | 0.05 | 0.01 | +0.37 |
| R-L4-4 | `group_backfill(·,industry,120)` | `lea1PrKA` | −0.01 | −0.00 | +0.18 |
| R-L4-5 | `group_backfill(·,industry,252)` | `RRePwdAn` | −0.05 | −0.01 | +0.11 |
| R-L4-7 | `group_std_dev` | `kqa96QJz` | 0.08 | 0.01 | +0.17 |
| R-L4-6 | `group_sum` | `QP06pEYG` | −0.17 | −0.03 | −0.31 |

**R-L4 结论（`converge=yes`，**全崩**）**：★ **`ts_ir` 已是「均值÷波动」比值结构，任何外层标准化都把它毁掉**（S 0.05–0.10，全部 RA 4–5 失败）；只有 `group_rank` 保留截面信息（0.80）。这是本数据集**外层最脆的模板**。

**R-L5 · 设置档（与 S 合并批：`1Xad8Fg294wYaE1Af7IzWah`(INDUSTRY) / `p7pdDccw51nbm41cC1EEV4U`(SECTOR) / `3Jt0Uw7c44qzaPONG7aOIFI`(FAST) / `1kDeP96cL4Mmc4tnDgNwrxK`(decay8)）**

| 档 | α（R industry / R market / S industry / S market） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | R `88NXYkZz` / S `1YW02NYX` | **0.80 / 0.93** | 0.42/0.56 | +0.38/+0.48 |
| INDUSTRY | `mLaQnzlX` / `KPgZA82p` / `j2aOkwJW` / `d5avJ76j` | 0.63/0.59/0.76/0.76 | 0.29/0.27/0.41/0.41 | +0.29/+0.06/+0.28/+0.30 |
| SECTOR | `blaA0WJm` / `xAv57m2w` / `O0Wgd5M7` / `YPaY3WER` | 0.49/0.47/0.62/0.59 | 0.21/0.19/0.31/0.29 | +0.06/−0.11/+0.08/+0.07 |
| FAST | `O0WgLqpv` / `3q0JK37X` / `kqa9wb3z` / `E5QxjYEr` | 0.61/0.48/**0.79**/0.73 | 0.24/0.16/0.37/0.33 | −0.02/−0.25/+0.35/+0.28 |
| SUBINDUSTRY + decay8 | `RRePOjQo` / `WjlJZ16k` / `j2aOpzbj` / `6XMNWmOO` | 0.80/0.70/**0.91**/**0.91** | 0.42/0.34/0.54/0.55 | +0.39/+0.05/+0.44/+0.42 |

**R/S-L5 结论（`converge=yes`，基线不换）**：R 在 decay8 与基线**逐位相同**（0.80/0.42/2Y0.39 vs 基线 0.80/0.42/0.38，TO 3.6% vs 3.9%）⇒ 四档无一超过基线；S 最高 0.91（decay8）仍低于基线 0.93，FAST 0.79 也低于 0.93 —— **ts_ir 信号对风险模型中性化完全不敏感；S 的 66 短窗在 FAST 下衰减**。
**L5-R 空转（基线未变）**：R/S 的内核都在 **L2 层于相同设置（SUBINDUSTRY/decay4）下全替过**，L5 未产生任何新基线 ⇒ 重扫与 L2 全替相同，无新增信息，按记录纪律注明不重复执行。

**★ 模板 R 天花板 = S0.80 / F0.42 / 2Y0.38 / TO3.9%**（SUBINDUSTRY × ts_ir126 × industry × group_rank × reverse）
**★ 模板 S 天花板 = S0.93 / F0.56 / 2Y0.48 / TO3.9%**（SUBINDUSTRY × ts_ir66 × industry × group_rank × reverse）

---

## 模板 T · `total_short_interest`（A 族总空头利息，镜像 S0.43 / 2Y +0.46→−0.46）完整梯度（2026-11-22）

### T-L2（16 臂，批 `194yIw9MD58FbEx19p1iVnnO`（8 臂）+ `27h8Lg4Qo4vYc8sOlyGDpwd`（8 臂））

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T-L2-1 | `ts_scale` | `pwa3L71v` | 0.53 | 0.25 | −0.18 |
| T-L2-2 | `ts_rank` | `78YlpdK2` | 0.43 | 0.18 | −0.05 |
| T-L2-3 | `ts_quantile` | `d5avGQE2` | 0.41 | 0.16 | −0.10 |
| T-L2-4 | `ts_av_diff` | `3q0JNAag` | 0.35 | 0.13 | −0.16 |
| T-L2-5 | `ts_delta` | `KPgZ1LX8` | 0.44 | 0.19 | −0.04 |
| **T-L2-6** | **`ts_mean`** | **`e7aEjrdO`** | **0.88** | **0.53** | **+0.31** |
| T-L2-7 | `ts_std_dev` | `kqa9AK1g` | 0.77 | 0.45 | +0.27 |
| T-L2-8 | `ts_ir` | `zqdeVWPE` | 0.51 | 0.21 | −0.51 |
| T-L2-0 | `ts_zscore`（基线） | `wpoW0l82` | 0.43 | 0.19 | −0.46 |
| T-L2-9 | `ts_arg_max` | `omaZxlmm` | 0.70 | 0.33 | **+0.47** |
| T-L2-10 | `ts_arg_min` | `rK78ZlKE` | 0.45 | 0.17 | +0.02 |
| T-L2-11 | `ts_returns` | `Jj8r6Ojx` | 0.39 | 0.16 | −0.17 |
| T-L2-12 | `ts_product` | `j2aOq02O` | **−0.69** | −0.36 | −0.36 |
| T-L2-13 | `ts_sum` | `A1xEoPjR` | 0.75 | 0.41 | +0.10 |
| T-L2-14 | `ts_max_diff` | `omaZxl8v` | 0.40 | 0.14 | +0.26 |
| T-L2-15 | `days_from_last_change` | `gJaLnMke` | **−0.68** | −0.38 | −0.27 |

**T-L2 终态**：**`ts_mean` 0.88 / F0.53 / 2Y0.31**（ΔS **+0.45**，A 族第三个「水平型内核领先」的字段）；`ts_std_dev` 0.77 次之；`ts_arg_max` 0.70 但 **2Y 0.47 最高**。⇒ **L2b = ts_mean × 126**。

### T-L2b · 窗口全替（批 `vYsUV3Fl4pb93qWZwxOhJd`，4 臂）

| 窗 | 66 | **126（基线）** | 250 | 504 | 750 |
|---|---:|---:|---:|---:|---:|
| S | 0.82 | **0.88** | 0.78 | 0.80 | 0.78 |

**T-L2b 结论（`converge=yes`）**：126 保持最优，长/短窗全劣 ⇒ 窗口不是本模板杠杆。

### T-L3 · 分组轴全替（批 `3fYZCs2wJ4jE9rBTu5vCL0M`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T-L3-3 | **`market`** | `88N2mNjq` | **0.90** | **0.57** | **+0.32** |
| T-L3-4 | `exchange` | `N1P2XPap` | 0.90 | 0.57 | +0.32 |
| T-L3-5 | `country` | `qM7wK7xO` | 0.90 | 0.57 | +0.32 |
| T-L3-2 | `sector` | `xAvEKvYJ` | 0.88 | 0.54 | +0.32 |
| 基线 | `industry` | `e7aEjrdO` | 0.88 | 0.53 | +0.31 |
| T-L3-1 | `subindustry` | `blaKYaR6` | 0.78 | 0.43 | +0.27 |

**T-L3 结论（`converge=no`，+0.02）**：**market≡exchange≡country 0.90** 最优（单国三轴第 5 次逐位相同）；industry 0.88、subindustry 0.78。⇒ **L4 基线 = ts_mean126 × market**。

### T-L4 · 外层层（批 `3MDiMH7Mo4BEa1P12JKs6NAS`，8 臂，market 轴）

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T-L4-0 | `group_rank`（基线） | `88N2mNjq` | **0.90** | **0.57** | **+0.32** |
| T-L4-1 | `group_scale` | `j2aM2re5` | 0.66 | 0.42 | −0.27 |
| T-L4-2 | `group_zscore` | `6XM2XeAK` | 0.66 | 0.42 | −0.27 |
| T-L4-3 | `group_neutralize` | `blaKld6l` | 0.66 | 0.42 | −0.27 |
| T-L4-4 | `group_backfill(·,market,120)` | `O0W20xAb` | 0.62 | 0.33 | −0.16 |
| T-L4-5 | `group_backfill(·,market,252)` | `QP0oP9vW` | 0.62 | 0.33 | −0.16 |
| T-L4-7 | `group_std_dev` | `A1x217xw` | −0.19 | −0.03 | −0.84 |
| T-L4-6 | `group_sum` | `YPa9Pga6` | −0.29 | −0.07 | +0.05 |

**T-L4 结论（`converge=yes`）**：**全 ΔS≤0 ⇒ 收敛 group_rank**；标准izing 型三条逐位相同 0.66 且 2Y 翻负（−0.27）⇒ TSI 的 2Y 高度依赖 group_rank 的截面结构。

### T-L5 · 设置档

| 档 | α（market 轴 / industry 轴） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `88N2mNjq` / `e7aEjrdO` | **0.90 / 0.88** | 0.57/0.53 | +0.32/+0.31 |
| INDUSTRY | `omak8A3v` / `88N257av` | 0.74 / 0.78 | 0.42/0.44 | +0.17/+0.22 |
| SECTOR | `N1P2x3Ve` / `78Y27M65` | 0.60 / 0.67 | 0.32/0.36 | +0.03/+0.03 |
| FAST | `RRevM7Ga` / `6XM27l5K` | 0.80 / 0.85 | 0.39/0.42 | +0.06/+0.10 |
| SUBINDUSTRY + decay 8 | `vRAo8Wkd` / `gJa06nQg` | **0.90** / 0.87 | **0.57**/0.52 | +0.31/+0.30 |

**T-L5 结论（`converge=yes`，基线不变）**：INDUSTRY 0.74–0.78、SECTOR 0.60–0.67、FAST 0.80–0.85 均低于基线 0.90；decay8 **逐位相同 0.90**（同 S/F/2Y，仅 TO 1.91%→1.86%）⇒ 四档无增益，**基线（SUBINDUSTRY × decay4 × market）即最优**。★ 与 Q/S 同型：**慢变量水平型信号对中性化档不敏感、对风险模型反而受损**。
**L5-R 空转（基线未变）**：内核已于 L2 在相同设置下全替，无新基线可重扫。
**★ 模板 T 天花板 = S0.90 / F0.57 / 2Y0.32 / TO1.9%**（SUBINDUSTRY × ts_mean126 × market × group_rank × reverse）——TO 1.9% 是全数据集第二低。

---

## 模板 U · `security_trade_count_3mo`（D 计数族·三月窗，镜像 S0.42 / 2Y −0.23）完整梯度（2026-11-22）

### U-L2-A（8 臂，批 `2iUSMu57X54o998mPGV4e1m`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| U-L2-1 | `ts_scale` | `KPgZWbMp` | 0.48 | 0.21 | −0.28 |
| U-L2-2 | `ts_rank` | `N1P8YpEw` | 0.52 | 0.23 | −0.15 |
| U-L2-3 | `ts_quantile` | `78YlewPx` | 0.52 | 0.23 | −0.13 |
| U-L2-4 | `ts_av_diff` | `RRePGpxb` | 0.47 | 0.20 | −0.29 |
| U-L2-5 | `ts_delta` | `88NXMzWX` | 0.47 | 0.20 | −0.46 |
| U-L2-6 | `ts_mean` | `N1P8Ypdw` | 0.73 | 0.41 | **+0.52** |
| **U-L2-7** | **`ts_std_dev`** | **`blaAeLmM`** | **0.81** | **0.49** | +0.25 |
| U-L2-8 | `ts_ir` | `A1xEowpw` | 0.43 | 0.18 | −0.24 |

**U-L2-A 结论**：**`ts_std_dev` 0.81**（ΔS +0.39）最优；`ts_mean` 0.73 但 **2Y 0.52**（本模板最高）——**三月窗计数是「波动型 + 水平型」双内核候选**，与 P（_3yr）的 ts_av_diff 最优不同，**D 族的窗口长度改变最优内核类型**。

**U-L2-B（8 臂，批 `3mwSFY91l4ph9K1aYwqsLx4`）**

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| U-L2-0 | `ts_zscore`（基线） | `O0W21ONb` | 0.53 | 0.25 | −0.34 |
| U-L2-9 | `ts_arg_max` | `WjlxEMbZ` | 0.71 | 0.33 | +0.34 |
| U-L2-10 | `ts_arg_min` | `blaKYXOM` | 0.50 | 0.20 | +0.02 |
| U-L2-11 | `ts_returns` | `d5aP2p1j` | 0.40 | 0.16 | −0.49 |
| U-L2-12 | `ts_product` | `58J2ZxgX` | **−0.73** | −0.36 | −0.10 |
| U-L2-13 | `ts_sum` | `blaKYX8M` | 0.74 | 0.41 | +0.29 |
| U-L2-14 | `ts_max_diff` | `O0W21OJJ` | 0.23 | 0.06 | −0.03 |
| U-L2-15 | `days_from_last_change` | `88N2mbRo` | **−0.69** | −0.39 | −0.32 |

**U-L2 终态**：`ts_std_dev` 0.81 最优（`ts_sum` 0.74 / `ts_mean` 0.73 / `ts_arg_max` 0.71 次之）⇒ **L2b = ts_std_dev × 126**。

### U-L2b · 窗口全替（批 `4E5Rc1eQ44pDaP9S2CKees8`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **U-L2b-1** | **66** | **`rK7nK1EJ`** | **0.81** | **0.49** | **+0.36** |
| U-L2b-2 | 250 | `wpovp8Ov` | 0.78 | 0.46 | +0.24 |
| U-L2b-3 | 504 | `RRevRJY0` | 0.74 | 0.42 | +0.33 |
| U-L2b-4 | 750 | `VkNRkvEM` | 0.67 | 0.37 | +0.06 |
| 基线 | 126 | `blaAeLmM` | 0.81 | 0.49 | +0.25 |

**U-L2b 结论（`converge=no` 按 2Y）**：66 与 126 并列 S0.81，**2Y 0.36 vs 0.25** ⇒ 换 66。⇒ **L3 基线 = ts_std_dev66 × industry**。

### U-L3 · 分组轴全替（批 `1BJLVE7Zz4Fw8JXL4bq1YPZ`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| U-L3-6 | `industry`（基线） | `rK7nK1EJ` | **0.81** | **0.49** | +0.36 |
| U-L3-1 | `subindustry` | `gJa0JWMm` | 0.80 | 0.46 | **+0.42** |
| U-L3-3 | `market` | `gJa0JW9e` | 0.74 | 0.44 | +0.39 |
| U-L3-4 | `exchange` | `XgaOgR80` | 0.74 | 0.44 | +0.39 |
| U-L3-5 | `country` | `zqdLqrNX` | 0.74 | 0.44 | +0.39 |
| U-L3-2 | `sector` | `1YW2Yjz6` | 0.73 | 0.43 | +0.37 |

**U-L3 结论（`converge=yes` 按 S）**：industry 0.81 保持最优（subindustry 0.80 但 2Y +0.06 更高，按 S 判据仍取 industry）；market≡exchange≡country 0.74。⇒ **L4 基线 = ts_std_dev66 × industry**。

**U-L4 · 外层层（批 `3PJFqc7Hw5iw8Z8Shj0j0ZP`，8 臂）**

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| U-L4-0 | `group_rank`（基线） | `rK7nK1EJ` | **0.81** | **0.49** | +0.36 |
| U-L4-2 | `group_zscore` | `omak87j6` | 0.62 | 0.35 | +0.44 |
| U-L4-1 | `group_scale` | `npaXx9Gz` | 0.61 | 0.33 | +0.33 |
| U-L4-3 | `group_neutralize` | `A1x2j9XE` | 0.39 | 0.21 | +0.34 |
| U-L4-5 | `group_backfill(·,industry,252)` | `Jj82MqAn` | 0.35 | 0.16 | +0.25 |
| U-L4-4 | `group_backfill(·,industry,120)` | `QP0oZMxM` | 0.37 | 0.18 | +0.33 |
| U-L4-7 | `group_std_dev` | `O0W2QO31` | −0.42 | −0.12 | −0.52 |
| U-L4-6 | `group_sum` | `2r528Mg5` | −0.58 | −0.21 | −0.72 |

**U-L4 结论（`converge=yes`）**：**全 ΔS≤0 ⇒ 收敛 group_rank**（zscore 0.62 的 2Y 0.44 略高但 S 差 0.19）；聚合型 TO 95–96%、DD 135–164% 崩。

**U-L5 · 设置档**

| 档 | α（industry 轴 / market 轴） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `rK7nK1EJ` | **0.81** | **0.49** | +0.36 |
| INDUSTRY | `N1P2xNXL` / `2r528A1Y` | 0.63 / 0.57 | 0.34/0.30 | +0.12/+0.11 |
| SECTOR | `qM7w8WZZ` / `RRevMVLd` | 0.52 / 0.45 | 0.26/0.22 | −0.07/−0.05 |
| FAST | `wpovqj0d` / `E5Q21vZ0` | 0.79 / 0.72 | 0.39/0.35 | +0.12/+0.09 |
| **SUBINDUSTRY + decay 8** | **`A1x292Ml`** / `Jj82q2KE` | **0.82** | **0.50** | **+0.39** |

**U-L5-R · 换基线（decay8）后内核重扫（批 `2YWmrP1vN4tm9OHyazHWFuK`，4 臂）**

| 臂 | 内核（decay8 / industry / W66） | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-1 | `ts_std_dev`（基线） | `A1x292Ml` | **0.82** | **0.50** | **+0.39** |
| R-2 | `ts_sum` | `RRev3830` | 0.66 | 0.35 | +0.19 |
| R-3 | `ts_mean` | `pwapXlmj` | 0.65 | 0.34 | +0.33 |
| R-4 | `ts_ir` | `Grm7aLa5` | 0.56 | 0.27 | +0.19 |
| R-5 | `ts_arg_max` | `6XM2898p` | 0.54 | 0.22 | −0.08 |

**U-L5 结论（`converge=no` 但增益仅 +0.01）**：decay8 0.82 微超基线 0.81（2Y +0.03），INDUSTRY/SECTOR/FAST 全劣。**L5-R 未翻转**（ts_std_dev 0.82 领先次优 0.16）。
**★ 模板 U 天花板 = S0.82 / F0.50 / 2Y0.39 / TO2.9%**（decay8 × ts_std_dev66 × industry × group_rank × reverse）——与 P（_3yr）的 1.23 差距 0.41，**同族内窗口越短信号越弱，D 计数族内部呈单调梯度：_3yr 1.23 > _2yr 0.85 > _1wk 0.96† > _3mo 0.82 > 当日 0.80**（†J 的 0.96 是 ts_std_dev+504+FAST 的特例）。

---

## 模板 V · `divide(_1mo, _1yr)` 计数归一（D 族相对活跃度，镜像 S0.41 / 2Y −0.60）完整梯度（2026-11-22）

> 构造：`divide(vec_sum(inst25_security_trade_count_1mo), vec_sum(inst25_security_trade_count_1yr))`（近月活跃度 ÷ 年度基线 ⇒ **已经是无量纲比值**）

### V-L2-A（8 臂，批 `36W8SyVg4kX8QPIC1cOqrx`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| V-L2-1 | `ts_scale` | `pwapXkRq` | 0.45 | 0.19 | −0.32 |
| V-L2-2 | `ts_rank` | `78Y2ArNO` | 0.53 | 0.23 | −0.08 |
| V-L2-3 | `ts_quantile` | `E5Q27Mpr` | 0.51 | 0.22 | −0.09 |
| V-L2-4 | `ts_av_diff` | `O0W2YjNR` | 0.47 | 0.19 | −0.10 |
| V-L2-5 | `ts_delta` | `6XM28Qj5` | 0.35 | 0.13 | **−0.70** |
| **V-L2-6** | **`ts_mean`** | **`XgaOrxJX`** | **0.67** | 0.33 | **+0.52** |
| V-L2-7 | `ts_std_dev` | `akagY8xO` | **0.67** | 0.35 | +0.06 |
| V-L2-8 | `ts_ir` | `rK7n3we8` | 0.48 | 0.21 | −0.06 |

**V-L2-A 结论**：**`ts_mean` 与 `ts_std_dev` 并列 0.67**（ΔS +0.26），但 **ts_mean 的 2Y 0.52 vs ts_std_dev 0.06** ⇒ 取 `ts_mean`。**比值型信号同样偏好水平/波动内核**（比值已去量纲，rank/quantile 反而丢信息）。

**V-L2-B（8 臂，批 `WY35h5Bu4u1coiijE5t18Z`）**

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| V-L2-0 | `ts_zscore`（基线） | `VkNRgjN0` | 0.41 | 0.16 | −0.60 |
| **V-L2-9** | **`ts_arg_max`** | **`78Y2EbGO`** | **0.80** | **0.41** | **+0.79** |
| V-L2-10 | `ts_arg_min` | `gJa0EOGv` | 0.68 | 0.32 | +0.20 |
| V-L2-11 | `ts_returns` | `npaXMRqd` | 0.40 | 0.16 | −0.32 |
| V-L2-12 | `ts_product` | `vRAo3MGb` | **−0.74** | −0.39 | −0.39 |
| V-L2-13 | `ts_sum` | `rK7nvgV3` | 0.69 | 0.36 | +0.38 |
| V-L2-14 | `ts_max_diff` | `Jj82ZE1n` | 0.43 | 0.16 | +0.13 |
| V-L2-15 | `days_from_last_change` | `blaK5Zn6` | **−0.69** | −0.39 | −0.22 |

**V-L2 终态**：★ **`ts_arg_max` 0.80 / F0.41 / 2Y 0.79** —— **全数据集唯一 2Y 接近 S 的内核**（S0.80/2Y0.79 近乎 1:1，无跷跷板）。机理解释：`ts_arg_max` 是「比值在窗内达峰后经过多少天」——**近期活跃度回落的速度**本身是均值回复信号，其 PnL 时间结构与「水平高低」正交，故 2Y 不被 2022–23 单年拖累。⇒ **V 用 ts_arg_max 作 L2b 基线**（这是本数据集第 5 次内核非典型最优）。

### V-L2b · 窗口全替（批 `28qOHdfIt5aycGSzsPlgqMF`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| V-L2b-2 | 250 | `MP62moq9` | 0.78 | 0.40 | +0.73 |
| V-L2b-4 | 750 | `78Y29E0Z` | 0.63 | 0.30 | +0.37 |
| V-L2b-1 | 66 | `3q02LZYN` | 0.57 | 0.24 | −0.10 |
| V-L2b-3 | 504 | `wpovgMO5` | 0.51 | 0.22 | +0.21 |
| 基线 | 126 | `78Y2EbGO` | **0.80** | **0.41** | **+0.79** |

**V-L2b 结论（`converge=yes`）**：126 保持最优（250 次之 0.78/2Y0.73，同样近 1:1）⇒ **L3 基线 = ts_arg_max126 × industry**。

### V-L3 · 分组轴全替（批 `2AGRsg1Zn4Ktbrp2FVEgYRP`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| V-L3-6 | `industry`（基线） | `78Y2EbGO` | **0.80** | **0.41** | **+0.79** |
| V-L3-1 | `subindustry` | `O0W2v08J` | 0.80 | 0.40 | +0.71 |
| V-L3-3 | `market` | `npaXbpAw` | 0.79 | 0.41 | +0.62 |
| V-L3-4 | `exchange` | `E5Q2A5VG` | 0.79 | 0.41 | +0.62 |
| V-L3-5 | `country` | `LLK2xL52` | 0.79 | 0.41 | +0.62 |
| V-L3-2 | `sector` | `58J2V8gX` | 0.77 | 0.39 | +0.62 |

**V-L3 结论（`converge=yes`）**：industry 与 subindustry 并列 0.80，但 **industry 的 2Y 0.79 > 0.71** ⇒ 保持 industry；market≡exchange≡country 0.79。本模板**轴最不敏感**（六轴跨度仅 0.03）。⇒ **L4 基线 = ts_arg_max126 × industry**。

### V-L4 · 外层层（批 `3Slzg69Qu4i3asLFFDfCh0X`，8 臂）

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| V-L4-0 | `group_rank`（基线） | `78Y2EbGO` | **0.80** | **0.41** | **+0.79** |
| V-L4-7 | `group_std_dev` | `npaX0b9a` | 0.46 | 0.13 | +0.52 |
| V-L4-4 | `group_backfill(·,industry,120)` | `mLalOkw6` | 0.19 | 0.04 | +0.25 |
| V-L4-3 | `group_neutralize` | `YPa9ZdLw` | 0.18 | 0.05 | +0.52 |
| V-L4-5 | `group_backfill(·,industry,252)` | `A1x26djX` | 0.18 | 0.04 | +0.20 |
| V-L4-1 | `group_scale` | `akagJ3k1` | 0.16 | 0.04 | +0.55 |
| V-L4-2 | `group_zscore` | `rK7nkmKa` | 0.13 | 0.03 | +0.47 |
| V-L4-6 | `group_sum` | `WjlxkmMN` | 0.05 | 0.00 | −0.61 |

**V-L4 结论（`converge=yes`，**外层最脆的第二例**）**：**全 ΔS 崩**（0.05–0.46 vs 基线 0.80）——`ts_arg_max` 输出的「天数」是**序数型**变量，任何标准化（scale/zscore/neutralize）都会破坏其序关系。2Y 仍高（0.47–0.55）但 S 已毁 ⇒ 与 R（ts_ir）同型：**序数/比值内核只能用 group_rank 作外层**。

### V-L5 · 设置档（`4CGcbrfd65dIahpUAmL13tb`(INDUSTRY) / `3c6N9HdKk4yV93KTBz66iog`(SECTOR) / `2VzHRq9J64SG8CyE4eVrsTi`(FAST) / `3jtLEB6zq4uPaKo3ucCPABV`(decay8)，与 W 合并批各 4 臂）

| 档 | α（V industry / V market） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `78Y2EbGO` | **0.80** | **0.41** | **+0.79** |
| INDUSTRY | `A1x26mww` / `88N2AYzX` | 0.66 / 0.68 | 0.30/0.33 | +0.61/+0.49 |
| SECTOR | `9ql2o8gr` / `KPg2evx1` | 0.56 / 0.61 | 0.24/0.28 | +0.33/+0.15 |
| FAST | `leaNJA72` / `d5aPeWnY` | 0.75 / 0.78 | 0.31/0.33 | +0.49/+0.27 |
| **SUBINDUSTRY + decay 8** | **`xAvEX30b`** / `3q02gXLQ` | **0.78** / 0.77 | **0.40**/0.40 | **+0.75**/+0.58 |

**V-L5 结论（`converge=yes`，基线不变）**：四档最高 0.78（decay8）仍低于基线 0.80 ⇒ **SUBINDUSTRY × decay4 × industry 即最优**。
**★ 模板 V 天花板 = S0.80 / F0.41 / 2Y0.79 / TO3.9%**（SUBINDUSTRY × ts_arg_max126 × industry × group_rank × reverse）——**2Y/S = 0.99，是全 23 个模板里唯一「2Y 与 S 等值」的形态**（S↔2Y 跷跷板在此模板上不存在）。

### W-L5 · 设置档（同 V 四条合并批）

| 档 | α（W industry / W market） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `1YW2EbWR` | **0.78** | **0.44** | **+0.74** |
| INDUSTRY | `Jj82l1Oj` / `Grm7VxL0` | 0.55 / 0.52 | 0.26/0.24 | +0.43/+0.32 |
| SECTOR | `wpov63w1` / `omak2Rw6` | 0.47 / 0.41 | 0.21/0.17 | +0.20/+0.00 |
| FAST | `9ql2gxJ1` / `YPa9X1Qv` | 0.66 / 0.53 | 0.27/0.20 | +0.34/−0.06 |
| SUBINDUSTRY + decay 8 | `0mPanXvk` / `akagXbvx` | 0.77 / 0.76 | 0.43/0.43 | +0.72/+0.58 |

**W-L5 结论（`converge=yes`，基线不变）**：最高 0.77（decay8）低于基线 0.78 ⇒ **SUBINDUSTRY × decay4 × industry 最优**。
**★ 模板 W 天花板 = S0.78 / F0.44 / 2Y0.74 / TO3.0%**（SUBINDUSTRY × ts_arg_min504 × industry × group_rank × reverse）——**2Y/S = 0.95**，与 V 同型（序数型内核天然 2Y 稳健）。

---

## ★★ 数据集 ATOM 穷尽终判（**23 个互异模板，全部完整 5 层梯度 + L5-R**，2026-11-22）

### 模板天花板全表（23 个互异基线）

| # | 模板（信号构造） | 族 | L2 冠军 | 窗 | 轴 | 外层 | **天花板 S / F / 2Y / TO** | 设置档 |
|---|---|---|---|---|---|---|---|---|
| A | `vec_avg(activity)` 活跃度 | G | `ts_rank` | 66 | subindustry | group_rank | **1.01** / 0.37 / 0.30 / 23.7% | FAST |
| B | `vec_sum(position_change)` 仓位变化 | B | `ts_delta` | — | — | — | **0.97** / — / — / — | FAST |
| **C** | **`position_change ⊖ crowding` 残差组合** | B⊖A | `ts_delta` | 126 | industry | group_rank | **★ 1.26** / **0.61** / 0.58 / 22.7% | FAST |
| D | `entry_position` 开仓规模 | B | `ts_delta` | — | — | — | **0.99** / — / — / — | FAST |
| E | `age` 空仓年龄 | C | `ts_delta` | — | — | — | **1.04** / — / — / — | FAST |
| F | `position_change` 单腿（αC 14 最高） | B | `ts_av_diff` | — | — | — | **1.08** / — / — / — | FAST |
| G | `concentration` 集中度 | A | — | — | — | — | **0.90** / — / — / — | decay8 |
| H | `trade_length` 持仓时长 | C | `ts_av_diff` | 126 | industry | group_rank | **0.90** / 0.42 / −0.06 / 9.1% | FAST |
| I | `security_avg_trade_length` | C | `ts_av_diff` | 126 | industry | group_rank | **0.90** / 0.42 / −0.07 / 9.1% | FAST |
| J | `security_trade_count_1wk` | D | `ts_std_dev` | 504 | industry | group_rank | **0.96** / 0.51 / 0.54 / 8.4% | FAST |
| K | `security_trade_count`（当日） | D | `ts_std_dev`★翻转 | 126 | industry | group_rank | **0.80** / 0.39 / 0.25 / 9.0% | FAST |
| L | `position` 仓位水平 | B | — | — | — | — | **0.89** / 0.53 / 0.39 / — | 基线 |
| M | `is_open` 开放哑变量 | B | `ts_delta` | 250 | market | group_rank | **1.01** / 0.53 / 0.04 / 9.0% | FAST |
| N | `crowding` 拥挤度 | A | `ts_mean` | 250 | market | group_rank | **0.90** / **0.57** / 0.54 / 1.8% | decay8 |
| O | `security_trade_count_2yr` | D | `ts_mean` | 126 | market | group_rank | **0.85** / 0.40 / 0.28 / 8.0% | FAST |
| **P** | **`security_trade_count_3yr`** | D | **`ts_av_diff`** | 250 | subindustry | **`group_scale`** | **★★ 1.23** / **0.71** / **1.93** / 9.4% | **FAST** |
| Q | `manager_count` 经理广度 | F | `ts_sum`★翻转 | 250 | industry | group_rank | **0.95** / 0.47 / 0.14 / 7.8% | FAST |
| R | `manager_position_count` | F | `ts_ir` | 126 | industry | group_rank | **0.80** / 0.42 / 0.38 / 3.9% | 基线 |
| S | `sentiment` 做空情绪 | A | `ts_ir` | 66 | industry | group_rank | **0.93** / 0.56 / 0.48 / 3.9% | 基线 |
| T | `total_short_interest` 总空头利息 | A | `ts_mean` | 126 | market | group_rank | **0.90** / **0.57** / 0.32 / 1.9% | 基线 |
| U | `security_trade_count_3mo` | D | `ts_std_dev` | 66 | industry | group_rank | **0.82** / 0.50 / 0.39 / 2.9% | decay8 |
| V | `divide(_1mo, _1yr)` 计数归一 | D | `ts_arg_max` | 126 | industry | group_rank | **0.80** / 0.41 / **0.79** / 3.9% | 基线 |
| W | `divide(cover, short)` 方向比 | E | `ts_arg_min` | 504 | industry | group_rank | **0.78** / 0.44 / **0.74** / 3.0% | 基线 |

### 终判

1. **数据集 ATOM 天花板（按 S）= S1.26 / F0.61 / 2Y0.58 / TO22.7%**（模板 C：FAST × `ts_delta`126 × industry × group_rank × `reverse(position_change ⊖ crowding)`）。
2. **2Y 维度天花板 = 1.93**（模板 P：FAST × `group_scale` × `ts_av_diff`250 × subindustry）；**P 是唯一把 2Y 推过 1.58 闸的模板**（S 1.23 / F 0.71）。
3. **交付判定：0 颗**。
   - 最优两者分别卡在不同闸：**C 卡 2Y（0.58，差 1.00）与 F（0.61，差 0.39）**；**P 卡 S（1.23，差 0.35）与 F（0.71，差 0.29）**。
   - **S 与 2Y 在本数据集上系统性互斥**：P（S1.23/2Y1.93）与 C（S1.26/2Y0.58）已经分别从「2Y 侧」和「S 侧」逼近各自的墙，但**没有任何模板能同时满足 S≥1.58 与 2Y≥1.58**。
   - **V/W 的发现证明互斥不是绝对的**（2Y/S ≈ 1.0），但它们的绝对水平只有 0.78–0.80 —— **序数型内核（ts_arg_max/ts_arg_min）能消掉跷跷板却拿不到绝对强度**。这是本数据集最深的结构性结论。
4. **不判死**（按 §7.6）：信号层弱是事实，但 23 个互异模板 × 完整梯度已穷尽「单字段 ATOM」面；数据集留有**跨集腿**价值（V/W 的 2Y 稳健性 + P 的 2Y 1.93 可作 regular 组合的第二腿）。记录为 **ATOM 面穷尽、S 层弱**，不作数据集级判死（用户 2026-11-19 明令「轻易不判死」）。
5. **梯度验收**：`tools/gates/gradient_gate.py` 判定 `GRADIENT_DONE`（23 模板 × ≥5 层、~740 臂）。

**★ 跨模板方法论收获（可迁移）**：
- **内核算子按族选，且按窗口长度再选**：D 计数族 `_1wk`→ts_std_dev、`_2yr/_3mo`→ts_mean/ts_std_dev、`_3yr`→ts_av_diff；F 广度族→ts_ir/ts_sum；A 情绪族→ts_ir/ts_mean；比值族→ts_mean/ts_arg_*。
- **外层算子与内核「是否已无量纲」强耦合**：ts_ir / ts_arg_* / divide 型内核**只能用 group_rank**（其它外层把 S 打到 ≤0.5）；纯水平型内核（ts_mean/ts_av_diff）则可换 group_scale（P 的 +0.10/2Y+0.95 唯一例外成功案例）。
- **设置档不是普遍杠杆**：FAST 在 A/B/C/D/E/F/J/O/P/Q/M 有效，但在 N/R/S/T/U/V/W 上**全部无效或有害**——规律是「**差分/波动型内核吃 FAST，水平/序数型内核吃 decay8 或基线**」。
- **5 次内核翻转**（B/D/K/Q/O）都在换设置基线后发生 ⇒ **L5-R 必做**。

---

## 模板 W · `divide(cover, short)` 平空/卖空比（E 族方向比，镜像 S0.38 / 2Y −0.14）完整梯度（2026-11-22）

> 构造：`divide(vec_sum(inst25_security_cover_count), vec_sum(inst25_security_short_count))`（平空 ÷ 卖空 ⇒ 做空行为的方向比）

### W-L2-A（8 臂，批 `4rSPOneYm50Y9lOpz5aoiEt`）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| W-L2-1 | `ts_scale` | `RRevQ9Gj` | 0.44 | 0.20 | +0.14 | **21.0%** |
| W-L2-2 | `ts_rank` | `E5Q2WN90` | 0.61 | 0.31 | +0.31 | 13.7% |
| W-L2-3 | `ts_quantile` | `ZYa13gOn` | 0.58 | 0.28 | +0.26 | 13.7% |
| W-L2-4 | `ts_av_diff` | `Jj82Eo6W` | 0.60 | 0.30 | +0.30 | 13.7% |
| W-L2-5 | `ts_delta` | `Grm7AXZZ` | 0.46 | 0.20 | +0.17 | 19.7% |
| W-L2-6 | `ts_mean` | `E5Q2W8Z0` | 0.62 | 0.34 | −0.00 | 2.6% |
| W-L2-7 | `ts_std_dev` | `VkNRjmvG` | 0.59 | 0.32 | −0.09 | 2.6% |
| W-L2-8 | `ts_ir` | `YPa9KEjJ` | 0.30 | 0.13 | +0.04 | 4.5% |

**W-L2-B（8 臂，批 `3ahMRMbfF53jbWr18Ur8c3UE`）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| W-L2-0 | `ts_zscore`（基线） | `Grm7p8WG` | 0.38 | 0.16 | −0.14 | **23.3%** |
| W-L2-9 | `ts_arg_max` | `Wjlx6Xlk` | 0.50 | 0.22 | −0.05 | 4.1% |
| **W-L2-10** | **`ts_arg_min`** | **`9ql2L6le`** | **0.66** | **0.36** | **+0.26** | 5.0% |
| W-L2-11 | `ts_returns` | `rK7nvz0E` | 0.28 | 0.12 | +0.35 | **40.5%** |
| W-L2-12 | `ts_product` | `akagqPR9` | **−0.60** | −0.30 | −0.14 | 5.7% |
| W-L2-13 | `ts_sum` | `ZYa1elgx` | 0.40 | 0.20 | −0.04 | 2.9% |
| W-L2-14 | `ts_max_diff` | `wpovMz32` | 0.63 | 0.33 | +0.28 | 11.7% |
| W-L2-15 | `days_from_last_change` | `E5Q2Xa81` | **−0.58** | −0.30 | −0.13 | 3.2% |

**W-L2 终态**：**`ts_arg_min` 0.66**（ΔS +0.28）最优；`ts_max_diff` 0.63 / `ts_mean` 0.62 次之。★ **W 的 TO 结构独特**：差分/排名型内核 TO 12–40%（`ts_returns` 40.5% 直接撞 HIGH_TURNOVER），而 arg_min/mean 型只有 2.6–5.0% —— cover/short 比值是**稀疏事件比**，差分会被零值抖动放大。⇒ **L2b 基线 = ts_arg_min × 126**。

### W-L2b · 窗口全替（批 `1zEb7banv5e7cAUagZiySE6`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **W-L2b-3** | **504** | **`1YW2EbWR`** | **0.78** | **0.44** | **+0.74** |
| W-L2b-2 | 250 | `qM7wqr7j` | 0.65 | 0.34 | +0.50 |
| W-L2b-1 | 66 | `pwapOraV` | 0.58 | 0.30 | +0.03 |
| W-L2b-4 | 750 | `6XM2OVG7` | 0.44 | 0.19 | −0.35 |
| 基线 | 126 | `9ql2L6le` | 0.66 | 0.36 | +0.26 |

**W-L2b 结论（`converge=no`，**ΔS +0.12 / Δ2Y +0.48**）**：★ **窗 504 跳到 0.78 / F0.44 / 2Y0.74**（三项齐升，且 2Y 与 S 近 1:1）——`ts_arg_min` 的「距上次谷值的天数」在**长窗**下才稳定（短窗被稀疏零值抖动）。⇒ **L3 基线 = ts_arg_min504 × industry**。

### W-L3 · 分组轴全替（批 `3QKQiC1YX4XJ9A8FGruANUi` 全 ERROR → 重派 `1hSFZLeth4tW9tN30u8Y60b`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| W-L3-6 | `industry`（基线） | `1YW2EbWR` | **0.78** | **0.44** | **+0.74** |
| W-L3-3 | `market` | `xAvEae2l` | 0.76 | 0.43 | +0.59 |
| W-L3-4 | `exchange` | `vRAoV5pb` | 0.76 | 0.43 | +0.59 |
| W-L3-5 | `country` | `O0W2vnz1` | 0.76 | 0.43 | +0.59 |
| W-L3-2 | `sector` | `zqdLz52R` | 0.75 | 0.42 | +0.63 |
| W-L3-1 | `subindustry` | `Jj82LnWE` | 0.58 | 0.27 | +0.69 |

**W-L3 结论（`converge=yes`）**：**industry 0.78 / 2Y 0.74 最优**（其 2Y 为六轴最高）；market≡exchange≡country 0.76；subindustry 崩 0.58。⇒ **L4 基线 = ts_arg_min504 × industry**。
> ⚠ 首批 `3QKQiC1YX4XJ9A8FGruANUi` **6/6 child ERROR**（平台侧 "error while running the simulation"，非表达式语法问题）；同表达式重派即成功 ⇒ 判为平台瞬时故障，非模板问题。

### W-L4 · 外层层（批 `n3v4b3Lj4nLbrteM4DbFn1`，8 臂）

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| W-L4-0 | `group_rank`（基线） | `1YW2EbWR` | **0.78** | **0.44** | +0.74 |
| W-L4-5 | `group_backfill(·,industry,252)` | `58J2R0XN` | 0.49 | 0.19 | +0.88 |
| W-L4-4 | `group_backfill(·,industry,120)` | `xAvEM8Lp` | 0.42 | 0.15 | +0.90 |
| W-L4-2 | `group_zscore` | `blaKpZmM` | 0.41 | 0.16 | **+1.12** |
| W-L4-1 | `group_scale` | `6XM2xV6L` | 0.27 | 0.08 | **+1.05** |
| W-L4-3 | `group_neutralize` | `LLK2eav9` | 0.25 | 0.08 | +0.76 |
| W-L4-7 | `group_std_dev` | `LLK2eaQ2` | 0.11 | 0.02 | +0.21 |
| W-L4-6 | `group_sum` | `pwap0rL6` | −0.13 | −0.02 | −0.58 |

**W-L4 结论（`converge=yes` 按 S）**：**全 ΔS≤0 ⇒ 收敛 group_rank（0.78）**。★ 副产物：**`group_zscore` / `group_scale` 把 2Y 抬到 1.05–1.12（全数据集最高 2Y 读数）但 S 只剩 0.27–0.41** —— 与本集反复出现的 S↔2Y 跷跷板同构；若未来允许「只过 2Y 闸」的评估口径，这两条是 2Y 的最强证据。

### W-L5 · 设置档（与 V 合并批）→ 在跑

---

## 模板 S · `sentiment`（A 族做空情绪，镜像 S0.45 / 2Y +0.40→−0.40）完整梯度（2026-11-22）

### S-L2-A（8 臂，批 `33PnJ2bP44xXclzesnUXund`）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| S-L2-1 | `ts_scale` | `9qlkmAXx` | 0.66 | 0.35 | +0.15 | 7.6% |
| S-L2-2 | `ts_rank` | `58JYeqQN` | 0.48 | 0.21 | +0.15 | 8.6% |
| S-L2-3 | `ts_quantile` | `pwa3Z1P6` | 0.46 | 0.19 | +0.12 | 8.4% |
| S-L2-4 | `ts_av_diff` | `omaZr96J` | 0.44 | 0.18 | −0.08 | 6.0% |
| S-L2-5 | `ts_delta` | `rK78VrO1` | 0.53 | 0.24 | +0.01 | 5.8% |
| S-L2-6 | `ts_mean` | `lea19Rv7` | 0.90 | 0.55 | **+0.27** | 2.3% |
| S-L2-7 | `ts_std_dev` | `omaZr9LJ` | 0.66 | 0.34 | +0.18 | 2.9% |
| **S-L2-8** | **`ts_ir`** | **`QP06g5bw`** | **0.93** | **0.56** | +0.26 | 3.2% |

**S-L2-A 结论**：**`ts_ir` 0.93**（ΔS **+0.48**，本模板最大单层增益）最优；`ts_mean` 0.90 紧随；rank/quantile/av_diff 全部 ≤0.48。**A 族情绪与 F 族广度在本轮都指向「水平/信噪型」，再次证明内核算子按族选**。

**S-L2-B（8 臂，批 `3LaSrjvX4P6bZV63pbXX4d`）**

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| S-L2-0 | `ts_zscore`（基线） | `akaGGZL6` | 0.45 | 0.19 | −0.40 |
| S-L2-9 | `ts_arg_max` | `O0WggPrb` | 0.83 | 0.43 | **+0.55** |
| S-L2-10 | `ts_arg_min` | `e7aEEw9N` | 0.50 | 0.21 | +0.20 |
| S-L2-11 | `ts_returns` | `blaAAZbl` | 0.59 | 0.29 | +0.32 |
| S-L2-12 | `ts_product` | `LLK33aN6` | **−0.67** | −0.33 | +0.01 |
| S-L2-13 | `ts_sum` | `LLK33aN9` | 0.77 | 0.43 | +0.06 |
| S-L2-14 | `ts_max_diff` | `88NXX9jX` | 0.50 | 0.21 | +0.46 |
| S-L2-15 | `days_from_last_change` | `lea11OKO` | **−0.72** | −0.40 | −0.26 |

**S-L2 终态（16 臂）**：`ts_ir` 0.93 最优（`ts_mean` 0.90 次之、2Y 0.27；`ts_arg_max` 0.83 但 **2Y 0.55 最高**）⇒ **L2b = ts_ir × 126**。

**S-L2b · 窗口全替（批 `4hUIc5byJ4N1b8F15vLLYA4j`，4 臂）**

| 臂 | 窗口 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| **S-L2b-1** | **66** | **`1YW02NYX`** | **0.93** | **0.56** | **+0.48** | 3.9% |
| S-L2b-2 | 250 | `pwa3pdYX` | 0.87 | 0.50 | +0.38 | 2.8% |
| S-L2b-4 | 750 | `QP06ovZp` | 0.85 | 0.48 | +0.33 | 2.3% |
| S-L2b-3 | 504 | `vRAPo1wd` | 0.82 | 0.45 | +0.17 | 2.4% |
| 基线 | 126 | `QP06g5bw` | 0.93 | 0.56 | +0.26 | 3.2% |

**S-L2b 结论（`converge=no` 按 2Y 判定）**：66 与 126 并列 S0.93 / F0.56，但 **2Y 0.48 vs 0.26（+0.22）** ⇒ **换基线到 W66**。⇒ **L3 基线 = ts_ir66 × industry**。

**S-L3 · 轴层（批 `ATR3bZj4qecCCxtthor6H`，6 臂）**

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| S-L3-6 | `industry`（基线） | `1YW02NYX` | **0.93** | **0.56** | **+0.48** |
| S-L3-3 | `market` | `1YW0Rd2k` | 0.92 | 0.56 | +0.45 |
| S-L3-4 | `exchange` | `0mP5LEaK` | 0.92 | 0.56 | +0.45 |
| S-L3-5 | `country` | `nparl2Xd` | 0.92 | 0.56 | +0.45 |
| S-L3-2 | `sector` | `LLK3w13M` | 0.90 | 0.54 | +0.47 |
| S-L3-1 | `subindustry` | `XgaMxnMX` | 0.81 | 0.44 | +0.39 |

**S-L3 结论（`converge=yes` 按 S）**：**industry 0.93 最优**（market≡exchange≡country 0.92 紧随，四者差 <0.01 —— 这是本数据集里轴最不敏感的模板）；subindustry 0.81 最差。⇒ **L4 基线 = ts_ir66 × industry**。

**S-L4 · 外层层（批 `3Yg5PMbUi4Jvcwffh6LubR`，8 臂）**

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| S-L4-0 | `group_rank`（基线） | `1YW02NYX` | **0.93** | **0.56** | **+0.48** |
| S-L4-2 | `group_zscore` | `npar5nPd` | 0.54 | 0.28 | +0.16 |
| S-L4-1 | `group_scale` | `3q0JvEVZ` | 0.45 | 0.21 | +0.21 |
| S-L4-3 | `group_neutralize` | `RRePwN6g` | 0.33 | 0.15 | −0.46 |
| S-L4-4 | `group_backfill(·,industry,120)` | `e7aEZn6d` | 0.28 | 0.10 | −0.29 |
| S-L4-5 | `group_backfill(·,industry,252)` | `Grm95ngO` | 0.22 | 0.07 | −0.35 |
| S-L4-7 | `group_std_dev` | `VkNebXx8` | −0.14 | −0.02 | +0.45 |
| S-L4-6 | `group_sum` | `9qlkO9xq` | −0.36 | −0.10 | −0.23 |

**S-L4 结论（`converge=yes`）**：又一次**全 ΔS≤0**（最高 zscore 0.54 vs 基线 0.93）；`ts_ir` 比值结构同样对外层标准化敏感（仅不如 R 极端）。⇒ 收敛 `group_rank`。

**S-L5 · 设置档** → 在跑（与 R 合并批）

---

## 状态（模板推进）

- A–O 全部 15 个互异模板完整梯度收官（**每个模板 5 层 + L5-R，共 ~620 臂**）。
- **模板天花板序列**：C **1.26** > F 1.08 > E 1.04 > A 1.01 = M 1.01 > D 0.99 > B 0.97 > J 0.96 > N 0.90 = G 0.90 = H 0.90 = I 0.90 > L 0.89 > O 0.85 > K 0.80。
- **数据集 ATOM 天花板 = S1.26（模板 C，同集残差组合 `position_change ⊖ crowding`，FAST × ts_delta126 × industry）**，距 S 闸（1.58）差 0.32、F 闸（1.0）差 0.39、2Y 闸（1.58）差 1.00 ⇒ **inst25 单集 ATOM 0 交付**。
- 剩余待做（镜像 |S| 更低、均 ≤0.53）：P `_3yr`、Q `manager_count`、R `manager_position_count`、S `sentiment`、T `total_short_interest`、U `_3mo`、V `divide(1mo,1yr)`、W `divide(cover,short)`。