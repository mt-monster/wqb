# DEU ATOM 战役 — 段台账：PS-VAL-B 判死归因 + NEWS17 开波

日期：2026-11-10
region=DEU / universe=TOP500 / delay=1 / neutralization=SUBINDUSTRY / decay=4 / truncation=0.08

---

## 一、PS-VAL-B 判死（批次 `4gBCNg2Ca4vmagb16jNKLKFt`，10/10 COMPLETE，10/10 REJECT）

复合几何（3 腿 rank add + bucket 中性化 / 双视界 delta 乘积 / multiply 交互 / subindustry 对照），天花板 **S 0.89**。

| alpha | 结构 | S | F | 2Y | sub_u | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| WjOJ8Kdx | `ep_yield f12m ts_mean5 + ts_av_diff(ep_yield fy1, 66)` 双视界 | **0.89** | **0.53** | −0.63 | 0.41 | 0.1042 | 0.000852 |
| ZYQNGkxQ | `multiply(rank(预期差), rank(ep_yield 22))` | **0.79** | 0.45 | 0.54 | 0.38 | 0.0617 | **0.001321** |
| A1VEKqbg | `multiply(rank(ts_delta(iv_forward,66)), rank(ts_delta(iv_forward,22)))` | **0.79** | 0.40 | 0.73 | 0.47 | 0.1494 | 0.000519 |
| akKGvXl2 | 4 腿：预期差+ep_yield+iv_pe ts_rank+ep_yield66 delta，sector | 0.69 | 0.36 | −0.05 | 0.21 | 0.1080 | 0.000635 |
| 2rAedPZP | 3 腿（同上去 4 腿）@subindustry | 0.60 | 0.30 | 0.32 | 0.30 | 0.0777 | 0.000823 |
| 6XdNOg3J | 3 腿 @`bucket(rank(ep_yield 252), "0,1,0.05")` | 0.53 | 0.25 | **1.64** | 0.32 | 0.1128 | 0.000496 |
| Xg9M6XLm | 2 腿（预期差+ep_yield）@同 bucket | 0.47 | 0.21 | 1.27 | 0.30 | 0.0977 | 0.000530 |
| 1YN0E6mX | 3 腿（预期差+ep_yield+rel_val_book）@bucket | 0.34 | 0.13 | 1.35 | 0.24 | 0.0862 | 0.000435 |
| leA1XJze | `iv_pe ts_rank252 + ep_yield 22` 两腿 | 0.32 | 0.11 | −0.45 | 0.27 | 0.0852 | 0.000370 |
| vR1Pgazd | `ep_yield 22 − (forward_pe/iv_pe)` rank 差 | 0.24 | 0.09 | −0.47 | −0.04 | 0.0941 | 0.000341 |

**判死结论**：`iv_* / rel_val_* / forward_pe_* / ep_yield_* / recommendation_*` 五大估值族在**复合几何**下天花板仍仅 0.89，距 1.58 资格线差 0.69。
预测性 starmine 的剩余三族 `actual_last_* / eq_vr_dlra* / days_since_last_report_*` 优先级下调（同数据集同信息域，预期同档）。

---

## 二、★★★ 方法论修正：上一段「简单几何系统性低估数据集潜力」是**部分错误**的

### 2.1 实测增益量级：复合几何是**加性 +0.2~0.4**，不是乘性

| 同一族 | 简单几何最佳（PS-VAL-A） | 复合几何最佳（PS-VAL-B） | ΔS |
|---|---:|---:|---:|
| 预期差 `iv_forward − iv_market` | 0.67（E56xXnGP） | 0.79（ZYQNGkxQ） | **+0.12** |
| `ep_yield` 水平 | 0.53（6XdNv6rP） | 0.89（WjOJ8Kdx 双视界） | **+0.36** |
| `iv_warranted_f12m_pe` | 0.40（leA1bwjl） | 0.32（leA1XJze 两腿） | **−0.08** |
| 3 腿估值复合 | — | 0.53 / 0.60 / 0.69 | — |
| 双视界 delta 乘积 | — | 0.79（A1VEKqbg） | — |

