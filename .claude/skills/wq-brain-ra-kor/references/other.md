# KOR × other（组合分支）

> 回到 [KOR 区域流程](../SKILL.md) · [KOR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/KOR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region KOR --category other`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Other　**类别卡**：other

**涉及数据集**：acquisition_model、equity_forum_data、insider_feats、kor、ml_factor_proj、other455、other496、other532

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | KOR | 区域 settings.json |
| universe | TOP600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 10 | 0 | 4 | 2 | 36 | 7 |

主要数据集（回测数）：other455（8）、other532（2）

### S1 字段理解

- 数据集名会骗人：必读字段 description；稀疏高 valueScore 是陷阱
- 窗口（类别卡，均在白名单内）：daily 5/22；quarterly 66/252

### S2 生成

- **避**：other455 n2v 网络嵌入全灭；other496 _t 时间戳陷阱；other553 分析师绝对值全灭（RULES §G）
- **类别通用原语**（类别卡，跨区）：
  - name the priced risk first; the operator is secondary
  - 先按字段 description 判断经济含义，再套对应类别卡的思路（例：KOR other466 是财务比率 → fundamental；IND other532 是 Barra 特质收益 → 残差反转）
- **跨区结论**（KOR/EUR/DEU/GBR；negative）：other455 网络嵌入（n2v）族（证据：KOR RULES §G；EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS；DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923；GBR 红榜） <!-- lint:const-ok 证据原文 -->
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region KOR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| KOR-ACQ-MODEL-DEAD | acquisition_model 收购概率 | 勿再挖 acquisition_model 收购概率/文本因子类信号；model170 隐含估值单独保留 | acquisition_model | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-ANALYST44-WEAK-SIGNAL |  | analyst44一致预期类字段在KOR信号强度不足，不再投任何变体 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-ANL10-MODEA-AGGRESSIVE-OVERFIT | mode_a_parameter_tuning |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-ANL10-NUMS-NEGLECTED-PREMIUM | neglected_firm_premium |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-ANL10-REVISE-VALUE-CEILING | analyst10 revise_value 修正幅度族 | KOR/SECTOR/TOP600 下 analyst10 revise_value 族禁止再挖（裸信号/组合/参数均判死）；如需 analyst 系信号，转向 innovation_score 净方向族（wave97 1号 sharpe  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-ANL10-TSRANK252-PRODWALL | prod_correlation_wall |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-E10-CLUSTER-SH-DEAD | E10 评级2+簇内SH 混合 (wave95) | 评级修正×SH 族已饱和(2 ACTIVE + 缓冲), 新候选必须先本地互相关矩阵确认 <0.7 再投入仿真 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-EPS-REVISION-SPREAD-PROD-FLOOR-0723 | eps_estimate_4wk_change x pv106 spread | 该族 prod 地板 0.7231（两腿 E5vql38G），四种解拥挤手段全部失败，无法降到 0.70 以下。 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-FND93-ACCRUALS-DEAD | signal_family | fnd93 全部字段判死，不再投任何变体 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-FND94-FORWARD-PROFITABILITY | signal_direction | fnd94 rt_capex_sales_q/rt_psales_q/rt_net_mgn_q 等profitability族表达式必须reverse或subtract取反 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-FORUM-DEAD | equity_forum_data 论坛情绪/注意力 | 勿再挖 equity_forum_data 及同类论坛评论量/注意力信号; 事件流字段(CW 结构性集中)均需先验证 CW | equity_forum_data | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-FUNDAMENTAL89-ACCRUALS-DEAD | fundamental89 应计异象(Sloan accruals anomaly) | KOR TOP600下fundamental89应计异象族禁止再挖(裸信号/组合均判死); 慢变基本面质量因子在KOR无截面预测力, 转向分析师预期变化类或价格/量衍生信号 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-HEDGE3-Q4Q5-WHITESPACE-DEAD | short_horizon_hedge3 quantile4/5/confidence legs | only hedge3 quantile1_5d_pred usable (88lr21xo); do not reuse q2-q5/confidence legs | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-INSIDER-PROD-SATURATED | insider_feats 内部人交易信号族 | KOR insider_feats 信号族禁止再挖 (裸信号/字段组合/中性化/辅助信号均无法突破 PROD 0.7 硬闸); 如需内部人交易信号, 必须跨数据集混合且 PROD <0.7 | insider_feats | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-ML-FACTOR-PROJ-DEAD | ml_factor_proj change- fundamentals | do not probe fundamental change-family datasets in KOR | ml_factor_proj | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-MLPROJ-RATING-SH-SATURATED | ml_factor_proj 评级修正×短周期混合族 | 评级修正×短周期混合族变体空间已挖尽: 新变体与已提交 88lr21xo/A1lb2KpR 及 production book 相关>0.7 提交必 FAIL PROD_CORRELATION; 不再扫该组合变体 | ml_factor_proj | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-MODEL219-QUALITY-DEAD | model219 盈余质量/前瞻估值族 | 下次 model219 不投入慢变基本面族; 可留作评级修正类的分组器候选 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-MODEL313-DEAD | model313 knowledge capital | do not probe knowledge capital datasets in KOR again | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-NEWS79-SENTIMENT-DEAD | news79 event-stream sentiment | news sentiment event fields unusable with decay4 daily aggregation on KOR; would need event-anchored persistence design  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-OTH496-AFTERCONS-MODEA-CEILING | aftercons_percentage | other496 aftercons_percentage 族参数层天花板确认（decay=2/窗口5/22/66/组合腿/双信号全灭），不再投任何变体 | other496 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTH496-RETURN-WEAK | pure_return_signals | oth496 纯收益字段（returns2/4/10/20/60/250/252）在 KOR/D1 仅有微弱短期反转，与平台动量/反转族高度同质，不再投入新变体。 | other496 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTH496-TIMESTAMP-TRAP | field-semantics | oth496_returns*_t 字段是时间戳（Timestamp，cov=1.0）不是收益变换；凡 description 含 'Timestamp for' 的 _t 字段一律不得作为信号输入；信号只能用 returns2/3/4/1 | other496 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER455-GROUP-CLUSTER-DEAD | other455 GROUP cluster 分组器 | GROUP cluster 作分组器包裹评级修正削信号: 簇内同质化后 alpha 被平均, 簇内排名相对全网 rank 无增量; 不再投入 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER455-NETWORK-EMBEDDING-DEAD | other455 network embedding PCA MATRIX | KOR OTHER 不再重复 other455 n2v/roam MATRIX pca_fact*_value 探针; 若再攻仅剩 GROUP cluster 字段(vec_*包裹) 或与已验证金矿(评级修正/model170)跨数据集混合 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER455-RELATION-EMBED-DRIFT-NOSIGNAL-20261004 | supply_chain_graph_embedding_drift | 图嵌入 PCA 分量（*_pca_fact*_value）不可作 alpha 输入：符号随 PCA 对齐随机翻转，绝对水平无经济含义，时序漂移亦无横截面预测力。KOR 已验证。若日后重试需换非 PCA 的连续 latent score 且先 | other455 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER455-REVISION-CLUSTER-DEAD | other455 prediction x rating revision | 评级修正(change_6m_rating_revision)为腿的任何 other455 混合族禁止再挖, 与 ACTIVE 88lr21xo/A1lb2KpR 同族 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER553-ABSOLUTE-DEAD |  | other553绝对值类分析师预期字段在KOR判死，不再投任何变体 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-PV106-COST-DISPERSION-COVERAGE-DEAD | pv106 transaction_cost_maximum/median dispersion | KOR 不再尝试 transaction_cost_maximum/median 作为主信号。配非稀疏腿后 longCount 恢复到 283-322，但 sharpe 也只有 0.52-0.72——稀疏信号被稀释后无贡献。 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-PV30-NO-SIGNAL |  | pv30行业聚类标签数据集在KOR判死，无数值信号字段 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-PVDOM-SECTOR-VARIANTS-SATURATED | gvm+pv20 sector-wrapped recipe variants | Do not mine variants of the wpjJK60l recipe; sector skeleton remains reusable only with non-gvm/pv signal sources | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-RISK88-SEMI-ANALYST-CEILING |  | risk88慢腿+analyst16快腿组合在KOR SECTOR中性化下S≤1.42，不再投参数变体 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-SHORTINTEREST3-DEAD | shortinterest3 borrow/lending data | KOR securities-lending data at rate-bin granularity is unusable for cross-sectional factors; do not re-mine shortinteres | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-SUBINDUSTRY-PROD-SATURATED | neutralization | KOR区域REV1类信号禁用SUBINDUSTRY中性化；prod安全设置是STATISTICAL或SECTOR | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-VALUE-QUALITY-SEEDS | price_volume_quantile1_* / short_term_regime* 变体族（value/qual | KOR 85 个 value/quality 草稿全部勿再提交；区域隔离不解码风格因子 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-W182-FND93-ACCRUALS-NOSIGNAL-DEAD | fundamental93 应计/递延税/费用/负债比率 单信号(取负) | KOR fundamental93 判死(fast_kill 8探针无／S／>=0.5)。应计/递延税质量族在 KOR 无信号，与 GLB fundamental23 判死(慢信号 turnover 墙+无信号)跨区一致。fundament | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-WAVE104-FAMILY-CORR-DEAD | wave91c 配方家族快腿变体 | wave91c 配方家族 (评级修正 x SH 快腿) 已达扩展天花板, 不再做同族快腿变体; 需结构性差异化 (换慢腿族/换区域/换信号源) | kor | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| KOR-ANL10-SMARTEST-SP-TSRANK-INDGROUP | analyst_pred_surps |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-COMBO-LEG-CONSTRAINT | methodology |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-INSIDERS5-CLEAN-FAMILY-OPENED | insiders5 ownership level x pv106 spread |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-RATING-REV-SH-MIX-WIN | wave91c 跨数据集混合: 评级修正(ml_factor_proj) × short_horizon_hedge3_ | 慢变量 2y 金矿(评级修正 2.14) × 短周期低相关信号(SH) 混合三闸全过: 评级2+SH1 → 1.77/1.40/2y 2.52; 评级1+SH3 → 1.83/1.14/2y 2.34。与同周期慢信号(LT)混合全灭 | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-REV1-COMBO-WIN | combo_leg |  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-SHRT38-VALLEY-BREAKTHROUGH-20261004 | shortinterest38 净买入占比 × 窗口谷破 prod 墙 | 窗口微调 = 唯一只动 prod 不动 2Y 的旋钮。prod 直方图 [0.7,0.8) 桶 n=0 ⇔ 过线（12/12 精确）。amt net_buy/(buy+sell) 谷 W∈[408,480]；oth466 净利/资产谷也在  | kor | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-W113-PVDOM-SECTOR-WIN | wave113 grp_sec wpjJK60l: gvm(1x)+pv20(2x) blend wrapped gro | value_mom slow axis + price_volume_quantile1_20d_pred fast leg + expression-level group_neutralize(sector); sector strip | kor | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
