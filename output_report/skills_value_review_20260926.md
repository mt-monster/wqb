# 33 个 skills 功能点与输入输出价值评估（实证版）

> 日期：2026-09-26 · 判据：**全部来自本地可查的实测数据，不以文档自述为准**
> 用途：回答"每个 skill 到底做什么、吃进去什么、吐出来什么、**这些产出值不值**"

---

## 0. 实证基准（先立标尺，再评价值）

| 指标 | 实测值 | 含义 |
|---|---|---|
| `expressions` 表 | **65,580** | S2 累计生成 |
| `backtest_results` | **8,267** | 回测率 **12.6%**（生成远超回测吞吐） |
| `gate_results` | 1,502（全过 747 = **49.7%**） | S2→S3 门禁 |
| `wave_results` | **930**：PASS 92 / PARTIAL 256 / **FAIL 509** | **波级失败率 55%，PASS 仅 10%** |
| `alphas` | 8,323；**已测 prod 421** | prod 预检覆盖率 **5.1%** |
| 其中 `prod ≤ 0.7` | **135（32.1%）** | 相关性闸门淘汰率 **68%** |
| `submit_ready` | SUBMITTED 65 / DEAD 25 / BLOCKED 5 / READY 2 | 终局产出 |
| **端到端转化率** | 65,580 → 65 提交 = **0.10%** | 漏斗总效率 |

**两条贯穿性结论**：
1. **gate（49.7% 通过）不是瓶颈，prod（68% 淘汰）才是** → 提升 S2 生成量与 IS 优化**几乎不产生终局价值**；
2. **任何声称"能提升产出"的 skill，若作用点在 IS 或生成量上，其价值存疑**——必须作用在**结构性降相关**上才有效。

### 本轮新发现的实证缺陷（影响两个 skill 的价值兑现）

> ★ **`wave_results.verdict` 枚举污染**：930 行中 **73 行（68 种）是描述性值**
> （如 `8/8 过硬闸, 新高 3.58`、`0/6 过硬闸, 新高 0.63`，另 1 行 NULL），
> 而 `wq-brain-ra-pipeline` 步 9 明确规定 **verdict 强制枚举 PASS/FAIL/PARTIAL**。
> 后果：**停止规则 B（同轴连续 3 波 FAIL 熔断）无法计入这 7.8% 的波** → 熔断判据被系统性低估。

---

## 1. 编排层（3 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **wq-brain-ra-pipeline**<br>791 行 / 引用 39 MCP | 九步 SOP 编排：区域 profile 路由、停止闸、饱和路由、PPA 分支、日循环 | region → 各阶段决策 + `wave_results`/`registry_empirical`/ledger | **价值兑现（主干）**。930 波、1014 条 registry 实证是它驱动的。但**步 9 的 verdict 枚举规定未被执行**（73 行污染），且 19 个 workflow 节点中 9 个从未进 SOP |
| **wq-brain-campaign-matrix**<br>135 行 | 查表：region+意图 → 预解析配置包（universe/候选集/死路/胜绩）；战役后回写 registry | platform+DB → 配置包参数 | **价值兑现**。1014 条 `registry_empirical` + 4665 条 `ledger_kv` 是其实证产出 |
| **wq-brain-campaign-toolkit**<br>345 行 / 114 文件 | 战役执行引擎：8 闸 gate、pipeline、wave、probe、ledger、scan_fields、review、diversity | 战役目录+子命令 → DB 各表 | **价值兑现（最硬的产出者）**。1,502 条 `gate_results`（49.7% 通过）、8,267 条 `backtest_results` 全部由它落地。是 `wave_results`/`registry_empirical`/`ledger_kv` 的**唯一正式写入方** |

