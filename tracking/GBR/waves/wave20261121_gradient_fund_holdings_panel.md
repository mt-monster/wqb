# GBR / fund_holdings_panel 完整梯度档案（wave20261121_fund_holdings_panel）

> 依据：`wq-brain-ra-pipeline` 步 7「梯度回测（必做）」+ §7.10 + `tools/gates/gradient_gate.py`
> 用户 2026-11-21 指令：「继续 inst4 和 fund_holdings 的梯度做完」。
> ⚠ **该集是 GBR 数据集级死键**（ledger `fund_holdings_panel_dead`：`dead_at=2026-08-18`，`reason=stageA best sh=0.79 2y=1.56 … margin 1.5bp 结构性低, sharpe 0.79 << 1.58 判死`，`dead_count=4`）。
> 本轮按**用户显式指令**重测（= 授权重开）；**未改动台账**。结果出来后按协议决定：出货 → `dead_sets.py --reopen` 回写；仍弱 → 维持死键并补「完整梯度也弱」证据。
> 数据集：fund_holdings_panel（18 字段 = 9 概念 × 2 [主版 + `_active` 孪生]，全 VECTOR，cov 0.89–0.93）｜塔：institutions（1/3）
> 基线（梯度前）：历史 24 探针「真 F 墙」（best S0.79/2Y1.56，margin 1.5bp 结构性低）；`gradient_gate` 曾判 DONE（dom=3/6 层）但那是**死键前的探针聚集，不是真梯度**。

---

## 完整梯度计划（5 层）

| 层 | 槽位 | 全类别候选 | 臂数 |
|---|---|---|---:|
| **L1 信号构造** | 9 概念的经济配比 | 每账户交易额/边界笔数/大单占比/耐久占比/边界金额占比/HHI/分布评分/信念占比/账户广度 = 9 | 9 |
| **L2 内层时序** | `<K>(SIG, 126)` | Time Series 9/21 | 9–10 |
| **L3 分组轴** | `group_rank(·, G)` | 6 轴 | 6 |
| **L4 外层包装** | `group_rank` → Group 类 | 8/9 | 8 |
| **L5 设置档** | 中性化 × decay | 4–5 批 × 2 臂 | 8–10 |

**字段覆盖说明（验收①）**：18 字段中 9 个 `_active` 版本是主版的**同概念孪生**（description 逐字同源），按「同族不重复测」排除并写明；主版 9 概念全进 L1 配比。
⚠ 全部 VECTOR ⇒ `vec_sum`/`vec_avg` 折叠；分母 0 风险（交易笔数类）——如整批 UNITS/除零拒收，改 `add(...,1)` 同单位版本。

---

## §7.10.0 数据窗口前置体检（2026-11-21，批 `4jQp8fyj4BzaMPoIiBN8z1`，2 臂）

探针（NONE 中性化 / decay0 / trunc0 / nanOFF，只测数据存在性）：
`rank(ts_backfill(vec_sum(transaction_account_total),250))` → `npaeY6ol`；`rank(ts_backfill(vec_sum(security_transaction_usd_value),250))` → `O0WMq6mq`

`get_alpha_yearly_stats` 逐年（两条逐位同型）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | **0** | 768 | 830 | 996 | 901 | 881 | 813 | 798 | 843 | 802 |
| pnl | **0** | 3.40M | 1.05M | 2.90M | −2.17M | 5.35M | 4.89M | 4.60M | −2.94M | 2.83M |

- **数据窗口 = 2015–2023（9 年）**：2014 全年 lc/sc/pnl 全 0 = 无数据（不是零持仓）。
- 最近两年（2022/2023）有数据 ⇒ **2Y 闸可正常评估**（与 in4「只有 2019–2020」不同，不构成数据层排除）。
- 探针读数（未中性化、长仓单边）：`npaeY6ol` S0.73/F0.80/TO17.7%/2Y−0.03；`O0WMq6mq` S0.71/F0.45/TO51.4%/2Y−0.19。原始 rank 单边 ⇒ 只作数据存在性判据，不作信号判据。
- **结论：数据窗口合格，梯度照做**；档案所有结论的适用域写「2015–2023」。

---

## Layer 1 · 配比全替换（2026-11-21，批 `318j9q1r64TzcIv14htMkHlz`，8 臂）

冻结：`group_rank(ts_zscore(<SIG>, 126), industry)` / SUBINDUSTRY / decay4 / trunc0.08 / nanON

