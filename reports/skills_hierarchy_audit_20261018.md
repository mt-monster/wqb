# skills 目录层级规划审查报告（2026-10-18）

> 审查对象：`Claude/skills/`（51 个 skill，源目录）+ 6 个安装位（`.workbuddy` / `.claude` / `.codex` / `.cline` / `.agents` / `.cursor`）
> 审查方法：目录清点 + 命名一致性统计 + `sync_skills.py` 行为验证 + 守护测试交叉验证。
> 结论摘要：**当前布局 7/10 可用，但存在 5 处系统性不一致，其中 2 处会导致「找不到/找不到权威」的实际故障。**

---

## §1 现状清点（事实基线）

| 指标 | 数值 |
|---|---|
| skill 总数 | 51 |
| 仅有 `SKILL.md`（无附属目录） | 6（`brain-alpha-research-hypothesis-first` / `-news-sentiment` / `brain-dataset-mining-experience` / `wq-brain-campaign-matrix` / `wq-brain-ra-twn` / `wqb-concurrency`） |
| 含 `references/` 目录 | 30 |
| 含 `reference.md` 单文件 | 11 |
| **两者并存（冲突）** | **3** |
| 含 `scripts/` | 14（共 69 个脚本） |
| 含 `config/` vs `configs/` | **命名分裂**（1 vs 3） |

**references 体量 Top5**：
`wq-brain-ra-pipeline` 40 文件 464KB ｜ `wq-brain-ra-eur` 15 文件 204KB ｜ `wq-brain-ra-kor` 17 文件 252KB ｜ `wq-brain-ra-deu` 16 文件 192KB ｜ `wq-brain-ra-gbr` 21 文件 248KB

---

## §2 问题诊断（按严重度排序）

### P0-1 `reference.md` 与 `references/` 并存 —— 同一 skill 内两套参考入口

**事实**：`brain-how-to-pass-alpha-test` / `planning-with-files` / `wq-brain-alpha-optimization-v1` 三个 skill 同时拥有：
- 根级单文件 `reference.md`（8–12KB）
- `references/` 目录（多文件）

**危害**：Agent 检索时的**权威歧义**。同一个 skill 内两个「参考入口」，读到哪份取决于检索实现，且两份内容无同步机制 ⇒ 必然漂移。

**根因**：历史上从「单文件 → 目录」演进时的中间态未被收口。

### P0-2 跨区方法论层缺位，导致 `docs/reference` 与 `skills/references` 职责重叠

**事实**：
- `Claude/skills/*/references/` = skill 内**区域专属**知识（DEU/GBR/EUR/IND…）
- `docs/reference/` = 跨区**方法论**（`field_profile_to_alpha_playbook.md` 等）+ 区域归档（`docs/reference/DEU`、`GBR`…）

**已出现的事实性重复**：GBR 的 `_field-profile-playbook.md` 里显式写着「跨区方法论主文：`docs/reference/field_profile_to_alpha_playbook.md`」，即**同一知识被拆成 skill 内 + docs 两处并互相引用**。

**危害**：跨区经验（画像方法、算子 playbook）没有单一权威，14 个区域 skill 各自复述一遍，改一处不会传播到其余 13 处。

### P1-3 `config` vs `configs` 命名分裂 —— ⚠ **经深查后撤销「改名」建议**

**初判（错误）**：`config/`（1 个）与 `configs/`（3 个）分裂，建议统一为单数。

**深查后的实际情况**——这 3 个 `configs/` **不是普通配置目录，而是被测试锁定的凭据契约**：

| 证据 | 内容 |
|---|---|
| `tests/unit/02_workflow/test_judge_never_submits.py:218` | 断言 stderr **必含字面量** `configs/config.json`，且不泄漏凭据 |
| `tests/unit/07_docs_skills/test_sf_docs.py:134` | 断言三来源顺序：环境变量 **<** `configs/config.json` **<** MCP `.env` |
| `scripts/vendor/load_credentials.py:46` | `config_filename: str = "configs/config.json"` —— 该路径用于**明文凭据迁移检测**（发现即提示迁移，不打印值） |

