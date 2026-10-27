# other384「财报电话会披露结构」字段画像与战役档案（2026-10-21）

> 区域口径：USA / TOP3000 / Delay 1 / ATOM（全部字段来自 `other384`；分组字段 subindustry 属豁免）。
> 判死口径沿用 USA 纪律：S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB/|S|≥0.43 / TO∈[1%,70%]；先读 `rns`（<0.3 = 风格 beta）。
> 提交前必须 `check_correlation(refresh=True)` 实测 prod/self 均 <0.7，且用户明确确认。 <!-- from config.prod_corr_max -->

## 0. 选集理由（接 hiring_trends 之后）

**排期约束**：hiring_trends 的预注册上限是 2 批（3 字段无第二轴），批 2 收批即终判（见
[`_usa-hiring-trends-field-profile-20261021.md`](_usa-hiring-trends-field-profile-20261021.md) §2.6）。
若其批 2 未出全闸候选，按「无计可施才换集」的纪律转本集——**不是偏好切换**，是前集规则穷尽。

| 判据 | other384 | 为何不是别的 |
|---|---|---|
| 库内历史回测行 | **0**（`backtest_results WHERE dataset='other384'` 实测 0；`code LIKE '%oth384_%'` 亦 0） | — |
| 是否在 dead_end 名单 | **不在**（`registry_empirical` USA 42 条 dead_end 无此集） | — |
| 塔状态 | `USA/D1/OTHER` / 未点亮 | 与 hiring_trends、other359 同塔，倍率同级 |
| 字段数 | **66**（返回 61，`sharpe_filter_removed=5`）｜33 个基名 + `_fast_d1` 孪生 | 相比 hiring_trends 的 3 字段，这里**有多个独立轴**（结构 / 长度 / 情绪三组） |
| 覆盖 | **0.8197–0.8199**（远高于 0.4 阈值，无需 group_backfill） | other359 0.69–0.80；hiring_trends 0.50 |
| 拥挤度 | 结构类 **aC 0–55**；情绪类 aC 39–341（`qerfsop_aq` 341 为全集最高） | 结构轴**几乎无人使用**（`laughter` aC 0–1、`speaker_list` 0–4、`company_attendees` 1） |
| 机制独立性 | **披露质量 / 会议结构**，与价量、分析师、基本面、社媒情绪均不同源 | 交付日志 §4 第 24 条已登记该轴 |

**为什么不选 `other623`**：TextBlob 情绪轴 ⇒ 属 sentiment 家族，USA 已六次判死（`news12` / `sentiment26` / `equity_forum_data` /
`filing_sentiment` / `forum_sentiment` / `other359`），换供应商不换机制。
**为什么不选 `search_interest`**：attention 家族同上，且 `equity_forum_data` / `sentiment26` 已证纯关注度在 USA 被开采。

**本集的核心赌注**：**不碰 tone / polarity**（交付日志第 24 条明令），只挖「谁在讲、讲多长、Q&A 占多少、是否照稿念」——
这些是**披露行为**而非**披露内容**，与已判死的情绪轴正交。

**已知风险**
1. **季度事件数据**：每公司每年约 4 次更新 ⇒ 必须 `ts_backfill(...,66)`（一个季度），且窗口一律以 252（≈4 次事件）为基本单位。
2. **VECTOR 单条记录**：每次快照很可能只有 1 条 transcript ⇒ `vec_sum / vec_avg / vec_max` 三者相同（pv173 已实证过这种退化）。
   **批 1 全部用 `vec_avg`**，并在首条读数里核对；`vec_*` 聚合器的选择在本集**大概率是伪自由度**，不占探查槽。
3. **名称列表类字段**（`conference_analyst_attendees` / `speaker_list` / `event_headline_text`）可能是字符串向量，
   `vec_sum` 会报错；且**坏表达式会连坐整批 CANCELLED**（交付记忆 `cancelled-error`）⇒ 这类字段**单独发探针**，不混进 10 条批。
4. 覆盖率 0.82 但**事件期才更新**：非事件期的信号是 backfill 值，换手可能极低 ⇒ 须盯 `LOW_TURNOVER`（1%）。

## 1. 字段全表（平台 66 / 返回 61，全 VECTOR）

`get_datafields(region=USA, universe=TOP3000, delay=1, dataset_id="other384")` 实测：
`platform_count: 66, count: 61, complete: true, sharpe_filter_removed: 5, pages_fetched: 2`。
**每条基名都有一个 `_fast_d1` 孪生**（同量、另一更新频率，覆盖率 0.8199 vs 0.8198）；交付日志第 25 条：
`_fast_d1` = 同一数量的另一频率档，**一批只用一档**。本档案批 1 全用**基名档**，`_fast_d1` 留批 2 对照。

