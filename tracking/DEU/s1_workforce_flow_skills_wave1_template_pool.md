# s1_workforce_flow_skills_wave1_template_pool — DEU/TOP500/D1 · Global Workforce Flow and Skills（workforce_flow_skills）

> 状态：探针 P1-P6 设计中，双预检后派发（runner 2/2）。
> 字段面（全 VECTOR·月频）：employee_inflow/outflow_count_2（雇入/离职）、employee_headcount_2、position_seniority_level_2(1-4)、employee_prestige_score_2、total_salary_amount_2。
> **禁信号腿**：unreliable_user_count/inflow/outflow（数据质量元数据，look-ahead 类）。

## 机制先验（两读 + 外部文献）

1. **陈坚《The Return Predictability of (Un)expected Labor Flow》**（web_search）：净劳动力流动分解为预期/非预期两成分——**预期成分长期与收益显著负相关（现金流通道）**、**非预期成分短期显著正相关（贴现率通道）**。⇒ 双面机制：预期面反转 / 非预期面动量。
2. **RFS《Information Dispersion across Employees and Stock Returns》**（36353193394455 + 35849719386647 两帖复现）：rank-and-file 入职/辞职决定反映未来盈利能力，月度环比员工数构建因子。
3. **《招聘变化与业务扩张》92 赞（43322749748503）**：亲测简化模板 `group_rank(ts_delta(vec_avg(<招聘字段>), 21), industry)`（21→22 月度白名单映射）；关键消融=删收入条件 IS 反升（Sharpe 3.00）、vec_sum→vec_avg 口径、报告条数分层。

## 探针 P1-P6（定方向，单边）

| # | 面 | 骨架 | 方向先验 | 来源 |
|---|---|---|---|---|
| P1 | 非预期净流入 | zscore 自身基线(22/504) of (vec_sum(inflow)−vec_sum(outflow)) | 动量（非预期→短期正） | 陈坚 |
| P2 | 预期流量 | -ts_rank(ts_mean(净流入,252),252) | 反转（预期高→长期负） | 陈坚 |
| P3 | 招聘变化率 | group_rank(ts_delta(vec_avg(inflow),22), sub) | 动量 | 92赞照抄臂 |
| P4 | 流失率 | -divide(vec_sum(outflow), vec_sum(inflow)) | 高流失→空 | 自建（比值纪律） |
| P5 | 职级重心 | ts_delta(ts_mean(vec_avg(seniority),22),22) | 高管扩张→多 | 自建 |
| P6 | 净增长率 | divide(净流入, vec_avg(headcount)) | 扩张→多 | 自建（比值纪律） |

## 开放问题（≥3）

① 陈坚「预期/非预期」分解在 DEU/TOP500 月频字段上是否成立（P1 vs P2 方向分离）？
② 92 赞的 vec_sum→vec_avg 口径差异在 inflow/outflow 上是否复现（探针用 vec_sum 聚合，正式波加 vec_avg 对照臂）？
③ 月频字段在 D1 回测里的换手形态——事件月度跳变，ts_mean 平滑窗多大才不抹平信号？
④ seniority/prestige 聚合均值是「人才质量流入」还是「岗位结构漂移」？（P5 读数 + 正式波 split 臂分离）

## PC/SC 占位

- PC/SC 未测；与 oth699 T2 同属 zscore 自身基线家族——P1 若出货先查互相关。

## 正式波模板池 T1-T12（≥10 结构互异；待探针读数定/翻方向）

| # | 家族 | 骨架 | 窗口 | 方向先验 | 来源 |
|---|---|---|---|---|---|
| T1 | A 非预期×SNR | divide(ts_zscore(net,66), ts_std_dev(ts_zscore(net,5),22)) | 66/5/22 | 动量 | 107赞 SNR 骨架 × 陈坚非预期 |
| T2 | A 非预期×gate | trade_when(vec_avg(seniority)>ts_quantile(.,252), P1core, -1) | 22/504/252 | 动量·高管扩张过滤 | 自建（gate 合规） |
| T3 | B 预期×长窗 | -ts_rank(ts_mean(net,504),252) | 504/252 | 反转 | 陈坚预期面 |
| T4 | B 预期×增速 | -ts_delta(ts_mean(net,252),66) | 252/66 | 反转 | 陈坚 |
| T5 | C 招聘×vec_avg 对照 | ts_delta(vec_avg(inflow),5) | 5 | 动量 | 92赞消融②（短窗） |
| T6 | C 招聘×自身基线 | divide(subtract(ts_mean(vec_avg(inflow),22), ts_mean(.,504)), ts_std_dev(.,504)) | 22/504 | 动量 | zscore 自身基线 |
| T7 | D 流失×zscore | -divide(subtract(ts_mean(divide(vec_sum(outflow),vec_sum(inflow)),22), ts_mean(.,504)), ts_std_dev(.,504)) | 22/504 | 高流失→空 | 比值纪律 × 自身基线 |
| T8 | D 流失×gate | trade_when(divide(vec_sum(outflow),vec_sum(inflow))>ts_quantile(.,252), -ts_rank(ts_mean(net,22),252), -1) | — | 交互 | 自建（gate 合规） |
| T9 | E 职级×水平 | -ts_rank(ts_mean(vec_avg(seniority),252),252) | 252 | 低职级扩张→多（RFS rank-and-file） | RFS |
| T10 | F 增长率×rank | ts_rank(divide(net, vec_avg(headcount)),252) | 252 | 扩张→多 | 比值纪律 |
| T11 | G 声望流入 | ts_rank(ts_mean(vec_avg(employee_prestige_score_2),22),252) | 22/252 | 人才质量→多 | 自建 |
| T12 | G 薪酬趋势 | ts_delta(ts_mean(vec_avg(total_salary_amount_2),22),22) | 22 | 薪酬扩张→多 | 自建 |

