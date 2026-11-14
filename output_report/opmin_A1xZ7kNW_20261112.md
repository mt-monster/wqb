# op-min 收口：`A1xZ7kNW`（DEU / TOP500 / intraday_pv_feats）

生成时间：2026-11-12 17:05 (GMT+8)｜skill：`wq-alpha-gate-push-op-min`｜**未提交**

---

## 0 结论

**3 算子已是下限，不可交付。判死，换信息源。**

| 硬闸 | 状态 |
|---|---|
| IS 八项（S 1.75 / F 1.01 / 2Y 1.72 / sub 1.04 / CLUSTER 1.52） | 全 PASS，但 **F 仅余量 0.01** |
| **CONCENTRATED_WEIGHT** | **WARNING 且 val=null** → `submit_gate` 硬拦（`WebDataScope Failed RA=1`） |
| **PROD_CORRELATION** | **0.8377 > 0.70**，硬墙超线 0.138 |
| self | 0.1481 ✅ |
| 塔 | DEU/D1/PV ×1.6（ATOM） |

**两道墙互斥**：能压 prod 的换概念件 IS 全崩；能保 IS 的水平矩件 prod 恒在 0.82–0.88。

---

## 1 原件

```
ts_target_tvr_decay(group_rank(ts_zscore(skew_bid_ask_size_to_volume_ratio, 252), sector), target_tvr=0.45)
```

DEU / TOP500 / delay 1 / decay 4 / INDUSTRY / trunc 0.08 / nan ON｜**3 算子**

逐年 **2014–2023 十年完整无空窗**（2018 是 0.12 弱年，近三年 0.89/1.35/2.32）⇒ 样本有效，**允许调参**（与 `QPveY7Kg` 只有 5 年有效样本不同）。

---

## 2 ★ 发现一：CW 硬门由 `ts_target_tvr_decay` 引入

`submit_gate` 按 WebDataScope 口径把 `result != PASS/PENDING` 一律计失败（`config.py:410`），`CONCENTRATED_WEIGHT` 在 `RA_CHECK_NAMES` 内 ⇒ **WARNING 也算硬失败**，且 val/limit 都为 null（平台未回填数值）。

因果证据：

| alpha | 构造 | CW |
|---|---|---|
| `npaRgLbE` | 裸骨架，**无** tvr_decay，industry 轴 | **PASS** |
| `A1xZ7kNW` / `LLKadk9v` | + `ts_target_tvr_decay` | WARNING |
| 批 1 全部 12 条（换轴 / 换字段 / 换 L3 / 换 L4 / 换 τ） | 全部含 tvr_decay | **全 WARNING** |
| 批 2 `MP6R1epM`（hump）、裸骨架 decay 8/12/16/20/24/28/32 | 无 tvr_decay | **全 PASS** |
| 收口批 truncation 0.01/0.02/0.04/0.15 | 有 tvr_decay | 全 WARNING |

⇒ **truncation 与 CW 无关；`tvr_decay` 是唯一元凶。** 但 `tvr_decay` 同时是把 F 从 0.59 推到 1.01 的唯一杠杆（历史报告已证：S 1.72→1.75，F 0.59→1.01）。

裸骨架用 settings 层 decay 压换手（零算子成本）：

| decay | 8 | 12 | 16 | **20** | 24 | 28 | 32 |
|---|---|---|---|---|---|---|---|
| S | 1.81 | 1.75 | 1.69 | **1.62** | 1.54 | 1.46 | 1.38 |
| **F** | 0.83 | 0.91 | 0.96 | **0.98** | 0.97 | 0.95 | 0.91 |
| 2Y | 1.59 | 1.66 | 1.65 | **1.66** | 1.62 | 1.57 | 1.51 |
| CW | PASS | PASS | PASS | **PASS** | PASS | PASS | PASS |

**F 峰值 0.98，永远差 0.02。** 峰后 S 掉闸。⇒ 无 tvr 路线到不了 F≥1.0。

---

## 3 ★ 发现二：prod 墙是「信号概念」层面的，不是参数层面的

`plan.py` 结构性判定命中：**S ≥ 1.40 且 prod ≥ 0.70 ⇒ 本族 S↔prod 前沿已到顶，调参无效，必须换横截面/换概念。**

本轮 6 颗 prod 实测（全部 `prod_peek` 实读，status=ok）：

| alpha | 构造 | **prod** |
|---|---|---|
| `A1xZ7kNW` | 原件（历史实测） | **0.8377** |
| `E5QWlQVK` | 换横截面 `rank()` 全市场 | 0.8172 |
| `ZYa30NNn` | 裸骨架 decay 16 | **0.8702** |
| `akaZbEg1` | 裸骨架 decay 20 | 0.8783 |
| `2r5zl55P` | tvr τ=.30 | 0.8490 |
| `blaZOvmZ` | truncation 0.02 | 0.8375 |
| **`d5aVjaWx`** | **P3 水平→变化 `ts_delta(f,22)`** | **0.6031 ✅ 破墙** |

