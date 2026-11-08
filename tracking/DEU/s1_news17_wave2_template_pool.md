# news17 开波设计（波 2 备料）：论坛+论文取证 + 模板池（2026-11-03）

## 一、字段面（get_datafields 实拉；双簇：裸 nws17_* cov 0.65 / nws17_multiple_comp_* cov 0.93，优先用 multiple_comp 簇）

信号面：event_sentiment_score(-1..1) / acb·bee（财报情绪）/ ber（升降级）/ bam（企业行动）/ qcm·qep（语气/词典）/ ghc_lna（复合）/ nip（2h 影响）；结构面：event_similarity_days（距相似事件天数 0-365）、event_relevance/relevance(0-100)；vec_count(x)=当日事件条数。

## 二、论坛取证（search_forum_posts 2026-11-03）

| 帖 | 要点 | 启示 |
|---|---|---|
| **PW58059《从「搜索量」到「新闻密度」》78 赞/34 评** | 「近一季度新闻事件密度异常高（相对自身过去一年）→ 未来收益系统性偏低」；SVI→新闻计数的换代理量迁移 | T1 密度反转（负向）；66/252 双窗基准 |
| WL27618 relevance 加权+新颖度过滤（31 赞） | 裸 sentiment 不可靠，relevance 加权、novelty 过滤 | T7 加权；T6 相似度结构 |
| WL13229 news48 Data Idea | nws48_aes：滚动 91 日积极事件占比 | 事件占比型臂 |

## 三、论文取证（web_search 2026-11-03）

- **2026 预印本（457 万篇/17 事件标签/168 万 stock-day 事件）**：**硬数据（财报/指引/升降级）发布后数周同向延续（反应不足）；软故事（产品/人事/战略）即时跳涨后回落（过度反应）**；传闻日即完成定价 ⇒ T3 硬数据延续 / T4 软故事反转 的事件型不对称。
- SMU News co-occurrence：注意力外溢多空 68bp/月，负向预测 ⇒ 密度/共现负向先验。
- SSRN 4538670 News-based Investor Disagreement：分歧（量-波弹性）负向预测横截面收益 ⇒ T5 分类器分歧臂。

## 四、模板池（12 个结构互异 ✓，全部单数据集 news17，NEWS 单塔）

约定：X = nws17_multiple_comp_event_sentiment_score；分类器 acb/bee/ber/qep/qcm 同构代入。全波 DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc 0.08。

| # | 机制 | 表达式 | 方向先验 | 来源 |
|---|---|---|---|---|
| T1 | 密度反转 | `subtract(0, group_rank(divide(ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 66), ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 252)), subindustry))` | 密度高→负 | forum PW58059 |
| T2 | 密度×相似度（GBR 58E7jkaN 迁移） | `group_rank(multiply(ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 22), vec_avg(nws17_multiple_comp_event_similarity_days)), subindustry)` | 交互 | GBR 实证 |
| T3 | 硬数据延续 | `group_rank(ts_mean(vec_avg(nws17_multiple_comp_acb), 22), subindustry)` | 正向延续 | preprint 硬数据 |
| T4 | 软故事反转 | `subtract(0, group_rank(ts_mean(vec_avg(nws17_multiple_comp_qep), 5), subindustry))` | 反转 | preprint 软故事 |
| T5 | 分类器分歧 | `subtract(0, group_rank(ts_std_dev(vec_avg(nws17_multiple_comp_event_sentiment_score), 22), subindustry))` | 分歧高→负 | SSRN 4538670 |
| T6 | 相似度结构 | `group_rank(ts_ir(vec_avg(nws17_multiple_comp_event_similarity_days), 22), subindustry)` | 重复结构 | forum WL27618 |
| T7 | relevance 加权情绪 | `group_rank(ts_mean(multiply(vec_avg(nws17_multiple_comp_event_sentiment_score), vec_avg(nws17_multiple_comp_event_relevance)), 5), subindustry)` | 正向 | forum WL27618 |
| T8 | nip 条件侧 | `trade_when(group_rank(ts_mean(vec_avg(nws17_multiple_comp_acb), 5), subindustry), greater(vec_avg(nws17_multiple_comp_nip), 0), 0)` | 门控 | GBR news50 教训 |
| T9 | 升降级硬数据 | `group_rank(ts_mean(vec_avg(nws17_multiple_comp_ber), 22), subindustry)` | 正向延续 | preprint |
| T10 | 有新闻天数密度 | `group_rank(ts_sum(greater(vec_count(nws17_multiple_comp_event_sentiment_score), 0), 22), subindustry)` | 持续性 | 自建 |
| T11 | 密度加速度 | `group_rank(ts_delta(ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 5), 22), subindustry)` | 脉冲 | 自建 |
| T12 | 低密度干净信号 | `trade_when(group_rank(ts_mean(vec_avg(nws17_multiple_comp_ber), 5), subindustry), less(divide(ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 22), ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 252)), 1), 0)` | 条件 | 自建·PW58059 |

