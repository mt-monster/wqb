# EUR · 模板库（SOP + 论坛 + 外部论文三源合一）

> 建立时间：2026-11-06。用途：按**字段画像**匹配模板，而不是先有模板再找字段。
> 每个模板标注：骨架 / 适配画像 / 来源 / 本区或他区实证。

## 一、模板总表（16 个结构互异）

| # | 模板名 | 骨架 | 适配字段画像 | 来源 | 实证 |
|---|---|---|---|---|---|
| A1 | 水平量截面排序 | `group_rank(ts_sum(X, W), industry)` | 稀疏事件流的累计量；有方向语义 | SOP；论坛 43837157183895 变体 | EUR insider_agg_matrix **S 2.00 / F 1.03 / fRA=0**（prod 0.7647 ✗） |
| A2 | 自身基线异常度 | `ts_zscore(ts_sum(X, W), 252)` | 事件时点可信的市场（USA Form4 两日强制） | 论坛 43152032301591（USA S 2.25–3.06，prod 0.542–0.686） | **EUR 坍塌**：insider S 0.90（延迟披露搅碎时点） |
| A3 | 差量纲比值（长窗÷短窗） | `group_rank(divide(ts_sum(金额,1260), ts_sum(股数,84)), industry)` | 两字段都暴露同一共同因子（规模/流动性），量纲不同 | 论坛 43837157183895 | EUR insider **S 1.89 / F 1.00 / 2Y 2.29**，prod 深钉 |
| A4 | 事件计数 / 集群度 | `ts_sum(divide(total, avg), W)`（total/avg 严格等于笔数） | 字段对里有 total_* 与 avg_*/mean_* 配对 | 论坛 43467688159511「多人协同更可信」+ CMP 2012 | EUR 异常度形态 S 0.58；**水平量形态未测** |
| A5 | 层级份额 | `divide(ts_sum(top_X, W), ts_sum(all_X, W))` | 同族有 top_ 前缀与无前缀两套字段 | CMP 2012 分层假设 | USA S 0.22（被对照实验杀死）；EUR 未测 |
| A6 | 方向纯度 | `divide(ts_sum(buy−sell, W), ts_sum(buy+sell, W))` | 成对买卖字段 | Seyhun 方向强度 | EUR **S 1.41 / sub 0.85 ✗** |
| A7 | 二阶加速 | `ts_delta(ts_zscore(ts_sum(X,W),252), D)` | 需一阶已有效 | 行为金融惯性/加速 | 未测 |
| A8 | 时序分位 | `ts_rank(ts_sum(X,W), 252)` | **仅水平量信号**；会抹掉尖峰幅度 | 论坛 43152032301591（rank 自废武功 0.61 vs 2.25） | 未测（本区） |
| A9 | 肥尾几何 | `winsorize(X, std=4)` / `signed_power(x, k)` | 肥尾、极值主导 | 意外族处方（Memory） | 意外族专属，套到比率类反损 |
| A10 | 截面残差 | `subtract(ts_zscore(A,W), group_neutralize(ts_zscore(A,W), industry))` | 需要剥离行业共同因子 | IND 出货模板 | 未测 |
| A11 | 双重标准化 | `group_zscore(ts_zscore(X, W), industry)` | 分布偏斜、需两级标准化 | 论坛方法论 | 未测 |
| A12 | 时间衰减加权 | `ts_decay_linear(X, W)` | 近期事件更重要 | 论坛（交易后 3 个月最强） | EUR S 0.51（单窗组）；TO 172% 风险 |
| A13 | 自归一去拥挤 | `divide(X, ts_mean(X, 252))` | 水平量、想做时序标准化 | 论坛单杠杆自归一 | 未测 |
| A14 | **多口径加权合成** | `add(multiply(k, group_rank(A, ind)), group_rank(B, ind))` | 同机制、不同参与人/来源的字段对 | **本战役自建**（破 prod 墙用） | EUR **S 1.95 / F 0.99 / sub 1.14 / 2Y 1.65 / fRA=1**（2:1 @decay8） |
| A15 | 风险门控 | `if_else(风险条件, 0, 主信号)` | 主信号 + 一个极端风险字段 | 论坛 43615381230871 评论（卖侧当风险闸） | 未测 |
| A16 | 比率族（基本面） | `divide(A, B)` 同级量纲比 | 财务三表成对字段 | 经典价值/质量因子文献 | 未测（本区 fundamental 已判死） |

