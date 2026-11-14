# BE15 结论：双新腿交叉 S 上限 1.38（路线收口）

## 一、十臂结果（sim 3rUh40dp64Rr9XTn4RSPsCe，complete=10 error=0）

骨架：`group_zscore(add(负向新腿, 正向新腿), market)`，两腿均 `ts_delta(ts_backfill(vec_avg(FIELD),132), W)` + `sector` 内层

| alpha | 组合 | S | F | TO | sub | 2Y | fail |
|---|---|---:|---:|---:|---:|---:|---|
| **GrmqmWq5** | loan_rate_vol × nws20情绪 | **1.38** | 0.66 | 0.2899 | **0.74** | 2.13 | S/F |
| **akaraK62** | lending_fee × nws20情绪 | 1.20 | 0.57 | 0.2596 | 0.45 | 0.82 | 4 项 |
| **oma1aE7E** | lending_fee × loan_rate_vol | 1.17 | **0.83** | **0.1221** | 0.68 | 1.21 | S/F/Ladder |
| O0W1WA07 | loan_rate_vol × nws20(平滑22) | 1.15 | 0.75 | 0.1296 | 0.81 | 1.48 | S/F/Ladder |
| rK717Rpd | nws20 × 贷出市值 | 1.10 | 0.46 | 0.2761 | 0.15 | **2.52** | 3 项 |
| Jj8V8ejA | loan_rate_vol × 贷出市值 | 0.84 | 0.43 | 0.1531 | 0.21 | 2.40 | 3 项 |
| 88NmNRom | 贷出市值 × 内部人显著性 | 0.62 | 0.28 | 0.1323 | 0.23 | **2.96** | 3 项 |
| 2r515A8P | loan_rate_vol × inst25集中度 | 0.47 | 0.22 | 0.1130 | 0.60 | 0.96 | 3 项 |
| pwaqadXV | nws20 × 机构显著性 | 0.45 | 0.15 | 0.2365 | 0.41 | 0.77 | 3 项 |
| Jj8V8eMA | nws20 × inst25集中度 | 0.33 | 0.09 | 0.2420 | 0.29 | 0.88 | 3 项 |

## 二、结论：双新腿路线收口（n=10，最高 1.38）

**S 上限 1.38，距 1.58 差 0.20。** 这是信息量叠加的物理上限：
- 每条新腿单独 S ≈ 0.9-1.1（BE13b 与 I7 配对时的表现扣掉 I7 贡献后反推）
- 两条独立信号叠加 ≈ `sqrt(S_a² + S_b²)` ≈ `sqrt(1.0² + 1.0²)` ≈ 1.41 —— **与实测 1.38 吻合**
- ⇒ 不引入 S≥1.3 的强腿，组合永远到不了 1.58

**与强腿配对的代价（已量化）**：
| 强腿 | 已被占用 | 新件与之互相关 |
|---|---|---:|
| I7 (insd1_holdings ts_rank252) | qM7KxkQV | 0.8451（rK71dLbE） |
| shrt3 Δ220 | qM7KxkQV / Jj8VQwoe | — |
| analyst 预估核心 | zq3eb7No / RREPm361 / 1YNMAA8M / bl6AvMkN | 0.6-0.69 |

⇒ **强腿的相关性配额已耗尽**：任何"强腿 + 新腿"组合都会撞 0.7 上限。

## 三、累计证据：DEU 剩余机制面 29 臂实测（BE13b 9 + BE14 10 + BE15 10）

```
S 分布：max 1.52 / median 1.15 / mean 1.06
S≥1.58: 0 / 29
S≥1.40: 4 / 29  （rK71dLbE 1.40、KPgKg68p 1.41、P05JM61x 1.46、QP010j5W 1.52）
```

**这 4 条 ≥1.40 的臂全部靠 I7 第二腿**，而 I7 已被 qM7KxkQV 占用（互相关 0.85）。

## 四、唯一剩余希望：FUNDAMENTAL（篮子里零覆盖）

**决定性证据**：已提交件 **Wje5K71x** 是 fundamental6 的 `fnd6_newq_oiadpq`，用骨架
`group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(F,66),240)), rank(ts_delta(F,66),176)), target_tvr=0.03), sector)`
拿到 **S1.73 / F1.37 / sub1.25 / TO0.1269 / self0.1882 / prod0.4305**。

⇒ **「fundamental ATOM 天花板 1.15」的旧结论是模板受限，不是字段受限**。换双窗口 tvr_decay 骨架后可达 1.73。
⇒ fundamental 在篮子 6 件里**零覆盖** ⇒ 互相关天然低。
⇒ 单数据集 fundamental = ATOM，无禁混风险。

**BE16 已派发**（sim j7Qn78tb5gObZH1h9J52Tde，10 臂）：fundamental89（Accrual based Earnings Model，407 字段，Sloan 应计异象）的 10 个字段 × 同一骨架。
⚠ 风险：fundamental89 全字段 platform coverage=0.0，若 DEU 无数据将整波 ERROR 或 pnl=0 —— 这本身就是一次必要的数据可用性验证。
