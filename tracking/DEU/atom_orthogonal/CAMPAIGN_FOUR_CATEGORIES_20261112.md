# 四类深挖战役计划（INSIDERS / INSTITUTIONS / SENTIMENT / RISK，2026-11-12 深夜启动）

> 用户指令：四类逐数据集回测，机制尽可能多，模板从平台论坛 + 外部金融论文按字段画像匹配。
> 本战役覆盖此前「快速判死」的四类，用机制丰富的模板库重新深耕；每集一个 10 臂机制波，收割后按协议 v2 升级（≥1.2 满波 / 1.0-1.2 定向 / <1.0 该集判死——但判死证书必须列已试机制数）。

## 模板来源（已核实）

**论坛（高赞直对口）**
- 70 赞 DEU 专帖「内部人信念强度」：动了多少仓位 > 动了多少钱 ⇒ **conviction ratio = 交易股数/交易后持仓**，只有相对仓位异常重的一笔冒出来（insiders1 直接适配）
- 43 赞证伪帖：内部人字段必须**先时间聚合**（脉冲→连续强度）再**横截面标准化**（大盘股天然强度高一个量级）
- 31 赞「买侧已写烂」：买侧拥挤，卖侧欠挖；别用 8-K 文本
- 57 赞「insider × institution 残差对冲」：披露节奏差（跨类组腿，受禁混配额限制）
- 4 赞 EUR 实证「两个不同量纲交易额相除 0.77→1.89」：**量纲相除**是大杠杆
- 28 赞 institutions6 三族口径：存量（held/aggregate）/ 流量（acquired/disposed）/ 广度（count）分族配比
- 52 赞机构波动负号：ts_std_dev(机构持仓占比,66) 高 = 观点分歧期 → 做空（M 形净值→平滑，1.55→2.76 先例）
- 30 赞 IVA/MFM/CNI 三分法：保险/顾问持仓比 = 稳定性因子
- 31 赞「别用裸 sentiment」：relevance 加权 + 新颖度过滤
- 29 赞 risk60 特质波动率之谜（Ang et al 2006 高 IVOL 低收益）⇒ 反向 IVOL
- 16/24/28 赞波动率/尾部/beta 因子族

**论文**
- Cohen-Malloy-Pomorski 2012（JF）Decoding Inside Information：**高管（top）比董事（non-top）知情** ⇒ 高管净买/董事净买分离
- Lakonishok-Lee 2001：内部人**买入**有预测力、卖出没有 ⇒ buy-side intensity + sell 仅作分母
- Yan-Zhang 2009：机构**持仓变化**短期有预测力（fast traders）⇒ ts_delta(aggregate_share_count)
- Da-Engelberg-Gao 2011（JF）In Search of Attention：关注度（搜索量/流量）高 → 短期反转/过度定价 ⇒ sentiment27（Tranco 网站排名）与 sentiment7（Wikipedia 页面浏览）直接适配；Fang-Peress 2009 无关注溢价（低关注 → 正溢价）
- Ang-Hodrick-Xing-Zhang 2006：IVOL 之谜 ⇒ 反向特质波动；Baker-Bradley-Wurgler 2011 低 beta 异常
- Nofsinger-Sias 1999 机构羊群；Gompers-Metrick 2001 机构需求变化 ⇒ demand shift 定价

## 数据集 × 波次（按信息含量排序）

| 波 | 数据集 | 字段面 | 机制族 |
|---|---|---|---|
| **BE103 已派**（3nIvC3gYa4CNanOmJswGDgt） | institutions6（11 MATRIX，cov 1.0） | 净流量值/净流量比/广度净差/人均买入强度/流量持续性/持仓变化/流量×广度交互/**持仓波动负号**/**买入/存量比**/衰减持续性 | Yan-Zhang + 羊群 + 52 赞波动 + conviction |
| **BE104 已派**（3udRMT95j4o0bjzrTkCx3vM） | insider_agg_matrix（34 MATRIX） | 买卖流量比/**高管−董事分离**/人均强度比/大额交易值/方向指标 Δ/**方向×量级交互**/高管−全体差/**卖侧负号**/直接交易净差/**买入占比(66d)** | CMP 2012 + LL 2001 + 43 赞聚合 |
| BE105 | sentiment27（Tranco 网站热度，cov 0.90） | 排名动量/关注度尖峰/排名偏度/峰度/relpopularity 双 α 差/排名 zscore/低关注溢价/域数量扩张/流量稳定性(CV)/热度变化率 | Da-Gao 2011 + Fang-Peress |
| BE106 | fund_holdings_panel（18 字段，cov 0.93） | 边界交易/稳定新仓 21d/HHI 集中度/大额交易数/conviction 交易/账户数/交易值分布分 | 羊群 + 聪明钱持续性 |
| BE107 | sentiment33（255 字段多方法 NLP，cov 0.32） | Method 6/7/8/9 集成均值/方法间分歧/负面取反/词频计数/Δ | 多模型共识 + 分歧度 |
| BE108 | insiders1（8 字段） | **conviction ratio（70 赞 DEU 配方）**/量纲相除（EUR 1.89 先例）/significance 加权/交易后持仓变化/卖侧 | 信念强度 |
| BE109 | institutions4 + institutions1 | 持仓变化（current vs previous shares）/组合占比变化/市值变化/ conviction | 巨鲸跟随 |
| BE110 | institutions25（24 字段空头持仓）+ risk88 | 存在性探针（crowding/total_short_interest/activity）+ risk88 单字段 | 空头拥挤 |
| BE111 | risk60/68/71/72 | 反向 IVOL/低 beta/波动变化/tail/风险条件化 | Ang 2006 + BBW |

## 纪律

- MATRIX 字段一律直接裸用（vec_ 包裹 = 类型错连坐整批——BE102 实证）
- 每臂算子 ≤12；比例分母一律 add(...,0.0001) 防 0
- 设置档：decay4/SUBINDUSTRY/trunc0.08/nan ON（事件型字段按新判据：无事件=真值⇒ON）
- 收割后 |S|≥1.2 先查 longCount/shortCount（空心件拦截）
- 判死证书必须列「已试机制族数」——判死的是机制面，不是数据集名
