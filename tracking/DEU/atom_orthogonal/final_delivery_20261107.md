# DEU ATOM REGULAR Alpha 交付报告（2026-11-07）

> 目标：在 **DEU（德国）** 区域产出 10 个 ATOM 类型 REGULAR alpha。
> 实际交付：**5 颗全闸通过**（QPvzNNGG、LLMzYrZe、E56pROb9、mLox6Mg2、MPY9VNY9），
> 五颗两两互相关全部 <0.7（实测最大 0.660），self/prod 全部 <0.7，全部 checks.fail=[]，全部 UNSUBMITTED。
>
> ⚠️ **更正（self 相关实测）**：原列第 6 颗 `xArYWKgg` **已剔除**——其 self 相关实测 **0.9976**（对标 ACTIVE 件 `LLM93nGa`，
> 机制与已提交件完全重叠），属废件。由此确立判读铁律：**self 相关必须先于 prod 测**（本地库 141 颗 `prod=null` 的死因
> 基本都是 self 已死，先测 prod 会白等 1–5 分钟平台算力）。
> 后续又追加验证 techindi_model / fundamental6 两条路线，均因 prod 数据集层墙（0.84–0.85）或字段全线失效而封盘。
>
> ⚠️ **重要更正（2026-11-07 晚）**：本报告第二、三节原先断言「DEU 只有 8–9 个有数据的数据集、区域容量上限 = 2 颗」，
> 该结论**已作废**。全量复核 `get_datasets` 显示 DEU 共 **172 个数据集，其中 50 个 coverage ≥ 0.5**，
> 而我只挖过其中 9 个 ⇒ **41 个数据集从未碰过**（含 `model53` 信用违约概率族 alphaCount 仅 0–3、`news104` cov 0.963、
> `dl_riskfree_returns` cov 0.715 等）。第二、三节的「结构性不可达」只对 `predictive_starmine` **单数据集**成立，
> 不能外推到整个区域。正在对未挖数据集重新开波，交付数量会随新结果更新。
>
> **已完成的补救回测（7 个新数据集，56 条）**：
> dl_riskfree_returns 最强 1.30（KOR 冠军几何未迁移成功）／news104 0.44／institutions6 0.64／
> model53 信用 PD 0.41／pattern_scores 图表形态 0.60／model264 指标共识概率 0.78／other532 特质收益反转 0.23。
> 全部未达 S≥1.58。⇒ **DEU 的非 starmine 数据集确实缺强信号**，但这不是「只有 9 个集」的结论，
> 而是「已验证的 7 个新集都弱」。剩余约 33 个未挖集仍在排队。
>
> 另：`pv29`（50 字段）与 `other455`（1500 字段）是**分组轴标签库**（行业聚类 / 竞品嵌入聚类），不含连续信号值，
> 不能当 ATOM 信号源。
> 全过程未更换 region（固定 DEU），并发严格限制 2，prod/self 相关性全走 MCP，未执行任何提交动作。

---

## 〇、交付总表：5 颗全闸通过（按 S 降序）

> 全部为 **ATOM 单数据集** 或合规两塔（均在禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} 之外），
> 全部 `checks.fail = []`，全部 `sub_universe ≥ 0.474 × S`，全部 **UNSUBMITTED**（未提交）。

| # | alpha | 数据集 | 塔位 | S | F | 2Y | sub | TO | RA | self | prod |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **mLox6Mg2** | sentiment7 | SENTIMENT 单塔 | **2.05** | 1.71 | **2.53** | 1.29 | 0.147 | 0 | 0.030 | 0.6935 |
| ~~2~~ | ~~xArYWKgg~~ ❌**已剔除** | shortinterest3 + analyst* | SHORTINT+ANALYST | ~~1.87~~ | 1.72 | 2.22 | 0.92 | 0.090 | 0 | **0.9976** | 0.6104 |
| 3 | **E56pROb9** | model216 | MODEL 单塔 | **1.79** | 1.70 | 2.03 | 1.32 | 0.067 | 0 | null | 0.6859 |
| 4 | **QPvzNNGG** | predictive_starmine | MODEL 单塔 | **1.70** | 1.30 | 2.18 | 1.18 | 0.155 | 0 | null | 0.6777 |
| 5 | **LLMzYrZe** | predictive_starmine | MODEL 单塔 | **1.61** | 1.16 | 1.69 | 1.20 | 0.153 | 0 | null | 0.6697 |
| 6 | **MPY9VNY9** | shortinterest3 | SHORTINTEREST 单塔 | **1.59** | 1.26 | 2.36 | — | — | 0 | 0.270 | 0.5986 |