## 二、模板选择的判据（按画像 → 模板）

1. **稀疏事件流 + 时点可信** → A2 / A4；**时点不可信（延迟披露）** → A1 / A3（累计量）。
2. **字段有成对 total/avg** → A4；**有成对 top/无前缀** → A5；**有成对 buy/sell** → A6。
3. **两个字段共享同一规模因子且量纲不同** → A3（差量纲相除，不是同族加减）。
4. **分布肥尾 + 极值主导** → A9；**分布偏斜但连续** → A11。
5. **信号强但 prod 卡墙** → A14（多口径合成），这是唯一在本区实证有效的破墙模板。
6. **单字段已有效但需要去拥挤** → A13 / A10。

## 三、失败模板黑名单（本区实证）

| 模板 | 失败证据 |
|---|---|
| A2 异常度 @EUR | insider S 0.90 / 0.58（欧盟延迟披露） |
| CROWDING 中性化 | S 0.86 双条（摧毁因子） |
| subindustry 分组轴 | S 1.60（细分组稀释） |
| 双窗平滑 add(ts_sum(63), ts_sum(126)) | S 1.71（稀释单一行为窗） |
| 窗口 126 | S 1.44（信息稀释） |
| 宇宙换 TOP1200 | S 1.22（信号在中小盘） |
| 全体董事口径 + 卖出腿 | 2Y 1.97→1.29（被动卖出稀释） |

## 四、使用纪律

- 每个数据集做画像后，**至少匹配 10 个结构互异模板**再派发。
- 每批恰好 2 条、批级设置单一；一条表达式 ≤12 算子。
- 判死需「同一面 ≥6 全灭」+ 四项必查（中性化档全试 / 毒字段排查 / 结构族覆盖 / decay 与窗口穷举）。


## 五、画像 → 模板 指派表（47 个数据集已画像；随遍历持续回填）

> 判据：**字段画像 = 字段族 × 覆盖 × 拥挤度 × 时间形态**；模板按画像里「信息加工方式」匹配，不按数据集名字匹配。
> 状态标记：⏳ 待派发 / 🚀 已派发 / ✅ 已出结果 / ⛔ 画像阶段即排除。

### 5.1 NEWS 族（20 个数据集）
| 数据集 | 画像族 | 指派模板 | 状态 |
|---|---|---|---|
| **news73** | 新闻情绪多维（fear/uncertainty/certainty/hype/volatility），cov 0.813，ac ≤18 | A1 水平量（uncertainty/fear）、A9 极值几何 | 🚀 第23批 |
| **news48** | 事件新奇度（ENS 0–100 + 相似事件间隔天数），cov 0.6326，ac ≤24 | A1 新奇度、A4 事件计数、A13 自归一（新奇度/间隔） | 🚀 第23批 |
| **news84** | 情绪转移族（mean/median/max/min/**skew**/sum）+ 新闻条数，cov 0.66–0.80 | A1 均值、A9 偏度、A4 关注度（条数） | ⏳ 第24批 |
| **news76** | 单一情绪 −1/0/1 + MMN 标签，cov 0.7263 | A1/A6；`mws76_score_value` 恒 0＝毒字段 | ⏳ |
| **news38** | 新闻热度 heat + 正负分，ac ≤12 | A1 heat、A6 方向纯度 | ⏳ |
| **news36** | novelty / 正负 phrase / key_event_confidence / relevance，cov 0.7713 | A1、A2、A9、置信度加权 | ⏳ |
| **news52** | 电话会结构（P/Q&A 的字数·句数·段落·问题数·发言人轮次·参与者数） | **A5 层级份额（Q&A/P 结构比）**、A4 参与度 | ⏳ |
| news23 | 融资事件（发行价/投资轮/可转债比），cov 0.19–0.77 | A4 事件（需事件过滤） | ⏳ 低优先 |
| news54 | 时间戳/日历/布尔/文本，仅 1 个数值字段 | — | ⛔ 低产 |
| news_sentiment_dl | 词级情绪 + 可读性，三文本源 | —（**Wave1 已 24 探针判死**） | ⛔ 已判死 |

