# GBR analyst7 —— 目标价/一致预期修订模板库（12 结构互异）

> 建立于 2026-11-04（W57 出货后）。每条的「结构差异」标注差异轴：信息矩 / 算子几何 / 分组轴 / 非线性变换。
> 算子计数口径：`len(re.findall(r'[a-z_0-9]+\s*\(', expr))`，每实例计 1，重复各计 1；合规范 [10,15]。

## 0. 数据集事实（实测，勿重推）

- `analyst7`（dataset_id 185）GBR 502 字段，coverage 均值 0.7526，平台 alpha 数 5823（**饱和**）。
- 16 个会计科目，每个都有 `_4wks_ago` / `_3mth_ago` 显式滞后快照：
  `bps cps csh dps ebi ebt ent gps grm nav net opr pre roa sal tbv`
- 覆盖率最好的科目：`dps 0.689 / sal 0.688 / pre 0.688 / ebt 0.676 / net 0.666 / ebi 0.666 / bps 0.633`。
- **`_4wks_ago` / `_3mth_ago` 是本集最有价值的几何入口**：可直接做干净修订率，无需 `ts_delta`（也就没有「季度字段时序无输入」的问题）。
- 广度字段 `est_12m_{item}_raisednum_4wks` / `_lowerednum_4wks` / `_raised_1wk` / `_lowered_1wk` / `_raisednum_1mth` / `_lowerednum_1mth` coverage = 1.0。

## 1. 骨架（ops 已计入）

```
LT(core, T)  = group_rank(ts_target_tvr_decay(winsorize(rank(core), std=0.2),
                          lambda_min=0, lambda_max=1, target_tvr=T), sector)          # 4 + core
bf(x)        = ts_backfill(x, 500)                                                        # 1
rev(f, lag)  = divide(subtract(bf(f), bf(lag)), add(abs(bf(lag)), 1))                     # 7
```

## 2. 十二个结构互异模板

| # | 名称 | 结构内核 | 差异轴 | ops | 实证 |
|---|---|---|---|---:|---|
| T1 | 归一化修订率 | `rev(f, f_lag)` | 一阶差分 + 相对幅度归一 | 11 | ★ **S 1.98 / F 1.45**（`2rAw9o7J`, pre_mean 3mth） |
| T2 | 绝对差分 | `subtract(bf(f), bf(lag))` | 同阶但**不做幅度归一**（保留规模信息） | 需补 | 未测 |
| T3 | 截面排名差分 | `ts_backfill(subtract(rank(bf(f)), rank(bf(lag))), 250)` | 在**排名空间**做差，非线性变换轴 | 10 | ✔ 全闸（`A6_T3_pre_high`, W58） |
| T4 | 广度净差 | `ts_backfill(subtract(rank(bf(raised)), rank(bf(lowered))), 250)` | 事件广度矩（非价格水平） | 10 | ★ S 1.86 / 1.84（`LLMNEYpM` 4wks, `gJebXV1l` 1wk） |
| T5 | 广度一致性比 | `divide(bf(raised), add(add(bf(raised), bf(lowered)), 1))` | 有界比值（上市/下调占比），非线性轴 | 10 | ✔ W58 |
| T6 | 分歧度变化 | `(high−low)/|mean|` 的本期 − 滞后 | 二阶矩（方差）轴 | 11 | ✗ **反向**（W57 G5 S = −0.67） |
| T7 | 修订加速度 | `[(f−f_4w) − (f_4w−f_3m)] / |f_3m|` | 二阶差分 | 12 | 未测 |
| T8 | 覆盖度加权修订 | `rev × rank(num)` | 加权轴（分析师人数=置信度） | 需补 | 未测 |
| T9 | 修订动量平滑 | `ts_mean(rev, 22)` | 时序平滑轴 | 12 | ✔ W58 |
| T10 | 子行业内 z 修订 | 把 `group_rank(·, sector)` 换成 `group_zscore(·, subindustry)` | 分组轴 + 归一化轴 | 10 | 未测 |
| T11 | 纯历史修订 | `rev(f_4wks_ago, f_3mth_ago)` | **完全去掉当期**，只用两档滞后 | 11 | 未测（正交性最高的设计） |
| T12 | 上下尾不对称 | `rev(high, high_lag) − rev(low, low_lag)` | 不对称分解轴 | 15 | 未测 |

## 3. 已被证伪（勿重试）

| 攻法 | 结果 | 出处 |
|---|---|---|
| 加 `group_neutralize` + `ts_mean` 平滑裸信号 | S 1.90 → 0.58–1.28，全跌破 1.58 闸 | W55 |
| 分析师分歧度做多高分歧 | S = −0.41，方向反 | W55 A5 |
| 跨会计科目广度加总（pre+net+bps） | S 0.94 < 单科目 1.28 | W55 A6 |
| 广度 × 盈利惊喜相乘 | S 0.25 | W55 A7 |
| 覆盖度动量 `Δnum/σ` | S 0.11 | W55 A8 |
| 用 `ts_delta` 做修订 | 季度字段时序无输入，噪声 | 结构性 |

## 4. 关键方向性先验

- **目标价（pre）修订 > 净利（net）修订**：W57 G1/G2/G6（pre 系）S 1.74–1.98，G4（net_mean）只有 1.37。
- **分歧度要取反**：目标价上下限区间扩张 = 坏信号（W57 G5 −0.67，W55 A5 −0.41 同向印证）。
- **`last_diff_value` 优于 `ts_backfill` 做修订载体**：已提交的 `gJZQZkZe`（prod 0.6793）用的就是 `last_diff_value(·, 100)`。
- **FAST 中性化 + decay 0 + trunc 0.10** 是 W57 出货的档位；`STATISTICAL` 在 W55 表现更弱。

## 5. prod 侧事实

- 已提交 analyst7 两件：`gJZQZkZe` prod **0.6793**、`npP83YQq` prod **0.6938** ⇒ 族代表落在 0.68–0.69，**< 0.70 = 族干净**，可继续量产。
- 新件对已提交池本地互相关：`2rAw9o7J` max 0.533 / `YP1b8oNo` 0.267 / `gJebXV1l` 0.420 ⇒ self 闸余量充足。
- **量产阶段不测 prod**；只在上交前对单颗跑 `check_correlation(refresh=True)` 终验。