**结论：撤销改名建议。** 改名的收益（Agent 按 `config/` 约定能多找到 3 个 skill）远小于
破坏两条**凭据安全测试**的代价。这属于「表面不一致、实则语义不同」——`config/` = 静态配置资产，
`configs/` = 凭据契约路径（历史约定，已被测试与代码双重锁定）。

**替代处置（已落地）**：用测试固化语义，避免后人误"统一"：

- `config/` = 静态配置资产（可提交，可批量处理）
- `configs/config.json` = **凭据契约路径，禁止改名**（AGENTS.md 红线 + 2 条测试锁定）
- 新增 `tests/unit/07_docs_skills/test_skill_layout_contract.py` 守护两者语义边界
| `configs/` | `brain-alpha-judge` / `brain-forum-browse` / `brain-sim-alphas-in-batch-and-track` |

### P1-4 `scripts/` 内存在跨 skill 同名脚本（重复实现）

**事实**：同一脚本名在多个 skill 下各存一份——
`validator.py` ×4 ｜ `helpful_functions.py` ×3 ｜ `ace_lib.py` ×3 ｜ `skill_roots.py` ×2 ｜ `merge_expression_list.py` ×2 ｜ `load_credentials.py` ×2 ｜ `implement_idea.py` ×2 ｜ `fetch_dataset.py` ×2 ｜ `diversity_enhancer.py` ×2

**⚠ 同样需深查再动手**：`load_credentials.py` ×2 已被 §P1-3 的测试锁定，**不可上收**。
其余 8 个待逐一 diff 确认是否真同功能（同名不等于同实现）。

**危害**：修复 bug 需改 N 份，且必然出现「只改了一处」的版本分裂。`brain-inspect-raw-template-create-setting` 的 `ace_lib.py` 同时在根目录和 `scripts/` 各有一份。

**事实**（`du -sk`）：`wq-brain-campaign-toolkit` 2175KB（19 脚本 + config + references）｜`brain-make-some-gem` 880KB ｜`wq-brain-ra-pipeline` 512KB（40 参考文件）｜`brain-alpha-judge` 440KB。

`wq-brain-ra-pipeline` 的 40 个参考文件 464KB，是**唯一被 14 个区域 skill 共同依赖**的上游。

**风险**：上游一处改动 ⇒ 14 个下游受影响；且 464KB 超出单次注入的合理阅读量，Agent 实际只能靠索引跳转。

### P2-6 `data/` 目录语义不清

**事实**：`brain-alpha-judge` / `brain-alpha-robustness` / `brain-forum-browse` / `brain-sim-alphas-in-batch-and-track` 下有 `data/`。
skill 被安装到 6 个位置 ⇒ **这些 `data/` 是样本数据还是运行时产物？** 若为产物，应在 `.gitignore` 且不入安装位（当前 `sync_skills.py` 会整目录复制）。

### P2-7 根目录散落文件无统一归位

**事实**：`brain-inspect-raw-template-create-setting` 根目录直接放 `ace_lib.py` / `helpful_functions.py`（可执行代码）+ `AgenticFlow.png`（图）；`brain-data-feature-engineering` 根目录放 `OUTPUT_TEMPLATE.md` / `examples.md`；4 个 skill 根目录有 `requirements.txt`。

**问题**：可执行代码与文档混在同一层，违反「scripts/ 放代码、references/ 放文档」的隐含约定。

---

## §3 现状做对了什么（应保留）

