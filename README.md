# wqb — WorldQuant BRAIN Alpha 挖掘工作区

面向 WorldQuant BRAIN 平台的量化研究工作台：以 Python 脚本驱动 alpha 的挖掘、回测、评审与提交，以 MCP 服务作为与编码 Agent 的主要接口，以 SQLite 作为战役产物的单一事实源。

> **文档分工**
> - **本文件（README.md）** —— 面向人：项目是什么、如何上手、去哪找东西。
> - **[AGENTS.md](AGENTS.md)** —— 面向 AI Agent：硬约束、九步流水线细节、反模式与变更影响面。**动手前必读。**
> - **[CLAUDE.md](CLAUDE.md)** —— Claude Code 宿主的常驻上下文：alpha 挖掘准则（启发式）。
>
> 三份文档定位不重叠；新增治理约定一律进 AGENTS.md，勿三处各写一份。

---

## 1. 30 秒理解这个项目

```
平台数据 ──► S-PRE 查表 ──► S0 体检 ──► S1 字段 ──► S2 生成 ──► S3 七槽回测
                                                                      │
                                                                      ▼
                              提交 ◄── S5 判定 ◄── S4 诊断 ◄── 结果入库
                                                                      │
                                                                      ▼
                                                          S6 复盘回写（闭环）
```

- **一套流水线，多区域复用**：14 个区域（`src/wqb/config.py::REGIONS`，已启用 12 个 profile）共用同一套九步骨架，区域差异通过 profile 注入。
- **产物只进数据库**：expressions / gate_results / backtest_results / wave_results / ledger 全部落在 `data/wqb.db`，不散落 JSON/CSV。
- **技能即执行器**：流水线各步由 skills 承载，禁止手写一次性脚本替代（见 §5）。

---

## 2. 架构总览

自底向上分四层，**依赖只允许向下**：

```
┌─────────────────────────────────────────────────────────────────┐
│  ④ 知识/编排层  Claude/skills/（32 个 SKILL.md）                  │
│     L-RA 唯一编排 SOP（wq-brain-ra-pipeline 九步流水线）           │
│     L-PRE 选区查表 · L-TOOL 战役引擎 · L0–L7 各环节专用技能        │
├─────────────────────────────────────────────────────────────────┤
│  ③ 服务层      两个 MCP 服务器（stdio，.mcp.json 注册）            │
│     wq-brain-http：69 个平台交互工具（回测/提交/相关性/论坛）      │
│     wqb-db：战役数据库读写工具（计数见 INDEX）                     │
│     workflow 引擎：19 个注册节点（src/wqb/workflow/registry.py）   │
├─────────────────────────────────────────────────────────────────┤
│  ② 客户端层    world-quant-brain-mcp/                             │
│     brain_api.py 门面 → 5 个 brain_mixin_*（transport/auth/       │
│     simulation/spcread/correlation，verbatim 拆解）               │
│     tools_*.py 按域分组注册 MCP 工具；自带 429 退避与配额纪律      │
├─────────────────────────────────────────────────────────────────┤
│  ① 核心包      src/wqb/（single source of truth）                 │
│     config（区域/算子/中性化域常量）· expression（语法/骨架/        │
│     算子审计）· store（CampaignStore 十张表的唯一落库入口 +         │
│     submit_queue 提交队列）· workflow（节点注册与执行）·            │
│     research（OS 衰减/假设挖掘）· modeb（Mode B 自适应改进）        │
└─────────────────────────────────────────────────────────────────┘
        ▲ 数据层：data/wqb.db（SQLite，~223 MB，幂等迁移）
        ▲ 工具层：tools/（139 个 CLI，索引见 tools/README.md）
```

### 关键设计决策

