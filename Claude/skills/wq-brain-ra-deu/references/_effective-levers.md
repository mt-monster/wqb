# DEU 有效杠杆册（实测入册，勿凭理论新增）

> 回到 [DEU 区域流程](../SKILL.md)。本册只收**DEU 实测过、有读数对照**的结构杠杆；
> 跨区不可外推（每条都注明实测区）。新增杠杆必须附：实测前→后读数、适用结构边界、失效反例。
> 权威实测档案在 `tracking/DEU/atom_orthogonal/` 对应 wave 文件。

## 杠杆 A — 双层中性化（破 2Y）

`group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)`

- 实测：S 1.57→1.63（DEU，2026-11-12 前轮战役）
- **边界**：仅对「单层 sector 排序 + 多腿相加」的 **MODEL 结构**有效；单腿/非 MODEL 未证实
- 失效先验：单腿机构/内部人数据上无效（见 [['_basket-and-atom']] §四无效搭档族）

## 杠杆 B — 反转 × 应计质量乘法交互（破 IS_LADDER）

`multiply(reverse, accruals)`（**乘法**；加性并入崩到 0.50）

- 实测：2Y 1.47→1.77（DEU，杠杆B 原始定义波）
- **边界**：跨集反转腿 × 应计腿；ATOM 内不可复制（反转腿在 PV）——同集版见 BE242 归因「乘法稀释」

## 杠杆 C — 自身动量条件化 trade_when（质量分族 S/2Y 双升，2026-11-14 入册）

```
trade_when(ts_delta(ts_backfill(质量分, 66), 66) > 0, group_rank(ts_backfill(质量分, 66), sector), -1)
```

只在该质量分自身 66 日改善时持仓，否则维持前值。经济含义：**质量信号只在边际改善期被定价**
（QMJ 式条件化；裸质量分在大盘已定价，条件化解锁其信息）。

- 实测（DEU/TOP500/D1/SUBINDUSTRY，BE244→BE248/249，`waveBE242_FND89_ACCRUAL_ATOM_20261114.md` §十二-十三）：

| 结构 | 裸跑 S/2Y | 条件化 S/2Y |
|---|---|---|
| fnd90 GP/TA（grossprofit_asset） | −0.13 / −0.39 | **0.75 / 1.71（2Y 过闸）** |
| fnd90 pscore（Piotroski） | 0.02 / −0.49 | 0.88 / 1.12（gate22 最优 S） |
| fnd90 cash_flow_coverage | 0.08 / −0.84 | 0.82 / 0.54 |

- **边界**：① 质量分/评分类字段族（GAME/评分/报告类）通用，事件/情绪类未验证；② 门控窗 22 最优 S、66 最优 2Y；
  ③ `ts_decay_linear` 外层平滑不增益（0.70 vs 0.71）；④ group_zscore 与 group_rank 等效略低；
  ⑤ 信号 TO 降至 1.4-2.5%，margin 0.4-0.7bp。
- **增强子（BE250 实测）**：`tail(winsorize(<杠杆C>, std=2), lower=0.25, upper=0.75, newval=0.5)` 包装再 +0.09 S
  （0.75→0.84，2Y 保持 1.68）；阈值升级（Δ>自身 252 均值）+0.03。
- **失效反例**：icfroe_5y 条件化 2Y 0.23（5 年窗太慢，动量门控无意义；1y/3y 全窗亦死）；fnd93 税应计族整体无信号，
  条件化救不了无信号字段；**同源合成无效**——杠杆 C 两腿等权加/乘法在 fnd90 内全稀释（同族质量分，BE250）；
  **杠杆 A 单腿无效**（gated pscore 双层中性化 0.70 vs 0.71，A 边界坐实）。

## 杠杆 D — group_backfill 叠加修 CW（2026-11-14 入册，用户配方）

```
group_backfill(ts_backfill(vec_avg(F), 250), sector, 250)   // ✅ 唯一正确用法：叠加在 ts_backfill 之上
group_backfill(vec_avg(F), sector, 66)                       // ❌ 裸用禁止
```