## 2. L0 情报选题（4 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **brain-next-move-analysis**<br>70 行 | 日报/平台进展/金字塔分析/区域态势 | 平台活动+DB → 情报报告 | **部分兑现**。并行情报层，不产配置；区域清单曾缺 DEU/JPN/AMR（代码 14 区）已记待修 |
| **wq-brain-ppa-mining**<br>313 行 | PPA 主题匹配 + S0 三硬门槛方法论（cov≥.85/α≤50/f≥10） | 公告+快照 → 门槛判定 | **价值存疑（实证不利）**。`PURE_POWER_POOL_THEME` 主题闸**两次实证不过**（9/2 GLB、9/3 USA），只能等主题轮换；"体检硬门槛"本身未被执行验证 |
| **brain-forum-browse**<br>246 行 | 论坛浏览与经验回收 | 论坛 → 方法沉淀 | **部分兑现**。硬规则"每轮必贡献"与"平台无写工具"**结构性不可满足**（已记录待降级措辞） |
| **alpha-template-labs-data-analysis**<br>90 行 | Brain Labs 原始数据诊断（覆盖/缺失/频率/离群/相关） | Labs 原始数据 → 诊断 | **存疑（无入边）**。ra-pipeline 完全未提及；零实证产出记录 |

## 3. L1 数据理解（7 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **brain-dataset-exploration-general**<br>76 行 | 数据集级审计与分类（选集） | 平台 datasets → 选集画像 | **部分兑现**。自带区域表是 2026-08 快照（已标注非权威）；与 `recommend_datasets`（不校验区域覆盖率）接口脱节 |
| **brain-datafield-exploration-general**<br>80 行 | 单字段 6 法评测（覆盖/非零/频率/取值/中心趋势/分布） | 字段 → 可用性结论 | **部分兑现**。本层是"覆盖率审计硬闸"与"幽灵字段验活"的唯一落点，但**两条铁律此前未写入任何 skill**（本轮已补入 ra-pipeline 步 3） |
| **brain-data-feature-engineering**<br>322 行 | 字段→特征工程决策，产 ideas.md | 字段白名单 → 预处理决策+ideas | **部分兑现（有实证损失）**：其产物曾被 GEM 引擎读成**空串**（内嵌副本无 SKILL.md），顶层 322 行**从未进入 LLM prompt**（本轮已修） |
| **brain-alpha-research**<br>53 行 | 通用研究方法/范式库/跨区陷阱 | 研究需求 → 方法参考 | **存疑（与权威常量冲突）**：「区域优先级 HKG≈KOR>EUR」与 `config.REGION_PRIORITY`（EUR=2/HKG=1）**相反**（本轮已改为标注冲突+以 config 为准） |
| **brain-alpha-research-field-quality**<br>68 行 | WebDataScope 数据包质量预筛（离线圈选） | 本地快照 → 字段种子排序 | **存疑（无入边 + 已失效引用）**：`WebData_*.zip` 实为目录（照抄必失败）；数据包仅 7 区，DEU 白名单 9 集**0 集**落在快照内 |
| **brain-alpha-research-hypothesis-first**<br>97 行 | 饱和数据集的假设驱动路径 | 假设目录 → 主假设/消融/对照/变体 | **失效（实证零使用）**：`data/hypothesis_catalog/` 仅 1 个文件、无生成器；ra-pipeline 步 2 的饱和路由是**死路**（dry-run 唯一 FAIL） |
| **brain-alpha-research-news-sentiment**<br>68 行 | news/sentiment 家族分类 + 6 桶配对 + Tier A | 新闻/情绪数据集 → 字段组合 | **存疑（无入边 + CLI 不存在）**：引用的 `wqb news-refresh-portfolio` 无此入口；Tier A 门槛缺 coverage 项 |

## 4. L2 表达式生成（3 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **brain-make-some-gem**<br>152 行 | **S2 唯一主链生成器**：概念优先 GEM + priors 注入 | 字段池+priors → `expressions` 表 | **价值兑现但当前受阻**：65,580 条 expressions 是它的产出；**但 LLM 通道 `402 Insufficient Balance` → 实跑报"no meta.json within 90s"的假失败**，且干跑验证不了 LLM 可达性（假绿）。绕行：手写 ideas 走 `--ideas-file` |
| **brain-feature-implementation**<br>111 行 | idea Markdown → 表达式实现（含下载） | ideas → `final_expressions.json` | **价值有限（定位被纠正）**：本 skill 被内嵌在 GEM 内，**不得当主链入口**（本轮已写入边界段）；其产物 `final_expressions.json` **不是真相源**（真相源是 DB `expressions`） |
| **alpha-expression-verifier**<br>67 行 | 纯语法校验（括号/元数/参数） | 表达式 → 语法判定 | **价值兑现（窄而可靠）**：被 MCP `create_multi_simulation` 内置调用做静态门禁；**无入边**（ra-pipeline 未提及）但不影响实际调用链 |

