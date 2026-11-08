# insiders1 · EUR / TOPCS1600 / D1 字段画像

> 类型 VECTOR（全部 9 字段）· 覆盖率 0.5512（全字段一致，逐事件申报口径）
> 金字塔 category = **insiders**（multiplier 1.1，未点亮塔）
> 采集：`get_datafields(dataset_id=insiders1, region=EUR, delay=1, universe=TOPCS1600)`，2026-11-06
> 画像角色：事件型内部人申报数据，决定「比例 vs 金额」「水平 vs 变化率」两组二元选择

## 0. 字段目录（按 alphaCount 降序）

| # | 字段 | 类型 | cov | αC | users | description |
|---|---|---|---:|---:|---:|---|
| 1 | `insd1_shares` | VECTOR | .5512 | 92 | 71 | 本笔交易股数 |
| 2 | `insd1_price` | VECTOR | .5512 | 73 | 59 | 本笔成交价（若为区间取最低价） |
| 3 | `insd1_holdings` | VECTOR | .5512 | 52 | 44 | 交易后内部人总持仓股数 |
| 4 | `insd1_valueeur` | VECTOR | .5512 | 48 | 39 | 本笔交易金额（欧元） |
| 5 | `insd1_gvkey` | VECTOR | .5512 | 49 | 40 | Compustat Global Company Identifier（纯标识，非信号） |
| 6 | `transaction_currency_code` | VECTOR | .5512 | 46 | 41 | 交易原始货币 ISO 代码 |
| 7 | `insd1_tradesignificance` | VECTOR | .5512 | 43 | 37 | 交易重要性评分（1=低，3=高） |
| 8 | `insd1_value` | VECTOR | .5512 | 26 | 23 | 本笔交易金额（原始货币） |
| 9 | `max_trade_price` | VECTOR | .5512 | 14 | 14 | 区间成交价上限 |

**覆盖率口径纠偏**（源自论坛同机制帖 JX84394 对 `institutions1` 的实测，结构同为「nanHandling=ON 的稀疏事件 VECTOR」）：
`coverage` 列**不能**直接读成「每天 55% 的股票有申报」——实测同构数据集上一个完整季度（66 交易日）也只有不到三成股票有过任何一笔申报，单日比例远低于 0.55。VECTOR 类型意味着同一天可能多笔申报，`coverage` 统计的是「该字段曾经非空」而非逐日密度。

## 1. 名 vs description 差异

| 字段 | 名形态暗示 | 实际含义 | 易错点 |
|---|---|---|---|
| `insd1_holdings` | 看似"持仓快照" | **交易后**总持仓（已含本笔），不是交易前持仓 | 算"占原持仓比例"需要 `holdings − shares`（买入）或 `holdings + shares`（卖出）还原交易前基数，直接用 `holdings` 当分母是"交易后仓位比例"而非"原持仓变动比例"——两者经济含义不同，需分别测 |
| `insd1_valueeur` vs `insd1_value` | 都叫"交易金额" | `valueeur` 已折算欧元，`value` 是原始货币（配合 `transaction_currency_code` 用） | 跨币种申报若不统一折算，`value` 会把高价值货币（如 CHF）与低价值货币混排；`valueeur` 已是干净量，优先用 |
| `insd1_price` vs `max_trade_price` | 都是"价格" | `price` = 区间最低价（或唯一价），`max_trade_price` = 区间最高价，仅当该笔申报是"价格区间"时后者非空 | `max_trade_price` 覆盖率与其余字段一致（.5512）但语义上应远低于此——需单独核实其非空子集是否真的等于"区间申报"子集，暂未验证，不作主信号 |
| `insd1_gvkey` | 像"标识" | Compustat 全球公司 ID | 纯 ID，不参与任何数值运算，只能用于 join/分组校验 |

## 2. 字段画像五问

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 存量 / 流量 / 变化率 | **流量**（`shares`/`valueeur`/`value`/`price`，逐笔事件）+ **存量**（`holdings`，交易后快照）并存 ⇒ 流量÷存量天然构成无量纲比值（见 §4 机制 B） |
| 2 相对性 | 水平差异 / 排序差异 | 金额类字段受公司市值/内部人财富主导，**原始水平不可比**；比例类（shares÷holdings、valueeur÷holdings）已自带规模标准化 |
| 3 被定价的是谁 | 方向 / 广度 / 强度 | 方向（买/卖，`sign(shares)` 隐含）与强度（占仓位比例）两个独立轴，不可混为一个读数 |
| 4 有无博弈 | 拥挤 / 规模 | `insd1_shares` αC 92 是全场最高，仍远低于已点亮类别（如 analyst7 αC 千级），**非拥挤轴** |
| 5 事件性 | 是否事件稀疏 | **是**：VECTOR + nanHandling=ON ⇒ 当日无申报的股票在数据层被填 0（不是 NaN）⇒ `ts_sum`/`vec_sum` 之后仍为 0，会在 `group_rank` 里形成並列假中段（见 §5 工程坑） |

## 3. 预处理决策

