# WAVE rt-insiders-w3 — `insiders1` 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集：`insiders1`（目标塔 **INSIDERS**）；配对集：`institutions6`（塔 INSTITUTIONS）
- 配置（平台 `get_alpha_details` 逐臂回显，10/10 一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、maxPosition=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR、simulationMode=FULL；`startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:5-16`（decay=4、nanHandling=OFF、2013-01-01 起）不同 ⇒ **第三波仍是探针口径（decay0/nanON）**。**本波结论只在 decay0/nanON/SUBINDUSTRY/单一 66+252 窗这一格内成立**。
- 派发/收割（收割说明转录，本档未重跑派发）：`preflight_expressions` valid=true / unknown_fields=[] / any_changed=false（10/10；`insd1_shares` 已显式聚合、未触发 `vec_*` 自动包裹）；`operator_audit` safe=true / violations=[]；精确式查重全仓 0 历史命中（仅本波输入件 `logs/_tmp_rt-insiders-w3_arms.json`、`logs/_tmp_rt_insiders_w3_arms.txt`）；与 w1/w2 已入库 20 条逐条不同。
  - 派发：`create_multi_simulation` 单波 10 臂 → multisim `2iMbL6g0l5et94o1dclIG3nj`；轮询第 1/2 次 children=0，第 3 次（约 4 分钟）10/10 all_terminal=true、**errors=0（全 COMPLETE，无 WARNING / CANCELLED / UNITS）**；`harvest_multisim_alphas` 首试成功（未走 404 兜底），total=10/complete=10/error_count=0；逐臂用平台 `code` 核对归属，10 条与臂表/提交顺序逐条一致（臂1→`2r5v12Kb` … 臂10→`Jj8nV2OE`）。
  - 落库：`upsert_backtest_rows(DEU, rt-insiders-w3, insiders1, 10)` → n=10；写后核验 10 条 `alpha_id/sharpe/fitness/margin/turnover` 与平台逐条一致。
- 判读基准（ask 给定，本档另附平台实读限值见 §1.1）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0 / 0.01≤TO≤0.70 / margin≥0.0005 / CW≤0.5 / self 与 prod 各<0.70。
- 闸种：**6 条 atom 单集件走 `LOW_2Y_SHARPE`（limit 1.58）；4 条 combined 双集件走 `IS_LADDER_SHARPE`（year=2，limit 1.58）**；`two_year_sharpe` 与 RA 载体逐臂一致（10/10）。
- 本波换的是**字段口径 + 壳**：`insd1_shares`（股数，w1 用 holdings、w2 用 valueeur）+ `ts_rank(...,252)` / `ts_ir(...,252)` 长窗壳 + `vec_count` 事件口径 + `trade_when`。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

指标经 `batch_get_alpha_metrics`（10/10 success）与 `get_alpha_details`（10/10）逐臂复核，与 ask 转录**逐值一致**。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔（pyramids/list） | RA fail（平台 `ra.ra_failed_checks`） |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|
| 1 | `2r5v12Kb` | **集中度单腿（shares）**：`ts_rank(ts_sum(max÷sum,66),252)` | 0.17 | 0.04 | −0.23 | 0.00 | 7.27% | 12.22% | 2.08bp | 139/154 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.08), LOW_2Y |
| 2 | `O0Wn129p` | **新鲜度单腿（vec_count）**：`ts_rank(252−dfc(bf(vec_count,252)),252)` | 0.27 | 0.08 | 0.09 | 0.02 | 9.31% | **8.61%** | 2.56bp | 143/148 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.13), LOW_2Y |
| 3 | `RReNJvre` | **集中度信噪比**：`group_rank(ts_ir(ts_sum(max÷sum,66),252), subindustry)` | **0.78** | **0.43** | **0.93** | 0.10 | **1.94%** | 8.63% | **39.61bp** | 130/153 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.37), LOW_2Y |
| 4 | `KPgnK2L1` | **trade_when 事件门控**：`trade_when(dfc(bf(vec_count))<66, ts_rank(conc,252), −1)` | −0.23 | −0.07 | −0.76 | −0.36 | 6.64% | **26.56%** | −3.41bp | 136/128 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(−0.11), LOW_2Y |
| 5 | `MP6bj2po` | **乘法（H2 预注册）**：`multiply(ts_rank(conc,252), rank(1/(dfc(vec_count)+1)))` | 0.55 | 0.26 | 0.58 | 0.14 | 9.14% | 11.88% | 6.05bp | 130/168 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.26), LOW_2Y |
| 6 | `blaNYKLN` | **加权（低带）**：`multiply(ts_rank(conc,252), 1−group_rank(inst_ratio,subindustry))` | −0.22 | −0.07 | −0.63 | −0.12 | 4.15% | 21.66% | −5.37bp | 137/162 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(−0.10), IS_LADDER |
| 7 | `qM7nKwAA` | **加权（高带）**：`multiply(ts_rank(conc,252), group_rank(inst_ratio,subindustry))` | 0.33 | 0.12 | 0.39 | 0.15 | 4.81% | 12.15% | 7.20bp | 134/165 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.16), IS_LADDER |
| 8 | `vRA5KoLr` | **掩码（低带）**：`if_else(rank(bf(inst_ratio,252))<0.5, ts_rank(conc,252), 0.5)` | 0.27 | 0.10 | 0.44 | −0.02 | 6.20% | 17.90% | 5.05bp | 116/123 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.13), IS_LADDER |
| 9 | `VkNXvRpb` | **掩码（高带）**：同臂8，比较方向翻 `>0.5` | −0.01 | −0.00 | −0.68 | 0.04 | 7.77% | 13.70% | −0.10bp | 126/138 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | **3**：LOW_SHARPE, LOW_FITNESS, IS_LADDER（sub 过闸） |
| 10 | `Jj8nV2OE` | **离散度单腿（shares）**：`ts_rank(ts_sum(stddev÷sum,66),252)` | 0.44 | 0.18 | 0.56 | **0.47** | 6.08% | 14.40% | 6.72bp | 129/152 | DEU/D1/INSIDERS×1.6（eff 1） | **3**：LOW_SHARPE, LOW_FITNESS, LOW_2Y（**sub 过闸**） |

