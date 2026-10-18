# IND 字段画像 · 适用模板 · 回测指标（2026-10-18 实测快照）

> **唯一权威数据源** = `data/wqb.db::field_profile_ind`（14 334 字段，9 类 verdict）。
> 查询工具：`tools/fields/field_profile.py`（多区域通用，DEU/GBR 同款）。
> **读法**：§0 速查 → 目标集的三节（① 画像 ② 模板 ③ 指标）→ §4 跨集规律。
> **本文历经两次修正**：① 早先把 `earnings3` 整体当「日期类毒药」跳过 —— 错，`*_interval` 确有画像 ALIVE；
> ② 随后把这两个 ALIVE 当「可直接投产的 ATOM」—— **也错**。深查 44 条历史回测后确认：S 4.49 来自
> `trade_when(ern3_pre_interval < -5, <PV 腿>, ...)`，即 **ern3 只是门控、信号来自别的数据集 ⇒ combined**。
> 独立形态全灭（S −0.77~0.86）。详见 §3 的「二次修正」。**这是「画像 verdict ≠ ATOM 可用」的活样本。**

## §0 十二集速查表

| 数据集 | 类别 | 字段 | cov | 类型 | 画像 verdict | 实测裁决 | 波 |
|---|---|---|---|---|---|---|---|
| `earnings3` | EARNINGS | 8 | 0.709–0.872 | MATRIX×8 | **ALIVE×2 / DEAD×6** | **ATOM 判死**（ALIVE 仅 gate，combined 才有 S 4.49） | — |
| `analyst_consensus` | ANALYST | 2351 | 0.761 | VECTOR 为主 | **ALIVE×7** | **prod 墙 0.73–0.77**（S/2Y/sub 全过） | 248 |
| `analyst_factor_signals` | ANALYST | 62 | 0.611 | **MATRIX×62** | UNTESTED 为主 | ★ **最高优先（未开采）** | 248/249 |
| `analyst_earnings_ibes` | MODEL | 28 | **0.9965** | MATRIX×28 | UNTESTED×28 | 未测（事件遮蔽 PV） | 249 |
| `earnings6` | EARNINGS | 20 | 0.357 | VECTOR×20 | UNUSABLE×20 | 未测（EPS surprise 族） | 249 |
| `analyst_revision_horizons` | MODEL | 1026 | 0.782 | MATRIX 为主 | UNTESTED×874 | 未测（revision 广度） | — |
| `analyst_base_ref` | ANALYST | 14 | 0.441–0.981 | VECTOR×10 MATRIX×4 | UNTESTED×13 | 判死（TO 1.20 爆） | 245 |
| `model68` | MODEL | 4 | 0.782 | VECTOR×4 | UNTESTED×4 | 判死（2Y 塌） | 246 |
| `model207` | INSIDERS | 3 | 0.671 | VECTOR×3 | WEAK×2 / DEAD_STATIC×1 | 判死（TO 0.03 近静态） | 246 |
| `news_sentiment_nlp` | OTHER | 23 | 0.671 | VECTOR×23 | UNTESTED×23 | 判死（TO 1.5 爆） | 247 |
| `pv70` | PV | 33 | 1.000 | VECTOR×33 | UNTESTED×33 | 判死（关系图近静态） | 未发批 |
| `fundamental1` | FUNDAMENTAL | 118 | 0.562–0.563 | VECTOR×118 | **UNUSABLE×118** | 判死（平台画像已判全不可用） | 未发批 |

---

## §1 analyst_base_ref —— 盈利惊喜（实际 vs 预期）

### ① 字段画像

- **类型**：10 VECTOR（需 `vec_avg`）+ 4 MATRIX。
- **覆盖率**：惊喜/预期字段整齐 **0.791**；MATRIX 中 3 个 0.98、1 个 **0.441**（低于 0.5 硬闸）。
- **更新频率**：**财报日驱动**（`reported_actual_value` 是实际报告值）⇒ 事件型脉冲。
- **分布**：连续值；`consensus_surprise_percentage` 已归一化为百分比。
- **可用性**：aCnt 0–73（全库最低拥挤之一），但画像 `n_tests=0`（从未被回测覆盖）。

| 族 | 字段 | cov | aCnt |
|---|---|---|---|
| **惊喜** | `consensus_surprise_percentage` | 0.791 | 67 |
| | `consensus_vs_actual_diff` | 0.791 | 24 |
| **实际值** | `reported_actual_value` | 0.791 | 19 |
| **预期分布** | `consensus_high_estimate` | 0.791 | 17 |
| | `consensus_mean_estimate` | 0.791 | 16 |
| | `consensus_stddev_estimate` | 0.791 | 16 |
| | `consensus_low_estimate` | 0.791 | 10 |
| | `consensus_median_estimate` | 0.791 | 9 |
| **覆盖数** | `num_estimates_consensus` | 0.791 | 14 |

### ② 适用模板

```text
# 惊喜变化（推荐形态：ts_delta 把财报日阶跃摊平）
group_rank(ts_delta(vec_avg(consensus_surprise_percentage), 66), sector)
group_rank(if_else(greater(vec_avg(num_estimates_consensus), 3), ts_delta(vec_avg(consensus_surprise_percentage), 66), 0), sector)

# ⚠ 真惊喜水平 —— 实测 TO 1.20 爆表，仅作对照，勿投产
group_rank(subtract(vec_avg(reported_actual_value), vec_avg(consensus_mean_estimate)), sector)
group_rank(divide(subtract(vec_avg(reported_actual_value), vec_avg(consensus_mean_estimate)), add(abs(vec_avg(consensus_mean_estimate)), 1)), sector)

# 预期区间结构
group_rank(subtract(vec_avg(consensus_high_estimate), vec_avg(consensus_low_estimate)), sector)
```

**要点**：VECTOR 必 `vec_avg`；财报日阶跃类必须 `ts_delta` 包装；
`divide(A, add(abs(B),1))` 是防除零标准式（加常量不违规）。