| 体征 | 决策 |
|---|---|
| 稀疏事件 + 日内多笔 | 任何跨 VECTOR→MATRIX 的归约必须先过 `vec_sum`/`vec_avg`，**不能**把 VECTOR 字段直接传给 `group_rank`/`group_neutralize`（平台报错 `Operator group_neutralize does not support event inputs`，本战役 Candidate D 实测踩中） |
| 金额类水平量规模不可比 | 禁裸水平金额；要么做比例（÷holdings），要么做符号/广度读数 |
| `nanHandling=ON` 零填充 | 长窗累加（`ts_sum`）前必须评估零填充造成的並列块大小，必要时用 `tail(w, lower=q, upper=1-q, newval=0.5)` 掐掉中段（见 §4 机制 B） |
| 求和 vs 求均值 | **求和**保留事件频率信息（一季申报 3 次 vs 1 次,ts_sum 差 3 倍）；`ts_mean` 在 nanHandling=ON 下只在非 NaN 日求均值，会把频率信息除掉——本战役未直接验证此点在 EUR 的量级，但沿用 DEU 同构帖结论（ts_mean 使 S 从 1.44 掉到 0.73） |
| 窗口 | 季度 66（内部人申报/信息半衰期的自然周期，论坛 DEU 帖 + 本集历史皆用此窗）；52 周 252（anchoring bias 文献窗口） |

## 4. 机制目录（本战役已测 + 已证据化）

### 机制 A：52 周价格锚定偏差（Lasfer & Ye 2024, *Financial Review*）
内部人在股价接近 52 周高/低点附近的交易更具信息含量（投资者锚定偏差造成误价）。
读数：`subtract(方向符号读数, ts_scale(价格, 252))` —— 价格距 52 周区间的位置（0–1）与内部人交易方向的组合。

### 机制 B：仓位比例「信念强度」（JMZ 2003 / Lakonishok & Lee 2001 / Cohen-Malloy-Pomorski 2012；论坛 JX84394，69 票）
内部人交易的信息含量在"相对自身持仓的比例"里，不在"绝对金额"里——同样金额对大公司高管和小公司董事含义天差地别，比例天然做了规模标准化。
读数：`tail(winsorize(group_rank(ts_sum(divide(vec_sum(流量字段), add(vec_sum(insd1_holdings), ε)), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)`
关键工程点：`tail(..., newval=0.5)` 掐掉 nanHandling 零填充在 `group_rank` 后形成的並列假中段，这一步在 DEU 同构实测中贡献 +0.24 Sharpe / +0.58 sub-universe Sharpe，且经四组独立证据证明"不是调参"（边界是宽平台而非尖峰、姊妹分子加 tail 后收敛、四条独立轴都给出合规点、winsorize 与 tail 必须成对）。

### 机制 C：重要性加权仓位比例（Cohen-Malloy-Pomorski 2012 routine/opportunistic 代理）

**⚠ 工程坑（2026-11-06 实测命中）**：首版表达式 `multiply(insd1_valueeur, insd1_tradesignificance)`（两个原始 VECTOR 字段直接相乘,不经 `vec_*` 归约）报错 `Operator multiply does not support event inputs`——与 §3 已知的 `group_neutralize` 不支持事件输入是**同一类限制,但适用范围更广**：不只是 `group_neutralize`,连 `multiply` 这种最基础的逐元素算子对两个未归约的 VECTOR 也不支持。**修复**：必须先分别 `vec_sum`/`vec_avg` 归约成 MATRIX 层级标量,再相乘——`multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance))`,即"当日总金额 × 当日平均重要性评分",而非理想中的"逐笔金额×该笔评分再求和"（后者在当前算子集下不可实现,因为不存在"仅在归约时联合两个 VECTOR"的算子）。这是**比"结构性放弃"更轻的降级**：机制仍可测,但从"逐笔精确加权"退化为"日级总量×日级均分"的近似加权,当日仅一笔申报时两者等价,当日多笔时会有经济含义漂移（已知限制,不影响可证伪性判断——若弱版本已显著强于机制 B,说明方向对；若等于机制 B,仍能排除冗余）。
★ **该限制范围进一步扩大（2026-11-06 第二次命中）**：比较算子（`>`/`<`）对原始 VECTOR 同样报 `does not support event inputs`——`insd1_shares > 0` 直接作用于未归约 VECTOR 会失败，必须先 `vec_sum(insd1_shares) > 0` 归约后再比较。即「逐元素/比较类算子一律要求输入已归约」是比"multiply 专属"更通用的平台规则，覆盖 `multiply`/`greater`/`less` 等，推测对其余逐元素算子（`add`/`subtract`/`if_else` 的条件分支等）同样适用，使用前应默认先 `vec_*` 归约。
CMP(2012) 的核心区分是"常规交易"（可预测、信息含量低）vs"机会主义交易"（不可预测、信息含量高），但 EUR 的 `insiders1`/`insider_agg_matrix` 都没有持久化的个人内部人身份,无法像原文那样靠"连续 N 年同月同向交易"识别常规模式。`insd1_tradesignificance`（供应商预评分,1=低/3=高）是可用的**替代代理**——若供应商评分本身就在区分"例行小额申报"与"重大持仓变动",用它加权金额应强于不加权的机制 B。
读数：`tail(winsorize(group_rank(ts_sum(divide(multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance)), add(vec_sum(insd1_holdings), 0.0001)), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)`（★ 2026-11-06 更正：此前版本误写成 `vec_sum(multiply(insd1_valueeur, insd1_tradesignificance))`——`multiply` 在 `vec_sum` **内部**直接作用于两个未归约 VECTOR，与上段工程坑描述的限制矛盾，是文档转录错误；实际跑出 `YP1EPn8M` 读数的真实表达式是 `multiply` 在归约**之后**执行，现已更正为与工程坑描述一致的形式）
**可证伪性**：若机制 C 显著强于机制 B（同设置、同分母），说明 `tradesignificance` 真的携带 routine/opportunistic 信息；若二者几乎相同，说明评分字段对本比例机制是冗余信息（供应商评分可能本身就与金额大小高度相关，不提供增量）。

