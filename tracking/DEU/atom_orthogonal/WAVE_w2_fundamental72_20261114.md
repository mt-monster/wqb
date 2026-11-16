# WAVE w2 — fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-14；归因员：atom_orthogonal 单槽（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 波标签：**w2 在 DEU 无撞车**（收割自报 + 本槽独立复核：wave_results 无 w2 行、backtest/expressions 仅本集 8 行）——与 w1 的 fnd86/fnd72 混标情形不同
- 配置（收割自报，全臂一致，同波1）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=4、trunc=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR
- 派发链（收割自报）：preflight 5 数据字段平台侧全部核实（含新探针字段 `fnd72_s_pit_or_is_a_is_oper_inc`）→ PLY validator 8/8 → **查重 8 臂全库零命中**（无波1 式平台撞件，8 条读数全部为本波新样本）→ multisim 8 臂 → 8/8 COMPLETE errors=0 → harvest（臂4 A1xJRrlY / 臂7 A1xJRr0l 相似 id 由平台 code 区分）→ upsert_backtest_rows n=8 → 只读复核
- **本槽只读核验（本轮实跑 `logs/_tmp_fnd72_w2_attr_verify.py`，sqlite mode=ro，零写入）**：backtest_results DEU/w2 恰 8 行全 fundamental72、alpha id 与臂表全对、sharpe/fitness/turnover/2Y/sub/LC/SC 逐行与臂序读数一致（**8/8 通过**）；expressions 8 行；wave_results 无 w2 行
- 判读基准（同波1 + 本槽前轮一手复核）：季度 IS delta 几何天花板 1.42（RREALzx0，FAST 格）；裸年报宽面天花板 0.37（wave107）；新自由度目标带 1.5–1.7；fnd45 量级参照 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，事实非承诺）；**2Y 硬闸 = 1.58**（`tracking/DEU/config/thresholds.json:5` two_year_sharpe_min）；sharpe_min 1.58（:14）/ fitness_min 1.0（:15）；sub<0.75 稳健告警；TO <20% 目标 / >25% 结构告警；死档 id 1573（年报面 rank(F) 探针 ≥50）/ 1575（TVR 层禁用）/ 1577（bf 窗 66）
- **波1 锚（跨波对照基线，`WAVE_w1_fundamental72_20261114.md`）**：LLKO3vZ9 rank(a_ebit) S 0.07/2Y 1.51/sub 0.39；qM7eVaEP rank(tle) S -0.16/2Y 0.99/sub 0.01；kqae9wJl rank(a_sales_rev_turn) 2Y 1.17；WjlKJZeZ rank(a_net_income) 2Y 0.93；季度族 trade_when 门控 22d 门 S 0.48–0.53 > 66d 门 0.44、2Y 全负（-0.31~-0.60）

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | 臂（缩写） | alphaId | S | F | 2Y | sub | TO | DD | margin | LC/SC | RA fail / 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | group_rank(bf66 a_ebit, sector) 形对照 | P05rJYOx | -0.27 | -0.11 | 0.04 | 0.38 | 1.32% | 26.86% | -0.003008 | 104/138 | 3 项；CLUSTER_TEST warning -0.46 |
| 2 | trade_when(δ66>0, 臂1载荷) | QP0r1NGG | 0.22 | 0.09 | 1.14 | 0.39 | 1.48% | 26.69% | 0.00255 | 63/62 | 4 项：+CW(0.5, limit 0.1, 2014-03-06)；risk_neut 0.55 |
| 3 | trade_when(δ22>0, 臂1载荷) | N1PWXJbE | 0.11 | 0.03 | 0.94 | 0.33 | 1.39% | 31.81% | 0.001287 | 63/62 | 4 项：+CW(0.5, 2014-03-06) |
| 4 | trade_when(δ66>0, group_rank(bf66 a_net_income,sector)) | A1xJRrlY | -0.14 | -0.04 | 0.76 | -0.10 | 1.54% | 32.14% | -0.001491 | 65/63 | 5 项：+CW(0.5, 2014-03-10) + LOW_SUB_UNIVERSE_SHARPE(-0.1, limit -0.07) |
| 5 | trade_when(δ66>0, group_rank(bf66 a_sales_rev_turn,sector)) | LLKbPm7M | **0.25** | 0.10 | 1.10 | 0.35 | 1.41% | 21.97% | **0.003106** | 66/65 | 4 项：+CW(0.5, 2014-03-10)；波内最佳 S/margin/DD |
| 6 | group_rank(bf66 tle, sector) 形对照 | lea6L58x | -0.47 | -0.25 | -0.16 | 0.11 | 1.16% | 42.65% | -0.005837 | 113/157 | 3 项；CLUSTER_TEST warning -0.75 |
| 7 | trade_when(δ66>0, 臂6载荷) | A1xJRr0l | 0.20 | 0.08 | 1.20 | 0.18 | 1.59% | 37.77% | 0.002466 | 69/69 | 4 项：+CW(0.5, 2014-03-03) |
| 8 | rank(a_is_oper_inc) 裸 rank 探针 | gJaqYgQl | 0.11 | 0.03 | **1.53** | 0.33 | 1.57% | 35.59% | 0.001083 | 76/79 | 3 项；存在性探针：LC+SC=155≥50 过死档 1573 主臂开门线 |

