# WAVE w1 — fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-14；归因员：atom_orthogonal 单槽（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- ⚠ **w1 标签共享**：w1 在 DEU 已被早槽 fundamental86 波占用（expressions/backtest_results 各 10 行、wave_results 行 id 2174 于 16:19:51 落库）；本档按集名后缀区分（同 S0 档命名纪律 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:4`），不覆写他槽档案；wave_results 行按契约合并式追加（§9）
- 配置（收割自报，全臂一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=4、trunc=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR
- 派发链（收割自报）：preflight valid=true（6 数据字段平台侧全部核实、无 VECTOR 包裹 any_changed=false）→ PLY validator 10/10 → 查重（本战役派发前零记录；臂 1/2 曾在 2026-11-05 mcp-20261105 多集探索波派发，非本战役重复，按臂表原样派发）→ multisim 10 臂 → 10/10 COMPLETE errors=0 → harvest（臂归属按平台 code 逐条核验，臂 5 WjlKJZbZ / 臂 8 WjlKJZeZ 相似 id 已区分）→ upsert_backtest_rows n=10 → 只读复核
- **本槽只读核验（本轮实跑 `logs/_tmp_fnd72_w1_attr_verify.py`，sqlite mode=ro，零写入）**：backtest_results 中 DEU/w1 + dataset='fundamental72' 恰 **10 行**、alpha id 与臂表全对、sharpe/fitness/turnover/LC/SC 逐行与臂序读数一致（**10/10 通过**）；expressions 同键 10 行；wave_results DEU/w1 行存在（id 2174，fnd86 早槽所写，verdict=PARTIAL）
- 判读基准（ask 给定 + 本槽一手复核）：季度 IS delta 几何天花板 **1.42**（RREALzx0 DB 读数，FAST 格）；裸年报宽面天花板 **0.37**（wave107，死档 1574 payload）；新自由度臂目标带 **1.5–1.7**；fnd45 量级参照 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，**事实非承诺**）；**2Y 硬闸 = 1.58**（`tracking/DEU/config/thresholds.json:5` two_year_sharpe_min，:6 注记一手证据 RREALzx0 checks.fail {LOW_2Y_SHARPE, value 1.43, limit 1.58}；KPJmRpGN 2Y=1.58 恰过）；sharpe_min 1.58（:14）、fitness_min 1.0（:15）；sub<0.75 稳健告警（近闸族参照 0.83–0.92 属 FAST 格）；TO <20% 目标 / >25% 结构告警；死档约束：id 1573（年报面先 rank(F) 探针验 LC+SC ≥50）/ 1575（ts_target_tvr_decay 禁用）/ 1577（bf 窗基线 66）——本波臂表已遵守（臂 7–10 即 1573 协议探针；全波未用 TVR 层；bf66）

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | 臂（缩写） | alphaId | S | F | 2Y | sub | TO | DD | margin | LC/SC | RA fail / 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 三重乘 δ240×δ176×ts_rank1008(q_ebit)，group_rank sector | E56VAa19 | 0.20 | 0.07 | 0.12 | 0.63 | 4.38% | 23.41% | 0.000667 | 97/139 | 3 项；⚠平台撞件=2026-11-05 既有件全同 payload，本次零新仿真 |
| 2 | 同臂1 换 q_is_oper_inc | 2r5Pegw8 | 0.21 | 0.07 | 0.21 | 0.67 | 4.32% | 22.89% | 0.000686 | 103/156 | 3 项 |
| 3 | trade_when(δ22(bf66 ebit)>0, 臂1载荷) | A1xqEpNw | 0.48 | 0.27 | -0.34 | 0.51 | 3.16% | 15.51% | 0.00245 | 65/57 | 4 项：+CONCENTRATED_WEIGHT(0.285714, limit 0.1) |
| 4 | trade_when(δ66(bf66 ebit)>0, 臂1载荷) | rK7Q8qO9 | 0.44 | 0.22 | -0.60 | 0.36 | 4.11% | 15.44% | 0.001551 | 65/58 | 3 项 |
| 5 | trade_when(δ22(bf66 oper_inc)>0, 臂2载荷) | WjlKJZbZ | 0.53 | 0.30 | -0.31 | 0.53 | 3.15% | 14.52% | 0.00261 | 68/59 | 4 项：+CONCENTRATED_WEIGHT(0.285714, limit 0.1) |
| 6 | 臂1载荷 group_rank bucket(rank(ts_std_dev(ebit,252)), range 0,1,0.25) | npawrjPw | **0.68** | **0.43** | -0.04 | 0.40 | 6.33% | **8.82%** | 0.001599 | 68/68 | 3 项；CLUSTER_TEST warning 0.76；本波信号臂最高 S、最低 DD |
| 7 | rank(fnd72_s_pit_or_is_a_ebit) 年报水平探针 | LLKO3vZ9 | 0.07 | 0.02 | **1.51** | 0.39 | 1.57% | 39.08% | 0.000747 | 73/76 | 3 项；存在性探针（死档 1573 协议） |
| 8 | rank(a_net_income) | WjlKJZeZ | -0.01 | -0.0 | 0.93 | 0.16 | 1.61% | 40.71% | -0.000104 | 76/79 | 3 项；探针 |
| 9 | rank(a_sales_rev_turn) | kqae9wJl | -0.04 | -0.01 | 1.17 | 0.14 | 1.37% | 35.91% | -0.000448 | 76/79 | 3 项；探针 |
| 10 | rank(total_liabilities_and_equity_value) 通用名 MATRIX | qM7eVaEP | -0.16 | -0.05 | 0.99 | 0.01 | 1.49% | 42.85% | -0.001849 | 74/77 | 3 项；探针 |

