# sentiment21 模板库（HKG / TOP800 / D1）· 2026-11-04

> 字段来源：`get_datafields(region=HKG, universe=TOP800, delay=1, dataset_id=sentiment21)`
> 数据集资质：**138 字段全部 MATRIX / coverage 1.0 / 单字段 alphaCount 1–16 / userCount 1–11**
> category = `sentiment` ⇒ **不在禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL}**，可做单塔 ATOM（不占组合配额）。
> 模板来源标注：[自建] 自设计；[文献] 外部金融论文先验（**未在线核验**：本会话 `web_search` 返回 402、`search_forum_posts` 持续挂起，仅凭既有知识引用）。

## 字段结构（138 个，五套窗口族）

| 族 | 命名 | 字段数 | 说明 |
|---|---|---:|---|
| 基础 | `snt21_{pos,neg,neut}_{conf_low,conf_up,max,mean,median,min,std}` | 21 | 无窗口前缀的综合情绪 |
| 2 日窗 | `snt21_2{pos,neg,neut}_{同上 7 stat}` | 21 | 短窗情绪 |
| 3 日窗 | `snt21_3{...}` | 21 | |
| 4 日窗 | `snt21_4{...}` | 21 | |
| 5 日窗 | `snt21_5{...}` | 21 | |
| dts 族 | `snt21_{2,3,4,5}dts_{gen,sop,tuen}` | 12 | 负/正/中情绪的**标准差** |
| dts 基础 | `snt21dts_{gen,sop,tuen}` | 3 | |
| 无 std 套 | `snt21{pos,neg,neut}_{conf_low,conf_up,max,mean,median,min}` | 18 | 第二套打分（无下划线） |

三类情绪：`pos`（正面）/`neg`（负面）/`neut`（中性）。七类统计量：
`conf_low`/`conf_up`（置信区间下/上界）、`max`/`min`（极值）、`mean`（均值）、`median`（中位）、`std`（标准差）。

## 12 个结构互异模板

> 互异维度：**矩**（水平 / 一阶差分 / 二阶方差 / 三阶偏度）· **算子几何**（归一化 / 比值 / 差 / 绝对值 / 秩）· **分组轴**（sector / industry）· **窗口语义**（22 / 66 / 2d-vs-5d 跨窗）· **非线性**（zscore / rank / reverse）。

### S1 · 净情绪水平（一阶矩 · 水平）[自建]
```
group_zscore(ts_mean(divide(subtract(snt21_pos_mean, snt21_neg_mean), add(add(snt21_pos_mean, snt21_neg_mean), 0.0001)), 22), sector)
```
7 算子。假设：净正面情绪溢价（情绪延续）。分母做强度归一，剔除"情绪总量"混淆。

### S2 · 相对分歧（二阶矩 · 离散度）[文献 Miller 1977]
```
reverse(group_zscore(ts_mean(divide(add(snt21_pos_std, snt21_neg_std), add(add(snt21_pos_mean, snt21_neg_mean), 0.0001)), 22), sector))
```
7 算子。假设：意见分歧（dispersion）= 卖空受限下的高估，故**反向**。分歧理论经典预测。

### S3 · 置信区间宽度（信息不确定性 · 一阶）[文献 Zhang 2006]
```
reverse(group_zscore(ts_mean(divide(subtract(snt21_pos_conf_up, snt21_pos_conf_low), add(snt21_pos_mean, 0.0001)), 22), sector))
```
6 算子。假设：情绪区间越宽 = 信息越模糊 → 不确定性折价。

### S4 · 区间方向不对称（尾部不对称）[自建]
```
group_zscore(ts_mean(subtract(snt21_pos_conf_up, snt21_neg_conf_up), 22), sector)
```
5 算子。假设：「最好的乐观情形」减「最坏的悲观情形」= 尾部不对称性，与水平量（S1）正交。

### S5 · 中性占比（无信息度）[文献 Merton 1987]
```
reverse(group_zscore(ts_mean(divide(snt21_neut_mean, add(add(snt21_pos_mean, snt21_neg_mean), add(snt21_neut_mean, 0.0001))), 22), sector))
```
7 算子。假设：中性情绪占比高 = 缺乏信息覆盖 → 投资者认知度低 → 折价（反向）。

### S6 · 情绪加速度（跨窗一阶差分）[文献 Tetlock 2007]
```
group_zscore(ts_mean(subtract(divide(subtract(snt21_2pos_mean, snt21_2neg_mean), add(add(snt21_2pos_mean, snt21_2neg_mean), 0.0001)), divide(subtract(snt21_5pos_mean, snt21_5neg_mean), add(add(snt21_5pos_mean, snt21_5neg_mean), 0.0001))), 22), sector)
```
13 算子。假设：2 日窗净情绪减 5 日窗 = 情绪**改善速度**，领先于水平。

