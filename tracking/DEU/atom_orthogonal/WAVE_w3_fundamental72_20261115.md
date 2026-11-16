# WAVE w3 — fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-15；归因员：atom_orthogonal 单槽（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 波标签：**w3 在 DEU 无撞车**（收割自报 + 本槽独立复核：wave_results 无 w3 行、backtest/expressions 仅本集 7 行）
- 配置（收割自报，全臂一致，同波1/2）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=4、trunc=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR
- 派发链（收割自报）：preflight 6 数据字段平台侧全部核实（含 3 个新探针字段 `cf_a_cf_cash_from_oper` / `cf_a_cf_net_inc` / `bs_q_1_bs_tot_asset`）→ PLY validator 7/7 → **查重 7 臂全库零命中**（7 读数全部本波新样本）→ multisim 7 臂 → 7/7 终态 **errors=1（臂 6 child status=WARNING：UNITS 告警）** → harvest 7/7（归属按平台 code 核对）→ upsert_backtest_rows n=7 → 只读复核
- **臂 6 WARNING 处置（沿收割自报，本槽不改判）**：batch_status 报 WARNING + 平台错误文本（`Incompatible unit for input of "group_backfill" at index 0, expected "Unit[]", found "Unit[TSPrice:1]"`），但平台实际完成仿真：RReqRmza 为真实 alpha、全量 IS 指标在册（S -0.35/2Y 0.84/sub -0.30），UNITS 落在 checks.warning 桶（非 RA 项）；非 ERROR/CANCELLED 连坐 ⇒ 波级不判 rebuild_needed；**同构臂 5（a_ebit，无单位）无此告警 ⇒ 单位差为 tle 字段特有**；臂 6 读数可用性（gBF 在价格单位场输入上是否语义有效）待评审裁定——本档按「低可靠+UNITS 缠绕」口径引用臂 6，不以其构建符号/机制结论
- **本槽只读核验（本轮实跑 `logs/_tmp_fnd72_w3_attr_verify.py`，sqlite mode=ro，零写入）**：backtest_results DEU/w3 恰 7 行全 fundamental72、alpha id 与臂表全对、sharpe/fitness/turnover/2Y/sub/LC/SC 逐行与臂序读数一致（**7/7 通过**，含 RReqRmza sub=-0.3、j2aW26G5 2Y=1.16 两处关键值）；expressions 7 行；wave_results 无 w3 行
- 判读基准（同波1/2 + 前轮一手复核）：S 天花板 1.42（RREALzx0，FAST 格）；裸年报宽面 0.37（wave107）；目标带 1.5–1.7；fnd45 参照 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，事实非承诺）；**2Y 硬闸 = 1.58**（`tracking/DEU/config/thresholds.json:5`）；sharpe_min 1.58（:14）/ fitness_min 1.0（:15）；sub<0.75 稳健告警；TO <20% / >25% 告警；死档 1573/1575/1577
- **波1/波2 锚（跨波对照基线，`WAVE_w1_fundamental72_20261114.md` / `WAVE_w2_fundamental72_20261114.md`）**：LLKO3vZ9 rank(a_ebit) S 0.07/2Y 1.51/sub 0.39；w2 门控 group_rank 形 QP0r1NGG（a_ebit）S 0.22/2Y 1.14/CW 0.5、A1xJRr0l（tle）S 0.20/2Y 1.20/sub 0.18/CW 0.5；裸 IS 年报锚 gJaqYgQl 2Y 1.53；波2 杠杆「形态-2Y：裸 rank 保 2Y / group_rank 灭 2Y / 门控复活封顶」

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | 臂（缩写） | alphaId | S | F | 2Y | sub | TO | DD | margin | LC/SC | RA fail / 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rank(cf_a_cf_cash_from_oper) 探针 | xAv9AN2m | 0.15 | 0.05 | 0.59 | 0.40 | 1.57% | 22.34% | 0.001498 | 75/78 | 3 项；CLUSTER_TEST warning 0.0 |
| 2 | rank(cf_a_cf_net_inc) 探针 | 6XM3XpoK | -0.0 | -0.0 | 0.94 | 0.16 | 1.62% | 40.10% | -0.00004 | 76/79 | 3 项 |
| 3 | rank(bs_q_1_bs_tot_asset) 探针 | YPanPvEJ | -0.39 | -0.20 | 0.62 | -0.13 | 1.39% | **51.77%** | -0.004854 | 70/73 | 3 项；CLUSTER_TEST warning -0.59 |
| 4 | rank(is_q_ebit) 季度×水平格探针 | j2aW26G5 | 0.13 | 0.04 | 1.16 | 0.30 | 2.75% | 29.63% | 0.000749 | 66/68 | 3 项 |
| 5 | trade_when(δ66>0, rank(group_backfill(bf66 a_ebit,250,sector))) gBF 修复臂 | zqdQqNG1 | 0.09 | 0.02 | 0.86 | 0.27 | 1.37% | 27.28% | 0.001133 | 59/66 | 4 项：+CW(0.5, limit 0.1, 2014-03-06)；gBF 叠层后 CW 仍 FAIL 0.5 |
| 6 | trade_when(δ66>0, rank(group_backfill(bf66 tle,250,sector))) gBF 修复臂 | RReqRmza | -0.35 | -0.19 | 0.84 | -0.30 | 1.44% | **58.51%** | -0.004867 | 65/73 | 5 项：+CW(0.5, 2014-03-03) + LOW_SUB_UNIVERSE_SHARPE(-0.3, limit -0.17)；⚠UNITS 告警（tle 价格单位场），simStatus=WARNING，IS 指标在册 |
| 7 | group_neutralize(rank(a_ebit), bucket(rank(ts_std_dev(a_ebit,1008)), 4桶)) | ZYaqYEzn | **0.21** | 0.08 | 0.70 | **0.43** | 2.51% | 24.54% | 0.001422 | 80/69 | 3 项；本波最佳 S/sub |

