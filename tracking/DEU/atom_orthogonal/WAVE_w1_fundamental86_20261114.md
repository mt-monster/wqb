# WAVE w1 — fundamental86 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-14；归因员：atom_orthogonal 单槽（纯本地归因，判读不改写邻接数据集先验，跨区不外推）
- 配置：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=4、trunc=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR
- 派发链：preflight（valid=true、unknown_fields=[]、any_changed=false）→ 静态闸（ExpressionValidator 10/10 VALID + operator_audit safe）→ 查重（used_ids 仅 fnd86_earnings_score，本波 10 臂零全同全派）→ multisim=`2hhCTvc8m58gbZB1eHMXe7x7` → 10/10 COMPLETE、errors=0 → harvest 首试即成 → upsert_backtest_rows n=10、0 跳过
- 判读基准（ask 给定）：裸水平天花板 S~0.94；条件化/未测字段组合目标带 1.2–1.6；2Y 裸水平 0.00/−1.17（本集最弱轴）、条件化 ≥1.58 可期待（lever C，DEU FUNDAMENTAL 2Y 天然达标轴）；量级参照 fnd45 基线 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，非现行承诺）；sub 低覆盖 ⇒ 分组轴必须粗（DEU 本地实证 sector 1.30 > industry 0.38 > subindustry 0.30，s2_nearmiss_rescue_20261104.md:4963，已本会话核验）

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | 臂（缩写） | alphaId | S | F | 2Y | sub | TO | DD | margin | LC/SC | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | backfill(insider) 裸 | kqaeVEY6 | -0.39 | -0.29 | -0.6 | ERROR | 0.0639 | 92.34% | -0.002127 | 8/8 | 存在性探针；CW=0.5 FAIL；宽度塌缩 |
| 2 | backfill(price_momentum) 裸 | O0WKrQjb | 0.52 | 0.37 | -0.23 | 0.68 | 0.1075 | 24.22% | 0.00121 | 47/44 | 存在性探针；TO 全波最高 |
| 3 | trade_when(δavg>0, rank(avg,sector)) | rK7Q5pw9 | 0.59 | 0.45 | 1.07 | 0.47 | 0.0366 | 34.51% | 0.004015 | 65/55 | 2Y 跨 1.0 |
| 4 | rank(insider mean, sector) | YPaX5Lo6 | 0.19 | 0.07 | 0.16 | 0.02 | 0.0421 | 22.34% | 0.000794 | 59/62 | insider 裸排位 |
| 5 | trade_when(δinsider>0, rank(insider,sector)) | j2aN3zKW | 0.22 | 0.13 | 0.67 | ERROR | 0.0311 | 45.59% | 0.002622 | 11/9 | 宽度塌缩 |
| 6 | rank(divide(rel_val, momentum), sector) | d5aeOkrj | -0.19 | -0.06 | 0.72 | 0.69 | 0.0429 | 48.58% | -0.000662 | 112/113 | 比值轴 |
| 7 | multiply(zscore(δmom), zscore(rel_val)) | gJa7QkV0 | 0.56 | 0.39 | 0.89 | 0.77 | 0.1457 | 24.75% | 0.000974 | 41/41 | sub 全波最佳 |
| 8 | rank(avg, bucket(rel_val,0,10,2)) | N1PkQxEw | **0.91** | 0.70 | 0.97 | 0.55 | 0.0574 | **12.18%** | 0.00256 | 113/113 | 全波最佳 S；CW=0.109432 边缘 FAIL（limit 0.1） |
| 9 | rank(risk, sector) | akaXLjmW | 0.01 | 0.0 | 0.91 | -0.4 | 0.031 | 30.31% | 0.000085 | 106/116 | S-2Y 跷跷板最强 |
| 10 | trade_when(δmom>0×δrelval>0, rank(avg,sector)) | 1YW6xk3W | 0.76 | **0.83** | 0.71 | 0.35 | 0.0245 | 27.87% | **0.012109** | 47/38 | PnL=14,021,624 全波最高 |

臂1/臂5 的 sub 项为平台 LOW_SUB_UNIVERSE_SHARPE:ERROR 态、无数值，未造数。臂归属按平台 code 字段逐条比对臂表达式核验（收割步骤⑥）。

## §2 逐臂归因条目