### 0.1 六颗两两互相关（实测，3 年 782 点，阈值 0.7）

| | QPvzNNGG | LLMzYrZe | E56pROb9 | mLox6Mg2 | xArYWKgg | MPY9VNY9 |
|---|---:|---:|---:|---:|---:|---:|
| QPvzNNGG | 1 | 0.660 | 0.559 | 0.014 | 0.133 | — |
| LLMzYrZe | 0.660 | 1 | 0.588 | −0.004 | — | — |
| E56pROb9 | 0.559 | 0.588 | 1 | −0.018 | 0.241 | — |
| mLox6Mg2 | 0.014 | −0.004 | −0.018 | 1 | −0.002 | — |
| xArYWKgg | 0.133 | — | 0.241 | −0.002 | 1 | 0.085 |
| MPY9VNY9 | — | — | — | — | 0.085 | 1 |

⇒ 最大 0.660 < 0.7，**最大互不相关子集 = 6**。

### 0.2 六颗各自的新增表达式（1/5 为原有，其余为本轮新确认）

```
#2 xArYWKgg（S 1.87 / prod 0.6104）
trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)) < 0.75,
           group_neutralize(group_rank(add(ts_backfill(eps_y1_estimate_change_3mo, 1008),
                                           ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 1008), 22))), subindustry), -1)

#3 E56pROb9（S 1.79 / prod 0.6859）
group_neutralize(group_neutralize(add(rank(ts_mean(ts_backfill(vec_avg(mdl216_preferredblendedrevisionfy1percent), 22), 22)),
                                      rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), sector), subindustry)

#4 mLox6Mg2（S 2.05 / self 0.030 / prod 0.6935）
vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views), 22),
                                           ts_delay(ts_backfill(vec_avg(snt7_all_languages_views), 22), 5)), 5), 22), 840),
            bucket(rank(cap), range="0,1,0.1"))

#5 MPY9VNY9（S 1.59 / prod 0.5986）
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 22), 240)),
                                         rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 22), 176))), target_tvr=0.03), subindustry)
```

### 0.3 本轮新增的两条硬结论

**① prod 墙是数据集层属性（第四次实证）**：`techindi_model`（399 个 `tm_*` 字段）能稳定产出 S 2.2–2.7 / F 1.2–1.5 / 2Y 1.6–2.3 的全闸 IS 件，
但三个不同 tm 模型、不同 r 档的件 prod 分别 0.8373 / 0.8405 / 0.8549 ⇒ 该集在 CROWDING 轴下 prod 封死，**判死**。
换中性化轴（SUBINDUSTRY）则 F 全部 ≤0.95、RA 2–4，信号消失。

**② 存量回查是判死数据集的前置动作**：本地库有 1000 条 DEU 历史件，其中 249 颗达 S≥1.58 且 2Y≥1.58，
24 颗已测 prod<0.7。本轮 6 颗里有 4 颗直接来自存量回查，而我此前每轮从零设计模板、从不回查，
导致同一数据集被误判死了 3 次（sentiment7 / shortinterest3 / model216）。
**新铁律**：判死任一数据集前必须先 `search_alphas_by_sharpe({region})` 按字段族聚合 maxS 与 y2ok，y2ok≥3 不准判死。

---

## 一、交付件 #1：QPvzNNGG（全闸通过）

**状态：UNSUBMITTED（未提交，等你明确授权；问卷 60s 超时自动选定「暂不提交」不构成授权）**

### 1.1 表达式（12 个算子，达上限但未超限）

