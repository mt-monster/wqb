---
name: brain-make-some-gem
layer: L2
description: "S2 概念优先的 GEM 表达式生成引擎：标准入口是 workflow_gem，本 skill 写引擎契约（priors / ideas 注入、LLM 通道与凭据前置、产物与落库核对）和排障。要为某 region / dataset / delay / universe 生成候选表达式，或排查 GEM 失败（no meta.json / 402 / [skill-doc] MISSING）时使用。触发词：生成表达式 / 跑 GEM / 概念优先生成 / final_expressions。"
last_verified: 2026-10-06
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__*
---

# brain-make-some-gem（S2 表达式生成引擎）

## 职责边界

- **本 skill 负责**：**S2 唯一主链生成器**——概念优先 GEM，产出候选表达式（`final_expressions.json` → `expressions` 表，status `gem`）。写引擎契约与排障；**不是编排器**（编排 = `wq-brain-ra-pipeline` 步 4）。
- **本 skill 不做**：不做门禁、不回测（S3）、不判提交；`build-wave` 只去重 / 分桶 / 骨架配给，**不产表达式**；**不写 priors 快照**（唯一写入方 = `assemble-priors`）。
- **上游 / 下游**：上游 = `priors_snapshot_<region>` + S1 `s1_<ds>_d<delay>`（ideas / 字段池）；下游 = 步 5 门禁——调**一个入口** `tools/wave_gate.py`（节点 `wave_gate`；内含闸 1–8、体检硬门、SEM、PF）。**不要**再手工串「`check_batch` → `check_expr_against_inspect` → 闸 1–5」（`check_batch` 已不是门禁）。
- **共享产物约定**：`priors_snapshot_<region>` 本 skill **只读消费**。agent 在**每次开生成前先跑一次** `workflow_campaign(stage="S2", subcommand="assemble-priors")`（与 RA 步 4 同一条；`stage` 只是标签，路由按 subcommand 走）。快照过期检查只 WARN、不阻断，**不得据此认为「已确认安全」**——旧先验会让本波沿用过期 win / dead（GBR 实证落后 8 天）；刷新责任归 RA 步 9。

## 标准调用与返回

```
mcp__wq-brain-http__workflow_gem  region=$REGION  dataset_id=$DS  delay=$DELAY  universe=$UNIVERSE  data_type=$DTYPE
```

- `data_type` 必须与 S1 `get_datafields` 确认的 MATRIX / VECTOR / GROUP 一致（传错 = 整批类型不匹配）。GROUP 入口只用于网络 / 行业等分组轴，须给出已解释的分组概念与实际数值信号，禁止把类别编号的大小直接当收益预测。
- **可省略**：`ideas_file`（S1 ledger 的 `source` 不属模板渲染时自动注入，显式传入覆盖；规则见 [`brain-data-feature-engineering`](../brain-data-feature-engineering/SKILL.md)「两条产物路径」）；`priors_file`（缺省走 DB 快照，`priors_from_db=True`，**缺快照即 fail-closed**）；`pipeline_mode`（缺省 `phased`）。
- MCP 工具只暴露上面这些与 `detached` / `launch_only` / `console` / `data_category` / `instrument_type` / `dry_run`；`require_operators` / `require_count` / `batch_size` / `prod_first` 只在节点上，走 `workflow_execute(node="gem", params={…})`。
- **返回**：`success` / `expression_count` / `final_expressions_path` / `quality_estimation` / `mode_b_required` / `steps[]`。异步（`detached` 缺省 True）时用 `workflow_task_status(prefix="gem")` 轮询。
- **`mode_b_required = true` 怎么办**：它是**提示**——零配额的质量预估（`tools/quality_predict.py`，wave_gate 也用它，只作建议性标注、不判 FAIL；刻度在历史上失准）认为有候选 `EXPECTED_BLOCK`，或开了 `prod_first` 且有字段族 prod ≥ 0.7。处置：**照常进步 5 门禁**（不据它丢候选、不据它判死）；把原因写进本波 `key_findings`，步 7 走 Mode B 想法层（换信号概念 / 字段组合；`workflow_execute(node="modeb_improve")`），**不做同族参数变体**。探针 / 修复批用 `wave_gate.py --batch-type probe|repair` 跳过 qp 标注。

## 前置：LLM 通道与凭据（GEM 是唯一会调外部 LLM 的引擎）

