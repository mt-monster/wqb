# WQ/BRAIN Skills 整理与改进建议（多维审计）

> 审计范围：`~/.workbuddy/skills/`（用户级，本 WQ BRAIN 项目实际使用的 30 个 skill）
> 审计日期：2026-08-20
> 方法：枚举全部 SKILL.md → 抽取元数据（标题/触发/脚本引用）→ 跨 skill 重复脚本 md5 比对 → INDEX.md 引用一致性校验 → 关键经验（operator/区域）正确性复核

---

## 0. 执行摘要

**规模**：30 个 skill（24 个 WQ-BRAIN 域 + 6 个非 WQ 通用/商品域）。已有 `INDEX.md` 做 L0–L7 分层 + 七阶段挖掘流水线（S-PRE…S5）的架构基准，分层思想成熟。

**已验证的优势（不应破坏）**
- 分层架构清晰：`brain-deepExplore`(L-INT 编排) → `wq-brain-campaign-matrix`(L-PRE 查表) → `wq-brain-campaign-toolkit`(L-TOOL 引擎) → L0–L6 各职能 skill，职责链明确。
- **关键平台经验已正确沉淀并跨 skill 一致**：经逐行核对，`combination(alpha(...))` 已被标记"平台禁用、改用 selection+combo"（`wq-brain-superalpha` L36-37/89、`wq-brain-alpha-optimization-v1` L99、`worldquant-submit-alpha` L102）；`prod_correlation` 在 `selection` 可用、在 `combo` 报 "unknown variable"（`wq-brain-superalpha` L47/59）均正确，与项目 MEMORY 实证一致。**这几点不是 bug，是资产。**

**核心问题（按严重度）**

| 严重度 | 问题 | 证据 | 风险 |
|---|---|---|---|
| **P0** | `INDEX.md` 悬空引用 5 个不存在的 skill | `brain-alpha-orchestrator`/`brain-alpha-repair`/`brain-alpha-research`/`brain-alpha-robustness`/`alpha-template-labs-data-analysis` 目录均不存在 | 索引作为"唯一架构基准"，却指向缺失实体，误导维护者 |
| **P1** | 共享脚本复制粘贴，且已分叉 | `validator.py` 3 份 md5 全不同；`arxiv_api.py` 2 份 md5 不同；`ace_lib.py` 2 份字节相同；共 11 个文件名跨 skill 重复 | 同一逻辑多份实现，改一处漏 N 处，行为逐步漂移 |
| **P2** | 命名前缀不统一 | `brain-`(19) / `wq-`(5) / `wqb-`(1) / `worldquant-`(1) / `alpha-`(1) 混用 | Agent 按名匹配时分类模糊，难以一眼判断层/域 |
| **P2** | 战役型 skill 职责边界模糊 | `wq-brain-campaign-toolkit` 自称"战役脚本唯一权威实现"，但 `wq-brain-ppa-mining`/`wq-brain-superalpha` 也是可运行战役工作流且自带 scripts | "唯一权威"声明与实际并存实现冲突 |
| **P3** | 区域假设陈旧 | 9 个 skill 仍列 IND、8 个列 GLB、8 个列 KOR 为开放目标 | 实证：IND=0 ACTIVE、KOR 种子 prod-corr 全败、GLB emotion 族全败（`MEMORY.md`）→ 浪费算力探针死路 |
| **P3** | 非 WQ skill 物理同居 | `code-optimization`/`dead-code-cleanup`/`gold-analysis`/`jin10-news`/`planning-with-files`/`pull_BRAINSkill` 与 WQ skill 同目录 | INDEX 虽标"非 WQ 隔离区"，但物理未分离 |

---

## 1. 现状盘点（Inventory）

**WQ-BRAIN 域（24）按 INDEX 层归类**