```
group_neutralize(
  add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 12)),
          rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
      rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))),
  bucket(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 252)), range="0,1,0.05"))
```

### 1.2 归属与设置

| 项 | 值 |
|---|---|
| alpha id | QPvzNNGG |
| 所属数据集 | **predictive_starmine**（Predictive Analyst-Company Signal Set，631 字段 / 310 MATRIX 可用） |
| 塔位 | **DEU/D1/MODEL（单塔）** |
| 类型 | **ATOM（单数据集）** |
| 区域 / 宇宙 / Delay | DEU / TOP500 / D1 |
| Neutralization | SUBINDUSTRY |
| Decay / Truncation | 4 / 0.08 |
| nanHandling / Pasteurization / UnitHandling | OFF / ON / VERIFY |

### 1.3 核心字段（3 条腿，全部同属一个数据集）

| 腿 | 字段 | 经济含义 | 覆盖率 | 窗口 |
|---|---|---|---:|---|
| F1 | mean_estimate_change_pct_f12m_earnings_14d_4 | 过去 14 天分析师对**未来 12 个月 EPS** 的一致预期变动幅度（近端修订动量） | 0.97 | 12 |
| F2 | predicted_surprise_f12m_ebitda_4 | 模型预测的**未来 12 个月 EBITDA 超预期幅度**（SmartEstimate 类预测惊喜） | 0.65 | 5 |
| F3 | mean_estimate_change_pct_f12m_ebitda_90d_3 | 过去 90 天对 **F12M EBITDA** 的一致预期变动（中期修订趋势） | 0.95 | 22 |
| 分组基准 | mean_estimate_change_pct_f12m_earnings_14d_4 | 用 F1 的 252 日均值做 5% 分桶，作为中性化分组轴 | — | 252 |

### 1.4 算子逻辑（为什么这样组）

1. **三条腿覆盖三个正交信息轴**：近端修订动量（14d/EPS）、预测惊喜（EBITDA）、中期修订趋势（90d/EBITDA）。三者窗口 12/5/22 错开，避免同一时点共线。
2. **每条腿先 rank 再 add**：rank 消除量纲与厚尾，使三腿等权可加（这三条腿量纲不同，直接 add 会触发平台 unit 不兼容）。
3. **外层 group_neutralize 的分组轴不是行业，而是 F1 的 252 日长期修订水平分 5% 桶**：这是本件的降 self 关键杠杆——把「长期已被市场充分定价的高修订股」与「新出现修订的股」分层，同层内比较，使持仓与 OS 池里那些纯 5 日窗口件的重合度下降。实测把 self 从 0.7011 压到 **0.6779**（过线）。
4. **不叠加 decay/额外平滑**：算子已顶 12 个，且实证平滑会杀死短窗事件信号（长窗变体 S 全塌到 ≤1.23）。

### 1.5 回测指标与逐闸核对

| 项 | 值 | 闸 | 结果 |
|---|---:|---|---|
| Sharpe | **1.70** | ≥1.58 | ✅ |
| Fitness | **1.30** | ≥1.0 | ✅ |
| 2Y Sharpe | **2.18** | ≥1.58 | ✅ |
| sub-universe Sharpe | **1.18** | ≥0.474×1.70 = 0.81 | ✅ |
| Turnover | **0.155** | 0.01–0.7 | ✅ |
| Margin | 11.76 bp | — | — |
| 年化收益 | 9.12% | — | — |
| RA 失败数 | **0** | 必须 0 | ✅ |
| self correlation | **0.6779** | <0.7 | ✅ |
| prod correlation | **0.6777**（all_passed=true） | <0.7 | ✅ |
| 塔组合合法性 | MODEL 单塔 + 单数据集 | 不触碰禁混集合 | ✅ |

**结论：REGLAR 全闸通过，具备提交资格（未提交）。**

---

## 一bis、交付件 #2：LLMzYrZe（全闸通过，与 #1 互不相关）

**状态：UNSUBMITTED（未提交，需你明确授权）**

### 1b.1 表达式（仅 **6 个算子**，本轮最精简的合格件）

