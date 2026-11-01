# news31（Refinitiv / RavenPack News Analytics 2.0）— KOR/D1 数据集档案

> 塔：**news**（未点亮，平台基础倍率 **1.6**，为未点亮塔最高档）
> 画像来源：`get_datafields(news31, KOR, d1, TOP600, filter_sharpe=false)` 全量 25 字段
> （`platform_count=25`, `complete=true`）+ `query_dataset_profile(KOR)`
> 建档：2026-10-30（wave 206 开波前）。§3/§4 待首波回测回填。

## 0 为什么是 news31（与已死 news 集的区分）

| 读数 | news31 | 参照 |
|---|---|---|
| 数据集覆盖 | **0.7991** | news7 .715 / news18 .61 / news21 .5266 / news46（已判死） |
| 字段数 | 25（全量已取尽） | news18 124 / news21 47 |
| **平台 alphaCount** | **105** | news21 **1282** / news18 636 / news7 300 / news46（已死） |
| 字段级 αC | **0–3（几乎无人碰）** | 典型活集字段 αC 数十起 |
| 数据类型 | VECTOR（事件/逐笔） | — |
| 塔状态 | 未点亮 0/3，倍率 1.6 | — |

**选择理由**：news 塔已死三条机制轴（情绪/标题语气 `news38/50`、注意力计数 `news7`、
内容强度 novelty/relevance `news46`），而 news31 **不是这三条轴的重复**：
它的独有资产是**报道结构与显著性元数据**（资产在正文第几句首次出现、快讯/全文标记、
同篇涉及公司数、篇幅），这正是文献里的 **news prominence / attention dilution** 轴，
本战役从未测过；且 αC=105 属本塔最不拥挤的一档。

⚠ 与 news46 同属 Refinitiv 系（`mws46_*` vs `nws31_*`），但 news46 的判死条目点名的是
**novelty / relevance** 两族；news31 本波只用结构元数据，不碰这两族、不碰情绪概率族。

## 0.1 质量先验（αC 降序 → 头部字段定性）

| 字段 | αC | userCount | cov | 定性 |
|---|---|---|---|---|
| `nws31_emeatimestamp_time` | 2 | 2 | .3717 | 时间戳（**禁作信号**） |
| `nws31_amertimestamp_time` | 3 | 3 | .3503 | 时间戳（禁） |
| `nws31_sentimentclass` | 3 | 2 | .3536 | 情绪类别 — **同已死情绪轴，不用** |
| `nws31_sentimentneutral` | 3 | 3 | .3536 | 情绪概率 — 同上，不用 |
| `nws31_urgency` | 3 | 1 | .3536 | **快讯(1)/全文(3)** — 显著性轴 ✅ |
| `nws31_companycount` | 3 | 3 | .3536 | **同篇公司数** — 注意力稀释轴 ✅ |
| `nws31_firstmentionsentence` | 2 | 1 | .3536 | **资产首次出现句位**（1=标题） — 显著性核心 ✅ |
| `nws31_wordcount` / `bodysize` | 2 / 1 | 1 | .3536 | 篇幅 — 显著性代理（备用） |
| `nws31_noveltycounts` / `volumecounts` | 3 / 0 | 1 / 0 | .3536 | 5 窗新颖度/总量 — **news46 已判死族，不用** |
| `nws31_relevance` | 1 | 1 | .3536 | 相关度 — news46 已判死族，不用 |
| `nws31_sentimentpositive/negative` | 0 / 2 | 0 / 2 | .3536 | 情绪概率 — 不用 |
| `nws31_*timestamp_time` ×6 | 0–2 | 0–2 | .35 | 时间戳（禁）；**差分=传播时延**属另一机制，本波不测 |

**头部读数**：αC 最高的一档（3）里已经同时出现 `urgency` 与 `companycount`，
说明平台上前人做过的少量尝试也落在**结构元数据**上 —— 与本波方向一致，但总量仅 105 条，
不存在「已被挖透」的证据。**αC=0 的字段**（feedtimestamp/sentencecount/sentimentpositive/
sentimentwordcount/sourcetimestamp/volumecounts）在本区**从未被用过**。

## 0.2 字段分类（以 description 为准，不按字段名）

