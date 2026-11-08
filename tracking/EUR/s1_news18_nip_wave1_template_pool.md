# S1 模板池 · EUR/D1 news18 (Ravenpack nip 族) wave1 · 2026-11-05

> 硬约束：模板库 ≥10 个**结构互异**模板；差异须落在 骨架结构 / 算子几何 / 矩(水平·一阶差分·二阶方差) / 分组轴 / 非线性变换，换窗口不算。
> 来源标注：[F]=平台论坛取证 [P]=论坛帖引用论文 [S]=自建。
> 全部为 **单数据集 ATOM**（news18 内部字段 + 基准收益 returns），不占塔组合配额；NEWS 塔当前 1/3。

## 字段面（MCP get_datafields，EUR/TOP2500/D1）
- MATRIX 59 个，全 cov 0.5：`rp_nip_*`(19，新闻影响投影) / `rp_css_*`(21，综合情绪) / `rp_ess_*`(19，事件情绪)。
- VECTOR：`nws18_nip`(0.8327,ac10) / `nws18_multiple_comp_nip`(0.9914,ac74) / `nws18_relevance`(0.8327,ac6) / `nws18_multiple_comp_relevance`(0.9914,ac253) / `nws18_ssc`(0.8327,ac4) / `nws18_event_relevance`(0.8172,ac8)。
- 论坛命中：nip 族点塔帖 article 40847481080087（EUR/D0/D1 相关性算子+FAST+nip 出 PPA 容易，Sharpe 3.31/Fitness 2.67）。

## 论坛/论文取证（本轮已读原文）
- [F] 40847481080087 使用nip族数据点亮news塔：`ts_corr/ts_covariance/ts_regression`+FAST+nip；评论建议短窗(10/20) vs 长窗(120) 对比衰减、排除高拥挤字段。
- [F] 33566303033751 Data Idea news48：22 字段逐字经济含义（情绪/新颖度/相关度/事件计数/分析师推荐变化）。
- [P] 18641983716503 The Momentum of News（Wang, Zhang, Zhu 2018, SSRN 3267337）：好/坏消息五分位多空、年化 7.45%、信息环境差的股票更有效。
- [F] 19353819839639 新闻动量启发的反转策略：`ts_regression` 残差 + 市值分组 + `abs(returns)` 进入/退出条件。
- [F] 42659817284375 relevance 加权+新颖度过滤：情绪×relevance、变化类情绪配 ts_decay、多公司聚合族 Entity-Story Deviation。
- [F] 33020085052823 NEWS 如何做 ATOM："没有新闻就是好消息" → vec_count/vec_sum 取 -rank；ts_delta 捕捉反应速度变化。