## 5. L3 设置仿真（3 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **brain-sim-alphas-in-batch-and-track**<br>202 行 | 批量仿真/发批/跟踪/断点续跑 | 已过闸批次 → `backtest_results` | **价值兑现**：8,267 条回测的落地者。但**回测率仅 12.6%**（65,580→8,267），说明 **S2→S3 断链是真实积压**；`--submit` 默认含义易被误读为"提交 alpha"（实为提交回测） |
| **brain-inspect-raw-template-create-setting**<br>91 行 | 原始模板/设置的创建与合法性核对 | 模板 → 设置计划 | **部分兑现**：与 sim-alphas 争写 `settings.json`/`final_expressions.json`，本轮已裁定"只产计划、不写真相源" |
| **wqb-concurrency**<br>111 行 | 并发调优：Token-Bucket C≈7、七槽填槽、429 退避 | 并发参数 → 吞吐 | **价值兑现（有量化实证）**：multi(8) 86.1 α/hr vs single 54.3 α/hr，加速 1.59×；七槽模式已固化进 pipeline |

## 6. L4 诊断优化（6 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **wq-brain-alpha-optimization-v1**<br>189 行 | Mode B 换概念（70%）/ Mode A 调参数（30%），**产生新变体并回测** | 卡住候选 → 新变体 | **核心但实证收益低**：`wave_results` 里大量 FAIL 描述为"prod 0.85–0.97 撞墙""Mode A …prod 0.84–0.85"——**改了仍撞 prod 墙**，印证"优化 IS 无效" |
| **brain-how-to-pass-alpha-test**<br>124 行 | 只读查阈值、解释"为什么不过闸" | 指标 → 阈值解释 | **价值兑现（只读，安全）**：本轮已与 optimization-v1 划清（判据=是否产新表达式） |
| **brain-alpha-robustness**<br>140 行 | 反过拟合/稳健性闸（跨年、子宇宙、逐年归因），S4→S5 必经 | 达标候选 → 稳健性裁决 | **价值兑现**：`LOW_ROBUST_UNIVERSE_SHARPE`（limit 1.0）是 IND 的主绑墙，实证在 wave_results 中大量出现 |
| **brain-calculate-alpha-selfcorr-quick**<br>61 行 | 本地快筛 self-corr/PPAC（不占平台配额） | PnL → 本地相关值 | **部分兑现**：本轮实测本地预检会偏低（0.397→平台 0.546），**不能替代实测**；本轮已改掉"用 GET /submit 探测"的错误写法 |
| **brain-explain-alphas**<br>57 行 | 收益来源归因与机制解释（按需） | alpha → 归因 | **部分兑现（按需，非必经）**：无独立产出表，价值依赖人工解读 |
| **brain-alpha-repair**<br>43 行 | 弱候选修复配方查表 | 弱候选 → 配方参考 | **存疑**：改进入口是 optimization-v1，本 skill 仅配方；43 行、零资源引用、命中 0 边界词（本轮已补） |

## 7. L5 过闸提交（3 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **worldquant-submit-alpha**<br>284 行 | **REGULAR 单颗真实提交**：POST 四态处置、异步补发、属性规范 | 已确认候选 → `ACTIVE` | **价值兑现（65 颗实证）**。但本轮实测纠正三处硬错误：① `GET /submit` **恒 404**（不是"SPA 壳/403 权威"）；② **`PENDING ≠ FAIL`**；③ 403 真因常是**配额 `REGULAR_SUBMISSION 4/4`**而非相关性 |
| **wq-brain-superalpha**<br>242 行 | SUPER 组套（selection+combo，需 ACTIVE REGULAR ≥10） | ≥10 组件 → SUPER alpha | **价值兑现**：GLB `A1NQ57NW`（IS S4.26/F3.72）、KOR `9qjGvaWe`（S3.27/F4.13）均已 ACTIVE。双闸 0.7 名义阈值 vs 实证（0.8094/0.8571 PASS，0.8938 FAIL）分界在 0.86–0.89 |
| **brain-alpha-judge**<br>292 行 | S5 **参考核对层**：PPA 主题/相关性人工核对 + trend score + 点塔排序 | 达标候选 → 参考评分 | **价值兑现（参考层定位清晰）**：判定权已移交 submit_verdict；`submit_ready` 97 条（READY 2 / BLOCKED 5 / DEAD 25 / SUBMITTED 65）是其实证面。**无入边**（ra-pipeline 未提及）但属有意设计 |