| 臂 | 配比 | 表达式核心 | α | S | F | 2Y | TO | RA | ΔS |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| L1-7 | 分布评分（水平） | avg(distribution_score) | `YPaEmnKo` | **0.22** | 0.03 | −0.09 | 46.4% | 3 | **——（L1 最强，但远低于闸）** |
| L1-3 | 大单占比 | large50 / boundary | `gJagKwAm` | 0.14 | 0.02 | **0.69** | 27.6% | 3 | −0.08 |
| L1-6 | HHI 集中度（水平） | avg(herfindahl) | `rK7NLEgj` | 0.14 | 0.02 | −0.19 | 49.0% | 3 | −0.08 |
| L1-8 | 信念交易占比 | top_weighted / boundary | `blarMV5Z` | 0.04 | 0.00 | 0.49 | 37.2% | 3 | −0.18 |
| L1-5 | 边界金额占比 | boundary_usd / sec_usd | `O0WMkqPv` | 0.00 | 0.00 | −0.26 | 27.2% | 3 | −0.22 |
| L1-2 | 每账户边界笔数 | boundary / acct | `j2aPXWvO` | −0.05 | −0.00 | −0.47 | 39.5% | 3 | −0.27 |
| L1-4 | 耐久占比 | stable21 / boundary | `j2aPXWEO` | −0.08 | −0.01 | 0.60 | 19.5% | 3 | −0.30 |
| L1-1 | 每账户交易额 | sec_usd / acct | `1YWlL1e6` | −0.75 | −0.17 | −0.75 | 46.4% | 3 | −0.97 |

**L1-A 结论（8 配比全灭）**：S 最高仅 0.22（分布评分），全部 RA3、TO 19–49%（配比型噪声大）；大单占比/耐久占比/信念占比呈「**2Y 有 S 无**」（2Y 0.49–0.69 / S ≈0）。

### L1-B · 计数水平族（2026-11-21，批 `2AznrreXk4yNbKqQ009iVnT`，4 臂）

| 臂 | 水平字段 | α | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| L1-11 | 大单笔数水平 `sum(large_trade_count_50bps)` | `58JA91vz` | 0.04 | 0.00 | **0.61** | 27.6% | 3 |
| L1-10 | 边界笔数水平 `sum(boundary_transaction_total)` | `9qldK3RK` | 0.06 | 0.00 | −0.20 | 38.9% | 3 |
| L1-12 | 耐久边界笔数水平 `sum(stable_boundary_trade_count_21d)` | `j2aPXJgk` | −0.21 | −0.03 | −0.45 | 34.7% | 3 |
| L1-9 | 账户广度水平 `sum(transaction_account_total)` | `2r5XRxJY` | −0.67 | −0.17 | −0.68 | 43.0% | 4 |

**L1 终态（9 概念 + 4 水平 = 12 臂全灭）**：
1. **最强 = 分布评分（0.22）**——它是唯一的 **0–1 有界指数**（与 imb5_score 同类）；其余配比/水平 ≤0.14。
2. 计数水平族同样弱（−0.67~0.06），且 TO 28–43%（比历史 fhp 探针 5–10% 高一个量级 ⇒ 本集信号在高频比例变换下被噪声主导）。
3. 多个形态仍是「**2Y 有 S 无**」（大单 0.61 / 耐久 0.60 / 信念 0.49）——与 in6 同型。
4. **L2 基线 = 分布评分**（有界指数族；L2 目标：内核能否把 0.22 拉起来，参照 imb5 的 ts_scale 效应）。

---

## Layer 2 · 内层时序算子全替换（以分布评分为基线，2026-11-21，批 `3fLQhHeGH5b2aeL1aaRrqMks` 8 臂）

冻结：`group_rank(<K>(ts_backfill(vec_avg(transaction_value_distribution_score), 250), 126), industry)`；SUBINDUSTRY/decay4/trunc0.08/nanON

