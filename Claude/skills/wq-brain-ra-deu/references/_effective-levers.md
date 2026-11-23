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

## 杠杆 I — 跨维度乘法交互（同集两腿不同维度：规模集中 × 事件新鲜度；2026-11-16 入册）

```
conc66 = ts_sum(divide(vec_max(insd1_valueeur), vec_sum(insd1_valueeur)), 66)  // 最大单笔占当日总额（规模/信念集中）
fresh  = 1/(days_from_last_change(vec_avg(insd1_holdings))+1)                   // 距上次持仓变动天数（信息新鲜度）
multiply(rank(conc66), rank(fresh))                                             // ✅ 两腿是不同维度，乘法增益
subtract(rank(conc66), rank(ts_ir(vec_avg(insd1_holdings), 66)))                // ❌ 同集复合≠增益：减法+错维度 → 负
```

「又大又新」：规模集中度是**存量/截面**维度，事件新鲜度是**流量/时间**维度——不是同一潜变量的投影，
乘法保留两维信息并让「大且新」的持仓拿最高分（`WAVE_rt-insiders-w2_20261116.md` §2.2）。

**对照读数（DEU/TOP500/D1/insiders1、中性化 SUBINDUSTRY、decay0/nanON/trunc0.08/66 窗，2014-01-01→2023-12-31）**

| 臂 | 结构 | S | F | 2Y | sub | margin | 来源 |
|---|---|---:|---:|---:|---:|---:|---|
| conc 单腿（w1 臂7 `oma3GYeb`） | 裸 `rank(conc66)` | 0.81 | 0.50 | 0.83 | 0.19 | 20.39bp | w1 平台实读 |
| fresh 单腿（w2 臂1 `gJaR5gov`） | `group_rank(fresh, sector)` | 0.78 | 0.51 | **1.08** | 0.18 | 19.89bp | w2 平台实读 |
| **复合（w2 臂3 `d5aE63Ew`）** | `multiply(rank(conc66), rank(fresh))` | **0.89** | **0.63** | 0.92 | **0.26** | **21.56bp** | w2 平台实读 |
| Δ vs conc 单腿 | 左腿表达式**逐字相同**、同配置同日期（跨波） | +0.08 | +0.13 | +0.09 | +0.07 | +1.17bp | 纯单变量 |
| Δ vs fresh 单腿 | ⚠ 含 `group_rank(sector)`→`rank` 混淆 | +0.11 | +0.12 | **−0.16** | +0.08 | +1.67bp | 非纯单变量 |

- **增益方向**：S/F/sub/margin 四项同时高于两条单腿 ⇒ 不触发稀释铁律；这是 insd1 两波 20 臂里**首个「复合高于单腿」**的形态（§5）。
- **归因纯度（如实标注）**：左腿对照为**跨波**（w1 已入库档，本波未重跑 conc 腿），但表达式逐字相同 + 同配置同日期 ⇒ 单变量成立；
  右腿含分组差混淆 ⇒ 只能把「不稀释」判给乘法结构，不能把 +0.11 精确归因到乘法。严格按本册「同批」口径，跨波对照是残留折扣。
- **波 verdict=PARTIAL（n_pass=0 / n_near=2；判定表 `src/wqb/wave_results_contract.py:79-90`）**：10/10 臂 `failed_ra_count` 3–5、无一过 RA 全闸；
  近闸仅两条——复合臂 `d5aE63Ew` 距 F 闸 0.37（F 0.63 vs limit 1.0，S/F/margin 全波最高）、fresh 单腿 `gJaR5gov` 距 CW 闸 0.069
  （0.168741 vs limit 0.1，挂点 **2014-01-02 样本首日**）。距 S 闸最近 0.69（复合臂）、距 2Y 闸最近 0.47（臂6 1.11）、距本地 sub 线最近 0.56（臂2 0.44）。
- **平台闸限实读（`checks.fail.limit`）**：LOW_SHARPE=1.58（10/10）/ LOW_FITNESS=1.0 / HIGH_TURNOVER=0.70 / LOW_2Y·IS_LADDER=1.58 /
  CONCENTRATED_WEIGHT=0.10（比本地 review 线 0.5 严 5 倍）/ LOW_SUB **逐臂动态 0.09–0.42** ⇒ **sub≥1.0 是本地 review 线、不是平台闸限**
  （臂2 sub 0.44 平台判 PASS；`tracking/DEU/config/thresholds.json:21`）；verdict 与 sub 口径无关（10/10 臂都挂 S+F 两项）。

**边界**

