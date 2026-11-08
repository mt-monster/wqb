# EUR ATOM 挖掘战役 · 中期报告（2026-11-07）

> SOP：/wq-brain-ra-eur · 区域固定 EUR/TOPCS1600/D1 · 目标 10 个 ATOM regular alpha
> 本报告为里程碑快照；字段画像存档见各 `tracking/EUR/reference/datasets/<dataset>.md`

## 一、当前席位（Mode B eligible，机制互相关 ≤0.03）

| 席位 | alpha id | 数据集 / 塔 | 表达式核心 | S | F | 2Y | sub | Mode B | 剩余 RA 缺口 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **`leA5JeP7`** | insider_agg_matrix / **INSIDERS ×1.1** | `rank(group_scale(tail(winsorize(group_zscore(ts_sum(top_significant_value_2, 88), industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))` @ SLOW_AND_FAST | **1.76** | **0.94** | **2.32** | **1.07** | **main_gate** | 仅 LOW_FITNESS 0.94（warning 级） |
| 2 | **`ZYQdErnd`** | news18 / **NEWS ×1.3** | `rank(group_scale(ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws18_multiple_comp_sse), vec_avg(nws18_multiple_comp_relevance)), 66), 252), densify(market)), target_tvr=0.05), sector))` @ SLOW_AND_FAST | **1.68** | 0.76 | **1.81** | **0.90** | bypass_E（2Y≥1.2∧S≥0.8） | 仅 LOW_FITNESS 0.76（warning 级） |

- 两席互相关 **0.023**（`compute_mutual_correlation` 实测），机制正交、塔位不同
- 备用：`N1NJRNWL`（席 2 无包装栈版，S 1.73/F 0.81，与 ZYQdErnd 互相关 0.989 二选一）；`QPvNeeqK`（席 1 的 `_1` 版，互相关 0.997）
- 提交链未启动：`submit_verdict`/prod/self 相关性检查需用户显式确认后才执行

## 二、机制地图（本战役产出）

### 机制 1：内部人买入强度（INSIDERS 塔）
- **核心字段**：`top_significant_value_1/_2`（高管前二大显著交易金额）S 1.75/1.76；`total_top_buy_shares`/`total_secondary_top_buy_shares` 1.51/1.52
- **字段梯度规律**：_1/_2 正向（conviction 集中）、_3/_4 反向（routine 分散）——CMP(2012) 字段级证据
- **关键杠杆**：`group_zscore` 替换 `group_rank`（+0.10-0.13 S，信息保真度）；88d 窗口（季度+申报滞后）；SLOW_AND_FAST；`rank(group_scale(·,industry))` 包装栈
- **已证伪**：cap 掩码（×2）、signed_power、sector 分组（强度族）、ts_decay_linear 累加器、ts_zscore 自身基线、时序形态、TOP2500（sub 反噬）、RAM/CROWDING 中性化
- **F 结构性天花板**：returns ~0.035 → F=1.0 需 S≈1.9，S 峰 1.76

### 机制 2：新闻注意力密度反转（NEWS 塔）
- **来源**：论坛帖 `43541109631895`（PW58059，Da et al. 2011 → 事件密度迁移，GBR 1.97/EUR 1.60）
- **核心字段**：`nws18_multiple_comp_sse`（多实体情绪，`vec_count` 密度）× `nws18_multiple_comp_relevance`（相关性加权）
- **关键参数**：平滑窗 **66**（EUR 实测峰，60/44/88 更差）；分位窗 252；`densify(market)` 中性化；`ts_target_tvr_decay(target_tvr=0.05)`；宇宙 **TOP2500**（TOPCS1600 上归零）；SLOW_AND_FAST 修 2Y（1.21→1.81）
- **反常识发现**：`vec_count` 只有在「一天多条独立事件」的 Ravenpack 字段上才有效——NLP/DL 集的标题字段 `vec_count` 退化为 0/1，模板失效

## 三、数据集覆盖台账（本战役 15 集）

