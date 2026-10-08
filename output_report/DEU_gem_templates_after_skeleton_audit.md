# GEM 兼容模板库 · DEU（骨架审计后版）· 2026-10-07

> **仿 GEM 工作原理产出**：Concept / Mechanism / Fields / Implementation Example / Direction。
> **两条纪律**：① 骨架只用 **A 级**（S1 含窗 / S2 双窗）+ 已验证框架（单桶轴 gran 0.05）；
> ② 每条标 **经济机制来源** 与 **验证状态**（✅已过闸 / ⚠️已测不够强 / ❓未测）。
>
> **★ 与现有 EUR ideas 的区别**：那份用了 `rank(zscore(F))`（**单调无操作**，已实测）和 `rank(ts_delta(F,22))`（变化形，弱）；
> 本库**只用双窗 S2 / 含窗 S1**，并把窗长钉到实测最优的 **1/210**。

---

## 〇 全局框架（所有模板共用）

```
group_neutralize(
  rank(add(ts_mean(bf(F), 1), ts_mean(bf(F), 210))),          # ★ 双窗 S2（A 级）
  bucket(rank(ts_mean(bf(F), 252)), range="0,1,0.05"))        # ★ 单桶轴（A 级）
其中 bf(F) = ts_backfill(F, 1008)（VECTOR 则 ts_backfill(vec_max(F), 1008)）
```

**已实测过闸的两例**（证明该框架可用）：
- `58gkLAkk`（MODEL，S1.75 / 2Y2.07）— **已提交 ACTIVE**
- `9qWX78vV`（ANALYST，S1.65 / F1.47 / 0 失败）— **已就绪**

---

# 一 预期修正族（**唯一已证有效机制**）

**机制来源**：Post-Revision Drift（分析师预期修正后价格漂移）—— 学术与卖方研究均有记载。

### Concept 1 · 盈利预期修正动量 ✅（已验证）
- **Mechanism**: 一致预期上调且修正广泛时，价格继续沿修正方向漂移（反应不足）
- **Fields Used**: `eps_y1_estimate_change_3mo`（ANALYST，cov 0.9234）
- **Implementation Example**: `group_neutralize(rank(add(ts_mean(bf,1), ts_mean(bf,210))), bucket(rank(ts_mean(bf,252)), range="0,1,0.05"))`
- **Direction**: High → long
- **验证状态**: ✅ **`9qWX78vV` S1.65 / F1.47 / 0 失败 / 塔 DEU/D1/ANALYST**

### Concept 2 · EBITDA 预期修正（**跨指标同构**）⚠️
- **Mechanism**: 同一机制换现金流口径 —— EBITDA 修正比会计净利更难被盈余管理扭曲
- **Fields Used**: `mean_estimate_change_pct_f12m_ebitda_14d_4`（MODEL，cov 0.9706）
- **Implementation Example**: 同 Concept 1 的框架
- **Direction**: High → long
- **验证状态**: ⚠️ 轻框架峰值 **S1.41 / sub1.20**（距闸 S+0.17）—— **本库最接近的未过闸候选**

### Concept 3 · 销售（营收）预期修正
- **Mechanism**: 营收修正是需求端信号，比盈利修正更早（盈利可被成本掩盖）
- **Fields Used**: `est_12m_sal_mean` + `est_12m_sal_mean_3mth_ago`（analyst7，cov 0.736）
- **Implementation Example**: `group_neutralize(rank(subtract(rank(bf(est_12m_sal_mean)), rank(bf(est_12m_sal_mean_3mth_ago)))), bucket(...))`
- **Direction**: High → long
- **验证状态**: ⚠️ S3 快照差实测 **S1.29 / sub0.95**

---

# 二 ★ 信用 / 违约风险族（**全新机制，未测，67 个字段**）

**机制来源**：Merton (1974) 结构化违约模型 —— 把股权看作公司资产的看涨期权。

### Concept 4 · 违约距离（Distance to Default）
- **Mechanism**: DD = 公司资产距违约边界的标准差数。DD 低 = 违约风险高。**符号有两个竞争假说**：①信用溢价（低 DD → 高预期收益）②财务困境（低 DD → 低收益）
- **Fields Used**: `mdl28_sm_structural_credit_structural_distance_to_default`（model28，cov 0.6838）
- **Implementation Example**: 全局框架；**必须同时测正号与反号**（`multiply(..., -1)` 需换成 `group_neutralize(rank(subtract(0, ...)), ...)` 或先测 `signed_power`）
- **Direction**: **待定**（两个假说方向相反，先测哪边显著）
- **验证状态**: ❓ **未测**