| 决策 | 内容 | 守护机制 |
|---|---|---|
| 单源核心 | 区域/算子/中性化域常量只在 `src/wqb/config.py` 定义，MCP 包与 toolkit 共享引用，禁止重复硬编码 | 代码评审 + AGENTS.md §3.x |
| brain_api 稳定门面 | `BrainApiClient` 只继承 5 个 mixin，方法体 verbatim 迁移不重写；新端点=新增 mixin 方法 | 备份在 `attic/brain_api_backup/` |
| 提交判定唯一权威 | `submit_verdict`（模拟层 checks + GET /submit 双视图）；`brain-alpha-judge`/`workflow_judge` 只是参考层 | SOP 步 8 + 代码无提交路径 |
| 处女提交 404 盲区 | UNSUBMITTED 的 alpha GET /submit 返回 404 → UNVERIFIABLE，须补 prod/self 终验（`batch_submit_verdict.py --phase2-prod`）才能放行 | `tests/unit/test_batch_submit_verdict_phase2.py` |
| dry-run 契约 | 全部 workflow 节点统一「零成本前置 → 构建命令计划 → 不 subprocess 不写库」；失败必须带 error | `tests/unit/test_skill_integrity.py` |
| 四处同步 | 新增/修改 workflow 节点须同步 registry / test_workflow / _DRY_RUN_CASES / INDEX.md | `python tools/audit_node_registration.py` |
| argv 契约 | 拼子进程命令的节点必须过 `validate_argv` 静态解析目标脚本 argparse，杜绝不存在的 flag | 仓脚本内建 |
| skill 单向同步 | 仓库 `Claude/skills/` 是源，安装位是派生物；改完跑 `python tools/sync_skills.py` | `--check` 模式 + 单测守护 |

### 核心数据流（一轮挖掘战役）

```
选区（campaign_intel s0-select：平台点塔 × 历史产出率 × 判死清单三方交叉）
  → 字段体检（field_inspect 包：低覆盖/厚尾/稀疏硬门，缺包可 enforce fail-closed）
  → 生成（GEM 概念优先 + priors 注入；预闸：幽灵算子/毒模式/同骨架封顶）
  → 门禁（wave_gate：语法 + gate.py 多样性 + 体检硬门 + 区域非法 group）
  → 回测（pipeline.py 七槽并发 + 账户级槽位仲裁 + 错误连坐自动隔离重发）
  → 收割（harvest_multisim → backtest_results；s4-prescreen 8 倍评审压缩）
  → 判定（prod-first 族级探针 → submit_verdict → 用户确认 → 提交）
  → 回写（win/dead_end 沉降 salvage_pool → region_kb 自动刷新 → 下一波先验）
```

---

## 3. 快速开始

### 环境

```bash
# 根环境（运行测试、通用工具）
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt

# MCP 环境（所有网络/回测操作，必须用它）
world-quant-brain-mcp/.venv/Scripts/python.exe -m pip install -r world-quant-brain-mcp/requirements.txt
```

> ⚠️ **网络类工具一律用 MCP 虚拟环境运行**（`world-quant-brain-mcp/.venv`）。工具已内置自动切换，切勿手写 `requests` 脚本——这是历史上 429 限流事故的根因之一，统一走 `BrainApiClient`（自带 429 退避）。

### 凭据

BRAIN 凭据位于 `world-quant-brain-mcp/.env`。**禁止读取、打印或提交到 git。**

### 验证安装

```bash
python -m pytest tests/ -x          # 根套件，~1356 个用例应全绿（含 tests/unit/ 递归）
world-quant-brain-mcp/.venv/Scripts/python.exe -m pytest world-quant-brain-mcp/tests   # MCP 包 84 个
```

建议激活 pre-commit 钩子（提交前自动跑测试，失败即阻断提交）：

```bash
git config core.hooksPath tools/git-hooks
```

### 启动 MCP 服务

已在 `.mcp.json` 注册两个 stdio 服务，由客户端按需拉起，无需手动启动：

| 服务 | 入口 | 用途 |
|---|---|---|
| `wq-brain-http` | `world-quant-brain-mcp/main.py` | BRAIN 平台交互（回测、提交、相关性、论坛） |
| `wqb-db` | `wqb_db_mcp.py` | 战役数据库读写 |