- `conc` = `ts_sum(divide(vec_max(insd1_shares), vec_sum(insd1_shares)), 66)`；`dfc` = `days_from_last_change`；`bf` = `ts_backfill`；`inst_ratio` = `divide(aggregate_share_count_institutions, aggregate_share_count_all_owners)`。
- **本波极值**：best S **0.78**（臂3）/ best F **0.43**（臂3）/ best 2Y **0.93**（臂3）/ best sub **0.47**（臂10，本波唯一 sub 双过闸之一）/ **最低 TO 1.94%**（臂3）/ **最高 margin 39.61bp**（臂3）/ 最低 DD **8.61%**（臂2）与 8.63%（臂3）。
- **0 达标**：10/10 臂 `failed_ra_count` ≥3（4/4/4/4/4/4/4/4/3/3），**无一条 RA 全闸**；`status` 10/10 = `UNSUBMITTED`（提交态），仿真态全 COMPLETE、errors=0。
- **CW 10/10 全 pass**（无一条 CW 在 fail 名单）、**LC/SC 116–168 全宽**（无宽度塌缩）。

### 1.1 平台闸限实读（补齐 ask 的「平台 LOW_SHARPE limit 未读到」）

| 闸 | 平台实读 limit | 与 ask 基准的关系 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10 臂） | 与内部严线一致 |
| LOW_FITNESS | **1.0** | 一致 |
| HIGH_TURNOVER / LOW_TURNOVER | **0.70 / 0.01**（10/10 pass，最高 TO 9.31%、最低 1.94%） | 一致 |
| CONCENTRATED_WEIGHT | 本波 10/10 **pass**（无 value 回显） | 本波无 CW 事件 |
| LOW_2Y_SHARPE / IS_LADDER_SHARPE | **1.58**（year=2） | 一致 |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂不同**：臂4 −0.11 / 臂6 −0.10 / 臂1 0.08 / 臂2 0.13 / 臂8 0.13 / 臂7 0.16 / 臂5 0.26 / 臂3 0.37；臂9/臂10 判 PASS | ⚠ **sub≥1.0 是本地 review 线，不是平台闸限**（`thresholds.json:21`）；平台限只有 −0.11…0.37 |

⇒ ask 的「平台 LOW_SHARPE limit 本轮未读到」**本轮已实读补齐 = 1.58**；且 **verdict 与 sub 口径无关**——任何 sub 判据下 10/10 臂仍全部挂 LOW_SHARPE + LOW_FITNESS（S≤0.78 vs 1.58、F≤0.43 vs 1.0）。

## §2 逐臂归因条目

### 2.1 集中度 / 离散度的**同壳干净消融**（臂1 vs 臂10）——本波最干净的一条对照

1. **臂1 `2r5v12Kb`（集中度单腿，shares 口径）**：S 0.17 / F 0.04 / 2Y −0.23 / sub 0.00 / TO 7.27% / DD 12.22% / margin 2.08bp / LC-SC 139/154；RA 4 挂。
2. **臂10 `Jj8nV2OE`（离散度单腿，同口径同壳）**：S 0.44 / F 0.18 / 2Y 0.56 / sub **0.47** / TO 6.08% / DD 14.40% / margin 6.72bp / LC-SC 129/152；RA 仅 3 挂（sub 过闸）。
   - **两臂表达式只差一个 token：`vec_max` → `vec_stddev`**（其余 `ts_sum(divide(·, vec_sum(insd1_shares)), 66)` 与 `ts_rank(·, 252)` 逐字相同）⇒ 这是**三波里最干净的单变量消融**。
   - Δ：S **+0.27** / F +0.14 / 2Y **+0.79** / sub **+0.47** / TO −1.19pp / margin +4.64bp；唯 DD **+2.18pp**。
   - ⇒ **「单笔金额的离散度」全面优于「最大单笔占比」**，且这正是 w2 已登记为 sprout 的方向（w2 臂2 stddev 的 sub 0.44 vs w1 掩码臂 max 的 sub 0.19）。**两波、两次独立对照、同向** ⇒ 升格为杠杆（§12）。
   - ⚠ 但同时看到：**shares 口径的集中度（臂1，0.17）远弱于 valueeur 口径（w1 臂7，0.81）**——同一个 `max÷sum` 统计量换字段后 S 掉 0.64。所以"离散度更好"这条不能理解成"shares 口径可用"：**shares 口径的整个族都弱**（臂1 0.17、臂5 0.55、臂8 0.27、臂7 0.33），本波最强臂 0.78 仍是集中在"集中度信噪比"这一特殊壳上。

### 2.2 集中度的信噪比壳（臂3）——本波最强、且是**三波里效率最高**的臂

