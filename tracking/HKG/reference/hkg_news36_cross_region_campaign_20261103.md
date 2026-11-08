# HKG news36 跨区迁移战役（2026-11-03）

> 战役目标：把 GBR 的 NEWS 模板族迁移到 HKG，点亮 **HKG/D1/news 塔（当前 0/3）**。
> 靶位：**news36 News Analytics Data**（cov **0.81** / 数据集 aC=50 / **字段级 aC 0–14** / valueScore 5 / 43 字段全 VECTOR）。
> 设置档（HKG 既有）：`HKG/TOP800/D1/SECTOR/decay4/trunc0.08/VERIFY/nanHandling ON/pasteurization ON/maxTrade OFF/FASTEXPR`。
> 闸线：S≥1.58 / F≥1.0 / 2Y≥1.6 / TO 5–30% / fRA=0 / prod<0.7 / self<0.7。

## §1 为什么选 HKG 而不是 CHN

| region | S 闸 | 2Y 闸 | 塔位 | 本轮实测 |
|---|---:|---:|---|---|
| CHN | **2.07** | **2.07** | news 0/3（倍率 1.7） | 两个最高质量集（news46 cov1.0 / news38 双通道）均证**两极同负** ⇒ 判死 |
| **HKG** | **1.58** | **1.6** | news 0/3 | 首批**两极对称（+0.27 / −0.27）⇒ 真信号** |
| AMR | 1.58 | 1.0 | news 0/3 | 模板池就绪待发 |

⇒ **HKG 闸线比 CHN 松一档，且首批已出现「真信号指纹」** ⇒ 主力转向 HKG。

## §2 news36 字段族（与 GBR 模板槽位映射）

| 语义槽位 | HKG news36 字段 | 特点 |
|---|---|---|
| S3 正负双通道 | `mws36_sentiment_positive_confidence` / `negative_confidence` | **真·正负通道**（置信而非分数） |
| S3' 词/短语计数 | `mws36_sentiment_words_positive` / `phrase_positive` / `words_negative` / `phrase_negative` | unigram vs bigram 两口径 |
| **归一分母（GBR 没有）** | `mws36_total_words` / `token_count_total` | ★ **词数归一的情绪强度 = 语调的「密度」** |
| S5 新颖度 | `mws36_novelty` / `novelty_score_value` / `story_uniqueness_score` | 0–100 |
| S9 时间链 | `mws36_novelty_newest_span` / `oldest_span` / `recent_story_time_gap` | 毫秒 |
| S4 相关度 | `mws36_relevance` / `entity_relevance_score` | 0–100 |
| 事件置信 | `mws36_key_event_confidence` / `main_event_certainty` | |

**★ 最值得测的新结构（GBR 五轴里完全没有）**：
> **词数归一分母** —— `divide(vec_avg(情绪分), add(vec_avg(total_words), 1))` = 「每千词的语调强度」；
> 这把「情绪水平」除以「报道篇幅」，天然剔除长文稀释，是**情绪密度**而非情绪水平。

## §3 首波实测（6 组 SIG × 正负两极 = 12 条，SECTOR/decay4）

| tag | alpha | S | F | TO | 判读 |
|---|---|---:|---:|---:|---|
| H_wordnorm_neg | `2rApJ67b` | **+0.27** | 0.08 | 4.9% | ✅ **真信号指纹**（与正极严格对称） |
| H_wordnorm_pos | `KPJGb92p` | **−0.27** | −0.08 | 4.9% | ✅ 两极符号相反、|S| 完全相等 |

**★★ 这与 CHN 的「两极同负」形成完美对照，验证双极判据的分辨力**：
> CHN news46 密度：−0.74 / −1.24（同负 ⇒ 伪影）
> HKG news36 词数归一：+0.27 / −0.27（对称 ⇒ 真信号）

