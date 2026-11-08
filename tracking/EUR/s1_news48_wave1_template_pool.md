# S1 模板池 · EUR/D1 news48 (Global News Data / 新闻文本统计量) wave1 备靶 · 2026-11-05

> 硬约束：模板库 ≥10 个结构互异模板；差异落在 骨架结构 / 算子几何 / 矩(水平·一阶差分·二阶方差) / 分组轴 / 非线性变换，换窗口不算。来源 [F]平台论坛 [P]外部论文(OpenAlex/arXiv 独立核验) [S]自建。
> 全部为 单数据集 ATOM：仅 news48 内部字段 + 平台内置 group 轴(sector)，不含 returns / price / volume 腿 —— 规避 §82「returns 腿被计入 PV 塔」；补 NEWS 塔(当前 1/3)，不占塔组合配额。派发后按 platform pyramid 实测确认塔位，不预判。
> 本池 §95 首批(T05/T06)已于 §96 收批、§96 递进探针(T03/T13 时序分位)已于 §97 收批：时间平滑成功破换手墙(TO 158%→47%、CW FAIL→PASS)但 S/2Y 归零(T05 0.76→T03 −0.06)⇒ 高 S 是「靠 158% 换手兑现的日频噪声」、非可提取 alpha，信号本身横截面弱。§97 派最后跨几何终验(T09 vec_sum 计数 / T11 vec_stddev 二阶矩，multisim 3HirxTDL4IfaCt26gC8b8O 收批在途)：这是 wave1 最后一批，若仍 0/2 则 6 骨架全灭正式判整集收手。后续批次派发前须再过 toolkit_static 静态闸(create_multi_simulation 时触发，preflight 查不到)。

## 字段面（MCP get_datafields，EUR/TOP2500/D1，22 字段 100% 拉全 complete=true / platform_count=22）
- 全 VECTOR，coverage 全 0.6326，alphaCount 1–24、userCount 1–11（低拥挤）。起手一律 vec_* 聚合。
- 六大语义族（论坛 33566303033751 Step1 逐字释义）：
  - 综合/实体情绪：nws48_ssc(综合)、nws48_ess(实体)、nws48_qcm(股票多分类)、nws48_qep(全球股票)、nws48_qmb(社论评论)。
  - 主题情绪：nws48_acb(企业行动)、nws48_bam(并购)、nws48_bee(盈利评估)、nws48_ber(盈利发布)。
  - 新颖性/注意力：nws48_ens(实体24h新颖度)、nws48_g_ens(全球24h新颖度)、nws48_ens_elapsed / g_ens_elapsed(新颖性链首末间隔 ms)、nws48_ens_similarity_gap / g_ens_similarity_gap(距相似故事天数)、nws48_nip(未来2h市场影响预测)、nws48_ghc_lna(分析师推荐变化)。
  - 积极度/活跃度：nws48_aes(91d 积极事件占比)、nws48_vea(91d 事件计数)。
  - 相关度/实体数：nws48_relevance(实体相关度)、nws48_rp_story_event_count(每 story 实体记录数)、nws48_rp_story_event_index(实体出现顺序)。

## 论坛取证（本轮 MCP read_forum_post 读正文含评论）
- [F] 33566303033751「Data Idea系列3：Global News Data_news48」(WL13229)：22 字段逐字经济含义 + Step3 十个特征工程方案（overall_news_sentiment / sentiment_novelty_ratio / action_earnings_sentiment_diff / relative_event_novelty / analyst_sentiment_correlation / news_impact_per_event / sentiment_stability / event_novelty_trend / positive_event_density / sentiment_relevance_product）。
  - ★ 负向先验（评论）：XC66172「用 vec_avg 回测方案1(综合情绪均值水平) 没有信号」⇒ T01/T02 的水平均值族是对照臂，不是指望出货的主臂；WL13229「没有 vector_choose 会带来困难、可暂时放弃」⇒ 不能用取最后一个时点值；ZH34713 在 IND/TOP500 用 vec_norm(field)+ts_backfill(·,5)+group_median，但 vec_norm 在 EUR 不合法（见下）；QD44113 提「信息熵」思路（相似度缺口/事件数离散度可作二阶代理）。
