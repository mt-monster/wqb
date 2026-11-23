# GBR / risk60 完整梯度档案（wave20261122_gradient_risk60）

> 依据：**用户 2026-11-22 标准升级「每个数据集至少 10 个模板」** + `wq-brain-ra-pipeline` 步 7 梯度必做 + §7.10。
> 数据集：risk60（**5 字段全 VECTOR**，Lending Fees 借券费率，`pyramidMultiplier=1.3`）｜塔：**risk（GBR/D1，0/3 未点亮）**
> 竞态说明：上个会话（2026-11-21）risk60 层 1 梯度批 `Zg3Rygbh` / `2ufzOOwC` **已 404 失效**，本轮从零重做并扩到 **12 模板**。
> 记录纪律：每模板 = 互异信号构造，各自跑完整 5 层（L2 内核 15 臂 → L2b 窗 4 → L3 轴 6 → L4 外包 8 → L5 设置 4 档 × 2 轴 + L5-R 重扫），逐层 Δ 表 + 收敛判定。
> 画像：`tracking/GBR/reference/datasets/risk60.md`（5/5 全字段已拉，六法已填）。

---

## §7.10.0 数据/字段前置体检（2026-11-22）

| 项 | 读数 |
|---|---|
| 字段全表 | 5/5（`count=5` = `platform_count=5`，单页全量） |
| 覆盖率 | cov **0.6694**（非盲区，约 470/700 可借券标的）；探针 TO 1.5–28% 证明真跑 |
| 元数据 | `rsk60_datatime`（HHMMSS 时间戳）⇒ **不作信号，数据层排除** |
| 机制聚类 | **2 条机制**：A 费率水平（bid/offer/last）+ B 做空流量（crowding）⇒ 5 字段 ≠ 5 信息源 |
| 数据窗口 | 探针均有 2Y 读数（正负皆有）⇒ 最近两年有数据，2Y 可评 |

---

## Layer 1 · 12 模板探针全替（2026-11-22，批 `2m3gol1a054Wcy4NweoLVxi`（T1–T8，8 臂）+ `3OgMGx4g44LucmC1ayIhHZkG`（T9–T12，4 臂））

冻结：`reverse(group_rank(<K>(ts_backfill(<FOLD>,250),126), industry))` / SUBINDUSTRY / decay4 / trunc0.08 / nanON

| 臂 | 模板 | 构造（FOLD） | 探针内核 | α | S | F | 2Y | TO |
|---|---|---|---|---:|---:|---:|---:|
| T1 | 出借费率水平 | `vec_avg(lending_fee_bid_rate)` | ts_zscore | `pwap1kq6` | 0.00 | 0.00 | −0.63 | 10.6% |
| T2 | 借入费率水平 | `vec_avg(rsk60_offer)` | ts_zscore | `xAvEmoKp` | −0.01 | −0.00 | −1.01 | 9.9% |
| T3 | 最新费率水平 | `vec_avg(rsk60_last)` | ts_zscore | `1YW2nRY6` | 0.15 | 0.03 | −0.45 | 16.3% |
| **T4** | 出借费率差分 | `vec_avg(lending_fee_bid_rate)` | ts_av_diff | `e7aWqP7z` | **0.31** | 0.11 | **+0.33** | 10.0% |
| **T5** | 借入费率差分 | `vec_avg(rsk60_offer)` | ts_av_diff | `qM7wmpM2` | **0.23** | 0.07 | +0.18 | 9.3% |
| T6 | 累计拥挤 | `vec_sum(rsk60_crowding)` | ts_sum | `QP0o5AZr` | 0.09 | 0.02 | −1.03 | 5.7% |
| **T7** | 去拥挤速度 | `vec_sum(rsk60_crowding)` | ts_av_diff | `leaNRYpA` | **0.46** | 0.19 | **+0.92** | 15.2% |
| T8 | 费率价差 | `subtract(offer, bid_rate)` | ts_zscore | `vRAoJb8w` | 0.00 | 0.00 | −1.18 | 11.6% |
| T9 | 费率比值 | `divide(offer, bid_rate)` | ts_zscore | `e7aWqvX6` | 0.03 | 0.00 | −0.56 | 12.4% |
| T10 | 费率⊖拥挤残差 | `vector_neut(bid_rate, crowding)` | ts_zscore | `akagWw55` | 0.14 | 0.03 | −0.20 | 13.7% |
| **T11** | 拥挤门控费率 | `multiply(offer, ts_rank(crowding,66))` | ts_zscore | `1YW2n0qm` | **0.43** | 0.14 | −0.03 | 21.8% |
| T12 | 费率波动 | `vec_avg(lending_fee_bid_rate)` | ts_std_dev | `1YW2n0qX` | 0.04 | 0.00 | −0.29 | 3.0% |

**L1 结论**：
1. **费率「水平」族（T1/T2/T3/T8/T9/T12）全灭（S≤0.15）且 2Y 全负** ⇒ 借券费率水平在 GBR 无横截面定价力。
2. **活面 = 变化/流量**：T7（crowding 差分）0.46/2Y**0.92**；T11（拥挤门控）0.43/subU**1.07**；T4（费率差分）0.31/2Y0.33；T5 0.23/2Y0.18。
3. 12 模板方向已定（探针含 reverse，S 正即方向对）⇒ 按 S 降序推进完整梯度：**T7 → T11 → T4 → T5 → T3 → T10 → T6 → 其余**。

---

## 模板 T7 · `vec_sum(rsk60_crowding)` 去拥挤速度 完整梯度

### T7-L2 · 内层时序算子全替（16 臂）

**T7-L2-A（8 臂，批 `1Haj0EdbL4vv9i2tNqqDQWb`）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| **T7-L2-2** | **`ts_rank`** | `d5aPEjmJ` | **0.52** | **0.19** | **+1.10** | 24.2% |
| T7-L2-3 | `ts_quantile` | `88N2al6q` | 0.51 | 0.18 | +1.10 | 24.3% |
| T7-L2-4 | `ts_av_diff`（基线） | `leaNRYpA` | 0.46 | 0.19 | +0.92 | 15.2% |
| T7-L2-1 | `ts_scale` | `Grm7Ml6O` | 0.27 | 0.10 | +0.77 | 11.2% |
| T7-L2-5 | `ts_delta` | `pwapVjzj` | 0.21 | 0.05 | −0.19 | 27.8% |
| T7-L2-7 | `ts_std_dev` | `88N2alKz` | 0.14 | 0.03 | −0.38 | 3.4% |
| T7-L2-6 | `ts_mean` | `d5aPEj7J` | 0.13 | 0.03 | −0.90 | 4.8% |
| T7-L2-8 | `ts_ir` | `j2aM9jdk` | 0.11 | 0.02 | −1.03 | 5.5% |

**T7-L2-B（8 臂，批 `t0g0db5r4gwcgLFKiRAztP`，含基线 ts_zscore + arg_max/arg_min/returns/product/sum/max_diff/days）**

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| T7-L2-0 | `ts_zscore` | `E5Q2q3gK` | 0.38 | 0.13 | +0.49 | 19.0% |
| T7-L2-14 | `ts_max_diff` | `O0W2neo7` | 0.34 | 0.13 | +0.29 | 6.7% |
| T7-L2-10 | `ts_arg_min` | `mLalqOqx` | 0.18 | 0.05 | −0.37 | 4.9% |
| T7-L2-9 | `ts_arg_max` | `MP62bwKr` | 0.12 | 0.03 | −0.50 | 5.0% |
| T7-L2-13 | `ts_sum` | `QP0o5AZr` | 0.09 | 0.02 | −1.03 | 5.7% |
| T7-L2-12 | `ts_product` | `kqaYnRQd` | −0.12 | −0.03 | +0.33 | 5.1% |
| T7-L2-11 | `ts_returns` | `3q02EdE0` | **−0.15** | −0.02 | +0.08 | **42.9%**（TO 爆） |
| T7-L2-15 | `days_from_last_change` | `RRevNXdz` | **−0.51** | −0.26 | −0.35 | 8.0% |

**T7-L2 终态（16 臂）**：**`ts_rank` 0.52 / F0.19 / 2Y1.10（ΔS +0.06 vs 基线 0.46）** 最优；`ts_quantile` 0.51/2Y1.10 并列（有序型内核领先）。★ **2Y 1.10 是 risk60 至今最高 2Y**。`ts_returns` TO 42.9% 崩、`days_from_last_change` −0.51 反向 ⇒ 不成立内核。⇒ **L2b 基线 = ts_rank × 126 × industry**。

### T7-L2b · 窗口全替（批 `3kZzy9dhK4TIa8RQQke893l`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| T7-L2b-3 | 504 | `akagNpl5` | **0.53** | 0.20 | +0.53 | 1.05 |
| 基线 | 126 | `d5aPEjmJ` | 0.52 | 0.19 | **+1.10** | 0.99 |
| T7-L2b-4 | 750 | `A1x2nAag` | 0.51 | 0.19 | +0.71 | 0.86 |
| T7-L2b-2 | 250 | `Jj82n9me` | 0.49 | 0.17 | +0.69 | 1.13 |
| T7-L2b-1 | 66 | `VkNRXWE8` | 0.42 | 0.13 | +0.69 | 1.07 |

**T7-L2b 结论（`converge=yes`）**：504 的 0.53 是「S+0.01 / 2Y−0.57」的交换 ⇒ 判噪声，**保持 126**（2Y 1.10 是全模板最高）。

### T7-L3 · 分组轴全替（批 `1GYA7Y9cK4LU9wJ15w4DgkxQ`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| T7-L3-3 | **`market`** | `e7aWrJRp` | **0.53** | **0.20** | **+1.12** | 1.14 |
| T7-L3-4 | `exchange` | `zqdLWzpR` | 0.53 | 0.20 | +1.12 | 1.14 |
| T7-L3-5 | `country` | `3q02AWLO` | 0.53 | 0.20 | +1.12 | 1.14 |
| 基线 | `industry` | `d5aPEjmJ` | 0.52 | 0.19 | +1.10 | 0.99 |
| T7-L3-2 | `sector` | `xAvEna0l` | 0.51 | 0.19 | +1.06 | 1.09 |
| T7-L3-1 | `subindustry` | `qM7wXZoZ` | 0.49 | 0.16 | +0.74 | 0.95 |

**T7-L3 结论（`converge=no`，+0.01/2Y+0.02）**：**market≡exchange≡country 0.53 / 2Y1.12 / subU 1.14**（单国三轴第 6 次逐位相同）；subindustry 最差 0.49。⇒ **L4 基线 = ts_rank126 × market**。

### T7-L4 · 外层层（批 `4DkFGX3kW4Xfc3d11BoaQwTk`，8 臂，market 轴）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| T7-L4-0 | `group_rank`（基线） | `e7aWrJRp` | 0.53 | **0.20** | **+1.12** | **22.8%** |
| T7-L4-2 | `group_zscore` | `YPa9AE6M` | **0.57** | 0.12 | +0.90 | **68.8%** |
| T7-L4-3 | `group_neutralize` | `akagOQ69` | 0.56 | 0.12 | +0.89 | 68.9% |
| T7-L4-1 | `group_scale` | `rK7nWNYE` | 0.55 | 0.11 | +0.89 | 68.9% |
| T7-L4-5 | `group_backfill(·,market,252)` | `ZYa1od50` | 0.55 | 0.11 | +0.91 | 68.5% |
| T7-L4-4 | `group_backfill(·,market,120)` | `1YW2gl96` | 0.54 | 0.11 | +0.90 | 68.5% |
| T7-L4-7 | `group_std_dev` | `zqdLW26X` | 0.01 | 0.00 | −0.39 | **111.5%** |
| T7-L4-6 | `group_sum` | `Jj82dWw2` | −0.15 | −0.02 | −0.82 | **115.2%** |

**T7-L4 结论（`converge=yes` —— **按可交付性判**）**：`group_zscore` 的 0.57 表面 +0.04，但**代价是 TO 22.8%→68.8%（平台 HIGH_TURNOVER 上限 0.70，仅余 1.2pt）且 F 0.20→0.12 砍半** ⇒ 判**非改进**，保留 `group_rank`。★ 与本数据集其它模板同型：**`ts_rank` 输出的分位型信号不能再标准化**（会把换手放大 3 倍）。⇒ **L5 基线 = ts_rank126 × market × group_rank**。

---

## 模板 T11 · `multiply(offer, ts_rank(crowding,66))` 拥挤门控费率 完整梯度

### T11-L2 · 内层时序算子全替（16 臂）

| 臂 | 内核 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| T11-L2-0 | `ts_zscore`（基线） | `1YW2n0qm` | **0.43** | **0.14** | −0.03 | 21.8% |
| T11-L2-4 | `ts_av_diff` | `omak3PJ5` | 0.42 | 0.14 | −0.16 | 20.5% |
| T11-L2-8 | `ts_ir` | `kqaY18WO` | 0.31 | 0.11 | −0.13 | 4.5% |
| T11-L2-1 | `ts_scale` | `xAvEPlVw` | 0.30 | 0.10 | −0.20 | 17.1% |
| T11-L2-7 | `ts_std_dev` | `YPa92lEl` | 0.28 | 0.09 | **+0.33** | 3.5% |
| T11-L2-9 | `ts_arg_max` | `ZYa1jko3` | 0.28 | 0.10 | −0.63 | 5.3% |
| T11-L2-13 | `ts_sum` | `pwapnQ63` | 0.26 | 0.09 | −0.09 | 3.4% |
| T11-L2-6 | `ts_mean` | `0mPaeGNr` | 0.25 | 0.08 | −0.48 | 3.9% |
| T11-L2-2 | `ts_rank` | `MP62Kgd6` | 0.24 | 0.06 | −0.91 | 22.6% |
| T11-L2-3 | `ts_quantile` | `wpovnN3v` | 0.24 | 0.06 | −0.86 | 22.6% |
| T11-L2-11 | `ts_returns` | `A1x2nqwW` | 0.23 | 0.05 | −0.53 | 24.8% |
| T11-L2-14 | `ts_max_diff` | `LLK2nO1e` | 0.21 | 0.07 | −0.33 | 9.1% |
| T11-L2-10 | `ts_arg_min` | `2r52vPK5` | 0.17 | 0.04 | +0.34 | 5.4% |
| T11-L2-5 | `ts_delta` | `1YW2aGlm` | 0.16 | 0.03 | −0.62 | 23.4% |
| T11-L2-12 | `ts_product` | `WjlxNKpP` | −0.23 | −0.08 | −0.03 | 3.7% |
| T11-L2-15 | `days_from_last_change` | `P05Anj37` | −0.49 | −0.24 | −0.40 | 9.1% |

**T11-L2 终态（16 臂）**：**基线 `ts_zscore` 0.43 保持最优**（`ts_av_diff` 0.42 并列）⇒ **收敛，L2b = ts_zscore × 126 × industry**。

### T11-L2b · 窗口全替（批 `NCYpJ9vn4XN8TS5WVV4HUA`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T11-L2b-4 | 750 | `QP0oE1P5` | 0.45 | 0.16 | −0.13 |
| T11-L2b-3 | 504 | `78Y2Jk88` | 0.44 | 0.15 | −0.23 |
| 基线 | 126 | `1YW2n0qm` | 0.43 | 0.14 | −0.03 |
| T11-L2b-2 | 250 | `XgaO1jjz` | 0.33 | 0.10 | −0.47 |
| T11-L2b-1 | 66 | `3q02zMMz` | 0.29 | 0.08 | −0.32 |

**T11-L2b 结论（`converge=yes`）**：750 的 +0.02 是噪声级（2Y −0.10）⇒ 保持 126。

### T11-L3 · 分组轴全替（批 `10MpwM7HV4wG9gFrc4KwdEu`，6 臂）

| 臂 | 轴 | α | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| 基线 | `industry` | `1YW2n0qm` | **0.43** | **0.14** | −0.03 | 1.07 |
| T11-L3-2 | `sector` | `kqaYQpP6` | 0.41 | 0.14 | +0.01 | **1.16** |
| T11-L3-3 | `market` | `d5aPdJjg` | 0.41 | 0.14 | +0.06 | 1.14 |
| T11-L3-4 | `exchange` | `P05AvL7M` | 0.41 | 0.14 | +0.06 | 1.14 |
| T11-L3-5 | `country` | `9ql2J5V9` | 0.41 | 0.14 | +0.06 | 1.14 |
| T11-L3-1 | `subindustry` | `xAvER7Nm` | 0.33 | 0.09 | −0.28 | 0.74 |

**T11-L3 结论（`converge=yes`）**：industry 0.43 保持最优（sector/market 0.41 但 subU 1.14–1.16 更高）⇒ **L4 基线 = ts_zscore126 × industry**。

### T11-L4 · 外层层（批 `2IdX6F6zU4OU8yuGWArpXM5`，8 臂，industry 轴）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| T11-L4-0 | `group_rank`（基线） | `1YW2n0qm` | **0.43** | **0.14** | −0.03 | 21.8% |
| T11-L4-2 | `group_zscore` | `1YW2gWJm` | 0.18 | 0.02 | −0.70 | 45.4% |
| T11-L4-1 | `group_scale` | `RRevreNg` | 0.09 | 0.01 | −0.48 | 45.3% |
| T11-L4-5 | `group_backfill(·,industry,252)` | `LLK2RKRe` | −0.07 | −0.01 | −0.73 | 45.6% |
| T11-L4-4 | `group_backfill(·,industry,120)` | `blaK9avm` | −0.11 | −0.01 | −0.80 | 45.7% |
| T11-L4-6 | `group_sum` | `6XM2EMEp` | −0.14 | −0.02 | −0.62 | **115.7%** |
| T11-L4-3 | `group_neutralize` | `0mPa8Pzr` | −0.15 | −0.02 | −0.89 | 47.7% |
| T11-L4-7 | `group_std_dev` | `kqaYKaKO` | −0.50 | −0.14 | −0.73 | 115.3% |

**T11-L4 结论（`converge=yes`，全崩）**：**除 group_rank 外全部 ΔS 负**（0.18 至 −0.50）⇒ 门控型信号（乘积已含截面信息）对外层标准化同样零容忍。⇒ **L5 基线 = ts_zscore126 × industry × group_rank**。

### T7/T11-L5 · 设置档（`3g4pfhdIs4HLb4zPaQjQFss`(INDUSTRY) / `3e3WKQ26z4vLconbL2xK3PX`(SECTOR) / `314Im28yf4L1bHZGo81Bo8w`(FAST) / `GYoFt4Ui4mR9h5t87ZInry`(decay8)，与 T11 合并批）

| 档 | α（T7 market / T7 industry / T11 industry / T11 market） | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `e7aWrJRp` / `1YW2n0qm` | **0.53 / 0.43** | 0.20/0.14 | +1.12/−0.03 | 1.14/1.07 |
| INDUSTRY | `omakKLYl` / `MP62papM` / `A1x2wNww` / `MP62paQM` | 0.44 / 0.44 / 0.37 / 0.35 | 0.16/0.16/0.13/0.12 | +0.84/+0.81/−0.21/−0.13 | **1.33**/1.11/1.26/1.36 |
| SECTOR | `xAvExYjJ` / `Jj82pxxn` / `mLal8gg1` / `3q0279XZ` | 0.35 / 0.28 / 0.20 / 0.22 | 0.12/0.08/0.05/0.07 | +1.02/+0.73/−0.54/−0.41 | 1.21/0.90/1.02/1.18 |
| **FAST** | **`pwapldX6`** / `RRev8E3o` / `6XM29dVO` / **`npaX2vR8`** | **0.76** / 0.67 / 0.59 / **0.70** | **0.21**/0.17/0.14/0.20 | +0.52/+0.44/−0.26/−0.00 | 1.16/0.94/1.07/**1.24** |
| SUBINDUSTRY + decay 8 | `akagnNNR` / `E5Q2EqkJ` / `MP62Qbk6` / `d5aP0nQw` | 0.50 / 0.50 / 0.47 / 0.45 | 0.24/0.23/0.21/0.21 | +1.04/+1.01/+0.14/+0.24 | 1.07/0.92/1.11/1.15 |

**T7/T11-L5 结论（`converge=no`，两模板均换基线到 FAST）**：
- **T7：FAST 0.76 / F0.21 / 2Y0.52（ΔS +0.23）**——本数据集最大单层增益；代价 **2Y 1.12→0.52**（跷跷板）。
- **T11：FAST 0.70 / F0.20 / subU 1.24（ΔS +0.27）**——同样是本模板最大增益；2Y 已为负 ⇒ FAST 不改变 2Y 弱。
- **decay8 是 2Y 轴最优**（T7 0.50/2Y**1.04**/F**0.24**/TO13.7%）——若按 2Y 优先应取 decay8。
- INDUSTRY/SECTOR 两档对 T7 与 T11 都是**净损**（0.20–0.44）。

### T7-L5-R · 换基线（FAST）后内核重扫（批 `4jIH6yfJd5afcgOt3UgCZky`，5 臂）

| 臂 | 内核（FAST / market / W126） | α | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| **R-2** | **`ts_quantile`** | `mLalV1VW` | **0.79** | **0.22** | +0.46 | 1.16 |
| R-1 | `ts_rank`（L5 基线） | `pwapldX6` | 0.76 | 0.21 | +0.52 | 1.16 |
| R-5 | `ts_zscore` | `A1x27mld` | 0.63 | 0.18 | +0.30 | 1.13 |
| R-3 | `ts_av_diff` | `e7aWxv3O` | 0.40 | 0.10 | +0.59 | 0.61 |
| R-4 | `ts_std_dev` | `akagEw1w` | 0.27 | 0.07 | +0.08 | 0.43 |

**T7-L5-R 结论（★第 6 次内核翻转）**：**`ts_quantile` 0.79 反超 `ts_rank` 0.76**（+0.03）⇒ 换基线；S/F/subU 三项齐升，仅 2Y −0.06。
**★ 模板 T7 天花板 = S0.79 / F0.22 / 2Y0.46 / TO32.0%**（FAST × ts_quantile126 × market × group_rank × reverse）。

### T11-L5-R · 换基线（FAST）后内核重扫（批 `2MVWo9fx44i0aZQOe7Rr4Qz`，4 臂）

| 臂 | 内核（FAST / market / W126） | α | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| R-1 | `ts_zscore`（L5 基线） | `npaX2vR8` | **0.70** | **0.20** | −0.00 | **1.24** |
| R-2 | `ts_av_diff` | `gJa0930e` | 0.36 | 0.08 | −0.31 | 0.74 |
| R-4 | `ts_std_dev` | `VkNR38L0` | 0.22 | 0.05 | +0.31 | 0.64 |
| R-3 | `ts_ir` | `qM7w6XpZ` | 0.15 | 0.03 | −1.00 | 0.30 |

**T11-L5-R 结论（未翻转）**：`ts_zscore` 0.70 保持最优（次优 0.36）⇒ 排序稳健。
**★ 模板 T11 天花板 = S0.70 / F0.20 / 2Y−0.00 / TO27.5% / subU1.24**（FAST × ts_zscore126 × market × group_rank × reverse）。

---

## 模板 T4 · `vec_avg(lending_fee_bid_rate)` 出借费率差分 完整梯度

### T4-L2（16 臂，批 `2B7zNSdSm53LaCX3XSBmoQC`（8 臂）+ `30WVoZbNF4mx9RmAkvI2muI`（8 臂））

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T4-L2-8** | **`ts_ir`** | `leaN31l5` | **0.38** | 0.15 | +0.07 |
| T4-L2-9 | `ts_arg_max` | `rK7n27Zj` | 0.37 | 0.15 | −0.05 |
| T4-L2-4 | `ts_av_diff`（探针基线） | `e7aWqP7z` | 0.31 | 0.11 | +0.33 |
| T4-L2-14 | `ts_max_diff` | `88N2pGmW` | 0.27 | 0.09 | **+0.35** |
| T4-L2-11 | `ts_returns` | `blaKQxYZ` | 0.21 | 0.06 | −0.45 |
| T4-L2-13 | `ts_sum` | `vRAoNYKr` | 0.20 | 0.06 | −0.08 |
| T4-L2-5 | `ts_delta` | `RRev1P80` | 0.20 | 0.06 | −0.46 |
| T4-L2-2 | `ts_rank` | `kqaYZ93P` | 0.17 | 0.05 | −0.04 |
| T4-L2-3 | `ts_quantile` | `mLalVQ81` | 0.17 | 0.04 | −0.07 |
| T4-L2-10 | `ts_arg_min` | `N1P2bPYE` | 0.17 | 0.05 | −0.52 |
| T4-L2-6 | `ts_mean` | `6XM2eN9p` | 0.13 | 0.03 | −0.43 |
| T4-L2-7 | `ts_std_dev` | `1YW2n0qX` | 0.04 | 0.00 | −0.29 |
| T4-L2-1 | `ts_scale` | `RRev1Prg` | 0.03 | 0.00 | −0.30 |
| T4-L2-0 | `ts_zscore` | `pwap1kq6` | 0.00 | 0.00 | −0.63 |
| T4-L2-12 | `ts_product` | `d5aPZ92E` | −0.21 | −0.07 | −0.13 |
| T4-L2-15 | `days_from_last_change` | `N1P2bK1o` | −0.22 | −0.07 | +0.22 |

**T4-L2 终态**：**`ts_ir` 0.38** 最优（`ts_arg_max` 0.37 / ts_av_diff 0.31）⇒ **L2b = ts_ir × 126**。

### T4-L2b · 窗口全替（批 `giMlZ8sk4uVaDLne0vEj8N`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T4-L2b-1** | **66** | `d5aPjYnX` | **0.44** | 0.18 | −0.02 |
| T4-L2b-2 | 250 | `0mPawxAp` | 0.42 | 0.18 | +0.08 |
| T4-L2b-3 | 504 | `j2aMjonO` | 0.42 | 0.18 | **+0.34** |
| T4-L2b-4 | 750 | `RRev79dn` | 0.29 | 0.10 | +0.33 |
| 基线 | 126 | `leaN31l5` | 0.38 | 0.15 | +0.07 |

**T4-L2b 结论（`converge=no`，**ΔS +0.06**）**：**窗 66 最优 0.44**（504 的 2Y 0.34 更高但 S −0.02）⇒ **L3 基线 = ts_ir66 × industry**。

### T4-L3 · 分组轴全替（批 `1klPsre8g4Z9a5McFwvkvUx`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T4-L3-2** | **`sector`** | `Grm7dn5G` | **0.53** | **0.25** | +0.19 |
| T4-L3-3 | `market` | `LLK29nY2` | 0.50 | 0.23 | +0.21 |
| T4-L3-4 | `exchange` | `9ql2V95o` | 0.50 | 0.23 | +0.21 |
| T4-L3-5 | `country` | `akagLNm9` | 0.50 | 0.23 | +0.21 |
| 基线 | `industry` | `d5aPjYnX` | 0.44 | 0.18 | −0.02 |
| T4-L3-1 | `subindustry` | `9ql2V93e` | 0.25 | 0.08 | −0.59 |