### ③ 回测结果及指标（wave245 · 10 条 · IND/TOP500/d1/decay4/STATISTICAL/trunc0.08/nanOFF）

| # | 表达式要点 | alpha | S | F | TO | 2Y | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | `ts_delta(surprise_pct,66)` | `O0J59kP1` | 0.05 | 0.01 | 0.1628 | 0.54 | ❌ |
| 2 | 同 1 + `numest>3` | `58jqv906` | 0.55 | 0.17 | 0.3296 | 0.20 | ❌ TO 高 |
| 3 | `ts_delta(vs_actual_diff,66)` | `wp9Je1xY` | −0.03 | — | 0.1647 | 0.38 | ❌ |
| 4 | 同 3 + `numest>3` | `xA1mnQ8J` | **0.60** | 0.19 | 0.3339 | 0.57 | ❌ 最高 |
| 5 | `high − low` | `QPY5QjL5` | 0.41 | 0.08 | **1.1478** | 1.76 | ❌ TO 爆 |
| 6 | `divide(high−low, abs(mean)+1)` | `YPxWAmGl` | 0.36 | 0.06 | **1.1547** | 1.94 | ❌ |
| 7 | `ts_delta(stddev,66)` | `E5VrKbJJ` | 0.33 | 0.10 | 0.0984 | 0.97 | ❌ |
| 8 | `actual − mean` | `P0MX1697` | 0.50 | 0.10 | **1.1971** | 1.99 | ❌ |
| 9 | `divide(actual−mean, abs(mean)+1)` | `mLYxXAkp` | 0.49 | 0.10 | **1.202** | 0.73 | ❌ |
| 10 | `ts_delta(mean,66)` | `omo9Yven` | 0.38 | 0.13 | 0.1661 | 1.36 | ❌ |

**判死依据**：真惊喜 TO 1.20 爆表；惊喜变化 TO 0.16–0.33，比 analyst44 的 `ts_delta`（0.10）高 3 倍。最高 S 0.60。

---

## §2 model68 —— 风险调整动量评分

### ① 字段画像

- **类型**：4 VECTOR（需 `vec_avg`）。cov 整齐 0.782。
- **更新频率**：**低频**（DREAM 模型评分）⇒ 实测 TO 0.16–0.22 印证。
- **分布**：连续评分（`ram`/`score` 已标准化）。⚠ 属「模型评分型」。
- **可用性**：aCnt 32–80；画像 `n_tests=0`（未测过）。

| 字段 | cov | aCnt | 语义 |
|---|---|---|---|
| `mdl68_raw` | 0.782 | 32 | 原始动量评分 |
| `mdl68_mktcap` | 0.782 | 49 | 市值（百万） |
| `mdl68_ram` | 0.782 | 62 | 风险调整动量评分 |
| `mdl68_score` | 0.782 | 80 | 最终标准化评分 |

### ② 适用模板

```text
group_rank(vec_avg(mdl68_ram), sector)                    # 动量水平
group_rank(vec_avg(mdl68_score), sector)
group_rank(ts_delta(vec_avg(mdl68_ram), 66), sector)      # 动量变化
group_rank(subtract(rank(vec_avg(mdl68_ram)), rank(vec_avg(mdl68_mktcap))), sector)  # 同集减，合法
group_rank(divide(vec_avg(mdl68_ram), vec_avg(mdl68_mktcap)), sector)                 # 同集除，合法
group_rank(ts_mean(vec_avg(mdl68_raw), 5), sector)         # 短窗平滑
```

**要点**：低频更新 ⇒ 需 `ts_mean(F,5)`；与市值组合**必须同集**（跨集 = 拼腿违禁）。

### ③ 回测结果及指标（wave246 · 7 条）

| # | 表达式要点 | alpha | S | F | TO | 2Y | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | `ram` 水平 | `rKdrowW3` | 1.02 | 0.50 | 0.1766 | 0.45 | ❌ |
| 2 | `score` 水平 | `58jqw1v6` | 0.97 | 0.47 | 0.1753 | **0.01** | ❌ 2Y 塌 |
| 3 | `ts_delta(ram,66)` | `bl8WLg96` | 0.25 | 0.05 | 0.2187 | −0.23 | ❌ |
| 4 | `ts_delta(score,66)` | `d5Klx6QJ` | 0.28 | 0.06 | 0.2123 | −0.36 | ❌ |
| 5 | `subtract(rank,rank)` | `omo9KXK5` | 1.05 | 0.56 | 0.1627 | 0.35 | ❌ |
| 6 | `divide(ram, mktcap)` | `QPY5aAa5` | **1.09** | 0.55 | 0.1817 | 0.70 | ❌ 最高 |
| 7 | `ts_mean(raw,5)` | `P0MXpbp7` | 0.96 | 0.56 | 0.1004 | 1.08 | ❌ |

**判死依据**：**2Y 全部 0.01–1.08**（阶梯闸必死）+ TO 0.16–0.22 偏高 ⇒ 动量在 IND 无收益锚。

---

## §3 earnings3 —— 财报间隔（⚠ ATOM 判死；只能当 gate）

### ① 字段画像

- **类型**：8 个全 **MATRIX**（可直接 `ts_*`/`rank`，**无需 `vec_avg`**）。
- **覆盖率**：0.709–0.872。
- **更新频率**：财报日驱动。
- **画像 verdict**：`ALIVE×2` / `DEAD×6`。**两个 ALIVE 是「距上次/下次财报的交易日数」，不是时间戳本身**。

