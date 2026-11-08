# SENTIMENT 面 wave3 模板池：sentiment26（EUR/D1/TOP2500）2026-11-05

## 一、S1 字段面体检（MCP get_datafields，零仿真成本）
- **sentiment7**：24 字段全 VECTOR；22 个 cov=0 元数据字段（company_name/isin/ticker/exchange/website/access_type 等且描述错位），真正有信号仅 snt7_all_languages_views(cov0.5,ac19) / snt7_views(0.5,15) / snt7_timestamp(0.5,9)。字段面贫瘠，不宜作主数据集。
- **sentiment26**：19 字段全 VECTOR，cov 0.5835–1.0（中位 0.7482），ac 7–103；是 DNS 网站流行度排名的分布矩族：avgranking / kurtosis / skewness / rank / relpopularity08 / relpopularity1 / top10|25|50|75pctranking(avg) / topranking / totaldomains / totalcountrydomains / dltcc / wq_pit。水平/一/二/三/四阶矩天然齐备，覆盖远好于 sentiment7 ⇒ 选作 SENTIMENT 面主数据集。
- **命名混淆**：DEU 记忆/论坛里的 sentiment27 / snl27_* / snt27_*（DEU 因 prod 墙 + 2014–2018 五年空窗封盘）与 EUR 在架 sentiment26 / snt26_* 不是同一编号；DEU 结论不可外推 EUR，须逐区实测。

## 二、论坛/论文取证（本轮已读 4 篇正文 + 关键评论）
- [F] 43383627584023「聚合→突增→相对化→去基数」：VECTOR 先 vec_* 聚合；水平无横截面信息，真正有用是突增动态——ts_max(5) 抹平周内周期、ts_ir(22)(均值/标准差) 把绝对突增译成相对自身异常度；ts_zscore 对右偏长尾太敏感、禁用；vector_neut 对人气规模去基数。峰值 5 / 相对化 22。
- [F] 43444585257879「vec_sum vs vec_avg」：计数类用 vec_sum（avg 把强度压没）、时长/典型水平用 vec_avg；稀疏字段除法 +1；截面比较 group_rank(..., densify(industry))。
- [F] 41420742165527「HKG snl27/snt27 三种后处理实测」：路径1 clamp+rank+group_backfill(PPAC0.65)、路径2 ts_backfill(5)+ts_zscore(66)+group_rank(0.40)、路径3 ts_mean(22)-ts_mean(66) 差分 + ts_vector_neut(ts_mean(120),66) + winsorize(0.15)；窗口 66 标准化 / 22-66 差分 / 120 长期均值。
- [F][P] 43179860065303「DEU 维基百科突压」（72赞，DEU/SENTIMENT S2.04/F1.92/margin24.2bp/17项全PASS/prod0.6338）：完整脉冲链 vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(ATTENTION),22),5),5),22),120), POPULARITY)。文献支撑 Jacobs&Lauber 2025(SSRN 5143296) / Chalamandaris 2026 / Da,Engelberg&Gao 2011 / Barber&Odean 2008 ⇒ 情绪水平不可交易、脉冲动态才有边际信息。
- **★关键风险警告（直接约束本波设计）**：
  1. 同族三代 PC 0.319→0.557→0.6338 单调爬升，第 4 代必撞 0.7 ⇒ 正确做法是换 ATTENTION_MEASURE 字段源，而非换壳重排(JR57542)。本波 S01 故意用 snt7 浏览量作 ATTENTION、snt26 人气作 POPULARITY，S02/S03 全换 snt26 内部字段，避开 DEU 字段组合。
  2. 迁区 prod 可能撞墙：YL61874 报同族注意力信号迁区 PC 0.78–0.84 全线超线，「注意力类数据平台存量供给太密，换区域不解决拥挤」⇒ 出货后必须 prod 真测（MCP prod_wait 后台），不得据 DEU 0.6338 乐观。
  3. 样本抹除坑：JH66822 实测 snl27_relpopularity08 只有后五年有数据，vector_neut 组合会抹掉前五年 ⇒ 掩盖连续空窗。S01/S02/S03 用 relpopularity08 作腿，入篮前必查 get_alpha_yearly_stats 逐年 longCount>0 && pnl!=0。
  4. 伪脉冲坑：XZ17517 指 ts_backfill(22)+ts_ir 在「数据刚有记录」时会把回填水平线÷极小标准差误标成突增 ⇒ S01/S02/S03/S08 要对比含/不含回填段。
  5. ts_ir 换 ts_zscore 全结构崩盘；rank 包装每剥一层 +FT 0.3–0.65（脉冲字段先试无 rank）；FF45555 引述「同一模板换 region 做多做空可能互换」⇒ 首轮先小样本确认方向，别照搬 DEU。