### 1.1 结构 / 出席（13）

| 字段 | 语义 | cov | uC | aC |
|---|---|---:|---:|---:|
| `oth384_oecsi` | CEO 是否在参会名单（flag） | .8198 | 48 | 89 |
| `oth384_ofcsi` | CFO 是否在参会名单（flag） | .8198 | 30 | 86 |
| `conference_analyst_attendees` | 参会分析师名单 | .8198 | 1 | **1** |
| `conference_company_attendees` | 参会公司方名单 | .8198 | 1 | **1** |
| `presentation_section_speaker_list` | presentation 段发言人与次数 | .8198 | 0 | **0** |
| `qa_section_speaker_list_fast_d1` | Q&A 段发言人与角色（**无基名孪生**） | .8199 | 2 | 2 |
| `presentation_laughter_count` | presentation 段笑声标注计数 | .8198 | 0 | **0** |
| `qa_section_laughter_count` | Q&A 段笑声标注计数 | .8198 | 1 | **1** |
| `transcript_is_initial_version_fast_d1` | 是否为供应商初版转写（**无基名孪生**） | .8199 | 1 | 1 |
| `event_full_title_fast_d1` | 会议全名（如 "Q1 2018 Apple Inc Earnings Call"） | .8199 | 0 | 0 |
| `event_headline_text_fast_d1` | 会议标题正文 | .8199 | 1 | 1 |
| `transcript_body_headline` | 从正文抽取的标题 | .8198 | 1 | 2 |
| `company_name_match_score_fast_d1` | 实体映射置信度（0–1） | .8199 | 14 | 18 |

### 1.2 长度 / 复杂度（10 基名 ×2 档）

| 字段 | 语义（平台原文摘要） | cov | uC | aC |
|---|---|---:|---:|---:|
| `oth384_presentation_count` | presentation 段**实词数**（不含标注与说话人） | .8198 | 29 | 51 |
| `oth384_presentation_wordcount` | presentation 段总词数（含标注） | .8198 | 24 | 54 |
| `oth384_presentation_sentcount` | presentation 段句数 | .8198 | 16 | 16 |
| `oth384_presentation_paragraphcount` | presentation 段段落数 | .8198 | 19 | 29 |
| `oth384_presentation_questions` | presentation 段内的提问数（照稿念通常为 0） | .8198 | 17 | 21 |
| `oth384_qa_count` | Q&A 段实词数 | .8198 | 30 | 57 |
| `oth384_qa_wordcount` | Q&A 段总词数 | .8198 | 25 | 67 |
| `oth384_qa_sentcount` | Q&A 段句数 | .8198 | 11 | 15 |
| `oth384_qa_paragraphcount` | Q&A 段段落数 | .8198 | 17 | 20 |
| `oth384_qa_questions` | Q&A 段提问总数 | .8198 | 21 | 55 |

### 1.3 情绪（10 基名 ×2 档）——**本集不挖，仅登记**

| 字段 | 语义 | cov | uC | aC |
|---|---|---:|---:|---:|
| `oth384_presentation_tone` | presentation 语气分 | .8197 | 63 | 152 |
| `oth384_presentation_posfreq` | presentation 正向词比率 | .8198 | 55 | 94 |
| `oth384_presentation_posnum` | presentation 正向例数 | .8198 | 26 | 39 |
| `oth384_presentation_negfreq` | presentation 负向词比率 | .8198 | 44 | 152 |
| `oth384_presentation_negnum` | presentation 负向例数 | .8198 | 39 | 75 |
| `oth384_qa_tone` | Q&A 语气分 | .8197 | 34 | 49 |
| `oth384_qa_posnum` | Q&A 正向例数 | .8198 | 52 | 92 |
| `oth384_qa_negnum` | Q&A 负向例数 | .8198 | 40 | 63 |
| `oth384_qerfgen_aq` | Q&A 负向词 / 实词总数 | .8198 | 25 | 54 |
| `oth384_qerfsop_aq` | Q&A 正向词 / 实词总数 | .8198 | 83 | **341** |

**结构观察**
1. **aC 梯度本身就是证据**：情绪类 39–341、长度类 15–67、结构/出席类 **0–2**。前两类在 USA 已被反复开采，
   第三类是**白空间**（`laughter` 与 `speaker_list` 全平台 0 人用过）。
2. **`_fast_d1` 与基名同覆盖率、同语义**：两档并存 ⇒ 同一机制有两次独立抽样的机会（若基名档全灭，`_fast_d1` 可作为
   第二批的唯一自由度），但**不得同批混用**（会变成同信号重复计数）。
3. **`presentation_questions` = 0 的含义要分开读**：照稿念的会是 0/缺失；有值说明 presentation 段有互动。
   这不是"质量差"，是"没照稿"。