| 族 | 字段 | 说明 / 名 vs description 差异 |
|---|---|---|
| **F1 显著性与结构** | `firstmentionsentence`, `urgency`, `wordcount`, `bodysize`, `sentencecount`, `sentimentwordcount` | description 说 `firstmentionsentence` 的 1=headline、2=第一句正文 ⇒ **越小越显著**（方向与直觉的「越大越重要」相反，必须显式记住） |
| **F2 注意力稀释** | `companycount`（同篇列出的公司数）, `subjects`（主题码数组）, `audiences`（受众码） | `companycount` 计的是 **subjects 字段里显式列出的公司数**，不是全市场覆盖数 ⇒ 纯「同篇分摊」口径 |
| **F3 新颖度/总量阶梯** | `noveltycounts`, `volumecounts`, `windows` | 5 个窗（12H/24H/3D/5D/7D）的数组；`windows` 只是标签数组 ⇒ **不是信号**。本族与 news46 重叠，**不用** |
| **F4 情绪** | `sentimentclass`, `sentimentpositive/neutral/negative` | 与已死情绪族同机制，**不用** |
| **F5 时延** | 6 个 `*timestamp_time` | 绝对时间戳 ⇒ **禁作信号**；差分（feed − source）在本区未验，本波不测 |
| **F6 关联** | `linkedidvalues`, `linkedidpositions` | 关联新闻 ID / 位置 = **连接键**，同 socialmedia39 的教训（ID 不是信号） |

**差异表（被名字误导的坑）**：`firstmentionsentence` 听上去像「首次提及的句子」= 重要性，
实际语义是**句位序号**（1=标题最显著，越大越埋没）；`urgency` 的 1 是「快讯」不是「紧急度低」；
`companycount` 不是覆盖广度而是**同篇分摊广度**。

## 0.3 画像五问 + 预处理决策

| 问 | 读数 | 决策 |
|---|---|---|
| 测什么 | 显著性元数据 / 稀释度（连续或有序小整数） | 取 `vec_avg`（事件多值时按篇均值） |
| 怎么测（量纲） | `firstmentionsentence` 1–10 量级小整数；`companycount` 1–N；`urgency` {1,3} | 必须**秩化**（`ts_rank` → `group_rank`），禁裸水平 |
| 时间维度 | 日频事件，非事件日无记录（稀疏） | 先 `ts_backfill(·,22)` 把事件日值带到后续月，再 `ts_rank(·,252)` 取年内分位 |
| 为何存在 | Refinitiv 编辑流水线产出的**报道结构标注**，非交易派生 | 非内生 → 不受价格反馈污染（好） |
| 可靠性 | 字段 cov ≈ .3536（有新闻的股票才有点）；数据集 cov .7991 | 事件稀疏 ⇒ 用 news46 已验证的壳层（`ts_backfill`+双秩），**CW 不触发已实证** |
| 更新频率 | 日内/日频 | 窗口 ≥22d；本波用 22d backfill + 252d ts_rank |
| 中心趋势 | 小正整数，右偏 | 秩化后连续，无需 delta（铁律 A 不触发：非单边恒正） |
| 单边/事件性 | **事件稀疏型** | 壳层内已含 backfill+rank；**禁裸 rank(F)** |

**壳层（机械复用 news46 已验证壳，非机制）**：
`group_rank(ts_rank(ts_backfill(vec_avg(F), 22), 252), sector)`，方向对测用 `multiply(-1, …)`。

## 1 概念块（A-3 契约）

**Concept**: 报道显著性决定信息被吸收的速度 —— 埋在正文深处的信息，价格反应慢、后续漂移长
- **Fields Used**: `nws31_firstmentionsentence`
- **Definition**: 资产在新闻中首次出现的句位（1=标题）的年内分位；分位越高 = 该股新闻越"埋没"
- **Logical Meaning**: 被定价的是**注意力分配**。散户/被动资金只读标题；同一消息若只出现在正文第 N 句，
  信息扩散慢 ⇒ 低显著度股票存在**未完全反映**。修复期数日到两周（文献：非头条反应首小时仅头条的 1/3，
  差距 2 天仍显著、15 天归零）
- **Directionality**: 无新闻方向时**方向不确定**（低显著度既可正漂移也可负漂移）⇒ **铁律 B 正反各测一条**
- **Boundary Conditions**: 无新闻股票（cov .35 之外）不参与；停牌/覆盖变更期失效；`firstmentionsentence`
  对「仅有标题的快讯」恒为 1，会造成显著性被高估