## 8. L6 监控复盘（2 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **wq-backtest-monitor**<br>154 行 | 机器级进程枚举、四关审计、ETA/吞吐、判停 | 在跑任务 → 复盘报告+台账 | **部分兑现**：它是 `wave_results` 的**文档级**回写方，但本轮实测 **73 行 verdict 非枚举** → 其 §14 台账回写与停止规则 B 的判据被削弱；§5 与 §10 内容重复 |
| **brain-dataset-mining-experience**<br>56 行 | 逐数据集中文经验沉淀（只读台账） | 已回测数据集 → `reports/dataset_experience/*.md` | **价值兑现（正面样板）**：自限只读、不判死不改台账；是 S6→S-PRE 闭环的经验载体 |

## 9. L7 元技能（2 个）

| skill | 功能点 | 输入 → 输出 | 实证判定 |
|---|---|---|---|
| **planning-with-files**<br>213 行 | 复杂任务文件化规划（task_plan/findings/progress） | 任务 → 三件套 | **非 WQ 链**：hooks 全局注入会在所有 WQ 任务触发副作用（已记录待收敛） |
| **pull-brain-skills**<br>60 行 | skill 导入（ZIP/目录/Git） | 外部源 → `Claude/skills/` | **有治理风险**：`--dest` 默认直写权威目录，只校验 SKILL.md 存在、不校验 layer/命名（已记待修） |

---

## 10. 价值排序（按"是否作用在真正的瓶颈上"）

### 高价值（直接作用于 prod 相关性 / 终局提交）

1. **wq-brain-campaign-toolkit** — 唯一把所有阶段落地成 DB 行的引擎（1,502 gate + 8,267 回测）
2. **wq-brain-ra-pipeline** — 唯一编排；930 波由其驱动
3. **worldquant-submit-alpha** — 65 颗 ACTIVE 的唯一执行路径
4. **wq-brain-superalpha** — 已产出 2 颗 ACTIVE SUPER（GLB / KOR）
5. **brain-make-some-gem** — 65,580 条表达式来源（**但当前被 LLM 402 阻塞**）

### 中价值（有效但不作用在瓶颈上）

`campaign-matrix`、`sim-alphas`、`wqb-concurrency`（吞吐实证）、`how-to-pass`、`robustness`、`dataset-mining-experience`、`expression-verifier`、`optimization-v1`（在 prod 墙上收益有限）

### 价值存疑 / 失效（本轮实证标红）

| skill | 实证理由 |
|---|---|
| `brain-alpha-research-hypothesis-first` | catalog 仅 1 文件、无生成器 → 饱和路由死路；dry-run 唯一 FAIL |
| `brain-alpha-research-field-quality` | 无入边；`WebData_*.zip` 实为目录；数据包仅 7 区、DEU 0 覆盖 |
| `brain-alpha-research-news-sentiment` | 无入边；`wqb news-refresh-portfolio` 不存在；Tier A 缺 coverage |
| `brain-alpha-repair` | 仅配方参考，改进入口是 optimization-v1 |
| `alpha-template-labs-data-analysis` | 无入边、零实证产出 |
| `wq-brain-ppa-mining` | 主题闸两次实证不过，重试无效 |
| `brain-alpha-research` | 与 `config.REGION_PRIORITY` 结论相反（本轮已改） |
| `brain-feature-implementation` | 不得当主链入口（内嵌于 GEM） |

---

## 11. 由本次评估引出的三个待办（按 ROI）

1. **P0 · 修 `wave_results.verdict` 枚举污染（73 行）** —— 否则停止规则 B 的熔断判据长期失真；建议 `tools/migrate_wave_verdict_enum.py` 归一 + 加守护测试。
2. **P0 · 解 GEM 的 LLM 402 阻塞** —— 否则 S2（65,580 条的来源）当前不可用于新生成；固化 `--ideas-file` 旁路 + 起跑前 LLM 探活。
3. **P1 · 把"停止规则 B 计数"与 verdict 枚举绑定** —— 与第 1 条同源，是 wq-backtest-monitor 判停价值兑现的前提。
