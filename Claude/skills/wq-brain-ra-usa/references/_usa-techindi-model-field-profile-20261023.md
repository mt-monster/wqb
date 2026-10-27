# techindi_model「Deep Learning Technical Indicator Returns」字段画像与机制档案（USA / D1 / TOP3000）

> as_of 2026-10-23。来源：`get_datasets(region="USA", delay=1, universe="TOP3000")`（平台）
> + `fields WHERE dataset_id=579`（DB，1830 行）。塔位：**other / 未点亮**（USA/D1 仅 analyst、model 点亮）。
> 结构：§0 路由 · §1 结构解剖 · §2 覆盖率画像 · §3 分布与拥挤度 · §4 机制目录 ·
> §5 可用性判读 · §6 已知陷阱 · §7 存档索引。

## §0 路由与元数据

| 项 | 值 |
|---|---|
| id / 名称 | `techindi_model` / Deep Learning Technical Indicator Returns |
| 类别 / 塔 | `other` / **未点亮**（倍率 **×1.4**） |
| coverage / fieldCount | **0.973** / **1830**（全 MATRIX） |
| userCount / alphaCount（平台） | **523 / 1512** |
| valueScore | 4 |
| delay / dataType | 1 / MATRIX |
| DB id | **579**（`datasets` 行 aC 495，落后平台约 3×，一律以平台读数为准） |
| 平台描述 | 把技术指标时序转成图像，用深度学习模仿散户看图交易的行为来预测收益 |

**为什么是它**：承 `chart_model_alpha` 判死（`tracking/USA/runs/usa_cma_w1_notes.md` §12，11 波 30 臂
信号真实但 fitness 结构性封顶）。techindi_model 同时满足：未点亮塔、字段多（1830）、覆盖 0.973、
**16 个模型配置对同一目标并行预测**（= `ai_equity` 已验证的低相关池结构）、且有**独立的期限轴**。

## §1 结构解剖：1830 字段 = 两套并行命名，不是 1830 个独立信号

### 1.1 机器命名 `tm_*`（912 = 16 配置 × 57）

```
tm_<配置>_r1_r5_r10_rh_<变体>_d1_<r1|r5|r10>_<后缀>
```

| 维度 | 取值 | 说明 |
|---|---|---|
| 配置 | `tm_1`(standardized) `tm_4` `tm_8` `tm_10` `tm_11` `tm_12` `tm_13` `tm_14` `tm_15` `tm_20` `tm_22` `tm_25` `tm_28` `tm_33` `tm_35` `tm_36` | 16 个，后 9 个带 `ah3` 变体标记 |
| 变体 | `r1` / `r5` / `r10` | ⚠ 描述文本一律写「1-day forward」，**不是预测期限**，是模型/训练窗口变体 |
| 后缀 | `q1` ×1 · `q2..q5` ×4 · `q2..q5_p0..p(k-1)` ×14 | `q1`=连续回归输出；`qk`=分桶标签(0-based 整数)；`qk_pi`=log-softmax 对数概率 |

每配置 57 字段 = 3 变体 × 19 后缀，个别配置少 5 个（`tm_20` r10 整组缺失）。

### 1.2 人类命名 `{predicted,likelihood,probability,confidence}_*`（915）

| 前缀 | 数量 | 语义（以字段描述为准） | 例 |
|---|---|---|---|
| `predicted_*` | 241 | **该分位组的预测收益**（带单位，不是概率） | `predicted_fifth_quantile_ten_day_return_34` |
| `likelihood_*` | 316 | 落入某桶的**对数**概率（log-softmax） | `likelihood_fifth_quantile_five_day_bucket_four` |
| `probability_*` | 353 | 落入某桶的概率 / 标签 | `probability_fifth_bucket_five_day_label_four_3` |
| `confidence_*` | 5 | 分位数模型置信度（覆盖 1.0） | `confidence_five_quantile_prediction` |

命名轴：`{first|second|third|fourth|fifth}_quantile`（5 分位）或 `_{first..fifth}_bucket`；
`{one|five|ten}_day`；`bucket_{zero..four}` / `label_{one..four}`；尾缀 `_2 _3 _4 _5 _7 _9 _10 _11 _12 _13 _14 _31.._35 _41.._43 _51`。

### 1.3 ⚠ 期限轴只存在于人类命名里

`horizon` token 统计（DB 全 1830 字段）：**`one` 303 / `five` 301 / `ten` 301 / 无期限 925**。
`tm_*` 族**没有**期限轴（全部标 1-day）。⇒

- 要**压换手 / 提单次收益**，唯一入口是 `predicted_*` 的 `five_day` / `ten_day`；
- `tm_*` 族的 `r1/r5/r10` 是**模型变体**，做差得到的是「模型分歧」而不是「期限溢价」，两者经济含义不同，
  不可混称。

## §2 覆盖率画像

### 2.1 总体分位（1830 字段 `fields.coverage`）