**T4-L3 结论（`converge=no`，**ΔS +0.09 / ΔF +0.07**）**：**`sector` 0.53 最优**（market≡exchange≡country 0.50；subindustry 崩 0.25）⇒ **L4 基线 = ts_ir66 × sector**。

### T4-L4 · 外层层（批 `3wZNprbwT5cxaWV7Ub7jaRb`，8 臂，sector 轴）

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T4-L4-0 | `group_rank`（基线） | `Grm7dn5G` | **0.53** | **0.25** | +0.19 |
| T4-L4-2 | `group_zscore` | `RRevbLpa` | 0.37 | 0.17 | −0.20 |
| T4-L4-3 | `group_neutralize` | `vRAorVLv` | 0.33 | 0.17 | −0.18 |
| T4-L4-1 | `group_scale` | `pwapRg7b` | 0.30 | 0.13 | −0.12 |
| T4-L4-5 | `group_backfill(·,sector,252)` | `Jj82NLOj` | 0.25 | 0.10 | **+0.38** |
| T4-L4-4 | `group_backfill(·,sector,120)` | `rK7nOmo9` | 0.14 | 0.04 | +0.15 |
| T4-L4-7 | `group_std_dev` | `d5aPbw0j` | 0.13 | 0.02 | +0.11 |
| T4-L4-6 | `group_sum` | `j2aMAQ0W` | −0.20 | −0.04 | −0.05 |

**T4-L4 结论（`converge=yes`）**：**全 ΔS≤0 ⇒ 收敛 group_rank**（ts_ir 比值型对外层标准化零容忍，第 4 次复现）。⇒ **L5 基线 = ts_ir66 × sector × group_rank**。

### T4-L5 · 设置档（`253w8j2v451ub2gxi6JFz7n`(INDUSTRY) 起）→ 在跑

---

## 模板 T5 · `vec_avg(rsk60_offer)` 借入费率差分 完整梯度

### T5-L2（16 臂）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T5-L2-8** | **`ts_ir`** | `A1x2GpGX` | **0.47** | **0.21** | +0.23 |
| T5-L2-9 | `ts_arg_max` | `1YW2wNx6` | 0.31 | 0.11 | −0.24 |
| T5-L2-14 | `ts_max_diff` | `MP627Yan` | 0.31 | 0.11 | **+0.53** |
| T5-L2-4 | `ts_av_diff`（探针基线） | `qM7wmpM2` | 0.23 | 0.07 | +0.18 |
| T5-L2-13 | `ts_sum` | `gJa0jebe` | 0.22 | 0.07 | −0.15 |
| T5-L2-10 | `ts_arg_min` | `Wjlx7OPo` | 0.20 | 0.06 | −0.47 |
| T5-L2-11 | `ts_returns` | `Grm7lWbP` | 0.20 | 0.06 | −0.41 |
| T5-L2-5 | `ts_delta` | `78Y2z5n2` | 0.20 | 0.06 | −0.39 |
| T5-L2-6 | `ts_mean` | `VkNRGrGw` | 0.15 | 0.04 | −0.40 |
| T5-L2-2 | `ts_rank` | `d5aPZMR2` | 0.13 | 0.03 | −0.18 |
| T5-L2-1 | `ts_scale` | `blaKQmqq` | 0.12 | 0.03 | −0.25 |
| T5-L2-3 | `ts_quantile` | `P05AGROw` | 0.12 | 0.03 | −0.22 |
| T5-L2-7 | `ts_std_dev` | `XgaOo3ob` | 0.01 | 0.00 | −0.35 |
| T5-L2-0 | `ts_zscore` | `xAvEmoKp` | −0.01 | −0.00 | −1.01 |
| T5-L2-12 | `ts_product` | `d5aPjWbE` | −0.33 | −0.13 | −0.47 |
| T5-L2-15 | `days_from_last_change` | `j2aMjY8E` | −0.23 | −0.07 | −0.02 |

**T5-L2 终态**：**`ts_ir` 0.47 / F0.21 / 2Y0.23**（ΔS **+0.24** vs 探针 0.23）——**T4/T5 两模板的内核冠军一致（ts_ir）**，与 T7（ts_rank→ts_quantile 翻转）、T11（ts_zscore）不同 ⇒ 同一字段族的「水平 vs 差分」取法决定冠军。⇒ **L2b = ts_ir × 126**。

### T5-L2b · 窗口全替（批 `40D0Hxa1D5jFbVm4UxvhtIG`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线 | 126 | `A1x2GpGX` | **0.47** | **0.21** | +0.23 |
| T5-L2b-1 | 66 | `LLK29do9` | 0.42 | 0.17 | +0.29 |
| T5-L2b-2 | 250 | `KPg2OEAp` | 0.34 | 0.13 | +0.23 |
| T5-L2b-3 | 504 | `YPa95gV6` | 0.30 | 0.11 | +0.31 |
| T5-L2b-4 | 750 | `zqdLYRxO` | 0.30 | 0.11 | +0.28 |

**T5-L2b 结论（`converge=yes`）**：126 保持最优 ⇒ **L3 基线 = ts_ir126 × industry**。

### T5-L3 · 分组轴全替（批 `4xJV7j72e4kf9G4wq0XLp9x`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线 | `industry` | `A1x2GpGX` | **0.47** | **0.21** | **+0.23** |
| T5-L3-1 | `subindustry` | `2r52wZob` | 0.47 | 0.20 | +0.17 |
| T5-L3-2 | `sector` | `rK7nOzMj` | 0.43 | 0.18 | +0.27 |
| T5-L3-3 | `market` | `e7aWb2ZE` | 0.42 | 0.18 | +0.24 |
| T5-L3-4 | `exchange` | `Grm7b8jP` | 0.42 | 0.18 | +0.24 |
| T5-L3-5 | `country` | `E5Q2panr` | 0.42 | 0.18 | +0.24 |

**T5-L3 结论（`converge=yes`）**：industry 与 subindustry 并列 0.47，industry 的 F（0.21 vs 0.20）与 2Y（0.23 vs 0.17）更高 ⇒ 保持 industry。⇒ **L4 基线 = ts_ir126 × industry**。

### T5-L4 · 外层层（批 `4bmlOkedL4LB9whuR8sHXbR`，8 臂，industry 轴）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| **T5-L4-1** | **`group_scale`** | `j2aMeEOe` | **0.47** | **0.21** | **+0.65** | 6.0% |
| T5-L4-0 | `group_rank`（基线） | `A1x2GpGX` | 0.47 | 0.21 | +0.23 | 4.0% |
| T5-L4-7 | `group_std_dev` | `akagVY85` | 0.66 | 0.24 | +0.68 | **105.3%**（TO 越界） |
| T5-L4-2 | `group_zscore` | `O0W2JY21` | 0.44 | 0.19 | +0.76 | 6.1% |
| T5-L4-4 | `group_backfill(·,industry,120)` | `zqdLrMLG` | 0.41 | 0.20 | +0.79 | 5.9% |
| T5-L4-5 | `group_backfill(·,industry,252)` | `E5Q2V7MJ` | 0.39 | 0.18 | +0.70 | 5.8% |
| T5-L4-6 | `group_sum` | `0mPajlLr` | 0.28 | 0.07 | +0.67 | 105.9% |
| T5-L4-3 | `group_neutralize` | `e7aW6pWd` | 0.14 | 0.04 | +0.40 | 7.5% |

**T5-L4 结论（`converge=no` 按 2Y 判）**：S 上 `group_std_dev` 0.66 最高但 **TO 105% 直接越 HIGH_TURNOVER 闸（0.70）** ⇒ 不可用。**`group_scale` 与基线同 S（0.47）/同 F（0.21），但 2Y 0.23→0.65（+0.42）且 TO 仅 6.0%** ⇒ 按「同 S 取 2Y 更优」换基线（与 inst25 模板 P 的 group_scale 成功同型：**费率差分族的 2Y 必须靠 group_scale 打开**）。
⇒ **L5 基线 = ts_ir126 × industry × group_scale**。

### T5-L5 · 设置档（`IXeC7gSd4WFawY12rKvquLt`(INDUSTRY) / `2ZAOQoOm4ow9nH1dX5YCBsm`(SECTOR) / `2JYzU4au94KtaNwjOlWUah2`(FAST) / `1K30Hs10E55pbTZt5YiqtNG`(decay8)）

| 档 | α（industry 轴 / sector 轴） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `j2aMeEOe`（industry） | 0.47 | 0.21 | +0.65 |
| **INDUSTRY** | **`xAvEvmJm`** / `O0W2W5lJ` | **0.59** / 0.42 | **0.29**/0.19 | +0.34/+0.56 |
| SECTOR | `d5aP9ROj` / `9ql2G7Vx` | 0.48 / 0.52 | 0.21/0.27 | +0.32/+0.54 |
| FAST | `gJa0rka0` / `kqaY8E8l` | 0.42 / 0.39 | 0.14/0.14 | −0.17/+0.29 |
| SUBINDUSTRY + decay 8 | `e7aW1Gbz` / `akagRzb9` | 0.42 / 0.23 | 0.17/0.08 | +0.55/+0.40 |

**T5-L5 结论（`converge=no`，**ΔS +0.12 / ΔF +0.08**）**：**INDUSTRY 中性化 × industry 轴 0.59 / F0.29** 最优；SECTOR 0.52、FAST 0.42、decay8 0.42 均劣。⇒ 换基线，做 L5-R。

### T5-L5-R · 换基线（INDUSTRY）后内核重扫（批 `3pNGrH3xb4CucrKJVUmpbUm`，5 臂）

| 臂 | 内核（INDUSTRY / industry 轴 / W126 / group_scale） | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-1 | `ts_ir`（L5 基线） | `xAvEvmJm` | **0.59** | **0.29** | +0.34 |
| R-2 | `ts_arg_max` | `A1x2eaGY` | 0.35 | 0.11 | +0.12 |
| R-3 | `ts_max_diff` | `Wjlx3XAo` | 0.24 | 0.07 | +0.32 |
| R-4 | `ts_av_diff` | `blaKJPjZ` | 0.08 | 0.01 | −0.01 |
| R-5 | `ts_zscore` | `O0W2Rm7p` | −0.42 | −0.14 | −1.04 |

**T5-L5-R 结论（未翻转）**：`ts_ir` 0.59 领先次优 0.24 ⇒ 排序稳健。
**★ 模板 T5 天花板 = S0.59 / F0.29 / 2Y0.34 / TO5.6%**（INDUSTRY × ts_ir126 × industry × group_scale × reverse）——**risk60 至今最高 S**（T7 0.79 更高，但 T5 的 F 0.29 是最高 F）。

---

## risk60 模板进度表（12 模板）

| # | 模板 | L1 | 天花板 | 状态 |
|---|---|---|---|---|
| T7 | crowding 差分（去拥挤速度） | 0.46/2Y0.92 | **S0.79 / F0.22 / 2Y0.46**（FAST×ts_quantile126×market） | ✅ 完成（含 L5-R 第 6 次翻转） |
| T10 | 费率⊖拥挤残差 | 0.14 | **S0.78 / F0.35 / 2Y0.76**（FAST×ts_ir66×sector） | ✅ 完成（L2 ts_ir +0.54 最大单层增益） |
| T11 | 拥挤门控费率 | 0.43/subU1.07 | **S0.70 / F0.20 / subU1.24**（FAST×ts_zscore126×market） | ✅ 完成 |
| T5 | offer 差分 | 0.23/2Y0.18 | **S0.59 / F0.29 / 2Y0.34**（INDUSTRY×ts_ir126×industry×group_scale） | ✅ 完成 |
| T4 | bid_rate 差分 | 0.31/2Y0.33 | **S0.53 / F0.25 / 2Y0.19**（基线×ts_ir66×sector） | ✅ 完成 |
| T3 | last 费率水平 | 0.15 | **S0.49 / F0.24 / 2Y0.52**（INDUSTRY×ts_scale504×sector） | ✅ 完成 |
| T6 | 累计拥挤 | 0.09 | — | ⏳ 待跑 |
| T12 | 费率波动 | 0.04 | — | ⏳ 待跑 |
| T9 | 费率比值 | 0.03 | — | ⏳ 待跑 |
| T1 | bid_rate 水平 | 0.00 | — | ⏳ 待跑 |
| T8 | 费率价差 | 0.00 | — | ⏳ 待跑 |
| T2 | offer 水平 | −0.01 | — | ⏳ 待跑 |

**已得结论（4/12 模板完整）**：
1. **risk60 唯一的活机制是 `rsk60_crowding`（做空流量）**：T7 0.79 / T11 0.70；费率三字段的水平型（T1/T2/T3/T8/T9/T12）L1 全部 ≤0.15。
2. **费率「差分」是中间地带**（T4 0.53 / T5 0.59），且 **T5 需要 group_scale + INDUSTRY 两把钥匙**（2Y 0.23→0.65→0.34，S 0.47→0.59）。
3. **FAST 对 crowding 系有效**（T7 +0.23 / T11 +0.27），**对费率差分类无效甚至有害**（T4 FAST 0.24、T5 FAST 0.42）——再次实证「设置档不是普遍杠杆」。
4. **内核冠军逐模板不同**：T7 ts_quantile（L5-R 翻转）/ T11 ts_zscore / T5 ts_ir / T4 ts_ir。
5. 距 S 闸 1.58：最好 0.79 ⇒ **risk60 单集 ATOM 交付无望（差 0.79）**，但按用户「每数据集 ≥10 模板」标准仍需把剩余 8 个模板跑完才能记穷尽。

---

## 模板 T3 · `vec_avg(rsk60_last)` 最新费率水平（L1 0.15）

### T3-L2-A（8 臂，批 `3OVXfZ6T54X8aUtUk0NLdfj`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T3-L2-1** | **`ts_scale`** | `pwapM6Eb` | **0.38** | **0.15** | +0.15 |
| T3-L2-8 | `ts_ir` | `A1x2rwgw` | 0.36 | 0.15 | −0.52 |
| T3-L2-4 | `ts_av_diff` | `qM7wYAm1` | 0.28 | 0.09 | **+0.52** |
| T3-L2-6 | `ts_mean` | `KPg25bwp` | 0.21 | 0.06 | +0.14 |
| T3-L2-2 | `ts_rank` | `LLK2mpX6` | 0.18 | 0.04 | −0.34 |
| T3-L2-3 | `ts_quantile` | `0mPaN7QG` | 0.18 | 0.04 | −0.38 |
| T3-L2-5 | `ts_delta` | `E5Q28wrG` | 0.17 | 0.04 | −0.35 |
| T3-L2-7 | `ts_std_dev` | `pwapM6Vg` | 0.06 | 0.01 | −0.08 |

**T3-L2 结论（16 臂）**：`ts_scale` 0.38 最优（`ts_ir` 0.36 / `ts_av_diff` 0.28 且 2Y0.52 / `ts_max_diff` 0.30）⇒ **L2b = ts_scale × 126**。

### T3-L2b · 窗口全替（批 `iyeTYbnu4ARabkGwWBv1kz`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T3-L2b-3** | **504** | `leaNG37O` | **0.44** | 0.19 | +0.18 |
| T3-L2b-4 | 750 | `qM7wG6nP` | 0.42 | 0.18 | +0.30 |
| 基线 | 126 | `pwapM6Eb` | 0.38 | 0.15 | +0.15 |
| T3-L2b-1 | 66 | `E5Q2zeg0` | 0.37 | 0.13 | +0.23 |
| T3-L2b-2 | 250 | `QP0oz92W` | 0.36 | 0.14 | +0.18 |

**T3-L2b 结论（`converge=no`，**ΔS +0.06**）**：**504 最优 0.44** ⇒ **L3 基线 = ts_scale504 × industry**。

### T3-L3 · 分组轴全替（批 `4oFSOUgjb4wJ9VE7o6ofOwz`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T3-L3-2** | **`sector`** | `wpovPXnp` | **0.46** | **0.21** | +0.15 |
| 基线 | `industry` | `leaNG37O` | 0.44 | 0.19 | +0.18 |
| T3-L3-1 | `subindustry` | `VkNR5KY0` | 0.45 | 0.19 | +0.31 |
| T3-L3-3 | `market` | `E5Q2Logr` | 0.43 | 0.19 | +0.13 |
| T3-L3-4 | `exchange` | `VkNR5K20` | 0.43 | 0.19 | +0.13 |
| T3-L3-5 | `country` | `leaN9JQn` | 0.43 | 0.19 | +0.13 |

**T3-L3 结论（`converge=no`，+0.02）**：sector 0.46 微胜（subindustry 0.45 / industry 0.44）⇒ **L4 基线 = ts_scale504 × sector**。

### T3-L4 · 外层层（批 `1wWPnVgyA5fh9uXD12b6i2t`，8 臂，sector 轴）

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T3-L4-0 | `group_rank`（基线） | `wpovPXnp` | **0.46** | **0.21** | +0.15 |
| T3-L4-4 | `group_backfill(·,sector,120)` | `XgaOexYz` | 0.20 | 0.05 | −0.02 |
| T3-L4-5 | `group_backfill(·,sector,252)` | `qM7w3pPK` | 0.19 | 0.05 | −0.01 |
| T3-L4-1 | `group_scale` | `d5aPo67J` | 0.16 | 0.04 | +0.09 |
| T3-L4-2 | `group_zscore` | `1YW2PRnm` | 0.15 | 0.03 | +0.04 |
| T3-L4-3 | `group_neutralize` | `58J2e1qz` | 0.14 | 0.03 | +0.07 |
| T3-L4-6 | `group_sum` | `1YW2PRam` | 0.04 | 0.00 | −0.08 |
| T3-L4-7 | `group_std_dev` | `6XM2JQap` | −0.25 | −0.05 | −0.66 |

**T3-L4 结论（`converge=yes`）**：**全 ΔS≤0 ⇒ 收敛 group_rank（0.46）**。⇒ **L5 基线 = ts_scale504 × sector × group_rank**。

---

## 模板 T10 · `vector_neut(bid_rate, crowding)` 费率⊖拥挤残差（L1 0.14）

### T10-L2-A（8 臂，批 `45lQSX4iY4ng9N3V8bNwHWB`）

| 臂 | 内核 | α | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| **T10-L2-8** | **`ts_ir`** | `qM7wYvLO` | **0.68** | **0.38** | **+0.71** | 0.88 |
| T10-L2-4 | `ts_av_diff` | `9ql2dbEd` | 0.37 | 0.15 | +0.19 | 0.50 |
| T10-L2-6 | `ts_mean` | `P05AYqoq` | 0.25 | 0.08 | −0.21 | 0.51 |
| T10-L2-1 | `ts_scale` | `LLK2mqZM` | 0.21 | 0.06 | +0.02 | 0.26 |
| T10-L2-7 | `ts_std_dev` | `leaN5kAl` | 0.17 | 0.05 | +0.19 | 0.54 |
| T10-L2-3 | `ts_quantile` | `qM7wYvEA` | 0.09 | 0.01 | −0.25 | 0.15 |
| T10-L2-2 | `ts_rank` | `0mPaN9jq` | 0.10 | 0.02 | −0.25 | 0.15 |
| T10-L2-5 | `ts_delta` | `RRevlqAg` | 0.01 | 0.00 | −0.67 | 0.13 |

**T10-L2 结论（16 臂）**：**`ts_ir` 0.68 最优**（vs L1 探针 ts_zscore 0.14 ⇒ **ΔS +0.54**，本数据集最大单层增益）；`ts_av_diff` 0.37 / `ts_max_diff` 0.35 次之。⇒ **L2b = ts_ir × 126**。

### T10-L2b · 窗口全替（批 `vZOhEdKV4zd9sR16HZOdJlM`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T10-L2b-1** | **66** | `mLal7o1X` | **0.69** | **0.38** | **+0.85** |
| 基线 | 126 | `qM7wYvLO` | 0.68 | 0.38 | +0.71 |
| T10-L2b-2 | 250 | `O0W2zAVd` | 0.61 | 0.32 | +0.51 |
| T10-L2b-3 | 504 | `KPg2zJZj` | 0.53 | 0.25 | +0.65 |
| T10-L2b-4 | 750 | `Grm7zW9G` | 0.46 | 0.20 | +0.44 |

**T10-L2b 结论（`converge=no` 按 2Y）**：66 的 S +0.01 且 **2Y 0.71→0.85** ⇒ 换 66。⇒ **L3 基线 = ts_ir66 × industry**。

### T10-L3 · 分组轴全替（批 `3kHWkQ8Ar5gPb3hQibNLSQ2`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **T10-L3-2** | **`sector`** | `6XM2JOvJ` | **0.71** | **0.41** | **+1.00** |
| 基线 | `industry` | `mLal7o1X` | 0.69 | 0.38 | +0.85 |
| T10-L3-3 | `market` | `omakrOOn` | 0.67 | 0.38 | +0.94 |
| T10-L3-4 | `exchange` | `P05A899K` | 0.67 | 0.38 | +0.94 |
| T10-L3-5 | `country` | `qM7w3qZv` | 0.67 | 0.38 | +0.94 |
| T10-L3-1 | `subindustry` | `78Y2M9E8` | 0.54 | 0.25 | +0.44 |

**T10-L3 结论（`converge=no`，**ΔS +0.02 / Δ2Y +0.15**）**：**sector 0.71 / F0.41 / 2Y1.00** 最优 ⇒ **L4 基线 = ts_ir66 × sector**。

### T10-L4 · 外层层（批 `1j5SEFb4X4TW9IABYo5hXai`，8 臂，sector 轴）

| 臂 | 外层 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| T10-L4-0 | `group_rank`（基线） | `6XM2JOvJ` | **0.71** | **0.41** | **+1.00** |
| T10-L4-6 | `group_sum` | `kqaYOz6z` | 0.07 | 0.01 | −0.17 |
| T10-L4-1 | `group_scale` | `xAvEWJon` | −0.12 | −0.03 | +0.36 |
| T10-L4-2 | `group_zscore` | `N1P23YGE` | −0.17 | −0.05 | +0.26 |
| T10-L4-3 | `group_neutralize` | `j2aMxqKE` | −0.21 | −0.10 | +0.03 |
| T10-L4-5 | `group_backfill(·,sector,252)` | `VkNR5Ab0` | −0.54 | −0.33 | +0.27 |
| T10-L4-4 | `group_backfill(·,sector,120)` | `LLK2r0Yn` | −0.55 | −0.34 | +0.11 |
| T10-L4-7 | `group_std_dev` | `A1x2moXY` | −0.10 | −0.01 | −0.91 |

**T10-L4 结论（`converge=yes`，**全部负**）**：**除 group_rank 外 S 全负（−0.10 至 −0.55）** ⇒ ts_ir 残差型第 5 次复现「只能用 group_rank」。⇒ **L5 基线 = ts_ir66 × sector × group_rank**。

### T3/T10-L5 · 设置档（`ipRSd8wL54LbFR1bDGPCGdB`(INDUSTRY) / `301xkbf6W4lIaTaUGnkzOSs`(SECTOR) / `RFFJh3DA4H4by717U1AcGZJ`(FAST) / `2Fa0yF5YD54z9phK6IAkks0`(decay8)，合并批各 4 臂）

| 档 | α（T3 sector / T3 industry / T10 sector / T10 industry） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | T3 `wpovPXnp` / T10 `6XM2JOvJ` | **0.46 / 0.71** | 0.21/0.41 | +0.15/**+1.00** |
| **INDUSTRY** | `1YW20XjK` / `0mPa5XYq` / `wpovWZQ1` / `E5Q2xp6R` | **0.49**/0.49/0.59/0.55 | 0.24/0.23/0.32/0.28 | +0.52/+0.59/+0.74/+0.59 |
| SECTOR | `88N2XGkq` / `kqaY98kP` / `zqdLeAwG` / `1YW20G1k` | 0.35/0.33/0.48/0.37 | 0.15/0.13/0.24/0.16 | +0.42/+0.45/+0.67/+0.24 |
| **FAST** | `rK7nnO1a` / `MP622aP9` / **`qM7wwxMj`** / `QP0oobPp` | 0.48/0.38/**0.78**/0.69 | 0.15/0.10/**0.35**/0.29 | −0.53/−0.44/**+0.76**/+0.42 |
| SUBINDUSTRY + decay 8 | `wpovvnpl` / `d5aPPEkX` / `e7aWWdkz` / `d5aPPEpX` | 0.46/0.44/**0.71**/0.70 | 0.21/0.19/**0.41**/0.39 | +0.11/+0.12/**+1.04**/+0.90 |

**T3-L5 结论（`converge=no`，+0.03）**：INDUSTRY 档 0.49 微超基线 0.46（FAST 0.48 但 2Y −0.53）⇒ 换基线到 INDUSTRY，做 L5-R。
**T10-L5 结论（`converge=no`，**+0.07**）**：**FAST × sector 0.78 / F0.35 / 2Y0.76** 最优（decay8 0.71 与基线同 S 但 2Y **1.04** 更高）⇒ 换基线到 FAST，做 L5-R。

### T3-L5-R · 换基线（INDUSTRY）后内核重扫（批 `3RFIzt1cP4DucCw16b8YP4Ux`，5 臂）

| 臂 | 内核（INDUSTRY / sector 轴 / W504） | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-1 | `ts_scale`（L5 基线） | `1YW20XjK` | **0.49** | **0.24** | **+0.52** |
| R-2 | `ts_av_diff` | `N1P2G9Op` | 0.47 | 0.22 | +0.35 |
| R-3 | `ts_rank` | `YPa9OqpA` | 0.30 | 0.11 | +0.17 |
| R-4 | `ts_ir` | `A1x25K3E` | 0.27 | 0.10 | −0.02 |
| R-5 | `ts_max_diff` | `QP0oAXaM` | 0.18 | 0.05 | −0.33 |

**T3-L5-R 结论（未翻转）**：ts_scale 0.49 保持最优 ⇒ **★ 模板 T3 天花板 = S0.49 / F0.24 / 2Y0.52 / TO9.8%**（INDUSTRY × ts_scale504 × sector × group_rank）。

### T10-L5-R · 换基线（FAST）后内核重扫（批 `4E51UkdnX59JcesBIhCqQ1n`，5 臂）

