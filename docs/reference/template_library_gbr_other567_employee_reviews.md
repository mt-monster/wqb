# GBR `other567`（Employee Review Data）模板库

> 区域 `GBR` / `TOP700` / `D1`。归属 **OTHER 塔**（GBR D1 当前 other=1，需 2 个）。
> 本文件是**派发前**的模板设计台账，含 12 个结构互异模板、来源标注、预注册判据。

---

## 1. 数据集画像

| 项 | 值 |
|---|---|
| dataset id | `other567` |
| 名称 | Employee Review Data |
| 字段数 | **48，全部 VECTOR** |
| users / alphas | 9 / **11**（极低拥挤） |
| valueScore | **7.0**（满档） |
| 时间粒度 | **company-month 月度面板**（`oth567atlas_month` 为 vendor 月键） |
| 评分标度 | 大部分 **1–5 分**（天然无量纲、同单位） |

**★ 与 `fundamental1` 的关键差别**：`fundamental1` 是年报快照，实测四种几何换手全锁在 2%（见
`template_library_gbr_fundamental_cap_scaled.md` §8.6 的 H-F1 假设）；`other567` 是**月度面板**，
天然具备时间维度 ⇒ 时序几何（T2/T3/T4/T6/T8/T9）在这里不会结构性退化。

**学术支撑**：Green, Huang, Wen, Zhou (2019), *Crowdsourced Employer Reviews and Stock Returns*,
Journal of Financial Economics —— 员工满意度（Glassdoor 类评级）高的公司未来收益更高，年化约 2.4%。
另有 Edmans (2011, JF) 的 "100 Best Companies to Work For" 员工满意度异象作为跨来源佐证。

---

## 2. 字段分层（三层聚合，本身是一条结构轴）

| 层 | 代表字段 | 语义 |
|---|---|---|
| **L1 评论者级原始** | `overall_company_rating`、`senior_management_rating`、`work_life_balance_rating`、`career_growth_rating`、`culture_values_rating`、`diversity_inclusion_rating`、`remuneration_benefits_score`、`employment_duration_years`、`review_helpful_count` / `review_unhelpful_count` | 单条评论的评分 ⇒ 用 `vec_stddev` 可得**评论者分歧度** |
| **L2 公司-月均值** | `avg_overall_company_score`、`avg_senior_management_score`、`avg_pay_and_benefits_score`、`avg_work_life_balance_score`、`avg_career_growth_score`、`avg_culture_values_score`、`avg_diversity_inclusion_score`、`avg_business_outlook_score`、`avg_ceo_approval_score`、`avg_recommend_to_peer_score` | 已聚合的共识值 ⇒ 主信号 |
| **L3 vendor 趋势评级** | `oth567_trendrating_overall`、`_senior_leadership`、`_compensation_and_benefits`、`_culture_and_values`、`_work_life_balance`、`_career_opportunities`、`_diversity_and_inclusion`、`_ceo`、`_business_outlook`、`_recommend_to_friend` | 厂商已做趋势化 ⇒ 与 L2 的差 = **趋势 vs 水平的背离** |
| **L4 文本情感分** | `leadership_sentiment_score`、`compensation_sentiment_score`、`culture_values_rating` 之外的各 `*_sentiment_score`、`workplace_culture_sentiment`、`remote_work_sentiment_score` 等 | 文本衍生分（标度不一，需先 `rank()`） |
| **L5 纯文本（不可用）** | `review_positive_comments`、`review_title_summary`、`suggestion_to_management`、`negative_feedback_text` | 自由文本，数值化后无意义 ⇒ **排除** |

**处理规约**：
- 全部 VECTOR ⇒ 先 `vec_avg(...)`（共识）或 `vec_stddev(...)`（分歧）折叠成标量。
- L1/L2 的 1–5 分标度**同单位** ⇒ 可以互相 `divide` 得无量纲比值（这是本数据集相对 `fundamental1` 的额外便利）。
- L4 情感分标度不一 ⇒ 必须先 `rank()` 再做任何比值。
- 月度面板稀疏度未知 ⇒ 用 `ts_backfill(·, 22)`（1 个月回填）而不是 252。

---

## 3. ★ 十二个结构互异模板

差异落在**骨架结构 / 算子几何 / 矩（水平·一阶·二阶） / 聚合层（L1 vs L2 vs L3） / 非线性变换 / 条件激活**上，不是换窗口换常数。