| 数据集 | 状态 | 最好 \|S\| | 归档原因 |
|---|---|---|---|
| insider_agg_matrix | **席位 1** | 1.76 | 34 字段全测，杠杆穷尽 |
| news18 | **席位 2** | 1.73 | 密度模板族 + 姊妹字段/nip 模板已测 |
| insiders1 | 归档 | 0.97 | 机制 B/C 0.93-0.97，杠杆全试尽（universe 三档单调劣化、SLOW_AND_FAST 反向、group_scale 无效、方向拆分结构性无效） |
| insiders12 | 跳过 | — | cov 0.193 < 0.35（历史判死维持） |
| news_sentiment_dl | 归档 | 0.91 | 反向天花板 0.91 + sub/robust 结构性 FAIL；14 探针 |
| news_sentiment_nlp | 归档 | 0.19 | 全噪声 |
| news54 | 跳过 | — | 时间戳/自由文本，FASTEXPR 不可用 |
| institutions6 | 归档 | 0.95 | 8 探针（截面+密度+净买入），2Y 结构性低 |
| fund_holdings_panel | 归档 | 0.48 | 5 探针快判死 |
| behavioral_signals | 归档 | 0.87 | 9 探针；EUR 无彩票反转，正向动量 0.74-0.87 不足 |
| search_interest | 归档 | 0.87 | 4 探针；正向动量形态，机制与席位 2 不同源 |
| stock_search_trends | 跳过 | — | 语义错位（USA 搜索量×EUR 股票）+ 与席位 2 重叠 |
| event_relation | 平台报错 | — | 4/4 ERROR（网络边数据集，平台层故障） |
| news36 | 探针在跑 | — | novelty/phrase 族，结果待回填 |
| other571（Wikipedia） | 未开 | — | 排队中 |

## 四、可复用结论（跨战役）

1. **`group_zscore` > `group_rank`**（对幅度有信息的字段）：+0.10-0.13 S，信息保真度而非数值路径差异
2. **`vec_count` 只吃 Ravenpack 式多事件字段**；日更连续面板和标题级 NLP 字段上退化为 0/1
3. **MATRIX 预聚合字段吃宽宇宙（TOP2500 +0.16 S），稀疏事件字段被宽宇宙稀释（insiders1 −0.66）**——宇宙杠杆必须按数据集实测
4. **稀疏流量字段唯一正确累加器是 `ts_sum`**（`ts_decay_linear` 会把 0 值纳入加权 → TO 爆炸）
5. **SLOW_AND_FAST 在 EUR 是 insiders/news 密度机制的关键档**（修 sub/robust/2Y），但对仓位比例机制（insiders1）有害——杠杆效应是（数据集×机制）级事实
6. **F 闸闭式拆解**：`F=S×sqrt(returns/0.125)`（TO<0.125 时）——低 returns 族的 F=1.0 需 S≈1.9+，比表面闸线难得多
7. **sub 比率闸（0.52×S）下「先修结构后加强度」**：sub 余量大的基底才允许上抬 S 的杠杆

## 五、下一步

1. news36 novelty/phrase 探针结果回填（在跑）
2. other571 / 其余 other ×1.5 低竞争集续扫
3. 两席位候选交用户确认后走 prod/self 相关性与提交流程

## 六、用户锁定令后的 insiders 收束（2026-11-07 更新）

用户指令：**锁定 insiders 不轻易切换**。锁定令后的增量实测：

| 批次 | 结果 |
|---|---|
| 方向符号显著金额族 4 臂（`imZTFf4t4qP9J7jl9vi2ag`） | 4/4 平台级 FAIL——8 支方向字段 EUR 数据层损坏，按不可用计入覆盖 |
| insiders1 新杠杆回灌 9 臂 | 天花板 0.97→**1.14**（44d 栈 `vR1poWNz`），仍差主闸 0.11/2Y 0.71；第二轮归档 |
| insider_agg_matrix 卖方直接交易 4 臂（`e3ta1gTk5an8PSA4eClzEf`） | 反向 sub/robust 0.96/0.93 全战役最优结构，但 **2Y≈0.04-0.15（近两年枯竭）**，归档 |
| insider_agg_matrix 34 字段覆盖闸 | **100%**（含平台级不可用字段） |

**insiders 类别终态**：席位 1（`leA5JeP7`）+ 完整机制地图（买方层级/窗口粒度/卖方枯竭/方向族数据损坏四大结论）。类别内剩余增量接近穷尽；复核触发条件 = 新杠杆发明或席位提交后的 self/prod 反馈。

