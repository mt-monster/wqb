# USA / OTHER 塔开面台账 —— mmp_nlp_sentiment（2026-11-06）

## 0. 为什么是这里：USA 塔位洼地实读

`get_pyramid_alphas(region=USA)` D1 实读（塔内 ≥3 = 点亮）：

| 状态 | category（数量） |
|---|---|
| 已点亮 | model(4) / analyst(6) |
| 近亮（差1颗） | **other(2)** / **risk(2)** |
| 其他 | institutions(1) / earnings(1) |
| 零塔 | pv, fundamental, socialmedia, news, **option**, macro, insiders, sentiment, shortinterest, imbalance |

★ **other 的 pyramidMultiplier = 1.4，全表最高**（risk 1.2 / pv 1.0）。再 1 颗即点亮 USA/OTHER ⇒ 当前性价比最高的单点。

USA 缓存 `tracking/mining/field_coverage_USA_d1_TOP3000.json`：294 数据集，other 57 个、risk 仅 7 个。

## 1. OFI 面（USA OPTION）收尾 —— 信号真实但天花板 0.93

6 个结构互异模板全部收完（数据集 `order_flow_imb`，120 字段全 MATRIX，cov 0.77–0.91，aC 113）：

| alpha | 模板 | 机制 | S | F | TO | 2Y | sub | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `0mYG9Lvk` | OFI1 单腿水平（正号） | client 看涨 vol 失衡 22 日均 | **+0.93** | 0.27 | 21.28% | 0.67 | 0.41 | ★ 面内最强 |
| `LLM8qEbm` | OFI1 同款（负号） | 同上取负 | **−0.93** | −0.27 | 21.28% | −0.67 | −0.41 | 完美镜像 |
| `QPvWqOrp` | OFI2 双腿差值 | customer − broker_dealer vol 失衡 | 0.73 | 0.19 | 21.37% | 0.69 | 0.33 | 组合反而更弱 |
| `Xg9NPx61` | OFI4 OTM 虚值看涨长窗 | ts_zscore(bullish_vol_otm, 252) | 0.32 | 0.03 | **85.17%** | 0.57 | 0.44 | TO 高频噪声档 |
| `LLM8qQLL` | OFI5 笔数-金额背离 | trade_count vs vol 背离 | 0.29 | 0.02 | **109.25%** | 0.99 | −0.11 | 极端换手，判死 |
| `1YNG1MYJ` | OFI6 回归残差 | ts_regression(vol, count) | — | — | — | — | — | **单位不兼容报错** |

### 1.1 三条硬结论

1. **符号方向被数据推翻论文先验**：Pan & Poteshman (2006) 说客户看跌需求 → 负收益；本数据集 `customer_vol_imbalance` 实测**正号预测正收益**（+0.93 vs 负号 −0.93，六项指标完整镜像���。按实测走，不按先验走。
2. **`imbalance` 类字段落在「完美镜像」字段类**（与事件流/计数/金额同类），不是「分位/评分/排名」类。加负号可得严格反向，可用于快速方向确认（1 批成本）。
3. **双腿组合不增强**：单腿 0.93 → 双腿差值 0.73。本数据集内部参与者间差值抹掉了有效成分 ⇒ 加强手段不能用「双腿组合」。

### 1.2 判死 vs 挂起的界定

OFI 面 **不是「全灭」**（最强 |S| 0.93 远超噪声档 <0.3），而是**信号天花板不足**：
0.93 → USA 门槛 1.58 需 1.7x，且三条正交方向（符号/双腿/OTM/背离）都在 0.3–0.93 区间 ⇒ **不投入第二批**，面挂起备用。

## 2. 为什么换 mmp_nlp_sentiment（而不是 ml_factor_proj / techindi_model）