4. **`qa_questions / qa_sentcount` 与 `qa_count / presentation_count` 是两个不同比值**：前者=每句多少提问（追问密度），
   后者=Q&A 占全场比重（话语权分配）。

## 2. 机制、壳与批 1 设计

### 2.1 机制（全部落在"披露行为"，不碰 tone）

| # | 机制 | 构造直觉 | 文献/逻辑 | 方向先验 |
|---|---|---|---|---|
| M1 | 篇幅异动 = 坏消息需要更多解释 | 本次电话会词数相对自身历史的 z 分 | 「obfuscation / 长文掩盖」：管理层在坏消息期讲得更长、更啰嗦 | **负**（越长 → 后续收益越低） |
| M2 | 高管出席变动 | CEO/CFO flag 的同比变化 | CEO 缺席财报会是异常信号（Matsumoto-Hirshleifer-Teoh 类研究：CEO 出席与信息含量正相关） | **正**（高管新出现 → 正） |
| M3 | Q&A 信息含量 | Q&A 实词/提问数的时序异动 | Q&A 是**未被脚本化**的部分，异动比总量更接近预期差 | **负**（Q&A 膨胀 = 争议/坏消息） |
| M4 | 话语权分配 | Q&A 占比、presentation 段被追问的比例 | 管理层控场强（presentation 占比高）= 叙事受控；Q&A 占比高 = 被质询 | **负**（被质询 → 负） |
| M5 | 句法复杂度 | 每句词数 | 长句 = 复杂/规避性表述（readability 文献：可读性差 → 坏消息） | **负** |
| M6 | 会中情绪氛围（行为，非词袋） | 笑声标注累计 | 笑声是**副语言**信号，与词袋 tone 不同源；aC 0 ⇒ 未被开采 | **正** |

### 2.2 通用壳与聚合纪律

```
quantile(group_rank(winsorize(ts_backfill(<SIG>, 66), std=4), subindustry))
```

- `<SIG>` 内部先 `vec_avg`（单条记录时与 `vec_sum` 等价，本集实测前不改聚合器），**再** `ts_backfill`（论坛 43031425132823 顺序纪律）。
- `ts_backfill(...,66)` = 一个季度：季度事件数据的**唯一合理补齐窗**（用 22 会把上次会议的值留到会议后三周就消失）。
- `winsorize(...,std=4)` 必须具名（preflight 对 `std` 报 `unknown_fields` 属已知误报；发批带 `validate_fields=false`）。
- `quantile(...)` 只接 1 参数（平台硬约束）；分组用豁免字段 `subindustry`，中性化用 cell 缺省 `SUBINDUSTRY`。
- **不用 `+1` 分母**：other359 / hiring_trends N9 已两次实证 `add(x,1)` + 稀疏数据 ⇒ `CONCENTRATED_WEIGHT`。
  比值一律用 `divide(a, b)`，靠 `ts_backfill` 处理缺失（缺失就不是该组的极端值）。
  例外：若分母存在真零（如 `presentation_questions=0`），改用 `subtract`/`rank` 形态而不是 `+1`。

### 2.3 批 1（10 条，预登记，发批前写死）

| # | 桶 | 机制 | 构造（SIG 部分，外层走 §2.2 壳） | 方向 |
|---:|---|---|---|---|
| A1 | Surprise | M1 | `ts_zscore(ts_delta(vec_avg(oth384_presentation_wordcount),252),504)` | 负 |
| A2 | Surprise | M1（反号对照） | `multiply(-1, ts_zscore(ts_delta(vec_avg(oth384_presentation_wordcount),252),504))` | 正 |
| A3 | Surprise | M3 | `ts_zscore(ts_delta(vec_avg(oth384_qa_count),252),504)` | 负 |
| A4 | Change | M2 | `ts_delta(vec_avg(oth384_oecsi),252)` | 正 |
| A5 | Change | M2 | `ts_delta(vec_avg(oth384_ofcsi),252)` | 正 |
| A6 | Surprise | M3 | `ts_zscore(ts_delta(vec_avg(oth384_qa_questions),252),504)` | 正 |
| A7 | Level(ratio) | M4 | `divide(vec_avg(oth384_qa_count), vec_avg(oth384_presentation_count))` | 负 |
| A8 | Level(ratio) | M4 | `divide(vec_avg(oth384_presentation_questions), vec_avg(oth384_qa_questions))` | 负 |
| A9 | Level(ratio) | M5 | `divide(vec_avg(oth384_presentation_wordcount), vec_avg(oth384_presentation_sentcount))` | 负 |
| A10 | Change | M6 | `ts_sum(vec_avg(qa_section_laughter_count),252)` | 正 |

