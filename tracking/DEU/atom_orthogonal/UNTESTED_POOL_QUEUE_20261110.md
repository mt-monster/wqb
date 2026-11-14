# 未派发模板池队列（DEU D1，2026-11-10 20:1x 第三版·核实完毕）

> 修订史：v1 把「文档 hasRun=false」误当「未派发」；v2 纠正 institutions25/workforce/other699（已跑完）；v3 核实 ern6/earnings_sent_matrix 亦已跑完。

## 一、真实剩余面（全部核实过）

| 序 | 数据集 | 塔 | 塔位 | 状态 |
|---|---|---|---|---|
| ✅1 | fund_holdings_panel | institutions | 1/3 | **BA5 在飞**（sim 46JbfOnj4XdcyoUc4gpkL，10 条，确证首派） |
| 2 | insiders1 | insiders | 0/3 | **从未测**（8 VECTOR cov0.534，无方向字段但可用 holdings 差分推方向）——本文件同目录 waveBA6 设计 |

## 二、核实为「已跑完封盘」的池（全列出，避免再误判）

| 数据集 | 证据 | max S |
|---|---|---:|
| other699 | 12 臂全落（T2 活跃度 zscore504 最佳） | 0.84 |
| institutions25 | 12 臂全落（T10 条件交互最佳） | 0.61 |
| workforce_flow_skills | 12 臂全落（T8 流失率 gate×净流入） | 0.96 |
| earnings_sent_matrix | 12 臂全落（M11 概率变换净差最佳，失望腿为主载体） | 0.63 |
| ern6（earnings6/SUE） | 探针闸未过：SUE 0.40 / cap 分组 0.26，且 2014-2018 五年全空窗 | 0.40 |
| pv30 | 11 臂（returns×分组轴），多数挂 REVERSION 警告 | 0.79 |
| pv29 | 字段自测否决：50 字段全是统计行业簇标签（MATRIX/GROUP），不能做单数据集信号 | — |
| institutions6 | 波 AG 新骨架二次判死（符号混乱=真噪声） | — |
| news20/news50/news104/news17/news29/news38 | BA3/BA3b + 历史波全测（事件情绪族天花板 0.31-0.73） | 0.57 |
| sentiment7/27/33/earningscall/event_sent/socialmedia12 | 全族闭环（天花板 0.64-1.02） | 1.02 |
| risk60/risk88 | BA1-BA2b 六维合规终判死 | 0.90 |

## 三、塔规则排除（不构成可挖面）

- analyst46/analyst9/analyst_earnings_ibes/analyst44：ANALYST/MODEL 塔已点亮（6/3）。
- shortinterest3 池：塔已 3（点亮）。
- 全部 PV 内建价格机制（波 W：S≤0.94 符号混乱）。

## 四、结论（与 FINAL_STATUS 一致）

DEU D1 单数据集 ATOM 剩余面 = **fund_holdings_panel + insiders1**，共 2 个候选；
这与「DEU 域内可交付上限 4-5 颗」的判断一致——绝大多数已设计池都已实测封盘。
若要突破 5 颗，需要：① 用户授权 3 颗待提交件；② insiders1 出货；③ 放开双塔组合配额（如 PV×NEWS 等集合外×集合内，≤5 个）。