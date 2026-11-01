# GBR `sentiment33` 模板库与实证账本

**创建：2026-10-30** · 区域 GBR / D1 / TOP700 · 目标塔 SENTIMENT（**当前 0**）

---

## 0. 为什么选这个数据集

| 项 | 值 |
|---|---|
| 塔位 | **SENTIMENT = 0**（未点亮） |
| 字段数 | **255**，全部 `VECTOR` |
| coverage | **0.3199–0.3239**（约 224 只股票，极薄） |
| 拥挤度 | 极低：最高 `alphaCount` 仅 **13**（`snt33_sefke1v1_fkw1_method_1_pos`），最高 `userCount` 仅 8 |
| GBR 可打性 | GBR 只剩 TOP700 一个 universe，无小盘退路 ⇒ 薄覆盖是硬约束 |

---

## 1. ★★★★★ 字段语义（2026-10-31 **第二次修正：字段分四类，前一批探针打错了类**）

> **修正史**：2026-10-30 曾把全部字段当「token 计数」并推导出「必须除以 `valid_tokens_total`」；2026-10-31 拉全 `fkw1_method_*`（39 字段）后确认 **`pos`/`neg` 的含义随 `method` 编号而变** —— `method_1` 是计数，`method_2/3/4` 是 **0–1 加权平均分**。前 3 条探针（S1/S2/S3）全部打在 A 类上。

### 1.1 四类字段（`fkw1` 层实测，`coverage` 全为 0.3239）

| 类 | 字段模式 | 描述关键短语 | 语义 / 单位 | ac 最高 |
|---|---|---|---|---|
| **A** | `method_1_{pos,neg,neut,filtered_pos,filtered_neg,filtered_neut}` | "positive sentiment **count**, **total number of** positive tokens" | **token 计数**（受文档长度污染） | `_pos` 13 / `_neg` 7 |
| **B** | `method_{2,3,4}_{pos,neg}` 与 `method_{2,3,4}_filtered_{pos,neg}` | "positive sentiment **weighted average score** for the document" / "**weighted average 0–1** for the entire document" | **连续情绪分，值域 [0,1]**（已归一化，不受长度污染） | `method_2_neg` 6 / `method_2_filtered_pos` 3 |
| **C** | `method_{2,3,4}_obj` 与 `method_{2,3,4}_filtered_obj` | "**Objectivity** weighted average score ... weighted average **0–1**" | **客观性 [0,1]** ⇒ 天然的「置信度/决绝度」门控字段 | `method_4_filtered_neg` 同族 2 / `method_2_filtered_obj` 1 |
| **D** | `method_{5,7,8}_*`、`method_9_feature_1..11` | "Count of tokens flagged by Method N ...; **no explicit polarity**" | 无极性语言特征计数 | `method_5` 3 / `method_9_feature_2,3` 各 1 |

**⇒ 三条可执行结论**：
1. **真正能当情绪分用的是 B 类**（`subtract(pos,neg)` 天然落在 [−1,1]，且已按文档长度归一化）⇒ **不需要除以 `valid_tokens_total`**。
2. **C 类 `obj` 是 memory「破 SUB 唯一有效杠杆」的现成载体** —— `multiply(x, rank(1 − obj))` 正是 USA wave249 上把 SUB/S 从 0.332 抬到 0.556 的那个形态（客观性高＝事实陈述、情绪不明确 ⇒ 权重应压低）。
3. **A 类（`method_1`）是最差的一类**：token 计数被文档长度主导，`vec_sum` 后更被超长文档（如完整财报电话会记录）吃掉。S1/S2/S3 的负结果**不能用来判死本数据集**，只能用来判死 A 类。

### 1.2 命名维度（修正）

