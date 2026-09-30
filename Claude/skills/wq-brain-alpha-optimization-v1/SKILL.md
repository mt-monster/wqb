---
last_verified: 2026-10-01
name: wq-brain-alpha-optimization-v1
description: "现有 WorldQuant BRAIN alpha 的两模式改进器：Mode B（想法层——换信号概念/字段组合，含卡闸后的组合腿救援）→ Mode A（参数层——冻结核心想法，8 候选严格批调 decay/窗口/中性化/truncation）。用户要求改进/优化某个 alpha ID、修复失败的提交测试项（含 IS_LADDER_SHARPE），或候选已按资格判定表（references/mode-b-qualification.md）值得继续改时使用。prod 相关性墙按 RA 决策表 D0-P 处置，本 skill 不承诺把 PROD 压到某个数。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - Write
  - mcp__wq-brain-http__*
  - mcp__wqb-db__get_salvage_pool
user-invocable: true
---

# WQ BRAIN Alpha Optimization V1（两模式）

## 职责边界

- **本 skill 负责**：**动手改**现有 alpha——Mode B 想法层（换信号概念 / 字段组合 / 组合腿救援）→ Mode A 参数层（decay / 窗口 / 中性化 / truncation）；**会产生新变体并回测**。
- **本 skill 不做**：不做提交判定（`tools/submit_verdict.py`）；不做只读的阈值 / 失败原因查询（→ `brain-how-to-pass-alpha-test`）；不做稳健性审计（→ `brain-alpha-robustness`）；**不承诺把 PROD 相关性压到某个数**——prod 墙的处置只有 RA 决策表 [D0-P](../wq-brain-ra-pipeline/references/decision-table.md) 一张表，本 skill 只承接其中「已 eligible 且有 salvage 辅助腿」的组合腿救援与「踩线带 1 次结构性尝试」。
- **上游 / 下游**：上游 = S4 判「可改」的候选（`brain-how-to-pass-alpha-test` 定位失败项，下节判资格）；下游 = `brain-calculate-alpha-selfcorr-quick` →（可选）`brain-explain-alphas` → `brain-alpha-robustness` → `tools/submit_verdict.py`（提交前否决闸；放行须用户确认，见 `worldquant-submit-alpha`），**不直接提交**。

**运行环境**：所有 Python 命令用 MCP venv（`$WQ_PY`），不要用系统 Python。

## 入场：先做资格判定

候选值不值得继续改，只看一张表：[`references/mode-b-qualification.md`](references/mode-b-qualification.md)（主闸 + 旁路 A–E + 判死线；数值出自 `mode_b_config`，别处不手抄）。判定用同一个函数的 CLI（只读），把**全部**指标喂进去（judge 节点只喂 6 个，A / B / D 旁路在那里恒不命中）：

```bash
$WQ_PY tools/mode_b_qualify.py evaluate --region <REGION> --sharpe <S> --fitness <F> --two-year-sharpe <2Y> \
    [--robust-sharpe ..] [--margin-bp ..] [--turnover ..] [--returns .. --returns-median ..] [--prod-corr .. --other-dims-pass]
```

| 结论（`result.verdict`） | 本 skill 的动作 |
|---|---|
| `main_gate` | 进 Mode B 通用步骤 B1–B5 |
| `bypass` | 进 Mode B，**首选修法 = 该旁路绑定的 `mode_b_action`**（结果里给出） |
| `no_qualify` | 不进改进；候选留在 near / salvage 或结束；**不写 `dead_end`** |
| `dead_end` | 不改；候选级封存流程见 RA [step9 §9.5](../wq-brain-ra-pipeline/references/step9-writeback.md)（先 `forum_recon`，再 `seal_dead_end`） |

## 模式调度与止损（一条规则）

