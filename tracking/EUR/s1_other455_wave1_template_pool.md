# other455 · EUR/TOP2500/D1 字段画像与模板池（第一波）

> 数据集：`other455` · category=OTHER · 1500 字段 · coverage 竞对 0.9705 / 客户 0.8691 / 合作 1.0 · 平台 alphaCount 3407 · userCount 753 · valueScore 3
> 采集：2026-11-06 · 用途：按画像匹配结构互异模板 → 派发 → 回收归因

## 一、命名骨架拆解（画像核心）

字段名 = `oth455_<relation>_<param>_<w>_<output>`

| 维度 | 取值 | 语义 |
|---|---|---|
| relation | `competitor` / `customer` / `partner` / `relation` | 新闻共现网络的关系类型：竞争对手 / 客户 / 合作伙伴 / 泛关联 |
| param | `n2v_p10_q50` / `n2v_p10_q200` / `n2v_p50_q50` / `n2v_p50_q200`；另有 `roam` 变体（无 p/q） | news2vec 训练参数：p=游走返回概率、q=进出概率（node2vec 的 p/q），q 同时是语料分位档 |
| w | `w1` .. `w5` | 同一配置下 **5 次独立随机游走实现**（集成，天然多实现） |
| output | `pca_fact{1,2,3}_value`（MATRIX） / `kmeans_cluster_{5,10,20}`（GROUP） / `pca_fact{k}_cluster_{5,10,20}`（GROUP） | 输出两类：<br>**MATRIX = 嵌入空间 PCA 因子坐标**（可作信号腿）<br>**GROUP = 在嵌入空间做的 KMeans 簇标签**（只能作分组轴，簇数 5/10/20） |

### 关键结构事实

1. **MATRIX 信号腿只有 `pca_fact{1,2,3}_value` 一族**，共 4 relation × 4 param + roam ≈ 数十个，不随 cluster 后缀变化。
2. **GROUP 字段占绝大多数（1500 里约 3/4）**，它们的用途是 **替换 `industry` / `sector` / `subindustry` 作自定义分组轴**，不是信号腿。这与 CLAUDE.md「有些字段适合做 group 或 bucket 自定义分组」对齐。
3. **天然集成结构**：同一 (relation, param) 下有 w1–w5 五个独立实现 ⇒ 可直接构造「实现间背离」与「实现间一致性」两类二阶信号，无需外部数据。
4. **天然参数轴**：p/q 四档 ⇒ 可构造跨参数价差（长窗 vs 短窗嵌入漂移），代理信息扩散速度。
5. **天然关系轴**：competitor / customer / partner 三条关系 ⇒ 可构造跨关系价差，把「竞争挤出」与「供应链信息传导」分开。

## 二、文献与论坛先验（模板来源）

| # | 来源 | 结论 | 对应模板 |
|---|---|---|---|
| P1 | Cohen & Frazzini (2008), *Economic Links and Predictable Returns*, JF | 经济关联（客户-供应商）而非统计相关驱动收益可预测性；客户收益领先供应商 | T2 / T3 |
| P2 | Rizova (2010), *Return Predictability along the Supply Chain: The International Evidence*, FAJ 66(3) | **22 个发达市场**（含欧洲）客户行业收益领先供应商行业；按滞后客户收益排序多空年化异常收益至 **15%** ⇒ **EUR 有直接国际证据，不必担心美市独占** | T2 |
| P3 | Guo, Peng, Tao & Tu, *Joint News, Attention Spillover, and Stock Returns* | **新闻共现网络**度量投资者注意力溢出，是市场与截面收益的强预测器 ⇒ 直接对应 news2vec 机制 | T5 / T7 |
| P4 | Breiman (1996) bagging 方差分解 | 同一模型多次重采样的输出方差 = 参数不确定性，可作独立信号维度 | T4 / T10 |
| P5 | 论坛《Cluster Alpha 与普通 Stock Alpha 的根本区别》 | 用聚类簇替代行业做分组，属「同叙事同侪」相对定位，与 GICS 行业正交 | T7 / T8 |
| P6 | 论坛《【KOR/D1】Cluster Test 上线实测：4 条 group_rank 类 alpha 的 Cluster Sharpe 均低于 1.58》 | ⚠ 反面证据：`group_rank` 类在 Cluster 口径下普遍偏弱。**本波以常规 REGULAR 闸为准**，同时记录 group_rank 占比，若整波 S 偏低优先怀疑此因 | 全局设置 |
| P7 | Freeman (1979) 网络中心度 | 中心度 ≠ 影响力方向：竞争网络中心度高可能是被抢份额（负），合作网络中心度高是资源获取（正）⇒ 两条关系应异号 | T3 |