**insiders1 第三轮收束（2026-11-07 晚）**：幅度轴四臂（quantile/std3/std4/power1.5）全落 1.11–1.14 平台——天花板 1.14 钉死；S&F+decay13 抬 S 到 1.20 但 robust/2Y 双崩（设置轴穷尽，SUBINDUSTRY+decay4 唯一正确）。Mode B 判定 `dead_end`（S 1.14/F 0.68/2Y 0.71 三项同弱）。**insiders1 独立席位不可行，但其与 agg_matrix 互相关仅 0.14–0.17 的独立信息源价值保留**——过闸条件明确（S +0.11 / F +0.12 / 2Y +0.49），等新杠杆。

## 七、锁定令第二阶段（2026-11-07 深夜）：agg_matrix 补测收束

- top_* 族 zscore 栈全面复现席位 1（S 1.74–1.76）
- **country 分组轴首测**：F 0.87/2Y 2.40/robust 0.96（`mLo0E6A2`），但与 industry 版互相关 0.97–0.997——单席位确认
- 44d 窗口对 top_* 更差（1.29）——「粒度决定窗口」假说修正为「厂商预聚合=88d、逐笔明细=44d」
- 非高管切片（0.82）/月度聚合（1.25）无增量
- **insider_agg_matrix 全轴穷尽，席位池 6 条（leA5JeP7/mLo0E6A2/LLMmvgr9/2rAX3q2w/9qxdNWKd/QPvNeeqK）互相关 0.97+**

## 八、论坛交叉验证与协同读数（2026-11-07 深夜，第三阶段）

- 论坛帖 `43467688159511`（WL27618，29 赞）与 `43615381230875`（AM12075，31 赞）与本战役四大结论互证：买强卖弱、高管层级、显著成交>笔数、比例机制。
- 论坛提示的「多人协同」维度实测：`add(top_1, top_2)` 与 `_2` 单字段逐位同级（合成无增量但语义更强，`QPvz1Q1r` 入池）；`+_3` 被反向字段污染（0.75）。
- **席位池最终 7 条**（leA5JeP7/QPvz1Q1r/mLo0E6A2/LLMmvgr9/2rAX3q2w/9qxdNWKd/QPvNeeqK），互相关 0.97+，单席位提交。
- insider_agg_matrix **16 节全维度穷尽**（覆盖闸 100%）；insiders1 三轮归档（天花板 1.14，独立信息源 0.14 保留）。
- **insiders 类别最终产出：1 个 Mode B main_gate 席位 + 7 条候选池 + 2 个数据集完整机制地图。**

## 九、冲刺第 3 席：insiders1 频次协同读数（2026-11-08）

forum `43615381230875` 提示「协同」与「比例」是两个未在 insiders1 用过的读数维度。insiders1 现有机制 B（valueeur/holdings 比例）与 44d 栈（`vR1poWNz`，S 1.14，dead_end）。**协同新读数**：`ts_sum` 窗口内的**申报次数**（vec_count）而非金额——「连续多笔申报」= 高管在多日持续加仓，与单笔大额（金额读数）是不同信号。三臂：
1. `vec_count` 次数密度 × 44d 栈（insiders1）
2. `vec_count` × 88d 栈
3. `ts_rank` 自身基线版（insiders1 未测过 count 形态）

**次数密度结果（multisim `Q7ieS3Es5fsbFK1eu9DSS04`）**：44d 0.82 / 88d 0.92 / 自身基线 −0.42——次数弱于金额（金额信息 > 频次信息），且 ts_rank 自身基线再次证伪。**insiders1 的「次数」读数关闭；机制读数空间（金额/比例/次数/协同）在本类别全部测尽。**

**insiders 类别最终格局（2026-11-08）**：
- 席位 1：`leA5JeP7`（main_gate）+ 6 条同族候选池
- insider_agg_matrix：16 节全维度穷尽
- insiders1：三轮归档，天花板 1.14，独立信息源保留
- 全类别读数形态（金额/比例/次数/协同/买卖/身份层级/窗口/分组/归一化/分布/设置）全部实测穷尽

## 十、★ 席位 1 全闸验证通过（2026-11-08）

| 闸 | 值 | 阈值 | 结果 |
|---|---|---|---|
| Mode B 主闸 | S 1.76 / F 0.94 | 1.25 / 0.8 | **PASS** |
| RA 检查 | 仅 LOW_FITNESS 0.94 | warning 级 | PASS（无 hard fail） |
| **self 相关性** | **0.328**（最高 RRAvGrn0） | <0.7 | **PASS** |
| **prod 相关性** | **0.6498**（直方图 0.6-0.7 仅 2 颗） | <0.7 | **PASS** |

