# ★insiders 双数据集 = 单塔 ATOM：判据纠正与 1.37 天花板

日期：2026-11-12
用户提问：「这2个互补是不是意味着，它们可以组在一起」

## 一、纠正：ATOM 是金字塔级判定，不是数据集级判定

**此前错误结论**（`INSIDERS_ATOM_FINAL_VERDICT_20261112.md` §二）：
「ATOM 硬约束 #1：单数据集，只能用 insiders1 或 insider_agg_matrix 之一」

**实证推翻**：`WjlMlWJd` 用了 5 个数据集——
- `insd1_holdings`（insiders1）
- `significant_value_1..4`（insider_agg_matrix）
- `est_12m_ebi_*`（analyst7）
- `cap`（PV）
- `days_from_last_change`（算子，非字段）

但 `pyramids.list` 只有 **3 座**：`DEU/D1/PV` + `DEU/D1/INSIDERS` + `DEU/D1/ANALYST`。

⇒ **insiders1 与 insider_agg_matrix 被平台合并为同一座 `DEU/D1/INSIDERS` 金字塔。**
⇒ **两个数据集组合后仍为 `effective = 1` = ATOM。**

## 二、BE188 直接验证（6 臂，全部 eff=1）

| 构造 | S | Y2 | sub | pyramids.effective |
|---|---:|---:|---:|---|
| 2腿 Δ66+HHI | 1.25 | 1.28 | 0.55 | **1** |
| **3腿 Δ66+ir66+HHI** | **1.37** | **1.45** | 0.66 | **1** |
| 3腿 Δ66+Δ132+HHI | 1.26 | 1.22 | 0.40 | **1** |
| 4腿 +Δ132 | 1.33 | 1.36 | 0.51 | **1** |
| 短窗22 | 0.78 | 0.99 | 0.27 | **1** |
| 长窗132 | 0.90 | **2.05** | 0.31 | **1** |

塔名唯一：`["DEU/D1/INSIDERS"]`，倍数 1.6。

**⇒ 用户判断正确：两个互补数据集可以组合，且组合后仍是 ATOM。**
**⇒ 同时拿到年份对冲：Y2 从 insiders1 单集的 0.85 抬到 1.45。**

## 三、设置的三个硬结论（decay / nan / 中性化）

| 设置 | 结果 | 判定 |
|---|---|---|
| **decay 0** | S 1.33-1.37 / Y2 1.45-2.10 | 基线 |
| **decay 4** | S 1.32-1.37 / **Y2 2.10-2.64** | ★ 最优（Y2 大幅抬升，S 几乎不损）|
| decay 10 | S 1.23-1.26 / Y2 2.31-2.35 | 次优 |
| **nan_handling=OFF** | **S 0.32-0.72**（全崩）| ❌ 致命 |
| neut=FAST | S 0.88-1.01 | ❌ 差 |
| neut=SUBINDUSTRY | S 1.32-1.37 | ★ 最优 |
| truncation 0.05 / 0.08 / 0.12 | 1.32-1.36 同档 | 非关键变量 |

**注意**：`nan=OFF` 摧毁本策略（S 掉到 0.32-0.72，且全触发 `CONCENTRATED_WEIGHT`，TO 从 6% 飙到 18-22%）。
这与「事件型字段必须 nan=OFF」的旧结论**相反**——insiders 双集组合的正确设置是 **nan ON + decay 4**。

## 四、冠军结构：交互式乘法而非求和

**关键发现**：历史冠军 `d5apW38x`（S 2.36 / Y2 2.67，非 ATOM，含 MODEL 腿）的几何是
`add(multiply(a,c), multiply(b,f), c, b, p)` —— **交互乘法结构**，不是等权求和。

去掉 MODEL 腿 p、换成纯 INSIDERS 交互后：

```
h=vec_avg(insd1_holdings)
a=group_rank(ts_delta(ts_mean(h,44),44), sector)          # 持仓变化
b=group_rank(ts_ir(h,66), sector)                          # 持仓信噪比
c=group_rank(ts_mean(HHI_4,66), sector)                    # 集中度（微鲸）
f=group_rank(1/(days_from_last_change(h)+1), sector)       # 新鲜度
group_zscore(add(multiply(a,c), multiply(b,f), multiply(a,c,b), c), sector)
```

**冠军 `qM78axX1`：S 1.37 / F 1.01 / Y2 2.58 / sub 0.73 / TO 6.7% / eff=1**
- checks.pass 8 项全过（含 `IS_LADDER_SHARPE`、`CLUSTER_TEST`、`MATCHES_PYRAMID`）
- checks.fail **唯一 1 项：`LOW_SHARPE 1.37 < 1.58`**

## 五、逐年诊断：拖累年份明确

`qM78axX1` 逐年 Sharpe：

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.38 | 1.11 | 0.52 | 0.36 | **2.66** | **2.20** | 1.24 | 0.44 | 1.65 | **3.66** |

- **强年**：2018 / 2019 / 2023
- **弱年（拖累）**：2014 (0.38) / 2016 (0.52) / 2017 (0.36) / 2021 (0.44)
- 全期 S 1.37 被这四年拉低；近两年 S 2.58 说明结构在近期极强

## 六、已试无效的提 S 路径（约 60 臂）