## 三、12 个结构互异模板（差异落在骨架 / 算子几何 / 矩 / 分组轴 / 非线性）

记 `Fk`=competitor pca_fact1（p10_q200 w1）、`Fc`=customer pca_fact1、`Fp`=partner pca_fact1、`W{n}`=competitor pca_fact1 的第 n 次实现、`CLUSTER{n}`=kmeans_cluster_n。

| 编号 | 模板 | 骨架 | 差异维度 | 来源 | 方向先验 | 算子数 |
|---|---|---|---|---|---|---|
| T1 | 网络位置水平（基线） | `group_rank(ts_zscore(Fk,252), industry)` | 水平量 + 时序标准化 | 自建基线 | 正 | 2 |
| T2 | 客户−竞争跨关系价差 | `group_rank(ts_backfill(subtract(ts_zscore(Fc,252), ts_zscore(Fk,252)),22), industry)` | **跨关系轴一阶差**（非时间差分） | P1/P2 | 正 | 5 |
| T3 | 合作−竞争价差 | `group_rank(subtract(ts_zscore(Fp,252), ts_zscore(Fk,252)), industry)` | 跨关系轴差，异号假设 | P7 | 正 | 4 |
| T4 | 随机游走实现背离 | `group_rank(ts_backfill(subtract(ts_zscore(W1,252), ts_zscore(W5,252)),22), industry)` | **同模型两次实现之差**（集成方差代理） | P4 | 负 | 5 |
| T5 | news2vec 参数背离 | `group_rank(subtract(ts_zscore(P10Q200,252), ts_zscore(P50Q50,252)), industry)` | **超参数轴价差**（长窗 vs 短窗嵌入漂移） | P3 | 正 | 4 |
| T6 | PCA 二阶曲率 | `group_rank(subtract(rank(F2), rank(F1)), industry)` | **主成分几何**（正交分量差） | 自建 | 待定 | 4 |
| T7 | 自定义分组轴 | `group_rank(ts_zscore(Fk,252), CLUSTER20)` | **分组轴替换**（行业 → 新闻共现簇） | P5 | 正 | 2 |
| T8 | 组内中性化几何 | `group_neutralize(rank(ts_zscore(Fk,252)), CLUSTER10)` | **中性化算子几何**（group_rank → group_neutralize∘rank） | P5 + 慢信号档 | 正 | 3 |
| T9 | 网络位置迁移速度 | `group_rank(ts_delta(ts_zscore(Fk,63),22), industry)` | **矩阶**（水平 → 一阶时间差分） | 自建 | 正 | 4 |
| T10 | 实现符号一致性 | `group_rank(ts_mean(sign(subtract(ts_zscore(W1,252), ts_zscore(W4,252))),63), industry)` | **非线性**（sign 截断幅度，只留方向一致性） | P4 | 正 | 6 |
| T11 | 三关系共识计数 | `group_rank(add(sign(Fk), add(sign(Fc), sign(Fp))), industry)` | **离散计数几何**（跨关系符号求和） | 自建 | 正 | 5 |
| T12 | 信噪比归一 | `group_rank(divide(ts_zscore(F1,504), ts_std_dev(F1,252)), industry)` | **二阶矩归一**（幅度 / 自身波动） | 自建 | 正 | 4 |

全部模板算子数 ≤ 12（硬上限），无 `directional_*` 毒字段，无 if_else 双分支复制。

## 四、派发记录

批级设置（单一，不得混档）：EUR / TOP2500 / D1 · neutralization=SLOW_AND_FAST · decay=8 · truncation=0.08 · unit_handling=VERIFY · nan_handling=ON · pasteurization=ON · max_trade=ON。