- **先想法后参数**：Mode B 决定「改什么信号」，Mode A 只在核心想法已验证后做参数收敛。进 Mode A 的线（Stage B）：最优候选 Sharpe > 1.40 且 Fitness > 0.90（[`reference.md`](reference.md) §6.5）。
- **止损阶梯**（同一 alpha 累计，先到先停）：

  | 累计想法周期（B1–B5 走一遍 = 1 个） | 仍卡在结构性闸门 → |
  |---|---|
  | 第 3 个 | 候选 `eligible` → 组合腿救援（下文）；不 `eligible` → 结束该候选 |
  | 第 5 个 | 判死回写（先 `forum_recon`、再 `seal_dead_end`），换字段回 S1 |
  | 累计试过的结构 > 10 种仍无果 | 换数据集回 S0（阶段定义见 [`INDEX.md`](../INDEX.md) 流水线表；数据集探索见 `brain-dataset-exploration-general`） |

  没有「精力占比」——只按周期数与结构数计；每个周期的调用预算见下（不按分钟计）。

## Mode B：想法层改进（B1–B5）

**触发**：Sharpe 卡在低水平、负年份、与 book 高相关等结构性弱点；或用户明确要「改进想法 / 换概念」。

| 步 | 做什么 | 预算 |
|---|---|---|
| **B1 收集** | `get_alpha_details`（表达式 / 设置 / 指标 / `is.checks`）；相关性读 `alphas.prod_correlation`，缺才 `check_correlation`（阻塞轮询 ≤ 60 min、账号级单并发，见 [`prod-corr-avoidance.md`](../wq-brain-ra-pipeline/references/prod-corr-avoidance.md) §1）。记录失败项与对应 `mode_b_action` | ≤ 2 次平台调用 |
| **B2 评估核心字段** | 字段 `type`（VECTOR / EVENT）与 coverage；用 `brain-datafield-exploration-general` 的评测在中性设置下摸清数据性质（如「季度稀疏 → 优先 persistence 类想法」）。**EVENT 字段会让整个 multi-sim 批次失败**（如 `winsorize` 报 `does not support event inputs`），闸 8 会拦：移除 EVENT 字段或先单条探针 | 每字段 1 次评测 |
| **B3 提想法级改进** | 查平台文档 / 社区技巧；arXiv 概念检索（**外发边界见下**）；头脑风暴 4–6 个变体，**每个只动 1–2 个概念**；变体所用算子对照 `known_ops`（[`reference.md`](reference.md) §8 标注了哪些未核验） | 4–6 条变体 |
| **B4 仿真对比** | 变体**先过 `ghost-audit` 与 `wave_gate --batch-type repair`**（命令见 Mode A 校验层），再 `create_multi_simulation`（2–8 条；multi 失败退并行单仿）；收割入库（`harvest_multisim_alphas` → `wqb-db harvest_multisim_results`）；按 Fitness / Sharpe 排名，查 sub-universe 与逐年一致性，负信号可翻转 | 1 个 multi 批 |
| **B5 验证迭代** | Top 变体做相关性检查。失败 → 回 B3（受上面的止损阶梯约束）；通过 → 交 Mode A 收敛，然后走下游链，**不直接提交** | — |

**arXiv 概念检索的外发边界**（`scripts/arxiv_api.py`，用法见 [`arXiv_API_Tool_Manual.md`](arXiv_API_Tool_Manual.md)）：

- 查询词发往 `export.arxiv.org`：**只发通用关键词**（如 `abs:"post-earnings-announcement drift"`），**不发**未公开表达式、数据集名 / 字段名、alpha id。
- `--concepts` 只用本地规则层抽概念，不外发。**`--llm` 会把检索到的公开论文标题 / 摘要发给第三方 LLM**（缺省 `api.deepseek.com`、模型 `deepseek-v4-flash`，可用 `--llm-base` / `--llm-model` 改）；密钥只读进程环境变量 `OPENAI_API_KEY`，或 skill 目录内被 gitignore 的 `scripts/.arxiv_llm.env`（`sync_skills` 不会复制它）；缺密钥自动降级规则层。**不要把密钥写进命令行、文档或对话。**
- 运行：`$WQ_PY Claude/skills/wq-brain-alpha-optimization-v1/scripts/arxiv_api.py "<query>" --concepts [--llm] -j <region>_<topic>_concepts.json`。`brain-explain-alphas` 用同一份脚本（不再各留一份拷贝）。

## Mode A：参数层优化（8 候选严格批）