| 数据集 | cat | cov | 字段 | aC | uC | 实测可用性 |
|---|---|---:|---:|---:|---:|---|
| `ml_factor_proj` | other | 0.9996 | 1070 | 73 | 40 | ❌ `get_datafields` 在 TOP3000 与 TOP1000 均返回 **0 字段** |
| `earningscall_embed` | other | 0.8496 | 515 | 22 | 13 | △ 只有 `analyst` **单一角色**；字段全为 `{embedding,projection}_component_{N}`，单维无语义、算子预算内难聚合 |
| `techindi_model` | other | 0.973 | 1830 | 382 | 134 | ○ 备选：`confidence_*_quantile_prediction` aC 仅 1–2 但单字段无方向，需配点预测 |
| **`mmp_nlp_sentiment`** | other | 0.9724 | **1650** | **81** | 32 | ✅ **选定**：成对字段多、命名可解释、aC 0–16 极低拥挤 |

★ 教训：缓存里的 `fieldCount` 是**数据集元数据**，不代表该组合（region/universe/delay）下真有字段可取。`ml_factor_proj` 1070 字段是空的——**开面前必须 `get_datafields` 实测**。

## 3. mmp_nlp_sentiment 字段画像（MATRIX，cov 0.9025–1.0）

四大家族：

| 家族 | 代表字段 | cov | aC | 语义 |
|---|---|---:|---:|---|
| AFINN 词典计数 | `afinn_positive_sentiment_count` / `afinn_negative_sentiment_count` | 1.0 | 9 / 16 | 正/负情感词**计数**（事件流类） |
| AFINN 词典打分离散 | `afinn_sentiment_mad` / `afinn_sentiment_score_mad` | 0.9791 | 7 / 1 | 情感分数**离散度**（分歧代理） |
| 评级主题提及 | `average_raise_price_target_mention` / `average_lower_price_target_mention` | 0.9025 | 2 / 0 | 文本中「上调/下调目标价」提及均值 |
| 多空主题分 | `avg_bullish_topic_score` / `average_bearish_mention_score` | 0.9025 | 3 / 3 | 看涨/看跌主题得分 |
| 关注度/文本量 | `article_count_benzinga_standard` / `analyst_reference_count_sum` / `average_character_count_median` | 1.0 / 1.0 / 0.9791 | 5 / 5 / 0 | 报道数、分析师提及数、文本长度 |

## 4. ★★ 决定性机制发现：稀疏新闻字段必须 `ts_backfill`

**来源**：论坛《【Alpha模板】情绪数据中用 ts_covariance 构建alpha模板》(article 35294898626711, 52 votes) 评论区 ZZ47696，在 GLB/ai_news_scores 上同表达式对照实测：

| 构造 | Sharpe | ht_ratio |
|---|---:|---:|
| 不回填 | 0.89 | 0.64 |
| `ts_backfill(f, 120)` | **1.53** | 0.83 |

且 **`ts_backfill` 窗口 20 与 120 结果逐位相同** ⇒ 只要覆盖到「上一条新闻」即可，不必调窗口；但完全不填会废掉。

**为什么**：新闻/情绪是**事件驱动稀疏序列**，多数票多数天无新闻 ⇒ 字段为 NaN。`nanHandling=ON` 把缺失当 **0**，等于把「没消息」误判成「情绪中性且刚刚发生」；`ts_backfill` 才是「沿用上一条新闻的值」。两者语义完全不同，不可互相替代。

★ 这是新闻/情绪类与量价类**最大的工程差异**，也是此前 HKG/KOR 新闻面 TO 40%+ 且 |S|<0.3 的可能共因之一。

## 5. 模板池（12 个结构互异，MMP1–MMP12）

全部以 `ts_backfill(x,120)` 为稀疏字段前置。记 `NET = subtract(bf(pos_cnt), bf(neg_cnt))`，`RAISEDIF = subtract(bf(raise_pt), bf(lower_pt))`。