- 桶：Surprise ×4 / Change ×3 / Level ×3 ⇒ **3 桶**，其余三桶（Dispersion / Event-conditioned / Propagation）本批不占槽：
  Dispersion 需要跨说话人分歧（本集只有整段聚合，无说话人级情绪）；Event-conditioned 用 `trade_when` 在稀疏 VECTOR 上
  **已两次产生 CW**（other359 M7、hiring N9）⇒ **本集禁用 `trade_when`**；Propagation 属跨资产，单集不可做。
- 算子覆盖：`vec_avg` / `ts_zscore` / `ts_delta` / `ts_sum` / `divide` / `multiply` / `winsorize` / `ts_backfill` / `group_rank` / `quantile`。
- **A1/A2 是显式符号对**：`quantile(group_rank(...))` 壳不保证镜像对称（hiring N1 0.80 vs N2 0.09 已证），故符号不能纸上推导。

### 2.4 预注册止损规则（**先写后测，收批后不得改**）

1. **数据集级**：10 条 `max |S| < 1.0` ⇒ 构造层失败，判弱 `USA-OTHER384-WEAK`，**不发批 2**。
2. **机制级**：同一机制 ≥2 条且 `max |S| < 1.0` ⇒ 该机制封存（M1 的 A1/A2、M2 的 A4/A5、M3 的 A3/A6、M4 的 A7/A8 各按一对判）。
3. **核心轴优先**：若 M1（篇幅异动）与 M3（Q&A 异动）**两条核心轴全部方向** `<1.0`，**不再为 M2/M4/M5/M6 补批**——
   结构与出席类先验最弱，核不动就整集封存。
4. **过闸即测 prod**：任一条 `S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 ∧ SUB/|S|≥0.43 ∧ TO∈[1%,70%]` ⇒ 立即 `check_correlation(refresh=True)`；
   prod ≥0.7 按 D0-P 看直方图，`[0.7,0.8)` n≥1 ⇒ **族级封存，不磨参数**。
5. **风格 beta 早停**：`risk_neutralized_sharpe < 0.3` ⇒ 判风格 beta，不再修 SUB/2Y。
6. **频率问题单次换窗**：全部 TO >70% 或 <1% ⇒ 只允许**一次**把 66 换到 22 或 252 重发前 5 名，仍不行则封存。
7. **批次上限**：最多 2 批（10 + ≤8）；批 2 **只许一个自由度**，且只能是下列之一：
   ① 换到 `_fast_d1` 档（同一机制的另一频率抽样）；② 中性化 SUBINDUSTRY → INDUSTRY。**不得同时改**。
8. **字符串/名称类字段单发**：`conference_*_attendees` / `*_speaker_list` / `event_*` / `transcript_*` 若要用，
   先单独发 1 条 `vec_count` 探针验证类型，**不进 10 条批**（坏表达式连坐）。
9. **`trade_when` 禁用**（稀疏 VECTOR 两次 CW 实证）。

### 2.5 取证

| 来源 | 可复用结论 | 对本批的作用 |
|---|---|---|
| 交付日志 §4 第 24 条（本仓） | `other384` 的**结构轴**（CEO/CFO 出席、Q&A 长度与问题数、presentation/Q&A 比、笑声）是独立于语气的披露质量轴 | 全批设计依据；**禁止**再挖 tone/polarity |
| 交付日志 §4 第 25 条 | `_fast_d1` = 同一数量的另一频率档，一批只用一档 | 批 1 全用基名档；批 2 单自由度可换 fast 档 |
| 论坛 43031425132823《vec 操作符解析》 | `vec_avg` 用于每记录强度；回填必须在 vec 聚合之后；存量 vs 流量是两个 alpha | §2.2 顺序；A3/A7 用 Q&A 与 presentation 分别聚合后再比值 |
| other359 §5（本仓） | `ts_zscore(level,252)` 在慢变量上会抹信号；**Δ 的 z 分用于修 SUB，时序分位用于拿 DD** | A1/A3/A6 一律 z 分 **Δ**，不对水平值做 z 分 |
| hiring_trends §4（本仓） | 稀疏数据上 `trade_when` 产生 `CW 0.496`；`+1` 分母与 CW 同源 | 规则 8/9；比值不用 `+1` |
| 平台 aC 分布（本集实测） | 结构类 aC 0–2、情绪类 39–341 ⇒ **低 aC ≠ 低 prod，但高 aC 一定高 prod**（交付日志第 13 条） | 本批全部落在低 aC 结构轴，**预期 prod 风险低于前两集**——这是本集相对 hiring_trends（aC 340）的结构性优势 |
| 论坛 43209577496983《nan 与覆盖率要按成因拆解：断粮型 vs 真缺型》 | **断粮型**（低频字段两次披露之间）用短窗 backfill 有意义；**真缺型**硬填会造假信号 | `ts_backfill(...,66)` 的正当性：季度事件 = 断粮型；且回填窗恰好一个披露周期，不跨两个季度 |
| 论坛 41974186627351《别盲目全 region 遍历》 | 财报/earnings 季度更新在 D1 下是"昨天盘后那份财报"，**事件窗口会跳变**，裸用会把财报日跳变喂成假信号 | 全批用 `ts_delta(...,252)`（≈4 次事件）而不是短窗差分；比值类先 `ts_backfill` 再 `group_rank`，避免事件日横截面错位 |
| 论坛检索（2026-10-21，query=earnings call transcript 财报电话会 披露，15 条） | **命中的全是 tone / 情绪 / 财报日期类帖子**（`fundamental45`、`earningscall_sentiment`、`earnings_sent_matrix`、财报漂移"快慢手"），**没有一条讲 CEO/CFO 出席、Q&A 结构、笑声** | 反证本集结构轴是白空间（与 aC 0–2 一致）；取证留痕：检索已完成、结论可复现 |

