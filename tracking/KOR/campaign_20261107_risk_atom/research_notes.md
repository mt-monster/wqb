# research_notes · KOR Risk（2026-11-07）

## 论坛取证（通道 A）

### risk70 帖 43621466539671（USA/D1 158 字段分型）
- **区域前缀不通用**：USA=`usfast`，ASI/HKG/KOR=`asetrd`，GLB=`gemtrd`，EUR=`euetrd`。KOR 实测用 `asetrd`（preflight 已验）。
- **★ 单字段直用基本没信号**：HKG 实测 `ts_min(ts_backfill(anlystsn,252),66)` IS Sharpe **0.41** / fitness 0.17。
  ⇒ **载荷类字段的价值在组合，不在单点**。本战役 R01–R08 有 4 条是单字段直用，预期偏弱，须尽快转组合。
- 推荐结构：
  1. **特异收益÷特异风险**：`ts_zscore(daily_specific_return, 60)`；量纲要对齐（srisk 是 %-squared ⇒ 开方再除 √252）
  2. **风险收缩幅度**：`srisku − srisk`，差值越大模型回收越多 = 数据质量维度
  3. **反转期限结构**：`ltrevrsl − strevrsl`
  4. **行业暴露做回归中性化**：`regression_neut(ts_zscore(dsrt,60), industry_factor_banks)`（risk70 无 GROUP 字段，行业只能进 X）
  5. 多空两侧拥挤度对比：持股比例/家数 比值 × short_interest
- 坑：loading 类厚尾 ⇒ 组合前先 `winsorize` 或 `ts_zscore`。

### risk88 帖 43622632452631（纯净残差漫谈）
- risk88 = 剔除市场 + **全部风格因子**收益后的特质残差 ⇒ 比 risk70 的 dsrt 更纯，**更适合做均值回归**。

## 论文取证（通道 B）
- Kim & Lee 2017「Aggregate idiosyncratic volatility and stock return predictability: Evidence from the Korean stock market」⇒ **KOR 本地证据**，总体特质波动可预测。
- Ang et al. 2006 idio vol puzzle；Frazzini-Pedersen BAB；D'Avolio 2002 借券约束。
- Bozhkov 2020：**mean-reverting** 特质波动部分才是被定价的（支持「反转」而非「纯波动水平」）。

## 双通道裁决
- 通道 A（论坛 risk70/risk88）与 B（KOR idio vol 论文）**指向同一机制**：特质残差反转 + 特质风险。⇒ 优先组装。
- 但 A 明确警告单字段直用无效 ⇒ **R1 之后必须立刻转组合结构**（本战役最大风险点）。

## ⛔ 幽灵算子拦截（本回合，避免整批 CANCELLED）
- 论坛 risk70 帖给的 `regression_neut(ts_zscore(dsrt,60), 行业载荷)` —— **`regression_neut` 不是平台算子名**。
  - 依据：`Claude/skills/wq-brain-ra-kor/references/*.md` 全局锁定条目明示「'regression_neut' 仍非平台算子名；'vector_neut' 平台可用」。
- 替代：`ts_regression(y, x, 252, lag=0, rettype=0)` 取残差；或 `vector_neut` / `group_neutralize`。
- ✅ `winsorize` 平台可用，且是 prod 承重件（算子矩阵标 ⭐）。
- **教训**：论坛帖的算子名不可直接照抄到 KOR，落池前必须过本地算子矩阵核对。

## 论坛工具故障
- `get_glossary_terms` 报 `ERR_CONNECTION_CLOSED`（support 站不可达）⇒ 按 fail-closed 纪律：**工具故障 ≠ 论坛无解**，改用本地算子矩阵替代核验。
