# WAVE rt-insiders-w2 — `insiders1` 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集：`insiders1`（目标塔 **INSIDERS**）；配对集：`institutions6`（塔 INSTITUTIONS）
- 配置（平台 `get_alpha_details` 逐臂回显，10/10 一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、maxPosition=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR、simulationMode=FULL；`startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:5-16`（decay=4、nanHandling=OFF、2013-01-01 起）不同 ⇒ 仍是**探针口径配置（decay0/nanON）**，与 w1 同档。**本波所有结论只在 decay0/nanON/SUBINDUSTRY/单一 66 窗这一格内成立**。
- 派发/收割（收割说明转录，本档未重跑派发）：`preflight_expressions` valid=true / unknown_fields=[] / any_changed=false（10/10；覆盖 `aggregate_equity_value_*` / `aggregate_share_count_*` / `insd1_holdings` / `insd1_valueeur` 六字段）；`operator_audit` safe=true / violations=[]；精确式查重全仓 0 历史命中（仅命中本波输入件 `logs/_tmp_rt-insiders-w2_arms.json`、`logs/_tmp_rt_insiders_w2_arms.txt` 与闸门临时件）；与 w1 已入库 10 条逐条不同。
  - **派发异常**：首次 `create_multi_simulation` 返回 **429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED**（账号级并发上限，非表达式问题）→ 退避 150 s 后**单次**重试成功（未多次硬重试）。multisim `opjxw6pb4USbZxCLVgrUEf`。
  - 轮询：首次 children=0，约 2 分钟后第二次查询即 10/10 all_terminal=true、**errors=0（全 COMPLETE，无 WARNING / 无 CANCELLED / 无 UNITS）**。`harvest_multisim_alphas` 首试成功（未走 404 兜底），total=10/complete=10/error_count=0；逐臂用平台 `code` 核对归属，10 条与臂表/提交顺序逐条一致（臂1→`gJaR5gov` … 臂10→`9qla3dJV`）。
  - 落库：`upsert_backtest_rows(DEU, rt-insiders-w2, insiders1, 10)` → n=10；写后 `list_expressions` 10 条，`alpha_id/sharpe/fitness/margin/turnover` 与平台逐条一致。
- 判读基准（ask 给定，本档另附平台实读限值见 §1.1）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0 / 0.01≤TO≤0.70 / margin≥0.0005 / CW≤0.5 / self 与 prod 各<0.70。
- 闸种：**5 条 atom 单集件走 `LOW_2Y_SHARPE`（limit 1.58）；5 条 combined 双集件走 `IS_LADDER_SHARPE`（year=2，limit 1.58）**；`two_year_sharpe` 与 RA 载体逐臂一致（10/10）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

指标经 `batch_get_alpha_metrics`（10/10 success）与 `get_alpha_details`（10/10）逐臂复核，与 ask 转录**逐值一致**。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔（pyramids/list） | RA fail（平台 `ra.ra_failed_checks`） |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|
| 1 | `gJaR5gov` | **新鲜度单腿**：`group_rank(1/(days_from_last_change(vec_avg(insd1_holdings))+1), sector)` | 0.78 | 0.51 | 1.08 | 0.18 | 5.39% | 15.20% | 19.89bp | 114/134 | DEU/D1/INSIDERS×1.6（eff 1） | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.168741>0.1@2014-01-02**, LOW_SUB(0.37), LOW_2Y |
| 2 | `mLarN0x1` | **离散度单腿**：`group_rank(ts_sum(vec_stddev(ve)/vec_sum(ve),66), sector)` | 0.72 | 0.44 | 0.60 | **0.44** | 4.54% | 14.35% | 21.00bp | 97/140 | DEU/D1/INSIDERS×1.6（eff 1） | **3**：LOW_SHARPE, LOW_FITNESS, LOW_2Y（sub/CW/TO/margin 全 pass） |
| 3 | `d5aE63Ew` | **乘法**：`multiply(rank(conc66), rank(1/(dfc(holdings)+1)))` | **0.89** | **0.63** | 0.92 | 0.26 | 5.76% | 14.93% | **21.56bp** | 124/158 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.42), LOW_2Y |
| 4 | `0mPeLNer` | **减法**：`subtract(rank(conc66), rank(ts_ir(vec_avg(holdings),66)))` | −0.16 | −0.06 | −0.53 | 0.28 | 12.29% | **44.56%** | −2.81bp | **31/30** | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, **CW 0.285488>0.1@2014-02-19**, LOW_2Y |
| 5 | `j2a9JP9k` | **变化轴**：`rank(ts_delta(ts_sum(conc66), 66))` | 0.19 | 0.05 | −0.93 | −0.11 | 9.07% | 14.85% | 1.78bp | 142/142 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.09), LOW_2Y |
| 6 | `QP02ANn5` | **掩码（价值口径）**：`if_else(rank(bf(inst_eqv/all_eqv,252))<0.5, rank(conc66), 0.5)` | 0.77 | 0.45 | **1.11** | 0.09 | 4.71% | 13.42% | 18.51bp | 133/128 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.37), IS_LADDER |
| 7 | `0mPeLNAr` | **掩码（股数口径）**：同臂6，比率换 `inst_shares/all_shares` | 0.75 | 0.44 | 1.04 | 0.09 | 4.58% | 13.72% | 18.54bp | 133/128 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.36), IS_LADDER |
| 8 | `akaA8QN5` | **掩码高带（反向分支）**：`>0.5` 版臂7 | 0.57 | 0.30 | 0.50 | 0.14 | 4.98% | 11.88% | 14.06bp | 131/141 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.27), IS_LADDER |
| 9 | `1YWaRlJm` | **bucket 分组**：`group_rank(conc66, bucket(rank(bf(inst_eqv/all_eqv,252)),0/0.5/1))` | 0.82 | 0.48 | 0.50 | 0.21 | 5.59% | **11.10%** | 15.33bp | 135/152 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.39), IS_LADDER |
| 10 | `9qla3dJV` | **掩码 + 新鲜度**：`if_else(mask<0.5, rank(fresh), 0.5)` | 0.50 | 0.24 | 0.96 | 0.13 | 4.10% | 19.70% | 14.22bp | 132/127 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.24), IS_LADDER |

