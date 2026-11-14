# DEU S1 字段画像：news17 / news18（2026-11-13）

> 归档路径规则：`tracking/DEU/atom_orthogonal/FIELD_PROFILE_<数据集>_<YYYYMMDD>.md`（沿用本战役 FIELD_PROFILE_RECHECK_20261112 命名惯例）。
> 任务上下文：DEU 20 颗 regular alpha 攻坚（缺口 3 颗），NEWS 塔（0 颗未点亮）首攻。
> 数据源：MCP `get_datafields`（DEU/TOP500/D1，filter_sharpe=false 全量拉取，complete=true）。

## 一、数据集级画像

| 维度 | news17（PR Edition Data） | news18（Ravenpack News Data） |
|---|---|---|
| 塔位 | DEU/D1/NEWS（0 颗未点亮）×1.8 | DEU/D1/NEWS（0 颗未点亮）×1.8 |
| 平台 cov | 0.7906 | 0.8046 |
| 字段总数 | 48（全 VECTOR） | 70（64 VECTOR + 6 SYMBOL） |
| **双档结构** | 单实体 `nws17_*` cov **0.6489**；多实体复合 `nws17_multiple_comp_*` cov **0.9323** | 单实体 cov **0.6925/0.6965**；`multi_entity_*` / `nws18_multiple_comp_*` cov **0.9788** |
| 数据形态 | 事件流：每日每股多条新闻记录（VECTOR 多值），**必须 vec_* 聚合后 ts_backfill 转面板** | 同左 |
| 更新频率 | 日频事件驱动（有新闻才有值，无新闻日 NaN） | 同左 |
| 近十年数据 | ✅ 平台 cov 0.79-0.93 非稀薄覆盖，无 sentiment7/27 的 5 年断档问题（待首波探针 yearly 验证） | ✅ 同左 |
| ATOM 契合 | 单集自足（情绪+relevance+新颖度+事件数同集内组腿，保 ATOM） | 同左 |

## 二、news17 字段族画像（48 字段全梳理）

### 2.1 情绪信号族（9 字段，核心 alpha 载体）

| 字段 | cov | 类型 | 取值分布 | 机制 | 可用性 |
|---|---:|---|---|---|---|
| `nws17_multiple_comp_ssc` | 0.9323 | VECTOR | 连续 [-1,1] 综合情绪 | Tetlock 情绪因子主载体 | ★★★ 首选 |
| `nws17_multiple_comp_event_sentiment_score` | 0.9323 | VECTOR | 连续 [-1,1] 实体级情绪 | 同上（实体 vs 故事级差异） | ★★★ |
| `nws17_multiple_comp_acb` | 0.9323 | VECTOR | 三值 {-1,0,1} 盈利发布情绪 | 盈利事件通道 | ★★★（用户最多 18） |
| `nws17_multiple_comp_bee` | 0.9323 | VECTOR | 三值 盈利评估情绪 | 盈利事件通道 | ★★ |
| `nws17_multiple_comp_nip` | 0.9323 | VECTOR | 连续 [-1,1] 2h 市场冲击预测 | 尾部冲击/门控 | ★★★（信息量大） |
| `nws17_multiple_comp_qcm` | 0.9323 | VECTOR | tone 综合（BMQ/BEE/BCA/ANL-CHG 合成） | 综合质量分 | ★★ |
| `nws17_multiple_comp_qep` | 0.9323 | VECTOR | 三值 PEQ 股票情绪 | 词频情绪 | ★ |
| `nws17_multiple_comp_bam/qmb` | 0.9323 | VECTOR | 三值 M&A / 社论情绪 | 事件类型通道 | ★（M&A 稀疏） |
| `nws17_multiple_comp_ber` | 0.9323 | VECTOR | 三值 分析师评级变化新闻 | **与 analyst 塔机制重叠，篮内已有修正族 → 慎用（相关性风险）** | ⚠️ |
| 单实体档同族 `nws17_ssc/acb/bee/nip/qcm/qep/qmb/event_sentiment_score/ghc_lna` | 0.6489 | VECTOR | 同上 | cov 低 30%，仅作多实体档对照 | ★ |

