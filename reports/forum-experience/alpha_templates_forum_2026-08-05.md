# WorldQuant BRAIN 论坛 Alpha 模板合集与总结

> 拉取时间：2026-08-05 | 数据来源：WorldQuant BRAIN 官方论坛（`support.worldquantbrain.com`）+ 官方文档「Alpha Examples for Beginners」/「Power Pool Alphas」
> 覆盖：论坛搜索 "alpha template" 返回的 50 篇帖子中的高价值模板贴（含 `Machine Alpha 进阶知识` 系列、`Alpha灵感` 系列、`Alpha Template` 系列）+ 官方入门示例 + Power Pool 准入门槛
> 说明：论坛模板贴多为「经济逻辑 + 抽象表达式 + 可替换插槽」的形式，便于批量枚举。本文把所有**可落地表达式**与**抽象模板骨架**一并抽出，便于直接套用。

---

## 0. 与当前 EUR PPA 挖掘任务的关系（必读）

我们当前在 `ml_factor_proj`（EUR/TOP1200/D1）挖 3 个 PPA，本质是产 **Power Pool Alpha**。官方对 Power Pool 的硬性门槛（取自「Power Pool Alphas」文档）：

| 指标 | 阈值 |
|---|---|
| Sharpe | **≥ 1.0** |
| 唯一 operator 数（重复计、ts_backfill/group_backfill 不计） | **≤ 8** |
| 唯一 data field 数（分组字段不算） | **≤ 3** |
| Power Pool Correlation | **< 0.5** |
| Turnover / Sub-universe / Robust-universe 测试 | 必须 PASS |
| Self-Correlation（与已提交 PP alpha） | 若 > 0.5，则需比最相关者 Sharpe 高 10% |

**结论**：下面 §1–§5 中「差异/期限结构」「小稳反转」「信息论」三族天然契合 Power Pool（算子少、字段少、PC 易低），应作为 EUR 挖掘优先模板；§2 估值族跨 region 拥挤度高，PC 易 >0.5，需做差异化（换字段/换 region）。

---

## 1. 时间序列反转 / 动量族（最易过 Power Pool 闸门）

### T1. Delta 反转（经典短期反转）
- **作者**：XD81759（20 赞）｜贴：`【Alpha灵感】Template：Delta反转`
- **表达式**：`-ts_delta(A, 3)`
- **逻辑**：短期涨多必回落、跌多必反弹；负号为「涨做空、跌做多」。
- **泛化要点**：
  - 量价数据（pv1 / model77 等日频）窗口用 `3`；**基本面/季度数据改用 `66`（约一季度）**，Sharpe 可从 0.5 → 1.2+（评论实测）。
  - 组合增强：`-ts_delta(A,3) * ts_std_dev(A,20)`（反转+波动率）。
  - 平滑：`ts_mean(close,3)` 替代 `close`；`winsorize(close, std=4)` 截断极端值。
  - 筛选经验：`|sharpe|≥1.2`、`turnover≤0.4`、`|margin|≥0.0009`，再加「近 2 年 Sharpe>0」过滤失效 alpha。

### T2. 小而稳（低换手 & 低换手波动率）
- **作者**：XD81759（25 赞）｜贴：`【Alpha灵感】Template：小而稳`
- **表达式**：`-A * ts_std_dev(A, 30)`
- **逻辑**：做多「字段值本身低 + 其 30 日波动也低」的股票（量小、量稳）。
- **泛化**：窗口与字段皆可换；已在 pv1/model77（548 字段）扫出 7 个可提交候选（sharpe>1.25）。

### T3. Operating Earnings Yield（盈利动能）
- **来源**：官方入门示例｜`ts_rank(operating_income, 252)`
- 设置：`SUBINDUSTRY` 中性、trunc 0.08、pasteurization ON、delay 1。
- 提示：可改比率形式纳入股价动量与纯基本面比较。