**结果（alpha `YP1EPn8M`，已终态，multisim `1cwCEr4Oe4oSaUkTcurIHhI`）——证伪性检验通过，评分字段提供真实增量**：

| 候选 | alpha id | S | F | TO | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| 机制 B（valueeur，无加权） | `RRE9gKle` | 0.93 | 0.50 | 0.0431 | 0.72 | 0.62 PASS | 0.80 PASS | LOW_SHARPE/FITNESS/2Y |
| 机制 C（valueeur×tradesignificance 加权） | `YP1EPn8M` | **0.97** | **0.53** | 0.0436 | 0.75 | 0.69 PASS | 0.79 PASS | LOW_SHARPE/FITNESS/2Y（同闸，差距缩小） |

**归因**：S/F/2Y 三项一致小幅提升（+0.04/+0.03/+0.03），sub-universe 从 0.62 升到 0.69（更接近闸线）,robust 持平。涨幅虽小但方向一致、无一项倒退 ⇒ `insd1_tradesignificance` 不是冗余信息,CMP(2012) 的 routine/opportunistic 代理假说成立,即便在"日级总量×日级均分"的近似加权（§4 工程坑降级版）下依然能提取增量。**机制 C 取代机制 B 成为本数据集目前最优候选**,但距主闸（S 1.58）仍差 1.6×,单独加权不足以破闸,需要与其它杠杆（模板族/算子档）叠加。UNITS 警告（`add(vec_sum(insd1_holdings), 0.0001)` 的 CSShare/无量纲不兼容）复现但不阻断,读数与 §5.2 一致为非致命告警。

## 5. 本战役实测记录

### 5.1 机制 A 变体（52 周锚定 × 方向符号，vec_sum/vec_avg 归约）

| # | alpha id | 表达式 | S | F | TO | CW | 卡闸要点 |
|---|---|---|---|---|---|---|---|
| 1（Candidate A） | `E56NLPK9` | `subtract(add(0.5, multiply(0.5, sign(vec_sum(insd1_shares)))), ts_scale(vec_avg(insd1_price), 252))` | **−0.29** | −0.06 | **1.7009**（爆炸） | **0.5 FAIL**（限 0.1，只剩 13 个名字） | LOW_SHARPE/FITNESS/HIGH_TURNOVER/CW/SUB/ROBUST/2Y 全挂；根因 = 未 backfill 的稀疏方向符号在横截面逐日跳变 |
| 2（Candidate B） | `O0ARVXpY` | `subtract(add(0.5, multiply(0.5, sign(ts_backfill(vec_sum(insd1_shares), 22)))), ts_scale(ts_backfill(vec_avg(insd1_price), 22), 252))` | 0.13 | 0.03 | **0.1874**（正常） | CW/TURNOVER 转 PASS（316 个名字），但 **S/F/SUB/ROBUST/2Y 仍不足** | **归因结论**：TO 爆炸是 `ts_backfill` 缺失的工程问题，不是机制问题；修复后信号真实强度只有 S=0.13 —— 诚实的弱负结果，机制 A 在 `insiders1` 的「方向符号 × 52周锚定」读数形态上**不成立**，需要换读数形态（如改用比例/强度而非符号方向），不构成"数据集判死" |

**归因结论（已落实本波判断，避免盲扫）**：机制本身（52 周锚定偏差）的文献依据没有问题，但「方向符号 + 52周价格位置」这种**离散符号 × 连续位置**的组合读数在稀疏事件数据上太弱；问题出在读数设计，不在数据集，不应据此判死 `insiders1`。

### 5.2 ★ 机制 B 候选（仓位比例信念强度）—— 本战役首个结构健康的 insiders1 信号