- [F] 43794115713431「Vector 字段：先聚合，还是先研究事件结构？」(YX50005)：vec_avg(整体水平) / vec_sum(事件总量) / 极值(异常冲击) / 事件数量(活跃度) / 离散程度(分歧) 五种聚合的经济含义互不相同，评论 HZ55211 追问「条数 = vec_avg×条数，须与当天覆盖变化区分开」⇒ T09(vec_sum 事件计数) 与 T11(vec_stddev 离散度) 是刻意保留的独立几何轴，不与 vec_avg 水平族混为一谈。
- [F] 论坛 43541109631895（历史已读，§86）：Da 抽象成「异常注意力代理 → 时序分位 → 反向持仓」三步模板、60 日季窗是甜点。
- [F] 论坛 41995684467479（§6133，历史已读）：事件/低频字段别盲用长窗 ts_rank(252/66)，改 ts_decay_linear(d=10/20) 或 ts_backfill 对齐事件日；本池主体短窗(1/5/22) + T03/T13 两条 66 长窗单变量对照。

## 外部论文独立核验（web_fetch OpenAlex/arXiv HTTP200，逐篇取摘要；web_search 402 余额耗尽、S2 429，走备用通道）
- [P] Tetlock (2007) JF「Giving Content to Investor Sentiment」doi 10.1111/j.1540-6261.2007.01232.x，被引 4790：媒体悲观 → 股价下行压力后回归基本面，异常高/低悲观 → 高成交量；与「媒体内容是新信息代理」理论不一致 ⇒ 情绪是短期反转/噪声交易代理，方向上支持「情绪极端值反向」而非顺势（T03 分位反向的理论锚）。
- [P] Da, Engelberg & Gao (2011) JF「In Search of Attention」doi 10.1111/j.1540-6261.2011.01679.x，被引 3046：SVI 注意力↑ → 未来 2 周股价↑ → 年内反转；注意力须取相对自身历史分位 ⇒ 支持「异常关注度(个股 vs 全局) + 时序分位」几何（T05/T13）。
- [P] arXiv 2309.05560「New News is Bad News」：用 RNN 熵度量新闻文本分布变化(新颖性)，新颖性↑ → 未来一年负收益、横截面熵暴露带负风险溢价 ⇒ 直接给 nws48_ens/g_ens 新颖性族负号方向先验（T05/T06/T07 取 -rank）。
- 语义核验结论：三篇一致指向「新闻/情绪的水平顺势弱、极值/新颖性反向强、须相对化(自身分位或个股-全局差)」。这与 §91(T01 换手墙/T05 方向反转)、§92(中心矩族字段本身弱) 的 EUR 实证同向，故本池不以水平均值族为主臂，把权重放在相对化/新颖性/二阶矩几何。

## ★ 算子/门禁实测坑（本轮 preflight 抓到，落入 S1 台账）
- vec_norm 在 EUR 不在算子白名单：preflight 14 条里 T13 原版 rank(ts_backfill(vec_norm(nws48_qep),5))（照抄 ZH34713 IND 实测）被判 unknown_fields:["vec_norm"]、valid:false。与历史 clamp / ts_vector_neut / ts_max / quantile(x,120) 同类——论坛/跨区表达式是概念骨架，非目标区合法式，直接派会整批连坐 CANCELLED。已改写成 EUR 合法版（T13 用 vec_avg + subtract + ts_rank）。
- 修正后 preflight 14/14 valid、unknown_fields=[]、any_changed=false、platform_field_count=12；22 个 VECTOR 字段全部手动 vec_* 包裹（不依赖 auto_fix 改动）。
- 算子数（每个实例计 1）：[2,2,4,4,4,2,4,2,2,4,2,4,6,3]，最大 6 ≤ 12 上限，符合「上限 12、越少越好」。
- toolkit_static 静态闸只在 create_multi_simulation 触发，preflight 查不到；派发时须确认无 [INACCESSIBLE_OP] / arity 连坐。

## 窗口口径（硬约束：日1/周5/月22/季66；其它值须解释+实证）
- 主体 5 / 22 / 短 decay：ts_backfill(·,5) 周窗对齐事件日、ts_backfill(·,22) 月窗（§6133 事件字段半衰期）、ts_delta(·,5) 周度一阶差分。
- T03 / T13 保留 66(季) 长窗作单变量对照：论坛 43541109631895 指 60 日季窗是注意力甜点；配合 news18「四季窗 2Y 全灭」与 news52「短窗非万能解」反证，长窗只留 2 条对照、不铺开。
- 与 §6133 + news52 反证配合：若整池 2Y 全灭，先分「字段真衰减 / 窗口匹配错 / 字段本身横截面弱」三因，用同字段族单变量只改窗长做干净对照，别只押短窗。