**`leA5JeP7` 成为全战役第一颗全闸可提交的 ATOM alpha**（Mode B main_gate + self + prod 三闸全过，唯一缺口是 RA warning 级 LOW_FITNESS 0.94 与正式提交需用户确认）。prod 直方图健康：主质量在 ±0.1 区间，尾部无密墙。

表达式：`rank(group_scale(tail(winsorize(group_zscore(ts_sum(top_significant_value_2, 88), industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))` @ EUR/TOPCS1600/D1/SLOW_AND_FAST/decay4/trunc0.08

**提交待用户显式确认**（项目纪律）。

**第二颗候选 `mLo0E6A2` 双端点同样全过**（prod 0.6478 / self 0.336）——⚠ 但它与席位 1 互相关 0.975：**提交其一后另一颗 self 必爆（0.97>0.7），两颗只能提一颗**。提交顺序决策：席位 1（`leA5JeP7`）F 0.94 > `mLo0E6A2` F 0.87，默认提前者；若前者 prod 反馈异常再换。

**`vR1poWNz`（insiders1 44d）双端点 PASS**（prod 0.6052/self 0.340，直方图最干净）——但 Mode B 主闸 dead_end（S 1.14），**相关性过关≠可提交**。它是「相关性健康、资格不足」的典型：一旦未来任何杠杆把它推过 S 1.25，即成第 2 席（与席位 1 互相关仅 0.17）。

## 十一、insiders 类别最终收官（2026-11-08）

- decay0 确认与 decay4 逐位相同——insiders1 设置轴（2 中性化 × 4 decay）穷尽,天花板 **1.14** 钉死,`dead_end` 维持。
- **insiders 类别产出**：1 颗全闸可提交（`leA5JeP7`）+ 6 条同族候选池（互相关 0.97+，仅一席可提）+ insiders1 独立信息源档案（相关性健康、差 0.11 过主闸）+ 2 个数据集完整机制地图。
- **类别内已无可挖掘增量**。10-alpha 目标的路径：① 用户确认提交 `leA5JeP7`；② 解锁后按 SOP 重扫新类别（优先 other ×1.5 / news ×1.3 低竞争集——本战役已在 news_sentiment_dl/nlp/news18 上有初步地图）。

## 十二、news18 席位 prod 卡墙（2026-11-08）

`ZYQdErnd`：self 0.102 干净，**prod 0.7239 FAIL**（0.7-0.8 桶 n=1，max 单颗钉子）——按 `wq-prod-corr-read` 的族级判据：n=1 可救。窗口微调是首选杠杆（`wq-window-valley-break-prod-wall`：ts_rank 的 W 已是 252，可试 126/504/三档密度窗），或换字段（ssc/qcm 变体）。**该席位未死，转入窗口谷扫描。**

## 十三、★ 席位 2 全闸通过——窗口谷破 prod 墙（2026-11-08）

`ZYQdErnd` prod 0.7239 卡墙（n=1 单颗钉子）→ 按窗口谷方法论扫 `ts_rank` 分位窗 126/504：

| 变体 | alpha id | S | F | 2Y | prod | self |
|---|---|---|---|---|---|---|
| 分位窗 126 | `pwdGmAYX` | 1.35 | 0.55 | 1.68 | — | — |
| **分位窗 504** | **`mLo7pMwx`** | **1.69** | 0.77 | 1.51 | **0.6366 PASS** | **0.090 PASS** |

**`mLo7pMwx` 全闸通过**：Mode B bypass_E + prod 0.6366 + self 0.090（本战役最干净的 self）。252→504 一格挪走钉子，S 反而 1.68→1.69。news18 密度机制正式成为**第 2 颗全闸可提交候选**（与席位 1 `leA5JeP7` 互相关 0.023——真正正交双席位）。

**战役可提交库存：2/10**（`leA5JeP7` INSIDERS + `mLo7pMwx` NEWS），均待用户确认提交。

## 十四、★ 席位 3 全闸通过——sse 单实体正交兄弟（2026-11-08）