## 三、窗口口径（硬约束：日1/周5/月22/季66/年252；其它值须给解释+实证）
- 1 日事件对齐 / 5 周提峰值 / 22 月相对化 / 66 季标准化 / 252 年长窗对照 —— 均为标准窗。
- 120：论坛实证甜点，非随意取值 —— 43179860065303「Sentiment 大类 120d 是 IS_Ladder 甜点」+ 41420742165527 路径3 ts_mean(120) 长期均值，两篇独立帖给出。

## 四、塔混 / ATOM 纯净检查
- sentiment7 / sentiment26 同属 SENTIMENT（禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} 之外）；SENTIMENT×SENTIMENT = 集合外×集合外，不限量、不占 trio 配额。
- 全部模板不含 returns/price/volume 腿 ⇒ 按 §82/§84 确证不带 PV 属性，纯净 SENTIMENT 单塔 ATOM 或 SENTIMENT 内组合。
- 算子数 4–9，全 ≤12 合规（用户 2026-11-04 上限 12、越少越好）。

## 五、模板池（14 个，结构互异）
| # | 来源 | 机制 / 结构轴 | 表达式 | 算子 | 经济含义 |
|---|---|---|---|---:|---|
| S01 | [F][P] | 脉冲全链·换字段源 | vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt7_all_languages_views),22),5),5),22),120), ts_backfill(vec_avg(snt26_relpopularity08),22)) | 9 | ATTENTION=snt7浏览量、POPULARITY=snt26人气；换字段源防PC爬升 |
| S02 | [F] | 脉冲链·纯单集 | vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt26_dltcc),22),5),5),22),120), vec_avg(snt26_relpopularity08)) | 8 | ATTENTION 也换 snt26 内部，纯 sentiment26 ATOM |
| S03 | [F] | 脉冲链·消融(无rank/quantile) | vector_neut(ts_ir(ts_max(ts_backfill(vec_sum(snt26_avgranking),22),5),22), vec_avg(snt26_relpopularity08)) | 6 | vec_sum计数 + 去 quantile/ts_mean 双层，验「无rank」增益 |
| S04 | [F] | HKG路径1·去基数(修正) | group_backfill(rank(winsorize(vec_sum(snt26_relpopularity08),std=2.5)),industry,5) | 4 | clamp 不在EUR算子白名单→改 winsorize 控极值；industry backfill |
| S05 | [F] | HKG路径2·主动填充 | group_rank(ts_zscore(ts_backfill(vec_sum(snt26_totalcountrydomains),5),66),industry) | 4 | backfill5 + zscore66 + group_rank（独立几何，非S01脉冲链） |
| S06 | [F] | HKG路径3·差分去趋势(修正) | winsorize(vector_neut(subtract(ts_mean(vec_sum(snt26_rank),22),ts_mean(vec_sum(snt26_rank),66)),ts_mean(vec_sum(snt26_rank),252)),std=3) | 9 | 22-66差分捕短期偏离、对年窗均值 vector_neut；ts_vector_neut 不在白名单→改截面正交(几何替换非等价复现) |
| S07 | [S] | 一阶差分·事件冲击 | rank(ts_delta(ts_backfill(vec_avg(snt26_dltcc),22),1)) | 4 | 日1 事件日对齐 |
| S08 | [F] | 突降反向·独立链 | group_neutralize(ts_ir(ts_min(ts_backfill(vec_avg(snt7_all_languages_views),22),5),22),industry) | 5 | 反向不是镜像负号，走 ts_min 独立回测(JR57542) |
| S09 | [F] | 回落时点·峰值年龄 | rank(ts_arg_max(ts_backfill(vec_avg(snt26_avgranking),22),5)) | 4 | ts_arg_max 定位峰值日，回答「市场多久完成定价」 |
| S10 | [S] | 三/四阶矩·分布形态 | -rank(subtract(vec_avg(snt26_skewness),vec_avg(snt26_kurtosis))) | 4 | 偏度−峰度，尾部不对称(水平矩) |
| S11 | [S] | 分位结构比 | rank(subtract(vec_avg(snt26_top10pctrankingavg),vec_avg(snt26_top75pctrankingavg))) | 4 | 头部vs尾部域名排名差=注意力集中度结构 |
| S12 | [S] | 非线性·压幅 | rank(signed_power(group_zscore(ts_backfill(vec_avg(snt26_relpopularity1),22),sector),1.5)) | 5 | signed_power 压幅 + 行业内 zscore |
| S13 | [S] | 二阶矩·分歧 | -rank(ts_std_dev(ts_backfill(vec_avg(snt26_avgranking),22),66)) | 4 | 排名波动=不确定性(Miller方向) |
| S14 | [S] | 长窗分位·分组对照 | group_rank(ts_rank(ts_backfill(vec_avg(snt26_topranking),22),252),industry) | 4 | 年窗252时序分位+行业分组，长窗对照(验事件字段长窗是否崩) |