### 2.6 批 1 规则核算与批 2 预登记（**2026-10-21，收批后、发批 2 前写死**）

**规则核算（逐条对 §2.4 原始条款，不改条款）**

| 规则 | 判据 | 实测 | 结论 |
|---|---|---|---|
| 1 数据集级 | 10 条 max\|S\| < 1.0 | **1.30**（A5） | 不触发 ⇒ 非判弱，批 2 允许 |
| 2 机制级 | 同机制 ≥2 条且 max\|S\| < 1.0 | M1 1.11 / M2 1.30 / M3 1.29 / **M4 0.83** / M5 单条 / M6 单条 | **仅 M4 封存**（A7/A8 话语权比值）；M1/M2/M3 存活 |
| 3 核心轴优先 | M1 与 M3 全部方向 <1.0 | M1 1.11、M3 1.29 | 不触发 ⇒ 不整集封存 |
| 4 过闸即测 prod | 全闸 | 无一条 S≥1.58 | **prod 配额 0 消耗** |
| 5 风格 beta 早停 | rns < 0.3 | **A7 0.18 / A8 0.21 / A10 0.03** | 三条判风格 beta，不再修 SUB/2Y |
| 6 频率换窗 | 全部 TO >70% 或 <1% | TO 2.54%–5.36% | 不触发（T 全在带内） |
| 7 批次上限 | 10 + ≤8，批 2 单自由度 | — | 批 2 允许，**取 ② `_fast_d1` 档**（不取 INDUSTRY：hiring §4 已证 INDUSTRY 用 2Y −0.15 换 S +0.02，本集 2Y 本就短 0.26–0.94，不能再削） |
| 8 字符串字段单发 | 未使用 | ✅ | — |
| 9 `trade_when` 禁用 | 未使用 | ✅ | — |

**批 2（5 条，全部 `_fast_d1` 档，表达式逐字预登记）**

| # | 机制 | 构造（SIG 部分，外层同 §2.2 壳） | 批 1 对照 | 方向 |
|---:|---|---|---|---|
| B1 | M1 | `multiply(-1, ts_zscore(ts_delta(vec_avg(oth384_presentation_wordcount_fast_d1),252),504))` | A1（S 1.11 / rns 0.82） | 正 |
| B2 | M2 | `ts_delta(vec_avg(oth384_oecsi_fast_d1),252)` | A4（1.24 / 0.86） | 正 |
| B3 | M2 | `ts_delta(vec_avg(oth384_ofcsi_fast_d1),252)` | A5（1.30 / 0.93） | 正 |
| B4 | M3 | `ts_zscore(ts_delta(vec_avg(oth384_qa_questions_fast_d1),252),504)` | A6（1.29 / 0.87） | 正 |
| B5 | M5 | `multiply(-1, divide(vec_avg(oth384_presentation_wordcount_fast_d1), vec_avg(oth384_presentation_sentcount_fast_d1)))` | A9（1.27 / 0.68） | 正 |

不选 A2（0.95）与 A3（0.91）：同机制里较弱的一支，且 SUB/|S| 0.19 / 0.30 已破 0.43。不选 A7/A8/A10：规则 5 已封。

**批 2 终局预登记**：收批后若仍无 `S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 ∧ SUB/|S|≥0.43` 候选 ⇒ 判弱 `USA-OTHER384-WEAK`：
披露行为轴的**幅度天花板**就是 S≈1.30 / returns≈3.9%（F 公式 `F = S·√(ret/0.125)` 在 TO<12.5% 时封顶 0.72），
距过闸需同时 +22% S 与 +29% returns，单自由度设置轴不可能提供该幅度 ⇒ 不磨参数、转下一集。

