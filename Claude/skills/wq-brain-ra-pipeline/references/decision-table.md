# wq-brain-ra-pipeline 挖掘决策表（执行查表）

> 拿到阶段结果后**直接查表执行**；表中没有的分支才允许停下问用户。
> **优先级**：用户显式指令 > 锁定表（`src/wqb/profiles/locked.py`）> 代码 fail-closed 闸（唯一放行 = waiver）> 区域 × 类别组合（`cells.json`）> 区域 profile > 类别卡 > 本决策表 > skill 正文；**D0-P 在锁定表里，不接受区域 / 类别 / 组合改写**（全链与说明见 SKILL.md「怎么读这份 SOP」）。
> 用户指令与表中**硬约束**冲突时：能执行的直接执行并写 waiver 留痕（键 `waiver_<gate>_<region>_<wave|all>`，协议见 `AGENTS.md` §8.1.2；旧键 `stop_rules_override` / `backlog_gate_override` 仍被识别），**不请示**。
> **红线不可覆盖**（任何人批准都无效，`wqb.waiver.RED_LINES`）：提交前的用户明确确认、凭据（`world-quant-brain-mcp/.env`：禁止读取 / 打印 / 提交）、平台条款与限额。另：用户没要求时**不创建自动化任务**。
> **被 SKILL 哪一步引用**：D0 / D0-P / D1 / D2 / D3 / D12 / D14 → 步 7；D1 / D9 → 步 8、9；D4 / D6 / D13 → 步 2、3；D5 / D8 / D11 → 步 6；D7 可选（默认关闭）；D15（判死判据表）→ 步 9。
> 阈值一律「见 `src/wqb/config.py`」；表里出现的数字是**经验值并带出处**，或是某个代码缺省（注明在哪）。

## D0. 拿到回测结果后的主决策（S4 入口）

| 结果状态 | 动作 | 输出 |
| --- | --- | --- |
| 有 alpha 过廉价闸（`config.GATES["internal"]`：Sharpe / Fitness / 换手区间 / margin / returns，且 `is.checks` 无 FAIL；**用户临时阈值只在该次会话提示词内生效，不进本表**） | 进 D1 验证链 | 验证报告 |
| 单数据集 alpha 过廉价闸但 Sharpe 只是刚过内部线（经验：< 2.0），且白名单存在正交数据集 | 进 D3：第二数据集**只能作条件 / 分组 / 残差入场**（辅助腿入场三式，步 7 §7.7.3），**不并列相加** | 单信号结构表达式 |
| 全部未过廉价闸 | 进 D2 证据复核分支 | 分支动作 |
| 过闸但 prod 首探偏高（≥ 0.60） | **按 D0-P 查表**（本表是 prod 墙处置的唯一决策表） | 见 D0-P |

## D0-P. prod 墙首探决策（**唯一决策表**——其余文档一律引用本表，不得另立学说）

> 同一情景（某家族首探 prod 相关性偏高，下一步怎么办）此前有 ≥6 套互相矛盾的处置（首探即判 / prod-first 串行 / 镜像稀释 / 反馈循环与组合腿救援 / 先 5 探针 / 区域预警线）。
> 现统一为下表（skills 审查 X-1；2026-09-29 定案，理由与证据见 `reports/skills_review_20260929_closure.md` 与 `docs/design/skills_review_decisions.md` DEC-07）。
> **首探口径**：族内最强 1 条、平台实测（`check_correlation` 读 `GET correlations/prod`）、串行；实现 `tools/campaign_intel.py prod-first`（`--top-k` 缺省 3 个族、每族最强 1 条，以 argparse 缺省为准）。

| 首探 prod | 动作 | 说明 / 例外 |
| --- | --- | --- |
| **< 0.60** | 正常扩变体，进步 7–8 | — |
| **0.60–0.70** | **不扩变体，当天进步 8**（提交前仍须 `check_correlation(refresh=True)` 终验） | 外部同款会在一小时内把 prod 堵到 1.0（pv103 实证）。**区域 profile 不得另设「预警线」改写本行**（USA 的「0.6 即停扩换腿」已并入本行） |
| **0.70–0.75（踩线带）** | **只允许 1 次有诊断依据的结构性尝试**（先做下方「诊断前置」，再从 ①–④ 选 1 种、做 1 批）：① 删腿 / 换广度轴（MEA 9qXoJge2 0.716→0.6525 实证）② 表达式层 `group_neutralize(同信号, sector)` 包裹（KOR wave113 0.7003→0.6993，n=1）③ **换分母口径**（同族兄弟同分母时；KOR other466 0.8061→0.6843）④ **换设置档 / 分组轴**（中性化、universe、分组轴使用频次；USA 0.95→0.68、GLB 0.7088→0.695）；尝试后仍 ≥0.70 → 按下一行 | 前提：诊断显示撞的是同族同分母兄弟，或自家 book 低相关（拥挤源在外部池）。**禁止**：**无诊断的盲扫网格**（decay / 窗口 / 中性化逐档扫）、对单颗钉子换窗口 / 门控 / 平滑（option8 IV 族 0.83–0.91 全参数空间无效；IND behavioral_signals 9 种构造 prod 0.7161–0.8261，最优只差 0.016）、镜像稀释与任何腿相加 |
| **≥ 0.75，或踩线带尝试失败** | **先做「诊断前置」**：指向单颗钉子 / 族墙，或踩线带尝试已失败 → 家族记 `dead_end`：先 `forum_recon`（`found=true` 不得直接判死）→ `seal_dead_end`；下一步 = **换机制 / 换白名单不同数据集**（勿磨同腿变体） | **唯一例外**：已过 `mode_b_qualification`（主闸或旁路）且有 salvage 辅助腿的候选，可走 Mode B 组合腿救援（optimization-v1 入场三式；禁加权）。**第二个例外**：诊断指向同族同分母 / 设置档拥挤时，≥ 0.75 也可做 1 次同样的结构性尝试（KOR 同分子换分母 0.8061→0.6843 就是从 ≥ 0.75 起步），仍失败才判死 |
| **探针方式** | 只读 `GET correlations/prod`（`check_correlation` / `prod-first`） | **禁用 POST /submit 探测**（通过即提交，见 `worldquant-submit-alpha/references/submit-chain.md`） |

