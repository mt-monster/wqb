# wqb 项目代码组织与文件内容全面分析报告

> 分析时间：2026-08-23
> 方法：AST 静态解析（153 个 Python 文件 / 26,967 LOC）+ 核心文件抽样精读 + 依赖/重复扫描
> 范围：代码目录 `src/ world-quant-brain-mcp/ tools/ pipeline/ mining/ database/ polling/ tests/` 及根级 `.py`
> 排除（非源码/生成物/归档）：`tracking/`（数据湖）、`research-data/`（生成物）、`extensions/`（前端 js）、`reports/`、`attic/`（归档）、`logs/`

---

## 1. 整体规模与目录结构

| 顶级代码目录 | 文件数 | LOC | 角色定位 |
|---|---:|---:|---|
| `world-quant-brain-mcp/` | 34 | 10,028 | MCP 服务（BRAIN API 客户端 + 回测/提交/论坛工具），**占代码总量 37%** |
| `tools/` | 43 | 6,378 | 工具化 CLI 族（门禁/状态/探针/提交/组套），替代散落的一次性脚本 |
| `src/wqb/` | 19 | 2,971 | **规范核心包**（single source of truth）：域常量/表达式/研究/搜索/记忆 |
| `database/` | 9 | 2,086 | DAO 数据访问层（DatabaseManager + BaseDAO/RegionDAO…） |
| `pipeline/` | 11 | 1,944 | 战役 pipeline（campaign_pipeline / regions / core） |
| `tests/` | 16 | 1,936 | pytest 单测（根 16 文件，254→264 用例全绿） |
| `mining/` | 15 | 614 | 挖掘脚本与诊断（探索类） |
| 根级散落 `.py` | 4 | 939 | `wqb_db_mcp.py`(551) + `track_mea_super*.py`(3) + `probe_kor_sa.py`(58) |

**最大文件（重构候选）**

| LOC | 文件 | 备注 |
|---:|---|---|
| 1,898 | `world-quant-brain-mcp/labs_data_analysis_agent.py` | 单文件职责过重 |
| 1,087 | `world-quant-brain-mcp/brain_mixin_simulation.py` | |
| 943×2 | `brain_mixin_correlation.py` / `brain_mixin_spcread.py` | |
| 810 | `src/wqb/expression/diversity_enhancer.py` | |
| 733 | `tools/webdata_quality.py` | |
| 610 | `world-quant-brain-mcp/tools_sim.py` | |
| 551 | `wqb_db_mcp.py` | 根级散落，见 §6 P0 |

---

## 2. 核心文件职责与模块划分

### 2.1 `src/wqb/`（规范核心，标杆级）
- `config.py`（332 LOC）：**区域搜索空间、算子家族、幽灵算子黑名单、WebDataScope 闸门、并发口径的单一事实源**。质量上乘——分节清晰、类型注解、docstring 完备，并显式固化此前审计发现的"Sharpe 1.58/1.5/1.28/1.1 四值并存"问题（`GATES_INTERNAL/GATES_PLATFORM` 集中管理）。**这是本项目架构纪律的范本。**
- `expression/`（diversity_enhancer / grammar / operator_audit / validator）：表达式多样性增强、语法、算子审计、校验。
- `memory/`（db / events / idea_ledger / idea_store）：研究记忆与想法台账（SQLite 支撑）。
- `research/`（evidence / hypothesis_miner / news_field_classifier）、`search/`（failure_memory / scheduler）：研究假设挖掘与失败记忆调度。

### 2.2 `world-quant-brain-mcp/`（MCP 服务，API 客户端）
- `brain_api.py`（36 行）：**纯门面**。仅继承 5 个 mixin（`Transport/Auth/Simulation/SpcData/Correlation`），保持 `BrainApiClient` 类名与 `brain_client` 单例及旧导入路径不变。设计正确。
- `brain_mixin_*.py`：方法体按职责切片到此（`brain_mixin_simulation.py` 含 `create_simulation`/`batch_create_simulations` 等）。
- `brain_api_models.py` / `brain_config.py`：Pydantic 模型 / 配置加载。
- `mcp_core.py`（356）：MCP 工具注册与分发。
- `tools_*.py`（account/alpha/corr/data/forum/labs/sim/spc/submit/config）：各业务域工具原语。
- `labs_*.py` / `create_super_alpha.py` / `super_alpha_tool.py`：Labs 与 SuperAlpha 特性。
- `配置前运行我_安装必要依赖包.py`：**中文命名文件**（docstring 仍写 `check_install_packages.py`），且硬编码 `REQUIRED_PACKAGES` 与 `requirements.txt` 重复（见 §6 P1）。