组内 winsorized 均值填充缺失值，把覆盖率铺开直接稀释 CONCENTRATED_WEIGHT。

- **gBF 三定律（BE259/261 实测，`waveBE242_FND89_ACCRUAL_ATOM_20261114.md` §十七）**：
  1. **裸 gBF 对慢变量灾难**：填充值随组均值日漂移，季度/年度字段被变成日频信号——TO 47–60%，5 臂全灭；
  2. **唯一正确用法 = 叠加在 ts_backfill 之上**：先 ts_backfill(250) 锚定自身历史，再 gBF 铺组内覆盖——
     实证 CW warning 0.25 → **PASS**（KPgxRLG8）且指标无损（1.55 ≈ 1.56）；
  3. **修 CW 不损指标**：pwaQ0bx3 = gBF ±0.95 std4 = **S 1.60/F 1.40/2Y 2.01/sub 1.25，failed_ra=0，已提交 ACTIVE**。
- **边界**：慢变量（年度/季度更新）专用；带宽峰随形态漂移——rank-tail 峰 0.15/0.85=1.53、非 gBF zscore ±1=1.56、
  **gBF zscore ±0.95+std4=1.60**（双向回落证峰非单调，精修须扫 ±0.85~±1.1）。
- **失效反例**：fnd1 上 5 臂裸 gBF 全灭（waveBE242 §十七 BE259）；⚠ 波3 反证（fnd72）：trade_when 门控臂上按本杠杆正确叠层仍修不了 CW（CW=0.5 是门格结构属性、与载荷形无关，跨波跨形 7/7），且叠层本身纯退化（a_ebit 干净对 S -0.13/2Y -0.28/sub -0.12）——门控臂的 CW 修复走门格/持仓层，见杠杆 G；价格单位场（tle）上 gBF 触发 UNITS 告警、语义存疑，启用前 rank 去量纲或换字段（`WAVE_w3_fundamental72_20261115.md` §2.5–§2.6）。

## 杠杆 E — group_zscore 量级形态（rank 会扔掉量级信息，2026-11-14 入册）

`group_zscore(ts_backfill(vec_avg(F), 250), sector)` 替代 `group_rank(...)` ——保留「25 年 vs 8 年 CEO」的量级差。

- 实测（fnd1 CEO 任期，BE257）：zscore **1.38**/F1.08/sub1.32 > rank 裸跑 1.26-1.35；配合 tail(winsorize(±带宽)) 后
  达 **1.56-1.60**（BE258-261，pwaQ0bx3 提交 ACTIVE）。
- **边界**：① vec_avg 聚合最优（vec_max 1.17 更弱——平均值比最长者信息量大）；② 输出无界，tail 带宽语义变为
  zscore 对称带（±1 ≠ rank 的 0.15/0.85），须重扫；③ 符号必须区内指纹校验——CEO 任期文献先验「壕堑」负号，
  **DEU 实证「经验」正号**（BE251 −1.26 翻正，跨区不外推又一例）。
- **失效反例**：ratchet 变量（任期只涨）上 ts_zscore 动量 0.68 死、trade_when 门控 0.98<1.26 裸跑——
  杠杆 C 的门控与动量类变换对单调爬升变量全部无效。

## 杠杆 F — 形态决定 2Y：年报 IS 水平信号的 2Y 轴由形态决定（2026-11-15 入册）

fnd72 年报 IS 标量族对照（DEU/TOP500/D1/SUBINDUSTRY）：

```
rank(F)                                        // ✅ 裸 rank 形保 2Y（2Y 闸位载体；S 面仍死）
group_rank(bf66 F, sector)                     // ❌ group_rank 形灭 2Y（bf66 = backfill 66 窗，死档 1577 基线窗）
trade_when(δ66>0, group_rank(bf66 F, sector))  // ⚠ 门控复活 2Y 但封顶，不过 1.58 闸
```

实测读数（裸 vs 改造，跨波同字段对照 2/2 同向 + 波内门控分解）：

