# USA 可交付候选清单（prod 全测版）

> 更新时间：2026-10-28 15:30｜约束：**算子 ≤15**（用户 2026-10-27 定）｜**只挖不提交**（提交权归用户）
> 所有数值来自平台实测，prod 一律经 `check_correlation(refresh=True)` 获取。

## 一、已确认全闸通过（可提交）

| # | alpha | 构造 | ops | S | F | 2Y | sub | inv_S | TO | **prod** | self | eff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **`rKRY3NZ1`** | assetutil + cap桶 + 动量63桶 + **波动252桶** | **15** | 1.79 | 1.17 | 2.28 | 0.93 | 1.65 | 0.0459 | **0.6995** | 0.4700 | **2** |
| 2 | `zq3ZMvkX` | assetutil + cap桶 + 动量63桶 + **RISK动量桶** | 14 | 1.87 | 1.26 | 2.36 | 1.13 | 1.73 | 0.0491 | **0.6737** | 0.4652 | 0 ❌ |

```
#1 rKRY3NZ1（推荐 —— 唯一同时满足 ops≤15 + eff=2 + 全闸通过）
group_neutralize(group_neutralize(group_neutralize(
  group_rank(ts_zscore(ts_backfill(vec_avg(assetutilization_sentiment_polarity),126),504), industry),
  bucket(rank(cap),                     range="0,1,0.1")),
  bucket(rank(ts_mean(returns, 63)),    range="0,1,0.1")),
  bucket(rank(ts_std_dev(returns, 252)),range="0,1,0.1"))
@ CROWDING / decay5 / TOP3000 / D1 / trunc0.08 / nanHandling ON / maxTrade OFF / 2014-01-01→2023-12-31
```

**闸门逐项（`rKRY3NZ1`）**

| 闸 | 值 | 限 | 判定 |
|---|---|---|---|
| Sharpe | 1.79 | 1.58 | ✅ |
| Fitness | 1.17 | 1.0 | ✅ |
| IS_LADDER / 2Y | 2.28 | 1.58 | ✅ |
| sub_universe | 0.93 | 0.779 (=0.435×S) | ✅ |
| investability | 1.65（ratio 0.918） | — | ✅ |
| Turnover | 0.0459 | 0.01–0.7 | ✅ |
| **prod corr** | **0.6995** | <0.70 | ✅（余量 0.0005） |
| **self corr** | **0.4700** | <0.70 | ✅（池 135） |
| `checks.fail` | `[]` | — | ✅ |
| `failed_ra_count` | 0 | — | ✅ |
| pyramid | `[PV 1.1×, OTHER 1.4×]` ⇒ **effective=2** | — | ✅ |

⚠ 风险：① prod 余量仅 0.0005，提交前必须 `refresh=True` 复测；② `REVERSION_COMPONENT` warning（动量桶轴带来，不 fail，平台保留未来拒收权）。

## 二、RA 全过但 prod 未达（存档，不提交）

| alpha | 构造 | ops | S | F | sub | **prod** | eff |
|---|---|---|---|---|---|---|---|
| `1YNeYa3R` | assetutil + cap + 动量63（2 轴） | 11 | 1.92 | 1.34 | 1.09 | 0.7349 | 2 |
| `pwdmdxEx` | 上式 + **hump 1e-4** | 12 | 1.87 | 1.29 | 1.05 | **0.7501** | 2 |
| `1YNem7Rk` | assetutil + cap + 动量252 + 波动252 | 15 | 1.81 | 1.18 | 1.00 | 0.7168 | 2 |
| `akK6ZNYw` | assetutil + cap + 动量63 + returns | 14 | 1.90 | 1.29 | 1.05 | 0.7305 | 2 |
| `leAdO3R7` | assetutil + cap + 动量63 + volume63 | 15 | 1.83 | 1.25 | 1.10 | 0.7216 | 2 |
| `bl6X5r66` | assetutil + cap + RISK动量 + RISK残差波动 | 13 | 1.74 | 1.11 | 1.07 | 0.7067 | 0 |
| **`P0oabx6w`** | **profitability_fast_d1** + cap + 动量63 + 波动252 | 15 | 1.66 | 1.04 | 0.86 | **0.7135** | 2 |
| `78Lb33W2` | hump1e-4 + cap + 动量63 + `ts_delta(returns,5)` | 15 | 1.88 | 1.28 | 1.03 | **0.7332** | 2 |
| `qML8EnL1` | 同 #1 但 zscore 窗 756 | 15 | 1.79 | 1.17 | 0.92 | 未测（同族同席） | 2 |
| `9qxLZ929` | 同 #1 但 trunc 0.04 | 15 | 1.79 | 1.17 | 0.93 | 未测（指标逐位相同） | 2 |
| `P0odQnkp` | 同 #1 但 decay 10 | 15 | 1.72 | 1.11 | 0.90 | 未测（同族） | 2 |
| `e75kq7LE` | assetutil + 5 轴（超预算） | 25 | 1.85 | 1.18 | 1.02 | **0.6509** | 2 |

