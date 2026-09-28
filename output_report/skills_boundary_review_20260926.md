# 33 个 skills 职责边界专项审计

> 日期：2026-09-26 · 方法：可测量判据，**不凭印象**
> 判据：抽取 33 个 SKILL.md 的 frontmatter 声明 + 统计各自引用的 **MCP 工具 / DB 表 / CLI / 产物**，
> 以「同一资源被多个 skill 声明为自己职责」定位边界不清；再逐条回原文核实是真冲突还是已声明的上下游

---

## 0. 结论摘要

1. **边界声明覆盖率只有 39%（13/33）**。20 个 skill 没有写清"上游/下游/不做什么"——这是边界问题的**主因**：不是职责真的重叠，而是**没人声明**。
2. **写得最清楚的是判定层，写得最差的是执行层与数据层**。`brain-alpha-judge` 是唯一堪称范本的（明确"参考层、不执行提交"）；而真正执行提交的 `worldquant-submit-alpha` 与 `wq-brain-superalpha` **都没有书面边界**，却共享 6 个资源。
3. **发现一处与权威常量的正面矛盾**：`brain-alpha-research` 写"区域优先级 **HKG ≈ KOR > EUR**"，而 `src/wqb/config.py::REGION_PRIORITY` 是 `EUR=2, KOR=2, GLB=2, HKG=1` —— **权威常量里 EUR 高于 HKG，与该 skill 的结论完全相反**。
4. **L4 的触发词直接撞车**：`brain-how-to-pass-alpha-test`（"提交失败原因…如何提升指标"）与 `wq-brain-alpha-optimization-v1`（"**修复失败的提交测试**"）对同一用户意图各自宣称归属，且共享 7 个资源。

---

## 1. 体检方法

| 步骤 | 做法 |
|---|---|
| ① 声明抽取 | 解析每个 SKILL.md 的 frontmatter（`name` / `layer` / `description` / `last_verified`） |
| ② 资源指纹 | 正则提取各自引用的 MCP 工具、DB 表、`tools/*.py`、产物文件 |
| ③ 撞车计算 | 同一资源被 ≥2 个 skill 引用 → 候选冲突；**剔除三个跨层枢纽**（ra-pipeline / toolkit / matrix，它们横跨是设计使然） |
| ④ 声明完整度 | 统计正文含「边界 / 不负责 / 不做 / 上游 / 下游 / 职责 / 勿用」等词的密度 |
| ⑤ 原文核实 | 每个候选冲突**回原文读声明**，区分真冲突 vs 已声明上下游 |

原始结果：`logs/_skill_boundary_audit.json`（冲突项 60+）

---

## 2. 分层与规模

| 层 | 数量 | 成员 |
|---|---|---|
| L-RA / L-PRE / L-TOOL | 1 / 1 / 1 | ra-pipeline（编排）、campaign-matrix（查表）、campaign-toolkit（引擎） |
| L0 情报选题 | 4 | next-move-analysis、forum-browse、ppa-mining、labs-data-analysis |
| **L1 数据理解** | **7** | alpha-research、field-quality、hypothesis-first、news-sentiment、data-feature-engineering、datafield-exploration、dataset-exploration |
| L2 表达式生成 | 3 | make-some-gem、feature-implementation、expression-verifier |
| L3 设置仿真 | 3 | inspect-raw-template、sim-alphas-in-batch-and-track、wqb-concurrency |
| **L4 诊断优化** | **6** | optimization-v1、alpha-repair、robustness、explain-alphas、selfcorr-quick、how-to-pass-alpha-test |
| L5 过闸提交 | 3 | judge、submit-alpha、superalpha |
| L6 监控复盘 | 2 | backtest-monitor、dataset-mining-experience |
| L7 元技能 | 2 | planning-with-files、pull-brain-skills |

## 3. 边界声明完整度（关键指标）

**有较充分声明（13）**：judge、robustness、dataset-mining-experience、inspect-raw-template、make-some-gem、sim-alphas、submit-alpha、optimization-v1、campaign-matrix、campaign-toolkit、ppa-mining、ra-pipeline、superalpha

**声明薄弱/缺失（20）**：

| skill | 缺失风险 |
|---|---|
| `alpha-expression-verifier`、`brain-feature-implementation`、`brain-datafield-exploration-general` | 命中 0~1，完全未声明边界 |
| `brain-alpha-research`*、`brain-alpha-research-hypothesis-first`、`brain-alpha-research-news-sentiment` | L1 三件套互不知道对方存在 |
| `brain-alpha-repair`、`planning-with-files`、`pull-brain-skills` | 命中 0 |
| `brain-calculate-alpha-selfcorr-quick`、`brain-explain-alphas`、`brain-how-to-pass-alpha-test`、`wq-backtest-monitor`、`wqb-concurrency` | 命中 2，仅顺带提及 |

