# insiders12 · 10 模板 TemplatePlan v2（2026-11-23，按用户铁律重起：≥10 模板 + 论坛/论文来源 + 单模板穷尽串行）

> **规则**（template-10-source-gradient-order）：① ≥10 模板 ② 每模板标注论坛帖/论文 DOI 来源 ③ 单模板完整梯度（算子逐类别全替换+参数精调+多配置）穷尽后才许下一个 ④ 弱模板精简梯度需说明理由。
> 配置基准：TOP2500 / CROWDING / decay4 / trunc0 / nan ON / maxTrade OFF。
> 已测遗产（首批 10 臂，见画像 §4）：T1'流量÷存量44d=−0.32（取反+0.32 稳定弱负）、T2'percent z252=−0.21、T3'percent 水平=−0.23、T4'密度63d=−0.24、T5'金额=−0.24、exchange/长窗无改善。**本轮 10 模板全部与已测结构互异。**

## 0. 取证留痕（EVID 闸已过）

### 0.1 论文（paper_search.py --diverse：20 篇 / 16 作者）

| DOI | 标题 | 年 | 挂靠模板 |
|---|---|---|---|
| 10.1093/rfs/6.1.79 | Insider Trading as a Signal of Private Information | 1993 | M1/M2 信号方向 |
| 10.1002/9781119200697.ch7 | The Insider Trading Anomaly | 2012 | M3 异常检测 |
| 10.1080/00036846.2014.937035 | Insider ownership and financial flexibility | 2014 | M4 ownership 水平 |
| 10.1016/j.jcorpfin.2023.102389 | Common ownership constrains managerial rent extraction | 2023 | M5 集中度 |
| 10.1080/13504851.2024.2399748 | Insider trading profitability: managerial ability | 2024 | M6 盈利能力条件 |
| 10.2139/ssrn.3744165 | Insider Ownership and Investment Efficiency | 2020 | M7 ownership×投资 |

### 0.2 论坛（MCP）

| 帖 | votes | reading |
|---|---:|---|
| 44731710962839 内部人三信号对齐 | 3 | **三腿 rank 后 add + 加权衰减**（ts_weighted_decay）；单一字段会被事件日历打穿 |
| 44673331508503 group_backfill | 23 | `group_backfill(ts_rank(f,252),subindustry,63,std=2)` 标准用法 |
| 44491324058775 ts_backfill 指南 | 6 | insider 数据是 ts_backfill **最佳用例**（稀疏申报）|
| 45145827440919 KOR Tips | 12 | `(-1)*alpha` 不是镜像——反向必须单独重测（已做）|
| 44770798147735 ATOM 65 赞 | 65 | ATOM 豁免 6 分组字段含 **country/exchange**（本集英国子集关键）|

## 1. TemplatePlan（10 模板，每模板一行，全与已测结构互异）