**结论**：复合几何把 0.5–0.7 的族推到 0.8–0.9，**推不过 1.58**。它没有「解锁」能力，只有「增幅」能力。

### 2.2 真正的解释：增益取决于**腿之间的信息独立性**，不是腿的数量

- **同维度重复无增益**：`ep_yield` / `forward_pe` / `iv_warranted_pe` / `rel_val_book` **四个字段都在测「贵不贵」同一个维度**。四者组腿 = 同信息重复平均 ≈ 单腿平滑，天花板锁在 0.89。
  - 证据：6XdNOg3J（3 腿 @bucket）0.53 **低于** WjOJ8Kdx（单族双视界）0.89。加腿反而降 S。
- **独立维度才有乘性增益**：已交付 QPvzNNGG / LLMzYrZe 的腿是
  `mean_estimate_change_pct_*`（分析师修正 **方向**）× `predicted_surprise_*`（实际 vs 预期 **超预期幅度**）
  —— 这是**两个不同信息源**，不是同一维度的两个度量 → 2 腿 add 即达 1.61–1.70。

### 2.3 与既有记忆的一致性

本结论与既有条「双数据集组腿是稀释而非增益：强腿 1.61 + 次强腿 1.18 → 合成 S≈0」**同构**：
组腿增益的必要条件是**信息独立**，与腿的强度阈值是第二位的。
⇒ 修正后的选腿判据：**先问「这两条腿回答的是不是同一个问题」，再问「各自强度够不够」。**

### 2.4 对「容量」的直接推论

predictive_starmine 631 字段里，**只有 `mean_estimate_change_* × predicted_surprise_*` 这一个独立信息维度**。
该维度已被 QPvzNNGG（3 腿）与 LLMzYrZe（2 腿）占用，两者 self 0.678，**共用同一对腿**。
⇒ 按既有判据「只有字段集合不相交才算新颗」，**PS 第 3 颗 ATOM 不成立**，容量锁死 2 颗。

---

## 三、NEWS17 开波（批次 `2ctx6V6Du4QeahY1869LMjcq`，在飞）

### 3.1 为什么选 news17

- cov `multiple_comp` 族 **0.9323**（全 DEU 剩余未测数据集中最高），单实体族 0.6489。
- 48 个字段全 VECTOR，情绪分类器结构完整（acb/bee/ber/qcm/qep/qmb/bam/ssc/nip/event_sentiment_score）+ 三个**结构性元字段**：`relevance`(0-100) / `event_similarity_days`(0-365) / `rp_story_event_count`。
- NEWS 不在禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL}，单数据集 ATOM 不占两塔配额。

### 3.2 论坛模板来源（已读原文）

**帖①《新闻情绪因子:别再用裸 sentiment 了 —— relevance 加权 + 新颖度过滤》**（作者 WL27618，31 赞，`article_id=42659817284375`）
以 news20 为例给出 3 套路 + 1 进阶，与 news17 字段一一对应：

| 帖子套路 | news20 字段 | news17 等价字段 | 采用模板 |
|---|---|---|---|
| 套路一 relevance 加权（低相关性=噪声） | `nws20_relevance` | `nws17_multiple_comp_relevance` 0.9323 | T1 |
| 套路二 新颖度（相似事件越久远 → 新信息越多） | `nws20_event_similarity_days` | `nws17_multiple_comp_event_similarity_days` 0.9323 | T2 |
| 套路三 情绪动量（变化优于水平，配 decay） | `nws20_ghc_lna` | `nws17_multiple_comp_ssc` 差分 | T3 |
| 进阶 Story Attention Dilution（故事里实体越多，单票注意力被摊薄） | `rp_story_event_count` | `nws17_multiple_comp_rp_story_event_count` 0.9323 | T5 |
| 进阶 Entity-Story Deviation（单实体 vs 聚合偏离） | 单实体 vs `multiple_comp` | `nws17_ssc` vs `nws17_multiple_comp_ssc` | T4 |
| 进阶 Next-Day Confirmation（短长窗同向才强） | — | 同上 | T10 |
| 多分类器平均 | `(acb+bam+bee+ber+qcm+qep+qmb)/9` | 同族齐备 | T6 |