| 分位 | q0 | q05 | q25 | 中位 | q75 | q95 | max |
|---|---|---|---|---|---|---|---|
| coverage | 0.9497 | 0.9543 | 0.9571 | **0.9625** | 0.9996 | 1.0000 | 1.0000 |

覆盖率**极高且集中**（最差 0.9497），这是本数据集少见的优势：不需要大规模 `ts_backfill` 就能做多腿组合。
代价是**档位极密**（0.9497 / 0.9543 / 0.9558 / 0.9562 / 0.9569 / 0.9571 / 0.9582 / 0.9606 / 0.9625 /
0.9766 / 0.9989 / 0.9996 / 1.0000 十三档），跨档做差会把缺失写成信号。

### 2.2 `tm_*` 十六配置 × 三变体的 `q1` 覆盖（DB 实测）

| 配置 | r1 | r5 | r10 |
|---|---|---|---|
| tm_10 / tm_11 / tm_22 | 0.9569 | 0.9569 | 0.9569 |
| tm_12 / tm_14 / tm_33 / tm_36 | 0.9625 | 0.9625 | 0.9625 |
| tm_13 | 0.9766 | 0.9766 | 0.9766 |
| tm_15 | 0.9558 | 0.9562 | 0.9558 |
| tm_1 | 0.9543 | 0.9543 | **1.0000** |
| tm_20 | 0.9625 | **1.0000** | 缺 |
| tm_25 | 0.9582 | 0.9582 | 0.9582 |
| tm_28 | 0.9606 | 0.9606 | 0.9606 |
| tm_35 | 0.9571 | 0.9571 | 0.9571 |
| tm_4 | 0.9497 | 0.9497 | 0.9497 |
| tm_8 | **1.0000** | 0.9606 | **1.0000** |

**同覆盖可直接多腿的组**：`{tm_10,tm_11,tm_22}`(0.9569) · `{tm_12,tm_14,tm_33,tm_36}`(0.9625) ·
`{tm_25}` · `{tm_35}` · `tm_13` 单腿 · `tm_4` 单腿。

### 2.3 ⚠ 覆盖率恰为 1.0000 的腿 = 合成填充腿

`tm_10_*_r5_q5_p2`、`tm_22_*_r1_q5_p1`、`tm_13` 的多个桶、`tm_8` 的 q1(r1/r10) 等覆盖**恰好 1.0**，
而同组兄弟腿是 0.95x。判断：这些缺失行被**默认值填满**（log-softmax 下默认 0 ⇔ 概率 1），
不是真的多覆盖了 4%。

**五桶覆盖全部等于 0.9569（无 1.0 腿）的配置**：`tm_11`（三个变体全 OK）、`tm_12`、`tm_14`、`tm_36`、
`tm_25`、`tm_35`、`tm_22`(r5)、`tm_1`(r5/r10)、`tm_20`(r1)。
⇒ 任何**分桶概率**类多腿臂的基准配置应取上表之一，首选 **`tm_11_r5`**。

### 2.4 `predicted_*` 的覆盖分布（波 2 主力的关键先验）

| 组 | 字段数 | 覆盖 | 备注 |
|---|---|---|---|
| `predicted_fifth_quantile_ten_day_return*` | 14 | **13 个 0.9996** + 1 个 0.9989 | **最干净的高覆盖组**，适合共识/阈值臂 |
| `predicted_fifth_quantile_{one,five}_day_return*` | 各 ~14 | 以 0.9996 为主 | 同上 |
| `predicted_first_quantile_ten_day_return*` | 13 | **0.9497–1.0000 极不均匀** | 做「顶−底」价差必须先选同档（如 `_5` / `_51` / `_6` 同为 0.9625） |

## §3 分布与拥挤度

| 项 | 观测 | 判读 |
|---|---|---|
| 字段级 aC | **1526/1830 为 0**；≥4 的仅 ~40 个 | 绝大多数字段**从未被用于任何 alpha** ⇒ 不是「被别人挖烂」的数据集 |
| 最高 aC | 14（`likelihood_fifth_quantile_five_day_bucket_four_3`）、11、8（`predicted_fifth_quantile_ten_day_return_34`） | 高 aC 集中在 `predicted_*` / `likelihood_*` 的五分位顶桶 |
| 数据集级 aC（平台） | **1512** | 中等拥挤；相对 1830 字段，人均使用深度低 |
| 值分布 | q1 描述明写 **"must be winsorized before use"**；概率族混用 "Probability" 与 "Log-probability (log-softmax)" | ⇒ **一律先 `rank()` 再运算**（对任何单调变换免疫，自动解决 winsorize 与 log/linear 量纲混用） |
| 更新频率 | 日频（D1，MATRIX） | 无事件稀疏问题 |
| 量纲 | 收益类（`predicted_*` 带收益单位）vs 概率类（0–1 / log 空间）vs 标准化分数（`q1`） | 跨族不可直接相加，必须 rank 后组合 |

## §4 机制目录（每个机制对应一个可证伪的经济假设）