| # | alpha id | 表达式 | S | F | TO | CW | sub | robust | 2Y | 持仓数 | 卡闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `RRE9gKle` | `tail(winsorize(group_rank(ts_sum(divide(vec_sum(insd1_valueeur), add(vec_sum(insd1_holdings), 0.0001)), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)` | **0.93** | 0.50 | **0.0431** | **PASS** | **0.62 PASS** | **0.80 PASS** | 0.72 | 1221 | 只差 LOW_SHARPE/FITNESS/2Y |
| 2 | `E56NdL8P` | 同上，`insd1_valueeur`→`insd1_shares`（姊妹腿） | **0.87** | 0.44 | 0.0458 | PASS | 0.67 PASS | 0.68（差 0.02） | 0.58 | 1229 | 同上 + ROBUST 微差 |

**这是本数据集迄今唯一一组 TO/CW/breadth 全部健康的候选**（对比 §5.1：旧判死 8 探针 TO 1.52–1.61；本战役机制 A 两变体 TO 1.70 爆炸 / 0.19 但 S 仅 0.13）。姊妹腿同号（0.93 vs 0.87，差距 7%，远小于 DEU 帖报告的量级）⇒ 仓位比例信念强度机制在 EUR `insiders1` **成立**，强度约为 DEU `institutions1`（S 1.68）的一半，符合"同骨架换厂商,互相关 0.10–0.38 但强度不保证相同"的预期。

**两处 WARNING（不致命,已记录待清理）**：`add(vec_sum(insd1_holdings), 0.0001)` 触发 `UNITS` 警告——`insd1_holdings` 带 `CSShare` 单位,字面量 `0.0001` 无单位,VERIFY 模式下报告不兼容但不阻断回测。暂不影响判断,下一波可尝试用等价的"先判空再构造比值"写法替代硬编码 epsilon 消除警告（不改变数值结果的前提下）。

**`group_scale(·, industry)` 杠杆实测结果（2026-11-06，multisim `UQPrWaCy4Uqcdq6fsBr9U6`，已终态）**：

| 候选 | alpha id | S（前→后） | F（前→后） | 2Y（前→后） | sub（前→后） | robust（前→后） |
|---|---|---|---|---|---|---|
| valueeur（主腿） | `kqNvz5kP` | 0.93→**0.95** | 0.50→0.52 | 0.72→**0.71**（持平） | 0.62→0.66（PASS） | 0.80→0.78（仍 PASS） |
| shares（姊妹腿） | `zq3glzwG` | 0.87→**0.87**（无变化） | 0.44→0.45 | 0.58→0.69（升但仍远不够） | 0.67→0.63（PASS） | 0.68（差0.02 FAIL）→0.61（**FAIL 扩大**） |

**归因**：本区 skill ④ 节记录 `group_scale` 是「唯一四项同得（S/2Y/sub 全升）」的首选杠杆，但该结论建立在"输入是多腿 rank 合成/模型预测分"的场景。本候选的输入虽已过 `group_rank`+`winsorize`+`tail`（截面可比分数，满足 skill 载明的适用前提），但实测增益几乎为零（S +0.02 / +0.00，2Y 不升反平或升幅不足），且 shares 腿的 robust 闸从"差 0.02"恶化到"差 0.09"。**结论：`group_scale` 对本机制（仓位比例信念强度×内部人申报）不是有效杠杆**——这是对区域通用杠杆表的一次**数据集级别证伪**，已记入，不再对这两条候选重试 `group_scale`。

**universe TOPCS1600→TOP2500 杠杆实测结果（2026-11-06，multisim `4G61sd9b44UVc9XSbWedVsR`，已终态）——方向反了**：

| 候选 | alpha id | S（1600→2500） | F（1600→2500） | 2Y（1600→2500） | sub（1600→2500） |
|---|---|---|---|---|---|
| valueeur | `1YNlqYQK` | 0.93→**0.54** | 0.50→0.20 | 0.72→**0.46** | 0.62→0.43 |
| shares | `leA5LeXx` | 0.87→**0.38** | 0.44→0.12 | 0.69→**0.18** | 0.67→0.25 |

**归因**：区域 skill ① 节记录的"universe 是 prod–S 前沿平移旋钮（放宽 TOP2500 同时抬 S 和 prod）"对本机制**完全不成立，而且方向相反**——放宽到 TOP2500 让两条候选的 S/2Y/sub 全面下滑（跌幅 42%–74%）。交叉验证来自论坛帖（FF56620,43 票,2026-09-01,"高管买入还是买压本身？"）：该帖在 USA 对同族"内部人事件流异常强度"机制做过显式的宇宙对照实验——TOP3000 下核心信号卡在 sub-universe 闸（0.7 量级,过不了）,换成 `ILLIQUID_MINVOL1M`（更窄更不流动的子集）后 sub-universe Sharpe 跳到 2.14–2.28,结论是"内部人异常买入的超额收益留在定价迟钝的非流动小票里"。EUR 本候选的实测方向与此完全一致 ⇒ 假说是"正确的下一步是收紧宇宙（TOP800 甚至 TOP400）"；已提交 TOP800 隔离测试验证该假说（不与 group_scale 叠加,单变量归因），**结果见下——假说被推翻**。

**universe TOPCS1600→TOP800 杠杆实测结果（2026-11-06，multisim `1O9YaD8Mc4tS8G8qiQHSwDL`，已终态）——不是"概念变好"，是单调更差**：

