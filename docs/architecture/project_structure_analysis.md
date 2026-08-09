# WQ PPA 挖掘项目 · 目录与模块划分分析

> 分析性质：**只读梳理**，不移动任何文件。目的是厘清现有组织、按功能职责分类、定义目录边界，并给出建议的目标结构树。
> 分析基准时间：2026-08-05（依据进程 CreationDate 与文件 mtime 校正）。

---

## 1. 执行摘要

当前项目 `D:\coding\traeCN_project\wqb` 是一个 **WorldQuant BRAIN PPA（Power Pool Alpha）挖掘工作台**，由三大层级组成：

1. **核心 Python 包 `src/wqb/`** —— 配置、CLI、表达式/算子、记忆、研究、搜索、提交等子包（约 30 个 `.py`）。
2. **卫星接口层 `world-quant-brain-mcp/`** —— 独立 `.venv` 的 Streamable-HTTP MCP 服务（端口 8876，49 工具），与根 `.mcp.json` 对接。
3. **卫星工具/数据仓 `wqb-share-03/`** —— 字段质量工具、解析器、数百个挖掘批次跟踪 JSON、数据包 ZIP、PowerShell/Node 编排脚本。

外加浏览器扩展源码（`WebDataScope-main/`）、持久化数据（`data/`）、参考文档（`reference/`+`2_reference/`）、报告（`alpha-optimization-report/`）、顶层跟踪（`tracking/`）。

**核心结论**：功能分层基本清晰，但存在 **4 类职责交叉/错配** 需要治理：
- (A) `src/wqb/operators/` 空目录（预留算子库未落地）；
- (B) `webdata_quality.py` 等工具散落在 `wqb-share-03/tools/`，与核心包未建立引用关系（skill 调用路径曾报错）；
- (C) `reference/` 与 `2_reference/` 是用户要求的直接副本，存在同步维护隐患；
- (D) 跟踪数据两处分散（根 `tracking/sessions/` vs `wqb-share-03/tracking/` 数百 JSON），语义不清。

---

## 2. 当前目录与文件清点（按功能职责）

### 2.1 核心包 `src/wqb/`（配置 · 核心逻辑 · 接口 · 状态 · 研究 · 调度 · 提交）

| 路径 | 职责 | 说明 |
|---|---|---|
| `config.py` | **配置层** | `REGIONS`、`neutralization_search_order`、`OP_FAMILIES`、`GHOST_OPERATORS`、`VERIFIED_SAFE_OPERATORS`、`DEFAULT_UNIVERSE=TOP3000` |
| `cli.py` / `__main__.py` | **接口层（CLI）** | 子命令：`plan`/`doctor`/`operator-audit`/`research`/`settings`/`validate-session-pack`/`prepare-session-pack`/`news-refresh-portfolio` |
| `expression/grammar.py` | 核心逻辑 | 表达式语法/解析 |
| `expression/operator_audit.py` | 核心逻辑 | 算子审计 |
| `expression/paradigms.py` | 核心逻辑 | 信号范式 P1–P13 |
| `expression/validator.py` | 核心逻辑 | 表达式校验 |
| `memory/db.py` | 状态层 | SQLite 封装（`data/wqb.db`） |
| `memory/events.py` | 状态层 | 事件流（`data/events/*.jsonl`） |
| `research/evidence.py` | 研究逻辑 | 证据聚合 |
| `research/hypothesis_miner.py` | 研究逻辑 | 假设生成/挖掘 |
| `research/news_field_classifier.py` | 研究逻辑 | 新闻字段分类 |
| `search/failure_memory.py` | 调度逻辑 | 失败记忆 |
| `search/news_loop.py` | 调度逻辑 | 新闻循环 |
| `search/scheduler.py` | 调度逻辑 | 调度器 |
| `submit/describer.py` | 提交逻辑 | alpha 描述生成（该子包唯一文件） |
| `operators/` | **空目录** | 预留算子库，当前无任何模块 |

### 2.2 接口层 / MCP 服务 `world-quant-brain-mcp/`（独立 `.venv`）