| 好实践 | 说明 |
|---|---|
| **`_` 前缀 = 跨类别文档** | 17 个 `_*.md` 已形成稳定惯例；且 `test_profiles_layer.py` 会把非 `_` 前缀的跨类别文件判为「孤儿分支文件」⇒ **该约定有测试强制，勿破坏** |
| **区域 skill 结构高度一致** | 14 个 `wq-brain-ra-*` 统一为 `SKILL.md` + `references/<类别>.md`（类别名与 `cells.json` 对齐），可预测性高 |
| **`profiles` 生成物机制** | `region-panel` / `cells-index` / `manual` 三 marker 块分离生成与手改，`render --apply` 幂等（有测试守护 `R.plan()` 幂等） |
| **`_field-profile.md` 已跨区统一** | DEU / GBR / IND 均用 `_field-profile*.md` 命名，且都锚定同一工具 `tools/fields/field_profile.py` + DB 视图 ⇒ **这是全仓最成功的横向统一，应作为模板推广** |
| **同步脚本覆盖 6 安装位** | `sync_skills.py` 单源多目标，比「各机手改」强得多 |
| **配置外置于 `tracking/<REGION>/config/`** | skill 不自带区域配置，避免多处漂移 |

---

## §4 调整建议

### 建议 1（立即 · 低风险）：消除 P0-1 并存

**动作**：把 3 个并存 skill 的 `reference.md` 内容并入 `references/`（如 `references/overview.md`），删除根级单文件。
**收益**：消除权威歧义；与另外 27 个 skill 对齐。
**风险**：低（纯文件移动，需同步 3 处 SKILL.md 引用）。

### 建议 2（高优先 · 中风险）：确立五层目录契约

**现状是「事实上的四类」**（`references` / `scripts` / `config(s)` / `data`），但**无成文契约**，且各 skill 用法不一。建议固化为：

```text
<skill>/
├── SKILL.md          # 唯一入口：职责边界 + 控制面板 + 索引（硬约束：<5000 words）
├── references/       # 只读知识
│   ├── <类别>.md      # 与 cells.json 类别对齐（区域 skill 专属）
│   └── _<主题>.md     # 跨类别主题（_ 前缀，测试强制）
├── config/           # 静态配置（统一单数；configs/ 全部并入）
├── scripts/          # 可执行代码（根目录散落的 .py 全部下沉）
└── (data/ 移除)      # 运行期产物不入 skill，改指 tools/ 或 tracking/
```

**命名契约（建议写进 AGENTS.md）**：

| 层 | 目录名 | 内含 | 禁止 |
|---|---|---|---|
| 知识 | `references/` | 只读 `.md` | 禁止 `.py`、禁止可执行 |
| 配置 | `config/` | `*.json` / `*.yaml` / `*.toml` | **禁止 `configs/` 复数** |
| 代码 | `scripts/` | `*.py` / `*.sh` | **禁止放根目录** |
| 产物 | （无） | — | **禁止 `data/`**：产物走 `results/` `logs/` `tools/ledger/` |

### 建议 3（高优先）：跨区方法论上收到 `docs/reference/`，区域事实留在 skill

**问题**：画像方法、算子 playbook 这类**跨区通用**知识目前在 14 个区域 skill 里各写一遍。

**建议分工**：

| 知识类型 | 归属 | 理由 |
|---|---|---|
| 画像**方法**（9 类 verdict 定义、查询方法） | `docs/reference/field_profile_to_alpha_playbook.md` | 跨区通用，改一处全体生效 |
| 画像**事实**（某区某字段的实测值） | `skills/wq-brain-ra-<区>/references/_field-profile.md` | 区域专属，随区演进 |
| 算子**跨区** playbook | `docs/reference/operators_playbook.md` | 同上 |
| 算子**本区**实证 | `skills/wq-brain-ra-<区>/references/` | 同上 |
| 闸门铁律 | `.workbuddy/memory/MEMORY.md`（跨项目级）或 skill 顶部 | 唯一出处，禁止多处复制 |

**落地方式**：区域 skill 只保留**本区差异**（像现在 SKILL.md 的「本区覆盖」段那样），通用部分改为一行链接 + 「详见 `docs/reference/xxx.md`」。