**诊断前置（2026-10-03 增补，`docs/design/skills_review_decisions.md` DEC-72）**——判 `dead_end` 或做那 1 次尝试之前，先用 1–2 次零配额 / 单次平台调用定位「撞的是什么」。原因：prod 墙至少有三种形态，一刀切「禁止磨设置」会把可破的那类也判死。

1. **看直方图、找钉子**：`compute_mutual_correlation(候选, 已提交 / 同族兄弟)`（本地 PnL，不占平台相关性配额）+ `check_correlation` 直方图，分三种形态：(a) **单颗钉子型**——0.7+ 仅 1–3 颗、0.6–0.7 仅 6–16 颗（IND behavioral_signals）→ 任何构造都被钉住，直接 `dead_end`；(b) **密墙型**——0.6–0.7 桶数百颗（GLB probability_label 系 n=848–877），信号层与 prod book 同族，裁剪 / winsorize / 换轴 / 等价算子全无效（GLB 一批 8 条 prod 仍 0.8073–0.8398）→ 不在本表里磨，**换信号载体**；拥挤族强候选全部撞墙（IND pv47 0.78–0.99、尾盘反转 0.88）同属此类；(c) **可破型**——钉子是少数同族兄弟或设置档，见 2、3。
2. **钉子是同族兄弟（共享信号 / 同数据集）**：先比**分母口径**——分母是横截面比较基准，同分母必高相关（KOR 同分子只换分母：self 0.7422→0.6244、prod 0.8061→0.6843；同分母扫 8 个分子无一过闸；机器规则 `denominator_is_the_real_self_wall_variable_v1`）。分母相同 → 换分母类别；仍相同才查分子 / 窗口 / 轴。
3. **钉子在外部池（拥挤风格）**：比**设置档**与**分组轴使用频次**——USA 历史 ACTIVE：SUBINDUSTRY avg prod 0.685（n=4，最高）vs SECTOR 0.532（n=1，最低），换 STATISTICAL + 换宇宙后 0.95→0.68；GLB 某一族的分组轴 country（用 91 次）0.7088 → subindustry（66 次）0.695。**分组轴不是通用旋钮**：IND 的 exchange / country / currency prod 全 0.7501–0.7503、7 个轴 0.74–0.83（对轴免疫）；GLB 另一族的 exchange 轴 0.8138 也没破墙；KOR 的 subindustry 轴反而饱和——「轴空白区」判据不可跨区、跨族外推，逐区逐族小批实测。
4. **先判信号类型再压换手**：水平型信号（桶索引、水平 z 值）压换手能同降 prod（GLB 换手 0.13 → prod 0.7024，0.47 → 0.708–0.728）；变化型信号压换手会杀信号（DEU）。

区域差异是真实的（最优中性化 USA / GLB / KOR / IND 各不相同），所以本表仍**不接受区域改写阈值与处置顺序**；区域 profile 只提供第 3 步「该试哪几档」的实证清单。上述证据来自 WorkBuddy 记忆 2026-10-01 ~ 10-03（`.workbuddy/memory/`），样本很小，按「可试」而非「规则」执行；每次读数记进 `key_findings`，攒够再升级。

## D1. 通过廉价闸后的验证链（全自动，逐 alpha 执行）

*被引用：步 7（逐候选链）、步 8。*

| 步骤 | 动作 | 通过条件 |
| --- | --- | --- |
| 1 | test robust（不同 universe / neutralization 重跑） | 各档稳健、无塌陷 |
| 2 | 过拟合测试（2Y sharpe） | `LOW_2Y_SHARPE` 过**平台线**（`config.PLATFORM_CHECK_LINES["low_2y_sharpe_min"]`；平台把 `LOW_2Y_SHARPE` / `LOW_SHARPE` / `LOW_FITNESS` 的 WARNING 视同 FAIL） |
| 3 | 相关性矩阵 `compute_mutual_correlation`（候选集内两两） | 彼此 < 0.5（内部线） |
| 4 | 硬闸核查：`get_alpha_details` 的 `is.checks` + 本地 SELF / PPAC（PPAC = Power Pool Alpha Correlation） | **平台线**：PROD < 0.7、`LOW_2Y_SHARPE` 过线、CW（`CONCENTRATED_WEIGHT`）必过；**内部线**：SELF < 0.5（平台线为 0.7，别互相顶替） |
| 5 | Failed-count 清零后才可 `set_alpha_properties` 设属性（口径见 [`webdatascope-failed-gates.md`](webdatascope-failed-gates.md)） | — |
| 6 | 入待提交队列：**独立 SQL 表 `submit_ready`**（`src/wqb/store/submit_queue.py` 是单一事实源；CLI `tools/submit_queue.py`；收批自动入队、提交自动退役）——**不是** `ledger_kv` 键，也不再写战役 state json | — |