## 六、全模板字段预检（MCP preflight_expressions，零回测成本）
- 初版 14 模板 preflight 暴露 clamp / ts_vector_neut 不在 EUR 平台算子白名单（被当字段查无结果）⇒ S04 改 winsorize(std=2.5)、S06 改 vector_neut(...,252)。修正版复检：14/14 valid=true / unknown_fields=[] / any_changed=false / platform_field_count=12。
- 算子数逐一 [9,8,6,4,4,9,4,5,4,4,4,5,4,4] 全 ≤12。
- 软标记：snt26_topranking 分页探查 get_datafields(offset=0): failed after 6 attempts（平台瞬时故障）；首轮全字段面确证在架(cov0.7482/ac36)，不判缺失。

## 七、派发纪律（待并发槽释放后执行，本轮未派）
- 每批恰好 2 条 create_multi_simulation（并发限 2），一批一套 settings：EUR/TOP2500/D1、FAST、decay1、trunc0.04、maxTrade OFF。
- 收批按模板编号归因；逐年空窗闸（警惕 relpopularity08 后五年才有数据）、算子≤12、CW/self/prod 逐件验；出货件 prod 必须 MCP prod_wait 后台真测（DEU 同族迁区 PC 可能 0.78–0.84）。
- 首批建议 S01(脉冲全链换字段源) + S03(脉冲链消融)：论坛最厚取证 + 「有/无 rank·quantile」单变量对照，纯 SENTIMENT 塔、不含 returns 腿。
- 前置风险：S01/S02/S03 用 relpopularity08 作 POPULARITY 腿，收批后先查逐年空窗再谈 prod（JH66822 样本抹除坑）。
## 八、外部论文独立核验补充（并入 S1 台账，2026-11-05 §86）
- 通道：`web_fetch` OpenAlex(HTTP200) + arXiv(HTTP200)，`web_search` 402/SemanticScholar 429 仍不通；本次为**独立论文元数据+摘要核验**，非论坛转述。
- **Da, Engelberg & Gao (2011)「In Search of Attention」(Journal of Finance, doi 10.1111/j.1540-6261.2011.01679.x, 被引3046)**：SVI 上升→未来2周股价更高→**年内反转**；注意力须取「相对自身历史分位」而非绝对水平。⇒ 为 S01–S14 的脉冲/突压/分位几何给出**方向先验：高注意力分位→反向持仓(做空)**，并为 `ts_rank/quantile/ts_ir` 的标准化提供文献依据。
- **Ben-Rephael, Da & Israelsen (2017) RFS doi 10.1093/rfs/hhx031**：机构注意力领先散户、促永久价格调整 ⇒ 散户注意力(反转)与机构注意力(价格发现)方向相反，本模板池用 DNS 网站流行度/维基类**公共注意力**代理，归散户侧、取反转方向合理。
- **arXiv 1703.02715「Joint News, Attention Spillover, and Stock Returns」**：联合新闻触发注意力传染→临时估值膨胀 ⇒ 支撑脉冲链/突压几何(S01/S03)与「去基数相对化」。
- **论坛 43541109631895（EUR/TOP2500 5变体）**：注意力模板在 EUR 方向泛化成立但 Fitness 全<1.0；60日(季)窗是甜点；`ts_target_tvr_decay` 买 margin 非 Sharpe；`signed_power` 基本无效；`vec_count` 无事件日 NaN 需 0 填充对照；收批后若出货须按年拆 margin 防单年塌陷。⇒ 本池 S14 年窗252分位对照、S13 二阶矩、S12 signed_power 压幅已覆盖这些检查面；**新增备靶(未入14模板/未派发)**：事件密度分位反向 `group_neutralize(-ts_rank(ts_mean(vec_count(ATTENTION),60),252), densify(market))` 作为机制模板对照。
- 收批纪律不变：出货件先查逐年空窗(relpopularity08 后五年坑)、算子≤12、CW/self/prod 逐件验，prod 必走 MCP prod_wait 后台真测。
## 九、★静态门禁(toolkit_static)算子可访问性修正（2026-11-05 §87）
- **新平台事实**：`create_multi_simulation` 有一道 `toolkit_static` 静态闸，preflight_expressions **只验字段、不验算子可访问性**；S01/S03 原版含 `ts_max` 被整批拒绝：`[INACCESSIBLE_OP] ts_max 平台不可访问，用已验证等价算子替换`。
- **已确证**：`ts_max` 在 EUR 不可访问。据此 `ts_min`(S08) / `ts_arg_max`(S09) 高度同源、派发前必须先过门禁探测，被拦则换已验证等价算子；其余 11 模板算子(group_backfill/group_neutralize/group_rank/group_zscore/quantile/rank/signed_power/subtract/ts_backfill/ts_delta/ts_ir/ts_mean/ts_rank/ts_std_dev/ts_zscore/vec_avg/vec_sum/vector_neut/winsorize)未触发告警。
- **首批改写并派发**：S01b=`vector_neut(quantile(ts_ir(ts_mean(ts_backfill(vec_avg(snt7_all_languages_views),5),5),22),120), ts_backfill(vec_avg(snt26_relpopularity08),22))`（算子8，去掉 ts_max、改短窗回填峰值）、S03b=`vector_neut(ts_ir(ts_backfill(vec_sum(snt26_avgranking),5),22), vec_avg(snt26_relpopularity08))`（算子5）。保留论坛 43383627584023「突增→相对化→去基数」核心，峰值取法由 ts_max 改 ts_backfill(...,5)+ts_ir。preflight 2/2 valid、platform_field_count=3、any_changed=false。**multisim QH47wf585eLcjqnMp66JOS 过静态闸但批次实际 ERROR**（quantile arity=1 整批 ERROR+CANCELLED，详见下方补充）；合法版重派 multisim **3d6H8Ogoo4SZczo16yi7jj6f 收批在途**（lookINTO progress=0.15、真在飞）。
- 收批按模板编号归因 + 逐年空窗(relpopularity08后五年坑) + CW/self/prod 逐件验；出货件 prod 走 MCP prod_wait 后台真测。
- **★补充(同轮实测)**：`quantile(x,120)` 在 EUR 平台 arity=1（120 被当第二个输入、报 `Invalid number of inputs : 2, should be exactly 1`），DEU 论坛脉冲全链里的 quantile 是概念简写非 EUR 合法式；首批 QH47wf585eLcjqnMp66JOS 因此整批 ERROR+CANCELLED。合法版去 quantile、保 `ts_ir` 相对化 + `vector_neut` 去基数：S01c=`vector_neut(ts_ir(ts_mean(ts_backfill(vec_avg(snt7_all_languages_views),5),5),22), ts_backfill(vec_avg(snt26_relpopularity08),22))`(7算子)、S03c=`vector_neut(ts_ir(ts_backfill(vec_sum(snt26_avgranking),5),22), vec_avg(snt26_relpopularity08))`(5算子)，重派 multisim 3d6H8Ogoo4SZczo16yi7jj6f 收批在途。**派发前必须过静态门禁 + 实测 arity，preflight 不可当提交判据**。

