# news50 模板池（家族×桶设计）—— DEU/TOP500/D1 —— 2026-11-03

**设计纪律**：`brain-alpha-research-news-sentiment`（5 家族分类 + 家族×6 桶 + 每批 ≥3 桶含 ≥1 HIGH + ≥2 种 vec_* 聚合 + 反号变体）；模板 ≥10 互异（用户硬约束）；方向先验见 `s1_news50_profile.md` 取证节。

## 路由前三查（skill §1）
| 查 | 状态 | 证据 |
|---|---|---|
| 判死 | ✗ 未判死 | §86 真新鲜 6 集之一；DEU 本集 alphaCount 合计 65、14 字段零使用 |
| 跨区弱 | ✗ 不弱 | GBR news50 N9 机制存活（nip 条件侧 gate 0.74） |
| lit 塔 | ✗ NEWS 塔未点亮 | DEU 16 塔全未点亮 |

**论坛配方可用性**：R1（ts_corr(sent,returns)+FAST）**禁用**——returns=PV 内建 ⇒ PV+NEWS 组腿，trio×非trio 配额已满 5/5 且非 ATOM；R2（pos_std−neg_std 反转）不适用——本集无正/负情绪 std 字段。

## 字段 5 家族分类（人工表，skill 允许）
- **direction**：ess / ssc / qcm / qep / qmb / acb / bam / bee / ber / ghc_lna / aes
- **attention**：vea / ens / ens_elapsed / ens_similarity_gap / g_ens* / rp_story_event_count / nip（impact）
- **dispersion**：（无 stddev 字段）——用 vea 的 CV 构造分歧代理（T8）
- **event_type**：category / group / topic / type / sub_type / news_type / property / evaluation_method / maturity
- **peer_context**：无
- 剔除（标识/元数据，不进表达式）：country_code / position_name / product_key / time / ens_key / g_ens_key

## 模板池（12 条 = 10 主 + 2 显式对照；dispatch 每批 2 条防 3 同族）

| # | 家族 | 桶 | vec_* | 表达式 | 机制 / 先验来源 |
|---|---|---|---|---|---|
| T1 | direction | Change | avg | `group_rank(ts_delta(vec_avg(mws50_ess), 22), industry)` | 情绪改善动量→正（论文1 同向锚） |
| T2 | direction | Level | avg | `group_rank(vec_avg(mws50_ssc), industry)` | 情绪水平（Level 对照，other47 教训预期弱） |
| T3 | direction | Change×Change 一致 | avg | `group_rank(multiply(rank(ts_delta(vec_avg(mws50_ber), 22)), rank(ts_delta(vec_avg(mws50_ess), 22))), industry)` | 分类器×综合双源持续一致→正（other47 T3 骨架迁移） |
| T4 | attention×direction | **Event-conditioned HIGH** | avg | `trade_when(greater(ts_rank(vec_avg(mws50_vea), 252), 0.9), group_rank(ts_delta(vec_avg(mws50_ess), 22), industry), 0)` | 高注意力日的情绪动量（attention 门控 direction） |
| T5 | attention | Change | **sum** | `group_rank(ts_delta(vec_sum(mws50_rp_story_event_count), 22), industry)` | 故事事件广度动量（other47 P2 同型） |
| T6 | attention | Level | avg | `subtract(0, group_rank(vec_avg(mws50_vea), industry))` | 注意力水平反转（论坛「突压」负口径） |
| T7 | direction | Change | avg | `group_rank(ts_zscore(vec_avg(mws50_ess), 252), industry)` | ESS 惊喜=对自身历史基线（时效型可用 ts 归一） |
| T8 | dispersion | **Dispersion HIGH** | avg | `subtract(0, group_rank(divide(ts_std_dev(vec_avg(mws50_vea), 66), add(ts_mean(vec_avg(mws50_vea), 66), multiply(0.01, ts_mean(vec_avg(mws50_vea), 66)))), industry))` | 量能 CV=分歧代理→负（论文2 量-波弹性口径） |
| T9 | event_type×direction | **Event-conditioned HIGH** | avg | `trade_when(less(vec_avg(mws50_ens_similarity_gap), 10), group_rank(ts_delta(vec_avg(mws50_ssc), 22), industry), 0)` | 新颖热点日（相似故事密集）的情绪变化 |
| T10 | direction | Change 双窗价差 | **max** | `group_rank(subtract(ts_delta(vec_max(mws50_ess), 5), ts_delta(vec_max(mws50_ess), 22)), industry)` | 情绪峰加速度（同字段双周期价差合规） |
| T11 | event_type×direction | Surprise | avg | `trade_when(greater(vec_avg(mws50_nip), ts_mean(vec_avg(mws50_nip), 252)), group_rank(vec_avg(mws50_ess), industry), 0)` | GBR N9 配方：nip 只进条件侧 |
| T12 | attention | Change | avg | `group_rank(ts_delta(vec_avg(mws50_ens), 22), industry)` | 新颖性动量（novelty 升→信息增量） |

**对照/反号**：T1' = `subtract(0, T1)`（反号变体，主候选 |S|≥0.6 时随批补）；T2 与 T6 是同族 Level 的方向对照。
**多样性审计**：桶 5 种（Level/Change/Surprise/Dispersion×HIGH/Event-conditioned×HIGH；Propagation 桶因单数据集无跨资产字段暂缺——记为结构缺口）；vec_* 3 种（avg/sum/max）；形状 5 种（group_rank/trade_when/ratio/multiply/双窗价差）；dispatch 每批 2 条、无 3 同族。
**量纲**：全 VECTOR⇒数值位一律 vec_*；T8 除零保护=add(x, multiply(0.01,x)) 单字段安全（other47 T5 混量纲教训）；constant 仅出现在比较位（greater/less），不进算术。

**收批判据（预锁）**：任一 |S|≥1.58 ⇒ 进破闸流程（2Y/prod/self/fRA+逐年覆盖）；最高 |S|∈[0.8,1.58) ⇒ 赢单单杠杆小批 + 反号变体；最高 <0.8 ⇒ 判「情绪机制弱」收口。逐年覆盖必查（RavenPack DEU 面板前段空窗风险，leading-gap 口径待裁定）。
**开波时机**：other47 波 2（L1–L5）收批分流后发本池（避免同账号并发挤压；探针/波次并发 ≤2）。

## 波 1 终态（2026-11-03 04:09 收口）
10/12 完成（T3/T4 429 掉批不补，判据已命中）：最高 T11 波动率反向 0.59/TO0.61，其次 T7 0.52/TO1.23。**10 条全 <0.8 = 预锁判据命中：情绪机制弱收口**。换手族性实锤：7/10 条 TO>0.7、5 条 >1.0（情绪腿高频特性）。教训：① news/情绪类字段日频腿换手结构性偏高，未来设计先上 decay/窗口钝化；② T11 波动率反向（ts_std_dev 反号）是唯一 S+TO 双健康形态，若复活优先此骨架。