提交响应的四种形态（200 明确通过 / 201·202 异步受理 / 200 空体 / 403 失败）见 `worldquant-submit-alpha`；判据只认 `status == ACTIVE`。**没有「201 + success:false 是工具 bug」这回事**——旧注已删，它会让人把「异步受理、结果未知」当成可忽略而不补发。

## D2. 未过闸 → 证据复核分支（增强模式决策闸）

*被引用：步 7。*

| 信号状态 | 动作 | 前置条件 |
| --- | --- | --- |
| 单一簇、局部不稳定 | single 增强 | — |
| 两个及以上互补赢家 | cross 增强 | metadata（region / universe / delay / neutralization）一致 |
| \|sharpe\| 0.8–1.5、至少一维过闸（tv / 2y / fit）、同数据集变体耗尽（3+ 次） | **辅助腿入场**（条件 / 分组 / 残差，步 7 §7.7.3；不并列相加） | 白名单存在正交经济维度的数据集 |
| 该集**最强 \|sharpe\| < 0.8**，且已做镜像探针（D12） | 放弃该数据集，换白名单下一个 | 强负信号先按 D12 镜像，别当无信号（旧版只写「sharpe < 0.8」符号盲、粒度错位） |
| 撞 prod 墙 | 按 **D0-P** | — |
| CW（`CONCENTRATED_WEIGHT`）失败 | 只按 **D6 的 CW 修法顺序**；**不补腿**（D3：不允许靠增删腿数修不达标信号）；亦不要 `rank(add(...))` | — |

## D3. 跨数据集补腿（原「混合 mix amplify」；2026-09-29 按**意图**而非语法重定义）

*被引用：步 7。旧版把「主动混合冲更高 Sharpe」写成手段，正是 CLAUDE.md 禁止的「混信号调参」；且「允许的 5 类」与 SKILL 的清单不是同一份（RD-03 / RD-11）。*

| 场景 | 规则 |
| --- | --- |
| **定位** | 跨数据集补腿**不是**提分捷径：优先单数据集 atom；第二数据集只在「主信号有信号但卡某一闸、白名单有正交数据集」时才引入，且**只能以条件 / 分组 / 残差三种身份入场**（辅助腿入场三式，步 7 §7.7.3），**不作并列相加项** |
| 触发 | 主动：单数据集 alpha 过廉价闸但 Sharpe 只是刚过内部线（经验：< 2.0）；补救：\|sharpe\| 0.8–1.5、至少一维过闸、同数据集变体耗尽（3+ 次）（D2） |
| 选辅助腿的经济方向 | 情绪 / 动量 → 补基本面（EPS revision、估值）或微观结构；技术评级 → 补空头兴趣、机构持仓、分析师修正；微观结构 → 补情绪、基本面 |
| **组合形态（铁律）** | **禁止两条独立信号腿的任何加和**（加权 / 等权 / `add` / 中缀 `+`）。**允许形态只有一份清单——步 7 §7.7.2**，本表不再另列。闸 5 是兜底不是许可证（2026-09-28：等权 `add(rank,rank)` 曾漏闸，7 条已作废，见 `incidents.md` I-1） |
| 乘积交互（灰区） | `multiply(rank(A), rank(B))` 闸 5 **不拦**（非加和），但不在允许清单内：**默认不用**；仅当两个基础信号各自 \|Sharpe\| > 1.0 且交互有单一经济解释时，作为 Mode B 想法层的一次尝试并记录理由（margin 脆） |
| 中性化 | 跨数据集表达式用 `group_zscore(..., industry/subindustry)` 包裹 |
| **margin 铁律** | margin 是数据集属性，补腿**不能**修 margin；margin 不足 → 换数据集 |

（曾有的「数据集数 2–5」一行无依据且与「单数据集 atom 优先」方向相反，已删；已废止的 `MINING.slow_fast_mix`（0.40/0.60 慢快配比）见 `Claude/skills/CHANGELOG.md`。）

## D4. 健康检查（S0，generate 前必做）

*被引用：步 2。顺序：`s0-select` → `calibrate` → 打分（`workflow_campaign(stage="S0")` 内部即 `score_datasets.py`），见 `step2-s0.md` §2.1。阈值缺省在 `score_datasets.py`，区域覆盖写 `tracking/<REGION>/config/thresholds.json` 的 `dataset_health`（例：EUR 覆盖为 cov 硬地板 0.6 / 可用字段 10）。*