### 2.3 `tools/`（工具化 CLI 族，替代一次性脚本）
- `wave_gate.py` / `batch_status.py` / `sa_probe.py` / `submit_verdict.py` / `super_build.py`：AGENTS.md §6 规定的工具化替代物。
- `gate.py`：区域无关通用提交前闸门（从 `src/wqb/config` 取权威算子表，从 skill 目录注入 verifier）。
- `mcp_5slot_batch.py`：经 SSE 调 MCP 的五槽批量提交客户端。
- 其余：`webdata_quality` / `expr_lint` / `corr_precheck` / `scan_fields` / `migrate_*` 等专项工具。

### 2.4 `pipeline/` / `database/` / `mining/` / `polling/`
- `pipeline/`：战役编排（`core/campaign_pipeline.py` 584 LOC、`regions/`、`core/`）。
- `database/`：DAO 层（`dao.py` 经 `db_manager` 抽象；另有 `init_db`/`migrate`/`full_migrate`/`integration`/`adapter`）。
- `mining/`：挖掘与诊断脚本（探索类，614 LOC）。
- `polling/`：6 个 `.sh` shell 轮询脚本（71 LOC，运维侧）。

### 2.5 根级散落
- `wqb_db_mcp.py`（551）：**DB 查询 MCP 服务**（FastMCP + 直连 `data/wqb.db`），即 AGENTS.md §5 的"wqb-db MCP 工具"根因修复件。
- `track_mea_super*.py`（3 个）、`probe_kor_sa.py`：已被 `tools/super_build.py`、`tools/sa_probe.py` 取代的遗留一次性脚本（见 §6 P0）。

---

## 3. 模块间依赖关系

**Import 图关键事实（AST 解析）**
- `brain_api` 被 **32 次** import —— 确认为中央客户端门面，下游（tools/submits、track_*.py、pipeline）均依赖它发起平台交互。
- `wqb.config` 被 **6 次** import（`tools/gate.py`、`pipeline`、`expression` 等）—— 域常量单一事实源生效。
- `wqb.expression.*`（diversity_enhancer / grammar）被 pipeline/memory 引用 —— 表达式子系统被复用，耦合合理。
- 基线文件名无跨目录功能冲突（仅 `__init__.py`×12、`conftest.py`×2，属正常）。

**分层（理想态）**
```
src/wqb (域常量/表达式/记忆)         ← 被依赖方，无反向依赖
        ↑
world-quant-brain-mcp (API 客户端)   ← 平台交互唯一出口
        ↑
tools/ · pipeline/ · 根级脚本         ← 编排/CLI 消费层
```

**现实缺陷**：消费层大量使用 `sys.path.insert(0, ...)` 注入路径来 import（如 `tools/gate.py` 注入 `tools/lib` 与 `src` 根；`track_mea_super.py` 注入 `world-quant-brain-mcp`；`wqb_db_mcp.py` 依赖 `ROOT` 推导）。这是一种**脆弱的环境耦合**，使模块不可作为包安装/测试，违背分层理想。

---

## 4. 七维度质量评估

| 维度 | 评级 | 依据 |
|---|---|---|
| 可读性 | **良** | `config.py` 标杆级；docstring/类型注解普遍；但存在 emoji 日志（`🚀`）、`lookINTO_SimError_message` 驼峰命名不一。 |
| 可维护性 | **中** | 分层方向正确、有工具化纪律；但**两套 DB 层**、`sys.path` 注入、根目录散落脚本削弱一致性。 |
| 性能 | **良** | 仿真/提交采用异步 + 429 退避（`batch_create_simulations` 内置退避与限流缓冲）；无显著瓶颈。风险点见 DB 并发。 |
| 重复代码 | **中高** | 两套 DB 访问层；多条提交入口（MCP/CLI/SSE）；`track_mea_super*` 与 `tools/super_build` 功能重叠未清理。 |
| 命名规范 | **中** | 前缀基本统一（`brain_`/`wq_`/`wqb_`）；但中文文件名、`lookINTO` 驼峰、emoji 日志属不一致。 |
| 错误处理 | **良（基调）** | **0 处裸 `except:`**；批量操作采用 "try/except 每 item、记录 error 字符串、继续" 的弹性模式。但 **13 处 `except ...: pass` 静默吞异常**（含 `src/wqb/expression/diversity_enhancer.py`、`brain_mixin_*`），且 mixin 普遍高频 `except Exception`（correlation 26、spcread 19、transport 17、simulation 16 次）—— 过宽捕获会掩盖根因、降低可调试性。 |
| 架构设计 | **方向正确，执行有债** | SSoT + facade + 工具化纪律已落地，整体可演进；但 DB 层分裂、提交入口多、根目录散落削弱架构纯净度。 |