- `conc66` = `ts_sum(divide(vec_max(insd1_valueeur), vec_sum(insd1_valueeur)), 66)`；`fresh` = `1/(days_from_last_change(vec_avg(insd1_holdings))+1)`；`bf` = `ts_backfill`。
- **本波极值**：best S **0.89**（臂3）/ best F **0.63**（臂3）/ best 2Y **1.11**（臂6）/ best sub **0.44**（臂2）/ 最低 DD **11.10%**（臂9）/ best margin **21.56bp**（臂3）。
- **0 达标**：10/10 臂 `failed_ra_count` ≥3（5/3/4/4/4/4/4/4/4/4），**无一条 RA 全闸**；`status` 10/10 = `UNSUBMITTED`（提交态）；仿真态全 COMPLETE、errors=0。

### 1.1 平台闸限实读（补齐 ask 的「平台 LOW_SHARPE limit 未读到」）

`get_alpha_details.checks.fail` 逐臂携带 `value/limit`，实读：

| 闸 | 平台实读 limit | 与 ask 基准的关系 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10 臂） | 与内部严线一致 |
| LOW_FITNESS | **1.0** | 一致 |
| HIGH_TURNOVER | **0.70**（本波 10/10 pass，最高 TO 12.29%） | 一致 |
| CONCENTRATED_WEIGHT | **0.10**（臂1 value 0.168741@**2014-01-02**；臂4 value 0.285488@2014-02-19） | ⚠ **比 ask 的 CW≤0.5 严 5 倍**；0.5 是本地 review 线（`tracking/DEU/config/thresholds.json:20`） |
| LOW_2Y_SHARPE / IS_LADDER_SHARPE | **1.58**（year=2） | 一致 |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂不同**：臂5 0.09 / 臂10 0.24 / 臂8 0.27 / 臂7 0.36 / 臂6 0.37 / 臂9 0.39 / 臂3 0.42 / 臂1 0.37；臂2/臂4 判 PASS（limit 未回显） | ⚠ **sub≥1.0 是本地 review 线，不是平台闸限**（`thresholds.json:21`）；平台动态限只有 0.09–0.42 |

⇒ 两点：① ask 的「平台 LOW_SHARPE limit 本轮未读到」**本轮已实读补齐 = 1.58**；② **verdict 与 sub 口径无关**——换任何 sub 判据，10/10 臂仍全部挂 LOW_SHARPE + LOW_FITNESS（S≤0.89 vs 1.58、F≤0.63 vs 1.0）。

## §2 逐臂归因条目

### 2.1 新机制单腿（臂1 新鲜度 / 臂2 离散度）

1. **臂1 `gJaR5gov`（事件新鲜度：距上次持仓变动的天数取倒数，sector 组内秩）**：S 0.78 / F 0.51 / 2Y **1.08** / sub 0.18 / TO 5.39% / DD 15.20% / margin 19.89bp / LC-SC 114/134；RA 5 挂，其中 **CW 0.168741>0.1 出现在 2014-01-02（样本首日）**。⇒ 机制**成立且不靠换手**（TO 5.39%、宽度 248 只），是本波 2Y 第二高的单腿；CW 挂点落在首日，形态像建仓首日的小分母伪影，**可修但未验证**（本档不假设它已被修）。与 FIELD 档 M7「事件新鲜度：越近越未衰减」的先验方向一致（`FIELD_insiders1_20261116.md:245`，该档原判「N：符号是假设、未验证」）——**本波把 M7 从"未验证"推进到"实测 S 0.78/F 0.51/2Y 1.08、方向为正"**。
2. **臂2 `mLarN0x1`（离散度：`vec_stddev/vec_sum` 的 66 日均值，sector 组内秩）**：S 0.72 / F 0.44 / 2Y 0.60 / **sub 0.44（本波最高，且平台 LOW_SUB 判 PASS）** / TO 4.54% / DD 14.35% / margin 21.00bp / LC-SC 97/140；**RA 只 3 挂（本波最少）**。⇒ 与 FIELD 档 M5「日内集中度」互为**同一族的两面**：M5 是"最大单笔占当日总额"（max/sum），本臂是"单笔金额的离散度"（stddev/sum）。两者 S 相近（0.72 vs w1 的 0.81），但**离散度版的 sub 显著更高（0.44 vs w1 集中度 0.19）且回撤更低**。⇒ 若后续目标函数是 **sub**，本族应优先用 stddev/sum 而不是 max/sum。

### 2.2 乘法复合（臂3）——本波唯一"高于所有对应单腿"的复合