1. **臂1 kqaeVEY6**：存在性探针成立（LC=8>0 ⇒ `fnd86_insider_trading_score` 有数据，非全 NaN）。**数据层排除判读**：LC8/SC8（TOP500 下 1.6% 宽度塌缩）+ CW=0.5 FAIL + DD 92.34%（裸 backfill 未 rank 化的 16 名持仓集中）⇒ 本臂记 **data_excluded 形态**——S=-0.39 不作信号层证据；**数据层排除≠信号死，≠数据集排除**。符号指纹：裸水平 -0.39 vs 臂4 sector 排位 +0.19——结构不同（8 名裸持仓 vs ~60 名排位）、量级不对称（0.39 vs 0.19），**不构成衰减对称对，不触发翻转保留**；insider 方向记「未决」。跨区不外推：未引用任何 TWN/KOR 经验。
2. **臂2 O0WKrQjb**：存在性探针成立（LC=47>0 ⇒ 臂6/7/10 跨支柱腿前提成立）。符号 S=+0.52 与 higher=better 一致，无需翻转。**S-2Y 跷跷板指纹**（S 0.52 / 2Y -0.23）：momentum 支柱裸水平近期 regime 转负，与基准「裸水平 2Y 0.00/−1.17 最弱轴」同向。TO 0.1075 全波最高（裸 backfill 未平滑）。
3. **臂3 rK7Q5pw9**：自门控（δ66(avg)>0）。**2Y=1.07 跨 1.0 ⇒ 裸水平 2Y 死轴的条件化复活首证**（对照裸 2Y 0.00/−1.17），方向与 lever C 先验一致。符号与动量门控符号先验一致（分数改善→做多，S>0）。TO 0.0366 极低（trade_when 持仓效应）。波内对照：同载荷交叉双门（臂10 0.76）> 自门（0.59）⇒ 交叉门控 > 自门控。
4. **臂4 YPaX5Lo6**：insider 裸排位 S 0.19/F 0.07 弱。LC=59/SC=62 远宽于臂1 裸形态（8）⇒ 臂1 的塌缩属「裸未 rank 化」形态属性、非字段全空；但 ~60/500 仍窄。符号弱正不翻转。
5. **臂5 j2aN3zKW**：条件化 insider。门控把 2Y 从 0.16（臂4）抬到 0.67，与臂3 同向（门控救 2Y）；但 LC=11/SC=9 **宽度塌缩** ⇒ 读数薄，记宽度塌缩形态，不作信号层结论。sub=ERROR 无数值未造数。
6. **臂6 d5aeOkrj**：比值轴 divide(rel_val, momentum)。|S| 0.19 噪声带；**S-2Y 跷跷板**（S -0.19 / 2Y 0.72 / sub 0.69 双正）。比值无 higher=better 经济先验 ⇒ **符号未决**，下波可跑反向腿（momentum/valuation）作符号判别。稀释铁律：divide 对应单腿本轮均未测 ⇒ 判定挂起；记弱轴不判死。
7. **臂7 gJa7QkV0**：乘法形态 zscore(δ66(momentum))×zscore(rel_val mean)。sub 0.77 全波最佳。**稀释铁律**：纯腿（δ66(momentum) 裸、rel_val 裸排位）未测；最近实测对照=臂2 momentum 裸水平 0.52，0.56≥0.52 ⇒ 对已测对照不稀释（严格判定挂起）。TO 0.1457 全波最高（双 zscore 无平滑）⇒ 推进需预平滑压 TO。
8. **臂8 N1PkQxEw**：bucket 交互 rank(avg, bucket(rel_val, range 0,10,2))。**全波最佳 S 0.91**、DD 12.18% 全波最低、LC=SC=113 宽度健康。**稀释铁律通过**：0.91 > 同载荷已测对照（臂10 0.76 / 臂3 0.59）；裸单腿 group_rank(avg, sector) 未测，挂起注记。CW=0.109432 边缘 FAIL（平台 checks limit 0.1）⇒ 距硬闸 0.0094 ≤0.4 ⇒ near-gate#1。2Y 0.97 ≈1.0。
9. **臂9 akaXLjmW**：risk 裸排位。**最强 S-2Y 跷跷板**（S 0.01/F 0.0 vs 2Y 0.91 / sub -0.4）⇒ risk 支柱 **S 轴死、2Y 轴活**，需条件化表达。risk_score 存在性 LC=106>0 有数据（非专探针、不判数据层排除）。
10. **臂10 1YW6xk3W**：交叉双门 trade_when(δmomentum>0 × δrelval>0, rank(avg, sector))。F 0.83 / margin 0.012109 / PnL 14.02M 三项全波最高、TO 0.0245。**稀释铁律通过**：同载荷单门对照臂3 0.59 ⇒ 0.76>0.59，门控叠加有增益（波内归因对照）。F=0.83 距 fitness_min 1.0（tracking/DEU/config/thresholds.json:15）差 0.17 ≤0.4 ⇒ near-gate#2。