席位 2（多实体 `multiple_comp_sse` 密度）的正交兄弟：**单实体 `nws18_sse` 密度**（互相关 0.810<0.9,不同事件源）。杠杆阶梯实测：decay20 降（1.48）→ tvr 0.06/0.07 抬 S 降 2Y 跷跷板 → **tvr=0.06 × 分位窗 252**（`akKzvXww`）S 1.68 PASS / 2Y 1.31 命中旁路 E。

| 闸 | 值 | 结果 |
|---|---|---|
| Mode B | S 1.68 / F 0.77 / 2Y 1.31 | **bypass_E PASS** |
| 与席位 1/2 互相关 | 0.016 / 0.810 | **<0.9 PASS** |
| self | 0.074 | **PASS** |
| prod | 0.6183 | **PASS** |

**可提交库存 3/10**：`leA5JeP7`（INSIDERS，main_gate）+ `mLo7pMwx`（NEWS 多实体，bypass_E）+ `akKzvXww`（NEWS 单实体，bypass_E）——三席互相关 0.016-0.810 全部 <0.9，同批提交合法。

**sse 族杠杆地图**：tvr 0.055→S 1.58 压线/0.06→1.60/0.07→1.61 但 2Y 递减（1.15/1.11/1.00）；分位窗 252 优于 504（2Y 1.31 vs 1.15）；country/sector 分组无差异；decay 15>20。

## 十五、★ 席位 4 全闸通过——bee 财报事件密度（2026-11-08）

`0mYgWNOq`：`rank(group_scale(ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws18_multiple_comp_bee), vec_avg(nws18_multiple_comp_relevance)), 66), 252), densify(market)), target_tvr=0.055), sector))` @ S&F/decay15/TOP2500

| 闸 | 值 | 结果 |
|---|---|---|
| Mode B | S 1.63 / F 0.72 / 2Y 1.22 | **bypass_E PASS** |
| 与席位 1/2/3 互相关 | −0.003 / 0.738 / 0.695 | **<0.9 PASS** |
| self | 0.085 | **PASS** |
| prod | 0.6475 | **PASS** |

**关键归因**：bee/bam/acb/qmb 四字段的 `vec_count` **逐位相同**（同一批多实体事件日期集合）——事件子类密度是同一信号，bee 为代表。其与席位 2/3（sse 新闻流）互相关仅 0.70-0.74：**「事件子类计数」与「情绪事件计数」是不同信号**。2Y 修复杠杆：tvr 0.06→0.055（1.17→1.22 过旁路线）；分位窗 504 反而崩（2Y 0.67）——与席位 2 相反，杠杆效应按字段实测。

**可提交库存 4/10**：`leA5JeP7`（INSIDERS）+ `mLo7pMwx`（NEWS 多实体 sse）+ `akKzvXww`（NEWS 单实体 sse）+ `0mYgWNOq`（NEWS bee 财报）。四席互相关矩阵全 <0.9。

## 十六、news18 内部正交源封顶（2026-11-08）——第 5 席必须出集

- `ghc_lna`（分析师评级变化）密度与 bee **逐位相同**（同一事件集）——事件子类计数收敛为席位 4 一个信号
- 新颖度读数（simildays/事件数）0.85 无信号
- **news18 独立信号源共 3 个**：sse 新闻流（席位 2 `mLo7pMwx` / 席位 3 `akKzvXww`——单/多实体互相关 0.81）+ 事件子类计数（席位 4 `0mYgWNOq`）——全部全闸通过
- **news18 内部正交空间封顶 3 席**；第 5 席转出至 `insider_feats`（other ×1.5，vS=6，论坛标注「全球成交特征」，与 agg_matrix 预聚合互补的特征大表，αC 58 低竞争）

## 十七、insider 机制级 prod 墙终判 + 第 5 席路线（2026-11-08）

**三个 insider 姊妹集同撞一个机制级墙**：

| 数据集 | 最优候选 | S/F/2Y | prod | 墙形态 |
|---|---|---|---|---|
| insider_feats | `LLMzOe3M`（比例直读）/`WjOzwnlO`（country） | 1.76-1.80/0.94-0.96/2.17-2.53 | 0.7955-0.8409 | 钉子随杠杆移动 |
| insider_trx_matrix | `VkxzdXZ0`（USD 金额） | 1.60/0.81/2.09 | **0.8248** | 0.8-0.9 n=1 |
| insider_agg_matrix | `leA5JeP7`（席位 1） | 1.76/0.94/2.32 | **0.6498 PASS** | 无墙 |