| 项 | 要求 |
|---|---|
| **LLM 通道** | Moonshot（OpenAI 兼容 SSE，缺省模型 `kimi-k2.6`）。密钥 = 环境变量 `MOONSHOT_API_KEY`（优先）或 `config.json` 的 `moonshot_api_key`；端点 `MOONSHOT_BASE_URL`。**给了 `ideas_file` 就不调 LLM、不需要密钥** |
| **BRAIN 账号** | 环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（标准名，优先；旧别名 `BRAIN_USERNAME` / `BRAIN_EMAIL` / `BRAIN_PASSWORD` 仍认）→ 缺才读 `config.json` 的 `brain_email` / `brain_password` |
| **`config.json`** | 节点在**解析到的 skill 目录**（安装位优先，不是仓库副本）的 `scripts/headless_runner/config.json` 找它，缺则 `check_config` 失败；模板 = 同目录 `config.example.json`。**用户自建**，已 `.gitignore`、不参与 sync；**agent 不读、不写、不打印它**，缺了就停下让用户建 |
| **症状** | 缺键 → `Missing required config fields: <键名>`（只报名字）；`401` = 鉴权失败、`402` = 余额不足、`403` = 无权限——都是**不可重试**错误，会直接带绕行指引抛出；**干跑（`dry_run`）只验证命令构建，验证不了 LLM 可达性 / 余额**，`402` 时也显示 OK；启动会打印 `[cred] BRAIN 凭据来源=… ；LLM 密钥来源=…`（只打来源，不打值） |

## 概念优先铁律（与 RA 步 4 同源，此处不复写阈值）

1. **机制 → 1–2 个具体字段 id → 一个 Implementation Example**。禁止「每个字段套 `rank`」式枚举。
2. **必须带 priors**：默认 DB 快照直读（fail-closed，无快照即报错，不静默无 priors 运行）；`priors_file` 仅作显式覆盖 / 降级兜底。（RA 旧硬约束「必须带 `priors_file`」已过期。）
3. **引擎实际消费的 priors 键**（`economic_priors.compact_priors_text`）：`wins`（≤ 6）、`dead_ends`（≤ 12）、`region_context`（`tier` / `settings_proven` / `key_notes` ≤ 4）、`skeleton_field_matrix`（有效 ≤ 6 / 死 ≤ 8 / 正交提示 ≤ 4）、`gate_priors` 的 `by_operator_count` / `by_field_family` / `avoid`（`by_decay` / `by_neutralization` 是仿真设置，**不进 prompt**，由步 6 改写设置）。旧文说「只消费 `wins` / `dead_ends` 两个键」是错的。
4. 只用标准时间窗口 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260；其他窗口须给解释或实测证据（预闸会把 20 / 60 / 250 等别名到最近标准窗）。
5. 取骨架前必查 `KB/community_tpl_kb` 的 `ghost_operator_advisory`，先做幽灵算子替换再进批，否则整批 ERROR / CANCELLED。
6. **复杂度预算**：默认 2–5 个算子，8 个概念里至少 3 个 ≤ 4 算子（859 条过闸样本：算子数 p25 = 3 / 中位 5 / p90 = 12，46% 的过闸者只有 ≤ 4 个算子）。**不靠加腿修闸**（CLAUDE.md「禁止混信号调参」、决策表 D3）：多组件概念的每个组件必须写明**经济角色**——条件 / 分组 / 残差 / 同源对偶价差（RA 步 7 §7.7.2 的允许形态）；「补它以修 `sub_universe_sharpe` / `2Y_sharpe` / `concentrated_weight`」**不是**理由（CW 修法顺序看 D6；margin 是数据集属性，补腿修不了）。反例：`add(rank(A), rank(B))`、`0.4*rank(A) + 0.6*rank(B)`（闸 5 拦）。
7. **多样性按语义维度判，不按算子类别**：≥ 3 个不同 Expected Exposure、≥ 3 个字段族、≥ 2 个分组轴、≥ 2 个时间尺度。旧规则「每波 ≥ 1 个 Logical 算子」已废除（`if_else` 在过闸者中仅 5.1%，`group_rank` 占 32.0%、`vec_avg` 12.6%）；Logical 类算子只在**事件型数据集**（有真实事件时点）才合适。**但闸 6 的批级契约仍在**：`diversity_audit_latest.next_round_injections` 的 `required_operators`（每批 ≥ `per_batch_min_operators` 条命中）与 `skeleton_quota` 由 `build-wave` **确定性注入**、闸 6 强制。所以 GEM 按语义多样性生成，**不为算子配额装饰**；`require_operators` / `require_count` 在 prompt 里只是**软提示**（引擎自己写明「权威保证是 build_wave 的契约骨架注入」）。`batch_simulator.py`（sim-alphas）与 `build_wave.py` 的 `--enhance-diversity` 缺省都是 `never`（不改写表达式）。
8. **Expected Exposure 声明会被验证**：回测后以 `risk_neutralized_sharpe` 核对。它 ≈ 0 或为负而 raw sharpe 高 ⇒ **该概念**就是那个暴露本身，判 `dead_end` 且禁止调参（判死粒度 = 概念，不是数据集）。

