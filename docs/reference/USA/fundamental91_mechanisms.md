# USA · `fundamental91`（8-K 公告文本分析）机制台账

> **S1 阶段产物**（2026-10-29）。字段画像见同目录 `fundamental91_field_profile.md`。
> 数据集选择依据：平台 `recommend_datasets` 在「未点亮塔优先」口径下把本集排为基本面首选；
> 全场拥挤度最低（488 个 alpha / 193 用户 / **270 个字段 `userCount==0`**）。
> 目标塔：**FUNDAMENTAL（USA D1 当前 0/3，未点亮）**。

---

## 0 硬约束（写任何表达式前先过这五条）

| 约束 | 内容 |
|---|---|
| 单数据集（ATOM） | 全部信号字段只能来自 `fundamental91`；**禁止**引入 `returns` / `close` / `adv20` / 其他数据集字段 |
| 分组轴 | 只能用 ATOM 豁免字段：`country` / `exchange` / `market` / `sector` / `industry` / `subindustry` |
| 类型闸 | **407 个字段全部是 VECTOR** ⇒ 必须先 `vec_avg` / `vec_sum` 聚合成标量，否则平台报 `does not support event inputs` |
| 单位闸 | `unit_handling=VERIFY`：比值一律「同单位相除」，**不许**加无量纲 ε |
| 时间窗口 | 只用 `config.STANDARD_WINDOWS` = 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260 |
| 非信号字段 | `fnd91_8k_kic` = SEC Central Index Key（公司标识），**不是信号**，任何表达式都不许用 |

---

## 1 字段分档

### A 层 — coverage 0.866，可直接做尽

| 族 | 字段 | 含义 |
|---|---|---|
| 全套文本统计 | `fnd91_measure_0..4` | 句数 / 音节数 / 复杂词数 / 长词数 / 总词数 |
| 可读性 | `fnd91_readability_0/1/2` | 三个可读性衡量（方向未标注，需实测定号） |
| 数字密度 | `fnd91_numeric_count` | 正文中数字个数 |
| 语气模型 1 | `fnd91_sentiment1_1/2/3` | 正 / 负 / 中性 |
| 语气模型 2 | `fnd91_sentiment1_4/5/6` | 正 / 负 / 中性 |
| 语气模型 3 | `fnd91_sentiment1_7/8/9` | 正 / 负 / 中性 |
| 语气族 2 | `fnd91_sentiment2_0/1` | 正 / 负（另一套词典） |
| 归一化分母 | `fnd91_sentiment1_0`、`fnd91_sentiment2_2` | 过滤后词数（**只作分母，不当信号**） |

### B 层 — coverage 0.64–0.86，主题暴露 `fnd91_topic_0..19`

具名的几条（其余 `topic_<0..20>` 描述未具名）：

| 字段 | 主题 | cov | 拥挤度 |
|---|---|---|---|
| `fnd91_topic_7` | Earnings Results | 0.8597 | 2 用户 / 2 alpha |
| `fnd91_topic_12` | Business Strategy | 0.8487 | 3 / 3 |
| `fnd91_topic_13` | Securities Lending | 0.8327 | 3 / 5 |
| `fnd91_topic_3` | Real Estate | 0.7505 | 2 / 2 |
| `fnd91_topic_14` | **Management Change** | 0.7458 | 6 / 7 |
| `fnd91_topic_17` | Stock Dilution | 0.7199 | 4 / 4 |
| `fnd91_topic_6` | Amendment of Shareholder Rights | 0.7078 | 7 / 7 |
| `fnd91_topic_15` | Healthcare Sector | 0.6967 | 2 / 2 |

### C 层 — coverage 0.30–0.66，逐段文本变量（`cat0..cat13`）

- `catN_primary_sentiment_score{0..8}` — 3 套模型 × 正/负/中性，逐段落
- `catN_secondary_sentiment_score{0,1}` — 另一套词典的正/负
- `catN_section_feature_count{0..3}` — 词性计数
- **`catN_section_metric1_{0,1,2}_value` — 本期该段落文本 vs 上一期的相似度**（仅 `cat6` / `cat10` 有，cov 0.305–0.320）

