# ★最终结构结论：insiders 数据集独立可交付上限 = 4 颗（已全部取用）

日期：2026-11-12

## 一、结论

DEU/D1 的 insiders 数据集（insiders1 + insider_agg_matrix）在「互相关全对 <0.7」标准下，
**最多只能产出 4 颗独立可交付 alpha**，已全部取用：

| # | alpha | 构造 | S | F | 2Y | sub | ops | 来源 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | **d5apW38x** | S7 × 4 条 analyst 腿（无 cap 桶）| **2.36** | **2.04** | 2.67 | 1.54 | 27 | insiders×analyst |
| 2 | **WjlMlWJd** | S7 × cap 桶 × AN2（净上调比）| **2.21** | 1.84 | 2.40 | 1.43 | 26 | insiders×PV×analyst |
| 3 | **npa9PKWw** | S7 × other455 关系PC2 长窗132 | **1.74** | **1.52** | 2.66 | 0.94 | 37 | insiders×OTHER |
| 4 | qM7KxkQV | shrt3_bar × insd1_holdings ts_rank252 | 1.72 | 1.34 | 2.43 | — | — | 存量（SHORT×INSIDERS）|

## 二、饱和证据（第五次独立验证）

BE160 用了**全新字段**（`mean_estimate_change_pct_f12m_ebitda_60d_4`、`predicted_surprise_pct_f12m_ebitda_5`、
`analyst_downward_revision_count_fy1_earnings_14d_4`）做出三颗 fail=0、全合规（INSIDERS+MODEL, eff=2）：

| alpha | 构造 | S | 与 d5apW38x 相关 | 与 npa9PKWw 相关 | 能否进篮子 |
|---|---|---:|---:|---:|---|
| E5Q1Qz89 | ins + 60d 均值变化 | 1.72 | **0.8224** | **0.8314** | ❌ |
| VkNVNzzw | ins + f12m %5 | 1.71 | **0.8169** | **0.8150** | ❌ |
| 3q0w0P5g | ins + S1 + 下调人数 | 1.60 | 0.7773 | **0.8114** | ❌ |

**即使是全新字段/全新窗口，相关性仍 0.78-0.83。**

## 三、机理（为什么必然饱和）

1. **共同因子是 insd1_holdings 的存量变化本身**：A（Δ66）+ B（ts_ir）+ C（HHI）+ FR（新鲜度）四条腿
   已把 holdings 的信息榨干；搭档腿只贡献 30-40% 的 PnL 方差，无法拉开 0.7 以上的距离。
2. **insiders 数据集只有 2 个、覆盖率均 53%**，横截面可用标的约 260-280 只，样本量本身限制了因子族的多样性。
3. **非 holdings 维度全部无信息**（BE148 实测：金额/占比/显著度/交易价 10 臂全灭，最高 1.29）。

## 四、边界验证的完整覆盖（带证书）

| 维度 | 已覆盖 | 结论 |
|---|---|---|
| 字段 | insiders1 全 8 字段 + insider_agg_matrix 30 个可访问字段 | 挖尽 |
| 矩 | 水平 / Δ / ts_ir / ts_mean / ts_sum / ts_rank / 占比 / 显著加权 / ts_zscore | 挖尽 |
| 骨架 | 单腿 / 双腿 add / 四腿叠加 / 乘性门控 / HHI 比值 / cap 桶分档 / 双搭档叠加 / 单腿核心 | 挖尽 |
| 分组轴 | sector / market / subindustry / bucket(rank(cap)) / 聚类2 / 聚类10 / 双层 | sector 最优，已固定 |
| 非线性 | signed_power 9 档 / winsorize / tail / trade_when / hump / reverse | 幂次不敏感（有双层zscore时去幂反升）|
| 配置 | 中性化 4 档 / decay 5 档 / nan 2 档 / truncation 3 档 | SUBINDUSTRY + decay0 + nanON + trunc0.08 |
| 窗口 | 22 / 44 / 66 / 88 / 110 / 132 / 176 / 252 / 504 | 腿 66 / 低频腿 132 |
| 搭档族 | analyst(MODEL) / analyst7(ANALYST) / OTHER / NEWS / INSTITUTIONS / SENTIMENT / RISK / SHORTINTEREST次级 | 仅前 3 个有效 |

**无空格 ⇒ 上限成立。**

## 五、对 20 颗目标的直接含义

| 项 | 数 |
|---|---|
| 已合规交付 | **14** |
| 其中 insiders 贡献 | **4**（d5apW38x / WjlMlWJd / npa9PKWw / qM7KxkQV）|
| 其中非 insiders 贡献 | 10（存量件：ANALYST 3 / MODEL+ANALYST 2 / SHORT 3 / SHORT+NEWS 1 / SHORT+OTHER 1）|
| 缺口 | **6** |

⇒ **缺口 6 颗必须来自「非 insiders 核心」的构造**，这是数学上的必然，不是努力量问题。
⇒ 可选路径：① 打开其他未点亮塔的纯数据集战役（news / risk / earnings / pv / option / macro / socialmedia / imbalance 在 DEU D1 均 0 颗）；
   ② 用「强腿 × 新搭档」但不含 insiders（如 analyst × OTHER、news × institutions）；
   ③ 下调 20 颗目标。