对现有 alpha 做端到端参数优化：严格预检、结构化迭代、强制低相关检查。全部规则（硬规则 / 阶段 / 主题配额 / 执行流）见 [`reference.md`](reference.md)。

**硬规则**：

1. 冻结基线 alpha 的核心字段与数据集，后续轮次不得替换。
2. **任何仿真之前，每个候选必须先过本地校验与门禁**（见下）。
3. 每轮恰好 8 个候选表达式。
4. **PPA** 候选的 `operatorCount` 上限 8（平台 Power Pool 规则）；REGULAR 无此上限，复杂度纪律见 `brain-make-some-gem`「复杂度预算」。平台返回的 `operatorCount` 是最终裁判。
5. Stage A（最优候选未达 Sharpe > 1.40 且 Fitness > 0.90）禁止纯微调，只能做结构化升级（定义见 `reference.md` §6.5 / §7）。
6. 全部检查零 FAIL 的候选立即做 PROD 相关性检查，读数按 D0-P 处置。
7. **结果入库、不写自建文本文件**：批回测结束后确认 `backtest_results` 已入库（`harvest_multisim_alphas` → `wqb-db harvest_multisim_results`）；迭代日志（8 槽角色 / 失败项 / next_actions）写在本轮回复里，S6 回写时进 `wave_result.key_findings`（RA [step9](../wq-brain-ra-pipeline/references/step9-writeback.md)）。
8. 校验或仿真失败时只修精确的报错点；不得为过校验而删核心逻辑。

**校验层**（3 段，顺序执行，全过才可仿真）：

```bash
# ① 语法 / 算子元数：alpha-expression-verifier（wave_gate 内含，与闸 1 同源）
# ② 幽灵算子：validate_expressions / preflight_expressions 不查幽灵算子，必须单独跑
$WQ_PY tools/campaign_intel.py ghost-audit --region <REGION> --exprs-file <变体文件>
# ③ 闸 1–9 + SEM：repair 批不做质量预估标注、默认豁免批级多样性
$WQ_PY tools/wave_gate.py --campaign-dir tracking/<REGION> --dataset <主信号数据集> --wave <本 alpha 所属波次> \
    --exprs-file <变体文件> --batch-type repair
```

退出码：`0` PASS / `1` 表达式不合格（改表达式）/ `2` 环境错误（不是表达式问题）。闸的现象 → 动作 → 能否豁免见 RA [step5-gates.md](../wq-brain-ra-pipeline/references/step5-gates.md) §5.2。

**候选批三灯分级**（复用 probe_scoring_v2 原则）：8 候选批的优劣分级可套 `wq-brain-campaign-toolkit` 的 v2 三灯公式（`score_datasets.py --probe-score --from-json` 离线校准，公式见 toolkit `references/probe-scoring-v2.md`）。三条原则：① 联合评估在最强单点，禁止跨候选 OR 拼出不存在的理想探针；② 2Y 红灯仅当平台返回值判定（`two_year_sharpe=None` 不算败）；③ tvr 结构性墙——全部候选同侧出界时绿灯封顶黄灯（LOW → trade_when / decay 拉 tvr；HIGH → 拉长窗口压 tvr）。

## prod 相关性墙 → D0-P；组合腿救援是它的「唯一例外」

prod 读数怎么处置只看 RA 决策表 [D0-P](../wq-brain-ra-pipeline/references/decision-table.md)（< 0.60 扩；0.60–0.70 不扩、当天进步 8；0.70–0.75 只 1 次结构性尝试；≥ 0.75 或尝试失败 → `dead_end`）。本 skill 不另立反馈循环。

**唯一例外**（D0-P 明写）：候选已 `eligible`（[资格判定表](references/mode-b-qualification.md)：主闸或旁路），且 Mode B 常规改进 3 个周期仍被结构性闸门卡住，才进入组合腿救援。**救援不是重写主信号**：保留强主腿 + 从 salvage_pool 取补强辅助腿做合规改造。

**弹药查询**（`mcp__wqb-db__get_salvage_pool`；参数 `region` / `boost_dim` / `exclude_dataset` / `min_sharpe`，全可选）：

