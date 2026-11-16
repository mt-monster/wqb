# WAVE rt-fundamental-w5 — fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 主集：`fundamental72`（目标塔 FUNDAMENTAL）；配对集 insiders1 本波**未出臂**（10/10 单集件，全部只引用 fnd72 字段）
- 配置（平台回显，DB payload 逐臂一致）：DEU/TOP500/D1、neutralization=FAST、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR；平台回显 `startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:16-17`（2013-01-01 起）不同；`create_multi_simulation` 无 startDate/endDate 参数（`world-quant-brain-mcp/tools_sim.py:672-690`）。本档原样记录平台值。
- 派发/收割（收割说明转录）：create_multi_simulation 单波 10 臂 → multisim `17zizO38W4Bfc3b1e5Rklf8Y`；batch_status 2 次至 `child_count=10/terminal=10/errors=0`（约 2.5 分钟）；harvest_multisim_alphas 首试成功（未走 404 兜底）；upsert_backtest_rows(DEU, rt-fundamental-w5, fundamental72, 10 行) → n=10。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / sub≥1.0（本地 review 线；平台 LOW_SUB limit 动态，本波无 LOW_SUB fail）/ TO 0.01–0.70 / margin≥0.0005（5bp，`tracking/DEU/config/thresholds.json:7`）/ prod&self corr≤0.70；CW 用**平台 limit 0.1**（`thresholds.json:20` 的 0.5 只是本地 review 线）。
- 2Y 闸种：本波 **10/10 臂为单数据集件**（expressions `atom_flag=atom`、`atom_n_datasets=1`；DB `alphas.is_ladder_sharpe` 全 null），全部走 `LOW_2Y_SHARPE`（limit 1.58）；**无多数据集件**，IS_LADDER 三处一致条款本波不适用（非漏检）。
- 符号指纹：本波仍**无翻符号对照臂**（0 条 multiply(-1,…)；settings decay 固定 0；arm3 的 `reverse(...)` 是反向排序，不是整式反号）。⇒ 本波不对方向做裁定。

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | alphaId | 结构（简） | S | F | 2Y（LOW_2Y） | sub | TO | DD | margin | LC/SC | 塔（effective） | RA fail（DB `ra_failed_checks`） |
|---|---|---|---|---|---:|---|---:|---:|---|---:|---|---|
| 1 | oma9mwpE | EBIT 三年窗核 + `tail(0.06/0.94)` | 1.37 | 0.87 | 2.14 | 1.08 | 17.39% | 7.15% | 0.000812 / 8.12bp | 220/162 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 2 | 3q0nqYbN | EBIT 三年窗核 + `tail(0.07/0.93)` | **1.53** | **1.02** | **2.39（本波最高）** | 1.10 | 17.43% | 6.72% | 0.000898 / 8.98bp | 218/164 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE 1.53<1.58]；其余 pass |
| 3 | Jj85j0El | H9 留存稳定性：`reverse(ts_std_dev(ts_backfill(nm÷gm,10),120))`，sector | 0.34 | 0.12 | −0.13 | 0.19 | 13.10% | 11.24% | 0.000252 / 2.52bp | 157/225 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；CLUSTER −0.03 warning |
| 4 | pwa1wJrV | H3 慢趋势：`group_rank(ts_mean(p,504)−ts_mean(p,1008), sector)` | 0.76 | 0.40 | 0.41 | 0.73 | 12.20% | 9.38% | 0.000580 / 5.80bp | 187/196 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；CLUSTER 0.40 warning |
| 5 | 78YK8qbZ | H4 资产周转增量：`group_rank(rank(δ240(sales÷assets)), sector)` | 1.21 | 0.74 | 1.33 | 0.82 | 14.77% | 5.97% | 0.000756 / 7.56bp | 185/198 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；⚠ `checks.fail=[]`；CLUSTER 0.85 warning |
| 6 | 9qlAqP12 | H4 营业利润率增量：`group_rank(rank(δ240(oper_inc÷sales)), sector)` | 1.28 | 0.81 | 1.15 | 0.88 | 15.12% | 8.16% | 0.000797 / 7.97bp | 185/197 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；⚠ `checks.fail=[]`；CLUSTER 0.93 warning |
| 7 | WjlWjw6Q | H5 正确毛利率定义增量：`group_rank(rank(δ240((sales−cogs)÷sales)), sector)` | 1.02 | 0.60 | 0.85 | 0.95 | 14.24% | 6.02% | 0.000700 / 7.00bp | 159/223 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；⚠ `checks.fail=[]`；CLUSTER 0.75 warning |
| 8 | blaWl25q | H2 恒等式价差：`group_rank(rank(δ240(oper_inc)÷assets − δ240(p)), sector)` | 0.58 | 0.26 | 0.22 | 0.62 | 13.82% | 13.12% | 0.000396 / 3.96bp | 183/200 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；CLUSTER 0.26 warning |
| 9 | RRekRZnz | 分母口径 B（当期总资产）：`group_rank(rank(δ240(oper_inc)÷assets), sector)` | **1.54** | **1.07** | 1.39 | 1.12 | 15.34% | 6.50% | 0.000974 / 9.74bp | 184/198 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE 1.54<1.58, **LOW_2Y 1.39<1.58**]；⚠ `checks.fail=[]`；F/sub/CW/CLUSTER pass |
| 10 | E5Qr50X9 | 分母口径 C（504 日均资产）：`group_rank(rank(δ240(oper_inc÷ts_mean(assets,504))), sector)` | 1.45 | 0.98 | 1.43 | 0.96 | 15.22% | 8.65% | 0.000918 / 9.18bp | 184/198 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；⚠ `checks.fail=[]` |

