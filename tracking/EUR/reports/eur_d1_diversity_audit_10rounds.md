# EUR D1 战役第 10 轮表达式多样性评估（2026-08-18）

> 触发：用户执行要求第 7 点"每进行 10 轮回测后，执行一次 alpha 表达式多样性评估并优化 skills"。
> 统计范围：wave1/2/3/3b/3c/3d/5/6/6b/6c/7（10 轮已判死/存档 wave）+ wave8 在飞，共 12 波 ~192 探针。

## 1. 操作符探索率（低）

| 算子 | 次数 | 占比 | 备注 |
|---|---|---|---|
| rank | 231 | ~65% | 每表达式必用，横截面归一化 |
| subtract | 95 | ~27% | 94% 为 `subtract(0, x)` 镜像 |
| vec_avg / vec_sum | 60 | ~17% | 仅 VECTOR 数据集（w1/w6）聚合 |
| add | 27 | ~8% | 仅 FCF 家族线性混合 |
| multiply | 14 | ~4% | 权重乘法（0.5/0.3 等） |
| ts_delta / ts_mean / ts_av_diff / ts_decay_linear | 20 | ~6% | 多为 VECTOR 时序聚合 |

**未探索算子（0 次）**：`ts_zscore`、`ts_std_dev`、`ts_rank`、`ts_corr`、`ts_regression`、`ts_skewness`、`group_rank`、`group_neutralize`、`signed_power`、`scale`、`winsorize`、`log`、`abs`、`if_else`、`quantile`（禁 2 参）、`ts_backfill`（仅回填带需用）。

## 2. 字段探索率（主题集中）

跨 wave 去重后实际触及字段主题：

| 主题 | 字段数 | 数据集 | 状态 |
|---|---|---|---|
| 新闻/情感 | 15+ | news_sentiment_dl / news_sentiment_nlp / ai_news_scores | 3 数据集全灭（top sh ≤0.58） |
| 分析师/基本面 | 15 | multi_horizon_alpha（FCF 家族）/ model193 | FCF 撞 rnf+prod_corr 双墙；model193 在飞 |
| CDS/信用风险 | 5 | model193 | 在飞（wave8） |
| 价格/形态 | 2 | chart_cnn_alpha / price_signal_dl / pattern_scores | 全灭 |
| 其他 | 4 | — | — |

**零竞争覆盖率**：白名单 10 个 tier1 数据集已消耗 7 个（news_sentiment_dl、chart_cnn_alpha、multi_horizon_alpha、price_signal_dl、pattern_scores、news_sentiment_nlp、ai_news_scores），剩余 model193（在飞）、model354、ml_factor_proj 等。

## 3. 模板骨架多样性（极低）

| 骨架 | 数量 | 占比 |
|---|---|---|
| rank_single（`rank(x)`） | 112 | 58% |
| mirror_single（`subtract(0, rank(x))`） | 53 | 28% |
| linear_mix（`add(w1*rank(a), w2*rank(b))`） | 27 | 14% |

**缺失骨架**：ts 长窗时序包裹（`ts_mean(x,66)` 作分母/比较）、双时序差（`ts_delta(ts_mean,22)`）、事件触发（`if_else`）、行业组内 rank、三因子混合（0.5/0.3/0.2）、`ts_decay_linear` 加权（仅 2 次且无效）。

## 4. 风格多样性（已覆盖 5 类，4 类判死）

1. 新闻情感（VECTOR NLP ×2 + AI 评分 ×1）→ RED（EUR 新闻情感结构性无效）
2. CNN 图像特征 → RED（rn 近期失效）
3. 基本面价值/反转（FCF 镜像家族）→ AMBER 终结（rnf 0.32-0.62 结构墙 + prod_corr 0.758 墙）
4. 技术形态相似度 → RED（单字段 IS 弱）
5. CDS 信用风险/分析师修订（model193）→ wave8 在飞，风格与前 4 类完全正交

## 5. 预处理方式（单一）

- 100% 用 `rank` 横截面归一化，无时序标准化（ts_zscore）、无行业组内处理（SUBINDUSTRY 全局中性化是 settings 层）
- decay 固定 4 / truncation 0.08 / maxTrade ON，无参数面探索（wave3d 权重扫描除外）
- VECTOR 统一 vec_avg（无 vec_max/vec_first 探索——wave1 曾用 vec_max 弱信号）

## 6. 收益来源归因

- **EUR 全期限反转统治**（wave3 实证）：基本面 long 因子全线负（fcf sh=-1.9、value -1.34、est_rev -1.41），镜像 FCF 为唯一正贡献家族（sh 1.84-2.02）但撞 prod_corr 墙（0.90→0.76，稀释边际递减）
- **新闻情感无 alpha**：4 个数据集 top sh ≤0.58、margin ≤2.6bp，与 GBR sentiment27（0.59）、EUR news_sentiment_dl（0.37）跨区一致 → 结构性排除
- **rnf 墙**：FCF 家族 rn_fitness 封顶 0.62，用户新闸 0.7 需近期仍强负的镜像源或正分量
- 价格类单字段 IS 弱（≤0.72），需加工型复合信号

## 7. 失效风险总结与扫盲

| 风险 | 证据 | 对策 |
|---|---|---|
| 反转家族 prod_corr 饱和 | FCF 0.90→0.76，直方图 0.7-0.8 仅剩 1 个 | 异质分量（CDS/分析师/做空）稀释，model193 是主候选 |
| rnf 结构墙 | FCF 全家族 ≤0.62 | 换数据集；model193 的近期信号（CDS 变化/评级修订）天然短窗，rn 可能强 |
| 新闻类 margin 墙 | 全部 ≤2.6bp <5bp | 永久排除 EUR 新闻情感类 |
| 零竞争≠有 alpha | price_signal_dl/pattern_scores 零竞争仍灭 | 需加工型复合，非单字段 |
| 共享配置冲突 | settings.json 被外部会话改 universe（wave6b 事故） | runner 局部覆盖 universe，不动共享 settings |

## 8. 对后续 wave 的优化（wave9+）

1. **算子扩展**：优先 `ts_zscore(x, 66)` 时序标准化、`group_rank`（SUBINDUSTRY 组内）、`ts_corr`（价格 vs 信用）、`ts_decay_linear`（信号平滑）
2. **骨架扩展**：L/S 三因子混合（0.5/0.3/0.2）、`ts_delta(ts_mean(x,66), 22)` 长窗动量、双方向配对（原始+镜像同场对照）
3. **方向策略**：EUR 近期转正因子（momentum/est_rev 原始方向）与反转镜像（FCF）配对，规避 prod_corr 墙
4. **字段**：model193 的 CDS 变化量 + 分析师修订为全新维度；若 wave8 灭，转 model354（同风格家族但字段不同）/ ml_factor_proj（机器学习投影）
5. **预处理**：对月度更新字段（分析师/信用）尝试 decay 0-2 变体（信息衰减慢，可能抬 tvr 与 rn）
6. **skills 优化**：brain-deepExplore 的 S1 阶段增加"算子-骨架矩阵"预检（每 wave 强制 ≥2 种新骨架），S2 makeSomeGem 输入增加本报告 §1-3 的缺口清单