## §3 波级判读

### 绿芽（sprouts）
- **臂8 bucket 交互（avg×rel_val）**：S 0.91 全波最佳 + DD 12.18% 最低 + CW 距闸 0.0094 —— 头号绿芽。
- **臂10 交叉双门载荷 avg**：F 0.83 + margin 0.0121 + PnL 14.0M 三项全波最高。
- **臂3 自门控**：2Y 1.07 —— 裸水平 2Y 死轴条件化复活首证。
- **臂7 zscore 乘法**：sub 0.77 全波最佳。
- **支柱结论**：`average_score` = 最佳载荷支柱（top3 臂 8/10/3 全以其为载荷）；`price_momentum_score` / `relative_valuation_score` = 最佳门控与交互搭档。

### 死轴（deadAxes）
- **裸水平 2Y 轴**（基准 0.00/−1.17，波内复证臂2 2Y=-0.23）——**条件化复活路径已实证**（臂3 1.07），记「裸水平死/条件化活」，不作绝对死轴。
- **risk 支柱 S 轴**（裸排位 S 0.01/F 0.0）——S-2Y 跷跷板（2Y 0.91），S 维度死、2Y 维度活。
- **insider 宽度塌缩轴**（裸 8 名/条件化 11 名 + CW 0.5 FAIL + DD 92.34%）＝**数据层排除轴，非信号死**；排位形态略宽（59/62）但 |S|≤0.22 弱 ⇒ 低优先。
- **比值轴**（臂6）：|S| 0.19 噪声带、符号未决——记弱轴/待符号判别，不判死（2Y 0.72/sub 0.69 双正）。

### 数据层排除登记（口径区分）
- `fnd86_insider_trading_score`：裸水平与条件化形态均宽度塌缩（LC 8→11）+ 臂1 CW=0.5 FAIL ⇒ **data_excluded（数据层排除）**，登记时与「信号死」严格区分；字段排位形态 LC=59>0 证明非全空。
- 数据集级：**不排除**——average/price_momentum/relative_valuation/risk 四支柱 LC 41–116 宽度健康。

### 符号指纹汇总
- higher=better 构造（臂2/3/4/5/8/9/10）全系 S≥0 或中性 ⇒ 符号一致，无翻转对被触发（本波无刻意反向臂，无衰减对称对成立）。
- 方向未决两处：insider（臂1 -0.39 vs 臂4 +0.19，结构不同量级不对称）、比值轴（臂6 -0.19 弱负，无先验方向）。

### 跨区不外推核对
- 本波归因未引用 TWN 经验；低覆盖粗分组依据为 **DEU 本地实证**（s2_nearmiss_rescue_20261104.md:4963：cov 0.26 时 sector 1.30 > industry 0.38 > subindustry 0.30），已本会话核验原文。
- fundamental86 的 cov0 判死已于 11-05 撤回（同档案 :4973，已核验），本波数据存在性由 10 臂 LC>0 直接复证；判死档/dead 标记未单独作依据。

## §4 datasetStatus 裁决

**= active（继续加注）**。依据（全部为本波读数）：
1. 最佳 S 0.91 已触裸水平天花板参照（~0.94）而臂型为条件化/bucket 形态；梯度方向明确：裸 0.19–0.59 → 门控 0.59–0.76 → bucket 0.91；条件化目标带 1.2–1.6 尚有一档未试。
2. 2Y 条件化复活实证（臂3 2Y=1.07；臂8 0.97、臂9 0.91 紧随），对照 lever C「条件化后 ≥1.58 可期待」方向一致、未达。
3. 四支柱宽度健康（LC 41–116），仅 insider 一字段宽度塌缩（字段级 data_excluded，非集级）。
4. **六维判死闸 D1–D6 远未满足**（见 §6），距判死线极远；「近穷尽」标签不构成排除；探针条款未触发（本波 10 臂，非 <10 探针）。
5. 判死依据=读数；不改写邻接数据集先验；fnd45/fnd72 等邻接集结论不受本裁决影响。