- DB 只读核验（sqlite `mode=ro`，零写入）：10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count`/名单一致；payload `settings` 逐臂 FAST/decay0/TOP500/D1/2014-01-01→2023-12-31；`pyramids` 10/10 = `DEU/D1/FUNDAMENTAL`×1.8（effective=1）。
- ⚠ **checks 表示不一致（平台原文）**：臂5/6/7/9/10 的 `checks.fail=[]`，但 `ra.failed_ra_count=3/3/3/2/3`，对应 LOW_SHARPE/LOW_FITNESS/LOW_2Y（及 CLUSTER_TEST）落在 `checks.warning` 带 value/limit。本档以 `ra_failed_checks` 判 fail（AGENTS §8.7：RA 资格门失败含 WARNING/ERROR）；只看 `checks.fail=[]` 会把臂5/6/7/9/10 误判成通过。
- **查重/预检（收割说明转录）**：preflight `unknown_fields=[gm,m,nm,p,t]` 全为多语句左值变量，非字段；6 个真实字段（含新启用的 `fnd72_s_pit_or_is_q_net_income`）已验存、`any_changed=false`；`operator_audit` 多语句解析 error（Unexpected character at position 72，工具限制），展开单语句 10 条 `safe=true`、violations=[]，ghost 列表不含本波算子；查重全同命中 0，10 臂全派发。

## §2 逐臂归因条目

1. **臂1 oma9mwpE（EBIT 三年窗核 + tail 0.06）**：S 1.37/F 0.87/2Y 2.14/sub 1.08/TO 17.39%/DD 7.15%/margin 8.12bp/LC 220-162；RA fail 2。**vs w4 臂9（EBIT + tail 0.08，1.62/1.12/2.54/1.16）**：S **−0.25**/F −0.25/2Y −0.40/sub −0.08/DD +1.00pp。⇒ 带宽收到 0.06 时 S/F **单侧塌陷**，与 w4 的 oper_inc 0.05 塌陷同型；0.06 不可行。
2. **臂2 3q0nqYbN（EBIT + tail 0.07）**：S **1.53**/F **1.02**/**2Y 2.39（本波最高）**/sub 1.10/TO 17.43%/DD 6.72%/margin 8.98bp/LC 218-164；RA fail 1=LOW_SHARPE（差 0.05）。**vs 0.06**：S +0.16/F +0.15/2Y +0.25/sub +0.02；**vs 0.08（w4 臂9）**：S −0.09/F −0.10/2Y −0.15/sub −0.06。⇒ 0.07 位于 0.06→0.08 的上升段，但 0.08 仍全面更高；0.07 是"2Y 仍高（2.39）且 S 1.53"的备选取舍点，不是峰。
3. **臂3 Jj85j0El（H9 留存稳定性：净利率÷毛利率的 120 日波动，反向）**：S 0.34/F 0.12/2Y −0.13/sub 0.19/TO 13.10%/DD 11.24%/margin 2.52bp/LC 157-225；RA fail 3、CLUSTER −0.03 warning。⇒ **留存稳定性机制在本配置无信号**（S 0.34、2Y 负）；"稳定性/低波动"假设不成立；TO 13.10% 低但收益不支持。
4. **臂4 pwa1wJrV（H3 慢趋势：504 日均值 − 1008 日均值）**：S 0.76/F 0.40/2Y 0.41/sub 0.73/TO 12.20%（本波最低）/DD 9.38%/margin 5.80bp/LC 187-196；RA fail 3、CLUSTER 0.40 warning。⇒ 慢趋势腿把换手压到 12.2%，但 S/F/2Y 全弱（S 0.76、2Y 0.41）；**慢趋势不是本族 S 载体**（与 w1/w2 的短窗 delta 动量族方向相反）。
5. **臂5 78YK8qbZ（H4 资产周转增量：δ240(sales/assets) 单腿）**：S 1.21/F 0.74/2Y 1.33/sub 0.82/TO 14.77%/DD 5.97%/margin 7.56bp/LC 185-198；RA fail 3（checks.fail 空）、CLUSTER 0.85 warning。⇒ 单腿 1.21 高于 w1 单腿 A 1.29？不，低于 A 1.29（S −0.08/F −0.10/2Y +0.54/sub +0.34）——周转腿 2Y 更好但 S/F 更低；作为独立机制**不足以替代营收/资产主腿**（**注意：文献"周转独立"在本配置只复制出 2Y 面、没复制出 S 面**）。
6. **臂6 9qlAqP12（H4 营业利润率增量：δ240(oper_inc/sales) 单腿）**：S 1.28/F 0.81/2Y 1.15/sub 0.88/TO 15.12%/DD 8.16%/margin 7.97bp/LC 185-197；RA fail 3（checks.fail 空）、CLUSTER 0.93 warning。⇒ S 1.28 与 A 1.29 持平、F −0.03、**2Y +0.36（1.15 vs 0.79）**、sub +0.40；**利润率腿在 2Y/sub 面有独立信息，但 S 面不超主腿**——与文献"margin 无预测力"部分相反（本配置下 2Y 面并非无信息），但不足以上升为 S 载体。
7. **臂7 WjlWjw6Q（H5 正确毛利率定义增量：δ240((sales−cogs)/sales) 单腿）**：S 1.02/F 0.60/2Y 0.85/sub 0.95/TO 14.24%/DD 6.02%/margin 7.00bp/LC 159-223；RA fail 3（checks.fail 空）、CLUSTER 0.75 warning。**读数更正**：ask 括注称本臂 F 0.60/2Y 0.85「均不及 w2 的 sales/COGS 加成率 1.00？」——按 w2 档 DB 读数，w2 臂4 `gJaP0Vkl` 是 **1.00/0.58/2Y 0.55/sub 0.84 的 p×g 两腿复合**；本臂 **1.02/0.60/2Y 0.85/sub 0.95 四项均高于它**，并非「均不及」。但两者结构不同（w2 是 p×g 复合、本臂是 g 单腿），**不构成单变量对照**；本臂作为单腿仍远低于 1.56 主核，H5 不掉队也不出彩。
8. **臂8 blaWl25q（H2 恒等式价差：δ240(oper_inc)/assets − δ240(p)）**：S 0.58/F 0.26/2Y 0.22/sub 0.62/TO 13.82%/DD 13.12%/margin 3.96bp/LC 183-200；RA fail 3、CLUSTER 0.26 warning。⇒ 恒等式分解价差**无信号**（S 0.58、2Y 0.22、DD 13.12% 最高）；"价差=错误定价"假设在本配置不成立。
9. **臂9 RRekRZnz（分母口径 B：当期总资产，`δ240(oper_inc)÷assets`）**：S **1.54**/F **1.07**/2Y 1.39/sub **1.12**/TO 15.34%/DD 6.50%/margin **9.74bp**/LC 184-198；RA fail 2（LOW_SHARPE 1.54 差 0.04、LOW_2Y 1.39 差 0.19），F/sub/CW/CLUSTER pass（checks.fail 空）。**vs A（w1 单腿 `rank(δ240(p))`，1.29/0.84/0.79/0.48）**：S **+0.25**/F **+0.23**/2Y **+0.60**/sub **+0.64**/TO −0.46pp/margin +1.24bp——A→B 是全维大幅改善，但**含 sector 分组（A 无分组）+ 分母时点两处差异**，不是单变量（§3.3）。⇒ B 是本波最强单腿，但 2Y 1.39 仍距 1.58 差 0.19，且 S 差 0.04；**不能因 S/F/sub 改善就忽略 2Y 挂闸**。
10. **臂10 E5Qr50X9（分母口径 C：504 日均资产，`δ240(oper_inc÷ts_mean(assets,504))`）**：S 1.45/F 0.98/2Y 1.43/sub 0.96/TO 15.22%/DD 8.65%/margin 9.18bp/LC 184-198；RA fail 3（LOW_SHARPE 1.45 差 0.13、LOW_FITNESS 0.98 差 0.02、LOW_2Y 1.43 差 0.15），checks.fail 空。**vs B**：S −0.09/F −0.09/2Y +0.04/sub −0.16/DD +2.15pp ⇒ 504 日均值分母只换到 +0.04 的 2Y，代价是 S/F/sub 与回撤；**C 不如 B**。**vs A**：S +0.16/F +0.14/2Y +0.64/sub +0.48（同样含分组/分母差异，不可单变量归因）。

## §3 带宽 / 杠杆结论（本波重点）

### 3.1 EBIT 核带宽缺口闭合：0.06 / 0.07 / 0.08 / 0.10 / 0.12（同核同字段、sector、单变量）

| 带宽 | 臂（波） | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 0.06 | w5 臂1 oma9mwpE | 1.37 | 0.87 | 2.14 | 1.08 | 17.39% | 7.15% | 8.12bp |
| 0.07 | w5 臂2 3q0nqYbN | 1.53 | 1.02 | 2.39 | 1.10 | 17.43% | 6.72% | 8.98bp |
| **0.08** | w4 臂9 kqamAeRg | **1.62** | **1.12** | **2.54** | **1.16** | 17.40% | 6.15% | 9.48bp |
| 0.10 | w4 臂8 WjlX5KkN | 1.56 | 1.05 | 2.30 | 1.04 | 17.30% | 7.14% | 9.14bp |
| 0.12 | w4 臂10 2r5ZYPE6 | 1.51 | 1.00 | 2.17 | 1.00 | 17.13% | 6.94% | 8.85bp |

**结论（带宽缺口闭合）**：0.06→0.07→0.08 **上升**（S 1.37→1.53→1.62、F 0.87→1.02→1.12、2Y 2.14→2.39→2.54、sub 1.08→1.10→1.16），0.08→0.10→0.12 **下降**（S 1.62→1.56→1.51、F 1.12→1.05→1.00、2Y 2.54→2.30→2.17、sub 1.16→1.04→1.00）。⇒ **0.08 是已测区间的内点峰（两侧均已补测回落）**；w4 档「0.06/0.07 未测、0.08 是已测最窄点而非已证峰」的 caveat 本波**关闭**。同时 0.06 的塌陷（S 1.37）与 w4 的 oper_inc 0.05 塌陷同型：**带宽过窄会裁掉有效信息**，不是越窄越好。
- 0.07 是"2Y 仍高（2.39）+ S 1.53 + F 1.02"的备选取舍点，但全面低于 0.08；若后续需要更低回撤/不同换手，0.07 可作备选，不改变 0.08 的峰位。
- **本波无新 PASS**：0.08 峰仍由 w4 `kqamAeRg`（RA 全闸）占据；0.06/0.07 两臂均未过闸。

### 3.2 机制探针（H9 / H3 / H4 / H5 / H2）：全部弱于现有载体

| 机制 | 臂 | 表达式要点 | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| H9 留存稳定性 | 3 Jj85j0El | `reverse(ts_std_dev(ts_backfill(nm÷gm,10),120))`, sector | 0.34 | 0.12 | −0.13 | 0.19 | 13.10% | 11.24% | 2.52bp |
| H3 慢趋势 | 4 pwa1wJrV | `ts_mean(p,504)−ts_mean(p,1008)`, sector | 0.76 | 0.40 | 0.41 | 0.73 | 12.20% | 9.38% | 5.80bp |
| H4 资产周转增量 | 5 78YK8qbZ | `rank(δ240(sales÷assets))`, sector | 1.21 | 0.74 | 1.33 | 0.82 | 14.77% | 5.97% | 7.56bp |
| H4 营业利润率增量 | 6 9qlAqP12 | `rank(δ240(oper_inc÷sales))`, sector | 1.28 | 0.81 | 1.15 | 0.88 | 15.12% | 8.16% | 7.97bp |
| H5 毛利率增量 | 7 WjlWjw6Q | `rank(δ240((sales−cogs)÷sales))`, sector | 1.02 | 0.60 | 0.85 | 0.95 | 14.24% | 6.02% | 7.00bp |
| H2 恒等式价差 | 8 blaWl25q | `rank(δ240(oper_inc)÷assets − δ240(p))`, sector | 0.58 | 0.26 | 0.22 | 0.62 | 13.82% | 13.12% | 3.96bp |
| 对照：A 单腿（w1） | omazqreb | `rank(δ240(p))`（无分组） | 1.29 | 0.84 | 0.79 | 0.48 | 15.80% | 6.43% | 8.50bp |
| 对照：w4 PASS | kqamAeRg | EBIT 三年窗三腿 + tail 0.08 | 1.62 | 1.12 | 2.54 | 1.16 | 17.40% | 6.15% | 9.48bp |

**结论（机制）**：6 条机制探针 S 0.34–1.28，全部低于 A 单腿 1.29 或仅与 A 持平（H4 margin 1.28 基本持平），更远低于 w4 PASS 1.62。分面看：
- **H9 留存稳定性**：S 0.34/2Y −0.13，**彻底无信号**（稳定性/低波动假设不成立）。
- **H3 慢趋势**：TO 12.20% 最低、DD 9.38%，但 S 0.76/2Y 0.41——**慢趋势只降换手不产收益**。
- **H4 资产周转**：2Y 1.33 > A 的 0.79（+0.54），但 S 1.21 < A 1.29（−0.08）⇒ **周转腿只在时间维有增量，S 面不超主腿**；文献"周转独立"在本配置只复制出 2Y 面。
- **H4 营业利润率**：2Y 1.15 > A 0.79（+0.36）、sub 0.88 > 0.48（+0.40），S 1.28 与 A 持平 ⇒ **margin 腿在 2Y/sub 面并非无信息**（与文献"margin 无预测力"部分相反），但 S 不超主腿，不能升为 S 载体。
- **H5 毛利率增量**：S 1.02/F 0.60/2Y 0.85，单腿弱；读数更正见 §2.7（ask 括注的"均不及 w2"不成立，且结构不同不可比）。
- **H2 恒等式价差**：S 0.58/2Y 0.22/DD 13.12%，**无信号**。
⇒ 6 条机制均为**单腿单臂探针**，按「探针 <10 条不产生判死」，**不据此判任何数据集/字段族死**；只记「本波不产出可推进结构」。

### 3.3 分母口径 A/B/C：改善真实但含混淆，不能作单变量杠杆

| 口径 | 臂（波） | 表达式 | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| A 比率 delta | w1 omazqreb | `rank(δ240(oper_inc÷assets))`（无分组） | 1.29 | 0.84 | 0.79 | 0.48 | 15.80% | 6.43% | 8.50bp |
| B 当期总资产 | w5 臂9 RRekRZnz | `group_rank(rank(δ240(oper_inc)÷assets), sector)` | **1.54** | **1.07** | 1.39 | **1.12** | 15.34% | 6.50% | **9.74bp** |
| C 504 日均资产 | w5 臂10 E5Qr50X9 | `group_rank(rank(δ240(oper_inc÷ts_mean(assets,504))), sector)` | 1.45 | 0.98 | 1.43 | 0.96 | 15.22% | 8.65% | 9.18bp |

- **B vs A**：S +0.25 / F +0.23 / 2Y +0.60 / sub +0.64 / margin +1.24bp——但 A 无 `group_rank(sector)`、B 有，且分母时点不同（δ(oper_inc)/assets vs δ(oper_inc/assets)）⇒ **至少两处差异，不能把 +0.25 全记到"当期总资产分母"头上**（w1/w3 已证 sector 分组本身可贡献 +0.03 S/+0.07 F/+1.00 2Y/+0.36 sub 量级）。
- **C vs B**：S −0.09 / F −0.09 / 2Y +0.04 / sub −0.16 / DD +2.15pp——504 日均值分母只换到 +0.04 的 2Y，代价是 S/F/sub 与回撤 ⇒ **C 不如 B**；且 C 与 B 同时差"分母均值化"与"delta 时点"两处，非单变量。
- **B/C 的共同短板是 2Y**：B 1.39、C 1.43，均 <1.58；而三窗口 tail 核（w4 PASS）2Y 2.54。⇒ **分母口径轴提高 S/F/sub 但不解决 2Y 闸**；如果要用 B，必须另配 2Y 载体（sector/三窗 tail 等），不能单独推进。
- **结论**：A/B/C 是**设计对照**而非干净杠杆；B 的 S/F/sub 读数值得保留为"单腿强候选"，但**不入册 newLever**（§10）。

### 3.4 稀释铁律 / 复合形态

- 本波**零 bucket、零多腿乘法复合**（10 臂均为单腿或单腿+tail/分组；arm8 是 subtract 恒等式，不是乘法）。⇒ **稀释铁律（乘法/bucket 低于对应单腿）本波不适用**。
- 机制探针的弱读数属**单腿机制弱**，不是"复合稀释"；A/B/C 的差异属"分母时点/分组"对照，不是乘法。分开登记，避免把"单腿弱"误写成"稀释"。
- 唯一的"复合"是 w4 PASS 的三窗乘法核（1.62）与 w5 单腿 B（1.54）/C（1.45）的**跨波对照**：三窗核 > 单腿 B/C ⇒ 三窗乘法在 S/2Y 面仍是更强载体（但两者字段/壳不同，非严格单变量）。

## §4 符号指纹 / 跨区核对

- **符号指纹：未测**。无整式反号臂；`reverse` 只是排序反向（arm3），不是反号；settings decay 固定 0。⇒ 不能按「衰减对称=机制在/符号错；单向=事件型」判定；本波不对方向做裁定。近闸件（RRekRZnz / 3q0nqYbN）推进前应补反号对照（w1–w4 连续登记该缺口，本波仍未补）。
- **跨区不外推**：零 TWN/KOR 引用；对照全部 DEU 域内（w1 A 单腿、w4 PASS、本波波内）。fnd45/fnd86/fnd89/fnd90 邻接集先验未改写；insiders1 本波未测、状态不变（沿用 w1/w2：不判死、无可推进结构）。

## §5 塔位判读（点塔相关性）

平台 payload `pyramids` 原文（逐臂回读）：10/10 臂 = `DEU/D1/FUNDAMENTAL` ×1.8、effective=1。

- **目标塔 FUNDAMENTAL 出现 10/10 臂归属**（本波无 insiders 臂、无双塔件、无多数据集件）。
- **点位≠点亮**：10/10 臂 RA fail≥1，本波无新全闸件；**全族唯一 RA 全闸 PASS 仍是 w4 `kqamAeRg`**（S 1.62/F 1.12/2Y 2.54/sub 1.16，ra_failed_count=0），本波实际点亮 0。
- 单塔件（effective=1）占满全波 ⇒ 不涉及双塔配位/配额问题。

## §6 数据层判读（data_excluded 与信号死分开）

- **本波零 data_excluded 臂**：LC/SC 157–225 全宽，无 LC/SC≤5；无宽度塌缩。
- **CW 10/10 全 pass**：本波无 insiders 腿，CW 挂闸（数据层指纹）未出现；与 w1/w2 的 insiders 臂形成对照，进一步支持「CW 挂由 insiders 持仓宽度驱动」的判读。
- **无判死**：本波 10 臂但每条机制仅 1 臂（H9/H3/H4a/H4b/H5/H2 各 1，带宽 2，分母 2），结构互异 <10；按探针条款**不判死**。fundamental72 不 data_excluded、不判死；机制弱读数是**信号层**结论，不是数据层排除。
- fundamental72 `coverage=0` 仍是平台元数据退化（`FIELD_fundamental72_20261115.md` §2），不作可用性判据。

## §7 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义 10 臂，互异机制 ~8：EBIT 带宽 2（0.06/0.07）+ H9/H3/H4 周转/H4 利润率/H5 毛利率/H2 价差 6 + 分母 B/C 2——但带宽两臂是同一核的参数变体，机制臂各 1 臂 | **✗ 未达**（<10） |
| D2 字段族自测 | 本波碰 6 个 fnd72 字段（ebit、tot_asset、net_income、sales_rev_turn、cogs_to_fe_and_pp_and_g、oper_inc）；fnd72 共 1031 字段 | **✗ 远未达** |
| D3 矩全家 | 一阶差（δ240）✓、二阶波动（H9 ts_std_dev）✓、比值（多组）✓；**缺**纯水平腿、信噪比 | **✗ 未达**（本波补了二阶波动，仍缺水平/SNR） |
| D4 分组轴 ≥2 | 本波全部 sector（单一轴） | **✗ 本波自身未达**（历史 w3/w4 有 industry/subindustry，非本波读数） |
| D5 非线性 ≥1 | group_rank、rank、reverse、tail、ts_std_dev、subtract | ✓ |
| D6 配置 ≥2 | 本波固定 FAST/decay0/TOP500/D1 **一套** | **✗ 本波自身未达**（跨槽累计有 SUBINDUSTRY 三波，非本波读数） |

⇒ 缺 D1/D2/D3/D4/D6：**不得判死、不得封集、不得作为邻接集先验**（AGENTS §7.6）。PASS/带宽峰都是候选层/参数层事件，不是数据集终态。

## §8 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

> 本波**无 PASS 臂**；w4 `kqamAeRg` 仍是全族唯一 RA 全闸件（prod/self/分年仍未验，不占本波 near 位）。以下按 S 降序取前 2。

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `RRekRZnz` | **1.54** | S≥1.2；距 S 闸 0.04≤0.4、距 2Y 闸 0.19≤0.4；FAIL=LOW_SHARPE+LOW_2Y；F 1.07/sub 1.12/CW pass/CLUSTER pass/margin 9.74bp/TO 15.34% |
| 2 | `3q0nqYbN` | **1.53** | S≥1.2；距 S 闸 0.05≤0.4；唯一 FAIL=LOW_SHARPE；F 1.02/2Y 2.39/sub 1.10/CW pass/CLUSTER pass/margin 8.98bp/TO 17.43% |

- 排序外登记（如实）：`E5Qr50X9` S 1.45 且三闸均近（S 差 0.13、F 差 0.02、2Y 差 0.15），但按 S 降序第 3 出局；`9qlAqP12` 1.28、`78YK8qbZ` 1.21 亦满足 S≥1.2，但 F 0.81/0.74 与 2Y 1.15/1.33 缺口更大，按 S 降序出局（全量读数见 §1）。
- **prod/self 未测（本波全 null，相关性查询按分工未做）**：两条 near 均为 fnd72 核心件（无搭档/insiders 腿）——按「prod 雷在核心不在搭档」，先测这两条 prod 再决定扫参。w4 PASS 件 `kqamAeRg` 的 prod/self/data-diversity 仍 pending，**优先测 PASS 件**；near 件不得越过 PASS 件先推进。
- **年度分年未取** ⇒ 2018/2019/2020 时间集中度**未验证**。族级既有读数（`S0_TOWER_SCAN_20261115.md:130`：mLaALJX2 2018 0.80/2019 0.80/2020 −0.35，2021–2023 3.03/2.60/1.96）提示该族存在时间集中风险。**PASS 件与 near 件推进前必须补分年**；若 2018/2019/2020 仍全 <1.0 而总 S 靠 2021–2023 撑起，按「时间集中度风险」登记，**不得按可提交推进**。
- **mode_b_qualification**（`thresholds.json:23-27`）：`RRekRZnz` S 1.54/F 1.07、`3q0nqYbN` S 1.53/F 1.02、`E5Qr50X9` 1.45/0.98 均过 S≥1.25/F≥0.8 资格线。

## §9 datasetStatus 裁决 + 波 verdict

**datasetStatus = active（维持 w2–w4 的 active，无终态转换）**。依据：

1. **带宽峰闭合**：EBIT 核 0.06/0.07/0.08/0.10/0.12 呈"上升→0.08 峰→下降"，0.08 内点峰确认（S 1.62/F 1.12/2Y 2.54/sub 1.16，w4 PASS）；w5 两臂 0.06（1.37）/0.07（1.53）补全两侧回落证据。
2. **本波无新 PASS**：0 达标（10/10 臂 RA fail≥1），但 near 2 条（RRekRZnz 1.54、3q0nqYbN 1.53）；全族唯一 RA 全闸仍是 w4 `kqamAeRg`（prod/self/分年未验，不能算"可提交"）。
3. **机制探针全弱**：H9 0.34 / H3 0.76 / H4 1.21/1.28 / H5 1.02 / H2 0.58，均低于 A 1.29 或仅持平，不产出可推进结构；分母 B/C 1.54/1.45 有 S/F/sub 改善但 2Y 1.39/1.43 挂闸。
4. **无数据层排除**：LC/SC 157–225 全宽、CW 10/10 pass、无宽度塌缩 ⇒ 不满足 data_excluded。
5. **不得判死/封集**：D1/D2/D3/D4/D6 未达（§7），AGENTS §7.6 六维闸禁止终判死；PASS/带宽峰都是候选层/参数层事件，不是数据集终态。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 近闸 ⇒ PARTIAL；`n_pass=0 / n_near=2`）。禁止自造枚举。

## §10 newLever 登记

**空串（本波不入册新杠杆）**。理由：
1. **带宽 0.08 峰确认**是对 w4 已入册杠杆（tail 带宽峰随字段核移动）的**验证/补测**，不是新杠杆；w5 补的是 0.06/0.07 两侧回落证据，结论方向与 w4 一致，无新增机制。
2. **A/B/C 分母口径**的 A→B、B→C 对照均含**两处以上差异**（sector 分组的有无 / 分母时点 / 分母均值化 / delta 时点），**不是单变量归因**，不能入册为"当期总资产分母"或"504 日均资产分母"杠杆。
3. **机制探针 H9/H3/H4/H5/H2** 全部为单腿单臂且弱于现有载体（0.34–1.28），是**证伪/弱化**结论，不是可入册杠杆。
⇒ 待后续波次做单变量拆解（B vs A 拆 sector 分组、C vs B 拆分母均值化）后，再考虑入册。

## §11 证据通道与盲区

- **读数来源**：ask 转录的臂序读数 + 本槽 DB 只读核验（sqlite `mode=ro`，零写入）：10/10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count`/名单一致；payload `settings` 逐臂 FAST/decay0/TOP500/D1/2014-01-01→2023-12-31；`pyramids` 10/10 FUNDAMENTAL×1.8、effective=1；`alphas.is_ladder_sharpe` 全 null、prod/self 全 null。
- **IS_LADDER**：本波 10/10 单数据集件（`atom_n_datasets=1`），全部走 LOW_2Y_SHARPE；DB `two_year_sharpe` 与 checks 值 10/10 一致 ⇒ 三处一致条款不适用（非漏检）。
- **checks 表示不一致**：臂5/6/7/9/10 `checks.fail=[]` 但 `ra.failed_ra_count=3/3/3/2/3` 且 ra 名单含 LOW_SHARPE/LOW_FITNESS/LOW_2Y（及 CLUSTER_TEST，warning 桶带 value/limit）——本档以 ra 名单判 fail（AGENTS §8.7）；`checks.fail` 原文照录。
- **盲区（如实登记，不猜不补）**：
  1. 年度分年未取 → 2018/2019/2020 时间集中度未验证（§8）；PASS 件与 near 件提交前必补。
  2. prod/self 相关性未测（10 臂全 null；w4 PASS 件平台 SELF/PROD/DATA_DIVERSITY 仍 pending）。
  3. 符号指纹未测（无翻符号对照臂）。
  4. `operator_audit` 对原 10 条多语句表达式解析失败 `error: Unexpected character at position 72`（工具限制）——如实记 error、不作无解证据；展开单语句 10 条 `safe=true`、violations=[]、ghost 列表不含本波算子（reverse/ts_std_dev/subtract 等）。
  5. `preflight` 的 `unknown_fields=[gm,m,nm,p,t]` 为多语句左值变量，非字段；6 个真实字段（含 net_income）已验存、`any_changed=false`、fixed 与原文逐字相同。
  6. create_multi_simulation 不暴露 startDate/endDate（`tools_sim.py:672-690`），平台回显 2014-01-01→2023-12-31 与 settings.json 2013-01-01 不同——原样记录平台值。
  7. 本波结构互异 <10，按探针条款不产生判死；六维 D1/D2/D3/D4/D6 未达。

## §12 终态

- **波**：PARTIAL；0 达标 / 2 近闸；best S **1.54**（RRekRZnz）/ best 2Y **2.39**（3q0nqYbN）。
- **数据集**：fundamental72 = **active**（维持，无终态转换；带宽 0.08 峰闭合、本波无新 PASS，D1/D2/D3/D4/D6 未达 → 不判死、不封集）；insiders1 本波未测、不判死（沿用 w1/w2）。
- **提交链**：**未推进**（本波 0 达标；全族唯一 PASS 件仍是 w4 `kqamAeRg`，其 prod/self/data-diversity pending、年度分年未取、无用户确认）。下一步：① 优先测 `kqamAeRg` 的 prod/self/data-diversity 并补 2018–2020 分年；② near 件 `RRekRZnz`/`3q0nqYbN` 先测 prod；③ 若要继续带宽/分母轴，先做单变量拆解（B vs A 拆 sector 分组、C vs B 拆分母均值化），不要直接叠加；④ 机制探针 H9/H3/H4/H5/H2 本配置下不推进（均弱于 A 1.29 或仅持平），不判死但暂停加注；⑤ 保持 sector 分组、三窗 tail 核、不要动 settings decay（族内 0/2/4 负杠杆）。