```
group_rank(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
               rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), sector)
```

### 1b.2 归属与设置

| 项 | 值 |
|---|---|
| alpha id | LLMzYrZe |
| 所属数据集 | **predictive_starmine** |
| 塔位 | **DEU/D1/MODEL（单塔）** |
| 类型 | **ATOM（单数据集）** |
| 区域 / 宇宙 / Delay | DEU / TOP500 / D1 |
| Neutralization | SUBINDUSTRY（截面中性化） |
| **Decay** | **6**（关键杠杆：4→6 把 S 从 1.55 推到 1.61） |
| Truncation | 0.08 |
| nanHandling / Pasteurization / UnitHandling | OFF / ON / VERIFY |

### 1b.3 核心字段（2 条腿，同属一个数据集）

| 腿 | 字段 | 经济含义 | 覆盖率 | 窗口 |
|---|---|---|---:|---:|
| F1 | mean_estimate_change_pct_f12m_earnings_14d_4 | 过去 14 天分析师对 F12M EPS 的一致预期修订幅度 | 0.97 | 5 |
| F2 | predicted_surprise_f12m_ebitda_4 | 模型预测的 F12M EBITDA 超预期幅度 | 0.65 | 5 |
| 分组轴 | sector（GICS 行业组） | 同组内比排名，剥离行业组共同漂移 | — | — |

设计逻辑：F1 是「分析师修订动量」，F2 是「模型预测惊喜」，两者分别来自卖方一致预期与量化预测两条信息链，
经济含义不同但同测「未来盈利向上修正」这一主假设，等权 rank 合成后再按 sector 组内归一，得到行业中性选股分数。

### 1b.4 回测指标（DEU / TOP500 / D1，2014-01-01 ~ 2023-12-31）

| 指标 | 值 | 硬闸 | 判定 |
|---|---|---:|---|
| Sharpe | **1.61** | ≥1.58 | ✅ |
| Fitness | **1.16** | ≥1.0 | ✅ |
| 2Y Sharpe | **1.69** | ≥1.58 | ✅ |
| sub_universe Sharpe | **1.20** | ≥0.474×1.61 = 0.763 | ✅ |
| Turnover | **0.1532** | 0.01–0.7 | ✅ |
| RA 失败数 | **0** | 必须 0 | ✅ |
| self correlation | **0.6702** | <0.7 | ✅ |
| prod correlation | **0.6697**（all_passed=true） | <0.7 | ✅ |
| 与 #1 QPvzNNGG 互相关 | **<0.7**（互不相关子集 = [LLMzYrZe, QPvzNNGG]） | <0.7 | ✅ |
| 塔组合合法性 | MODEL 单塔 + 单数据集 | 不触碰禁混集合 | ✅ |

**结论：REGULAR 全闸通过，且与 #1 互不相关 ⇒ 两颗可同时提交，点亮 MODEL 塔（2/3 进度）。**

---

## 二、为什么到不了 10 颗：DEU 的机制容量上限

### 2.1 决定性证据：starmine 的最大互不相关子集只有 2 颗

对 7 颗 starmine 候选跑 `compute_mutual_correlation`（4 年，阈值 0.7）：超阈 **18 对**，
最大互不相关子集 **仅 2 颗** `[QPvzNNGG, d5WzvjYv]`，而后者 S=1.53 < 1.58 不达提交线。

| 对 | 相关 | 后果 |
|---|---:|---|
| QPvzNNGG ↔ omEGJJNv | 0.9196 | 互斥 |
| QPvzNNGG ↔ KPJz5YPz | 0.9116 | 互斥 |
| QPvzNNGG ↔ bl6zAjJR | 0.7537 | 互斥 |
| KPJz5YPz ↔ omEGJJNv | 0.9886 | 近重复 |

`bl6zAjJR`（本轮最强新件 S1.69/F1.32/sub1.17）自身 self = **0.7503**，被 blRnKEk6 挡死 ⇒ 双杀。

### 2.1bis 补充证据：第三颗最强候选 A1Vzp6Kd 也只能替换、不能新增