（臂 1/6 = group_rank 形对照；臂 2–5/7 = trade_when 门控；臂 8 = 新字段裸 rank 探针。全波无乘法/bucket 复合臂。）

## §2 逐臂归因条目

1. **臂1 P05rJYOx**（group_rank(bf66 a_ebit,sector) 形对照）：S -0.27 / 2Y 0.04。**跨波同字段对照**：波1 裸 rank LLKO3vZ9（同字段）S 0.07/2Y 1.51 → 本臂（+bf66+group_rank）S -0.27/2Y 0.04 ⇒ **group_rank 形同时杀 S（-0.34）与 2Y（-1.47）**。符号：负 margin 与 IS delta 先验无冲突（非 delta 结构）；无翻转对，衰减对称未实测。CLUSTER_TEST warning -0.46 登记。宽度 104/138 健康。TO 1.32%。
2. **臂2 QP0r1NGG**（δ66 门控 a_ebit）：**波内归因对照成立**——门控把 S 从形对照 -0.27 提到 0.22（+0.49）、2Y 从 0.04 复活到 1.14（+1.10）。但 2Y 1.14 < 波1 裸锚 1.51 < 闸 1.58（**距闸 0.44 出线**，边界登记）⇒ **门控复活 2Y 成功、推 2Y 过闸失败**（fnd90「门控推 2Y」先验在本族的第一条证伪读数）。CW 0.5 FAIL（2014-03-06）：宽度 63/62 健康 ⇒ **结构层指纹（门控集中）非数据层**。risk_neut 0.55 > S 0.22 ⇒ 风险中性化后增强（非风险因子套利形态）。
3. **臂3 N1PWXJbE**（δ22 门控 a_ebit）：S 0.11 / 2Y 0.94。**窗对照：66d 门（0.22/1.14）> 22d 门（0.11/0.94）**——与波1 季度族（22d 门 S 0.48–0.53/2Y -0.31~-0.34 优于 66d 门 0.44/-0.60）**方向相反**；收割自报「窗 66>22 与波 1 季度族方向同」与本槽对波 1 读数的核对不符，差异如实登记不静默改写 ⇒ 窗维族间不稳定、效应弱（ΔS 0.11/Δ2Y 0.20），不入杠杆。CW 0.5 FAIL 同指纹。
4. **臂4 A1xJRrlY**（δ66 门控 a_net_income）：S -0.14 / 2Y 0.76 / **sub -0.10 = 全波唯一平台 sub 闸实挂**（LOW_SUB_UNIVERSE_SHARPE，value -0.1 vs limit -0.07；与本地 thresholds.json:21 sub_universe_sharpe_min=1.0 是两个口径，原样转录）+ CW 0.5 FAIL。跨波对照：裸 rank（波1）S -0.01/2Y 0.93 → 门控 S -0.14/2Y 0.76 ⇒ **门控对该族无增益反退化；net_income 族双形死**（S/2Y/sub 三面全弱）。
5. **臂5 LLKbPm7M**（δ66 门控 a_sales_rev_turn）：**S 0.25 波内最佳** / F 0.10 / margin 0.003106 波内最佳 / DD 21.97% 波内最低 / 2Y 1.10。跨波：裸 rank（波1）2Y 1.17 → 门控 1.10（≈平）；S -0.04→0.25（门控提 S）。2Y 距闸 0.48 出线。CW 0.5 FAIL 同指纹。本波相对最优结构，但绝对值距 S 闸 1.33。
6. **臂6 lea6L58x**（group_rank(bf66 tle,sector) 形对照）：S -0.47 全波最低 / 2Y -0.16 / sub 0.11 / CLUSTER_TEST warning -0.75。**跨波同字段第二对对照**：裸 rank（波1）S -0.16/2Y 0.99 → 本臂 S -0.47/2Y -0.16 ⇒ group_rank 形杀 S 与 2Y 在 tle 上同向复现（与臂1 构成 2/2 一致形态对）。LC 113/SC 157 全波最宽（宽度健康）。
7. **臂7 A1xJRr0l**（δ66 门控 tle）：S 0.20 / 2Y 1.20 / sub 0.18 / LC 69/SC 69。波内对照：S -0.47→0.20、2Y -0.16→1.20（门控复活）。跨波：**唯一 2Y 超裸锚的门控臂**（裸 0.99 → 门控 1.20），但距闸 0.38 险入近闸、sub 0.18 极弱、CW 0.5 FAIL。near-gate#1（按 S 降序；2Y 载体非 S 候选）。
8. **臂8 gJaqYgQl**（rank(a_is_oper_inc) 裸 rank 探针）：LC 76/SC 79、**LC+SC=155≥50 ⇒ 存在性正向证据 + 波 3 主臂开门线通过**（死档 1573 协议）。S 0.11 / **2Y 1.53——距 2Y 硬闸 1.58 仅 0.05，全战役最近闸读数**；裸 rank 锚形态跨波复现（a_ebit 波1 1.51 → a_is_oper_inc 波2 1.53）。near-gate#2（2Y 载体）。sub 0.33。