## 模板池（14 个，结构互异；全部 EUR preflight 通过，算子 ≤6）
| # | 来源 | 机制 / 结构轴 | 表达式骨架 | 算子数 | 经济含义 / 方向先验 |
|---|---|---|---|---|---|
| T01 | [F][S] | 综合情绪·水平均值（对照臂） | rank(vec_avg(nws48_ssc)) | 2 | 整体新闻情绪水平；论坛 XC66172 实测 vec_avg 无信号 ⇒ 负向对照，验证「水平弱」 |
| T02 | [F][S] | 实体情绪·水平反向 | -rank(vec_avg(nws48_ess)) | 2 | 实体基调取反；与 T01 组成「同族方向」对照（§91 方向反转先验） |
| T03 | [P][F] | 综合情绪·时序分位反向（66 长窗对照） | -rank(ts_zscore(ts_backfill(vec_avg(nws48_ssc),22),66)) | 4 | Tetlock 2007 极端悲观→回归基本面；取相对自身历史分位反向；66 窗对照 |
| T04 | [F] | 主题情绪差·横截面结构 | rank(subtract(vec_avg(nws48_acb),vec_avg(nws48_bee))) | 4 | 企业行动 vs 盈利评估情绪差（论坛方案3）；捕捉业务面关注差异 |
| T05 | [P][F] | 相对新颖度·个股/全局比（反向） | -rank(divide(vec_avg(nws48_ens),vec_avg(nws48_g_ens))) | 4 | 论坛方案4 + arXiv 2309.05560 新颖性↑→负收益；个股相对全球新颖度 |
| T06 | [P] | 实体新颖度·水平反向 | -rank(vec_avg(nws48_ens)) | 2 | arXiv 2309.05560 负号先验；纯水平，作 T05 相对化的对照 |
| T07 | [P][S] | 新颖度·一阶差分短窗 | -rank(ts_delta(ts_backfill(vec_avg(nws48_ens),5),5)) | 4 | 新颖性变化率(周)；§6133 短窗对齐事件日；检验「变化量 vs 水平」 |
| T08 | [F] | 相似度缺口·水平（信息熵代理） | rank(vec_avg(nws48_ens_similarity_gap)) | 2 | 距相似故事天数↑=新闻越独特；QD44113 信息熵思路的连续代理 |
| T09 | [F][S] | 事件计数·vec_sum 总量几何 | rank(vec_sum(nws48_rp_story_event_count)) | 2 | 每 story 实体记录数=信息活跃度；Vector 帖五几何之一，刻意区别于 vec_avg 水平 |
| T10 | [F] | 积极事件密度·乘积非线性 | rank(multiply(vec_avg(nws48_aes),vec_avg(nws48_vea))) | 4 | 论坛方案9；积极占比×事件数；非线性交互项，非秩和融合(避 add(A,B) 反模式) |
| T11 | [F][S] | 情绪分歧·二阶矩 vec_stddev | -rank(vec_stddev(nws48_ssc)) | 2 | 论坛方案7 情绪波动性；Vector 帖「离散程度」几何；二阶矩，与一阶矩族区分 |
| T12 | [F] | 单事件影响·归一化比率 | rank(divide(vec_avg(nws48_nip),vec_sum(nws48_rp_story_event_count))) | 4 | 论坛方案6；新闻影响/事件数=单位事件冲击；比率型非线性 |
| T13 | [P][F] | 异常关注度·个股−全局差 + 时序分位反向 | -rank(ts_rank(ts_backfill(subtract(vec_avg(nws48_qep),vec_avg(nws48_ssc)),5),66)) | 6 | Da 2011 注意力先涨后反转 + 论坛 43541109631895 三步模板；vec_norm 修正后的 EUR 合法版；66 季窗对照 |
| T14 | [F][S] | 情绪水平·分组轴中性化 | group_neutralize(rank(vec_avg(nws48_ssc)),sector) | 3 | 分组轴几何；检验 sector 中性化能否救 margin（§analyst9 口径：sector 是 margin 来源但伤 2Y） |

