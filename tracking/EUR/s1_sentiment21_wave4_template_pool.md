# SENTIMENT 面 wave4 模板池：sentiment21（EUR/D1/TOP2500）2026-11-05

> 定位：SENTIMENT 塔当前 1/3（未点亮）。sentiment26 走「DNS 注意力突压」机制（全 VECTOR，S01c/S03c 在飞 multisim 3d6H8）；本波改走第二条独立机制面 = 社交媒体情绪分数的分布矩 + 情绪-收益/情绪-情绪相关性错位，选 sentiment21（全 MATRIX）。两波机制面不重叠，符合「模板/机制多样性」硬约束。

## 一、S1 字段面体检（MCP get_datafields，零仿真成本，本轮实测）
- sentiment21 = 210 字段，全部 MATRIX（无需 vec_* 聚合，天然规避 VECTOR 修复坑），cov 0.9317–1.0（中位 1.0），acMax 341，complete=true / platform_count=210。
- 字段族结构：按情绪极性 × 分布矩 × 时间尺度三维笛卡尔积 —— 极性 3 档：2neg_(负) / 2pos_(正) / 2neut_(中性)，各 70 字段；分布矩：mean / median / std(2dts_*) / max / min / conf_low / conf_up（置信区间上下界）；尺度前缀 2/3/4（不同回溯聚合尺度），另有后缀数字变体（不同分位/口径）。
- 关键字段（本波 14 模板实际用到 8 个，preflight platform_field_count=8 全在架）：snt21_2pos_mean / snt21_2neg_mean / snt21_2pos_std / snt21_2neg_std / snt21_2pos_median / snt21_2neut_median / snt21_2neg_conf_up / snt21_2neg_conf_low。cov 0.9317–1.0，远高于论坛担心的「EUR 覆盖低于 70%」阈值，故不必重 backfill，短 backfill(22) 仅防空洞。
- 与 sentiment26 的机制分工：sentiment26 = DNS 网站流行度排名的分布矩（注意力/流量代理，全 VECTOR）；sentiment21 = 社交网络正/负/中性情绪评分的分布矩（态度/分歧代理，全 MATRIX）。前者赌「注意力突压→反转」，后者赌「情绪水平/分歧/相关性错位」，两条独立先验。
- 覆盖口径提醒（用户两次纠正）：入篮/派发前必查 get_alpha_yearly_stats 逐年 longCount>0 且 pnl≠0，判「连续多年彻底空窗」而非「近十年满覆盖」；数据集级 cov 高不等于逐年无空窗，出货件仍须逐年核验。

## 二、论坛 / 外部论文取证（用机制前先查，2026-11-05）
### 论坛（本轮读 3 篇正文 + 评论）
- [F] 44406909668631「情绪相关性错位：snt 系列在 IND 的因子族实践」(FF65210, 2026-10-21) —— 本波最核心模板来源。4 个已提交因子（S1.75–2.46 / margin 15–28bp / Fitness 1.5–2.2）。抽象出两个可复用接口：
  - 接口A（轻量·推荐先试）：winsorize(-ts_corr(情绪字段, returns, 126) - ts_zscore(returns, 126), std=2~3) + group_neutralize(industry/subindustry)。经济含义=交易「情绪传导时滞」：情绪与价格夫唱妇随，alpha 藏在联动错位的日子；减 ts_zscore(returns) 是动量对冲项，省了会退化成纯反转、PC 立刻变差。
  - 接口B（重量）：reverse(ts_regression(returns, ts_regression(volume, 情绪字段, 200), 300)) + ts_zscore(504) + signed_power(0.5) + group_neutralize + group_backfill(60)。
  - 字段三档：离散度类(highest−lowest)→顺势(正号+幂放大)、中性/均值类→反向回归(负号)、极端悲观类(neg_conf)→出清修复。
  - 避坑：① 情绪字段有界、与无界 returns 回归前确认量纲；② 事件驱动跳变令 ts_corr 在事件周失真，winsorize 缓解不消除；③ 接口A/B 都带 returns 腿——按本项目 §82/§84 确证会带 PV 塔，EUR 硬约束下吃「集合内×集合外 ≤5」配额，非纯净 ATOM；④ snt21 搬去 EUR/USA 前先查 coverage，低于 70% 加大 backfill（本轮已查：EUR 0.93–1.0，无需重填）；⑤ 相关窗 126 天（半年）甜点，63 太噪、252 滞后。
  - 评论 QQ38141 补：相关性信号本质是 −1..1 有界量，缩尾要轻(std=3)；回归残差无界才放宽 std=6。「有界量轻缩、无界残差重缩」尺度分工。