| 卡点 | 参数 |
|---|---|
| LOW_2Y_SHARPE / 2Y 墙 | `boost_dim="boost_2y"` |
| TVR 墙（turnover 出界） | `boost_dim="boost_tvr"` |
| CONCENTRATED_WEIGHT / sub-universe | `boost_dim="boost_cw"` |
| 信号弱（sharpe / fitness 不足） | `boost_dim="boost_sharpe"` |
| PROD / SELF 相关 ≥ 0.7 | `exclude_dataset=<主信号数据集>`（优先跨数据集正交腿） |
| 只要强腿（可选） | `min_sharpe=1.0`（与入池线 `combo_sharpe_min` 缺省 1.0 同口径；缺省不传） |

入池对象是 S4 `review_wave.py --write-ledger` 幂等写入的 combo 候选 + near 补充（入池线 vs 动用线的区别见资格判定表 §5：**入池宽、动用严**）。

**构造纪律**（路线 A：禁加权混合）：

1. 主腿冻结；辅助腿 ≤ 2 条，**必须取自 salvage_pool 返回条目**（禁止凭空另造腿）。
2. **禁止一切加权混合 / 等权相加 / 中缀 `+` / 权重网格**（闸 5 结构判定 block）。仅允许两种合规形态：
   a) **结构交互式**（首选）：辅助腿只能以「条件 / 分组轴 / 残差化 / 协动对象 / 同源价差」五种方式之一入场——形态族 F1–F6、**可检判据**与卡点映射见 [`references/structural-interaction-forms.md`](references/structural-interaction-forms.md)（跨数据集的辅助腿只能走前四种，不得走 F1）。
   b) **SuperAlpha combo**（组件级）：本区已有 ≥ 10 颗 ACTIVE REGULAR 时走 `wq-brain-superalpha` 的 selection + combo（平台机制，不做表达式层加权）；SUPER 的 prod 闸与提交路径以该 skill 为准。
3. 每条候选溯源标记 `combo_rescue_from_<本alpha_id>_with_<salvage_id>_<形态>`，写入本轮日志。
4. 验证走 Mode A 批纪律：8 候选严格批 → 校验层三段 → multiSim。

**验证与兜底**：过闸（全 checks PASS + prod 读数按 D0-P 可放行）→ 走标准下游链（见「职责边界」），不直接提交；池内无匹配（返回空 / 全同数据集）或组合 1–2 轮仍 FAIL → 判死回写（先 `forum_recon`，再 `seal_dead_end` 沉降残值），禁止无限烧配额；残余线索写 ledger salvage 字段留痕。

## 过拟合与稳健性

不在本 skill 内做：参数敏感性、子宇宙一致性、逐年一致性、概念对照的**判据与阈值只有一处**——[`brain-alpha-robustness`](../brain-alpha-robustness/SKILL.md)（同库 L4，S4 → S5 必经）。Mode A 收敛后直接交给它；本 skill 只保证「回测前后每个候选都留有逐年 / sub-universe 读数」。

## 预期产出

Mode B → Mode A 迭代，直到出现**至少一个达标候选**，或触发上面的止损阶梯（判死回写）。

「达标」= 平台全部检查 PASS（`Failed RA == 0`，口径见 RA [`webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md)，含 `IS_LADDER_SHARPE`）**且**满足内部闸线（`wqb.config.GATES_INTERNAL`；Sharpe / Fitness / Turnover 等数值以 config 为准，**不在此复写**），并且 PROD 读数按 D0-P 可放行。

## 渐进式文档

- Mode A 完整规则、主题配额、逐步执行流：[reference.md](reference.md)
- 示例（直接优化 / Stage A / 负信号翻转 / 校验合同 / 迭代日志）与场景卡：[examples.md](examples.md)
- Mode B 资格判定表：[references/mode-b-qualification.md](references/mode-b-qualification.md)
- 组合腿救援形态库：[references/structural-interaction-forms.md](references/structural-interaction-forms.md)
- arXiv 工具：[arXiv_API_Tool_Manual.md](arXiv_API_Tool_Manual.md) + [scripts/arxiv_api.py](scripts/arxiv_api.py)