（臂 7–10 = 年报 IS 标量族 + 通用名 MATRIX 族存在性探针；全部 LC>0、LC+SC 149–155 ≥50 ⇒ 死档 1573 开门线通过。）

## §2 逐臂归因条目

1. **臂1 E56VAa19**（三重乘 δ240×δ176×ts_rank1008(q_ebit)，group_rank sector）：⚠**平台撞件**——2026-11-05 mcp-20261105 多集探索波既有 SUBINDUSTRY×TOP500×D1 件全同 payload 返回同 id，**本次零新仿真，读数为 2026-11-05 数据点复读**；设计注记「季度 IS 族从未在 SUBINDUSTRY 下跑过/首次跑 SUBINDUSTRY」被撞件证伪（D6 假设按库内既有点重估）。符号：S +0.20 与 IS delta 符号先验（盈利改善→做多）同向；无反向臂 ⇒ 衰减对称未实测。稀释铁律：对应单腿（rank(ts_delta(·,240)) 等）本波零实测 ⇒ 严格判定挂起；波内间接对照 = 同复合的条件化变体 0.48–0.68 全部 > 0.20 ⇒ 条件化在提纯非稀释。**跨配置对照（D6 核心）**：同表达式 RREALzx0（FAST 格）DB 读数 S 1.42 vs 本臂（SUBINDUSTRY 格）0.20 ⇒ **中性化轴 7x 缺口**，弱读数主归因配置轴而非几何本身。2Y 0.12 双弱。
2. **臂2 2r5Pegw8**（同臂1 换 q_is_oper_inc）：S 0.21 vs 臂1 0.20（ΔS=0.01）⇒ q_ebit→q_is_oper_inc 字段内同构，季度 IS 双字段在该几何下无实质差；2Y 0.12→0.21 同族双弱。符号与先验一致。
3. **臂3 A1xqEpNw**（trade_when δ22>0 门控，ebit）：**门控提纯成立**（波内归因对照：0.20→0.48）但 **2Y +0.12→-0.34 反转** ⇒ S-2Y 跷跷板——门控样本=盈利改善事件子集，全期 S 由早期贡献、近 2Y 机制失效。**CW 0.285714 FAIL(limit 0.1) 判读：LC 65/SC 57 无宽度塌缩** ⇒ 结构层指纹（trade_when 门控集中），**非数据层排除**（死档 1573 的「宽度≤5 必挂」形态本轮未出现）；按 ask CW 指纹纪律不改符号重试。TO 3.16% 低（门控持仓效应）。
4. **臂4 rK7Q8qO9**（trade_when δ66 门控，ebit）：门窗口径对照 22d > 66d（S 0.48 vs 0.44）；**2Y -0.60 比 22d 门（-0.34）更深** ⇒ 确认窗越长、信号滞后放大、2Y 反转越深。无 CW fail。与臂3 同属跷跷板死形。
5. **臂5 WjlKJZbZ**（trade_when δ22 门控，oper_inc）：S 0.53 波内信号臂第二；字段内对照 oper_inc 门控 0.53 > ebit 门控 0.48。与臂3 同形跷跷板（2Y -0.31）+ CW FAIL；宽度 68/59 健康 ⇒ CW=结构层指纹。
6. **臂6 npawrjPw**（bucket(rank(ts_std_dev(ebit,252)),4桶) 条件化）：**S 0.68 波内最高**、F 0.43 波内最高、DD 8.82% 波内最低、TO 6.33% 健康。**波内条件化梯度链完整：裸跑 0.20–0.21 → trade_when 门控 0.44–0.53 → bucket 条件化 0.68**——条件化每加一层 S 单调上升（波内归因对照）。稀释铁律：0.68 高于全部波内同复合对照 ⇒ 不稀释；单腿未测严格判定仍挂起。2Y -0.04 ≈ 平 ⇒ 轻度跷跷板（全期收益非近 2Y 驱动）。sub 0.40 <0.75 ⇒ 稳健告警。CLUSTER_TEST warning 0.76 登记。
7. **臂7 LLKO3vZ9**（rank(a_ebit) 年报水平探针）：**存在性探针通过**（死档 1573 协议：LC 73/SC 76 >0、LC+SC=149 ≥50）⇒ 年报 IS 标量族数据在（正向存在性证据；per 探针协议不作覆盖度读数）。S 0.07 低于裸年报宽面天花板 0.37（wave107）⇒ **S 面弱**。**2Y 1.51 ∈ 近闸族带 1.43–1.58、距 2Y 硬闸 1.58（thresholds.json:5）仅 0.07 ≤0.4 ⇒ 全波唯一近闸形状、2Y 轴活体**（near-gate#1）。S-2Y 极端跷跷板（S≈0 vs 2Y 1.51）。sub 0.39 告警带；TO 1.57%（慢变量低 TO 一致）。
8. **臂8 WjlKJZeZ**（rank(a_net_income)）：LC 76/SC 79 ⇒ 数据在。S -0.01 噪声带（水平利润排序无信号）；2Y 0.93 <1.0 ⇒ 按 S0 基准记「机制需条件化」指纹、不记死；sub 0.16 弱。margin -0.000104 弱负。
9. **臂9 kqae9wJl**（rank(a_sales_rev_turn)）：LC 76/SC 79 ⇒ 数据在。S -0.04 噪声带；2Y 1.17——距 2Y 闸 1.58 = **0.41，恰在 0.4 近闸线外 0.01** ⇒ 机械判据不入 near-gate（边界如实登记）；2Y 方向活但未达近闸族带 1.43–1.58。sub 0.14。
10. **臂10 qM7eVaEP**（rank(total_liabilities_and_equity_value)，通用名 MATRIX 族）：LC 74/SC 77 ⇒ 族数据在（S0 档 §3.2 D2 缺口「通用名 MATRIX 族零本地实测」本轮补上）。S -0.16 全波最低、sub 0.01 全波最低 ⇒ 水平负债权益排序 S 面死；2Y 0.99 <1.0 需条件化指纹。margin -0.001849 全波最弱。