**帖②《Data Idea系列3：Global News Data_news48》**（WL13229，16 赞）：`(acb+bam+bee+ber+qcm+qep+qmb)/9` 多分类器综合 → T6 依据。
**帖③《【Alpha模板】情绪数据中用 ts_covariance 构建 alpha 模板》**（RM49262，52 赞 29 评）：明确「**days 较短时跑出的 alpha 结果都比较一般**」⇒ 不用 1–3 日短窗做主体，最小窗取 5，主体 22/66。
**帖④《【Alpha Idea】给信号标保质期——新闻情绪字段的时效性分级与短窗模板》**（YQ11169）：短窗模板 `group_rank(ts_mean(vec_avg(composite_sentiment_score_2), 5), industry)`。

### 3.3 本波 10 个模板（结构互异，非换参数）

| # | 骨架类型 | 表达式核心 | 算子数 | 来源 |
|---|---|---|---:|---|
| T1 | **权重乘性**（线性 relevance 加权） | `ts_mean(multiply(rank(vec_avg(ssc)), rank(vec_avg(relevance))), 22)` | 7 | 帖①套路一 |
| T2 | **权重乘性**（新颖度加权） | `ts_mean(multiply(rank(vec_avg(ssc)), rank(vec_avg(event_similarity_days))), 22)` | 7 | 帖①套路二 |
| T3 | **一阶差分 + 线性衰减** | `ts_decay_linear(ts_av_diff(vec_avg(ssc), 66), 5)` | 4 | 帖①套路三 |
| T4 | **截面偏离**（单实体 − 聚合） | `ts_mean(subtract(rank(vec_avg(nws17_ssc)), rank(vec_avg(multiple_comp_ssc))), 22)` | 7 | 帖①进阶 |
| T5 | **比值稀释**（注意力摊薄） | `ts_mean(divide(rank(vec_avg(ssc)), add(rank(vec_avg(rp_story_event_count)), 1)), 22)` | 8 | 帖①进阶 |
| T6 | **同机制多腿 rank add**（3 分类器） | `ts_mean(add(add(rank(vec_avg(acb)), rank(vec_avg(bee))), rank(vec_avg(ber))), 22)` | 10 | 帖② |
| T7 | **双视界差分乘积** | `multiply(rank(ts_delta(vec_avg(ssc),66)), rank(ts_delta(vec_avg(ssc),22)))` | 8 | DEU 已验证（MPY9VNY9 骨架） |
| T8 | **双条件 rank multiply**（影响 × 情绪） | `ts_mean(multiply(rank(vec_avg(nip)), rank(vec_avg(event_sentiment_score))), 22)` | 7 | 自建（nip=nws17 独有 2h 影响分） |
| T9 | **二阶矩**（情绪分歧度） | `ts_std_dev(vec_avg(qep), 22)` | 3 | 自建（分歧 ≠ 水平，独立维度） |
| T10 | **双视界水平 add**（昨日确认） | `add(rank(ts_mean(vec_avg(ssc),5)), rank(ts_mean(vec_avg(ssc),22)))` | 8 | 帖①进阶 |

**未派发（备批）**：
- T11 非线性权重：`ts_mean(multiply(rank(vec_avg(ssc)), signed_power(rank(vec_avg(relevance)), 2)), 22)` —— 等价「只在 relevance 高分段取情绪」，用平方替代被禁的比较算子门控。
- T12 三权重乘积：`ts_mean(multiply(multiply(rank(ssc), rank(relevance)), rank(event_similarity_days)), 22)`。

