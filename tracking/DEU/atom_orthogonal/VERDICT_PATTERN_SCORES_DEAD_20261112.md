# 判死：pattern_scores（504 字段 K 线形态相似度）在 DEU 无 alpha

日期：2026-11-12
BE156 multisim 1HhSE9dbP4ADb10X7SS8lC2（10 臂，修正 group_rank 参数错后重测）

## 实测全灭

| 臂 | 形态字段 | alpha | S | F | 2Y | sub | fail |
|---|---|---|---:|---:|---:|---:|---:|
| Y3 下降楔形 | min_similarity_continuation_falling_wedge | pwamao8j | **0.56** | 0.27 | 1.13 | 0.35 | 3 |
| Y7 V顶-V底 | 两形态差 | YPa6anAA | 0.49 | 0.23 | 0.40 | 0.41 | 3 |
| Y4 向上缺口 | breakaway_gap_up_dynamic_simscore_60 | 78YWY0Jv | 0.02 | 0.00 | 0.09 | -0.05 | 4 |
| Y10 缺口-楔形 | 差 | 3q0w037z | -0.37 | -0.15 | -0.05 | -0.31 | 4 |
| Y2 V底 | max_similarity_reversal_v_bottom_pattern | 88NbN7nq | -0.39 | -0.16 | -0.23 | -0.42 | 4 |
| Y6 V底均值 | avg_similarity_v_reversal_bottom | VkNVNq8J | -0.43 | -0.19 | 0.03 | -0.33 | 4 |
| Y1 V顶反转 | max_similarity_v_reversal_top | LLKWKqnM | -0.47 | -0.22 | -0.50 | -0.37 | 4 |
| Y5 上升楔形反转 | avg_similarity_rising_wedge | LLKWKqkv | -0.48 | -0.22 | -0.02 | -0.27 | 4 |
| Y9 V顶反转+V底 | 双腿 | E5Q1QYwJ | -0.49 | -0.23 | -0.40 | -0.41 | 4 |
| Y8 V底-上升楔 | 差 | 78YWY0dv | **-0.74** | -0.41 | -0.29 | -0.53 | 4 |

**最高 0.56，8/10 臂为负，10/10 fail≥3。**

## 判死结论

pattern_scores 的「K 线形态相似度」字段在 DEU TOP500 D1 上无可用 alpha。

机理：这类字段衡量当前价格形态与历史形态模板的相似程度，本质是技术形态识别的相似度打分。问题在于——
1. 它已有 lag（相似度基于历史窗口算出），对 D1 而言信息已滞后；
2. 形态识别在截面上的区分度低（大量股票同时匹配同一形态，无区分）；
3. 平台已有 pv 类动量/反转因子覆盖同一信息面。

我同时检查了方向假设（V顶应反向、上升楔形应反向），反向后幅度仍只有 +0.4~+0.5，远低于闸线 1.58 ⇒ 不是方向问题，是无信息。

## 踩坑记录：group_rank 第二参是分组轴不是窗口

BE151 那批 10 臂全批报：
`Incompatible unit for input of "group_rank" at index 1, expected "Unit[Group:1]", found "Unit[]"`

根因：我写了 `group_rank(max_similarity_v_reversal_top, 22)`，本意是「22 日窗口的均值再排序」，
但 `group_rank(x, group)` 的第二参是**分组轴**，传 22 就把整数当分组。

正确写法：`group_rank(ts_mean(<field>, 22), sector)` —— 窗口交给 `ts_mean`，分组轴交给 `sector`。

⇒ **纪律：`group_*` 系列（group_rank/group_zscore/group_neutralize）的第二参只能是 GROUP 类型字段**
（sector/market/subindustry/densify(...)/bucket(rank(...)) 或 pv29 的 GROUP 类聚类标签）。

## 合并判死清单（本战役累计）

| 数据集/族 | 最好 S | 状态 |
|---|---:|---|
| insiders 非 holdings 维度 | 1.29 | 判死 |
| RISK（rsk60_*）| 1.37 | 判死 |
| SHORTINTEREST 次级维度 | 1.11 | 判死 |
| other455 竞争PCA | 1.21 | 判死 |
| SENTIMENT 域名热度 | 1.37 | 判死 |
| model264（ML 趋势概率）| 0.74 | 判死 |
| pattern_scores（K线形态）| 0.56 | 判死 |