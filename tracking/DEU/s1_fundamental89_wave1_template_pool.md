# fundamental89 S1 台账（DEU / TOP500 / D1）

> 日期：2026-11-03　数据集：`fundamental89`（Accrual based Earnings Model）
> 平台元数据：407 字段全 MATRIX / valueScore 4.0 / userCount 195 / alphaCount 412
> 注意：论坛同机制帖把「Accrual based Earnings Model」标为 `other395`；两者是同一机制的**两个数据集**（other395 属 OTHER 塔 = trio，单用合法但不可与 PV/MODEL 组腿；fundamental89 属 FUNDAMENTAL 塔，非 trio）

## 一、字段画像（get_datafields 实证，407/407 complete）

**命名骨架**：`fnd89_<metric>_<sample>_<xy>`，159 个互异 stem。
- `<sample>` = `major`（MAJOR overlay）/ `other`；另有 `sector` / `industry` / `all` 横截面版（`csjones` 族）
- `<xy>` 七变体：**x = 分母轴**（1 = 总资产 / 2 = 流动资产 / 3 = 其他），**y = 分子口径变体**（1/2/3）
- 例：`fnd89_major_11_11` = (NI − CFO)/TotalAssets；`fnd89_major_11_21` = (NI − CFO)/CurrentAssets

**指标族（metric）**：

| metric | 含义 | 学术对应 |
|---|---|---|
| `major_1x/2x/3x` | 原始应计（NI/CFO/资产变动口径） | **Sloan (1996) accruals** |
| `jones_accrual` | Jones 模型时间序列总应计比率 | Jones (1991) |
| `jones_nondiscretionary_accrual` | **非可操纵**应计 | Jones 分解 |
| `jones_accrual_pct` | **可操纵（discretionary）应计占总应计比** | Dechow-Sloan-Sweeney (1995) 盈余管理 |
| `jones_accrual_r2` | Jones 模型 R² | 应计质量（Dechow-Dichev 2002 同族） |
| `csjones_all/industry/sector` | 横截面 Jones（行业/部门内估计） | 横截面版盈余管理 |
| `asset_41..64` | 资产负债表分项应计（流动/非流动/其他） | Richardson et al. (2005) 应计可靠性 |
| `fixed1313_d1_accum_4q` | **累计 4 季应计比率** | 年度化应计（更稳，慢变量） |

**拥挤度分布（关键选址依据）**：

| 字段 | alphaCount | users | 说明 |
|---|---:|---:|---|
| `fnd89_major_11_11` | **173** | 89 | Sloan 原始应计，该集最热 |
| `fnd89_major_13_11` | 37 | 27 | 含 D&A 的应计 |
| `fnd89_fixed1313_d1_accum_4q` | 36 | 24 | 累计 4 季 |
| `fnd89_jones_accrual_major_11` | **1** | 1 | 总应计（几乎无人用） |
| `fnd89_jones_accrual_pct_major_11` | **0** | 0 | 可操纵占比（**零人用**） |
| `fnd89_jones_nondiscretionary_accrual_major_11` | **0** | 0 | 非可操纵（零人用） |
| `fnd89_jones_accrual_r2_major_11` | **0** | 0 | 应计质量（零人用） |
| `fnd89_csjones_all_major_11` | **0** | 0 | 横截面 Jones（零人用） |

⇒ **核心机会**：Sloan 原始应计面已 173 alphas 拥挤，但**Jones 分解四件套（可操纵/非可操纵/R²/横截面）全部 0-1 users**——同一数据集内的低拥挤子面。

## 二、论坛取证

**帖 A `43691660126615`（24 赞）《应计异常这件事：从论文到数据》**
| 要点 | 原文 | 对设计的约束 |
|---|---|---|
| 机制 | 应计偏高 ⇒ 盈利质量偏低 ⇒ 后续收益弱（应计异常） | 主方向 **负向**（高应计做空） |
| **方向性** | **这类模型历史上偏「负面筛选」——更擅长指出谁的质量差，而不是保证谁涨** | 预期空头腿强、多头腿弱 ⇒ 注意 CW/多空不对称 |
| 环境依赖 | 应计异常强弱随市场环境、宏观周期变化，不可刻舟求剑 | 需查逐年 pnl 稳定性 |
| 定位 | **辅助视角**，与现金流/营业质量交叉，不单点依赖 | 本波先验单塔；弱则转条件腿 |