⇒ **词数归一分母轴在 HKG 有真实但微弱的定价力**（S 0.27，离闸线 1.58 还远）⇒ 需增益波（wave3：换窗 / 换中性化族 / 换字段 / 换口径）。

## §4 wave3 增益波设计（11 条，已 preflight `valid=true`）

| tag | 增益杠杆 | 目的 |
|---|---|---|
| H2_wn_fast15 | wordnorm + FAST 中性化 | 测因子型中性化在 HKG 是否也毒（HKG 既有档是 SECTOR=分组型） |
| H3_wn_short | 短窗（22/66） | 情绪时效性短窗（论坛帖：新闻情绪短窗 5–22 有效） |
| H4_wn_stat | STATISTICAL 中性化 | 同族对照 |
| H5_wn_fast | FAST 中性化 | 同族对照 |
| H6_phrase | bigram 口径归一 | 换情绪测量口径 |
| H7_posneg_spread | 正负置信价差 | 双通道价差轴 |
| H8_conf_cov | 正负置信协方差 | 96 赞帖双通道协方差法 |
| H9_negheat | 负面置信水平 | 恐惧溢价轴 |
| H10_novelty | 新颖度水平 | S5 轴 |
| H11_relevance | 相关度水平 | S4 轴 |
| H12_eventcert | 事件置信 | 事件确定性轴 |

## §5 跨区迁移参考

- GBR 模板总结速查：`docs/reference/gbr_news_template_summary_quickref_20261103.md`
- 字段语义映射：`docs/reference/news_template_field_semantic_map_20261103.md`
- 迁移 SOP：`docs/reference/cross_region_template_migration_sop_20261103.md`
- 完整归因：`docs/reference/gbr_news_template_summary_and_cross_region_migration_20261103.md`
## §3b 首波实测四读数（全部严格对称 ⇒ 真信号已确认）

| tag | alpha | S | F | TO |
|---|---|---:|---:|---:|
| H_wordnorm_neg | `2rApJ67b` | **+0.27** | 0.08 | 4.9% |
| H_wordnorm_pos | `KPJGb92p` | **−0.27** | −0.08 | 4.9% |
| H_confspread_neg | `O0AGp35d` | **+0.15** | 0.03 | 4.8% |
| H_confspread_pos | `JjeGp9gm` | **−0.15** | −0.03 | 4.8% |

**★★ 四条读数两两严格对称（|S| 完全相等、符号相反）⇒ HKG news36 的词数归一情绪轴与正负置信价差轴都是真信号。**

与 CHN 的对照（同一骨架）：CHN 六组全部**两极同负**（伪影），HKG 两组全部**两极对称**（真信号）——判据的分辨力得到实证。

### ⇒ HKG 的问题性质 = 「真但弱」，不是「假」

S 0.27 / 0.15 离 HKG 闸线 1.58 还差一个数量级 ⇒ 属**工程问题**（增益），不是机制问题。

## §6 wave4 强度放大波（12 条，已 preflight `valid=true`）

| tag | 放大杠杆 | 针对 |
|---|---|---|
| H4_netnorm | 正负情绪都归一后取差（净语调密度） | 提高信噪 |
| H5_wn_short | 短窗 22/66 | 情绪时效性（论坛：短窗 5–22 有效） |
| H6_wn_long | 长窗 120/504 | 反向对照 |
| H7_wn_noshell | **去壳**（纯 rank） | 强度↑换手↑，检验 F 是否上得去 |
| H8_wn_stat | 中性化 → STATISTICAL | 中性化族（CHN 已证 FAST 族有毒，HKG 需独立验证） |
| H9_wn_fast | 中性化 → FAST | 同上 |
| H10_wn_d22 | decay 22 | 提 F / 降换手 |
| H11_wn_tok | 换分母 `token_count_total` | 归一分母口径变体 |
| H12_confnorm | 正负置信差 ÷ 词数 | 置信通道归一 |
| H13_wn_x_phrase | unigram × bigram 交互 | 两口径一致性（质量代理） |
| H14_wn_short_d8 | 短窗 + decay 8 | 组合 |
| H15_wn_x_rel | 词数归一 × 相关度（乘子） | 相关度作置信乘子（论坛已验证套路） |