**合规自检**：全臂单数据集（NEWS 单塔，不触塔混）；无两条独立信号 add/subtract（T5 是同字段时序离散度、T4 单腿取反）；密度类一律有界化（比值/mean）防规模混淆；窗口 5/22/66/252 全白名单。

**派发前置**：等三波在飞（pv30/sentiment7/news104）任一收批归因后再派（并发纪律）；派发前照例双预检。

## 六、收批定案（2026-11-04 06:2x，12/12 全 COMPLETE）

| 臂 | 机制 | S | F | TO | 定性 |
|---|---|---|---|---|---|
| T3 | 财报情绪延续 acb w22 | **+0.84** | 0.46 | 0.13 | 全波最强，仍远低于 1.58 |
| T12 | ber 升降级条件 × 情绪延续 | +0.44 | 0.16 | 0.15 | 次强 |
| T11 | 密度变化 Δ w5 | +0.41 | 0.09 | 0.47 | 弱 |
| T7 | relevance 加权 | +0.39 | 0.09 | 0.51 | 弱 |
| T5 | 分类器分歧 std | +0.36 | 0.11 | 0.21 | 弱 |
| T10 | 密度事件计数 | +0.30 | 0.11 | 0.10 | 弱 |
| T4 | 软故事反转 qep | +0.18 | 0.03 | 0.38 | 弱 |
| **T9** | **升降级硬数据 ber w22（关键对照）** | **+0.02** | 0.00 | 0.13 | **死——硬数据延续假设被否定** |
| T8 | nip 条件 trade_when | −0.10 | −0.01 | 1.01 | 死（TO 爆） |
| T6 | 相似度 IR | −0.18 | −0.04 | 0.23 | 死 |
| T1 | 密度反转 | −0.20 | −0.05 | 0.09 | 死（方向反） |
| T2 | 密度×相似度 | −0.23 | −0.03 | 1.59 | 死（TO 爆） |

### 归因结论
- **「硬数据延续 vs 软故事反转」不对称假设被关键对照臂否定**：T9（ber 升降级硬数据同骨架）S 0.02 = 零信号；T3 的 0.84 来自 acb 财报情绪本身，不是「硬数据」属性。
- 条件/交互臂（T8/T12）与密度族变体（T10/T11）全部 ≤0.44，信号面整体薄。
- **全波 max|S|=0.84 < 1.58，12/12 收齐 ⇒ news17 波2 模板池判死封盘**（不再出变体）。

## 五、双预检与派发实录（2026-11-03 06:10）

- verify_expr：T8/T12 初版 trade_when 缺第 3 参（exit）FAIL，补 `, 0` 后 12/12 PASS；其余 10 臂一次过。
- preflight_expressions：12 臂全过，7 个 nws17_multiple_comp_* 字段全存在，unknown_fields 空，any_changed=false。
- 载荷 `tracking/DEU/news17_wave2_templates.json`（12 条 {type,settings,regular} 三键全）已生成。
- 06:10 派发 `news17_wave2`（pid 58308，batch-size 2 / concurrency 1），首批 T1/T2 在飞；同刻在飞仅 sentiment7_wave1r，守并发 ≤2。