3. **臂3 `RReNJvre`（`group_rank(ts_ir(ts_sum(max÷sum,66), 252), subindustry)`）**：S **0.78** / F **0.43** / 2Y **0.93** / sub 0.10 / **TO 1.94%（三波最低）** / DD **8.63%** / **margin 39.61bp（三波最高，是 w2 最高值 21.56bp 的 1.84 倍）** / LC-SC 130/153；RA 4 挂（S/F/sub/2Y），CW/TO/margin pass。
   - **vs 臂1（同核 `ts_rank` 壳）**：S **+0.61** / F +0.39 / 2Y +1.16 / sub +0.10 / TO **−5.33pp** / DD −3.59pp / margin **+37.53bp**。
   - ⚠ **但这不是单变量**：臂3 与臂1 差**两处**——(i) `ts_ir(·,252)` vs `ts_rank(·,252)`；(ii) 多了 `group_rank(·, subindustry)`。按 w1/w2 的既有对照（sector 分组 ≈ 零增益：w1 臂7 vs 臂5 S −0.03；w2 bucket 分组 S +0.01），分组项的历史效应量 ≤0.1，故 **+0.61 主要来自 `ts_ir` 壳**（推断，本波未直接验证）。
   - ⇒ 机制判读：`ts_ir`（252 日均值÷标准差）把信号**变慢**，于是 TO 从 7.27% 压到 1.94%、margin 从 2.08bp 抬到 39.61bp，而 S 同时上升——**不是"用收益换低换手"，而是低换手与高 S 同时出现**。对 submit 链条意义大（低 TO ⇒ 低交易成本、低 self-corr 风险），是本波最值得保留的结构。

### 2.3 trade_when 事件门控（臂4）——负杠杆

4. **臂4 `KPgnK2L1`（`trade_when(dfc(bf(vec_count,252)) < 66, ts_rank(conc,252), −1)`）**：S **−0.23** / F −0.07 / 2Y −0.76 / sub −0.36 / TO 6.64% / DD **26.56%（三波最高）** / margin −3.41bp / LC-SC 136/128；RA 4 挂。
   - **vs 臂1（同核，门控内层表达式逐字相同）**：S **−0.40** / F −0.11 / 2Y −0.53 / sub **−0.36** / DD **+14.34pp** / margin **−5.49bp**。
   - ⇒ **`trade_when(…, −1)` 在本波是破坏性的**：门控失败即全额做空（−1）会制造长期空头偏置与来回摆动，DD 翻倍、S 转负。FIELD 档 M9 原评"B：DEU 未测 trade_when"（`FIELD_insiders1_20261116.md:249`），**本波实测为负**，该先验由"未测"改为"实测负"。

### 2.4 H2 预注册：乘法（臂5）——**复现 w2 的"复合高于单腿"，且效应量更大**

5. **臂5 `MP6bj2po`（`multiply(ts_rank(conc,252), rank(1/(dfc(vec_count)+1)))`）**：S 0.55 / F 0.26 / 2Y 0.58 / sub 0.14 / TO 9.14% / DD 11.88% / margin 6.05bp / LC-SC 130/168；RA 4 挂。
   - **vs 左腿（臂1，子表达式逐字相同）**：S **+0.38** / F **+0.22** / 2Y **+0.81** / sub **+0.14** / margin **+3.97bp** / DD −0.34pp / TO +1.87pp ⇒ **干净单变量**，复合显著高于左腿。
   - **vs 右腿（臂2，⚠ 不同新鲜度实现）**：S +0.28 / F +0.18 / 2Y +0.49 / sub +0.12。⚠ 臂2 的新鲜度是 `ts_rank(252−dfc(ts_backfill(vec_count,252)),252)`，臂5 的右因子是 `rank(1/(dfc(vec_count)+1))`（**无 252 回填、取倒数、裸 rank**）⇒ 两处不同，**此项只作参考、不作单变量归因**。
   - ⇒ **这是 w2 已入册杠杆（规模集中度 × 事件新鲜度 乘法交互）的第二次独立验证**，且这次换到 shares 口径 + `vec_count` 事件代理，增益从 w2 的 +0.08~+0.11 放大到 +0.38（左腿对照为纯单变量）。**杠杆的跨波稳健性因此显著增强**；本波不再重复入册，只在 §12 记"复现确认"。

### 2.5 H5 加权 vs H4 掩码：**方向互相反号**——本波最重要的认知修正

6. **臂6 `blaNYKLN`（加权低带：`multiply(ts_rank(conc,252), 1−group_rank(inst_ratio,subindustry))`）**：S **−0.22** / F −0.07 / 2Y −0.63 / sub −0.12 / TO 4.15% / DD 21.66% / margin −5.37bp / LC-SC 137/162；RA 4 挂。
7. **臂7 `qM7nKwAA`（加权高带：`multiply(ts_rank(conc,252), group_rank(inst_ratio,subindustry))`）**：S **0.33** / F 0.12 / 2Y 0.39 / sub 0.15 / TO 4.81% / DD 12.15% / margin 7.20bp / LC-SC 134/165；RA 4 挂。
8. **臂8 `vRA5KoLr`（掩码低带 `<0.5`）**：S **0.27** / F 0.10 / 2Y 0.44 / sub −0.02 / TO 6.20% / DD 17.90% / margin 5.05bp / LC-SC 116/123；RA 4 挂。
9. **臂9 `VkNXvRpb`（掩码高带 `>0.5`）**：S **−0.01** / F −0.00 / 2Y −0.68 / sub 0.04 / TO 7.77% / DD 13.70% / margin −0.10bp / LC-SC 126/138；RA 仅 3 挂（sub 过闸）。

