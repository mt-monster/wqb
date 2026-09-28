# EUR D1 other455：客户网络分组的增量信息探针

## S-PRE / S0 选择依据

最新252已闭环，0个完整合格，旧库存仍受PV×MODEL/加权混合或相关性约束。analyst9的修正广度/陈旧度及analyst10的预测惊喜已有失败证据，不重跑同机制。other455在EUR/TOPCS1600/D1可用：coverage .9599，1500字段，alphaCount293，userCount142，category OTHER，S0 score .814、tier2、hard_excluded=false。未找到该集/客户网络机制的dead_end。

本次将other455作为有依据的有限探索加入白名单：客户网络提供区别于财报数值的分组参照；不是把tier2改称平台高质量，也不降低提交标准。使用GROUP标签而非无经济方向的PCA坐标。竞争者/伙伴字段描述与EUR存在歧义，暂不采用。

## S1 字段与证据边界

- `oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5`：GROUP，coverage .8691，users0，alphaCount0；平台描述明确为D1-lagged EUR customer Node2Vec(P10,Q200)、seed1的KMeans五组标签。w1是种子，不能当成时间窗口。
- `returns`：pv1 MATRIX，coverage1，users714，alphaCount1798，仅作为公开收益基线。使用前已逐字段MCP核实。没有MODEL字段；不含加权混合。
- 数值腿只有returns；冷门GROUP参照不是独立已验证信号。2个唯一输入中1个冷门，四个实验均固定该冷门轴；高使用者returns只做方向和增量对照，不进行参数打磨。
- scan_fields任务`campaign_EUR_S1_20260924_232453`已实查1500字段（1200 GROUP、300 MATRIX）。现有field_type=signal不能覆盖平台type=GROUP；以真实类型决定用法。
- 完整分布/逐日分组成员/网络历史构建过程未获得。元数据覆盖不是每日有效持仓保证，D1标注也不能单独证明历史网络不存在回填。首次回测需核查实际持仓、单位、CW、RN和2Y；通过初筛后再核对历史可得性。

## 特征工程建议与可证伪假设