- [F] 43622633366807「散户的盛宴与狂欢：sentiment21 社交情绪动量之思」(WL27618, 30赞) —— 机制定性：顺势吃前半段、逆向防后半段；讨论度刚破圈早期动量强劲，破纪录沸点时刻增量资金断流、踩踏。给出 T05(一阶差分动量) 与 T07(长窗分位反向/沸点离场) 的方向先验；与 short squeeze 叠加更剧烈。
- [F] 42022631228183「USA D0 Social Media 反直觉发现」(HS65681, 20赞) —— ① 聚合方式对 Sharpe 非线性影响，aggregated 系列信息量远超单字段；② INDUSTRY 中性化在社媒最好（情绪天然行业聚集，剥离 beta）；③ decay 6 快衰减（>10 Sharpe 腰斩）；评论 YR99599 提醒：稀疏覆盖 + INDUSTRY 中性化会把单票行业裁掉、breadth 偏低，且「EUR 跑出非零」可能是少数跨市场美股 + backfill 伪截面，必须逐年核验真实覆盖。
### 外部论文（web_search 402 余额耗尽 / SemanticScholar 429，故 web_fetch OpenAlex+arXiv HTTP200 独立取数）
- [P] OpenAlex 检索 social media investor sentiment dispersion disagreement stock returns：命中 785 篇，含 2025「BEYOND THE NOISE: social media sentiment, VOLUME, and DISPERSION on stock market volatility」(doi 10.57233/gujoba.v4i2.40)，支撑「情绪分歧度/离散度(dispersion)是独立于情绪水平的定价因子」。
- [P] arXiv 2607.28496「Beyond Sentiment: Structured Information Extraction from Financial News」：FinBERT 情绪特征在非线性模型下预测力强(F1 0.576)、线性模型弱(0.230)，即情绪-收益关系高度非线性，支撑本池 signed_power 幂变换(T09/T12) 与分位/相关几何，而非纯线性 rank。
- [P] 承接 §86 已核验：Da, Engelberg & Gao (2011) JF「高注意力→短期价格压力→年内反转、须取相对自身历史分位」；Ben-Rephael et al. (2017) RFS「散户注意力=反转 / 机构注意力=价格发现」；arXiv 1703.02715「联合新闻→注意力传染→临时估值膨胀」。公共社媒情绪归散户侧、取反转/沸点离场方向合理。

## 三、窗口口径（硬约束：日1/周5/月22/季66/年252；其它值须解释+实测）
- 本池只用标准窗：5(周) T05/T06、22(月) backfill 防空洞、66(季) T08/T11/T12/T14 标准化与相关窗、252(年) T07 长窗分位对照。
- 论坛 126(半年)相关窗未直接照搬：IND 帖给 126 为甜点，但 EUR 硬约束窗口须有意义，首波取季 66 作对照；若季窗信号不足，再考虑 126 并附实测证据后启用（不预先用非标准窗）。
- 水平模板 T01–T04/T09/T10/T13 无时间窗（纯横截面矩），刻意与时序几何对照。

