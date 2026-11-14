# ★ATOM 重构结论：形态可行但 S 过不了闸（DEU insiders）

日期：2026-11-12
BE172 `4AO7cF4Ao4wB9pp1agfXatOR`（纯 insiders1，10 臂）+ BE173 `1XmMzB8BC4DT98L13JNvX2FT`（纯 insider_agg_matrix，10 臂）

## 一、ATOM 的机制被完全验证（铁证两条）

读 6 颗 ATOM 件的 checks 明细：

| alpha | S | Y2 | 塔数 | 有 IS_LADDER_SHARPE？ | 闸5 | fail 内容 |
|---|---:|---:|---:|---|---|---|
| A1x9mO9Y | 1.22 | 0.85 | **1** | ❌ **没有** | **OK** | LOW_SHARPE / CONC / SUB / **LOW_2Y_SHARPE** |
| e7amvqkE | 1.17 | 1.10 | 1 | ❌ 没有 | OK | 同上 |
| pwamZ1Yq | 1.11 | 1.11 | 1 | ❌ 没有 | OK | + LOW_FITNESS |
| N1P03jQp | 0.86 | 1.89 | 1 | ❌ 没有 | OK | 仅 LOW_SHARPE / LOW_FITNESS |
| vRA86zjb | 0.76 | 1.93 | 1 | ❌ 没有 | OK | 仅 LOW_SHARPE / LOW_FITNESS |
| 1YWePmxk | 0.66 | 2.06 | 1 | ❌ 没有 | OK | 仅 LOW_SHARPE / LOW_FITNESS |

**铁证 1**：ATOM 件里 `IS_LADDER_SHARPE` 完全消失，替换为 `LOW_2Y_SHARPE`
⇒ 与官方「放松 IS Ladder，仅要求最近两年 2-Year Sharpe」**逐字对应**。
⇒ 这也反证：之前多颗非 ATOM 件卡 `IS_LADDER_SHARPE`（ladderWin=3/4）是**结构导致**，不是信号不行。

**铁证 2**：6/6 全部 `gate5 = OK`
⇒ 「单字段 × 单算子形态 × 多窗」确实是闸5 放行形态（同形态不同窗）。
⇒ **ATOM + 闸5 双合规的构造空间是真实存在的。**

## 二、但 S 过不了闸

### BE172（纯 insiders1，单字段 holdings）

| 臂 | 形态 | S | F | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|---:|
| A10 Δ 单窗66 | Δ66 | **1.22** | 1.10 | 0.85 | 0.31 | 4 |
| A8 Δ 多窗66/132 | ΔΔ | 1.17 | 1.01 | 1.10 | 0.04 | 4 |
| A5 Δ 多窗22/66/132 | ΔΔΔ | 1.11 | 0.95 | 1.11 | 0.42 | 5 |
| A9 ts_ir 单窗66 | ir66 | 1.07 | 0.90 | 1.13 | 0.46 | 4 |
| A1 ts_ir 22+66 | ir,ir | 1.06 | 0.86 | 0.68 | 0.46 | 4 |
| A4 Δ 22+66 | Δ,Δ | 1.06 | 0.80 | 0.93 | 0.68 | 4 |
| A3 ts_ir 66/132 | ir,ir | 1.03 | 0.82 | 1.26 | 0.33 | 4 |
| A6 水平 22+66 | lvl,lvl | 0.94 | 0.74 | 0.62 | 0.25 | 4 |
| A7 水平 66/132 | lvl,lvl | 0.76 | 0.52 | 0.53 | 0.27 | 4 |

**最高 S 1.22，10/10 fail≥4。多窗平滑没有带来增益**（A1-A8 全在 0.76-1.17）。

### BE173（纯 insider_agg_matrix）