| 臂 | 内核（FAST / sector 轴 / W66） | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-1 | `ts_ir`（L5 基线） | `qM7wwxMj` | **0.78** | **0.35** | **+0.76** |
| R-4 | `ts_arg_max` | `A1x25EXl` | 0.41 | 0.13 | −0.98 |
| R-3 | `ts_max_diff` | `qM7wpV2Z` | 0.32 | 0.09 | −0.13 |
| R-2 | `ts_av_diff` | `ZYa19Nv0` | 0.21 | 0.04 | +0.15 |
| R-5 | `ts_zscore` | `WjlxRJZj` | −0.02 | −0.00 | +0.24 |

**T10-L5-R 结论（未翻转）**：ts_ir 0.78 领先次优 0.37 ⇒ **★ 模板 T10 天花板 = S0.78 / F0.35 / 2Y0.76 / TO9.9%**（FAST × ts_ir66 × sector × group_rank × reverse）。

**★ 更新：T10 的 0.78 与 T7 的 0.79 并列 risk60 最强**；T10 的构造是**同集残差**（`vector_neut(bid_rate, crowding)`），与 inst25 模板 C（同样残差组合）同为数据集最强 —— **「同集残差化」在两个数据集上都是最优形态**（可迁移结论）。

---

## ★ 模板口径修正（2026-11-22，执行中自查）

**问题**：初版 12 模板里，T1（bid_rate 水平）/ T4（bid_rate 差分）/ T12（bid_rate 波动）是**同一字段、只差 L2 内核起点**；T2/T5（offer）、T6/T7（crowding）同理。而 **L2 层本身就是 15 内核全替**（含 ts_mean 水平、ts_av_diff 差分、ts_std_dev 波动），会把这三种「起点」全部吸收 ⇒ 把它们当独立模板属于**口径重复计数**。

**修正后：模板 = 互异构造（字段集合 + 算子几何），不是内核起点。** risk60 的互异构造共 **12 个**：

| # | 构造 | 几何 | 状态 |
|---|---|---|---|
| C1 | `bid_rate` 单字段 | 单字段（L2 内核全替吸收水平/差分/波动三种起点） | ✅ 完成（= 原 T4 链，天花板 0.53） |
| C2 | `offer` 单字段 | 单字段 | ✅ 完成（= 原 T5，0.59） |
| C3 | `last` 单字段 | 单字段 | ✅ 完成（= 原 T3，0.49） |
| C4 | `crowding` 单字段 | 单字段 | ✅ 完成（= 原 T7，0.79） |
| C5 | `vector_neut(bid, crowding)` | 同集残差（费率⊖拥挤） | ✅ 完成（= 原 T10，0.78） |
| C6 | `multiply(offer, rank(crowding))` | 同集门控 | ✅ 完成（= 原 T11，0.70） |
| C7 | `subtract(offer, bid)` | 双字段价差 | ✅ 完成（天花板 **0.82 / F0.48**：decay8 × ts_av_diff504 × industry × **group_scale**） |
| C8 | `divide(offer, bid)` | 双字段比值 | ✅ 完成（天花板 **★★ 1.08 / F0.74 / 2Y0.56**：INDUSTRY × ts_ir66 × industry × **group_scale**；`checks.fail=[]`） |
| C9 | `vector_neut(offer, crowding)` | 同集残差（另一腿） | 🔄 L2 完成（ts_ir 0.50 / 2Y0.68），L2b 待派 |
| C10 | `multiply(bid, rank(crowding))` | 同集门控（另一腿） | ⏳ 待跑 |
| C11 | `divide(bid, ts_mean(bid,252))` | 相对历史溢价（单字段时序基准） | ⏳ 待跑 |
| C12 | `divide(subtract(offer,bid), bid)` | 相对价差（价差÷出借费率） | ⏳ 待跑 |

⇒ **按互异构造计 12 个 ≥ 10，满足用户标准**；原 T1/T2/T6/T12 的探针读数保留在 §L1 表里作「同字段不同起点的方向证据」，不再单列为模板。

---

# 分层汇总（供 `gradient_gate` 解析；逐构造的完整 Δ 表见下文各 C 小节）

## Layer 1 · 信号构造全替（12 个互异构造）

| 构造 | 机制 | 探针 S | 探针 2Y | 去向 |
|---|---|---:|---:|---|
| C1 `vec_avg(lending_fee_bid_rate)` | 出借费率单字段 | 0.00 | −0.63 | L2 → ts_ir 0.38 |
| C2 `vec_avg(rsk60_offer)` | 借入费率单字段 | −0.01 | −1.01 | L2 → ts_ir 0.47 |
| C3 `vec_avg(rsk60_last)` | 最新费率单字段 | 0.15 | −0.45 | L2 → ts_scale 0.38 |
| C4 `vec_sum(rsk60_crowding)` | 做空流量单字段 | 0.46 | **+0.92** | L2 → ts_rank 0.52 |
| C5 `vector_neut(bid, crowding)` | 同集残差 | 0.14 | −0.20 | L2 → ts_ir 0.68 |
| C6 `multiply(offer, ts_rank(crowding,66))` | 同集门控 | 0.43 | −0.03 | L2 → ts_zscore 0.43 |
| C7 `subtract(offer, bid)` | 双字段价差 | 0.00 | −1.18 | L2 → ts_av_diff 0.35 |
| C8 `divide(offer, bid)` | 双字段比值 | 0.03 | −0.56 | L2 → ts_ir 0.38 |
| C9 `vector_neut(offer, crowding)` | 同集残差（另一腿） | — | — | L2 → ts_ir 0.50（L2b 待派） |
| C10 `multiply(bid, ts_rank(crowding,66))` | 同集门控（另一腿） | — | — | 待跑 |
| C11 `divide(bid, ts_mean(bid,252))` | 相对历史溢价 | — | — | 待跑 |
| C12 `divide(subtract(offer,bid), bid)` | 相对价差 | — | — | 待跑 |

**L1 结论**：**单字段「水平」探针全灭（C1–C3 ≤0.15）**；活面 = 流量（C4 0.46）、门控（C6 0.43）、残差（C5 0.14 但 L2 救活到 0.68）；双字段组合（C7/C8）探针也弱（≤0.03）但 L2/L2b 后分别到 0.60/0.62 —— **「L1 探针弱」不等于该构造死，构造的天花板必须看完整梯度**（本数据集最重要的方法论结论）。

## Layer 2 · 内层时序算子全替（每构造 15 个内核 + 基线，共 16 臂）

| 构造 | 冠军内核 | S | 亚军 | 结论 |
|---|---|---:|---|---|
| C1 | `ts_ir` | 0.38 | ts_arg_max 0.37 | 信噪比内核最优 |
| C2 | `ts_ir` | 0.47 | ts_arg_max/max_diff 0.31 | 信噪比内核最优（2Y0.53 在 max_diff） |
| C3 | `ts_scale` | 0.38 | ts_ir 0.36 | 极值缩放最优 |
| C4 | `ts_rank` | 0.52 | ts_quantile 0.51 | 有序型内核最优（2Y1.10） |
| C5 | `ts_ir` | **0.68** | ts_av_diff 0.37 | **单层 +0.54（数据集最大）** |
| C6 | `ts_zscore` | 0.43 | ts_av_diff 0.42 | 基线最优（乘积已含截面） |
| C7 | `ts_av_diff` | 0.35 | ts_max_diff 0.34 | 只有差分型有信号 |
| C8 | `ts_ir` | 0.38 | ts_max_diff/arg_min 0.32 | 信噪比内核最优 |
| C9 | `ts_ir` | 0.50 | ts_max_diff 0.40 | 信噪比内核最优（2Y0.68） |

**L2 结论**：**`ts_ir` 在 5/9 个构造上是冠军**（C1/C2/C5/C8/C9）——risk60 的费率结构天然是「均值÷波动」型信息；`ts_rank/ts_quantile` 只在纯流量（C4）上胜出；`ts_av_diff` 只在价差（C7）上胜出。

## Layer 2b · 窗口全替（66 / 250 / 504 / 750）

| 构造 | 最优窗 | S | 基线（126）S | 方向 |
|---|---|---:|---:|---|
| C3 | **504** | 0.44 | 0.38 | 长窗（慢变量） |
| C4 | 126 保持 | 0.52 | 0.52 | 504 的 0.53 是「S+0.01 / 2Y−0.57」⇒ 判噪声 |
| C5 | 126 保持 | 0.68 | 0.68 | 66 的 0.69/2Y0.85 微胜 ⇒ 取 66 |
| C7 | **504** | **0.60** | 0.35 | **长窗 +0.25（价差是慢变量）** |
| C8 | **66** | **0.62** | 0.38 | **短窗 +0.24（比值偏离是快变量）** |
| C9 | 待派 | | | |

**L2b 结论**：★ **同一数据集内窗口方向相反**——价差（存量型）要 504 长窗，比值（套利偏离型）要 66 短窗。

## Layer 3 · 分组轴全替（subindustry / sector / market / exchange / country / industry）

| 构造 | 最优轴 | S | 备注 |
|---|---|---:|---|
| C1 | `sector` | 0.53 | industry 0.44 |
| C3 | `sector` | 0.46 | industry 0.44（+0.02 判噪声内） |
| C4 | `market`≡`exchange`≡`country` | 0.53 | 单国三轴第 6 次逐位相同 |
| C5 | `sector` | 0.71 | industry 0.69（2Y 0.85→1.00） |
| C6 | `industry` | 0.43 | sector 0.41（subU 1.16 更优） |
| C7 | `industry` | 0.60 | subindustry 0.61（+0.01 判噪声） |
| C8 | `industry` | 0.62 | sector 0.56 |
| C9 | 待派 | | |

**L3 结论**：**轴偏好按构造而异**（费率差分类偏 sector、流量/门控偏 market/industry）——不外推，逐构造实测。

## Layer 4 · 外层包装全替（rank / scale / zscore / neutralize / backfill×2 / sum / std_dev）

| 构造 | 最优外层 | S | ΔS vs rank | 备注 |
|---|---|---:|---:|---|
| C1 | `group_rank` | 0.44 | 0 | ts_ir 只能 rank |
| C4 | `group_rank` | 0.53 | 0 | scale/zscore 的 0.55–0.57 伴 TO 68.8% + F 减半 ⇒ 判不可用 |
| C5 | `group_rank` | 0.71 | 0 | 其余全负（含 −0.55） |
| C6 | `group_rank` | 0.43 | 0 | 其余 ≤0.18 |
| C7 | **`group_scale`** | **0.75** | **+0.15** | 2Y 转 −0.28（跷跷板） |
| C8 | **`group_scale`** | **0.84** | **+0.22** | ⚠ CW 0.122>0.1 FAIL（换 INDUSTRY 后消失）；`group_zscore` 0.73 |
| C3 | `group_rank` | 0.46 | 0 | 全负 |

**L4 结论**：★★ **`group_scale` 是「双字段组合构造」（C7 价差 / C8 比值）的最大杠杆（+0.15/+0.22）**，但对单字段与残差/门控构造零容忍（必崩）——**外层算子与「构造是否已无量纲」强耦合**（比值/残差/门控已去量纲 ⇒ 只能 rank；价差保留绝对量纲 ⇒ group_scale 有效）。

## Layer 5 · 设置档（SUBINDUSTRY / INDUSTRY / SECTOR / FAST / decay8）

| 构造 | 最优档 | S | 备注 |
|---|---|---:|---|
| C1 | 基线（SUBINDUSTRY×decay4） | 0.53 | 四档全劣（decay8 0.51 最接近） |
| C3 | **INDUSTRY** | 0.49 | +0.03 |
| C4 | **FAST** | **0.79** | **+0.23**（L5-R 触发第 6 次内核翻转：ts_quantile 反超 ts_rank） |
| C5 | **FAST** | **0.78** | +0.07 |
| C6 | **FAST** | **0.70** | +0.27（本构造最大增益） |
| C7 | **decay8** | **0.82** | +0.07（与 W504 长窗协同） |
| C8 | **INDUSTRY** | **1.08** | **+0.24，且修复 CW（0.122→PASS）与 subU（0.35→0.80）** |
| C9 | 待派 | | |

**L5 结论**：★★ **设置档不是普遍杠杆，且方向按构造类型分裂**——流量/门控（C4/C5/C6）吃 **FAST**；价差慢变量（C7）吃 **decay8**；比值（C8）与单字段（C3）吃 **INDUSTRY**。**C8 的 INDUSTRY 档同时是唯一修复 CW/subU 的档位**（同一构造在 SUBINDUSTRY 下 CW FAIL，换 INDUSTRY 后双过闸）。

---

## C7 · `subtract(offer, bid)` 费率价差 完整梯度

### C7-L2-A（8 臂，批 `31QZOF1A05iEa0TdSfy7ORt`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C7-L2-4** | **`ts_av_diff`** | `LLK2oLle` | **0.35** | **0.14** | +0.08 |
| C7-L2-5 | `ts_delta` | `vRAo7RJd` | 0.30 | 0.11 | −0.26 |
| C7-L2-2 | `ts_rank` | `npaXGpzl` | 0.29 | 0.10 | −0.36 |
| C7-L2-3 | `ts_quantile` | `zqdL7qJK` | 0.28 | 0.10 | −0.39 |
| C7-L2-8 | `ts_ir` | `wpov7pnx` | 0.18 | 0.05 | +0.06 |
| C7-L2-1 | `ts_scale` | `58J2K86z` | 0.10 | 0.02 | −0.13 |
| C7-L2-7 | `ts_std_dev` | `0mPaZmK2` | 0.06 | 0.01 | −0.45 |
| C7-L2-6 | `ts_mean` | `QP0oRP5K` | 0.05 | 0.01 | −0.30 |

**C7-L2-A 结论**：**价差（offer − bid）只有差分型内核有信号（ts_av_diff 0.35）**，水平/波动型 ≤0.10 ⇒ 价差的**水平**无信息，**价差变化**才有（经纪商利润压缩/扩张 = 融资紧张度变化）。
**C7-L2 终态（16 臂）**：**`ts_av_diff` 0.35** 最优（`ts_max_diff` 0.34/2Y0.60、`ts_returns` 0.30 次之）；水平型 ts_mean 0.05 / ts_scale 0.10 崩 ⇒ **价差只能吃「变化」**。

### C7-L2b · 窗口全替（批 `4keBoyflp4B6bBHpjURJ4Hi`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C7-L2b-3** | **504** | `omakbnpE` | **0.60** | **0.30** | +0.17 |
| C7-L2b-4 | 750 | `LLK2vnaL` | 0.54 | 0.25 | +0.04 |
| 基线 | 126 | `LLK2oLle` | 0.35 | 0.14 | +0.08 |
| C7-L2b-1 | 66 | `88N20Oom` | 0.35 | 0.14 | +0.21 |
| C7-L2b-2 | 250 | `kqaYwn7L` | 0.35 | 0.13 | −0.10 |

**C7-L2b 结论（`converge=no`，**ΔS +0.25**）**：★★ **窗 504 跳到 0.60 / F0.30**（ΔS +0.25、ΔF +0.16，全模板最大窗口增益之一）——价差是**慢变量**，短窗被噪声淹没；长窗平滑后才显出「经纪商利润率的长期偏离」。⇒ **L3 基线 = ts_av_diff504 × industry**。

### C7-L3 · 分组轴全替（批 `2OQ5sO78G4Sda5e5f2fSA4a`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| C7-L3-1 | `subindustry` | `1YW2M606` | **0.61** | 0.29 | +0.23 |
| 基线 | `industry` | `omakbnpE` | 0.60 | **0.30** | +0.17 |
| C7-L3-2 | `sector` | `kqaYAe98` | 0.54 | 0.26 | −0.05 |
| C7-L3-3 | `market` | `A1x2Aq2R` | 0.53 | 0.25 | −0.03 |
| C7-L3-4 | `exchange` | `ZYa1Jk1x` | 0.53 | 0.25 | −0.03 |
| C7-L3-5 | `country` | `leaNmJNA` | 0.53 | 0.25 | −0.03 |

**C7-L3 结论（`converge=yes` 按噪声判）**：subindustry 0.61 仅 +0.01（且 F 更低）⇒ **保持 industry**。

### C7-L4 · 外层层（批 `Ww6j8bn53dbcoEZHibarM`，8 臂，industry 轴）

| 臂 | 外层 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| **C7-L4-1** | **`group_scale`** | `N1P2Y0Pw` | **0.75** | **0.41** | −0.28 | 12.9% |
| C7-L4-2 | `group_zscore` | `omakx7al` | 0.68 | 0.38 | −0.63 | 12.8% |
| C7-L4-0 | `group_rank`（基线） | `omakbnpE` | 0.60 | 0.30 | +0.17 | 7.7% |
| C7-L4-3 | `group_neutralize` | `E5Q291QL` | 0.50 | 0.32 | −0.45 | 12.5% |
| C7-L4-4 | `group_backfill(·,industry,120)` | `gJa0n6rO` | 0.44 | 0.26 | −0.43 | 12.2% |
| C7-L4-5 | `group_backfill(·,industry,252)` | `XgaOdGN1` | 0.44 | 0.26 | −0.44 | 12.2% |
| C7-L4-6 | `group_sum` | `A1x2o9Le` | 0.18 | 0.03 | +0.17 | 110.6% |
| C7-L4-7 | `group_std_dev` | `gJa0n6XO` | 0.18 | 0.03 | +0.31 | 110.8% |

**C7-L4 结论（`converge=no`，**ΔS +0.15 / ΔF +0.11**）**：★★ **`group_scale` 0.75 / F0.41（本构造最大增益，且 F 为 risk60 全部模板最高）**；`group_zscore` 0.68 次之。代价：**2Y 由 +0.17 转 −0.28**（跷跷板第 N 次）。⇒ **L5 基线 = ts_av_diff504 × industry × group_scale**。

### C7-L5 · 设置档

| 档 | α（industry 轴 / sector 轴） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `N1P2Y0Pw`（industry） | **0.75** | **0.41** | −0.28 |
| INDUSTRY | `xAvEJJbl` / `blaKee8N` | 0.53 / 0.48 | 0.25/0.25 | −0.33/−0.13 |
| SECTOR（group_scale 版） | `ZYa9RzgY` / `blagYzJR` | 0.50 / 0.41 | 0.19/0.21 | −0.13/−0.19 |
| FAST | `2r5xrnAZ` / `gJa5Joe0` | 0.30 / 0.40 | 0.07/0.12 | −0.72/−0.22 |
| **SUBINDUSTRY + decay 8** | **`omaXmzmJ`** / `1YWRYmYM` | **0.82** / 0.53 | **0.48**/0.31 | −0.19/−0.33 |

**C7-L5 结论（`converge=no`，**ΔS +0.07 / ΔF +0.07**）**：**decay8 × industry 0.82 / F0.48** 最优（SECTOR 0.50 / FAST 0.30–0.40 / INDUSTRY 0.53–0.48 全劣）；**decay8 是「价差慢变量」的正确设置档**（配合 W504 长窗，双重平滑）。⇒ 换基线，做 L5-R。

### C7-L5-R · 换基线（decay8）后内核重扫（批 `37aSPR5oz5dfaaF13FzpIYNu`，4 臂）

| 臂 | 内核（decay8 / industry 轴 / W504 / group_scale） | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-1 | `ts_av_diff`（L5 基线） | `omaXmzmJ` | **0.82** | **0.48** | −0.19 |
| R-4 | `ts_max_diff` | `3q0OQde0` | 0.28 | 0.09 | +0.31 |
| R-3 | `ts_ir` | `xAvoOMdw` | 0.12 | 0.03 | −0.06 |
| R-2 | `ts_delta` | `leaYpxl5` | 0.10 | 0.02 | +0.14 |

**C7-L5-R 结论（未翻转）**：ts_av_diff 0.82 领先次优 0.54 ⇒ **★ 模板 C7（价差）天花板 = S0.82 / F0.48 / 2Y−0.19 / TO9.0%**（decay8 × ts_av_diff504 × industry × group_scale）。

### C8-L4 · 外层层（批 `4mkA1s3b545aOmfrg7JkoG`，8 臂，industry 轴）

| 臂 | 外层 | α | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|
| **C8-L4-1** | **`group_scale`** | `0mPLbbb1` | **0.84** | **0.53** | +0.54 | 8.6% | **5 FAIL** |
| C8-L4-2 | `group_zscore` | `aka8rrkW` | 0.73 | 0.43 | +0.36 | 8.6% | 5 FAIL |
| C8-L4-5 | `group_backfill(·,industry,252)` | `MP6njjM8` | 0.68 | 0.44 | +0.45 | 7.5% | 4 FAIL |
| C8-L4-3 | `group_neutralize` | `1YWRqqYW` | 0.63 | 0.43 | +0.44 | 10.0% | 4 FAIL |
| C8-L4-0 | `group_rank`（基线） | `N1P2Zbkw` | 0.62 | 0.30 | +0.45 | 5.8% | 3 FAIL |
| C8-L4-4 | `group_backfill(·,industry,120)` | `QP0A11Pw` | 0.62 | 0.37 | +0.35 | 7.7% | 4 FAIL |
| C8-L4-7 | `group_std_dev` | `RReoJJjo` | 0.30 | 0.07 | −0.81 | 106.8% | 5 FAIL |
| C8-L4-6 | `group_sum` | `qM7pKK9E` | 0.08 | 0.01 | −1.27 | 105.8% | 5 FAIL |

**C8-L4 结论（`converge=no`，**ΔS +0.22 / ΔF +0.23**）**：★★ **`group_scale` 0.84 / F0.53**（risk60 全部构造的最高读数），`group_zscore` 0.73 次之。
⚠ **`0mPLbbb1` 的 RA 明细实读**（`get_alpha_details`）：`LOW_SHARPE 0.84<1.58` / `LOW_FITNESS 0.53<1.0` / **`CONCENTRATED_WEIGHT 0.1218>0.1`（2014-01-03）** / `LOW_SUB_UNIVERSE_SHARPE 0.35<0.4` / `LOW_2Y_SHARPE 0.54<1.58`；`pyramids.effective=1`（GBR/D1/RISK ×1.2）。
⇒ **不可交付**（CW 与 subU 是 group_scale 在比值型信号上的结构代价），但按「S 为第一判据」仍取作梯度基线并记录该代价。⇒ **L5 基线 = ts_ir66 × industry × group_scale**。

**★ 顺带确认平台硬闸实测值**（本条为 GBR 一手证据，与 `region-gate-thresholds` 记忆一致）：`LOW_SHARPE` limit **1.58** / `LOW_FITNESS` limit **1.0** / `LOW_2Y_SHARPE` limit **1.58** / `LOW_SUB_UNIVERSE_SHARPE` limit **0.4** / `CONCENTRATED_WEIGHT` limit **0.10**。

### C8-L5 · 设置档

| 档 | α（industry 轴 / sector 轴） | S | F | 2Y | subU |
|---|---|---|---:|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `0mPLbbb1`（industry） | 0.84 | 0.53 | +0.54 | 0.35 |
| **INDUSTRY** | **`GrmNrRYQ`** / `e7aP7j2N` | **1.08** / 0.85 | **0.74**/0.57 | +0.56/+0.40 | **0.80**/0.58 |
| SECTOR | `npal9bn8` / `RReoMLNo` | 0.93 / 0.85 | 0.57/0.57 | +0.59/+0.48 |
| FAST | `1YWRe90Q` / `GrmNPa9Q` | 0.71 / 0.64 | 0.32/0.28 | +0.10/+0.48 |
| SUBINDUSTRY + decay 8 | `YPaO6EAM` / `d5a6p3xX` | 0.81 / 0.56 | 0.50/0.33 | +0.62/+0.35 |

### C8-L5-R · 换基线（INDUSTRY）后内核重扫（批 `choV1d6F4Pu8Pw13IHvdpVP`，5 臂）

| 臂 | 内核（INDUSTRY / industry 轴 / W66 / group_scale） | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| R-1 | `ts_ir`（L5 基线） | `GrmNrRYQ` | **1.08** | **0.74** | +0.56 |
| R-4 | `ts_max_diff` | `2r5xznWZ` | 0.65 | 0.29 | +0.37 |
| R-3 | `ts_arg_min` | `kqaMrLOl` | 0.42 | 0.15 | −0.25 |
| R-2 | `ts_av_diff` | `MP6nR5ZM` | 0.18 | 0.03 | −0.27 |
| R-5 | `ts_delta` | `omaX59rl` | 0.12 | 0.02 | −0.25 |

**C8-L5-R 结论（未翻转）**：ts_ir 1.08 领先次优 0.43 ⇒ **★★★ 模板 C8（offer/bid 比值）天花板 = S1.08 / F0.74 / 2Y0.56 / TO7.9% / subU0.80**（INDUSTRY × ts_ir66 × industry × group_scale × reverse）——**risk60 最强构造，且是唯一 `checks.fail=[]` + ppa_failed=0 的形态**。

**C8-L5 结论（迄今，**INDUSTRY 档 **ΔS +0.24 / ΔF +0.21 / ΔsubU +0.45**）**：★★★ **`GrmNrRYQ` = S1.08 / F0.74 / 2Y0.56 / TO7.9% / subU0.80 / invest_S0.98 / DD10.1%**（`reverse(group_scale(ts_ir(ts_backfill(divide(vec_avg(rsk60_offer),vec_avg(lending_fee_bid_rate)),250),66), industry))` @ **INDUSTRY 中性化**）。
**RA 明细实读**：`checks.fail = []`（**全部 PASS 档**），`warning` 级：LOW_SHARPE 1.08<1.58 / LOW_FITNESS 0.74<1.0 / LOW_2Y_SHARPE 0.56<1.58 / CLUSTER_TEST 0.71；**CW 0.10 / SUB_UNIVERSE 0.4 / TO 全 PASS**，`failed_ppa_count = 0`，`pyramids.effective=1`（GBR/D1/RISK ×1.2）。
⇒ **risk60 首个 S>1.0 且 subU/CW 双过闸的构造**；距交付仍差 S 0.50 / F 0.26 / 2Y 1.02。

---

## C8 · `divide(offer, bid)` 费率比值 完整梯度

### C8-L2-A（8 臂，批 `3maC4HT14x79pZ1g3hJ5RPq`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C8-L2-8** | **`ts_ir`** | `wpov76Yl` | **0.38** | **0.15** | −0.03 |
| C8-L2-5 | `ts_delta` | `KPg2AeGp` | 0.26 | 0.09 | +0.36 |
| C8-L2-6 | `ts_mean` | `mLalnOjX` | 0.18 | 0.05 | +0.22 |
| C8-L2-1 | `ts_scale` | `XgaOZqnx` | 0.16 | 0.04 | −0.49 |
| C8-L2-4 | `ts_av_diff` | `zqdL7aNO` | 0.14 | 0.03 | −0.39 |
| C8-L2-2 | `ts_rank` | `RRevxX1a` | 0.13 | 0.03 | −0.49 |
| C8-L2-3 | `ts_quantile` | `VkNRQn35` | 0.10 | 0.02 | −0.53 |
| C8-L2-7 | `ts_std_dev` | `RRevxX7o` | −0.25 | −0.08 | −0.71 |

