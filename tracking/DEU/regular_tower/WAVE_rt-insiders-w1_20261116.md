# WAVE rt-insiders-w1 — `insiders1` 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集：`insiders1`（目标塔 **INSIDERS**）；配对集：`institutions6`（塔 INSTITUTIONS）
- 配置（平台 `get_alpha_details` 逐臂回显，10/10 一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、maxPosition=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR、simulationMode=FULL；`startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:5-16`（decay=4、nanHandling=OFF、2013-01-01 起）不同 ⇒ 本波是**探针口径配置（decay0/nanON）**，不是区域生产档。按 DEU skill 提醒「设置是强度闸：nanHandling / decay / 中性化换档等于换信号，跨档结果不可比」，本波读数**只能在 decay0/nanON 档内比较**。
- 派发/收割（收割说明转录，本档未重跑派发）：`preflight_expressions(DEU/TOP500/D1, dataset_id=insiders1)` valid=true / unknown_fields=[] / any_changed=false（10/10）；`operator_audit` safe=true / violations=[]；精确式查重全仓 0 历史命中（仅命中本波输入件 `logs/_tmp_rt-insiders-w1_arms.json`、`logs/_tmp_rt_insiders_w1_arms.txt`）；`create_multi_simulation` 单波 10 臂 → multisim `2MK3Hr1eg57S8Mv11Wfx5MXF`；`batch_status` 终态 10/10 all_terminal（5 COMPLETE + 5 WARNING，errors=5）；`harvest_multisim_alphas` 首试成功（未走 404 兜底），total=10/complete=10/error_count=0；`upsert_backtest_rows(DEU, rt-insiders-w1, insiders1, 10)` → n=10。
- 判读基准（ask 给定，本档另附平台实读限值，见 §1.1）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0 / 0.01≤TO≤0.70 / margin≥0.0005 / CW≤0.5 / self 与 prod 各<0.70。
- 闸种：**5 条 atom 单集件走 `LOW_2Y_SHARPE`（limit 1.58）；5 条 combined 双集件走 `IS_LADDER_SHARPE`（year=2，limit 1.58）**。`two_year_sharpe` 字段与 RA 2Y 载体逐臂一致（10/10，值见 §1）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

本表指标经 `mcp__wq-brain-http__batch_get_alpha_metrics`（10/10 success）与 `get_alpha_details` 逐臂复核，与 ask 转录**逐值一致**。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔（pyramids/list） | RA fail（平台 `ra.ra_failed_checks`） |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|
| 1 | `2r5a6KzP` | holdings Δ66 ÷ 其 252 日波动（z 化），`group_rank(,sector)`，**无回填** | −0.11 | −0.02 | −1.00 | −0.09 | 107.58% | 90.60% | −0.48bp | **1/5** | DEU/D1/INSIDERS×1.6（eff 1） | 6：LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB, LOW_2Y |
| 2 | `ZYa2zo38` | holdings Δ66 ÷ holdings 水平，裸 `rank` | −0.01 | −0.00 | 0.07 | **11.18**（退化，见 §2.2） | 21.94% | 20.76% | −0.10bp | **0/0** | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y |
| 3 | `kqa1GK2L` | `if_else(inst_share_rank<0.5, 臂1核, 0.5)` | 0.35 | 0.14 | 0.94 | −0.06 | 2.39% | 12.67% | 17.41bp | 131/115 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB, **IS_LADDER**；⚠ warning UNITS |
| 4 | `A1xgz3MQ` | 臂1核 + `bucket(inst_share_rank, 0/0.5/1)` 分组 | −0.07 | −0.01 | −1.11 | 0.05 | 107.60% | 89.14% | −0.32bp | 0/4 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 5：LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, **IS_LADDER**；⚠ warning UNITS |
| 5 | `wponGeg5` | valueeur 单笔集中度 max/sum，`ts_sum(,66)`，`group_rank(,sector)` | 0.78 | 0.47 | 0.88 | 0.16 | 5.38% | 13.87% | 17.04bp | 127/142 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB, LOW_2Y |
| 6 | `RRe2zrLj` | 臂7核 + `tail(winsorize(rank), std=2, 0.2/0.8→0.5)` | 0.60 | 0.35 | 0.32 | 0.38 | 7.02% | 14.46% | 11.83bp | 71/129 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y |
| 7 | `oma3GYeb` | valueeur 单笔集中度 max/sum，`ts_sum(,66)`，裸 `rank` | **0.81** | **0.50** | 0.83 | 0.19 | 4.73% | 13.90% | **20.39bp** | 129/140 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB, LOW_2Y |
| 8 | `vRAeGm0Q` | `if_else(inst_share_rank<0.5, 臂5核, 0.5)` | 0.74 | 0.43 | **1.17** | 0.08 | 5.54% | 13.95% | 15.54bp | 134/126 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB, **IS_LADDER**；⚠ warning UNITS |
| 9 | `N1PgzOk8` | `if_else(inst_share_rank>0.5, 臂5核, 0.5)`（臂8 的反向分支） | 0.53 | 0.27 | 0.44 | 0.08 | 5.87% | 11.25% | 10.83bp | 128/143 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB, **IS_LADDER**；⚠ warning UNITS |
| 10 | `3q0aPAYe` | `if_else(inst_share_rank<0.5, 臂2核, 0.5)` | 0.35 | 0.14 | 0.96 | −0.06 | 2.44% | 12.73% | 17.29bp | 131/115 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB, **IS_LADDER**；⚠ warning UNITS |

- **平台 `status`**：10/10 = `UNSUBMITTED`（alpha 提交态）；ask 所称 `WARNING` 是**仿真态**（臂3/4/8/9/10，errors=5，原因 UNITS）。
- **本波极值**：best S **0.81**（臂7 `oma3GYeb`）/ best 2Y **1.17**（臂8 `vRAeGm0Q`）/ best F 0.50（臂7）/ best margin 20.39bp（臂7）。
- **0 达标**：10/10 臂 `failed_ra_count` ≥3（3/4/4/5/4/3/4/4/4/4），**无一条 RA 全闸**。