注：net = subtract(vec_sum(inflow), vec_sum(outflow))。交互臂一律 trade_when gate 形式（禁 add/multiply 混信号）。P1-P6 探针臂不重跑。

## 八、探针收批归因与翻向修正（2026-11-03，6/6 全落）

| 探针 | 形态 | S | TO | 读法 |
|---|---|---:|---:|---|
| P1 非预期净流入动量（zscore 自身基线） | zscore(net,66)/std(zscore(net,5),22) | +0.37 | 7.6% | 净流入正向 |
| P2 预期流量反转 | -ts_rank(ts_mean(net,252),252) | -0.37 | 5.8% | 陈坚反转假说 DEU 证伪 |
| P3 招聘变化率照抄（92 赞帖） | ts_delta(vec_avg(inflow),22) | +0.17 | 3.3% | 论坛模板 DEU 弱迁移 |
| P4 流失率比值翻负 | -outflow/inflow（水平） | -0.35 | 9.3% | 翻错向 |
| P5 职级重心 | ts_delta(ts_mean(seniority)) | -0.11 | 9.2% | 弱负，与 T9 反转同向 |
| P6 净增长率 | net/headcount | +0.37 | 9.3% | 扩张正向 |

**方向结论**：labor flow 在 DEU 单面正向（流入/净流入扩张 → 多），陈坚「预期流量反转」面未兑现（P2 严格反号）。P2/P4 的 multiply(.,-1) 翻向与探针证据相悖。

**翻向修正（派发前执行，4 臂）**：T3/T4/T7/T8 核心腿去 multiply(.,-1) 改正向；T9 职级反转保留（P5 同向）。翻向属方向定案（同 news29 P4 先例），非调参。

**派发记录**：workforce_w1_20261103（pid 73264，T1-T12 共 12 条）；翻向 4 臂双预检通过（verify_expr 4/4 valid + preflight 零未知字段）。

## 九、正式波 T1-T12 收批归因（2026-11-03，12/12 全落，max|S|=0.96 判弱封盘）

| T | 形态 | S | TO | alpha_id | 读法 |
|---|---|---:|---:|---|---|
| T1 | 净流入 zscore 自身基线 | 0.00 | **0.0%** | O0AGK0vp | **退化臂**（见下诊断） |
| T2 | 预期×职级 gate | 0.34 | 6.7% | JjeGRjL2 | 交互弱正 |
| T3 | 长窗 rank 正向(504/252) | 0.08 | 5.9% | kqNPeRvz | 翻正后归零（探针 P1 0.37 未复现） |
| T4 | 增速正向(252/66) | -0.02 | 6.8% | 9qxpgodr | 归零 |
| T5 | 招聘 ts_delta(5) | 0.00 | **0.0%** | e753e9G6 | **退化臂** |
| T6 | 招聘 × 自身基线 | 0.17 | 7.1% | leAWJ8G5 | 弱正 |
| T7 | 流失率 zscore 正向 | -0.51 | 7.3% | kqNPe8a6 | **翻正后转负 = 原 -1 是对的** |
| **T8** | **流失率 gate × 净流入 rank** | **0.96** | 7.4% | qMLNe551 | 全场领跑（唯一 gate 交互成功臂） |
| T9 | 职级反转(252) | 0.23 | 3.9% | 6XdpPXdp | 弱正 |
| T10 | 净增长率 rank(252) | 0.07 | 9.3% | bl6Q2l6m | 归零 |
| T11 | 声望流入 rank | -0.49 | 5.5% | 0mYpkWPG | 反向 |
| T12 | 薪酬趋势 | -0.38 | 8.1% | wpQawVod | 反向 |

**★★ 退化臂诊断（T1/T5，TO=0.0 与 S=0.00 双零，新踩坑）**：
劳动力流量是**月频稀疏数据**，在日频窗口上：
- **T5** 「ts_delta(vec_avg(inflow), 5)」：5 日内无新数据点 ⇒ **恒零**，整条表达式退化为常数。
- **T1** 「ts_zscore(x,66)/ts_std_dev(ts_zscore(x,5),22)」：日内 ts_zscore(x,5) 在同一月内恒定 ⇒ std 分母退化 ⇒ 输出常数。
**判据**：S=0.00 且 TO=0.0 是**数据频率错配的退化签名**，不是「弱信号」。遇到必须换窗口到 ≥22（月频至少一个完整周期）或直接弃臂，**不能记入弱信号证据**。

**模板级归因（三条结论）**：
1. **唯一成功面 = 流失率 gate × 净流入信号（T8 0.96）**：劳动力市场的**条件化**（高流失期才看净流入）有效，而单面水平（T3/T4/T7/T10）全部归零或反号 ⇒ 与 news29 结论一致：**DEU/TOP500 单面慢变量几乎无残余 alpha，只有「条件/状态切换」能榨出微弱信号**。
2. **翻向决策部分证伪**：探针 P2/P4（-0.37/-0.35）被解读为「反转错向」并翻正 T3/T4/T7/T8，但正式波长窗下 T3=0.08 / T4=-0.02 / **T7=-0.51（翻错）**，只有 T8 借 gate 翻身。⇒ **探针短窗的方向判定不能直接外推到长窗结构**；翻向应只对「探针与正式波结构同构」的臂执行。
3. **声望/薪酬族（T11 -0.49 / T12 -0.38）反向**：高声望人才流入、薪酬扩张在 DEU 是**负向**信号（成本压力 > 质量溢价），与文献先验相悖，以实测为准。

**封盘判定**：max|S|=0.96 < 1.58 的 61%，T8 虽为唯一亮点但单臂无组合腿可用 ⇒ **workforce_flow_skills 判弱封盘**，不追投。