### T4. Appreciation of Liabilities（负债公允价值恶化）
- **来源**：官方入门示例｜`-ts_rank(fn_liab_fair_val_l1_a, 252)`
- 设置同上（SUBINDUSTRY）。

---

## 2. 截面比较 / 估值族

### T5. 基础模板（fundamental 跨行业排名）— 一切模板的起点
- **作者**：WL13229（64 赞）｜`Machine Alpha 基础知识1：什么是Alpha模板`
- **示例**：`group_rank(ts_rank(eps, 252), industry)`
- **抽象骨架**（核心范式，后续所有模板都从这推）：
  ```
  <group_comparete_op>( <ts_compare_op>( <company_fundamentals>, <days>, <group> ) )
  ```
  - `<company_fundamentals>`：EPS / DPS / CPS / BPS / EBIT / 销售额 …（可任意替换）
  - `<ts_compare_op>`：ts_rank / ts_zscore / ts_delta / ts_avg_diff …
  - `<group_compare_op>`：group_rank / group_zscore / group_neutralize …
  - `<days>` / `<group>`：回溯窗、分组维度（industry/subindustry/market…）均可调。

### T6. Earnings Yield Momentum（盈利收益率动量）
- **来源**：官方入门示例｜`group_rank(ts_rank(est_eps/close, 60), industry)`
- 设置：`INDUSTRY` 中性；提示用 NAN HANDLING 预处理提升表现。

### T7. PEG 比率估值
- **作者**：WL13229（14 赞）｜`Machine Alpha 进阶知识6：PEG`
- **表达式**：`-group_zscore(P/E/G - 1, industry)`
- **逻辑**：PEG<1 相对低估、>1 高估；行业标准化捕捉相对错估。
- **抽象**：`<group_compare_op>( <cs_compare_op>(P/E, G), <group> )`，`cs_compare_op` 可选 subtract/divide/vector_neut/regression_neut。
- **注意**：除法（P/E/G）假设估值随增长**比例**变，减法（P/E-G）假设**线性**平移，两者选股池与换手差异大（评论实测）。

### T8. 戈登增长模型（GGM）内在价值
- **作者**：WL13229（11 赞）｜`Machine Alpha 进阶知识5：Gordon`
- **表达式**：`group_zscore( <D(t=1)> / (<r> - <g>) - ts_mean(close, 21), industry )`
- 其中 `D(t=1)=D(t=0)*(1+g)`，`g=b*ROE`，`r=Rf+beta*(Rm-Rf)`。
- **抽象**：`<group_compare_op>( <cs_compare_op>(D/(r-g), ts_mean(price,21)), <group> )`。
- 适用：稳定、成熟、股息可预测的公司；`D` 可换 cash flow / earnings。

### T9. Power of Leverage（杠杆力）
- **来源**：官方入门示例｜`liabilities/assets`
- 设置：`MARKET` 中性、trunc 0.01；跨行业差异大，可考虑换中性化维度。

---

## 3. 差异 / 期限结构族（Power Pool 最优候选）

### T10. 分析师数据期限结构（estimate term structure）
- **作者**：WL13229（19 赞）｜`Machine Alpha 进阶知识3：期限结构`
- **表达式**：
  ```
  group_zscore(
    subtract(
      group_zscore(anl14_mean_eps_fp1, industry),
      group_zscore(anl14_mean_eps_fp2, industry)
    ), industry)
  ```
- **逻辑**：同一指标（`anl14_mean_eps_` 前缀）不同时间范围（fp1 下一季 / fy1 下一年）的行业标准化差，捕捉预期增长差异。
- **关键**：**前缀必须一致**，避免无意义随机比较。
- **泛化**：把 `fp1/fp2` 换成任意「中缀表示时间窗」的字段对（评论实测 ASI 另类数据 `oth455_relation_roam_w1/w2/w5_pca_fact*` 同构，w 为周窗口，`ts_delta(...,22)` 验证信号在 22 天）。
- **抽象**：`<gco1>( <diff>( <gco2>(X_<p1>, <g2>), <gco3>(X_<p2>, <g3>) ), <g1> )`

