# GBR D0 `news48`（Global Media News）模板库与实测账本

> 战场：GBR / TOP700 / **Delay 0**（D0 塔位全未点亮，news 倍率 1.9）
> 数据集画像：22 字段全 VECTOR / coverage **0.7389** / alphaCount **4** / valueScore **6**
> 建立日期：2026-10-31
> 关联：`template_library_gbr_d0_analyst44.md`（同区 D0 首战，已判死）
> 硬约束提醒：**D0 提交门槛 = S 2.69 / F 1.5 / 2Y 2.69**（S 门槛是 D1 的 1.70 倍）

---

## §1 字段结构（22 字段 / 五族）

数据集级 description 不可信是本项目的已知坑，下表**全部来自 `get_datafields` 的字段级 description**。

### §1.1 情绪分族（0–100，越高越正面）

| 字段 id | 语义 | alphaCount |
|---|---|---:|
| `nws48_ess` | **Event Sentiment Score** — 故事中该实体的新闻情绪分 | 0 |
| `nws48_ssc` | 故事整体情绪分（Story Sentiment） | 1 |
| `nws48_qcm` | 多分类器综合情绪分（面向故事中最相关公司） | 0 |
| `nws48_qep` | 全球股票新闻情绪分，专做正/负识别 | 0 |
| `nws48_qmb` | 社论 / 评论类文章对股市的情绪分 | 0 |

### §1.2 事件情绪分族（按事件类型切分）

| 字段 id | 语义 | alphaCount |
|---|---|---:|
| `nws48_acb` | 公司行动公告（corporate action）情绪分 | 0 |
| `nws48_bam` | 创投 / 公司事件 / 并购 / 收购 / 要约 情绪分 | 0 |
| `nws48_bee` | 财报**评估**（earnings evaluations）情绪分 | 0 |
| `nws48_ber` | 财报**发布公告**（earnings release）情绪分 | 0 |
| `nws48_ghc_lna` | **分析师评级变化**数值分 | 0 |

### §1.3 新颖度族（RavenPack 特色，本数据集的差异化维度）

| 字段 id | 语义 | alphaCount |
|---|---|---:|
| `nws48_ens` | **Event Novelty Score**（0–100），24h 窗口内故事有多"新" | 0 |
| `nws48_g_ens` | 全局版新颖度分（跨 provider） | 0 |
| `nws48_ens_elapsed` | 事件链首条 → 当前条的**毫秒**间隔 | 0 |
| `nws48_g_ens_elapsed` | 全局版毫秒间隔 | 0 |
| `nws48_ens_similarity_gap` | 距上次相似故事的**天数**（信息陈旧度） | 0 |
| `nws48_g_ens_similarity_gap` | 全局版天数间隔 | 0 |

### §1.4 聚合比 / 计数族（91 日滚动窗口，慢变量）

| 字段 id | 语义 | alphaCount |
|---|---|---:|
| `nws48_aes` | 91 日窗口内**正面事件 / 非中性事件**比例（0–100） | 0 |
| `nws48_vea` | 91 日窗口内**非中性事件计数** | 0 |

### §1.5 冲击 / 元数据族

| 字段 id | 语义 | alphaCount |
|---|---|---:|
| `nws48_nip` | **News Impact Projection** — 未来 2 小时预计市场冲击分（0–100） | 2 |
| `nws48_relevance` | 实体与故事的关联强度（0–100） | 0 |
| `nws48_rp_story_event_count` | 每条故事涉及的实体数 | 1 |
| `nws48_rp_story_event_index` | 实体在故事中的序号位置 | 0 |

### §1.6 拥挤度判读

22 个字段里 **18 个 alphaCount = 0**（完全没人挖过），最高仅 2。全数据集 alphaCount 合计 4。
⇒ **这是 GBR D0 里最"干净"的高覆盖数据集之一**（对比 `analyst44` alphaCount 121、`news18` 33）。
⇒ 但 alphaCount 0 是双刃：可能是矿，也可能是"没人挖得出"。**本批探测就是回答这个问题。**

### §1.7 D0 相对 D1 的信息优势（为什么值得在 D0 上做新闻）

