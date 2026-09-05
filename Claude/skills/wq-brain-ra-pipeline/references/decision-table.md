# wq-brain-ra-pipeline 挖掘决策表（执行查表）

> 拿到阶段结果后**直接查表执行**；表中没有的分支才允许停下问用户。
> 优先级铁律：**用户显式指令 > 本决策表 > skill 正文**。用户指令与表中硬约束冲突时，直接执行用户指令并在台账记录覆盖原因，不请示。

## D0. 拿到回测结果后的主决策（S4 入口）

| 结果状态                                                                                                                                             | 动作                                                 | 输出         |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- | ---------- |
| 有 alpha 过廉价闸（Sharpe>1.58 / Fitness≥1.0 / TVR 5–20% / 无 FAIL；及用户阈值 margin>5bp、turnover 5–30%、risk\_neut S>1、F>0.7、margin>5bp、ra\_failed\_count=0） | 进 D1 验证链                                           | 验证报告       |
| 单数据集 alpha 过廉价闸但 Sharpe 在接近区（1.58–2.0）且白名单存在正交数据集                                                                                          | **主动**进 D3 混合提分（不等失败；MEA 区域优先组合）                     | 混合表达式      |
| 全部未过廉价闸                                                                                                                                          | 进 D2 证据复核分支                                        | 分支动作       |
| 过闸但 prod-corr>0.7                                                                                                                                | 判"撞 prod-corr 墙"→ 换白名单**不同数据集** regenerate（勿磨同腿变体） | 新 wave 表达式 |

## D1. 通过廉价闸后的验证链（全自动，逐 alpha 执行）

| 步骤 | 动作                                                       | 通过条件                                       |
| -- | -------------------------------------------------------- | ------------------------------------------ |
| 1  | test robust（不同 universe/neutralization 重跑）               | 各档稳健、无塌陷                                   |
| 2  | 过拟合测试（2y sharpe）                                         | LOW\_2Y strictly > 1.6                     |
| 3  | 相关性矩阵 `compute_mutual_correlation`（候选集内两两）               | 彼此 < 0.5                                   |
| 4  | 硬闸核查 `get_alpha_details` is.checks + 本地 self/PPAC        | PROD<0.7 / SELF<0.5 / LOW\_2Y>1.58 / CW 必过 |
| 5  | IS 检查通过后 `set_alpha_properties` 设属性                      | —                                          |
| 6  | 写入 submit\_ready 池（战役台账 mea\_d1\_campaign\_state.json 等） | —                                          |

注：`submit_alpha` 返回 201 + success:false 是工具 bug，不算失败；以 OS pool ACTIVE 为准。

## D2. 未过闸 → 证据复核分支（增强模式决策闸）

| 信号状态                                            | 动作                       | 前置条件                                             |
| ----------------------------------------------- | ------------------------ | ------------------------------------------------ |
| 单一簇、局部不稳定                                       | single 增强                | —                                                |
| 两个+ 互补赢家                                        | cross 增强                 | metadata（region/universe/delay/neutralization）一致 |
| sharpe 0.8–1.5、至少一维过闸（tv/2y/fit）、同数据集变体耗尽（3+ 次） | mix amplify（跨数据集混合）      | 白名单存在正交经济维度互补数据集                                 |
| sharpe < 0.8                                    | 放弃该数据集，换白名单下一个           | —                                                |
| 撞 prod-corr 墙                                   | 换白名单**不同数据集** regenerate | 勿磨同腿变体                                           |
| CW 失败                                           | backfill + 线性混合增强        | 不要 `rank(add(...))` 结构                           |

## D3. 混合（mix amplify）构造规则