### 5.2 OTHER / 另类数据族（36 个数据集）
| 数据集 | 画像族 | 指派模板 | 状态 |
|---|---|---|---|
| **institutions6** | 机构买入/卖出**家数** + 持有人数 + 持股金额，**cov 0.9976**（覆盖率最高） | **A4 持股广度**（论坛 37137602566679 改进式：ts_rank(126)+波动率归一）、A6 方向纯度 | 🚀 第22批 |
| **other553** | 财报文本语言学（blame 归因 / 被动语态比 / 数字密度 / 句长），cov 0.47–0.97 | **A1 归因强度**（blame/word）、A11 双重标准化 | 🚀 第22批 |
| **other567** | 员工评价（business outlook / CEO approval / culture / senior mgmt），cov 0.5277，ac ≤16 | **A1 满意度水平（Edmans 2011）**、A7 变化 | ⏳ 第24批 |
| **news_sentiment_nlp** | 标题情绪 / 可读性 / 主客观，**cov 0.9134**，ac ≤13 | A1、A6 正负极性、A9 情绪方差 | 🚀 第21批 |
| **stock_search_trends** | Google 搜索兴趣多窗（today/7d/14d/28d/84d/1y）MATRIX | **A13 自归一（7d/84d）**、A2、A7 斜率 | 🚀 第21批 |
| **ai_news_scores** | 情绪均值 + 95% 置信上下界 + 离散度 + 极值，105 字段 cov 0.7924 | A1、A9、A11、**置信度加权** | ⏳ |
| **earningscall_sentiment** | 电话会 主题×章节(P/Q/A/Summary)×极性 + chunk 计数，167 字段 | **A5 章节差（Q&A−Presentation，Matsumoto 2011）**、A6 主题极性 | ⏳ |
| **fund_holdings_panel** | 基金持仓/交易 HHI、边界交易、large_trade、conviction 交易，cov 0.84–0.92 | A4 集群度、**HHI 拥挤度门控** | ⏳ |
| **equity_forum_data** | 论坛买卖情绪 + 评论量 + 参与人数，cov 0.406 | A6 分歧度（Miller 1977）、A13 关注度 | ⏳ |
| **euro_equity_imbalance** | 参与者级主动买卖 + HHI 集中度，cov 0.3175 | A1、A4、HHI 门控 | ⏳ |
| **other571** | Wikipedia 浏览量（1d/7d/14d/28d/84d/1y × 时段/设备），cov 0.78 | A13 自归一、A1 | ⏳ |
| **acquisition_model** | 并购目标概率（valuation/size/credit/text 四轴），cov 0.7484 | A1、A5 层级份额、A10 截面残差 | ⏳ |
| **other545** | NEMO2.0 复合分（价格动量 + **NLP 同业网络动量**），cov 0.5424 | A1、A14 合成 | ⏳ |
| **other546** | 同业网络连接度（busnet/geonet/risknet），cov 0.30–0.43 | **分组轴 / 门控**（非信号） | ⏳ |
| other296 / other635 | 电话会 / 新闻标题情绪 + 长度 | A1、A7 | ⏳ |
| other250 | 电商产品（价格/评分/评论/畅销排名），cov 0.49 | A1、A4 | ⏳ |
| other128 | CEO/CFO 任期与薪酬 z-score，cov 0.3893 | A1、A5 | ⏳ |
| event_relation | 实体关系类型 + 关系强度（并购/合作/财务） | A4 事件 | ⏳ |
| event_sentiment_signals | 关键驱动事件正负分 + 事件计数，cov 0.3567 | A6、A4 | ⏳ |
| other699 | 机构持股变动（shares traded / new / prev），cov 0.2732 | 比值探针已死（S −0.11） | ⛔ 低优先 |
| other315 / stock_cluster_dl / other436 | 衍生品枚举 / 无标签 PCA / divyld+mktcap | — | ⛔ 排除 |