## 模板池（14 个，结构互异；窗口 66=季、22=月、5=周，均有经济含义）
| # | 来源 | 机制 / 结构轴 | 表达式骨架 | 算子数 | 经济含义 |
|---|---|---|---|---|---|
| T01 | [F] | 相关性几何·一阶共动 | `rank(ts_corr(rp_nip_earnings, returns, 66))` | 2 | nip 冲击与收益时序同向共动，季窗捕捉中期衰减 |
| T02 | [F] | 协方差几何·幅度加权 | `rank(ts_covariance(rp_nip_business, returns, 66))` | 2 | 换算子几何：协方差保留幅度 vs 相关系数归一化；换低拥挤字段(ac330) |
| T03 | [F] | 回归残差几何 | `rank(ts_regression(returns, rp_nip_ptg, 66, lag=0, rettype=2))` | 2 | 剥离收益后的新闻暴露残差 |
| T04 | [F] | 情绪水平·横截面 | `group_rank(ts_mean(rp_css_business, 22), sector)` | 3 | 综合情绪月均水平，行业中性排序（矩=水平+平滑） |
| T05 | [P] | 分位多空·动量门控 | `trade_when(greater(vec_avg(nws18_relevance),20), group_rank(ts_mean(rp_ess_revenue,5), subindustry), -1)` | 4 | 好消息动量 + relevance 信噪比门控 |
| T06 | [F] | 回归残差反转·分组 | 改写内部轴：`group_neutralize(-ts_regression(returns, ts_delay(rp_ess_earnings,1),66), sector)` | 4 | 残差大=收益过高未来回落；原式 bucket(rank(cap)) 含非 news18 字段、破坏 ATOM 纯净，已弃用；改写版 preflight 通过 |
| T07 | [F] | 信噪比·relevance 加权 | `group_rank(ts_mean(multiply(vec_avg(nws18_relevance), rp_css_earnings),22), sector)` | 5 | 情绪×相关度，压低顺带提及噪声 |
| T08 | [F] | "没有新闻=好消息"·计数 | `-rank(ts_mean(vec_count(nws18_ssc), 22))` | 4 | 新闻越少注意力越稀缺（矩=计数） |
| T09 | [S] | 一阶差分·冲击加速度 | `rank(ts_delta(ts_backfill(rp_nip_earnings,66), 22))` | 4 | 变化而非水平，捕捉冲击加速/衰减 |
| T10 | [S] | 二阶矩·情绪分歧 | `-rank(ts_std_dev(rp_ess_earnings, 66))` | 3 | 情绪波动=不确定性（Miller 假说方向） |
| T11 | [F] | 偏差·Entity-Story | `rank(subtract(rp_ess_earnings, vec_avg(nws18_multiple_comp_nip)))` | 3 | 单实体情绪相对故事聚合的独立信息 |
| T12 | [S] | 非线性变换·幅值 | `rank(signed_power(group_zscore(rp_nip_mna, sector), 1.5))` | 4 | signed_power 压幅 + 分组轴 |
| T13 | [F] | 新颖度交互 | `group_rank(ts_mean(multiply(vec_avg(nws18_event_relevance), rp_css_earnings),22), subindustry)` | 5 | 新信息加权，旧闻重播无效 |
| T14 | [S] | 注意力溢出·高覆盖聚合族 | `rank(ts_mean(vec_avg(nws18_multiple_comp_nip), 66))` | 3 | 聚合族 cov0.9914 提覆盖，注意力溢出 |

## 派发纪律
- 每批恰好 2 条 `create_multi_simulation`（并发限 2），一批一套 settings：EUR/TOP2500/D1、FAST、decay1、trunc0.04、maxTrade OFF。
- 派发前过 `preflight_expressions`（字段存在 + VECTOR 自动修复）；表达式差异可同批。
- 收批按**模板编号**归因（哪个结构族出货、哪个族全灭），不按单条 alpha 归因。
- 逐年空窗闸（longCount=0&pnl=0）、算子 ≤12、CW/self/prod 在收批后逐件验。

## 首批 2 条（论坛最命中、最干净：纯 MATRIX + returns，算子 2）
- N1 = T01 `rank(ts_corr(rp_nip_earnings, returns, 66))`
- N2 = T02 `rank(ts_covariance(rp_nip_business, returns, 66))`
- 差异：算子几何（相关 vs 协方差）+ 字段拥挤度（ac1038 vs ac330），单变量对照，符合"禁止混信号调参"。

## 全模板字段预检（MCP preflight_expressions，零回测成本）
- 首批 N1(T01)/N2(T02)：valid=true / unknown_fields=[] / platform_field_count=3 / any_changed=false。
- 其余 11 个骨架（T03–T05、T07–T14）：valid=true / unknown_fields=[] / platform_field_count=12 / any_changed=false（VECTOR 字段已手工 vec_avg，preflight 复核无需再修）。算子数逐一计数 2–5，全部 ≤12 合规。
- **T06** 原式（`bucket(rank(cap),range=...)`）含非 news18 字段且语法待核，已改写为内部轴版本 `group_neutralize(-ts_regression(returns, ts_delay(rp_ess_earnings,1),66), sector)`；字段预检通过（valid=true / platform_field_count=4 / any_changed=false），改写版可派。
- 结论：模板池 **14/14 全部可派**（T01/T02 已收批见 WAVE_LEDGER §82；T06 已改写为内部 sector 轴版本并预检通过；T03–T05/T07–T14 预检通过待续批）。按「收批按模板编号归因」纪律续派。

