# macro27（DEU 招聘趋势）波 1 模板池 — 金帖两读 + 论文取证

> 状态：双预检全绿（字段 5/5 确认 + 语法 12/12 PASS）→ 待并发空位派发。并发纪律 ≤2 runner（snt27 pid 54700 + covprobe pid 62660 占满）。
> 数据集：macro27（13 VECTOR，ac 165）。单数据集 ATOM，零内建字段 = 单 MACRO 塔，不触碰 trio×非trio 配额（已满 5/5）。

## 一、金帖两读（AK85882《招聘变化与业务扩张：hiring_trends 在 USA》，article 43322749748503，92 赞 / 12 评）

### 作者提交占位（生产池拥挤度先验）
- 作者迭代链：e79r6wVp（S 1.57）→ GrdogzX3（S 2.40，Ladder 过，RA 先到先得）→ pwP7a10b（**S 3.00 / F 1.88 / TO 16.9% / Margin 7.86bps**）。
- **关键**：作者是 USA/TOP3000/D1 + INDUSTRY/SLOW 中性化，**不是 DEU**。DEU macro27 是跨区迁移验证，不是同池竞争；帖子明确「只比较 IS，不把 PC 纳入筛选」。
- 金帖获胜式（USA）：`group_rank(if_else(p>0, (a-p)/p, NaN), industry)`，a=vec_avg(存量)，p=ts_delay(a,21)，Decay 5 / Trunc 0.01。

### 帖子「未解决疑问」面 = 差异化模板空间
1. 招聘变化里多少是真实经营信息？（重复发布 / 长期未招满 / 采集覆盖变化）→ is_job_repost_flag 门控 / 分层。
2. 收入条件为什么没帮助？（删掉后 S 1.57→3.00）→ 减法对照，收入硬筛滞后信号介入点。
3. 换时间和市场后是否成立？（有效历史仅 2019–2023）→ **DEU 正是这个问题**，逐年覆盖闸必查。
4. JZ76850：vec_count 报告条数变化是否驱动读数波动 → 报告条数门控轴。
5. AK76468：简化式 `group_rank(ts_delta(a,21), industry)`（绝对 delta vs 变化率几何对照）。
6. BW14163（EUR/D1 实测）：`vec_skewness(bucket_avg_days_job_closed)` 180 日回填 + 66 日滞后 120 日相关 + country 标准化 → **矩变换 + 时序相关结构**，S 2.49/2.22 双过。最强迁移先验。
7. TT92977：按报告条数门槛复跑 + 年份分段稳定性。

## 二、论文先验（机制验证）
- Lin-Song (2026, Pacific-Basin)：JP_Growth = 同比（q/q−4−1）**不是 21 日环比**，正预测 sales growth（1sd→+1.79%）/ earnings surprise / 股价，多空月超额 1.254%。
- Campello-Kankanhalli-Muthukrishnan (2020)：招聘扩张公司后续季度风险调整收益更高。
- Gutiérrez et al. (2020)：job postings 预测业绩与股价（US）。
- 机制 = revealed preference（行动难造假）；招聘领先官方就业 2–3 月（Lightcast）。
- 风险：ghost jobs（挂而不招）、季节性（校招秋 / 预算 Q1，**同比窗口天然去季节**）、岗位滞留（filled 后仍挂）。
- Lin-Song 调节：劳动密集/国企/低市场化弱；信息环境差/亏损/子公司级强（DEU TOP500 无国企轴，用 SUBINDUSTRY 分组）。

## 三、12 模板池（结构互异轴：变化率 / delta / 同比 / 矩 / 反向 / 净额 / 二阶 / 门控×2 / 价差 / 概率变换）

