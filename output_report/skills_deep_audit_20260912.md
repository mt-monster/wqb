# Skills 深度研读审计报告（逐篇精读级）

> 2026-09-12 · 范围：`Claude/skills/` 全部 32 个 skill。方法：① 全量结构扫描（frontmatter 契约/链接/脚本存在性/MCP 工具名比对，脚本 `logs/_tmp_skill_audit_20260912.py`）；② 12 个核心 SKILL.md 逐篇精读；③ 全部扫描命中逐条对原文甄别（排除 4 类误报）。
> 与 09-11 复验的关系：那次验证的是"24 项改进是否落地"；本次是**横向精读找新问题**——结果确实找到了 09-11 改动的"未回灌面"。

---

## 一、总体结论

| 层 | 评价 |
|---|---|
| **架构与分工设计** | ✅ 优秀。"编排(ra-pipeline) / 查表(campaign-matrix) / 引擎(toolkit) / 入口(sim-alphas)" 四层分工清晰，衔接协议、单轨 DB、"唯一权威"声明覆盖率高，反模式段具体可用 |
| **新鲜度分布** | ⚠️ 两极分化：09-10/09-11 被这轮审计改过的 15 个 skill 很新鲜；其余 17 个 `last_verified` 停在 08-22~08-25，其中**至少 8 个内容实际被改过却没更新元数据** |
| **事实准确性** | ❌ 存在 9 项 A 级问题——多数是 **09-06~09-11 的一系列修正（8 闸统一、步5 入 MCP、DB 单轨、阈值 schema 补齐）只改了"主链"skill，没有回灌到引用同一事实的"旁支"skill** |

**一句话**：体系设计是好的，病根是"**同一事实写在多处，修正时只改了一处**"——这正是上一轮 P0-1（文档一致性测试）要治的病，但测试覆盖面还没包含这几类跨 skill 事实。

---

## 二、A 级发现（事实性错误 / 跨 skill 矛盾，按危害排序）

### A1. campaign-matrix 的步 5 派发映射仍是 09-11 审计前的**已纠正错误**
- 位置：`wq-brain-campaign-matrix/SKILL.md` §3 派发（约 :87）
- 现文：`步 5 门禁（workflow_campaign stage="S2" + preflight_expressions）`
- 事实：09-11 审计已定性"`workflow_campaign(stage='S2')` 只路由到 build_wave.py＝**选波**，不要拿它代替门禁"；且步 5 已有 `workflow_execute(node="wave_gate")`。ra-pipeline/docs/AGENTS 三处都改了，**唯独 campaign-matrix 的派发节漏改**。该 skill 是 S-PRE 查表入口，按此执行会把选波当门禁、跳过真正门禁。

### A2. wqb-concurrency §8.4 与 toolkit §9 的台账权威**直接矛盾**（单轨化漏网）
- 位置：`wqb-concurrency/SKILL.md` §8 SOP 第 4/6 步
- 现文："每波回收后立即**追加**到 `WAVE_LEDGER.md` + 同步更新 `ledger.json`……**台账唯一写入入口是这两个文件**"
- 矛盾方：`wq-brain-campaign-toolkit/SKILL.md` §9："WAVE_LEDGER.md 快照：**从数据库生成（覆盖写，勿手改）**"；§8/衔接协议："DB（`wave_results`/`ledger_kv`）为唯一事实源，禁止 Agent Write 战役 json/csv"。
- 危害：S3 执行者按 concurrency 写文件 → 单轨被破坏 → `check_ledger_sync` 与 DB 视角分裂。§8 第 6 步"台账驱动选波"也指向文件而非 DB。

### A3. `ra-campaign-prompt.md` 步 5 仍写"**不在 MCP**"（被自己 09-11 下午的 P0-3 推翻）
- 位置：`wq-brain-ra-pipeline/references/ra-campaign-prompt.md:54`
- 该文件写于 wave_gate 节点落地**之前**，落地后未回头改。提示词方案是给未来挖掘会话用的，会持续教错。

### A4. MCP 工具数/节点数**三处口径分裂**
- `wq-brain-ppa-mining` §9：**66 工具**（wqb-db **32**）+ "workflow 引擎：**7 个节点**快捷方式"
- `wq-brain-ra-pipeline` 尾注（:535）：wq-brain-http **68** 个 / wqb-db **33** 个
- 实况：wave_gate 注册后 workflow 节点 = **8 个**；工具总数无单一权威统计器（`@mcp.tool()` 装饰器只捕到 11 个，注册机制分散在 tools_*.py，无法机械裁决 66 vs 68）。
- 危害：低危但持续磨损信任；"7 个节点"会直接误导链路判断。