### 建议 4（中优先）：`scripts/` 同名脚本上收到 `tools/`

**动作**：`validator.py` ×4、`ace_lib.py` ×3、`helpful_functions.py` ×3、`skill_roots.py` ×2 等**同名且同功能**的脚本，从各 skill 的 `scripts/` 上收到 `tools/<模块>/`，skill 内改为薄封装或直接引用。

**收益**：符合项目已有铁律「`tools/` = 工具链唯一入口，索引见 `tools/README.md`」；修 bug 只改一处。

**前置**：需先确认它们**真同功能**（同名不等于同实现），逐个 diff 后再迁。

### 建议 5（中优先）：移除 skill 内 `data/`

**动作**：确认 4 个 skill 的 `data/` 是样本还是产物。产物 ⇒ 移出并 gitignore；样本 ⇒ 改名 `fixtures/` 或 `examples/` 并入版本控制。
**理由**：skill 是**只读知识 + 可执行**的组合，安装到 6 处；若含产物则每次同步都复制垃圾。

### 建议 6（低优先）：拆分超大 skill

`wq-brain-ra-pipeline`（40 参考文件 464KB，14 区依赖）：
- 建议按「通用九步 SOP」/「六步纵深骨架」/「区域无关的闸门与铁律」拆 3 个参考文件，SKILL.md 只留索引 + 本区 override。
- 拆完后用 `wc -w` 守住 SKILL.md < 5000 words（项目已有此治理口径）。

### 建议 7（低优先）：统一依赖声明

4 个 skill 根目录有 `requirements.txt`（`alpha-expression-verifier` / `brain-sim-alphas-in-batch-and-track`）。
建议：Python 依赖统一到仓库根 `requirements.txt`；skill 内 `requirements.txt` 只保留**该 skill 独有**的额外依赖，并标注是否与根文件重复。

---

## §5 建议优先级与实施顺序

| 序 | 建议 | 优先级 | 风险 | 预估工作量 |
|---|---|---|---|---|
| 1 | 消除 `reference.md` / `references/` 并存 | **P0** | 低 | 3 skill × （合并+改引用） |
| 2 | 五层目录契约写入 AGENTS.md + 统一 `config/` | **P0** | 低 | 文档 1 节 + `configs`→`config` 重命名 3 处 |
| 3 | 跨区方法论上收 `docs/reference/` | P1 | 中 | 需先定「哪些段落通用」的判定标准 |
| 4 | 同名 scripts 上收 `tools/` | P1 | 中 | 需 diff 验证同功能 |
| 5 | 移除 skill 内 `data/` | P2 | 低 | 4 处确认 + 迁移 |
| 6 | 拆分 `wq-brain-ra-pipeline` | P2 | 中 | 40 文件重组 |
| 7 | 依赖声明统一 | P3 | 低 | 4 处 diff |

---

## §6 审查结论

**做得好的**：区域 skill 的 `_field-profile.md` 跨区统一 + `profiles` 生成物三 marker 机制 + 6 安装位单源同步，这三项是本仓最有价值的工程设计，应推广。

**最该修的**：① 同 skill 内 `reference.md` / `references/` 并存造成权威歧义；② `config` / `configs` 命名分裂会让按约定检索的 Agent 直接失败；③ 跨区通用知识（画像方法论）散在 14 个区域 skill 里，缺单一权威，是「同一铁律两处并存必然漂移」的具体案例。

**核心判断**：当前 `skills/` 缺的不是目录，而是**成文的目录契约**。五类目录（知识 / 配置 / 代码 / 产物 / 入口）都在用，但命名和边界靠默契。建议把 §4 建议 2 的契约写进 `AGENTS.md`，并用测试守护（如：禁止 skill 内出现 `configs/`、禁止 `.py` 出现在 skill 根目录、禁止 `data/` 出现在 skill 内）。