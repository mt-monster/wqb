# EUR / investor_activity 零售流向 ATOM 突破报告（2026-11-20）

> 数据集：`investor_activity`（47 字段全 VECTOR，cov 0.1644，aC 0–120 极冷门，2026-03-01 新 onboard）
> 塔位 EUR/D1 **PV 2/3（差 1 席）**｜mult 1.1｜**PV 类不得两两组腿 ⇒ 只能单集 ATOM**
> 画像：`tracking/EUR/reference/profiles/eur_pv_investor_activity_profile_20261120.md`（完整性闸 47/47 PASS）
> 回测：**59 臂**（wave=mcp-20261120, dataset=investor_activity）
> 结论：**信号层与平台闸全绿（S 最高 2.84 / F 2.08 / 2Y 2.49 / sub1.85），prod 0.78–0.84 信息源墙未破 ⇒ PROVISIONAL（未提交）**

## 1. 机制与证据

- **论文**（12 篇/8 作者，多样闸 PASS）：*Active Attention, Retail Investor Base, and Stock Returns*（JBF 2023）、
  *Individual Investor Trading and Stock Returns*（JFE 2008，Barber-Odean）、*Retail investor attention and stock liquidity*（JIMF 2015）。
- **论坛**：无该集专帖。
- **核心机制**：把「零售 vs 专业」的资金流拆开 —— 散户净买入与专业净买入的**分歧**。

## 2. ★ 突破一：presence 门控是本族决定性杠杆（今日门控判据第三次验证）

| 形态 | S | F | 2Y | sub | failed_ra |
|---|---:|---:|---:|---:|---:|
| 无门控 骨架 | 0.91 | 0.62 | **−0.08** | 0.79 | 3 |
| + `trade_when(vec_avg(total_trading_turnover_eur) > 0, ·, −1)` | **2.36** | **1.00** | **3.12** | 1.55 | **0** |

**判据「cov < 0.6 才试门控」第三次成立**：
earningscall cov0.51（S 0.51→1.76）✅ / investor_activity cov0.16（S 0.91→2.36）✅ / institutions cov0.88（8 臂全灭）❌。
**机制解释**：该族信息只存在于「有成交的日子」，无成交日的读数是稀释噪声。

## 3. ★ 突破二：散户方向与经典文献相反

`subtract(0, rank(net_retail_net))` = **S−2.52** ⇒ **散户净买入正向是强正 alpha**（S≈+2.84）；
`net_professional_net` 正向 = **S−2.61** ⇒ 专业买入是坏信号。
⇒ 与 Barber-Odean「散户过度反应后反转」**方向相反**（该文献在本区不成立）⇒ **跨区/跨期先验不可照搬**。

## 4. ★ 突破三：decay 阶梯同时解 TO 并抬 F

| decay | S | F | 2Y | TO | failed_ra |
|---|---:|---:|---:|---:|---:|
| 4 | 2.36 | 1.00 | 3.12 | 59.4% | 0 |
| 16 | 2.61 | 1.80 | 2.24 | 25.9% | 0 |
| **24** | 2.52–2.65 | **1.98–2.11** | 1.92–2.28 | **19.9–21.7%** | 0 |

⚠ `hump` 与 `ts_mean` 内层是**摧毁器**（S 0.34/0.58）；`ts_target_tvr_decay(target_tvr=0.1)` 亦有效（S2.47/F1.56/TO28.4%）。

## 5. 逐层算子替换 Δ 表（用户新规则的完整执行）

| 层 | 替换 | 结果 |
|---|---|---|
| **时序算子层**（ts_* 同类全替换，8 条） | ts_rank / ts_quantile / ts_av_diff | **2.48–2.72 ✅** |
| | ts_delta / ts_std_dev / ts_scale / ts_ir | **0.05–0.68 ❌ 全灭** |
| **截面算子层**（group_* 全替换） | group_zscore / group_neutralize / group_scale | 1.89–2.20（略低于 group_rank） |
| **核字段层** | 散户净额 / 专业净额反向 / 差分 | **2.84 / 2.84 / 2.68**（同号同信息） |
| **窗口层** | zscore 252 / 504 / 756 | 504 最优（+0.25 S） |
| **轴层** | industry / sector / subindustry / market | sector ≈ industry > subindustry |
| **门控层** | 总成交额 / 总订单数 / 散户成交额 / ts_sum 22 宽门控 | **2.36–2.40（几乎无差 ⇒ 门控字段不改变 PnL 形状）** |
| **新维度**（6 条） | 订单失衡 / 日内振幅 / 收盘开盘比 / 均价差 / 成交额占比 | **全灭（S −0.44~0.81）** |
| **幅度形态** | winsorize0.35 / signed_power1.5 / 差分×订单数 | 2.59–2.68（无增益） |

## 6. prod 墙（未破）

| 变体 | prod |
|---|---:|
| 差分 + ts_zscore + industry + decay4 | 0.8198 |
| 差分 + ts_quantile + industry + decay4 | **0.7888（最佳）** |
| 差分 + ts_zscore + industry + decay16 | 0.7947 |
| 差分 + ts_zscore + sector + decay16 | 0.8158 |
| 散户净额 + sector + decay16 | 0.8444 |

**梯度有效（每层降 0.02–0.03）但需再降 0.09–0.14** ⇒ 「零售资金流」在生产池已有饱和实现（与 earningscall 0.78 / institutions 0.89 同类）。
⚠ **prod 最优 ≠ S 最优**（ts_quantile 的 S 略低但 prod 最低；sector 轴 S 最高但 prod 差 0.02）⇒ 选候选要同时看两表。

## 7. 判定与后续

- **平台闸**：多颗 `failed_ra_count=0`（checks.fail 空），最优 `xAvrAo9w` S2.84/F2.08/2Y2.49/TO27.4%/sub1.85/invest1.61；
  **TO 达内部严线的最优 = `Xga9mpqa`（decay24, TO19.85%/S2.52/F2.01）**。
- **prod 0.79–0.84 ⇒ 不可提交**（红线 0.7 / 内部严线 0.65）。
- **不判数据集死** ⇒ **PROVISIONAL**。
- **下一步**：宇宙轴（TOPCS1600/TOP1200，换持仓股票集最可能改 prod）→ 若仍 >0.7，转 §7.7 regular fallback：
  PV 主腿 + **非 PV 类**辅助腿（gating/residual/ratio 四形态，跨类配额 1/5）。