**两条对照读出相反方向**：
- **加权形态**：低带 −0.22 vs 高带 0.33 ⇒ **高带强 0.55**；
- **掩码形态**：低带 0.27 vs 高带 −0.01 ⇒ **低带强 0.28**。

**为什么这不矛盾、而且可以定量拆开**：臂6 与臂7 是**互补权重**——`multiply(x, 1−g)` 与 `multiply(x, g)`（`g = group_rank(inst_ratio, subindustry) ∈ [0,1]`）逐元素相加**恰好等于裸腿 x**（= 臂1 的 `ts_rank(conc,252)`）。
⇒ 代数上 `臂6 = 臂1 − 臂7`。而读数：裸腿 **0.17**、高带半 **0.33**、低带半 **−0.22** ⇒ **集中度的预测力集中在"机构持股高"的一侧**，低持股侧是负的。
⇒ 由此得到本波最重要的一条认知修正：**w2 记的「低机构持股是强侧」只在 `if_else` 掩码形态内成立**（w2：0.75 vs 0.57，Δ0.18；w3：0.27 vs −0.01，Δ0.28，两波掩码形态方向一致），**而互补权重分解给出相反答案**。两者不可能同时是"经济方向"，因此**掩码形态的"低带强"不能归因于 insiders 核**——它更可能来自 `if_else(…, 0.5)` 那条常数腿（常数在 SUBINDUSTRY 中性化后被部分抵消，但与信号腿的混合会额外注入一个"低机构持股"方向的横截面倾斜）。
⇒ **纪律结论**：① 任何"低/高机构持股是强侧"的表述**必须带形态限定**（掩码 or 加权），不能裸说；② w2 档登记的那条只能降级为"形态内观察"，**不得**作为经济结论外推；③ 这也间接证实 w1/w2 连续登记的"缺掩码单独对照"缺口**是真实有害的**——两种形态给出反号，说明掩码里的方向读数是构造产物。

### 2.6 新鲜度（臂2）

10. **臂2 `O0Wn129p`（`ts_rank(252 − dfc(ts_backfill(vec_count(insd1_shares),252)), 252)`）**：S 0.27 / F 0.08 / 2Y 0.09 / sub 0.02 / TO **9.31%（本波最高）** / DD **8.61%（三波最低）** / margin 2.56bp / LC-SC 143/148；RA 4 挂。
    - **vs w2 的新鲜度单腿（`group_rank(1/(dfc(vec_avg(holdings))+1), sector)`，S 0.78 / 2Y 1.08）**：S **−0.51** / 2Y −0.99。⚠ 两处不同：**事件代理**（`vec_count(shares)` vs `vec_avg(holdings)`）与**壳**（`ts_rank(252−…,252)` vs `1/(dfc+1)` 再 group_rank）⇒ 非单变量，**不能据此说"新鲜度机制换 shares 就失效"**。
    - 本波新鲜度的唯一确定贡献是 **DD 8.61%（三波最低）**——`ts_rank(…,252)` 的长窗把回撤压得最低，但 S/2Y 也随之压低。

## §3 对照实验汇总（裸 vs 改造，同配置同日期）

| # | 对照 | 改造件 | 裸件 | Δ（S/F/2Y/sub） | 判定 |
|---|---|---|---|---|---|
| C1 | 离散度 vs 集中度（**单 token**：`vec_max`→`vec_stddev`） | 臂10 `0.44/0.18/0.56/0.47` | 臂1 `0.17/0.04/−0.23/0.00` | **+0.27/+0.14/+0.79/+0.47** | **离散度全面更优**（仅 DD +2.18pp） |
| C2 | ts_ir 壳 vs ts_rank 壳 | 臂3 `0.78/0.43/0.93/0.10` | 臂1 `0.17/0.04/−0.23/0.00` | **+0.61/+0.39/+1.16/+0.10**（TO −5.33pp、margin +37.53bp） | 强增益；⚠ 含 `group_rank(subindustry)` 一处混淆 |
| C3 | trade_when 门控 vs 无门控 | 臂4 `−0.23/−0.07/−0.76/−0.36` | 臂1 `0.17/0.04/−0.23/0.00` | **−0.40/−0.11/−0.53/−0.36**（DD +14.34pp） | **负杠杆** |
| C4 | 乘法 vs 左腿（**纯单变量**） | 臂5 `0.55/0.26/0.58/0.14` | 臂1 `0.17/0.04/−0.23/0.00` | **+0.38/+0.22/+0.81/+0.14** | **增益**（复现 w2） |
| C5 | 乘法 vs 右腿（⚠ 新鲜度实现不同） | 臂5 同上 | 臂2 `0.27/0.08/0.09/0.02` | +0.28/+0.18/+0.49/+0.12 | 参考，不作单变量 |
| C6 | 加权高带 vs 低带（**互补权重**） | 臂7 `0.33/0.12/0.39/0.15` | 臂6 `−0.22/−0.07/−0.63/−0.12` | **+0.55/+0.19/+1.02/+0.27** | **高带强侧**（与 C7 反号） |
| C7 | 掩码高带 vs 低带 | 臂9 `−0.01/−0.00/−0.68/0.04` | 臂8 `0.27/0.10/0.44/−0.02` | **−0.28/−0.10/−1.12/+0.06** | **低带强侧**（与 C6 反号） |
| C8 | 掩码 vs 裸（低带） | 臂8 `0.27/0.10/0.44/−0.02` | 臂1 `0.17/0.04/−0.23/0.00` | +0.10/+0.06/+0.67/−0.02 | 小幅正（与 w2 的 −0.06 不同向，见 §4） |

