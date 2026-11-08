# socialmedia12（研报热度反转）波 1 模板池 — 金帖两读 + 约束适配

> 状态：双预检全绿（字段 3/3 + 语法 12/12 PASS）→ 已派发 sm12w1_20261103 / pid 55996。
> 数据集：socialmedia12（PulsePick，18 字段，覆盖实测 2014-23 满）。纯单数据集 SOCIALMEDIA ATOM，零 builtin = 单塔。

## 一、金帖两读（HH77144《股票舆情热度的反转效应与热点反应因子构建》，article 35876513619607）

### 作者三因子（USA 实测）+ 提交占位
- signal1 热度漂移反转 = -zscore(ts_decay_linear(abs(scl12_buzz),5)) + hump(0.01)：**decay_linear>mean**（时序趋势），初版反转需负号，weight 过大用 **hump** 平滑（Sharpe/fitness 反升）。
- signal2 热度反转 = -if_else(price_delta>0, scl_delta^2, -scl_delta^2)：**四象限**（热度↑价↑=空 / 热度↑价↓=多 / 热度↓价↑=空 / 热度↓价↓=多）；zscore^2 = 阈值筛选（放大|>1|压缩|<1|）；vwap>open（跳空污染）。
- signal3 = signal1+signal2 + hump(0.008)：综合最优。
- 提交占位：三因子均过提交（hump 后指标达标），但**测试期偏弱**（2022 后动量 regime 削弱反转）。votes 3。

### 开放问题面 = 差异化模板空间
① hump vs winsorize：winsorize 任意阈值都严重削弱信号，hump 好得多（为什么？）→ 平滑方法对照轴。
② 跨市场验证：原论文 A 股，本研报美股，**建议测其他市场** ← DEU 正是此问。
③ 评论机制·信息分散度 regime 切换：Z=ts_std_dev(volume,21)/ts_mean(volume,21)，if_else(rank(Z)>0.9,signal,-signal) 动态切换动量/反转，Sharpe/fitness 显著提升（但 weight/TO 高）。
④ 对照因子 signal3=ts_decay_linear(ts_delta(vwap,1),5)：反转 regime 时热点因子好，动量 regime 时差。

## 二、DEU 约束适配（关键）
- **塔混**：金帖用 vwap/close(PV)+scl12(SOCIALMEDIA)=trio×非trio 组合，但该配额已满 5/5 → **本波剔除全部 PV 字段，纯 SOCIALMEDIA 单塔**。四象限的价格反应腿在 DEU 因配额满被阻断（记入待解锁项）。
- **类别卡**：主信号 scl12_buzz；第二字段（scl12_sentiment/sentiment_score）只作**条件/分组/残差**入场，不并列作信号腿（无独立腿 add/subtract）。
- **金帖三雷**：ts_zscore 外层在情绪/脉冲族禁用 → 用 group_rank/rank 截面归一替代 zscore；ts_max/ts_min 无；quantile 双位置参无。
- **合法信号字段**（真情绪面）：scl12_buzz / scl12_sentiment / sentiment_score（均 MATRIX，直接用）。**禁**（前瞻元数据）：backtest_hit_ratio / sentiment_significance / sentiment_expected_price_change / sentiment_stddev。**不用**（价格复制）：sentiment_*_price / sentiment_intraday_return（信号条件化）/ sentiment_open_to_close_return_pct。
- **稳态水平面已证死**（注意力/情绪类）→ 全动态/突变面，无纯水平。

## 三、12 模板池（结构轴：decay_linear/delta/双周期价差/平方放大/regime切换/慢均/条件×4/残差/第三字段主）

| # | 骨架 | 核心 | 结构轴 | 来源 |
|---|---|---|---|---|
| T1 | 热度漂移反转 | −ts_decay_linear(buzz,5) | 衰减加权 | **金帖照抄（≤1）** |
| T2 | 热度骤变反转 | −ts_delta(buzz,5) | 突变面 | 金帖 signal2 内核 |
| T3 | 快慢热度差 | Δbuzz5−Δbuzz66 | 同字段双周期 | 自建（合规） |
| T4 | 热度突变平方 | −(Δbuzz5)² | 平方放大 | 金帖 threshold trick |
| T5 | 信息分散度 regime | if_disp>0.9:Δ,−Δ | 条件切换 | 评论③开放问题 |
| T6 | 慢热度动态反转 | −ts_mean(Δbuzz22,66) | 慢均 | 自建 |
| T7 | 情绪正动量门控 | trade_when(Δsent22>0,…) | 条件腿 | 开放问题② |
| T8 | 情绪分位门控 | trade_when(qsent>0.5,…) | 条件腿 | 自建 |
| T9 | 热度-情绪背离门控 | trade_when(Δbuzz−Δsent>0,…) | 条件腿 | 金帖四象限内生 |
| T10 | 热度-情绪残差 | rank(Δbuzz)−rank(Δsent) | 残差腿 | 自建 |
| T11 | 情绪水平动态反转 | −ts_delta(sentiment_score,22) | 第三字段主 | 自建 |
| T12 | 共振背离门控 | trade_when(Δbuzz·Δscore<0,…) | 条件腿 | 自建 |

照抄臂 1（T1）✓；开放问题臂 T4/T5/T7/T9 ≥3 ✓。全单塔 SOCIALMEDIA。

## 四、派发实录
- JSON：tracking/DEU/socialmedia12_wave1_templates.json（12 臂，DEU 标准 decay4/SUBINDUSTRY/trunc0.08）。
- task-id：sm12w1_20261103 / pid 55996。
- 收批：逐颗 get_alpha_yearly_stats 覆盖闸（sm12 已实测满 10 年，预期全过）；归因按 T1-T12 模板编号。

## 收批归因（2026-11-03 收满 12/12）
- 全批判弱：max S 0.06（T7 条件腿），TO 0.4-1.07 偏高；T11/T12 末批 0.01/−0.15。
- 1 行 TIMEOUT 经 lookINTO 查明真终态 = **WARNING 量纲违规真死**（`subtract(0, ts_delta(sentiment_score,22))` 裸常数 0 − 带量纲 TSPrice）——不补发；**反转带量纲信号正解 = `multiply(x, -1)`**，subtract(0,…) 只用于无量纲信号。
- 判弱只封 sm12×动态面组合；scl12 真情绪面（buzz/sentiment/score）DEU 动态面无货，与 snt7/sn12/snt27 合并为「注意力/情绪族 DEU 系统性弱」证据链。
- 待解锁：四象限价格反应腿（PV+SOCIALMEDIA）需 trio×非trio 配额空出才可派。