| 条件 | 动作 |
| --- | --- |
| 已有战役目录 `tracking/<REGION>/` | `workflow_campaign(stage="S0")`（`score_datasets.py`；分位 tier） |
| 无战役目录（跨区试探） | `tools/campaign_intel.py s0-select` / `xr-probe` |
| generate 白名单 | tier1 + `tier_note=pyramid_quota` 上提的非 MODEL（配额后仍无非 MODEL 不得退回纯 MODEL） |
| 白名单排序 | 先按金字塔配给（每波至少 2 个非 MODEL 位），再 score desc；**禁止** pyramidMultiplier desc 把 PV 整座挤出（**例外**：`mode=ppa` 的 PPA 排序见 `wq-brain-ppa-mining` §1.0） |
| 用户指定数据集与白名单冲突 | **用户指令优先**，写 waiver 留痕；**两条用户指令冲突时，后到的显式指令覆盖先前的「定案」**并记 override |
| MCP 不可达 | 健康检查回退 `--mode direct`（端口 / 传输见环境章），不重试烧 turn |
| 本 ET 日已验证 max\|Sharpe\| < 0.5 的数据集 | 跳过，不 re-GEM / re-enhance |
| 当前 Power Pool 主题不匹配 region / delay / universe | 走 RA 分支（`ppa-vs-ra.md`） |
| 白名单空 | 换区域 / universe，不 generate |

**字段数 / 覆盖率 → 处置**（一张表；旧版同一指标散落 5 与 10 两个阈值、三种处置）——注意两个「字段数」**不是同一个量**：

| 量 | 定义 | 判据（缺省；出处） | 处置 |
| --- | --- | --- | --- |
| **usableFields**（S0） | typed catalog 内 coverage ≥ 0.85 的字段数（`score_datasets.usable_fields`） | cov < 0.65 或 usableFields < 5（`thresholds.json` `dataset_health.coverage_hard_min` / `field_count_hard_min` 缺省） | `excluded`（mode 无关） |
| 回填带（S0） | 0.65 ≤ cov < 0.85 且 alphaCount ≤ 50 且 valueScore ≥ 6 | 同上出处（`backfill_band_*`） | tier2 保底；生成**必须** `ts_backfill(66)` 包裹（季频 / 年频字段用 `252`；`120` 不在窗口白名单，见 D6 窗口行） |
| 探针例外（S0） | cov ≥ 0.9 且 alphaCount = 0 且 valueScore ≥ 6 且字段 < 硬地板 | 同上（`probe_exception_*`） | tier2，仅 Stage-A 探针 1 批早停；**字段 < 5 → 仅条件腿 / 事件探针**（`s0-select` 标 `仅条件腿`），不进主攻 |
| **有覆盖的字段数**（S1，步 3） | `catalog_<ds>` 里 coverage > 0 的字段数 | < 10 → 移出白名单；< 5 → 仅条件腿 | 见步 3 失败分支 |

## D5. 设置规则（S2' 展开，勿硬编码 SUBINDUSTRY）

*被引用：步 6（设置层先验在 `pipeline.py run` 里按库存实测自动改写，显式 `--set` 钉住的维度不动）。*