**归因**：prod 池已有一颗 insider 买方强度/比例类 OS alpha,与「insiders 类新读数」高相关。席位 1（agg_matrix 股数口径）恰好低于墙（0.65）,而 USD/比例/直读口径全部落进它的相关圈。**墙不是可绕的,是机制占位**——insider 域内新席位不再可能,除非该 OS alpha 退役。

**第 5 席路线修正**：跳出 insider 机制域 → news18 的剩余正交轴已封顶 3 席 → 下一优先级：`insider_feats`/`insider_trx_matrix` 归档备用,转向 **news_sentiment_dl 的 reverse(22d) 0.91**（已归档但 sub/robust 结构差）、或**全新低竞争集**（`other571`/`news36` 已死,候选：`model307`（vS=4,全球销售分配）、`model238`（SmartHoldings vS=4）、`other571` 已死）。**先测 news18 已全闸 3 席提交后的 prod 池变化**——4 颗全闸席位中 `leA5JeP7` 与 `mLo7pMwx`/`akKzvXww`/`0mYgWNOq` 同批提交会改变 prod 池,insider 墙可能因此松动。提交决策再次前置到用户。

## 十八、model238（SmartHoldings）爆发（2026-11-08,进行中）

- 首探针：`industry_rank_d1` **S 2.06 / F 1.51 / 2Y 2.30**、`region_screening_rank_d1` S 2.00/F 1.50——**全战役最强原始读数**（此前最高 1.80）
- 卡点：CONCENTRATED_WEIGHT + sub 0.52（闸 1.09）+ robust 0.53——模型分集中持仓
- 修复批在飞：zscore 栈 / winsorize std4 / group_neutralize；**用户提示 group_backfill 解 CW**（模型分 NaN 缺口集中 → 组内回填分散持仓）,已加发 3 臂

## 十九、model238 终判（2026-11-08）

- `group_backfill`（用户提示）成功破 CW：S 2.06→2.12，CW FAIL→PASS
- quantile(gaussian) 再抬 S 到 2.16/F 1.61/2Y 2.35——但 sub 0.59/robust 0.59 结构性卡死
- 窄宇宙验证（TOP800 S=0.34/TOP1200 S=0.72）证明信号在 TOPCS1600 中尾部——sub/robust 宇宙不含该段
- **model238 归档**：「半全绿」S 2.16 候选（`wpQGoApQ`），sub/robust 结构性不可修
- 可复用结论：① group_backfill 解 CW（NaN 集中持仓型）；② 模型分/合成因子一律 FAST 档（S&F 剥掉慢轴= 0.7x 崩盘）

## 二十、战局快照（2026-11-08 中段）

**已全闸 4/10**：`leA5JeP7`（insider_agg_matrix, INSIDERS ×1.1, S 1.76）｜`mLo7pMwx`（news18, NEWS ×1.3, S 1.69）｜`akKzvXww`（news18, NEWS ×1.3, S 1.68）｜`0mYgWNOq`（news18, NEWS ×1.3, S 1.63）——全部互相关 <0.9，prod/self 双 PASS，待用户确认提交。

**已归档**：insider_feats（prod 墙 0.80-0.84）、insider_trx_matrix（prod 墙 0.82）、insiders1（S 1.14 主闸差 0.11）、model238（sub/robust 结构性）、model68/other545/price_signal_dl/acquisition_model/behavioral_signals/search_interest/other571/news36/news_sentiment_dl/news_sentiment_nlp/insiders12（覆盖不足跳过）/fund_holdings_panel/institutions6/insider_feats 卖方直接交易族（2Y 枯竭）。

**prod 机制墙发现**：insider 买方强度三集（agg_matrix 股数口径/insider_feats 比例口径/trx_matrix USD 口径）共享同一 prod 钉子圈 0.74-0.84——同机制不同读数撞同一颗已提交 OS alpha。**唯一例外是 `leA5JeP7` 的 0.6498**——SLOW_AND_FAST 中性化（其他三集都是 FAST/SUBINDUSTRY 档）把持仓结构挪出了钉子圈。

**剩余正交源**：news18 三席已封顶。第 5 席候选方向：insider_feats 的 SLOW_AND_FAST 档从未测过（首探针即 SUBINDUSTRY 档 S 1.39; 直读形态下 S&F 是唯一未动的中性化轴）——**若 S&F 把 insider_feats 也挪出钉子圈，即复现 leA5JeP7 的成功路径**。立刻测试。