**跨波对照（同一判据在不同波上的符号）**：

| 判据 | w1 | w2 | w3 | 跨波结论 |
|---|---|---|---|---|
| 掩码低带 vs 高带 | +0.21（0.74 vs 0.53） | +0.18（0.75 vs 0.57） | +0.28（0.27 vs −0.01） | **掩码形态三波一致：低带强** |
| 加权（互补权重）低带 vs 高带 | — | — | **−0.55**（−0.22 vs 0.33） | 与掩码**反号**；代数上 臂6+臂7=裸腿 ⇒ 信号在高带侧 |
| 乘法复合 vs 左腿 | — | +0.08 | **+0.38** | **两波一致为正**（w2 已入册） |
| 离散度 vs 集中度 | — | +0.25（sub，跨波不同壳） | **+0.27（S，单 token）** | **两波一致：离散度更优** |

## §4 符号指纹 / 方向

- **严格符号指纹仍未测**：10 条表达式**无整式取反**（`logs/_tmp_rt-insiders-w3_arms.json` 全文无前置负号 / `multiply(-1,…)`）。ask 的判据（S(−expr)≈−S(expr) 且差<0.03 且 TO/DD/longCount 逐位相同）**无法执行**，如实记「未测」；FIELD 档 §5 要求的"增持语义必须同波带反号对照臂"**连续三波未带**。
- **本波有一条比"伪反号对照"更强的对照**：**互补权重对**（臂6/臂7），因为 `multiply(x,1−g) + multiply(x,g) ≡ x`。它不是反号，但能**把裸腿按机构持股轴精确二分**，因此方向归因比反号对照更干净：
  - 裸腿 x（臂1）S 0.17 → 高带半（臂7）**0.33** / 低带半（臂6）**−0.22** ⇒ **x 的正向预测力集中在机构持股高的一侧**。
- **形态敏感性（必须写进判读）**：掩码形态三波都是"低带强"（+0.21/+0.18/+0.28），加权形态本波是"高带强"（+0.55）⇒ **"低/高机构持股"不是稳定的经济方向，而是组合形态的产物**。任何后续引用必须写明形态。
- **跨区符号不外推**：本档未引用 USA 文献符号，也未把 DEU 的 insiders 符号外推到 TWN/KOR。

## §5 稀释铁律（乘法/bucket/壳层低于对应单腿 = 稀释）

- **乘法（臂5）：不触发**（C4：S +0.38 / F +0.22 / 2Y +0.81 / sub +0.14 全部高于左腿）⇒ 与 w2 同向，**复合增益在两波、两种字段口径上复现**。
- **加权（臂6/臂7）：不是稀释问题而是"方向拆分"问题**（§2.5）——单一"加权 vs 裸"的稀释判定在这里没有意义，因为两半相加等于裸腿；正确做法是读**两侧各自的正负**。
- **掩码（臂8 vs 臂1）：小幅正（S +0.10）**，与 w2 的 −0.06 不同向 ⇒ **掩码对 S 的效应不稳定（−0.06~+0.10），跨波不可作杠杆**。
- **trade_when（臂4）：强稀释/破坏**（S −0.40、DD +14.34pp、sub −0.36）。
- **ts_ir 壳（臂3）：不是稀释，是增益**（+0.61，但含分组混淆）。

## §6 宽度 / CW 登记（数据层 ≠ 信号死 ≠ 表达层）

- **本波 0 条宽度塌缩、0 条 CW 挂闸**：LC/SC 116–168 全宽（最低 臂8 116/123），CW 10/10 pass。
- **本波 0 条 data_excluded**：10/10 臂 pnl 有值（臂4/臂6/臂9 为负但非零，−41,347 ~ −1,167,800），TO 1.94–9.31% 全在区间内，无「字段无数据」证据。
- **臂4 的高 DD（26.56%）属表达层**（trade_when 的 −1 空头偏置），**不得**登记成数据层或信号死。

## §7 塔位判读（点塔相关性）

平台 `get_alpha_details.pyramids` 逐臂实读（10/10）：

- **目标塔 INSIDERS 出现 10/10 臂**：
  - 单塔 6 条（`effective=1`）：臂1 `2r5v12Kb`、臂2 `O0Wn129p`、臂3 `RReNJvre`、臂4 `KPgnK2L1`、臂5 `MP6bj2po`、臂10 `Jj8nV2OE` = `DEU/D1/INSIDERS`×1.6。
  - 双塔 4 条（`effective=2`）：臂6 `blaNYKLN`、臂7 `qM7nKwAA`、臂8 `vRA5KoLr`、臂9 `VkNXvRpb` = `DEU/D1/INSTITUTIONS`×1.6 + `DEU/D1/INSIDERS`×1.6；`ra.pyramid_short` 同步为 `institutions/insiders`。
- **点位 ≠ 点亮**：10/10 臂 RA fail ≥3 ⇒ **本波实际点亮 INSIDERS 塔 0 颗、INSTITUTIONS 塔 0 颗**，塔计数不变（insiders 1/3、institutions 1/3，`CAMPAIGN_REPORT_20261116.md:34`）。
- **三波塔位结构对照**：w1 5 单 + 5 双（双塔件全带 UNITS）、w2 5 单 + 5 双（全干净）、w3 **6 单 + 4 双**。三波双塔件的 S/F/sub 都未超过同波最好的单塔件（w3 双塔最好 0.33 vs 单塔最好 0.78）⇒ **institutions 双塔在本族三波无强度优势**。

