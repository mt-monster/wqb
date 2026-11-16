# WAVE rt-fundamental-w1 — fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 主集：`fundamental72`（目标塔 FUNDAMENTAL）；配对集：`insiders1`（塔 INSIDERS）
- 配置（平台回显，逐臂一致）：DEU/TOP500/D1、neutralization=FAST、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR；平台回显 `startDate=2014-01-01`、`endDate=2023-12-31`
  - ⚠ 与 `tracking/DEU/config/settings.json:16-17`（2013-01-01→2023-12-31）不同。`create_multi_simulation` 不暴露日期参数（`world-quant-brain-mcp/tools_sim.py:672-690` 只构造 testPeriod），本档原样记录平台回显值，不按 settings.json 改写、不推断。
- 派发/收割链（收割说明转录）：create_multi_simulation 单波 10 臂 → multisim `4lMJsK7Xc4AXaUX18tp4QBBq`；batch_status 4 次轮询至 `child_count=10/terminal=10/errors=0`；harvest_multisim_alphas 首次即成功（未走 404 兜底）；upsert_backtest_rows(DEU, rt-fundamental-w1, fundamental72, 10 行) → n=10。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / sub≥1.0（本地 review 线；平台 LOW_SUB_UNIVERSE_SHARPE limit 动态，本波实读 0.61/0.69/0.37/0.39）/ TO 0.01–0.70 / margin≥0.0005（5bp，`tracking/DEU/config/thresholds.json:7`）/ prod&self corr≤0.70；CW 用**平台 limit 0.1**（`thresholds.json:20` 的 0.5 只是本地 review 线，不作验收）。
- 2Y 双闸（本波实测口径）：单集件走 `LOW_2Y_SHARPE`（limit 1.58）；多数据集件（effective=2）走 `IS_LADDER_SHARPE`（limit 1.58 / year=2），`checks.pass` 不再含 LOW_2Y。本波 5/5 多集件三处一致（见 §10）。

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | alphaId | 结构（简） | S | F | 2Y（闸种） | sub（平台 limit） | TO | DD | margin | LC/SC | 塔归属（effective） | RA fail |
|---|---|---|---|---|---:|---|---:|---:|---|---:|---|---|
| 1 | LLKX7rxL | 三窗乘：rank(δ240)×rank(δ176)×rank(ts_rank1008)，group_rank(sector)；p=oper_inc÷tot_asset | **1.42** | 0.94 | 1.96（LOW_2Y PASS） | 0.91（PASS） | 15.28% | 9.30% | 0.000869 / 8.69bp | 185/198 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE 1.42<1.58, LOW_FITNESS 0.94<1.0]；CW PASS |
| 2 | Xgal7eEb | 同臂1 去 group_rank(sector) | **1.45** | **1.01** | 0.96（LOW_2Y 0.96<1.58） | 0.55（<0.69） | 16.38% | 5.64% | 0.000977 / 9.77bp | 168/214 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE] |
| 3 | omazqreb | 单腿 rank(δ240) | 1.29 | 0.84 | 0.79（LOW_2Y 0.79<1.58） | 0.48（<0.61） | 15.80% | 6.43% | 0.00085 / 8.50bp | 191/191 | FUNDAMENTAL×1.8（1） | 4：[LOW_SHARPE, LOW_FITNESS, LOW_SUB, LOW_2Y] |
| 4 | RRea7KXa | trade_when(δ66 insiders 持股>0, 裸腿 δ240, 0) | 0.39 | 0.15 | 0.35（IS_LADDER 0.35<1.58, year=2） | 0.38（PASS） | 19.96% | 16.25% | 0.000298 / 2.98bp | 189/197 | INSIDERS×1.6 + FUNDAMENTAL×1.8（2） | 4：[LOW_SHARPE, LOW_FITNESS, **CW 0.168503>0.1@2014-08-22**, IS_LADDER] |
| 5 | 6XMqlJxK | trade_when(vec_count(insiders)>0, 裸腿 δ240, 0) | 0.45 | 0.18 | −0.01（IS_LADDER −0.01, year=2） | 0.27（PASS） | 18.99% | 14.18% | 0.000322 / 3.22bp | 189/193 | INSIDERS + FUNDAMENTAL（2） | 4：[LOW_SHARPE, LOW_FITNESS, **CW 0.144418>0.1@2014-02-14**, IS_LADDER] |
| 6 | pwazjZ0b | multiply(裸腿 δ240, greater(δ66 insiders 持股,0)) | 0.60 | 0.27 | 1.41（IS_LADDER 1.41<1.58, year=2） | 0.33（PASS） | 25.82% | 38.84% | 0.000396 / 3.96bp | 151/218 | INSIDERS + FUNDAMENTAL（2） | 4：[LOW_SHARPE, LOW_FITNESS, **CW 0.313151>0.1@2015-05-21**, IS_LADDER] |
| 7 | vRAzj6aa | trade_when(vector_neut(insiders 流, 裸腿)>0, 裸腿, 0) | 0.79 | 0.43 | 0.12（IS_LADDER 0.12, year=2） | 0.76（PASS） | 19.75% | 14.38% | 0.000598 / 5.98bp | 187/199 | INSIDERS + FUNDAMENTAL（2） | 4：[LOW_SHARPE, LOW_FITNESS, **CW 0.172248>0.1@2014-09-11**, IS_LADDER] |
| 8 | ZYal7Mkn | trade_when(ts_delta(ts_mean(裸腿,66),252)>0, 裸腿, 0)（**纯 fnd72 时序门控**） | 0.78 | 0.40 | −0.47（LOW_2Y −0.47<1.58） | 0.36（<0.37） | 14.92% | 14.13% | 0.00052 / 5.20bp | 190/192 | FUNDAMENTAL×1.8（1） | 4：[LOW_SHARPE, LOW_FITNESS, LOW_SUB, LOW_2Y]；**CW PASS** |
| 9 | N1Pj73k8 | insiders 主体（group_rank/δ66/subindustry）+ trade_when(fnd72 δ66>0) | 0.30 | 0.10 | 0.85（IS_LADDER 0.85, year=2） | 0.21（PASS） | 18.82% | 23.49% | 0.000211 / 2.11bp | 167/216 | INSIDERS + FUNDAMENTAL（2） | 4：[LOW_SHARPE, LOW_FITNESS, **CW 0.271844>0.1@2014-02-18**, IS_LADDER] |
| 10 | mLazj129 | 纯 insiders：group_rank(δ66(ts_backfill(vec_sum(insd1_holdings),250)), subindustry) | 0.83 | 0.33 | 0.78（LOW_2Y 0.78<1.58） | 0.35（<0.39） | 21.96% | 7.08% | 0.00032 / 3.20bp | 162/220 | INSIDERS×1.6（1，无 fundamental） | 5：[LOW_SHARPE, LOW_FITNESS, **CW 0.144689>0.1@2014-01-29**, LOW_SUB, LOW_2Y] |