3. **臂3 `d5aE63Ew`（`multiply(rank(conc66), rank(fresh))`，单集 atom）**：S **0.89（本波最高）** / F **0.63（最高）** / 2Y 0.92 / sub 0.26 / TO 5.76% / DD 14.93% / margin **21.56bp（最高）** / LC-SC 124/158；RA 4 挂（S/F/sub/2Y），CW/TO/margin pass，CLUSTER 0.68 warning。
   - **vs 左腿（conc 单腿 = w1 `oma3GYeb`，表达式逐字相同 `rank(ts_sum(divide(vec_max(ve),vec_sum(ve)),66))`、同配置同日期）**：S **+0.08** / F **+0.13** / 2Y +0.09 / sub **+0.07** / TO +1.03pp / DD +1.03pp / margin **+1.17bp**。
   - **vs 右腿（fresh 单腿 = 臂1；⚠ 差异含 `group_rank(,sector)`→`rank`，非纯单变量）**：S **+0.11** / F **+0.12** / 2Y −0.16 / sub **+0.08** / margin **+1.67bp** / DD −0.27pp。
   - ⇒ **S/F/sub/margin 四项均高于两条单腿 ⇒ 不触发稀释铁律**。这是本族两波里**第一次**出现"复合高于单腿"。机理可解释：「最大单笔占当日总额（规模/信念集中）」×「距上次变动天数（信息新鲜度）」是**两个不同维度**的乘积（"又大又新"），不是 BE176 所判的"同源潜变量叠加稀释"（`BE176_INSIDERS1_CEILING_130_20261112.md:35-40`）。
   - ⚠ 代价：2Y 0.92 **低于** freshness 单腿 1.08；且仍远在 S 闸 0.69 之外、也在 BE176 的单集上限 1.30 之下。

### 2.3 减法复合（臂4）——破坏性，且缺对照不可完全归因

4. **臂4 `0mPeLNer`（`subtract(rank(conc66), rank(ts_ir(vec_avg(holdings),66)))`）**：S −0.16 / F −0.06 / 2Y −0.53 / sub 0.28 / TO 12.29% / DD **44.56%** / margin −2.81bp / **LC-SC 31/30**；RA 4 挂，**CW 0.285488>0.1@2014-02-19**。
   - **vs 被减腿（conc 单腿 = w1 臂7）**：S **−0.97** / F −0.56 / 2Y −1.36 / sub +0.09 / TO +7.56pp / DD **+30.66pp** / margin **−23.20bp** / 票池 129-140 → 31-30。
   - ⚠ **归因边界**：本波**没有 `ts_ir(vec_avg(insd1_holdings),66)` 的单腿对照臂**（w1 也没有）⇒ 无法区分"减法把两条有效腿相消"与"ts_ir 腿本身强负、减它反而增益但被 conc 腿拉平"。**只能记"减法形态在本波是破坏性的"，不能记"ts_ir 是负信号"。** 这是本波第 2 个设计缺口（w1 已登记同类缺口：缺掩码单独对照）。

### 2.4 变化轴（臂5）——水平 vs 一阶差的干净消融

5. **臂5 `j2a9JP9k`（`rank(ts_delta(ts_sum(conc66), 66))`）**：S 0.19 / F 0.05 / **2Y −0.93** / **sub −0.11** / TO 9.07% / DD 14.85% / margin 1.78bp / LC-SC 142/142；RA 4 挂。
   - **vs 水平版（同一核，w1 臂7，表达式仅差外层 `ts_delta(·,66)`）**：S **−0.62** / F **−0.45** / 2Y **−1.76** / sub **−0.30** / TO +4.34pp / DD +0.95pp / margin **−18.61bp**。
   - ⇒ **本族信号在"水平"不在"变化"**：同一集中度核做 66 日差分后 S 从 0.81 掉到 0.19、2Y 转为 −0.93。这是一条**干净的单变量消融**，同时把六维 D3 的「一阶差」维度补齐（结果为负）。

### 2.5 掩码族（臂6/7/8/9/10）——单位已修干净，配对结论本波才可判读

**跨波关键闭合**：w1 的 5 条配对臂全部带平台 `UNITS` 警告（根因：`aggregate_share_count_all_owners + 1` 对 CSShare 字段加无量纲 1），因此 w1 只能记「配对路线无可判读读数」。**本波比率全部改为 `divide(aggregate_*_institutions, aggregate_*_all_owners)`，不加 1**，平台 5/5 臂 **无 UNITS 警告**（warning 仅 CLUSTER_TEST / MATCHES_COMPETITION / MATCHES_THEMES）⇒ **w1 的判读缺口在本波闭合，以下配对结论首次可判**。

6. **臂6 `QP02ANn5`（价值口径掩码 `<0.5` + conc）**：S 0.77 / F 0.45 / **2Y 1.11（本波最高）** / sub 0.09 / TO 4.71% / DD 13.42% / margin 18.51bp / LC-SC 133/128；RA 4 挂。
7. **臂7 `0mPeLNAr`（股数口径掩码 `<0.5` + conc）**：S 0.75 / F 0.44 / 2Y 1.04 / sub 0.09 / TO 4.58% / DD 13.72% / margin 18.54bp / LC-SC 133/128；RA 4 挂。
   - **臂6 vs 臂7 = 纯口径对照（只换比率的分子/分母字段）**：S +0.02 / F +0.01 / 2Y +0.07 / sub 0 / TO +0.13pp / DD −0.30pp / margin −0.03bp，**LC/SC 逐位相同（133/128）** ⇒ **价值口径与股数口径几乎完全等价**。⇒ 以后不必再为"用权益市值还是股数"消耗臂位。
