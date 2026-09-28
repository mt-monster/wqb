---
last_verified: 2026-09-26
name: brain-make-some-gem
description: "S2 概念优先的 GEM alpha 表达式生成器（headless_runner）。当需要为某个 region/dataset/delay/universe 组合生成候选 alpha 表达式、跑 GEM、补候选池、按 priors 做增强变体扩展时使用。触发词：生成表达式 / 跑 GEM / makeSomeGem / 选波生成 / 概念优先生成 / final_expressions。编排入口是 wq-brain-ra-pipeline 步 4，标准调用走 mcp__wq-brain-http__workflow_gem，本 skill 描述其后端引擎与产物契约。"
layer: L2
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__*
---

# brain-make-some-gem（S2 表达式生成引擎）

## 职责边界

- **本 skill 负责**：**S2 唯一主链生成器**：概念优先 GEM，产出表达式并落 `expressions` 表（status=`gem`/`enhanced`）
- **本 skill 不做**：不做门禁（`wave_gate`）、不回测（S3）、不判提交；`build-wave` 只做去重/分桶/骨架配给，不产表达式
- **上游 / 下游**：上游 = priors + 字段池；下游 = 步 5 门禁 → S3
- **共享产物约定（2026-09-27 补）**：`priors_snapshot_<region>` 本 skill **只读消费**，
  **唯一写入方 = `workflow_campaign(stage=S2, subcommand="assemble-priors")`**，本 skill 禁止回写。
  若快照早于 `region_kb` / `registry_empirical`，**先提示重跑 assemble-priors 再开生成** ——
  旧先验会让本波沿用过期 win/dead（GBR 实证落后 8 天）。stale 检查当前只 WARN、不阻断，
  **不得据此认为"已确认安全"**；刷新责任归 ra-pipeline 步 9（S6 完成定义）。



## 定位声明

- **本 skill 不是编排器**。唯一挖掘编排 SOP 是 `wq-brain-ra-pipeline`（步 4 = 本 skill）。
- **标准调用方式 = `mcp__wq-brain-http__workflow_gem`**（workflow `gem` 节点）。它负责：解析 skill 目录 → 组装 headless_runner 命令 → 执行 → 校验 `final_expressions.json` → 自动跑质量预估 → 标记 Mode B。
- 只有在 workflow 节点不可用（skill 目录解析失败、需要 workflow 未暴露的 run.py 参数）时，才按下方「直接命令」小节手工执行。
- `brain-feature-implementation` 与 `brain-data-feature-engineering` 在本管道**内部**被调用，**不要**把它们当主链入口。
- 显式 `ideas_file` 的表达式保持经济方向与条件；不得通过替换外层算子强制制造多样性。结构多样性由下游门禁评审。

## 上下游

| 位置 | 内容 |
|---|---|
| **上游** | 步 3（S1）`s1_<ds>_d<delay>` ledger 的 ideas.md；`assemble-priors` 落的 `priors_snapshot_<region>` |
| **本 skill** | 概念优先生成候选表达式 → `final_expressions.json` |
| **下游** | 步 5（S2→S3）门禁：`check_batch` 多样性守卫 → `check_expr_against_inspect` 体检硬门 → `wave_gate` 闸1–5 预检（闸编号基准见 INDEX） |

## 两种生成模式的定位（2026-09-12 补）

| 模式 | 触发 | 模板来源 | 表达式由谁产出 |
|---|---|---|---|
| **family mode**（`--pipeline-mode phased`，默认） | 常规七槽生成 | `wq-brain-campaign-toolkit/config/template_families.json` 8 个 mechanism 族（skeleton 表达式串 + placeholders + forbidden_operators） | LLM 按 priors 概念绑定时相对自由，经 implement_idea 展开占位符 |
| **skeleton mode**（`--pipeline-mode skeleton`） | 字段语义分层后可机械配槽（P0 协议） | `trailSomeAlphas/skeletons.py` 代码骨架（field layering → WINDOW_DOMAINS → 骨架组装） | **代码组装**（LLM 只输出结构化 JSON，语法合法性构造保证） |

选择规则：字段可分层（signal/metadata/scale 清晰）→ skeleton mode；需要族级经济机制叙事（mechanism_premise / field_profile_match）→ family mode。
**2026-09-15 ②**：`workflow_gem` / gem 节点新增 `pipeline_mode`（single/phased/skeleton）透传；headless runner 缺省从 `single` 改为 `phased`
（与本表一致），`skeleton` 从节点层可达。S1 ledger `source ∈ {feature_engineering_node, standalone, standalone_v2}` 的模板渲染文档
**不再自动注入** `--ideas-file`（注入后本管线零 LLM 调用、整波退化为模板展开）；显式 `ideas_file` 仍可覆盖。落盘前 `pipeline_pregate.py`
把 `quantile(x, driver="gaussian")` 无损归一为 `quantile(x)`、丢弃加权混合毒模式（规则同 toolkit `platform_constraints.json`）。社区模板（`KB/community_tpl_kb`，经 `tools/kb_templates.py --emit-ideas` 导出）只作为两者的 ideas 供给源，入批前必须过 ghost advisory。

