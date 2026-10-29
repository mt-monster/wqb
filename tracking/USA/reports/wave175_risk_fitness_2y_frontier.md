# 波 175 — RISK 塔 F/2Y 双闸前沿攻坚

**区域**：USA / TOP3000 / D1
**数据集**：`mfm_model_output`（RISK category，117 字段，cov 0.9963，alphaCount 308，valueScore 3.0）
**主字段**：`discount_store_retail_score`（实为「日度特质残差收益 %」，命名陷阱）
**波次结论**：PARTIAL（n_pass=0 / n_near=2），但**收尾时拿到全闸 alpha**

---

## 1. 出发点（波 174 遗留的结构性对立）

波 174 已证明 F（fitness）与 2Y（近两年 Sharpe）在本信号上朝相反方向走：

| alpha | 配置 | S | F | 2Y | 唯一失败项 |
|---|---|---|---|---|---|
| `E563Eea1` | subindustry s22 + decay 8 | — | **1.00** ✅ | 1.12 ✗ | LOW_2Y_SHARPE |
| `j2YL06rE` | subindustry s22 + decay 16 | 1.62 | **1.03** ✅ | 1.16 ✗ | LOW_FITNESS(2Y) |
| `vR10lNYd` | subindustry s66 + decay 0 | 1.77 | 0.87 ✗ | **1.71** ✅ | LOW_FITNESS |
| `A1V670QW` | **sector** s66 + decay 0 | 1.65 | 0.95 ✗ | **1.65** ✅ | LOW_FITNESS |

**待解问题**：能否找到同时满足 `F ≥ 1.0` 且 `2Y ≥ 1.58` 的设置？

---

## 2. 实验矩阵（21 条）

骨架统一为 `group_rank(reverse(ts_decay_linear(ts_backfill(discount_store_retail_score, 22), W)), G)`，
全部 STATISTICAL / TOP3000 / D1 / truncation 0.05（注明者除外）。

### 2.1 hump 阶梯（算子族杠杆）

| # | hump | 平滑 W | S | F | TO | R | 2Y |
|---|---|---|---|---|---|---|---|
| — | 0 | 66 | 1.77 | 0.87 | 26.20% | 6.30% | 1.71 |
| H1 | 0.0005 | 66 | 1.20 | 0.66 | 11.32% | 3.80% | 1.10 |
| H2 | 0.001 | 66 | 0.82 | 0.27 | 3.43% | 1.37% | 0.73 |
| H3 | 0.002 | 66 | 0.62 | 0.18 | 3.26% | 1.06% | 0.72 |
| H4 | 0.001 | 22 | 0.71 | 0.22 | 3.45% | 1.20% | 0.49 |

**判死**：margin 从 4.81bp 升到 6.71bp（+39%）但 S −32%、R −40%，`F = S·sqrt(R/TO)` 净降 24%。
阈值 ≥0.001 时 TO 锁死在 3.3% 不动 —— 这是悬崖不是旋钮。**hump 在本信号上不可能有用，不再重试。**

### 2.2 universe 杠杆

| # | universe | S | F | 2Y |
|---|---|---|---|---|
| U1 | TOP1000 | 0.85 | 0.26 | 0.24 |
| U2 | TOP500 | 0.73 | 0.21 | 0.55 |
| — | TOP3000 | 1.77 | 0.87 | 1.71 |

**判死**：该特质残差反转异象**只活在中小盘**，降 universe 直接毁信号。

### 2.3 nanHandling 隔离（零影响，三重确认）

| 配对 | 结果 |
|---|---|
| `GrWVeL7Q` vs `Vkxn3o3b` | 逐位相同（0.82 / 0.27 / 3.43% / 1.37 / 0.73） |
| `78LOnak8` vs `leAx3XK8` | 逐位相同 |
| `omE2gqXm` vs `78LO188Z` | 逐位相同（2.16 / 0.95 / 39.33% / 1.53） |

⇒ 波 172(ON) 与 173(OFF) 的对比顾虑正式排除，此后不必为此分批发仿真。

### 2.4 分组轴四档（W=66, decay 0）

