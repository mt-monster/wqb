# 波 203 — sentiment22 × 10 个结构互异模板 × 双中性化：概率型情感字段的纹理墙

- 日期：2026-10-29
- 区域/设置：USA / TOP3000 / D1 / decay=5 / truncation=0.08 / nanHandling=ON / maxTrade=OFF / unitHandling=VERIFY
- 塔位：平台实测 `pyramid_short = sentiment`，`pyramids.list = [USA/D1/SENTIMENT, multiplier 1.4]`（全部 20 条一致）
- 批：203a = `63eWWfGZ4gmb8T4tBBO3oM` @ `SLOW_AND_FAST`；203b = `28zKAFbrB5g5byix1Kiot8W` @ `FAST`
- **结论：FAIL 0/20。最高 |Sharpe| = 0.77。判死。**

---

## 1. 为什么先打 sentiment22

`get_pyramid_alphas` 显示 USA/D1 本季度仅 `model:4 / analyst:6 / earnings:1` 点亮，`sentiment / other / option / news / pv / risk / insiders / shortinterest / macro / fundamental / institutions / socialmedia / imbalance` **全部为 0**。乘数排序 `other 1.4 = sentiment 1.4 > option 1.3 > news 1.2`。

OPTION 塔已被全面封锁（`order_flow_imb` 波 202 全灭 + `option40`/`option9`/`option3`/`option_chart_model`/`option_horizon_decomp` 均判死或触顶），因此转 SENTIMENT 塔。

同 category 三候选对比：

| 数据集 | 字段数 | 覆盖率 | alphaCount（实测） | virgin | 判定 |
|---|---|---|---|---|---|
| **sentiment22** | 210 | **0.9996** | **692** | **59/210** | **选它**（无覆盖墙 + 最不拥挤） |
| sentiment23 | 210 | 0.9996（同构） | 1571 | 12/210 | 拥挤度 2.3×，留备 |
| news_transformer_scores | 315 | 0.6923–0.8810 | 179 | 161/315 | 按时段切分，有覆盖墙，留作 NEWS 塔 |

**选区原则（本轮确立）**：同构数据集之间先看「覆盖率 × 拥挤度」，不看 valueScore。`news_transformer_scores` valueScore 5.0 高于 sentiment22 的 4，但其覆盖率按 pre/main/post 时段断裂到 0.69–0.88，存在覆盖墙；sentiment22 的 210 字段全部 cov ≥ 0.95 ⇒ 选 sentiment22。

## 2. 字段结构：三根轴，其中两根是伪自由度

210 字段 = **5 个模型变体（base / 2 / 3 / 4 / 5）× 3 个极性（pos / neut / neg）× 7 个统计量（mean / median / min / max / std / conf_low / conf_up）= 105**，加 **15 个 `dts` 时间序列聚合**（105 + 15 = 120 ≠ 210，差额为变体 2/3/4/5 的重复后缀 id）。

命名两族（混用会静默出错）：
- **base 无下划线分隔且必带数字后缀**：`snt22pos_mean_270`、`snt22neg_mean_253`、`snt22_2pos_mean`（变体有下划线、无后缀）
- **base 变体没有 `std` 字段**，std 只出现在 variant 2/3/4/5
- **`dts` 族同名根不同语义**：变体族 `snt22_2dts_gen_166` 是**水平**；base 族 `snt22dts_gen_265` 是 **std**

派生恒等式（决定伪多样性的部分）：

```
conf_up − conf_low = 3.92·σ            ⇒ 区间宽度 ≡ std 的仿射变换
(conf_up + conf_low) / 2 = mean        ⇒ 单端点 ≡ mean + 常数·std
pos + neut + neg = 1（三分类概率）      ⇒ 换桶 ≡ 单调变换
```

⇒ **真正的正交自由度只有三类**：① `pos − neg`（极性差，一阶矩方向）② `pos_conf_up − neg_conf_low`（跨极性跨度，不可由 std 线性表示）③ `neut`（信息真空度）。其余「换桶 / 换统计量 / 换变体」都是同一颗信号的仿射重排。