8. **臂8 `akaA8QN5`（同一股数口径、比较方向翻成 `>0.5`）**：S **0.57** / F 0.30 / 2Y 0.50 / sub 0.14 / TO 4.98% / DD 11.88% / margin 14.06bp / LC-SC 131/141；RA 4 挂。
   - **vs 臂7（只翻比较方向，其余逐字相同）**：S **−0.18** / F −0.14 / 2Y −0.54 / sub +0.05 / TO +0.40pp / DD −1.84pp / margin −4.48bp。⇒ **低机构持股（<0.5）是强侧**，且 TO/DD/LC-SC 逐项不同、两向不对称差 0.18 > 0.1 ⇒ **不是"方向层无净信息"的退化指纹**（§4）。
9. **臂9 `1YWaRlJm`（bucket 分组，价值口径 0/0.5/1）**：S 0.82 / F 0.48 / 2Y 0.50 / sub 0.21 / TO 5.59% / **DD 11.10%（本波最低）** / margin 15.33bp / LC-SC 135/152；RA 4 挂。
   - **vs 裸（w1 臂7，同核无分组）**：S **+0.01** / F −0.02 / 2Y **−0.33** / sub +0.02 / TO +0.86pp / DD **−2.80pp** / margin −5.06bp。⇒ bucket 分组**不增 S、明显降 2Y，但换到最低回撤**；是一个"风险换收益"的壳，不是强度壳。
10. **臂10 `9qla3dJV`（掩码 `<0.5` + 新鲜度腿）**：S 0.50 / F 0.24 / 2Y 0.96 / sub 0.13 / TO 4.10% / DD 19.70% / margin 14.22bp / LC-SC 132/127；RA 4 挂。
    - **vs 臂1（新鲜度单腿；⚠ 差异含 `group_rank(,sector)`→`rank`，非纯单变量）**：S **−0.28** / F **−0.27** / 2Y −0.12 / sub −0.05 / TO −1.29pp / DD **+4.50pp** / margin −5.67bp。⇒ 掩码套在**新鲜度腿**上是**强稀释**（与套在集中度腿上只 −0.06 形成鲜明对照）。⇒ **掩码的损益依核心而异**：对"规模/集中度"核近乎中性（−0.06），对"时间距离"核是强负（−0.28）。

## §3 对照实验汇总（本波主要产出：裸 vs 改造，全部同配置同日期）

| # | 对照 | 改造件（读数 S/F/2Y/sub） | 裸件（读数） | Δ | 判定 |
|---|---|---|---|---|---|
| C1 | 乘法 vs 左腿 | 臂3 `0.89/0.63/0.92/0.26` | w1 臂7（conc 水平，表达式逐字相同）`0.81/0.50/0.83/0.19` | **+0.08/+0.13/+0.09/+0.07** | **增益**（不触发稀释铁律） |
| C2 | 乘法 vs 右腿 | 臂3 同上 | 臂1 fresh `0.78/0.51/1.08/0.18` | +0.11/+0.12/**−0.16**/+0.08 | 增益（2Y 例外；含分组差异） |
| C3 | 变化 vs 水平 | 臂5 `0.19/0.05/−0.93/−0.11` | w1 臂7 `0.81/0.50/0.83/0.19` | **−0.62/−0.45/−1.76/−0.30** | **变化轴死**（干净单变量） |
| C4 | 减法 vs 被减腿 | 臂4 `−0.16/−0.06/−0.53/0.28` | w1 臂7 `0.81/0.50/0.83/0.19` | −0.97/−0.56/−1.36/+0.09 | **破坏**（缺 ts_ir 单腿对照） |
| C5 | 掩码 vs 裸 | 臂7 `0.75/0.44/1.04/0.09` | w1 臂7 `0.81/0.50/0.83/0.19` | −0.06/−0.06/**+0.21**/−0.10 | 以 S/F/sub 换 2Y |
| C6 | 口径（价值 vs 股数） | 臂6 `0.77/0.45/1.11/0.09` | 臂7 `0.75/0.44/1.04/0.09` | +0.02/+0.01/+0.07/0 | **等价**（LC/SC 逐位相同） |
| C7 | 高带 vs 低带 | 臂8 `0.57/0.30/0.50/0.14` | 臂7 `0.75/0.44/1.04/0.09` | **−0.18**/−0.14/−0.54/+0.05 | 低带强侧 |
| C8 | bucket 分组 vs 裸 | 臂9 `0.82/0.48/0.50/0.21` | w1 臂7 `0.81/0.50/0.83/0.19` | +0.01/−0.02/**−0.33**/+0.02 | S 零增益、2Y 大幅下降、DD −2.80pp |
| C9 | 掩码 + fresh vs fresh | 臂10 `0.50/0.24/0.96/0.13` | 臂1 `0.78/0.51/1.08/0.18` | **−0.28**/−0.27/−0.12/−0.05 | 强稀释（含分组差异） |

**跨波复现（两波同向，构成"跨波实证"）**：
- **掩码指纹**：w1（`0.74 vs 0.81`）S −0.04 / 2Y **+0.29** / sub −0.08；w2（C5）S −0.06 / 2Y **+0.21** / sub −0.10 ⇒ **"institutions 掩码：S/F/sub 小幅负、2Y +0.2~0.3"两波独立复现**。
- **分支方向**：w1（<0.5 0.74 vs >0.5 0.53，Δ0.21）；w2（C7：0.75 vs 0.57，Δ0.18）⇒ **低机构持股为强侧，两波同向、量级接近**。
- **单集上限**：BE176 判 `insiders1` 单集 S 上限 ≈1.30（三波 1.22/1.30/1.19）；本波单集最强 0.89（臂3）**仍低于该上限** ⇒ 两波合计 0/20 臂破 1.30，**上限判断继续成立**。