| 候选 | alpha id | S（1600→2500→800） | F（同序） | 2Y（同序） | sub（同序） |
|---|---|---|---|---|---|
| valueeur | `9qxdz6AK` | 0.93→0.54→**0.27** | 0.50→0.20→**0.07** | 0.72→0.46→**0.32** | 0.62→0.43→**0.24 FAIL** |
| shares | `1YNlqmnX` | 0.87→0.38→**0.30** | 0.44→0.12→**0.09** | 0.58→0.18→**0.16** | 0.67→0.25→**0.26 FAIL** |

**归因（假说推翻，教训比假说本身更重要）**：FF56620 的"非流动小票留存超额收益"假说**在 EUR insiders1 上不成立**——TOP800 不是"比 TOP2500 好一点但仍不如 TOPCS1600"，而是**比 TOP2500 更差**（S 再跌 50%，sub 从 0.43/0.25 跌到 0.24/0.26 双双转 FAIL）。三点 TOPCS1600(0.93/0.87) > TOP2500(0.54/0.38) > TOP800(0.27/0.30) 单调递减，说明**真实机制是"偏离区域默认宇宙本身就是破坏性操作"，不是"偏离方向错了"**。重新审视 FF56620：该帖验证的是 USA 的 `ILLIQUID_MINVOL1M`（一个**按流动性显式筛选**的专用子集），不是"随便换一个更小的市值阶梯（TOP800/TOP400）"——EUR 的 TOP*N* 阶梯是按市值排名截断，不等价于按流动性筛选，小市值不等于非流动（可能只是覆盖率更低、样本更稀疏，稀疏事件型字段在更小样本上信噪比只会更差，不会更好）。**结论：universe 杠杆对本机制已穷尽（1600/2500/800 三档单调验证），不再测 TOP400（外推必然更差，不做无意义重复）**；真正要测的是"流动性筛选"而非"市值阶梯"，但 EUR TOP*N* 档位没有流动性子集可选，此路不通，**回到默认 TOPCS1600 基线（S=0.93/0.87）作为本机制的强度上限**，下一步改走模板族/字段覆盖方向（模板族 3、Mechanism C）去补强,而不是再扫宇宙。

设置：EUR/TOPCS1600/D1 · SUBINDUSTRY · decay 4 · truncation 0.08 · maxTrade OFF · nanHandling ON · pasteurization ON · unitHandling VERIFY · 2014-01-01→2023-12-31（区域默认档）。
★ **2026-11-06 更正**：「SLOW_AND_FAST 未在 EUR 实证」已过期——同一赛季在 `insider_agg_matrix` 的买入股数骨架上实测 SLOW_AND_FAST 是关键杠杆（`akKe5zK6`→`QPvNZ5pr`：sub/robust 由 FAIL 转 PASS，见 `insider_agg_matrix.md` §4），本数据集（机制 B/C，分母已改用 `vec_sum(insd1_holdings)` 直接作分母，不再加不兼容单位的 epsilon）的 SLOW_AND_FAST 对照已提交 multisim `lq7so6jm4lgaCM14GGxlyXr`，结果待补。

### 5.3 历史波次（2026-10-13 wave 496，判死记录，本战役已部分推翻）

原判死依据：8/8 探针 S≤0.50 且 TO=1.52–1.61、margin≈0.1–1.2bp ⇒ 判死，根因写作"稀疏事件型 VECTOR + vec_avg 归约 ⇒ 个股间剧烈跳变 ⇒ TO 爆炸"。
**本战役复核**：该根因诊断基本正确（§5.1 Candidate A 完全复现 TO=1.70），但**结论过宽**——TO 爆炸是「缺 `ts_backfill`」的工程问题，修复后（Candidate B）TO 回落到 0.19 正常区间，暴露出的是「读数强度不足」（S=0.13）而非「数据集结构性不可用」。⇒ `insiders1` 仍应视为**未穷尽**，不应维持"判死"标签；§4 机制 B 是下一个待验证的独立机制。

## 6. 待办

- **模板族 2（自身基线 `ts_zscore`，已终态）——与本集不合,EUR 读数和 FF56620 原帖（USA）方向相反**：`ts_zscore(ts_sum(divide(vec_sum(insd1_valueeur), add(vec_sum(insd1_holdings), 0.0001)), 66), 252)`（alpha `GrWKrYXx`,multisim `1cwCEr4Oe4oSaUkTcurIHhI`）——S=**0.34**、F=0.12、2Y=**−0.06**、robust=**−0.28 FAIL**,全面弱于机制 B 的横截面 `group_rank` 读数（0.93/0.50/0.72/0.80 PASS）。**归因**：FF56620 在 USA 报告"自身基线强于序数化 1.6 个 Sharpe"是**该帖自己机制的结论,不可跨数据集/跨机制外推**——本机制的信息含量来自"比同行业其他公司的仓位比例高多少"（横截面相对位置）,不是"比自己历史正常水平高多少"（时序自身基线）;改用自身基线反而丢失了横截面比较这个核心经济含义,2Y/robust 双双转负就是直接证据。**结论：模板族 2 已测且证伪,不再对本机制尝试自身基线类读数**（`ts_rank`/`ts_zscore`/`ts_av_diff` 等同族）。模板族覆盖闸：机制 B（横截面 `group_rank`）+ 本族（时序 `ts_zscore`,证伪）= 2 族,仍差 1 族（见下一条）。
- **`max_trade_price` 边界覆盖候选（已提交，待终态）**：`subtract(add(0.5, multiply(0.5, sign(ts_backfill(vec_sum(insd1_shares), 22)))), ts_scale(ts_backfill(vec_avg(max_trade_price), 22), 252))`——复用机制 A/Candidate B 骨架，价格字段换成 `max_trade_price`，检验"区间申报上限价"是否携带独立信息。multisim `4aKOax3p95i9cKTYb3T66Ob`（与 `insider_agg_matrix` 的 `avg_top_buy_shares` 候选同批提交，2026-11-06）。