- `fkw{1,2,3,4,5}` —— 5 个族（coverage 0.3199–0.3239，**fkw1 最宽** 0.3239）
- `method_{1..9}` —— **实测 9 种方法全部存在**（早前台账「无 method_4」是错的）；有极性的是 **1（计数）+ 2/3/4（评分）**，无极性的是 5/7/8/9
- `sentiment_model{6,7,8,9}_score1[_fkw{1..5}]` —— **也是 token 计数**，描述明写 "Total number of such tokens in a document ... **no explicit positivity/negativity**" ⇒ **不是连续模型分**，早前的「换信息源」预设（S10）需降级
- `snt33_{1..5}_{event_title,headline,time_ingested_epoch,true_timestamp,true_timestamp_epoch}` —— 事件槽元数据（非信号）
- `snt33_sefke1v1_fkw{1..5}_valid_tokens_total` —— "Total number of tokens in a sentence"（**只对 A 类作分母有意义**）

### 1.3 拉取陷阱

`get_datafields(search="...")` 只命中平台前 **100** 条（本轮返回 39 条 + `pagination_truncated: true` / `truncated_reason: "search_window_capped"`），`platform_count` 恒为 255。**要看全量必须传 `dataset_id` 且不传 `search`。**

---

## 2. 派生量定义（全文复用，全部无量纲）

### 2.1 B 类（**主用**：连续情绪分，值域 [0,1]，已归一化）

```
POSB = vec_avg(snt33_sefke1v1_fkw1_method_2_pos)     当日多文档的平均正向情绪分
NEGB = vec_avg(snt33_sefke1v1_fkw1_method_2_neg)
SCOR = subtract(POSB, NEGB)                          净情绪分，值域约 [−1,1]  ★ 不需要除分母
OBJ  = vec_avg(snt33_sefke1v1_fkw1_method_2_obj)     客观性 [0,1] ⇒ CONF = subtract(1, OBJ)
```

> **为什么 B 类用 `vec_avg` 而不是 `vec_sum`**：`pos`/`neg` 已是**逐文档的 0–1 评分**，`vec_sum` 会把「当日文档数」混进信号（文档多的股票分数被放大）。用 `vec_avg` 得「当日平均情绪」，把「文档数」这个独立的注意力维度留给 A 类/D 类。

### 2.2 C 类（**门控专用**）

```
CONF = subtract(1, vec_avg(snt33_sefke1v1_fkw1_method_2_obj))    决绝度 = 1 − 客观性
```

### 2.3 A 类（前 3 条探针所用，**已证最差**）

```
POS = vec_sum(snt33_sefke1v1_fkw1_method_1_pos)      当日正向 token 数
NEG = vec_sum(snt33_sefke1v1_fkw1_method_1_neg)
NEU = vec_sum(snt33_sefke1v1_fkw1_method_1_neut)
TOK = vec_sum(snt33_sefke1v1_fkw1_valid_tokens_total)

NET = divide(subtract(POS, NEG), TOK)       净语调强度，值域约 [−1,1]
DEC = subtract(1, divide(NEU, TOK))         决绝度（非中性占比）
ATT = TOK                                   注意力强度（当日处理的总 token 量）
```

> **为什么 A 类必须先 `vec_sum` 再相除**：`pos`/`neg` 是 token **计数**，必须用文档总长度归一化才有意义。但 `vec_sum` 会让**超长文档**（完整财报电话会记录可达数万 token）主导当日取值 ⇒ **这是 A 类失效的根因**，见 §7.1。

---

## 3. ★★★★ 两条决定性先验（预注册，防止事后解释）

### 先验 A：纯情绪方向在 GBR 上大概率弱
论坛帖 `43541109631895`（**78 赞 34 评**）「从『搜索量』到『新闻密度』」明示：
> **纯 sentiment 方向 Sharpe < 0.5；要的是「异常注意力」。**

⇒ **S1（纯方向）预注册为「反例/对照组」**，不是主攻。若 S1 意外 >1.2，则该帖结论在 GBR 不成立，需回论坛复核。

### 先验 B：能抬 SUB 的只有「改变权重幅度分布」的算子
Agent memory（2026-10-30 USA `earnings_sent_matrix` 实证）：
> `multiply(x, rank(1 − P_neutral))` 把 SUB/S 从 **0.332 抬到 0.556（+67%）**；而 `group_rank`（0.328）/ `ts_delta`（0.309）/ 比值条件化（0.336）**全部无效**。
> 判据：**只改排序的算子对 SUB 无帮助；改权重幅度分布的算子才有希望。**