新闻是本区唯一有真正 D0 信息优势的数据类别 —— D1 新闻已经过一夜定价，D0 是在同一交易日内的原始流。
`nws48_nip`（未来 2 小时冲击）这一字段在 D1 语境下几乎没有意义，只有 D0 才能兑现。
**这与 `analyst44` 的失败形成对照**：基本面修正在 D1 下信息损失很小（修正本来就是慢变量），
所以 D0 对基本面只是"更早看到同一个数"；而对新闻，"更早"就是 alpha 本身。

---

## §2 12 个结构互异模板库

**多样性说明**：差异落在 **水平 / 一阶差分 / 质量权重 / 条件门控 / 跨源结构差 / 二阶冲击 /
计数差分 / 慢变量水平 / 双均线趋势 / 陈旧度 / 跨源确认 / 事件类型价差** 共 12 个互不相同的结构轴上，
不是"同一骨架换窗口"。

### §2.1 合规声明

- **无 `add(A,B)` 混信号调参**：所有双信号结构均为 `subtract(rank, rank)` 形式（同尺度相减，用于定义价差而非加权求和）。
- **权重恒为 1**：不需要 `multiply(x, 0.3)` 这类扫描式权重；`multiply(A, B)` 仅用于两个**同量纲 0–100 分数**的点乘（质量加权），非混信号。
- **窗口全部落在白名单** `1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260`。
- **VECTOR 全部经 `vec_avg` 折叠**成标量后使用（本数据集无计数型字段需要 `vec_sum`；`nws48_vea` 本身已是计数标量语义）。
- **门控一律 `greater(rank(x), 常数)`**，避免带单位字段与无量纲常数比较。

### §2.2 模板清单

| # | 名称 | 表达式 | 机制（一句话） | 结构轴 | 来源 |
|---|---|---|---|---|---|
| **T1** | 情绪水平项 | `rank(ts_mean(vec_avg(nws48_ess), 22))` | 22 日平均语调 = 中期情绪，正面语调→资金流入 | 水平项 | 自建 + forum `43179860065303`（sentiment 塔） |
| **T2** | 情绪意外 | `rank(ts_delta(ts_mean(vec_avg(nws48_ess), 22), 22))` | 语调相对自身 22 日前的改变 = 新信息，比水平更接近 alpha | 一阶差分 | paper Tetlock 2007（"Giving Content to Investor Sentiment"） |
| **T3** | 相关性加权情绪 | `rank(ts_sum(multiply(vec_avg(nws48_ess), vec_avg(nws48_relevance)), 22))` | 只有真关于该公司的新闻才计价；按 relevance 折价"提及型噪声" | 质量权重 | 自建（RavenPack 语义）+ forum `41420742165527`（`vec_avg` 稀疏被单值主导） |
| **T4** | 新颖度门控情绪 | `trade_when(greater(rank(ts_mean(vec_avg(nws48_ens), 22)), 0.7), rank(ts_mean(vec_avg(nws48_ess), 22)), -1)` | 只在新闻"新"时交易语调；重复故事已被定价 | 条件门控 | forum `33120494662423`（`trade_when` 三参数语义，`-1` = 不平仓） |
| **T5** | 跨分类器分歧度 | `rank(subtract(vec_avg(nws48_qcm), vec_avg(nws48_ssc)))` | 两个独立分类器对同一故事的情绪分歧 = 信息模糊度，模糊度折价 | 跨源结构差 | paper Diether-Malloy-Scherbina 2002（分析师分歧度）→ 新闻域移植 |
| **T6** | 冲击加权情绪 | `rank(ts_sum(multiply(vec_avg(nws48_ess), vec_avg(nws48_nip)), 66))` | 预期冲击 × 语调方向 = 可交易新闻 alpha；低冲击新闻无论语调都不该重仓 | 二阶冲击 | 自建（RavenPack NIP 语义） |
| **T7** | 事件计数加速 | `rank(ts_delta(vec_avg(nws48_vea), 22))` | 非中性事件数的增量 = 关注度冲击，注意力驱动净买入 | 计数差分 | paper Barber-Odean 2008 + Merton 1987（investor recognition） |
| **T8** | 正面事件占比 | `rank(vec_avg(nws48_aes))` | 91 日窗口正面事件占比 = 中期事件气候（慢变量、低换手） | 慢变量水平 | 自建 |
| **T9** | 双均线语调差 | `rank(subtract(ts_mean(vec_avg(nws48_ess), 5), ts_mean(vec_avg(nws48_ess), 66)))` | 短均线高于长均线 = 语调正在改善 | 双均线趋势 | 自建 / Brock-Lakonishok-LeBaron 1992（MA 规则）移植 |
| **T10** | 相似故事间隔 | `rank(ts_mean(vec_avg(nws48_ens_similarity_gap), 66))` | 距上次相似故事天数越长 = 信息越新；间隔短说明故事在重复、已被定价 | 陈旧度 | 自建（event novelty 语义） |
| **T11** | 跨源确认 | `rank(ts_mean(vec_avg(nws48_ghc_lna), 22))` | 分析师评级变化被新闻流捕获 = 第二信源确认 | 跨源确认 | paper Womack 1996 / Barber-Lehavy-Trueman-Womack 2001 |
| **T12** | 事件类型价差 | `rank(subtract(ts_mean(vec_avg(nws48_ber), 22), ts_mean(vec_avg(nws48_bam), 22)))` | 财报发布语调 vs 并购语调 —— 两条独立信息通道，价差隔离"基本面 vs 交易事件" | 事件类型价差 | 自建 |