| # | 模板 | 几何 / 矩 | 经济机制 | 来源 |
|---|---|---|---|---|
| **T1** | `rank(ts_backfill(vec_avg(avg_overall_company_score), 22))` | 0 阶水平（L2） | 员工满意度水平 ⇒ 未来收益（论文原假设） | Green et al. 2019 JFE |
| **T2** | `rank(ts_zscore(ts_backfill(vec_avg(avg_overall_company_score), 22), 252))` | 自身基线偏离 | 满意度相对自身 1 年基线异常升高 = 内部人信息提前泄露 | forum 43152032301591 铁律 #3 |
| **T3** | `rank(ts_av_diff(ts_backfill(vec_avg(avg_overall_company_score), 22), 66))` | 1 阶差分（3 月） | 满意度**改善**的动量 | Edmans 2011（满意度异象的时序版）/ 自建 |
| **T4** | `rank(ts_quantile(ts_av_diff(ts_backfill(vec_avg(avg_overall_company_score), 22), 66), 22, driver=gaussian))` | 1 阶 + 高斯分位 | 改善幅度的高斯分位（幅度保留的非线性） | 自建（本会话招牌，`omEQ9kK5` 曾靠它 ×10） |
| **T5** | `rank(divide(ts_backfill(vec_avg(avg_overall_company_score), 22), ts_backfill(vec_avg(avg_senior_management_score), 22)))` | 0 阶、**同单位比值**（信号定义式） | 总体评价 / 高管评价 = **「除高管之外的一切都好」**，高管是拖累还是加分 | 自建（比值作信号定义，不作信号合成） |
| **T6** | `rank(ts_std_dev(ts_backfill(vec_avg(avg_overall_company_score), 22), 252))` | **二阶时序离散度** | 满意度波动大 = 组织不稳定 ⇒ 折价 | 自建（不确定性溢价） |
| **T7** | `rank(divide(rank(ts_backfill(vec_avg(avg_pay_and_benefits_score), 22)), rank(ts_backfill(vec_avg(avg_work_life_balance_score), 22))))` | 秩比秩（密度） | 薪酬 vs 工作生活平衡的相对满意度（先各自 `rank()` 才同单位） | 自建 |
| **T8** | `rank(ts_rank(ts_backfill(vec_avg(avg_overall_company_score), 22), 504))` | 时序序数 | 当前水平在自身 2 年历史中的分位（序数 vs T2 的幅度保留，对照） | forum 43152032301591 铁律 #2 |
| **T9** | `rank(ts_sum(ts_backfill(vec_avg(avg_overall_company_score), 22), 252))` | 长期累积 | 两年累积满意度（「聚强度」而非取均值） | forum 43152032301591 铁律 #3 |
| **T10** | `rank(ts_backfill(vec_stddev(overall_company_rating), 22))` | **源头分歧度（L1）** | 评论者之间的**分歧**（而非共识）⇒ 分析师分散度的员工版 | Diether-Malloy-Scherbina 2002（分散度异象）的跨数据类比 / 自建 |
| **T11** | `trade_when(greater(rank(ts_std_dev(ts_backfill(vec_avg(avg_overall_company_score), 22), 252)), 0.5), rank(ts_av_diff(ts_backfill(vec_avg(avg_overall_company_score), 22), 66)), -1)` | **条件激活**（只在分歧高时交易动量） | 满意度信号只在组织不稳定期才有信息量 | 自建（`trade_when` 语义见 forum 33120494662423） |
| **T12** | `group_rank(ts_backfill(vec_avg(avg_overall_company_score), 22), subindustry)` | 分组轴（**对照**） | 行业内满意度排名 | 本会话实测反例 |

**论证覆盖**：T1/T2/T3/T4 是同一字段的「水平 / 自身基线 / 一阶 / 非线性一阶」；
T5/T7 是两种比值（同单位直接比 vs 秩比秩）；
T6/T10 是两个层级的离散度（时序二阶 vs 源头截面二阶）；
T8/T9 是「序数」与「累积」两种信息压缩；
T11 是唯一条件激活；T12 是唯一分组轴。
**十二个模板落在七个不同几何维度上。**

---

## 4. 预注册判据（派发前写死）

1. **若 T1（论文原假设）的 |S| < 0.8 且 T3/T2 也 < 0.8** ⇒ `other567` 在 GBR/TOP700 无信号，与它全平台仅 11 个 alpha 一致 ⇒ 判死，换 `other571`（Wikipedia 浏览量）/ `other699`（散户交易）。
2. **若某条 S > 1.3 且 fRA = 0** ⇒ 得到 OTHER 塔的独立腿。此时必须验它与既有 6 条估值位移族候选的 mutual corr —— 预期远低于 0.52 相关地板（因为员工评价与估值倍数无共享分量）。
3. **若 T1 强而 T2–T4 全灭** ⇒ 说明信号是**水平型**（横截面质量差），不是**变化型**，那么后续应在 L2 内找互补字段做 T1 族，而不是继续做时序几何。
4. **若换手 < 3%** ⇒ 检查是否又是「无时间维度」陷阱（同 §8.6 H-F1）；`other567` 是月度面板，理论上不该出现，若出现则说明 GBR 侧只给了单点快照。

---

## 5. 与其它塔的配额关系

- `other567` 是**单数据集** alpha ⇒ **不占任何两塔组合配额**，也不触碰「PV/MODEL/OTHER 禁两两混」硬约束。
- 若后续要与另一数据集组腿：`other567`（OTHER lane）× 非 trio category（如 ANALYST / NEWS）**允许**，但该类组合总量 ≤5，需先查已用配额。
- **禁止**：`other567` × `PV` / `MODEL` / 另一个 `OTHER` 数据集。

---

## 6. 派发设置

与 FUND 族一致：`GBR / TOP700 / D1 · INDUSTRY · decay 10 · trunc 0.05 · nanHandling OFF · maxTrade OFF · pasteurization ON · unitHandling VERIFY`。

**若首条命中 `HIGH_TURNOVER`**：第一步扫平台 decay ∈ {4,6,8,10,12}，不要先动表达式（本会话已验证平台 decay 作用在持仓权重层，同 TO 档位下 S 比表达式内平滑高 26%）。