① **仅单一探针档验证**：decay0/nanON/SUBINDUSTRY/trunc0.08/66 窗（两波同档），与区域生产档（decay4/nanOFF/2013 起）不同 ⇒ **配置层未验**，配置层死/活未判。
② **2Y 是让步项**：0.92 **低于** fresh 单腿 1.08 ⇒ 2Y 为主缺口时不适用；本波 10 臂 2Y ≤1.11，两项近闸也都不在 2Y。
③ **绝对强度弱、不改路线结论**：S 0.89 距 LOW_SHARPE 闸 0.69，仍低于 BE176 的 insiders1 单集上限 1.30（两波 20 臂 0/20 破 1.30）⇒
   「insd1 单集 ATOM 过不了 1.58」继续成立；本杠杆是**方向性结构增益**，不是过闸配方（复合臂自身挂 4 闸：S/F/sub/2Y）。
④ **单点对照**：未做配置/时间稳健性；窗口只 66（22/132 未测）；prod/self 全 null（未测）。
⑤ **对照纯度**：conc 侧纯单变量但跨波；fresh 侧含 `group_rank→rank` 混淆。

**失效反例 / 适用边界修正**

- **修正 BE176 的适用范围**：BE176「6 字段同源 ⇒ 任何叠加都平均化同源噪声」（`BE176_INSIDERS1_CEILING_130_20261112.md`「机理（已确认）」）
  对**加法/等权叠加**成立，对**不同维度的乘法**不成立。这是边界修正、不是推翻：**同一潜变量投影**的乘法仍按同源处理
  （杠杆 C 内 fnd90 同族质量分乘法稀释，BE250；insd1 的 value/valueeur 亦是同源）。
- **同集复合≠增益**：`subtract(rank(conc66), rank(ts_ir(...)))`（臂4 `0mPeLNer`）S −0.16 / F −0.06 / 2Y −0.53 / DD **44.56%** / LC-SC **31/30**，
  CW 0.285488>0.1 挂 ⇒ 方向错（减法）+ 维度错（ts_ir 与 conc 同属交易强度族）即崩到负；且缺 `ts_ir` 单腿对照，定量归因不成立。
- **同源门控仍稀释**：`if_else(mask<0.5, rank(fresh), 0.5)`（臂10 `9qla3dJV`）0.50/0.24/0.96/0.13 vs fresh 单腿 **−0.28/−0.27/−0.12/−0.05**
  ⇒ 增益来自「不同维度 × 乘法」这个结构，不是「复合」本身。
- **2Y 主缺口场景**：要 2Y 用 fresh 单腿（1.08）或掩码臂（1.11），不要用本复合。

- 实测域：DEU/TOP500/D1/`insiders1`（provisional，未判死）/decay0。权威档案：`tracking/DEU/regular_tower/WAVE_rt-insiders-w1_20261116.md` §1 臂7、
  `WAVE_rt-insiders-w2_20261116.md` §1 臂1/臂3、§1.1、§2.2、§3 C1/C2/C9、§5、§6、§10、§12；先验 `tracking/DEU/atom_orthogonal/BE176_INSIDERS1_CEILING_130_20261112.md`。

## 杠杆 J — 单笔金额统计量：离散度优于集中度（`vec_stddev÷vec_sum` 取代 `vec_max÷vec_sum`，2026-11-16 入册）

```
conc66 = ts_sum(divide(vec_max(insd1_shares),    vec_sum(insd1_shares)), 66)   // 最大单笔占当日总额
conc_s = ts_rank(conc66, 252)                                                  // 集中度臂
disp66 = ts_sum(divide(vec_stddev(insd1_shares), vec_sum(insd1_shares)), 66)   // 单笔金额离散度÷当日总额
disp_s = ts_rank(disp66, 252)                                                  // ✅ 同壳替换：离散度臂
```

同字段、同壳（`ts_sum(·,66)` + `ts_rank(·,252)`）、**只差一个 token**（`vec_max` → `vec_stddev`）——insd1 三波 30 臂里**最干净的单变量消融**（w3 §2.1 原话）。
经济含义：内部人**单笔金额的分散/一致程度**比「最大单笔占比」更含信息（后者易被一次性协议转让/巨额单笔主导），
集中度只回答「有没有大手笔」，离散度回答「多笔之间是否一致」。

**同壳单 token 消融（w3 臂1 vs 臂10；DEU/TOP500/D1/`insiders1`、SUBINDUSTRY、decay0/nanON/trunc0.08、66+252 窗、2014-01-01→2023-12-31）**