| 路径 | 结果 |
|---|---|
| 加 DI 长窗 `ts_sum(ts_backfill(DI,66),252)` 作主腿 | S **1.03-1.27**（反而降）|
| DI × CORE 门控 | 1.25 |
| decay 10 | 1.23-1.26 |
| neut=FAST | 0.88-1.01 |
| nan=OFF | 0.32-0.72（崩）|
| truncation 0.05/0.12 | 1.32-1.36 |
| `winsorize(h,std=3)` 前处理 | 1.32 |
| `ts_zscore(h,44)` 替代 Δ | 1.31 |
| `group_neutralize(·,industry)` 内层 | 1.34 |
| `ts_mean(CORE,5)` 外层平滑 | 1.24 |
| `multiply(CORE,b)` 二次门控 | 1.05 |
| 二次交互 `multiply(c,b)` 加入 | 1.32-1.35 |
| 加 SV2 / 高管买卖比腿 | 1.16-1.25 |
| `signed_power` 1.4/1.5 | 1.27-1.35 |

## 七、S 天花板 1.37 的机制解释

1. **覆盖率 53.4%**（约 267 只/TOP500）⇒ 横截面宽度固定，信噪比有结构上限
2. **禁 cap 桶**（保 ATOM）⇒ 失去市值分层中性化（历史实测 value 0.63→0.90）
3. **两数据集同源**（coverage 0.5343 vs 0.5342）⇒ 互补的是「视角」而非「信息源」，边际信息有限
4. 交互结构已把两个视角榨到 `a×c`、`b×f` 三重交互，再加腿必稀释

## 八、结论

| 项 | 值 |
|---|---|
| 用户问题答案 | **是，可以组，且仍是 ATOM** |
| 当前最优 ATOM | `qM78axX1`：S 1.37 / F 1.01 / Y2 2.58 / sub 0.73 |
| 唯一 fail | `LOW_SHARPE 1.37 < 1.58`（差 0.21）|
| 距 1.58 | **−0.21**（此前的 1.30 上限已提到 1.37）|
| 是否可提交 | 否（LOW_SHARPE 未过）|

**从 0 颗新挖 ATOM 到 1 颗 S 1.37 的准 ATOM，且是首次证明 insiders 双集组合可保 ATOM 标签。**

## 九、BE200–BE206 补充扫描（2026-11-12 晚）

用户追问后追加 7 波 34 臂，全部 ATOM（eff=1）。

### BE201 买卖方向腿并入（6 臂，字段名修正后）

| 腿 | S | Y2 | sub |
|---|---:|---:|---:|
| SV2 Σ66 | **1.27** | 2.60 | 0.72 |
| SV2×c 交互 | 1.25 | 2.35 | 0.75 |
| 鲸鱼集中度 avg/total | 1.21 | 2.37 | 0.59 |
| 董事净买 | 1.19 | 2.26 | 0.67 |
| 高管净买 | 1.22 | 2.10 | 0.67 |
| 直接董事净买 | 1.17 | **2.85** | **0.77** |

⇒ 全部 < 冠军 1.37。**加方向腿 ⇒ S 降、Y2 升**（规律固化）。

### 轴扫描结果（决定性）

| 轴 | 值 | 结果 | 判定 |
|---|---|---|---|
| universe | TOP500 | 1.37 | ★ 唯一可用 |
| universe | TOP200 | — | ❌ 平台拒绝：DEU 合法仅 TOP500/TOP300 |
| universe | TOP300 | — | ❌ 「not available for EQUITY and region DEU」 |
| neutralization | SUBINDUSTRY | 1.37 | ★ 最优 |
| neutralization | FAST | 0.88–1.01 | ❌ |
| neutralization | MARKET | — | ❌ 平台侧运行报错 |
| truncation | 0.05/0.08/0.12 | 1.32–1.36 | 非关键 |

**⇒ universe 与 neutralization 两轴已穷尽，无提 S 空间。**

### BE205/206 换核心（12 臂）

按「换核心而非换搭档」纪律，把核心从「持仓动量×集中度」换成「新鲜度×集中度」：

| 构造 | S | Y2 |
|---|---:|---:|
| f×c + b×f + f | 1.09 | 1.39 |
| f×c + f + c | 1.05 | 2.12 |
| 三重 a×c×f（乘法串联） | 0.72 | 1.56 |
| f×c132 + f + c132 | 0.74 | 2.25 |
| 冠军 c→SV1 水平 | 1.15 | 2.64 |
| 冠军 +(1−c) 反向 | 0.52 | 0.48 |

⇒ **换核心同样失败，最高 1.15。**

### BE205 失败原因（工程记录）

`Found unused variables` —— 平台要求预定义变量**必须全部被引用**。声明了 `b` 但只在 `multiply(b,f)` 里用、或声明了未用的变量都会整批 ERROR。
**修法：全内联展开（不写变量赋值）**，BE206 据此成功。

## 十、最终结论：S 天花板 = 1.37（约 76 臂多路径确认）

| 轴 | 已穷尽的值 | 上限 |
|---|---|---|
| decay | 0 / 4 / 10 | 1.37 (decay 4) |
| nan_handling | ON / OFF | ON 必需，OFF 崩到 0.32 |
| neutralization | SUBINDUSTRY / FAST / MARKET | 1.37 (SUBINDUSTRY) |
| truncation | 0.05 / 0.08 / 0.12 | 1.36 |
| universe | TOP500 only | 1.37 |
| 腿结构 | 2/3/4/5 腿、加性/交互/门控/正交 | 1.37 (4 腿交互) |
| 换核心 | 新鲜度×集中度、SV1、反向 c | 1.15 |
| DI 长窗 | 126/252/504、门控、加权 | 1.27 |

**⇒ 差距定格：S 1.37 vs 闸 1.58，差 −0.21。**
**⇒ 但 Y2 2.58 / F 1.01 / sub 0.73 / TO 6.7% 全部过闸，仅剩 S 一维。**