## ideas、预闸与两种模式

- **ideas 注入**：`source ∈ {feature_engineering_node, standalone, standalone_v2}` 的模板渲染文档**不自动注入**（注入后本管线零 LLM 调用、整波退化为模板展开）；其余 `source`（`manual` / `s2_nested`）且 `ideas_md_path` 存在、`pipeline_mode ≠ skeleton` → 自动注入；显式 `ideas_file` 覆盖。**手写 ideas ≠ 手写表达式**——概念块格式见 FE 的「第 4 步」，是绕开 LLM 故障的合法通道。
- **社区模板**：`tools/kb_templates.py --emit-ideas` 产出的是 **JSON**（`source: "kb_templates.py"`，不是 ideas markdown，也不在模板渲染源清单里），**不能直接当 `ideas_file`**；只作人读参考，或由 agent 按概念块格式改写成 `manual` ideas 后再注入，入批前必过 ghost advisory。
- **预闸**：`pipeline_pregate.py` 在落盘前自动处理（quantile 归一 / hump 命名参数 / bucket range / 区域非法字段与 group / JPN 的 `ts_*(vec_*)` / 非标窗口别名 / 加权混合毒模式 / 同骨架变体封顶 12）。**规则表只在一处维护**：RA [`step4-generation.md`](../wq-brain-ra-pipeline/references/step4-generation.md) §4.4（自动动作 / agent 动作对照）；步 5 门禁只作兜底。
- **两种模式**：**family mode**（`--pipeline-mode phased`，缺省）用 `wq-brain-campaign-toolkit/config/template_families.json` 的机制族模板，LLM 按 priors 概念绑定、`implement_idea` 展开占位符；**skeleton mode**（`skeleton`）由 `trailSomeAlphas/skeletons.py` **代码组装**（LLM 只输出结构化 JSON，语法合法性构造保证），不消费 ideas 文件。字段可分层（signal / metadata / scale 清晰）→ skeleton；需要族级机制叙事 → family。概念位分类学（dfe 8 问 ↔ GEM 概念位 ↔ hypothesis 12 类）见 [`concept-taxonomy-map.md`](../wq-brain-ra-pipeline/references/concept-taxonomy-map.md)——「概念位」是生成时的分类，与**波内配额**、**并发令牌**是三个东西。
- 显式 `ideas_file` 的表达式保持经济方向与条件；不得通过替换外层算子强制制造多样性，结构多样性由下游门禁评审。

## 直接命令（仅当 workflow 节点不可用）

参数、凭据来源与示例见 [`scripts/headless_runner/README.md`](scripts/headless_runner/README.md)（在仓库根用 `$WQ_PY` 运行，**不需要 `cd`**）。要点：`--priors-from-db` **必须带区域值**；用绝对路径的 `--tasks-dir`（仓库战役用 `<仓库根>/logs/_async_tasks`）；`--detached` 后台启动、`--status <task_id> --tail-lines 60` 查状态；`--dry-run` 只校验命令。**看实时输出**：默认用 `--watch <task_id> --tasks-dir <root> [--from-start]`（对在飞任务 tail -f，Ctrl+C 只退跟随）；`--detached --console`（= `workflow_gem(console=True)`）**Windows 专有**——另弹真实控制台窗口（`DETACHED_PROCESS | CREATE_NO_WINDOW` 下终端天生看不到输出），代价是任务寿命绑在窗口上：关窗口 = 杀任务，phased 无断点 = 整波丢弃，只在人盯盘时开。

## 产物契约与落库核对

- `final_expressions.json` 由 `gem` 节点 `_find_final_expressions` 按序查三段：① **新稳定路径（首选）** `<仓库根>/data/gem_runs/{DATASET}_{REGION}_delay{DELAY}/final_expressions.json`（`WQB_GEM_DATA_ROOT` 可覆盖）；② 旧深嵌套位 `scripts/trailSomeAlphas/skills/brain-feature-implementation/data/…`（历史兜底，**勿再用于新跑**）；③ 旧备用位 `scripts/headless_runner/outputs/…`（同）。GEM 自生成的 ideas 报告写 `GEM_REPORT_ROOT` = `data/gem_runs/output_report/gem_{REGION}_delay{DELAY}_{DATASET}_ideas.md`（2026-09-26 前写在 skill 树内部，造成 16 个产物文件混入仓库）。
- **`final_expressions.json` 不是真相源**——战役产物只入 `data/wqb.db`：`run_pipeline.py` 收尾时**自己**把通过校验的表达式写进 `expressions`（`status=gem`，wave = `s2_<DS>_d<DELAY>`），并打印 `[db] expressions/<REGION>/<wave> n=… status=gem`；`workflow_gem` 节点再做来源标注（`gem_<mode>`）、质量预估与 `mode_b_required`。**核对：`mcp__wqb-db__list_expressions(region, wave)` 有行——看不到行，不得声称步 4 成功。** 后续 `workflow_campaign(stage="S2", dataset, wave=$W)` 才把它们选进战役波。