| 形 | a_ebit 2Y | tle 2Y | 其他年报族 2Y |
|---|---|---|---|
| 裸 rank | **1.51**（波1 LLKO3vZ9） | 0.99（波1 qM7eVaEP） | a_is_oper_inc **1.53**（波2 gJaqYgQl，距 2Y 硬闸 1.58 仅 0.05）；a_sales_rev_turn 1.17（kqae9wJl）；a_net_income 0.93（WjlKJZeZ） |
| group_rank(+bf66) 形对照（波2） | **0.04**（P05rJYOx） | **-0.16**（lea6L58x） | 未测 |
| trade_when 门控（同 bf66+group_rank 底，波2） | 1.14（δ66 QP0r1NGG）/ 0.94（δ22 N1PWXJbE） | 1.20（A1xJRr0l，距闸 0.38 近闸） | a_sales_rev_turn 1.10（LLKbPm7M）；a_net_income 0.76（A1xJRrlY，族级双形死） |

- 裸 rank 形跨波 2 字段复现（a_ebit 1.51 / a_is_oper_inc 1.53，2Y 1.5±0.02）；group_rank(+bf66) 形灭 2Y（跨波同字段对照 2/2 同向：a_ebit 1.51→0.04、tle 0.99→-0.16，S 同崩 0.07→-0.27 / -0.16→-0.47）；门控臂同带 bf66 仍复活 2Y（复活带 0.94–1.20）但全部不过 1.58 闸、4/5 低于各自裸锚 ⇒ **杀手在 group_rank 形而非 bf66**（波内分解对照）。
- 归因对照链：同字段跨波对（a_ebit/tle）+ 波内门控分解（同 bf66 底、仅差门控）三层对照；波 verdict=PARTIAL（n_pass=0 / n_near=2：A1xJRr0l、gJaqYgQl；判定表 `src/wqb/wave_results_contract.py:79-90`）。
- **边界**：① 跨波对照的形差捆绑 bf66+group_rank 两变量，单变量归因靠波内门控分解间接支撑（bf66 为死档 1577 基线窗，先验上不动年报水平信号）；② 裸 rank 形 S 面死（0.07–0.11，低于裸年报宽面天花板 0.37）⇒ 本杠杆只解 2Y 闸位、不解 S 闸；③ S0 处方「分组轴主用 sector」对 **2Y 轴**不成立（对 S 面结论不变——本波未测 sector 对 S 的独立效应）；④ 仅年报 IS 水平族实测；季度 IS delta 族门控 2Y 全负（-0.31~-0.60，S-2Y 跷跷板）是另一死形，不共用本结论。
- **失效反例**：「trade_when 门控推 2Y 过闸」族级证伪（5/5 门控臂 0.76–1.20 < 1.58，4/5 低于各自裸锚；fnd90 先验在本族不成立，只登记本族不改写邻接集）；net_income 族双形死（裸 rank 0.93 + 门控 0.76，波内唯一平台 sub 闸实挂 LOW_SUB_UNIVERSE_SHARPE）。
- **设计含义**：下波 2Y 闸位设计用裸 rank 形。权威档案：`tracking/DEU/atom_orthogonal/WAVE_w1_fundamental72_20261114.md`（§1 臂7–10）、`WAVE_w2_fundamental72_20261114.md`（§1、§9）。

## 杠杆 G — CW=门格结构属性：载荷形替换修不了门控臂 CW，gBF 叠层在门控臂上纯退化（2026-11-15 入册，反证杠杆）

fnd72 年报 IS 族 trade_when 门控臂（DEU/TOP500/D1/SUBINDUSTRY）——模板与死路：

```
trade_when(δ66>0, group_rank(bf66 F, sector))                // 波2 载荷：5/5 挂 CW 0.5
trade_when(δ66>0, rank(group_backfill(bf66 F, 250, sector))) // 波3 载荷：2/2 仍挂 CW 0.5，且叠层纯退化
// ⇒ 载荷形替换修门控臂 CW = 死路；CW 修复方向 = 门格/持仓层（缩短开门期/放宽门条件/持仓平滑，未实测）
```

实测读数（同字段同门控干净对照，仅差载荷形 group_rank → rank∘group_backfill；跨波跨形 CW 7/7 恒 0.5）：