---

## 5. 技术债务与冗余清单（按严重度）

### 🔴 P0 — 架构级，建议优先解决
1. **两套并行数据库访问层**
   - `wqb_db_mcp.py` 用 `sqlite3.connect(str(DB_PATH))` **直连** `data/wqb.db`；
   - `database/` 包用独立的 `DatabaseManager`/`dao.py` 抽象层，同样指向 `wqb.db`。
   - 二者连接机制互不兼容，作用于同一 SQLite 文件 → **并发写冲突、schema 漂移、查询逻辑重复**风险。须收敛为单一 DB 层。
2. **根目录遗留一次性脚本未清理**
   - `track_mea_super.py` / `track_mea_super_submit.py` / `track_mea_super_resume.py` 已被 `tools/super_build.py` 取代；`probe_kor_sa.py` 已被 `tools/sa_probe.py` 取代。
   - 按 AGENTS.md §6 纪律，应归档至 `attic/`，不在活跃目录累积。

### 🟠 P1 — 明确冗余/混乱
3. **中文命名文件 + 依赖硬编码**
   - `world-quant-brain-mcp/配置前运行我_安装必要依赖包.py`：文件名违规（非 ASCII、含指令）；docstring 仍为 `check_install_packages.py`；`REQUIRED_PACKAGES` 硬编码与 `requirements.txt` 重复（双重维护源）。
4. **多条提交入口并行**
   - MCP `tools_submit.submit_alpha`、CLI `tools/submit_batch.py`（`build_payload`/`run`）、`tools/mcp_5slot_batch.py`（SSE 客户端）三者最终都提交 alpha，payload 构造/轮询逻辑可能重复。
5. **`sys.path.insert` 路径注入**（`gate.py`/`track_*.py`/`wqb_db_mcp.py` 等）：环境耦合，不可打包、难移植。

### 🟡 P2 — 局部改善
6. **超大文件**：`labs_data_analysis_agent.py`(1898)、`brain_mixin_simulation`(1087)、`brain_mixin_correlation/spcread`(943×2)、`diversity_enhancer`(810) 单文件职责偏重，可再拆。
7. **13 处 `except ...: pass` 静默吞异常**：应至少记录日志。
8. **命名/风格不一**：`lookINTO_SimError_message` 驼峰混排、emoji 日志。

---

## 6. 结论：是否需要优化 & 优先方向

**结论：需要优化，但属于可控演进，而非推倒重来。**
项目的**架构方向是正确的**——规范核心 `src/wqb/config.py` 的单一事实源、客户端 `brain_api` 的纯门面 + mixin 切片、`tools/` 工具化纪律、异步 + 429 退避、根测试 264 全绿，都表明工程基线健康。问题集中在**少数高杠杆的架构债**（DB 层分裂、遗留脚本、提交入口多）与**局部规范不一致**，不影响业务正确性，但会持续侵蚀可维护性与可移植性。

**优先优化方向（按 ROI 排序）**

| 优先级 | 方向 | 具体动作 | 预期收益 |
|---|---|---|---|
| **① 最高** | 统一 DB 访问层 | 让 `wqb_db_mcp.py` 复用 `database/` 的 `DatabaseManager`/DAO（或反之），消除双 `sqlite3.connect`；收敛 schema 与并发模型 | 消除并发冲突与逻辑重复，单一事实源 |
| **② 高** | 清理根目录遗留 | `track_mea_super*.py`/`probe_kor_sa.py` 归档 `attic/`；中文文件改名 `check_install_packages.py` 并改为读 `requirements.txt`（去硬编码） | 活跃目录纯净、消除双重维护 |
| **③ 中** | 收敛提交入口 | 明确 MCP `submit_alpha` 为唯一提交原语；`tools/submit_batch` 与 `mcp_5slot_batch` 复用 `brain_api`，避免重复 payload 构造 | 减少重复、统一行为 |
| **④ 中** | 消除 `sys.path` 注入 | 改为可安装包或稳定相对导入 + 环境变量配置 | 可移植、可测试、可打包 |
| **⑤ 低** | 局部打磨 | 拆分超大文件；清理 `except: pass` 加日志；统一命名（去 emoji、`lookINTO`→`lookup_simulation_error_message`） | 可读性/一致性提升 |

**综合判断**：当前**不应**做大规模重构；建议以 ① ② 为切入点，在保持 264 测试全绿与 pre-commit 门禁的前提下，按上表小步推进。优先级 ① 的 DB 层统一是收益最高、风险最需管控的一项（涉及 `data/wqb.db` 并发，改动前须备份并做回归）。
