# WAVE rt-insiders-w4 — `insiders1` 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集：`insiders1`（目标塔 **INSIDERS**）；配对集：`institutions6`（塔 INSTITUTIONS）
- 配置（平台 `get_alpha_details` 逐臂回显，10/10 一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、maxPosition=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR、simulationMode=FULL；`startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:5-16`（decay=4、nanHandling=OFF、2013-01-01 起）不同 ⇒ **第四波仍是探针口径（decay0/nanON）**；四波同一档，**本波结论只在 decay0/nanON/SUBINDUSTRY 这一格内成立**。
- 派发/收割（收割说明转录，本档未重跑派发）：`preflight_expressions` valid=true / unknown_fields=[] / any_changed=false（10/10；臂10 的 `nan` 字面量被 preflight 接受）；`operator_audit` safe=true / violations=[]（`reverse` / `group_zscore` / `ts_ir` 均不在幽灵算子清单）。
  - 查重：10 条精确式全仓扫描——**arm8 额外命中 `tracking/DEU/regular_tower/FIELD_insiders1_20261116.md:240`**，核实为该档案的 M3 **模板提案**（`group_rank(ts_sum(vec_count(insd1_shares),66), subindustry)` 带空格写法），**从未派发**，不是已派表达式；其余命中均为本波输入件与闸门临时件；与 w1/w2/w3 已入库 30 条逐条不同；派发前 `list_expressions(DEU,rt-insiders-w4)` 为空 ⇒ 无跳过臂。
  - 派发：`create_multi_simulation` → multisim `16sDwR4al4DY9pWCuwiSHey`；轮询第 1 次 children=0，第 2 次（约 2 分钟）10/10 all_terminal=true、**errors=0（全 COMPLETE，无 WARNING/CANCELLED/UNITS）**；`harvest_multisim_alphas` 首试成功（未走 404 兜底），total=10/complete=10/error_count=0；逐臂用平台 `code` 核对归属，10 条与臂表/提交顺序逐条一致（臂1→`LLKnekRL` … 臂10→`MP6bwkGM`）。
  - 落库：`upsert_backtest_rows(DEU, rt-insiders-w4, insiders1, 10)` → n=10；写后核验 10 条 `alpha_id/sharpe/fitness/margin/turnover` 与平台逐条一致。
- 判读基准（ask 给定，本档另附平台实读限值见 §1.1）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0 / 0.01≤TO≤0.70 / margin≥0.0005 / CW≤0.5 / self 与 prod 各<0.70。
- 闸种：**8 条 atom 单集件走 `LOW_2Y_SHARPE`（limit 1.58）；2 条 combined 双集件走 `IS_LADDER_SHARPE`（year=2，limit 1.58）**；`two_year_sharpe` 与 RA 载体逐臂一致（10/10）。
- **本波的三个轴**：① `ts_ir` 的信噪比窗（66 vs 252，**纯单变量**）；② 事件条件（`vec_count>1` 才算集中度）；③ 机构持股轴的**第三种形态**（有符号斜率 `reverse(group_zscore)`）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

指标经 `batch_get_alpha_metrics`（10/10 success）与 `get_alpha_details`（10/10）逐臂复核，与 ask 转录**逐值一致**。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔（pyramids/list） | RA fail（平台 `ra.ra_failed_checks`） |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|
| 1 | `LLKnekRL` | **集中度信噪比（无分组）**：`ts_ir(ts_sum(max÷sum,66), 252)` | **0.89** | **0.67** | 0.86 | **−0.11** | 2.29% | 14.40% | **62.63bp** | 98/131 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.42), LOW_2Y |
| 2 | `WjlNk9gN` | **有符号斜率**：`multiply(ts_rank(conc,252), reverse(group_zscore(inst_ratio,subindustry)))` | **−0.44** | −0.20 | −0.79 | −0.11 | 3.49% | **32.32%** | −14.89bp | 141/158 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 3：LOW_SHARPE, LOW_FITNESS, IS_LADDER（sub 过闸） |
| 3 | `pwan087v` | **硬掩码（低带）**：`if_else(rank(bf(inst_ratio,252))<0.5, ts_rank(conc,252), 0.5)` | 0.32 | 0.12 | 0.37 | 0.10 | 6.13% | 17.39% | 6.00bp | 115/124 | INSTITUTIONS×1.6+INSIDERS×1.6（eff 2） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.15), IS_LADDER |
| 4 | `A1xn6k3X` | **ts_ir 252 窗 + 分组**：`group_rank(ts_ir(conc,252), subindustry)` | 0.67 | 0.34 | 0.58 | 0.06 | **1.94%** | 11.18% | 34.13bp | 130/153 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.32), LOW_2Y |
| 5 | `QP0neEaX` | **H2 乘法**：`multiply(ts_rank(conc,252), rank(1/(dfc(vec_count)+1)))` | 0.56 | 0.27 | 0.41 | 0.19 | 9.09% | 12.07% | 6.18bp | 129/168 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.27), LOW_2Y |
| 6 | `9ql9oJw9` | **裸核（H2/H5 基准）**：`ts_rank(ts_sum(max÷sum,66), 252)` | 0.20 | 0.05 | −0.47 | 0.08 | 7.20% | 13.09% | 2.43bp | 138/155 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.09), LOW_2Y |
| 7 | `Jj8nlbpW` | **ts_ir 66 窗 + 分组**：`group_rank(ts_ir(conc,66), subindustry)` | 0.88 | 0.52 | **1.05** | **0.46** | 5.44% | **10.37%** | 16.14bp | 118/161 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y（sub 过闸） |
| 8 | `qM7nbgl1` | **频率代理（H3 对照）**：`group_rank(ts_sum(vec_count(insd1_shares),66), subindustry)` | 0.62 | 0.32 | 0.72 | 0.01 | 4.26% | 11.96% | 15.79bp | 115/144 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.29), LOW_2Y |
| 9 | `1YWovJdJ` | **H4 时钟（valueeur）**：`ts_rank(252−dfc(bf(vec_sum(valueeur),252)), 252)` | 0.43 | 0.17 | 0.32 | 0.24 | **11.21%** | **8.48%（**四波最低**）** | 3.53bp | 145/147 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y（sub 过闸） |
| 10 | `MP6bwkGM` | **事件条件 ts_ir**：`group_rank(ts_ir(if_else(vec_count>1, max÷sum, nan), 66), subindustry)` | 0.82 | 0.53 | 0.81 | **0.68（**四波最高**）** | 6.71% | 11.93% | 15.62bp | **55**/145 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y（sub 过闸） |