## §8 数据层判读（data_excluded 与信号死分开）

- **不 data_excluded**：§6（10/10 臂 LC/SC 116–168、TO 正常、无 CW）；`insiders1` 8 字段全 VECTOR、平台 `get_datafields` 实读 8/8（`FIELD_insiders1_20261116.md:23-40`）；preflight `unknown_fields=[]`、`insd1_shares` 已证存。
- **不判信号死**：本波 10 臂、**1 套配置**、**1 组窗口（66+252）**、**无翻符号对照**、**无掩码单独对照** ⇒ 六维 D2/D6 未达（§9），按「探针不产生判死」与 AGENTS §7.6 **只能记 provisional**。
- **本波新增的两条负结论都是信号层/表达层**：`trade_when(−1)` 破坏性（表达层）、shares 口径的集中度弱（信号层）。**都不是数据层排除。**

## §9 判死六维闸盘点（D1–D6；w1+w2+w3 三波累计口径）

| 维 | 三波现状 | 判定 |
|---|---|---|
| **D1 结构互异模板 ≥10** | 三波累计约 **13–15** 个互异机制：holdings-Δ（w1）/ holdings-Δ z 化（w1）/ holdings 新鲜度（w2）/ valueeur 集中度（w1/w2）/ valueeur 离散度（w2）/ valueeur 乘新鲜度（w2）/ valueeur 减法（w2）/ institutions 掩码（w1/w2/w3）/ institutions bucket（w2）/ shares 集中度 ts_rank（w3）/ shares 集中度 ts_ir（w3）/ shares trade_when（w3）/ shares 互补加权（w3）/ shares 离散度（w3）/ vec_count 新鲜度（w3） | **✓ 达**（本波补齐） |
| **D2 字段族自测** | 已测 **3/6** 信号字段：`insd1_holdings`（w1/w2）、`insd1_valueeur`（w1/w2）、`insd1_shares`（w3）；**未测** `insd1_price` / `insd1_value` / `insd1_tradesignificance`（三者有族级判死先验 S 1.13/1.14/1.21，但按 AGENTS §7.6「禁止凭族先验封禁未测字段」**不能算已测**） | **✗ 未达** |
| **D3 矩全家（水平/一阶差/二阶波动/比值或信噪比 各≥1）** | 水平 ✓（w1 臂7、w2 臂1、w3 臂1/臂10）、一阶差 ✓（w2 臂5，负）、二阶波动 ✓（w2 臂2、w3 臂10 的 `vec_stddev÷vec_sum`）、比值 ✓（max÷sum、stddev÷sum）、**信噪比 ✓（w3 臂3 的 `ts_ir`）** | **✓ 达**（五类齐） |
| **D4 分组轴 ≥2** | sector ✓（w1/w2）、subindustry ✓（w3 臂3/6/7）、bucket(institutions) ✓（w2 臂9） | **✓ 达** |
| **D5 非线性 ≥1** | `multiply` / `if_else` / `trade_when` / `bucket` / `ts_rank` / `ts_ir` / `subtract` | **✓ 达** |
| **D6 配置 ≥2** | 三波**同一套**：DEU/TOP500/D1 + decay0 + SUBINDUSTRY + trunc0.08 + nanHandling ON；**decay 4 / nanHandling OFF 三波均未扫** | **✗ 未达** |

⇒ 只剩 **D2 / D6** 未达：**仍不得判死、不得封集、不得作为邻接数据集/族的先验**（AGENTS §7.6）。但要如实登记：**判死资格已从"缺 4 维"缩到"缺 2 维"**——若下一波补测 `price`/`value`/`tradesignificance` 三字段（各 ≥1 条）并跑第二套配置（decay4/nanOFF），六维即可齐备，届时才轮到 dataset 级终态裁决。

## §10 近闸候选（ask 口径：S≥1.2 或距任一硬闸 ≤0.4；≤2 条，按 S 降序）

**本波 0 条近闸候选。**

- **S≥1.2：无**（最高 0.78，臂3；距 S 闸 **0.80**）。
- **距 F 闸（1.0）≤0.4：无**（最高 F 0.43，臂3；距闸 **0.57**）。
- **距 2Y 闸（1.58）≤0.4：无**（最高 2Y 0.93，臂3；距闸 **0.65**）。
- **距本地 sub 线（1.0）≤0.4：无**（最高 sub 0.47，臂10；距线 **0.53**；且臂10 在平台侧 sub 判 PASS，本无缺口）。
- **TO / CW：10/10 全 pass**（TO 1.94–9.31% 全在 0.01–0.70；CW 无一条挂闸）⇒ 无缺口。
- ⚠ **唯一机械命中的是 margin**：臂1 2.08bp（缺 0.000292）、臂2 2.56bp（缺 0.000244）、臂4 −3.41bp（缺 0.000841）、臂6 −5.37bp（缺 0.001037）、臂9 −0.10bp（缺 0.00051）——按绝对差都在 0.4 内，但 **margin 闸的量纲是 0.0005（全区间约 0.005），"0.4"比该指标全区间大 80 倍，阈值在此闸上失去分辨力**。且这 5 条臂 S 全 ≤0.27、2Y 全负 ⇒ **明确不列入 near**（与 w1 排除"TO 超限但 S −0.11/DD 90%"的臂同一处置逻辑）。
- **区域 near 池线**（`tracking/DEU/config/thresholds.json` 的 `near.sharpe_min = 1.0`）：同样 **0 条**满足。