### T11. 杜邦分析（ROE 分解）
- **作者**：WL13229（15 赞）｜`Machine Alpha 进阶知识4：DuPont`
- **表达式**：`group_zscore(subtract(ts_zscore(<ROE数据>, <days>), ts_zscore(<利润率数据>, <days>)), industry)`
- **逻辑**：ROE = 利润率 × 资产周转率 × 权益乘数；比较「行业标准化后的 ROE 时间序列」与「利润率时间序列」之差，找利润率被低估/隐藏价值的公司。
- **实测**：`subtract` 与 `ts_regression` 曲线相似；ROE 类数据更新不连续，窗口拉长平滑效果不明显，`ts_rank` 略平滑但换手上升。
- 落地示例（评论）：`-group_zscore(subtract(ts_zscore(rsk62_return,252), ts_zscore(anl4_sadaf_netprofit_mean,252)), subindustry)`

### T12. 预期质量评估（分析师关注度 + 分歧度）
- **作者**：JS30938｜`【Alpha Template】基于预期质量的评估策略`
- **表达式**：`if_else(greater(act_q_bps_surprisenum, 5), ts_scale(act_q_ebi_surprisestd, 60), 0)`
- **逻辑**：仅对「分析师估计数>5」的高关注、高流动性股票，用其 EBIT 预期分歧度的 60 日时序标准化作信号；非价格数据，天然跨股票可比。
- **优化网格**（评论建议）：关注度阈值 3/5/8/10 × 窗口 30/60/90 × 外层 ts_scale/ts_zscore/ts_rank 分别对照；可换 revenue/eps 等字段的分歧度。

---

## 4. 信息论 / 行为金融族

### T13. 信念熵值幂放大（ASI broker 行为分歧）
- **作者**：LH94963（94 赞，高赞）｜`【Alpha 模板】ASI 点亮 broker Pyramid`
- **表达式**：`signed_power(ts_entropy({field}, 144), 0.618)`
- **逻辑**：用信息熵量化「预测不确定性」，以黄金比例 `0.618` 幂次非线性放大强信号、压制弱信号（保持符号）。
  - 高熵 = 信念高度随机、市场分歧巨大 → 强信号；低熵 = 意见一致 → 弱信号。
- **二阶组合**：`ts_mean(-signed_power(ts_entropy(vec_sum(brk1_conviction_flag), 144), 0.618), 120)`
- **场景**：行为分歧策略（极端高做多/低做空，配行业/规模中性）；或作为「预测质量调节系数」与其他 alpha 相乘提信息比率。
- **争议/注意**（评论）：144/0.618 为经验值，可能过拟合；对异常值敏感；二阶组合略有「厂」感。ASI broker 交的人少 → PC 普遍低，适合点亮 Pyramid。

### T14. 半方差（下行波动反转）
- **作者**：XD81759（23 赞）｜`【Alpha灵感】Template：半方差`
- **逻辑**：论文结论需加负号才盈利——反转信号，做多「30 天内向下波动大」、做空「向上波动大」的股票（基于 SSRN 2565660）。与 T2 同源，优化后提升 Returns/Drawdown 比。

---

## 5. 注意力 / 情绪稳定性族

### T15. 短期情绪量稳定性
- **来源**：官方入门示例｜`-ts_std_dev(scl12_buzz, 10)`
- **逻辑**：某股 10 日情绪量 std 高 = 投资者注意力不稳定（由短期新闻/炒作驱动）→ 之后易跑输；取负做多稳定者。
- 提示：更短窗口对流动性好的股票更有效的可能性。

---

## 6. 方法论：模板抽象 + 参数优化