- `conc` = `ts_sum(divide(vec_max(insd1_valueeur), vec_sum(insd1_valueeur)), 66)`；`dfc` = `days_from_last_change`；`bf` = `ts_backfill`；`inst_ratio` = `divide(aggregate_share_count_institutions, aggregate_share_count_all_owners)`。
- **本波极值**：best S **0.89**（臂1）/ best F **0.67**（臂1，四波最高）/ best 2Y **1.05**（臂7）/ **best sub 0.68（臂10，四波最高）** / 最低 TO **1.94%**（臂4）/ **最高 margin 62.63bp（臂1，四波最高，为 w3 最高值 39.61bp 的 1.58 倍）** / **最低 DD 8.48%（臂9；⚠ ask 括注称臂7 为"全波最低 DD"，实读只有 10.37%，最低是臂9 的 8.48% —— 本档更正）**。
- **0 达标**：10/10 臂 `failed_ra_count` ≥3（4/3/4/4/4/4/3/4/3/3），**无一条 RA 全闸**；`status` 10/10 = `UNSUBMITTED`（提交态），仿真态全 COMPLETE、errors=0。
- **CW 10/10 全 pass**（含臂10 的 55 只长侧）；**LC/SC 55–168**（臂10 为单侧窄，见 §6）。

### 1.1 平台闸限实读（补齐 ask 的「平台 LOW_SHARPE limit 未读到」）

| 闸 | 平台实读 limit | 与 ask 基准的关系 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10 臂） | 与内部严线一致 |
| LOW_FITNESS | **1.0** | 一致 |
| HIGH_TURNOVER / LOW_TURNOVER | **0.70 / 0.01**（10/10 pass，TO 1.94–11.21%） | 一致 |
| CONCENTRATED_WEIGHT | 本波 10/10 **pass**（无 value 回显） | 本波无 CW 事件 |
| LOW_2Y_SHARPE / IS_LADDER_SHARPE | **1.58**（year=2） | 一致 |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂不同**：臂2 pass / 臂6 0.09 / 臂3 0.15 / 臂5 0.27 / 臂8 0.29 / 臂4 0.32 / 臂1 0.42；臂7/臂9/臂10 判 PASS | ⚠ **sub≥1.0 是本地 review 线，不是平台闸限**（`thresholds.json:21`）；平台限只有 0.09–0.42 |

⇒ ask 的「平台 LOW_SHARPE limit 本轮未读到」**本轮已实读补齐 = 1.58**；且 **verdict 与 sub 口径无关**——任何 sub 判据下 10/10 臂仍全部挂 LOW_SHARPE + LOW_FITNESS（S≤0.89 vs 1.58、F≤0.67 vs 1.0）。

## §2 逐臂归因条目

### 2.1 `ts_ir` 信噪比窗：66 vs 252（**纯单变量**，本波最干净的窗宽对照）

3. **臂4 `A1xn6k3X`（`group_rank(ts_ir(conc, 252), subindustry)`）**：S 0.67 / F 0.34 / 2Y 0.58 / sub 0.06 / **TO 1.94%** / DD 11.18% / margin 34.13bp / LC-SC 130/153；RA 4 挂。
7. **臂7 `Jj8nlbpW`（`group_rank(ts_ir(conc, 66), subindustry)`）**：S **0.88** / F **0.52** / 2Y **1.05** / sub **0.46** / TO 5.44% / DD **10.37%** / margin 16.14bp / LC-SC 118/161；RA 仅 3 挂（sub 过闸）。
   - **两臂只差 `ts_ir` 的第二参（252 → 66）**，其余 `ts_sum(divide(vec_max(ve),vec_sum(ve)),66)` 与 `group_rank(·,subindustry)` 逐字相同 ⇒ **四波里最干净的窗宽单变量对照**。
   - Δ（66 − 252）：S **+0.21** / F **+0.18** / 2Y **+0.47** / sub **+0.40** / DD −0.81pp；代价 TO **+3.50pp**、margin **−17.99bp**、LC 130→118、SC 153→161。
   - ⇒ **在 ts_ir 壳内，66 窗在 S/F/2Y/sub 四项全面优于 252 窗，换手与 margin 让步**。机制解释：252 窗的 ts_ir 把信号压得更慢（TO 1.94%），强项只剩 margin（34.13bp）；66 窗保留了更多时变信息，S/2Y/sub 因此更高。**两者是"效率 vs 强度"的取舍，不是单调优劣。**
   - ⚠ **ask 的衰减梯判据（22→66→132 应呈单峰）本波仍不能判**：只有 66 与 252 两点，**22 与 132 未扫**。只能记"252→66 方向上升"，**不能**说"66 是峰"或"结构没对上"。

### 2.2 分组轴：subindustry（**本波推翻我在 w3 的"分组效应 ≤0.1"推断**）

