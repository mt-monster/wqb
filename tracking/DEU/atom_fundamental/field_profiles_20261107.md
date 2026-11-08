# DEU Fundamental 数据集字段画像汇总（2026-11-07，S1 存档）

> 战役：DEU Fundamental ATOM ×10（goal tg_dexhasu9e9mw5fln7m）。数据源：平台 get_datasets/get_datafields（DEU/TOP500/D1，filter_sharpe=false 全量），逐集原始目录存 tracking/DEU/atom_fundamental/fields/<ds>_fields.json。
> ⚠ 平台集级 coverage 多次证伪；本表覆盖率为字段级读数，「连续多年空窗」判死口径在探针回收后按 get_alpha_yearly_stats 实测补记。

## 一、数据集全景（平台 12 集，全部拉了字段目录）

| 数据集 | 名称/真实机制 | 字段数 | 类型 | 字段cov>0 | cov峰值 | users/alphas | 历史回测 | 状态 |
|---|---|---:|---|---:|---:|---|---:|---|
| fundamental45 | Systematic mining of earnings calls（电话会 NLP） | 12 | MATRIX:12 | 12 | 0.316 | 65/90 | **0** | **旗舰·全新未测** |
| fundamental90 | GAMES 质量/盈余管理模型 | 66 | MATRIX:66 | 0(平台) | 0 | 199/428(集级) | **0(4表达式未回测)** | **存在性探针待跑** |
| fundamental22 | ESG KPI value（描述错标 RIC 映射） | 1 | VECTOR:1 | 1 | 0.69 | 10/40 | 11(3 ra_clean) | 近闸复采 |
| fundamental6 | Company Fundamental（点时财务快照） | 196 | MATRIX:196 | 196 | 1.0 | 460/1077 | 26(0 过) | CLOSED（oiadpq 顶 1.73） |
| fundamental17 | FactSet Direct（季度报表） | 135 | MATRIX:135 | 0 | 0 | 636/1799 | 10(0 过) | 探针全灭 |
| fundamental89 | Accrual Earnings Model | 407 | MATRIX:407 | 0 | 0 | 199/428 | 20(0 过) | 探针全灭 |
| fundamental72 | S&P PIT 报表 | 1031(VECTOR684/MATRIX347) | 混合 | 0 | 0 | 152/286 | 10(0 过) | 探针全灭 |
| fundamental93 | Earnings Tax Data（税项应计） | 46 | MATRIX:46 | 0 | 0 | 24/41 | 8(0 过) | 探针全灭 |
| fundamental86 | Stock Reports Plus（综合评分） | 7 | MATRIX:7 | 0 | 0 | 93/178 | 10(0 过) | 探针全灭 |
| fundamental1 | 管理层/董事会画像 | 123 | VECTOR:123 | 0 | 0 | 56/80 | CLOSED（sum_tree REJECT） | 关闭 |
| digital_ad_spend | 广告投放情报 | 9 | VECTOR:9 | 0 | 0 | 5/5 | 0 | 低优先 |
| alpha_factor_lib | 因子库 | 65 | VECTOR:65 | 0 | 0 | 4/4 | 判死 | longCount 3/3 |

## 二、fundamental45 字段画像（旗舰，逐字段）

| 字段 | 类型 | cov | u/a | 语义（description） | 机制角色 |
|---|---|---:|---|---|---|
| fnd45_sentiment_lm2_net_qa | MATRIX | 0.2675 | 28/36 | LM2 模型 Q&A 段净情绪 | **主信号**：分析师拷问段语调（增量信息核心） |
| fnd45_sentiment_lm2_net_pr | MATRIX | 0.2675 | 4/6 | LM2 净情绪·陈述段（PR） | 主信号对照：管理层 prepared remarks |
| fnd45_sentiment_vader_net_qa | MATRIX | 0.2675 | 2/4 | Vader 净情绪·Q&A | 次级：跨模型一致性 |
| fnd45_sentiment_vader_net_pr | MATRIX | 0.2675 | 3/3 | Vader 净情绪·PR | 次级 |
| fnd45_score | MATRIX | 0.2675 | 16/18 | 复合总分（情绪+可读性+主题综合） | 聚合信号 |
| fnd45_readability_executives | MATRIX | 0.2675 | 7/8 | 高管发言可读性（复杂度） | 信息不透明度 |
| fnd45_numeric_perct_qa | MATRIX | 0.2675 | 7/7 | Q&A 数字 token 占比 | 信息具体度 specificity |
| fnd45_numeric_perct_pr | MATRIX | 0.2675 | 2/2 | PR 数字 token 占比 | specificity 对照 |
| fnd45_sentiment_chanage_ceo | MATRIX | 0.2393 | 2/2 | CEO 情绪变化 | 管理层语气动量 |
| fnd45_sentiment_chanage_othr | MATRIX | 0.2576 | 4/4 | 其他高管情绪变化 | 对照腿 |
| fnd45_lda_bigram_pr | MATRIX | 0.275 | 14/14 | LDA 主题得分（PR bigram） | 主题显著度 |
| fnd45_mktcap | MATRIX | 0.3162 | 24/26 | 报告时点市值 | 辅助（bucket/规模） |

更新频率：季度事件节奏（电话会），回测后按 yearly stats 补实测；探针几何一律先 ts_backfill(66) 对齐事件日（论坛 FF45555 实证纪律）。

## 三、fundamental90 字段画像（存在性探针目标，cov 显示 0 需验证）

高用户字段：fnd90_qes_gamef_pscore(33u/41a 质量 P 分)、fnd90_game_cash_flow_coverage(26u)、fnd90_game_deferred_sal_chg(25u/44a 递延收入变化)、fnd90_qes_gamef_icfroe_5y(21u)、fnd90_qes_gamef_ohlson(14u O-score)、fnd90_game_inventory_chg(12u)。机制=质量/盈余管理/ distress 经典面（Piotroski/Ohlson/应计）。

## 四、S0 白名单与优先级
1. fundamental45 —— 唯一零回测真覆盖面，单集 ATOM 旗舰；
2. fundamental90 —— 从未真回测，2-6 条存在性探针；
3. fundamental22 —— 1 字段 VECTOR（ESG KPI），台账有 3 ra_clean 但未见高 S 行，补 2 条几何探针；
4. 其余 cov0 集 —— 探针已灭，不再投槽（除非 fnd45 面枯竭）。