⇒ n_pass = 0，n_near = 0。

## §11 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`（维持 w1/w2，无终态转换）**。依据：

1. **单集 66 窗路线的天花板已被三次测量夹住**：BE176 判 `insiders1` 单集 S 上限 ≈1.30（三波 1.22/1.30/1.19，`BE176_INSIDERS1_CEILING_130_20261112.md:23,28-30`）；本族三波（w1/w2/w3）最强 0.81/0.89/0.78，**全部低于 1.30**，且**三波之间没有单调进步**（0.81→0.89→0.78）。⇒ 单集路线边际产出趋零，但**这仍不是判死证据**（D2/D6 未达，且每波换的是字段/壳，不是同一几何的重复）。
2. **配对路线（institutions6）三波皆为负或平**：掩码 S −0.06~+0.10、加权（高带）0.33、低带 −0.22；sub 全部 ≤0.21 ⇒ **institutions 作第二腿在 DEU 仍未把 sub 留在 ≥1.0**（对比平台实读的 [INSIDERS,MODEL] 存量件 sub 1.49/1.51，见 w1 §2.4 与 w2 §11）。
3. **数据层无排除**：LC/SC 116–168、CW 10/10 pass、TO 正常、pnl 有值。
4. **六维只剩 D2/D6 未达**（§9）⇒ 按 AGENTS §7.6 **不得终判死、不得封集**。
5. **DB 侧一致**：`get_dead_datasets("DEU")` 返回 19 集，**不含 `insiders1`**。

**波 verdict = `FAIL`**（判定表 `src/wqb/wave_results_contract.py:79-90`：PASS=有臂过 RA 全闸 / PARTIAL=0 达标但 ≥1 近闸 / FAIL=0 达标 0 近闸；本波 `n_pass=0 / n_near=0`）。**未自造枚举值。**

- **稳健性**：该判定对 sub 口径不敏感（10/10 臂在任何 sub 判据下仍挂 LOW_SHARPE+LOW_FITNESS）。
- **与 w2（PARTIAL）的差异**：w2 有一条臂（F 0.63）距 F 闸 0.37；本波最好 F 只有 0.43（距闸 0.57）⇒ 本波**确实更弱**，不是口径收紧。best S 也从 0.89 回落到 0.78。
- **与 w1（FAIL）一致**：两波的"近闸"都只剩量纲失效的机械命中（w1 是 TO、本波是 margin），均明确不计入。
- **本波的真实价值不在闸位，而在两条结构结论**：① 离散度 > 集中度（干净单 token 消融，+0.27 S / +0.47 sub）；② 机构持股轴上的方向是**形态产物**（互补权重给出与掩码相反的方向，且代数上 臂6+臂7=裸腿）。

## §12 newLever 登记

**入册 1 条（跨波实证 + 干净归因对照）**：

> **`insd1` 的单笔金额统计量：离散度（`vec_stddev ÷ vec_sum`）优于集中度（`vec_max ÷ vec_sum`）**。同字段、同壳（`ts_sum(·,66)` + `ts_rank(·,252)`）、**只差一个 token** 的消融：离散度 S 0.44 / F 0.18 / 2Y 0.56 / **sub 0.47** / margin 6.72bp vs 集中度 S 0.17 / F 0.04 / 2Y −0.23 / **sub 0.00** / margin 2.08bp ⇒ **S +0.27、F +0.14、2Y +0.79、sub +0.47、margin +4.64bp**（唯一代价 DD +2.18pp）。
> **跨波支撑**：w2 的 valueeur 口径上，离散度臂（`mLarN0x1`，sub 0.44）同样高于集中度臂（w1 `oma3GYeb`，sub 0.19）⇒ **两波、两种字段口径（shares / valueeur）、两次独立对照，方向一致**。
> **适用条件与 caveat**：① 只在 decay0/nanON/SUBINDUSTRY 档验证；② 只证明"同一族内离散度统计量优于集中度"，**不改变 shares 口径整体偏弱**的事实（本波 shares 集中度仅 0.17，valueeur 集中度 w1 是 0.81）；③ 离散度臂的 S 仍只有 0.44（距闸 1.14），**不构成可推进候选**；④ sub 是它的强项（0.47，三波非退化最高），若后续目标是 ★v2 的 sub≥1.0，本族应优先用离散度而不是集中度。

**复现确认（不算新入册，如实标注）**：
- **w2 已入册的"集中度 × 新鲜度乘法交互"本波复现**：臂5 对左腿（纯单变量）+0.38 S / +0.22 F / +0.81 2Y / +0.14 sub，且换到 shares 口径 + `vec_count` 事件代理仍成立 ⇒ 该杠杆的跨波稳健性由"两波同向"升到"两波、两字段、两事件代理同向"。

**未入册（负结论 / 不稳定 / 排除性）**：
- `trade_when(…, −1)` 事件门控：S −0.40、DD +14.34pp ⇒ **负杠杆**。
- 掩码对 S 的效应：w2 −0.06 / w3 +0.10 ⇒ **不稳定，不可入册**。
- "低机构持股是强侧"：**只在掩码形态成立**（三波同向），加权形态反号 ⇒ **降级为形态内观察，明确不入册为经济杠杆**（修正 w2 档的该条 sprout 表述）。
- "价值口径 = 股数口径"（w2 已记）、`bucket` 不增 S（w2 已记）：本波未重复，维持原结论。

## §13 证据通道与盲区