1. **臂1 `LLKnekRL`（`ts_ir(conc, 252)`，**无分组**）**：S **0.89** / F **0.67** / 2Y 0.86 / sub −0.11 / TO 2.29% / DD 14.40% / **margin 62.63bp** / LC-SC 98/131；RA 4 挂。
   - **vs 臂4（唯一差异：多一层 `group_rank(·, subindustry)`）**：S **−0.22** / F **−0.33** / 2Y **−0.28** / margin **−28.50bp**；换到 sub **+0.17**、DD −3.22pp、LC 98→130、SC 131→153。
   - ⇒ **`group_rank(subindustry)` 在这条核上是强负杠杆**：它把 S 砍 0.22、F 砍 0.33、margin 砍 28.5bp，只换来 sub +0.17 与回撤 −3.22pp、宽度 +54 只。
   - ⚠ **这是一条对我自己 w3 结论的更正**：w3 档 §2.2/§12 曾按 w1/w2 的 sector 分组（−0.03 / +0.01）推断"分组效应量 ≤0.1，故 w3 臂3 的 +0.61 主要来自 ts_ir"。**本波直接实测 subindustry 分组 = −0.22 S**，说明该推断低估了分组代价 ⇒ **w3 臂3 的 ts_ir 增益应上调到约 +0.83（0.61 + 0.22）**，且"分组效应 ≤0.1"这条只能限定在 **sector** 轴上，**不能推广到 subindustry**。
   - 方向一致性：分组轴的三次测量（sector ≈0 / bucket ≈0 / subindustry −0.22）说明**分组越细，S 损失越大，但 sub 与 DD 越好**——这是一条形态内部的稳定取舍。

### 2.3 H2 乘法：第三次独立复现（**纯单变量**，左因子逐字相同）

5. **臂5 `QP0neEaX`（`multiply(ts_rank(conc,252), rank(1/(dfc(vec_count(insd1_shares))+1)))`）**：S 0.56 / F 0.27 / 2Y 0.41 / sub 0.19 / TO 9.09% / DD 12.07% / margin 6.18bp / LC-SC 129/168；RA 4 挂。
6. **臂6 `9ql9oJw9`（裸核 `ts_rank(ts_sum(max÷sum,66), 252)`，= 臂5 的左因子逐字相同）**：S 0.20 / F 0.05 / 2Y −0.47 / sub 0.08 / TO 7.20% / DD 13.09% / margin 2.43bp / LC-SC 138/155；RA 4 挂。
   - Δ（复合 − 左腿）：S **+0.36** / F **+0.22** / 2Y **+0.88** / sub **+0.11** / TO +1.89pp / DD −1.02pp / margin **+3.75bp**。
   - ⇒ **w2 入册的"集中度 × 事件新鲜度乘法交互"的第三次独立验证**（w2 +0.08~+0.11、w3 +0.38、w4 **+0.36**），且三次都至少有一侧是**逐字相同的单变量**。**不触发稀释铁律**。
   - 三次的字段组合覆盖：w2 = valueeur 集中度 × holdings 新鲜度（`vec_avg`）；w3 = shares 集中度 × shares 新鲜度（`vec_count`）；w4 = valueeur 集中度 × shares 新鲜度（`vec_count`）⇒ **交互对"集中度字段"和"新鲜度字段"的换用都稳健**。

### 2.4 H3 机制对照：`ts_ir` 集中度 vs 事件频率（同分组同窗，公平对照）

7. **臂7（ts_ir 66，见 §2.1）** vs 8. **臂8 `qM7nbgl1`（`group_rank(ts_sum(vec_count(insd1_shares), 66), subindustry)`）**：S 0.62 / F 0.32 / 2Y 0.72 / sub **0.01** / TO 4.26% / DD 11.96% / margin 15.79bp / LC-SC 115/144；RA 4 挂。
   - Δ（臂7 − 臂8）：S **+0.26** / F **+0.20** / 2Y **+0.33** / sub **+0.45** / TO +1.18pp / DD −1.59pp / margin +0.35bp。
   - ⇒ **"集中度的信噪比"在每个面都优于"交易条数"**（尤其是 sub：0.46 vs 0.01）。两者分组与窗口一致，是机制层的公平对照。
   - FIELD 档 M3（事件广度）原评"N：250 日 count 有截面，方向未定"（`FIELD_insiders1_20261116.md:244`）——**本波实测：频率有正信号（S 0.62）但 sub≈0，作为主核不如集中度信噪比**。

### 2.5 H4 事件时钟：金额时钟 vs 条数时钟（**跨波纯单变量**）

9. **臂9 `1YWovJdJ`（`ts_rank(252 − dfc(ts_backfill(vec_sum(insd1_valueeur),252)), 252)`）**：S **0.43** / F 0.17 / 2Y 0.32 / sub 0.24 / **TO 11.21%（本波最高）** / **DD 8.48%（四波最低）** / margin 3.53bp / LC-SC 145/147（本波唯一接近平衡的票池）；RA 3 挂（sub 过闸）。
   - **vs w3 臂2（`ts_rank(252 − dfc(ts_backfill(vec_count(insd1_shares),252)), 252)`，S 0.27 / F 0.08 / 2Y 0.09 / sub 0.02 / TO 9.31% / DD 8.61% / margin 2.56bp）**：**同壳、只差 `ts_backfill` 里的字段**（金额和 vs 交易条数）⇒ **纯单变量跨波对照**。
   - Δ（金额 − 条数）：S **+0.16** / F +0.09 / 2Y **+0.23** / sub **+0.22** / TO +1.90pp / DD −0.13pp / margin +0.97bp。
   - ⇒ **"事件时钟"用金额变化优于用交易条数**（差 0.16 > ask 给的 0.10 阈值）。两者 S 都低（0.43/0.27），是"哪个时钟更对"的设计结论，不是可推进候选。

### 2.6 事件条件（臂10）：sub 大幅改善，但长侧腰斩