| 场景            | 规则                                                                         |
| ------------- | -------------------------------------------------------------------------- |
| **定位**        | 混合是**主动提分手段**（非必要条件）：单数据集信号 sharpe 1.0–2.0 且白名单有正交数据集 → 直接混合冲更高 sharpe；不仅作失败后的退路 |
| 主动触发          | 单数据集 alpha 过廉价闸但 Sharpe 接近区（1.58–2.0）→ 主动混合；MEA 区域已提交 alpha 倾向跨数据集，优先组合 |
| 补救触发          | sharpe 0.8–1.5、至少一维过闸、同数据集变体耗尽（3+ 次）→ 混合 |
| 基础信号维度补全      | 情绪/动量 → 补基本面（EPS revision、估值）或微观结构；技术评级 → 补空头兴趣、机构持仓、分析师修正；微观结构 → 补情绪、基本面  |
| 加法优先          | 跨金字塔用 win 配比 `add(0.40*慢MODEL, 0.60*快PV)`（`MINING.slow_fast_mix`）；同金字塔才用等权 `add(rank(A), rank(B))` |
| 乘法仅限          | 两个基础信号都强（>1.0）才用 `multiply(rank(A), rank(B))`（margin 脆）                    |
| 数据集数          | 2–5 个（>5 边际收益 < 复杂度成本）                                                     |
| 中性化           | 混合信号必须 `group_zscore(..., industry/subindustry)` 包裹                        |
| **margin 铁律** | margin 是数据集属性，混合**不能**修 margin；margin 不足 → 换数据集而非混合                        |

## D4. 健康检查（S0，generate 前必做）

| 条件                                             | 动作                                                                          |
| ---------------------------------------------- | --------------------------------------------------------------------------- |
| 已有战役目录 tracking/<REGION>/                      | `score_datasets.py --campaign-dir tracking/<REGION>`（权威，v3.1 分位 tier）       |
| 无战役目录（跨区试探）                                    | `dataset_health_check.py --region R --delay D --universe U`（固定阈值，仅试探）       |
| generate 白名单                                   | tier1 + `tier_note=pyramid_quota` 上提的非 MODEL（配额后仍无非 MODEL 不得退回纯 MODEL 七槽） |
| 白名单排序                                          | 先按金字塔配给（每波 ≥2 槽非 MODEL），再 score desc；**禁止** pyramidMultiplier desc 把 PV 整座挤出 |
| 硬地板                                            | cov<0.65 或 usableFields<5 → excluded（mode 无关）                               |
| 回填带（cov 0.65–0.85 & ac≤50 & valueScore≥6）      | tier2 保底，生成必须 `ts_backfill(66/120)` 包裹                                      |
| 探针例外（cov≥0.9 & ac=0 & valueScore≥6 & fields<5） | tier2，仅 Stage-A 探针 1 批早停                                                    |
| **用户指定数据集与白名单冲突**                              | **用户指令优先**，执行并台账记录覆盖原因                                                      |
| 本地 MCP 127.0.0.1:8876 宕机                       | 健康检查回退 `--mode direct`，不重试烧 turn                                            |
| 本 NY 日已验证 max\|Sharpe\|<0.5 的数据集               | 跳过，不 re-GEM/re-enhance                                                      |
| 当前 Power Pool 主题不匹配 region/delay/universe      | 只挖 Regular                                                                  |
| 白名单空                                           | 换区域/universe，不 generate                                                     |

## D5. 设置规则（S2' 展开，勿硬编码 SUBINDUSTRY）

| 场景         | 值                                                                                                                     |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| 中性化        | **有 win 则跟 win**（EUR 实证 SUBINDUSTRY/decay4）。无 win 才用区域默认。对照轨可探 COUNTRY / ILLIQUID_MINVOL1M / delay0，但不能把未验证档写成主轨 |
| 禁用         | SECTOR/MARKET 压垮 IS\_LADDER\_SHARPE（按区域经验判断）                                                                          |
| decay      | returns 信号 4 / close 6                                                                                                |
| truncation | 0.08                                                                                                                  |
| delay      | 数据存在时 0，否则 1（MEA 仅 D1）                                                                                                |
| universe   | 区域合法档（MEA TOP300/400；KOR TOP600；EUR TOP2500/1200/800；HKG TOP500/800；IND TOP500；GBR TOP700；USA TOP3000…）；非法 → HTTP 500 |
| EVENT 字段   | 禁 winsorize → `ts_event_*` 或裸 rank                                                                                    |
| VECTOR 字段  | 必须先 `vec_*` 聚合再进常规算子                                                                                                  |
| 低 coverage | `ts_backfill(66/120)` 包裹                                                                                              |
| 有界字段       | 跳过 winsorize                                                                                                          |
| 整数型        | 用 rank/bucket，不要 ts\_mean                                                                                             |
| max\_trade | ON（用户要求时）                                                                                                             |