| 臂 | 结构 | S | F | 2Y | sub | TO | DD | margin | RA 挂闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 裸（臂1 `2r5v12Kb`） | `ts_rank(ts_sum(vec_max÷vec_sum, 66), 252)` 集中度 | 0.17 | 0.04 | −0.23 | 0.00 | 7.27% | 12.22% | 2.08bp | 4（含 LOW_SUB 0.08） |
| 改造（臂10 `Jj8nV2OE`） | `ts_rank(ts_sum(vec_stddev÷vec_sum, 66), 252)` 离散度 | **0.44** | **0.18** | **0.56** | **0.47** | 6.08% | 14.40% | **6.72bp** | 3（sub 平台判 PASS） |
| Δ（单 token） | | **+0.27** | +0.14 | **+0.79** | **+0.47** | −1.19pp | **+2.18pp** | +4.64bp | |

**跨波支撑（valueeur 口径，独立对照；⚠ 壳不同 ⇒ 非单变量）**

| 波 | 臂 | 结构 | S | F | 2Y | sub | DD | margin |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| w1 | `oma3GYeb`（臂7） | 集中度 `ts_sum(max÷sum,66)` + 裸 `rank` | **0.81** | 0.50 | 0.83 | 0.19 | 13.90% | 20.39bp |
| w2 | `mLarN0x1`（臂2） | 离散度 `group_rank(ts_sum(stddev÷sum,66), sector)` | 0.72 | 0.44 | 0.60 | **0.44** | 14.35% | 21.00bp |
| Δ | | | −0.09 | −0.06 | −0.23 | **+0.25** | +0.45pp | +0.61bp |

⇒ 两次独立对照（不同波、不同字段口径 shares / valueeur）：**sub 方向一致**（+0.47 / +0.25），margin 同向；
⚠ **S/2Y 在 valueeur 跨波对上方向相反**（0.72 < 0.81 / 0.60 < 0.83）⇒ 「离散度全面优于集中度」**只在 shares 同壳单变量上成立**，
跨波可复现的只有 **sub 维度**。如实登记，不外推。

**边界**

① **仅单探针档**：decay0/nanON/SUBINDUSTRY/trunc0.08/单一 66+252 窗；区域生产档（decay4/nanOFF、2013 起，`tracking/DEU/config/settings.json:5-16`）三波未跑 ⇒ 配置层死/活未判（D6 未达）。
② **只证明族内统计量选择**，**不改变 shares 口径整体偏弱**：同波 shares 集中度 0.17、加权 0.33/−0.22、掩码 0.27/−0.01、乘法左腿 0.17，
   而 valueeur 集中度 w1 是 0.81 ⇒ 同一个 `max÷sum` 换字段后 S 掉 0.64。「离散度更好」≠「shares 口径可用」。
③ **不构成可推进候选**：臂10 S 0.44 距 LOW_SHARPE 闸 **1.14**；sub 0.47 距本地 review 线 1.0 仍 0.53
   （平台 `LOW_SUB_UNIVERSE_SHARPE` 是**逐臂动态限** 0.08–0.37，臂10 判 PASS——sub≥1.0 是本地 review 线而非平台闸限，`tracking/DEU/config/thresholds.json:21`）。
④ **强项是 sub**：0.47 = **三波非退化最高**（w1 0.38 / w2 0.44 / w3 0.47）；若目标是 ★v2 的 sub≥1.0，本族优先离散度而非集中度。
⑤ **波 verdict=FAIL**（n_pass=0 / n_near=0；判定表 `src/wqb/wave_results_contract.py:79-90` 的 `verdict_from_counts`）——本杠杆是方向性结构结论，不是过闸配方。
⑥ **未扫**：窗口梯（只 66+252，22/132 未测）、prod/self 全 null（归相关性员）、宇外维度未变。

**失效反例**

- **同波 `trade_when(…, −1)` 兜底做空是破坏性的**：`trade_when(dfc(bf(vec_count,252))<66, ts_rank(conc,252), −1)`（臂4 `KPgnK2L1`）
  S −0.23 / 2Y −0.76 / sub −0.36 / DD **26.56%**，对同核臂1 为 **S −0.40 / 2Y −0.53 / sub −0.36 / DD +14.34pp** ⇒ 门控失败落 −1 制造长期空头偏置。
  FIELD 档 M9「DEU 未测 trade_when」由此改为「实测负」。本杠杆若要叠门控，先别用 −1 兜底。
