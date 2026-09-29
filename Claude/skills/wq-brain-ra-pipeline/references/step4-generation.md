# 步 4（S2）细则：选波——概念优先生成

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 4。生成器 = **`workflow_gem`（强制）**；`build-wave` 只去重 / 分桶 / 骨架配给，**不产表达式**。增强 = 对已有 idea 的变体扩展，经 priors / ideas 注入实现。
> 引擎实现与 CLI 参数见 [`brain-make-some-gem`](../../brain-make-some-gem/SKILL.md)。可选：`workflow_campaign(subcommand="diversity-extract")` 做方向参考，**不替代** GEM，不强制先行。

## 4.1 生成前的硬约束与准则

术语：**波内配额**（一波里表达式的配比，如「跨金字塔 ≥ 2」；旧称「七槽」）≠ **并发令牌**（Token-Bucket，`slots=7`）≠ **批**（一次 `create_multi_simulation`，8 条子模拟）——见 [`GLOSSARY.md`](../../GLOSSARY.md)。

| # | 约束 | 类型 | 说明 |
|---|---|---|---|
| 1 | **先读 win 层**（= priors 的 `wins`：论坛模板 / `region_kb.win_recipes` / `registry_empirical` win 层 / `template_kb` validated / active alpha，来源与名额见 [`assemble-priors-internals.md`](assemble-priors-internals.md)）；有胜绩则本波**至少 2 个波内配额位按机制换腿**（此前「≥2 槽」与「≥1 win 换腿」两个数已合并为这一个） | 准则 | 已验证配方**只指「信号概念 + 设置」，不再记录混合比例**。例：EUR 的胜绩 = 「慢 MODEL 残差作 group / bucket / 条件，快 PV 作主信号」，**不是**「0.4 × 慢 + 0.6 × 快」的加权相加（该形态自 2026-09-13 起被全局禁止，见 [`decision-table.md`](decision-table.md) D3） |
| 2 | **GEM 概念优先**：机制 → 1–2 个具体字段 id → 一个 Implementation Example；禁止「每个字段套 `rank`」 | 硬 | `priors_file` **默认无需**（GEM 从 DB 快照 `priors_snapshot_<region>` 直读）；仅 DB 快照缺失时显式传 |
| 3 | 有信号：`\|Sharpe\| ≥ 1.0` / `PASS_CHEAP`（= 过 ① IS 廉价闸，**不等于可提交**，见 INDEX「闸门阶梯」）/ registry 标明有 IS 但卡 prod；复合后 `\|S\| < 0.5` 不再入选波池 | 准则 | |
| 4 | 波内配额：≥ 2 跨金字塔；弱探针最多 1 个位且仅当本波尚无近闸字段 | 准则 | 「弱探针 / 组合批」：弱探针 = 只为取证的窄批；组合批 = 每条都带完整机制的批 |
| 5 | 两个数据集的想法：能合并 catalog 就合并；否则拆成**慢腿批**（季 / 月频基本面）+ **快腿批**（日频价量）同波对照，不停挖 | 准则 | 与「优先单数据集 atom」不冲突：这是**已经决定做跨集**时的落地方式，不是鼓励跨集 |
| 6 | **时间窗口有意义**：只用 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260；其他窗口必须给出解释或实测证据 | 准则（预闸别名化，闸 9 只 WARN） | 证据登记位置：该 idea 的 rationale 文字 + 本波 `key_findings` |
| 7–9 | 禁止混信号调参（尤其 `add(A,B)`）、字段角色区分、点塔均匀——**遵守 CLAUDE.md「寻找 alpha 准则」**，本文不复述 | 准则（闸 5 兜底） | |

## 4.2 priors 与 ideas 注入

```
# 确定性组装 priors 并写 DB 快照（priors_snapshot_<region>）；stage="S2" 只是标签，路由按 subcommand 走 campaign.py
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  subcommand="assemble-priors"
```