## §4 符号指纹 / 方向

- **严格符号指纹仍未测**：10 条表达式**无整式取反**（`logs/_tmp_rt-insiders-w2_arms.json` 全文无前置负号 / `multiply(-1,…)`）。ask 的判据（S(−expr)≈−S(expr) 且差<0.03 且 TO/DD/longCount 逐位相同 ⇒ 方向层无净信息）**无法执行**，如实记「未测」。⚠ FIELD 档 §5 要求「增持语义必须同波带反号对照臂」（`FIELD_insiders1_20261116.md:207-215`），**w1/w2 两波连续未带** ⇒ 该缺口连续两波登记。
- **可做的是互补分支对**（不是整式反号）：臂7（`<0.5`，0.75）vs 臂8（`>0.5`，0.57）——S 差 **0.18 > 0.1**，TO 4.58% vs 4.98%、DD 13.72% vs 11.88%、LC/SC 133/128 vs 131/141 **逐项不同** ⇒ **非退化指纹**；结论仅到「掩码条件的方向有意义（低机构持股一侧更强）」，**不涉及 insd1 增持方向的正负**。
- **跨区符号不外推**：本档未引用 USA 文献符号，也未把 DEU 的 insiders 符号外推到 TWN/KOR；`risk72 残差为动量 / CEO 任期为正` 两处反转先例在本波无对应结构，不适用。

## §5 稀释铁律（乘法/bucket/壳层低于对应单腿 = 稀释）

- **乘法（臂3）：不触发**。S 0.89 > 左腿 0.81 > 右腿 0.78，F/sub/margin 同样高于两腿（§2.2/C1/C2）⇒ 这是**本族首个"复合高于单腿"**的形态；唯一让步是 2Y（0.92 < 1.08）。
- **减法（臂4）：触发且严重**，S 比被减腿低 0.97、DD 高 30.66pp、票池从 129-140 塌到 31-30；⚠ 但缺 `ts_ir` 单腿对照，**"稀释"的定量归因不成立，只能记"形态破坏"**。
- **bucket（臂9）：S 不稀释也不增益（+0.01），但 2Y −0.33** ⇒ 按"复合需高于单腿才值得留"的口径，**bucket 在强度维不划算**（其唯一卖点是 DD −2.80pp）。
- **掩码（臂7 vs 裸）：对 S/F/sub/margin 稀释、对 2Y 增益**（C5，两波复现）⇒ **不是强度杠杆**，与 DEU skill 既有口径「门控只修 prod/robust，不造强度」一致（`Claude/skills/wq-brain-ra-deu/references/insiders.md:52`）。
- **掩码 × 不同核心：损益依核心而异**（C5 −0.06 vs C9 −0.28）⇒ **不能把"掩码几乎中性"当成普遍结论**；它对时间距离类核是强负。

## §6 宽度塌缩 / CONCENTRATED_WEIGHT 单独登记（数据层 ≠ 信号死 ≠ 表达层）

| 臂 | LC/SC | CW（value vs limit） | 归因 |
|---|---|---|---|
| 臂4 `0mPeLNer` | **31/30**（本波唯一窄票池） | **0.285488 vs 0.1**（2014-02-19）挂 | **表达层**：减法两腿相消 + DD 44.56% → 票池塌到 61 只 |
| 臂1 `gJaR5gov` | 114/134（**健康，非塌缩**） | **0.168741 vs 0.1**（**2014-01-02，样本首日**）挂 | **首日建仓伪影**（小分母单日尖峰），与"宽度塌缩"是**两种不同形态**，不可合并登记 |
| 其余 8 臂 | 97–158 | pass | 无塌缩 |

- **本波 0 条 data_excluded**：8/10 臂 LC/SC 97–158、pnl 全为正（臂5 +0.83M … 臂3 +6.41M）、TO 4.10–12.29% 均在合理区间 ⇒ 数据存在且可交易。
- **臂4 的窄票池归表达层**（减法几何），**不得**登记成 `data_excluded`，也**不得**登记成信号死。
- **臂1 的 CW 挂点必须是"首日尖峰"口径**：它不是宽度问题（宽度 248 只），若下一波要提交/推进，应先确认该尖峰是否随 warm-up/分母护栏消失，**不能假设已修**。

## §7 塔位判读（点塔相关性）

平台 `get_alpha_details.pyramids` 逐臂实读（10/10）：

- **目标塔 INSIDERS 出现 10/10 臂**：
  - 单塔 5 条（`effective=1`）：臂1 `gJaR5gov`、臂2 `mLarN0x1`、臂3 `d5aE63Ew`、臂4 `0mPeLNer`、臂5 `j2a9JP9k` = `DEU/D1/INSIDERS`×1.6。
  - 双塔 5 条（`effective=2`）：臂6 `QP02ANn5`、臂7 `0mPeLNAr`、臂8 `akaA8QN5`、臂9 `1YWaRlJm`、臂10 `9qla3dJV` = `DEU/D1/INSTITUTIONS`×1.6 + `DEU/D1/INSIDERS`×1.6；`ra.pyramid_short` 同步为 `institutions/insiders`。