| 臂 | 内层算子（同窗 126） | α | S | F | 2Y | TO | RA | ΔS vs 0.22 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| L2-3 | `ts_quantile` | `LLKmX1p2` | **0.32** | 0.05 | 0.11 | 51.6% | 3 | **+0.10** |
| L2-2 | `ts_rank` | `pwaMzl66` | 0.31 | 0.05 | 0.15 | 51.7% | 3 | +0.09 |
| L2-6 | `ts_av_diff` | `npaez22q` | 0.29 | 0.04 | 0.13 | 50.6% | 3 | +0.07 |
| L2-8 | `ts_ir` | `zqd2ommV` | 0.09 | 0.01 | −0.55 | 5.7% | 4 | −0.13 |
| L2-1 | `ts_scale` | `LLKmX1R2` | 0.02 | 0.00 | **−1.18** | 31.3% | 4 | −0.20 |
| L2-4 | `ts_mean` | `xAv2zkkg` | −0.03 | −0.00 | −1.09 | 2.9% | 4 | −0.25 |
| L2-5 | `ts_std_dev` | `P05Yl33p` | −0.28 | −0.10 | −0.85 | 4.8% | 4 | −0.50 |
| L2-7 | `ts_delta` | `N1PJjrre` | −0.41 | −0.08 | −0.17 | 41.1% | 3 | −0.63 |

**L2-A 结论**：排名类（quantile/rank/av_diff 0.29–0.32，TO ~51%）> 水平/波动类（≤0.02，TO 3–31%）；**ts_scale 在 fhp 上完全失效（2Y −1.18）**——与 imb5 相反 ⇒ **内核选择按数据集实测，不可跨集搬运**。天花板仍在 0.32，距闸 1.58 差 1.26；比分制 3 臂 TO 51% 已接近上限。

### L2-B · 剩余 7 内核（2026-11-21，批 `2dvKrs2GO4BlaCE10G0UqT1Y`）

| 臂 | 算子 | α | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| L2-13 | `days_from_last_change` | `j2aPdQrZ` | **0.25** | 0.09 | −0.11 | 14.7% | 4 |
| L2-15 | `ts_max_diff` | `KPg5wREl` | 0.14 | 0.02 | −0.49 | 26.8% | 4 |
| L2-11 | `ts_product` | `N1PJ5orq` | 0.15 | 0.04 | −0.88 | 2.7% | 4 |
| L2-12 | `ts_arg_min` | `akaQW3d2` | 0.06 | 0.01 | 0.51 | 6.7% | 3 |
| L2-14 | `ts_arg_max` | `6XMoYbEJ` | −0.20 | −0.05 | −0.74 | 9.0% | 4 |
| L2-16 | `ts_sum` | `vRApJVlA` | −0.33 | −0.12 | −0.98 | 2.9% | 4 |
| L2-17 | `ts_returns` | `xAv2maxW` | −0.42 | −0.08 | −0.24 | 41.2% | 3 |

**L2 终态（15/16 可测全扫；ts_step 只收数字排除）**：最高 **`ts_quantile` 0.32**（L2-A），次 ts_rank 0.31；其余 ≤0.29。⇒ **fhp 内层天花板 0.32**，距 S 闸 1.26。L3 轴层（6 臂 `3s5HRJeMT4UocJL1eKH6CweX`）在测。

---

## Layer 3 · 分组轴全替换（2026-11-21，批 `3s5HRJeMT4UocJL1eKH6CweX`，6 臂）

冻结：`group_rank(ts_quantile(ts_backfill(vec_avg(distribution_score),250),126), <G>)`

| 臂 | 分组轴 | α | S | F | 2Y | TO | RA | ΔS vs industry |
|---|---|---|---:|---:|---:|---:|---:|---:|
| L3-1 | `industry`（基线） | `LLKmX1p2` | **0.32** | 0.05 | 0.11 | 51.6% | 3 | — |
| L3-3 | `subindustry` | `npaeZW7M` | 0.31 | 0.04 | 0.13 | 53.1% | 3 | −0.01 |
| L3-2 | `sector` | `O0WMb9G7` | 0.27 | 0.04 | 0.18 | 50.6% | 3 | −0.05 |
| L3-4 | `market` | `RRel2r71` | 0.26 | 0.04 | 0.18 | 50.4% | 3 | −0.06 |
| L3-5 | `exchange` | `Jj8Wgd7A` | 0.26 | 0.04 | 0.18 | 50.4% | 3 | −0.06 |
| L3-6 | `country` | `78YvadZQ` | 0.26 | 0.04 | 0.18 | 50.4% | 3 | −0.06 |

**L3 结论（`converge=yes`，industry 最优）**：industry ≡ subindustry（0.32/0.31）；**market ≡ exchange ≡ country 逐位相同**（0.26，单国三轴等价再次复现）；轴层增益 ≤0.05 ⇒ 天花板 0.32。

---