> `P0oabx6w` 证明「换 EC 章节」不能降 prod：同一 3 轴栈下 assetutil 0.6995 < proffast 0.7135。
> 章节的作用是决定 **IS 强度**（assetutil S 1.79 > proffast 1.66），不是决定 prod。
> `78Lb33W2` 证明 **hump 不降 prod**（相同 2 轴基础上 hump 版 0.7501 > 无 hump 版 0.7349）。

## 二·B、免费参数已扫尽（不改算子、不改表达式）

| 变体 | S | 2Y | sub | 判定 |
|---|---|---|---|---|
| 基线（TOP3000 / trunc 0.08 / decay 5 / z504） | 1.79 | 2.28 | 0.93 | ✅ 选定 |
| trunc 0.04 | 1.79 | 2.28 | 0.93 | 指标逐位相同 ⇒ truncation 无效 |
| decay 10 | 1.72 | 2.19 | 0.90 | 只降 S |
| ts_zscore 窗 756 | 1.79 | **2.41** | 0.92 | 等价（2Y 略优） |
| **TOP2000** | **1.37** | 1.42 | 1.11 | ❌ 3 fail（信息在中小盘） |
| **TOP1000** | **1.07** | 0.45 | 1.23 | ❌ 3 fail |

## 三、RA 全过、prod 待测（排队中）

| alpha | 构造 | ops | S | F | 2Y | sub | eff | 备注 |
|---|---|---|---|---|---|---|---|---|
| `6Xd7A5V7` | `trade_when(ts_zscore(returns,63)>0, 2轴基底, -1)` | 13 | 1.77 | 1.01 | 2.54 | 0.91 | 2 | DD 2.68%（−52%）｜nanHandling 被记 OFF（非纯净对照） |
| `78Lb33W2` | hump1e-4 + cap + 动量63 + `ts_delta(returns,5)` | 15 | **1.88** | **1.28** | 2.47 | 1.03 | 2 | IS 最优 eff=2 |
| `P0oabx6w` | profitability_fast_d1 + cap + 动量63 + 波动252 | 15 | 1.66 | 1.04 | 2.51 | 0.86 | 2 | 换章节，prod 可能更低 |

## 四、15 ops 预算的硬性上限（本族精算）

```
基底             4 ops  group_rank(ts_zscore(ts_backfill(vec_avg(F),BF),W), industry)
  ├ ts_zscore 不可删（删后 S 1.87→1.07）
  └ subtract(·,0.5) 可删（指标完全不变）
MATRIX 桶轴      3 ops  group_neutralize(·, bucket(rank(cap|risk_factor),"0,1,0.1"))
需 ts_* 的桶轴   4 ops  group_neutralize(·, bucket(rank(ts_mean|ts_std_dev(...)),"0,1,0.1"))
投影轴           2 ops  但实测无效（volume/adv20 甚至反向 +0.047）
```
⇒ **15 = 基底4 + 3 条桶轴**，即预算上限。四轴最低 17 ops。
⇒ eff=2（仅 PV+OTHER）时，第 3 轴必须是 PV 派生量 ⇒ 最强只能是 `ts_std_dev(returns,252)`（−0.035）⇒ **prod 地板 0.6995**。
⇒ 想再降 prod 必须用 RISK 轴（3 ops，−0.061）⇒ 金字塔变三类 ⇒ **eff=0**（塔 multiplier 归零）。

## 五、杠杆有效性总结（16 次实测）

| 杠杆 | Δprod | 判定 |
|---|---|---|
| 加桶轴（PV 动量63 / RISK 动量 / 波动252） | −0.035 ~ −0.069 / 轴 | ✅ 唯一稳定有效 |
| 换信号章节（profit → assetutil） | −0.06 | ✅ 有效 |
| `hump` 平滑（1e-4） | **+0.015** | ❌ 降 TO/抬 margin，**不降 prod** |
| mm 结构（`ts_max_diff`） | 毁 2Y（1.22） | ❌ 事件型数据不适用 |
| `vector_neut` 投影轴 | ≈0 / 反向 | ❌ |
| 窗口 / decay / 中性化微调 | ±0.01~0.02 | ⚠ 弱 |

## 六、提交前 checklist

1. `check_correlation(alpha_id=rKRY3NZ1, refresh=True)` 复测 prod（余量 0.0005，必须复测）
2. `check_self_correlation` 复测（池会变，0.4700 余量 0.23 尚安全）
3. `submit_verdict` 预检（否决权威）
4. **用户点名确认** → 才可 `workflow_submit_alpha(confirm_submit=True)`