| 批 | multisimulation_id | 模板 | 表达式要点 | 状态 |
|---|---|---|---|---|
| B1 | `1FQeLB4jS5ifaqcoLfJ5imq` | T2 + T1 | 客户−竞争价差；合作网络位置水平 | 已派发（子任务未注册） |
| B2 | `2gEyuF8vI4OCajbFb20DeAy` | T4 + T6 | 实现 w1−w5 背离；PCA 二阶曲率 | 已派发（子任务未注册） |
| B3 | `3ogMlqaIQ4kuasF1bHjQTcaq` | T7 + T8 | 自定义分组轴 cluster_20；组内中性化 cluster_10 | 已完成：S 0.22 / 0.16 |
| B4–B6 | **不再派发** | — | 6 骨架已达判死门槛 | 取消 |
| B4 | 待派 | T3 + T5 | 合作−竞争价差；参数轴背离 | 待槽位 |
| B5 | 待派 | T9 + T11 | 位置迁移；三关系共识 | 待槽位 |
| B6 | 待派 | T10 + T12 | 符号一致性；信噪比归一 | 待槽位 |

## 五、风险与判死门槛

1. **PCA 因子量纲未知**：首波必须先看 T1 基线是否出量级合理的信号；若 T1 与 T2 同时 S<0.3 且 coverage 正常 ⇒ 信号腿不可用，剩余 10 个模板不再派发（省 5 批）。
2. **GROUP 字段作分组轴的合法性**：`group_rank(x, GROUP字段)` 平台接受，但需首波验证不报错。
3. **判死门槛**：同一面 ≥6 个结构互异骨架全灭才判死；2–3 个骨架为负只降级。
4. **塔位**：OTHER 塔 EUR 已 2/3，再出 1 颗即点亮；本数据集全程单数据集 ATOM，不占两塔配额，也不触碰 {PV,MODEL,OTHER,FUNDAMENTAL} 禁混。

## 六、★ 收批结论：信号腿判死（6 骨架全灭），GROUP 字段保留作外挂分组轴

| 模板 | alpha | S | F | 2Y | sub | TO | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| T1 合作网络位置水平 | `omEPmrM2` | 0.31 | 0.06 | 0.59 | 0.31 | 3.1% | 灭 |
| T2 客户−竞争价差 | `GrWQrxAZ` | 0.29 | 0.05 | 0.58 | 0.13 | 3.0% | 灭 |
| T4 实现 w1−w5 背离 | `LLM8L3pn` | −0.05 | 0.00 | −0.37 | −0.12 | 3.5% | 灭 |
| T6 PCA 二阶曲率 | `ZYQXYNp0` | 0.28 | 0.05 | 0.20 | 0.21 | 2.7% | 灭 |
| T7 自定义分组轴 cluster_20 | `GrWQ1XW0` | 0.22 | 0.04 | 0.60 | 0.20 | 3.4% | 灭 |
| T8 组内中性化 cluster_10 | `mLoKwdoX` | 0.16 | 0.02 | 0.35 | 0.10 | 3.3% | 灭 |

**最优 0.31，距 REGULAR 线 1.58 差 1.27** ⇒ 不是参数问题，是机制问题。三条可外推的判据：

1. **TO 全部 2.7–3.5%**（本区正常信号 8–25%）⇒ news2vec 的 PCA 坐标是**慢变结构描述符**，截面几乎不动，天然没有换手也没有 alpha。这是「数据在但信号不在」的典型形态：coverage 0.87–1.0 完全正常，S 却贴地。
2. **换分组轴没有改善反而更差**（T1 industry 0.31 → T7 cluster_20 0.22）⇒ 说明该因子与行业高度共线，自定义簇只是把同样的行业信息切得更碎。**「自定义分组轴」不是万能杠杆**，前提是被分组的因子本身要有非行业成分。
3. **实现间背离 T4 为 −0.05** ⇒ 5 次随机游走的实现差异里没有可提取的不确定性溢价，embedding 已足够稳定。

**保留价值**：`kmeans_cluster_{5,10,20}` 与 `pca_fact{k}_cluster_*` 这 ~1100 个 GROUP 字段，可作为**其它数据集信号腿的外挂分组轴**（替换 industry）。但那是两塔混合（OTHER × 其它），受「集合内×集合外 ≤5 类」「每两塔组合 ≤3 颗」配额约束，且当前 OTHER 塔已 2/3，需要时再评估。

