---
name: brain-alpha-research-news-sentiment
layer: L1
description: "新闻 / 情绪 / 社媒类数据集的研究指引：字段 5 家族分类、家族 × 6 桶配对设计、Tier A / Tier B 候选数据集的路由前核对。要在 news / sentiment / socialmedia 数据集上分类字段、设计一批表达式、判断新闻类数据集值不值得挖时使用；指引层，不是闸门，选集仍走 S0。触发词：新闻数据集 / 情绪数据集 / 5 家族 / 6 桶 / Tier A。"
last_verified: 2026-09-29
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究 — 新闻/情绪（News/Sentiment）

## 职责边界

- **本 skill 负责**：news / sentiment / socialmedia **家族专用**的研究指引——字段 5 家族分类、家族 × 6 桶的配对设计、Tier A / Tier B 候选数据集在**路由前**的核对。
- **本 skill 不做**：不覆盖非新闻数据集（→ `brain-dataset-exploration-general` / `brain-datafield-exploration-general`）；不回测；**不是闸门**——6 桶与「每批 ≥ 3 桶」在代码里**没有执行点**（旧文档提到的 `news_loop.py` 不存在），批级多样性的真闸是 toolkit 闸 6 `check_batch_diversity`；不选集（选集 = RA 步 2 / S0）。
- **上游 / 下游**：上游 = S0 已放行的新闻类数据集（或 S0 候选）；下游 = 步 3 的 `s1_semantic_<ds>`（闸 SEM 读它）→ 步 4 概念优先生成；news / sentiment 的相关性修复走 [`docs/reference/news_sentiment_playbook.md`](docs/reference/news_sentiment_playbook.md)（`brain-alpha-repair` 指向同一份）。

## 1. 路由前三查：Tier A 只是候选来源，不是默认路由

[`docs/reference/news_dataset_portfolio.md`](docs/reference/news_dataset_portfolio.md) 是 **2026-04-23 的快照**：只回答「哪些新闻集**曾经**结构上值得看」，不回答「现在该不该挖」。任何数字（Tier B 的 ~120K / ~40K / ~43K α、Tier A 门槛）以 `get_datasets(category="news"|"sentiment", region, delay, universe)` 与 S0 的 `recommend_datasets` 为准。路由前用 RA 步 2 ① 的输出逐条核对（不要绕过 S0 直接开挖）：

```powershell
& $WQ_PY tools/campaign_intel.py s0-select --region <REGION> --delay <D> --universe <U> --top-n 15
```

| 查 | 读什么 | 命中 → |
|---|---|---|
| **判死** | `s0-select` 里该集沉底，或 `hist_yield_rate = 0` 且 `hist_backtested ≥ 8`（`*_dead`） | **不路由**；不因「在 Tier A 清单里」复活 |
| **跨区弱** | `[跨区弱:REG:maxS@bt]`（同集在其它区 ≥ 16 条回测且 max\|S\| < 1.0） | 降权、排在健康集之后；本区只投**弱探针槽位**（`MINING["weak_probe_slots_max"]` = 1），不上整波 |
| **lit 塔** | `lit=Y`（该 category 当季 ACTIVE ≥ 3） | **直接剔除**（步 2 硬约束 0）；新闻字段只能在**未点亮塔**的主信号里作辅助腿（条件 / group / bucket） |

三查都过、且数据集在白名单里，才进 §2。理由写进 `s0_whitelist` 的 `entries[].reason`（例：「未判死 / 无跨区弱 / lit=N」）。**Tier A 清单是候选来源**：命中任一查就不路由，清单里其余集照常按 S0 排序。

### Tier B（平台 α ≥ 1 万：`news12` / `news18` / `socialmedia12` 等）——告知之后怎么办

必须先告知用户「该集已饱和」，然后**只有这三个分支**：

| 分支 | 何时 | 动作 |
|---|---|---|
| ① 假设优先（缺省） | 用户没有别的指示 | 转 [`brain-alpha-research-hypothesis-first`](../brain-alpha-research-hypothesis-first/SKILL.md)（RA 步 2 约束 6 的同一条路由）；不再做模板遍历 |
| ② 放弃 | 用户不想投饱和集 | 回步 2 换集 / 换区 |
| ③ 用户坚持模板遍历 | 用户明确要求 | **只许高度非对称结构**，且**先做 prod-first 探针**（步 5b，处置见决策表 D0-P）：prod ≥ 0.75 或结构性尝试失败 → 按 D0-P 判 `dead_end`，不再扩变体 |