## D6. 信号笔记（S2 生成/enhance 输入约束）

| 规则                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 优先 `returns` 反转而非 `close`；IS\_LADDER\_SHARPE 必须 strictly > 1.58                                                                                              |
| `hump` 已废弃禁用；`divide` 无 filter 参数；`ts_regression(A,B,n).residual` 非法                                                                                         |
| `subtract(..., filter=true)` 可用                                                                                                                              |
| CONCENTRATED\_WEIGHT：避免 `rank(add(...))`，用线性混合 `add(multiply(rank(ts_delta(ts_backfill(F,66),66)),0.5), multiply(rank(ts_delta(ts_backfill(F,66),22)),0.5))` |
| 字段名**逐一经 get\_datafields 验证**再入批（虚构字段名 = 整批 CANCELLED 连坐）                                                                                                    |

## D7. S2-D 多样性榨取决策

| 条件                                 | 动作                                                                                  |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| 选定目标数据集后、生成表达式前                    | **可选**跑 `diversity_extract.py --campaign-dir <CD> --dataset <ds> --rounds 3 --size 8`（方向参考，不替代 GEM 概念优先） |
| 总表达式 ≥15 且低 PPAC 比例 ≥0.7 且新颖度 ≥0.8 | enter\_multi\_dataset（进入多数据集阶段须过 gate 白名单；跨集乱混失败则退回**单数据集内组合**，不停挖） |
| 总表达式 ≥10 且低 PPAC 比例 ≥0.6           | continue\_extraction（再榨 1–2 轮）                                                      |
| 总表达式 <5                            | adjust\_strategy（改生成策略或换数据集）                                                        |

## D8. S3 七槽填槽模式（批量回测执行标准）

| 步骤       | 动作                                                                                                             |
| -------- | -------------------------------------------------------------------------------------------------------------- |
| 0 台账同步门  | 提交新波前先 `check_ledger_sync.py` 校验台账一致性                                                                          |
| 1 提交前门禁  | 每批表达式先过 `gate.py` 5 闸（语法/字段白名单/VECTOR vec\_\* 包裹/ts\_min,ts\_max 不可访问/quantile 仅 1 参/banned+poison 正则+sha1 缓存） |
| 2 批同提    | `create_multi_simulation` 每轮同时提交 7 批。每槽先 1–2 条骨架（prod-first）；prod<0.7 才扩到 8。填槽：≥2 跨金字塔、≥1 win 换腿、弱探针≤1。禁止七槽纯 MODEL / 七槽裸探针 |
| 3 统一轮询   | `lookINTO_SimError_message` 批量查 multisim 状态                                                                    |
| 4 写波结论   | 回收筛选后立即追加 WAVE\_LEDGER.md + ledger.json                                                                        |
| 4b 结果双写  | 回测指标入 `backtest_results` 表（pipeline stage\_review 自动调 `save_backtest_results`；结构化查询用库，原始响应保留 JSON 排障，CSV status 文件废弃） |
| 5 即收即补   | 任一批 COMPLETE 立即回收筛选，空槽当轮补**组合批**（不要空等、不要拿弱探针凑数）；S0 弱探针仅当本波尚无 `|Sharpe|` 近闸字段时最多占 1 槽 |
| 6 台账驱动选波 | 下一波批次设计前先读 WAVE\_LEDGER.md 最新「下一波决策」节                                                                          |

## D9. 提交与停止闸（S5）