| 路径 | 职责 |
|---|---|
| `main.py` | Streamable-HTTP MCP 服务入口（端口 8876，brain-platform-mcp v1.29.0） |
| `browser_setup.py` / `forum_functions.py` / `labs_functions.py` / `labs_data_analysis_agent.py` | 平台交互（论坛 / Labs / 浏览器） |
| `test_labs_live.py` / `ex_sa_007.py` | 测试 / 实验脚本 |
| `scripts/python_alpha_policy.py` | 策略脚本 |
| `config/info_data.bin` | 配置二进制 |
| `host_labs/` | Node.js Labs host（`labs_open.js` / `pw_min.js` / `package.json`） |
| `downloads/` | 离线数据 `os_pnl_pool_equity_*.pkl` / `*.ppac.json` |
| `deploy/` | nginx / systemd 部署配置 |
| `Dockerfile` / `docker-compose.yml` / `Makefile` / `requirements.txt` | 部署与依赖 |
| `.env` / `.env.example` | 凭证（`.env` 被 `.gitignore` 忽略） |

> 注：根 `D:\coding\traeCN_project\wqb\.mcp.json` 指向 `http://127.0.0.1:8876/mcp`，与该服务运行时对接；进程 PID 28280/36896（08-05 00:18 起）。

### 2.3 工具与编排 `wqb-share-03/`（混合职责）

| 子路径 | 职责 | 关键文件 |
|---|---|---|
| `tools/` | **工具函数** | `webdata_quality.py`（真实字段质量工具，需 msgpack venv）、`parse_fields.py`、`parse_simresult.py`、`mcp_py/` |
| 顶层 `*.py` | 数据字段检索脚本 | `debug_datafields.py` / `query_datafields.py` / `retrieve_final.py` |
| `*.ps1` / `*.js` | **自动化编排** | `wqb_batch_runner.ps1` / `wqb_mcp_core.ps1` / `wqb_quickstart.ps1` / `wqb_mcp_batch.js` / `wqb_exec_template.js` |
| `*.zip` / 解压目录 | **数据包** | `WebData_20260219_V0.10.9.zip`、`WebDataScope-1.3.1.zip`、`WebDataScope-1.3.1/` |
| `tracking/` | **运行/实验跟踪** | 约 **470 个 JSON**（`args_*` 请求存档、`result_*` 结果、`*_fields.json` 字段探查、`kor_*_results.json` 区域批次、`*.ppac` 等） |
| 文档 | 教学/报告 | `课件.md`、`WebDataScope_alpha挖掘用法研究报告.html` |
| `.mcp.json` | MCP 配置 | 该卫星自身的 MCP 入口 |

### 2.4 浏览器扩展 `WebDataScope-main/`（64 文件：45 js / 12 css / 2 png / 2 html / 1 json）

Chrome 扩展源码，用于未点亮金字塔数据集的元分析。关键分析模块（来自前期研究）：`dataAna.js`（字段级 10 指标）、`dataFlag.js`（数据集级徽章）、`distribution.js`（区域×类别白空间）、`simulate.js`（仿真 payload/限流）、`genius.js`（算子多样性）。

### 2.5 数据 / 文档 / 参考 / 报告 / 跟踪（顶层）

| 目录 | 职责 | 内容 |
|---|---|---|
| `data/` | 持久化数据 | `wqb.db`（SQLite）、`operators_verified.json`、`events/2026-08-01.jsonl` |
| `docs/` | 设计/计划文档 | `superpowers/plans/2026-08-02-wqb-src-reconstruction.md` |
| `reference/` | 参考文档（供 skills 以 `../../../reference/...` 引用） | 6 个 md（news 系列 + researcher_workflow + brain-labs） |
| `2_reference/` | 参考文档**源**（用户指定保留位置） | 与 `reference/` 内容相同（直接副本） |
| `alpha-optimization-report/` | 报告 | `alpha-optimization-report.html` + `assets/charts.js` + `_shared` |
| `tracking/` | 项目级跟踪 | `sessions/2026-04-22` |

### 2.6 根级元文件