C 层覆盖偏低，**预期难过覆盖率闸**；但 `section_metric1` 是唯一直接对应 Lazy Prices 的变量，值得单独一颗探针验证是否真被否。

---

## 2 机制目录

> **文献核验状态**：本节文献引用来自模型已有知识，**本轮未能在线核验**（`web_search` 因订阅余额用尽不可用）。
> 机制方向属「先验假设」，最终以回测实证为准；若后续可联网应补核。

### M1 语气净额（Tone）

- **假设**：8-K 正文净语气（正 − 负）越正面，信息含量越偏利好，后续存在漂移。
- **文献**：Loughran & McDonald (2011) 金融词典；Feldman et al. (2010) MD&A 语气变化 → 盈余后漂移。
- **字段**：`fnd91_sentiment1_1 − fnd91_sentiment1_2`（同单位相减，无需 ε）
- **期望方向**：**正**（净语气越正越做多）
- **冒烟判据**：S ≥ 0.9 且 `eff = fitness/sharpe ≥ 0.5` ⇒ 该机制有承载能力，进下一轮骨架优化；否则判死

### M2 可读性（Readability / 模糊化）

- **假设**：公告越难读（句子冗长、词汇生僻），管理层越可能在掩盖坏消息；低可读性预示后续负收益。
- **文献**：Li (2008) 年报可读性与盈余持续性；Rennekamp (2012) 可读性影响投资者反应。
- **字段**：`fnd91_readability_0`（直接用，无需构造比值）
- **期望方向**：**未定** —— 平台未标注该字段是「易读度」还是「难度等级」，方向由探针实测定号
- **冒烟判据**：同 M1；若 `|S| ≥ 0.9` 但方向与 Li(2008) 相反，记录为「平台口径为易读度」并反向复用

### M3 用词复杂度（Long-word ratio）

- **假设**：长词占比高 = 表述复杂/含混，与 M2 同源但更稳（比值化，抗规模）。
- **字段**：`divide(vec_avg(fnd91_measure_3), vec_avg(fnd91_measure_4))`（长词数 ÷ 总词数，同单位约掉）
- **期望方向**：**负**（长词占比高 ⇒ 做空）
- **注**：与 M2 若高度同向，二者只保留信息量更大的一个，避免同族重复提交

### M4 数字密度（Numeric density）

- **假设**：公告里量化信息占比越高，披露越实质、越透明；空话连篇的公告信息含量低。
- **字段**：`divide(vec_avg(fnd91_numeric_count), vec_avg(fnd91_measure_4))`（数字个数 ÷ 总词数）
- **期望方向**：**正**
- **判据**：若与 M1 相关性过高（>0.5），说明只是「语气」的影子变量，降级

### M5 主题暴露异动（Topic shift）

- **假设**：8-K 主题暴露反映当期事件类型。「管理层变动」类披露异常放大预示负面事件。
- **字段**：`ts_zscore(vec_avg(fnd91_topic_14), 504)`（相对自身 2 年历史的异常度）
- **期望方向**：**负**（异常放大 ⇒ 做空）
- **可证伪**：若换成 `topic_7 Earnings Results` 也同号同强，说明是「任何主题都在放大」的机械效应（=公告数量代理），该机制判死

### M6 文本相似度 / Lazy Prices

- **假设**：本期段落文本相对上期改动越大，说明公司在实质修改披露；文献发现在 10-K/10-Q 上「改动越多，后续收益越低」（惰性定价）。
- **文献**：Cohen, Malloy & Nguyen (2020) "Lazy Prices", *Journal of Finance* 75(3)。
- **字段**：`vec_avg(cat6_section_metric1_0_value)`（cov 0.3054）
- **期望方向**：**正**（相似度高 = 惰性 = 做多；改动大 = 做空）
- **已知风险**：cov 0.305 ⇒ 预计 `LOW_SUB_UNIVERSE_SHARPE` / 覆盖率闸会否；若否，记录为「C 层不可用」，Lazy Prices 机制在本数据集上封存

---

## 3 首批探针设计（已派发）

统一骨架，只换信号核，保证可比：

```
group_rank(ts_decay_linear(<信号核>, 66), subindustry)
```