| 场景 | 值 |
| --- | --- |
| 中性化 | **有 win 则跟 win**（EUR 实证 SUBINDUSTRY / decay4）。无 win 才用区域默认。对照轨可另探本区合法档，但不能把未验证档写成主轨。⚠ `ILLIQUID_MINVOL1M` 对 USA / ASI / EUR 已被平台**永久停提**（2026-09-14 公告；且已从档位表移除），不得再作对照档 |
| 禁用 | **逐区判断，不跨区套用**：SECTOR / MARKET 中性化在 EUR 等区压垮 `IS_LADDER_SHARPE`；但 USA D1 的 OS 池 86 颗里 75 颗是 TOP3000 / MARKET（medSharpe 1.49、medTVR 0.038），且 SUBINDUSTRY 反而是 USA 历史 ACTIVE 里 prod 最高的一档（avg 0.685，n=4；WorkBuddy 记忆 2026-10-01）。区域画像里没有实证时，先用小批对照，不要整档禁用。⚠ `docs/experience/02_signal_patterns.md` §3 另记过「USA 的 SUBINDUSTRY 是子宇宙 / ladder 闸的解药（STATISTICAL 必挂 `LOW_SUB_UNIVERSE_SHARPE`）」——两条证据针对**不同的闸**（SUB / ladder vs prod），中性化档要按**目标闸**选并小批对照，别一刀切 |
| decay | **仅缺省**（无 win、无区域实测时）：returns 信号 4 / close 6；有库存实测时以 settings prior 为准（GBR：decay=14 过闸 28.3% n=46 vs decay=4 3.9% n=408） |
| truncation | 缺省 0.08（同上：缺省，非规则）。**不作扫描维度**：实测零杠杆（IND 行为族 0.02 与 0.08 指标逐位相同；GLB 0.08→0.15 零影响，换手低时截断触及不到） |
| decay 与信号速度 | **decay 必须匹配信号速度，不是越大越好**：IND 行为族 mean-5 水平形 decay=1 最优（S 2.36 / 2Y 1.81）、decay=20 全灭；raw(window1) 必须 decay=8（decay10 → 2Y 1.49）。`decay=0` 与 `decay=1` 指标逐位相同，扫描时只留一个。GLB 水平型信号 decay 越大 EMEA 子宇宙越差（22→0.45、33→0.36），用 decay 换 prod 是亏本买卖（WorkBuddy 记忆 2026-10-03） |
| delay | 数据存在时 0，否则 1（MEA 仅 D1） |
| universe | **见 `config.REGIONS[region]["universes"]`**（权威；本表不再抄档位——旧版把 HKG 写成 TOP500/800 而 HKG profile 写待实测）；非法 → HTTP 500 |
| EVENT 字段 | 引用即闸 8 FAIL：**平台无 `ts_event_*` 算子**（KOR wave16 实测 8/8 ERROR）；标准算子在 EVENT 字段上的行为**未验证**——先单条探针；禁 `winsorize`（`winsorize does not support event inputs`） |
| VECTOR 字段 | 必须先 `vec_*` 聚合再进常规算子 |
| 低 coverage | `ts_backfill(66)` 包裹（季频 / 年频字段用 `252`；窗口只取白名单值，见 D6 窗口行） |
| 有界字段 | 跳过 `winsorize` |
| 整数型 | 用 `rank` / `bucket`，不要 `ts_mean` |
| nanHandling / maxTrade | **强度闸，不是风格开关**：IND 行为族同表达式 decay8 下，`nanHandling=OFF` 或 `maxTrade=ON` 使 S 2.19→0.46（2026-10-03 实测）。各区 `settings.json` 取值本就不统一（nanHandling 7 OFF / 6 ON，maxTrade 8 OFF / 5 ON，DEC-39），所以：**跟本区 win 的设置（连同这两项）；无 win 才跟 `tracking/<R>/config/settings.json`**；换档 = 换信号，跨档结果不可比。`tools/submit_batch.py` 固定 nanHandling=OFF / maxTrade=OFF，它的批与 MCP 批不可比；需要精确控制设置时用 `tools/ind_sim_submit.py`（settings 全显式、可带 `--preflight-catalog` 预检字段名）。max_trade 在用户要求时设 ON |

## D6. 信号笔记（S2 生成 / enhance 输入约束）

*被引用：步 2 / 步 4。*

| 规则 |
| --- |
| 优先 `returns` 反转而非 `close`；`IS_LADDER_SHARPE` 须过平台线（`config.PLATFORM_CHECK_LINES`） |
| `hump` **仍受支持，但必须命名参数**：`hump(x, hump=k)`（预闸把 `hump(x, k)` 自动改写；旧版「`hump` 已废弃禁用」说法已删）；`divide` 无 filter 参数；`ts_regression(A,B,n).residual` 非法 |
| `subtract(..., filter=true)` 可用 |
| CW（`CONCENTRATED_WEIGHT`）修法，**按优先级**：①**时间平滑**（同一字段多窗口取均值 / 衰减）`ts_decay_linear(ts_backfill(F,66), 66)` 或 `ts_mean(ts_backfill(F,66), 66)`（低频字段用 `252`；平滑必须作用在**补过覆盖的原始字段**上——只对最终信号套 `ts_decay_linear` 不修 CW：KOR shortinterest38 换手 −53%、CW 仍 FAIL，机器规则 `concentrated_weight_is_data_quality_not_params_v1`）；②**换算子几何** `group_rank(F, subindustry)` / `group_zscore(F, sector)` / `ts_quantile`；③**单信号结构**（`ts_scale`；同源对偶价差 `subtract`——须同数据集且有单一经济含义，步 7 §7.7.2）；④换字段或换信号概念。避免 `rank(add(...))`，**亦禁用任何加权混合**（线性混合已被闸 5 拦） |
| 字段名**逐一经 `get_datafields` 验证**再入批（虚构字段名 = 整批 CANCELLED 连坐） |
| **窗口匹配输入更新频率**：日频→5 / 22；周频→22；月频→66；季频→66 或 252；年频→252 / 504。白名单只有 `1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260`，`120` / `126` / `42` 等不在内——要用先给解释与实测（CLAUDE.md），否则取就近白名单值。证据：GLB analyst_consensus 的年频字段套 `ts_delta(vec_avg(F), 42)`，窗口内几乎无变化、信号被稀释殆尽（WorkBuddy 记忆 2026-10-03）；机器规则 `sparse_field_long_window_v1` 同向（判别量是输入时变频率，不是 coverage） |
| **取负放在 rank 之后且保持零均值**：信号信息在横截面排序里。`subtract(0.5, group_rank(X, g))` ≡ `reverse(group_rank(X, g))` ≡ `multiply(-1, group_rank(X, g))` 有效（KOR insd5 S +0.71 / 2Y +2.42）；`group_rank(reverse(X), g)`（rank 前取负，S −0.84）与裸 `reverse(X)`（S −0.39）被中性化吞掉；`subtract(1, rank)` 结果全正，方向同样被吃掉。`reverse(x)` ≡ `-x`，是平台算子；`inverse(x)` = 1/x，不是取负（WorkBuddy 记忆 2026-09-29） |

## D7. S2-D 多样性榨取决策（**可选，默认关闭**）