- **`vec_stddev` 的增益不可跨指标外推**：valueeur 跨波对上 S −0.09 / 2Y −0.23（见上表）⇒ 需要 S/2Y 时不能假设离散度更好，必须重测。
- **「低/高机构持股是强侧」是形态产物，与本杠杆无关，勿混**：掩码形态三波一致「低带强」（+0.21/+0.18/+0.28），而互补权重形态同波**反号**
  （低带 −0.22 vs 高带 0.33，且代数上 臂6+臂7 = 裸腿）⇒ 引用时必须带形态限定；不要把机构的形态效应记到统计量选择名下。
- **同源稀释仍适用**：insd1 内部 `value` / `valueeur` 是同一潜变量投影，等权加法/乘法按同源处理（BE176；边界修正见杠杆 I）。

- 实测域：DEU/TOP500/D1/`insiders1`（provisional，未判死）/decay0。权威档案：`tracking/DEU/regular_tower/WAVE_rt-insiders-w3_20261116.md`
  §1 臂1/臂10、§1.1、§2.1、§2.3、§3 C1/C3、§10–§12；跨波对照 `WAVE_rt-insiders-w2_20261116.md` §1 臂2 / §2.1、
  `WAVE_rt-insiders-w1_20261116.md` §1 臂7；闸限 `src/wqb/wave_results_contract.py:79-90`、`tracking/DEU/config/thresholds.json:2-12,21`。

## 杠杆 K — 事件时钟用金额变化，不用交易条数（同壳单变量，跨波；2026-11-16 入册）

```
金额时钟 = ts_rank(252 - days_from_last_change(ts_backfill(vec_sum(insd1_valueeur), 252)), 252)   // ✅ w4 臂9 1YWovJdJ
条数时钟 = ts_rank(252 - days_from_last_change(ts_backfill(vec_count(insd1_shares),  252)), 252)   // ❌ w3 臂2 O0Wn129p
```

「事件多久没发生」的时钟按**金额**计量：一次大额申报与一次小额申报不是同一个事件，条数把两者等价。
两式**同壳**，`ts_backfill` 内只差一个聚合式（`vec_sum(valueeur)` vs `vec_count(shares)`）。

**对照读数（DEU/TOP500/D1/`insiders1`、SUBINDUSTRY、decay0/nanON/trunc0.08、2014-01-01→2023-12-31；两波同档同日期）**

| 臂 | 时钟 | S | F | 2Y | sub | TO | DD | margin | RA 挂闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 裸（w3 臂2 `O0Wn129p`） | 条数 `vec_count(insd1_shares)` | 0.27 | 0.08 | 0.09 | 0.02 | 9.31% | 8.61% | 2.56bp | 4（含 LOW_SUB 0.13） |
| 改造（w4 臂9 `1YWovJdJ`） | 金额 `vec_sum(insd1_valueeur)` | **0.43** | **0.17** | **0.32** | **0.24** | 11.21% | **8.48%（四波最低）** | **3.53bp** | 3（sub 平台判 PASS） |
| Δ（单变量，跨波） | | **+0.16** | +0.09 | **+0.23** | **+0.22** | **+1.90pp** | −0.13pp | **+0.97bp** | |

- **判据**：S 差 0.16 > ask 给的 H4 阈值 0.10（`WAVE_rt-insiders-w4_20261116.md` §2.5、§3 C5）。
- **归因纯度**：两波配置/日期/中性化逐项相同（平台 `get_alpha_details` 逐臂回显 10/10 一致；两波各 10/10 COMPLETE、errors=0），表达式同壳、仅时钟聚合式不同 ⇒ **跨波单变量**（满足本册「裸 vs 改造」口径；唯一残留折扣是跨波而非同批）。
- ⚠ **条数轴的语义前提未复核**：`vec_count` 是「当日申报记录条数」，不是股数口径的新鲜度——FIELD 档曾证 5 个字段的 `vec_count` 指标逐位相同（`FIELD_insiders1_20261116.md` §4.2），w3 未复核该等价性（`WAVE_rt-insiders-w3_20261116.md` §3 末项）⇒ 「条数」这一解释带一条未复核前提，不影响两式读数本身。
- **波 verdict=PARTIAL**（n_pass=0 / n_near=2；判定表 `src/wqb/wave_results_contract.py:79-90` 的 `verdict_from_counts`）：10/10 臂 `failed_ra_count` 3–4、无一过 RA 全闸。近闸仅两条——臂1 `LLKnekRL` 距 F 闸 0.33（F 0.67 vs limit 1.0）、臂10 `MP6bwkGM` 距本地 sub 线 0.32（sub 0.68 vs 1.0；⚠ 平台 `LOW_SUB_UNIVERSE_SHARPE` 判 PASS，该近闸只在本地 1.0 线下成立，且长侧仅 55 只）。**本杠杆两臂都不在 near 池**（臂9 四闸距 S 1.15 / F 0.83 / 2Y 1.26 / 本地 sub 0.76）。排序外如实登记：臂7 `Jj8nlbpW` S 0.88 / 2Y 1.05 / sub 0.46 是综合最好结构，但四闸距 S 0.70 / F 0.48 / 2Y 0.53 / 本地 sub 0.54 全 >0.4 ⇒ 不入选。margin 机械命中（臂6 2.43bp / 臂9 3.53bp / 臂2 负值，绝对差均 ≤0.4）因闸量纲 0.0005（全区间约 0.007）、「0.4」比全量程大 50+ 倍而失去分辨力，明确不列 near（同 w1 排 TO、w3 排 margin 的处置逻辑）。
- **verdict 对 sub 口径不敏感**：10/10 臂在任何 sub 判据下仍挂 LOW_SHARPE + LOW_FITNESS（§11）⇒ n_pass=0 不依赖 sub 线取平台动态限（逐臂 0.09–0.42）还是本地 1.0；只有臂10 的 near 依赖本地线（`tracking/DEU/config/thresholds.json:21`）。