## 引擎的 skill 目录解析（排障）

解析顺序 **`WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR`（env）> `skill_roots` 候选（主安装位 → 仓库兜底）> 内嵌 legacy 兜底**（`pipeline_paths.py::_resolve_skill_dir`）。跑批时 stdout 会打印 `[skill-doc] <label>: OK|MISSING (N 行) dir=… source=…`——**排障先看这行**。

- ⚠ **更正**：这两份 `SKILL.md` **正文从不进 LLM prompt**（旧文写反了）：`build_prompt` 只用 dfe `SKILL.md`「是否非空」决定附不附一句固定的 8 问提示，FI 那份完全不用（AST 测试钉死）。所以文档篇幅与措辞**不影响**生成质量；`MISSING` / `embedded:legacy` 的真正含义是**skill 目录解析异常**——FI 目录同时承载 `ace_lib` / `validator` / `implement_idea` 脚本，解析错了脚本也可能是旧的。
- 内嵌副本平时不生效；顶层与内嵌的同名文件必须逐字节一致（FI `SKILL.md` + dfe 的 `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md`），漂移由 `tests/unit/03_gem/test_gem_skill_paths.py` 守护，修复 `python tools/sync_gem_embedded_skill.py --apply`。**维护警示**：改 `scripts/` 须回归 GEM 全链路，`validator.py` 与 `alpha-expression-verifier` 权威版四处一起改。

## 失败分支

| 现象 | 处理 |
|---|---|
| **「no meta.json within 90s」**（`GEM_META_TIMEOUT_SEC`） | **先查 LLM 通道，不要重试**：`402 Insufficient Balance` 会被这句误导性报错吞掉，干跑也验证不了。绕行 = 手写 `manual` ideas 走 `ideas_file`（完全跳过 LLM） |
| **`402 Insufficient Balance`** | LLM 余额不足，不可重试；由用户充值，或按上一行绕行 |
| **LLM 通道不可达**（超时 / 连接失败 / `MOONSHOT_BASE_URL` 写错） | 引擎按 `MOONSHOT_RETRIES`（缺省 2–3 次）退避后抛错；查网络与端点；同样可绕行 |
| `401 Incorrect authentication credentials` | 凭据（BRAIN 或 Moonshot 之一）不对，不是管道逻辑问题；看 `[cred]` 行的来源，由用户改环境变量 / `config.json` |
| `config.json not found`（`check_config`）/ `Missing required config fields` | 用户按 `config.example.json` 建 / 补；agent 不代填凭据 |
| GEM 未入库（没有 `[db] expressions/…` 行，或 `list_expressions` 为空） | 先 `workflow_task_status(prefix="gem")` / `--status <task_id>` 查后台任务，确认终态失败才回退；不要手写脚本 |
| 候选不足 | **显式扩容 / 分波 / 换数据集**；**不补参数变体凑数**（与 RA 步 4 选波清单一致） |
| `[skill-doc] … MISSING` 或 `source=embedded:legacy` | 见上节：skill 目录解析异常。查 `WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR` 与安装位，`python tools/sync_skills.py --check` |
| 无 priors 快照 | 先 `workflow_campaign(stage="S2", subcommand="assemble-priors")` |
| 输出为空或非法 | 核对 dataset 与 `data_type` 是否匹配、算子过滤条件是否过严 |

## 反模式

- 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽。
- 把 `final_expressions.json` 当真相源；没核对 `expressions` 表就说步 4 成功。
- 直接把 `brain-feature-implementation` 当主链入口（它在本管道内部）。
- 手写 PowerShell / requests 替代 `workflow_gem`；把凭据写进命令行参数。
- 读取 / 打印 / 提交 `config.json`。

## references

| 文件 | 何时读 |
|---|---|
| [`reference.md`](reference.md) | 查目录结构、`run.py` 参数、`workflow_gem` 与节点的参数差异时 |
| [`examples.md`](examples.md) | 想看触发例与期望行为（含 `402` 场景）时 |
| [`scripts/headless_runner/README.md`](scripts/headless_runner/README.md) | 手工运行 `run.py`、配置凭据来源时 |
| [`scripts/trailSomeAlphas/skills/README.md`](scripts/trailSomeAlphas/skills/README.md) | 弄清内嵌兜底副本与守护测试时 |