## 四、塔混 / ATOM 纯净检查
- sentiment21 属 SENTIMENT（禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} 之外）；14 模板全部仅 sentiment21 内部字段，不含 returns/price/volume 腿，按 §82/§84 确证不带 PV 属性，纯净 SENTIMENT 单塔 ATOM，不占任何两塔组合配额、不受禁混约束。
- T11/T12 用 ts_corr(A,B,66)，两腿都是 sentiment21 字段（非 returns）——与 §82「ts_corr(X, returns, W) 带 PV」形成干净对照：本波预期纯 SENTIMENT 单塔，收批时以 pyramid 实测复核（写为待验证假设，不预先当结论）。
- 论坛接口A/B 原版带 returns 腿，会变成 PV×SENTIMENT 组合、吃 ≤5 配额，故不在本主池，列为第九节备靶。
- 算子数 1–4，全 ≤12、越少越好（用户 2026-11-04 口径）；无装饰算子、无权重网格、无 add(独立信号A,B) 混调参（T02 的 add 是「正+负情绪标准差=同一分歧度两分量合成」，非两个独立信号混合）。

## 五、模板池（14 个，结构互异；来源 [F]论坛 / [P]论文 / [S]自建）
| # | 来源 | 机制 / 结构轴 | 表达式 | 算子 | 经济含义 |
|---|---|---|---|---:|---|
| T01 | [F][P] | 水平·净情绪差 | -rank(subtract(snt21_2pos_mean, snt21_2neg_mean)) | 2 | 净乐观水平高→散户拥挤→反向(Da反转/沸点离场) |
| T02 | [F][P] | 二阶矩·分歧度 | -rank(add(snt21_2pos_std, snt21_2neg_std)) | 2 | 多空观点分歧=不确定性(Miller/OpenAlex dispersion) |
| T03 | [F][S] | 置信区间宽度 | -rank(subtract(snt21_2neg_conf_up, snt21_2neg_conf_low)) | 2 | 悲观情绪估计离散=恐慌分歧幅度 |
| T04 | [F] | 水平·极端悲观 | rank(snt21_2neg_conf_up) | 1 | 极端悲观置信上沿→出清后修复(IND LLGLjKmm 字段) |
| T05 | [F] | 一阶差分·情绪动量 | rank(ts_delta(ts_backfill(snt21_2pos_mean, 22), 5)) | 3 | 破圈早期顺势吃前半段(专帖) |
| T06 | [S] | 二阶差分·情绪加速度 | rank(ts_delta(ts_delta(ts_backfill(snt21_2pos_mean, 22), 5), 5)) | 4 | 情绪变化率的变化=动能拐点(与T05同骨架不同矩阶) |
| T07 | [F][P] | 长窗分位·沸点反向 | -rank(ts_rank(ts_backfill(snt21_2pos_mean, 22), 252)) | 3 | 情绪破年内纪录→增量资金断流→离场(专帖+Da年内反转) |
| T08 | [F] | 相对化·中性关注 | rank(ts_zscore(ts_backfill(snt21_2neut_median, 22), 66)) | 3 | 中性情绪相对自身历史异常(ts_zscore 几何) |
| T09 | [F][P] | 非线性·分组轴 | rank(signed_power(group_zscore(subtract(snt21_2pos_mean, snt21_2neg_mean), sector), 2)) | 4 | 行业内净情绪 zscore 取幂放大极端(arXiv非线性+signed_power旋钮) |
| T10 | [F] | 分组轴·group_rank | group_rank(subtract(snt21_2pos_mean, snt21_2neg_mean), industry) | 2 | 行业内净情绪排名(43444585257879/IND中性化) |
| T11 | [F] | 内部字段相关·错位 | -ts_corr(snt21_2pos_mean, snt21_2neg_mean, 66) | 1 | 正负情绪同步性塌缩=极化错位(接口A改编：returns→内部字段保纯ATOM) |
| T12 | [F] | 幂放大·趋势共识 | signed_power(ts_corr(snt21_2neg_std, snt21_2pos_mean, 66), 2.5) | 2 | 分歧与乐观强绑定→趋势共识顺势(IND qM65aPeA 简化) |
| T13 | [S] | 分布形态·偏度代理 | rank(subtract(snt21_2pos_mean, snt21_2pos_median)) | 2 | mean−median=正情绪分布右偏(三/四阶矩族) |
| T14 | [S] | 时序二阶矩·分歧波动 | -rank(ts_std_dev(ts_backfill(snt21_2neut_median, 22), 66)) | 3 | 中性关注波动=注意力不稳(Miller) |
- 结构互异核对：水平净差/水平单腿/二阶矩分歧/置信宽度/一阶差分/二阶差分/长窗时序分位/时序相对化/非线性幂+分组轴/分组排名/字段间相关/幂放大相关/分布偏度/时序波动 —— 覆盖不同矩(水平·一阶·二阶·分布形态)、不同几何(rank/group_rank/group_zscore/ts_rank/ts_zscore/ts_corr/ts_std_dev/signed_power)、不同分组轴(sector/industry)、不同非线性，非「换窗口/换常数」凑数。≥10 达标。

