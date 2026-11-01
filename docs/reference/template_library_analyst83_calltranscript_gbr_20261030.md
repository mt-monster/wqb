# analyst83（电话会议逐句文本分析）GBR 模板库 — 10 个结构互异模板

- 区域/设置：**GBR / TOP700 / D1**，`STATISTICAL` 中性化，`decay 4`，`trunc 0.08`，`maxTrade ON`，`nanHandling ON`
- 数据集：`analyst83`，345 字段**全部 VECTOR**，GBR 侧 coverage **0.3209–0.3358**
- 波次：`anl83_probe_20261030`
- 建库日期：2026-10-30
- 建库动机：GBR 侧 `analyst_*` 前缀 10 条已试（GBR maxS **1.00**，全灭）；
  `anl83_*`（214 个）+ 无前缀（115 个）共 **329 个字段名在 GBR 一次都没用过**
  （`expression LIKE '%anl83_%'` 在 region_id=7 返回 0 条）

## 0. 字段四档（先看这一节，别直接抄模板）

| 档 | 语义 | coverage | 代表字段 | 用法 |
|---|---|---|---|---|
| **A 结构/事件型** | 谁出席、说了多少、问了几轮 | 0.3209 | `anl83_ceoattendence`(0/1)、`anl83_analystattendence`(人数)、`anl83_numqapair`、`anl83_numsuppans`、`anl83_qasentratio`、`anl83_numvswordsratioceoqa`、`anl83_actinvoratioceoqa` | 计数/比率**本身无量纲**，可直接进 `ts_*`；作门控要用 `rank()` 后再与常数比 |
| **B 可读性型** | ARI/CLI/DCS/FKGL/FRE/GFI/SMOG/LIX 指数 | 0.3358 | `anl83_corppart_fkgl_qa/pres`、`anl83_ceo_smog_qa`、`anl83_cfo_smog_qa` | **只做同指数相减**（Q&A − 展示、CEO − CFO）；跨指数相减无意义 |
| **C 情绪型** | pos/neg/neu logit + sent_score + forw_sent | 0.3343 | `anl83_analyst_sent_score_qa`、`anl83_corppart_sent_score_qa`、`anl83_ceo_forw_sent_pres/qa` | 做**跨说话人**或**跨段落**的差，不要做单边水平（最拥挤：`pos_logit_qa` alphaCount=9） |
| **D 第三方参与者型** | 买方/散户/其他公司高管/其他参与者 | 0.3209–0.3358 | `buyside_*`、`retail_*`、`other_ceo_*`、`other_participant_*`、`overall_lix_*` | **alphaCount 几乎全 0，完全处女地**；先验证非零率再用 |

**为什么必须做「差」而不是「水平」**：三分类 logit 的 `pos+neg+neu ≡ 1`，单桶之间互为单调变换（见 memory
「三分类 log-prob 数据集只有 2 个自由度」）。只有**跨说话人差** / **跨段落差** / **中性桶** / **结构型量**
才是真正新的自由度。

## 1. 十个模板

> **共同水管（不是模板，是所有模板共用的必要处理）**：季度事件数据 → `ts_backfill(F, 500)` 填成日频台阶；
> 变化量用 **66（≈1 季）/ 252（≈1 年）** 这两个白名单窗口；两个窗口都符合「窗口必须有经济含义」的硬约束。