## §3 指纹 / 铁律 / 跨区核对汇总

- **符号指纹**：无反向臂 ⇒ **衰减对称两波累计未实测**（如实登记）。符号结构：形对照双负（-0.27/-0.47）→ 门控后 4/5 转正（仅 net_income 门控 -0.14 保持弱负）——门控构造为「水平改善→持多」，与 IS delta 符号先验（盈利改善→做多）同向；符号翻转是条件化效应非符号错。|S| 全部 ≤0.47（噪声-弱带），无单向事件型指纹判定成立。
- **稀释铁律**：本波**零复合形态**（无乘法/bucket 臂，全部单腿）⇒ 铁律无触发条件、不适用。group_rank vs rank vs 门控的对照属**形态对照**，不属稀释铁律范畴，按跨波形对照登记（§2.1/§2.6）。
- **跨区不外推**：零 TWN 引用；**fnd90「门控推 2Y 过闸」先验在本族族级证伪**（5/5 门控臂 2Y 0.76–1.20 < 1.58）——只登记本族读数，不改写 fnd90/fnd45 等邻接集先验。
- **波级聚合**：sub 0.11–0.39 八臂全部 <0.75 告警线（**两波累计 18/18 臂 <0.75 @SUBINDUSTRY 格**）；TO 1.16–1.59% 全部远低于 20% 线（门控+年报慢变量持仓极慢；亦低于死档 1575 的年报面 TO 基线 11.92%）；**CW 恒 0.5 结构指纹 5/5**（value 恒定、date 集中于 2014-03-03/06/10 三日）。

## §4 绿芽（sprouts）/ 死轴（deadAxes）

**绿芽**：
1. **年报 IS 水平裸 rank 的 2Y 锚跨波复现且贴闸**：a_ebit 波1 1.51 → a_is_oper_inc 波2 **1.53（距闸 0.05，全战役最近）**；两字段裸 rank 形 2Y 稳定 1.5±0.02 而 S 面 0.07–0.11 死 ⇒ 「2Y 闸位载体」形态（非 S 候选）。
2. **门控 2Y 复活增益（波内对照）**：形对照 2Y 0.04/-0.16 → 门控 0.76–1.20（5 臂全部复活）；复活实、过闸败（全部 <1.58，除 tle 外均低于各自裸锚）。
3. **门控 S 方向性增益（波内对照）**：形对照 -0.27/-0.47 → 门控 -0.14~+0.25；臂5 同帧拿到波内最佳 S/margin/DD 三项。
4. **臂8 开门线通过（LC+SC=155≥50）⇒ 波 3 a_is_oper_inc 族主臂派发前置满足**（死档 1573 协议）。

**死轴**：
1. **年报水平 × sector group_rank 形（无门控）**：S -0.27/-0.47、2Y 0.04/-0.16 ⇒ 形级死轴；跨波同字段对照 2/2 同向（a_ebit 1.51→0.04、tle 0.99→-0.16）。
2. **「trade_when 门控推 2Y 过闸」假设族级证伪**：5 门控臂 2Y 0.76–1.20 全部 <1.58，4/5 低于各自裸 rank 锚（仅 tle 1.20>0.99）；fnd90 先验方向在本族不成立。
3. **net_income 年报族双形死**：裸 rank（波1）S -0.01/2Y 0.93 + 门控（波2）S -0.14/2Y 0.76/唯一 sub 闸实挂 ⇒ 族级 S/2Y/sub 三面全弱，降权。
4. **trade_when 门控 CW=0.5 恒定结构指纹**：5/5 门控臂同挂（宽度 62–69/侧健康 ⇒ 非数据层）——年报慢变量上门控集中度系统性不过 CW 闸，门控形在年报族的铁死法（不解集中度前，门控形年报臂默认带此死法）。