### 3.4 预检

`valid=true` / `unknown_fields=[]` / `unknown_soft=[]` / `any_changed=false` / `platform_field_count=10`。
唯一 warning：`nws17_multiple_comp_rp_story_event_count: get_datafields(offset=50): failed after 6 attempts`
⇒ **预检自身分页超时假阳性**（该字段在先前 `get_datafields` 返回中已确认存在，cov 0.9323），不阻塞派发。

### 3.5 设计守则（本波新增）

- 所有参与算术的腿**先 `rank()` 再运算**：`event_similarity_days` 带 Day 量纲、`relevance` 0–100，直接相乘/相除可能触发 `unitHandling=VERIFY` 单位不兼容；rank 后一律无量纲。
- `trade_when` 门控（帖①「只在 relevance>60 取情绪」）本波**未用比较算子**，改用 `signed_power` 平方加权替代（T11），规避 `greater` 算子可用性未验证的风险。
- 无 `ts_entropy` / `ts_skewness` / `ts_percentage` / `ts_decay_exp_window`（DEU 幽灵算子黑名单）。
- 无 `ts_max`（toolkit 静态门禁 `INACCESSIBLE_OP`）。

---

## 四、本轮判死累计（截至本段）

| # | 数据集 | 批次 | 几何数 | 天花板 S | 关键副产物 |
|---|---|---|---:|---:|---|
| 1 | model264 | DzD2ZaAZ4 / 44kQhGalN | 20 | 0.66 | `_class` 作 bucket 分组轴合法写法 |
| 2 | shortinterest3（loan rate 族） | 4qpqEGfWo | 10 | 0.68 | `_p5_d1` 是慢变量 TO 0.06 |
| 3 | model28 | 1nl9I45WQ | 10 | 0.74 | 单腿 0.10 → 双 rank multiply 0.74（7.4×） |
| 4 | predictive_starmine（估值 5 族） | 1DJDST7Uo | 10 | 0.67 | 预期差 2Y 1.33 |
| 5 | predictive_starmine（估值 5 族，复合） | 4gBCNg2Ca | 10 | **0.89** | **复合几何=加性增幅，非解锁** |
| 6 | insider_agg_matrix | 3cueYzcqh | 10 | 0.46 | 稀疏披露 → 截面 rank 差 TO>1.0 |

**活着的出货数据集**：`sentiment7` / `sentiment27` / `predictive_starmine`（容量锁 2）/ `shortinterest3`（容量锁 1）。

---

## 五、NEWS17-A 判死（批次 `2ctx6V6Du4QeahY1869LMjcq`，10/10 COMPLETE，10/10 REJECT）

天花板 **S 0.53**，最佳 F **0.22**。**这是本段第二次用论坛配方打高覆盖数据集而全灭。**