⇒ 换轴、换字段、换 τ、换 truncation、换 decay，**prod 全在 0.817–0.878**，一点没动。
⇒ **唯一破墙路径是换信号概念**（`ts_delta` 变化率而非水平矩），印证「本平台冷门 ≠ 生产池冷门」。

---

## 4 ★ 发现三：破 prod 的换概念件，IS 救不回来

`d5aVjaWx`：`ts_target_tvr_decay(group_rank(ts_zscore(ts_delta(f,22),252),sector),target_tvr=0.45)`
**S 1.53 / F 0.75 / 2Y 0.92 / sub 1.11 / CW WARNING**，三项硬闸全掉。

批 4 用 `ts_delta` 窗口绝对值阶梯 + `ts_zscore` 窗口 + 轴扫描（10 条，全部无 tvr ⇒ CW PASS）：

| 变体 | S | F | 2Y | 结果 |
|---|---|---|---|---|
| delta 5 / 11 / 66 / 126 / 252 | 0.58–1.38 | 0.22–0.48 | 0.34–1.31 | 全死 |
| delta 44 | 1.22 | 0.51 | 1.23 | 死 |
| zscore 126 / 504 | 1.49 / **1.59** | 0.64 / 0.71 | 0.88 / 1.13 | F、2Y 掉 |
| 轴 industry / market | 1.53 / 1.57 | 0.64 / 0.70 | 1.18 / 1.03 | F、2Y 掉 |

**2Y 最好只有 1.31（需 ≥1.585），F 最好 0.71（需 ≥1.0）。** 无任何窗口/轴能把换概念件推回全闸。

---

## 5 算子数：3 是下限

| 删除 | alpha | ops | S | F | 判定 |
|---|---|---|---|---|---|
| 删 `group_rank` | `blaZjaOm` | **2** | 1.63 | **0.90** | F 掉闸 + CW WARNING |
| 删 `ts_zscore` | — | 2 | — | — | 语义上等于删信号 |
| 删 `ts_target_tvr_decay` | `npaRgLbE` | 2 | 1.72 | **0.59** | F 掉闸（历史实证） |

⇒ **3 个算子没有一个可删**。本轮没有任何 ≤2 算子且全闸通过的版本。

---

## 6 四批全景（40 条仿真）

| 批 | 内容 | 规模 | 结果 |
|---|---|---|---|
| 1 | P1 换横截面/轴、P2 换冷门字段、P3 换概念、L3/L4 等效替换、τ 档、2 算子删除 | 12 | 全带 CW WARNING；仅 τ=.30 有 F 1.03 |
| 2 | `tvr_hump` / `hump` 替代 + 裸骨架 decay 8/12/16 | 6 | CW 归因成功；裸骨架 F 峰值 0.96 |
| 3 | decay 20/24/28/32 + truncation 4 档 + delta 裸骨架 decay | 12 | F 峰值 0.98；CW 与 truncation 无关 |
| 4 | `ts_delta` 窗口阶梯 6 档 + zscore 2 档 + 轴 2 档 | 10 | 换概念 2Y/F 全掉 |

**prod 实测 6 颗**（上表）。

---

## 7 判定与止损（skill ⑥）

- **全闸通过 = 否**：`submit_gate` 被 `CONCENTRATED_WEIGHT` 硬拦，且 prod 0.8377 超线 0.138。
- **算子最少 = 3**（已达成，但无交付价值）。
- **止损条件命中**：4 轮结构性闸门未破，已完整走完 ③ 杠杆扫描（换横截面/换字段/换概念/τ/decay/truncation）与 ④ 消融扫描（2 算子删除）。
- **判死理由**：不是调参问题，是**信号概念与生产池撞车**。该字段是 vendor 标准微观结构指标，各家独立收敛到 `ts_zscore + group_rank` 骨架；换概念能躲开 prod，但 DEU/TOP500 上 2Y 与 F 同时不达标。
- **建议**：转 `pattern_scores` 或换数据集（历史报告 V2/V3 选项），不要在这颗上继续投仿真。

**未提交。** 提交权归用户；本件当前不可提交。

---

## 8 产物

- 批次：`results/batch_A1xZ7kNW_opmin1.txt`(12，拆 1a/1b 派发，平台 multi-sim 上限 10)、`opmin2.txt`、`opmin4.txt`；spec：`_A1xZ7kNW_notvr_spec.json`、`_A1xZ7kNW_decay2_spec.json`、`_A1xZ7kNW_final_spec.json`
- 签核：`results/op_coverage_signoff.jsonl` 4 条（session `A1xZ7kNW-opmin1..4`）
- prod：`results/prod_wait_{E5QWlQVK,ZYa30NNn,d5aVjaWx,2r5zl55P,akaZbEg1,blaZOvmZ}.json`
- 原始读数：`results/_corr_out.json`（历史 0.8377 / 0.8446）