\* `brain-alpha-research` 不仅没声明边界，还**主动宣称推翻了权威常量**（见 §4-①）。

---

## 4. 明确的边界缺陷（按严重度）

### ① P0 · L1 与权威常量正面矛盾

| 来源 | 主张 |
|---|---|
| `brain-alpha-research/SKILL.md:45` | 「区域优先级**修正为 HKG ≈ KOR > EUR**」（自称 2026-08-05 实证） |
| `src/wqb/config.py::REGION_PRIORITY`（AGENTS.md 声明的唯一权威） | `{'USA':3, 'EUR':2, 'KOR':2, 'GLB':2, 'CHN':1,'ASI':1,'JPN':1,'AMR':1,'TWN':1,'GBR':1,'DEU':1,'IND':1,'MEA':1,'HKG':1}` → **EUR > HKG** |

**两者结论相反**，且 skill 用的是"修正/撤回"口吻（它还"撤回"了 EUR 死路判断）。一个 skill 文档单方面推翻权威常量，且该主张会直接误导选区投入。
另 `brain-dataset-exploration-general:60-65` 自带第三份区域表（KOR 192 数据集 / EUR TOP2500，标注"截至 2026-08"）——第三套口径。

### ② P0 · L5 执行权分工无书面边界

`worldquant-submit-alpha`（REGULAR）与 `wq-brain-superalpha`（SUPER）**共享 6 个资源**
（`registry_empirical`、`wave_results`、`run_selection`、`set_alpha_properties`、`submit_verdict`、`workflow_submit_alpha`），
但两者**都没有"我不做什么 / 何时不该用我"的声明**。
反倒是**不执行提交**的 `brain-alpha-judge` 把边界写得最清楚（"参考层、非最终判定、提交由 submit_verdict 判定 + 用户确认后走 worldquant-submit-alpha"）。

→ 结果：**判定权的边界很清楚，执行权的边界是空的**。Agent 可能用 SA 路径提交 REGULAR，或反之。

### ③ P1 · L4 触发词直接撞车

| skill | frontmatter 触发词 | 重叠点 |
|---|---|---|
| `brain-how-to-pass-alpha-test` | "alpha 提交**失败原因**、如何**提升 alpha 指标**" | 与下方"修复失败的提交测试"同一意图 |
| `wq-brain-alpha-optimization-v1` | "**修复失败的提交测试**、把 PROD 相关性压到 0.7 以下" | 同上 |

两者共享 `backtest_results`、`salvage_pool`、`check_correlation`、`get_alpha_details`、`simulation_status`、`thresholds.json`、`submit_verdict` 共 7 个资源，**互不提及对方**，且均属 L4。

### ④ P1 · L2 生成层的"内嵌关系"未声明

`brain-feature-implementation` 正文中 **GEM / trailSomeAlphas / 主链 / 入口 出现 0 次**，
但它（a）被内嵌在 `brain-make-some-gem` 引擎里、（b）ra-pipeline 把"把它当主链入口"列为**反模式**。
三者共享 `expressions` 表与 `final_expressions.json`。**FI 自己不知道自己被内嵌**，读它的 Agent 会误当独立入口。

### ⑤ P2 · L3 设置 vs 执行的产物归属重叠

`brain-inspect-raw-template-create-setting` 与 `brain-sim-alphas-in-batch-and-track` 共享 5 个资源
（`alphas`、`candidates`、`expressions`、`final_expressions.json`、`settings.json`）。
前者应只产出**设置计划**，后者执行；但两者都写 `settings.json` / `final_expressions.json`，未声明谁主写。

### ⑥ P2 · L0/L6 轻微

- L0：`ppa-mining` 与 `labs-data-analysis` 都调 `webdata_quality`；`next-move` 与 `ppa-mining` 都调 `get_campaigns`。前者已声明边界，后两者（next-move / labs）声明薄弱。
- L6：`backtest-monitor` 与 `sim-alphas` 都写 `wave_results` / `ledger_kv`，且**都**写着"正式回写走 toolkit 幂等 CLI；轻量回写可用 MCP 直写"——口径一致，但给同一张表留了**两道门**，未约定单点写入方。

### 已判定为"边界清晰"（不必改）

- **L6 内部**（backtest-monitor ↔ dataset-mining-experience）：无资源撞车。
- **L1 资源层面**：7 个 skill 只有 `get_datafields` 被 2 个引用，天然分工（数据集级 / 字段级 / 特征工程级）——问题是**分类法与区域口径**（见 ①），不是资源争夺。
- **ra-pipeline / toolkit / matrix**：横跨全部资源是设计使然（编排器 / 引擎 / 查表层），不计冲突。

