# ★DEU D1 塔级关闭清单（2026-11-11 收口）

> 全部 12 个未点亮塔 + 4 个已点亮塔的实测状态。每塔一行，含天花板、封堵理由、档案指针。

## 一、未点亮塔（可投面）—— 全部关闭或探针级弱

| 塔 | 数据集 | 天花板 S | 状态 | 封堵理由 | 档案 |
|---|---|---:|---|---|---|
| EARNINGS | earnings6 | **0.80（真实）/ 2Y 0.19** | ❌ **关闭（四面 v2 全证书）** | ① EAT 日历：ts_min_max_cps inaccessible（BE62）② EAT 近似重建：ts_zscore 全负 −0.65~−0.42（BE64）③ PEAD 快慢手：max 0.60 且 TO 70-77%（BE63）④ **EPS surprise 面（BE99，用户解禁覆盖后实采）**：真实 0.80（累计 surprise，lc 91/127 健康），2Y 仅 0.19；另发现 **|S|1.25 空心臂（lc/sc=0）已作废** | WAVE_BE99_EARNINGS6_VERDICT_20261112.md |
| EARNINGS | earnings_sent_matrix | 0.63 | ❌ | 单字段弱 + cov 0 | master 表 |
| INSTITUTIONS | institutions1 | 1.73（历史件） | ❌ **关闭** | 自锁 0.9287（自家 2rmGAPqN）+ 簇轴承重 + 20 算子超预算 | INST1_FAMILY_FINAL_CLOSE_20261111.md |
| INSTITUTIONS | institutions6/25/4/1、fund_holdings | 0.27-0.65 | ❌ | 覆盖/强度不足 | INSTITUTIONS_FAMILY_FINAL_20261111.md |
| INSIDERS | insiders1 + insider_agg_matrix（三正交排序） | **1.27 / F 0.95 / 2Y 1.37 / sub 0.64** | ⚠️ **定型（80 臂全证书）** | **Δ66（变化）× ts_ir（信噪比）× HHI（集中度）三正交排序 + 嵌套 sector→market 外层**；距 S 闸 0.31 / F 闸 0.05 / 2Y 闸 0.21；单调变换在 group_rank 下空操作；行业中性会剥掉个股 alpha（market 外层 +0.13S）；门控类全灭 | INSIDERS_FINAL_REPORT_20261111.md |
| INSIDERS | insider_agg_matrix | 0.84 | ⚠️ 弱存活 | 覆盖 0.53，方向指标族有效 | WAVE_BE44 |
| SENTIMENT | sentiment27 | 0.95 | ❌ | 水平面有效但强度不足；慢速变量 | WAVE_BE27_28 |
| SENTIMENT | sentiment7 | 0.66 | ❌ | 六波 48 探针，2Y 全负 | deu_priors.json |
| SENTIMENT | sentiment33 | 0.57 | ❌ | 小样本幻觉（覆盖扩大后 R 翻负） | SENTIMENT33_FULL_VERDICT |
| NEWS | news20 | 1.52 | ❌ 判死 | 31 臂七维穷尽，三档无改善；分组轴换到原生簇仍 1.42-1.49 | WAVE_BE43B_NEWS_FINAL_CLOSE |
| NEWS | news17/18/38/50/104 | 0.29-0.79 | ❌ | 事件情绪通道在 DEU 无定价力 | WAVE_BE38 |
| RISK | risk60/88/72/71/68 | 0.30-0.90 | ❌ | 描述性无方向 / TO 违规 / lc 稀疏 / cov 0；risk72 replicator BE55 终证（lc 74-98，|S|≤0.2）；risk68/71 复活探针 BE89 在飞 | RISK_FAMILY_REAL_PROFILE / WAVE_BE53_54_55_VERDICT |
| FUNDAMENTAL | fundamental6 | 1.73（oiadpq，已占槽） | ⚠️ 槽位占 | oiadpq 已被 Wje5K71x 占用 | DATASET_DISPOSITION_MAP |
| FUNDAMENTAL | fundamental45 | 0.99（2Y 1.89） | ❌ | S 差 60%，杠杆穷尽 | atom_fundamental 终审 |
| FUNDAMENTAL | fundamental90 | 1.02（2Y 0.42） | ❌ | 2023 内禀死亡 | atom_fundamental 终审 |
| FUNDAMENTAL | fundamental17/22/72/86/89/93/1 | <1.0 | ❌ | 历史探针全灭 | atom_fundamental 终审 |
| OPTION | option1 | 0.62 / 0.39 | ❌ **关闭（v2 证书）** | 10 臂穷尽（BE53 XZZ 微笑 7 臂全负 S-0.17~-0.39，lc 157 数据在但无定价力） | WAVE_BE53_54_55_VERDICT_20261112.md |
| PV | pattern_scores | 0.71 / 0.32 | ❌ **关闭（v2 证书）** | 15 模板穷尽（BE54 LoMW+Peak 10 臂 max 0.32，lc 150） | WAVE_BE53_54_55_VERDICT_20261112.md |
| PV | continuation_score / intraday_pv_feats / pv109 | 0.42/0.31/0.42 | ❌ | 探针死 | WAVE_BE47 |
| PV | pv1 | 0.75（符号反） | ❌ | 价格反转在 DEU 不成立（外部报告结论不迁移） | WAVE_BE66 |
| PV | pv29 / pv30 | — / 0.79 | ❌ | 簇标签非信号 / tm 族拥挤 | master 表 |
| PV | pv1+pattern_scores 组合族 | **1.21**（量窗3） | ❌ **关闭（v2 全证书）** | 24 臂九维穷尽（BE86-88）：S≥1.09 区 2Y 全负、2Y 正区 S≤1.03，双闸结构性不可达；10/10 REVERSION warning | WAVE_BE87_BE88_PV_L3_20261112.md |
| PV×INSIDERS | pv20+insd1 冠军族 | **1.41 / 2Y 1.56** | ⚠️ **PROVISIONAL 封顶（102 臂）** | 62 结构 + 10 nan（OFF 崩 0.16）+ 10 trunc/封装 + 10 earnings 换腿 + **10 Δ 腿换腿（BE112：Δ132 腿 1.41 新天花板、三腿 1.39/F1.11；Δ 腿 S 涨 2Y 跌跷跷板腿级复现）** ⇒ 约束内正式无破闸路径 | PV20_FAMILY_FINAL / BE97/100/101/112 |
| MACRO | macro27 | 0.09 | ❌ **关闭（实测证书）** | BE93 4 臂：jobsactive/jobscreated × 水平/Δ66/zscore252，|S| 0.00-0.09 且符号互翻 ⇒ 非方向错而是无信号（TO 4.6-15% 证数据在）；推翻 cov=0 先验 | WAVE_BE93_VERDICT_20261112.md |
| PV | pv47（spret 特异收益） | 1.01（负向） | ❌ **关闭（实测证书）** | BE93 3 臂：spret z −0.35 / spret Δ66 −0.11 / for_stats spret z −1.01；TO 72-91%、2Y ≤0.57、sub 全负 | WAVE_BE93_VERDICT_20261112.md |
| NEWS | news52（电话会议） | 0.13 | ❌ **关闭（实测证书）** | BE93 3 臂：chars_in_qa/participants/corporate_participants 全 0.07-0.13，TO 仅 2.6% ⇒ 稀疏事件计数死法（同 EUR insiders1） | WAVE_BE93_VERDICT_20261112.md |
| FUNDAMENTAL | alpha_factor_lib（65 字段 VECTOR） | 0.49 | ❌ **关闭（实测证书）** | BE95 10 臂：max S 0.49（利润增长 1Y，2Y 1.13），**TO 0.9-6.6%**（10/10 ≤6.6%）⇒ 年度财务口径与 D1 频率不匹配；全平台 alphaCount 仅 4 却无信号 ⇒ 不拥挤≠有信号 | WAVE_BE95_VERDICT_20261112.md |
| NEWS | news50 / news18 / news104（事件**流量计数**面） | 待测 | ⏳ **BE98 在飞** | news50 在 BE38 只按情绪通道验过（0.29-0.79），计数面（rp_story_event_count / multi_entity_story_event_count cov 0.98）从未测；EUR 同源机制是唯一非模型胜件（S 2.72/prod 0.64） | WAVE_BE98_NEWS_FLOW_20261112.md |
| IMBALANCE | imbalance5 / order_book_imbalance | — | ❌ | 外部报告：订单失衡类 DEU 零覆盖 | DEU_EXTERNAL_MAP |
| SOCIALMEDIA | socialmedia12 / 39 | 0.73 / — | ❌ | 弱 / ID 列表无数值语义 | master 表 |
| 复活面（news81/23/73、risk68/71、pv103/106/13、digital_ad_spend） | NEWS/RISK/PV/FUND | 0.86 | ❌ **关闭（网格级 v2 证书）** | 38 臂全灭（存在性 18 + L1 网格 20）：网格 max 0.79(pv103)/0.70(news81 计数，全矩一致负)/0.51(pv13，2Y 2.07 复现但前段拖死)；画像 cov=0 全部证伪（lc 45-165） | WAVE_BE89_90 + WAVE_BE91_92_L1_GRID |

## 二、已点亮塔（用户 11-11 指令冻结）

| 塔 | OS | 说明 |
|---|---:|---|
| ANALYST | 8 | 预估族被 9 件 OS 占用，外部报告亦判「生产池结构性饱和 0.71-0.72」 |
| MODEL | 7 | 同上 |
| OTHER | 4 | oth455 簇/关系字段被 3 件占用 |
| SHORTINTEREST | 5 | 融券池仅 ~260 只 ⇒ CONC 结构性墙 |

## 三、结论

**DEU D1 在用户约束集（未点亮塔 + ≤12 算子 + 禁混 ≤5 + 双品类 + D1/TOP500）内，
所有可探明信号面已关闭；剩余缺口无法靠新波次填补，只能靠用户裁定调整约束。**