（臂 1–4 = 存在性探针；臂 5/6 = gBF 修复臂；臂 7 = group_neutralize 收尾轴。全波无信号复合臂——bucket 在臂 7 为中性化轴非信号组合。）

## §2 逐臂归因条目

1. **臂1 xAv9AN2m**（CF cash_from_oper 年报水平探针）：LC 75/SC 78、LC+SC=153≥50 ⇒ **数据在 + 波 4 主臂开门线通过**。S 0.15 噪声带弱正、2Y 0.59 <1.0 ⇒ 记「机制需条件化」指纹不记死（S0 基准）。符号与现金流 higher=better 直觉同向（弱）；无翻转对。CLUSTER_TEST warning 0.0 原样登记。**本字段属死档 1573 允许族（BS 主表 + cf_net_inc + cf_cash_from_oper）**——主线宽度 75–79/侧进一步证实 1573 的 cov<2% 排除确指 CF/BS 明细字段，非主线。
2. **臂2 6XM3XpoK**（CF net_inc 年报水平探针）：LC 76/SC 79、LC+SC=155≥50 ⇒ 数据在 + 开门线过。S -0.0 平坦（水平净利润排序零信号）；2Y 0.94 <1.0 需条件化指纹；sub 0.16 弱。同属 1573 允许族。符号平坦不构成方向证据。
3. **臂3 YPanPvEJ**（BS q_1 tot_asset 水平探针）：S -0.39 **本波最大 |S|** / 2Y 0.62 / sub -0.13 / DD 51.77% 全波最高 / CLUSTER_TEST warning -0.59。LC 70/SC 73、143≥50 ⇒ 数据在 + 开门线过。**符号方向未决**：资产水平无 higher=better 先验（类规模因子），负 S 可读「小资产占优」但无翻转对、不判符号错也不判机制；该字段为平台高拥挤位（uc 17/ac 30，S0 档 §3.1 头部表）⇒ 拥挤+弱负，低优先。若启用 asset 轴须先跑反向臂作符号判别。
4. **臂4 j2aW26G5**（季度 q_ebit 水平探针，新格）：LC 66/SC 68、134≥50 ⇒ 数据在 + 开门线过。S 0.13 / **2Y 1.16——距 2Y 硬闸 1.58 差 0.42，出线 0.02**（边界如实登记，不入 near-gate）。**ebit 族 2Y 阶梯跨波补全**：年报水平 1.51（波1）> 季度水平 1.16（本波）> 季度 delta 复合 0.12–0.21（波1）——「水平保 2Y、delta 杀 2Y」在季度/年度两粒度一致，为波2 形态-2Y 杠杆的增量证据。
5. **臂5 zqdQqNG1**（gBF 修复臂，a_ebit）：S 0.09 / 2Y 0.86 / sub 0.27 / CW **仍 FAIL 0.5**（2014-03-06）。**跨波同字段同门控干净对照**（vs 波2 QP0r1NGG：同 δ66 门、同 bf66 a_ebit，载荷 group_rank → rank∘group_backfill）：S 0.22→0.09（-0.13）、F 0.09→0.02、2Y 1.14→0.86（-0.28）、sub 0.39→0.27，**CW 0.5→0.5 未解**。⇒ 双重归因：①gBF 叠层在门控年报臂上是**纯退化**；②**CW=0.5 是门格结构属性，与载荷形无关**（gBF 归因读数，CW PASS 预期未实现——设计注记预测落空，如实登记）。⚠ 波2 杠杆处方的「裸 rank 门控形」仍未派发（本臂为 gBF 修复尝试，载荷仍带 sector 分组）。
6. **臂6 RReqRmza**（gBF 修复臂，tle）：S -0.35 / 2Y 0.84 / **sub -0.30 平台 sub 闸实挂**（-0.3 vs limit -0.17）/ DD 58.51% 全波最高 / CW 0.5 FAIL / **⚠UNITS 告警**（gBF 期望 Unit[] 实得 Unit[TSPrice:1]——tle 为价格单位场）。跨波对照（vs 波2 A1xJRr0l 同字段同门控 group_rank 形）：S 0.20→-0.35、2Y 1.20→0.84、sub 0.18→-0.30——退化方向与臂5 一致，**但本对缠绕 UNITS 告警（gBF 在价格单位场输入上语义存疑）⇒ 退化归因不纯净，读数低可靠**，不作符号/机制证据；可用性（是否需 rank 去量纲重建）待评审。tle 族三形态累计：裸 rank（波1）S -0.16/2Y 0.99、门控 group_rank（波2）S 0.20/2Y 1.20、门控 gBF（本波）S -0.35/2Y 0.84+UNITS——族级全面降权。
7. **臂7 ZYaqYEzn**（group_neutralize 收尾轴）：S 0.21 本波最佳 / F 0.08 / 2Y 0.70 / **sub 0.43 本波最佳** / TO 2.51%。**同载荷跨波干净对照**（vs 波1 LLKO3vZ9，payload 同为 rank(a_ebit)，± vol-bucket group_neutralize）：S 0.07→0.21（+0.14）、sub 0.39→0.43（+0.04）、**2Y 1.51→0.70（-0.81，近半）**。**稀释铁律核过：S 0.21 > 单腿 0.07 ⇒ 不触发稀释**；2Y 代价单列 ⇒ S-2Y 取舍形态（vol-bucket 中性化 = S/sub 微增益换 2Y 半价）。跨族旁证（波1）：vol-bucket 作分组轴时同样提 S（0.20→0.68，季度复合载荷）——「vol-bucket 提 S 压 2Y」两族 2/2 同向，但算子角色不同（分组 vs 中性化）、幅度不同（+0.48 vs +0.14），仅作刻画不入杠杆。

