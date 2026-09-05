---
last_verified: 2026-08-22
name: brain-inspectRawTemplate-create-Setting
description: "本 skill 仅用于检查原始 BRAIN 模板（raw template），与增强模板无关，不要用于增强模板 （do not use for enhanced templates）。 读取 BRAIN 模板/idea JSON（template/idea/expression_list，如 fundamental28_GLB_1_idea_<timestamp>.json），通过 ace_lib.get_instrument_type_region_delay 获取有效的模拟设置选项，解析 region/delay/universe/neutralization，并使用 ace_lib.generate_alpha 构建 Alpha 列表 JSON（每个表达式一个 Alpha）。 当用户要求检查模板文件、附加设置、创建 alpha 列表或验证设置时使用 （inspect template / create alpha list / validate settings）。"
layer: L3
allowed-tools:
  - Read
  - Bash
user-invocable: true
---

## 持久化铁律（DB 单轨）

战役产物只写入 `data/wqb.db`（经 `wqb.store` / `mcp__wqb-db__*`）。**禁止**把 `final_expressions.json` / `alpha_list.json` / `candidates/*.json` / `cache/*batches*.json` / `results/*.csv` 当交接真相源；Agent 禁止 Write 这些文件。静态配置与凭证除外。








> **职责说明（2026-09-01 精简）**：人工设置决策环节已删除（由 pipeline 参数覆盖：`--neutralization` A/B 实验、`--set key=value` 任意 settings 覆盖、profile `settings_proven` 已验证设置跟 win 走）。**本 skill 现仅两个职能**：① 解析 idea JSON → `build_alpha_list.py` 直写 expressions 表（S2→S3 的 DB 入库通道）；② 新区域合法设置选项快照（sim_options_snapshot）。

# brain-inspectRawTemplate-create-Setting

**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`，即工作区根下 `world-quant-brain-mcp/.venv`）。不要使用系统 Python。

本 skill 面向 **稳定、可重复的运行**。

## 衔接协议（上游来源 / 下游去向）

- **上游**：`brain-makeSomeGem`（trailSomeAlphas 流水线产出 `*_idea_*.json`，命名 `<dataset>_<region>_<delay>_idea_<ts>.json`，含 `template`/`idea`/`expression_list` 三键）；或用户手动提供的模板/idea JSON。增强模板不经过本 skill（见顶部说明）。
- **本 skill 输出**：`settings_candidates.json` + `alpha_list.json`（完整 alpha 对象，脚本追加式）+ **expressions 表（`data/wqb.db`，默认模式：`build_alpha_list.py` 直写，结构化真相源；S3 `pipeline.py --from-db` 默认读此表）**。
- **下游**：`alpha_list.json` 交 **brain-simAlphasinBatch-and-track** 批量回测（S3 编排器，执行后端为 `wq-brain-campaign-toolkit`）。

## 确定性流程（2026-09-01 精简后仅此一条路）

- **入口点**：`scripts/process_template.py` 处理初始流程（Part 1）→ 输出 `settings_candidates.json`（Region/Delay 的有效平台选项）。
- **入库**：调用 `scripts/build_alpha_list.py`，以 JSON 字符串传入设置（region/delay/universe/neutralization 必填）→ **追加**到 `alpha_list.json` 并直写 **expressions 表**（默认模式，S3 `pipeline.py --from-db` 读此表）。
- **设置取值**：跟随战役 `settings.json` / profile `settings_proven`（已验证设置跟 win 走）；A/B 实验与覆盖走 pipeline `--neutralization` / `--set`，不再在本环节做多组设置的人工决策循环。中性化必须始终选一个有效选项（不能为 None），可按需选用 Risk Neutralization。

## 配置 / 凭据检查（启动时）

要连接 BRAIN API（仅获取模拟选项时需要），通过以下任一方式提供凭据：
1. 环境变量：`BRAIN_USERNAME`（或 `BRAIN_EMAIL`）和 `BRAIN_PASSWORD`
2. 本文件旁的 `config.json`（见 `config.example.json`）
3. `~/secrets/platform-brain.json`（键：`email`/`password`）

切勿提交真实凭据。`config.json` 仅保留在本地。

## 运行步骤

**重要**：脚本依赖相对路径，请先切换到 skill 目录。

### 一键处理（推荐）
1. **切换到 skill 目录**：
   `cd "path/to/brain-inspectRawTemplate-create-Setting"`

2. **运行包装脚本**：
   使用包装脚本在专用文件夹（如 `processed_templates/<filename>/`）中生成所有产物。

   `$WQ_PY scripts/process_template.py --file <absolute_path_to_input_json>`

   *示例*：
   `$WQ_PY scripts/process_template.py --file "<下载目录>/fundamental28_GLB_1_idea_...json"`

此流程将：
1. 解析 idea 文件（`idea_context.json`）。
2. 获取模拟选项（若根目录下缺 `sim_options_snapshot.json`）。
3. 解析设置候选（`settings_candidates.json`）。
4. **停止并交还控制权给 AI**：AI 需读取 `idea_context.json` + `settings_candidates.json`，选定设置组合后手动调用 `build_alpha_list.py` 生成 `alpha_list.json`（每调用一次追加一次）。

### 手动步骤（调试）

在本文件夹下：

1. 解析 idea JSON
- `$WQ_PY scripts/parse_idea_file.py --input fundamental28_GLB_1_idea_1769874845978315000.json --out idea_context.json`

2. 获取模拟选项快照（需要凭据）
- `$WQ_PY scripts/fetch_sim_options.py --out sim_options_snapshot.json`

3. 解析设置
- `$WQ_PY scripts/resolve_settings.py --idea idea_context.json --options sim_options_snapshot.json --out resolved_settings.json`

4. 构建 Alpha 列表
- 从 `resolved_settings.json` 读取设置 JSON 字符串（或按步骤 3 决定新的组合），然后**以 JSON 字符串**传入。`region`、`delay`、`universe`、`neutralization` 为必填字段，缺失会抛 KeyError：
  `$WQ_PY scripts/build_alpha_list.py --idea idea_context.json --settings_json '{"region":"GLB","delay":1,"universe":"TOP3000","neutralization":"INDUSTRY"}' --out alpha_list.json`
- 可选字段及默认值：`decay`(0)、`truncation`(0.08)、`pasteurization`(ON)、`testperiod`(P0Y0M0D)、`unithandling`(VERIFY)、`nanhandling`(OFF)、`maxtrade`(OFF)。
- 脚本会**追加**到 `alpha_list.json`；若 idea 需要多组运行，可换其他设置组合重复执行。
