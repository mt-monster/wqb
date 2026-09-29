---
last_verified: 2026-09-29
name: brain-feature-implementation
description: "排查或手动复现 GEM 引擎的模板渲染（idea Markdown → alpha 表达式）时查阅：模板语法规则与手动流程。不是生成表达式的入口——要生成表达式请用 brain-make-some-gem。"
layer: L2
allowed-tools:
  - Read
  - Bash
---

# Brain 特征实现（Brain Feature Implementation）

## 职责边界

- **本 skill 负责**：把 idea Markdown 里的模板公式渲染成 alpha 表达式——`implement_idea.py`（渲染）、`fetch_dataset.py`（下载字段）、`merge_expression_list.py`（合并）。这是 GEM 引擎内部的一段；本文写**模板语法规则**与**手动复现 / 排障流程**。
- **本 skill 不做**：**不得作为主链入口**（主链入口 = `brain-make-some-gem`；ra-pipeline 把「直接把 FI 当主链入口」列为反模式）；不选数据集 / 字段（S0 / S1）；不回测、不提交、**不写 DB**。
- **上游 / 下游**：上游 = ideas 文档（GEM 的 LLM 产物，或手写）；下游 = GEM 引擎内部。手动流程的产物 `final_expressions.json` **不是真相源**（真相源是 DB `expressions` 表），也没有任何下游读它——只有 GEM 节点会在自己的流程里把它入库。想让这批表达式进 `expressions` 表：走 `brain-inspect-raw-template-create-setting`（外部 / 手写通道），或直接用 `brain-make-some-gem`；**不要自己写 SQL**。

## 模板语法

- 模板用 Python format 语法：`{variable}`，`variable` 必须是数据集字段的**后缀**（如 `mean`、`st_dev`、`gro`），不带数据集前缀或 horizon（脚本自动检测）。
  - 正确：字段 `anl15_gr_12_m_gro / anl15_gr_12_m_pe` → 模板 `{gro} / {pe}`。
  - 错误：`{anl15_gr_12_m_gro} / {pe}`（带了前缀）；`${gro} / ${pe}`（Shell 语法）。
- 同名占位符可在条件与信号中重复出现，**只绑定一次**；不同占位符仍**禁止**退化为同一字段的恒等式（脚本默认开语义 lint，会拦恒等式 / 裸字段 / 元数据腿）。
- 下载支持 MATRIX / VECTOR / GROUP。GROUP 是分组轴：单个 GROUP 占位符只保留概念原式，**不自动扩展** `rank(label)`、`ts_delta(label)` 等数值变体。
- 组合爆炸受 `--max-expressions`（缺省 24）约束：每个模板的展开条数上限；完全匹配的字段 id 保持 1:1。

## 与 GEM 引擎的关系（谁读本文件）

- GEM 的 LLM prompt **不拼入本文件**：`pipeline_prompts.build_prompt` 只把 feature-engineering 的 8 问当提示，FI 文本虽被读入但**不使用**（源码注释：Concept-first，不要整篇灌进去）。所以本文只面向人 / agent 的手动流程与排障；对 LLM 的机器约束在 prompt 的 `CRITICAL OUTPUT RULES` 里。这一条由 `tests/unit/test_se_docs.py` 钉死——将来若又把 FI 文本拼进 prompt，要同步改本节。
- GEM 运行时用哪份脚本：`pipeline_paths._resolve_skill_dir` 解析——环境变量 `WQB_FI_SKILL_DIR` > 各宿主安装位 > 仓库自带；都找不到才用内嵌副本 `brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-feature-implementation/`（启动时打印 `[skill-doc] … embedded:legacy` 即走了兜底）。
- **两份目录当前逐字节相同**：SKILL.md 由 `python tools/sync_gem_embedded_skill.py --apply` 从本文件同步；`validator.py` 与 `alpha-expression-verifier` 的权威版一致（`hump` 命名参数、`bucket` 必带 `range=`/`buckets=`、`densify` 分组键的修复都在里面）——改 validator 必须四处一起改，由测试守护。

## 前置：凭据（只影响 `fetch_dataset.py`）