| # | 名称 | 机制（经济学假设） | 表达式骨架 | 几何 | 来源 |
|---|---|---|---|---|---|
| **T1** | Non-GAAP 强调强度 QoQ | 频繁强调 pro-forma 口径 = 在替 GAAP 数字打掩护（欺骗信号），后续跑输 | `divide(vec_avg(anl83_numnongaappres), vec_avg(anl83_numwordexepres))` → Δ66 | `group_zscore(reverse(rank(Δ)), sector)` | **论文** Larcker & Zakolyukina 2012 JAR 50(2)「Detecting Deceptive Discussions in Conference Calls」（其模型核心变量即 non-GAAP 提及） |
| **T2** | Q&A 可读性劣化（遮掩） | 被追问时语言突然变难 = 在回避；书面展示段是打磨过的，Q&A 段是即席的 | `subtract(fkgl_qa, fkgl_pres)`（同为 FKGL 年级） | `group_rank(reverse(ts_rank(backfill, 504)), subindustry)` | **论文** Hobson, Mayew & Venkatachalam 2012 JAR 50(2)「Analyzing Speech to Detect Financial Misreporting」（obfuscation）+ Li 2008 JF 可读性与盈余持续性 |
| **T3** | CEO / CFO 复杂度背离 | 两位高管语言复杂度分歧 = 内部对坏消息的掌握程度不一致 | `subtract(ceo_smog_qa, cfo_smog_qa)`（同为 SMOG） | `rank(group_neutralize(ts_av_diff(backfill, 252), subindustry))` | **论文** Hobson et al. 2012（vocal dissonance）+ Larcker & Zakolyukina 2012 |
| **T4** | 前瞻性语调缺口（脚本 vs 即席） | 展示段敢说前瞻、被追问时不敢再说 = 说了不该说的 | `subtract(ceo_forw_sent_pres, ceo_forw_sent_qa)` | `group_zscore(reverse(ts_mean(backfill, 252)), industry)` | **论文** Larcker & Zakolyukina 2012（缺前瞻陈述是欺骗最强单变量） |
| **T5** | 卖方 vs 管理层语调背离（带门控） | 卖方即席语调相对管理层脚本语调 = 外部 vs 内部信息差 | `subtract(analyst_sent_score_qa, corppart_sent_score_qa)` | `trade_when(greater(rank(analystattendence), 0.5), group_rank(ts_rank(backfill,504), sector), -1)` | **论文** Matsumoto, Pronk & Roelofsen 2011 TAR 86(4)「Q&A 段比展示段信息量更大」 |
| **T6** | 数字具体性 YoY | 数字词占比上升 = 披露变硬、可核查；下降 = 话术化 | `vec_avg(anl83_numvswordsratioceoqa)` → Δ252 | `group_rank(rank(Δ), industry)` | **论文** Li 2010 JAR（可读性/具体性与信息含量） |
| **T7** | CEO 问答段发言份额突变 | CEO 突然抢麦 = 危机公关；平时交给 CFO，出事才自己上 | `vec_avg(anl83_actinvoratioceoqa)` → Δ66 | `reverse(group_rank(rank(Δ), subindustry))` | **论文** Mayew & Venkatachalam 2012 JF 67(1)（管理者在电话会中的情绪与未来业绩）；**自建**（份额突变非水平） |
| **T8** | 卖方覆盖人数 YoY（注意力） | 覆盖人数变化 = 注意力流入/流出，注意力驱动短期需求压力 | `vec_avg(anl83_analystattendence)` → Δ252 | `group_rank(rank(Δ), sector)` | **论文** Barber & Odean 2008 RFS（注意力买入） |
| **T9** | 追问强度（补充回答/问答对） | 每个问答对被迫补答越多 = 管理层越被动；横截面分位化 | `divide(vec_avg(anl83_numsuppans), vec_avg(anl83_numqapair))` | `winsorize(quantile(backfill, driver=cauchy), std=1)` | **论文** Hollander, Pronk & Roelofsen 2010 JAR 48(3)「Does Silence Speak?」回避与沉默 |
| **T10** | 问答句数失衡（问多答少） | 问题句数 / 答案句数 高 = 回答简略、回避 | `vec_avg(anl83_qasentratio)` | `group_rank(reverse(ts_rank(backfill, 252)), sector)` | **论文** Hollander et al. 2010 JAR + Matsumoto et al. 2011（Q&A 结构） |

## 2. 十条硬约束（写表达式前逐条过）

1. **全字段 VECTOR** ⇒ 必须先 `vec_avg` 折叠。计数/存量类可考虑 `vec_sum`，但本数据集是「一场会一条记录」，
   `vec_avg` 与 `vec_sum` 在本集上语义接近，统一用 `vec_avg` 便于横向比较。
2. **单位闸 `unit_handling=VERIFY`**：计数/计数、指数/指数相除相减 OK；**禁止**给带单位字段加无量纲常数、
   禁止 `greater(<计数>, 3)` 这类带单位与常数比较 —— 门控一律 `greater(rank(x), 0.5)`。