> 修改 `world-quant-brain-mcp/` 后**需重启 MCP 服务**才生效。

**跨平台写法（2026-09-29）**：`.mcp.json` 用 Claude Code 支持的 `${VAR:-default}`（command / args / env 均可展开）。
**没设任何环境变量时，展开结果与旧版逐字相同**（作者 Windows 本机行为不变）；其他环境覆盖下面三个变量即可：

| 变量 | 含义 | Windows 缺省 | Linux / 云端示例 |
|---|---|---|---|
| `WQB_HOME` | 仓库根 | `D:/coding/traeCN_project/wqb` | `/home/user/wqb` |
| `WQB_MCP_PY` | `wq-brain-http` 用的解释器 | `<根>/world-quant-brain-mcp/.venv/Scripts/python.exe` | `/home/user/wqb/world-quant-brain-mcp/.venv/bin/python` |
| `WQB_DB_MCP_PY` | `wqb-db` 用的解释器 | `<根>/.venv/Scripts/python.exe` | 同上（云端一个 venv 即可） |

`mcp_config.json`（供 Claude Desktop，不展开变量）保持字面路径，与 `.mcp.json` 缺省展开值的一致性由
`tests/unit/test_mcp_config_portable.py` 守护。体检：`python tools/mcp_ping.py`（同样按上表展开）。

#### 云端会话（Claude Code on the web）连接 MCP

云端容器里 `.mcp.json` 的 Windows 缺省值不存在（ENOENT，两个服务都起不来）。在**环境设置**
（会话标题栏的云环境菜单 → Edit）里：