## 概念优先铁律（与 ra-pipeline 步 4 硬约束同源，此处不复写阈值）

1. **机制 → 1-2 个具体字段 id → 一个 Implementation Example**。禁止「每个字段套 rank」式枚举。
2. 必须带 priors。默认从 DB 快照直读（`priors_from_db=True`，fail-closed：无快照即报错，不静默无 priors 运行）；`priors_file` 仅作显式覆盖/降级兜底。
3. GEM 管道只消费 priors 的 `wins`（≤6）与 `dead_ends`（≤12）两个键（`economic_priors.py`），其余键会被忽略。
4. 只用标准时间窗口 1/5/22/66/252/504/1008/1260；其他窗口必须给出解释或实测证据。
5. 取骨架前必查 `KB/community_tpl_kb` 的 `ghost_operator_advisory`，先做幽灵算子替换再进批，否则整批 ERROR/CANCELLED。
6. **复杂度预算（2026-09-08）**：默认 2–5 个算子，8 个概念里至少 3 个 ≤4 算子。
   依据 859 条过闸样本——算子数 p25=3 / 中位数 5 / p90=12，**46% 的过闸者只有 ≤4 个算子**。
   第二腿之后每加一腿都必须点名它修的是哪个闸（`sub_universe_sharpe` / `2Y_sharpe` /
   `concentrated_weight`），"信号更强"不算理由。
7. **多样性按语义维度判，不按算子类别（2026-09-08 修订）**：要求 ≥3 个不同 Expected Exposure、
   ≥3 个字段族、≥2 个分组轴、≥2 个时间尺度。旧规则强制"每波 ≥1 个 Logical 算子"已废除——
   `if_else` 在过闸者中仅占 5.1%，`trade_when`/`bucket`/`ts_corr`/`ts_kurtosis` 未进前 22，
   而 `group_rank` 占 32.0%、`vec_avg` 12.6%。算子多样性应是语义多样性的结果，不是目标。
   Logical 类算子只在**事件型数据集**（有真实事件时点）才合适。
8. **Expected Exposure 声明会被验证（2026-09-08）**：回测后以 `risk_neutralized_sharpe` 核对。
   它 ≈0 或为负而 raw sharpe 高 ⇒ 该概念**就是**那个暴露本身，判 `dead_end` 且禁止调参。

## 标准调用（推荐）

```
mcp__wq-brain-http__workflow_gem  region=$REGION  dataset_id=$DS  delay=$DELAY  universe=$UNIVERSE  data_type=$DTYPE
```

`data_type` 必须与 S1 `get_datafields` 确认的 VECTOR/MATRIX/GROUP 类型一致——传错会导致整批表达式类型不匹配。
GROUP 入口用于网络/行业等分组轴，须提供已解释的分组概念与实际数值信号；禁止把类别编号的大小或变化直接解释为收益预测。生成器不再对孤立 GROUP 字段自动扩展数值包装。跨集数值字段仍须单独核实来源、白名单与类型，并通过下游门禁。
`ideas_file` 可省略：默认从 S1 ledger 自动注入；显式传入则覆盖。
`priors_file` 可省略：默认走 DB 快照。

返回含 `expression_count` / `quality_estimation` / `mode_b_required`（`EXPECTED_BLOCK > 0` 时为真）。

## 直接命令（仅当 workflow 节点不可用）

```bash
cd scripts/headless_runner
python run.py --config config.json \
  --data-category <CATEGORY> --region <REGION> --delay <DELAY> \
  --dataset-id <DATASET_ID> --universe <UNIVERSE> \
  --instrument-type EQUITY --data-type <MATRIX|VECTOR> \
  --priors-from-db --detached
```

长任务控制：`--detached` 后台启动并立即返回；`--task-id` 指定任务 ID；`--tasks-dir` 任务根目录（默认 `../outputs/tasks`，仓库战役用 `logs/_async_tasks`）。
状态查询：`python run.py --status <task_id> --tail-lines 60`。
`--dry-run` 只校验并打印命令，不执行。

**看实时生成过程**（2026-09-25）：`--detached` 写死 `DETACHED_PROCESS|CREATE_NO_WINDOW` +
stdout 重定向到文件，MCP 服务自身也无控制台，所以终端里天生看不到。两种补法：