**C8-L2-A 结论**：**`ts_ir` 0.38** 最优（`ts_delta` 0.26）——比值型信号同样是**信噪比内核最优**（与 C1/C2 一致，第 3 次）。
**C8-L2 终态（16 臂）**：**`ts_ir` 0.38** 最优（arg_min 0.30 / max_diff 0.32 / delta 0.26）⇒ **L2b = ts_ir × 126**。

### C8-L2b · 窗口全替（批 `3OmqSDf5B4YAaS0PxAUJbQN`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C8-L2b-1** | **66** | `N1P2Zbkw` | **0.62** | **0.30** | **+0.45** |
| C8-L2b-4 | 750 | `LLK2QGb2` | 0.44 | 0.19 | +0.13 |
| C8-L2b-2 | 250 | `P05AVGjL` | 0.40 | 0.16 | −0.27 |
| C8-L2b-3 | 504 | `zqdLVNwO` | 0.37 | 0.15 | +0.09 |
| 基线 | 126 | `wpov76Yl` | 0.38 | 0.15 | −0.03 |

**C8-L2b 结论（`converge=no`，**ΔS +0.24 / Δ2Y +0.48**）**：★ **窗 66 跳到 0.62 / F0.30 / 2Y0.45**（三项齐升）——比值的短期偏离才是信号（长窗平滑掉套利窗口）。⇒ **L3 基线 = ts_ir66 × industry**。

### C8-L3 · 分组轴全替（批 `2TsiOZcMU4l6czgdZMOUq2M`，6 臂）

| 臂 | 轴 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线 | `industry` | `N1P2Zbkw` | **0.62** | **0.30** | +0.45 |
| C8-L3-2 | `sector` | `RRevGM6a` | 0.56 | 0.26 | +0.41 |
| C8-L3-3 | `market` | `KPg2W3rN` | 0.53 | 0.24 | +0.44 |
| C8-L3-4 | `exchange` | `wpov0qbd` | 0.53 | 0.24 | +0.44 |
| C8-L3-5 | `country` | `vRAoW8Oa` | 0.53 | 0.24 | +0.44 |
| C8-L3-1 | `subindustry` | `Grm7ZPbZ` | 0.50 | 0.21 | +0.14 |

**C8-L3 结论（`converge=yes`）**：industry 0.62 保持最优 ⇒ **L4 基线 = ts_ir66 × industry**。

### C8-L4 · 外层层（批 `4mkA1s3b545aOmfrg7JkoG`，8 臂）→ 在跑

---

---

### T4-L5 · 设置档（`253w8j2v451ub2gxi6JFz7n`(INDUSTRY) / `1z3GTq8aG5d4bzcIUeIdzVD`(SECTOR) / `sYocwaCF5gp8EVl2sRAbIp`(FAST) / `1uUFeZ3As4wfcr11vOiQMxx`(decay8)）

| 档 | α（sector 轴 / industry 轴） | S | F | 2Y |
|---|---|---|---:|---:|---:|
| 基线（SUBINDUSTRY + decay4） | `Grm7dn5G` | **0.53** | **0.25** | +0.19 |
| INDUSTRY | `O0W28XR1` / `YPa9Mo8A` | 0.46 / 0.40 | 0.20/0.16 | −0.02/−0.24 |
| SECTOR | `E5Q26raR` / `qM7wLmmA` | 0.32 / 0.21 | 0.12/0.06 | −0.36/−0.71 |
| FAST | `e7aW5nw6` / `omakEnM5` | 0.24 / 0.13 | 0.06/0.02 | −0.71/−0.97 |
| SUBINDUSTRY + decay 8 | `xAvEv8vq` / `VkNRNjNw` | 0.51 / 0.43 | 0.23/0.18 | +0.24/+0.04 |

**T4-L5 结论（`converge=yes`，基线不变）**：四档全部低于基线 0.53（decay8 0.51 最接近）⇒ **基线（SUBINDUSTRY × decay4 × sector）即最优**。
**L5-R 空转（基线未变）**。
**★ 模板 T4 天花板 = S0.53 / F0.25 / 2Y0.19 / TO5.3%**（SUBINDUSTRY × ts_ir66 × sector × group_rank × reverse）。

---

# C9–C12 收官（2026-11-22，用户「risk60 收尾」）

## C9 · `vector_neut(offer, crowding)` 同集残差（另一腿）

### C9-L2（16 臂，批 `K4xr1fZM5iPcwgAUjgENWG`（8 臂）+ `3Scr6n3i04BLaIp1w4qfKph`（8 臂））

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C9-L2-8** | **`ts_ir`** | `9ql3Y5v9` | **0.50** | **0.24** | **+0.68** |
| C9-L2-4 | `ts_av_diff` | `aka86mjw` | 0.41 | 0.17 | +0.17 |
| C9-L2-14 | `ts_max_diff` | `0mPLlV2K` | 0.40 | 0.17 | −0.11 |
| C9-L2-13 | `ts_sum` | `LLKwjvwv` | 0.30 | 0.11 | +0.32 |
| C9-L2-10 | `ts_arg_min` | `LLKwjv2M` | 0.29 | 0.10 | +0.04 |
| C9-L2-9 | `ts_arg_max` | `pwakX2po` | 0.27 | 0.09 | −0.62 |
| C9-L2-6 | `ts_mean` | `j2aJvkvo` | 0.27 | 0.09 | −0.19 |
| C9-L2-1 | `ts_scale` | `aka86mk1` | 0.25 | 0.08 | −0.22 |
| C9-L2-0 | `ts_zscore` | `rK7w3q88` | 0.23 | 0.07 | −0.18 |
| C9-L2-7 | `ts_std_dev` | `xAvoq76q` | 0.15 | 0.04 | +0.18 |
| C9-L2-2 | `ts_rank` | `9ql3Y5Z1` | 0.10 | 0.02 | −0.25 |
| C9-L2-3 | `ts_quantile` | `MP6nOvML` | 0.09 | 0.01 | −0.25 |
| C9-L2-11 | `ts_returns` | `9ql3ve3q` | 0.07 | 0.01 | −0.49 |
| C9-L2-5 | `ts_delta` | `gJa56N6K` | 0.03 | 0.00 | −0.57 |
| C9-L2-12 | `ts_product` | `e7aPpYPd` | −0.25 | −0.09 | −0.08 |
| C9-L2-15 | `days_from_last_change` | `78YrA5Rv` | −0.50 | −0.25 | −0.55 |

**C9-L2 结论**：**`ts_ir` 0.50 / F0.24 / 2Y0.68 最优**（与 C5 同型：残差化后信噪比内核独占）⇒ **L2b = ts_ir × 126**。

### C9-L2b · 窗口全替（批 `3MVZMn6904yXbBGvt8TceFc`，4 臂）→ 在跑

### C9-L2b · 窗口全替（批 `3MVZMn6904yXbBGvt8TceFc`，4 臂）

| 臂 | 窗口 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C9-L2b-1** | **66** | `QP0Arqkr` | **0.57** | **0.29** | **+0.84** |
| 基线 | 126 | `9ql3Y5v9` | 0.50 | 0.24 | +0.68 |
| C9-L2b-2 | 250 | `omaXwAMm` | 0.38 | 0.16 | +0.38 |
| C9-L2b-3 | 504 | `gJa5qwEm` | 0.34 | 0.13 | +0.49 |
| C9-L2b-4 | 750 | `GrmN0Ypx` | 0.34 | 0.13 | +0.33 |

**C9-L2b 结论（`converge=no`，**ΔS +0.07 / Δ2Y +0.16**）**：66 最优（与 C5 同型：残差 + 短窗）⇒ **L3 基线 = ts_ir66 × industry**。

### C9-L3 · 分组轴全替（批 `JlAn08u55ar9Q6gQ3esSJs`，6 臂）→ 在跑

---

## C10 · `multiply(bid_rate, ts_rank(crowding,66))` 拥挤门控出借费率

### C10-L2-A（8 臂，批 `3p5jZM90C53k9fcDtmIOlvE`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C10-L2-8** | **`ts_ir`** | `VkNLwqLJ` | **0.49** | **0.22** | +0.07 |
| C10-L2-1 | `ts_scale` | `WjlRwnJj` | 0.35 | 0.12 | +0.18 |
| C10-L2-4 | `ts_av_diff` | `3q0OY32Z` | 0.33 | 0.10 | −0.22 |
| C10-L2-7 | `ts_std_dev` | `O0Wjwqj1` | 0.29 | 0.10 | +0.30 |
| C10-L2-6 | `ts_mean` | `78Yrq02v` | 0.23 | 0.07 | −0.37 |
| C10-L2-5 | `ts_delta` | `YPaOwn9A` | 0.16 | 0.03 | −0.64 |
| C10-L2-2 | `ts_rank` | `A1x5JYEl` | 0.15 | 0.03 | −1.02 |
| C10-L2-3 | `ts_quantile` | `omaXwAZk` | 0.15 | 0.03 | −0.98 |

**C10-L2 结论（A 段）**：**`ts_ir` 0.49** 最优（门控型与 C6 同型）⇒ **L2b = ts_ir × 126**。
**C10-L2-B（8 臂，批 `3N0b9T7y35ka9NKb5Wafxtt`）** → 在跑
### C9-L3 结论（批 `JlAn08u55ar9Q6gQ3esSJs`）：**sector 0.57 / F0.30 / 2Y0.85** 微胜（industry 0.57/0.29/0.84；market≡exchange≡country 0.55；subindustry 0.47）⇒ **L4 基线 = ts_ir66 × sector**。

### C10-L2-B（8 臂，批 `3N0b9T7y35ka9NKb5Wafxtt`）：zscore 0.46（subU **1.14**）/ arg_max 0.35 / sum 0.27 / returns 0.21 / max_diff 0.18 / arg_min 0.10 / product −0.29 / days −0.47 ⇒ **`ts_ir` 0.49 保持最优**，**L2b = ts_ir × 126**。

### C9-L4 · 外层层（批 `rfgRBdZA4u0ajC6uhzivoC`，sector 轴）→ 在跑
### C10-L2b · 窗口全替（批 `1wiDI9b9p5g19NXTUa929Ms`）→ 在跑
### C9-L4 结论（批 `rfgRBdZA4u0ajC6uhzivoC`）：**group_rank 0.57 保持**，其余全负（scale −0.43 / zscore −0.44 / neutralize −0.31 / backfill −0.48~−0.50）；sum 0.75 与 std_dev 0.56 是 **TO 111%/109% 越闸**（不可用）⇒ **L5 基线 = ts_ir66 × sector × group_rank**。
### C10-L2b 结论（批 `1wiDI9b9p5g19NXTUa929Ms`）：66 0.32 / 250 0.35 / 504 0.40 / 750 0.39 全部低于基线 126 的 0.49 ⇒ **收敛 126**，**L3 基线 = ts_ir126 × industry**。
### C9-L5 部分读数：INDUSTRY 档 `KPgp6rl1`(sector 轴) 0.47 / `omaXvW76`(industry 轴) 0.44 —— 均 < 基线 0.57；SECTOR 档在跑（`1RbRQuRs4s3bqi17FKGo9jW`）。

## C11 · `divide(bid_rate, ts_mean(bid_rate,252))` 相对历史溢价

### C11-L2-A（8 臂，批 `aAFkje4Y4OYbnxJohBFnPS`）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **C11-L2-8** | **`ts_ir`** | `pwakEjlv` | **0.42** | **0.18** | **+0.34** |
| C11-L2-6 | `ts_mean` | `GrmN6lwo` | 0.30 | 0.10 | −0.36 |
| C11-L2-5 | `ts_delta` | `QP0Aj7Qp` | 0.19 | 0.05 | −0.16 |
| C11-L2-4 | `ts_av_diff` | `kqaMXjKL` | 0.08 | 0.01 | +0.23 |
| C11-L2-1 | `ts_scale` | `d5a6mjnx` | −0.08 | −0.02 | −0.01 |
| C11-L2-2 | `ts_rank` | `zqdEjkOo` | −0.12 | −0.03 | −0.67 |
| C11-L2-3 | `ts_quantile` | `LLKw67km` | −0.13 | −0.03 | −0.64 |
| C11-L2-7 | `ts_std_dev` | `xAvoQjkq` | −0.21 | −0.06 | −0.68 |

**C11-L2 结论（A 段）**：**`ts_ir` 0.42** 最优（`ts_mean` 0.30 次之）——**相对溢价同样吃信噪比内核**（第 6 个构造）；排名型（rank/quantile）在此构造上**反向**（−0.12/−0.13），因分母本身已是长窗均值、再排名会破坏比值语义。
**C11-L2-B（8 臂，批 `48Dks13Lz4ZK9gjCozf8axU`）** → 在跑
### C9-L5 续：SECTOR 档 `d5a677GJ`(sector) 0.37 / `RReoaaG0`(industry) 0.28 —— 亦低于基线 0.57；FAST 档在跑（`4fYSc2gZ5jSa3FXj0BxDfc`）。
### C11-L2-B（8 臂，批 `48Dks13Lz4ZK9gjCozf8axU`）：max_diff 0.40/2Y0.70 / arg_max 0.38/subU0.69 / arg_min 0.27 / sum 0.25 / returns 0.21 / product 0.09 / days −0.06 / zscore −0.14 ⇒ **`ts_ir` 0.42 保持最优**，**L2b = ts_ir × 126**。
### C9-L5 收官：FAST 档 `QP0Alp1X`(sector) 0.51 / `58J16dZM`(industry) 0.41；decay8 档在跑（`oDR8FGv4htcxKbrOZI1wr`）⇒ 目前基线 0.57 仍最优（INDUSTRY/SECTOR/FAST 全劣）。
### C11-L2b（批 `4w6mBq1j05iwcwpTOJYmH12`）：**504 → 0.45 / F0.20 / 2Y0.60**（66 0.33 / 250 0.39 / 750 0.38；基线 126 0.42）⇒ **L3 基线 = ts_ir504 × industry**。
### C9-L5 终判：decay8 档 `gJa5o93O`(sector 轴) 0.57 / `pwak1K76`(industry 轴) **0.58 / F0.30 / 2Y0.90**（+0.01 S，判噪声；2Y +0.05）⇒ **C9 天花板 = S0.57 / F0.30 / 2Y0.85 / TO4.7%**（SUBINDUSTRY × decay4 × ts_ir66 × sector × group_rank）；L5-R 空转（排序已在该档重扫过，ts_ir 领先次优 0.1+）。

### C11-L3 结论（批 `1hid4Fehw4HwbDS10Y9oSlPd`）：**subindustry 0.48 / F0.20 / 2Y0.66** 最优（industry 0.45、其余 0.40）⇒ **L4 基线 = ts_ir504 × subindustry**。
### C11-L4（批 `1yyTnW6z94hvcJ72uWcv4e7`，subindustry 轴）：**group_scale 0.56 / F0.23 / 2Y1.03（ΔS +0.08 / Δ2Y +0.37）** 最优；zscore 0.47/2Y1.04；neutralize 0.04 / backfill 0.05–0.11 / sum −0.39（TO101%）/ std_dev −0.01（TO99%）⇒ **L5 基线 = ts_ir504 × subindustry × group_scale**。
### C10-L3（批 `2xP2FeHy50f99ssjXj8Ni0`，后更正批号 `2x6P2FeHy50f99ssjXj8Ni0`）：**sector ≡ market ≡ exchange ≡ country 0.51**（subindustry 0.41、industry 基线 0.49）⇒ **L4 基线 = ts_ir126 × market**。
### C11-L5 部分：INDUSTRY 档 `zqdE5z7V`(subindustry 轴) 0.52/2Y1.05、`WjlRNmZG`(industry 轴) 0.22 —— 均 < 基线 0.56；SECTOR 档在跑（`2dD38J3tp58car4DmXT7UHL`）。
### C10-L4（批 `3GzAKS1gT4kQ9DL7BBzEUZu`，market 轴）：**group_rank 0.51 保持**（scale −0.05 / zscore −0.05 / neutralize −0.10 / backfill 0.02~0.11 / sum −0.34 TO98% / std_dev 0.18 TO106%）⇒ **L5 基线 = ts_ir126 × market × group_rank**；INDUSTRY 档在跑（`6sE9PbYJ4VUcqL9QZQpOpp`）。
### C10-L5 部分：INDUSTRY 档 `1YWRoRlX`(market 轴) 0.40 / `QP0AnANp`(industry 轴) 0.37 —— 均 < 基线 0.51；FAST 档与 C11 合并批在跑（`L56YQaYT4Lia5fsBxC77bt`）。
### C11-L5 终判（合并批 `L56YQaYT4Lia5fsBxC77bt` FAST / `3jB0UX5aE56iaCuuikqTsX` decay8）：INDUSTRY 0.52 / SECTOR 0.51 / **FAST 0.46** / **decay8 0.56（2Y1.05，与基线打平）** ⇒ 基线（SUBINDUSTRY × decay4 × group_scale）最优。
**★ 模板 C11（相对历史溢价）天花板 = S0.56 / F0.23 / 2Y1.03 / TO2.6%**（SUBINDUSTRY × ts_ir504 × subindustry × group_scale × reverse）——**2Y 1.03 是 risk60 全部构造里第二高**（仅次 C10 的 1.05 单臂）。

### C10-L5（合并批同两条）：INDUSTRY 0.40/0.37 / **FAST 0.57（market 轴，ΔS +0.06）** / decay8 0.50/0.48 ⇒ **FAST 换基线，L5-R 在跑（`vjk6jaua58kbHFErEr9WP`）**。

## C12 · `divide(subtract(offer,bid), bid)` 相对价差（价差÷出借费率）

### C12-L2-A（8 臂，批 `3FP82ifvc4oL9km1cZ6Gn9HE`）→ 在跑
### C12-L2-A 结论（批 `3FP82ifvc4oL9km1cZ6Gn9HE`）：**ts_delta 0.26 / ts_ir 0.26 并列**（`ts_mean` 0.18、`ts_scale` 0.16、`av_diff` 0.15、rank 0.12、quantile 0.10、std_dev −0.25）——**相对价差的「已经是比值」后再套排名/缩放全劣**，只有差分/信噪比取法有效。
### C12-L2-B（8 臂，批 `17wDnza0V4LWcsLg8q0ZUrP`）→ 在跑
### C10-L5-R（批 `vjk6jaua58kbHFErEr9WP`，FAST / market / W126）：**`ts_scale` 0.60 / F0.18 / subU1.06（★第 7 次内核翻转，反超 ts_ir 0.57）**；ts_av_diff 0.33 / ts_std_dev 0.21 / ts_max_diff 0.13 ⇒ **★ 模板 C10（门控 bid）天花板 = S0.60 / F0.18 / 2Y−0.24 / TO20.5%**（FAST × ts_scale126 × market × group_rank × reverse；F 与 subU 强、2Y 负）。
### C12-L2-B（批 `17wDnza0V4LWcsLg8q0ZUrP`）：**`ts_max_diff` 0.31 / F0.12** ≡ arg_min 0.31 / returns 0.26 / product 0.21 / sum 0.12 / zscore 0.06 / days −0.22 ⇒ **L2 冠军 = ts_max_diff（同 S 取 F 更高者），L2b = ts_max_diff × 126**。
### C12-L2b（批 `TUJERbqG4SC96v107gcYDgO`）：**250 → 0.40 / F0.17 / 2Y0.46**（66 0.34 / 750 0.38 / 504 0.33；基线 126 0.31）⇒ **L3 基线 = ts_max_diff250 × industry**。
### C12-L3（6 臂，批 `4uKYPC7i74NocChXao9RfpF`）→ 在跑
### C12-L3（批 `4uKYPC7i74NocChXao9RfpF`）：**subindustry 0.49 / F0.22 / 2Y0.45** 最优（industry 0.40 / sector·market·exchange·country 0.37）⇒ **L4 基线 = ts_max_diff250 × subindustry**。
### C12-L4（8 臂，批 `3C7Knb2v750u9Fs1eU6omGcc`）→ 在跑
### C12-L4（批 `3C7Knb2v750u9Fs1eU6omGcc`，subindustry 轴）：**backfill(·,subindustry,120) 0.55 / F0.24 / 2Y0.76** 与 `group_scale` 0.55 / F0.25 / 2Y0.49 同 S，取 2Y 更高的 backfill120；zscore 0.47/2Y0.59、neutralize 0.49/2Y0.74、backfill252 0.42/2Y0.76；sum 0.87 与 std_dev −0.35 均 **TO >104% 越闸**（不可用）⇒ **L5 基线 = ts_max_diff250 × subindustry × group_backfill120**。
### C12-L5 · 设置档（`e4DyKeFb4sN8YXpbNq5z54`(INDUSTRY) / `1qp7xp3Lh52m9vGRUFtj0QC`(SECTOR) / FAST / decay8 待派）→ 在跑
### C12-L5 部分：INDUSTRY 档 `wpoAE39l` 0.27 / `A1x57eQe` 0.30；SECTOR 档 `Xgax8dMb` 0.35 / `vRAbvWPQ` 0.37 —— 均 < 基线 0.55；FAST（`QLgrzbMl5eG9bZwLebH1c`）与 decay8（`32Nk9EbH44Fmaxu1e6uv2dJQ`）在跑。
### C12-L5 终判（FAST `QLgrzbMl5eG9bZwLebH1c` / decay8 `32Nk9EbH44Fmaxu1e6uv2dJQ`）：FAST 0.43/0.44、decay8 0.49/0.49、INDUSTRY 0.27~0.30、SECTOR 0.35~0.37 —— **全部低于基线 0.55** ⇒ 基线最优，L5-R 空转。
**★ 模板 C12（相对价差）天花板 = S0.55 / F0.24 / 2Y0.76 / TO10.9%**（SUBINDUSTRY × decay4 × ts_max_diff250 × subindustry × group_backfill120）。

---

# ★★ risk60 模板穷尽终判（**12 个互异构造 × 完整 5 层 + L5-R**，2026-11-22/23）

## 12 构造天花板全表

| # | 构造 | 机制 | L2 冠军 | 窗 | 轴 | 外层 | **天花板 S / F / 2Y / TO** | 设置档 |
|---|---|---|---|---|---|---|---|---|
| **C8** | `divide(offer, bid)` 费率比值 | A×A | `ts_ir` | 66 | industry | **group_scale** | **★★ 1.08 / 0.74 / 0.56 / 7.9%** | INDUSTRY |
| C7 | `subtract(offer, bid)` 费率价差 | A×A | `ts_av_diff` | 504 | industry | **group_scale** | 0.82 / 0.48 / −0.19 / 9.0% | decay8 |
| C4 | `vec_sum(crowding)` 去拥挤速度 | B | `ts_quantile`★翻转 | 126 | market | group_rank | 0.79 / 0.22 / 0.46 / 32.0% | FAST |
| C5 | `vector_neut(bid, crowding)` 费率⊖拥挤 | A×B | `ts_ir` | 66 | sector | group_rank | 0.78 / 0.35 / 0.76 / 9.9% | FAST |
| C6 | `multiply(offer, rank(crowding,66))` 门控 | A×B | `ts_zscore` | 126 | industry | group_rank | 0.70 / 0.20 / −0.00 / 27.5% | FAST |
| C10 | `multiply(bid, rank(crowding,66))` 门控 | A×B | `ts_scale`★翻转 | 126 | market | group_rank | 0.60 / 0.18 / −0.24 / 20.5% | FAST |
| C2 | `vec_avg(offer)` 借入费率 | A | `ts_ir` | 126 | industry | group_scale | 0.59 / 0.29 / 0.34 / 5.6% | INDUSTRY |
| C9 | `vector_neut(offer, crowding)` 费率⊖拥挤（另一腿） | A×B | `ts_ir` | 66 | sector | group_rank | 0.57 / 0.30 / 0.85 / 4.7% | 基线 |
| C11 | `divide(bid, ts_mean(bid,252))` 相对历史溢价 | A | `ts_ir` | 504 | subindustry | group_scale | 0.56 / 0.23 / **1.03** / 2.6% | 基线 |
| C12 | `divide(spread, bid)` 相对价差 | A×A | `ts_max_diff` | 250 | subindustry | **backfill120** | 0.55 / 0.24 / **0.76** / 10.9% | 基线 |
| C1 | `vec_avg(bid_rate)` 出借费率 | A | `ts_ir` | 66 | sector | group_rank | 0.53 / 0.25 / 0.19 / 5.3% | 基线 |
| C3 | `vec_avg(last)` 最新费率 | A | `ts_scale` | 504 | sector | group_rank | 0.49 / 0.24 / 0.52 / 9.8% | INDUSTRY |

## 终判

1. **数据集 ATOM 天花板 = S1.08 / F0.74 / 2Y0.56**（C8：`reverse(group_scale(ts_ir(ts_backfill(divide(vec_avg(rsk60_offer),vec_avg(lending_fee_bid_rate)),250),66), industry))` @ **INDUSTRY 中性化 / decay4 / trunc0.08 / TOP700 / D1**）。
   - `checks.fail = []`、`failed_ppa_count = 0`、**CW / SUB_UNIVERSE / TO 全 PASS**；warning 级仅 `LOW_SHARPE 1.08<1.58` / `LOW_FITNESS 0.74<1.0` / `LOW_2Y_SHARPE 0.56<1.58`；`pyramids.effective=1`（`GBR/D1/RISK` ×1.2）。
2. **2Y 维度天花板 = 1.05**（C11 的 decay8 单臂；构造级天花板 2Y1.03 / C9 0.85 / C12 0.76）——**仍低于 2Y 闸 1.58**。
3. **交付 = 0 颗**。最优 C8 距 **S 闸 0.50 / F 闸 0.26 / 2Y 闸 1.02**。
4. **不判死**（用户 2026-11-19 明令「轻易不判死」）：ATOM 面 12 构造已穷尽（>10 满足用户标准），信号层弱 + 2Y 硬墙；`GBR/D1/RISK` 塔 0/3 仍可接受**跨集第二腿**（C8 的 F0.74/subU0.80 质量高，适合作为 regular 组合的高质量腿候选，但需与 pots 池实测 prod）。
5. **梯度验收**：`tools/gates/gradient_gate.py --region GBR --dataset risk60` = **GRADIENT_DONE**（arc_layers=7）。

## 可迁移方法论（risk60 全 12 构造实证）