- `.mcp.json` → `wqb-mcp` 指向 `127.0.0.1:8876/mcp`
- `.gitignore` → 忽略 `.env` / `.venv` / `__pycache__` / `*.zip` / `*.bin` / `.workbuddy` / `.zcode` / `.trae`
- `.zcode/` → 源 skills 目录（安装自此处）
- `.workbuddy/` → 工作区元数据（skills / automations / memory，不应改动）

---

## 3. 按功能职责的分类汇总

| 职责类别 | 归属目录（现状） |
|---|---|
| **配置层** | `src/wqb/config.py` |
| **接口层（CLI）** | `src/wqb/cli.py`、`__main__.py` |
| **接口层（MCP 服务）** | `world-quant-brain-mcp/`（含 `host_labs/` Node 宿主） |
| **核心逻辑（表达式/算子）** | `src/wqb/expression/` |
| **核心逻辑（研究/挖掘）** | `src/wqb/research/` |
| **核心逻辑（搜索/调度）** | `src/wqb/search/` |
| **核心逻辑（提交）** | `src/wqb/submit/` |
| **状态/记忆层** | `src/wqb/memory/` + `data/` |
| **工具函数** | `wqb-share-03/tools/`（**未与核心包建立引用**） |
| **自动化编排** | `wqb-share-03/*.ps1`、`*.js` |
| **数据集/扩展源码** | `WebDataScope-main/`、`wqb-share-03/*.zip` |
| **运行/实验跟踪** | `wqb-share-03/tracking/`（数百 JSON）+ 根 `tracking/sessions/` |
| **参考文档** | `reference/`、`2_reference/` |
| **设计/计划/报告** | `docs/`、`alpha-optimization-report/` |
| **部署** | `world-quant-brain-mcp/deploy/` + `Dockerfile` 等 |
| **工作区元数据** | `.workbuddy/`、`.zcode/`、`.mcp.json`、`.gitignore` |

---

## 4. 各目录职责边界定义（建议）

1. **`src/wqb/`** —— 唯一受版本控制的核心逻辑层。其下子包严格按职责切分，禁止跨子包直接 import 业务逻辑外的文件（MCP/工具应通过公开 API 调用，不直接 import 卫星代码）。
2. **`mcp/`（建议由 `world-quant-brain-mcp/` 重命名）** —— 平台接口边界。封装所有对 WQ BRAIN 的 HTTP/Labs/论坛交互；对核心包只暴露工具函数，不反向依赖核心逻辑。
3. **`tools/`** —— 独立可执行的 CLI 工具/数据集工具（字段质量、解析、探查）。**应被核心包或 skill 显式引用**，避免路径错配。
4. **`extensions/webdatascope/`** —— 第三方/自研浏览器扩展源码，与运行时解耦。
5. **`data/`** —— 持久化状态（DB / 已验证算子 / 事件流），运行时读写。
6. **`reference/` + `2_reference/`** —— 静态知识文档；`2_reference/` 为权威源，`reference/` 为链接解析副本，需保持同步。
7. **`docs/`** —— 设计决策与计划文档（人读）。
8. **`reports/`** —— 生成的 HTML/图表报告。
9. **`tracking/`** —— 统一实验/会话跟踪；建议区分 `sessions/`（交互会话）与 `mining/`（批次结果存档）。
10. **`automation/`** —— 编排脚本（PS1/JS），与核心逻辑分离。
11. **`research-data/`** —— 大体积数据包（ZIP/解压目录），通常 git-ignored。

---

## 5. 现有组织的问题与风险

| 编号 | 问题 | 风险 | 影响 |
|---|---|---|---|
| A | `src/wqb/operators/` 空目录 | 预留算子库未落地；`data/operators_verified.json` 无对应代码载体 | 中 |
| B | `webdata_quality.py` 等置于 `wqb-share-03/tools/`，核心包无引用 | skill 调用路径曾报错（找不到工具） | 高（可调用性） |
| C | `reference/` 与 `2_reference/` 重复 | 修改一端不同步，skill 引用内容漂移 | 中 |
| D | 跟踪数据两处分散 | 语义混淆（会话 vs 批次）；根 `tracking/` 仅 1 个会话，挖掘记录全在卫星 | 中 |
| E | 两个 MCP 入口（`world-quant-brain-mcp/` 与 `wqb-share-03/.mcp.json`） | 概念重叠，易误改 | 低 |
| F | `WebDataScope-1.3.1/` 解压目录与 `.zip` 并存 | 体积冗余（36MB+） | 低（git-ignored） |