**判读口径**：找 S ≥ 1.0 的格（离闸线 1.58 最近）；若全部仍 < 0.5 ⇒ HKG news36 也判死，转 AMR。
## §3c ★ 修正：HKG 首波三组全部严格对称（第三组是 novelty 时间链，非 confspread）

| # | 轴 | SIG | 负极 alpha / S | 正极 alpha / S | 判读 |
|---|---|---|---|---|---|
| 1 | **词数归一情绪** | `divide(vec_avg(mws36_sentiment_words_positive), add(vec_avg(mws36_total_words), 1))` | `2rApJ67b` **+0.27** | `KPJGb92p` **−0.27** | ✅ 严格对称 |
| 2 | **新颖度时间链** | `ts_mean(vec_avg(mws36_novelty_newest_span), 22)` | `O0AGp35d` **+0.15** | `JjeGp9gm` **−0.15** | ✅ 严格对称 |
| 3 | 正负置信价差 | `subtract(vec_avg(mws36_sentiment_positive_confidence), vec_avg(mws36_sentiment_negative_confidence))` | `O0AGp35d`（见下注） | `JjeGp9gm`（见下注） | ⚠ 实为第 2 组 |

⚠ **注**：先前记录的「confspread ±0.15」经 `get_user_alphas` 回读表达式，实为 **novelty 时间链轴**（`mws36_novelty_newest_span`）；confspread 组（第 3 组）尚未跑出。

### ★ 修正后的判断

- **HKG news36 已有 2 条轴确认真信号**（词数归一 ±0.27、novelty 时间链 ±0.15），两极严格对称 ⇒ 定价力真实存在。
- **但两条轴共享同一骨架与同一档位** ⇒ 强度都只有 0.15–0.27 ⇒ 更可能是「**该骨架在 HKG 的整体定价力就这个量级**」，而不是「单轴弱」。
- ⇒ wave4 的增益波（换窗 / 去壳 / 换中性化族 / 换分母 / 短窗）必须能显著提强度，否则 HKG news36 也判死。
- ⚠ **表述纪律**：不要用「两轴独立确认」夸大——**两条轴的 |S| 不同（0.27 vs 0.15）且同骨架**，独立性未证。
## §7 ★★★★ wave4 突破：窗口是主杠杆（不是轴）

| tag | 杠杆 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| H4_netnorm | 正负情绪都归一后取差（**换轴**） | `QPvGVN7W` | +0.11 | 0.02 | 4.9% |
| **H5_wn_short** | **同轴，窗口 60/252 → 22/66** | **`xArNk2jp`** | **+0.64** | **0.32** | **5.2%** |

### ★ 判决

- **换轴（净语调差）反而更差**：0.27 → **0.11**（信号被正负相消抵消）。
- **只换窗口（60/252 → 22/66）就提升 2.4 倍**：0.27 → **0.64**，F 也从 0.08 → 0.32。
- ⇒ **新闻情绪类信号，窗口（时效性）比轴（语义）更能决定强度。**

**论坛佐证**：「给信号标保质期——新闻情绪字段的时效性分级与短窗模板」把长窗 120 缩到 5 日后信号清晰，**「不是池塘没鱼，是鱼饵保质期不对」**；另一帖「新闻情绪短窗 5–22 有效」。

### ⇒ 对 GBR 强几何的反向校正

GBR 的强几何用 `ts_mean(·,60) + ts_rank(·,252)`，因为 GBR 的信号是**事件到达率**（慢变量）；
但**跨区换到情绪/语调类字段后，60/252 把时效性压没了** ⇒ **换区后必须重扫窗口，不能照抄源区窗口**。

### wave5 窗口细化波（12 条，已 preflight `valid=true`）