| # | 模板 | 机制/几何 | 来源 |
|---|---|---|---|
| MMP1 | `group_rank(ts_mean(NET, 63), sector)` | 净情绪**水平** | AFINN 经典净情绪 + 论坛回填实证 |
| MMP2 | `group_rank(ts_delta(ts_mean(NET,63), 63), sector)` | 情绪**一阶加速** | 事件驱动动量 |
| MMP3 | `group_rank(ts_mean(RAISEDIF, 63), sector)` | 分析师**目标价修正净差** | 论坛 43250301270295「换数据腿：目标价上调vs下调也能套」 |
| MMP4 | `group_rank(ts_zscore(subtract(bf(bull),bf(bear)), 252), subindustry)` | 多空主题净差长窗 | 主题分数族 |
| MMP5 | `-group_rank(ts_mean(bf(afinn_sentiment_mad),63), sector)` | 情绪**分歧度反转** | Baker-Wurgler 分歧代理 |
| MMP6 | `group_rank(multiply(ts_mean(NET,63), ts_rank(bf(art_cnt),252)), sector)` | **关注度加权**情绪 | Da-Engelberg-Gao 注意力 |
| MMP7 | `group_rank(subtract(ts_zscore(ts_mean(NET,63),252), ts_zscore(ts_mean(bf(art_cnt),63),252)), sector)` | 情绪-**注意力背离** | 同上，正交化 |
| MMP8 | `-group_rank(ts_covariance(bf(neg_cnt), bf(pos_cnt), 252), sector)` | 正负情绪**协方差反转** | 论坛 35294898626711 原模板 |
| MMP9 | `group_rank(ts_zscore(ts_av_diff(bf(pos_cnt), 63), 252), market)` | 情绪**冲击高通滤波** | 论坛 ZZ47696 短周期版 |
| MMP10 | `-group_rank(ts_arg_max(bf(pos_cnt), 240), sector)` | 情绪**极值定位** | 距峰值越久越弱 |
| MMP11 | `-group_rank(ts_std_dev(NET, 66), sector)` | 情绪**波动率反转** | 二阶矩 |
| MMP12 | `group_rank(ts_regression(ts_mean(NET,63), ts_mean(bf(art_cnt),63), 252, lag=0, rettype=0), sector)` | 剔除关注度的**回归残差** | 论坛通用残差模板 |

★ 外部文献约束（论坛 RM49262 引 *Investor Sentiment in Asset Pricing Models: A Review of Empirical Evidence*）：情绪冲击**约 4–5 天后同幅度反转** ⇒ 短窗（<22）做的是反转而非动量，且短窗实测普遍平庸；**主用 63/252/504**。

## 6. 派发记录与 A/B 设计

**批 `42XeW322c4GW8OjQ9EsN8pv`（无回填基线）** —— USA/TOP2000/D1/decay 0/STATISTICAL/trunc 0.08/unit VERIFY/nan ON/pasteurization ON/maxTrade OFF：
```
E1 = group_rank(ts_mean(subtract(afinn_positive_sentiment_count, afinn_negative_sentiment_count), 63), sector)        // MMP1, 3 ops
E2 = group_rank(ts_mean(subtract(average_raise_price_target_mention, average_lower_price_target_mention), 63), sector) // MMP3, 3 ops
```

**批 `nHp9FcKb5id9avh4vDw0Zd`（+ts_backfill 120）** —— 与上批**逐字相同只差 `ts_backfill(.,120)`**：
```
E1 = group_rank(ts_mean(subtract(ts_backfill(afinn_positive_sentiment_count, 120), ts_backfill(afinn_negative_sentiment_count, 120)), 63), sector)        // MMP1b, 5 ops
E2 = group_rank(ts_mean(subtract(ts_backfill(average_raise_price_target_mention, 120), ts_backfill(average_lower_price_target_mention, 120)), 63), sector) // MMP3b, 5 ops
```

★ 这是**只换一个维度**的干净 A/B（回填有/无），可直接量化论坛实证在本区的效应。三闸均过：valid=true、unknown_fields=[]、算子 5 ≤ 12。

## 7. 待验证与后续队列