### §2.3 起始设置

沿用 `analyst44` 的 D0 档案（这是本区唯一实测跑通的 D0 设置）：

```
region=GBR  universe=TOP700  delay=0
neutralization=INDUSTRY  decay=10  truncation=0.08
nan_handling=ON  max_trade=OFF  pasteurization=ON  unit_handling=VERIFY
```

**为什么 decay 用 10**：新闻流稀疏 → 有新闻的日子信号跳变 → 天然高换手。
`analyst44` 实测「`ts_mean(66)` + decay 10」把 TO 从 150.5% 压到 4.46%、CW 从 0.50 转 pass、margin 从 1.40bp 升到 16.13bp。
按项目已沉淀的结论「**平台 decay 是换手治理的正确层**」，先动平台 decay，不动表达式内平滑。

---

## §3 实测账本

### §3.0 D0 门槛对照（不可遗忘）

| 检查 | D0 limit | D1 limit |
|---|---:|---:|
| `LOW_SHARPE` | **2.69** | 1.58 |
| `LOW_FITNESS` | **1.5** | 1.0 |
| `LOW_2Y_SHARPE` | **2.69** | 1.58 |
| `HIGH_TURNOVER` | 0.70 | 0.70 |
| `CONCENTRATED_WEIGHT` | 0.10 | 0.10 |
| `LOW_SUB_UNIVERSE_SHARPE` | ≈0.434×S | ≈0.434×S |

### §3.1 探测批 1（`USkAQ24Y5jiaP51dWASSaUb`）— **双灭**

设计：一条测「语调趋势」（T9），一条测「新颖度门控」（T4）—— 覆盖本数据集两个最不同的结构轴。

| 模板 | 表达式 | alpha | S | F | 2Y | SUB | TO | margin | CW | 持仓 | 结论 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| T9 双均线语调差 | `rank(subtract(ts_mean(vec_avg(nws48_ess),5), ts_mean(vec_avg(nws48_ess),66)))` | `d5W82bl2` | **−0.14** | −0.03 | 0.30 | 0.07 | **69.06%** | −0.66bp | **0.50 fail** | **14/14** | 判死 |
| T4 新颖度门控 | `trade_when(greater(rank(ts_mean(vec_avg(nws48_ens),22)),0.7), rank(ts_mean(vec_avg(nws48_ess),22)), -1)` | `3qoYMXng` | **0.08** | 0.01 | 0.82 | 0.12 | 2.17% | 2.76bp | pass | 246/233 | 判死 |

`d5W82bl2` 的 `failed_ra_count = 4`（LOW_SHARPE / LOW_FITNESS / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE），
`3qoYMXng` 的 `failed_ra_count = 3`（LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE）。两条都 `ppa_failed`（LOW_SHARPE）。