- 平台 checks 原文（payload.checks.fail）逐臂回读与上表 RA fail 10/10 一致；上表 2Y/sub 平台 limit 值取自 checks.fail 原文（PASS 项不返回 limit，故臂1 的 sub/single 2Y 只记 PASS 不补 limit）。
- margin 换算：平台原值 ×10000 = bp（`Claude/skills/wq-brain-campaign-toolkit/scripts/metrics_cache.py:117`、`tools/verdict/candidate_health_card.py:141`）。低于 0.0005 的臂：4/5/6/9/10（2.11–3.96bp）。

## §2 逐臂归因条目

1. **臂1 LLKX7rxL**（三窗乘法 + group_rank(sector)，q_is_oper_inc÷tot_asset）：本波最接近全闸的 fundamental 核心件——S 1.42（差 0.16）、F 0.94（差 0.06）、2Y 1.96 ✓、sub 0.91（本地 1.0 未达但平台 PASS）、TO 15.28%、margin 8.69bp、CW PASS、LC/SC 185/198。**跨形同字段对照**：既有 `KPJmRpGN`（同三腿 sector + q_is_oper_inc，DB S 1.38/F 0.90/2Y 1.58/sub 0.92）→ S +0.04 / F +0.04 / 2Y +0.38 / sub −0.01；族峰 `mLaALJX2`（S 1.50/F 1.04/2Y 2.30，带 tail 0.12 + hump 0.003）→ S −0.08 / F −0.10 / 2Y −0.34。⚠ 臂1 未叠已入册的 tail/hump 压缩器；与 KPJmRpGN 的差还含 decay/窗口配置差（本波 decay=0、平台回显 2014 起）——**单变量未拆，不记为杠杆、不记为新证据**。符号/机制定位：与族内既有近闸件同向（盈利改善→做多），但本波无翻符号臂（§3）。
2. **臂2 Xgal7eEb**（同臂1 去 group_rank sector）：**本波最佳 S 1.45（距闸 0.13）、F 1.01 已过 fitness_min**、DD 5.64% 本波最低；但 2Y 0.96（距 1.58 差 0.62）、sub 0.55（<0.69，差 0.14）。**单变量对照（vs 臂1）**：去分组 → S +0.03、F +0.07、TO +1.10pp，但 **2Y −1.00（1.96→0.96）、sub −0.36（0.91→0.55）**。⇒ **group_rank(sector) 是 2Y 与 sub 的载体**：S/F 面可去，时间维与子宇宙不可去。这是本波最有价值的结构指纹（波内单变量、非跨波）。
3. **臂3 omazqreb**（单腿 rank(δ240) 基线）：S 1.29/F 0.84/2Y 0.79/sub 0.48（<0.61）/TO 15.80%/margin 8.50bp/LC 191-191。**vs 臂1 三窗乘法**：乘法 1.42/0.94/1.96/0.91 全维高于单腿 1.29/0.84/0.79/0.48 ⇒ **乘法复合相对单腿不稀释**（稀释铁律不触发）；S 主载荷在 δ240 动量腿本身，附加 ts_rank1008 与 sector 分组主要补时间维/子宇宙。vs 臂2（无分组乘法 1.45）：臂3 低 0.16，说明三腿乘法的 S 增益不来自分组（分组只在 2Y/sub 上兑现）。
4. **臂4 RRea7KXa**（trade_when(insiders 持股增加, 裸腿, 0)）：S 0.39/F 0.15/2Y 0.35（IS_LADDER, year=2）/sub 0.38/TO 19.96%/DD 16.25%/margin 2.98bp/**CW 0.168503 @2014-08-22**。**vs 裸腿（臂3 1.29）→ S −0.90** ⇒ 门控稀释。CW 挂 = **数据层指纹**：`insd1_holdings` 250 日宽度仅 193/500=38.6%（`FIELD_insiders1_20261115.md` §4.2），2014 年初回填历史不足、截面窄，CW 超 0.1；不是信号死，不改符号重试。
5. **臂5 6XMqlJxK**（trade_when(vec_count(insiders)>0, 裸腿)）：S 0.45/F 0.18/2Y −0.01（IS_LADDER）/sub 0.27/CW 0.144418@2014-02-14。vs 裸腿 −0.84 ⇒ 门控稀释；"有申报"条件（vec_count>0）比"持股增加"（δ66>0）更宽，S 略高 0.06 但 2Y 从 0.35 掉到 −0.01（时间维更差）。CW 数据层指纹同上。
6. **臂6 pwazjZ0b**（multiply(裸腿, greater(insiders 持股增加,0))）：S 0.60/F 0.27/2Y 1.41（IS_LADDER，距 0.17）/sub 0.33/TO 25.82%（本波最高）/DD 38.84%（本波最高）/margin 3.96bp/**CW 0.313151@2015-05-21（本波最高）**。**稀释铁律直接命中：乘法 0.60 < 对应单腿 1.29**（−0.69），且换手 +7.9pp、DD 爆到 38.8%——用一条弱二值信息腿乘核心动量不是增益而是放大噪声。2Y 1.41 是本波第二高但 S 全灭，记 S-2Y 跷跷板（与 11-15 atom 槽比值形同构的跷跷板指纹，但此处机制不同，不作跨波归因）。
7. **臂7 vRAzj6aa**（trade_when(vector_neut(insiders 流, 裸腿)>0, 裸腿, 0)）：S 0.79/F 0.43/2Y 0.12/sub 0.76（非核心臂最高、接近臂1 的 0.91）/TO 19.75%/margin 5.98bp/CW 0.172248@2014-09-11。vs 裸腿 −0.50 ⇒ 稀释；`vector_neut` 平台接受（仿真正常完成，无语法/算子异常）且对 sub 有改善（0.76），但 CW 仍挂、S 仍远离闸。**向量正交化不是免死牌**（本波唯一 vector_neut 实测）。
8. **臂8 ZYal7Mkn**（纯 fnd72 时序门控：trade_when(δ252(ts_mean(裸腿,66))>0, 裸腿, 0)）：S 0.78/F 0.40/2Y **−0.47**/sub 0.36（<0.37，差 0.01）/TO 14.92%（本波最低）/DD 14.13%/margin 5.20bp/**CW PASS**。**关键控制变量对照**：门控条件完全不含 insiders，只是核心腿自身的时序动量 → S 1.29→0.78（−0.51）、2Y 0.79→−0.47 ⇒ **trade_when 门控形态在本腿上自身即负杠杆**。因此臂4/5/6/7 的稀释不能全部归因于 insiders 数据质量；同时臂8 CW PASS 反证 CW 挂与 insiders 腿直接相关（纯 fnd72 臂 4/4 CW PASS）。
9. **臂9 N1Pj73k8**（insiders 主体 + fnd72 q δ66>0 门控，subindustry）：S 0.30/F 0.10/2Y 0.85（IS_LADDER）/sub 0.21/TO 18.82%/DD 23.49%/margin 2.11bp（本波最低）/CW 0.271844@2014-02-18。vs 臂10 纯 insiders 0.83 → **−0.53** ⇒ 门控同样稀释 insiders 腿；主体换成 insiders 后 fnd72 门控无增益。CW 数据层指纹同上；margin 2.11bp 远低于 5bp 线，与 S/F 同向弱。
10. **臂10 mLazj129**（纯 insiders，与 `FIELD_insiders1_20261115.md` §6 **M2 逐字同构**：group_rank(δ66(ts_backfill(vec_sum(insd1_holdings),250)), subindustry)）：S 0.83/F 0.33/2Y 0.78（LOW_2Y）/sub 0.35（<0.39）/TO 21.96%/DD 7.08%/margin 3.20bp/CW 0.144689@2014-01-29。**与 FIELD 档先验存在口径差**：FIELD 档引 DEU 既有证据「A 单腿 Δ66 S 1.72」（`Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:31`，BA6 I1 用 vec_avg + 132 回填）；本波用 vec_sum + 250 回填得到 0.83，差 0.89。口径差（vec_avg vs vec_sum、132 vs 250、窗口/settings 未核）**未做单变量拆解** ⇒ **不得声称 M2 机制已死，也不得用 0.83 否定 1.72 先验**；记「口径敏感、需单变量对照」。CW 0.1447 与门控臂同量级，说明 CW 挂的主因是 insiders 腿宽度而非 trade_when 形态（臂8 无 insiders → CW PASS）。

## §3 符号指纹 / 稀释铁律 / 跨区核对

- **符号指纹：未测（无翻符号对照臂）**。本波 10 臂全为正向构造，**没有** multiply(-1, …) 反号臂；也无 decay 对照（全波 decay=0 固定）。⇒ 无法按「衰减对称=机制在/符号错；单向=事件型」做判定。**本波不对方向做裁定**；近闸候选若推进，先补一条反号对照（`FIELD_insiders1_20261115.md` §5 明确要求「每个含增持/减持语义的模板必须同波带反号对照臂」，本波未执行，登记为设计缺口）。不得以本波为「符号指纹已过」的依据。
- **稀释铁律**：命中 2 类、不触发 2 处。命中：①**乘法**——臂6 `multiply(裸腿, greater(...))` S 0.60 < 单腿 1.29（−0.69）⇒ 乘法低于对应单腿=稀释；②**门控**——臂4/5/7/9 S 0.30–0.79 全低于对应单腿（1.29 或 0.83）。不触发：臂1/2 三窗乘法 1.42/1.45 > 单腿 1.29（连续 rank 三腿，全维增益）。⇒ 判据收敛：**第二腿是连续信息腿（rank 乘积）→ 增益；第二腿是二值/门控/向量正交 → 稀释**（本波 7 条复合臂一致，无例外）。
- **跨区不外推**：零 TWN/KOR 引用；对照全部 DEU 域内（KPJmRpGN / RREALzx0 / mLaALJX2 / 本波波内）。`insiders1` 的 DEU 既有证据（1.72 / 2.36）只作口径对照，不作跨区或跨波增益承诺；fnd45/fnd86/fnd89/fnd90 邻接集先验未因本波改写。
- **配置维**：全波固定 FAST / decay=0 / TOP500 / D1 / trunc 0.08，**未扫**中性化、decay、宇宙、delay、trunc。族内既有证据：decay 对动量族单调负杠杆（0/2/4，`NEARGATE_BREAK_GRID_FND72_20261115.md` §B4）⇒ 本波用 decay=0 是已知最优档，不派「加 decay 提 S」臂。

## §4 塔位判读（点塔相关性）

平台 payload `pyramids` 原文（逐臂回读）：

| 臂 | pyramids.list | effective |
|---|---|---|
| 1/2/3/8 | `DEU/D1/FUNDAMENTAL` ×1.8 | 1 |
| 4/5/6/7/9 | `DEU/D1/INSIDERS` ×1.6 + `DEU/D1/FUNDAMENTAL` ×1.8 | 2 |
| 10 | `DEU/D1/INSIDERS` ×1.6 | 1 |

- **目标塔 FUNDAMENTAL 出现 9/10 臂归属**（臂1/2/3/4/5/6/7/8/9）；**INSIDERS 塔 6/10 臂**（臂4/5/6/7/9/10）。点塔入口成立。
- **但点位≠点亮**：10/10 臂 RA fail≥2，无一条过全闸；本波对塔位的实际贡献 = 0（无可提交件）。
- **配腿代价**：5 条 effective=2 双塔件 S 0.30–0.79，全低于单 FUNDAMENTAL 塔件 1.29–1.45 ⇒ 当前构造下 insiders 配腿是负担不是增益；双塔件若未来达标会同时占两个塔位（配额逻辑需单独核算），本波不产生塔位申请。
- 臂10 只挂 INSIDERS（无 FUNDAMENTAL）：它的弱读数只说明 insiders 腿在该构造下弱，不构成 fundamental 塔证据。

## §5 数据层判读（data_excluded 与信号死分开）

- **本波零 data_excluded 臂**：LC/SC 151–220 全宽，无任何臂 LC/SC≤5；无宽度塌缩形态。fundamental72 的 `coverage=0` 是本集×本区平台元数据退化（`FIELD_fundamental72_20261115.md` §2 三条对照 + 真实持仓已证伪「0=没数据」），**不作可用性判据**。
- **CW 挂闸 6 臂（4/5/6/7/9/10）全部含 insiders 腿**；纯 fnd72 臂 4/4 CW PASS。⇒ **CW 挂 = insiders1 数据层指纹**（`insd1_holdings` 250 日宽度 193/500=38.6%，2024 年前申报稀疏；`FIELD_insiders1_20261115.md` §4.2），非信号死；不 data_excluded、不改符号重试。
- **无判死动作**：本波 10 臂，结构互异模板 <10（见 §6），按「探针 <10 条不产生判死」+ 六维未达，**fundamental72 与 insiders1 均不判死**；insiders1 只记「本波不产出可推进结构」。

## §6 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义 10 臂，互异机制 ~3：三窗动量乘（1/2）、单腿动量（3）、trade_when/insiders 门控族（4/5/7/8/9：同一「门控/二值腿」机制的 5 种写法，非不同经济机制）、insiders 单腿（10） | **✗ 未达** |
| D2 字段族自测 | 只碰 2 个 fnd72 字段（oper_inc、tot_asset）+ 1 个 insd1 字段；fnd72 共 1031 字段（`FIELD_fundamental72_20261115.md` §1） | **✗ 远未达** |
| D3 矩全家 | 一阶差（δ240/δ176/δ66）✓、比值（oper_inc÷tot_asset）✓；**缺**二阶波动、信噪比、纯水平腿 | **✗ 未达** |
| D4 分组轴 ≥2 | sector（臂1）、subindustry（臂9/10） | ✓ |
| D5 非线性 ≥1 | ts_rank、group_rank、trade_when、multiply(greater) | ✓ |
| D6 配置 ≥2 | 本波固定 FAST/decay0/TOP500/D1 **一套** | **✗ 本波自身未达**（跨槽累计有 SUBINDUSTRY 三波，但那不是本波读数） |

⇒ 缺 D1/D2/D3/D6：**只能 provisional，不得判死、不得封集、不得作为邻接数据集/字段族先验**（AGENTS §7.6）。

## §7 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `Xgal7eEb` | **1.45** | S≥1.2；距 S 硬闸 1.58 差 **0.13**≤0.4；F 1.01 已过 fitness_min；剩余缺口=2Y 0.96（差 0.62）、sub 0.55（平台 limit 0.69，差 0.14） |
| 2 | `LLKX7rxL` | **1.42** | S≥1.2；距 S 硬闸差 **0.16**≤0.4；F 0.94 距 1.0 差 **0.06**≤0.4；2Y 1.96 ✓、sub 0.91 ✓、CW PASS、margin 8.69bp——**本波距全闸最近（仅 2 项 FAIL）** |

- 排序外登记（如实）：`omazqreb`（S 1.29≥1.2；F 0.84 距 0.16；sub 0.48 距平台 limit 0.61 差 0.13；2Y 0.79 距 0.79）也满足多轴触发，按 S 降序第 3 出局。机械上「距任一硬闸 ≤0.4」的还有全部 CW 挂闸臂（CW 差值 0.044–0.213）、臂8（LOW_SUB 差 0.01）等，均按 S 降序出局（§1 已列全量读数）。
- **prod/self 未测（本波全 null，相关性查询按分工未做）**：候选 Xgal7eEb / LLKX7rxL 均为 fnd72 核心件（非 insiders 搭档件）——按「prod 雷在核心不在搭档」，先测这两条的 prod 再决定是否扫参。族内先验 `mLaALJX2` prod 0.5444（<0.70）是利好但不同表达式，**不构成保证**。
- **年度分年未取（本波未跑 get_alpha_yearly_stats）** ⇒ 2018/2019/2020 时间集中度**未验证**。族级既有读数（`S0_TOWER_SCAN_20261115.md:130`：mLaALJX2 2018 0.80 / 2019 0.80 / 2020 −0.35，2021–2023 3.03/2.60/1.96）提示该族存在时间集中风险。**推进前必须补分年**：若 2018/2019/2020 仍全 <1.0 而总 S 靠 2021–2023 撑起，按「时间集中度风险」登记，**不得按可提交推进**。

## §8 datasetStatus 裁决 + 波 verdict

**datasetStatus = provisional（判弱入档延续；本波无终态转换）**。依据：

1. **本波 0 达标**：10/10 臂 RA fail≥2（DB 回读），最高 S 1.45（臂2）< 族峰 1.50（mLaALJX2）< S 闸 1.58；核心三臂 1.29–1.45 落在既有近闸带，**无突破**（对照 atom 槽 11-15 FAST 轮曾以 1.47 > 1.42 判 active；本波 1.45 未破 1.47/1.50，不构成升级 active 的读数）。
2. **与 standing state 一致**：`CATEGORY_MATRIX_FUNDAMENTAL_20261115.md` §5 定 fnd72 = **provisional（判弱入档）**并明确「供下一槽引用」；本波即下一槽，无终态转换（不 dead_proposed、不 data_excluded、不 capped）。
3. **无数据层排除**：LC/SC 全宽（151–220）、纯 fnd72 臂 4/4 CW PASS、无宽度塌缩 → 不满足 data_excluded。
4. **不得判死**：D1/D2/D3/D6 未达（§6），AGENTS §7.6 六维闸禁止终判死；本波也不作为邻接集先验。
5. **insiders1 同样不判死**：本波只有 1 条纯 insiders 结构 + 5 条门控变体（结构互异 <10，探针条款），且 CW 挂属数据层；记「本波不产出可推进 insiders 结构」，不记死。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 近闸 ⇒ PARTIAL；`n_pass=0 / n_near=2`）。禁止自造枚举。

## §9 newLever 登记

**空串（不入册）**。理由：本波所有结构指纹（sector group_rank 承载 2Y；trade_when 自身负杠杆；insiders 二值腿乘法稀释）均为**波内对照**，无跨波单变量复现；臂1 vs KPJmRpGN 的 S +0.04 / 2Y +0.38 与 tail/hump 缺失、decay/窗口配置差**捆绑未拆**，不能作为杠杆归因。跨波实证+归因对照两条都不满足。

## §10 证据通道与盲区

- **读数来源**：ask 转录的 harvest 回传（每臂 metrics/checks/pyramids/settings）+ 本槽只读核验 `logs/_tmp_rtfund_w1_readback.py`（sqlite `mode=ro`，零写入）：10/10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与 `payload.checks.fail` 10/10 一致；payload `settings`（FAST/decay0/TOP500/D1/2014-01-01→2023-12-31）与 ask 一致；`pyramids.effective` 与 ask 一致（1/2 分类 5/5）。
- **IS_LADDER 三处一致（多数据集件 5/5）**：`alphas.is_ladder_sharpe` = `alphas.two_year_sharpe` = `checks.fail[IS_LADDER_SHARPE].value` —— 臂4 0.35/0.35/0.35、臂5 −0.01/−0.01/−0.01、臂6 1.41/1.41/1.41、臂7 0.12/0.12/0.12、臂9 0.85/0.85/0.85；`year=2` 取自 checks 原文。单集件 5/5 走 LOW_2Y 且 two_year 与 checks value 一致（1.96/0.96/0.79/−0.47/0.78）。
- **盲区（如实登记）**：
  1. 年度分年未取 → 时间集中度未验证（§7）；
  2. prod/self 相关性未测（10 臂全 null，按分工归相关性槽）；
  3. `operator_audit` 对多语句表达式解析失败，返回 `error: Unexpected character at position 79`——工具解析限制，**如实记为 error，不作无解证据**；补充正证：单语句/展开等价形态 7 条 safe=true、violations=[]，ghost_operators 不含本波 14 个算子，create_multi_simulation 内置静态闸未拦截；
  4. `preflight_expressions` 的 `unknown_fields=[h,i,m,p,q,v]` 为多语句左值变量（赋值目标），非字段；3 个真实字段不在 unknown；`any_changed=false`、fixed 与原文逐字相同 ⇒ 10 臂按原表达式派发；
  5. create_multi_simulation 不暴露 startDate/endDate（`world-quant-brain-mcp/tools_sim.py:672-690`），平台回显 2014-01-01→2023-12-31 与 settings.json 的 2013-01-01 不同——原样记录平台值，不推断；
  6. 本波 10 臂、结构互异 <10，按探针条款不产生判死；六维 D1/D2/D3/D6 未达。
- **跨槽纪律**：本波（regular_tower / `rt-fundamental-w1`）与 atom_orthogonal 槽的 fnd72 `w1/w2/w3` 是不同波标签，读数不合并、本档不覆写其档案；只引用 `CATEGORY_MATRIX_FUNDAMENTAL_20261115.md` §5 的 standing state。

## §11 终态

- **波**：PARTIAL；0 达标 / 2 近闸；best S **1.45**（Xgal7eEb）/ best 2Y **1.96**（LLKX7rxL）。
- **数据集**：fundamental72 = **provisional**（判弱入档延续，无终态转换）；insiders1 = 本波无可推进结构、**不判死**（探针 + D1 未达）。
- **提交链**：无（0 达标，无候选进入提交语境）。
- **下一波输入**：① 臂1 型（三窗乘法 + sector）距全闸最近（S 差 0.16、F 差 0.06），先测 prod/分年；如需补 S，族内唯一未叠的已入册杠杆是 tail 0.12 + hump 0.003（族峰 S 1.50），须单变量拆分后再归因；② sector group_rank 保留（2Y/sub 载体）；③ insiders 腿先修宽度（vec_avg/132 口径或更长回填）并补反号对照，且复合前须过 CW 0.1；④ 本波未扫 decay/中性化/宇宙，若开第二配置轴需独立成波。