**边界**

① **仅探针档**：decay0/nanON/SUBINDUSTRY/单一 252 回填窗；区域生产档是 decay4/nanOFF/2013 起（`tracking/DEU/config/settings.json:5-17`）⇒ 配置层死/活未判（D6 未达）。
② **两侧 S 都低**（0.43 vs 0.27）：这是「哪个时钟更对」的**设计结论，不是可推进候选**——臂9 四闸距 1.15 / 0.83 / 1.26 / 0.76，全部远离 near。
③ **换手代价**：金额时钟 TO 11.21%（本波最高，+1.90pp）；DD 8.48%（四波最低，−0.13pp）⇒ 低换手目标下不适用，回撤优先时可作候选轴。
④ **时钟未穷尽**：只测 valueeur（金额）与 count（条数）。`vec_avg(insd1_holdings)` 在 w2 是**不同壳**（`1/(dfc+1)` + 裸 rank/group_rank，杠杆 I fresh 单腿 `gJaR5gov` S 0.78 / 2Y 1.08）⇒ **不可与两时钟直接比**；holdings 时钟待同壳补测（本结论最大的未覆盖面）。
⑤ **单点对照**：只一个回填窗，未做时间/配置稳健性；prod/self 全 null（归相关性员）。

**失效反例**

- **条数时钟不作默认口径**：同壳下 S −0.16 / 2Y −0.23 / sub −0.22；若沿用 count 时钟当新鲜度/事件腿，会把「时钟选错」误读成「字段没信号」。
- **不可外推成「金额场一切皆优」**：杠杆 J 的跨波 valueeur 对照已显示方向可反（valueeur 离散度 vs 集中度 S −0.09 / 2Y −0.23）⇒ 本杠杆的优势在**时钟轴（金额 vs 条数）**，不是「valueeur 优于 shares」的一般命题。
- **不可把 0.43 当进度**：仍需 S/F/2Y 三闸同时破；本条只提供时钟轴方向，不提供过闸配方。

- 实测域：DEU/TOP500/D1/`insiders1`（provisional，未判死）/decay0。权威档案：`tracking/DEU/regular_tower/WAVE_rt-insiders-w4_20261116.md` §1 臂9、§2.5、§3 C5、§10、§11；对照臂 `WAVE_rt-insiders-w3_20261116.md` §1 臂2、§2.6；闸限 `src/wqb/wave_results_contract.py:79-90`、`tracking/DEU/config/thresholds.json:2-12,21`。

## 杠杆 L — Δmean66 分子的分母通道：事件 IR(shares, bf250) 优于静态集中度(valueeur)（通道级跨块交换；2026-11-17 入册）

```
裸（w2批2 臂4 XgaKMZwb）   = group_rank(divide(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66),
                             ts_sum(divide(vec_max(insd1_valueeur),vec_sum(insd1_valueeur)),66)),sector)
改造（w3批2 臂6 A1x3AN0l）  = group_rank(divide(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66),
                             ts_ir(ts_backfill(vec_avg(insd1_shares),250),66)),sector)
```