## 归因设计（派发后按模板编号归因，不是按单条 alpha）
- 4 个对照轴：① 水平(T01/T02) vs 相对化(T03/T05/T13) —— 验「水平弱、相对化强」论文先验；② 一阶矩(T01/T04) vs 二阶矩(T11) —— 验 Vector 帖「离散度几何」；③ vec_avg(T01) vs vec_sum(T09) —— 验「条数几何」是否独立于水平；④ 短窗(T07/T08 5/22) vs 长窗对照(T03/T13 66) —— 验 §6133 窗口匹配错假设。
- 方向自洽检验：T01(顺势) vs T02(反向)、T05(反向相对) vs T06(反向水平)，按 §91 纪律区分「方向反转」与「字段弱」两种死因。
- 硬止损：若 14 模板全族 2Y 全灭且 S 普遍 <1.0，先按 news52 反证分三因（字段衰减 / 窗口错配 / 字段本身弱），同字段族做单变量只改窗长对照；短长窗都全灭 ⇒ 判 news48 字段弱、换数据集(news29 / news50，须各自先 S1 画像 + 论坛/论文取证 + ≥10 模板池)，不得凭记忆点名已判死集(sentiment27/other553/sentiment7/news17/news52/news54)。

## 状态
- 取证齐备(论坛 2 篇正文 + 论文 3 篇独立核验) + 模板池 14 个结构互异 + preflight 14/14 valid + 算子 ≤6 ≤12 上限。
- §95 首批已派发并于 §96 收批（2026-11-05）：§94 硬止损触发(sentiment21 整集收手) + 10nV2Td0 并发槽收口后派 T05+T06 干净单变量对照(相对化新颖度 vs 水平新颖度)，multisim **23iE5K1N25facsn15rCDSWg2** COMPLETE。收批：T05 1YNjjWEJ S0.76/2Y0.40/TO158.73%/CW FAIL、T06 E56VVQJG S−0.45/2Y0.07/TO158.85%/CW FAIL，两条 pyramid 均仅 EUR/D1/NEWS 1.3、逐年 10 年全覆盖无空窗。归因：相对化杠杆把 S/2Y/sub 三项翻正(方向先验成立)，但共享「TO 158% 逐年恒定=i.i.d. 噪声重排 + CW 结构性集中」形态墙，主因收敛为「VECTOR 聚合逐日跳变 + rank 无时间平滑」；2/14 模板未触发整集收手。
- §96 递进探针已于 §97 收批（决定性对照）：T03 wpQ9Q9z2 S−0.06/TO47.32%/CW PASS(仅3 failed RA)、T13 2rAjAjZx S−0.56/TO72.7%/2Y−1.37/CW PASS，两条 pyramid 均仅 EUR/D1/NEWS 1.3、逐年 10 年全覆盖。时间平滑破形态墙后 S/2Y 归零 ⇒ §95 相对化 S0.76 是噪声换手伪影、字段本身横截面弱；且短长窗对照都全灭 ⇒ 排除「窗口错配」。但 4 模板几何同质(全 vec_avg+rank/比率)，独立几何轴未碰。
- ★§97 最后跨几何终验已派发：T09 rank(vec_sum(nws48_rp_story_event_count))(计数几何,对照轴③) + T11 -rank(vec_stddev(nws48_ssc))(二阶矩,对照轴②)，preflight 2/2 valid / 算子 2/2 ≤12 / vec_stddev 过 toolkit_static，multisim **3HirxTDL4IfaCt26gC8b8O** 提交成功、收批在途。**这是 wave1 最后一批**：若 T09/T11 仍 0/2 ⇒ 6 结构互异骨架全灭、正式判 news48 整集弱收手，剩余 T01/T02/T04/T07/T08/T10/T12/T14 不再追加；若有货 ⇒ 反证只是 vec_avg 几何错配、按出货几何定向补模板。后续批次按并发 2、每批恰好 2 条、preflight→create_multi_simulation→toolkit_static→batch_status→harvest→workflow_auto_harvest 入库执行，收批按模板编号归因。本波零提交、零不可逆动作。
- 三颗已达标候选(imb5 族 1YNjqknX/LLM5eAMn、est_12m_ebt 族 ZYQmolVx)仍待用户明确授权，两族各交 1 颗。