本数据集的 `NEU/TOK` 正是那个「P_neutral」，**先在 GBR/TOP700 上跨区验证这条杠杆**（S3）。

---

## 4. 模板库（12 条结构互异 · 来源标注 · 互异性自检）

> 满足硬约束「模板池 ≥10 且结构互异」：差异落在**信息源 / 矩 / 分组轴 / 非线性变换 / 时间尺度 / 复合方式**上。

| # | 名称 | 表达式 | 结构差异所在 | 来源 |
|---|---|---|---|---|
| **S1** | 净语调水平（**对照组**） | `group_rank(ts_mean(<NET>,5), subindustry)` | 纯方向基线 | 定则 #7（新闻必须 `ts_mean·5` 前置）；论坛 `43541109631895`（预注册反例） |
| **S2** | **异常注意力** | `group_rank(ts_zscore(<ATT>,252), subindustry)` | **时序异常**而非水平；注意力轴 | 论坛 `43541109631895`（78 赞）+ Da-Engelberg-Gao 2011 ASVI |
| **S3** | 净语调 × 决绝度门控 | `multiply(group_rank(ts_mean(<NET>,5), subindustry), rank(<DEC>))` | **乘性置信度门控**（幅度重分布） | memory「破 SUB 唯一有效杠杆」；权重恒为 `rank(DEC)`，**不扫描常数** ⇒ 合规 |
| **S4** | 跨方法分歧度 | `group_rank(ts_mean(abs(subtract(<NET_m1>, <NET_m2>)),22), subindustry)` | **模型间分歧**轴（不确定性） | 自建 |
| **S5** | 过滤前后噪声 | `group_rank(ts_mean(subtract(<NET_raw>, <NET_filtered>),22), subindustry)` | **同概念双实现之差** = NLP 噪声 | 自建（`filtered_*` 专为此而生） |
| **S6** | 语调时序异常 | `group_rank(ts_zscore(ts_mean(<NET>,5),504), subindustry)` | **时序**标准化（vs 横截面） | 自建 |
| **S7** | 语调动量 | `group_rank(ts_delta(ts_mean(<NET>,5),22), subindustry)` | **一阶差分** | 自建 |
| **S8** | 长短语调共振 | `group_rank(add(ts_mean(<NET>,252), ts_mean(<NET>,5)), subindustry)` | **多尺度同字段**（权重恒 1） | 论坛 `43583615602711`（23 赞）跷跷板：慢分量撑 S、快分量撑 2Y |
| **S9** | 语调极端性（高斯化） | `group_rank(ts_quantile(ts_mean(<NET>,5),252, driver="gaussian"), subindustry)` | **非线性重分布** | memory「`ts_quantile(gaussian)` 抬 SUB +31%」（USA 实证） |
| **S10** | 预训练模型分 | `group_rank(ts_mean(vec_avg(sentiment_model7_score1),5), subindustry)` | **换信息源**（模型分 ≠ token 计数） | 数据集原生 |
| **S11** | 文档覆盖广度 | `group_rank(ts_mean(vec_count(snt33_sefke1v1_fkw1_method_1_pos),5), subindustry)` | **广度/覆盖度**轴 | 自建（注意：定则 #7 警告 `vec_count` 用于稀疏事件有 tie 陷阱，本模板即该警告的实测） |
| **S12** | 异常注意力 × 决绝度 | `multiply(group_rank(ts_zscore(<ATT>,252), subindustry), rank(<DEC>))` | **两个非方向轴复合** | S2 × S3 的交叉（自建） |

**互异性自检**：信息源轴 2（S1–S9 用 token 计数 / S10 用模型分）；矩轴 3（S1 水平 / S7 一阶差分 / S2,S6 时序 z）；非线性 3（S3 乘性门控 / S9 高斯化 / S12 双轴复合）；时间尺度 1（S8）；分歧/噪声 2（S4 / S5）；广度 1（S11）。**无任何两条只差窗口或常数。**