本波 10 个模板正是按这三类正交自由度 + 算子几何铺设，未落进伪多样性陷阱。

## 3. 十个结构互异模板与结果

| # | 结构差异点 | 表达式 | S (SAF) | S (FAST) | TO (SAF) |
|---|---|---|---|---|---|
| T1 | 极性差·水平·一阶矩 | `ts_zscore(ts_mean(subtract(snt22pos_mean_270, snt22neg_mean_253), 22), 252)` | 0.35 | 0.22 | 19.10% |
| T2 | 极性比·有界商式 | `ts_zscore(ts_mean(divide(snt22pos_mean_270, add(snt22pos_mean_270, snt22neg_mean_253)), 22), 252)` | 0.31 | 0.33 | 18.46% |
| T3 | **二阶矩·分歧度** | `ts_zscore(ts_mean(snt22_2neg_std, 22), 252)` | −0.31 | −0.53 | 21.19% |
| **T4** | **跨极性跨度（唯一非仿射量）** | `ts_zscore(ts_mean(subtract(snt22_2pos_conf_up, snt22_2neg_conf_low), 22), 252)` | **0.77** | 0.37 | 20.14% |
| T5 | 尾部极值差·秩几何 | `ts_rank(subtract(snt22pos_max_257, snt22neg_max_255), 252)` | 0.19 | 0.18 | **148.47%** |
| T6 | 极性耦合·双变量相关 | `reverse(ts_zscore(ts_corr(snt22pos_mean_270, snt22neg_mean_253, 66), 252))` | −0.28 | −0.61 | 14.62% |
| T7 | 慢速累积融入 | `ts_zscore(ts_sum(subtract(snt22pos_mean_270, snt22neg_mean_253), 66), 252)` | −0.24 | −0.60 | 11.79% |
| T8 | 语调一阶差分 | `ts_zscore(ts_av_diff(ts_mean(subtract(snt22pos_mean_270, snt22neg_mean_253), 22), 66), 252)` | 0.09 | −0.04 | 20.37% |
| T9 | 跨模型分歧 | `ts_zscore(ts_mean(subtract(snt22_2pos_mean, snt22pos_mean_270), 22), 252)` | 0.71 | 0.18 | 20.18% |
| T10 | 中性真空度 | `reverse(ts_zscore(ts_mean(snt22_2neut_mean, 66), 252))` | 0.43 | 0.30 | **10.37%** |

**没有一条过 S 闸（1.58）。** 20 条中 15 条 |S| < 0.45。

## 4. 归因：这不是卡闸，是信号不存在

四条独立证据同时成立：

1. **换手正常**。除 T5 外全部落在 **9.85%–21.19%**，远低于 70% 上限；`HIGH_TURNOVER` 只在 T5 触发（148%/152%）。⇒ 不是换手墙。
2. **持仓分散正常**。longCount 1145–1590、shortCount 1538–1980，`CONCENTRATED_WEIGHT` 仅 T5 触发。⇒ 不是集中度墙。
3. **margin 量级差两个数量级**。全部落在 **1e-05 ~ 3.58e-04**，而过闸需要的 margin 在 1.6e-03 量级（对照 insider_trx_matrix B 档冠军 `O0Jgd7Y7` margin 3.4e-03）。⇒ 每单位交易赚不到钱，是信号微弱而非成本高。
4. **SUB 闸多数反而 PASS**（T3/T6/T7 pass）。⇒ 连「大票有信号、小票没有」这种典型形态都不存在。

**机理**：`snt22*` 是模型输出的**三分类概率**，不是情绪强度。概率被压缩在 [0,1] 且多数股票高度集中于中性值 ⇒ 横截面可用变异极小；5 个「模型变体」只是同一个概率换了估计器，不提供新信息维度。横截面上真正变化的更可能是**新闻覆盖密度**（有没有被报道），而非**情绪方向**（报道好坏），后者才与未来收益相关。

