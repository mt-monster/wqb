# sentiment27 波1 模板池台账（DEU / TOP500 / D1 / SENTIMENT 单塔，snl27 集内 ATOM）

## 一、战略定位（2026-11-03 金帖两读定调）

**本波 = 「换测量本身」的 extraction，不是 snt7 脉冲线的第 4 代变体。**

- 维基突压金帖（LC97552，2026-09-02，72 赞/21 评）作者三代同线 **PC 爬台阶 0.319→0.557→0.6338（=SC）**；JR57542 实测同族兄弟变体互相关 0.94 级 ⇒ **该线只剩一个槽位，继续换壳大概率撞 0.7**；作者复用警告原话「换 ATTENTION_MEASURE 字段源，而非复制字段组合」。
- 但评论 XC78928 反向实测：「snt7 纯突增字段过得了反转模板，**relpopularity 稳态人气字段一上来就挂**」⇒ snl27 当主信号必须做**动态/突变面**（偏离/脉冲/变化），**禁做水平面**（Chalamandaris 2026「情绪水平只可测量不可交易」互证）。
- 本波 15 臂全部 snl27 集内动态面：这是与 np7nn69l（snt7 主信号+snl27 中性化腿）的**信号主体差异**；但提交前必查 PC/SC（YL61874：注意力类存量供给密，别等提交才发现）。

## 二、论坛金帖两读

### 2.1 LC97552《维基百科关注度突压信号 sent 在 DEU》（article 43179860065303）
- **作者提交占位**：三代已提交/全过（PC 0.319→0.557→0.6338）；DEU/SENTIMENT 金字塔×1.9；获胜式 np7nn69l = vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt7_all_languages_views),22),5),5),22),120), ts_backfill(vec_avg(snl27_relpopularity08),22))，S 2.04/F 1.92/MG 24.2bp/TO 9.11%。
- **实测教训（照抄前必读）**：ts_zscore 外层在该字段族**禁用**（全结构崩盘 SH −0.33）；rank 包装每剥一层 +FT 0.3-0.65（脉冲型字段 rank 有害）；SUBINDUSTRY(2.18)>INDUSTRY(1.79)>SECTOR(1.53 FAIL)；decay 甜点随骨架重置（dec16/trunc0.02）；ts_backfill(22) 防 CW 权重集中；**ts_max 平台无此算子**（恒等式 subtract(x, ts_max_diff(x,w))）；帖子 quantile(x,120) 是 2 位置参**签名不合法**（平台 quantile 只收 1 位置参），且 120 不在 DEU 白名单。
- **开放疑问面（差异化臂来源）**：① 回落时点 ts_arg_max 峰值年龄 vs 峰值强度 ② 突降反向未测（JR57542：反向不是镜像，必须独立测）③ group_neutralize 替代 vector_neut 第 4 骨架 ④ snl27 α=0.8 平滑敏感度 ⑤ XM75236「基线偏离 vs 脉冲」对照 ⑥ XZ17517 ts_backfill 伪脉冲污染（数据可得性造假突增）。
- 评论区附加：DS48533 照抄模板 KOR 出 PPA+RA（group_neut(ts_decay_linear(rank(a)−rank(b),10), sector)）；FF45555：同模板跨区方向可反转；YL61874：注意力类跨区迁移 PC 0.78-0.84 全线超阈。

### 2.2 HH77144《股票舆情热度的反转效应与热点反应因子》（article 35876513619607，中信建投研报复现）
- 热点漂移因子：zscore(ts_decay_linear(abs(buzz),5))，反转特性加负号；weight 超标用 hump 平滑（winsorize 会严重削弱信号——开放问题）。
- **热度-价格背离四象限**：热度涨+价涨=负 alpha（追涨回调）/ 热度涨+价跌=正（派发退潮）/ 热度跌+价涨=负 / 热度跌+价跌=正（抗跌定价偏差）。⚠️ 价格腿=PV 内建字段——按塔混口径内建不算另一 PV 数据集，但为单塔纯净本波不收，留作波 2 备选。
- 评论补充：信息分散度 Z=ts_std_dev(volume,21)/ts_mean(volume,21) 动态切换动量/反转方向（volume=内建，同上留波 2）。

## 三、论文取证（web_search 2026-11-03）