围绕 22/66 细化为 5/66、5/126、22/126、22/252 四格，并把净语调差轴 / novelty 时间链轴 / 置信差轴也换成短窗版，
另加 1 格中性化族对照（STATISTICAL）。

**判读口径**：找 S ≥ 1.0 的格（离闸线 1.58 最近）；若 12 格全 < 0.5 ⇒ HKG news36 也判死，转 AMR / EUR。
### §7b 窗口阶梯四档（单调关系，同轴同骨架同档）

| 窗口（平滑/分位） | alpha | S | F | TO |
|---|---|---:|---:|---:|
| 120 / 504 | `A1VG7dqd` | **+0.10** | 0.02 | 4.6% |
| 60 / 252（GBR 强几何惯例） | `2rApJ67b` | +0.27 | 0.08 | 4.9% |
| **22 / 66** | **`xArNk2jp`** | **+0.64** | **0.32** | **5.2%** |
| 60 / 252 去壳（纯 rank） | `ZYQEKLkn` | +0.21 | 0.05 | 8.2% |

⇒ **S 与窗口长度单调反比**：0.10 → 0.27 → 0.64。**单调比单点更可信**。

**附带两条**：
- **壳在长窗下有保留作用**（去壳 0.21 < 带壳 0.27）—— 与「壳有害」的直觉相反，但只在这一档成立；
- **换轴可能因正负相消反而更差**（净语调差 0.11 < 词数归一 0.27）。

⇒ **跨区迁移的第一增益波 = 窗口阶梯波**（≥3 档形成单调趋势），不是换轴波。
### §7c wave4 单变量杠杆完整表（6 条，同轴同骨架同档）

| tag | 唯一变动 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| H6_wn_long | 窗口 → 120/504 | `A1VG7dqd` | +0.10 | 0.02 | 4.6% |
| H4_netnorm | **换轴**（正负归一后取差）60/252 | `QPvGVN7W` | +0.11 | 0.02 | 4.9% |
| H11_wn_tok | 换分母 → `token_count_total` 60/252 | `P0oGO7PM` | +0.23 | 0.07 | 5.2% |
| H10_wn_d22 | decay 4→22 60/252 | `LLMGd786` | +0.20 | 0.05 | 4.1% |
| H7_wn_noshell | **去壳** 60/252 | `ZYQEKLkn` | +0.21 | 0.05 | 8.2% |
| **H5_wn_short** | **窗口 → 22/66** | **`xArNk2jp`** | **+0.64** | **0.32** | **5.2%** |

⇒ **单变量隔离结论**：在 HKG news36 上，**窗口是唯一能带来量级提升的杠杆**（0.64 vs 其余 0.10–0.23）；
换轴 / 换分母 / 换 decay / 去壳 都只带来 0.10–0.23 的边际变化，**不足窗口提升的 1/3**。

### 逐年覆盖核查（入篮前必查，`get_alpha_yearly_stats` 实测）

`xArNk2jp`（S 0.64 / F 0.32）：**10/10 年全有 pnl + longCount 220–315** ⇒ 覆盖闸通过，无 leading-gap、无连续空窗。

但逐年 S 摆动大：0.72 / −0.30 / 0.61 / **2.36** / 0.09 / 0.59 / −0.14 / 0.95 / 0.72 / 1.17
⇒ **整体 0.64 主要由 2017 的 2.36 拉动**，稳定性不足 ⇒ 该件尚不可入篮，需窗口阶梯波（wave5）再提强度与稳定性。

## §7d ★★★★ wave4 完整 12 条表（补齐 §7/§7c 未记的后 6 条）