| # | 核心字段 | reading（机制假设） | template（骨架） | 来源 | 与已测互异点 |
|---|---|---|---|---|---|
| **M1** | amount÷sharesheld, ts_weighted_decay | 三信号对齐帖：稀疏申报会被日历打穿 ⇒ **加权衰减替代 ts_sum**（近期权重大） | `group_rank(ts_weighted_decay(divide(vec_sum(amount),add(vec_sum(sharesheld),1)),k=8),subindustry)` | 帖44731710962839 | 衰减替代求和（新算子） |
| **M2** | amount÷percent | 内部人增仓占**总股本**比（percent 作分母=跨公司可比，RFS1993 私有信息信号） | `group_rank(tail(group_backfill(ts_sum(divide(vec_sum(amount),add(vec_avg(percent),1)),44),subindustry,66),lower=0.25,upper=0.75,newval=0.5),subindustry)` | 论文 10.1093/rfs/6.1.79 | 分母换 percent（新比值） |
| **M3** | amount 的 z 相对自身 | Insider Anomaly：**交易行为偏离自身基线**才是信号（非绝对量） | `group_rank(ts_zscore(ts_backfill(divide(vec_sum(amount),add(vec_sum(sharesheld),1)),66),252),subindustry)` | 论文 10.1002/9781119200697.ch7 | z 化（首测批用的是 ts_sum 无 z） |
| **M4** | percent × amount 方向 | ownership 水平**加权**交易方向：高持仓内部人的交易更有信息 | `group_rank(tail(group_backfill(ts_sum(multiply(divide(vec_sum(amount),add(vec_sum(sharesheld),1)),vec_avg(percent)),44),industry,66),lower=0.25,upper=0.75,newval=0.5),industry)` | 论文 10.1080/00036846.2014.937035 | 交互项（amount×percent） |
| **M5** | sharesheld 变化率 | 交易后持仓的**变化**（不是存量水平）= 内部人仓位调整速度 | `group_rank(ts_delta(ts_backfill(vec_sum(sharesheld),66),66),industry)` | 论文 10.2139/ssrn.3744165 | sharesheld 的 delta（此前只测过 percent） |
| **M6** | amount 正负分离（只买） | Insider Purchase Anomaly：**只有买入**有预测力（卖出多因流动性） | `group_rank(tail(group_backfill(ts_sum(greater(vec_sum(amount),0),44),industry,66),lower=0.25,upper=0.75,newval=0.5),industry)` | 论文 10.1002/9781119200697.ch7 | greater 门控（买/卖分离，全新形态） |
| **M7** | 买卖比（笔数） | 买笔数÷卖笔数（方向强度，非金额） | `group_rank(tail(group_backfill(divide(ts_sum(greater(vec_sum(amount),0),44),add(ts_sum(less(vec_sum(amount),0),44),1)),industry,66),lower=0.25,upper=0.75,newval=0.5),industry)` | 帖44731710962839（买卖强度腿） | 笔数比值（新形态） |
| **M8** | amount×mktprice ÷ percent市值代理 | **金额占持股价值比**（value-weighted 强度，mktprice 作换算） | `group_rank(tail(group_backfill(ts_sum(divide(multiply(vec_sum(amount),vec_avg(mktprice)),add(multiply(vec_sum(sharesheld),vec_avg(mktprice)),1)),44),industry,66),lower=0.25,upper=0.75,newval=0.5),industry)` | 论文 10.1016/j.jcorpfin.2023.102389 | 金额/持仓市值（无量纲新比值） |
| **M9** | percent 的截面分位 | ownership **截面分位**（哪些公司内部人占比异常高）| `group_rank(ts_backfill(vec_avg(percent),66),country)` | 论文 10.1080/00036846.2014.937035 + 帖44770798147735 | **country 分组**（英国子集同组可比，ATOM 豁免字段） |
| **M10** | amount 的 trade_when 稀疏门控 | 申报稀疏 ⇒ 只在**有申报的日子**更新信号（状态化持仓） | `trade_when(greater(vec_count(amount),0),group_rank(ts_backfill(divide(vec_sum(amount),add(vec_sum(sharesheld),1)),66),subindustry),-1)` | 帖44734752518039 + LC97552 模板 | trade_when 状态化（全新形态） |

## 2. 串行执行序（单模板穷尽后才下一个）

| 序 | 模板 | 探针 | 梯度范围（若 |S|≥0.5 或有稳定方向） | 精简梯度理由（若弱） |
|---|---|---|---|---|
| 1 | M1 加权衰减 | 1 臂 | ts 16 全替换 + k 参数 3 档 + 分组轴 + 配置 2 档 | — |
| 2 | M2 percent 分母 | 1 臂 | 同上 | — |
| 3 | M3 z 化 | 1 臂 | 同上 | — |
| 4 | M4 交互项 | 1 臂 | — | 首批 T5'（金额）已证弱，交互项精简为内层 4 算子+窗 3 档 |
| 5 | M5 sharesheld delta | 1 臂 | — | 同上精简 |
| 6 | M6 只买门控 | 1 臂 | 同上 | — |
| 7 | M7 买卖笔数比 | 1 臂 | 同上 | — |
| 8 | M8 金额/持仓市值 | 1 臂 | — | 首批 T5' 弱 ⇒ 精简 |
| 9 | M9 country 分位 | 1 臂 | 分组轴 4 + 窗 3 | — |
| 10 | M10 trade_when | 1 臂 | 门控条件 3 档 + 内层 4 | — |

**预期总臂**：探针 10 + 梯度（强模板 ~30/个 ×2~3 个 + 弱模板 ~8/个 ×7）≈ 110–130 臂。