| # | 模板 | alpha | S | F | 2Y | sub_u | TO | drawdown |
|---|---|---|---:|---:|---:|---:|---:|---:|
| T8 | `nip × event_sentiment_score` 双条件 multiply | 9qxk0kRV | **0.53** | **0.22** | −0.46 | 0.07 | 0.1670 | 0.1128 |
| T4 | 单实体 `nws17_ssc` − 聚合 `multiple_comp_ssc` 偏离 | P0oK9KvK | **0.44** | 0.18 | 0.33 | **1.02** | 0.1674 | 0.1668 |
| T2 | 新颖度加权 `ssc × event_similarity_days` | A1VEKEkg | 0.33 | 0.11 | −0.08 | 0.09 | 0.1684 | 0.1026 |
| T10 | 5d + 22d 双视界水平 add | j2YOmOZQ | 0.28 | 0.06 | 0.24 | −0.06 | 0.3305 | 0.2266 |
| T6 | 3 分类器 (acb+bee+ber) 多腿 add | j2YOmOgQ | 0.20 | 0.06 | 0.59 | −0.03 | 0.1323 | 0.1506 |
| T7 | 双视界 delta (66/22) 乘积 | A1VEKE3g | 0.19 | 0.02 | 0.46 | 0.11 | **1.1556** | 0.2810 |
| T3 | `ts_decay_linear(ts_av_diff(ssc,66),5)` 动量 | O0Agago7 | 0.14 | 0.01 | 0.82 | 0.04 | **0.9867** | 0.3259 |
| T5 | 注意力稀释 `ssc / (story_event_count+1)` | MPYVmVkr | −0.03 | −0.00 | −0.37 | −0.59 | 0.1396 | 0.1729 |
| T1 | relevance 线性加权 `ssc × relevance` | akKGvGN5 | **−0.06** | −0.01 | −0.64 | −0.37 | 0.1400 | 0.1193 |
| T9 | 情绪分歧度 `ts_std_dev(qep,22)` | MPYVmVxr | −0.23 | −0.06 | −0.62 | −0.01 | 0.1625 | 0.2643 |

### 5.1 ★ 论坛配方在 DEU 全部失效——逐条反证

| 论坛主张（帖①WL27618，31 赞） | DEU 实测 | 结论 |
|---|---|---|
| relevance 加权「信噪比显著提升，漂移更持久」 | **S −0.06**（全波最差） | ✗ 反向失效 |
| 新颖度 `event_similarity_days × sentiment` 「多一个信息新鲜度维度」 | S 0.33 / 2Y −0.08 | ✗ 无增益 |
| 情绪动量 `ghc_lna` + decay「天生高换手，配合衰减更佳」 | S 0.14 / **TO 0.9867** / **drawdown 0.3259** | ✗ 高换手且无收益 |
| Story Attention Dilution「实体越多情绪冲击越弱」 | **S −0.03** | ✗ 无效应 |
| 多分类器平均 `(acb+bee+ber+...)/n` | S 0.20 | ✗ 弱 |
| Entity-Story Deviation「独立信息」 | S 0.44 / **sub_u 1.02（全波最佳子宇宙项）** | △ 唯一有边际信息的模板 |
| 多公司聚合族「覆盖率 0.96 是宝藏」 | cov 0.9323 实测 S 0.06–0.53 | ✗ **覆盖率不携带信号** |
| 双视界 delta 乘积（DEU 自验证骨架） | S 0.19 / **TO 1.1556** | ✗ 新闻是脉冲型，差分即噪声放大 |

### 5.2 ★★ 新判据：脉冲型数据不能用差分/动量类几何

`ssc` 类新闻情绪是**事件脉冲**（某日有新闻→大幅跳变，无新闻→回 0/NaN）。
任何 `ts_delta` / `ts_av_diff` / `ts_decay_linear(差分)` 都会把「当日是否恰好有新闻」的伯努利噪声放大成主信号：
- T3（动量）TO **0.9867**、drawdown **0.3259**
- T7（双视界 delta 乘积）TO **1.1556**、drawdown **0.2810**
- 两条 S 均 ≤0.19

对照：MPY9VNY9 用同样双视界 delta 乘积骨架在 `shrt3_bar` 上得 S1.59 —— 因为 `shrt3_bar` 是**连续慢变量**（借券成本），差分有意义。
⇒ **判据：先辨字段是「脉冲型」还是「慢变量型」，再决定是否允许差分类算子。**
脉冲型（新闻情绪 / 披露计数 / 事件）→ 只能用水平类 + 长窗平滑 + 加权；
慢变量型（借券费率 / 模型分 / 财务比率）→ 差分 / delta 乘积可放大。

### 5.3 覆盖率与信号强度第三次证伪

- news17 `multiple_comp` cov **0.9323**（全 DEU 最高）→ S 天花板 **0.53**
- predictive_starmine cov 0.60 级 → S **1.70**（已交付）
- shortinterest3 `_p5_d1` cov 0.78 → S **0.68**
- sentiment7/sentiment27 → S **2.05**（已交付）

