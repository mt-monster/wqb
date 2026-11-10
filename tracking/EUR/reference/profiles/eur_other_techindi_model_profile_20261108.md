# EUR × techindi_model 字段画像（2026-11-08）

> 平台目录：**400+ 字段未拉完**（count=400, complete=false，需按语义族抽样画像；本次已拉前 400 条）
> 塔位：OTHER(×1.5，本季 2/3 未点亮，差 1 颗点亮)；字段拥挤度：主流字段 uC 1–99 / aC 1–197（中等偏冷）

## 一、字段族结构（400+ 字段 = 5 分位 × 3 horizon × ~10 模型版本）

| 族 | 示例字段 | cov | 语义 | 备注 |
|---|---|---|---|---|
| Q5 十日 | predicted_fifth_quantile_ten_day_return_15/14/13/141/16/17 | 0.9997 | 模型对第五分位（最强）股票的十日收益预测 | **LL5VwgO1 在用 _15**（prod 0.6926） |
| Q5 五日 | predicted_fifth_quantile_five_day_return_15/151/16/17 | 0.9997 | 同上五日 | TOP700 批在用（pwvYnnOg 族 S3.8） |
| Q5 一日 | predicted_fifth_quantile_one_day_return_13–17 | 0.9997 | 同上一日 | 快信号，TO 风险 |
| Q1 十日 | predicted_first_quantile_ten_day_return_13–17 | 1.0 | 模型对第一分位（最弱）股票的十日收益预测 | **未开采**——Q5−Q1 利差读数待测 |
| Q1 五日/一日 | predicted_first_quantile_*_13–17 | 1.0 | 同上 | 同上 |
| Q4 十日 | predicted_fourth_quantile_ten_day_return_13–18 | 0.9997 | 第四分位预测 | 次强腿备选 |
| bucket 变体 | predicted_fifth_quantile_five_bucket_return_2 | 0.9997 | 分桶指派 | 语义不同（one-hot 型） |

## 二、EUR 历史实证（关键判死边界）

- **已提交锚点 LL5VwgO1**（ACTIVE，[OTHER]，S2.64/F?/prod **0.6926**/self 0.1224，TOPCS1600）：
  `signed_power(group_rank(multiply(rank(ts_mean(F,2)), rank(ts_mean(F,252))), industry), 2.5)`，F=predicted_fifth_quantile_ten_day_return_15。
  **双窗秩乘积读数已被占位**；e76kv2xE 同构实测 self 0.9980 ⇒ 锁死。
- tm_N 模型族 + group_scale 幂次：4 次 prod 实测 0.7454/0.7794/0.7819/0.8163，幂次 0.8–2.1 全扫 S 恒 2.65–2.74 ⇒ 子路径判死。
- **TOP700/STATISTICAL 批**（gbr_w1_snt27，2026-10-29，平台 region=EUR）：ts_zscore 读数 S 3.36–3.84、F 1.49–1.67、2Y 1.9–2.57、sub 1.63–1.91；**本地互相关 vs LL5VwgO1 = 0.503–0.509（self 可过）**；族内互相关 0.9–1.0（只 1 席）；TO 0.54–0.65（贴 HIGH_TURNOVER 0.7 线）。
- ⚠ **TOP700 非 EUR 合法宇宙**（get_platform_setting_options：EUR = TOP2500/TOP1200/TOP800/TOP400/TOPCS1600）⇒ 必须在合法宇宙重测。

## 三、结论与模板方向

1. 主力读数 = **ts_zscore(F, 252) + group_rank**（与 LL5 的双窗乘积相关 0.51，强度 S 3.5+），在 TOPCS1600/STATISTICAL 重开，注意 decay 压 TO（0.54 → 目标 ≤0.4 以留 F 余量）。
2. 新读数探针：**Q5−Q1 十日利差**（模型置信度差，400+ 字段中 Q1 族全未开采）。
3. 判死不适用：400+ 字段远未做尽；本画像为语义族画像，全字段逐条枚举留给 techindi 专项波次。