- **点位 ≠ 点亮**：10/10 臂 RA fail ≥3 ⇒ **本波实际点亮 INSIDERS 塔 0 颗、INSTITUTIONS 塔 0 颗**，塔计数不变（insiders 1/3、institutions 1/3，`CAMPAIGN_REPORT_20261116.md:34`）。
- **与 w1 的塔位对照**：两波都是"5 单塔 + 5 双塔"，但 **w2 的双塔件是单位干净的**（w1 双塔件 5/5 带 UNITS）⇒ 若后续要评估"双塔件是否值得做"，**w2 的 5 条是第一批可用的干净样本**（结论：S 0.50–0.82、sub 0.09–0.21，未见塔位带来的强度或 sub 优势）。

## §8 数据层判读（data_excluded 与信号死分开）

- **不 data_excluded**：见 §6（8/10 臂宽度 97–158、pnl 正、TO 正常）；`insiders1` 8 字段全 VECTOR、平台 `get_datafields` 实读 8/8（`FIELD_insiders1_20261116.md:23-40`）；本波 preflight `unknown_fields=[]`。
- **不判信号死**：本波 10 臂、**1 套配置**、**1 个窗口（66）**、**无翻符号对照**、**无掩码单独对照**、**无 ts_ir 单腿对照** ⇒ 六维 D1/D2/D6 未达（§9），按「探针不产生判死」与 AGENTS §7.6 **只能记 provisional**。
- **本波属"信号层弱 + 表达层坏（臂4/臂5）+ 配置层未扫"的混合，不是数据层排除**。

## §9 判死六维闸盘点（D1–D6；w1+w2 两波累计口径）

| 维 | 两波现状 | 判定 |
|---|---|---|
| **D1 结构互异模板 ≥10** | 两波 20 臂，互异机制约 **8–9**：holdings-Δ（w1，已判弱）/ 新鲜度（w2 臂1）/ 离散度（臂2）/ 集中度水平（w1 臂7）/ 乘法交互（臂3）/ 减法交互（臂4）/ 变化轴（臂5）/ 引擎掩码·口径 2 变体（臂6/7，LC/SC 逐位相同 ⇒ 计 1）/ 分支翻转（臂8）/ bucket 分组（臂9）/ 掩码×fresh（臂10）。按「换常数、同假设两向不算」口径 **<10** | **✗ 未达**（比 w1 的 6–8 有前进） |
| **D2 字段族自测** | 仍只用 `insd1_holdings`（vec_avg / days_from_last_change / ts_ir）与 `insd1_valueeur`（max/sum / stddev/sum）**2 个信号字段**；未碰 `insd1_shares` / `insd1_price` / `insd1_value` / `insd1_tradesignificance`（其中 value/price/significance 已有判死记录 S 1.14/1.13/1.21，属"有先验的未重测"，不是"未测即封禁"） | **✗ 未达** |
| **D3 矩全家（水平/一阶差/二阶波动/比值或信噪比 各≥1）** | 水平 ✓（w1 臂7 集中度水平、w2 臂1 fresh 水平）；一阶差 ✓（臂5，结果负）；二阶波动 ✓（臂2 `vec_stddev/vec_sum`）；比值 ✓（max/sum、stddev/sum）；信噪比 ✗（`ts_ir` 仅作被减腿、无单腿读数） | **✓ 达**（两波累计补齐；SNR 只有"被减腿"不算自测） |
| **D4 分组轴 ≥2** | sector ✓（臂1/2/w1 多数）、bucket(institutions 价值口径) ✓（臂9）；另有裸 rank（无分组）作对照 | **✓ 达** |
| **D5 非线性 ≥1** | `multiply` / `if_else` / `subtract` / `bucket` / `rank` / `group_rank` | **✓ 达** |
| **D6 配置 ≥2** | 两波**同一套**：DEU/TOP500/D1 + decay0 + SUBINDUSTRY + trunc0.08 + nanHandling ON；**decay 4 / nanHandling OFF 两波均未扫** | **✗ 未达** |

⇒ 缺 **D1 / D2 / D6**：**不得判死、不得封集、不得作为邻接数据集/族的先验**（AGENTS §7.6）。本波所有结论只在「decay0/nanON/SUBINDUSTRY/单一 66 窗」这一格内成立。

## §10 近闸候选（ask 口径：S≥1.2 或距任一硬闸 ≤0.4；≤2 条，按 S 降序）

按平台实读限值逐条核（S 闸 1.58 / F 1.0 / 2Y 1.58 / sub 本地 1.0 / CW 0.1 / TO 0.70 / margin 5bp）：

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `d5aE63Ew`（臂3） | **0.89** | **距 F 闸 0.37 ≤ 0.4**（F 0.63 vs limit 1.0）——本波唯一命中"实质硬闸"的臂；且 S/F/margin 三项均为本波最高（0.89/0.63/21.56bp），S 距闸 0.69、2Y 距闸 0.66、sub 距本地线 0.74；结构为乘法复合，已证高于两单腿 |
| 2 | `gJaR5gov`（臂1） | 0.78 | **距 CW 闸 0.069 ≤ 0.4**（CW 0.168741 vs limit 0.1，挂点 **2014-01-02 样本首日**）；但其余四闸距 0.49–0.82（F 0.49 / 2Y 0.50 / S 0.80 / sub 0.82）⇒ 其"近闸"**只来自一个可修的单日尖峰，不代表结构接近过关** |