## Layer 4 · 外层包装全替换（2026-11-21，批 `2m15JbeUz5e19FDFXC9bUiu`，7 臂）

| 臂 | 外层 Group | α | S | F | 2Y | TO | RA | ΔS vs group_rank |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **L4-3** | **`group_scale`** | `O0WMoQMJ` | **0.53** | 0.09 | 0.43 | 60.1% | 3 | **+0.21** |
| L4-6 | `group_backfill(·,industry,120)` | `omaJV8Gl` | 0.51 | 0.09 | 0.65 | 59.2% | 3 | +0.19 |
| L4-7 | `group_backfill(·,industry,252)` | `QP0NEZzW` | 0.51 | 0.09 | 0.66 | 59.2% | 3 | +0.19 |
| L4-1 | `group_zscore` | `kqaWQEv6` | 0.48 | 0.08 | 0.50 | 59.8% | 3 | +0.16 |
| L4-2 | `group_neutralize` | `1YWlJklJ` | 0.47 | 0.08 | 0.59 | 59.5% | 3 | +0.15 |
| L4-5 | `group_std_dev`（聚合型） | `Wjlo91oZ` | 0.02 | 0.00 | 0.26 | **115.2%** | 6 | −0.30（DD 71%） |
| L4-4 | `group_sum`（聚合型） | `wpo2LKG6` | −0.09 | −0.01 | −0.37 | **114.9%** | 6 | −0.41 |
| — | `group_rank`（基线） | `LLKmX1p2` | 0.32 | 0.05 | 0.11 | 51.6% | 3 | — |

**L4 结论（`converge=no`——层内出现 +0.21 的最大单层增益）**：**`group_scale` 0.53** ⇒ L5 基线切换为 `group_scale(ts_quantile(...126), industry)`；代价 TO 51.6%→60.1%。聚合型 TO 115% / DD 71% 崩（与 in6/imb5 一致）。

---

## Layer 5 · 设置档（4 档 × 2 臂，2026-11-21；每批 2 臂）

基线：`group_scale(ts_quantile(...126), industry)` @ SUBINDUSTRY/decay4 = **0.53**

| 批 | 设置档 | α（group_scale / group_zscore） | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|
| A | `INDUSTRY` 中性化 | `9qldJwe9` / `KPg5kbop` | 0.38 / 0.34 | 0.06/0.05 | 0.56/0.63 | 59.6/59.2% | 3 |
| B | `SECTOR` 中性化 | `88NEnxGX` / `pwaM8exg` | 0.27 / 0.35 | 0.04/0.05 | 0.30/0.64 | 60.1/59.2% | 3 |
| C | `FAST` 中性化（风险档） | `YPaEprbW` / `rK7No3e1` | 0.51 / 0.48 | 0.08/0.07 | 0.61/0.71 | 60.7/59.8% | 3 |
| **D** | **SUBINDUSTRY + decay 8** | **`pwaM6Kxg` / `LLKmpdE9`** | **0.70** / 0.64 | 0.18/0.15 | 0.60/0.73 | 40.8/40.5% | 3 |

**L5 结论（`converge=yes`）**：**decay 8 是唯一增益档（0.53→0.70，+0.17，TO 60%→40.8%）**；换中性化档全部劣化（0.27–0.51）——与 in6「换档全削」同型。

### L4-R · 换基线（decay8）后外层重扫（2026-11-21，批 `32o091e8Z4LvbbkrMRxtlnx`，5 臂）

| 臂 | 外层 | α | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|
| **R-1** | **`group_scale`（baseline）** | `pwaM6Kxg` | **0.70** | **0.18** | 0.60 | 40.8% | 3 |
| R-2 | `group_backfill(·,252)` | `vRApLX1Q` | 0.64 | 0.16 | 0.92 | 39.9% | 3 |
| R-3 | `group_backfill(·,120)` | `XgavpA9b` | 0.65 | 0.16 | 0.91 | 39.8% | 3 |
| R-4 | `group_zscore` | `LLKmpdE9` | 0.64 | 0.15 | 0.73 | 40.5% | 3 |
| R-5 | `group_neutralize` | `6XMowLdY` | 0.63 | 0.15 | 0.84 | 40.1% | 3 |
| R-6 | `group_rank` | `omaJK0ob` | 0.43 | 0.09 | 0.35 | 34.3% | 3 |

**L4-R 结论**：decay8 下 **`group_scale` 仍最优（0.70）**，外层排序不变 ⇒ 换基线未改变外层选择（与 imb5「换基线后内核排序反转」不同：fhp 的外层排序对 decay 稳健）。梯度收敛闭环成立。

