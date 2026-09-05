# ASI 区域 Alpha 进阶方法论（从信号到出仓）

> 来源：论坛文章系统性学习（2026-08-04）：
> - post 37473718017175《ASI MINVOL1M市场Robust Universe优化案例》（SC16582, Main 3.28 / Robust 3.04 / 12-12 checks）
> - post 36383377642391《ASI robust FAIL优化小技巧》（SZ83096）
> - post 41311721014423《MINVOL1M中的行业中性化探讨》
> 关联：[[backtest-experience-archive]]、[[forum-template-library]]

## 1. 信号层：ASI 最强信号族

- **`star_eps_surprise_prediction_fy1`（model30 EPS Estimate Model）**：SmartEstimate vs 共识的 EPS 意外预测，ASI/MINVOL1M 上 3.28/3.04 分。**字段本身仅 12 users/13 alphas（不拥挤，ProdCorr 友好）**；`_d1` 变体 404 users（拥挤，慎用）。
- 教训：之前用 analyst10 的近似字段（`anl10_smartest_net_fy1_pred_surps_v1`）封顶 0.66——**信号强度差异 5 倍，先查对字段再谈模板**。
- ASI 其他有效族：model110（ML 复合，峰值 2.42，2Y/asi_jpn 卡）、fundamental（1.61）。news/sentiment 类全灭（ASI 实测 6 数据集）。

## 2. 预处理层（异常值管理 = Robust 安全垫）

- **winsorize std=5 而非 4**：std=4 过度压缩异常值会削弱 JPN 极端信号（JPN sharpe 1.12→1.34 靠 std=5 释放）。
- **tail 过滤**：字段值范围异常尾部（如 0-10 的高值段）常是过拟合噪音，`tail` 处理后 robust sharpe 明显改善。
- **quantile 变换**：分布变换后 robust 直接 pass（分布形状决定稳健性）。
- **ts_backfill(60)**：覆盖率不足的必补。

## 3. 转换层（顺序即效果）

- `ts_decay_linear(5)` 平滑 → `ts_rank(30)` 时序排名：信号短窗口去噪 + 排名稳健。
- **算子顺序实验**：power 与 group_op 的处理顺序交换 → robust returns 过关（sharpe 未过）；去掉 power（op 6 个→5 个）robust 也能过。

## 4. 分组层（ASI 特有：country 优先）

- **country 分组 > subindustry**：ASI 多国家，行业分组在 MINVOL1M（~1000 只）下组内仅 2-3 只 → 中性化≈抹信号。
- 行业级：INDUSTRY > SUBINDUSTRY（MINVOL1M 实测：INDUSTRY 0.40 vs SUBINDUSTRY 0.17）。
- **细粒度中性化**：`group_neutralize(..., group_cartesian_product(country, densify(bucket(rank(cap), range='0,1,0.1'))))` = country × 市值十分位。
- **group_mean 替代技巧**：`-group_neutralize(x, group)` → `group_mean(x, 1, group) - x`（用掉季度 group_mean 金字塔，同效果）。

## 5. 去噪层（流动性过滤）

- `(group_rank(ts_mean(volume,20), country) > 0.03) * alpha`：剔成交量尾 3% 噪音股，**降低 Main Sharpe 分母 → 直接助攻 Robust Universe**（本文用 multiply，受禁时代之以 rank 门控/ts_rank 内嵌）。
- 核心逻辑：Main 别冲太高，保持 Robust ≈ Main × 0.9 的比率健康。

## 6. 出仓/提交层（Robust 检查达标路径）

| 手段 | 作用 | 优先级 |
|---|---|---|
| winsorize std=4→5 | 释放极端信号（JPN 安全垫） | ★★★ |
| 流动性过滤 | 控制 Main/Robust 比率 | ★★★ |
| tail 过滤异常值 | robust sharpe 改善 | ★★★ |
| quantile 变换 | robust pass 兜底 | ★★ |
| 算子顺序调整 | returns/sharpe 分别过关 | ★★ |
| 减 op 数（去 power） | robust 仍过 + 简洁 | ★★ |

## 7. 实战复刻（2026-08-04 model30 b22 批次）——验证成功

- 设置：ASI / MINVOL1M / delay1 / INDUSTRY / decay6 / trunc0.08 / max_trade ON
- 8 表达式：论坛原版（去 multiply 格子）× country/industry 分组 × 44 窗 × d1 变体 × 冷门字段
- **结果（强验证）**：

