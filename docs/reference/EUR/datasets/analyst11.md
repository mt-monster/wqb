# analyst11 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst11` |
| 名称 | ESG scores |
| 类别 | ANALYST |
| 数据字段数(平台) | 445 |
| 覆盖率 | 0.8489 |
| 平台已有 alpha | 150 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RICs) and Bloomberg Identifiers (BBIDs), facilitating cross-platform security identification and data integration. By linking these two widely used financial identifiers, the dataset enables seamless aggregation and comparison of market data from Bloomberg and Refinitiv sources. This mapping is essential for portfolio managers, researchers, and trading systems that require accurate and efficient reconciliation of securities across different data vendors. While not directly predictive of price movements, the dataset is crucial for ensuring data integrity and consistency in multi-source financial analysis, which underpins robust quantitative research and trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **445** |
| 类型分布 | MATRIX×445 |
| 平均覆盖率 | **0.849** |
| 覆盖率区间 | 0.70 ~ 0.91 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 76 | 17.1% |
| 中 (0.70–0.90) | 362 | 81.3% |
| 低 (0.50–0.70) | 7 | 1.6% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 439 | 98.7% |
| DEAD | 6 | 1.3% |

- 已实测字段：**6** 个（1%），best_sharpe 最高 **0.43**，中位 -0.03

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 259 | 0.85 | anl11_greg_industryrnk、anl11_citreg_industryrnk、anl11_esgreg_industryrnk |
| 持仓与资金流 | 107 | 0.84 | management_ethics_standards_score_2、social_score_industry_position、social_score_sector_position |
| 风险与质量 | 53 | 0.85 | anl11_rocsopgse、anl11_2_gse、anl11_2_pme |
| 其他 | 19 | 0.84 | anl11_2g、anl11_1tic、anl11_2tic |
| 价量与波动 | 6 | 0.79 | social_totalcorr_sector_position、social_totalcorr_subsector_position、social_totalcorr_sector_percentile |
| 元数据与非信号 | 1 | 0.82 | anl11_company_name |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl11_rocsopgse` | MATRIX | 0.831 | 风险与质量 | 1 | 0.43 | — | — | DEAD | Composite score for ESG that weights E, EMP, CIT, and G scores based on their positive and negative correlations to key |
| 2 | `anl11_greg_industryrnk` | MATRIX | 0.906 | 宏观与行业 | 1 | 0.42 | — | — | DEAD | Rank within the industry peer group for the Governance (G) score, with 1 being the highest |
| 3 | `anl11_citreg_industryrnk` | MATRIX | 0.907 | 宏观与行业 | 1 | -0.03 | — | — | DEAD | Rank of company's CIT Score within its industry peer group, where 1 means highest rank |
| 4 | `anl11_2_gse` | MATRIX | 0.824 | 风险与质量 | 1 | -0.25 | — | — | DEAD | The ESG Score averages the E, S, and G scores. |
| 5 | `anl11_2_pme` | MATRIX | 0.810 | 风险与质量 | 1 | -0.31 | — | — | DEAD | The EMP score averages the three EMP scores. |
| 6 | `anl11_esgreg_industryrnk` | MATRIX | 0.909 | 宏观与行业 | 1 | -0.33 | — | — | DEAD | Rank of the company within its industry peer group based on ESG score, with 1 being the highest rank |
| 7 | `overall_sustainability_score_2` | MATRIX | 0.912 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall ESG Score for the company, calculated as the average of its Environmental (E), Social (S), and Governance (G) sc |
| 8 | `environmental_pillar_score` | MATRIX | 0.911 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall Environmental score for the company, computed as the unweighted average of E1, E2, and E3 metrics, representing |
| 9 | `social_pillar_score_2` | MATRIX | 0.911 | 风险与质量 | 0 | — | — | — | UNTESTED | Social score, calculated as the simple average of the CIT (Citizenship) and EMP (Employment) scores, with no subjective |
| 10 | `citizenship_pillar_score` | MATRIX | 0.911 | 风险与质量 | 0 | — | — | — | UNTESTED | The average score for Capital Investment KPIs CIT1, CIT2, and CIT3, representing overall capital investment performance |
| 11 | `governance_pillar_score` | MATRIX | 0.910 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite Governance Score, calculated as the average of G1, G2, and G3 scores for the entity, without applying subjecti |
| 12 | `pollution_prevention_score_2` | MATRIX | 0.909 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregated score for Pollution Prevention, reflecting how well the company is transitioning toward lower pollution based |
| 13 | `resource_efficiency_score_2` | MATRIX | 0.909 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregated score for Resource Efficiency, reflecting how well a company is reducing consumption (water, energy, etc.) an |
| 14 | `antipollution_policy_score` | MATRIX | 0.909 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregated score for Environmental Transparency, reflecting the quality of company’s environmental policies, reporting a |
| 15 | `management_ethics_standards_score_2` | MATRIX | 0.909 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Composite score for Management Ethics, summarizing company performance on integrating ethics, equitable stakeholder trea |
| 16 | `anl11_esgregsubsecrnk` | MATRIX | 0.909 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company within its subsector peer group based on ESG score, with 1 being the highest rank |
| 17 | `anl11_gse` | MATRIX | 0.909 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall ESG (Environmental, Social, Governance) score, calculated as the average of the E, S, and G scores |
| 18 | `anl11_knrtcesgergse` | MATRIX | 0.909 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company within its sector peer group based on ESG score, with 1 being the highest rank |
| 19 | `anl11_e` | MATRIX | 0.908 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall environmental (E) score, calculated as the average of E1, E2, and E3 scores |
| 20 | `anl11_ereg_industryrnk` | MATRIX | 0.908 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the Environmental (E) score for a company within its industry peer group, with 1 being the highest rank |
| 21 | `anl11_eregsubsecrnk` | MATRIX | 0.908 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company within its subsector peer group based on Environmental Score, with 1 being the highest rank |
| 22 | `anl11_knrtcesgere` | MATRIX | 0.908 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company within its sector peer group based on Environmental Score, with 1 being the highest rank |
| 23 | `social_pillar_score` | MATRIX | 0.908 | 风险与质量 | 0 | — | — | — | UNTESTED | Social (S) score for the company; calculated by simple average of CIT (Citizenship) and EMP (Employment) metrics, with n |
| 24 | `social_score_industry_position` | MATRIX | 0.908 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Social (S) score within its industry peer group; 1 is highest |
| 25 | `social_score_sector_position` | MATRIX | 0.908 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Social (S) score within its sector peer group; 1 is highest |
| 26 | `social_score_subsector_position` | MATRIX | 0.908 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Social (S) score within its subsector peer group; 1 is highest |
| 27 | `transparency_accountability_score` | MATRIX | 0.908 | 风险与质量 | 0 | — | — | — | UNTESTED | A composite KPI measuring Disclosure & Accountability, aggregating the quality of reporting on financial and sustainabil |
| 28 | `anl11_citregsubsecrnk` | MATRIX | 0.907 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of company's CIT Score within its subsector peer group, where 1 means highest rank |
| 29 | `anl11_knrtcesgertic` | MATRIX | 0.907 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of company's CIT Score within its sector peer group, where 1 means highest rank |
| 30 | `anl11_tic` | MATRIX | 0.907 | 风险与质量 | 0 | — | — | — | UNTESTED | Average of the CIT1, CIT2, and CIT3 scores for the company |
| 31 | `community_engagement_score_2` | MATRIX | 0.907 | 风险与质量 | 0 | — | — | — | UNTESTED | KPI measuring company contribution to communities, including charity, protection of public health, and balancing positiv |
| 32 | `anl11_g` | MATRIX | 0.906 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall Governance (G) Score, calculated as the average of G1, G2, and G3 governance metrics for the company |
| 33 | `anl11_gregsubsecrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the subsector peer group for the Governance (G) score, with 1 being the highest |
| 34 | `anl11_knrtcesgerg` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the sector peer group for the Governance (G) score, with 1 being the highest |
| 35 | `anl11_1e` | MATRIX | 0.906 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregate score for Pollution Prevention & Environmental Remediation for the company |
| 36 | `anl11_3e` | MATRIX | 0.906 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregate score for Energy & Resource Efficiency for the company |
| 37 | `anl11_e1reg_industryrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E1 KPI within its region-industry group (1 = highest rank) |
| 38 | `anl11_e1regsubsecrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E1 KPI within its region-subsector group (1 = highest rank) |
| 39 | `anl11_e3reg_industryrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E3 KPI within its region-industry group (1 = highest rank) |
| 40 | `anl11_e3regsubsecrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E3 KPI within its region-subsector group (1 = highest rank) |
| 41 | `anl11_knrtcesger1e` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E1 KPI within its region-sector group (1 = highest rank) |
| 42 | `anl11_knrtcesger3e` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E3 KPI within its region-sector group (1 = highest rank) |
| 43 | `anl11_2e` | MATRIX | 0.906 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregate score for Anti-Pollution Policies & Environmental Transparency for the company |
| 44 | `anl11_e2reg_industryrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E2 KPI within its region-industry group (1 = highest rank) |
| 45 | `anl11_e2regsubsecrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E2 KPI within its region-subsector group (1 = highest rank) |
| 46 | `anl11_knrtcesger2e` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company on E2 KPI within its region-sector group (1 = highest rank) |
| 47 | `human_rights_supply_chain_score_2` | MATRIX | 0.906 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite score indicating a company's performance and policies regarding human rights, including child/compulsory labor |
| 48 | `employer_pillar_score` | MATRIX | 0.906 | 风险与质量 | 0 | — | — | — | UNTESTED | The average score of Employment KPIs EMP1, EMP2, and EMP3, providing an overall, non-subjectively weighted employment sc |
| 49 | `anl11_2g` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator for management standards and ethics |
| 50 | `anl11_g2reg_industryrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G2 score within its region-industry peer group, with 1 being the highest |
| 51 | `anl11_g2regsubsecrnk` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G2 score within its region-subsector peer group, with 1 being the highest |
| 52 | `anl11_knrtcesger2g` | MATRIX | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G2 score within its region-sector peer group, with 1 being the highest |
| 53 | `anl11_region_industrycount` | MATRIX | 0.905 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of industries within the specified region |
| 54 | `anl11_regionsectcount` | MATRIX | 0.905 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of sectors within the specified region |
| 55 | `anl11_regionsubseccount` | MATRIX | 0.905 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of subsectors within the specified region |
| 56 | `anl11_3g` | MATRIX | 0.904 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator for disclosure, transparency, and stakeholder accountability |
| 57 | `anl11_g3reg_industryrnk` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of company within its industry peer group based on the G3 governance KPI, where 1 is the highest rank |
| 58 | `anl11_g3regsubsecrnk` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G3 score within its region-subsector peer group, with 1 being the highest |
| 59 | `anl11_knrtcesger3g` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G3 score within its region-sector peer group, with 1 being the highest |
| 60 | `board_independence_effectiveness_score` | MATRIX | 0.904 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite score for Board Effectiveness, aggregating policies and outcomes for board independence, diversity, effectiven |
| 61 | `anl11_1tic` | MATRIX | 0.904 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator for Community Engagement and Charitable Activities |
| 62 | `anl11_cit1reg_industryrnk` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within industry for CIT1 (Community Engagement & Charitable Activities), 1 being highest |
| 63 | `anl11_cit1regsubsecrnk` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within subsector for CIT1 (Community Engagement & Charitable Activities), 1 being highest |
| 64 | `anl11_knrtcesger1tic` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within sector for CIT1 (Community Engagement & Charitable Activities), 1 being highest |
| 65 | `anl11_cit2reg_industryrnk` | MATRIX | 0.902 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company within its industry peer group for the CIT2 KPI, with 1 being the highest rank |
| 66 | `anl11_cit2regsubsecrnk` | MATRIX | 0.902 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of CIT2 KPI within the region-subsector peer group, with 1 being the highest (best) |
| 67 | `anl11_2tic` | MATRIX | 0.902 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Human Rights Activism, Supply Chain, Labor & Human Rights Policies |
| 68 | `anl11_knrtcesger2tic` | MATRIX | 0.902 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of CIT2 KPI within the region-sector peer group, with 1 being the highest (best) |
| 69 | `anl11_empreg_industryrnk` | MATRIX | 0.902 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Score within its industry group, where 1 is the best/highest score |
| 70 | `anl11_empregsubsecrnk` | MATRIX | 0.902 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Score within its subsector group, where 1 is the best/highest score |
| 71 | `anl11_knrtcesgerpme` | MATRIX | 0.902 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Score within its sector group, where 1 is the best/highest score |
| 72 | `anl11_pme` | MATRIX | 0.902 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall Employment (EMP) Score, calculated as the average of the three EMP KPIs for the company |
| 73 | `sustainable_product_innovation_score` | MATRIX | 0.902 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite score indicating a company’s sustainability integration, aggregating data on evolving products, marketing, and |
| 74 | `workplace_diversity_score` | MATRIX | 0.902 | 风险与质量 | 0 | — | — | — | UNTESTED | KPI measuring workplace diversity, labor-management relations, and employee rights, focusing on building a diverse and f |
| 75 | `workplace_safety_training_score` | MATRIX | 0.901 | 风险与质量 | 0 | — | — | — | UNTESTED | KPI measuring workplace safety, worker training, and policies relating to employee health, productivity, and morale |
| 76 | `anl11_1g` | MATRIX | 0.900 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator for board independence, diversity, and effectiveness |
| 77 | `anl11_g1reg_industryrnk` | MATRIX | 0.900 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G1 score within its region-industry peer group, with 1 being the highest |
| 78 | `anl11_g1regsubsecrnk` | MATRIX | 0.900 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G1 score within its region-subsector peer group, with 1 being the highest |
| 79 | `anl11_knrtcesger1g` | MATRIX | 0.900 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's G1 score within its region-sector peer group, with 1 being the highest |
| 80 | `anl11_3tic` | MATRIX | 0.899 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator measuring Business Model & Products under the Citizenship pillar |
| 81 | `anl11_cit3reg_industryrnk` | MATRIX | 0.899 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's CIT3 score within its region-industry peer group, with 1 being the highest |
| 82 | `anl11_cit3regsubsecrnk` | MATRIX | 0.899 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's CIT3 score within its region-subsector peer group, with 1 being the highest |
| 83 | `anl11_knrtcesger3tic` | MATRIX | 0.899 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's CIT3 score within its region-sector peer group, with 1 being the highest |
| 84 | `anl11_2pme` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator for Employee Diversity Treatment and Labor Rights |
| 85 | `anl11_emp2reg_industryrnk` | MATRIX | 0.898 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the industry for EMP2 (Employee Diversity Treatment & Labor Rights), 1 being the highest in industry |
| 86 | `anl11_emp2regsubsecrnk` | MATRIX | 0.898 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the subsector for EMP2 (Employee Diversity Treatment & Labor Rights), 1 being the best in subsector |
| 87 | `anl11_knrtcesger2pme` | MATRIX | 0.898 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the sector for EMP2 (Employee Diversity Treatment & Labor Rights), 1 being the highest among sector peers |
| 88 | `anl11_3pme` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator for Employee Continuing Education, Training, Work Conditions, Safety & Health |
| 89 | `anl11_emp3reg_industryrnk` | MATRIX | 0.897 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the industry for EMP3 (Continuing Education, Training, Work Conditions, Safety & Health), 1 as highest |
| 90 | `anl11_emp3regsubsecrnk` | MATRIX | 0.897 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the subsector for EMP3 (Continuing Education, Training, Work Conditions, Safety & Health), 1 as highest |
| 91 | `anl11_knrtcesger3pme` | MATRIX | 0.897 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the sector for EMP3 (Continuing Education, Training, Work Conditions, Safety & Health), 1 as highest |
| 92 | `employee_satisfaction_score` | MATRIX | 0.896 | 风险与质量 | 0 | — | — | — | UNTESTED | KPI measuring employee compensation and satisfaction, including fair pay, benefits, and practices promoting productivity |
| 93 | `sustainability_industry_position` | MATRIX | 0.894 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its industry peer group based on the overall ESG score, with 1 being the best ESG score in th |
| 94 | `sustainability_sector_position` | MATRIX | 0.894 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its sector peer group based on the overall ESG score, with 1 meaning the highest ESG score in |
| 95 | `sustainability_subsector_position` | MATRIX | 0.894 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its subsector peer group based on the overall ESG score, with 1 being the top ESG performer i |
| 96 | `environmental_industry_position_2` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Environmental score within its industry peer group, with 1 being the highest score in the industry |
| 97 | `environmental_sector_position_2` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Environmental score within its sector peer group, with 1 denoting the highest score in the sector |
| 98 | `environmental_subsector_position_2` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Environmental score within its subsector peer group, with 1 being the highest rank in the subsecto |
| 99 | `social_industry_position_2` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Social Score within the industry peer group, 1 indicating top score in industry |
| 100 | `social_sector_position_2` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Social Score within the sector peer group, 1 indicating top score in sector |
| 101 | `social_subsector_position_2` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Social Score within the subsector peer group, 1 indicating top score in subsector |
| 102 | `citizenship_industry_position` | MATRIX | 0.892 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's overall CIT score within its industry peer group, with 1 as highest |
| 103 | `citizenship_sector_position` | MATRIX | 0.892 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's overall CIT score within its sector peer group, with 1 as highest |
| 104 | `citizenship_subsector_position` | MATRIX | 0.892 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's overall CIT score within its subsector peer group, with 1 as highest |
| 105 | `anl11_1pme` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Aggregate key performance indicator measuring company’s Compensation and Employee Satisfaction |
| 106 | `anl11_emp1reg_industryrnk` | MATRIX | 0.892 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the industry for EMP1 (Compensation & Employee Satisfaction), 1 being the highest in industry |
| 107 | `anl11_emp1regsubsecrnk` | MATRIX | 0.892 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the subsector for EMP1 (Compensation & Employee Satisfaction), 1 being the best in subsector |
| 108 | `anl11_knrtcesger1pme` | MATRIX | 0.892 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the sector for EMP1 (Compensation & Employee Satisfaction), 1 being the highest among sector peers |
| 109 | `governance_industry_position_2` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Industry Peer Group on the G Score with 1 being the highest rank |
| 110 | `governance_sector_position_2` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Sector Peer Group on the G Score with 1 being the highest rank |
| 111 | `governance_subsector_position_2` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the SubSector Peer Group on the G Score with 1 being the highest rank |
| 112 | `pollution_prevention_industry_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its industry peer group on the Pollution Prevention (E1) KPI, where 1 is highest |
| 113 | `pollution_prevention_sector_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its sector peer group on the Pollution Prevention (E1) KPI, where 1 is highest |
| 114 | `pollution_prevention_subsector_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its subsector peer group on the Pollution Prevention (E1) KPI, where 1 is highest |
| 115 | `resource_efficiency_industry_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its industry peer group based on the OWL E3 KPI, where 1 is the highest rank |
| 116 | `resource_efficiency_sector_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its sector peer group on the Resource Efficiency (E3) KPI, where 1 is highest |
| 117 | `resource_efficiency_subsector_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its subsector peer group based on the OWL E3 KPI, where 1 is the highest rank |
| 118 | `antipollution_policy_industry_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its industry peer group on the Environmental Transparency (E2) KPI, where 1 is highest |
| 119 | `antipollution_policy_sector_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its sector peer group on the Environmental Transparency (E2) KPI, where 1 is highest |
| 120 | `antipollution_policy_subsector_position` | MATRIX | 0.891 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Company's rank within its subsector peer group on the Environmental Transparency (E2) KPI, where 1 is highest |
| 121 | `management_ethics_industry_position` | MATRIX | 0.890 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's G2 Management Ethics KPI within its industry peer group, with 1 being the highest rank |
| 122 | `management_ethics_sector_position` | MATRIX | 0.890 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's G2 Management Ethics KPI within its sector peer group, with 1 being the highest rank |
| 123 | `management_ethics_subsector_position` | MATRIX | 0.890 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's G2 Management Ethics KPI within its subsector peer group, with 1 being the highest rank |
| 124 | `anl11_creptcesgergse` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company within its sector peer group based on ESG score, with 100% being the best |
| 125 | `anl11_esgreg_industryperc` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company within its industry peer group based on ESG score, with 100% being the best |
| 126 | `anl11_esgregsubsecperc` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company within its subsector peer group based on ESG score, with 100% being the best |
| 127 | `sustainability_industry_percentile_score` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's ESG score within its industry peer group, with higher percentiles representing bette |
| 128 | `sustainability_sector_percentile_score` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's ESG score within its sector peer group, with higher percentiles indicating better ES |
| 129 | `sustainability_subsector_percentile_score` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's ESG score within its subsector peer group, with higher percentiles indicating better |
| 130 | `anl11_creptcesgere` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the Environmental (E) score for a company within its sector, with 100% being the best |
| 131 | `anl11_ereg_industryperc` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental (E) score within its industry peer group (100% is best) |
| 132 | `anl11_eregsubsecperc` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental (E) score within its subsector peer group; 100% is best |
| 133 | `social_score_industry_percentile` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Social (S) score within its industry peer group; 100% is best |
| 134 | `social_score_sector_percentile` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Social (S) score within its sector peer group; 100% is best |
| 135 | `social_score_subsector_percentile` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Social (S) score within its subsector peer group; 100% is best |
| 136 | `transparency_industry_position` | MATRIX | 0.889 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its industry peer group based on the G3 Disclosure & Accountability KPI, with 1 being the top |
| 137 | `transparency_sector_position` | MATRIX | 0.889 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its sector peer group based on the G3 Disclosure & Accountability KPI, with 1 being the highe |
| 138 | `transparency_subsector_position` | MATRIX | 0.889 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its subsector peer group based on the G3 Disclosure & Accountability KPI, with 1 being the be |
| 139 | `anl11_citreg_industryperc` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of company's CIT Score within its industry peer group, with 100% being the best |
| 140 | `anl11_citregsubsecperc` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of company's CIT Score within its subsector peer group, with 100% being the best |
| 141 | `anl11_creptcesgertic` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of company's CIT Score within its sector peer group, with 100% being the best |
| 142 | `environmental_industry_percentile_score` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental score within its industry peer group, with 100% being the best |
| 143 | `environmental_sector_percentile_score` | MATRIX | 0.889 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental score within its sector peer group, 100% being the best scoring position |
| 144 | `environmental_subsector_percentile_score` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental score within its subsector peer group, with 100% being the best |
| 145 | `social_industry_percentile_score` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Social Score within industry peer group, with 100% being the best |
| 146 | `social_sector_percentile_score` | MATRIX | 0.889 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentile of the Social Score within sector peer group, with 100% denoting best position |
| 147 | `social_subsector_percentile_score` | MATRIX | 0.889 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentile of the Social Score within subsector peer group, with 100% denoting best position |
| 148 | `community_engagement_industry_position` | MATRIX | 0.888 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its industry peer group based on the OWL CIT1 KPI, where 1 is the highest rank |
| 149 | `community_engagement_sector_position` | MATRIX | 0.888 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its sector peer group based on the OWL CIT1 KPI, where 1 is the highest rank |
| 150 | `community_engagement_subsector_position` | MATRIX | 0.888 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its subsector peer group based on the OWL CIT1 KPI, where 1 is the highest rank |
| 151 | `citizenship_industry_percentile_score` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's Citizenship (CIT) Score within its Industry peer group, with 100% being the best |
| 152 | `citizenship_sector_percentile_score` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's overall CIT score within its sector peer group, with 100% being the best |
| 153 | `citizenship_subsector_percentile_score` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's Citizenship (CIT) Score within its SubSector peer group, with 100% being the best |
| 154 | `anl11_creptcesgerg` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the sector peer group for the Governance (G) score, with 100% being the best |
| 155 | `anl11_greg_industryperc` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the industry peer group for the Governance (G) score, with 100% being the best |
| 156 | `anl11_gregsubsecperc` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the subsector peer group for the Governance (G) score, with 100% being the best |
| 157 | `anl11_creptcesger1e` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E1 KPI within its region-sector group (100% = best) |
| 158 | `anl11_e1reg_industryperc` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E1 KPI within its region-industry group (100% = best) |
| 159 | `anl11_e1regsubsecperc` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E1 KPI within its region-subsector group (100% = best) |
| 160 | `anl11_creptcesger2e` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E2 KPI within its region-sector group (100% = best) |
| 161 | `anl11_creptcesger3e` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E3 KPI within its region-sector group (100% = best) |
| 162 | `anl11_e2reg_industryperc` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E2 KPI within its region-industry group (100% = best) |
| 163 | `anl11_e2regsubsecperc` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E2 KPI within its region-subsector group (100% = best) |
| 164 | `anl11_e3reg_industryperc` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking (within industry) for the third Environmental KPI (E3), with higher percentiles indicating better per |
| 165 | `anl11_e3regsubsecperc` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company on E3 KPI within its region-subsector group (100% = best) |
| 166 | `governance_industry_percentile_score` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Industry Peer Group on the G Score with 100% being the best |
| 167 | `governance_sector_percentile_score` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Sector Peer Group on the G Score with 100% being the best |
| 168 | `governance_subsector_percentile_score` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the SubSector Peer Group on the G Score with 100% being the best |
| 169 | `human_rights_industry_position` | MATRIX | 0.887 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's CIT2 KPI within its industry peer group, with 1 being the highest rank (best performer in industry f |
| 170 | `human_rights_sector_position` | MATRIX | 0.887 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's CIT2 KPI within its sector peer group, with 1 being the highest rank (best performer in sector for h |
| 171 | `human_rights_subsector_position` | MATRIX | 0.887 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's CIT2 KPI within its subsector peer group, with 1 being the highest rank (best performer in subsector |
| 172 | `anl11_creptcesger2g` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's G2 score within its region-sector peer group, with 100% being the best |
| 173 | `anl11_g2reg_industryperc` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's G2 score within its region-industry peer group, with 100% being the best |
| 174 | `anl11_g2regsubsecperc` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's G2 score within its region-subsector peer group, with 100% being the best |
| 175 | `employer_industry_position` | MATRIX | 0.887 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's aggregate employment score within its industry peer group, with 1 being the best |
| 176 | `employer_sector_position` | MATRIX | 0.887 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's aggregate employment score within its sector peer group, with 1 being the best |
| 177 | `employer_subsector_position` | MATRIX | 0.887 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's aggregate employment score within its subsector peer group, with 1 being the best |
| 178 | `pollution_prevention_industry_percentile_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile standing within its industry peer group on the Pollution Prevention (E1) KPI, with 100% being the b |
| 179 | `pollution_prevention_sector_percentile_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile standing within its sector peer group on the Pollution Prevention (E1) KPI, with 100% being the bes |
| 180 | `pollution_prevention_subsector_percentile_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile standing within its subsector peer group on the Pollution Prevention (E1) KPI, with 100% being the |
| 181 | `resource_efficiency_industry_percentile_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its industry peer group based on the OWL E3 KPI, with 100% being the best |
| 182 | `resource_efficiency_sector_percentile_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its sector peer group based on the OWL E3 KPI, with 100% being the best |
| 183 | `resource_efficiency_subsector_percentile_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its subsector peer group based on the OWL E3 KPI, with 100% being the best |
| 184 | `antipollution_policy_industry_percentile` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile standing within its industry peer group on the Environmental Transparency (E2) KPI, with 100% being |
| 185 | `antipollution_policy_sector_percentile` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile standing within its sector peer group on the Environmental Transparency (E2) KPI, with 100% being t |
| 186 | `antipollution_policy_subsector_percentile` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile standing within its subsector peer group on the Environmental Transparency (E2) KPI, with 100% bein |
| 187 | `management_ethics_industry_percentile_score` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's G2 KPI (governance subcomponent 2) within its industry peer group, with higher perce |
| 188 | `management_ethics_sector_percentile_score` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's G2 Management Ethics score within its sector, with 100% representing the best performa |
| 189 | `management_ethics_subsector_percentile_score` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's G2 Management Ethics score within its subsector, with 100% representing the best perfo |
| 190 | `anl11_g3reg_industryperc` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of company within its industry peer group based on the G3 governance KPI, with 100% being the best |
| 191 | `anl11_creptcesger3g` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of company within its sector peer group based on the G3 governance KPI, with 100% being the best |
| 192 | `anl11_g3regsubsecperc` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of company within its subsector peer group based on the G3 governance KPI, with 100% being the best |
| 193 | `board_independence_industry_position` | MATRIX | 0.885 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's G1 Board Effectiveness KPI within its industry peer group, with 1 being the highest rank |
| 194 | `board_independence_sector_position` | MATRIX | 0.885 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's G1 Board Effectiveness KPI within its sector peer group, with 1 being the highest rank |
| 195 | `board_independence_subsector_position` | MATRIX | 0.885 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's G1 Board Effectiveness KPI within its subsector peer group, with 1 being the highest rank |
| 196 | `anl11_cit1reg_industryperc` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within industry for CIT1 (Community Engagement & Charitable Activities), 100% as best |
| 197 | `anl11_cit1regsubsecperc` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within subsector for CIT1 (Community Engagement & Charitable Activities), 100% as best |
| 198 | `anl11_creptcesger1tic` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within sector for CIT1 (Community Engagement & Charitable Activities), 100% as best |
| 199 | `transparency_industry_percentile_score` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's G3 Disclosure & Accountability KPI within its industry peer group, with higher perce |
| 200 | `transparency_sector_percentile_score` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's G3 Disclosure & Accountability KPI within its sector peer group, with higher percent |
| 201 | `transparency_subsector_percentile_score` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's G3 Disclosure & Accountability KPI within its subsector peer group, with higher perc |
| 202 | `community_engagement_industry_percentile_score` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT1 KPI score within its industry peer group, with 100% representing the best perform |
| 203 | `community_engagement_sector_percentile_score` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT1 KPI score within its sector peer group, with 100% representing the best performan |
| 204 | `community_engagement_subsector_percentile_score` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT1 KPI score within its subsector peer group, with 100% representing the best perfor |
| 205 | `anl11_creptcesgerpme` | MATRIX | 0.884 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Score within its sector group, where 100% is the best score |
| 206 | `anl11_empreg_industryperc` | MATRIX | 0.884 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Score within its industry group, where 100% is the best score |
| 207 | `anl11_empregsubsecperc` | MATRIX | 0.884 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Score within its subsector group, where 100% is the best score |
| 208 | `anl11_cit2reg_industryperc` | MATRIX | 0.884 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentile position of a company within its industry peer group for the CIT2 KPI, with 100% being the best |
| 209 | `anl11_cit2regsubsecperc` | MATRIX | 0.884 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of CIT2 KPI within the region-subsector peer group, with 100% being the highest (best) |
| 210 | `anl11_creptcesger2tic` | MATRIX | 0.884 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of CIT2 KPI within the region-sector peer group, with 100% being the highest (best) |
| 211 | `employee_diversity_industry_position` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its industry peer group based on the OWL EMP2 KPI, where 1 is the highest rank |
| 212 | `sustainable_product_industry_position` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's CIT3 KPI within its industry peer group, with 1 being the highest rank (best performer in industry f |
| 213 | `sustainable_product_sector_position` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's CIT3 KPI within its sector peer group, with 1 being the highest rank (best performer in sector for s |
| 214 | `sustainable_product_subsector_position` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company's CIT3 KPI within its subsector peer group, with 1 being the highest rank (best performer in subsector |
| 215 | `workplace_diversity_sector_position` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its sector peer group based on the OWL EMP2 KPI, where 1 is the highest rank |
| 216 | `workplace_diversity_subsector_position` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its subsector peer group based on the OWL EMP2 KPI, where 1 is the highest rank |
| 217 | `human_rights_industry_percentile_score` | MATRIX | 0.883 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT2 KPI score within its industry, with 100% representing the best performance on hum |
| 218 | `human_rights_sector_percentile_score` | MATRIX | 0.883 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT2 KPI score within its sector, with 100% representing the best performance on human |
| 219 | `human_rights_subsector_percentile_score` | MATRIX | 0.883 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT2 KPI score within its subsector, with 100% representing the best performance on hu |
| 220 | `employer_industry_percentile_score` | MATRIX | 0.883 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's aggregate employment score within its industry peer group, with 100% being the best |
| 221 | `employer_sector_percentile_score` | MATRIX | 0.883 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's aggregate employment score within its sector peer group, with 100% being the best |
| 222 | `employer_subsector_percentile_score` | MATRIX | 0.883 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's aggregate employment score within its subsector peer group, with 100% being the best |
| 223 | `anl11_creptcesger1g` | MATRIX | 0.882 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's G1 score within its region-sector peer group, with 100% being the best |
| 224 | `anl11_g1reg_industryperc` | MATRIX | 0.882 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's G1 score within its region-industry peer group, with 100% being the best |
| 225 | `anl11_g1regsubsecperc` | MATRIX | 0.882 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's G1 score within its region-subsector peer group, with 100% being the best |
| 226 | `workplace_safety_industry_position` | MATRIX | 0.882 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its industry peer group based on the OWL EMP3 KPI, where 1 is the highest rank |
| 227 | `workplace_safety_sector_position` | MATRIX | 0.882 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its sector peer group based on the OWL EMP3 KPI, where 1 is the highest rank |
| 228 | `workplace_safety_subsector_position` | MATRIX | 0.882 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its subsector peer group based on the OWL EMP3 KPI, where 1 is the highest rank |
| 229 | `board_independence_industry_percentile_score` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's G1 Board Effectiveness score within its industry, with 100% representing the best perf |
| 230 | `board_independence_sector_percentile_score` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's G1 Board Effectiveness score within its sector, with 100% representing the best perfor |
| 231 | `board_independence_subsector_percentile_score` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's G1 Board Effectiveness score within its subsector, with 100% representing the best per |
| 232 | `anl11_cit3reg_industryperc` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's CIT3 score within its region-industry peer group, with 100% being the best |
| 233 | `anl11_cit3regsubsecperc` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of CIT3 KPI within the region-subsector peer group, with 100% being the highest (best) |
| 234 | `anl11_creptcesger2pme` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within sector for EMP2 (Employee Diversity Treatment & Labor Rights), with 100% as the best |
| 235 | `anl11_creptcesger3tic` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of CIT3 KPI within the region-sector peer group, with 100% being the highest (best) |
| 236 | `anl11_emp2reg_industryperc` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within industry for EMP2 (Employee Diversity Treatment & Labor Rights), with 100% as the best |
| 237 | `anl11_emp2regsubsecperc` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within subsector for EMP2 (Employee Diversity Treatment & Labor Rights), with 100% as the best |
| 238 | `anl11_creptcesger3pme` | MATRIX | 0.880 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within sector for EMP3 (Continuing Education, Training, Work Conditions, Safety & Health), 100% as best |
| 239 | `anl11_emp3reg_industryperc` | MATRIX | 0.880 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within industry for EMP3 (Continuing Education, Training, Work Conditions, Safety & Health), 100% as best |
| 240 | `anl11_emp3regsubsecperc` | MATRIX | 0.880 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within subsector for EMP3 (Continuing Education, Training, Work Conditions, Safety & Health), 100% as best |
| 241 | `employee_diversity_industry_percentile_score` | MATRIX | 0.879 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its industry peer group based on the OWL EMP2 KPI, with 100% being the best |
| 242 | `employee_diversity_sector_percentile_score` | MATRIX | 0.879 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its sector peer group based on the OWL EMP2 KPI, with 100% being the best |
| 243 | `employee_diversity_subsector_percentile_score` | MATRIX | 0.879 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its subsector peer group based on the OWL EMP2 KPI, with 100% being the best |
| 244 | `sustainable_product_industry_percentile_score` | MATRIX | 0.879 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT3 KPI score within its industry, with 100% representing the best performance on sus |
| 245 | `sustainable_product_sector_percentile_score` | MATRIX | 0.879 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT3 KPI score within its sector, with 100% representing the best performance on susta |
| 246 | `sustainable_product_subsector_percentile_score` | MATRIX | 0.879 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of a company's CIT3 KPI score within its subsector, with 100% representing the best performance on su |
| 247 | `workplace_safety_industry_percentile_score` | MATRIX | 0.878 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its industry peer group based on the OWL EMP3 KPI, with 100% being the best |
| 248 | `workplace_safety_sector_percentile_score` | MATRIX | 0.878 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its sector peer group based on the OWL EMP3 KPI, with 100% being the best |
| 249 | `workplace_safety_subsector_percentile_score` | MATRIX | 0.878 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its subsector peer group based on the OWL EMP3 KPI, with 100% being the best |
| 250 | `anl11_global_industrycount` | MATRIX | 0.877 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of industries globally in the dataset |
| 251 | `anl11_globalsectcount` | MATRIX | 0.877 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of sectors globally in the dataset |
| 252 | `anl11_globalsubseccount` | MATRIX | 0.877 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of subsectors globally in the dataset |
| 253 | `employee_satisfaction_industry_position` | MATRIX | 0.877 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its industry peer group based on the OWL EMP1 KPI, where 1 is the highest rank |
| 254 | `employee_satisfaction_sector_position` | MATRIX | 0.877 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its sector peer group based on the OWL EMP1 KPI, where 1 is the highest rank |
| 255 | `employee_satisfaction_subsector_position` | MATRIX | 0.877 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its subsector peer group based on the OWL EMP1 KPI, where 1 is the highest rank |
| 256 | `anl11_creptcesger1pme` | MATRIX | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within sector for EMP1 (Compensation & Employee Satisfaction), with 100% as the best |
| 257 | `anl11_emp1reg_industryperc` | MATRIX | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within industry for EMP1 (Compensation & Employee Satisfaction), with 100% as the best |
| 258 | `anl11_emp1regsubsecperc` | MATRIX | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within subsector for EMP1 (Compensation & Employee Satisfaction), with 100% as the best |
| 259 | `employee_satisfaction_industry_percentile` | MATRIX | 0.873 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its industry peer group based on the OWL EMP1 KPI, with 100% being the best |
| 260 | `employee_satisfaction_sector_percentile` | MATRIX | 0.873 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its sector peer group based on the OWL EMP1 KPI, with 100% being the best |
| 261 | `employee_satisfaction_subsector_percentile` | MATRIX | 0.873 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company within its subsector peer group based on the OWL EMP1 KPI, with 100% being the best |
| 262 | `anl11_esg_totalcor` | MATRIX | 0.832 | 风险与质量 | 0 | — | — | — | UNTESTED | Hybrid ESG score, combining E, EMP, CIT, and G KPIs weighted by strongest positive rank correlation to 1-year/3-year tot |
| 263 | `anl11_esg_totalcorregsectrnk` | MATRIX | 0.832 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's rank in its sector on the ESG Hybrid Score (weighted positive correlation), with 1 being the highest |
| 264 | `anl11_esg_totalcorregsubsecrnk` | MATRIX | 0.832 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's rank in its subsector on the ESG Hybrid Score (weighted positive correlation), with 1 being the highest |
| 265 | `anl11_esg_ttcrg_industryrnk` | MATRIX | 0.832 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's rank in its industry on the ESG Hybrid Score (weighted positive correlation), with 1 being the highest |
| 266 | `anl11_esgposcorreg_industryrnk` | MATRIX | 0.831 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's rank in its industry on the ESG Max Correlation Score, with 1 being the highest |
| 267 | `anl11_esgposcorregsubsecrnk` | MATRIX | 0.831 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's rank in its subsector on the ESG Max Correlation Score, with 1 being the highest |
| 268 | `anl11_knrtcesgerrocsopgse` | MATRIX | 0.831 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's rank in its sector on the ESG Max Correlation Score, with 1 being the highest |
| 269 | `social_score_total_correlation` | MATRIX | 0.828 | 风险与质量 | 0 | — | — | — | UNTESTED | Total correlation value for the S (Social) score with financial metrics |
| 270 | `social_totalcorr_industry_position` | MATRIX | 0.828 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Region of the world in which company is headquartered |
| 271 | `social_totalcorr_sector_position` | MATRIX | 0.828 | 价量与波动 | 0 | — | — | — | UNTESTED | Company’s position within sector peer group for social score weighted by total correlation to financial returns. |
| 272 | `social_totalcorr_subsector_position` | MATRIX | 0.828 | 价量与波动 | 0 | — | — | — | UNTESTED | Company’s position within subsector peer group for social score weighted by total correlation to financial returns. |
| 273 | `anl11_esg_totalcorregsectperc` | MATRIX | 0.828 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile in its sector on the ESG Hybrid Score (weighted positive correlation), with 100% being the best |
| 274 | `anl11_esg_totalcorregsubsecperc` | MATRIX | 0.828 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile in its subsector on the ESG Hybrid Score (weighted positive correlation), with 100% being the best |
| 275 | `anl11_esg_ttcrg_industryperc` | MATRIX | 0.828 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile in its industry on the ESG Hybrid Score (weighted positive correlation), with 100% being the best |
| 276 | `anl11_creptcesgerrocsopgse` | MATRIX | 0.827 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile in its sector on the ESG Max Correlation Score, with 100% being the best |
| 277 | `anl11_esgposcorreg_industryperc` | MATRIX | 0.827 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile in its industry on the ESG Max Correlation Score, with 100% being the best |
| 278 | `anl11_esgposcorregsubsecperc` | MATRIX | 0.827 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company's percentile in its subsector on the ESG Max Correlation Score, with 100% being the best |
| 279 | `anl11_e_totalcor` | MATRIX | 0.825 | 风险与质量 | 0 | — | — | — | UNTESTED | Hybrid E score, with the three E KPIs weighted by their strength of positive correlation to financial metrics related to |
| 280 | `anl11_e_totalcorregsectrnk` | MATRIX | 0.825 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank position of the company’s E Hybrid Score (composite E metric weighted by correlation) within sector peer group, 1 i |
| 281 | `anl11_e_totalcorregsubsecrnk` | MATRIX | 0.825 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank position of the company’s E Hybrid Score within subsector peer group, 1 is highest |
| 282 | `anl11_e_ttcrg_industryrnk` | MATRIX | 0.825 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank position of the company’s E Hybrid Score within industry peer group, 1 is highest |
| 283 | `social_totalcorr_industry_percentile` | MATRIX | 0.824 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region of the world in which company is headquartered |
| 284 | `social_totalcorr_sector_percentile` | MATRIX | 0.824 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking within sector peer group for social score weighted by total correlation to financial returns. |
| 285 | `social_totalcorr_subsector_percentile` | MATRIX | 0.824 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking within subsector peer group for social score weighted by total correlation to financial returns. |
| 286 | `anl11_2_region` | MATRIX | 0.824 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region of the world in which the company is headquartered |
| 287 | `anl11_company_name` | MATRIX | 0.824 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Company name |
| 288 | `social_poscorr_industry_position` | MATRIX | 0.823 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Social max correlation score within its industry peer group; 1 is highest |
| 289 | `social_poscorr_sector_position` | MATRIX | 0.823 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Social max correlation score within its sector peer group; 1 is highest |
| 290 | `social_poscorr_subsector_position` | MATRIX | 0.823 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company’s Social max correlation score within its subsector peer group; 1 is highest |
| 291 | `social_score_positive_correlation` | MATRIX | 0.823 | 风险与质量 | 0 | — | — | — | UNTESTED | Social (S) score for the company; calculated by simple average of CIT (Citizenship) and EMP (Employment) metrics, with n |
| 292 | `anl11_g_totalcor` | MATRIX | 0.823 | 风险与质量 | 0 | — | — | — | UNTESTED | Governance hybrid score, weighting G1, G2, G3 by their positive correlation to financial performance, particularly 1-yea |
| 293 | `anl11_g_totalcorregsectrnk` | MATRIX | 0.823 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the sector peer group for the governance hybrid score (positively correlated only), with 1 being the highest |
| 294 | `anl11_g_totalcorregsubsecrnk` | MATRIX | 0.823 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the subsector peer group for the governance hybrid score (positively correlated only), with 1 being the high |
| 295 | `anl11_g_ttcrg_industryrnk` | MATRIX | 0.823 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the industry peer group for the governance hybrid score (positively correlated only), with 1 being the highe |
| 296 | `anl11_cit_totalcor` | MATRIX | 0.821 | 风险与质量 | 0 | — | — | — | UNTESTED | Hybrid score for Capital Investment pillar, weighting CIT1, CIT2, and CIT3 based on strong positive rank correlations to |
| 297 | `anl11_cit_totalcorregsectrnk` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | The rank of the company within its sector based on the Citizenship (CIT) Hybrid Score, where 1 is the highest rank among |
| 298 | `anl11_cit_totalcorregsubsecrnk` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | The rank of the company within its subsector based on the Citizenship (CIT) Hybrid Score, where 1 is the highest rank am |
| 299 | `anl11_cit_ttcrg_industryrnk` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | The rank of the company within its industry on the Citizenship (CIT) Hybrid Score, where 1 is the highest rank among ind |
| 300 | `anl11_e_totalcorregsectperc` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental Hybrid score within its sector (100% is best) |
| 301 | `anl11_e_totalcorregsubsecperc` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental Hybrid score within its subsector (100% is best) |
| 302 | `anl11_e_ttcrg_industryperc` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental Hybrid score within its industry (100% is best) |
| 303 | `social_poscorr_industry_percentile` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region of the world in which company is headquartered |
| 304 | `social_poscorr_sector_percentile` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Social max correlation score within its sector peer group; 100% is best |
| 305 | `social_poscorr_subsector_percentile` | MATRIX | 0.821 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Social max correlation score within its subsector peer group; 100% is best |
| 306 | `anl11_2_e` | MATRIX | 0.821 | 风险与质量 | 0 | — | — | — | UNTESTED | The E Score averages the E1, E2, and E3 scores. |
| 307 | `anl11_emp_totalcor` | MATRIX | 0.820 | 风险与质量 | 0 | — | — | — | UNTESTED | EMP Hybrid Score representing a weighted combination of three EMP scores, weighted based on their positive correlation t |
| 308 | `anl11_emp_totalcorregsectrnk` | MATRIX | 0.820 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Hybrid Score within its sector peer group, where 1 is the highest rank |
| 309 | `anl11_emp_totalcorregsubsecrnk` | MATRIX | 0.820 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Hybrid Score within its subsector peer group, where 1 is the highest rank |
| 310 | `anl11_emp_ttcrg_industryrnk` | MATRIX | 0.820 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Hybrid Score within its industry peer group, where 1 is the highest rank |
| 311 | `anl11_2_g` | MATRIX | 0.820 | 风险与质量 | 0 | — | — | — | UNTESTED | The G Score averages the G1, G2, and G3 scores. |
| 312 | `anl11_g_totalcorregsectperc` | MATRIX | 0.819 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the sector peer group for the governance hybrid score (positively correlated only), 100% being the bes |
| 313 | `anl11_g_totalcorregsubsecperc` | MATRIX | 0.819 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the subsector peer group for the governance hybrid score (positively correlated only), 100% being the |
| 314 | `anl11_g_ttcrg_industryperc` | MATRIX | 0.819 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the industry peer group for the governance hybrid score (positively correlated only), 100% being the b |
| 315 | `anl11_2_tic` | MATRIX | 0.818 | 风险与质量 | 0 | — | — | — | UNTESTED | The CIT Score averages the CIT1, CIT2, and CIT3 scores. |
| 316 | `anl11_2_2g` | MATRIX | 0.817 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Management Standards & Ethics |
| 317 | `anl11_cit_totalcorregsectperc` | MATRIX | 0.817 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentile of the company within its sector on the Citizenship (CIT) Hybrid Score, with 100% being best among sector |
| 318 | `anl11_cit_totalcorregsubsecperc` | MATRIX | 0.817 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentile of the company within its subsector on the Citizenship (CIT) Hybrid Score, with 100% being best among sub |
| 319 | `anl11_cit_ttcrg_industryperc` | MATRIX | 0.817 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentile of the company within its industry on the Citizenship (CIT) Hybrid Score, with 100% indicating top perfor |
| 320 | `anl11_emp_totalcorregsectperc` | MATRIX | 0.816 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Hybrid Score within its sector peer group, where 100% is the best value |
| 321 | `anl11_emp_totalcorregsubsecperc` | MATRIX | 0.816 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Hybrid Score within its subsector peer group, where 100% is the best value |
| 322 | `anl11_emp_ttcrg_industryperc` | MATRIX | 0.816 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Hybrid Score within its industry peer group, where 100% is the best value |
| 323 | `anl11_2_3e` | MATRIX | 0.816 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Energy & Resource Efficiency |
| 324 | `anl11_2_3g` | MATRIX | 0.816 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Aggregate KPI for Disclosure, Transparency, & Stakeholder Accountability |
| 325 | `anl11_2_1tic` | MATRIX | 0.810 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Community Engagement & Charitable Activities |
| 326 | `anl11_empposcorreg_industryrnk` | MATRIX | 0.809 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Max Correlation Score within its industry peer group, where 1 is the highest rank |
| 327 | `anl11_empposcorregsubsecrnk` | MATRIX | 0.809 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Max Correlation Score within its subsector peer group, where 1 is the highest rank |
| 328 | `anl11_knrtcesgerrocsoppme` | MATRIX | 0.809 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of a company's EMP Max Correlation Score within its sector peer group, where 1 is the highest rank |
| 329 | `anl11_rocsoppme` | MATRIX | 0.809 | 风险与质量 | 0 | — | — | — | UNTESTED | EMP Max Correlation Score, weighting the three EMP KPIs by their strong positive and negative correlations with financia |
| 330 | `anl11_2_1e` | MATRIX | 0.807 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for pollution prevention & environmental remediation |
| 331 | `anl11_creptcesgerrocsoppme` | MATRIX | 0.806 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Max Correlation Score within its sector peer group, where 100% is the best value |
| 332 | `anl11_empposcorreg_industryperc` | MATRIX | 0.806 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Max Correlation Score within its industry peer group, where 100% is the best value |
| 333 | `anl11_empposcorregsubsecperc` | MATRIX | 0.806 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of a company's EMP Max Correlation Score within its subsector peer group, where 100% is the best value |
| 334 | `anl11_gposcorreg_industryrnk` | MATRIX | 0.806 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the industry peer group for the governance max correlation score (both positive and negative) with 1 being t |
| 335 | `anl11_gposcorregsubsecrnk` | MATRIX | 0.806 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the subsector peer group for the governance max correlation score (both positive and negative) with 1 being |
| 336 | `anl11_knrtcesgerrocsopg` | MATRIX | 0.806 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank within the sector peer group for the governance max correlation score (both positive and negative) with 1 being the |
| 337 | `anl11_rocsopg` | MATRIX | 0.806 | 风险与质量 | 0 | — | — | — | UNTESTED | Governance max correlation score, weighting G1, G2, G3 by their correlation (both positive and negative) to financial pe |
| 338 | `anl11_2_2e` | MATRIX | 0.805 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Anti-Pollution Policies & Environmental Transparency |
| 339 | `anl11_creptcesgerrocsopg` | MATRIX | 0.803 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the sector peer group for the governance max correlation score (both positive and negative), 100% bein |
| 340 | `anl11_gposcorreg_industryperc` | MATRIX | 0.803 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the industry peer group for the governance max correlation score (both positive and negative), 100% be |
| 341 | `anl11_gposcorregsubsecperc` | MATRIX | 0.803 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the subsector peer group for the governance max correlation score (both positive and negative), 100% b |
| 342 | `anl11_2_1g` | MATRIX | 0.803 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Board Independence, Diversity, & Effectiveness |
| 343 | `anl11_2_2tic` | MATRIX | 0.802 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Human Rights Activism, Supply Chain, Labor & Human Rights Policies |
| 344 | `anl11_2_2pme` | MATRIX | 0.800 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for employee diversity treatment & labor rights |
| 345 | `anl11_citposcorreg_industryrnk` | MATRIX | 0.798 | 宏观与行业 | 0 | — | — | — | UNTESTED | The rank of the company within its industry on the Citizenship (CIT) Max Correlation Score, where 1 is the highest score |
| 346 | `anl11_citposcorregsubsecrnk` | MATRIX | 0.798 | 宏观与行业 | 0 | — | — | — | UNTESTED | Subsector Rank of CIT Max Correlation Score, where 1 is the highest rank |
| 347 | `anl11_knrtcesgerrocsoptic` | MATRIX | 0.798 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector Rank of CIT Max Correlation Score, where 1 is the highest rank |
| 348 | `anl11_rocsoptic` | MATRIX | 0.798 | 风险与质量 | 0 | — | — | — | UNTESTED | Max Correlation score for Capital Investment pillar, weighting CIT1, CIT2, and CIT3 based on both positive and negative |
| 349 | `anl11_2_3pme` | MATRIX | 0.797 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Employee Continuing Education, Training, Work Conditions, Safety & Health |
| 350 | `anl11_citposcorreg_industryperc` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentile of the company within its industry on the Citizenship (CIT) Max Correlation Score, with 100% being best a |
| 351 | `anl11_crptcsknrtcsgrscptc` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | The rank and percentile of the company within its sector on the Citizenship (CIT) Max Correlation Score, with rank 1 bei |
| 352 | `anl11_ctpscrgsbscrnksbscprc` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | The rank and percentile of the company within its subsector on the Citizenship (CIT) Max Correlation Score, with rank 1 |
| 353 | `anl11_2_1pme` | MATRIX | 0.792 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Compensation & Employee Satisfaction |
| 354 | `sustainability_max_correlation_weighted_score` | MATRIX | 0.792 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite ESG score weighted by the strength of correlation (positive and negative) of underlying KPIs with financial pe |
| 355 | `sustainability_maxcorr_industry_position` | MATRIX | 0.792 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its industry peer group based on the ESG Max Correlation score, with 1 indicating strongest c |
| 356 | `sustainability_maxcorr_sector_position` | MATRIX | 0.792 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its sector peer group based on the ESG Max Correlation score, with 1 indicating the highest w |
| 357 | `sustainability_maxcorr_subsector_position` | MATRIX | 0.792 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its subsector peer group based on the ESG Max Correlation score, with 1 indicating strongest |
| 358 | `sustainability_hybrid_industry_position` | MATRIX | 0.790 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its industry peer group based on the ESG Hybrid score, with 1 being the highest positively co |
| 359 | `sustainability_hybrid_sector_position` | MATRIX | 0.790 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its sector peer group based on the ESG Hybrid score, with 1 being the highest positively corr |
| 360 | `sustainability_hybrid_subsector_position` | MATRIX | 0.790 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company within its subsector peer group based on the ESG Hybrid score, with 1 being the highest positively c |
| 361 | `sustainability_hybrid_weighted_score` | MATRIX | 0.790 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite ESG score weighted only by positive correlations of underlying KPIs with financial performance metrics (such a |
| 362 | `social_max_correlation_weighted_score` | MATRIX | 0.789 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite score for Social KPIs (EMP1, EMP2, EMP3, CIT1, CIT2, CIT3) reflecting the strongest positive or negative corre |
| 363 | `social_maxcorr_industry_position` | MATRIX | 0.789 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Industry Peer Group based on the S Max Correlation Score, with 1 being the highest (best) |
| 364 | `social_maxcorr_sector_position` | MATRIX | 0.789 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the S Max Correlation score within sector peer group, 1 is best |
| 365 | `social_maxcorr_subsector_position` | MATRIX | 0.789 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the SubSector Peer Group based on the S (Social pillar) Max Correlation Score, with 1 being the highest (bes |
| 366 | `sustainability_maxcorr_industry_percentile_score` | MATRIX | 0.789 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking within industry peer group based on the ESG Max Correlation score, with higher percentiles meaning st |
| 367 | `sustainability_maxcorr_sector_percentile_score` | MATRIX | 0.789 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking within sector peer group based on the ESG Max Correlation score, with higher percentiles meaning stro |
| 368 | `sustainability_maxcorr_subsector_percentile_score` | MATRIX | 0.789 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking within subsector peer group based on the ESG Max Correlation score, with higher percentiles meaning s |
| 369 | `social_maxcorr_industry_percentile_score` | MATRIX | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Industry Peer Group for the S Max Correlation Score, with 100% being the best standing in the peer |
| 370 | `social_maxcorr_sector_percentile_score` | MATRIX | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Sector Peer Group for the S Max Correlation Score, with 100% being the best standing in the peer g |
| 371 | `social_maxcorr_subsector_percentile_score` | MATRIX | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the SubSector Peer Group for the S Max Correlation Score, with 100% being the best standing in the pee |
| 372 | `sustainability_hybrid_industry_percentile_score` | MATRIX | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking within industry peer group based on the ESG Hybrid score, with higher percentiles indicating stronger |
| 373 | `sustainability_hybrid_sector_percentile_score` | MATRIX | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking within sector peer group based on the ESG Hybrid score, with higher percentiles indicating stronger p |
| 374 | `sustainability_hybrid_subsector_percentile_score` | MATRIX | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking within subsector peer group based on the ESG Hybrid score, with higher percentiles indicating stronge |
| 375 | `anl11_2_3tic` | MATRIX | 0.784 | 其他 | 0 | — | — | — | UNTESTED | Aggregate KPI for Business Model & Products |
| 376 | `anl11_eposcorreg_industryrnk` | MATRIX | 0.782 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company’s Environmental max correlation score within its industry peer group; 1 is highest |
| 377 | `anl11_eposcorregsubsecrnk` | MATRIX | 0.782 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company’s Environmental max correlation score within its subsector peer group; 1 is highest |
| 378 | `anl11_knrtcesgerrocsope` | MATRIX | 0.782 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rank of the company’s Environmental max correlation score within its sector peer group; 1 is highest |
| 379 | `anl11_rocsope` | MATRIX | 0.782 | 风险与质量 | 0 | — | — | — | UNTESTED | Environment Max Correlation Score, weighting E1, E2, and E3 metrics according to positive and negative correlations to f |
| 380 | `anl11_creptcesgerrocsope` | MATRIX | 0.780 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental max correlation score within its sector peer group; 100% is best |
| 381 | `anl11_eposcorreg_industryperc` | MATRIX | 0.780 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental max correlation score within its industry peer group; 100% is best |
| 382 | `anl11_eposcorregsubsecperc` | MATRIX | 0.780 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the company’s Environmental max correlation score within its subsector peer group; 100% is best |
| 383 | `governance_max_correlation_weighted_score` | MATRIX | 0.777 | 风险与质量 | 0 | — | — | — | UNTESTED | Governance Max Correlation Score, which weights governance KPIs (G1, G2, G3) based on their strong rank correlation to f |
| 384 | `governance_maxcorr_industry_position` | MATRIX | 0.777 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Industry Peer Group on the Governance Max Correlation Score, with 1 being the highest |
| 385 | `governance_maxcorr_sector_position` | MATRIX | 0.777 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Sector Peer Group on the Governance Max Correlation Score, with 1 being the highest |
| 386 | `governance_maxcorr_subsector_position` | MATRIX | 0.777 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the SubSector Peer Group on the Governance Max Correlation Score, with 1 being the highest |
| 387 | `governance_maxcorr_industry_percentile_score` | MATRIX | 0.774 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Industry Peer Group for the Governance Max Correlation Score, with 100% being the best |
| 388 | `governance_maxcorr_sector_percentile_score` | MATRIX | 0.774 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Sector Peer Group for the Governance Max Correlation Score, with 100% being the best |
| 389 | `governance_maxcorr_subsector_percentile_score` | MATRIX | 0.774 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the SubSector Peer Group for the Governance Max Correlation Score, with 100% being the best |
| 390 | `employer_maxcorr_industry_position` | MATRIX | 0.772 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's EMP Max Correlation Score within its industry peer group, with 1 as highest |
| 391 | `employer_maxcorr_sector_position` | MATRIX | 0.772 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's EMP Max Correlation Score within its sector peer group, with 1 as highest |
| 392 | `employer_maxcorr_subsector_position` | MATRIX | 0.772 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's EMP Max Correlation Score within its subsector peer group, with 1 as highest |
| 393 | `employer_maxcorr_weighted_score` | MATRIX | 0.772 | 风险与质量 | 0 | — | — | — | UNTESTED | A composite employment score weighting EMP1, EMP2, EMP3 by their strongest correlations (both positive and negative) wit |
| 394 | `social_hybrid_industry_position` | MATRIX | 0.771 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Industry Peer Group based on the S Hybrid Score, with 1 being the highest (best) |
| 395 | `social_hybrid_sector_position` | MATRIX | 0.771 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Sector Peer Group based on the S Hybrid Score, with 1 being the highest (best) |
| 396 | `social_hybrid_subsector_position` | MATRIX | 0.771 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the SubSector Peer Group based on the S Hybrid Score, with 1 being the highest (best) |
| 397 | `social_hybrid_weighted_score` | MATRIX | 0.771 | 风险与质量 | 0 | — | — | — | UNTESTED | Hybrid Social score that emphasizes positive correlations of Social KPIs (EMP1, EMP2, EMP3, CIT1, CIT2, CIT3) with finan |
| 398 | `employer_maxcorr_industry_percentile_score` | MATRIX | 0.769 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's EMP Max Correlation Score within its industry peer group, with 100% being the best |
| 399 | `employer_maxcorr_sector_percentile_score` | MATRIX | 0.769 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's EMP Max Correlation Score within its sector peer group, with 100% being the best |
| 400 | `employer_maxcorr_subsector_percentile_score` | MATRIX | 0.769 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's EMP Max Correlation Score within its subsector peer group, with 100% being the best |
| 401 | `social_hybrid_industry_percentile_score` | MATRIX | 0.767 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Industry Peer Group for the S Hybrid Score, with 100% being the best standing in the peer group |
| 402 | `social_hybrid_sector_percentile_score` | MATRIX | 0.767 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Sector Peer Group for the S Hybrid Score, with 100% being the best standing in the peer group |
| 403 | `social_hybrid_subsector_percentile_score` | MATRIX | 0.767 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the SubSector Peer Group for the S Hybrid Score, with 100% being the best standing in the peer group |
| 404 | `environmental_max_correlation_weighted_score` | MATRIX | 0.760 | 风险与质量 | 0 | — | — | — | UNTESTED | A composite score for Environmental KPIs (E1, E2, E3) representing their strongest positive or negative correlation with |
| 405 | `environmental_maxcorr_industry_position` | MATRIX | 0.760 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Environmental Max Correlation score within industry peer group, with 1 being the top rank |
| 406 | `environmental_maxcorr_sector_position` | MATRIX | 0.760 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Environmental Max Correlation score within sector peer group, with 1 being the top rank |
| 407 | `environmental_maxcorr_subsector_position` | MATRIX | 0.760 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Environmental Max Correlation score within subsector peer group, with 1 being the top rank |
| 408 | `citizenship_maxcorr_industry_position` | MATRIX | 0.757 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its Industry peer group based on the Citizenship (CIT) Max Correlation Score, with rank 1 being |
| 409 | `citizenship_maxcorr_sector_position` | MATRIX | 0.757 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its Sector peer group based on the Citizenship (CIT) Max Correlation Score, with rank 1 being t |
| 410 | `citizenship_maxcorr_subsector_position` | MATRIX | 0.757 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its SubSector peer group based on the Citizenship (CIT) Max Correlation Score, with rank 1 bein |
| 411 | `citizenship_maxcorr_weighted_score` | MATRIX | 0.757 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite capital investment score weighting CIT1, CIT2, CIT3 by strongest correlations (positive and negative) with fin |
| 412 | `environmental_maxcorr_industry_percentile_score` | MATRIX | 0.757 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Environmental Max Correlation score within industry peer group, with 100% being the best |
| 413 | `environmental_maxcorr_sector_percentile_score` | MATRIX | 0.757 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Environmental Max Correlation score within sector peer group, with 100% being the best |
| 414 | `environmental_maxcorr_subsector_percentile_score` | MATRIX | 0.757 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Environmental Max Correlation score within subsector peer group, with 100% being the best |
| 415 | `citizenship_maxcorr_industry_percentile_score` | MATRIX | 0.754 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's CIT Max Correlation Score within its Industry peer group, with 100% being the best |
| 416 | `citizenship_maxcorr_sector_percentile_score` | MATRIX | 0.754 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's CIT Max Correlation Score within its Sector peer group, with 100% being the best |
| 417 | `citizenship_maxcorr_subsector_percentile_score` | MATRIX | 0.754 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's CIT Max Correlation Score within its SubSector peer group, with 100% being the best |
| 418 | `governance_hybrid_industry_position` | MATRIX | 0.747 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Industry Peer Group on the Governance Hybrid Score, with 1 being the highest |
| 419 | `governance_hybrid_sector_position` | MATRIX | 0.747 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the Sector Peer Group on the Governance Hybrid Score, with 1 being the highest |
| 420 | `governance_hybrid_subsector_position` | MATRIX | 0.747 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank within the SubSector Peer Group on the Governance Hybrid Score, with 1 being the highest |
| 421 | `governance_hybrid_weighted_score` | MATRIX | 0.747 | 风险与质量 | 0 | — | — | — | UNTESTED | Governance Hybrid Score, which weights governance KPIs (G1, G2, G3) based on their strong positive rank correlation to f |
| 422 | `governance_hybrid_industry_percentile_score` | MATRIX | 0.744 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank within the Industry peer group for the Governance Hybrid Score, with 100% being the best |
| 423 | `governance_hybrid_sector_percentile_score` | MATRIX | 0.744 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile within the Sector Peer Group for the Governance Hybrid Score, with 100% being the best |
| 424 | `governance_hybrid_subsector_percentile_score` | MATRIX | 0.744 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank within the SubSector peer group for the Governance Hybrid Score, with 100% being the best |
| 425 | `citizenship_hybrid_industry_position` | MATRIX | 0.731 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its Industry peer group on the Citizenship (CIT) Hybrid Score, with rank 1 being the best |
| 426 | `citizenship_hybrid_sector_position` | MATRIX | 0.731 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its Sector peer group on the Citizenship (CIT) Hybrid Score, with rank 1 being the best |
| 427 | `citizenship_hybrid_subsector_position` | MATRIX | 0.731 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of a company within its SubSector peer group on the Citizenship (CIT) Hybrid Score, with rank 1 being the best |
| 428 | `citizenship_hybrid_weighted_score` | MATRIX | 0.731 | 价量与波动 | 0 | — | — | — | UNTESTED | Composite capital investment score weighting CIT1, CIT2, CIT3 by strongest positive correlations with financial returns, |
| 429 | `citizenship_hybrid_industry_percentile_score` | MATRIX | 0.727 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's CIT Hybrid Score within its Industry peer group, with 100% being the best |
| 430 | `citizenship_hybrid_sector_percentile_score` | MATRIX | 0.727 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's CIT Hybrid Score within its Sector peer group, with 100% being the best |
| 431 | `citizenship_hybrid_subsector_percentile_score` | MATRIX | 0.727 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of a company's CIT Hybrid Score within its SubSector peer group, with 100% being the best |
| 432 | `employer_hybrid_industry_position` | MATRIX | 0.726 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's EMP Hybrid Score within its industry peer group, with 1 as highest |
| 433 | `employer_hybrid_sector_position` | MATRIX | 0.726 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's EMP Hybrid Score within its sector peer group, with 1 as highest |
| 434 | `employer_hybrid_subsector_position` | MATRIX | 0.726 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the company's EMP Hybrid Score within its subsector peer group, with 1 as highest |
| 435 | `employer_hybrid_weighted_score` | MATRIX | 0.726 | 价量与波动 | 0 | — | — | — | UNTESTED | A composite employment score weighting EMP1, EMP2, EMP3 by their strongest positive correlations with financial returns, |
| 436 | `employer_hybrid_industry_percentile_score` | MATRIX | 0.722 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's EMP Hybrid Score within its industry peer group, with 100% being the best |
| 437 | `employer_hybrid_sector_percentile_score` | MATRIX | 0.722 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's EMP Hybrid Score within its sector peer group, with 100% being the best |
| 438 | `employer_hybrid_subsector_percentile_score` | MATRIX | 0.722 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile ranking of the company's EMP Hybrid Score within its subsector peer group, with 100% being the best |
| 439 | `environmental_hybrid_industry_position` | MATRIX | 0.700 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Environmental Hybrid score within industry peer group, 1 being the highest |
| 440 | `environmental_hybrid_sector_position` | MATRIX | 0.700 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Environmental Hybrid score within sector peer group, 1 being the highest |
| 441 | `environmental_hybrid_subsector_position` | MATRIX | 0.700 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank of the Environmental Hybrid score within subsector peer group, 1 being the highest |
| 442 | `environmental_hybrid_weighted_score` | MATRIX | 0.700 | 风险与质量 | 0 | — | — | — | UNTESTED | A composite score for Environmental KPIs (E1, E2, E3) emphasizing only positive correlations with financial metrics tied |
| 443 | `environmental_hybrid_industry_percentile_score` | MATRIX | 0.696 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Environmental Hybrid score within industry peer group, 100% being the best |
| 444 | `environmental_hybrid_sector_percentile_score` | MATRIX | 0.696 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Environmental Hybrid score within sector peer group, 100% being the best |
| 445 | `environmental_hybrid_subsector_percentile_score` | MATRIX | 0.696 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile of the Environmental Hybrid score within subsector peer group, 100% being the best |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **8** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `LLNP1AZL` | 0.43 | 0.23 | — | — | 0.36 | 0 | 190 | `ts_zscore(anl11_rocsopgse, 66)` |
| `1YXqdQxR` | 0.42 | 0.32 | — | — | 0.12 | 0 | 190 | `rank(ts_delta(anl11_greg_industryrnk, 22))` |
| `vRrKl3kA` | 0.02 | 0.00 | — | — | 0.18 | 0 | 190 | `group_rank(anl11_2_e, subindustry)` |
| `0mXbE0X8` | -0.03 | 0.00 | — | — | 0.36 | 0 | 190 | `rank(anl11_citreg_industryrnk)` |
| `GrbqLpbQ` | -0.16 | -0.07 | — | — | 0.11 | 0 | 190 | `group_rank(ts_delta(anl11_2_e, 22), subindustry)` |
| `npd12MK3` | -0.25 | -0.14 | — | — | 0.13 | 0 | 190 | `rank(ts_delta(anl11_2_gse, 66))` |
| `3qXMRZXg` | -0.31 | -0.13 | — | — | 0.36 | 0 | 190 | `ts_zscore(anl11_2_pme, 66)` |
| `3qXMRZlN` | -0.33 | -0.15 | — | — | 0.36 | 0 | 190 | `rank(anl11_esgreg_industryrnk)` |

## 七、判死记录（sealed dead_end）

- `EUR-ANL11-ESG-SLOWVAR-LONGCOUNT`（None）family=analyst11 ESG 评分体系（三支柱 + 行业排名 + 改善动量）：{"critical_lesson": "★ coverage 元数据虚报（缺陷#3 第4次坐实）：catalog 报 cov=0.9123/0.9087，实际回测 longCount 仅 51-52（占 TOP2500 的 2%）。选数据集时不能信 catalog coverage，必须用 1-2 条探针实测 longCount。", "dataset": "analyst11", "evidence": {"1YxzzPmQ": "ESG 绝对水平 rank(overall_sustainability_score_2)：S-0.68/F-0.13/TVR0.0985/longCount 52/CW FAIL", "A1077x7l": "行业内排名 rank(reverse(anl11_esgreg_industryrnk))：S-0.25/F-0.03/longCount 51/C
- `EUR-INST6-INSTITUTIONS-TOWER-EXHAUSTED`（None）family=institutions6 机构持股聚合（净流向/存量/动量三机制）：{"dataset": "institutions6", "evidence": {"d5ORZ8NX": "持股存量水平：S0.09/F0.02/TVR0.014/returns0.0052/longCount1417", "kqVZPRJK": "净买家数：S0.18/F0.05/TVR0.038/returns0.0089/longCount1326/2Y-1.71", "xAYdNXjW": "买入金额动量：S0.30/F0.07/TVR0.086/returns0.0065/longCount1350"}, "math_proof": "Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.30*sqrt(0.0089/0.125) = 0.080；即使 Sharpe 达 1.58 也仅 0.42，要 Fitness>=