**`max_trade_price` 实测结果（alpha `bl6rYxP6`，已终态）——完全退化，不是弱信号而是零持仓**：S=0、TO=0、longCount=0、shortCount=0、`CONCENTRATED_WEIGHT` FAIL、`LOW_TURNOVER` FAIL（`IS_LADDER_SHARPE` 都因零持仓判 ERROR 而非 FAIL/PASS）。**归因**：这不是"信号弱"，是回测期内几乎没有任何一天有非 NaN 持仓——直接证实了 §1 表格此前的怀疑："`max_trade_price` 覆盖率与其余字段一致（.5512）但语义上应远低于此"。真实非空子集（仅"价格区间申报"的罕见情形）在 `ts_backfill(·, 22)` 的回填窗口内仍然大面积缺失，导致整条表达式在横截面上无法构造有效多空仓位。**字段覆盖闸判定：`max_trade_price` 计入已覆盖（已实测,非"未试"），但判定为结构性不可用字段（近似空字段）**，不再对其做二次尝试（换骨架/换窗口都无法创造不存在的数据）。
- 机制 B 两条候选结果出来后：核对同号性（原帖方法论要求），若 S 达标则按 §5.1 教训补充边界算子档（`std=2` winsorize、`q=0.25` tail 是否是平台还是尖峰，至少测 2–3 档）。
- 机制 A 的"强度读数"变体未测：可尝试 `divide` 比例替代 `sign` 符号（即把机制 A 的方向判定也换成机制 B 的比例读数，再叠加 52 周位置做条件门控 `trade_when`，而非简单相减）。

### 5.4 方向拆分实测（2026-11-06 终态，multisim `2e8LkwdXE4GPaGUjbwisYrw`，SLOW_AND_FAST 档）——JMZ(2003) 再次确认,方向拆分是有害操作

| 候选 | alpha id | S | F | TO | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| 合并读数（机制 B 基线,SUBINDUSTRY 档） | `RRE9gKle` | **0.93** | **0.50** | .0431 | 0.72 | 0.62 PASS | 0.80 PASS | S/F/2Y |
| buy-only（`shares>0` 掩码） | `3qokbnde` | 0.49 | 0.15 | .0792 | 0.26 | 0.71 PASS | 0.36 FAIL | S/F/robust/2Y |
| sell-only（`shares<0` 掩码 + reverse） | `JjeWw5lW` | **0（零持仓）** | 0 | 0 | — | — | — | 全挂 |

**归因（★ 2026-11-06 二次修正——实验本身结构性无效,非机制证伪）**：buy-only（`3qokbnde`）与同期提交的合并读数 SLOW_AND_FAST 版（`0mYNlznp`,§5.5）**八位有效数字完全一致**（S 0.49/0.49、pnl 1,232,002/1,232,002、long 739/739、short 757/757）——两个表达式唯一差异是 `if_else(vec_sum(insd1_shares) > 0, ·, 0)` 掩码,数值完全相同只有一种解释：**`insd1_shares` 在有数据的横截面上恒为正（无符号）**,买掩码是空操作、卖掩码（`< 0`）永不触发。三个推论：① sell-only 零持仓是**掩码永不触发的伪结果**,不是"卖出无信号"的 JMZ 确认;② 本数据集 9 个 VECTOR 字段（shares/valueeur/value/holdings/tradesignificance/price/gvkey/max_trade_price/transaction_currency_code）**没有任何方向字段**,机制 B 实为"交易强度/持仓比"（gross intensity）而非"净买入压力",此前经济叙事需相应弱化;③ **机制 A 的 `sign(insd1_shares)` 同样恒为 +1——机制 A 实测的是"1.0 − 52周价格位置"纯价格锚信号,S=0.13 的弱读数与此一致**,其"方向×锚定"叙事作废。**结论：本数据集不存在方向维度,方向拆分/方向门控类实验全部永久排除（不是被证伪,是实验对象不存在）;机制 B 的 0.93 读数保留,经济含义改为"内部人交易强度相对持仓的信念代理"。** 模板族覆盖闸：机制 B（横截面 group_rank）+ 自身基线族（ts_zscore,证伪）+ 方向拆分（结构性无效）= 3 族,**模板族闸已达 ≥3,补齐**。