- [ ] A/B 回收 → 若回填增益成立，MMP1b/MMP3b 作为该面基线骨架
- [ ] 若单腿水平 |S| < 1.2，转 MMP8（协方差）/ MMP4（长窗 zscore）/ MMP12（残差）三条正交几何
- [ ] TO 若 >40% ⇒ 按「高频刷新噪声描述符」判据评估是字段级属性还是骨架问题（decay 0 → 4/8 单杠杆先测）
- [ ] risk 面差 1 颗点亮（多因子模型输出 `mfm_model_output` 117 字段 aC 253；`risk59/70/62` 已高度饱和 aC 4464–66609，禁入）
## 8. 第二批实测（MMP8 / MMP4）—— 双双未过

| alpha | 模板 | S | F | TO | 2Y | sub | inv | fRA | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `pwdWEvJ6` | **MMP8 正负情绪协方差反转** `-group_rank(ts_covariance(neg,pos,252),sector)` | **−0.61** | −0.20 | **5.97%** | −1.03 | −0.55 | −0.56 | 4 | ❌ 反号仅 +0.61 |
| `bl6xM82R` | MMP4 多空主题净差 `ts_zscore(bull−bear,252)` | 0.44 | 0.04 | **110.95%** | 0.75 | 0.11 | 0.57 | 6 | ❌ TO 极端 |

★ **MMP8 协方差反转并未成功**：TO 只有 5.97%（典型慢变量），但 |S| 仅 0.61 —— 是弱信号不是噪声，强度不足以支撑 USA 门槛 1.58。
★ 论坛 52-vote 的 `ts_covariance` 模板在本数据集未复现（该帖用的是 Sentiment21 + EUR/TOP2500）。**模板迁移要看数据集，不能照搬**。

## 9. ★★ 第三批实测 —— 真正过线的是 techindi_model 极值桶概率差

**⚠️ 归属更正**：初稿把 S +2.29 记到了 MMP8 名下，实为 techindi 构造。以下为逐条 `get_alpha_details().code` 实读核实后的正确表：

| alpha | 真实表达式 | S | F | TO | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---|
| `pwdWER5x` | `group_rank(subtract(P4_v5, P0_v5), sector)` —— **极值桶概率差** | **+2.29** | 0.59 | **75.07%** | 1.53 | ★ 面内首个过 1.58 |
| `vR1Y9rOw` | `-group_rank(subtract(P4_v4, P4_v5), sector)` —— 同族版本分歧度 | −0.30 | −0.03 | 75.48% | −0.03 | ❌ |

`pwdWER5x` 的 `checks.fail` 实读（三项）：
- `LOW_FITNESS` 0.59（limit 1）
- `HIGH_TURNOVER` 0.7507（limit 0.7）
- `LOW_2Y_SHARPE` 1.53（limit 1.58，**只差 0.05**）

pyramid 实读 = **USA/D1/OTHER ×1.4** ⇒ 出货即点亮 USA/OTHER（2→3）。

**机制**：`likelihood_fifth_quantile_five_day_bucket_{zero…four}` 是模型对「5 日后收益落入第几档」的**完整概率分布**。`P4 − P0` = 最高桶概率 − 最低桶概率 = **净看涨概率**，本身就是训练好的方向预测，不需要在它上面另造骨架。
⇒ 本面唯一有效用法：**直接取分布两端的概率差**。版本分歧度（`P4_v4 − P4_v5`）远不如它。

★ 「同族编号相减」的边界：
- ✅ 慢变评分/等级类：`buzz_intensity_score_2 − score_11`(S 2.67)、`credit_risk_model_score_5 − score_7`(S 2.63)
- ❌ 每日更新的预测概率：`P4_v4 − P4_v5`(S −0.30 / TO 75.48%)
⇒ 判据是**被减项是否都慢变**。

## 10. 对 MMP8 的两次压 TO 尝试（已判死，仅作反面记录）

批 `1B5fAwf7e55oc5IyCyP8A3i`：
```
MPYgXZga = hump(-group_rank(ts_covariance(neg,pos,252), sector), hump=0.01)     // S −0.95 / TO 4.09%
GrWQ6xQx = -group_rank(ts_mean(ts_covariance(neg,pos,252), 22), sector)         // S −0.61 / TO 4.88%
```
原式 `pwdWEvJ6` = −0.61 / TO 5.97% ⇒ hump 让它更负（−0.95），平滑无变化。
★ **教训：`hump` 是压高 TO 专用，对本来就低 TO 的件是纯损耗**（此处 TO 已只有 5.97%）。