**相关系数约等于 0，甚至轻微负相关。覆盖率彻底不可作信号质量先验，只能作「防空窗」下限筛。**

---

## 六、MODEL250（MALTA ML）开波（批次 `36XQQyNj4GD8Hn1fVlIuvcn`，在飞）

### 6.1 为什么这是剩余最佳候选

20 字段，cov 0.5366–0.5556（sector 1.0），**5 个信息维度彼此正直交**：

| 维度 | 字段 | cov | uc/ac |
|---|---|---:|---|
| 复合 alpha 分（主模型） | `mdl250_malta_eq_score` | 0.5556 | 45/48 |
| 复合 alpha 分（hc 变体） | `mdl250_maltahc_eq_score` | 0.5556 | 25/28 |
| 复合分（lmt close/open） | `mdl250_lmt_close_eq_score` / `_lmt_open_eq_score` | 0.5366 | 6/7、4/5 |
| **短期 2–3 日** | `mdl250_eq_short` / `mdl250_hc_eq_short` | 0.5556 | 7/7、1/1 |
| **中期 1–4 周** | `mdl250_eq_medium` / `mdl250_hc_eq_medium` | 0.5556 | 6/6、13/13 |
| **防御 overlay** | `mdl250_eq_hedge` / `mdl250_hc_eq_hedge` | 0.5556 | 4/4、3/3 |
| **季节性** | `mdl250_eq_seasonality` / `mdl250_hc_eq_seasonality` | 0.5556 | 14/15、**27/33** |
| group 轴 | `mdl250_*_sector` ×4 | 1.0 | 仅分组 |

**与 PS-VAL 的关键区别**（按本台账 2.2 判据）：PS 的四腿全测「贵不贵」同一维度；model250 的 `composite / short / medium / hedge / seasonality` 是**五个回答不同问题的维度** ⇒ 满足组腿增益的必要条件。

### 6.2 本波 10 模板（结构互异）

| # | 骨架类型 | 表达式核心 | 算子数 |
|---|---|---|---:|
| T1 | 双模型一致 rank add | `add(rank(malta_eq_score), rank(maltahc_eq_score))` | 4 |
| T2 | **期限结构**（短 − 中） | `subtract(rank(eq_short), rank(eq_medium))` | 4 |
| T3 | **非线性尾部强调**（三次方） | `signed_power(rank(malta_eq_score), 3)` | 4 |
| T4 | 模型分一阶差分（动量） | `ts_av_diff(malta_eq_score, 22)` | 3 |
| T5 | 季节性强弱（独立轴水平） | `ts_mean(hc_eq_seasonality, 22)` | 3 |
| T6 | **防御 overlay 双条件 multiply** | `multiply(rank(eq_hedge), rank(eq_medium))` | 4 |
| T7 | 主信号 × 季节性正交交互 | `multiply(rank(malta_eq_score), rank(hc_eq_seasonality))` | 4 |
| T8 | 双视界 delta (66/22) 乘积 | `multiply(rank(ts_delta(malta,66)), rank(ts_delta(malta,22)))` | 8 |
| T9 | **双模型分歧**（意见不一致） | `subtract(rank(malta), rank(maltahc))` | 4 |
| T10 | **截面 vs 时序双轴背离** | `subtract(rank(malta), ts_rank(malta, 252))` | 4 |

T1 与 T9 用同一对字段但方向相反（一致 vs 分歧），T2 与 T6 共用 `eq_medium` 但一问「期限」一问「防御」。
算子数全部 ≤8，远低于上限 12。
注：T8 允许使用差分——`mdl250_*_score` 是**每日重算的连续慢变量**（按 5.2 判据合法），与 news17 的脉冲型字段性质不同。

### 6.3 禁混合规

