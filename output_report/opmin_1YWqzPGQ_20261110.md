# op-min 交付报告：`1YWqzPGQ` → `wpo8olA6`（12 → 8 算子，全闸通过）

> 生成 2026-11-10 22:00 ET 09:00｜区 DEU｜universe TOP500｜delay 1｜decay 4｜SUBINDUSTRY｜truncation 0.08｜nanHandling ON
> 会话：`1YWqzPGQ-opmin`（批 1–4，40 条仿真）

## 0 结论

| 项 | 值 |
|---|---|
| **交付件** | **`wpo8olA6`** |
| 算子数 | **8**（原 `1YWqzPGQ` = 12，↓4，−33%） |
| Sharpe | **1.65**（原 1.59，**+0.06**；闸线 1.58，余量 +0.07） |
| Fitness | **1.27**（原 1.10；闸线 1.00，余量 +0.27） |
| Turnover | 0.1396（原 0.1555） |
| IS Ladder | 2.59（闸 1.59） ｜ Sub-universe 1.07 ｜ Cluster 1.15 |
| checks | **0 FAIL / 0 WARN** |
| prod corr | **0.6306**（< 0.70；实读入权威表 `prod_peek` @21:59:19） |
| self corr | **0.5784**（< 0.70；最高相关 `xArzm3Mn` 0.578） |
| ΔSharpe | **+0.56**（分区 `EQUITY:DEU:1:POWER_POOL`，正向分散） |
| 稳健性 | **PASS**（十年无负年；近三年 1.04/2.78/2.40 均值 2.07、CV 0.36） |
| 塔归属 | `DEU/D1/SHORTINTEREST` + `DEU/D1/OTHER`（effective 2） |
| 塔边际 | **OTHER 2 → 3 点亮**（新塔 +1）；SHORTINTEREST 3 → 4（已亮） |

**压缩是净赚**：算子从 12 降到 8，Sharpe 升 0.06、Fitness 升 0.17、换手降 1.6pct。没有用「指标换算子」的代价。

## 1 最终表达式

```
subtract(group_rank(ts_delta(ts_backfill(vec_avg(oth47_organic_traffic), 132), 126), subindustry),
         group_rank(ts_delta(vec_avg(shrt3_bar), 252), subindustry))
```
算子清单（8）：`subtract, group_rank×2, ts_delta×2, ts_backfill, vec_avg×2`

与原式（12）的差别：
1. `add(-A, B)` → `subtract(B, A)`：**省 1 个算子，无损**（`neg + add` 两个调用变一个）
2. 删 `ts_quantile(..., 252)`：**省 1**，删后 S 反升（1.78→1.79 同族对照）
3. 删外层 `group_rank(..., sector)`：**省 1**，内外同轴冗余
4. 删 `shrt3_bar` 腿的 `ts_backfill`：**省 1**，该腿本就月度级低频，线性外推由 `ts_delta(252)` 自身吸收

## 2 压缩路径（逐批实证，非一次性猜）

| 批 | 目的 | 最优件 | ops | S | F | 结果 |
|---|---|---|---|---|---|---|
| 基线 | 原 alpha | `1YWqzPGQ` | 12 | 1.59 | 1.10 | S 余量仅 .01 |
| ① | 先推 S（窗口阶梯，结构冻结） | `58JZgp8o`（D2 66→126） | 12 | **1.78** | 1.31 | 余量扩到 .20 |
| ② | 无损改写 + 单算子消融 | `mLaPYkbp`（删 quantile + 删外层 rank） | 9 | 1.71 | 1.36 | 0 FAIL |
| ③ | 冲 8 算子 / 参数细扫 | `1YWqjz0Q`（删一腿 backfill） | 8 | 1.61 | 1.23 | 0 FAIL |
| ④ | 收敛加厚余量 | **`wpo8olA6`**（D1 264→252） | **8** | **1.65** | **1.27** | **0 FAIL / 0 WARN** |

**7 算子已证不可行**：`RReJAL80`（删 quantile + 删 backfill）S 1.42 / F 0.93 / 4 WARN ⇒ F 掉闸，**8 是硬底**。故 `operatorCount` 已压到该骨架的下限。

## 3 闸门记录（`workflow_submit_alpha` confirm_submit=false 实测）

| 步骤 | 结果 |
|---|---|
| `submit_gate` | **passed**，`failed_any=0`，`robustness.verdict=PASS` |
| `mix_audit` | `kind=none`，`legs=0` ⇒ **免三问**（两腿同向加性，非加权混信号） |
| `marginal_contribution` | before S 1.73 → after S 2.29，**ΔS +0.56**，`dilutive=false` |
| `diversity_audit` | 平台未回填 `is.selfCorrelation` ⇒ fail-open；本地实读 self 0.5784 < 0.70，且 ΔS +0.56 ≥ +0.02 ⇒ 分散度软闸不受阻 |
| `set_properties` / `submit` | 跳过（`confirm_submit=false`） |

## 4 稳健性（`get_alpha_yearly_stats` 十年）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 3.13 | 1.51 | **0.22** | 1.18 | 2.19 | 1.49 | **0.24** | 1.04 | 2.78 | 2.40 |

- 无负年、无零平年；弱年是 2016（0.22）与 2020（0.24），两年都是低波动/低借券活跃度环境，两腿同时失信息
- 近三年均值 **2.07**（闸 1.58）、CV **0.36**（阈值 0.5）、max/min **2.67**
- 最近一年 2.40 > 全期均值 1.65 ⇒ 无衰减迹象
- 已写入 `ledger_kv(DEU, robustness_wpo8olA6) = PASS`

## 5 塔信息（`is.checks[MATCHES_PYRAMID]` → `get_pyramid_alphas` 当季计数）

| 塔 | 归属 | 当前 | 提交后 | 是否新点亮 |
|---|---|---|---|---|
| `DEU/D1/OTHER` | ✅ | **2** | **3** | **是（+1 新塔）** |
| `DEU/D1/SHORTINTEREST` | ✅ | 3（lit） | 4 | 否（今日 `78Yk8VR1` 已点亮） |

DEU/D1 其余：analyst 6（lit）、model 3（lit）、fundamental 1、institutions 1、sentiment 1。

## 6 待办（提交前，需用户点名）

1. 属性：name `DEU_R_shrt3org_08op_01`；color BLUE；tags `CH_REG` + `SRC_shrt3` + `SRC_oth47` + `W20261110`
2. 三段式 description 需按 8 算子实况重写：**原第三段里关于 `ts_quantile` 与两腿 backfill 的论证已不成立**，必须改写为「删 quantile 后信息仍由 rank+delta 承载」「shrt3 腿以 ts_delta(252) 直接吸收稀疏性」
3. 提交前 `prod` 需 `refresh=True` 终验（当前 0.6306 为 21:59:19 实读，48h 内有效）
4. ET 11-10 配额 2/4 已用，剩 2 位

## 7 变体总账（40 条仿真，供回溯）

完整逐条指标见 `results/1YWqzPGQ_opmin_b1..b4.json`；签核见 `results/op_coverage_signoff.jsonl`（session `1YWqzPGQ-opmin1..4`）。

`SUPERSEDED`：`1YWqzPGQ`（12）、`58JZgp8o`、`O0W1Jvp1`、`VkNvdop8`、`mLaPYkbp`、`1YWqjz0Q`、`MP6j6QNM`、`ZYaRan9d` —— 全部保留在平台可查，不再作为交付候选。