- **Expected Exposure**: sentiment
- **Implementation Example**: `group_rank(ts_rank(ts_backfill(vec_avg({firstmentionsentence}), 22), 252), sector)`

**Concept**: 同篇新闻的公司分摊 —— 一条消息挂 N 家公司，单家公司分到的注意力与定价权重被稀释
- **Fields Used**: `nws31_companycount`
- **Definition**: 新闻 subjects 字段中显式列出的公司数的年内分位
- **Logical Meaning**: 被定价的是**注意力稀释**。同篇覆盖多家公司 ⇒ 单股获得的信息强度低、
  更可能是行业/主题级消息 ⇒ 个股特异性定价不足，后续存在补定价
- **Directionality**: 方向不确定（补定价可正可负）⇒ **铁律 B 正反各测一条**
- **Boundary Conditions**: 行业级联新闻（如指数调整）会系统性抬升 companycount；小盘股更常见多公司稿
- **Expected Exposure**: sentiment
- **Implementation Example**: `group_rank(ts_rank(ts_backfill(vec_avg({companycount}), 22), 252), sector)`

## 2 双通道取证

**通道 A｜BRAIN 论坛**：2026-10-30 两次检索（`news prominence headline first sentence article length attention`；
`新闻 标题 报道位置 关注度 过度反应 反转 因子`）——**无 prominence/句位/稀释机制的专属帖**，
只命中两类无关结果：①通用 agent 工作流帖（42274443124119）；②舆情热度反转/焦点效应帖（35876513619607，
讲的是**热度水平**的反转，属已判死的注意力计数轴）。⇒ 记为 `no_result`，不作为判死依据，也不作模板来源。

**通道 B｜外部研究**：
- **"Front-Page News: The Effect of News Positioning on Financial Markets"**（新闻定位研究）：
  头条重要性新闻在 30 分钟内完成定价、长期无漂移；**非头条新闻首小时只反应约 1/3，且 2 天内差距仍显著、
  15 天归零** ⇒ 支持「低显著度 ⇒ 慢吸收 ⇒ 数日漂移」，但作者在专业终端用户样本中**未发现过度反应**
  （注意：本区为散户占比高的 KOR，结论不可照搬）。
- 投资者注意力与过度反应文献（Barber–Odean 注意力假说；Yu 2012《Investor Attention, Psychological
  Anchors, and Stock Return Predictability》JFE 104:401-419）提供「显著度 → 短期反应 → 反转」的
  一般框架，但**未给出 KOR 证据**。

**裁决**：A 无对应表达、B 有机制 ⇒ 按 A-1 自建骨架（本文件 §0.3 壳层 + §1 概念块），
B 的方向句仅作「必须双向测试」的依据，**不得据此设定单边方向**。

## 3 实测记录（wave 206 回填）

multisim `3ZG32NcOc51XbgF108nAPjBV`（batch1，2 条）；设置 SUBINDUSTRY / decay=9 / truncation=0.08。

| leg | 字段 | αid | S | 2Y | F | TO | 结论 |
|---|---|---|---|---|---|---|---|
| L1 | 句位 prominence + | `vR1n8g1w` | **-0.23** | -1.35 | -0.05 | 0.249 | ⛔ 噪声 |
| L2 | 句位 prominence − | `LLMbWJMn` | **0.01** | 1.05 | 0.00 | 0.249 | ⛔ 纯噪声（S=0.01） |
| L3 | 同篇公司数 + | `mLo2px91` | **0.28** | -0.01 | 0.07 | 0.245 | ⛔ 噪声 |
| L4 | 同篇公司数 − | `1YNVen5k` | **-0.55** | -0.33 | -0.20 | 0.245 | ⛔ 反转后仍无信号 |

batch2 = multisim `1sBYOk3nK4uqbWO1bvObYZyp`（本波 2/2 批全收，4/4 条 `|S|<0.6`，评审 `candidates=0 near=0` 全灭）。

### 3.1 ⭐ 归因（这一波真正的产出）

**读数**：两条 TO 都 **0.2486**，且 **S ≈ 0（-0.23 / +0.01）**，2Y 一正一负（-1.35 / +1.05）——
**符号在 2Y 窗口内都能翻转** ⇒ 不是弱信号，是**没有信号**。