model250 属 MODEL 类（禁混集合内），但本波**全部为单数据集 ATOM，无任何组腿** ⇒ 不触发任何两塔约束。MODEL 塔当前已提交 1 颗（<3 未点亮），符合「已点亮塔不选」。

---

## 七、★★★ MODEL250 Wave A 结果（批次 `36XQQyNj4GD8Hn1fVlIuvcn`）——8 批判死后首个正信号集

**12/18 进入 prescreen REVIEW（其余 6 批全 REJECT）**。所有 REVIEW 件 `failed_ra_count=2`，即**只卡 LOW_SHARPE + LOW_2Y_SHARPE 两个闸**，其余全 PASS。

### 7.1 Wave A 全表（10/10 COMPLETE，4 REVIEW / 6 REJECT）

| # | 模板 | alpha | S | F | 2Y | sub_u | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| T7 | 复合分 × 季节性 multiply | vR1PVaAQ | **1.35** | 1.32 | 0.39 | 0.83 | 0.1175 | 0.002041 |
| T1 | 双模型一致 rank add | ZYQNLkm8 | 1.29 | 1.24 | 0.07 | 0.85 | 0.1064 | 0.002173 |
| T5 | 季节性强弱 ts_mean 22 | npvrbwa3 | 1.24 | 1.16 | **0.90** | 0.87 | **0.0574** | **0.003794** |
| T3 | 复合分 signed_power 3 | RREPL0Ez | 1.14 | 0.98 | −0.23 | 0.60 | 0.1309 | 0.001484 |
| T6 | 防御 × 中期 multiply | E56xAoQm | 0.95 | 0.74 | 0.42 | 0.67 | 0.1320 | 0.001198 |
| T8 | 双视界 delta (66/22) 乘积 | ZYQNLkXZ | 0.63 | 0.31 | −1.13 | 0.14 | 0.1987 | 0.000486 |
| T4 | 复合分一阶差分 22 | JjerLR8l | 0.52 | 0.21 | −0.84 | 0.08 | 0.2357 | 0.000335 |
| T10 | 截面 vs 时序双轴背离 | j2YOQNVo | 0.27 | 0.11 | **0.88** | 0.24 | 0.1307 | 0.000329 |
| T9 | 双模型分歧 | 0mY5WnG8 | −0.15 | −0.04 | −0.88 | −0.52 | 0.1740 | −0.000132 |
| T2 | 期限结构（短 − 中） | j2YOQNYZ | −0.52 | −0.27 | −0.77 | −0.69 | 0.1532 | −0.000548 |

### 7.2 ★ 新判据（第三次同型）：z-score 标准化的字段**不能做差分**

`mdl250_*_score` 是每日截面 z-score（`daily cross-sectional z-score`）。
T4（`ts_av_diff` 22）= S 0.52 / 2Y −0.84；T8（双视界 delta 乘积）= S 0.63 / 2Y **−1.13**；T9（两 z-score 相减）= −0.15。
⇒ 对已标准化字段取差分，等价于对「标准化分母的日间跳动」建模，信号被噪声吞掉。

**统一判据（合并 NEWS17 与 model250 两处实证）**：
| 字段性质 | 可否差分 | 例证 |
|---|---|---|
| 脉冲型（事件驱动，多数日为空/0） | ✗ 禁用 | news17 `ssc`：T3 TO 0.99、T7 TO 1.16 |
| 已截面标准化（z-score 类 ML 输出） | ✗ 禁用 | model250：T8 2Y −1.13 |
| 连续慢变量（原始水平量） | ✓ 可放大 | shortinterest3 `shrt3_bar` → S1.59 |

### 7.3 Wave B 结果（批次 `2EvAvT9pM4GEbD3WSOpcPyR`，8 REVIEW / 2 REJECT）