### S7 · 情绪波动率（dts 时序分散）[自建]
```
reverse(group_zscore(ts_mean(divide(snt21dts_sop, add(snt21dts_gen, 0.0001)), 22), sector))
```
6 算子。假设：正情绪本身不稳定 = 情绪泡沫 → 后续回撤，反向。

### S8 · 分布偏斜代理（三阶矩 · 偏度）[文献 Barberis & Huang 2008]
```
group_zscore(ts_mean(divide(subtract(add(snt21_pos_max, snt21_pos_min), multiply(2, snt21_pos_median)), add(subtract(snt21_pos_max, snt21_pos_min), 0.0001)), 22), sector)
```
10 算子。假设：(max+min−2·median)/(max−min) 为偏度代理；右偏（少数极乐观）→ 后续反转。

### S9 · 尾部乐观缺口（极值 vs 中位）[文献 De Bondt & Thaler 1985]
```
group_zscore(ts_mean(subtract(snt21_pos_max, snt21_pos_median), 22), sector)
```
5 算子。假设：极端乐观值相对中位的抬升 = 过度反应，随后均值回复。

### S10 · 情绪不稳定度（净情绪的时序二阶矩）[自建]
```
reverse(group_zscore(ts_std_dev(divide(subtract(snt21_pos_mean, snt21_neg_mean), add(add(snt21_pos_mean, snt21_neg_mean), 0.0001)), 22), sector))
```
7 算子。假设：净情绪时序波动大 = 叙事反复，风险溢价。

### S11 · 情绪突变（绝对变化）[自建]
```
reverse(group_zscore(ts_mean(abs(ts_delta(divide(subtract(snt21_pos_mean, snt21_neg_mean), add(add(snt21_pos_mean, snt21_neg_mean), 0.0001)), 5)), 22), sector))
```
8 算子。假设：情绪跳变（无论方向）预示高波动 → 反向。

### S12 · 季度窗 + industry 轴（非线性 · 秩空间）[自建]
```
group_rank(ts_mean(divide(subtract(snt21_pos_mean, snt21_neg_mean), add(add(snt21_pos_mean, snt21_neg_mean), 0.0001)), 66), industry)
```
7 算子。窗口 66 = 季度（有明确经济含义）；`group_rank` 与 `group_zscore` 是不同非线性，industry 比 sector 更细。

## 待验的双塔用法（若 S1–S12 任一条 S ≥ 1.0）

`senti × PV` 属「禁混集合内 × 集合外」⇒ **允许**，但计入 ≤5 的组合类型额度（已用 0/5）。
已验证的构型是 **bucket 分组轴**（`trade_when` 与线性复合双双证否）：

```
reverse(group_zscore(ts_mean(<PV 裸核>, 126), bucket(rank(<snt21 字段>), range="0,1,0.2")))
```
代价：bucket 轴本身吃掉约 0.5 的 2Y（2.10 → 1.16–1.57），固定档下结构性过不了 1.58 阶梯闸。
⇒ **优先走单塔 ATOM（不付 2Y 代价）**，双塔只在单塔确认出货后再考虑。

## 已判死的同批候选（本轮画像结论）

| 数据集 | category | 字段 | 判定 |
|---|---|---|---|
| `risk59` | risk | 16 全 VECTOR | 判死（需表达式级 `fix_vector_fields` 才可能用） |
| `news104` | news | 11 全 VECTOR | 判死 |
| `shortinterest3` | shortinterest | 56 全 VECTOR | 判死 |
| `news_sentiment_transfer` | sentiment | 20 MATRIX / cov 1.0 / ac 1–9 | **实测无信号**：T1 水平随动 S 0.42、T2 离散度 S 0.67，均挂 3 闸 ⇒ 判死该数据集的聚合情绪类骨架 |
| `risk88` | risk | 80 全 MATRIX / cov 0.8844 | **待验**：字段描述全写 "in ASI region"（区域错位红灯）；结构为 MFM 因子暴露（`rsk88_mfm_ase1_{ctn_<国家>,ind_<行业>,dsrt}`）+ `alternative_market_cap_usd` |

**教训**：`news_sentiment_transfer` 与 `sentiment21` 同属 sentiment 塔、同为 cov≈1.0 / 极冷门，但前者只有简单聚合分数（average/max/min/skewness），后者有 **置信区间 + 标准差 + 三分类** 的完整分布刻画。**冷门度高（ac 1–16）本身不保证有信号，要看字段是否刻画到"分歧/不确定性"维度**——这正是情绪类 alpha 的真正来源。
