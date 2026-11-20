# EUR · macro27 交付候选报告（2026-11-20）

> 数据集：`macro27`（Job records from job posting，33/33 全 VECTOR，cov 0.3273，mult 1.2，2026-03-01 onboard）
> 字段画像全文：`tracking/EUR/reference/profiles/eur_macro_macro27_profile_20261120.md`
> 候选：**`RReEEgwb`**（EUR/D1/TOP2500/decay16/INDUSTRY/trunc0.08）

## 一、回测字段

| 项 | 值 |
|---|---|
| 表达式 | `trade_when(ts_sum(vec_sum(mcr27_company_jobscreated), 22) > 0, group_zscore(ts_quantile(ts_backfill(divide(vec_sum(mcr27_company_jobscreated), add(vec_avg(mean_days_job_closed), 1)), 66), 252), industry), -1)` |
| Sharpe | **2.18** |
| Fitness | **1.27** |
| 2Y Sharpe | **2.62**（EUR IS_Ladder 固定限 2.02） |
| Turnover | **17.39%** |
| Returns | 5.94% |
| Drawdown | 2.62% |
| Margin | 6.83 bp |
| sub_universe_sharpe | 1.54 |
| investability_sharpe | 1.21（保留比例 0.555，落在内部严线分离带 0.45–0.839 灰区） |
| risk_neutralized_sharpe | 2.11（**有值 ⇒ 标准档，非风险线**） |
| long / short count | 750 / 763 |
| prod 相关性 | **0.5339**（平台 <0.7 ✓ / 内部严线 <0.65 ✓） |
| self 相关性 | **0.2613**（平台 <0.7 ✓ / 内部严线 <0.50 ✓） |
| platform checks | `checks.fail` 空，`ra_failed=false`，LOW_SHARPE/LOW_FITNESS/TO/CW/SUB/2Y/MATCHED_PYRAMID 全部 PASS |
| pyramid | **EUR/D1/MACRO**（mult 1.2，该塔当前 0/3） |

## 二、字段画像（要点）

- 33 字段 = 6 语义族：流量（jobscreated / jobsremoved）、存量（jobsactive）、净增（ajnet）、时长（mean_days_job_active / mean_days_job_closed）、桶级（bucket_*，cov 0.1478）、元数据/质量标记。
- 全部 VECTOR ⇒ 须 vec_avg / vec_sum 降维；净流量字段带 `Unit[CSPrice:1,CSShare:1]` ⇒ 与常数做算术须先 rank() 化（同量纲相减合法）。
- 覆盖率 0.3273（稀疏事件型）⇒ 事件日之外无信息，是门控判据的适用面。
- 拥挤度极低：绝大多数字段 aC ≤ 5，`mcr27_company_jobscreated` aC 17。

## 三、匹配机制

**「招聘需求的可持续性」**：公司**新发布的岗位数 ÷ 这些岗位被撤下的平均存续天数**。

- 分子 = 招聘投入的强度（当月新发岗位）；
- 分母 = 岗位被撤销前的存续时长——**长**说明岗位是结构性需求（招了就不撤），**短**说明是试探性/虚假招聘（挂两天就撤）；
- 两者相除 = 每单位「撤销速度」对应的新增岗位量 ⇒ 招聘行为的**净可持续性**；
- 事件门控（22 天内有新岗位才持仓）= 只在招聘动作真正发生时建仓。

## 四、调优过程

| 阶段 | 关键动作 | 读数变化 |
|---|---|---|
| 基线 | `ts_mean(group_zscore(vec_avg(stable_boundary_trade_count_21d_active), country), 22)` | S1.64 / F1.05 / 2Y2.61，prod 0.8887 |
| 时长归一 | 分母改「撤岗时长」（而非活跃存续天数） | S1.47 / F0.81 / 2Y1.77（换回活跃时长 S−0.01 全灭） |
| 连续化外层 | `group_rank` → `group_zscore`（保留幅度） | prod 0.7462 → **0.4983**（重尾内核专用杠杆） |
| 长 zscore 窗 | 252 → 504 / 756 | S 1.54 → 1.81 |
| **presence 宽门控** | `ts_sum(jobscreated,22) > 0` | F 0.90 → 0.97，TO 21.95% → 21.0% |
| **decay16** | 12 → 16 | TO 21.0% → 17.4%，S 1.88 → 2.18，**F 0.97 → 1.27** |
| **ts_quantile 内层** | `ts_zscore` → `ts_quantile`（重尾比值上做分位映射） | S 1.84 → 2.18，F 1.03 → 1.27，2Y 2.27 → 2.62 |
| 组合定稿 | 门控 + decay16 + ts_quantile + group_zscore | **S2.18 / F1.27 / 2Y2.62 / TO17.4% / prod0.5339** |
| 被否路径 | TOPCS1600（该核依赖大市值高招聘量股票，S 掉到 1.4）/ trunc0.1（空操作）/ 桶级门控 / 净增核 / 撤岗率核 / 活跃时长核 | 全部劣于定稿 |

## 五、结论判据

| 判据 | 读数 | 结论 |
|---|---|---|
| 平台 RA/PPA | failed_ra 0 / failed_ppa 0 | ✅ |
| 平台 checks | fail 列表空 | ✅ |
| S / F / 2Y / sub / TO / CW | 2.18 / 1.27 / 2.62 / 1.54 / 17.39% / PASS | ✅ |
| prod（平台 0.7 / 内部 0.65） | 0.5339 | ✅ 双过 |
| self（平台 0.7 / 内部 0.50） | 0.2613 | ✅ 双过 |
| TO 内部严线 [5%,20%] | 17.39% | ✅ |
| 档位性质 | risk_neutralized_sharpe 有值 | ✅ 标准档（可交付） |
| 塔位 | EUR/D1/MACRO 0/3 | ✅ 新塔（点亮第 1 席） |
| 数据层 | 2014–2020 零持仓属**序列起点型缺失**（用户 2026-11-20 已放开年限约束） | ✅ 不构成排除 |
| 内部严线残余 | investability 保留比例 0.555（灰区，非硬失败） | ⚠ |
| 提交 | 需用户明确确认（不可逆） | ⏸ **未提交** |

**交付判读**：这是本条线上第一颗**平台闸全绿 + 内部严线全过 + 落在未点亮新塔（MACRO 0/3）**的候选；`A1xVVA5w`（同结构、ts_zscore 内层，S1.84/F1.03/TO17.8%）作备份，prod 待测。