### 5.3 FUNDAMENTAL 族（13 个数据集）
| 数据集 | 画像族 | 指派模板 | 状态 |
|---|---|---|---|
| fundamental93 / other452 | 递延税 + 税应计（BTD），cov 0.19–0.54，ac ≤6 | A1（BTC 探针 S −0.24） | ⛔ **EUR 不深挖**（欧洲应计异象论文否定），迁美国区 |
| fundamental22 | 单字段 ESG KPI，cov 0.6866，ac 26 | A1（ESG 水平量） | ⏳ |
| fundamental25 | 运营指标 key-value 面板，cov 0.25 | 需 metriccode 过滤 | ⏳ 低优先 |
| digital_ad_spend | 广告投放 6 字段，cov 0.1725 | — | ⛔ 覆盖过低 |

### 5.4 ANALYST / RISK / INSIDERS / 其它
| 数据集 | 画像族 | 指派模板 | 状态 |
|---|---|---|---|
| analyst45 | 投资想法绩效（net_market_exposure ac158 / jensensalpha），cov 1.0 | A1 暴露水平、A7 变化 | ⏳ |
| analyst_base_ref | 一致预期 + 意外 + 股数，cov 0.32/0.97 | **A4 意外事件（PEAD）**、A1 | ⏳ |
| analyst40 | 董事会结构（turnover / age / gender），cov 0.27–0.36 | A1 治理、A7 | ⏳ 覆盖薄 |
| analyst81 | 违约概率族，cov 0.23 | 低优先 | ⏳ 低优先 |
| risk72 / risk68 | 残差收益 / beta / DADV，cov 1.0 | **残差动量/反转**、A10 截面残差 | ⏳ |
| risk60 | 证券借贷（borrow fee / crowding），cov 0.8168，ac ≤835 | A1 卖空压力（拥挤） | ⏳ |
| imbalance5 | `imb5_score` ac 15128 | — | ⛔ 极拥挤 |
| macro10 / model52 / socialmedia15 | 泛值单字段 / PD / 多维情绪 | A6（socialmedia 分歧度） | ⏳ |

## 六、本轮新增的论坛 / 论文来源（供模板溯源）

| 来源 | 类型 | 关键结论 |
|---|---|---|
| 论坛 43691920040087「应计家族：五种算法一个故事」 | 论坛 | 应计高＝利润质量可疑；**必须五口径同跑**，单口径报警属模型问题 |
| 论坛 37137602566679「机构情绪分歧因子」 | 论坛 | `(buy−sell)/(buy+sell+1)` 原始式平庸；改进＝`ts_rank(raw,126) / ts_std_dev(returns,20)` + 短线反转腿 |
| Gonçalves/Gaio/Lélis《Accrual mispricing: Evidence from European sovereign debt crisis》 | 论文 | **欧洲不存在应计异象**（2005–2016） |
| Weber (2005)《Book-tax differences, analysts' forecast errors, and stock returns》 | 论文 | BTD 的收益预测力走**分析师预期误差**渠道 |
| Görlitz & Dobler (2021) 递延税实证综述 | 论文 | 递延税价值相关性证据**集中在 US**，非美薄弱 |
| Choi/Jin/Yan (2013)《What Does Stock Ownership Breadth Measure?》 | 论文 | 散户广度上升 → 未来收益**极低**（−23%/年，t=9.7）；**机构广度上升 → 未来收益高** |
| Edmans (2011)《Does the stock market fully value intangibles?》 | 论文 | 员工满意度高的公司长期跑赢（年化 ~3.5%） |
| Matsumoto/Pronk/Roelofsen (2011) | 论文 | 电话会 **Q&A 语气比 presentation 更有信息量** |
| Miller (1977) | 论文 | 意见分歧 + 卖空约束 → 高估 → 未来低收益 |