### 2.2 结构/注意力族（4 字段）

| 字段 | cov | 分布 | 机制 | 可用性 |
|---|---:|---|---|---|
| `nws17_multiple_comp_relevance` | 0.9323 | 整数 0-100 | 31 赞配方：情绪加权分母；高 relevance=强注意 | ★★★ |
| `nws17_multiple_comp_event_similarity_days` | 0.9323 | 0-365 天 | Da-Gao 新颖度：小=新事件；31 赞新颖度过滤 | ★★★ |
| `nws17_multiple_comp_rp_story_event_count` | 0.9323 | 计数 | 事件量脉冲=关注度冲击（Da-Gao 反转） | ★★ |
| `nws17_multiple_comp_rp_story_event_index` | 0.9323 | 序号 | 元数据 | ✗ |
| `analyst_recommendation_change_score` | 0.9323 | 三值 | 分析师通道（同 2.1 ber 风险） | ⚠️ |

### 2.3 元数据/无信号族（31 字段，全部排除）

`*_country_code`（2）、`*_event_end/start_time_utc`（4）、`*_event_text/headline`（4）、`*_reporting_*_time_utc`（4）、`*_timestamp_utc_time`（2）、`nws17_relevance` 单实体档与 `nws17_ghc_lna`、单实体档全族对照件。⇒ **48 字段中可用信号面 = 多实体档 17 字段（13 信号 + 4 结构），单实体档仅作聚合算子对照**。

## 三、news18 字段族画像（70 字段全梳理）

### 3.1 情绪信号族（multi_entity 档 cov 0.9788 为全库最高档）

| 字段 | cov | 分布 | 机制 | 可用性 |
|---|---:|---|---|---|
| `nws18_multiple_comp_ssc` | 0.9788 | 连续 [-1,1] | 主载体（用户 12/alpha 18 最热） | ★★★ |
| `nws18_multiple_comp_sse` | 0.9788 | 连续 [-1,1] 事件极性 | 实体-事件级情绪（与 ssc 成对做 spread） | ★★★ |
| `nws18_multiple_comp_nip` | 0.9788 | 连续 [-1,1] 2h 冲击 | 尾部门控 | ★★★ |
| `nws18_multiple_comp_bee/ber/acb/bam/qmb/qep/qcm/ghc_lna` | 0.9788 | 三值 | 同 news17 分类器族（ber/ghc_lna=分析师通道慎用） | ★★（ber/ghc_lna ⚠️） |
| 单实体档 `nws18_ssc/sse/nip/qcm/qep/qmb/bee/acb/bam/ber` | 0.6965 | 同上 | 对照档 | ★ |
| D1 别名族 `sentiment_commentary_classifier(BMQ)/sentiment_composite_score_d1(CSS)/…` | 0.6925 | 同上 | **同一底层字段的别名**（描述明示 alias）⇒ 与主字段完全共线，只测其一 | ⚠️ 别名陷阱 |

### 3.2 结构/注意力族

| 字段 | cov | 机制 | 可用性 |
|---|---:|---|---|
| `nws18_mltpl_cmp_event_simildays` / `days_since_similar_event` | 0.9788/0.6925 | 新颖度门控（同 news17） | ★★★ |
| `nws18_mltpl_cmp_event_relevance` / `nws18_multiple_comp_relevance` | 0.9788 | 情绪加权 | ★★★ |
| `multi_entity_story_event_count` / `story_event_record_count` | 0.9788/0.6965 | 事件量脉冲 | ★★ |
| `event_relevance_score` / `sentiment_relevance_score`（alias） | 0.6925 | 别名共线 | 只测其一 |

### 3.3 SYMBOL 型（6 字段）与元数据（排除）