分子（Δmean66·holdings）、壳（`group_rank`·sector）、轴、配置逐项相同，**只有分母块不同**：
静态集中度 `ts_sum(max÷sum valueeur, 66)` → 事件 IR `ts_ir(bf(vec_avg(shares),250),66)`。
分母回答的问题从「单笔大手笔的集中度」换成「申报强度的事件稳定性」（IR = 均值÷波动，bf250 补稀疏覆盖）。

**对照读数（DEU/TOP500/D1/`insiders1`、SUBINDUSTRY、decay0/nanON/trunc0.08、2014-01-01→2023-12-31；两波同档同日期，跨波单块交换）**

| 臂 | 分母块 | S | F | 2Y | sub | TO | DD | RA 挂闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 裸（w2批2 臂4 `XgaKMZwb`） | conc66 `ts_sum(max÷sum valueeur,66)` | 1.16 | 1.01 | 0.98 | 0.26 | 9.81% | 10.50% | 4（F 平台 pass，全战役首次；S/CW/sub/2Y 挂） |
| 改造（w3批2 臂6 `A1x3AN0l`） | `ts_ir(bf(vec_avg(shares),250),66)` | **1.27** | **1.15** | 1.02 | **0.32** | 10.19% | **9.89%** | 4（F 平台 pass；LOW_SHARPE 1.27/1.58、CW 0.5@2014-01-29、sub 0.32/0.6、2Y 挂） |
| Δ（块交换） | | **+0.11** | **+0.14** | +0.04 | **+0.06** | +0.38pp | **−0.61pp** | |

**同波复现**（仅分母统计量 vec_avg→vec_count 的单变量变体，`XgaK0bWX`）：1.23 / 1.10 / 1.09 / 0.32 / DD 10.94% ⇒ 对基线 S **+0.07** / F +0.09 / sub +0.06，同向复现；vec_avg 优于 vec_count（同壳单变量对 ΔS −0.04）。三波 S 演进 0.81→0.89→1.16→1.27 单调爬升（1.27 = 全战役 insiders1 系新高）。

- **归因层级（如实登记）**：分子/壳/轴/配置逐项相同仅分母块不同 ⇒ **跨波单块交换对照**；但分母块内含 **3 个 token 差异**（字段 valueeur→shares、统计 ts_sum(max÷sum)→ts_ir、backfill 250 有无）⇒ 是**通道级对照，不是单 token 消融**；shares 裸 IR 腿（`group_rank(rank(ts_ir(ts_backfill(vec_avg(insd1_shares),250),66)),sector)`）本波未排，复合 vs 裸分母的归因部分开放。
- **波 verdict=PARTIAL**（n_pass=0 / n_near=2；判定表 `src/wqb/wave_results_contract.py:84-90` 的 `verdict_from_counts(0,2)`）：10/10 臂 `failed_ra_count` 3–5、无一过 RA 全闸。近闸 2 条（按 S 降序）：①`A1x3AN0l` S 1.27——S≥1.2✓ + 距 S 闸 0.31✓ + CW 0.5 vs 平台 limit 0.1 差 0.40（边界）✓ + sub 0.32 距平台动态限 0.6 差 0.28✓，F 1.15 平台 pass；②`XgaK0bWX` S 1.23——距 S 闸 0.35✓ + CW 差 0.40✓，F 1.10 pass。机械命中出名额（如实登记，非 near）：臂9 `YPaAebbA` / 臂2 `E5QKdper` F 0.97 距 F 闸 0.03、臂3 `N1POZaRE` 2Y 1.20 距 1.58 闸 0.38，按 S 降序 ≤2 名额用尽未入池。指纹①取反对 0 条（本波未排，不得据此判死或证机制在）。
- **prod/self 状态（入册时点核验，更新 ask 口径）**：ask/波档记「prod/self 未测」；本员核验时 DB 实读 **prod 已测**：`A1x3AN0l` 0.5715 / `XgaK0bWX` 0.5819（`prod_corr_source=check_correlation`，corr_checked_at 2026-11-17T22:48–22:49，均低于内部严线 0.65 与平台线 0.70——`src/wqb/config.py:512,532`）⇒ **prod 净**；`self_correlation` 仍 null（未测，仍开放）。
- **与杠杆 I（conc×fresh 乘法）的关系**：不同层级——杠杆 I 是**壳层**跨维度交互（conc×fresh 两腿相乘）；本条是**分母通道替换**（÷ 什么）。两者不互替，也不能把本条的 +0.11 记到乘法名下。

**边界**