| 对照对（波2→波3，δ66 门 + bf66 底） | S | 2Y | sub | CW |
|---|---|---|---|---|
| a_ebit（QP0r1NGG→zqdQqNG1，干净对） | 0.22→0.09（**-0.13**） | 1.14→0.86（**-0.28**） | 0.39→0.27（**-0.12**） | **0.5→0.5 未解** |
| tle（A1xJRr0l→RReqRmza）⚠UNITS 缠绕 | 0.20→-0.35 | 1.20→0.84 | 0.18→-0.30 | **0.5→0.5 未解** |

- 归因对照链：同字段同门控对照 2 对（a_ebit 干净；tle 缠绕 UNITS 低可靠）+ 跨波跨形 7/7（波2 group_rank 载荷 5/5 + 波3 rank∘gBF 载荷 2/2 同挂 0.5）⇒ **CW=0.5 是门格结构属性、与载荷形无关**；gBF 叠层在门控臂上**纯退化**。波 verdict=FAIL（n_pass=0/n_near=0，判定表 `src/wqb/wave_results_contract.py:79-90`；与波1/波2 PARTIAL 相比降档，归因=本波无条件化增益形且无近闸臂）。
- **边界**：① tle 对照对的 S/2Y/sub 退化缠绕 UNITS 告警（gBF 期望 Unit[] 实得 Unit[TSPrice:1]，价格单位场语义存疑）⇒ 归因不纯净、读数低可靠；**CW 不变结论不受影响**（无论载荷形如何，门格产出同值 0.5）；② 波2 杠杆（2Y 用裸 rank 形）继续有效，与本杠杆叠加 ⇒ 下波年报门控臂设计空间收窄为「裸 rank 载荷 × 门格修复」（波2 处方的裸 rank 门控形三波仍未派发，`WAVE_w3_fundamental72_20261115.md` §10 设计缺口）；③ 只否定「门控臂 × 载荷形替换」路径，**不推翻杠杆 D**——非门控 MODEL 形上的 gBF 修 CW（BE259/261，CW 0.25→PASS KPgxRLG8）仍成立；④ 适用域=fnd72 年报 IS 族 @SUBINDUSTRY 格，跨集不外推。
- **失效反例**：「gBF 修 CW」假设在门控臂族级证伪（波3 2/2 败且纯退化）；tle 族三形态累计全弱（裸 rank S -0.16 / 门控 group_rank +0.20 / 门控 gBF -0.35+UNITS，sub -0.30 平台实挂）——启用前必须 rank 去量纲重建或换字段。
- **设计含义**：CW 挂在 trade_when 门控年报臂上时，别再扫载荷形，改攻门格/持仓层。权威档案：`tracking/DEU/atom_orthogonal/WAVE_w3_fundamental72_20261115.md`（§1 臂5/6、§2.5–§2.6、§4、§9）。

## 杠杆 H — tail 低/高尾压缩壳（0.12/0.88/0.5；带宽是核/字段相关参数，2026-11-16 入册）

```
tail(group_rank(multiply(rank(δ240), rank(δ176), ts_rank(p,1008)), sector),
     lower=0.12, upper=0.88, newval=0.5)
```

用法：把 <12% 与 >88% 分位的尾部压到 0.5（只保留中段排序信息）。**壳层压缩器，不产生新信息**；套在已排序的 `group_rank` 外层。

**对照读数（DEU/TOP500/D1/FAST/decay0/trunc0.08）**

| 臂 | 结构 | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| w1 `LLKX7rxL` | 裸 `group_rank(multiply(rank(δ240), rank(δ176), rank(ts_rank(p,1008))), sector)` | 1.42 | 0.94 | 1.96 | 0.91 | 15.28% | 9.30% | 8.69bp |
| w2 `d5a7PrpK` | 同式外裹 `tail(...,0.12,0.88,0.5)`（`ts_rank` 为 raw） | 1.51 | 1.00 | 2.33 | 1.14 | 18.11% | 7.47% | 8.69bp |
| Δ（跨波，仅作读数） | | +0.09 | +0.06 | +0.37 | +0.23 | +2.83pp | −1.83pp | 0 |