- **排序外如实登记**：臂4 也命中 CW（0.285488 vs 0.1，超 0.186），但 S −0.16、2Y −0.53、DD 44.56%、票池 31/30 ⇒ 按 S 降序第 3 出局，且**明确不建议**把它当 near。
- **S≥1.2：无**（最高 0.89）。**距 S 闸最近 0.69**（臂3）、距 2Y 闸最近 0.47（臂6 的 1.11）、距本地 sub 线最近 0.56（臂2 的 0.44）。
- **与区域 near 池线的差异（如实登记）**：`tracking/DEU/config/thresholds.json` 的 `near.sharpe_min = 1.0` ⇒ 本波 **0 条**进区域 near 池；上表两条是按 **ask 的"距任一硬闸 ≤0.4"** 判据入选。两者口径不同，本档并列呈现，不混用。
- **推进顺序**：先测 `d5aE63Ew` 的 prod/self（它是全波最强且结构有新意）；`gJaR5gov` 只在其首日 CW 尖峰处理后再议。

## §11 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`（维持 w1，无终态转换）**。依据：

1. **单集上限继续成立**：BE176 判 `insiders1` 单集 S 上限 ≈1.30（`BE176_INSIDERS1_CEILING_130_20261112.md:23,28-30`）；两波合计 20 臂最强 0.89（臂3），**仍低于 1.30**，且离 1.58 差 0.69 ⇒ 既不破顶也不证伪。
2. **配对路线首次取得可判读读数**（w1 的 UNITS 缺口本波闭合）：`institutions6` 三种形态（价值掩码 / 股数掩码 / bucket）S 0.57–0.82、**sub 0.09–0.21**，全部达不到 ask 的 sub≥1.0 目标 ⇒ **INSTITUTIONS 作为第二腿不能把 sub 留在 ≥1.0**（这是干净的结论，不再是"不可判读"）；对照平台实读的 [INSIDERS,MODEL] 存量件 sub 1.49/1.51（`Vk6eodeb`/`qMWVeeME`）⇒ **第二腿的选择是 sub 的决定变量，MODEL 才是已验证的那条**（仅 DEU 同区实读；跨区禁外推；且这两条 MODEL 件并非 `insd1_*` 原生几何，见 w1 §2.4）。
3. **数据层无排除**：8/10 臂 LC/SC 97–158、pnl 正（§6）。
4. **六维 D1/D2/D6 未达**（§9）⇒ 按 AGENTS §7.6 不得终判死、不得封集。
5. **DB 侧一致**：`get_dead_datasets("DEU")` 返回 19 集，**不含 `insiders1`**（含 `insider_trx_matrix`，是不同数据集）。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90`：PASS=有臂过 RA 全闸 / PARTIAL=0 达标但 ≥1 近闸 / FAIL=0 达标 0 近闸；本波 `n_pass=0 / n_near=2`）。**未自造枚举值。**

- **稳健性**：该判定对 sub 口径不敏感（10/10 臂在平台动态 sub 限与本地 1.0 线下都挂 LOW_SHARPE+LOW_FITNESS）。
- **与 w1（FAIL）的差异必须说明**：w1 的"距闸 ≤0.4"命中项只有 TO 超限的 −0.11/−0.07 臂（负 Sharpe、DD 89–91%），故判 FAIL；本波的命中项是 **F 0.63 距 1.0 仅 0.37 的正 Sharpe 臂**（且 S/F/margin 全波最高）⇒ 判 PARTIAL。两波判据同一条，差异来自命中项的经济含义，**不是口径漂移**。
- **旁证：本波是全族两波里进步最明显的一波**——best S 0.81→0.89、best F 0.50→0.63、best margin 20.39→21.56bp、RA 最少挂数 3（臂2，与 w1 臂6 同）；但 best 2Y 1.17→1.11（略退）。

## §12 newLever 登记

**入册 1 条（跨波实证 + 裸/改造对照）**：

> **`insd1` 的"规模集中度 × 事件新鲜度"乘法交互（不是加法叠加）**：`multiply(rank(conc66), rank(fresh))` 在 decay0/nanON/SUBINDUSTRY/66 窗档下 S 0.89 / F 0.63 / sub 0.26 / margin 21.56bp，**高于两条对应单腿**（conc 单腿 w1 `oma3GYeb` 0.81/0.50/0.19/20.39bp，表达式逐字相同；fresh 单腿 w2 臂1 `gJaR5gov` 0.78/0.51/0.18/19.89bp）⇒ S +0.08~+0.11、F +0.12~+0.13、sub +0.07~+0.08、margin +1.17~+1.67bp。**这修正了 BE176 的"6 字段同源 ⇒ 任何叠加都平均化同源噪声"结论的适用边界**：该结论对**加法/等权叠加**成立，但**两个不同维度（规模集中 × 时间新鲜）的乘法交互不稀释、反而增益**。
> **适用条件与 caveat**：① 只在同档（decay0/nanON/SUBINDUSTRY）验证；② 2Y 反而低于 freshness 单腿（0.92 vs 1.08），若 2Y 是主缺口不适用；③ 仍低于 BE176 单集上限 1.30，**不改变"单集 ATOM 路线过不了 1.58"的路线结论**；④ 单点对照，未做配置/时间稳健性；⑤ 复合与 fresh 单腿的比较含 `group_rank(sector)→rank` 一处混淆（conc 侧是纯单变量）。

**未入册（如实登记，避免把复现当新杠杆）**：
- "institutions 掩码以 S/F/sub 换 2Y"（C5/C7，两波复现）——方向与既有口径「门控只修 prod/robust，不造强度」重复（`insiders.md:52`），且从未把任一候选推到 2Y≥1.58（两波最高 1.17/1.11），**不算新杠杆**。
- "价值口径 = 股数口径"（C6，LC/SC 逐位相同）——是**排除性结论**（省臂位），不是杠杆。
- "变化轴死"（C3）、"减法破坏"（C4）、"bucket 不增 S"（C8）——均为**负结论**，按口径不入册。

## §13 证据通道与盲区

**本轮实跑的核验（全部只读，零写入生产库）**：
- `mcp__wq-brain-http__batch_get_alpha_metrics(10 ids)`：10/10 success，S/F/2Y/sub/TO/margin/DD/`failed_ra_count` 与 ask 转录**逐值一致**。
- `mcp__wq-brain-http__get_alpha_details`：**逐臂 10/10** 取回 `settings`（decay0/nanON/SUBINDUSTRY/trunc0.08/2014-01-01→2023-12-31，10/10 一致）、`metrics`（含 longCount/shortCount）、`ra.ra_failed_checks`、`checks.fail`（含 limit 与 CW 的 date）、`checks.warning`（**5 条配对臂均无 UNITS**，仅 CLUSTER_TEST/MATCHES_*）、`pyramids.list`（含 multiplier/effective）、`code`。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w2)`：10 条，表达式与 `logs/_tmp_rt-insiders-w2_arms.json` **逐条同序**；`atom_flag` = 5 atom(1 集) + 5 combined(2 集)，`atom_n_datasets` 同步。
- 跨波对照件读数取自 w1 已入库档（`WAVE_rt-insiders-w1_20261116.md` §1，源为平台 `get_alpha_details`）与 `oma3GYeb` 的平台实读；**本档未重跑 w1 臂**。