### Concept 5 · 资产漂移 / 资产波动（结构模型分量）
- **Mechanism**: 结构模型的两个核心输入 —— 资产漂移（预期增长）与资产波动率（不确定性）。资产波动率是"股权作为期权"的价值来源
- **Fields Used**: `mdl28_sm_structural_credit_structural_asset_drift_pct` / `..._asset_volatility_pct`（cov 0.684）
- **Implementation Example**: 全局框架
- **Direction**: drift High → long；volatility **待定**
- **验证状态**: ❓ 未测

### Concept 6 · 信用质量综合分
- **Mechanism**: 信用质量的五维分解（覆盖 / 成长 / 杠杆 / 流动性 / 盈利），是"财务健康度"的多角度刻画
- **Fields Used**: `credit_risk_{coverage,growth,leverage,liquidity,profitability}_score_d1`（model36，cov ~0.698）
- **Implementation Example**: 全局框架（**注意：五个分是同一概念的多角度，建议各测一条而非相加——相加属多腿**）
- **Direction**: High → long
- **验证状态**: ❓ 未测

### Concept 7 · ★ 违约概率期限结构斜率
- **Mechanism**: `annualized_pd_1_month` 与 `annualized_pd_10_year` 的差 = **近期违约风险的陡升**。短端相对长端抬升 = 市场认为近期风险骤然上升（财务恶化的前置信号）
- **Fields Used**: `annualized_pd_1_month_jc7` / `annualized_pd_10_year_jc7`（model53，cov 0.873）
- **Implementation Example**: `group_neutralize(rank(subtract(rank(bf(pd_1m)), rank(bf(pd_10y)))), bucket(...))`
- **Direction**: 短端抬升 → short
- **验证状态**: ❓ 未测 —— **本库最有理论新意的构造**（字段本身就带期限维度，不是"快照差分"）

---

# 三 机构资金流族（**MATRIX cov=1，最快上手**）

**机制来源**：机构资金流 / Smart Money 假说。

### Concept 8 · 机构买入家数净额（Institutional Breadth）
- **Mechanism**: 净买入的机构**家数**（而非金额）反映共识广度 —— 多家小额买入比一家大额买入更有信息含量
- **Fields Used**: `count_institutional_buyers_security` − `count_institutional_sellers_security`（institutions6，**cov 1.0**）
- **Implementation Example**: `group_neutralize(rank(subtract(rank(bf(buyers)), rank(bf(sellers)))), bucket(...))`
- **Direction**: High（净买入多）→ long
- **验证状态**: ❓ 未测

### Concept 9 · 机构增减持强度
- **Mechanism**: 机构增持市值 / (增持+减持) = 净买入强度，剔除了规模效应
- **Fields Used**: `market_value_institutional_shares_acquired` / `..._disposed`（cov 1.0）
- **Implementation Example**: 同上（`subtract(rank(acquired), rank(disposed))`）
- **Direction**: High → long
- **验证状态**: ❓ 未测

### Concept 10 · 持仓集中度（Herfindahl）
- **Mechanism**: 基金持仓的 HHI 高 = 少数大玩家主导 = 定价更可能被少数人错定价
- **Fields Used**: `herfindahl_index_transactions{,_active}`（fund_holdings_panel，cov 0.928）
- **Implementation Example**: 全局框架（需 `vec_avg`）
- **Direction**: **待定**
- **验证状态**: ❓ 未测

---

# 四 做空 / 借贷族

**机制来源**：卖空约束与做空需求（Boehmer et al.）。

### Concept 11 · 借券费率（做空需求强度）
- **Mechanism**: 借券费率高 = 做空需求强且供给紧。经典结论是**负向**（做空者信息优势）
- **Fields Used**: `lending_fee_bid_rate`（risk60，cov 0.835）/ `loan_rate_main`（shortinterest3，cov 0.687）
- **Implementation Example**: 全局框架（需 `vec_avg`）
- **Direction**: High → **short**
- **验证状态**: ❓ 未测（注：`mean_loan_rate_main` 的历史高分**全是多腿组合**）

### Concept 12 · 借券费率波动（做空压力不确定性）
- **Mechanism**: 费率波动 = 做空观点的分歧/不稳定，比费率水平更能刻画"做空压力的可持续性"
- **Fields Used**: `loan_rate_volatility{,_main,_p5_d1}`（shortinterest3）
- **Implementation Example**: 全局框架（需 `vec_avg`）
- **Direction**: **待定**
- **验证状态**: ❓ 未测

---

# 五 新闻事件族（**212 字段，prod 墙压力最小**）

**机制来源**：新闻情绪动量 / 定价不足（Tetlock 2007 等）。

### Concept 13 · 事件情绪动量
- **Mechanism**: 基本面新闻情绪的持续偏向（不是单条新闻），市场对情绪的调整是渐进的
- **Fields Used**: `event_sentiment_score`（news17/18/20，cov 0.64~0.70）
- **Implementation Example**: 全局框架（需 `vec_avg`）
- **Direction**: High（正情绪）→ long
- **验证状态**: ❓ 未测

