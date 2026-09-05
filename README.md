# wqb — WorldQuant BRAIN Alpha 挖掘工作区

面向 WorldQuant BRAIN 平台的量化研究工作台：以 Python 脚本驱动 alpha 的挖掘、回测、评审与提交，以 MCP 服务作为与编码 Agent 的主要接口，以 SQLite 作为战役产物的单一事实源。

> **文档分工**
> - **本文件（README.md）** —— 面向人：项目是什么、如何上手、去哪找东西。
> - **[AGENTS.md](AGENTS.md)** —— 面向 AI Agent：硬约束、九步流水线细节、反模式与变更影响面。**动手前必读。**

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

- **一套流水线，多区域复用**：KOR / USA / EUR / IND / GBR / HKG / DEU / GLB / ASI / MEA 等区域共用同一套九步骨架，区域差异通过 profile 注入。
- **产物只进数据库**：expressions / gate_results / backtest_results / wave_results / ledger 全部落在 `data/wqb.db`，不散落 JSON/CSV。
- **技能即执行器**：流水线各步由 skills 承载，禁止手写一次性脚本替代（见 §5）。

---

## 2. 快速开始

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
python -m pytest tests/ -x          # 根套件，313 个用例应全绿
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

---

## 3. 目录结构

| 路径 | 职责 |
|---|---|
| `src/wqb/` | **规范核心包（single source of truth）**：`config` / `expression` / `research` / `search` / `memory` / `store` / `workflow`。区域、算子、中性化等域常量**只在此定义** |
| `world-quant-brain-mcp/` | MCP 服务。`brain_api.py` 为门面，方法体拆至 `brain_mixin_*.py`；业务工具在 `tools_*.py` |
| `tracking/` | 区域战役追踪（candidates / results / reviews / scripts）。**`tracking/mining/` 为共享数据湖，勿改动或移动** |
| `tools/` | 工具链，84 个 CLI。索引见 [`tools/README.md`](tools/README.md) |
| `mining/` | 挖掘脚本与归档 |
| `data/` | `wqb.db`（64 MB，战役产物单一事实源）+ 只读参考数据 |
| `docs/` | 计划 / 参考 / 经验 / 教程文档 |
| `reports/` · `output_report/` | 报告与 ideas 产物 |
| `attic/` | 隔离归档，**只读**，勿回迁进活跃代码 |
| `logs/` | 日志与临时脚本（`_*.py` 前缀即临时） |

---

## 4. 核心工作流

唯一挖掘编排 SOP 是 **`wq-brain-ra-pipeline`** 的九步流水线（S-PRE → S6），三角形分工：

| Skill | 回答的问题 |
|---|---|
| `wq-brain-ra-pipeline` | **when / what** —— 怎么挖 Regular Alpha（S-PRE→S6） |
| `wq-brain-campaign-matrix` | **where** —— 查表选区域、选数据集 |
| `wq-brain-campaign-toolkit` | **how** —— 战役目录内的执行引擎 |

各步的 MCP 调用、产物与失败分支详见 **[AGENTS.md §3.5](AGENTS.md)**。关键约束在此重申三条：

1. **任一步 FAIL 就地回退，不允许跳过继续。**
2. **Artifact 契约**：战役产物只入 `data/wqb.db`，禁止 Agent 直接 Write 战役 JSON/CSV。
3. **提交判定链**：Failed-count 资格门 → `submit_verdict`（零成本，唯一权威）→ 可选 `brain-alpha-judge` → **用户确认** → `workflow_submit_alpha`。**submit_verdict READY 后不得自动提交。**

---

## 5. 一次性脚本工具化纪律

高频同构操作**禁止新建一次性脚本**。先查 [`tools/README.md`](tools/README.md) 是否有对应工具；缺参数就给工具加参数（保持 `--help` 自文档），而不是另起炉灶。常用映射：

| 场景 | 工具 |
|---|---|
| 每波门禁（语法 + 5 闸 + 多样性） | `tools/wave_gate.py` |
| 批次状态查询与轮询 | `tools/batch_status.py --ids … [--watch]` |
| SuperAlpha 组件池探针 | `tools/sa_probe.py --region …` |
| 提交层判定（403 盲区） | `tools/submit_verdict.py --alpha-id …` |
| SUPER 组套与提交全流程 | `tools/super_build.py {select\|status\|probe\|submit}` |
| 批量提交 | `tools/submit_batch.py` |

探索性探针可写在 `tracking/_scratch/`（已 gitignore），**结论落地后归档到 `attic/`**，不在活跃目录累积。

---

## 6. 三条最容易踩的约定

| 约定 | 说明 |
|---|---|
| **Shell 引号** | Windows 环境，引号经"工具传参 → PowerShell → 解释器"三层嵌套必出事故。**结构化数据读写优先走 `wqb-db` MCP 工具**（传 JSON，不经 shell）；需执行逻辑则写临时脚本 `logs/_tmp_*.py` |
| **测试计数口径** | 根 `tests/` **递归包含** `tests/unit/`，`313 = 10 + 303`，**勿把两者相加**。以 `pytest --collect-only -q \| tail -1` 为准 |
| **提交前检查** | 提交前必查按目录聚合的删除量，警惕一次性清空整个目录的误操作：<br>`git status --porcelain \| grep "^ D" \| awk '{print $2}' \| cut -d/ -f1-2 \| sort \| uniq -c \| sort -rn` |

---

## 7. 当前状态

| 维度 | 现状（2026-09-04） |
|---|---|
| 分支 / 远端 | `main` → `git@github.com:mt-monster/wqb.git` |
| 测试 | 根套件 313 通过；MCP 包 79 通过（需 `.venv`，单独运行） |
| 数据库 | `data/wqb.db` 64 MB |
| 区域战役活跃度（文件数） | IND 1170 · EUR 1064 · USA 516 · KOR 474 · GBR 930 · ASI 286 · HKG 204 · MEA 145 · DEU 11 |

---

## 8. 文档索引

| 文档 | 内容 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **Agent 操作规约**：流水线细节、反模式、变更影响面、Shell 规约 |
| [`docs/README.md`](docs/README.md) | 文档中心索引 |
| [`docs/experience/`](docs/experience/) | 平台交互经验（并发、配额、429 规避） |
| [`docs/plans/`](docs/plans/) | 改造计划 |
| [`docs/reference/`](docs/reference/) | 参考材料，含历史状态报告（`CODE_QUALITY_SUMMARY.md`、`INTEGRATION_COMPLETE.md`） |
| [`tools/README.md`](tools/README.md) | 工具链索引 |
| [`tracking/README.md`](tracking/README.md) | 战役追踪目录说明 |
| `tracking/MANIFEST.json` | 追踪目录全量索引。**当前未生成**（历史上曾存在，现已丢失）；可用 `tracking/reference/tooling/generate_manifest.py` 重建，注意该脚本会顺带把 >500 KB 文件 zip 归档到 `tracking/archive/large/` |
