# earnings_sent_matrix 波1 模板池台账（DEU / TOP500 / D1 / EARNINGS 单塔）

## 一、覆盖闸通过（2026-11-03 07:2x，探针 MPYLnZVa + get_alpha_yearly_stats）
- 10/10 年有数（pnl ±百万级、TO 0.35-1.22），cov 0.0 系 intraday slice 稀疏性统计失真。earnings 塔点亮，开波资格确认。

## 二、论坛金帖两读（WL58980《Earnings模板分享》，2026-05-28，39 赞/21 评）

### 2.1 作者提交占位（生产池拥挤度先验）
- 一阶模板 `<ts_op>(ts_backfill(<field>, d1), d2)`：USA 用 `positive_sentiment_probability_3` 点亮 Earnings、EUR 用 `sentiment_weighting_method1` 点亮 Earnings；2000 次回测轻松提交 6 个 RA（USA）。
- **关键情报：作者只报 USA/EUR，GLB 未测，DEU 未提** ⇒ DEU 该集生产池占位**可能仍空窗**（平台 ac 131 是全球口径），抢占窗口存在。
- 作者原话：「新推出的数据相关性普遍很低，可以轻松提交」；发帖时该集全球 Alpha 数为 0。
- **风险标注**：LG97237 实测「USA 出了不少货，**EUR 表现一般**」——DEU 同属欧洲，方向先验中性偏谨慎，机制×区域二维律须重测不外推。

### 2.2 模板配方（照抄面 ≤1 限额）
- 骨架：`<ts_op>(ts_backfill(<field>, d1), d2)`；ts_op 用过 ts_arg_max / ts_av_diff / ts_quantile / ts_zscore / **ts_scale（待过 get_operators 名单，禁照抄）**；d1 ∈ {10, 252}、d2 = 252。
- 替换发现：ts_backfill 可换 ts_mean（作者猜想 ts_sum 亦可）；嵌套降相关：`<ts_op>(<ts_op>(ts_backfill(f, d1), d2), d2)`。
- **⚠️ 窗口合规改造**：d1=10 **不在 DEU 白名单**（1/5/22/66/252/504/1008/1260）——用 5 或 22 替代（近期消息消化面），252 合规原样。

### 2.3 开放疑问面（评论区 → 差异化臂来源，开放问题臂 ≥3 ✓）
- LY66036/XW23690：**d1=10 vs 252 是两种信息持有假设**（近期消息消化 vs 跨报告期持有），分别核对缺失/换手/相关性 → 双臂对照。
- DS18646：**配合 pos−neg 情绪净差 GEM 模板效果更好** → 净差臂。
- SY90356：① ts_backfill vs ts_mean 语义场景 ② **negative 概率做多空组合** ③ 短回填灵敏 vs 长回填平滑。
- FF65210/JC31003：**单字段先预处理（回填/平滑）后出信号率大增**。
- 作者附赠 PPA 警示：IS 好但 **investability 可能低得离谱**，收批时盯 investability 指标。

## 三、论文取证（web_search 2026-11-03）

- **Loughran-McDonald (2011)**：通用词典（Harvard-IV）在金融语境失效 ⇒ method1（词典法）与 method2（ML 法）测的不是同一构念，method1−method2 净额=测量分歧信号（M4 理论依据）。
- **Tonin & Scherer (2022, 1165 场电话会)**：分析师 tone > 管理层 tone 显著；introductory 正 / Q&A 负——**同一通话内 tone 有结构**，turn-level 波动与分歧度有信息。
- **Druz-Wagner-Zeckhauser (2016)**：**tone disappointment（负面）信息量 ≫ tone delight（正面）**，post-call drift 由失望驱动 ⇒ 情绪非对称面（M5 长记忆负 − 短记忆正；M6 NEG 独立腿）。
- **Off Script (2026)**：跨渠道 tone 分歧产生可预测性 ⇒ M4 方法分歧面再获支撑。
- **LAW 假说**：管理层对正私有信息反向低报（managed sentiment）⇒ 原始 POS 是被管理的，净差/惊喜比水平更可信（M1/M3 走 ts_zscore 惊喜而非裸水平，与「禁裸 rank(field)」一致）。

## 四、模板池（12 个结构互异 ✓ ≥10；照抄臂 1、开放问题臂 4、论文臂 2）