首选 `assemble-priors` 节点，**勿手写组装**；内部映射（哪些键进 `wins` ≤ 6 / `dead_ends` ≤ 12）见 [`assemble-priors-internals.md`](assemble-priors-internals.md)。

> **取骨架前必查 `ghost_operator_advisory`**（`KB/community_tpl_kb` 键内）：含幽灵 / 未验证算子（sigmoid / ts_entropy / ts_skewness / ts_percentage / ts_decay_exp_window 等）的骨架必须替换为已验证等价算子，
> 或先 `mcp__wq-brain-http__preflight_expressions` 实测，否则整批 ERROR / CANCELLED。这条是**独立必做项**，步 5 失败分支重复引用它。

**`gate_priors` 分流**：`region_kb.gate_priors`（库存实测过闸率）按维度分两路——`by_operator_count` / `by_field_family` 进 GEM prompt（表达式层能作用）；`by_decay` / `by_neutralization` 是仿真设置，**不进 prompt**，由步 6 `pipeline.py run` 的 settings prior 直接改写本波设置。

**ideas 注入规则**：S1 ledger 的 `ideas_md_path` 只有在 `source` 为 LLM / 人工产出（`s2_nested`、手写）时才自动注入 GEM；`source ∈ {feature_engineering_node, standalone, standalone_v2}` 的是确定性模板渲染，注入后 GEM 一行 LLM 都不调——节点与 runner 都跳过这类文档；显式 `ideas_file` 仍可覆盖。

## 4.3 调用

```
# 变量：$DELAY / $UNIVERSE 取自 settings.json；$DTYPE 取自 catalog 的 data_type（VECTOR 比例先用 get_datafields 确认）
# ① assemble-priors 已在 4.2 调过——本波只调这一次（步 9 收尾会为「下一波」再刷新一次，那是另一回事）
mcp__wqb-db__get_ledger_key            region=$REGION  key="s1_${DS}_d${DELAY}"
mcp__wq-brain-http__workflow_gem       region=$REGION  dataset_id=$DS  delay=$DELAY  universe=$UNIVERSE  data_type=$DTYPE  pipeline_mode="phased"
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  dataset=$DS  wave=$W        # build-wave：去重 / 分桶 / 骨架配给（产出波号 $W）
```

`pipeline_mode`：**`phased`（缺省）**；`skeleton` = 代码组装、语法构造保证，用于「需要语法构造保证的骨架填充」；`single` = 一次性 LLM，不推荐。`workflow_gem`（含干跑）的 `priors_snapshot_check` 步在快照缺失或早于 region_kb 等 KB 源时告警。

## 4.4 生成侧预闸：系统自动做什么、agent 还要做什么

`pipeline_pregate` 在 GEM 落盘前自动处理；步 5 门禁只作兜底：

| 预闸规则 | 自动动作 | agent 动作 |
|---|---|---|
| `hump(x, k)` | 改写为 `hump(x, hump=k)`（平台只认命名参数；hump 仍受支持，只是必须命名） | 无 |
| `bucket(rank(x))` 缺 range | 补 `range="0,1,0.1"`；非 rank 输入**丢弃** | 被丢弃的补重生成 |
| 区域非法 group 字段 | 丢弃（`platform_constraints.json` `region_invalid_group_fields`，JPN = sector / subindustry / industry） | 无；非 GEM 来源的表达式靠闸 2b 兜底 |
| 非标窗口 | 按别名表归一（20/21→22、60/63/65→66、250/255→252、500→504、1000→1008、1250→1260）；其余非标窗**只 WARN** | 给解释或实测证据（约束 6），否则改标准窗口 |
| **同骨架换字段变体封顶** | `WQB_GEM_MAX_PER_SKELETON`，缺省 12 / 骨架（JPN analyst_revision_horizons 1026 字段曾渲染出 7538 条几乎全是同骨架换字段） | 触封顶 = 机制枯竭信号，见 4.6 |
| `quantile(x, driver="gaussian"[, sigma=1.0])` | 无损归一为 `quantile(x)`（平台默认 driver；闸 4 ARITY 曾因此 312 次命中） | 无 |
| 加权混合毒模式 | 丢弃（闸 5 同源正则） | 不要靠增删腿修不达标的信号 |