**`<NET>` 展开式**（写成一行以便复制）：
```
divide(subtract(vec_sum(snt33_sefke1v1_fkw1_method_1_pos), vec_sum(snt33_sefke1v1_fkw1_method_1_neg)), vec_sum(snt33_sefke1v1_fkw1_valid_tokens_total))
```
**`<DEC>` 展开式**：
```
subtract(1, divide(vec_sum(snt33_sefke1v1_fkw1_method_1_neut), vec_sum(snt33_sefke1v1_fkw1_valid_tokens_total)))
```
**`<ATT>` 展开式**：
```
vec_sum(snt33_sefke1v1_fkw1_valid_tokens_total)
```

---

## 4b. ★★★★★ B/C 类模板库（**主战场**，2026-10-31 因字段语义修正而新增）

> §4 的 S1–S12 全部建立在 **A 类 token 计数**上；前 3 条探针已证 A 类在 GBR 上为负（§7.1）。下列模板改用**B 类连续情绪分**（已归一化、不受文档长度污染）与 **C 类客观性**（现成置信度门控）。满足「≥10 条且结构互异」。

| # | 名称 | 表达式骨架 | 结构差异所在 | 来源 |
|---|---|---|---|---|
| **S4** ✅已派 | B 类净情绪水平（**B 类基线**） | `group_rank(subtract(vec_avg(m2_pos), vec_avg(m2_neg)), subindustry)` | 换字段类（A→B），水平 | 自建（标准情绪分定义） |
| **S5** | 换方法复核 | 同上但 `m3_pos/m3_neg` | **换独立 NLP 方法**（排除 method_2 特定噪声） | 自建（字段族笛卡尔积清点） |
| **S6** | 跨方法分歧度 | `group_rank(abs(subtract(<SCOR_m2>, <SCOR_m3>)), subindustry)` | **模型间分歧** = 情绪模糊性轴 | 自建（analyst dispersion 类比） |
| **S7** | 净情绪 × 客观性门控 | `multiply(group_rank(<SCOR_m2>, subindustry), rank(<CONF>))` | **乘性置信度门控**（幅度重分布，权重恒为 rank ⇒ 不扫描常数） | memory 2026-10-30「破 SUB 唯一有效杠杆」（USA wave249 SUB/S 0.332→0.556） |
| **S8** | 净情绪时序异常 | `group_rank(ts_zscore(<SCOR_m2>, 252), subindustry)` | **时序**标准化（vs 横截面） | Da-Engelberg-Gao 2011 ASVI 的形态迁移 |
| **S9** | 净情绪动量 | `group_rank(ts_delta(<SCOR_m2>, 22), subindustry)` | **一阶差分** | 自建 |
| **S10** | NLP 过滤前后的噪声 | `group_rank(ts_mean(subtract(<SCOR_filtered>, <SCOR_raw>), 5), subindustry)` | **同概念双实现之差** = 过滤引入的信息 | 自建（`filtered_*` 专为此设计） |
| **S11** | 客观性水平（**纯 C 类轴**） | `group_rank(ts_mean(vec_avg(m2_obj), 22), subindustry)` | 单用置信度字段本身当信号 | 自建（`obj` 从未被测，ac 近似 0） |
| **S12** | 净情绪高斯化 | `group_rank(ts_quantile(<SCOR_m2>, 252, driver="gaussian"), subindustry)` | **非线性重分布** | memory「`ts_quantile(gaussian)` 抬 SUB +31%」 |
| **S13** | 三方法等权共识 | `group_rank(divide(add(add(<SCOR_m2>, <SCOR_m3>), <SCOR_m4>), 3), subindustry)` | **同概念多字段等权合成**（权重恒 1、不扫描 ⇒ 合规） | 自建（降单方法噪声） |
| **S14** | 注意力 × 情绪交叉 | `multiply(group_rank(<SCOR_m2>, subindustry), rank(vec_sum(valid_tokens_total)))` | **A 类注意力 × B 类方向**（跨类复合） | 论坛 `43541109631895`（78 赞）「要的是异常注意力」的严格实现 |
| **S15** | 无极性语言特征密度 | `group_rank(divide(vec_sum(method_9_feature_2), vec_sum(valid_tokens_total)), subindustry)` | 换 **D 类**（无极性特征，ac 仅 1） | 自建 |

