# DEU D1 数据集可用性总表（2026-11-11，本战役全部实测汇总）

> 覆盖本战役累计实测的 20+ 数据集。字段数/覆盖率取自平台，S 天花板取本轮实测最高值。

| 数据集 | 类别/塔 | 字段数 | 覆盖率 | 实测 S 天花板 | 判定 | 支撑交付件 |
|---|---|---:|---|---:|---|---|
| **shortinterest3** | SHORTINTEREST | 25 | 0.653-0.783 | **1.72** | ✅ 主力 | 78Yk8VR1 / qM7KxkQV / Jj8VQwoe |
| **insiders1** | INSIDERS | 8 | 0.534 | 0.85（单）/1.72（组合腿） | ✅ 优质第二腿 | qM7KxkQV |
| **other47** | OTHER | 18 | 0.502-0.652 | 1.65（组合腿） | ✅ 可用 | Jj8VQwoe |
| **anl93** | ANALYST | 993 | 0.5-0.7 | **1.62** | ✅ ATOM 有效 | GrW9OxmG |
| **analyst（est_12m_*）** | ANALYST | — | 0.5-0.7 | **2.02** | ✅ 最强族 | zq3eb7No / RREPm361 |
| **fundamental6** | FUNDAMENTAL | 196 | 0.188-0.66 | **1.73**（仅 oiadpq 单点） | ⚠ 极窄 | Wje5K71x（存量） |
| fundamental89 | FUNDAMENTAL | 407 | 0.0（实际 lc 78-94） | 0.69 | ❌ 死 | — |
| fundamental17 | FUNDAMENTAL | 135 | 0.0 | <1.0 | ❌ 死（11-07 atom_fundamental 历史探针复核） | — |
| fundamental45 | FUNDAMENTAL | 12 | 0.269 | 0.99 | ❌ 死（11-07 X3 正交三轴，S 差 60%，杠杆穷尽） | — |
| fundamental90 | FUNDAMENTAL | 66 | 0.0(实有) | 1.02 | ❌ 死（2Y 0.42 内禀，2023 信号死亡） | — |
| fundamental22 | FUNDAMENTAL | 1 | 0.69 | 0.48 | ❌ 死（11-07 vec_avg 水平 2 几何） | — |
| **pattern_scores** | **PV(未点亮)** | 504 | **0.9888** | 0.71 | ❌ 探针级死（BE44 5 模板） | — |
| **insider_agg_matrix** | **INSIDERS(未点亮)** | 34 | 0.534-1.0 | 0.84 | ⚠ 弱存活（directional 族），低于升级线 | — |
| socialmedia39 | SOCIALMEDIA | 1 | 0.275 | — | ⛔ 画像级排除（ticker ID 列表无数值含义） | — |
| institutions1 | INSTITUTIONS | 7 | 0.229 | 0.41 | ❌ 探针死（BE45 2 臂：-0.35/0.41，cov 不足） | — |
| fundamental72 | FUNDAMENTAL | 1031 | 0.0 | 未单独实测 | ⚠ 待验（低拥挤 152 用户） | — |
| fundamental45 | FUNDAMENTAL | 12 | 0.269 | 未单独实测 | ⚠ 待验 | — |
| opt1_* | OPTION | — | — | **0.62** | ❌ 死（3 臂全灭，2Y 非负即零） | — |
| rsk60_* | RISK | — | — | **0.93** | ❌ 弱 | — |
| risk60 / risk88 | RISK | — | — | 0.90 / 0.79 | ❌ 六维合规死 | — |
| inst25_* | INSTITUTIONS | — | — | 0.90 | ❌ 弱 | — |
| institutions25 | INSTITUTIONS | — | — | 0.61 | ❌ 死 | — |
| institutions6 | INSTITUTIONS | — | — | 符号混乱 | ❌ 死 | — |
| fund_holdings_panel | INSTITUTIONS | — | — | 0.65 | ❌ 弱 | — |
| news20/nws18/news50/news38 | NEWS | — | — | **1.52**（nws20×I7 线，31 臂） | ❌ **终审判死**（六维穷尽，BE43B 档案） | — |
| mws50 | NEWS | — | — | 未单独实测 | ⚠ 待验 | — |
| lending_fee_bid_rate | RISK（实测塔标） | — | — | 1.20 | ❌ 弱 | — |
| workforce_flow_skills | OTHER/INST | — | — | 0.96 | ❌ 弱 | — |
| other699 | OTHER | — | — | 0.84 | ❌ 弱 | — |
| earnings_sent_matrix | EARNINGS | — | — | 0.63 | ❌ 弱 | — |
| ern6（SUE） | EARNINGS | — | 2014-2018 五年空窗 | 0.40 | ❌ 死 | — |
| oth384（电话会） | OTHER | — | — | 未单独实测 | ⚠ 待验 | — |
| snl27 / socialmedia12 | SOCIALMEDIA | — | — | 0.73 | ❌ 死 | — |
| pv29 / pv30 | PV | 50 / — | — | 0.79 | ❌ 信号死；**pv29 转用途：聚类标签是 MATRIX，group_* 不可直接用，需 bucket(rank(·)) 桥接**（BE46 ERROR 实证；BE46b 在验） | — |
| sentiment7/27/33 | SENTIMENT | — | — | 0.64-1.02 | ❌ 死（s33 小样本幻觉四波 32 臂；s7 六波 48 探针 0.71） | — |
| opt1_deltasurface | OPTION | — | — | 0.62 | ❌ 死 | — |