[Cohen与Frazzini原始论文](https://pages.stern.nyu.edu/~afrazzin/pdf/Economic%20Links%20and%20Predictable%20Returns%20-%20Cohen%20and%20Frazzini.pdf)研究直接客户—供应商关系的信息传导；[node2vec原论文](https://arxiv.org/abs/1607.00653)描述保留网络邻域的嵌入。这里仅推断客户网络聚类可能提供经济关联代理，不能把同簇股票等同实际客户，亦不能声称复现论文收益。

H1：同客户网络簇近一个月的共同收益可能捕捉缓慢传播的信息；与个股一个月动量对照，判断是否只有自身动量暴露。H2：个股落后于同簇共同收益可能产生补涨；与个股一个月反转对照，判断网络是否增加信息。

事先固定22交易日约一个月、seed1、k5、EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/truncation.08；不扫种子、簇数或窗口。group_mean包含自身，不能据此作无自身污染的因果解释；若初筛有价值，必须补排除自身和持仓掩码诊断。

对照用group_count>0保持同一网络可用性条件；缺组填0。摘要持仓计数一致仍不能证明每日掩码完全一致。该明确掩码也进入原式清单，不在选择时删除。

**Dataset**: other455
**Region**: EUR
**Delay**: 1

**Concept**: Customer-network common return drift
**Mechanism**: Test whether the one-month common return of a customer-network cluster contains information beyond own-stock momentum. The cluster label is only a grouping axis; it is not a direct customer identity. Fix seed and cluster count before testing. Expected exposure: network common-demand momentum.
**Fields**: oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5, returns.
**Implementation Example**: `rank(group_mean(ts_sum(returns,22),1,densify({oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5})))`

**Concept**: Own momentum control on available customer-network universe
**Mechanism**: Missing-group-aware own one-month momentum control for the network-drift hypothesis; group labels only determine data availability and are never numerically ranked. Expected exposure: own price momentum.
**Fields**: oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5, returns.
**Implementation Example**: `if_else(greater(group_count(returns,densify({oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5})),0),rank(ts_sum(returns,22)),0)`

**Concept**: Customer-network relative catch-up
**Mechanism**: Test whether a stock lagging the common one-month return of its customer-network cluster catches up, holding the same horizon and network definition. Compare against own-stock reversal to separate network information from mechanical reversal. Expected exposure: network-relative price adjustment.
**Fields**: oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5, returns.
**Implementation Example**: `rank(subtract(group_mean(ts_sum(returns,22),1,densify({oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5})),ts_sum(returns,22)))`

**Concept**: Own reversal control on available customer-network universe
**Mechanism**: Missing-group-aware own one-month reversal control for the network catch-up hypothesis. Reuse the exact grouping availability mask from the momentum control; do not optimize the high-user returns field. Expected exposure: own price reversal.
**Fields**: oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5, returns.
**Implementation Example**: `if_else(greater(group_count(returns,densify({oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5})),0),reverse(rank(ts_sum(returns,22))),0)`

## 实验预算与停止条件

最多4条：2主假设、2必要对照，全部经GEM生成，按身份清单执行；不因8条传输批量而填充。四项共享分组轴和收益字段是配对设计要求，max-field-repeat设4并在清单记录，不能据此声称四个独立字段机制。六维多样性不足须显式登记有限探针例外。

若出现单位/分组兼容性错误先关闭该失败执行并精确修复，不删核心分组逻辑凑过门。若主假设不达S≥1.25且F≥.8，或收益由同方向对照解释，关闭本轮结构，不扫描w2/w3/k10/k20；只读证据可以留存。达到资格后先查Prod/Self、逐年、RN和覆盖，再按Mode B解释差异；无论原始Sharpe多高均不算完成目标。

## S2 / 门禁执行证据（23:42）

- GEM任务`gem_1790264035_634722`真实生成4条，源ID52433–52436；selection_w253按身份选4/4，目标ID52437–52440，零自动注入、零缩水。原式没有在选择环节被改写。
- GROUP支持已贯通GEM入口、下游CLI及字段实现器；GROUP字段不再生成rank(label)/ts_delta(label)孤儿数值变体。主实现与内嵌副本同步。
- S2 workflow干跑地区门禁通过；沿用已复现的封装300秒等待问题的权威CLI路径。独立预检先发现缺旧版reference消费文件，由preflight --repair从DB生成后再次预检全PASS；未手写字段目录。
- 第一次gate因本地densify拒绝数据集GROUP标识符而4/4 FAIL，未发模拟。已修复语法层的标识符识别，仍拒绝densify数值表达式及把densify输出作数值信号。清除该数据集仅有的4条旧错误缓存，再跑gate4/4 PASS。
- 完整测试1411 passed、10 skipped，45.78秒；技能同步4个安装位。这里的1411是工程验证，不是Alpha数量。
- 体检包缺失仍以warn记录；六维结构多样性例外只适用于事先定义的4条匹配探针。质量预测2弱/2硬拒仅为旧模型标签，不冒充已发生的回测结果。
- S3任务`batch_track_EUR_253_20260924_234159`，真实模拟批`3GdY8S8yn4sg9kVr2gnHy93`，4条在飞，尚无Alpha结果。

## S3 / S4 / S6 完成结果（23:51）

上述在飞状态已结束：4条均返回Alpha，pipeline收割4/4，0执行错误；平台子任务均WARNING（REVERSION_COMPONENT），其警告不得抹掉。

| 机制 | Alpha | S / F | 2年阶梯S | RN S | 多/空数 |
|---|---|---|---:|---:|---:|
| 网络共同收益 | j2Aej6Le | .32 / .10 | .76 | -.07 | 639 / 614 |
| 自身动量对照 | xA31jNal | .00 / .00 | .43 | .08 | 736 / 762 |
| 网络相对滞后 | O0NJ7GK1 | .16 / .04 | .29 | .07 | 624 / 628 |
| 自身反转对照 | gJbWj8vv | -.00 / -.00 | -.43 | -.08 | 762 / 736 |

2年阶梯来自实时IS_LADDER_SHARPE的year=2；S4缓存two_year_sharpe为null，已单独记录口径限制。四条均无UNITS警告，但RA失败4/5项，Prod/Self仍未知。

网络式和对照的持仓总数不同，不能把S提升作网络独立贡献的干净证据；本轮raw强度也明显不足。停止该固定结构和参数扩展，不判死整个other455。掩码、PIT、自身贡献的问题写入research_leads_w253，剩余预算0，待新证据重开。

S4任务campaign_EUR_S4_20260924_234745、S6任务campaign_EUR_S6_20260924_235031均成功；wave_results253已closed/FAIL，s6_verdict_253与精确范围registry已写库。经验文件见[other455](dataset_experience/eur_other455_campain.md)、[辅助pv1](dataset_experience/eur_pv1_campain.md)。本战役累计49条完成，完整合格仍0/10。
