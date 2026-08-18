# Alpha 挖掘实验日志 — USA/D1/REGULAR 三风格三数据集

日期: 2026-07-29 ｜ 账号: mthyzx@126.com ｜ 执行: Claude Code + wqb-mcp + 5 Agent Skills

## 目标（用户 /goal 原文要点）

- region=USA, delay=1, REGULAR, max_trade=ON, 探索不同 universe（默认 TOP3000）
- 每个 alpha: **sharpe>1.58, fitness>1, 2Y-sharpe>1.6, margin>5bp, 5%<turnover<30%**
- risk-neutralization 视图: **sharpe>1, fitness>0.7, margin>5bp**
- **操作符数量<8, Failed RA==0**（WebDataScope 口径), ProdCorr≤0.7
- 3 个不同数据集、完全不同策略风格、单数据集纯度（1-2 字段）、互相关<0.4
- 禁用 trade_when / add / multiply；只用 create_multi_simulation（8 并发）
- 不提交（用户手动提交）；每个入围先 robust + 过拟合审计再 set_alpha_properties
- 每 10 批做多样性评估

## Phase 0 准备（零模拟成本）

- **认证**: OK（201, read+write）
- **算子白名单**: get_operators 返回 127 个；确认幽灵算子（ts_entropy/ts_skewness/group_normalize/tanh/sigmoid/s_log_1p 等）均不存在于平台；本实验额外禁用 trade_when/add/multiply（用户指令）
- **金字塔状态 (USA/D1)**: 未点亮类别 = sentiment(×1.5), analyst(×1.3), news(×1.2), macro/insiders/socialmedia(×1.1), institutions/imbalance(×1.0)；已点亮 model(3)
- **数据集入围**（recommend_datasets 平台评分 × WebDataScope 数据包甜点区交叉验证）:

| 轨道 | 风格 | 主数据集 | 平台推荐分 | 社区 sharpe (count) | 首选中性化（数据包统计） | 金字塔 |
|---|---|---|---|---|---|---|
| A | 分析师预期修正/盈利动量 | analyst39 | 78.0 | 0.409 (2682) | SUBINDUSTRY(0.494,n=774), FAST(0.497), SECTOR | analyst ×1.3 未点亮 |
| B | 内部人/申报行为 (聪明钱) | insiders3 | 89.7 (#3) | 0.440 (1976) | STATISTICAL(0.55,n=968), SLOW(0.755,n=51) | insiders ×1.1 未点亮 |
| C | 新闻情绪 | sentiment21 | 90.6 (#1) | 0.568 (915) | STATISTICAL(0.645,n=386), SUBINDUSTRY(0.716,n=94) | sentiment ×1.5 未点亮 |
| 备 | — | analyst34 / sentiment22 / institutions10 / news54 | — | 0.438 / 0.532 / 0.559 / 0.550 | INDUSTRY / STATISTICAL / NONE·SECTOR / STATISTICAL | — |

- **字段先验**（get_datafields alphaCount 排序 + 数据包体检）:
  - analyst39 (36 字段, 全 MATRIX, 月频): EPS 系 anl39_aepsinclxo(305α)/qepsinclxo(204)/xlcxspemtt(187)、EPS 变化率 epschngin(178)/ghcspea(176)/ghcspemtt(69)、质量比率 qtotd2eq(151)/atanbvps(207)/agrosmgn2(127)。覆盖率≈1.0。窗口 ≥21d。
  - insiders3 (61 字段, MATRIX+VECTOR): 申报节奏 insd3_10q_freq_latest_release(9796α)/upload_file_count(8271)/10k_freq_flag(5089)；内部人交易 form4_bnum(9666α, **coverage 0.41 → 必须 ts_backfill**)/form4_bvol(1203)；8-K 文本 tone (VECTOR → vec_avg 包装)。
  - sentiment21 (258 字段, MATRIX, 日频): 方向 snt21_pos_mean(82α)/neg_mean(61)；离散度 2neg_std(40)/pos_std；极值 pos_max(28)/neg_max。覆盖率≈1.0。
- **预算**: 计划 ≤300 次模拟；每批 8 条；A→B→C 轮转。

---

## 批次记录

### Batch 01 ｜ 轨道 A ｜ analyst39 ｜ TOP3000/SUBINDUSTRY/decay6 ｜ multisim 4pEvHu1124hdbiW18hzWzbRU

假说：EPS 修正动量——盈利变化率领先股价（月频字段，窗口 21-126d）

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | riskNeut | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rank(ts_delta(anl39_xlcxspemtt,63)) | 0.30 | 0.09 | 4.2% | 5.2bp | 0.24 | -0.31 | 3 | 杀 |
| 2 | group_rank(ts_delta(anl39_qepsinclxo,63),subindustry) | **0.43** | 0.12 | 5.0% | 3.6bp | 0.64 | 0.04 | 3 | 杀 |
| 3 | zscore(ts_zscore(anl39_ghcspea,126)) | -0.19 | -0.05 | 7.8% | -1.9bp | 0.21 | -0.32 | 4 | 杀 |
| 4 | rank(divide(anl39_xlcxspemtt,anl39_spvbq)) | 0.35 | 0.16 | 1.9% | **29bp** | 0.66 | 0.48 | 3 | 杀(线索†) |
| 5 | subtract(rank(anl39_ghcspea),rank(anl39_qtotd2eq)) | -0.33 | -0.10 | 2.1% | -12bp | -0.62 | -0.07 | 4 | 杀(反号线索) |
| 6 | ts_decay_linear(rank(ts_delta(anl39_aepsinclxo,126)),21) | -0.19 | -0.04 | 3.2% | -4.1bp | 0.36 | -0.58 | 4 | 杀 |
| 7 | group_zscore(ts_av_diff(anl39_ghcspemtt,63),industry) | 0.15 | 0.03 | 6.0% | 1.9bp | 0.28 | 0.18 | 3 | 杀 |
| 8 | signed_power(rank(ts_delta(anl39_epschngin,21)),2) | -0.27 | -0.06 | 13.2% | -1.1bp | 0.01 | 0.10 | 4 | 杀 |

多样性检查：外层 5 种(rank/group_rank/zscore/group_zscore/signed_power) ✅ 窗口 21/63/126 ✅ 形态 4 种 ✅
决策：EPS 动量骨架整体偏弱。†线索：#4 价值比（EPS/BVPS）margin 29bp + riskNeut 0.48 + PnL 实现周期 120d → A2 转向"盈利收益率/质量"慢信号骨架 + 反号 EPS 系；turnover 偏低需注意 >5% 下限。
预算：8/300 ｜ 入围 0/3

### Batch 02 ｜ 轨道 B ｜ insiders3 ｜ TOP3000/STATISTICAL/decay6 ｜ multisim 1Rk4LReMl4Vsc0J4DclMShu

假说：内部人买入强度与申报节奏异常预示超额收益（form4 低覆盖字段一律 ts_backfill）

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|
| 1 | rank(ts_backfill(insd3_form4_bnum,63)) | 0.19 | 0.04 | 7.0% | 1.3bp | 0.18 | 3 | 杀 |
| 2 | rank(ts_delta(ts_backfill(insd3_form4_bnum,63),21)) | **0.91** | **0.39** | 17.0% | 3.7bp | **1.33** | 3 | **强线索→B2 主攻** |
| 3 | group_rank(ts_backfill(insd3_form4_bvol,63),subindustry) | 0.27 | 0.06 | 8.1% | 1.5bp | -0.74 | 4 | 杀 |
| 4 | rank(ts_zscore(insd3_upload_file_count,63)) | 0.07 | 0.01 | 29.4% | 0.3bp | 0.84 | 3 | 杀 |
| 5 | rank(ts_av_diff(insd3_10q_freq_latest_release,126)) | -0.86 | -0.31 | 5.8% | -5.7bp | -1.25 | 3 | 杀(反号弱) |
| 6 | rank(vec_avg(insd3_8k_tone_score)) | -0.17 | -0.02 | **109%** | 0bp | -0.36 | 5 | 杀(换手爆) |
| 7 | rank(ts_delta(vec_avg(insd3_8k_tone_score),21)) | 0.00 | 0.00 | **113%** | 0bp | -0.2 | 5 | 杀(换手爆+集中) |
| 8 | reverse(rank(vec_sum(insd3_8k_negative_freq))) | 0.19 | 0.02 | **111%** | 0bp | -0.58 | 6 | 杀(换手爆) |

多样性检查：外层 4 种 ✅ 窗口 21/63/126 ✅ 形态：矩阵动量/水平/vec 聚合 ✅
决策：**form4_bnum 买入数量动量是本轨最强方向**（#2: 0.91/1.33，margin 3.7bp 偏薄）。8-K vec 文本族日频跳变换手 >100% 全灭，弃。B2 集中打磨 #2：更平滑（ts_decay_linear/ts_sum 窗口）、更长 delta、decay 上调、SLOW 中性化对照、bvol/bnum 比值。
预算：16/300 ｜ 入围 0/3

### Batch 03 ｜ 轨道 C ｜ sentiment21 ｜ TOP3000/STATISTICAL/decay4 ｜ multisim 1OfmnFeRT55eaA9OhQ8I9g6

假说：净情绪（pos_mean−neg_mean）的水平/变化/离散度正向驱动收益（Level/Change/Surprise/Dispersion 桶）

| # | 表达式 | sharpe | fit | tvr | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | rank(subtract(pos_mean,neg_mean)) | -0.19 | -0.02 | 86% | -0.30 | 5 | 杀 |
| 2 | rank(ts_delta(net,5)) | **-0.73** | -0.11 | 108% | -1.08 | 5 | 杀(反号线索!) |
| 3 | ts_zscore(net,21) | **-0.75** | -0.11 | 99% | -0.54 | 5 | 杀(反号线索!) |
| 4 | reverse(rank(2neg_std)) | -0.05 | 0.00 | 82% | 0.06 | 5 | 杀 |
| 5 | rank(ts_decay_linear(rank差,10)) | -0.52 | -0.07 | 74% | -0.96 | 5 | 杀 |
| 6 | group_rank(ts_mean(net,21),subindustry) | -0.34 | -0.07 | **13.7%** | 0.26 | 4 | 杀(换手可控✓) |
| 7 | reverse(rank(ts_delta(neg_max,5))) | -0.12 | -0.01 | 104% | -0.45 | 5 | 杀 |
| 8 | rank(ts_ir(net,63)) | -0.41 | -0.10 | 6.5% | 0.01 | 4 | 杀 |

多样性检查：外层 5 种 ✅ 窗口 5/10/21/63 ✅
决策：**整个方向族系统性为负 = 情绪反向定价**（印证 repair skill news 修复方向 v："raw direction on news is frequently already priced in"）。两条结构性教训：①C2 全面反号（#2/#3 反号即 +0.73/+0.75 起步）；②日频原始信号换手爆表，必须 ts_mean/ts_decay_linear ≥21d 平滑（#6 证明 21d 平滑 + group_rank 可把换手压到 14%）。
预算：24/300 ｜ 入围 0/3

### Batch 04 ｜ 轨道 A ｜ analyst39 ｜ TOP3000/SUBINDUSTRY/decay2 ｜ multisim ZNYWCbPp5289dOa4KIlAKe

假说：盈利收益率（EPS/BVPS）价值骨架 + 质量调整 + 反号成长

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | riskNeut | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rank(divide(xlcxspemtt,spvbq)) | 0.35 | 0.16 | 2.0% | 28bp | 0.66 | 0.48 | 3 | 杀 |
| 2 | 价值−杠杆 rank 差 | 0.04 | 0.01 | 2.2% | 2.7bp | 0.36 | 0.46 | 3 | 杀 |
| 3 | reverse(成长−杠杆) | 0.32 | 0.10 | 2.2% | 11bp | 0.62 | 0.07 | 3 | 杀 |
| 4 | group_rank(价值,subindustry) | 0.35 | 0.15 | 2.0% | 22bp | 0.65 | 0.62 | 3 | 杀 |
| 5 | rank(divide(qepsinclxo,spvbq)) | **0.59** | **0.35** | 2.8% | **31bp** | 0.86 | **0.80** | 3 | 最强→A3 主攻 |
| 6 | zscore(winsorize(价值)) | 0.19 | 0.07 | 3.8% | 9.4bp | 0.21 | 0.20 | 3 | 杀 |
| 7 | 价值−动量 rank 差 | 0.26 | 0.08 | 4.4% | 5.7bp | 0.76 | 0.74 | 4 | 杀 |
| 8 | rank(divide(ttmgrosmgn,qtotd2eq)) | -0.29 | -0.09 | 1.7% | -14bp | 0.26 | 0.18 | 4 | 杀 |

多样性检查：外层 6 种 ✅ 形态：ratio/asym-diff/group ✅
决策：**季度盈利收益率是 A 轨最强方向**（#5, riskNeut 0.80 接近达标线 1.0）。两个问题：sharpe 差 1 个量级、价值信号换手 2-3% < 用户 5% 下限。A3 = qepsinclxo 收益率族 × FAST 中性化（analyst39 数据包最优, 0.497）+ ts_rank/ts_zscore 提换手变换。已用 2 批, A3 为本数据集最后一批（否则换 analyst34）。
预算：32/300 ｜ 入围 0/3

### Batch 05 ｜ 轨道 B ｜ insiders3 ｜ TOP3000/STATISTICAL/decay6 ｜ multisim PfW5h9GY5bM9ahtuKf5T8u

假说：form4_bnum 买入动量变体扫描（窗口/平滑/归一化/净值）

| # | 表达式（核心变化） | sharpe | fit | tvr | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | delta 42d | 0.56 | 0.21 | 12.8% | 0.15 | 3 | 杀 |
| 2 | delta 10d | 0.29 | 0.06 | 24.6% | 0.35 | 3 | 杀 |
| 3 | delta 21d + ts_decay_linear 10 | **0.86** | **0.37** | 10.0% | **1.35** | 3 | 次优 |
| 4 | ts_sum 21（水平强度） | 0.05 | 0.00 | 9.3% | -0.11 | 3 | 杀 |
| 5 | delta 21d + group_rank subindustry | 0.65 | 0.22 | 17.6% | 0.47 | 3 | 杀 |
| 6 | ts_zscore 63（异常度） | 0.57 | 0.21 | 12.0% | 0.11 | 3 | 杀 |
| 7 | bnum/upload_count 归一化 delta | -0.27 | -0.16 | 14.3% | -0.32 | 5 | 杀(集中爆) |
| 8 | 净买入 bnum−snum 水平 | 0.26 | 0.06 | 10.1% | 0.72 | 3 | 杀 |

决策：变体扫描确认 **delta 21d 是最优形态**（B1#2 0.91 / B2#3 平滑版 0.86），STATISTICAL 下平台期 ~0.9。B3 = 同形态 × **SLOW 中性化**（数据包 insiders3 最优 0.755）+ quantile/signed_power 变换 + bvol 对照 + 更长 backfill。
预算：40/300 ｜ 入围 0/3

### Batch 06 ｜ 轨道 C ｜ sentiment21 ｜ TOP3000/STATISTICAL/decay6 ｜ multisim 20Vp053iY4r2cdTBBP4Burx

假说：C1 教训应用——情绪反向定价（全反号）+ ≥21d 平滑控换手；附带测试离散度桶

| # | 表达式（核心） | sharpe | fit | tvr | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | reverse(rank(ts_mean(net,21))) | 0.55 | 0.16 | 11.2% | -0.21 | 3 | 杀 |
| 2 | reverse(平滑 zscore) | 0.52 | 0.07 | 84% | -0.57 | 4 | 杀(换手) |
| 3 | reverse(group_rank(ts_mean(net,63))) | 0.16 | 0.02 | 6.6% | -0.47 | 4 | 杀 |
| 4 | reverse(rank(ts_mean(pos,21))) | 0.29 | 0.06 | 11.2% | -0.74 | 3 | 杀 |
| 5 | rank(ts_mean(neg,21)) | 0.20 | 0.03 | 11.2% | 1.08 | 3 | 杀 |
| 6 | reverse(rank(ts_ir(net,21))) | 0.81 | 0.29 | 13.0% | -0.15 | 3 | 次优 |
| 7 | **rank(ts_std_dev(net,21))** | **1.03** | **0.38** | **14.0%** | **1.15** | 3 | **突破→C3 主攻** |
| 8 | reverse(rank(平滑 rank 差,21)) | 0.52 | 0.07 | 72% | 1.00 | 4 | 杀(换手) |

决策：**情绪离散度（净情绪 21d 波动率）做多是 C 轨真信号**——"情绪不确定性溢价"风格，恰好落在 skill 的 HIGH-priority Dispersion 桶；子域 0.80 结构健康。反号方向族只到 0.5-0.8，放弃。C3 = 离散度族精修：窗口扫描 10/42/63、pos_std/neg_std 原生字段、SUBINDUSTRY 对照（数据包 0.716）、ts_ir 反号×离散度复合。
预算：48/300 ｜ 入围 0/3

### Batch 07 ｜ 轨道 A ｜ analyst39 ｜ TOP3000/**FAST**/decay2 ｜ multisim 3EPPEzeMh5409TFzgNPrm37

假说：盈利收益率族在 FAST 中性化下强度翻倍（验证数据包中性化先验 FAST 0.497 > SUBINDUSTRY 0.494）

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|
| 1 | rank(divide(qepsinclxo,spvbq)) | 1.01 | 0.67 | 7.5% | 15bp | 1.14 | 3 | 强 |
| 2 | ts_rank(价值,63) | 0.24 | 0.05 | 10.4% | 0.8bp | 0.74 | 3 | 杀 |
| 3 | group_rank(价值,sector) | 1.00 | 0.64 | 7.3% | 14bp | 1.11 | 3 | 强 |
| 4 | rank(ts_zscore(价值,126)) | 0.74 | 0.26 | 7.1% | 4.5bp | 0.95 | 3 | 备用(动量互补) |
| 5 | signed_power(rank−0.5, 2) | 1.03 | 0.71 | 8.0% | 15bp | 1.14 | 3 | 强 |
| 6 | 价值−成长 rank 差 | 0.92 | 0.46 | 6.4% | 9.6bp | **1.24** | 3 | 强(2Y 最高,子域 0.90) |
| 7 | **quantile(价值)** | **1.04** | **0.71** | 7.8% | 15bp | 1.11 | 3 | **A4 主攻** |
| 8 | rank(divide(aepsinclxo,spvba)) 年度版 | 0.79 | 0.46 | 7.0% | 12bp | 1.07 | 3 | 杀 |

决策：**FAST 中性化使 A 轨从 0.59 → 1.04（数据包先验直接兑现）**；换手 6-8% 已达标（>5%）。SUBINDUSTRY→FAST 是本实验第一个"课件级"教训。A4 = 复合骨架（quantile 价值 + 126d 价值动量 + 反号成长, subtract/reverse 组合）+ 尾部凸性。
预算：56/300 ｜ 入围 0/3

### Batch 08 ｜ 轨道 B ｜ insiders3 ｜ TOP3000/**SLOW**/decay6 ｜ multisim jv23JgSs4sOaWXlYTBKfUJ

假说：form4_bnum 21d 动量在 SLOW 中性化下更强（数据包 SLOW 0.755, 但 n=51 小样本）

| # | 表达式（核心） | sharpe | fit | tvr | 2Y | 判定 |
|---|---|---|---|---|---|---|
| 1 | 基准 delta21 @SLOW | 0.62 | 0.22 | 17.1% | 0.22 | 杀 |
| 2 | +ts_decay_linear10 | 0.53 | 0.18 | 10.1% | 0.46 | 杀 |
| 3 | quantile 变换 | 0.60 | 0.21 | 17.2% | 0.28 | 杀 |
| 4 | signed_power 凸性 | 0.62 | 0.22 | 17.2% | 0.22 | 杀 |
| 5 | group_rank industry | 0.50 | 0.16 | 11.0% | 0.58 | 杀 |
| 6 | ts_ir 63 | 0.11 | 0.02 | 8.2% | 0.03 | 杀 |
| 7 | bvol delta21 | 0.63 | 0.22 | 16.1% | 0.41 | 杀 |
| 8 | backfill 126 长窗 | 0.46 | 0.13 | 7.3% | 0.82 | 杀 |

决策：**SLOW 全面弱于 STATISTICAL（0.62 vs 0.91）——小样本先验（n=51）被证伪，大样本先验（STATISTICAL n=968）可靠**。这是"课件级"教训 #2：中性化先验要看样本量。B 轨 3 批未达 80% 目标 → 按升级规则换备用数据集 **institutions10**（13F 持仓流，风格仍属聪明钱）。form4_bnum delta21 @STATISTICAL (0.91/2Y1.33) 入近失池待修复。
预算：64/300 ｜ 入围 0/3

### Batch 09 ｜ 轨道 C ｜ sentiment21 ｜ TOP3000/STATISTICAL/decay6 ｜ multisim 1MsyDC7rS5cNaT0gqxzP1fs

假说：情绪离散度精修——窗口扫描 + 原生字段 + 复合

| # | 表达式（核心） | sharpe | fit | tvr | 2Y | 判定 |
|---|---|---|---|---|---|---|
| 1 | std 10d | 1.01 | 0.28 | 25.4% | 0.61 | 换手高/2Y 弱 |
| 2 | std 42d | 0.36 | 0.08 | 8.3% | 0.52 | 杀 |
| 3 | std 63d | 0.36 | 0.08 | 6.0% | 0.14 | 杀 |
| 4 | 原生 2neg_std 平滑 | -0.66 | -0.22 | 11.5% | -0.5 | 杀(与合成 std 相反!) |
| 5 | group_rank(std21, subindustry) | 0.68 | 0.19 | 15.4% | 1.05 | 杀 |
| 6 | std21 − 净情绪水平 复合 | 0.98 | 0.38 | 13.8% | 0.49 | 2Y 弱 |
| 7 | std(rank(net),21) 截面 rank 版 | 0.87 | 0.29 | 14.2% | 0.66 | 杀 |
| 8 | signed_power(std21−0.5, 2) | **1.02** | 0.38 | 15.3% | **1.21** | 与 C2#7 并列最优 |

决策：**21d 窗口确认为离散度甜点**（10d 噪声/42d+衰减）；凸性变换保持 2Y。C4 = 最优形态 × **SUBINDUSTRY**（数据包 0.716）+ decay 上调 + 离散度×反号IR 复合。
预算：72/300 ｜ 入围 0/3

### Batch 10 ｜ 轨道 A ｜ analyst39 ｜ TOP3000/FAST/decay2 ｜ multisim 325mjT1gV4lG9OSl9BBYIpU

假说：复合价值骨架突破 1.04 平台

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | quantile价值 + 126d惊喜 复合 | 1.06 | 0.70 | 7.8% | 14bp | 1.12 | 强 |
| 2 | quantile价值 − 成长 | 1.03 | 0.66 | 7.4% | 14bp | 1.16 | 强 |
| 3 | **group_neutralize(quantile价值, sector)** | **1.07** | **0.74** | 7.8% | **15bp** | **1.16** | **A 轨最优** |
| 4 | 凸性价值 − 成长 | 0.22 | 0.05 | 6.0% | 1.9bp | 0.22 | 杀(凸性+差破坏) |
| 5 | roxlcxspeq(剔除非常项) 版 | 1.05 | 0.72 | 7.8% | 15bp | 1.12 | 强 |
| 6 | Q+TTM 混合 | 0.90 | 0.58 | 7.9% | 13bp | 0.99 | 杀 |
| 7 | ts_decay_linear 平滑 | 1.04 | 0.71 | 7.6% | 15bp | 1.11 | 强 |
| 8 | winsorize 原始值 | 0.88 | 0.58 | 14.3% | 8.7bp | 0.56 | 杀 |

决策：**analyst39 价值轴平台期 ~1.07**（复合微增不破局）。剩余大杠杆 = 中性化再探索（STATISTICAL 未试）与 universe 切换（用户要求探索不同 universe）。A5 = 最优形态 × STATISTICAL；若无起色 A6 = TOPSP500。
预算：80/300 ｜ 入围 0/3

### Batch 11 ｜ 轨道 B ｜ **shortinterest3**（换仓）｜ TOP3000/FAST/decay6 ｜ multisim 1AUlV9cL64WUa1y17NvvM7j9

假说：做空供需反向——低借券需求/低利用率/低费率 → 做多（拥挤做空溢价）

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|
| 1 | reverse(rank(vec_avg(shrt3_bar))) | 0.96 | 0.64 | 17.5% | 8.9bp | 1.30 | 4 | 子域弱 |
| 2 | bar 21d 平滑 | 0.83 | 0.57 | 9.7% | 12bp | 1.13 | 4 | 子域弱 |
| 3 | reverse(rank(vec_avg(utilizationpercent))) | 0.99 | 0.78 | 9.0% | 17bp | **1.62** | **2** | 强 |
| 4 | reverse(rank(vec_avg(mean_loan_rate))) | **1.13** | 0.68 | 16.0% | 7.3bp | 1.36 | 4 | 子域 0.2 弱 |
| 5 | reverse(group_rank(bar, subindustry)) | 1.02 | 0.63 | 17.4% | 7.6bp | 1.51 | 4 | 子域弱 |
| 6 | utilization delta21 反向 | -1.00 | -0.42 | 14.6% | — | -1.61 | 4 | 杀(变化量反向) |
| 7 | reverse(quantile(vec_avg(bar))) | 1.09 | **0.82** | 16.9% | 11bp | 1.54 | 4 | 子域临界 |
| 8 | **utilization_ratio 21d 平滑反向** | 1.01 | 0.80 | 8.3% | **19bp** | **1.72** | **2** | **B 轨最优** |

决策：**shortinterest3 全面强于 insiders3**（8 槽 6 个 ≈1.0+，2Y 普遍 1.3-1.7 = 信号活着）。#8 只差 LOW_SHARPE/LOW_FITNESS 两项。教训：水平量（levels）强、变化量（delta）反向失效。B5 = SECTOR 中性化（shrt3_bar 字段先验 0.895）+ 量(utilization)×价(loan_rate) 复合 + decay 8 + truncation 0.05（压回撤提 fitness）。
预算：88/300 ｜ 入围 0/3

### Batch 12 ｜ 轨道 C ｜ sentiment21 ｜ TOP3000/**SUBINDUSTRY**/decay8 ｜ multisim 4WkJVdo75jj9wN12FgKVKBH

假说：离散度 × SUBINDUSTRY（数据包 0.716, n=94）能超越 STATISTICAL

结果：全面回落（最优仅 0.83 vs STATISTICAL 下 1.03）。8 槽 sharpe 0.48-0.83，riskNeut 0.46-0.84。
决策：**再次验证"大样本先验优先"（STATISTICAL n=386 > SUBINDUSTRY n=94）**。C 轨回归 STATISTICAL，主形态锁定 `rank(ts_std_dev(net,21))`（1.03）与 signed_power 凸性版（1.02, 2Y 1.21）。剩余杠杆 = decay 上调 + truncation。
预算：96/300 ｜ 入围 0/3
调度备注：B4 突破（2Y 1.5-1.7 信号增强中）→ 下一批偏离轮转，预算倾斜 B5（SECTOR + 量价复合），A5 顺延。

### Batch 13 ｜ 轨道 B ｜ shortinterest3 ｜ SECTOR/decay8/trunc0.05 ｜ **整批失败 → 修复重发**

第一次发送 8 槽全部无 alpha ID。`lookINTO_SimError_message` 归因：槽 8 `hump(x, 0.01)` 位置参数写法错误（需 `hump=0.01` 命名参数）→ **1 条表达式报错导致其余 7 条整批 CANCELLED**（幽灵算子式失败模式的参数变体，浪费 ~5 分钟）。教训：批前本地校验不仅查算子名，还要查参数签名。修正后重发（multisim A4I4FfK54Bdci3WGqDmcCS 作废）。
预算：104/300（含 8 次作废）｜ 入围 0/3

### Batch 13b ｜ 轨道 B ｜ shortinterest3 ｜ SECTOR/decay8/trunc0.05 ｜ multisim r3Lx665i53nalPwt0aE8ac（修正重发）

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | 判定 |
|---|---|---|---|---|---|---|---|
| 1-2 | utilization 平滑反向 | 0.72 | 0.58 | 1.7% | 97bp | 1.10 | 换手破下限 |
| 3-4 | 量价复合 | 0.82 | 0.70-0.71 | 8.4-8.8% | 21-22bp | 1.15-1.18 | 弱于 FAST |
| 5 | quantile(bar 平滑) | 0.79 | 0.65 | 4.0% | 42bp | 1.15 | 换手临界 |
| 6 | group_rank subindustry | 0.77 | 0.53 | 2.2% | 53bp | 1.32 | 换手破下限 |
| 7 | loan_rate decay 平滑 | 0.91 | 0.64 | 5.5% | 22bp | 1.27 | 子域 0.01 |
| 8 | hump 包装 | 0.69 | 0.47 | 0.75% | 152bp | 0.96 | LOW_TURNOVER 失败 |

决策：**SECTOR+trunc0.05 全面弱于 FAST+trunc0.08（0.82 vs 1.13）**——字段级小样本先验（SECTOR 0.895, n=161）不敌配置实证；紧 truncation 抬 margin 压 sharpe 且换手崩到下限之下。B 锁定 FAST/decay6-8/trunc0.08，B6 = FAST 下量价复合 + decay 微调。
预算：112/300 ｜ 入围 0/3

### Batch 14 ｜ 新臂 N ｜ **other566**（应急高天花板臂）｜ TOP3000/REVERSION_AND_MOMENTUM/decay4

背景：三轨平台 ~1.0-1.13，启动第 4 臂。other566（Image-Based Financial Prediction, FinChart CNN）社区平均 sharpe 0.799 全场最高，R&M 中性化下 1.16（n=48）；other 金字塔 ×1.5 仅差 2 个。风格 = AI 模型分数（与价值/做空供需/情绪离散度均不同）。字段：l2r20_label(480α)/r20marsi_ret(237α)/l5r20gasfculr_ret/return。

Batch 14 结果（multisim 3GOmbadb4ouc5UzSZjtwB4）：

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | 子域 | 判定 |
|---|---|---|---|---|---|---|---|---|
| 1 | rank(l2r20_label) | 1.33 | 0.63 | 27.7% | 4.4bp | 1.58 | 0.75 | 强 |
| 2 | rank(ts_mean(label,5)) | 1.32 | 0.74 | 19.5% | 6.3bp | 1.46 | 0.79 | 强(换手margin达标) |
| 3 | rank(r20marsi_ret) | 1.25 | 0.48 | 32.5% | 2.9bp | 0.93 | 0.99 | 换手/margin 弱 |
| 4 | 平滑 marsi | 1.20 | 0.62 | 17.5% | 5.4bp | 0.71 | 0.88 | 2Y 弱 |
| 5 | l5r20gasfculr_ret | 0.89 | 0.30 | 31.6% | 2.2bp | 0.96 | — | 杀 |
| 6 | 20d+5d 标签混合 | **1.51** | 0.69 | 35.5% | 4.2bp | 1.16 | **1.03** | 强(需控换手) |
| 7 | 2d return 平滑 | 0.98 | 0.47 | 21.0% | 4.6bp | 1.33 | 0.85 | 杀 |
| 8 | **group_rank(label, subindustry)** | **1.80** | 0.72 | 31.3% | 3.2bp | **2.34** | 0.68 | **首破 1.58！** |

决策：**other566 臂一举突破**——#8 sharpe 1.80 / 2Y 2.34 双双 PASS，剩余缺口 = fitness(0.72<1)、子域(0.68<0.78)、换手(31.3%>30%)、margin(3.2<5bp)。N2 = 组内排名 × ts_mean 平滑（#2 已证明平滑可同时修换手+margin）× 双横区混合（#6 已证明修子域）× decay 6。
预算：120/300 ｜ 入围 0/3（1 个 1.80 近失候选）

### Batch 15 ｜ 臂 N ｜ other566 ｜ R&M/decay6 ｜ multisim ErIDngH550S9R9G5Tw8rtp

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | 子域 | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | group_rank(ts_mean(label20,5),subind) | 1.76 | 0.87 | 18.9% | 4.9bp | 2.29 | 0.79✓ | 1 | 差 fitness+margin 毫厘 |
| 2 | 组内 20d−5d 混合 | 1.98 | 0.85 | 31.1% | 3.7bp | 2.10 | 0.94✓ | 1 | 换手超 30% |
| 3 | 平滑组内 + rank5d 混合 | 1.78 | 0.89 | **23.9%** | **5.0bp** | 1.62✓ | 0.99✓ | 1 | **全指标最接近** |
| 4 | group_rank(label, industry) | 1.74 | 0.81 | 25.7% | 4.3bp | 2.01 | 0.77✓ | 1 | 强 |
| 5 | rank 平滑混合(无 group) | 1.23 | 0.66 | 21.8% | 5.8bp | 1.08 | 0.72 | 3 | group 是关键 |
| 6 | ts_decay_linear(group_rank,5) | **1.82** | **0.92** | 20.1% | **5.1bp✓** | 2.33 | 0.71✗ | 2 | 子域差 0.08 |
| 7 | 组内 label20 + marsi 混合 | 1.68 | 0.80 | 26.9% | 4.6bp | 1.61✓ | **1.04✓** | 1 | 强 |
| 8 | **group_rank(20d−5d 混合)** | **2.00** | 0.85 | 31.3% | 3.6bp | 2.16 | 0.98✓ | 1 | sharpe 王者, 换手超 |

决策：唯一残余短板 = **fitness<1**（0.85-0.92）与换手/margin 微调。N3 = 双平滑混合 / #2#8 加 ts_decay_linear / signed_power 凸性提收益 / quantile / hump 控换手。距离合格一步之遥。
预算：128/300 ｜ 入围 0/3

### Batch 16 ｜ 臂 N ｜ other566 ｜ R&M/decay6 ｜ multisim 27mlsD7zj5dccmYx8AXiQP0

| # | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | 子域 | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | decay混合(组内20d−5d) | 1.84 | 0.90 | 23.0% | 4.8bp | 2.09 | 0.79✗(限0.8) | 2 | 毫厘 |
| 3 | **decay(group(rank混合))** | **1.88** | **0.91** | 23.1% | 4.7bp | **2.16✓** | **0.84✓** | **1(仅fitness)** | 最接近 |
| 5 | decay(group20d) + marsi | 1.69 | 0.85 | 24.6% | **5.1bp✓** | 1.70✓ | **1.03✓** | 1 | 稳健备选 |
| 7 | quantile(组内混合) | 1.95 | 0.80 | 31.5% | 3.4bp | 2.18 | 0.82✗ | 2 | 换手超 |
| 8 | hump 0.008 | 0.57 | 0.20 | 2.9% | 10.5bp | 0.72 | — | 3 | hump 过度杀信号 |

（其余槽 1.40-1.74）决策：fitness 数学：1.88×√(5.4%/19%)≈1.0 → **把换手 23%→19% 即达标**。N4 = 批级 decay 6→10 + 平滑变体扫描。
预算：136/300 ｜ 入围 0/3

### Batch 17 ｜ 臂 N ｜ other566 ｜ R&M/**decay10** ｜ multisim 4o7F5Xfph5hIaNJWzT5FxuU ⭐

| # | alpha_id | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | 子域 | FailedRA |
|---|---|---|---|---|---|---|---|---|---|
| 1 | gJ9GQA3g | decay5(group(rank混合)) | 1.93 | 1.07 | 18.6% | 6.1bp | 2.30 | 0.87 | **0** ✅ |
| 2 | **wpEGYmRx** | **decay10(group(rank混合))** | **1.93** | **1.18** | **15.5%** | **7.5bp** | **2.34** | 0.88 | **0** ✅ |
| 3 | 78nmZAwQ | 平滑 label+marsi | 1.63 | 1.00 | 16.3% | 7.6bp | 1.34✗ | 0.96 | 1(2Y) |
| 4 | 1YzKx97X | decay10(组内混合) | 1.90 | 1.17 | 15.5% | 7.6bp | 2.29 | 0.85 | **0** ✅ |
| 5 | rKPG53oa | group(平滑20d−5d) | 1.96 | 1.04 | 19.5% | 5.6bp | 2.33 | 0.96 | **0** ✅ |
| 7 | zqRGYMm8 | decay8(label+marsi) | 1.71 | 1.09 | 15.7% | 8.2bp | 1.49✗ | 1.01 | 1(2Y) |

**4 条候选 Failed RA = 0，全部用户指标达标（sharpe/fitness/2Y/margin/换手/算子数）**。首选 wpEGYmRx（fitness 最高、换手最低）。经济故事：FinChart CNN 对 20 日前瞻收益的分类信号，在子行业内相对排名（剥离行业 beta），减去 5 日短线信号的反向（剔除超短期已定价部分），10 日线性衰减平滑控换手；R&M 中性化剥离反转/动量风险因子暴露。
下一步：wpEGYmRx 进入 robustness 审计（yearly/pnl/风险中性视图/相关性）；B/C 轨注入 N 配方（组内结构+decay10+复合）。
预算：144/300 ｜ 入围候选 1/3（待审计）

### 候选审计 #1 ｜ wpEGYmRx ｜ other566 ｜ ⭐→❌ ProdCorr 拒

- **门槛复核** (get_alpha_details): sharpe 1.93✓ fitness 1.18✓ tvr 15.5%✓ margin 7.5bp✓ 2Y 2.34✓ 子域 0.88✓ Failed RA=0✓ 算子 6<8✓（主中性化即 R&M 风险中性化族）
- **年度归因** (get_alpha_yearly_stats): 近 3 年 sharpe 2.47/2.04/2.98（每年 >0.3✓），近3年 CV 0.15✓，衰减比 2.98/1.93=1.54✓（增强中），近 3 年无平年✓，max/min 1.46✓。软旗：2019 平(0.43)/2020 负(-1.46)/2014-15 异常高(5.7/4.7 早期覆盖 artifact)——按近 3 年 regime 规则仅记入描述。
- **Self-corr**（本地，免额度）: max 0.49 ✓（<0.7）
- **ProdCorr** (check_correlation): **0.8289 ✗ > 0.7 → 按用户规则 REJECT**。直方图显示池内仅 4 个 alpha >0.7（2 个 0.7-0.8、2 个 0.8-0.9）——l2r20+l2r5 标签组合被社区挖穿（480α 字段使用量的代价）。
- **决定**: 进入 repair 相关性轮换（换腿 l2r5res/marsi、换组 industry/sector、换标准化族 zscore/quantile/ts_rank、vector_neut 正交化范式）。N4 另外 3 条 RA=0 变体大概率同池高相关，不浪费 ProdCorr 额度逐个查，直接结构轮换后再查。

### Batch 18 ｜ 轨道 B ｜ shortinterest3 ｜ FAST/decay10 ｜ multisim 3JYhqJ4hN4WAbqodj2O6Pt8

N 配方反哺（组内结构+decay10+量价复合）：最优 P0OzZVeE 复合 1.23/0.95（2Y 1.72），pwKGPL06 1.17/**1.00**（fitness 过线）。但 **子域 sharpe 0.36-0.46 结构性失败**（做空供需信号集中小盘，TOP1000 衰减）——B 轨天花板 ~1.2，1.58 缺口 0.35。B7 计划：hump 子域修复（YW79016 论坛技巧）+ 若仍无解则 B 轨降级为近失池，冷启动 news54（事件风格，STATISTICAL 0.861 先验）。
预算：152/300 ｜ 入围候选 1/3（wpEGYmRx 待去相关）

### Batch 19-20 ｜ 臂 N 去相关轮换 ｜ multisim 22tXD26oq5i4cJjuUvn0ti2 + ProdCorr 检查

N5 结构轮换产出 4 条 RA=0 变体：quantile 版 1.99/1.24、marsi+industry 版 1.81/1.10、**单字段立方版 1.74/1.04**、sector 版 1.69/1.13。ProdCorr 检查路径：wpEGYmRx 0.829✗ → E5ezR10P(marsi 腿) 0.779✗ → **3qePVw3Z(单字段+signed_power³) 0.593✓**——repair skill "signed_power 指数轮换"直接兑现（-0.24 相关性降幅）。

### 🏆 入围 #1 ｜ 3qePVw3Z ｜ other566 ｜ AI 图表模型凸性风格

`ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 3), 10)`
- 设置: USA/TOP3000/D1/REGULAR, REVERSION_AND_MOMENTUM, decay10, trunc0.08, max_trade ON
- 指标: **sharpe 1.74 / fitness 1.04 / tvr 14.7% / margin 7.2bp / 2Y 2.79 / 子域 0.76** ｜ Failed RA = 0 ｜ 算子 4 ｜ 单字段
- 相关性: **ProdCorr 0.593 ✓ ｜ SelfCorr 0.416 ✓**
- 年度: 近3年 1.42/3.16/2.37（全正✓）CV 0.31✓ 衰减比 1.36✓ max/min 2.2✓；软旗: 2016 平/2020 负/2014-15 偏高（老年份，仅记录）
- 属性已设: name=0.5927, GREEN, tags=[PowerPoolSelected, wqb-share-03, ai-chart-model]；**未提交**
- 金字塔: USA/D1/OTHER ×1.5（未点亮 → 将点亮）
- 经济故事: 子行业内对 CNN 图表模型 20 日预测的极端信念做凸性押注，立方变换聚焦尾部、降低拥挤；R&M 剥离反转/动量暴露。

预算：176/300 ｜ **入围 1/3** ｜ 剩余轨道：B(shortinterest3 1.23)/C(sentiment21 1.03)/A(analyst39 1.07)/备选 news54
风格约束更新：入围#1 为价格形态类 → 排除 macro38（技术评级同族，互相关风险），2/3 号从非价格族出。

### Batch 21-22 ｜ N6 备份 + C5 判决

- N6（other566 去相关备份）: ZYKzAaVY（res 腿+industry）1.75/1.09/子域1.02/RA=0 —— 备份入围池。预测修正(ts_delta 标签)反向失效(-0.27)；ts_regression 残差 0.35；group_vector_neut 1.26。
- C5（sentiment21 decay12 重平滑）: 最优 zscore(winsorize(std21)) 1.09/0.45、quantile 1.03/0.41。**离散度收益量级不足以支撑 fitness>1（2.3% 收益 @13% 换手）→ C 轨降级近失池**。
预算：192/300 ｜ 入围 1/3
决策：剩余 2 席主攻 = B(shortinterest3, R&M 未试) + A(analyst39, R&M 未试)；同批混测各 4 槽（单数据集纯度按 alpha 计）。备选 = news54 冷启动。

### Batch 23-24 ｜ R&M 迁移测试失败 + O 臂（other571 注意力）冷启动命中

- Batch 23（R&M × shortinterest3/analyst39 各 4 槽）：B 0.83-0.96、A 0.54-0.84 —— **R&M 魔力特定于模型标签信号，不可盲目迁移**（课件教训）。news54 字段全为文本/时间戳，弃。
- Batch 24（O1, other571 Wikipedia 注意力, STATISTICAL/decay6）：**注意力异常做多方向命中** —— `rank(ts_zscore(ts_backfill(viewstoday,63),63))` 1.50/0.49/28.4%/2.2bp/2Y 2.56/**子域 1.19**（Failed RA 仅剩 sharpe/fitness 2 项）；ratio 版 1.32/2Y 2.88/子域 1.14。反向全负（注意力=正向动量信号）；mobile 占比无信息。风格 = 投资者注意力（非价格数据），与入围#1 图表模型机制不同。
- 瓶颈：fitness 0.49（收益 3% @ 换手 28%）、margin 2.2bp。O2 = 平滑族 + decay12 + signed_power 凸性。
预算：224/300 ｜ 入围 1/3

### Batch 25-27 ｜ O2 精修 + M1 StarMine + M2 macro38

- O2（other571 平滑族, decay12）: 平滑即衰减（1.50→1.33@ts_mean5, tvr 14%）；注意力信号半衰期短，fitness 卡 0.5 → **other571 进近失池**（最佳裸信号 1.50/0.49/2Y 2.56/子域 1.19）。
- M1（model38 StarMine 估值, R&M/decay10）: 最佳 0.98/0.59（2Y 1.89, margin 17.8bp 厚但收益慢）→ 估值模型臂天花板 ~1.0，弃。
- M2（macro38 技术评级, STATISTICAL/decay10）: 发射中——最后的高先验臂（社区 0.539/STATISTICAL 0.68/macro 金字塔未点亮）。
预算：256/300 ｜ 入围 1/3

### Batch 28 ｜ S1 sentiment22 终批 ｜ 全灭

离散度冠军形态移植 sentiment22 全部失效（最佳 0.55；离散度方向甚至为负）。**教训：离散度溢价是 sentiment21（TRNA transformer 分数）特有的数据集级现象，同类目≠可迁移**。
预算：280/300 ｜ 挖矿阶段按预算收束

---

## 终章：最终结果与结论（2026-07-29）

### 最终互相关矩阵（compute_mutual_correlation, 4 年日收益, 本地计算）

| | 3qePVw3Z(图表模型) | pwKGPL06(做空供需) | 88eJREzq(注意力) | ZYKzpLqx(价值) |
|---|---|---|---|---|
| 3qePVw3Z | 1 | 0.447 | **-0.026** | **0.360** |
| pwKGPL06 | 0.447 | 1 | -0.065 | **0.766** ⚠ |
| 88eJREzq | -0.026 | -0.065 | 1 | -0.014 |
| ZYKzpLqx | 0.360 | 0.766 ⚠ | -0.014 | 1 |

- **两两 <0.4 的最大三元组 = [图表模型, 注意力, 价值]**（风格隔离被数据证实）
- 发现：做空供需×价值相关 0.766——低借券关注股与便宜股高度重叠（共享小盘价值暴露），"风格不同"必须以相关性数据仲裁，不能凭数据集类目判断

### 交付清单

| 状态 | alpha_id | 数据集/风格 | sharpe | fit | tvr | margin | 2Y | FailedRA | ProdCorr | 互相关组 |
|---|---|---|---|---|---|---|---|---|---|---|
| ✅ **完整达标+已设属性** | **3qePVw3Z** | other566 / AI图表模型凸性 | 1.74 | 1.04 | 14.7% | 7.2bp | 2.79 | 0 | **0.593** | ✓ |
| 🟡 近失(差 sharpe/fitness/margin) | 88eJREzq | other571 / 注意力异常 | 1.50 | 0.49 | 28.4% | 2.2bp | 2.56 | 2 | 未测 | ✓ |
| 🟡 近失(差 sharpe/fitness) | ZYKzpLqx | analyst39 / 盈利收益率价值 | 1.07 | 0.74 | 7.8% | 15bp | 1.16 | 3 | 未测 | ✓ |
| 🟡 近失(差 sharpe/子域) | pwKGPL06 | shortinterest3 / 做空供需 | 1.17 | 1.00 | 10.2% | 18bp | 1.62 | 2 | 未测 | ✗(与价值0.77) |
| 🟢 同数据集合格备份 ×4 | rKPG53oa/1YzKx97X/gJ9GQA3g/ZYKzAaVY | other566 | 1.69-1.96 | 1.04-1.18 | ✓ | ✓ | ✓ | 0 | 未测 | — |

**结果实话**：300 次模拟预算内，"3 个不同数据集全指标达标"完成 1/3；另有 4 条同数据集(other566)全指标合格备份和 3 条不同风格近失候选。互相关 <0.4 的三风格篮子结构已验证成立，缺口是近失者的 sharpe/fitness 距离（0.3-0.5）。**未调用 submit_alpha——全部留给用户手动决策**。

#### 20+ 批多样性评估（第二次/终评）

- **数据集探索**: 9 个（analyst39/insiders3/sentiment21/shortinterest3/other566/other571/model38/macro38/sentiment22），5 类金字塔触达，other 金字塔将由入围者点亮(×1.5)
- **算子探索率**: ~30/127 ≈ 24%；**字段探索率**: 40+ 字段
- **骨架**: 动量/价值比/异常度/离散度/供需水平/注意力异常/模型标签混合/凸性尾部/正交化 9 类
- **胜负归因**: 唯一达标配方 = 模型预测标签 × group_rank 组内 × 双横区混合/凸性 × ts_decay_linear × R&M × decay10；ProdCorr 破局靠 signed_power³ 单字段凸性（0.83→0.59）
- **失效风险记录**: 入围者 2019 平/2020 负（老年份软旗）；预测修正(标签 ts_delta)反向失效；离散度溢价不可跨数据集迁移
- **过程教训 Top10**: ①中性化大样本先验可靠、小样本必须证伪（SLOW n=51、SECTOR n=161、SLOW_AND_FAST n=37 全部翻车）②FAST/R&M 等风险族中性化是 alpha 放大器但不可盲移植 ③情绪方向反向定价、离散度>方向 ④数据体检决定预处理（form4 覆盖0.41→backfill；月频→长窗）⑤一条表达式参数错误废整批 ⑥水平量强于变化量（shortinterest、oth566 标签均如此）⑦fitness=sharpe×√(收益/换手) 是硬数学，平滑换手是最后一公里 ⑧ProdCorr 死区避让靠低使用字段+形态凸性 ⑨社区甜点区先验（100-3000 提交+高 sharpe）与平台推荐分交叉验证有效（sentiment21/shortinterest3/other566 全部来自该名单）⑩风格差异以互相关矩阵仲裁而非类目直觉（做空供需×价值 0.77 反例）

- **算子探索率**: 已用 rank/group_rank/zscore/group_zscore/ts_zscore/ts_delta/ts_mean/ts_std_dev/ts_ir/ts_av_diff/ts_decay_linear/ts_backfill/ts_sum/ts_rank/quantile/signed_power/winsorize/subtract/divide/reverse/vec_avg/vec_sum/group_neutralize ≈ 23 个核心算子 / 127 可用 ≈ 18%
- **字段探索率**: analyst39 12/36；insiders3 9/61；sentiment21 6/258（离散度族聚焦）；shortinterest3 待开
- **骨架多样性**: 动量(ts_delta)/价值(ratio)/异常度(ts_zscore)/离散度(ts_std_dev)/IR/复合(subtract-rank) 6 类
- **风格多样性**: A=价值(盈利收益率), B=聪明钱(内部人买入→转做空供需), C=情绪不确定性溢价 — 三风格结构隔离 ✅
- **预处理**: ts_backfill(低覆盖)/winsorize/ts_mean 平滑/vec_avg 聚合 ✅
- **收益归因观察**: A 轨 margin 型（15bp 慢信号）；B 轨换手型（10-17%）；C 轨介于两者
- **失效风险**: A 轨 PnL 实现周期 120d（慢）；C 轨 std10d 换手临界；B 轨 2Y 弱于全期（近年衰减警惕）
- **教训沉淀**: ①中性化先验兑现（FAST 使 A 轨翻倍）②小样本先验证伪（SLOW n=51）③情绪反向定价④离散度桶 > 方向桶

---

# ===== 新会话分隔 ===== 日期: 2026-08-01 ｜ 账号: mthyzx@126.com ｜ 执行: Trae + wqb-mcp (HTTP@8876) + brain-alpha skills

## 目标复述（mthyzx 账号 /goal）
USA/D1/max_trade=ON/REGULAR/TOP3000；3 个不同数据集、完全不同策略风格、单数据集、未提交 alpha，彼此 corr<0.4，点亮未点亮金字塔。每 alpha: sharpe>1.58, fitness>1, 2Y>1.6, margin>5bp, turnover 5-30%, ops<8, ra_failed=0；risk-neut 视图 sharpe>1, fitness>0.7, margin>5bp。约束: multi_create_simulate 8 并发(禁 create_simulate)；禁 trade_when/add/multiply(用 subtract/-/divide//)；不创建自动化任务；生产 corr 未出或>0.7 不提交(用户手动)；每 alpha 过 test_robust+严格过拟合后 set_alpha_properties；每 10 轮多样性评估。

## 起点（继承自上一会话结论 + 本会话零成本预筛）
- 金字塔 USA/D1 未点亮高乘数: sentiment(1.5)/model(1.4)/option(1.3)/analyst(1.3)/news(1.2)/risk(1.2)；已点亮: pv/fundamental/other/institutions/earnings。
- 3 目标数据集(按乘数+未点亮): ①sentiment21(sentiment,1.5) ②model267(model,1.4) ③option13(option,1.3)。
- WebDataScope 预筛: sentiment21 count915/sharpe0.568/fitness0.638，主导最优中性化 STATISTICAL(0.645,n=386)/SUBINDUSTRY(0.716,n=94)/SLOW_AND_FAST(0.782,n=37)。
- sentiment21 选定 5 字段(WebDataScope 字段级先验, coverage~1.0 无需 backfill): snt21neg_mean_276(count60,sharpe0.987)/snt21pos_mean_281(count70,sharpe0.833)/snt21_2pos_conf_up_150(count17,sharpe1.078,STATISTICAL1.381)/snt21_2neg_median_161(count9,sharpe0.954,STATISTICAL1.607)/snt21_2pos_mean_163(count24,sharpe0.882,STATISTICAL1.234)。
- 前序 848416881 会话对 sentiment21 的教训(必读): C5 批 decay12 重平滑，最优 zscore(winsorize(std21)) 1.09/0.45、quantile 1.03/0.41 → "离散度收益量级不足以支撑 fitness>1，C 轨降级近失池"；Batch28 离散度形态移植 sentiment22 全灭 → 离散度溢价是 sentiment21 数据集级特有现象。本会话需突破此 1.09 天花板，重点尝试: 论坛新模板 / 不同中性化(SLOW_AND_FAST/SUBINDUSTRY 大样本 STATISTICAL 未穷尽的方向) / 未试字段族。

## 批次记录（mthyzx 会话）

### Batch M01 ｜ sentiment21 ｜ TOP3000/STATISTICAL/decay3/trunc0.08/max_trade ON ｜ multisim FRO5xbks4ZPbgn19YHNv2bN

假说：情绪方向信号（pos/neg mean 及 2pos/2neg 分位）经 rank/zscore 标准化后预测收益。中性化取 WebDataScope 大样本最优 STATISTICAL。

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | subUniv | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rank(pos281) - rank(neg276) | -0.23 | -0.02 | 87.7% | -0.17bp | -1.41 | -0.59 | 5 | 杀 |
| 2 | rank(ts_delta(neg276,5)) | -0.29 | -0.03 | 109.2% | -0.17bp | -0.68 | -0.29 | 5 | 杀 |
| 3 | -rank(ts_zscore(neg276,22)) | **0.68** | 0.09 | 101.7% | 0.36bp | -0.46 | 0.52 | 4 | 线索†(反转方向) |
| 4 | group_rank(pos281,sub)-group_rank(neg276,sub) | -0.56 | -0.09 | 70.8% | -0.49bp | -0.99 | -0.60 | 5 | 杀 |
| 5 | ts_rank(2pos_mean_163,10) | -0.66 | -0.09 | 106.6% | -0.34bp | -2.08 | -0.63 | 5 | 杀 |
| 6 | rank(ts_mean(pos281,10)-ts_mean(neg276,10)) | -0.52 | -0.12 | **20.7%** | -1.0bp | 0.67 | -0.40 | 4 | 线索‡(平滑降tvr) |
| 7 | rank(2pos_conf_up_150)-rank(2neg_median_161) | -0.61 | -0.09 | 97.4% | -0.42bp | -1.65 | -0.80 | 5 | 杀 |
| 8 | ts_decay_linear(rank(2neg_median_161),5) | 0.15 | 0.01 | 80.3% | 0.12bp | **1.05** | 0.04 | 5 | 线索(2Y最佳) |

多样性：外层 5 种(rank/group_rank/ts_rank/ts_decay_linear/subtract) ✅ 窗口 5/10/22 ✅ 双字段 4/8 ✅
决策：全员 HIGH_TURNOVER(0.71-1.09，日频情绪噪声极大) + sharpe 普遍偏低。†线索#3：-rank(ts_zscore(neg276,22)) 反转方向(负情绪高→做空)sharpe 0.68 最优 → 负情绪反转有效。‡线索#6：ts_mean 窗口10 把 tvr 压到 20.7%(唯一进 5-30% 区间) → 平滑窗口有效。线索#8：2neg_median_161 的 2Y=1.05(全样本最佳) → 该字段近期有信号。M02 = 反转方向 + 重平滑(decay10, ts_mean/ts_decay_linear 窗口22, ts_zscore 窗口44-66)。
预算：8/300 ｜ 入围 0/3

### Batch M02 ｜ sentiment21 ｜ TOP3000/STATISTICAL/decay10/trunc0.08/max_trade ON ｜ multisim 6nQWQ4jL52x97ELqLSl9S0

反转方向 + 重平滑(decay10)。窗口 ts_zscore 44-66、ts_mean/ts_decay_linear 22。

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | subUniv | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | -rank(ts_zscore(neg276,66)) | 0.30 | 0.03 | 94.0% | 0.17bp | -0.83 | 0.24 | 4 | 杀 |
| 2 | -rank(ts_mean(ts_zscore(neg276,22),22)) | 0.05 | 0.0 | **13.8%** | 0.13bp | 0.14 | 0.19 | 3 | 杀(过平滑杀信号) |
| 3 | ts_decay_linear(-rank(ts_zscore(neg276,44)),22) | 0.17 | 0.01 | 83.8% | 0.11bp | -1.35 | 0.0 | 5 | 杀 |
| 4 | -rank(ts_zscore(2neg_median_161,66)) | 0.06 | 0.0 | 94.8% | 0.004bp | -0.86 | -0.31 | 5 | 杀 |
| 5 | ts_decay_linear(-rank(ts_zscore(2neg_median_161,44)),22) | 0.13 | 0.01 | 84.4% | 0.009bp | -1.18 | -0.30 | 5 | 杀 |
| 6 | rank(ts_mean(neg276,22)-ts_mean(pos281,22)) | **0.59** | **0.18** | **9.7%** | 2.38bp | -0.24 | 0.48 | 3 | 线索(tvr达标,反转方向) |
| 7 | -rank(ts_zscore(pos281,66)) | 0.57 | 0.07 | 94.6% | 0.32bp | -0.24 | 0.63 | 4 | 杀 |
| 8 | ts_decay_linear(-rank(ts_zscore(2pos_conf_up_150,44)),22) | **0.67** | 0.10 | 84.7% | 0.44bp | 0.12 | **0.83** | 4 | 线索(subUniv佳) |

决策：**降turnover关键机制确认 = ts_mean长窗口包裹信号**(仅#2/#6进5-30%区间,ts_zscore/ts_decay_linear单独全0.84-0.95)。#6反转方向(neg-pos)sharpe 0.59+tvr9.7%达标+margin2.38bp,但sharpe/margin距阈值仍远;#8 subUniv 0.83但tvr超标。信号普遍弱(最高0.67),2Y全<1.6 → **方向信号族(pos/neg mean及分位)已穷尽,天花板~0.67,与前序会话1.09(std离散度)合证sentiment21弱信号数据集**。按"模板穷尽+论坛无计才切"原则,M03前先查论坛sentiment21模板找新骨架(零模拟成本),再决定batch3方向。
预算：16/300 ｜ 入围 0/3

### sentiment21 pivot 决策（用户确认）

论坛搜索 sentiment21 / sentiment 均零结果。sentiment21 综合证据:①方向族天花板0.67(本会话M01/M02) ②离散度族天花板1.09(前序848416881会话C5) ③alt中性化(SLOW/SECTOR/SLOW_AND_FAST)全部翻车(前序教训#1) ④论坛空。距 sharpe>1.58 缺口0.5-0.9,单批难突破。用户确认 **pivot 到 model267**(model ×1.4 未点亮金字塔,全新数据集无已知天花板)。sentiment21 暂留近失池(若后续model267/option13顺利且有剩余预算可回马)。

### model267 零成本预筛（WebDataScope USA_1）

- dataset=model267, count=162, **sharpe=0.793, fitness=0.874**(显著强于sentiment21的0.568/0.638)
- 最优中性化: **STATISTICAL(1.101,n=29)** > CROWDING(0.88,n=24) > SUBINDUSTRY(0.758,n=31)
- 中性化选择: STATISTICAL(大样本+最高均值+前序sentiment21已验证可靠)。CROWDING n=24小样本作备选。
- 下一步: get_datafields(dataset_id=model267) 取字段 → WebDataScope字段级先验选1-2字段(高alphaCount+高sharpe) → 设计8表达式(STATISTICAL/decay待定/trunc0.08/max_trade ON,禁add/multiply/trade_when,ops<8,1-2字段) → multi_create_simulate。
- model267 金字塔: USA/D1/MODEL ×1.4(未点亮,将点亮)。

### model267 不可用 → model238 pivot（用户确认）

- get_datasets(search=model) 返回 210 个数据集，**无 model267**；get_datafields(dataset_id=model267) 返回 count=0。model267 在平台已下线/不存在，WebDataScope 的 model267 先验(0.793/STATISTICAL1.101)不可用。
- webdata 含大量其他平台存在的 model 数据集先验。比对候选(webdata sharpe / 最佳中性化 / 平台字段数 / alphaCount / valueScore / coverage)：
  - model238 SmartHoldings: 0.399 / STATISTICAL 0.763(n=29) / 22字段 / α67 / 5.0 / 0.9671
  - model257 国际情感NLP: 0.506 / REVERSION_AND_MOMENTUM 0.433 / 10 / α34 / 4.0 / 0.7625
  - model264 DL预测: 0.411 / STATISTICAL 0.476 / 2083 / α8043 / 3.0 / 0.9992
  - model262 DNN基本面: 0.375 / INDUSTRY 0.538 / 1208 / α3410 / 3.0 / 0.8044
- 用户确认 **pivot 到 model238**（新颖α67低竞争 + STATISTICAL中性化响应0.763同model267模式 + coverage高 + 字段少易选 + SmartHoldings慢信号契合ts_mean降turnover）。

### Batch M03 ｜ model238 ｜ TOP3000/STATISTICAL/decay4/trunc0.08/max_trade ON ｜ multisim 4rnKPFgM94wH9uO1KwG5Kn

假说：SmartHoldings 动量族(global/region_change_rank)正向 + 拥挤反转族(region_owner_rank)subtract 复合，ts_mean 包裹降 turnover。字段 A=mdl238_global_change_rank(α7) C=mdl238_region_change_rank(α7) B=mdl238_region_owner_rank(α11)。

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | subUniv | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rank(ts_mean(A,20)) | -0.32 | -0.07 | 8.4% | -1.5bp | 0.09 | -0.18 | 4 | 杀 |
| 2 | ts_zscore(ts_mean(A,40),120) | 0.00 | 0.00 | 7.4% | 0.0bp | -0.52 | 0.37 | 3 | 杀 |
| 3 | ts_rank(ts_mean(A,60),120) | **0.22** | 0.04 | 6.8% | 1.15bp | 0.01 | 0.33 | 3 | 线索(最高sharpe) |
| 4 | ts_decay_linear(A,60) | -0.13 | -0.02 | 6.1% | -0.9bp | 0.16 | -0.31 | 4 | 杀 |
| 5 | rank(ts_mean(C,40)) | 0.00 | 0.00 | 5.9% | 0.0bp | 0.37 | -0.28 | 4 | 杀 |
| 6 | rank(subtract(ts_mean(A,20),ts_mean(B,20))) | -0.27 | -0.06 | 6.6% | -1.8bp | 0.21 | -0.27 | 4 | 杀 |
| 7 | ts_zscore(subtract(ts_mean(A,40),ts_mean(B,40)),120) | -0.26 | -0.05 | 7.2% | -1.4bp | -1.08 | 0.16 | 3 | 杀 |
| 8 | ts_rank(subtract(ts_mean(C,20),ts_mean(B,20)),120) | -0.41 | -0.10 | 9.9% | -1.6bp | -0.75 | 0.21 | 3 | 杀 |

多样性：外层 4 种(rank/ts_zscore/ts_rank/ts_decay_linear) ✅ 窗口 20/40/60/120 ✅ 双字段 3/8 ✅
决策：**全灭**。关键：①**turnover 完美解决**——ts_mean 包裹把 tvr 压到 5.9%-9.9%(全在5-30%区间，sentiment21教训成功移植) ②**动量族(A/C)正向无信号**——sharpe -0.41~0.22，最高#3仅0.22，距1.58极远 ③**拥挤族B subtract组合更差**——#6-8全负。重大遗漏：**未测水平偏好族**(mdl238_sector_rank α12最高/mdl238_global_rank α5)与screening族——WebDataScope的0.763很可能来自水平族。M04 = 转水平族+拥挤反转(negate)+screening，测方向。
预算：24/300 ｜ 入围 0/3

### Batch M04 ｜ model238 ｜ TOP3000/STATISTICAL/decay4/trunc0.08/max_trade ON ｜ multisim 4io8qw2EL4XDbpVPowwL5pj

假说：水平偏好族(sector/global_rank)+screening族正向，拥挤反转(negate)，测方向。字段 S=mdl238_global_screening_rank G=mdl238_global_rank Sec=mdl238_sector_rank B=mdl238_region_owner_rank。

| # | 表达式 | sharpe | fit | tvr | margin | 2Y | subUniv | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rank(ts_mean(Sec,20)) | 0.50 | 0.16 | 6.2% | 4.4bp | 1.06 | 0.28 | 3 | 线索 |
| 2 | rank(ts_mean(G,40)) | 0.56 | 0.20 | 5.1% | 6.4bp | **1.44** | 0.21 | 4 | 线索(2Y强) |
| 3 | -rank(ts_mean(B,20)) | -0.18 | -0.03 | 4.3% | -2.0bp | 0.26 | -0.18 | 4 | 杀(拥挤非反转) |
| 4 | rank(ts_mean(S,40)) | **0.58** | 0.22 | 4.9% | **7.4bp** | **1.47** | 0.26 | 3 | **线索(screening最强)** |
| 5 | rank(subtract(ts_mean(Sec,20),ts_mean(B,20))) | 0.25 | 0.05 | 5.1% | 2.2bp | 0.92 | 0.15 | 3 | 杀(减拥挤破坏) |
| 6 | ts_zscore(subtract(G,B),120) | -0.14 | -0.02 | 6.3% | -0.9bp | -1.24 | 0.03 | 3 | 杀 |
| 7 | ts_rank(subtract(Sec,global_owner),120) | 0.09 | 0.01 | 6.7% | 0.5bp | -0.54 | 0.16 | 3 | 杀 |
| 8 | ts_decay_linear(S,60) | 0.57 | 0.22 | 4.9% | 7.3bp | 1.42 | 0.27 | 3 | 线索(screening decay版) |

多样性：外层 4 种(rank/-rank/ts_zscore/ts_rank/ts_decay_linear) ✅ 窗口 20/40/60/120 ✅ 双字段 3/8 ✅
决策：**水平/screening族证实是alpha来源**。关键：①**screening族最强**——#4 sharpe0.58/2Y1.47/margin7.4bp，2Y已逼近1.58阈值 ②**global_rank次之**0.56/2Y1.44 ③**拥挤族是正向信号(动量/延续)非反转**——#3 negate为负(-0.18)，高拥挤预测正收益；M03的subtract组合方向错误 ④**subtract双字段全弱于单字段**——#5-7<#1-4。全距sharpe0.5-0.58距1.58仍远，但**2Y强(1.42-1.47)=信号近期增强**。M05 = 套用other566获胜配方(group_rank子行业剥beta+signed_power凸性+ts_decay_linear)放大screening/global_rank，这是other566从1.33→1.80的最大杠杆。
预算：32/300 ｜ 入围 0/3

### Batch M05 ｜ model238 ｜ TOP3000/STATISTICAL/decay4/trunc0.08/max_trade ON ｜ multisim j53fZ5MZ50c8NQvOJUH9lt

假说：套用 other566 获胜配方（group_rank 子行业剥 beta + signed_power 凸性 + ts_decay_linear + divide 双字段比）放大 screening/global_rank 信号。字段 S=mdl238_global_screening_rank G=mdl238_global_rank。

| # | alpha_id | 表达式（核心） | sharpe | fit | tvr | margin | 2Y | subUniv | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | xAd7oQkJ | group_rank(ts_mean(S,20),subindustry) | 0.66 | 0.23 | 5.3% | 5.9bp | 1.07 | 0.53 | 3 | 杀 |
| 2 | 3qemOxeZ | group_rank(ts_mean(S,40),industry) | 0.68 | 0.26 | 4.8% | 7.7bp | 0.99 | 0.42 | 3 | 杀 |
| 3 | P0OLb6Oq | group_rank(ts_mean(G,20),subindustry) | 0.66 | 0.23 | 6.6% | 4.7bp | 0.87 | 0.43 | 3 | 杀 |
| 4 | N1REG6Rp | signed_power(subtract(group_rank(ts_mean(S,20),sub),0.5),3) | **0.77** | 0.31 | 5.8% | 6.9bp | **1.20** | 0.52 | 3 | 杀(最优但远) |
| 5 | j2rkJXre | ts_decay_linear(group_rank(ts_mean(S,20),sub),10) | 0.67 | 0.24 | 4.8% | 6.7bp | 1.11 | 0.51 | 3 | 杀 |
| 6 | omgjXvgk | rank(divide(ts_mean(S,20),ts_mean(G,20))) | 0.46 | 0.14 | 8.1% | 2.8bp | 0.37 | 0.25 | 3 | 杀 |
| 7 | A17X5bGW | ts_zscore(divide(ts_mean(S,40),ts_mean(G,40)),120) | 0.55 | 0.16 | 7.5% | 2.8bp | 0.70 | 0.20 | 4 | 杀 |
| 8 | d5RJ6mZw | group_rank(divide(ts_mean(S,20),ts_mean(G,20)),sub) | 0.80 | 0.28 | 8.5% | 3.7bp | 0.30 | 0.34 | 4 | 杀(sharpe最高但2Y崩) |

多样性：外层 5 种(group_rank/signed_power/ts_decay_linear/rank/ts_zscore) ✅ 窗口 20/40/120 ✅ 双字段 3/8 ✅ 算子全部<8 ✅
决策：**全灭——other566 配方不可移植到 model238（课件教训 #3）**。关键：
① **group_rank 微增 sharpe 但摧毁 2Y**——M04#4 rank(ts_mean(S,40))=0.58/2Y1.47 → M05#1 group_rank(...sub)=0.66/2Y1.07（sharpe+0.08 但 2Y-0.40）。group_rank 放大了旧周期信号、压制了近 2 年信号，方向与目标（2Y>1.6）相反。
② **signed_power 凸性温和有效**——#4 sharpe0.77/2Y1.20 为本批最优组合，但仍不及 M04#4 的 2Y1.47。
③ **divide 双字段比不稳定**——#8 sharpe 最高(0.80)但 2Y 崩至 0.30，时序不稳定。
④ **PnL 实现周期极长**（39-93 天，HT_PNL_REALIZATION_HORIZON warning）= 慢信号，收益量级低（1-2%/年）。
⑤ **根因**：model238 字段本身已是 rank 形态（global_screening_rank），对已排序值再套 group_rank 不像 other566（raw 模型分数）那样能提取新的截面信息。
⑥ **3 批 24 表达式天花板确认 ~0.80 sharpe / ~1.47 2Y**，距 1.58/1.6 阈值缺口 0.78/0.13。2Y 缺口虽小但 group_rank 类变换会反向，无明确突破路径。
**model238 降级近失池**（最佳 M04#4: 0.58/2Y1.47/margin7.4bp）。按原计划转 **option40**（option ×1.3 未点亮金字塔，201 字段）。
预算：40/300 ｜ 入围 0/3

### Batch O01 ｜ option40 ｜ TOP3000/STATISTICAL/decay4/trunc0.08/max_trade ON ｜ multisim 3Ljhzi8OS56BarNC4eiev3q

假说：IV 水平/skew/term-structure 广撒网（ivcall/ivput/ivmean/09vhp 已验证字段，反向探测方向）

| # | id | 表达式 | sharpe | fit | tvr | margin | subU | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | e7xMZnpE | rank(ts_mean(ivmean60,20)) | -0.52 | -0.23 | 6.4% | -0.8bp | -0.09 | -1.48 | 3 | 杀 |
| 2 | Grej5nAP | -rank(ts_mean(ivmean60,20)) | 0.52 | 0.23 | 6.4% | 0.8bp | 0.09 | 1.48 | 4 | 杀(反号也不行) |
| 3 | qM62JnrZ | rank(subtract(ts_mean(ivcall90,20),ts_mean(09vhp,20))) | 0.63 | 0.23 | 6.0% | 0.5bp | **0.88✓** | 0.60 | 3 | **线索†(IV-RV subU过!)** |
| 4 | LLdoYnan | -rank(ts_zscore(ivcall150,60)) | -1.49 | -0.69 | 20.3% | -4.3bp | -0.96 | -0.89 | 4 | 杀(反号线索) |
| 5 | QP9RpnkG | rank(subtract(ts_mean(ivput150,20),ts_mean(ivcall150,20))) | -1.27 | -0.62 | 7.1% | -8.5bp | -0.04 | -0.94 | 3 | 杀(put-call反向=skew正向) |
| 6 | 6Xe6LRVG | rank(subtract(ts_mean(ivcall30,20),ts_mean(ivcall150,20))) | -0.75 | -0.30 | 8.5% | -4.6bp | -0.14 | -0.82 | 3 | 杀(term结构反号) |
| 7 | kqZp6nrz | group_rank(ts_mean(ivmean60,20),sub) | -0.42 | -0.13 | 5.7% | -4.3bp | -0.16 | -1.32 | 3 | 杀 |
| 8 | zqR7n51X | ts_decay_linear(rank(subtract(ivput150,ivcall150)),10) | -1.50 | -0.81 | 10.2% | -7.2bp | -0.17 | -1.67 | 3 | **杀(反号=skew正向强信号!)** |

多样性：外层 5 种 ✅ 字段 4 族(ivmean/ivcall/ivput/09vhp) ✅ 窗口 20/60 ✅
决策：**两条关键线索**：①#5/#8 put-call 差强反号 → call-put IV skew（=subtract(ivcall,ivput)）正向预测收益，#8 decay 版反号 sharpe -1.50 即正向 +1.50 起步；②**#3 IV-RV spread（ivcall90−09vhp）subU 0.88 通过**——IV-RV 是 vol risk premium，大盘股同样有效，与 IV skew（小盘集中）经济机制不同。O02 主攻 IV skew 凸性放大 + 对照 zscore level。
预算：48/300 ｜ 入围 0/3

### Batch O02 ｜ option40 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 3msZuI80q4qVaZBhHuTR1rO

假说：IV skew 凸性放大（signed_power³）+ ts_zscore level 对照（O01#8 反号→正向 skew）

| # | id | 表达式 | sharpe | fit | tvr | margin | subU | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | YPg33mzv | ts_decay_linear(rank(subtract(ivcall150,ivput150)),10) | 1.48 | 0.80 | 9.4% | 7.7bp | 0.15✗ | 1.65 | 3 | 近失(subU差) |
| 2 | Grejj6zQ | rank(ts_zscore(ivcall150,60)) | 1.45 | 0.72 | 17.2% | 4.9bp | **0.93✓** | 0.83 | 3 | zscore subU强但2Y弱 |
| 3 | zqR77jGE | signed_power(subtract(rank(zscore(ivcall150,60)),0.5),3) | 1.40 | 0.67 | 19.6% | 4.6bp | 0.85✓ | 0.84 | 3 | 同上 |
| 4 | vRv779GQ | ts_decay_linear(rank(skew),20) | 1.49 | 0.81 | 7.3% | 10.0bp | 0.11✗ | 1.69 | 3 | decay20 margin升 |
| 5 | QP9RRjgX | group_rank(skew,sub) | 1.33 | 0.53 | 17.4% | 3.2bp | -0.08✗ | 2.46 | 3 | group_rank subU崩 |
| 6 | LLdoo6r6 | rank(ts_zscore(ivcall90,60)) | 1.46 | 0.73 | 17.5% | 5.0bp | 0.77✓ | 1.12 | 3 | zscore 90d subU过 |
| 7 | QP9RRjgQ | group_rank(ts_zscore(ivcall150,60),sub) | 1.50 | 0.69 | 16.8% | 4.3bp | 0.74✓ | 1.58 | 2 | subU过但fit低 |
| 8 | Vk3QQE5G | ts_decay_linear(signed_power(subtract(rank(skew),0.5),3),10) | **1.87** | **1.26** | 10.0% | 11.3bp | 0.44✗ | **2.34** | **1** | **⭐凸性突破!仅subU失败** |

多样性：外层 5 种 ✅ 凸性 signed_power³ 首次引入 ✅
决策：**#8 重大突破**——signed_power³ 凸性放大 IV skew：sharpe 1.87/fit 1.26/2Y 2.34/margin 11.3bp，**唯一失败项 = LOW_SUB_UNIVERSE_SHARPE（0.44 vs 0.81）**。zscore level（#2/#6/#7）subU 全过但 sharpe/2Y 不足。**group_rank（#5/#7）摧毁 subUniv skew 信号**。O03 验证凸性稳健性 + 复合尝试修 subU。
预算：56/300 ｜ 入围 0/3（近失池 +Vk3QQE5G）

### Batch O03 ｜ option40 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 1QhtkM6aZ4qCa2E1eyGImaBA

假说：复合 zscore+skew / group_rank 凸性 / decay20 试图修 subU（O02#8 基础上变体）

| # | id | 表达式 | sharpe | fit | tvr | margin | subU | 2Y | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | bld001Em | group_rank(凸性skew,sub)外层 | 1.14 | 0.48 | 10.3% | 4.2bp | -0.25✗ | 1.54 | 4 | 杀(外层group_rank毁) |
| 2 | E5ennPAJ | 凸性(group_rank(skew,sub))内层 | 1.22 | 0.60 | 9.1% | 6.6bp | -0.09✗ | 2.65 | 3 | 杀(内层也毁) |
| 3 | ZYKVVvLj | 凸性(rank(zscore(ivcall150,60))) | 1.35 | 0.78 | 12.5% | 6.8bp | 0.82✓ | 0.61✗ | 3 | zscore凸性subU过2Y崩 |
| 4 | KPEAAMRE | signed_power(group_rank(zscore,sub)−0.5,3) | 1.47 | 0.68 | 17.6% | 4.2bp | 0.69✓ | 1.78 | 2 | 近(2Y过但fit/subU差) |
| 5 | 58kKKdVz | decay(凸性(group_rank(zscore,sub)),10) | 1.40 | 0.74 | 10.6% | 6.6bp | 0.63✓ | 1.65 | 2 | 近(同上) |
| 6 | wpE77kVv | decay(凸性skew,20) | **1.84** | **1.23** | 8.0% | **14.0bp** | 0.41✗ | **2.39** | **1** | **⭐decay20稳健(subU仍卡0.41)** |
| 7 | 78nPPRO8 | rank(subtract(凸性skew, rank(zscore))) | -1.25 | -0.57 | 17.2% | -4.2bp | -0.90✗ | -0.58 | 4 | 杀(复合反号) |
| 8 | E5ennP3J | decay(rank(subtract(zscore,skew)),10) | 1.11 | 0.56 | 11.0% | 5.7bp | 0.82✓ | 0.07✗ | 3 | 杀(复合毁2Y) |

多样性：外层 5 种 ✅ 复合 2 条 ✅
决策：**全灭**——三条结构性教训：①**group_rank（内/外层）均摧毁 skew 凸性 subU**（#1/#2 subU -0.25/-0.09）；②**zscore 凸性 subU 过但 2Y 系统性崩**（#3 2Y0.61, #8 2Y0.07）——zscore 放大旧周期压制近 2 年；③**复合 zscore+skew 全失败**（#7 反号, #8 2Y 崩）。#6（decay20）确认凸性 skew 稳健在 sharpe1.84/fit1.23/2Y2.39/margin14bp，**subU 卡在 0.41 结构性无解**。O04 切 SUBINDUSTRY 中性化 + decay 扫描。
预算：64/300 ｜ 入围 0/3（近失池 +wpE77kVv）

### Batch O04 ｜ option40 ｜ TOP3000/**SUBINDUSTRY**/decay6/trunc0.08/max_trade ON ｜ multisim 16c4m36Pj5a7bzi8RaHYlV3

假说：SUBINDUSTRY 中性化提升 fit/margin + decay 扫描 + tenor 扫描（O02#8/O03#6 配方迁移）

| # | id | 表达式 | sharpe | fit | tvr | margin | subU | 2Y | riskNeut | FailedRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1Yz38opQ | decay(凸性skew,10)@SUB | 1.82 | 1.49 | 8.8% | 19.1bp | 0.40✗ | 2.45 | 1.57 | 1 | 近失(decay10) |
| 2 | LLdovnG6 | decay(凸性skew,20)@SUB | 1.81 | 1.49 | 6.3% | **26.9bp** | 0.38✗ | 2.52 | 1.55 | 1 | 近失(margin最高) |
| 3 | O0xdLnGb | decay(凸性skew,15)@SUB | **1.83** | **1.51** | 7.3% | 23.4bp | 0.38✗ | **2.49** | 1.57 | 1 | **⭐最佳(仅subU失败)** |
| 4 | 3qemKEpe | decay(凸性(rank(zscore)),10)@SUB | 0.87 | 0.51 | 11.7% | 7.3bp | 0.54 | 0.71 | 1.30 | 3 | zscore@SUB崩 |
| 5 | WjVrZNAO | decay(凸性(group_rank(zscore,sub)),10)@SUB | 1.04 | 0.63 | 9.9% | 9.4bp | 0.46 | 1.23 | 1.10 | 3 | group_rank@SUB崩 |
| 6 | le3wn7WN | 凸性skew无decay@SUB | 1.86 | 1.32 | 16.9% | 10.0bp | 0.44✗ | 2.47 | 1.67 | 1 | 近失(tvr高) |
| 7 | 2rNVgvl8 | 凸性skew(ivcall90)@SUB | 1.56 | 1.19 | 9.0% | 16.2bp | 0.27✗ | 2.20 | 1.47 | 2 | 短tenor subU更差 |
| 8 | A17Xpnld | 凸性skew(ivcall30)@SUB | 1.02 | 0.65 | 10.1% | 10.1bp | 0.13✗ | 1.45 | 1.08 | 4 | 最短tenor崩 |

凸性skew = ts_decay_linear(signed_power(subtract(rank(subtract(opt40_ivcall150,opt40_ivput150)),0.5),3),N)
多样性：中性化切换 ✅ decay 10/15/20/无 ✅ tenor 30/90/150 ✅ zscore 对照 2 条 ✅
决策：**SUBINDUSTRY 大幅提升 fit/margin**（STATISTICAL→SUBINDUSTRY：fit 1.26→1.51, margin 11→23bp, returns 3.6→8.5%）但 **subU 不变（0.38-0.44）**。tenor 越短 subU 越差（150→90→30: 0.38→0.27→0.13）。zscore/group_rank 在 SUBINDUSTRY 下更差。**最佳 O0xdLnGb（decay15）sharpe1.83/fit1.51/2Y2.49/margin23.4bp/riskNeut1.57，唯一失败 = LOW_SUB_UNIVERSE_SHARPE（0.38 vs 0.79）**。

**option40 subUniv 根因诊断**：IV skew 信号集中在中小盘——大盘股期权市场更有效、IV skew 预测力弱，导致 TOP1000 子域 sharpe 不足。tenor/decay/中性化/凸性指数均无法修复（4 批 32 表达式验证）。**option40 IV skew 降级近失池**（O0xdLnGb 等待用户手动提交决策）。

近失池（option40 IV skew）：O0xdLnGb(O04#3 最优), 1Yz38opQ(O04#1), LLdovnG6(O04#2), le3wn7WN(O04#6), wpE77kVv(O03#6), Vk3QQE5G(O02#8)
预算：72/300 ｜ 入围 0/3（近失池 6 条，均 FailedRA=1 仅 LOW_SUB_UNIVERSE_SHARPE）

**用户批准 4 条路径（都试一下）**：①接受 O0xdLnGb 为近失候选转新数据集 ②试 option40 其他字段族(delta/gamma/vega/theta 等 201 字段) ③试 TOP1000 universe ④O0xdLnGb 记候选 1，继续找候选 2/3

### Batch O05 ｜ option40 Greeks ｜ TOP3000/SUBINDUSTRY/decay6/trunc0.08/max_trade ON ｜ multisim（路径2）

假说：Greek 字段族（gamma/vega/theta/delta）+ IV-RV spread，凸性结构，找 subUniv 更好的信号

| # | id | 信号族 | sharpe | fit | tvr | margin | subU | 2Y | riskNeut | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | qM62RXaK | IV-RV spread(ivcall90−09vhp)凸性 | 0.62 | 0.32 | 5.7% | 11.8bp | **0.87✓** | 0.87 | 1.25 | 3 | subU过但sharpe太弱 |
| 2 | d5RJGQMw | Gamma skew(call−put)凸性 | -1.62 | -1.18 | 8.5% | -15.5bp | -0.19✗ | -3.13 | -1.59 | 3 | 杀(反号=+1.62但subU仍败) |
| 3 | ZYKVJo8j | Theta skew(call−put)凸性 | -0.85 | -0.64 | 5.9% | -23.8bp | -0.40✗ | -1.02 | -1.13 | 4 | 杀 |
| 4 | 58kKXvmz | Vega skew(call−put)凸性 | -0.09 | -0.02 | 4.4% | -2.3bp | -0.16✗ | -0.06 | -0.61 | 4 | 杀(无信号) |
| 5 | le3wm0n5 | Delta spread(call−put)凸性 | 0.60 | 0.39 | 6.8% | 15.8bp | 0.07✗ | 1.07 | 0.47 | 4 | 杀(margin高但subU败) |
| 6 | qM62RXRK | Gamma level zscore凸性 | 0.17 | 0.05 | 9.6% | 2.6bp | 0.17 | 0.19 | 0.14 | 3 | 杀(无信号) |
| 7 | LLdoQRQe | Theta level zscore凸性 | 0.18 | 0.06 | 9.7% | 2.8bp | 0.07 | 0.23 | 0.22 | 4 | 杀(无信号) |
| 8 | 9q75nRnK | Vega level zscore凸性 | -0.76 | -0.47 | 9.1% | -10.2bp | -0.73✗ | -0.33 | -1.46 | 4 | 杀 |

多样性：字段族 5 种(IV-RV/gamma/theta/vega/delta) ✅ 模式 2 种(skew/level) ✅
决策：**全灭**——三条结论：①**IV-RV spread 是唯一 subU 通过的信号（0.87，印证 O01#3 的 0.88）**但 sharpe 仅 0.62，凸性放大无效（O01#3 无凸性 0.63 ≈ O05#1 凸性 0.62），VRP 信号真实但太弱，距 1.58 缺口 0.96 无突破路径；②**Greek skew 全部小盘集中**（gamma/theta/vega skew subU 全负或接近 0），与 IV skew 同根因——大盘股期权市场有效；③**Greek level（zscore）无预测力**（sharpe 0.17-0.18）。**option40 Greeks 路径终结**，subUniv 结构性问题跨所有期权衍生信号确认无解。
预算：80/300 ｜ 入围 0/3（option40 近失池不变，O0xdLnGb 仍为最优近失候选）

### Batch O06 ｜ option40 IV skew @TOP1000 ｜ TOP1000/SUBINDUSTRY/decay6/trunc0.08/max_trade ON ｜ multisim（路径3）

假说：IV skew 信号直接在 TOP1000（大盘）运行——若大盘仍有效则 sharpe>1.58 且 subU 通过

| # | id | 变体 | sharpe | fit | tvr | margin | subU | 2Y | riskNeut | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | wpE7rkPv | decay15(O0xdLnGb原版) | 0.55 | 0.28 | 8.2% | 7.7bp | 0.30 | 0.57 | 0.89 | 3 | 杀(信号崩塌) |
| 2 | E5endPxJ | decay10 | 0.55 | 0.27 | 10.0% | 6.2bp | 0.28 | 0.47 | 0.90 | 4 | 杀 |
| 3 | 9q75nOkK | decay20 | 0.54 | 0.27 | 7.2% | 8.9bp | 0.30 | 0.64 | 0.87 | 3 | 杀 |
| 4 | KPEA1MZE | 无decay | 0.57 | 0.23 | 20.0% | 3.2bp | 0.26 | 0.55 | 0.95 | 4 | 杀 |
| 5 | 58kKXdYz | 360 tenor | 0.37 | 0.15 | 7.6% | 5.6bp | 0.21 | 0.23 | 0.71 | 3 | 杀(长tenor更弱) |
| 6 | YPg3eoYl | 90 tenor | 0.52 | 0.25 | 9.1% | 6.5bp | 0.13 | 0.61 | 0.78 | 4 | 杀 |
| 7 | bld0w1Am | power² | 0.51 | 0.24 | 7.9% | 6.8bp | 0.27 | 0.48 | 0.85 | 3 | 杀 |
| 8 | A17XA82W | power⁵ | 0.61 | 0.34 | 8.6% | 9.2bp | 0.34 | 0.69 | 0.93 | 3 | 杀(power5略好仍远不足) |

多样性：decay 4 种 ✅ tenor 3 种 ✅ power 3 种 ✅
决策：**决定性诊断**——IV skew 信号在 TOP1000 上 **sharpe 从 1.83 崩塌至 ~0.55**（全线 0.37-0.61），**2Y 全部 <0.7**。这最终证明 IV skew 信号**纯粹是小盘股现象**：大盘股期权市场有效定价、IV skew 无预测力。TOP1000 路径非但没修好 subU，反而让主 sharpe 也崩塌。power⁵（#8）略好（0.61）但仍远低于 1.58。

**option40 全面终结**（6 批 48 表达式）：
- IV skew 凸性（O01-O04）：TOP3000 sharpe1.83 但 subU 0.38 结构性失败
- Greeks（O05）：全灭，subUniv 问题跨所有期权衍生信号
- TOP1000（O06）：信号崩塌至 0.55，确认小盘集中
- **最优近失候选 O0xdLnGb**（sharpe1.83/fit1.51/2Y2.49/margin23.4bp/riskNeut1.57，FailedRA=1 仅 LOW_SUB_UNIVERSE_SHARPE）→ 用户手动决定是否提交
预算：88/300 ｜ 入围 0/3（option40 关闭，转新数据集找候选 2/3）

### Batch R1 ｜ risk60 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 10Sha5lL4Ik91IMv0uTyaA

假说：借券费率反转（低费率→做多，同 shortinterest3）+ crowding 反转 + 凸性放大。字段 offer(α2336)/crowding(α902)/lending_fee_bid_rate(α127)。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | le3woMax | reverse(rank(vec_avg(rsk60_offer))) | 0.87 | 0.47 | 9.9% | 7.3bp | -0.03 | 2.24 | 3 | 线索(offer反转) |
| 2 | GrejZgm3 | rank(ts_mean(offer,10)) | -0.79 | -0.39 | 6.8% | -9.2bp | -0.16 | -2.06 | 3 | 杀(正向失效,反转确证) |
| 3 | akEm5VaO | decay10(reverse(rank(crowding))) | -0.78 | -0.30 | 24.6% | -3.0bp | -0.49 | -1.36 | 4 | 杀(crowding无信号) |
| 4 | mLVnEYa5 | decay15(reverse(rank(offer))) | 0.89 | 0.48 | 9.1% | 8.0bp | 0.02 | 2.19 | 3 | 线索(decay15) |
| 5 | omgjxoa6 | decay15(power³(reverse(rank(offer))−0.5)) | **0.96** | 0.55 | 9.2% | 8.8bp | 0.05 | **2.32** | 3 | **最优(凸性+0.09)** |
| 6 | xAd7J1vl | decay10(power³(reverse(rank(crowding))−0.5)) | 0.01 | 0.0 | 22.4% | 0.05bp | -0.36 | 0.83 | 4 | 杀(crowding凸性无信号) |
| 7 | d5RJNKaJ | reverse(group_rank(offer,sub)) | 0.64 | 0.27 | 9.5% | 4.7bp | 0.06 | 2.34 | 3 | 杀(group_rank毁sh) |
| 8 | rKPaZd03 | decay10(reverse(rank(ts_mean(offer−bid,10)))) | 0.85 | 0.45 | 7.6% | 9.4bp | -0.07 | 2.03 | 3 | 杀(双字段复合弱于单) |

决策：**borrow fee(offer)反转有效**（低费率→做多，同 shortinterest3），sharpe 0.87-0.96。**subU 0.0-0.05 结构性失败**（借券市场大盘有效定价，同 option40/shortinterest3 小盘集中）。2Y 极强 2.24-2.32（信号近期增强）但全期 sharpe 0.96 远不够 1.58，社区均值 0.909(n=786) 印证天花板。crowding 字段弱/反号；group_rank 摧毁；凸性 +0.09。**risk60 降级近失池**（最佳 omgjxoa6: 0.96/2Y2.32）。
预算：96/300 ｜ 入围 0/3（risk60 关闭）

### Batch N1 ｜ news76 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 2gsRZf3Ye4BEaMC11qiw5ouQ

假说：新闻情绪分数(mws76_score)方向/凸性 + confidence 字段 + 离散度(std_dev)广撒网。score α/main field, confidence α/alt。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | O0xL1vMg | reverse(rank(vec_avg(score))) | 0.83 | 0.18 | 45.9% | 0.93bp | 0.69 | 1.32 | 3 | 线索(反转方向) |
| 2 | 3qeKMWPg | rank(vec_avg(score)) | -0.83 | -0.18 | 45.9% | -0.93bp | -0.69 | -1.32 | 4 | 杀(反号确证方向) |
| 3 | P0ORJEzw | decay10(reverse(rank(score))) | 0.57 | 0.12 | 32.0% | 0.92bp | 0.5 | 1.01 | 3 | 杀(decay10降tvr但弱) |
| 4 | Xg83jEzb | decay10(reverse(rank(ts_mean(score,10)))) | 0.01 | 0.0 | 12.2% | 0.06bp | 0.01 | 0.36 | 3 | 杀(过平滑杀信号) |
| 5 | j2rp5QGo | decay15(power³(reverse(rank(score))−0.5)) | 0.69 | 0.16 | 31.9% | 1.1bp | 0.46 | 1.21 | 3 | 线索(power3凸性) |
| 6 | O0xL1vVY | rank(vec_avg(confidence)) | -0.02 | 0.0 | 43.6% | -0.02bp | -0.23 | 0.21 | 4 | 杀(confidence无信号) |
| 7 | 3qeKMW5g | decay15(power³(rank(confidence)−0.5)) | 0.37 | 0.06 | 34.2% | 0.54bp | -0.01 | 0.59 | 4 | 杀(confidence凸性弱) |
| 8 | 0mMVbW68 | decay10(reverse(rank(ts_mean(score,21)))) | -0.02 | 0.0 | 8.2% | -0.14bp | 0.04 | 0.59 | 3 | 杀(21d平滑杀信号) |

决策：**情绪反向定价确证**（high sentiment→short，reverse(rank(score))正确，同 sentiment21）。**subU 优秀(0.69)**！news 情绪跨市值有效，与 option40/risk60 微观结构信号根本不同。**power 凸性是核心放大器**（power3 已见效）。confidence 字段无信号。ts_mean 平滑杀信号（同 sentiment21 教训）。margin 极低(0.93bp)是结构性问题。tvr 45.9% 远超 30%。N2 = decay 扫描(3/5) + power 扫描(5/7) + 离散度对照。
预算：104/300 ｜ 入围 0/3

### Batch N2 ｜ news76 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 37dycVaXN4GE9uJ11WVOVApg

假说：decay 短窗扫描(3/5) + power5 凸性 + 离散度(std_dev)对照。验证 decay 越短信号越强。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WjVZELMQ | decay3(reverse(rank(score))) | 0.72 | 0.16 | 38.4% | 0.95bp | 0.65 | 1.26 | 3 | 线索(decay3提信号) |
| 2 | kqZwxJdL | decay5 | 0.69 | 0.15 | 35.4% | 1.0bp | 0.63 | 1.2 | 3 | 杀 |
| 3 | bldmY8Xq | reverse(rank(ts_mean(score,5))) | 0.4 | 0.08 | 22.3% | 0.9bp | 0.44 | 0.59 | 3 | 杀(ts_mean杀2Y) |
| 4 | omgb1o7E | decay5(power⁵(reverse(rank(score))−0.5)) | **0.99** | 0.26 | 36.4% | 1.35bp | 0.7 | **1.63** | **2** | **线索(power5首过2Y!)** |
| 5 | RR1OJAMz | decay5(reverse(rank(std_dev10))) | 0.64 | 0.21 | 12.7% | 2.15bp | 0.26 | 1.2 | 4 | 杀(离散度弱+subU败) |
| 6 | QP9x1YMp | 反号#5 | -0.64 | -0.21 | 12.7% | -2.15bp | -0.26 | -1.2 | 3 | 杀(反号确认离散度方向) |
| 7 | LLdvP5jL | reverse(group_rank(score,sub)) | 0.39 | 0.07 | 28.5% | 0.66bp | 0.48 | 0.77 | 3 | 杀(group_rank毁,同option40) |
| 8 | rKPq1d3m | decay5(reverse(rank(ts_zscore(score,22)))) | 0.75 | 0.15 | 41.3% | 0.77bp | **0.89** | 0.33 | 3 | 杀(zscore subU强2Y崩,同option40) |

决策：**power5 凸性首过 2Y(1.63)**！sharpe 0.99 为本批最优。decay3 比 decay5 信号更强(0.72 vs 0.69)。**ts_zscore subU 极强(0.89)但 2Y 崩(0.33)**——放大旧周期，同 option40 教训。**group_rank 摧毁信号**（全数据集一致）。离散度(std_dev)弱于方向。N3 = power 扫描(5/7) × decay 扫描(3/5/8) 精修凸性甜点。
预算：112/300 ｜ 入围 0/3

### Batch N3 ｜ news76 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 1n48fi2lQ5bKcHN1hgx5lSwF

假说：power(5/7) × decay(3/5/8) 凸性甜点扫描 + 离散度 power 对照 + 短期均值偏离。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1Yz8YYRM | power5 decay5 | 0.65 | 0.17 | 41.1% | 1.3bp | 0.77 | 0.63 | 3 | 杀(2Y崩) |
| 2 | KPEoPPMj | power7 decay5 | 0.72 | 0.19 | 41.3% | 1.3bp | 0.78 | 0.68 | 3 | 杀 |
| 3 | e7xY77Zg | power5 decay8 | 0.54 | 0.13 | 39.2% | 1.2bp | 0.64 | 0.49 | 3 | 杀 |
| 4 | le3neeP7 | power7 decay8 | 0.59 | 0.14 | 39.5% | 1.2bp | 0.65 | 0.5 | 3 | 杀 |
| 5 | j2rp22Kj | power5 decay3 | 0.68 | 0.17 | 43.6% | 1.3bp | 0.83 | 0.68 | 3 | 杀 |
| 6 | vRvERRXG | std_dev power5 decay5 | 0.13 | 0.02 | 12.2% | 0.8bp | 0.13 | 0.52 | 3 | 杀(离散度power毁) |
| 7 | xAdLAApp | decay5(reverse(rank(score−ts_mean(score,5)))) | 0.76 | 0.14 | 59.4% | 0.7bp | 0.85 | 0.45 | 3 | 杀(tvr爆) |
| 8 | d5RM55JX | power7 无decay | 0.78 | 0.19 | 49.5% | 1.2bp | 0.87 | 0.76 | 3 | 杀(tvr爆) |

决策：**全灭——2Y 全崩(0.5-0.76)**。本批 power5/7 + decay3/5/8 组合 2Y 系统性弱于 N2#4(power5 decay5=1.63)。可能 N2#4 的 1.63 是波动而非稳健甜点。**power 越高 subU 越强但 2Y 越弱**（power7 subU0.78 但 2Y0.68）。N4 = 提 power 到 7-9 + decay5 甜点重测，验证 N2#4 是否可复现。
预算：120/300 ｜ 入围 0/3

### Batch N4 ｜ news76 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 1oRq2q77n4Zn9cFYogN69Sj

假说：power(7/9) + decay(5/8/10/无) 甜点精修，验证 N2#4(power5 decay5 2Y1.63)可复现性。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A17p1GGR | power7 decay5 | **1.07** | 0.29 | 36.3% | 1.5bp | 0.72 | **1.68** | **2** | 强(2Y过!) |
| 2 | 9q7eqppo | power5 decay8 | 0.89 | 0.23 | 34.3% | 1.3bp | 0.58 | 1.46 | 3 | 杀 |
| 3 | Vk3rkGGY | power7 decay8 | 0.95 | 0.25 | 34.4% | 1.4bp | 0.6 | 1.48 | 3 | 杀 |
| 4 | WjVZjAAG | power9 decay5 | **1.09** | 0.3 | 36.1% | 1.6bp | 0.74 | **1.67** | **2** | 强(2Y过) |
| 5 | Xg83gooa | power5 decay10 | 0.83 | 0.21 | 33.5% | 1.2bp | 0.52 | 1.38 | 3 | 杀 |
| 6 | bldmlQQK | power7 decay10 | 0.89 | 0.23 | 33.6% | 1.3bp | 0.54 | 1.41 | 3 | 杀 |
| 7 | E5ej5Gl1 | power9 无decay | 1.09 | 0.28 | 43.0% | 1.4bp | 0.78 | 1.52 | 3 | 杀(tvr超30%) |
| 8 | A17p1GlY | power7 decay3 | **1.12** | 0.3 | 38.6% | 1.5bp | 0.79 | **1.71** | **2** | **强(2Y+subU双过)** |

决策：**power7-9 + decay3-5 是甜点**！3 条 2Y 过线(1.67-1.71)，sharpe 1.07-1.12，subU 0.72-0.79 全过。但 **sharpe 1.07-1.12 距 1.58 缺口 0.46-0.51，fit 0.29-0.30 距 1.0 极远**。margin 1.5bp 距 5bp 缺口大。tvr 36-39% 超 30%。N5 = power 提至 11 + decay1/3 极短窗 + ts_rank 替代 rank 探索 subU 极值。
预算：128/300 ｜ 入围 0/3

### Batch N5 ｜ news76 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON ｜ multisim 3fse6ebr84S6aXFU3o7Vy2K

假说：power11 极端凸性 + decay1/3 极短窗 + ts_rank(22/10) 替代 rank 探 subU 极值。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Vk3rkLo5 | power11 decay3 | **1.13** | 0.32 | 37.7% | 1.6bp | 0.8 | **1.68** | **2** | **⭐最优(2Y+subU双过,sh最高)** |
| 2 | 58km81VX | power9 decay1 | 1.09 | 0.28 | 43.0% | 1.4bp | 0.78 | 1.52 | 3 | 杀(tvr超) |
| 3 | wpEdpA66 | power7 decay1 | 1.11 | 0.28 | 44.2% | 1.3bp | 0.79 | 1.57 | 3 | 杀(2Y差0.03) |
| 4 | 2rNgrxEZ | ts_rank22 power7 decay3 | 1.08 | 0.25 | 45.4% | 1.1bp | **0.98** | 1.34 | 3 | 杀(subU极强2Y弱) |
| 5 | zqRxqEaO | ts_rank22 power9 decay3 | 1.13 | 0.27 | 44.8% | 1.2bp | **0.99** | 1.42 | 3 | 杀(subU0.99但2Y/tvr差) |
| 6 | E5ej5M3G | ts_rank10 power7 decay3 | 0.9 | 0.18 | 49.7% | 0.8bp | 0.9 | 1.2 | 3 | 杀 |
| 7 | 9q7eq3ox | power11 decay1 | 1.06 | 0.28 | 42.0% | 1.4bp | 0.77 | 1.46 | 3 | 杀 |
| 8 | A17p156e | ts_rank10 power9 decay3 | 0.91 | 0.19 | 48.6% | 0.9bp | 0.88 | 1.28 | 3 | 杀 |

决策：**Vk3rkLo5(power11 decay3)为 news76 最优**：sharpe1.13/fit0.32/tvr37.7%/margin1.6bp/subU0.80/2Y1.68，FailedRA=2(LOW_SHARPE+LOW_FITNESS)。**power 凸性进展：power3(0.69)→5(0.99)→7(1.12)→11(1.13)，7-11 为甜点**。**ts_rank subU 极强(0.98-0.99)但 2Y/换手不可用**（同 option40 ts_zscore 教训：时序标准化放大旧周期）。**news76 天花板 ~1.13 确认**（5 批 40 表达式平台化），sharpe 距 1.58 缺口 0.45，fit 距 1.0 缺口 0.68，margin 距 5bp 缺口 3.4bp，tvr 37.7% 超 30%。**news76 降级近失池**（Vk3rkLo5 等待用户手动决策）。

**news76 跨数据集关键发现**：①情绪反向定价(high sentiment→short)，reverse(rank(score))正确 ②subU 优秀(0.70-0.99)，news 情绪跨市值有效，与 option40/risk60 微观结构信号根本不同 ③power 凸性是核心放大器(power7-11 甜点) ④decay 越短信号越强但 tvr 越高，核心矛盾 ⑤SUBINDUSTRY 摧毁 news76 信号(与 option40 相反!)，STATISTICAL 是正确中性化 ⑥ts_rank/ts_zscore subU 强但 2Y 系统性崩 ⑦group_rank 跨数据集一致摧毁信号 ⑧margin 极低(1.6bp)是结构性问题 ⑨confidence 字段无信号。
预算：136/300 ｜ 入围 0/3（news76 关闭，近失池 +Vk3rkLo5）

---

## 近失候选池汇总（mthyzx 会话，batch 1-17）

| 候选 | alpha_id | 数据集/风格 | sh | fit | tvr | margin | 2Y | subU | riskNeut | RAfail | 缺口 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | O0xdLnGb | option40/IV skew凸性 | 1.83 | 1.51 | 7.3% | 23.4bp | 2.49 | 0.38 | 1.57 | 1(仅subU) | subU 0.38 vs 0.79 |
| 2 | Vk3rkLo5 | news76/新闻情绪反转凸性 | 1.13 | 0.32 | 37.7% | 1.6bp | 1.68 | 0.80 | — | 2(sh+fit) | sh/fit/margin/tvr |
| 3 | 待找 | analyst类目(×1.3未点亮) | — | — | — | — | — | — | — | — | — |

待找候选3从 analyst 类目（mthyzx 未试过，×1.3 未点亮金字塔）。前序本会话已试过 analyst39（天花板 1.07, FAST 中性化, EPS 收益率 divide(qepsinclxo,spvbq)）。可试 analyst39+凸性配方(power7/11)，或试新 analyst 数据集。

---

# 续章 — MT38799 会话 ｜ 三 alpha 挖掘（alpha1/2/3 定型 + b87-b90 收尾）

日期: 2026-08-01 ｜ 账号: MT38799 (GOLD) ｜ 目标: 3 个不同数据集 alpha，互相关<0.4，点亮未点亮金字塔

## 三 alpha 终态（不变）

| alpha | id | 数据集 | 金字塔 | 状态 | sh | fit | 2Y | subU | tvr | margin | prod_corr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alpha2 | xAdL5vmN | ai_equity_alpha | MODEL×1.4 | ✅**唯一可提交** | 4.51 | 4.13 | 3.65 | 1.96 | 6.1% | 34.6bp | 0.6697 |
| alpha3 | GreR6x2J | other566 | OTHER×1.5 | ❌DISQUALIFIED | 1.92 | — | — | — | — | — | 0.7447>0.7 |
| alpha1 | 6XeWqEE7 | option40 | OPTION | ❌DISQUALIFIED | 2.28 | — | — | — | — | — | >0.7 |

**alpha2 表达式**（proven 模板）: `ts_decay_linear(signed_power(subtract(group_rank(vec_avg(historic_earnings_surprise_score), subindustry), 0.5), 5), 90)` + SLOW_AND_FAST + trunc0.08 + decay6 + max_trade ON + nan_handling ON。**凸性放大(power5 + centered subtract 0.5)是关键**。properties 已设。

## Batch b87 ｜ model227 ｜ DEAD END（8/8 灭）

假说：EMI(earnings momentum)是动量衍生，可能补 alpha2 缺口。5 个 fact_predict(EMI 字段) + 3 个基本面比率(ROE/ROIC/op_margin)，proven 模板 power3。

| # | id | 字段 | sh | 2Y | 判定 |
|---|---|---|---|---|---|
| 1 | 88ewQ81X | op_margin | 0.24 | — | 杀 |
| 2 | 9q7nrq0x | ROIC | 0.71 | — | 杀 |
| 3 | 78np189x | ROE | 0.96 | 1.91 | 最佳但 sh 远低 |
| 4 | np8E2pVw | predict_8 subind p5 | -0.48 | — | 杀 |
| 5 | N1RZr19w | predict_2 subind p3 | 0.84 | — | 杀 |
| 6 | WjV5Gj6Z | predict_1 | -0.13 | — | 杀 |
| 7 | 3qeNRqZP | predict_8 sector | -0.59 | — | 杀 |
| 8 | QP98VPLQ | predict_8 subind p3 | -0.60 | — | 杀 |

决策：**EMI = 动量衍生，被 SLOW_AND_FAST 中性化剥离**。ROE 最佳 sh0.96/2Y1.91 但 sh 距 1.58 缺口 0.62。model227 关闭。

## Batch b88 ｜ model239 ｜ DEAD END（8/8 灭） ｜ multisim 3vRf0D3Ev4XuaQ21b8t3pX5A

假说：做空信号(shortlasso1d/30d/92d) + 借贷(utilisation/loanrate1)，proven 模板 power3 + 1 个 reverse。

| # | id | 字段 | sh | 2Y | 判定 |
|---|---|---|---|---|---|
| 1 | j2r7rZNW | shortlasso1d subind | 0.84 | — | 杀 |
| 2 | vRvQvLav | shortlasso1d sector | 0.88 | -0.61 | 最佳但近期恶化 |
| 3 | QP989amW | shortlasso30d | 0.80 | — | 杀 |
| 4 | 6XekewgL | shortlasso92d | 0.83 | — | 杀 |
| 5 | le3m3V6O | reverse | -1.34 | -0.51 | 灾难 |
| 6 | zqRVR9wO | combo_utilisation | 0.45 | -0.70 | 杀 |
| 7 | A17A7wJe | combo_loanrate1 | 0.12 | -0.18 | 杀 |
| 8 | 1YzMz7VM | combo_utilisation_x_rate | 0.26 | -0.75 | 杀 |

决策：**做空信号被 SLOW_AND_FAST 剥离**（shortlasso 是市场已定价的做空预期）。reverse sh-1.34 灾难。shortlasso1d sector sh0.88 但 2Y-0.61 近期恶化。model239 关闭。

## Batch b89 ｜ news46 ｜ DEAD END（8/8 灭）

假说：RavenPack 新闻情绪(mean_ssc/nip/ess/relevance + sum_ssc/story_count)，ts_mean 版 power3。

| # | id | 字段 | sh | 2Y | subU | 判定 |
|---|---|---|---|---|---|---|
| 1 | A17AlwEd | mean_ssc subind | 0.50 | 0.19 | 0.21 | 杀 |
| 2 | 9q7nXwk9 | mean_ssc sector | 0.38 | 0.02 | 0.12 | 杀 |
| 3 | gJ92j1LQ | mean_nip5d subind | 0.97 | 1.08 | 0.30 | **最佳** |
| 4 | Jjv97prW | mean_ess5d subind | 0.87 | -0.53 | 0.71 | 杀(2Y崩) |
| 5 | le3mjV1N | mean_relevance | 0.23 | 0.49 | -0.10 | 杀 |
| 6 | A17Alw2d | sum_ssc subind | 0.75 | 0.48 | 1.05 | subU强 |
| 7 | RR1g7pva | sum_story_count20d subind | 0.82 | 0.64 | 0.72 | 杀 |
| 8 | omgdqKkl | mean_nip10d sector | 0.79 | 1.57 | 0.17 | 2Y近门槛 |

决策：**nip5d subind sh0.97/2Y1.08 最强**（power3 无 center）。nip10d sector sh0.79/2Y1.57 近 1.6 门槛。sum_ssc subU1.05 强。但全部 sh<1.0，距 1.58 缺口 ≥0.58。news46 power3 天花板 ~0.97。

## Batch b90 ｜ news46 + alpha2 凸性风格 ｜ DEAD END（sims 未创建）

假说：b89 nip5d subind sh0.97(power3 无 center)，改用 alpha2 凸性模板 `subtract(group_rank(FIELD,group),0.5)` + power5（centered + 更强凸性放大 extremes），可能 push sh 过 1.58。8 表达式：nip(5d/10d/3d/20d × subindustry/sector) + sum_ssc + sum_story_count。

**结果：create_multi_simulation 返回 REQUEST_TIMEOUT。get_user_alphas(order=-dateCreated, limit=12) 验证：最新 12 alpha 全是 b89(8, power3) + b88(4, power3)，无任何 b90 凸性模板(subtract+power5)alpha。结论：timeout = 请求被拒，sims 从未在 BRAIN 创建。** args 存 args_news46_b90.json，结果存 result_news46_b90.json。

## 最终结论

**三 alpha 目标仅 1/3 达成**：仅 alpha2 (xAdL5vmN, ai_equity_alpha) 可提交（prod_corr=0.6697<0.7，properties 已设）。alpha1/alpha3 均 prod_corr>0.7 DISQUALIFIED。

**核心 Pattern（SLOW_AND_FAST 中性化剥离）**：在 alpha2 的 SLOW_AND_FAST + trunc0.08 + decay6 + max_trade ON 配方下，**所有非 alpha2/alpha3 数据集 sharpe 上限 ~0.5-1.0**。剥离机制：
- 动量衍生信号（model227 EMI）→ 被剥离
- 做空/借贷信号（model239 shortlasso/utilisation/loanrate）→ 被剥离
- 新闻情绪（news46 nip/ess/ssc，b89 power3 天花板 0.97；b90 凸性未跑成）
- 期权微观结构（option40 subU 失败 + prod_corr>0.7）
- other566（prod_corr>0.7）

**累计已排除数据集天花板**：other571/model38/sentiment21,22/analyst39,consensus/news76/shortinterest3/insiders3/macro38/fundamental91/risk65/model238/option40/other566/model227/model239/news46。

**近失池（等待用户手动决策）**：
1. alpha2 (xAdL5vmN) — ✅可提交，prod_corr=0.6697
2. O0xdLnGb (option40 IV skew 凸性) — sh1.83/fit1.51/2Y2.49 但 subU0.38 vs 0.79（仅 subU 失败）
3. Vk3rkLo5 (news76 新闻情绪反转凸性) — sh1.13/2Y1.68/subU0.80 但 sh/fit/margin/tvr 差
4. news46 b89 gJ92j1LQ (nip5d subind) — sh0.97/2Y1.08，power3 无凸性
5. news46 b89 omgdqKkl (nip10d sector) — sh0.79/2Y1.57，2Y 近门槛

**预算**：本轮 b87-b90 共 32 sims（b90 实际 0 sims 创建），累计 ~302/300（略超）。**停止挖掘**，等待用户手动提交 alpha2 或指示下一步。

---

## analyst_consensus 探索（mthyzx 会话，batch 18-20）

### 数据集选择
get_datasets(search=analyst) 筛选 valueScore≥4 + cov≥0.6 + 低 alphaCount（未充分挖掘）：
- **analyst_consensus**（选中）：cov 0.7733, 3424 fields, valueScore 5.0, 仅 61 alphas（最未挖掘）
- analyst_factor_signals: cov 0.66, 922 fields, valueScore 5.0, 125 alphas
- analyst10 (StarMine SmartEstimate): cov 0.8069, 2258 fields, valueScore 3.0, 3373 alphas（crowded）

选定 2 字段（EPS 修正动量信号）：
- `mean_estimate_eps_annual12_3`（当前 EPS 一致预期 mean, cov 0.9779）
- `mean_estimate_four_weeks_prior_eps_annual12_3`（4 周前 EPS, cov 0.9699）

### Batch 18 ｜ analyst_consensus b1 ｜ TOP3000/STATISTICAL/decay6/trunc0.08/max_trade ON
8 表达式：方向(动量4+反向3)×凸性(power7/9/11)×decay(3/6)，base=rank(subtract(eps_now, eps_4wk))
**结果：8/8 全失败** — "Operator subtract does not support event inputs"。analyst_consensus 字段为 VECTOR/event 类型（同 news76），必须用 vec_avg() 转 scalar。批次废弃（预算 -8）。

### Batch 19 ｜ analyst_consensus b2 ｜ STATISTICAL ｜ multisim 3ONrE09mG4W4c55W9qe6Zky
修正：所有 EPS 字段用 vec_avg() 包裹。8 表达式同 b1 设计。

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RR1OMX61 | 动量 power7 decay3 | 0.7 | 0.27 | 6.3% | 5.8bp | 0.31 | 0.05 | 3 | 弱 |
| 2 | P0ORNegK | 动量 power11 decay3 | 0.6 | 0.23 | 6.7% | 5.2bp | 0.32 | -0.03 | 3 | 杀 |
| 3 | JjvAqlQA | 动量 power7 decay6 | **0.71** | 0.27 | 6.1% | 6.1bp | 0.34 | 0.01 | 3 | b2最优(STATISTICAL) |
| 4 | kqZwdRJd | 动量 power9 decay3 | 0.65 | 0.25 | 6.5% | 5.5bp | 0.31 | -0.01 | 3 | 杀 |
| 5 | 2rNgMEjP | 反向 power7 decay3 | -0.52 | -0.15 | 5.0% | -4.0bp | -0.37 | -0.09 | 4 | 杀(方向反) |
| 6 | zqRxZaro | 反向 power11 decay3 | -0.54 | -0.16 | 5.1% | -4.4bp | -0.31 | -0.39 | 4 | 杀 |
| 7 | xAdLqM1N | 动量 power11 decay6 | 0.62 | 0.23 | 6.6% | 5.5bp | 0.35 | -0.06 | 3 | 杀 |
| 8 | ZYK86ZmQ | 反向 power9 decay3 | -0.53 | -0.15 | 5.0% | -4.2bp | -0.34 | -0.25 | 4 | 杀 |

**b2 关键发现**：
①**方向确认=动量**（反向全负 -0.52~-0.54），analyst EPS 修正是基本面漂移，**与 news76 情绪反向相反**（教训⑦不适用 analyst）
②**凸性反向**：power7(0.70)>power9(0.65)>power11(0.60)，高 power 在 analyst 损害（噪声放大，与 news76/option40 凸性甜点相反）
③STATISTICAL 天花板 0.71，2Y 灾难 0.01-0.05（信号近 2 年失效）
④margin 5.2-6.1bp✓ / tvr 5-6.7%✓ 过线，但 sh/fit/2Y/subU 全差

### Batch 20 ｜ analyst_consensus b3 ｜ FAST ｜ 多样性评估里程碑
假说：FAST 中性化是 analyst 放大器（教训⑨，prior analyst39 用 FAST 达 1.07）+ 低/无凸性（b2 证伪高 power）+ estimate_count 注意力信号替代。8 表达式：

| # | id | 表达式 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6XeW7N1p | EPS修正 纯rank decay6 | 0.78 | 0.32 | 6.1% | 7.1bp | 0.53 | 0.54 | 3 | 强(FAST放大) |
| 2 | Xg83GMLz | EPS修正 纯rank decay3 | 0.79 | 0.33 | 6.2% | 6.9bp | 0.54 | 0.54 | 3 | 强 |
| 3 | qM6a8VzK | EPS修正 power3 decay6 | **0.80** | 0.36 | 6.8% | 7.6bp | 0.47 | 0.65 | 3 | **⭐analyst最优(FAST)** |
| 4 | xAdLq5zw | EPS修正 power5 decay6 | 0.78 | 0.36 | 7.3% | 7.3bp | 0.45 | 0.66 | 3 | 强 |
| 5 | E5ej1xaK | est_count 动量 rank decay6 | -0.16 | -0.03 | 7.0% | -1.2bp | 0.03 | -1.16 | 3 | 杀(信号死) |
| 6 | QP9xM6lK | est_count 动量 power7 decay3 | -0.25 | -0.07 | 10.6% | -1.9bp | -0.06 | -0.96 | 3 | 杀 |
| 7 | gJ9l6LPg | est_count 反向 rank decay6 | 0.16 | 0.03 | 7.0% | 1.2bp | -0.03 | 1.16 | 4 | 杀(sh差2Y有趣) |
| 8 | 58kmxY61 | EPS修正 纯rank decay10 | 0.78 | 0.32 | 6.0% | 7.3bp | 0.51 | 0.55 | 3 | 强 |

**b3 关键发现**：
①**FAST 是 analyst 放大器**（教训⑨确认）：sh 0.71→0.80，2Y 0.01→0.65（+0.64！），subU 0.34→0.53，margin 6.1→7.6bp，fit 0.27→0.36。FAST 全指标提升，尤以 2Y 恢复最关键。
②**estimate_count 注意力信号死亡**（sh -0.25~0.16），EPS 修正是唯一有效 analyst 信号
③**低/无凸性最优**：power3(0.80)≈power5(0.78)≈纯rank(0.78-0.79)，高 power 损害 analyst（与 news76/option40 凸性甜点 power7-11 相反——analyst 信号本身已含噪声，凸性放大噪声）
④**analyst 天花板确认 ~0.80**（FAST+EPS修正），距 1.58 缺口 0.78。2Y 0.65 距 1.6 缺口 0.95。subU 0.47 距 0.79 缺口 0.32。margin/tvr 过线。
⑤analyst 降级近失池（qM6a8VzK 等待用户手动决策）

**analyst 跨数据集关键发现**：①方向=动量（基本面漂移，非情绪反向，与 news76 相反）②FAST 是关键放大器（2Y 从 0→0.65）③凸性反向（低 power 优，analyst 信号已含噪声）④estimate_count 注意力无信号 ⑤USA analyst 信号天花板 ~0.8-1.07（well-arbed 流动市场）⑥VECTOR 字段须 vec_avg()（同 news76）

预算：160/300 ｜ 入围 0/3（analyst 关闭，近失池 +qM6a8VzK）

---

## 多样性评估（batch 20 里程碑）｜ 3 近失候选互相关

compute_mutual_correlation（years=4, threshold=0.4, num_points=986）：

| 配对 | 相关系数 | 判定 |
|---|---|---|
| O0xdLnGb(option40) ↔ Vk3rkLo5(news76) | 0.1417 | ✓<0.4 |
| O0xdLnGb(option40) ↔ qM6a8VzK(analyst) | 0.1701 | ✓<0.4 |
| Vk3rkLo5(news76) ↔ qM6a8VzK(analyst) | 0.1334 | ✓<0.4 |

**all_below_threshold=true**，max_pair=0.1701。3 候选跨 3 类目（option×1.3/news×1.2/analyst×1.3）×3 信号类型（IV skew凸性/新闻情绪反转凸性/EPS修正动量）×3 中性化（SUBINDUSTRY/STATISTICAL/FAST），多样性优秀。

## 近失候选池最终汇总（mthyzx 会话，batch 1-20）

| 候选 | alpha_id | 数据集/风格 | sh | fit | tvr | margin | 2Y | subU | riskNeut | RAfail | 缺口 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | O0xdLnGb | option40/IV skew凸性 | 1.83 | 1.51 | 7.3% | 23.4bp | 2.49 | 0.38 | 1.57 | 1(仅subU) | subU 0.38 vs 0.79 |
| 2 | Vk3rkLo5 | news76/新闻情绪反转凸性 | 1.13 | 0.32 | 37.7% | 1.6bp | 1.68 | 0.80 | — | 2(sh+fit) | sh/fit/margin/tvr |
| 3 | qM6a8VzK | analyst_consensus/EPS修正动量FAST | 0.80 | 0.36 | 6.8% | 7.6bp | 0.65 | 0.47 | — | 3(sh+fit+2Y) | sh/fit/2Y/subU |

**结论**：3 候选互相关 0.13-0.17（远<0.4），多样性达标。但 3 个均未过完整门槛（仅 O0xdLnGb 接近，仅 subU 失败）。analyst 类目天花板 ~0.80（FAST+EPS修正），低于 prior analyst39 的 1.07。**待用户手动决策**：①接受 3 近失候选（O0xdLnGb 最接近）②试 analyst10(StarMine SmartEstimate)突破 ③试其他未点亮类目（sentiment×1.5/model×1.4/option×1.3/risk×1.2/news×1.2 已降级, analyst×1.3 已降级）。生产 corr 未出或>0.7 不提交（用户手动）。

## other566 二轮深挖（会话 3，batch b80-b84）｜ 点亮 USA/D1/OTHER 新金字塔

背景：前序会话确认 other566 是甜点区数据集（count=791, Sharpe=0.799），首轮（Batch 14-22）已产出入围 alpha 3qePVw3Z（sh1.74/fit1.04）但 ProdCorr 拒。本轮目标：用 1-2 字段 + 简单结构找 ra_failed=0 的 other566 alpha 点亮新金字塔 USA/D1/OTHER（multiplier=1.5）。约束：sharpe>1.58, fitness>1, 2Y>1.6, margin>5bp, turnover 5-30%, ops<8, ra_failed=0。详见 result_other566_b80~b84.json。

### Batch b80 ｜ other566 ｜ TOP3000/SLOW_AND_FAST/subindustry/P5/D90/mean10 ｜ 4字段
假说：SLOW_AND_FAST 中性化 + subindustry group_rank + signed_power(P5) + ts_decay_linear(D90) + ts_mean(10) 平滑，4 字段扫描
结果：最佳 l2r20_label sh=1.21（未达标，平滑+subindustry 组合下 sharpe 偏低）
结论：mean10 平滑 + subindustry 分组限制了 sharpe 上限，需去平滑/换分组

### Batch b81 ｜ other566 ｜ STATISTICAL 中性化 ｜ 8种P/D/mean 组合
假说：换 STATISTICAL 中性化是否提升
结果：最佳 sh=0.97（比 SLOW_AND_FAST 更差）
结论：STATISTICAL 对 other566 标签信号不适用，SLOW_AND_FAST 确认更优

### Batch b82 ｜ other566 ｜ SLOW_AND_FAST + 8 新字段扫描
假说：换字段突破 l2r20_label 的 sh 上限
结果：最佳 r20marsi_ret sh=0.98（无超 l2r20_label 的 b80 sh=1.21）
结论：l2r20_label 仍是 other566 最强字段，换字段无效

### Batch b83 ｜ other566 ｜ SLOW_AND_FAST + trunc0.04 + 结构变化 ｜ 突破
假说：加 trunc0.04（限制极值权重）+ 切 sector/market 分组 + 去 ts_mean 平滑
结果：sector P5 sh=1.42, subindustry P3 sh=1.45（首次突破 1.4）
结论：**trunc0.04 + 去平滑（raw）是关键突破**——raw 字段 > mean10；sector 接近 subindustry

### Batch b84 ｜ other566 ｜ SLOW_AND_FAST + trunc0.04 + P3/sector 组合 ｜ ⭐全达标命中
假说：b83 突破后，固定 sector + P3 + raw，扫描分组/power/mean 确认最优 ｜ multisim 3Shbv11tU4Bi9wgjAqzk26Q

| # | id | 结构 | sharpe | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6Xek1JLJ | sector_P3_mean10 | 1.56 | 0.77 | 8.1% | 7.6bp | 0.86 | 2.15 | 2(sh+fit) | 杀(mean10毁fit) |
| 2 | 78npQMPQ | industry_P3_mean10 | 1.58 | 0.78 | 8.0% | 7.7bp | 0.85 | 1.94 | 1(fit) | 杀(industry略逊) |
| 3 | Vk3WE5QM | market_P3_mean10 | 1.43 | 0.68 | 8.1% | 7.0bp | 0.75 | 1.96 | 2(sh+fit) | 杀(market更差) |
| 4 | **GreR6x2J** | **sector_P3_raw** | **1.92** | **1.13** | 9.3% | 9.4bp | 0.98 | **2.55** | **0** | **⭐全达标** |
| 5 | LLdQ6rv1 | sector_P1_mean10 | 1.75 | 0.96 | 8.5% | 8.8bp | 0.91 | 2.54 | 1(fit) | 近(P1 fit差0.04) |
| 6 | gJ92Kd2J | sector_P2_mean10 | 1.66 | 0.86 | 8.2% | 8.2bp | 0.88 | 2.36 | 1(fit) | 杀(P2弱) |
| 7 | j2r7Xx7Z | sector_P3_mean5 | 1.74 | 0.93 | 8.7% | 8.2bp | 0.96 | 2.29 | 1(fit) | 近(mean5略好仍fit差) |
| 8 | xAdZQWZW | sector_P3_mean20 | 1.24 | 0.54 | 7.2% | 6.6bp | 0.70 | 1.76 | 2(sh+fit) | 杀(mean20毁) |

多样性：分组 4 种(sector/industry/market/subindustry) ✅ power 3 种(P1/P2/P3) ✅ 平滑 4 种(raw/mean5/mean10/mean20) ✅
决策：**#4 GreR6x2J 全达标**——code=`ts_decay_linear(signed_power(group_rank(oth566_l2r20_label, sector), 3), 90)`，sh1.92/fit1.13/2Y2.55/subU0.98/tvr9.31%/margin9.35bp/ra_failed=0，点亮新金字塔 USA/D1/OTHER（multiplier=1.5）。

**关键发现（b80-b84 五批 40 表达式）**：
- **raw 字段（无 ts_mean）> mean10/mean5/mean20**——#4 raw sh1.92 vs #1 mean10 sh1.56，平滑系统性降低 fit（mean10 fit0.77 vs raw fit1.13）
- **sector > industry > market > subindustry**（b83-b84: sector P3 raw sh1.92 为最优组合）
- **P3 > P5 > P7 > P11 > P15**（b84: P3 fit1.13 唯一过 1.0；P1 fit0.96 差 0.04）
- **trunc0.04 是突破关键**（b80-b82 无 trunc，sh 上限 1.21；b83-b84 加 trunc0.04 后突破 1.92）
- **SLOW_AND_FAST > STATISTICAL**（b81: STATISTICAL 最佳 0.97，明显更差）

### GreR6x2J 稳健性审计（brain-alpha-robustness skill）

**Phase B Attribution**：
- get_alpha_details: UNSUBMITTED/IS, USA/TOP3000/D1/SLOW_AND_FAST/trunc0.04/decay6, sh1.92/fit1.13/2Y2.55/subU0.98/tvr9.31%/margin9.35bp, failed_ra=0, failed_ppa=0, pyramid=USA/D1/OTHER(×1.5)
- get_alpha_yearly_stats（recent-3yr regime 2021-2023 PRIMARY，按 2026-06-20 用户指令）：
  - 2021 sh=3.08, 2022 sh=2.61, 2023 sh=2.56（全正且>0.3，min 2.56≥2Y bar 1.6）✓
  - Decay ratio = 2.56/1.92 = 1.33（≥0.50，信号增强未衰减）✓
  - Recent-3yr CV = 0.085（<0.40，极稳定）✓
  - Recent-3yr max/min = 1.20（≤3）✓
  - Recent-3yr flat years = 0 ✓
  - 历史soft-flag（非reject）: 2020 sh=-1.65（COVID regime）, 2019 sh=0.64, 2016 sh=1.05
- check_self_correlation: max=0.39（vs do61Ynv）<0.7 ✓，pool_size=124

**Phase C Anti-overfit Gate**：

| 检查 | 结果 | 判定 |
|---|---|---|
| WebDataScope failed count | failed_ra=0, failed_ppa=0 | PASS |
| Recent-3yr Sharpe (PRIMARY) | min 2.56≥1.6, 全>0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.085<0.40 | PASS |
| Decay ratio | 1.33≥0.50 | PASS |
| Recent-3yr flat years | 0 | PASS |
| Recent-3yr max/min | 1.20≤3 | PASS |
| Full-history old-year softness | 2020 sh=-1.65 | soft-flag（非reject） |
| Sub-universe Sharpe | 0.98（差0.02） | CONDITIONAL |
| Operator count | 3≤5 | PASS |
| Margin @ turnover | 9.35bp@9.31% | PASS |
| Self correlation | max 0.39<0.7 | PASS |
| Economic interpretability | sector相对标签排名+尾部增强+90天衰减 | PASS |

**决策：PASS（with soft-flags）** → set_alpha_properties 完成（name=0.3906, color=GREEN, tags已设）。subU 0.98 的 CONDITIONAL 与已确认 alpha1（subU 0.99）等同，且 OS 生存关键指标（recent-3yr sharpe/decay/CV）全部强 PASS。不提交——prod_corr 待用户手动检查。

### 三 alpha 候选篮子互相关（compute_mutual_correlation, 4年986点）

| 对 | 相关性 | 判定 |
|---|---|---|
| GreR6x2J(alpha3/other566) ↔ 6XeWqEE7(alpha1/option40) | 0.0623 | ✓<0.4 |
| GreR6x2J(alpha3/other566) ↔ xAdL5vmN(alpha2/ai_equity_alpha) | 0.1248 | ✓<0.4 |
| 6XeWqEE7(alpha1/option40) ↔ xAdL5vmN(alpha2/ai_equity_alpha) | 0.1124 | ✓<0.4 |

**all_below_0.4=true**。三 alpha 跨 3 数据集（other566/option40/ai_equity_alpha）×3 金字塔（OTHER×1.5/未确认/MODEL×1.4）×3 风格（sector标签凸性/IV skew凸性/subindustry盈余惊喜凸性），多样性优秀。

### 三 alpha 候选篮子最终状态

| # | alpha_id | 数据集/风格 | sh | fit | 2Y | subU | tvr | margin | RAfail | 金字塔 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6XeWqEE7 | option40/IV skew凸性 | 2.28 | 2.10 | 3.37 | 0.99 | 8.3% | 25.4bp | 0 | STATISTICAL | 候选（prod_corr>0.7不可提交） |
| 2 | xAdL5vmN | ai_equity_alpha/盈余惊喜凸性 | 4.51 | 4.13 | 3.65 | 1.96 | 6.1% | 34.6bp | 0 | MODEL×1.4 | ✅已设属性 |
| 3 | GreR6x2J | other566/sector标签凸性 | 1.92 | 1.13 | 2.55 | 0.98 | 9.3% | 9.4bp | 0 | OTHER×1.5 | ✅已设属性 |

**结论**：3 alpha 互相关全<0.4，alpha2/alpha3 已设属性待 prod_corr 用户手动检查后提交，alpha1 prod_corr>0.7 不可提交但作候选保留。alpha3（GreR6x2J）点亮新金字塔 USA/D1/OTHER（×1.5）。预算：~270/300 已用。

---

## 续章：替换 alpha1 的搜索 + alpha3 prod_corr 重验（2026-08-01 续）

背景：alpha1（6XeWqEE7/option40）prod_corr>0.7 不可提交，需在未点亮金字塔数据集找替换。WebDataScope 甜点区=other566+option40 均已用/失败，转向最后的高先验 contingency 数据集。

### ⚠️ alpha3 (GreR6x2J) prod_corr 重验 → DISQUALIFIED

check_correlation（此前返回 null/pending，本轮重验平台已算完）：
- **production max_correlation = 0.7447 > 0.7 → passes_check=false → DISQUALIFIED**
- 直方图：池内仅 2 个 alpha 在 0.7-0.8 区间，1 个 0.6-0.7（边界），其余 99.99% <0.5
- **状态变更**：alpha3 从"待验"变为"不可提交"。现在 **alpha1 + alpha3 均 prod_corr>0.7 失格**，仅 alpha2（xAdL5vmN, prod_corr=0.6697✓）可提交。需找 2 个替换（原计划仅需 1 个）。

### Batch b85 ｜ macro38（技术评级）｜ TOP3000/SLOW_AND_FAST/trunc0.04/decay6 ｜ multisim 4vQVqU93G4xmbGjzX8GZwQT

假说：技术评级（direction/strength/overall_percent/shortterm/longterm）经 proven 模板（sector+P3+D90+SLOW_AND_FAST）放大。macro 金字塔 ×1.1 未点亮。

| # | id | 表达式（核心） | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | (b85#1) | mcr38_overall_percent sector P3 D90 | — | — | — | — | — | — | — | 杀 |
| 2 | RR1g2Jxe | mcr38_direction_rating sector P3 D90 | **0.53** | 0.18 | 10.67% | 2.84bp | 0.45 | **0.94** | 3 | **最佳但仍远** |
| 3 | gJ92RYNl | mcr38_strength_rating sector P3 D90 | 0.39 | 0.11 | 8.2% | 2.31bp | 0.19 | 0.67 | 3 | 杀 |
| 4 | N1RZgXdo | mcr38_shorttermpercent sector P3 D90 | 0.31 | 0.08 | 9.79% | 1.64bp | 0.19 | 0.62 | 3 | 杀 |
| 5 | qM6RPKaA | mcr38_overall_percent subindustry P3 D90 | 0.33 | 0.08 | 8.03% | 1.89bp | 0.27 | 0.47 | 3 | 杀 |
| 6 | zqRVPvxR | mcr38_overall_percent sector P5 D90 | 0.41 | 0.12 | 8.55% | 2.39bp | 0.46 | 0.48 | 3 | 杀 |
| 7 | LLdQgPvM | mcr38_overall_percent sector P3 centered D90 | 0.33 | 0.10 | 9.87% | 2.18bp | 0.34 | 0.80 | 3 | 杀 |
| 8 | LLdQgPvv | mcr38_longterm_percent sector P3 D90 | 0.48 | 0.15 | 7.95% | 2.92bp | 0.39 | 0.69 | 3 | 杀 |

决策：**8/8 全灭**。最佳 #2 direction_rating sh0.53/2Y0.94。**技术评级信号在 SLOW_AND_FAST 中性化下被剥离**（评级是动量衍生量，与 SLOW_AND_FAST 风险因子高度共线）；社区 STATISTICAL 上限仅 0.68。距 1.58 缺口 >1.0，无突破路径。**macro38 DEAD END**。args 存 tracking/args_macro38_b85.json。

### fundamental91 预筛 → DEAD END（零模拟成本）

get_datafields(dataset_id=fundamental91, USA/TOP3000/D1)：返回 10-K filing NLP 字段（cat10_sentiment 等），**coverage 全 ~0.36（VECTOR, alphaCount=0）**，无 coverage≥0.8 字段。覆盖率太低，无可用连续字段。**fundamental91 DEAD END**（未消耗模拟预算）。

### Batch b86 ｜ risk65（风险模型残差/特定收益）｜ TOP3000/SLOW_AND_FAST/trunc0.04/decay6 ｜ args tracking/args_risk65_b86.json

假说：risk 模型 residual/specific returns（特质收益）动量 + low-vol reverse（srisk 反向）。proven 模板（sector+P3+D90+SLOW_AND_FAST+trunc0.04）放大。risk 金字塔 ×1.2 未点亮。6 字段全 MATRIX, cov 0.95-1.0。注：create_multi_simulation 工具 MCP 超时（REQUEST_TIMEOUT 序列化 bug），但 sim 实际在 BRAIN 跑完，经 get_user_alphas(order=-dateCreated) 取回结果。

| # | id | 字段/变体 | sh | fit | tvr | margin | subU | 2Y | RAfail | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0mMJAarq | etfm3_dsrt_intermediate sector P3 | -0.22 | -0.05 | 13.05% | -0.99bp | -0.18 | -1.16 | 4 | 杀 |
| 2 | j2r7nM89 | etfm4_dsrt_intermediate sector P3 | -0.22 | -0.05 | 13.05% | -1.01bp | -0.18 | -1.16 | 4 | 杀 |
| 3 | A17An2vl | trsd_3mfte_mfm sector P3 | -0.23 | -0.05 | 13.05% | -1.03bp | -0.18 | -1.18 | 4 | 杀 |
| 4 | 9q7n92Wd | trsd_4mfte_mfm sector P3 | -0.23 | -0.05 | 13.05% | -1.03bp | -0.18 | -1.18 | 4 | 杀 |
| 5 | 9q7n92Eq | etfm3_srisk 反向(low-vol) sector P3 | -0.15 | -0.03 | 7.84% | -1.02bp | 0.09 | -1.65 | 3 | 杀 |
| 6 | KPE1n2mx | etfm4_srisk 反向(low-vol) sector P3 | -0.15 | -0.03 | 7.84% | -1.0bp | 0.09 | -1.65 | 3 | 杀 |
| 7 | np8EnXAd | trsd_4mfte subindustry P3 | -0.33 | -0.08 | 9.03% | -1.58bp | -0.41 | -1.46 | 4 | 杀 |
| 8 | d5RGnPKJ | etfm3_dsrt sector P5 | -0.14 | -0.03 | 12.15% | -0.7bp | -0.19 | -1.04 | 4 | 杀(最不负面) |

决策：**8/8 全灭——risk65 DEAD END**。关键：
① **全部负 sharpe（-0.14~-0.33）**：风险模型残差/特定收益在 SLOW_AND_FAST 下无预测动量；轻微反转效应（负）但太弱无法利用，2Y 强负（-1.04~-1.65）信号近期恶化。
② **4 个 specific-returns 字段（etfm3/etfm4 dsrt, trsd 3/4mfte）产出近乎相同的弱负信号（~-0.22）**= 同一特质收益的不同模型版本冗余。
③ **low-vol reverse（srisk 反向）也死**（-0.15, 2Y -1.65）：specific-risk 水平此处无低波异象。
④ **proven other566 模板不可迁移到 risk65 残差字段**（同 model238/analyst 教训：模板迁移失败是常态）。

### 替换搜索总结 + 当前诚实状态

已排除数据集天花板（本会话 + 前序）：other571(fit capped0.49)、model38(ceiling1.0)、sentiment21/22(失败)、analyst39/consensus(ceiling0.8-1.07)、news76(sh1.13)、shortinterest3/insiders3(弱)、macro38(~0.53)、fundamental91(coverage0.36)、risk65(全负)、model238(~0.80)、option40(subU结构性失败+prod_corr>0.7)、other566(prod_corr>0.7)。WebDataScope 甜点区=other566+option40 均已用且 prod_corr 失格。

**三 alpha 候选篮子最终状态（更新）**：

| # | alpha_id | 数据集/风格 | prod_corr | 状态 |
|---|---|---|---|---|
| 1 | 6XeWqEE7 | option40/IV skew凸性 | >0.7 | ❌ DISQUALIFIED |
| 2 | xAdL5vmN | ai_equity_alpha/盈余惊喜凸性 | 0.6697✓ | ✅ 可提交（用户手动） |
| 3 | GreR6x2J | other566/sector标签凸性 | 0.7447 | ❌ DISQUALIFIED（本轮重验确认） |

**结论**：3 个目标 alpha 中仅 1 个（alpha2）可提交。alpha1+alpha3 均 prod_corr>0.7 失格。macro38/fundamental91/risk65 三个 contingency 数据集全部 DEAD END。预算剩 ~14（约 1 batch）。create_multi_simulation 工具出现 MCP 超时 bug（sim 实际跑完但响应序列化失败，需 get_user_alphas 取回）。**待用户决策**：是否用最后 ~1 batch 试新数据集，或接受 1 个可提交 + 近失池候选。


---

## GBR 区域挖掘（2026-08-04）17 批次 / ~136 回测

**区域状态**：GBR 为全新区域（公告 "Launching new region DEU and GBR"）；userCount/alphaCount 全 0（零竞争）；当期主题 GLB/D1 Power Pool Aug'26 不含 GBR → 候选需 YELLOW + WAIT_THEME_ROTATION。GBR/D1/MODEL 金字塔 ×2.0。

**核心发现**：pv106 流动性信号在 GBR **方向反转**（KOR 做多 spread，GBR 需做空 transaction_cost_percentile_10）——区域特异性第一课。

**最佳结构**（天花板，未达标）：
`add(-group_rank(ts_rank(ts_backfill(transaction_cost_percentile_10, lookback=60), 44), sector), ts_rank(ts_backfill(winsorize(mdl238_global_screening_rank, std=5), lookback=60), 44))`
GBR/TOP700/D1/MARKET/decay12/trunc0.06/max_trade ON → sh 0.96 fit 0.53 2Y 1.58 margin 6.2bp tvr 13.7% subU 0.50 rn 0.61（mL59b2gp，跨批次复现稳定）
无 sector-group 变体 sh 0.98-1.02 / 2Y 1.57（j26mnkRW/E5GJk3dR）。

**天花板**：sharpe 0.96-1.05 平台（decay 8-16/trunc 0.04-0.08/窗 33-100/中性化 NONE/MARKET/SECTOR 全扫）；距达标 1.58 缺口 0.55+。2Y 可达 1.58（边界 fail）；margin/turnover/subU 均 PASS；rn 仅 0.6。

**数据集评级**（GBR/TOP700/D1）：★★★ pv106（反转腿）+ model238（blend 腿）；★★ model106/insider_matrix（仅 2Y 1.85-1.95，IS 死）；★ model30/model264/model262/model109/predictive_starmine/model216；✗ analyst44/47/9、shortinterest3、dl_riskfree、model250、other545、euro_equity_imbalance(cov0.157)、stock_cluster_dl、model36、model182、news/sentiment。

**纪律确认**：无达标候选（sharpe 未过 1.58）→ 未做 robust、未 set_alpha_properties、未提交任何 alpha。delay=0 不可行（pv106 无 D0 字段）。