## 2. 字段 5 家族分类

家族分类是**设计用**的（决定这一批怎么配对）；步 3 的 `s1_semantic_<ds>`（`field_semantic_classify.py`）是**闸用**的（哪些字段能当信号）。先做 S1 语义（非信号字段——标识符 / 日期 / 汇率码——先被剔除），再对剩余字段分家族；两者互补，不互相替代。

| 家族 | 含义 | 分类器关键词（字段 id 命中，优先级自上而下） |
|---|---|---|
| **peer_context**（同侪上下文） | 预聚合的同侪值 | `peer` / `sector_avg` / `industry_avg` |
| **event_type**（事件类型） | 主题代码、显著性标记、交易类型、日内 / 头版标记 | `topic` / `event` / `category_code` / `type` |
| **dispersion**（分歧度） | 标准差、方差、不确定性、分歧 | `stddev` / `std_dev` / `variance` / `dispersion` / `divergence` |
| **attention**（关注度） | relevance / 量 / 提及计数 / 新颖度 | `relevance` / `buzz` / `volume_count` / `mentions` / `attention` / `coverage_count` / `novelty` |
| **direction**（方向） | 带符号的情绪 / 语气；**也是无命中时的缺省** | `tone` / `sentiment` / `polarity` / `direction` / `score` / `rating` |

顺序：数据集覆盖（`DATASET_OVERRIDES`，**目前只有 `news12`**：`news_pct_*min` → direction、`news_vol_stddev` → dispersion）→ 字段 id 关键词 → 描述关键词 → direction 缺省。用法（`fields.json` = `get_datafields` 返回的字段列表，含 `id` / `description`；一次性中间文件，可丢弃）：

```powershell
& $WQ_PY -c "import sys,json; sys.path.insert(0,'src'); from wqb.research.news_field_classifier import classify_dataset_fields, save_taxonomy; t=classify_dataset_fields(json.load(open('cache/<ds>_fields.json',encoding='utf-8')), dataset_id='<ds>'); print(save_taxonomy('<ds>','<REGION>',t))"
```

缓存写到 `tracking/taxonomies/taxonomy_<ds>_<REGION>.json`（运行时缓存）。**没有任何流水线节点调用这个分类器**，它只是本 skill 的辅助工具，结果不会自动进 S1 台账。

**已知盲区（分类后必须人工复核）**：① 缺省 direction 会吞掉所有无关键词命中的字段——`news12` 以外几乎全靠关键词，先看哪些字段落进了缺省；② `novelty` 归 attention（关键词表如此，不是 dispersion）；③ `is_news_dataset` 只认 `category == "news"` 与前缀 `news` / `snt` / `sentiment`——`socialmedia*` / `nws*` / `twitter_*` / `creator_*` / `event_return_model` 不会被自动识别，**分类函数本身不设门**，对任意数据集都能跑，触发条件以 `get_datasets` 的 `category` 或数据集 id 前缀为准。

覆盖 < 0.4 的字段必须显式 `ts_backfill` / `group_backfill` 或直接弃用——裸用会产生 5–10 只股票集中持仓的 alpha，即使 IS 指标好看也会挂 `CONCENTRATED_WEIGHT`。这一条**有代码执行**（体检硬门检查 1），其余都是指引。

## 3. 家族 × 6 桶配对设计（指引，无代码闸）

| 桶 | 设计目标 | 优先级 | ● 强适配家族 | ◐ 可选 |
|---|---|---|---|---|
| **Level** 水平 | 字段原始水平；仅当 Labs / WebDataScope 显示水平行为**异常稳定且不拥挤**时才用 | 普通 | — | attention |
| **Change** 变化 | 近期 vs 自身历史基线的变化 / 偏离（`ts_zscore` / 短窗 vs 长窗） | 普通 | direction、attention | event_type、peer_context |
| **Surprise** 意外 | 相对**预期**的跳变（事件值 − 期望） | 普通 | direction、event_type | attention |
| **Dispersion** 分歧 | 字段的截面 / 观点分歧（stddev、disagreement） | **HIGH** | dispersion、peer_context | — |
| **Event-conditioned** 事件条件 | 只在关注度异常日交易：`trade_when(attention 异常, …)` | **HIGH** | attention、event_type | — |
| **Propagation** 传播 | 跨资产溢出 / 滞后扩散（lead-lag、跨资产相关） | **HIGH** | event_type | direction、attention、dispersion、peer_context |