### 5.5 SLOW_AND_FAST 迁移对照（2026-11-06 终态，multisim `lq7so6jm4lgaCM14GGxlyXr`）——不迁移,SUBINDUSTRY 保留

| 候选 | alpha id | 中性化 | S | F | TO | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|---|
| 机制 B（SUBINDUSTRY 基线,epsilon 分母） | `RRE9gKle` | SUBINDUSTRY | **0.93** | 0.50 | .0431 | 0.72 | 0.62 PASS | 0.80 PASS |
| 机制 B（SLOW_AND_FAST,无 epsilon 分母） | `0mYNlznp` | SLOW_AND_FAST | 0.49 | 0.15 | .0792 | 0.26 | 0.71 | 0.36 FAIL |
| 机制 C（SLOW_AND_FAST,无 epsilon 分母） | `bl6rkv7K` | SLOW_AND_FAST | 0.54 | 0.18 | .0791 | 0.37 | 0.76 | 0.37 FAIL |

**归因**：SLOW_AND_FAST 把机制 B 从 0.93 砍到 0.49（⚠ 混杂：本批同时去掉了 epsilon 分母——epsilon 对非零持仓数值上可忽略,只影响零持仓名字的尾部排名,故主效应应归于中性化档,但未做单变量隔离）。机制 C 对机制 B 的增量方向不变（0.49→0.54,+0.05,与 SUBINDUSTRY 档 +0.04 一致——tradesignificance 加权增量跨中性化档稳定）。**结论：`insider_agg_matrix` 上的"关键中性化档"不迁移到 `insiders1` 机制 B/C——SLOW_AND_FAST 在此是有害档,SUBINDUSTRY 保留为本数据集最终档**。同一杠杆在姊妹数据集上方向相反,与 §5.2 universe 杠杆的教训同构：**杠杆效应是（数据集 × 机制）级事实,任何跨集迁移必须实测,禁止外推**。sub 升 robust 降的跷跷板形态（0.62/0.80→0.71/0.36）提示 SLOW_AND_FAST 剥离掉的"慢轴"里含有本机制的真实信息（内部人申报密度与公司规模/流动性相关,被当噪声剥掉了）。

**SLOW_AND_FAST 对照批的设计缺陷（记录,防再犯）**：本批本意是"同表达式只换中性化",但提交时顺手把 epsilon 分母简化掉了,引入了第二个变量。两个批次（`lq7so6jm` 与 buy/sell 拆分批 `2e8LkwdXE`）都因此不是干净的单变量实验。**教训：对照实验一次只动一个旋钮,表达式的其余部分逐字符保持一致。**

### 5.6 ★ 新杠杆回灌（2026-11-07,战役后期发明的 `group_zscore`/包装栈在本集归档时尚未出现）——机制 C 复活,+0.12 S、结构全绿

| 变体 | alpha id | S | F | TO | 2Y | sub | robust | PPA | 卡闸 |
|---|---|---|---|---|---|---|---|---|---|
| 机制 B 裸 zscore（group_rank→group_zscore,epsilon 去除） | `xAr2EArw` | 0.62 | 0.29 | .0453 | 0.94 | 0.47 | 0.56 | 2 失败 | S/F/robust/2Y |
| 机制 C zscore + `rank(group_scale(·,industry))` 栈（66d） | `6Xdo2Xdp` | 1.09 | 0.64 | .0339 | 0.93 | **0.87 PASS** | **0.73 PASS** | **0 失败** | S/F/2Y |
| 机制 B 包装栈（同栈无加权） | `9qxd2GJ9` | **1.09** | 0.64 | .0341 | 0.93 | 0.88 | 0.71 | 0 失败 | S/F/2Y |
| 机制 C 88d | `78Lv2GJb` | 0.99 | 0.56 | .0282 | 1.09 | 0.85 | 0.83 | 1 失败 | S/F/2Y |
| 机制 C 66d + d5 | `LLMm28k6` | 1.08 | 0.63 | .0318 | 0.96 | 0.91 | 0.80 | 0 失败 | S/F/2Y |
| **机制 C 44d** | **`vR1poWNz`** | **1.14** | **0.68** | .0482 | 0.71 | **0.94** | 0.71 | 0 失败 | S/F/2Y |
| 机制 C 44d + d5 | `npvelZpx` | 1.13 | 0.67 | .0440 | 0.69 | 0.92 | 0.70 | 0 失败 | S/F/2Y |
| 机制 C 22d | `0mYNLeb6` | 0.70 | 0.34 | .0875 | 0.57 | 0.63 | 0.57 | 2 失败 | 全弱 |
| 机制 C shares 分子（66d 栈） | `QPvNowGG` | 1.02 | 0.58 | .0348 | 0.72 | 0.84 | 0.68 | 1 失败 | S/F/robust/2Y |