| tag | 唯一变动 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| **H14_wn_short_d8** | **22/66 + decay 8** | **`JjeGGQVE`** | **+0.69** | **0.36** | **5.0%** |
| H5_wn_short | 22/66（基准） | `xArNk2jp` | +0.64 | 0.32 | 5.2% |
| **H8_wn_stat** | **60/252 + 中性化 STATISTICAL** | **`qMLN6w6O`** | **+0.52** | 0.19 | 7.0% |
| **H9_wn_fast** | **60/252 + 中性化 FAST** | **`9qxp72pq`** | **+0.40** | 0.13 | 8.2% |
| H11_wn_tok | 换分母 `token_count_total` | `P0oGO7PM` | +0.23 | 0.07 | 5.2% |
| H15_wn_x_rel | 词数归一 × `rank(relevance)` | `pwdNN5qo` | +0.22 | 0.06 | 4.9% |
| H7_wn_noshell | 去壳 | `ZYQEKLkn` | +0.21 | 0.05 | 8.2% |
| H10_wn_d22 | decay 22 | `LLMGd786` | +0.20 | 0.05 | 4.1% |
| H4_netnorm | 换轴（净语调差） | `QPvGVN7W` | +0.11 | 0.02 | 4.9% |
| H6_wn_long | 120/504 | `A1VG7dqd` | +0.10 | 0.02 | 4.6% |
| H13_wn_x_phrase | × 短语正分 | `qMLNN9qv` | −0.04 | −0.00 | 4.9% |
| H12_confnorm | 置信度归一（正/负置信差） | `0mYppO02` | −0.48 | −0.19 | 4.9% |

### ★★★ 新结论：HKG 上**因子型中性化是增益**，与 CHN 完全相反

| 中性化（60/252 词数归一） | S | 族 |
|---|---:|---|
| **STATISTICAL** | **+0.52** | 因子型 |
| **FAST** | **+0.40** | 因子型 |
| SECTOR（既有档） | +0.23 | 分组型 |
| SECTOR dec22 | +0.20 | 分组型 |

⇒ **同一结构在 HKG 上，因子型中性化比分组型高 1.8–2.3×**；而在 CHN 上因子型是**毒档**（−0.67…−0.76）。
⇒ **中性化族的优劣是 region 特异的，源区出货档不可跨区照抄**（与 §7 的窗口结论并列的第二条跨区铁律）。

### ⇒ wave5 / wave6 状态

- **wave5（12 条窗口细扫 + STATISTICAL 22/66）**：已 preflight `valid=true`，在飞。
  其中 **STATISTICAL 22/66** 是全波最高价值格 —— 若 STATISTICAL 的 2.3× 优势在短窗保持，
  则 0.64 × 2.3 ≈ **1.47**，逼近闸线 1.58。
- **wave6（12 条未用字段轴）**：已 preflight `valid=true`，待发。
  **触发原因**：HKG news36 共 **43 个字段**，此前只用了 7 个。
  未测的高价值字段：`mws36_key_event_confidence`（**aC=14，全数据集最高**）、`story_uniqueness_score`（HKG 存在）、
  `mws36_novelty`、`positive_sentiment_certainty`、`negative_sentiment_certainty`、`event_impact_value`，
  以及乘法结构（`multiply(词数归一, rank(relevance))`）的短窗版。

## §8 ★★★ wave5 收批（10/12 已收，2 条在飞）

| tag | 内容 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| H5_wn_w22_126 | 词数归一 22/126 | `58Epl2RM` | **+0.56** | 0.26 | 5.3% |
| H5_net_w22_66 | 净语调差 22/66 | `JjeGxR0O` | +0.34 | 0.12 | 5.2% |
| H5_net_w22_126 | 净语调差 22/126 | `3qop9g3g` | +0.30 | 0.10 | 5.3% |
| H5_wn_w22_252 | 词数归一 22/252 | `omEN6YRk` | +0.22 | 0.07 | 5.3% |
| H5_conf_w22_66 | 置信差 22/66 | `O0AGN20R` | +0.12 | 0.03 | 5.2% |
| H5_nov_w22_66 | novelty 22/22→66 | `npvNdXpz` | +0.10 | 0.02 | 5.5% |
| H5_wn_w5_66 | 词数归一 5/66 | `RREmVrl0` | +0.03 | 0.00 | **28.8%** |
| H5_wn_w22_66b | 词数归一 **10/66** | `9qxpX2o1` | −0.03 | −0.01 | 10.5% |
| H5_net_w10_66 | 净语调差 10/66 | `zq3N8WaO` | −0.03 | −0.00 | 10.5% |
| H5_net_w5_66 | 净语调差 5/66 | `VkxGa8o5` | −0.20 | −0.06 | **29.0%** |
| （在飞） | relevance 22/66 | — | — | — | — |
| （在飞） | **STATISTICAL 22/66** ★ | — | — | — | — |