① **通道级对照非单 token 消融**（见上）：3 token 同时变，「事件 IR 更好」是块级结论，不能精确归因到字段/统计量/backfill 任一 token；shares 裸 IR 腿未测是最大开放点。
② **仅探针档**：decay0/nanON/SUBINDUSTRY/trunc0.08/单一 66+250 窗；区域生产档 decay4/nanOFF、2013 起（`tracking/DEU/config/settings.json:5-16`）未扫 ⇒ 配置层死/活未判（D6 是 insiders1 六维唯一未达维）。
③ **获胜臂仍挂两闸**：CW 0.5@2014-01-29（Δmean66 分子首月建仓伪影；**Δmean 分子 7 臂 7/7 挂、非 Δmean 臂 3/3 pass** ⇒ CW 是 Δmean 分子的家族属性，臂4 ts_av_diff+bf250 证明 bf250 可修）+ sub 0.32；2Y 1.02 距 1.58 闸 0.56 仍挂。S 1.27 距 LOW_SHARPE 1.58 闸 0.31 ⇒ **不是过闸候选**，是近闸件。
④ **分组轴通道已关闭，不能当替代路径**：同核 Δmean66÷conc66 四点扫 sector 1.16（基线跨波复现）/ market 1.13 / industry 1.10 / subindustry 0.99 ⇒ 三个替代轴全部低于基线、更低于分母通道改造的 1.27，sector 局部最优已扫净。
⑤ **窗口不能随意缩**：分母窗 66→22 无增益（S +0.00、TO +6.38pp、margin −5.45bp）；分子窗 66→22 损 S（−0.39）且 TO 翻倍。66+250 是实测局部最优。
⑥ **裸 vec_count 频次不能当主信号**：`rank(ts_sum(vec_count(shares),66))` 0.77，远低于复合 1.23/1.27 ⇒ 频次只配当分母件。
⑦ **未测清单**：shares 裸 IR 腿、分子裸腿（`group_rank(rank(Δmean66),sector)`——全战役最大归因缺口）、分子窗 126、self-corr、生产档配置（D6）。

**失效反例**

- **不可外推成「shares 口径可用」**：分母换 shares 通道赢，不代表 shares 当主信号好——11-16 批实测同一 `max÷sum` 统计量换到 shares 口径 S 从 valueeur 的 0.81 掉到 0.17；本杠杆分子仍是 holdings，shares 只出现在分母。
- **不可把块交换增益记到任一单 token 名下**（尤其不能记成「backfill 万能」）：3 token 同时变，单 token 消融未做；唯一已证的单 token 是 vec_avg vs vec_count（+0.04）。
- **不可据此判 vec_count 无用**：vec_count 变体同向 +0.07 复现了通道结论；它只是弱于 vec_avg，不是失效。

- 实测域：DEU/TOP500/D1/`insiders1`（provisional，未判死）/decay0。权威档案：`tracking/DEU/regular_tower/WAVE_rt-insiders-w3_20261117.md` §1 臂5/6、§2.1、§3、§10–§12；基线臂 `WAVE_rt-insiders-w2_20261117.md` §1 臂4、conc66 定义 `WAVE_rt-insiders-w2_20261116.md` §1 注；闸限 `src/wqb/wave_results_contract.py:84-90`、`tracking/DEU/config/thresholds.json:2-12`、prod 线 `src/wqb/config.py:512,532`；表达式逐字核验 `mcp__wqb-db__get_alpha_by_id`（XgaKMZwb id 46330 / A1x3AN0l id 46386 / XgaK0bWX id 46390）、波台账 `mcp__wqb-db__get_wave_result(DEU, rt-insiders-w3)` id 2238。

## 反模式（实测证伪，勿再投）

| 反模式 | 实测证据 |
|---|---|
| **同源合成**（等权 add / 乘法把**同一潜变量**的两腿拼一起） | BE250/BE242#9/BE257/BE252 四证全稀释（fnd90 0.84→0.49、fnd1 1.26→1.17）；闸5 同源豁免的 corr<0.7 假设在同族字段上不成立。⚠ **2026-11-16 边界修正**：**不同维度**两腿的乘法不在此列（杠杆 I：insd1 规模集中×事件新鲜 `d5aE63Ew` **0.89** > 两单腿 0.81/0.78，S/F/sub/margin 四项全高）；判据是「同一潜变量投影」而**不是「同数据集」** |
| **S-2Y 跷跷板**（设置级手段破不了 S 闸） | decay12/轴切换/平滑/锐化在 fnd1 上无一抬 S（1.43-1.49 反降），fnd1 靠结构跃迁（zscore 量级）破闸——S 卡壳先换结构再动设置 |
| **宽度塌缩入场**（平台集级 cov=0 或 lc<50 的集不开波） | digital_ad_spend lc25/sc25+CW 挂、alpha_factor_lib DD 71-199% 超窄账户签名——**数据层排除≠信号死**，登记口径见判死分层 |
| **tail 跨核外推**（把三年窗核的 tail 增益搬到任意核） | w3 增量 ROA 核同波干净对照：裸 C0 1.48/1.02 → tail0.12 1.35/0.86（S −0.13/F −0.16）、tail0.15 1.43/0.93（S −0.05/F −0.09）；w4 又证字段×带宽交互（oper_inc 0.10 / EBIT 0.08，无全族统一带宽）——tail 是核相关杠杆，换核必须重测 |
| **`trade_when(…, −1)` 兜底做空**（门控失败落满仓空头） | w3 臂4 `KPgnK2L1` 对同核臂1：S −0.40 / 2Y −0.53 / sub −0.36 / DD **+14.34pp**（DD 26.56%）⇒ 门控失败落 −1 制造长期空头偏置与来回摆动；insiders1 由「未测」改「实测负」（杠杆 J §失效反例） |