## 4.5 选波实验清单（按实验问题选波）——四种情景

`8 条`不是固定上限；普通探索的 `--size N` 只是**容量**，workflow 不再隐式补精确数量。清单格式、身份检查、延后项审计见 [`selection-plan.md`](../../wq-brain-campaign-toolkit/references/selection-plan.md)。

| 情景 | 触发条件 | 调用 / 做法 | 核验与产物 |
|---|---|---|---|
| **A 普通探索** | 没有预定实验问题 | `workflow_campaign(stage="S2", dataset, wave)`；`--size N` 仅容量 | 波内表达式已入库（4.7 完成定义） |
| **B 预定实验（配对）** | 要验证某机制 / 基线—反证对照 | 先把「机制 + 基线 / 反证对照」清单写入 ledger `selection_w<W>`，再 `extra_args=["--selection-contract-key","selection_w<W>","--size","<容量>","--enhance-diversity","never","--auto-coverage","never"]`；**条数由清单推导**，容量不足必须**显式扩容或分波**，不得补参数变体凑数 | 落库核验 selected 与无 alpha_id；受保护状态或计划外旧 selected / gated 导致回滚，先核对再显式处理 |
| **C 重建** | 需要按旧清单重跑 | 用清单内 `source_wave` 明确 GEM 源；逐项核验 source_id / 原式 / 来源 / 状态 | 缺机制或被配额挡住即**失败** |
| **D 结果解读** | 回测后（→ 步 7 / 步 9） | S4 / S6 依据**配对证据**决定：有新增机制或对照缺口 → 扩展；强候选 → 有理由的参数敏感性；重复弱变体降低优先级而非永久删除 | `wave_meta` 保留选中 / 延后项及原因；**未选、未回测不能写成 dead_end**；每轮报告「计划 / 选中 / 门禁通过 / 实际完成」与尚未覆盖的问题；指标上升但未达增强资格 → ledger `research_leads_w<W>`（与 near / ready 分开，见 selection-plan） |

旧调用可显式 `--expected-count N` 保留数量检查，但它不证明机制覆盖。

## 4.6 失败分支（症状 → 判据 → 处置）

| 症状 | 判据 | 处置 |
|---|---|---|
| **GEM 报「no meta.json within 90s」** | 先怀疑 LLM 通道：`402 Insufficient Balance`（余额不足）返回的报错是误导性的；**干跑（dry_run）只验证命令构建、验证不了 LLM 可达性，会显示 OK 的假绿** | **先查 LLM 通道，不要重试**。已验证的绕行：手写 ideas md（**手写 ideas ≠ 手写表达式**）→ `--ideas-file` 跑 `Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py`，完全跳过 LLM |
| GEM 未入库 | 后台任务状态非终态 | `mcp__wq-brain-http__workflow_task_status(prefix="gem")` 查任务；确认终态失败才回退，**不要手写表达式** |
| 候选不足 | 波内表达式数 < 计划 | **显式扩容或分波**（enhance / 扩组合）；仍不足换数据集；**不补参数变体凑数** |
| 机制枯竭 / 同质化 | GEM 产出同骨架触封顶，或 win 配方无腿可换 | `tools/forum_recon.py` 取证回补 KB（[`forum-recon-triggers.md`](forum-recon-triggers.md)），模板须先过 `ghost_operator_advisory` 替换，再重跑 GEM |

## 4.7 完成定义

**DB 里有本波表达式**（`mcp__wqb-db__list_expressions(region, …)` 查到 `status ∈ {gem, enhanced, selected}` 的本波条目）。**未验证 DB 有表达式，不得声称步 4 成功。** build-wave 会消费 `methodology_rules` 做配给，但**不替代 GEM**；该 `$DS` 在本区从未跑过 GEM 则必须先跑 GEM。