**本轮实跑的核验（全部只读，零写入生产库）**：
- `mcp__wq-brain-http__batch_get_alpha_metrics(10 ids)`：10/10 success，S/F/2Y/sub/TO/margin/DD/`failed_ra_count` 与 ask 转录**逐值一致**。
- `mcp__wq-brain-http__get_alpha_details`：**逐臂 10/10** 取回 `settings`（decay0/nanON/SUBINDUSTRY/trunc0.08/2014-01-01→2023-12-31，10/10 一致）、`metrics`（含 longCount/shortCount/returns）、`ra.ra_failed_checks`、`checks.fail`（含 limit）、`checks.warning`（**10/10 无 UNITS**，仅 CLUSTER_TEST/MATCHES_*）、`pyramids.list`（含 multiplier/effective）、`code`。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w3)`：10 条，表达式与 `logs/_tmp_rt-insiders-w3_arms.json` **逐条同序**；`atom_flag` = 6 atom + 4 combined(2 集)，与塔位一致。
- 跨波对照件读数取自 w1/w2 已入库档（`WAVE_rt-insiders-w1_20261116.md` §1、`WAVE_rt-insiders-w2_20261116.md` §1，源为平台 `get_alpha_details`）；**本档未重跑 w1/w2 臂**。

**盲区（如实登记，不猜不补）**：
1. **符号指纹未测**：0 条整式反号臂，严格判据无法执行（§4）；连续三波缺该对照臂。本波用**互补权重对**替代，它比反号对照更能拆分方向，但**不是** ask 指定的指纹形态。
2. **掩码单独对照仍缺**：本波通过互补权重**间接证明**该缺口有害（两种形态反号），但未跑 `if_else(cond, 1, 0.5)` 类纯掩码臂。
3. **臂3 的 +0.61 含分组混淆**：`ts_ir` 与 `group_rank(subindustry)` 两处同时变，分组效应量按历史 ≤0.1（推断）。
4. **臂5 vs 臂2 不是单变量**：两处新鲜度实现不同（§2.4），右腿对照只作参考。
5. **窗口梯未扫**：只用 66（时序聚合）+252（时序秩/信噪比）；ask 的「22→66→132 单峰」衰减梯判据**本波不适用/未测**。
6. **配置只 1 套**：decay4/nanOFF 区域生产档三波均未跑 ⇒ **配置层死/活未判**（D6）。
7. **prod / self 全部 null**：按分工归相关性员，本档不测、不猜。
8. **年度分年未取**：本波未跑 `get_alpha_yearly_stats`；ask 称 `XgaGb3J1` / `d5a2aO7v` 已核十年——二者**不在本波 10 臂内**，本档仅转录，**未复跑**。
9. **`vec_count` 事件口径的语义未验**：本波用 `vec_count(insd1_shares)` 作事件新鲜度代理（FIELD 档 §4.2 曾证 5 个字段的 `vec_count` 逐位相同），但**本波未单独复核该等价性**。

## §14 终态

- **波**：`FAIL`（0 达标 / 0 近闸，n_pass=0 / n_near=0）；best S **0.78**（`RReNJvre` 臂3）/ best F **0.43**（同）/ best 2Y **0.93**（同）/ best sub **0.47**（`Jj8nV2OE` 臂10）/ 最低 TO **1.94%**（臂3）/ 最高 margin **39.61bp**（臂3）/ 最低 DD **8.61%**（`O0Wn129p` 臂2）。
- **数据集**：`insiders1` = **provisional**（维持；不判死、不 data_excluded、不封集）。单集路线三波最强 0.78–0.89、无单调进步；配对路线（institutions6）三波皆负或平。
- **塔位**：INSIDERS 10/10 臂归属（6 单塔 + 4 双塔），**实际点亮 0**。
- **提交链**：**未推进**（0 达标；prod/self 未测）。
- **下一步（按优先级）**：
  1. **保留并复用 `ts_ir` 壳**：臂3 是**三波里唯一同时做到 TO 1.94% / DD 8.63% / margin 39.61bp** 的结构（S 0.78）。若后续要拼"可提交级"的候选，**低换手 + 高 margin 的壳比提高 S 更容易换来 self/prod 通过**；应先补 `group_rank` 去掉与否的单变量对照（拆掉臂3 的分组混淆）。
  2. **离散度替代集中度**（已入册）：在同一壳下把 `vec_max` 换 `vec_stddev`，sub 从 0.00 抬到 0.47，是**目前离 ★v2 的 sub≥1.0 最近的一条改动方向**（三波非退化最高 sub）。
  3. **不要再开第四波同一路线的重复**：单集 66 窗三波 30 臂最强 0.89，且 BE176 已给 1.30 上限 ⇒ 第四波若仍只换壳/字段口径，预期产出为零。
  4. **若要继续单集路线，唯一还有信息的两条**：① 补测 `insd1_price` / `insd1_value` / `insd1_tradesignificance`（补齐 D2，三波都没碰过，只有族级先验）；② 换第二套配置（decay4/nanOFF，补齐 D6）。两者齐备后六维全达，才可做 dataset 级终态裁决。
  5. **配对路线换搭档**：institutions6 三波证明它保不住 sub；平台已验证能保 sub 的是 MODEL（1.49/1.51，但那是非 `insd1_*` 原生几何），**是否允许 MODEL 作搭档腿需用户裁定**（「已点亮塔不选」口径的边界）。
  6. **不要再用 `trade_when(…, −1)`**（本波实证 S −0.40、DD +14.34pp）。