`fetch_dataset.py` 的凭据来源，优先级从高到低：环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（标准名，与 MCP 服务、toolkit 同名）→ 旧别名 `BRAIN_USERNAME`（或 `BRAIN_EMAIL`）/ `BRAIN_PASSWORD` → 本 skill 根目录的 `config.json`（可选，已 `.gitignore`；只在环境变量不全时才需要）：

```json
{ "BRAIN_CREDENTIALS": { "email": "<your_brain_email>", "password": "<your_brain_password>" } }
```

**agent 不读取、不回显、不提交 `config.json` 与 `.env`**（AGENTS.md）；缺凭据时脚本报错退出，不消耗平台资源。

## 手动流程（复现 / 排障；在仓库根运行，脚本与 CWD 无关）

`$WQ_PY` = MCP venv 解释器；`FI = Claude/skills/brain-feature-implementation/scripts`（GEM 内嵌副本用它的对应目录）。

1. **分析 idea 文档**：读 markdown，提取数据集 ID（如 `analyst15`）、区域（如 `GLB`）、延迟（`0` / `1`）。缺任何一项 → 问用户，不要猜。
2. **下载字段**：
   ```powershell
   & $WQ_PY $FI/fetch_dataset.py --datasetid <ID> --region <REGION> --delay <DELAY> --universe <U> [--data-type MATRIX|VECTOR|GROUP]
   ```
   **`--universe` 缺省 `TOP3000` 只适用于部分区域**（USA / GLB 等）；其它区域必须显式传该区的合法 universe——取值以 `src/wqb/config.py::REGIONS[<R>]["default_universe"]` 为准（例：KOR / AMR 是 `TOP600`）。产物落在 `<数据根>/<ID>_<REGION>_delay<DELAY>/`，数据根 = 环境变量 `WQB_GEM_DATA_ROOT`，未设 → skill 目录下 `data/`。
3. **规划**：列出 idea 里每个「特征定义 / 公式」（`Definition: <formula>` 或公式代码块），每条一项；用宿主自带的清单能力跟踪（本文不指定具体工具名）。
4. **逐条渲染**：
   ```powershell
   & $WQ_PY $FI/implement_idea.py --template "<模板>" --dataset "<数据集目录名>"
   ```
   数据集目录名 = `{ID}_{REGION}_delay{DELAY}`（如 `analyst10_GLB_delay1`）。可选参数：`--idea`（自然语言说明）、`--max-expressions`、`--no-lint`（**不建议关**）、`--field-whitelist <json>`（S1 白名单，收窄绑定池）、`--field-profile` + `--family-match`（按字段画像过滤绑定池）。**不要**用 `python -c` 或临时脚本去检查数据 / 处理结果，信任脚本输出（生成条数、被 lint 拦下的原因）。
5. **合并**：
   ```powershell
   & $WQ_PY $FI/merge_expression_list.py --dataset "<数据集目录名>"
   ```
   在数据集目录生成 `final_expressions.json`（去重后的表达式）。向用户报告唯一表达式条数与路径，并**注明它不是真相源、未入库**（见职责边界）。

## 常见错误

| 现象 | 含义 | 处理 |
|---|---|---|
| `Error: BRAIN credentials missing …` | 环境变量与 `config.json` 都没给出凭据 | 由用户在本机设 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（或建 `config.json`）；不要把口令贴进对话 |
| `Error: No data found or empty response.` | 该 `dataset × region × delay × universe` 组合没有字段（常见于 universe 写错） | 核对 `config.REGIONS` 里该区的合法 universe；用 `get_datafields` 先确认 |
| `Multiple datasets found. Please specify --dataset.` | 数据根下有多个数据集目录 | 显式传 `--dataset` |
| 渲染出 0 条 | 占位符没匹配上字段后缀，或被语义 lint 拦下 | 看脚本输出的拦截原因；按「模板语法」修模板 |
| `Error: Could not import 'ace_lib'` | 依赖缺失或 skill 目录不完整 | 用 `$WQ_PY`；确认 `scripts/ace_lib.py` 存在 |