## 二十一、insider_feats S&F 档复测（2026-11-08）——prod 钉子不随中性化移动

S&F 档重跑与 SUBINDUSTRY 档读数逐位相同（`LLMzOe3M` 1.76/`WjOzwnlO` 1.80，回读同一 alpha ID）——**首次提交已是 S&F**（我记忆错位，当时该批就是 S&F）。prod 复测 `WjOzwnlO` 仍 0.8409 卡墙。**机制墙确认不可绕**（同一持仓不管什么中性化都撞那颗 OS alpha）。

**结论**：insider_feats 与 insider_trx_matrix 的 prod 墙在提交 4 席之前无法突破。**第 5 席唯一可行路径 = 先提交 4 席**（含 `leA5JeP7` INSIDERS 席），等 prod 池变化后 insider_feats 0.80-0.84 的墙可能松动（直方图尾 0.8-0.9 n=1，若该钉子是自己的则提交后消失）。

## 二十二、全数据集终局快照（2026-11-08 深夜）

**可提交 4/10（全闸）**：`leA5JeP7`｜`mLo7pMwx`｜`akKzvXww`｜`0mYgWNOq`（详见 §十至十五）——待用户确认提交。

**半全绿 2（S 2.0+ 但 sub/robust 或 prod 结构性卡）**：
- `wpQGoApQ`（model238, S 2.16/F 1.61）——sub/robust 信号位置结构性
- `WjOzwnlO`（insider_feats, S 1.80/F 0.96）——prod 机制墙 0.84

**其余正交源已尽**：news18 封顶 3 席、insiders1 封顶 1.14、卖方族 2Y 全族枯竭（数据层变化）、model238 sub/robust 结构性、其他 13 集归档。

**战役结论**：EUR ATOM 全景扫描后,可提交席位在 insider_agg_matrix（1）+ news18（3）共 4 席全部找到并验证。第 5 席起被三类结构性约束锁死（prod 机制墙/sub-robust 信号位置/卖方 2Y 枯竭）,解锁条件均为**先提交现有 4 席**（prod 池与 self 池变化后再回来挖）。提交决策权在用户。

## 二十三、扫尾与终局（2026-11-08）

- institutions6 @ CROWDING：死（GLB 论坛结论不迁移，−0.05/0.05）——中性化档第 5 次验证「杠杆效应是数据集×机制级事实」
- news18 事件子类密度家族（ssc/qep/bee/ghc_lna/acb/bam/qcm）全部逐位相同——同一事件集，收敛为席位 4 一个信号
- news20（Web Sources 源）密度 1.14/0.51——源稀薄，不构成席位
- 剩余未触碰类（socialmedia/sentiment/earnings/macro/imbalance）全部为 aC>331 拥挤或 cov<0.35 或 vS≤2——先验不足，不做无意义扫描
- **终局：4/10 全闸 + 2 颗半全绿（model238 S 2.16 sub/robust 结构性、insider_feats S 1.80 prod 墙）**

## 二十四、交付清单定稿（2026-11-08）

交付文档：`tracking/EUR/reports/deliverable_atom_2026-11.md`（A 全闸 4 颗含完整表达式与逻辑 / B 半全绿 2 颗 / C 22 集终局地图 / D 11 条战役级结论 / E 提交建议）

## 二十五、验收标准修正（2026-11-08,用户指令）——F ≥ 1.0 才算过闸

用户明确：**F 没有大于 1 不算过闸**（review.fitness_min 1.0 是真闸,此前误用 Mode B 台账闸 0.8 作及格线）。按新标准重算：
- 4 颗「全闸」候选 F 全部 <1.0（0.72–0.94）——**全部降级为「未过闸」**
- 唯一 F≥1.0 族 = model238（F 1.41–1.61）,但 sub/robust 结构性卡死
- F 杠杆 = 持仓集中度：tail(newval=0.5) 把中段压半仓稀释单位资金收益 → 收窄带宽（0.35/0.65）或末端再加集中 tail,推资金到两端
- 已提交 2 批 F-push：席位 1 族（带宽收窄 + 外层 tail）× 席位 2 族（外层 tail 0.3/0.7 与 0.25/0.75）