### A5. submit-alpha 的配额模型**缺 PPA 通道**，且 PPA 提交路径的关键事实未上浮
- 位置：`worldquant-submit-alpha/SKILL.md` §"提交前 ET 日历日配额闸"（:204-214、:230）
- 现文：配额模型只写 "REGULAR 4/日 + SUPER 1/日"，check 只读 `REGULAR_SUBMISSION/SUPER_SUBMISSION`。
- 缺失：① `POWER_POOL_SUBMISSION`（1/ET 日，独立不互占）；② `brain-alpha-robustness:117` 已实证的**关键事实**——MCP `submit_alpha` 内置常规 RA 闸（Sharpe>1.3/Fitness>0.75/Margin>15bp）**对合法 PPA 照拦**，合法 PPA（S≥1.0/算子≤8/字段≤3/PC<0.5）**只能走平台 web UI、且仅在当期活跃主题窗口内**。这条散落在 robustness 深处，ppa-mining §7 的"提交 tags=[PowerPoolSelected]"完全没提。
- 注：这正是 DB 台账 PPA 提交=0 的结构性原因之一——没有可自动化的 PPA 提交路径，纪律里"每天先提 PPA"从未接上管道。

### A6. toolkit 同文档**自相矛盾**：§1.x 表 vs §6 闸数
- 位置：`wq-brain-campaign-toolkit/SKILL.md` §1.x 核心工具表（:34）`gate.py | 5 闸预检（语法/字段白名单/VECTOR 包裹等）` vs §6（:107）`**8 闸 + 可选闸0**`（09-11 已修）。§工具化纪律表（:207）"每波门禁（语法 + 5 闸 + 多样性）"同病。
- 另 §3（:64）："KOR/IND/DEU 实为扁平形态（无 quick_scan / probe_scoring_v2 / hard_gates）"——**过期**：09-11 P1-6 已给三区补齐 quick_scan+hard_gates（仍缺 probe_scoring_v2 属刻意），现为"混合形态"。

### A7. ra-pipeline signal_floor 行未反映 09-11 实证回填
- 位置：`wq-brain-ra-pipeline/SKILL.md:447`（循环停止表"信号天花板闸"行）
- 现文仍以"`max_sharpe_floor` 缺省 0.5"为主口径，未提 09-11 已按实证上调：**IND 1.2 / USA 0.9 / MEA 1.2**（每波 max|sharpe| p25，只上调不下调）。对高信号区 0.5 形同虚设的结论应写进来。

### A8. 内部线与平台闸**未做双层标注**，跨 skill 数字互相"打架"
- turnover：ppa-mining §6 "TVR ∈ [5%,20%]（廉价闸门）" vs optimization-v1（:180）"平台硬闸 1%–70%，内部目标 ≤40%"。两处都自称闸门，实际一个是 PPA 内部经验线、一个是平台硬闸+内部稳健线。
- sub-universe：submit-alpha 验证清单 "LOW_SUB_UNIVERSE_SHARPE≥0.9" vs how-to-pass（:81）平台公式 `≥0.75×sqrt(子域/全域)×sharpe`。
- 危害：执行者无法判断哪些是平台硬线（违反=FAIL）、哪些是内部从严线（可按区调整）。

### A9. campaign-matrix 硬编码工作区绝对路径
- 位置：`wq-brain-campaign-matrix/SKILL.md:35` `D:\coding\traeCN_project\wqb\data\wqb.db`
- 换机/换路径即失效；其余 skill 均用相对路径或 `data/wqb.db`。与"禁止硬编码绝对路径"纪律精神不一致（docs-consistency 测试只扫 `C:\Users` 模式，扫不到这条）。

---

## 三、B 级发现（元数据卫生）

### B1. `last_verified` 系统性失真（17 个陈旧，其中 8 个"内容改了元数据没改"）

| skill | lv 现值 | 实况 |
|---|---|---|
| wq-brain-ppa-mining | 08-22 | 09-10/09-11 两轮改动（适用域注、.qoder-cn 清除）未 bump |
| wq-brain-campaign-toolkit | 08-24 | 09-11 改 §6/描述，未 bump |
| wqb-concurrency | 08-22 | 09-11 改 check_ledger_sync 路径，未 bump |
| brain-sim-alphas-in-batch-and-track | 08-23 | 09-10/09-11 改 CSV 定位，未 bump |
| wq-brain-campaign-matrix | 08-22 | 09-11 改 skill 计数/删 .qoder-cn，未 bump |
| wq-brain-alpha-optimization-v1 | 08-22 | 09-11 改上游读库口径，未 bump |
| pull-brain-skills | 08-22 | 09-11 清 .qoder-cn，未 bump |
| brain-data-feature-engineering | 08-22 | **正文含"2026-09-01 精简"整节**，元数据滞后 10 天 |