### ★ 结论：HKG 词数归一的最优窗口是 22/66，且**分位比窗口更敏感**

- **窗口维度**：5/66 → 0.03（TO 爆 28.8%）、**22/66 → 0.64（峰值）**、更长待补。
- **分位维度**：22/126 → 0.56、22/252 → 0.22 ⇒ **分位缩短也单调提升**（与 AMR uncertainty 的 22/30 最优同向）。
- **10/66 反而更差**（−0.03）⇒ 与 AMR uncertainty 的「10/66 最强」**方向相反**
  ⇒ 再次印证「**每区每轴的最优窗口不同，必须独立扫**」。
- 置信差轴（0.12）与 novelty 轴（0.10）都是**弱轴**，不值得继续。

### ★ 最高价值待收格：STATISTICAL 22/66

wave4 实测（60/252）STATISTICAL 0.52 vs SECTOR 0.23 = **2.3×**。
若该优势在 22/66 保持 ⇒ 0.64 × 2.3 ≈ **1.47**，逼近闸线 1.58。## §9 ★★★★★ wave5 全收（12/12）：STATISTICAL 中性化把 HKG 推到 **0.81**

### 补收的两条（原「在飞」）

| tag | 内容 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| H5_rel_w22_66 | relevance 22/66 | `xArN1arl` | +0.29 | 0.09 | **1.96%** |
| **H5_wn_w22_66_stat** | **词数归一 22/66 / STATISTICAL** ★ | `VkxGdoxb` | **+0.81** | **0.40** | 7.75% |

### ★★★ 核心发现：HKG 上因子型中性化是**增益**（与 CHN 完全相反）

| 中性化 | 族 | 窗口 | S | 来源 |
|---|---|---|---:|---|
| SECTOR | 分组型 | 22/66 | 0.64 | wave4 #1 |
| **STATISTICAL** | **因子型** | **22/66** | **0.81** | wave5 #11 |
| STATISTICAL | 因子型 | 60/252 | 0.52 | wave4 #6 |
| FAST | 因子型 | 60/252 | 0.40 | wave4 #7 |

⇒ **同区、同轴、同窗口下，STATISTICAL 比 SECTOR 高 1.27×**（0.64 → 0.81）。
⇒ 与 CHN 的「因子型是毒档（FAST −0.67 / STATISTICAL −0.74 / SLOW −0.76）」**完全相反**。
⇒ 中性化族的增益/毒性与区域强相关，**源区（GBR=FAST）出货档不可跨区照抄** 这条铁律再添一例。

### ★ 其余读数

- **relevance 22/66 = +0.29，TO 仅 1.96%** —— 换手极低（其它轴 5–10%），但 S 太低，不足以单独成事。
- 净语调差 22/66 = +0.34、22/126 = +0.30 ⇒ 第二强轴，明显弱于词数归一。
- 置信差 0.12、novelty 0.10 ⇒ 弱轴，放弃。
- **10/66 = −0.03**（SECTOR）再次确认 HKG 最优窗是 **22/66**，不是 10/66（与 AMR 相反）。

### ⇒ wave9（12 条，已 preflight `valid=true`，已派）

在 **STATISTICAL** 档下重扫窗口（22/126、22/252、10/66、15/66、22/30、22/504）
与字段（net / keyconf / uniq / nov / rel），并测 STATISTICAL + decay8。基线 0.81，目标 ≥1.0。