⚠ **归因更正：w1→w2 不是单变量对照**（`WAVE_rt-fundamental-w2_20261116.md` §12 / `WAVE_rt-fundamental-w3_20261116.md` §0）：两式还差 `rank(ts_rank(p,1008))` vs raw `ts_rank(p,1008)`，即「加 tail」与「去外层 rank」两处同改；w3 推得 rank 包装约 +0.03~0.04（w2 arm5 vs w3 C0 四项差）⇒ **+0.09/+0.06/+0.37/+0.23 不得全部记到 tail 名下**（DB `wave_results id=2207` 的 `[newLever-tail 壳]` key_finding 为更正前文本，以本条为准）。

**干净对照（单变量）**

- **带宽曲线（三年窗核，同 raw `ts_rank`，只差带宽；w3 臂9/10 + w2 臂7）**：0.10 `O0WmdbPR` **1.56/1.05/2.41/1.18（TO 18.30%）** > 0.12 `d5a7PrpK` 1.51/1.00/2.33/1.14 > 0.15 `88N6Wa9W` 1.53/1.02/2.10/1.09；2Y/sub 随带宽放宽单调下降（2.41→2.33→2.10 / 1.18→1.14→1.09）。
- **w4 补测 0.05–0.15（同核同字段）**：0.05 `0mPQJnWv` **塌陷** 1.31/0.82/2.32/1.19；0.08–0.11 平台区（S 1.54–1.56 / F 1.03–1.05 / sub 1.18–1.21 / 2Y 2.27–2.56）；**0.10 是 S/F 内点峰**（w3 的边界值缺口关闭），**0.08 是 2Y/DD 峰**（2.56 / 7.38%）；0.12/0.15 回落 1.51/1.53。
- **字段×带宽交互（w4 EBIT 核 0.08→0.10→0.12 单调下降）**：S 1.62→1.56→1.51 / F 1.12→1.05→1.00 / 2Y 2.54→2.30→2.17 / sub 1.16→1.04→1.00；`kqamAeRg`（EBIT×tail0.08）= **1.62/1.12/2.54/1.16，ra_failed_count=0（fnd72 首个 RA 全闸 PASS）**，但 SELF/PROD/DATA_DIVERSITY pending、年度分年未取 ⇒ **RA PASS ≠ 可提交**。
- **反面对照（增量 ROA 核，同波同核干净；w3 臂1/2/3）**：裸 C0 `qM7z2P1Z` 1.48/1.02/1.64/0.95 → +tail0.12 `O0WmdbYp` 1.35/0.86/1.71/0.84（S −0.13 / F −0.16 / sub −0.11，仅 2Y +0.07）→ +tail0.15 `ZYalV250` 1.43/0.93/1.77/0.96（S −0.05 / F −0.09 / 2Y +0.13 / sub +0.01）。

**边界**

① **核相关，不是通用免费增益**：三年窗核上 tail 臂均高于裸臂，但裸列有 rank 包装混淆、净增益幅度不可精确归因；增量 ROA 核上 tail 0.12/0.15 的 S/F 反而低于裸 C0 ⇒ 换核必须重测。② **带宽峰随核/字段/包装层移动**：NEARGATE §四 的 0.12–0.15 峰测于 winsorize(std3)+hump(0.003) 包装核；本族裸核 oper_inc 以 0.10 为 S/F 峰、0.08 为 2Y/DD 峰，EBIT 以 0.08 最优 ⇒ 不存在全族统一带宽（0.06/0.07 未测，不得称全局峰）。③ **换手上升**：TO +2.8~3.0pp（15.28%→18.11/18.30%），margin 视核可降（d5a7PrpK 8.69bp vs 同族 mLaALJX2 9.55bp）。④ **不能替代 hump 的 F/margin 价值**：无 winsorize(std3)/hump(0.003) 也达 mLaALJX2 级 S/2Y（1.51/2.33 vs 1.50/2.30），但 F 1.00 vs 1.04、margin 8.69 vs 9.55bp；hump 的边际价值主要在 F/换手。⑤ **分组轴不可补偿**：sector ≫ subindustry（w4 同核同带宽 1.56/1.05/2.41/1.18 vs 1.18/0.69/1.87/0.78），tail 救不了错轴。