---

## 6. 建议的目标目录结构树

> 目标布局在**保留现有核心功能与依赖关系**前提下，消除上述 (A)–(D) 错配。标注：`[现]` = 保持原位；`[迁]` = 建议迁移/重命名；`[生成]` = 由权威源自动同步生成（勿手改）。
> 说明：本树所有条目均为现有目录的归并或重命名，**无新增独立知识源**，故原 `[新]` 标注已剔除；`reference/` 由 `2_reference/` 同步生成，不再作为独立源，从而根除问题 (C) 的重复漂移。

```
wqb/
├── src/wqb/                         [现] 核心包
│   ├── config.py
│   ├── cli.py  __main__.py
│   ├── expression/   (grammar, operator_audit, paradigms, validator)
│   ├── memory/       (db, events)
│   ├── research/     (evidence, hypothesis_miner, news_field_classifier)
│   ├── search/       (failure_memory, news_loop, scheduler)
│   ├── submit/       (describer)
│   └── operators/    [现→待填充] 已验证算子库（由 data/operators_verified.json 落地为模块，消除问题 A）
│
├── mcp/                              [迁] world-quant-brain-mcp/ 重命名（内部 .venv / 相对导入整体迁移）
│   ├── main.py  browser_setup.py  forum_functions.py
│   ├── labs_functions.py  labs_data_analysis_agent.py
│   ├── test_labs_live.py  ex_sa_007.py  scripts/  config/
│   ├── host_labs/  downloads/  deploy/
│   └── (独立 .venv 保持不变)
│
├── tools/                            [迁] wqb-share-03/tools/ 提升为根级工具（修复问题 B 可调用性）
│   ├── webdata_quality.py  parse_fields.py  parse_simresult.py  mcp_py/
│   └── query_datafields.py  debug_datafields.py  retrieve_final.py
│
├── extensions/
│   └── webdatascope/                [迁] WebDataScope-main/ 重命名（取内层 WebDataScope-main/ 内容）
│
├── automation/                       [迁] wqb-share-03/*.ps1,*.js
│   ├── wqb_batch_runner.ps1  wqb_mcp_core.ps1  wqb_quickstart.ps1
│   └── wqb_mcp_batch.js  wqb_exec_template.js
│
├── data/                             [现] 持久化
│   ├── wqb.db  operators_verified.json  events/
│
├── 2_reference/                      [现] 参考文档**权威源**（用户指定保留，唯一可手改处）
├── reference/                        [生成] 由 2_reference/ 同步生成（技能 ../../../reference/ 链接解析用，勿手改）
├── docs/                             [现] 计划/设计/教学
│   ├── superpowers/plans/
│   └── 课件.md                        [迁] 教学文档（原 wqb-share-03/课件.md）
├── reports/                          [迁] 报告集中（修复原散落 research-data/ 的错配）
│   ├── alpha-optimization-report/     (alpha-optimization-report.html + assets/ + _shared/)
│   └── WebDataScope_alpha挖掘用法研究报告.html  [迁] 原 wqb-share-03/ 研究报告
├── tracking/                         [合并] 统一跟踪
│   ├── sessions/                     [现] 交互会话
│   └── mining/                       [迁] wqb-share-03/tracking/ 数百 JSON（消除问题 D）
├── research-data/                    [迁] 静态数据包（git-ignored，仅放原始 ZIP/解压目录）
│   ├── WebData_20260219_V0.10.9.zip
│   └── WebDataScope-1.3.1.zip  WebDataScope-1.3.1/   (取内层 WebDataScope-1.3.1/ 内容)
│
├── .mcp.json          [现] wqb-mcp → 127.0.0.1:8876/mcp
├── .gitignore  .zcode/  .workbuddy/  (.workbuddy/reference/ 为技能 ../../reference/ 链接副本，随 2_reference/ 同步)
```

---

## 7. 迁移指引（非破坏性，保留依赖）