- `ts_decay_linear(...,66)`：8-K 是事件型数据，平台侧已按日铺平；66 日线性衰减 ≈ 一个季度，对应 PEAD 型漂移长度
- `group_rank(..., subindustry)`：子行业内横截面归一（`subindustry` 是 ATOM 豁免分组字段）
- 设置：`USA / TOP3000 / D1 / decay=0 / neutralization=SUBINDUSTRY / truncation=0.08 / maxTrade=OFF / 2014-01-01~2023-12-31`
- **decay=0 的原因**：平滑已在表达式内用 `ts_decay_linear` 显式做，平台 decay 会叠加二次平滑，两者混用后无法归因

| # | 机制 | 探针表达式 | 期望符号 |
|---|---|---|---|
| 1 | M1 语气净额 | `group_rank(ts_decay_linear(subtract(vec_avg(fnd91_sentiment1_1), vec_avg(fnd91_sentiment1_2)), 66), subindustry)` | + |
| 2 | M2 可读性 | `group_rank(ts_decay_linear(vec_avg(fnd91_readability_0), 66), subindustry)` | 待定 |
| 3 | M3 长词占比 | `reverse(group_rank(ts_decay_linear(divide(vec_avg(fnd91_measure_3), vec_avg(fnd91_measure_4)), 66), subindustry))` | − |
| 4 | M4 数字密度 | `group_rank(ts_decay_linear(divide(vec_avg(fnd91_numeric_count), vec_avg(fnd91_measure_4)), 66), subindustry)` | + |
| 5 | M5 主题异动 | `reverse(group_rank(ts_decay_linear(ts_zscore(vec_avg(fnd91_topic_14), 504), 66), subindustry))` | − |
| 6 | M6 文本相似度 | `group_rank(ts_decay_linear(vec_avg(cat6_section_metric1_0_value), 66), subindustry)` | + |

---

## 4 判读规则（先算 eff，再决定下一批测什么）

平台 `fitness = sharpe × sqrt(|returns| / max(turnover, 0.125))`，故 **`eff = fitness / sharpe = sqrt(R/TO)`** 是独立于 Sharpe 的第二条轴。

| eff 档 | S 档 | 判读 | 下一批动作 |
|---|---|---|---|
| ≥ 0.8 | 不够 | 信号有收益承载能力，瓶颈在骨架 | 扫同位置等价算子（`ts_rank` / `ts_decay_linear` / `winsorize` / `signed_power` / `quantile`）+ 窗口微调 |
| ≥ 0.8 | 已够 | 候选 | 进六步闸（`failed_ra_count` → `invest_S/S` → prod → self） |
| 低（≈0.1–0.2） | 任意 | 字段本身没有收益承载能力 | **换字段/换机制**，不要继续扫骨架 |
| 中（0.3–0.6） | 任意 | 信号弱但非空 | 换聚合口径（`vec_sum` / `vec_max`）+ 换归一化分母，最多两轮 |

**追加硬闸**：`invest_S / S ≥ 0.70`（USA 实测口径）。低换手 + 内部价差是已实证的通用解
（`xAdL5vmN`：`ai_equity_alpha`、TO 6.06%、S4.51、invest 达标；`zqrgna91`/`N1eLE1de`：TO 14–16%、invest 比 0.95–1.01）。

---

## 5 待补（下一轮 S1 深化）

1. **向量维度语义未定**：`vec_avg` vs `vec_sum` 的差别有多大，首批只用 `vec_avg`，第二轮对比 `vec_sum` / `vec_max`
2. **`cat0..cat13` 的 14 个类别未映射到具体 8-K item 编号**（2.02 财报、5.02 高管变动、1.01 重大协议…）：数据集描述未给出映射表，需靠「哪个 cat 的 `section_metric1` 覆盖最高」反推，或查平台文档
3. **十年跨度未验**：探针出结果后立刻跑 `get_alpha_yearly_stats`，逐年看 `longCount` / `pnl`，确认 2014 起有数据（**不要**用 `get_datasets` 的 coverage 代替）
4. **`sentiment21`（备选，SENTIMENT 塔，乘数 1.4）**：258 个 MATRIX 字段、cov 0.9994、253/258 字段 alphaCount ≤50。画像已完成（`sentiment21_field_profile.md`），机制待起草