## §5 数据层排除判读（口径区分）

- **本波无 data_excluded 臂**：LC 63–113 / SC 62–157 全部健康，无宽度塌缩；死档 1573 的「宽度≤5 必挂」形态两波累计未出现。
- CW=0.5 FAIL（5/5 门控臂）：结构层指纹（trade_when 门控集中，value 恒 0.5），**非数据层排除**——登记口径与数据层严格区分；按 ask 纪律不改符号重试。
- 臂4 LOW_SUB_UNIVERSE_SHARPE(-0.1, limit -0.07)：平台 sub 闸实挂（与本地 thresholds.json:21=1.0 两个口径），原样转录。
- 臂8 探针：存在性判断成立（LC>0），per 探针协议不作覆盖度读数；开门线通过 ⇒ 波 3 主臂前置满足。

## §6 nearGateCandidates（≤2，按 S 降序；先测 prod 再扫参——prod 雷在核心不在搭档）

| alphaId | 臂 | 触发 | 读数（原样） |
|---|---|---|---|
| A1xJRr0l | 臂7 | 2Y 1.20 距 2Y 硬闸 1.58（thresholds.json:5）差 **0.38 ≤0.4**；S 0.20 不达 S≥1.2，近闸资格来自 2Y 轴 | S=0.20/F=0.08/2Y=1.20/sub=0.18/TO=1.59%/DD=37.77%/LC=69/SC=69；CW 0.5 FAIL |
| gJaqYgQl | 臂8 | 2Y 1.53 距 2Y 硬闸 1.58 仅 **0.05**（全战役最近闸读数）；裸 rank 锚形态跨波复现；S 0.11 不达 S≥1.2 | S=0.11/F=0.03/2Y=1.53/sub=0.33/TO=1.57%/DD=35.59%/margin=0.001083/LC=76/SC=79 |

- 边界登记：臂2 QP0r1NGG 2Y 1.14 距闸 0.44、臂5 LLKbPm7M 1.10 距闸 0.48——均 >0.4 出线（与波1 臂9 0.41 出线同口径）。
- CW 0.5 挂（5/5）：超限 0.4 且为恒定形态死法（指纹非边缘 miss），不作近闸触发（与波1 臂3/5 处理一致）。
- ⚠ 两候选均为 **2Y 轴载体非 S 达标候选**（S 0.11–0.20/F 0.03–0.10 距 fitness_min 1.0 ≥0.9）：prod 测序意义 = 按 §7.5 收割优先核对 prod/self 占用，**不是提交链候选**；若推进，方向是 2Y 闸位的配置轴/形态轴表达（波1 中性化 7x 缺口对照）。

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = provisional（判弱入档，两波连续）**。依据（全部为本波+波1 读数）：
1. S 面 @SUBINDUSTRY 格系统性弱：两波 18 臂 best S 0.68（波1 bucket 条件化）→ 0.25（本波门控），全部低于 fnd45 量级基线 0.96 与目标带 1.5–1.7；本波 8/8 RA fail。
2. 设计假设族级证伪：波2 主假设「trade_when 门控推年报水平 2Y 过闸」5/5 失败（0.76–1.20 < 1.58，4/5 低于裸锚）；波1 的季度族门控跷跷板同样未过闸——条件化路径两族皆未产出过闸读数。
3. 活体仅剩 2Y 裸锚形态（1.51/1.53，S 死）与未扫自由度：配置轴（FAST 7x 对照，DB 既有点）、比值/SNR 腿（D3 缺口）、CF/BS q 族等未测字段——这些是**下波设计输入**，不构成本波升级 active 的读数。
4. 判死六维闸仍未满足（§8：D1 互异性/D3 比值腿/D6 配置维）⇒ 按 AGENTS §7.6 缺任一维只能 provisional；判死依据=读数，本波读数不支持任何死（无宽度塌缩、有贴闸活体、有未扫维度）⇒ 不判死、不封集、不 data_excluded。
5. **mode_b_qualification 张力再登记**（thresholds.json:23-27，best 0.25/0.10 远低于 1.25/0.8 资格线）：判死分支不采用——AGENTS §7.6（2026-11-10）+ 波1 同日先例（fnd86 槽 active / 本集 provisional 均未触发该分支）；冲突留区域配置治理。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 near ⇒ PARTIAL；n_pass=0 / n_near=2：A1xJRr0l、gJaqYgQl）。w2 行为 clean insert（无撞车）。