**指纹匹配（不是事后编故事，是命中了既有规则）**：`sparse_field_long_window_v1` 明写
「③ 高频输入（日频新闻情绪）→ 长窗 ts_rank **无效**（KOR w41 实证 S 从 -0.03 掉到 -0.20）」，
并给了佐证判据「**失败组 T≈0.25**（成功配方 T 0.075–0.136）」。本波 TO=0.2486、S≈0 ⇒ **逐项命中**。

**根因**：本波直接照搬了 news46 wave 191 的壳层
`group_rank(ts_rank(ts_backfill(vec_avg(F), 22), 252), sector)`。
那个壳层当初验证的是 **CW 安全**（不是强度），而 news46 本身**已判死** ⇒
**把一个死集上只验证过 CW 的壳层当成了万能模板**（违反铁律 G「不得复用已判死结构」的引申）。

**下一波必须改的那一处（不是换字段，是换时序几何）**：
先把日频事件序列**降频聚合**（`ts_decay_linear(F,10)` 或 `ts_mean(F,5)`）再入 `group_rank`，
即放弃「252 日 ts_rank 直接吃日频」。news85 的设计已按此改（见 `news85.md` §0.3）。

**不做的三件事**（防止烧配额）：
① 不扫 ts_rank 窗口谱（0.25 的 TO 说明日频抖动是主成分，窗口调不动它）；
② 不扫 decay / truncation（TO 与 S 同时坏，不是执行层问题）；
③ 不换中性化档（raw 与 2Y 同步无信号 ⇒ 铁律 E 的「信号自身衰减」分支）。

### 3.2 数据集级结论（wave 206 收官，2026-10-30）

**四个表达式用了两个互不相同、经济含义相反的字段**（句位 prominence / 同篇公司数），
读数却是同一个模子：**TO 恒在 0.245–0.249 区间，4/4 条 |S| < 0.6**（-0.23 / +0.01 / +0.28 / -0.55）。
TO 与字段无关 ⇒ 驱动换手的是**壳层几何**（252 日 ts_rank 吃日频事件），而 S 与字段无关 **且与方向无关**（正反都死）
⇒ 这一集在本几何下**没有可提取的横截面信息**。

叠加该集自身条件：`coverage = 0.3541`（低于 KOR 0.4 换集线）、字段仅 25 个、`alphaCount` 全表偏低。
⇒ **处置：news31 停投（parked），不判死**。
不判死的理由不是还有希望，而是 `seal_dead_end` 的 forum-recon 闸要求一条**可靠的「论坛无解」记录**，
本波取证记录尚未核对通过；按 §8.11 不得用 `force_seal` 绕过（那是需要人工确认的逃生口）。
**停投 = 不再向本集派发任何配额**（与判死同等执行力度，只是账面上保留可翻案身份）。

**唯一允许的复活条件**（写死，防止未来自己重犯）：出现「先把日频聚合成低频」的**新几何**
（`ts_decay_linear(F,10)`/`ts_mean(F,5)` → 再 `group_rank`），且必须先在**已证明有信号的 news 集**上验证该几何有效，
才允许回到 news31。同几何换字段/换方向/换窗口**一律不得复活**。


## 4 十年覆盖检查（用户约束 4）— ✅ 数据够，信号没有

`LLMbWJMn` 的 `get_alpha_yearly_stats`（2014–2023）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | 294 | 305 | 309 | 308 | 333 | 325 | 323 | 338 | 322 | 322 |
| shortCount | 286 | 307 | 312 | 314 | 320 | 322 | 324 | 344 | 333 | 334 |
| Sharpe | **-0.84** | **-0.38** | 0.48 | **-0.89** | **-0.95** | 1.20 | 0.24 | **-0.52** | 0.54 | 1.57 |
| TO | .265 | .252 | .244 | .220 | .240 | .251 | .258 | .272 | .250 | .236 |

- **十年多空各 286–344 只，无整年空白** ⇒ 用户硬要求 #4 达标。
- **但 5 年为负、TO 常年 0.22–0.27** ⇒ 数据完整 ≠ 有信号；坏的是壳体时序几何，不是数据。
- ⛔ **本节结论对 `news31` 的定位**：数据可用，但本波机制未证成；若后续再用本集，
  **必须换时序几何（先聚合再排序）**，且**不得**再用 `ts_rank(·,252)` 直接吃日频。