`event_sequence_number_in_story`、`multi_entity_event_sequence_number`、`multi_entity_record_date/time_utc`、`record_timestamp_utc_date/time` = 序号/时间戳，无信号。日期时间类 VECTOR（`event_start/end_date_utc` 等约 16 字段）、国家码（2）、文本（2）全部排除。**70 字段可用信号面 ≈ 22 字段（multi_entity 档 17 + 单实体对照 5）**。

## 四、机制模板匹配（画像 → 模板，论坛+论文来源已核）

| # | 机制 | 模板骨架（≤12 算子） | 来源 |
|---|---|---|---|
| M1 | **relevance 加权情绪**（裸 sentiment 是错的） | `group_rank(ts_backfill(vec_sum(multiply(情绪, relevance)), W), sector)` | 论坛 31 赞帖 |
| M2 | 情绪水平对照 | `group_rank(ts_backfill(vec_avg(情绪), W), sector)` | Tetlock 2007 |
| M3 | **新颖度门控情绪**（只交易新事件） | `trade_when(vec_max(simildays) < T, 情绪信号, -1)` | Da-Gao 2011 + 31 赞 |
| M4 | 关注度冲击反转 | `-group_rank(ts_backfill(vec_sum(event_count), W), sector)` | Da-Gao / Fang-Peress |
| M5 | 尾部冲击门控（nip 单向事件指纹） | `trade_when(abs(vec_max(nip)) > x, 信号, -1)` | risk60 取反衰减指纹沉淀 |
| M6 | ssc-sse spread（故事级 vs 事件级情绪分歧） | `group_rank(ts_backfill(vec_sum(subtract(ssc, sse)), W), sector)` | 本战役「跨字段比值/差值有效」判词（sentiment27 死档） |
| M7 | 双层中性化（杠杆 A） | `group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)` | FINAL_LEDGER 杠杆 A |
| M8 | 聚合算子维度 | vec_sum / vec_avg / vec_max / vec_min（S1 实证 vec_max>vec_avg） | DEU S1 教训 |
| M9 | 情绪动量 Δ | `group_rank(ts_delta(ts_backfill(vec_sum(情绪), W1), W2), sector)` | Chan 2003 新闻动量 |
| M10 | backfill 窗口阶梯 | 66 / 126 / 252（慢变量 66 基线律 + news 事件 126 中档） | BACKFILL-WINDOW-SUB-CLIFF 死档 |

**别名共线陷阱（画像新发现）**：news18 的 `sentiment_*_d1` 系列描述明示是 BEE/CSS/NIP/PEQ 等的 **D1 feed 别名**——测主字段即可，别名不重复测（省槽位）。

**分析师通道风险（画像新发现）**：`ber / ghc_lna / analyst_recommendation_*` 是新闻流里的分析师评级变化。篮内 17 颗有大量 ANALYST 修正族（zq3eb7No 等 9 颗）⇒ 此通道相关性风险高，**首波不派**，除非情绪主通道全军覆没。

## 五、首波派发计划（探针 SOP v2：双结构 × 跨族代表 + 机动）

波 **BE221**（news18 multi_entity 档，cov 0.9788 最高）+ **BE222**（news17 multiple_comp 档）并发 2：

- 双结构 = M2 裸水平（对照）+ M1 relevance 加权（论坛配方）
- 跨族代表字段 = ssc（综合情绪）/ nip（冲击）/ simildays（新颖度）/ event_count（量）
- 机动 = M6 spread / M3 新颖度门控 / M8 vec_max
- 全臂过 preflight（VECTOR 自动 vec_* 包裹 + 字段存在性）
- 设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF

## 六、判读预案（探针三分法）

| 读数 | 动作 |
|---|---|
| 任一臂 S≥1.58 且 2Y≥1.58 | 全闸验证 → 与 17 颗篮互相关 → 入篮 |
| S 1.0-1.58 | 不判死：升级窗 W/轴/聚合算子扫描（M10 阶梯） |
| 双结构全 <0.5 | NEWS 事件情绪族免测收窄，转 model238/36（候选 #3/#4） |