| 层 | skill | SKILL.md LOC | 备注 |
|---|---|---|---|
| L-INT 编排 | `brain-deepExplore` | 15673 | 最大，日循环总指挥；引用 campaign-matrix/forum-browse/how-to-pass |
| L-PRE 查表 | `wq-brain-campaign-matrix` | 3602 | 区域×数据集矩阵，读 `campaign_registry.json` |
| L-TOOL 引擎 | `wq-brain-campaign-toolkit` | 5096 | 自称唯一权威；含 gate/pipeline/wave/probe/ledger/scan/review/diversity |
| L0 情报 | `brain-nextMove-analysis` | 976 | 日报 |
| L0 情报 | `brain-forum-browse` | 10697 | 论坛浏览/贡献，含 profile/harvest 工作流 |
| L0 情报 | `wq-brain-ppa-mining` | 13861 | PPA 挖掘方法论（WebDataScope 增强） |
| L1 数据 | `brain-dataset-exploration-general` | 2517 | 数据集探索 |
| L1 数据 | `brain-datafield-exploration-general` | 3143 | 字段评估 6 法 |
| L1 数据 | `brain-data-feature-engineering` | 4345 | 特征工程 |
| L2 生成 | `brain-makeSomeGem` | 4643 | GEM 风格批量生成；scripts/trailSomeAlphas |
| L2 生成 | `brain-feature-implementation` | 3223 | idea→本地 CSV 表达式 |
| L2 生成 | `brain-enhance-template` | 3566 | 模板增强 |
| L2 生成 | `alpha-expression-verifier` | 1889 | 语法校验（仅语法层） |
| L3 仿真 | `brain-inspectRawTemplate-create-Setting` | 3652 | raw template 检查+设置 |
| L3 仿真 | `brain-simAlphasinBatch-and-track` | 5411 | 批量回测+跟踪 |
| L3 仿真 | `wqb-concurrency` | 4751 | 并发调优/429 |
| L4 诊断 | `brain-how-to-pass-AlphaTest` | 1619 | 提交阈值要求 |
| L4 诊断 | `wq-brain-alpha-optimization-v1` | 4466 | 两模式优化（Mode B 想法/Mode A 参数） |
| L4 诊断 | `brain-calculate-alpha-selfcorrQuick` | 709 | 本地 self-corr/PPAC 快筛 |
| L4 诊断 | `brain-explain-alphas` | 1276 | 表达式解释 |
| L5 提交 | `brain-alpha-judge` | 6501 | 双闸评审（含中文论坛语料库） |
| L5 提交 | `worldquant-submit-alpha` | 5205 | 实际提交（正则） |
| L5 提交 | `wq-brain-superalpha` | 5638 | SUPER 合成（selection+combo） |
| L6 监控 | `wq-backtest-monitor` | 6778 | 机器级进程监控/效率框架 |

**非 WQ 域（6）**：`code-optimization`(2848)、`dead-code-cleanup`(5890)、`gold-analysis`(4132)、`jin10-news`(992)、`planning-with-files`(4097)、`pull_BRAINSkill`(1580)。

---

## 2. 维度一：架构层面（Architecture）

### 2.1 已有分层（优点，保留）
`INDEX.md` 的 L0–L7 + 七阶段流水线是当前最值钱的资产。任何重构都应以它为准绳，不要另起炉灶。

### 2.2 共享脚本库缺失 → 复制粘贴 + 分叉（P1，最大架构债）
11 个脚本文件名跨 ≥2 个 skill 重复。md5 实测：

| 文件 | 出现 skill 数 | md5 状态 | 含义 |
|---|---|---|---|
| `validator.py` | 4（alpha-expression-verifier / brain-feature-implementation / brain-inspectRawTemplate-create-Setting / brain-makeSomeGem） | **3 份各不相同**（9aab910de873 / 2ef88146420f / 0cc83e71f136） | 已分叉漂移，校验行为可能不一致 |
| `arxiv_api.py` | 2（brain-explain-alphas / wq-brain-alpha-optimization-v1） | 不同（c624e9c655eb / 37ec6955c326） | 已分叉 |
| `ace_lib.py` | 2（brain-feature-implementation / brain-simAlphasinBatch-and-track） | **字节相同**（6f0b70a9eb8d） | 纯拷贝，55KB |
| `dataset_health_check.py` | 2（brain-deepExplore / wq-brain-ppa-mining） | — | 重复 |
| `fetch_dataset.py` | 2（brain-feature-implementation / brain-makeSomeGem） | — | 重复 |
| `helpful_functions.py` | 3（feature-implementation / makeSomeGem / simAlphasinBatch） | — | 重复 |
| `implement_idea.py` | 2 | — | 重复 |
| `load_credentials.py` | 2（alpha-judge / inspectRawTemplate） | — | 重复 |
| `merge_expression_list.py` | 2 | — | 重复 |
| `run.py` | 2（enhance-template / makeSomeGem） | — | 重复 |
| `parsetab.py` | 4 | — | ply 生成表（相对良性，但应统一生成） |