- `--detached --console`（= `workflow_gem(console=True)`）：另弹一个真实控制台窗口滚动输出，
  同时经 `_ConsoleFileTee` 双写**同一份** `stdout.log`，所以 `--status` / `workflow_task_status`
  / 闸门读取面全部不变。代价：任务寿命绑在那个窗口上 —— 关窗口 = 杀任务，而 phased
  无断点（mapping 只在内存累加、Phase 3 才落盘），中途被杀 = 整波丢弃。只在人盯盘时开。
- `--watch <task_id> --tasks-dir <root> [--from-start]`：对任意在飞任务做 tail -f，
  `meta.status` 进终态自动收尾，Ctrl+C 只退跟随、不动任务。**看而不抢输出流**，默认用这个。

其余可选参数（`--pipeline-mode phased` / `--max-expressions` / `--require-operators` / `--regen-ideas` 等）见 [reference.md](reference.md)。

## 产物契约

`final_expressions.json` 按序查找**三段**（`gem` 节点 `_find_final_expressions` 同口径，
`src/wqb/workflow/nodes/gem.py:1219`）：

1. **新稳定路径（首选）**：`<repo>/data/gem_runs/{datasetID}_{region}_delay{delay}/final_expressions.json`
   —— 2026-09-25 起数据产物迁出 skill 安装位，与 `skill_roots` 解析解耦；`WQB_GEM_DATA_ROOT` 可覆盖
2. 旧深嵌套位（历史产物兜底，**勿再用于新跑**）：`scripts/trailSomeAlphas/skills/brain-feature-implementation/data/...`
3. 旧备用位（历史产物兜底）：`scripts/headless_runner/outputs/...`

**GEM 自生成 ideas 报告**写 `GEM_REPORT_ROOT`（= `GEM_DATA_ROOT/output_report`，即
`data/gem_runs/output_report/gem_{region}_delay{delay}_{datasetID}_ideas.md`）。
2026-09-26 前它写在 `FEATURE_ENGINEERING_DIR/output_report`（**skill 树内部**），
已造成 16 个产物文件混入仓库；现已迁出。

**`final_expressions.json` 不是真相源**——战役产物只入 `data/wqb.db`（`expressions` 表 status=`gem`/`enhanced`）。该文件仅为管道中间产物，落库后以 DB 为准。未验证 DB 有表达式，不得声称步 4 成功。

### 引擎的 skill 目录解析（2026-09-26 审计重写，排障必读）

引擎读**两份 SKILL.md 拼进 LLM prompt**，解析顺序为
**`WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR`（env）> `skill_roots` 候选（主安装位 → 仓库兜底）> 内嵌 legacy 兜底**
（`pipeline_paths.py::_resolve_skill_dir`）。跑批时会在 stdout 打印一行
`[skill-doc] <label>: OK|MISSING (N 行) dir=… source=…`——**排障先看这行**。

- 实测（本机）：两者都解析到 `~/.claude/skills/...`（FI 111 行 / dfe 322 行），内嵌副本**平时不生效**。
- ⚠ **历史坑**：内嵌 dfe 目录没有 `SKILL.md`，而 `read_text_optional()` 失败返回**空串** →
  顶层 322 行文档曾**从未进入 prompt** 且完全静默；内嵌 FI 的 SKILL.md 曾停在 2026-08-22 的 49 行旧稿。
  两者均已修，并由 `tests/unit/test_gem_skill_paths.py` 守护（修复入口
  `python tools/sync_gem_embedded_skill.py --apply`）。
- 若看到 `MISSING` 或 `source=embedded:legacy` → 立刻停下排查（prompt 会退化为缺该 skill 指导），
  不要当成正常。

## 失败分支

| 现象 | 处理 |
|---|---|
| GEM 未入库 | 先按 `--status <task_id>` 查后台任务，确认失败才回退，不要手写脚本 |
| 候选不足 | enhance / 扩组合；仍不足则换数据集 |
| `401 Incorrect authentication credentials` | 凭据/配置问题，不是管道逻辑问题 |
| `[skill-doc] … MISSING` 或 `source=embedded:legacy` | 引擎没解析到权威 SKILL.md → prompt 会缺该 skill 指导。先查 `WQB_FI_SKILL_DIR`/`WQB_DFE_SKILL_DIR` 与安装位，再跑 `python tools/sync_gem_embedded_skill.py --apply` |
| 缺 config 字段 | run.py fail-fast 并打印缺失键 |
| 输出为空或非法 | 核对 dataset 与 `data_type` 是否匹配、算子过滤条件是否过严 |
| 无 priors 快照 | 先跑 `workflow_campaign(stage="S6", subcommand="assemble-priors")` |

## 反模式

- 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽。
- 把 `final_expressions.json` 当真相源。
- 直接把 `brain-feature-implementation` 当主链入口（它在本管道内部）。
- 手写 PowerShell/requests 替代 `workflow_gem`。