★ 踩坑：`hump(x, 0.01)` 被 toolkit 静态闸拒绝 —— **第 2 个参数必须写成命名参数 `hump=0.01`**。报错原文：`函数 hump 的第2个参数必须使用命名参数 hump=`。

## 11. 第四批（针对 `pwdWER5x` 的真实降 TO 实验）

批 `19rN9u5N74TvbSgcMVEfSjB`，**decay 16** 作共同背景，隔离 hump 作用：
```
L1 = group_rank(subtract(P4_v5, P0_v5), sector)                       // 原式 + decay16 → 干净测 decay 单杠杆
L2 = hump(group_rank(subtract(P4_v5, P0_v5), sector), hump=0.002)     // decay16 + 轻 hump
```
★ 目标：TO 75.07% → <40%（F 才能从 0.59 升到 ≥1），同时 2Y 从 1.53 抬过 1.58。
★ 已排除路径：techindi_model **只有 `five_day` 一个 horizon**（无 10 日/20 日版本），拉长预测期限降 TO 不可行。
## 12. 第四批实测（decay 16）—— TO 修好了，F 成了新的硬障碍

| alpha | 构造 | S | F | TO | 2Y | sub | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `j2YVwE3o` | 原式 + **decay 16** | **1.26** | 0.51 | **18.40%** | **1.89** | 0.77 | 2 |
| `RRE5a3bj` | hump 0.002 + decay 16 | 0.05 | 0.00 | 3.56% | 0.84 | −0.08 | 4 |

**decay 16 的净效果**（对照 decay 0 的 `pwdWER5x`：S 2.29 / TO 75.07% / 2Y 1.53 / F 0.59）：
- TO **75.07% → 18.40%**（压掉 75%）✅ 修好 HIGH_TURNOVER
- 2Y **1.53 → 1.89** ✅ 修好 LOW_2Y_SHARPE（反向上升）
- S **2.29 → 1.26** ❌ 新增 LOW_SHARPE
- F **0.59 → 0.51** ❌ 反而更差

### 12.1 ★★ 为什么 F 是硬障碍（反推 fitness 公式）

`fitness ≈ sharpe × sqrt(|returns| / max(turnover, 0.125))`，用两组实测反推：

| 构造 | S | TO | F | 反推 \|returns\| |
|---|---:|---:|---:|---:|
| decay 0 | 2.29 | 0.7507 | 0.59 | **4.98%** |
| decay 16 | 1.26 | 0.1840 | 0.51 | **3.01%** |

⇒ TO 降了 75%，returns 只降 40% —— 但 **returns 绝对值只有 3–5%**，这是「5 日预测概率」类统计套利信号的固有特征（低收益低波）。
⇒ 要 F ≥ 1：TO = 0.30 时需 **S ≥ 2.58**；TO = 0.125（公式下限）时仍需 **S ≥ 2.04**。而该构造在 TO 30% 时 S 只有约 1.8。
**结论：F ≥ 1 在本构造上几乎不可达，除非 returns 翻倍。** 这比 S 更难修。

★ 方法论：**遇到「S 高但 F 低」的件，先反推 returns，再判断 F 是否可达**。若 returns < 5%，F 门槛基本封死该构造，不要继续在 decay/窗口上磨。

## 13. 第五批（最后一次尝试：neutralization 轴 + 信号集中化）

批 `1Rjnc6d8x4I09pF119dZHsuP`，decay 8 作共同背景、neutralization 换 SUBINDUSTRY：
```
N1 = group_rank(subtract(P4_v5, P0_v5), sector)                       // 干净测 STATISTICAL→SUBINDUSTRY 单杠杆
N2 = signed_power(N1, 1.5)                                            // 信号集中化，试图抬 returns
```
★ 若本批 returns 仍 <5%，则 `P4−P0` 路线判死（S 能过但 F 永不可达），USA/OTHER 面转其他数据集。