*被引用：无（步 4 不要求；`diversity-extract` 只作方向参考，不替代 GEM 概念优先）。`enter_multi_dataset` 会把流程推向跨集，与「单数据集 atom 优先」方向相反——仅当已决定走跨集辅助腿（D3）时才参考。以下阈值是 `diversity_extract.py` 的缺省，无独立实证。*

| 条件 | 动作 |
| --- | --- |
| 选定目标数据集后、生成表达式前 | **可选**：`workflow_campaign(subcommand="diversity-extract")`（方向参考，不替代 GEM） |
| 总表达式 ≥ 15 且低 PPAC 比例 ≥ 0.7 且新颖度 ≥ 0.8 | `enter_multi_dataset`（须过 gate 白名单；跨集失败则退回**单数据集内组合**，不停挖） |
| 总表达式 ≥ 10 且低 PPAC 比例 ≥ 0.6 | `continue_extraction`（再榨 1–2 轮） |
| 总表达式 < 5 | `adjust_strategy`（改生成策略或换数据集） |

## D8. S3 并发回测：决策（步骤清单见 `step6-backtest.md`）

*被引用：步 6。旧版 D8 是 0–6 的**步骤清单**（不是「条件 → 动作」体裁），还要求「追加 `WAVE_LEDGER.md` + `ledger.json`」——与「战役产物只入 `data/wqb.db`」冲突（`WAVE_LEDGER.md` 现只是 `tools/export_wave_ledger_md.py` 的导出视图）。步骤已并入步 6 细则，这里只留真正的决策。*

| 条件 | 动作 |
| --- | --- |
| 任一批 COMPLETE | 立即回收（`harvest_multisim_alphas` → `harvest_multisim_results`），空槽当轮补**组合批**（不空等、不拿弱探针凑数） |
| 首波 / 新信号族 | 先每族 1–2 条骨架做 prod-first（步 5b），族级 `EXPAND` 才扩到 8 条 |
| 波内配额 | ≥ 2 个跨金字塔位；有胜绩则至少 2 个位按机制换腿（步 4 约束 1）；弱探针最多 1 个位，且仅当本波尚无 \|Sharpe\| 近闸字段。**禁止波内全 MODEL / 全裸探针** |
| 开跑前 | 已过步 5 门禁；三道开波闸（DB 判定）通过 |
| 波结论 | 写 `upsert_wave_result`（**不写** `WAVE_LEDGER.md`）；回测指标由 `pipeline.py` 自动入 `backtest_results` |
| 下一波前 | 读 `wave_results`（`get_latest_wave`）与 `tools/step_funnel.py`，**不读** `WAVE_LEDGER.md` |
| 「台账同步门」 | 两份 `check_ledger_sync.py`（`tools/` 与 toolkit）都是 `runs/` 批次字母 + `WAVE_LEDGER.md` 的**文件时代**校验，DB 单轨后只在战役目录仍保留这些文件时才有意义；现行同步门 = 开波三道闸 + `step_funnel` |

## D9. 提交与停止闸（S5）

*被引用：步 8、9。*

| 条件 | 动作 |
| --- | --- |
| Regular Alpha：OS ACTIVE ≥ 10（用户给目标 N 时按 N） | **停**，可转 SuperAlpha（平台要求本区已 ACTIVE 的 REGULAR ≥ 10） |
| PPA 日循环：submit-ready ≥ 4 | **停**（操作约定）。PPA 走**独立配额 `POWER_POOL_SUBMISSION` 1 / ET 日**，与 `REGULAR_SUBMISSION` 4 / 日**并行、不互占**；当天应先提 PPA 那一颗 |
| 配额有槽（`python tools/quota_status.py`）且**用户确认** | POST submit（`worldquant-submit-alpha`；**不可逆**）。**2026-10-02 起节点自动前置三闸**：`_submit_gate`（模拟层 FAIL / 硬闸 WARNING / Failed RA·PPA / **robustness 台账 REJECT**）+ 配额闸（ET 今日满 4 → blocked）+ **prod 闸**（`check_correlation(production, refresh=True)`，max ≥ 0.7 或未出数 → blocked，fail-closed）——人工只需确认「用户明确确认」一项；`force` **不豁免** prod / 配额闸（prod 须显式 `allow_prod_above_07=True` 留痕） |
| 提交前未跑 robustness 审计 | 台账 `robustness_<alpha_id>` 无记录时，节点仍要求 `robustness_audited=True` 显式声明（fail-closed）；**审计结论落台账后本声明闸降为辅助**（REJECT 由 `_submit_gate` 直接拦下） |
| 提交响应异常（201 / 空体 / 403） | 按 `worldquant-submit-alpha` 的四态表处置；**不再有「201 + success:false 是工具 bug」的说法**（D1 已删） |
| 同数据集同腿兄弟 | 相关性 0.82–1.0，提交前 `compute_mutual_correlation` 核查 |
| PPA 提交 | 仅当 `get_messages` 主题匹配**且**用户确认；**合法 PPA 只能走平台 web UI**（MCP 通道不感知 PPA），agent 停下交接（`ppa-vs-ra.md`） |

## D10. 迭代纪律与陷阱自查