## §5 nearGateCandidates（≤2，按 S 降序；先测 prod 再扫参——prod 雷在核心不在搭档）

| alphaId | 臂 | 触发 | 读数（原样） |
|---|---|---|---|
| N1PkQxEw | 臂8 | S 0.91 全波最佳；CW=0.109432 距平台 limit 0.1 仅 0.0094（≤0.4） | S=0.91/F=0.70/2Y=0.97/sub=0.55 |
| 1YW6xk3W | 臂10 | F 0.83 距 fitness_min 1.0（thresholds.json:15）差 0.17（≤0.4） | S=0.76/F=0.83/2Y=0.71/sub=0.35 |

臂3（S 0.59/F 0.45）距 F 闸 0.55 >0.4 且 S<1.2 ⇒ 不入选。阈值出处：`tracking/DEU/config/thresholds.json`（fitness_min=1.0 line 15；sharpe_min=1.58 line 14；近闸参照 near.sharpe_min=1.0 line 12；本地评审层 concentrated_weight_max=0.5 line 20 与平台 checks limit 0.1 是两个不同口径，本档案近闸距离按 ask 转录的平台 checks limit 0.1 计）。

## §6 判死闸六维自检（本波后更新；对照 DEATH_AUDIT_20261110.md §3.2 零命中基线）

| 维度 | 状态 |
|---|---|
| D1 结构互异模板 | 本波 10 臂约 7 类机制（裸水平/排位/自门/交叉双门/比值/zscore 乘法/bucket 交互），距 ≥10 仍有缺 |
| D2 字段族自测 | 本波实测 5 字段（insider/price_momentum/average/relative_valuation/risk）；earnings_score 此前 G 波已用，未测字段仍存 |
| D3 矩全家 | 水平✓ 一阶差✓ 比值✓；**二阶波动矩缺失** |
| D4 分组轴 | sector + bucket = 2 ✓（subindustry/industry/market 未测，低覆盖粗分组纪律下 sector 优先） |
| D5 非线性 | bucket✓ trade_when✓（signed_power/ts_rank/ts_quantile 未测） |
| D6 配置 | **单配置**（TOP500/SUBINDUSTRY/decay4），<2 ✗ |

结论：远未触闸；本波裁决 active，与判死无关。

## §7 下波方向（由本波读数驱动，供开波参考）

1. bucket 交互主线加密：臂8 骨架换载荷/换 bucket 维度（bucket(momentum)/bucket(risk)），目标带 1.2–1.6。
2. 门控叠加：臂10 双门 → 三门或换门源；保持载荷 avg。
3. 2Y 深化：条件化 2Y 1.07 → ≥1.58（lever C 预期带），优先 bucket+门控复合形态。
4. 臂7 若推进必须预平滑压 TO（0.1457 全波最高）。
5. insider 支柱降权（宽度塌缩 + 弱信号）；比值轴先跑反向腿作符号判别再决定投入。
6. 补 D3 二阶波动矩模板 ≥1 条、D6 第二配置（换 decay 或中性化域），为将来任何判死论证预存维度。

## §8 证据通道与盲区登记

- 本档案读数来源：ask 转录的臂序读数（收割步骤⑥臂归属按平台 code 核验）+ 本会话实读 `tracking/DEU/config/thresholds.json`、`tracking/DEU/s2_nearmiss_rescue_20261104.md:4963/:4973`。
- 核验缺口（如实登记）：`list_alphas_by_wave(DEU, 1)` 返回空——该工具 wave_number 仅收整数而本波以字符串 `w1` 落库，**逐臂落库行未经该通道复核**；落库依据为收割步骤⑦回执（n=10、0 跳过）。
- 通道盲区（沿 ask）：query_dataset_profile/query_field_profile 对 DEU 全 0 行；expressions 表不含 MCP 直连仿真，G 波由战役文档平台 alpha id 记录覆盖。
- 相关性查询未做（单槽在相关性员，按 ask 边界）；near-gate 两臂的 prod 测序归下槽。