10. **臂10 `MP6bwkGM`（`group_rank(ts_ir(if_else(vec_count(insd1_shares) > 1, max÷sum, nan), 66), subindustry)`）**：S 0.82 / F 0.53 / 2Y 0.81 / **sub 0.68（四波最高，平台 LOW_SUB 判 PASS）** / TO 6.71% / DD 11.93% / margin 15.62bp / **LC-SC 55/145**；RA 3 挂。
    - **vs 臂7（唯一差异：内层集中度多包一层 `if_else(vec_count>1, ·, nan)`）**：S −0.06 / F +0.01 / 2Y −0.24 / sub **+0.22** / TO +1.27pp / DD +1.56pp / margin −0.52bp / **LC 118→55（−63）、SC 161→145（−16）**。
    - ⇒ **"只在当日 ≥2 笔内部人交易时计算集中度"把 sub 从 0.46 抬到 0.68（+0.22）**，代价是 S −0.06、2Y −0.24、DD +1.56pp，**以及长侧票池从 118 腰斩到 55**。
    - ⚠ **单侧宽度不对称必须单独登记**（§6）：这不是"宽度塌缩"（总票池 200、CW 平台判 PASS），而是**长/空严重不对称**。sub 0.68 是在**55 只长侧**的截面上取得的，其可靠性受此限制——**不得**把 0.68 当作"已接近 ★v2 的 sub≥1.0"的充分证据，只能说"方向上本波最接近"。

### 2.7 机构持股轴的第三种形态：有符号斜率（臂2）——再次指向"高带侧"

2. **臂2 `WjlNk9gN`（`multiply(ts_rank(conc,252), reverse(group_zscore(inst_ratio, subindustry)))`）**：S **−0.44** / F −0.20 / 2Y −0.79 / sub −0.11 / TO 3.49% / **DD 32.32%（四波最高）** / margin −14.89bp / LC-SC 141/158；RA 3 挂（sub 过闸）。
   - **H5 预注册条件**（臂2 S ≥ 臂6−0.05 = 0.15 且 sub ≥ 臂3+0.3 = 0.40）：**实读 S −0.44 < 0.15 ⇒ 条件不成立**（与 ask 转录一致）。
   - **三种形态横向比**：
     | 形态 | 表达式核心 | S | 隐含方向 |
     |---|---|---:|---|
     | 裸核（臂6） | `ts_rank(conc,252)` | 0.20 | — |
     | 硬掩码低带（臂3） | `if_else(rank(bf(inst))<0.5, core, 0.5)` | **+0.32** | 低带强 |
     | 有符号斜率（臂2） | `core × reverse(group_zscore(inst))` | **−0.44** | 高带强（反向加权即负） |
     | w3 加权高带 | `core × group_rank(inst)` | +0.33 | 高带强 |
     | w3 加权低带 | `core × (1−group_rank(inst))` | −0.22 | 高带强 |
   - ⇒ **除硬掩码外，所有"显式加权"形态（w3 高带 +0.33 / w3 低带 −0.22 / w4 有符号斜率 −0.44）一致指向：正信号在机构持股高的一侧。**硬掩码是唯一的反例（+0.32），且它自带 `0.5` 常数腿。
   - ⇒ **四波汇总结论**：**"低机构持股是强侧"只在硬 `if_else(…, 0.5)` 掩码形态内成立，是形态产物，不是经济方向。** 这条从 w3 的"两波反号"升级为 **w4 的"三形态一致 + 掩码孤例"**，证据强度显著提高；也再次说明 **"缺掩码单独对照"这个缺口是真有害的**。

## §3 对照实验汇总（裸 vs 改造，同配置同日期）