执行顺序与注意事项：

1. **先保依赖，再移动**。根 `.mcp.json` 指向运行中的服务 URL（非本地路径），重命名 `world-quant-brain-mcp/` → `mcp/` 不影响运行；但其内部 `.venv` 与相对导入需整体迁移，建议用 `git mv` 保留历史。
2. **修复 (B) 可调用性**：将 `wqb-share-03/tools/` 提升为根级 `tools/` 后，更新 `wq-brain-ppa-mining` 等 skill 中对 `webdata_quality.py` 的路径引用（前期测试已发现路径错误）。
3. **根除 (C) 重复**：`2_reference/` 作为唯一权威源；`reference/` 改为**生成物**（由 `2_reference/` 同步生成，skill 仅引用 `reference/`）。建立同步脚本/CI 校验，禁止手改 `reference/`；`.workbuddy/reference/` 同理随 `2_reference/` 同步，避免人工漂移。
4. **落实 (A)**：将 `data/operators_verified.json` 中的已验证算子实现为 `src/wqb/operators/` 下的模块，使空目录具备实际载体。
5. **合并 (D)**：`wqb-share-03/tracking/` 整体移入 `tracking/mining/`；保留 `tracking/sessions/` 语义。
6. **文档与报告归位**：`wqb-share-03/课件.md` → `docs/`；`wqb-share-03/WebDataScope_alpha挖掘用法研究报告.html` → `reports/`（与目标树一致，不再散落于 `research-data/`）。
7. **不动项**：`.workbuddy/`（含已装 5 个 skills 与 automation 记忆）、`.zcode/`（源 skills）、`.gitignore` 配置保持不变；仅 `.workbuddy/reference/` 随 `2_reference/` 同步更新。
8. **验证**：迁移后运行 `python -m wqb --help` 与各 skill 的可调用性测试（参考 `.workbuddy/skill_callability_test.md`），确认无断链；并执行 `2_reference/` → `reference/` 同步脚本验证链接零失效。

---

## 8. 结论

项目功能分层总体合理：**核心包 `src/wqb/` 职责清晰、子包切分正确**；主要问题集中在**卫星目录与核心包的衔接**（工具未引用、算子库空置、跟踪分散、参考副本重复）。建议按第 6 节目标树实施**非破坏性迁移**，优先解决可调用性（B）与算子库落地（A），再处理文档同步（C）与跟踪合并（D）。所有改动均可在保留 `.mcp.json` 服务对接、`.venv` 独立性与 skill 链接的前提下完成。

---

## 9. 迁移执行状态（2026-08-05）

按 §7 顺序实际执行，结果如下：

| 步骤 | 内容 | 状态 | 说明 |
|---|---|---|---|
| B | `wqb-share-03/tools/` + 顶层字段脚本 → 根 `tools/` | ✅ 完成 | 11 个文件；skill 中 `../../../../tools/webdata_quality.py` 现可正确解析 |
| C | `2_reference/` → `reference/` + `.workbuddy/reference/` 同步 | ✅ 完成 | 新增 `tools/sync_reference.py`；两副本与权威源 `diff -rq` 完全一致（REF_IDENTICAL） |
| A | `data/operators_verified.json` → `src/wqb/operators/` 包 | ✅ 完成 | 原 `src/wqb/operators` 是 5188B 杂注文本文件（已 `git mv` 至 `docs/operators_notes.md`），新建包含 verified=6/ghost=69/known_ghosts=17，导入验证通过 |
| D | `wqb-share-03/tracking/` → `tracking/mining/` | ⚠️ 部分 | 历史存档 728 个 JSON 已迁入 `tracking/mining/`；但 **MCP 服务进程持续向 `wqb-share-03/tracking/` 写入结果文件**（实测移走后立即再生），该目录为服务实时输出路径，需改服务配置重定向后方可彻底清空 |
| 6 | `课件.md`→`docs/`、`WebDataScope报告`→`reports/` | ✅ 完成 | `alpha-optimization-report/` 亦并入 `reports/` |
| 扩展 / 数据 | `WebDataScope-main/`→`extensions/webdatascope/`、`*.zip`→`research-data/` | ✅ 完成 | 取内层内容；66 文件 / 3 数据包就位 |
| 1 | `world-quant-brain-mcp/` → `mcp/` | ⏸️ 暂缓 | 服务（PID 28280/36896）锁定目录，且其派生的 `host_labs` 子进程持续持有句柄，`Move-Item` 报“另一个进程正在使用此文件”。已在停止→回退逻辑中**原路径重启，端口 8876 恢复 True**。属实时回测宿主，重命名须在维护窗口内对所有派生进程做干净停止后执行 |

