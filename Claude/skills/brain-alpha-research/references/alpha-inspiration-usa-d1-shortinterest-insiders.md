# 基于 us_short_sale / board_gov_stats / short_interest_pred / biasfree_analyst 的 Alpha 模板

> 来源：参考 `alpha_inspiration_analyst10.md` 模板格式，基于本轮 USA/D1 PPA 挖掘（批 63/64/65）实际回测的表达式提炼。
> 全部表达式已通过 `wqb.expression.validator.check_batch` 校验（外层包装≥2、双字段≥3、形状≥2、窗口≥2）。
> 回测配置：USA / TOP3000 / D1 / SUBINDUSTRY / decay8 / trunc0.04 / nan ON / maxTrade ON。

---

### 模板1：做空压力占比的反向排名模板
**经济逻辑**：单日做空成交股数占总成交股数的比例，衡量当日做空压力。做空压力高的股票往往面临更弱的短期价格支撑（卖压），因此反向（reverse）持有做空压力低的股票，捕捉卖压释放后的反弹。这是做空（shortinterest）金字塔类别的基础一阶信号。
**模板公式**：
```
reverse(quantile(ts_backfill(divide(<做空股数>, <总成交股数>), <回溯天数>)))
```
**占位符说明**：
- `<做空股数>`：当日做空成交股数（如 `executed_short_trade_share_count`）；
- `<总成交股数>`：当日总成交股数（如 `aggregate_executed_trade_share_count`）；
- `<回溯天数>`：数据填充窗口（60 天验证，120 天等价）。
**实测**：`reverse(quantile(ts_backfill(divide(executed_short_trade_share_count, aggregate_executed_trade_share_count), 60)))` = sharpe 1.25 / fit 0.64 / 2Y 1.37 / ppa=0。

---

### 模板2：做空压力占比的组内反向排名模板（二阶）
**经济逻辑**：模板1 的基础上，用 `group_rank` 按 subindustry 分组后取反。行业（subindustry）内相对做空压力更低的股票，剔除行业整体做空环境差异，突出个股层面卖压的相对缓解，增强选股稳健性。
**模板公式**：
```
reverse(group_rank(quantile(ts_backfill(divide(<做空股数>, <总成交股数>), <回溯天数>)), <分组维度>))
```
**占位符说明**：
- `<做空股数>` / `<总成交股数>` / `<回溯天数>`：同模板1；
- `<分组维度>`：subindustry（实测最优，sharpe 1.28）或 sector（组内排名变体，批量校验时提供第二分组维度）。
**实测**：
- `reverse(group_rank(quantile(ts_backfill(divide(executed_short_trade_share_count, aggregate_executed_trade_share_count), 60)), subindustry))` = sharpe 1.28 / fit 0.63 / 2Y 1.34 / ppa=0（本轮 USA/D1/SHORTINTEREST 最优）；
- `reverse(group_rank(ts_rank(ts_backfill(divide(executed_short_trade_share_count, aggregate_executed_trade_share_count), 60), 44), sector))`（sector 组内 ts_rank 变体，已回测）。

---

### 模板3：做空压力动量（变化率）的反向模板
**经济逻辑**：做空压力占比的 22 日变化，衡量做空力量的边际增减。做空压力上升（delta 为正）预示卖压加剧，反向持有做空压力下降的股票，捕捉做空退潮的修复机会。
**模板公式**：
```
reverse(quantile(ts_delta(divide(<做空股数>, <总成交股数>), <变化天数>)))
```
**占位符说明**：
- `<做空股数>` / `<总成交股数>`：同模板1；
- `<变化天数>`：delta 计算窗口（22 天）。
**实测**：`reverse(quantile(ts_delta(divide(executed_short_trade_share_count, aggregate_executed_trade_share_count), 22)))` 已回测（turnover 0.17，信号强度中等）。

---