| # | 对照 | 改造件 | 裸件 | Δ（S/F/2Y/sub） | 判定 |
|---|---|---|---|---|---|
| C1 | **ts_ir 窗 66 vs 252**（纯单变量） | 臂7 `0.88/0.52/1.05/0.46` | 臂4 `0.67/0.34/0.58/0.06` | **+0.21/+0.18/+0.47/+0.40** | 66 窗强（TO +3.50pp、margin −17.99bp 为代价） |
| C2 | **subindustry 分组 vs 无分组**（纯单变量） | 臂4 `0.67/0.34/0.58/0.06` | 臂1 `0.89/0.67/0.86/−0.11` | **−0.22/−0.33/−0.28/+0.17** | 分组强负（唯 sub/DD/宽度获益） |
| C3 | **乘法 vs 左腿**（纯单变量、第三次） | 臂5 `0.56/0.27/0.41/0.19` | 臂6 `0.20/0.05/−0.47/0.08` | **+0.36/+0.22/+0.88/+0.11** | **增益**（不稀释） |
| C4 | **ts_ir 集中度 vs 事件频率**（同分组同窗） | 臂7 `0.88/0.52/1.05/0.46` | 臂8 `0.62/0.32/0.72/0.01` | **+0.26/+0.20/+0.33/+0.45** | 集中度信噪比全胜 |
| C5 | **金额时钟 vs 条数时钟**（跨波纯单变量） | 臂9 `0.43/0.17/0.32/0.24` | w3 臂2 `0.27/0.08/0.09/0.02` | **+0.16/+0.09/+0.23/+0.22** | 金额时钟更优 |
| C6 | **事件条件 vs 无条件**（纯单变量） | 臂10 `0.82/0.53/0.81/0.68` | 臂7 `0.88/0.52/1.05/0.46` | −0.06/+0.01/−0.24/**+0.22** | sub 换 S/2Y/宽度 |
| C7 | **硬掩码 vs 裸核** | 臂3 `0.32/0.12/0.37/0.10` | 臂6 `0.20/0.05/−0.47/0.08` | +0.12/+0.07/+0.84/+0.02 | 小正（与加权形态反号） |
| C8 | **有符号斜率 vs 裸核** | 臂2 `−0.44/−0.20/−0.79/−0.11` | 臂6 `0.20/0.05/−0.47/0.08` | **−0.64/−0.25/−0.32/−0.19** | 强负 |

**跨波对照总表（同一判据在不同波上的符号）**：

| 判据 | w1 | w2 | w3 | w4 | 跨波结论 |
|---|---|---|---|---|---|
| 乘法复合 vs 左腿 | — | +0.08~+0.11 | +0.38 | **+0.36** | **三波一致为正，杠杆成立** |
| 离散度 vs 集中度 | — | +0.25(sub) | +0.27 | （本波未测） | 两波一致 |
| 掩码低带 vs 高带 | +0.21 | +0.18 | +0.28 | （本波无高带） | 掩码三波一致（但见下条） |
| **显式加权的高/低带** | — | — | 加权高带 +0.33 / 低带 −0.22 | 有符号斜率 −0.44 | **所有加权形态一致：高带侧为正** |
| ts_ir 窗 | — | — | 252 only | **66 > 252** | 单波（22/132 未扫） |
| 事件时钟（金额 vs 条数） | — | — | 条数 | **金额 +0.16** | 跨波纯单变量，金额更优 |

## §4 符号指纹 / 方向

- **严格符号指纹仍未测**：10 条表达式**无整式取反**（`logs/_tmp_rt-insiders-w4_arms.json` 全文无前置负号 / `multiply(-1,…)`）。ask 的判据（S(−expr)≈−S(expr) 且差<0.03 且 TO/DD/longCount 逐位相同）**无法执行**，如实记「未测」；FIELD 档 §5 要求的"增持语义必须同波带反号对照臂"**连续四波未带**。
- **本波有一条比反号对照更强的形态对照**：臂2 的 `reverse(group_zscore(...))` 与"高带加权"在**同一个机构持股轴上方向相反**（互为镜像）；配 w3 的 `x·g` / `x·(1−g)` 互补权重（两者相加 ≡ 裸腿），可以把机构持股轴**完整二分**：
  - 裸核 x（臂6）S 0.20；高带加权（w3 臂7）**+0.33**；低带加权（w3 臂6）**−0.22**；有符号斜率反权重（臂2）**−0.44**。
  - ⇒ **x 的正向预测力在机构持股高的一侧，反向权重一律变负**；三种独立写法一致。
- **与 w2 的关系（重要）**：w2 记录的"低机构持股为强侧"**只在硬掩码形态成立**；本波是由"第三种形态（有符号斜率）"把它从"两波反号"推进到"三形态一致 + 掩码孤例"。⇒ 该条继续**只作形态内观察**，不得作经济结论（见 §12 deadAxes）。
- **跨区符号不外推**：本档未引用 USA 文献符号，也未把 DEU 的 insiders 符号外推到 TWN/KOR。

## §5 稀释铁律（乘法/bucket/壳层低于对应单腿 = 稀释）

- **乘法（臂5 vs 臂6）：不触发**，S +0.36 / F +0.22 / 2Y +0.88 / sub +0.11 全部高于单腿 ⇒ 第三次复现。
- **有符号斜率（臂2 vs 臂6）：强稀释且为负**（S −0.64、DD +19.23pp）⇒ 反向加权不是稀释而是"把信号翻转"。
- **硬掩码（臂3 vs 臂6）：小幅正**（S +0.12）——与 w2 的 −0.06、w3 的 +0.10 一起构成"掩码对 S 的效应在 −0.06~+0.12 之间抖动"⇒ **不稳定，不可作杠杆**。
- **ts_ir 壳（臂7 vs 臂4）：不是稀释，是窗宽取舍**（S/2Y/sub 升、TO/margin 降）。
- **子分组（臂4 vs 臂1）：是"强度换宽度/回撤"**（S −0.22 换 sub +0.17 / DD −3.22pp / 宽度 +54 只），**不是无条件稀释**——按"复合需高于单腿才值得留"的强度口径，分组不划算。

## §6 宽度 / CW 登记（数据层 ≠ 信号死 ≠ 表达层）

| 臂 | LC/SC | CW | 归因 |
|---|---|---|---|
| 臂10 `MP6bwkGM` | **55/145** | **pass** | **单侧宽度不对称**（长侧 55、空侧 145）：事件条件 `vec_count>1` 只在多笔自然日生效，长侧被系统性削薄。总票池 200、CW 平台判 PASS，**不是宽度塌缩**，但 **sub 0.68 建立在 55 只长侧上**，可靠性受限 |
| 臂1 `LLKnekRL` | 98/131 | pass | 轻度不对称（无分组导致长侧偏薄） |
| 臂2 `WjlNk9gN` | 141/158 | pass | 宽度正常；DD 32.32% 来自反向加权（表达层） |
| 其余 7 臂 | 115–168 | pass | 全宽 |

- **本波 0 条宽度塌缩、0 条 CW 挂闸**；**0 条 data_excluded**（10/10 臂 pnl 有值，臂2 −2,685,089 为负但非零）。
- 臂2 的高 DD（32.32%）与臂10 的单侧窄都**属表达层**（形态选择），**不得**登记成数据层或信号死。

## §7 塔位判读（点塔相关性）

平台 `get_alpha_details.pyramids` 逐臂实读（10/10）：

- **目标塔 INSIDERS 出现 10/10 臂**：
  - 单塔 8 条（`effective=1`）：臂1 `LLKnekRL`、臂4 `A1xn6k3X`、臂5 `QP0neEaX`、臂6 `9ql9oJw9`、臂7 `Jj8nlbpW`、臂8 `qM7nbgl1`、臂9 `1YWovJdJ`、臂10 `MP6bwkGM` = `DEU/D1/INSIDERS`×1.6。
  - 双塔 2 条（`effective=2`）：臂2 `WjlNk9gN`、臂3 `pwan087v` = `DEU/D1/INSTITUTIONS`×1.6 + `DEU/D1/INSIDERS`×1.6；`ra.pyramid_short` 同步为 `institutions/insiders`。
- **点位 ≠ 点亮**：10/10 臂 RA fail ≥3 ⇒ **本波实际点亮 INSIDERS 塔 0 颗、INSTITUTIONS 塔 0 颗**，塔计数不变（insiders 1/3、institutions 1/3，`CAMPAIGN_REPORT_20261116.md:34`）。
- **四波塔位结构对照**：w1 5 单+5 双（双塔全带 UNITS）、w2 5 单+5 双、w3 6 单+4 双、w4 **8 单+2 双**。四波双塔件的 S/F/sub **从未超过同波最好的单塔件**（w4：双塔最好 0.32 vs 单塔最好 0.89）⇒ **institutions 双塔在本族四波无强度优势**，且双塔件还要多吃一次 IS_LADDER 审查。

## §8 数据层判读（data_excluded 与信号死分开）

- **不 data_excluded**：§6（LC/SC 55–168、CW 10/10 pass、TO 1.94–11.21%、pnl 均有值）；`insiders1` 8 字段全 VECTOR、平台 `get_datafields` 实读 8/8（`FIELD_insiders1_20261116.md:23-40`）；preflight `unknown_fields=[]`（`insd1_valueeur` / `insd1_shares` / `vec_count` 均已证存）。
- **不判信号死**：本波 10 臂、**1 套配置**、**窗口只有 66 与 252 两点**、**无翻符号对照**、**无掩码单独对照** ⇒ 六维 D2/D6 未达（§9），按「探针不产生判死」与 AGENTS §7.6 **只能记 provisional**。
- **本波的三条负结论都是信号层/表达层**：有符号斜率破坏（表达层）、subindustry 分组负杠杆（表达层）、事件频率弱于信噪比（信号层）。**都不是数据层排除。**

## §9 判死六维闸盘点（D1–D6；四波累计口径）

| 维 | 四波现状 | 判定 |
|---|---|---|
| **D1 结构互异模板 ≥10** | 四波累计约 **17–20** 个互异机制（在 w1–w3 的 13–15 之上新增：`ts_ir` 66 窗 / 事件条件 ts_ir / 有符号斜率加权 / 频率代理 / 金额时钟 / 无分组 ts_ir） | **✓ 达** |
| **D2 字段族自测** | 已测 **3/6**：`insd1_holdings`（w1/w2）、`insd1_valueeur`（w1/w2/w4）、`insd1_shares`（w3/w4）；**未测** `insd1_price` / `insd1_value` / `insd1_tradesignificance`（三者有族级判死先验 S 1.13/1.14/1.21，但按 AGENTS §7.6「禁止凭族先验封禁未测字段」不能算已测） | **✗ 未达** |
| **D3 矩全家（水平/一阶差/二阶波动/比值或信噪比）** | 水平 ✓、一阶差 ✓（w2 臂5，负）、二阶波动 ✓（w2 臂2 / w3 臂10）、比值 ✓、信噪比 ✓（w3 臂3 / w4 臂1/4/7/10） | **✓ 达** |
| **D4 分组轴 ≥2** | sector ✓、subindustry ✓、bucket ✓ | **✓ 达** |
| **D5 非线性 ≥1** | `multiply` / `if_else` / `trade_when` / `bucket` / `ts_rank` / `ts_ir` / `reverse` / `group_zscore` | **✓ 达** |
| **D6 配置 ≥2** | 四波**同一套**：DEU/TOP500/D1 + decay0 + SUBINDUSTRY + trunc0.08 + nanHandling ON；**decay 4 / nanHandling OFF 四波均未扫** | **✗ 未达** |

⇒ 仍只缺 **D2 / D6**：**不得判死、不得封集、不得作为邻接数据集/族的先验**（AGENTS §7.6）。但必须如实登记一个转折：**本波是该族四波里唯一出现"三项新高位"的一波**（best F 0.67、best sub 0.68、best margin 62.63bp 均为四波最高），且 D2 未测的三个字段恰是族内**最有判死先验、最不可能翻盘**的三个 ⇒ 判死资格实质已"差一步"，但**在 D2/D6 补齐前仍不得下终态**。

## §10 近闸候选（ask 口径：S≥1.2 或距任一硬闸 ≤0.4；≤2 条，按 S 降序）

按平台实读限值逐条核（S 闸 1.58 / F 1.0 / 2Y 1.58 / sub 本地 1.0 / CW 0.1 / TO 0.70 / margin 5bp）：

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `LLKnekRL`（臂1） | **0.89** | **距 F 闸 0.33 ≤ 0.4**（F 0.67 vs limit 1.0）——本波唯一命中实质硬闸且 S 最高的臂；同时是四波最高 F、最高 margin（62.63bp）、最低 TO 之一（2.29%）；其余：S 距闸 0.69、2Y 距闸 0.72、sub 距本地线 1.11（sub −0.11 是它的硬伤）、CW/TO/margin 全 pass |
| 2 | `MP6bwkGM`（臂10） | 0.82 | **距本地 sub 线 0.32 ≤ 0.4**（sub 0.68 vs 1.0）；⚠ **该"近闸"只在本地 1.0 线下成立**——平台 `LOW_SUB_UNIVERSE_SHARPE` 对臂10 判 **PASS**，按平台口径无缺口；其余：S 距 0.76、F 距 0.47、2Y 距 0.77；且 **长侧仅 55 只**（§6） |

- **排序外如实登记**：`Jj8nlbpW`（臂7）S **0.88**、2Y 1.05（本波最高）、sub 0.46（平台 PASS）、DD 10.37%，是**综合最好的结构**，但它的四个闸距分别为 S 0.70 / F 0.48 / 2Y 0.53 / 本地 sub 0.54，**没有任何一个 ≤0.4** ⇒ 按 ask 判据**不入选**；本档仍把"先测 `d5aE63Ew`/`LLKnekRL` 这一类要先补 prod"的次序里给它一席（见 §14）。
- **S≥1.2：无**（最高 0.89）。**距 S 闸最近 0.69**（臂1）、距 2Y 闸最近 0.53（臂7 的 1.05）。
- ⚠ **margin 机械命中**：臂6 2.43bp（缺 0.000257）、臂9 3.53bp（缺 0.000147）、臂2 负值（缺 0.001989）——按绝对差都在 0.4 内，但 **margin 闸量纲 0.0005（全区间约 0.007），"0.4" 比该指标全区间大 50+ 倍、阈值失去分辨力**；三者 S 分别 0.20/0.43/−0.44 ⇒ **明确不列入 near**（与 w1 排除 TO、w3 排除 margin 的机械命中同一处置逻辑）。

⇒ n_pass = 0，n_near = 2。

## §11 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`（维持 w1–w3，无终态转换）**。依据：

1. **本波确有实质进步**：best F **0.67**（四波最高，w3 为 0.43）、best sub **0.68**（四波最高，w3 为 0.47）、best margin **62.63bp**（四波最高，w3 为 39.61bp）、best 2Y **1.05**（四波最高，w2 为 1.11 除外——w2 的 1.11 是配对件）。⇒ 该族在"F / sub / 效率"三个面都创了新高。
2. **但仍 0 达标、且仍在已知单集上限内**：四波 40 臂最强 0.81/0.89/0.78/**0.89**，**全部低于 BE176 的 1.30 单集上限**（`BE176_INSIDERS1_CEILING_130_20261112.md:23,28-30`），距 1.58 闸差 0.69。
3. **配对路线（institutions6）四波皆负或平**：硬掩码 +0.32、有符号斜率 −0.44、w1/w2/w3 掩码/加权均在 −0.22~+0.33 之间；**sub 从未 ≥1.0**（本波配对件 sub 0.10 / −0.11）。对照平台实读的 [INSIDERS,MODEL] 存量件 sub 1.49/1.51 ⇒ **第二腿的选择仍是 sub 的决定变量，MODEL 才是已验证的那条**（仅 DEU 同区实读；那两条并非 `insd1_*` 原生几何，见 w1 §2.4）。
4. **数据层无排除**：LC/SC 55–168、CW 10/10 pass、TO 正常、pnl 有值。
5. **六维只剩 D2/D6 未达**（§9）⇒ 不得终判死、不得封集。
6. **DB 侧一致**：`get_dead_datasets("DEU")` 返回 19 集，**不含 `insiders1`**。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90`：PASS=有臂过 RA 全闸 / PARTIAL=0 达标但 ≥1 近闸 / FAIL=0 达标 0 近闸；本波 `n_pass=0 / n_near=2`）。**未自造枚举值。**

- **稳健性**：该判定对 sub 口径不敏感（10/10 臂在任何 sub 判据下仍挂 LOW_SHARPE+LOW_FITNESS）。
- **与 w3（FAIL）的差异**：w3 最好 F 0.43（距 F 闸 0.57）、无任何实质近闸；本波臂1 F **0.67（距闸 0.33）**、臂10 sub 0.68（距本地线 0.32）⇒ 本波**确实更强**，不是口径放宽。
- **与 w2（PARTIAL）的差异**：w2 的近闸只有臂3（F 0.63 距 0.37）；本波有两条，且臂1 的 S 更高（0.89 vs 0.89 持平）、F 更高（0.67 vs 0.63）、margin 高 41bp。

## §12 newLever 登记

**入册 1 条（跨波实证 + 纯单变量对照）**：

> **事件时钟：用"金额变化"（`vec_sum(insd1_valueeur)`）比用"交易条数"（`vec_count(insd1_shares)`）更好**。同壳（`ts_rank(252 − days_from_last_change(ts_backfill(F,252)), 252)`）、**只差 `ts_backfill` 里的字段**：臂9（金额）S 0.43 / F 0.17 / 2Y 0.32 / sub 0.24 / margin 3.53bp vs w3 臂2（条数）S 0.27 / F 0.08 / 2Y 0.09 / sub 0.02 / margin 2.56bp ⇒ **S +0.16、F +0.09、2Y +0.23、sub +0.22、margin +0.97bp**（代价 TO +1.90pp、DD −0.13pp）。
> **跨波支撑**：这是 w3 与 w4 两波之间、同一壳、只换一个字段的**纯单变量**对照，满足"裸 vs 改造"要求；差额 0.16 高于 ask 给的 H4 判据阈值 0.10。
> **适用条件与 caveat**：① 只在 decay0/nanON/SUBINDUSTRY 档；② 两侧 S 都低（0.43 vs 0.27），**这是"哪个时钟更对"的设计结论，不是可推进候选**；③ 金额时钟的 TO 更高（11.21%，本波最高），若目标是低换手则不适用；④ 只测了 valueeur 与 count 两种时钟，未测 `vec_avg(holdings)`（w2 用过、但壳不同，不可直接比）。

**复现确认（不算新入册，如实标注）**：
- **w2 入册的"集中度 × 事件新鲜度乘法交互"第三次复现**：臂5 对左腿（逐字相同的单变量）+0.36 S / +0.22 F / +0.88 2Y / +0.11 sub ⇒ 三次独立验证（w2 +0.08~+0.11、w3 +0.38、w4 +0.36），且覆盖三种字段组合 ⇒ 该杠杆已从"两波同向"升为"三波同向、多字段稳健"。
- **w3 入册的"离散度 > 集中度"本波未测**（本波集中度用 valueeur、离散度未跑）⇒ 维持两波证据，不新增。

**未入册（负结论 / 不稳定 / 单波）**：
- **`ts_ir` 66 窗优于 252 窗**（+0.21 S / +0.47 2Y / +0.40 sub）：本波是最干净的单变量对照，但**只有本波一个数据点**（w3 只跑过 252），不满足"跨波实证" ⇒ 记 sprout，**不入册**；补 132 窗或第二套配置后可再议。
- **subindustry 分组是强负杠杆**（−0.22 S / −0.33 F / −28.5bp margin）：单波实测，且与 w1/w2 的 sector 分组结论不同轴 ⇒ 记 sprout + **更正 w3 的推断**，不入册。
- **有符号斜率破坏**（−0.44）、**事件频率弱于信噪比**、**硬掩码效应不稳定** ⇒ 负结论/不稳定，不入册。

## §13 证据通道与盲区

**本轮实跑的核验（全部只读，零写入生产库）**：
- `mcp__wq-brain-http__batch_get_alpha_metrics(10 ids)`：10/10 success，S/F/2Y/sub/TO/margin/DD/`failed_ra_count`/`returns` 与 ask 转录**逐值一致**。
- `mcp__wq-brain-http__get_alpha_details`：**逐臂 10/10** 取回 `settings`（decay0/nanON/SUBINDUSTRY/trunc0.08/2014-01-01→2023-12-31，10/10 一致）、`metrics`（含 longCount/shortCount）、`ra.ra_failed_checks`、`checks.fail`（含 limit）、`checks.warning`（**10/10 无 UNITS**，仅 CLUSTER_TEST/MATCHES_*）、`pyramids.list`（含 multiplier/effective）、`code`。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w4)`：10 条，表达式与 `logs/_tmp_rt-insiders-w4_arms.json` **逐条同序**；`atom_flag` = 8 atom + 2 combined(2 集)，与塔位一致。
- 跨波对照件读数取自 w1/w2/w3 已入库档（`WAVE_rt-insiders-w1/w2/w3_20261116.md` §1，源为平台 `get_alpha_details`）；**本档未重跑 w1–w3 臂**。

**盲区（如实登记，不猜不补）**：
1. **符号指纹未测**：0 条整式反号臂，严格判据无法执行（§4）；连续四波缺该对照臂。本波用"有符号斜率的镜像"部分替代，但**不是** ask 指定的指纹形态。
2. **掩码单独对照仍缺**：本波由"第三种形态"再次间接证明该缺口有害，但未跑 `if_else(cond, 1, 0.5)` 类纯掩码臂。
3. **衰减梯只有两个点**：66 与 252；**22 与 132 未扫** ⇒ 不能判"单峰"，只能判"252→66 上升"。
4. **配置只 1 套**：decay4/nanOFF 区域生产档四波均未跑 ⇒ **配置层死/活未判**（D6）。
5. **prod / self 全部 null**：按分工归相关性员，本档不测、不猜。
6. **年度分年未取**：本波未跑 `get_alpha_yearly_stats`；ask 称 `XgaGb3J1` / `d5a2aO7v` 已核十年——二者**不在本波 10 臂内**，本档仅转录，**未复跑**。
7. **臂10 的事件条件语义未隔离**：`vec_count>1` 同时改变了「有效样本数」与「长侧可交易域」，两者在本波纠缠；未跑"只在 vec_count==1 时计算"的对照臂，故无法区分"多笔日信息量更高"与"长侧变薄导致截面不同"。
8. **arm8 查重命中 `FIELD_insiders1_20261116.md:240` 是模板提案**（带空格写法、从未派发），不是已派表达式 ⇒ 不构成重复臂；该判断基于文本比对，**未做 fingerprint 级校验**（DB 无该提案的 fingerprint 记录）。

## §14 终态

- **波**：`PARTIAL`（0 达标 / 2 近闸，n_pass=0 / n_near=2）；best S **0.89**（`LLKnekRL` 臂1）/ best F **0.67**（同，四波最高）/ best 2Y **1.05**（`Jj8nlbpW` 臂7）/ **best sub 0.68**（`MP6bwkGM` 臂10，四波最高）/ 最低 TO 1.94%（`A1xn6k3X` 臂4）/ **最高 margin 62.63bp**（臂1，四波最高）/ 最低 DD 8.48%（`1YWovJdJ` 臂9）。
- **数据集**：`insiders1` = **provisional**（维持；不判死、不 data_excluded、不封集）。单集路线四波最强 0.89，仍在 BE176 的 1.30 上限内；配对路线四波皆负或平、sub 从未 ≥1.0。
- **塔位**：INSIDERS 10/10 臂归属（8 单塔 + 2 双塔），**实际点亮 0**。
- **提交链**：**未推进**（0 达标；prod/self 未测）。
- **下一步（按优先级）**：
  1. **先测 `LLKnekRL`（臂1）与 `Jj8nlbpW`（臂7）的 prod/self**：臂1 是四波最高 F + 最高 margin + 次高 S（且无分组、结构最简）；臂7 是 2Y 最高 + sub 过闸 + DD 次低。两条都是"离闸只差 S/2Y"的类型，**prod 雷在核心不在搭档**，先测这两条比继续扫参更省。
  2. **把"ts_ir 66 窗"做成单变量族**：固定分组，只扫 22 / 66 / 132，把 ask 的衰减梯判据补齐；同时补"分组 vs 无分组"在 66 窗上的对照（本波只在 252 窗测过分组）。
  3. **事件条件（臂10）单独拆解**：补 `vec_count==1` 分支与"仅按长侧子集"对照，分离"多笔日信息"与"长侧变薄"两种解释；在此之前**不得**把 sub 0.68 当作 ★v2 的进展证据。
  4. **若要继续单集路线，只剩 D2 一条**：补测 `insd1_price` / `insd1_value` / `insd1_tradesignificance`（三波都没碰过，只有族级先验），并同步跑第二套配置（decay4/nanOFF）补齐 D6 —— 两者齐备后六维全达，才可做数据集级终态裁决（当前实质"差一步"，但**不得**提前下结论）。
  5. **配对路线换搭档**：institutions6 四波证明它保不住 sub；平台已验证能保 sub 的是 MODEL（1.49/1.51，非 `insd1_*` 原生几何），**是否允许 MODEL 作搭档腿需用户裁定**（「已点亮塔不选」口径的边界）。
  6. **不要再用**：`trade_when(…, −1)`（w3 实证 S −0.40）、有符号斜率 `reverse(group_zscore(…))`（本波 S −0.44）、硬 `if_else(…, 0.5)` 的"低带更强"结论（四波证明是形态产物）。