### §3.2 判死（2 探针 / 2 模板全灭，缺口 ≥2.61）

| 观测 | 数值 | 解读 |
|---|---|---|
| 最好 S | **0.08** | 距 D0 门槛 2.69 差 **2.61**，是所有战役里缺口最大的一个数据集 |
| T9 持仓数 | **14 长 / 14 空** | ★★ 数据集级 coverage 0.7389 是**假象**：`vec_avg(nws48_ess)` 的**有效日频横截面覆盖只有 ~4%**（700 只里约 28 只）。这与 `analyst44` 的「约 20% 股票有事件」相比更极端 |
| T9 CW | **0.50**（2023-12-28） | 28 个持仓里单一名字占一半权重 ⇒ 稀疏到无法分散 |
| T4 vs T9 | T4 持仓 246/233、S 0.08 | 门控救了持仓结构与换手（69%→2.17%），但 S 只从 −0.14 抬到 0.08 ⇒ **不是骨架问题，是字段没有方向性信息** |
| 两个方向 | −0.14 / +0.08 | 正反两个方向都无信号 ⇒ 不是符号搞反 |

**根因判断**：`nws48_ess` 的语义是「故事中该实体的情绪分」，但这是 **RavenPack 的实体级情绪**，
在 GBR TOP700 这种大盘股池上，新闻情绪的定价速度极快 —— D0 拿到的是"当天某条故事的语调"，
而大盘股的日内新闻噪声远大于信息量。**「有真 D0 信息优势」的假设被证伪**：
信息优势存在 ≠ 可提取，因为大盘股覆盖的新闻密度高到情绪均值退化。

### §3.3 D0 结论升级为「结构性不可达」（两次独立尝试 + 外部交叉验证）

| 证据 | 数值 |
|---|---|
| GBR D0 `analyst44` 最好 S | 0.83（缺口 1.86） |
| GBR D0 `news48` 最好 S | 0.08（缺口 2.61） |
| **USA D0 31 批最好 S**（`docs/reference/usa_d0_mining_experience.md`） | **`search_interest` 2.47 / `shortinterest3` 1.95 —— 同样没有任何一条达到 2.69** |

⇒ **三个区域/数据集族、跨 40+ 批次的独立证据一致指向**：D0 的 `LOW_SHARPE / LOW_2Y_SHARPE = 2.69`
（= D1 的 1.70 倍）在本账号的常规骨架下**不可达**。USA D0 原作者自己的结论也是
「D0 门槛 2.69/1.5 极高，单数据集达标难；满足用户指标(1.58/1.0/1.6)的候选可作为 D1 或提示用户降门槛」。

**战役动作**：GBR D0 降为「**不做主动进攻**」，除非出现满足以下之一的新证据，否则不再派 D0 仿真：
1. 找到能在 D0 上做到 S ≥ 2.69 的骨架配方（当前零先例）；
2. 平台下调 D0 门槛（复查 `checks.fail[].limit` 即可，零成本）。

### §3.4 可迁移的负面教训

1. **数据集级 `coverage` 不等于字段的日频横截面覆盖。** `news48` 全数据集 coverage 0.7389，
   但 `vec_avg(nws48_ess)` 实际只覆盖 ~4% 的股票。**判稀疏数据集必须先看 `longCount + shortCount`**，
   而不是 `coverage`。（与 `analyst44` 的「覆盖率匹配 ≠ 字段配对」是同一类陷阱的两个面。）
2. **`CONCENTRATED_WEIGHT 0.50` 是稀疏数据的指纹。** 见到 CW 恰好 0.5 且持仓数 < 50，
   先怀疑字段覆盖稀疏，不要先怀疑骨架。
3. **`trade_when` 门控能修换手与持仓结构，修不了信号方向的有无。** T4 把 TO 从 69% 压到 2.17%、
   持仓从 28 只拉到 479 只，但 S 只从 −0.14 动到 0.08。**门控是放大器不是发生器。**


---

## §4 判死累计

| 对象 | 判据 | 日期 |
|---|---|---|
| （暂无） | | |