| 纪律 / 陷阱 |
| --- |
| 每次迭代最多改 1–2 个变量 |
| 持久化 artifact 与 verdict 到 **DB**（`upsert_wave_result`；战役 state json 已废）；无进展连胜 → 换白名单数据集 regenerate |
| 多样性评估节奏：每 15 轮回测做一次（算子 / 字段探索率、模板骨架 / 风格多样性、预处理、收益归因、失效风险）——**经验节奏，无统计依据**，据此优化生成方向 |
| 不要手写 HTTP，用 MCP `create_multi_simulation` |
| 并发以 `wqb.config.CONCURRENCY` 与 `wqb-concurrency` §8 为准；`TaskStop` 会留孤儿占槽 → 429 |
| 批内一个坏字段 / 坏算子 → 整批 CANCELLED 连坐（提交前逐字段验证） |
| 用户没要求时**不创建自动化任务**（同上文红线） |

## D11. 批次策略选择：探针批 vs 复杂经济学模板（KOR wave96–104 实证，2026-08）

*被引用：步 4 / 步 6。以下只保留仍有效的规则；曾经的「慢变量 × 快变量加权混合」配方（wave91c 的 2 RA ACTIVE 即来自它）自 2026-09-13 起**已废止**（闸 5 拦）——可继承的只有**跨数据集补腿的意图**，落地必须走 D3 / 步 7 §7.7 的允许形态。*

> 背景：KOR wave96–103 连续 8 波单字段探针（`rank(x)` / `ts_zscore` 水平值）全灭（6 数据集 64 条探针 0 达标）；wave104 站在已验证配方上做复杂模板扩展，首批即命中 2 条过全部廉价闸 + IS 硬闸。

| 场景 | 动作 |
| --- | --- |
| 区域已有 \|Sharpe\| ≥ 1.0 或过廉价闸的字段 / 骨架（腿禁用 ≠ 整集判死） | **先做同数据集组合批填满空槽**；禁止把槽位散到新数据集裸探针或复合后仍 \|S\| < 0.5 的弱集。弱探针仅当本波尚无近闸字段时最多 1 个位（步 4 / 步 6） |
| 区域 registry 已有 win 配方（`registry_empirical` layer=win） | 优先做配方家族扩展（复杂经济学模板），不继续探针新数据集；先拉 ACTIVE alpha 的表达式 + settings 作基线 |
| 完全空白数据集（无 win 无历史） | 探针批仅限 1 批 8 条早停；三灯判定后要么判死要么转复杂模板，**不做第二轮探针** |
| 探针连续 2–3 波全灭 | 停探针，回查台账 wins 层找配方；无 win 则换区域或查论坛模板（触发表 #2） |
| 配方家族扩展设计（换腿 / 加腿 / 门控） | **设计前先估算与母配方的相关性**：主导字段（提供绝大部分信号暴露的那条腿）不变 → SELF 相关必然 ≥ 0.9，结构性死路，不做 |
| 真正差异化扩展 | 必须换主导信号源（换慢腿族 + 换快腿族同换）；单换一条腿 = 母配方的高相关变体（KOR 实证：B3 / B4 sh 1.80 / 1.82 达标但与 88lr21xo SELF 0.93 / 0.98 → 双判死） |
| 同族扩展判死回写 | `dead_end` 的 rule 写明「家族扩展天花板」，salvage 记录 NEAR 候选（如 A4 confidence 1.34）备 Mode A 参数收敛 |
| 复杂模板的经济学骨架 | 只用步 7 §7.7.2 的允许形态：事件门控 `trade_when(事件, 腿, -1)`、动量门控 `if_else(rank(快)>0.5, …)`、行业相对强度 `group_zscore(慢, sector)`（⚠ JPN 的 `sector` / `subindustry` / `industry` 是非法 group 字段，见 `regions/JPN.md`）。**跨数据集**的 `ts_corr(慢, 快, n)` / `divide(慢, 快)` 属拼腿，除非两腿是同一经济量的对偶两侧；否则改用条件 / 分组 / 残差三式 |

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

## D14. PROD 墙路由细则（**决策以 D0-P 为准**；本节只补「踩线带」里可做的那 1 次结构性尝试怎么做；先做 D0-P 的「诊断前置」）