| 分组轴 | alpha | S | F | TO | R | 2Y | SUB |
|---|---|---|---|---|---|---|---|
| subindustry | `vR10lNYd` | **1.77** | 0.87 | 26.20% | 6.30% | 1.71 | — |
| **industry** | `gJev8YnM` | 1.71 | 0.93 | 24.16% | 7.20% | **1.73** | 0.83 |
| sector | `A1V670QW` | 1.65 | 0.95 | 22.49% | 7.38% | 1.65 | — |
| market | `88RAe0zW` | 1.57 | 0.90 | 22.04% | 7.20% | 1.63 | 0.83 |

⇒ **分组越粗 → TO 越低、margin 越高、F 越高、S 越低；2Y 在 industry 取峰值（非最粗的 market）。**
industry 是 2Y 的甜点轴，sector 是 F 的甜点轴。

### 2.5 窗口轴（sector, decay 0）

| 窗口 W | alpha | S | F | TO | R | 2Y |
|---|---|---|---|---|---|---|
| 22 | `88RAp5Lo` | **1.98** | 0.98 | 35.33% | 8.57% | 1.46 |
| 66 | `A1V670QW` | 1.65 | 0.95 | 22.49% | 7.38% | 1.65 |
| 252 | `1YNvz8pk` | 1.55 | 0.94 | 18.23% | 6.68% | **1.98** |

⇒ **窗口是「用 S 换 2Y」的轴**，F 基本不动。2Y 随窗口单调上升。

### 2.6 平台 decay 轴（sector s66）

| decay | alpha | S | F | TO | 2Y |
|---|---|---|---|---|---|
| 0 | `A1V670QW` | 1.65 | 0.95 | 22.49% | 1.65 |
| 1 | `wpQ6E7rY` | 1.65 | 0.95 | 22.48% | 1.65 |
| 2 | `YP1ZvjWA` | 1.58 | **1.00** | 17.70% | 1.57 |

⇒ decay 0→1 是**无效档**（TO 只掉 0.01pp）；decay 1→2 是**悬崖**（2Y −0.08）。
平台 decay 是「用 2Y 换 F」的轴，且转换点极陡。

### 2.7 交叉象限（本波核心补测）

把「2Y 甜点轴（industry）」与「F 杠杆（decay 2）」相乘：

| # | 配置 | alpha | S | F | TO | 2Y | SUB | invest_r | fRA |
|---|---|---|---|---|---|---|---|---|---|
| **R4** | **industry s66 decay2** | **`ZYQZEawY`** | **1.64** | **1.00** ✅ | 18.58% | **1.64** ✅ | 0.78 ✅ | **0.8049** | **0** |
| R5 | sector s252 decay2 | `LLMeGmJa` | 1.51 ✗ | 0.99 | 15.00% | **1.90** | 0.72 | 0.7285 | 2 |

---

## 3. ★ 关键成果：`ZYQZEawY` 全闸

```
group_rank(reverse(ts_decay_linear(ts_backfill(discount_store_retail_score, 22), 66)), industry)
STATISTICAL / TOP3000 / D1 / decay 2 / truncation 0.05 / nanHandling OFF
```

| 指标 | 值 | 闸 |
|---|---|---|
| Sharpe | 1.64 | ≥1.58 ✅ |
| **Fitness** | **1.00** | ≥1.00 ✅ |
| **2Y Sharpe** | **1.64** | ≥1.58 ✅ |
| Turnover | 18.58% | 区间内 ✅ |
| Returns | 6.85% | — |
| Margin | 7.37bp | — |
| Drawdown | 7.66% | — |
| Sub-universe | 0.78 | ≥1.64×0.4346=0.71 ✅ |
| Investability Sharpe | 1.32 | — |
| **invest_S / S** | **0.8049** | ≥0.70 ✅（自设闸） |
| longCount / shortCount | 1563 / 1563 | 均衡 ✅ |
| **ra_failed_checks** | **[]** | **fRA = 0** ✅ |
| pyramid | `USA/D1/RISK`（multiplier 1.1） | 点塔 ✅ |