| # | 名称 | 表达式 | 机制面 / 来源 | 结构轴 |
|---|------|--------|--------------|--------|
| 0 | M1_pos_surprise_22 | `group_rank(ts_zscore(ts_backfill(positive_sentiment_probability_3, 22), 252), subindustry)` | **照抄臂**金帖一阶骨架（d1=10→22 窗口合规改造） | 水平惊喜 |
| 1 | M2_pos_surprise_252_hold | `group_rank(ts_zscore(ts_backfill(positive_sentiment_probability_3, 252), 252), subindustry)` | 开放问题 LY66036：d1 长=跨报告期信息持有假设 | 同骨架换信息假设 |
| 2 | M3_net_diff_surprise | `group_rank(ts_zscore(ts_backfill(subtract(pos, neg), 22), 252), subindustry)` | 开放问题 DS18646：pos−neg 情绪净差 GEM 配方 | 同机制净额合成 |
| 3 | M4_method_disagree | `group_rank(ts_av_diff(subtract(sentiment_weighting_method1, sentiment_weighting_method2), 22), subindustry)` | 论文 LM2011+OffScript：词典 vs ML 测量分歧 | 一阶矩 + 方法净额 |
| 4 | M5_asym_memory | `group_rank(subtract(ts_mean(neg, 252), ts_mean(pos, 22)), subindustry)` | 论文 Druz2016：失望长记忆 vs 欣喜短记忆 | 双周期价差（非对称记忆） |
| 5 | M6_neg_surprise | `group_rank(ts_zscore(ts_backfill(neg, 22), 252), subindustry)` | 开放问题 SY90356：negative 概率独立多空腿 | 负面腿 |
| 6 | M7_neutral_vacuum | `group_rank(ts_av_diff(ts_backfill(likelihood_of_neutral_tone, 22), 252), subindustry)` | 信息真空度（NTR 一阶变化） | 一阶差矩 |
| 7 | M8_peak_age | `group_rank(ts_arg_max(ts_backfill(pos, 22), 252), subindustry)` | 峰值年龄几何（情绪高峰距今天数） | 时间结构算子 |
| 8 | M9_nested_two_layer | `group_rank(ts_zscore(ts_av_diff(ts_backfill(pos, 22), 252), 252), subindustry)` | 金帖嵌套降相关模板2（异 op 双层） | 嵌套骨架 |
| 9 | M10_tsmean_swap | `group_rank(ts_zscore(ts_mean(pos, 22), 252), subindustry)` | 开放问题 SY90356/FF65210：ts_backfill vs ts_mean 对照 | 预处理替换对照 |
| 10 | M11_prob_transform | `group_rank(ts_quantile(ts_backfill(subtract(pos, neg), 22), 66), subindustry)` | 净差+概率变换（66 窗） | 非线性几何 |
| 11 | M12_label_gate | `trade_when(greater(ts_mean(overall_sentiment_score, 22), ts_mean(overall_sentiment_score, 252)), ts_zscore(ts_backfill(subtract(pos, neg), 22), 252), -1)` | argmax 标签转折作门控（lab 以条件入场=类别卡合规） | 条件门控骨架 |

注：表达式中 `pos`/`neg` 展开为 `positive_sentiment_probability_3` / `negative_sentiment_probability_3`（JSON 内全称）。**M2 与 M1 同骨架换 d1 是设计内对照臂**（两种信息持有假设），一腿一票裁剪时留一。M4/M5 为同量纲净额/双周期价差=类别卡合规；无裸 rank(field)、无加权混合、无双独立信号腿 add。

## 五、双预检与派发实录

- 字段存在性 `preflight_expressions`：valid=true，unknown_fields=[]，platform_field_count=6（pos/neg/ntr/lab/m1/m2 全命中）。
- 语法 `verify_expr.py`：12/12 valid=true。
- 算子硬闸：全部算子（ts_zscore/ts_backfill/ts_av_diff/ts_mean/ts_arg_max/ts_quantile/subtract/greater/group_rank/trade_when）均在本战役已实测出数名单内；未用 ts_scale/ts_max/ts_min。trade_when 槽位=(条件, alpha, -1) 复核 ✓。
- 塔混终检：全部字段属 earnings_sent_matrix 单集（earnings 单塔），零 PV 内建字段 ✓。
- 派发 2026-11-03 07:4x：task `ernsentw1_20261103`，pid 61064，batch-size 2 / concurrency 1 / detached。CSV=outputs/earnings_sent_matrix_wave1_templates_simulation_status.csv。

## 六、全波收口（12/12 全 COMPLETE 零 ERROR）

| # | 臂 | S | TO | 判 |
|---|---|---|---|---|
| 0 | M1 POS 惊喜 d1=22（照抄臂） | −0.01 | 0.25 | 平 |
| 1 | M2 POS 长持有 d1=252 | +0.32 | 0.061 | 干净弱正 |
| 2 | M3 净差惊喜 pos−neg | +0.56 | 0.25 | 第 3 |
| 3 | M4 测量分歧 m1−m2 | +0.03 | 0.61 | 灭（TO 爆）|
| 4 | M5 非对称记忆 | −0.66 | 0.24 | 负向强 |
| 5 | M6 NEG 惊喜 | −0.46 | 0.25 | 负向 |
| 6 | M7 中性真空 | −0.21 | 0.25 | 弱 |
| 7 | M8 峰值年龄 | +0.29 | 0.034 | 弱正极净 |
| 8 | M9 嵌套双层 | +0.60 | 0.26 | 第 2 |
| 9 | M10 ts_mean 替换 | −0.01 | 0.25 | 平 |
| 10 | **M11 概率变换 ts_quantile(净差,66)** | **+0.63** | 0.27 | **全波最强** |
| 11 | M12 argmax 标签门控 | +0.46 | 0.062 | 干净 |

**归因**：① **方向一致性成立**——净差族（M3 +0.56 / M9 +0.60 / M11 +0.63 / M12 +0.46）全正，NEG 腿独立为负（M6 −0.46）⇒ **失望腿（negative tone）是信息主载体**，与 Druz 2016「disappointment≫delight」先验吻合；② 概率变换几何（ts_quantile）> 嵌套 > 裸惊喜（照抄臂 −0.01 灭——金帖骨架在 DEU 不出货，d1 短期面死）；③ M4 测量分歧灭+TO 0.61，m1/m2 不承载分歧；④ max|S|=0.63 距闸 1.58 差 60% ⇒ **earnings_sent_matrix×DEU 组合判弱收口**（按机制×数据集二维律只封本组合），失望腿非对称机制记为跨集迁移种子（ern6 SUE 面/analyst 修正面可复测）。