### 模板4：治理稳健性（独立董事比例减董事会离职率）模板
**经济逻辑**：独立董事比例高代表监督机制完善，董事会离职率高代表治理动荡。用"独立董事比例 − 董事会离职率"构造治理质量综合分：治理结构稳定、监督有效的公司更可能获得市场溢价。属于 insiders 金字塔类别。
**模板公式**：
```
subtract(
    quantile(ts_backfill(<独立董事比例>, <回溯天数>)),
    quantile(ts_backfill(<董事会离职率>, <回溯天数>))
)
```
**占位符说明**：
- `<独立董事比例>`：如 `independent_director_ratio`（coverage 0.95）；
- `<董事会离职率>`：如 `board_departure_rate_1y_board`（coverage 0.89）；
- `<回溯天数>`：60 天。
**注意**：慢变量（turnover ~0.014），低换手下 margin 高但 sharpe 偏低（0.54），更适合作为二阶组合的组件而非独立 PPA。

---

### 模板5：做空预测变化的反向模板
**经济逻辑**：模型对下一期做空兴趣变化的预测（`short_interest_predicted_change`），若预测做空增加，预示未来卖压；反向持有预测做空减少的股票。该字段来自 short_interest_pred 数据集，是前瞻性做空信号。
**模板公式**：
```
reverse(quantile(ts_backfill(<做空预测变化>, <回溯天数>)))
```
**占位符说明**：
- `<做空预测变化>`：如 `short_interest_predicted_change`（coverage 0.999）；
- `<回溯天数>`：60 天（120 天等价）。
**实测**：`reverse(quantile(ts_backfill(short_interest_predicted_change, 60)))` = sharpe 0.92 / fit 0.29 / 2Y 1.54（2Y 接近门槛，turnover 0.41 偏高）。

---

### 模板6：无偏分析师目标价上修动量模板
**经济逻辑**：无偏分析师（biasfree）目标价上修次数减下修次数，衡量分析师对个股前景的净修正方向。上修多于下修说明基本面预期改善，正向持有。属于 analyst 金字塔类别。
**模板公式**：
```
subtract(
    quantile(ts_backfill(<上修次数>, <回溯天数>)),
    quantile(ts_backfill(<下修次数>, <回溯天数>))
)
```
**占位符说明**：
- `<上修次数>`：如 `num_upward_biasfree_price_target_revisions`；
- `<下修次数>`：如 `num_downward_biasfree_price_target_revisions`；
- `<回溯天数>`：60 天。
**注意**：单字段水平信号弱（sharpe ~0.5），修正次数字段稀疏，建议与做空信号组合（如 `subtract(上修, 做空预测变化)`）使用。

---

### 模板7：无偏分析师乐观与做空压力对冲模板（跨数据集组合）
**经济逻辑**：分析师乐观预期（高目标价）与做空压力（卖压）是同一股票的多空两面。用目标价水平减去做空意外值，构造"基本面乐观 − 市场卖压"的净信号，兼顾分析师修正与做空行为两个维度。
**模板公式**：
```
subtract(
    quantile(ts_backfill(<无偏目标价>, <回溯天数>)),
    quantile(ts_backfill(<做空意外值>, <回溯天数>))
)
```
**占位符说明**：
- `<无偏目标价>`：如 `median_first_biasfree_price_target_estimate`；
- `<做空意外值>`：如 `short_interest_surprise_value`（实际−预测做空偏差）；
- `<回溯天数>`：60 天。

---

### 使用建议
1. **金字塔点亮**：模板1/2/3/5 均归属 USA/D1/SHORTINTEREST（multiplier 1.1），模板4 归属 USA/D1/INSIDERS，模板6/7 归属 USA/D1/ANALYST——均为当前未点亮类别，可作 PPA 候选。
2. **算子合规**：全部使用平台标准算子（reverse/quantile/ts_backfill/ts_delta/divide/group_rank/subtract/ts_rank/ts_zscore/ts_mean），外层包装多样（reverse/quantile/subtract/group_rank），无 add+负号（统一用 subtract/reverse 保持经济学语义）。
3. **数据质量**：us_short_sale 与 short_interest_pred coverage 均 ≥0.999；board_gov_stats coverage 0.89-0.95；biasfree_analyst coverage 0.84-0.94。
4. **下一步**：模板2（sharpe 1.28）距门槛 1.58 仍差 0.30，可试三阶 trade_when 事件工程（参考 machine_lib 事件库）或中性化/decay 变体提升。

