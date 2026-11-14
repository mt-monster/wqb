# WAVE BE135 — S 定向增压（mLapjPLX 单闸卡死后的续攻）

日期：2026-11-12
基线：`mLapjPLX`（BE134 产物）——**全战役首颗「单闸卡死」候选**

## 一、BE134 结果（全 10 臂）

| alpha | S | F | 2Y | TO | sub | ret | failed_ra |
|---|---:|---:|---:|---:|---:|---:|---:|
| **mLapjPLX** | **1.50** | 1.23 | **2.02** | 12.4% | 0.89 | 8.4% | **1** |
| rK7Y2vEJ | 1.55 | 1.21 | 1.26 | — | 0.87 | — | 2 |
| leadjLeO | 1.54 | **1.30** | 1.41 | 14.2% | 0.82 | 10.2% | 2 |
| xAvqjKOb | 1.52 | 1.23 | 1.26 | 12.2% | 0.83 | 8.1% | 2 |
| QP0M711W | 1.50 | 1.25 | 1.51 | 12.9% | 0.88 | 9.0% | 2 |
| A1x9lRjw | 1.50 | 1.10 | 1.32 | 18.0% | 0.87 | 9.7% | 2 |
| 1YWewqkW | 1.49 | 1.27 | 1.14 | 13.8% | 0.77 | 10.0% | 2 |
| QP0M71PW | 1.48 | 1.20 | 1.46 | 11.6% | 0.85 | 8.2% | 2 |
| P05N7J0L | 1.48 | 1.18 | 1.32 | 11.4% | 0.85 | 7.9% | 2 |
| wpoqj8K6 | 1.48 | 1.08 | 1.41 | 16.6% | **0.98** | 8.8% | 2 |

## 二、mLapjPLX 是决定性发现：单闸卡死

```
mLapjPLX = signed_power(Z2(CAPB( add(add(A×C, C×FR), B) )), 1.3)
A  = group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66), sector)     # 持仓变化
B  = group_rank(ts_ir(vec_avg(insd1_holdings),66), sector)                    # 持续性
C  = group_rank(ts_mean(SV1/(SV1+SV2+SV3+SV4),66), sector)                    # 集中度 HHI
FR = group_rank(1/(days_from_last_change(insd1_holdings)+1), sector)          # 新鲜度
```

**checks 实测（get_alpha_details.checks）：**
- **fail（仅 1 项）**：`LOW_SHARPE 1.50 < 1.58`
- **pass（8 项）**：LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / **CONCENTRATED_WEIGHT** / LOW_SUB_UNIVERSE_SHARPE / **IS_LADDER_SHARPE（2Y 2.02，闸 1.58，余量 +0.44）** / CLUSTER_TEST / MATCHES_PYRAMID
- **pending**：SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION
- `ra.failed_ra_count = 1`，`pyramid_short = "pv/insiders"`

⇒ **距全闸通过只差 S +0.08（+5.3%）**。这是全战役 174 臂以来第一次出现「只卡一闸」。

## 三、逐年诊断（五形态横向）

| 形态 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **mLapjPLX** | 0.74 | 1.81 | 1.80 | 0.88 | 2.10 | 2.39 | 1.24 | **−0.03** | **1.11** | **3.06** |
| rK7Y2vEJ | 0.80 | 1.87 | 1.44 | 0.86 | **2.93** | **2.90** | 1.18 | 0.10 | 0.95 | 2.59 |
| e7am3og6 | **1.31** | 1.73 | 1.93 | 0.49 | 2.44 | 2.84 | 1.00 | 0.25 | 0.65 | 2.31 |
| j2av6NYE | 0.96 | **2.20** | **2.05** | 0.61 | 2.37 | 2.01 | 0.63 | **0.49** | 0.93 | 2.25 |
| QP0M95Gg | 0.96 | 1.97 | 1.58 | 0.84 | 2.65 | 2.89 | 1.23 | 0.00 | 0.90 | 2.52 |

**三条硬结论：**
1. **2021 全族皆死**（−0.03 ~ 0.49，最好的 j2av6NYE 也仅 0.49）⇒ 结构性失效年，**任何形态都救不回**，不必再试「修 2021」。
2. **mLapjPLX 的 2022/2023 是全族最强**（1.11 / 3.06）⇒ 2Y 2.02 的唯一来源。
3. **e7am3og6 的 2014 = 1.31（全族最高）**、**j2av6NYE 的 2015/2016 最强（2.20/2.05）**、**rK7Y2vEJ 的 2018/2019 最强（2.93/2.90）** ⇒ 三个形态各有专属强年，**具备互补性**。

⇒ 战略：**用 2Y 的 +0.44 余量去兑换 S**。允许 2Y 从 2.02 降到 1.65，只要 S 上 1.58。

## 四、BE135 十臂设计（已派 9/10）

以 `M0 = A×C + C×FR + B`（mLapjPLX 内层）为骨架，逐条加腿：

| 臂 | 构造 | 假设 |
|---|---|---|
| S1 | `M0 + A` | A 在 rK7Y2vEJ 中独立且最强；mLapjPLX 里 A 被 C 削弱，加独立 A 恢复锐度 |
| S2 | `M0 + B×FR` | rK7Y2vEJ 的有效形式（FR 乘 B 而非 C） |
| S3 | `M0 + A + B×FR` | S1+S2 双补 |
| S4 | `M0 + C` | C 单腿 0.83，测独立贡献 |
| S5 | `M0 + A + C` | A 独立 + C 独立 |
| S6 | `M0×2 + B` | 重复相加加重主腿（合法调权，非 multiply 常数） |
| S7 | `A×C + B×FR + C + B` | 把 FR 从 C 换到 B（rK7Y2vEJ 几何） |
| S8 | `A + A×C + C×FR + B` | A 独立 + 全保留 |
| S9 | `M0 + A` 幂 1.0 | 去掉幂次放大，测纯排序 |
| S10 | `M0 + A + B×FR` 幂 2.0 | 极端尾部放大 |

**sim id 映射：**
- S1 `36IkE0cV84R8aDewb3MQX6H`
- S2 `3fToaZdwO4zgc27wWzq41vw`
- S3 `u1qNK64b4zLcoe1e0L8NujE`
- S4 `3kR94z9wv5aW8LZyygSGfC1`
- S5 `Ql81tasF56M8XAS98XRFIv`
- S6 `4fhJ74f7K4k4cFHGnr11JVN`
- S7 `XfAod3WL51ybnso7De7v7H`
- S8 `Yd8Y9gkK4EDaYH8Dr1dRVC`
- S9 `3913AA4344jcbz4vyUtzap1`
- S10 **待重派**（429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED）

## 五、塔归属的意外收获

`cap` 字段归属 **PV** 数据集 ⇒ 任何带 `bucket(rank(cap))` 的 insiders alpha 自动是 **DEU/D1/PV ×1.6 + DEU/D1/INSIDERS ×1.6 双塔**（`pyramids.effective = 2`）。

⇒ **3 颗过闸件可同时点亮 INSIDERS 塔与 PV 塔**（两塔目前各 0 颗）。