### 1.1 平台实读限值（本轮补齐 ask 的「平台 LOW_SHARPE limit 未读到」缺口）

`get_alpha_details` 的 `checks.fail` 逐臂携带 `value/limit`，实读：

| 闸 | 平台实读 limit | 与 ask 基准的关系 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10 臂） | 与内部严线一致 |
| LOW_FITNESS | **1.0** | 一致 |
| HIGH_TURNOVER | **0.70** | 一致 |
| CONCENTRATED_WEIGHT | **0.10**（臂1/2/4 实读，value 均 0.5） | ⚠ **比 ask 的 CW≤0.5 严 5 倍**；0.5 是本地 review 线（`tracking/DEU/config/thresholds.json:20`） |
| LOW_2Y_SHARPE / IS_LADDER_SHARPE | **1.58**（year=2） | 一致 |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂不同**：臂1 −0.05 / 臂3 与臂10 0.17 / 臂9 0.25 / 臂8 0.35 / 臂5 0.37 / 臂7 0.38；臂2/4/6 判 PASS（limit 未回显） | ⚠ **sub≥1.0 是本地 review 线，不是平台闸限**（`thresholds.json:21`）；平台动态限只有 0.17–0.38，故臂6（sub 0.38）在平台侧 PASS |

⇒ 两点结论：① ask 的「平台 LOW_SHARPE limit 本轮未读到」**已由本轮实读补齐 = 1.58**；② **本波 verdict 不依赖 sub 口径**——即使把 sub 判据换成平台动态限（更宽）或本地 1.0 线（更严），10/10 臂仍全部挂 LOW_SHARPE + LOW_FITNESS（S≤0.81 vs 1.58、F≤0.50 vs 1.0），**0 达标这个结论对 sub 口径不敏感**。

## §2 逐臂归因条目

### 2.1 holdings-Δ 族（臂1/2/3/4/10）——本波全部弱于 insiders1 已知单集上限

**共同结构缺陷（本波最重要的一条）**：这 5 臂的 `insd1_holdings` 腿**都没有 `ts_backfill`**，直接 `ts_delta(vec_sum(insd1_holdings), 66)`。而本集 FIELD 档 §4.6 已实证「**时间平滑是本集的入场条件，不是优化项**」：裸 `vec_*` 换手 1.62–1.79（硬线 0.7），加 250 日回填后降到 0.011–0.034（`FIELD_insiders1_20261116.md:195-206`）。本波读数与该判断完全吻合——**凡保留 ts_delta 无回填的臂，换手/回撤立刻爆炸**（臂1/4 TO 107.6%、DD 89–91%），凡被掩码压住的臂（臂3/10）换手降到 2.4%，但那是掩码的功劳（§3.2）。

1. **臂1 `2r5a6KzP`（holdings Δ66 z 化 + sector group_rank，无回填）**：S −0.11 / F −0.02 / 2Y −1.00 / sub −0.09 / TO **107.58%** / DD **90.60%** / margin −0.48bp / **LC-SC 1/5**；RA 6 挂（含 HIGH_TURNOVER、CW value 0.5 vs limit 0.1）。⇒ 截面塌到 6 只票，换手 1.08（远超 0.7），DD 90%：这是「稀疏事件流被当逐日变化读」的典型形态，与 FIELD 档 §4.6 预测的裸 `vec_*` 高换手同型，也与 EUR 侧整集判死的那套**裸 vec 短窗几何**同型（`FIELD_insiders1_20261116.md:259-266`）。**不是数据没有，而是几何读错**。
2. **臂2 `ZYa2zo38`（Δ66 ÷ holdings 水平，裸 rank）**：S −0.01 / F −0.00 / 2Y 0.07 / sub **11.18** / TO 21.94% / DD 20.76% / LC-SC **0/0**。⚠ **读数自相矛盾**：LC/SC 报 0/0，但 `pnl=-106,769`、`turnover=0.2194`、`bookSize=20,000,000`、`investability_ratio=-84` —— 说明**账面并非真空仓，是长/空计数与其它指标不自洽**。故 sub 11.18 **不可当真实优势**（也不可反读成"sub 崩塌"）：该字段在退化截面下不携带信息。按 ask 要求原值照录，但归因上只记「构造级失败」，不记数据层结论。
3. **臂3 `kqa1GK2L`（掩码 <0.5 + 臂1核）**：S 0.35 / F 0.14 / 2Y 0.94 / sub −0.06 / TO 2.39% / DD 12.67% / margin 17.41bp / LC-SC 131/115。**vs 臂1（同核，无掩码）**：S **+0.46**、F +0.16、2Y +1.94、TO −105.19pp、DD −77.93pp、LC/SC 1/5→131/115。⇒ **掩码把塌缩的票池拉宽、把换手压掉两个数量级**，但它把 S 只抬到 0.35（距闸 1.23）。掩码修的是**宽度/换手**，不是强度——与 DEU skill 的既有铁律「门控只修 prod/robust，不造强度」同向（`Claude/skills/wq-brain-ra-deu/references/insiders.md:52`）。
4. **臂4 `A1xgz3MQ`（臂1核 + bucket(inst_share) 分组）**：S −0.07 / F −0.01 / 2Y −1.11 / sub 0.05 / TO **107.60%** / DD 89.14% / LC-SC **0/4**；RA 5 挂（含 HIGH_TURNOVER、CW）。**vs 臂1（同核，换分组轴 sector→bucket）**：S +0.04、F +0.01、sub +0.14、但 2Y −0.11、**TO 逐位不变（107.58%→107.60%）**。⇒ **换分组轴不治换手**：bucket 分组对该核是零作用，与 §3.4 的 sector 分组零增益同型。
5. **臂10 `3q0aPAYe`（掩码 <0.5 + 臂2核）**：S 0.35 / F 0.14 / 2Y 0.96 / sub −0.06 / TO 2.44% / DD 12.73% / margin 17.29bp / LC-SC 131/115。**vs 臂2（同核，无掩码）**：S +0.36、2Y +0.89、TO −19.50pp、LC/SC 0/0→131/115。⚠ **与臂3（另一个核 + 同掩码）读数几乎逐位相同**——见 §3.2，这是本波最强的结构诊断。