- **Da-Engelberg-Gao (2011) In Search of Attention**：SVI 突增 → 随后 1-2 周收益延续 → **年内反转**（XZ17517 评论同引）。
- **Liu-Peng (2015)**：AbnAttention = 对过去一年基线（360~31 日均值）的偏离——T1 基线偏离臂的直接模板；注意力有季节性（周五/夏季低）。
- **新闻联播注意力研究 (2013)**：注意力事件后 day2 +0.36%、**day3-15 反转 −0.92%**、成交量 1.87 倍——短周期反转面窗口依据。
- **韩国消息板排名研究 (2013)**：上榜日异常放量、散户持续买入一周、**收益效应 2 天内消散**。
- **注意力传染模型 (2015)**：有限注意→反应不足动量，正反馈投资者→反转，动量与反转共存（呼应帖 1 信息分散度切换）。
- **Chalamandaris (2026)**：情绪状态真实影响横截面定价（FF25 R² 0.10→0.31）但**水平不可交易**——动态面才有 alpha。

## 四、模板池（15 臂结构互异；照抄臂 0、开放问题臂 5；全部动态面）

| # | 名称 | 核心结构 | 机制面 / 来源 |
|---|------|----------|--------------|
| 0 | T1_pop_baseline_dev | ts_av_diff(relpop08, 252) | 异常人气对年基线偏离（Liu-Peng；XM75236 基线对照）|
| 1 | T2_rank_surge_inv | −group_rank(ts_av_diff(avgranking, 22)) | 排名骤升=人气突增（排名数值反向）|
| 2 | T3_fast_slow_spread | mean(relpop08,5) − mean(relpop08,66) | 热度消退速度（day3-15 反转窗口）|
| 3 | T4_pop_backfill_dev | ts_av_diff(ts_backfill(relpop08,22),22) | snt7 T8 迁移种子改型（防 CW 回填）|
| 4 | T5_peak_age | ts_arg_max(relpop08, 252) | **开放问题①**：回落时点/峰值年龄 |
| 5 | T6_top_drop_reverse | ts_av_diff(topranking, 22) | **开放问题②**：突降反向独立面（非镜像）|
| 6 | T7_alpha_variant_net | ts_av_diff(relpop08 − relpop1, 252) | **开放问题④**：α=0.8 vs 1 测量分歧净额 |
| 7 | T8_rank_gap_dispersion | ts_av_diff(avgranking − topranking, 22) | 排名分布 gap 扩大=注意力分散 |
| 8 | T9_skew_dynamic | ts_av_diff(skewness, 252) | 分布偏度动态（注意力集中度迁移）|
| 9 | T10_kurt_probgeom | ts_quantile(kurtosis, 66) | 尾部极端度+概率变换几何 |
| 10 | T11_footprint_growth | ts_delta(ts_mean(totaldomains,22),22) | 数字足迹扩张（平滑后差分，稀疏合规）|
| 11 | T12_cctld_share_dynamic | ts_av_diff(ccTLD/totaldomains, 252) | 本地化注意力占比动态（同集内比率）|
| 12 | T13_alpha1_control | ts_av_diff(relpop1, 252) | T1 的 α=1 对照臂（设计内对照）|
| 13 | T14_heat_gate | trade_when(relpop08>mean252, 排名反冲, -1) | 条件门控：高人气环境做排名反转 |
| 14 | T15_decay_weighted | ts_decay_linear(ts_av_diff(relpop08,22),22) | 帖 1 热点漂移衰减加权结构 |

结构轴：基线偏离/排名反向/双周期价差/回填偏离/时间峰值年龄/反向突降/测量净额/分布 gap/偏度动态/概率几何/计数差分/比率动态/对照变体/条件门控/衰减加权——15 轴互异 ✓。
类别卡复核：无裸 rank(field)（全臂前置变换）；无加权混合；T7/T8 为同机制净额（同字段测量变体/同分布统计量）；窗口全白名单（5/22/66/252）；算子全在实测名单（ts_av_diff/ts_arg_max/ts_mean/ts_backfill/ts_delta/ts_quantile/ts_decay_linear/group_rank/trade_when/greater/subtract/divide/vec_avg）；未用 ts_max/ts_zscore 外层/quantile 双位置参（金帖三雷全避）。
塔混终检：全字段 snl27 集内（sentiment 非目标塔单塔）✓ 零 PV 内建字段 ✓。trade_when 槽位=(条件, alpha, -1) ✓。

## 五、双预检与派发实录

- 字段存在性 `preflight_expressions`：valid=true，unknown_fields=[]（snl27 全部字段命中）。
- 语法 `verify_expr.py`：15/15 valid=true。
- 派发 2026-11-03 07:5x：task `snt27w1_20261103`，pid 54700，batch-size 2 / concurrency 1 / detached。CSV=outputs/sentiment27_wave1_templates_simulation_status.csv。
- 收批时必看：① 按模板轴归因（动态面 vs 水平面）② 若出货提交前必查 PC/SC（注意力类存量拥挤，YL61874 教训）③ 与 np7nn69l 线（PC 0.6338）互相关风险。
