# WAVE rt-fundamental-w2 — fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 主集：`fundamental72`（目标塔 FUNDAMENTAL）；配对集：`insiders1`（塔 INSIDERS）
- 配置（平台回显，逐臂一致）：DEU/TOP500/D1、neutralization=FAST、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR；平台回显 `startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:16-17`（2013-01-01 起）不同。`create_multi_simulation` 无 startDate/endDate 参数（`world-quant-brain-mcp/tools_sim.py:672-690` 只构造 testPeriod），本档原样记录平台回显值，不推断。
- 派发/收割链（收割说明转录）：create_multi_simulation 单波 10 臂 → multisim `1T5fJWehu4WEb8P1555KUjOF`；batch_status 2 次至 `child_count=10/terminal=10/errors=0`；harvest_multisim_alphas 首试成功（未走 404 兜底）；upsert_backtest_rows(DEU, rt-fundamental-w2, fundamental72, 10 行) → n=10。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / sub≥1.0（本地 review 线；平台 LOW_SUB limit 动态，本波实读 0.61/0.15）/ TO 0.01–0.70 / margin≥0.0005（5bp，`tracking/DEU/config/thresholds.json:7`）/ prod&self corr≤0.70；CW 用**平台 limit 0.1**（`thresholds.json:20` 的 0.5 只是本地 review 线）。
- 2Y 闸种：本波 **10/10 臂均为单数据集件**（expressions `atom_flag=atom`、`atom_n_datasets=1`），全部走 `LOW_2Y_SHARPE`（limit 1.58）；**无多数据集件**，故 IS_LADDER 三处一致验收条款本波不适用（如实登记，不虚构）。
- 符号指纹：本波**仍无翻符号对照臂**（0 条 multiply(-1,…)；decay 固定 0），只有 arm3 的 `sign(δ176)` 二值腿（是幅度压缩，不是整式反号）。⇒ 本波不对方向做裁定（详见 §3）。

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | alphaId | 结构（简） | S | F | 2Y（LOW_2Y） | sub | TO | DD | margin | LC/SC | 塔（effective） | RA fail（DB `ra_failed_checks`） |
|---|---|---|---|---|---:|---|---:|---:|---|---:|---|---|
| 1 | MP682NMo | `group_zscore(三窗乘(δ240×δ176×ts_rank1008), sector)`；p=oper_inc÷tot_asset | 1.29 | 0.83 | 0.81 | 0.50（<0.61） | 16.66% | 7.40% | 0.000824 / 8.24bp | 168/214 | FUNDAMENTAL×1.8（1） | 4：[LOW_SHARPE, LOW_FITNESS, LOW_SUB, LOW_2Y]；CW pass |
| 2 | 78YX2R71 | `group_rank(multiply(ts_rank(δ240,252), ts_rank(δ176,252), ts_rank(p,1008)), sector)` | 1.30 | 0.79 | 1.93 | 0.90（pass） | 15.93% | 13.72% | 0.000735 / 7.35bp | 185/198 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS]；⚠ 平台 `checks.fail=[]`，两项在 warning 桶 |
| 3 | xAvzEpOl | `group_rank(multiply(rank(δ240), sign(δ176), rank(ts_rank(p,1008))), sector)` | 1.01 | 0.55 | 1.15 | 0.67（pass） | 15.12% | 5.66% | 0.000591 / 5.91bp | 185/197 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；CLUSTER 0.67 warning |
| 4 | gJaP0Vkl | 第二腿换毛利率轨迹 `g=sales_rev_turn÷cogs_to_fe_and_pp_and_g`，`rank(δg,252)` | 1.00 | 0.58 | 0.55 | 0.84（pass） | 14.61% | 7.50% | 0.000668 / 6.68bp | 159/223 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；CLUSTER 0.84 warning |
| 5 | YPak9o6q | **增量 ROA 两腿**：`group_rank(multiply(rank(δ(oper_inc,240)÷ts_mean(assets,240)), rank(ts_rank(p,1008))), sector)` | **1.52** | **1.05** | 1.67 | 0.98（pass） | 15.20% | 8.42% | 0.000953 / 9.53bp | 185/198 | FUNDAMENTAL×1.8（1） | **1：[LOW_SHARPE 1.52<1.58]（唯一 FAIL）**；F/sub/2Y/CW/CLUSTER 全 pass |
| 6 | blaPK1XN | DuPont 两腿：`m=oper_inc÷sales_rev_turn`、`t=sales_rev_turn÷assets`；`group_rank(multiply(rank(δm,252), rank(δt,252)), sector)` | 1.14 | 0.67 | 0.80 | 0.74（pass） | 15.52% | 7.04% | 0.000691 / 6.91bp | 184/198 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；⚠ 平台 `checks.fail=[]`，三项在 warning 桶；CLUSTER 0.73 warning |
| 7 | d5a7PrpK | `tail(group_rank(三窗乘(δ240×δ176×ts_rank(p,1008)), sector), lower=0.12, upper=0.88, newval=0.5)` | **1.51** | **1.00** | **2.33** | **1.14** | 18.11% | 7.47% | 0.000869 / 8.69bp | 216/167 | FUNDAMENTAL×1.8（1） | **1：[LOW_SHARPE 1.51<1.58]（唯一 FAIL）**；F/sub/2Y/CW/CLUSTER 全 pass |
| 8 | vRAzoX8b | 同臂1 结构，p=`ebit÷tot_asset`（字段换 EBIT） | 1.46 | 0.98 | 1.86 | 0.86（pass） | 14.87% | 8.34% | 0.000899 / 8.99bp | 181/201 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 9 | 3q062vbZ | 纯 insiders M2：`group_rank(δ66(ts_backfill(vec_avg(insd1_holdings),132)), subindustry)` | 0.82 | 0.33 | 0.94 | 0.53（pass） | 22.22% | 8.47% | 0.000322 / 3.22bp | 151/232 | INSIDERS×1.6（1） | 4：[LOW_SHARPE, LOW_FITNESS, **CW 0.144689>0.1@2014-01-29**, LOW_2Y]；CLUSTER 0.52 warning |
| 10 | P05lAmWq | 纯 insiders M5 集中度：`group_rank(ts_mean(vec_max(insd1_valueeur)÷vec_sum(insd1_valueeur),66), subindustry)` | 0.32 | 0.09 | 0.43 | −0.03（<0.15） | 14.90% | 8.76% | 0.000158 / 1.58bp | 144/239 | INSIDERS×1.6（1） | 4：[LOW_SHARPE, LOW_FITNESS, LOW_SUB, LOW_2Y]；CLUSTER 0.20 warning |