**唯一有统计结构的两个方向**（但幅度不足）：
- T3 `neg_std` 二阶矩：**稳定负号**（−0.31 / −0.53）⇒ 负面语调分歧度高 → 未来收益低，符合 Miller (1977) 卖空受限 + 意见分歧定价。方向对，量级差 3 倍。
- T6 `ts_corr(pos, neg)` reverse：**稳定负号**（−0.28 / −0.61 / 2Y −1.03 / −1.75）⇒ 正负语调同向波动（模型不确定）→ 收益差。同上，方向对量级不足。

**T4 与 T9 的 0.77 / 0.71 是假信号**：两者 2Y 分别是 **−0.28** 和 **−1.01**，符号翻转 ⇒ 收益集中在训练期前段、后两年反向，典型衰减/过拟合形态，不可用。

## 5. 反实证：SLOW_AND_FAST 优于 FAST（推翻论坛共识）

论坛帖 `40847481080087`（**94 赞**）称「sentiment / news 类数据最适合相关性算子 + FAST 中性化」。本轮 20 条给出**反向实证**：

| 模板 | S (SLOW_AND_FAST) | S (FAST) | Δ |
|---|---|---|---|
| T9 跨模型分歧 | 0.71 | 0.18 | **+0.53** |
| T4 跨极性跨度 | 0.77 | 0.37 | +0.40 |
| T7 慢速累积 | −0.24 | −0.60 | +0.36 |
| T6 极性耦合 | −0.28 | −0.61 | +0.33 |
| T3 二阶矩 | −0.31 | −0.53 | +0.22 |
| T1 极性差 | 0.35 | 0.22 | +0.13 |
| T8 一阶差分 | 0.09 | −0.04 | +0.13 |
| T10 中性真空 | 0.43 | 0.30 | +0.13 |
| T5 尾部极值 | 0.19 | 0.18 | +0.01 |
| T2 极性比 | 0.31 | 0.33 | −0.02 |

**9/10 模板 SLOW_AND_FAST 更优，平均差 +0.24。**

**读法**：sentiment 是慢变量（22–66 日累积窗口）。`FAST` 中性化把慢速风格成分当作风格因子剥离，连带把慢速情绪信号一起剥掉了；`SLOW_AND_FAST` 保留慢成分。⇒ **「情感数据配 FAST」这条论坛结论不适用于慢窗口情感聚合，只适用于快节奏新闻事件信号。**

## 6. 判死与后续

已落库：`USA-SENTIMENT22-PROBABILITY-TEXTURE-DEAD`（layer=dead_end，含 10 模板 × 双中性化完整对照表 + 20 个 alpha_id）。

**下次怎么办（写入 rule）**：
1. SENTIMENT 塔**不要**再用 sentiment22 的概率类字段。
2. 若仍走 SENTIMENT，必须换**非概率型**信号源（情绪强度分、事件计数、新闻量），不要换概率桶 —— 换桶是仿射重排。
3. 概率型字段做横截面时先与「新闻覆盖密度」正交化（`ts_count_nans` / 覆盖度分位做 bucket 中性化），分离「有没有被报道」与「报道好坏」。
4. **下一条点塔路径优先级**：① OTHER 塔（1.4×）已有 6 颗 prod<0.70 现成候选，先变现；② NEWS 塔（1.2×）未试。

## 7. 留项

- `sentiment23`（同构 210 字段、alphaCount 1571、仅 12 virgin）：与 sentiment22 结构几乎相同，**判死可继承**，不另跑。
- `news_transformer_scores`（315 字段）：真第三维是**时段轴**（pre/main/post），与 sentiment22 的「模型变体轴」正交，留作 NEWS 塔候选。
- `dts` 族 15 个字段本波未用（同名根语义分裂：变体族=水平、base 族=std）。若重开 sentiment 战场，这是唯一未探的字段组。
