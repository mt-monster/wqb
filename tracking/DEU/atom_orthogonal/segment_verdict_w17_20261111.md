# DEU ATOM 战役 · Wave 17（sentiment33）判决 + 论坛逆方差模板
> region=DEU / TOP500 / D1 / SUBINDUSTRY / decay4 / trunc0.08 / nan OFF / pasteurize ON / unit VERIFY
> 生成时间：2026-11-11

---

## 一、Wave 17：`sentiment33` 新闻情感极性 → **判死**

批次 `19ocKH1OY4BaaRbOFwGoNjQ` · 10/10 REJECT · cov 0.3221 / 255 字段全 VECTOR / ac 45

### 数据集结构（5 套 NLP 方法 × 5 个关键词窗口 fkw1..fkw5）
- `method_1_*` = **计数**（positive token count），含 `_neut`，配 `valid_tokens_total`（总词数）
- `method_2/3/4_*` = **0–1 加权平均分数**（含 `_filtered_*` 额外 NLP 过滤版）；**无 `_neut`**
- `method_5/6/7/9` = 纯计数无极性
- `group_level_3/5_count` = 层级关键词计数；`median/max_token_length` = 文本长度
- 元数据：`snt33_1..5`（headline / event_title / true_timestamp）

### 结果全表

| # | 模板 | 机制 | 算子 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| T1 | `group_rank(ts_mean(m3f_pos − m3f_neg,22),industry)` | 净极性差（NLP 过滤分数版） | 7 | 88RXKVno | 0.13 | 0.05 | **1.44** | 0.0996 | 0.17 | 4 |
| T2 | `group_rank(ts_mean((m1_pos−m1_neg)/valid_tokens,22),industry)` | 计数型净极性占比 | 10 | kqN9LvQK | **−0.37** | −0.22 | **1.48** | 0.0948 | 0.01 | 4 |
| T3 | `group_rank(ts_mean(m3_pos/(m3_pos+m3_neg),22),industry)` | 正情绪占比（比率几何） | 10 | mLoQxdZK | −0.07 | −0.02 | 0.96 | 0.1007 | −0.08 | 5 |
| T4 | `group_rank(add(rank(ts_mean(m3f_pos,132)),rank(ts_mean(m3f_neg,11))),industry)` | 长窗正 vs 短窗负（异窗骨架） | 11 | xAr5mVRp | **0.53** | 0.32 | −0.04 | 0.1729 | 0.47 | 4 |
| T5 | `group_rank(ts_delta(ts_mean(m4_pos−m4_neg,22),66),industry)` | method_4 情绪动量 | 9 | 6XdNYZEO | −0.05 | −0.01 | 0.83 | 0.1325 | 0.47 | 4 |
| T6 | `group_rank((m3f_pos−m3f_neg)−(m3_pos−m3_neg),industry)` | NLP 过滤增量（二阶差分） | 12 | Xg9MYVK1 | 0.22 | 0.09 | −0.73 | 0.1732 | 0.09 | 5 |
| T7 | `group_rank(ts_mean(m2_pos+m3_pos+m4_pos,22),industry)` | 跨方法正情绪共识 | 10 | akKGWeOx | −0.09 | −0.03 | 1.14 | 0.0988 | 0.11 | 4 |
| T8 | `group_rank(ts_mean((m2f_pos−m2f_neg)×valid_tokens,22),industry)` | 情绪 × 信息量交互 | 10 | omEZ9RYJ | 0.07 | 0.02 | 0.77 | 0.0973 | −0.05 | 5 |
| T9 | `group_rank(ts_mean(group_level_5_count/valid_tokens,22),industry)` | 层级事件强度 | 7 | 1YN0nOgM | 0.07 | 0.02 | −0.66 | 0.0980 | 0.08 | 4 |
| T10 | `group_rank(ts_mean(signed_power(m3f_pos−m3f_neg,3),22),industry)` | 极端情绪三次方放大 | 9 | ZYQNWgpx | 0.11 | 0.04 | **1.38** | 0.0996 | 0.13 | 4 |