| 字段 | cov | n_tests | TO | **S** | **2Y** | **F** | verdict |
|---|---|---|---|---|---|---|---|
| **`ern3_pre_interval`** | 0.872 | 19 | 0.3374 | **4.49** | **1.48** | **3.25** | **ALIVE ★** |
| **`ern3_next_interval`** | 0.709 | 15 | 0.2093 | **3.03** | 1.08 | **1.91** | **ALIVE ★** |
| `ern3_pre_reptime` | 0.872 | 1 | 0.1198 | 0.86 | 0.42 | 0.55 | DEAD |
| `ern3_all_delay_1_pre_interval` | 0.872 | 3 | 0.1124 | 0.58 | 0.35 | 0.24 | DEAD |
| `ern3_all_delay_1_next_reptime` | 0.709 | 2 | 0.3116 | 0.45 | 1.08 | 0.21 | DEAD |
| `ern3_next_reptime` | 0.709 | 2 | 0.1595 | 0.40 | 0.55 | 0.18 | DEAD |
| `ern3_all_delay_1_next_interval` | 0.709 | 1 | 0.1798 | 0.01 | −1.65 | 0.00 | DEAD |
| `ern3_all_delay_1_pre_reptime` | 0.709 | 1 | 0.1699 | −0.20 | 0.20 | −0.05 | DEAD |

**★ 修正说明**：早先版本把 earnings3 整体判为「日期类毒药字段」并跳过，**这是错的**。
`*_interval`（间隔天数）是**连续数值变量**，与 `*_reptime`（时间戳）性质完全不同：
前者有强信号（S 3.03–4.49，F 1.91–3.25），后者确实死（S −0.20–0.86）。
⇒ **判「日期类毒药」必须区分 timestamp 与 interval，不能一刀切。**

**经济锚**：财报间隔 = 距上次财报已过多少天（PEAD 事件时钟）。财报后 1 个月内漂移最强，
间隔天数本身是事件时点的单调代理 ⇒ 属「事件时钟 + 漂移」机制，有锚。

### ② 适用模板

```text
# ⛔ ATOM 形态（单数据集）：实测全灭，勿再发批
group_rank(ern3_pre_interval, sector)          # S -0.59
group_rank(ern3_next_interval, sector)         # S  0.06 / 2Y -1.38
rank(ts_delta(ts_delta(ern3_pre_interval, 5), 5))   # S 0.70 但 TO 0.47 超闸

# ✅ 唯一有效形态 = 择时 gate（combined，非 ATOM 目标，仅供理解机制）
trade_when(less(ern3_pre_interval, -5), <任何 PV 腿>, greater(ern3_pre_interval, -2))
#   ⇒ 财报后 5 日内开仓、临近下次财报前 2 日平仓：本质是「避开财报事件窗」的择时器
```

**要点**：
- **它不是 alpha 源，是 event clock（择时开关）**。作为 gate 能把 PV 腿的 S 从 ~1 推到 4.5，
  但 gate 与被门控腿分属两个数据集 ⇒ **必然 combined**。
- 若将来允许 combined，这是本区最强 gate（S 4.40 那颗已 ACTIVE，prod 0.6842）。
- MATRIX 免 `vec_avg`，TO 0.21–0.34 在 0.4 闸内 —— 这些优点在 ATOM 语境下用不上。

### ③ 回测结果及指标 —— ★★ 二次修正：ALIVE 是 combined 造出来的，ATOM 路线已判死

**决定性的新证据（2026-10-18，查 IND 历史 44 条 ern3 alpha）**：

画像里 `ern3_pre_interval` 的 **S 4.49 / F 3.25 来自这条**：

```text
trade_when(less(ern3_pre_interval, -5),
           rank(multiply(-1, ts_mean(corr_last_trade_price_with_volume, 5))),
           greater(ern3_pre_interval, -2))
# ↑ ern3 只是「何时交易」的门控；真正的信号是 intraday_pv_feats 的 corr_last_trade_price_with_volume
# ⇒ n_ds = 2 ⇒ combined，不是 ATOM
```

同一结构的 S 4.40 那颗 **已经是 ACTIVE**（prod 0.6842 / self 0.6233）。也就是说：
**画像的 4.49 是「ern3 当择时开关」的成绩，不是「ern3 当信号」的成绩。**

**纯单字段形态实测全灭**（同一批 44 条里的对照组）：

| 表达式 | S | F | TO | 2Y |
|---|---|---|---|---|
| `(-1)*rank(ts_delta(ts_delta(ern3_pre_interval, 5), 5))` | 0.70 | 0.24 | **0.4717**（超 0.4 闸） | 1.48 |
| `(-1)*rank(ern3_next_interval)` 族 | 0.56 | 0.20 | 0.19 | −0.38 |
| `(-1)*group_rank(ern3_all_delay_1_pre_interval, subindustry)` | 0.45 | 0.16 | 0.12 | 0.35 |
| `(-1)*rank(ts_decay_linear(ern3_all_delay_1_pre_interval, 10))` | 0.43 | 0.15 | 0.11 | −0.52 |
| `rank(ts_zscore(ern3_pre_interval, 10))` | −0.77 | −0.32 | 0.33 | −0.28 |
| `group_rank(ern3_pre_interval, subindustry)` | −0.59 | −0.24 | 0.12 | −0.82 |
| `group_rank(ern3_next_interval, subindustry)` | 0.06 | 0.01 | 0.18 | −1.38 |

| 指标 | 作为**独立信号** | 作为 **gate**（combined） | IND 闸线 |
|---|---|---|---|
| best S | **0.70**（且 TO 超闸） | 4.49 | ≥1.58 ❌ |
| best F | 0.24 | 3.25 | ≥1.0 ❌ |
| best 2Y | 1.48 | 1.48 | ≥1.58 |
| prod | 未测（不必测） | 0.68（ACTIVE 那颗） | <0.7 |

**裁决**：`earnings3` 的 8 个字段**全部不能做 ATOM**。它是**择时开关数据集**（gate provider），
价值只在 combined 结构里 —— 而 combined 不是本战役交付目标（用户明令只挖 ATOM）。
⇒ **不要再为 earnings3 发 ATOM 波次。**

**★ 方法论教训（比结论更值钱）**：`field_profile_ind` 的 `best_s` 是**骨架无关的最大值**，
画像清洗时用的骨架里**混有跨数据集 `trade_when` 门控形态**。所以
**ALIVE ≠ 该字段能单独出 alpha，只等于「它在某个骨架里能出 alpha」**。
⇒ 读画像前必须先反查达成该 `best_s` 的表达式属于 atom 还是 combined
（查询法：`SELECT expression,sharpe,... FROM alphas WHERE expression LIKE '%<field>%'`）。