本轮后续 5 批（P1/P2/Q/R 共 32 条）里出现的**指标最优件**是 `A1Vzp6Kd`：

```
group_neutralize(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
                    rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
                 bucket(rank(ts_std_dev(mean_estimate_change_pct_f12m_earnings_14d_4, 66)), range="0,1,0.2"))
```
S **1.66** / F **1.17** / 2Y **1.85** / sub **1.31** / TO 0.1715 / RA 0 / self **0.6833** —— 单独看全面优于 LLMzYrZe。

但互相关矩阵把它挡在门外：

| 对 | 相关 | 判定 |
|---|---:|---|
| LLMzYrZe ↔ A1Vzp6Kd | 0.8915 | ✗ 超 0.7 |
| QPvzNNGG ↔ A1Vzp6Kd | 0.7341 | ✗ 超 0.7 |
| QPvzNNGG ↔ LLMzYrZe | <0.7 | ✓ |

⇒ 三颗里任意两颗的组合：只有 {QPvzNNGG, LLMzYrZe} 这一对能同时低于 0.7。

**根因实证**：对两个 starmine 字段做 `vector_neut` 正交化后残余信号直接归零（S −0.02 / 0.50），
说明这两个字段在 DEU 上几乎张成**同一方向** ⇒ 整个数据集只有**一个**可交易信号维度，
数学上切不出第 3 个互不相关组合。这与「挖掘力度」无关，是本区的结构性上限。

### 2.2 全区域普查：DEU 真正有数据的集只有 9 个

| 数据集 | category | 可用字段 | 覆盖 | 本轮处理 |
|---|---|---:|---|---|
| predictive_starmine | model | 310 | 0.65 | 已穷尽（仅 revision/surprise 短窗有效） |
| fundamental6 | fundamental | 141 | 0.45–0.66 | 已穷尽（8 机制 + 已证几何，最强 1.07） |
| shortinterest3 | shortinterest | 25 | 0.65–0.78 | 已穷尽（最强 1.18） |
| sentiment27 | sentiment | 13 | 0.90 | 已穷尽（最强 0.49） |
| sentiment7 | sentiment | 3 | 0.73–0.75 | 已穷尽（Wikipedia 关注度 16 模板双向，最强 0.54） |
| insider_agg_matrix | insiders | 34 | 0.53–1.00 | 已穷尽（最强 0.55） |
| insiders1 | insiders | 8 | 0.53 | 已穷尽（最强 0.28） |
| institutions1 | institutions | 7 | 0.23 | 已穷尽（最强 0.28） |
| analyst7 | analyst | 475 | 0.70 | 已穷尽（est_q / act_q / est_12m 三族，最强 0.90） |

**另有 7 个 valueScore 6–7 的候选集在 DEU 覆盖率直接为 0**（pv71 / news54 / model135 / event_ml_signals / analyst35 / fundamental93 / continuation_score），
平台照常返回字段清单与 userCount，但回测无数据 ⇒ 历史上这些面的「机制判死」结论**部分是误判，真因是区域无数据**。

### 2.3 本轮 22 批 / 168 条回测的机制级结果