## §3 指纹 / 铁律 / 跨区核对汇总

- **符号指纹**：三波累计无反向臂 ⇒ **衰减对称未实测**（如实登记）。本波符号面：探针 +0.15/-0.0/-0.39/+0.13、修复臂 +0.09/-0.35（UNITS 缠绕不作符号证据）、收尾轴 +0.21——全部噪声-弱带（|S| ≤0.39），无单向事件型指纹判定；臂3 资产水平负读数**方向未决**（无先验、无翻转对）。CW 挂（臂5/6）= 结构指纹，按纪律不改符号重试。
- **稀释铁律**：本波唯一复合形态 = 臂7（group_neutralize + vol-bucket），对应单腿 = 裸 rank(a_ebit)（波1 LLKO3vZ9 S 0.07）：**0.21 > 0.07 ⇒ 不稀释**（2Y 代价非铁律范畴，单列取舍刻画）；臂5/6 为单字段载荷非信号复合。全波无乘法/bucket-信号组合臂。
- **跨区不外推**：零 TWN 引用；全部对照为 DEU 域内跨波/波内（波1/波2 锚、fnd45 量级参照）；fnd90/fnd45/fnd86/fnd89 先验未因本波改写。
- **波级聚合**：sub 0.43 ~ -0.30 八臂…7 臂全部 <0.75 告警线（**三波累计 25/25 臂 <0.75 @SUBINDUSTRY 格**）；TO 1.37–2.75% 全部远低于 20% 线；**CW=0.5 跨载荷形 7/7**（波2 group_rank 5/5 + 波3 rank∘gBF 2/2）。