---

## §4 model207 —— 内部人交易

### ① 字段画像

- **类型**：3 VECTOR。cov 整齐 0.671。
- **更新频率**：事件型稀疏 ⇒ 画像直接标出 **TO 0.027–0.058（近静态）**。
- **画像 verdict**：`WEAK×2` / `DEAD_STATIC×1`。

| 字段 | cov | n_tests | TO | S | 2Y | verdict |
|---|---|---|---|---|---|---|
| `security_transaction_unit_price_usd` | 0.671 | 11 | 0.058 | 1.40 | 1.70 | WEAK |
| `transactional_share_quantity_change` | 0.671 | 11 | **0.0312** | 1.25 | 1.67 | WEAK |
| `post_transaction_share_balance` | 0.671 | 2 | **0.0272** | 1.19 | 1.48 | **DEAD_STATIC** |

### ② 适用模板

```text
group_rank(vec_avg(transactional_share_quantity_change), sector)
group_rank(ts_mean(vec_avg(transactional_share_quantity_change), 66), sector)   # 累计净买入
```

**要点**：只有 `transactional_share_quantity_change` 有方向性（正=买入）；**TO 0.03 低于 LOW_TURNOVER 闸 0.01 附近 ⇒ 必须 `ts_mean` 聚合**；价格字段无经济锚，勿单独用。

### ③ 回测结果及指标（wave246 · 3 条）

| # | 表达式要点 | alpha | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| 8 | 变动水平 | `XgRYpxpz` | −0.05 | −0.01 | 0.0682 | −0.32 |
| 9 | `ts_mean(变动,66)` | `78oKwr18` | 0.04 | — | 0.0625 | 0.11 |
| 10 | `ts_delta(持股余额,66)` | `O0J5pjZq` | 0.45 | 0.17 | 0.0974 | −0.53 |

**判死依据**：S −0.05–0.45。与画像一致（`DEAD_STATIC`：TO 0.027 过低，无换手）。**我的实测比画像更差**，说明连 `ts_mean` 聚合都不足以救。

---

## §5 news_sentiment_nlp —— 新闻标题情绪

### ① 字段画像

- **类型**：23 VECTOR（需 `vec_avg`）。cov 整齐 0.671。
- **更新频率**：**日频** ⇒ 画像 `n_tests=0`（未测），实测 TO 1.2–1.5 印证事件型。
- **分布**：连续归一化值（VADER / TextBlob / SentiWordNet）✅ 满足 §3 铁律例外条件。
- **可用性**：aCnt 2–9（全库最低拥挤）。

| 族 | 字段 | aCnt |
|---|---|---|
| **复合情绪** | `headline_sentiment_vader_score` | 6 |
| | `headline_textblob_sentiment_score` | 7 |
| | `headline_sentence_sentiment_average` | 2 |
| | `headline_sentence_sentiment_median` | 2 |
| **极性分量** | `headline_sentiwordnet_positive_polarity` | 2 |
| | `headline_sentiwordnet_negative_polarity` | 6 |
| **离散度** | `headline_sentence_sentiment_variance` | 7 |
| **文本特征** | `headline_subjectivity_score` / `headline_word_count_total` | 5 / 6 |

### ② 适用模板

```text
# ⚠ 水平形态 TO 爆表
group_rank(vec_avg(headline_sentiment_vader_score), sector)
# 22 日平滑（TO 0.17 但 S 只剩 0.33）
group_rank(ts_mean(vec_avg(headline_sentiment_vader_score), 22), sector)
group_rank(ts_delta(vec_avg(headline_sentiment_vader_score), 22), sector)
# 净情绪（同集两字段，合规）
group_rank(subtract(vec_avg(headline_sentiwordnet_positive_polarity), vec_avg(headline_sentiwordnet_negative_polarity)), sector)
```

**要点**：日频事件 ⇒ **必 `ts_mean(22)`**，代价是信号被抹掉；文本特征类（词数/可读性）无经济锚。

### ③ 回测结果及指标（wave247 · 10 条）

| # | 表达式要点 | alpha | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| 1 | `vader` 水平 | `j2ed0J6j` | 0.03 | — | **1.4594** | 1.32 |
| 2 | `ts_mean(vader,22)` | `vROJlbNG` | −0.03 | — | 0.1713 | 0.71 |
| 3 | `ts_delta(vader,22)` | `KPmw9p7j` | 0.06 | — | **1.1988** | 1.11 |
| 4 | `textblob` 水平 | `leMRlYj7` | 0.23 | 0.03 | **1.4168** | 0.72 |
| 5 | `ts_mean(textblob,22)` | `2rjnLxlw` | **0.33** | 0.10 | 0.1747 | −0.32 |
| 6 | 净情绪 | `A1QOP5le` | −0.14 | −0.01 | **1.4693** | −0.44 |
| 7 | `sentence_avg` 水平 | `QPY5VA7w` | 0.04 | — | **1.4585** | 1.28 |
| 8 | `ts_mean(sentence_avg,22)` | `rKdrlw5E` | −0.09 | −0.01 | 0.1734 | 0.36 |
| 9 | `subjectivity` 水平 | `YPxW0O5M` | −0.48 | −0.08 | **1.4146** | 0.31 |
| 10 | `ts_mean(variance,22)` | `78oK1rZ5` | −0.12 | −0.02 | 0.1715 | −0.55 |

**判死依据**：水平形态 TO 1.20–1.47 爆表；平滑后 S 仅 0.33。aCnt 2–9 换不来强度。

---

## §6 pv70 —— 实体关联强度（未发批）

### ① 字段画像

- **类型**：33 VECTOR。cov 整齐 **1.000**（全区最高）。aCnt 0–3。
- **分布**：`*_relation` = 股票 ID 列表（**毒药**）；`*_score` = 整数；**`*_score_float` = 归一化连续（唯一可用）**。
- **画像**：`UNTESTED×33`（从未测过）。