## §3 指纹 / 铁律 / 跨区核对汇总

- **符号指纹**：本波无反向臂 ⇒ **衰减对称未实测、无翻转保留判定**（如实登记，不造对称对）。正向证据：6 条信号臂 delta/rank 结构 S 0.20–0.68 全正，与 IS delta 符号先验（盈利改善→做多）一致；年报水平臂 S -0.16~0.07 为水平排序弱读数量级（噪声带），不构成单向事件型指纹。**CW 挂闸（臂 3/5）宽度健康（LC 65–68 / SC 57–59）** ⇒ 结构层指纹（trade_when 门控集中），**非数据层指纹**——死档 1573 的「宽度≤5 必挂」形态本轮未出现，登记口径已区分。
- **稀释铁律**：核心判定**挂起**——三重乘法复合（臂1/2）与 bucket 条件化（臂6）的对应单腿（rank(ts_delta(·,240)) / rank(ts_delta(·,176)) / rank(ts_rank(·,1008)) / ts_std_dev 裸）本波零实测 ⇒ 按「缺对照不判稀释也不判达标」挂起（同兄弟槽 fnd86 臂7 处理）。波内间接对照：同复合的三个条件化变体（0.48 / 0.44–0.53 / 0.68）**全部 > 裸跑（0.20–0.21）** ⇒ 条件化在提纯，「复合低于对应单腿」的稀释触发条件无一成立。
- **跨区不外推**：本波归因零 TWN 引用；全部对照为 DEU 域内（RREALzx0/KPJmRpGN DB 读数、wave107 死档 payload、fnd45 基线 waveBE242:35 仅量级参照）；fnd45 收敛结论与 fnd89 六维死均不因本波改写（S0 档 §二 明文）。
- **波级稳健性聚合**：全波 sub 0.01–0.67 **十臂全部 <0.75 稳健告警线**（近闸族参照 0.83–0.92 属 FAST 格）——SUBINDUSTRY 格稳健性整体偏低，与 §2.1 的 7x 配置缺口同向。TO 1.37–6.33% 全部远离 20%/25% 线，无结构性 TO 告警。