## §10 ★★★★★ wave9 全收（10/12 落库，2 条与 wave4 重复）：**decay8 把 HKG 推到 0.88**

| tag | 内容 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| **H9_wn_22_66_stat_d8** | 词数归一 22/66 / STATISTICAL / **decay8** ★ | `KPJGvmEp` | **+0.88** | **0.45** | 7.55% |
| H9_wn_22_504_stat | 词数归一 22/504 / STAT | `xArNVz3w` | +0.65 | 0.29 | 7.93% |
| H9_wn_15_66_stat | 词数归一 15/66 / STAT | `mLo5Kd9X` | +0.60 | 0.29 | 9.25% |
| H9_rel_22_66_stat | **relevance 22/66 / STAT** | `e753V15l` | **+0.53** | 0.17 | **3.16%** |
| H9_wn_22_30_stat | 词数归一 22/30 / STAT | `mLo5dzg1` | +0.41 | 0.15 | 7.66% |
| H9_net_22_66_stat | 净语调差 22/66 / STAT | `kqNPvJPl` | +0.38 | 0.13 | 7.72% |
| H9_uniq_22_66_stat | story_uniqueness 22/66 / STAT | `j2Y6Pnpo` | −0.33 | −0.10 | 7.65% |
| H9_keyconf_22_66_stat | key_event_confidence 22/66 / STAT | `3qopkEKg` | +0.32 | 0.13 | 12.39% |
| H9_wn_10_66_stat | 词数归一 10/66 / STAT | `akK1RevW` | +0.26 | 0.09 | 12.56% |
| H9_novnewest_22_66 | novelty_newest_span 22→22/66 | `LLMGm859` | +0.13 | 0.03 | 8.32% |
| （重复） | 词数归一 22/126、22/252 | wave4 已读 | +0.30 / +0.22 | — | — |

### ★★★ 三条结论

1. **decay8 在 HKG 是增益**：词数归一 22/66 从 decay4 的 0.81 → **0.88（+8.6%）**；
   SECTOR 档同样 0.64 → 0.69。**与 AMR（decay8 = −0.28，毒档）完全相反**
   ⇒ 再次印证「decay 档也是区域特异的，不可跨区照抄」。
2. **22/66 仍是 STATISTICAL 下的峰值**：15/66 = 0.60、22/30 = 0.41、10/66 = 0.26、22/504 = 0.65。
   窗口单调性：10/66 (0.26) < 15/66 (0.60) < **22/66 (0.88)** > 22/504 (0.65) ⇒ 峰值在 22 附近。
3. **relevance 轴在 STATISTICAL 下跳到 +0.53**（SECTOR 下仅 +0.29，**1.83×**），且 **TO 仅 3.16%**
   —— 低换手 + 中等强度，是**最优的「第二腿」候选**（待与词数归一做合规组合）。

### ⇒ wave10（12 条，峰值回差新几何，已 preflight `valid=true`）

骨架 `ts_target_tvr_decay(group_neutralize(-ts_max_diff(vec_avg(F), 620), densify(market)), …)`，
字段 = 词数正/负、正/负置信度、relevance、novelty、key_event_confidence，另含镜像、252/1008、hump、group_scale。
来源：论坛 pid `43836589723287`（EUR/D1/EARNINGS 实测 **S 1.69 / 2Y 2.24 / 0 FAIL**，已提交 OS）。


### ⇒ wave12（12 条，ts_zscore 分布概率差新几何，已 preflight `valid=true`，16:08 已派）