**字段三件套规律**（每组都有，只取 `_score_float`）：
`pv70_bbgnews_*`｜`pv70_ibeseps_*`｜`pv70_ibesptg_*`｜`pv70_ibesrec_*`｜`pv70_news_*`｜`entity_*`

### ② 适用模板

```text
# ⚠ 唯一合规形态
group_rank(vec_avg(pv70_ibeseps_score_float), sector)
group_rank(ts_mean(vec_avg(pv70_ibeseps_score_float), 22), sector)
# ⛔ 禁用 *_relation（ID 列表）/ *_score（整数，无连续尾部）
```

### ③ 回测结果及指标

**未发批**。判死依据 = §3 铁律「网络/嵌入型 → 近静态（探针 TO<0.02）」+ §4「码/ID 类毒药」。

---

## §7 fundamental1 —— 高管薪酬（未发批，平台画像已判死）

### ① 字段画像

- **类型**：118 VECTOR。cov **0.562–0.563**（刚过 0.5 硬闸）。
- **画像 verdict**：**`UNUSABLE×118`（全部）** ⇒ 平台侧画像工具已判该集整体不可用。
- **更新频率**：年度披露 ⇒ 近静态。
- **字段主题**（前 50 全是薪酬/董事会，无财务数据）：
  `director_base_salary`｜`annual_bonus_payment`｜`bonus_to_compensation_ratio`｜`compensation_change_percent`｜`equity_linked_compensation_ratio`｜`board_nationality_diversity_ratio`｜`fnd1_board_characteristics_*`

### ② 适用模板

```text
# 若必测，只能用变化类（绝对值类是水平信号，无收益锚）
group_rank(vec_avg(compensation_change_percent), sector)
```

### ③ 回测结果及指标

**未发批**。**画像 `UNUSABLE` 已足以否决**（比我的「暂缓」结论更硬）⇒ 换集时直接跳过，不必再想。

---

## §8 跨集规律

### 8.1 IND 全区画像总览（14 334 字段）

| verdict | 数量 | 占比 |
|---|---|---|
| UNTESTED | 10 770 | 75.1% |
| UNUSABLE | 2 785 | 19.4% |
| AXIS_ONLY | 573 | 4.0% |
| DEAD | 116 | 0.8% |
| **ALIVE** | **54** | 0.4% |
| WEAK | 15 | 0.1% |
| DEAD_TURNOVER | 14 | 0.1% |
| DEAD_STATIC | 7 | 0.05% |

**⇒ 全区仅 69 个字段（ALIVE+WEAK，0.5%）值得投。** 其余 10770 个 UNTESTED 字段里绝大多数已由 §4 的死因清单覆盖。

### 8.2 ALIVE+WEAK 字段的 22 个来源数据集

| 数据集 | 字段数 | maxS | 数据集 | 字段数 | maxS |
|---|---|---|---|---|---|
| `intraday_pv_feats` | 8 | **6.48** | `model238_anlrev` | 1 | 2.59 |
| `model135` | 17 | 3.60 | `model252` | 1 | 2.37 |
| `analyst_consensus` | 7 | 3.25 | `risk68` | 1 | 2.26 |
| `model32` | 6 | 3.31 | `option30` | 1 | 1.94 |
| `institutions6` | 5 | 3.45 | `model36` | 1 | 1.38 |
| `sentiment21` | 4 | 3.01 | `model144` | 2 | 1.59 |
| `news85` | 2 | 3.47 | `model207` | 2 | 1.40 |
| `pv103` | 2 | 4.04 | `analyst45` | 1 | 1.29 |
| `imbalance5` | 2 | 2.81 | `global_seasonal_model` | 1 | 1.16 |
| **`earnings3`** | **2** | **4.49** | `model238` | 1 | 2.59 |

**⚠ 注意**：`analyst44`（546 字段，本次战役主战场）在 ALIVE 名单上**一个都没有**（481 UNTESTED + 65 UNUSABLE）。
但我们已实测拿到唯一达标 ATOM（`zqrj0bzK`，S 1.66 / prod 0.6664）⇒ **画像 UNTESTED 不等于没价值，
只是该字段从未被单字段裸测过（我们用的是 `ts_delta` + 覆盖门控的组合形态）。**

### 8.3 ★ 元教训：低 aCnt ≠ 有信号

三个全库最低拥挤集（`analyst_base_ref` 0–73｜`news_sentiment_nlp` 2–9｜`pv70` 0–3）**实测全部 0 达标**。

> 低拥挤只解决「prod 相关性」，不解决「信号强度」。
> ⇒ **选集优先级 = 「经济锚 > 覆盖率 > 拥挤度」**，不是按 aCnt 排序开炮。

### 8.4 ★ 次教训：先查画像再判死 —— 但别把「画像 ALIVE」当「能出 ATOM」

两层教训，第二层是本轮新踩的坑：

1. **判死前必须查画像**：`earnings3` 曾被我按「日期类毒药」跳过，而画像显示 `ern3_pre_interval` S 4.49。
   指纹（cov/类型/aCnt）只能预筛，不能终判。且「日期类」必须区分 **timestamp（死）** 与 **interval（活）**。
2. **但画像 ALIVE 也不等于「该字段单独能出 alpha」**：同一字段深查 44 条历史回测后发现，
   4.49 来自 `trade_when(ern3_pre_interval < -5, <PV 腿>, ...)` —— **它只是门控，信号来自另一个数据集**。
   独立形态最高 S 0.70 且 TO 超闸。

> ⇒ **画像 verdict 的语义是「在某个骨架里能出分」，不是「单字段能出 alpha」。**
> 读到高 `best_s` 必须反查达成它的表达式属于 atom 还是 combined：
> `SELECT expression, sharpe FROM alphas WHERE expression LIKE '%<field>%' ORDER BY sharpe DESC`。

### 8.5 IND 已验证有效的机制