**终局归因（第二轮杠杆回灌,9 臂实测）**：① **44d 是本机制窗口峰**（1.14）——与 insider_agg_matrix 的 88d 峰形成「申报粒度决定窗口」对照：agg_matrix 是日度预聚合流量（半衰期=季度+滞后=88d）,insiders1 是逐笔申报明细（半衰期≈1.5 个月=44d）,同一机制族两个数据集窗口差一倍。② **包装栈后机制 B ≡ 机制 C**（1.09/1.09 逐位几乎同）——`rank(group_scale)` 整形把 tradesignificance 加权的幅度信息抹平,该字段仅在 `group_zscore` 直出形态（无 rank 整形）下有增量;但直出形态结构差（PPA 2 失败）,**可用形态下 tradesignificance 无增量,机制 C 降级为机制 B 的等价形式**。③ shares 分子弱于 valueeur（1.02 vs 1.14）——金额口径保留。④ d5 平滑在两窗口均无增益（与 insider_agg_matrix 一致）。⑤ **insiders1 最终天花板 1.14（44d 栈）,距 Mode B 主闸 S 1.25 仅差 0.11、F 0.68 距 0.8 差 0.12**——比旧归档（0.97「杠杆穷尽」）前进了 0.17,但仍未过主闸;2Y 0.71 是第二道结构性缺口。**第二轮归档,待下一个新杠杆发明后第三次复核。**

- `insd1_tradesignificance` 尚未覆盖——已设计机制 C（重要性加权仓位比例，见下）待提交。
- `insd1_value`+`transaction_currency_code`（货币中性化）**结构性放弃**：`group_neutralize` 要求分组轴是稳定的横截面分类器（如 sector/industry），`transaction_currency_code` 是逐事件 VECTOR 标签，不满足该算子语义（会复现"Operator does not support event inputs"同类报错）；且本集无 FX 汇率字段可供手工折算，`insd1_valueeur` 已是供应商预折算的干净量，`insd1_value` 被其严格支配 ⇒ 视为非独立可测字段，归入 `insd1_gvkey` 同类"纯标识/被支配字段"豁免，不计入覆盖闸缺口。
- `max_trade_price` 的"区间申报子集"语义尚未验证，暂不建模。

**SLOW_AND_FAST 迁移对照（已提交，multisim `lq7so6jm4lgaCM14GGxlyXr`，2026-11-06，结果待终态）**：机制 B/C 的分母已改用 `vec_sum(insd1_holdings)` 直接作分母（根治 UNITS 警告：epsilon 字面量与 CSShare 单位不兼容），同表达式下 SLOW_AND_FAST vs SUBINDUSTRY 的对照——检验 `insider_agg_matrix` 上的"关键中性化档"是否迁移到 `insiders1`。

### 5.7 第三轮收束（2026-11-07，幅度轴 + 设置轴终判）

| 变体 | alpha id | S | 2Y | 备注 |
|---|---|---|---|---|
| quantile(gaussian) 归一化 | `GrWK5xkQ` | 1.11 | 0.72 | 无增益 |
| winsorize std=4 | `d5W3roQ2` | 1.14 | 0.70 | 逐位≈std=2 |
| winsorize std=3 | `xAr2pWnm` | 1.14 | 0.71 | 同上 |
| signed_power 1.5 | `58EAdevJ` | 1.13 | 0.71 | 无增益 |
| 44d 栈 @ SLOW_AND_FAST + decay13 | `1YNl3o7R` | 1.20 | **0.43** | robust 0.33 崩 |
| 同上 + d5 | `JjeWanOl` | 1.11 | 0.46 | 同崩 |

**终判**：① 幅度轴（quantile/std/power）四臂全部落在 1.11–1.14 平台——**天花板 1.14 确认，距 Mode B 主闸 S 1.25 差 0.11**。② SLOW_AND_FAST+decay13 把 S 抬到 1.20（+0.06）但 robust/2Y 双崩（0.33/0.43）——**SUBINDUSTRY+decay4 是本机制唯一正确设置，设置轴正式穷尽**（此前 SLOW_AND_FAST 对照 0.49 的教训第三次确认：本机制的申报密度慢信息被 S&F 剥离）。③ Mode B 判定 `dead_end`（三项同弱，旁路不救）。④ **insiders1 第三轮归档**：天花板 1.14、独立信息源（与 agg_matrix 互相关 0.14-0.17）、全部已测轴见 §5.6/5.7。**复核触发条件：战役级新杠杆发明，或 agg_matrix 席位提交后的相关性反馈。**

### 5.8 最终封档（2026-11-08）——decay0 确认无效,全轴彻底穷尽

decay0（`78Lm796x`）与 decay4 读数逐位相同（1.13/1.14）——decay 轴第四档确认,设置轴（SUBINDUSTRY/SLOW_AND_FAST × decay 0/4/13/20）全部穷尽。**insiders1 最终天花板 1.14（`vR1poWNz`）,Mode B dead_end 三项同弱（S−0.11/F−0.12/2Y−0.49）。相关性端点已测（prod 0.6052/self 0.340 双 PASS）——一旦未来推过 S 1.25 即成第二席,档案保留,不再投入。**