- DB 回读（`logs/_tmp_rtfund_w2_readback.py` 同口径只读脚本，sqlite `mode=ro`）：10/10 行指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count` 一致；payload `settings`（FAST/decay0/TOP500/D1/2014-01-01→2023-12-31）逐臂一致；`pyramids` 与 ask 一致（臂1-8 FUNDAMENTAL、臂9-10 INSIDERS）。
- ⚠ **checks 表示不一致（平台原文，不猜不补）**：臂2（78YX2R71）与臂6（blaPK1XN）body 的 `checks.fail=[]`，但同一 body 的 `ra.failed_ra_count=2/3`、`ra_failed_checks` 含 LOW_SHARPE/LOW_FITNESS（臂6 另含 LOW_2Y），对应项在 `checks.warning` 带 value/limit。本档判「0 达标」以 `ra_failed_checks` 为准（AGENTS §8.7：RA 资格门失败含 WARNING/ERROR；`ra` 块是平台预算名单）；若只看 `checks.fail=[]` 会把臂2/6 误判成「全闸通过」。

## §2 逐臂归因条目

1. **臂1 MP682NMo**（`group_rank`→`group_zscore` 量级变换）：S 1.29/F 0.83/2Y **0.81**/sub 0.50/TO 16.66%/DD 7.40%/margin 8.24bp/LC 168-214；RA fail 4、CW pass。**vs w1 同结构基准 `LLKX7rxL`（group_rank，S 1.42/F 0.94/2Y 1.96/sub 0.91）**：S −0.13、F −0.11、**2Y −1.15（1.96→0.81）**、sub −0.41（0.91→0.50，平台 limit 0.61 实挂）。⇒ **group_zscore 量级变换在本族是全维负杠杆**，尤其打断 2Y 载体；不是"换壳等价"。
2. **臂2 78YX2R71**（`rank(δ)`→`ts_rank(δ,252)` 时序秩替换截面秩）：S 1.30/F 0.79/2Y 1.93/sub 0.90/TO 15.93%/DD 13.72%/margin 7.35bp/LC 185-198；RA fail 2（checks.fail 空，见 §1 注）。**vs 基准**：S −0.12、F −0.15、**2Y −0.03（1.96→1.93，基本保住）**、sub −0.01（0.91→0.90）。⇒ 2Y 载体在「秩化+分组」而非截面秩的具体形态；S/F 面时序秩略弱。DD 13.72% 为基本面臂中最高。
3. **臂3 xAvzEpOl**（`sign(δ176)` 二值腿替换 `rank(δ176)`）：S 1.01/F 0.55/2Y 1.15/sub 0.67/TO 15.12%/DD 5.66%/margin 5.91bp/LC 185-197；RA fail 3、CLUSTER 0.67 warning。**vs 基准 1.42/0.94/1.96/0.91**：S −0.41、F −0.39、2Y −0.81、sub −0.24。**二值化丢掉幅度=稀释**（与 w1 的 trade_when 二值门控臂 S 0.30–0.79 同一指纹：把连续信息腿换成二值腿即稀释）。
4. **臂4 gJaP0Vkl**（第二腿换毛利率轨迹 `g=sales_rev_turn÷cogs_to_fe_and_pp_and_g` 的 `rank(δg,252)`）：S 1.00/F 0.58/2Y 0.55/sub 0.84/TO 14.61%/DD 7.50%/margin 6.68bp/LC 159-223；RA fail 3、CLUSTER 0.84 warning。vs 基准：S −0.42、F −0.36、2Y −1.41、sub −0.07。⇒ 毛利率轨迹腿在 DEU/TOP500 本族无增益（FIELD_fundamental72 §6 T6 的机制假设本波实测弱）；LC 159 为本波基本面臂最低（仍 >100，非塌缩）。
5. **臂5 YPak9o6q**（**增量 ROA 两腿**）：S **1.52**/F **1.05**/2Y 1.67/sub 0.98/TO 15.20%/DD 8.42%/margin 9.53bp/LC 185-198；**唯一 FAIL=LOW_SHARPE（差 0.06）**，CW/CLUSTER/2Y/sub/F 全 pass。**跨波对照**：vs w1 裸基准 LLKX7rxL（1.42/0.94/1.96/0.91）→ S +0.10、F +0.11、2Y −0.29、sub +0.07；vs w1 单腿 omazqreb（1.29/0.84/0.79/0.48）→ **S +0.23、F +0.21、2Y +0.88、sub +0.50**（对单腿全维增益，不稀释）。⚠ 相对基准是**复合改造**（去掉 δ176 腿 + 把 `δ(p)` 换成 `δ(oper_inc)÷ts_mean(assets,240)`），**两变量捆绑、单变量未拆**，不能作为"增量 ROA 杠杆"的严格归因；但读数本身是干净的活体：**S 1.52 破 fnd72 族峰 1.50（mLaALJX2）**。
6. **臂6 blaPK1XN**（DuPont 两腿：净利率 δm × 资产周转 δt，各 252 窗）：S 1.14/F 0.67/2Y 0.80/sub 0.74/TO 15.52%/DD 7.04%/margin 6.91bp/LC 184-198；RA fail 3（checks.fail 空）、CLUSTER 0.73 warning。vs 基准：S −0.28、F −0.27、2Y −1.16、sub −0.17。⇒ DuPont 两腿分解低于三窗动量基准；分解后的两个 delta 腿没有比"单一 ROA 动量的三窗乘积"更强（注意：这是**基准对照**，不是与两条单腿的严格稀释判定——两条 DuPont 单腿本波未单测）。
7. **臂7 d5a7PrpK**（**tail 壳**：`tail(group_rank(三窗乘, sector), 0.12/0.88/0.5)`）：S **1.51**/F **1.00**/2Y **2.33**/sub **1.14**/TO 18.11%/DD 7.47%/margin 8.69bp/LC 216-167；**唯一 FAIL=LOW_SHARPE（差 0.07）**，F/sub/2Y/CW/CLUSTER 全 pass。**跨波单变量对照（裸→改造）**：w1 LLKX7rxL（1.42/0.94/1.96/0.91，同字段同几何同配置）→ 本臂：**S +0.09、F +0.06、2Y +0.37、sub +0.23**；对族峰 mLaALJX2（1.50/1.04/2.30/1.12）：S +0.01、F −0.04、2Y +0.03、sub +0.02、TO +1.80pp、margin −0.86bp。⇒ **tail 0.12/0.88/0.5 单独包裹即可复现族峰级 S/2Y/sub，无需 winsorize(std3)+hump(0.003)**；代价是 F 1.00 vs 1.04、margin 8.69 vs 9.55bp（仍全过线）。**这是本波唯一可做单变量归因的跨波改造**（§9）。
8. **臂8 vRAzoX8b**（字段换 EBIT：`ebit÷tot_asset`）：S 1.46/F 0.98/2Y 1.86/sub 0.86/TO 14.87%/DD 8.34%/margin 8.99bp/LC 181-201；RA fail 2。**跨波单变量字段对照**：w1 LLKX7rxL（oper_inc）1.42/0.94/1.96/0.91 → EBIT：S +0.04、F +0.04、2Y −0.10、sub −0.05。⇒ EBIT 与 oper_inc 在 S/F 面近似、2Y/sub 略降；**字段排序随指标轴反转，不能单轴外推**（与 11-15 atom 档"字段×几何交互"同型，但本波是单变量字段差，仅作敏感度登记，不入杠杆）。
9. **臂9 3q062vbZ**（insiders M2 变体：`vec_avg` + 132 回填）：S 0.82/F 0.33/2Y 0.94/sub 0.53/TO 22.22%/DD 8.47%/margin 3.22bp/LC 151-232；RA fail 4、CW **0.144689**@2014-01-29、CLUSTER 0.52 warning。**跨波单变量口径对照**：w1 臂10 mLazj129（`vec_sum`+250 回填）S 0.83/F 0.33/2Y 0.78/sub 0.35，**CW 同为 0.144689** ⇒ 换聚合/窗口后 **S/F 不变（0.83→0.82）**、2Y +0.16、sub +0.18、CW 逐位相同。⇒ **insiders 的 S 面弱不是 vec_sum/vec_avg 或 132/250 造成的**；CW 值逐位相同说明 CW 由子行业分组暴露主导（数据层指纹），不随聚合口径变化。与 FIELD 档「A 单腿 Δ66 S 1.72」的 0.89 差仍**未解析**，不判 insiders1 死。
   - **查重偏离（如实登记，待派发方裁定）**：本臂 normalized code 与旧件 `MP6jkd88`（wave=`mcp-20261110`，SUBINDUSTRY/decay4）全同；旧件平台读数 S 0.78/F 0.49/2Y 0.82/sub 0.26/TO 8.02%/DD 10.68%/margin 0.001221/CW 0.5。本波 FAST/decay0 下平台返回新 id 3q062vbZ（读数见上）⇒「同表达式必回同 id」跨设置不成立。本档按「同 code 不同配置=合法对照臂」保留读数并完整登记；**若派发方按严格查重规则剔除，臂9 不进入任何结论**（S 0.82 不在近闸、不影响 best S/2Y、verdict、datasetStatus），偏离对波次结论无影响；是否作废 3q062vbZ 属派发方/用户裁定，本档不自行剔除。
10. **臂10 P05lAmWq**（insiders M5 日内集中度：`vec_max(valueeur)÷vec_sum(valueeur)` 的 66 日均值）：S 0.32/F 0.09/2Y 0.43/sub **−0.03**/TO 14.90%/DD 8.76%/margin 1.58bp/LC 144-239；RA fail 4、CW pass、CLUSTER 0.20 warning。vs w1 纯 insiders M2 0.83：S −0.51、F −0.24、2Y −0.35；sub −0.03 低于平台 limit 0.15 实挂。⇒ FIELD_insiders1 §6 标为"真正新增几何"的 M5 在 DEU/TOP500 本波实测为**最弱臂**；单臂探针，不判 insiders1 数据集死。

## §3 符号指纹 / 稀释铁律 / 跨区核对

- **符号指纹：未测（无翻符号对照臂）**。本波 10 臂全为正向构造；臂3 的 `sign(δ176)` 是**幅度二值化**（sign 保留方向、丢幅度），不是整式反号（无 `multiply(-1, …)`）。⇒ 不能按「衰减对称=机制在/符号错；单向=事件型」判定；本波不对方向做裁定。近闸件（YPak9o6q / d5a7PrpK）推进前应补一条整式反号对照（FIELD_insiders1 §5 同源要求；w1 档已登记该缺口，本波仍未补）。
- **稀释铁律**：以同核心单腿基准 w1 `omazqreb`（S 1.29）对照——**命中**：臂3 1.01、臂4 1.00、臂6 1.14 均低于单腿（复合/换腿后低于对应单腿 ⇒ 稀释）；**不触发**：臂1 1.29（持平）、臂2 1.30、臂5 1.52、臂7 1.51、臂8 1.46 均 ≥ 单腿（臂5/7 对单腿 +0.23/+0.22）；**无 bucket 臂**（本波零 bucket，w1 的 bucket 经验不适用于本波）。判据与 w1 一致：**第二腿是连续 rank 信息腿→增益；二值/门控腿→稀释**；本波新增一例：**量级变换（group_zscore）与字段替换（毛利率/DuPont）也可低于单腿**，属"非信息性替换"。
- **跨区不外推**：零 TWN/KOR 引用；对照全部 DEU 域内（w1 LLKX7rxL/omazqreb、atom 槽 mLaALJX2、本波波内）。insiders1 既有证据（1.72/2.36）只作口径对照，不作跨区/跨波增益承诺；fnd45/fnd86/fnd89/fnd90 邻接集先验未改写。
- **配置维**：全波固定 FAST / decay=0 / TOP500 / D1 / trunc 0.08，未扫中性化/decay/宇宙/delay/trunc；族内既有 decay 单调负杠杆（0/2/4，NEARGATE §B4）⇒ 本波不派"加 decay 提 S"臂。

## §4 塔位判读（点塔相关性）

平台 payload `pyramids` 原文（逐臂回读）：

| 臂 | pyramids.list | effective | 塔相关性 |
|---|---|---|---|
| 1-8 | `DEU/D1/FUNDAMENTAL` ×1.8 | 1 | 点 fundamental 塔 |
| 9-10 | `DEU/D1/INSIDERS` ×1.6 | 1 | 点 insiders 塔（无 fundamental） |

- **目标塔 FUNDAMENTAL 出现 8/10 臂归属**（臂1-8）；**INSIDERS 塔 2/10**（臂9-10）。**本波零双塔件**（与 w1 的 5 条 effective=2 形成对照，w1 的双塔配腿在本波被拆掉）。
- **点位≠点亮**：10/10 臂 RA fail≥1，无一条过全闸；本波对塔位实际贡献 = 0（无可提交件）。
- **塔位观察**：告别双塔后，fundamental 单塔出现 1.52/1.51/1.46 三条强读数（w1 双塔件仅 0.30–0.79）⇒ 与 w1 的"insiders 配腿是负担"结论方向一致；本波进一步给出正面对照（去掉配腿后 S 更高）。但这是两波不同臂的对照，不是同臂单变量拆腿，登记为**方向一致、非严格因果**。

## §5 数据层判读（data_excluded 与信号死分开）

- **本波零 data_excluded 臂**：LC/SC 144–239 全宽，无 LC/SC≤5；无宽度塌缩。fundamental72 `coverage=0` 是本集×本区平台元数据退化（FIELD_fundamental72 §2），不作可用性判据。
- **CW 挂闸 1 臂（臂9，insiders M2 变体）**：CW 0.144689>0.1@2014-01-29；纯 fnd72 臂 8/8 CW pass、insiders M5 臂10 CW pass。⇒ CW 挂是 **insiders1 的 holdings 字段数据层指纹**（`insd1_holdings` 250 日宽度 193/500=38.6%，FIELD_insiders1 §4.2；2014 初回填不足），不是信号死；不 data_excluded、不改符号重试。CW 值与 w1 臂10 逐位相同（0.144689），说明由子行业分组暴露主导。
- **insiders 读数的数据层边界**：M5 用 `insd1_valueeur`（250 日宽度 294/500=58.8%，FIELD_insiders1 §4.2），CW pass；M2 用 `insd1_holdings`（38.6%），CW 挂。**宽度差的直接影响可见**，但 M5 的 S 0.32 仍最弱 ⇒ 宽度不是唯一解释，机制本身弱。
- **无判死**：本波 10 臂但结构互异 <10（§6），按探针条款不判死；fundamental72 与 insiders1 均不判死。

## §6 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义 10 臂，互异机制 ~5：三窗动量乘（1/7/8，含量级/字段/壳变体）、时序秩替换（2）、二值腿（3）、毛利率/DuPont 字段分解（4/6）、增量 ROA（5）、insiders M2/M5（9/10）——其中 1/2/3/4/6/7/8 同属"动量乘族"的不同替换 | **✗ 未达**（互异机制 <10） |
| D2 字段族自测 | 本波碰 6 个 fnd72 字段（oper_inc、ebit、tot_asset、sales_rev_turn、cogs_to_fe_and_pp_and_g）+ 2 个 insd1 字段；fnd72 共 1031 字段 | **✗ 远未达** |
| D3 矩全家 | 一阶差（δ240/δ176/δ66/δ252）✓、比值（oper_inc÷assets、毛利率、DuPont、vec_max÷vec_sum）✓；**缺**二阶波动、信噪比、纯水平腿 | **✗ 未达** |
| D4 分组轴 ≥2 | sector（臂1-8）、subindustry（臂9-10） | ✓ |
| D5 非线性 ≥1 | ts_rank、group_rank、group_zscore、sign、tail、multiply | ✓ |
| D6 配置 ≥2 | 本波固定 FAST/decay0/TOP500/D1 **一套** | **✗ 本波自身未达**（跨槽累计有 SUBINDUSTRY 三波，非本波读数） |

⇒ 缺 D1/D2/D3/D6：**不得判死、不得封集、不得作为邻接集先验**（AGENTS §7.6）。本波为 **active 级推进**而非终态（§8）。

## §7 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `YPak9o6q` | **1.52** | S≥1.2；距 S 硬闸 1.58 差 **0.06**≤0.4；**唯一 FAIL=LOW_SHARPE**；F 1.05/2Y 1.67/sub 0.98/CW pass/CLUSTER pass/margin 9.53bp/TO 15.20%；**本波最佳且破族峰 1.50** |
| 2 | `d5a7PrpK` | **1.51** | S≥1.2；距 S 硬闸差 **0.07**≤0.4；**唯一 FAIL=LOW_SHARPE**；F 1.00/2Y **2.33**/sub **1.14**/CW pass/CLUSTER pass/margin 8.69bp/TO 18.11%；**2Y/sub 双过线** |

- 排序外登记（如实）：`vRAzoX8b` S 1.46（距 0.12）、F 0.98（距 0.02）多轴触发，按 S 降序第 3 出局；`78YX2R71` S 1.30（F 0.79、2Y 1.93、sub 0.90）第 4；`MP682NMo` S 1.29（sub 0.50 距 0.61 差 0.11）第 5。机械上"距任一硬闸 ≤0.4"还覆盖臂3/4/6 的 S/F 差值与臂9/10 的 CW/sub 差值，均按 S 降序出局（§1 已列全量）。
- **prod/self 未测（本波全 null，相关性查询按分工未做）**：候选 `YPak9o6q` / `d5a7PrpK` 均为 fnd72 核心件（非 insiders 搭档）——按「prod 雷在核心不在搭档」，先测这两条 prod 再决定扫参。族内先验 `mLaALJX2` prod 0.5444（<0.70）是利好但不同表达式，不构成保证。
- **年度分年未取（本波未跑 get_alpha_yearly_stats）** ⇒ 2018/2019/2020 时间集中度**未验证**。族级既有读数（`S0_TOWER_SCAN_20261115.md:130`：mLaALJX2 2018 0.80/2019 0.80/2020 −0.35，2021–2023 3.03/2.60/1.96）提示该族存在时间集中风险。**推进前必须补分年**；若 2018/2019/2020 仍全 <1.0 而总 S 靠 2021–2023 撑起，按「时间集中度风险」登记，**不得按可提交推进**。
- **mode_b_qualification**（`thresholds.json:23-27`）：本波最强 YPak9o6q S 1.52≥1.25 且 F 1.05≥0.8 **双过资格线**；d5a7PrpK S 1.51/F 1.00 同样过线 ⇒ 有资格进 Mode B 组合增强/继续优化（与 §8 的 active 判定同向）。

## §8 datasetStatus 裁决 + 波 verdict

**datasetStatus = active（继续加注；自 provisional 升档）**。依据：

1. **S 面破族峰**：臂5 S 1.52 / 臂7 S 1.51，双破 fnd72 既有族峰 1.50（mLaALJX2，`S0_TOWER_SCAN_20261115.md` §4.3）与 11-15 atom 槽 FAST 轮 best 1.47（ZYaqv2L0）；F 1.05/1.00 亦破/平族峰 1.04。距 S 全闸仅 0.06–0.07，且臂7 的 2Y 2.33/sub 1.14 双过线。
2. **与 standing state 的关系**：`CATEGORY_MATRIX_FUNDAMENTAL_20261115.md` §5 的 fnd72 standing state 是 provisional（判弱入档），其依据是 SUBINDUSTRY 三波 best 0.68/0.25/0.21；本波读数方向相反且有新增突破 ⇒ 按 atom 槽 w1 先例（1.47>1.42 → active）升 **active**，**不是** capped/dead/data_excluded。
3. **无数据层排除**：LC/SC 144–239 全宽；纯 fnd72 臂 8/8 CW pass；唯一 CW 挂臂（9）属 insiders 数据层指纹。
4. **不得判死**：D1/D2/D3/D6 未达（§6），AGENTS §7.6 六维闸禁止终判死；本波不作邻接集先验。
5. **insiders1 不判死**：本波只有 2 条纯 insiders 结构（M2 变体、M5 集中度），结构互异 <10；M2 S 0.82 与 w1 0.83 复现、M5 0.32 最弱；CW 挂属数据层。记「本波不产出可推进 insiders 结构」，不记死、不 data_excluded。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 近闸 ⇒ PARTIAL；`n_pass=0 / n_near=2`）。禁止自造枚举。

## §9 newLever 登记

**tail 0.12/0.88/0.5 壳（跨波单变量已证）**：
- **裸 vs 改造**：w1 `LLKX7rxL`（=`group_rank(multiply(rank(δ240), rank(δ176), rank(ts_rank(p,1008))), sector)`，S 1.42/F 0.94/2Y 1.96/sub 0.91/TO 15.28%/margin 8.69bp）→ w2 `d5a7PrpK`（同式外裹 `tail(..., lower=0.12, upper=0.88, newval=0.5)`，S 1.51/F 1.00/2Y 2.33/sub 1.14/TO 18.11%/margin 8.69bp）：**S +0.09 / F +0.06 / 2Y +0.37 / sub +0.23**，唯一差异是 tail 壳（同字段、同窗口、同 FAST/decay0/TOP500/D1、同 multisim 派发口径）。
- **附带发现（非杠杆，登记备查）**：本臂无 winsorize(std3)/hump(0.003) 也达到 mLaALJX2 级 S/2Y（1.51/2.33 vs 1.50/2.30），F 1.00 vs 1.04、margin 8.69 vs 9.55bp——tail 单独贡献已足够过 S/2Y/sub 三闸，hump 的边际价值主要在 F/margin/换手（本波不据此撤销 hump 杠杆，只是记录"可简化"候选）。
- **caveat**：① w1/w2 是相邻波但非同一 multisim，派发时点/平台队列不同，严格复现需同批裸/壳对照；② tail 已在 NEARGATE §B5/B8 作为族内尾部压缩器入册（tail 0.12–0.15 峰），本波是把该杠杆在 regular_tower 谱系上做**单变量跨波确认**，不是全新机制；③ 2Y 增益 +0.37 大于 S +0.09，验证"tail 主要拉时间维/子宇宙"的定位。

## §10 证据通道与盲区

- **读数来源**：ask 转录的 harvest 回传（每臂 metrics/checks/ra/pyramids/settings）+ 本槽只读核验（sqlite `mode=ro`，零写入）：10/10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count`/名单一致；payload `settings` 与 ask 一致；`pyramids` 与 ask 一致（8 条 FUNDAMENTAL、2 条 INSIDERS）。
- **IS_LADDER**：本波 10/10 臂 `atom_n_datasets=1`（单集件），全部走 LOW_2Y_SHARPE；DB `alphas.is_ladder_sharpe` 全 null 与"无多数据集件"一致 ⇒ **三处一致条款本波不适用**（不是漏检）。
- **checks 表示不一致**：臂2/6 的 `checks.fail=[]` 与 `ra.failed_ra_count=2/3` 并存；本档以 ra 名单判 0 达标，`checks.fail` 原文照录（§1 注）。这是 AGENTS §8.7「RA 资格门失败含 WARNING」的直接实例。
- **查重偏离**：臂9 与旧件 MP6jkd88 同 code（不同配置）；本档保留并标注，剔除与否不影响任何结论（§2.9）。
- **盲区（如实登记）**：
  1. 年度分年未取 → 时间集中度未验证（§7）；2018/2019/2020 未读数，不填数；
  2. prod/self 相关性未测（10 臂全 null）；
  3. `operator_audit` 对原 10 条多语句表达式解析失败 `error: Unexpected character at position 79`（与 w1 同一工具限制）——如实记 error、不作无解证据；补充正证：展开单语句 10 条 `safe=true`、violations=[]、ghost_operators 不含本波任何算子；
  4. `preflight_expressions` 的 `unknown_fields=[g,m,p,t]` 为多语句左值变量（赋值目标），非字段；7 个真实字段已验存（platform_field_count=7）、`any_changed=false`、fixed 与原文逐字相同；
  5. create_multi_simulation 不暴露 startDate/endDate（`tools_sim.py:672-690`），平台回显 2014-01-01→2023-12-31 与 settings.json 的 2013-01-01 不同——原样记录平台值，不推断；
  6. 本波结构互异 <10，按探针条款不产生判死；六维 D1/D2/D3/D6 未达。