| 机制 | 代表 | 实测 | 状态 |
|---|---|---|---|
| **分析师预期连续修正** | `anl44_eps_best_eeps_cur_yr` + `ts_delta(66)` + `numest>3` | S 1.66 / prod 0.6664 / self 0.4211 | ✅ **唯一达标 ATOM** |
| 分析师预期水平 z-score | `analyst_consensus.mean_flash_estimate_pretax_annual12` + `ts_zscore(252)` | S 1.62–1.65 / 2Y 3.02–3.16 / **prod 0.7347–0.7672** | ⚠ 强度够，卡 prod |
| ~~财报间隔事件时钟~~ | `ern3_pre_interval` | 独立 S ≤0.70；4.49 系 gate | ❌ **ATOM 判死（§3）** |
| 残差化 | `ts_regression` 家族 | S 2.05–2.87 / prod 0.29–0.51 | ✅ 过闸（但含 `returns` ⇒ combined） |
| 盘口/量价相关 | `intraday_pv_feats.*` | S 3.5–6.48 | 未验 ATOM/PV 空间 prod 拥挤 |

### 8.6 有效机制三要素

1. **连续慢变量**（每日微调，非财报阶跃）
2. **有经济锚**（PEAD / 事件时钟漂移）
3. **TO 适中**（0.01–0.4 闸内，理想 0.10–0.125）
---

# 第二部分 · 财报（earnings）宇宙专章

> **范围界定**：平台 `EARNINGS` 类目在 IND 只有 3 个数据集（`earnings3` / `earnings6` / `earnings11`，共 63 字段）。
> 但「财报机制」的经济实质分布在 6 个数据集里（下表）。做 earnings ATOM 时按本表选，不要只按 category 筛。

| 数据集 | 平台 category | 字段 | cov | alpha_count（拥挤度） | pm | ATOM 裁决 |
|---|---|---|---|---|---|---|
| `analyst_factor_signals` | ANALYST | 62 | 0.611 | **1 731（低）** | **1.4** | ★ **首选** |
| `analyst_earnings_ibes` | MODEL | 28 | **0.9965** | **988（最低）** | 1.2 | ○ 待测 |
| `earnings6` | EARNINGS | 20 | 0.357 | **585（最低）** | 1.1 | ○ 待测（cov 低） |
| `analyst_consensus` | ANALYST | 2351 | 0.761 | 2 518 | **1.4** | ⚠ 强度够、卡 prod |
| `analyst_revision_horizons` | MODEL | 1026 | 0.782 | 4 924 | 1.2 | ○ 待测 |
| `earnings3` | EARNINGS | 8 | 0.791 | 7 751（高） | 1.1 | ❌ 判死（§3） |
| `earnings11` | EARNINGS | 35 | 0.499 | 1 495 | 1.1 | ❌ 画像 7 DEAD / 28 UNUSABLE |

## §9 analyst_factor_signals —— 财报 ATOM 首选集

### ① 字段画像

- **类型**：62 个**全 MATRIX** —— 本区稀有优势：**无需 `vec_avg`，robust 不被摧毁**（`vec_avg` 会把 robust 从 1.02 压到 0.34）。
- **覆盖率**：0.265–0.889；核心修正族 0.87–0.88。
- **拥挤度**：全平台仅 **1 731** 条 alpha（对比 `analyst44` 26 063、`model26` 60 757）⇒ prod 池天然稀疏。
- **金字塔**：ANALYST 类，multiplier **1.4**（本区最高档之一）。
- **画像 verdict**：几乎全 UNTESTED（从未被单字段裸测）。

**字段分四族**（族＝机制，跨族才可能过 self 闸）：

| 族 | 代表字段 | cov | 经济含义 |
|---|---|---|---|
| **修正幅度** | `eps_revision_magnitude` / `revenue_revision_magnitude` | 0.878 | Street 修正幅度（标量化的「修正强度」） |
| **修正变化** | `eps_y1_estimate_change_3mo` / `eps_y2_estimate_change_3mo` / `revenue_y1_estimate_change_3mo` / `eps_q1_estimate_change_1mo` | 0.87 / 0.55–0.64 | 3 个月 / 1 个月的预期变化 |
| **预期趋势** | `eps_estimate_trend_slope_1yr` / `_2yr` / `revenue_estimate_trend_slope_1yr` | 0.31–0.74 | 预测序列斜率 |
| **预期增长** | `eps_y1_cagr_2yr/3yr/4yr/5yr` / `eps_y1_consensus_value` | 0.68–0.86 | FY1 增长 CAGR |
| ~~分歧度~~ | `eps_y1_estimate_coeff_var` / `_skewness` / `_asymmetry` / `eps_surprise_stddev` | 0.37–0.89 | ⛔ IND 已实测「分歧度」无收益锚（wave244 全灭），仅可作**分母/门控** |

### ② 适用模板

```text
# 修正幅度（族1）—— 建议 ts_mean 平滑，事件型否则 TO 偏高
group_rank(ts_mean(ts_backfill(eps_revision_magnitude, 22), 22), sector)
group_rank(ts_mean(ts_backfill(revenue_revision_magnitude, 22), 22), sector)

# 修正强度 ÷ 分歧度（GBR 已验证结构，IND 待验；divide 属放行算子）
signed_power(group_rank(divide(ts_backfill(eps_revision_magnitude, 22),
                              add(ts_mean(ts_backfill(eps_y1_estimate_coeff_var, 22), 55), 0.01)),
                        industry), 3.0)

# 修正变化（族2）
group_rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 22), 22), sector)
group_rank(ts_mean(ts_backfill(revenue_y1_estimate_change_3mo, 22), 22), sector)
group_rank(ts_mean(ts_backfill(eps_y2_estimate_change_3mo, 22), 22), sector)

# 预期趋势（族3）
group_rank(ts_zscore(ts_backfill(eps_estimate_trend_slope_1yr, 22), 252), sector)

# 预期增长（族4）
group_rank(ts_zscore(ts_backfill(eps_y1_cagr_2yr, 22), 252), sector)
```