| # | 骨架 | 核心信号 | 结构轴 | 来源 |
|---|---|---|---|---|
| T1 | 存量环比变化率 | (a−a₂₂)/a₂₂ | 变化率几何 | **金帖照抄（≤1）** |
| T2 | 绝对 delta | ts_delta(a,22) | 差分几何 | 开放问题⑤ AK76468 |
| T3 | 同比 504 | (jobscreated−₅₀₄)/₅₀₄ | 长窗去季节 | 论文 Lin-Song JP_Growth |
| T4 | 时序相关结构 | ts_corr(days_closed,lag66,252) | 分布形状 | 开放问题⑥ BW14163 |
| T5 | 填岗速度反向 | −ts_mean(days_closed,66) | 语义反转 | 论文（短=需求强） |
| T6 | 招聘净流 | ts_mean(created−removed,22) | 同机制净额 | 论文扩张 + 金帖 |
| T7 | 二阶加速度 | ts_delta(Δa,22) | 二阶矩 | 自建 |
| T8 | ghost 门控+净流 | trade_when(低重招率,净流,−1) | 条件触发 | 开放问题① |
| T9 | 报告条数门控+环比 | trade_when(vec_count>0,环比,−1) | 数据质量条件 | 开放问题④ |
| T10 | 快慢价差 | 5 vs 66 动量差（同字段） | 双周期价差 | 自建（合规） |
| T11 | 概率变换 | ts_quantile(净流,66) | 非线性几何 | earnings M11 迁移 |
| T12 | repost 率反向 | −ts_mean(is_job_repost_flag,66) | 反向 | 开放问题① |

照抄臂 1（T1）≤1 ✓；开放问题臂 T2/T4/T8/T9/T12 = 5 ≥3 ✓。

## 四、派发前硬闸（已过）
- 算子硬闸：13 用到算子全部在 get_operators 103 精确名单（ts_corr 在册，BW14163 迁移可行）。
- 金帖三雷全避：无 ts_max/ts_min 幽灵、情绪 ts_zscore 外层（macro27 非情绪族）、quantile 双位置参（用 ts_quantile(x,66) 合法）。
- trade_when 槽位 =（条件, alpha, 出场条件）✓ 条件第一槽，z=−1。
- 量纲：issuer 级聚合计数（jobscreated/removed/active）用 vec_avg 保值；days 字段 vec_avg；无 add(量纲,裸常数)。
- 塔混：单 MACRO 塔，零内建字段，trio×非trio 配额不动。
- 类别卡：group_rank 带 subindustry 分组轴 ≥2 参 ✓；禁裸 rank ✓；净额/同字段价差合规 ✓。

## 五、派发实录（待空位）
- JSON：tracking/DEU/macro27_wave1_templates.json（12 臂，DEU 标准设置 decay4/SUBINDUSTRY/trunc0.08）。
- 任务 id：待派发时定。收批必跑 get_alpha_yearly_stats 逐年覆盖闸（连续多年空窗才排除，macro27 cov=0.0 系稀疏失真）。
- 归因按模板编号（T1–T12），哪族出货 / 哪族全灭。
## 六、覆盖闸实测（covprobe 4 臂，2026-11-03）— 改判 macro27/sm12 优先级

| 探针 alpha | 字段 | 逐年 longCount | 覆盖判定 |
|---|---|---|---|
| O0AxdjL1 | mcr27_company_jobscreated | 2014-15 空 / 2016-20 稀疏(2-9) / 2021-23 满(66-119) | leading gap 2 年 + 中段稀疏 |
| RRE1xoO0 | mean_days_job_closed | **2014-2020 七年全空** / 2021-23(61-120) | ★严重 leading gap，有效史仅 3 年 |
| E56en9vK | scl12_buzz | 2014-23 全满(104-185) | ✓✓ 满覆盖 clean |
| A1V7Xo0Q | scl12_sentiment | 2014-23 全满(105-187) | ✓✓ 满覆盖 clean |

### 判读
- **sm12（socialmedia12）满 10 年覆盖** → cov=0.0 系稀疏失真已证伪，是可靠基底；对应「研报热度反转」机制（buzz/sentiment），应优先。
- **macro27 严重前段空窗**：mean_days_job_closed 仅 2021-2023 有数（连续空窗 7 年），jobscreated 空 2014-15 + 2016-20 稀疏。金帖自曝 USA「有效史 2019-2023」，DEU 更糟。
- **对已派 macro27 波的影响**：T4/T5（mean_days_job_closed 腿）有效史仅 3 年，IS_LADDER/2Y 高危；T1/T2/T3/T6-T11（jobsactive/created/removed 腿）中段稀疏但 2021+ 满。覆盖闸在入篮时逐颗核验（leading-gap 裁定未决，暂保留但标旗）。
- **优先级改判**：sm12 > macro27。下一波优先 sm12（研报热度反转，满覆盖）。