## 通用纪律

- **近闸 prod 前置（用户 2026-11-14 明令）**：候选达到**近闸**（S≥1.2 或距任一硬闸 ≤0.4）时，**先 `check_correlation(production, refresh=True)` 探 prod，再决定是否继续网格扫参**——prod 雷在核心不在搭档，同核变体共 prod 命运；prod 堵则整族停手换核，prod 净才烧扫参配额（model238 54 臂后才发现 0.77 堵的反例；wpoXmKGv 1.35 时即探得 0.6805 净的正例）。
- 每个杠杆先做**归因对照**（裸跑 vs 加杠杆同批）再入册，禁止无对照入册。
- 跨区移植前 2 槽小批先验方向（TWN/KOR/DEU 符号翻转先例见 [['_basket-and-atom']] §四）。
- 同一经济腿只贡献 1 颗（clone 相关 self 0.96 实例）。

## 收割与克隆墙（2026-11-21 战役新增，详见 [['_harvest-and-clone-wall']]）

- **★ 收割顺序**：`prod` → **本地** `check_self_correlation` → **本地** `compute_mutual_correlation` → 逐年 longCount/pnl。28 颗 prod 未超线候选（阈值见 `config.PRODCORR_CEILING`）里 **self-corr 挂 11 颗**、篮内互相关挂 9 颗、**prod 挂 0 颗** ⇒ 两个本地闸零配额零等待，应紧跟 prod 之后做。
- **★ 收割分母用 `pyramids.effective ≥ 1`（≤2 塔）**，不是「塔位是否点亮」：DEU 池 925 → 484（≤2 塔）→ 28（prod 未超线，阈值见 `config.PRODCORR_CEILING`）→ 17（self 过）→ **6**（篮内互相关过）。
- **★ 判 self 闸只认 `check_self_correlation` 的 `max_correlation`**，不认 `alphas.self_correlation` 列（实测 `GrmPOz05`：DB 记 0.3136 / 本地 OS 池实测 **0.9038**）。
- **★ 「换字段」不能当梯度用**：`sentiment7 × sentiment27` 残差化族换 `snl27` 中性化目标（分位/中心/形状三类）产出 **6 颗 RA-clean**（S 1.84–1.94 / 2Y 2.18–2.46），**族内互相关 0.77–0.999**、对已提交件 `bl6OWZ2M` **0.932–0.976** ⇒ 6 颗只有 1 条独立信息且被 OS 池占位，**全撞 self-corr 0.70**。同族冗余度高时梯度必须换**信息源**。
- **★ 跨区移植比值形态先做 2 槽小批先验**：EUR 已交付的内部人「金额 ÷ 股数」比值移植 DEU ⇒ S **0.37** / 2Y **−0.41**。但 **self-corr 仅 0.038**（与 OS 池完全正交）⇒ **形态不迁移 ≠ 机制无价值**：是干净的**新信号位储备**，缺强度杠杆。
- **★ 平台 prod 相关性服务会账号级熔断**：`status=platform_unavailable` + `retry_after` 递减但**每次重试都拉长冷却期** ⇒ 熔断期内不重试，先做本地闸；`inflight=true` 时不重新触发。
- **★ 会话内 MCP 参数类型会被压平**：整数透传、**浮点/布尔被转字符串** ⇒ `truncation` / `filter_sharpe` / `refresh` / `threshold` 传不进去。绕过＝用 MCP 客户端直连同一个 `main.py` 服务（见 [['_harvest-and-clone-wall']] §七）。