### 四结论

1. **★ S 上限 0.53**（T4 异窗骨架），其余全在 −0.37 ~ 0.22。sentiment33 无截面预测力。
2. **★★★ 净极性族出现「S 与 2Y 符号相反」的方向不稳定**：T1 S +0.13 / 2Y +1.44；T2 **S −0.37 / 2Y +1.48**；T7 S −0.09 / 2Y +1.14；T10 S +0.11 / 2Y +1.38。
   ⇒ 情感极性在 **2022–2023（近两年）有效，2014–2021 无效甚至反向**。但**翻转符号会同时把 2Y 打成负的**（−1.48），无法两者兼得。**这类「半程有效」信号不可用**——判死的正确理由不是「2Y 不够」，而是「方向在整个样本期内不稳定」。
3. **情感「极性」无效，但「关注度」有效**：同塔已出货 mLox6Mg2（S 2.05 / 2Y 2.53）用的是 `snt7_all_languages_views`（新闻浏览量）、`snl27_relpopularity08`（相对流行度）。⇒ **DEU 新闻类里，注意力/热度维度有信息，文本情感极性维度没有信息。** 与「新闻情感在德语小池子上样本稀疏、NLP 跨语言迁移失真」一致。
4. **cov 0.3221 的连带损伤**：10 条 `investability_ratio` 有 6 条为负（−0.22 ~ −3.71），子宇宙 Sharpe 普遍 <0.2。覆盖率太薄是结构性缺陷，不是模板能修的。

---

## 二、★★★ 论坛收获：《稳定性调整的模型概率》逆方差模板（高价值，待 DEU 验证）

来源：WORLDQUANT BRAIN 中文论坛，作者 CW62372，2026-09-22，article_id `43666906426647`
标题：《【Alpha Idea】概率高还不够：用"稳定性调整"过滤五日下行预测》

### 抽象模板（**单字段结构，非混信号**，符合用户硬约束）

```
relative_probability = group_rank(model_probability, economic_group)
probability_uncertainty = ts_std_dev(model_probability, uncertainty_window)²
confidence_adjusted_signal = direction × relative_probability / (regularizer + probability_uncertainty)
alpha = smooth(confidence_adjusted_signal, holding_window)
```

关键设计（论文作者原话）：
- **分子是方向，分母是置信度**：`relative_probability / probability_variance` —— 方向与置信度围绕**同一个字段**，保持单腿结构，不引入第二条规则。
- **为什么不用 `ts_delta(probability)`**：概率上升既可能是新信息也可能是分类边界抖动；本模板回答「模型是否持续看空」，不是「今天是否比昨天更看空」。
- **为什么必须加 regularizer（0.001）**：无 regularizer 的逆方差结构在方差趋零时产生巨大值，即使有 truncation 也会让排序对数值误差敏感。
- **为什么需要平滑（30 日线性衰减）**：概率每日更新、滚动方差会随窗口跳变；平滑使持仓接近「持续信念」而非「短窗统计量交易」。

### USA 实测（作者原文，可作为迁移前的上限参考）

| 指标 | 全体 | 可投资性约束后 |
|---|---:|---:|
| Sharpe | 1.63（门槛 1.58 PASS） | 1.35 |
| Fitness | 1.02（门槛 1.00 PASS） | 0.82 |
| **2Y Sharpe** | **1.61**（门槛 1.58 PASS） | — |
| Turnover | 14.35% | 12.05% |
| Prod Correlation | **0.5408** | — |
| 最大回撤 | 4.73% | 5.05% |

**★ 2Y 1.61 且 prod 0.54** —— 这两项正是 DEU 的最大短板（本段三波 30 条 alpha 无一条 2Y > 1.58）。逆方差加权降低权重波动，使 PnL 时间分布更均匀，**机理上正好治 DEU 的 2Y 病**。