| # | 机制 | 假设 | 字段入口 | 首测波次 |
|---|---|---|---|---|
| M1 | 连续水平 | 模型对「前瞻市场中性收益」的横截面排序有真实预测力 | `tm_*_q1` | **tm_w1 W1/W2** |
| M2 | 集成共识 | 16 个配置是同目标的并行预测，秩和可降噪；共享同一覆盖率档的配置互为冗余 | `tm_*_q1` 多配置 | **tm_w1 W3/W4** |
| M3 | 模型变体分歧 | `r1/r5/r10` 三个训练窗口在同一股票上意见不同 ⇒ 残差型 alpha，天然低相关 | `tm_11_{r1,r5,r10}_q1` | **tm_w1 W5/W6** |
| M4 | 分位置信 | 分类头的顶−底概率差 = 「模型有多确信该股在顶端」，与回归头信息通道不同 | `tm_11_r5_q5_p{0,4}` | **tm_w1 W7/W8** |
| M5 | 头部分歧 | 回归头与分类头对同一目标排序不同时，差本身可作信号 | `q1` vs `(p4−p0)` | **tm_w1 W9/W10** |
| M6 | **期限结构** | 1/5/10 日预测的差 = 市场对短周期与中周期的定价分歧；10 日腿单次收益更大、换手更低 | `predicted_*_{one,five,ten}_day_return*` | 波 2（待） |
| M7 | 分位组价差 | 顶分位预测收益 − 底分位预测收益 = 经典多空价差（带真实收益单位） | `predicted_{fifth,first}_quantile_*` | 波 2（待） |
| M8 | 置信加权 | 用 `confidence_*` / 概率熵给 M1–M5 的腿加权（高置信时仓位更大） | `probability_*` + `confidence_*` | 视 M1–M5 结果 |

**禁止混轴**：M1–M5（`tm_*` 族，1-day 变体）与 M6–M7（`predicted_*` 族，带期限）**不在同一臂内混用**，
否则「分歧」与「期限」两种解释互相污染。

## §5 可用性判读

| 判据 | 结论 |
|---|---|
| 覆盖率 | **优**（最差 0.9497），多腿组合几乎无 backfill 负担 |
| 字段数 / 结构 | **优**（1830，16 配置 × 3 变体 × 19 后缀 + 带期限的人类命名族） |
| 拥挤度 | **中**（平台 aC 1512，但 83% 字段 aC=0）⇒ 有白空间 |
| 塔位 | **优**（other 未点亮，×1.4） |
| 语义合规 | 1830 字段全部判定为 signal，`s1_semantic_techindi_model` 黑名单 **0** 字段 |
| 主要风险 | ① 覆盖率档位太密，跨档做差易造假信号；② `q1` 需 winsorize、概率族 log/linear 混用 ⇒ 必须 rank；③ 模型是「模仿散户看图」，可能天然高换手（首波实测换手率是关键观测） |

## §6 已知陷阱（写进下一波的必读项）

1. **`tm_*` 的 `r1/r5/r10` 不是期限**。描述模板一律写 1-day。当变体差用，别当期限溢价解释。
2. **覆盖 1.0 的腿是合成填充**，混进多腿臂会把缺失变成概率质量（log-softmax 下 0 ⇔ p=1）。
3. **`q5_p2` 在 `tm_10` 的 r5/r1 上是 1.0，在 r10 上直接缺失** ⇒ 想用 5 桶全概率，取 `tm_11`（三变体全 0.9569）。
4. **`q1` 字段名在多个数据集里重名**（如 `tm_13_r1_q1` 同时存在于 ds 579 与 ds 964，覆盖 0.9766 vs 0.9816）。
   查覆盖一律加 `dataset_id=579` 过滤，否则会读到别家的值。
5. **`predicted_*` 的顶桶族覆盖 0.9996，底桶族 0.9497–1.0** ⇒ 「顶−底价差」不能直接相减。
6. **算子调用点 <10**（gate.py 静态闸）。多腿臂要先算调用点数：`decay(1) + 加减(1~3) + rank×腿数`，超了先简化。

## §7 存档索引

| 产物 | 路径 |
|---|---|
| 本字段画像 | `Claude/skills/wq-brain-ra-usa/references/_usa-techindi-model-field-profile-20261023.md` |
| 语义台账（S1） | DB `ledger_kv`: `USA/s1_semantic_techindi_model`（1830 signal / 0 blocked） |
| 体检包（降级） | `tracking/mining/field_inspect_usa_techindi_model.json`（coverage-only；完整包 `tools/gen_field_inspect_packs.py --region USA --dataset techindi_model`） |
| 首波设计与派发记录 | `tracking/USA/runs/usa_tm_w1_notes.md` |
| 首波表达式 | `tracking/USA/runs/usa_tm_w1{a,b}.txt`（各 5 条） |
| 首波设置 | `tracking/USA/runs/usa_tm_w1_spec.json` |