**帖 B `21149919634071`（10 赞）《Back to Fundamentals: The Accrual-Cash Flow Correlation, the Inverted-U Pattern, and Stock Returns》**
- 论文核心：应计与未来收益的关系是 **倒 U 型（inverted-U）**，不是单调；应计异象强度随经济因素动态变化
- 作者给的公式：`accrual_ratio = (income − (cashflow_op + cashflow_invst)) / total_assets`
- **★ 作者实测结论：「目前结果表现一般，Prod correlation 0.83」** ⇒ 应计面在平台**拥挤**，prod 墙高风险
- 评论补充：`regression_neut` / `ts_regression` 都有效果，可用 GA 搜索算子组合

**★★ 倒 U 型的设计后果（本数据集最关键约束）**：单调 `group_rank(accrual)` 只能捕捉单调段，**倒 U 型必须用非线性构造**：
- 极端度版：`group_rank(abs(ts_zscore(accrual, 252)))` —— 距中枢越远（无论正负）＝质量越可疑
- 或分段 gate：`trade_when(accrual > q_high, -accrual, ...)` / `trade_when(accrual < q_low, accrual, ...)`

## 三、论文取证（学术骨架）

| 文献 | 结论 | 可操作 |
|---|---|---|
| Sloan (1996) | 高应计 → 未来收益低（应计异象） | 主方向负向 |
| Jones (1991) | 应计 = 可操纵 + 非可操纵（回归分解） | 用差分提取可操纵部分 |
| Dechow-Sloan-Sweeney (1995) | Jones 模型检测盈余管理 | `jones_accrual_pct` 是现成度量 |
| Dechow-Dichev (2002) | 应计质量 = 应计与现金流的匹配度 | `jones_accrual_r2` 代理 |
| Richardson et al. (2005) | 应计可靠性随资产负债表分项递减 | `asset_41..64` 分项可信度分层 |

## 四、探针 P1-P6（已派发 f89_probe_20261103, pid 70584）

| P | 形态 | 目的 |
|---|---|---|
| P1 | `group_rank(fnd89_major_11_11, subindustry)` | **基准对照**（最热字段，看 DEU 应计方向与强度） |
| P2 | `group_rank(fnd89_jones_accrual_major_11, subindustry)` | Jones 总应计（低拥挤，与 P1 口径对比） |
| P3 | `group_rank(fnd89_jones_accrual_pct_major_11, subindustry)` | 可操纵应计占比（最纯盈余管理面） |
| P4 | `group_rank(subtract(jones_accrual, jones_nondiscretionary), subindustry)` | 可操纵绝对量（Jones 分解差分） |
| P5 | `group_rank(fnd89_jones_accrual_r2_major_11, subindustry)` | 应计质量（低 R² = 低质量） |
| P6 | `group_rank(subtract(csjones_all_major_11, jones_accrual_major_11), subindustry)` | 横截面 vs 时间序列背离（信息含量差） |

双预检：verify_expr 6/6 valid；preflight `valid:true` / `unknown_fields:[]`。

## 五、正式波 T1-T12 设计草稿（≥10 结构互异）