**结论**：缺一个 `wqb-skills-common/` 共享包。这是第一大架构改进点。

### 2.3 命名前缀不统一（P2）
同一域出现 `brain-`/`wq-`/`wqb-`/`worldquant-` 四种前缀，且无明显规则（`wq-` 与 `wqb-` 仅差一个字母）。建议统一为 `wqb-<layer>-<name>` 或全量 `brain-<layer>-<name>`，让前缀直接表达层（编排/查表/引擎/生成/提交…）。

### 2.4 战役型 skill 职责边界（P2）
`wq-brain-campaign-toolkit` 声明"战役脚本唯一权威实现，禁止在别处复制 scripts 逻辑"，但 `wq-brain-ppa-mining`(13.8K LOC) 与 `wq-brain-superalpha`(5.6K LOC) 各自带完整可运行脚本，本质是 PPA/SUPER 两个**领域战役**工作流。边界应是：toolkit=**通用引擎**（gate/probe/ledger 原语），ppa/superalpha=**领域编排**（调用引擎原语 + 领域专属 selection/combo 配方）。当前 INDEX 把这三者都归在 L0/L5，未在"引擎 vs 领域"维度说清，易诱发二次实现。

### 2.5 非 WQ skill 物理同居（P3）
通用/商品类 skill 与 WQ 类同目录。INDEX 已逻辑隔离（"非 WQ 隔离区"），但物理未分。建议移入 `general/` 子目录，避免 Agent 在 WQ 任务中误触发 `gold-analysis`。

---

## 3. 维度二：逻辑 / 正确性层面（Logic）

### 3.1 关键平台经验正确（已验证，优点）
逐项核对 `combination()` / `prod_correlation` / `SUBINDUSTRY` 三处易错点，全部正确：
- `combination(alpha(...))` 在 3 个 skill 中被正确标记为"平台已禁用，改用 selection+combo"。
- `prod_correlation` 在 `selection` 可用、`combo` 报 "unknown variable" —— 与 `KPGvRMg1` 重建实证一致。
- `SUBINDUSTRY` 中性化是 SA 组合层降 prod-corr 的杠杆、对单 alpha 无效 —— skill 描述与此吻合。

### 3.2 区域假设陈旧（P3）
9 个 skill 列 IND、8 个列 GLB、8 个列 KOR 为可挖区域。但 `MEMORY.md` 实证：IND=0 ACTIVE、KOR 11 个种子 prod-corr 全 >0.7 被拒、GLB emotion 族 42 候选全被 PROD_CORRELATION 一刀挡。skill 未反映这一"当前 book 死路"状态，Agent 可能反复探针已知死路。

### 3.3 硬编码阈值分散（P3）
`0.7`（prod/self 相关闸）、`≥0.85/≤50/≥10`（PPA 体检）等阈值散落多个 skill。逻辑上正确，但没有集中常量，未来平台调阈需改 N 处。建议集中到 `wqb-skills-common/thresholds.py`。

### 3.4 分叉脚本导致逻辑不一致（P1 的下游）
`validator.py` 三份 md5 不同 → 同一个"表达式校验"在不同 skill 里可能给出不同判定。这是隐蔽的逻辑正确性风险（同一 alpha 在 A skill 校验过、在 B skill 跑却因校验差异失败）。

---

## 4. 维度三：可维护性 / 文档（Maintainability）

### 4.1 INDEX.md 悬空引用（P0）
`INDEX.md` "外部 Agent Skill 登记"段登记 5 个 `.workbuddy/skills/` 下的 skill，但目录中**均不存在**。作为"修改任何 skill 前必须先读"的唯一基准，这是最高优先级文档缺陷。两种修法：① 若确已弃用 → 标注 `[已弃用 2026-XX]`，保留名以备追溯；② 若应存在 → 补建或恢复。

### 4.2 缺"最后验证日期 / owner"（P3）
30 个 skill 无统一的 `last_verified` / `owner` 字段。平台 operator/阈值频繁变动（如 `combination()` 禁用），无时间戳无法判断"这条经验还新鲜吗"。