## 3. 回测结果

### 3.1 批 1（multisim `3Mc85uglR55i92G9vWMMB82`，10/10 COMPLETE，2026-10-21 05:44Z 发批）

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / VERIFY / NaN ON / pasteurization ON / maxTrade OFF；
平台窗 2014-01-01 → 2023-12-31。`S` 为平台 sharpe，`SUB/|S|` 按 `sub_universe_sharpe / |S|` 手算。

| # | alpha | 机制 | S | F | TO | 2Y | SUB | SUB/\|S\| | rns | DD | returns | 闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A1 | `MP0aZPoo` | M1（−1·z(Δ252)） | **1.11** | 0.60 | 3.76% | 0.84 | 0.71 | 0.64 | **0.82** | 4.43% | 3.61% | 3 红 |
| A2 | `ZYmbMYG3` | M1（+z(Δ252)） | 0.95 | 0.47 | 3.77% | 0.65 | 0.18 | 0.19 | 0.40 | 7.14% | 3.03% | 4 红 |
| A3 | `2rjwWrd5` | M3（−1·z(Δ252 qa_count)） | 0.91 | 0.44 | 3.78% | 0.71 | 0.27 | 0.30 | 0.48 | 6.57% | 2.95% | 4 红 |
| A4 | `88vjY8qq` | M2（Δ252 oecsi） | 1.24 | 0.67 | 3.83% | 0.64 | 0.85 | 0.69 | **0.86** | 3.18% | 3.68% | 3 红 |
| A5 | `2rjwWrk5` | M2（Δ252 ofcsi） | **1.30** | **0.72** | 3.83% | 0.81 | **0.91** | **0.70** | **0.93** | **2.88%** | **3.88%** | 3 红 |
| A6 | `LL5NrLee` | M3（z(Δ252 qa_questions)） | 1.29 | 0.74 | 3.78% | 0.74 | 0.76 | 0.59 | **0.87** | 3.72% | 4.11% | 3 红 |
| A7 | `YPxbJPZl` | M4（−1·qa/pres count） | 0.70 | 0.29 | 5.36% | 0.36 | −0.01 | −0.01 | 0.18 | 5.30% | 2.14% | 4 红 |
| A8 | `omoLrmQ5` | M4（−1·pres_q/qa_q） | 0.83 | 0.35 | 5.24% | 0.56 | −0.13 | −0.16 | 0.21 | 4.71% | 2.25% | 4 红 |
| A9 | `58jze8Nz` | M5（−1·word/sent） | 1.27 | 0.70 | 4.92% | **1.32** | 0.71 | 0.56 | 0.68 | 4.11% | 3.75% | 3 红 |
| A10 | `bl8bnl7m` | M6（ts_sum laughter 252） | 0.06 | 0.02 | 2.54% | −0.91 | −0.16 | −2.67 | 0.03 | **55.62%** | 1.10% | 5 红（含 **CW 0.469@2020-08-18**） |

- **全批零完整过闸，零 prod 配额消耗**；无一条触发 `CONCENTRATED_WEIGHT`，除 A10。
- `CLUSTER_TEST` 全部 WARN 但 <1.58（A5 0.99、A6 1.22、A9 1.25 最接近线）⇒ 簇内无强共动。
- 金字塔：全部 `USA/D1/OTHER`，multiplier **×1.4**（未点亮塔）。

### 3.2 批 2（multisim `WA69e9ZJ4ixcncNzFfdbd4`，5/5 COMPLETE，2026-10-21 05:48Z 发批）

单自由度 = **`_fast_d1` 档**（§2.6 预登记 ②），设置与批 1 完全一致，表达式逐字同 §2.6。

| # | alpha | 对照 | S | F | TO | 2Y | SUB | SUB/\|S\| | rns | DD | returns |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B1 | `kqJoOV8d` | A1 | 1.10 | 0.59 | 3.69% | 0.79 | 0.60 | 0.55 | 0.72 | 4.63% | 3.59% |
| B2 | `RRAbKV51` | A4 | 1.05 | 0.53 | 3.76% | 0.65 | 0.58 | 0.55 | 0.49 | 4.76% | 3.22% |
| B3 | `e76bv91M` | A5 | 1.23 | 0.67 | 3.76% | 0.88 | 0.71 | 0.58 | 0.77 | 3.97% | 3.74% |
| B4 | `78oNMZ3Q` | A6 | 1.18 | 0.65 | 3.72% | 0.68 | 0.62 | 0.53 | 0.69 | 4.94% | 3.84% |
| B5 | `omoLr6RE` | A9 | 1.24 | 0.67 | 4.94% | **1.31** | 0.66 | 0.53 | 0.61 | 4.17% | 3.69% |