**族级锚点（必须先看再读本族读数）**：`insiders1` 的**单数据集 S 上限 ≈1.30** 已由三波独立路径收敛确认（`tracking/DEU/atom_orthogonal/BE176_INSIDERS1_CEILING_130_20261112.md:23,28-30`：BE172 同字段多窗 1.22 / BE174 跨形态叠加 1.30 / BE176 未试形态 1.19；`:50` 判「ATOM 在 insiders 上确定不可行，三波 30 臂验证」）。本波 5 条 atom 臂 **0.35–0.81**，全部**低于**该上限 ⇒ 它们既没有破顶、也没有证伪上限，只是**更差的结构**。⇒ 本波不能用来支持或反驳「insiders1 单集可过 1.58」这一命题。

### 2.2 valueeur-集中度族（臂5/6/7）——唯一有正 S 的核，但天花板更低

6. **臂5 `wponGeg5`（集中度 max/sum，`ts_sum(,66)`，`group_rank(,sector)`）**：S 0.78 / F 0.47 / 2Y 0.88 / sub 0.16 / TO 5.38% / DD 13.87% / margin 17.04bp / LC-SC 127/142。**对照臂7（同核，裸 rank）**：S **−0.03**、F −0.03、2Y **+0.05**、sub −0.03、TO +0.65pp、margin −3.35bp ⇒ **sector 分组对该核是零增益**（§3.4）。
7. **臂6 `RRe2zrLj`（臂7核 + winsorize(std=2) + tail(0.2/0.8→0.5)）**：S 0.60 / F 0.35 / 2Y 0.32 / sub 0.38 / TO 7.02% / DD 14.46% / margin 11.83bp / LC-SC 71/129；RA 只 3 挂（本波最少）。**对照臂7（裸 rank 单腿）**：S **−0.21**、F −0.15、2Y **−0.51**、margin −8.56bp、DD +0.56pp、TO +2.29pp，唯 sub **+0.19**。⇒ **符合稀释铁律：单调壳层叠加（winsorize+tail）低于对应单腿 = 稀释**（§3.3）。注意 LC/SC 由 129/140 变 71/129：tail 把 20% 尾部压成常数，票池单侧收窄。
8. **臂7 `oma3GYeb`（集中度 max/sum，`ts_sum(,66)`，裸 rank）**：S **0.81（本波最高）** / F **0.50** / 2Y 0.83 / sub 0.19 / TO 4.73%（本波最低之一）/ DD 13.90% / margin **20.39bp（本波最高）** / LC-SC 129/140；RA 4 挂。⇒ 本波唯一「四项指标同向为正且换手/回撤健康」的结构，但 S 距闸 0.77、2Y 距闸 0.75、sub 0.19 vs 本地 1.0 线 —— **离闸太远，不构成近闸**（§8）。其核与 FIELD 档 M5 同族，该档给的先验是「姊妹集 HHI 集中度 S 1.74–2.20，但本集原生版本截面只有 6–8 只/日，宽度风险最高」（`FIELD_insiders1_20261116.md:242`）——本波实测截面 127–140 只（远宽于 6–8），**说明本波这条腿的实际宽度比 FIELD 档担心的好，但强度只到 0.81**，即「宽度不是瓶颈、强度才是」。

### 2.3 配对腿（institutions6）族（臂3/4/8/9/10）——全部 UNITS 挂，未取得可判读读数

9. **5/5 配对臂共享同一平台警告**：`UNITS: Incompatible unit for input of "add" at index 1, expected "Unit[CSShare:1]", found "Unit[]"` —— 根因是条件式里 `aggregate_share_count_institutions / (aggregate_share_count_all_owners + 1)` 对 CSShare 单位字段加了无量纲 1。平台照常出指标（故读数照录），但按纪律 **5 臂一律记 `rebuild_needed`**：在两处单位不兼容的条件下，掩码的截面排序、换手与权重稳定性都可能是单位错误的产物。
10. **臂8 `vRAeGm0Q`（掩码 <0.5 + 臂5核）**：S 0.74 / F 0.43 / 2Y **1.17（本波最高）** / sub 0.08 / TO 5.54% / DD 13.95% / margin 15.54bp / LC-SC 134/126。**对照臂5（同核，无掩码）**：S **−0.04**、F −0.04、sub **−0.08**、margin −1.5bp、TO +0.16pp、DD +0.08pp，**唯一收益是 2Y +0.29（0.88→1.17）**。⇒ 按稀释铁律，**掩码对 S/F/sub 是净稀释**；即便以 2Y 为唯一目标，1.17 仍距闸 0.41（刚出 0.4 近闸带，故不计近闸）。
11. **臂9 `N1PgzOk8`（掩码 >0.5 + 臂5核，臂8 的反向分支）**：S 0.53 / F 0.27 / 2Y 0.44 / sub 0.08 / TO 5.87% / DD 11.25% / margin 10.83bp / LC-SC 128/143。**vs 臂8**：S −0.21、2Y −0.73、DD −2.70pp、LC/SC 128/143 vs 134/126。⇒ **两向不对称差 0.21 > 0.1**，且 TO/DD/LC-SC 全不同 ⇒ **不是「方向层无净信息」的退化指纹**；方向层结论是「**低机构持股（<0.5）分支更强**」，可用的强侧是臂8 一侧（§4）。
12. **★ v2 目标未达成且不可判读**：ask 的 ★v2 更正指出「第一设计目标是选对第二腿把 sub 留在 ≥1.0」，并给出 [INSIDERS,MODEL] 配对 sub 1.51–1.54（38/40 全闸）、只有 insd1+shrt3 配对全灭的先验。本波选的第二腿是 **INSTITUTIONS**（不是 MODEL），5 臂 sub = 0.05 / 0.08 / −0.06 / −0.06 / −0.06，**全部远离 1.0**。但**这 5 条全部 rebuild_needed**，所以正确表述是「**INSTITUTIONS 作第二腿在本波没有留下可判读的 sub 证据**」，不能写成「INSTITUTIONS 配对已证死 sub」。