| 序 | 尝试（踩线带 0.70–0.75 内只许选 1 种、做 1 次） | 适用条件 / 实证 |
| --- | --- | --- |
| 1 | **结构性去相关**：删腿 / 换广度轴（如 revision 腿 → raised-breadth 双轴，MEA 9qXoJge2 0.716→0.6525） | 候选与自家已提交族高相关，且存在可替换的经济等价维度 |
| 2 | **中性化骨架重构**：`group_neutralize(同信号, sector)` 包裹——行业暴露是与 PROD 池拥挤的接触面（KOR wave113：同一 pvdom 信号裸结构 0.7003→包裹后 0.6993 过闸并直接提交 ACTIVE；注意是表达式层骨架，不是设置层中性化。**证据强度：n=1，差值 0.001 在测量噪声内，只算「可试」不算规则**；同一份文档里 pv103 一小时内 0.6997→1.0000 说明单次读数会被外部提交冲走） | prod 踩线 0.70–0.75 且诊断显示自家 book 低相关（拥挤源在外部池） |
| 3 | **换分母口径**（2026-10-03 增补）：同族兄弟共享分母时，分母是横截面比较基准，同分母必高相关；同分子只换分母（换口径类别，不是换同类字段）。KOR other466：self 0.7422→0.6244、prod 0.8061→0.6843，而同分母扫 8 个分子无一过闸 | 诊断（D0-P 诊断前置第 2 步）显示钉子是同族同分母兄弟；分母决定信号强度的区域要同时读 2Y（KOR 资产侧 2Y 2.22 vs 权益侧 1.12–1.18）。证据强度：KOR 一族，按「可试」执行 |
| 4 | **换设置档 / 分组轴**（2026-10-03 增补）：中性化、universe 与分组轴的使用频次。USA 历史 ACTIVE：SUBINDUSTRY avg prod 0.685（n=4）vs SECTOR 0.532（n=1），换 STATISTICAL + 换宇宙 prod 0.95→0.68；GLB 某一族分组轴 country 0.7088 → subindustry 0.695（差 0.014，接近测量噪声） | 诊断显示拥挤源在外部池、直方图不是密墙，且本区有未试的合法档位（先查 `config.REGIONS[region].universes`）。**不可跨区、跨族外推**：IND 对分组轴免疫（7 轴 0.74–0.83）、KOR 的 subindustry 轴饱和、GLB 另一族 exchange 轴 prod 0.8138。证据强度：USA 一族有效、GLB 差值在噪声内，按「可试」执行 |
| 前置 | 达标候选提交前必须平台侧 `check_correlation(refresh=True)`（本地互相关只是下限：本地 0.61 → 平台 0.7723 REJECT 实证） | 全部达标候选 |
| **禁止** | **无诊断的盲扫**（decay / 窗口 / 中性化逐档扫）降 PROD——option8 IV 族 0.83–0.91 全参数空间实证无效，IND 单颗钉子型同理；有诊断指向设置档 / 分母 / 轴时见上面第 3、4 行；bucket / 门控 / 平滑；**镜像稀释**（加一条与主腿相关≈0 的稀释腿）——**已撤回**：它是「腿相加」，与全局禁令（禁止任何加权混合 / 等权腿相加，见 D3）直接冲突；其引用的 `docs/experience/prod_wall_breakthrough_sop.md` 并不存在，历史实证（EUR Wj71Q12o 0.9013→0.6847）只作背景，不得复现 | — |

## D15. 判死判据表（对象 → 判据 → 记录位置）

*被引用：步 9（§9.5）。旧版「判死」阈值散落各处（D2 < 0.8、D12 < 0.6、`signal_floor` 0.5 / 0.9 / 1.2、`yield=0 且 bt≥8`、profile 的 `fast_kill` 0.5），没有统一定义。下表**不统一数字**（它们是不同粒度的不同判断），只把「对象 / 判据 / 出处 / 记在哪」摆在一处。*

| 对象 | 判据（各自的出处） | 记录位置 |
| --- | --- | --- |
| 候选（单条 alpha） | 未过廉价闸且无 near 资格；或 `RN_EXPOSURE` / `ROBUST_STRUCTURAL` 墙（步 7 §7.3） | review payload 的 `walls`（RN 墙不入 salvage） |
| 字段搭配 | 主导字段不变的兄弟 SELF ≥ 0.9（D11） | `dead_end` 的 payload |
| 家族（信号族） | D0-P：首探 ≥ 0.75（且诊断前置不指向可破形态）或踩线带尝试失败；RN 想法级（该想法**全部**变体 ≤ 0）；同一想法 > 10 种结构仍不过（经验上限）。**前置（2026-10-03）**：IS 强但被某闸卡住的族，封存前须先扫**等价算子替换**——判「不可能 / 天花板」之前这是必做项（KOR：`signed_power`→`quantile` 后 2Y 1.51→1.56；GLB：`ts_scale`→`quantile` 后 S +0.20 / F +0.06；机器规则 `equivalent_operator_substitution_v1`），并在 `seal_dead_end` 的 `reason` 里以「equiv_op_scan：…」写明已试的替换与读到的**全部**闸（替换会同时动多个闸，含 prod：GLB `quantile` 使 prod 0.475→0.565，KOR 则 −0.015） | `registry_empirical` `dead_end`（先 `forum_recon`，再 `seal_dead_end`） |
| 数据集 | 该集**最强 \|sharpe\| < 0.8** 且已做镜像探针（D2）；全方向含镜像 \|sh\| < 0.6（D12，才允许判死回写）；`yield_rate = 0` 且已测 bt ≥ 8（样本量下限）；新数据集 8 探针无 \|S\| ≥ 0.5（区域 profile 的 `fast_kill`，文档级快判死） | ledger `<ds>_dead` |
| 波 | 判定表（`step9-writeback.md` §9.3）：0 达标且 0 near → `FAIL` | `wave_results.verdict` |
| 区 | 停止规则 A / B1 / B2；`signal_floor`（`loop-and-stop.md`）——**是开波闸，不是「记录」** | 闸的 `evidence` |

**未选、未回测不能写成 dead_end**（选波清单里的延后项不是判死）。