| 臂 | 形态 | S | F | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|---:|
| B4 HHI 单窗66 | hhi66 | **0.86** | 0.50 | **1.89** | 0.50 | 2 |
| B5 SV1 22+66 | sv1,sv1 | 0.79 | 0.45 | 1.60 | 0.22 | 3 |
| B1 HHI 22+66 | hhi,hhi | 0.76 | 0.43 | **1.93** | 0.37 | 2 |
| B7 DI 66/252 | di,di | 0.70 | 0.41 | 1.06 | 0.24 | 4 |
| B6 DI 132/252 | di,di | 0.69 | 0.40 | 1.17 | 0.27 | 4 |
| B2 HHI 22/66/132 | hhi×3 | 0.66 | 0.33 | **2.06** | 0.42 | 2 |
| B9 HHI 44/88 | hhi,hhi | 0.64 | 0.33 | 1.60 | 0.47 | 2 |
| B8 DI 单252 | di252 | 0.59 | 0.31 | 1.12 | 0.21 | 4 |
| B3 HHI 66/132 | hhi,hhi | 0.59 | 0.28 | 1.95 | 0.44 | 2 |
| B10 HHI 四窗 | hhi×4 | 0.54 | 0.25 | 1.90 | 0.45 | 2 |

**最高 S 0.86，10/10 fail≥2。但注意 2Y 很高（1.60-2.06）**
⇒ HHI 在**近两年有效**、全期弱。这是「近期风格」而非「持续 alpha」。

## 三、根因归因

原版能到 S 2.20-2.36 的两个信息源，拆开各自都过不了闸：

| 组成 | 单独 S | 合起来 S |
|---|---:|---:|
| insiders1 的 holdings 变化（A/B/F）| **1.22** | — |
| insider_agg_matrix 的 HHI 集中度（C）| **0.86** | — |
| **A/B/F × C × analyst 腿** | — | **2.36** |

⇒ **原版的高 S 正是来自跨数据集信息互补 + 跨腿相加的权重叠加。**
⇒ 这两个手段恰好是 ATOM（禁跨数据集）与闸5（禁跨腿相加）各自禁止的。

**结论：在 DEU insiders 上，ATOM + 闸5 双合规与 S≥1.58 不可兼得。**
这不是投入量问题，是信息量问题——单数据集的 insiders 信息不足以单独支撑 1.58 的 Sharpe。

## 四、三条现实路径（需用户裁决）

| 路径 | 做法 | 预期结果 | 代价 |
|---|---|---|---|
| **P1 放宽闸5，坚持 ATOM** | 允许同数据集内跨形态/跨字段叠加（如 `add(Δ66, ts_ir66)`），仍单数据集 | S 可能到 1.4-1.6，但仍可能不够 | 违反闸5；但 ATOM 免 IS_Ladder 仍在 |
| **P2 放宽 ATOM，坚持闸5** | 跨数据集但同形态多窗（如 holdings 多窗 + HHI 多窗做不到，因为跨数据集）| 基本不可行（闸5 禁跨字段，跨数据集必然跨字段）| — |
| **P3 两条都放宽（= 原范式）** | 跨数据集 + 跨腿相加 | **S 2.20-2.36，已验证** | 撞闸5；非 ATOM 要过 IS_Ladder |
| **P4 降 targets** | 接受 S 1.22 的 ATOM 件 | 过不了 LOW_SHARPE(1.58) | 平台不可提交 |

**P4 不可行**（1.22 < 1.58，平台会拒）。**P1 值得一试**——它是唯一可能同时满足「ATOM 免 ladder」与「S 够」的形态，因为 ATOM 只禁跨 dataset，不禁同 dataset 内跨形态。

## 五、下一步（若用户选 P1）

在**单一 dataset 内**做跨形态叠加，测试能否把 S 从 1.22 推到 1.58：

```
insiders1 内（单 dataset，ATOM）：
  add(group_rank(ts_delta(ts_mean(holdings,66),66),sector),
      group_rank(ts_ir(holdings,66),sector),
      group_rank(divide(1,add(days_from_last_change(holdings),1)),sector))
  ↑ 跨形态（Δ / ts_ir / 倒数天数）同字段，撞闸5 但是 ATOM

insider_agg_matrix 内（单 dataset，ATOM）：
  add(HHI多窗, SV1多窗, directional_indicator长窗)
  ↑ 跨字段同数据集，撞闸5 但是 ATOM
```

这是「宁可撞闸5 也要保 ATOM」的取舍方向，因为 ATOM 免掉的 IS_Ladder 是硬闸、闸5 是内部纪律。