### Concept 14 · 事件相关性加权情绪
- **Mechanism**: 只对**高相关性**事件计情绪，低相关性新闻是噪声
- **Fields Used**: `event_relevance` + `event_sentiment_score`
- **Implementation Example**: **不能直接相乘（混信号）** ⇒ 改用 `trade_when(greater(relevance, <阈值>), 情绪信号, -1)`，但**门类骨架已实测为削弱器**，预期收益低
- **Direction**: 待定
- **验证状态**: ❓ 未测（**且门类骨架是 B 级，不推荐**）

### Concept 15 · 相似事件距今（事件重演的时距）
- **Mechanism**: 同一类型事件上次发生距今多远 —— 距今天数短 = 事件集群/催化密集
- **Fields Used**: `event_similarity_days`（news17，cov 0.649）
- **Implementation Example**: 全局框架（需 `vec_avg`）
- **Direction**: **待定**（借鉴 S10 极值时点的失败经验，**此构造优先级低**）
- **验证状态**: ❓ 未测

---

# 六 数字营销 / 电商族（**最另类，独特性最高**）

**机制来源**：需求侧高频代理数据（搜索流量、电商评价）—— 领先于财报的需求信号。

### Concept 16 · 付费搜索投放强度（获客投入）
- **Mechanism**: 广告投放预算是管理层对**未来需求**的下注。投放激增 = 公司预期增长
- **Fields Used**: `paid_search_budget_estimate` / `paid_search_terms_count`（other47，cov 0.652）
- **Implementation Example**: 全局框架（需 `vec_avg`）
- **Direction**: High → long
- **验证状态**: ❓ 未测

### Concept 17 · 自然搜索流量（需求侧代理）
- **Mechanism**: 自然搜索量反映**未被营销驱动的真实需求**，是营收的领先指标
- **Fields Used**: `oth47_organic_traffic` / `oth47_organic_keywords`
- **Implementation Example**: 全局框架
- **Direction**: High → long
- **验证状态**: ❓ 未测

### Concept 18 · 商品评价数与评分
- **Mechanism**: 评价数 = 销量代理（需求）；平均星级 = 产品竞争力。**评价数激增 + 高星级** = 增长
- **Fields Used**: `item_review_count` / `item_rating` / `average_star_score`（other250，cov 0.613）
- **Implementation Example**: 全局框架
- **Direction**: review_count High → long；rating High → long（**分别测，不合并**）
- **验证状态**: ❓ 未测

---

# 七 零售关注族

### Concept 19 · 人气排名变化（Attention Reversal）
- **Mechanism**: 零售关注度骤升 → 短期被推高 → 随后反转（Barber & Odean 关注驱动买入）
- **Fields Used**: `snl27_relpopularity1` / `snl27_top50pctranking`（sentiment27，cov 0.902）
- **Implementation Example**: 全局框架（需 `vec_avg`）；**预期为反转 ⇒ 先测正号**
- **Direction**: **待定**（关注度上升 → short？）
- **验证状态**: ❓ 未测

---

# 八 汇总与执行顺序

| # | Concept | category | 骨架 | 验证状态 | 优先 |
|---|---|---|---|---|---|
| 1 | 盈利预期修正 | analyst | S2 | ✅ **已过闸** | — |
| 2 | **EBITDA 预期修正** | model | S2 | ⚠️ **S1.41（最近）** | **1** |
| 7 | **违约概率期限斜率** | model | S3 变体 | ❓ | **2** |
| 8 | 机构买入家数净额 | institutions | S2 | ❓ | **3** |
| 4/5 | 违约距离 / 资产波动 | model | S2 | ❓ | **4** |
| 11/12 | 借券费率 / 波动 | risk+shortinterest | S2 | ❓ | 5 |
| 13 | 事件情绪动量 | news | S2 | ❓ | 6 |
| 16/17 | 搜索投放 / 自然流量 | other | S2 | ❓ | **7** |
| 18 | 电商评价 | other | S2 | ❓ | 8 |
| 19 | 人气排名 | sentiment | S2 | ❓ | 9 |
| 6/9/10 | 信用分 / 机构增减持 / HHI | model+institutions | S2 | ❓ | 10 |
| 3 | 营收快照差 | analyst | S3 | ⚠️ S1.29 | 低 |
| 14/15 | 事件相关性门 / 相似时距 | news | S6/S10 | ❓ | **不推荐**（骨架 B 级） |

**★ 全部 19 条共用同一个框架（S2 双窗 + 单桶轴），只有字段与机制不同** —— 这正是本会话中心结论的体现：**框架固定，变量只有字段**。

**每条的测试成本 = 1 条模拟**。19 条 ≈ 2 批。