**要点**：
- **全部 MATRIX ⇒ 不要写 `vec_avg`**（写了反而毁 robust）。
- `*_revision_magnitude` 本身就是「变化量」⇒ 外层再用 `ts_delta` 会变成加速度（未验证），优先 `ts_mean`。
- 族 1–4 是**四个不同机制**，是同一数据集内唯一可能凑出多颗 ATOM 的路径；
  同族内换字段（eps→revenue change_3mo）日收益相关性预计仍高，别指望各出一颗。

### ③ 回测结果及指标

**IND 从未单字段裸测**（画像全 UNTESTED）。可用三段外部证据：

| 证据 | 表达式 | 结果 |
|---|---|---|
| **GBR 同结构**（同集、跨区） | `signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var,55)), industry), 3.0)` | S 1.71 / F 1.09 / TO 0.112 / 2Y 1.78 / **sub 1.15** |
| GBR 幂次网格 | 幂次 1.55–4.0 共 20 档 | S 1.60–1.72，2Y 1.50–1.80 ⇒ **对幂次不敏感，稳健** |
| **IND 残差化**（含 `returns`，combined） | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(eps_y1_estimate_skewness,252), 252, rettype=0))` | S 2.87 / F 2.29 / 2Y 2.66 / **prod 0.5087 / self 0.2970** |

**IND 派发**：wave248（6 条，族 1/2/3 + GBR 结构）。**实测回填**：

| alpha | 表达式骨架 | S | F | TO | 2Y | sub | robust | **prod** | **self** | 裁决 |
|---|---|---|---|---|---|---|---|---|---|---|
| **`LL5gZoLm`** | `signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var,55)), industry), 3.0)` | **1.88** | **1.38** | 0.139 | **2.17** | 1.37 | 1.07 | **0.666** | **0.3115** | ✅ **ATOM #2 全闸通过** |
| `MP0K3vP9` | `group_rank(ts_mean(eps_revision_magnitude, 22), sector)` | 1.92 | 1.48 | 0.078 | 2.42 | 1.20 | 1.09 | **0.8817** | 0.5032 | ❌ 仅卡 prod |
| `0mjerZOv` | `group_rank(ts_mean(eps_y1_estimate_change_3mo, 22), sector)` | 2.07 | 1.66 | 0.080 | 2.31 | 1.14 | 0.99 | **0.8274** | 0.5429 | ❌ prod 爆 + robust 差 0.01 |
| `bl8oO0lq` | `group_rank(ts_mean(revenue_revision_magnitude, 22), sector)` | 0.80 | 0.39 | 0.082 | 2.12 | 0.13 | 0.13 | — | — | ❌ S/sub/robust 全塌 |
| `KPmXrAll` | `group_rank(ts_zscore(eps_estimate_trend_slope_1yr, 252), sector)` | −0.49 | −0.19 | 0.101 | −0.78 | −0.41 | −0.44 | — | — | ❌ 斜率族无信号 |

**★★★ 核心发现：`divide(F, 分歧度)` 是本区第二个已验证的破 prod 杠杆。**
同一 `eps_revision_magnitude`，只加一个「÷ 分歧度」外层：

| 形态 | S | 2Y | **prod** |
|---|---|---|---|
| `group_rank(ts_mean(F,22), sector)` | 1.92 | 2.42 | **0.8817** ❌ |
| `signed_power(group_rank(divide(F, ts_mean(coeff_var,55)), industry), 3.0)` | 1.88 | 2.17 | **0.666** ✅ |

⇒ **prod −0.216，S 只掉 0.04**。机制：除以分歧度改变的是**横截面权重结构**（等价于「按置信度加权」），
不是保序形变，所以能真正改 PnL 路径 —— 这是它和 `signed_power`/`quantile` 那类无效保序形变的本质区别。
**适用前提**：分母必须是**同数据集内**的分歧度字段（跨集即 combined）；分母为无量纲（coeff_var）可加 0.01 保护，
有量纲（`stddev_*`，与分子同币种）则**不要加常数**（会触发 `unitHandling=VERIFY` 单位报错，wave248 已踩）。

**★ 同批副产品**：`group_rank(ts_mean(F,22), sector)` 这种「裸平滑 + 分组」形态在 analyst_factor_signals 上
**S 极强（1.9–2.1）但 prod 恒 0.83–0.88** ⇒ 该形态在本集只能当「强度探针」，不能当交付形态。

**wave250 排除性实测（10 条，全部未过闸）—— 用来划定本集的有效族边界**：

| 字段 | 形态 | S | 2Y | 裁决 |
|---|---|---|---|---|
| `eps_y1_estimate_change_3mo` | ÷coeff_var, **sector** 轴, 幂3 | **2.09** | **1.06** | 仅 2Y 差 0.52（其余全过） |
| 同上 | ÷coeff_var, industry 轴, 幂2 | 1.73 | 1.31 | robust 0.75 |
| `revenue_revision_magnitude` | ÷revenue_y1_coeff_var | 0.65 | 1.48 | ❌ revenue 族无信号 |
| `revenue_y1_estimate_change_3mo` | 同上 | 0.59 | 1.78 | ❌ |
| `revenue_y2_estimate_change_3mo` | 同上 | 0.75 | 0.65 | ❌ |
| `eps_q1_estimate_change_1mo` | ÷coeff_var | 0.85 | 1.66 | ❌ 季度频太噪 |
| `revenue_q1_estimate_change_1mo` | 同上 | 0.54 | 1.06 | ❌ |
| `eps_y1_consensus_value`（增长水平） | ÷coeff_var | 0.27 | 0.28 | ❌ 水平量 |
| `eps_q2_estimate_qoq_growth` | ÷coeff_var | −0.41 | −0.92 | ❌ 增长率水平量 |
| `revenue_y1_cagr_2yr` | ÷coeff_var | −0.71 | −1.36 | ❌ CAGR 水平量 |

> **边界结论（analyst_factor_signals 有效族只有 3 个）**：
> ✅ `eps_revision_magnitude`（修正幅度）、✅ `eps_y2_estimate_change_3mo`（FY2 修正变化）、
> ⚠ `eps_y1_estimate_change_3mo`（S 足够但 2Y 塌）。
> **一切 revenue / 季度频 / 增长水平 / CAGR 字段在本集全部无信号** ⇒ 不要再投。
> 这再一次验证 §8.6「连续慢变量 + PEAD 锚」三要素：revenue 与 growth 缺 PEAD 锚，季度频缺「慢」。

---

## §10 analyst_earnings_ibes —— 事件遮蔽 PV（拥挤度最低）

### ① 字段画像

- **类型**：28 个全 MATRIX。
- **覆盖率**：**0.9688–1.0000**（全 IND 最高档，几乎无缺失）。
- **拥挤度**：**988 条 alpha**（财报宇宙最低）。
- **关键特性**：全部字段带 **event-masked** —— 财报事件窗内该值为 NaN。
  ⇒ `nanHandling=OFF` 时**自动剔除财报日**，等价于「不含财报冲击的价量序列」。
- **字段清单**（7 类 × dlr1/dlr2 双版本）：
  `closing_price` / `opening_price` / `highest_price` / `lowest_price` / `volume_weighted_avg_price` /
  `trading_volume` / `market_capitalization` / `shares_outstanding` /
  `one_day`·`five_day`·`twenty_day`·`sixty_day`·`one_twenty_day`·`two_fifty_day` `_total_return`。

### ② 适用模板

```text
# 日内振幅（低波动异象）—— 比率形态，避免 subtract 两字段
group_rank(-ts_mean(divide(highest_price_dlr1, lowest_price_dlr1), 22), sector)