骨架：`signed_power(subtract(ts_zscore(vec_avg(mws36_sentiment_positive_confidence),252), ts_zscore(vec_avg(mws36_sentiment_negative_confidence),252)), 3)`
来源：论坛 pid `43620895448343`（EUR/TOP2500/D1/COUNTRY，earnings_sent_matrix 实测 **S 1.69 / 2Y 2.24 / 0 FAIL**，已提交 OS）。
12 个结构互异变体：分别标准化 / 先差后标准化 / 线性 / 平方 / 短标准化窗 / 先平滑 / 词数占比 / 末端 rank / zscore 后 ts_rank / group_neutralize 壳 / 相对净比。
**注意**：这是本区**首次使用 `ts_zscore`（自身历史标准化）几何**，与既有 `ts_rank`（横截面）骨架完全不同——是跨区迁移里少见的「换几何」而非「换字段」。

### ⇒ wave13（12 条，sign 持续性几何，已 preflight `valid=true`，待派）

骨架：`ts_mean(sign(ts_delta(net_sentiment, 5)), 22)` 等；net = 正/负置信度差。
来源：论坛 pid `43614940683799`（「从变化的稳定性而非变化的大小入手」）。
12 个结构互异变体：方向均值 / 方向净计数 / 变化波动 / 长步长 / 持续性+自身标准化 / 末端 rank / ts_rank / 换字段 / 长持续性窗 / 分组中性化壳 / 符号波动 / 立方放大。

### ⇒ wave14（12 条，跨族乘子 wn × 事件元数据，16:53 派，17:22 停于 7/12）

骨架：`ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(wn, MULT), 22), 66), densify(market)), …)`
wn = `divide(vec_avg(mws36_sentiment_words_positive), add(vec_avg(mws36_total_words), 1))`，设置 HKG/TOP800/D1/STATISTICAL/decay8。
12 个乘子：relevance（rank / ts_rank / zscore / 归一化 4 种）、key_event_confidence（rank / ts_rank）、novelty（rank / zscore）、story_uniqueness_score、entity_relevance_score、event_impact_value、main_event_certainty。
来源：记忆「跨族乘子（事件元数据 × 情绪）是唯一未被证伪的乘子结构」+ wave9 relevance 轴 TO 仅 3.16%。

| 条目 | 乘子 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| #0 | wn × rank(relevance) | `KPJGWdmz` | +0.91 | 0.47 | 7.63% |
| #3 | wn × relevance/mean(relevance,66) | `RRE7JMRg` | **+0.92** | 0.48 | 7.62% |
| #1 | wn × ts_rank(relevance,66) | `zq3NlkoG` | +0.76 | 0.36 | 7.58% |
| #6 | wn × rank(novelty) | `3qolM55Q` | +0.48 | 0.22 | 12.63% |
| #8 | wn × rank(story_uniqueness) | `wpQjpzm1` | +0.44 | 0.16 | 7.58% |
| #4 | wn × rank(key_event_confidence) | `zq3kvOAO` | +0.14 | 0.04 | 12.42% |
| #2 | wn × ts_zscore(relevance,252) | `MPYGJV8r` | +0.03 | 0.00 | 4.09% |

**结论**：跨族乘子**只有 relevance 系有效**（0.91–0.92，比基座 0.88 高 4.5%），其余事件元数据乘子全部 ≤0.48。
⇒ **乘子结构在 HKG 是边际增益（+4.5%），不是破墙杠杆**。破 1.58 闸不能靠乘子。

### ⇒ AMR news85（新数据集，16:53 派，17:07 停于 4/12，判死）

news85 "News Sentiment Analysis using DNN"，cov=0.9261，23 字段（22 MATRIX + 1 VECTOR），每字段 aC ≤ 6（极度不拥挤）。
带壳版 12 条（MATRIX 字段无 vec_avg，壳 22/66）→ 4 条全弱：−0.18 / −0.24 / −0.01 / +0.13。
**结论**：**判死**。字段（sentiment_overall_average/median、distribution_skewness、peak_sentiment_value、sentiment1/2_*）作为信号全部 |S| ≤ 0.24。
⇒ 印证「弱数据集当信号活不了；换角色 ≠ 换族」在 DNN 情绪集上同样成立。

