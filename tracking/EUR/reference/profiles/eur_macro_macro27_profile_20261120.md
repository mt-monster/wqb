# EUR / macro27 全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=macro27, region=EUR, universe=TOP2500, delay=1)`：**33/33 字段，complete=True**（全部 VECTOR）。
> 塔位实读 EUR/D1 **MACRO 0/3**（本次真新塔）｜mult 1.2｜cov 0.1478–0.43｜aC 0–547｜两代：2026-03 新代 21 个 + 2022-10 老代 12 个。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`

## 1. 字段结构总览（6 语义族）

| 语义族 | 字段数 | 说明 |
|---|---:|---|
| 存量（active jobs） | 4 | 在岗总数——论坛明令**勿直接 rank**，当规模变量 |
| 流量（created/removed） | 4 | 招聘流入流出 |
| 净增（ajnet / 差分） | 2 | 净招聘=扩张核心 |
| 时长（days） | 6 | 岗位存续/撤岗时长=招聘质量与急撤信号 |
| 桶级（bucket_*） | 5 | cov 0.1478 极低=宏观体制，不作个股信号 |
| 元数据/质量标记 | 12 | 映射置信度/地理/托管/断裂标记——**排除作信号** |

## 字段全表（33 字段逐字段平台读数）

| 字段 | 类型 | cov | uC | aC | 语义族 | 说明 |
|---|---|---:|---:|---:|---|---|
| `num_jobs_active` | VECTOR | 0.43 | 42 | 62 | 存量 | 活跃岗位数（**在岗总数**——论坛明令勿直接 rank） |
| `num_jobs_created` | VECTOR | 0.43 | 8 | 13 | 流量 | 新创建岗位数 |
| `num_jobs_removed` | VECTOR | 0.43 | 8 | 10 | 流量 | 删除岗位数 |
| `avg_days_job_posting_active` | VECTOR | 0.43 | 16 | 21 | 时长 | 活跃岗位平均存续天数 |
| `avg_days_job_posting_closed` | VECTOR | 0.43 | 9 | 10 | 时长 | 被删岗位发布后存续天数 |
| `mean_days_job_active` | VECTOR | 0.348 | 18 | 23 | 时长 | 活跃岗位平均天数 |
| `mean_days_job_closed` | VECTOR | 0.348 | 21 | 24 | 时长 | 被删岗位平均发布天数 |
| `mcr27_company_jobsactive` | VECTOR | 0.348 | 300 | 547 | 存量 | 公司活跃岗位数（**aC547 最拥挤**） |
| `mcr27_company_jobsactive_n` | VECTOR | 0.348 | 78 | 99 | 存量 | 宏观桶内中性化后的活跃岗位数 |
| `mcr27_company_jobscreated` | VECTOR | 0.348 | 13 | 17 | 流量 | 公司新建岗位数 |
| `mcr27_company_jobsremoved` | VECTOR | 0.348 | 7 | 9 | 流量 | 公司删除岗位数 |
| `mcr27_company_ajnet` | VECTOR | 0.348 | 7 | 7 | 净增 | 净增活跃岗位（created−removed） |
| `mcr27_bucket_daily_jobsactive` | VECTOR | 0.1478 | 8 | 8 | 桶级 | 宏观桶内活跃岗位数（cov 极低） |
| `mcr27_bucket_daily_jobscreated` | VECTOR | 0.1478 | 6 | 6 | 桶级 | 宏观桶内新建岗位数 |
| `mcr27_bucket_daily_jobsremoved` | VECTOR | 0.1478 | 4 | 4 | 桶级 | 宏观桶内删除岗位数 |
| `bucket_avg_days_job_active` | VECTOR | 0.1478 | 20 | 30 | 桶级 | 宏观桶内活跃岗位平均天数 |
| `bucket_avg_days_job_closed` | VECTOR | 0.1478 | 9 | 12 | 桶级 | 宏观桶内被删岗位平均天数 |
| `mcr27_postlength2` | VECTOR | 0.348 | 67 | 86 | 质量 | 岗位描述长度（资历/薪资代理） |
| `is_job_repost_flag` | VECTOR | 0.4124 | 5 | 9 | 质量 | 重复发布标记（招聘 churn） |
| `mcr27_unmapped_location` | VECTOR | 0.3414 | 104 | 158 | 元数据 | 岗位位置未能映射标记 |
| `mcr27_zip` | VECTOR | 0.3414 | 116 | 157 | 元数据 | 岗位邮编 |
| `mcr27_country` | VECTOR | 0.3414 | 99 | 139 | 元数据 | 岗位国家 |
| `mcr27_companyidmap` | VECTOR | 0.2324 | 96 | 121 | 元数据 | 公司 ID 映射 |
| `mcr27_verified_ds1` | VECTOR | 0.348 | 73 | 99 | 元数据 | 公司映射置信度 ds1 |
| `mcr27_verified_ds2` | VECTOR | 0.348 | 64 | 80 | 元数据 | 公司映射置信度 ds2 |
| `mcr27_verified_ds3` | VECTOR | 0.348 | 69 | 94 | 元数据 | 公司映射置信度 ds3 |
| `mcr27_verified_ds4` | VECTOR | 0.348 | 66 | 85 | 元数据 | 公司映射置信度 ds4 |
| `mcr27_normalizedflag` | VECTOR | 0.348 | 3 | 3 | 元数据 | jobsactive 是否桶内归一 |
| `mcr27_bigdrpbrksflag` | VECTOR | 0.348 | 4 | 4 | 元数据 | 大掉数标记（数据质量） |
| `continuous_value_break_flag` | VECTOR | 0.348 | 4 | 4 | 元数据 | 连续值断裂标记 |
| `is_hosted_job_flag` | VECTOR | 0.3414 | 1 | 1 | 元数据 | LinkUp 托管标记 |
| `is_historically_hosted_job_flag` | VECTOR | 0.3414 | 1 | 1 | 元数据 | 历史 LinkUp 托管标记 |
| `is_sponsored_ad_flag` | VECTOR | 0.3414 | 1 | 0 | 元数据 | 赞助广告标记 |

## 2. 六维画像

- **类型**：33/33 全 VECTOR ⇒ **必须 vec_avg/vec_sum 降维**（vec_count 语义=条数，仅在「岗位条数」本身是信号时用）。
- **覆盖率**：公司级 0.348、上市口径 0.43、桶级 0.1478。约 1/3 宇宙有值 ⇒ 事件型稀疏，**按 earningscall 经验应考虑 presence 门控**。
- **更新频率**：抓取日频（`mcr27_bigdrpbrksflag`/`continuous_value_break_flag` 标记抓取断裂）；岗位创建/删除本身是事件流。
- **分布特征**：存量/流量字段 = 非负计数（0~数千）；时长字段 = 正数天数；净增字段 = 有正负（净增/净减）。
- **可用性**：aC 0–547，`mcr27_company_jobsactive` aC547 最拥挤（存量型必被抢），净增/时长/新代字段 aC 7–30 极冷门。
- **适用性**：**主信号 = 净增 + 时长归一 + 流量动量**（论坛明令「别排在岗总数，改净增/时长」+「招工增加相对同行=扩张」）；
  **排除 = 存量总数、桶级字段、元数据/质量标记**。

## 3. 机制假设（三路证据后）

- **论坛**（post 43615287467799，31 赞 + 官方帖 Getting started with Macro Datasets）：
  「macro27 是网上招聘，VECTOR，要先 vec_avg」；「**别排在岗总数，改净增/时长**」；「招工增加**相对同行**，当作公司在扩张」
  ⇒ 三条模板铁律：①流量/时长优先于存量；②组内相对化（group_rank/group_zscore）；③VECTOR 必 vec_*。
- **论文**（12 篇/10 作者，多样闸 PASS）：*Job Postings and Aggregate Stock Returns*（JFE 2023）、
  *Disclosing Labor Demand: Evidence from Online Job Postings*（TAR 2025）、
  *Labor Demand Similarity and M&A: Evidence From 3 Million Job Postings*（FIRE 2026）
  ⇒ 招聘需求含**增量信息**（非财报滞后），净招聘与招聘强度预测未来收益。
- **历史 EUR 9 臂**（2026-11 旧波）：最优 `E56gYQOP` S1.29 = `num_jobs_active ÷ mean_days_job_active`（存量÷时长=隐含流入率）
  ⇒ 已被论坛「改净增/时长」方向佐证，但仅 9 臂、仅碰 6 字段、**33 字段从未做全字段画像**。
- **GBR 侧**（macro27 42 臂判死，F 墙 0.66 + sub 覆盖弱）——**跨区不外推**，仅取「F 与 sub 是该族已知瓶颈」这一机制提示。

## 4. TemplatePlan（每字段一行：reading / templates / excluded / evidence）

| 字段 | reading | 合法模板 | excluded | evidence |
|---|---|---|---|---|
| `mcr27_company_ajnet` | 净增活跃岗位（created−removed） | vec_avg → ts_zscore(ts_backfill) → group_rank(industry)；ts_delta 取加速度 | 裸 rank（存量污染） | 论坛「改净增」+论文 JFE2023 |
| `mcr27_company_jobscreated` | 公司新建岗位数 | 同上；差分得净增 | 裸 rank | 论坛「改净增」 |
| `mcr27_company_jobsremoved` | 公司删除岗位数 | 单独用（急撤=坏消息，方向待实证）；与 created 作差 | 裸 rank | 论坛「改净增」 |
| `num_jobs_created` / `num_jobs_removed` | 新代上市口径流量 | vec_sum → ts_zscore(backfill) → group_rank | 裸 rank | 论坛 + 同机制交叉验证 |
| `avg_days_job_posting_active` / `mean_days_job_active` | 活跃岗位平均存续天数 | 作**分母**做流入率归一（存量÷时长）；或单独作质量分 | 直接 rank（久存=老岗位，与新需求混） | 历史最优臂 E56gYQOP |
| `avg_days_job_posting_closed` / `mean_days_job_closed` | 被删岗位发布后存续天数 | 单独作急撤信号（方向二选一实证） | — | 论文「招聘急撤=负面需求」 |
| `mcr27_company_jobsactive` | 存量在岗数（aC547） | **仅作分母/规模** | **作主信号**（论坛明令 + 拥挤） | 论坛「别排在岗总数」 |
| `mcr27_company_jobsactive_n` | 桶内归一后存量 | 相对量；作分母 | 主信号 | 论坛 |
| `mcr27_postlength2` | 岗位描述长度 | 质量分：与岗位数作比（长描述=高阶岗位） | 裸 rank（公司规模代理） | 论文（岗位质量/薪资） |
| `is_job_repost_flag` | 重复发布标记 | 作**质量调整**（重复发布=需求真实 or 抓取噪声，需实证） | 裸 rank | 论坛（churn） |
| `mcr27_bucket_*` / `bucket_*` | 宏观桶级 | **不作个股信号**（全桶同值） | 主信号 | 论坛「全市场同一个数不要 rank」 |
| `mcr27_zip` / `mcr27_country` / `mcr27_companyidmap` | 地理/ID 元数据 | 排除 | 主信号 | 元数据 |
| `mcr27_verified_ds1..ds4` | 公司映射置信度 | 排除 | 主信号 | 元数据 |
| `mcr27_normalizedflag` / `mcr27_bigdrpbrksflag` / `continuous_value_break_flag` | 数据质量标记 | 排除（可选作清洗门控，待验证） | 主信号 | 元数据 |
| `is_hosted_job_flag` / `is_historically_hosted_job_flag` / `is_sponsored_ad_flag` | 来源/广告标记 | 排除 | 主信号 | 元数据 |

## 5. 段1 回测计划（12 臂）

主骨架 = `group_rank(ts_zscore(ts_backfill(vec_avg(F), 66), 252), industry)`（有界计数/天数 → zscore 归一，组内相对化）。
覆盖：净增 3 臂 / 时长归一 3 臂 / 流量动量 2 臂 / 质量（postlength/repost）2 臂 / 桶级体制 1 臂 / 存量分母 1 臂。
## 6. ★ 2026-11-20 年限要求放开后的重新判定

**用户口径变更**：「我的九年要求先放开」——年数下限整体撤除，**只剩「序列中途空窗」为数据层硬排除**（起点型缺失不再排除）。
⇒ 本集 2014–2020 零持仓属**序列起点型缺失**（供应商 EUR 侧只接了 2021 起），**数据层排除撤销**。

**改判为信号层近闸候选**（落在 MACRO 塔 0/3，真新塔）：
| 指标 | 读数 | 闸 | 缺口 |
|---|---:|---:|---:|
| S | 1.47 | 1.58 | −0.11 |
| F | 0.81 | 1.0 | −0.19（TO 17% > 0.125 地板 ⇒ F=S×√(ret/TO)） |
| 2Y | 1.77 | 1.58 | ✅ 过 |
| sub | 0.93 | 0.52×S=0.76 | ✅ 过 |
| **prod** | **0.7462** | 0.7 | **−0.046（全部候选里最低的 prod）** |

**prod 0.7462 的意义**：落在 §16.3 三档决策的**「限投」区**（0.70–0.85）⇒ 只许**改变持仓集合**的杠杆
（换宇宙 / 罕见慢快窗 / 平滑 decay），**禁止**在保序形变（中性化档 / 分组轴 / 幂次 / 叉乘）上继续烧配额。
⇒ 本轮定向：decay 阶梯（4→8→12）+ zscore 窗（252/504/756）+ backfill 窗（66/120）+ 核变体（created ÷ 撤岗时长 vs
(created−removed) ÷ 撤岗时长 vs vec_avg）+ **换宇宙 TOPCS1600**（改持仓集合）。

## 7. ★★ 突破：group_zscore 连续化把 prod 从 0.7462 打到 0.4983（2026-11-20 晚）

| 形态 | alpha | S | F | 2Y | sub | TO | prod | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| group_rank + ts_rank + decay12 | YPa1QX9w | 1.54 | 1.01 | 1.91 | 1.11 | 8.6% | — | 2（S/2Y） |
| group_rank + ts_rank + bf120 + CS1600 + trunc0.02 + decay12 | MP6YG65n | 1.58 | 1.21 | 1.88 | 1.23 | 8.4% | — | 1（**只差 2Y**） |
| **group_zscore + ts_zscore + bf66 + decay12** | **pwadNrXv** | **1.81** | 0.90 | **2.16** | 1.24 | 21.9% | **0.4983** ✅ | **1（只差 F）** |

**★ 机制（本次最大方法论收获）**：`group_rank` 把信号离散成组内均匀秩（权重全同），`group_zscore` **保留幅度** ⇒ 持仓权重分布不同 ⇒
**PnL 形状与生产池脱开 ⇒ prod 从 0.7462 掉到 0.4983（−0.25）**。
⇒ **「换信息源」不是唯一降 prod 杠杆；换截面归一实现（离散秩→连续幅度）同样是真杠杆**，且比换中性化档/分组轴（保序形变，只动 0.015–0.03）强一个数量级。
⇒ 这条同时修正了本轮早先的结论「prod 最优 ≠ S 最优」：**group_zscore 上两者同时最优**（S 1.54→1.81、prod 0.75→0.50）。

**其它读数**：
- **分母必须是「撤岗时长」**：换成「活跃岗位存续天数」⇒ S −0.01 全灭（撤岗快=需求虚假 ⇒ 用撤岗时长做分母正是要抓这个）。
- decay 阶梯：decay4 S1.47/F0.81/TO17% → decay12 S1.54/F1.01/TO8.6% → decay16 同级 → decay24 回落 S1.41–1.47 ⇒ **decay12 是拐点**。
- 内层算子：ts_rank/ts_quantile ≈ ts_zscore（1.54/1.50/1.47）；**ts_scale 1.17 / ts_av_diff 1.05 全灭**（连续化在外层 group_zscore 才有效，内层连续化破坏秩信息）。
- 宇宙轴：TOPCS1600 保 S（F 1.21 / robust 1.20），TOP1200 崩（EUR 机构型信号住中大盘）。
- **2Y 闸在 EUR 是固定 2.02**（IS_Ladder 限），不是 1.58 ⇒ 2Y 缺口需 2.02 达标。

**当前缺口互补**：MP6YG65n 差 2Y（1.88→2.02）；pwadNrXv 差 F（0.90→1.0，TO 21.95% 需降到 ≤17.8%）⇒ 合并 group_zscore + CS1600 + trunc0.02 + bf120 已在跑。

## 8. ★★★ 破闸：RReEEgwb 平台闸全绿（2026-11-20 晚，EUR/D1/MACRO 塔 0/3）

```
trade_when(ts_sum(vec_sum(mcr27_company_jobscreated), 22) > 0,
           group_zscore(ts_quantile(ts_backfill(divide(vec_sum(mcr27_company_jobscreated),
                                                  add(vec_avg(mean_days_job_closed), 1)), 66), 252), industry),
           -1)