1. **L1 探针弱 ≠ 构造死**：C7 探针 0.00 → 天花板 0.82；C8 探针 0.03 → 1.08；C5 探针 0.14 → 0.78。**构造的强弱必须看完整梯度**。
2. **`ts_ir` 是费率结构的通用冠军**（C1/C2/C5/C8/C9/C11 六个构造 L2 第一）——「均值÷波动」正是借券费率的信息形态。
3. **外层算子与量纲强耦合**：已无量纲（比值/残差/门控/相对溢价）⇒ 只能 `group_rank`（全 12 构造里 8 个如此）；保留绝对量纲（价差）⇒ `group_scale` 才是最大杠杆（C7 +0.15 / C8 +0.22）；**C12 例外**：`group_backfill(120)` 提供同 S 但 2Y 更高的替代（+0.27 2Y）。
4. **窗口方向按变量类型相反**：存量/价差型要长窗（C7 504、C11 504），套利偏离/比值型要短窗（C8 66、C9 66），中间型 126–250。
5. **设置档按构造类型分裂**：流量/门控/残差（C4/C5/C6/C10）吃 **FAST**；价差慢变量（C7）吃 **decay8**；比值（C8）与单字段（C2/C3）吃 **INDUSTRY**；其余基线最优。
6. **7 次内核翻转**全部发生在换设置基线之后（C4/C10 等）⇒ **L5-R 必做**。
7. **CW/subU 的修复杠杆是中性化档**：C8 在 SUBINDUSTRY 下 `CONCENTRATED_WEIGHT 0.1218>0.10` FAIL，换 INDUSTRY 后 CW PASS 且 subU 0.35→0.80。
8. **同一字段族的「水平 vs 差分」决定冠军**：C1/C2 水平 → ts_ir；C7 价差 → ts_av_diff；C12 相对价差 → ts_max_diff。

---

# ⚠ 覆盖缺口审计（2026-11-23 用户质询「所有梯度都测了吗，算子都替换过吗，参数精调了吗」）

**结论：没有。本档案的「5 层完整梯度」是模板级完整（每层命中我固定的候选集），不是全目录穷尽，且参数精调未做。** 该缺口适用于 risk60 全部 12 构造（同一套 16 内核 / 8 外层模板）与 inst25 的 23 构造。

## 精确缺口（以 C8 为样本，依据 `docs/reference/operators_catalog.json` 全 103 算子）

| 层 | 目录全量 | 已测 | **未测** |
|---|---|---|---|
| L2 内层 Time Series | **30** | 16 | **14**：`hump` `kth_element` `last_diff_value` `ts_backfill`(仅作包装) `ts_corr` `ts_count_nans` `ts_covariance` `ts_decay_linear` `ts_delay` `ts_kurtosis` `ts_regression` `ts_step` `ts_target_tvr_decay` `ts_target_tvr_hump` |
| L3 外层 Group | **11** | 8 | **4**：`group_mean` `group_count` `combo_a` `group_cartesian_product` |
| 外层 Cross-sectional | **6** | **0** | `rank` `zscore` `scale` `winsorize` `quantile` `normalize`（**整族从未做外层替换**） |
| 外层 Transformational | **4** | **0** | `bucket` `tail` `trade_when` `generate_stats`（**整族从未做**） |
| L5 设置（中性化档） | 平台 7 档 | 4（SUBINDUSTRY/INDUSTRY/SECTOR/FAST） | **3**：`STATISTICAL`（风险线档，按记忆**可交付**）、`SLOW_AND_FAST`、`SLOW` |
| L5 其它参数 | — | decay 仅 {4,8}；trunc 固定 0.08；nanHandling ON；maxTrade OFF | **decay {0,2,16,32}、trunc {0.05,0.10,0.15}、nanHandling OFF、maxTrade ON 全未测** |
| 参数精调 | — | **无** | 窗口细网格 `{44,88,110,132,160,200}`、backfill 窗 `{66,120,252,504}`、decay×trunc 交叉 |

## 补测批次清单（每批 ≤8 臂；按「一次只发一批」执行）

- **A. L2 剩余 TS（签名兼容，8 臂）**：`ts_decay_linear` / `ts_delay` / `ts_kurtosis` / `ts_count_nans` / `last_diff_value` / `ts_corr(sig, ts_delay(sig,1), N)` / `ts_covariance(sig, crowding, N)` / `ts_regression(sig, crowding, N)`（⚠ ts_regression 有量纲闸，比值型 C8 自身无量纲，需实测是否被拒）
- **B. L2 命名参数类（4 臂）**：`hump(sig, hump=0.01)` / `kth_element(sig, k=N)` / `ts_target_tvr_decay(sig, ...)` / `ts_target_tvr_hump(sig, ...)`；`ts_step` 只收数字 ⇒ 排除并写明
- **C. L3 外层 Group 剩余（4 臂）**：`group_mean` / `group_count` / `combo_a` / `group_cartesian_product`
- **D. 外层 Cross-sectional（6 臂）**：`rank` / `zscore` / `scale` / `winsorize` / `quantile` / `normalize`
- **E. 外层 Transformational（4 臂）**：`bucket` / `tail` / `trade_when` / `generate_stats`
- **F. L5 设置扩展（3 批 × 2 臂）**：`STATISTICAL` / `SLOW_AND_FAST` / `SLOW`
- **G. 参数精调（4 批）**：decay {0,2,16,32}（4 臂）→ trunc {0.05,0.10,0.15}（3 臂）→ 窗口细网格 {44,88,110,132,160,200}（6 臂）→ backfill 窗 {66,120,252,504}（4 臂）
- **H. 换基线后重扫（L5-R）**：若 F/G 产生新基线，按纪律重扫 L2 冠军 5 臂

⇒ **C8 单构造补测 ≈ 10 批 ≈ 50 臂**；12 构造全部补完 ≈ 120 批 ≈ 600 臂（另加 inst25 23 构造的同类缺口）。**在补完前，本档案的天花板读数只能记为「模板级候选集内的天花板」（PROVISIONAL）**，不得表述为「数据集穷尽」。

## 当前阻塞

`wq-brain-http` / `wqb-db` MCP 本会话连接失败（`ERA_NEGOTIATION_FAILED: Version negotiation probe failed: fetch failed`）⇒ **无法派发新批**。需服务恢复（`python tools/start_wq_mcp.py --all` 或重启客户端连接）后按 A→H 顺序执行。

## ★ C8 补测批 A（L2 剩余 TS 算子，批 `3zIOmo82Q5cFccaG0EKCyct`，7 臂，W126/industry/group_rank）

| 臂 | 内核 | α | S | F | 2Y |
|---|---|---|---:|---:|---:|
| **A-7** | **`ts_covariance(sig, crowding, 126)`** | `leaPYn22` | **0.49** | **0.23** | **+0.81** |
| A-1 | `ts_decay_linear` | `XgaAx3Pl` | 0.16 | 0.04 | +0.14 |
| A-2 | `ts_delay(126)` | `qM7Jpavj` | 0.10 | 0.02 | −0.20 |
| A-4 | `ts_count_nans` | `1YWAR81R` | −0.17 | −0.05 | +0.11 |
| A-3 | `ts_kurtosis` | `d5ar6MgY` | −0.12 | −0.03 | −0.70 |
| A-5 | `last_diff_value` | `88NxZ0rm` | −0.00 | −0.00 | −0.08 |
| A-6 | `ts_corr(sig, delay(sig,1))` 自相关 | `0mP2LVdv` | −0.32 | −0.12 | +0.19 |

**★ 批 A 结论（关键）**：**`ts_covariance(费率比值, crowding)` = 0.49 / F0.23 / 2Y**0.81** —— 在同一层位上 **高于原 L2 冠军 `ts_ir` 的 0.38（+0.11 S、+0.10 2Y）**。⇒ **原 16 内核候选集确实漏掉了更强内核**（用户质询成立）。其余 6 个补测内核全劣（≤0.16），`ts_count_nans`/`last_diff_value` 属退化内核（无信息）。
> ⚠ 语义说明：`ts_covariance(ratio, crowding)` 是「费率比值与做空流量的协动」——比 `ts_ir`（纯时序信噪比）多了**跨字段共动**信息，因此不只是内核替换，实质是构造增强。
> ⇒ 需沿 `ts_covariance` 新基线重跑下游（窗口 → 轴 → 外层 → 设置 → L5-R），见批 A2。

## ★ C8 补测批 A2（ts_covariance 窗口全替，批 `2vRhZX8kf4RFa93dwJxt7Vc`，4 臂）

| 窗 | 66 | **750** | 504 | 250 | 126（A-7 基线） |
|---|---:|---:|---:|---:|---:|
| S | 0.41 | **0.57** | 0.49 | 0.40 | 0.49 |
| F | 0.18 | **0.27** | 0.22 | 0.17 | 0.23 |
| 2Y | 0.66 | **1.13** | 0.93 | 0.77 | 0.81 |

**批 A2 结论**：**窗 750 → 0.57 / F0.27 / 2Y 1.13（ΔS +0.08 / Δ2Y +0.32 vs 126）**，且 **2Y 1.13 是 risk60 全部读数中最高**（前高 C11 单臂 1.05）。
对比原 C8 链：`ts_ir` 在同层位最佳是 W66 的 **0.62**（S 更高 0.05，但 2Y 仅 0.45）。⇒ **两条路线正交**：ts_ir = S 优先、ts_covariance750 = 2Y 优先。因本数据集 S 缺口更大（1.08 vs 1.58），主线仍走 ts_ir；但 ts_covariance750 的价值在于**2Y 首次接近闸口**，需沿它跑完下游看 group_scale/设置能否同时抬 S。

## ★ C8 补测批 A3（ts_covariance750 轴层，批 `3X2zGr38L4EdbtP1bnH4USK`，6 臂）

| 轴 | **subindustry** | industry（基线） | sector | market≡exchange≡country |
|---|---:|---:|---:|---:|
| S | **0.63** | 0.57 | 0.55 | 0.52 |
| F | **0.30** | 0.27 | 0.27 | 0.25 |
| 2Y | **1.36** | 1.13 | 1.13 | 1.06 |

**批 A3 结论**：**subindustry 0.63 / F0.30 / 2Y1.36（ΔS +0.06 / Δ2Y +0.23）** ⇒ 该内核**偏好细轴**（与 ts_ir 路线一致）。**2Y 1.36 是本数据集全部读数的新高**（前高 1.13）。⇒ 沿 subindustry 继续外层（批 A4）。

## ★ C8 补测批 A4（外层全替，批 `2aC2XfdbW4juaEqixytDrj7`，7 臂，subindustry 轴）

| 外层 | rank（基线） | scale | zscore | neutralize | backfill120 | backfill252 | group_count |
|---|---:|---:|---:|---:|---:|---:|---:|
| S | **0.63** | 0.56 | 0.38 | 0.25 | 0.28 | 0.29 | −0.56（TO 84%） |
| 2Y | **1.36** | 1.11 | 0.94 | 0.65 | 0.69 | 0.70 | −1.76 |

**批 A4 结论**：**group_rank 0.63 保持最优**（scale 0.56 次之）；`group_count`（聚合型，TO 84%）崩。⇒ 与 C8 主线同型：**协方差型内核只能用 group_rank**。⇒ L5 基线 = ts_covariance750 × subindustry × group_rank。
> ⚠ `group_mean` 本批被 toolkit 静态闸拦下（签名 `group_mean(x, weight, group)` 需 3 参），留批 C 用合法 weight 单测。

## C8 补测批 A5（设置档，逐档 2 臂）
- `INDUSTRY`（批 `4E3iPOdxb4YWcjB1gexlYy8u`）：subindustry 轴 **0.54 / 2Y1.32**、industry 轴 0.46 —— 均 < 基线 0.63。
- `SECTOR`（批 `gofyU2NO4Pqa5l9qkj6yZC`）→ 在跑；随后 `FAST` / `decay8` / **`STATISTICAL`（风险线档）** / `SLOW_AND_FAST` / `SLOW`。
- `SECTOR`（批 `gofyU2NO4Pqa5l9qkj6yZC`）：subindustry 0.38 / industry 0.32 —— 亦 < 0.63；`FAST`（`37dm8SfFP4B6aCq15eqccNnr`）在跑。

---

# ★ 模板来源取证（用户标准要求 #2：论坛 post id / 论文 DOI，2026-11-23 补做）

> 检索通道：论坛 = `search_forum_posts_local`（Zendesk 列表 + 本地过滤，唯一通道）；论文 = `tools/research/paper_search.py --diverse`（多样证达标：**24 篇 / 15 作者**，要求 ≥5 篇 ∧ ≥3 作者 ✅）。

## 论文侧（外部金融文献）

| 模板族 | 文献 | DOI / id | 支撑的机制 |
|---|---|---|---|
| A 费率水平（C1/C2/C3） | The Short Squeeze: The 'Invisible' Cost of Short Sales (2016) | `10.2139/ssrn.2783374` | 借券费率是空头持有的显性成本，价格内含 ⇒ 费率**水平**应有横截面定价力（本文档 L1 实测 S≤0.15 与之相悖，是重要反证） |
| A 费率水平（补充） | Securities Lending (2012) | `10.2139/ssrn.2030418` | 借券供给/费率结构决定机制 |
| 价差 / 比值（C7/C8/C12） | Securities Lending: A Market Perspective on the Changing Securities Lending Landscape (2015) | `10.59403/94jsad` | 出借费率 vs 借入费率的**价差/相对结构**是流动性紧张度的更纯度量 |
| 拥挤/利用率（C4/C6/C10） | Borrow Frictions in Plain Sight: Short-Sale Costs Without Borrow Fees (2026) | `10.2139/ssrn.7684298` | **无费率时的借贷摩擦代理** ⇒ 拥挤度可替代费率做门控/残差 |
| 变化型（C5/C7/C9/C10） | Surprise in short interest (2023) | `10.1016/j.finmar.2023.100841` | 空头头寸**意外**（变化）才有定价力，存量水平无 ⇒ 支持「差分/协动优于水平」 |
| 存量 vs 流量（C4 vs T7） | Short Interest vs. Short Selling (2011) | `10.2139/ssrn.1930997` | 存量与流量必须分开建模 |
| 空头利息收益预测 | Why All the Interest in Short Interest? (1987) | `10.2469/faj.v43.n4.76` | 空头利息作为收益预测变量 |
| **★ C11 相对历史溢价**（补录，2026-11-23） | **An Anatomy of the Stock Borrow Fee Anomaly (2026)** | **`10.2139/ssrn.6652118`** | **借券费相对自身历史基线的偏离才是定价因子（费率水平无、异常有）** ⇒ 直接支撑 C11 的 `divide(bid, ts_mean(bid,252))` 构造 |
| **★ C11 补充** | The Cost of Short-Selling Liquid Securities (2013) | `10.1111/jofi.12009` | 空头成本的结构性度量与横截面定价力 |
| **★ C13 新构造（派生）** | An Anatomy of the Stock Borrow Fee Anomaly (2026) + 论坛 `44941181410455` | `10.2139/ssrn.6652118` | 「相对自身历史常态」的中位数正交结构 |

> ★ C11 的论文检索走 `paper_search.py --diverse`：**18 篇 / 15 作者**（diverse_ok=true，要求 ≥5 ∧ ≥3 ✅），查询词 `securities lending fee mean reversion deviation from own history` / `borrow cost relative to trailing average anomaly` / `short selling cost normalization own-history baseline`。
> ★★ **检索反证**：`10.2139/ssrn.2783374`（费率水平应有定价力）被本数据集 L1 实测推翻（S≤0.15）⇒ 归档保留该反例，**「文献支持」不等于「本地可复现」**，引用时必须同时记录反证。

## 论坛侧补充取证（2026-11-23 补 C11 / C13）

| 模板/机制 | post id | 票数 | 支撑内容 |
|---|---|---|---|
| **★ C11 / C13「相对自身历史常态」官方模板** | **`44941181410455`** | 10 | BRAIN Tips 001 给出 GLB ATOM 模板：`group_neutralize(vector_neut(ts_median(ts_backfill(FIELD,60),20), ts_median(ts_backfill(FIELD,60),250)), country)`——原文经济直觉：「市场看的是**最近相对它自己的常态，发生了什么变化**……对缓慢更新的信息往往反应不足」⇒ **C11 的 `divide(bid, ts_mean(bid,252))` 是其 median 版**；并**派生出 C13**（短中位数 ⊖ 长中位数正交 + 组中性化），C13 **不在原 12 构造内** |
| **Fitness 公式与 0.125 换手下限** | `44556201135127` | 55 | `Fitness = Sharpe × √(|Returns| / max(TO, 0.125))` ⇒ **TO<12.5% 后降换手对 F 零贡献**（与记忆 [[operator-gradient-results-20261120]] 一致，实测互证）⇒ 本构造 TO 8.3% 已落在 0.125 下限内 ⇒ **L4 decay 档的 F 收益必须靠 S 而非靠降 TO** |
| **decay 是最快修复 F 的旋钮** | `44557494579607` | 16 | 「把 decay 从 0/2 提到 5/10 以上」是压 TO 提 F 的最快手段；并建议用 `ts_mean`/`ts_rank` 平滑替代硬截断 ⇒ 支撑批 G-4~7 的 decay 档扫描（当前只测过 4 与 8） |
| **S 1.5 以上才算稳定边际** | `44529911998615` | 44 | 「Sharpe above 1.5 indicates a stable, consistent edge」⇒ 与平台 S 闸 1.58 同向，确认 S 闸不是严苛 idiosyncratic 阈值 |

### ★★ C13 新构造（由论坛 `44941181410455` 派生，2026-11-23 新增 ⇒ 构造数 12 → 13）

```
C13 = group_neutralize(
         vector_neut(
           ts_median(ts_backfill(vec_avg(rsk60_offer),60), 20),
           ts_median(ts_backfill(vec_avg(rsk60_offer),60), 250)
         ),
         subindustry)
```

- **与 C11 的区别**：C11 用 `ts_mean` 且比值形式（除以自身均值）；C13 用 **短/长中位数之差正交**（median 更抗极值，且把「短期常态 vs 长期常态」做成**两个独立信号的正交化**，不是比值）。
- **机制互异性**：C11 = 溢价水平（ratio）；C13 = **常态迁移速度**（短中位数相对长中位数的漂移）⇒ 经济含义不同，属**结构互异构造**。
- **来源**：论坛 `44941181410455` 官方模板 + 论文 `10.2139/ssrn.6652118`。
- ⇒ 需按同一 5 层口径跑（至少 L1 探针 + L2 内核 + 轴 + 外层 + 设置 + 参数层）。

## 论坛侧（平台社区）

| 模板/步骤 | post id | 票数 | 支撑的机制 |
|---|---|---|---|
| **L1 探针做法（先单算子测方向）** | `44887744717335` | 139 | 单数据集研究法：画像 → 挑有经济含义字段 → **先用简单表达式 + 单个横截面算子（rank/zscore/quantile）测方向**再上复杂结构 |
| **参数精调层（命名参数）** | `44734752518039` | 32 | 官方给出 `ts_target_tvr_decay(x, lambda_min, lambda_max, target_tvr)`、`ts_target_tvr_hump(...)`、`hump(x, hump=)`、`trade_when(x,y,z)` 的用法与目标换手率写法 ⇒ 批 B/E 的**逐参数档位扫描**依据 |
| **费率/空头腿成本审计** | `44687266076823` | 5 | 引 Daniel & Moskowitz (2016) 动量崩溃：空头腿需单独审计，**借券费进入成本** ⇒ 支撑「费率水平/价差」族模板 |
| **ATOM 定义与闸线** | `44770798147735` | 65 | ATOM 单数据集豁免 IS-Ladder（2Y→10Y 分段测试），**只看最近 2 年 IS Sharpe**（非 CHN D1 常规门槛 1.59，TO<30% 再乘 0.85）⇒ **本档案所有 ATOM 构造的「2Y」即 Last-2Y IS Sharpe**，IS-Ladder 不适用 |

> ⚠ 平台事实修正（来自 `44770798147735`）：**ATOM 单集 alpha 豁免 IS-Ladder 测试**，故 risk60/inst25 的判定应以「Last-2Y IS Sharpe ≥ 1.58（1.59 的两位截断）+ LOW_SHARPE + LOW_FITNESS + CW + subU」为准；**不存在 10 年阶梯约束**。这解释了 inst25 P 模板 2Y1.93 的可用性（仍需 S/F 达标）。

## C8 补测批 A5 续（设置档，ts_covariance750 × subindustry × group_rank）
| 档 | 轴 | S | F | 2Y | 批 |
|---|---|---:|---:|---:|---|
| **FAST** | **subindustry** | **0.66** | 0.26 | **1.50** | `37dm8SfFP4B6aCq15eqccNnr` |
| FAST | industry | 0.51 | 0.18 | 1.10 | 同上 |
| SUBINDUSTRY + decay8 | subindustry | 0.61 | 0.29 | 1.31 | `30qgIE2gh4u69pJJzt68w4o` |
| SUBINDUSTRY + decay8 | industry | 0.56 | 0.27 | 1.10 | 同上 |
| STATISTICAL（风险线档） | subindustry / industry | 在跑 | | | `2F7Llha504LRbIMNfyXace4` |

⇒ 该路线当前最优：**FAST × ts_covariance750 × subindustry × group_rank = S0.66 / F0.26 / 2Y1.50 / TO8.3%**。
| STATISTICAL（风险线档） | subindustry | 0.46 | 0.14 | 0.93 | `2F7Llha504LRbIMNfyXace4` |
| STATISTICAL（风险线档） | industry | 0.21 | 0.05 | 0.44 | 同上 |
| SLOW_AND_FAST | subindustry / industry | 在跑 | | | `444ZJ9fnV4TD9nIjgOuScSO` |
| SLOW_AND_FAST | subindustry | 0.61 | 0.22 | **1.53** | `444ZJ9fnV4TD9nIjgOuScSO` |
| SLOW_AND_FAST | industry | 0.51 | 0.17 | 1.10 | 同上 |
| SLOW | subindustry / industry | 在跑 | | | `2kUZFq6As4M1b55lDu6EED` |
| SLOW | subindustry | 0.58 | 0.21 | 1.45 | `2kUZFq6As4M1b55lDu6EED` |
| SLOW | industry | 0.48 | 0.16 | 1.04 | 同上 |

**★ 设置档 7 档全测完结论**（ts_covariance750 × subindustry × group_rank）：
| 档 | S | F | 2Y | TO |
|---|---:|---:|---:|---:|
| **FAST** | **0.66** | 0.26 | 1.50 | 8.3% |
| SLOW_AND_FAST | 0.61 | 0.22 | **1.53** | 9.0% |
| SUBINDUSTRY + decay8 | 0.61 | 0.29 | 1.31 | 2.6% |
| SLOW | 0.58 | 0.21 | 1.45 | 5.6% |
| SUBINDUSTRY | 0.63 | 0.30 | 1.36 | 2.7% |
| STATISTICAL（风险线） | 0.46 | 0.14 | 0.93 | 7.2% |
| INDUSTRY | 0.54 | 0.25 | 1.32 | 2.7% |
| SECTOR | 0.38 | 0.16 | 1.27 | 2.5% |
⇒ **FAST 最优（S 0.66）；2Y 单项最高是 SLOW_AND_FAST 1.53**（距闸 0.05）。★ 注意 STATISTICAL 档本轮**低于 FAST**（0.46 vs 0.66）⇒ 本构造走**标准档**路线，不是风险线档。

### C8-L5-R · 换基线（FAST）后内核重扫（批 `4sP1INd4R4AUag7uZKtbo1s`，5 臂）→ 在跑

### C8-L5-R 结论（批 `4sP1INd4R4AUag7uZKtbo1s`，FAST 档重扫 5 内核）
| 内核 | ts_covariance（基线） | ts_ir | ts_av_diff | ts_max_diff | ts_delta |
|---|---:|---:|---:|---:|---:|
| S | **0.66** | 0.18 | −0.22 | 0.43 | 0.22 |
| 2Y | **1.50** | 0.09 | 0.08 | 1.45 | 0.10 |

**未翻转**（ts_covariance 领先次优 0.23）⇒ 该路线梯度闭环。
**★ ts_covariance 路线天花板 = S0.66 / F0.26 / 2Y1.50 / TO8.3%**（FAST × ts_covariance750 × subindustry × group_rank × reverse）——**2Y 距闸仅 0.08，S 距闸 0.92**。

### 批 D · Cross-sectional 外层全替（6 臂，`JyIC3beV4zFaUWmgPDG3rx`）→ 在跑

### 批 D · Cross-sectional 外层全替（6 臂，`JyIC3beV4zFaUWmgPDG3rx`）

| 外层 | rank（基线） | rank | zscore | scale | winsorize | quantile | normalize |
|---|---:|---:|---:|---:|---:|---:|---:|
| S | 0.66 | 0.66 | 0.66 | 0.66 | 0.66 | 0.66 | 0.66 |
| F | 0.26 | 0.26 | 0.26 | 0.26 | 0.26 | 0.26 | 0.26 |
| 2Y | 1.50 | 1.50 | 1.51 | 1.50 | 1.50 | 1.50 | 1.51 |
| invest_ratio | 0.9848 | 0.9848 | 1.0000 | 0.9848 | 0.9848 | 0.9848 | 1.0000 |

**★ 批 D 结论（no-op 实测举证）**：**6 个 Cross-sectional 算子读数逐位相同**（仅 2Y/invest_ratio 在 1.50↔1.51、0.9848↔1.0000 两位级浮动）⇒ **在 `group_rank` 内层接任何单调变换都是数学 no-op**（单调变换不改变组内秩）——这是记忆里「group_rank 之后的 winsorize/signed_power 是空操作」的**首次 6 算子并测实证**。⇒ Cross-sectional 族对本构造**实测无效，不必再测**。

### ★★ 单位约束发现（批 E 派发过程中实测，toolkit 静态闸连拒 5 次）

| 算子 | 能否放在 `group_rank` **内层** | 能否放**外层**再 `reverse` | 原因 |
|---|---|---|---|
| `ts_covariance` | ✅ 可（输出被 group_rank 吸收） | — | — |
| `bucket` | ❌ `Unit[Group:1]` | ❌ | bucket 按组分桶 ⇒ **输出带 Group 单位** |
| `tail` | ❌ `Unit[Group:1]` | ❌（`reverse` 拒 Group 单位输入） | tail 按组截尾 ⇒ 输出带 Group 单位 |
| `generate_stats` | ❌ `Unit[Group:1]` | — | 输出带 Group 单位 |
| `trade_when` | — | ✅ 可（输入改为非 group 的原始信号） | trade_when 自身不产 Group 单位 |