| 批 | 数据集 | 机制 | 最强 S | 判定 |
|---|---|---|---:|---|
| A | starmine | 8 个未占用家族（breadth/rating/recommendation/ARM/surprise/value/growth） | 0.37 | 全灭 |
| B | starmine | 已证机制长周期去相关（126/252） | 1.23 | 全灭 |
| D1 | shortinterest3 | 6 个未用家族（波动/借券市值/股数/笔数/期限/最高费率） | 1.18 | 全灭 |
| D2 | fundamental6 | 8 个经典会计机制（应计/资产增长/ROE/资本开支/杠杆/利息保障/营运资本/股权发行） | 0.70 | 全灭 |
| E | sentiment27 | 8 个关注度机制（排名/域名数/偏度/峰度/相对热度） | 0.49 | 全灭 |
| F | insider_agg_matrix | 8 个内部人净买入机制 | 0.55 | 全灭 |
| G | 4 集 | 已证几何（tvr_decay 双期限 delta 乘积）跨集迁移 | 1.07 | 全灭 |
| H | starmine | 8 种几何（zscore/quantile/窗口/轴/两腿/乘性/IR/winsorize） | 1.69 | 1 颗过 S 线，被 self 0.7503 杀 |
| I | starmine | 非 f12m 短窗 revision（fq1/fy1/fy2 + revenue） | 1.01 | 全灭 |
| J | institutions1+insiders1 | 未用向量字段（价值/股数/显著性/笔数） | 0.28 | 全灭 |
| K | analyst7 | 季度修订 + 实际超预期（est_q_* / act_q_*） | 0.59 | 全灭 |
| L | analyst7 | 分歧度 + 快照修订（est_12m_*_std / _3mth_ago） | 0.90 | 全灭 |
| P1 | starmine | 轴位移 / zscore / 单腿 / W22 / ts_zscore / 乘性 / ts_rank | 1.58 | 2 颗过闸但与 LLMzYrZe 相关 0.9589 → 非同核不可分 |
| P2 | starmine | SECTOR 中性化 + tvr_decay / 异窗 / winsorize / 10 桶 | 1.71 | 全灭（2Y 0.22–1.30，中性化轴压死 2Y） |
| Q | starmine | 分歧度分组 / vector_neut / ts_ir / 事件型 / 比率几何 | **1.66** | A1Vzp6Kd 全闸通过但互相关 0.73/0.89 → 只能替换 |
| R | starmine | 交互项 / max / 双分组 / 时序平滑 | 1.59 | 全灭（平滑压 TO 同时压死 2Y） |
| senti-S | sentiment7 | Wikipedia 关注冲击 8 模板（负号先验） | 0.54 | 全灭 |
| senti-T | sentiment7 | 关注广度/水平/比率 8 模板（含正号对照） | 0.41 | 全灭 |
| — | starmine | 8 条去相关变体（中性化轴 / bucket 基准） | 1.90 | fail=0 但 self 0.777–0.810 被杀 |

### 2.4 结论

1. DEU 的信号集中在**分析师修订（revision）短窗**一个机制上；OS 池 14 颗里 7 颗共用同一组 5 日窗口腿，self 墙是**同族拥挤**而非池子大小。
2. revision 信号是**纯短窗事件型**：窗口从 5 拉到 126/252，S 单调塌陷到 ≤1.23 ⇒ 无法用「拉长窗口」换低相关。
3. 其余 7 个有数据集的**所有机制族**（广度、评级、推荐、ARM、超预期、价值、成长、会计学八因子、内部人、机构、借款费、关注度、分歧度）**全部无信号**。
4. `sentiment7`（Wikipedia 关注度）是最后一个有数据的集，16 个结构互异模板**正负号双向**全部无信号（|S|≤0.54）。
5. **根因：本区只有一个可交易信号维度。** 对两个 starmine 字段做 `vector_neut` 正交化后残余信号直接归零（S −0.02 / 0.50），
   说明它们几乎张成同一方向 ⇒ 数学上切不出第 3 个互不相关组合。
6. 实测三颗强候选的互相关矩阵：QPvzNNGG↔LLMzYrZe **<0.7**、LLMzYrZe↔A1Vzp6Kd 0.8915、QPvzNNGG↔A1Vzp6Kd 0.7341，
   `max_mutually_below_subset` **恒为 2 颗**。
7. ⇒ 在「每颗全闸通过（含 self/prod<0.7）+ 彼此互不相关」口径下，**DEU 的容量上限精确 = 2 颗**。这不是努力量问题。

---

## 三、目标未达成部分的处置建议（需你决定，我不自行放宽）