**互异性自检**：字段类轴 3（B / C / D）；加工轴：水平（S4/S5）、分歧（S6）、门控（S7）、时序异常（S8）、一阶差分（S9）、双实现差（S10）、纯置信度（S11）、非线性重分布（S12）、多字段合成（S13）、跨类乘性（S14）、密度比（S15）。**无任何两条只差窗口或常数。**

**展开式速查**（均可直接替换进骨架）：
```
<SCOR_m2> = subtract(vec_avg(snt33_sefke1v1_fkw1_method_2_pos), vec_avg(snt33_sefke1v1_fkw1_method_2_neg))
<SCOR_m3> = subtract(vec_avg(snt33_sefke1v1_fkw1_method_3_pos), vec_avg(snt33_sefke1v1_fkw1_method_3_neg))
<SCOR_m4> = subtract(vec_avg(snt33_sefke1v1_fkw1_method_4_pos), vec_avg(snt33_sefke1v1_fkw1_method_4_neg))
<SCOR_filtered> = subtract(vec_avg(snt33_sefke1v1_fkw1_method_2_filtered_pos), vec_avg(snt33_sefke1v1_fkw1_method_2_filtered_neg))
<CONF> = subtract(1, vec_avg(snt33_sefke1v1_fkw1_method_2_obj))
```

**单位合法性**：`pos`/`neg`/`obj` 均为 **0–1 无量纲分** ⇒ `subtract` 合法、`subtract(1, obj)` 里常数 1 配无量纲合法、`rank` 输出无量纲 ⇒ 全部 `unit_handling=VERIFY` 安全。

---

## 5. 设置档案

- 主档：**GBR / TOP700 / D1 / `FAST` / decay 10 / trunc 0.05 / nanHandling ON / maxTrade OFF / pasteurization ON / VERIFY**
- 理由：`FAST` 已在 `shortinterest3`（S 1.56→1.95）与 `ts_covariance` 二阶矩（1.30→1.60）上**两次独立验证**为慢变量计数族的数量级杠杆（定则 #34）。
- 备选第二档（若 `FAST` 塌）：`MARKET`（`shortinterest3` 次优）/ `REVERSION_AND_MOMENTUM`（中间）。
- **`coverage = 0.32` 是本数据集最大风险** ⇒ 高度依赖「并列假中段」的处理（定则 #41）。S2/S6 的 `ts_zscore` 与 S3/S9/S12 的幅度重分布都部分对冲该风险，但**必须在复盘时先扫 `longCount + shortCount`**：若持仓数 ≪ 909（GBR TOP700 真实可交易容量），说明大部分股票被 nanHandling 填成并列值。

---

## 6. 派发序与判定门（预注册）

| 批 | 模板 | 目的 |
|---|---|---|
| 1 | **S2 + S1** | 核心假设（异常注意力）× 对照组（纯方向基线）—— 同数据集同设置，只改信号轴 ⇒ 严格受控对比 |
| 2 | S3 + S9 | SUB 杠杆跨区验证（乘性门控 vs 高斯化） |
| 3 | S10 + S11 | 换信息源（模型分）/ 广度轴 |
| 4 | S8 + S6 | 多尺度共振 / 时序异常 |
| 5 | S4 + S5 | 分歧度 / NLP 噪声 |
| 6 | S7 + S12 | 动量 / 双非方向轴复合 |

**判定门**（2026-10-31 修订：加入字段类维度）：