| T | 骨架 | 结构差异点 | 来源 |
|---|---|---|---|
| T1 | `group_rank(ts_rank(fnd89_major_11_11, 252), subindustry)` | 基准 × 长窗时序分位（低换手） | Sloan 1996 |
| T2 | `group_rank(ts_delta(fnd89_major_11_11, 66), subindustry)` | **应计变化**（增量而非水平） | Sloan 引申 |
| T3 | `group_rank(fnd89_jones_accrual_pct_major_11, subindustry)` | 可操纵占比（零拥挤） | DSW 1995 |
| T4 | `group_rank(subtract(jones_accrual, jones_nondiscretionary), subindustry)` | Jones 分解差分 | Jones 1991 |
| T5 | `group_rank(abs(ts_zscore(fnd89_major_11_11, 252)), subindustry)` | **倒 U 型·极端度**（非线性） | 倒U论文 |
| T6 | `trade_when(fnd89_major_11_11 > ts_quantile(fnd89_major_11_11, 252), group_rank(multiply(fnd89_major_11_11, -1), subindustry), -1)` | **倒 U 型·高段 gate**（仅高应计做空） | 倒U + 负面筛选帖 |
| T7 | `trade_when(fnd89_jones_accrual_r2_major_11 > ts_quantile(fnd89_jones_accrual_r2_major_11, 252), group_rank(fnd89_jones_accrual_pct_major_11, subindustry), -1)` | **质量 gate × 可操纵比**（只在高质量样本用盈余管理信号） | Dechow-Dichev |
| T8 | `group_rank(ts_rank(fnd89_fixed1313_d1_accum_4q, 504), subindustry)` | 累计 4 季应计 × 长窗分位（年度慢变量） | 慢变量定律 |
| T9 | `group_rank(ts_zscore(fnd89_fixed1313_d1_accum_4q, 252), subindustry)` | 年度应计的自身基线标准化（zscore 金型第三次跨集测试） | oth699 金型测试 |
| T10 | `group_rank(divide(fnd89_major_11_11, fnd89_jones_accrual_major_11), subindustry)` | **原始应计 / Jones 应计**（模型解释力比值） | 自建 |
| T11 | `group_rank(ts_corr(fnd89_major_11_11, fnd89_jones_accrual_major_11, 252), subindustry)` | 两口径**相关性**（口径一致性 = 数据可信度代理） | 帖B（accrual-CFO 相关性） |
| T12 | `group_rank(ts_delta(fnd89_jones_accrual_pct_major_11, 252), subindustry)` | 可操纵占比**年度变化**（盈余管理恶化速度） | 自建 |

## 六、★★★ 宽度实证判死（2026-11-03，探针 P1 逐年 longCount 核查）

`get_alpha_yearly_stats(alpha_id=2rApvagZ)`（P1 Sloan 基准臂）：

| 年份 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **longCount** | **0** | **0** | **0** | 1 | 1 | 1 | 1 | 1 | 1 | **0** |
| pnl | 584K | −343K | 425K | 879K | −1.04M | −1.57M | −1.14M | −156K | −504K | −339K |

**判读**：多头持仓 **0–1 只**，pnl 全部来自空头腿 ⇒ 该表达式在 DEU/TOP500 上实际是「纯空头 1 只股票」的组合，**完全不可交易**。S=−0.38 方向虽符合 Sloan 先验（高应计→低收益），但基数为 0–1 只，无任何统计意义。

**★★ 关键推论（修正 §3775 的旧判据）**：平台 `alphaCount` / `userCount` 是**全局统计，不区分 region/universe**。`fnd89_major_11_11` 的 173 个 alpha 来自**其他 region**，在 DEU/TOP500 上该字段宽度 0–1。⇒ **「alphaCount 极低 ⇒ prod 天然低 ⇒ 蓝海」这条旧判据方向错了**：低 alphaCount 更常见的真相是**「该 universe 下根本没数据」**。

**判定：`fundamental89` 判死（宽度 0–1）**，剩余 4 臂跑完仅作取证，不进正式波。

## 七、风险登记

1. **prod 墙高风险**：帖 B 作者实测 prod correlation **0.83**；应计面在平台已被占。缓解：优先用 0-1 users 的 Jones 分解字段（T3/T4/T7/T12），它们不在任何人的 alpha 里。
2. **倒 U 型**：单调 rank 必然表现平庸，T5/T6 是非线性正解；若 P1-P6 探针全弱，优先怀疑单调假设而非数据。
3. **负面筛选特性**：多头腿可能天然弱 ⇒ 关注 CW FAIL 与多空比例（DEU 历史多次栽在这）。
4. **财报数据频率**：季度更新，日频窗口上 `ts_delta(x,5)` 会退化（workforce 已踩过 T5 恒零）⇒ 窗口一律 ≥66。
