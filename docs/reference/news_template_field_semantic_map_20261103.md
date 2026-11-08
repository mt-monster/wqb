# NEWS 模板跨区字段语义映射表（2026-11-03）

> 用途：把 GBR/论坛的 NEWS 模板从「GBR 具体字段」翻译成**跨区可落地的语义槽位**。
> 迁移时**先查语义槽位，再选具体字段**；字段名相似 ≠ 语义相同（见 §4 反例）。

## §1 语义槽位（Semantic Slots）——模板的真正接口

| 槽位 | 语义 | GBR 实测字段 | CHN news46 | CHN news38 | HKG news36 | AMR news73 |
|---|---|---|---|---|---|---|
| **S1 情绪水平** | 综合情绪分（0–100） | `nws17_multiple_comp_ssc` | `mws46_ssc` | `mws38_score` / `mws38_tone_score` | `positive_sentiment_score_2` | `nws73_globalsent_positivescore` |
| **S2 事件情绪** | 事件层情绪分 | `nws18_multiple_comp_sse` | `mws46_ess` | `mws38_positive_score`/`negative_score` | — | `nws73_globalsent_negativescore` |
| **S3 正负双通道** | 正/负**分开**计分 | （news17 无） | ❌ **无** | ✅ `mws38_positive_score`/`negative_score` | ✅ `mws36_sentiment_positive_confidence`/`negative_confidence` | ✅ `nws73_entitiessent_positivepartscr`/`negativepartscr` |
| **S4 相关度** | 新闻↔实体相关度 | `nws17_multiple_comp_relevance` | `mws46_relevance` | `mws38_relevances` | `mws36_relevance` | — |
| **S5 新颖度** | 事件新鲜度（0–100） | `event_similarity_days` | `mws46_ens` | — | `mws36_novelty` | — |
| **S6 全球新颖度** | 跨供应商新颖度 | — | `mws46_g_ens` | — | `mws36_novelty_oldest_span` | — |
| **S7 冲击幅度** | 未来 2h 市场冲击 | `nws20_nip` | `mws46_nip` | `market_impact_indicator` | — | — |
| **S8 事件计数** | 到达率 / 故事数 | `vec_count(...)` | `mws46_story_count` | `mws38_related_num` | `mws36_total_words` | `nws73_entitiescounter` |
| **S9 时间链年龄** | 距首条事件的毫秒 | `event_similarity_days` | `mws46_ens_elapsed` | — | `mws36_novelty_newest_span` | — |
| **S10 链位序** | 事件链中的序号 | — | `mws46_story_index` | — | `recent_story_time_gap` | — |
| **S11 观点性** | 社论/评论内容强度 | — | `mws46_mce` | — | — | `nws73_entitiessent_finhypepartscr` |
| **S12 恐惧/不确定** | 情绪的非对称维度 | — | — | — | — | `nws73_entitiessent_fearpartscr` / `uncertaintypartscr` |

## §2 模板 → 槽位映射（模板的字段无关写法）

| 模板族 | 必需槽位 | 可选槽位 | 适配区（本次已验） |
|---|---|---|---|
| **T-密度反转**（Da et al. 2011 ASVI） | S8 事件计数 | S9 / S10 | CHN news46 ✓ / HKG news36 ✓（total_words 作代理） |
| **T-乘性置信** | S1 情绪 | S4 相关度 或 S5 新颖度 | CHN news46 ✓（C5）/ CHN news38 ✓ |
| **T-双通道协方差** | S3 正负双通道 | — | **仅** CHN news38 / HKG news36 / AMR news73 |
| **T-nip×收益相关** | S7 冲击幅度 + 内建 `returns` | — | CHN news46 ✓（**方向与 EUR 相反**） |
| **T-冲击×相关价差** | S7 + S4 | — | CHN news46 ✓（C12） |
| **T-观点溢价** | S11 | — | CHN news46 ✓（C11）/ AMR news73 ✓ |
| **T-恐惧/不确定溢价** | S12 | — | **仅 AMR news73** |
| **T-时间链年龄** | S9 | — | CHN news46 ✓ / HKG news36 ✓ |
| **T-链位序** | S10 | — | CHN news46 ✓ |
| **T-实体-故事偏离** | 事件层 vs 全局层同源字段 | — | AMR news73 ✓（**CHN news46 已证退化**） |

## §3 槽位填充优先级（同区多候选字段时）

1. **优先字段级 alphaCount 低**（没人用过）→ 同语义优先取 aC 最低者。
2. **同语义多字段时按「正交性」挑**（GBR L1：相关性的载体 = 字段信息轴 ⇒ 换同语义但不同信息轴的字段才是换轴）。
3. **同源镜像字段对（X vs X_storyid / X vs X_uniq）禁止做差** —— 会退化成恒 0（CHN C9 实测 S=0.00 / TO=0.00；GBR S9 同因）。
4. **元数据字段（time / entitlement / version / country_code / topic_code / *_key）一律不作信号腿**：前者是时间戳，`topic_code`/`news_type` 是分类码（KOR GROUP 标签陷阱：整数分类码禁包 rank/ts_*）。

## §4 ⚠ 三个必须避开的语义陷阱

1. **同名不同层**：`mws46_ess`（实体层事件情绪）vs `mws46_storyid_ess`（故事层）——**同一口径的两层**，做差恒 0（实测退化）。想要「实体 vs 故事」必须用**真正不同的口径**（如 AMR news73 的 per-entity 部分分 vs story-level 全局分）。
2. **同名字段不同通道**：`mws38_positive_score`（正情绪分）vs `mws38_sg_positive_score`（**story-global 层**正情绪分）——**是通道维度而非噪声**，可做「层级差」轴。
3. **论坛模板的方向先验不跨区**：nip×returns 在 EUR 出 PPA（S 3.31），CHN 同结构 **−1.19** ⇒ 方向必须正反各测，且反向腿**换几何不取负**。

## §5 迁移前三查（清单）

- [ ] 目标区 universe = `config.py` 的 `default_universe`（否则 `get_datasets` 静默返回空）
- [ ] 目标字段的 **description** 语义与模板槽位一致（不是字段名相似）
- [ ] 目标区**既有死路**是否覆盖该机制（`tracking/<R>/config/cells.json` 的 dead_ends）
- [ ] 目标区**闸线**（CHN LOW_SHARPE 2.07 / KOR SECTOR+decay4 / HKG SECTOR+decay4 / AMR SUBINDUSTRY+decay4）
- [ ] 目标区**既有档的 `nanHandling`/decay** 与模板壳是否兼容（CHN 禁 `ts_backfill`）
- [ ] 首波必须是 **2×N 因子 A/B（档位 × 壳）**，不能单档直跑