### 6.1 通用模板骨架（贯穿 §1–§5）
所有具体模板都可还原为：
```
<group_compare_op>( <diff_op>( <group_compare_op>(X_<a>), <group_compare_op>(Y_<b>) ), <group> )
```
每一步插槽（operator / field / window / group）**都可替换**，经济直觉不变 → 系统性枚举因子空间。

### 6.2 参数优化（爬山算法）
- **作者**：WL13229（14 赞）｜`Machine Alpha 进阶知识1：参数优化案例一`
- **流程**：初始化 → 模拟评估 → 随机选邻域参数 → 重模拟 → 改进则更新 → 连续 10 次无改进停止。
- **已知归纳偏差与改进**（高赞评论总结）：
  1. **局部最优** → 模拟退火 / 遗传算法（交叉变异）；
  2. **参数独立假设** → 协同变异 / 贝叶斯优化建模联合分布；
  3. **单目标偏差**（只看 Sharpe）→ 多目标帕累托（Sharpe × turnover × 稳健性）；
  4. **无记忆重复评估** → 缓存已评估组合 + 高斯过程代理模型（EI）；
  5. **随机无方向** → 强化学习策略网络引导搜索。

---

## 7. 模板族速查表（落地用）

| 族 | 代表模板 | 典型表达式 | Power Pool 适配 | 关键调参 |
|---|---|---|---|---|
| 反转 | Delta反转 | `-ts_delta(A,3)`（季频 `66`） | ★★★ | 窗口、乘波动率 |
| 反转 | 小而稳 | `-A*ts_std_dev(A,30)` | ★★★ | 窗口、字段 |
| 估值 | 基础排名 | `group_rank(ts_rank(eps,252),industry)` | ★★☆ | group、ts算子 |
| 估值 | PEG | `-group_zscore(P/E/G-1,industry)` | ★★☆ | 除法vs减法 |
| 估值 | GGM | `group_zscore(D/(r-g)-ts_mean(close,21),industry)` | ★★☆ | D/r/g 来源 |
| 差异 | 期限结构 | `group_zscore(sub(gz(X_fp1,ind),gz(X_fp2,ind)),ind)` | ★★★ | 前缀一致、中缀 |
| 差异 | 杜邦 | `group_zscore(sub(ts_zscore(ROE,d),ts_zscore(margin,d)),ind)` | ★★★ | 窗口、算子 |
| 差异 | 预期质量 | `if_else(>5, ts_scale(disp,60),0)` | ★★★ | 阈值、窗口 |
| 信息论 | 信念熵 | `signed_power(ts_entropy(f,144),0.618)` | ★★☆ | 熵窗、幂次 |
| 情绪 | 量稳 | `-ts_std_dev(scl12_buzz,10)` | ★★★ | 窗口 |

---

## 8. 给 EUR 挖掘的下一步建议（衔接 ml_factor_proj）

1. **优先套用 §3 差异族 + §1 反转族**：算子 ≤8、字段 ≤3，最易满足 Power Pool Sharpe≥1.0 / PC<0.5。
2. `ml_factor_proj` 已有 `active_return` 10 窗口（1m/3m/…/60m）与 `change_*` 族 → 天然适配 **T10 期限结构**（不同窗口的 `change_*_active_return` 做行业标准化差）与 **T11 杜邦式 spread**（两个基本面变化率做差）。
3. 参数优化直接用 §6.2 的「网格 + 帕累托」而非纯爬山，避免局部最优。
4. 提交前过 `prod_corr<0.7` / `self_corr<0.5` 硬闸门，打 `PowerPoolSelected` 标签。

---

*注：论坛另有多篇「乐高式积木拼装」「Gemini CLI 全自动模板工作流」「双字段 alpha 构建」「Python Alpha 转写」等元方法贴，以及 Option Greeks / CAPM 等扩展模板（未在本文逐篇抽取，可按需再拉）。*