## §4 绿芽（sprouts）/ 死轴（deadAxes）

**绿芽**：
1. **年报 a_ebit 水平 × 2Y 轴活体**（LLKO3vZ9：2Y 1.51，距 2Y 硬闸 1.58 仅 0.07）——年报面 S 死但 2Y 轴活，全波唯一近闸形状；需条件化/配置轴表达而非裸水平重跑。
2. **bucket(vol) 条件化几何**（npawrjPw：S 0.68 波内最高 + DD 8.82% 最低 + F 0.43）——SUBINDUSTRY 格内条件化梯度顶点（0.20→0.44–0.53→0.68）。
3. **配置轴对照活体**：同表达式 SUBINDUSTRY 0.20（E56VAa19）vs FAST 1.42（RREALzx0，DB）——**中性化轴 7x 缺口**，D6 宇宙/中性化/delay 轴是本集最大未扫自由度（§54.5 处方轴同向）。
4. **trade_when 门控 S 提纯**（0.20→0.44–0.53，波内对照成立）——半株：S 提纯实、2Y 轴死（跷跷板），2Y 未解前不重注门控。

**死轴**：
1. **季度 IS delta 三重乘法裸跑轴 @SUBINDUSTRY 格**：S 0.20–0.21 / 2Y 0.12–0.21 双弱（臂1/2）。⚠死域限定 SUBINDUSTRY 格——同几何 FAST 格 S 1.42 在册（RREALzx0），**不外推为几何死**。
2. **trade_when 门控 IS delta 轴的 2Y 面**：门控全提 S 但 2Y 全反（-0.31 ~ -0.60，臂3/4/5）⇒ S-2Y 跷跷板死形；门窗口径 22d > 66d（66d 门 2Y 更深）。
3. **年报水平 rank 的 S 面**：S 0.07 ~ -0.16（臂7–10），低于/远低于裸年报宽面天花板 0.37（wave107）⇒ S 维死；2Y 维活（1.51/1.17/0.99/0.93）——记「S 死 2Y 活」，非全轴死。
4. **2Y 轴不判死**：LLKO3vZ9 1.51 近闸活体在册；裸水平 2Y<1.0（臂8/10）按 S0 基准记「机制需条件化」指纹，非死轴。

## §5 数据层排除判读（口径区分）

- **本波无 data_excluded 臂**：全部 10 臂 LC 65–103 / SC 57–156，无宽度塌缩；6 数据字段（q_ebit/q_is_oper_inc/a_ebit/a_net_income/a_sales_rev_turn/total_liabilities_and_equity_value）存在性全部正向（LC>0）。
- 臂 3/5 的 CONCENTRATED_WEIGHT(0.285714) FAIL：宽度健康（57–68/侧）⇒ **结构层指纹（trade_when 门控集中），非数据层排除**——登记口径与死档 1573 的数据层形态（宽度≤5 必挂）严格区分。
- 年报面开门线：臂 7–10 LC+SC 149–155 ≥50（死档 1573 波 2 主臂开门线）⇒ 后续年报面主臂派发前置条件已满足。

## §6 nearGateCandidates（≤2，按 S 降序；先测 prod 再扫参——prod 雷在核心不在搭档）