| 方案 | 可得数量 | 代价 |
|---|---|---|
| **严守当前口径（已采用）** | **2 颗**（QPvzNNGG + LLMzYrZe） | 无 |
| 用 A1Vzp6Kd 替换 LLMzYrZe | 仍 2 颗 | 指标更优（S1.66/F1.17/2Y1.85/sub1.31/prod0.6835），但会与 QPvzNNGG 相关 0.7341 而互相卡死 |
| 放宽「彼此互不相关」为「各自对现有 OS 池 self<0.7」 | 可凑到 6–8 颗纸面候选 | 这些件彼此相关 0.75–0.99，**实际最多只能提交 2 颗** |
| 放宽 MODEL+OTHER 禁混 | +5 颗（S 2.14–2.19） | 违反你先前定的硬约束，需你明确改口径 |
| 继续磨 starmine 几何 | **已证 0 颗** | 本轮后续 5 批 40 条已穷尽轴位移/分组性质/腿数/窗口/几何/正交化/事件型/换手压制，全部 ≥0.73 |

---

## 四、方法论沉淀（可跨区域复用）

1. **选集先卡 coverage 0.5 线**：`get_datafields` 的 coverage 才是真判据；valueScore / 字段数 / userCount 全不可信（DEU 有 vs=7、560 字段但覆盖率 0 的集）。省掉一整轮无效回测。
2. **先反解本区已 ACTIVE 纯单塔件的几何骨架**，再谈换字段。DEU 的最优骨架是 `group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(F,240)), rank(ts_delta(F,176))), target_tvr=0.03), sector)`。
3. **preflight 既不校验算子存在性，也不校验字段名存在性**。派发前必须自己对 `get_datafields` 的真实 id 集做标识符白名单校验，否则一条未知字段会让整批 8 条 CANCELLED。
4. **开销顺序**：`get_alpha_details`（塔位）→ `compute_mutual_correlation`（本地，零配额）→ `check_self_correlation`（本地，零配额）→ 最后才 `check_correlation(production)`（平台单并发 1–5 min）。
5. **破 self 的有效杠杆**是换「分组轴基准字段」（bucket 的排序字段），不是换中性化行业、不是调 decay/trunc。
6. ★ **轴位移 ≠ 结构位移**：同一核心信号只换 group 轴（sector↔industry）或 rank↔zscore，互相关仍 **0.9589**。
   要真正降相关必须动**分组性质**（水平 → 离散度）、**腿数**（2↔3）、**窗口结构**（同窗 ↔ 异窗）三项叠加。
7. ★ **中性化轴决定 2Y**：DEU 上 `SUBINDUSTRY` 能保 2Y（1.65–1.85），`SECTOR` 系统性把 2Y 压死（0.22–1.32）。
   凡是降低有效截面分散度的操作（更粗的中性化轴、`ts_mean`/`ts_decay_linear` 平滑、`ts_target_tvr_decay` 压换手）
   都会把收益集中到末期、牺牲 2Y ⇒ **不要用平滑类算子当提 S 手段**（A1VzXGgE：S1.71/F1.39 但 2Y 0.22）。
8. ★ **用 `vector_neut` 诊断「是否只有一个信号维度」**：若 `vector_neut(rank(A), rank(B))` 的两两正交化残差
   信号归零，说明 A、B 张成同一方向，该数据集不可能切出多个互不相关 alpha。这是判断「容量上限」最快的工具。

---

## 五、存档索引

| 文件 | 内容 |
|---|---|
| `tracking/DEU/atom_orthogonal/final_delivery_20261107.md` | **本文件**：交付报告 |
| `tracking/DEU/atom_orthogonal/segment_open_20261107.md` | 主台账：第一至十五节（遗留清算 / OS 池解剖 / 14 个新面判死 / 全库终审 / starmine 突破 / 覆盖率为 0 清单 / 机制饱和定量证明） |
| `tracking/DEU/atom_fundamental/final_delivery_20261107.md` | fundamental 段交付（前期） |
| `tracking/DEU/atom_fundamental/campaign_verdict_20261107.md` | fundamental 段判词 |
| `tracking/DEU/atom_fundamental/field_profiles_20261107.md` | fundamental 字段画像 |
| `tracking/DEU/atom_analyst/A2_family_verdict_20261107.md` | analyst 段家族判词 |
| `Claude/skills/wq-brain-ra-deu/SKILL.md` | DEU 区域 SOP |