1. **环境变量**：`WQB_HOME` / `WQB_MCP_PY` / `WQB_DB_MCP_PY`（值见上表 Linux 列）。
2. **安装脚本**（setup script）：`python3 -m venv /home/user/wqb/world-quant-brain-mcp/.venv && /home/user/wqb/world-quant-brain-mcp/.venv/bin/pip install -r /home/user/wqb/world-quant-brain-mcp/requirements.txt`。
3. 只想用**离线工具**（`operator_audit`、本地闸门、`wqb-db` 全部工具）时，到这里就够了。
4. 要调用**平台**（`authenticate` / `get_operators` / 提交判定等），还需：**Network access** 放开
   `api.worldquantbrain.com`、`platform.worldquantbrain.com`、`support.worldquantbrain.com`
   （默认策略会让 CONNECT 返回 403），并把凭据以环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`
   配进环境——**不要**把口令贴进对话，也不要写进仓库（AGENTS.md：凭据只在 `world-quant-brain-mcp/.env`，
   禁止读取、打印或提交）。新会话生效。
5. 验证：`python tools/mcp_ping.py`，应显示两个服务 `OK`（69 / 44 个工具）。

---

## 4. 目录结构

| 路径 | 职责 |
|---|---|
| `src/wqb/` | **规范核心包（single source of truth）**：`config` / `expression` / `research` / `search` / `memory` / `store` / `workflow` / `modeb`。区域、算子、中性化等域常量**只在此定义** |
| `world-quant-brain-mcp/` | MCP 服务。`brain_api.py` 为门面，方法体拆至 `brain_mixin_*.py`；业务工具按域在 `tools_*.py` |
| `Claude/skills/` | 32 个技能（SKILL.md + 脚本）。仓库为源，安装位由 `tools/sync_skills.py` 单向同步 |
| `tracking/` | 区域战役追踪（candidates / results / reviews / config）。**`tracking/mining/` 为共享数据湖（320+ 字段体检包），勿改动或移动** |
| `tools/` | 工具链，139 个 CLI。索引见 [`tools/README.md`](tools/README.md) |
| `mining/` | 挖掘脚本与归档 |
| `data/` | `wqb.db`（~223 MB，战役产物单一事实源）+ 只读参考数据 |
| `cache/` | 篮子/候选池等可再生产物（篮子 JSON、终验结果） |
| `extensions/` | 平台扩展（webdatascope 字段导出配套） |
| `docs/` | 计划 / 参考 / 经验 / 教程文档 |
| `reports/` · `output_report/` | 报告与 ideas 产物 |
| `attic/` | 隔离归档，**只读**，勿回迁进活跃代码 |
| `logs/` | 日志与临时脚本（`_*.py` 前缀即临时）；`test-results.xml` JUnit 可追溯 |

---

## 5. 核心工作流

唯一挖掘编排 SOP 是 **`wq-brain-ra-pipeline`** 的九步流水线（S-PRE → S6），三角形分工：

| Skill | 回答的问题 |
|---|---|
| `wq-brain-ra-pipeline` | **when / what** —— 怎么挖 Regular Alpha（S-PRE→S6） |
| `wq-brain-campaign-matrix` | **where** —— 查表选区域、选数据集 |
| `wq-brain-campaign-toolkit` | **how** —— 战役目录内的执行引擎 |

各步的 MCP 调用、产物与失败分支详见 **[AGENTS.md §3.5](AGENTS.md)**（唯一权威正文在 `Claude/skills/wq-brain-ra-pipeline/SKILL.md`）。关键约束在此重申三条：

1. **任一步 FAIL 就地回退，不允许跳过继续。**
2. **Artifact 契约**：战役产物只入 `data/wqb.db`，禁止 Agent 直接 Write 战役 JSON/CSV。
3. **提交判定链**：Failed-count 资格门 → `submit_verdict`（零成本，唯一权威）→ 可选 `brain-alpha-judge` → **用户确认** → `workflow_submit_alpha`。**submit_verdict READY 后不得自动提交。**

### 库存收割（先清库存，再开新挖）

账户已有三万条以上已回测 IS alpha，其中约 11% 通过 IS 硬闸——开新战役前先收割存量（2026-09-07 实证：新挖 170 次回测产出 0 条 vs 一次库存扫描 20 条）：

```bash
python tools/build_gate_prior_from_inventory.py --regions GLB,ASI --emit-candidates cache/candidates.json
python tools/select_ra_basket.py cache/candidates.json --target 20 --out cache/basket.json   # 去参数网格 + OS 撞车预筛 + 篮内正交
# 篮内逐条 submit_verdict；处女提交补 prod/self 终验：tools/batch_submit_verdict.py --phase2-prod
```

---

## 6. 一次性脚本工具化纪律

高频同构操作**禁止新建一次性脚本**。先查 [`tools/README.md`](tools/README.md) 是否有对应工具；缺参数就给工具加参数（保持 `--help` 自文档），而不是另起炉灶。常用映射：

| 场景 | 工具 |
|---|---|
| 每波门禁（语法 + 多样性 + 体检硬门） | `tools/wave_gate.py` |
| 幽灵算子硬闸（防整批 CANCELLED 连坐） | `tools/campaign_intel.py ghost-audit` |
| S3 收批后族级 prod 探针 | `tools/campaign_intel.py prod-first` |
| S4 评审前预筛压缩（~8 倍） | `tools/campaign_intel.py s4-prescreen` |
| 步级漏斗（哪一跳掉得最狠） | `tools/step_funnel.py --region R` |
| 提交层判定（403/404 盲区） | `tools/submit_verdict.py --alpha-id …` |
| 批量判定 + Phase2 相关性终验 | `tools/batch_submit_verdict.py [--phase2-prod]` |
| 批次状态查询与轮询 | `tools/batch_status.py --ids … [--watch]` |
| SuperAlpha 组件池探针 | `tools/sa_probe.py --region …` |
| 批量提交 | `tools/submit_batch.py` |

探索性探针可写在 `tracking/_scratch/`（已 gitignore），**结论落地后归档到 `attic/`**，不在活跃目录累积。

---

## 7. 三条最容易踩的约定

| 约定 | 说明 |
|---|---|
| **Shell 引号** | Windows 环境，引号经“工具传参 → PowerShell → 解释器”三层嵌套必出事故。**结构化数据读写优先走 `wqb-db` MCP 工具**（传 JSON，不经 shell）；需执行逻辑则写临时脚本 `logs/_tmp_*.py` |
| **测试计数口径** | 根 `tests/` **递归包含** `tests/unit/`（当前约 1356 个 + MCP 包 84 个独立跑），数字随新增用例增长，**以 `pytest --collect-only -q \| tail -1` 为准**，勿引用静态数字做断言 |
| **提交前检查** | 提交前必查按目录聚合的删除量，警惕一次性清空整个目录的误操作：<br>`git status --porcelain \| grep "^ D" \| awk '{print $2}' \| cut -d/ -f1-2 \| sort \| uniq -c \| sort -rn` |

---

## 8. 当前状态（2026-09-24）

| 维度 | 现状 |
|---|---|
| 测试 | 根套件 **1356 passed**（`tests/` 递归含 `tests/unit/`）；MCP 包 **84 passed**（需 `.venv` 单独运行） |
| MCP 工具 | `wq-brain-http` 69 · `wqb-db` 44 · workflow 节点 19（计数基准：`Claude/skills/INDEX.md`「MCP 工具/节点计数」，单测机械守护；README 此前写 45 是漂移） |
| Skills | 32 个（L-RA/L-PRE/L-TOOL/L0–L7 分层），4 个安装位与仓库零漂移 |
| 工具链 | 139 个 CLI（`tools/`） |
| 数据库 | `data/wqb.db` ~223 MB |
| 基础设施健康度 | 19 节点 dry-run 18/19 通过（`hypothesis_round` 属设计内 fail-closed）；audit_node_registration 四处同步零漂移 |
| 近期里程碑 | 2026-09-23 P0-1 库存收割：GLB/ASI 328 候选 → 19 颗正交篮 → 18 撞 prod 墙 / **O0NoPARJ 提交 ACTIVE**（prod 0.6193）；同日修复 `batch_submit_verdict.py` Phase2 三处假阴性并补 7 条单测 |
| 已知短板 | S2→S3 断链（数百个活跃波无门禁记录、积压超 7 天）；`risk_neutralized_sharpe` 在多数主力区未采集——诊断与优化方案见 [`docs/plans/2026-09-23-dryrun-audit-optimization-plan.md`](docs/plans/2026-09-23-dryrun-audit-optimization-plan.md) |

---

## 9. 文档索引

| 文档 | 内容 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **Agent 操作规约**：流水线细节、反模式、变更影响面、Shell 规约 |
| [`Claude/skills/INDEX.md`](Claude/skills/INDEX.md) | 技能路由（用户意图 → skill）· 分层与阶段 · 由代码生成的区域 / 闸门 / 计数表 |
| [`Claude/skills/CONTRACT.md`](Claude/skills/CONTRACT.md) | skill 写作契约：frontmatter · 职责边界 · 命名 · 共享产物归属 · 质量门禁 |
| [`docs/env_and_switches.md`](docs/env_and_switches.md) | 环境变量目录（代码扫描生成）· 凭据来源登记 · 外发通道 · CLI 开关 |
| [`docs/README.md`](docs/README.md) | 文档中心索引 |
| [`docs/experience/`](docs/experience/) | 平台交互经验（并发、配额、429 规避） |
| [`docs/plans/`](docs/plans/) | 改造计划（含 2026-09-23 dry-run 全链审计与优化方案） |
| [`docs/reference/`](docs/reference/) | 参考材料，含历史状态报告 |
| [`tools/README.md`](tools/README.md) | 工具链索引 |
| [`tracking/README.md`](tracking/README.md) | 战役追踪目录说明 |
| `tracking/MANIFEST.json` | 追踪目录全量索引。**当前未生成**；可用 `tracking/reference/tooling/generate_manifest.py` 重建，注意该脚本会顺带把 >500 KB 文件 zip 归档到 `tracking/archive/large/` |