**盲区（如实登记，不猜不补）**：
1. **符号指纹未测**：0 条翻符号臂，严格判据无法执行（§4）；连续两波缺该对照臂。
2. **掩码单独对照仍缺**：无 `if_else(cond, 1, 0.5)` 类臂 ⇒ 掩码效应与核贡献的分离仍不彻底（w1 已登记，本波未补）。
3. **`ts_ir` 单腿对照缺失**：臂4 的减法无法定量归因（§2.3）。
4. **窗口梯未扫**：全波只用 66（与 252 归一）；ask 的「22→66→132 单峰」衰减梯判据**本波不适用/未测**。
5. **配置只 1 套**：decay4/nanOFF 区域生产档两波均未跑 ⇒ **配置层死/活未判**。
6. **prod / self 全部 null**：按分工归相关性员，本档不测、不猜。
7. **年度分年未取**：本波未跑 `get_alpha_yearly_stats`；ask 称 `XgaGb3J1` / `d5a2aO7v` 已核十年（逐 pnl>0、LC99-198/SC105-199）——二者**不在本波 10 臂内**，本档仅转录，**未复跑**。
8. **臂1 的 CW 首日尖峰成因未验**：只知挂点为 2014-01-02、value 0.168741，**未验证**是否随 warm-up/分母护栏消失。
9. **`[INSIDERS,MODEL]` 的 sub 1.49/1.51 来自非 `insd1_*` 原生几何**（五腿 add + `significant_value_1` + MODEL 预估字段），**不能直接当作 `insd1_*` + MODEL 的可复现配方**。

## §14 终态

- **波**：`PARTIAL`（0 达标 / 2 近闸，n_pass=0 / n_near=2）；best S **0.89**（`d5aE63Ew` 臂3）/ best F **0.63**（同）/ best 2Y **1.11**（`QP02ANn5` 臂6）/ best sub **0.44**（`mLarN0x1` 臂2）/ 最低 DD 11.10%（`1YWaRlJm` 臂9）/ best margin 21.56bp（臂3）。
- **数据集**：`insiders1` = **provisional**（维持 w1；不判死、不 data_excluded、不封集）。单集 ATOM 路线仍受 BE176 的 1.30 上限约束（两波最强 0.89）；配对路线首次可判读 ⇒ **INSTITUTIONS 作第二腿 sub 只有 0.09–0.21，未达 ≥1.0**。
- **塔位**：INSIDERS 10/10 臂归属（5 单塔 + 5 双塔），**实际点亮 0**。
- **提交链**：**未推进**（0 达标；prod/self 未测）。
- **下一步（按优先级）**：
  1. **先测 `d5aE63Ew` 的 prod/self**（全波最强、结构有新意且已证高于两单腿）；
  2. **把"乘法交互"做成单变量族**：固定 conc 腿，只换第二维（鲜度/离散度/规模），验证 +0.08 是否稳定；同时补 `group_rank→rank` 的混淆拆解；
  3. **补 `ts_ir` 单腿与"掩码单独"两个对照**——这是 w1/w2 连续两波的空缺，不补则减法与掩码的归因永远不闭环；
  4. **若要保 sub，换第二腿**：`institutions6` 三种形态均只到 0.09–0.21；平台已验证能保 sub 的是 MODEL（1.49/1.51），但需先确认 `insd1_*` 原生几何 + MODEL 是否可复现，以及「已点亮塔不选」口径是否允许 MODEL 作搭档腿（**需用户裁定**）；
  5. **补第二套配置**（decay 4 / nanHandling OFF）——两波都是同一探针档，配置层结论为空；
  6. **不要再扫**：单集 66 窗的 holdings-Δ（两波 10 臂均弱）、集中度的一阶差（0.19，已干净证伪）、institutions 的价值/股数口径（等价）。