- **A 类（`method_1` token 计数）方向轴 + 注意力轴已判负**（S1 −0.24 / S2 −0.32 / S3 −0.11）⇒ **A 类不再投入**，除非有全新经济假设（不是换窗口/换算子）。
- **B 类方向轴已判负**（S4 −0.37）⇒ B 类的**水平/动量/时序异常**形态不再单调；只剩「复合/门控/分歧」形态值得一试。
- **S6（分歧）与 S11（客观性）是最后两条非方向轴。** 若两者 \|S\| < 0.5 ⇒ **A/B/C/D 四类的「方向 + 注意力 + 置信度 + 分歧」四轴全部覆盖完毕** ⇒ 按定则 #18/#19 判 `CONFIRMED-DEAD`（探针 6 / 结构 6 / 字段类 4 ≥ 2）。
- **任何模板 `investability_ratio < 0.3`** ⇒ 信号主要来自不可投资股票，**该条判无效**（S4 即此，0.108）。
- **任何模板 `longCount + shortCount < 400`** ⇒ 覆盖太薄，结论无效（不是信号弱，是没持仓）。
- **翻符号不是出路**：四条探针 S 全为负且 2Y 全为正 ⇒ `multiply(·,−1)` 后 S 最多 0.37 而 **2Y 全部转负**，双向不达标。

**★ 若 `sentiment33` 最终判死，SENTIMENT 塔的剩余路径只有**：换 `fkw{2,3,4,5}` 族（coverage 0.3199–0.3237 与 fkw1 几乎相同 ⇒ **不解决薄覆盖**，预计无增量）⇒ 实际等于**SENTIMENT 塔在本季度 GBR 判结构性不可达**，应把资源转 `fundamental6`（197 字段 / cov 0.4969 / FUNDAMENTAL 塔）。

---

## 7. 实证账本

### 7.1 全量账本（8 探针）：四类字段 × 六种结构 —— **方向全部为负**

统一设置：**GBR / TOP700 / D1 / `FAST` / decay 10 / trunc 0.05 / nanHandling ON / maxTrade OFF / pasteurization ON / VERIFY**

| # | 字段类 | 结构 | alpha | S | F | TO | 2Y | SUB | DD | CW | long+short | invest_ratio |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **S1** | A 计数 | NET 水平 `ts_mean(·,5)` | `3qoYalPQ` | −0.24 | −0.04 | 26.80% | **+0.28** | −0.06 | 18.47% | 0.106 | 910 | — |
| **S2** | A 计数 | ATT 异常注意力 `ts_zscore(·,252)` | `Xg9w2LgX` | −0.32 | −0.06 | 36.04% | **+0.36** | −0.27 | 26.86% | **0.303** | 909 | 0.094 |
| **S3** | A 计数 | NET + `ts_backfill(·,22)` | `pwdJVWp3` | **−0.11** | −0.02 | **13.55%** | **+0.01** | −0.12 | **16.93%** | — | — | 0.727 |
| **S4** | **B 评分** | SCOR 水平 | `gJeqRNxg` | **−0.37** | −0.08 | 35.99% | +0.18 | −0.14 | 24.65% | — | — | **0.108** |
| **S6** | B 评分 | 跨方法分歧 `\|SCOR_m2 − SCOR_m3\|` | `P0ornvjL` | −0.30 | −0.06 | 26.76% | **−0.33** | **+0.15** | 17.42% | — | — | 0.0667 |
| **S11** | **C 客观性** | `group_rank(ts_mean(vec_avg(method_2_obj), 22), subindustry)` | `58E7LerM` | **−0.07** | −0.01 | 14.61% | **+0.32** | +0.05 | 11.22% | — | 910 | 4.5714 † |
| **S10** | B × C | 残差化 `vector_neut(·, rank(obj))` | 在飞 | | | | | | | | | |
| **S15** | B × C | 高决绝子集掩码 `if_else(greater(rank(CONF),0.7), ·, nan)` | 在飞 | | | | | | | | | |

**S 区间 [−0.37, −0.07]，8 条里没有一条为正 ⇒ 翻符号后最高也只有 0.37，距闸 1.58 差 4.3 倍。2Y 区间 [−0.33, +0.36]，同样全部不达标。**

† **`investability_ratio` 在 \|S\| 极小时失效** —— S11 的 `invest_S/S = −0.32/−0.07 = 4.5714`，数学上是负值相除得正大数，**不能读成「信号全来自可投资股票」**。判据补一条边界：**`investability_ratio` 只在 \|S\| ≥ 0.3 时可用**（S2 0.094 / S4 0.108 / S6 0.0667 三条有效且全部 < 0.3 ⇒ 判无效；S3 0.727 / S11 因 \|S\|<0.3 不适用）。