| 条件                                             | 动作                                               |
| ---------------------------------------------- | ------------------------------------------------ |
| Regular Alpha：OS ACTIVE ≥10（用户目标 N 时按 N） | **停**，可转 SuperAlpha |
| PPA 日循环：submit-ready ≥ 4（ET 日历日 REGULAR 4/日配额保守占用） | **停** |
| 配额有槽（REGULAR\_SUBMISSION remaining>0）且**用户确认** | POST submit（worldquant-submit-alpha）             |
| `submit_alpha` 201 + success:false             | 不算失败，查 OS pool ACTIVE                            |
| 同数据集同腿兄弟                                       | 相关性 0.82–1.0，提交前 `compute_mutual_correlation` 核查 |
| PPA 提交                                         | 仅当 get\_messages 主题匹配且用户确认                       |

## D10. 迭代纪律与陷阱自查

| 纪律/陷阱                                                          |
| -------------------------------------------------------------- |
| 每次迭代最多改 1–2 个变量                                                |
| 持久化 artifact 与 verdict 到 state；无进展连胜 → 换白名单数据集 regenerate      |
| 每 15 轮回测做一次多样性评估（算子/字段探索率、模板骨架/风格多样性、预处理、收益归因、失效风险），据此优化生成方向   |
| 不要手写 HTTP，用 MCP create\_multi\_simulation                      |
| 本地在飞数 = min(工作线程, C)，C 为服务端并发上限（实测约 5–7）；TaskStop 会留孤儿占槽 → 429 |
| 批内一个坏字段/坏算子 → 整批 CANCELLED 连坐（提交前逐字段验证）                        |
| 不创建自动化任务（用户未要求时）                                               |

## D11. 批次策略选择：探针批 vs 复杂经济学模板（KOR wave96–104 实证，2026-08）

> 背景：KOR wave96–103 连续 8 波单字段探针（`rank(x)`/`ts_zscore` 水平值）全灭（6 数据集 64 条探针 0 达标）；
> 唯一出 RA 的路径是 wave91c 复杂跨数据集混合模板（慢变量×短周期快变量加权混合 → 2 RA ACTIVE）。
> wave104 站在已验证配方上做复杂模板扩展，首批即命中 2 条过全部廉价闸+IS 硬闸。

| 场景 | 动作 |
| --- | --- |
| 区域已有 `|Sharpe|≥1.0` 或过廉价闸的字段/骨架（腿禁用 ≠ 整集判死） | **先做同数据集组合批填满空槽**；禁止把槽位散到新数据集裸探针或复合后仍 `|S|<0.5` 的弱集。弱探针仅当本波尚无近闸字段时最多 1 槽（见 `wq-brain-ra-pipeline` 步 4/步 6） |
| 区域 registry 已有 win 配方（`registry_empirical` layer=win） | **70% 精力做配方家族扩展**（复杂经济学模板），不继续探针新数据集；先拉 ACTIVE alpha 的表达式+settings 作基线 |
| 完全空白数据集（无 win 无历史） | 探针批仅限 1 批 8 条早停；三灯判定后要么判死要么转复杂模板，**不做第二轮探针** |
| 探针连续 2–3 波全灭 | 停探针，回查台账 wins 层找配方；无 win 则换区域或查论坛模板 |
| 配方家族扩展设计（换腿/加腿/门控） | **设计前先估算与母配方的相关性**：主导腿（占权重 ≥2/3 的字段）不变 → SELF 相关必然 ≥0.9，结构性死路，不做 |
| 真正差异化扩展 | 必须换主导信号源（换慢腿族 + 换快腿族同换）；单换一条腿 = 母配方的高相关变体（KOR 实证：B3/B4 sh 1.80/1.82 达标但与 88lr21xo SELF 0.93/0.98 → 双判死） |
| 同族扩展判死回写 | dead_end rule 写明“家族扩展天花板”，salvage 记录 NEAR 候选（如 A4 confidence 1.34）备 Mode A 参数收敛 |
| 复杂模板的经济学骨架（已验证有效模式） | ①慢变量×快变量加权混合（2:1 / 1:3）②`ts_corr(慢,快,20)` 共振腿（因子协同确认）③`if_else(rank(快)>0.5, ...)` 动量门控 ④`group_zscore(慢, sector)` 行业相对强度 |