其余 9 个（08-22~08-25）内容未动，属"长期未复核"：alpha-expression-verifier、brain-datafield/dataset-exploration-general、brain-explain-alphas、brain-feature-implementation、brain-forum-browse（09-11 我修过断链！也在"改过没 bump"列）、brain-how-to-pass-alpha-test、brain-inspect-raw-template-create-setting、wq-backtest-monitor、brain-next-move-analysis（08-25）。
- 根因：lv 靠手改，无守护。上一轮 P0-1 测试没覆盖"lv 与 git 最后修改日期"的漂移。

### B2. 无工具注册数的单一权威来源
66/68 之争无法机械裁决 → 需要一个生成式统计（从注册表读数、写入 INDEX、测试守护），而不是三处手写数字。

---

## 四、C 级发现（小项，顺手修）

1. `brain-make-some-gem` 步 5 行（:28）"wave_gate 5 闸预检"——未引用 INDEX 闸编号基准表（闸1–5 口径应对齐）。
2. sim-alphas 标准命令示例 `workflow_batch_track(concurrency=7)` 与 ra-pipeline"禁止拼 `--concurrency`"的边界未说明（MCP 参数 vs CLI flag 是两回事，但读者会混淆）。
3. `docs/reference/feature_engineering_sop.md:188` "七阶段战役流水线" → 应为"九步"。
4. sim-alphas 扫描器误报澄清（`build_wave.py` 是 toolkit 相对路径、`_gate_waveNN` 是反模式禁止项）——**无需改**，但可考虑把跨 skill 相对路径写成 repo 相对，减少误报。
5. **误报排除清单**（验证过，勿"修复"）：`lookINTO_SimError_message` 是真实工具名（tools_sim.py:366 亲述）；INDEX/gate-rules/skill_call_chain 的 `.qoder-cn` 均为合法上下文（junction 说明/探测链/废弃对照表）；brain-alpha-judge 论坛语料中的 TOP2500 是用户帖原文。

---

## 五、优化方案（P0/P1/P2，待确认后落地）

### P0 · 事实纠错（预计半天，全部是定点文字修）
| # | 动作 | 位置 |
|---|---|---|
| 1 | 步 5 派发改为 `workflow_execute(node="wave_gate")`（或 `tools/wave_gate.py`），删"workflow_campaign(stage=S2)+preflight 当门禁" | campaign-matrix §3 |
| 2 | §8.4/§8.6 台账口径改为 DB 单轨：结论入 `wave_results`/`ledger_kv`（campaign.py CLI），WAVE_LEDGER.md 定位为生成快照；选波输入改为 DB 查询 | wqb-concurrency §8 |
| 3 | 步 5 行改双通道："MCP `workflow_execute(node="wave_gate")` 优先，CLI `tools/wave_gate.py` 兜底"，删"不在 MCP" | ra-campaign-prompt.md:54 |
| 4 | 配额模型补 `POWER_POOL_SUBMISSION 1/日`；新增"PPA 提交路径"小节：MCP submit 非 PPA 感知 → web UI + 活跃主题窗口（引用 robustness:117 实证），并回指 ppa-mining | submit-alpha §配额闸 |
| 5 | §9 工具数/节点数改为引用唯一基准（INDEX.md），"7 个节点"→8 | ppa-mining §9 |
| 6 | §1.x 表与 §工具化纪律表的"5 闸"→"闸1–5（基准表见 INDEX）"；§3 三区形态描述更新为"混合形态（quick_scan/hard_gates 已补，probe_scoring_v2 刻意缺）" | toolkit |
| 7 | signal_floor 行补实证回填值（IND 1.2/USA 0.9/MEA 1.2 + 回填规则） | ra-pipeline:447 |
| 8 | campaign-matrix:35 绝对路径 → `data/wqb.db`（相对） | campaign-matrix |