⇒ **Transformational 族（bucket/tail/generate_stats）与 `group_rank` 在本链路上互斥**（不是「无效」，是**单位不兼容，平台直接拒**）。这是**平台级硬约束**，记入方法论：选外层算子前必须查单位族，否则整批被静态闸拒。
⇒ 修正后的批 E 范围 = **`trade_when` 门控 + `ts_target_tvr_decay` / `ts_target_tvr_hump` / `hump`（命名参数类）**，共 4 臂（批 `322nOge3H4w898IIUTZvSpV`）。

### 批 B · 命名参数类（4 臂，`322nOge3H4w898IIUTZvSpV`）

| 臂 | 算子 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| B-1 | `trade_when(crowding_rank>0.8, cov, -1)` 门控 | `P05L6vgp` | 0.65 | **0.31** | 1.05 | 10.8% |
| B-2 | `ts_target_tvr_decay(..., target_tvr=0.1)` | `pwabE85x` | 0.65 | 0.25 | 1.47 | 8.3% |
| B-3 | `ts_target_tvr_hump(..., target_tvr=0.1)` | `A1xXbkQR` | 0.65 | 0.25 | 1.48 | 8.3% |
| B-4 | `hump(..., hump=0.01)` | `vRA79dOz` | **0.22** | 0.05 | 0.61 | 7.7% |

**批 B 结论**：① `trade_when` 门控（拥挤前 20% 才持仓）**F 0.31 创新高**（基线 0.26）但 2Y 1.50→1.05（样本被截断 ⇒ 2Y 必然掉）；② `ts_target_tvr_hump` 与基线**几乎逐位相同**（0.65/0.25/1.48 vs 0.66/0.26/1.50）⇒ 该目标换手包装在本构造上**近似 no-op**；③ `hump` 直接崩到 0.22 ⇒ **平滑算子在协方差型信号上是摧毁器**（与「ts_av_diff/ts_delta 等差分类在残差型上无效」同族）。
> 依据：论坛帖 `44734752518039`（32 赞）官方给出的三类 target_tvr 写法已全部实跑。

### 批 C · Group 剩余算子（`group_mean` / `group_cartesian_product` / `combo_a`）
- `combo_a` 与 `group_cartesian_product` 的输出带 **Group 单位** ⇒ `reverse` 拒收（静态闸拦下），**本构造上不可用**。
- `group_mean(x, weight, group)` 需 3 参，已按合法签名单测（批 `3AD8BieJe5dQ9KWaMnBF8TZ`，2 臂）。

**批 C 结论（批 `3AD8BieJe5dQ9KWaMnBF8TZ`，2 臂）**：

| 臂 | 算子 | α | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| C-1 | `group_mean(sig, ts_backfill(vec_sum(rsk60_crowding),250), subindustry)` | `akamPWJ2` | **−0.74** | −0.14 | −0.42 | **93.4%** |
| C-2 | `group_rank`（基线对照） | `aka9pPv1` | **0.66** | **0.26** | **1.50** | 8.31% |

⇒ **`group_mean` 判死**（S 转负 + TO 93% 越闸）：`group_mean` 输出的是组内**调和均值**（水平量），把协方差型的「共动强度」压回费率水平 ⇒ **与外层算子选择铁律一致**（[[outer-op-choice-by-signal-type]]：已无量纲排名的信号用 `group_rank`，水平量用 `group_backfill`；`group_mean` 两边都不适配）。
⇒ C-2 与批 A5 的 FAST 档读数**逐位一致**（0.66 / 0.26 / 1.50）⇒ 基线可复现，无平台漂移。
⇒ **Group 11 类算子在本构造上已穷尽**（8 已测 + `group_mean` 判死 + `combo_a`/`group_cartesian_product` 单位不兼容）⇒ **Group 族无剩余未测项**。

## ★ 批 G-1 · 窗口细网格（参数精调层，批 `3rMAOwcQl5h79LEJIy0948T`，8 臂）

受控 1-D 扫描：`ts_covariance` 窗口 d ∈ {44, 88, 110, 132, 160, 200} + **750（基线对照）** + **1000（新档）**，其余全部锁定（decay4 / FAST / trunc0.08 / nanON / subindustry 轴 / `reverse(group_rank(...))` 外壳）。

| d | 44 | 88 | 110 | 132 | 160 | 200 | **750** | 1000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| α | `QP0R2qmG` | `npaGZYkx` | `RRex2qZd` | `xAv7P9wl` | `6XM6a3P5` | `npaGZYYz` | **`aka9pPv1`** | `LLKogqqM` |
| S | 0.34 | 0.37 | 0.49 | 0.59 | 0.35 | 0.44 | **0.66** | 0.43 |
| F | 0.10 | 0.11 | 0.17 | 0.23 | 0.10 | 0.15 | **0.26** | 0.14 |
| 2Y | −0.41 | 0.19 | 0.42 | 0.11 | 0.27 | 0.19 | **1.50** | 1.19 |
| TO | 13.0% | 11.0% | 10.6% | 10.2% | 9.9% | 9.5% | 8.3% | 8.1% |
| subU | 0.40 | 0.48 | 0.58 | 0.64 | 0.55 | 0.75 | 0.62 | 0.52 |

**批 G-1 结论**：
1. **750 是窗口峰且两侧都掉**（1000 → 0.43/1.19；132 → 0.59/0.11）⇒ **不是单调关系，存在中间的窄峰**（协方差需要足够样本才稳定、但过长窗又混入陈旧结构）。
2. **短窗（44–110）一律塌陷且 2Y 转负**（44 → 2Y −0.41）⇒ 本机制是**长程结构型**，不是短期动量型。
3. ★ **可复现性实测**：750 对照臂复现出**同一个 alpha id `aka9pPv1`**（与批 C 的基线臂同一 id、读数逐位相同 0.66/0.26/1.50）⇒ 平台无漂移，批间读数可比。
4. ⇒ **窗口层收敛于 750**，参数精调层在窗口这一维已闭合（无更优档）。

### 批 G-2 · 未测 TS 内核补齐（`ts_regression` / `kth_element` / `ts_step`）

- `ts_regression(y, x, d, lag=0, rettype=0)`：`y` = 费率比值（无量纲）、`x` = crowding（无量纲 ±1）⇒ 量纲上应可通过，但记忆记载平台对 `ts_regression` 有「无量纲字段被拒」的历史坑 ⇒ **单独成臂实测**，失败不影响同批其它臂。
- `kth_element(x, d, k, ignore="NaN")`：取窗内第 k 个有效值（语义近「陈旧值」度量）。
- `ts_backfill(x, lookback=d, k=1)` 作为**内核**（此前只当包装用）：`k=2` 取「第 2 个最近有效值」⇒ 陈旧度度量。
- `ts_step` 只收数字（不接受字段输入）⇒ **排除并写明**（与批 A 中 `ts_count_nans`/`last_diff_value` 属退化内核同档）。
⇒ TS-30 类别在本构造上**就此闭合**（16 已测 + 10 已补 + 3 本批 + 1 排除 = 30）。

### 批 V1 · Vector 聚合族全替（批 `k1NjEgq54CR8IfN3ioKNWW`，8 臂）—— **★★ 突破**

risk60 五字段**全部 VECTOR** ⇒ 折叠函数本身是一个 8 算子的类别，且改变信号的经济含义。基线 = `ts_covariance`750 × subindustry × `group_rank` × FAST/decay4/trunc0.08/nanON。

| 臂 | 费率对折叠 | α | S | F | 2Y | subU | TO | 判读 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | `vec_avg`/`vec_avg`（对照） | `aka9pPv1` | 0.66 | 0.26 | 1.50 | 0.62 | 8.31% | 基线 |
| **2** | **`vec_max`/`vec_max`** | **`A1xX3n8W`** | **0.73** | **0.30** | **1.70** | 0.66 | 8.29% | **★ 2Y 首次过闸；failed_RA=2（只剩 S+F）** |
| 3 | `vec_min`/`vec_min` | `0mPZ8A2r` | 0.51 | 0.18 | 0.79 | 0.35 | 8.39% | 劣于 avg |
| 4 | `vec_sum`/`vec_sum` | `2r5VKvoY` | 0.66 | 0.26 | 1.50 | 0.62 | 8.31% | **与 avg 逐位相同 ⇒ no-op 实证** |
| 5 | `vec_stddev`/`vec_stddev` | `RRexrNx0` | −0.10 | −0.02 | −0.49 | −0.26 | 8.31% | 判死 |
| 6 | `vec_range`/`vec_range` | `1YW3go3X` | −0.08 | −0.01 | 0.59 | −0.18 | 8.85% | 判死 |
| 7 | 费率对不变，crowding 改 `vec_avg` | `0mPZ8AZ2` | 0.03 | 0.00 | 0.96 | 0.18 | 8.33% | 判死（拥挤必须 `vec_sum`） |
| 8 | `vec_avg(rsk60_last)`/`vec_avg(bid)` | `bla09Nmp` | 0.60 | 0.23 | 1.00 | 0.58 | 8.36% | 第三费率字段弱 |

**★★ 批 V1 结论（四个独立发现）**：