`checks.pass` 8 项：LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER /
CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / **LOW_2Y_SHARPE** / MATCHES_PYRAMID。
`checks.fail` = **空**。仅 3 条 warning（CLUSTER_TEST 1.22/1.58、MATCHES_THEMES、OSMOSIS_ALLOCATION）。

**这是 RISK 塔在本战役中第 1 颗全闸 alpha（0/3 → 1/3）。**

---

## 4. zscore 分支：更高的天花板，但撞子域墙

同一骨架换 `group_zscore`：

```
group_zscore(reverse(ts_decay_linear(ts_backfill(discount_store_retail_score, 22), 66)), sector)
```
`RREXmrro`：**S 1.91 / F 1.30 / 2Y 1.96 / R 14.04% / margin 9.22bp**

- `checks.pass` 含 **LOW_2Y_SHARPE**（1.96）
- `checks.fail` = **唯一一项 `LOW_SUB_UNIVERSE_SHARPE`：0.75 vs limit 0.83**

**USA 子域阈值的精确口径**：`limit = 0.83 = 1.91 × 0.4346` ⇒ **ratio 门槛 ≈ 0.4346**
（注意：这与 DEU/TOP500 的 0.4743 不是同一个数，不可跨区套用）。

同一批全部 7 颗 rank 版全部通过该闸，比值稳定在 0.48–0.53；
zscore 版掉到 **0.393**。⇒ **横截面变换决定子域可得性**，不是 decay/truncation/分组轴能补的。

**机理**：`group_rank` 输出均匀权重，`group_zscore` 按原始偏差赋权 —— 而偏差极值集中在
小盘/低流动性残差股，这些票不在更流动的子域里。R +107%（7.38%→14.04%）正是这种集中度的产物。

**结论**：zscore 分支的 SUB 缺口是 11%（需 0.83，有 0.75），比 2Y 的 0.6% 缺口大得多。
**主路径走 rank，zscore 仅作为「若换数据集需要更高 Sharpe 天花板」的备选。**

---

## 5. 归因总结：三条正交杠杆

| 杠杆 | 主要作用指标 | 副作用 | 可调性 |
|---|---|---|---|
| **inner 窗口 W** | 2Y（单调 ↑） | S ↓、TO ↓ | 平滑，可作旋钮（22/66/252） |
| **分组轴粗细** | F（单调 ↑） | S ↓ | 平滑，但 2Y 在 industry 取峰 |
| **平台 decay** | F（↑） | 2Y ↓、S ↓ | **悬崖型**，0→1 无效、1→2 断崖 |
| hump | — | 全指标 ↓ | **判死** |
| universe 降档 | — | 全指标 ↓ | **判死** |

**F 的解析式复核**（TO 已 < 0.125 地板？`ZYQZEawY` TO 18.58% > 12.5%，未触地板）：
`F = 1.64 × sqrt(0.0685 / 0.1858) = 1.64 × 0.607 = 0.996 ≈ 1.00` ✅ 公式成立。

**最优组合的逻辑**：industry 给出最高的 2Y 基线（1.73），decay 2 把它压到 1.64（仍在闸上），
同时把 F 从 0.93 抬到 1.00。**两者在 industry 轴上刚好同时落在闸上** —— 这是 sector 轴做不到的
（sector 2Y 基线 1.65，压完只剩 1.57）。

---

## 6. 下一步

1. **`ZYQZEawY` 测 prod**（唯一剩余闸），通过则提交 → RISK 塔 1/3。
2. 还需 2 颗 RISK 才能点塔。可复用本波结论的候选方向：
   - `LLMeGmJa`（sector s252 decay2）2Y 1.90 但 S 1.51 —— 需要 S +0.07 而 2Y 有 0.32 余量，
     可回退一个 decay 档（decay 1）或用 **s252 + industry + decay 2**（R1/R2 在飞）换更高的 S。
   - 点塔三颗之间的相关性约束：同数据集同字段，必须靠**窗口跨度**（66 vs 252 vs 22）
     与**变换**（rank vs zscore）拉开，不能只换分组轴。
3. 子域口径已定量（USA ratio 0.4346），后续候选预检前先算 `SUB / S`，<0.44 直接判该形状不可用。
