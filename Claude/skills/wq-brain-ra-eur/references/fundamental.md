# EUR × fundamental（组合分支）

> 回到 [EUR 区域流程](../SKILL.md) · [EUR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/EUR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region EUR --category fundamental`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 full-coverage）　**分组**：Fundamental　**类别卡**：fundamental

**备注**：EUR 破 prod 墙的残差化路径：★ 'vector_neut' **平台可用**（2026-10-20 平台二次核实：wave291 整批 8 条含 vector_neut×3 被 create_multi_simulation 接受；JjQmx9nm 已 ACTIVE 交付）⇒ 2026-10-10「op-lint 判定平台已移除」是**本地算子清单假阳性**（research-data/operators_platform_*.json 不含该算子），该结论作废。残差化四选一：vector_neut（首选，prod 最优）/ ts_regression / group_neutralize / subtract(rank,rank)；残差轴的选择仍决定成败 ★ 当前主力：fundamental72 VECTOR CFO/TA 冠军族（7 颗已验证，prod 0.6585–0.6747 / self ≈0.50）；MATRIX 载荷与 sector / market 轴是 prod 墙。

**涉及数据集**：fundamental17、fundamental23、fundamental93、other401、fundamental72、fundamental90、fundamental1

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | EUR | 区域 settings.json |
| universe | TOPCS1600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | ON | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 41 | 2 | 6 | 0 | 7 | 0 |

主要数据集（回测数）：fundamental23（18）、fundamental17（14）、other401（9）

### S1 字段理解

- 低频字段窗口取 66 / 252，补覆盖用 ts_backfill(·, 66)（季频）或 252（年频）（决策表 D5 / D6）
- 比率型信号的分母口径往往决定 self / prod 与 2Y——先看分母
- 窗口（类别卡，均在白名单内）：quarterly 66/252；annual 252/504

### S2 生成

- **用**：嵌套残差化：先削自由现金流，再削投资（CAPEX）或经营现金流维度（WorkBuddy MEMORY §1.7）
- **用**：★ 冠军配方（EUR fnd72，7 颗已验证：rKd5lAo8 / leM88RN5 / KPmOOwZx / vROkA5nw / P0MZ5nrp / pwvPanJx / akVLzLV1）：'ts_target_tvr_decay(trade_when(greater(vec_avg(<盈利质量A>), vec_avg(<盈利质量B>)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.06~0.24)' —— S 1.58–1.64 / F 1.07–1.14 / 2Y 1.68–1.83 / prod 0.6585–0.6747 / self ≈0.50。**恰好 9 个调用点（闸1b-2 上限 9，无余量）**：只能换算子 / 换轴 / 换 tvr 档 / 换载荷，不能加算子
- **说明**：ts_backfill 在 EUR / TOPCS1600 / nanHandling=ON 下是 no-op：写 EUR 表达式先删它；但 /assets 归一化是真信号，残差轴也要归一化
- **说明**：hump 必须写命名参数（hump=k）；hump(vec_avg(x), …) 会 FAIL
- **说明**：★★ 'vector_neut' **平台可用**（2026-10-20 复核：本地 'research-data/operators_platform_*.json' 不含该算子 = 本地清单假阳性；平台侧 wave291 整批 8 条含 vector_neut×3 被 create_multi_simulation 接受，JjQmx9nm 已 ACTIVE 交付）⇒ 2026-10-10「op-lint 判定平台已移除」的结论作废，残差化首选仍是 vector_neut。其它可用残差化：ts_regression(y,x,d,rettype=0) / group_neutralize(x,group)（内层须细于 setting 的 SUBINDUSTRY）/ subtract(rank(A),rank(B))（合规放行形态）
- **说明**：★★★ 【三层闸门口径差异·实测样本】EUR fnd72 'mL617YPx'（2026-10-11）：**平台 review 闸全过**（S1.82/F1.25/TO0.0675/**2年 ladder 2.23**/margin17.6bp/Failed RA=0/prod0.5421/self0.3999），但 **skill Phase C 判 REJECT**（近 **3年** CV_Sharpe 0.661 / max-min 5.26）。★ 差异点：**平台看 2 年窗口，skill 看近 3 年波动性** —— 该腿 2021 年异常高（3.63）拉大 CV。★ repair 2 轮实证（16 条变体）：'target_tvr' 0.06→0.30 仅改善 CV 0.020（饱和于 0.641）；max/min 可从 5.26 修复至 **4.63**（tvr=0.10）；**CV 属结构性，参数层不可弥合**。⇒ **选腿先验：若某腿单年 Sharpre 异常突出（如 2021），它会被 skill Phase C 拦，应优先找年度分布均匀的腿**。
- **说明**：★★ prod 墙是「表达式 × 设置档 × 轴」**三维**，不是表达式单独决定：同族在 maxTrade ON / decay 4 下 tvr 0.017、prod 0.79–0.81；在 decay 1 / maxTrade OFF 下 tvr 0.068–0.089、prod 0.66 ⇒ **turnover 是判别指纹**。任何结构上强的表达式必须先在冠军设置档重跑再判 prod（wave304 vs 301/305/306 同族对照）。
- **说明**：★ MATRIX 载荷族（'fnd72_s_*'，+ 'bs_a' MATRIX 口径）**双轴皆 prod 墙**：industry 0.7968（6XArAz1E）、subindustry **0.7870**（bl8RalWK，S2.00/2Y1.67/F1.57 全闸过、tvr 仅 0.0154）⇒ 该族是慢信号席位，指标再漂亮也不可交付；不要再在 MATRIX 载荷上换轴。
- **说明**：★ EUR group_zscore 合法轴只有 industry / sector / subindustry / market / country；**sector（prod 0.7553–0.7571）与 market（0.7805）是 prod 密墙**，industry 是唯一破墙轴（0.6585–0.6747）；subindustry 对 VECTOR 载荷抬 prod、country 轴 failRA=1。
- **说明**：★ 闸1b-2 调用点 <10（合法 ≤9）。'target_tvr' 是命名参数、decay / maxTrade / 中性化 / truncation 是设置，二者都不占调用点预算 ⇒ 补丁只能落在「换轴 / 换 tvr 档 / 换算子 / 换载荷」四类上。
- **说明**：★ prod-sat 闸按（字段集 + 轴 + 归一化）**三元组**匹配且不可豁免：VECTOR + industry + group_zscore 未饱和；VECTOR + sector 与 MATRIX + industry 已饱和。换 tvr / 换闸字段不会命中三元组。
- **说明**：★ 'quantile' 归一化首次实测即本族最强单点（wave306 P0MZzZMW：S 1.82 / F 1.43 vs group_zscore 1.64/1.14），但 2Y 1.52 差线 0.06 ⇒ **quantile + 更高 target_tvr 是既定 2Y 杠杆**（wave307 已开）。
- **说明**：★ 归一化毒药三件：group_neutralize（CFO/TA 上 CONCENTRATED_WEIGHT）、group_rank（S 1.27–1.5）、normalize（CW 0.2477）；FCF 率 subtract 形态（(CFO−CAPEX)/TA）tvr 1.28、S −0.01 全崩。
- **说明**：★ 本族 decay 必须 1（decay 4 使 2Y 1.77→1.18）；maxTrade 必须 OFF（ON 同时压 S 与 tvr ⇒ 抬 prod）。已在 dataset_overrides.fundamental72 钉住。
- **说明**：★ CFO/TA 同族互相关 0.948–0.991 ⇒ **整个 tvr 阶梯只算一个席位**；组合分散必须换经济概念（EBITDA/TA 毛利资产比、CAPEX/TA 投资异象）或换数据集。
- **说明**：★ 处女地（从未开波）：**fundamental28（1605 字段）/ fundamental6（279 字段）**；fundamental72 仍有 876 字段中约 870 未覆盖。
- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：

  ```text
  vector_neut(vector_neut(reverse(rank(divide(FCF_fin, assets))), rank(divide(free_cash_flow, assets))), rank(divide(operating_cashflow, assets)))
  vector_neut(vector_neut(vector_neut(rank(A),rank(B)),rank(C)),rank(D))  # A/B/C/D = 平台原生 scale-free 字段（mpns/ppgs/ppos/kcqs/rucs/sebv/sedv/iabs/iads/fbbs/fbds/pbts/rtes/mtps/1spdd）
  ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebit), vec_avg(fnd72_pit_or_is_a_net_income)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.06)
  ```

  - vector_neut(vector_neut(reverse(rank(divide(FCF_fin, assets)… ← 2 层嵌套 prod 0.6997 过线（WorkBuddy MEMORY §1.7）；★ 2026-10-20 更正：12 次算子调用**过不了闸 1b-2**（gate.py MAX_OP_CALLS=10 ⇒ 合法 ≤9），且其 fam3 'vector_neut→vector_neut→reverse' 实测 n=4、prod 0.9789 / 0.9859 / 0.9998 / 0.9998 = **DEAD** ⇒ 只作历史证据，不再作首选
  - vector_neut(vector_neut(vector_neut(rank(A),rank(B)),rank(C)… ← ★ 当前首选：depth-3 / 4 叶 / per-leg rank / 无 divide = 7~8 次调用（闸 1b-2 预算内）。fam3 = 'vector_neut→vector_neut→vector_neut'，n=1 prod 0.6695 = EUR 当前唯一 <0.7 的深度（JjQmx9nm，ACTIVE，S1.73 / F1.17 / 2Y2.10 / prod0.6695 / self0.3807）<!-- from config.prod_corr_max -->。★ per-leg 'rank' 必需：wave290 同几何去掉 rank 改用 divide（8 调用）10 条 S 0.16–1.14 全灭 ⇒ 量纲不齐即崩塌
  - ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_… ← 9 调用点。EBIT>NI 闸是该闸族最优；tvr 0.06 → vROkA5nw（S1.58/F1.08/2Y1.68/prod0.6663/self0.5270）。同骨架 tvr 0.09 ⇒ P0MZ5nrp(0.6653)、0.12 ⇒ pwvPanJx(0.6595)、0.15 ⇒ akVLzLV1(0.6585/2Y1.83)。闸替换：EBITDA>CFNI（rKd5lAo8 0.6747）、EBIT>CFNI（leM88RN5 0.6701）、EBITDA>NI（wave307 新探）。CFO>NI / OPINC>NI 闸摧毁信号（S→0，不得用）
- **类别通用原语**（类别卡，跨区）：
  - accrual / cash gap: earnings quality, not the earnings level
  - leverage change: delta of debt or interest burden
  - efficiency: turnover or incremental margin, not the stock of assets
  - invert value only as a residual after industry neutralization
  - asset growth: delta of total assets vs revenue growth (efficiency)
  - margin trajectory: gross margin change vs operating margin change
  - capital allocation: capex vs depreciation (growth vs maintenance)
- **跨区结论**（KOR/EUR；conflict）：换分母在 KOR 是破 self / prod 墙的主杠杆，在 EUR 是毒药——不作类别级规则，按组合取用（证据：KOR other466 只换分母 self 0.7422→0.6244、prod 0.8061→0.6843；EUR value_investment 换分母 S 0.10 全灭（WorkBuddy MEMORY §1.2 / §1.7）） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（USA/KOR；negative）：慢变的经典基本面单因子（value / quality / book 及其线性变体）判死或 prod 饱和（证据：USA seed basics 全族死、book/value 145 颗同族 ACTIVE；KOR 慢变基本面族 fnd86/89/93/f21 四连死） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(fundamental_score)（必须 group_neutralize 或 group_zscore）
- **禁止**（类别卡）：禁止使用加权混合（0.4*rank(A) + 0.6*rank(B)）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize / vector_neut）入场（★ 2026-10-20 更正：'vector_neut' **平台可用**——本地算子清单缺它是假阳性，EUR 平台已用它交付 JjQmx9nm；'regression_neut' 仍非平台算子名）
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [组合] 降 prod 换维度而不是加层：同维度加层边际几何衰减（0.9073→0.7432→0.7071→0.6997），换到投资维度（CAPEX / 资产）一次降 0.029（证据：WorkBuddy MEMORY §1.7（2026-10-04）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
2. [组合] 替换优于叠加，且顺序敏感：2 层 fcf→capex（9 算子）prod 0.6708 < 3 层 fcf→ocf→capex 0.6776（证据：WorkBuddy MEMORY §1.7；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
3. [组合] hump 档位降 prod 最强（0.0012→0.01：0.686→0.568），可用窗口约 0.0012–0.0035；只能在该族尚无提交时用，否则 self 爆（证据：wave273 / wave274（WorkBuddy MEMORY §1.7）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
4. [组合] prod 与 2Y 的**双免费杠杆** = 'target_tvr'（命名参数）：同族 tvr 0.06→0.09→0.12→0.15 使 prod 0.6747→0.6624→0.6595→**0.6585**、2Y 1.78→1.80→1.80→**1.83**、S 稳在 1.58–1.64 ⇒ 提 tvr 同时改善两端，是本族唯一不需要换算子的免费升级；已外推 0.18/0.21/0.24（wave307）（证据：wave301/302/305/306（rKd5lAo8 → KPmOOwZx → pwvPanJx → akVLzLV1）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
5. [组合] 结构性强的表达式先在**冠军设置档**（decay 1 / maxTrade OFF）重跑再判 prod：maxTrade ON ⇒ tvr 0.017 / prod 0.79–0.81；OFF ⇒ tvr 0.068 / prod 0.66。turnover 是判别指纹 —— 看到 tvr < 0.03 就别按 prod 判死，换档重测（证据：wave304（maxTrade ON）vs wave301/305/306（OFF）同族对照；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
6. [组合] 归一化算子是本族最强的单点换算子：'quantile' 替 'group_zscore' 使 S 1.64→1.82、F 1.14→1.43（2Y 1.78→1.52 需配更高 tvr 补回）；反之 group_rank / normalize / group_neutralize 全部劣化或触发 CW（证据：wave306 P0MZzZMW（quantile）/ leM8G8M2（normalize, CW 0.2477）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
7. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
8. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- **不要用**：换分母：在 EUR 是毒药（value_investment S 0.10 全灭）（WorkBuddy MEMORY §1.7） <!-- lint:const-ok 证据原文 -->
- **不要用**：削应计 / ROA 维度：等于削信号本体（S 1.76→1.12）（WorkBuddy MEMORY §1.7） <!-- lint:const-ok 证据原文 -->
- **不要用**：慢化（ts_mean）：反而抬 prod（0.7071→0.7974）（WorkBuddy MEMORY §1.7） <!-- lint:const-ok 证据原文 -->
- **不要用**：ts_target_tvr_hump：只对齐换手、不降 prod（WorkBuddy MEMORY §1.7） <!-- lint:const-ok 证据原文 -->
- **不要用**：中性化切到 MARKET：IS 最高但 prod 涨到 0.7254（WorkBuddy MEMORY §1.7） <!-- lint:const-ok 证据原文 -->
- **不要用**：MATRIX 载荷族 'fnd72_s_*'（双轴皆 prod 墙）：industry 0.7968 / subindustry 0.7870（wave303 6XArAz1E；wave305 bl8RalWK（S2.00/F1.57 全闸过仍 prod 0.7870）） <!-- lint:const-ok 证据原文 -->
- **不要用**：sector 轴（prod 0.7553–0.7571）与 market 轴（0.7805）（wave305 E5VvwZer / gJWQMx9v / 1Yjxxn2m） <!-- lint:const-ok 证据原文 -->
- **不要用**：group_neutralize（CFO/TA 上 CONCENTRATED_WEIGHT）与 group_rank（S 1.27–1.5）（wave301 / wave302） <!-- lint:const-ok 证据原文 -->
- **不要用**：normalize() 归一化（CONCENTRATED_WEIGHT 0.24771，S 1.41 差线）（wave306 leM8G8M2） <!-- lint:const-ok 证据原文 -->
- **不要用**：FCF 率 subtract 形态 (CFO−CAPEX)/TA：tvr 1.2816、S −0.01、failRA 6 全崩（wave306 RRAVzVAz） <!-- lint:const-ok 证据原文 -->
- **不要用**：fundamental1 董事会流失率族（director_attrition_ratio_2 / fnd1_filtered_attrition3yr）：longCount 4 / shortCount 4，数据集不可用（wave306 1YjxKlMK / N1eQzJYo） <!-- lint:const-ok 证据原文 -->
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region EUR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| EUR-FND23-ACCRUAL-EXPENSE-DEAD | fundamental23 应计质量/费用结构族 | Leave fundamental23 应计质量/费用结构族 in EUR。accrual anomaly 在 EUR D1 无效（与美股文献结论相反，勿再按美股经验搬）。本 session 已在 fundamental23 累计 4 个正 | fundamental23 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-FND23-CAPSTRUCT-DIVIDEND-DEAD | fundamental23 资本结构/杠杆族 + 股息族 | Leave fundamental23 的资本结构与股息族在 EUR。已验证「高覆盖 × 零竞争」字段也不产生信号，故不必再在 fundamental23 内部按 coverage/userCount 筛选——该筛选维度已证伪。换概念必须离 | fundamental23 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-FND23-WORKINGCAP-INVENTORY-DEAD | fundamental23 营运资本/存货效率族 | Leave fundamental23 营运资本/存货族 in EUR。本 session 已在 fundamental23 累计 5 个正交概念 28 式全灭（税务会计质量 / 资产负债表杠杆 / 股东回报 / 费用结构应计 / 营运资本 | fundamental23 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-FND93-TAXACCRUAL-ZERO-SIGNAL-DEAD | fundamental93 Earnings Tax Data（递延税/税务应计族） | Leave fundamental93 in EUR。开波前先用 4 式探针预算判定，不要直接开 10 式波。fitness 1.0 在本集数学上不可达（returns 天花板 0.016 vs 需求 0.05），不要试图用衰减/窗口/分组 | fundamental93 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-OTHER401-WEAK | other401 基本面矩阵族（oth401_* 65 字段 MATRIX） | wave235 9 探针全灭：best sharpe 0.70 / fit 0.34 / 2Y 1.07，CONCENTRATED_WEIGHT+LOW_ROBUST_UNIVERSE；D4 资格线 1.25 未达 → 判死。1 条 gro | other401 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-W251-FUNDAMENTAL17-QUALITY-PROBE | fundamental17 operating-quality changes and matched levels | Do not parameter-expand these 12 mechanisms/settings. Deferred untested variants are not empirical dead ends; reopening  | fundamental17 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-W252-FUNDAMENTAL17-MEASUREMENT-RETEST | fundamental17 reported earnings level and accounting adjustm | No parameter expansion of these weak expressions. Retain profitability-level research lead; entire dataset and untested  | fundamental17 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