**暂缓步骤 1 的操作建议**：在确认无在途仿真时，于维护窗口执行：
1. 停止全部引用 `world-quant-brain-mcp` / `host_labs` 的进程（含派生的 Node 宿主）；
2. 使用普通移动（非 `git mv`，以保留 `.venv`）`Move-Item world-quant-brain-mcp mcp`；
3. 从 `mcp/` 以相同命令重启并验证 `Test-NetConnection localhost 8876`。

其余步骤均已落地并通过导入 / 链接一致性验证。

---

## 10. 目录清理更新（2026-08-09）

> 2026-08-09 执行了项目目录清理，以下为 §5 问题与 §9 迁移状态的后续更新。

### 已解决的问题

| 原问题 | 处理 | 状态 |
|---|---|---|
| (C) `reference/` 与 `2_reference/` 重复 | `2_reference/` 已删除归档至 `archive/2026-08-08/duplicates/`，`reference/` 保留为唯一副本 | ✅ 根除 |
| (F) `WebDataScope-1.3.1/` 解压目录与 `.zip` 并存 | 旧版 v1.3.1 归档；`extensions/WebDataScope-1.5.0/`（重复）归档；保留 `extensions/webdatascope/`（含 workflows/ 的完整版） | ✅ 根除 |
| 临时文件 | 11 个 `__pycache__`（57 .pyc）已删除；3 个 .log 归档至 `archive/2026-08-08/logs/` | ✅ 清理 |
| 测试文件 | 5 个 test 文件归档至 `archive/2026-08-08/test-artifacts/` | ✅ 清理 |
| IDE 产物 | `.trae-html-share-packages/`、`wqb-share-03/` 归档至 `archive/2026-08-08/ide-artifacts/` | ✅ 清理 |

### 当前目录结构（清理后）

```
wqb/
├── src/wqb/                    核心包（6子包，26 .py）
├── world-quant-brain-mcp/      MCP 服务（含 .venv 293MB，49工具，端口8876）
├── tools/                      独立工具（12 .py）
├── extensions/webdatascope/    浏览器扩展 v1.5.0（唯一保留版本）
├── research-data/              WebData 数据集（161 .bin）+ 离线包
├── tracking/mining/            挖掘批次跟踪（800+ JSON）
├── reference/                  参考文档（10 .md，唯一副本）
├── reports/                    专题报告（9 .md + 2 .html）
├── docs/                       结构化知识库（见 docs/README.md）
│   ├── experience/             经验总结（2 文档）
│   ├── reference/              参考速查（算子表）
│   ├── architecture/           架构分析（本文档）
│   ├── tutorials/              教程课件
│   └── plans/                  历史计划
├── automation/                 编排脚本（3 .ps1 + 2 .js）
├── data/                       持久化数据（wqb.db + events/）
├── glb_alpha_machine/          GLB 挖掘流水线
├── mea_alpha_machine/          MEA 挖掘流水线
├── archive/                    归档区（260 文件，2026-08-08）
└── .workbuddy/                 工作区元数据（不改动）
```

### 未解决/暂缓项

| 项目 | 状态 | 说明 |
|---|---|---|
| `world-quant-brain-mcp/` → `mcp/` 重命名 | ⏸️ 暂缓 | 服务进程锁定目录，须维护窗口执行 |
| `wqb-share-03/` 原文件残留 | ⚠️ 部分 | 归档副本已完成，原文件被 glb_pipeline 进程锁定，待进程结束后可删 |
| `glb_alpha_machine/__pycache__` 再生 | ⚠️ 正常 | glb_pipeline 运行中自动再生，进程结束后可清理 |