---

## 5. 边界定义提案（可直接写进各 SKILL.md）

统一采用「**一句话硬边界**」模板：

```markdown
## 职责边界
- **本 skill 负责**：<产物/动作>
- **本 skill 不做**：<明确排除>（遇到 → 转 <skill/工具>）
- **上游**：<谁给我> | **下游**：<我给谁>
```

各冲突簇的具体裁定：

| 簇 | 硬边界裁定 |
|---|---|
| **L5 执行权** | `worldquant-submit-alpha` = **REGULAR 单颗提交**（`POST /alphas/{id}/submit`）；`wq-brain-superalpha` = **SUPER 组套**（selection+combo，需 ACTIVE REGULAR ≥10）。二者**互不代劳**；SUPER 组件不足 10 → 回 ra-pipeline 步 7，不得用 REGULAR 路径绕。判定权归属 `submit_verdict`，`judge` 仅参考。 |
| **L4 诊断 vs 改进** | `brain-how-to-pass-alpha-test` = **只读查阈值/解释"为什么不过"**（不改表达式、不回测）；`wq-brain-alpha-optimization-v1` = **动手改**（Mode B 换概念 / Mode A 调参数，会产生新变体并回测）。判据：**是否产生新表达式** —— 不产生 → how-to-pass；产生 → optimization-v1。 |
| **L2 生成层** | `brain-make-some-gem` = **S2 唯一主链生成器**；`brain-feature-implementation` = idea→表达式的**实现器**，**在 GEM 内部被调用**，**不得当独立主链入口**（ra-pipeline 已列反模式）；`alpha-expression-verifier` = **纯语法校验**，不生成、不回测。 |
| **L1 数据层** | 按**粒度**硬切：`dataset-exploration`=数据集级（选集）→ `datafield-exploration`=单字段级（选字段）→ `data-feature-engineering`=字段→特征决策；`field-quality`=**S-PRE 数据包预筛**（离线，不产选集）；`news-sentiment`=news/sentiment 家族专用分类（不通用）；`hypothesis-first`=饱和数据集的假设驱动路径。**区域优先级一律以 `config.py::REGION_PRIORITY` 为准**，skill 不得自行"修正/撤回"权威常量。 |
| **L3 设置 vs 执行** | `inspect-raw-template-create-setting` 只**产出设置计划**（不写 `settings.json` 真相源、不回测）；`sim-alphas-in-batch-and-track` 是**唯一执行者**（写 `settings.json` / `final_expressions.json` / 回测）。 |
| **L6 台账** | `wave_results` / `registry_empirical` / `ledger_kv` 的**唯一正式写入方 = toolkit 幂等 CLI**；MCP 直写仅在"无战役目录"场景，且**须在文档标注为逃生阀**，两个 skill 不再各开一道门。 |

---

## 6. 落地建议（按 ROI 排序）

| 优先级 | 动作 | 工作量 |
|---|---|---|
| **P0** | 改 `brain-alpha-research` 的区域优先级段：删除自行"修正/撤回"结论，改为引用 `config.py::REGION_PRIORITY`；同步修 `brain-dataset-exploration-general` 的 2026-08 区域表 | 2 处 |
| **P0** | 给 `worldquant-submit-alpha` / `wq-brain-superalpha` 各补一段「职责边界」（REGULAR vs SUPER 互不代劳） | 2 处 |
| **P1** | 给 `brain-how-to-pass-alpha-test` / `wq-brain-alpha-optimization-v1` 补「是否产生新表达式」判据，并互相引用 | 2 处 |
| **P1** | 给 `brain-feature-implementation` 补「我在 GEM 内部，不是主链入口」 | 1 处 |
| **P2** | 为其余 **14 个声明薄弱的 skill** 补统一模板的「职责边界」段 | 14 处 |
| **P2** | 新增守护测试：断言每个 SKILL.md 含「职责边界」段（与 `last_verified`/`frontmatter` 门禁同级） | 1 个测试 |

> 建议同时把「职责边界」段写进 `Claude/skills/INDEX.md` 的 frontmatter 规范，作为**新增 skill 的必备字段**——否则这次补齐后还会再漂。

---

## 7. 复核命令

```bash
python logs/_tmp_skill_boundary_audit.py     # 重跑撞车扫描（产出 logs/_skill_boundary_audit.json）
python tools/sync_skills.py --check          # 改完同步各安装位
python -m pytest tests/unit/test_skill_integrity.py tests/unit/test_docs_consistency.py -q
```