| 表达式变体 | sharpe | fitness | 2Y | rn_sh |
|---|---|---|---|---|
| `ts_rank(ts_backfill(winsorize(F,std=5),60),44)` | **1.39** | 0.66 | 1.42 | 1.39 |
| `group_rank(ts_rank(ts_backfill(winsorize(F,std=5),60),44),country)` | **1.46** | 0.65 | 1.21 | 1.45 |
| 论坛原版 30 窗 + country | 1.27 | 0.51 | 1.16 | 1.29 |
| 论坛原版 30 窗 裸 | 1.21 | 0.51 | 1.46 | 1.29 |
| 30 窗 + industry 分组 | 1.22 | 0.52 | 1.52 | 1.28 |
| 反向 44 窗 | -1.39 | - | - | -（方向确认） |
| 冷门字段 mdl30_psprise_pct_fy1_eps + country | 1.01 | 0.36 | 1.21 | 1.00 |

- **关键发现**：
  1. **44 窗 > 论坛原版 30 窗**（1.39-1.46 vs 1.21-1.27）：window 是核心旋钮，论坛参数非最优。
  2. **`_d1` 变体在 delay=1 下被平台去重为原字段**（两个 child 返回同一 alpha id）——`_d1` 404 users 拥挤的真相：它就是主字段的 delay 等价物，勿重复使用。
  3. 无 `ts_decay_linear` 的 44 窗版反而更强——smoothing 在此场景非必需。
  4. 相比 b10/b11 用错字段（analyst10 近似 0.66）：**真字段 + 44 窗 = 2.2 倍提升**。
  5. 全指标（2Y/rn）同步达标，方向为正——进入 robust 测试条件良好。
- 存档：`wqb-share-03/tracking/result_model30_asi_b22.json` / `details_a16_m30.json`

## 8. ASI 全轨道结论（2026-08-05，b22-b34 共 13 批 104 表达式）

### 8.1 单腿极限（model30，SUBINDUSTRY 中性化）
- 52 窗 country：1.48（sharpe 峰值）；cap 十分位组内：1.48/0.71；**SUBINDUSTRY 中性化 × 双窗 blend（60+88）= 2Y 1.64 ✅ / JPN 0.97**（2Y/JPN 达标但 sharpe 1.39 不达标）
- SUBINDUSTRY 在 ASI 的作用**反直觉**：论坛说 MINVOL1M 用 SUBINDUSTRY 抹信号（sh 降 0.09），但它把 JPN 子域从 0.89 提到 0.96——JPN 内部选股受益

### 8.2 跨数据集 blend 突破（model30 × model110）
- `add(ts_rank(W_m30,52), ts_rank(W_m110,60))`（7 ops）= **sh 2.25 / fit 1.40 / ret 4.9% / rn 1.74 / subU 1.24**（7 项中 5 项达标）
- 腿字段选择：`mdl110_score`（sharpe 最强 2.25）vs `mdl110_value`（JPN 最优 0.75）；growth/sentiment/momentum/alternative 腿 JPN 灾难性（≤0.05）
- 遗留瓶颈：**LOW_ASI_JPN_SHARPE 0.70-0.75 vs 1.0、IS_LADDER 1.47 vs 1.6**——model110 腿固有稀释，论坛公认 ASI 结构性难题

### 8.3 三腿 blend 实测（b34）——不可行
- 全预处理三腿 = 11 ops 超限（<8 硬约束）
- 压缩预处理（裸 ts_rank + 外层 zscore/rank/winsorize 补偿，6 ops）：**JPN 从 0.70 崩到 0.37**——外层补偿无法替代字段级 winsorize+ts_backfill（再次验证第 2 节结论）
- 三族各一腿（m30+score+value）：JPN 0.72 但 fitness 崩 0.76
- **结论：<8 ops 下三腿不可行；两腿全预处理是唯一有效结构**。若平台放宽 ops/multiply 约束，三腿 2:1 加权骨架（`add(add(ts_rank(W_m30,52), ts_rank(W_m30,88)), ts_rank(W_m110,60))`）可直接复用

### 8.4 其他失效变体（避坑清单）
- 双层 rank（ts_rank(ts_rank(x,52),10)）：sharpe 崩至 0.26
- 外层 ts_decay_linear：1.21（降）
- std=3 winsorize：1.35（降）；std=6：无改善
- backfill 120：无益；trunc 0.04/0.15：无差异；decay 12/20：sharpe 降 0.12
- group_neutralize(country×cap cartesian)：1.40（无提升）
- group_mean(x,1,country)-x：-1.45（反向信号，反转后与基线持平）
- fy2/12m 字段：0.8-0.97 无效