### 可替换接口（作者给出的迁移清单）
- `model_probability`：上涨桶 / 下跌桶 / **违约概率** / 事件概率 / 盈利超预期概率 / 新闻情绪分类概率
- `economic_group`：sector / industry / country
- `uncertainty_window`：5 / 10 / 20 日
- `regularizer`：按概率方差的典型尺度选择（**不可机械复制 0.001**）
- `holding_window`：10 / 20 / 30（**不可机械复制 30**）

### 作者自陈的失效边界（必须记）
- 年度 Sharpe：2019 年 **−0.88**（其余 2.48/2.38/1.44/0.94/1.13/2.29/2.37/1.62/1.50）
- 未解决问题：「稳定 ≠ 正确」——低方差也可能意味着模型反应迟钝。
- 分母用**方差**比标准差惩罚更强；作者建议后续对比 std / variance / 绝对变化均值。

---

## 三、按本模板重构的候选（Wave 19 已用）

`model28`（StarMine 结构性信用风险 / Merton 模型）的 `mdl28_sm_structural_credit_structural_pd_pct`（1 年违约概率百分比，cov 0.6838）是本模板最契合的软概率字段。

Wave 19 的 M1 表达式（原样迁移，仅换字段与 group 轴）：
```
ts_decay_linear(
  divide(
    -group_rank(mdl28_sm_structural_credit_structural_pd_pct, industry),
    add(0.001, multiply(
      ts_std_dev(mdl28_sm_structural_credit_structural_pd_pct, 5),
      ts_std_dev(mdl28_sm_structural_credit_structural_pd_pct, 5)))),
  30)
```
算子 7 个（ts_decay_linear / divide / group_rank / add / multiply / ts_std_dev ×2）。

M6 把同一结构迁移到 `distance_to_default`（用 22 日不确定窗口）。

---

## 四、本段勘察判死的数据集（未开波）

| 数据集 | 画像 | 判死理由 |
|---|---|---|
| `analyst_earnings_ibes` | cov 0.9978 / 42 字段全 MATRIX / ac 279 | **不是分析师数据**，是纯日频行情矩阵（closing/highest/lowest/open price、shares_outstanding、market_cap、total_return 1d/5d/20d/60d/120d/250d、trading_volume、VWAP），且三套冗余变体 `dlr1`(美)/`dlr2`(欧)/`dlr3`(通用)。PV 塔 DEU 全族已判死 + 全为原始价格/成交量水平（❌ 类字段） |
| `model307` | cov 0.4333 / 11 字段全 VECTOR / ac 2 | 地区营收分解（axj/cnax/emea/eu/gb/jp/latam/us/unclassified/canada/australia_nz），**成分数据（合计=1）不可多字段相加**；年报频率慢变量，cov 0.43 薄。暂搁置，非判死 |
| `model106` | cov 0.7878 / 14 字段 / ac 32 | 星级评级模型（stars 0–4 / global_evaluation −2~+2 / rv 估值 −2~+2，均 cov 1.0）。**但只有 5 档分辨率**，与 model264 `_class` 同病（分档压掉符号与幅度）。备选，低优先 |

---

## 五、累计战果

| 波次 | 数据集 | 塔 | 最高 S | 最高 2Y | 判决 |
|---|---|---|---:|---:|---|
| Wave 15 | model216 | MODEL | 1.41 | 1.01 | 判弱（增量腿） |
| Wave 16 | shortinterest3（24 原始字段） | SHORTINTEREST | 0.61 | 0.99 | 判死 |
| Wave 17 | sentiment33 | SENTIMENT | 0.53 | 1.48（方向不稳） | 判死 |
| Wave 18 | model238 | MODEL | 在飞 | — | — |
| Wave 19 | model28 | MODEL | 在飞 | — | — |

**严格单数据集 ATOM 合格 4 颗**（QPvzNNGG / LLMzYrZe / MPY9VNY9 / QPv6jLvX）；合格件 6 颗（含违 MODEL+MODEL 禁混的 E56pROb9、双集 mLox6Mg2，剔除后 5 颗）。缺口 6 颗。

**累计有数据判死 ≈41 个数据集**（本段新增 sentiment33、analyst_earnings_ibes；model216 判弱、shortinterest3 24 字段判死）。