## D12. 镜像方向探针（强负信号 = 方向写反，不是无信号；EUR wave3b + KOR wave34A 实证，2026-08）

| 场景 | 动作 |
| --- | --- |
| 探针批出现强负信号（sh ≤ -1.0 或 2y ≤ -1.0） | **不判死**；下一批对该字段族做镜像反转探针 `subtract(0, rank(x))` / `multiply(-1, ...)`（EUR multi_horizon_alpha fcf_to_price sh -1.9 → 镜像 1.91 实证） |
| 镜像探针过廉价闸 | 按 D1 验证链走；镜像骨架登记台账，后续波次默认双向（原始+镜像）入批 |
| 慢变量（修正/评分类）差分激活全转负 | 慢信号水平值有效、差分可能反向（KOR wave99/100 双实证）——差分转负时回水平值 + 考虑镜像差分 |
| 全批所有方向（含镜像）均 \|sh\| < 0.6 | 才允许判死回写 |

## D13. S1 结构性前置体检（仿真配额前拦截结构性死路；MEA/KOR 多区实证，2026-08）

| 检查项 | 阈值/动作 |
| --- | --- |
| 小宇宙（TOP400/TOP500）VECTOR 字段 | 挖前必查 longCount≥80（cov 0.85 但 longCount 11-16 = 伪白空间，MEA f72 实证） |
| 低 alphaCount 白空间判定 | 小宇宙中 alphaCount≤50 可能是"没人能用"而非"没人挖过"——交叉验证 userCount/longCount |
| 稀疏事件流字段（论坛评论/行为/事件计数） | 预期 CW 1.0 结构性无解（KOR 三族实证）——先单仿真探针看 CW 再投整批；勿期望 backfill 救活 |
| 新数据集首批 | 先 1 条单仿真探针验证字段可用性（元数据类型可能标错：MEA fundamental6 标 VECTOR 实为 EVENT → 整批 ERROR） |
| 字段批内连坐预防 | 不确定字段隔离到独立小批；一个坏字段会 CANCEL 整批 8 条（实证） |
| 慢变量族差分设计 | 见 D12：差分激活对慢变量可能反向，设计时水平值与差分分开批验证 |

## D14. PROD 墙路由（撞墙后的三条破墙路径，按优先级；EUR/MEA/KOR 实证，2026-08）

| 优先级 | 路径 | 适用条件 |
| --- | --- | --- |
| 1 | **结构性去相关**：删腿/换广度轴（如 revision 腿 → raised-breadth 双轴，MEA 9qXoJge2 0.716→0.6525 实证） | 候选与自家已提交族高相关，且存在可替换的经济等价维度 |
| 2 | **镜像稀释**：加一条与主腿相关≈0 的稀释腿（EUR Wj71Q12o prod 0.9013→0.6847、IS 反升；SOP 见 `docs/experience/prod_wall_breakthrough_sop.md`） | IS 全过但 prod 0.8-0.95；先用 `compute_mutual_correlation` 找相关≈0 的候选腿 |
| 2b | **中性化骨架重构**：`group_neutralize(同信号, sector)` 包裹——行业暴露是与 PROD 池拥挤的接触面（KOR wave113 实证：同一 pvdom 信号裸结构 0.7003→包裹后 0.6993 过闸并直接提交 ACTIVE；注意是表达式层骨架非设置层中性化） | prod 踩线 0.70-0.75 且诊断显示自家 book 低相关（拥挤源在外部池） |
| 3 | **换白名单不同数据集**（D0 默认动作） | 1/2 无素材时；勿磨同腿变体 |
| 禁止 | 磨参数（decay/中性化/窗口）降 PROD——拥挤风格与参数无关（option8 IV 族 0.83-0.91 全参数空间实证） | — |
| 前置 | 达标候选提交前必须平台侧 `check_correlation`（本地互相关只是下限，本地 0.61 → 平台 0.7723 REJECT 实证） | 全部达标候选 |

