# DEU D1 数据集处置图谱（处置结论 ↔ 画像档案对照，2026-11-11 上午）

> 目标第 4 条交付要求「附字段画像存档索引」的收口件。172 集每集一行：处置结论 + 结论依据档案 + 字段画像档案。
> 字段级画像：`tracking/DEU/atom_orthogonal/<dataset_id>_fields.csv`（172 集全量，20,012 字段，列 id/type/cov/uc/ac/desc）+ `field_profile_index.json`。

## 一、实测出结论（有回测证据）

| 数据集 | 塔 | 实测 S 天花板 | 判定 | 结论档案 |
|---|---|---:|---|---|
| shortinterest3 | SHORTINTEREST | 1.72 | ✅ 主力（已交付 4 颗） | RECIPE_MATRIX_SHORTINTEREST / reports/dataset_experience/deu_shortinterest3_campain.md |
| analyst 族(anl93/est) | ANALYST | 2.02 | ✅ 已交付 4+ 颗 | FINAL_DELIVERY_REPORT_11ALPHAS / ALPHA11 档案 |
| insiders1 | INSIDERS | 1.00(单) / 1.72(组合) | ✅ 组合腿已交付 | WAVE_BE29 |
| other47 | OTHER | 1.65(组合) | ✅ 组合腿已交付 | WAVE_BE22 / WAVE_BE26 |
| fundamental6 | FUNDAMENTAL | 1.73(oiadpq 单点) | ⚠ 单点已被 Wje5K71x 占用 | atom_fundamental/campaign_verdict_20261107 |
| news20 | NEWS | 1.52×I7 线 | ❌ 七维判死（31 臂，三档无改善） | WAVE_BE43B_NEWS_FINAL_CLOSE |
| news18 | NEWS | 0.79 | ❌ | WAVE_BE38_NEWS_CEILING_FINAL |
| sentiment27 | SENTIMENT | 0.95 | ❌ 水平面有效但强度不足 | WAVE_BE27_28_SENTIMENT27_VERDICT |
| sentiment7 | SENTIMENT | 0.66 | ❌ 六波 48 探针 | priors/deu_priors.json |
| sentiment33 | SENTIMENT | 0.57(幻觉) | ❌ 小样本幻觉（四波 32 臂） | SENTIMENT33_FULL_VERDICT |
| insider_agg_matrix | INSIDERS | 0.84 | ❌ 弱存活低于升级线 | WAVE_BE44_PATTERN_INSIDERAGG_VERDICT |
| institutions6 | INSTITUTIONS | 0.27 | ❌ | INSTITUTIONS_FAMILY_FINAL |
| institutions25 | INSTITUTIONS | 0.35 | ❌ | INSTITUTIONS_FAMILY_FINAL |
| institutions4/1, fund_holdings_panel | INSTITUTIONS | 0.41-0.65 | ❌ | INSTITUTIONS_FAMILY_FINAL / WAVE_BE45(institutions1) |
| risk88 | RISK | 0.30 | ❌ 描述性无方向 | RISK_FAMILY_REAL_PROFILE |
| risk60 | RISK | 0.90 | ❌ 六维合规死 | RISK_FAMILY_REAL_PROFILE |
| risk72 | RISK | 0.39 | ❌ lc 25-62 稀疏 | RISK_FAMILY_REAL_PROFILE |
| pattern_scores | PV | 0.71 | ❌ 探针死 | WAVE_BE44 / WAVE_BE47 |
| pv30 | PV | 0.79(本战役)/1.61(存量已死) | ❌ | WAVE_BE44 汇总 |
| pv29 | PV | — | ❌ 全字段簇标签 | master 表 |
| continuation_score | PV | 0.42 | ❌ 探针死 | WAVE_BE47_PV_RESIDUAL_PROBE |
| intraday_pv_feats | PV | 0.31 | ❌ 探针死 | WAVE_BE47 |
| pv109 | PV | 0.42 | ❌ 探针死（债券面） | WAVE_BE47 |
| fundamental45 | FUNDAMENTAL | 0.99 | ❌ S 差 60%（杠杆穷尽） | atom_fundamental/campaign_verdict |
| fundamental90 | FUNDAMENTAL | 1.02(2Y 0.42) | ❌ 2Y 内禀死 | atom_fundamental/campaign_verdict |
| fundamental22 | FUNDAMENTAL | 0.48 | ❌ | atom_fundamental/campaign_verdict |
| fundamental89/17/86/93/72/1 | FUNDAMENTAL | <1.0 | ❌ 历史探针+复核 | atom_fundamental/campaign_verdict / DEU_fundamental_round2 |
| earnings6/earnings_sent_matrix | EARNINGS | 0.40/0.63 | ❌（ern6 另有五年空窗） | master 表 |
| option1 | OPTION | 0.62 | ❌ 3 臂全灭 | master 表 |
| opt1 同上 | OPTION | — | — | — |
| lending_fee(RISK 类字段) | RISK | 1.20(×I7) | ❌ 强度不足 | WAVE_BE13_NEWLEG_MATRIX |
| socialmedia12 | SOCIALMEDIA | 0.73 | ❌ | master 表 |
| workforce_flow_skills | OTHER | 0.96 | ❌ | master 表 |
| other699 | OTHER | 0.84 | ❌ | master 表 |
| dl_riskfree_returns/stock_cluster_dl/techindi 等OTHER/MODEL 族 | 已点亮塔 | 各历史波 | 冻结（11-11 用户指令） | 各历史 result_*.json / priors |

## 二、探针/画像级排除（无回测价值或语义不可用）

| 数据集 | 排除原因 | 档案 |
|---|---|---|
| socialmedia39 | 单字段=邻居 ticker ID 列表，数值聚合无意义 | FIELD_PROFILE_PATTERN_INSIDERAGG |
| news21/23/29/3/31/52/54/7/73/76/81、fundamental86/93、model16/27/29/32/37/68/77/252/257、option1(cov0)、risk68/71、macro27、imbalance5 等 cov=0 集 | cov=0→lc<100 先验 4/4（f89 78-94/f72 26-68/risk72 25-62/BE47 三集） | master 表终局补记 / WAVE_BE47 |

## 三、约束冻结（非数据问题）

| 范围 | 依据 |
|---|---|
| ANALYST/MODEL/OTHER/SHORTINTEREST 全部数据集（新增投入） | 用户 11-11 23:35「已点亮的塔不再投入」（PIVOT_UNLIT_TOWERS） |
| 全部 D0 数据集 | 用户裁定「先不考虑 D0」（D0_FROZEN_20261110） |
| TOP300/TOP800 宇宙 | 平台拒绝，仅 TOP500 可用 |

## 四、已点亮塔存量画像（冻结前已归档）

analyst7/9/93/factor_signals（ANALYST）、model25/26/28/30/106/109/216/250/264 等（MODEL）、
other47/455/384/532/545/699（OTHER）、shortinterest3（SHORTINTEREST）——
字段画像 CSV 全在档；历史波结论见 tracking/mining/result_*.json 与 deu_priors.json。

## 五、交付侧索引

- 交付清单：FINAL_DELIVERY_REPORT_11ALPHAS_20261111.md（11 颗全指标+算子逻辑）
- 提交暂存：SUBMIT_STAGING_INDEX_20261111.md（终验补记 08:5x）
- 换防选项：SWAP_AUDIT_88NmN37X_20261112.md
- 可复用方法论：FINAL_DELIVERY_REPORT 九条 M1-M9 + REUSABLE_METHODOLOGY_20261110.md