### 4.3 深层分析文件可能滞后（P3）
`INDEX.md` 指向 `research-data/skills_architecture_analysis.md`（2026-08-15，14.5KB）。本次审计发现的新分叉（validator/arxiv_api）建议回填进该文件。

### 4.4 物理隔离缺失（见 2.5）

---

## 5. 改进建议（优先级 + 可执行）

| 优先级 | 动作 | 改动面 | 风险 | 回归验证 |
|---|---|---|---|---|
| **P0** | 修 `INDEX.md` 5 个悬空引用：标 `[已弃用]` 或补建 | 仅 1 个 md 文件 | 零（纯文档） | 重读 INDEX 确认无缺失路径 |
| **P1** | 抽 `wqb-skills-common/`：收纳 `validator/ace_lib/arxiv_api/dataset_health_check/fetch_dataset/helpful_functions/implement_idea/load_credentials/merge_expression_list/run/parsetab`；各 skill 改为 `from wqb_skills_common import ...` | 11 文件迁出 + 引用改写 | 中（需跑各 skill 的 smoke） | 逐 skill `python -c "import scripts.xxx"` + 一次真实回测 |
| **P2** | 命名规范化 `wqb-<layer>-<name>`（或全 `brain-`），同步 INDEX 与所有跨引用 | 全部 SKILL.md frontmatter + INDEX | 中（改名破坏 Skill 发现，须连带改引用） | `Skill` 工具可正常 load 每个改名后 skill |
| **P2** | 明确战役边界：INDEX 增"引擎 vs 领域"小节，规定 ppa/superalpha 只能调用 toolkit 原语，禁止自带 gate/probe 副本 | INDEX + 2 skill 说明 | 低 | 文档评审 |
| **P3** | 区域状态注记：S-PRE/S0 增"当前 book 死路"一节（IND=0 / KOR 全败 / GLB emotion 全败），引 MEMORY 实证 | 2–3 个 SKILL.md | 零 | 文档评审 |
| **P3** | 阈值集中 `wqb-skills-common/thresholds.py` | 新文件 + 引用改写 | 低 | grep 确认无残留字面量 |
| **P3** | 非 WQ skill 移入 `general/` 子目录 | 6 目录移动 | 低（Skill 按相对路径发现） | `Skill` 工具可 load |
| **P3** | 每个 SKILL.md 加 `last_verified` / `owner` 字段 | 30 文件头 | 零 | — |

---

## 6. 推荐落地顺序（执行计划）

1. **第一批（零风险，建议立即执行）**：P0（INDEX 悬空引用）+ P3 区域注记 + P3 last_verified 字段。纯文档，git 可回滚。
2. **第二批（需回归）**：P1 抽共享库。先迁 `validator.py`/`ace_lib.py`（分叉/拷贝最严重），用 MCP venv 跑各 skill 的 import smoke + 一次真实回测确认行为不变，再迁其余。
3. **第三批（破坏性，需确认）**：P2 命名规范化 + 战役边界澄清 + 非 WQ 物理隔离。改名必须连带改 INDEX 与所有 `Skill` 调用点，建议单独一批并全量 `Skill` 加载验证。

---

## 附录 A：跨 skill 重复脚本清单（md5 证据）
- `validator.py`：`alpha-expression-verifier`(9aab910de873) / `brain-feature-implementation`(2ef88146420f) / `brain-inspectRawTemplate-create-Setting`(0cc83e71f136) → **三份均不同**
- `arxiv_api.py`：`brain-explain-alphas`(c624e9c655eb) / `wq-brain-alpha-optimization-v1`(37ec6955c326) → 不同
- `ace_lib.py`：`brain-feature-implementation` = `brain-simAlphasinBatch-and-track`(6f0b70a9eb8d) → 字节相同

## 附录 B：已确认正确的关键经验（勿动）
- `combination(alpha(...))` 已禁用 → 用 selection+combo（`wq-brain-superalpha` L36-37,89 / `wq-brain-alpha-optimization-v1` L99 / `worldquant-submit-alpha` L102）
- `prod_correlation`：selection 可用、combo 报 unknown variable（`wq-brain-superalpha` L47,59）
- `SUBINDUSTRY` 中性化是 SA 组合层降 prod-corr 杠杆、对单 alpha 无效