3. **不要做跨指数相减**（ARI − SMOG 无意义）；只做同指数跨**段落**或跨**说话人**。
4. **三分类 logit 只有 2 个自由度**：`pos+neg+neu ≡ 1`，换桶不是换机制；必须做跨说话人差。
5. **窗口只用 66 / 252 / 504**（季度/年度/两年），500 只用于 `ts_backfill` 填充长度。
6. **最拥挤的字段避开**：`anl83_analyst_pos_logit_qa`（alphaCount 9）、`anl83_sent_score_qa`（7）、
   `anl83_ceo_neu_logit_qa`（5）。本波 10 个模板一个都没用它们。
7. **禁止 `add(A,B)` 混信号**；`multiply(rank(B), 0.3/0.5)` 权重混合同样违规。
   放行形态：`subtract(rank,rank)` / 同单位 `divide` / `trade_when` / `group_rank` / 同字段多尺度。
8. **不要在 `analyst83` 上引用 `cap` / `fnd6_*`** —— 那会把 ANALYST 单塔变成 ANALYST+PV 两塔组合。
9. **宁可用 `reverse` 定方向，不要靠调参翻符号**：每个模板的符号先按文献定，实测反了再一次性翻。
10. **判死前至少跑 6 个不同模板**：GBR 的失败模式是「同族换参数全灭 ≠ 机制不成立」。

## 3. 独立性自评（这 10 个是不是同一个信号换皮）

| 机制族 | 模板 | 有没有真正独立 |
|---|---|---|
| 欺骗/遮掩（可读性 + non-GAAP） | T1, T2, T3 | 三个都指向「语言复杂度异常」，**彼此可能相关 0.3–0.6**；但底料分别落在 non-GAAP 词频、FKGL 跨段落、SMOG 跨人，算三个独立加工方式 |
| 前瞻性/语调差 | T4, T5 | T4 是同一个人跨段落，T5 是跨人；一个是「不敢前瞻」，一个是「外部比内部乐观」 |
| 具体性 | T6 | 独立（数字词占比，与情绪/复杂度都不同轴） |
| 说话人结构 | T7 | 独立（发言份额，不是语言内容） |
| 注意力 | T8 | 独立（覆盖人数，纯结构量） |
| 问答动力学 | T9, T10 | T9 是补答强度，T10 是问答句数比；同一段但不同量 |

**结论**：10 个模板落在 **6 个机制族**，最大同族 3 个，可接受。

## 4. 第 1 波判读规则（先写死，防止事后合理化）

- **≥2 条 |S| ≥ 1.3 且 F ≥ 0.9** ⇒ 该机制族继续深挖，同族补 3–4 个变体
- **全部 |S| < 0.8** ⇒ `analyst83` 在 GBR 判死（与 `analyst_*` 的 maxS 1.00 合并成完整判死证据）
- **出现 |S| ≥ 1.5 但 TO > 70%** ⇒ 先扫平台 decay ∈ {6, 8, 10, 12} 再判（不要动表达式）
- **只出 T2/T3 这类可读性族** ⇒ 说明本数据集唯一有效轴是「语言复杂度」，转做跨说话人**方差**
  （`signed_power` / `ts_std_dev`）而不是均值
- **符号全反** ⇒ 整体 `reverse` 重跑一轮，不要逐条调

## 5. 已知失败记录（不要重复踩）

- GBR `analyst_*` 前缀 10 条：`group_rank(vec_avg(anl93_analyst_consistency), sector)` 及其
  `ts_backfill` / `subtract` / `trade_when` 变体 → **maxS 1.00**（这是 `analyst93` 的，
  `analyst83` 的 `analyst_*` 前缀同为 presentation 段可读性/情绪字段）
- 跨区对照：`analyst83` 在 rid 4 有 27 条 maxS **2.29** / maxF **2.67**、rid 5 有 7 条 maxS **2.64** / maxF **2.88**
  ⇒ 机制本身有强信号，GBR 侧弱；coverage 0.33 是首要嫌疑


## 6. 收批结果与判死（2026-10-30 · 6/6 全灭，已封盘）

按「先跑结构差异最大」策略，实际跑 6 个模板 / 5 个机制族，**全部落在 |S| 0.07-0.29 噪声带**：