| alphaId | 臂 | 触发 | 读数（原样） |
|---|---|---|---|
| LLKO3vZ9 | 臂7 | 2Y 1.51 距 2Y 硬闸 1.58（thresholds.json:5；KPJmRpGN 已触 1.58）仅 **0.07 ≤0.4**；S 0.07 不达 S≥1.2，近闸资格来自 2Y 轴 | S=0.07/F=0.02/2Y=1.51/sub=0.39/TO=1.57%/DD=39.08%/LC=73/SC=76 |

- 臂9 kqae9wJl 2Y 1.17 距闸 0.41——**恰出线 0.01**，不入册（边界如实登记）。
- 臂6 npawrjPw：S 0.68 距 sharpe_min 1.58 = 0.90、F 0.43 距 fitness_min 1.0 = 0.57，均 >0.4 ⇒ 不入册；sub 0.40 距 0.75 告警线 0.35，但告警线 ≠ 硬闸，不作近闸触发。
- 臂3/5 CW 0.285714：超限 0.1857，且 S/F/2Y 闸距离均 >1.0；CW 挂=指纹非候选（ask 纪律），不入册。
- ⚠ LLKO3vZ9 为年报水平裸 rank（S 面 0.07）：prod 测序前须明确它是 **2Y 轴活体载体**，不是 S 达标候选——若 prod 通过，推进方向是 2Y 闸位（2Y 条件化/配置轴），非直接提交链。

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = provisional（判弱入档）**。依据（全部为本波读数，判死依据=读数）：
1. 信号臂 S 0.20–0.68 全部低于 fnd45 量级基线 0.96（waveBE242:35）与新自由度目标带 1.5–1.7；10/10 臂 RA fail（LOW_SHARPE/LOW_FITNESS 全军，臂 3/5 另加 CW）；n_pass=0。
2. 但自由度未穷尽：2Y 轴活体（1.51 近闸）、bucket 条件化活体（0.68）、中性化轴 7x 缺口（0.20 vs 1.42）——active 的加注方向（换轴重设计）与本波几何（SUBINDUSTRY×裸乘/门控）不同 ⇒ 本波读数不支持对**当前几何**继续加注，判弱入档。
3. 判死六维闸未满足（§8：D1/D3/D6 未达）⇒ 按 AGENTS §7.6 缺任一维只能 provisional，不判死、不封集、不改写邻接集先验。
4. 数据面无宽度塌缩、无 data_excluded 臂（§5）⇒ 不触发 data_excluded。
5. **配置张力如实登记**：`thresholds.json:23-27` mode_b_qualification（2026-09-01）写「整波最强候选须 S≥1.25 且 F≥0.8 才有资格继续优化，未达一律判死」——本波最强 npawrjPw 0.68/0.43 不达该线。**不采用其判死分支**，理由：(a) AGENTS §7.6（2026-11-10 用户指令，更新）判死须六维逐维举证，本集 D1/D3/D6 未达；(b) 同日兄弟槽先例（fnd86 w1 最佳 0.91/0.70 同不达，裁决 active + near×2 入池，WAVE_w1_fundamental86_20261114.md §4–§5）；(c) ask 框架将本波路由到 provisional（dead_proposed 须先过检索覆盖审计+六维闸）。该规则与现行判死纪律的冲突留待区域配置治理，不在本槽单方改写。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 near ⇒ PARTIAL；n_pass=0 / n_near=1）。near=LLKO3vZ9。与同 wave_number 的 fnd86 行（PARTIAL）同值，合并写入不改变 verdict 单元格语义（§9）。

## §8 判死六维闸自检（对照 S0 档 §3.2 基线的增量）