### 2.4 族内存量对照（防止把"本波弱"读成"insiders 不行"）

平台实读（`batch_get_alpha_metrics`，6/6 success）DEU 已有 **6 条 `failed_ra_count=0` 的 INSIDERS 族存量件**：

| alpha | S | F | 2Y | sub | TO | DD | margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Vk6eodeb` | 1.63 | 1.41 | 1.66 | 1.49 | 12.43% | 5.58% | 15.0bp |
| `akLG3VgO` | 1.82 | 1.70 | 2.12 | 1.43 | 12.17% | 6.11% | 18.0bp |
| `RRVPLpG0` | 1.88 | 1.66 | 1.78 | 1.00 | 12.96% | 5.83% | 15.7bp |
| `le81ZVo5` | 1.91 | 1.69 | 1.85 | 0.96 | 11.22% | 5.78% | 17.5bp |
| `O0rgvJgR` | 1.76 | 1.65 | 1.64 | 1.36 | 12.15% | 9.25% | 18.2bp |
| `qMWVeeME` | 1.64 | 1.42 | 1.67 | 1.51 | 12.42% | 5.47% | 15.1bp |

- **但这不是 insiders1 的先例**：`Vk6eodeb` 平台实读 `code` = `add(add(add(add(rank(ts_sum(ts_backfill(significant_value_1,66),252)), rank(ts_mean(predicted_surprise_f12m_ebitda_4,5))), …))`，`pyramids` = **DEU/D1/INSIDERS×1.6 + DEU/D1/MODEL×1.8**（effective 2），即**五腿 equal-weight `add` + MODEL 预估字段 + `significant_value_1`**，既不是 insiders1 的 `insd1_*` 几何，也不是单集件。其余 5 条只取了指标（`failed_ra_count=0`），**未逐条取 pyramids**（如实登记为盲区）。
- 用途仅两条：① 证明「insiders 族在 DEU 能过 RA」不是本波能否定的（**本波 0.35–0.81 vs 存量 1.63–1.91，差 0.82–1.10**）；② 该存量形态用的是 `add` 多腿，**正是 DEU skill 现在明令禁止的形态**（`Claude/skills/wq-brain-ra-deu/references/insiders.md:44`：禁止两条独立信号腿相加）⇒ **不可当可复用配方**，也不构成对本波结论的反证。

## §3 符号指纹 / 稀释铁律 / 宽度塌缩

### 3.1 符号指纹：**严格口径不可测（0 条翻符号臂）**

- 本波 10 条表达式**没有任何整式取反**（`logs/_tmp_rt-insiders-w1_arms.json` 全文无前置负号 / `multiply(-1,…)`）。按 FIELD 档 §5 的硬约束「**方向：无方向字段 ⇒ 任何"增持/减持"语义的模板必须同波带反号对照臂**」（`FIELD_insiders1_20261116.md:207-215`；本集数值 20 条探针 `shortCount` 全 0 ⇒ 数值本身不带买卖方向），本波**违反了该入场纪律**。
- 因此 ask 的符号指纹判据（「S(−expr)≈−S(expr) 且差<0.03 且 TO/DD/longCount 逐位相同 ⇒ 方向层无净信息、机制不在」）**本波无法执行**——如实记「未测」，**不得**据此判死、也不得反读成「机制在」。
- 可做的近似只有**互补分支对**（不是反号）：臂8（`<0.5`）vs 臂9（`>0.5`）——S 0.74 vs 0.53（差 **0.21 > 0.1**）、2Y 1.17 vs 0.44、TO 5.54% vs 5.87%、DD 13.95% vs 11.25%、LC/SC 134/126 vs 128/143：**逐项不同，不是退化指纹**。结论强度仅到「**掩码条件的方向有意义（低机构持股一侧更强）**」，**不涉及 insd1 增持方向的正负**。
- 跨区符号禁照搬：本档**未引用** USA 文献符号，也未把 DEU 的 insiders 符号外推到 TWN/KOR；`risk72 残差为动量 / CEO 任期为正` 两处反转先例在本波无对应结构，不适用。

### 3.2 掩码主导 / 核贡献不可分离（本波最强的结构诊断）

臂3（core A = holdings Δ66 z 化）与臂10（core A′ = Δ66÷holdings 水平）在**同一掩码**下读数几乎逐位相同：

| | S | F | 2Y | sub | TO | DD | margin | LC/SC |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 臂3 core A | 0.35 | 0.14 | 0.94 | −0.06 | 2.39% | 12.67% | 17.41bp | 131/115 |
| 臂10 core A′ | 0.35 | 0.14 | 0.96 | −0.06 | 2.44% | 12.73% | 17.29bp | 131/115 |

两种结构不同的核（z 化 vs 水平比）在掩码下**给不出可区分的结果**（S/F/sub 数值相同、TO 差 0.05pp、DD 差 0.06pp、LC/SC 完全相同）。可能解释有二：① 掩码（`if_else(…, 0.5)`，一半截面取常数）主导了组合，核只提供扰动；② holdings-Δ 族两个变体本身在无回填几何下退化为同一信号。**本波没有「掩码单独成臂」的对照**（如 `if_else(cond, 1, 0.5)`）⇒ **两种解释无法分离**。这是设计缺口，不是结论——下一波必须补掩码单独对照，才能把「掩码的收益」与「核的收益」拆开，否则任何"配对增益/稀释"都无法定量。

旁证（同向）：臂8（core B + 掩码）S 0.74 ≠ 臂3/10 的 0.35，说明**核在 core B 上仍然可分**；退化的只是 core A/A′ 这一对。故本条准确表述是「**core A/A′ 在无回填几何下不可区分**」，而不是「核一概无效」。

### 3.3 稀释铁律（乘法/bucket/壳层低于对应单腿 = 稀释）

本波**零乘法复合**（无 `multiply`），但有壳层与分组两类复合，逐条对照：

| 复合形态 | 复合读数（S/F/2Y/sub） | 对应单腿 | 差 | 判定 |
|---|---|---|---|---|
| 臂6 `tail(winsorize(rank(core B)))` | 0.60 / 0.35 / 0.32 / 0.38 | 臂7 裸 `rank(core B)`：0.81 / 0.50 / 0.83 / 0.19 | S **−0.21** / F −0.15 / 2Y **−0.51** / sub +0.19 | **稀释**（唯一改善是 sub 与 DD） |
| 臂8 `if_else(cond<0.5, core B, 0.5)` | 0.74 / 0.43 / 1.17 / 0.08 | 臂5 `group_rank(core B, sector)`：0.78 / 0.47 / 0.88 / 0.16 | S **−0.04** / F −0.04 / 2Y **+0.29** / sub **−0.08** | **对 S/F/sub 净稀释**；2Y 是唯一正项 |
| 臂5 `group_rank(core B, sector)` | 0.78 / 0.47 / 0.88 / 0.16 | 臂7 裸 `rank(core B)`：0.81 / 0.50 / 0.83 / 0.19 | S −0.03 / F −0.03 / 2Y +0.05 / sub −0.03 | **零增益**（非稀释，也无增益） |
| 臂4 `group_rank(core A, bucket(inst))` | −0.07 / −0.01 / −1.11 / 0.05 | 臂1 `group_rank(core A, sector)`：−0.11 / −0.02 / −1.00 / −0.09 | S +0.04 / 2Y −0.11 / **TO 逐位不变 107.6%** | **零作用**（换分组轴不治换手） |
| 臂3/10 `if_else(cond, core A/A′, 0.5)` | 0.35 / 0.14 / 0.95 / −0.06 | 臂1 −0.11 / 臂2 −0.01（各自无掩码） | S +0.46 / +0.36，TO −105pp / −19.5pp | **掩码修宽度与换手，不是"增强"**（见 §3.2 与 `insiders.md:52` 门控不造强度） |

⇒ 本波**没有一条复合形态高于其对应单腿**（唯一高于单腿的是被掩码修好的两个塌缩臂，属"修复"不属"增强"）。这与「乘积/bucket 复合需高于单腿才值得留」的既有纪律一致：**本波的复合全部不划算**。

### 3.4 宽度塌缩 + CONCENTRATED_WEIGHT 单独登记（数据层 ≠ 信号死 ≠ 表达层）

| 臂 | LC/SC | CW（value vs limit） | 归因 |
|---|---|---|---|
| 臂1 `2r5a6KzP` | **1/5** | 0.5 vs **0.1**（2023-02-13）挂 | **表达层**：无回填的 Δ66 z 化把截面压到 6 只（同波其它臂 127–143 只） |
| 臂2 `ZYa2zo38` | **0/0** | 0.5 vs **0.1**（2023-12-13）挂 | **构造级失败**；且与 pnl≠0 / TO 0.2194 自相矛盾（§2.1-2） |
| 臂4 `A1xgz3MQ` | **0/4** | 0.5 vs **0.1**（2023-02-13）挂 | **表达层**：同臂1 核 + bucket 分组，仍塌缩 |
| 臂3/5/6/7/8/9/10 | 71–143 | pass | 无塌缩 |

- **本波 0 条 data_excluded**：同数据集同配置下 7 条臂能持有 71–143 只票、pnl 为正（臂5/6/7/8/9 各 +3.2M~+4.98M）、TO 在 2.4–7.0% 正常区间 ⇒ **数据存在且可交易**，不存在「字段无数据」的证据。
- 三臂的宽度塌缩**必须归到表达层**（几何把稀疏事件流当逐日量），**不得**登记成 `data_excluded`，也**不得**登记成信号死。

## §4 配对腿（institutions6）判读

- **构造**：二次腿以三种形态入场——① 条件 `if_else`（臂3/8/10 用 `<0.5`，臂9 用 `>0.5`）；② 分组 `bucket(rank(…), 0/0.5/1)`（臂4）。符合 DEU skill「第二个数据集只以条件 / 分组 / 残差入场」的合法空间（`Claude/skills/wq-brain-ra-deu/references/insiders.md:44`）。
- **效果（唯一可读的两条同核对照）**：掩码对 core B 的净效应 = **S −0.04 / F −0.04 / sub −0.08 / margin −1.5bp / 2Y +0.29**（臂5→臂8）。⇒ **在 decay0/nanON 档、institutions 作第二腿，掩码不是强度杠杆；它只换来 2Y 的 +0.29，且 2Y 仍差 0.41**。
- **方向**：`<0.5`（低机构持股）侧 0.74 强于 `>0.5` 侧 0.53（差 0.21）⇒ 若要留一条，取 `<0.5` 侧。
- **不可下结论的部分**：5/5 臂 `UNITS` 警告（`+1` 无量纲加在 CSshare 字段上）⇒ 掩码的截面排序本身可能被单位错误扭曲。正确处置是 rebuild 为同单位守卫（例如把 `+1` 换成 `+ ts_backfill(aggregate_share_count_all_owners, 252)` 的稳健分母，或先 `rank` 再比较），**重建后重跑再判**。
- **与 ★v2 先验的对照（不外推、只记录）**：★v2 说 [INSIDERS,MODEL] 配对 sub 1.51–1.54；本轮平台实读的两条 [INSIDERS,MODEL] 存量件 `Vk6eodeb` sub **1.49**、`qMWVeeME` sub **1.51** —— **与该先验同量级，可视为对"MODEL 作第二腿能保住 sub"的独立佐证（DEU 域内）**。本波用 INSTITUTIONS 时 sub ≤0.08。⇒ **在 DEU，保住 sub 的已验证搭档是 MODEL，不是 INSTITUTIONS**。⚠ 该结论只到「平台实读 + 同区」，跨区禁用；且若沿用「已点亮塔（MODEL）不作战役目标」的口径（`mcp__wqb-db__list_wave_results` 中 `s2_risk60_d1` 记录的用户铁律），**把 MODEL 作搭档腿是否受限需用户裁定**，本档不擅自推荐。

## §5 塔位判读（点塔相关性）

平台 `get_alpha_details.pyramids` 逐臂实读（10/10）：

- **目标塔 INSIDERS 出现 10/10 臂**：
  - 单塔 5 条（effective=1）：臂1 `2r5a6KzP`、臂2 `ZYa2zo38`、臂5 `wponGeg5`、臂6 `RRe2zrLj`、臂7 `oma3GYeb` = `DEU/D1/INSIDERS`×1.6。
  - 双塔 5 条（effective=2）：臂3 `kqa1GK2L`、臂4 `A1xgz3MQ`、臂8 `vRAeGm0Q`、臂9 `N1PgzOk8`、臂10 `3q0aPAYe` = `DEU/D1/INSTITUTIONS`×1.6 + `DEU/D1/INSIDERS`×1.6。`ra.pyramid_short` 同步为 `institutions/insiders`。
- **点位 ≠ 点亮**：10/10 臂 RA fail ≥1 ⇒ **本波实际点亮 INSIDERS 塔 0 颗、INSTITUTIONS 塔 0 颗**。塔计数不变（insiders 1/3、institutions 1/3，见 `CAMPAIGN_REPORT_20261116.md:34`）。
- **双塔件占比 5/10**：本波是全 run 里少见的「一半双塔」，但 effective=2 的双塔件同时受两塔配额约束，且它们恰好全部是 `atom_n_datasets=2` 的 combined 件（走 IS_LADDER）——**双塔 + 双集 + 单位警告三重叠加**，是这 5 臂可推进性最差的根因。
- **族内存量不改变本波塔位结论**：6 条 `failed_ra_count=0` 的 INSIDERS 族存量件（§2.4）是**别的几何 + 多腿 add + dual(INSIDERS,MODEL)**，既不是 insiders1，也不在本波归属内；它们的塔位点亮状态本档未逐条核（只核了 `Vk6eodeb` 的 pyramids）。

## §6 数据层判读（data_excluded 与信号死分开）

- **不 data_excluded**：见 §3.4——7/10 臂 LC/SC 71–143、pnl 正、TO 正常；数据集 `insiders1` 8 字段全部 VECTOR、平台 `get_datafields` 实读 8/8（`FIELD_insiders1_20261116.md:23-40`），本波 preflight `unknown_fields=[]`。**没有任何"取不到数"的证据**。
- **不判信号死**：本波 10 臂、**1 套配置**、**1 个窗口（66）**、**无翻符号对照**、**无掩码单独对照**、5 臂需 rebuild ⇒ 六维闸 D1/D2/D3/D6 未达（§7），按「探针不产生判死」与 AGENTS §7.6，**只能记 provisional**。
- **单集路线的"封顶"与数据集的"判死"是两件事**：`BE176` 判的是「insiders1 **单数据集**（ATOM）上限 ≈1.30，三波 30 臂收敛」——这是**路线级 capped**，可写进"不要再重复单集 66/22/132 窗扫"的排除表；但它**不等于数据集死**，也不覆盖本波的**配对路线**。
- **本波属"信号层弱 + 表达层坏 + 配置层未扫"的混合，不是数据层排除**：ARM1/2/4 的塌缩是表达层（§3.4）；ARM3/10 的 0.35 是被掩码修好的弱核；ARM5–9 的 0.35–0.81 是同配置下的真实弱读数；**配置层（decay4/nanOFF/其它中性化）本波一条没扫** ⇒ 无法区分"这套配置弱"与"信号弱"。

## §7 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| **D1 结构互异模板 ≥10** | 名义 10 臂，结构互异约 **6–8**：core A（臂1）/ core A′（臂2）/ core B 三种壳（臂5/6/7）/ A×mask（臂3）/ A′×mask（臂10，与臂3 读数逐位相同 ⇒ 不计独立）/ A×bucket（臂4）/ B×mask 两向（臂8/9，同假设正反两向 ⇒ 计 1）。按「换常数、同假设两向不算」口径 **<10** | **✗ 未达** |
| **D2 字段族自测** | insiders1 只用 `insd1_holdings`（存量/差分）与 `insd1_valueeur`（max/sum 集中度）**2 个信号字段**；未碰 `insd1_shares` / `insd1_price` / `insd1_value` / `insd1_tradesignificance`；institutions6 只用 2 个（`aggregate_share_count_institutions`、`aggregate_share_count_all_owners`）。⚠ 其中 `value/price/significance` 已有判死记录（`deu-insiders-evidence.md:47-54`：1.14 / 1.13 / 1.21），属"有先验的未重测"，**不是"未测即封禁"** | **✗ 未达** |
| **D3 矩全家（水平/一阶差/二阶波动/比值或信噪比 各≥1）** | 一阶差 ✓（Δ66）、二阶波动 ✓（Δ66÷ts_std_dev252、且 ts_sum 66 的时序聚合）、比值 ✓（Δ÷水平、max÷sum）；**纯水平腿 ✗**（无 `ts_backfill(vec_sum(holdings),250)` 的直接水平臂）；**信噪比 ts_ir ✗** | **✗ 未达**（缺水平/SNR） |
| **D4 分组轴 ≥2** | sector ✓（臂1/3/5/8/9/10）、bucket(institutions share) ✓（臂4）；另有裸 rank（无分组）作为对照 | **✓ 达** |
| **D5 非线性 ≥1** | `if_else` / `bucket` / `tail` / `winsorize` / `rank` / `group_rank` | **✓ 达** |
| **D6 配置 ≥2** | 全波 **1 套**：DEU/TOP500/D1 + decay0 + SUBINDUSTRY + trunc0.08 + nanHandling ON。**decay 4（区域生产档）与 nanHandling OFF 一条未扫** | **✗ 未达** |

⇒ 缺 **D1 / D2 / D3 / D6**：**不得判死、不得封集、不得作为邻接数据集/族的先验**（AGENTS §7.6）。本波的所有弱读数只在「decay0/nanON/SUBINDUSTRY/单一 66 窗」这一格内成立。

## §8 近闸候选（ask 口径：S≥1.2 或距任一硬闸 ≤0.4；≤2 条，按 S 降序）

**本波 0 条近闸候选。** 逐条核对（用平台实读限值）：

- **S≥1.2：无**。最高 S = 0.81（臂7），距 1.58 差 **0.77**。
- **距 S 闸 ≤0.4：无**（最接近 臂7，差 0.77）。
- **距 F 闸（1.0）≤0.4：无**（最接近 臂7 F 0.50，差 0.50）。
- **距 2Y 闸（1.58）≤0.4：无**。最接近是 臂8 `vRAeGm0Q` 2Y 1.17，差 **0.41**——**刚好出 0.4 带**（1.58−1.17=0.41 > 0.40），且其 S 0.74 距闸 0.84、F 0.43 距闸 0.57、sub 0.08，**不构成可推进的 near**。
- **距本地 sub 线（1.0）≤0.4：无**（最高非退化 sub = 0.38，臂6）。
- **距 TO 上限（0.70）≤0.4：有 2 条，但不可用**——臂1 TO 107.58%、臂4 107.60%，**超出 0.376 ≤ 0.4**。⚠ **本档明确不把它们列入 near**：同两条臂的 S 为 −0.11 / −0.07（距闸 1.65–1.69）、2Y −1.00 / −1.11（距闸 2.58–2.69）、CW 0.5 vs limit 0.1、DD 89–91%、LC/SC 1/5 与 0/4。把它们当 near 会让下一步"先测 prod"落到一条负 Sharpe、换手 108%、回撤 90% 的臂上，**与「先测 prod 再扫参」的意图相反**。此条如实登记为"机械判据命中但无经济含义"。
- 区域自己的 near 池线（`tracking/DEU/config/thresholds.json` 的 `near.sharpe_min = 1.0`）同样**0 条满足**——与 ask 判据结论一致。

⇒ n_pass = 0，n_near = 0。

## §9 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`**。依据：

1. **单集（ATOM）路线已被独立证据封顶在 1.30**（`BE176_INSIDERS1_CEILING_130_20261112.md:23,28-30,50`，三波 1.22/1.30/1.19、30 臂收敛）。本波 5 条 atom 臂 0.35–0.81 **低于**该上限 ⇒ 既不支持"单集可行"，也不构成对上限的证伪。该事实记在**路线层（capped-route 排除表）**，不改写数据集终态。
2. **配对路线（institutions6）没有取得可判读读数**：5/5 臂 `UNITS` 警告 ⇒ `rebuild_needed`。故不能写 capped（"剩余结构手段全部实测"这一条不成立）。
3. **数据层无排除**：7/10 臂 LC/SC 71–143、pnl 正、TO 正常（§3.4/§6）。
4. **六维 D1/D2/D3/D6 未达**（§7）⇒ 按 AGENTS §7.6 **不得终判死、不得封集、不得作邻接集先验**。
5. **DB 侧一致**：`mcp__wqb-db__get_dead_datasets("DEU")` 返回 19 个判死集，**不含 `insiders1`**（含 `insider_trx_matrix`，是不同数据集）。
   ⇒ 若下一波把配对路线 rebuild 干净后仍 ≤0.8、且补到 ≥2 套配置 + 水平/SNR 矩 + ≥10 互异模板，**那时**才轮得到 dataset 级 `capped` 或 `dead_proposed`；现在不够。

**波 verdict = `FAIL`**（判定表 `src/wqb/wave_results_contract.py:79-90`：PASS=≥1 达标 / PARTIAL=0 达标但 ≥1 近闸 / FAIL=0 达标 0 近闸；本波 `n_pass=0 / n_near=0`）。**未自造枚举值。**

- **稳健性**：该 FAIL 对 sub 口径不敏感——即便把 sub 判据换成平台动态限（0.17–0.38，比本地 1.0 宽得多），10/10 臂仍全部挂 LOW_SHARPE（S≤0.81 vs 1.58）+ LOW_FITNESS（F≤0.50 vs 1.0）。
- **不是"全灭到无信息"**：best S 0.81 / best 2Y 1.17 / 8/10 臂 S>0 是"真实但远不到闸"的弱信号，与 `s2_insider_trx_matrix_d1`（2026-09-22，best 0.33）那种全灭不同量级；但按判定表，弱≠近闸。
- **停止规则上下文**：DEU 最近 3 个 closed 波 = `rt-fundamental-w4` **PASS** / `rt-fundamental-w5` **PARTIAL** / 本波 **FAIL**（DB id 2209/2210）；按规则 B「连续可计数 FAIL ≥K」计，本波使 `insiders1` 轴的连续 FAIL 计数 = 1（前一波是 PARTIAL，不连号）。

## §10 newLever 登记

**空串（本波不入册新杠杆）**。理由：

1. **无可入册的正向杠杆**：本波所有复合形态都**不高于**其对应单腿（§3.3）——`tail(winsorize(rank))` 稀释 0.21 S、掩码对 S/F/sub 净稀释、sector 分组零增益、bucket 分组零作用。入册需要"高于"，本波没有。
2. **唯一"效果"是换手压制，不是强度**：掩码把 TO 从 107.58%/21.94% 压到 2.39%/2.44%，同时把 S 从 −0.11/−0.01 抬到 0.35 —— 但这是**修宽度/换手的副作用**（同核无掩码时票池只有 1/5、0/0），与既有已入册口径「门控只修 prod/robust，不造强度」（`insiders.md:52`）**重复**，不是新杠杆；且 5 臂全带 UNITS 警告、无掩码单独对照 ⇒ 效应量不可归因。
3. **"贵在选对第二腿"这一条本波给不出正例**：INSTITUTIONS 作第二腿只有 2Y +0.29、S/F/sub 全降；**MODEL 作第二腿的 sub 1.49/1.51 是 11-12 就有的存量事实**（`CRITICAL_INSIDERS_SINGLE_SIGNAL_20261112.md:38`「Vk65zLzG 已证 insiders×model 可到 S 1.79 且全闸」），**属旧杠杆，不是本波新发现**。
4. ⇒ 待下一波满足「同核、单变量、带裸对照、脱开单位错误」三条后，再议入册。

## §11 证据通道与盲区

**本轮实跑的核验（全部只读，零写入生产库）**：
- `mcp__wq-brain-http__batch_get_alpha_metrics(10 ids)`：10/10 success，S/F/2Y/sub/TO/margin/DD/`failed_ra_count` 与 ask 转录**逐值一致**。
- `mcp__wq-brain-http__get_alpha_details`：**逐臂 10/10** 取回 `settings`、`metrics`（含 longCount/shortCount）、`ra.ra_failed_checks`、`checks.fail`（含 limit）、`checks.warning`（含 UNITS 原文）、`pyramids.list`（含 multiplier/effective）、`code`。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w1)`：10 条，表达式与 `logs/_tmp_rt-insiders-w1_arms.json` **逐条同序**；`atom_flag` = 5 atom(1 集) + 5 combined(2 集)，`atom_n_datasets` 同步。
- `mcp__wqb-db__get_wave_result(DEU, rt-insiders-w1)`：**未找到**（本档为首次写入）。
- `mcp__wqb-db__get_dead_datasets("DEU")`：19 集，不含 `insiders1`。
- `mcp__wqb-db__query_dataset_profile(DEU)`：**count=0**（DEU 无画像行）⇒ 本档**不用**数据集画像表做任何判据（如实登记为通道空）。
- `batch_get_alpha_metrics(6 条 INSIDERS 族存量件)`：6/6 success（§2.4）。

**盲区（如实登记，不猜不补）**：
1. **符号指纹未测**：0 条翻符号臂，ask 的严格判据无法执行（§3.1）；FIELD 档 §5 要求同波带反号对照，本波未带。
2. **掩码单独对照缺失**：无 `if_else(cond, 1, 0.5)` 类臂 ⇒ 掩码收益 vs 核收益不可分离（§3.2）。
3. **5 臂 `rebuild_needed`**：臂3/4/8/9/10 平台 warning `UNITS`（`add` 对 CSShare 字段加无量纲 1）；读数照录但**不作配对结论**。
4. **窗口梯未扫**：全波只用 66（与 252 归一）；ask 提到的「ts_mean/ts_ir 22→66→132 单峰」衰减梯判据**本波不适用/未测**，不得据此说"结构没对上"。
5. **配置只 1 套**：decay0/nanON 探针档；区域生产档（decay4/nanOFF）一条未跑 ⇒ **配置层死/活未判**。
6. **prod / self 相关性全部 null**：按分工归相关性员，本档不测、不猜。
7. **年度分年未取**：本波未跑 `get_alpha_yearly_stats`；ask 说「十年跨度已核并关闭（`XgaGb3J1` / `d5a2aO7v` 2014-2023 逐年 pnl>0）」— 该两条不在本波 10 臂内，**本档仅转录，未复跑**。
8. **6 条族内存量件只取了指标**：未逐条取 `pyramids`/`code`（仅 `Vk6eodeb` 取全）⇒ 它们的塔归属与几何**未逐条核**。
9. **臂2 读数自相矛盾**：LC/SC 0/0 但 pnl/TO/bookSize 非零 ⇒ 平台指标不自洽；`sub 11.18` 与 `investability_ratio −84` 均不可作证据，本档已按此处理。
10. `create_multi_simulation` 不暴露 startDate/endDate，平台回显 2014-01-01→2023-12-31 与 `settings.json` 的 2013-01-01 不同——原样记录平台值，不作推断。

## §12 终态

- **波**：`FAIL`（0 达标 / 0 近闸）；best S **0.81**（`oma3GYeb`，臂7）/ best 2Y **1.17**（`vRAeGm0Q`，臂8）/ best F 0.50 / best margin 20.39bp。
- **数据集**：`insiders1` = **provisional**（不判死、不 data_excluded、不封集）。单集路线**已由 BE176 封顶 1.30**（路线级排除，三波 30 臂），本波不重复该路线；配对路线（institutions6）**5/5 rebuild_needed**，未取得可判读证据。
- **塔位**：INSIDERS 10/10 臂归属（5 单塔 + 5 双塔 INSIDERS+INSTITUTIONS），**实际点亮 0**（10/10 臂 RA fail≥1）。
- **提交链**：**未推进**（0 达标；无 near 件；prod/self 未测）。
- **下一步（按优先级）**：
  1. **修单位**：把 `aggregate_share_count_institutions / (aggregate_share_count_all_owners + 1)` 的 `+1` 换成同单位守卫（或用 `rank` 后比较），重建 5 条配对臂 → 再判配对路线；
  2. **补掩码单独对照**（`if_else(cond, 1, 0.5)` 一类）与**翻符号对照**（θ → −θ），否则方向与掩码贡献永远分不开；
  3. **先定"强腿"再加搭档**：11-12 的结论是「强腿换搭档仍强才算真强腿」（`CRITICAL_INSIDERS_SINGLE_SIGNAL_20261112.md:38`、`insiders.md:52`）——本波拿 0.35–0.81 的弱腿去换搭档，按该方法论必然不成立；若要继续 insiders 配对路线，应先用 1.30 上限附近的结构作腿；
  4. **配置维至少补一档**（decay 4 / nanHandling OFF，即区域生产档），否则无法区分"配置层死"与"信号层死"；
  5. **不要再扫单集 66 窗的既有形态**：BE176 三波已收敛 1.22–1.30，本波 0.35–0.81 再次低于该上限，重复无增量。