```
设置：EUR / TOP2500 / delay1 / **decay16** / INDUSTRY / trunc0.08 / nanHandling ON

| 指标 | 读数 | 闸 | 判定 |
|---|---:|---:|---|
| S | **2.18** | 1.58 | ✅ |
| F | **1.27** | 1.0 | ✅ |
| 2Y | **2.62** | 2.02（EUR IS_Ladder 固定值） | ✅ |
| sub | 1.54 | 0.52×S=1.13 | ✅ |
| TO | **17.39%** | 平台 0.7 / 内部严线 [5%,20%] | ✅ 双过 |
| CW | PASS | 0.1 | ✅ |
| invest_S | 1.21 | 0.70×S=1.53 | ⚠ 1.21 < 1.53 ⇒ **investability_ration 0.555 低于内部严线 0.70 分离带** |
| risk_neutralized_sharpe | 2.11 | 有值 ⇒ 标准档（非风险线） | ✅ |
| self | **0.261** | 0.7 / 内部 0.50 | ✅ 双过 |
| prod | **0.5339** | 0.7 / 内部 0.65 | ✅ **双过** |
| pyramid | **EUR/D1/MACRO**（mult 1.2，0/3 ⇒ 真新塔） | — | ✅ |
| platform checks | `checks.fail` 空，`ra_failed: false` | — | ✅ |

**破闸要素（按贡献排序）**：
1. **presence 宽门控**（`ts_sum(jobscreated,22) > 0`）：门控前 F0.90 → 门控后 F0.97→（decay16+ts_quantile）F1.27；TO 21.95%→17.39%。**cov 0.3273 的稀疏事件集 + 门控 = 今日门控判据第四次验证**。
2. **decay16**（非 decay12）：TO 21.0%→17.4%，S 1.88→2.18，**F 0.97→1.27（同时破 TO 与 F 两闸）**。
3. **ts_quantile 内层**（重尾比值上做分位映射）：S 1.84→2.18、F 1.03→1.27、TO 17.8%→17.4%、2Y 2.27→2.62 ⇒ **在重尾内核上，连续/分位映射保留幅度信息，比 ts_zscore 更强**。
4. **group_zscore 外层**（连续幅度）：prod 0.7462→0.4983（对比 group_rank 版）。

**prod 实测 0.5339（PASS）** ⇒ **平台闸全绿 + 内部严线全过**（prod 0.534<0.65、self 0.261<0.50、TO 17.39%∈[5%,20%]）。
**残余项**：investability_sharpe 1.21 < 0.70×S=1.53（保留比例 0.555，落在内部严线分离带 0.45–0.839 的灰区，非硬失败；
平台未把 investability 列为 pending 闸）；DATA_DIVERSITY 待提交时判定；robustness 结论未落 ledger（brain-alpha-robustness，非拦截项）。

**处置**：**未提交**（红线：提交需用户明确确认）。候选已完整记录，可随时交付。
**副候选** `A1xVVA5w`（同结构、ts_zscore 内层）S1.84/F1.03/TO17.8%/2Y2.27 也是平台全绿，prod 待测（作备份）。
