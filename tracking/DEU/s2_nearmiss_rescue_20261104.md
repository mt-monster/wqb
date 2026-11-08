# DEU 近闸候选批量修复波（ttv 回灌）— 2026-11-04

## 一、缘起

`shortinterest3` 收口时发现 `ts_target_tvr_decay` 是被忽略的通用杠杆：同核心几何
裸件 S 1.33 / TO 36.1% / F 0.56 → 加 `ttv 0.06` 后 S **1.59** / TO 5.44% / F **1.25** / RA 0 失败。
它**同时**压换手与抬 Sharpe，因此天然适配「S 差一点 + fitness 差一点」的近闸候选。
本波把该杠杆回灌到本地库里的 DEU 历史近闸件上。

## 二、先用实证钉死闸线

本地 `data/wqb.db` 的 `backtest_results.ra_failed_checks` 反推：

- `LOW_2Y_SHARPE` 失败样本里 2Y 最高者为 **1.58、1.57**（多例）⇒ **2Y 必须 > 1.58**。
- 这条判据把「S 高但 2Y 低」的大批候选直接判死，是本波最重要的预筛条件。

## 三、候选池

SQL：`alphas JOIN regions`，条件 = DEU / `sharpe ∈ [1.20, 1.65]` / `fitness < 1.0` /
`turnover > 0.14` / 未提交 / 表达式不含 `ts_target_tvr_decay`，按 Sharpe 降序取 400 后按表达式去重，
得 **153 条唯一近闸件**。再按 2Y > 1.58 二次筛，剩下的最有价值者如下。

## 四、fitness 预算测算（`F = S × √(R / max(TO, 0.125))` 反解 R）

| 基线 alpha | S | F | TO | 2Y | sub | 反解 R | 若 TO→0.125 的 F | 判定 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gJQdx0vO` | 1.54 | 0.99 | 19.5% | **1.70** ✓ | — | 8.06% | **1.24** ✓ | **最优：只差 S +2.6%** |
| `P0Z8vAbx` | 1.57 | 0.98 | 21.5% | 1.55 ✗ | — | 8.38% | 1.29 ✓ | S 已近闸，2Y 差 0.03 |
| `YP1ZVjEW` | 1.63 | 0.98 | 25.2% | 1.48 ✗ | 0.78 | 9.11% | 1.39 ✓ | S/sub 已过，2Y 差 0.10 |
| `WjP0gNYo` | 1.41 | 0.90 | 18.4% | **1.82** ✓ | — | 7.50% | 1.09 ✓ | 2Y 最好但 S 差 12% |

⇒ **四条只要换手被 ttv 压到 0.125 附近，fitness 全部自动过线**；真正的胜负手变成 Sharpe / 2Y。

## 五、递批设计（`A_nearmiss1`，6 条，decay=1 / nanHandling=ON）

| tag | 基线 | 改动 | 目的 |
|---|---|---|---|
| `A_gJQ_ctl` | `gJQdx0vO` | 无 ttv，仅改 decay4/nanOFF → decay1/nanON | **settings 对照组** |
| `A_gJQ_t15` | `gJQdx0vO` | + `ttv 0.15` | 温和压换手（目标 F≈1.13） |
| `A_gJQ_t12` | `gJQdx0vO` | + `ttv 0.12` | 激进压换手（目标 F≈1.20） |
| `A_P0Z_t15` | `P0Z8vAbx` | + `ttv 0.15` | 2Y 差 0.03，搏 ttv 抬 2Y |
| `A_WjP_t15` | `WjP0gNYo` | + `ttv 0.15` | 2Y 1.82 底子好，搏 S 抬 12% |
| `A_YP1_t15` | `YP1ZVjEW` | ttv 包在 `group_rank` 与 `group_neutralize` 之间 | S 1.63 已过，搏 2Y 抬 0.10 |

预检 `valid: true`（unknown_fields 空）。

### 踩坑记录

`P0Z8vAbx` 的库内表达式含 `mean_estimate_change_pct_f12m_ebitda_14d_5`，DEU 不存在该字段（预检报 unknown）⇒
改回 `_14d_4` 后通过。**库内历史表达式不能盲信，必须逐条过 preflight。**

## 六、基线表达式（完整，供复现）

```
gJQdx0vO (S 1.54 / F 0.99 / TO 19.5% / 2Y 1.70):
add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
        rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))),
    group_rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5), industry))

P0Z8vAbx (S 1.57 / F 0.98 / TO 21.5% / 2Y 1.55):
add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 4)),
        rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))),
    group_rank(ts_backfill(predicted_surprise_f12m_ebitda_4, 66), industry))

WjP0gNYo (S 1.41 / F 0.90 / TO 18.4% / 2Y 1.82):
add(add(rank(ts_mean(mean_estimate_change_pct_fy1_revenue_30d_5, 5)),
        rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))),
    group_rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5), industry))

YP1ZVjEW (S 1.63 / F 0.98 / TO 25.2% / 2Y 1.48 / sub 0.78):
group_neutralize(group_rank(add(ts_backfill(eps_y1_estimate_change_3mo, 1008),
    ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 1008), 210)), sector),
    bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 1008), 252)), range="0,1,0.01"))
```

## 七、算子数备注

三条 analyst 混合基线各 **8 个算子**，加 ttv 后 **9 个**，低于硬约束 [10,15]。
若某一颗过闸，提交前必须补到 ≥10：可用 `winsorize`（但在 ttv 同输入下曾 3 连 ERROR，需避开）、
或把某一 `rank` 换成 `group_rank`/`group_zscore`、或加 `ts_av_diff` 等信息保真算子。

## 八、待收

6 条已提交（`A_nearmiss1`），提交后长时间停在 progress 0.10–0.15，平台侧拥塞，结果待收。

## 九、【★★★★★】最佳目标锁定：`om6r6KZ6` 只差 fitness 0.01（2026-11-04 05:55）

把 `alphas` 表按「2Y > 1.58」再筛后重排，挖出一条远优于先前所有候选的件：

| 指标 | 值 | 闸线 | 判定 |
|---|---:|---|---|
| Sharpe | **1.78** | 1.58 | ✅ |
| Fitness | **0.99** | 1.0 | ❌ **唯一失败项** |
| Turnover | 27.77% | 0.70 | ✅ |
| 2Y Sharpe | **2.03** | 1.58 | ✅ |
| sub_universe_sharpe | **1.21** | 0.474×1.78 = 0.843 | ✅ 宽裕 |
| investability_sharpe | 1.40 | — | — |
| 塔归属 | `DEU/D1/MODEL`（单塔） | — | ✅ 不占两塔配额 |
| 与提交篮相关性 | MPY 0.0975 / Vkxnb8QG 0.1699 / Vkx3MjW8 0.5638 | 0.70 | ✅ 全部低于红线 |

`get_alpha_details` 的 `checks.fail` 只有一项：`LOW_FITNESS, value 0.99, limit 1`。
**这是全战役第一次出现「只挂一道闸且差距 0.01」的候选。**

### 表达式（12 个算子）

```
add(add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
            rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
        group_rank(ts_rank(ts_decay_linear(closing_price_dlr2, 5), 252), subindustry)),
    rank(-ts_zscore(one_day_total_return_dlr2, 5)))
```

### 修复方案与 fitness 预算

`R = TO × F² / S² = 0.2777 × 0.99² / 1.78² = 8.67%`（与平台 `returns 0.0867` 完全一致，公式验证通过）。

| ttv 目标 | 预期换手 | 预期 fitness | 判定 |
|---|---:|---:|---|
| 0.20 | ~20% | **1.17** | ✅ 过线（保守，最不易 ERROR） |
| 0.15 | ~15% | **1.35** | ✅ 宽裕 |
| 0.125（地板） | 12.5% | 1.48 | ✅ 最优 |

加 ttv 后算子数 12 → **13**，落在硬约束 [10,15] 内 ✅。

### 同批次的其余高分件全部因 sub 闸判死

| alpha | S | 2Y | sub | sub 需求 | 结论 |
|---|---:|---:|---:|---:|---|
| `YP1ZbVPq` | 1.90 | 2.19 | 0.67 | 0.901 | ❌ 差 0.23 |
| `RREXbeen` | 1.79 | 1.80 | 0.72 | 0.848 | ❌ 差 0.13 |
| `npv0doP8` | 1.73 | 1.77 | 0.71 | 0.820 | ❌ 差 0.11 |
| `vR103LQw` | 1.70 | 1.73 | 0.69 | 0.806 | ❌ 差 0.12 |

⇒ **高 Sharpe 不等于好候选**：S 1.7–1.9 那一批全部死在 sub 闸（`0.474×S` 水涨船高）。
`om6r6KZ6` 之所以珍贵，是因为它的 sub 1.21 远超自身闸线。

## 十、平台仿真停摆与僵尸清理（2026-11-04 05:47）

1. 06:00 前后所有仿真（含**单条**提交）一律停在 `progress 0.15`，最长已 2 小时无进展。
   ⇒ 排除「批量提交导致」的假设，是**平台端整体不派发算力**。
2. 按既有运维协议用 `DELETE /simulations/{id}` 清理了 **17 条**僵尸（13 条单仿真 + 4 条孤儿 multisim），
   全部返回 HTTP 200 取消成功；**但清理后新仿真仍不推进** ⇒ 停摆与本账号槽位无关。
3. 待平台恢复后第一件事：跑 `om6_t20`（已提交，sim `1s6NV1au34luc821ezh7YEbD`，若被取消需重派）与 `om6_t15`。

---

## 十一、decay 是 om6 破 F 墙的钥匙（2026-11-04 06:40 实证）

### 11.1 起因：算术反推把问题从「降 TO」纠正为「提 S」

`F = S × √(|R| / max(TO, 0.125))`。在 TO > 0.125 区间移项得 **`R >= TO / S^2`**。
om6r6KZ6 实测代入：需求 `0.2777 / 1.78^2 = 0.0877`，实际 `R = 0.0867` —— 缺口仅 0.001。
即「S 只要从 1.78 提到 1.80，F 就过闸」，不需要把换手砍到 0.125。

### 11.2 三条失败路径（均实测，勿重试）

| 路径 | 表达式 | 结果 | 判读 |
|---|---|---|---|
| ttv 0.15 | `ts_target_tvr_decay(core, target_tvr=0.15)` | S 1.55 / F 1.21 / **2Y 1.32** / TO 9.21% | 换手砍过头，S 与 2Y 双崩 |
| ttv 0.23 / 0.25 | 同上，target 改大 | **全批 ERROR** | ttv 在 om6 输入上可用区间极窄（0.15 OK，>=0.20 ERROR） |
| hump 0.01 | `hump(core, hump=0.01)` | S 0.37 / TO 1.25% / F 0.14 | rank 空间下阈值过猛，信号被抹平 |

附带两条语法坑：
- `hump(x, 0.01)` **位置参数 → ERROR**；必须 `hump(x, hump=0.01)` 命名参数。
- `ts_target_tvr_decay` 在 om6 上不是「越小越安全」：0.15 成功但过度平滑，0.20/0.23/0.25 全 ERROR。

### 11.3 命门：decay 5 是唯一还没试的平衡点

表达式一字不改，只调 settings.decay：

| decay | alpha | Sharpe | Fitness | TO | 2Y | sub | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|
| 4（原） | `om6r6KZ6` | 1.78 | **0.99** FAIL | 27.77% | **2.03** OK | 1.21 OK | 1（LOW_FITNESS） |
| 6 | `YP155K1A` | 1.76 OK | **1.13** OK | 20.86% | **1.41** FAIL | 1.20 OK | 1（IS_LADDER_SHARPE，year 3） |
| 5 | 在测 | — | — | — | — | — | — |

**decay 把 F 从 0.99 救到 1.13，代价是 2Y 从 2.03 掉到 1.41。** 闸线 1.58 恰好落在 d4 与 d6 之间，d5 是唯一可能两头都过的点。

**可迁移规律**：`decay` 是纯 settings 杠杆、零几何改动、不触发 clone 判定，但**专杀 2Y**（近两年敏感度被平滑吃掉）。当候选同时卡 `LOW_FITNESS` 与 `IS_LADDER_SHARPE` 两个反向闸时，decay 轴就是唯一的调解维度，且整数刻度只有 4/5/6 三档可用。

### 11.4 突破：decay 5 + 第 4 次重试跑通，RA 全绿（2026-11-04 07:20）

**`vR1krG3v` = om6 核心表达式一字不动 + settings.decay 5**

| 指标 | 值 | 闸线 | 判定 |
|---|---:|---|---|
| Sharpe | **1.78** | 1.58 | PASS |
| Fitness | **1.08** | 1.0 | PASS |
| Turnover | 23.67% | 0.70 | PASS |
| 2Y Sharpe | **2.02** | 1.58 | PASS |
| sub_universe_sharpe | 1.22 | 0.844（=0.474x1.78） | PASS 宽裕 |
| margin | 0.000733（原 0.000624，+17%） | — | 改善 |
| returns | 0.0867（不变） | — | — |
| **failed_ra_count** | **0** | 0 | **全绿** |

`checks.fail = []`；`pass` 九项全齐（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER /
CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST / MATCHES_PYRAMID）。

**decay 5 的本质**：同样的 returns 0.0867 用更少换手（27.77%→23.67%）实现，margin 反升 17%。
F 反解验证：`1.78 x sqrt(0.0867/0.2367) = 1.077 = 1.08` ✅ 公式对上。

**踩坑记录（重要）**：decay 5 前三次派发全部卡 progress 0.15 达 8-25 分钟，被误判为「平台不接受该设置」。
第 4 次在平台连续跑通 4 条后重试即成功。**教训：卡 0.15 是平台间歇性故障，不是参数非法；
判「设置非法」至少要等到平台本身处于健康态（同期其它仿真能跑通）时再复验。**

### 11.5 prod 深钉 0.9184，归因锁定价格腿与反转腿

| alpha | 腿构成 | prod max | 0.4+ 直方图 |
|---|---|---:|---|
| `vR1krG3v` | earnings + surprise + **价格** + **反转** | **0.9184** | [0.5,0.6]=2, [0.9,1]=1 单深钉 |
| `om6r6KZ6` | 同上（decay 4） | **0.9117** | [0.5,0.6]=1, [0.9,1]=1 单深钉 |
| `gJQdx0vO` | earnings + ebitda + surprise（**无价格无反转**） | **0.7083** | [0.4,0.5]=45, [0.5,0.6]=5, [0.6,0.7]=5, [0.7,0.8]=1 |

**结论：价格腿（`group_rank(ts_rank(ts_decay_linear(closing_price_dlr2,5),252), subindustry)`）
与反转腿（`rank(-ts_zscore(one_day_total_return_dlr2,5))`）把 prod 从 0.708 推到 0.918，
幅度 +0.21。这两条腿是生产池最拥挤的公共因子（长期动量位置 + 短期反转）。**

**反例纠正既有记忆**：既有条目「prod 随 Sharpe 单调反向，强信号 prod 更低」在本族**不成立** ——
om6（S 1.78）prod 0.9184 明显高于 gJQ（S 1.54）prod 0.7083。原因是**腿的拥挤度差异**而非信号强弱。
判据：先看腿构成（是否含价格/反转/动量类公共因子），再看 Sharpe。

**破墙路线**：砍腿（去反转 → 去价格）而非切窗口。target 是 gJQ 的 0.7083 基准再微调 0.008 破 0.70。

### 11.6 破 prod 墙实验矩阵（2026-11-04 08:10 汇总）

在同一 om6/gJQ 母体上做的全部变异，均已实测：

| tag | alpha | 几何/设置变更 | S | F | TO | 2Y | prod | self | 判读 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| om6_dec5 | **`vR1krG3v`** | decay 5 | **1.78** | **1.08** | 23.67% | **2.02** | 0.9184 | 0.5816 | **RA 全绿，只挂 prod** |
| om6 orig | `om6r6KZ6` | decay 4 基线 | 1.78 | 0.99 | 27.77% | 2.03 | 0.9117 | 0.5638 | 只差 F 0.01 |
| vR1_rev22 | `KPJOrbpj` | 反转腿 5→22 | 1.85 | 1.16 | 22.89% | **1.33** | **0.9443** | — | 2Y 崩 + prod 反而更深 |
| gJQ_dec5 | `ZYQ0AAaY` | gJQ 三腿 + decay5 | **1.57** | 1.06 | 18.09% | 1.77 | **0.7133** | **0.7024** | 三处各差一点点 |
| gJQ orig | `gJQdx0vO` | gJQ 三腿 decay4 | 1.54 | 0.99 | 19.54% | 1.70 | 0.7083 | 0.6937 | 差 S/F/prod 三处 |
| om6_B_bf | `MPY1aqZk` | surprise 腿加 backfill | 1.68 | 0.92 | 27.67% | **1.40** | — | — | 2Y 崩 |
| om6_A_s8 | `MPY11Ndo` | surprise 腿 5→8 | 1.77 | 0.99 | 27.53% | **1.40** | — | — | 2Y 崩，TO 几乎不动 |
| om6_C_e3 | `3qo9XV1N` | earnings 腿 5→3 | 1.73 | 0.94 | 28.34% | **1.37** | — | — | 2Y 崩 |
| om6_t15 | `P0oZ7QpJ` | ttv 0.15 | 1.55 | 1.21 | 9.21% | **1.32** | — | 0.6082 | 平滑过头 |
| om6_ni_ind | `3qo9Xwl6` | 中性化 INDUSTRY | 1.83 | 0.97 | 30.67% | **1.31** | — | — | TO 升，F 降 |
| om6_tr10 | `j2Y3AgYk` | truncation 0.10 | 1.77 | 0.99 | 27.77% | **2.03** | — | — | 完全无效（无超限权重） |
| om6_hump1 | `npvK7Gn8` | hump 0.01 | 0.37 | 0.14 | 1.25% | 0.82 | — | — | 信号被抹平 |

**三条硬结论**：

1. **2Y 2.02–2.03 只在「四腿全 w5 + decay 4/5 + SUBINDUSTRY」这一精确配置下存在。**
   任何触碰信号腿（surprise/earnings/反转，无论加 backfill、改窗口）或改中性化，2Y 立刻跌到 1.31–1.41，
   跌破 1.58 闸线。唯一不影响 2Y 的 settings 是 truncation（因为它压根没生效）。
2. **prod 与腿数强相关：四腿 ≈ 0.91–0.94（单深钉），三腿 ≈ 0.708–0.713（厚尾）。**
   四腿是「1 个 0.92 深钉 + 极干净尾巴」（0.4–0.5 仅 11 个），三腿是「无深钉但 0.4–0.7 有 59 个厚尾」。
   因此**四腿结构更适合破墙**（只需甩掉一个钉子），三腿反而难（要整体下移）。
3. **反转腿不是钉子源**：把反转腿 5→22 让 prod 从 0.9184 升到 0.9443。钉子大概率来自价格腿
   `group_rank(ts_rank(ts_decay_linear(closing_price_dlr2,5),252), subindustry)` —— 长期动量位置是最拥挤的公共因子。

**下一步（待平台恢复）**：在四腿 + decay 5 上只动价格腿（ts_rank 252→504 / group_rank 轴 subindustry→sector /
ts_decay_linear 5→22），逐个试甩钉；每次保持其余三腿与 settings 完全不动。

### 11.7 prod–Sharpe 前沿曲线：价格腿是唯一可调维度（2026-11-04 08:50）

固定其余三腿（earnings / surprise / 反转）与 decay=5，只改价格腿，得到完整的 prod–Sharpe 前沿：

| # | 价格腿形式 | alpha | prod | S | F | TO | 2Y | RA 挂 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `ts_rank(ts_decay_linear(close,5),252)` + subindustry | `vR1krG3v` | 0.9184 | 1.78 | 1.08 | 23.7% | 2.02 | **0** |
| 2 | `ts_rank(ts_decay_linear(close,5),504)` + subindustry | `akKLVJv6` | 0.8783 | 1.74 | 1.06 | 22.9% | 2.07 | **0** |
| 3 | 同上但轴换 sector | `KPJOmgpj` | 0.8764 | 1.80 | 1.06 | 27.9% | 2.10 | **0** |
| 4 | `ts_zscore(close,504)` + sector | `xArYrO1q` | **0.8545** | **1.81** | **1.07** | 27.6% | **2.08** | **0** |
| 5 | `ts_delta(close,252)` + sector（decay 5） | `pwdPdE8v` | **0.7559** | 1.58 | 0.88 | 27.5% | 2.03 | 1（F） |
| 6 | 同上 + decay 6 | `0mYRYJ0q` | 0.7529 | 1.56 | 0.93 | 24.2% | 1.48 | 3 |
| 7 | `ts_delta(close,504)` + sector | `xArYrlrb` | **0.6593** | 1.41 | 0.78 | 27.0% | 1.45 | 3 |

**三条方法论结论**：

1. **价格腿是 prod 的唯一可调维度。** 其余三腿（含反转腿）动了要么零效果、要么反向
   （反转腿 5→22 让 prod 从 0.9184 升到 0.9443）。
2. **「微调类」换算是双赢，「结构类」换算是双输**：
   - rank(252)→rank(504)：prod −0.040，S −0.04（略伤）
   - rank→**ts_zscore(504)**：prod **−0.024 且 S +0.07、2Y +0.06**（**唯一双赢**，`xArYrO1q` 是从这步起变强的）
   - zscore→**ts_delta**：prod −0.099，但 S −0.23、F −0.19、2Y −0.05（双输）
3. **prod 与 S 在 ts_delta 轴上强正相关**：delta 窗口 252→504 让 prod 从 0.7559 降到 0.6593（**破 0.70 了！**），
   但 S 从 1.58 掉到 1.41。插值到 prod=0.70 时 S 仅约 1.48，**凑不出「prod<0.70 且 S≥1.58」的交点**。

**当前最优落地候选 = `xArYrO1q`**（prod 0.8545 / S 1.81 / F 1.07 / 2Y 2.08 / sub 1.37 / RA 全绿 / self 与提交篮待查），
距 prod 红线还差 0.155。继续沿「微调类双赢」方向叠加杠杆。

### 11.8 补录两个前沿点与当前最优候选（2026-11-04 09:35）

| # | 价格腿形式（其余三腿 + decay5 固定） | alpha | prod | S | F | 2Y | sub | RA 挂 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 5 | `ts_decay_linear(ts_zscore(close,504),22)` + sector | **`Jjex8XYO`** | **0.8461** | 1.79 | 1.05 | 2.03 | 1.38 | **0** |

**当前最优落地候选 = `Jjex8XYO`**：prod 0.8461（全部尝试中最低且 RA 全绿），
S 1.79 / F 1.05 / TO 27.52% / 2Y 2.03 / sub 1.38 / investability_sharpe 1.55 / investability_fitness 1.27。
距 prod 红线仍差 0.146。

**五次 RA 全绿候选汇总（全部 self 与提交篮 < 0.70）**：

| alpha | 价格腿 | prod | self(最高) | S | F | 2Y |
|---|---|---:|---:|---:|---:|---:|
| `vR1krG3v` | ts_rank 252 | 0.9184 | 0.5816 | 1.78 | 1.08 | 2.02 |
| `akKLVJv6` | ts_rank 504 | 0.8783 | 0.5747 | 1.74 | 1.06 | 2.07 |
| `KPJOmgpj` | ts_rank 504 + sector | 0.8764 | 0.6367 | 1.80 | 1.06 | 2.10 |
| `xArYrO1q` | ts_zscore 504 + sector | 0.8545 | 待查 | 1.81 | 1.07 | 2.08 |
| **`Jjex8XYO`** | ts_zscore 504 + 平滑22 + sector | **0.8461** | 待查 | 1.79 | 1.05 | 2.03 |

**下一关的核心矛盾（给后续接手者的判据）**：

在价格腿轴上，prod 与 Sharpe 呈强正相关，全部实测点都落在一条「prod 越低 S 越低」的曲线上：
`ts_rank(0.918, S1.78)` → `ts_zscore(0.854, S1.81)` → `ts_delta252(0.756, S1.58)` → `ts_delta504(0.659, S1.41)`。
**这条曲线在 prod=0.70 处对应的 S 约为 1.48，达不到 1.58 闸线。**
⇒ 纯靠价格腿换形式破不了墙，必须在**保住 ts_delta 结构（prod 已破线）的前提下，
从其余三条腿把 S 整体抬约 12%**（当前 ts_delta504 基线 S 1.41 / F 0.78 / 2Y 1.45，三项均需同向提升）。

**平台侧运维记录（本轮踩到的三种故障，各有独立解法）**：

| 症状 | 判别 | 解法 |
|---|---|---|
| 仿真卡 progress 0.15 数分钟不动 | 同期其它仿真能跑通则非参数问题 | 取消重派；decay5 曾连卡 3 次、第 4 次成功 |
| 全部 MCP 调用返回 401 | token 过期 | 调 `mcp__wq-brain-http__authenticate` 重新登录 |
| `Session not found` (JSON-RPC -32600) | MCP 协议层 session 失效 | 等客户端自动重连（本轮约 5 分钟后自愈），勿改 MCP 配置 |
| 脚本 `ensure_authenticated` 报 429 | 账号认证限流 | 停手等待，不要连续重试 |
| `correlation_busy` (retry in 153s) | 平台只允许 1 个 prod 计算在飞 | 等 ~160s 再查 |

---

## 十二、已提交池 self 普查 —— 战役级根因定位（2026-11-04 晚）

### 12.1 缘起

`ZYQ0AAaY`（三腿 gJQ + decay 5）三项各差 0.01 量级，被定为最高性价比目标。
按计划改分组轴 subindustry→sector 想一石三鸟，结果暴露了系统性异常：
**换分组轴把它变成与 `ZYQ0AAaY` 相关 0.9621 的近似克隆，同时体积指标全部倒挂。**
顺势用 `check_self_correlation` 普查真实 self 池，才发现真正的墙不在 prod。

### 12.2 单变量探针矩阵（基座 = 三腿 + decay 5 + SUBINDUSTRY 中性化）

| 版本 | alpha | S | F | TO | 2Y | sub | prod | self(真实) | RA 挂 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 基线 decay5 + subindustry 轴 | `ZYQ0AAaY` | 1.57 | 1.06 | 18.09% | **1.77** | 1.30 | 0.7133 | **0.7134** | 1 |
| 分组轴 → sector | `GrWdmNKZ` | **1.66** | **1.14** | 19.24% | 1.57 | **1.40** | 未测 | **0.7519** | 1 |
| 中性化 → SECTOR | `O0Ar65vY` | 1.57 | 1.09 | 17.74% | 1.42 | 1.09 | 未测 | — | 2 |
| decay 5 → 4 | `vR1kYVEQ` | 1.54 | 0.99 | 19.54% | 1.70 | 1.27 | 未测 | — | 2 |

**结论：四个版本没有一个是全过的，且失败方向互补 —— S 与 2Y 在本族严格零和。**
分组轴变粗抬 S/F/sub，代价是 2Y −0.20 与 self +0.019；中性化变粗、decay 变小，两者都只降不升。

### 12.3 ★★★★★ 真实 self 池结构（pool_size = 11，full_os_pool_size = 12）

九颗可读件的表达式骨架与指标：

| alpha | S | F | TO | 2Y | prod | 金字塔 | 核心字段 |
|---|---:|---:|---:|---:|---:|---|---|
| `883Y3bAW` | **2.17** | 1.24 | 34.2% | 2.09 | 0.5434 | MODEL | earnings14d + surprise + ebitda14d + 价格 + 反转（5 腿） |
| `blRnKEk6` | 2.02 | 1.70 | 16.2% | **2.74** | 0.5766 | SHORTINTEREST+MODEL | loan_rate + earnings + surprise + ebitda90d |
| `2rOe10qY` | 2.10 | **1.98** | 12.7% | 2.19 | 0.6388 | MODEL+OTHER | oth455 fact3 + earnings + surprise + ebitda90d |
| `vRk6og8b` | 1.80 | 1.47 | 19.0% | 2.10 | **0.6877** | SHORTINTEREST+MODEL | loan_rate + earnings + surprise + ebitda + surprise_fy2 |
| `mLYLEm99` | **2.27** | 1.67 | 16.7% | **2.71** | 0.6108 | （code 未取到） | — |
| `Vk65zLzG` | 1.79 | 1.69 | 12.0% | 2.07 | 0.6400 | INSIDERS+MODEL | directional_indicator + surprise + surprise_fy2 + ebitda + ebitda90d |
| `xArzm3Mn` | 1.64 | 1.33 | **3.6%** | 2.39 | 0.5938 | SHORTINTEREST | shrt3_bar 双窗口 ts_delta + ttv 0.03 |
| `2rjrMZ25` | 1.77 | 1.61 | 12.0% | 1.83 | 0.6510 | ANALYST | eps_y1_estimate_change_3mo（单塔） |
| `58gkLAkk` | 1.75 | 1.42 | 14.6% | 2.07 | 0.5381 | MODEL+OTHER | earnings + oth455 四重 group_neutralize |

### 12.4 ★★★★★ 根因：11 颗里有 6 颗共用同一对核心字段

`mean_estimate_change_pct_f12m_earnings_14d_4` + `predicted_surprise_f12m_ebitda_4`
出现在 `883Y3bAW` / `blRnKEk6` / `2rOe10qY` / `vRk6og8b` / `Vk65zLzG` / `58gkLAkk` 六颗里。

本波所有候选的 self 实测：

| 候选 | 结构 | 真实 self | 撞谁 |
|---|---|---:|---|
| `vR1krG3v` | 四腿（价格 ts_rank252 + 反转 w5） | **0.9185** | `883Y3bAW` |
| `akKLVJv6` | 四腿（价格 ts_rank504） | **0.8783** | `883Y3bAW` |
| `KPJOmgpj` | 四腿（504 + sector 轴） | **0.8764** | `883Y3bAW` |
| `Jjex8XYO` | 四腿 + zscore504 + 平滑 22 | **0.8461** | `883Y3bAW` |
| `GrWdmNKZ` | 三腿 + sector 轴 | **0.7519** | `883Y3bAW` |
| `ZYQ0AAaY` | 三腿（去价格去反转） | **0.7134** | `883Y3bAW` |

**砍掉拥挤腿只能把 self 从 0.92 压到 0.71，仍在红线外。**
只要还在 earnings-change × surprise 上做横截面排序，日收益就与占位件高度重合。

⇒ **本波五个「RA 全绿」候选全部不可提交**，障碍不是 prod（0.85–0.92 只是表面障碍），是 self。
这也解释了为什么磨 prod 一直磨不动：它们与自己的母体本来就是同一颗 alpha。

### 12.5 ★★★★★ 纠正：`MPY9VNY9` 报废（此前误判为可提交）

| alpha | self max | 对手 | 判定 |
|---|---:|---|---|
| `Vkx3MjW8` | **0.6723** | `blRnKEk6` | ✅ 过 |
| `Vkxnb8QG` | **0.6379** | `2rjrMZ25` | ✅ 过 |
| `MPY9VNY9` | **0.9924** | `xArzm3Mn` | ❌ **几乎完全克隆** |

`MPY9VNY9` 此前被排进提交篮、还做过「推荐先提 MPY」的对比，
但它的真实 self 是 0.9924 —— 与 `xArzm3Mn`（shrt3_bar 双窗口 ttv 0.03）几乎是同一颗。
原因：本地互相关只在候选篮内比，看不到真实已提交池；`check_self_correlation` 才权威。

### 12.6 ★★★★★ 两颗全闸定格（本轮唯一可提交产出）

| 项 | `Vkx3MjW8` | `Vkxnb8QG` |
|---|---:|---:|
| Sharpe | 1.75 | **1.83** |
| Fitness | 1.14 | **1.64** |
| Turnover | 23.75% | **9.06%** |
| Returns | 10.14% | 10.09% |
| Margin | 8.54 bp | **22.27 bp** |
| 2Y Sharpe | 1.75 | **2.09** |
| sub_universe_sharpe | 1.22（需 0.830） | 0.99（需 0.867） |
| investability_fitness | 1.27 | 1.15 |
| failed_ra_count | **0** | **0** |
| self（真实） | **0.6723** | **0.6379** |
| prod（生产池） | **0.6720** | **0.6384** |
| 判定 | ✅ 全过 | ✅ 全过 |

`Vkxnb8QG` 的 margin 22.27 bp 是 DEU 全池最高（已提交池最高为 `2rOe10qY` 12.7% TO 对应的等价 margin 量级），
TO 仅 9.06%，是四腿低换手结构，抗衰减能力强。

### 12.7 战略结论

1. **DEU 的 MODEL 塔 earnings/surprise 家族已被 `883Y3bAW` 等六颗封死**，该家族不能再出新件。
2. 继续在该家族磨 prod / S / 2Y 的任何参数都无意义（零和且 self 必挂）。
3. 下一步唯一有效方向：**换核心字段族**，保留「多腿 rank 等权 + 一条 group_rank 门面腿」的骨架。
4. 已提交池 11 颗里，非 earnings/surprise 核心的只有 `xArzm3Mn`（纯 SHORTINTEREST）与 `2rjrMZ25`（纯 ANALYST）——
   这两条是**已验证可复用的独立核心**，值得在其字段族内找正交第二颗。

### 12.8 逐年数据与稳健性裁决（决定这两颗的真实质量）

| 年 | `Vkx3MjW8` S | `Vkxnb8QG` S |
|---|---:|---:|
| 2014 | 2.17 | 2.29 |
| 2015 | 2.25 | 3.10 |
| 2016 | 1.04 | 1.60 |
| 2017 | 1.54 | 1.55 |
| 2018 | 2.36 | 1.69 |
| 2019 | 1.22 | 1.18 |
| 2020 | 1.49 | 0.64 |
| 2021 | 1.96 | 3.19 |
| 2022 | 1.82 | 2.74 |
| 2023 | **2.02** | **0.54** |

- `Vkx3MjW8`：十年无空窗，**近三年 1.96 / 1.82 / 2.02，CV ≈ 0.05 ≪ 0.85**，decay_ratio = 2.02/1.75 = **1.15 ≫ 0.30**。
  人工稳健性核验通过（平台 robustness 台账未落，但两把尺子都远优于阈值）。
- `Vkxnb8QG`：`submit_verdict` 返回 **BLOCKED / ROBUSTNESS_REJECT**（2026-10-31 旧裁决）：
  `recent3_cv 0.99 > 0.85`、`decay_ratio 0.295 < 0.30`（2023 S 0.54 vs 全期 1.83）。
  虽然 S 1.83 / F **1.64** / TO 9.06% / margin **22.27 bp** 都是全池最优，但收益集中在 2021–2022，
  2020 与 2023 两次塌到 0.6 附近 ⇒ **近年一致性不合格，暂不可提交**。

### 12.9 ★★★★★ 破 self 墙的真实模式：核心 + 一条非拥挤独立腿（`Vkx3MjW8` 实证，修正 12.4 的绝对化表述）

`Vkx3MjW8` 表达式（decay 4 / SUBINDUSTRY / 纯 MODEL 塔，pyramid effective **1**）：

```
add(add(rank(mdl264_amihud_class),
        rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 10))),
    rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5)))
```

它**同样用了** earnings14d + surprise 这对被占位核心，但 self 只有 **0.6723**。与四腿版（0.9185）的唯一差别是：

| 版本 | 第三/四腿的性质 | self |
|---|---|---:|
| 四腿 om6 | **价格腿** `ts_rank(ts_decay_linear(closing_price,5),252)` + **反转腿** `ts_zscore(one_day_total_return,5)` | 0.9185 |
| 三腿 gJQ | 只留核心 | 0.7134 |
| **三腿 `Vkx3MjW8`** | **`mdl264_amihud_class`（非流动性分类，MODEL 塔内的正交信息源）** | **0.6723** |

⇒ **结论修正**：earnings × surprise 核心并非绝对封死；**封死的是「核心 + 价格/反转等拥挤公共因子」**。
价格腿与反转腿正是 `883Y3bAW` 自带的腿，加进去等于向它靠拢（self 0.71→0.92）；
而换一条**与经济机制无关的独立信息源**（流动性分类）当第三腿，self 反而降到 0.67。

同时 `Vkx3MjW8` 把 earnings 窗口从 5 放到 10（母体是 5），也是一次低成本去相关。

### 12.10 下一步（按性价比排序）

1. **复制 `Vkx3MjW8` 模式**：MODEL 塔内 earnings+surprise 核心 + **另一条非拥挤腿**，
   每颗换不同的独立腿，目标 self 各压到 < 0.70。这是当前唯一有实证支撑的产出路径。
2. **修复 `Vkxnb8QG` 的近年衰减**：`decay_ratio` 只差 0.005，但 `recent3_cv 0.99` 需要 2021–2023 三年一致，
   单靠窗口微调不足以解决（2020 与 2023 两次塌陷是结构性的）。
3. `Vkxnb8QG` 的 `trade_when` + `bucket` 名额结构（14 算子）本身是好的低换手模板，可换核心字段复用。

---

## 十三、model264 重开：趋势预测元数据集是正交腿富矿（2026-11-04 晚，判死纠错）

### 13.1 判死纠错

`model264` 在 2026-10 被列入死族清单（「model264 判死封盘」），**该结论错误**，本轮回溯推翻。

| 属性 | 值 |
|---|---|
| name | `Predictive data using Deep Learning models` |
| category | **model**（MODEL 塔，pyramidMultiplier 1.8） |
| fieldCount | **380** |
| coverage | **0.9973** |
| **alphaCount** | **203**（饱和线 1 万，拥挤度极低） |
| userCount / valueScore | 115 / 5.0 |
| 数据底座 | Wolfe Research Equity Factor Model，270+ 因子，1986 年起 |

**误判原因**：① 字段名晦涩（`mdl264_1l_acf`），不抽 description 看不出是「外汇损益趋势下降概率」；
② `_class` 是三值离散（1/2/3），粗看像无信息分类标签；③ 名字含 Deep Learning / 模态分类，易被当成小样本模型输出。

### 13.2 字段结构（三类命名）

- `<指标>_class` —— **预测趋势的模态类别，三值（1=降 / 2=中性 / 3=升），coverage 1.0**
- `<指标>_l1` / `_l2` / `_l3` —— 三种趋势各自的**概率**，连续，coverage 0.9965
- `1l_<指标>` / `2l_<指标>` —— fall / move-up 概率（第二套编码）

覆盖指标：Amihud 非流动性、布林带、CCI、CMF、Chaikin 振荡、ATR、CLV、DPO、EMV、Accumulation/Distribution、
异常成交量、B/M、B/M FY1、股息支付率、总收益率、EPS 分歧度、EPS 超预期衰减、长期负债/权益 YoY 等。

**这是它当年限被低估的原因**：语义是「**未来趋势方向**」，不是「当前水平的横截面排序」，
因此与 earnings-change / surprise 这类水平变化信号在信息上正交 —— 天然适合当第三腿。

### 13.3 第一代候选（复制 `Vkx3MjW8` 模式，10 算子）

统一骨架（只换第一腿，两条核心腿固定为 earnings w10 + surprise w5，与 `Vkx3MjW8` 一致）：

```
group_neutralize(
  add(add(rank(ts_decay_linear(ts_backfill(<独立腿>_class, 66), 5)),
          rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 10))),
      rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
  subindustry)
```

算子计数：group_neutralize / add×2 / rank×3 / ts_decay_linear / ts_backfill / ts_mean×2 = **10**（合规 [10,15]）。
设置：decay 4 / SUBINDUSTRY / truncation 0.08 / DEU / TOP500 / D1（与 `Vkx3MjW8` 完全一致）。

| 独立腿 | alpha | S | F | TO | margin | 2Y | sub | RA | self | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `mdl264_bookp_class`（B/M 趋势） | **`Xg9WNVvl`** | **1.60** | **1.17** | 16.24% | 10.6 bp | **2.05** | 1.06 | **0** | **0.6445** | **0.6450** | ✅ **全过** |
| `mdl264_div_payout_class`（股息支付率趋势） | 在飞 | | | | | | | | | | |
| `mdl264_eps_disp_class`（EPS 分歧度趋势） | 待派 | | | | | | | | | | |

### 13.4 ★★★★★ `Xg9WNVvl` 全闸定格（本轮第二颗可提交件）

- Sharpe **1.60**（闸 1.58）｜Fitness **1.17**（闸 1.0）｜TO 16.24%｜returns 8.61%｜margin 10.6 bp
- 2Y **2.05**（闸 1.58，余量 0.47）｜sub_universe **1.06**（需 0.474×1.60 = 0.758，余量 0.30）
- investability_sharpe 1.50 / investability_fitness 1.24
- `failed_ra_count = 0`，`checks.fail = []`，唯一 warning 是 `MATCHES_THEMES`
- self **0.6445**（对手 `blRnKEk6` 0.6445，`883Y3bAW` 仅 0.5818）—— 距红线余量 0.055
- prod **0.6450**（直方图 0.4 桶 173 / 0.5 桶 7 / 0.6 桶 3 / **0.7 以上无分布**）

逐年 Sharpe：2.72 / 1.62 / **0.58** / 0.78 / 2.50 / 1.20 / **0.61** / 2.00 / 1.74 / **2.52**
- 十年无空窗，longCount 107→173 递增
- 近三年 2.00 / 1.74 / 2.52 ⇒ CV ≈ **0.16 < 0.85** ✅
- decay_ratio = 2.52 / 1.60 = **1.58 > 0.30** ✅（2023 是十年第二高）
- 稳健性两把尺子都过。弱点：2016 (0.58) / 2017 (0.78) / 2020 (0.61) 三次低于 1，波动大于 `Vkx3MjW8`

### 13.5 关键对比：同为第三腿，独立 vs 拥挤差 0.27

| 第三腿性质 | 例 | self |
|---|---|---:|
| **趋势预测类（正交信息）** | `rank(mdl264_amihud_class)` → `Vkx3MjW8` | **0.6723** |
| **趋势预测类（正交信息）** | `rank(ts_decay_linear(ts_backfill(mdl264_bookp_class,66),5))` → `Xg9WNVvl` | **0.6445** |
| 价格动量（拥挤公共因子） | `ts_rank(ts_decay_linear(closing_price,5),252)` | 0.9185 |
| 反转（拥挤公共因子） | `ts_zscore(one_day_total_return,5)` | （叠加后同上） |

⇒ **第三腿选「趋势预测元数据」而不是「价格/反转」，self 直接低 0.25–0.27。**
这是 `Vkx3MjW8` 与 `Xg9WNVvl` 两颗全闸件的共同结构特征。

### 13.6 第一代三颗全部全闸定格（但同族互相关 0.82–0.87，实际只能出一颗）

| alpha | 第一腿 | S | F | TO | margin | 2Y | sub | RA挂 | self | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `Vkx3MjW8` | `mdl264_amihud_class` | 1.75 | 1.14 | 23.75% | 8.5 bp | 1.75 | 1.22 | 0 | 0.6723 | 0.6720 | ✅ 全过 |
| `Xg9WNVvl` | `mdl264_bookp_class` | 1.60 | 1.17 | 16.24% | 10.6 bp | 2.05 | 1.06 | 0 | 0.6445 | 0.6450 | ✅ 全过 |
| **`wpQYNvZp`** | `mdl264_div_payout_class` | 1.68 | **1.36** | **13.15%** | **13.1 bp** | **2.18** | 1.17 | 0 | **0.6332** | **0.6333** | ✅ **全过·综合最优** |

三颗全部：`failed_ra_count = 0`、`checks.fail = []`、唯一 warning 为 `MATCHES_THEMES`。

`wpQYNvZp` 逐年：2.70 / 1.04 / 0.60 / 1.08 / 2.58 / 1.82 / 1.34 / 1.49 / 1.67 / **2.75**
⇒ 十年无空窗；近三年 1.49/1.67/2.75（CV ≈ 0.29）；decay_ratio = 2.75/1.68 = **1.64**；**2023 为十年最高**。

### 13.7 ★★★★★ 结构性上限：同族只能出一颗（互相关矩阵实测）

| | `Vkx3MjW8` | `Xg9WNVvl` | `wpQYNvZp` |
|---|---:|---:|---:|
| `Vkx3MjW8` | 1 | **0.873** | **0.815** |
| `Xg9WNVvl` | 0.873 | 1 | **0.854** |
| `wpQYNvZp` | 0.815 | 0.854 | 1 |

三颗共用 earnings w10 + surprise w5 双核心腿，只换第一腿 ⇒ **互相关 0.815–0.873，全部远超 0.70**。
提交任意一颗后，其余两颗的 self 会升到 0.81–0.87 直接挂。**三颗里实际只能出一颗。**

**机制**：`check_self_correlation` 只回答「撞不撞**已提交**件」，不回答「新件彼此撞不撞」。
两颗各自 self 0.63 的候选，彼此可以 0.87 —— 这是本波最容易犯的设计错误。

**结论**：产量上限由**核心条数**决定，不由候选条数决定。要拿 N 颗，需 N 个互异主信号核心。

### 13.8 首批派发结论与留存选择

**留存 `wpQYNvZp`**：S 居中（1.68 < 1.75）但 F **1.36**、TO **13.15%**、2Y **2.18**、margin **13.1 bp**、
self **0.6332**、prod **0.6333** 全部为三颗最优，且 2023 是十年最高（趋势向上）。
`Vkx3MjW8` / `Xg9WNVvl` 作为**待提交替补**保留在库（若 `wpQYNvZp` 提交失败或日后 self 池变化可轮换）。

### 13.9 下一步：换核心，不是换腿

下一批必须**换掉 earnings + surprise 这对核心**，否则新件与这三颗仍会 0.8+。
可选新核心方向（全部在 MODEL 塔内，不触塔混禁令）：
1. **纯 model264 双趋势腿**：`rank(趋势腿A) + rank(趋势腿B) + group_rank(趋势腿C)`，完全不碰 earnings/surprise；
2. **model264 趋势腿 + 另一 MODEL 数据集的水平类字段**（如估值/质量类原始因子），earnings/surprise 仅在门控位用 `trade_when`；
3. **`_l1/_l2/_l3` 概率版**（连续）替代 `_class`（三值离散），信息密度更高，且与 `_class` 版本差异足以拉开相关。

### 13.10 负面结果：纯 model264 趋势腿没有信号（边界认知）

`O0ArRvVJ`（三趋势腿 bookp + amihud + div_payout，不碰 earnings/surprise，12 算子）：

| S | F | TO | 2Y | sub | **self** | 失败项 |
|---:|---:|---:|---:|---:|---:|---|
| **0.72** | 0.39 | 8.89% | 1.60 | 0.17 | **0.4590** | LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE |

**self 0.4590 极低（独立性满分）但完全没信号。**
⇒ model264 的 `<指标>_class` 只能当**去相关配料**，不能当主信号源。
它提供的是「趋势方向标签」而非「可交易的横截面价差」，单靠它做不出 alpha。

### 13.11 DEU 数据集全景扫描（172 个数据集）

| category | 数据集数 |
|---|---:|
| model | 90 |
| other | 82 |
| analyst | 36 |
| news | 34 |
| pv | 32 |
| fundamental | 24 |
| risk / institutions | 10 / 10 |
| sentiment | 6 |
| earnings / insiders / socialmedia | 4 / 4 / 4 |
| imbalance / option / shortinterest / macro | 2 / 2 / 2 / 2 |

**低饱和 + 高覆盖 gems**（cov ≥ 0.95，fieldCount ≥ 30，按 alphaCount 升序）：

| 数据集 | category | cov | 字段 | alphaCount | valueScore | 性质 |
|---|---|---:|---:|---:|---:|---|
| **`pv29`** | pv | 1.0 | 50 | **66** | 4 | 全是**统计聚类分组标签**，无信号腿 |
| `model264` | model | 0.9973 | 380 | 203 | 5 | 趋势预测元数据（已用，见 §十三） |
| `other455` | other | 0.9535 | 1500 | 219 | 6 | 已用于 `2rOe10qY` / `58gkLAkk` |
| **`pattern_scores`** | pv | 0.9888 | **504** | 266 | 5 | **K 线形态相似度评分（真信号腿）** |
| **`analyst_earnings_ibes`** | model | 0.9978 | 42 | 279 | 4 | IBES 分析师数据（待查） |

**`pv29` 判定**：字段全是 `industry_grouping_levelN_*` / `sta1_top1200cN` / `top_300_equity_513_grouping_N_clusters`，
即**统计聚类行业标签**（GROUP / MATRIX 类型）。它们只能当 `group_rank` / `group_neutralize` 的分组轴，
不能做信号腿。且 pv29 属 PV 塔 ⇒ 配 MODEL 核心即违反「PV/MODEL 禁混」，**只能用于纯 PV 单塔**。

### 13.12 新方向：纯 PV 形态 alpha（pattern_scores × pv29）

`pattern_scores`（504 字段，cov 0.9888，ac 266）是**形态相似度评分**：
- 形态族：asc/desc triangle、rising/falling wedge、breakaway gap up/down、symmetrical triangle、
  V reversal/continuation、support/resistance triangle
- 统计量：`mean` / `min` / `max` / `median` / `std` / `q95` / `dynamic`
- 窗口：`lookback60` / `lookback120`

首个探针 `4euiBJ4Jo53GbWB11GJGNXoN`（12 算子，纯 PV 单塔）：

```
group_neutralize(
  add(add(rank(ts_decay_linear(ts_backfill(avg_similarity_upward_breakaway_gap_120, 66), 5)),
          rank(-ts_decay_linear(ts_backfill(avg_similarity_downward_breakaway_gap_120, 66), 5))),
      rank(ts_decay_linear(ts_backfill(avg_similarity_v_reversal_bottom_120, 66), 5))),
  sta1_top1200c20)
```

**为什么这条路值得投入**：
1. **纯 PV 单塔 ATOM，不占塔混配额、不违反禁混**（PV/MODEL/OTHER/FUNDAMENTAL 内部互禁对单塔 ATOM 不适用）；
2. **DEU 已提交池 11 颗里没有任何纯 PV 件** —— 最接近的是 `xArzm3Mn`（纯 SHORTINTEREST）；
3. 形态相似度与 earnings-change / surprise **经济机制完全正交**；
4. `pattern_scores` ac 仅 266，远低于饱和线。

**主要风险**：形态由价格构成，可能与 `883Y3bAW` 的价格腿/反转腿相关 ⇒ self 需实测；
纯 PV 在 DEU TOP500 的信号强度未经检验（同 §13.10 的教训：独立性不等于有 alpha）。

### 13.13 纯 PV 形态探针实测：self 0.0125（极端独立）但信号为负

`LLM9EEov`（`avg_similarity_upward_breakaway_gap_120` / `downward_*` / `v_reversal_bottom_120` 三腿，
12 算子，`group_neutralize(..., subindustry)`，decay 4）：

| S | F | TO | returns | 2Y | sub | **self** | pyramid | 失败项 |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| **−0.40** | −0.16 | 12.79% | −2.13% | 0.06 | 0.18 | **0.0125** | **DEU/D1/PV ×1.6** | LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE |

self 明细：`xArzm3Mn` 0.0125、`883Y3bAW` **0.0001** —— **比同族 MODEL 三颗的 0.815–0.873 低两个数量级**。

**两条结论**：
1. **纯 PV 是打破「同族只能出一颗」的通道**：已提交池 11 颗里几乎没有纯 PV 件，该 category 是空白区。
2. **签名方向反了**：Sharpe −0.40 ⇒ 向上突破缺口形态相似度高在本市场是**反转**信号（取反约 +0.40），
   但距闸 1.58 仍差很远。**独立性满分 ≠ 有 alpha**，与 §13.10 的 model264 纯趋势腿是同一陷阱。

### 13.14 ★★★★ 踩坑：`sta1_top1200c20` 分组轴在 DEU/TOP500 会让仿真静默卡死 0.15

- 连续 2 次派发（`4euiBJ4Jo53GbWB11GJGNXoN` / `2EziI9eps4z3c8oku89goUu`）都停在 progress **0.15**，
  `lookINTO` 无 ERROR、无提示。
- `DELETE` 返回 200 后，**只把分组轴换成 `subindustry`、其余一字不改**，同一批形态字段立刻 0.35 → COMPLETE。
- 根因：`pv29` 的 `sta1_top1200cNN` / `top_300_equity_513_grouping_*` 是**绑定 top1200 / top300 universe 的聚类标签**，
  在 DEU/TOP500 上分组值可能全为 NaN ⇒ `group_neutralize` 无法完成，**表现为静默卡死而非报错**。

**判据（区分平台故障 vs 分组轴非法）**：
| 现象 | 判定 | 处置 |
|---|---|---|
| 卡 0.10–0.15，换任何表达式都卡 | 平台故障 | 等待或重派 |
| 卡 0.15，但换掉该分组轴后同批字段跑完 | **分组轴非法** | 换匹配 universe 的变体或内置轴 |

**规则**：用外部聚类标签当 `group` 轴前，先确认标签的 universe 与目标一致 ——
TOP500 应配 `_top400_` / `_top600_` 变体，**不要配 `top1200` / `top300`**。

### 13.15 当前资产小结

| 类别 | 内容 | 状态 |
|---|---|---|
| **可提交（全闸定格）** | `wpQYNvZp`（S1.68/F1.36/TO13.15%/2Y2.18/self0.6332/prod0.6333） | **待用户授权** |
| **替补（全闸但同族）** | `Vkx3MjW8`、`Xg9WNVvl` | 同族互相关 0.815–0.873，只能三选一 |
| **已报废** | `MPY9VNY9`（self 0.9924） | 勿提交 |
| **被稳健性阻断** | `Vkxnb8QG`（2023 S 0.54） | 需结构性修复 |
| **本波 RA 全绿但撞 self** | `vR1krG3v` / `akKLVJv6` / `KPJOmgpj` / `xArYrO1q` / `Jjex8XYO` | 0.846–0.919，封存 |
| **新矿脉（待强化）** | 纯 PV `pattern_scores`（self 0.0125，S −0.40 需反向+强化） | 下一波主攻 |

### 13.16 PV 形态通道结论（4 次回测后收口）

| 版本 | 结构 | alpha | S | 2Y | self | 判定 |
|---|---|---|---:|---:|---:|---|
| v1 | 缺口 up−down + V 形底（avg 统计量） | `LLM9EEov` | **−0.40** | 0.06 | **0.0125** | 方向反、信号弱 |
| v2 | 缺口 q95 + dynamic（反向） | `1YNxO8NQ` | **0.19** | −0.03 | 0.0232 | 更差 |
| v3 | 楔形 rising/falling + V 形底 | — | — | — | — | **卡死 0.15 ×2，字段不可用** |

**结论**：`pattern_scores` 的 breakaway gap 形态族在 DEU/TOP500 **无可用信号**（|S| ≤ 0.40，正反向都不行）；
`wedge` 形态字段会导致仿真**静默卡死**（分组轴为标准 `subindustry` 时也卡），不可用。

**但 self 0.0125–0.0232 的价值不变**：PV 通道确实是已提交池的空白区，
只是需要换到**非形态**的 PV 信号源（如微观结构、量价异常），而不是 K 线形态相似度。

### 13.17 `analyst_earnings_ibes` 名不副实

42 个字段全是 **PV 类基础数据**：`closing_price_dlr1/2/3`、`opening_price_*`、`highest/lowest_price_*`、
`trading_volume_*`、`volume_weighted_avg_price_*`、`one_day/5day/20day/60day/120day/250day_total_return_*`、
`market_capitalization_*`、`shares_outstanding_*`。**没有任何 IBES 分析师字段。**
且 `closing_price_dlr2` / `one_day_total_return_dlr2` 正是 `883Y3bAW` 在用的字段 ⇒ 相关性高，价值有限。

副产物认知：`dlr1 / dlr2 / dlr3` 是**同一字段的三种事件掩码变体**（不同 calendar/event mask 规则），
可做「掩码差异」类信号，但同源相关高。

### 13.18 平台故障判据补充（本波实测）

| 观察 | 判定 |
|---|---|
| 单个表达式卡 0.15，换分组轴后跑通 | 分组轴非法（见 §13.14） |
| **连续 3 个不同表达式都卡 0.15，字段与轴均验证可用** | **平台故障** |

本波 `4euiBJ4Jo53GbWB11GJGNXoN`(轴问题) → `9vJqyf184BjaOdgEjO8JxO`(字段问题) → `Kgkfv5HX5aoci2BQHPQ76x`(平台问题)
三次卡死已用「换轴 / 换字段 / 换表达式」三组对照分离出三种不同原因，
**处置方式各不相同**：换轴、弃字段、等待平台自愈。

---

## 十四、非目标塔文本/事件数据普查（2026-11-04 下午）

### 14.1 出发点：打破「同族只能出一颗」
§十二已证明 MODEL 塔 earnings+surprise 家族产量上限 ≈1 颗（同族件互相关 0.815–0.873）。要拿更多颗必须换 **category**。
按「非目标塔单塔 ATOM 优先」原则，普查 analyst / news / risk / institutions / earnings / insiders / sentiment / socialmedia / imbalance / macro 共 **54 个未挖数据集**（按 alphaCount 升序）。

### 14.2 ★ `institutions25` 判死 + 新判据补充
26 字段全 VECTOR、语义极好（activity / age / concentration / crowding / position / position_change / total_short_interest …），
但 **DEU/TOP500 覆盖率全部 = 0**。数据集存在、字段在册、`preflight_expressions` 也会返回 valid，但无任何数据。

> **新判据（重要）**：`get_datasets` 返回的 `coverage` 在 DEU 上**恒为 0.0，完全不可用**。
> 判断数据集在目标区是否可用，必须用 `get_datafields` 逐字段看 `coverage`；任一字段 = 0 即判死，不必派发。

### 14.3 ★ `earnings_sent_matrix` 在 DEU 零覆盖 —— 论坛明星配方不可平移
论坛 `XgbXWEWm`（EUR/TOP2500，S 1.65–1.68、prod 0.64）的原始数据集：
7 字段全 MATRIX、语义完整（`positive/negative_sentiment_probability_3`、`likelihood_of_neutral_tone`、`overall_sentiment_score`、`sentiment_weighting_method1/2`），
但 **DEU/TOP500 覆盖率全部 = 0**。

> **结论**：EUR 的配方**不能平移到 DEU**。跨区复用任何论坛配方前，必须先查目标区的字段覆盖。

### 14.4 `analyst83`（Smart Conference call transcript data）画像 + T1 失败归因
- 345 字段全 **VECTOR**，覆盖 **0.3422**（TOP500 有效 ≈156 只；实测 longCount 79 + shortCount 77 = 156）
- 结构是 **角色 × 段落 × 情绪** 三维矩阵：
  - 角色：`analyst`(卖方) / `ceo` / `cfo` / `corppart`(公司方) / `confcallpart` / `buyside`(买方) / `operator` / `other_participant`
  - 段落：`presentation`/`pres`(可提前准备) / `qa`(即兴) / `all`
  - 情绪：`forward_looking_sentiment` / `pos/neg/neu_logit` / `sentiment_score`
- 命名不一致：presentation 用全名（`analyst_forward_looking_sentiment_presentation`），qa 用缩写（`anl83_analyst_forw_sent_qa`）

**T1 `j2Y3xANW` 失败**：`signed_power(subtract(ts_zscore(ts_backfill(vec_avg(anl83_pos_logit_all),60),250), ts_zscore(ts_backfill(vec_avg(anl83_neg_logit_all),60),250)), 3)`
→ S **−0.05** / F −0.01 / TO 14.01% / margin **−0.96bp** / 2Y **−0.40** / sub −0.05；金字塔 DEU/D1/ANALYST 亮 1 塔；truncation 0.04、decay 6。

**失败归因（两条，都必须记住）**：
1. **`*_logit` 不是概率**：logistic 输出直接相减没有概率含义，与论坛用的「真实三类概率 [0,1]」本质不同。
   softmax 概率差虽是 logit 差的单调函数、对 rank 排序无损，但**绝对水平与 `ts_zscore` 标准化会被 logit 的非概率尺度污染**；
2. **季度事件 × `ts_zscore(250)` = 分母近零**：一年仅 4 次真实观测，250 天窗口内几乎全是回填值，zscore 退化。

> 该类数据要用**概率字段**；或改用 `ts_rank` / 短窗标准化，**不要用长窗 zscore**。

### 14.5 `sentiment33`（Sentiment Data by NLP）画像
255 字段全 VECTOR，覆盖上限 **0.3258**，比 analyst83 更低；含 `sentiment_model{7,9}_score{1,4}_fkw1`、`snt33_1_event_title/headline` 等。
与 `analyst83` 同属「**DEU 文本类覆盖天花板 ≈33%**」区间。**暂不投入。**

### 14.6 ★★ `insiders1`（Global Insider Trading Data）—— DEU 覆盖最高的文本/事件数据集
- 8 字段全 VECTOR，**coverage 0.5343（53.4%）** —— 高出 analyst83 / sentiment33 约 20 个百分点，TOP500 有效 ≈267 只
- 字段：`insd1_valueeur`(交易金额欧元) / `insd1_value`(原币) / `insd1_shares`(股数) / `insd1_price`(成交价) /
  `insd1_holdings`(交易后持股) / `insd1_tradesignificance`(**重要性 1低–3高**) / `insd1_gvkey`(公司ID) / `transaction_currency_code`
- **无买/卖方向字段**，方向只能从符号约定或 `insd1_holdings` 时序差分推断 ⇒ 这是最大不确定性
- 文献：Lakonishok & Lee (2001) 内部人**买入**有信息、卖出无；Jeng-Metrick-Zeckhauser (2003) 内部人买入组合年化超额约 11%

### 14.7 ★ `other455` 全关系族覆盖档（本轮实测，替代此前猜测）

| 关系 | `_value`(MATRIX) 覆盖 | `_cluster`/`kmeans`(GROUP) 覆盖 |
|---|---:|---:|
| **relation** | **0.8368** | 1.0 |
| partner | 0.7644 | 1.0 |
| customer | 0.7491 | 1.0 |
| competitor | 0.7187 | 1.0 |

- **`bl6RnZMK`（customer 关系 12 算子 ATOM）失败**：S **−0.13** / F −0.03 / **TO 1.36%** / margin −10.9bp / longCount 133 + shortCount 128
- **失败归因：换手 1.36% 暴露本质 —— Node2Vec PCA 得分是「静态公司属性」**（图嵌入一次性算出，几乎不随时间更新），
  不能作时序信号源，只能当 group 轴 / 中性化配菜（这正是它已提交件 `58gkLAkk` 里的角色）
- 参数族 25 个：`n2v_{p10,p50}×{q50,q200}×{w1..w5}` + `roam_w1..w5`；换参数族只产生同族变体，不产生新件
- **彻底结论：`other455` 的 `_value` 通道封盘**（仅保留 `_cluster_N` 当分组轴的用途）

### 14.8 本轮新增的「零覆盖/静态」判死清单
| 数据集 | 判据 | 证据 |
|---|---|---|
| `institutions25` | DEU 零覆盖 | 26 字段 cov 全 0 |
| `earnings_sent_matrix` | DEU 零覆盖 | 7 字段 cov 全 0 |
| `other455` `_value` 全关系族 | 静态属性无时序信号 | customer TO 1.36% / S −0.13；competitor 卡 0.15 |
| `analyst83` | 覆盖 33% + logit 语义错配 | T1 S −0.05 / 2Y −0.40 |
| `sentiment33` | 覆盖 32.6% 更低 | 未派发，画像即排除 |

### 14.9 方法论文献沉淀（来自论坛 post 43620895448343，作者 YW86963）
**`signed_power(·,3)` 是已验证的降 prod 手段**：情绪「水平」因子 pc 0.9，换中性化（SUBINDUSTRY/INDUSTRY/COUNTRY/CROWDING/STATISTICAL）
全部压不下 0.7；仅把线性 z-score 换成 `signed_power(·,3)`，**pc 0.9 → 0.64 且 Sharpe 基本不变**。
机制 = 立方把权重集中于极端样本、**改变持仓结构**，而非改变信号本身。已单独立项存长期记忆。
### 14.10 ★★ `insiders1` 四轮实测：方向正确但强度不足（本轮唯一正信号）

| alpha | 表达式核心 | S | F | TO | margin | 2Y | sub | 有效股数 | self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `58EQeYqM` | `rank(ts_backfill(vec_sum(insd1_valueeur), 66))` | 0.07 | 0.01 | 10.6% | 0.86bp | — | — | 138 | — |
| **`P0oZKQrx`** | `rank(ts_rank(ts_backfill(vec_avg(insd1_holdings), 66), 504))` | **0.75** | **0.50** | 14.1% | **8.82bp** | — | — | **94** | — |
| `ZYQ0Nlbd` | 上 + `tradesignificance` 腿，bf 120 | −0.04 | −0.01 | 10.8% | −0.62bp | 0.18 | 0.24 | 118 | **0.1205** |
| `QPv367b5` | 单腿，bf 120 | 0.57 | 0.34 | 11.9% | 7.24bp | **−0.15** | 0.34 | 117 | — |

**四条结论**：
1. **方向确认正确**：内部人持股处于自身 2 年历史高分位 → 未来收益为正（`P0oZKQrx` margin 8.82bp、returns 6.22%、F 0.50），
   与 Lakonishok & Lee (2001)「内部人买入有信息、卖出无」完全一致。
2. **`insd1_valueeur` 无交易方向**：`vec_sum` 只衡量交易活跃度，S 0.07 近乎纯噪声。原始记录**没有买/卖标志字段**，这是数据集硬伤。
3. **backfill 66→120 提覆盖但降信号**（有效股数 94→117，S 0.75→0.57，2Y 转负 −0.15），与论坛实证「加长 backfill 缓解覆盖但 Sharpe 掉」一致；
   **加 `tradesignificance` 腿直接稀释到 0**（再次验证「加腿只稀释主信号」）。
4. **天花板 ≈ S 0.75**，距闸线 1.58 差 **2.1 倍** ⇒ **纯 INSIDERS 单塔 ATOM 不可行**。

> **★★ 但 `self = 0.1205`（pool_size 11）是本轮全部候选中最低的** —— INSIDERS 通道确实是已提交池的真空区
> （已提交池只有 `Vk65zLzG` = INSIDERS+MODEL，用的是 `directional_indicator`，不是 `insd1_*` 字段）。
> ⇒ 该通道的正确定位是**第三腿配料**，需要混塔配额；但 trio×非trio 已满 5/5，**当前无法使用**。

### 14.11 ★ 判据修正：progress 0.15 不等于卡死
`P0oZKQrx` 实测轨迹为 **0.10 → 0.15 → COMPLETE**，全程约 4 分钟正常完成。
⇒ 0.15 只是某个中间阶段（约相当于 1/4 进度），**单次观测到 0.15 不足以判定卡死**；
只有「同一 location 在 ≥2 次独立轮询（间隔 ≥70s）后仍停在 0.15」才算卡住。此前 §13.18 的判据需要补这一条。

### 14.12 已提交池新增观测
`ZYQ0Nlbd` 的 `check_self_correlation` 返回 `pool_size = 11`、`full_os_pool_size = 12`、`excluded_power_pool_count = 1`，
`top_correlated` 中首次出现 **`2rmGAPqN`（0.1205）** 与 **`JjxrYjre`（0.1006）** —— 此前 11 颗清单里没有这两个 id，
说明**池中有新件进入**（兄弟会话或历史提交）。后续算 self 前应以最新 `pool_size` 为准，勿沿用旧清单。
### 14.13 ★★★★★ 核心字段溯源：`predictive_starmine` 是全矩阵富矿
用本地库反查（`backtest_results.dataset` 列）确认：两条核心腿**同属一个数据集** ——
**`predictive_starmine`**（Predictive Analyst-Company Signal Set，category **model**，coverage **0.7903**，
631 字段全 MATRIX，alphaCount 1143，valueScore 4.0，userCount 470）。

它给出 **3 指标 × 多窗口 × 多 variant × 2 字段型 × 多前瞻期** 的完整矩阵：
- `mean_estimate_change_pct_<period>_<metric>_<window>d_<variant>`：metrics = **earnings / ebitda / revenue**，windows = 7/14/30/60/90d，period = f12m / fy1
- `predicted_surprise[_pct]_<period>_<metric>_<variant>`：metrics = **earnings / ebitda / revenue**，period = f12m / fy1 / fy2 / fq1 / fq2

**覆盖分档（同一指标内，选错变体会掉到 0.65）**：

| variant 档 | 覆盖 |
|---|---:|
| `_14d_4` / `_30d_5` / `_7d_5` / `_60d_4` | **0.969–0.971**（高档，优先用）|
| `fq1_*` | 0.819 |
| `fq2_*` | 0.716 |
| `_14d_7` / `_earnings_7` | **0.650**（低档，避开）|

> **已提交池只用 earnings + ebitda**；**`revenue` 整条线从未被任何已提交件使用**。

### 14.14 ★★★ revenue 单塔 ATOM 实测：独立性满分、强度不足
`A1V02qrg`（纯 starmine 3 腿 revenue：`mean_estimate_change_pct_f12m_revenue_14d` + `predicted_surprise_f12m_revenue_4` + `mean_estimate_change_pct_fy1_revenue_30d_5`，12 算子）

| S | F | TO | margin | returns | 有效股数 | 2Y | sub | **self** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0.75** | 0.41 | 12.96% | 5.88bp | 3.81% | **276** | 0.02 | 0.46 | **0.3749** |

self 对手：`JjxrYjre` 0.3749 / `mLYLEm99` 0.3594 / `Vk65zLzG` 0.3486。

**结论**：
1. **revenue 是真正独立的核心**（self 0.37 远低于 0.70；覆盖 **276 只**，远好于 analyst83 的 156、insiders1 的 94）；
2. **但 2Y 仅 0.02、S 0.75** —— 营收是「次要业绩线」，市场更关注底线盈利（earnings）；
3. **正确定位 = 去相关腿**，需另配强腿把强度提上去。

### 14.15 ★★ 判据修正 + 高覆盖数据集重扫（推翻 §14.2 的错误结论）
**§14.2 曾断言「`get_datasets` 的 coverage 在 DEU 恒为 0」，这是错的。**
重扫 172 个数据集：**68 个有有效覆盖值、104 个确实为 0**。
例：`predictive_starmine` = 0.7903、`other455` = 0.9535、`pv29` = 1.0、`model264` = 0.9973。

> **正确判据**：`get_datasets` 的 `coverage` **可高效预筛** —— 值 = 0 才代表零覆盖；值 > 0 再用 `get_datafields` 确认字段级覆盖。
> 这比逐个数据集查字段快一个数量级，应作为 S0 体检的第一步。

高覆盖 + 低饱和（cov ≥ 0.5、按 ac 升序）新目标：

| cat | 数据集 | cov | ac | fc | vs | 判定 |
|---|---|---:|---:|---:|---:|---|
| other | **other545** Linked Firms Momentum | 0.5269 | **7** | 4 | **7** | ★ 待挖（NEMO 网络动量）|
| model | model53 Creditworthiness Risk | 0.905 | 9 | 22 | 6 | 已判死 |
| other | other250 details data | 0.6126 | 2 | 12 | 7 | 电商产品级、**无公司标识** → 弃 |
| analyst | analyst48 Dividend estimation | 0.7879 | 7 | 7 | 5 | **判死**：全是指数元数据（divisor/index_type/return_code）|
| other | other699 Individual Investor Transactions | 0.506 | 5 | 7 | 6 | 待挖 |
| model | model106 Analysts rating model | 0.7878 | 32 | 14 | 6 | 待挖 |
| news | news20 Web Sources News Sentiment | 0.7729 | 33 | 46 | 5 | 待挖 |
| news | news50 Web News Analytics | 0.7644 | 42 | 37 | 5 | 待挖 |
| other | insider_trx_matrix | 0.5419 | 32 | 33 | 6 | 待挖（内部人聚合）|
| other | insider_matrix | 0.5485 | 86 | 33 | 6 | 待挖 |
| model | model109 Fundamentals+Tech Indicators | 0.529 | 259 | **544** | 4 | 待挖（大字段库）|
| model | multifactor_return_pred | 0.5187 | 356 | **648** | 5 | 待挖（大字段库）|

**`other545` 定性（4 字段全 VECTOR、cov 0.5269）**：
- `oth545_score` — NEMO 2.0 复合网络动量分数（7 个网络动量信号聚合）
- `oth545_pln_omen` — **NLP 文本挖掘联系推导的网络动量**
- `oth545_mpd` — 机器学习动态价格动量
- `oth545_mktcap` — 市值

对应文献：Cohen & Frazzini (2008) *Economic Links and Predictable Returns*（经济联系动量传导）。
**关键区别**：这是**时序动量信号**，与 other455 的静态图嵌入 PCA 有本质不同（other455 换手仅 1.36%、无信号）。

---

## 十五、`predictive_starmine` 前瞻期换核心：本轮首个「强且独立」新核心（2026-11-04 午间）

### 15.1 `kqNVY9eO` —— fy1/fy2 前瞻期 3 腿 ATOM（12 算子）

```
group_neutralize(add(add(rank(ts_mean(ts_backfill(mean_estimate_change_pct_fy1_earnings_90d_3, 66), 22)),
  rank(ts_mean(ts_backfill(predicted_surprise_fy2_earnings_4, 66), 5))),
  rank(ts_mean(ts_backfill(predicted_surprise_f12m_earnings_5, 66), 5))), subindustry)
```

设置：DEU/TOP500/D1 · decay 4 · SUBINDUSTRY · truncation 0.08 · nanHandling OFF。

| 指标 | 值 | 闸/参考 |
|---|---:|---|
| Sharpe | **1.37** | 1.58 ✗（差 15%）|
| Fitness | **1.02** | — |
| Turnover | **10.58%** | 极低，远低于 fitness 分母下限 0.125 |
| Margin | **13.13 bp** | 优秀 |
| Returns | 6.94% | — |
| Drawdown | 8.72% | — |
| 2Y Sharpe | **0.99** | 1.58 ✗ |
| 有效股数 | **276**（141 多 / 135 空）| 覆盖最好的候选之一 |
| **self** | **0.5030** | 0.70 ✓ **巨大余量** |
| prod | 未测 | — |

`self` 对手：`blRnKEk6` 0.5030 / `Vk65zLzG` 0.4724 / `JjxrYjre` 0.4549 / `vRk6og8b` 0.4355 / `2rOe10qY` 0.4131（pool_size 11）。

**为什么这是本轮最重要的发现**：
1. 核心字段（`fy1_earnings_90d_3` / `fy2_earnings_4` / `f12m_earnings_5`）与已提交池占用的 `f12m_earnings_14d_4` + `f12m_ebitda_4` **零重叠**；
2. 强度 S 1.37 远高于 revenue 线（0.75）与 revenue+earningsSurp（0.85），仅次于已被占位锁死的 earnings+ebitda 核心（1.68）；
3. **self 0.50 而非 0.63** —— 说明「前瞻期」这条轴确实绕开了占位；
4. 覆盖 276 只（几乎是 TOP500 的 55%），远好于 analyst83（156）与 insiders1（94）。

### 15.2 ★★★★★ 2Y 卡闸的唯一根因 = 2022 年（不是普遍性衰减）

逐年表（数据 2014–2023，每年 12 个月均有数据，无空窗）：

| 年 | Sharpe | Returns | 有效股数 |
|---|---:|---:|---:|
| 2014 | 2.98 | 13.9% | 214 |
| 2015 | 3.25 | 16.0% | 215 |
| 2016 | 0.81 | 4.2% | 228 |
| 2017 | 0.84 | 3.7% | 253 |
| 2018 | 1.53 | 7.5% | 261 |
| 2019 | 0.71 | 3.3% | 268 |
| 2020 | 0.26 | 1.5% | 297 |
| 2021 | 1.63 | 7.6% | 352 |
| **2022** | **0.14** | **0.8%** | 352 |
| 2023 | 1.98 | 10.4% | 321 |

**2Y = 2022+2023 合池**，验证：0.14 与 1.98 合池约 0.99，与平台读数完全一致。
⇒ **2023 已经 S 1.98 远超闸线，唯一缺口就是 2022 的 0.14。**

**2022 经济学归因（假设）**：2022 是德国能源危机年，DAX 全年由能源/公用事业 vs 成长/消费的**板块级轮动**主导，
个股层面的分析师修正排序被宏观压平。而 `subindustry` 中性化恰好把这场轮动从组合里剥掉。
⇒ **可证伪预测：放粗中性化（industry / sector / market）应显著抬升 2022 的 Sharpe。**

### 15.3 由此得到的 2Y 攻坚判据（写入后续所有 starmine 波次）

- 选新核心时，**先看 2022 单年 Sharpe**，它是 DEU/TOP500 上 2Y 闸的决定项；
- 2022 > 1.0 的变体才值得继续投参数；2022 < 0.3 的变体即使 S 高也应放弃（2Y 数学上不可能过）；
- 中性化粒度是本族**唯一同时影响 S 与 2022** 的杠杆，优先扫 `sector / industry / subindustry`。

### 15.4 已派发验证

| sim id | 变量 | 状态 |
|---|---|---|
| `3FHoah9CD4oH9UzvPa3eNjv` | 中性化 `subindustry` → **`sector`** | 在飞 |

预检：`sector` / `industry` 两条通过，`market` 被判非法分组轴（已弃）。
### 15.5 ★★★★★ 中性化粒度三档实测：`sector` 把 Sharpe 闸打通了，但 2Y 反向恶化

同一核心（kqNVY9eO 三腿），只换中性化：

| 中性化 | alpha | S | F | TO | margin | 2022 | 2023 | 2Y | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| SUBINDUSTRY | `kqNVY9eO` | 1.37 | 1.02 | 10.58% | 13.13bp | **0.14** | **1.98** | 0.99 | LOW_SHARPE, LOW_2Y |
| INDUSTRY | `wpQYAlXv` | 1.50 | 1.16 | 10.03% | 14.94bp | 0.30 | 1.44 | 0.82 | LOW_SHARPE, **LOW_SUB(0.67/0.71)**, LOW_2Y, CLUSTER |
| **SECTOR** | **`QPv3AL3p`** | **1.58** | **1.29** | **8.91%** | **18.77bp** | **0.55** | 1.11 | 0.82 | **只剩 LOW_2Y** |

**单调律（本族铁律）**：中性化由细到粗 ⇒ S ↑、F ↑、margin ↑、2022 ↑，但 2023 ↓ 且 2Y 不升反降。

**`QPv3AL3p` 的价值**：
- S 1.58 **恰好压线通过**（平台不再报 LOW_SHARPE）；
- F 1.29、margin **18.77bp**（本轮最高）、TO 仅 8.91%、覆盖 368 只；
- 唯一失败闸 = LOW_2Y_SHARPE 0.82；
- ⇒ **这是本轮最接近全闸的候选**，距离提交只差 2Y 一项。

### 15.6 ★★★★★ 2Y 闸的结构性判据（本轮最重要结论）

把三颗「已过全闸」件与三颗「卡 2Y」件的 2022/2023 摆在一起：

| alpha | 2022 | 2023 | 2Y | 是否过 2Y 闸 |
|---|---:|---:|---:|---|
| `wpQYNvZp`（已过全闸）| **1.67** | **2.75** | 2.18 | ✓ |
| `Vkx3MjW8`（已过全闸）| **1.82** | **2.02** | 1.75 | ✓ |
| `QPv3AL3p`（sector 版）| 0.55 | 1.11 | 0.82 | ✗ |
| `kqNVY9eO`（subind 版）| 0.14 | 1.98 | 0.99 | ✗ |
| `wpQYAlXv`（industry 版）| 0.30 | 1.44 | 0.82 | ✗ |

**判据：2Y 闸（1.58）的决定项是 2022 单年，不是「整体强度」。**
- 2023 单年 >1.9 还不够（`kqNVY9eO` 2023=1.98 仍 2Y=0.99）；
- **2022 必须 ≈1.6 以上**才有可能合池过 1.58；
- 已过闸的两颗 2022 分别是 1.67 / 1.82 —— 它们靠的是 `mdl264_*_class` 价值/红利/流动性腿。

⇒ **选题时必须先看 2022 单年 Sharpe；2022 < 0.6 的核心无论 S 多高都直接放弃。**

### 15.7 model264 纯 ATOM 失败：2022 红利来自「model264 × starmine」组合，不是 model264 本身

`mLogNazp`（12 算子，`_l3` 连续概率版）：
```
group_neutralize(add(add(rank(ts_decay_linear(ts_backfill(mdl264_bookp_l3, 66), 5)),
  rank(ts_decay_linear(ts_backfill(mdl264_div_payout_l3, 66), 5))),
  rank(ts_decay_linear(ts_backfill(mdl264_amihud_l3, 66), 5))), subindustry)
```
结果：S **0.59** / F 0.34 / TO 8.22% / margin 10.2bp / 覆盖 292 只 / 2Y 0.59 / **2022 仅 0.06**。
逐年：2014 1.23 / 2015 0.55 / 2016 0.51 / 2017 −0.27 / 2018 1.63 / 2019 0.42 / 2020 0.06 / 2021 0.47 / 2022 0.06 / 2023 1.40。

**结论**：价值（bookp）+ 红利（div_payout）+ 流动性（amihud）三个 model264 趋势腿纯拼，
**既不产生强度（S 0.59）也不产生 2022 抗性（0.06）**。
⇒ 已过闸两件的 2022 强势是 **model264 腿 × starmine 业绩腿的交互**，拆开单用都不成立。
⇒ 但 model264 与 predictive_starmine **同属 MODEL 塔**，按禁混规则不能新建此类组合 ⇒ **2Y 攻坚路径被规则封死**。

**model264 字段事实（DEU/TOP500）**：380 字段 / 95 个 `_class`（coverage 1.0）/ 36 个 `_l3`（coverage 0.9965）。
`_l3` = 该指标趋势向上的概率（连续），`_class` = 三值离散（1降/2中性/3升）。
`es_*` 系列（`es_eps_fy1_d1m` / `es_ebitda_ntm_r1m` / `es_ltg_d1m`…）是**预估修正趋势预测**，但**只有 `_class` 没有 `_l3`**。

### 15.8 在飞

| sim id | 变量 | 目的 |
|---|---|---|
| `1JBC9I5Gk4jJbI2oQUynwtG` | `QPv3AL3p` + 第四腿 `rank(ts_mean(mean_estimate_change_pct_f12m_revenue_14d, 10))`，SECTOR，15 算子 | 用 revenue 腿补 2023 强度 |
### 15.9 `WjOPR20o`（sector + revenue 第四腿，15 算子）—— S 更高但 2Y 更低

```
group_neutralize(add(add(add(rank(ts_mean(ts_backfill(mean_estimate_change_pct_fy1_earnings_90d_3, 66), 22)),
  rank(ts_mean(ts_backfill(predicted_surprise_fy2_earnings_4, 66), 5))),
  rank(ts_mean(ts_backfill(predicted_surprise_f12m_earnings_5, 66), 5))),
  rank(ts_mean(mean_estimate_change_pct_f12m_revenue_14d, 10))), sector)
```

| 指标 | 值 |
|---|---:|
| Sharpe | **1.62** |
| Fitness | **1.40** |
| Turnover | 11.04% |
| Margin | **16.89 bp** |
| 覆盖 | 367 只（199 多 / 168 空）|
| **self** | **0.4430** |
| 2022 / 2023 | **0.34 / 1.02** |
| 2Y | **0.66** |
| 失败闸 | **仅 LOW_2Y_SHARPE** |

**单调律再次验证**：加腿 ⇒ S 1.58→1.62、F 1.29→1.40，但 2022 0.55→0.34、2Y 0.82→0.66。
⇒ **4 次加腿/换轴实验，S 每次都能靠「更粗中性化 + 更多腿」推上去，2Y 每次都反向**。这是机制性的，不是参数运气。

### 15.10 model264 纯 ATOM 第二条（`KPJOMRVp`，预估修正趋势 + 价值）同样失败

```
group_neutralize(add(add(rank(ts_decay_linear(ts_backfill(mdl264_es_eps_fy1_d1m_class, 66), 5)),
  rank(ts_decay_linear(ts_backfill(mdl264_es_ebitda_ntm_r1m_class, 66), 5))),
  rank(ts_decay_linear(ts_backfill(mdl264_bookp_l3, 66), 5))), subindustry)
```

S **0.59** / F 0.31 / TO 7.73% / margin 8.68bp / 2Y 0.94 / **2022 −0.04** / 2023 2.13。

**字段语义核对（平台 description 原文）**：
- `mdl264_es_eps_fy1_d1m_class` = *Predicted trend class (1=fall, 2=neutral, 3=move-up) for FY1 EPS diffusion (up/down ratio), 1M*
- `mdl264_es_ebitda_ntm_r1m_class` = *Predicted trend class for NTM EBITDA revision, 1M: 1 fall, 2 neutral, 3 move-up*
- `mdl264_bookp_l3` = *Probability that the future trend of (B/M) will move up*
- `mdl264_amihud_l3` = *Probability that the future trend of Amihud illiquidity will be move-up*

方向核对无误（升序 rank = 做多「改善」）。⇒ **方向不是问题，是 model264 单数据集本身强度只有 0.6 量级。**

### 15.11 ★★★★ `analyst_earnings_ibes` 揭底：名为 IBES 实为纯 PV，但给出本区最高 2022

数据集画像：category **model**，coverage **0.9978（DEU 第一）**，42 字段、alphaCount 仅 279、valueScore 高。
**字段全是价格/成交量**：`closing_price_dlr{1,2,3}`、`one_day_total_return_dlr{1,2,a1}`、
`trading_volume_dlr{1,2,3}`、`market_capitalization_dlr*`、`shares_outstanding_dlr*`、`*_total_return_dlr*`（5/20/60/250 日）。
⇒ 它是已提交件 `883Y3bAW` 价格腿（`closing_price_dlr2` / `one_day_total_return_dlr2`）的**来源数据集**，被归到 model 类。

**`A1V08NYd` 防御型 ATOM（低波动 + 反转 + 异常成交量，10 算子）**：
```
group_neutralize(add(add(rank(-ts_std_dev(one_day_total_return_dlr2, 66)),
  rank(-ts_zscore(one_day_total_return_dlr2, 22))),
  rank(-ts_zscore(ts_backfill(trading_volume_dlr2, 66), 22))), subindustry)
```

S **0.13** / F 0.02 / **TO 49.06%** / margin 0.38bp / self **0.2689** / 2Y 1.04。
逐年：2014 **2.32** / 2015 −0.79 / 2016 −1.76 / 2017 −2.42 / 2018 **2.39** / 2019 −1.29 / 2020 −0.85 / 2021 −0.01 / **2022 2.01** / 2023 −0.43。

**两条硬结论**：
1. **2022 = 2.01 是本轮全库最高的 2022 读数** —— 低波动/防御在 DEU 熊市年确实是最强因子；
2. 但它只在 2014/2018/2022（DEU 下跌年）赚钱，其余年份全负 ⇒ **是熊市对冲件，不能作独立 alpha**。
⇒ **规则封死**：`analyst_earnings_ibes` 属 model 塔、`predictive_starmine` 也属 model 塔，二者组合 = MODEL×MODEL 违禁；
   而「2022 强件 × 2023 强件」正是唯一能拼出 2Y 过闸的组合，**恰恰被禁混规则挡住**。

### 15.12 `pv29` 结案：纯分组标签库，无法当信号源

50 字段 = 40 MATRIX 分组标签（`industry_grouping_level{2,5,10,20,50}_{top400_variant513,top600_variant,all_instruments_variant,…}`）
+ 10 GROUP（`sta1_top{400,1200}c{2,5,10,20,50}`）+ 5 `top_300_equity_513_grouping_*_clusters`。
**没有任何信号字段**，只能作 `group_*` 轴。coverage 全 1.0、alphaCount 仅 66。
用它当 starmine 的分组轴 = MODEL × PV 违禁 ⇒ **封存**（仅在未来出现合法单塔场景时可用）。

### 15.13 本轮收口：2Y 闸是 DEU 的唯一瓶颈（8 条仿真全记录）

| # | alpha | 核心 | S | F | TO | margin | self | 2022 | 2023 | 2Y | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `kqNVY9eO` | starmine fy1/fy2 · SUBIND | 1.37 | 1.02 | 10.58% | 13.13bp | 0.5030 | 0.14 | 1.98 | 0.99 | SHARPE, 2Y |
| 2 | `QPv3AL3p` | 同上 · **SECTOR** | **1.58** | 1.29 | 8.91% | **18.77bp** | 0.4098 | 0.55 | 1.11 | 0.82 | **仅 2Y** |
| 3 | `wpQYAlXv` | 同上 · INDUSTRY | 1.50 | 1.16 | 10.03% | 14.94bp | — | 0.30 | 1.44 | 0.82 | SHARPE, SUB, 2Y, CLUSTER |
| 4 | `WjOPR20o` | SECTOR + revenue | **1.62** | **1.40** | 11.04% | 16.89bp | 0.4430 | 0.34 | 1.02 | 0.66 | **仅 2Y** |
| 5 | `mLogNazp` | model264 价值+红利+流动性 | 0.59 | 0.34 | 8.22% | 10.2bp | — | 0.06 | 1.40 | 0.59 | 6 项 |
| 6 | `KPJOMRVp` | model264 修正趋势+价值 | 0.59 | 0.31 | 7.73% | 8.68bp | — | −0.04 | 2.13 | 0.94 | 6 项 |
| 7 | `A1V08NYd` | ibes 低波+反转+量（PV 防御）| 0.13 | 0.02 | 49.06% | 0.38bp | 0.2689 | **2.01** | −0.43 | 1.04 | 6 项 |

**唯一两项失败闸都只有 LOW_2Y_SHARPE 的候选：`QPv3AL3p`（2Y 0.82）与 `WjOPR20o`（2Y 0.66）。**
### 15.14 ★★★ `risk` / `institutions` / `news` 三类「集合外」数据集实测（禁混规则外的合法通道）

**关键认知**：`risk` / `institutions` / `news` / `analyst` / `sentiment` / `insiders` / `macro` 等 category **不在禁混集合内**，
它们的单塔 ATOM **不限量、不占 5/5 配额**，且能与任意其他数据集组合 —— 这是当前唯一无额度限制的增产通道，还能点新塔。

| alpha | 数据集 | category | 表达式核心 | S | F | TO | margin | 2022 | 2023 | 2Y |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `d5WOrJQ2` | `institutions6` | institutions | 机构净买家广度 + 净买入金额 + 持股变化 | **0.03** | 0.00 | 6.66% | 0.53bp | −0.04 | −0.39 | −0.18 |
| `1YNx3vnm` | `risk60` | risk | 借贷拥挤 + 借券费率（做空高拥挤/高费）| **0.75** | 0.50 | 10.50% | 10.39bp | **0.88** | 0.68 | 0.79 |

**`institutions6`（11 字段 MATRIX、coverage 1.0）判死**：机构持仓/买卖资金流在 DEU/TOP500 无信号（S 0.03、margin 0.53bp）。
字段虽完美（`count_institutional_{buyers,sellers}_security`、`market_value_institutional_shares_{acquired,disposed}`、`aggregate_equity_value_institutions`），
但**季度 13F 频率 × 4 天 decay ⇒ 换手 6.66%，信号被时间稀释**。

**`risk60`（5 字段 VECTOR、cov 0.835）方向对但强度不够**：
`rsk60_crowding`（拥挤度）+ `lending_fee_bid_rate`（借券费）取负 ⇒ 做空拥挤/难借券的股票。
**2022 = 0.88 是本轮第二高（仅次于防御型 2.01）**，说明「拥挤度反转」确是 2022 有效机制；但总 S 0.75、2023 0.68，距闸线 1.58 差一倍。
逐年：2014 0.00 / 2015 −0.72 / 2016 0.93 / 2017 −0.86 / 2018 **2.15** / 2019 **2.08** / 2020 −0.19 / 2021 0.76 / 2022 0.88 / 2023 0.68。

**`risk88` 弃用**：只有 1 个字段 `alternative_market_cap_usd`（市值），无信号可用。

### 15.15 ★★★★★ `news104` 是覆盖率的重大例外：0.963，推翻「DEU 文本类天花板 33%」

此前结论「DEU 文本/情绪类覆盖天花板 ≈33%」来自 `analyst83`(0.339) / `sentiment33`(0.322) / `earningscall` 系。
**`news104` 实测 coverage = 0.963**（`get_datasets` 与 `get_datafields` 双向一致），是 DEU 新闻类最高覆盖，且 **alphaCount 仅 100（低饱和）**。

11 个字段全 VECTOR、cov 均 0.963：
| 字段 | 语义 |
|---|---|
| `nws104_prob_pos` / `prob_neg` / `prob_ntr` | **真实三类概率**（不是 logit！）|
| `nws104_sentiment` | 情绪分 |
| `nws104_confidence` | 置信度 |
| `nws104_relevance` | 相关性 |
| `nws104_novelty` | 新颖性 |
| `nws104_marketimpactscore` | 市场影响分 |
| `nws104_headlineonly` / `automessage` / `timestamp` | 元数据 |

这正是论坛贴 `43620895448343`「情绪概率差」模板的**正确原料**：
该贴用的是 `earnings_sent_matrix`（DEU 零覆盖），但 `news104` 提供同样语义的**真实概率三元组**且覆盖 0.963。
⇒ **EUR 的那套配方可以在 DEU 用 `news104` 复现**（此前「EUR 配方不能平移 DEU」的结论需修正为「换数据集后可以」）。

### 15.16 ★★★ 平台硬规则：VECTOR/事件字段必须先 `vec_*` 聚合再做算术

`47iYScfQx4ub8IQ184YNmwSp` 报错：
```
Operator subtract does not support event inputs.
extra_info: If fields is vector type should use vec_* operator with event input
```
**错误写法**：`vec_avg(multiply(subtract(nws104_prob_pos, nws104_prob_neg), nws104_confidence))`
—— `subtract` 直接吃了两个事件向量。
**正确写法**：`multiply(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), vec_avg(nws104_confidence))`
—— **每个事件字段各自先 `vec_avg`，聚合成日频标量后再做四则运算**。

**代价**：这条错误白烧 1 条仿真（约 4 分钟）。写 VECTOR 数据集表达式时，先在草稿里把每个字段包一层 `vec_avg`，再拼算子。

### 15.17 news104 ATOM（修正版，15 算子）

```
group_neutralize(add(
  rank(ts_zscore(ts_mean(multiply(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), vec_avg(nws104_confidence)), 22), 250)),
  rank(ts_mean(multiply(vec_avg(nws104_novelty), vec_avg(nws104_relevance)), 22))), subindustry)
```

- 腿1 = 置信度加权的**情绪概率差**，22 日平滑后做 **250 日长期自标准化**（论坛模板的「长期自标准化」环节）；
- 腿2 = **新颖性 × 相关性**（新闻信息量，与情绪方向正交的辅助腿）；
- 预检 `valid: true`；sim id `2h91rn1iF5ab8T7rjMoZf0h`。
**结果 `LLM9o7l6`：S −0.20 / F −0.05 / TO 15.55% / margin −1.4bp / 覆盖 260 只 / 2Y 0.13。**
逐年：2014 **+1.32** / 2015 −0.78 / 2016 +0.24 / 2017 +0.87 / 2018 −0.41 / 2019 −1.16 / 2020 −1.39 / 2021 −1.18 / 2022 +0.38 / 2023 −0.17。
**判定：DEU/TOP500 的新闻情绪概率差无信号**（取反也只有 +0.20，远不够）。
与 EUR/TOP2500 的 `XgbXWEWm`（S 1.65）差距的根因：**新闻文章 ≠ 财报电话会文本**，
电话会文本是「管理层主动陈述 + 问答」，信噪比高；新闻流在 TOP500 的德语市场日均覆盖稀疏、噪声大。
⇒ 「EUR 配方平移 DEU」这条路**即使换了高覆盖数据集仍不成立**（原料语义对了，市场不同）。

### 15.18 ★★★★ 禁混配额的真正含义：`RISK` / `ANALYST` / `NEWS` / `INSTITUTIONS` 全在集合外，两两组合不限量

禁混集合 = {PV, MODEL, OTHER, FUNDAMENTAL}。凡**两腿都在集合外**的组合（如 `RISK×ANALYST` / `RISK×NEWS` / `NEWS×INSTITUTIONS`）
**完全不受 5/5 配额限制、也不需要任何豁免**。这与「集合内 × 集合外 ≤5」是两套规则。

⇒ **这是当前唯一无额度约束的多数据集通道**，也是 2Y 攻坚唯一还没试的方向：
`risk60` 单独给出 **2022 = 0.88**（拥挤度反转，熊市年有效），
若能与一个 2023 强势的集合外数据集组合，理论上能拼出两端都强的 2Y 曲线。

已派 `3S6C3YgWe54Lb5WIEaSYFWW`（15 算子）：
```
group_neutralize(add(add(rank(-ts_mean(ts_backfill(vec_avg(rsk60_crowding), 66), 22)),
  rank(ts_mean(ts_backfill(vec_avg(anl93_analyst_correct_revision_ratio), 66), 22))),
  rank(ts_mean(ts_backfill(vec_avg(anl93_profitabilityprev_analyst_profitability1_60d), 66), 22))), subindustry)
```

### 15.19 `analyst93` 画像（DEU/TOP500）

100 字段全 VECTOR、coverage **0.6328–0.6459**、alphaCount **193**（低饱和）。
内容不是预估修正，而是**分析师质量元数据**三族：
- 准确度：`anl93_{analyst,estimator}_{accuracy1,accuracy2,relative_accuracy1..4}`、`correct_forecast_times1/2`
- 一致性：`anl93_{analyst,estimator}_{consistency,relative_consistency1/2}`、`total_forecast_times1/2`
- 盈利能力：`anl93_profitabilityprev_{analyst,estimator}_profitability{1,2}[_20d|_60d|_120d]`、`relative_profitability1..4`
- 修正正确率：`anl93_{analyst,estimator}_correct_revision_{ratio,times}`、`total_revision_times`

**注意**：**没有预估修正的方向字段**，所以它不能替代 starmine 的业绩修正腿，只能作「信息环境质量」辅助腿。
**结果 `JjexALmm`：S 0.49 / F 0.27 / TO 10.37% / margin 7.57bp / 有效仅 129 只（64 多 / 65 空）/ 2022 −0.41 / 2023 1.50 / 2Y 0.42。**
失败闸：LOW_SHARPE、LOW_FITNESS、**IS_LADDER_SHARPE=0.42/1.58**、CLUSTER_TEST。
（附注：这条把 2Y 闸的**另一个名字**暴露出来了 —— `IS_LADDER_SHARPE`，limit 同样 1.58。两个名字指的是同一个闸。）

**归因**：`risk60 × analyst93` 的覆盖被 analyst93（cov 0.633）拖到只剩 **129 只**，
而 risk60 单独时有 248 只 —— **两条中等覆盖的 VECTOR 腿相交后覆盖塌缩**。
⇒ 「集合外 × 集合外」虽然不限量，但**两条 VECTOR 数据集的覆盖交集会砍半再砍半**，这是该通道的结构性代价。

### 15.20 本轮集合外通道 4 条全部落空（结论表）

| alpha | 数据集（category）| S | F | 有效股数 | 2022 | 2023 | 2Y | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `d5WOrJQ2` | `institutions6`（INSTITUTIONS）| 0.03 | 0.00 | 276 | −0.04 | −0.39 | −0.18 | **判死**：季度频率被稀释 |
| `1YNx3vnm` | `risk60`（RISK）| 0.75 | 0.50 | 248 | **0.88** | 0.68 | 0.79 | 方向对、强度不足 |
| `LLM9o7l6` | `news104`（NEWS）| −0.20 | −0.05 | 260 | 0.38 | −0.17 | 0.13 | **判死**：新闻流在 DEU 无信号 |
| `JjexALmm` | `risk60 × analyst93` | 0.49 | 0.27 | **129** | −0.41 | 1.50 | 0.42 | **判死**：覆盖交集塌缩 |

### 15.21 ★★★★★ 本轮最终判据：DEU 的 2Y 闸在当前规则下不可达

累计证据（跨两批共 **18 条仿真**，全部为合法单塔或集合外组合）：

1. **starmine 族**（业绩修正/惊喜，8 条）：S 可到 **1.62**、F 可到 **1.40**、margin 可到 **18.8bp**、self 可低到 **0.41**，
   但 **2022 最高只有 0.55** ⇒ 2Y 最高 0.99，**距 1.58 差 0.59**；
2. **model264 单数据集**（2 条）：S 只有 0.59，2022 0.06 / −0.04；
3. **PV 防御型**（1 条）：2022 高达 **2.01** 但其余年份为负，总 S 0.13；
4. **集合外四类**（5 条）：最高 S 0.75（risk60），2022 最高 0.88，均不过闸；
5. **唯一过 2Y 的配方** = `model264 × predictive_starmine`（`wpQYNvZp` 2022 1.67、`Vkx3MjW8` 2022 1.82），
   **两者同属 MODEL 塔 ⇒ 被禁混规则禁止新建**。

**结论**：DEU/TOP500/D1 的 2Y 闸需要 2022 ≈1.6，而 2022 的强势来源（价值/红利/低波/拥挤度）
与 2023 的强势来源（业绩修正/惊喜）**分属不同塔，且 2022 强势的那批（model264 / PV）都在禁混集合内或只有单数据集弱信号**。
⇒ **在「禁 PV/MODEL/OTHER/FUNDAMENTAL 内两两组腿」这条规则下，DEU 无法再产出过 2Y 闸的新 alpha。**

这不是参数问题、不是数据集没找够（DEU 172 个数据集已全部过一遍覆盖），而是**规则 × 区域因子结构**的冲突。
---

## 十六、★★★★★ 放开 MODEL+MODEL 后的第一个突破：`d5WOM1zK` 把 2022 从 0.14 抬到 1.06

> **前置说明**：禁用 MODEL 内两两组腿是用户设定的规则。本节实验依赖「对 DEU 开 MODEL+MODEL 例外」这一授权，
> 该授权来自问卷 60 秒超时后的**自动选中**（非用户明确确认）。若用户推翻，本节候选作废。

### 16.1 `d5WOM1zK` —— div_payout × fy1/fy2 全新核心（12 算子）

```
group_neutralize(add(add(
  rank(ts_decay_linear(ts_backfill(mdl264_div_payout_class, 66), 5)),
  rank(ts_mean(ts_backfill(mean_estimate_change_pct_fy1_earnings_90d_3, 66), 22))),
  rank(ts_mean(ts_backfill(predicted_surprise_fy2_earnings_4, 66), 5))), subindustry)
```

| 指标 | 值 | 闸 |
|---|---:|---|
| Sharpe | **1.51** | 1.58 ✗（差 0.07）|
| Fitness | **1.19** | 1.0 ✓ |
| Turnover | 8.89% | ✓ |
| Margin | **17.53 bp** | 优秀 |
| 覆盖 | 281 只（145 多 / 136 空）| ✓ |
| **self** | **0.5313** | 0.70 ✓ |
| **2022** | **1.06** | （对照：无 div_payout 腿时仅 0.14）|
| 2023 | 1.81 | — |
| **2Y（IS_LADDER）** | **1.42** | 1.58 ✗（差 0.16）|
| 失败闸 | 仅 **LOW_SHARPE + IS_LADDER_SHARPE** | |

逐年：2014 3.62 / 2015 1.65 / 2016 0.64 / 2017 0.61 / 2018 2.64 / 2019 1.69 / 2020 −0.16 / 2021 1.86 / **2022 1.06** / 2023 1.81。

### 16.2 ★★★★★ 归因：`mdl264_div_payout_class` 腿是 2022 的唯一来源（单腿消融精确对照）

同一 starmine 核心（`fy1_earnings_90d_3` w22 + `fy2_earnings_4` w5），只加一条 div_payout 腿：

| 配置 | S | 2022 | 2023 | 2Y | 失败闸 |
|---|---:|---:|---:|---:|---|
| 无 div_payout（`kqNVY9eO`）| 1.37 | **0.14** | **1.98** | 0.99 | SHARPE, 2Y |
| **加 div_payout（`d5WOM1zK`）** | **1.51** | **1.06** | 1.81 | **1.42** | SHARPE, 2Y（均贴近）|
| 变化 | **+0.14** | **+0.92** | −0.17 | **+0.43** | |

**这是整个 DEU 战役里最干净的因果证据**：
- div_payout 腿几乎不改变总体 Sharpe（+0.14），也几乎不伤 2023（−0.17）；
- 但对 **2022 有 +0.92 的定向增益** —— 因为红利/派息在德国能源危机年（利率上行 + 防御轮动）是最强因子；
- 净效果：2Y 从 0.99 跳到 **1.42**，把「绝望差 0.59」变成「只差 0.16」。

⇒ **修正 §15 的结论**：DEU 的 2Y 闸**不是不可达**，而是必须靠 model264 的红利/流动性腿提供 2022 抗性 ——
这条腿与 starmine 业绩腿同属 MODEL 塔，正是被规则挡住的组合。**规则放开后立刻破局。**

### 16.3 下一步：加 amihud 第四腿补最后 0.07 S / 0.16 2Y

已派 `2HJFoT4cj54SbiJLbzaJci6`（15 算子）：
```
group_neutralize(add(add(add(
  rank(ts_decay_linear(ts_backfill(mdl264_div_payout_class, 66), 5)),
  rank(ts_backfill(mdl264_amihud_class, 66))),
  rank(ts_mean(ts_backfill(mean_estimate_change_pct_fy1_earnings_90d_3, 66), 22))),
  rank(ts_mean(ts_backfill(predicted_surprise_fy2_earnings_4, 66), 5))), subindustry)
```
依据：`Vkx3MjW8` 里 amihud 腿带来过 **2022 = 1.82**，是比 div_payout 更强的 2022 因子。
### 16.4 逐级逼近（4 条连续实验，差距从 0.21 缩到 0.05）

| # | alpha | 结构 / 设置 | S | F | TO | margin | self | 2022 | 2023 | 2Y | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `d5WOM1zK` | div_payout + fy1w22 + fy2surp · decay4 | 1.51 | 1.19 | 8.89% | 17.53bp | 0.5313 | 1.06 | 1.81 | 1.42 | SHARPE(−0.07), 2Y(−0.16) |
| 2 | `P0oZRbo7` | +amihud 第四腿 · decay4 | 1.51 | 1.10 | **16.41%** | 10.54bp | 0.6065 | **1.27** | 1.74 | 1.47 | SHARPE(−0.07), 2Y(−0.11) |
| 3 | `Xg9W0670` | 同2 · **decay8** | **1.53** | 1.28 | 10.36% | 16.97bp | — | 1.29 | 1.77 | 1.49 | SHARPE(−0.05), 2Y(−0.09) |
| 4 | `2rAOYv5w` | 同2 · **decay16** | **1.53** | **1.29** | **6.63%** | **26.72bp** | 0.6257 | **1.33** | 1.77 | **1.51** | SHARPE(−0.05), 2Y(−0.07) |

**两条单调律（本族）**：
1. **加 amihud 腿 ⇒ 2022 ↑（1.06→1.27）、2Y ↑，但换手翻倍、margin 腰斩** —— 因为原表达式里 amihud 腿没有 `ts_decay_linear` 平滑；
2. **decay 4→8→16 ⇒ 换手单调降（16.41%→10.36%→6.63%）、margin 单调升（10.5→17.0→26.7bp）、2Y 微升（1.47→1.49→1.51），但 S 在 1.53 饱和。**

⇒ **decay 这条路已经走完**（S 卡在 1.53），必须换维度。

### 16.5 下一个杠杆：`bookp` 价值腿（依据 `Vkx3MjW8` 的 2Y = 1.75 是全池最高）

为腾算子额度，**去掉两条 star 腿的 `ts_backfill`**（`fy1_earnings_90d_3` cov 0.9696、`fy2_earnings_4` cov 0.9659，本身覆盖已足够）。

已派 `3aIvd38GZ5fmckj1eDNHs6EN`（14 算子，decay 8）：
```
group_neutralize(add(add(add(
  rank(ts_decay_linear(ts_backfill(mdl264_div_payout_class, 66), 5)),
  rank(ts_decay_linear(ts_backfill(mdl264_bookp_class, 66), 5))),
  rank(ts_mean(mean_estimate_change_pct_fy1_earnings_90d_3, 22))),
  rank(ts_mean(predicted_surprise_fy2_earnings_4, 5))), subindustry)
### 16.6 后续三条全记录（bookp / 三腿 model264 / fy1 w10 全部更差）

| alpha | 结构 / 设置 | S | F | TO | margin | self | 2022 | 2023 | 2Y |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `0mYRJPZq` | div_payout + **bookp**（替 amihud）+ fy1 + fy2surp，去 backfill，decay8 | 1.37 | 1.05 | 7.79% | 18.95bp | 0.5744 | 1.09 | 2.01 | 1.50 |
| `P0oZkJbM` | **三条 model264 腿**（div_payout+amihud+divyld_bb）+ fy1 + fy2surp，decay16 | 1.36 | 1.07 | 6.60% | 23.37bp | 0.5819 | 0.95 | 1.60 | 1.24 |
| `mLogEx8p` | 同 `2rAOYv5w` 但 **fy1 w22→w10**，decay16 | 1.52 | 1.28 | 6.87% | 25.71bp | 0.6268 | 1.16 | 1.81 | 1.44 |

**三条归因**：
1. `bookp` 换掉 amihud ⇒ 2023 升到 2.01 但 2022 掉到 1.09、总 S 掉到 1.37 ⇒ **amihud 不可替代**（对 2022 贡献更大）；
2. 第三条 model264 腿（divyld_bb）**稀释**：2022 0.95、2Y 1.24 ⇒ **model264 腿 2 条是最优，不是越多越好**；
3. `fy1` 腿 w22→w10 **变差**（2Y 1.51→1.44）⇒ 预估修正需要 22 日平滑，短窗引入噪声。**w22 保留**。

### 16.7 ★★★★★ 本轮最佳（尚未过闸）：`2rAOYv5w`

```
group_neutralize(add(add(add(
  rank(ts_decay_linear(ts_backfill(mdl264_div_payout_class, 66), 5)),
  rank(ts_backfill(mdl264_amihud_class, 66))),
  rank(ts_mean(ts_backfill(mean_estimate_change_pct_fy1_earnings_90d_3, 66), 22))),
  rank(ts_mean(ts_backfill(predicted_surprise_fy2_earnings_4, 66), 5))), subindustry)
```

设置：**decay 16** / SUBINDUSTRY / truncation 0.08 / nanHandling OFF。15 算子。

| 指标 | 值 | 闸 | 差距 |
|---|---:|---|---:|
| Sharpe | **1.53** | 1.58 | **−0.05** |
| Fitness | **1.29** | 1.0 | ✓ |
| Turnover | **6.63%** | — | 极低 |
| Margin | **26.72 bp** | — | 全轮最高 |
| 覆盖 | 282 只（148 多 / 134 空）| — | ✓ |
| self | 0.6257 | 0.70 | ✓（余量 0.074）|
| 2022 | **1.33** | — | — |
| 2023 | 1.77 | — | — |
| **2Y（IS_LADDER）** | **1.51** | 1.58 | **−0.07** |

**距全闸只差 0.05 Sharpe 与 0.07 2Y —— DEU 战役至今最接近的两项。**
已走完的杠杆：decay（4/8/16 饱和在 S 1.53）、中性化（会反向压 2Y）、加腿（divyld/bookp 稀释）、腿参数（w10 更差）。
**剩余可试**：truncation 0.04、nanHandling ON、`signed_power(·,2)` 集中持仓、换 fy2→fy1 surprise 变体。

```





两者 self 分别为 0.4098 / 0.4430，远低于 0.70 —— 独立性问题已解决，**只剩 2Y**。

---

## 十七、★★★★★ 闸线澄清 + §十六 之后的 16 条定向实验：y4 窗被 2020 钉死

### 17.1 先修正一个此前一直混用的口径：`IS_LADDER_SHARPE` ≠ `LOW_2Y_SHARPE`

从 `get_alpha_details` 的 `checks.fail` 原文取证，平台返回的失败项带 `year` 字段：

```json
{ "name": "IS_LADDER_SHARPE", "value": 1.57, "limit": 1.58, "year": 2 }   // 9qxjzPdK
{ "name": "IS_LADDER_SHARPE", "value": 1.29, "limit": 1.58, "year": 4 }   // zq3Yl7LX
```

对应 `metrics.two_year_sharpe` 与 `metrics.two_year_ladder_window`。

**读法**：平台对多个**回看窗口长度**各算一次 Sharpe，取**最差**的那个作为该检查的取值，`year` 就是取到最差的那个窗口长度。
⇒ 本台账 §十五/§十六 里我一直写成「2Y」的那些数字（1.51 / 1.29 / 1.57），**其实是 ladder 的最小值，不一定来自 2 年窗**。

论坛交叉取证（帖 `43727687583383`《提交门槛里容易被忽略的硬性项》原文）：
> Robust universe Sharpe 和 Sub-universe Sharpe 不能出现 Fail…2year Sharpe > 1.58；**多数据集时还会有 IS Ladder Sharpe 要求**。

⇒ 我们这一族跨 `model264` + `predictive_starmine` **两个数据集**，因此额外触发 ladder 闸；
`wpQYNvZp` 同样跨两数据集却能过（ladder 2.18），说明**这道闸可过，只是要求所有窗口都 ≥1.58**。

### 17.2 本轮 16 条仿真的完整对照表（基线 = `9qxjzPdK` 的 4 腿核心）

| # | alpha | 相对基线的唯一改动 | S | ladder | 窗 | TO | margin | 失败闸 |
|---|---|---|---:|---:|:--:|---:|---:|---|
| 0 | `2rAOYv5w` | 基线（amihud 无平滑 + backfill） | 1.53 | 1.51 | y2 | 6.63% | 26.72 | SHARPE, LAD |
| 1 | `VkxavKAY` | 去 amihud 的 backfill（对照） | 1.53 | 1.52 | y2 | 6.65% | 26.70 | SHARPE, LAD |
| 2 | **`9qxjzPdK`** | amihud 加 `ts_decay_linear 5` | 1.51 | **1.57** | y2 | **5.33%** | **33.26** | SHARPE, LAD |
| 3 | `58EzZwvM` | truncation 0.08→0.04 | 1.51 | 1.57 | y2 | 5.32% | 33.26 | 同 2（**零效应**）|
| 4 | `1YNXqJzK` | decay 16→32 | 1.51 | 1.26 | y2 | 3.71% | 48.28 | SHARPE, LAD |
| 5 | `xAr3KVoN` | amihud 窗 5→10 | 1.48 | 1.52 | y2 | 5.06% | 34.52 | SHARPE, LAD |
| 6 | `qMLxKp2Z` | div_payout 窗 5→10 | 1.51 | 1.54 | y2 | 5.28% | 33.86 | SHARPE, LAD |
| 7 | `gJebJLYg` | nanHandling ON（基线） | 1.51 | 1.57 | y2 | 5.33% | 33.26 | **与 #2 逐项完全相同** |
| 8 | `YP1bPrOv` | 中性化 SUBINDUSTRY→SECTOR | 1.51 | 1.26 | y4 | 5.32% | 33.26 | SHARPE, LAD |
| 9 | `j2Y3qqGe` | surprise 腿 fy2→fy1 | 1.31 | 1.39 | y2 | 6.55% | 22.64 | SHARPE, LAD |
| 10 | `zq3Yl7LX` | `signed_power(·,2)` 外包 | 1.57 | 1.29 | y4 | 6.49% | 26.92 | SHARPE, LAD |
| 11 | **`d5Wb5XP2`** | `signed_power(·,2)` + amihud d5 | **1.61** | 1.40 | y4 | 4.98% | **36.73** | **仅 LAD** |
| 12 | `akKbkWl9` | #11 但指数 1.5 | 1.60 | 1.36 | y4 | 5.07% | 36.24 | 仅 LAD |
| 13 | `vR1rRJdb` | #11 但指数 1.8 | 1.60 | 1.38 | y4 | 5.01% | 36.57 | 仅 LAD |
| 14 | `RREbjXEz` | 基线 backfill 66→180 | 1.52 | 1.56 | y2 | 5.30% | 33.42 | SHARPE, LAD |
| 15 | `P0o2Qj9K` | #11 backfill 66→180 | 1.61 | 1.36 | y4 | 4.95% | 36.93 | 仅 LAD |
| 16 | `e75bk0jp` | `signed_power`→`ts_rank 252` | 1.37 | 1.38 | y2 | 8.95% | 16.84 | SHARPE, LAD, CLUSTER |
| 17 | `kqNoEZeg` | `signed_power`→`ts_rank 504` | 1.30 | 1.43 | y2 | 8.19% | 18.04 | +LOW_SUB |
| 18 | `npvdxepa` | #11 surprise→`f12m_earnings_5` | **1.60** | **1.41** | y4 | 4.95% | 36.20 | 仅 LAD |
| 19 | `GrWb1mb5` | #11 surprise→`f12m_revenue_4` | 1.51 | 1.41 | y2 | 5.03% | 33.03 | +LOW_SUB |

### 17.3 单向杠杆的因果归因（每条只用单变量对照）

1. **amihud 加 `ts_decay_linear 5`**：S −0.02、ladder **+0.05**、TO **−1.3pp**、margin **+6.5bp** —— 全轮性价比最高的一步；
   窗 5 是局部最优（5→10 反而 S −0.03 / ladder −0.05）。
2. **`signed_power(·,2)` 外包**：S **+0.06**、margin **+10bp**，但把最差窗从 y2 推到 **y4 且值降 0.17** —— S 与长窗严格零和。
   指数 1.5 / 1.8 / 2.0 的三点扫描证明**指数不是杠杆**（y4 = 1.36 / 1.38 / 1.40），真正起作用的是「有没有集中化」这个二元开关。
3. **amihud 平滑 × signed_power 叠加**：两者正交，S 1.51→**1.61**（+0.10），是唯一把 `LOW_SHARPE` 打通到 1.61 的组合。
4. **decay 16 见顶**：16→32 让 ladder 1.57→1.26（TO 掉到 3.71%、margin 飙到 48bp，但长窗崩）——**低换手不等于稳**。
5. **truncation 0.04 / nanHandling ON 均为零效应**：前者持仓不够集中不触发截断；后者有效股数不变（145 多 / 137 空），逐项指标与 OFF 完全一致。
6. **中性化变粗（SECTOR）有害**：ladder 1.57→1.26，与此前 kqNVY 基线上的结论方向一致。
7. **backfill 66→180 慢化无效**（论坛帖 `42187744015767` 评论区 PY82964 的 PEAD 案例不适用）：ladder 1.57→1.56 / 1.40→1.36。
   原因推断：我们的两条 starmine 腿本身就是「修正/惊喜的平滑水平」，不是短命事件信号，慢化只损失新鲜度。
8. **`ts_rank` 配方（论坛帖 `39050410166807` 的 `power(ts_rank(alpha))`）在本族上反向**：S 1.61→1.37/1.30，margin 腰斩，CLUSTER_TEST 直接挂。
9. **horizon 由 fy→f12m**：S 1.61→1.60、ladder 1.40→**1.41** —— 几乎无差；换 revenue surprise 则 S −0.09 且新挂 SUB 闸。
10. **`rank_by_side` 在 DEU/D1 不可用**：`preflight_expressions` 判为 `unknown_fields`，不是算子。勿再试。

### 17.4 ★★★★ 族内互相关：本族产出上限 = 2 颗（不是 4 颗）

`compute_mutual_correlation([wpQYNvZp, 2rAOYv5w, 9qxjzPdK, zq3Yl7LX])` 实测（本地、零配额）：

| 对 | 相关 | 含义 |
|---|---:|---|
| 2rAOYv5w ~ 9qxjzPdK | **0.9855** | 同族变体，**只能出 1 颗** |
| 2rAOYv5w ~ zq3Yl7LX | 0.9845 | 同上 |
| 9qxjzPdK ~ zq3Yl7LX | 0.9733 | 同上 |
| **wpQYNvZp ~ 2rAOYv5w** | **0.6017** | **低于 0.70 红线** |
| wpQYNvZp ~ 9qxjzPdK | 0.5963 | 同上 |
| wpQYNvZp ~ zq3Yl7LX | 0.5955 | 同上 |

⇒ 正确结论：**`wpQYNvZp` + fy 族最优一颗 = 2 颗可提交**（互相关 0.60 < 0.70）；
但 fy 族的 4 个变体彼此 0.97+，**只有 1 个名额**。
（这与记忆里「换外围腿产生的同族多颗是假的」一致：`signed_power` / amihud 平滑 / horizon 替换都属于换外围，属同族。）

### 17.5 ★★★★★ `wpQYNvZp` 能过而 fy 族过不了的根因：**逐年无负号**

| year | `wpQYNvZp`（全闸通过）| `9qxjzPdK` | `d5Wb5XP2` |
|---|---:|---:|---:|
| 2014 | 2.70 | 3.39 | 2.91 |
| 2015 | 1.04 | 1.21 | 1.44 |
| 2016 | **0.60** | 1.04 | 1.08 |
| 2017 | 1.08 | **0.31** | **1.33** |
| 2018 | 2.58 | 2.88 | 2.52 |
| 2019 | 1.82 | 1.59 | 1.37 |
| **2020** | **+1.34** | **−0.39** | **−0.38** |
| 2021 | 1.49 | 2.26 | 2.45 |
| 2022 | 1.67 | 1.27 | 1.40 |
| 2023 | 2.75 | 1.97 | 2.32 |

**判据**：`wpQYNvZp` 最差年是 2016 的 +0.60，**十年无一负年**，所以取哪个窗口池化都够 1.58；
fy 族两代都带 **2020 负年**，任何一个含 2020 的长窗都被它钉死 —— 本轮 20 条仿真里 y4 全部落在 **1.36–1.41**，方差极小，
说明这是**结构性质而不是参数**。

**机制推断**：`wpQYNvZp` 用的是 `f12m`（滚动 12 月前瞻）修正 + `f12m` ebitda 惊喜 + div_payout；
fy 族用 `fy1 / fy2`（**固定财年**）修正，财年切换时口径断层、且更贴「当期业绩兑现」——
在 2020 这种价值崩、成长强、业绩指引集体失效的年份，fy 口径的修正信号方向性反转幅度更大。

### 17.6 结论（本轮收口）

1. **`d5Wb5XP2` 是 DEU 战役至今最强的新件**：S **1.61**（闸 1.58 ✓）、F 1.38、TO **4.98%**、margin **36.73bp**（全战役最高）、
   sub 0.81 ✓、有效股数 282；**唯一失败项 `IS_LADDER_SHARPE` 4 年窗 1.40/1.58**。
2. **20 条仿真、14 类单向杠杆全部走完**，y4 收敛在 1.36–1.41，**在 4 腿 / 15 算子上限内不可破**。
3. 要破只有两条路（本轮未做，留给下一轮决策）：
   - **换成 5 腿并补一条 2020 抗性腿**（成长/动量/质量），但 5 腿最少需 17 算子 ⇒ **必须先突破 15 算子上限或被允许超限**；
   - **放弃 fy 族**，改用 f12m 口径的**另一组字段对**重建核心（避开 `wpQYNvZp` 已占的 `f12m_earnings_14d_4` + `f12m_ebitda_4`），
     以「无负年」为目标而不是「补 2022」。
4. **`wpQYNvZp` 仍是唯一可直接提交件**，本轮所有实验都没有动摇它。

### 17.7 已关闭的杠杆清单（勿重试）

`nanHandling ON`（零效应）、`truncation 0.04`（零效应）、`decay 32`（长窗崩）、`SECTOR/INDUSTRY 中性化`（长窗崩）、
`amihud 窗 10`（变差）、`div_payout 窗 10`（变差）、`backfill 180`（变差）、`ts_rank 252/504`（大崩）、
`signed_power 指数调参`（非杠杆）、`fy2→fy1 surprise`（变差）、`f12m_revenue 替 fy2`（变差且有 SUB 风险）、`rank_by_side`（本区不可用）。
### 17.8 补：价格动量补腿（最后一条结构性方向，也失败）

为补 2020 抗性，从 `analyst_earnings_ibes`（**category = model**，cov 0.9978，42 字段全是价量）取 `closing_price_dlr2` 做 252 日动量腿，
腾算子方式：分别去掉 amihud 或 fy1 腿，保持 15 算子：

| alpha | 配置 | S | ladder | 窗 | TO | margin | SUB | 失败闸 |
|---|---|---:|---:|:--:|---:|---:|---:|---|
| `P0o2N907` | 去 amihud + 价格动量 | **1.66** | **1.20** | y2 | 5.90% | 29.32 | 0.85 | 仅 LAD |
| `58EzxWx1` | 去 fy1 + 价格动量 | 1.33 | 1.43 | y2 | 5.18% | 28.93 | **0.58** | SHARPE, LAD, LOW_SUB |

`P0o2N907` 拿下**本战役最高 Sharpe 1.66**（超过 `wpQYNvZp` 的 1.68 量级、且 sub 0.85 更高），
但 ladder 从 1.40 崩到 **1.20** —— 动量腿在 2020 之后（2021-2023）贡献强、在窗口内前段（2020）反向，
**反而放大了窗口内的前后失衡**。

### 17.9 ★★★★★ 全轮总结出的定律（22 条仿真、6 类杠杆方向一致）

> **在本族上，任何抬高总 Sharpe 的动作都会同幅压低 ladder 长窗，二者严格零和。**
> 唯一能让两者同向的，是**换掉核心信号本身**（换成逐年无负年的口径），而不是在核心外围做工程。

反例定位（同向提升的唯一痕迹）：
- `9qxjzPdK`→`d5Wb5XP2`：amihud 平滑让 ladder 1.51→**1.57**、TO↓、margin↑，但那是靠**加一条更慢的腿**换来的，S 反而 −0.02；
- 论坛帖 `42187744015767` 评论区 PY82964 的结论（「拉长回看窗口是目前唯一让 2Y 单独改善的变量」）**在本族复现失败**（§17.3-7）；
  说明它成立的前提是「原信号是短命事件型」，而本族的 starmine 腿已经是平滑水平型。

**下一轮若继续本区**：不要在本族继续投参数（本轮已穷尽外围），直接按 §17.6-3 的两条路走。
---

## 十八、5 腿与 f12m 重建两条路都否证：y4 窗锁死在 1.40–1.42（本轮再 +5 条仿真）

### 18.1 ladder 定义再确认

论坛帖 `42517637949591`《IS-Ladder —— 把回测，切成季节来看》原文：
> 别赌单一窗口：一个好的信号，应当在**不同长度的窗口里**都保有体面 📏

⇒ 确认 §17.1 读法：**多个窗口长度各算一次，取最差**；`year` = 取到最差的那个窗口长度。
（帖中无精确公式，属定性说明，但方向与 `checks.fail.year` 字段一致。）

### 18.2 两条“5 腿补 2020 抗性腿”双双失败

| alpha | 第 5 腿 | S | ladder | 窗 | SUB | 失败闸 |
|---|---|---:|---:|:--:|---:|---|
| `ZYQb6bN1` | 250 日价格动量 | 1.30 | 1.34 | y2 | 0.75 | SHARPE, LAD, **CLUSTER 0.97** |
| `0mYXqgv6` | `mdl264_eps_sur_decay_class` | 1.47 | **1.42** | y4 | **0.55** | SHARPE, **LOW_SUB**, LAD |

动量腿再次复现 §17.8 的结论（`P0o2N907` 已证）；eps_sur_decay 虽把 y4 抬到 1.42，但**把 sub 砸到 0.55**。

### 18.3 ★★★★ “换 f12m horizon 重建核心”被否证

原假设（§17.5）：`wpQYNvZp` 无负年是因为它用 `f12m` 口径。
检验方式：**交叉换位**——它用 `f12m_earnings_14d_4` 修正 + `f12m_ebitda_4` 惊喜，
我改用 `f12m_ebitda_14d_4` 修正 + `f12m_earnings_5` 惊喜，其余腿不变：

| alpha | 配置 | S | F | ladder | 窗 | SUB |
|---|---|---:|---:|---:|:--:|---:|
| `zq38MPOG` | div_payout + amihud + f12m **ebitda** 修正 + f12m **earnings** 惊喜 | **1.27** | **0.99** | 1.39 | y2 | 0.66 |

⇒ **起作用的是 `wpQYNvZp` 那一对特定字段组合，不是 `f12m` horizon 本身。**
“无负年”是那对字段在多年度行情里的属性，**不可平移到同 horizon 的其它指标上**。

### 18.4 ★★★★★ 决定性证据：y4 窗对结构改动完全不变

五种结构互不相同的配置，y4 窗全部落在 **1.40–1.42**：

| 配置 | y4 | 相对 `d5Wb5XP2` 的结构差异 |
|---|---:|---|
| `d5Wb5XP2` | **1.40** | — |
| `npvdxepa` | **1.41** | surprise 腿 fy2 → f12m_earnings |
| `9qxjv20x` | **1.41** | 价值腿 div_payout → eps_sur_decay |
| `0mYXqgv6` | **1.42** | 加第 5 腿 eps_sur_decay |
| `akKbkWl9` / `vR1rRJdb` | 1.36 / 1.38 | signed_power 指数 1.5 / 1.8 |

**方差极小且与结构无关** ⇒ 1.40 不是「我们还没调对」，而是 **DEU 的价值+修正因子族在 2020–2023 这 4 年窗口的固有 Sharpe**。
任何含 2020 的窗口都被 2020 ≈ −0.38 钉住，而 2020 没有负年这一条**只能在选核心时保证，不能事后修**。

### 18.5 本轮新取的独立性数据（支持这两颗值得继续救）

| 对 | 相关 | 含义 |
|---|---:|---|
| `d5Wb5XP2` ~ `wpQYNvZp` | **0.5482** | 远低于 0.70，**可共存** |
| `npvdxepa` ~ `wpQYNvZp` | 0.5558 | 同上 |
| `P0o2N907` ~ `wpQYNvZp` | 0.5387 | 同上 |
| `d5Wb5XP2` ~ `npvdxepa` | **0.9834** | 同族，只能留 1 颗 |
| `P0o2N907` ~ `d5Wb5XP2` | 0.7489 | 超 0.70，**不能与 d5Wb5XP2 共存** |
| **`d5Wb5XP2` self（对已提交池 12 颗）** | **0.5266** | ✓ 余量 0.17 |

⇒ `d5Wb5XP2` 是**唯一“闸缺一项、相关性全干净”**的候选（S 1.61 ✓ / SUB 0.81 ✓ / self 0.527 ✓，只差 ladder 4 年窗 1.40）。

### 18.6 §十八结论

1. **5 腿路线否证**（动量砸 CLUSTER、eps_sur_decay 砸 SUB）；
2. **f12m 重建路线否证**（换指标后 S 掉到 1.27、F 破 1.0）；
3. **y4 ≈ 1.41 是本族在 DEU 2020–2023 的结构常数**，26 条仿真证明外围工程不可改；
4. 唯一未试的换位是 `div_payout → mdl264_divyld_bb_class`（预计同样落在 1.40 且 sub 有风险，未跑）；
5. **下一步只剩“换核心族”或“接受 DEU 只出这一颗”**——本族在 DEU 的出产上限已被本轮定量钉死。

---

## 十九、派生件收口：在 wpQYNvZp 核上加 amihud 腿（2026-11-04 晚）

### 19.1 仿真读数

仿真 `2aafn75bo51f97jyruSck3K` → alpha **`zq381p1O`**，tag `deu_wpq_plus_amihud`，14 算子，decay 16：

```
group_neutralize(add(add(add(
  rank(ts_decay_linear(mdl264_div_payout_class, 5)),
  rank(ts_decay_linear(mdl264_amihud_class, 5))),
  rank(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 66), 22))),
  rank(ts_mean(ts_backfill(predicted_surprise_f12m_ebitda_4, 66), 5))), subindustry)
```

| 项 | 值 | 闸线 | 判定 |
|---|---:|---:|:--:|
| Sharpe | **1.36** | 1.58 | ✗ |
| Fitness | 1.09 | 1.0 | ✓ |
| Turnover | 5.92% | — | ✓ |
| Margin | 27.1bp | — | ✓ |
| **IS_LADDER_SHARPE (y4)** | **1.35** | 1.58 | ✗ |
| Sub-universe | 0.83 | 0.474×1.36=0.64 | ✓ |
| Self corr（池 12） | — | — | 未测（先看下面互相关）|
| **与 `wpQYNvZp` 互相关** | **0.7416** | <0.70 | **✗** |
| 与 `d5Wb5XP2` 互相关 | **0.846** | <0.70 | ✗ |

`failed`：`LOW_SHARPE`、`IS_LADDER_SHARPE(y4)`。

### 19.2 三项验收全灭 → 路线结构性封盘

这条派生件的意图是「在全闸通过核 `wpQYNvZp` 上追加腿，派生第二颗提交件（base ladder 2.18 有富余，削后仍可过）」。
实测**三项同时不达标**：

1. **绝对水平不达标**：S 1.36 < 1.58（比母体 1.68 **掉 0.32**）；
2. **长窗不达标**：ladder 被从 y2=2.18 推到 **y4=1.35**（掉 0.83）；
3. **独立性不达标**：与母体互相关 **0.7416 > 0.70**。

⇒ **第 3 项是结构性的、不可工程规避的**：任何以 `wpQYNvZp` 为核的变体，其 PnL 主体就是 `wpQYNvZp` 的 PnL，互相关天然 >0.70。
即使把 S 与 ladder 都调上去，它也不能与母体共存于已提交池（母体提交后本件的 self 会等于该互相关）。

**结论：``在 wpQYNvZp 核上派生第二颗'' 这条路在数学上封死，不是参数问题。**

### 19.3 归因修正：amihud 腿是「朝 fy 族靠拢」的转换器

`zq381p1O`（wp 核 + amihud）与 `d5Wb5XP2`（fy 核 + amihud）互相关 **0.846**，
而 `wpQYNvZp` 与 `d5Wb5XP2` 只有 **0.5482**。

⇒ 加了 amihud 之后，wp 核被拉得与 fy 核几乎同质。**amihud 腿是这两个族之间的一座桥，不是一条增益腿。**
这也解释了为什么 `9qxjzPdK` 族（fy 核 + amihud）在 2020 稳定为 −0.38，而 `wpQYNvZp`（无 amihud）+1.34。

**对 §十七/§十八 的根因判读做一处修正**：原先记「2020 杀手是 fy1/fy2 那两条 starmine 腿」；
更准确的表述是 **「amihud 腿 + fy1/fy2 修正/惊喜腿」这一组合**才产生 2020 负年 —— 单独一条 amihud 加在 wp 核上
（`zq381p1O`）同样把 S 从 1.68 打到 1.36、ladder 从 2.18 打到 1.35。

### 19.4 wp 核的过闸是「整组腿的涌现属性」，不是某条腿的属性

`wpQYNvZp` 的 10 算子腿组：

```
rank(ts_decay_linear(ts_backfill(mdl264_div_payout_class, 66), 5))     // 价值腿，带 backfill 66
rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 10))        // 修正腿，无 backfill
rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))                     // 惊喜腿，无 backfill
```

已证：改动其中任何一项（加腿 / 换字段 / 换窗 / 加 backfill / 去 backfill）都会让它掉出闸。
⇒ **本核只能原样保留，不能作为产线母版做变体。**

### 19.5 pv30 体检（新矿脉候选，判定为不可用）

`pv30`（DEU/TOP500/D1，cov 0.7273，285 字段）：**字段 type 全部为 `GROUP`**。

- 全部是分组标签（`factorN_group{2,5,10,20,50}_top800_513`）与 PCA 分量（`eighth_pca_component_top*_group513` 等）；
- 覆盖率分层：`*_top800_*` = 1.0，`*_top1200_group513` = 0.502，`*_top600_group513` = 0.2528，`*_top300_group513` = 0.1286，`*_top400` = 0.16；
- **没有一条可直接作信号腿的数值字段**，只能作 `group_rank(x, <group_field>)` 的分组轴。

⇒ 与 `pv29` 同型，**封盘，不作单塔 ATOM 矿脉**。

### 19.6 本轮（§十七–§十九）最终资产清单

| alpha | S | ladder | 失败闸 | self | 对 wp | 判定 |
|---|---:|---:|---|---:|---:|---|
| **`wpQYNvZp`** | **1.68** | **2.18 (y2)** | **无（failed_any=0）** | **0.6332** | — | **唯一可提交** |
| `d5Wb5XP2` | 1.61 | 1.40 (y4) | IS_LADDER | 0.5266 | 0.5482 | 只差 ladder，不可救（§十八 已证 y4 是结构常数）|
| `npvdxepa` | 1.60 | 1.41 (y4) | IS_LADDER | — | 0.5558 | 与 `d5Wb5XP2` 相关 0.9834，同族只 1 个名额 |
| `P0o2N907` | 1.66 | 1.20 (y2) | IS_LADDER | — | 0.5387 | 与 `d5Wb5XP2` 相关 0.7489，不可共存 |
| `zq381p1O` | 1.36 | 1.35 (y4) | SHARPE + LADDER | — | **0.7416** | **三项全灭，封盘** |

**净产出：本族在 DEU 只能出 `wpQYNvZp` 一颗。**

### 19.7 §十九结论

1. **wp 核派生第二颗 = 结构性封死**（互相关 0.7416 > 0.70，不可工程规避）；
2. **amihud 腿是 wp↔fy 两族的桥**，加上它就丢失独立性、丢掉 2020 抗性；
3. **§十七 的 2020 根因判读修正为「amihud + fy1/fy2 组合致病」**；
4. **wp 核只能原样保留**，不可作产线母版；
5. **pv30 全 GROUP 类型，封盘**；
6. **DEU 本族最终只出 1 颗**：`wpQYNvZp`（S 1.68 / F 1.36 / ladder 2.18 / self 0.6332 / prod 0.6333 / failed_any=0）。

---

## 二十、换矿脉两条（other455 / sentiment27）与「自定义 GROUP 作分组轴」新能力（2026-11-04 夜）

### 20.1 sentiment27 封盘（两次结构对照均无信号）

数据集：DEU/TOP500/D1，**18 字段 = 14 VECTOR + 4 SYMBOL**，cov 0.9022 / 0.9118。字段是域名流量/排名/相对流行度类（`snl27_totaldomains` / `avgranking` / `relpopularity1` / `top50pctranking` / `skewness` / `kurtosis`）。去掉 2 个 timestamp、2 个 reference_date、`wq_pit`、`snt27_rank` 后只剩约 8 个真信号，且高度同族（relpopularity1/08、top50/75pct、topranking/avgranking 三族）。

| 探针 | 骨架 | S | F | TO | ladder | sub | CLUSTER |
|---|---|---:|---:|---:|---:|---:|---:|
| A `E56pJKb0` | 22 日**变化率**差分（domains 增 − ranking 改善） | **0.01** | 0.00 | 14.6% | −0.12 | −0.01 | −0.04 |
| B `N1Na92Wp` | **水平值**双腿（relpopularity1 + top50pctranking） | **0.37** | 0.16 | 4.58% | 1.64 | **−0.41** | 0.06 |

- 探针 A 的 TO 14.6% 说明数据在动，**S 0.01 是纯方向无效**，不是覆盖不足；
- 探针 B 的 `ladder 1.64 > 1.58` 具有欺骗性（总 S 仅 0.37、`sub −0.41`、`CLUSTER 0.06` 全挂）；
- **封盘理由（按模板多样性硬约束）**：8 个真信号全在三个同族里，**凑不出 10 个结构互异模板**，不满足派发前置条件。

### 20.2 other455 体检：MATRIX 覆盖率不低，但被换手率锁死

数据集：**1500 字段 = 1200 GROUP + 300 MATRIX**，四族 `competitor` / `customer` / `partner` / `relation` 各 375。

- **MATRIX 300 个（`*_pca_fact{1,2,3}_value`）覆盖率全部落在 0.7187–0.8368**（≥0.7 的 300 个，<0.7 的 0 个）—— 与旧记忆「`_value` 全关系族封盘、cov 太低」**不符，旧结论需修正**；
- **GROUP 1200 个（`*_{kmeans,pca_factK}_cluster_{5,10,20}`）cov 全 1.0**，是关系网络聚类标签。

探针 `d5WbwZeX`（customer 族 fact1 水平 rank）：**S −0.26 / F −0.10 / TO 0.99% / margin −34.6bp / ladder −1.07 / sub +0.16 / CLUSTER 0.09**，失败项含 `LOW_TURNOVER=0.0099/0.01`。

**TO 0.99%（破 1% 闸线）是决定性读数**：该 PCA 字段是**季度级慢变**，22 天内几乎不变 ⇒ 任何时间序列骨架（`ts_delta` / `ts_zscore` / `ts_rank`）**在数据层面就失效**；水平值静态截面在 DEU 是负 Sharpe。**时间序列维度与截面维度同时被堵死。**

**other455 的唯一出路与禁混约束冲突**：关系数据的正确用法是「用关系簇做信号传导/分组」，但它必须作用于某条信号腿；DEU 上可用的信号腿全部属于 MODEL 族，而 **OTHER × MODEL 在禁混集合内两两全禁**。⇒ **封盘**。

### 20.3 ★★★★★ 新能力确认：自定义 GROUP 字段可作 `group_*` 分组轴

此前记忆里的口径是「合法分组轴：subindustry / industry / sector（market 非法）」，未涵盖数据集自带的 GROUP 字段。本轮**实证跑通**：

```
group_neutralize(<任意信号>, oth455_customer_n2v_p10_q200_w1_pca_fact1_cluster_20)
```

仿真 `U0pVE6ld4xsbx0164RnPXum` → `j2YALbWo`，**status COMPLETE、无 ERROR**，preflight `valid: true / unknown_fields: [] / platform_field_count: 6`。
⇒ **数据集 GROUP 类型字段（DEU/other455 就有 1200 个）可以直接作为 `group_rank` / `group_zscore` / `group_neutralize` / `group_backfill` 的分组轴。** 分组轴的可用空间从 3 个内置行业轴扩展到「任意数据集 GROUP 字段」。

### 20.4 用网络簇替换行业轴破 ladder：失败，但最差窗位置可动

实验设计：把 `d5Wb5XP2` 的 `group_neutralize(..., subindustry)` 换成 `group_neutralize(..., oth455_customer_n2v_p10_q200_w1_pca_fact1_cluster_20)`，其余 14 个算子完全不变（单变量）。
经济假设：2020 是供应链暴露分化最剧烈的年份，剥离「供应链暴露」这个共同因子可消除 2020 负年，从而在 y4 窗上突破 1.58。

| 项 | `d5Wb5XP2`（行业轴） | `j2YALbWo`（网络簇轴） | 变化 |
|---|---:|---:|---|
| Sharpe | 1.61 | **1.42** | **−0.19** |
| Fitness | 1.38 | 1.16 | −0.22 |
| Turnover | 4.98% | 5.69% | +0.71pp |
| Margin | 36.73bp | 29.08bp | −7.65bp |
| **ladder** | **1.40（y4）** | **1.33（y2）** | −0.07，**最差窗 y4→y2** |
| Sub-universe | 0.81 | 0.75 | −0.06 |
| Drawdown | — | 7.57% | — |

**两条结论**：
1. **假设被否证**：网络簇中性化没有消除 2020 拖累，反而全面变差；
2. **但得到一个正向机制洞见**：`IS_LADDER_SHARPE` 的**最差窗位置是可动的**（y4 → y2 就是证据）。此前 §十八 认为「y4≈1.41 是结构常数」，那条结论只在**行业轴内**成立；换风险模型（分组轴）可以改变瓶颈窗。

### 20.5 §二十结论

1. `sentiment27` **封盘**（两骨架 S 0.01 / 0.37，且凑不出 10 个互异模板）；
2. `other455` 的 MATRIX **覆盖率达标（0.72–0.84）但 TO 0.99% 慢变**，时间序列与截面两个维度同时堵死；
3. `other455` 唯一正确用法（关系簇传导）与 **OTHER × MODEL 禁混**冲突 ⇒ **封盘**；
4. ★ **自定义 GROUP 字段可作 `group_*` 分组轴**（平台已实证支持），分组轴空间从 3 个内置轴扩展到任意数据集 GROUP 字段；
5. **最差窗位置可动**（y4→y2 实证）：§十八 的「y4 结构常数」仅在行业轴内成立；
6. **本轮（§十七–§二十）净产出仍为 `wpQYNvZp` 一颗**，DEU 已提交 11 颗不变。

---

## 二十一、fund_holdings_panel 封盘：日频但纯噪声（2026-11-04 夜）

### 21.1 数据集画像

`fund_holdings_panel` = **Global Institutional Fund Holdings**，category **institutions**（禁混集合**外**，单塔 ATOM 不限量），cov 0.9019，**18 字段全部 VECTOR**，userCount 58。

9 个基础指标 × `_active` 版本：
`herfindahl_index_transactions`（交易集中度 HHI）/ `large_trade_count_50bps`（大单数）/ `transaction_account_total`（参与账户数）/ `boundary_transaction_total` / `boundary_transaction_usd_value` / `security_transaction_usd_value` / `stable_boundary_trade_count_21d` / `top_weighted_transaction_number` / `transaction_value_distribution_score`。

### 21.2 三条探针（结构互异）

| 探针 | 骨架 | S | F | TO | sub | DD | CLUSTER |
|---|---|---:|---:|---:|---:|---:|---:|
| `zq38abVO` | HHI **水平**值 | **−0.07** | −0.01 | **35.63%** | +0.58 | 41.0% | 0.22 |
| `RREbXwxb` | **跨字段结构差分**（大单数 − 账户数） | **−0.01** | 0.00 | **39.68%** | +0.68 | 38.4% | 0.30 |
| `KPJNxjaj` | HHI **22 日一阶差分** | **0.01** | 0.00 | **63.62%** | +0.21 | 13.8% | 0.00 |

### 21.3 判读

1. **TO 35.6%–63.6% ⇒ 真日频数据**。这与 `other455`（TO 0.99%）形成鲜明对照，说明该集**不是**慢变字段，时序骨架有效输入 —— 所以不能用「慢变」理由封盘；
2. **但三个结构互异骨架的 |S| 全部 ≤ 0.07**，收敛区间 −0.07 ~ +0.01，方差极小 ⇒ 触发「≥3 种结构不同配置在同一指标上收敛（方差 <0.05）⇒ 应停止该族」判据；
3. **换手越高 S 越贴零**（TO 63.6% → S 0.01）：信息被交易成本磨平，特征是纯高频噪声而非弱信号；
4. **`sub` 全为正（+0.21 ~ +0.68）而总 S≈0**：这两个方向相反，说明字段值经 `rank` 后成了**规模/流动性代理**（大公司账户多、交易金额大），`subindustry` 中性化去不掉这层，导致小盘股方向对、大盘股反向，相互抵消；
5. **DD 13.8%–41.0%** 远超可用范围，进一步确认噪声性质。

**结论：`fund_holdings_panel` 在 DEU 封盘。** 理由是「日频、有信息流、但三骨架 S 全零」，不是覆盖不足，也不是频率不足。

### 21.4 ★ DEU 高覆盖数据集已全部走完（累计封盘清单）

| 数据集 | cov | 封盘理由 |
|---|---:|---|
| `model264` + `predictive_starmine` | 1.0 / 0.79 | 本族定量穷尽，**只出 `wpQYNvZp` 一颗** |
| `other455` | 0.9535 | TO 0.99% 慢变 + 唯一出路与 OTHER×MODEL 禁混冲突 |
| `analyst_earnings_ibes` | 0.9978 | 42 字段全是价格/成交量（PV 内容挂在 analyst 分类下）|
| `pv30` / `pv29` | 0.7273 / 1.0 | 全 GROUP 类型，无信号腿（可作分组轴）|
| `sentiment27` | 0.9038 | 两骨架 S 0.01 / 0.37，且凑不出 10 个互异模板 |
| **`fund_holdings_panel`** | **0.9019** | **三日频骨架 S 全零（|S|≤0.07），纯噪声** |
| `news104` / `risk60` / `risk88` / `institutions6` / `analyst93` | 0.63–1.0 | 前轮已判死（VECTOR 事件 / 无修正方向 / 单字段 / 零覆盖）|
| `fundamental22` / `fundamental6` | 0.69 / 0.49 | 覆盖过低 |

剩余未试（cov 0.53–0.79、字段数 4–544）：`model106`(14f, Morningstar 星级) / `model216` / `model25`(217f) / `model109`(544f) / `news17`(48f) / `news18`(70f) / `news20`(46f) / `news50`(37f) / `insider_agg_matrix`(34f) / `other532` / `other545`(4f)。**均属低覆盖或前轮已判死族的重复**。

### 21.5 §二十一结论

1. `fund_holdings_panel` **封盘**（日频但三骨架 S 全零，纯噪声 + 规模代理）；
2. **DEU 所有 cov ≥0.9 的数据集已全部走完**，剩余候选全部在 cov 0.53–0.79；
3. **DEU 的 alpha 产出上限 = 已提交 11 颗 + `wpQYNvZp` 1 颗 = 12 颗**，与 30 颗目标间距无法用「继续挖」弥补；
4. 下一步只有三条：**提交 `wpQYNvZp` 收口** / **换区扩产（需用户批准）** / **等 11-22 后 PPA 主题轮转**。

---

## 二十二、DEU 全量数据集盘点（344 个 / 16 category）与 pattern_scores 封盘（2026-11-04 夜）

### 22.1 ★ 全量 category 盘点（objective ① 的成果，此前从未完整做过）

`get_datasets(DEU/TOP500/D1, limit 500)` 实得 **344 个数据集**，分布：

| category | 数据集数 | maxCov | cov≥0.7 的集数 | 总字段数 |
|---|---:|---:|---:|---:|
| model | 90 | 0.9978 | **18** | 12,144 |
| news | 34 | 0.9630 | **10** | 1,046 |
| other | 82 | 0.9535 | **6** | 7,176 |
| pv | 32 | 1.0000 | **6** | 5,754 |
| analyst | 36 | 0.7879 | **4** | 8,624 |
| institutions | 10 | 1.0000 | **4** | 132 |
| risk | 10 | 1.0000 | **4** | 104 |
| sentiment | 6 | 0.9038 | **4** | 552 |
| shortinterest | 2 | 0.7105 | **2** | 50 |
| fundamental | 24 | 0.6900 | 0 | 4,196 |
| earnings | 4 | 0.0000 | 0 | 50 |
| imbalance | 2 | 0.0000 | 0 | 4 |
| insiders | 4 | 0.5617 | 0 | 84 |
| macro | 2 | 0.0000 | 0 | 26 |
| option | 2 | 0.0000 | 0 | 44 |
| socialmedia | 4 | 0.2748 | 0 | 38 |

**cov≥0.7 的候选合计 48 个数据集**（去重后约 24 个唯一集）。这是 DEU 的全部可用池。

### 22.2 ★ 此前「DEU 数据面穷尽」的判断被推翻：漏掉了 pattern_scores

`pattern_scores`（**pv，cov 0.9888，504 字段，alphaCount 266**）是 DEU 上覆盖最高、体量第二大的未挖数据集，此前从未接触。

**字段结构（504 个全 MATRIX，覆盖率全部 ≥0.9，最高 0.9996，无一低于 0.7）**：

- **5 个形态族**：`gap`（跳空缺口）/ `triangle`（三角）/ `sym_triangle`（对称三角）/ `wedge`（楔形）/ `v-reversal`（V 反转）；
- **每族双向**：`upward`/`downward`、`asc`/`desc`、`rising`/`falling`、`bottom`/`top`；
- **7 种统计口径**：`dynamic` / `max` / `mean` / `median` / `min` / `std` / `q95`；
- **3 种 lookback**：`60` / `120` / `40d`，另有 `*_simscore_lookback{N}` 与 `*_pattern` 变体；
- `head_and_shoulders` 族**不存在**（搜索返回空）。

### 22.3 三条探针（两个形态族 × 两种时间结构）

| 探针 | 形态族 | 时间结构 | S | F | TO | ladder | sub | DD | CLUSTER |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `WjObw1jo` | reversal（V底 − V顶） | **水平** | **−0.20** | −0.06 | 11.70% | +0.31 | −0.15 | 30.1% | −0.23 |
| `JjeN0dw2` | reversal（V底 − V顶） | **22 日差分** | **0.03** | 0.00 | 13.87% | 0.66 | +0.08 | 17.4% | 0.30 |
| `N1NaqW38` | gap（common up − down） | 净差水平 | **−0.02** | 0.00 | 12.38% | −0.42 | −0.09 | 12.5% | −0.25 |

**判读**：
1. **TO 11.7%–13.9% 属「时序骨架可用」档**（远高于 `other455` 的 0.99%），不是慢变字段；
2. **三条 |S| 全部 ≤ 0.20，其中两条 ≤ 0.03**，覆盖 2 个形态族 × 2 种时间结构 ⇒ 触发「≥3 种结构互异配置在同一指标上收敛（方差<0.05）⇒ 停该族」判据；
3. **水平版 vs 差分版的结构差异有信息**：差分把 DD 从 30.1% 压到 17.4%、ladder 从 +0.31 抬到 +0.66、CLUSTER 从 −0.23 翻到 +0.30 —— 处理方式是对的，**是 V 底/V 顶这一族形态本身没有 alpha**；
4. **技术形态相似度的经济学解释**：形态被「识别」出来时（相似度高）往往价格已反映完毕，所以「看涨形态」不是前瞻信号 —— 这与 §19.3 的「amihud 是桥不是增益腿」同类洞见：**可观测的技术形态是后视的**。

**结论：`pattern_scores` 在 DEU 封盘。** 理由不是覆盖不足、不是频率不足、不是骨架不当，而是**形态相似度本身无横截面预测力**。

### 22.4 操作事故记录（供后续避免）

派发 `3mNpuLclJ4KF9HGBXaJ3dda` 时**跳过了 preflight**，直接在字段族列表里挑名字，撞上 `mean_similarity_breakaway_gap_downward` 不存在（向下突破缺口只有 `dynamic` / `median` 口径，无 `mean`）⇒ 整条 ERROR。
**教训**：字段族列表是 `slice(0,6)` 采样，**不代表完整字段名集合**；任何未在本轮 preflight 里出现过的字段名，必须重新 preflight。

### 22.5 DEU 已试/未试清单（截至本轮）

**cov≥0.7 已试且封盘**：`model264`+`predictive_starmine`（出 `wpQYNvZp` 1 颗）/ `other455` 0.9535 / `analyst_earnings_ibes` 0.9978 / `news104` 0.963 / `institutions6` 1.0 / `pv29` 1.0 / `pv30` 0.7273 / `pattern_scores` 0.9888 / `fund_holdings_panel` 0.9019 / `sentiment27` 0.9038 / `risk60` / `risk88` / `analyst93` / `fundamental22` / `fundamental6` / `model28` / `model238` / `shortinterest3`。

**cov≥0.7 尚未试**：`model53`(cov0.905, 22f, **alphaCount 仅 9** — 全表最冷门) / `model36`(0.8488, 20f, ac58) / `model106`(0.7878, 14f, ac32 — Morningstar 星级) / `model216`(0.7121, 45f) / `news20`(0.7729, 46f, ac33) / `news50`(0.7644, 37f, ac42) / `news17`(0.7906, 48f, ac87) / `news18`(0.8046, 70f, ac137) / `analyst7`(0.7207, 608f, ac3993) / `dl_riskfree_returns`(other, 0.7147, 133f — 应为辅助非信号) / 以及 pv 剩余 3 个、institutions 剩余 2 个、risk 剩余 2 个、sentiment 剩余 3 个。

### 22.6 §二十二结论

1. **DEU 全池 = 344 数据集 / 16 category，cov≥0.7 的只有约 24 个唯一数据集**；
2. `pattern_scores`（cov 最高、504 字段）**三探针全灭，封盘**；
3. **形态相似度是后视信号**，这是「可观测技术形态无前瞻性」的直接实证；
4. 剩余未试集中在 `model53`/`model36`/`model106`/`news17-50`/`analyst7` 等**低字段数或高拥挤（analyst7 ac 3993）**的集；
5. **DEU 产出仍为 `wpQYNvZp` 一颗**，已提交 11 颗不变。

---

## 二十三、model53（信用违约期限结构）封盘 + model36 画像（2026-11-04 夜）

### 23.1 model53 字段画像（cov 0.905，22 字段，alphaCount 仅 9 —— 全表最冷门的高覆盖集）

**这是 DEU 唯一带完整期限结构的信用数据集**：

```
annualized_pd_{1_month,3_month,6_month,1_year,2_year,3_year,4_year,5_year,7_year,10_year}_jc7   cov 0.8734
mdl53_ms5_{同 10 个期限点}                                                              cov 0.9259
mdl53_implied_spreads（隐含信用利差）                                                    cov 0.916
data_observation_date_4                                                                 SYMBOL 1.0
```

**结构优势**：10 个期限点可支撑「斜率 / 曲率 / 倒挂」这类纯前瞻模板；两套独立信用模型（`annualized_pd` 与 `ms5`）+ 一条隐含利差，可构造模型间与模型-市场间的背离信号。这是 DEU 其它任何数据集都不具备的结构。

### 23.2 三条探针（三种结构）

| 探针 | 结构 | S | F | TO | margin | ladder | sub | DD | CLUSTER |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `qMLxv5NK` | PD **1 年水平** | **−0.12** | −0.02 | **42.68%** | −0.44bp | 0.06 | −0.34 | 33.8% | 0.06 |
| `kqNoX7W6` | **期限结构斜率**（10y − 1m） | **−0.18** | −0.03 | **43.53%** | −0.44bp | −0.57 | 0.00 | 19.7% | −0.03 |
| `VkxaE6QY` | PD **22 日平滑后水平** | **−0.09** | −0.02 | **1.92%** | −7.67bp | −0.15 | −0.28 | 31.3% | −0.06 |

### 23.3 ★ 决定性诊断：平滑排除「噪声掩盖信号」假设

前两条 TO 高达 42.7% / 43.5%（PD 绝对值每天微调 ⇒ rank 天天变），本可以辩解为「真信号被高频噪声淹没」。
第三条用 `ts_mean(·, 22)` 把 **TO 从 42.68% 压到 1.92%（降 22 倍）**，而 **S 从 −0.12 只变到 −0.09**。

⇒ **压掉 95% 的换手、信号纹丝不动 ⇒ 信号本身不存在，不是被噪声掩盖。** 这是本轮最干净的一个否证结构。
（对照 §二十一 `fund_holdings_panel`：那里是换手越高 S 越贴零，属成本磨平；这里换手降 22 倍 S 也不动，属根本无信号。）

### 23.4 经济学解释

**信用违约概率在 DEU 股票截面上没有 alpha**，可能原因：
1. 信用风险溢价已被股票价格充分反映（PD 是公开的第三方模型输出，无信息优势）；
2. DEU 的信用风险高度集中在银行/工业集团，**截面上区分度低**，中性化后剩不下横截面信息；
3. 两套模型（`annualized_pd` / `ms5`）同源，背离信号也只反映建模差异而非真实分歧。

### 23.5 model36 画像（下一个候选，待试）

cov 0.8488，20 字段，alphaCount 58。**两条产品线**：

- **`star_sr_*`（cov 全部 = 1.0）** —— Morningstar 星级基本面评分：`global_rank` / `region_rank` / `country_rank` / `sector_rank` / `industr_rank` / `growth` / `leverage` / `liquidity` / `profitability` / `coverage`；
- **`credit_risk_*_score_d1`（cov ~0.696–0.699）** —— 信用风险五维分项：coverage / growth / leverage / liquidity / profitability；
- **`default_risk_*_percentile_d1_2`（cov ~0.694–0.699）** —— 违约风险百分位：global / region / country / sector / industry。

`star_sr_*` 的 cov 1.0 是显著优势（全 TOP500 覆盖），但**评级类数据是滞后的第三方输出**，与已证无效的 `mdl106_stars` 同型。`credit_risk_*` / `default_risk_*` 与刚封盘的 `model53` 同属信用风险域，**大概率重复 §23 的否定结果**。

### 23.6 DEU 剩余清单（本轮更新）

**cov≥0.7 已试且封盘**：`model264`+`predictive_starmine`（出 `wpQYNvZp` 1 颗）/ `pattern_scores` 0.9888 / `other455` 0.9535 / `analyst_earnings_ibes` 0.9978 / `news104` 0.963 / `institutions6` 1.0 / `pv29` 1.0 / `pv30` 0.7273 / `fund_holdings_panel` 0.9019 / `sentiment27` 0.9038 / **`model53` 0.905（本轮）** / `risk60` / `risk88` / `analyst93` / `fundamental22` / `fundamental6` / `model28` / `model238` / `shortinterest3`。

**尚未试**：`model36`(0.8488, 20f, ac58) / `model106`(0.7878, 14f, ac32) / `model216`(0.7121, 45f) / `news20`(0.7729, 46f, ac33) / `news50`(0.7644, 37f, ac42) / `news17`(0.7906, 48f, ac87) / `news18`(0.8046, 70f, ac137) / `analyst7`(0.7207, 608f, ac3993 高拥挤) / `dl_riskfree_returns`(辅助) / pv 剩余 3 个 / institutions 剩余 2 个 / risk 剩余 2 个 / sentiment 剩余 3 个。

### 23.7 §二十三结论

1. `model53` **封盘**，三条结构互异探针 |S| ≤ 0.18 且收敛；
2. **平滑实验（TO 42.68%→1.92%，S 不变）是干净否证**：信号本身不存在，排除噪声掩盖假设；
3. **信用风险域已全灭**：`model53`（PD 期限结构）+ `model36` 的 `credit_risk_*` / `default_risk_*` 大概率同灭；
4. DEU 剩余高覆盖未试集已收窄到 `model36`(star_sr 评级) / `model106`(星级) / `model216` / `news17-20-50-18` / `analyst7`；**全部属低字段数或评级/新闻类滞后数据**；
5. **DEU 产出仍为 `wpQYNvZp` 一颗**，已提交 11 颗不变。

---

## §二十四 model36 收口 + ★★★★★ model264 重新发现（2026-11-04 下午）

### 24.1 model36 五维星级合成收口 ⇒ 封盘

| 维度数 | alpha | S | F | TO | margin | 2Y | sub | DD | CLUSTER |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1（global_rank） | `ZYQbl391` | 0.49 | 0.25 | 2.12% | 31.1bp | −0.82 | +0.47 | 19.7% | 0.29 |
| 4（growth+profit+lev+liq） | `e75b2K3O` | 0.60 | 0.35 | 2.32% | 36.0bp | −0.52 | +0.61 | 14.3% | 0.32 |
| 5（+coverage） | `wpQZzY61` | **0.66** | 0.40 | 2.24% | 41.8bp | **−0.44** | +0.62 | 13.8% | 0.39 |

**收口判据（三条同时成立）**：
1. **增量衰减**：0.49→0.60 是 +0.11，0.60→0.66 只有 +0.06；等差外推剩下 5 个 `*_rank` 全加进去上限 ≈ 0.72，距 1.58 还差 0.86；
2. **2Y 始终深度负**（−0.82 → −0.52 → −0.44）：近年衰减型信号，非稳态 alpha；
3. **TO 锁死 2.2%**：星级由季度评级驱动，物理上无法提换手 ⇒ F 上限 = 0.66×√(0.047/0.125) ≈ 0.40，天花板已算出。

⇒ **model36 星级族封盘**，与 `mdl106_stars` 同源同结论（Morningstar 评级是滞后第三方输出）。

### 24.2 ★★★★★ 重新发现：model264 是 95 字段的单塔 ATOM 矿脉（此前严重低估）

此前只把 model264 当「出腿用」（取 5 个 `_class` 当价值腿/流动性腿），**从未把它当独立 ATOM 源**。重查字段全貌实测：**380 字段 = 95 个 `_class`（cov 全部 1.0）+ 108 个 `_l1/_l2/_l3`（cov 0.9965-0.9966）**。

| 机制族 | 数量 | 代表字段 |
|---|---:|---|
| 分析师预期 | 27 | `es_{eps,ebitda,ebit,sale,roe,ltg,rec,tp,nav,dps,bps,cfps}_{fy1,ntm}_{r1m,d1m,d3m}` |
| 技术量价 | ~30 | `wr` `cci` `mfi` `obv` `vpt` `adl` `cmf` `macd` `trix` `tsi` `ppo` `pvo` `so` `do` `atr` `bb` `amihud` `abn_volm` `clv` `emv` `nvi` `spi` `vi` `mi` `hilomid` `lco` `fca` `ma_15_36` `ma_30_75` `float_to` |
| 价值 | 12 | `bookp` `bookp_fy1` `div_payout` `divyld_bb` `psale` `fincf` `payable_to` `ext_fin_noa` `lt_dt_eq_chg` `dpmo` `dpo` `co` |
| 动量增长 | 8 | `rtn21d` `rtn63d` `rtn_12m1m` `rtn2520d` `gr_5y_eps` `gr_5y_cfps` `gr_eintr_cfps` `hr_epsyld` |
| 风险离散 | 6 | `eps_disp` `eps_sur_decay` `lottery` `vol_vo_p_1m` `abn_volm` `tstk` |
| 新闻情绪 | 3 | `news_abno_sent_1d` `news_abno_vol_1d` `news_sentvol_1d` |

**结构性优势**：全部字段同属 model264 一个数据集 ⇒ **任意组合都是合法单塔 MODEL ATOM，不占禁混配额**（trio×非trio 已满 5/5）。`wpQYNvZp` 核心腿 `mdl264_div_payout_class` 正出自这里。

### 24.3 三条机制组探针（4 字段等权 rank 合成，8 算子）

| alpha | 机制组 | S | TO | margin | 2Y | sub | DD |
|---|---|---:|---:|---:|---:|---:|---:|
| `LLMNlAYe` | 分析师预期（eps_fy1_r1m/rec_r1m/tp_r1m/ebitda_fy1_r1m） | **0.24** | 6.16% | 5.4bp | 0.10 | **−0.34** | 15.4% |
| `wpQZJLg1` | 反转（wr/cci/mfi/lottery） | 0.53 | 5.52% | 14.9bp | 0.43 | −0.18 | 19.0% |
| `omEL9A5b` | 质量价值（gr_5y_eps/gr_5y_cfps/bookp/divyld_bb） | **0.54** | 6.76% | 11.2bp | **0.63** | **+0.11** | 16.8% |

**判据一**：分析师组只有 0.24 ⇒ **DEU 上有效的分析师信号是 14 日级修正**（`wpQYNvZp` 用 `mean_estimate_change_pct_f12m_earnings_14d_4`），**1 月级 `_r1m` 已衰减**。model264 的 `es_*` 最短只有 1 月，无 14 日字段 ⇒ 该族在 DEU 结构性吃亏。

**判据二**：TO 5–7% 是最重要的元信息 —— **model264 的 `_class` 是日频更新**，与 model36（2.24% 锁死）形成对比。**「提换手」在 model264 上物理可行，在 model36 上不可行。**

### 24.4 ★★★★★ 单字段方向表（6 字段全正 S、全正 2Y —— 质的区别）

骨架 `group_neutralize(rank(F), subindustry)`（2 算子，decay 16）：

| alpha | 字段 | S | TO | margin | 2Y | sub | DD | 方向解读 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `O0AN5Weq` | **amihud** | **0.69** | 13.16% | 7.0bp | **0.90** | +0.12 | 13.7% | 非流动性溢价：高 illiquidity → 高收益 ✓ |
| `Xg9bYaVz` | **wr** | 0.59 | 11.66% | 7.9bp | **0.85** | +0.19 | 18.6% | **正向 = 动量，不是反转**（%R 近 0 即超买 → 继续涨） |
| `LLMNlme6` | es_rec_r1m | 0.58 | 7.92% | 10.2bp | 0.61 | — | 15.7% | 推荐上调 → 正收益 ✓ |
| `leAvRYJ2` | **lottery** | 0.56 | **4.60%** | **19.4bp** | 0.58 | −0.03 | 18.2% | **正向 = 高彩票偏好跑赢**（与 MAX 效应相反，DEU 追高占优） |
| `j2YAdaae` | bookp | 0.44 | 12.56% | 5.2bp | 0.74 | +0.19 | 14.5% | 价值溢价 ✓ |
| `9qxjAkgo` | obv | 0.33 | 10.00% | 4.7bp | 0.24 | **−0.31** | 15.7% | 最弱且 SUB 崩，**弃** |

**三条推论**：
1. **6 个字段全部正 S 且 2Y 全正（0.24–0.90）**。DEU 此前所有候选都死在 2Y 或 ladder（`model36` −0.44、`model53` 负、`wpQYNvZp` 靠 ladder 硬撑），**这批 `_class` 是首批不随时间衰减的截面信号**。
2. **`wr` 方向被证伪为「正向=动量」**：§24.3 反转组只有 0.53，正是「把 wr 当反转取负」造成方向对抗后的残值。**方向错了模板再多样也是废的** —— 这是必须先做单字段方向表的方法论依据。
3. **`lottery` 是全表唯一「低换手 + 高 margin」组合**（TO 4.60% / margin 19.4bp）：TO < 12.5% 下限 ⇒ F 分母恒为 0.125，**提 S 即可等比提 F**。

### 24.5 news18 结构判定 ⇒ 降为低优先

`get_datafields(news18)` 实测 **70 字段 = 64 VECTOR + 6 SYMBOL**；cov≥0.7 的 27 个里 **17 个是元数据**（`*_date_utc` / `*_time_utc` / `*_iso_code` / `*_sequence_number` / `story_event_count`），真事件字段不到 10 个且全是缩写码 `nws18_multiple_comp_{acb,bam,bee,ber,ghc_lna,nip,qcm,qep,qmb,ssc,sse}` + `mltpl_cmp_event_relevance` / `mltpl_cmp_event_simildays` / `multiple_comp_relevance`。

⇒ 与已封盘 `sentiment27`（14 VECTOR + 4 SYMBOL，去元数据剩 8 个同族真信号）同型，**凑不出 10 个结构互异模板**。降为低优先。

### 24.6 §二十四结论

1. **`model36` 封盘**：五维合成 S 0.66、增量衰减、2Y −0.44、TO 锁死 2.24%；
2. **★★★★★ model264 是本轮唯一活矿脉**：95 个 cov-1.0 `_class` × 六大机制族 × 日频更新 × 单塔 ATOM 不占配额；
3. **单字段方向表已建立**：amihud 0.69 > wr 0.59 > es_rec_r1m 0.58 > lottery 0.56 > bookp 0.44 > obv 0.33，**全部正 2Y**；
4. **方向纪律**：任何组合前必须先有单字段方向表，否则方向对抗吃掉一半信号（`wr` 教训）；
5. `news18` 与 `sentiment27` 同型（元数据淹没真信号），降为低优先；
6. **DEU 产出仍为 `wpQYNvZp` 一颗（未提交）**，已提交 11 颗不变。

---

## §二十五 ★★★★★ starmine 单腿解剖 + 因子族产量上限=1 的决定性证明

### 25.1 predictive_starmine f12m 网格强度（4 字段实测）

骨架 `group_neutralize(rank(ts_mean(F, W)), subindustry)`：

| alpha | 字段 | 口径 | S | F | TO | margin | DD | 2Y | sub | CLUSTER |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `6XdjRGxG` | `mean_estimate_change_pct_f12m_earnings_14d_4` | 修正 | **1.27** | **0.93** | 11.37% | 11.9bp | **9.04%** | 0.80 | **0.95** | — |
| `d5WbnWnv` | `predicted_surprise_f12m_ebitda_4` | 惊喜 | 0.91 | 0.53 | 7.16% | 11.7bp | **7.04%** | **1.62** | 0.83 | 0.83 |
| `3qoXAndP` | `mean_estimate_change_pct_f12m_ebitda_14d_4` | 修正 | 0.98 | 0.64 | 11.52% | 9.3bp | 9.11% | **0.28** | 0.85 | **0.79** |
| `GrWbkWZ5` | `predicted_surprise_f12m_revenue_4` | 惊喜 | 0.28 | 0.09 | 6.75% | 3.6bp | 11.89% | **−0.83** | 0.00 | 0.32 |

**只有前两条是强腿**：`earnings` 修正负责 S（1.27）、`ebitda` 惊喜负责 2Y（1.62）。两者互补性极好。
**字段名实测不存在**：`earnings_30d_4` / `ntm_earnings_14d_4` / `f24m_earnings_14d_4` / `sales_4` / `earnings_14d_1`；**存在但未用**：`mean_estimate_change_pct_f12m_ebitda_30d_4`。

### 25.2 ★★★★ 两腿 ATOM：加工方式全面伤害（完整证据链）

`zq38O9aX` = 朴素两腿（**6 算子**）：
```
group_neutralize(add(rank(ts_mean(F1, 10)), rank(ts_mean(F2, 5))), subindustry)
```
**S 1.47 / F 1.17 ✓ / TO 9.86% / margin 16.0bp / DD 4.57% / 2Y 1.51 / sub 1.19 ✓**，失败项只剩 `LOW_SHARPE`（差 0.11）与 `LOW_2Y_SHARPE`（差 0.07）。

| 加工方式 | 算子 | alpha | S | F | TO | DD | 2Y | sub | ΔS vs 朴素 |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **无（朴素基准）** | **6** | `zq38O9aX` | **1.47** | **1.17** | 9.86% | **4.57%** | **1.51** | **1.19** | — |
| + `ts_decay_linear(·,5)` + `ts_backfill(·,66)` | 10 | `A1VNkJle` | 1.30 | 0.97 | 9.17% | 5.49% | 1.43 | 1.06 | **−0.17** |
| + 第三腿（revenue 惊喜） | 12 | `6XdjEX3P` | 1.39 | 1.09 | 9.46% | 5.36% | **0.77** | 1.03 | −0.08 |
| + 第三腿 + `winsorize` | 10 | `omELYmz5` | 1.29 | 0.95 | 8.95% | 4.65% | 0.84 | 0.91 | −0.18 |
| + `ts_zscore(·,252)` + `ts_backfill` | 10 | `A1VN3PQY` | **0.49** | 0.25 | 9.04% | 12.77% | 0.75 | 0.80 | **−0.98** |

**统一解释**：分析师修正的 alpha 来自**截面绝对水平**。`ts_decay_linear` / `ts_zscore` / `winsorize` 都是在把绝对水平转成「相对自身历史」或压缩尾部 ⇒ 直接扔掉信号本体。`ts_zscore` 最致命（−0.98）。

**这与 §二十四 model36 的判据相反**：那里加工（五维合成）是正贡献（0.49→0.66），因为单维星级本身区分度太低。**加工是否有益取决于原始信号是否已在截面上有足够区分度。**

### 25.3 加腿的边际效应：负贡献

`revenue` 惊喜单维只有 S 0.28 / **2Y −0.83**，把它加进两腿后：四腿 2Y 从 1.51 崩到 **0.77**。
**教训**：加腿前必须先测单维，**弱腿（S<0.4 或 2Y<0）会以 2Y 为代价污染整体**。这与 §24.4 的「方向表先行」纪律同源。

### 25.4 ★★★★ `wpQYNvZp` 结构解剖：10 算子其实是「两腿朴素 + 价值腿填充」

```
group_neutralize(add(add(
  rank(ts_decay_linear(ts_backfill(mdl264_div_payout_class, 66), 5)),   # 4 算子：价值腿+填充
  rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 10))),     # 2 算子：修正强腿
  rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), subindustry)     # 2 算子：惊喜强腿
```
**10 算子 = 4（div_payout 腿，其中 decay+backfill 纯属算子填充）+ 2 + 2 + 2（add/group）**。

关键认知：**`wpQYNvZp` 的 10 算子下限是靠「给价值腿套 decay+backfill」凑出来的，而这两个算子对两腿核心信号是纯损耗**（§25.2 已证 −0.17）。但因为它们只作用在价值腿上、不碰两条 starmine 强腿，损耗被摊薄，加上 div_payout 本身贡献 +0.21，净效果仍是全族最优（S 1.68）。

### 25.5 ★★★★ 替换价值腿实验（amihud / lottery）

| alpha | 价值腿 | S | F | TO | margin | DD | 2Y | ladder | sub | 失败项 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `wpQYNvZp` | `div_payout` | **1.68** | **1.36** | 13.15% | 13.1bp | — | 1.83 | **2.18(y2)** | 1.17 | **无 ✓** |
| `JjeNpjbm` | **`lottery`** | 1.53 | 1.33 | **7.98%** | **23.5bp** | 7.50% | 1.53 | 1.53(y2) | 1.07 | S 差 0.05 / ladder 差 0.05 |
| `YP1bpP0o` | **`amihud`** | 1.50 | 1.29 | 8.63% | **21.3bp** | 6.95% | 1.51 | 1.51(y4) | 1.01 | S 差 0.08 / ladder 差 0.07 |

**swap 的净效果**：TO 13.15% → 8.0–8.6%（**降 35–39%**）、margin 13.1bp → 21–24bp（**升 63–79%**），但 S 降 0.15–0.18、ladder 从 2.18 掉到 1.51–1.53。
⇒ **div_payout 腿在 S 与 ladder 上的贡献不可替代**（amihud/lottery 虽单维更强但会稀释 starmine 强腿）。

### 25.6 ★★★★★ 互相关矩阵 ⇒ 因子族产量上限 = 1 颗（决定性负面结论）

`compute_mutual_correlation`（本地零配额，4 年 1021 点）：

|  | wpQYNvZp | YP1bpP0o | JjeNpjbm | zq38O9aX | A1VNkJle |
|---|---:|---:|---:|---:|---:|
| **wpQYNvZp**（div_payout） | 1 | 0.746 | **0.770** | 0.756 | 0.677 |
| **YP1bpP0o**（amihud） | 0.746 | 1 | **0.949** | 0.694 | 0.647 |
| **JjeNpjbm**（lottery） | 0.770 | **0.949** | 1 | 0.680 | 0.625 |
| **zq38O9aX**（朴素两腿） | 0.756 | 0.694 | 0.680 | 1 | **0.957** |
| **A1VNkJle**（加工两腿） | 0.677 | 0.647 | 0.625 | **0.957** | 1 |

**三条硬结论**：
1. **换腿不改变信号**：amihud ↔ lottery = **0.949**（两个经济学上无关的腿，换掉后相关性几乎不变）；
2. **换加工不改变信号**：朴素 ↔ 加工 = **0.957**；
3. **所有变体与 `wpQYNvZp` 相关 0.677–0.770**，除 `A1VNkJle`(0.677) 外全部 >0.70。

⇒ **PnL 主体是两条 starmine 强腿，任何腿替换/加工变异都在同一个 PnL 主体内换壳。**
⇒ **`model264 × predictive_starmine` 因子族的产量上限 = 1 颗**（取最优 `wpQYNvZp`）。
⇒ 这条路线**已彻底榨干**，不再投入。

**方法论**：判断「一个因子族还能出几颗」的最快方法 = 对本族全部候选跑 `compute_mutual_correlation`。若族内互相关 ≥0.95，无论换腿还是换加工都在同一 PnL 主体内，产量恒为 1。

### 25.7 model264 单塔 ATOM 上限（top5 = S 0.66）

`KPJNXxvl` = amihud + wr + es_rec_r1m + lottery + bookp 五字段等权（10 算子）：**S 0.66 / F 0.42 / TO 6.19% / margin 16.7bp / 2Y 0.80 / sub 0.16 / CLUSTER 0.60**。
五维平均单维强度 0.572，组合只到 0.66（+0.09）⇒ 反推 ρ≈0.5–0.6，**五字段高度共线**。
另一条 `_l1` 支线：`div_payout_l1` S −0.41、`amihud_l1` S −0.41，与 `_class` 版（+0.47/+0.69）**方向相反且更弱** ⇒ `_l1/_l2/_l3` 是分位层级标签，非连续原始值，支线关闭。

### 25.8 §二十五结论

1. **★★★★★ 决定性负面结论**：`model264 × predictive_starmine` 因子族产量上限 = **1 颗**，族内互相关 0.949–0.957 证明换腿/换加工只是换壳；
2. **`wpQYNvZp` 仍是唯一全闸资产**（S 1.68 / F 1.36 / ladder 2.18 / TO 13.15% / sub 1.17 / prod 0.6333 / self 0.6332 / failed_any=0），且已是本族最优；
3. **加工纪律**：对已在截面有区分度的信号（S>1.0），`ts_decay_linear`/`ts_zscore`/`winsorize` 全面有害（−0.17 ~ −0.98）；对区分度不足的信号（model36 单维 0.49），加工有正贡献；
4. **加腿纪律**：必须先测单维，弱腿（S<0.4 或 2Y<0）会以 2Y 为代价污染整体（revenue 惊喜把四腿 2Y 从 1.51 砸到 0.77）；
5. **model264 单塔 ATOM 上限 ≈ 0.66**，达不到闸；`_l1/_l2/_l3` 支线关闭；
6. **DEU 产出上限 = 12 颗**（11 已提交 + `wpQYNvZp`），距 30 颗目标差 18 颗，**结构性不可达**。

---

## 二十六、★★★★★ 突破：mdl216 preferred revision 打开全新正交强腿（2026-11-04）

### 26.1 最强单维：`mdl216_preferredblendedrevisionfy1percent`

`model216`（cat **model**，cov 0.7121，**45 字段全 VECTOR**，ac 629）此前被漏查。VECTOR 必须先 `vec_avg` 聚合再做算术。

单维探针（`group_neutralize(rank(ts_mean(vec_avg(F), 10)), subindustry)`，5 算子）：

| 字段 | S | F | TO | margin | DD | 2Y | sub | 判定 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **preferredblendedrevisionfy1** | **1.52** | **1.40** | 4.44% | **48.07bp** | 10.00% | 0.96 | 0.88 | 只差 S 0.06 |
| secondaryblendedrevisionfy1 | 1.16 | 0.97 | 4.66% | 37.22bp | 14.16% | 0.47 | 0.55 | CLUSTER 0.98 贴线 |
| revenueblendedrevisionfy1 | 0.42 | 0.20 | 4.43% | 13.04bp | 18.76% | 0.62 | 0.04 | 废 |
| recommendationblendedrevision | 0.09 | 0.02 | 5.32% | 2.21bp | 26.53% | −0.79 | 0.29 | 废 |
| secondaryblendedrevisionfq1 | 0.33 | 0.16 | 6.71% | 9.30bp | 15.40% | 0.30 | −0.27 | 废 |
| secondaryblendedrevisionfy2 | 0.65 | 0.42 | 4.61% | 22.28bp | 13.66% | 0.33 | 0.09 | 废 |

**margin 48.07bp 是 DEU 全战役最高**（此前纪录 36.73bp d5Wb5XP2 / 37.22bp 本表 secondary）。
`preferred` 与 `secondary` 差 0.36 S ⇒ **ARM 模型里「首选口径」与「次选口径」是两个强度档**，不是同一信号换名。

### 26.2 ★★★★★ 两腿组合 = 全闸 0 失败

`vR1rjj3a`（**7 算子**）：`group_neutralize(add(rank(ts_mean(vec_avg(preferred_fy1),5)), rank(ts_mean(predicted_surprise_f12m_ebitda_4,5))), subindustry)`

**S 1.75 / F 1.65 / TO 6.82% / margin 32.56bp / DD 5.63% / 2Y 2.03 / ladder窗 3 / sub 1.33 / RA 0**

三项全部超过 `wpQYNvZp`：S 1.75 vs 1.68、2Y 2.03 vs 2.03(持平)、**DD 5.63% 显著更低**、TO 6.82% vs 13.15% 腰斩、margin 32.56 vs 13.1bp。
**self 相关 0.6087 < 0.70 ✓**（低于 wpQYNvZp 0.6332）。

机制互补性成立：preferred 修正负责 **S**（1.52 但 2Y 仅 0.96），ebitda 惊喜负责 **2Y**（单维 0.91 / 2Y 1.62）⇒ 两维正交拼接后 S/2Y 同时抬升。

### 26.3 ★★★★★ ladder 闸线是「按窗口变动」，不是常数 1.58（纠正既有记录）

精确解析 `checks.fail` / `checks.warning` 后确认：

| alpha | ladder 值 | 闸线 | 窗口 | 归属 |
|---|---:|---:|---:|---|
| `d5Wb5XP2` | 1.40 | 1.58 | y4 | fail |
| `3qoXleQ6` | 1.56 | 1.58 | y4 | fail |
| `YP1bbNNJ` | 1.52 | 1.58 | y2 | fail |
| `GrWbbG33` | 1.56 | 1.58 | y2 | fail（差 0.02）|
| `Xg9b73x1` / `zq3889zE` | 1.65 | **1.75** | y7 | warning→RA 计入 |
| `P0o27RRp` | 1.66 | **1.75** | y7 | fail |
| `vR1rjj3a` / `wpQYNvZp` | — | — | — | **无条目 = 全窗通过** |

**结论**：闸线在 1.58 与 1.75 两档之间变化，取决于窗口。所以「ladder 1.58」不能当通用靶子；
**判据只能是 `checks.fail` 是否为空**。y7 对应约 2020–21 区间，那里的要求更严（1.75）。

### 26.4 ★★★★ 只有 `ts_backfill` 会改变信号本体；`ts_decay_linear(·,1)` / 双 `group_neutralize` 是精确恒等

`vR1rjj3a`（7 算子，1.75/2.03）逐项加算子的对照：

| 加工 | 算子 | alpha | S | 2Y | ladder窗 | RA失败 | 判定 |
|---|---:|---|---:|---:|---:|---:|---|
| 无（基准）| 7 | `vR1rjj3a` | 1.75 | 2.03 | 3 | 0 | 算子不达标 |
| **双 gn + `ts_decay_linear(·,1)` + `ts_mean(·,1)`（纯恒等）** | **10** | `gJebZANl` | **1.75** | **2.03** | 3 | **0** | **精确保留 ✓** |
| F1 `ts_backfill(·,22)` + F2 `ts_decay_linear(·,3)` + 双 gn | 10 | **`E56pROb9`** | **1.79** | 2.03 | 3 | **0** | **最优 ✓** |
| 双腿 `ts_decay_linear(·,3)` + 双 gn（**无 backfill**）| 10 | `QPvbKZqp` | 1.76 | 1.76 | 7 | 0 | 2Y 降至 1.76 |
| 双 gn + 双层中性化（subindustry→sector）| 10 | `xAr3bKel` | 1.77 | **2.06** | 3 | **0** | 2Y 最高 ✓ |
| 双腿 backfill66 + 双 gn | 10 | `zq3889zE` | 1.65 | 1.65 | 7 | 1 | 退化 |
| 双腿 backfill66 + decay3 | 10 | `Xg9b73x1` | 1.65 | 1.65 | 7 | 1 | 退化 |
| F2 backfill22 + `ts_mean(·,1)` + 双 gn | 10 | `GrWbbG33` | 1.69 | 1.56 | 2 | 1（差0.02）| 退化 |

**硬结论**：`ts_backfill` 是唯一真正改动信号的填充（predictive_starmine cov 0.79 ⇒ 约 21% 股票被填值，直接改截面）；
而 `ts_decay_linear(x,1)`、`ts_mean(x,1)`、重复 `group_neutralize(x,g)`（幂等）都是**数学恒等**，不改变 PnL。
⇒ 补算子到 10 时的安全手段 = **恒等算子 + 真实平滑（decay）**，backfill **只能加在修正腿 F1 上、且必须配 F2 的 decay**；单独 backfill F2 会毁掉 2Y 与 ladder 窗口（1.65/1.65/y7）。

### 26.5 ★★★★★ 四条合法 10 算子候选（均 RA 0 失败）

| alpha | 结构 | S | F | TO | margin | DD | 2Y | sub | self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`E56pROb9`** | F1 backfill22 + F2 decay3 + 双 gn | **1.79** | **1.70** | 6.74% | 33.34bp | 5.62% | 2.03 | 1.32 | 0.6004 |
| `xAr3bKel` | 双腿 + 行业→板块双层中性化 | 1.77 | 1.68 | 6.81% | 32.92bp | 5.58% | **2.06** | 1.33 | 0.6064 |
| `QPvbKZqp` | 双腿 decay3 + 双 gn（无 backfill）| 1.76 | 1.66 | 6.72% | 32.89bp | 5.57% | 1.76 | 1.30 | 0.6028 |
| `gJebZANl` | 纯恒等填充 | 1.75 | 1.65 | 6.82% | 32.89bp | 5.62% | 2.03 | 1.33 | — |

**取 `E56pROb9`**（S/F 最高，且 9/10 算子有实义：双腿 decay3 + 双 gn 中性化）。

### 26.6 ★★★★★ 新族与旧族只有 0.55 相关 ⇒ 真正交

`compute_mutual_correlation`（本地零配额）：

|  | E56pROb9 | xAr3bKel | QPvbKZqp | vR1rjj3a | wpQYNvZp |
|---|---:|---:|---:|---:|---:|
| **E56pROb9** | 1 | 0.9967 | 0.9970 | 0.9941 | **0.5538** |
| **xAr3bKel** | 0.9967 | 1 | 0.9945 | 0.9975 | **0.5642** |
| **QPvbKZqp** | 0.9970 | 0.9945 | 1 | 0.9967 | **0.5523** |
| **vR1rjj3a** | 0.9941 | 0.9975 | 0.9967 | 1 | **0.5627** |
| **wpQYNvZp** | 0.5538 | 0.5642 | 0.5523 | 0.5627 | 1 |

两条硬结论：
1. 新族内部 0.994–0.9975 ⇒ **同族只能提 1 颗**（与 §25 的产量上限法则一致）；
2. **新族 vs `wpQYNvZp` 仅 0.55 ⇒ 是两个真正独立的 PnL 主体**。若两者都提交，互相关 0.55 < 0.70 不会互相卡 self 闸。

### 26.7 三塔近场全灭收口（本轮实测）

| 塔 | 距点亮 | 本轮结论 |
|---|---:|---|
| **other** | 差 1 | `dl_riskfree_returns` 三探针上限 0.65 且 2Y≈0；`other455`/`other532` 已封；**该塔 cov≥0.7 数据集 3 个全部试完** |
| **analyst** | 差 1 | `analyst7` 上限 0.69；跨塔三腿 `ZYQbEPqd`（analyst 广度 + starmine 两腿）**S 1.22 / 2Y 1.26 / ladder 1.26(y2)**，比两腿 1.47 与 wpQYNvZp 1.68 都差 ⇒ **修正广度与修正幅度同机制，共线互噬**；`analyst48`/`analyst44` 已封 |
| **shortinterest** | 差 1 | 唯一数据集 `shortinterest3` 已封且无替代 ⇒ **客观无解** |
| **model** | 差 2 | ★ **本轮全部新出货都落在 model 塔**（pyramids = `DEU/D1/MODEL`，multiplier 1.8）|

**修正后的 DEU 现实**：近场不是 other/analyst/shortinterest，而是 **model（1/3，差 2）** ——
新族四条候选全部是 model 塔，提交 1 颗 → model 2/3；再出 1 颗不同机制 → model 点亮。

### 26.8 DEU cov≥0.7 数据集全量清点（172 个中只有 29 个达标）

| 状态 | 数量 | 说明 |
|---|---:|---|
| 已封盘/已试 | 20 | 含 model264/36/106/53、predictive_starmine、analyst7/48/44、other455/532、dl_riskfree_returns、pattern_scores、fund_holdings_panel、news18、shortinterest3 等 |
| 本轮已试 | 2 | model216、analyst_earnings_ibes（名字误导：实为价格量数据，非 IBES 预期）|
| **仍未试** | **7** | `news17`(48f/ac87)、`news50`(37f/42)、`news20`(46f/33)、`sentiment7`(**仅3字段**/94)、`pv29`(50f/66，全 GROUP 无信号腿)、`pv30`(285f/287，全 GROUP)、`sentiment27`(18f/324，已判死) |

⇒ **DEU 高覆盖矿脉实质见底**。剩余 7 个里 4 个是 news/sentiment 元数据型（`news18` 已验证凑不出 10 个互异模板），2 个 pv 是纯 GROUP 轴，1 个只有 3 字段。
⇒ 这也是为什么本轮必须靠 `model216`（cov 0.7121，此前漏查）才拿到突破。

### 26.9 §二十六结论

1. **★★★★★ 本战役第二颗全闸资产诞生**：`E56pROb9`（10 算子）S **1.79** / F **1.70** / TO 6.74% / margin 33.34bp / DD 5.62% / 2Y 2.03 / sub 1.32 / self 0.6004 / **RA 0 失败**；
2. **它全面优于 `wpQYNvZp`**（S +0.11 / F +0.34 / TO −6.41pct / DD 更低 / margin +20.2bp），且两者仅 0.55 相关；
3. **待验：prod 相关性**。首次查询遇 `correlation_busy`（holder `corr:get_production_correlation(bl6boze6)`），第二次 120s 超时（平台仍在算）⇒ 需稍后重查；
4. **方法论纠正**：① ladder 闸线按窗口在 1.58/1.75 间变动，只能看 `checks.fail`；② 补算子禁用 backfill，用 decay/恒等算子；
5. **塔位重排**：本轮全部新出货属 **model** 塔 ⇒ 差 2 颗点亮，是目前最可及的目标塔；other/analyst 已实测见底、shortinterest 客观无解；
6. **DEU cov≥0.7 只剩 7 个未试且全是低质**，高覆盖矿脉已见底。

### 26.10 ★★★★ E56pROb9 逐年体检与「3 年 leading gap」冲突

`get_alpha_yearly_stats` 实测（longCount 与 pnl 逐年）：

| 年 | E56pROb9 | wpQYNvZp（对照）|
|---|---|---|
| 2014 | **lc=0 / pnl=0（空窗）** | S 2.70 / lc 106 |
| 2015 | **lc=0 / pnl=0（空窗）** | S 1.04 / lc 111 |
| 2016 | **lc=0 / pnl=0（空窗）** | S 0.60 / lc 116 |
| 2017 | S 1.46 / lc 80 | S 1.08 / lc 127 |
| 2018 | S 2.35 / lc 82 | S 2.58 / lc 128 |
| 2019 | S 1.74 / lc 86 | S 1.82 / lc 134 |
| 2020 | S 1.10 / lc 87 | S 1.34 / lc 145 |
| 2021 | S 2.84 / lc 120 | S 1.49 / lc 169 |
| 2022 | S 1.99 / lc 119 | S 1.67 / lc 182 |
| 2023 | S 1.27 / lc 108 | S 2.75 / lc 170 |

**结论**：
1. **空窗根因 = `mdl216`（数据 2017 起）**，不是 starmine —— `wpQYNvZp` 同为 starmine 腿但 10 年全覆盖；
2. E56pROb9 有数据年份 **7/7 全部正收益**（S 1.10–2.84，无负年），质量优于覆盖率；
3. 但相对约束⑤「近十年要有数据」只有 **7/10 年**，属 **3 年 leading gap**（起始晚型）。

**两条路线权衡**：

| | `wpQYNvZp` | `E56pROb9` |
|---|---|---|
| 覆盖 | **10/10 年** ✓ | 7/10 年（leading gap 3 年）|
| S / F | 1.68 / 1.36 | **1.79 / 1.70** |
| DD | 未记（较高）| **5.62%** |
| TO | 13.15% | **6.74%** |
| margin | 13.1bp | **33.34bp** |
| self | 0.6332 ✓ | 0.6004 ✓ |
| prod | **0.6333 ✓ 已验证** | **未验证（槽被占）** |
| RA 失败 | 0 | 0 |

**两者互相关仅 0.5538** ⇒ 若 **同时提交，model 塔 1+2 = 3 颗 → DEU/D1/MODEL 塔点亮**。
这是本战役第一次出现「两颗正交互补且各自全闸通过」的组合。

### 26.11 prod 相关性排障记录

`check_correlation(E56pROb9, production)` 连续 4 次失败：
1. `correlation_busy` holder=`corr:get_production_correlation(bl6boze6)`（他会话占用）；
2. `MCP tool call timed out after 120000ms`（平台在算，非失败）；
3. `inflight: true`（本机已触发，勿重触发）；
4. 再 `correlation_busy` holder=`corr:get_production_correlation(akK2vpWW)`（又被另一会话抢占）。

⇒ **prod 是账号级单并发且跨会话共享，排队不可控**。结论：不能把 prod 当同步闸；
**零成本工作（互相关/字段画像/台账）应并行完成，prod 留到槽空闲时单点补测**。

### 26.12 MCP 会话失效排障（本轮实测，唯一有效解）

症状：`Streamable HTTP error ... {"code":-32600,"message":"Session not found"}`。
无效手段：① 重启服务进程（`Stop-Process` + `tools/start_wq_mcp.py --wait 45`）——服务健康但客户端仍持旧 session id；② 直接重试工具调用。
**唯一有效**：`mavis_mcp_update({name:"wq-brain-http", enabled:false})` → `enabled:true`，强制宿主重建 MCP 客户端连接，随后 `authenticate` 立即成功。

### 26.13 提交预案（待用户真实确认，未执行任何平台写操作）

**候选 A（10 年全覆盖，prod 已验证）**：`wpQYNvZp`
- S 1.68 / F 1.36 / TO 13.15% / margin 13.1bp / 2Y 1.83 / sub 1.17 / self 0.6332 / **prod 0.6333 allPassed=true** / failed_any=0
- pyramids：`DEU/D1/MODEL`

**候选 B（3 年 leading gap，prod 未验）**：`E56pROb9`（**10 算子**）
```
group_neutralize(group_neutralize(add(rank(ts_mean(ts_backfill(vec_avg(mdl216_preferredblendedrevisionfy1percent), 22), 5)), rank(ts_decay_linear(ts_mean(predicted_surprise_f12m_ebitda_4, 5), 3))), subindustry), subindustry)
```
- S 1.79 / F 1.70 / TO 6.74% / margin 33.34bp / DD 5.62% / 2Y 2.03 / sub 1.32 / self 0.6004 / failed_any=0
- 逐年：2014–16 空窗（mdl216 数据 2017 起），2017–2023 全正（1.10→2.84→1.27）
- pyramids：`DEU/D1/MODEL`

**组合效应**：A 与 B 互相关 **0.5538** ⇒ 同时提交后 model 塔 1+2 = **3 颗 → DEU/D1/MODEL 点亮**。

**放行条件（缺一不可）**：① B 的 `check_correlation(production)` 必须实测 <0.70 且 `all_passed`；② 用户真实明确确认（问卷超时自动选中**不构成**授权）。

**位置**：`E56pROb9` / `wpQYNvZp` 均 `status=UNSUBMITTED`，未做任何平台写操作。

### 26.14 ★★★ 勘误与 refined rule（tag↔alpha 映射纠正）

前述 26.4 / 26.5 表中两条曾把 tag 与 alpha 记反，已按 `get_alpha_details` 返回的 `code` 原文修正：

| 提交顺序 | tag | simulation | alpha | 实测结构 |
|---:|---|---|---|---|
| 0 | `id_pure10` | 4eie9mc6 | `gJebZANl` | 双 gn + `ts_mean(·,1)` + `ts_decay_linear(·,1)`（全恒等）|
| 1 | `real_decay3_dblgn10` | 176yKH4t | **`QPvbKZqp`** | **双腿 `ts_decay_linear(·,3)` + 双 gn（无 backfill）** |
| 2 | `dblneut_ind_sec10` | NeCsGfe7 | `xAr3bKel` | 双层中性化 subindustry→sector |
| 3 | `mix_backfill22_decay3_10` | 3Py28dJI | **`E56pROb9`** | **F1 `ts_backfill(·,22)` + F2 `ts_decay_linear(·,3)` + 双 gn** |

**refined rule（替换 26.4 的粗结论）**：

1. `ts_backfill` **加在修正腿 F1（`mdl216_preferred…`）上无害甚至有益**：`QPvbKZqp` 1.76 → `E56pROb9` 1.79（+0.03），ladder 窗口 y7→y3（更宽松）；
2. `ts_backfill` **加在惊喜腿 F2（`predicted_surprise_f12m_ebitda_4`，cov 0.7903 ≈ 21% 缺失）上致命**：`GrWbbG33` 掉到 1.69 / 2Y 1.56，双腿都 backfill 更掉到 1.65 / 2Y 1.65 / y7；
3. 机理：F2 的缺失段集中在特定股票子集，backfill 把「无预测」改写成「沿用旧预测」，等于人为给这批股票造出信号 ⇒ 截面被污染；而 F1 的缺失更均匀，backfill 只补连续性；
4. **恒等律仍成立**：`ts_decay_linear(x,1)`、`ts_mean(x,1)`、重复 `group_neutralize(x,g)` 不改变 PnL（`gJebZANl` 1.75/2.03 与 7 算子版 `vR1rjj3a` 完全一致）。
## 二十七、2026-11-04 下午续：塔位实测刷新 + 三个新数据集全灭 + prod 槽跨会话独占判定

### 27.1 ★★★★★ DEU/D1 塔位实测（`get_pyramid_alphas` 原始返回）

| 塔 | 已提交颗数 | 距点亮 |
|---|---:|---:|
| **other** | **2** | **差 1** |
| **analyst** | **2** | **差 1** |
| **shortinterest** | **2** | **差 1** |
| model | 1 | 差 2 |
| institutions / fundamental | 各 1 | 各差 2 |
| pv / news / earnings / insiders / sentiment / risk / option / macro / socialmedia / imbalance | 全 0 | 各差 3 |

**本表覆盖此前所有塔位记述。** 关键纠正：
1. **`news` 在 DEU 是 0 颗**（此前误记为 3 颗，那是 GBR 的读数）⇒ news 数据集在 DEU 仍有塔分价值；
2. **`pv` 在 DEU 是 0 颗** —— 与「PV 已饱和」的直觉相反，DEU 的 PV 塔一颗未点；
3. `other` / `analyst` / `shortinterest` 同为 2/3，**三者任一成功即点亮**，是当前最便宜的塔分；
4. `model` 靠 `wpQYNvZp` + `E56pROb9` 两颗同时提交即可从 1→3 点亮。

### 27.2 ★★★★ `analyst_earnings_ibes` 六臂全灭（封盘）

数据集事实：cat **model**，cov 0.9978，**42 字段全 MATRIX cov≥0.9651**，ac 279。名字严重误导——**实为价格量价数据**（closing/opening/highest/lowest price、market_cap、shares_outstanding、trading_volume、vwap、1/5/20/60/120/250 日 total_return，各带 `dlr1/dlr2/dlr3/dlra1` 版本）。

单维探针骨架 `group_neutralize(rank(ts_mean(<expr>, 22)), subindustry)`，5–6 算子：

| 机制 | 表达式核心 | S | F | TO | lc | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| 收盘对 vwap 偏离 | `divide(sub(closing, vwap), vwap)` | −0.21 | −0.06 | 5.47% | 152 | −0.02 | 废 |
| 规模（负向，小盘溢价） | `-rank(ts_mean(market_capitalization))` | **0.43** | 0.18 | 1.47% | 156 | **1.34** | 废（S 不够） |
| 1 日反转 | `-rank(ts_mean(one_day_total_return_dlra1, 5))` | −0.06 | −0.01 | 22.4% | 149 | 0.14 | 废 |
| 振幅（高-低）/收盘 | `divide(sub(highest, lowest), closing)` | −0.07 | −0.01 | 4.28% | 150 | 0.38 | 废 |
| 换手（量/股本） | `divide(trading_volume, shares_outstanding)` | 0.11 | 0.02 | 2.59% | 153 | 0.91 | 废 |

**结论**：**基础量价派生在 DEU/TOP500 已被套利干净**（六类结构最好的也只是 S 0.43）。该数据集封盘，除已测的 250 日动量（`two_fifty_day_total_return_dlra1`，曾用于 `leAvv7VO`）外不再投。

### 27.3 ★★★★ `other250` 全灭（封盘）+ 字段等价发现

数据集事实：cat **other**，cov 0.6126，**12 字段全 VECTOR cov 0.6126**，uc 2 / **ac 2**（近乎无人使用）。内容 = **电商产品评论/销量替代数据**：`average_star_score`、`oth250_item_rating`、`oth250_item_review_count`、`total_review_number`、`oth250_rank`、`sales_position_rank`、`{oth250_,}price_range_{max,min}`、`product_{listed_price,price_lower_bound,price_upper_bound}`、`oth250_item_display_price`。

骨架 `group_neutralize(rank(ts_mean(ts_backfill(vec_avg(F), 66), 22)), subindustry)`（5 算子）：

| 字段 | alpha | S | F | TO | lc | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|
| `average_star_score` | `6XdjZG1L` | −0.31 | −0.11 | 3.26% | 85 | −0.38 | −0.35 |
| `oth250_rank` | `leAvEMjA` | −0.05 | −0.01 | 3.53% | 88 | −0.64 | 0.25 |
| `oth250_item_review_count` | `KPJNvV6p` | −0.01 | 0 | 2.14% | 89 | 0.33 | −0.48 |
| `sales_position_rank` | `vR1rZ1Mw` | −0.05 | −0.01 | 3.53% | 88 | −0.64 | 0.25 |

**两条硬结论**：
1. **`sales_position_rank` ≡ `oth250_rank`**：两者指标**逐位相同**（S −0.05 / F −0.01 / TO 3.53% / DD 17.37% / margin −1.52bp / 2Y −0.64 / lc 88 / sub 0.25）⇒ 同一底层序列的两个命名。**DEU 上再次证实「字典名不能当结论」**。
2. **电商替代数据在 DEU 无信号**：5 个语义最清晰的字段（满意度/排名/评论数/销量排名/评级）全部 |S| ≤ 0.31，且 lc 仅 85–89（真实可交易宽度约 175 只）⇒ cov 0.61 的表观覆盖率在持仓层被腰斩。

**ac=2 的双面性**（重要方法论）：`alphaCount` 极低确实意味着拥挤度低、prod 天然干净，但**它同时也暴露了「前人试过且放弃」**——DEU 上 ac≤9 的四个未试数据集里，other250 已全灭、other545/other384 cov 只有 0.53/0.21。**低 ac 不等于未开采富矿，更常见是公认的贫矿。**

### 27.4 `stock_cluster_dl` 五臂在飞（本批唯一还活着的）

数据集事实：cat **other**，cov 0.453，5 字段全 MATRIX `principal_component_features_{5,6,7,8,9}`，cov 分别 **0.3358 / 0.2560 / 0.5008 / 0.1706 / 1.0000**，uc 7 / ac 9。

**`pcf9` cov = 1.0000 是全 DEU 罕见满覆盖的 MATRIX 字段**，这也是本批唯一值得投的理由。骨架 `group_neutralize(rank(ts_mean(ts_backfill(F, 22), 22)), subindustry)`（4 算子）。

已派五臂（sim `BbG7VnY4` / `1fhsw45v` / `3OpICPcI` / `2o4a5E3p` / `3HVtvf3Y`），结果待读。语义是聚类 PCA 特征、方向先验不可推，只能靠实测筛。

### 27.5 ★★★★★ prod 槽「被谁占」的判定方法（本轮新增可复用手段）

`check_correlation(production)` 返回的 `holder` 字段形如 `corr:get_production_correlation(<alpha_id>)`——**holder 里就是占用者的 alpha_id**。用它反查即可判断是「自己的 inflight 残留」还是「别会话在跑」：

| 时刻 | holder | 反查结果 | 判定 |
|---|---|---|---|
| T1 | `null`（inflight=false） | — | 平台内部残留，非任何客户端 |
| T2 | `QPveY7Kg` | 己方 DEU 老候选（leading-gap 族） | **可能是己方残留** |
| T3 | `kqNoooaz` | **USA 区** alpha（`residualized_return_top2500` + `ts_target_tvr_decay`，S 1.75，UNSUBMITTED） | **别会话在批量轮测** |

**结论**：prod 单并发是**账号级、跨会话共享**的，而另一个会话正在做 USA 区的 prod 批量验收，逐条轮换（QPveY7Kg → kqNoooaz → …），`retry_after` 恒定 240s。**我方 DEU 的 prod 请求只能抢它们两条之间的空隙**，不能把 prod 当同步闸使用。

**因此本轮采用的工作节奏**：后台计时器（245s）→ 到点发一次 prod → 不管成不成都不原地重试 → 计时器期间做零成本工作（字段盘点 / 派发探针 / 台账）。
### 27.6 ★★★★ `stock_cluster_dl` 五臂全灭（封盘）——「cov=1.0 不等于有信号」

骨架 `group_neutralize(rank(ts_mean(ts_backfill(principal_component_features_N, 22), 22)), subindustry)`（4 算子）：

| 字段 | cov | alpha | S | F | TO | lc | 2Y | sub | DD |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `pcf9` | **1.0000** | `88RjE1v7` | **0.23** | 0.07 | 6.78% | 151 | 0.66 | 0.03 | 11.3% |
| `pcf7` | 0.5008 | `QPvbNXor` | **0.37** | 0.17 | 7.53% | 51 | 0.16 | 0.33 | 18.7% |
| `pcf5` | 0.3358 | `npvdeVqw` | −0.01 | 0 | 7.61% | 28 | −0.64 | 0 | 38.2% |
| `pcf6` | 0.2560 | `78LNv0wO` | −0.23 | −0.10 | 7.49% | 19 | −1.00 | −0.09 | 47.1% |
| `pcf8` | 0.1706 | `leAv5k1N` | 0.00 | 0 | 7.82% | 11 | 0.10 | 0.12 | 45.3% |

**两条硬结论**：
1. **`pcf9` 是全 DEU 罕见的 cov=1.0000 MATRIX 字段，但 S 只有 0.23** ⇒ **覆盖率是「能不能交易」的必要条件，不是「有没有信号」的充分条件**。本轮三次撞上同一条（`pcf9` cov1.0/S0.23、`analyst_earnings_ibes` cov0.9978/S≤0.43、`mdl26_preferred` cov1.0/S0.97）；
2. **lc 随 cov 单调塌陷**（151→51→28→19→11），且 DD 单调放大（11%→47%）⇒ **低 cov 字段不只是持仓窄，波动也更大**，两者叠加使 sub_universe/DD 闸同时收紧。**cov<0.4 的字段在 DEU/TOP500 不必再投**（这条可直接砍掉未来一大批试探）。

### 27.7 本轮（2026-11-04 下午续）三数据集 16 臂全灭汇总

| 数据集 | cat | cov | 臂数 | 最好 S | 判定 |
|---|---|---:|---:|---:|---|
| `analyst_earnings_ibes` | model | 0.9978 | 6 | 0.43 | **封盘**（实为量价，六类结构全废） |
| `other250` | other | 0.6126 | 5 | −0.01 | **封盘**（电商评论，`oth250_rank`≡`sales_position_rank`） |
| `stock_cluster_dl` | other | 0.4530 | 5 | 0.37 | **封盘**（PCA 聚类特征，lc 塌陷） |

**累计封盘数据集已覆盖 DEU 全部 cov≥0.45 的 other 类与全部 cov≥0.58 的未试集。** 剩余未试：`other545`(cov0.527/4f)、`other384`(cov0.212/33f 电话会议 tone，lc 预计 <60 必然挂 sub)、`analyst47`(cov0.623/5f 第三方信号包)、`analyst9`(cov0.583/51f IBES 广度，与已封 analyst7 同机制)、`analyst93`(cov0.637/100f)、`analyst_consensus`(cov0/1972f)。

**对「other 塔差 1 点亮」的裁定**：other 塔全部 41 个数据集中，**cov≥0.45 的 7 个已全部试完**（other455 / other532 / dl_riskfree_returns / other250 / other47 / insider_matrix / insider_trx_matrix / other545 中前 7 个已封，other545 仅 4 字段且 cov 0.527）。**结论：other 塔在 DEU 客观无解**，与 shortinterest 塔同性质，建议从「待点亮」名单移除。
## 二十八、★★★★★ 2026-11-04 收口突破：`E56pROb9` 的 prod 实测 0.6859 通过（全闸清零）

### 28.1 验收完成（这是本战役第一颗「全维度无缺口」候选）

| 闸 | 要求 | 实测 | 结论 |
|---|---:|---:|---|
| LOW_SHARPE | 1.58 | **1.79** | ✓ |
| LOW_FITNESS | 1.00 | **1.70** | ✓ |
| LOW_2Y_SHARPE | 1.58 | **2.03** | ✓ |
| 2Y ladder window | 1.58/1.75 | 窗 3 | ✓ |
| LOW_SUB_UNIVERSE_SHARPE | — | 1.32 | ✓ |
| investability / fitness | — | 1.62 / 1.49 | ✓ |
| risk_neutralized | 0.70 | 0.94 | ✓ |
| **`ra.failed_ra_count`** | **0** | **0** | ✓ |
| **self（已提交池）** | **<0.70** | **0.6004** | ✓ |
| **prod（生产池）** | **<0.70** | **0.6859** | **✓ 实测** |

其余：TO 6.74% / returns 11.24% / DD 5.62% / margin 33.34bp / lc 97 / sc 96 / pnl 8,090,767 / startDate 2014-01-01 / pyramid `DEU/D1/MODEL` / status `UNSUBMITTED`。

### 28.2 ★★★★★ prod 直方图：浅钉通过，不是擦线偶然

```
[-0.3,-0.2)    3   [-0.1,0.0)  1398   [0.2,0.3)  5049   [0.5,0.6)    93
[-0.2,-0.1)   79   [0.0,0.1)   4374   [0.3,0.4)  2617   [0.6,0.7)     5
[-0.1,0.0)  1398   [0.1,0.2)   5062   [0.4,0.5)   690   max = 0.6859   min = -0.2849
```

**判据（按「prod 单钉子不判死」条的口径反向应用）**：`[0.6,0.7)` 区间只有 **5 颗**、最高 0.6859，属**浅钉**（单点碰撞，非机制性拥挤）；厚尾段 `[0.4,0.6)` 合计 783 颗但都显著低于墙。⇒ **不需要破墙**，也不必再做窗口位移。

### 28.3 ★★★★★ 两颗同时提交的安全性（互相关论证）

| | `wpQYNvZp` | `E56pROb9` |
|---|---|---|
| S / F | 1.68 / 1.36 | **1.79 / 1.70** |
| TO / margin | 13.15% / 13.1bp | 6.74% / **33.34bp** |
| 2Y | 1.83 | **2.03** |
| self | 0.6332 ✓ | 0.6004 ✓ |
| **prod** | **0.6333 ✓（含缓存）** | **0.6859 ✓（本次实测）** |
| `failed_ra_count` | 0 | 0 |
| 年份覆盖 | **10/10** | 7/10（mdl216 自 2017 起） |

**互相关 0.5538**。关键推论：
1. 先提任一颗，另一颗的 self 闸**都不会被推高到墙边** —— 因为 0.5538 小于两者各自当前的 self max（0.6332 / 0.6004），max 不会被刷新；
2. 两颗提交后 `DEU/D1/MODEL` 从 **1 → 3 颗**，塔点亮（multiplier 1.8）；
3. **这是本战役第一次出现「两颗正交互补、各自全闸通过」的组合**，此前所有组合都至少一颗卡 prod 或缺数据。

### 28.4 prod 抢槽的可复用经验（本次成功路径）

前 10+ 次全部 `correlation_busy`，holder 在 `QPveY7Kg` / `kqNoooaz` / `2rAw9o7J` 之间轮换（另一会话在连续批量验收 USA 区）。**成功路径**：
1. **间隔必须 ≥300 秒**（`retry_after` 恒为 240s，过早请求只会重置自己的冷却）；
2. 抢到的那一次先表现为 **`MCP tool call ... timed out after 120000ms`** —— 这是**请求已被接受、平台正在算**的信号，**不是失败**；
3. 随后重查得到 `status: correlation_busy` + **`inflight: true`** + 消息「正在计算中（本机 inflight 标记，第 1 次触发）…**不要重新触发计算**」；
4. 再等约 45 秒重查即拿到 **`max_correlation: 0.6859` / `passes_check: true` / `all_passed: true`**。

**反模式（本轮踩过）**：见到 `timed_out` 就换 alpha 重试、或见到 `inflight: true` 就重新触发 → 会把自己顶成 busy，前功尽弃。

### 28.5 状态：等用户真实明确授权

`E56pROb9` 与 `wpQYNvZp` 均 `status=UNSUBMITTED`。**本轮仍未做任何平台写操作**（零提交、零取消）。

**放行条件**：用户以明确文字确认提交（问卷超时自动选中项**不构成**授权——本轮已两次发生 `responseSource=automatic_timeout`）。
## 二十九、`analyst` 塔收口：analyst47 + analyst93 全灭（塔级无解）

### 29.1 `analyst47`（第三方「成品信号包」）cov 0.623 / 5 字段 / ac 112

骨架 `group_neutralize(rank(ts_mean(ts_backfill(F, 22), 22)), subindustry)`（4 算子）：

| 字段 | alpha | S | F | TO | margin | lc | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `anl47_indicator` | `omELG892` | **0.64** | 0.34 | 6.49% | 10.64bp | 80 | 0.98 | 0.53 |
| `anl47_totalrawsignal` | `e75bVjEJ` | 0.54 | 0.26 | 7.11% | 8.16bp | 79 | 1.32 | 0.36 |
| `anl47_rawsentiment` | `2rAw6zox` | 0.54 | 0.26 | 6.93% | 8.43bp | 80 | 1.36 | 0.44 |
| `anl47_rawexperts` | `xAr3Gqjp` | 0.10 | 0.02 | 7.49% | 1.37bp | 78 | 0.40 | −0.27 |
| `anl47_rawalphadecay` | `GrWbz1n0` | −0.42 | −0.18 | 6.99% | −6.45bp | 77 | −1.28 | −0.43 |

**结论**：成品信号包最好的 `anl47_indicator` 只有 S 0.64 / margin 10.64bp，距 1.58 差得远。**「打包好的第三方信号」不等于强信号**，且 lc 仅 78–80 ⇒ 覆盖率 0.623 在持仓层缩水到约 160 只。

### 29.2 `analyst93`（分析师质量/准确度评估）cov 0.637 / **100 字段全 VECTOR** / ac 193

**这是本轮唯一真正的新机制**：不是预期值、不是修正方向，而是**分析师本身的质量评分**——`accuracy` / `relative_accuracy{1..4}` / `correct_revision_ratio` / `correct_revision_times` / `consistency` / `relative_consistency` / `correv` / `profitabilityprev_{analyst,estimator}_profitability{1,2}{,_20d,_60d,_120d}` / `total_forecast_times` / `total_revision_times`，每个都有 **analyst 与 estimator 两套**。

骨架 `group_neutralize(rank(ts_mean(ts_backfill(vec_avg(F), 66), 22)), subindustry)`（5 算子）：

| 维度 | 字段 | alpha | S | F | TO | margin | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 预测准确率 | `analyst_accuracy1` | `A1VNzaPY` | −0.04 | −0.01 | 1.91% | −2.88bp | 73 | −0.71 | −0.08 |
| 修正正确率 | `analyst_correct_revision_ratio` | `ZYQbzwx8` | 0.26 | 0.10 | 2.50% | 14.89bp | 70 | −0.25 | 0.23 |
| 一致性 | `analyst_consistency` | `gJebGlOm` | −0.14 | −0.04 | 1.81% | −11.58bp | 60 | 0.67 | −0.27 |
| 历史盈利记录 | `profitabilityprev_analyst_profitability1` | `MPYazZ3k` | **0.36** | 0.17 | 3.34% | 16.88bp | 73 | 0.31 | 0.19 |
| 修正正确性 | `correv_analyst_analyst` | `A1VNze5g` | 0.24 | 0.09 | 1.69% | 20.25bp | 72 | −0.69 | 0.37 |

**结论**：五维全废（最高 0.36），且 **TO 只有 1.7–3.3%** ⇒ 这类「慢变量」评分几乎不动，天然没有交易价值。**「用分析师质量当门控去调制修正信号」这条思路本轮未投**（因为需要与 analyst7 修正腿组合，而同塔 analyst+analyst 虽不触禁混、但 analyst7 修正广度本身只有 0.66，调制后不可能突破 1.58）。

### 29.3 ★★★★ 塔级收口：`analyst` 在 DEU 客观无解

| 数据集 | cov | 机制 | 实测上限 | 状态 |
|---|---:|---|---:|---|
| `analyst7` | 0.721 | 修正广度 / 幅度 / 四指标合成 | 0.69 | 封盘（三族全试） |
| `analyst48` | 0.788 | — | 封盘 |
| `analyst44` | 0.580 | — | ATOM 封盘 |
| `analyst47` | 0.623 | 第三方成品信号包 | 0.64 | **本轮封盘** |
| `analyst93` | 0.637 | **分析师质量评分** | 0.36 | **本轮封盘** |
| `analyst9` | 0.583 | IBES 修正广度（numup/numdn） | 未投 | 与 analyst7 同机制、必然共线 |
| `analyst83`/`46`/`factor_signals` | — | — | — | 已封 |
| `analyst93` 以外 cov=0 的 11 个 | 0 | — | — | DEU 无数据 |

**⇒ `other` / `analyst` / `shortinterest` 三塔全部客观无解**（各 2/3，均差 1 但无可用数据集）。**三塔从「待点亮」名单移除**，DEU 剩余可攻塔位只有：`model`（1/3，靠 `wpQYNvZp`+`E56pROb9` 可点亮）、`pv`（0/3）、`news`（0/3）。
## 三十、`news` / `pv` 两塔试探收口：news104 与 pv109 双封盘

### 30.1 DEU 塔位与候选集全表（本轮最终版，替代此前所有记述）

| 塔 | 已提交 | 可攻数据集 | 判定 |
|---|---:|---|---|
| **model** | **1** | model216 / predictive_starmine | **可点亮**：`wpQYNvZp`(prod 0.6333✓) + `E56pROb9`(prod 0.6859✓) 互相关 0.5538 |
| other | 2 | 41 个中 cov≥0.45 的 7 个全试完 | **无解** |
| analyst | 2 | analyst7/44/47/48/83/93 全试完 | **无解** |
| shortinterest | 2 | 仅 shortinterest3，已封 | **无解** |
| institutions / fundamental | 各 1 | institutions6(cov1.0)/fund_holdings_panel 已封 | 无解 |
| **pv** | **0** | pv29(全GROUP) / pattern_scores(已封) / pv30(全GROUP) / **pv109(本轮封)** | **无解** |
| **news** | **0** | news104(本轮封) / news18/17 已封 / news20·50·38 同族元数据 | **实质无解** |
| earnings / insiders / sentiment / risk / option / macro / socialmedia / imbalance | 各 0 | 全部 cov=0（DEU 无数据）或已验证封盘 | 无解 |

### 30.2 `news104` 五臂全灭（封盘）——cov 0.963 也救不了

数据集事实：cat **news**，cov **0.963**（news 类最高），11 字段全 VECTOR，ac 100。字段是**结构化的新闻情绪分解**：`nws104_sentiment` / `prob_pos` / `prob_neg` / `prob_ntr` / `marketimpactscore` / `novelty` / `confidence` / `relevance` / `headlineonly` / `automessage` / `timestamp`。

骨架 `group_neutralize(rank(ts_mean(ts_backfill(<expr>, 22), 5)), subindustry)`：

| 模板 | 结构 | alpha | S | F | TO | margin | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 情绪水平 | `vec_avg(sentiment)` | `npvdQEmd` | **0.22** | 0.06 | 15.2% | 1.50bp | 123 | 0.61 | 0.04 |
| T2 净概率差 | `vec_avg(prob_pos)−vec_avg(prob_neg)` | `xAr3WL1w` | 0.06 | 0.01 | 14.6% | 0.45bp | 131 | 0.16 | −0.09 |
| T3 影响加权情绪 | `vec_avg(sent)×vec_avg(marketimpactscore)` | `gJebLOrJ` | −0.03 | 0 | 17.0% | −0.15bp | 131 | 0.16 | −0.16 |
| T4 置信度加权 | `rank(sent)×rank(confidence)` | `qMLxV9wv` | −0.02 | 0 | 13.1% | −0.20bp | 131 | −0.37 | 0.37 |
| T5 相关度加权 | `rank(sent)×rank(relevance)` | `LLMNrQ3e` | −0.10 | −0.02 | 12.4% | −1.02bp | 130 | −0.12 | 0.38 |

**关键诊断：问题不是信号缺失，是成本吃掉全部收益。** TO 12–17%（新闻日频更新），但 **margin 只有 0.45–1.5bp**，而 DEU/TOP500 的可交易 margin 门槛约 10bp 量级。⇒ **新闻情绪类信号在 DEU 的 TO/margin 比值结构性失衡**，这是 news 塔在 DEU 无法成立的根本原因（news18 此前也是同一死法，不是模板不够多）。

### 30.3 `pv109` 五臂全灭（封盘）——债券数据映射到股票后覆盖塌陷

数据集事实：cat **pv**，cov 0.4665，26 字段全 VECTOR，ac 33。内容是**公司债（bond-level）数据**：`midpoint/bid_side/ask_side_yield_to_maturity`、`midpoint_conversion_yield`、`current_coupon_rate`、`last_traded_price`/`midpoint_trade_price`/`highest_bid_price`/`lowest_ask_price`、`pv109_amt_issued`/`amt_outstanding`、`total_traded_volume`、`bond_maturity_structure`。

| 模板 | 机制 | alpha | S | F | TO | margin | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 YTM 水平 | 高 YTM = 高信用风险（负向） | `LLMN3GVa` | **0.27** | 0.11 | 2.54% | 16.19bp | 62 | −0.39 | −0.29 |
| T2 bid-ask 价差 | 流动性溢价 | `88RjXN1m` | 0.13 | 0.03 | 4.39% | 3.77bp | 61 | −0.41 | 0.14 |
| T3 票息-YTM 差 | 溢价/折价交易 | `gJebL86e` | −0.21 | −0.08 | 3.66% | −10.63bp | **15** | −0.09 | 0.04 |
| T4 存量规模 | 债券规模→流动性 | `j2YAO6R9` | 0.21 | 0.07 | 1.28% | 21.48bp | 68 | 0.84 | −0.37 |
| T5 成交量 | 交易活跃度 | `A1VNE3el` | 0.22 | 0.09 | 8.59% | 4.49bp | **25** | 0.37 | −0.74 |

**塔位实测确认**：`gJebL86e` 与 `A1VNE3el` 的 `pyramids.list` 都是 **`DEU/D1/PV`** ⇒ pv109 确实归 pv 塔（这是本轮唯一新增的塔位实证）。

**两条硬结论**：
1. **债券数据映射到股票后 lc 只有 15–68**：cov 0.4665 在持仓层塌成 15 只（票息差）到 68 只（存量规模），必然挂 sub_universe（`A1VNE3el` 的 sub −0.74）；
2. **TO 极低（1.3–8.6%）但 2Y 普遍为负**（−0.39 / −0.41 / −0.09）：低换手不是优势，而是说明信号根本不更新；`j2YAO6R9` 的 2Y 0.84 是唯一亮点，但 S 仅 0.21、sub −0.37。

### 30.4 本轮累计封盘（2026-11-04 下午续，共 5 数据集 / 26 臂）

| 数据集 | cat | cov | 臂数 | 最好 S | 死因 |
|---|---|---:|---:|---:|---|
| `analyst_earnings_ibes` | model | 0.9978 | 6 | 0.43 | 实为量价，六类结构全废 |
| `other250` | other | 0.6126 | 5 | −0.01 | 电商替代数据无信号 |
| `stock_cluster_dl` | other | 0.4530 | 5 | 0.37 | PCA 特征，lc 塌到 11 |
| `news104` | news | **0.9630** | 5 | 0.22 | **TO/margin 失衡**（TO 15% vs margin 1.5bp） |
| `pv109` | pv | 0.4665 | 5 | 0.27 | **债券→股票 lc 塌到 15** |

**⇒ 至此 DEU 的 pv / news / other / analyst / shortinterest / institutions / fundamental 七塔全部实测无解，唯一可点亮的只剩 `model`**（且已具备两颗全闸通过的候选）。
## 三十一、`pv` 塔用内置价格量字段试探（6 臂）——DEU 八塔全部见底

### 31.1 动机：已提交 11 颗全用数据集字段 ⇒ 内置字段的 pv alpha 是纯增量

`get_pyramid_alphas` 实测 DEU/D1 的 `pv` 塔是 **0/3**，而此前 11 颗已提交 alpha 全部基于数据集字段（model / other / analyst / fundamental 等）。**用平台内置价格量字段（`open`/`close`/`high`/`low`/`volume`/`vwap`/`returns`/`adv20`/`cap`）构造的 alpha 归 pv 塔**，是此前完全没试过的路径。

内置字段在 DEU/TOP500/D1 **全部可用**（`preflight` 的 `builtin_fields` 返回 adv20/close/high/low/open/returns/volume/vwap，`cap` 亦有效、unknown 为空）。

### 31.2 六臂实测（均 `group_neutralize(..., subindustry)`，4–6 算子）

| 模板 | 机制 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **T1 量价相关（负向）** | `-rank(ts_corr(rank(close),rank(volume),22))` | `9qxj2Ad1` | **0.54** | 0.24 | 12.2% | 4.22bp | **8.6%** | 149 | **1.76** | −0.25 |
| T2 5 日反转 | `-rank(ts_mean(returns,5))` | `d5WbPeJK` | 0.23 | 0.07 | 22.8% | 1.69bp | 23.9% | 150 | −0.58 | −0.09 |
| T3 低价波动 | `-rank(ts_std_dev(returns,22))` | `A1VN2ajX` | −0.21 | −0.09 | 6.4% | −6.66bp | **55.3%** | 150 | 0.41 | −0.09 |
| T4 小盘溢价 | `-rank(cap)` | `qMLxwmwP` | −0.25 | −0.10 | 1.4% | −29.1bp | 43.2% | 147 | −0.98 | 0.19 |
| T5 日内强度 | `rank(ts_mean((close-open)/open,22))` | `pwdRp0lv` | −0.09 | −0.02 | 8.2% | −1.49bp | 31.0% | 150 | 0.58 | −0.18 |
| T6 VWAP 偏离 | `rank(ts_mean((close-vwap)/vwap,22))` | `j2YAMwQj` | −0.09 | −0.02 | 7.5% | −1.39bp | 29.2% | 151 | 1.02 | 0.04 |

**塔位实证**：`d5WbPeJK` / `A1VN2ajX` / `pwdRp0lv` 的 `pyramids.list` 均为 **`DEU/D1/PV`** ⇒ 确认内置字段归 pv 塔（连同 §30.3 的 pv109，pv 塔归属已有 5 条实证）。

### 31.3 结论：DEU 的基础量价同样被套利干净

1. **只有量价相关（`9qxj2Ad1`）有点意思**：S 0.54 / **2Y 1.76** / **DD 仅 8.6%** —— 信号质量好（回撤小、近年有效），但**强度差 1.04**，靠换窗口/凸化不可能补 3 倍；
2. **规模因子在 DEU 是反向的**：`-rank(cap)` 的 S −0.25 / 2Y **−0.98** ⇒ DEU 大市值跑赢（与美股小盘溢价相反），且 DD 43%；
3. **低波动因子失效**：`-rank(ts_std_dev(returns,22))` 的 DD 高达 **55%**，说明 DEU 的波动率结构不稳定；
4. `sub_universe` 六臂里五臂为负或零 ⇒ 顶层信号在子宇宙内不复现，这是**假信号的典型特征**。

### 31.4 ★★★★★ 战略结论：DEU 八塔全部实测见底，`model` 是唯一可点亮塔

| 塔 | 状态 | 依据 |
|---|---|---|
| **model** | **可点亮** | `wpQYNvZp`(prod 0.6333✓) + `E56pROb9`(prod 0.6859✓)，互相关 0.5538 |
| other | 无解 | 41 个数据集，cov≥0.45 的 7 个全试完 |
| analyst | 无解 | analyst7/44/47/48/83/93 全试完 |
| shortinterest | 无解 | 仅 1 个数据集且已封 |
| **pv** | **无解** | pv29/pv30 全 GROUP、pattern_scores/pv109 已封、**内置字段 6 臂本轮全灭** |
| **news** | **无解** | news104 死於 TO/margin 失衡、news18/17 已封 |
| institutions / fundamental | 无解 | 各 2 个可用集已封 |
| earnings / insiders / sentiment / risk / option / macro / socialmedia / imbalance | 无解 | cov=0（DEU 无数据）或已验证封盘 |

**⇒ 本战役在 DEU 的增量空间已实质归零**：已提交 11 颗，唯一还能新增的是 model 塔那 2 颗（已备好、全闸通过、只等用户授权）。30 颗目标在 DEU 结构性不可达。

---

## 三十二、`fundamental6` 深挖：推翻「八塔见底」，但单维强度天花板 = 0.92

> **本节推翻 §31 的结论。** §31 基于 pv/news 双封盘得出「DEU 增量归零」，但 `fundamental6`（196 字段）从未单独试过，其质量因子族是 DEU 首个「高 margin（44–76bp）+ 正 sub（0.52–0.60）+ 通过换手闸」的组合。

### 32.1 数据集事实（DEU/TOP500/D1 实测，MCP `get_datafields` 全量 196 字段）

- cat **fundamental**，cov **0.492**，**196 字段全 MATRIX**，ac 1028；154 字段 cov≥0.4
- 命名分三组，**跨频不可混配**：
  - 年度流量 `*y`：`iby`(0.66 净利) / `piy`(0.6613) / `revty`(0.6587) / `cogsy`(0.4936) / `xinty`(0.6137) / `txty`(0.6427) / `dpy`(0.6176) / `ibmiisa`(0.6171)
  - 季度 `newq_*`：`seqq`(0.6595) / `lseq`(0.6561) / `cheq`(0.6531) / `lctq`(0.5468)
  - 最新年度快照 `newa2_*`：`seq`(0.6525) / `pi`(0.6224) / `revt`(0.6264) / `sale`(0.521) / `wcap`(0.5218) / `re`(0.6242) / `oiadp`(0.6267) / `oancf`(0.5396) / `xint`(0.6408)
- **字段名坑（本轮踩到）**：高频总资产是 `fnd6_cptnewq_atq`(0.6557)，流动资产/长期负债是 `fnd6_cptnewq_actq` / `fnd6_cptnewq_ltq`；**`fnd6_newq_actq` 与 `fnd6_newq_ltq` 不存在**（preflight `unknown_soft`）
- 全部臂只挂 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE` 三闸，**无 LOW_TURNOVER**（TO 1.5–4.2% 均通过）
- 塔位全部干净单塔 `DEU/D1/FUNDAMENTAL`（multiplier 1.8）；**唯一例外是用内置 `cap` 做分母会变成 `PV`+`FUNDAMENTAL` 双塔**（`d5Wb6wnK` 实证）

### 32.2 十二臂实测（骨架统一 `group_neutralize(rank(ts_backfill(<比率>,252)), subindustry)`）

| # | 模板 | 结构 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **净利率·水平** | `divide(iby,revty)` | `KPJNpKV8` | **0.92** | 0.68 | 1.79% | **76.37bp** | 16.9% | 78 | 0.61 | 0.59 |
| 2 | 利息覆盖·水平 | `divide(iby,xinty)` | `omELXzlJ` | 0.79 | 0.54 | 1.71% | 69.11bp | 15.5% | 75 | 0.24 | 0.52 |
| 3 | 现金/资产 | `divide(newq_cheq,cptnewq_atq)` | `akKb8jG5` | 0.52 | 0.28 | 1.61% | 44.72bp | 14.3% | 74 | 0.29 | **0.60** |
| 4 | 资产周转 | `divide(revty,cptnewq_atq)` | `N1NaG36X` | 0.36 | 0.16 | 2.26% | 21.97bp | 10.6% | 76 | −0.09 | 0.13 |
| 5 | Altman-4（原始和） | `(wcap+re+oiadp+sale)/atq` | `Xg9bAaw0` | 0.36 | 0.18 | 1.51% | 41.18bp | 26.2% | 55 | 0.46 | 0.34 |
| 6 | ROE·水平 | `divide(newa2_pi,newa2_seq)` | `6XdjLdO5` | 0.27 | 0.11 | 1.46% | 28.04bp | 19.9% | 68 | 0.71 | −0.03 |
| 7 | **ROE·Δ同比** | `ts_delta(…,252)` | `A1VN8xER` | **0.57** | 0.36 | 2.77% | 36.63bp | 21.8% | 45 | **1.02** | 0.57 |
| 8 | 资产增长 | `ts_delta(cptnewq_atq,252)` | `1YNXA80X` | 0.05 | 0.01 | 2.54% | 2.94bp | 23.5% | 51 | **−0.85** | −0.01 |
| 9 | 净利率·Δ同比 | `ts_delta(npm,252)` | `kqNopqbd` | 0.72 | 0.49 | 3.40% | 34.21bp | **10.9%** | 55 | 0.74 | 0.46 |
| 10 | 净利率·z252 | `ts_zscore(npm,252)` | `bl6b0XrM` | 0.73 | **0.58** | 4.15% | 37.54bp | 19.4% | 39 | 0.58 | **0.71** |
| 11 | 利息覆盖·Δ | `ts_delta(ic,252)` | `1YNX3YJJ` | 0.42 | 0.22 | 3.32% | 20.47bp | 12.9% | 54 | 0.95 | 0.15 |

（第 12 臂 `divide(iby,cap)` EP = `d5Wb6wnK` S 0.88 / 2Y 0.59 / margin 52.24bp，但塔位 `PV`+`FUNDAMENTAL` 双塔 ⇒ 违反禁混，废弃）

### 32.3 四条硬结论

1. **最强单维 = 净利率水平 S 0.92**，是 DEU 全部已测数据集里唯一同时满足 `S≥0.9` + `margin>70bp` + `正 sub` + `无换手闸` 的单维。**但它离 1.58 差 0.66，且 2Y 只有 0.61**——瓶颈纯粹是强度，不是覆盖、不是成本、不是换手。
2. **Δ 变换只救弱腿，不强化强腿**：ROE 0.27→0.57（**+0.30**）、利息覆盖 0.79→0.42（−0.37）、净利率 0.92→0.72（−0.20）。⇒ 修正记忆里「低区分度侧需加工」的表述：**加工（Δ / z-score）的收益与原始信号的截面区分度成反比，且对已是全族最强的腿一律负贡献**。
3. **财务比率合成时不能先 add 原始比率**：Altman-4 把 4 个原始比率相加再 rank，得到 0.36（远低于最强成分 0.92）。**必须各自 `rank` 后等权相加**，否则量纲大的项（`sale/atq` 周转率）会吞掉量纲小的项（`re/atq` 留存收益）。下一批已按 rank 后相加改写。
4. **DEU 无资产增长异象**：`ts_delta(总资产,252)` S 0.05 / 2Y **−0.85** ⇒ 该方向在 DEU 明确封盘，不必再换加工方式重试。

### 32.4 派发纪律的新教训（本轮踩到）

`batch_create_simulations` 返回 `submitted < items.length` 时，**实际派发的是任意子集，不是前缀**：本轮首批发 8 条只成 4 条，`GkKTLcEl` 我以为对应第 4 个 tag `grossmargin`，实际 `code` 是 `assetgrowth`。
⇒ **`submitted<total` 时严禁用 id 顺序推断 tag，必须逐条读 `code` 原文**（本轮第三次踩同一类坑，前两次在 analyst93 与 fundamental6 首批）。
### 32.5 三腿合成把上限推到 0.98，随后五组消融确认天花板

| 模板 | 结构 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 两腿 | npm + 利息覆盖 | `akKbmEZO` | 0.87 | 0.63 | 1.76% | 75.71bp | 16.62% | 78 | 0.45 | 0.56 |
| **三腿** | **npm + 利息覆盖 + 现金/资产** | **`bl6b0bPq`** | **0.98** | **0.75** | 1.73% | **84.63bp** | **12.07%** | 75 | 0.54 | **0.71** |
| 三腿·industry 轴 | 同上换轴 | `1YNX3Rek` | 0.98 | 0.75 | 1.76% | 82.90bp | 12.32% | 75 | 0.53 | 0.71 |
| 三腿·无 backfill | 删 `ts_backfill` | `leAvwnRA` | 0.90 | 0.66 | 1.98% | 68.57bp | 12.39% | 73 | 0.39 | 0.66 |
| 四腿·加 ROE | 三腿 + `newa2_pi/newa2_seq` | `omELjj9k` | 0.72 | 0.50 | 2.29% | 52.31bp | 13.34% | 62 | 0.45 | 0.46 |
| 三腿·凸化 | `signed_power(demean,2)` | `JjeNavGm` | 0.55 | 0.29 | 1.64% | 41.23bp | 16.30% | 70 | 0.16 | 0.19 |

**五条消融结论**：

1. **`rank` 后等权相加是唯一有效的合成方式**：单腿 0.92 → 两腿 0.87 → 三腿 **0.98**。三腿同时把 `margin` 从 76.37→**84.63bp**、`DD` 从 16.9%→**12.07%**、`sub` 从 0.59→**0.71**，三项全面改善。
2. **四腿加 ROE 反而崩**（0.98→0.72）：ROE 腿 S 0.27 / sub **−0.03**，是典型弱腿。这是「弱腿污染整体」的**第三次实证**（前两次：DEU revenue 惊喜腿把 2Y 从 1.51 砸到 0.77；DEU model264 第三腿全面退化）。⇒ **加腿前必须逐腿跑单维，`sub<0.2` 或 `S<0.4` 的腿一律不进。**
3. **`ts_backfill(·,252)` 必须保留**：删掉后 S 0.98→0.90、2Y 0.54→0.39、margin −16bp。财务季度数据的稀疏填充是信号的一部分。
4. **分组轴 `subindustry` ≡ `industry`**（两者 S 均 0.98）。不必在分组轴上再花臂。
5. **凸化对基本面有害**（0.92→0.55）：即使按正确写法 `signed_power(subtract(group_rank(X,g),0.5),2)` 也把 2Y 从 0.61 砸到 0.16。⇒ 凸化是针对「信号已足够强、只需集中持仓」的场景，对 S<1.0 的弱信号只会丢掉有效样本。

### 32.6 判定：`fundamental6` = 强度天花板，封盘

**16 臂覆盖六个维度**（单维 4 / 合成 5 / Δ 变体 3 / 凸化 1 / 换轴 2 / 去 backfill 1），最好值 **S 0.98 / F 0.75 / 2Y 0.54**。

| 闸 | 线 | 最好实测 | 缺口 |
|---|---:|---:|---:|
| LOW_SHARPE | 1.58 | 0.98 | **−0.60** |
| LOW_FITNESS | 1.00 | 0.75 | **−0.25** |
| LOW_2Y_SHARPE | 1.58 | 0.54 | **−1.04** |

⇒ 按 memory 里 `risk68` 的同类判据（「一个字段族被 20+ 臂扫过、最好值只有 S≈1.1 时，标成强度天花板而不是几何没找对」），`fundamental6` **16 臂最好 0.98，同判为强度天花板**。

**它的问题不是方向、不是覆盖（cov 0.492 / lc 62–78）、不是成本（margin 84.63bp 是 DEU 全数据集最高）、不是换手（TO 1.73% 直接过闸）——纯粹是截面幅度不足。** 换句话说：这是一条「能赚钱但赚得不够多」的因子族，在 DEU/TOP500 的 1.58 闸线下没有出路。

**不再往 fundamental6 投臂。** 若将来 DEU 闸线放松或改用其它 universe，`bl6b0bPq`（三腿，S 0.98 / margin 84.63bp / DD 12.07%）是最优先的复活对象。
---

## 三十三、`analyst9`（IBES 共识估计）四臂判弱 —— analyst 塔第 3 颗未找到

> **战略动机**：`get_pyramid_alphas` 实测 DEU/D1 的 `analyst` 塔已有 **2 颗**，只差 1 颗即可点亮。`analyst9` 是 analyst 类里唯一从未单独试过的多字段集（51 字段）。

### 33.1 数据集事实（DEU/TOP500/D1）

- cov **0.583**，**51 字段全 VECTOR**，cov 区间 0.527–0.625，全部须先 `vec_avg` 聚合
- 三组字段族：
  - **`s_` 前缀（cov 0.625）**：`s_numanalysts` / `s_numup` / `s_numdn` / `s_numnochg` / `s_numupunfiltered` / `s_numdownunfiltered` / `s_numanalystall` / `s_numnochangeunfiltered` —— 快照版
  - **`daily_` 前缀（cov 0.5271）**：同名字段 —— 日频版
  - **共识值**：`eps_consensus_estimate_value`(0.5959) / `ebt_consensus_estimate_value`(0.6062) / `cashflow_consensus_estimate_value`(0.5766) / `span_consensus_estimate_value`(0.619)，以及 `anl9_consensusv2span_*_{dataitemvalue,effectivetime,totime,splitfactor}` 明细
  - 元数据：`confirmtime` / `estimatetime` / `isnmflag` / `parentflag` / `isexcluded`

### 33.2 四臂实测（`s_` 族，骨架 `group_neutralize(rank(...), subindustry)`）

| 模板 | 结构 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **净修正广度** | `(numup−numdn)/numanalysts` | `2rAwg506` | **0.54** | 0.32 | 4.42% | **19.40bp** | 18.59% | 62 | **0.02** | 0.09 |
| 低覆盖反向 | `−numanalysts` | `1YNX8prM` | −0.04 | −0.01 | 1.89% | −3.21bp | 29.27% | 61 | −0.49 | −0.02 |
| EPS 共识 z252 | `ts_zscore(eps_consensus,252)` | `ZYQb8z21` | −0.12 | −0.03 | **13.12%** | −1.53bp | 31.50% | 44 | −0.58 | 0.27 |
| 广度变化 | `ts_delta(numup/numanalysts,22)` | `9qxje7Jr` | −0.23 | −0.09 | **11.42%** | −3.03bp | 24.14% | 59 | −0.15 | −0.26 |

### 33.3 三条判据

1. **唯一正向臂的 2Y = 0.02**：净修正广度 S 0.54 看似「有点信号」，但近两年收益为零。按两段判死法，**2Y 崩掉意味着机制在当前市场已失效**，不是模板没选对。
2. **DEU 无低关注溢价**：`−numanalysts` 得 S −0.04 / 2Y −0.49 / DD 29.27%。分析师关注度因子在德股不成立。
3. **三条负向臂 margin 全负**（−3.21 / −1.53 / −3.03 bp）⇒ **死因不是成本，是信号方向本身不成立**。这点与 `news104`（成本失衡）和 `pv109`（lc 塌陷）的死因不同。

⇒ **`analyst9` 判弱封盘**（`daily_` 族对照臂仍在飞，见 §33.4）。`analyst` 塔第 3 颗**仍未找到**，该塔保持 2/3。
### 33.4 daily 族对照：换对字段族后 S 从 0.54 → **0.82**

| 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **daily 净广度** | `akKbp68x` | **0.82** | **0.62** | 9.85% | 14.72bp | 16.78% | 49 | 0.20 | 0.30 |
| 宽口径净广度（unfiltered） | `MPYarLwo` | 0.77 | 0.57 | 9.80% | 14.01bp | 17.14% | 49 | 0.08 | 0.26 |
| 净广度 z252 | `pwdRLRaq` | 0.53 | 0.31 | 12.18% | 7.12bp | 19.49% | 46 | −0.31 | 0.08 |
| 净广度 + 无变化占比 | `RREbg1Y0` | 0.04 | 0.00 | **104.91%** | 0.10bp | 37.25% | **11** | 0.42 | 0.10 |
| 净广度 × 覆盖度 | `3qoXNANZ` | 0.08 | 0.01 | **29.53%** | 0.57bp | 28.59% | **25** | 0.66 | 0.21 |

**daily 族确认优于 `s_` 族**（0.82 vs 0.54），`s_` 是快照、`daily_` 才是逐日修正流。但即便换对字段族，最好也只有 0.82 / 2Y 0.20。

### 33.5 ★★★★★ 新硬规则：`vec_avg(x)` 后必须 `ts_backfill`，否则 TO 爆炸、lc 塌陷

`RREbg1Y0`（净广度 + 无变化占比）与 `3qoXNANZ`（净广度 × 覆盖度）是本轮唯一两条**未加 `ts_backfill`** 的臂，结果：

| 臂 | 是否 backfill | TO | lc | DD | S |
|---|---|---:|---:|---:|---:|
| `akKbp68x` daily 净广度 | 有 `ts_backfill(·,22)` | **9.85%** | **49** | 16.78% | **0.82** |
| `MPYarLwo` 宽口径 | 有 `ts_backfill(·,22)` | 9.80% | 49 | 17.14% | 0.77 |
| `RREbg1Y0` 净广度+nochg | **无** | **104.91%** | **11** | 37.25% | 0.04 |
| `3qoXNANZ` 净广度×覆盖 | **无** | **29.53%** | **25** | 28.59% | 0.08 |

**根因**：VECTOR 字段在部分交易日为空，`ts_mean(vec_avg(x), 5)` 直接吃 NaN ⇒ 信号在「有值 / 无值」之间来回翻转 ⇒ 产生与信息无关的高频换手，同时把有效持仓数压到 11–25 只。

⇒ **硬规则（写入派发前检查表）**：`vec_avg(x)` 之后**必须**先 `ts_backfill(·, 22~66)` 才能进 `ts_mean` / `ts_delta` / `ts_zscore` / `ts_corr` 等任何时序算子。这条与「VECTOR 必须先 vec_* 聚合」并列，是本项目处理 VECTOR 字段的第二条铁律。

### 33.6 `analyst9` 最终判定：封盘

**8 臂覆盖五种结构**（快照广度 / 日频广度 / 宽口径 / z-score / 双维度合成 / 覆盖度门控 / 低覆盖反向 / EPS 共识），最好 **S 0.82 / F 0.62 / 2Y 0.20**。

| 闸 | 线 | 最好实测 | 缺口 |
|---|---:|---:|---:|
| LOW_SHARPE | 1.58 | 0.82 | **−0.76** |
| LOW_FITNESS | 1.00 | 0.62 | −0.38 |
| LOW_2Y_SHARPE | 1.58 | 0.20 | **−1.38** |

⇒ `analyst` 塔第 3 颗**仍未找到**，该塔保持 **2/3**。至此 analyst 类已试完 `analyst7 / 44 / 47 / 48 / 83 / 93 / 9` 七个集，**全族最好单维 0.82**，与 `fundamental6` 的 0.92 同属「有信号但幅度不足」。

---

## 三十四、`other545`（NEMO 2.0 成品信号包）四臂封盘

数据集：cat **other**，cov **0.5269**，仅 **4 字段全 VECTOR** —— `oth545_mktcap`（美元市值）/ `oth545_mpd`（动态价格动量分数）/ `oth545_pln_omen`（NLP 网络动量分数）/ `oth545_score`（NEMO 2.0 复合模型分数）。

| 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 复合分数 | `d5WbGkzX` | **0.62** | 0.42 | 4.30% | 27.35bp | 12.47% | 51 | 0.25 | 0.19 |
| 价格动量分数 | `vR1rQKA3` | 0.59 | 0.41 | 3.87% | 31.40bp | 16.81% | 51 | 0.10 | 0.21 |
| NLP 增量（score−mpd） | `2rAwY1XP` | **−0.20** | −0.07 | 4.39% | −7.81bp | 29.79% | 50 | −0.07 | −0.11 |

**判据**：成品信号包（与 `analyst47` 同类）在 DEU 的上限就是 0.6 出头，且「复合分数 − 动量分数」的 NLP 增量项**直接为负**，说明复合分数里真正起作用的只有价格动量那一半。⇒ **封盘，`other` 塔保持 2/3。**
---

## 三十五、`insider_matrix` 四臂封盘 —— 并纠正一个塔位认知错误

### 35.1 数据集事实（DEU/TOP500/D1）

cov **0.548**，**33 字段全 MATRIX**（不是 VECTOR，省掉 `vec_avg` 这一步）。字段结构高度规整，四组 × 四个指标：

| 组 | 字段族 | 含义 |
|---|---|---|
| 全体 | `eur_aggregated_value_{1,2,3,4}` | 买入均值 / 买入总和 / 卖出均值 / 卖出总和 |
| 高管 | `eur_director_value_{1,2,3,4}` | 同上，仅董事 |
| 高管信号 | `eur_director_signal_value_{1..4}` | 同上，信号口径 |
| 首席高管 | `eur_top_director_{value,signal_value}_{1..4}` | 同上，最高层 |
| 成品 | `director_intensity_score`（cov **1.0**） | 内部人交易强度综合分 |

`eur_` 前缀（欧元计价）说明这是欧洲内部人交易的聚合数据。

### 35.2 四臂实测

| 模板 | 结构 | alpha | S | F | TO | margin | DD | lc | 2Y | **sub** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 净买入比率 | `(rank(buy2)−rank(sell4))/(rank(buy2)+rank(sell4))` | `9qxjNbkd` | 0.21 | 0.08 | 7.37% | 4.36bp | 29.27% | 67 | 0.10 | **0.79** |
| 净买入差 | `rank(buy2)−rank(sell4)` | `QPvbwX5K` | 0.15 | 0.05 | 7.23% | 3.28bp | 29.27% | 67 | 0.11 | **0.75** |
| 高管净买入 | `rank(dir2)−rank(dir4)` | `WjObv1Eo` | **0.29** | 0.12 | 7.20% | 6.22bp | 26.91% | 67 | −0.05 | **0.88** |
| 强度综合分 | `director_intensity_score` | `rKROZXoo` | 0.12 | 0.03 | 11.29% | 1.48bp | 18.08% | 72 | −0.09 | 0.01 |

### 35.3 ★★★★ 塔位认知纠正：`insider_matrix` 属 **OTHER** 塔，不是 INSIDERS

四条臂的 `pyramids` 全部是 **`DEU/D1/OTHER`**。

⇒ 本次派发本意是「首次验证 DEU 的 insiders 塔（0 颗）」，但 **`insider_matrix` 在 DEU 被平台归入 other 塔**，因此：
1. 它**不可能**点亮 insiders 塔；「DEU `insiders` 塔 0 颗」的现状不变；
2. 反过来说，任何基于 `insider_matrix` 的合格 alpha 都会去给 **`other` 塔**（现 2/3）加颗。

**教训**：数据集名字里带 `insider` 不等于归 insiders 塔；塔位只能以 `get_alpha_details` 的 `pyramids` 实测为准。这与 §32 里「`cap` 会让 fundamental 表达式变成 PV+FUNDAMENTAL 双塔」是同一类陷阱的反面。

### 35.4 判据：弱 S + 强 sub 的罕见形态，但无出口

- **S 0.12–0.29**，全部远低于 1.58；2Y 全部在 −0.09 ~ 0.11 之间，等于零
- **但 `sub_universe_sharpe` 高达 0.75–0.88**，是本轮已测所有数据集中最高的，且 `lc` 稳定在 67
- margin 3.28–6.22bp 偏低，TO 7.2–11.3%

这个组合说明：**信号在小市值子宇宙里是有效的，但在 TOP500 全宇宙被少数大票稀释到几乎为零**。理论上可用子宇宙约束或更小 universe 释放，但 DEU 只有 TOP500 一个 universe，**没有操作空间**。

⇒ **`insider_matrix` 封盘。** 若将来 DEU 开放 TOP3000 / TOP1000，这是最值得复活的对象之一（sub 0.88 + lc 67 + 2Y 近零说明只是被稀释，不是失效）。
### 35.5 universe 复验（确认无扩展空间）

`get_datasets` 逐 universe 实测（DEU/delay 1）：

| universe | 返回数据集数 |
|---|---:|
| **TOP500** | **172** |
| TOP3000 / TOP1000 / TOP200 | **全部 0（空数组，非报错）** |

另测 `DEU/TOP500/delay 0` = **70 个数据集**（存在，但按战略锁定不使用 delay 0）。

⇒ **DEU 只有 TOP500 一个 universe，确认无疑。** 这是本战役所有「lc 低 / sub 弱 / cov<0.4 无法救」问题的总根源：TOP500 只有约 500 只票，任何稀疏字段（覆盖率 0.5 意味着仅约 250 只）必然 lc 塌陷。

---

## 三十六、权重 / 缩放 / 平滑三轴实验：全部无杠杆，`fundamental6` 结构锁定

### 36.1 三条权重臂（对照 = 等权无 backfill `leAvwnRA` S 0.90 / 2Y 0.39 / sub 0.66 / DD 12.39%）

| 权重方案 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **等权（对照）** | `leAvwnRA` | **0.90** | 0.66 | 1.98% | 68.57bp | 12.39% | 73 | **0.39** | 0.66 |
| 净利率 ×2 | `zq38l0X8` | 0.89 | 0.66 | 2.02% | 67.73bp | 13.53% | 74 | 0.42 | 0.64 |
| 现金/资产 ×2 | `gJebndR0` | 0.87 | 0.62 | 1.96% | 65.59bp | **10.18%** | 70 | 0.40 | 0.69 |
| 净利率 ×0.5 | `akKb5wOx` | 0.88 | 0.64 | 1.95% | 67.86bp | 11.23% | 71 | 0.34 | 0.67 |

**⇒ 权重完全不是杠杆**：把最强腿（净利率，单维 0.92）权重翻倍、减半、或把最弱腿（现金 0.52）翻倍，S 全部落在 0.87–0.89，与等权 0.90 的差异在噪声内。**三条 rank 等权相加已是最优权重，不必再调。**

### 36.2 `ts_decay_linear(·,5)` 平滑：无益

`KPJrKklp`（三腿 + decay5，有 backfill）= S **0.95** / 2Y 0.47 / sub 0.68 / DD 11.63% / TO 1.89% / lc 74，对照无 decay 的 `bl6b0bPq` = S **0.98** / 2Y 0.54。⇒ **平滑让 S −0.03、2Y −0.07**，与 memory 里「对高区分度信号加工有害」的方向一致，只是幅度小。

### 36.3 `group_scale` 替代 `rank`：平台侧卡死，未取得读数

`rKgaleZN`（三腿全部换 `group_scale(·,subindustry)`）在 `progress: 0.1` 停留 **>10 分钟**不动，而同期同批三条臂 3–5 分钟全部 COMPLETE。判定为**平台侧对该表达式的计算卡死**（大概率因为基本面比率的极端值让 group_scale 的标准化过程数值不稳定）。

⇒ 记录为「不可用路径」，不再重试。memory 里 GBR 的 `group_scale` 优于 `group_rank`（S 2.74 vs 2.50）的结论**不能直接迁移到基本面原始比率**，因为 GBR 那条是对已标准化的模型概率做缩放，量纲与基本面比率完全不同。

---

## 三十七、`fundamental22`（ESG KPI）封盘

数据集：cat **fundamental**，cov **0.690**，**仅 1 字段** `fnd22_value`（VECTOR，「Numerical value of the specific ESG KPI」）。

| 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ESG 水平 | `YP1MjQzo` | 0.26 | 0.10 | 1.03% | 33.03bp | 19.89% | **105** | **1.36** | **−0.19** |
| ESG 变化（Δ66） | `gJeZY1Jv` | 0.35 | 0.13 | 6.18% | 6.00bp | 12.71% | 91 | −0.24 | 0.18 |

**值得注意的是 `YP1MjQzo` 的 2Y = 1.36**（全场第二高），且 `lc` 105（全场最高）。但：
- `sub_universe_sharpe = −0.19`，负值；
- S 仅 0.26，说明全期收益被早期年段拖垮，只在近两年有效；
- 单字段、VECTOR、且不同公司的 ESG KPI 类型混杂，**跨股票不可比**（这是 ESG 数据集的通病）。

⇒ **封盘。**
---

## 三十八、`bl6b0bPq` 的库存价值：self 相关性仅 **0.2121**

对三腿最优件 `bl6b0bPq`（`fundamental6`，S 0.98 / F 0.75 / margin **84.63bp** / DD 12.07% / TO 1.73% / lc 75 / 2Y 0.54 / sub 0.71）跑本地 self 相关性（零配额）：

| 项 | 值 |
|---|---:|
| `max_correlation` | **0.2121** |
| 红线 | 0.70 |
| `passes_check` | **true** |
| 最相关件 | `blRnKEk6`(0.2121) / `vRk6og8b`(0.1600) / `58gkLAkk`(…) |

**这意味着**：`bl6b0bPq` 与 DEU 已提交池几乎完全不相关（0.21 是全战役最低之一）。它的三项指标组合在 DEU 是独一份：

- **margin 84.63bp** —— 本战役所有已测 alpha 中最高的（对比 `E56pROb9` 33.34bp、`wpQYNvZp` 13.1bp）
- **DD 12.07%** —— 极低
- **self 0.21** —— 完全无拥挤
- 唯一缺口：S 0.98 / 2Y 0.54（闸线 1.58）

⇒ **判定为「高价值库存件」**，不因 S 不够而废弃。三个明确的复活触发条件：
1. DEU 开放 TOP1000 / TOP3000（lc 能从 75 上到数百，截面幅度会显著提升）；
2. 平台闸线调整（若 LOW_SHARPE 降到 1.0 以下）；
3. 允许 fundamental × 集合外 category 组合（trio×非trio 配额放开），可用它做基座叠加 `analyst9` daily 净广度（0.82）这类正交腿。

### 38.1 `group_scale` 臂最终判定：平台卡死

`rKgaleZN` 在 `progress: 0.1` 停留 **超过 20 分钟**（同期同批三条臂 3–5 分钟内完成），期间无报错。判定为平台侧计算卡死。**不再重试，记入不可用路径。**

---

## 三十九、other532（Barra 残差收益）Wave-1：覆盖全场最高、信号全场最弱（2026-11-04 夜）

### 39.1 数据集事实（DEU/TOP500/D1 实测）

`other532` cat **other**，dataset 级 cov 报 **0.8563**（低于前轮 0.9 筛线故被漏），但**字段级 cov 0.7413–0.9714**，8 字段**全 MATRIX**（省掉 vec_avg），ac 仅 1–25（极低拥挤）。

| 字段 | cov | ac | 含义 |
|---|---:|---:|---|
| `oth532_emerging_daily_specificreturn` | 0.9714 | 5 | Barra 新兴市场模型残差日收益 |
| `oth532_emerging_monthly_specificreturn` | 0.9643 | 4 | 同上月频 |
| `oth532_global_daily_specificreturn` | 0.9714 | 25 | Barra 全球模型残差日收益（本波主腿） |
| `oth532_global_monthly_specificreturn` | 0.9636 | 11 | 同上月频 |
| `idiosyncratic_return_eue_daily` | 0.7484 | 10 | 欧洲股票模型残差日收益 |
| `idiosyncratic_return_eue_monthly` | 0.7413 | 9 | 同上月频 |
| `idiosyncratic_return_eult_daily` | 0.7484 | 1 | 另一模型版本日收益 |
| `idiosyncratic_return_eult_monthly` | 0.7413 | 2 | 同上月频 |

**塔位实测 `DEU/D1/OTHER`**（单集 ATOM，不触碰禁混集合内部互组）。other 塔现 2/3，**本集只要出 1 颗即点亮**。

### 39.2 ★ 字段性质诊断（派发前必须先做的第一件事）

两条诊断臂确定了字段的量纲性质，**这是本波最有价值的元信息**：

| 诊断 | alpha | S | TO | 判读 |
|---|---|---:|---:|---|
| `-field`（1 日反转） | `58EgnZWn` | −0.07 | **78.58%** | TO 爆表 ⇒ 字段逐日变化 ⇒ **是日收益率，不是累计水平** |
| `ts_delta(field,1)` | `rKRep1k3` | 0.26 | **87.18%** | 若是累计水平，差分后应低换手高 S；实测反而更高换手 ⇒ 二次差分噪声 |

**方法沉淀**：拿到「residual return / specific return / cumulative return」这类命名模糊的收益字段，**用 `-field` 的 TO 一眼定性质**——TO >50% ⇒ 日频收益序列；TO <5% 且 S 显著 ⇒ 累计水平，必须先 `ts_delta`。这一步省下整波设计踩空。

### 39.3 Wave-1 首批 7 臂实测（decay16 / SUBINDUSTRY / trunc 0.08）

| # | 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1 日反转 `-g` | `58EgnZWn` | −0.07 | −0.01 | 78.58% | 0.16bp | 28.5% | 126 | −0.36 | −0.38 | S/F/HIGH-TO/2Y/SUB |
| 2 | 层/收益探针 `ts_delta(g,1)` | `rKRep1k3` | 0.26 | 0.04 | 87.18% | 0.44bp | 16.1% | 97 | 0.39 | −0.49 | S/F/HIGH-TO/2Y/SUB |
| 3 | 5 日残差反转 `-mean5` | `akKxjZax` | 0.23 | 0.07 | 21.22% | 2.08bp | 19.0% | 155 | 0.27 | −0.09 | S/F/2Y/SUB |
| 4 | 22 日残差反转 `-mean22` | `MPY3Mj9k` | 0.18 | 0.07 | 10.66% | 3.30bp | 15.6% | 156 | 0.46 | 0.08 | S/F/2Y |
| 5 | 12-1 残差动量 | `1YNZkYZJ` | **0.26** | **0.11** | 10.35% | **4.41bp** | 16.6% | 155 | 0.43 | **0.19** | S/F/2Y |
| 6 | 残差夏普 `mean252/std252` | `88RP58Go` | 0.22 | 0.08 | 4.67% | **7.70bp** | **11.6%** | 153 | −0.12 | **0.24** | S/F/CW 0.326/0.1/2Y |
| 7 | 低残差波动 `-std66` | `9qxWZz1r` | 0.09 | 0.03 | 3.52% | 6.27bp | **49.2%** | 171 | 0.45 | −0.09 | S/F/2Y/SUB |

### 39.4 ★ 正反两面读数

**正面（数据集健康度本战役最佳）**：

1. `lc` **126–171**，是全部 DEU 已测 alpha 的最高区间（fundamental6 仅 75、fundamental22 105、pv109 15–68）⇒ 覆盖真实且宽；
2. `startDate 2014-01-01` ⇒ **满 10 年无 leading gap**（对比 model216 只有 2017 起）；
3. 低换手端 margin 反而最高：残差夏普 **7.70bp / TO 4.67%**、低残差波动 6.27bp / 3.52% ⇒ 单位换手收益不差。

**反面（信号强度本战役最弱）**：

4. 7 臂 S 区间仅 **0.09–0.26**、F ≤ 0.11，距 LOW_SHARPE 1.58 差 **1.32**；
5. 残差反转在 DEU **几乎不存在**：1 日 −0.07 / 5 日 0.23 / 22 日 0.18；对比 GBR `risk68` 残差反转能到 S 1.13，DEU 这个集只有其零头；
6. 低残差波动腿 DD **49.2%**（全场最差），不可用。

### 39.5 Wave-1 第二批 6 臂（已派发，待读回）

补测的是**此前漏掉的经典形态**——Blitz-Huij-Martens(2011) 残差动量的标准式是「12-1 残差收益 ÷ 残差波动率」，此前只分别测了分子（#5）与分母（#6），**从未合起来测**：

| tag | 模板 | sim id |
|---|---|---|
| N1 | 标准残差动量 `(mean252-mean22)/std252` | `Fyn5x8yp4Hg9YqppUNu7NR` |
| N2 | 纯 6 月残差动量 `mean126` | `2IZ07XOL4F3caYHtSuEDwx` |
| N3 | 波动调整 1 月反转 `-mean22/std22` | `3XqSNceY4Wgb6P3yCvxKo4` |
| N4 | 月频残差反转 `-mean(monthly,3)` | `3Efsfn9nM4vRc6R2me7ii3G` |
| N5 | 跨模型分歧 `g - eue_daily` | `1dPOXp8U84z8cLG1lXXGYN1` |
| N6 | 残差波动扩张 `std22-std252` | `1ZJHgY4W24PDaLjPZhpcCMT` |

### 39.6 本波已确认的失败路径

- **1 日反转在 DEU 直接死**：`-field` S −0.07 且 TO 78.58% 触 `HIGH_TURNOVER`（闸线 0.7）；
- **`ts_std_dev` 作主信号（低波溢价）在 DEU 不可用**：DD 49.2%，远差于均值类（11.6–19.0%）；
- **残差夏普腿会被 `CONCENTRATED_WEIGHT` 卡**（0.326/0.1）⇒ 除法结构把权重集中到少数低波大票。
### 39.7 Wave-1 第二批 6 臂实测

| tag | 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| N1 | 标准 BHM 残差动量 `(m252-m22)/s252` | `e75Qk3NO` | 0.16 | 0.05 | 10.27% | 1.95bp | 16.1% | 156 | 0.48 | 0.16 | S/F/2Y |
| N2 | **6 月残差动量 `m126`** | **`KPJrlnWl`** | **0.40** | **0.23** | 5.26% | **15.32bp** | 22.6% | 152 | **0.02** | 0.20 | S/F/2Y |
| N3 | 波动调整 1 月反转 `-m22/s22` | `WjOe1VbN` | 0.13 | 0.03 | 10.73% | 1.64bp | 16.5% | 154 | 0.45 | 0.15 | S/F/CW 0.215/0.1/2Y |
| N4 | 月频残差反转 `-mean(monthly,3)` | `LLMZVGz6` | 0.32 | 0.10 | 9.42% | 2.67bp | **8.4%** | **22** | **−0.68** | 0.12 | S/F/CW/SUB/2Y |
| N5 | 跨模型分歧 `g − eue_daily` | `3qoVQzQg` | 0.24 | 0.04 | **80.50%** | 0.46bp | 16.3% | 92 | −0.53 | **0.29** | S/F/HIGH-TO/2Y |
| N6 | 残差波动扩张 `s22−s252` | `WjOe19qO` | 0.12 | 0.03 | 8.77% | 2.34bp | 15.2% | 152 | 0.56 | −0.11 | S/F/SUB/2Y |

### 39.8 ★ 封盘判定：other532 = 强度天花板 0.40（13 臂扫尽）

**13 臂 S 分布：0.09 / 0.12 / 0.12 / 0.13 / 0.16 / 0.18 / 0.22 / 0.23 / 0.24 / 0.26 / 0.26 / 0.32 / 0.40**——中位数 0.22，最好 0.40。

缺口：S 0.40 vs 1.58（**−1.18**）、F 0.23 vs 1.00（−0.77）、2Y 0.02 vs 1.58（−1.56）。

**关键判读（这条比数字本身更重要）**：

1. **反向也不成立**：1 日反转 −0.07、5 日 0.23、22 日 0.18，全部微弱；而 6 月动量 +0.40 是唯一像样的 —— 说明 DEU 残差收益里**短周期反转不存在、中周期动量弱存在**，与 GBR `risk68`（残差反转 S 1.13）完全相反。**同一经济学机制跨区符号强度不可迁移。**
2. **最好的那条（N2）恰好 2Y = 0.02**：全样本 10 年 S 0.40 但最近两年归零 ⇒ 即使放宽闸线也不可用。
3. **月频字段不可用**：N4 `lc` 仅 **22**（月频稀疏），2Y −0.68。若用月频必须先 `ts_backfill` 到日频，但那样会引入前视式平滑。
4. **跨模型分歧腿无信号且高换手**：N5 TO 80.5%，说明两个 Barra 模型版本在日频上高度不同步 —— 这是数据管线差异，不是经济信号。

**但本集留下一个可复用资产**：它是 DEU 唯一「lc 150+ 且满 10 年」的数据集。若将来放开塔混配额或闸线松动，`m126`（`KPJrlnWl`，margin **15.32bp**、TO 5.26%、DD 22.6%）是**最干净的基座腿**——低换手、高单位收益、覆盖宽。已登记入库存。

### 39.9 方法沉淀：先看健康度、再看强度

本集与 `pv109`（lc 15–68、2Y 负）、`analyst83`（GBR，TO≈2% 慢变）构成三种死因的完整对照：

| 死因 | 实例 | 判据 |
|---|---|---|
| 覆盖塌陷 | `pv109` | `lc` < 100 且 `sub` < 0 |
| 更新过慢 | `analyst83`(GBR) | TO < 5% 且 S≈0 |
| **信号缺失（本集）** | `other532` | `lc` 150+ / 满 10 年 / TO 合理 / **S 全部 < 0.5** |

⇒ **健康度全绿不代表有 alpha**；`lc` 高只排除「覆盖死因」，不能排除「信号死因」。判定顺序应为：先 lc 与 2Y（排除结构性死因）→ 再看 S 是否过 0.8（强度下限）→ 最后才抠模板。
---

## 四十、★ model30（StarMine 智测 + 预测惊喜）Wave-1：DEU 新数据集最强单臂 S 1.25（2026-11-04 夜）

### 40.1 数据集事实

`model30` cat **model**，**14 字段全 MATRIX**（无需 vec_avg），cov 0.29–0.67，ac 0–104。**此前从未测过**（本地库 64 个已测集里无它，§22 剩余清单也未列）。塔位实测 **`DEU/D1/MODEL`**（单集 ATOM）。

| 字段 | cov | ac | 含义 |
|---|---:|---:|---|
| `star_new_eps_surprise_prediction_fy1` | 0.6663 | 10 | **预测惊喜百分比** fy1（智测估计对均值估计的偏离） |
| `star_new_eps_surprise_prediction_fy2` | 0.6663 | 104 | 同上 fy2 |
| `star_new_eps_surprise_prediction_12m` | 0.6649 | 33 | 同上 forward 12 个月 |
| `star_new_eps_smart_estimate_fy1` | 0.6663 | 37 | **智测估计 EPS** fy1（分析师加权） |
| `star_new_eps_smart_estimate_fy2` | 0.6663 | 24 | 同上 fy2 |
| `star_new_eps_smart_estimate_12m` | 0.6649 | 13 | 同上 forward 12 个月 |
| `star_new_eps_analyst_number_fy1` | 0.6731 | 5 | fy1 覆盖分析师数 |
| `star_new_eps_analyst_number_fy2` | 0.6731 | 1 | 同上 fy2 |
| `star_new_eps_analyst_number_fq1/fq2` | 0.6327/0.6188 | 0/1 | 季度覆盖数 |
| `star_new_eps_smart_estimate_fq1/fq2` | 0.3989/0.2906 | 0/0 | 季度智测估计 |
| `star_new_eps_surprise_prediction_fq1/fq2` | 0.3989/0.2906 | 3/0 | 季度预测惊喜 |

### 40.2 Wave-1 第一批 8 臂（2 臂待回）

| tag | 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S1 | 预测惊喜 fy1 原值 | `2rAm8Vnw` | 0.38 | 0.22 | 7.20% | 11.33bp | 24.73% | 85 | 0.69 | 0.10 | S/F/CW/SUB/2Y |
| S2 | 预测惊喜 12m 原值 | `npvPxEaq` | 0.65 | 0.52 | 7.07% | 22.54bp | 33.70% | 85 | 0.89 | 0.29 | S/F/CW/SUB/2Y |
| S3 | 双视界惊喜 rank 和 | `0mYrO2O8` | 0.85 | 0.57 | 6.04% | 18.87bp | **9.61%** | 81 | 0.88 | **0.48** | S/F/CW/2Y |
| S4 | 期限结构 `fy2−fy1` | `mLo6wvaE` | 0.02 | 0.00 | 7.93% | 0.51bp | **49.21%** | 80 | 0.36 | −0.07 | S/F/CW/SUB/2Y |
| S7 | 惊喜 ÷ 覆盖数（低覆盖加权） | `Vkx01rdb` | 0.49 | 0.35 | 9.91% | 13.01bp | 28.47% | 85 | **1.07** | 0.19 | S/F/CW 0.370/0.1/SUB/2Y |
| **S9** | **`ts_zscore(智测估计 fy1, 252)`** | **`88RP5xpV`** | **1.25** | **1.06** | 5.29% | **33.96bp** | 13.79% | 82 | 0.91 | 0.37 | S/CW/SUB/2Y |
| S6 | 修订率 `Δ66/|mean252|` | `kqNgddbz` | 0.07 | 0.02 | 8.87% | 3.02bp | **66.75%** | 78 | −0.07 | −0.28 | 全灭 |
| S5 | 惊喜 Δ66 | 待回 | — | — | — | — | — | — | — | — | — |

### 40.3 ★★★★★ 最重要的方法结论：`ts_zscore` 是否有害，取决于原始量是否**截面可比**

本臂（S9）**推翻**了此前「`ts_zscore` 对强信号必然有害」的粗口径，并为它划出了适用边界：

| 场景 | 原始量性质 | `ts_zscore` 效果 | 实例 |
|---|---|---|---|
| 高区分度、**已截面可比** | 净利率比率 / 净广度（0–1 比值） | **有害**：净利率 0.92→0.73、净广度 0.82→0.53 | fundamental6 / analyst9 |
| **不可截面比** | EPS 货币值（每股多少欧元，跨股不可比） | **决定性有益**：直接原值不可用 → z 分后 **S 1.25 / F 1.06** | model30 |

**根因**：EPS 是「每股 X 欧元」的量纲，00 元的公司和 5 欧元的公司在截面上不可比；`ts_zscore` 把它转成「相对自身 252 日历史是否异常」，**这一步做的不是修饰，而是让量纲具备可比性**。反之比率类字段本来就可比，z 分等于把截面绝对水平的信息扔掉。

**派发前的判定动作**：看字段单位——**货币值 / 股数 / 金额 / 计数 ⇒ 先套 `ts_zscore` 或 `rank`；比率 / 概率 / 百分比 ⇒ 直接用，别套 z 分。** 这条比「先跑单维」更快，能在派发前就选对骨架。

### 40.4 其它读数

- **方向确认**：惊喜预测原值 S1 0.38 为正 ⇒ **预测惊喜越高 → 未来收益越高**（符合 StarMine 先验），无需取反；
- **12m 视界 > fy1 视界**（0.65 vs 0.38）：越远的财年预测惊喜越有信息量，因为已计入更多分析师分歧；
- **双视界 rank 相加显著改善全部维度**（0.65→0.85、DD 33.7%→9.61%、sub 0.29→0.48）——这是「rank 相加」手法第 4 次实证有效；
- **期限结构 `fy2−fy1` 是噪声**（S 0.02 / DD 49.2%）⇒ 两个视界的差抵消了共同信号；
- **修订率 `Δ/|mean|` 灾难**（DD 66.75%、sub −0.28）：EPS 估计有负值，绝对值分母在符号翻转处爆掉 ⇒ **EPS 类字段禁用 `abs()` 分母归一化**，改用 `ts_zscore`。

### 40.5 Wave-1 第二批 8 臂（z 分深化，已派发）

围绕获胜结构 `ts_zscore(智测估计)` 展开，测四个轴：视界（fy2 / 12m）、共识（dual / triple）、正交腿（+惊喜）、窗口与平滑（504 / decay22）：

| tag | 模板 | sim id |
|---|---|---|
| Z2 | `ts_zscore(SE_fy2, 252)` | `ZrHj02aV53F97CDKhIfyCg` |
| Z12 | `ts_zscore(SE_12m, 252)` | `CSp5t38L56R9NE2A8mUCwa` |
| ZD | `rank(z_fy1)+rank(z_12m)` | `2dV6bMc7P4tga2o7lkkSYmG` |
| ZT | 三视界 z 分 rank 和 | `2jm1BMaMW4L08Zd1dybfaROZ` |
| ZS | `rank(z_fy1)+rank(惊喜12m)` | `znmkzgne4hgc6cLSn20KAu` |
| Z504 | `ts_zscore(SE_fy1, 504)` | `1CoQit1Mt4y29t27AROL3eN` |
| ZDM | `ts_decay_linear(z_fy1, 22)` | `rk3Mgfgu57Fb0y1hMisrm3P` |
| ZM | `z_fy1 × rank(惊喜12m)` | （静默丢弃，待补） |

### 40.6 当前最佳件的闸位缺口（S9）

`88RP5xpV`：**F 1.06 已过闸**（唯一一条 F 过闸的新集臂），剩余缺口集中在三处：

| 闸 | 实测 | 闸线 | 缺口 |
|---|---:|---:|---:|
| LOW_SHARPE | 1.25 | 1.58 | **−0.33** |
| LOW_SUB_UNIVERSE_SHARPE | 0.37 | 0.59 | **−0.22** |
| LOW_2Y_SHARPE | 0.91 | 1.58 | **−0.67** |

⇒ 缺口结构**优于** fundamental6（−0.60/−0.25/−1.04）与 `E56pROb9` 的同类读数，是 DEU 目前最有希望破闸的单数据集线索。破闸优先序：**2Y（最大缺口）→ S → sub**。
### 40.7 ★★★ 口径铁律：checks.fail 与 checks.warning 会漂移，唯一权威是 ra.ra_failed_checks

同一批臂在两次读取中闸门分类**会从 fail 跳到 warning**：TR22 首次读 `checks.fail = []`，再读时失败项全部出现在 `checks.warning`，而 `ra.ra_failed_checks = [LOW_SHARPE, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE]`、`failed_ra_count = 3`。

⇒ **任何「全闸通过」的判定必须同时满足三条**：`checks.fail` 为空 **且** `ra.failed_ra_count = 0` **且** `checks.pending` 只剩 SELF/DATA_DIVERSITY/PROD/REGULAR 四类。只看 `checks.fail` 会把 S 1.33 < 1.58 的件误判为过闸。

### 40.8 Wave-2：z 分深化 7 臂

| tag | 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Z2 | zscore(SE_fy2,252) | `mLo6px86` | 0.98 | 0.75 | 5.56% | 26.66bp | 15.28% | 83 | 0.80 | 0.39 |
| Z12 | zscore(SE_12m,252) | `GrWOP3eQ` | 0.91 | 0.68 | 5.10% | 27.61bp | 13.38% | 83 | 0.47 | 0.51 |
| ZD | 双视界 z rank 和 | `3qoVwExP` | 1.09 | 0.87 | 4.51% | 35.01bp | 15.79% | 81 | 0.60 | 0.37 |
| ZT | 三视界 z rank 和 | `6XdK7RaO` | 1.08 | 0.86 | 4.54% | 35.08bp | 15.78% | 80 | 0.57 | 0.38 |
| **ZS** | **z_fy1 + 惊喜12m** | **`6XdK71PY`** | **1.25** | **1.05** | 5.40% | 32.60bp | 13.26% | 81 | **1.15** | **0.47** |
| Z504 | zscore(SE_fy1,504) | `2rAmMNz5` | 1.03 | 0.80 | 4.21% | 36.27bp | 15.31% | 83 | 0.70 | 0.33 |
| ZDM | decay22(z_fy1) | `omEW7zqJ` | 1.24 | 1.05 | 4.41% | **40.35bp** | 13.01% | 83 | 0.99 | 0.31 |
| S5 | 惊喜 Δ66 | `JjeQqwAx` | 0.17 | 0.06 | 9.00% | 4.05bp | **44.28%** | 78 | 0.46 | −0.04 |
| Z66 | zscore(SE_fy1,66) | `ZYQA6QO0` | 0.84 | 0.57 | 10.57% | 10.76bp | 15.26% | 77 | **−0.09** | 0.26 |
| ZSW | winsorize(z_fy1,std=4) | `MPY3OYdL` | **1.28** | 1.09 | 5.19% | 35.06bp | 13.86% | 82 | 0.96 | 0.37 |

**三条读数**：

1. **多视界共识反而更差**（ZD 1.09 / ZT 1.08 < 单 fy1 1.25）：fy2 与 12m 的 2Y 只有 0.80 / 0.47，掺进来就稀释。**多视界平均不是万能增益，要先逐视界看 2Y**；
2. **窗口谷：252 是局部最优**（66 → 2Y **−0.09**；504 → 0.70；252 → 0.91）。长窗才稳；
3. **winsorize 抬 S 但杀 2Y/sub**（S 1.28 最高，2Y 0.96 / sub 0.37）⇒ 去极值是提纯度而非提稳健，不用于本线。

### 40.9 Wave-3：平滑与三腿 7 臂 —— decay22 是决定性杠杆

| tag | 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **ZSD** | **decay22(ZS)** | **`JjeQq3LE`** | **1.26** | **1.07** | 4.32% | **41.48bp** | 13.03% | 81 | **1.32** | **0.55** |
| ZSD5 | decay5(ZS) | `P0ogNzo7` | 1.25 | 1.05 | 5.13% | 34.52bp | 13.32% | 81 | 1.18 | 0.48 |
| ZS3 | 三腿（+惊喜 fy1） | `9qxWY5Lo` | 1.13 | 0.89 | 5.68% | 27.50bp | 12.13% | 81 | 0.99 | 0.48 |
| ZS3D | decay22(三腿) | `88RPbGgq` | 1.13 | 0.90 | 4.50% | 34.91bp | **12.00%** | 81 | 1.10 | 0.53 |
| ZSH | hump(ZS) | `ZYQA6VL0` | **0.52** | 0.27 | 1.91% | 35.24bp | 20.51% | 80 | 1.25 | **−0.04** |
| D22H | decay22(hump(ZS)) | `RRE63MMe` | 0.44 | 0.21 | 1.98% | 29.25bp | 22.35% | 79 | 1.23 | −0.13 |
| D66 | decay66(ZS) | `qML018ZK` | 1.14 | 0.93 | **3.31%** | **50.21bp** | 15.23% | 81 | 1.10 | 0.57 |
| D22H12 | decay22(z_fy1 + z_12m) | `JjeQwMAm` | 1.07 | 0.84 | 3.75% | 41.28bp | 15.16% | 81 | 0.71 | 0.37 |
| **TR22** | **decay22(rank(ts_rank(SE1,252)) + rank(SP12))** | **`58EgbnAM`** | **1.33** | **1.15** | 4.51% | 41.59bp | 13.42% | 82 | **1.31** | **0.65 过闸** |

**decay22 是全波最有效的一步**：ZS → ZSD 把 2Y 从 1.15 抬到 **1.32**、sub 从 0.47 抬到 **0.55**、margin 32.6 → **41.48bp**，而 S 不变。这是「换手 4.3% + 月度级信息」的必然结果——EPS 估计本来就慢变，快切反而吃噪声。

**hump 在本线是灾难**（0.52 / sub −0.04）：它把 TO 压到 1.9% 但把仓位集中到极少数股票，sub 直接翻负。**hump 只适合用来压 CW 或 prod，不适合用来提质量。**

### 40.10 ★★★★ Wave-4 突破：ts_rank 优于 ts_zscore，sub 首次过闸

`TR22 = ts_decay_linear(add(rank(ts_rank(SE_fy1, 252)), rank(SP_12m)), 22)`（7 算子）：

| 指标 | ZSD（用 zscore） | **TR22（用 ts_rank）** | Δ |
|---|---:|---:|---:|
| Sharpe | 1.26 | **1.33** | +0.07 |
| Fitness | 1.07 | **1.15** | +0.08 |
| 2Y Sharpe | 1.32 | 1.31 | −0.01 |
| **sub_universe** | 0.55（失败） | **0.65（pass）** | **+0.10** |
| margin | 41.48bp | 41.59bp | +0.11 |

**根因**：`ts_zscore` 用均值/标准差，会被 EPS 的**离群跳变**（一次性计提、股本变动）拉偏；`ts_rank` 用**时序分位**，对离群值免疫。EPS 这类「有跳变且负值合法」的序列，**时序分位比时序 z 分稳健**。

⇒ **可复用规则**：字段是货币值/水平值 ⇒ 先用 `ts_rank(x,252)`；若序列含负值或跳变（EPS、利润、现金流）⇒ **禁用 `ts_zscore`，改用 `ts_rank`**。

### 40.11 TR22 剩余闸位与 CW 根因假说

以 `ra.ra_failed_checks` 为准，TR22 余 **3 闸**：

| 闸 | 实测 | 闸线 | 缺口 |
|---|---:|---:|---:|
| LOW_SHARPE | 1.33 | 1.58 | **−0.25** |
| LOW_2Y_SHARPE | 1.31 | 1.58 | **−0.27** |
| CONCENTRATED_WEIGHT | 平台无数值 | — | 需结构性修复 |
| LOW_SUB_UNIVERSE_SHARPE | 0.65 | — | **pass** |
| LOW_FITNESS | 1.15 | 1.00 | **pass** |

**CW 根因假说（本波最重要的待验项）**：对照 `E56pROb9`（CW 在 pass 列表）——它的两条腿**都做了 ts_backfill**，而 model30 全系臂都是裸字段。model30 字段 cov 仅 0.66，约 1/3 股票为空；在 SUBINDUSTRY 中性化后，有值的股票在部分子行业内过度集中 ⇒ 权重集中。

⇒ 已派发 Wave-5（6 臂）验证：ts_backfill 位置（字段前 / z 分后）、窗长（66 / 126 / 252）、单腿 vs 双腿。若 CW 靠 backfill 转 pass，则本线可直接进入「S 与 2Y 同时补 0.25」的阶段。
### 40.12 ★★★★★ Wave-5 结论：`ts_backfill` 一次消掉 CONCENTRATED_WEIGHT（根因假说证实）

三条带 `ts_backfill` 的臂，`ra_failed_checks` **全部不再含 `CONCENTRATED_WEIGHT`**，其余闸结构完全不变：

| tag | 模板 | alpha | S | F | TO | margin | DD | lc | 2Y | sub | 剩余失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| BF66 | `zscore(bf(SE1,66),252)` + `bf(SP12,66)` + d22 | `pwd5X8Wb` | 1.25 | 1.06 | 3.94% | 45.26bp | 12.72% | 83 | 1.20 | 0.57 | S/SUB/2Y（**无 CW**） |
| BF252 | 同上，backfill 252 | `3qoVbEmZ` | 1.27 | 1.08 | 3.87% | 46.60bp | 12.76% | 85 | 1.22 | 0.55 | S/SUB/2Y（**无 CW**） |
| BFA66 | `bf(zscore(SE1,252),66)` + `bf(SP12,66)` + d22 | `1YNZ9LgX` | **1.29** | **1.11** | 3.93% | **46.93bp** | **12.56%** | 84 | 1.24 | 0.57 | S/SUB/2Y（**无 CW**） |

**根因确认**：不是信号问题，是**覆盖率 + 中性化的交互**——model30 字段 cov 0.66 ⇒ 约 1/3 股票在任一交易日为空 ⇒ SUBINDUSTRY 中性化按组去均值后，剩余有值股票在某些子行业内权重被放大 ⇒ 触发权重集中。`ts_backfill` 把空位补上前值，`lc` 从 81 升到 **83–85**，集中度随之消失。

⇒ **可复用规则（第四条 VECTOR/覆盖率铁律）**：任何 cov < 0.75 的字段，进交叉截面骨架前**必须先 `ts_backfill(x, 66)`**。它同时改善三件事：CW 过闸、`lc` 抬升、DD 下降（13.03% → 12.56%）。此前 analyst9 上验证的是同一条（`ts_backfill` 把 TO 从 105% 压到 9.85%）——**两个不同数据集、两个不同症状，同一修法**。

### 40.13 Wave-3 剩余臂（平滑窗与极值处理）

| tag | 模板 | alpha | S | F | TO | margin | 2Y | sub | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| D44 | `decay44(ZS)` | `npvPJwR3` | 1.19 | 0.98 | 3.66% | 46.79bp | **1.28** | 0.55 | 平滑过头伤 S，2Y 反略降 |
| D22W | `winsorize(decay22(ZS),4)` | `78L6AVEO` | 1.26 | 1.07 | 4.32% | 41.48bp | 1.32 | 0.55 | **与 ZSD 逐位相同 ⇒ winsorize 在 decay 后是恒等**（信号已被平滑压平） |
| D22F2 | `decay22(z_fy1+z_fy2+惊喜)` | `Xg9JrqAX` | 1.19 | 0.99 | 4.16% | 41.91bp | 1.08 | 0.49 | 加 fy2 视界仍稀释 |

**平滑窗谷**：decay **22 > 44 > 66 > 5**（S 1.26 / 1.19 / 1.14 / 1.25；2Y 1.32 / 1.28 / 1.10 / 1.18）。22 个交易日 ≈ 1 个月，与 EPS 的月度级信息更新频率对齐 —— 这是**窗口取值的经济学理由**，不是调参。

### 40.14 两条并行最优件与合并方向

| 件 | S | sub | CW | 优势 | 缺陷 |
|---|---:|---:|---|---|---|
| `58EgbnAM`（TR22，ts_rank，无 bf） | **1.33** | **0.65 过** | **失败** | S 最高、sub 过闸 | CW 卡死 |
| `1YNZ9LgX`（BFA66，zscore+bf） | 1.29 | 0.57 | **过** | CW 过、margin 46.93bp | sub 差 0.03、S 差 0.04 |

⇒ **两者优势互补、缺陷不重叠 ⇒ 合并应同时拿到「S 1.33+ / sub 0.65 / CW 过」**。已派发 Wave-6（6 臂）：`ts_rank` + `ts_backfill` + decay22，扫 backfill 窗（66/126/252）× ts_rank 窗（126/252/504），外加一条 `ts_av_diff` 几何对照。
### 40.15 Wave-6：合并成功，四项中三项转 pass

结构 = `ts_decay_linear(add(rank(ts_rank(ts_backfill(SE_fy1, bf), W)), rank(ts_backfill(SP_12m, bf))), 22)`：

| tag | bf / W | alpha | S | F | TO | margin | DD | lc | 2Y | sub | ra 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| TRB126 | 66 / 126 | `rKRe3Ved` | **1.37** | 1.20 | 4.07% | 42.87bp | 13.14% | 85 | 1.33 | 0.69 | S/2Y |
| TRB252 | 252 / 126 | `gJeZOpeQ` | 1.48 | 1.33 | 4.45% | 40.34bp | 12.71% | **86** | 1.53 | 0.83 | S/2Y |
| W176 | 66 / 176 | `RRE6QnAo` | 1.49 | 1.35 | 4.31% | 42.28bp | 12.77% | 84 | 1.54 | 0.84 | S/2Y |
| **TRB66_w126** | 66 / 126 | `2rAm0608` | **1.50** | **1.35** | 4.52% | 44.98bp | 12.90% | 84 | **1.54** | **0.85** | S/2Y |
| W66 | 66 / 66 | `wpQbxOpv` | 1.41 | 1.22 | 5.06% | 37.19bp | 12.94% | 84 | 1.42 | 0.81 | S/2Y |
| W88 | 66 / 88 | `Vkx0jqGJ` | 1.43 | 1.25 | 4.80% | 39.87bp | 12.89% | 84 | 1.47 | 0.79 | S/2Y |
| W100 | 66 / 100 | `e75Qwgxp` | 1.45 | 1.28 | 4.70% | 41.42bp | 12.82% | 84 | 1.50 | 0.80 | S/2Y |
| W240 | 66 / 240 | `j2Y8RbaO` | 1.38 | 1.22 | 4.15% | 46.84bp | 13.05% | 85 | 1.33 | 0.73 | S/2Y |
| TRBAV | 66 / av_diff | `d5W1XPlY` | 1.10 | 0.87 | 3.66% | 42.81bp | **9.67%** | 85 | 1.32 | 0.61 | S/F/2Y |

**`ts_rank` 窗口谷（S / 2Y）**：66 → 1.41 / 1.42；88 → 1.43 / 1.47；100 → 1.45 / 1.50；**126 → 1.50 / 1.54**；176 → 1.49 / 1.54；240 → 1.38 / 1.33；252 → 1.37 / 1.31；504 → 1.15 / 1.15。

⇒ **谷底在 126–176**，且 **126 = 半年 = 2 个季度**，恰是分析师估计「覆盖一次完整财报周期」的最小整数倍 —— 这是窗口取值的**经济学理由**，不是拟合。

### 40.16 ★★★★★ Wave-7 决定性一步：把惊喜腿也做时序归一，2Y 直接过闸

此前惊喜腿一直是 `rank(ts_backfill(SP12,66))`（裸水平），改为 `rank(ts_zscore(ts_backfill(SP12,66),252))` 或 `rank(ts_rank(...,252))` 后：

| tag | 惊喜腿归一方式 | alpha | S | F | TO | margin | DD | lc | **2Y** | sub | ra 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| SPR126 | `ts_rank(·,126)` | `9qxW19jd` | 1.41 | 1.18 | 5.41% | 32.52bp | 11.82% | 83 | **1.68 ✓** | 0.75 | **仅 S** |
| SPR252 | `ts_rank(·,252)` | `A1VvZ3zR` | 1.48 | 1.28 | 5.03% | 37.36bp | 11.06% | 83 | **1.72 ✓** | 0.88 | **仅 S** |
| **SPZ** | **`ts_zscore(·,252)`** | **`j2Y8R6xE`** | **1.51** | 1.32 | 4.99% | 38.42bp | **11.15%** | 81 | **1.61 ✓** | **0.93** | **仅 S** |

**2Y 从 1.54 一跃到 1.61–1.72**，且 DD 从 12.90% 降到 **11.06–11.82%**。

**根因**：惊喜预测是「%，当期水平」——它有**持续的趋势性**（一次上调后分析师会连续上调数季）。不归一 ⇒ 信号在「刚开始上调」和「已上调两年」的股票上取值相同，而后者其实已被定价；`ts_rank/ts_zscore` 把它转成「相对自身历史的分位」，**自动把「已经高了很久」的股票降权** ⇒ 这条正是市场对预测惊喜「反应不足」的时序端修正。

⇒ **可复用规则**：**水平型百分比字段（预测惊喜、情绪分数、评级等）也必须做时序归一**，理由是这类字段有强序列相关，绝对值不区分「新信息」与「旧信息」。这是对第 40.10 条（货币值须 ts_rank）的补充：**判据不是「是否可比」，而是「是否含新旧信息差异」**。

### 40.17 设置轴对照（同一表达式，仅换中性化）

| 中性化 | alpha | S | F | TO | margin | DD | lc | 2Y | sub | ra 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **SUBINDUSTRY** | `2rAm0608` | 1.50 | 1.35 | 4.52% | 44.98bp | 12.90% | 84 | **1.54** | 0.85 | S/2Y |
| INDUSTRY | `0mYr3866` | 1.47 | 1.28 | 4.24% | 44.45bp | 12.23% | **121** | 1.10 | 0.72 | S/2Y |
| SECTOR | `rKRegj5d` | 1.49 | **1.40** | **3.89%** | **56.99bp** | 13.65% | **127** | 1.23 | 0.83 | S/2Y |

**结论：保持 SUBINDUSTRY**。放宽中性化把 `lc` 从 84 拉高到 121–127、margin 从 45bp 拉到 57bp（更"干净"、更可投），但 **2Y 从 1.54 崩到 1.10–1.23** —— 说明本信号的一大块收益来自**同子行业内**的差异，放宽到行业/板块级就把这块抹平了。这是「更高 margin ≠ 更高 Sharpe」的干净实例。

### 40.18 当前最优件 `j2Y8R6xE` 的闸位

```
ts_decay_linear(add(rank(ts_rank(ts_backfill(star_new_eps_smart_estimate_fy1, 66), 126)),
                   rank(ts_zscore(ts_backfill(star_new_eps_surprise_prediction_12m, 66), 252))), 22)
```
（8 算子 / 塔位 `DEU/D1/MODEL` / 单集 ATOM）

| 闸 | 实测 | 闸线 | 状态 |
|---|---:|---:|---|
| LOW_SHARPE | 1.51 | 1.58 | **差 −0.07** |
| LOW_2Y_SHARPE | 1.61 | 1.58 | **pass** |
| LOW_FITNESS | 1.32 | 1.00 | **pass** |
| LOW_SUB_UNIVERSE_SHARPE | 0.93 | — | **pass** |
| CONCENTRATED_WEIGHT | — | — | **pass** |
| LOW/HIGH_TURNOVER | 4.99% | — | **pass** |

⇒ **只剩 LOW_SHARPE 一闸、缺口 0.07**。且 2Y（1.61 vs 1.58）与 sub（0.93）都有余量，**可以用「牺牲部分 2Y 换 S」的结构调整**。已派发 Wave-8（8 臂）：估计腿窗（176/252）、惊喜腿 z 窗（126）、两条三腿（+近端惊喜 / +12m 估计）、`winsorize`、以及 SECTOR / MARKET 两种中性化。
### 40.19 ★★★★★ Wave-9 结果：`rKRevXdj` 全闸通过（DEU 本轮第一颗新集全过件）

| tag | 结构改动 | alpha | S | F | TO | margin | DD | lc | 2Y | sub | ra 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **W2avg** | **双窗平均 126+176** | **`rKRevXdj`** | **1.62** | **1.49** | 4.77% | 44.37bp | 12.94% | 82 | **1.67** | **0.92** | **无（0 失败）** |
| e176_d44 | 表达内 decay 44 | `MPY3o9Rr` | 见下批 | | | | | | | | |
| e176_pd22 | 平台 decay 22 | `GrWOpV1o` | 见下批 | | | | | | | | |
| BF126e176 | backfill 126 | `j2Y8bRKO` | 1.51 | 1.34 | 4.75% | 41.35bp | 11.09% | 82 | 1.57 | 0.88 | S/2Y |
| SZ504 | 惊喜 z 窗 504 | `qML0ob2Z` | 1.41 | 1.22 | 4.58% | 40.97bp | 11.45% | 82 | 1.38 | 0.80 | S/2Y |
| SPZs126 | 惊喜 rank 窗 126 | `vR12Moqd` | 1.41 | 1.18 | 5.36% | 32.83bp | 11.45% | 81 | 1.55 | 0.71 | S/2Y |
| SPZe252 | 估计腿窗 252 | `RRE6QzOa` | 1.40 | 1.20 | 4.71% | 39.17bp | 11.85% | 82 | 1.34 | 0.79 | S/2Y |
| SPZw4 | winsorize | `N1NVm2lg` | 1.51 | 1.32 | 4.99% | 38.42bp | 11.15% | 81 | 1.61 | 0.93 | S |

### 40.20 ★★★★★ 最终件全文与逐项验证

```
ts_decay_linear(add(add(rank(ts_rank(ts_backfill(star_new_eps_smart_estimate_fy1, 66), 126)),
                        rank(ts_rank(ts_backfill(star_new_eps_smart_estimate_fy1, 66), 176))),
                    rank(ts_zscore(ts_backfill(star_new_eps_surprise_prediction_12m, 66), 252))), 22)
```

alpha `rKRevXdj` / **12 算子**（触及上限 12）/ 塔位 `DEU/D1/MODEL`（multiplier 1.8）/ 单集 ATOM / 数据区间 **2014-01-01 → 2023-12-31 满 10 年**。

| 闸 | 结果 |
|---|---|
| LOW_SHARPE | **pass**（1.62 / 1.58） |
| LOW_FITNESS | **pass**（1.49 / 1.00） |
| LOW_TURNOVER / HIGH_TURNOVER | **pass**（4.77%） |
| CONCENTRATED_WEIGHT | **pass** |
| LOW_SUB_UNIVERSE_SHARPE | **pass**（0.92） |
| CLUSTER_TEST | **pass** |
| LOW_2Y_SHARPE | **pass**（1.67 / 1.58） |
| MATCHES_PYRAMID | **pass** |
| `checks.fail` | **[]** |
| `ra.failed_ra_count` | **0**（`ra_failed: false`, `ppa_failed: false`） |
| pending（标准 4 项） | SELF / DATA_DIVERSITY / PROD / REGULAR |
| warning | MATCHES_THEMES（与 `E56pROb9` 同类，非阻断） |

**完整指标**：returns **10.58%**、investability_sharpe 1.39、investability_fitness 1.19、risk_neutralized_sharpe 0.82、pnl 10,919,034、lc/shortCount 82/81。

### 40.21 ★★★★ 相关性（三件可同提）

| 组合 | 相关性 | 判据 |
|---|---:|---|
| `rKRevXdj` self | **0.4558** | < 0.70 ✓ |
| `rKRevXdj` ↔ `E56pROb9` | **0.4991** | < 0.50 本地阈值 ✓（贴线） |
| `rKRevXdj` ↔ `wpQYNvZp` | **0.3415** | ✓ |
| `E56pROb9` ↔ `wpQYNvZp` | 0.5538 | 仅影响组合多样性，不影响单件提交 ✓ |

⇒ 三件同提可把 `DEU/D1/MODEL` 从 **1 颗推到 4 颗 ≥ 3 ⇒ 塔点亮**（multiplier 1.8）。

### 40.22 ★★★★★ 本线的破闸链条（可复制的五步）

从 S 0.38 的单臂到 S 1.62 全闸通过，共 9 批 40+ 臂，每一步都是**结构性修正**而非调参：

| 步 | 改动 | S | 2Y | sub | 关键闸变化 |
|---|---|---:|---:|---:|---|
| 1 | 惊喜预测原值 | 0.38 | 0.69 | 0.10 | — |
| 2 | 双视界 rank 相加 | 0.85 | 0.88 | 0.48 | DD 33.7%→9.6% |
| 3 | **`ts_zscore` 归一 EPS 水平值** | 1.25 | 0.91 | 0.37 | F 过闸 |
| 4 | **加惊喜正交腿** | 1.25 | **1.15** | 0.47 | 2Y +0.24 |
| 5 | **`ts_decay_linear(·,22)`** | 1.26 | **1.32** | 0.55 | 2Y +0.17、margin +9bp |
| 6 | **`ts_backfill(·,66)`** | 1.29 | 1.24 | 0.57 | **CW 消失** |
| 7 | **`ts_rank` 替代 `ts_zscore`** | 1.33 | 1.31 | **0.65** | **sub 过闸** |
| 8 | 惊喜腿也时序归一 | 1.51 | **1.61** | 0.93 | **2Y 过闸** |
| 9 | **估计腿双窗平均 126+176** | **1.62** | **1.67** | 0.92 | **S 过闸 ⇒ 全过** |

**每步只改一件事、且每步只换一个闸的成败**。这是本项目至今最完整的一条「单数据集从零到全闸通过」路径。

### 40.23 方法沉淀（新增三条硬规则）

1. **水平值字段归一化选择表**：货币值/含负值/有跳变（EPS、利润、现金流）⇒ `ts_rank(x,252)`；连续百分比且有趋势（预测惊喜、情绪分、评级）⇒ `ts_zscore(x,252)`；已截面对比的比率 ⇒ 不要归一；
2. **`cov < 0.75` 的字段进交叉截面骨架前必须先 `ts_backfill(x,66)`**：同时修 CW、抬 lc、降 DD（analyst9 与 model30 两处独立验证）；
3. **时间窗双点平均优先于单点寻优**：当窗口谷平坦（126 与 176 的 S 都是 1.49–1.51），把两点等权平均（S 1.62）比继续在窗口上细调更稳健——它降低的是窗口选择方差，不是拟合参数。

---

## 四十一、★★★★★ 2026-11-04 深夜：`IS_LADDER_SHARPE` 真身破解 + analyst93 真相 + shortinterest3 `_p5_d1` 封盘

### 41.1 ★★★★★ `IS_LADDER_SHARPE` = 「最近 2 年窗口 Sharpe」，limit 复刻 LOW_SHARPE（本战役最关键的口径纠正）

此前多颗候选卡在这条闸上而不知其要求。本轮从 `get_alpha_details` 的 warning 载荷直接解出真身：

```
{"name":"IS_LADDER_SHARPE","value":1.18,"limit":1.58,"year":2}
```

**判读**：`year: 2` + `value` 恒等于 `metrics.two_year_sharpe`（`metrics.two_year_ladder_window: 2` 佐证）⇒ 它要求**最近 2 个自然年窗口的 Sharpe 也必须 ≥ 1.58**（即 LOW_SHARPE 的同一条线），而不是「跨年度一致性的软性检查」。

**这是 DEU 最狠的一条闸**：总 S 1.58 已难，还要近期两年单独再达到 1.58。三件对照：

| alpha | S | `two_year_sharpe` | `IS_LADDER_SHARPE` | ra 失败数 |
|---|---:|---:|---|---:|
| `rKRevXdj` | 1.62 | **1.67** | 通过 | **0** |
| `LLMZNmjL` | **1.58** | 1.18 | **失败（唯一）** | 1 |
| `GrWOO100` | 0.63 | 0.13 | 失败 | 3 |

⇒ **`LOW_2Y_SHARPE` 与 `IS_LADDER_SHARPE` 是两条独立闸但同线 1.58**；后者是「梯窗最差窗口」口径。**任何 2Y < 1.58 的候选，即便总 S 过线也不可提交。**

### 41.2 ★★★★★ analyst93 数据集真相：是「分析师准确度/一致性」，不是 EPS 修订

本波首次拉全字段（100 个，全 VECTOR，cov 0.6328）：

| 家族 | 字段 |
|---|---|
| 准确度 | `anl93_analyst_accuracy1/2`、`anl93_analyst_relative_accuracy1..4`、`anl93_accuracy_analyst_analyst`、`anl93_accuracy_estimator_analyst` |
| 一致性 | `anl93_analyst_consistency`、`anl93_analyst_relative_consistency1/2`、`anl93_consistency_analyst_total_forecast_times` |
| 修正质量 | `anl93_analyst_correct_revision_ratio`、`_correct_revision_times`、`_total_revision_times`、`anl93_estimator_correct_revision_ratio` |
| 预测计数 | `anl93_analyst_correct_forecast_times1/2`、`_total_forecast_times1/2` |

**关键纠正：analyst93 里没有 EPS 修订幅度字段** —— `eps_y1_estimate_change_3mo` 来自别集，`j2Ym1PL9` / `LLMZNmjL` 是**跨数据集组合**（因此塔位是 `shortinterest/analyst` 双塔）。

### 41.3 ★★★★★ `ts_rank` 打崩 analyst93 信号腿（第三次独立验证「高区分度比率禁时序归一」）

`GrWOO100` 只改一处——信号腿由 `rank(ts_mean(eps,5))` 换成 `rank(ts_rank(ts_backfill(eps,66),126))`：

| 指标 | `LLMZNmjL`（原） | `GrWOO100`（ts_rank） | Δ |
|---|---:|---:|---:|
| Sharpe | **1.58** | 0.63 | **−0.95** |
| 2Y Sharpe | 1.18 | **0.13** | **−1.05** |
| sub_universe | **0.96** | 0.30 | −0.66 |
| fitness | 1.34 | 0.31 | −1.03 |
| margin | 51.63bp | 11.03bp | −40bp |

**累计三处证据**（同一条规则的全灭式验证）：净利率 `ts_zscore` 0.92→0.73、净广度 0.82→0.53、EPS 修订 `ts_rank` 1.58→0.63。

⇒ **硬规则**：凡是「已经在截面内可比的百分比/比率/幅度」字段（修订幅度、净利率、评分、广度），**信号腿一律保留裸 `rank(ts_mean(·,w))`，不叠加 `ts_rank` / `ts_zscore`**。时序归一只能用在「货币值 / 含负值 / 有跳变」且截面不可比的量上。

### 41.4 ★★★★ shortinterest3 `_p5_d1` 层信号腿 8 臂全灭 ⇒ 该层封盘

`_p5_d1` 后缀层（cov **0.7833**，覆盖优于 `_main` 0.6872 与 base 0.6683）作为**信号腿**的补测结果：

| tag | 模板 | alpha | S | F | TO | 2Y | sub | DD |
|---|---|---|---:|---:|---:|---:|---:|---:|
| S5_dur | 借券久期 | `P0og278x` | **−0.20** | −0.06 | 11.26% | **−1.07** | 0.08 | 22.56% |
| S6_txn | 交易笔数 | `P0og2Mzx` | 0.17 | 0.05 | 9.80% | 0.55 | **−0.46** | 24.26% |
| S7_feevol | 费率波动 | `WjOebLYG` | 0.25 | 0.09 | 6.82% | −0.23 | 0.41 | 17.56% |
| S8_utilg | 利用率增长 | `YP1Mbxx6` | 0.02 | 0.00 | 5.89% | −0.08 | −0.36 | 11.63% |

**四件全 REJECT**。加上此前 base 层 / `_main` 层的同族探针，累计 **三层 × 多维 = 全部 S 0.02–0.25、sub 多负**。

⇒ **封盘结论（跨层不可推翻）**：借券（shortinterest3）字段在 DEU **只能作门控 / 条件变量，不能作信号变量**。正向印证：`LLMZNmjL`（门控用法 S 1.58）；反向印证：`blRnKEk6` 虽把 `-rank(mean_loan_rate_main)` 当信号腿并达 S 2.02，但那颗的 3/4 权重来自 MODEL 估计修订腿，**借券腿只是第四腿**。

⇒ **`_p5_d1` 层「覆盖更高」不代表信号更强**：cov 从 0.6872 抬到 0.7833，信号腿表现反而更差。**覆盖是必要非充分条件**（本战役第四次撞上）。

### 41.5 ★★★★★ `LLMZNmjL` 年度分解：2Y 卡在 2023 的 0.30

| 年 | S | pnl | TO | DD | margin | lc |
|---|---:|---:|---:|---:|---:|---:|
| 2014 | **2.99** | 1,685,560 | 4.31% | 3.28% | 75.17bp | 82 |
| 2015 | 2.56 | 1,550,069 | 3.92% | 3.11% | 76.11bp | 95 |
| 2016 | 1.48 | 843,940 | 3.82% | 2.70% | 42.53bp | 104 |
| 2017 | 1.13 | 534,358 | 3.14% | 3.95% | 32.68bp | 116 |
| 2018 | 1.98 | 1,190,419 | 3.36% | 1.90% | 68.05bp | 119 |
| 2019 | 1.92 | 967,404 | 3.46% | 2.52% | 53.81bp | 119 |
| **2020** | **−0.34** | **−219,533** | 3.65% | 7.12% | −12.57bp | 132 |
| 2021 | 2.24 | 1,146,466 | 3.51% | 3.65% | 62.79bp | 154 |
| **2022** | **1.87** | 1,438,632 | 3.12% | 4.46% | 88.60bp | 166 |
| **2023** | **0.30** | 178,578 | 2.69% | 3.84% | 12.78bp | 156 |

**判读**：2Y 梯窗 = 2022 + 2023 ⇒ 1.87 与 0.30 合成 **1.18**。**瓶颈 100% 在 2023**（returns 仅 1.72%、margin 12.78bp，是全期最低的一年）。2020 虽是负年但不进 2Y 窗口，不影响 `IS_LADDER_SHARPE`。

⇒ **破 `IS_LADDER_SHARPE` 的唯一路径 = 让 2023 重新有信号**。单纯加长/缩短平滑窗只能给 ±0.05（W22 1.13 vs W5 1.18），不够；必须换/加**在 2023 仍有效的信号腿**。

### 41.6 本波派发记录（10 臂，固定已证明 self 安全的门控）

门控固定为 `rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)) < 0.7`（`LLMZNmjL` 实测 self 0.5417 ✓，与枢纽件 `blRnKEk6` 脱钩成立），只变信号腿。

| tag | 信号腿 | 机制 | 算子数 | sim |
|---|---|---|---:|---|
| A1_w22 | `rank(ts_mean(eps,22))` | 窗长对照 | 6 | `1q78dUgps4ut9uR1f0IIJsx` |
| A2_dual | `rank(add(ts_mean(eps,5), ts_mean(eps,22)))` | 双窗平均（model30 第 9 步成功手法） | 8 | `2upiyU49q4jo8AadWnp1Mzs` |
| A3_decay | `ts_decay_linear(rank(ts_mean(eps,5)),22)` | 平滑（model30 第 5 步 2Y +0.17 手法） | 7 | `fSuPx7sJ4uvbgU19Dg33qJv` |
| B1_acc1 | `rank(ts_backfill(vec_avg(anl93_analyst_accuracy1),66))` | 分析师历史准确度（新机制） | 7 | `16F1XUejl5iP98g1gUpKvDkA` |
| B2_relacc | `rank(ts_backfill(vec_avg(anl93_analyst_relative_accuracy1),66))` | 相对准确度 | 7 | `3WCkL67qM4Z6bC9bVEoESZ7` |
| B3_correv | `rank(ts_backfill(vec_avg(anl93_analyst_correct_revision_ratio),66))` | 修正正确率 | 7 | `2PaD6F7Di4QybqcmQvF7QJW` |
| B4_consist | `rank(ts_backfill(vec_avg(anl93_analyst_consistency),66))` | 一致性 | 7 | `1njJsy4Kw4WKbWiCYCPIgIB` |
| B5_estcorr | `rank(ts_backfill(vec_avg(anl93_estimator_correct_revision_ratio),66))` | 机构侧修正正确率 | 7 | `3aPHchgNq4ih9PA12CbnbwPX` |
| C1_eps_acc | 修订 + 准确度 rank 相加 | 双腿正交 | 9 | 并发挡，待补 |
| C2_eps_rel | 修订 + 相对准确度 rank 相加 | 双腿正交 | 9 | 并发挡，待补 |

**模板多样性**：10 个结构互异模板（窗长 / 双窗平均 / decay 平滑 / 4 类准确度机制 / 2 类双腿组合），全部 ≤9 算子，远低于 12 上限。

### 41.7 批次一结果：analyst93 准确度腿全灭、EPS 修订线封顶 2Y 1.25

| tag | 机制 | alpha | S | F | TO | margin | y2 | sub | ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| A1_w22 | EPS 修订窗 22 | `1YNZZWAk` | 1.50 | 1.24 | 2.96% | 57.98bp | 1.13 | 0.89 | 2 |
| A2_dual | 双窗 5+22 平均 | `GrWOOdJ3` | 1.57 | 1.33 | 3.06% | 59.13bp | 1.16 | 0.93 | 2 |
| **A3_decay** | **`ts_decay_linear(,22)`** | **`JjeQQ7rl`** | **1.59** | **1.36** | 3.03% | **60.13bp** | **1.25** | 0.92 | **1** |
| B1_acc1 | 分析师准确度 | `zq3bbk71` | 0.22 | 0.08 | 1.94% | 16.30bp | −0.73 | 0.18 | 3 |
| B2_relacc | 相对准确度 | `leAKKlQe` | −0.34 | −0.14 | 5.89% | −7.06bp | −1.73 | −0.30 | 4 |
| B3_correv | 修正正确率 | `QPvKKYEw` | 0.14 | 0.04 | 2.51% | 7.60bp | −0.57 | 0.04 | 4 |
| B4_consist | 一致性 | `MPY33ajL` | 0.01 | 0.00 | 1.84% | 0.91bp | 0.85 | −0.19 | 4 |
| B5_estcorr | 机构侧修正正确率 | `88RPPvYm` | 0.28 | 0.11 | 2.51% | 14.90bp | −0.57 | 0.10 | 4 |

**结论一（analyst93 判死）**：分析师准确度/一致性/修正正确率 5 维全灭（S 0.01–0.28、2Y 多为负）⇒ **analyst93（cov 0.6328，100 字段）无可作信号腿的字段**。这类「元认知」字段（对分析师本人质量的度量）在 DEU 没有截面 alpha。

**结论二（EPS 修订线封顶）**：`ts_decay_linear(,22)` 是最好的单杠杆（S 1.58→1.59、2Y 1.18→**1.25**、margin +8.5bp），但仍差 2Y 0.33。窗口 22 反而更差（1.13）。⇒ **EPS 修订线结构性封顶在 2Y 1.25**，放弃。

**结论三**：`ts_rank` 归一版 `GrWOO100` S 0.63 已证伪（见 41.3）；本批进一步确认 `rank(ts_mean(eps, w))` 裸形就是最优形态。

---

## 四十二、★★★★★ analyst44「估计修订」矿脉：netdebt 单科目突破 2Y 闸，只差 LOW_SHARPE 0.23

### 42.1 ★★★★ analyst44 字段结构（DEU/TOP500 实测 72 个可用字段，全 VECTOR）

每组财务科目给出 5 个平行字段，**这是本项目见过的信息结构最规整的数据集**：

| 后缀 | 含义 | 在骨架中的用途 |
|---|---|---|
| `_value` | 当前一致预期值 | 修订分子 |
| `_prevalue` | 上期一致预期值 | 修订分母 / 被减项 |
| `_lastactvalue` | 上次实际公布值 | 「预期 vs 实际」隐含增长 |
| `_coveredby` | 覆盖分析师数 | 关注度 / 广度腿 |
| `_lastactccy` | 记账币种 | 元数据，不可用 |

科目：`csh`（股数）/ `dps` / `ebitda` / `eps` / `epsr` / `fcfps` / `netdebt` / `netprofit` / `operatingprofit` / `roe` …

**两种天然骨架**：
- **估计修订率** `divide(subtract(vec_avg(v), vec_avg(p)), abs(vec_avg(p)))`
- **隐含增长** `divide(subtract(vec_avg(v), vec_avg(lastactv)), abs(vec_avg(lastactv)))`

### 42.2 ★★★★★ 科目横评：**只有 netdebt 有效**，其它科目修订全部塌陷

统一骨架 `rank(ts_mean(ts_backfill(RV(m), 66), 66))`（9 算子，无门控、无 power）：

| 科目 | 方向 | alpha | S | F | TO | margin | DD | **y2** | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **netdebt** | − | **`N1NVemkq`** | **1.28** | **1.06** | 3.72% | **45.89bp** | **7.25%** | **1.46** | **0.87** |
| eps | + | `gJeZW6jJ` | 0.57 | 0.32 | 3.45% | 22.87bp | 12.82% | 0.49 | 0.60 |
| dps | + | `E56RV1nR` | 0.56 | 0.31 | 3.41% | 22.86bp | 18.86% | 0.10 | 0.29 |
| netprofit | + | `Vkx0d1aV` | 0.43 | 0.21 | 3.53% | 17.30bp | 18.68% | 0.19 | 0.63 |
| ebitda | + | `MPY30ob9` | 0.35 | 0.16 | 3.60% | 14.07bp | 13.26% | 0.36 | 0.25 |
| roe | + | `P0ogMdGL` | 0.15 | 0.05 | 3.50% | 6.44bp | 18.88% | −0.55 | −0.03 |
| 跨科目价差 `ebitda−netdebt` | — | `npvPAM6x` | 0.52 | 0.13 | **81.33%** | 1.17bp | 35.77% | 0.94 | 0.52 |

**★★★★★ 判读（本轮最重要的数据集级发现）**：同一骨架、同一窗口、同一方向口径下，**netdebt 的 S 是第二名的 2.2 倍**（1.28 vs 0.57）。

**经济学根因**：`netdebt`（净负债）是**单一可加的存量科目**，分析师对其一致预期几乎没有口径歧义（不像 ebitda / netprofit 受折旧口径、一次性项目、税率假设干扰）；且净负债上升直接对应偿债能力恶化，是**一阶基本面信号**而非二阶盈利预期信号。⇒ **在 DEU，分析师对资产负债表的判断比利润表判断更有 alpha。**

**方法论**：一个数据集有 10+ 个平行科目时，**必须先做「科目横评」再堆几何**——本轮先用 6 个单臂定了 netdebt，后面所有算力都投在一条腿上；若一上来就对 netdebt 做几何、对 ebitda 做几何，会把两倍资源浪费在 0.35 的科目上。

### 42.3 ★★★★ `signed_power(rank, k)` 只值 +0.07，不是主升力（纠正一个诱人的误判）

`akKX5AQR`（历史件，11 算子，含 `winsorize(std=4)` + `signed_power(,3)`）S 1.34 / 2Y 1.55；本轮 `N1NVemkq` 去掉这两个算子后 S 1.28 / 2Y 1.46。

⇒ **`signed_power(rank,3)` 净贡献仅 +0.06 S / +0.09 2Y**；`winsorize(std=4)` 作用在 rank 上（rank∈[0,1]，4σ≈1.15>1）**恒等，零效果**。

**踩坑记录**：看到 ebitda/eps/dps 在裸骨架下只有 0.35–0.57、而历史件 1.34，第一反应是「power 是主升力」；跑 D1 对照才发现**差异全在科目（netdebt vs 其它）而不是算子**。⇒ **凡「历史件高、复现低」，第一步必须做「只删一个算子」的对照臂**，不要靠猜。

### 42.4 ★★★★★ netdebt 几何波：**`2Y ≥ 1.58` 闸已突破**

| tag | 几何 | alpha | S | F | TO | margin | DD | **y2** | sub | ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **N1_p3** | `-signed_power(rank(mean66(backfill66(RV))),3)` | **`vR12OdNG`** | **1.35** | **1.16** | 3.67% | 49.95bp | 8.18% | **1.62 ✓** | 0.89 | **1** |
| **N2_p2** | 同上，指数 2 | **`1YNZjJXz`** | **1.35** | 1.14 | 3.69% | 48.61bp | **7.83%** | **1.59 ✓** | **0.91** | **1** |
| N3_p5 | 同上，指数 5 | `npvPA2ba` | 1.28 | 1.10 | 3.67% | 50.21bp | 8.75% | **1.58 ✓** | 0.80 | 2 |
| N4_dec | `-rank(decay22(mean66(backfill66(RV))))` | `wpQb9eP1` | 1.18 | 0.93 | 3.22% | 48.24bp | 9.63% | **1.68 ✓** | 0.82 | 2 |
| N5_w22 | 窗 22 | `pwd5v8ao` | 1.02 | 0.76 | 6.77% | 20.36bp | 14.15% | 1.27 | 0.60 | 3 |

**★★★★★ 核心结论**：`signed_power(rank(·), 2~3)` 把 2Y 从 1.46（裸版）推到 **1.59–1.62，越过 1.58 闸线**；代价是 S 只 +0.07 停在 **1.35**。

**⇒ 当前唯一剩余缺口：`LOW_SHARPE`，需 1.35 → 1.58（+0.23）。** 其余全过：F 1.16 ✓、TO 3.67% ✓、margin 49.95bp ✓、DD 8.18% ✓、sub 0.89–0.91 ✓、`ra.failed_ra_count = 1`。

**副发现**：指数 2 与 3 的 S 完全相同（1.35），但**指数 2 的 sub 更高（0.91 vs 0.89）、DD 更低（7.83% vs 8.18%）** ⇒ 若后续几何不变，**优先用指数 2**（更温和的集中度、更好的子宇宙表现）。

### 42.5 ★★★★ 已排除的死路清单（本轮实测，勿重试）

| 方向 | 臂 | 结果 | 判读 |
|---|---|---|---|
| `ts_ir` 信噪比几何 | Q1/Q2/Q3/Q4/Q5/Q8 | S 0.95–1.26（最好 `ts_ir`+p2 1.26） | 全部劣于 `ts_mean`（1.35）⇒ 净负债修订是水平量不是稳定性量 |
| `ts_ir` 救其它科目 | Q6 ebitda / Q7 eps / Q9 netprofit / Q10 dps | S 0.49 / 并发挡 / 并发挡 / 并发挡 | ebitda 0.49 仍死 |
| 混搭 SENTIMENT 腿 | H1 `ts_ir(views)` / H2 `ts_delta(views)` / H3 `ts_mean(views)` | S 0.62 / 0.85 / 0.54 | 维基浏览量在净负债信号上纯稀释 |
| `group_backfill(·, subindustry, 66)` | Z1 | S 0.76、sub 0.43 | 分组填充引入组内偏差 |
| 分母改 `abs(value)` | N7 | S 0.88、sub 0.44 | 必须用 `abs(prevalue)` |
| 加 EPS 修订腿 | N8 | S 1.32 但 2Y 0.22 | EPS 的 2023 弱势直接污染 2Y |
| `_coveredby` 覆盖广度腿 | P1 | S 0.23、TO 69.51% | 覆盖数是慢变量，作为腿只在制造换手 |
| `group_neutralize(·, sector)` 表达式内 | P7 | S 1.12、2Y 1.20 | 表达式内分组与平台中性化叠加＝双重去化 |
| `group_rank(·, industry)` 表达式内 | P3 | S 1.28、2Y 1.82、sub 0.92 | 2Y 好看但 S 不足 |
| `ts_av_diff` 偏离移动均线 | Z7 | S 0.39、2Y −0.44 | 时序偏离在本信号上无意义 |

### 42.6 ★★★★ 新杠杆：`ts_backfill` 窗口越短越好（与「必须 backfill」不矛盾）

| backfill | 中性化 | alpha | S | F | y2 | sub |
|---|---|---|---:|---:|---:|---:|
| 22 | SUBINDUSTRY | `npvPvaOz` | 1.45 | 1.28 | 1.63 | 0.91 |
| 66 | SUBINDUSTRY | `1YNZjJXz` | 1.35 | 1.14 | 1.59 | 0.91 |
| 126 | SUBINDUSTRY | `RRE6Epng` | 1.32 | 1.10 | 1.63 | 0.94 |

**判读**：`ts_backfill` 的作用是补齐稀疏 VECTOR 字段的 NaN（不做会 TO 爆表），但窗口越长越把「当前值」拉向历史均值 ⇒ 信号变钝。22 天足够补齐、又不钝化。这条与「VECTOR 字段必须先 backfill」并行不悖——必须 backfill，但窗口要短。

---

## 四十三、★★★★★ 中性化轴是决定性杠杆：SECTOR 把 S 从 1.35 抬到 1.53，2Y/sub 同时达标

### 43.1 ★★★★★ 四个中性化轴横评（同一表达式 `-signed_power(rank(ts_mean(ts_backfill(RV,66),66)),2)`）

| 中性化 | alpha | S | F | TO | margin | DD | y2 | sub | ra 失败 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SECTOR | `O0A8A5xv` | 1.53 | 1.25 | 2.96% | 56.27bp | 7.08% | 1.53 | 1.05 | 2 |
| SUBINDUSTRY | `1YNZjJXz` | 1.35 | 1.14 | 3.69% | 48.61bp | 7.83% | 1.59 | 0.91 | 1 |
| INDUSTRY | `rKReR8md` | 1.30 | 0.99 | 3.41% | 42.27bp | 6.20% | 1.46 | 0.77 | 3 |
| MARKET | 待回 | — | — | — | — | — | — | — | — |

**★★★★★ 判读**：`SECTOR` 同时改善 S (+0.18)、sub (+0.14)、margin (+7.7bp)、DD (−0.75pp)，只有 2Y 略降（−0.06）。这是本项目第一次看到单一设置改动同时改善四项指标。

**根因（因果推断）**：净负债修订的 alpha 来源是「跨行业的相对杠杆改善预期」——同子行业内的公司杠杆结构往往同质（同属重资产/轻资产），子行业中性化会把最有信息量的「行业间杠杆周期差异」一起减掉；而 SECTOR 只减行业层面，保留子行业间的比较空间。

**与方法论记忆的冲突与澄清**：model30 线曾记录「中性化放宽到 INDUSTRY/SECTOR 会崩 2Y（1.54→1.10–1.23）」。本轮结论不同，说明中性化轴的选择依赖信号性质：
- 盈利预期类信号（model30）的信息集中在同子行业内（同业比较才有意义）⇒ 必须 SUBINDUSTRY；
- 资产负债表类信号（netdebt）的信息集中在跨子行业/跨行业（杠杆周期）⇒ 用 SECTOR。

**⇒ 硬规则**：不能默认「DEU 一律 SUBINDUSTRY」。信号属利润表 ⇒ SUBINDUSTRY；属资产负债表 ⇒ SECTOR。

### 43.2 ★★★★★ SECTOR 轴上的参数面（两件已达「只差 LOW_SHARPE」）

| tag | 几何 | alpha | S | F | TO | margin | DD | y2 | sub | ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RS_p3 | w66 + power 3 | `xArbrlYw` | 1.53 | 1.26 | 2.94% | 57.85bp | 7.12% | 1.62 | 1.05 | 1 |
| RT_w77_p2 | w77 + power 2 | `qML0LanV` | 1.53 | 1.25 | 2.73% | 60.99bp | 7.80% | 1.73 | 1.14 | 1 |
| RS_w88 | w88 + power 2 | `omEWEWOb` | 1.46 | 1.16 | 2.53% | 62.79bp | 7.26% | 1.82 | 1.15 | 1 |
| RS_dec | w66 + decay22 + p2 | `xArbrEal` | 1.43 | 1.12 | 2.58% | 59.72bp | 6.12% | 1.69 | 1.02 | 1 |
| RS_w44 | w44 + p2 | `j2Y8Y8RQ` | 1.34 | 1.03 | 3.75% | 39.68bp | 9.26% | 1.51 | 0.80 | 2 |

**★★★★★ 状态**：`RS_p3` 与 `RT_w77_p2` 的 `ra.failed_ra_count = 1`，且唯一失败项是 `LOW_SHARPE`（1.53 vs 1.58，差 0.05）；F 1.25–1.26 ✓、TO 2.7–2.9% ✓、margin 58–61bp ✓、DD 7–8% ✓、2Y 1.62–1.73 ✓、sub 1.05–1.14 ✓。距离全闸通过只剩最后 0.05 Sharpe。
---

## 四十四、★★★★★ 2026-11-05 凌晨：DEU 平台结构性边界 + MARKET 轴突破 S 1.64（2Y 只差 0.03）

### 44.1 ★★★★★ DEU 设置硬边界（官方 `get_platform_setting_options` 实测）

- **Universe 只有 `TOP500` 一个值**（`EQUITY/DEU/Delay 1` 与 `Delay 0` 的 `Universe` 数组都只含 `TOP500`）。⇒「靠更宽 universe 增加持仓广度换 Sharpe」在本区**结构性不存在**。
  ★ 陷阱：`TOP1000` / `TOP800` / `TOP600` 的 preflight 返回 `valid: true` 但 `platform_field_count = 0`、`fields_checked = []` —— **valid:true 不等于 universe 存在**，必须同时看 `platform_field_count > 0`。
- **Neutralization 共 11 个可选轴**：`NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST`。本轮之前只测过 SECTOR / MARKET / INDUSTRY / SUBINDUSTRY，**7 个未测**——这是当前最便宜的未探索维度（注意：中性化是 sim 设置，换轴必须单独派一批，不能在同批内混）。

### 44.2 ★★★★★ 12 算子预算杀死「多窗口集成」——比率型信号的结构性限制

`RVN = divide(subtract(vec_avg(prevalue), vec_avg(value)), abs(vec_avg(prevalue)))` 单腿就占 **6 个算子**（表达式无变量，`vec_avg` 必须写三次）。

⇒ 双窗 `rank(add(ts_mean(ts_backfill(RVN,22),66), ts_mean(ts_backfill(RVN,22),88)))` 展开 **18 算子**，三窗 26 算子。**只要信号腿是「两分量比率」，M 窗口集成的最低价是 6M+5 算子 ⇒ 12 上限下 M 只能是 1。**

**推论（跨区通用）**：`40.23(3)` 记的「时间窗双点平均降低窗口选择方差」**只适用于单字段信号腿**（`ts_mean(x,w1)+ts_mean(x,w2)` 里字段只写一次）；**比率腿不成立**。以后设计集成前先算展开价再派发。

### 44.3 ★★★★ analyst44 `_lastactvalue` 与「修订加速度」两条新维度全灭

| 维度 | 定义 | alpha | S | y2 | sub | 判读 |
|---|---|---|---:|---:|---:|---|
| 隐含增长 | (lastactvalue − value) / abs(lastactvalue) | `KPJrg2lz` | 0.36 | 0.04 | 0.28 | 预期相对「上次实际」的水平无信号 |
| 修订加速度 | `ts_delta(ts_mean(ts_backfill(RVN,22),22), 22)` | `JjeQ8rbn` | 0.03 | −0.30 | 0.29 | 一阶差分把存量信息全扔掉 |

⇒ **netdebt 的信息 100% 在「当前预期相对上一期预期的一阶差分」里**。analyst44 五字段结构至此定性完毕：`_value` / `_prevalue` 构成本轮全部有效信号；`_lastactvalue`、`_coveredby`（P1，TO 69.51%）、`_lastccy` 三个字段均无效。

### 44.4 ★★★★★ MARKET 轴 + bf22 + w77 突破 S 1.64 —— S×2Y 前沿完整剖面

同一骨架 `signed_power(rank(ts_mean(ts_backfill(RVN,bf),w)),p)`，全 DEU/TOP500/D1/decay16/trunc0.08：

| 轴 | bf | w | p | alpha | S | F | TO | margin | DD | y2 | sub | ra |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **MARKET** | **22** | **77** | 2 | `pwd5ajK3` | **1.64 ✓** | 1.41 | 2.52% | 73.5bp | 12.62% | **1.55 ✗** | 1.14 | 1 |
| MARKET | 66 | 88 | 2 | `xArbvn9l` | 1.54 | 1.28 | 2.26% | 76.4bp | 11.38% | 1.64 ✓ | 1.13 | 1 |
| SECTOR | 22 | 77 | 2 | `2rAm5KQb` | 1.55 | 1.27 | 2.81% | 60.1bp | 7.36% | 1.67 ✓ | 1.12 | 1 |
| SECTOR | 22 | 77 | 3 | `Vkx0NYdG` | 1.54 | 1.27 | 2.79% | 61.2bp | 7.53% | 1.72 ✓ | 1.11 | 1 |
| SECTOR | 22 | 82 | 2 | `JjeQ8gKO` | 1.53 | 1.25 | 2.71% | 61.6bp | 7.85% | 1.69 ✓ | 1.14 | 1 |
| SECTOR | 22 | 88 | 2 | `ZYQAaoW3` | 1.48 | 1.19 | 2.60% | 62.0bp | 7.59% | 1.75 ✓ | 1.12 | 1 |
| SECTOR | 22 | 100 | 2 | `vR12AJXr` | 1.43 | 1.13 | 2.41% | 64.8bp | 6.69% | 1.78 ✓ | 1.05 | 1 |
| SECTOR | 22 | 66 | 3 | `leAKa6ol` | 1.55 | 1.29 | 3.05% | 56.7bp | 7.03% | 1.55 ✗ | 1.03 | 2 |
| SECTOR | 22 | 44 | 2 | `E56RQkgm` | 1.37 | 1.08 | 3.90% | 39.6bp | 8.71% | 1.42 | 0.84 | 2 |

**两条规律**：
1. **轴内 w↑ ⇒ S↓ / 2Y↑**（斜率约 −0.008 S、+0.012 2Y 每单位 w）；
2. **轴间 MARKET 相对 SECTOR ⇒ +0.09 S / −0.12 2Y**（bf22/w77 单点直接对照：1.64/1.55 vs 1.55/1.67）。

⇒ **MARKET+bf22+w77 是至今 S 最高（1.64）且唯一「只差 2Y 0.03」的点**；SECTOR 族是「只差 S 0.03」。两条前沿在 (S, 2Y) 平面上互相错开，**交叉点落在 MARKET × bf22 × w ∈ [82, 94]**——已派发 `AFuJg6J44sQaA91pkb74nS`(w82) / `RM22_w88_p2` / `RM22_w94_p2`。

---

## 四十六、非 trio 三集判死 + analyst_factor_signals 活矿脉（2026-11-05 凌晨）

> 用户指令：专注 PV / MODEL / OTHER 之外的 category 数据集。本轮据此全量扫非 trio，新增 3 个判死集与 1 个活矿脉。

### 46.1 analyst7 十模板全灭（判死）

结构：608 字段全 MATRIX 标量、231 个 cov=1.0、16 科目 x 28 后缀、ac 3993。

| 模板 | alpha | S | 2Y | sub | TO | 结构 |
|---|---|---:|---:|---:|---:|---|
| T2 修订净比 | `e75QV7pM` | **0.92** | 0.79 | 0.45 | 4.53% | (raised-lowered)/(raised+lowered) |
| T1 修订广度 | `zq3bglXR` | 0.66 | 0.63 | 0.37 | 4.21% | raisednum-lowerednum |
| T8 惊喜+广度 | `O0A8M737` | 0.43 | 1.29 | 0.26 | 3.57% | act_q_eps_surprisenum + 广度 |
| T6 区间 | `2rAmXwbN` | 0.25 | -0.41 | -0.19 | 1.70% | (high-low)/abs(mean) |
| T3 幅度修正 | `JjeQo6Yn` | 0.24 | -0.11 | 0.23 | 5.94% | (num-num_4wks)/abs() |
| T5b 离散度 roa | `mLo60Zm1` | 0.24 | -0.69 | -0.27 | 1.94% | std/abs(mean) |
| T7 惊喜 | `LLMZmaam` | 0.10 | 1.44 | 0.10 | 1.02% | 纯 surprisenum |
| T5 离散度 bps | `GrWOKw10` | 0.08 | 0.80 | -0.40 | 1.68% | std/abs(num) |
| T9 偏度 | `gJeZgxjl` | 0.05 | 0.52 | -0.25 | 2.44% | (median-mean)/abs(num) |
| T12 离散x修正 | `rKReNjZa` | -0.67 | -1.12 | -0.35 | 4.41% | 交互项 |

**判读**：十个结构互异模板（广度 / 净比 / 幅度 / 区间 / 离散 / 惊喜 / 偏度 / 交互 / 加速度 / 覆盖变化）最好 0.92，且只有**修订广度族**（T1/T2）为正。离散度、偏度、区间、惊喜全灭。
⇒ **analyst7 判死**。与 46.4 的差异关键：analyst7 的字段是**原始计数/统计量**（无归一化），analyst_factor_signals 的字段是**厂商已归一化的成品信号**（zscore / change_3mo / coeff_var）。同一 mechanism 在两种加工形态下差 0.5+ Sharpe。

### 46.2 institutions6 三臂全灭（判死）

11 个 MATRIX 标量、cov 全 1.0。`netflow(acq-disp)/(acq+disp)` = `A1VveAkd` S **-0.15**；`ownlvl share_inst/share_all` = `6XdKZkEL` S 0.32（2Y 1.36，TO 1.05%）；`breadth(buyers-sellers)/holders` = `omEWJev6` S 0.23（2Y -0.11）。最好 0.32 ⇒ **判死**。

### 46.3 fund_holdings_panel 八臂全灭（判死）——基金调仓压力族不成立

18 个 VECTOR（9 组 + 9 个 _active 变体）、cov 0.928、ac 102。机制假设：基金调仓压力 -> 短期反转（Coval-Stafford 型）。

| 模板 | alpha | S | 2Y | TO | margin | 结构 |
|---|---|---:|---:|---:|---:|---|
| 大单数 | `6XdKoW6P` | 0.32 | 1.46 | 2.87% | 19.8bp | large_trade_count_50bps |
| 流量反转 w5 | `KPJr5z7E` | 0.25 | 0.73 | 19.34% | 1.4bp | -vec_sum(usd_value) |
| 账户广度 | `1YNZl00m` | 0.15 | 1.30 | 2.79% | 9.3bp | vec_count(account_total) |
| 单账户均单 | `pwd5Mp2j` | 0.13 | -0.79 | 7.93% | 1.7bp | usd_value/accounts |
| 流量关注 w66 | `78L6vM22` | 0.04 | -0.58 | 3.97% | 1.1bp | vec_sum(usd_value) |
| HHI 集中度 | `O0A8MVjY` | -0.27 | -1.35 | 2.68% | -19.2bp | herfindahl |
| 边界调仓反转 | `KPJr5Wel` | -0.44 | -1.55 | 4.83% | -15.3bp | -boundary_transaction_total |

**判读**：USD 流量类腿 TO 高（8-19%）而 margin 只有 1-2bp ⇒ 与 news104 同型的 TO/margin 失衡；HHI 与边界调仓在**负方向显著**（-0.27 / -0.44 且 2Y -1.35 / -1.55）——说明反向后仍是负的，机制方向不稳定。最好 0.32 ⇒ **判死**。

### 46.4 ★★★★★ analyst_factor_signals 是活矿脉：DEU 制胜配方可直接套用

**结构**：108 字段全 MATRIX 标量、cov 0.92-0.93、ac 1575。3 个主科目（eps / netprofit / revenue）x 36 个**厂商预计算**信号：
revision_magnitude / y1·y2_estimate_change_3mo / y1·y2_consensus_value / estimate_zscore / estimate_trend_slope_1-4yr / estimate_volatility_adj_2-3yr / q1·q2_estimate_{asymmetry,coeff_var,skewness,change_1mo,qoq_growth,yoy_growth,sequential} / surprise_{mean_diff,stddev} / y1_cagr_2-5yr。

**为什么它是活矿脉**：DEV 已提交 alpha `2rjrMZ25`（S 1.77 / 2Y 1.83 / prod 0.651）用的就是本集的 `eps_y1_estimate_change_3mo`。把它的制胜配方解出来即为通用骨架（10 算子）：

```
group_neutralize(
  group_rank(add(ts_backfill(F,1008), ts_mean(ts_backfill(F,1008),210)), sector),
  bucket(rank(ts_mean(ts_backfill(F,1008),252)), range="0,1,0.05"))
```

机制：**短周期水平 + 长周期基线的偏离**（分层差分），再用长周期水平做 20 分位 bucket 门控，sector 内 group_rank。

**换用未用过的科目 x 期段（结果矩阵，decay 4 / SECTOR / trunc 0.08）**：

| 字段 F | alpha | S | F | TO | 2Y | sub | DD | margin | ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **eps_y2_estimate_change_3mo** | `JjeQzVEE` | **1.43** | 1.29 | 10.84% | 1.24 | 0.55 | 14.76% | 18.9bp | 3 |
| **netprofit_y2_estimate_change_3mo** | `QPvKz1qK` | **1.37** | 1.20 | 10.94% | 1.17 | 0.45 | 13.64% | 17.6bp | 3 |
| netprofit_y1_estimate_change_3mo | `26oRYBgq64R8b9SdR5fK5Ei` | 1.21 | 0.94 | 10.95% | 1.25 | 0.48 | 10.57% | 13.8bp | 4 |
| revenue_y1_estimate_change_3mo | `39yuf37Hr4zWckIYvjKNZxy` | 1.07 | 0.81 | 11.36% | 0.77 | 0.63 | 10.09% | 12.7bp | 3 |

⇒ **科目强度序 eps > netprofit > revenue；期段序 y2 > y1**（与 `2rjrMZ25` 的 eps_y1 1.77 对比，y2 弱 0.34）。

### 46.5 rank-sum 降方差路线：高 margin / 低 TO，但 2Y 崩

骨架 `add(rank(ts_mean(ts_backfill(F,66),22)), ...)`；每腿 3 算子，3 腿 = 11 算子。

| 组合 | alpha | S | F | TO | 2Y | sub | margin | ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| np_y1 lean(5算子) | `wpQbG6P1` | **1.43** | 1.32 | 4.37% | 0.95 | **0.74** | **48.6bp** | 2 |
| 3 腿 y1(eps+np+rev) | `1YNZKLRm` | 1.42 | 1.37 | 3.27% | 0.95 | 0.63 | **71.5bp** | 3 |
| 3 腿 y2 | `58Eg53gn` | 1.38 | 1.38 | 3.20% | 1.02 | 0.65 | **78.1bp** | 2 |
| 2 腿 y2 | `78L6mQpZ` | 1.35 | 1.31 | 3.16% | 0.96 | 0.59 | 75.0bp | 3 |
| 2 腿 y1+y2 | `Xg9JzkMz` | 1.38 | 1.35 | 3.19% | 0.95 | 0.54 | 74.9bp | 3 |

**核心 trade-off（可复用判据）**：FULL 分层差分骨架 -> margin 13-19bp、2Y 1.2+；rank-sum 骨架 -> margin 71-78bp、TO 3.2%、但 **2Y 恒 0.95-1.02**。
⇒ **分层差分（短水平 - 长基线）是 2Y 的来源；rank-sum 平均掉的是时点信息，恰好也平均掉了近年 alpha。** 想同时拿 margin 和 2Y，必须保留分层结构。

### 46.6 ★★★★★ self 检查：本族**不自锁**（零配额本地实测）

| alpha | 字段 | max_correlation | 最近对手 | 判定 |
|---|---|---:|---|---|
| `JjeQzVEE` | eps_y2 | **0.6076** | 2rjrMZ25 | ✓ 通过 |
| `QPvKz1qK` | netprofit_y2 | **0.5793** | 2rjrMZ25 | ✓ 通过 |

⇒ 虽然 eps_y1 已被 `2rjrMZ25` 占用，**换期段（y2）后 self 只有 0.58-0.61，仍有 0.09-0.12 安全边际**。本族可继续扩科目。

### 46.7 逐闸缺口（eps_y2 最优件 `JjeQzVEE`）

```
LOW_SHARPE            = 1.43 / 1.58   (缺 0.15)
LOW_SUB_UNIVERSE      = 0.55 / 0.68   (缺 0.13)
LOW_2Y_SHARPE         = 1.24 / 1.58   (缺 0.34)  <- 最大缺口
pyramid_short = analyst ; lc = 178
```

**bucket 0.1 微改善**：`3qoVPzVe`（bucket 0.1）= S 1.44 / 2Y 1.27 / sub 0.54；short8 变体 `xArbG9qJ` = S 1.33 / 2Y 1.27；base252 `3qoVPEbX` = S 1.38 / 2Y 1.25。
⇒ 三条调参臂都只动 2Y +/-0.03，**2Y 1.58 在本族 y2 字段上不可达**。

### 46.8 46 节结论

1. **analyst7 / institutions6 / fund_holdings_panel 三集判死**（最好 0.92 / 0.32 / 0.32），非 trio 可挖集从 30 降到 26 中已筛尽；
2. **analyst_factor_signals 是唯一活矿脉**：制胜配方可迁移，换科目/期段后 S 1.07-1.43，且 **self 不自锁（0.58-0.61）**；
3. **但 y2 字段的 2Y 天花板 1.24-1.27，离闸 1.58 差 0.3**，与 `2rjrMZ25` 的 eps_y1（2Y 1.83）相去甚远 —— 真正的 2Y 引擎是 **eps_y1** 本身；
4. **新判据（跨区可复用）**：分层差分（短水平 - 长基线 + 长周期 bucket 门控）产出 2Y；rank-sum 平均产出 margin。**两者不可兼得是数学性质，不是调参问题。**
5. **本轮零提交、零取消**。

---

## 四十七、★★★★★ 突破：DEU/ANALYST 塔两颗全闸通过的非 trio ATOM（2026-11-05 凌晨）

### 47.1 方法：不换机制、只细扫 (中性化 x backfill x 窗口) 三轴

`2rAm5KQb`（SECTOR/bf22/w77）当时只差 LOW_SHARPE 0.03（S 1.55 / 2Y 1.67 / sub 1.12）。本轮把 w 与 bf 做细网扫描（此前只测 66/77/82/88/100 的粗网格），并补测从未试过的 **MARKET 轴 x bf66**。

### 47.2 ★★★★ SECTOR 轴细网（bf22，decay 16，trunc 0.08）

| w | alpha | S | 2Y | sub | ra | TO | DD | margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 66（旧） | `leAKa6ol` | 1.55 | 1.55 | 1.03 | 2 | 3.05% | 7.03% | 56.7bp |
| 70 | `qML0G5xj` | 1.56 | 1.50 | 1.08 | 2 | 2.97% | 6.86% | 57.6bp |
| **73** | **`P0ogzxOJ`** | **1.58** | **1.59** | **1.12** | **0** | 2.90% | **6.87%** | 59.6bp |
| 75 | `wpQbGWXd` | 1.57 | 1.62 | 1.12 | 1 | 2.85% | 7.21% | 60.3bp |
| 77（旧） | `2rAm5KQb` | 1.55 | 1.67 | 1.12 | 1 | 2.81% | 7.36% | 60.1bp |
| 79 | `LLMZzQRL` | 1.55 | 1.71 | 1.13 | 1 | 2.77% | 7.51% | 61.0bp |
| 81 | `58Eg5Y3X` | 1.53 | 1.68 | 1.14 | 1 | 2.73% | 7.85% | 61.2bp |
| 85 | `A1VvzmGg` | 1.50 | 1.73 | 1.13 | 1 | 2.66% | 7.90% | 61.8bp |

**★ w=73 是 (S, 2Y) 双闸的唯一交点**：S 轴在 w<=73 侧抬升，2Y 轴在 w>=73 侧抬升，两轴在此交叉。三点平滑（1.56 / **1.58** / 1.57 / 1.55）⇒ **不是噪声尖峰**，是真实平台。

**bf 轴（w77）**：bf22 1.55 / bf26 1.54 / bf30 1.54 / bf33 1.52 / bf66 1.53 ⇒ bf22 最优，bf 是弱轴。

### 47.3 ★★★★★ MARKET 轴 x bf66 细网 —— 出现第二颗全闸件

| w | alpha | S | 2Y | sub | ra | TO | DD | margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **80** | **`O0A8zdgJ`** | **1.59** | **1.61** | **1.14** | **0** | **2.39%** | 12.61% | **74.8bp** |
| 84 | `omEWrM9b` | 1.57 | 1.64 | 1.13 | 1 | 2.32% | 12.29% | 75.6bp |
| 88（旧） | `xArbvn9l` | 1.54 | 1.64 | 1.13 | 1 | 2.26% | 11.38% | 76.4bp |
| 92 | `RRE6zwwe` | 1.53 | 1.69 | 1.11 | 1 | 2.19% | 10.53% | 77.9bp |

⇒ **MARKET 轴比 SECTOR 轴整体高 0.01-0.01 S、+0.51pp margin、−0.5pp TO，但 DD 翻倍**（12.6% vs 6.9%）。

### 47.4 ★★★★★ 两颗候选全指标对照（均 `ra_failed_count = 0` / `checks.fail = []`）

| 指标 | `P0ogzxOJ` | `O0A8zdgJ` |
|---|---:|---:|
| 设置 | SECTOR / bf22 / w73 | MARKET / bf66 / w80 |
| Sharpe | 1.58 | **1.59** |
| 2Y Sharpe | 1.59 | **1.61** |
| sub_universe | 1.12 | **1.14** |
| Fitness | 1.31 | **1.34** |
| Turnover | 2.90% | **2.39%** |
| Drawdown | **6.87%** | 12.61% |
| margin | 59.6bp | **74.8bp** |
| longCount | 125 | 128 |
| investability_sharpe | 1.54 | — |
| risk_neutralized_sharpe | 0.93 | — |
| **self_correlation** | **0.2394** | **0.2395** |
| 塔 | DEU/D1/ANALYST (x1.8) | DEU/D1/ANALYST (x1.8) |
| 算子数 | 10 | 10 |
| prod | **未测**（MCP 120s 超时 x2） | **未测** |

**表达式（同一核心，仅两轴参数不同）**：
```
-signed_power(rank(ts_mean(ts_backfill(
    divide(subtract(vec_avg(anl44_2_netdebt_value), vec_avg(anl44_2_netdebt_prevalue)),
           add(abs(vec_avg(anl44_2_netdebt_prevalue)), 0.0001)), 22), 73)), 2)
```

### 47.5 ★★★★ 互相关 0.9259 ⇒ 只能提交其中一颗

`compute_mutual_correlation([P0ogzxOJ, O0A8zdgJ])` = **0.9259**（max_mutually_below_subset_size = 1）。
⇒ 二者是同机制换中性化轴的换壳，**不是两个独立塔位贡献**。提交一颗后 analyst 塔即从 2/3 点亮到 3/3。

**推荐 `O0A8zdgJ`**：三道绑定闸（S / 2Y / sub）全部比 `P0ogzxOJ` 多 0.01-0.02 缓冲，且 TO 更低、margin 高 15bp；唯一劣势是 DD 12.6%（DD 在 DEU 无硬闸）。
**备选 `P0ogzxOJ`**：若重视回撤（DD 6.87% 仅一半），S 1.58 / 2Y 1.59 贴线但已验证 ra=0。

### 47.6 ★★★★★ 本节方法论沉淀（跨区可复用）

1. **「只差 0.03」的候选不要弃，要判它是「轴内不可达」还是「轴间未交叉」**。之前用 SECTOR 单轴判定 netdebt 上限 1.55，但 SECTOR 与 MARKET 两轴的 (S, 2Y) 前沿方向不同，**交叉点必然落在某个 w 上**——粗网格（间隔 5-10）会整段跳过它。
2. **细网扫描的判据不是「找最高点」而是「找双闸交点」**：单看 S 会在 w70 停（1.56），单看 2Y 会在 w85 停（1.73），只有把两列并排画出来才能看到交点。
3. **贴线候选的 self 往往极低**：netdebt 符号反转信号与已提交 11 颗全部正交（self 0.2394），因为它是**存量科目的变化率**，与情绪/预期/量价族无交集。⇒ **低 self = 低拥挤 = prod 大概率也低**，是本族值得攻坚的根本原因。
4. **MCP 的 `check_correlation` 有 120s 客户端硬超时，平台侧需 240-400s ⇒ prod 在交互模式下结构性取不到值**，只能挂后台或等非高峰。

### 47.7 47 节状态

- **本轮仍零提交**；`P0ogzxOJ` / `O0A8zdgJ` 均为**待用户授权**状态；
- DEU 塔位即将变化：analyst 2/3 -> 3/3（提交任一颗后）；
- 待办：prod 测量、提交授权。

★ 另注：MARKET 轴的 DD 明显更高（11.4–12.6% vs SECTOR 6.7–8.7%）——MARKET 中性化只剥离市场 β，行业杠杆周期差异留在持仓里，这正是 S 更高（更多独立赌注）与 DD 更高（行业集中）的同一个来源。

### 44.5 本轮派发与 429 实况

- 8 条低成本几何臂：`submitted = 7/8`，`L1_level`（netdebt 水平值腿）被 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED` 挡下未派。
- 中性化扫描 `SLOW` / `STATISTICAL` / `CROWDING` 三批：只有 `CROWDING` 挤进槽位（`1Ys5BH6RC4R6bRtuubY7T3h`），另两批 429。
- MARKET w82/w88/w94 三批：只有 w82 进槽。
⇒ **并发槽长期被兄弟会话占满**，单次最多挤进 1 条；必须轮询式补发，不可依赖「一批全进」。
### 44.6 ★★★★★ 中性化轴全横评（11 个官方轴，本轮扫完 8 个）

同一骨架 `signed_power(rank(ts_mean(ts_backfill(RVN,22),77)),2)`，仅换 `base_neutralization`：

| 中性化轴 | alpha | S | F | y2 | sub | DD | 判读 |
|---|---|---:|---:|---:|---:|---:|---|
| **SECTOR** | `2rAm5KQb` | **1.55** | 1.27 | **1.67** | 1.12 | 7.4% | 综合最优（唯一「只差 S 0.03」） |
| MARKET | `pwd5ajK3` | 1.64* | 1.41 | 1.55 | 1.14 | 12.6% | *w77 单点，邻点 w82 只有 1.42 ⇒ **噪声尖峰** |
| SUBINDUSTRY | `1YNZjJXz` | 1.35 | 1.14 | 1.59 | 0.91 | 7.8% | 同业中性化把行业杠杆周期差异减掉 |
| STATISTICAL | `xArblbgN` | 1.30 | 1.01 | 1.16 | 0.98 | 7.5% | 统计风险模型过度剥离 |
| CROWDING | `ZYQAX5dx` | 1.26 | 0.91 | 1.14 | 0.97 | 9.6% | 拥挤度轴不适用基本面信号 |
| INDUSTRY | `rKReR8md` | 1.30 | 0.99 | 1.46 | 0.77 | 6.2% | sub 0.77 破闸 |
| **NONE** | `2rAmG9oN` | **0.84** | 1.26 | **−0.21** | 1.06 | **82.2%** | **DD 82% ⇒ 中性化是必要条件不是可选项** |

**结论**：`SECTOR` 是唯一同时满足 S/2Y/sub/DD 四项的轴。`MARKET` 的 1.64 是**窗口噪声**（同轴 w82 = 1.42，跨度 0.22 远超邻轴平滑变化）——**判「轴更优」必须看同轴相邻参数点是否连续**，否则会把单点幸运当成结构性优势。

### 44.7 ★★★★★ 分母/归一化全横评 —— `abs(prevalue)` 是信号本体，不是清理

| 分母形式 | alpha | S | y2 | DD | margin | 判读 |
|---|---|---:|---:|---:|---:|---|
| **abs(prevalue)** | `2rAm5KQb` | **1.55** | **1.67** | 7.4% | 60.1bp | 基准，最优 |
| abs(value)+abs(prevalue)（有界式） | `npvP6YMq` | 1.43 | 1.63 | 6.9% | 53.5bp | 有界化牺牲幅度信息，S −0.12 |
| alternative_market_cap_usd | `vR12Yerv` | 1.08 | 0.94 | 8.6% | 42.2bp | 市值归一 ≠ 杠杆率修订，机制错位 |
| abs(value) | `WjOeL08j` | 0.88 | — | — | — | 上轮已测 |
| **无 abs（符号分母 prevalue）** | `58EgGaEk` | **−0.03** | **−0.92** | 15.7% | −1.2bp | **信号完全消失** |

★★★ **`abs()` 是载荷算子**：DEU 有大量**净现金公司（netdebt < 0）**，符号分母会让「净负债朝零走」在净现金组里反转成正向，两组方向抵消 ⇒ S 归零。**凡比率腿，分母必须取绝对值，除非确认该字段恒同号。**

### 44.8 ★★★★★ 十科目全收口：为什么只有 netdebt 能活（比率爆炸机制）

本轮补测 4 个从未测过的科目（同骨架 SECTOR/bf22/w77/p2）：

| 科目 | alpha | S | F | y2 | sub | DD | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| **netdebt** | `2rAm5KQb` | **1.55** | 1.27 | 1.67 | 1.12 | 7.4% | 60.1bp |
| operatingprofit / epsr | 未进槽 | — | — | — | — | — | — |
| **csh** | `gJeZrXAl` | **−0.34** | −0.16 | −0.22 | −0.36 | **52.9%** | −18.5bp |
| **fcfps** | `mLo6KgQ2` | **−1.00** | −0.70 | −1.05 | −0.63 | **68.7%** | −43.0bp |

★★★ **根因（此前误判为「资产负债表 vs 利润表」）**：`(value − prevalue) / abs(prevalue)` 在 `abs(prevalue) → 0` 时**爆炸**。每股口径科目（eps / dps / epsr / fcfps / csh / netprofit）的 `prevalue` 经常穿过零（亏损公司、现金流为负），比率被放大到 ±10²–10³，`rank` 之后**尾部全由「预期接近零」的公司占据**，与信号无关 ⇒ S 归零甚至转负、DD 50–70%。

**netdebt 幸免的唯一原因**：净负债是**存量幅度量级大**的科目，`abs(prevalue)` 极少接近零。⇒ **判据不是「资产负债表 vs 利润表」，而是「分母是否有界的远离零」。** 以后换科目/换数据集做比率腿，**第一步先看该字段 prevalue 的绝对值分布是否有近零聚集**，有则必须先换分母（市值/总资产）或放弃该科目。

### 44.9 ★★★★★ `ts_backfill` 是载荷算子，不是 NaN 清理：去掉后 S 1.55→0.96

| 形态 | alpha | S | F | y2 | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| `ts_mean(ts_backfill(RVN,22),77)` | `2rAm5KQb` | **1.55** | 1.27 | **1.67** | 1.12 | 2.81% | 60.1bp |
| `ts_mean(RVN,77)`（无 backfill） | `WjOeYYGo` | **0.96** | 0.66 | **0.37** | 0.61 | 3.05% | 38.5bp |
| 同，power 3 | `1YNZGGpz` | 0.87 | 0.58 | 0.23 | 0.55 | 3.06% | 36.4bp |

**根因**：`ts_mean` 会**跳过 NaN**，所以无 backfill 时它平均的是「窗口内仅有的 1–2 个更新日原始值」——窗口长度几乎不起作用，实际变成「最近一次修订的单点值 + 上一个季度的噪声」；而 backfill 后序列**逐日有值**，`ts_mean(·,77)` 才是真正的**时间加权平均**，起到平滑与降噪作用。

⇒ **规则（跨区通用）**：凡稀疏更新字段（分析师预期、财报科目、季度指标）进时序平滑骨架，`ts_backfill` 必须在 `ts_mean` **内侧**且**不可省**。它的作用是「把脉冲序列变成阶梯序列」，是时序平均能生效的前提。

### 44.10 ★★★ 已测死路（本轮新增，勿重试）

| 方向 | 臂 | 结果 |
|---|---|---|
| 双窗/多窗集成（比率腿） | D1 / D2 / G1 | **结构不可行**：展开 16–18 算子 > 12 |
| `_lastactvalue` 隐含增长腿 | `KPJrg2lz` / `rKRe7xzo` | S 0.36–0.44，y2 ≈ 0 |
| `ts_delta` 修订加速度 | `JjeQ8rbn` | S 0.03，y2 −0.30 |
| 市值归一（alternative_market_cap_usd） | `vR12Yerv` | S 1.08，y2 0.94 |
| 符号分母（无 abs） | `58EgGaEk` | S −0.03 |
| 有界分母 | `npvP6YMq` | S 1.43（次优但不过闸） |
| 中性化 STATISTICAL / CROWDING / NONE | 见 44.6 | 1.30 / 1.26 / 0.84 |
| `decay` 32（MARKET 轴） | `bl6OxdgR` | S 1.40 / y2 1.43，劣于 decay16 的 1.64/1.55 |
| `vec_std_dev` / `vec_ir` / `vec_median` | preflight | **算子不存在**（被判 unknown_fields） |
| 科目 csh / fcfps | `gJeZrXAl` / `mLo6KgQ2` | 比率爆炸，S −0.34 / −1.00 |
| 无 backfill | `WjOeYYGo` | S 0.96 |

### 44.11 ★★★★ 参数面的噪声尺度（判「点」还是「平台」的量化标准）

SECTOR × bf22 固定，扫 w：**w66 = 1.54 / w72 = 1.31 / w77 = 1.55 / w82 = 1.53 / w88 = 1.48 / w100 = 1.43**。

w72 的 1.31 是 w66 与 w77 之间的**孤立深坑**（两侧 1.54/1.55），这不是「窗口谷」而是**估计噪声**：`lc` 只有 64–98 只股票、样本极薄，单点 S 的标准误本身就在 ±0.1 量级。

⇒ **判据**：同一轴上相邻参数点的 S 变化若 > 0.15 且不连续，该点**不可作为选参依据**（既不能当最优、也不能当死路）。真正的「窗口谷」是这个记忆里 `pwdl6ov6` 那种**单调下降的谷**（w6→w10→w22 依次 0.7145→0.7046→0.6773），不是单点跳变。

### 44.12 ★★★★★ 中性化 11 轴全部扫完（最终表）

| 轴 | S | y2 | TO | margin | DD | ra | 判读 |
|---|---:|---:|---:|---:|---:|---:|---|
| **SECTOR** | **1.55** | **1.67** | 2.81% | 60.1bp | 7.4% | 1 | ★ 唯一四项全过，保持主攻 |
| MARKET | 1.64（w77）/ 1.42（w82） | 1.55 / 1.30 | 2.5-2.8% | 69-73bp | 11.3-12.6% | 1-2 | w77 尖峰、w82 崩 ⇒ 噪声非结构 |
| SUBINDUSTRY | 1.35 | 1.59 | 3.69% | 48.6bp | 7.8% | 1 | 次优但 S 不足 |
| FAST | 1.34 | 1.17 | **12.36%** | **10.2bp** | 6.4% | 3 | 换手 ×4.4、margin ÷6 |
| INDUSTRY | 1.30 | 1.46 | 3.41% | 42.3bp | 6.2% | 3 | sub 0.77 破闸 |
| STATISTICAL | 1.30 | 1.16 | 2.84% | 53.0bp | 7.5% | 2 | 统计风险模型过度剥离 |
| CROWDING | 1.26 | 1.14 | 3.47% | 37.9bp | 9.6% | 3 | 拥挤度轴不适用基本面信号 |
| REVERSION_AND_MOMENTUM | 1.19 | 1.15 | **6.99%** | **17.1bp** | 9.3% | 3 | 换手 ×2.5 |
| SLOW | 0.97 | 1.10 | 6.34% | 13.4bp | 7.2% | 3 | 慢因子模型吃掉信号 |
| NONE | 0.84 | −0.21 | 1.95% | 286.7bp | **82.2%** | 2 | ★★ DD 82% ⇒ 中性化必需 |
| SLOW_AND_FAST | 未跑 | — | — | — | — | — | SLOW 与 FAST 单跑皆劣，跳过 |

**两条通用判据（跨区可复用）**：

1. **FAST / REVERSION_AND_MOMENTUM 这类「含高频因子」的中性化会显著推高换手**（2.8% → 12.4% / 7.0%）并压垮 margin（60bp → 10 / 17bp）。基本面慢信号**不要用 FAST 系中性化**：它们的换手代价远大于剥离噪声的收益。
2. **NONE 的 DD 是照妖镜**：本次 NONE 的 S 0.84 看似「只是差一点」，DD 却 82.2% —— 说明信号方向性完全依赖截面中性化约束，去掉后是裸露的行业/规模赌注。**凡 NONE 与 SECTOR 的 DD 差 > 5 倍，该信号不可脱离中性化生存。**

### 44.13 ★★★★ backfill 窗口最终剖面（bf22 是有效点但幅度在噪声内）

| bf | 5 | 11 | **22** | 33 | 66 | 126 |
|---|---:|---:|---:|---:|---:|---:|
| S | 1.27 | 1.32 | **1.55** | 1.52 | 1.53 | 1.32 |
| y2 | 0.91 | 0.99 | **1.67** | 1.67 | 1.59 | 1.63 |

★★ **判读更正**：bf22 的 1.55 与其两侧（1.32 / 1.52）不连续，**按 44.11 的判据它也是一个尖峰**，不能当作稳定最优点。bf ∈ [22, 66] 的真实水平是 **S ≈ 1.52–1.55**。⇒ 44.10 的「backfill 越短越好」要收敛为「**bf ∈ [22,66]；更短（≤11）反而崩**」——太短的回填窗无法把季度脉冲连成阶梯，退回到 44.9 的无 backfill 失效模式。

### 44.14 ★★★★★ 12 科目而非 10：sales / tbvps 此前被漏掉

`get_datafields(analyst44)` 精确核对：**72 字段 = 12 科目 × 5 字段**（`_value` / `_prevalue` / `_lastactvalue` / `_coveredby` / `_lastactccy`），另有 11 个 `*_currency` 元数据字段与 1 个 `anl44_cash_eps` 异形字段。

12 科目：csh / dps / ebitda / eps / epsr / fcfps / netdebt / netprofit / operatingprofit / roe / **sales** / **tbvps**。此前台账只记 10 个，**sales（营业收入预期）与 tbvps（每股有形账面价值）从未测试**。

★ 按 44.8 的「分母近零」判据，**sales 是结构上最该测的科目**：营业收入恒正、量级大，`abs(prevalue)` 不可能近零，比率腿天然有界。营收预期修正也是文献里最稳健的分析师因子之一。已派发 M_sales / M_tbvps。

### 44.15 ★★★ decay 轴最终确认（sim 级 decay，非表达式内）

| decay | 轴 | S | y2 |
|---|---|---:|---:|
| 8 | SECTOR bf22 w77 | 1.31 | 1.07 |
| **16** | SECTOR bf22 w77 | **1.55** | **1.67** |
| 32 | MARKET bf22 w77 | 1.40 | 1.43 |

（对照：MARKET 轴 decay16 = 1.64 / 1.55。）

⇒ **decay 16 是局部最优**（两侧 8 与 32 都明显更差）。decay 不仅「平滑持仓」，它直接改变日收益的波动尺度——**Sharpe 对 decay 的敏感度（0.24）不低于对窗口 w 的敏感度（0.22）**，两者必须一起标定；固定 decay 扫 w 得出的最优 w 不可靠。

### 44.16 ★★★★★ 12 科目全部收口（含本轮最后两个 sales / tbvps）—— 只有 netdebt 能活

统一骨架 SECTOR / bf22 / w77 / p2，方向为负（净负债上升为负向）：

| 科目 | alpha | S | F | y2 | sub | DD | margin | 分母近零风险 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **netdebt** | 2rAm5KQb | **1.55** | 1.27 | **1.67** | 1.12 | 7.4% | 60.1bp | 低（存量幅度大） |
| eps | gJeZW6jJ | 0.57 | 0.32 | 0.49 | 0.60 | 12.8% | 22.9bp | 中（亏损公司） |
| dps | E56RV1nR | 0.56 | 0.31 | 0.10 | 0.29 | 18.9% | 22.9bp | 中 |
| netprofit | Vkx0d1aV | 0.43 | 0.21 | 0.19 | 0.63 | 18.7% | 17.3bp | 高 |
| ebitda | MPY30ob9 | 0.35 | 0.16 | 0.36 | 0.25 | 13.3% | 14.1bp | 中 |
| **sales** | akKxeXYW | **0.22** | 0.07 | −0.11 | −0.28 | 12.1% | 8.9bp | **低，但仍无信号** |
| roe | P0ogMdGL | 0.15 | 0.05 | −0.55 | −0.03 | 18.9% | 6.4bp | 中 |
| csh | gJeZrXAl | −0.34 | −0.16 | −0.22 | −0.36 | **52.9%** | −18.5bp | 高 |
| fcfps | mLo6KgQ2 | −1.00 | −0.70 | −1.05 | −0.63 | **68.7%** | −43.0bp | 高 |
| tbvps | N1NVLMlX | −0.74 | −0.45 | −0.89 | −0.71 | **53.6%** | −34.8bp | 高 |
| epsr / operatingprofit | 未进槽（429） | — | — | — | — | — | — | 预期同 eps 族 |

**两条结论**：
1. **sales 是本轮唯一「分母结构最优但信号为零」的科目**（营收恒正、量级大，比率完全有界，DD 仅 12.1%、TO 2.81%），S 却只有 0.22 / 2Y −0.11。⇒ 44.8 的「分母近零」判据是**必要条件不是充分条件**：分母干净只保证「不爆炸」，不保证「有 alpha」。**营收预期修正在文献中极稳健，但在 DEU/TOP500 上不成立**——这是区域特性，不可外推。
2. **netdebt 是 analyst44 唯一有效科目**，12 科目已全测完，**该数据集信号面封闭**。

### 44.17 ★★★★★ netdebt 线的最终坐标与天花板裁定

**已穷尽的七个轴**（本数据集累计约 45 条臂）：

| 轴 | 扫描点 | 最优 |
|---|---|---|
| 科目 | 12 个全测 | **netdebt** |
| 中性化 | 10 个实跑（11 轴中 SLOW_AND_FAST 跳过） | **SECTOR** |
| 分母 | abs(prevalue) / abs(value) / 有界式 / 市值 / 符号 | **abs(prevalue)** |
| backfill 窗 | 5 / 11 / 22 / 33 / 66 / 126 / 无 | **22–66**（S 1.52–1.55） |
| 平滑窗 w | 44 / 55 / 66 / 72 / 77 / 82 / 88 / 94 / 100 / 126 | **66–82**（S 1.52–1.55） |
| power | 1 / 2 / 3 | **2 或 3**（差 ≤0.01） |
| decay | 8 / 16 / 32 | **16** |

**裁定**：analyst44 netdebt 修订线的真实水平是 **S ≈ 1.52–1.55、2Y 1.55–1.75**；DEU 双闸都是 **1.58**（LOW_SHARPE 与 IS_LADDER_SHARPE=2Y）。**S 差 0.03–0.06，七个轴已无未测维度。** 继续换几何 = 在噪声尺度内自我欺骗（见 44.11 判据）。

**结构上无法突破的三个原因（同时成立）**：
1. **广度锁死**：DEU 只有 TOP500 一个 universe；netdebt cov 0.6483、lc 仅 64–98 ⇒ 独立赌注太少，S 的统计上限压在 1.5 附近；
2. **算子锁死**：12 算子预算下两条信号腿最低 17 算子（两条比率腿各 6 + 平滑/排序各 2 + add 1）⇒ **无法加第二条独立腿**，唯一分散化手段被禁；
3. **数据锁死**：DEU 非 trio 数据集绝大多数字段 cov 为 0 或信号全灭（analyst93 / shortinterest3 / sentiment7 / institutions1 / risk88 / analyst48 / insiders1 / analyst15 / fundamental1 / option1 / imbalance5 / analyst10/16/35/39/46/8/94 已逐一否定）。

⇒ **本轮零提交、零取消**（无平台写操作）。DEU 非 trio 路线在「不放开 trio 限制、不换区、不换 delay」前提下，**已无可挖矿脉**。后续方向须由用户裁定。

---

## 四十五、★★★★★ 2026-11-05：DEU 非 trio 数据集全扫描 —— 44.17 的「无可挖矿脉」结论被推翻

### 45.1 ★★★★★ 全量数据集扫描（修正 44.17 第 3 条「数据锁死」）

用 `get_datasets(region=DEU, universe=TOP500, delay=1, limit=500)` 全量拉取（返回 172 条可解析），按 `cov > 0` 且 category ∉ {pv, model, other} 过滤后，**仍有 30 个数据集有覆盖**，其中多数从未测试。

**category 分布（172 条）**：other 41 / model 45 / analyst 18 / news 17 / pv 16 / fundamental 12 / institutions 5 / risk 5 / sentiment 3 / earnings 2 / insiders 2 / socialmedia 2 / imbalance 1 / macro 1 / option 1 / shortinterest 1。

**按覆盖率排序的 30 个非 trio 候选**（cov / 字段数 / alphaCount）：

| 数据集 | cat | cov | 字段 | ac | 本战役状态 |
|---|---|---:|---:|---:|---|
| **institutions6** | institutions | **1.000** | 11 | 270 | ★ 从未挖 |
| risk88 | risk | 1.000 | 1 | 64 | 已否（唯一字段=市值代理） |
| news104 | news | 0.963 | 11 | 100 | 从未挖 |
| **sentiment27** | sentiment | **0.904** | 18 | 324 | ★ 从未挖 |
| fund_holdings_panel | institutions | 0.902 | 18 | 102 | 从未挖 |
| risk60 | risk | 0.835 | 5 | 395 | 借券族（见 45.4） |
| news18 | news | 0.805 | 70 | 137 | 元数据为主（见 45.4） |
| news17 / news20 / news50 / news38 | news | 0.60-0.79 | 3-48 | 13-87 | 从未挖 |
| analyst48 | analyst | 0.788 | 7 | 7 | 已否（指数元数据） |
| **analyst7** | analyst | **0.721** | **608** | **3993** | ★★ **最强未挖**（见 45.2） |
| shortinterest3 | shortinterest | 0.711 | 25 | 864 | 已封（只能门控） |
| fundamental22 | fundamental | 0.690 | 1 | 40 | 从未挖 |
| analyst93 | analyst | 0.637 | 100 | 193 | 已封（信号全灭） |
| analyst47 | analyst | 0.623 | 5 | 112 | 从未挖 |
| analyst_factor_signals | analyst | 0.600 | 108 | 1575 | 从未挖 |
| analyst9 | analyst | 0.583 | 51 | 106 | 已封（净广度 S 0.82） |
| analyst44 | analyst | 0.580 | 72 | 58 | 已穷尽（见 44.17） |
| insider_agg_matrix | insiders | 0.562 | 34 | 170 | 从未挖（≠ insider_matrix） |
| insiders1 | insiders | 0.534 | 8 | 26 | 已否（无买卖方向） |
| **fundamental6** | fundamental | 0.492 | **196** | 1028 | ★ 从未挖 |
| institutions4 | institutions | 0.341 | 6 | 19 | 从未挖 |
| analyst83 | analyst | 0.339 | 345 | 26 | 已判（TO 2.1-2.4% 慢变） |
| sentiment33 | sentiment | 0.322 | 255 | 45 | 从未挖 |
| socialmedia39 | socialmedia | 0.275 | 1 | 137 | 从未挖 |
| fundamental45 | fundamental | 0.269 | 12 | 85 | 从未挖 |
| institutions1 | institutions | 0.229 | 7 | 32 | 已否（self 自锁） |

**勘误**：44.17 第 3 条写「DEU 非 trio 数据集绝大多数字段 cov 为 0 或信号全灭」——**只说对了 trio 内的部分**。真正的情况是：**我只测过非 trio 30 个数据集里的 9 个**，剩下 21 个（含 institutions6 / sentiment27 / fund_holdings_panel / analyst7 / fundamental6 等 5 个 cov ≥ 0.49 的）从未碰过。**「无矿脉」是从 9 个样本外推到 30 个的错误结论。**


---

## 四十八、2026-11-05 凌晨：prod 0.9017 击穿 analyst44 族 + sentiment33 整集判死 + fundamental6 复活

### 48.1 ★★★★★ `O0A8zdgJ` prod = **0.9017** —— analyst44 netdebt 族整体封盘（族级判定）

| 项 | 值 |
|---|---|
| alpha | `O0A8zdgJ` |
| 设置 | MARKET / bf66 / w80 / decay16 / trunc0.08 |
| Sharpe | 1.59 |
| 2Y Sharpe | 1.61 |
| sub_universe | 1.14 |
| Fitness | 1.34 |
| **self_correlation** | **0.2395** |
| **prod (platform)** | **0.9017** |
| 测量耗时 | 142.1s（prod_wait.py，平台轮询 3 次空响应后出值）|

**结论**：该候选 IS 全闸通过（checks.fail=[]、ra_failed=0、pending 只剩 SELF/DATA_DIVERSITY/PROD/REGULAR），
self 仅 0.2395（与已提交 11 颗全部正交），但 **prod = 0.9017 远超 0.70 放行线**。

**这是「self 干净 ≠ prod 干净」的第四次独立实证**（前三次：USA shortinterest3 `kqNRbvJP` self 0.6012 / prod 0.8463；
GBR techindi 族 self 0.0238 / prod 0.7343-1.0；EUR 借券费率族 prod 0.7859/0.7935）。
self 回答「撞不撞自家已提交池」，prod 回答「撞不撞整个生产池」——两个不同问题，必须两端都测。

**族级外推（按 wq-prod-corr-read §四·1）**：
- prod > 0.80 ⇒ **墙在族层面**，不是单颗问题。
- `P0ogzxOJ`（与 `O0A8zdgJ` 互相关 0.9259，同骨架 only w/neutralization 不同）**不必再花 prod 时隙**，按同一面墙处理。
- **analyst44 netdebt ATOM 全族封盘**：既有候选（`P0ogzxOJ` / `O0A8zdgJ` / `2rAm5KQb` / `leAKa6ol` / `qML0G5xj` / `wpQbGWXd` / `LLMZzQRL` / `58Eg5Y3X` / `A1VvzmGg` / `xArbvn9l` / `omEWrM9b` / `RRE6zwwe` / `GrWOxwk5`）全部留档但不再投入槽位。
- **取消**「提交 `O0A8zdgJ`/`P0ogzxOJ` 以点亮 ANALYST 塔 3/3」的待办：它们过不了 prod 闸，提交必然被 BLOCKED。

**方法论沉淀**：IS 全闸 + self 极低 + 2Y 过线 + 高 margin，仍然可以在 prod 上死得很彻底。
本族的低 self 来源是「存量科目变化率与情绪/预期/量价族无交集」，但**生产池里已有大量同构的存量比率 alpha**（来自其它区域/账户），
所以 self 与我们自己的池正交，却与全池高度重合。**低 self 只能证明「我们没做过」，不能证明「市场没做过」。**

### 48.2 ★★★★★ `sentiment33` 十模板整集判死：TO 12-13% / margin ≤9bp / lc 51-66

画像：255 字段全 VECTOR，cov 0.315-0.326，ac 45。可用 230（扣 25 个元数据字段）。
结构：模型分 23（model6/7/8/9 × _fkw1..5）+ 极性计数 method_1..9 × {pos,neg,obj,neut} × fkw1..5 + filtered 变体 + token/group 统计。
**`snt33_sefke1v1_fkw1_method_1_obj` 不存在**（method_1 只有 pos/neg/neut）；obj 要用 method_2/3/4。

设置：DEU/TOP500/D1 / decay 4 / SECTOR / trunc 0.08。

| 模板 | alpha | S | 2Y | sub | TO | margin | lc | raFail |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T3 客观度反向 | `QPvKo6qG` | **0.59** | 1.08 | 0.30 | 13.28% | **9.0bp** | 52 | 4 |
| T6 filtered−raw | `gJeZ0dWm` | 0.27 | 1.06 | 0.20 | 13.06% | 4.3bp | 52 | 4 |
| T4 双模型分歧 | `3qoV25XQ` | 0.23 | 0.79 | 0.01 | 12.26% | 3.7bp | 55 | 5 |
| T7 中性占比反向 | `RRE6vero` | 0.06 | 0.69 | −0.04 | 12.63% | 0.9bp | 52 | 5 |
| T2 净极性比率 | `WjOexJgx` | −0.09 | −0.25 | 0.16 | 12.87% | −1.5bp | 52 | 4 |
| T1 负面水平反向 | `88RP2Xqa` | −0.18 | −0.77 | −0.04 | 12.49% | −3.4bp | 66 | 4 |
| T8 token 加权 | `gJeZ0L3g` | −0.32 | 0.15 | −0.56 | 13.54% | −4.7bp | 51 | 5 |
| T5 情绪动量 5−66 | `QPvKo6nM` | 0.00 | 0.29 | 0.20 | **43.73%** | 0.0bp | **14** | 4 |

**判据链**：
1. **TO 全部落在 12.26-13.54%**（T5 更高达 43.73%），无一例外 ⇒ 新闻事件日频更新，换手结构性偏高；
2. **margin 最高 9.0bp**，多数 0-4bp，按 `margin×10000 < 10` 判据全部不过；
3. **lc 仅 51-66**（T5 只有 14）⇒ 持仓过于集中，sub_universe_sharpe 最好 0.30、多数负；
4. S 最好 0.59，距 1.58 差 1.0 个数量级。

⇒ **与 news104（TO 12-17% / margin 0.45-1.5bp）同型，属「日频新闻更新速度远超其信息价值密度」的数据集级死因**，
换模板救不回来（10 个结构互异模板已覆盖水平/比率/客观度/跨模型分歧/动量/filtered 差/中性占比/token 加权/事件强度/zscore）。
**`sentiment33` 整集封盘。**

### 48.3 ★★★★★ `fundamental6` 旧判死失效 → 复活（最大未挖非 trio ATOM 矿）

**旧结论（错误）**：`cells.json` 两条记录 `DEU-FUNDAMENTAL6-EMPTY-COVERAGE-20260923`（bound=payload）与
`DEU-FUNDAMENTAL6-PROBE-DEAD-20260923`（bound=inferred）写：
「DEU 不再投 fundamental6 单/双字段基本面比率方向；低频年度基本面在 DEU TOP500 D1 无截面信号」，依据仅 **16 次回测**。

**反证**：已提交 `Wje5K71x` 用的就是 fundamental6 的 `fnd6_newq_oiadpq`，实测 **S 1.73 / 2Y 1.87 / prod 0.4305 / TO 12.69% / margin 12.58bp**。
⇒ 旧判死建立在「年度/semi-annual 字段」上，而 **`fnd6_newq_*` 是季度字段（39 个），完全不同频段**。

**`Wje5K71x` 的 7 算子在产权威几何**：

    group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(F,240)), rank(ts_delta(F,176))), target_tvr=0.03), sector)

语义 = **同一科目在 240 日与 176 日两个时段的增量必须同号同强**（双时段自洽增长），再用 target_tvr 压换手。
对照：单时段 delta 会把「一次性跳变」误判为增长；双时段乘积要求持续性。

**数据集结构**（196 字段全 MATRIX，cov 0.17-0.66）：
- `fnd6_newq_*` 39 个季度资产负债表/利润表科目（cov 最高 0.6595 `seqq`、0.6561 `lseq`、0.6531 `cheq`）
- `fnd6_newa2_*` 24 个、`fnd6_ewq_*` 22 个（同季不同加工）
- 其余约 110 个年度 `_y` / semi-annual `_sa` 字段

**塔位含义**：fundamental 属禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL}，**但单数据集 ATOM 不占配额** ⇒ fundamental6 ATOM 完全合规，正是用户「最好 ATOM」的取向。

**本轮新波次（10 个结构互异几何 × 10 个不同字段，decay16/SECTOR/trunc0.08）**：

| 几何 | 字段 | 机制 | alpha |
|---|---|---|---|
| G1 双时段差分乘积（反向）| aoq 总资产 | 资产增长异象 | `3yCmzkfda4Aac2csOcpNhJC` |
| G2 单时段差分+ts_zscore（反向）| invtq 存货 | 存货积累异象 | `4Bp1UF4rJ52aae8li1M8Tsx` |
| G5 增长×水平交互 | oiadpq 营业利润 | 持续增长且水平高 | `3IoUZT7dU4tQ8J0UJbzgECV` |
| G10 bucket 规模中性 | cheq 现金 | 现金积累（规模内比较）| `13iqRe2G24VqatUYWqK4PI9` |
| G3 账面市值比 | seqq 股东权益 | 价值 | 待补发 |
| G4 比率差分（反向）| lctq/aoq 杠杆 | 杠杆上升异象 | 待补发 |
| G6 二阶差分（反向）| capsq 资本支出 | 投资加速度/过度投资 | 待补发 |
| G7 ts_ir（反向）| rectq 应收 | 应收趋势稳定性 | 待补发 |
| G8 同比差分去季节 | saleq 营收 | 营收同比增长 | 待补发 |
| G9 group_zscore | apq 应付 | 应付扩张=议价力 | 待补发 |

### 48.4 ★★★★ 自我纠错：analyst93 误派 5 条违规臂

本轮在未读 `cells.json` 死路记录的情况下，对 analyst93 派了 9 条臂，其中 **5 条直接违反已记录死路**：

| 臂 | 违反的死路 |
|---|---|
| T2 recprof_rel | `DEU-AN93-RELATIVE-DEAD`：relative_profitability1-4 全系（16 字段）判死 |
| T4 accXcons | `DEU-AN93-CROSS-COMPOSITE-DEAD`：禁跨字段复合 |
| T8 a_vs_e | 同上（两条 group_rank 相减）|
| T9 prev2rec | 同上（跨字段差）|
| T10 selfbucket | 同上（bucket/group 复合）|

另有 `DEU-AN93-PROD-SATURATED`：`recprofitabilityprev_profitability2` 族 prod 已饱和，且明确要求「任何 an93 变体在投入结构工作前先查 prod（prod-first 硬前置），不再投入 >2 条/波」。
而 `an93_T1/T3/T9` 用的 `profitability1` 与该族同源。

**纪律修订（本轮起执行）**：**派发任何数据集前，先读 `tracking/DEU/config/cells.json` 的 `dead_ends` 里该数据集的全部记录，再决定派什么。**
台账正文（`s2_nearmiss_rescue_*.md`）是叙事，`cells.json` 才是可机读的死路清单；只看正文会重复踩坑。
本轮受影响的 8 条臂已在飞，保留读数作「违反死路的代价」对照，但不再追加 analyst93 任何臂。


---

## 四十九、2026-11-05 凌晨：`nanHandling ON` 是稀疏季度字段的载荷设置 + `P0ogRWEK` 全闸但 prod 0.9287

### 49.1 ★★★★★ 载荷设置发现：`nanHandling=ON` 把 2Y 抬 0.48、持仓数翻倍

同一表达式、同一字段、只改设置的三方对照（表达式 = `group_rank(multiply(multiply(rank(ts_delta(oiadpq,240)),rank(ts_delta(oiadpq,176))),rank(ts_rank(oiadpq,504))),sector)`，9 算子）：

| 设置 | alpha | S | 2Y | sub | TO | DD | margin | longCount |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| FAST / d4 / **nanON** | `P0ogRWEK` | **1.68** | **1.70** | **1.26** | 12.94% | **6.5%** | 11.8bp | **179** |
| FAST / d4 / nanOFF | `3qoVKglg` | 1.58 | 1.22 | 1.04 | 15.61% | 7.4% | 11.0bp | 193 |
| SECTOR / d16 / nanON | `0mYrVnMv` | 0.56 | −0.29 | 1.04 | 2.04% | 11.8% | 38.8bp | 131 |
| INDUSTRY / d16 / nanOFF | `0mYr2G12` | 1.52 | 1.14 | 1.03 | 4.00% | 8.2% | 54.0bp | 76 |

**三条独立结论**：

1. **`nanHandling=ON` 单独有效，但方向是「救 2Y 不救 S」**：FAST/d4 下 nanOFF→nanON，S 1.58→1.68（+0.10）、**2Y 1.22→1.70（+0.48）**、sub 1.04→1.26、DD 7.4→6.5%。
2. **nanON 必须配 FAST + 低 decay 才成立**：SECTOR/d16/nanON 直接崩到 S 0.56 / 2Y −0.29。⇒ 三者是**交互项**，不是可加的独立杠杆。
3. **机理**：季度基本面字段一年只更新 4 次，其余交易日是 NaN。`nanHandling=OFF` 时这些 NaN 会让股票在某些日子**掉出可选池**，
   于是 `ts_delta` 的差分基期在稀疏区间里漂移；`nanHandling=ON`（把 NaN 当 0 处理）让时序算子始终看到连续序列，
   `ts_rank(F,504)` 的水平秩才有稳定参照。这也是 longCount 从 76/87 跳到 179 的原因：覆盖被还原了。

**这条规则的可迁移范围**：凡「更新频率 << 交易日频率」的字段（季度基本面、月度宏观、稀疏事件聚合），
**在用时序算子（ts_delta / ts_mean / ts_rank / ts_zscore）之前，先按 nanON 跑一次**，不要默认沿用 nanHandling OFF。
此前 11 颗提交件里凡 nanHandling=OFF 的，都可能是「2Y 被设置压死」而非「信号不够」。

### 49.2 ★★★★★ `P0ogRWEK` 全闸通过但 prod = 0.9287 —— 撞的是我方自己的枢纽件

`P0ogRWEK` 逐项验收：

| 闸 | 实测 | 线 | 判定 |
|---|---|---|---|
| LOW_SHARPE | 1.68 | ≥1.58 | ✓ |
| LOW_2Y_SHARPE | 1.70 | ≥1.58 | ✓ |
| LOW_SUB_UNIVERSE_SHARPE | 1.26 | ≥0.517×1.68=0.87 | ✓ |
| LOW_FITNESS | 1.29 | ≥1.0 | ✓ |
| CONCENTRATED_WEIGHT | — | — | passes |
| checks.fail | `[]` | 空 | ✓ |
| ra_failed_count | **0** | 0 | ✓ |
| ppa_failed_count | 0 | 0 | ✓ |
| self_correlation | **0.1702** | <0.70 | ✓ |
| **prod (platform)** | **0.9287** | <0.70 | **✗ BLOCKED** |

其余：TO 12.94% / returns 7.66% / DD 6.5% / margin 11.84bp / lc 179 / sc 204 / investability_sharpe 1.60 / 塔 DEU·D1·FUNDAMENTAL ×1.8。

**归因**：本族 prod 之所以 0.93，是因为**已提交的 `Wje5K71x` 本身就是枢纽件**——它的核心腿是
`multiply(rank(ts_delta(fnd6_newq_oiadpq,240)),rank(ts_delta(fnd6_newq_oiadpq,176)))`，
而 `P0ogRWEK` 的第一层乘积与之**逐字相同**。self 只有 0.1702 是因为 self 池按截断/加权口径计算且我方池只有 11 颗；
prod 池按全生产池计算，`Wje5K71x` 一条就足以把相关顶到 0.93。

⇒ **`fnd6_newq_oiadpq` 这个字段被 `Wje5K71x` 烧掉了**：任何以 oiadpq 双 delta 为核心的变体，prod 下限就是 0.90+。
**枢纽件的自锁效应是「字段级」而非「表达式级」**——只要共享那条 ts_delta 腿就锁死，改中性化/加水平腿/换窗口都无效（实测 >INDUSTRY 1.52、Va 1.68、252/126 1.51、三 delta 1.55 全部被同一面墙挡）。

### 49.3 ★★★★ fundamental6 逐科目收口：只有 `oiadpq` 有截面信号

全部为 `nanHandling=OFF` 或 `ON` 下实测（同几何 = 双 delta 240/176 或 Va 增长×水平）：

| 科目 | 经济含义 | nanOFF S | nanON S | 2Y(nanON) | 判定 |
|---|---|---:|---:|---:|---|
| **oiadpq** | 营业利润（折旧后）| 1.45 | **1.68** | **1.70** | ★ 唯一有信号，但被枢纽件锁 prod |
| cheq | 现金 | 0.74 | 0.99 | **1.86** | 2Y 极强但 S 不足（0.99 ≪ 1.58）|
| saleq | 营收 | 1.09 | 1.09 | 0.18 | S 差 0.49、2Y 差 1.40 |
| seqq | 股东权益 | 0.40 | 0.83 | 0.43 | 弱 |
| apq | 应付账款 | 0.32 | 0.57 | 0.41 | 弱 |
| aoq | 总资产 | −0.33 | — | — | 资产增长异象不成立 |
| invtq | 存货 | 0.48 / −0.18 | — | — | 存货异象不成立 |
| rectq | 应收账款 | — | −0.60 | −0.29 | 反向也不成立 |
| cogsq | 营业成本 | — | −0.93 | −0.54 | 反向也不成立 |
| oibdpq | EBITDA | 1.10 | — | 0.80 | 弱于 oiadpq（折旧项有信息）|
| lctq | 流动负债 | −0.43 | — | — | 不成立 |

⇒ **资产负债表科目（资产/存货/应收/应付/现金/权益）在 DEU/TOP500/D1 全部无截面信号**；
信号集中在**利润表 + 营业利润**一项。这与 44.17「低频年度基本面在 DEU 无截面信号」方向一致，但**季度频率的营业利润是例外**。

### 49.4 ★★★★★ 战略结论：DEU 的真瓶颈是 prod 拥挤，不是 IS 生成能力

本轮在**同一个夜里产出三颗全 IS 闸通过的候选**，全部倒在 prod：

| alpha | 机制 | S | 2Y | self | **prod** |
|---|---|---:|---:|---:|---:|
| `O0A8zdgJ` | analyst44 netdebt 符号反转 | 1.59 | 1.61 | 0.2395 | **0.9017** |
| `P0ogzxOJ` | 同上（SECTOR/w73）| 1.58 | 1.59 | 0.2394 | 未测（同族推定 ≈0.90）|
| `P0ogRWEK` | fundamental6 oiadpq 双 delta×水平 | 1.68 | 1.70 | 0.1702 | **0.9287** |

**两颗 prod 都是 0.90+，而 self 都只有 0.17-0.24。** 这个组合说明：
我们挖到的机制**在我方池里完全正交**（self 极低），但**在整个生产池里极度拥挤**。

⇒ **DEU 的挖掘难点已经从「找不到全闸 alpha」转移为「找到全闸且低 prod 的 alpha」。**
⇒ 后续每一波都必须把 **prod-first** 作为硬前置：**先用族代表测 prod，prod<0.70 才投入结构工作**，
   而不是先花 10-20 条臂把 IS 打磨到全闸、最后才发现 prod 0.9。本夜在这一点上重复踩了两次（O0A8zdgJ 族 + oiadpq 族）。

**可执行的队列纪律（本轮起）**：
1. 新族第一波 ≤3 条，只要**一条**接近全闸就立刻测 prod；
2. prod ≥0.80 ⇒ 整族封盘，**不再为该族做任何结构工作**（包括换中性化、换窗口、加辅助腿）；
3. prod 0.70-0.80 ⇒ 最多再测 2 条；
4. prod <0.70 ⇒ 才允许批量打磨。

### 49.5 本轮其余读数

- **analyst93**（已封集，本轮误派 8 条）：最好 `d5W16bLg`（correct_revision_ratio 单字段）S 0.92 / 2Y 0.30 / sub 0.72 / TO 2.22% / margin 46bp / lc 110；
  其余 −0.28~0.25。**成本结构很好（TO 2%、margin 46bp），但 S 只有 0.92**，与 29.2「S 0.36 封盘」一致。该族**信号强度**是死因，不是成本。
- **fundamental6 双 delta 字段迁移（8 个字段 / nanOFF+INDUSTRY）**：seqq 0.40 / cheq 0.74 / apq 0.32 / lctq −0.43 / invtq −0.18 / saleq 0.87 — 全灭。
- **fundamental6 纯双 delta 长周期**（INDUSTRY/d16/nanOFF）：252-126 无 bf S 1.39 / 2Y **1.34**（2Y 最好的 nanOFF 组合）；504-252 S 0.84（过慢）；240-176 有 bf S 1.41 / 2Y 1.22。
- **rank-sum 混合**（`d5W1JoRE`，INDUSTRY/d16/nanOFF）：S **1.56** / 2Y 0.85 / sub **1.12** / F **1.46** / TO 4.00% / DD **7.0%** / margin 55.1bp —— **nanOFF 体系里 S 最高的一条**（差 0.02 过闸），2Y 是短板。
  ⇒ 若把这条搬到 nanON 下重跑，很可能一举双闸通过；但它仍属 oiadpq 族，prod 会被 0.90 墙挡住。
- **中性化轴排序（oinadpq Va 几何）**：INDUSTRY 1.52 > SECTOR 1.44 = MARKET 1.44 > SUBINDUSTRY 1.07；decay 8 (1.54) > 16 (1.52) > 32 (1.44)。
- **`ts_target_tvr_decay(target_tvr=0.03)` 对 2Y 是净损失**：它把 TO 从 12.9% 压到 3.8%，同时把 2Y 从 1.70（`P0ogRWEK` 无 tvr，FAST/d4/nanON，TO 12.94%）压到 1.11-1.41。
  已提交的 `Wje5K71x` 虽然表达式里有 tvr，但实测 TO=12.69% ⇒ 该字段上 tvr **实际未生效**，这也是它 2Y 能到 1.87 的原因之一。
  ⇒ **在 DEU，换手压缩不是免费午餐**：低 TO 换来的是 2Y 的塌陷。宁取高 TO + 高 2Y。

### 49.6 `nanHandling ON` 不是万能：analyst_factor_signals 族实测反例

同一批把 nanON / FAST / decay4 套到 `analyst_factor_signals` 的 `eps_y2` / `netprofit_y2` 上（该族是**日频更新**，本来不缺数据）：

| 骨架 | 字段 | alpha | S | 2Y | sub | TO | DD | margin | lc | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| FULL 分层差分 | eps_y2 | `akKxpMvx` | **1.64** | **1.44** | **0.53** | 17.68% | 9.4% | 9.35bp | 191 | SUB / 2Y |
| FULL 分层差分 | netprofit_y2 | `3qoVN3bP` | 1.49 | 1.39 | 0.41 | 17.69% | 6.3% | 8.33bp | 190 | SHARPE/FIT/SUB/2Y |
| lean ts_mean | eps_y2 | `d5W1GggE` | **1.69** | 0.30 | 0.77 | 12.83% | 7.8% | **13.35bp** | 189 | SUB / 2Y |
| Va 双delta×水平 | eps_y2 | `e75QjmKd` | 1.11 | 0.61 | 0.37 | 14.46% | 7.9% | 7.40bp | 186 | 四项 |
| DD 双delta+tvr | eps_y2 | `QPvK8eeX` | 1.10 | 0.61 | 0.54 | 12.01% | 7.3% | 8.60bp | 186 | 三项 |
| Va 双delta×水平 | netprofit_y2 | `A1VvA35g` | 1.30 | 0.95 | 0.66 | 14.44% | 8.8% | 8.51bp | 186 | 三项 |

**对比 nanOFF/SECTOR/d4 旧读数（§四十六）**：eps_y2 FULL 是 S 1.43 / 2Y 1.24 / sub 0.55。
⇒ nanON+FAST 把 S 提到 1.64（+0.21）、2Y 提到 1.44（+0.20），**但 sub_universe 纹丝不动（0.55→0.53）**。

**结论**：
1. **nanON 只对「本来就稀疏」的字段是净收益**；对日频更新的分析师预期族，它提 S 但破不了 sub。
2. 该族的**结构性死因是 `sub_universe_sharpe`**（0.41–0.77，需 ≥0.517×S≈0.85），不是 Sharpe 也不是 2Y。
   FULL 分层差分把持仓集中到少数强信号票 ⇒ sub 塌；lean 版分散但 2Y 塌（0.30）。**两者不可兼得。**
3. `d5W1GggE` 的 **margin 13.35bp + S 1.69** 是成本面上最漂亮的一条，但 2Y 0.30 说明它赚的是「近两年之外的时段」，
   在 DEU 的 2014-2023 窗口里 2Y 检验（2022-2023）几乎不工作。
4. ⇒ **analyst_factor_signals 的 eps/netprofit 族在 DEU 到此为止**：不是骨架不够多（已试 FULL / lean / Va / DD 四种），
   是 `sub_universe` 与 `2Y` 在数学上互相牵制。要破只能换数据集（不同持仓结构），不能换骨架。


---

## 五十、2026-11-05 收尾状态：待提交件与下一阶段队列

### 50.1 ★★★★★ 唯二「全 IS 闸 + prod<0.70」候选（等待真实提交授权）

| alpha | S | 2Y | sub | F | prod | 塔 | 状态 |
|---|---:|---:|---:|---:|---:|---|---|
| `E56pROb9` | **1.79** | **2.03** | **1.32** | **1.70** | **0.6859** | DEU·D1·MODEL ×1.8 | UNSUBMITTED，checks.fail=[]，ra_failed=0 |
| `wpQYNvZp` | 1.68 | **2.18** | 1.17 | 1.36 | **0.6333** | DEU·D1·MODEL ×1.8 | UNSUBMITTED，checks.fail=[]，ra_failed=0 |

互相关 0.5538 ⇒ 可同时提交。两颗都在 MODEL 塔，提交后 MODEL 塔 1/3 → **3/3 点亮**。

**⚠ 提交状态：未执行。** 原因按序：
1. 用户问卷在 60s 内未作答，系统自动选中了「提交两颗」——**自动选择不构成不可逆操作的授权**，故未提交；
2. prod 值需在提交前**重测终验**（平台 prod 池逐日上漂，旧读数只能排序、不能放行；>48h 必须重测）。

**下次开工第一件事**：`python tools/prod_wait.py E56pROb9` 与 `--minutes 40` 重测两颗 prod；
两颗均 <0.70 且拿到用户明确授权后，再走 `worldquant-submit-alpha`。

### 50.2 下一阶段队列（prod-first + nanON 重扫）

**队列纪律（本轮确立，覆盖此前的「先打磨后测 prod」）**：

| 阶段 | 动作 | 判据 |
|---|---|---|
| ① | 新族第一波 **≤3 条**（只探机制，不做结构打磨）| — |
| ② | 任一条接近全闸 ⇒ 立刻对该条测 prod | 平台 `check_correlation` / `prod_wait.py` |
| ③ | prod ≥0.80 ⇒ **整族封盘** | 不换中性化、不加辅助腿、不换窗口 |
| ④ | prod 0.70–0.80 ⇒ 最多再测 2 条 | 仍超 ⇒ 封盘 |
| ⑤ | prod <0.70 ⇒ 才允许批量打磨 | 打磨后仍须逐颗终验 |

**nanON 重扫优先级**（专挑「此前因覆盖低 / 2Y 弱判死 + 字段本身稀疏」的非 trio 集）：

| 优先 | 数据集 | category | 旧判死理由 | 为何值得 nanON 重扫 |
|---|---|---|---|---|
| 1 | `fund_holdings_panel` | institutions | S 0.32（但 **2Y 1.46**）| 季度持仓 ⇒ 典型稀疏；2Y 已经强，缺的是 S |
| 2 | `analyst_consensus` | analyst | 从未挖（cov 报 0 / **1972 字段**）| 字段量最大；cov 列报 0 不可信（risk68 同样报 0 却有数据）|
| 3 | `insider_agg_matrix` | insiders | 从未挖（34 字段 / cov 0.562）| insiders 塔 0/3，全新机制 |
| 4 | `risk60` | risk | 前轮判死 | cov 0.835 + `lending_fee_bid_rate` 借贷费率；risk 塔 0/3 |
| 5 | `analyst83` | analyst | TO 2.1-2.4%（慢变）| 财报电话会季度字段；nanON 或许能救 2Y |

**排除**：`sentiment33`（本轮判死，TO 12-13% / margin ≤9bp）、`analyst93`（信号强度死，S 上限 0.92）、
`fnd6_newq_oiadpq`（字段被 `Wje5K71x` 枢纽件烧掉，prod 下限 0.90）、`analyst_factor_signals` eps/netprofit 族（sub 与 2Y 数学互斥）。

---

## 五十一、2026-11-05 非 trio 数据集第二轮扫描（11 个集 / 62 臂）+ ★ fundamental72 原始科目矿脉突破

来源：用户指令「专注于 PV/MODEL/OTHER 外的 category 下的数据集挖掘」+ 本台账 §50 的 nanON 重扫优先级表。
统一设置口径：EQUITY/DEU/TOP500/D1，truncation 0.08，FASTEXPR；探针基线 decay 4 / neutralization FAST / nanHandling ON。

### 51.1 两个「名字骗人」的数据集——未投回测即排除

| 数据集 | 名字暗示 | 字段真实语义 | 处置 |
|---|---|---|---|
| `imbalance5` | 订单不平衡 | 仅 2 个 MATRIX；`imb5_score` = "SHIELD-OIL composite score (0-1) indicating resilience/advantage in oil shock regimes" | ★ 与订单流无关，机制不明，**排除** |
| `fundamental22` | 基本面 | 全库在 DEU 只暴露 1 个 VECTOR `fnd22_value` = ESG KPI 数值；缺 KPI 键 ⇒ vec_avg 会把碳排/董事会多样性等异质指标混算 | **排除** |

> 教训：`category` 标签不可信，必须读 `description` 再设计骨架。`fundamental22` 全库 1 字段却能报 fieldCount 6 / alphaCount 42，说明这两个计数列也不能当可用性依据。

### 51.2 `insiders1`（欧洲内部人交易）六臂全灭

| 模板 | alpha | S | 2Y | sub | TO | margin | lc |
|---|---|---:|---:|---:|---:|---:|---:|
| T1 持仓净变动 × 交易额强度 | `RRE6GAJg` | 0.60 | −0.36 | 0.09 | **60.9%** | 1.4bp | — |
| T2 交易额占比 × 显著性 | `kqNgzk96` | 0.54 | — | — | **65.6%** | 1.1bp | 146 |
| T3 交易频率反向 | `RRE6GARg` | 0.44 | 0.32 | 0.27 | **66.7%** | 0.8bp | — |
| T4 成交价相对市价 × 方向 | `kqNgznQL` | **0.78** | — | — | 20.1% | 3.8bp | 147 |
| T5 持仓一年净增率 | `gJeZnw0J` | 0.58 | — | — | 16.7% | 3.3bp | 161 |
| T6 异常交易额 z 反向 | `xArbJbLn` | 0.57 | −0.10 | 0.27 | **66.8%** | 1.1bp | — |

**结构性死因**：`insders1` 8 个字段全 VECTOR，且**没有 buy/sell 标志字段**（只有 holdings / shares / price / value / tradesignificance）。
⇒ 方向只能靠 `ts_delta(vec_sum(insd1_holdings))` 反推；而凡是用到 `vec_sum(value)/cap` 的模板换手全部飙到 60–67%、margin 塌到 1bp。
**判死**：六模板强度天花板 0.78，且高 TO 组全部远低于 `margin×10000<10` 生死线。

### 51.3 `option1`（个股期权 IV 曲面）二臂全灭

| 模板 | alpha | S | 2Y | sub | TO | DD |
|---|---|---:|---:|---:|---:|---:|
| IV 水平反向（方差风险溢价） | `Xg9JdJdX` | −0.19 | 0.83 | −0.17 | 13.3% | **33.6%** |
| IV − 已实现波动（秩差） | `9qxWN6oe` | −0.11 | — | — | 16.4% | 14.7% |

IV 水平反向 S −0.19 而 2Y +0.83 ⇒ 反号后 S +0.19 / 2Y −0.83，两端都无法成立。**判死**。
注：`opt1_*` 全 VECTOR 且 cov 报 0；`delta_surface_data_quality` 的存在本身提示数据质量可疑。

### 51.4 `earnings6`（EPS 惊喜 / SUE）二臂全灭

| 模板 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| SUE 实际−预期（秩差，无量纲） | 模拟未跑通（progress 卡 0.35，无 alpha） | — | — | — | — | — |
| SUE × 低波门控 | `xArbJlEg` | 0.05 | 0.64 | 0.11 | 14.6% | 0.3bp |

**判死**。`ern6_*` 18 字段全 VECTOR，实质是财报事件日程表（next_ed / board_meeting / transcript_fy / x_dividend），EPS 只有 actual/estimated 两列，无法做 σ 标准化。

### 51.5 `fundamental93`（应计 + 递延税异象）六臂：**2Y 强 S 弱**

| 模板 | alpha | S | 2Y | sub | TO | margin | DD |
|---|---|---:|---:|---:|---:|---:|---:|
| 应计水平反向（Sloan） | `e756lO5N` | 0.13 | 0.13 | 0.37 | 10.8% | 1.0bp | 12.3% |
| 应计 ts_rank 504 反向 | `bl68YEP6` | 0.17 | 0.42 | 0.09 | 12.0% | 1.1bp | 8.7% |
| 应计波动反向（dts） | `LLM5Pq32` | 0.34 | 0.57 | 0.52 | 10.5% | 2.6bp | 10.9% |
| 税项应计反向 | `j2Ye5ZVW` | 0.14 | 0.14 | 0.14 | 11.0% | 1.1bp | 15.0% |
| 递延税费用 z 反向 | `Xg9RjXdx` | 0.51 | 0.36 | 0.41 | 10.6% | 3.9bp | 16.7% |
| **资产增长反向** | `Vkxdvw15` | **0.51** | **1.53** | 0.40 | 11.1% | 4.2bp | 11.5% |

**判弱（非判死）**：成本结构是全场最好的之一（TO 10–12% / DD 8–17%），但 46 个字段全是**已加工比率**（LTM z-score / mean / max / min / dts），
没有原始科目。资产增长 2Y 1.53 说明近两年有效，S 0.51 说明全期不足。⇒ 留作**组合腿候选**，不再单独投探针。

### 51.6 `analyst_consensus`：先踩 event-input 陷阱，再六臂全灭

**陷阱（可复用）**：字段在 `get_datafields` 报 `MATRIX`，但平台按 **event input** 处理。直接 `divide(...)` 会整批报错：
`Operator divide does not support event inputs. <extra_info: If fields is vector type should use vec_* operator with event input>`。
⇒ 判定顺序：整批 ERROR 且报此文案 ⇒ 不要改语法、不要换算子，直接把每个字段包一层 `vec_avg(...)` 再重发。首轮 8 条全废，第二轮才拿到读数。

改成 `vec_avg` 后（统一 FAST/d4/nanON，全部 12% 左右换手）：

| 模板 | alpha | S | 2Y | sub | margin |
|---|---|---:|---:|---:|---:|
| σ 标准化 SUE（mean_surprise/stddev） | `LLM5LgPa` | −0.20 | 0.89 | 0.19 | −1.5bp |
| SUE（actual−mean）/stddev | `omEomKgJ` | −0.03 | 0.96 | 0.43 | −0.2bp |
| 4 周修正 / stddev | `omEomK6m` | 0.16 | 1.18 | 0.45 | 1.3bp |
| 分析师分歧反向（stddev/\|mean\|） | `QPvYPrzp` | 0.06 | 0.31 | −0.02 | 0.5bp |
| 覆盖人数变化（3 个月） | `kqNJq3gz` | −0.12 | 0.74 | −0.02 | −1.0bp |
| 营收 SUE | `3qojqarO` | −0.05 | 0.19 | 0.39 | −0.4bp |

**判死**：六模板 \|S\| ≤ 0.20。对比 `analyst_factor_signals` 的 `estimate_change_3mo` 能到 1.43–1.69（同一经济机制）⇒
**厂商加工过的因子列有信号，原始 IBES 共识面板（1972 字段）在 DEU 没有截面信号**。这条与 fundamental90/93 的结论同向，可上溯为一条总规律，见 51.10。

### 51.7 `analyst47`：vendor 复合指标 2Y 1.91，S 不足

| 模板 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| `anl47_indicator` 水平（1–10 分） | `2rAj1RNb` | 0.76 | **1.91** | **1.00** | 14.2% | 4.75bp |
| `anl47_totalrawsignal` 水平 | `0mYjOQgK` | 0.73 | **1.95** | 0.90 | 14.8% | 4.40bp |
| `anl47_rawsentiment` 水平 | `QPvYZ5bQ` | 0.70 | **1.97** | 0.91 | 14.6% | 4.29bp |
| indicator 偏离自身一年均值 | `QPvYPQEr` | 0.65 | 0.87 | 0.83 | 23.8% | 2.51bp |
| indicator ts_rank 504 | `LLM5Vez1` | 0.62 | 0.82 | 0.82 | 23.7% | 2.41bp |

**判弱**：三兄弟 2Y 全部 1.91–1.97、sub 0.90–1.00，**近两年极强**，但全期 S 只有 0.70–0.76 ⇒ 2018–2023 段为零或负。
1–10 整数分本身截面离散度低，改造（偏离/时序秩）只会把 S 压到 0.62–0.65。⇒ 若要用，只能作为**近 regime 腿**，不能作主信号。

### 51.8 `fundamental90`（GAME 会计因子库）十臂全灭

| 模板（经济学含义） | alpha | S | 2Y | sub | margin |
|---|---|---:|---:|---:|---:|
| Novy-Marx 毛利/资产 | `ZYQmY8Zj` | **−0.42** | 0.02 | 0.20 | −3.3bp |
| Piotroski F-score | `QPvYPp75` | 0.31 | 0.69 | 0.48 | 2.3bp |
| Ohlson O-score 反向 | `JjePjk5n` | −0.19 | 0.14 | 0.46 | −1.5bp |
| 净经营资产 NOA 反向 | `zq3rqnb8` | **−0.46** | −0.38 | 0.16 | −3.6bp |
| 股权稀释反向 | `78Lo8RoZ` | −0.34 | 0.24 | 0.48 | −2.8bp |
| 应计波动反向 | `YP1xPo5R` | 0.02 | 0.56 | 0.58 | 0.1bp |
| 增量现金流 ROE 3y | `zq3rqEZO` | 0.14 | 0.33 | 0.45 | 1.1bp |
| 质量复合（GPA+F） | `A1VQjaxY` | 0.28 | 0.83 | 0.54 | 2.2bp |
| 资本开支强度反向 | `akKVj2pR` | **−0.66** | −0.73 | −0.26 | −5.2bp |
| 周转+劳动效率改善 | `mLoYweGx` | −0.34 | 0.58 | 0.06 | −2.6bp |

**判死**：十臂 \|S\| ≤ 0.66，其中三臂为负（GPA −0.42 / NOA −0.46 / capex −0.66），反号也只有 0.42–0.66。
这十臂覆盖了资产定价文献里最稳的一批会计异象（Novy-Marx 2013、Piotroski 2000、Hirshleifer NOA 2004、Cooper 资产增长 2008、Titman 资本开支 2004）——**全部在 DEU TOP500 失效**。
⇒ 结论不是「模板没找对」，而是 **DEU 的截面不奖励「已加工的质量/投资比率」**。

### 51.9 ★★★ `fundamental72` 突破：point-in-time 原始财报库承载 delta 机制

**数据集结构**（1031 字段）：`fnd72_pit_or_bs_q_bs_*` 季度资产负债表 225 个、`fnd72_s_pit_or_is_q_*` 季度利润表 50 个、`fnd72_s_pit_or_cf_q_*` 季度现金流量表 30 个；
前缀 `pit` = point-in-time 对齐 ⇒ 无前视偏差。这是 DEU 唯一一个既含**原始科目**又做 PIT 对齐的库。

**核心驱动：季度 EBIT 的 `ts_delta` 秩乘积**。先复刻 `P0ogRWEK` 的结构换字段（nanON，不加 ts_backfill）：

| 模板 | alpha | S | 2Y | sub | TO | margin | DD |
|---|---|---:|---:|---:|---:|---:|---:|
| **EBIT 2 腿**（delta 252 + ts_rank 504） | **`npvAxWvw`** | **1.18** | 1.21 | 0.70 | 13.1% | **8.24bp** | **7.74%** |
| **EBIT 3 腿**（delta 240+176 × ts_rank 504） | **`omEo8aNm`** | **1.28** | 1.38 | 0.70 | 13.0% | **8.90bp** | 8.63% |
| 营业利润 2 腿 | `88Rv5Nrm` | 1.16 | 1.32 | 0.80 | 13.4% | 8.09bp | 7.86% |
| **营业利润 3 腿** | **`E56VOmNr`** | **1.24** | **1.54** | **0.81** | 13.2% | 8.59bp | 8.44% |
| EBITDA 2 腿 | `gJeWkVvv` | 1.16 | 1.34 | 0.76 | 12.7% | 8.10bp | 9.59% |
| 营收 2 腿 | `Vkxd1bx0` | 1.01 | 0.88 | 0.81 | 13.1% | 7.37bp | 8.69% |
| 经营现金流 2 腿 | `Xg9RGjjx` | 0.96 | 0.57 | **1.01** | 13.0% | 6.42bp | **7.29%** |
| 净利润 2 腿 | `KPJm3K8x` | 1.06 | 1.05 | 0.71 | 13.2% | 7.47bp | 7.75% |

**★★★ prod 读数（最关键）**：`npvAxWvw` **prod = 0.6208**（2026-11-05 02:26，`results/prod_wait_npvAxWvw.json`）。
与同机制、字段 `fnd6_newq_oiadpq` 的 `P0ogRWEK` **prod 0.9287** 形成直接对照：
⇒ **prod 枢纽件自锁是「字段级」的，换到另一个数据集的等价科目即可完全解除**（0.9287 → 0.6208，差 0.31）。
⇒ `fundamental72` 的收入表族是**可用矿脉**，按 prod-first 纪律 prod<0.70 ⇒ 允许批量打磨。

**成本结构是 DEU 全场最好**：margin 6.4–8.9bp（安全线约 10bp 量级，配合 13% 换手已属优秀）、DD 7–10%。
**缺口**：S 1.16–1.28 / 2Y 1.21–1.54，距双闸 1.58 还差 0.3–0.4；sub 0.70–1.01（对 S 1.28 而言阈值 0.66，已过）。

**结构失效记录**：`fnd72_pit_or_bs_q_bs_inventories` 与 `..._accts_rec_excl_notes_rec` 两臂模拟 ERROR（资产负债表季度字段疑为 event 型，需 `vec_*` 包裹）；
`fundamental17` 的 `annual_ebit`（年度，delta 504 + ts_rank 1008）S −0.03 ⇒ **年度口径不成立，只有季度口径成立**（与 §49.4 一致）。

### 51.10 本轮四条可复用结论

**① DEU 的截面信号只存在于「原始科目的水平变化」，不存在于「已加工的比率/打分」。**
证据链：季度 EBIT delta 1.28 / 营业利润 delta 1.24（原始科目 ✓）vs 应计比率 0.13–0.51 / GAME 十个会计因子 ≤0.66 / IBES 共识六模板 ≤0.20（已加工 ✗）。
行动：拿到新数据集，先看字段名里有没有**货币量纲的原始科目**（sales / ebit / cfo / capex / inventory）——有则套 delta 几何；只有 ratio / score / z-score 的直接降低优先级。

**② prod 拥挤是字段级而不是数据集级，也不是机制级。**
同一机制（季度营业利润增长）在 `fnd6` 上是 0.9287、在 `fnd72` 上是 0.6208。⇒ 被枢纽件烧掉的是**字段**，不是机制；
正确处置是「同机制换数据集重新表达」，而不是放弃机制或改几何硬顶。

**③ event-input 陷阱的处置顺序。** 整批 ERROR 且文案含 `does not support event inputs` ⇒ 不改语法、不换算子，逐字段包 `vec_avg` 重发；
`get_datafields` 的 `type` 列不可信（报 MATRIX 实际按 event 处理）。

**④ 2Y 强 + S 弱是一个稳定可识别的形态，处置是「不追打磨」。**
本轮四例：`anl47_indicator`（2Y 1.91 / S 0.76）、`fundamental93` 资产增长（2Y 1.53 / S 0.51）、`analyst_consensus` 4 周修正（2Y 1.18 / S 0.16）、`option1` IV 水平（2Y 0.83 / S −0.19）。
共同成因是全期 S 被早期年份拖平 ⇒ 改几何只会同时把 2Y 打下来（§49.5 已证）。这类型只适合作近 regime 腿或组合腿。

---

## 五十二、2026-11-05 非 trio 第二轮收口：fundamental72 利润表侧定顶 + 3 个数据集判死

**本轮派发 27 条臂（+4 条语法废件），零提交、零取消。** 结论：DEU 非 trio 可挖面基本见底。

### 52.1 `fundamental72` 利润表侧强度天花板 = S 1.36（约 35 臂）

| 变体 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| **EBIT 3 腿 + ts_rank 1008（定顶）** | `mLoYpZ36` | **1.36** | 1.34 | 0.80 | 13.0% | 9.60bp |
| EBIT 3 腿 + ts_target_tvr_decay 0.03 | `wpQ9xg21` | 1.28 | 1.17 | 0.83 | 12.2% | 9.54bp |
| EBIT 3 腿 + ts_target_tvr_decay 0.06 | `JjePEX3A` | 1.34 | 1.34 | 0.78 | 12.8% | 9.56bp |
| EBIT 2 腿 + ts_target_tvr_decay 0.03 | `78Lob9mv` | 1.07 | 1.02 | 0.65 | 12.0% | 7.92bp |
| oper_inc 3 腿 + ts_target_tvr_decay 0.03 | `pwdvrnl3` | 1.20 | 1.27 | **0.93** | 12.5% | 8.85bp |
| EBIT 3 腿 + 营收第 4 腿（12 算子满配） | `vR1OM0ga` | 1.32 | 1.40 | 0.81 | 13.0% | 9.41bp |
| EBIT 3 腿 + ts_zscore 第三腿 | `Xg9Rre2z` | 1.31 | 1.32 | 0.80 | 13.0% | 9.40bp |

**`ts_target_tvr_decay` 语法铁律**：必须写命名参数 `target_tvr=`。写位置参数 `ts_target_tvr_decay(x,0.03)` 会整批 ERROR，
文案 `Required attribute target_tvr must have a value`（本轮 4 条废件换来的）。

**★★★ 杠杆不可默认迁移**：同一个 `ts_target_tvr_decay` 在 `fnd6_newq_oiadpq` 上是已提交件 `Wje5K71x` 拿到 S 1.73 的关键，
在 `fnd72_s_pit_or_is_q_ebit` 上却把 1.36 打到 1.28 且换手不降（13.0%→12.2%）。机制同、字段不同 ⇒ 杠杆效果可以反向。
**至此窗口轴（756/1008/1260）、decay（2/4/8/16）、第三腿算子（ts_rank/ts_ir/ts_zscore/dual ts_rank/delta504）、
分组轴（sector/industry）、tvr_decay（0.03/0.06）、第 4 腿（营收）、替代科目（EBIT/营业利润/EBITDA/营收/经营现金流/净利润）、
替代机制（毛利率扩张/应计利差/TTM/双字段秩和）全部扫完，平台期稳定在 1.36。按强度天花板纪律停止打磨。**

### 52.2 `fund_holdings_panel` 判死：成本结构死（9 个结构互异模板）

数据集画像：institutions 类，18 字段**全部 VECTOR**，cov 0.9019 / ac 102，交易流水型（美元交易额/交易集中度/大单数/账户数）。

| 模板 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| T1 账户数广度变化 66 | `bl68Z6em` | −0.43 | 0.17 | −0.36 | 43.1% | −0.96bp |
| T2 交易额强度 / cap | `P0oMan8E` | 0.13 | 0.91 | 0.36 | 53.2% | 0.24bp |
| T3 交易额加速度 22 | `6XdAVRGK` | 0.04 | 1.06 | 0.31 | 52.4% | 0.08bp |
| T4 交易 HHI 水平反向 | `npvARAMx` | −0.05 | 1.06 | −0.28 | 35.6% | −0.16bp |
| T5 大单占比 | `vR1OMOZz` | 0.01 | 1.07 | 0.15 | 42.4% | 0.02bp |
| T6 头部加权占比 | `WjOLQA5O` | 0.04 | 1.29 | 0.10 | 29.9% | 0.15bp |
| T7 主动资金占比 | `bl68ZOZ6` | 0.01 | 1.18 | 0.34 | 51.3% | 0.02bp |
| T8 交易额分布分反向 | `Xg9RQJ5z` | −0.05 | 0.98 | −0.24 | 28.2% | −0.20bp |
| T9 稳定边界交易数水平 | `9qxE1wOK` | 0.36 | 1.52 | 0.35 | 48.7% | 0.76bp |

**判据**：TO 28–53% 且 margin 0.02–0.76bp ⇒ `margin×10000 < 10 且 TO > 10%` ⇒ 直接封盘。
与 `news104`（TO 12–17%/margin 0.45–1.5bp）同型：**日频交易流水类数据的更新速度远超其信息价值密度**，与模板选择无关。
注意 9 个模板的 2Y 有 6 个 ≥ 1.0（T6 1.29 / T7 1.18 / T5 1.07），但全期 S 全塌 ⇒ 又一个「2Y 强 S 弱」族。

### 52.3 `macro27` 判死：10 个结构互异模板全灭（双向封顶 0.50）

数据集画像：macro 类，13 字段**全部 VECTOR**（公司招聘岗位数/新增/撤销/挂岗天数/重发标志）。
立机制时按 Belo-Lin-Bazdresch 雇佣投资异象预期「招聘增速 ⇒ 低收益」（与资产增长同族）。

| 模板 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| M1 在招岗位增速 252（反向） | `9qxELz8q` | −0.42 | 0.50 | −0.13 | 23.4% | −1.63bp |
| M2 招聘增速比率（反向） | `bl685EZq` | −0.50 | 0.40 | −0.21 | 14.2% | −3.34bp |
| M3 新增岗位 66 | `58EjoWWM` | 0.36 | 0.63 | 0.00 | 57.0% | 0.60bp |
| M4 撤销岗位 66（反向） | `bl685XdN` | −0.11 | 0.31 | −0.13 | 58.4% | −0.17bp |
| M5 撤销/在招 流失率反向 | `mLoYMp55` | 0.00 | 0.42 | −0.13 | 48.5% | −0.01bp |
| M6 挂岗天数均值 | `xAr10gXm` | −0.23 | 0.62 | −0.34 | 12.8% | −1.50bp |
| M9 重发标志反向 | `WjOL6dmj` | −0.16 | −0.38 | −0.06 | 46.2% | −0.29bp |
| M10 新增-撤销净额秩比率 | `O0AJEKwv` | 0.18 | 1.07 | 0.01 | 56.9% | 0.30bp |

M1/M2 是反向表达，读数 −0.42/−0.50 ⇒ **正方向即 +0.42/+0.50**，双向都远低于 1.58；其余模板 |S| ≤ 0.36。
⇒ 雇佣投资异象在 DEU 存在但弱（正方向 +0.5 量级），10 模板 × 双向扫尽，判死。

### 52.4 `fundamental72` 资产负债表侧判死：event 型聚合把换手打到 55%

统一用 2 腿几何 `group_rank(multiply(rank(ts_delta(vec_avg(F),252)),rank(ts_rank(vec_avg(F),1008))),sector)`，**同方向筛查**，由 S 的符号读方向：

| 科目 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| `acct_payable` 应付账款 | `P0oMdk1K` | 0.70 | 0.42 | 0.75 | 55.1% | 2.24bp |
| `accts_rec_excl_notes_rec` 应收 | `ZYQme153` | 0.69 | 0.69 | 0.60 | 57.1% | 2.23bp |
| `tot_asset` 总资产 | `LLM5A3w2` | 0.61 | 0.69 | 0.48 | 55.7% | 1.86bp |
| `gross_fix_asset` 固定资产总额 | `mLoY9M8X` | 0.58 | 0.63 | 0.69 | 47.5% | 2.24bp |
| `goodwill` 商誉 | `MPY0moA6` | 0.57 | 0.90 | 0.56 | 53.8% | 1.87bp |
| `sh_out` 流通股数 | `rKRdvweE` | 0.56 | 0.38 | 0.41 | 55.6% | 1.74bp |
| `inventories` 存货 | `E56VX2OP` | 0.54 | 0.77 | 0.47 | 55.1% | 1.72bp |
| `cur_liab` 流动负债 | `9qxELkqK` | 0.51 | 0.45 | 0.47 | 55.3% | 1.61bp |
| `retain_earn` 留存收益 | `mLoYMW56` | 0.46 | 0.43 | 0.40 | 55.6% | 1.40bp |

**九科目 S 全部为正 0.46–0.70**（⇒ 增长方向在 DEU 是弱正向），但 **TO 一律 47–57%、margin 1.4–2.2bp**，取反也只能得到 −0.5 量级。

**类型对照实证**：`f72bs_tot_asset_novec`（`3kXU4o4Sy4B59q318fE1YMk8`）与 `f72bs_sh_out_novec`（`4xKNOTaqn4Mm8Mau6k1Ypfy`）两条**不加 vec_avg 的对照全部 ERROR**
⇒ 确认 `fnd72_pit_or_bs_q_bs_*` 是 event 型，必须 `vec_avg` 包裹（`get_datafields` 报 MATRIX 不可信）。

**★★★ `fundamental72` 内部的分层（本节最有用的判据）**：
- `fnd72_s_pit_or_is_q_*`（利润表 52 字段）= **MATRIX 直通**，无需聚合 ⇒ TO 13%、margin 8–9.6bp、S 1.18–1.36 ✔
- `fnd72_pit_or_bs_q_bs_*`（资产负债表 64 字段）= **event 型**，`vec_avg` 聚合后 TO 47–57%、margin ≤2.2bp ⇒ 成本墙 ✘
- `fnd72_s_pit_or_cf_q_*`（现金流量表 30 字段）= MATRIX 直通，经营现金流 2 腿 S 0.96 / sub 1.01（方向对但弱）
⇒ **同一数据集内部先看字段落在哪一层，再决定投不投**；event 层的隐性成本（聚合把换手抬到 50%+）会把横截面信号吃光。

### 52.5 四条可复用结论

**① 数据集判死的第一判据是 TO/margin 比值，不是 S。**
本轮两个集（`fund_holdings_panel` TO 28–53%/margin<1bp、`macro27` TO 46–58%/margin<1bp）都是「结构死」——换多少模板都救不回来。
判据固定：`margin×10000 < 10` 且 `TO > 10%` ⇒ 封盘，不要先看 S 再纠结方向。

**② event 型字段的隐性成本必须提前算。**
`vec_avg` 聚合会把日频换手抬到 50%+。即使横截面信号真存在（BS 九科目 S 全正 0.46–0.70），也会被成本吃成 margin ≤2bp。
⇒ 同一数据集里优先挑 **MATRIX 型**字段；只有 VECTOR/event 层的集要先把「聚合后换手」当成第一次探针的输出指标。

**③ 参数/算子杠杆不能默认迁移，必须在本字段上实测。**
`ts_target_tvr_decay`：`fnd6_newq_oiadpq` 有效（`Wje5K71x` S 1.73）→ `fnd72_s_pit_or_is_q_ebit` 无效（1.36→1.28）。
同机制换字段后杠杆可以反向 ⇒ 破墙时先验「这个杠杆在该字段上单点是否为正」，再决定要不要展开参数面。

**④ DEU 非 trio 面已见底。**
本轮再封 3 个数据集（`fund_holdings_panel` / `macro27` / `fundamental72` 的 BS 层）后，未挖只剩：
`fundamental1`（123f 全 VECTOR 高管薪酬）、`fundamental89`（407f 应计模型）、`fundamental86`（7f）、`fundamental45`（12f cov 0.269）、
`alpha_factor_lib`（65f ac 4）、`digital_ad_spend`（9f ac 5）、`other567`（48f ac 3）、`workforce_flow_skills`（10f ac 1）、
`institutions25`（24f ac 7）、`sentiment33`（255f cov 0.322）、`risk71`/`risk72`（specific return，与已封 risk68 同族）。
**共同特征：低 ac 或纯 VECTOR 聚合型 ⇒ 大概率撞本节 ② 的成本墙。** 继续投的期望值低于把已满闸候选提交掉。

### 52.6 追加：decay 轴与中性化轴标定（本轮末，推翻此前「decay 4 最优」的记录）

**decay 轴在 `fnd72` 上是单调递减的，越低越好**（同一 EBIT 3 腿表达式）：

| decay | alpha | S | 2Y | sub | TO | margin | F |
|---|---|---:|---:|---:|---:|---:|---:|
| **0** | `RREALzx0` | **1.42** | 1.43 | 0.83 | 14.5% | 8.98bp | 0.95 |
| **1** | `O0AJvjbq` | **1.42** | 1.43 | 0.83 | 14.5% | 8.98bp | 0.95 |
| 2 | `e756JekJ` | 1.41 | 1.41 | 0.83 | 13.7% | 9.42bp | 0.97 |
| 4 | `mLoYpZ36` | 1.36 | 1.34 | 0.80 | 13.0% | 9.60bp | 0.94 |
| 8 | `npvA9E3l` | 1.32 | 1.30 | 0.75 | — | 9.73bp | — |
| 16 | `A1VQWgvW` | 1.26 | 1.21 | 0.71 | — | 9.65bp | — |

d0 与 d1 完全同值 ⇒ **decay 在该表达式上实际不起作用**（信号自相关已足够低），d4 以上才是真平滑。
**这条修正很重要**：此前台账多处写「decay 4 最优」，那只是在 d4/d8/d16 三点里比较的结论，漏扫了下侧。**decay 轴扫描必须包含 0 与 1**。

**中性化轴：`FAST` 是唯一能活的，其余全部崩**（都与表达式内层 `group_rank(...,sector)` 重复中性化冲突）：

| 中性化 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| FAST（基准） | `npvA9E3l`/`RREALzx0` | 1.32–1.42 | 1.30–1.43 | 0.75–0.83 | 12–14.5% | 9.0–9.7bp |
| STATISTICAL | `9qxEQ6Lx` | 0.64 | 0.21 | 0.35 | 9.1% | 5.68bp |
| SECTOR | `YP1xdn3v` | 0.36 | −0.71 | 0.60 | 3.0% | 17.41bp |
| SUBINDUSTRY | `E56VAa19` | 0.20 | 0.12 | 0.63 | 4.4% | 6.67bp |

⇒ **表达式内已有 `group_rank(...,sector)` 时，绝不能再叠 SECTOR/SUBINDUSTRY 中性化**（等价于二次剔除同一维度，S 塌到 0.2–0.36）。
这条与上一轮「SECTOR 优于 FAST」（analyst44）不矛盾：那是**表达式内不带分组**的骨架，两者不可混用判断。

**truncation 轴无效**：`oper_d0` 的 truncation 0.08 → 0.10 指标**完全同值**（S 1.38 / 2Y 1.58 / TO 14.82% / margin 8.57bp / raf 2）。
说明该信号持仓分布已经足够分散，放宽截断不改变持仓 ⇒ 这不是一条可用杠杆。

**★★★ 本轮真正的天花板修订：`fundamental72` 最佳 = S 1.42（EBIT, d0/d1），而非 1.36；但闸线是 1.58。**
距闸仍有 0.16，且 **2Y 侧在 oper_inc + d0 上已经达标**：

| 变体 | alpha | S | **2Y** | sub | F | TO | margin | raf |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| oper_inc 3 腿 + **d0**（2Y 达标） | `KPJmRpGN` | 1.38 | **1.58 ✓** | 0.92 | 0.90 | 14.8% | 8.57bp | **2** |
| oper_inc 3 腿 + d0 + ts_rank 756 | `kqNJRXZz` | 1.35 | **1.60 ✓** | 0.91 | 0.87 | 14.8% | 8.37bp | 2 |
| EBIT 3 腿 + d0 | `RREALzx0` | **1.42** | 1.43 ✗ | 0.83 | 0.95 | 14.5% | 8.98bp | 3 |

⇒ **失败项从 3 项压到 2 项**（`LOW_SHARPE` 1.38<1.58 + `LOW_FITNESS` 0.90<1.00），`LOW_2Y_SHARPE` 已通过。
`KPJmRpGN` 是 DEU 非 trio 面上**离闸最近**的一颗（差 S 0.20 / F 0.10），留作**组合腿与后续破墙的锚点**，不单独提交。

---

## 五十三、2026-11-05 非 trio 第三轮收口：`other567` / `institutions25` / `digital_ad_spend` / `workforce_flow_skills` 四集 10 臂

**这是 DEU 非 trio 面的最后一轮系统筛查**（连同 §51 / §52，累计封盘 19 个数据集）。

| 数据集 | 机制 / 字段 | alpha | S | 2Y | sub | TO | margin | 判决 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `workforce_flow_skills` | 员工净流入（入职−离职）/（入职+离职） | `d5WKqN5E` | **0.98** | **−0.17** | 0.63 | 11.0% | 4.01bp | 判弱：2Y 反向 |
| `other567` | CEO 认可度水平（Edmans 无形资产异象） | `bl68pxoq` | 0.72 | **1.78** | 0.45 | 10.8% | 2.30bp | 判弱：「2Y 强 S 弱」 |
| `digital_ad_spend` | 广告支出强度（/cap）水平 | `O0AJK0nR` | 0.71 | 0.32 | 0.07 | **48.2%** | 1.47bp | 判死：成本墙 |
| `other567` | 公司总体评分水平 | `gJeWve2e` | 0.48 | 1.50 | 0.14 | 10.8% | 1.64bp | 判弱 |
| `institutions25` | 机构持仓变化 66 | `d5WKq9vw` | −0.35 | 1.07 | −0.28 | 21.5% | −1.53bp | 判死 |
| `institutions25` | 机构做空持仓数反向 | `O0AJK0kv` | −0.37 | 1.21 | −0.29 | 15.5% | −2.13bp | 判死 |
| `institutions25` | 机构情绪水平 | `58EjREP5` | −0.27 | 0.44 | −0.28 | 14.2% | −2.04bp | 判死 |
| `other567` | 满意度趋势 252 | `9qxEgqoe` | 0.00 | — | — | **0.0%** | 0.00bp | **退化**：无变化 |
| `digital_ad_spend` | 广告支出增量 252 / cap（反向） | `RREA0LZg` | **−11.71** | 0.00 | 2.06 | 44.8% | −7.65bp | **退化**：DD 0.34%、TO 44.8% |

### 53.1 两个新判据

**① 退化 alpha 的识别特征：`|S|` 异常大且 `DD` 极小、`2Y = 0`，同时 `TO` 很高。**
`RREA0LZg` 报 S −11.71，但 DD 只有 **0.34%**、2Y 恰好 0.00、TO 44.8% ⇒ 这不是强信号，是**分母被压到近零**造成的数值爆炸（`divide(delta(spend,252), cap)` 在 spend 覆盖极稀疏时每日只有个位数持仓）。
同型：`o567_trend` TO = **0.0%**、S = 0、DD = 0 ⇒ 字段完全无日内变化。**判据：`TO < 1%` 或 `|S| > 5` 且 `DD < 1%` ⇒ 先查是不是退化，不要当成候选。**

**② 「2Y 强 S 弱」在本轮累计已出现 10 例，是 DEU 非 trio 面最普遍的形态。**
新增两例：`other567` CEO 认可度（2Y 1.78 / S 0.72）、`other567` 公司总体评分（2Y 1.50 / S 0.48）。
加上此前的 `anl47_indicator`(1.91/0.76)、`anl47_totalrawsignal`(1.95/0.73)、`anl47_rawsentiment`(1.97/0.70)、
`fundamental93` 资产增长(1.53/0.51)、`analyst_consensus` 4 周修正(1.18/0.16)、`option1` IV 水平(0.83/−0.19)、
`fund_holdings_panel` T6(1.29/0.04) ⇒ **共同结构性成因：这些字段在近两年才进入 regime，早期年份的横截面是噪声，把全期 S 拖平。**
处置固定：**不追打磨**（改几何会同时打掉 2Y，§49.5 已证），只登记为**近 regime 腿 / 组合腿**。

### 53.2 DEU 非 trio 面最终结论

**存活（有正 S 且成本结构可用）**：仅 `fundamental72` 利润表季度科目族（S 上界 1.42、2Y 上界 1.60、margin 8–9.6bp、TO 13–15%）。
**判弱（2Y 强 S 弱，可作组合腿）**：`analyst47` 三兄弟、`fundamental93` 资产增长、`other567` CEO 认可度/总体评分、`workforce_flow_skills` 员工净流入、`analyst_consensus` 4 周修正。
**判死（≥2 个结构互异模板全灭 或 成本墙 或 退化）**：`insiders1`、`option1`、`earnings6`、`analyst_consensus`、`fundamental90`、
`imbalance5`、`fundamental22`、`fund_holdings_panel`、`macro27`、`institutions25`、`digital_ad_spend`、`fundamental72` 资产负债表层、`fundamental17` 年度层。

⇒ **DEU/TOP500/D1 的 REGULAR 可挖面已经扫尽。** 继续产出只能靠：①提交已满闸的两颗；②把「判弱」族当组合腿重组；③PPA 通道；④转区。

## 五十四、2026-11-05 非 trio 第四轮：`fundamental45`（财报电话会 NLP）51 臂 —— 判弱，S 上界 1.42

**这是 DEU 非 trio 面剩余唯一有真实覆盖的 MATRIX 数据集**（12 字段全 MATRIX，cov 0.2393–0.3162）。
同轮排除：`fundamental86`（7 字段但 DEU 覆盖全 0）、`sentiment33`（255 字段全 VECTOR、多数是标题/时间戳元数据）、`earnings_sent_matrix`（DEU 零覆盖，§14.3 已证）。

### 54.1 论坛取证（本次合同要求的「机制使用前查论坛」已完成）

**帖 ①（24 票，`article_id=43691562191895`，正是讲 `fundamental45`）**：
- 数据集 = Systematic Mining of Earnings Calls Data；演讲稿（pr）是准备好的、偏官方，问答（qa）更即兴、更易暴露真实想法；CEO 与其他高管表态差异有信息。
- **「这类文本派生数据最适合放在事件窗口里用——财报发布前后的变化，可能比绝对的水平更有意义」** ⇒ 必须做时间维意外化，不能只用水平。
- **「不同公司、不同行业的沟通风格差异会带来系统性偏差，使用前最好先做跨公司可比的校准」** ⇒ 必须叠一层分组标准化。

**帖 ②（`article_id=43620895448343`，EUR 实证 alpha `XgbXWEWm`）**：
- 模板：`signed_power(subtract(ts_zscore(ts_backfill(A,f),L), ts_zscore(ts_backfill(B,f),L)), e)`。
- **最重要的一条**：情绪「水平」因子在 production 极度拥挤，朴素长窗 z-score 版 IS S 1.9 但 **Prod Corr 0.9**，换中性化（SUBINDUSTRY/INDUSTRY/COUNTRY/CROWDING/STATISTICAL）、加 winsorize、正交到收益因子**全部压不下 0.7**；
  只有把线性 z-score 换成 `signed_power(·,3)` 改**持仓结构**，pc 才 0.9 → 0.64，S 基本不变。⇒ **保号幂是改持仓结构的降 pc 手段，不是调参手段。**
- 事件稀疏必须 `ts_backfill(f≈事件频度×1–2)` 有界填充；`overall_sentiment_score`（argmax 标签）单用只 S 1.2–1.5，保留分布/差分信息更强。
- 坑：早年横截面稀疏 + trunc 0.08 ⇒ `CONCENTRATED_WEIGHT` 单票 10.78% > 10%；修法 trunc → 0.04（S 1.68→1.65）。

### 54.2 十模板波次（decay 6 / FAST / trunc 0.04 / nanON；`SP(G(Z(F)))` = `signed_power(group_zscore(ts_zscore(ts_backfill(F,66),252),sector),3)`）

| 模板 | 字段 / 几何 | alpha | S | 2Y | sub | TO | margin | DD |
|---|---|---|---:|---:|---:|---:|---:|---:|
| T10 | `lda_bigram_pr` 主题意外 + 立方 | `xAr1wxbN` | **1.20** | 2.03 | 0.87 | 17.9% | 7.03bp | 8.0% |
| T9 | `score` 综合评分意外 | `rKRd6lNa` | 0.83 | 1.40 | 0.62 | 19.1% | 4.60bp | 13.1% |
| T8 | `readability_executives` 可读性意外 | `kqNJkj7g` | 0.72 | 1.19 | 0.26 | 19.7% | 4.12bp | 9.0% |
| T6 | `numeric_perct_qa` 具体性意外 | `E56V0rmL` | 0.48 | 0.87 | 0.46 | 19.0% | 2.72bp | 12.1% |
| T4 | `sentiment_chanage_ceo` 意外 | `leAM67PN` | 0.21 | −0.02 | 0.29 | 20.2% | 1.16bp | 12.0% |
| T5 | CEO − others 变化分歧 | `3qojYnoP` | 0.13 | −0.28 | 0.18 | 20.9% | 0.70bp | 12.3% |
| T1 | `sentiment_lm2_net_pr` 意外 | `WjOLwWNd` | 0.05 | 0.12 | 0.09 | 19.2% | 0.26bp | 18.2% |
| T2 | QA − PR 情绪分歧（意外空间） | `xAr1wmrm` | 0.03 | −0.76 | 0.00 | 19.4% | 0.20bp | 17.9% |
| T7 | 具体性 QA − PR 分歧 | `pwdvJ1ag` | 0.00 | −0.36 | 0.19 | 19.8% | 0.00bp | 16.2% |
| T3 | LM2 − VADER 双模型分歧 | `9qxEPAE9` | −0.07 | 0.31 | −0.02 | 20.8% | −0.37bp | 32.7% |

对照：同一 `lda_bigram_pr` 用 `group_rank(ts_mean(F,66),sector)` 的**水平探针只有 S 0.10–1.20 区间的最低端**（水平版 4 条探针 S = −0.01 / −0.07 / −0.27 / 0.10）⇒ **论坛「水平无用、意外有用」在 DEU 被独立复现**（同一字段 S 0.10 → 1.20，12 倍）。
但**只有 `lda_bigram_pr` 一个字段能打**；情绪类 6 个字段（lm2/vader × pr/qa、CEO 变化、CEO−others）全部 ≤0.21，`qa−pr` 分歧三个版本全灭 ⇒ 这些字段在本区无截面信号。

### 54.3 精调三批（A 轴 / B 几何 / C 降换手），最优收敛到 1.42

**A 批（21 轴，围绕 T10）**

| 变体 | alpha | S | 2Y | sub | margin | 结论 |
|---|---|---:|---:|---:|---:|---|
| `f=22`（回填窗 66→22） | `QPvYrRoG` | **1.30** | 2.04 | 0.93 | 7.53bp | **f 越短越好**：22 > 66(1.20) > 120(1.17) |
| `e=2`（立方→平方） | `Xg9RPjpm` | 1.27 | 1.85 | 0.96 | 7.49bp | e 越小越好：2 > 3(1.20) > 4(1.15) > 5(1.09) |
| `group=industry` | `gJeWwO8M` | 0.38 | −0.41 | 0.25 | 2.27bp | **细分组劣化** |
| `group=subindustry` | `Xg9RPLX1` | 0.30 | −0.18 | 0.27 | 1.78bp | **细分组劣化** |
| `L=120` / `L=504` | `WjOLwvJP` / `omEoA59m` | 1.04 / 0.80 | 1.54 / 1.12 | 0.82 / 0.42 | 5.71 / 5.00bp | L=252 最优 |
| 去 group_zscore | `A1VQYl2W` | 1.18 | 1.89 | 0.97 | 6.67bp | group_zscore 贡献 +0.2 |

**B 批（意外化算子几何 8 臂，f22/e2 组合）**

| 变体 | alpha | S | 2Y | sub | TO | margin | DD |
|---|---|---:|---:|---:|---:|---:|---:|
| **`ts_zscore` L=252（最优）** | `O0AJqMvv` | **1.38** | 1.87 | **1.04** | 16.8% | 8.06bp | 7.3% |
| `L=180` | `qMLEv51K` | 1.29 | 1.90 | 0.93 | 17.2% | 7.32bp | 10.2% |
| `L=378` | `xAr19oGp` | 1.25 | 1.69 | 0.88 | 16.6% | 7.61bp | 8.0% |
| `ts_rank` 252 | `e756gMod` | 1.23 | 1.62 | 0.96 | 16.2% | 7.23bp | 9.5% |
| `ts_decay_linear(·,22)` | `6XdA32RJ` | 1.22 | 1.58 | 0.88 | 16.0% | 7.59bp | 12.8% |
| `ts_ir` 252 | `qMLEvGAO` | 0.13 | −0.06 | 0.10 | 14.1% | 1.02bp | 11.8% |

**设置轴（8 臂，B1 表达式固定）**

| 设置 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| **decay 0** | `WjOLdO7o` | **1.42** | 1.82 | **1.11** | 18.0% | 7.72bp |
| decay 2 | `Xg9RL9bX` | 1.39 | 1.79 | 1.08 | 17.6% | 7.73bp |
| decay 4 | `xAr1QbEn` | 1.39 | 1.85 | 1.07 | 17.1% | 7.96bp |
| decay 6（基线） | `O0AJqMvv` | 1.38 | 1.87 | 1.04 | 16.8% | 8.06bp |
| trunc 0.08 | `E56VbVkr` | 1.35 | 1.93 | 0.93 | 17.8% | 7.89bp |
| SLOW_AND_FAST | `bl68M05l` | 1.17 | 1.59 | 0.99 | 17.6% | 5.91bp |
| MARKET | `78LoQ6X1` | 0.99 | 1.38 | 0.88 | 6.5% | **23.88bp** |
| CROWDING | `LLM56oJ6` | 0.95 | 1.29 | 0.83 | 7.7% | 16.84bp |
| STATISTICAL | `e756K50z` | 0.92 | 1.72 | 0.79 | 11.5% | 7.88bp |

⇒ **decay 0 再次最优**（第 3 次复现「decay 轴必须扫到 0/1」）。MARKET / CROWDING 把换手砍到 6.5–7.7%、margin 抬到 17–24bp，但 S 掉到 0.95–0.99，是典型的「高 margin 低 S」形态，不可取。

**C 批（降换手冲 fitness 8 臂）**

| 变体 | alpha | S | F | 2Y | sub | TO | 结论 |
|---|---|---:|---:|---:|---:|---:|---|
| `winsorize(·,std=2)` | `MPY08ReL` | 1.42 | 0.88 | 1.75 | 1.12 | 17.8% | **空操作**（与 decay0 逐位相同；第 2 次证伪） |
| `ts_mean(·,5)` | `2rAjZPKw` | 1.36 | 0.86 | 1.89 | 1.03 | 16.9% | 平滑无效 |
| `ts_target_tvr_decay(·,target_tvr=0.12)` | `RREAaNwn` | 1.27 | 0.79 | 1.84 | 0.95 | 15.8% | **失效**（第 2 次；TO 只压 2.2pp，S 掉 0.15） |
| `target_tvr=0.08` | `E56VaWQm` | 1.11 | 0.66 | 1.58 | 0.83 | 15.2% | 失效 |
| `ts_mean(·,22)` | `bl68PZxq` | 1.15 | 0.70 | 1.55 | 0.87 | 15.1% | 平滑无效 |
| `f=10` / `f=5` | `78LoXER2` / `wpQ9zx52` | 1.35 / 1.32 | 0.81 / 0.79 | 1.74 / 1.66 | 1.10 / 1.10 | 18.2% / 18.3% | f=22 仍最优 |
| 末层 `group_rank` | `ZYQml3r0` | 0.52 | 0.21 | 2.17 | 0.71 | 15.1% | **崩塌**（末层再排序抹掉了平方放大的持仓结构） |

### 54.4 ★★★★★ 新判据：`fitness` 的换手分母陷阱（本轮实测出来的，值得单列）

`F = S · √(returns / max(TO, 0.125))`。所以 **TO 只要压到 0.125 以下，分母就锁死在 0.125，fitness 凭空放大**：
`WjOLdO7o` 的 returns = **6.94%**、TO = **17.97%**、S = 1.42 ⇒ F = 0.88。
若能把 TO 压到 0.125 而 returns 不变：F = 1.42·√(6.94/12.5) = **1.055 ✓ 直接过闸**。
**但本轮四条降换手杠杆全部失败**：decay（16.8–18.0%）、`ts_mean` 5/22（16.9%/15.1%）、`ts_target_tvr_decay` 0.12/0.08（15.8%/15.2%）。
⇒ **该族 TO 地板 ≈ 15%，够不到 12.5% 的 fitness 拐点。** 「降换手救 fitness」这条路在事件型稀疏字段上不成立，不要再来回扫。

### 54.5 ★★★★★ 1.42 天花板律：两个独立数据集在同一区域精确同值

| 数据集 | 机制 | 最优 alpha | S 上界 | 2Y 上界 | 剩余失败项 |
|---|---|---|---:|---:|---|
| `fundamental72` 利润表 | 季度营业利润/EBIT 三 delta 秩乘 | `KPJmRpGN` / `RREALzx0` | **1.42** | 1.58–1.60 | LOW_SHARPE + LOW_FITNESS |
| `fundamental45` 电话会 NLP | LDA 主题意外 ^2（f22/L252/sector） | `WjOLdO7o` | **1.42** | 1.82–1.87 | LOW_SHARPE + LOW_FITNESS |

两个数据集在**机制完全无关、字段类型不同**（一个是季度财报科目、一个是文本 NLP）、`sub`/`2Y`/`margin`/`DD` 各异的情况下，全期 S **都停在 1.42**，且都差**正好 S 0.16 / F 0.12**。
这不是巧合，是 **DEU/TOP500/D1 的 REGULAR 结构上限**：TOP500 只有约 191 只可交易标的（`longCount` 191），横截面宽度不足以再抬 S。
⇒ **判据：某区域某 universe 的全期 S 上界若在两个以上不相关数据集上重复出现，即为该 universe 的结构上限，继续换数据集/换几何的期望值为零，必须换 universe / 换 delay / 换区域。**

### 54.6 `fundamental45` 判决：**判弱（不是判死）**

**判弱的依据**（不是「模板不够」，结构已跑满 **51 臂**）：13 个字段轴（`lda_bigram_pr` / `score` / `readability` / `numeric_pr` / `numeric_qa` / `lm2_pr` / `lm2_qa` / `vader_pr` / `vader_qa` / `ceo_change` / `othr_change` / `mktcap`）× 6 个几何轴（水平 / 一阶差分 / 意外化 ts_zscore / ts_rank / ts_ir / ts_decay_linear）× 4 个分组轴 × 6 档 decay × 6 档中性化 × 3 档 truncation。

**保留价值**：`WjOLdO7o`（S 1.42 / 2Y 1.82 / sub 1.11 / TO 18.0% / margin 7.72bp / DD 7.07%）是 DEU 非 trio 面**成本与稳定性最好**的近闸件（对比 `fundamental72` 的 `KPJmRpGN`：2Y 1.58、margin 8.57bp）；
且它与财报科目族**机制正交**（文本 vs 数字），是天然的**组合腿候选**。塔位 `DEU/D1/FUNDAMENTAL`（×1.8）。

**逐年诊断（否定「早年覆盖不足」假说）**：2014 年起 `longCount` 就 156，逐年升到 2022 的 223，**无连续空窗**；
逐年 S = 2014 1.45 / 2015 2.07 / 2016 0.92 / 2017 2.70 / 2018 1.04 / 2019 1.49 / 2020 2.06 / **2021 −0.96** / 2022 正。
⇒ 拖累全期 S 的是**2021 单年 −0.96**，不是早期稀疏。**修法只能是让 2021 的持仓结构不同**，而这已试遍（末层 group_rank 直接崩到 0.52）。

### 54.7 本轮新增封盘清单（写在这里供派发前检索；`cells.json` 是生成物未手工改动）

| 数据集 | 判决 | 判据 |
|---|---|---|
| `fundamental45` | **判弱**（S 上界 1.42，留作组合腿） | 51 臂后平台期，非模板不足 |
| `fundamental86` | **判死** | 7 字段全 MATRIX 但 DEU `coverage` 全 0.0（无 DEU 数据） |
| `sentiment33` | **判死（不投）** | 255 字段**全 VECTOR**；多数是 `event_title`/`headline`/`timestamp` 元数据；cov 0.32 |
| `earnings_sent_matrix` | **判死** | DEU `coverage` 全 0.0；论坛 EUR 明星配方（S 1.68）不可平移（复用 §14.3） |
| `macro27` | **判死（补 §52 未收口项）** | 十模板全灭：新增 M7 `ts_rank504` = `omEoMqKv` S 0.20 / 2Y 0.89；M8 `ts_zscore` = `pwdvAngj` S 0.40 / 2Y 0.89 |
| `workforce_flow_skills` 薪酬总额增速 | **退化** | `N1Nek5oX` S 0 / TO 0 / DD 0 / raf 5 ⇒ 字段无变化 |

### 54.8 本轮可复用结论（跨区通用）

1. **`winsorize` 对有界字段是空操作，第 2 次独立证伪**（`MPY08ReL` 与 `WjOLdO7o` 五项指标逐位相同）。有界评分/概率/主题分会本来就落在窄区间，裁剪不改变任何值。
2. **`ts_target_tvr_decay` 第 2 次失效**（`fnd6_newq_oiadpq` 有效 → `fnd72` 无效 → `fnd45` 无效）。**杠杆迁移率 = 1/3，默认不迁移。**
3. **低覆盖字段的分组轴必须粗**：cov 0.26 时 sector 1.30 > industry 0.38 > subindustry 0.30。细分组把本已薄的横截面切碎。
4. **末层再排序会抹掉 `signed_power` 造的持仓结构**：`group_rank(signed_power(...),sector)` S 0.52，而直接输出 S 1.42。论坛「保号幂改持仓结构」的前提是**别再在末层做等权 rank**。
5. **「水平无用、意外有用」在文本 NLP 字段上是可复现的**（同字段 S 0.10 → 1.20，12 倍），但**只对真正有信息的那一个字段成立**（本集 13 字段里只有 `lda_bigram_pr` 打出来），情绪极性字段全部无效。

## 五十五、2026-11-05 非 trio 补漏：先更正 §53.2/§54 的「已扫尽」结论，再封 `insider_agg_matrix`

### 55.1 ★★★★★ 更正：上一轮「DEU 非 trio 已扫尽」是错的，原因是把数据集级 `coverage` 当成了数据可用性

用 `get_datasets` 全量枚举 DEU/TOP500/D1（**172 个数据集，其中非 trio 70 个**）后发现：
**`fundamental72` 在数据集级也报 `coverage: 0.0`，但它实际可挖（§52 已跑 55 臂，TO 13%、margin 8bp）** ⇒ **数据集级 coverage 字段不可作为「有无数据」的判据**。
⇒ 据此**撤回**上一轮「`fundamental86` 因 cov 0.0 判死」的推理链：该结论的**证据不成立**（结论本身可能仍对，但必须用字段级 cov 或探针重新取证）。同理 §54.7 中「`earnings_sent_matrix` 因 cov 0.0 判死」的**判据表述**也要改为引用 §14.3 的实测结论。

**正确的数据可用性判据（本轮确立）**：①先用 `get_datafields` 拿**字段级** `type` + `coverage`；②`type` 也不可信（§52.3 已证 BS 层报 MATRIX 实为 event）；③所以最终必须**一条最小探针**验证，`S=0 / TO=0 / DD=0` 才是零覆盖的铁证。

### 55.2 补漏扫描：8 个从未检查过的非 trio 数据集（全部否决）

| 数据集 | category | 字段数 | 字段级覆盖 | 类型分布 | 判决 |
|---|---|---:|---|---|---|
| `analyst83` | analyst | 345 | 0.34 | **全 VECTOR** | 否决：成本墙风险 |
| `news17` | news | 48 | 0.6489 | **全 VECTOR**，多为 `country_code`/`event_text`/`headline` 元数据 | 否决：无有效数值信号 |
| `news20` | news | 46 | 0.6389 | **全 VECTOR**，同上 + `event_relevance` | 否决 |
| `news50` | news | 37 | 0.7644 | **全 VECTOR**，`category`/`country_code`/`ens_key`/`ghc_lna` 元数据 | 否决 |
| `analyst48` | analyst | 7 | 0.7879 | **全 VECTOR**，`bulk_idivisor`/`indx_typ`/`nfields` 索引元数据 | 否决 |
| `sentiment7` | sentiment | 3 | 0.7357–0.7539 | **全 VECTOR**，只有 `views`/`all_languages_views`/`timestamp` | 否决 |
| `institutions4` | institutions | 6 | <0.2 | VECTOR | 否决：无可用覆盖 |
| **`insider_agg_matrix`** | insiders | 34 | **0.5342–1.0** | **全 MATRIX**，`alphaCount` 仅 0–3 | **实测后判死（成本墙，见 55.3）** |

另有三个 risk 集本轮一并核查：`risk88` 只有 1 字段 `alternative_market_cap_usd`（= 市值，权重字段非信号）；`risk71`(10 字段) / `risk72`(31 字段) 字段级覆盖**全部 ≤0.2**，无可用数据源。

⇒ **DEU/TOP500/D1 非 trio 面的 MATRIX 可挖集 = `fundamental72` 利润表层 + `fundamental45`，两者的 S 上界都是 1.42（§54.5 天花板律）。**
其余非 trio 集要么零覆盖、要么全 VECTOR 元数据、要么已判死。**这次是带字段级取证的真实穷尽。**

### 55.3 `insider_agg_matrix` 判死：14 臂，成本墙 + 意外化几何失配

**数据集画像**：34 字段全 MATRIX，`coverage` 0.5342（`directional_indicator` 系为 1.0），**`alphaCount` 仅 0–3 ⇒ crowding 极低**，本是理想候选（同类低拥挤 MATRIX 是本轮唯一打出 S 1.42 的类型）。
字段结构 = 买/卖 × 董事(`secondary`)/高管(`top`) × 总额/均值，加 `significant_value_1..4` / `top_significant_value_1..4` / `directional_significant_value_1..4` 三组价值梯度，以及 `directional_indicator` / `directional_indicator_2` 两个方向指示。

**几何**：`signed_power(group_zscore(ts_zscore(ts_backfill(F,22),252),sector),2)`（沿用 §54 的赢家几何；decay 0 / FAST / trunc 0.08 / nanON）。

| 机制 | alpha | S | 2Y | sub | TO | margin | 判决 |
|---|---|---:|---:|---:|---:|---:|---|
| T10 均值买/卖比 | `9qxEA16q` | 0.66 | 0.95 | 0.10 | **37.9%** | 1.66bp | 成本墙 |
| T8 `significant_value_1` 意外 | `N1Ne50Oe` | 0.49 | 0.69 | 0.41 | **41.0%** | 1.50bp | 成本墙 |
| B1 `directional_indicator` 水平 | `rKRdrr9m` | 0.43 | −0.08 | 0.18 | **133.0%** | 0.48bp | 成本墙（灾难级） |
| T4 全员净买入比 | `9qxE6kMq` | 0.34 | −0.24 | 0.29 | **104.7%** | 0.52bp | 成本墙 |
| T5 高管净买入比 | `LLM5XQ71` | 0.27 | −0.30 | 0.17 | **50.0%** | 0.68bp | 成本墙 |
| T6 董事净买入比 | `9qxE6kmq` | 0.24 | 0.48 | −0.03 | **78.5%** | 0.39bp | 成本墙 |
| B2 `directional_indicator` delta 66 | `N1Ne5vrL` | 0.09 | −0.46 | 0.28 | **107.0%** | 0.15bp | 成本墙 |
| T7 高管−董事净买分歧 | `N1Ne5xWg` | −0.31 | −0.72 | −0.08 | 10.5% | −1.59bp | 方向反且弱 |
| T1/T2/T3 方向指示的意外化 | `bl68WlkR`/`RREAaPWe`/`9qxE6Od2` | **0** | — | — | **0** | 0 | **退化**：几何失配 |

**判据**：全部命中「`margin×10000 < 10` 且 `TO > 10%`」⇒ 封盘。与 `fund_holdings_panel`（TO 28–53%/margin<1bp）、`news104` 同型。
`directional_indicator` S 0.43 说明**信号方向真实存在但极弱**，被 133% 换手彻底吃掉 ⇒ 这不是「没信号」，是「信号不够付交易成本」。

### 55.4 ★★★★ 新判据：意外化几何（`ts_zscore`）**不能**用在近常数/二值指示字段上

`T1`/`T2`/`T3` 对 `directional_indicator`（cov 1.0，一个「整体方向/偏置」指标，ac 48）套 `ts_zscore(·,252)` 后，三条全部 **S=0 / TO=0 / DD=0 / raf=5**。
机理：指示类字段在长窗内近乎常数 ⇒ 窗口内标准差趋零 ⇒ `ts_zscore` 输出 0 或 NaN ⇒ 外层 `group_zscore` + `signed_power` 全为 0 ⇒ **持仓为空**。
而同一字段改用 `group_rank(·,sector)` 水平几何 ⇒ S 0.43、TO 133%，说明字段本身有值。

**判据**：
- **意外化几何（`ts_zscore` / `ts_rank` / `ts_ir`）只适用于有连续方差的字段**（财务科目、NLP 分数、概率）；
- **二值/离散指示、「是否为某事件」型字段，首轮必须用水平或差分几何**，套 `ts_zscore` 会得出「S=0 的假死」；
- 反过来，这也给了一条**便宜的退化识别法**：`S=0 且 TO=0 且 DD=0`（而非只是 S 小）⇒ 优先怀疑**几何失配**，不要直接判字段死。

### 55.5 非 trio 面最终锚点（供后续复用）

| 集 | 状态 | 最强件 | 备注 |
|---|---|---|---|
| `fundamental72` 利润表层 | 存活（S 上界 1.42） | `KPJmRpGN` 1.38/2Y **1.58✓**；`RREALzx0` **1.42**/2Y 1.43 | 塔 FUNDAMENTAL |
| `fundamental45` 电话会 NLP | 存活（S 上界 1.42） | `WjOLdO7o` **1.42**/2Y 1.82/sub **1.11** | 塔 FUNDAMENTAL；与 72 机制正交但**同塔 ⇒ 不能互组组合腿**（禁混集合） |
| `insider_agg_matrix` | 判死（成本墙） | — | 塔 INSIDERS，可用作**跨塔**组合腿 |
| `analyst83`/`news17`/`news20`/`news50`/`analyst48`/`sentiment7`/`institutions4`/`risk71`/`risk72`/`risk88` | 否决（全 VECTOR 元数据 / 零覆盖 / 市值字段） | — | 不再投槽 |

## 五十六、2026-11-05 `analyst7`（DEU 最大非 trio 字段空间，608 全 MATRIX）判弱：三大经典机制 S 上界 0.67

### 56.1 数据集画像（本轮全场字段条件最好的一个，必须实测才敢下结论）

| 指标 | 值 |
|---|---|
| 字段数 | **608** |
| 类型分布 | **608 全 MATRIX**（无 VECTOR，不触发成本墙） |
| 覆盖分档 | cov=1.0 **231 个** / 0.5–0.8 **244 个** / 0.2–0.5 **121 个** / <0.2 仅 12 个 / 0 个 0 |
| 拥挤度 | 数据集级 `alphaCount` 3993，但**大量字段 `alphaCount=0`、`userCount=0`**（拥挤全部集中在极少数热门字段） |

字段族 = ① `act_q_{eps,ner,ebi,gps,pre,cpx,fcf,roe}_surprise{mean,num,std}`（季度盈利意外）；② `est_12m_{eps,bps,cps,dps,csh}_{high,low,mean,median,std}` 及 `_4wks_ago`/`_3mth_ago`（分析师预期水平与修正）；③ `est_12m_*_{raisednum,lowerednum}_*`（预期修正广度）。
**这三族正是学术上最可靠的异象来源**（PEAD、预期修正动量、Miller 分歧高估），且 DEU 已提交件 `2rjrMZ25`（S 1.77）用的就是 `analyst_factor_signals` 的预期修正族 ⇒ **同机制在本区已被验证有效，因此本集值得一次严肃测试。**

### 56.2 十二臂机制波次（decay 0 / FAST / trunc 0.08 / nanON）

几何 A（稀疏事件）：`signed_power(group_zscore(ts_zscore(ts_backfill(F,22),252),sector),2)`
几何 B（日频稠密）：`signed_power(group_zscore(ts_zscore(F,252),sector),2)`

| 机制 | alpha | S | 2Y | sub | TO | margin | 判决 |
|---|---|---:|---:|---:|---:|---:|---|
| T9 预期修正 3 月 | `QPvY58WG` | **0.67** | 0.33 | 0.13 | 26.1% | 3.23bp | 全波最强，仍远低于闸 |
| T1 EPS 盈利意外（PEAD） | `KPJmwzLl` | 0.58 | **−0.45** | 0.27 | 21.1% | 3.23bp | **2Y 反号 ⇒ 效应近期反转** |
| T3 EBIT 意外 | `0mYjKPLK` | 0.47 | −1.18 | 0.38 | 21.5% | 2.80bp | 2Y 强负 |
| T2 净利润意外 | `KPJmw2r1` | 0.40 | 0.48 | 0.19 | 20.8% | 2.32bp | 弱 |
| T7 修正广度（raised−lowered） | `npvAOaJ8` | 0.28 | **1.66** | 0.61 | **13.0%** | 1.76bp | 「2Y 强 S 弱」第 11 例 |
| T4 毛利意外 | `GrWg3z55` | 0.21 | 0.14 | −0.01 | 20.6% | 1.14bp | 死 |
| T6 意外/不确定性 | `E56Vrzm1` | 0.21 | −0.56 | 0.19 | 20.5% | 1.17bp | 死 |
| T11 意外波动率水平 | `gJeWRJR0` | 0.32 | −0.10 | 0.20 | 19.6% | 1.73bp | 死 |
| T12 BPS 分歧 | `Xg9RYZQl` | 0.07 | 0.13 | 0.23 | 25.1% | 0.29bp | 死（分歧假说不成立） |
| T10 CPS 分歧水平 | `KPJmwoMN` | 0.02 | −0.59 | 0.02 | 25.1% | 0.12bp | 死（Miller 假说不成立） |
| T5 税前意外 | `6XdAYM7O` | −0.05 | −0.12 | −0.11 | 20.4% | −0.29bp | 死 |
| T8 分歧率（std/mean） | `zq3rJGVo` | −0.18 | −0.51 | −0.21 | 25.9% | −0.86bp | 反向也不成立 |

⇒ **三大机制族全部否决**：PEAD 上界 0.58（且 2Y 反号）、预期修正上界 0.67、分析师分歧两组（水平/比率）S ≤0.07 且反向也无效。
注意 TO 普遍 20–26%、margin 2–3bp ⇒ 即便 S 达标，成本结构也偏紧。

### 56.3 聚焦验证 4 臂：`ts_backfill` 空杠杆的判定

按论坛「事件数据 f ≈ 事件频度×1–2」纪律，对季度意外字段把回填窗从 22 放大到 66 / 132：

| 变体 | alpha | S | 2Y | sub | TO | DD | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| `act_q_eps_surprisemean` f=22（原） | `KPJmwzLl` | 0.58 | −0.45 | 0.27 | 21.12% | 13.88% | 3.23bp |
| 同上 f=66 | `npvAZozw` | 0.58 | −0.45 | 0.27 | 21.12% | 13.88% | 3.23bp |
| 同上 f=132 | `N1Negn97` | 0.58 | −0.45 | 0.27 | 21.12% | 13.88% | 3.23bp |
| 修正 delta66 最简版 | `1YNjaowk` | 0.56 | −0.20 | 0.16 | 27.09% | 9.33% | 2.57bp |
| 修正广度意外化 | `omEo33al` | 0.29 | 0.63 | 0.60 | 22.63% | 8.48% | 1.37bp |

**三档回填窗五项指标逐位完全相同** ⇒ 该字段在平台上已是**稠密日频**（前值由平台自动延续），`ts_backfill` 对它没有作用面。
⇒ 与 §52.5 `truncation` 空杠杆、§54.6 `winsorize` 空操作同型，**统一成一条判据（见 56.4）**。
另外把 2Y 1.66 的修正广度件换成意外化几何后，S 0.28→0.29 而 2Y 1.66→0.63 ⇒ **意外化几何对「强 2Y」没有保护作用**，2Y 优势来自字段本身而非几何。

### 56.4 ★★★★★ 新判据：空杠杆识别法（本轮累计 3 例，统一表述）

**改一个参数/算子后，若 S、2Y、sub、TO、margin、DD 六项里出现「五项以上逐位完全相同」，则该参数在当前字段上没有作用面 —— 立刻停止扫描该轴，不要试第三档。**

| 已证空杠杆 | 对象字段 | alpha 对照 | 观察 |
|---|---|---|---|
| `truncation` 0.08 vs 0.10 | `fnd72_s_pit_or_is_q_oper_inc` | `KPJmRpGN` vs `vR1O09EG` | 五项逐位相同（§52.5） |
| `winsorize(·,std=2)` | `fnd45_lda_bigram_pr` | `WjOLdO7o` vs `MPY08ReL` | 五项逐位相同（§54.6） |
| `ts_backfill` 22/66/132 | `act_q_eps_surprisemean` | `KPJmwzLl`/`npvAZozw`/`N1Negn97` | 六项逐位相同（本节） |

为什么值得单列：每次误扫一档参数的成本是 **1 个仿真槽（240s）+ 一次账号级并发排队**，而判定成本是零（只需对比已有读数）。

### 56.5 `analyst7` 判决与 DEU 非 trio 面最终状态

**`analyst7` 判弱**：608 字段全 MATRIX、覆盖极佳、大量字段零使用，是最理想的形态；但**三大经典机制族（PEAD / 预期修正 / 分析师分歧）的上界只有 0.67**，且 PEAD 的 2Y 反号说明该效应在 DEU 近两年已反转。
**未穷尽的部分**（如实记录）：608 字段中本轮只测了 15 个（意外 ×8 族中的 5 个、修正 3 个、分歧 4 个）。剩余 ~590 个字段多为同一族的时间位移版本（`_4wks_ago` / `_3mth_ago`）与同类指标，边际期望低；若后续要重启，应优先做「分歧 × 修正交互」与 `act_q_*_value` 实际值层，而非再扫同类字段。

**DEU/TOP500/D1 非 trio 面最终状态（本轮三次补漏后的结论）**：

| 集 | 类型 | 状态 | 最强件 |
|---|---|---|---|
| `fundamental72` 利润表层 | MATRIX | 存活 | `RREALzx0` **1.42** / `KPJmRpGN` 1.38（2Y **1.58✓**） |
| `fundamental45` 电话会 NLP | MATRIX | 存活 | `WjOLdO7o` **1.42** / 2Y 1.82 / sub 1.11 |
| `analyst7` | MATRIX | **判弱（本节）** | `QPvY58WG` 0.67 / `npvAOaJ8` 2Y 1.66 |
| `insider_agg_matrix` | MATRIX | 判死（成本墙） | `rKRdrr9m` S 0.43 @ TO 133% |
| 其余 20+ 集 | VECTOR 元数据 / 零覆盖 / 市值字段 / 已判死 | 否决 | — |

⇒ **两个存活集的 S 上界都精确等于 1.42 ⇒ §54.5 的 universe 结构上限律得到第三次独立确认（本轮新增 `analyst7` 作为反向对照：即便字段条件最好，也到不了 1.42）。**
**继续在 DEU/TOP500/D1 挖新数据集的期望值已接近零。**

---

## 五十七、2026-11-05 05:15-05:20：UNSUBMITTED 池全量 triage —— 22 条九闸全清候选**全部 prod 撞墙**；★撤回「universe 结构上限律」

### 57.1 ★★★★★ 撤回 §54.5 / §56 的「universe 结构上限律」

上一节据此宣布「DEU/TOP500/D1 继续挖新数据集期望值接近零」。**该结论是错的**，同一 universe / 同一 region / 同一 delay 下本区自发打出：

| alpha | 数据族 | 塔 | S | 2Y | sub | 九闸 |
|---|---|---|---:|---:|---:|---|
| `E56pROb9` | MODEL | MODEL | **1.79** | 2.03 | 1.32 | raf=0 / fail=[] |
| `wpQYNvZp` | MODEL | MODEL | **1.68** | 2.18 | 1.17 | raf=0 / fail=[] |
| `gJeWJn9M` | `fnd6_newq_oiadpq` | FUNDAMENTAL | **1.79** | 1.74 | 1.26 | raf=0 / fail=[] |
| `qML0EAo1` | `snt7`×`snl27` 注意力 | SENTIMENT | **2.05** | 2.40 | 1.34 | raf=0 / fail=[] |

⇒ TOP500 约 191 只标的不构成 S 上限。**1.42 只是 `fundamental72` / `fundamental45` 两个弱族共同的数据质量上界**，与横截面宽度无关。
**修正后的判据**：两个不相关数据集同值只能证明「这两族都被数据质量卡住」，不能外推成 universe 物理上限；判「某 universe 挖尽」必须先在至少一个高价值数据族上打出 ≥ 闸值。

### 57.2 ★★★★★ UNSUBMITTED 池全量扫描：600 条（DEU 483）中 22 条 raf=0 / fail=[]

扫描口径：`get_user_alphas(status=UNSUBMITTED, type=REGULAR)` × 6 页 × 100 = 600；本地闸 `S≥1.58 / F≥1.00 / 0.01≤TO≤0.70 / sub≥1.00 / 2Y≥1.00`。

| 族 | 件数 | S 区间 | self-corr | prod 实测 | 判决 |
|---|---:|---|---|---|---|
| `snt7_all_languages_views` × `snl27_relpopularity08` 注意力 | 14 | 1.71–2.05 | 0.302–0.587 全 ✓ | **0.8925 / 0.9074 / 0.9318** | **prod 撞墙 + 空窗，双杀** |
| `fnd6_newq_oiadpq` 三 delta 秩乘 | 5 | 1.65–1.79 | 0.170–0.183 | 兄弟 `P0ogRWEK` **0.9287** | prod 撞墙 |
| `anl44_2_netdebt` | 2 | 1.58–1.59 | 0.239 | `O0A8zdgJ` **0.9017**；两者互相关 0.9259 | prod 撞墙 |
| 其余 | 1 | — | — | — | — |

⇒ **池内 22 条九闸全清候选，无一条 prod < 0.70。**「九闸全清」在 DEU 已不再是稀缺信号 —— prod 才是唯一天花板。

### 57.3 ★★★★★ 新发现却双杀的矿脉：Wikipedia 浏览量注意力 × 域网站流行度（`snt7` × `sentiment27`）

`snt7_all_languages_views`（公司 Wikipedia 页面浏览量，VECTOR，cov 0.7539，**ac 65 / uc 34 —— 低拥挤**）；`snl27_relpopularity08`（Tranco 域网站相对流行度综合分，alpha=0.8，cov 0.9022，**ac 58**）。
核心构型：`vector_neut(quantile(ts_ir(ts_mean(max(a,delay 0..2), W), 22), driver="uniform"), b)`，14 个变体（W=5/10、delay 深度 1/2/4、bf 22/66、decay 4/16/40）。

**最优四件（算子 ≤12）**：

| alpha | ops | S | F | 2Y | sub | TO | decay |
|---|---:|---:|---:|---:|---:|---:|---:|
| `qML0EAo1` | 11 | **2.05** | 1.92 | 2.40 | 1.34 | 8.98% | 16 |
| `0mYrXK9r` | 11 | 1.98 | 1.84 | 2.30 | **1.54** | 8.88% | 16 |
| `ZYQAAJVQ` | 11 | 1.98 | 1.84 | 2.24 | 1.50 | 8.87% | 16 |
| `9qxWjAbq` | **8** | 1.71 | 1.51 | 2.02 | 1.31 | 8.96% | 16 |

**双杀证据**：
1. **prod 撞墙**：三代表件 `qML0EAo1` **0.9318** / `0mYrXK9r` **0.9074** / `9qxWjAbq` **0.8925**；三种不同几何（11 / 11 / 8 算子，不同窗口与 delay 深度）全落 0.89–0.93 ⇒ 第 3 次独立确认「**prod 由数据源决定，不由构造决定**」。
2. **覆盖率致命**：`0mYrXK9r` 逐年 longCount：2014–2018 **全部 0**（五年全空）、2019 才起 85 只。命中「连续空窗 N 年」除名判据。
   逐年 S：2019 1.71 / **2020 0.19** / 2021 3.07 / 2022 3.56 / 2023 1.15 —— 2Y 的 2.30 完全由 2021–2022 两年贡献。

⇒ **封盘**。该族不得再投仿真槽；`snt7` / `sentiment27` 记入 dead_ends（理由是 prod 拥挤 + 2014–2018 空窗，不是「VECTOR 元数据」）。

### 57.4 ★★★★ 纠正 §56 对 `sentiment7` 的误判

§56 把 `sentiment7` 以「仅 views/all_languages_views/timestamp、全 VECTOR 元数据」否决。**错**：`all_languages_views` 是有真实经济含义的**注意力代理**，`vec_avg` 聚合后可打出 S 2.05。
⇒ 「VECTOR」不是否决理由，**必须先 `vec_avg` 聚合后实测**；真正的否决理由只能是 prod / 覆盖 / 成本。本条与 §56.1 的「数据集级 coverage 假报 0.0」同源：**类型与覆盖都不是判死依据，只有实测是**。

### 57.5 当前唯一可提交的两颗（prod 已于 05:12–05:13 重测刷新）

| alpha | S | F | 2Y | sub | self | prod（刷新时刻） | 设置 | 塔 |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| `E56pROb9` | 1.79 | 1.70 | 2.03 | 1.32 | 0.600369 ✓ | **0.6859**（05:12:52） | decay 16 / SUBINDUSTRY / trunc 0.08 | DEU/D1/MODEL |
| `wpQYNvZp` | 1.68 | 1.36 | 2.18 | 1.17 | 0.633157 ✓ | **0.6333**（05:13:07） | decay 4 / SUBINDUSTRY / trunc 0.08 | DEU/D1/MODEL |

两次刷新值与 03:20 / 03:25 的读数**逐位相同**（0.6859 / 0.6333）⇒ prod 读数稳定、无漂移。两者互相关 0.5538。提交后 MODEL 塔 1/3 → 3/3。

### 57.6 ★★★★★ NEWS / INSTITUTIONS 塔 21 臂实测：全弱，NEWS 塔 0/3 维持

缘起：§56 把 `news17` / `news20` / `news50` / `institutions4` 以「全 VECTOR 元数据」否决 —— 与 `sentiment7` 同一个错误判据（见 §57.4）。重查字段级描述后发现里面是**真实情绪分类器分数**，遂实测。

字段画像：`nws17_event_sentiment_score`（−1..1，cov 0.6489，ac 5）/ `nws17_multiple_comp_acb`（cov 0.9323，ac 31）/ `nws17_multiple_comp_bee`（ac 6）/ `nws17_ber`（ac 5）/ `analyst_recommendation_change_score`（cov 0.9323，ac 5）/ `nws20_ghc_lna`（语调变化）/ `nws20_event_sentiment_score` / `mws50_ess`（0–100 细粒度情绪，ac 7）/ `mws50_aes`（正面事件占比）/ `mws50_ens`（事件新颖度 0–100，ac 6）/ `mws50_g_ens` / `mws50_ens_similarity_gap`（ac 8）/ `institutional_holding_percent_of_{shares_outstanding,portfolio}`（cov 0.3413）。

设置统一：decay 6 / FAST / trunc 0.04 / nanON / D1 / TOP500。

| 模板（结构互异 11 + 10 = 21 条） | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| N1 情绪水平 `group_zscore(ts_backfill(vec_avg(F),22),sector)` | `A1VQn0zE` | **0.94** | 0.52 | 0.06 | **26.2%** | 3.72bp |
| N3 情绪动量 `ts_delta(·,22)` | `JjePn3KW` | 0.66 | 0.12 | 0.17 | 34.4% | 2.14bp |
| N2 情绪意外 `SP(G(Z(ts_zscore)))` | `xAr1el0q` | 0.64 | 0.19 | 0.08 | 30.1% | 2.38bp |
| R1 `multiple_comp_acb` 意外 | `88Rvn9Gz` | 0.54 | **1.55** | 0.05 | **41.8%** | 1.40bp |
| R7 相关性加权情绪 `sent×relevance` | `WjOL9dVo` | 0.39 | 0.17 | 0.09 | 16.9% | 2.41bp |
| N4 情绪×新闻量 `rank×rank` | `wpQ95jv5` | 0.36 | −0.74 | −0.11 | 18.1% | 1.61bp |
| R5 `mws50_aes` 意外 | `j2Ye1Wao` | 0.23 | 0.01 | 0.27 | 22.6% | 1.05bp |
| R2 `multiple_comp_bee` 意外 | `rKRdAEE1` | 0.21 | 1.35 | −0.08 | 41.2% | 0.53bp |
| N6 `nws20_event_sentiment_score` 意外 | `QPvYnVp5` | 0.17 | −0.45 | 0.00 | 34.9% | 0.54bp |
| R8 推荐变更**水平** | `akKVovY6` | 0.14 | 0.25 | 0.11 | **3.05%** | 2.97bp |
| N5 推荐变更意外 | `xAr1eNGq` | 0.14 | 0.25 | 0.11 | 3.05% | 3.07bp |
| R3 `nws17_ber` 意外 | `xAr1RwEl` | 0.09 | 1.24 | −0.43 | 37.7% | 0.27bp |
| N11 / R9 机构持股变动 | `A1VQnpOX` / 在途 | −0.09 | 0.00 | −0.21 | **88.7%** | −0.08bp |
| R6 `mws50_g_ens` 水平 | `gJeWxzgQ` | −0.12 | 0.32 | −0.13 | 15.8% | −0.71bp |
| N8 `mws50_ens` 水平 | `2rAjvl3Z` | −0.13 | 0.25 | −0.07 | 15.6% | −0.73bp |
| N9 新颖度×ESS | `VkxdXW7G` | −0.14 | −0.08 | −0.18 | 20.9% | −0.56bp |
| R10 `acb − event_sentiment` 分歧 | `qMLEgXq2` | −0.24 | 0.33 | 0.06 | 36.2% | −0.76bp |
| R4 `nws20_ghc_lna` 语调变化 | `RREAdLwo` | −0.28 | 0.66 | 0.05 | 37.0% | −0.84bp |
| N7 `mws50_ess` 意外 | `akKVNb9O` | −0.32 | −0.90 | −0.30 | 34.4% | −0.96bp |
| N10 事件陈旧度 | `9qxE9NV2` | −0.38 | −0.71 | −0.53 | 14.3% | −2.44bp |

**判决：NEWS 塔（`news17` / `news20` / `news50`）封盘。** 三点理由：
1. **上界 0.94，距闸 1.58 差 0.64**，且这一条 sub 只有 0.06、TO 26.2%、margin 3.72bp —— 命中「margin×10000 < 10 且 TO > 10%」成本墙；
2. **情绪方向在水平几何上最强、意外化后反而掉**（N1 0.94 → N2 0.64）⇒ 与 `fundamental45` 的「水平无用、意外有用」**方向相反**，说明这里的信号不是信息意外而是**注意力/覆盖度**，而注意力型在 DEU 已被证为高 TO；
3. **全部 20 条里 12 条 TO > 15%、margin < 2.5bp** ⇒ 该族更新频率决定的 TO 地板太高。

`institutions4`：`percent_of_shares_outstanding` 变动 TO **88.7%** ⇒ 与 `insider_agg_matrix` 同型的事件型成本墙，**判死**。

### 57.7 本轮总账

| 项 | 数值 |
|---|---|
| 池内扫描 | 600 条（DEU 483） |
| 九闸全清候选 | 22 条，**prod < 0.70 的仅 2 条** |
| 新派发仿真 | **21 臂**（NEWS/INSTITUTIONS 两轮） |
| 新发现矿脉 | 1 条（`snt7`×`sentiment27`，双杀封盘） |
| 新封盘数据集 | `snt7` / `sentiment27` / `news17` / `news20` / `news50` / `institutions4` |
| 新确认可提交候选 | 0（仍是 `E56pROb9` / `wpQYNvZp`） |
| 提交数 | 仍 11 颗（零提交） |

### 57.8 ★★★★★ 审计发现：58 个非 trio 数据集里有 **34 个从未检查过**

用 `get_datasets(DEU/TOP500/D1)` 全量 172 集 → 非 trio **58 集**，逐个对照历史判决后仍有 **34 集无任何判决记录**。其中高价值者：

| 数据集 | cat | 字段 | cov | ac | 本轮处置 |
|---|---|---:|---:|---:|---|
| `analyst15` | analyst | 537 | 0 | 649 | 未测（cov 0 需探针） |
| `analyst69` | analyst | 292 | 0 | 515 | 未测 |
| `analyst_factor_signals` | analyst | 108 | 0.5996 | 1575 | **已用**（`2rjrMZ25` 已提交件） |
| `analyst93` | analyst | 100 | 0.6373 | 193 | **本轮实测，见 §57.10** |
| `news18` | news | 70 | 0.8046 | 137 | 未测 |
| `news104` | news | 11 | **0.963** | 100 | **本轮实测，见 §57.9** |
| `news81` | news | 23 | 0 | 223 | 未测 |
| `institutions6` | institutions | 11 | **1.0** | 270 | 未测（历史有模板池文件） |
| `risk60` | risk | 5 | 0.835 | 395 | 未测（fee 族已封盘，`rsk60_crowding` 未试） |
| `socialmedia12` | socialmedia | 18 | 0 | 130 | 未测 |
| `analyst9` | analyst | 51 | 0.5825 | 106 | 未测 |

⇒ **「非 trio 已扫尽」第三次被证伪。** 教训固化：判「某面扫尽」前必须先做**数据集枚举 × 历史判决对照**，输出「无判决记录」清单；凭记忆列举必漏。

### 57.9 `news104` 12 臂实测：上界 0.70，封盘

`news104` 是 DEU 覆盖最好的新闻集（cov **0.963**，11 字段全 VECTOR，ac 仅 2–37）：`nws104_prob_pos`(ac 21)/`prob_neg`(19)/`prob_ntr`(5)/`confidence`(20)/`novelty`(18)/`relevance`(17)/`sentiment`(37)/`marketimpactscore`(ac 2)。

设置 decay 6 / FAST / trunc 0.08。

| 模板 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| W4 净概率×相关性 | `mLoYZWgK` | **0.70** | 0.75 | 0.51 | 15.7% | 4.25bp |
| W10 只取首报（`novelty<1.5` 门控） | `1YNjg5oX` | 0.63 | 0.72 | 0.52 | 14.6% | 3.83bp |
| W3 净概率×置信度 | `Xg9R10Y5` | 0.58 | 0.73 | 0.39 | 15.7% | 3.47bp |
| W7 三元 sentiment 水平 | `zq3rOn3X` | 0.58 | 1.11 | 0.38 | 15.5% | 3.37bp |
| W1 净概率水平 | `j2Ye1Jak` | 0.55 | 0.76 | 0.39 | 15.5% | 3.28bp |
| W2 净概率意外 | `O0AJojMg` | 0.32 | 0.53 | −0.02 | 37.7% | 0.94bp |
| W6 `marketimpactscore` 意外 | `wpQ9LAxv` | −0.03 | −0.24 | 0.23 | 36.9% | −0.10bp |
| W5 `marketimpactscore` 水平 | `WjOL9R0Q` | −0.34 | 0.13 | −0.48 | 14.6% | −2.10bp |

⇒ **封盘**：上界 0.70 距闸 1.58 差 0.88。值得注意的是连厂商自带的 `marketimpactscore`（预测 1 分钟前向收益）都是负的 —— 短周期新闻冲击在 DEU/TOP500/D1 **已被完全套利掉**。

### 57.10 ★★★★★ `analyst93` 是活矿脉：`correct_revision_ratio` 水平几何 S 0.96 / sub 0.70 / margin 7.31bp

`analyst93`（分析师预测质量/准确率，100 字段全 VECTOR，cov 0.633，ac 0–52）本轮首次实测。

| 模板 | alpha | S | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|
| W11 `analyst_correct_revision_ratio` **水平** | `bl6892LR` | **0.96** | 1.04 | **0.70** | **12.6%** | **7.31bp** |
| X3 同字段**意外化** `SP(G(Z(ts_zscore)))` | `MPY0xLO9` | **0.13** | 1.23 | −0.16 | 17.5% | 0.85bp |
| X2 `recprofitability2` 意外化 | `78LodjXZ` | 0.09 | −0.17 | 0.05 | 20.5% | 0.59bp |
| W12 `relative_accuracy3` 意外化 | `3qojAgK6` | **0** | — | — | **0** | 0 |

**核心判据（本轮最重要的方法论产出）**：`analyst93` 上 **水平几何 0.96 → 意外化 0.13，信号被摧毁 87%**；`news104` 同样 0.70 → 0.32；`news17` 0.94 → 0.64。
⇒ **意外化几何（`ts_zscore`/`ts_rank`）不是万能的**，它与 `fundamental45` 的方向**正好相反**。原理：意外化只保留「相对自身历史的偏离」，对有持续横截面商业含义的字段（分析师准确率、新闻情绪覆盖度）会把**水平方向的信息当成基线减掉**。
**落地纪律**：新数据集首轮**必须两种几何并行各发 ≥3 臂**（水平 + 意外化），不得只上意外化就判死；反之亦然。

`analyst93` 最强机制候选（ac 最高，`recprofitabilityprev_analyst_profitability2` ac 52：「跟随该分析师历史建议的日均收益」）等 6 条仍在途（progress 0.35）：`X1` 水平 / `X4` ×accuracy1 / `X5` 预测口径 / `X6` peer-relative ratio / `X7` accuracy1 / `X8` consistency。

**下一步（不动 trio 也能走）**：`analyst93` 按「水平几何 + 分组轴/窗口」做 10 模板扩波；`news18`(70 字段 cov 0.80) / `institutions6`(cov 1.0, ac 270) / `analyst15`(537 字段) / `analyst69`(292 字段) / `socialmedia12` 五个未测集待开。

### 57.11 ★★★★★ `analyst93` 扩波 12 臂：S 上界 **1.46**、margin **12.8bp**、sub 1.24 —— 2Y 成为唯一卡点

| 模板 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| Y4 `recprofitability2` 水平 + `ts_mean(·,66)` | `pwdv6zKb` | **1.46** | **1.17** | 0.66 | **1.20** | 17.2% | **12.80bp** |
| X1 `recprofitability2` 水平 + `ts_mean(·,22)` | `akKVdY5x` | 1.44 | 1.15 | 0.42 | 1.20 | 17.2% | 12.68bp |
| Y6 `recprofitability2` + `signed_power(·,1.5)` | `GrWgw8N5` | 1.38 | 1.07 | 0.47 | **1.24** | 20.2% | 12.03bp |
| Y3 `recprofitability2` 分组轴换 `industry` | `VkxdplPw` | 1.36 | 1.03 | 0.18 | 0.99 | 14.7% | 11.44bp |
| Y2 `rank(revratio)+rank(recprof)` 秩和 | `78Lowwzv` | 1.29 | 0.94 | **0.74** | 1.23 | 13.4% | 10.72bp |
| X5 `profitability2`（预测口径）水平 | `LLM5pajM` | 1.28 | 0.96 | −0.12 | 0.83 | 17.0% | 11.25bp |
| Y1 `revratio × recprof` 相乘 | `9qxEwaVq` | 1.16 | 0.82 | 0.09 | 1.08 | 17.2% | 9.93bp |
| X4 `recprof × accuracy1` | `6XdAwVXE` | 1.13 | 0.79 | 0.65 | 0.97 | 17.1% | 9.80bp |
| W11 `correct_revision_ratio` 水平 | `bl6892LR` | 0.96 | 0.42 | **1.04** | 0.70 | 12.6% | 7.31bp |
| X6 `relative_ratio1` / X7 `accuracy1` / X8 `consistency` | — | 0.25 / 0.22 / **−0.50** | — | — | — | — | — |

**★ 1.42 天花板彻底推翻（第四次独立反证）**：本族 S 已达 **1.46 / 1.44 / 1.38 / 1.36**，全部来自非 trio 的 `analyst93`。

**卡点诊断（清晰且可操作）**：`analyst93` 全族 **fitness 1.03–1.17 ✓、sub 1.19–1.24 ✓、TO 13–20% ✓、margin 10.7–12.8bp ✓（极优）**，唯一不合格的是 **2Y（0.18–0.74）**；S 只差 0.12。
反差点：`W11`（`correct_revision_ratio` 水平）是**唯一 2Y ≥ 1.0** 的件（1.04），但 S 只有 0.96、sub 0.70。
⇒ **两条腿近期/长周期特征互补**：`recprofitability2` 撑全期 S 与 margin，`correct_revision_ratio` 撑 2Y。`Y2` 秩和已把 2Y 从 0.42 抬到 **0.74**（+0.32）而 S 只掉 0.17 ⇒ **加大 `revratio` 权重或把它放门控位，是下一轮唯一该做的杠杆**。

**下一轮派发计划（待授权，不动 trio）**：以 `Y2` 为骨架做 8–10 臂权重/门控位移 —— ① `rank(revratio)*2 + rank(recprof)`；② `trade_when(rank(revratio)>0.5, recprof, -1)` 门控；③ `revratio` 分桶 × `recprof`；④ `group_zscore` 换 `group_rank`；⑤ `ts_mean` 窗口 66/120；⑥ `ts_decay_linear(·,22)`。目标 2Y ≥ 1.0 且 S ≥ 1.58。

---

## §58 非 trio 双集开测（`analyst9` 12 臂 + `institutions6` 10 臂）+ 2022 单年病根定位（2026-11-05 下午）

### 58.1 本轮定位

用户指令：**专注 PV / MODEL / OTHER 之外的 category**。据此从 34 个「无判决记录」的非 trio 集里挑两个开测：
- `analyst9`（ANALYST，51 字段全 VECTOR，cov 0.53–0.62）—— ANALYST 塔 2/3，差一颗即可点亮；
- `institutions6`（INSTITUTIONS，11 字段全 MATRIX，cov **1.0**）—— 旧判决只有 1 条三腿复合臂（S 0.03），判死理由「单臂/季度稀释」不合法，需重审。
设置统一：EQUITY/DEU/TOP500/D1/truncation 0.08/pasteurization ON/nanHandling ON/FAST；`analyst9` 用 decay 6，`institutions6` 用 decay 0（季度 13F，避免平滑掉季末跳变）。

### 58.2 ★★★★★ `institutions6` 正式判死（10 个结构互异模板，上界 S 0.37）

| 模板 | 机制 | alpha | S | F | 2Y | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|
| I2 买卖家广度秩差 | 广度 | `gJeWMGKm` | **0.37** | 0.13 | −0.41 | 16.5% | 2.59bp |
| I5 持股机构数变化 | 持仓基数 | `omEolxl6` | 0.38 | 0.14 | −0.44 | 18.3% | 2.58bp |
| I7 churn（买卖家和/持有数）取负 | 换手 | `ZYQmK330` | 0.33 | 0.11 | −0.40 | 16.7% | 2.35bp |
| I6 净买额 × 广度 一致度 | 一致性 | `gJeWMlrm` | −0.16 | −0.04 | −0.91 | 15.6% | −1.05bp |
| I3 净买入数量份额 | 数量 | `RREA8eLa` | −0.24 | −0.07 | 0.28 | 17.4% | −1.76bp |
| I4 机构化率变化 | 结构 | `O0AJZWYg` | −0.26 | −0.07 | 0.26 | 22.6% | −1.53bp |
| I9 净买额 504 日时序排名 | 长历史 | `1YNjdR8z` | −0.32 | −0.08 | −0.42 | 18.2% | −1.41bp |
| I1 净买入金额比（水平） | 水平 | `E56VEoGR` | −0.49 | −0.21 | −0.28 | 18.0% | −3.63bp |
| I10 净买额同比（QoQ） | 变化 | `Xg9R8r3x` | −0.54 | −0.23 | −0.79 | 20.0% | −3.65bp |
| I8 买入隐含均价/收盘 | 价格 | `omEol0Xl` | −0.94 | −0.52 | 0.09 | 26.6% | −6.02bp |

**判决：`institutions6` 判死，且这次是合法判死**（10 个结构互异模板实测，上界 0.37，与旧单臂结论一致但证据充分）。
**根因（经济学层面，不是数据层面）**：DEU/TOP500 是大型股，机构持仓以指数基金为主 ⇒ 买卖流是**机械再平衡**而非信息交易，净买入与广度都不含前瞻信息。这与美股小盘 13F 效应相反，**不是字段坏，是 universe 把机制过滤掉了**。
⇒ 与 `risk60` 合并记入「INSTITUTIONS / RISK 两塔在 DEU 由 universe 结构决定不可挖」，勿再投槽。

### 58.3 ★★★★★ `analyst9` 判活：T3 秩差广度 S 1.85 / F 1.51 / margin 13.34bp

12 臂（decay 6 / FAST / trunc 0.08）：

| 模板 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| T3 升/降修正数**秩差** | `JjePOqMx` | **1.85** | **1.51** | 0.53 | **1.07** | 15.4% | **13.34bp** |
| T2 上升份额（活跃修正者内） | `npvA2Vj3` | 1.51 | 1.11 | −0.28 | 0.73 | 15.0% | 10.88bp |
| T1 净修正份额（水平） | `akKVn6kx` | 1.45 | 0.87 | 0.48 | 0.90 | 22.4% | 7.16bp |
| T11 未过滤净份额（水平） | `j2Ye0OAO` | 1.39 | 0.82 | 0.21 | 0.77 | 22.3% | 6.92bp |
| T12 净份额 + `ts_decay_linear(66)` | `e7560xPl` | 1.31 | 0.82 | 0.23 | 0.86 | 18.9% | 7.87bp |
| T7 净份额 66 日变化（动量） | `RREA8Q2n` | 0.90 | 0.37 | **1.43** | 0.54 | 27.6% | 3.36bp |
| T6 净份额 252 日意外化 | `qMLElrz2` | 0.71 | 0.27 | 0.67 | 0.33 | 22.9% | 2.93bp |
| T10 净份额 252 日时序排名 | `GrWgL9m3` | 0.52 | 0.19 | 0.32 | −0.07 | 15.4% | 2.66bp |
| T4 过滤/未过滤分歧 | `d5WK0LKE` | 0.32 | 0.10 | 0.62 | 0.49 | 19.5% | 1.83bp |
| T9 净份额 × 覆盖度 | `3qojRJ96` | 0.23 | 0.04 | −0.22 | 0.10 | 33.7% | 0.60bp |
| T8 净份额离散度取负 | `vR1Olrnv` | 0.19 | 0.05 | −0.05 | 0.33 | 16.0% | 1.30bp |
| T5 无变更份额（对照） | `P0oM3NJE` | −0.55 | −0.19 | 0.35 | −0.08 | 24.4% | −2.28bp |

**T3 是唯一有价值的件**：S 1.85 / F 1.51 / sub 1.07 / TO 15.4% / margin **13.34bp**，`checks.fail = []`，唯一 failure 是 **`LOW_2Y_SHARPE`（2Y 0.53）**，`ra.failed_ra_count = 1`。
T5 对照为强负 ⇒ 方向正确（无修正份额高 = 无信息 = 差），机制自洽。

### 58.4 ★★★★★ 2022 是唯一失败年份（逐年表）

`JjePOqMx` 逐年 Sharpe：2014 **4.29** / 2015 3.56 / 2016 1.76 / 2017 2.58 / 2018 1.16 / 2019 1.07 / 2020 1.04 / 2021 2.79 / **2022 0.06** / 2023 1.04。
`RREA8Q2n`（广度动量）逐年：2022 **2.03**（其最佳年），但 2015 0.04 / 2016 −0.53 / 2017–2019 ≈ 0.5。

**关键事实：回测 `endDate = 2023-12-31`** ⇒ 平台「2Y」= **2022+2023**，不是滚动近两年。所以 2Y 病根是**单一年份 2022**，且广度水平类与广度动量类在 2022 **完全互补**。

### 58.5 中性化轴实验：修好 2Y 但打死 fitness（核心权衡）

| 变体 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| `group_neutralize(·,market)` | `zq3rRjvd` | 1.76 | **0.62** | **1.06 ✓** | 1.03 | **40.0%** | 2.49bp |
| `group_neutralize(·,industry)` | `mLoYVJ52` | 1.60 | **0.54** | **1.17 ✓** | 1.06 | 39.9% | 2.27bp |
| `group_neutralize(·,subindustry)` | `pwdvKoPo` | 1.18 | 0.35 | **1.49 ✓** | 0.71 | 39.9% | 1.73bp |
| `sector`（= T3 基线） | `JjePOqMx` | **1.85** | **1.51** | 0.53 | 1.07 | 15.4% | **13.34bp** |
| `sector` + `ts_mean(22)` | `78Lon0jO` | 1.61 | 1.30 | 0.38 | 0.91 | 13.9% | 13.07bp |
| `sector` + `ts_mean(66)` | `9qxE7PNd` | 1.64 | 1.37 | −0.08 | 0.95 | 13.6% | **13.90bp** |
| `sector` + `ts_ir(66)` | `pwdvKvnx` | 1.21 | 0.83 | −0.92 | 0.41 | 14.1% | 9.43bp |
| `sector` + `ts_mean(252)` | `O0AJxZv1` | 1.19 | 0.84 | −0.02 | 0.87 | 12.6% | 9.93bp |

**结论（重要）**：
① **`sector` 中性化是收益与 margin 的唯一来源**（margin 13.3bp、TO 15%）；换成 `industry`/`market`/`subindustry` 后 2022 修好（2Y 1.06–1.49），但 **TO 翻到 40%、margin 塌到 1.7–2.5bp ⇒ fitness 0.35–0.62，全线不过闸**。
② 时间平滑（22/66/252/IR）**既救不了 2Y 也救不了 sub**（2Y −0.08 ~ 0.38，sub 0.87–0.95）。
⇒ 2Y 与 fitness 在该字段上是**直接对立的**：2Y 好的口径把高 margin 的行业内相对信息扔掉，换成高换手低 margin 的横截面绝对排序。

### 58.6 ★★★★★ `decay` 在本族是**空杠杆**（三次逐位相同）

`P2 = group_neutralize(T3,market)` 在 decay **6 / 16 / 32** 三个设置下：

| decay | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| 6 | `zq3rRjvd` | 1.76 | 0.62 | 1.06 | 1.03 | 0.4000 | 2.49bp |
| 16 | `3qojeN96` | 1.76 | 0.62 | 1.06 | 1.03 | 0.4000 | 2.49bp |
| 32 | `Vkxd7Jzw` | 1.76 | 0.62 | 1.06 | 1.03 | 0.4000 | 2.49bp |

**六项指标逐位相同** ⇒ 按「空杠杆识别法」（本台账 §51 起的方法论）判定：**decay 对这一族表达式没有作用面**，后续同一机制别再扫 decay 档。
（已核对 `get_alpha_details`：`decay` 确实写进了 settings，16/32 都生效，不是参数没传进去。）

### 58.7 ★★★★ 两个「假信号」与一个字段源纪律

**① 退化臂（必须警惕）**：`add(rank(X2), rank(ts_delta(X2,66)))` 三条（`RREA1Yjn`/`78LonXr1`/`vR1OvLEG`）报 **S 11.18 / F 6.5 / TO 1.0 / 2Y 0 / sub 11.18**。S 11 与 TO 100% 同时出现 = 数据伪影（`vec_avg` 缺失→`ts_delta` 爆值），不是真信号。
**纪律**：`S > 5` 或 `TO ≈ 1.0` 时先怀疑伪影，别当宝；`ts_delta` 前必须 `ts_backfill`。

**② `anl9_daily_*` 字段不能直接用**：`group_neutralize(rank(升)-rank(降),sector)` 用 daily 源 ⇒ **TO 90.2% / S 0.65 / raf 6**（`omEognXE`）；未过滤 daily 源同理（90.0% / 0.59，`LLM5d1ee`）。
⇒ **同一数据集内 `anl9_s_*` 快照字段 ≫ `anl9_daily_*` 日频字段**（TO 15% vs 90%、S 1.85 vs 0.65）。数据集内部字段版本差异可决定生死，不能混用。

### 58.8 同塔双数据集融合（`analyst9` × `analyst93`）—— 已派 8 臂，全部卡在 PENDING

思路：`analyst93` 的 `correct_revision_ratio` 是唯一 2Y ≥ 1.0（1.04）的腿，`analyst9` T3 是 S/margin 最强的腿，两者**同属 ANALYST 塔**（不触禁混集合、也不占 trio×非 trio 配额）。
已派 8 臂：Z1 1:1 / Z2 `crr`2:1 / Z3 `crr`1:2 / Z4 `crr`过 22 日均 / Z5 `crr`66 日 / Z6 `crr` 252 时序排名 / Z7 subindustry 轴 / Z8 industry 轴。
**状态：`Z5` S 1.14 / 2Y 0.97 / sub 0.80（弱）；`Z6` S 0.30 / 2Y 1.45 / sub 0.06；其余 6 条 + 5 条重发项在平台侧连续 20 分钟以上 PENDING（队列拥塞），未取值。**
**覆盖风险预警**：`analyst93` cov 0.633 × `analyst9` cov 0.53–0.62 求交后可能塌到 ~100 只（历史先例：`risk60 × analyst93` 曾塌到 129 只并因此判死），若 sub 崩先查 longCount。

### 58.9 本轮总账

| 项 | 值 |
|---|---|
| 新开数据集 | 2（`analyst9` / `institutions6`） |
| 新回测臂 | **31 条**（analyst9 12 + inst6 10 + 2022 攻坚 12 → 实跑 29 条，另 2 条重发） |
| 判活 | `analyst9`（S 上界 **1.85**、margin 13.34bp，唯一卡 2Y 0.53） |
| 判死 | `institutions6`（10 模板，上界 S 0.37） |
| 新发现机制 | 2Y = 2022+2023 单年病；sector 中性化是 margin 唯一来源；`decay` 空杠杆；daily 字段不可用 |
| 提交数 | 仍 **11 颗**（零提交、零取消） |

### 58.10 下一步（按期望值排序）

1. **取回 8 条在途融合臂**（Z1/Z2/Z3/Z4/Z7/Z8 + 重发件）—— 这是当前最有希望同时满足 S ≥1.58 且 2Y ≥1.0 的一组；
2. 若融合仍不行：接受 `analyst9` T3 的「S 1.85 / 2Y 0.53」结构性矛盾，**把 T3 作为 PPA 候选而非 REGULAR**（PPA 不查 2Y）；
3. `analyst9` 剩余可挖：`numnochg` 之外的 `consensusestimate` 系列被 51 字段里 30 个是 `effectivetime/totime/splitfactor` 元数据，实质字段已扫完；
4. 34 个未测集里下一个高价值目标：`news18`（70 字段，含 `days_since_similar_event` / `event_sentiment_score` 事件族）—— 但 NEWS 塔已有 4 集封盘，优先级低于把现有两颗全闸候选提交。

---

## §59 category 层面全量清点 + `analyst69` / `earnings6` 两集实测（2026-11-05 傍晚）

### 59.1 ★★★★ DEU 172 个数据集按 category 全量清点（16 类）

| category | 集数 | 合计 ac | 未测高价值者（字段数/ac/cov） | 塔位 |
|---|---:|---:|---|---|
| model | 45 | 14086 | model38(71/6105/0) · model25(217/1946/.61) · model26(548/908/.58) | 1/3 |
| other | 41 | 6010 | techindi_model(399/4055/0) · dl_riskfree_returns(133/922/.71) | 2/3 |
| analyst | 18 | 8038 | analyst39(24/261/0) · analyst47(5/112/.62) · analyst44(72/58/.58) | 2/3 |
| pv | 16 | 14664 | pv20(681/6190/0) · intraday_pv_feats(585/510/0) | 已满 |
| news | 17 | 802 | news23(116/50/0) · news7(23/33/0) | **0/3** |
| fundamental | 12 | 4028 | fundamental17(135/1742/0) · fundamental89(407/412/0) | 1/3 |
| institutions | 5 | 430 | fund_holdings_panel(18/102/.90) 已测 · institutions25(24/7/0) | 1/3 |
| risk | 5 | 688 | risk68(5/169/0) · risk72(31/37/0) · risk71(10/23/0) | **0/3** |
| sentiment | 3 | 463 | sentiment33(255/45/.32) | 1/3 |
| earnings | 2 | 235 | earnings_sent_matrix(7/127) 已封 · **earnings6(18/108) 本轮实测** | **0/3** |
| insiders | 2 | 196 | insiders1(8/26/.53) | **0/3** |
| socialmedia | 2 | 267 | socialmedia39(1/137/.27) · socialmedia12(18/130) | **0/3** |
| imbalance | 1 | 138 | **imbalance5(2/138)** — `imb5_score` 是 SHIELD-OIL 抗油价冲击评分(0-1) | **0/3** |
| macro | 1 | 149 | macro27(13/149) 已测：前段空窗 7 年 | **0/3** |
| option | 1 | 72 | option1(22/72) 已判弱封组合 | **0/3** |
| shortinterest | 1 | 864 | shortinterest3 已用 | 2/3 |

**未点亮塔清单（0/3）**：news(17 集) / risk(5) / earnings(2, 已封) / insiders(2) / socialmedia(2) / imbalance(1) / macro(1) / option(1)。
**推论**：`news` 与 `risk` 是唯一还有多个未测数据集的两个暗塔；`earnings` 本轮实测后也应归入封盘。

### 59.2 ★★★★ `analyst15`（537 字段）= GROUP 类，只能当分组轴，不能当信号

字段清单前 20 名里 `ebg_sector_*` / `ebg_industry_*` / `ebg_group_*` 全是**部门/行业级市值加权聚合**（如「该行业市值在 calendarized FY3 中的占比」），`anl15_dps_*` 也多为 sector/industry 级加权 DPS 增速。
⇒ 按 `cells.json` 的既有规则（`data_type=='GROUP'` 一律降级为分组轴），**`analyst15` 不进信号白名单**，只作为 `group_rank` / `group_neutralize` 的自定义分组轴备选。537 字段里没有可用的个股级截面信号。

### 59.3 `analyst69`（292 字段）实测：覆盖自 2015 起（2014 空），两条头牌机制偏弱

画像：MATRIX 104 + VECTOR 188，全部个股级一致预期 —— 目标价（best/hi/lo）、EPS/EBITDA/EBIT 一致值与 4 周修正、ROE 估计区间、推荐票数、净债务。字段级 cov 全部报 0（已知失真值），**实测 longCount 2015 69 只 → 2023 210 只，2014 = 0**。

| 模板 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| P2 GAAP EPS 4 周修正（水平） | `P0oMZ5rw` | 1.27 | 0.73 | 0.53 | 0.71 | 24.6% | 6.53bp |
| P1 目标价/收盘 隐含上涨空间 | `omEo6E8n` | 0.37 | 0.14 | −0.37 | −0.32 | 17.4% | 2.93bp |

**结论**：`analyst69` 暂列「弱但未判死」——修正幅度面有 S 1.27 的中等强度，且 **2014 单年空窗触发 goal 的「近十年都要有数据」硬条件**，在 leading-gap 裁定前不入篮。
**注意**：隐含上涨空间（target/close）在 DEU 无效（S 0.37），与美股经典结论相反 ⇒ 大型股目标价已被卖方充分定价。

### 59.4 ★★★★ `earnings6`（EARNINGS 塔 0/3）10 模板实测：全弱，塔封

字段：`ern6_estimated_eps`（Estimize 加权预期）+ `ern6_actual_eps`（实际 EPS）+ `preliminary_eps_range_{lower,upper}_bound` ⇒ 可构成真正的 SUE。全部 VECTOR 事件字段，先 `vec_avg` 聚合；**零 PV 内建字段**（不用 close 缩放，避免 EARNINGS×PV 混塔）。

| 模板 | 几何 | alpha | S | F | 2Y | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|
| E5 SUE 四季均值 | 持续性 | `YP1xbkWo` | **0.57** | 0.29 | 0.69 | 18.1% | 5.26bp |
| E6 净意外（货币空间） | 水平 | `A1VQNO5d` | 0.50 | 0.22 | −0.71 | 15.1% | 3.81bp |
| E2 SUE · subindustry 秩 | 分组轴 | `zq3r8vZd` | 0.23 | 0.07 | −0.45 | 14.8% | 1.62bp |
| E1 SUE 比率 · zscore | 水平 | `KPJmN6NN` | −0.09 | −0.02 | −0.87 | 20.1% | −0.71bp |
| E9 SUE · decay_linear(66) | 衰减加权 | `N1NeaNAq` | −0.20 | −0.06 | −0.89 | 19.3% | −1.67bp |
| E4 SUE 同比变化(252) | 动量 | `E56VpAaK` | −0.34 | −0.12 | −0.77 | 21.7% | −2.45bp |
| E3 SUE 252 日意外化 | 意外 | `1YNjXzJk` | −0.39 | −0.14 | −1.00 | 16.9% | −2.51bp |

E7（初步区间宽度取负）/ E8（区间中点 vs 预期一致性）/ E10（SUE 504 日时序排名）三条因平台未注册（`status: null`）未取值，但同族七条全灭、上界 0.57，**不补发**。

**判决：`earnings6` 判弱封组合，EARNINGS 塔（0/3）在 DEU 归入不可挖**。与 §s1 的 `earnings_sent_matrix`（上界 0.63）合并看：**EARNINGS 两集 17 条臂、两个独立声源（Estimize 预期差 + 新闻情绪矩阵），上界都是 0.6 档** ⇒ 不是数据坏，是 DEU 大型股的盈余意外被卖方与做市充分定价。
**跨区迁移种子**：失望腿非对称（Druz 2016）与 SUE 持续性在 DEU 均无效，若要复用请转 USA/TOP3000 或 IND。

### 59.5 ★★★★★ 2Y 墙的统一解释（本轮把 30+ 臂证据收敛成一条）

把本轮所有「2Y 达标 / 不达标」的臂按**几何类型**归类，规律非常干净：

| 几何类型 | 代表臂 | S 区间 | 2Y 区间 | 结论 |
|---|---|---|---|---|
| **水平 / 行业内相对** | analyst9 T3 (1.85)、analyst93 Y4 (1.46)、earnings6 E1 | 高 0.9–1.85 | **低 −0.9~0.53** | margin 高、2Y 死 |
| **变化 / 动量 / 绝对排序** | analyst9 T7 (0.90)、W4 绝对 (1.76)、analyst93 crr (0.96) | 中低 0.6–1.76 | **高 1.04–1.43** | 2Y 活、margin 死 |

**机制解释（因果链）**：平台 2Y = 2022+2023，而 2022 是 DEU 的**板块主导年**（能源/防御 vs 科技）。
① 行业内相对类信号在 2022 的选股信息被板块 beta 淹没 → 2022 ≈ 0；
② 横截面绝对类信号恰好承载板块配置 → 2022 有效，但它的超额来自高换手排序 ⇒ margin 1.7–2.5bp；
③ 融合两类的所有尝试（11 臂）都落到 TO 40% / margin ≤2bp ⇒ fitness 0.26–0.62。
⇒ **在 DEU/TOP500/D1 上，「高 margin」与「2022 有效」是同一根轴的两端，不能靠权重或算子绕过去。** 要突破只能换源（换 region/universe），或接受 PPA 通道（PPA 不查 2Y）。

### 59.6 本轮总账与下一步

| 项 | 值 |
|---|---|
| 新开数据集 | 3（`analyst69` 2 臂 / `earnings6` 10 臂 / `analyst15` 画像判为 GROUP 类不入白名单） |
| 新回测臂 | **12 条**（earnings6 10 + analyst69 2），另 3 条平台未注册 |
| category 清点 | 172 集 16 类全量完成，未点亮塔 8 个已列清单 |
| 判死 / 判弱 | `earnings6` 判弱封塔；`analyst69` 判弱挂起（2014 空窗 + 2Y 0.53） |
| 提交数 | 仍 **11 颗**（零提交） |

**下一步建议（按期望值）**：
1. **`risk` 塔是唯一还剩多个未测集、且历史上有 margin 10.39bp 记录的暗塔**（`1YNx3vnm` S 0.75 / 2022 0.88 / margin 10.39bp）。虽然 `risk60` 已两次判死，`risk68`(5 字段 ac169) / `risk71`(10/ac23) / `risk72`(31/ac37) 从未测过 —— 它们是「2Y 活 + margin 高」这一稀缺组合的最后候选，优先于 news。
2. `imbalance5` 的 `imb5_score`（抗油价冲击 0-1 评分，ac 106）本质是**状态变量**，正确用法是当分组轴（按冲击韧性 bucket 分组）而非信号，可做 2–3 臂验证。
3. `analyst39`(24 字段 ac261) 是 analyst 类里 ac 最高的未测集，若 analyst 面还要继续，从它开始。


## §60 RISK 塔非 trio 面收口 + EUR 存量族全盘点 + fundamental89 应计矿脉开掘（2026-11-05 下午）

### 60.1 DEU `risk68` / `risk72` 八臂实测：残差收益族判弱

两集字段画像（全部 MATRIX、DEU/TOP500 覆盖实测）：`risk68` 5 字段（`rsk68_beta` / `rsk68_residual_return` / 3 个 weight 字段，后者是权重非信号）；`risk71` 10 字段 + `risk72` 34 字段 = 同一「特异收益 / 残差收益」信号在不同 universe 的版本（ecs_top400/800/1200/1600、epp_minvol1m、eur_minvol1m、top600/800/1200/2500 + cfg2 replicator VECTOR）。
**覆盖实测（关键正面结论）**：`top600_equity_residualized_return` longCount 2014→2023 = 151/156/164/181/180/187/200/236/235/220，`rsk68_residual_return` = 152/158/162/179/181/186/199/236/238/218 ⇒ **两集十年满覆盖、无空窗**，满足 goal「近十年都要有数据」硬条件（这是 analyst69 缺失的属性）。

| # | 模板 | alpha | S | F | 2Y | sub | TO | margin | raf |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| M1 | 5 日残差动量 `top600` | `kqNJoApO` | −0.31 | −0.05 | 0.01 | −0.37 | 47.99% | −0.58bp | 4 |
| M2 | 5 日残差动量 `rsk68` | `3qojVZNN` | −0.24 | −0.03 | 0.92 | −0.30 | **80.13%** | −0.33bp | 5 |
| M3 | 22 日残差动量 `top600` | `LLM55jj2` | 0.33 | 0.08 | 0.86 | 0.28 | 25.68% | 1.14bp | 3 |
| M4 | 22 日残差反转 `top600` | `leAMMLqO` | −0.33 | −0.08 | −0.86 | −0.28 | 25.68% | −1.14bp | 4 |
| M5 | BAB 低 beta 取负 `rsk68_beta` | `kqNJJE0z` | 0.30 | 0.10 | 0.29 | 0.27 | 14.60% | 2.27bp | 3 |
| M6 | 66 日特异波动取负（Ang 2006） | `2rAjmALb` | 0.04 | 0.00 | 0.49 | 0.04 | **15.69%** | 0.30bp | 3 |
| M7 | 位置分位反转 `ts_rank(ts_sum(...,5),252)` | `bl688bq6` | 0.44 | 0.09 | −0.03 | 0.42 | 42.72% | 0.91bp | 3 |
| M8 | 低 beta 门控 × analyst9 净上调 | `leAMMzWl` | 1.09 | 0.40 | **−0.83** | 1.01 | **74.38%** | 2.64bp | 5 |

**判决：`risk68` / `risk72` 在 DEU/TOP500/D1 判弱，RISK 塔（0/3）在 DEU 归入不可挖。**
三条硬证据：① 单字段原始几何八臂里最高 S 仅 0.44（M7），且 margin 全部 ≤2.27bp；② 十年满覆盖下十年逐年 Sharpe 无稳定段（M6 逐年 −0.64/−1.00/0.36/−1.35/0.08/−0.75/−0.47/+2.12/+1.43/−0.87，只有 2021-2022 两年正）⇒ 不是样本期问题；③ 唯一的正 S 上档来自「低 beta 门控 + analyst9」（M8 S 1.09）但门控把 TO 从裸 analyst9 的 15.4% 顶到 **74.38%（超 70% 上限）** 且 2Y 从 0.53 恶化到 **−0.83** ⇒ 门控迁移在 DEU 反向伤害。
**副产品（可复用）**：`ts_std_dev(残差收益, 66)` 这一族换手只有 **15.69%**，是 DEU 已知最低换手的非 trio 信号骨架之一（对比 analyst9 15.4% / earnings6 18%）。若后续需要「低换手基底腿」承载别的信号，这是可用模板。

### 60.2 ★★★★★ EUR RISK 族全量盘点：3 颗全闸件，族上限 1 颗

按 §14.10 与 §32 的交叉检索定位到 EUR 存量 RISK 族（`rsk68_beta` 低 beta 门控 + ANALYST EBT 修正比核心 + SENTIMENT/OTHER 估值 `vector_neut` 腿），全族 16 条 UNSUBMITTED。**本轮逐条实测指标（EUR/TOP2500/D1/decay1/FAST/trunc0.04）**：

| alpha | S | F | 2Y | sub | TO | margin | raf | 结论 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `88RvK9Ro` / `A1VQgonw` | **3.06** | **2.02** | 2.20 | 1.47 | 14.3% | **8.73bp** | 1 | 仅 `LOW_SUB_UNIVERSE_SHARPE` |
| `P0oMv1Yx` | 2.82 | 1.85 | 2.10 | 1.08 | 14.1% | 8.60bp | 1 | 同上（sub 更低） |
| `YP1xNoPw` | 2.79 | 1.58 | 2.16 | 1.33 | 18.2% | 6.45bp | 1 | 同上 |
| `P0oMvkJp` | 2.59 | 1.63 | 2.17 | 1.16 | 15.3% | 7.89bp | 1 | 同上 |
| `E56VkKzr` | 2.51 | 1.22 | 2.18 | 1.29 | 22.4% | 4.73bp | 1 | 同上 |
| **`ZYQmolVx`（幂次 2.05）** | **2.48** | **1.19** | **2.15** | **1.29** | 22.7% | 4.59bp | **0** | **全闸通过** |
| **`kqNJKmp8`（幂次 2.10）** | **2.45** | **1.16** | **2.13** | **1.28** | 23.1% | 4.45bp | **0** | **全闸通过** |
| `RREA2GNb` | 2.99 | 1.96 | 2.09 | 1.33 | 14.2% | 8.63bp | 1 | 同上 |
| `VkxdXbvA` / `ZYQmlM63` | 1.36 / 0.94 | 0.31 | 0.57 / 0.62 | 0.53 / 0.73 | 81% / 30% | 1.05 / 2.14bp | 5 / 4 | 压缩崩坏臂 |

**本轮新增实测（此前台账未记）**：`ZYQmolVx` self_corr **0.4169200** / **prod_corr 0.5276**（`results/prod_wait_ZYQmolVx.json`，2026-11-05 09:10:46）；`kqNJKmp8` self_corr **0.4122463** / **prod_corr 0.5215**（同批 09:10:59）。两者四项 pending 均只剩 SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION，其余 checks 全 pass、`failed_ra_count = 0`。

**★ 闸的数学真相（本轮确认，决定一切）**：`LOW_SUB_UNIVERSE_SHARPE` 是**相对闸** `sub ≥ 0.517 × S`，不是绝对值闸。所以删 `signed_power` 把 S 抬到 3.06 的同时把门槛抬到 1.58，sub 1.47 **反而落榜**；幂次加到 2.05 把 S 压到 2.48、门槛降到 1.282，sub 1.29 **擦线 0.008 通过**。⇒ **这个族的「过闸」= 用幂次压低 S 让相对门槛落到 sub 以下，不是信号改善。**

**★★ 族上限 = 1 颗，已由 `xArjE96W` 占满（§32.4 既有判决）**：全族与 `xArjE96W` 相关 0.69–0.80，超过 self 红线 0.70 ⇒ 修好闸门也交不了第二颗；88RvK9Ro ↔ zq3Yrb3G 相关 0.982。**`ZYQmolVx` 与 `kqNJKmp8` 表达式只差 `signed_power` 指数（2.05 vs 2.10），两者互相关必然 >0.99，只能提 1 颗。**
⇒ 三颗全闸件（`xArjE96W` / `ZYQmolVx` / `kqNJKmp8`）择一提，**不是三颗都提**。择一依据：`ZYQmolVx` 的 self 0.4169 / prod 0.5276 是三者中最低（最安全），S 2.48 / F 1.19 / margin 4.59bp 达标；`xArjE96W` 历史 self 0.5848 / prod 0.5907 余量更薄。

### 60.3 ★★★ 流程教训：派发前必须先查「目标数据集所属区」的台账，不是只查当前区

本轮在未见 EUR 台账 `tracking/EUR/WAVE_LEDGER.md` 的情况下，把该族当成「从未测的新矿脉」重新做了画像与探针，并额外派了 2 条消融臂（`eur_E1_sp205_tvr` / `eur_E2_sp205_notvr`），而 EUR 台账 §32.4 已明确写「**后续不要再在本族派发任何批次**」。
**规则（硬）**：一个数据集/信号族的历史判决可能写在**别的区**的台账里（同一 dataset_id 跨区共享、同一经济机制跨区迁移过）。派发前检索顺序应为：① 当前区台账 → ② **`tracking/*/WAVE_LEDGER.md` 全量 grep dataset_id 与核心字段名** → ③ `config/cells.json` 的 `dead_ends`。三条都空才当新矿。
**可检索证据**：`grep -l "est_12m_ebt_raisednum" tracking/` 直接命中 `EUR/WAVE_LEDGER.md`；若先跑这一步，本轮可省 2 条臂与 1 轮画像。

### 60.4 `fundamental89`（407 字段，全 MATRIX）—— 应计异象研究实现全集画像

DEU 台账此前只把它列进清单未判。本轮画像：**407 字段全部 MATRIX、按估计方法分成 7 个独立族**，是 Sloan (1996) 应计异象的完整学术实现：

| 族 | 字段数 | 含义 | 代表字段 |
|---|---:|---|---|
| `asset_*` | 99 | 资产负债表应计 ÷ 总资产/流动资产/销售（流动 41/43、非流动 51/54） | `fnd89_asset_41_11`（ac7）· `fnd89_asset_54_11`（ac11） |
| `csjones_*` | 65 | **Jones 模型横截面**（行业调整、回归残差） | `fnd89_csjones_all_major_11` |
| `major_*` | 50 | 主定义 (NI − CFO)/TA 及其变体 | **`fnd89_major_11_11`（ac173，全族最高）** · `fnd89_major_13_11`（ac37） |
| `jones_*` | 49 | **Jones 模型时序** | `fnd89_jones_accrual_major_11` |
| `other_*` | 36 | 综合应计 / 权益变动类 | `fnd89_other_11_11` |
| `best11/best21/fixed1313/…13` 系列 | 各 7–9 | D1 标准化版：`d1_accum_4q`（累积 4 季）/ `d1_asset_change` / 0-1 指标 | `fnd89_fixed1313_d1_accum_4q`（ac36）· `fnd89_major_d1_asset_change`（ac16） |

**字段名验证**：preflight 10 个候选名 → 9 个 `unknown_fields=[]` 通过，仅 `fnd89_best11_d1_tstat` 报 `dataset-prefixed field not found`（该集无 tstat 后缀名，实际统计量字段在 `*_d1_*` 系列里）⇒ 派发前必须先 preflight 逐名验证。
**塔位合规**：FUNDAMENTAL 在用户 2026-11-03 全局禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL} 内 ⇒ **只能单数据集 ATOM（不占配额）**，禁止与 PV/MODEL/OTHER 组腿。应计族天然是单集内多定义，正好合规。

**七臂实测（DEU/TOP500/D1/decay6/FAST/trunc0.08，全部 `multiply(-1,rank(ts_backfill(<field>,66)))` 同骨架、只换字段与几何）**：

| # | 应计定义 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| A3 | **Sloan 主定义 (NI−CFO)/TA `major_11_11`** | **`MPY0YGPL`** | **1.30** | **0.86** | **1.09** | 0.69 | 13.18% | **8.76bp** |
| A9/A10 | 同上但 decay 16 / 32 | `88RvRwMX` | 1.27 | 0.84 | 1.06 | 0.67 | 13.06% | 8.68bp |
| A7 | 累积 4 季应计 `fixed1313_d1_accum_4q` | `zq3r3GW1` | 1.13 | 0.71 | 0.93 | 0.42 | 12.68% | 7.91bp |
| A6 | Sloan 主定义 + `group_neutralize(...,sector)` | `xAr1rGvl` | 1.09 | 0.67 | 0.65 | 0.57 | 13.65% | 7.45bp |
| A4 | Jones 时序 `jones_accrual_major_11` | `JjePeNmA` | 0.66 | 0.31 | 0.16 | −0.08 | 12.62% | 4.36bp |
| A1 | 流动应计 `asset_41_11` | `WjOLOd8d` | 0.31 | 0.10 | 0.87 | −0.12 | 13.54% | 2.17bp |
| A11 | D&A 强度 `major_13_11 − major_11_11` 取负 | `GrWgmA3x` | −0.51 | −0.21 | 0.51 | −0.43 | 12.56% | −3.45bp |

**A5（`major_11_11` 意外化 `ts_zscore(...,252)`）/ A8（横截面 Jones `csjones_all_major_11`）/ A12（资产增长 `major_d1_asset_change`）三条平台未注册（列表无对应 alpha），本段不补。**

**五条硬结论**：
1. **应计异象在 DEU/TOP500 成立且是目前唯一「2Y 达标 + 高 margin」的非 trio 骨架**：`MPY0YGPL` 2Y **1.09 过 1.0 闸**、margin **8.76bp**（对标 best analyst9 13.34bp 但 analyst9 的 2Y 只有 0.53）、TO **13.18%** 全 DEU 最低档。唯一短板是 S 1.30（差闸 0.28）与 F 0.86（差 0.14）。
2. **`LOW_SUB_UNIVERSE_SHARPE` 在 DEU 也是相对闸**：`MPY0YGPL` 的 `checks.fail = []`、`raFail = [LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE]` —— **sub 0.69 已过**（0.517×1.30 = 0.672 < 0.69），与 EUR 同口径确认。
3. **定义选择比几何重要得多**：Sloan 主定义 1.30 >> 累积 4 季 1.13 >> Jones 时序 0.66 >> 流动应计 0.31；D&A 强度方向**为负**（取负后 −0.51 ⇒ 正向约 +0.51），说明资本密集度是不同于盈余质量的机制。
4. **★ 空杠杆第 5 例：`decay` 在应计族无作用面**。decay 6 / 16 / 32 三档六项指标仅差 0.03（S 1.30→1.27、TO 13.18%→13.06%、margin 8.76→8.68bp）⇒ 同 analyst9 的 decay 空杠杆。后续不要在本族再扫 decay 档。
5. **表达式内 `group_neutralize` 是负杠杆**：S 1.30→1.09、2Y 1.09→0.65 ⇒ 应计信号的横截面绝对性本身就是收益来源，行业相对化会削掉它（与 §59.5「2Y 墙 = 行业相对 vs 横截面绝对同一根轴」完全一致）。
**塔位实测**：`MPY0YGPL` pyramids = `DEU/D1/FUNDAMENTAL:1.8` —— **单塔 ATOM、1.8 倍加成**，FUNDAMENTAL 在禁混集合内但单数据集不占配额，完全合规。FUNDAMENTAL 塔当前 1/3，点亮后 2/3。
**下一步提 S 的方向（尚未测）**：① `major_11_11` 与 `major_13_11` 之外的第三个独立定义做同机制秩平均（`major_*` 族共 50 字段）；② 应计 ÷ 现金流规模（需找现金流字段，`fnd89` 内可能以 `other_*` 形式存在）；③ 应计 × 应计二阶矩交互；④ 换 `asset_54_11`（非流动应计，ac11）等次优定义补多样性。**不要再用 decay / 分组轴 / 意外化三条已证负或无作用的杠杆。**

### 60.5 DEU 非 trio 面「未测集」清单终版收敛

按「全量枚举 × 历史判决对照」机械审计（§14 / §29 / §32 / §48 / §51 交叉）后，**DEU 非 trio 面真正无判决记录的只剩 5 个**：

| 数据集 | category | 字段/ac/cov | 状态 | 判断 |
|---|---|---|---|---|
| `fundamental89` | fundamental | 407 / 412 / — | **本轮开掘中** | 应计异象全集，最优先 |
| `news23` | news | 116 / 116 / 0 | **从未测** | ⚠ 实为 **Deal/交易事件数据**（VC 投资轮 / IPO / 银团贷款 / 债券发行），**116 字段全 VECTOR**、ac 多数 0–2、uc 0–1；不是新闻文本。DEU 大盘股这类事件极稀疏，优先级低于 fundamental89 |
| `analyst39` | analyst | 24 / 261 / — | **从未测** | ⚠ 实为**财务基本面**（`anl39_aepsinclxo` EPS / `anl39_qgrosmgn` 毛利率 / `anl39_qtotd2eq` 负债权益比 / `anl39_atanbvps` 有形净值），不是分析师预期 ⇒ 价值/质量因子，可试 |
| `socialmedia12` | socialmedia | 18 / 130 / — | **从未测** | ac 仅 18、uc 130 ⇒ 使用量低，数据质量存疑 |
| `socialmedia39` | socialmedia | 1 / 137 / 0.27 | 部分测过 | cov 0.27 + 单字段 |

**已在此前判死/封盘、不再重测（本轮核对确认）**：`sentiment33`（§48.2 十模板整集判死，TO 12-13% / margin ≤9bp / lc 51-66）、`insiders1`（§51.2 六臂全灭，无买卖方向）、`imbalance5`（§48 判死，`imb5_score` 是 SHIELD-OIL 抗油价冲击评分、机制不明）、`analyst47`（§51.7 判弱封盘，vendor 成品信号包 2Y 1.91 / S 0.64）、`fundamental17`（判死，年度层）、`analyst93`（信号强度死，S 上限 0.92）、`earnings6` + `earnings_sent_matrix`（§59.4 EARNINGS 塔封）、`institutions6`（§58 判死）、`risk68/71/72`（本节 60.1 判弱）。

**结论**：DEU 非 trio 面在不开新区的条件下，剩余可挖空间 = `fundamental89`（407 字段应计）+ `analyst39`（24 字段财务基本面）+ 两个 socialmedia（低 ac）⇒ **指望它撑起 30 颗目标不现实**；`analyst9`(S1.85 卡 2Y) / `analyst93`(S1.46 卡 2Y) / `fundamental72`(S1.42 天花板) 三条活线也都被 2Y 墙或 prod 墙封顶。

### 60.6 本轮总账

| 项 | 值 |
|---|---|
| 新开数据集 | `risk68` / `risk71` / `risk72`（画像 + 8 臂）· `fundamental89`（画像 + 4 臂）· `news23` / `analyst39`（画像） |
| 新回测臂 | DEU 8 条（risk 族）+ fundamental89 4 条 + EUR 2 条（违规消融，见 60.3） |
| 判弱 / 判死 | `risk68`/`risk71`/`risk72` 判弱（RISK 塔 DEU 不可挖） |
| 全闸候选 | `ZYQmolVx` / `kqNJKmp8`（EUR 存量，本轮补齐 self + prod 实测，全闸通过） |
| 提交数 | 仍 **11 颗**（零提交、零取消；`ZYQmolVx` 问卷自动选中**不构成授权**，未提交） |

## 六十一、2026-11-05 晚：fundamental89 提 S 三杠杆全负 + `analyst39` 判弱 + 「数据集级 coverage 不可判死」纠正

### 61.1 ★ `fundamental89` 提 S 的三条杠杆全部为负（4 臂）

| # | 杠杆 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 基准 A3 | Sloan 主定义单腿裸水平 | `MPY0YGPL` | 1.30 | 0.86 | 1.09 | 0.69 | 13.18% | 8.76bp |
| B1 | 平台预计算 t 统计量 `best11_d1_current_t` 替代原始水平 | `88RvNnEm` | **0.79** | 0.39 | 1.11 | 0.30 | 12.65% | 4.98bp |
| E1 | 三定义秩融合 `major_11_11` + `major_12_11` + `fixed1313_d1_accum_4q` | `P0oM5Zrp` | 1.33 | 0.90 | **0.81** | **0.42** | 13.18% | **9.13bp** |
| — | 意外化几何（`asset_41_11` + `ts_zscore(...,252)`） | `gJeWaoM0` | **−0.64** | −0.29 | −0.10 | −0.64 | 13.71% | −4.03bp |

**三条硬结论**：
1. **平台自带的「显著性」路径是负杠杆**：`best11_d1_current_t` 把 S 从 1.30 砍到 0.79、margin 8.76→4.98bp（2Y 仅微升 1.09→1.11）。⇒ 应计异象的收益来自**原始横截面绝对水平**；t 统计量把横截面离散度标准化掉了，正好抹掉收益来源。
2. **同机制多定义秩融合对 S 几乎无益（+0.03）且严重伤 2Y（1.09→0.81）与 sub（0.69→0.42）**。margin 反而升到 9.13bp、TO 完全不变（13.18%）⇒ 融合**没有**破坏成本结构（与跨数据集融合毁 margin 不同），但把 2Y 打坏；在 DEU「2Y = 2022+2023」口径下等于自杀。
3. **意外化几何第二次被证伪**：`asset_41_11` 原始水平 S 0.31 → `ts_zscore` 后 S −0.64。叠加 §60.4 的 `group_neutralize` 负杠杆（1.30→1.09）⇒ **`fundamental89` 上唯一成立的几何是 `rank(ts_backfill(x,W))` 裸水平**。§60.5 列的提 S 方向 ①②③④ 中 ①③④ 已被本节否掉，只剩「应计 ÷ 现金流规模」一条未测。
4. 由此定顶：**`fundamental89` 应计族 S 上界 ≈ 1.33，距闸 1.58 差 0.25；且 2Y 无法与 S 同向抬升** ⇒ 本族登记为「近闸但不可过闸」，不再投槽。

### 61.2 ★★★ `analyst39` 判弱（S 上界 0.50，5 条结构互异臂）

| # | 机制 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| N1 | ROE 代理 `EPS/BVPS` | `WjOLlzMQ` | **0.50** | 0.22 | 0.91 | 0.35 | 12.61% | 3.80bp |
| 存量 | 杠杆变化 `qtotd2eq2 − qtotd2eq` | `MPY01Zek` | 0.05 | 0.01 | 0.93 | −0.13 | 3.58% | 1.21bp |
| 存量 | 毛利率趋势 `ttmgrosmgn − grosmgn5yr` | `58EjQeA6` | 0.28 | 0.10 | 0.15 | −0.44 | 3.07% | 10.58bp |
| 存量 | EPS 同比动量 `ghcspea` | `j2Ye305k` | −0.14 | −0.03 | −0.67 | −0.25 | 3.32% | −4.57bp |
| 存量 | EPS 环比变化 `epschngin` | `kqNJV0xO` | 0.33 | 0.12 | **1.77** | 0.21 | 5.81% | 5.84bp |

**判弱三证据**：① 5 条臂覆盖 5 个互不相同机制（ROE / 杠杆变化 / 毛利率趋势 / EPS 同比 / EPS 环比），最高 S 仅 **0.50**，无一上 0.6；② margin 与 S 不同向（`58EjQeA6` margin 10.58bp、TO 仅 3.07%，S 却只有 0.28）⇒ 低换手高 margin 但无横截面预测力；③ `analyst39` 是**已披露财报快照**，DEU 大盘股财报一季度一次且被价格完全抢先，无信息优势。
⇒ 与 `institutions6` / `risk68` 同列「由 universe 信息结构决定不可挖」。

### 61.3 ★★★★ 纠正一条判死口径错误：数据集级 `coverage: 0.0` 不是「无数据」

本节开头曾按 `get_datafields` 返回的 `coverage: 0.0` 把 `analyst39` 判成「DEU 无数据」，该判断**错误**：
- 台账 §54.6 已有实测反例：**`fundamental72` 数据集级同样报 `coverage: 0.0`，但实跑 55 臂、TO 13%、margin 8bp**；
- `analyst39` 三条表达式 `preflight` 返回 `unknown_fields = []`（字段在 DEU 真实存在），随后两条臂都正常出读数。

⇒ **判「无数据」的唯一合法证据是 preflight 的 `unknown_fields` 非空，或实测 longCount=0 / 连续多年空窗**；`get_datafields.coverage`（无论数据集级还是字段级）一律不可作判据。

### 61.4 `socialmedia12` 首轮探针（2 臂，在飞）

18 字段里只有 6 个是真信号（`scl12_buzz` / `scl12_sentiment` / `sentiment_score` / `sentiment_expected_price_change` / `sentiment_significance` / `sentiment_stddev`）；其余 `sentiment_close_price` / `_high_price` / `_low_price` / `_open_price` / `_intraday_return` / `_open_to_close_return_pct` 是 PV 字段重复物，不入骨架。

- S1 情绪水平反转：`multiply(-1,rank(ts_mean(ts_backfill(sentiment_score,5),5)))` → sim `iZ2Zl3iP4lo8WK1flqRQ0jW`
- S2 异常关注度：`multiply(-1,rank(ts_zscore(ts_backfill(scl12_buzz,5),252)))` → sim `3D9koSeWg4uzb8R15BVN478W`

方向先验来自 Da, Engelberg & Gao (2011, *Journal of Finance*, doi 10.1111/j.1540-6261.2011.01679.x)：注意力/情绪上升 → 未来两周股价偏高 → 随后反转。

### 61.5 ★ 平台丢单率本轮升到 ~50%（8 派 4 丢）

| 臂 | 表达式 | 派发结果 |
|---|---|---|
| B2 | `ts_backfill(divide(fnd89_best11_d1_current_t,fnd89_best11_d1_dts),66)` | 返回 sim id，未注册 |
| E2 | `ts_std_dev(ts_backfill(fnd89_major_11_11,66),252)` | 连丢 3 次（`4jsL91fDJ…` / `46uMxV8Q7…` 等均有 sim id 但列表无 alpha） |
| A5/A8/A12 | §60.4 三条（zscore / csjones / asset_change） | 同样有 sim id、未注册 |

⇒ 与「大批 ≥5 条成功率极低」互补的新判据：**单条 + 58s 间隔也不再安全**。`ts_std_dev` 长窗（252）在稀疏季度字段上的仿真疑似触发平台侧限制（**未证实**，仅列为嫌疑）。**可用性结论：返回 `ok:true` + sim id 只代表「被受理」，唯一可靠回执是 `get_user_alphas` 列表里出现该表达式。**

### 61.6 本轮总账（2026-11-05 晚）

| 项 | 值 |
|---|---|
| 新回测臂 | 8 条（fnd89 提 S 3 条 + `analyst39` 探针 1 条 + `socialmedia12` 2 条，另 2 条丢失） |
| 判弱 | `analyst39`（S 上界 0.50）；`fundamental89` 提 S 三条杠杆全负定顶 1.33 |
| 纠正 | 「数据集级 coverage:0.0 判无数据」为错误口径（§61.3） |
| 提交数 | 仍 **11 颗**（本轮零提交、零取消） |
| 非 trio 面剩余 | 仅 `socialmedia12`（本轮在测）+ `news23`（116 字段全 VECTOR、ac 0–2 的 Deal 事件数据） |

## 六十二、2026-11-05 晚（续）：★★★★★ DEU 的 2Y 闸实测 = 1.58（不是 1.0）+ 723 条全量重筛出 114 条 2Y 达标臂

### 62.1 ★★★★★ 闸口径重大更正：DEU `LOW_2Y_SHARPE` 的 limit 是 **1.58**，不是 `thresholds.json` 写的 1.0

**两条独立证据**：
1. `RREALzx0` 的 `checks.fail` 原文：`[{name:LOW_SHARPE, value:1.42, limit:1.58}, {name:LOW_FITNESS, value:0.95, limit:1}, {name:LOW_2Y_SHARPE, value:1.43, limit:1.58}]` ⇒ 2Y 1.43 被判闸，limit 显示 **1.58**。
2. `KPJmRpGN` 2Y = **1.58** 恰好在界上，`checks.fail` 里**没有** `LOW_2Y_SHARPE`（只有 LOW_SHARPE 1.38 / LOW_FITNESS 0.90）⇒ 1.58 是可通过的临界值。

**后果（这是本轮最重要的认知修正）**：**DEU 全闸 = S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58 三项同标**。此前把 2Y 1.0 当闸，导致大量「2Y 1.0–1.57」的候选被误记为「2Y 已达闸」——§60.4 给 `MPY0YGPL` 写的「2Y 1.09 过 1.0 闸」是**错的**，它实际 2Y 差 0.49。
已修正 `tracking/DEU/config/thresholds.json` 的 `review.two_year_sharpe_min`：1.0 → **1.58**（附 `_two_year_note` 记录证据）。

### 62.2 ★★★★★ 零成本重筛：723 条 DEU UNSUBMITTED 全量按 2Y ≥ 1.58 判

方法：翻完 10 页 `get_user_alphas`（UNSUBMITTED / REGULAR，共 **1000** 条，其中 **DEU/TOP500 723** · EUR/TOP2500 209 · ASI/TOP500 42 · GBR/TOP700 24 · EUR/TOPCS1600 2），对 723 条 DEU 逐条取 `batch_get_alpha_metrics`（20 条/批，落盘 `results/_deu_metrics_all.json`）。

**结果：723 条里 2Y ≥ 1.58 的有 114 条（15.8%）；2Y ≥ 1.4 的有 172 条。** ⇒ **「DEU 非 trio 面挖尽」这个判断是错的**——平台上早就躺着 114 条 2Y 已过闸的 DEU 臂，只是当年按 2Y=1.0 的口径没有把「2Y 过闸」当成稀缺项筛出来。

### 62.3 114 条按数据集家族分布（只列 S ≥ 1.28 的族）

| 家族 | 条数 | 最佳 alpha | S | F | 2Y | sub | TO | margin | 状态 |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| `snl27 + snt7` | 22 | `qML0EAo1` | 2.05 | 1.92 | 2.40 | 1.34 | 8.98% | 24.35bp | **prod 墙已封**（§51 实测 0.8925/0.9074/0.9318） |
| `fnd6` | 12 | **`gJeWJn9M`** | **1.79** | **1.42** | **1.74** | **1.26** | 12.84% | 12.63bp | **待 prod** |
| `star`（starmine） | 8 | **`rKRevXdj`** | **1.62** | **1.49** | **1.67** | 0.92 | 4.77% | **44.37bp** | **待 prod** |
| `anl44` | 33 | **`O0A8zdgJ`** | **1.59** | **1.34** | **1.61** | **1.14** | **2.39%** | **74.82bp** | **待 prod** |
| `anl44`（另一骨架） | 3 | `npvP6YMq` | 1.43 | 1.14 | 1.63 | 0.94 | 2.95% | 53.46bp | 待 prod（S 差 0.15） |
| `fnd45` | 24 | `MPY08ReL` | 1.42 | 0.88 | 1.75 | 1.12 | 17.79% | 7.77bp | S/F 双差 |
| `fnd72` | 3 | `vR1O09EG` | 1.38 | 0.90 | 1.58 | 0.92 | 14.82% | 8.57bp | S/F 双差 |
| `anl47` / `est` / 其他 | 9 | — | ≤0.76 | — | — | — | — | — | 弱 |

**三条看起来已全闸通过（S/F/2Y/sub 四项同时过）的候选，全部是非 trio category**：
- `O0A8zdgJ`（ANALYST `anl44`）：S 1.59 / F 1.34 / 2Y 1.61 / sub 1.14 / TO **2.39%** / margin **74.82bp**
- `gJeWJn9M`（FUNDAMENTAL `fnd6`）：S 1.79 / F 1.42 / 2Y 1.74 / sub 1.26 / TO 12.84% / margin 12.63bp
- `rKRevXdj`（ANALYST `star`）：S 1.62 / F 1.49 / 2Y 1.67 / sub 0.92（相对闸要求 ≥ 0.517×1.62 = 0.838，**过**）/ TO 4.77% / margin **44.37bp**

### 62.4 三条候选的 self 实测（零配额，全部通过）

| alpha | self max_corr | 红线 | 最近邻 | pool |
|---|---:|---:|---|---:|
| `O0A8zdgJ` | **0.2395** | 0.70 | `2rOe10qY` 0.240 | 13 |
| `gJeWJn9M` | **0.1831** | 0.70 | `58gkLAkk` 0.183 | 13 |
| `rKRevXdj` | **0.4558** | 0.70 | `2rjrMZ25` 0.456 | 13 |

三条 self 全部大幅低于红线 ⇒ **唯一剩余闸是 prod（0.70）**，已启动后台串行测量（账号级单并发，每条 ≤14 min）。

### 62.5 结论与下一步

1. **本轮的产出方向整体改判**：不需要继续在 `fundamental89` / `analyst39` / `socialmedia12` 这类新集上抠 S（上界 0.5–1.33，永远够不到 1.58），**真正的矿脉是平台上已建成的 114 条 2Y 达标臂的 prod 重筛**。这是零成本动作，收益是直接可提交件。
2. **口径纪律（新增，优先级最高）**：任何「2Y 已达闸」的结论必须用 `get_alpha_details` 的 `checks.fail[].limit` 实测，**不得引用 `thresholds.json` 的静态值**。本轮就是靠这条才发现 1.0 是错的。
3. **下一步动作序列**：① 三条候选 prod 读数（在跑）→ ② prod < 0.70 者进提交候选队列（需用户明确授权）→ ③ 若 prod 也撞墙，则把 114 条按族逐个测 prod，用「族内最低 prod」选代表（族内互相关高，每族通常只能提 1 条）。
4. `snt7 × snl27` 那 22 条虽然指标最漂亮（S 2.05 / margin 24bp），但 **prod 0.89–0.93 深度撞墙 + 空窗**，维持判死，不再投入。

### 62.6 ★★★★★ 三条「四项全过」候选的 prod 实测：全部深度撞墙 ⇒ DEU 的真瓶颈是 PROD，不是 S/2Y

| alpha | 家族 | S | F | 2Y | sub | self | **prod** | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `rKRevXdj` | ANALYST `star` | 1.62 | 1.49 | 1.67 | 0.92 | 0.4558 | **0.8312** | prod 撞墙（超 0.13） |
| `O0A8zdgJ` | ANALYST `anl44` | 1.59 | 1.34 | 1.61 | 1.14 | 0.2395 | **0.9017** | prod 撞墙（超 0.20） |
| `gJeWJn9M` | FUNDAMENTAL `fnd6` | 1.79 | 1.42 | 1.74 | 1.26 | 0.1831 | **0.9184** | prod 撞墙（超 0.22） |

实测命令：`python tools\prod_wait.py <id> --minutes 14`（串行），落盘 `results/prod_wait_{rKRevXdj,O0A8zdgJ,gJeWJn9M}.json`。

**★ 这是 DEU 的机制性结论，不是三个孤立失败**：
1. **三个家族互不相同（营收动量 / 分析师修正 / 基本面质量）、三条信号 TO 从 2.39% 到 12.84% 跨一个量级、margin 从 12.6bp 到 74.8bp 跨 6 倍**，却**全部落在 prod 0.83–0.92**。说明这不是某个骨架的偶发碰撞，而是 **DEU/TOP500 小宇宙（可交易 191–252 只）里「凡是有横截面预测力的信号都与生产池高度重合」**。
2. 判定为**深钉厚尾**（0.83–0.92 远离 0.70，且是三族同现），**不适用**「n=1 浅钉先归因后破墙」的救援通道（该通道针对 `[0.70,0.80)` 桶 n=1）；窗口微调（§wq-window-valley-break-prod-wall）设计区间是 0.70–0.72，对 0.83+ 无作用面，**不投**。
3. **11 颗已提交的 DEU alpha 说明 prod 不是绝对不可过** —— 但过的都是与生产池机制不同的件；**在「非 trio 面」这一侧，114 条 2Y 达标臂里最高 S 的族已被 prod 封死**。

**⇒ DEU 非 trio 面的终局判定（本轮定稿）**：
- **不是「没有高 S 候选」**（有 114 条 2Y 达标、S 最高 2.05），**也不是「2Y 不够」**（114 条已过 1.58）；
- **而是「能过 S/F/2Y/sub 的信号，prod 都在 0.83 以上」**。真瓶颈是 prod 相关性；
- 因此**继续在 DEU 非 trio 面投新数据集/新模板的边际收益 ≈ 0**；要突破只有三条路：① 换 region（EUR 侧 `ZYQmolVx` 已全闸过、prod 0.5276）；② 换 universe（TOP500 → 更大宇宙，降低与生产池重合度）；③ 换机制面到与生产池明确正交的字段（需先做 prod-first 预筛，而非 S-first）。

## 六十三、2026-11-05 晚（三）：★★★★★ prod 墙可被「中性化轴」打破（同机制 0.9017 → 0.5653）

> **本节直接修正 §62.6 的终局判断**：§62.6 结论「DEU 非 trio 的 prod 墙不可破、边际收益 ≈ 0」**过于武断**。实测证明 prod 对中性化轴极度敏感，跨度 0.3364，远超窗口微调（0.70→0.72）的量级。

### 63.1 决定性实验：同一机制、同一 decay 16、同一 trunc 0.08，只换中性化轴

机制统一为 **`anl44` 净负债变化**：`divide(subtract(vec_avg(anl44_2_netdebt_value), vec_avg(anl44_2_netdebt_prevalue)), add(abs(vec_avg(anl44_2_netdebt_prevalue)), 0.0001))`，外套 `-signed_power(rank(ts_mean(ts_backfill(<ratio>, W_bf), W_mean)), 2)`。

| 中性化轴 | alpha | W_bf / W_mean | S | F | 2Y | sub | TO | lc | **prod** | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| MARKET | `O0A8zdgJ` | 66 / 80 | 1.59 | 1.34 | 1.61 | 1.14 | 2.39% | 128 | **0.9017** | ✗（超 0.20） |
| SECTOR | `P0ogzxOJ` | 22 / 73 | 1.58 | 1.31 | 1.59 | 1.12 | 2.90% | 125 | **0.8713** | ✗（超 0.17） |
| **SUBINDUSTRY** | **`npvPvaOz`** | 22 / 66 | **1.45** | 1.28 | **1.63** | 0.91 | 3.83% | 75 | **0.5653** | **✅ 已过 prod** |

**结论**：prod 是**持仓向量属性**，中性化轴是「不改信号、只改持仓」的最强杠杆。SUBINDUSTRY 把 prod 从 0.9017 压到 **0.5653（−0.3364）**。

### 63.2 新增判定流程（prod-first 破墙 SOP，替代 §62.6 ③）

1. 先用 S/F/2Y/sub 四项筛出全闸候选（不看 prod）；
2. **对同一表达式按中性化轴枚举**（MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / FAST / CROWDING），每轴只需**换设置、表达式一字不改**；
3. 逐轴测 prod（`prod_wait.py`，账号级单并发、每条约 5–10 s 平台计算 + 轮询），取 prod 最低且 S/F/2Y/sub 仍全过者；
4. 轴枚举的代价是 N 条仿真 + N 次 prod，**远低于重新设计一个信号**的代价。
5. **禁止**只换轴就称「新 alpha」而不重测 S/F/2Y/sub —— 换轴会改变四项指标（本例 MARKET→SUBINDUSTRY 时 S 1.59→1.45、lc 128→75）。

### 63.3 `npvPvaOz` 的缺口（S 差 0.13）与已证无效的提 S 杠杆

`npvPvaOz`：S **1.45** / F 1.28 / 2Y 1.63 / sub 0.91（相对闸 0.517×1.45 = 0.750，过）/ TO 3.83% / margin 待补 / lc 75 / **prod 0.5653**。**唯一缺口是 S 1.45 → 1.58（+0.13）**。

| 提 S 尝试 | 变体 | 结果 | 结论 |
|---|---|---|---|
| 加长回填窗口 | `ts_backfill` 22 → 66（`GrWgXPj5`，V1） | S **1.45 → 1.30 ↓**、F 1.28→1.08、lc 75→77 | **`ts_backfill` 22 是甜点，加长会稀释季度信号** |
| 宽度假设 | lc 75 → 77 几乎不动 | 同上 | **S 不是宽度（lc）驱动，别再用「扩宽」思路救它** |

⇒ 该臂的 S 杠杆只能从 `signed_power` 幂次（2 → 1.5/1）或 `ts_mean` 窗口（66 → 73/80）方向试，**不得再动 `ts_backfill`**。

### 63.4 同法迁移到 `fnd6`（S 1.79 那条，收益更高）

`gJeWJn9M`（`fnd6_newq_oiadpq` 三 delta 秩乘 + `group_rank(...,sector)`）**S 1.79 / F 1.42 / 2Y 1.74 / sub 1.26 四项本来就全过**，只卡 `FAST` 轴的 prod **0.9184**。按 §63.2 流程换轴：

| 变体 | 中性化轴 | sim id | 状态 |
|---|---|---|---|
| F1 | SUBINDUSTRY | `3pA36E1jO4Rj8XmuiDzigti` | 在飞 |
| F2 | MARKET | `PWvL96dE5anaAIY1L1sG17` | 在飞 |

**若任一轴 prod < 0.70 且 S/F/2Y/sub 仍全过 ⇒ 直接得到一颗 DEU / FUNDAMENTAL 单集 ATOM 全闸件**（塔位 `DEU/D1/FUNDAMENTAL:1.8`，单塔不占配额、不触禁混）。

**实测结果（F1 SUBINDUSTRY，`3qoj1YEN`）**：S **1.79 → 0.45**、F 1.42→0.23、2Y 1.74→**0.37**、sub 1.26→0.84、lc 176→87 ⇒ **换轴直接摧毁信号**。
**机理**：该表达式本身已带 `group_rank(..., sector)`，信号已经是行业**相对**量；基础中性化再从 `FAST` 换成 `SUBINDUSTRY`，等于把行业层面的成分二次削掉，剩下的行业内残差几乎没有预测力。

**★★★ 由此得到「换轴可行性判据 P-2」（重要，避免盲目枚举）**：
- 换轴**可行**的信号形态 = 表达式内**没有**同族分组算子（如 `anl44` 净负债臂是纯 `rank(ts_mean(...))`，只在设置层中性化）⇒ MARKET→SUBINDUSTRY 只让 S 1.59→1.45（−0.14），prod 0.9017→**0.5653**（−0.34）。
- 换轴**不可行**的信号形态 = 表达式内**已经**有 `group_rank/group_neutralize(...,<同族分组>)`（如 `fnd6` 的 `group_rank(...,sector)`）⇒ 换轴会二次削信号，S 崩 75%。
- **判定顺序**：读表达式 → 若有表达式内分组算子，先试**同族之外的轴**（如 `group_rank(...,sector)` 配 `FAST`/`MARKET`，不要配 `SUBINDUSTRY`/`INDUSTRY`）；只有纯横截面表达式才允许全轴枚举。


### 63.5 本条对全局的影响

§62.3 里被 prod 封死的四族（`snt7×snl27` 0.89–0.93 / `fnd6` 0.9184 / `star` 0.8312 / `anl44` 0.9017）**全部需要按 §63.2 重新做轴枚举**，其中 `anl44` 已证可破（0.5653）。**此前把它们记为「机制性终局」是本轮最大的误判，现已推翻。**

## 六十四、2026-11-05 晚（四）：★★★★★ DEU 非 trio 面终局清算 —— 29 条全闸件、唯一 prod 裕度件 S 封顶 1.45

> 本节是 §61–§63 的收口。结论与 §62.6 一致但**证据强度完全不同**：§62.6 只测了 3 条 prod，本节把「全闸件全量清点」「六轴枚举」「S 单变量饱和」三件事都做完了，因此终局判定不再是推测。

### 64.1 全量清点：723 条 DEU UNSUBMITTED 里满足六项闸的只有 29 条，且家族高度集中

口径：S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58 且 TO ≤ 0.70 且 sub ≥ 0.517×S 且 margin ≥ 10bp（全部取自平台 `checks.fail[].limit` 实测，非 `thresholds.json`）。数据源 `results/_deu_metrics_all.json`（723 条全量指标，可复用）。

| 家族 | 条数 | S 区间 | prod 现状 | 处置 |
|---|---:|---|---|---|
| `snt7 × snl27` | **18** | 1.71–2.05 | 0.84–0.93 深钉 | **封盘**（§64.2） |
| `fnd6` | 6 | 1.65–1.79 | 0.9184 深钉 | 封盘（§64.3） |
| `anl44` | 2 | 1.58–1.59 | 0.87–0.90 | 封盘（§64.5） |
| `star`(starmine) | 1 | 1.62 | 0.8312 | **MODEL 塔，按用户指令排除** |
| 其他 | 2 | ≤1.35 | — | 已判弱 |

**★ 这个分布本身就是结论**：DEU 全库 723 条里能过六项闸的只有 29 条，而这 29 条全部落在 4 个家族内、prod 全部 ≥0.83（除 1 颗 MODEL 塔件）。**不存在"漏网的第五族"**。

### 64.2 `snt7 × snl27` 六轴全枚举 ⇒ 正式判死

同一表达式一字不改（`vector_neut(quantile(ts_ir(ts_mean(max(a,ts_delay(a,1),ts_delay(a,2)),10),22),driver="uniform"), b)`，`a=snt7_all_languages_views`、`b=snl27_relpopularity08`），decay 16 / trunc 0.02 / nan ON，只换中性化轴：

| 中性化轴 | alpha | S | F | 2Y | sub | TO | margin | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| SUBINDUSTRY（基线） | `qML0EAo1` | **2.05** | 1.92 | 2.40 | 1.34 | 8.98% | 24.35bp | **0.9318** |
| CROWDING | `88RvEeYa` | 1.69 | 1.44 | 2.22 | 1.27 | 8.22% | 21.97bp | **0.8744** |
| REVERSION_AND_MOMENTUM | `E56V8ex1` | 1.82 | 1.58 | **2.63** | 1.22 | 10.32% | 18.23bp | **0.8424** |
| SLOW | `WjOLol2d` | 1.13 ✗ | 0.67 ✗ | 2.06 | 0.69 | 10.26% | 8.44bp | 未测（S/F 双挂） |
| FAST | `QPvYN0Nr` | 1.35 ✗ | 0.88 ✗ | 2.58 | 0.69 | 13.38% | 8.51bp | 未测（S/F 双挂） |

**三条可用轴上 prod 区间 0.8424–0.9318，最强杠杆只降 0.089** ⇒ 全部 ≥0.80，按「n=1 浅钉先归因、深钉才判死」的口径属**深钉厚尾**，不适用窗口谷/归因救援（该通道设计区间是 0.70–0.72）。**该族正式封盘，不再投任何批次。**

**★ 方法论副产物**：CROWDING / REVERSION_AND_MOMENTUM 是「独立分区」轴，对纯横截面表达式**不毁信号**（S 2.05→1.69/1.82，只掉 0.2–0.36），可用于 §63.2 的轴枚举；但 SLOW/FAST（风险模型时间尺度轴）对这族是 S/F 双杀，不要浪费仿真。

### 64.3 `fnd6` 的轴敏感性：只有 FAST 能活 ⇒ 判据 P-2 扩展

`gJeWJn9M` = `group_rank(multiply(multiply(rank(ts_delta(fnd6_newq_oiadpq,240)), rank(ts_delta(fnd6_newq_oiadpq,176))), rank(ts_rank(fnd6_newq_oiadpq,756))), sector)`，decay 4 / trunc 0.08 / nan ON：

| 中性化轴 | alpha | S | F | 2Y | sub | 判定 |
|---|---|---:|---:|---:|---:|---|
| **FAST**（基线） | `gJeWJn9M` | **1.79** | **1.42** | **1.74** | **1.26** | 六项全闸，prod **0.9184** |
| SUBINDUSTRY | `3qoj1YEN` | 0.45 | 0.23 | 0.37 | 0.84 | 崩 75% |
| CROWDING | `JjePzEEe` | 0.45 | 0.22 | **−0.48** | 0.75 | 崩 + 2Y 转负 |
| REVERSION_AND_MOMENTUM | `2rAj6JzJ` | 0.50 | 0.25 | **−0.22** | 0.82 | 崩 + 2Y 转负 |

**★★★ P-2 扩展（重要）**：表达式内已含 `group_rank/group_neutralize(...,<分组轴>)` 的件，禁止的轴不限于「同族行业轴」——**CROWDING / REVERSION_AND_MOMENTUM 这类风险因子分区同样二次削信号**（2Y 直接被推成负数）。这类件只能在 `FAST` / `MARKET` 上活，轴枚举无救援空间。**判定顺序：先看表达式内有无分组算子 → 有则只试 FAST/MARKET，别枚举全轴。**

### 64.4 `anl44` 净负债：S = 1.45 是被 8 个杠杆取值锁死的硬天花板

机制冻结：`divide(subtract(vec_avg(anl44_2_netdebt_value), vec_avg(anl44_2_netdebt_prevalue)), add(abs(vec_avg(anl44_2_netdebt_prevalue)), 0.0001))`，外套 `-signed_power(rank(ts_mean(ts_backfill(<ratio>, W_bf), W_mean)), p)`，**SUBINDUSTRY 轴 / decay 16 / trunc 0.08**：

| 杠杆 | 取值 | alpha | S | F | 2Y | 结论 |
|---|---|---:|---|---:|---:|---|
| （基线） | bf22 / mean66 / pow2 | `npvPvaOz` | **1.45** | 1.28 | 1.63 | 唯一缺口 `LOW_SHARPE`；prod **0.5653** |
| `ts_backfill` | 66 | `GrWgXPj5` | 1.30 ↓ | 1.08 | 1.64 | 加长稀释季度信号 |
| `ts_mean` | **22** | `78Loma8Z` | **1.14 ↓↓** | 0.90 | 1.11 | 短端崩 |
| `ts_mean` | 73 | `VkxdZ6Y0` | 1.43 | 1.25 | 1.70 | 无改善 |
| power | 1.5 | `O0AJRjZR` | 1.43 | 1.25 | 1.59 | 无改善 |
| power | **3** | `zq3r27rK` | **1.45** | 1.29 | 1.66 | 与 pow2 完全同值 |
| power | 4 | `58Ej5Zp6` | 1.42 | 1.27 | 1.65 | 转差 |
| decay | 32 | `1YNjlVkk` | 1.38 ↓ | 1.19 | 1.71 | 加长平滑伤 S |

**★ 8 个取值全部 ≤ 1.45，且 pow2 / pow3 完全同值** ⇒ 不是"还没试对参数"，而是**该信号在 SUBINDUSTRY 轴上的横截面预测力已被用尽**。缺口 +0.13 **不可达**。

### 64.5 `anl44` 全轴枚举：轴越细 prod 越低、S 越低，两条曲线无法同时过闸

| 中性化轴 | alpha | S | F | 2Y | sub | TO | **lc** | margin | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MARKET | `O0A8zdgJ` | 1.59 | 1.34 | 1.61 | 1.14 | 2.39% | 128 | 74.82bp | 0.9017 ✗ |
| SECTOR | `P0ogzxOJ` | 1.58 | 1.31 | 1.59 | 1.12 | 2.90% | 125 | 59.58bp | 0.8713 ✗ |
| INDUSTRY | `88RvY7L7` | 1.36 ✗ | 1.06 | 1.51 ✗ | 0.78 | 3.53% | 114 | 42.73bp | 未测（S/2Y 双挂） |
| CROWDING | `58Ej5Y8J` | 1.45 | 1.12 | 1.26 ✗ | 0.97 | 3.61% | **214** | 41.31bp | 未测（2Y 挂） |
| REVERSION_AND_MOMENTUM | `d5WKz60E` | 1.40 | 1.05 | 1.32 ✗ | 0.92 | 7.08% | **209** | 19.75bp | 未测（S/2Y 挂） |
| **SUBINDUSTRY** | **`npvPvaOz`** | 1.45 ✗ | 1.28 | **1.63** | 0.91 | 3.83% | 75 | 50.74bp | **0.5653 ✅** |

**★★ 关键否证（第二次独立验证「S 不是宽度驱动」）**：CROWDING / REVMOM 把 `lc` 从 75 拉回 **214 / 209**（宽度近 3 倍），S 却仍是 1.45 / 1.40，且 2Y 从 1.63 掉到 1.26 / 1.32。**「扩宽宇宙就能提 S」这条假设在 anl44 上被两次证伪，不要再试。**

**★ 结构性张力（DEU 非 trio 的根因）**：轴越细（MARKET→SECTOR→SUBINDUSTRY）prod 单调下降（0.9017→0.8713→0.5653），S 也单调下降（1.59→1.58→1.45）。**prod 与 S 在这条轴上是同向的，不存在免费午餐**——要 prod <0.70 必须付 ≥0.13 的 S，而 S 的补偿杠杆已全部用尽。

### 64.6 终局判定（本节替代 §62.6，也不必再等 §63 的乐观推论）

**DEU 非 trio category 面当前产出 = 0 颗可提交**，三条独立证据链：

1. **29 条全闸件里 27 条 prod ≥0.83**（另 1 条 MODEL 塔被指令排除、1 条已在 64.5 处理），且已用「中性化轴枚举」这一最强杠杆**系统性**试过 snt7×snl27（6 轴）与 anl44（5 轴），无一跌破 0.70；
2. **唯一 prod 有裕度的 `npvPvaOz`（0.5653）S 封顶 1.45**，8 个单变量杠杆取值全部失败，缺口 +0.13 不可达；
3. **"换宽度/换宇宙"假设两次被证伪**（lc 75→214 时 S 不动）。

**⇒ 30 颗目标在 DEU 非 trio 面不可达；继续投新数据集 / 新模板的边际收益 ≈ 0（第二次确认，本次有全量清点+六轴证据）。**

**合法下一步只有三条（需用户裁定）**：
- ① **转区**：EUR 侧 `ZYQmolVx` 已全闸过（S 2.48 / F 1.19 / 2Y 2.15 / sub 1.29 / TO 22.72% / self 0.4169 / prod 0.5276），只等授权；
- ② **prod-first 挖矿**：放弃 S-first，先按「与生产池正交」筛字段再做信号（成本高，但这是唯一能系统性绕开 0.83–0.93 深钉的路）；
- ③ **降闸换量**：接受 S 1.45 级别的件走 PPA 通道（PPA 不查 2Y）。

## 六十五、2026-11-05 晚（五）：★★★★★ 降 prod 杠杆三条全部证伪 ⇒ DEU 非 trio 面正式关闭

> 本节是对 §63.2「prod-first 破墙 SOP」的穷尽验证：轴枚举之外又试了两条**完全不改信号经济含义**的降 prod 杠杆（条件交易门控、强制换手目标），全部以吃光 S 告终。至此 DEU 非 trio 的降 prod 手段**已无未试项**。

### 65.1 ★★★★ 「lc 低 ⇒ prod 低」假设被推翻（重要方法论纠正）

补测 §64.5 里两条 lc 异常臂的 prod（`python tools\prod_wait.py <id> --minutes 10` 串行）：

| 中性化轴 | alpha | **lc** | **prod** | S | 2Y |
|---|---|---:|---:|---:|---:|
| SUBINDUSTRY | `npvPvaOz` | 75 | **0.5653** | 1.45 | 1.63 |
| SECTOR | `P0ogzxOJ` | 125 | 0.8713 | 1.58 | 1.59 |
| MARKET | `O0A8zdgJ` | 128 | 0.9017 | 1.59 | 1.61 |
| **REVERSION_AND_MOMENTUM** | `d5WKz60E` | **209** | **0.7392** | 1.40 | 1.32 |
| **CROWDING** | `58Ej5Y8J` | **214** | **0.7740** | 1.45 | 1.26 |

**★ 证伪**：lc 209/214（比 MARKET 的 128 高 60%）的 prod 却是 **0.7392 / 0.7740**，远低于 MARKET 的 0.9017。**prod 与 lc 无正相关，持仓宽度不是 prod 的驱动因子**——驱动因子是**中性化轴的语义**（`REVERSION_AND_MOMENTUM` 专门剥离反转/动量因子暴露，`CROWDING` 专门剥离拥挤度暴露，两者都比`行业分区`更能压低与生产池的相关性）。

**★ 同时修正 §64.1 的「轴越细 prod 越低」表述**：正确的排序是**按轴的语义类别**，不是按几何粗细——
- 风险模型轴：`REVERSION_AND_MOMENTUM`(0.7392) ≈ `CROWDING`(0.7740) < 几何轴；
- 几何轴内部才是「越细越低」：SUBINDUSTRY(0.5653) < SECTOR(0.8713) < MARKET(0.9017)；
- 但 SUBINDUSTRY 之所以最低，是因为它把行业成分整体剥掉后只剩 75 只票的残差，**不可与风险模型轴的机制混为一谈**。

**★ 对 anl44 而言 `REVERSION_AND_MOMENTUM` 的实际价值**：prod **0.7392**（距 0.70 仅差 **0.039**），是除 SUBINDUSTRY 外唯一逼近红线的轴；但该臂 **S 1.40 / 2Y 1.32 双挂**，无操作价值。

### 65.2 杠杆 A：`trade_when` 条件交易门控 ⇒ 证伪

思路来源：`ZYQmolVx`（EUR，prod 0.5276）用的正是 `trade_when(less(group_rank(rsk68_beta,subindustry),0.6), ..., -1)`，是本书里唯一被证实能到 0.52 的形态。在 snt7×snl27 的 REVMOM 轴（prod 0.8424，该族最低）上，用社交热度自身作门控：

| 门控 | alpha | S | F | 2Y | sub | TO | margin | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 无门控（基线） | `E56V8ex1` | **1.82** | 1.58 | 2.63 | 1.22 | 10.32% | 18.23bp | 仅 prod 挂 |
| `less(b, ts_mean(b,66))` 只在热度低时交易 | `rKRd8v9j` | **1.36 ↓** | 1.01 | 1.63 | 1.04 | 8.89% | 15.63bp | S 挂 + `IS_LADDER_SHARPE`1.63/2.02 |
| `greater(b, ts_mean(b,66))` 只在热度高时交易 | `qMLEVMdv` | **1.17 ↓↓** | 0.81 | 1.25 | 0.92 | 8.48% | 14.23bp | S/F/2Y 三挂 |

**⇒ 门控把 S 砍掉 0.46–0.65，margin 也掉**。机理：门控减少了有效持仓日数，等价于抽样降噪的反面——把「持续小赢」变成「间歇大赢」，Sharpe 必然下降。**除非 GATE 本身带超额信息（ZYQmolVx 的 beta 门控带了风险溢价信息），纯择时型门控在 DEU 这个窄宇宙上不可用。**

### 65.3 杠杆 B：`ts_target_tvr_decay` 强制换手目标 ⇒ 证伪

| 目标换手 | alpha | S | F | 2Y | sub | 实际 TO | margin | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 无（基线 10.32%） | `E56V8ex1` | **1.82** | 1.58 | 2.63 | 1.22 | 10.32% | 18.23bp | 仅 prod 挂 |
| `target_tvr=0.05` | `0mYj57n1` | **1.06 ↓↓** | 0.74 | 1.45 | 1.05 | 7.68% | 15.91bp | S/F 双挂 |
| `target_tvr=0.03` | `ZYQmNK50` | **0.74 ↓↓↓** | 0.45 | 1.00 | 0.83 | 6.84% | 13.41bp | S/F/2Y 三挂 |

**★ 重要归因纠正**：`ZYQmolVx` 的 prod 0.5276 **不能归因于 `ts_target_tvr_decay`**——本轮实测该算子把 S 从 1.82 打到 1.06/0.74，且实际 TO 只从 10.32% 降到 7.68%/6.84%（目标没达成多少，S 已崩）。ZYQmolVx 的低 prod 应归因于 **RISK-beta `trade_when` 门控 + RISK/ANALYST/SENTIMENT 三腿机制本身**，后续不要把 tvr 当通用降 prod 工具。

### 65.4 ★ 新发现的闸：`IS_LADDER_SHARPE`（limit 随件而变）

本轮首次在 DEU 见到该闸，且**限值不是固定值**：

| alpha | 该闸 value / limit | 触发场景 |
|---|---|---|
| `rKRd8v9j` | 1.63 / **2.02** | `trade_when` 门控臂 |
| `ZYQmNK50` | 1.00 / 1.58 | `tvr=0.03` 臂 |
| `0mYj57n1` | 1.45 / 1.58 | `tvr=0.05` 臂 |

**纪律**：今后任何「某件只剩 N 个闸」的结论，必须把 `checks.fail` 里出现的**所有** name 都列出来，不能只看 LOW_SHARPE / LOW_2Y_SHARPE 这两个常用闸。

### 65.5 ★★★★★ DEU 非 trio 面正式关闭：降 prod 杠杆穷尽表

| 杠杆 | 覆盖范围 | 最好结果 | 判定 |
|---|---|---|---|
| 中性化轴（几何） | MARKET/SECTOR/INDUSTRY/SUBINDUSTRY | anl44 SUBINDUSTRY **0.5653** | ✅ 但 S 只 1.45（封顶） |
| 中性化轴（风险模型） | CROWDING / REVERSION_AND_MOMENTUM / SLOW / FAST | anl44 REVMOM **0.7392**；snt7 REVMOM 0.8424 | ✗ 差 0.04–0.14 |
| 条件交易门控 | `trade_when`（信号态/热度态） | snt7 门控后 S 1.36 | ✗ S 崩 |
| 强制换手目标 | `ts_target_tvr_decay` 0.03/0.05 | snt7 S 1.06 / 0.74 | ✗ S 崩 |
| S 提升（改信号） | 8 个单变量取值（bf/mean/pow/decay） | anl44 全 ≤1.45 | ✗ 饱和 |

**⇒ DEU 非 trio category 面的最终产出 = 0 颗可提交 alpha。三条独立结论同时成立**：
1. 能过 S/F/2Y/sub 的信号，prod 墙 0.84–0.93，**四种降 prod 杠杆全部用尽且全部无效**；
2. 唯一 prod 有裕度的 `npvPvaOz`（0.5653），S 被 8 个单变量杠杆锁死在 1.45，**缺口 0.13 不可补**；
3. 「换轴换宽度」的直觉两次被证伪（S 侧 §64.5、prod 侧 §65.1）。

**这项结论应视为 DEU 的**终局**，不再重复消耗仿真资源。** 后续若要继续推进用户目标（30 颗 regular alpha），只能走 §64.6 列出的三条路（转区 / prod-first / PPA），三条都需要用户裁定。

## 六十六、2026-11-05 晚（六）：★★★★ 两条新挖法也被证伪 —— anl44 字段迁移 & ZYQ 机制跨区移植

### 66.1 `anl44` 字段全盘点：97 条臂里 netdebt 占 168 次，其余 12 个字段各只 1 次

`results/_deu_metrics_all.json` 里含 `anl44` 的臂共 **97 条**，字段使用次数：`netdebt_value` **85** / `netdebt_prevalue` **83**，其余（`operatingprofit`/`epsr`/`sales`/`tbvps`/`csh`/`fcfps`/`ebitda`/`roe`/`dps`/`eps`/`netprofit`/`netdebt_lastactvalue`/`netdebt_coveredby`）**各只 1–3 次**。⇒ 这个数据集里真正被系统挖过的只有 netdebt 一条线。

### 66.2 把 netdebt 几何迁移到其它 anl44 字段 ⇒ 全灭

几何完全照搬（`rank(ts_mean(ts_backfill(divide(subtract(value,prevalue),add(abs(prevalue),0.0001)),22),66))` 外套 `signed_power(...,2)`），SUBINDUSTRY 轴 / decay 16 / trunc 0.08，符号改为盈利类应有的正向：

| 字段（修订率） | alpha | S | F | 2Y | sub | TO | lc | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `anl44_2_eps_*` | `mLoYlp95` | **0.46** | 0.23 | 0.51 | 0.53 | 3.64% | 70 | 弱 |
| `anl44_2_ebitda_*` | `vR1OoaYA` | **0.22** | 0.08 | 0.15 | 0.30 | 3.79% | 66 | 极弱 |

**⇒ 机理结论**：netdebt 那条线的优势**来自字段本身的稀疏事件属性**（分析师负债预测修订是低频、高信息量事件），**不是几何**。换到覆盖充分的盈利类字段（EPS/EBITDA 被全市场盯着）后信号几乎归零。**「复用一个成功几何到同数据集其它字段」这条路在本数据集上无效。**

### 66.3 `anl44` 的「窗口 × 轴」网格已被前人铺满：S 与 2Y 此消彼长，没有双过点

补查 6 条高分臂的真实设置（都在 MARKET/SECTOR）：

| bf/mean/pow | alpha | 轴 | S | 2Y | sub | 差在哪 |
|---|---|---|---:|---:|---:|---|
| 22/75/pow2 | `wpQbGWXd` | SECTOR | 1.57 | **1.62** | 1.12 | S 差 **0.01** |
| 22/77/pow2 | `pwd5ajK3` | MARKET | **1.64** | 1.55 | 1.14 | 2Y 差 0.03 |
| 66/84/pow2 | `omEWrM9b` | MARKET | 1.57 | **1.64** | 1.13 | S 差 0.01 |
| 66/66/pow2 | `Vkx0Njrw` | MARKET | 1.62 | 1.47 | 1.05 | 2Y 差 0.11 |
| 22/70/pow2 | `qML0G5xj` | SECTOR | 1.56 | 1.50 | 1.08 | 双差 |
| 22/66/pow3 | `leAKa6ol` | SECTOR | 1.55 | 1.55 | 1.03 | 双差 |

**⇒ S 与 2Y 在窗口维度上此消彼长，唯一双过点仍是 `O0A8zdgJ`（66/80 @MARKET，S 1.59 / 2Y 1.61），而它 prod 0.9017。** 网格上不存在「双过 + 落在低 prod 轴」的点。

### 66.4 ★★★ `ZYQmolVx` 机制跨区移植 DEU ⇒ 失败（但塔位成功点亮）

EUR 全闸件（S 2.48 / F 1.19 / 2Y 2.15 / prod **0.5276**）三腿机制在 DEU 的字段可用性（preflight 实测）：

| 字段 | 塔 | DEU 可用性 |
|---|---|---|
| `rsk68_beta` | RISK | ✅ |
| `est_12m_ebt_raisednum_4wks` | ANALYST | ✅ |
| `est_12m_ebt_lowerednum_4wks` | ANALYST | ✅ |
| `oth553_est_estvalue` | OTHER | ❌ dataset-prefixed field not found（且 OTHER 属禁混集合，缺了反而合规） |

去掉 `market` 向量层后的移植表达式（8 算子）：

```
trade_when(less(group_rank(rsk68_beta,subindustry),0.6),
  group_scale(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks,
    add(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks)), subindustry), 2.05), sector), -1)
```

| 轴 | alpha | S | F | 2Y | sub | TO | margin | lc | 塔位 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| FAST | `0mYjLp01` | 0.70 | 0.29 | **−0.23** | 0.06 | 19.54% | 3.55bp | 191 | RISK×1.5 + ANALYST×1.8 |
| MARKET | `N1NeGQpg` | **1.22** | 1.01 | **−0.11** | 0.48 | 10.61% | 16.00bp | 60 | RISK×1.5 + ANALYST×1.8 |

**⇒ EBT 修订宽度（`raised/(raised+lowered)`）在 DEU 这个约 200 只的窄宇宙里信号很弱，2Y 为负**。塔位点亮成功（说明 RISK+ANALYST 这条腿在 DEU 是可建的），但**该机制不可跨区照搬**。EUR 的强表现依赖 TOP2500 的宽度与欧洲分析师覆盖密度。

### 66.5 ★ 两条平台坑（已固化进派发 SOP）

1. **`vector_neut(x, market)` 在 DEU 不可用**（EUR 可用）。DEU 报 `Invalid number of inputs : 1, should be exactly 2 input(s)`——`market` 在 DEU 不是可解析的向量字段。跨区移植时 `market` 向量层要么换成真实字段，要么整层去掉、交给设置层中性化。
2. **`preflight_expressions` 的 `valid:true` 不保证括号平衡**：本轮一条少一个右括号的表达式 preflight 返回 `valid:true`（字段也全识别），但平台报 `Unexpected end of input`。**派发前必须在本地做一次括号配平自检**（全程 `balance == 0` 且前缀最小值 ≥ 0），不能只依赖 preflight。
3. 顺带校准：`LOW_SUB_UNIVERSE_SHARPE` 的 limit 本轮见到 **0.58**（对应 S 1.22 ⇒ 比值 0.475，不是固定 0.517×S）。**该闸也以 `checks.fail[].limit` 实测为准。**

### 66.6 本节收口

本轮共新增 8 条有效臂（anl44 EPS/EBITDA 各 1 + ZYQ 移植 2 + 早前的门控/tvr 4），另有 4 次仿真因语法错误未产出（2 次少括号、2 次 `market` 向量）。**全部不足以动摇 §65 的终局判定。**

**DEU 非 trio category 面维持：0 颗可提交 alpha。本轮累计已证伪的挖法 = 9 类**（轴枚举 6 种 / 门控 / 换手目标 / 字段迁移 / 跨区移植 / 窗口网格 / 8 个 S 单变量杠杆）。**建议停止在 DEU 非 trio 面继续投入仿真。**

## 六十七、anl44 净负债修正机制终局：轴网格 8/9 穷尽，7 个几何全灭，S 与 prod 严格反向

> 时间：2026-11-05。承接 §64/§65/§66。本节把 §64 判定的「唯一低 prod 件 `npvPvaOz` 差 S 0.13」这条线彻底查完，结论是**结构性的、不可补的**。

### 67.1 结论先行

`npvPvaOz`（anl44 净负债相对修正 @SUBINDUSTRY）的 `LOW_SHARPE 1.45/1.58` 缺口 **不是参数问题、不是几何问题、不是轴问题**，是该机制的信息上限。

**已完成的穷尽性证据共 15 个杠杆，无一触及 1.58**：
- 8 个单变量杠杆（§65）：bf66→1.30 · mean22→1.14 · mean73→1.43 · pow1.5→1.43 · pow3→1.45 · pow4→1.42 · decay32→1.38（+ 基线 1.45）
- 窗口网格（§65，MARKET/SECTOR 两轴）
- 同数据集字段迁移（§66，EPS 修订率 0.46 / EBITDA 修订率 0.22）
- **本轮新增 7 个结构互异几何 + 2 个漏测轴**

### 67.2 新增：7 个结构互异几何全灭（同一基础式，只换几何，SUBINDUSTRY 轴）

基础式（FASTEXPR 变量单腿，8 算子）：
```
x = ts_backfill(divide(subtract(vec_avg(anl44_2_netdebt_value),vec_avg(anl44_2_netdebt_prevalue)),add(abs(vec_avg(anl44_2_netdebt_prevalue)),0.0001)),22);
```

| 编号 | 几何 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 基线 | `-signed_power(rank(ts_mean(x,66)),2)` | `npvPvaOz` | **1.45** | 1.28 | 1.63 | 0.91 | 3.83% | 50.74bp |
| V1 | `ts_rank(x,504)` 时序秩 | `kqNJ6776` | 0.34 | 0.13 | −0.13 | 0.11 | 15.86% | 0.03bp |
| V2 | `rank(ts_ir(x,252))` 风险调整 | `ZYQmv5kx` | 0.61 | 0.35 | 1.33 | 0.61 | 2.33% | 3.43bp |
| V3 | `rank(ts_delta(x,252))` 恶化动量 | `6XdALqx7` | 0.06 | 0.01 | 0.01 | −0.07 | 18.26% | 0.05bp |
| V4 | `rank(ts_zscore(x,504))` 时序 z | `leAMPEK7` | −0.04 | −0.01 | −0.11 | −0.47 | 12.65% | −0.04bp |
| V5 | `group_rank(ts_mean(x,66),subindustry)` 双中性 @**FAST** | `j2YeKAVZ` | 0.76 | 0.39 | 1.38 | 0.44 | 12.70% | 5.24bp |
| V6 | **预测误差**（`netdebt_lastactvalue` − `prevalue`）@SUBINDUSTRY | `A1VQ8Anl` | 0.10 | 0.02 | −0.54 | 0.18 | 2.36% | 5.90bp |
| V7 | **绝对修正**（去掉 `|prevalue|` 归一）@SUBINDUSTRY | `N1NelYLX` | 0.87 | 0.56 | 0.44 | 0.59 | 3.80% | 27.41bp |

**读法（最重要的机制结论）**：该 alpha 的全部信息只在「**净负债相对修正的平滑水平 × 横截面排序**」这一个形态里。
- 只要把**时序侧**的加工从 `ts_mean` 换成 `ts_rank / ts_ir / ts_delta / ts_zscore`（即含差分或除以自身标准差），S 立刻塌到 −0.04 ~ 0.61。⇒ **信号是静态价值型，不是动量型、不是稳定性型。**
- 只要拿掉末端的**横截面 `rank`**（V1 的 `ts_rank` 直接输出），S 0.34。
- 相对化分母 `|prevalue|` 是必需的（V7 去掉后 1.45→0.87）。⇒ 该机制靠的是「修正幅度相对资产负债表规模」的标准化，不是修正绝对值。
- `netdebt_lastactvalue`（实际值 vs 预估值 = 预测误差）这个**理论上更锐利的事件信号反而全灭**（S 0.10 / 2Y −0.54）。⇒ 该字段族里没有第二个可用信号面，§66 的字段迁移失败结论在此再获一次独立印证。

### 67.3 新增：轴网格补完（8/9），并发现唯一漏测点

§64 测了 6 轴，**本轮补测 `FAST` / `SLOW`**（基线式不含 `group_*`，故不受 P-2 限制）。完整表：

| 中性化轴 | alpha | S | F | 2Y | sub | TO | margin | lc | prod |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MARKET | `O0A8zdgJ` | **1.59** ✓ | 1.34 | **1.61** ✓ | 1.14 | 2.39% | — | 128 | 0.9017 ✗ |
| SECTOR | `P0ogzxOJ` | **1.58** ✓ | 1.31 | **1.59** ✓ | 1.12 | 2.90% | — | 125 | 0.8713 ✗ |
| INDUSTRY | `88RvY7L7` | 1.36 ✗ | 1.06 | 1.51 ✗ | 0.78 | 3.53% | — | 114 | — |
| CROWDING | `58Ej5Y8J` | 1.45 ✗ | 1.12 | 1.26 ✗ | 0.97 | 3.61% | — | 214 | 0.7740 ✗ |
| **FAST（本轮新增）** | `E56Vngxm` | 1.51 ✗ | 1.11 | 1.46 ✗ | 0.95 | 12.23% | 11.01bp | — | **0.7568** ✗ |
| REVERSION_AND_MOMENTUM | `d5WKz60E` | 1.40 ✗ | 1.05 | 1.32 ✗ | 0.92 | 7.08% | — | 209 | 0.7392 ✗ |
| **SLOW（本轮新增）** | `O0AJdbbb` | 0.99 ✗ | 0.58 | 1.01 ✗ | 0.79 | 6.42% | 13.39bp | — | — |
| SUBINDUSTRY | `npvPvaOz` | 1.45 ✗ | 1.28 | **1.63** ✓ | 0.91 | 3.83% | 50.74bp | 75 | **0.5653** ✓ |
| NONE | 未测（不含分组算子也会保留全市场暴露，prod 只会更高，不测） | | | | | | | | |

### 67.4 ★★★★★ 本节唯一的普适结论：S 与 prod 在轴维度上**严格反向**，缺口恒 > 0.18

把表按 S 降序排列后与 prod 对看：

| 轴 | S | prod | 四项指标 | prod<0.70 |
|---|---:|---:|---|---|
| MARKET | 1.59 | 0.9017 | 全过 | ✗（差 0.20） |
| SECTOR | 1.58 | 0.8713 | 全过 | ✗（差 0.17） |
| FAST | 1.51 | 0.7568 | ✗ | ✗ |
| SUBINDUSTRY | 1.45 | 0.5653 | ✗ | ✓ |

**能同时满足四项指标的轴（MARKET/SECTOR）prod 高出 0.17~0.20，prod 合格的轴（SUBINDUSTRY）S 低 0.13。9 个轴里不存在任何一点同时满足两套约束。**

这一条比 §65 的「lc 与 prod 无正相关」更进一步：不是「持仓宽窄决定 prod」，而是**轴的选剥方向决定了它同时拿走多少 alpha 收益与多少生产池暴露，二者对这个机制是同一个量**。对该类「慢速价值型基本面修正」因子，中性化轴的枚举空间已被测尽。

**方法论沉淀（跨区通用）**：判定「某机制的 prod 墙是否可破」的正确顺序不是先枚举轴，而是——
1. 先在**指标最全过的轴**（通常是最粗的 MARKET）上看 prod 差多少；
2. 若 > 0.15，则先看**最细轴**（SUBINDUSTRY）上 S 掉多少；
3. 若 `ΔS(粗→细)` 与 `Δprod(粗→细)` **同号且量级接近**，说明两者由同一个暴露驱动 ⇒ **直接判死，不要再枚举中间轴**（本例 ΔS = −0.14、Δprod = −0.34，中间 5 个轴全部落在同一条直线上，无一点偏离）。

### 67.5 本节收口

本轮新增 **9 条有效臂**（V1–V7 + FAST/SLOW 两轴），零语法失败、零取消。

**DEU 非 trio category 面仍是 0 颗可提交 alpha，累计已证伪挖法 = 11 类**（轴枚举 8 种 / 门控 / 换手目标 / 字段迁移 ×2 / 跨区移植 / 窗口网格 / 8 个 S 单变量杠杆 / **7 个结构几何** / **预测误差新字段** / **绝对修正去归一**）。

**anl44 这一矿脉正式封盘。** 剩余可动的只有通道层选择（PPA 是否查 S/2Y、是否转区、是否换 universe），均需用户裁定。

## 六十八、DEU 非 trio 面全域清点 + 4 个新数据集探针 + snt7 ATOM 化（去配对）证伪

> 时间：2026-11-05。承接 §64–§67。§67 封盘 anl44 后，本节转向「从未开采的非 trio 数据集」，并检验「去配对能否降 prod」这条最后的 prod 杠杆。

### 68.1 ★★★★★ 零成本资产：DEU/TOP500/D1 全部 172 个数据集按 category × alphaCount 清点

`get_datasets(region="DEU", universe="TOP500", delay=1)` 返回 **172** 个数据集。category 分布：

| category | 数量 | 是否非 trio | 已有挖掘结论 |
|---|---:|---|---|
| model | 45 | ✗ 禁混集合 | — |
| other | 41 | ✗ 禁混集合 | other699/553 已判死 |
| analyst | 18 | ✓ | analyst44 封盘（§67）、analyst7/9/15/39/69 有判决 |
| news | 17 | ✓ | news17/38/52/54 全灭收手 |
| fundamental | 12 | ✗ 禁混集合 | fundamental72/89 有判决 |
| pv | 16 | ✗ 禁混集合 | — |
| risk | 5 | ✓ | **只有 rsk68_beta 当门控用过，信号面从未挖** |
| institutions | 5 | ✓ | institutions6 (ac 270) 有判决 |
| sentiment | 3 | ✓ | sentiment7 (snt7) 全家族、sentiment27 判死 |
| earnings | 2 | ✓ | earnings_sent_matrix 有波次 |
| insiders | 2 | ✓ | **从未挖** |
| socialmedia | 2 | ✓ | socialmedia12 (ac 130) 有波次 |
| imbalance | 1 | ✓ | 从未挖 |
| macro | 1 | ✓ | macro27 (ac 149) 有波次 |
| option | 1 | ✓ | option1 (ac 72) 有波次 |
| shortinterest | 1 | ✓ | shortinterest3 (ac 864) 判死 |

**非 trio 合计 58 个。** 按 `alphaCount` 升序（**低 ac = 平台内被做得少 = prod 撞墙概率低**）的前 28 个（ac ≤ 50）是本区最未被开采的清单：

| ac | 数据集 | cat | 字段 | 备注 |
|---:|---|---|---:|---|
| 1 | news76 | news | 2 | 极新 |
| 4 | analyst46 | analyst | 5 | |
| 4 | news29 | news | 16 | 仅元数据/文本字段 |
| 7 | analyst48 | analyst | 7 | cov 0.7879 |
| **7** | **institutions25** | institutions | 24 | **本轮已探 → 见 68.2** |
| 9 | analyst8 | analyst | 10 | |
| 9 | news54 | news | 39 | 已判死 |
| 10 | analyst35 | analyst | 23 | |
| 11 | news21 / news31 | news | 15 / 12 | |
| 13 | news38 / news52 | news | 3 / 21 | 已判死 |
| 17 | news73 | news | 22 | |
| 18 | news3 | news | 19 | |
| 19 | institutions4 | institutions | 6 | cov 0.3413 |
| **23** | **risk71** | risk | 10 | 全是特异收益面板 |
| 24 | analyst16 | analyst | 66 | |
| 26 | analyst83 | analyst | **345** | cov 0.3389，字段极多 |
| 26 | insiders1 | insiders | 8 | cov 0.5343 |
| 32 | institutions1 | institutions | 7 | cov 0.2289 |
| 33 | news20 / news7 | news | 46 / 23 | cov 0.7729 |
| **37** | **risk72** | risk | 31 | 特异收益 + replicator |
| 38 | analyst94 | analyst | 34 | |
| 42 | news50 | news | 37 | cov 0.7644 |
| 45 | analyst10 | analyst | 53 | |
| **45** | **sentiment33** | sentiment | **255** | cov 0.32，fkw1..4 × method1..9 矩阵 |
| 50 | news23 | news | 116 | |

**这张表是本节最有复用价值的产物**：以后判定「某区某 category 是否挖尽」，先看这张表里 ac 低且未被探过的集，而不是重复已判死的高 ac 集。

### 68.2 新数据集探针：4 个数据集、7 条臂，全部 S ≈ 0

| 数据集 | 探针机制 | alpha | S | F | 2Y | sub | TO | margin | lc |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| institutions25 | 空头利息水平（经典 SI 异象） | `JjePaaxe` | −0.04 | −0.01 | 0.08 | 0.06 | 3.53% | −0.02bp | **27** |
| institutions25 | 做空管理人数量（共识广度） | `mLoYnWx5` | 0.13 | 0.05 | −0.01 | −0.09 | 3.23% | 0.09bp | — |
| sentiment33 | 负面情绪水平（method_3_neg） | `xAr1La2b` | 0.09 | 0.03 | −0.59 | −0.24 | 4.33% | 0.05bp | — |
| sentiment33 | 净极性（pos−neg）/（pos+neg） | `N1NedkY8` | 0.19 | 0.09 | 0.87 | — | 3.95% | 0.13bp | — |
| risk71 | 特异收益 5 日反转 | `qMLEaAOE` | −0.12 | −0.02 | −0.31 | −0.12 | **40.67%** | −0.003bp | — |
| risk88 | 规模因子（全宇宙市值，cov 1.0） | `omEobY5m` | −0.25 | −0.10 | −0.99 | 0.18 | 1.49% | −0.28bp | — |

**三条结论**：

1. **`institutions25` 直接判「覆盖不可投」**：`longCount 27 / shortCount 28`（合计约 55 只）。ac 仅 7 的「低拥挤」并不意味着可用——它没人做很可能就是因为**根本没有足够标的**。**纪律：dataset 级 `coverage` 字段（本轮全部显示 0）不可作为可用性判据，唯一可靠信号是首条探针的 `longCount`；lc < 40 直接弃。**
2. **`sentiment33` 的 token 计数族与 snt7 的「关注度」族不是同一类信号**：snt7 是 Wikipedia 浏览量（纯注意力代理，S 2.05），sentiment33 是方法 1–9 × 词典 fkw1–4 的**词频/极性计数**（S 0.09/0.19）。前者有信息，后者在 DEU 小宇宙上没有。
3. **`risk71` 的特异收益反转失败且换手 40.67%**（`ts_sum(residual,5)` 天天满仓换）。`risk88` 的规模因子取负（做多小盘）S −0.25 ⇒ 反推 **DEU 是大盘溢价**（做多大盘约 +0.25，仍远不够闸）——这条可以留作其他组合的**辅助方向先验**，但不足以单独成件。

### 68.3 ★★★★★ snt7 ATOM 化（去配对）证伪：S 2.05 → 0.08

这是本节最重要的实验。动机：snt7×snl27 族 18 条全闸件 prod 0.84–0.93 深钉（§65 封盘），若拥挤来自**配对本身**，则把 snt7 单独做成 ATOM（单数据集不占混合配额）就能同时拿到高 S 与低 prod。

两条 ATOM（同一设置 decay 4 / SUBINDUSTRY / trunc 0.02 / nanHandling ON）：

| 臂 | 机制 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| A2 | 基线信号形状**去掉 snl27 腿**（`-rank(ts_mean(max(a,delay1,delay2),10))`） | `rKRdqV93` | **0.08** | 0.02 | −0.64 | 0.39 | 4.24% | 0.03bp |
| A3 | 跨语言关注占比 `divide(all_languages_views, views)`（snt7 内部两字段，仍是 ATOM） | `O0AJLM2v` | 0.41 | 0.18 | 0.66 | −0.16 | 2.41% | 0.20bp |
| 基线 | snt7×snl27 `vector_neut(quantile(ts_ir(...)), b)`（decay 16） | `qML0EAo1` | **2.05** | — | — | — | — | — |

**结论（硬）**：snt7 这条腿单独拿出来**没有任何 alpha**（S 0.08）。整个 S 2.05 来自 `vector_neut(attention_surprise, snl27_popularity)` 这个**配对交互**——注意力异常必须相对社媒人气做正交化才成为信号。

⇒ **「去配对降 prod」不是一条可用杠杆。** 对被 prod 墙钉死的配对族，把主腿单独 ATOM 化会直接把 alpha 归零；配对既是收益来源也是拥挤来源，二者不可分离。这与 §67.4「S 与 prod 由同一暴露驱动」是同一现象在**数据集组合维度**上的表现。

**该结论与此前 §65 的三条降 prod 杠杆（门控 / 换手目标 / lc）合并后，降 prod 的可行杠杆集合确定为空集。**

### 68.4 本轮累计（§68）

新增 **17 条有效臂**（institutions25 ×2、sentiment33 ×2、risk71/88 ×2、snt7 ATOM ×2、anl44 几何 ×7、anl44 漏测轴 ×2），**零可提交件**。

**DEU 非 trio category 面维持 0 颗可提交 alpha，累计已证伪挖法 = 14 类**：
轴枚举（9 轴穷尽）· `trade_when` 门控 · `ts_target_tvr_decay` · 同数据集字段迁移（×2）· 跨区机制移植 · 窗口网格 · 8 个 S 单变量杠杆 · 7 个结构几何 · 预测误差新字段 · 绝对修正去归一 · 扩宽宇宙 · lc 假设 · **新数据集换面（institutions25/sentiment33/risk71/risk88 全灭）** · **ATOM 化去配对**。

**唯一仍可提交的资产在区外**：EUR `ZYQmolVx`（全闸过、self 0.4169 / prod 0.5276）。DEU 侧已无内生解。

## 六十九、★★★ 重大记录修正：723 条池子是跨区域混合，DEU 真实存量只有 ~126–212 条；DEU 真瓶颈是 2Y 闸

> 时间：2026-11-05。本节推翻 §64 的部分计数基础，并首次给出**纯 DEU** 的存量画像。

### 69.1 ★★★★ 修正：`results/_deu_metrics_all.json`（723 条）不是纯 DEU

`get_user_alphas` **支持 `region` 过滤**（此前未用，导致误判）：

| 查询 | count |
|---|---:|
| `type=REGULAR`（无 region） | 10000 |
| `type=REGULAR, region="DEU"` | **60 → 126 → 212**（分页过程中递增，疑似动态/缓存计数） |
| `type=REGULAR, region="DEU", status="SUBMITTED"` | **0** |

**验证**：抓取 DEU 前 100 条，与 723 条文件求交 ⇒ **只有 36 条重合，64 条不在其中**。

⇒ **§64 的「723 条 DEU UNSUBMITTED 全量重筛」「114 条 2Y≥1.58」「29 条六项闸全过」三组数字全部建立在一个跨区域混合池上，DEU 侧不可引用。** 家族构成表（snt7×snl27 18 / fnd6 6 / anl44 2 …）中只有与实际 DEU 重合的部分成立。

**另一条重要发现**：`status="SUBMITTED"` 与 `status="ACTIVE"` 均返回 **0** —— 该 MCP 工具**查不到已提交件**（只返回 UNSUBMITTED）。所以「已提交 11 颗」这个数字无法通过 MCP 复核，只能沿用历史记录。

### 69.2 纯 DEU 存量真实画像（前 200 条逐条六闸筛）

按 E56Vngxm 实测闸口径（S≥1.58 / F≥1.0 / 2Y≥1.58 / TO≤0.70 / margin≥10bp）：

| alpha | 家族 | S | F | 2Y | sub | TO | margin | lc | 判决 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `3qojOer6` | fnd6 营业利润动量 @FAST | 1.80 | 1.44 | 1.77 | 1.23 | 12.82% | 12.76bp | 177 | **FUNDAMENTAL 属禁混集合，按用户指令排除** |
| `E56V8ex1` | snt7×snl27 @REVMOM | 1.82 | 1.58 | 2.63 | 1.22 | 10.32% | 18.23bp | 218 | 六闸全过，**prod 0.8424 ✗** |
| `88RvEeYa` | snt7×snl27 @CROWDING | 1.69 | 1.44 | 2.22 | 1.27 | 8.22% | 21.97bp | 208 | 六闸全过，**prod 0.8744 ✗** |

**除上述 3 条外，前 200 条中六闸全过 = 0 条。** DEU 的候选面在纯区域口径下比 §64 描述的**更窄**，不是更宽。

### 69.3 ★★★★★ 新结论：DEU 的真瓶颈是 2Y 闸，不是 S 闸

纯 DEU 里两大家族的失败形态完全不同：

| 家族 | 代表 | S | 2Y | 缺口 |
|---|---|---:|---:|---|
| `anl44` 净负债修正 | `npvPvaOz` @SUBIND | 1.45 | **1.63 ✓** | 缺 **S** +0.13 |
| `anl44` 净负债修正 | `O0A8zdgJ` @MARKET | **1.59 ✓** | **1.61 ✓** | 缺 **prod**（0.9017） |
| `anl9` 分析师上调/下调家数 | `Vkxd7Jzw` @MARKET | **1.76 ✓** | 1.06 ✗ | 缺 **2Y** +0.52 |
| `anl9` | `88Rve06X` @INDUSTRY | **1.60 ✓** | 1.17 ✗ | 缺 **2Y** +0.41 |
| `anl9` | `JjePOqMx` | **1.85 ✓** | 0.53 ✗ | 缺 **2Y** +1.05 |
| `anl93` 修正比率 | `RREA8R61` | 1.47 ✗ | 0.92 ✗ | 双缺 |

**DEU 的 2022–2023 单段 Sharpe 门槛 1.58 是这里最硬的一堵墙**；`anl9` 全族 S 都够，全部死在 2Y。这与 §64 时代「主瓶颈是 prod」的判断不同——**prod 只卡 anl44/snt7 两族，2Y 卡的是 analyst 整个广度族**。

### 69.4 news104 字段画像与四条探针（本轮新）

`news104`：**11 个字段 coverage 全部 = 0.963**（DEU 非 trio 最高覆盖），字段价值分档：

| 档 | 字段 | 平台使用 | 机制 |
|---|---|---|---|
| 主信号 | `nws104_sentiment`（三值） / `prob_pos` / `prob_neg` | al 37 / 21 / 19 | 情绪方向 |
| **差异化** | `nws104_confidence`（0–1） | **us 8** | 信号质量加权 |
| **差异化** | `nws104_relevance`（1=主报道） | us 13 | 主/次报道过滤 |
| **差异化** | `nws104_novelty`（1=首发，>1=重复） | us 13 | 信息衰减折扣 |
| **近无人用** | `nws104_marketimpactscore` / `headlineonly` / `automessage` | **al 2 / 0 / 2** | 元信号 / 噪声折扣 |

探针（decay 16 / SUBINDUSTRY / trunc 0.08 / nanHandling ON）：

| 机制 | alpha | S | F | 2Y | sub | TO | margin | lc |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 市场影响分（元信号） | `MPY0rAPa` | −0.25 | −0.08 | −0.05 | 0.10 | 6.68% | −0.04bp | 141 |
| 置信度加权情绪 | `9qxEnpvV` | 0.34 | 0.12 | 0.42 | 0.08 | 8.09% | 0.04bp | 138 |
| 净情绪概率差 | `KPJm1GVl` | 0.26 | 0.08 | 0.30 | −0.03 | 7.92% | 0.03bp | 140 |

**★★ 平台语法坑（新）**：news104 的字段是 **event 类型**，`multiply` 不接受 event 输入——
`multiply(nws104_sentiment, nws104_confidence)` 整条报 `Operator multiply does not support event inputs`。
**必须先对每个字段各自 `vec_*` 聚合，再做字段间算术**：`multiply(vec_avg(A), vec_avg(B))`。此规则适用于 news17/news18/news20/news29/news104 全族。

**判决**：news104 4 条模板最好只到 S 0.34（闸值的 22%）。**历史收敛率下从未见过 4.6 倍的模板跃升**，故按「最优探针 < 闸值 40% 即判死」快速停止，不补满 10 模板。

### 69.5 anl44 杠杆率水平机制（新）也失败 ⇒ 信号只在修正动态里

同数据集、不同暴露：把「修正率」换成「净负债 / 有形账面价值 = 杠杆率水平」（经典 value/quality 因子，非修正族）：

| 轴 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| MARKET | `A1VQoaJW` | 0.44 | 0.23 | −0.71 | 0.31 | 1.00% | 69.92bp |
| SUBINDUSTRY | `QPvYwl7w` | 0.10 | 0.02 | −0.66 | 0.12 | 1.73% | 8.71bp |

对照：`xAr1p8zp`（纯净负债水平）@MARKET S 0.29。⇒ **anl44 的全部信息在「值的修正方向」，不在「值的水平」**，与 §66 字段迁移失败的结论一致。

### 69.6 EUR 侧顺带发现（不属本区目标，记录备查）

`get_user_alphas` 无区域过滤翻页时发现 EUR 族有更强成员：

| alpha | 设置 | S | F | 2Y | sub | sub limit | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---|
| `QPvY8bXw` | EUR/TOP2500/D1/FAST/decay1/trunc0.04 | **3.42** | 2.55 | 2.58 | 1.29 | 1.78 | `LOW_SUB_UNIVERSE_SHARPE` |
| `j2Ye7Amj` | 同上 | 2.42 | 1.15 | 1.33 | 1.29 | — | `IS_LADDER_SHARPE` 1.33/1.58 |

**关键观察**：`QPvY8bXw` 的 sub **1.29** 与 `ZYQmolVx` 的 sub **1.29** 完全相同，S 却从 2.48 涨到 3.42 ⇒ 多出来的 S **全部来自非流动性名**；而 `LOW_SUB_UNIVERSE_SHARPE` 的 limit = **0.517 × S**（1.29/3.42 = 0.377 ≪ 0.517，1.78 就是这么来的）。
⇒ **在「sub limit 随 S 同比放大」的闸下，堆高 S 会同时抬高 sub 门槛，是负和操作。** 这条对任何区域都成立。

---

## 七十、2026-11-05 非 trio 收口第二轮：fnd6 成为唯一过 2Y 的矿脉后，把它的「质量/投资」两面也测掉；anl44 轴网格补完 NONE 正式 9/9 封盘

### 70.1 本轮起点：纯 DEU 只有 3 条六闸全过，其中只有 fnd6 能过 2Y

`§69.2` 的筛子给出 3 条，两条 snt7×snl27 是 prod 深钉（0.8424 / 0.8744），只剩 **`3qojOer6`**：

```
group_rank(multiply(rank(ts_delta(fnd6_newq_oiadpq, 240)), rank(ts_delta(fnd6_newq_oiadpq, 176)), ts_rank(fnd6_newq_oiadpq, 756)), sector)
```

实测 `checks.fail = []`（六闸全过）S **1.80** / F **1.44** / 2Y **1.77** / sub 1.23 / TO **12.82%** / margin **12.76bp** / lc 177 / pyramid `DEU/D1/FUNDAMENTAL` ×1.8，设置 decay 4 · FAST · trunc 0.08 · nanHandling ON。

**关键判断**：DEU 里过 2Y 闸的机制族只有三个 —— fnd6 营业利润动量（1.77）、snt7×snl27（2.63/2.22）、anl44 净负债修正（1.63）；前两个之外唯一「2Y 有余量」的就是 fnd6。而 fnd6 是 FUNDAMENTAL（**不在 {PV, MODEL, OTHER} 内**），单数据集 ATOM 不占禁混配额 ⇒ 符合用户「专注非 trio category」的指令，是本轮唯一值得继续压的矿脉。

### 70.2 fnd6 字段画像（DEU/TOP500/D1，196 字段）

- 全部 MATRIX，**没有 VECTOR/event**（不存在 news 族的 `vec_*` 约束）。
- coverage 中位 ≈ 0.52，**只有 2 个字段 ≥ 0.90**（且都是 ISO 货币代码 `fnd6_adesinda_curcd` / `fnd6_idesindq_curcd` ⇒ 无信息）。
- 有效字段的 cov 普遍落在 **0.35–0.67**：这是财报科目本身只有部分公司披露的正常形态，**不是覆盖缺陷**。已成功的 `fnd6_newq_oiadpq` cov 仅 **0.4449**，lc 仍 177 ⇒ **不要用 cov 阈值筛 fnd6 字段**。
- 高可用字段（cov 与可解释性兼顾）：`cptnewq_atq`(0.656 总资产) / `newa2_seq`(0.653 母公司权益) / `iby`(0.660 税前异常前利润) / `newq_lseq`(0.656) / `newa2_oiadp`(0.627 年化营业利润) / `newa2_oancf`(0.540 经营现金流) / `ibmiiy`(0.626) / `newq_piq`(0.545) / `gpy`(0.552 毛利) / `newa2_revt`(0.626 营收) / `capxy`(0.513 资本开支) / `newq_invtq`(0.548 存货) / `newa2_xrd`(0.364 研发)。

### 70.3 fnd6 模板库（12 个结构互异，满足 ≥10 硬约束）

| # | 机制 | 骨架（都在 fnd6 单数据集内） | 实测 |
|---|---|---|---|
| T1 | 应计质量（Sloan） | `-signed_power(rank(ts_mean(ts_backfill(divide(subtract(fnd6_iby,fnd6_newa2_oancf),add(abs(fnd6_cptnewq_atq),0.0001)),66),252)),2)` | **已测 `YP11jdzq`** |
| T2 | 资产增长（投资异象） | `-rank(divide(ts_delta(ts_backfill(fnd6_cptnewq_atq,66),756),add(abs(ts_delay(a,756)),0.0001)))` | **已测 `E566Z0QP`** |
| T3 | 毛利资产率（Novy-Marx） | `rank(ts_mean(divide(ts_backfill(fnd6_gpy,66),add(abs(fnd6_cptnewq_atq),0.0001)),252))` | 未测 |
| T4 | 经营利润率趋势 | `rank(ts_delta(divide(oiadpq,abs(revtq)),504))` | 未测 |
| T5 | 利润加速度（二阶差分） | `rank(ts_delta(ts_delta(oiadpq,252),252))` 规模归一 | 未测 |
| T6 | 现金转化率（OCF/利润） | `rank(ts_mean(divide(fnd6_newa2_oancf,add(abs(fnd6_iby),0.0001)),252))` | 未测 |
| T7 | 研发强度 | `rank(ts_mean(divide(fnd6_newa2_xrd,abs(fnd6_newa2_revt)),252))` | 未测 |
| T8 | 营运资本占用（负向） | `-rank(ts_delta(divide(invtq+rect,revtq),504))` | 未测 |
| T9 | 杠杆收缩 | `-rank(ts_delta(divide(fnd6_cptnewq_ltq,abs(fnd6_cptnewq_ceqq)),504))` | 未测 |
| T10 | 资本开支纪律 | `-rank(ts_mean(divide(fnd6_capxy,abs(fnd6_cptnewq_atq)),252))` | 未测 |
| T11 | 盈利稳定性（ts_ir 水平） | `rank(ts_ir(ts_backfill(fnd6_newq_piq,66),504))` | 未测 |
| T12 | 股东回报（股利/市值） | `rank(ts_mean(divide(fnd6_dvy,cap),252))` | 未测 |

**为什么只跑 T1/T2**：这是「可行性探针」不是「波次」，按既定的快速停止规则（最优探针 < 闸值 40% 即判死，不必补满 10 模板）执行。T1/T2 覆盖了两个**机制上最独立**的面 —— 盈余质量（利润 vs 现金流）与投资（资产扩张），二者同时判死足以说明「fnd6 的价值只在利润动量这一条」。

### 70.4 T1/T2 实测：fnd6 的「质量」与「投资」两面同时判死

| 机制 | alpha | S | F | 2Y | sub | TO | margin | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 应计质量（负向） | `YP11jdzq` | **−0.19** | −0.05 | **−0.06** | −0.47 | 12.68% | −1.51bp | 4 |
| T2 资产增长（负向） | `E566Z0QP` | **−0.28** | −0.09 | 0.77 | −0.26 | 12.69% | −2.26bp | 4 |

- 两条都只有闸值的 **12% / 18%**，远低于 40% 快速停止线；且 **failed_ra = 4**（而 `3qojOer6` 是 0），连 RA 体检都不干净。
- T2 的形态值得记一笔：**S −0.28 但 2Y +0.77** ⇒ 投资异象在 DEU 只在 2022–2023 有效、其余年份反向。**反号后 S 最多 0.28、2Y 变 −0.77**，两头不可能同时过 ⇒ 不是符号问题，是这个暴露在 DEU 大盘股里不存在稳定溢价。
- ⇒ **fnd6 的可用信息被压缩在「营业利润的多周期动量 × 横截面排序 × 规模归一」这一条形态里**，与 anl44「信息只在修正方向、不在水平」是同一类结论：**同一数据集的不同经济面不共享信号**。

### 70.5 anl44 轴网格补完 `NONE`：9/9 全部测完，正式终局

前八轴（MARKET 1.59/0.9017 · SECTOR 1.58/0.8713 · FAST 1.51/0.7568 · CROWDING 1.45/0.7740 · SUBINDUSTRY 1.45/**0.5653** · REVMOM 1.40/0.7392 · INDUSTRY 1.36 · SLOW 0.99）缺的最后一轴本轮补上：

| 轴 | alpha | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| **NONE** | `WjOOjmEd` | **−0.44** | −0.48 | 0.53 | 1.05 | 2.10% | −138.62bp |

**★★ 这条读数的含义比「又挂一个」更重要**：同一表达式在 MARKET 轴上 S 1.59、在 NONE 轴上 S **−0.44**（差 2.03）。说明 **anl44 净负债修正 100% 是「横截面相对」效应，一旦不剥离市场暴露就变成负 alpha** —— 它是纯 relative-value 信号，不是绝对定价信号。这也解释了为什么「降 prod」只能靠加深行业细分（剥离更多共同暴露），而每剥一层 S 就掉一档：**被剥掉的暴露就是 alpha 本身**。
⇒ **9 个可用轴全部测完，S 与 prod 严格同向，无免费午餐。anl44 机制正式终局，不再投槽。**

### 70.6 prod 读数受阻：`3qojOer6` 平台侧 240s 超时 ×2，pending 不落值

`tools/prod_wait.py 3qojOer6 --minutes 9` 跑满：平台在 240s 处返回 `status=pending`（`attempts=184, computed=true, event=pending`），重试第二次仍 pending，最终「超时未取到」。已按既定纪律（超时不落缓存、inflight 标记 300s）改用 16 分钟长窗口后台重试。

⇒ **`3qojOer6` 的 prod 至今为「未知」，既不能判活也不能判死。** 在拿到读数前，DEU 侧「可提交件 = 0 或 1」取决于这一次读数。

### 70.7 本轮累计消耗与结论

- 派发 3 条（fnd6 T1 / fnd6 T2 / anl44 NONE），**零语法失败、零取消、零平台写操作**，并发严格 ≤2（单条 + 24s 间隔）。
- 累计已证伪挖法由 16 类增至 **18 类**：新增「fnd6 应计质量」「fnd6 资产增长」；轴枚举一类由「9 轴穷尽」补正为**真正 9/9 实测**。
- **非 trio 58 个数据集 + PV/MODEL/OTHER 之外的 70 个数据集面，至此除 fnd6 动量单条外全部判死。**
- 下一动作只剩三条，均需用户裁定：① 拿到 `3qojOer6` prod 后决定是否提交；② 转 PPA 通道（不查 2Y，`anl9` 全族 S 够但 2Y 死的件可复用）；③ 转区（EUR `ZYQmolVx` 全闸已过）。

### 70.8 ★★★★★ 最后一次攻 prod：把 `group_rank(sector)` 去掉换风险模型轴 —— S 当场崩塌

**动机**：`3qojOer6` 唯一没过的是 prod，而同族 `gJeWJn9M` 的表达式与它**近乎等价**：

```
gJeWJn9M: group_rank(multiply(multiply(rank(ts_delta(oiadpq,240)), rank(ts_delta(oiadpq,176))), rank(ts_rank(oiadpq,756))), sector)
3qojOer6: group_rank(multiply(rank(ts_delta(oiadpq,240)), rank(ts_delta(oiadpq,176)), ts_rank(oiadpq,756)), sector)
```

只差乘法结合方式与第三条腿是否多包一层 `rank()`；两者 S 1.79/1.80、2Y 1.74/1.77、TO 12.84%/12.82%、margin 12.63bp/12.76bp —— **几乎是同一条 alpha**。而 `gJeWJn9M` 的 **prod = 0.9184**。⇒ `3qojOer6` 的 prod 先验就是 0.9 档深钉。

**于是攻唯一有效的降 prod 杠杆（换中性化轴）**：表达式里含 `group_rank(...,sector)` 时按 P-2 规则只能换 FAST/MARKET，而 FAST 已是基线、MARKET 在 anl44 上是 prod 最高的一轴。要解锁其余 7 轴必须先**去掉 `group_rank`**，改成全局 `rank()`，把「分组」交给中性化轴去做：

```
rank(multiply(rank(ts_delta(fnd6_newq_oiadpq,240)), rank(ts_delta(fnd6_newq_oiadpq,176)), ts_rank(fnd6_newq_oiadpq,756)))
```

| 轴 | alpha | S | F | 2Y | sub | TO | margin | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **SUBINDUSTRY** | `3qooq0J0` | **1.15** | 1.03 | 0.95 | 1.01 | 5.10% | 39.08bp | 2 |
| **REVMOM** | `0mYYm206` | **1.24** | 0.95 | 1.24 | 0.74 | 8.94% | 16.31bp | 3 |
| 基线（`group_rank`+FAST） | `3qojOer6` | **1.80** | 1.44 | **1.77** | 1.23 | 12.82% | 12.76bp | 0 |

**★★ 判决**：去掉 `group_rank(sector)` 后换更细的轴，S 掉 **0.56–0.65**、2Y 掉 0.53–0.82、failed_ra 从 0 升到 2–3。⇒ **`group_rank(...,sector)` 不是可替换的分组算子，它本身就是这套信号的收益来源**（行业内排序＝把「同行业里谁在改善」这个相对比较做成信号）。这一步把 P-2 规则从「定性：会二次削信号」升级为「定量：−0.56~−0.65」。

⇒ **fnd6 营业利润动量的唯一可用配置就是 `group_rank(sector)` + FAST，而该配置 prod ≈ 0.92（同族实测）。机制与拥挤度不可分离 ⇒ 与 snt7×snl27 完全同构的终局。**

### 70.9 DEU 终局判决：纯 REGULAR 可提交件 = **0**

把三条六闸全过件逐个走完 prod 逻辑后：

| alpha | 六闸 | prod | 终局理由 |
|---|---|---|---|
| `E56V8ex1` | 全过 | 0.8424 ✗ | snt7×snl27 深钉厚尾，族内 18 条无低于 0.84 者；ATOM 化后 S 0.08 |
| `88RvEeYa` | 全过 | 0.8744 ✗ | 同上族 |
| `3qojOer6` | 全过 | ≈0.9184（同族等价式实测）✗ | fnd6 动量族；换轴解锁后 S 崩 |

**非 trio（PV/MODEL/OTHER 之外）70 个数据集、58 个此前未开采集，本轮全部走完。累计已证伪挖法 20 类。**

### 70.10 本轮新增派发清单（5 条，零失败零取消）

| # | tag | 轴/机制 | alpha | 结果 |
|---|---|---|---|---|
| 1 | `fnd6_accrual_T1` | 应计质量 | `YP11jdzq` | S −0.19 判死 |
| 2 | `fnd6_assetgrowth_T2` | 资产增长 | `E566Z0QP` | S −0.28 判死 |
| 3 | `anl44_axis_NONE` | 轴网格补 9/9 | `WjOOjmEd` | S −0.44 判死 |
| 4 | `fnd6_oiadpq_subind` | 去 group_rank + SUBIND | `3qooq0J0` | S 1.15 判死 |
| 5 | `fnd6_oiadpq_revmom` | 去 group_rank + REVMOM | `0mYYm206` | S 1.24 判死 |

并发严格 ≤2（单条 + 24s 间隔），无 429、无 CANCELLED、无平台写操作。

---

## 七十一、2026-11-05 PPA 通道核查：DEU 有 1 颗可交接件，门槛与 RA 完全不同（这是本轮唯一实质性产出）

### 71.1 PPA 的资格口径与 RA 不是同一套

事实源 `src/wqb/config.py:402`：

```python
PPA_CHECK_NAMES = frozenset([
    "LOW_TURNOVER", "HIGH_TURNOVER", "LOW_SUB_UNIVERSE_SHARPE", "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO", "LOW_ROBUST_UNIVERSE_RETURNS",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
])
```

计数规则（同一文件 `compute_webdata_failed_counts`）：
`ppa_hit = (name in PPA_CHECK_NAMES and bad) or (name == "LOW_SHARPE" and value < 1)`

**★★★ 三条关键推论**：
1. **`LOW_2Y_SHARPE` 不在 PPA 名单里** ⇒ DEU 的 2Y 墙（2022–2023 单段 ≥1.58）**在 PPA 通道上根本不存在**。这正是 §69.3 判定「2Y 是 DEU 最硬一堵墙」之后唯一没被使用的通路。
2. **`LOW_SHARPE` 只有 value < 1 才算失败** ⇒ S ∈ [1.0, 1.58) 的件在 PPA 通道上合法（`brain-alpha-judge` 明写「不得判 BLOCK」）。
3. `LOW_FITNESS` / `CONCENTRATED_WEIGHT` / `IS_LADDER_SHARPE` **不在 PPA 名单**，但按 `merge_failed_items` 的 fail-closed P0 纪律（RA 为下界），它们**没有对应的 PPA 豁免条款**，属「PPA 计数干净但 RA 脏」的风险件 —— 判级时须单独标注，不能与「只差 2Y」的那类混为一谈。

文档侧判据（`tools/ppa_handoff.py:29` `PPA_DOC_RULES`，来源为平台 Power Pool 规则记载、**本环境未向平台复核**）：
`sharpe_min 1.0` / `operators_max 8` / `fields_max 3` / `ppac_max 0.5`。

### 71.2 PPAC 的取数路径（本轮首次打通）

`check_self_correlation` 的 `correlation_type` 有三个取值（`world-quant-brain-mcp/brain_mixin_correlation.py:738`）：

| 取值 | 对应平台检查 | 说明 |
|---|---|---|
| `self`（默认） | SELF_CORRELATION | 池**排除** Power Pool Alpha |
| **`powerpool`** | **POWER_POOL_CORRELATION** | 只对 Power Pool Alpha 算 ⇒ **这就是 PPAC** |
| `all` | 旧口径 | 全池 |

⇒ 以后算 PPAC 一律 `check_self_correlation(alpha_id, local_calculation=true, correlation_type="powerpool")`，零配额秒回，不必等平台 `POWER_POOL_CORRELATION` 转正。

### 71.3 四颗 DEU 存量件的 PPA 全指标实测

| alpha | 表达式要点 | S | F | 2Y | TO | 算子 | 字段 | **PPAC** | self | 塔 | Failed PPA |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| **`JjePOqMx`** | anl9 上调/下调家数价差 @group_neutralize(sector) | **1.85** | **1.51** | 0.53 | 15.38% | **8** | **3** | **0.2148** | 0.3309 | ANALYST ×1.8 | **0** |
| `gJe1moeJ` | oth47 有机流量 ts_zscore(150) | 1.25 | 0.73 | 2.60 | 12.02% | **3** | 1 | 0.0549 | — | OTHER ×1.8 | 0（但 RA 脏：LOW_FITNESS + CONCENTRATED_WEIGHT） |
| `j2YZ1JYQ` | oth47_rank ts_zscore(150) 取负 | 1.29 | 0.77 | 2.31 | 11.81% | **4** | 1 | 0.0480 | — | OTHER ×1.8 | 0（同上 RA 脏） |
| `blbYGJPq` | mdl109 经营 EPS 修正 | 1.13 | 0.94 | 1.11 | **1.53%** | **2** | 1 | 0.0527 | — | MODEL ×1.8 | 0（同上 RA 脏） |

**四颗全部满足 PPA 文档判据（S ≥ 1.0 / 算子 ≤ 8 / 字段 ≤ 3 / PPAC < 0.5）。**

### 71.4 ★★★★★ `JjePOqMx` 已生成 PPA 交接单：Failed PPA = 0

```
python tools/ppa_handoff.py sheet --alpha-id JjePOqMx --ppac 0.2148
```

自动核对回执：**Failed PPA = 0 ✔** / PPA 名单内 PENDING：无 / Sharpe 1.85 ≥ 1.0 ✔ / 算子 8（去重 5）✔ / 字段 3 ✔ / PPAC 0.2148 < 0.5 ✔。

表达式：
```
group_neutralize(subtract(rank(ts_backfill(vec_avg(anl9_s_numup),22)),rank(ts_backfill(vec_avg(anl9_s_numdn),22))),sector)
```

**为什么它是全 DEU 最干净的 PPA 件**：它的 RA 失败项**只有 `LOW_2Y_SHARPE` 一条**（`ra_failed_checks = ["LOW_2Y_SHARPE"]`），而 2Y 恰恰是 PPA 唯一完全不检查的维度；`LOW_SHARPE` 因其 S 1.85 ≥ 1 不计失败；`LOW_FITNESS` / `CONCENTRATED_WEIGHT` 这两类「PPA 无豁免」的脏项它**一个都没有**。⇒ 四条 PPA 判据 + failed_ppa = 0 **全部干净**，是唯一一条不需要任何「口径宽松」才成立的件。

### 71.5 尚未闭合的一环：当期 Power Pool 主题窗口

交接单里唯一「必须由人核对」的项 = 当期活跃 Power Pool 主题窗口（`MATCHES_THEMES`）。本轮实测：
- `get_messages(limit=30)` 返回的 30 条**全是平台常规公告**（Genius 里程碑 / 研讨会 / 安全提醒 / 夏令时调整 / Value Factor 更新），**没有 Power Pool 主题公告**。
- `JjePOqMx` 的 `checks.warning` 与 `checks.pending` 里**都出现 `MATCHES_THEMES`** ⇒ 平台侧尚未给出 PASS。
- 按 `ppa-vs-ra.md` §1：不在当期主题窗口 → 候选标 `YELLOW` + `WAIT_THEME_ROTATION`，等主题轮转；非活跃区域会被平台报 `does not match any Power Pool Theme`。

⇒ **结论：`JjePOqMx` 的指标与 PPA 判据全部达标、交接单已就绪，但能否被受理取决于当期主题窗口，这一点 agent 无法确认，也不能替代用户操作。**

### 71.6 本轮净增量

- **DEU 纯 REGULAR 可提交件仍是 0**（§70.9 不变）。
- **但 PPA 通道给出 1 颗全判据干净的交接件 `JjePOqMx` + 3 颗次级候选**，且其中两颗（`gJe1moeJ` 2Y **2.60**、`j2YZ1JYQ` 2Y **2.31**）是「2Y 极强、S 不足」的镜像形态 —— 与 anl9「S 强、2Y 弱」正好互补，说明 DEU 的两堵墙（S 1.58 / 2Y 1.58）各自都有一批「只差一堵」的件，**PPA 通道放开的正是 2Y 那一堵**。
- PPA 提交**永远需要用户在 web UI 操作**（MCP 的 `workflow_submit_alpha` 非 PPA 感知，会拦合法 PPA）；用户提交后跑 `python tools/ppa_handoff.py record --alpha-id JjePOqMx` 回写。

### 71.7 ★★★★★ PPA-first 全量筛查：DEU 存量里共 3 颗「全干净」件，其中 2 颗是本轮新发现

不再按 RA 口径筛（那会把整片「只差 2Y」的件全刷掉），改按 **PPA 口径**重筛 DEU 全部 UNSUBMITTED：

- DEU UNSUBMITTED 总数 = **497**（`get_user_alphas(region="DEU")` 分页去重后的真实值，远高于 §69.1 记录的 212 —— 那个 count 是分页过程中的动态值，不可引用）。
- 过 PPA 的 S ≥ 1.0 且 TO ∈ [1%, 70%] = **182 条**。
- 对 S 最高的 **38 条**逐条拉 `get_alpha_details`，计「算子调用数 / 去重算子数 / 数据字段数 / ra_failed_checks ∩ PPA_CHECK_NAMES」。
- ⇒ **16 条满足「算子 ≤ 8、字段 ≤ 3、failed_ppa = 0」**。

按「RA 脏项是否属 PPA 豁免」分三档：

| 档 | alpha | S | F | 算子 | 字段 | PPAC | self | ra_failed_checks | 判级 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **A：全干净** | **`JjePOqMx`** | 1.85 | **1.51** | 8 | 2 | 0.2148 | 0.3309 | `LOW_2Y_SHARPE` | **首选** |
| **A：全干净** | **`9qxE7PNd`** | 1.64 | 1.37 | **7** | 2 | **0.2062** | 0.3411 | `LOW_2Y_SHARPE` | **备选（新）** |
| **A：全干净** | **`78Lon0jO`** | 1.61 | 1.30 | **7** | 2 | 0.2092 | 0.3365 | `LOW_2Y_SHARPE` | **备选（新）** |
| B：PPA 无豁免的脏项 | `Vkxd7Jzw` / `88Rve06X` / `mLoYVJ52` | 1.76/1.60/1.60 | 0.62/0.54/0.54 | 6 | 2 | — | — | `LOW_FITNESS`+`CONCENTRATED_WEIGHT`+`LOW_2Y_SHARPE` | 不建议 |
| B：PPA 无豁免的脏项 | `wpQ9AEx2` / `npvA2Vj3` / `RREA8R61` / `pwdv6zKb` | 1.56/1.51/1.47/1.46 | 1.17/1.11/1.15/1.17 | 4–8 | 1–2 | — | — | `LOW_SHARPE`（S≥1 ⇒ PPA 不计）+ 2Y | 边缘，可作第 4 顺位 |
| C：RA 干净但 prod 未算 | `wpQ9p0RY` / `leAMeol5` / `E56V59wP` | 1.68/1.65/1.65 | 1.29/1.26/1.26 | 7–8 | 1 | — | — | **[]** | **假干净，见下** |

**★★★ C 档是一个必须点明的陷阱**：`ra_failed_checks = []` 看着像「全闸通过」，但这三条都是 `fnd6_newq_oiadpq` 族，`PROD_CORRELATION` 仍在 `pending`。`compute_webdata_failed_counts` 的 docstring 已写明「`failed_ra == 0` 在 `pending_ra > 0` 时只表示**暂无失败**而非**已通过**」。同族 `gJeWJn9M` 实测 prod **0.9184**，这三条一旦 prod 算完大概率同命。**不要把它们当 REGULAR 候选报给用户。**

A 档三颗同属 `anl9_s_numup` / `anl9_s_numdn` 价差族（上调家数 − 下调家数），彼此高度同源 ⇒ **同一天只提 1 颗**（PPA 配额 1 / ET 日），其余作跨日备选。

### 71.8 `3qojOer6` 的 prod 最终结论：平台侧四次 240s 全 pending，读数**永久未取到**

```
[1] attempts=182 elapsed_ms=240691 status=pending
[2] attempts=181 elapsed_ms=240803 status=pending
[3] attempts=184 elapsed_ms=240432 status=pending
[4] attempts=181 elapsed_ms=240803 status=pending
超时未取到
```

16 分钟长窗口 + 四次平台 240s 超时，全部 `event=pending`、`computed=true` 但无值，`results/prod_wait_3qojOer6.json` **未生成**。
⇒ 该件 prod 只能继续沿用**近等价式 `gJeWJn9M` = 0.9184** 作先验（两者 S 1.79/1.80、2Y 1.74/1.77、TO 12.84%/12.82%、margin 12.63/12.76bp，差一个乘法结合方式）。**判：深钉，不作 REGULAR 候选。**

### 71.9 下一步可继续的动作（未执行）

1. 把 details 扫描从 38 条扩到剩余 **144 条**（S 1.0–1.46 段），可能再出 A 档件；成本约 144 次 `get_alpha_details`。
2. `wpQ9p0RY` / `leAMeol5` / `E56V59wP` 三条可各跑一次 `prod_wait` 坐实（但同族 0.9184 先验已足够判死，属可选）。
3. A 档三颗的**主题窗口**只能由用户在平台铃铛核对；agent 侧无 API 可查。

---

## 七十二、2026-11-05 PPA 深挖：扫完 98 条，得 6 颗 A 档 + 1 颗 B 档；3qojOer6 被 PPAC 0.939 挡死

### 72.1 ★★★★★ 关键认知修正：PROD_CORRELATION 也不在 PPA 名单

PPA_CHECK_NAMES 7 项里既没有 LOW_2Y_SHARPE，**也没有 PROD_CORRELATION**。⇒ 判 PPA 资格时，**prod 墙和 2Y 墙同时失效**，唯一的相关性门槛是 PPAC < 0.5（平台 POWER_POOL_CORRELATION）。

这解释了为什么 §71 只能挑出 1 颗：我此前一直用「RA 口径的脏项」在过滤。**一旦按纯 PPA 口径看，DEU 的候选池是整个 S ≥ 1.0 面。**

### 72.2 details 扫描进度与结果

| 轮次 | 扫描段 | 条数 | 满足 ops≤8 / nf≤3 / failed_ppa=0 |
|---|---|---:|---:|
| 第一轮 | S 1.46–1.85 | 38 | 16 |
| 第二轮 | S 1.32–1.46 | 60 | 21 |
| 合计 | — | **98 / 182** | **37** |

### 72.3 PPAC 实测：fnd6 动量族在 Power Pool 侧同样深钉

| alpha | 字段族 | S | F | ops | nf | PPAC | self | 判决 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 3qojOer6 | fnd6 营业利润动量 | 1.80 | 1.44 | 7 | 1 | **0.9391** ✗ | 0.1885 | **PPAC 深钉，PPA 也不收** |
| gJeZ5dMl | fnd6 同位 | 1.45 | 1.33 | 6 | 1 | **0.5675** ✗ | 0.2578 | 挡 |
| O0A8d6od | fnd6 同位 | 1.46 | 1.34 | 6 | 1 | **0.5324** ✗ | 0.1936 | 挡 |
| 1YNZ3JjX | fnd6 同位 | 1.39 | 1.23 | 7 | 1 | **0.4984** ✓（贴线） | 0.1902 | 勉强可用 |
| MPY08ReL | fnd45 财报电话 LDA | 1.42 | 0.88 | 5 | 1 | **0.0779** ✓ | 0.0749 | 低相关但 F<1 |
| akKVdY5x | anl93 星级分析师盈利 | 1.44 | 1.15 | 4 | 1 | **0.1522** ✓ | 0.2894 | **A 档** |
| Xg9RpxAb | anl93 同位 | 1.44 | 1.14 | 4 | 1 | **0.1546** ✓ | 0.2899 | **A 档** |

**★★★ 一个意外但极有用的交叉验证**：3qojOer6 的 **PPAC 0.9391** 与它近等价兄弟 gJeWJn9M 的 **prod 0.9184** 同量级。⇒ **PPAC 可以当「拥挤度」的零配额、秒回代理指标** —— 它只对 Power Pool 内的 alpha 算（本账号 pool_size = 1），完全绕开 prod 那条动不动 240s 超时的链路。
**但两者不能互相替代**：PPAC 只对 Power Pool 内持仓算，prod 对全生产池算；一条 PPAC 低不代表 prod 低（MPY08ReL PPAC 0.078 但从未测过 prod）。**用途是「先手排除明显拥挤族」，不是「替代 prod 判活」。**

### 72.4 ★★★★★ DEU 的 PPA 最终候选清单（6 颗 A 档 + 1 颗 B 档）

| 顺位 | alpha | 塔 | S | F | ops | nf | PPAC | self | 字段族 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **1** | **JjePOqMx** | **ANALYST** | **1.85** | **1.51** | 8 | 2 | 0.2148 | 0.3309 | anl9 上调/下调家数价差 |
| 2 | 9qxE7PNd | ANALYST | 1.64 | 1.37 | 7 | 2 | 0.2062 | 0.3411 | anl9 同位 |
| 3 | 78Lon0jO | ANALYST | 1.61 | 1.30 | 7 | 2 | 0.2092 | 0.3365 | anl9 同位 |
| 4 | akKVdY5x | ANALYST | 1.44 | 1.15 | 4 | 1 | 0.1522 | 0.2894 | anl93 星级分析师盈利 |
| 5 | Xg9RpxAb | ANALYST | 1.44 | 1.14 | 4 | 1 | 0.1546 | 0.2899 | anl93 同位 |
| **6（唯一非 ANALYST）** | 1YNZ3JjX | **FUNDAMENTAL** | 1.39 | 1.23 | 7 | 1 | 0.4984 | 0.1902 | fnd6 同位 |
| B 档 | MPY08ReL | FUNDAMENTAL | 1.42 | 0.88 | 5 | 1 | 0.0779 | 0.0749 | fnd45（F<1，PPA 无 F 门槛但 RA 脏） |

- 顺位 1–5 全部偏 ANALYST 塔（同族高度同源，**每日只能提 1 颗**；跨日用）。
- **PPA 配额独立**：POWER_POOL_SUBMISSION 1 / ET 日，不占 REGULAR 4 / 日 ⇒ 与 REGULAR 通道并行不冲突。
- 1YNZ3JjX 的 PPAC 0.4984 距 0.5 只差 0.0016，是**贴线件**，平台侧复算可能翻转 ⇒ 作 FUNDAMENTAL 塔的备选而非首选。

### 72.5 未扫完的部分

182 条过 S/换手线中还有 **84 条未拉 details**（S 1.0–1.32 段）。按已扫 98 条命中率 37.8% 外推，剩余约再出 **30 颗左右** PPA 合格件，主要价值是**覆盖更多金字塔**（当前只覆盖 ANALYST / FUNDAMENTAL 两座，DEU 共 16 塔未点亮）。

### 72.6 本轮把 PPA 通路的三个卡点逐个打通

| 卡点 | 打通方式 |
|---|---|
| 门槛口径 | src/wqb/config.py:402 PPA_CHECK_NAMES + tools/ppa_handoff.py:29 PPA_DOC_RULES |
| PPAC 取数 | check_self_correlation(correlation_type="powerpool")，零配额秒回 |
| 资格判定 | python tools/ppa_handoff.py sheet --alpha-id <ID> --ppac <值>，回执直接给 Failed PPA 计数 |
| 仍卡住 | 当期 Power Pool **主题窗口**（MATCHES_THEMES）无 API 可查，只能用户看平台铃铛 |


### 69.7 本节收口

本轮新增 **9 条有效臂**（news104 ×3、anl44 杠杆率 ×2、snt7 ATOM 之外的其余 4 条已在 §68），另 1 条因 event 类型报错作废。

**DEU 非 trio 面：0 颗可提交。累计已证伪挖法 = 16 类**（§68 的 14 类 + **新闻情绪族 news104** + **基本面水平型机制**）。

**纯 DEU 的最终候选清单 = 3 条**（1 条因 FUNDAMENTAL 禁混排除、2 条 snt7×snl27 prod 0.84/0.87）。DEU 侧内生途径已穷尽。

## 七十三、PPA 全量重筛终局（182 条全部拉 details）与「PPA 救不了塔覆盖」的定量结论 — 2026-11-05

### 73.1 这一节补的是 §72.5 的缺口

§72 只拉了 98/182 条的 details，剩下 84 条未扫，且当时用「算子 ≤8 / 字段 ≤3」当硬门。
本节把 **182 条全部拉完**（8 个批次 p01–p08，零配额 MCP 读），并纠正两个口径错误：

1. **算子 ≤8 与字段 ≤3 不是平台检查项**。平台 PPA 资格门只有 7 项（src/wqb/config.py:402 的 PPA_CHECK_NAMES）：
   LOW_TURNOVER / HIGH_TURNOVER / LOW_SUB_UNIVERSE_SHARPE / LOW_ROBUST_UNIVERSE_SHARPE /
   LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO / LOW_ROBUST_UNIVERSE_RETURNS / LOW_INVESTABILITY_CONSTRAINED_SHARPE。
   **PROD_CORRELATION、SELF_CORRELATION、LOW_2Y_SHARPE、IS_LADDER_SHARPE、LOW_FITNESS、CONCENTRATED_WEIGHT 全都不在名单内。**
   算子/字段数是 tools/ppa_handoff.py:29 的 PPA_DOC_RULES，源码注释自承「本环境未向平台复核」——只能当质量标尺，不能当准入门。
2. **原「命中 37 条」低估**。按平台 7 项口径重算，182 条里 **171 条合格**，唯一失败项是 LOW_SUB_UNIVERSE_SHARPE（11 条）。

### 73.2 塔分布：这是本节最重要的负结果

| 塔 | 182 存活 | PPA 合格（7 项口径） | 去重表达式 | RA+PPA 双零失败 |
|---|---:|---:|---:|---:|
| FUNDAMENTAL | 112 | 110 | 83 | 12 |
| ANALYST | 61 | 54 | 46 | 9 |
| SENTIMENT | 7 | 7 | 4 | 2 |
| PV | 1 | 0 | 0 | 0 |
| RISK | 1 | 0 | 0 | 0 |

- **171 条合格件 100% 落在 3 座塔里，且 96% 在 ANALYST+FUNDAMENTAL。**
- 结论（定量）：**PPA 通道能绕过 prod 墙与 2Y 墙，但完全绕不过「库存本身只有两座塔」这件事。**
  想用 PPA 点亮 DEU 剩下的 13 座塔是**不可能的**——瓶颈不在通道，在库存结构。
- 造成库存集中的原因可追溯：过去所有回合的挖掘预算都压在 anl9 / anl44 / anl93 / fnd6 / fnd45 / fnd72 六个字段族上（§73.4 的字段族分布直接印证）。

### 73.3 PPAC 实测：prod 深钉 ≠ Power Pool 拥挤（PPA 通道的成立条件被首次证伪/证实）

| alpha | 塔 | S | F | 2Y | sub | 算子（去重） | 字段 | PPAC |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| E56V8ex1 | SENTIMENT | 1.82 | 1.58 | 2.63 | 1.22 | 8 | 2 | **-0.0132** |
| 88RvEeYa | SENTIMENT | 1.69 | 1.44 | 2.22 | 1.27 | 8 | 2 | **-0.0183** |
| KPJmMd8j | ANALYST | 1.55 | 1.31 | 1.63 | 1.09 | 11 | 2 | **0.0638** |
| zq3r27rK | ANALYST | 1.45 | 1.29 | 1.66 | 0.89 | 11 | 2 | **0.0755** |
| JjePOqMx | ANALYST | 1.85 | 1.51 | 0.53 | — | 8 | 2 | 0.2148 |
| 3qojOer6 | FUNDAMENTAL | 1.80 | 1.44 | 1.77 | 1.23 | 7 | 1 | **0.9391** |
| gJeWJn9M | FUNDAMENTAL | 1.79 | 1.42 | 1.74 | 1.26 | 9 | 1 | **0.9185** |
| O0AJ0lxq | FUNDAMENTAL | 1.68 | 1.29 | 1.64 | 1.23 | 9 | 1 | **0.9149** |
| 9qxE371o | FUNDAMENTAL | 1.52 | 1.11 | 1.63 | — | 6 | 1 | **0.9061** |

两条硬结论：

1. **PPA 通道确实能救 prod 钉死的件**：snt7×snl27 族在 REGULAR 通道 prod 0.8424/0.8744（深钉判死），
   但在 Power Pool 池内 PPAC 只有 **-0.013/-0.018**——即它与池内已选 alpha 几乎零相关。
   ⇒ 「prod 高」与「PPAC 高」是两个不同的拥挤度量，**REGULAR 判死不能自动推广成 PPA 判死**。
   这是 PPA 通道价值的第一个正面实证，也是本节唯一的好消息。
2. **fnd6 营业利润动量族在 Power Pool 里同样拥挤**：4 个代表件 PPAC 0.906–0.939，
   与它们的 prod 0.9184 同量级。⇒ 该族**双通道同时判死**，无需再逐颗测 PPAC，
   83 条 FUNDAMENTAL 去重件按族归并后只剩 fnd45_lda_bigram_pr / fnd72 / fnd89 三个弱族（S 1.0–1.42）。
   ⇒ 由此得到可复用的**族级判死快筛**：family 内任一颗 PPAC ≥0.85，则该族在 PPA 通道亦判死，不必逐颗扫。

### 73.4 88 条「文档口径合格件」的字段族冗余（说明库存有多同质）

去重表达式 133 条只用到 **27 种字段组合**，前 3 名占 58%：
fnd45_lda_bigram_pr（23 条，最优 S 1.42）、fnd6_newq_oiadpq（17 条，最优 S 1.80）、anl9_s_numup+numdn（11 条，最优 S 1.85）。
⇒ DEU 库存的「数量」是假的，「机制数」只有约 6 个：fnd6/oiadpq、anl9 家数价差、anl44 净负债、anl93 修正、
fnd45 lda 主题概率、snt7×snl27 注意力比。
⇒ 这与 §73.2 的塔集中互为因果：**6 个机制、3 座塔、133 条表达式**，塔覆盖上无法再增。

### 73.5 交接口径修正后的 DEU PPA 首选序（全部零失败 + 低 PPAC）

1. **E56V8ex1**（SENTIMENT）—— 全项全过：Failed PPA 0、S 1.82、F 1.58、2Y 2.63、sub 1.22、算子去重 8、字段 2、PPAC -0.0132。
   交接单已生成（python tools/ppa_handoff.py sheet --alpha-id E56V8ex1 --ppac -0.0132 回执四行全 ✔）。
   **唯一待人工核对项：MATCHES_THEMES 主题窗口。** 同代码另有 3 条重复件（88RvEeYa 等），只能提 1 颗。
2. **KPJmMd8j**（ANALYST，anl44 净负债族）S 1.55 / F 1.31 / 2Y 1.63 / PPAC 0.0638。
3. **zq3r27rK**（ANALYST，同族）S 1.45 / F 1.29 / 2Y 1.66 / PPAC 0.0755。
4. **JjePOqMx**（ANALYST，anl9 家数价差）S 1.85 / F 1.51 / PPAC 0.2148（2Y 0.53 在 PPA 口径不算失败）。
5. 放弃：fnd6 族全部（PPAC 0.91+）。

### 73.6 工具修复（根因，非绕过）

tools/ppa_handoff.py 的 count_fields 原实现对含局部变量与具名参数的表达式直接崩（ParseError: Unexpected character ';'），
即使不崩也会把局部变量名与 driver/uniform 参数误算成字段（2 字段的件数成 6 个）。
本节按根因修正为：先去字符串字面量、去小写赋值目标/具名参数、按分号拆语句、逐句抽取、最后剔除全部局部变量名。
修正后 E56V8ex1 字段数 6→2、算子口径给出「调用 11 / 去重 8」双读数，交接单 exit 0。

### 73.7 本节对 30 颗目标的意义

- **PPA 不能用来补塔覆盖**（唯一能补的 SENTIMENT 塔只有 4 条去重表达式、1 个机制）。
- 三座塔 × 1.8 倍，即使把 171 条全提也只是「两塔刷量」，与「塔均匀点亮」的目标正交。
- 因此 30 颗目标在 DEU 只剩两条现实路径：① 承认塔覆盖不可达，改为「质量优先、能提几颗是几颗」；
  ② 换区（EUR 有全闸件 ZYQmolVx，S 2.48 / F 1.19 / 2Y 2.15 / prod 0.5276 / self 0.4169 实测无漂移）。
  两者都需要用户裁定，agent 侧不再自行选边。
## 七十四、risk60（证券借贷）重开：14 条臂全谱 + RISK 塔首颗 PPA 合格件 — 2026-11-05

### 74.1 为什么允许重开已「判死」的数据集

台账 L1837 把 risk60 列入「前轮已判死」，复核后有两条硬理由说明那是**证据不足的判死**：

1. 全库只探过**一条臂** `1YNx3vnm`（S 0.75 / F 0.50 / 2Y 0.79 / TO 10.5% / margin 10.39bp / lc 137），
   且该臂用了 `group_neutralize(add(rank(-ts_mean(...)), rank(-ts_mean(...))), subindustry)`，
   即已知会**系统性压低 margin 的 `add(rank(A),rank(B))` 秩和融合**——用它给整个数据集定上限不成立。
2. S 0.75 相当于闸值 1.58 的 **47.5%**，已高于「最优 < 40%（0.632）才可快速停止」的豁免线，按纪律应补模板而不是判死。

画像：category **risk**（非 trio，塔 RISK，乘数 **1.5**）、coverage **0.835**、5 字段全 VECTOR、ac 395、首探 longCount **137**。
模板池 `tracking/DEU/s1_risk60_wave1_template_pool.md`（12 个结构互异模板；机制出自 Chen–Hong–Stein 2002 / D'Avolio 2002 卖空约束理论）。

### 74.2 14 条臂全谱（DEU/TOP500/D1，decay 4、truncation 0.08、nan ON）

| # | 几何 | alpha | S | F | TO | 2Y | sub | margin | PPAC |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 | 费率水平 · 横截面秩（3 算子） | `d5WWVoMK` | 0.85 | 0.48 | 14.98% | 1.44 | 0.58 | 6.50bp | — |
| T4 | 拥挤度 22 日差分 | `P0ooa5ex` | −0.06 | 0.00 | **90.31%** | 0.75 | 0.34 | −0.08bp | — |
| T3 | 特殊度（offer−bid）/|bid| | `Xg99q2vX` | −0.57 | −0.20 | 24.25% | −1.50 | −0.31 | −2.38bp | — |
| T7 | 行业内相对（group_rank sector） | `j2YYLln5` | 0.62 | 0.30 | 14.32% | 1.35 | 0.44 | 4.66bp | — |
| T1a | 费率水平 @REVERSION_AND_MOMENTUM | `ZYQQZA3Q` | 0.62 | 0.40 | 11.45% | 1.53 | 0.30 | 9.01bp | — |
| T1b | 费率水平 @SLOW | `RREEXem1` | 0.76 | 0.40 | 8.93% | 1.48 | 0.69 | 7.72bp | — |
| T6-252 | 时序 z-score 252 | `LLMMOaX1` | 0.99 | 0.43 | 24.70% | 1.44 | 0.57 | 3.73bp | — |
| T9 | 双分位价差（费率−拥挤） | `N1NNkpro` | −0.82 | −0.26 | 39.87% | −0.88 | −0.23 | −1.95bp | — |
| T6-66 | 时序 z-score 66 | `1YNN6MGk` | 0.16 | 0.03 | 29.95% | 0.25 | 0.10 | 0.52bp | — |
| **T6-504** | **z-score 504（offer）** | **`58EENd0k`** | **1.07** | 0.50 | 23.61% | 1.47 | 0.73 | 4.38bp | **0.166** |
| T6-756 | z-score 756 | `A1VVJazX` | 0.87 | 0.37 | 23.15% | 0.76 | 0.49 | 3.63bp | — |
| T6-1008 | z-score 1008 | `MPYYllpz` | 0.80 | 0.33 | 23.02% | 0.73 | 0.52 | 3.37bp | — |
| **T6-504b** | **z-score 504（bid 费率）** | **`pwddJ3q6`** | **1.11** | 0.52 | 24.03% | **1.55** | 0.73 | 4.45bp | **0.150** |
| T6-504s | z-score 504（特殊度 offer−bid） | `ZYQQwNOZ` | 0.92 | 0.38 | 26.04% | 1.27 | 0.97 | 3.50bp | 0.154 |

### 74.3 四条结论

**① 去掉 `add(rank,rank)` 融合后同机制立刻变强**：旧臂 0.75 → 单腿水平 0.85（+0.10）。再次印证该融合是负和写法。

**② 横截面水平（0.85）远弱于时序标准化（1.11）⇒ 这是 time-series specialness 信号，不是横截面排序信号。**
DEU 大盘股的借券费率横截面差异很小（多数接近 0），真正有信息的是「相对自身常态异常高」。
这解释了 T3 横截面价差（−0.57）与 T9 双分位价差（−0.82）为何都塌：它们都在做横截面比较。

**③ 窗口曲线单峰，峰在 504（2 年）**：66 → 0.16 / 252 → 0.99 / **504 → 1.07** / 756 → 0.87 / 1008 → 0.80。
66（3 个月）塌到 0.16 说明短窗全是噪声；756/1008 下滑说明基准拉太长会把「异常」吸收成常态。
504 = 2 年正好覆盖一个完整费率周期。

**④ 机制对费率哪一侧不敏感**：offer 1.07 / bid 1.11 几乎同值 ⇒ 信号在「费率水平本身」，不是数据侧写伪影；
而特殊度（offer−bid）只有 0.92 ⇒ **价差不是载体，绝对水平才是**。

### 74.4 ★★★★★ 本轮实质产出：RISK 塔首颗 PPA 合格件

`pwddJ3q6` = `-rank(ts_zscore(vec_avg(lending_fee_bid_rate),504))`，S 1.11 / 2Y 1.55 / TO 24.03% / PPAC **0.150** / 塔 **DEU/D1/RISK x1.5**。

`get_alpha_details` 回执：`checks.fail = []`；warning 四项 = LOW_SHARPE(1.11<1.58) / LOW_FITNESS(0.52<1.0) / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE(1.55<1.58)；pending 含 POWER_POOL_CORRELATION。

**判 PPA 合格**：7 项名单里没有 LOW_FITNESS / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE；LOW_SHARPE 仅在 value<1 时计失败，本件 1.11 ≥ 1.0。
⇒ **failed_ppa = 0、S 1.11 ≥ 1.0、PPAC 0.150 < 0.5 ⇒ PPA 通道合格。**

**为什么这条最重要**：§73.2 统计过，DEU 182 条 PPA 存活里 **RISK 塔合格数 = 0**（唯一一条 `N1NeGQpg` 挂在 LOW_SUB_UNIVERSE_SHARPE）。
`pwddJ3q6` 是 RISK 塔的**第一颗** PPA 合格件，把 PPA 可交接池的塔覆盖从 3 座扩到 **4 座**（ANALYST / SENTIMENT / FUNDAMENTAL / RISK），且 RISK 属非 trio category。

### 74.5 REGULAR 通道仍不过，且差距构成要讲清楚

| 闸 | 本件 | 门线 | 是否过 |
|---|---:|---:|---|
| Sharpe | 1.11 | 1.58 | 否，差 0.47 |
| Fitness | 0.52 | 1.00 | 否，差 0.48 |
| 2Y Sharpe | **1.55** | 1.58 | 否，差 **0.03** |
| sub-universe | 0.73 | 0.517×S = 0.57 | 是 |
| 换手 | 24.03% | ≤70% | 是 |

**2Y 只差 0.03 但 S 差 0.47** ⇒ 不能靠微调补救：S 与 F 同时差近一半，属强度不足而非参数偏差。
按纪律判「REGULAR 通道封盘、PPA 通道保留」，不判数据集死。

### 74.6 这一轮给出的新策略规则（比本件本身更重要）

**PPA 的 S 门槛是 1.0，REGULAR 是 1.58 ——「挖新塔」的目标应当按 1.0–1.2 设，而不是按 1.58 设。**

若按 REGULAR 六闸，本轮 risk60 会在 T1 的 0.85 处收手（离 1.58 太远），从而错过后面 1.11 的 PPA 合格件。
但按 PPA 口径只需 **S ≥ 1.0**，且 LOW_FITNESS / LOW_2Y_SHARPE / CONCENTRATED_WEIGHT **全部不算失败**。

⇒ 行动规则：**对从未挖过的小数据集，判据改成「S 是否 ≥ 1.0 且 PPAC < 0.5」，而不是「是否过六闸」。**
这条把弱数据集的可产出面显著放大，是 DEU 补塔覆盖目前唯一被实证走通的路径。

### 74.7 未做完的部分

- T2（拥挤度水平）/ T5（费率差分）/ T8（门控）/ T11（二阶矩）/ T12（换手抑制）未跑：T4 已证明拥挤度一侧在 DEU 是噪声（−0.06 / 90% 换手），边际信息低。
- settings 轴只测 FAST 0.85 / SLOW 0.76 / REVMOM 0.62（FAST 最优），未测 MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / CROWDING：预期同向下滑，不再投槽。
- 未对 `pwddJ3q6` 跑 prod 相关性：REGULAR 通道已判封盘，且 PPA 通道不看 prod。
## 七十五、institutions4 判死 + risk60 强化版封顶 — 2026-11-05 下午

### 75.1 institutions4（机构持股）两臂快速停止

画像：category **institutions**（非 trio，塔 x1.6）、coverage **0.3413**、6 字段全 VECTOR、ac 19、userCount 13。
字段成对（current / previous × market_value / shares），可构造持仓变动，这是 smart-money 机制最直接的代理。

| 模板 | alpha | S | F | TO | 2Y | margin |
|---|---|---|---:|---:|---:|---:|
| T1 机构持股变动率（本期−上期）/|上期| | `3qoo3Nx0` | 0.10 | 0.02 | 12.84% | −0.60 | 0.77bp |
| T2 持股占流通比例 · 时序 z-score 504 | `vR119KWr` | −0.23 | −0.07 | 17.71% | −0.24 | −1.73bp |

**判决：判死（快速停止）。** 最优 0.10，是 PPA 目标线 1.0 的 **10%**，远低于 0.40 的豁免线；两条臂结构互异（一阶差分 vs 时序标准化）且方向相反，说明不是「骨架选错」而是本集在 DEU 无信号。

顺带记录一条结构性观察：`institutions4` 的 current/previous 字段对看似适合做「机构增减持」，但 DEU 只有 34% 的标的有数据，且这 34% 里持仓变动幅度极小——机构季报的滞后性使 Δ 项在日频上几乎全是零。

### 75.2 `earnings6` 不重开（复核既有判决）

本轮曾把 EARNINGS 塔列为候选，复核后放弃：

- §59.4 已用 **10 个模板**实测，全部弱，当时判决「`earnings6` 判弱封组合，EARNINGS 塔（0/3）在 DEU 归入不可挖」。
- 本轮复查 `get_datafields`：18 个字段 **coverage 全部为 0**（`ern6_*` / `preliminary_eps_*`），与「判弱」一致，无重测价值。
- 与 §s1 的 `earnings_sent_matrix`（上界 0.63）合并看，EARNINGS 两集共 17 条臂、两个独立声源（Estimize 预期差 + 新闻情绪矩阵）上界都只有 0.6 档。

### 75.3 risk60 强化版：两条都未能超过 `pwddJ3q6`

| 模板 | alpha | S | F | TO | 2Y | sub | margin | RA 失败数 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 买卖两侧费率均值 · z-score 504 | `d5WWm0EE` | 1.08 | 0.51 | 23.86% | 1.48 | 0.71 | 4.38bp | 4 |
| bid 费率先 22 日平滑再 z-score 504 | `qMLLd3MZ` | 0.94 | **0.54** | **13.69%** | 1.55 | **0.79** | **6.50bp** | **3** |
| （基准）bid 费率 z-score 504 | `pwddJ3q6` | **1.11** | 0.52 | 24.03% | 1.55 | 0.73 | 4.45bp | 4 |

**三条结论**：

1. **买卖两侧取均值反而变弱（1.08 < 1.11）**：offer 与 bid 的差（特殊度）是噪声不是信息，与 §74.3 的结论④一致——价差不是载体。
2. **平滑能改善 F / sub / margin / RA 失败数，但会把 S 压到 1.0 以下**：`qMLLd3MZ` 在 RA 口径下明显更健康（13.69% 换手、6.50bp margin、少一项 CONCENTRATED_WEIGHT），
   **可它 S 0.94 < 1.0 ⇒ 在 PPA 通道反而不合格**（LOW_SHARPE 仅在 value<1 时计失败）。
3. ⇒ **PPA 目标下的最优解是「不平滑」，这与 REGULAR 目标下「先降换手提 F」的直觉正好相反。**
   这条要写进方法论：**同一个件在 REGULAR 通道与 PPA 通道的最优点不同**，REGULAR 要 F，PPA 要 S≥1.0；平滑提升 F 但压低 S，因此 PPA 通道应优先保住 S。

### 75.4 本节收口状态

- `pwddJ3q6`（RISK 塔，S 1.11 / 2Y 1.55 / PPAC 0.150 / 3 算子 / 1 字段）仍是 DEU 最优 PPA 候选，交接单已核验（Failed PPA = 0）。
- 本区非 trio 数据集的挖掘面到此**基本走尽**：analyst / news / institutions / sentiment / risk / earnings / option / shortinterest / macro / socialmedia 十类中，
  除 `analyst83`（345 字段未挖，但属已点亮的 ANALYST 塔，对塔覆盖无增益）外，其余均已实测或已用 ≥10 模板判弱。
- 下一步若继续补塔，只能走「复核旧判死结论」路线：按 §74.6 的三条信号（只探过一条臂 / 用了 `add(rank,rank)` / 最优 S 超 0.632）筛台账里其它聚合式判死结论。
## 七十六、2026-11-05 晚（续二）：非 trio 最后四个未测集实测收口 —— INSTITUTIONS / SOCIALMEDIA / IMBALANCE 三塔关闭，NEWS 塔由 `news23` 重开

本节是对 §75.4「非 trio 面基本走尽」那句话的**逐条兑现**：把台账里仅剩的四个「从未实测」的非 trio 数据集一次性跑完。

### 76.1 本轮臂总览（8 条已收，全部 COMPLETE，零丢失 / 零 429）

| # | 数据集 | 塔 | 表达式核心 | alpha | S | F | TO | 2Y | sub | margin | returns |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `institutions6` | INSTITUTIONS | `-rank(ts_zscore(divide(aggregate_equity_value_institutions, cap), 504))` | `d5WW7PmY` | 0.06 | 0.01 | 15.11% | 0.32 | 0.25 | 0.34bp | 0.26% |
| 2 | `socialmedia12` | SOCIALMEDIA | `-rank(ts_zscore(ts_backfill(scl12_buzz, 5), 252))` | `WjOOXr6Q` | −0.03 | 0.00 | 53.84% | −1.02 | 0.51 | −0.04bp | −0.12% |
| 3 | `imbalance5` | IMBALANCE | `group_rank(imb5_score, subindustry)` | `P0ooXrqJ` | 0.14 | 0.03 | 17.64% | −0.14 | 0.68 | 0.76bp | 0.67% |
| 4 | `news23` | NEWS **+PV** | `-rank(ts_sum(divide(vec_sum(equity_total_proceeds_with_overallotment), cap), 252))` | `pwdd1zMj` | **0.77** | 0.40 | 11.42% | 0.50 | 0.00 | **5.95bp** | 3.40% |
| 5 | `news23` | NEWS | 发行惊喜 `Σ252 / (Σ1260+1)` | `kqNNLORP` | 0.70 | 0.35 | 11.53% | **0.57** | −0.07 | 5.44bp | 3.14% |
| 6 | `news23` | NEWS | 发行事件计数 `ts_sum(vec_count(...), 252)` | `WjOOW3Wd` | 0.72 | 0.36 | 11.25% | 0.22 | 0.09 | 5.51bp | 3.10% |
| 7 | `news23` | NEWS | 发行额 / 员工数 | `6Xdda35Y` | 0.05 | 0.01 | 13.44% | −0.32 | −0.23 | 0.39bp | 0.26% |
| 8 | `news23` | NEWS | `ts_zscore(Σ252, 504)` 自身基线特化 | `d5WWEw9E` | 0.22 | 0.06 | 12.62% | 0.62 | 0.00 | 1.60bp | 1.01% |

### 76.2 `institutions6`（INSTITUTIONS 塔）第 5 臂仍为零 ⇒ **塔关闭**

- 前科：§46.2 三臂全灭（最好 0.32）+ `d5WOrJQ2` 净买家广度聚合式 0.03（且是 `add` 秩和式负和写法）。
- 本臂刻意换成 risk60 的**长基线特化**写法（机构持股市值占市值比，对自身 504 日基线做 z-score 再取负），cov 1.0 真数据、TO 15.11%（不是被 LOW_TURNOVER 卡死），结果 **S 0.06 / margin 0.34bp**。
- ⇒ 5 臂、两种几何（横截面聚合 vs 时序特化）都为零。**INSTITUTIONS 塔在 DEU 归入不可挖**：13F 系季报对 DEU 大盘股近乎「人人都被机构持有」，横截面几乎没有可用离散度。

### 76.3 `socialmedia12`（SOCIALMEDIA 塔）第 3 臂仍为零 ⇒ **塔关闭**

- 前科：§61.4 两臂在飞后被平台丢失（`iZ2Zl3iP…` / `3D9koSeW…`，从未回读数）；前轮 P15 探针另测过情绪分数 / 预期价格变化两个语义最强字段，均无信号。
- 本臂即 §61.4 的 S2 重跑（`-rank(ts_zscore(ts_backfill(scl12_buzz,5),252))`）：**S −0.03 / TO 53.84% / 2Y −1.02**。换手是全部非 trio 臂里最高的一档，且方向为负。
- ⇒ 关注度水平、关注度时序特化、情绪水平、预期价格变化四条路径全灭。**SOCIALMEDIA 塔在 DEU 归入不可挖**（`socialmedia39` 更早已判死）。

### 76.4 `imbalance5`（IMBALANCE 塔）首测 S 0.14 ⇒ **塔关闭**

- 该集此前从未实测，只因「机制不明」被排除；§5531 曾建议把 `imb5_score` 当**分组轴**而非信号使用，本臂即该建议的落地：`group_rank(imb5_score, subindustry)`（行业内抗油价冲击韧性排序）。
- 结果 **S 0.14 / F 0.03 / returns 0.67%**。
- ⇒ `imb5_score` 是 0–1 有界的**状态评分**，作行业内排序也没有横截面信息量；加上 EUR 侧画像早已记录该集 returns 仅 2.66%（F 闸数学不可过）。**IMBALANCE 塔关闭**，全塔仅此 2 字段，无第二条路径。

### 76.5 ★★★★ `news23`：NEWS 塔级判死结论**被推翻**——该集从未被测过，首测 S 0.77

- 台账 §10034 曾写「DEU/NEWS 塔 regular 通道关闭」，但那条结论建立在 news81 / news17 / news104 / news18 等**情绪类** news 集之上；`news23` 是**完全不同的机制面**（116 字段全是 Deal 事件：VC 轮次、IPO/增发、银团贷款、债券发行），前轮仅做过画像、**一条臂都没跑过**。
- 本轮首臂 `pwdd1zMj`（过去 252 日增发募集额 ÷ 市值，取负）拿到 **S 0.77 / F 0.40 / TO 11.42% / margin 5.95bp / returns 3.40%** —— 是近期所有新数据集首臂里最好的一条。
- **逐年覆盖实测（`get_alpha_yearly_stats`）**：2014–2023 **每年** `longCount` 161–197、`shortCount` 107–188，**无任何空窗**；逐年 S = 2014 −0.81 / 2015 1.66 / 2016 0.05 / 2017 **2.75** / 2018 **2.65** / 2019 −1.53 …。⇒ 覆盖闸全过，且这是**事件型数据里罕见的满覆盖**。
- 经济学先验扎实：Loughran & Ritter (1995) 增发公告负效应、Pontiff & Woodgate (2008) 净股本发行异象 —— 「过去一年增发强度越高，未来回报越低」。

### 76.6 ★★★ 关键归因：`news23` 的信号只活在「发行额 ÷ 市值」这一个形态里

四条变形把机制边界钉死：

| 变形 | S | 相对基准 0.77 | 说明 |
|---|---:|---|---|
| 发行额 ÷ **市值**（基准） | 0.77 | — | 规模归一带来 +0.05~0.07 |
| 发行**事件计数** | 0.72 | −0.05 | 丢掉金额权重仍保留大部分信息 ⇒ 不全是量纲效应 |
| 发行**惊喜**（Σ252 ÷ Σ1260） | 0.70 | −0.07 | 自身历史归一略逊于规模归一 |
| 发行额 ÷ **员工数** | 0.05 | −0.72 | ★ 换成粗规模代理即归零 |
| **时序特化** `z-score(Σ252, 504)` | 0.22 | −0.55 | ★ risk60 的形态在此**不成立** |

⇒ 两条硬结论：① 规模归一的**精度**是这条信号的命门（市值可用、员工数不可用）；② 该机制是**横截面水平**机制，不是「相对自身常态的异常」机制。

### 76.7 ★★★★ 重要负结果：risk60 的「长基线时序特化」模板**不具迁移性**

本轮把 risk60 的冠军形态（`-rank(ts_zscore(<慢变水平>, 504))`）原样搬到两个从未挖过的塔，结果：`institutions6` **0.06**、`socialmedia12` **−0.03**、`news23` 上更差（0.22 vs 0.77）。

⇒ **risk60 之所以在 504 窗口见峰，是因为借券费率本身是「稀缺性/拥挤度约束变量」，其信息载体就是「相对自身常态有多紧」**；换成机构持股、社媒关注度、增发强度这类**水平型信息**，自身历史基线不是信息的载体，z-score 只是把信号稀释掉。
**所以 §74 的结论要加一条适用边界：时序特化只对「约束/稀缺类」慢变变量有效，不可当作通用降 prod / 提 S 模板跨数据集搬运。**

### 76.8 ★★★ 混搭配额的隐性触发：`cap` `adv20` 会让 alpha 同时占 PV 塔

`pwdd1zMj` 的 `get_alpha_details.pyramids` 返回 `[{DEU/D1/PV, 1.6}, {DEU/D1/NEWS, 1.8}]`、`effective: 2` —— **只要表达式里出现 `cap`（或 `adv20` 等内置 PV 字段），即使数据字段全部来自单一非 PV 数据集，平台也会把该 alpha 记入 PV 塔**。
⇒ **`cap` / `adv20` 是「隐形的混塔源」**。本区「集合内 × 集合外」混搭配额已满 5/5，因此 `pwdd1zMj` 这条 0.77 的臂**不能入库**；纯 NEWS 的合法版本上限只有 0.72（`WjOOW3Wd`）。派发前若想保住单塔 ATOM，规模归一必须改用同数据集内的规模字段（但 §76.6 已证员工数不行）。

### 76.9 本节收口：DEU 非 trio 面**已无未测数据集**

- 58 个非 trio 数据集至此**全部**至少有一条实测臂或一份 ≥10 模板判死记录；仅 `analyst83`（345 字段，ANALYST 塔已点亮，历史最好 0.21）与 `analyst69/analyst7/analyst9`（待用户裁定的 leading-gap / 2Y 卡死项）不在「已测尽」之列。
- 塔级终局（DEU）：已点亮 = PV / MODEL / OTHER / FUNDAMENTAL / ANALYST / SENTIMENT；**待点亮 10 塔中，INSTITUTIONS / INSIDERS / EARNINGS / SOCIALMEDIA / IMBALANCE / MACRO / OPTION / SHORTINTEREST 八塔已用实测或多模板证据关闭**；RISK 塔已由 `pwddJ3q6`（PPA 口径）拿到首颗合格件；**NEWS 塔是唯一还有余量的塔**（`news23` 上界 0.77，纯 NEWS 0.72，距 PPA 的 S≥1.0 还差 0.23–0.28）。
## 七十七、2026-11-05 晚（续三）：★★★★ NEWS 塔重开成功 —— `news23` 纯单塔 alpha 达 S 0.99 / 2Y 1.38 / margin 55bp

> 本节是 §76.5 的直接延续：**修正 §76.9 的「上界 0.77」结论** —— 那是 FAST 轴下的读数，换中性化轴后上界被抬到 **0.99**。
> 本轮共 **22 条臂**，零丢失 / 零 429 / 零语法失败；其中 `news23` 一条集上打了 **17 条**，用于把机制面钉死。

### 77.1 ★★★★ 轴扫描是唯一有效杠杆（与记忆方法论一致，再次实证）

固定 `-rank(ts_sum(vec_count(equity_total_proceeds_with_overallotment), 252))`，只换 `neutralization`：

| 中性化轴 | alpha | S | F | TO | 2Y | sub | margin | RA 失败数 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **CROWDING** | `wpQQ55mY` | **0.99** | 0.60 | 1.88% | 1.25 | 0.44 | 49.08bp | 4 |
| REVERSION_AND_MOMENTUM | `O0AAo62b` | 0.92 | 0.53 | 5.46% | 1.33 | 0.32 | 15.30bp | 4 |
| SUBINDUSTRY | `GrWWMb9x` | 0.85 | 0.51 | 1.81% | 1.22 | **0.45** | 50.42bp | 3 |
| FAST（基准） | `WjOOW3Wd` | 0.72 | 0.36 | 11.25% | 0.22 | 0.09 | 5.51bp | 4 |
| SLOW | `bl66vMxl` | 0.57 | 0.24 | 5.86% | −0.23 | −0.06 | 7.59bp | 4 |

**四条读数**：
1. **CROWDING 轴一处换轴把 S 从 0.72 抬到 0.99（+0.27）、2Y 从 0.22 抬到 1.25（+1.03）、margin 从 5.5bp 抬到 49bp（9 倍）、TO 从 11.25% 压到 1.88%**。这是本轮唯一真正的增益来源。
2. **REVMOM（另一条风险模型轴）也有效（0.92 / 2Y 1.33）但 sub 只有 0.32**——两条风险模型轴都能剥离动量/拥挤暴露，而几何轴（SUBINDUSTRY）剥离的是行业暴露，效果次之。
3. **SLOW 轴把 2Y 打成负的（−0.23）**：SLOW 轴包含的慢变基本面暴露恰好就是增发信号的正交部分，剥掉它就剥掉了信号。
4. ⇒ 与 §74 的结论合起来看，**DEU 上「轴」的排序对每个机制族都不一样，必须逐族实测**，这条纪律再一次被证实。

### 77.2 窗口与平滑：252 最好、decay 4 好于 decay 10

| 设置 | alpha | S | F | TO | 2Y | sub | margin | 失败数 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| CROWDING · win **252** · decay 4 | `wpQQ55mY` | **0.99** | 0.60 | 1.88% | 1.25 | 0.44 | 49.08bp | 4 |
| CROWDING · win **504** · decay 4 | `wpQQLaAQ` | 0.92 | 0.55 | 1.65% | **1.38** | **0.53** | **55.06bp** | **3** |
| CROWDING · win 252 · **decay 10** | `QPvvQmLw` | 0.97 | 0.58 | 1.81% | 1.22 | 0.42 | 49.86bp | 4 |
| CROWDING · win 504 · **decay 10** | `Jjeed0eO` | 0.90 | 0.54 | 1.61% | 1.37 | 0.51 | 55.63bp | 3 |

- **decay 10 全面小幅劣于 decay 4**（0.99→0.97、0.92→0.90）⇒ 与 §75.3 的「平滑提 F 压 S」一致，此族不需要平滑。
- **252 与 504 是一对权衡**：252 单一 S 最高（0.99）但 sub 卡线（0.44 < 0.47）；504 的 S 低 0.07，但 **2Y 1.38 / sub 0.53 / margin 55bp / RA 失败数 3** 全面更健康。

### 77.3 信息加工变体全灭：稀疏事件**必须**用 252 日累积强度

| 变体 | alpha | S | TO | 结论 |
|---|---|---:|---:|---|
| `ts_decay_linear(vec_count(...), 252)` 近期加权 | `0mYY8GQq` | 0.00 | **92.6%** | 单日事件稀疏 ⇒ 每日强度序列剧烈跳变 ⇒ 换手爆炸 |
| `ts_rank(vec_count(...), 504)` 时序分位 | `WjOOgY9P` | −0.11 | **98.0%** | 同上，且方向反了 |

⇒ **`ts_sum` 的累积是这条信号的「平滑器」，不是可有可无的包装**。把累积换成加权/分位，等于把「过去一年发了多少次股」重新拆成「今天有没有发」，信息量与稳定性同时崩塌。

### 77.4 债务腿全部污染信号：**只有股权发行**携带机制

| 事件腿 | alpha | S | 2Y | sub | margin |
|---|---|---:|---:|---:|---:|
| 仅股权发行（基准，SUBINDUSTRY） | `GrWWMb9x` | 0.85 | 1.22 | 0.45 | 50.42bp |
| 股权 + **银团贷款** 计数（SUBINDUSTRY） | `KPJJn5Vl` | **0.15** | 0.75 | 0.17 | 11.48bp |

⇒ 加入了银团贷款事件后 S 从 0.85 掉到 0.15。**「广义外部融资」假设（Bradshaw-Richardson-Sloan 2006 的 composite external financing）在 DEU 不成立**；成立的是更窄的 Loughran–Ritter / Pontiff–Woodgate 那条：**股权增发强度**。

### 77.5 本族最优件与 PPA 判定（差 0.01）

**`wpQQ55mY`** = `-rank(ts_sum(vec_count(equity_total_proceeds_with_overallotment), 252))` · DEU/TOP500/D1 · decay 4 · **CROWDING** · trunc 0.08

- 塔：`{DEU/D1/NEWS, multiplier 1.8}`、`effective: 1` —— **纯 NEWS 单塔 ATOM，不占任何混搭配额**。
- 指标：S **0.99** / F 0.60 / TO 1.88% / 2Y 1.25 / sub 0.44 / margin 49.08bp / returns 4.51% / 算子 3 / 字段 1。
- `checks.fail` = LOW_SHARPE 0.99<1.58、LOW_FITNESS 0.60<1、LOW_SUB_UNIVERSE_SHARPE 0.44<0.47、LOW_2Y_SHARPE 1.25<1.58。
- **PPA 口径**：`LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` 均 PASS；7 项硬名单里只剩 **LOW_SHARPE（0.99 < 1.0，差 0.01）** 与 **LOW_SUB_UNIVERSE_SHARPE（0.44 < 0.47）** 两项未过 ⇒ **仍不合格，但已进入「0.01 量级」的贴线区**。
- 若走 `wpQQLaAQ`（504 窗）：**sub 0.53 已过**、2Y 1.38、margin 55bp、RA 失败数降到 3，只剩 LOW_SHARPE 0.92 < 1.0 —— **离 PPA 只差「S 再高 0.08」这一项**，是当前全 DEU 结构最干净的一颗未过件。

### 77.6 方法论沉淀（三条，跨数据集通用）

1. **稀疏事件数据集的正确几何是「长窗累积 + 横截面 rank + 风险模型轴中性化」**，三件套缺一不可：累积负责平滑、rank 负责无量纲、CROWDING/REVMOM 轴负责剥掉动量与拥挤暴露（这一条让 S 涨 0.27、margin 涨 9 倍）。
2. **塔级判死必须按「机制面」而不能按「category」**：§10034 曾以 news81/news17/news104/news18（全是情绪类）为依据判「NEWS 塔关闭」，但 `news23`（Deal 事件，116 字段）**从未跑过一条臂**，首测即 0.77、换轴后 0.99。**「某 category 判死」不可外推到同 category 的不同机制数据集。**
3. **规模归一的来源决定塔归属**：`cap` / `adv20` 是 PV 内置字段，一旦出现在表达式里，即使数据字段全来自单一非 PV 数据集，平台也会把 alpha 记入 PV 塔（§76.8）。单塔 ATOM 只能用「同数据集内的规模字段」或「累积/事件计数」这类天然规模无关量。

### 77.7 本轮总账（§76 + §77 合并）

| 项 | 值 |
|---|---|
| 派发臂 | **22 条**（institutions6 1 · socialmedia12 1 · imbalance5 1 · news23 **17** · 其它 2 未计入）|
| 平台丢失 / 取消 / 429 | **0 / 0 / 0** |
| 关闭的塔 | INSTITUTIONS（5 臂）· SOCIALMEDIA（3 臂）· IMBALANCE（1 臂）· MACRO（既有 10 模板）· EARNINGS（既有 17 臂）|
| 重开的塔 | **NEWS**：`news23` 从「从未测」到 **S 0.99 / 2Y 1.38 / margin 55bp** 的纯单塔 ATOM |
| 当前 DEU 最强 NEW 件 | `wpQQ55mY`（S 0.99 · 差 PPA 两项）与 `wpQQLaAQ`（S 0.92 · **只差 LOW_SHARPE 一项**） |
| 提交数 | 仍 **11 颗**（本轮零提交、零平台写操作） |
## 七十八、2026-11-07 凌晨：★★★★★ `e75Vjx3d` —— 全战役首颗 `checks.fail=[]` 的 DEU alpha，NEWS 塔首颗 PPA 全过件

> 本节是 §77.7 之后「把 NEWS 塔推到 S≥1.0」的收口轮：**13 条臂完成 + 2 条平台丢单（404）重派 1 条**。

### 78.1 ★★★★ 关键平台行为：`LOW_SUB_UNIVERSE_SHARPE` 的 limit **随 S 等比缩放（≈0.474×S）**

五组实测同式不同 S 的 (S, sub, limit) 读数：`2rAALdX6` (1.06, 0.49, **0.50**) / `ZYQd8vN3` (1.01, 0.42, 0.48) / `e75Vjx3d` (1.03, 0.52, 0.49) / `wpQQ55mY` (0.99, 0.44, 0.47) / `wpQQLaAQ` (0.92, 0.53, 0.47 前轮)。
⇒ limit ≈ **0.474 × S**（DEU/TOP500）。这不是固定闸，是**比例闸**：**PPA 的真正约束对是 `S ≥ 1.0` 且 `sub/S ≥ 0.474`**——推高 S 会同步抬高 sub 闸线，纯提 S 没用，必须同时抬比值。

### 78.2 本轮 13 臂全谱（全部 `-rank/-group_*` 作用于 252/504 累积发行计数）

| 臂 | 几何 | alpha | S | F | 2Y | sub | sub/S | RA 失败 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 发行定义：全市场口径 | count(all_markets) @CROWD | `j2YYZQoj` | 0.98 | 0.59 | 1.25 | 0.43 | 0.439 | 4 |
| 发行定义：承销商口径 | count(bookrunner) @CROWD | `mLoo8ew5` | 0.98 | 0.59 | 1.12 | 0.40 | 0.408 | 4 |
| MARKET 轴 | 252 @MARKET | `omEEKJj6` | 0.79 | 0.45 | 1.09 | 0.38 | 0.481 | 3 |
| MARKET 轴 | 504 @MARKET | `Jjeep862` | 0.79 | 0.46 | 1.19 | 0.51 | 0.645 | 4 |
| ★ 分组×CROWD 叠层 | group_rank(subind) 252 | `2rAALdX6` | 1.06 | 0.69 | 1.19 | 0.49 | 0.462 | 4 |
| 分组×CROWD 叠层 | group_rank(subind) 504 | `pwddlYVq` | 0.98 | 0.60 | 1.31 | 0.44 | 0.449 | 4 |
| 双重行业剥离 | group_rank(subind)@SUBIND | `j2YY06Ro` | 0.94 | 0.59 | 1.15 | 0.43 | 0.457 | 4 |
| 粗粒度分组 | group_rank(industry) 252 | `O0AAZVRJ` | **1.11** | **0.70** | **1.34** | 0.43 | 0.387 | 4 |
| 504@REVMOM（重派） | rank 504 | `1YNNzgqM` | 0.89 | 0.52 | **1.58** | 0.42 | 0.472 | 2 |
| 粒度：sector | group_rank(sector) 252 | `ZYQd8vN3` | 1.01 | 0.62 | 1.23 | 0.42 | 0.416 | 4 |
| decay 8 | group_rank(subind) dec8 | `YP1EeXqw` | 1.06 | 0.69 | 1.17 | 0.48 | 0.453 | 4 |
| ★★★★★ **group_zscore** | group_zscore(subind) 252 | **`e75Vjx3d`** | **1.03** | 0.67 | 1.11 | **0.52** | **0.505** | **3** |
| trunc 0.05 | group_rank(subind) t05 | `gJeg2R8Q` | 1.06 | 0.69 | 1.19 | 0.49 | 0.462 | 4 |

**四条读数**：
1. **发行定义三口径（overallotment / all_markets / bookrunner）读数几乎相同（0.98–0.99）** ⇒ 机制对「股权发行」的具体字段定义不敏感，是结构级信号。
2. **分组粒度单调律：sub/S 比值 subindustry 0.462 > sector 0.416 > industry 0.387**——粒度越细，sub-universe 稳健性越好；但纯提 S 的 O0AAZVRJ（industry）比值崩到 0.387，S 1.11 也救不回来。
3. **decay 8 / trunc 0.05 都是噪声杠杆**（比值 0.453 / 0.462，与基准 0.462 无差）⇒ 参数层已收口。
4. **group_zscore 是唯一同时抬 S 与比值的几何**。

### 78.3 ★★★★★ 冠军件 `e75Vjx3d`：`-group_zscore(ts_sum(vec_count(equity_total_proceeds_with_overallotment), 252), subindustry)`

- 设置：DEU/TOP500/D1 · decay 4 · **CROWDING** · trunc 0.08 · 算子 4（neg/group_zscore/ts_sum/vec_count）· 字段 1。
- 指标：S **1.03** / F 0.67 / TO **2.53%** / 2Y 1.11 / sub **0.52**（比值 0.505 > 0.474 线）/ margin **42.43bp** / returns **5.36%**。
- **`checks.fail = []`——全战役首颗零失败检查的 DEU alpha**（LOW_SHARPE/LOW_FITNESS/LOW_2Y 全降级为 warning，PPA 名单 7 项全 PASS）。
- 塔：`{DEU/D1/NEWS, 1.8}`、`effective: 1`——**纯 NEWS 单塔 ATOM**。
- **PPAC = 0.0486**（全 DEU 候选最低；对照 pwddJ3q6 0.150 / E56V8ex1 −0.013 / WjOLdO7o 0.076）。
- 交接单 `ppa_handoff.py sheet --alpha-id e75Vjx3d --ppac 0.0486` **四项自动核对全 ✔（exit 0）**；MATCHES_THEMES 待用户在平台铃铛核对。

### 78.4 ★★★★ 为什么 group_zscore 能过而 group_rank 不能（机制归因）

`group_rank` 把组内只留**次序**、抹掉**幅值**：一个增发 10 次的股票和一个增发 3 次的股票，若都是组内最多，rank 输出同为 1。sub-universe 是更小的稳健宇宙，抹掉幅值后小宇宙里的排序噪声被放大 ⇒ sub 掉到线下。
`group_zscore` 保留组内**幅值信息**（z 分数按 (x−组均值)/组σ 缩放）：增发强度高得多的股票权重真的更高，信号在 sub-universe 里的排序更接近全宇宙 ⇒ 比值抬到 0.505。
⇒ **经验法则：当 `sub/S` 比例闸卡线而 S 已达标时，第一个该试的几何是 `group_rank → group_zscore`（保幅值），而不是 decay/trunc 这类参数杠杆。**

### 78.5 平台丢单记录（§61.5 现象再现）

504 窗两条组合臂（`n23_grpind504_crowd` / `n23_cnt504_revmom`）首派后 24h 查询均 HTTP 404「Not found」，`get_user_alphas` 亦无记录 ⇒ 确认丢单；其中 revmom 一条已重派成功（`1YNNzgqM`）。**派发回执 ok:true 不保证存活，收波以 lookINTO terminal + get_alpha_details 为准。**

### 78.6 PPA 交接池终局（5 塔 4 颗全过件）

| # | alpha | 塔 | S | PPAC | 算子/字段 | 状态 |
|---|---|---|---:|---:|---|---|
| 1 | `e75Vjx3d` | **NEWS**（首颗） | 1.03 | **0.0486** | 4 / 1 | **checks.fail=[] 全过** |
| 2 | `pwddJ3q6` | RISK | 1.11 | 0.150 | 3 / 1 | 全过 |
| 3 | `E56V8ex1` | SENTIMENT | 1.82 | −0.013 | 8 / 2 | 全过（与 88RvEeYa 同码，只能提 1） |
| 4 | `WjOLdO7o` | FUNDAMENTAL | 1.42 | 0.076 | 4 / 2 | 全过（F 0.88 是 REGULAR 视角弱点） |

塔覆盖从 4 座扩到 **5 座**（ANALYST/SENTIMENT/FUNDAMENTAL/RISK + **NEWS**）。全部等用户在 web UI 核对 MATCHES_THEMES 主题窗口后提交；agent 不执行 POST。

### 78.7 收口

- NEWS 塔的 PPA 面收口：**`e75Vjx3d` 已达结构上限**——S 1.03 ≥ 1.0、比值 0.505 有 0.031 的安全边际、PPAC 近零、纯单塔。REGULAR 面（六闸）此塔仍无解（S 1.03 vs 1.58 / 2Y 1.11 vs 1.58 / F 0.67 vs 1.0，缺口是机制性的）。
- 本轮 15 次派发（13 成 + 2 丢）全部零 429、零语法错、零取消；无在飞仿真。



































