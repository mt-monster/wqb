# IND 区 ATOM 路线可行性判定（2026-10-22）

> 目标：在 IND/TOP500/D1 产出 **ATOM（单数据集）** regular alpha。
> 判定口径：三闸（S ≥ 1.58｜F ≥ 1.0｜2Y ≥ 1.58）+ sub/rob + 8 个统计族全试。

---

## 一、结论先行

| 数据集 | 类别 | 字段数 | 试过表达式 | 最高 \|S\| | 最高 F | 判定 |
|---|---|---:|---:|---:|---:|---|
| `institutions6` | institutions | 11 | **24** | 0.62 | 0.26 | **ATOM 不可行** |
| `risk70`（机构持股字段） | risk | 35（2 个真机构持股） | **14** | 0.58 | 0.24 | **ATOM 不可行** |

**共性指纹：F 上限 0.26，sub/rob 接近 0，prod 毫无压力 ⇒ 不是 prod 拥挤，是「强度结构性不足」。**

---

## 二、institutions6（Institutions 类别唯一数据集）

字段：`aggregate_equity_value_all_owners` / `aggregate_equity_value_institutions` / `aggregate_share_count_all_owners` / `aggregate_share_count_institutions` / `count_institutional_buyers_security` / `count_institutional_holders_security` / `count_institutional_sellers_security` / `market_value_institutional_shares_acquired` / `market_value_institutional_shares_disposed` / `quantity_institutional_shares_acquired` / `quantity_institutional_shares_disposed`

| 轮次 | 覆盖的统计族 / 经济维度 | 最高 \|S\| | 最高 F |
|---|---|---:|---:|
| 1（10 条） | 横截面秩、一阶差分、时序秩、冠军栈、波动调整、group_rank + 买卖金额比、买卖家数比、净买入/持仓、持股比例变化、机构数变化、买方占比 | 0.61 | 0.25 |
| 2（8 条） | 二阶差分、双窗秩乘积、事件衰减（补齐 3 族）+ 持股集中度、持股比例水平、股数口径净买入、机构换手强度 | 0.60 | 0.26 |
| 3（6 条） | **数据集内部残差**（机构字段对机构字段 `ts_regression`，decay 126） | 0.62 | 0.09 |

⇒ 8 族全试 + 内部残差 + 11 字段用尽，天花板 0.62。与分支卡既有记录「institutions6 作主信号 best 0.32」方向一致（本轮更高但仍远低于闸线）。

---

## 三、risk70（机构持股经济，RISK 塔）

真机构持股字段：`hedge_fund_ownership_percentage`（对冲基金持股比例）、`hedge_fund_number_owners`（持有对冲基金家数），cov 均 1.0。

| alpha | 结构 | S | F | TO | 2Y | rob |
|---|---|---:|---:|---:|---:|---:|
| `1Yjj351J` | `rank(hedge_fund_ownership_percentage)` | 0.58 | 0.24 | 0.067 | **1.54** | 0.19 |
| `akVVm3l6` | `rank(hedge_fund_number_owners)` | 0.55 | 0.23 | 0.057 | 1.19 | 0.34 |
| `e766MJKN` | `rank(ts_delta(own_pct, 66))` | 0.50 | 0.19 | 0.064 | 1.27 | 0.11 |
| 其余 7 条 | 集中度 / 双窗 / ts_rank / 波动调整 / group_rank / 事件衰减 | ≤0.48 | ≤0.18 | — | — | — |

**值得注意的形状**：多条 **2Y（1.19–1.54）显著高于全期 S（0.48–0.58）** ⇒ 信号只在近年有效、全期被早年拖死。但 **S 闸 1.58 不可由 2Y 替代**，故不可交付。

### 逐年年表（`1Yjj351J`）—— 决定性否证「覆盖不足」假设

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | 0.05 | 1.18 | 0.26 | **−1.51** | −0.15 | −0.35 | 1.11 | 1.56 | 1.82 | 1.50 |
| long/short | 320/165 | 305/194 | 271/229 | 265/239 | 256/246 | 255/247 | 270/229 | 270/234 | 264/238 | 264/241 |

**2014 年已有 320 多 + 165 空**（字段在早年完全有数据），S 仍只有 0.05；**2017–2019 连续三年为负**。
⇒ **不是覆盖不足，是制度切换 + 符号翻转**：该信号只在 2020 年后有效，且 2017–2019 是反向的。
⇒ 覆盖假设零成本证伪，原计划的 `ts_backfill 252` 验证无需再跑。

### 补齐批（8 族闭环）

`4burfY3Je4MH8MIjwqFjdK0`：冠军栈 / 二阶差分 / `group_rank(subindustry)` / `ts_zscore 504` ⇒ 最高 |S| **0.20**，全部 RA_FAIL。

**risk70 机构持股 ATOM 最终战绩：14 条表达式 / 8 个统计族全覆盖 / 天花板 |S| 0.58。判死。**

---

## 四、为什么 ATOM 在 IND 结构性吃亏

IND 至今**唯二**被证能稳定过闸的机制：

1. **残差化**：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(F,252),252,rettype=0))` + decay 126
2. **分析师连续慢变量**（`anl44_eps_best_eeps_cur_yr` 系）

两者的共同点：**都需要一个强度锚** —— 前者用 `returns`（PV），后者用分析师高频修订。**ATOM 禁用第二个数据集，等于把锚拿掉**，只剩纯基本面/持仓的水平与差分，而这类慢变量在 IND/TOP500 的横截面区分度天然不足（TO 仅 0.06–0.13，说明持仓几乎不动）。

旁证：IND 全区历史**唯一达标 ATOM 是 `zqrj0bzK` 一颗**（14 334 字段中）。

---

## 五、建议

| 优先级 | 路线 | 说明 |
|---|---|---|
| ★★★★ | **放弃 ATOM 主攻，走残差化（非 ATOM）** | 已在 institutions6 复现 **8/8 RA 全过**（S 2.65–2.92 / F 1.88–2.18 / rob 1.14–1.76）；但互相关高（最大 0.944，<0.7 的最大子集仅 3 颗），需按「机制族」而非「参数」凑颗数 |
| ★★★ | 换类别点塔 | fundamental 塔 2/3、只差 1 颗且 multiplier 1.2，投入产出比最高 |
| ★★ | 若坚持 ATOM，换区试 | KOR/USA 的单数据集字段更密（如 KOR `shortinterest3/38` 共 144 字段），强度锚不依赖 `returns` |
| ★ | 继续在 IND 硬做 ATOM | 已证两个数据集、38 条表达式、天花板 0.62，不建议 |

---

## 附：本轮修正的错误结论

旧记「`regression_neut` / `hump_decay` / `ts_decay_exp_window` / `ts_target_tvr_delta_limit` / `ts_target_tvr_hump` / `ts_kurtosis` / `tail` / `kth_element` / `vec_std_dev` 在 IND 不可用」**已被用户实测推翻 —— 这些算子全部可用**。

真实原因：批次里混入一条错表达式 ⇒ **整个 multisim 被判 CANCELLED**，被误归因为「算子不存在」。

**新铁律：`整批 ERROR` 只证明「批内有错」，判算子不可用必须单条隔离；能做到的算子就尽量用。**