**失效反例**

- **带宽过窄塌陷**：tail 0.05（w4 臂1）S 1.31/F 0.82，比 0.08 低 0.23 ⇒ 裁尾过度丢掉有效信息。
- **核错位**：增量 ROA 核上 tail 0.12/0.15 S/F 双降（见上），方向与三年窗核相反 ⇒ 不可跨核搬运。
- **zscore 带宽形全灭**（NEARGATE §B5）：tail 带宽在 zscore 量级形上无效（全灭），本条只对 rank 型排序壳成立。
- **门控臂不适用**：trade_when 门控年报臂 CW=0.5 是门格结构属性，tail/gBF 载荷形替换修不了（杠杆 G，跨波跨形 7/7 恒 0.5）；tail 不改变该结论。
- **不解决 S 闸（w1–w3）**：w2/w3 最好 tail 件 1.51/1.56 仍差 LOW_SHARPE 0.07/0.02；w4 EBIT×0.08 才首过 RA 全闸（pending 项未验）。

- 实测域：DEU/TOP500/D1/FAST/decay0。权威档案：`tracking/DEU/regular_tower/WAVE_rt-fundamental-w1_20261116.md` §1 臂1、`WAVE_rt-fundamental-w2_20261116.md` §1 臂7 / §9 / §12、`WAVE_rt-fundamental-w3_20261116.md` §0 / §3、`WAVE_rt-fundamental-w4_20261116.md` §1 / §3；族内 tail 先验 `tracking/DEU/atom_orthogonal/NEARGATE_BREAK_GRID_FND72_20261115.md` §二 B5/B8、§四。

## 反模式（实测证伪，勿再投）

| 反模式 | 实测证据 |
|---|---|
| **同源合成**（等权 add / 乘法把同数据集两腿拼一起） | BE250/BE242#9/BE257/BE252 四证全稀释（fnd90 0.84→0.49、fnd1 1.26→1.17）；闸5 同源豁免的 corr<0.7 假设在同族字段上不成立 |
| **S-2Y 跷跷板**（设置级手段破不了 S 闸） | decay12/轴切换/平滑/锐化在 fnd1 上无一抬 S（1.43-1.49 反降），fnd1 靠结构跃迁（zscore 量级）破闸——S 卡壳先换结构再动设置 |
| **宽度塌缩入场**（平台集级 cov=0 或 lc<50 的集不开波） | digital_ad_spend lc25/sc25+CW 挂、alpha_factor_lib DD 71-199% 超窄账户签名——**数据层排除≠信号死**，登记口径见判死分层 |
| **tail 跨核外推**（把三年窗核的 tail 增益搬到任意核） | w3 增量 ROA 核同波干净对照：裸 C0 1.48/1.02 → tail0.12 1.35/0.86（S −0.13/F −0.16）、tail0.15 1.43/0.93（S −0.05/F −0.09）；w4 又证字段×带宽交互（oper_inc 0.10 / EBIT 0.08，无全族统一带宽）——tail 是核相关杠杆，换核必须重测 |

## 通用纪律

- **近闸 prod 前置（用户 2026-11-14 明令）**：候选达到**近闸**（S≥1.2 或距任一硬闸 ≤0.4）时，**先 `check_correlation(production, refresh=True)` 探 prod，再决定是否继续网格扫参**——prod 雷在核心不在搭档，同核变体共 prod 命运；prod 堵则整族停手换核，prod 净才烧扫参配额（model238 54 臂后才发现 0.77 堵的反例；wpoXmKGv 1.35 时即探得 0.6805 净的正例）。
- 每个杠杆先做**归因对照**（裸跑 vs 加杠杆同批）再入册，禁止无对照入册。
- 跨区移植前 2 槽小批先验方向（TWN/KOR/DEU 符号翻转先例见 [['_basket-and-atom']] §四）。
- 同一经济腿只贡献 1 颗（clone 相关 self 0.96 实例）。
