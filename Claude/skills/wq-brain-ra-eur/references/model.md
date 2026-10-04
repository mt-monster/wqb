# EUR × model（组合分支）

> 回到 [EUR 区域流程](../SKILL.md) · [EUR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/EUR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region EUR --category model`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：MODEL　**类别卡**：model

**涉及数据集**：ai_equity_alpha、ai_factor_transfer、analyst_earnings_ibes、analyst_revision_horizons、chart_cnn_alpha、global_seasonal_model、model193、model238、model264、model354、model36、model50、multi_horizon_alpha、multifactor_return_pred、other460、predictive_starmine、price_signal_dl、shortinterest6

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
| 156 | 3 | 4 | 4 | 67 | 3 |

主要数据集（回测数）：predictive_starmine（38）、shortinterest6（28）、model50（23）、global_seasonal_model（21）、model264（14）、other460（13）、chart_cnn_alpha（9）、price_signal_dl（5）

### S1 字段理解

- 分清分数水平与分位 / 概率标签：标签类在 GBR 2Y 崩（GBR-DLRISKFREE-LABEL-DEAD）
- 看字段 description 判断是不是别人做好的成品因子；成品因子的热门字段 prod 墙最硬
- 窗口（类别卡，均在白名单内）：level 22/66/252；change 5/22

### S2 生成

- **避**：model 族 62 条判死；库存 47 / 47 族 prod 不低于上限（EUR profile 2026-10-02）
- **说明**：历史胜绩机制「慢 MODEL 残差 × 快 PV」只许以条件 / 分组 / 残差入场；0.40 / 0.60 加权写法被闸 5 禁止（EUR profile）
- **类别通用原语**（类别卡，跨区）：
  - industry residual: group_zscore so the factor is not the sector bet
  - quality minus yield: a slow fundamental residual, not the raw score
  - invert only when the economic story is crowding or mean-reversion
  - never ship a lone rank(model_score) as a concept
  - model disagreement: ensemble variance across model outputs
  - regime conditional: model signal only in specific market regimes
- **跨区结论**（GLB/USA/EUR；negative）：成品模型分数的热门字段在多区撞 prod 墙（users 高的字段 prod 必超上限）（证据：GLB techindi_model predicted_first_quantile 系 qMNZX1o1 prod 0.7686（GLB profile）；USA mdl177 / book-value 145 颗同族 ACTIVE；EUR×model 62 条判死） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(model_score)（必须 group_neutralize 或 industry residual）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
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
| EUR-AEIBES-W125-OPERATOR-LEVERAGE-WEAK | analyst_earnings_ibes event-masked OHLCV × 未用算子族 | Leave analyst_earnings_ibes 这 8 个机制（规模桶内漂移残差/日内分歧/加速度门控翻转/量价确认度/执行压力残差/彩票需求/T-KB-01 单集跨周期）。不判死整个数据集——换手率方向有存活线索见 salvage | analyst_earnings_ibes | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AFT-OSC2-WEAK | ai_factor_transfer _2 oscillators/money-flow | Leave ai_factor_transfer. Next unused whitelist: global_seasonal_model non-return seasonal features. Do not deepen RelVa | ai_factor_transfer | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-ANALYST-REV-NOSCORE-WEAK | ai_equity_alpha analyst revision without vol/score | Do not occupy slots with AIEQ analyst-revision family without vol/score. Composite after still ／S／<0.6. | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-FORENSIC-ACCRUAL-MIX-PROD | ai_equity forensic+accrual mix dominant | Do not use forensic+accrual mix as dominant. Mode B must change AIEQ concept. | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-VOL-SCORE-PRODCORR | ai_equity_alpha financial_statement_volatility_factor / alph | Do not use financial_statement_volatility_factor or alpha_score as the dominant (weight>=0.6) leg. Wrappers/group/ts_av_ | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W50-QOC-LIQ-CLARITY-WEAK | ai_equity quality/opacity/unused liquidity/clarity x v_rev x | Do not occupy slots with earnings_quality, information_opacity, liquidity_buffer/asset_liquidity_score_2, business_clari | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W51-MOAT-UTIL-REPL-PSPAT-WEAK | ai_equity_alpha | Wave51 0.30/0.40/0.30 × v_rev/wedge: max S1.09 failed cheap gate; pspat volume/trend also weak; competitive slot ERROR | ai_equity_alpha | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W52-MARGIN-GROWTH-CASH-WEAK | ai_equity_alpha | Wave52 0.30/0.40/0.30 × v_rev/wedge: max S1.20 failed cheap gate | ai_equity_alpha | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W53-DEBT-VAL-YIELD-PHYS-WEAK | ai_equity_alpha | Wave53 0.30/0.40/0.30 × v_rev/wedge: max S1.02 failed cheap gate | ai_equity_alpha | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W54-DIV-YIELD-CORR-TVAL-WEAK | ai_equity_alpha | Wave54 0.30/0.40/0.30 × v_rev/wedge: max S1.18 failed cheap gate | ai_equity_alpha | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W55-SHTR-FDISP-FACC-FFLOW-WEAK | ai_equity_alpha | Wave55 0.30/0.40/0.30 x v_rev/wedge: max S1.20 failed cheap gate | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W56-BUYB-BUZZ-FIN-SIZE-WEAK | ai_equity_alpha | Wave56 0.30/0.40/0.30 x v_rev/wedge: max S1.35 failed cheap gate | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-AIEQ-W57-EQA-FCHG-PTB-DEBT-WEAK | ai_equity_alpha | Wave57 leftover AIEQ 0.30/0.40/0.30 x v_rev/wedge max S0.82. W50-W57 leftover path exhausted. | ai_equity_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ARH-PROFIT90D-GZSCORE-PROD | analyst_revision | IS Sharpe/Fitness pass but prod_corr 0.86>=0.7. Dominant profit90d 90d estimate-change is crowded. Do not Mode A clone t | analyst_revision_horizons | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ARH-PROFIT90D-PRIMARY-MIX-PROD | analyst_revision | Fitness 0.94 near gate but prod 0.95. Mixing primary_profit into profit90d does not dilute prod. Leave profit90d as domi | analyst_revision_horizons | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ARH-SIGNEDPOWER-COUNTRY-DECAY6 | analyst_revision | Same expression as YP7NQQLW (S1.38 F0.92 SUBINDUSTRY/4) drops to S1.13 under COUNTRY/6. Do not Mode A signed_power+COUNT | analyst_revision_horizons | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ARH-SURPRISE-PRIMARY-PROD | analyst_revision | Surprise×primary_profit has IS (S1.04 F0.71) but prod 0.95. Same crowding as profit90d mixes. Do not Mode A; only residu | analyst_revision_horizons | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ARH-SURPRISE-RESID-WEAK | analyst_revision surprise/primary residual | ts_av_diff/group_mean residual of surprise+primary killed IS vs wave34 surprise×primary S1.04. Best wpj5lVJp S0.48. Resi | analyst_revision_horizons | payload | <!-- lint:const-ok 证据原文 -->
| EUR-FCF-MINORITY-VALUE-MIX-PROD | multi_horizon FCF invert residual mixed with to-price value | FCF as minority mixed with other to-price/value fields does not break prod 0.7. np7n8Mgd S1.17 F0.69 2Y2.03 prod 0.8693  | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-FCF-PURE-INVERT-RESID-PROD | multi_horizon FCF invert industry residual dominant | IS S/F/2Y pass but prod 0.94 because pure FCF without heterogeneous dilution. Self vs Wj71Q12o 0.45 so not a clone of th | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-GSM-EVENT-WEAK | global_seasonal_model event flags | Leave global_seasonal_model. Do not mix PV. Do not use calendar constants or return-quantile fields. Next unused whiteli | global_seasonal_model | payload | <!-- lint:const-ok 证据原文 -->
| EUR-GSM-SAME-SRC-BUCKET-RATIO |  | confidence/prob 同源分桶置信度 divide 比值近乎常数零区分度；5d vs calendar_5d 变体同源相关；multiply(ts_zscore) 交互同源高相关 | global_seasonal_model | payload | <!-- lint:const-ok 证据原文 -->
| EUR-M193-NAMED-SLOW-INERT | model193 named MATRIX residual x v_rev/wedge | Do not reuse model193 high-coverage named fields as 0.30 slow legs with v_rev/falling_wedge. Do not Mode A the weights. | model193 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-M238-D1-RANK-COMBO-PROD | model238 d1 rank combos of screening/change/industry/country | Intra-dataset d1 rank combos do not beat wave26 single-field rank(mdl238_global_screening_rank) S1.32 F0.87. Best 1YwozL | model238 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-M238-UNCROWDED-ALIGN-INDREL-PROD | model238 uncrowded alignment / industry_relative / preferenc | Uncrowded m238 fields have IS but do NOT beat the change/screening prod ~0.89 wall. 9qX9pVKe industry_relative S1.34 F0. | model238 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-M354-VALUATION-YIELD-WEAK | model354 group valuation yield concepts | Leave model354 standalone valuation densify. Next unused whitelist: ml_factor_proj low-competition non-return MATRIX con | model354 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-M36-CREDIT-DEFAULTRISK-PROD | model36 credit / default_risk dominant | Credit/default_risk dominant not near-gate (max S0.96 F0.58) and prod 0.91>=0.7. Do not Mode A clone decay/neut. Next on | model36 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-M36-DEFAULTRISK-RESID-PROD | model36 default_risk residual | Industry residual lifts S to 1.04 vs naked 0.96 but Fitness still 0.58 and prod 0.86. ts_av_diff weaker. Leave MODEL cre | model36 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-CAPACQ-INVERT-RESID-PROD | multi_horizon capital_acquisition invert residual dominant | Do not use invert long_term_capital_acquisition_ratio_3 industry residual as dominant. Mode B must change field/concept. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-DEEPVALUE-INVERT-PROD | multi_horizon deep_value invert x common_gap_up | Do not Mode A deep_value invert. Do not submit prod>=0.7. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-ESTREV-INVERT-DILUTE-PROD | multi_horizon long_term estrev invert residual as minority | Salvage of EUR-MH-ESTREV-RESID-INVERT-CROWD failed. 0.30 invert x growth/FS killed IS (S~-0.08). 0.40 invert + 0.60 mid_ | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-ESTREV-RESID-INVERT-CROWD | multi_horizon long_term estimate_revision industry residual  | Has independent IS (／S／1.48, self vs Wj71Q12o 0.17) but the profitable invert aligns with model238 institutional crowdin | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-EV-EBITDA-3LEG-RN-PROD | multi_horizon EV rank / ebitda-to-EV x v_rev x wedge | Do not grind long_term_enterprise_value_europe_rank or ebitda_to_enterprise_value x v_rev x wedge. Mode B must change sl | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-FCF-INVERT-PROD | multi_horizon trailing FCF-to-price invert x common_gap_up | Do not Mode A FCF invert. Do not submit prod>=0.7. Leave FCF-to-price 2/3 aliases. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-FS-RANK-3LEG-PROD | multi_horizon FS rank residual x v_rev x wedge | Do not grind FS rank/strength x v_rev x wedge. Leave FS family as slow leg. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-FY2-INVERT-CROWD | multi_horizon invert FY2 three-month revision | Do not use invert FY2 revision as dominant. Same crowd as estrev invert. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-GROWTH-FLOW-3LEG-PROD | multi_horizon growth_flow_to_price residual x v_rev x wedge | Do not grind growth_flow_to_price x v_rev x wedge weights. Mode B must change slow field. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-INCOME-STMT-3LEG-PROD | multi_horizon income_statement_rank residual x v_rev x wedge | Do not grind income_statement_rank x v_rev x wedge. Leave OLL/income as slow leg. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-LEVERAGE-3LEG-VREV-WEDGE-PROD | multi_horizon leverage residual x v_reversal x falling_wedge | Do not grind leverage x v_reversal x falling_wedge weights. Mode B must change slow field or fast PV. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-LEVERAGE-INVERT-RN | multi_horizon mgmt leverage invert x common_gap_up | Do not Mode A leverage invert. Keep invert recipe on unused MH fields. Keep gJj1nxLM CONDITIONAL. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-LEVERAGE-RESID-DOMINANT | multi_horizon leverage industry residual as dominant | Do not use leverage residual as dominant. Wave41 slot5 uses it as 0.40 slow x PV. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-MGEFF-INVERT-GZ-PROD | multi_horizon invert management_efficiency gzscore | Do not use invert management_efficiency gzscore as dominant. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-MIDTERM-ESTREV-WEAK | multi_horizon mid_term estimate_revision | Horizon shift from long_term estrev residual (／S／1.48) to mid_term (alphaCount=0) failed. Best 88lOpzjm invert residual+ | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-NOA-PEG-WEAK | multi_horizon NOA change and PEG | Do not occupy slots with NOA or PEG probes. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-NREV-LADDER-WALL | multi_horizon_nrev | Wave49 Mode A/B: S/F tunable to pass; IS ladder / 2Y sharpe hard ceiling ~1.1-1.28; rn_sharpe weak | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-QUALITY-BS-EPS-WEAK | multi_horizon balance_sheet and price_adj_eps residual | Do not occupy another slot with BS or price_adj_eps residual probes. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-ROE-3LEG-WEAK | multi_horizon ROE residual x v_rev x wedge | Do not occupy slots with ROE residual x v_rev x wedge. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-VALUE-ANALYST-3LEG-PROD | multi_horizon value_analyst residual x v_rev x wedge | Do not grind value_analyst x v_rev x wedge. Mode B must change slow field. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-VALUE-COUNTRY-SALES-WEAK | multi_horizon country gz value and sales_to_price | Do not occupy slots with country-gz deep_value or sales_to_price. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MH-W49-UNUSED-3LEG-WEAK | multi_horizon PTA/street/nrev/pmom/rational_decay x v_rev x  | Do not occupy slots with PTA, street_revision FY1, nrev FY1, price_momentum, or rational_decay x v_rev x wedge. | multi_horizon_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-MODEL193-W129-CREDIT-AXIS-DEAD | model193 信用风险/CDS/困境轴 | Leave model193 的 CDS 利差波动/beta、破产风险(Altman Z / Ohlson)、违约概率、空头回补压力、现金流-稀释、ebitdaev-CDS 名义敷口全系。 | model193 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-ACTUAL-UPGDNG-ARMCOUNTRY-WEAK | starmine actual EPS/revenue and upgrade/downgrade and ARM co | new slows dilute winning surprise x gap mix | predictive_starmine | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-REC-SMEST-WEAK | starmine rec mean change / smest levels | Do not reuse recommendation_mean_change or smest levels as slow legs. Surprise last-year EPS may mix unused PV not v_rev | predictive_starmine | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-RELVAL-EVEBITDA-2Y-DEAD | starmine RelVal EV/EBITDA ts_delta × v_rev/wedge | Leave RelVal EV/EBITDA ts_delta family. Do not deepen v_rev/wedge on this slow. Do not clone FCF×gap. Next unused whitel | predictive_starmine | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-REVCOUNT-ARM-WEAK | starmine revision counts / ARM rec-activity | Do not reuse starmine revision counts or ARM rec/activity as slow legs. Do not deepen RelVal EV/EBITDA or v_rev/wedge. N | predictive_starmine | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STARHOLD-COUNTRY-RANK-PROD | shortinterest star_hold_country_rank dominant | Do not use star_hold_country_rank as dominant. | shortinterest6 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STARHOLD-INDUSTRY-RANK-PROD | shortinterest star_hold_industry_rank dominant | Do not use star_hold_industry_rank as dominant. Leave starhold rank family as dominant. | shortinterest6 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STARHOLD-SCREENING-GZSCORE-PROD | shortinterest | COUNTRY/6 wrapper lifts starhold to S1.39 F0.96 2Y1.45 but prod 0.89 and LOW_SUB 0.39. EUR/D1/MODEL crowded. Sibling E5l | shortinterest6 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STARHOLD-SCREENING-RESID-PROD | shortinterest residual of screening_rank | group_mean residual ≈ gzscore; still prod 0.85-0.89. ts_av_diff killed Sharpe (0.20-0.55). Do not Mode A clone residual  | shortinterest6 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STARHOLD-SECTOR-RANK-PROD | shortinterest star_hold_sector_rank dominant | Do not use star_hold_sector_rank as dominant. Do not Mode A decay/neut. Leave starhold sector/screening family. | shortinterest6 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-W254-OTHER460-FORWARD-PROBABILITY-PAIRS | other460 four target probability directions SUBINDUSTRY deca |  | other460 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-chart_cnn_alpha-LEAPSTAR-WEAK | chart_cnn_alpha leapstar6/malta2 image features | Leave chart_cnn_alpha leapstar6/malta2 in EUR. Do not retry ts_decay_linear/zscore on leapstar6 features or group_sum on | chart_cnn_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-chart_cnn_alpha-MODEB-CEILING | chart_cnn_alpha malta2 q3 × leapstar6 Mode B ceiling | Leave chart_cnn_alpha malta2 q3 × leapstar6 in EUR. Do not retry Mode B optimization on this combination; ceiling reache | chart_cnn_alpha | payload | <!-- lint:const-ok 证据原文 -->
| EUR-predictive_starmine-EQVR-WEAK | predictive_starmine eq_vr_dlra1 accruals/cashflow | Leave predictive_starmine eq_vr_dlra1 in EUR. Do not retry ts_mean/ts_delta on accruals/cashflow components. | predictive_starmine | payload | <!-- lint:const-ok 证据原文 -->
| EUR-predictive_starmine-SMEST-IV-WEAK | predictive_starmine smest/iv family | Leave predictive_starmine smest/iv in EUR. Do not retry ts_mean/ts_delta on smest_f12m or iv_cagr fields. | predictive_starmine | payload | <!-- lint:const-ok 证据原文 -->
| EUR-price_signal_dl-NO-DATA | price_signal_dl trend/volume indicators | Leave price_signal_dl in EUR. Do not retry any trend/volume indicator expressions. | price_signal_dl | payload | <!-- lint:const-ok 证据原文 -->
| EUR-shortinterest6-CHANGE-OWNER-WEAK | shortinterest6 change/owner component | change/owner 组件单独使用信号强度不足（IS 天花板 1.24），无法突破 EUR 硬闸；需回归 win recipe 结构 | shortinterest6 | payload | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| EUR-WIN-SLOW-MODEL-X-FAST-PV | 0.40 slow MODEL residual invert + 0.60 fast PV pattern inver | cross-pyramid mix; follow SUBINDUSTRY decay4; do not clone FCF+gap | — | keyword | <!-- lint:const-ok 证据原文 -->
| EUR-WIN-SLOW-MODEL-X-FAST-PV-3LEG | capacq residual x v_reversal x falling_wedge |  | — | keyword | <!-- lint:const-ok 证据原文 -->
| EUR-Wj71Q12o-slow-fast-mix | 0.4 slow MODEL residual + 0.6 fast PV | mix=0.4*slow_model_leg + 0.6*fast_pv_leg; neutralization=SUBINDUSTRY; decay=4; universe=TOP2500; delay=1 | — | keyword | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