## 六、全模板字段预检（MCP preflight_expressions，零回测成本，本轮实测）
- 14/14 valid=true / unknown_fields=[] / unknown_soft=[] / any_changed=false / platform_field_count=8 / vector_fields=[]。全 MATRIX 无需 VECTOR 修复。
- 算子数逐一 [2,2,2,1,3,4,3,3,4,2,1,2,2,3] 全 ≤12。
- 未验项（须派发前探测，诚实标注）：ts_corr 在 news18 batch1 已实测平台可访问（含 returns 腿、有回测结果）；add/ts_delta 二阶/group_zscore/signed_power 均在 §87「其余 11 模板算子未触发告警」清单内。但 toolkit_static 静态门禁只有 create_multi_simulation 时才触发，preflight 查不到（§87 教训），故首批按纪律仅派 2 条探测，含 ts_corr 的 T11/T12 优先留到门禁确认后再上，避免整批 CANCELLED 连坐。

## 七、派发实绩（2026-11-05 §90 已执行）
- 阻塞已解除：§89 中 multisim 3d6H8Ogoo4SZczo16yi7jj6f 最终 batch_status child_count=2 / all_terminal=true、收批入库完成、并发槽释放。本波已按下列纪律派发首批 T01+T05（multisim 1DMTwI7Om4Ymb4AyHYQThfc，preflight 2/2 valid、create_multi_simulation success=true 过 toolkit_static 静态闸、收批在途）。
- 释放后：每批恰好 2 条 create_multi_simulation（并发限 2），一批一套 settings：EUR/TOP2500/D1、FAST、decay1、trunc0.04、maxTrade OFF（与前几波同 settings 保证干净可比）。
- 收批按模板编号归因；逐年空窗闸、算子≤12、CW/self/prod 逐件验；出货件 prod 必走 MCP prod_wait 后台真测。首批已派 T01(水平净差反转) + T05(一阶差分动量) —— 论坛专帖「顺势前半段 / 逆向沸点」方向先验的一对干净对照，且都不含 ts_corr，门禁风险最低；§90 已过 toolkit_static 静态闸。
- ★首批收批(§91)：T01/T05 双双全灭但死因不同——T01 TO 151% 换手墙、T05 方向反转(S -0.58/2Y -1.15)；已按「水平几何 vs 意外化几何并行、勿单几何判死」纪律改上 T07(长窗分位沸点反向)+T08(ts_zscore 相对化) 复测(multisim 45Nzp98L050eaYMdrRloUp4，收批在途)，构成 2×2 几何×方向对照。若相对化几何也全灭 ⇒ 判字段弱、换机制面。
- ★★第二几何面收批(§92)：45Nzp98L 解冻 2/2 COMPLETE，T07(qMLExAPV) S0.09/2Y-0.84/TO41.7%、T08(d5WKbxn2) S0.69/2Y-0.10/TO40.2%，二者 CW/TO/sub 全正常、仅 S/2Y 强度不足 ⇒ 2×2 几何×方向对照干净收敛为「均值/中位数·一阶中心矩族字段本身横截面信号弱」(排除几何失配/窗口错配/方向错/换手墙四因)。累计 4 模板全灭、0/4 过硬闸。
- ★换机制面复测(§92)：遵循「不再同族加模板」，仅挑 14 池里完全避开均值/中位数字段族的 T02(`-rank(add(pos_std,neg_std))` 二阶矩分歧度 dispersion) + T03(`-rank(subtract(neg_conf_up,neg_conf_low))` 置信区间宽度尾部族)。二者字段族与已测 4 模板正交，是干净换面。preflight 2/2 valid、算子 2/2、过 toolkit_static，multisim **10nV2Td0P4ohbmAZ049UYEQ** 提交成功、已于 §94 收批（progress 0.15→0.35→COMPLETE 解冻，验证「不重发」决定正确）：T02 Xg9RRPP8 S0.77/2Y0.04/TO141%、T03 npvAAYYd S0.59/2Y0.23/TO145% 双双全闸 FAIL、0/6 过硬闸 ⇒ §92 硬止损触发、判 sentiment21 整集字段族在 EUR 弱、整集收手。硬止损：若 T02/T03 也 0/2 ⇒ 判整个 sentiment21 整集字段族在 EUR 弱、整集收手，不再追加 T04/T06/T09–T14。★§93 纠偏：sentiment27/other553/sentiment7 三者均已有判决(空窗/换手墙/字段贫瘠)，不是合法换数据集方向；真正下一步只剩 ①§九 带 returns 的 PV×SENTIMENT 论坛接口A/B(吃 ≤5 配额、非纯净ATOM、须先确认余量+prod真测) 或 ②S1 枚举×判决对照后换全新机制面/数据集。