## §4 绿芽（sprouts）/ 死轴（deadAxes）

**绿芽**：
1. **4 探针存在性全正向且开门线全过**（LC+SC 134–155 ≥50）：CF 主线 cash_from_oper 153、net_inc 155、BS 主表 q_1 tot_asset 143、季度水平 q_ebit 134 ⇒ **波 4 主臂派发前置满足**（4 族）；并实证死档 1573 的 cov<2% 排除确指明细字段，主线宽度健康。
2. **ebit 族 2Y 阶梯跨波补全**：年报水平 1.51 > 季度水平 1.16 > 季度 delta 复合 0.12–0.21（全 SUBINDUSTRY 格）⇒ 「水平保 2Y、delta 杀 2Y」跨粒度一致（波2 杠杆增量证据）。
3. **vol-bucket 收尾轴的 S/sub 微增益**（臂7 同载荷对照 +0.14/+0.04）——S 攻坚形的可选收尾（代价 2Y 半价，见死轴 4）。
4. **CW=门格属性的跨波跨形 7/7 一致**（波2 group_rank 5/5 + 波3 rank∘gBF 2/2 同挂 0.5）——把 CW 修复方向从「载荷形替换」（已证死路）收敛到「门格/持仓层」，缩小下波修复搜索空间。

**死轴**：
1. **gBF 修复路径**：CW 未解（2/2 仍 0.5）+ S/2Y/sub 全面退化（a_ebit 干净对 -0.13/-0.28/-0.12）⇒ 载荷形替换修 CW 是死路；CW=门格结构属性。
2. **tle 族（含 UNITS 层缺陷）**：三形态 S -0.16/+0.20/-0.35 全弱 + 波3 sub -0.30 实挂 + UNITS 告警（价格单位场上 gBF 语义存疑，读数低可靠）⇒ 族级降权 + 数据格式缺陷登记；启用前必须先解决单位语义（rank 去量纲或换字段）。
3. **CF/BS 主线裸水平 rank 的 S 面**：0.15/-0.0/-0.39/+0.13 全噪声-弱带、2Y 0.59–1.16 未达近闸带 1.43–1.58 ⇒ 主线裸水平形无活体；**2Y 活体目前仅年报 IS 两字段**（a_ebit 1.51 / a_is_oper_inc 1.53，波1/波2 在册）。
4. **vol-bucket 中性化的 2Y 代价**（臂7 同载荷对照 2Y 1.51→0.70）：S 攻坚形可用、2Y 闸位形禁用——与波2 杠杆（裸 rank 保 2Y）合成完整的形态-2Y 选择规则。
5. **BS q_1 tot_asset 方向未决**：S -0.39 最大 |S| 但无先验无翻转对、高拥挤（uc 17/ac 30）、DD 51.77% 最高 ⇒ 不判符号错不判机制，记「方向未决待判别」低优先。

