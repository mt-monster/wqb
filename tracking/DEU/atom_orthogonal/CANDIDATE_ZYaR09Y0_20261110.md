# ★★★ ZYaR09Y0 候选档案（2026-11-10 20:5x）—— 只差 sub 0.03

## 表达式（10 算子）
```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264), sector),
  group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings), 132), 252), sector)
), market)
```

- 腿 A：**借券需求变化 264 长窗**（`shrt3_bar`，SHORTINTEREST 塔，sector 内层）
- 腿 B：**内部人持股 52 周位置**（`insd1_holdings`，INSIDERS 塔，sector 内层）
- 组合层：**group_zscore @ market**（大样本 + zscore 标准化）
- 来源：BE9 臂1（zscore + 内 sector + 外 market 的合并最优结构）

## 平台闸门实测（`get_alpha_details` 权威）

| 项 | 值 | 门槛 | 判定 |
|---|---:|---|---|
| **S** | **1.60** | 1.58 | ✅ **PASS**（在 pass 列表） |
| **F** | **1.23** | 1.0 | ✅ **PASS** |
| **2Y** | **2.22** | 1.58 | ✅ PASS |
| **sub_universe** | **0.73** | **0.76** | ❌ **FAIL（差 0.03）** |
| TO | 0.139 | 0.01-0.7 | ✅ PASS |
| CONCENTRATED_WEIGHT | — | — | ✅ PASS |
| IS_LADDER_SHARPE | — | — | ✅ PASS |
| CLUSTER_TEST | — | — | ✅ PASS |
| **self_corr** | **0.5654** | 0.7 | ✅ 余量 0.135 |
| **prod_corr** | ⬜ 待测 | 0.7 | 平台队列拥塞 |

**平台 fail 列表仅 1 项**：`{ "name": "LOW_SUB_UNIVERSE_SHARPE", "value": 0.73, "limit": 0.76 }`

## 逐年覆盖（十年零空窗，**零负年**）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 1.45 | 1.86 | 1.26 | **0.21** | 1.13 | 2.12 | 1.61 | 1.59 | 2.09 | **2.55** |
| longCount | 109 | 115 | 122 | 133 | 138 | 143 | 158 | 201 | 196 | 170 |

- ✅ 十年零空窗，**全为正**（最低 2017 年 0.21）
- ✅ 最近三年 1.59 / 2.09 / 2.55 强劲
- 优于 1YWqzPGQ（后者 2016 年 -1.00）

## 塔位（比 1YWqzPGQ 更干净）

**DEU/D1/SHORTINTEREST + DEU/D1/INSIDERS**
- **两塔均属「禁混集合外」** ⇒ 双塔组合**不占用**「集合内×集合外」的 ≤5 配额
- 不影响 OTHER 塔（2）/ FUNDAMENTAL（1）的点亮状态

## 与既有候选的关系

| 对 | 相关 | 判定 |
|---|---:|---|
| ZYaR09Y0 ~ 1YWqzPGQ | 0.611（同族 3q0M99Gz 的读数） | ✅ 可共存（余量 0.089） |
| ZYaR09Y0 ~ E569ZE7L | 0.324 | ✅ |
| ZYaR09Y0 ~ RREPm361 | 0.033 | ✅ |
| 族内 3q0M99Gz / xAvKY0Ob / WjlEPPYP | 0.92-0.99 | 取 ZYaR09Y0（最强） |

## 缺口与修法（BE10 在测）

| 缺口 | 数值 | 当前修法 |
|---|---|---|
| **sub 0.73 → 0.76** | 差 **0.03** | BE10 六臂：内层改 industry / 内部人腿 504 窗 / 借券腿 220/308 邻域 / 外层 group_rank 对照 |

## 结论

**ZYaR09Y0 是本轮质量最高的未全清候选**：
- 平台 checks 只剩 1 项（sub），缺口 0.03；
- 逐年零负年、self 0.565 余量大、塔位干净（不占配额）；
- 若 BE10 补上 0.03 ⇒ **DEU 第 7 颗全清候选**（与 1YWqzPGQ 并列最强）。