- **跨槽纪律**：本波（regular_tower / `rt-fundamental-w2`）与 atom_orthogonal 槽的 fnd72 `w1/w2/w3` 是不同波标签，读数不合并、本档不覆写其档案；standing state 引用 `CATEGORY_MATRIX_FUNDAMENTAL_20261115.md` §5。

## §11 终态

- **波**：PARTIAL；0 达标 / 2 近闸；best S **1.52**（YPak9o6q）/ best 2Y **2.33**（d5a7PrpK）；两臂均只差 LOW_SHARPE 0.06–0.07。
- **数据集**：fundamental72 = **active**（自 provisional 升档；S 1.52/1.51 破族峰 1.50，F 1.05 破 1.04，2Y 2.33 破 2.30；D1/D2/D3/D6 未达 → 不判死、不封集）；insiders1 = 本波无可推进结构、**不判死**（探针 + D1 未达）。
- **提交链**：无（0 达标，无候选进入提交语境）。
- **下一波输入**：① 先测 `YPak9o6q` 与 `d5a7PrpK` 的 prod/self，再补 2018–2020 分年；② S 侧离闸 0.06–0.07，最小改造优先在 tail 壳上加已入册 hump 0.003（对照臂：tail vs tail+hump，单变量）或做 tail 带宽 0.10/0.15 微调（族内已证 0.12–0.15 峰，须单变量）；③ 不要动 decay（族内 0/2/4 负杠杆）；④ 增量 ROA（臂5）与 tail 壳（臂7）是两条独立活体，可做 2×2 交叉（增量 ROA × tail）但需单变量拆解；⑤ insiders 腿暂停加注（S 0.32–0.82、CW 挂），除非先解 1.72 口径差。

## §12 事后更正（2026-11-16，w3 档复核 expressions 原文）

- 本档 §9/newLever 写「w1 `LLKX7rxL` → w2 `d5a7PrpK` 唯一差异是 tail 壳」**不成立**：两式还差 `rank(ts_rank(p,1008))` vs `ts_rank(p,1008)`（w1 有外层 rank，w2 无）。w1→w2 实际是「加 tail + 去 ts_rank 外层 rank」两变量，**不能把 +0.09/+0.06/+0.37/+0.23 全部记到 tail 名下**。
- 干净带宽对照改由 w3 档 §3 给出（三臂同为 raw `ts_rank`，只差带宽）：0.10（`O0WmdbPR` 1.56/1.05/2.41/1.18）vs 0.12（`d5a7PrpK` 1.51/1.00/2.33/1.14）vs 0.15（`88N6Wa9W` 1.53/1.02/2.10/1.09）。
- 本档原文不回改；以本条 + w3 档为准。