**结构多样性自检**：水平 3 条（S1 NET / S4 SCOR / S11 OBJ，三个不同字段类）· 时序异常 1 条（S2）· 平滑 1 条（S3）· 分歧 1 条（S6）· 残差化 1 条（S10）· 掩码 1 条（S15）⇒ **6 种互异结构**，覆盖 A/B/C 三类字段。**没有任何两探针共用同一结构 + 同一字段类。**

### 7.2 四条判读

1. **★★★★★ 先验 A 在 GBR 上被证实，但方向是「负」而不是「弱」** —— 论坛帖 `43541109631895` 说「纯 sentiment 方向 Sharpe < 0.5」，实测 S1 = **−0.24**。不但弱，而且**符号相反**：GBR TOP700 上「净语调越正面 ⇒ 未来收益越差」。这是经典的**过度反应/反转**效应，而非 Tetlock (2007) 的「负面情绪 → 下跌」漂移。**⇒ 大盘股上新闻语调的信息被日内消化完，剩下的是反转。**
2. **★★★★★ 定则 #38 在新闻域复现：`ts_backfill` 一定救 TO/DD，但把信号一起抹掉。** S3 vs S1：TO 26.80%→**13.55%**（降 49%）、DD 18.47%→**16.93%**，但 **2Y 从 +0.28 塌到 +0.01**（降 96%）、S 从 −0.24 收敛到 −0.11（**向 0 收敛**，即信号消失而非改善）。⇒ **与 `insiders1` 的 I3/I4（TO 174%→8%、S 同步趋 0）是同一机理：平滑救的是噪声，一起救掉的是信号。**
3. **★★★★★ 「异常注意力」先验跨区不成立** —— 论坛帖给了 78 赞的强背书，但 S2（`ts_zscore(ATT,252)`）不但 S 最差之一（−0.32），**CW 0.303 是 limit 的 3 倍**、DD 26.86% 全族最差。机理：`vec_sum(valid_tokens_total)` 是「当日文档总 token 量」，被**超长文档**（完整财报电话会记录可达数万 token）主导 ⇒ 该量的横截面排序不稳定。**⇒ A 类的 `vec_sum` 折叠是失效根因，不是模板问题。**
4. **★★★★★ B 类评分比 A 类计数更差（S4 −0.37 vs S1 −0.24），且可投资性崩溃（invest_ratio 0.108）** —— 这证伪了「连续评分更干净所以更强」的直觉。`invest_ratio = 0.108` 意味着信号几乎全部来自**不可投资的股票**（小票/低流动性），在可投资子集上瓦解。对照 S3 的 0.727 是健康值。**⇒ 判读 B 类时必须以 `investability_ratio` 为第二把尺，不能只看 S。**

### 7.3 批次 2（非方向轴）：在飞

S6 跨方法分歧（`method_2` vs `method_3` 的 \|SCOR 差\|）· S11 客观性水平 —— 这两条是**唯一不依赖方向**的轴；若也全灭，则 A/B/C/D 四类中「方向 + 注意力 + 置信度 + 分歧」四轴覆盖完毕，可按定则 #18/#19 判 `CONFIRMED-DEAD`。

---

## 8. 交叉引用

- 定则 #7（新闻类必须 `ts_mean(·,5)` 前置；`vec_count` 不能用于稀疏事件）→ `docs/reference/template_library_gbr_news104.md`
- 定则 #34（`FAST` 是慢变量计数族的数量级杠杆）→ `template_library_gbr_shortinterest3.md` §6.8.4
- 定则 #41（薄 coverage 的「并列假中段」）→ `template_library_gbr_insiders1.md` §2
- memory「破 SUB 闸的唯一有效杠杆是重塑幅度分布」→ agent memory 2026-10-30 条
- 论坛 `43541109631895`（异常注意力）/ `43583615602711`（2Y 跷跷板）→ 见 `template_library_gbr_shortinterest3.md` 论坛索引
