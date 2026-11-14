# 算子 scope 验证记录（2026-11-11 00:10）

## 一、用户的批评

「你用的机制是不是不够充分，结论下的太早，所有算子都试了吗，查过平台论坛和外部金融论文了吗」

## 二、已确认的三处缺陷

### 1. 算子覆盖面严重不足

平台 **103 个算子**，我此前只用了不到 15 个。已用：ts_delta / ts_zscore / ts_rank / ts_mean / ts_quantile / ts_std_dev / ts_sum / ts_decay_linear / ts_target_tvr_decay / ts_backfill / ts_corr / group_rank / group_zscore / group_neutralize / rank / zscore / vec_avg / vec_max / hump / multiply / add / subtract / divide / subtract。

**从未触碰的关键类别**：

| 类别 | 数量 | 算子 |
|---|---:|---|
| Reduce | 14 | reduce_avg / ir / count / stddev / skewness / kurtosis / max / min / norm / percentage / powersum / range / choose / sum |
| Vector | 7 | vec_avg / count / max / min / range / stddev / sum |
| Transformational | 4 | bucket / tail / trade_when / generate_stats |
| Cross Sectional | 7 | normalize / quantile / rank / scale / vector_neut / winsorize / zscore |
| Time Series 未用部分 | ~15 | ts_arg_max / ts_arg_min / ts_av_diff / ts_covariance / ts_decay_linear / ts_delay / ts_ir / ts_kurtosis / ts_max_diff / ts_product / ts_regression / ts_returns / ts_scale / ts_step / kth_element / last_diff_value / days_from_last_change |
| Group 未用部分 | 7 | group_backfill / group_cartesian_product / group_count / group_mean / group_scale / group_std_dev / group_sum / combo_a |
| Logical | 11 | and / or / not / equal / not_equal / greater / greater_equal / less / less_equal / if_else / is_nan |
| Special | 3 | in / self_corr / universe_size |

**已存档**：`OPERATORS_FULL_20261111.md`（103 个，按类别 + 精确签名）。

### 2. ★实测发现的硬约束：reduce_* 只有 COMBO scope

查 `get_operators` 的 `scope` 字段：

| 算子 | scope | 能否用于 REGULAR alpha |
|---|---|---|
| vec_avg / vec_stddev / vec_count / vec_max / vec_min / vec_range / vec_sum | `['COMBO','REGULAR']` | ✅ 可用 |
| **reduce_* 全 14 个** | **`['COMBO']`** | ❌ **不可用，会整批 ERROR** |

**这解释了 BE31 八臂全灭**：我用了 reduce_stddev / reduce_ir / reduce_skewness / reduce_kurtosis，全属 COMBO-only。
BE31p 三臂（含 reduce_stddev(裸字段) / ts_backfill(reduce_stddev())）也全灭 —— 共 **11 臂废跑**，本可由一次 scope 检查省掉。

### 3. preflight 的盲区

`preflight_expressions` **只校验字段名存在性，不校验算子 scope、不校验类型匹配**。
BE31 的 preflight 报 `valid=True, unknown_fields=[]`，但八臂全 ERROR。

## 三、vec_stddev 验证结果（sim 1suywj88S50Ab9315XygAHoF）

| alpha | 表达式核心 | S | F | TO | longCount | sub | 2Y |
|---|---|---:|---:|---:|---:|---:|---:|
| MP6PjLVL | `group_rank(vec_stddev(sentiment_model7_score1_fkw3), sector)` | 0.37 | 0.12 | 0.39 | **16** | -0.09 | 0.24 |
| akakrEGw | `group_rank(vec_avg(同字段), sector)` | 0.32 | 0.10 | 0.39 | **17** | -0.16 | -0.01 |

**两个关键结论**：
1. **`vec_stddev` 确实可用且能跑通**（complete=2/2），比 vec_avg 略高 S（0.37 vs 0.32）——分歧度含独立信息；
2. **但 longCount 只有 16-17**（满覆盖件是 149-188）⇒ sentiment33 的 cov 0.32 在裸结构下暴露无遗，**必须配合 `ts_backfill` 恢复覆盖**。

⇒ 下一步正确写法：`ts_backfill(vec_stddev(FIELD), 132)` —— **vec 在内层、backfill 在外层**（与 reduce 不同，vec 输出已是标量，可被 backfill）。

## 四、尚未完成的

**外部金融论文未查成**：`web_search` 因订阅额度用尽（402 billing limit）持续不可用。
情感分歧度相关的经典文献（Loughran-McDonald 金融词典、Tetlock 2007 媒体情绪、tone dispersion 研究）无法检索验证，
目前只有论坛二手结论（「正面情绪分歧度峰值→做空、舆论稳定→做多」，出自帖「【sentiment 模板】帮助点 sentiment 塔」）。
这条缺口需额度恢复后补。