---

### 补充扫描结论（2026-08-06 第二批，USA/D1/SENTIMENT 等）
- **sentiment22**（新闻情绪，210 字段）：一般情绪 0.10 / 净情绪 -0.72 / 负面取反 -0.86 / 情绪动量 -0.42——全部不达标，SENTIMENT 类排除。
- **短空预测 short_interest_pred**：`reverse(quantile(ts_backfill(short_interest_predicted_change, 60)))` = 0.92 / 2Y 1.54（2Y 接近但 sharpe 不足，turnover 0.41 偏高）。
- **USA/D1 信号天花板总结**：us_short_sale 做空压力 1.28（经一阶/二阶/三阶全谱打磨确认天花板）、治理 0.95、做空预测 0.92、分析师 0.51、新闻情绪 0.1——单数据集均无法独立达到 1.58 门槛，需跨数据集组合或换更强信号源。

---

### USA/D1 PPA 实战突破（2026-08-07 补充）
- **PPA#1 达标并提交**：`quantile(ts_mean(ts_backfill(vec_avg(standardized_opinion_score), 66), 22))`
  @ USA/D1/TOP3000/SUBINDUSTRY/decay8 = **sharpe 1.58/fit 1.35/2Y 1.80/margin 49.7bp/ra=0/ppa=0**
  - 数据集：social_sent_score（社交观点分，仅 3 字段，coverage 0.64）
  - **关键突破**：ts_mean 22 平滑把 sharpe 从 1.38→1.58（+0.20）、fit 1.09→1.35
  - 论坛 ATOM 原则验证：单数据集纯信号 + 标准窗口 {66,126} + ts_mean 平滑
- **方法论**：8 批 × 8 表达式并行扫描（behavioral/search/social/news/shrt29/gov 六数据集 48 表达式）→ 筛出 social_sent_score 最强 → 窗口/平滑/分组逐级打磨
- **失败记录**：LLGXAj0L（收入-净利 zscore 组内差，sh 1.59 但 fit 0.92/sub 0.27/2Y 0.87 三项 FAIL）；analyst_factor_signals 组内 1.52 但 fit 不足；EUR 财报情绪天花板 0.91、EUR analyst69 4周修正天花板 1.14

### USA/D1 数据集信号档案（2026-08-07 扫描总结，PPA#2 挖掘）
| 数据集 | 最强信号 | 最优 sharpe | 结论 |
|---|---|---|---|
| social_sent_score | standardized_opinion_score ts_mean22 | **1.58 ✅** | PPA#1 达标提交 |
| analyst_factor_signals | 收入 zscore 组内+ts_mean | 1.53 | fit 0.97/sub 0.45/2Y 1.23 多 FAIL |
| us_short_sale | 做空/总交易占比 | 1.28 | 一/二/三阶天花板 |
| shortinterest29 | 月度做空量 | 1.01 | fit 1.23 但 sharpe 不足 |
| board_gov_stats | CEO 任期 | 0.95 | 慢变量 |
| short_interest_pred | 做空预测变化 | 0.92 | 2Y 1.54 接近 |
| web_traffic_engage | 访问-移动差 | 0.72 | coverage 0.43 稀疏 |
| behavioral_signals | 显著性加权 | 0.42 | 弱 |
| search_trends/news/sentiment22/acquisition/ai_factor | — | <0.55 | 排除 |
- **经验**：USA/D1 达标难（门槛 1.58/1.0/1.58 + sub 0.66 + 2Y），仅社交观点分 + ts_mean22 平滑破局；PPA#2 需跨数据集或换区域