---

## ★ 完整梯度终态（5 层 / 53 臂）

| 层 | 全类别覆盖 | 最优 | 收敛结论 |
|---|---|---|---|
| L1 信号构造（9 概念 + 4 水平 = 12 臂） | 9 主概念 + 18 字段（`_active` 孪生排除写明） | 分布评分 0.22 | 配比/水平全弱；大单/耐久/信念「2Y 有 S 无」 |
| L2 内层时序（15/16 可测） | Time Series 15 + 窗口 | `ts_quantile` × 126 **0.32** | 排名类唯一可用；ts_scale 失效（2Y −1.18） |
| L3 分组轴（6 臂） | industry…country | `industry` 0.32 | industry≡subindustry；market≡exchange≡country |
| L4 外层包装（7 臂） | Group 7（group_mean/count 排除写明） | `group_scale` **0.53** | +0.21 最大单层增益；聚合型 TO 115% 崩 |
| L5 设置档（4 档 × 2） | 中性化 4 + decay | SUBINDUSTRY + **decay8** **0.70** | 换档全削；decay8 +0.17 |

**最终判定（完整梯度后，可写死）**：
- **fhp 天花板 = S0.70 / F0.18 / 2Y0.60 / TO40.8%**（53 臂 × 5 层全类别后最高点），**距 S 闸 1.58 差 0.88**；TO 40.8% 已超内部严线带。
- **信号层结构性弱**：9 概念最强 0.22；架构层（内核/轴/外包/设置）合计 +0.48（0.22→0.70），但起点太低；与历史死键「stageA best S0.79 / 2Y1.56 / margin 1.5bp」同量级 ⇒ **完整梯度独立复现了死键结论**。
- **判死层级：信号层弱（与数据集级死键一致，维持 `fund_holdings_panel_dead` 不改）**；本档案提供「完整梯度也弱」证据（补 §7.6 D1–D6 的模板/字段族/矩/轴/非线性/配置维度）。
- 适用域：**2015–2023**（2014 无数据，见前置体检）。
- **验证门槛**：`gradient_gate` 应判 GRADIENT_DONE（arc_layers=5）。

---

## Layer 2–5 计划（L1 结果出来后按最优配比续填）

| 层 | 槽位 | 全类别候选 | 臂数 |
|---|---|---|---|
| **L2 内层时序** | `<K>(SIG, 126)` | Time Series 可测全集 16：ts_zscore(基线)/ts_scale/ts_rank/ts_quantile/ts_mean/ts_std_dev/ts_delta/ts_av_diff/ts_arg_max/ts_arg_min/ts_ir/ts_returns/ts_product/ts_sum/ts_max_diff/days_from_last_change（ts_step 只收数字、target_tvr_*/hump 需命名参 ⇒ 排除写明） | 16（2 批×8） |
| **L2b 窗口** | `ts_zscore(SIG, N)` | N ∈ {66, 126, 250, 504}（+ 双窗可选） | 4 |
| **L3 分组轴** | `group_rank(·, G)` | industry/sector/subindustry/market/exchange/country | 6 |
| **L4 外层包装** | `group_rank` → Group 类 | group_rank/zscore/neutralize/scale/std_dev/sum/backfill×2（group_mean 签名、group_count 常数排除） | 8 |
| **L5 设置档** | 中性化 × decay | SUBINDUSTRY(基线)/INDUSTRY/SECTOR/FAST + decay{4,8} | 4 批 × 2 |

⚠ 验收①：18 字段中 9 个 `_active` 是主版同概念孪生（description 逐字同源）⇒ 排除并写明；主版 9 概念全部进 L1（本批 8 + 下批 1 广度）。

## 状态

- 台账：**维持死键**（本轮为用户授权重测，未改）；完整梯度独立复现死键结论（最高 S0.70 vs 历史 0.79）。
- `gradient_gate --region GBR --dataset fund_holdings_panel --field-prefix transaction_` → **GRADIENT_DONE**（dom=12 / arc_layers=6 / arc_rows=8 / total=738）。
- 交付结论：**0 颗**（S 天花板 0.70，距闸 0.88；TO 40.8% 超内部严线带）。
- 梯度完成：**5 层 / 53 臂**（L1 12 + L2 15 + L3 6 + L4 7 + L5 8 + L4-R 5）。