## §5 数据层排除判读（口径区分）

- **本波无 data_excluded 臂**：LC 59–80 / SC 66–79 全部健康（最窄臂5 59/66 仍远超塌缩线）；死档 1573 的「宽度≤5 必挂」形态三波累计未出现。
- CW=0.5 FAIL（臂5/6）：**门格结构属性**（跨载荷形 7/7 一致），非数据层排除——登记口径区分。
- 臂6 UNITS 告警：**数据格式层缺陷**（tle 价格单位场 × gBF 语义），非宽度塌缩、非信号死——读数低可靠标注，修复路径 = rank 去量纲重建或换字段（归评审裁定）。
- 4 探针开门线全过（134–155 ≥50）⇒ 波 4 主臂前置满足：cf_cash_from_oper / cf_net_inc / bs_q_1_bs_tot_asset / 季度水平格。

## §6 nearGateCandidates（≤2，按 S 降序；先测 prod 再扫参）

**本波为空**——无一臂距任一硬闸 ≤0.4：
- S 闸 1.58：max S 0.21（距 1.37）；F 闸 1.0：max F 0.08（距 0.92）；
- 2Y 闸 1.58：臂4 1.16 距 **0.42 出线 0.02**（边界如实登记；与波1 臂9 0.41、波2 臂2 0.44 同口径）；其余 0.59–0.94 距 0.64–0.99；
- CW 0.5 挂（臂5/6）：恒定形态死法（指纹非边缘 miss），不作近闸触发（波1/波2 同口径）。
- 判定表后果：n_pass=0 / n_near=0 ⇒ **波 verdict=FAIL**（0 达标 0 near，机械结果；与波1/波2 PARTIAL 相比降档，归因=本波无条件化增益形且无近闸臂）。

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = provisional（判弱入档，三波连续）**。依据（全部为三波读数）：
1. S 面 @SUBINDUSTRY 格三波系统性弱：best S 0.68（波1 bucket 条件化）→ 0.25（波2 门控）→ 0.21（波3 中性化收尾），25 臂全部 RA fail；三波均未产出 S≥0.7 的新形。
2. 修复路径逐一证伪：门控推 2Y 过闸（波2，5/5 败）→ gBF 修 CW（波3，2/2 败且纯退化）——两条设计假设均被同字段对照干净否定。
3. 活体仅剩：2Y 裸锚形态（1.51/1.53，S 死）+ 4 族主臂开门线（探针 S 面 0.15~-0.39 全弱，主臂期望值低）；未扫自由度：配置轴（FAST 7x 对照）、比值/SNR 腿（D3）、宇宙/delay、裸 rank 门控形（波2 杠杆处方未执行）。
4. 判死六维闸仍未满足（§8：D1 互异性/D3 比值腿/D6 配置维）⇒ 按 AGENTS §7.6 只能 provisional；且本波 7 臂 <10 探针条款下更不产生判死；判死依据=读数，本波读数不支持任何死（开门线全过、有未扫维度、2Y 载体在册）⇒ 不判死、不封集、不 data_excluded。
5. **mode_b_qualification 张力三连登记**（thresholds.json:23-27，best 0.21/0.08 远低于 1.25/0.8）：判死分支不采用——AGENTS §7.6（2026-11-10）+ 同日三槽先例；冲突留区域配置治理。

**波 verdict = FAIL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 0 near ⇒ FAIL/RED；n_pass=0 / n_near=0）。w3 行 clean insert（无撞车）。

## §8 判死六维闸盘点（三波累计）