## 可用性结论

1. **有效族只有 4 个**：shortinterest3（1.72）、analyst/anl93（2.02/1.62）、insiders1（作为第二腿）、other47（作为第二腿）
2. **fundamental6 是单点有效**（仅 `fnd6_newq_oiadpq` 配特定双窗口骨架），同族其他 20 字段全负
3. **待验的还有 4 个**：fundamental17（135 字段）、fundamental72（1031 字段，仅 152 用户，低拥挤）、fundamental45、oth384、mws50
4. **已死 15 个**：opt1 / risk60/88 / institutions6/25 / earnings_sent / ern6 / socialmedia12 / pv29/30 / sentiment7/27/33 / fundamental89

## 下一步优先级（若授权继续）

1. **fundamental72**（1031 字段、仅 152 用户、286 个 alpha）—— 低拥挤度高字段数的唯一剩矿，用 Wje5K71x 骨架做单点扫描；
2. **shortinterest3 的 `_p5_d1` 变体**（覆盖率 0.783 > 基础 0.653）—— BE21 在验；
3. fundamental17（135 字段、636 用户）—— 拥挤度中等，可作次选。

## 增补记录（2026-11-11 全类目普查后）

- 按 category 枚举 DEU D1 全 172 集对照历史战役，勘误：fundamental17/45/90/22 已由 11-07 atom_fundamental 战役实测判死（此前误标「待验」）；
- **新发现两个从未回测的未点亮塔数据集**：pattern_scores（PV，cov 0.9888 全场最高）与 insider_agg_matrix（INSIDERS，cov 0.534-1.0）→ BE44 探针已派；
- socialmedia39 单字段为 ID 列表，画像级排除；
- Vkxnb8QG（pv30，10-30 期全闸遗留件）**已死**：self 0.9589 撞 LLM93nGa（11-03 提交），不再入篮。

## 终局补记（2026-11-12 BE47 后：数据集空间 100% 探针闭合）

| 数据集 | 塔 | 类型/覆盖 | 最佳 S | 判定 |
|---|---|---|---:|---|
| continuation_score | PV(未点亮) | MATRIX/cov0 | 0.42 | ❌ 探针死 |
| intraday_pv_feats | PV(未点亮) | MATRIX/cov0 | 0.31 | ❌ 探针死 |
| pv109 | PV(未点亮) | VECTOR债券/cov0.467 | 0.42 | ❌ 探针死 |

- 172 集全部处置：实测/探针关闭/画像排除/约束冻结；cov=0→lc<100 先验 4/4；IS 池近失扫描（128 件）无遗漏近失候选。