**批 2 结论：`_fast_d1` 档在 5/5 条上全面不优于基名档**——S −0.01 ~ **−0.19**（B2 最惨），F −0.01 ~ −0.05，
rns −0.10 ~ −0.03（唯 B3 仍 0.77），SUB 全线下滑（0.60–0.71 vs 0.71–0.91）。**不是抽样噪声**：同一批设置、同一壳、同一机制，
只有频率档变了，5 条同向变差 ⇒ 该档与基名档承载同一数值（覆盖 0.8198 vs 0.8199 无差异），
差别只在**披露时点更早**，而更早的时点**拿不到**电话会后的漂移（基名档的"晚一拍"恰好对齐市场消化窗口）。

## 4. 归因

### 4.1 批 1：两个簇，界限是 `rns`

| 簇 | 成员 | rns 区间 | S 区间 | DD 区间 | 判读 |
|---|---|---|---|---|---|
| **真信号簇** | A5 / A6 / A4 / A1 / A9 | **0.68–0.93** | 1.11–1.30 | **2.88–4.43%** | 风险中性化后 Sharpe 几乎不掉 ⇒ **不是风格 beta**，是独立的披露行为 alpha |
| 风格 beta 簇 | A7 / A8 / A10（+ 边缘 A2 0.40 / A3 0.48） | 0.03–0.21 | 0.06–0.83 | 4.71–55.62% | 比值与笑声在风险中性化后塌掉 ⇒ 承载的是行业/规模风格 |

**机制逐条**

| 机制 | 最强读数 | 归因（为什么是这个方向） |
|---|---|---|
| **M2 高管出席** | **A5 ofcsi S 1.30 / rns 0.93 / DD 2.88%**（A4 oecsi 1.24 / 0.86） | CFO 出席状态的同比变化**几乎全部是特质信息**（rns≈S）。CFO 由缺席转出席 = 财务信息可核验性上升，随后收益更高。这是本数据集**最好的轴**：DD 全批最低、returns 全批最高、rns 全批最高 |
| **M1 篇幅异动** | A1（−1·z）1.11 / rns 0.82 vs A2（+z）0.95 / rns 0.40 / DD 7.14% | 「比自身历史讲得更长 → 未来收益更低」成立；反号版本 rns 减半、DD 增 2.7pp ⇒ **符号不是纸面可推的**（第 5 次复现壳的不对称性：hiring N1/N2、other359） |
| **M3 Q&A 信息含量** | A6 `qa_questions` z **1.29 / rns 0.87** vs A3 `qa_count` −1·z 0.91 / rns 0.48 | **「问题条数」与「回答字数」方向相反**：提问数上升 = 分析师追问多、信息产出多 ⇒ 正收益；回答字数上升 = 冗长 ⇒ 负收益。同机制里选对**度量**比选对符号重要 |
| **M4 话语权分配** | A7 0.70 / A8 0.83，rns 0.18 / 0.21 | Q&A 占比是**行业惯例**（科技/医药 Q&A 天然更长）⇒ 中性化后塌掉。机制封存 |
| **M5 句法复杂度** | A9 word/sent **1.27 / 2Y 1.32 / rns 0.68** | 全批**唯一 2Y>1.2** 的构造：长句 = 规避性表述，且该效应在近两年增强。是 2Y 短板的最优来源 |
| **M6 笑声** | A10 S 0.06 / DD **55.62%** / CW **0.469 @2020-08-18** | 稀疏计数 + `ts_sum(…,252)` ⇒ 极少数公司常驻极端分位。**第三次**复现「稀疏 VECTOR + 累计算子 = CW」（other359 M7、hiring N9、本批 A10） |

**为什么 10 条一条都不过闸——是幅度，不是构造**

1. **TO 全部 2.5–5.4%**，落在 `F` 公式的封顶区：`F = S·√(returns/0.125)`。
   A5 手算 `1.30·√(0.0388/0.125) = 0.724` vs 平台 0.72 ✅（本会话第三次独立复核该公式）。
   ⇒ **decay / backfill / winsor / 平滑一律不动 F**，只有 S 或 returns 能动。
2. 要过闸（S 1.58 / F 1.0）需 **returns ≥ 0.125·(1/1.58)² = 5.0%**；本批最高 3.88%。缺口 = **+22% S 且 +29% returns**。
3. 真信号簇的 `SUB/|S|` = 0.56–0.70（线 0.43）✅、DD 2.9–4.4% ✅、`CLUSTER_TEST` 峰值 1.25（线 1.58）✅
   —— **质量项全过，只有幅度不够**。这与 hiring_trends「过闸线 2/3 处封顶」同形，但本集 rns 更高（0.93 vs 0.83）、TO 更低（3.8% vs 5–15%）。