## 八、与既有波次的机制分工（避免重复刷同族）
| 波 | 数据集 | 机制面 | 状态 |
|---|---|---|---|
| §82/§84 | news18 | 新闻事件×收益共动(含returns→PV+NEWS) / 纯ATOM水平·差分 | 4模板 2Y全灭，不判死、转线 |
| §85/§87 | news52 | 电话会文本结构·短事件窗 | 4模板全灭、判字段弱、收手 |
| §85–§87→§89 | sentiment26 | DNS注意力突压·脉冲链(全VECTOR) | S01c/S03c 已收批全灭(0/2过硬闸)、判弱(§89)、并发槽已释放 |
| 本波 §88→§92 | sentiment21 | 社媒情绪分布矩·相关性错位(全MATRIX) | 中心矩族 4 模板(T01/T05/T07/T08)全灭、2×2对照判字段弱(§92)；换机制面 T02/T03(分歧度/置信宽度族)已派 multisim 10nV2Td0P4ohbmAZ049UYEQ、收批在途；硬止损见 §七 |
- 四波机制面互异，符合「模板/机制多样性」；SENTIMENT 塔 1/3，本波是补塔的第二条独立腿。

## 九、备靶（未入 14 主模板池 / 未派发，登记待评估）
- 论坛接口A 原版（带 returns）：winsorize(-ts_corr(snt21_2neut_median, returns, 66) - ts_zscore(returns, 66), std=3) + group_neutralize(industry)，即 IND 78nmnZbZ 骨架(S2.46)。带 returns 腿=PV×SENTIMENT 组合、吃「集合内×集合外 ≤5」配额，需先确认配额余量且 prod 真测。方向与 T08/T11 形成「内部字段纯ATOM vs 带收益相关性」的机制对照。
- 离散度顺势接口：signed_power(ts_corr(subtract(snt21_2pos_max,snt21_2pos_min), returns, 66), 2.5)（IND qM65aPeA 骨架，margin 28.2bp/TO8%），同样占配额。
- 接口B 两级回归：reverse(ts_regression(returns, ts_regression(volume, snt21_2neg_conf_up, 200), 300)) —— 算子层级多、含 volume/returns 双腿，非 ATOM，最低优先。