- **每批设计目标**：≥ 3 个桶；≥ 1 个 HIGH 桶（Dispersion / Event-conditioned / Propagation）；含 VECTOR 字段时 ≥ 2 种 `vec_*` 聚合（`vec_avg` / `vec_max` / `vec_min` 轮换，先聚合再谈标量算子）；形状 ≥ 2 种。**每批不放 3 个同家族字段**（跨家族配对，不 3 取 1）。这些是设计目标，不是闸；形状多样性的**执行点**是闸 6。
- **配对规则**：direction × attention → Surprise / Event-conditioned（attention 把方向信号门控到异常日）；dispersion × peer_context → Dispersion；event_type × direction → Propagation / Event-conditioned；**情绪 × 非情绪**（returns / volume / volatility）的价差是另一种 motif，单数据集约束放宽时优先。**只作条件 / 分组 / 对偶价差，不把第二数据集当并列项相加**（CLAUDE.md「禁止混信号调参」；允许形态见 RA 步 7 §7.7）。
- **Event-conditioned 前提**：数据集要有事件时间戳或 attention / 异常字段；没有就退回 Surprise / Change。
- **每条主候选同时出一个反号变体**（`-rank(...)`）：原方向已被定价时常能救回信号；它降不降相关要实测（prod 相关一律 `check_correlation`），不当作降相关的既定手段。
- **窗口**：事件信号对窗口敏感（2026-04 经验，未复测）——先短窗（1 / 5 / 22）再谈长窗；仍只用标准窗口 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260，非标窗口须给证据。S0 的探针电池 P1–P8 是**探针**，不是设计模板。
- 主题与设计目标（动机，不是公式）见 [`docs/reference/news_sentiment_playbook.md`](docs/reference/news_sentiment_playbook.md)；家族 × 桶矩阵全表与 VECTOR 处理见 [`docs/reference/news_bucket_field_map.md`](docs/reference/news_bucket_field_map.md)。
- **结果归因**：每条结果在本波 `key_findings` 里带 (家族, 桶, `vec_*`)，供下一波取舍（`failure_memory` 不按新闻桶记忆，桶级教训只在笔记里）。

## 4. news12 专项（USA/D1，2026-04-21）

news12 没有语气 / 极性标量——它是新闻事件驱动的**价格反应微结构**数据集（RavenPack 风格 `news_pct_*min`、`news_max_up/dn_ret`、`news_ton_last`、`news_vol_stddev`）。不要做「情绪极性」alpha，用反应幅度 + 关注度门控。它的字段码与家族的对应（**字母 C 取代旧文的 M**，避免与下面的 motif 编号撞字母）：

| 码 | 含义 | → 家族 |
|---|---|---|
| R | 价格对新闻的反应 | direction |
| A | 关注度 / 量 | attention |
| V | 区间 / 波动上下文 | dispersion |
| C（旧称 M） | 微观结构 / 上下文（news12 没有真事件码，用 `nws12_mainz_vol_ratio` / `atrratio` 作合成触发器） | event_type |
| T | 反应持续时长 | event_type |

反应中心 motif M1–M6 → 桶：M1 / M3 → Surprise，M2 / M5 / M6 → Event-conditioned，**M4 → Surprise 或 Change**。motif 的原始定义仓库里没有，取舍按这条判据：参照的是「预期 / 事件典型值」→ Surprise；参照的是**该字段自身的历史** → Change。完整字段表见 [`docs/reference/news.md`](docs/reference/news.md)。news12 平台 α 约 12 万（2026-04 快照），属 Tier B——按 §1 的分支处理。

## 验证清单（每项写产物）

1. **路由前三查已做**：`s0_whitelist` 的 `entries[].reason` 写明该新闻集的判死 / 跨区弱 / lit 状态；Tier B 已告知用户并选定一个分支。
2. **字段已分类**：`tracking/taxonomies/taxonomy_<ds>_<REGION>.json` 存在（或对话里有家族表）；缺省 direction 的字段已人工复核；覆盖 < 0.4 的字段有 backfill 或已弃用。
3. **批设计有留痕**：本批每条表达式标 (家族, 桶, `vec_*`)；≥ 3 桶、≥ 1 HIGH、VECTOR 时 ≥ 2 种聚合、每批无 3 个同家族字段——写进本波 `key_findings`。