## §8 判死六维闸盘点（两波累计，对照 S0 档 §3.2 基线）

| 维 | 累计现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 两波形态族：三重乘裸跑 / trade_when 门控乘 / bucket(vol) 条件化 / 年报裸 rank / 年报 group_rank 形 / 年报门控 group_rank 形 / 裸 rank 探针 ≈ 7 族 | <10，互异性待审计（门控与形对照同载荷）——不单方面宣布达标 |
| D2 字段族自测 | 累计实测 7 字段：q_ebit/q_is_oper_inc（波1）/a_ebit/a_net_income/a_sales_rev_turn/a_is_oper_inc/tle（波1–2） | 增量达标；CF 族/BS q_1q_2/VECTOR 684 仍零实测 |
| D3 矩全家 | 水平✓（两波）/一阶差✓（波1）/二阶波动条件化✓（波1） | **比值/SNR 腿两波零实测** ✗——判死引用前必须补 |
| D4 分组轴 ≥2 | sector/bucket（波1）+ SUBINDUSTRY 配置 | ✓（bucket 变体未扫） |
| D5 非线性 ≥1 | ts_rank/trade_when/bucket 3 类 | ✓ |
| D6 配置 ≥2 | 两波全臂单配置（SUBINDUSTRY/decay4）；FAST 对照为 DB 既有点非本战役实测 | **✗ 未增维**——7x 缺口实证下 D6 是最高优先未扫轴 |

结论：D1/D3/D6 未达 ⇒ 任何判死只能 provisional（本波亦不判死）。

## §9 newLever 登记（跨波实证 + 归因对照链）

**形态-2Y 杠杆（本波新入册）**：年报 IS 水平信号的 2Y 轴由形态决定——
- 裸 rank 形**保 2Y**：a_ebit 波1 LLKO3vZ9 1.51 / a_is_oper_inc 波2 gJaqYgQl 1.53（跨波 2 字段复现，2Y 1.5±0.02）；
- group_rank(+bf66) 形**灭 2Y**：跨波同字段对照 2/2 同向（a_ebit 1.51→波2 P05rJYOx 0.04；tle 波1 0.99→波2 lea6L58x -0.16）；
- trade_when 门控（同 bf66+group_rank 底）**复活但封顶**：0.94–1.20，全部不过 1.58 闸、4/5 低于各自裸锚 ⇒ **杀手在 group_rank 形而非 bf66**（门控臂同带 bf66 仍复活 2Y）。
- 归因对照：同字段跨波对（a_ebit/tle）+ 波内门控分解（同 bf66 底、仅差门控）三层对照。
- ⚠ caveat：跨波对照的形差捆绑两变量（bf66+group_rank），单变量归因靠波内门控分解支撑（间接）；bf66 为死档 1577 基线窗，先验上不动年报水平信号。
- 设计含义：下波 2Y 闸位设计用裸 rank 形；S0 处方「分组轴主用 sector」对 **2Y 轴**不成立（对 S 面的结论不变，本波未测 sector 对 S 的独立效应）。

## §10 证据通道与盲区登记

- 本档读数来源：ask 转录臂序读数（收割步骤⑥臂归属按平台 code 核验，臂4/臂7 相似 id 已区分）+ 本轮实跑只读核验 `logs/_tmp_fnd72_w2_attr_verify.py`（8/8 行级一致、w2 无撞车）+ 实读 `WAVE_w1_fundamental72_20261114.md`（波1 锚）、`tracking/DEU/config/thresholds.json`（前轮一手）、`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md`。
- 查重通道：收割步骤③全库零命中（expressions+alphas）⇒ 8 读数全部本波新样本（无波1 式撞件复读）。
- 相关性查询未做（单槽在相关性员）；两近闸载体的 prod/self 未测（先测 prod 再扫参，归下槽）。
- 沿 ask 盲区：query_dataset_profile/query_field_profile 对 DEU 全 0 行；expressions 表不含 MCP 直连仿真。
- 收割注记差异登记：窗 66/22「与波 1 季度族方向同」与本槽核对不符（§2.3），两族方向相反。
- 判读不改写邻接数据集先验：fnd45/fnd86/fnd89/fnd90 结论未因本波变动（fnd90 先验在本族的证伪只登记在本族名下）。