### P1 · 防复发（与既有测试体系接轨）
| # | 动作 |
|---|---|
| 9 | `test_docs_consistency.py` 新增断言：① `last_verified` ≥ 该 SKILL.md 最后一次 git 提交日期（允许 ±2 天容差）；② skills 中出现的"节点数/工具数"数字必须来自引用（禁止裸写 66/68/7 个节点，改为指向 INDEX 基准段）；③ 禁止 `D:\\coding\\` 类工作区绝对路径 |
| 10 | INDEX.md 增设"**MCP 工具计数基准段**"：写清统计口径与统计命令（对注册表扫描），三处引用它；wave_gate 后节点数=8 一并固化 |
| 11 | 建立标注规范：平台硬闸（PLATFORM）vs 内部从严线（INTERNAL）双标签，先改 turnover/sub-universe 两处示范 |

### P2 · 卫生轮（可并入下次例行维护）
| # | 动作 |
|---|---|
| 12 | 17 个陈旧 lv 的复核轮：内容已改的 8 个直接 bump 至 09-11/09-12；其余 9 个做快速复核后 bump 或标注"未复核" |
| 13 | `feature_engineering_sop.md` "七阶段"→"九步" |
| 14 | sim-alphas 示例补一行边界注释（MCP concurrency 参数 vs CLI --concurrency） |

### 落地顺序
```
P0 #1/#2/#3（链路正确性）→ #4（PPA 通道认知，直接影响提交产出）→ #5-#8（口径统一）
P1 #9 测试先行 → #10/#11
P2 随下次例行维护
```

---
*审计脚本：`logs/_tmp_skill_audit_20260912.py`（可复跑）；原始扫描输出：`logs/_tmp_skill_audit_out.txt`。*

---

## 六、落地记录（2026-09-12 01:10，全部三阶段完成）

**验收：`pytest tests/ -q` = 763 passed（较基线 +36）；`sync_skills.py --check` = 4/4 一致；dry-run 复验脚本 39 项断言全 PASS。**

| Phase | 落地内容 | 结果 |
|---|---|---|
| **P0（8 项）** | ① campaign-matrix 步5 映射改 `workflow_execute` node="wave_gate"（含防再犯警示）；② wqb-concurrency §8.4/§8.6/frontmatter 台账口径改 DB 单轨（WAVE_LEDGER.md 降级为生成快照）；③ ra-campaign-prompt 步5 改 MCP 优先 + CLI 兜底；④ submit-alpha 新增「PPA 通道」节（POWER_POOL_SUBMISSION 1/日、MCP 非 PPA 感知、web UI + 活跃主题窗口）；⑤ ppa-mining 计数改 68/33 + 8 节点并引用基准段；⑥ toolkit §1.x/§3/纪律表对齐（闸1–5 引用、三区混合形态）；⑦ ra-pipeline signal_floor 补实证回填（IND 1.2/USA 0.9/MEA 1.2）；⑧ campaign-matrix 绝对路径改相对 | 23 项断言 PASS |
| **P1（3 项）** | ⑨ `test_docs_consistency.py` 新增 3 组断言（lv 新鲜度 vs git 提交日、裸写计数禁止、工作区绝对路径禁止）→ **234 项全绿**；⑩ INDEX.md 新增「MCP 工具/节点计数基准段」（68 = 13+8+1+3+10+4+3+5+6+4+0+11，装饰器机械计数，测试守护）；⑪ 平台硬线 vs 内部严线双层标注落地（ppa-mining §6 重写为两线三层 + PPAC≤0.5 附加；submit-alpha 验证清单标注 sub-universe 内部线并给出平台公式） | 11 项断言 PASS |
| **P2（3 项）** | ⑫ last_verified 刷新 **24 个**（双判据：`lv < git 最后提交日` 或 `lv ≤ 08-25`；8 个因内容-元数据漂移、16 个陈旧复核），全量 32 个 lv 现最低 09-10；⑬ feature_engineering_sop「七阶段」→「九步」；⑭ sim-alphas 补 MCP concurrency 参数 vs CLI `--concurrency` 边界注释 | 5 项断言 PASS |

**新断言首跑即再拦 3 处**（与上轮 P0-1 首跑揪 10 处同理，证明防线有效）：INDEX.md 两处 `WQ_PY` 硬编码盘符路径（已改 `$PWD` 相对写法）+ `docs/plans/` 历史计划 1 处（加只读白名单）。

**计数裁定**：66/68 之争以机械计数终结——`@mcp.tool` 装饰器逐模块合计 = **68**（13+8+1+3+10+4+3+5+6+4+0+11），已固化为 `test_mcp_tool_counts_match_index`（注册数变化测试即红），三处文档全部改为引用 INDEX 基准段。

**遗留提示**：本轮改动（14 个 skill 文档 + INDEX + 测试 + sop + 报告）在工作区未提交，与并行工作流脏树共存；按 §7 提交纪律需显式路径清单切分提交，待确认后执行。