| 维 | 累计现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义形态 ~10（三重乘/门控乘/bucket 条件化/年报裸 rank/group_rank 形/门控 group_rank 形/裸 rank 探针/gBF 修复形/vol-bucket 中性化/CF·BS 主线裸 rank） | **互异机制仅 ~5**（动量 delta 复合 / 水平排位 / 波动条件化 / 门控事件子集 / 中性化收尾）——多数为同机制载荷形变体 ⇒ 未达 |
| D2 字段族自测 | 累计 10 字段：q_ebit/q_is_oper_inc/a_ebit/a_net_income/a_sales_rev_turn/a_is_oper_inc/tle/cf_cash_from_oper/cf_net_inc/bs_q_1_bs_tot_asset | 主线族已覆盖；CF/BS 明细、VECTOR 684、其余有足迹字段仍零实测 ⇒ 未达 |
| D3 矩全家 | 水平✓ 一阶差✓ 二阶波动✓（条件化/中性化） | **比值/SNR 腿三波零实测** ✗ |
| D4 分组轴 ≥2 | sector/bucket/SUBINDUSTRY 配置 | ✓ |
| D5 非线性 ≥1 | ts_rank/trade_when/bucket/group_neutralize 4 类 | ✓ |
| D6 配置 ≥2 | 三波全臂单配置（SUBINDUSTRY/decay4） | **✗ 未增维**——FAST 7x 对照在册，最高优先未扫轴 |

结论：D1/D3/D6 未达 ⇒ 任何判死只能 provisional（本波亦不判死）。

## §9 newLever 登记（跨波实证 + 归因对照链）

**gBF/CW 反证杠杆（本波新入册）**：trade_when 门控年报臂的 CONCENTRATED_WEIGHT=0.5 是**门格结构属性、与载荷形无关**——
- 证据链：波2 group_rank 载荷 5/5 挂 0.5 + 波3 rank(group_backfill) 载荷 2/2 仍挂 0.5（跨波跨形 7/7 一致）；同字段同门控对照 2 对（a_ebit：0.22/1.14→0.09/0.86 CW 不变；tle：0.20/1.20→-0.35/0.84 CW 不变，后者缠绕 UNITS 低可靠）；
- 且 gBF 叠层本身纯退化（a_ebit 干净对 S -0.13/2Y -0.28/sub -0.12）；
- 设计含义：**CW 修复方向 = 门格/持仓层**（缩短开门期、放宽门条件、持仓平滑），载荷形替换已证死路；波2 杠杆（2Y 用裸 rank 形）继续有效，两者叠加 ⇒ 下波年报门控臂的设计空间收窄为「裸 rank 载荷 × 门格修复」。
- caveat：tle 对照对的退化缠绕 UNITS 告警，其 S/2Y 退化归因不纯净；CW 不变结论不受影响（无论载荷形如何，门格产出同值 0.5）。

## §10 证据通道与盲区登记

- 本档读数来源：ask 转录臂序读数（收割步骤⑥臂归属按平台 code 核验）+ 本轮实跑只读核验 `logs/_tmp_fnd72_w3_attr_verify.py`（7/7 行级一致、w3 无撞车）+ 实读 `WAVE_w1_fundamental72_20261114.md`、`WAVE_w2_fundamental72_20261114.md`（波1/波2 锚）、`tracking/DEU/config/thresholds.json`（前轮一手）、`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md`。
- 查重通道：收割步骤③全库零命中 ⇒ 7 读数全部本波新样本（三波累计无平台撞件复读）。
- **臂6 UNITS 缠绕**：batch_status errors=1 为 WARNING 非 ERROR/CANCELLED，平台完成仿真、IS 指标在册；本档按低可靠口径引用（不构建符号/机制结论），可用性待评审裁定。
- 相关性查询未做（单槽在相关性员）；波1/波2 近闸载体（LLKO3vZ9/gJaqYgQl/A1xJRr0l）的 prod/self 仍未测（先测 prod 再扫参，归下槽）。
- 沿 ask 盲区：query_dataset_profile/query_field_profile 对 DEU 全 0 行；expressions 表不含 MCP 直连仿真。
- 设计缺口登记：波2 杠杆处方的「裸 rank 门控形」（trade_when + rank 无分组载荷）三波未派发——波3 臂5/6 为 gBF 修复尝试非该形。
- 判读不改写邻接数据集先验：fnd45/fnd86/fnd89/fnd90 结论未因本波变动。