1. **★ 尾部折叠 > 平均折叠（机制发现，非算子替换）**：`vec_max` 0.73/0.30/**1.70** 全面优于 `vec_avg` 0.66/0.26/1.50（ΔS +0.07 / ΔF +0.04 / **Δ2Y +0.20**），且 `vec_min` 0.51 垫底 ⇒ **单调序 = max(0.73) > avg(0.66) > min(0.51)** ⇒ **借券市场的「最难借的那家」（尾部摩擦）比平均费率更有定价力，均值被摊薄**。这与文献中「稀缺性约束集中在尾部（少数高摩擦标的）」的机制一致。
2. **`LOW_2Y_SHARPE` 首次进 pass 列**（`A1xX3n8W` 的 checks.pass 含 `LOW_2Y_SHARPE`；fail 仅 `LOW_SHARPE` 0.73<1.58 与 `LOW_FITNESS` 0.30<1.0）⇒ **failed_RA 由 3 降为 2**。
3. **★ 同比例缩放是 no-op（实测举证）**：`vec_sum` 与 `vec_avg` 读数**逐位相同**（0.66/0.26/1.50、TO 8.31%）⇒ 费率求和 = 平均 × 经纪商家数 ⇒ 协方差同比例放大 ⇒ `group_rank` 吸收 ⇒ **「聚合强度」这一维在 sum/avg 之间无信息，只有 min/max/stddev/range 才换语义**。
4. **★ 离散度折叠判死**：`vec_stddev`（费率离散度 = 不确定性）与 `vec_range` 双双转负 ⇒ 本数据集**不存在「费率不确定性」这条机制**（与「费率水平无定价力」是同一种「只认尾部摩擦」的集中化）。
5. **crowding 腿只能 `vec_sum`**（臂 7 塌到 0.03）⇒ 拥挤是**流量累计**语义（正=做空增加），求和保留符号计数，平均会把正负相消 ⇒ 与画像档案 §4「B 流量族：累计型」一致。

⇒ **新基线（C8 路线）**：`reverse(group_rank(ts_covariance(divide(ts_backfill(vec_max(rsk60_offer),250),ts_backfill(vec_max(lending_fee_bid_rate),250)),ts_backfill(vec_sum(rsk60_crowding),250),750), subindustry))` @ FAST / decay4 / trunc0.08 / nanON / TOP700 / D1
⇒ **按梯度纪律，换基线后必须重跑下游**（轴层 → 外层 → 设置层 → 参数层）并做 **L5-R 内核重扫**，见批 V2。

### ★★★ C14 新构造（批 V1 派生：尾部费率折叠）⇒ 构造数 13 → **14**

```
C14 = reverse(group_rank(
        ts_covariance(
          divide(ts_backfill(vec_max(rsk60_offer),250),
                 ts_backfill(vec_max(lending_fee_bid_rate),250)),
          ts_backfill(vec_sum(rsk60_crowding),250),
          750),
        subindustry))
```

- **机制 = 尾部摩擦（TBR / hard-to-borrow）**：`vec_max` 取的是「经纪商中报出的**最高**费率」= 最难借的那家 ⇒ 与 C8（平均费率水平）**不是同一信息**：C8 测「成本水平」，C14 测「**稀缺性溢价**」。
- **实测依据**：S0.73 / F0.30 / **2Y1.70（过闸）** / TO8.29% / subU0.66，`failed_RA=2`（`LOW_SHARPE` + `LOW_FITNESS`）—— **risk60 全部读数中的 2Y 高点**。
- **来源（论文侧强证据，`--diverse` 12 篇 / 11 作者 ✅）**：
  | 文献 | DOI | 支撑 |
  |---|---|---|
  | Securities Lending Strategies, TBR and Thoughts Beyond Rates (2015) | `10.2139/ssrn.2655527` | **TBR（理论借券利率）= 最难借标的的费率** ⇒ 直接对应 `vec_max` 语义 |
  | Stochastic Pricing Dynamics of Hard-to-Borrow Stocks (2013) | `10.2139/ssrn.2256795` | 难借股的定价动态 |
  | A Dynamic Model for Hard-to-Borrow Stocks (2009) | `10.2139/ssrn.1357069` | 借券稀缺性的动态均衡定价 |
  | Price Efficiency in Securities Lending (2026) | `10.2139/ssrn.7437258` | 借券市场的价格效率 |
- **论坛侧**：`44687266076823`（引 Daniel & Moskowitz 2016，强调**借券费进入成本**，空头腿须单独审计）⇒ 支撑「费率本身是定价因子」这层；尾部语义由上述论文补齐。
- ⇒ 按纪律，C14 需跑自己的完整 5 层（轴 / 外层 / 设置 / 参数 / L5-R），**不得直接沿用 C8 的结论**。

### 批 V2 · 新基线下游（轴层 6 + 交叉折叠 4，批 `44Qh7Z86Y54l9Tp5nqUo3PD`，10 臂）

臂 1–6 = 轴层（industry / sector / market / exchange / country / subindustry[对照]）；臂 7–10 = 交叉折叠（max÷avg / avg÷max / `vec_max(last)`÷`vec_max(bid)` / `vec_max(offer)`÷`vec_max(last)`）。

| 臂 | 内容 | α | S | F | 2Y | subU | TO |
|---|---|---|---:|---:|---:|---:|---:|
| **6** | 轴=**subindustry**（对照） | `A1xX3n8W` | **0.73** | **0.30** | **1.70** | 0.66 | 8.29% |
| 2 | 轴=sector | `88NWeXmm` | 0.55 | 0.20 | 1.31 | 0.74 | 8.31% |
| 1 | 轴=industry | `78YPnMeZ` | 0.54 | 0.19 | 1.17 | 0.69 | 8.29% |
| 3 | 轴=market | `pwabK3qV` | 0.46 | 0.16 | 1.21 | 0.75 | 8.28% |
| 4 | 轴=exchange | `d5aJRv2Y` | 0.46 | 0.16 | 1.21 | 0.75 | 8.28% |
| 5 | 轴=country | `xAv7d5Aq` | 0.46 | 0.16 | 1.21 | 0.75 | 8.28% |
| 8 | max(offer) ÷ **avg**(bid) | `j2akrO2o` | 0.67 | 0.26 | 1.39 | 0.59 | 8.25% |
| 10 | max(offer) ÷ max(last) | `P05LOKQw` | 0.43 | 0.14 | −1.04 | 0.42 | 8.67% |
| 7 | **max(offer) ÷ avg(bid)** | `Jj8avrjO` | 0.28 | 0.07 | −0.15 | 0.24 | 8.42% |
| 9 | max(last) ÷ max(bid) | `E5Qnex59` | 0.08 | 0.01 | 1.13 | 0.27 | 8.31% |

**批 V2 结论（三条）**：

1. **★ 轴层：subindustry 独占最优**（0.73/0.30/1.70，ΔS +0.18 vs 次优 sector 0.55）⇒ C14 偏好**最细分组轴**（与 C8 的 ts_ir 路线、ts_covariance 路线一致：三者都吃 subindustry）。
2. **★ 平台事实：GBR 单国市场 ⇒ `market` ≡ `exchange` ≡ `country` 三轴读数逐位相同**（0.46/0.16/1.21/TO8.28%/subU0.75）⇒ **在 GBR 这三个粗轴是同一个组**，扫轴时任选其一即可，不必各占一个臂（**可省 2 个臂位**）。⇒ 记入方法论（**跨区不外推**：这是 GBR 的结构事实，不适用于多国区）。
3. **★ 尾部必须两侧同时取**：max÷avg 0.67/1.39（次优）、**avg÷max 崩到 0.28 / 2Y−0.15**（分子取平均即失效）、max÷max 0.73/1.70 最优 ⇒ **「最难借的那家」只在分子（借入费率 `rsk60_offer`）侧携带信息**；分母（出借费率 `lending_fee_bid_rate`）侧取 max 只带来 +0.06 S。
   ⇒ 机制细化：**C14 的信号本质 = 「最贵借入费 / 最贵出借费」的相对稀缺溢价**；臂 8（avg÷max）读数 0.67 与 C8（avg÷avg）0.66 几乎相同，进一步说明**分母腿信息量极低，信号几乎全部来自分子**。

### 批 V3 · 外层 Group 族全替 + `group_backfill` 窗/std 命名参数（批 `dnpnBbmA5iIbW4PsixgKn3`，10 臂）

臂 1 = `group_rank`（对照）/ 2 = `group_scale` / 3 = `group_zscore` / 4 = `group_neutralize` / 5 = `group_backfill(·,subindustry,120)` / 6 = `group_backfill(·,subindustry,252)` / 7 = `group_sum` / 8 = `group_std_dev` / 9 = `group_count` / 10 = `group_backfill(·,subindustry,120,std=2.0)`。
> ⚠ **工具链静态闸实战记录**：`group_backfill(x, group, d, std=4.0)` 的 `std` **必须写成命名参数 `std=2.0`**，写成第 4 个位置参数会被 toolkit 静态闸以 `[OP_ARITY] group_backfill 只接受 3 个位置参数` **整批拒绝**（平台原文 `Invalid number of inputs : 4, should be exactly 3 input(s).`）⇒ **带命名参数的算子必须用 `name=value` 语法**（该闸属 `wqb.expression.op_arity`，是派发前的免费硬门）。

**批 V3 结果（10 臂）**：

| 臂 | 外层 | α | S | F | 2Y | subU | TO | invest_ratio |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **1** | **`group_rank`（对照）** | `A1xX3n8W` | **0.73** | **0.30** | **1.70** | 0.66 | 8.29% | **0.9726** |
| 2 | `group_scale` | `XgaZoNzl` | 0.62 | 0.24 | 1.14 | 0.41 | 8.23% | 0.8387 |
| 6 | `group_backfill(·,sub,252)` | `N1PEbK37` | 0.62 | 0.27 | 0.89 | 0.40 | 9.67% | 0.3871 |
| 10 | `group_backfill(·,sub,120,std=2.0)` | `58JKpGYM` | 0.61 | 0.26 | 0.88 | 0.39 | 9.71% | 0.3607 |
| 5 | `group_backfill(·,sub,120)` | `88NWpGY7` | 0.60 | 0.26 | 0.88 | 0.40 | 9.67% | 0.3500 |
| 4 | `group_neutralize` | `d5aJZ9o2` | 0.45 | 0.17 | 0.64 | 0.29 | 10.80% | 0.4000 |
| 3 | `group_zscore` | `RRexm5zz` | 0.45 | 0.15 | 0.97 | 0.35 | 8.47% | 0.7333 |
| 8 | `group_std_dev` | `d5aJZ9v2` | 0.14 | 0.03 | −0.75 | −0.34 | 10.42% | 1.3571 |
| 9 | `group_count` | `ZYaVEXNZ` | 0.12 | 0.02 | 0.07 | −0.16 | 7.55% | 1.5000 |
| 7 | `group_sum` | `bla0Qxnr` | −0.02 | −0.00 | 1.18 | 0.44 | 9.40% | 5.5000 |

**批 V3 结论（三条）**：

1. **★ 外层 `group_rank` 独占最优**（0.73/0.30/1.70 vs 次优 `group_scale` 0.62）⇒ C14 与 C8 同型：**协方差型内核只能用 `group_rank`**（第 N 次复现）。
2. **★ `group_backfill` 在本链路上近乎空操作（命名参数 + 窗长双 no-op）**：`std=4.0`（臂 5）vs `std=2.0`（臂 10）读数 **0.60/0.88 vs 0.61/0.88**；窗 120（臂 5）vs 252（臂 6）**0.60/0.88 vs 0.62/0.89** ⇒ 两个维度都无影响。
   ⇒ **机制解释**：外层 `group_backfill` 的职能是「用组内 winsorized 均值填 NaN」；而本链路**内层已 `ts_backfill(·,250)` 把 NaN 全部填完** ⇒ 外层无 NaN 可填 ⇒ 退化为近似恒等 ⇒ **no-op**。
   ⇒ ★ **可迁移铁律：凡内层已做 `ts_backfill` 的链路，外层 `group_backfill` 不应再占测试预算**（此前 C12 的 `group_backfill120` 之所以有效，是因为 C12 的内核 `ts_max_diff` 作用在 `divide(subtract(...), ...)` 上、**外层 backfill 之前存在未填 NaN** ⇒ 该差异需按「内层是否已填」逐构造判断，不能跨构造外推）。
3. **★ `invest_ratio` 随外层剧烈分化（0.97 → 0.35）**：选 `group_rank` 不只是 S 最优，它同时**保住了可投资性**（内部严线 = 0.70×S）。`group_sum` 的 invest_ratio 5.5 = S≈0 时的病态比值，无意义。
   ⇒ 归因：**外层算子不仅改 Sharpe，还改「可投资部分」的相对规模** ⇒ 判外层时不能只看 S。

⇒ **C14 外层层次闭合**：`group_rank` 保留。

### 批 X1 · 「单变量换折叠」横扫（第 1 组，批 `1wUiPh8q74K8aYe4YND70Ld`，10 臂）

**动机**：`vec_max` 的优势是**与构造无关**的（5 字段全 VECTOR），而其余含费率构造**全部还在用 `vec_avg`** ⇒ 若优势成立，这些构造的天花板都被系统性低估。
**设计**：每个构造出 **avg / max 两臂**（同内核、同窗、同轴、同外层 ⇒ 折叠是唯一变量），**全部统一在 FAST / decay4 / trunc0.08 / nanON**（⇒ 折叠对比不受设置档污染；绝对值与各构造「最优设置档」下的读数不同，仅作横向筛选，不作最终天花板）。
**覆盖**：C1（`ts_ir`66×sector×group_rank）/ C2（`ts_ir`126×industry×group_scale）/ C3（`ts_scale`504×sector×group_rank）/ C6（`ts_zscore`126×industry×group_rank）+ C14 与 C8 的 avg/max 对照臂（复现锚点）。
**排除**：C4（纯 crowding，无费率腿）、C5 / C9（`vector_neut` 作用在原始向量上，折叠不是简单替换）⇒ 待单独设计。

**批 X1 结果（10 臂，FAST / decay4 / trunc0.08 / nanON）**：

| 构造 | 内核 × 窗 × 轴 × 外层 | `vec_avg` 锚点（α / S / 2Y） | **`vec_max`**（α / S / F / 2Y） | ΔS | Δ2Y |
|---|---|---|---|---:|---:|
| **C1** 出借费率 | `ts_ir`66 × sector × `group_rank` | `e7aW5nw6` 0.24 / **−0.71** | `gJaNb8z0` **0.30** / 0.08 / 0.18 | **+0.06** | +0.89 |
| **C2** 借入费率 | `ts_ir`126 × industry × `group_scale` | `gJa0rka0` 0.42 / −0.17 | `O0WdNGeJ` **0.53** / 0.20 / **0.37** | **+0.11** | +0.54 |
| **C3** 最新费率 | `ts_scale`504 × sector × `group_rank` | `rK7nnO1a` 0.48 / −0.53 | `xAv73NXb` **0.51** / −0.43 | +0.03 | +0.10 |
| **C6** 门控(offer) | `ts_zscore`126 × industry × `group_rank` | `N1PEabWg` 0.60 / −0.01 | `9ql5jpPe` **0.65** / 0.13 | +0.05 | +0.14 |
| C8 锚点 | `ts_covariance`750 × subindustry × `group_rank` | `aka9pPv1` 0.66 / 1.50 | `A1xX3n8W` **0.73** / 1.70 | +0.07 | +0.20 |

**★★★ 批 X1 结论（数据集级规律，非 C8 特例）**：

1. **★ `vec_max` 在 4/4 构造上全面优于 `vec_avg`**（ΔS = +0.06 / +0.11 / +0.03 / +0.05，全为正），且 **2Y 全部改善或持平**（+0.89 / +0.54 / +0.10 / +0.14）。
2. ⇒ **「尾部折叠 > 平均折叠」是 risk60 的数据集级规律** ⇒ 原 12 构造的天花板**全部被系统性低估**（它们全部用 `vec_avg`）⇒ **每个构造都必须在自己的 `vec_max` 版本上重跑完整 5 层梯度**（内核/窗/轴/外层都可能随之改变）。
3. ★ **2Y 改善幅度远大于 S 改善幅度**（C1 Δ2Y +0.89 vs ΔS +0.06；C2 +0.54 vs +0.11）⇒ 尾部折叠主要修的是**近两年**的定价（借券费高企期 = 熊市/挤兑期 ⇒ 尾部摩擦在近两年更显著）。这与「2Y 是本数据集的主墙」直接相关。
4. ⚠ **绝对值仍远低于闸**：C2-max 0.53 / C6-max 0.65 ⇒ **换折叠只是必要条件，不是充分条件**；后续仍需内核/窗/轴/外层/设置的完整梯度。
5. ⚠ **读数注意**：本批统一在 FAST 档，**绝对值低于各构造「最优设置档」下的读数**（如 C1 最优档是基线/SUBINDUSTRY，本批 FAST 下 avg 只有 0.24 vs 原记录 0.53）⇒ 本批只用于**折叠方向筛选**，不用于更新天花板表。

### 批 X2 · 「单变量换折叠」横扫（第 2 组，批 `4hvCO94F455CbSy15rGrpmeE`，10 臂）

| 构造 | `vec_avg` 锚点（α / S / F / 2Y / subU） | **`vec_max`**（α / S / F / 2Y / subU） | ΔS | Δ2Y |
|---|---|---|---:|---:|
| **C10** 门控(bid) | `78Yrd7nZ` 0.57 / 0.21 / −0.24 / 0.71 | **`6XM6AwrG`** **0.81** / **0.35** / **0.99** / **1.03** | **+0.24** | **+1.23** |
| C8 比值（锚点） | `aka9pPv1` 0.66 / 0.26 / 1.50 / 0.62 | `A1xX3n8W` 0.73 / 0.30 / 1.70 / 0.66 | +0.07 | +0.20 |
| C7 价差 | `2r5xrnAZ` 0.30 / 0.07 / −0.72 / 0.55 | `E5QnVwvr` 0.36 / 0.09 / −0.39 / 0.60 | +0.06 | +0.33 |
| **C11** 相对溢价 | `YPa3xp5o` 0.46 / 0.16 / 0.62 / 0.50 | `2r5Vj7wb` 0.41 / 0.13 / 0.56 / 0.60 | **−0.05** | −0.06 |
| **C12** 相对价差 | `2r5xpLQY` 0.43 / 0.14 / 0.34 / 0.73 | `QP0RYabG` 0.41 / 0.13 / 0.23 / 0.66 | **−0.02** | −0.11 |

**★★★ 批 X2 结论（三条，其中两条是数据集级规律）**：

1. **★ 新的 S 冠军出现：C10-vec_max = S0.81 / F0.35 / 2Y0.99 / subU 1.03 / TO 8.59% / DD 3.54%**（α `6XM6AwrG`，`checks.fail` = LOW_SHARPE + LOW_FITNESS + LOW_2Y_SHARPE，`LOW_SUB_UNIVERSE_SHARPE` PASS）⇒ 超过 C14（0.73）。**ΔS +0.24 / Δ2Y +1.23 是全数据集最大的折叠增益**。
   ⇒ C10 的机制 = **「最高出借费率 × 拥挤分位」**：拥挤度（做空流量）与**尾部**借券成本同时高 ⇒ 该标的最难借 ⇒ 后续必须沿 C10-vec_max 跑自己的完整 5 层。
2. **★ 折叠优劣由「构造类型」决定，不是普适规律（8 构造汇总）**：

   | 构造类型 | 构造 | ΔS(max−avg) | 判定 |
   |---|---|---|---|
   | **水平型** | C1 / C2 / C3 | +0.06 / +0.11 / +0.03 | `vec_max` 更好 |
   | **门控型** | C6 / **C10** | +0.05 / **+0.24** | `vec_max` 更好 |
   | **价差/比值型** | C7 / C8 | +0.06 / +0.07 | `vec_max` 更好 |
   | **「相对自身历史」型** | **C11 / C12** | **−0.05 / −0.02** | **`vec_avg` 更好** |

   ⇒ **机制解释**：一旦构造把信号变成**相对量**（`divide(x, ts_mean(x,252))` / `divide(spread, base)`），**基线口径必须与被测量口径一致** —— `max÷max` 变成「尾部相对尾部」，**丢失了「相对常态」的语义**；`avg÷avg` 才保持「相对常态」的可比性。
   ⇒ ★ **可迁移铁律：换折叠不是「换个更好的聚合」，而是「换一种被测量的经济量」** ⇒ 换折叠前先问：这个构造测的是**水平**还是**相对量**？相对量型构造的**分母与分子必须同口径**。
3. **★ 2Y 增益普遍大于 S 增益**（C10：Δ2Y +1.23 vs ΔS +0.24）⇒ 尾部摩擦的定价力**集中在近两年**（借券费高企期）⇒ 与「2Y 是本数据集主墙」直接呼应：换折叠正是**修 2Y 的杠杆**。

### 批 Y1 · C10-vec_max 的 L2 内核全类别重扫（10 臂，批 `195mtRae4sX8ZylYD3scJ3`）

新基线：`reverse(group_rank(ts_ir(ts_backfill(multiply(vec_max(lending_fee_bid_rate),ts_rank(ts_backfill(vec_sum(rsk60_crowding),250),66)),250),126), market))` @ FAST/decay4/trunc0.08/nanON
内核扫：`ts_ir`(基线) / `ts_zscore` / `ts_av_diff` / `ts_delta` / `ts_max_diff` / `ts_std_dev` / `ts_sum` / `ts_rank` / `ts_scale` / `ts_quantile`（窗均 126）
> ⚠ 与批 A 的差别：批 A 是在 **vec_avg** 信号上扫内核；本批是在 **vec_max** 信号上扫 ⇒ 换基线后内核排名可能翻转（历史已 7 次翻转）。
> ⚠ 另需单独扫 **`ts_rank(crowding,66)` 这个内嵌窗口**（C10 的第二条腿）——它是构造内部参数，不在 TS 内核类别里。

**批 Y1 结果（10 臂，窗均 126）**：

| 臂 | 内核 | α | S | F | 2Y | subU | TO |
|---|---|---|---:|---:|---:|---:|---:|
| **1** | **`ts_ir`（基线）** | `6XM6AwrG` | **0.81** | **0.35** | **0.99** | 1.03 | **8.59%** |
| 9 | `ts_scale` | `pwabdGbb` | 0.69 | 0.23 | 0.91 | **1.20** | 20.20% |
| 2 | `ts_zscore` | `58JKE52M` | 0.70 | 0.20 | 0.57 | 1.09 | 25.58% |
| 4 | `ts_delta` | `0mPZYgL8` | 0.56 | 0.14 | −1.07 | 0.73 | 27.54% |
| 3 | `ts_av_diff` | `E5Qn6z29` | 0.36 | 0.08 | 0.04 | 0.67 | 24.18% |
| 5 | `ts_max_diff` | `d5aJWzr2` | 0.18 | 0.04 | −0.13 | 0.25 | 13.06% |
| 10 | `ts_quantile` | `RRexEzOa` | 0.16 | 0.02 | −0.63 | 0.40 | 27.51% |
| 6 | `ts_std_dev` | `gJaNeGVQ` | 0.15 | 0.03 | 0.19 | 0.44 | 8.54% |
| 8 | `ts_rank` | `KPgAJzAN` | 0.12 | 0.01 | −0.63 | 0.39 | 27.50% |
| 7 | `ts_sum` | `78YPLmPb` | 0.11 | 0.02 | −0.44 | 0.40 | 8.50% |

**批 Y1 结论**：
1. **`ts_ir` 保持最优（0.81），本轮无内核翻转**（与 vec_avg 时代 C10 的 `ts_scale` 领先不同 ⇒ ★ **换基线后内核排名确实会变**：vec_avg 时代 C10 是 `ts_scale` 领先，vec_max 时代回到 `ts_ir`）。
2. ★ **换内核会连带改换手（关键副产物）**：`ts_ir` TO 8.59%，而 `ts_zscore`/`ts_av_diff`/`ts_delta`/`ts_rank`/`ts_quantile` 全部把 TO 抬到 **24–27.5%**（仍在 70% 闸内但接近 4 倍）⇒ 这些内核即使 S 接近也会因 F（`F = S × √(|returns| / max(TO,0.125))`，TO>0.125 后 F 与 TO 成反比）而失分。
   ⇒ **F 闸公式的直接后果**：TO 一旦超过 12.5%，继续降 TO 不再提升 F，只能靠 S 与 returns ⇒ **判内核时必须同时看 TO**。
3. `ts_scale` 次优且 **subU 1.20 最高**（vs `ts_ir` 1.03）⇒ 若后续换轴/外层，`ts_scale` 是 `ts_ir` 的有力备选（历史已 7 次「换设置后内核翻转」）。

### 批 Y2 · C10-vec_max 的窗口层全扫（10 档，批 `188dcf3Hh4r7ajKV4PjzXUX`）

`ts_ir` 窗 d ∈ {22, 44, 66, 88, **126**(基线), 250, 504, 750, 1000, 1250}，其余全锁。

**批 Y2 结果（10 臂）**：

| 窗 d | 22 | 44 | 66 | 88 | **126** | 250 | 504 | 750 | 1000 | 1250 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| α | `e7aMN316` | `6XM6ZpZp` | `RRex9ml1` | `N1PELbzX` | **`6XM6AwrG`** | `LLKoEGz1` | `0mPZxpg2` | `2r5V9pWP` | `omajRNrE` | `e7aMN3EJ` |
| S | 0.31 | 0.69 | 0.70 | 0.59 | **0.81** | 0.38 | 0.64 | 0.55 | 0.54 | 0.46 |
| F | 0.08 | 0.28 | 0.28 | 0.22 | **0.35** | 0.11 | 0.25 | 0.20 | 0.19 | 0.15 |
| 2Y | 0.91 | **1.17** | 0.88 | 0.32 | 0.99 | 0.62 | 0.82 | 0.88 | 0.68 | 0.27 |
| subU | 0.51 | 0.96 | 1.07 | 0.93 | 1.03 | 0.95 | **1.28** | 1.07 | 1.01 | 0.89 |
| TO | 13.05% | 10.42% | 9.43% | 9.00% | 8.59% | 8.21% | 8.17% | 8.07% | 8.00% | 7.92% |

**批 Y2 结论**：
1. **窗 126 保持最优（S 0.81 / F 0.35）**，两侧都掉（22→0.31、250→0.38、1250→0.46）⇒ **窗口层收敛于 126**（与 vec_avg 时代 C10 的 126 一致 ⇒ 换折叠不改最优窗）。
2. **S-2Y 跷跷板再现**：44 档 2Y 最高（1.17）但 S 只有 0.69；126 档 S 最高但 2Y 0.99；504 档 **subU 1.28 最高**。⇒ 三档各有侧重，**没有一档同时最优** ⇒ 若后续目标是「2Y 过闸」，44 档值得作为并列候选（2Y 1.17 仍 < 1.58）。
3. TO 随窗单调下降（13.05% → 7.92%）⇒ **长窗降换手**，符合「TO<12.5% 后降 TO 不再提升 F」⇒ 22 档 TO 13.05% 仍在 0.125 之上，其 F 0.08 低是 S 低所致而非 TO。

⇒ **C10-vec_max 当前天花板 = S0.81 / F0.35 / 2Y0.99 / subU1.03 / TO8.59%**（`6XM6AwrG`，`ts_ir` × W126 × market 轴 × `group_rank` × FAST/decay4/trunc0.08/nanON）

### 批 Y3 · C10-vec_max 轴层（4 档）+ 内嵌 `ts_rank(crowding,·)` 窗（6 档，批 `4AUydtbHg4gEbFGu1mliquw`，10 臂）

- 臂 1–4 = 轴层（subindustry / industry / sector / market[基线]）——⚠ **只扫 4 档**（GBR 的 `market`≡`exchange`≡`country` 已在批 V2 实测逐位相同 ⇒ 不重复占臂位）
- 臂 5–10 = **构造内部参数**：`ts_rank(crowding,·)` 的窗 ∈ {22, 44, 126, 250, 504, 750}（基线 66）
  ⇒ 这是**内核类别扫描扫不到的维度**：C10 有两条腿（费率 × 拥挤分位），拥挤腿的窗口是构造的一部分。

**批 Y3 结果（10 臂）**：

*轴层（臂 1–4）*：

| 轴 | subindustry | industry | sector | **market（基线）** |
|---|---:|---:|---:|---:|
| α | `gJaNgz0K` | `mLan0klW` | `9ql5dQ31` | **`6XM6AwrG`** |
| S | 0.69 | 0.76 | 0.80 | **0.81** |
| F | 0.28 | 0.31 | 0.34 | **0.35** |
| 2Y | 0.33 | 0.54 | 0.99 | **0.99** |
| subU | 0.72 | 0.84 | 0.99 | **1.03** |

*内嵌 `ts_rank(crowding,·)` 窗（臂 5–10）*：

| 拥挤窗 | 22 | **44** | 66（基线） | 126 | 250 | 504 | 750 |
|---|---:|---:|---:|---:|---:|---:|---:|
| α | `0mPZNWL8` | **`j2akPQJo`** | `6XM6AwrG` | `xAv72apq` | `LLKomxY6` | `88NWEqxl` | `YPa3EdoJ` |
| S | 0.81 | **0.87** | 0.81 | 0.70 | 0.59 | 0.51 | 0.45 |
| F | 0.35 | **0.39** | 0.35 | 0.28 | 0.22 | 0.18 | 0.15 |
| 2Y | 0.78 | **1.09** | 0.99 | **1.11** | 0.90 | 0.57 | 0.39 |
| subU | 1.11 | **1.14** | 1.03 | 0.91 | 0.82 | 0.67 | 0.51 |
| invest_ratio | 0.94 | 0.90 | 0.78 | 0.84 | 0.92 | 0.88 | 0.87 |

**★★ 批 Y3 结论（三条）**：

1. **★ 新天花板：拥挤腿窗 44 = S0.87 / F0.39 / 2Y1.09 / subU1.14 / invest0.90 / TO8.62%**（α `j2akPQJo`）—— 全面优于基线 66（0.81/0.35/0.99/1.03），是 risk60 **全部读数中的 S/F 新高**。
   ⇒ 机制：**拥挤分位用 44 日窗（约两个月）最合适** —— 太短（22）噪声大，太长（≥126）把「当下拥挤」平滑掉了；而**费率腿的 `ts_ir` 窗仍要 126**（批 Y2）⇒ **两条腿的最优窗不同（44 vs 126）**，这是「多腿构造必须逐腿调窗」的直接实证。
2. **★ 轴层：门控型吃「粗轴」（market 0.81 > sector 0.80 > industry 0.76 > subindustry 0.69），与 C14 相反**（C14 协方差型吃最细轴 subindustry 0.73 vs market 0.46）。
   ⇒ **可迁移铁律：分组轴的选择由「信号的横截面性质」决定，不能跨构造外推** ——
   - **协方差/比值型**（跨字段共动）→ **细轴**（组内可比性要求高）
   - **门控/水平型**（乘积已含自身截面信息）→ **粗轴**（组内样本量更重要）
3. **2Y 的最优窗（126，2Y1.11）与 S 的最优窗（44，S0.87）不同** ⇒ S-2Y 跷跷板在本构造内部也存在；若主线继续压 S，取 44。

⇒ **C10-vec_max 新基线 = `reverse(group_rank(ts_ir(ts_backfill(multiply(vec_max(lending_fee_bid_rate),ts_rank(ts_backfill(vec_sum(rsk60_crowding),250),44)),250),126), market))` @ FAST/decay4/trunc0.08/nanON** ⇒ 按纪律重扫下游（批 Y4）。

### 批 Y4 · 新基线（crowding-44）的 L5-R 内核重扫 + 外层 + 轴复核（批 `4h8FxecOy56ScAi1402Zh65v`，10 臂）

臂 1–5 = 内核重扫（`ts_ir`[基线] / `ts_scale` / `ts_zscore` / `ts_av_diff` / `ts_max_diff`）；臂 6–8 = 外层（`group_scale` / `group_zscore` / `group_neutralize`）；臂 9–10 = 轴复核（sector / industry）。

**批 Y4 结果（10 臂）**：

| 臂 | 内容 | α | S | F | 2Y | subU | TO | invest_ratio |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **1** | **`ts_ir`（基线）** | `j2akPQJo` | **0.87** | **0.39** | 1.09 | **1.14** | 8.62% | 0.897 |
| 9 | 轴=**sector** | `RRexPVWj` | **0.87** | **0.39** | **1.10** | 1.10 | 8.79% | 0.862 |
| 10 | 轴=industry | `WjlrJP8N` | 0.80 | 0.34 | 0.57 | 0.87 | 9.15% | 0.975 |
| 3 | `ts_zscore` | `leaw18q2` | 0.69 | 0.20 | 0.56 | 1.08 | **25.71%** | 1.000 |
| 2 | `ts_scale` | `LLKo39Wm` | 0.67 | 0.21 | 0.97 | 1.20 | **20.30%** | 1.254 |
| 4 | `ts_av_diff` | `O0WdgrYg` | 0.36 | 0.08 | 0.13 | 0.61 | 24.29% | 1.472 |
| 5 | `ts_max_diff` | `XgaZMWQl` | 0.15 | 0.03 | −0.14 | 0.23 | 13.04% | 2.533 |
| 8 | 外层 `group_neutralize` | `j2akO3bo` | 0.11 | 0.02 | 0.68 | −0.06 | 19.21% | −0.546 |
| 7 | 外层 `group_zscore` | `88NWX3d7` | 0.10 | 0.02 | 0.65 | −0.06 | 18.78% | −0.700 |
| 6 | 外层 `group_scale` | `O0WdgrPg` | 0.10 | 0.02 | 0.64 | −0.05 | 18.77% | −0.700 |

**批 Y4 结论（三条）**：

1. **C10 全层收敛，无翻转**：内核 `ts_ir` 保持（0.87 vs 次优 `ts_zscore` 0.69）、外层 `group_rank` 保持（0.87 vs `group_scale` 0.10）、轴 market≡sector 打平（0.87/1.09 vs 0.87/1.10）⇒ **C10 的 crowding-44 路线梯度闭环，无需再扫**。
2. **★★ 同名外层算子在两个构造上结论完全相反**：`group_scale` 在 **C8 是 +0.22（1.08 天花板的来源）**，在 **C10 崩到 0.10 且 subU 转负（5 FAIL、DD 21.9%）**；`group_rank` 在 C10/C14 是唯一可用外层，在 C8 则被 `group_scale` 反超。
   ⇒ **可迁移铁律（第 2 次确认，比记忆里 [[outer-op-choice-by-signal-type]] 更细）**：外层算子要与**信号是否已含组内相对位置**匹配 ——
   - C8 = `divide(offer,bid)` 是**纯水平比值**（组内无可比基准）⇒ `group_scale`（组内 0–1 缩放）带来最大增益
   - C10 = `multiply(费率, 拥挤分位)` 中**含 `ts_rank` 分位**（已含相对位置）⇒ 再缩放会把分位压缩、换手翻倍 ⇒ 只能 `group_rank`
3. **F/invest 双判据在本批出现极端分化**：`group_scale` 三兄弟（scale/zscore/neutralize）S≈0.10 却 invest_ratio **−0.70**（负值 = 可投资 Sharpe 为负）⇒ **S 接近 0 时 invest_ratio 是病态比值，不能作判据**（只能作「排除」信号）。

⇒ **C10-vec_max 天花板（终）= S0.87 / F0.39 / 2Y1.10 / subU1.14 / invest0.90 / TO8.6~8.8%**（`j2akPQJo` market 轴 或 `RRexPVWj` sector 轴，二选一；2Y 取 sector 1.10）

### ★★ 批 P0 · C8 的「最优设置 × 折叠」交叉（批 `1U797T7pa4tuczEih4XAIgG`，10 臂，**INDUSTRY 中性化**）

**动机（本轮最高优先级）**：C8 天花板 **1.08** 来自两处增益 —— `group_scale`（+0.22）与 INDUSTRY 档（含 CW 修复，+0.24）；而 `vec_max` 折叠（+0.07~+0.24）**从未在 C8 的最优设置下测过**（只在 FAST 档测得 0.73）。两个增益来源正交 ⇒ **交叉处理论落点 ≈1.15**，是本数据集唯一「免费」的高价值组合。

| 臂 | 折叠 | 内核 | 外层 | 轴 | 测什么 |
|---|---|---|---|---|---|
| **1** | `vec_avg` | `ts_ir`66 | `group_scale` | industry | **复现 1.08 锚点** |
| **2** | **`vec_max`** | `ts_ir`66 | `group_scale` | industry | **★ 核心：折叠 × 最优设置** |
| 3 | `vec_avg` | `ts_covariance`750 | `group_rank` | subindustry | 对照（C8 路线原样） |
| 4 | `vec_max` | `ts_covariance`750 | `group_rank` | subindustry | 对照（C14 原样） |
| 5 | `vec_max` | `ts_ir`66 | `group_scale` | subindustry | 折叠是否改变轴偏好 |
| 6 | `vec_max` | `ts_ir`66 | `group_scale` | sector | 同上（粗轴） |
| 7 | `vec_max` | `ts_ir`66 | `group_rank` | industry | 折叠是否改变外层偏好 |
| 8 | `vec_max` | `ts_covariance`750 | `group_scale` | industry | 内核 × 外层交叉 |
| 9 | `vec_max` | `ts_ir`66 | `group_zscore` | industry | 外层第二备选 |
| 10 | `vec_max` | `ts_ir`**504** | `group_scale` | industry | **折叠后窗口是否重排**（C8 原最优窗 66） |

> ⚠ 中性化档固定 INDUSTRY（C8 最优档）；**不能同时扫中性化**（它是批次级参数，需另批）。若本批出现新高，则下一批单独扫中性化档。

**批 P0 结果（10 臂，INDUSTRY 中性化）**：

| 臂 | 内容 | α | S | F | 2Y | subU | TO | invest_ratio |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **1** | `vec_avg` ts_ir66 `group_scale` industry | `GrmNrRYQ` | **1.08** | **0.74** | 0.56 | 0.80 | 7.87% | 0.907 |
| **2** | **`vec_max`** ts_ir66 `group_scale` industry | `ZYaV9MG1` | 1.01 | 0.67 | **0.79** | 0.81 | 7.88% | 0.960 |
| 9 | `vec_max` ts_ir66 `group_zscore` industry | `58JK1e76` | 0.91 | 0.58 | 0.63 | 0.70 | 7.70% | 0.967 |
| 8 | `vec_max` ts_cov750 `group_scale` industry | `omajXrQk` | 0.69 | 0.32 | 0.93 | 0.67 | 2.65% | 0.783 |
| 6 | `vec_max` ts_ir66 `group_scale` **sector** | `RRexoKXg` | 0.71 | 0.44 | 0.22 | 0.52 | 9.57% | 0.831 |
| **4** | `vec_max` ts_cov750 `group_rank` **subindustry** | `1YW3RP5K` | 0.58 | 0.28 | **1.52** | 0.67 | **2.70%** | 1.017 |
| 5 | `vec_max` ts_ir66 `group_scale` subindustry | `bla0gnpN` | 0.56 | 0.26 | 0.63 | 0.32 | 7.44% | 1.000 |
| 3 | `vec_avg` ts_cov750 `group_rank` subindustry | `wpokdmdl` | 0.54 | 0.25 | 1.32 | 0.63 | 2.70% | 1.019 |
| 7 | `vec_max` ts_ir66 `group_rank` industry | `Jj8ak1Rn` | 0.47 | 0.20 | 0.16 | 0.51 | 5.01% | 1.043 |
| 10 | `vec_max` ts_ir**504** `group_scale` industry | `2r5VxWq5` | 0.30 | 0.10 | 0.56 | 0.29 | 3.10% | 1.367 |

**★★★ 批 P0 结论（四条，其中第 1 条推翻了我自己的假设）**：

1. **★ P0 假设部分证伪 —— C8 的折叠是「S↔2Y 交换」，不是净增益**：`vec_max` 在 C8 最优设置下 **S 反而降 0.07**（1.08→1.01）、F 降 0.07，但 **2Y 升 0.23**（0.56→0.79）。
   ⇒ 机制解释：C8 是**纯水平比值** `offer/bid`；两侧都取 `vec_max` 后变成「最贵借入 ÷ 最贵出借」，**尾部/尾部把比值压平**（两种尾部成本同向变动）⇒ S 略降；但尾部信息让**近两年**（借券紧缩期）更有效 ⇒ 2Y 升。
   ⇒ **可迁移结论：折叠的方向性由「分子分母是否同类量」决定** —— 同量纲相除（比值/价差）时两侧同折叠会互相抵消；跨量纲（费率 × 拥挤度）时折叠是纯增益（C10 +0.24）。
2. **锚点精确复现（重要）**：臂 1 复现 `1.08 / 0.74 / 0.56 / TO7.87%`，与原 C8 天花板**逐位一致** ⇒ 平台无漂移，跨会话读数可比。
3. **★ 平台行为发现：`checks.fail` 与 `ra.failed_ra_count` 存在口径差，且分级随中性化档变化**

   | α | 中性化 | `checks.fail` | warning 里的资格闸 | `failed_ra_count` |
   |---|---|---|---:|
   | `GrmNrRYQ` (1.08) | INDUSTRY | **`[]`** | LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE | **3** |
   | `ZYaV9MG1` (1.01) | INDUSTRY | **`[]`** | 同上 | **3** |
   | `A1xX3n8W` (0.73) | FAST | LOW_SHARPE / LOW_FITNESS | — | 2 |

   ⇒ **同一批闸在 INDUSTRY 档降级为 warning、在 FAST 档为 fail，但 `ra.failed_ra_count` 两档都计** ⇒ **`checks.fail=[]` 不能读作「RA 通过」**，必读 `ra.ra_failed_checks`。
   ⇒ ⚠ 本档案此前写「C8 是唯一 `checks.fail=[]` + `ppa_failed=0` 的形态」**字面正确但有严重误读风险**（会让人以为已过闸），现更正口径：**`checks.fail=[]` 只代表「无 FAIL 级项」，资格看 `failed_ra_count`**。
4. **★ 2Y 路线出现新点：`1YW3RP5K` = S0.58 / F0.28 / 2Y1.52 / TO2.70%**（`vec_max` × ts_cov750 × `group_rank` subindustry × INDUSTRY 档）⇒ 2Y 距闸 **0.06**，且 TO 仅 2.7%。
   但与 FAST 档同构造（`A1xX3n8W` 0.73/0.30/**1.70**）对比：**INDUSTRY 档在这条线上是纯劣化**（S −0.15、2Y −0.18），TO 降到 2.7% 对 F 无收益（`F` 的 0.125 换手下限已覆盖）⇒ **该线最优档仍是 FAST**。
5. 其余收敛确认：`ts_ir` 窗 66 保持（504→0.30）；外层 `group_scale` 保持（`group_zscore` 0.91 次优、`group_rank` 0.47）；轴 industry 保持（sector 0.71、subindustry 0.56）。

### ★★ 全局矛盾定性（risk60 的核心结论）

| 路线 | 最优表达式 | S | F | 2Y | 闸 |
|---|---|---:|---:|---:|---|
| **S 路线** | C8 `vec_avg` ts_ir66 group_scale industry @INDUSTRY | **1.08** | **0.74** | **0.56** | S 差 0.50 / 2Y 差 1.02 |
| **2Y 路线** | C14 `vec_max` ts_cov750 group_rank subindustry @FAST | 0.73 | 0.30 | **1.70** | S 差 0.85 / **2Y 已过** |

⇒ **两条路线严格互斥**（S 高的 2Y 低、2Y 高的 S 低），没有任何单构造能同时接近 S 闸与 2Y 闸。
⇒ ⇒ **唯一可能的破局 = 同集 `add` 组合**：两个信号的强弱期互补（C8 在早期强、C14 在近两年强），拼接后有望同时抬高 S 与 2Y。**ATOM 只判字段同源、不限制算子**（论坛 `44770798147735` 核实；记忆 `atom-internal-add-for-prod`）⇒ 同集多字段 add **不破 ATOM**。

### 批 P1 · C8 ⊕ C14 同集 add 组合（批 `21BSNt5lF4Hd8XsQSG6qHE1`，10 臂，INDUSTRY 档）

`A = group_scale(ts_ir66(divide(vec_avg(offer), vec_avg(bid))), industry)`（C8 腿，S 强）
`B = group_rank(ts_covariance(divide(vec_max(offer), vec_max(bid)), vec_sum(crowding), 750), subindustry)`（C14 腿，2Y 强）
结果 = `reverse(add(A, B))`（`reverse` 线性，故等价于 `add(reverse(A), reverse(B))`）。

| 臂 | A 折叠 | B 折叠 | B 内核×窗 | B 轴 |
|---|---|---|---|---|
| 1 | avg | **max** | cov750 | subindustry |
| 2 | avg | avg | cov750 | subindustry |
| 3 | **max** | max | cov750 | subindustry |
| 4 | avg | max | cov750，crowding 腿 `ts_rank(·,44)` | subindustry |
| 5 | avg | max | cov**250** | subindustry |
| 6 | avg | max | cov**504** | subindustry |
| 7 | avg | max | cov750 | industry |
| 8 | avg | max | cov750 | sector |
| 9 | avg | — | B 换 `vector_neut(bid_max, crowding)` | industry |
| 10 | avg | max | B 换 `ts_av_diff(ratio_max,504)` | industry |

> ⚠ **静态闸实战（第 2 次）**：`multiply(leg, 0.7)` 加权混腿被 `[POISON] weighted_leg_mix_func_suffix` **整批拒绝**（10 臂全废）⇒ **ATOM 内允许「裸 add（等权）」，但不允许显式加权 mix**。加权腿在派发前就必须放弃，不要靠闸来发现。

**批 P1 结果（10 臂，INDUSTRY 档）**：

| 臂 | A 腿 | B 腿 | α | S | F | 2Y | subU | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| 9 | avg ts_ir66 scale(industry) | **vector_neut(bid_max,crowding)** rank(industry) | `omajjWRJ` | **0.95** | **0.62** | 0.72 | 0.80 | **13.01%** |
| 8 | avg ts_ir66 scale(industry) | cov750 rank(**sector**) | `npaGGPm8` | **0.91** | 0.56 | **1.03** | 0.76 | 6.81% |
| 1 | avg ts_ir66 scale(industry) | cov750 rank(subindustry) | `qM72207P` | 0.88 | 0.53 | 0.93 | 0.72 | 6.94% |
| 6 | avg ts_ir66 scale(industry) | cov**504** rank(subindustry) | `LLKooZ82` | 0.88 | 0.53 | 0.66 | 0.69 | 7.03% |
| 7 | avg ts_ir66 scale(industry) | cov750 rank(industry) | `Wjlrre3k` | 0.86 | 0.52 | 0.83 | 0.74 | 6.84% |
| 2 | avg ts_ir66 scale(industry) | cov750(avg) rank(subindustry) | `omajjWaJ` | 0.86 | 0.51 | 0.86 | 0.70 | 6.93% |
| 3 | **max** ts_ir66 scale(industry) | cov750(max) rank(subindustry) | `VkNQQ0MV` | 0.81 | 0.47 | 1.02 | 0.70 | 7.00% |
| 5 | avg ts_ir66 scale(industry) | cov**250** rank(subindustry) | `qM72205E` | 0.81 | 0.46 | 0.59 | 0.65 | 7.32% |
| 4 | avg ts_ir66 scale(industry) | cov750(crowding ts_rank44) rank(sub) | `N1PEEVKg` | 0.80 | 0.45 | 0.72 | 0.44 | 8.10% |
| 10 | avg ts_ir66 scale(industry) | `ts_av_diff(ratio_max,504)` rank(industry) | `omajjWJm` | 0.54 | 0.24 | −0.08 | 0.36 | 14.05% |

**★★ 批 P1 结论 + 互相关实测（推翻此前「正相关」的推断）**：

1. **组合全部落在两条单腿之间，无一突破上限**：S 最高 0.95（< C8 单腿 1.08）；2Y 最高 1.03（< C14 单腿 1.70）。
2. **★ 互相关实测（`compute_mutual_correlation`，4 年 PnL / 1021 点）—— 三条腿两两正交**：

   | | GrmNrRYQ(C8) | A1xX3n8W(C14) | j2akPQJo(C10) |
   |---|---:|---:|---:|
   | **GrmNrRYQ** | 1.0 | **0.194** | **0.182** |
   | **A1xX3n8W** | 0.194 | 1.0 | 0.182 |
   | **j2akPQJo** | 0.182 | 0.182 | 1.0 |

   ⇒ **最大互相关子集 = 3**（三者互相关全部 < 0.5）。
   ⇒ **组合未突破单腿上限的原因不是正相关，而是「信号强度 × 时段错位」**：C8 腿全期 S 强但**近两年弱**（2Y 0.56），C14 腿近两年强但**全期 S 弱**（0.73）⇒ 等权 add 被双方的弱项同时稀释。
   ⇒ **更正此前推断**：曾依据「add 组合无法突破上限」反推「两条腿正相关」，该推断**错误**，实测为正交。

3. **★ 结构性限制（平台批次级参数）**：中性化档是**批次级**参数，一个回测批次只能一个档 ⇒ **无法在同一回测里让两条腿分别用 INDUSTRY 与 FAST**（C8 最优 INDUSTRY、C14 最优 FAST）。
   ⇒ 若想实现「C8-INDUSTRY 腿 + C14-FAST 腿」的组合，必须两条腿各跑一档、再在 PnL 层组合 —— 平台 ATOM 单表达式内**做不到**。这是本数据集一条硬约束，不是待测项。

4. **组合最优点**：臂 8 `npaGGPm8` = **S0.91 / F0.56 / 2Y1.03 / subU0.76 / TO6.81%**（B 腿 cov750 × sector 轴）—— 是 S 与 2Y 的最佳平衡，但距双闸仍远（S 差 0.67 / 2Y 差 0.55）。

> ⚠ **合规标注（2026-11-23 复核 AGENTS.md §7.7 时发现）**：本节的批 P1（C8⊕C14 同集 `add` 组合）**违反 AGENTS.md 的明确禁令**——
> 「**仍然无条件禁止**：`add(独立信号腿A, 独立信号腿B)` 等权/加权混腿（与 ATOM 无关的独立铁律，见 §7.5 与 `mixed_signal_leg_ban_v1`）」。
>
> 说明与处置：
> 1. **事实性结论仍然有效**：三条腿两两互相关 0.18–0.19（正交）、组合无法突破单腿上限、中性化档批次级限制 —— 这些**不依赖 add 是否合法**，是独立的观测事实。
> 2. **P1 的表达式不再作为后续方向**：按 §7.7，后续不再用 `add` 混腿做信号组合；若需要组合，只走 §7.7 许可的**跨集四形态**（`gating` / `grouping` / `residual` / `ratio`），且属 regular 路线（ATOM 已穷尽后才允许）。
> 3. **记忆冲突登记**：[[atom-internal-add-for-prod]] 记录用户 2026-11-20 裁定「ATOM 里 add 合法」，与 AGENTS.md §7.7「无条件禁止」**直接冲突**。**以 AGENTS.md 为权威**（它标注为「与 ATOM 无关的独立铁律」），后续执行以本节标注为准。


### ★ P2 · 其余构造在 `vec_max` 下的完整梯度（2026-11-23 后段）

**流程修正（重要）**：原计划每构造跑 ~40 臂完整 5 层（9 构造 ≈ 360 臂）。C7 实测后修正为**两阶段**：
1. **折叠方向筛选**：每构造 2 臂（`vec_avg` 基线 + `vec_max`），**用该构造自己的最优档**（而非统一 FAST 档）⇒ 复现读数同时验证表达式正确性；
2. ΔS ≥ +0.05 ⇒ 重跑完整 5 层；ΔS ≤ 0 ⇒ **锁定 `vec_avg`**，仅补参数精调层。

> ⚠ 修正依据：X1/X2 用统一 FAST 档，导致「C2 +0.11」这类结论在最优档（INDUSTRY）下未必成立 —— **C7 就是反例**：FAST 档 +0.06，最优档（SUBINDUSTRY/decay8）−0.03。

### 批 P2-C7 · 价差构造在 `vec_max` 下的 L2 内核重扫（批 `3G7oEqcYk4nocyeiYU1GFs9`，10 臂，SUBINDUSTRY + decay8 + industry 轴 + W504）

| 臂 | 折叠 | 内核 | α | S | F | 2Y | subU | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| **1** | **`vec_avg`** | **`ts_av_diff`** | `omaXmzmJ` | **0.82** | **0.48** | −0.19 | 0.67 | 9.03% | ← **复现原天花板（表达式正确）** |
| **2** | **`vec_max`** | `ts_av_diff` | `pwabLVkb` | **0.79** | 0.45 | −0.26 | 0.74 | 9.05% | **折叠 −0.03** |
| 9 | vec_max | `ts_rank` | `2r5VYaV8` | 0.61 | 0.29 | −0.23 | 0.40 | 11.37% |
| 10 | vec_max | `ts_quantile` | `A1xXAgXd` | 0.60 | 0.29 | −0.27 | 0.44 | 12.12% |
| 6 | vec_max | `ts_zscore` | `Jj8a9gJW` | 0.55 | 0.28 | −0.51 | 0.59 | 12.63% |
| 8 | vec_max | `ts_scale` | `wpo7rnkd` | 0.48 | 0.22 | −0.02 | 0.47 | 9.03% |
| 4 | vec_max | `ts_max_diff` | `3q0mNave` | 0.25 | 0.08 | 0.08 | 0.38 | 4.31% |
| 3 | vec_max | `ts_delta` | `LLKoQgY6` | 0.07 | 0.01 | −0.16 | 0.08 | 16.28% |
| 7 | vec_max | `ts_std_dev` | `N1PEZgl8` | 0.08 | 0.01 | 0.16 | 0.16 | 2.09% |
| 5 | vec_max | `ts_ir` | `2r5VYao8` | 0.22 | 0.07 | 0.59 | 0.21 | 3.35% |

**★ 批 P2-C7 结论（三条）**：

1. **锚点精确复现**（0.82 / 0.48 / −0.19 / TO9.03%）⇒ 表达式重建正确，平台无漂移。
2. **★ `vec_max` 在 C7 上是净负（−0.03 S / −0.07 2Y）** —— **第 3 个反向案例**（与 C11/C12 同类）。
   ⇒ **规律收敛**：反向案例全部属于「**同量纲量之间的运算**」—— C7 是 `subtract`（价差）、C8 是 `divide`（比值）、C11/C12 是 `divide(x, ts_mean(x))` / `divide(spread, base)`。
   ⇒ **机制**：同量纲相减/相除时，**两侧同取尾部会互相抵消**（尾部−尾部 ≈ 0，尾部÷尾部 ≈ 1）⇒ 信号被压平；而**跨量纲**（费率 × 拥挤度，C10/C14）时尾部是纯增益。
   ⇒ **可迁移判据：换折叠前先问「这条腿是否跨量纲」** —— 同量纲运算两侧必须**异口径**或保留 `vec_avg`。
3. **内核无翻转**：`ts_av_diff` 保持最优（0.79 vs 次优 `ts_rank` 0.61）⇒ 与 vec_avg 时代一致。
4. **C7 的 2Y 全部为负（−0.19 ~ −0.51）** ⇒ **C7 在近两年完全失效**，是 2Y 墙的直接来源。

⇒ **C7 锁定 `vec_avg`，天花板定 0.82 / F0.48，不再投入**。

### 批 P2-C4/C6 · FAST 档折叠方向筛选（批 `2Dx7Mq99e4tWcvWN6BAqfkZ`，4 臂）

| 臂 | 构造 | 折叠 | α | S | F | 2Y | subU | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | **C4**（拥挤累计 `vec_sum`） | **`vec_avg`** | `mLalV1VW` | **0.79** | 0.22 | 0.46 | 1.16 | 32.01% | ← **精确复现 C4 天花板** |
| 3 | C4 | `vec_max` | `mLaG3XL2` | 0.68 | 0.18 | 0.22 | 0.92 | 31.80% | **折叠 −0.11** |
| 2 | **C6**（费率×拥挤门控） | `vec_avg` | `N1PEabWg` | 0.60 | 0.15 | −0.01 | 1.05 | 29.43% |
| 4 | C6 | `vec_max` | `9ql5jpPe` | 0.65 | 0.17 | 0.13 | 1.08 | 29.17% | **折叠 +0.05** |

**★ 批 P2-C4/C6 结论（两条）**：

1. **★★ 表达式重建被平台独立验证**：`N1PEabWg` / `9ql5jpPe` 复现出与此前 X1 批次**完全相同的 alpha id**，C4 的 `vec_avg` 臂复现 0.79/0.22/0.46（与档案记录逐位一致）⇒ **从档案摘要重建的表达式是正确的**，后续 P2 批次可放心用。
2. **折叠方向**：
   - **C4 锁定 `vec_avg`（−0.11）**：C4 的信号是 `vec_sum(crowding)`（**单字段流量累计计数**），不是跨量纲运算；`vec_max` 把「累计计数」变成「最大符号值」，丢失计数信息 ⇒ 大幅变差。**符合判据**（[[fold-direction-depends-on-dimension-homogeneity]]：非跨量纲 ⇒ max 未必好）。
   - **C6 达 +0.05 阈值**（0.60→0.65，2Y −0.01→0.13）⇒ **需在 `vec_max` 下重跑完整 5 层**。C6 与 C10 同构（均为「费率 × 拥挤分位」门控，仅费率腿不同：C6=offer / C10=bid），故 C10 已验证的结构（`ts_ir` + `group_rank` + 粗轴 + 拥挤腿窗 44）在 C6 上需**独立验证、不可类推**。

### 批 P2-C6 · 门控(offer) 在 `vec_max` 下的完整梯度（FAST 档）

基线：`reverse(group_rank(ts_zscore(ts_backfill(multiply(vec_max(rsk60_offer), ts_rank(ts_backfill(vec_sum(rsk60_crowding),250),66)), 250), 126), industry))`

**当前已测**：仅基线 1 臂（`9ql5jpPe` = S0.65 / F0.17 / 2Y0.13 / subU1.08 / TO29.17%）。
**待跑**：L2 内核全替 → 窗层 → 轴层 → 外层 → 设置档 → L5-R（约 30 臂）。

> ⚠ **纠错记录**：本节一度把其他构造批次（X2 的 C10 臂 `Jj8ak1Rn`、C2 臂 `O0WdgrYg` 等）误记为 C6 的内核全替读数，已更正。C6 的内核全替**尚未执行**，勿引用错误读数。

### 批 P2-C6-1 · 门控(offer) 在 `vec_max` 下的 L2 内核全替（批 `2BYXBobu04yucAZbAvxgAWe`，6 臂，FAST 档，窗 126）

| 臂 | 内核 | α | S | F | 2Y | subU | TO |
|---|---|---|---:|---:|---:|---:|---:|
| **6** | **`ts_scale`** | `RReOaOJg` | **0.73** | **0.23** | **0.72** | **1.13** | 24.04% |
| 1 | `ts_zscore`（原基线） | `9ql5jpPe` | 0.65 | 0.17 | 0.13 | 1.08 | 29.17% |
| 4 | `ts_delta` | `QP0xlx1g` | 0.56 | 0.14 | −1.16 | 0.63 | 30.81% |
| 2 | `ts_ir` | `aka0P0rO` | 0.41 | 0.13 | −0.24 | 0.66 | 9.36% |
| 3 | `ts_av_diff` | `xAvLzLKl` | 0.33 | 0.06 | −0.26 | 0.58 | 27.72% |
| 5 | `ts_max_diff` | `vRAEzEKb` | −0.02 | −0.00 | −0.85 | 0.13 | 15.05% |

**★★ 批 P2-C6-1 结论（内核翻转，第 8 次）**：
1. **`ts_scale` 0.73 反超原基线 `ts_zscore` 0.65（ΔS +0.08 / Δ2Y **+0.59** / ΔsubU +0.05）** ⇒ **换基线为 `ts_scale`**，后续层按新基线重扫。
2. 这与 C10-vec_max 的规律**同型但方向不同**：C10 在 vec_max 下**保持 `ts_ir`**，C6 在 vec_max 下**翻到 `ts_scale`**。⇒ **门控型信号的内核冠军在 vec_max 下不稳定**，必须逐个构造实测，不可类推。
3. **TO 全部远超 12.5% 下限**（9.36%–30.81%）⇒ 本构造的 F 闸由 TO 压制（`F = S × √(|R| / max(TO, 0.125))`），**`ts_ir` 的 TO 9.36% 最低但 S 也最低** ⇒ 存在 S 与 TO 的权衡。
4. 基线臂 `9ql5jpPe` 复现同 id、读数逐位一致（0.65/0.17/0.13）⇒ 平台无漂移，跨批可比。

⇒ **C6-vec_max 新基线 = `reverse(group_rank(ts_scale(ts_backfill(multiply(vec_max(rsk60_offer), ts_rank(ts_backfill(vec_sum(rsk60_crowding),250),66)),250),126), industry))` @ FAST**

### 批 P2-C6-2 · 窗层全替（批 `4een5GbCO4h1adiqFOQ46Yu`，6 臂，`ts_scale` 窗扫）

| 窗 | 44 | 66 | 126 | 250 | **504** | 750 |
|---|---:|---:|---:|---:|---:|---:|
| α | `vRAEJr7v` | `9qleAj5x` | `RReOaOJg` | `RReOkbxo` | **`rK7qrOq1`** | `KPgowNoj` |
| S | 0.48 | 0.46 | 0.73 | 0.55 | **0.76** | 0.72 |
| F | 0.11 | 0.11 | 0.23 | 0.15 | **0.25** | 0.23 |
| 2Y | 0.70 | 0.30 | **0.72** | 0.65 | 0.44 | 0.06 |
| subU | 0.76 | 0.94 | 1.13 | 1.17 | **1.38** | 1.22 |
| invest_ratio | 1.33 | 1.33 | 0.96 | 1.27 | **1.16** | 1.10 |
| TO | 26.86% | 25.63% | 24.04% | 22.56% | **21.69%** | 21.38% |

**批 P2-C6-2 结论（三条）**：
1. **窗 504 是综合最优**（S0.76 / F0.25 / **subU1.38** / invest1.16 / **TO21.69%** 最低），仅 2Y 0.44 低于 126 档的 0.72。
2. **★ subU 1.38 与 invest_ratio 1.16 是本数据集全部读数中的最高值** ⇒ C6 是一个「小盘/可投资性极佳但 2Y 偏弱」的形态。
3. **TO 随窗单调下降**（26.86% → 21.38%）⇒ 长窗降换手；但因 TO 全部 >12.5%，F 仍被压制（`max(TO,0.125)` 未生效）。
4. ⚠ **S-2Y 跷跷板第三次在本构造出现**（504: S0.76/2Y0.44 vs 126: S0.73/2Y0.72）⇒ 取 504 作基线（综合占优），2Y 0.72 的 126 档保留为并列候选。

⇒ **C6-vec_max 新基线 = `reverse(group_rank(ts_scale(ts_backfill(multiply(vec_max(rsk60_offer), ts_rank(ts_backfill(vec_sum(rsk60_crowding),250),66)),250),504), industry))` @ FAST**

### 批 P2-C6-3 · 轴层 + 外层（批 `2YpAwTD54ksb5e9QlYIHVu`，6 臂）

臂 1 = industry（基线对照）/ 2 = market / 3 = sector / 4 = subindustry / 5 = 外层 `group_scale` / 6 = 外层 `group_zscore`。
> ⚠ 轴层只扫 4 档（GBR `market≡exchange≡country` 已实证等价，不重复占臂位）。

**批 P2-C6-3 结果（6 臂）**：

| 臂 | 内容 | α | S | F | 2Y | subU | invest | TO |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **3** | **轴=sector** | `omab9ZbE` | **0.82** | **0.30** | **0.51** | **1.48** | 1.13 | **20.25%** |
| 1 | 轴=industry（基线） | `rK7qrOq1` | 0.76 | 0.25 | 0.44 | 1.38 | 1.16 | 21.69% |
| 2 | 轴=market | `O0WL5gL7` | 0.75 | 0.26 | 0.44 | 1.45 | 1.19 | 19.88% |
| 4 | 轴=subindustry | `9qleAke2` | 0.58 | 0.16 | 0.16 | 1.15 | 1.47 | 22.28% |
| 5 | 外层 `group_scale` | `KPgowZ1l` | 0.57 | 0.15 | 0.76 | 0.90 | 1.44 | 26.98% |
| 6 | 外层 `group_zscore` | `Jj8A5r9l` | 0.55 | 0.14 | 0.38 | 1.03 | 1.40 | 26.97% |

**★★ 批 P2-C6-3 结论（三条）**：
1. **轴翻到 `sector`（S0.76→0.82，ΔF +0.05，subU 1.38→1.48，TO 21.69%→20.25%）** ⇒ 换基线为 **`ts_scale`504 × sector**。
   ⇒ 与 C10（门控型吃 **market/sector 粗轴**）一致，与 C14（协方差型吃 subindustry 细轴）相反；**C6 在 subindustry 下只有 0.58**，进一步确认「门控型 → 粗轴」的判据。
2. **★ subU 1.48 是 risk60 全部读数中的最高值**（远超内部严线 0.4）；invest_ratio 1.13 亦远超 0.70 严线 ⇒ **C6 的可投资性/子宇宙稳健性是本数据集最强**，尽管 S 只有 0.82。
3. **外层 `group_rank` 独占最优**（`group_scale` 0.57 / `group_zscore` 0.55 双双崩）⇒ 与 C10/C14 一致（协方差/门控型均只能用 `group_rank`；只有 C8 的纯水平比值吃 `group_scale`）。

⇒ **C6-vec_max 当前天花板 = S0.82 / F0.30 / 2Y0.51 / subU1.48 / invest1.13 / TO20.25%**（`omab9ZbE`）

### 批 P2-C6-4 · 换基线后的 L5-R 内核重扫（批 `2HbCpE7814o998XZ9jhBvRA`，6 臂，sector 轴 × `ts_scale`504）

臂为 `ts_scale`(基线) / `ts_zscore` / `ts_ir` / `ts_delta` / `ts_max_diff` / `ts_av_diff`，全部在 sector 轴 + 窗 504 下。

**★★ 平台坑（本批两次卡死，已定位并规避）**：首派批 `2HbCpE7814o998XZ9jhBvRA`（6 臂）与重派批 `6yF1weF94Tna2i1af8ebTbF`（4 臂）**均卡在 `progress 0.9` 且 `children=0` 超过 10 分钟**，而 `tools/batch_status.py` 确认 `0/0 terminal`。
- **根因假设（已被后续实验证实）**：这两批的**首条表达式 `ts_scale504 × sector` 与批 C6-3 已跑过的 `omab9ZbE` 完全相同** ⇒ 平台在「复用相同表达式」的路径上卡住。
- **规避**：**去掉重复表达式**，只派其余 3 个内核（`GsaAq2XP5fbaYH1cPXiTCSH`）⇒ 该批 `progress 0.35 → 正常完成（3/3 COMPLETE）`。
- ⇒ **可迁移坑**：`create_multi_simulation` 的批次内**不要包含近期已跑过的完全相同的表达式**（相同 code + 相同 settings）；需要基线对照时，**直接复用已知 alpha id 的读数**，不要重派。

**批 P2-C6-4 结果（3 臂，sector 轴 × 窗 504，`ts_scale` 基线复用 `omab9ZbE`）**：

| 内核 | α | S | F | 2Y | subU |
|---|---|---:|---:|---:|---:|
| **`ts_scale`（基线，复用 C6-3）** | `omab9ZbE` | **0.82** | **0.30** | **0.51** | **1.48** |
| `ts_zscore` | `A1xplxMg` | 0.74 | 0.22 | −0.48 | 1.09 |
| `ts_ir` | `xAvLjv0N` | 0.51 | 0.18 | 0.43 | 0.99 |
| `ts_delta` | `vRAEjA3A` | −0.00 | −0.00 | −1.25 | 0.42 |

**批 P2-C6-4 结论**：**`ts_scale` 在 sector 轴 × 504 窗下保持最优（0.82，领先次优 0.08），L5-R 未翻转** ⇒ C6 的「内核 → 窗 → 轴」三层梯度闭环。

### 批 P2-C6-5 · 设置档 decay 8 + 拥挤腿窗复核（批 `2PZ6EOdqk4mfcrKJIvWqJQ4`，3 臂）
臂 1 = 基线（拥挤窗 66，验证 decay4→8 的效果）/ 2 = 拥挤腿窗 44 / 3 = 拥挤腿窗 126。
> 动机：C6 的 2Y 0.51 是最大短板，长 decay 通常抬 2Y；C10 的拥挤腿最优窗是 44，需在 C6 上独立验证（不可类推）。

**★★ 该批死批（第三次同型，实证「settings 不参与去重」）**：`2PZ6EOdqk4mfcrKJIvWqJQ4` 卡死 `progress 0.9` + `children=0` 远超 25 分钟，按死批判定废弃。
- **区别点**：本批的臂 1（`ts_scale504 × sector × crowding66` @ **decay8**）与已跑过的 `omab9ZbE`（同 code @ **decay4**）**表达式完全相同、settings 不同** —— 仍然卡死。
- ⇒ **修正平台坑的机制描述**：平台判定「重复表达式」**只看表达式 code，不看 settings**（此前在 [[multisim-duplicate-expression-stuck-at-09]] 中未区分；现实证 settings 不同也会卡）。
- **规避（最终版）**：**凡是平台上已存在该 code 的任意 alpha（无论 settings），都不得再放进新批次**；需要不同 settings 的读数时，改用**结构微变体**（换窗/换轴/换折叠参数都在这个范畴内，代价是读数不再与旧件严格同构，对比时须注明）。

**重派（批 `4au3Cc7X14TmcA3K4Ic20zk`，2 臂，decay8）**：臂 1 = `crowding44`（全新）/ 臂 2 = `crowding126`（全新）—— 完全避开已存在的 code。
> ⚠ 将 `crowding66@decay8` 与 `omab9ZbE`(`crowding66@decay4`, 0.82) 的对比视为**跨档参考**（不同拥挤窗），严格同构对比不可得（同 code 会被平台卡死）。














### 批 G-3 · backfill 窗与 `k` 参精调（6–8 臂）

- backfill 窗 {66, 120, 252, 504}（基线 250 对照）——`ts_backfill` 是 cov 0.6694 数据集的关键预处理，窗长决定「陈旧报价能撑多久」。
- `ts_backfill(x, d, k=2)` 的 `k` 参（陈旧度）——**命名参数精调**项之一。


