---
last_verified: 2026-08-22
name: wq-brain-alpha-optimization-v1
description: "现有 WorldQuant BRAIN alpha 的两模式优化器。Mode B（想法层，70% 精力）：改信号概念/ 字段组合，从 arXiv 引入概念，5 步改进工作流。Mode A（参数层，30% 精力）：冻结核心想法， 在严格 8 候选批中调 decay/窗口/中性化/truncation，含本地校验与低相关提交规则。 当用户要求改进或优化某个 BRAIN alpha ID、修复失败的提交测试、把 PROD 相关性压到 0.7 以下、 或通过包括 IS_LADDER_SHARPE 在内的全部检查时使用。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - Write
  - mcp__wq-brain-http__*
  - mcp__wqb-db__get_salvage_pool
user-invocable: true
---







**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`），确保依赖（requests/pandas/ply）可用。不要使用系统 Python。

# WQ BRAIN Alpha Optimization V1（两模式）

> **模式调度（原 improve-alpha-performance 已并入本 skill 并彻底移除（目录已删），2026-08-15）**：
> - **Mode B 想法层（默认入口，70% 精力）**：信号概念/字段组合需要改变时使用——换概念、换字段、arXiv 引入新金融概念。
> - **Mode A 参数层（30% 精力）**：核心想法已验证、只调 decay/窗口/中性化/truncation 时使用——8 候选严格批验证。
> - 规则：**先想法后参数（70/30 原则）**。Mode B 改出更好的"想法"后，交给 Mode A 做参数收敛。
> - 两者都失败、>10 种结构无果 → 转向换数据集（回 S0/S1，阶段定义见 `INDEX.md` 流水线表；数据集探索见 `brain-dataset-exploration-general`）。

## Mode B：想法层改进（5 步工作流，每周期 30–60 分钟）

**触发**：Sharpe 卡在低水平、负年份、与 book 高相关等"结构性弱"问题；或用户明确要"改进想法/换概念"。

### Step B1: 收集 Alpha 信息（5–10 min）
- `mcp__wq-brain-http__get_alpha_details` 拉表达式、设置、PnL/Sharpe/Fitness/Turnover/Drawdown。
- `mcp__wq-brain-http__get_alpha_details`（is.checks）+ `mcp__wq-brain-http__check_correlation`（self/prod，阈值 0.7）。
- 记录失败项（如 sub-universe 低 = 依赖非流动股；ATOM 单数据集 alpha 确认宽松阈值）。

### Step B2: 评估核心字段（5–10 min）
- 确认字段 `type`（VECTOR/EVENT）与 coverage。
- 用 `brain-datafield-exploration-general` 的 6 评测（Coverage / Non-Zero / 更新频率 / Bounds / 中心趋势 / 分布）在 neutral settings（NONE/decay=0/短测试期）下摸清数据性质。
- 产出洞察：如"季度稀疏数据 → 优先 persistence 类想法"。

### Step B3: 提出想法级改进（10–15 min）
- 查平台文档/社区技巧（ATOM 原则、负信号翻转）。
- **arXiv 概念检索（默认走 LLM 概念层）**：`scripts/arxiv_api.py "<query>" --concepts --llm -j <region>_<topic>_concepts.json`（用法见 [arXiv_API_Tool_Manual.md](arXiv_API_Tool_Manual.md)）。`<query>` 用 `abs:"短语"` 降噪写法（如 `abs:"post-earnings-announcement drift"`），`--concepts` 抽因子概念、`--llm` 走 DeepSeek 概念层（凭证在 `scripts/.arxiv_llm.env`），`-j` 把概念结构化落盘供候选池直接消费。例：搜 `abs:"return on assets momentum analyst estimates"` → 提取 3–5 篇论文概念（如 precision weighting = 除以 std_dev）。若 LLM 不可用则自动降级规则层。
- 头脑风暴 4–6 个变体：每个只动 1–2 个概念（如加 revision delta）。
- 对照平台算子库校验；不存在的算子换成等价构造（如自写动量公式）。

### Step B4: 仿真对比（10–20 min）
- `create_multiSim`（2–8 条）跑变体；multi 失败退并行单仿。
- 按 Fitness/Sharpe 排名；检查 sub-universe 与逐年一致性；负信号可翻转。

### Step B5: 验证迭代（5–10 min）
- Top 变体跑 submission/correlation 检查。
- 失败 → 回 Step B3（想法池上限 3–5 周期/alpha，仍卡 → 换字段，回 S1，阶段定义见 `INDEX.md` 流水线表）。
- 通过 → 交给 Mode A 做参数收敛；收敛后按「衔接协议」进入下游链（selfcorrQuick → explain-alphas → 过拟合与稳健性测试 → brain-alpha-judge 评审），**不直接提交**。

### Mode B 最佳实践
- 周期上限 3–5 次/alpha；70% 想法 / 30% 参数；成功 = 过检查 + 逐年稳定。
- 保持迭代日志（每轮 metrics 表）。

## Mode A：参数层优化（8 候选严格批）

本模式用于对现有 alpha 做端到端参数优化，含严格预检校验、结构化迭代与强制低相关检查。全部规则见 [reference.md](reference.md)（硬规则、主题配额、执行流、文件追加契约）。

### 硬规则

1. 冻结基线 alpha 的核心字段与数据集，后续轮次不得替换。
2. 任何仿真之前，每个候选必须先通过本地校验。
3. 每轮必须恰好包含 8 个候选表达式。
4. 平台 `operatorCount` 是最终裁判：任何算子数超过 8 的候选无效。
5. Stage A 阶段禁止纯微调，只能做结构化升级。
6. 任何零 FAIL 项的候选必须立即走提交相关性（correlation）检查。
7. `create_multiSim` 结束后，立即以 UTF-8 追加模式把本批结果写入指定的文本文件。
8. 校验或仿真失败时只修精确的报错点；不得为通过而删除核心逻辑来简化表达式。

### 必需工作流

1. 用 WorldQuant BRAIN MCP 工具确认平台设置合法。
2. 读取基线 alpha，冻结其核心数据字段。
3. 先规划 8 个角色，再在主题配额与常用算子限制内编写表达式。
4. 校验前先对照本地算子库做算子预检。
5. 运行本地表达式校验并修复至全部通过。
6. 用 `create_multiSim` 回测这 8 个已校验的表达式。
7. 若批量输出被截断，逐条补取缺失详情。
8. 回测后立即把 8 条结果追加到目标结果文件。
9. 下一轮前诊断负信号翻转、`operatorCount` 溢出、FAIL 原因与相关性。

### 校验层

- 首选：当前项目暴露本地 `validate_expression` 能力时使用它。
- 配套语法检查：复用现有 [expression verifier skill](../alpha-expression-verifier/SKILL.md)。
- 在任何平台请求之前，把语法校验与算子签名校验视为硬闸门。

### 候选批三灯分级（复用 probe_scoring_v2 原则）

8 候选批的优劣分级可套 `wq-brain-campaign-toolkit` 的 v2 三灯公式（`score_datasets.py --probe-score --from-json` 离线校准，公式见 toolkit `references/probe-scoring-v2.md`）。核心原则：
1. **联合评估在最强单点**，禁止跨候选 OR 拼出不存在的理想探针（v1 教训）；
2. **2Y 红灯仅当平台返回值判定**（`two_year_sharpe=None` 不算败）；
3. **tvr 结构性墙**：全部候选同侧出界时绿灯封顶黄灯（LOW→trade_when/decay 拉 tvr；HIGH→拉长窗口压 tvr）。

## 陷阱（已核实）

- **EVENT 字段会破坏 `winsorize`**：对 event 类型字段执行 `winsorize(x, std=N)` 会报 `winsorize does not support event inputs`。先用 `ts_event_*` 把 EVENT 转成 VECTOR（见 `brain-datafield-exploration-general`）。单个 event 字段会导致整个 multi-sim 批次失败。
- **PROD 相关（correlation）闸门**：`PROD correlation < 0.7` 是硬提交闸门（与 Self-Correlation 同族）。提交前用 `mcp__wq-brain-http__check_correlation` 探测；反复提交主导你 book 的同一因子族是常见的失败原因。
- **SuperAlpha 构造**：把 ≥10 颗 alpha 合成 `type=SUPER` 使用 selection+combo 工作流（而非 `combination()`）。见 `wq-brain-superalpha`。

## prod_corr 反馈循环（闸门失败回流规则）

若 `mcp__wq-brain-http__check_correlation` 返回 prod_corr ≥ 0.7，或生产相关性结果尚未出来：
1. 不提交、不进入 S5；该 alpha 不符合提交要求。
2. 回 **Mode B Step B3** 换字段组合/信号概念（想法池上限 3–5 周期/alpha）。
3. 常规想法级改进 2–3 轮仍卡闸 → 按下方「组合腿救援」协议执行（不是继续无脑换字段）。
4. 3 周期仍卡 0.7 → 换字段回 S1（数据集/字段探索见 `brain-dataset-exploration-general`）。
5. 换字段仍卡 → 换数据集（仅当模板多样性已穷尽且查阅论坛无解时，回 S0）。

## Mode B 卡闸 → 组合腿救援（salvage_pool 复用协议，区域无关）

**触发线（用户纪律 2026-09-02）**：本 alpha 必须已过 `mode_b_qualification` 资格线
（sharpe≥1.25 且 fitness≥0.8，以区域 `thresholds.json` 为准，缺省 1.25/0.8），
且 Mode B 常规想法级改进（Step B1–B5）2–3 轮仍被结构性闸门卡死时，才允许进入组合腿救援。
**未达资格线的弱信号候选一律判死（dead_end 回写 + wave 台账 closed），禁止救援**（弱信号组合成功率极低）。

救援不是重写主信号：保留强主腿 + 从 salvage_pool 取补强辅助腿做正交组合。

**弹药查询**（卡点 → boost_dim 映射，`mcp__wqb-db__get_salvage_pool`）：
- 卡 LOW_2Y_SHARPE / 2Y 墙 → `boost_dim="boost_2y"`
- 卡 TVR 墙（turnover 出界）→ `boost_dim="boost_tvr"`
- 卡 CONCENTRATED_WEIGHT / sub-universe → `boost_dim="boost_cw"`
- 信号弱（sharpe/fitness 不足）→ `boost_dim="boost_sharpe"`
- 卡 PROD/self correlation ≥0.7 → `exclude_dataset=<主信号数据集>`，优先跨数据集正交腿
- 通用过滤：`min_sharpe=0.5`（池内快达标因子下限）

**构造纪律**：
1. 主腿（本 alpha 核心字段/概念）冻结，辅助腿 ≤2 条，**必须取自 salvage_pool 返回条目**（禁止凭空另造腿）。
2. 组合用线性 add（各腿先 rank）；权重仅结构化单次设置（0.5/0.5 起步，最多 0.6/0.4），**禁止权重网格扫描**
   （同信号加权调参禁令延伸：同数据集同概念腿 + 调权 = 违规）。
3. 每条候选溯源标记 `combo_rescue_from_<本alpha_id>_with_<salvage_id>`，写入迭代日志。
4. 验证走 Mode A 批纪律：8 候选严格批 → 本地校验 → multiSim。

**验证与兜底**：
- 过闸（全 checks PASS + prod corr <0.7）→ 按标准下游链推进（selfcorrQuick → explain-alphas →
  robustness → judge/verdict），不直接提交。
- 池内无匹配（返回空 / 全同数据集）或组合 1–2 轮仍 FAIL → 判死（dead_end 回写），
  禁止无限烧配额；残余线索写 ledger salvage 字段留痕。

**弹药来源说明**：salvage_pool 由 S4 `review_wave.py --write-ledger` 自动幂等写入
（快达标因子：S≥1.0 且 prod corr<0.5 的 combo 候选 + near 补充），无需人工手写入池。

## 过拟合与稳健性测试（每个候选进入 S5 前必做）

Mode B/A 产出满足指标门槛的候选后，必须先通过本节四项检查：
1. **参数敏感性**：decay/窗口 ±1 档邻域内 Sharpe 不塌方（邻域塌方 = 过拟合信号）。
2. **子宇宙一致性**：sub-universe Sharpe 与主宇宙同向且达内部线（sharpe>1, fitness>0.7, margin>5bp）。
3. **逐年一致性**：分年 Sharpe 无连续两年大幅塌方（Mode B Step B4 已查，此处复核）。
4. **概念对照**：收益来源归因与既有 book 内 alpha 不重叠（见 `brain-explain-alphas`）。

完整审计工作流（归因 + 反过拟合闸门 + PPA 提交规则）见外部 Agent 技能 `brain-alpha-robustness`（登记于 INDEX.md 外部 Agent Skill 段）。

## 衔接协议

- **上游**：`brain-how-to-pass-AlphaTest`（失败项定位与阈值判定；S4 判定 FAIL 且达 mode_b_qualification
  的候选**强制回流**本 skill Mode B，非可选）← S3 `brain-simAlphasinBatch-and-track`（`simulation_status.csv` 候选池）。
- **下游**：`brain-calculate-alpha-selfcorrQuick`（本地快筛 self-corr/PPAC）→ `brain-explain-alphas`（收益来源归因）→ **brain-alpha-robustness**（过拟合/稳健性必经闸，S4→S5）→ `tools/submit_verdict.py`（提交层权威判定；brain-alpha-judge 仅作参考评审，verdict 不构成提交依据）。

## 渐进式文档

- Mode A 完整规则、主题配额、逐步执行流与文件追加契约：[reference.md](reference.md)
- 示例提示词、输出格式与 `LLbaqEqa` 优化案例：[examples.md](examples.md)
- Mode B 的 arXiv 工具：[arXiv_API_Tool_Manual.md](arXiv_API_Tool_Manual.md) + [scripts/arxiv_api.py](scripts/arxiv_api.py)

## 预期产出

持续迭代（Mode B → Mode A），直到至少一个候选满足以下全部条件：

- Sharpe > 1.58
- Fitness > 1.0
- Turnover 在 1%–40% 之间（平台硬闸门为 1%–70%；本 skill 为稳健性采用更严格的内部目标 ≤40%）
- 所有平台检查 PASS，包括 `IS_LADDER_SHARPE`
- `PROD correlation < 0.7`