| 维 | S0 档基线（本波前） | 本波增量 | 判定 |
|---|---|---|---|
| D1 结构互异模板 ≥10 | wave107 十模板（+近失波复合）已计 | 本波新增约 4 族形态：三重乘裸跑 / trade_when 门控 / bucket(vol) 条件化 / 年报水平 rank（门控窗 22/66 为同族变体） | 累计 ≥10 接近，但**互异性待审计**（裸跑与门控同载荷；水平探针为单字段 rank）——不单方面宣布达标 |
| D2 字段族自测 | IS 年度标量族 + 通用名 MATRIX 族零本地实测 | **本轮补上**：a_ebit/a_net_income/a_sales_rev_turn/total_liabilities_and_equity_value 各 1 条实测（臂7–10，LC 全 >0） | 增量达标；其余族（CF q、BS q_1/q_2、VECTOR 684 等）仍零实测 |
| D3 矩全家 | 水平✓ 一阶差✓ 比值✓ 二阶/分位✓（散在两波未逐项留痕） | 本波水平（臂7–10）/一阶差（臂1–5）/二阶波动条件化（臂6 ts_std_dev）各 ≥1 | **比值/SNR 腿本波零实测**——留痕仍不完整，判死引用前必须补 |
| D4 分组轴 ≥2 | industry+SUBINDUSTRY+sector 3 轴 | 本波 sector（group_rank）+ bucket（vol 分位 4 桶） | ✓（bucket/market 变体仍未扫） |
| D5 非线性 ≥1 | 仅 ts_rank 1 类 | **本轮补上 trade_when（臂3/4/5）+ bucket（臂6）** ⇒ 3 类 | ✓ 增量达标 |
| D6 配置 ≥2 | 中性化 2 套（SUBINDUSTRY/FAST）；宇宙/delay/decay 从未变 | 本波全臂单配置（SUBINDUSTRY）；撞件使臂 1 成 2026-11-05 点复读、零新配置样本 | **本波未增维**；7x 缺口实证强化 D6 处方轴优先级 |

结论：D1（互异性）/D3（留痕）/D6（本波零增量）未达 ⇒ 任何判死只能 provisional；本波亦不判死。

## §9 wave_results 共享行写库说明（w1 撞车处置）

- `wave_results` 表主键 = (region, wave_number)，**无 dataset 列**（`src/wqb/wave_results_contract.py:194` WHERE 子句实证）；w1 标签被 fnd86（早槽，行 id 2174，16:19:51）/ fnd72（本槽）共用。
- 处置按契约合并式协议（`wave_results_contract.py:18-19`「要追加请把原有条目一并传入」）：key_findings/candidates/batches **原 fnd86 条目逐字保留** + 追加以 `[fnd72]` 前缀标记的本槽条目；full_payload 保留 fnd86 原键原值 + 新增 `fundamental72` 键与 `waveLabelSharedNote` 键；focus/context **不传不覆写**（fnd86 原文保留）。
- verdict：两槽判定同值 PARTIAL（fnd86 n_pass≥0→PARTIAL 在库；fnd72 n_pass=0/n_near=1→PARTIAL），写入 PARTIAL 不改变单元格语义、不毁他槽结论。
- backtest_results / expressions 层面 w1 双集共存以 dataset 列区分（10+10 行，本槽只读核验通过）；跨层口径已在 key_findings 登记。
- 遗留风险（如实登记）：若 fnd86 槽后续对本行做整列覆写（未按契约追加），[fnd72] 条目会丢失——契约层面无 dataset 维度，双集共享单行是结构性限制，建议区域配置治理立项（不属本槽改动范围）。

## §10 证据通道与盲区登记

- 本档读数来源：ask 转录臂序读数（收割步骤⑥臂归属按平台 code 核验）+ 本轮实跑只读核验 `logs/_tmp_fnd72_w1_attr_verify.py`（backtest_results 10/10 行级一致）+ 实读 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md`、`tracking/DEU/config/thresholds.json`、`WAVE_w1_fundamental86_20261114.md`、`src/wqb/wave_results_contract.py`。
- `list_alphas_by_wave` 仅收整数 wave_number（兄弟槽 §8 同款缺口），w1 字符串波未走该通道，以 sqlite mode=ro 脚本替代复核（本轮实跑，10/10）。
- **臂 1 平台撞件** ⇒ 臂 1 读数为 2026-11-05 数据点复读，非本波新样本；波级有效新样本 = 9 臂。
- 相关性查询未做（单槽在相关性员，按 ask 边界）；LLKO3vZ9 的 prod/self 均未测（先测 prod 再扫参，归下槽）。
- 沿 ask 盲区：query_dataset_profile/query_field_profile 对 DEU 全 0 行（S0 档 §6）；expressions 表不含 MCP 直连仿真。
- 判读不改写邻接数据集先验：fnd45/fnd86/fnd89 结论未因本波变动；DEU 2Y 硬闸 1.58 引用 thresholds.json 原值。