# 收盘/VWAP 偏离（日内漂移）
group_rank(ts_mean(divide(closing_price_dlr1, volume_weighted_avg_price_dlr1), 22), sector)

# 开收盘缺口（日内反转）
group_rank(-ts_mean(divide(closing_price_dlr1, opening_price_dlr1), 22), sector)

# Amihud 非流动性
group_rank(-ts_zscore(ts_mean(divide(abs(one_day_total_return_dlr1),
                                     add(trading_volume_dlr1, 1)), 22), 252), sector)

# 成交量异象
group_rank(-ts_zscore(ts_mean(trading_volume_dlr1, 22), 252), sector)
```

**要点**：`dlr1` 与 `dlr2` 的描述文字高度重叠（一个写 Americas、一个写 Europe），
**很可能是同一数据的两套延迟版本** ⇒ 视为同一条腿，不要各下一注。

### ③ 回测结果及指标

**完全未测**（画像 28 字段全 UNTESTED，平台 alpha_count 988）。
**风险预判**：字段语义是价量 ⇒ 即使数据集新，**prod 池里价量 alpha 极密**，prod 可能远高于 `analyst_factor_signals`。
若 wave249 显示 prod>0.8，本集直接判死，不再投。

---

## §11 earnings6 / earnings11 / analyst_revision_horizons —— 三个待验或判死集

### ① 字段画像

| 集 | 字段 | 类型 | cov | 关键字段 | 画像 |
|---|---|---|---|---|---|
| `earnings6` | 20 | **VECTOR×20** | 0.351–0.365 | `ern6_actual_eps`、`ern6_estimated_eps`、`preliminary_eps_range_lower/upper_bound`、`eps_change_absolute/percentage_value` | UNUSABLE×20（cov<0.5 触顶） |
| `earnings11` | 35 | VECTOR×35 | 0.499 | `ern11_composite_sentiment_score`、`ern11_event_risk`、`ern11_document_sentiment` | **DEAD×7 / UNUSABLE×28** |
| `analyst_revision_horizons` | 1026 | MATRIX 为主 | 0.782 | `analyst_count_raising_*`、`analyst_count_lowering_*`、`avg_estimate_change_pct_*`、`preferred_earnings_revision_component_short`、`smartestimate_quarterly_eps_medium_2` | UNTESTED×874 |

### ② 适用模板

```text
# earnings6：EPS surprise（⚠ 事件型，TO 必爆；必须平滑）
group_rank(ts_mean(divide(subtract(vec_avg(ern6_actual_eps), vec_avg(ern6_estimated_eps)),
                          add(abs(vec_avg(ern6_estimated_eps)), 0.01)), 22), sector)
group_rank(ts_delta(ts_backfill(vec_avg(eps_change_percentage_value), 22), 66), sector)

# earnings11：情绪水平（⛔ 已判死，勿再发）
# analyst_revision_horizons：修正广度（MATRIX 免 vec_avg）
group_rank(ts_zscore(ts_backfill(analyst_revision_percentile_score_medium_4, 22), 252), sector)
group_rank(ts_delta(ts_backfill(avg_estimate_change_pct_next_year_ebitda_30d_short_4, 22), 66), sector)
```

### ③ 回测结果及指标

| 集 | 证据 | 结果 | 裁决 |
|---|---|---|---|
| `earnings6` | 平台 alpha_count 585、cov 0.357 | 未测 | ○ 低拥挤但 cov 触顶，sub-universe 大概率不足 |
| `earnings11` | 画像 7 次实测 | S 0.15–0.51 / 2Y −0.74~0.19 / TO 0.09–0.20 | ❌ 强度塌，判死 |
| `analyst_revision_horizons` | IND 历史 11 条（全 combined） | S 0.11–2.59，**prod 0.74–0.81** | ⚠ 单字段 ATOM 未测；历史全是 add/divide 双集 ⇒ prod 全爆 |
| 同上（`mdl238_global_rank` 画像） | — | S 2.59 / F 2.88 / TO 0.066 但 **2Y −0.30** | ❌ 2Y 闸死 |

**结论**：财报宇宙的 ATOM 火力应集中在 **`analyst_factor_signals`（首选）→ `earnings6`（赌低拥挤）**；
`analyst_consensus` 只做「prod 破墙」定向攻坚；其余不再投。