## 14. 第五批实测 + P4-P0 路线判死

| alpha | 构造 | S | F | TO | 2Y | sub | returns 实读 |
|---|---|---:|---:|---:|---:|---:|---:|
| 2rAGZZzP | SUBINDUSTRY + decay 8 | 1.09 | 0.48 | 25.26% | 1.45 | 0.81 | **4.91%** |
| A1VLaaZg | 同上 + signed_power(·,1.5) | 1.18 | 0.50 | 25.70% | 1.41 | 0.84 | **4.69%** |

★ fitness 反推公式验证成功：预测 4.90% / 4.61%，实测 4.91% / 4.69%。公式 F ≈ S × sqrt(|ret| / max(TO, 0.125)) 可靠，可用于零额度预筛。

### 14.1 ★★★ 判死依据：F 恒定在 0.48–0.59，四种配置都移不动

| 配置 | S | TO | F | returns |
|---|---:|---:|---:|---:|
| decay 0（STATISTICAL） | **2.29** | 75.07% | **0.59** | 4.98% |
| decay 16 | 1.26 | 18.40% | **0.51** | 3.01% |
| decay 8（SUBINDUSTRY） | 1.09 | 25.26% | **0.48** | 4.91% |
| decay 8 + signed_power 1.5 | 1.18 | 25.70% | **0.50** | 4.69% |

⇒ **F 在 0.48–0.59 区间纹丝不动，门槛是 1.0（差 67%）**。S 从 2.29 到 1.09 跨 2 倍、TO 从 75% 到 18.4% 跨 4 倍，F 几乎不变
⇒ **该信号的信息比是构造的不变量，不是参数问题**。换 neutralization（STATISTICAL→SUBINDUSTRY）反而让 S 从 2.29 掉到 1.09，是该面最差的一档；signed_power 只把 S 从 1.09 提到 1.18、returns 还略降。

**★ 判据（新增）：当四种配置把 S 和 TO 各自拉开 2–4 倍、F 却稳定在同一水平时，该构造判死 —— 这不是参数没调好，而是「收益/换手」比被字段本身锁死。继续磨 F 是纯浪费额度。**

### 14.2 USA/OTHER 面总结：10 条构造全部失败

| 数据集 | 构造 | 最好结果 | 死因 |
|---|---|---|---|
| mmp_nlp_sentiment | MMP1 AFINN 净情绪（±回填） | S −0.69 / −0.67 | 信号弱 |
| | MMP3 目标价修正净差（±回填） | S −0.13 / −0.19 | 信号弱 |
| | MMP8 正负情绪协方差反转 | S −0.61 / TO 5.97% | 信号弱 |
| | MMP8 + hump / + 平滑 | S −0.95 / −0.61 | 压 TO 手段无增益 |
| | MMP4 多空主题净差 | S 0.44 / TO 110.95% | TO 极端 |
| techindi_model | **P4−P0 极值桶概率差** | **S 2.29 / TO 75.07%** | **卡 F（恒 0.5–0.6）** |
| | 同族版本分歧度 P4_v4−P4_v5 | S −0.30 / TO 75.48% | 信号弱 + TO 高 |
| | P4−P0 + decay 16 | S 1.26 / TO 18.40% / 2Y 1.89 | 卡 F + S 不足 |
| | P4−P0 + SUBINDUSTRY | S 1.09 / TO 25.26% | 卡 F |
| | P4−P0 + signed_power 1.5 | S 1.18 / TO 25.70% | 卡 F |

⇒ **两个数据集、6 类结构（净差水平 / 协方差 / 主题分 / 极值概率差 / 版本分歧 / 集中化）、5 批 10 条仿真全部失败**，满足「同一面 ≥6 个结构互异骨架全灭」的判死条件。
⇒ **USA/OTHER 面暂封**（这两个数据集）。OTHER 尚有 55 个数据集，若回来需换完全不同的字段族（非新闻 NLP、非模型预测概率）。
⇒ USA/OTHER 塔仍为 **2**，未点亮。