**A10 的教训（写入交付日志）**：`ts_sum(vec_avg(稀疏计数),252)` 在 `quantile(group_rank(...))` 里
不是"平滑"，是把「一年内有过几次笑声」压成少数几档离散值 ⇒ 持仓塌到少数股票。稀疏计数类**禁止**用累计算子，
只能用 `ts_zscore(Δ)` 或比值，且必须逐条看 `long_count/short_count`（A10 是 1037/1969，看似正常，DD 却 55.6%——说明 CW 来自**权重**不是数量）。

## 5. 决策

**判弱 `USA-OTHER384-WEAK`（2026-10-21，两批 15 条，预注册规则全部执行完毕）**

**终局核算（规则逐条，条款未改）**

| 规则 | 终局读数 | 处置 |
|---|---|---|
| 1 数据集级 | 批 1 max\|S\| 1.30、批 2 1.24 ⇒ 均 ≥1.0 | 构造层**不**判失败（判弱理由不是"没信号"，见下） |
| 2 机制级 | M4 0.83 封存；M1/M2/M3/M5 全 ≥1.05 | 机制轴未死 |
| 3 核心轴优先 | M1 1.11 / M3 1.29 | 不触发整集封存条款 |
| 4 过闸即测 prod | **0 条全闸** | prod 配额 **0 消耗**（两批共 0 次 `check_correlation`） |
| 5 风格 beta | A7/A8/A10 rns 0.18/0.21/0.03 | 三条封存 |
| 6 频率换窗 | TO 2.5–5.4%，全在带内 | 不触发 |
| 7 批次上限 | 10 + 5，单自由度 = `_fast_d1` | **已到顶**；5/5 条该档更差 ⇒ 频率轴解完 |
| 8 / 9 | 均未使用 | — |

**为什么在"有真信号"的前提下仍判弱**

1. **幅度天花板**：两批 15 条的 S 分布 = 0.06–**1.30**，2Y = −0.91–**1.32**，且最优点恰好落在
   `S≈1.30 / returns≈3.9% / TO≈3.8%`。按 `F = S·√(ret/0.125)`，此时 `F` 封顶 **0.72**。
2. **过闸需要的幅度**：S 1.58 ∧ F 1.0 ⇒ returns ≥ **5.0%**。缺口 = **+22% S 且 +29% returns**，
   这不是设置层的量级（本会话两次实测：`_fast_d1` 换档让 S **−0.19 ~ −0.01**；hiring 的 SUBINDUSTRY→INDUSTRY 只给 S **+0.02**）。
3. **轴已穷尽**：6 个机制 × 2 个频率档 = 15 条；比值类（M4）与累加类（M6）已判风格 beta/CW；
   M2（出席）作为本集最强轴已用满（CEO 与 CFO 各一条 + `_fast_d1` 各一条）。
   剩下能动的只有 decay / 回填窗 / winsor 档 —— **参数打磨，规则 7 之后禁止**。
4. **质量项反而证明不是构造问题**：真信号簇 rns 0.68–**0.93**、DD 2.88–4.43%、`SUB/|S|` 0.53–0.70、`CLUSTER_TEST` ≤1.28，
   全部在平台线内。**是"信号太弱"而不是"信号不纯"**。

**不写 DB `dead_end`**：`seal_dead_end` 的论坛取证闸是 fail-closed，本集无 `forum_recon` 记录；
绕过需 `force_seal=True` / `require_forum_recon=False`（需用户确认），本轮不绕。判弱结论记在本文件与交付日志。

**三条可复用结论（已写入交付日志 §4）**

| # | 结论 | 证据 |
|---|---|---|
| ① | **`_fast_d1` 档是同一数值的"更早时点"，不是新信号轴**：5/5 条全面更差，S 最多 −0.19、SUB 全线下滑 | 本批 B1–B5 vs A1/A4/A5/A6/A9 |
| ② | **同一机制里"度量"比"符号"重要**：`qa_questions` z 1.29/rns 0.87，而 `qa_count` −1·z 0.91/rns 0.48；提问数=信息产出（正），回答字数=冗长（负） | A6 vs A3 |
| ③ | **披露行为轴的幅度上限 ≈ S 1.3**：6 机制 × 2 频率档全扫，天花板不动；要过 1.58 必须换到"幅度型"数据集，不能靠设置 | 本文件 §3/§4 |

**下一集**：`other623`（TextBlob 情绪族，已在本集选题时排除——六次判死）与 `search_interest`（关注度族）都不选；
转 **`option` 类零历史集**（cells 表：option 25 回测 / 0 RA 全过 / 4 判死，是新面）——按同样的三查（0 历史、非 dead_end、未点亮塔）重选。