| 模板 | alpha | S | F | TO | 2Y | SUB | margin |
|---|---|---|---|---|---|---|---|
| T1 non-GAAP 强调 QoQ | `pwdQr8Ax` | 0.29 | 0.09 | 13.02% | 0.52 | -0.03 | 1.9bp |
| T8 覆盖人数 YoY | `A1VqZkKR` | -0.18 | -0.04 | 6.35% | 0.69 | -0.07 | -1.7bp |
| T5 卖方 vs 管理层语调差+门控 | `E56oWNX9` | -0.26 | -0.07 | 5.81% | -0.01 | 0.01 | -2.7bp |
| T9 追问强度 cauchy 分位 | `A1VqZeKd` | -0.25 | -0.07 | 7.27% | 0.00 | 0.06 | -2.4bp |
| T3 CEO/CFO SMOG 背离 | `0mYn0mRK` | 0.07 | 0.01 | 7.56% | -0.56 | 0.01 | 0.6bp |
| T10 Q&A 句数比水平 | `GrWEprdO` | -0.18 | -0.04 | 6.08% | **1.64** | -0.11 | -1.6bp |

**判死依据（四条，缺一不可）**

1. **不是换手问题**：TO 全部 5.81%-13.02%，`ts_backfill(500)` 季度水管工作正常。
2. **不是覆盖率问题**：`pwdQr8Ax` 实测 `longCount 456 / shortCount 455`（TOP700 近全池）
   => coverage 0.33 被彻底排除。
3. **量级差 5.4 倍**：最佳 |S| = 0.29 = 闸（1.58）的 **18.4%**；最佳 R/TO = 0.095
   => F 上限 = 0.29 x sqrt(0.095) = **0.089** = 闸（1.00）的 **8.9%**。
4. **6 个互异骨架同时落噪声带**：涵盖披露语言强度 / 卖方注意力 / 跨主体语调 / 问答结构 /
   跨主体复杂度 / 单字段水平。若真有信号，不可能 6 个互不相干的加工方式同时 |S| < 0.30。

**唯一值得记住的近期结构**：T10 的 2Y = **1.64**（过 1.58 闸）但全期 S = -0.18
=> `anl83_qasentratio`（问答句数比）只近两年有效，被全期 `LOW_SHARPE` 锁死，不可用。

**累计判死规模**：本数据集 GBR 侧共 **16 条**全灭（本轮 6 + 前期 `analyst_*` 前缀 10，maxS 1.00）。

**规则**：`analyst83` 在 GBR/TOP700/D1 不再开波。跨区对照（rid4 maxS 2.29 / rid5 maxS 2.64）
说明电话会议语言机制在别的区有信号 —— 若要复用，去那两个区，不要回 GBR。

**方法论收获（可迁移）**：
- 「季度事件数据 -> `ts_backfill(F,500)` + 白名单窗口」这条水管是通用正确的，TO 压到 6%-13%。
- 判「字段没信号」前必须先看 `longCount/shortCount` 排除覆盖率解释（4 次 GET 换掉了错误结论）。
- 「先跑结构差异最大的模板」比按序号顺序跑更快收敛：本轮前 2 批（4 条）就基本定型，
  第 3 批只是确认。

## 7. 同源姊妹集 fundamental45 探针（2026-10-30）

`fundamental45`（GBR cov 0.2727，12 个 MATRIX 字段）同为电话会议文本集，但有两个
`analyst83` 完全没有的独立维度，故做最后一击探针（multisim `2DeNvZ8wF4uI9vnPlRXZ1GM`）：

- **F1 双 NLP 模型分歧**（LM2 vs VADER 对同一段 Q&A 的判断差）
  `group_rank(reverse(ts_rank(ts_backfill(abs(subtract(fnd45_sentiment_lm2_net_qa, fnd45_sentiment_vader_net_qa)), 500), 252)), sector)`
- **F2 跨段落 x 跨模型双重差分**（两模型对「Q&A 相对 Presentation 的语调变化」的判断分歧）
  `group_zscore(ts_delta(ts_backfill(subtract(subtract(fnd45_sentiment_lm2_net_qa, fnd45_sentiment_lm2_net_pr), subtract(fnd45_sentiment_vader_net_qa, fnd45_sentiment_vader_net_pr)), 500), 66), industry)`

两者均为 MATRIX（无需 `vec_*` 折叠），预检 `valid: true / unknown_fields: [] / any_changed: false`。
**判读规则**：两条全灭 => 「GBR 电话会议语言数据」整体判死，不再投入；
若出 |S| >= 1.0 => 说明真正的独立维度是「模型分歧」而非「语调水平」，转做该族。