| # | 模板 | alpha | S | F | 2Y | sub_u | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| B6 | 季节性两族 + 复合分 add | Xg9MEaN5 | **1.37** | **1.35** | 0.54 | 0.85 | 0.1240 | 0.001957 |
| B7 | 季节性两族 × 复合分 | 2rAek5GZ | 1.35 | 1.31 | 0.36 | 0.79 | 0.1242 | 0.001906 |
| B4 | 季节性 × 中期 | P0oKE55L | 1.32 | 1.30 | 0.94 | **0.96** | 0.1149 | 0.002114 |
| B10 | 季节性 × 防御 × 中期 | 9qxkQlGx | 1.32 | 1.25 | 0.62 | 0.93 | 0.1221 | 0.001836 |
| B1 | 季节性双族 add | 9qxkQll9 | 1.28 | 1.23 | 0.66 | 0.78 | 0.1229 | 0.001867 |
| B5 | 季节性 mean 66 | MPYVA6gM | 1.27 | 1.20 | **1.16** | **0.96** | **0.0370** | **0.005992** |
| B3 | 季节性 × 防御 | 88RXqNNX | 1.23 | 1.11 | 0.30 | 0.82 | 0.1225 | 0.001664 |
| B8 | `ts_target_tvr_decay` 0.03 | zq3ezdAO | 1.21 | 1.12 | 1.01 | 0.83 | 0.0441 | 0.004889 |
| B9 | bucket 中性化（复合分分桶内比季节） | vR1PVAYv | 0.70 | 0.42 | 1.00 | 0.53 | 0.1717 | 0.000716 |
| B2 | 季节性 `ts_rank` 252 | 1YN05WWW | 0.63 | 0.40 | −0.23 | 0.49 | 0.0714 | 0.001437 |

### 7.4 ★★★ 定论：model250 的 (S, 2Y) 前沿受限，无法同时达 1.58

**沿平滑度轴（换手从高到低）呈现严格单调的 S↔2Y 替代关系**：

| 平滑程度 | TO | S | 2Y | S 缺口 | 2Y 缺口 | 合计缺口 |
|---|---:|---:|---:|---:|---:|---:|
| 无平滑（B6 Xg9MEaN5） | 0.124 | **1.37** | 0.54 | 0.21 | 1.04 | 1.25 |
| 轻平滑（B4 P0oKE55L） | 0.115 | 1.32 | 0.94 | 0.26 | 0.64 | 0.90 |
| 中平滑（B5 MPYVA6gM） | **0.037** | 1.27 | **1.16** | 0.31 | 0.42 | **0.73** ★最优 |
| 中平滑（B8 zq3ezdAO） | 0.044 | 1.21 | 1.01 | 0.37 | 0.57 | 0.94 |

- **S 上界 1.37，2Y 上界 1.16，二者永不并存**（同一条替代曲线上取点）。
- 合计缺口最小点 = B5 `MPYVA6gM`（S1.27 / 2Y1.16 / TO0.037 / margin 0.005992 / F1.20 / sub_u 0.96），仍差 0.31 + 0.42。
- 结论：**model250 单数据集无法产出 REGULAR 合格件**，但其 12 颗 REVIEW 件是全 DEU 唯一的近合格池（0.73 合计缺口）。

**机理说明**：`mdl250_*_seasonality` 是 ML 从 10 年同日历历史训练出的静态季节性模式 ⇒ 2014–2021 段显著有效、2022–2023 段（2Y 窗口）边际衰减 ⇒ 任何把整体 S 抬上去的操作都会同时放大近两年的衰减。这与既有记忆「2Y 由字段定、S 由几何定」一致：**要动 2Y 必须换字段，不能调几何。**

### 7.5 可交付性裁定

model250 不产出可提交件。但 `MPYVA6gM`（S1.27/2Y1.16/F1.20/TO0.037/margin0.0060/sub_u0.96，`failed_ra` 仅 2）是 DEU 全库**质量最高而未过线**的一颗，保留为 A 类近合格池首位，供后续「放宽 2Y 或改 universe」时直接取用。
