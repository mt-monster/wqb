# 用户指定六数据集：探针实测结果（2026-11-10 12:3x）★ 推翻 cov 判死

## 一、★★★ 核心发现：cov=0 是 meta 造假，三个数据集实际都有十年满覆盖

探针 sim `3ufEWZ2pC52Zb9v1gF5dYPCC`，6 条全部 COMPLETE，**逐年 longCount 全部 > 0**：

| 数据集 | 平台 cov | 探针 alpha | 2014 | 2018 | 2021 | 2023 | 覆盖判定 |
|---|---:|---|---:|---:|---:|---:|---|
| **analyst10** | **0** | omExVJkk（anl10_smartest_tbv_ff） | 140 | 157 | 198 | 189 | ✅ **十年满覆盖** |
| **analyst10** | **0** | 6Xd5zoQP（analyst_innovation_tbv_innovation_score_fy1） | 124 | 162 | 197 | 191 | ✅ **十年满覆盖** |
| **continuation_score** | **0** | kqNzQWMP（ascending_channel_similarity_dispersion） | 148 | 179 | 238 | 217 | ✅ **十年满覆盖** |
| **continuation_score** | **0** | mLoEZ0N1（avg_similarity_bullish_flag） | 151 | 181 | 236 | 218 | ✅ **十年满覆盖** |
| **sentiment33** | 0.3258 | 9qxNJdOq（snt33_sefke1v1_fkw1_method_3_neg） | 142 | 118 | 203 | 207 | ✅ **十年满覆盖** |
| **sentiment33** | 0.3214 | LLM0kmYe（sentiment_model7_score1_fkw4） | 142 | 125 | 244 | 237 | ✅ **十年满覆盖** |

### ⇒ 判据 NA（本轮最高价值，跨区通用）

**平台 `coverage` / `meta_cov` 完全不可作为「有无供数」的判据。**
- analyst10 与 continuation_score 的 **53 / 560 个字段 cov 全为 0**，
  但实测**十年每年 longCount 124~238**（满覆盖）。
- sentiment33 cov 显示 0.32，实测 lc 118~253（远好于 32% 的暗示）。

**这直接推翻本战役此前一批「因 cov=0 而排除」的数据集判定**，包括：
macro27 / earnings6 / earnings_sent_matrix / option1 / option_chart_model /
socialmedia12 / imbalance5 / event_ml_signals / fundamental1·17·72·86·89·90·93 等。

**正确做法（skill Phase D.6 已明文，本轮实证）**：
1. 判断有无供数**只能靠探针仿真 + `get_alpha_yearly_stats` 逐年 longCount**；
2. 探针写法：`group_rank(ts_mean(ts_backfill(<field>,132),22), <axis>)` —— 简单结构最大化 lc；
3. VECTOR 字段先 `vec_avg`；
4. 一个数据集选 2 个高 uc 字段即可定性（本轮 6 条探针成本极低）。

## 二、探针信号强度（简单 ts_mean 结构，未做机制设计）

| alpha | 数据集 | S | 2Y | 逐年 S（2014→2023） |
|---|---|---:|---:|---|
| omExVJkk | analyst10 | 0.04 | 0.17 | -0.16, 0.93, -0.69, -0.72, 0.79, -1.14, 0.23, 0.35, -0.19, 0.58 |
| 6Xd5zoQP | analyst10 | 0.47 | 0.27 | 0.86, -0.76, 0.18, 0.46, 0.22, 0.73, -0.26, **3.11**, -0.01, 0.54 |
| kqNzQWMP | continuation_score | 0.04 | 0.99 | -1.06, -0.05, 0.28, 0.14, 0.34, **1.96**, -1.47, -1.18, **1.65**, 0.29 |
| mLoEZ0N1 | continuation_score | 0.00 | 0.33 | 0.33, 0.33, 0.11, -0.70, -0.80, -0.68, -0.37, 1.00, 0.74, -0.12 |
| 9qxNJdOq | sentiment33 | 0.21 | 1.06 | -0.63, 0.69, 0.10, 0.73, 0.31, 0.36, -1.60, 1.05, 0.01, **2.32** |
| LLM0kmYe | sentiment33 | 0.18 | 0.96 | -0.63, 0.69, 0.34, 0.73, 0.95, -0.42, -1.35, -0.24, 1.05, 0.87 |

**判读**：简单 `ts_mean` 结构下三者都是弱信号（S ≤ 0.47），符号逐年翻转 ⇒ 单腿水平值无定价力。
但这**不等于数据集判死** —— 参照 shortinterest3 的先例（简单结构 S≤0.90 判死，
换「双窗口加速度 × target_tvr_decay × 反向」骨架后出货 8+ 颗，判据 MX）。
⇒ **三个数据集都应做机制设计后再判**，尤其：
- **6Xd5zoQP（analyst10 创新分）2021 年 S=3.11** —— 恰好是借券族的共同弱年 ⇒ **可能补借券塔第二席的缺口**
- **9qxNJdOq（sentiment33 负向情绪）2023 年 S=2.32** —— 恰好是费率腿的失效年 ⇒ **同样可能互补**

## 三、fundamental23 / model354：DEU 不存在

MCP `get_datafields` 返回 `count=0, platform_count=0, complete=true` ⇒ **平台在 DEU 无此数据集**
（不是 cov=0 的 meta 造假，是真的不存在）。本地 172 集目录亦无。
⇒ 需用户提供 DEU 存在的替代 id，或放开 region 约束。

## 四、order_book_imbalance：已判死，不重测

波 AE 8 条实测 S -0.48~+0.50、符号混乱 ⇒ 真噪声；
正反成对 lc 160 vs 290 ≈ 1:2 ⇒ 样本集分裂（判据 MQ）非方向问题。

## 五、下一步建议（待用户确认）

1. **analyst10**（analyst 塔，53 字段，十年满覆盖）：用加速度骨架测「分析师创新分/预测惊喜」，
   重点看 2021 年（探针已显示 3.11）⇒ 有望补借券塔第二席的 2021 缺口。
2. **sentiment33**（sentiment 塔，255 字段全 VECTOR，十年满覆盖）：SEFKE 文档级情绪，
   与已判死的 RavenPack 事件级情绪不同源；2023 年探针 S=2.32 ⇒ 有望补费率腿的 2023 缺口。
3. **continuation_score**（pv 塔，560 字段，十年满覆盖）：K 线形态相似度。
   注意判据 MV「形态=价格的确定性变换」+ 波 AD（pattern_scores）已判死 ⇒ **优先级最低**。
4. **重扫因此前 cov=0 被误排除的数据集**（macro27 / earnings6 / option1 / socialmedia12 /
   fundamental1·17·72·89·90·93 等）—— 这是判据 NA 带来的最大机会面。
