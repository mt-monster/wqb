# wqb 项目代码与内容审计 — 优化方案

> 日期：2026-08-18 | 范围：`D:\coding\traeCN_project\wqb` 全仓 | 审计方式：只读静态扫描（未修改任何文件）

---

## 0. 执行摘要

项目总量：**445 个 Python 文件 / 49,454 行**（不含 `.venv` / `research-data`），另有 3,038 个 JSON（34.8 MB，其中 tracking 占 2,989 个 / 34.1 MB）、Markdown 文档约 5,000 行。测试现状：`tests/` 下 232 个用例全绿（`world-quant-brain-mcp/.venv` 环境，1.6s），但**覆盖面高度集中在 `src/wqb`**（12 个核心模块），MCP 服务端、tools/、mining/、pipeline/ 基本无测试。

核心结论一句话：**项目的"引擎"（src/wqb + MCP 服务端）质量尚可，但围绕引擎长出了三层失控的"一次性脚本壳"——`tools/`（113 文件）、`tracking/*/scripts/`（295 文件）、`mining/archive/`（22 个版本爆炸）——它们携带 122 处硬编码用户路径、119 个 100% 重复文件（KOR↔IND），是本次优化真正的靶心。**

### Top 7 优化项（按影响 × 成本排序）

| # | 问题 | 影响 | 成本 | 阶段 |
|---|------|------|------|------|
| 1 | `logs/`、`world-quant-brain-mcp/logs/` 未被 .gitignore 排除，运行时日志混进 `git status`（27 个未跟踪/未提交项） | 中 | 极低 | P1 |
| 2 | 根 `requirements.txt` 缺 `mcp/pydantic/redis/pytest` 等关键依赖，裸环境跑测试直接收集失败 | 高（新环境不可复现） | 极低 | P1 |
| 3 | 122 个活跃脚本硬编码 `C:/Users/MENGTAO/...` 路径（4 种不同 skill 根：`.workbuddy` / `.qoder-cn` / `.zcode`），换机器即全灭 | 高 | 低 | P1 |
| 4 | `tracking/KOR/scripts` 与 `tracking/IND/scripts` **119 个文件逐字节完全相同**（各 4,451 行） | 中（维护双份） | 低 | P1 |
| 5 | `brain_api.py` 4,113 行 / 186 KB 单体，40 函数 + 98 方法挤在一个类，且混入了 `FastMCP`/`redis`/`bs4` 依赖（与模块 docstring 自述"只依赖基础库"矛盾） | 高 | 中 | P2 |
| 6 | `tools/` 113 个文件（8,162 行）中 ~88 个 `_` 前缀一次性脚本 + 30+ 个 `_submit_*` 复制粘贴变体，无统一入口、无测试 | 高 | 中 | P2 |
| 7 | `mining/archive/mine_v6..v27` 22 个版本爆炸脚本（已被 `mine_core.py` 参数化模板取代）仍占位且全部硬编码路径 | 低 | 极低 | P1 |

---

## 1. 代码规模全景（实测）

| 目录 | 文件数 | 行数 | 定位 | 测试覆盖 |
|------|--------|------|------|----------|
| `world-quant-brain-mcp/` | 25 | 10,964 | MCP 服务端（brain_api + 10 个 tools_*.py） | ❌ 几乎无（自带 2 个未接入 pytest.ini 的单测文件） |
| `src/wqb/` | 17 | 2,740 | 核心引擎（配置/表达式/搜索/记忆） | ✅ 232 用例全绿 |
| `tools/` | 113 | 8,162 | 运维/提交/分析脚本（~88 个一次性） | ❌ 无 |
| `tracking/` | 196 | 18,744 | 区域战役脚本 + 34 MB JSON 台账 | ❌ 无 |
| `mining/` | 37 | 2,309 | 挖掘模板 + 22 个 archive 版本 | ❌ 无 |
| `pipeline/` | 7 | 906 | 通用战役 pipeline（质量较好） | ❌ 无 |
| `tests/` | 14 | 2,328 | 全部指向 src/wqb | — |
| `logs/` | 18 | 570 | 运行时残留脚本（不应入库） | — |

---

## 2. 按模块详细发现

### 2.1 MCP 服务端（`world-quant-brain-mcp/`）

**做得好的：**
- `main.py` 组装清晰：10 个 `tools_*.py` 按域拆分、import 副作用注册，已消除 main↔forum 循环耦合（2026-08-13 asyncio 重入 bug 的根源已修）。
- `mcp.run()` 严格收在 `__main__` guard 内，docstring 解释了历史教训。

**问题：**
1. **`brain_api.py` 单体过大（4,113 行 / 40 def / 4 class / 98 方法）**。docstring 声称"只依赖 requests/pandas/pydantic/python-dotenv，不含 FastMCP/redis/bs4"，但实际 import 了 `redis`、`bs4.BeautifulSoup`、`mcp.server.fastmcp.FastMCP` —— **自述与实现矛盾**，说明拆分（P2 单体拆分）只做了一半。
2. `brain_api.py` 模块级 `from forum_functions import forum_client`，而 forum_functions 又惰性引用 brain_api.brain_client —— 虽然靠惰性 import 避免了硬循环，但**依赖方向仍然双向**，是脆弱点。
3. 自带 `world-quant-brain-mcp/tests/test_brain_api_unit.py`（190 行）和 `test_mcp_tools_unit.py`（275 行），但根 `pytest.ini` 的 `testpaths = tests` **不包含它们** —— 这两个测试文件处于"存在但从不运行"的状态。
4. `brain_api.py` 与 `tools_account.py` 中存在少量裸 `except:` / `except Exception: pass`（共 4 处），会吞掉平台 429/403 等关键错误信号。
5. `create_super_alpha.py`、`super_alpha_tool.py`、`test_labs_live.py`、`配置前运行我_安装必要依赖包.py` 4 个顶层散文件未归档、未被引用（死代码候选）。

### 2.2 核心引擎（`src/wqb/`）

**项目里质量最高的部分**：单一真相源 `config.py`（区域搜索空间/算子家族/幽灵算子黑名单）、表达式 AST 校验、调度器、SQLite 记忆库，边界清晰、有测试。

**问题（轻微）：**
1. `src/wqb/expression/grammar.py` 是 4 个 expression 模块中**唯一零测试**的模块（operator_audit/validator/diversity_enhancer 均有覆盖）。
2. 测试通过 `tests/conftest.py` 的 `sys.path.insert(0, src)` 注入而非 `pip install -e .`——可用但不规范；且 conftest 中"包不存在时 skip 8 个测试文件"的兜底逻辑已过时（src/wqb 已重建完成），该 skip 列表现在永远不会触发，属于死代码。

### 2.3 `tools/` —— 本次审计最大的治理缺口

- 113 个文件、8,162 行，**没有任何一个被其他模块 import**（全部是一次性 CLI 脚本）。
- ~88 个 `_` 前缀文件是历史波浪（wave）的临时产物：`_submit_macro38_ap..aw`、`_submit_obim_aa..aj`、`_submit_mix_ak..as` 等 30+ 个提交脚本结构完全同构（改两行候选路径就另存一份）。
- 45 个 `_` 文件重复 `from brain_api import BrainApiClient` 样板；只有 24 个文件有 `__main__` guard。
- `tools/fetch_all_universes.py` 硬编码了一个**指向项目外**的 `.env` 路径（`C:\Users\MENGTAO\Desktop\E3\quant\worldquant_alpha\.env`）——最危险的一处硬编码。
- `tools/gate.py` 同时硬编码了 `.workbuddy` 和 `.qoder-cn` 两套 skill 根，且与 `mining/` 用的 `WQ_ACE_LIB` 环境变量约定不一致。

### 2.4 `tracking/` —— 数据台账有价值，脚本是复制粘贴重灾区

1. **KOR ↔ IND 119 个脚本逐字节相同**（各 4,451 行，MD5 全等）。IND 区域实际上是 KOR 的整目录克隆，连 `kor_scan_fields*.py` 这类文件名都原样保留在 IND 下。任何 bug 修复都需要改两遍（实际只会改一边，然后漂移）。
2. EUR 38 个 `run_wave*.py`（9,100 行）、GBR 19 个（3,813 行）全是 wave 级一次性 runner，各自硬编码 TOOLKIT 路径（`.qoder-cn`）。
3. `tracking/.gitignore` 已正确排除 `cache/results/*.bak`，边界意识是好的；问题只在 scripts。
4. JSON 台账 34 MB（2,989 个文件）在 git 追踪内 —— 量级尚可接受，但应设定增长上限与归档策略。

### 2.5 `mining/`

- `mine_core.py` 是正确的方向（参数化模板 + checkpoint/resume，且已带头用 `WQ_ACE_LIB` 环境变量），但**它自己仍保留硬编码回退路径**，且模板从未被真正实例化使用（`build_candidates()` 是空示例）。
- `mining/archive/mine_v6..v27` 22 个脚本（版本爆炸的历史证据）全部硬编码 `.workbuddy` skill 路径，应整体压缩归档或删除。
- `mining/scripts/diagnostics/` 8 个诊断脚本全部重复同一行 `sys.path.insert(...WQ_ACE_LIB 回退...)`。

### 2.6 依赖与测试环境

- 根 `requirements.txt`（5 个包）⊂ MCP `requirements.txt`（10 个包），且根文件缺 `mcp`、`pydantic`、`redis`、`email-validator`。**在根裸环境跑 `pytest` 会因 `ModuleNotFoundError: requests` 收集失败**——必须知道"要用 `world-quant-brain-mcp/.venv`"这个隐性知识才能跑通测试，这是新环境/CI 复现的第一道坑。
- 无 `pyproject.toml`、无 lock 文件、无 CI 配置。

---

## 3. 分阶段实施路线图

### Phase 1 — 紧急 / 低成本（半天内，零风险）

> 原则：只动配置与归档，不动任何运行逻辑；每步后 `pytest tests/ -q`（在 MCP venv 中）必须保持 232 全绿。

1. **修 `.gitignore`**：追加 `logs/` 与 `world-quant-brain-mcp/logs/` 两条目录规则（现有 `*.log` 只挡文件不挡目录里的 `.py`）。清掉 27 个未跟踪项中的日志噪音。
2. **统一依赖**：根 `requirements.txt` 改为 `-r world-quant-brain-mcp/requirements.txt` + `pytest`，消灭两套声明不一致。
3. **归档版本爆炸**：`mining/archive/mine_v*.py` 22 个 → 打包为 `mining/archive/mine_v6_v27.tar.gz` 或直接删除（`mine_core.py` 已取代）；`logs/*.py` 一次性脚本移出仓库（它们是运行时残留）。
4. **去重 KOR/IND**：119 个相同文件提取为 `tracking/shared/scripts/`（KOR/IND 各留薄 wrapper 传入 region 参数），或直接删除 IND 副本并注明来源。先 diff 确认、再分批（≤10 文件/批）移动到回收站式归档目录。
5. **conftest.py 清理**：删除已过时的 `collect_ignore` skip 列表（src/wqb 已存在，skip 永不触发）。

### Phase 2 — 结构改进（1–3 天，需要小步验证）

6. **硬编码路径歼灭战**（122 处，39 个核心文件先行）：
   - 确立唯一约定：环境变量 `WQ_SKILLS_ROOT`（默认 `~/.workbuddy/skills`）+ `WQ_ACE_LIB`；在 `src/wqb/config.py` 新增 `skills_root()` / `ace_lib_path()` helper。
   - 按目录分批替换：`mining/scripts/`（16 处）→ `tools/`（非 `_` 前缀）→ `tracking/EUR|GBR` runner 模板。**不动 `tracking/KOR|IND`**（待 Phase 1 去重后只剩一份再改）。
   - `tools/fetch_all_universes.py` 的项目外 `.env` 路径改为参数/环境变量，并加存在性校验。
   - 已有 `tracking/reference/tooling/dehardcore_all.py` / `patch_paths.py` 两个历史工具脚本，先审计能否复用，再写新脚本。
7. **tools/ 大清扫**：
   - 88 个 `_` 前缀一次性脚本按 wave 归档进 `tools/archive/waveXX/` 子目录（或整体移出仓库到冷存储）。
   - 30+ 个 `_submit_*` 同构脚本提炼为一个参数化 `tools/submit_batch.py`（输入：候选 JSON + 设置 JSON），这是 `mine_core.py` 思路在提交侧的复刻。
   - 为保留下来的公共脚本补 `__main__` guard 和 `--help`。
8. **MCP 测试接入**：把 `world-quant-brain-mcp/tests/` 两个既有单测文件纳入根 pytest（`testpaths = tests world-quant-brain-mcp/tests`），让它们从"从不运行"变为每次必跑；修复可能暴露的失败。
9. **补 `src/wqb/expression/grammar.py` 测试**（唯一零覆盖的核心模块）。

### Phase 3 — 长期工程（按需推进，每次独立 PR）

10. **`brain_api.py` 二次拆分**（4,113 行 → 按职责拆 4–5 个模块）：
    - `brain_api/models.py`（Pydantic 模型：AuthCredentials/SimulationSettings/SimulationData）
    - `brain_api/http.py`（请求、信号量、重试、429 退避）
    - `brain_api/cache.py`（Redis 缓存层；同时落实 docstring 承诺的依赖倒置——cache 可选注入）
    - `brain_api/client.py`（BrainApiClient  facade，组合上述模块）
    - 解除 `brain_api ↔ forum_functions` 双向依赖：forum_client 改为参数注入。
    - 验收：MCP 服务重启冒烟 + 两个接入的单测文件全绿 + 232 用例不回归。
11. **消灭裸 except**（4 处）：改为捕获具体异常并记日志，429/403 不得被静默吞掉。
12. **tracking JSON 增长治理**：为 34 MB 台账设定季度归档策略（旧 wave 的 `results/` 已排除，剩余 JSON 按 wave 打包压缩，保留 MANIFEST 索引）。
13. **规范化打包**：`pyproject.toml` + `pip install -e .` 取代 conftest 的 `sys.path` hack；评估引入轻量 CI（本地 pre-commit: pytest + 硬编码路径 linter）。

---

## 4. 风险与验证协议

| 风险 | 缓解 |
|------|------|
| 移动/删除一次性脚本后某个历史 wave 需要复现 | 全部先移入 `archive/` 目录或压缩包，git 历史可查；禁止硬删除，遵守"回收站优先"纪律 |
| 硬编码路径替换引入 import 失败 | 每批替换后跑 `python -c "import ast; ast.parse(open(f).read())"` 语法检查 + 目标脚本 `--help` 冒烟 |
| MCP 拆分破坏运行中的服务 | 拆分前先在 `world-quant-brain-mcp/tests/` 补 client 级契约测试；拆分后重启服务并跑一轮真实仿真冒烟（probe 3 个表达式） |
| KOR/IND 去重后发现两边已隐性漂移 | 已实测 119/119 MD5 全等，无漂移；去重窗口安全 |
| 测试回归 | 每个 Phase 的每个步骤后：`world-quant-brain-mcp/.venv/Scripts/python.exe -m pytest tests/ -q` 必须 232 passed |

**验收基线（执行前记录）：**
- pytest：232 passed（MCP venv）
- `git status --short`：27 项 → Phase 1 后应 ≤ 20 项（纯业务变更）
- 硬编码路径计数：活跃代码 104 处 → Phase 2 后应为 0（archive 内不计较）

---

## 5. 不做的事（明确划界）

- **不**改 `src/wqb/` 任何运行逻辑（它是全项目最健康的部分，232 测试锚定）。
- **不**删 `tracking/` 任何 JSON 台账（34 MB 尚在可接受范围，且有 MANIFEST 索引）。
- **不**在 Phase 1/2 触碰 MCP 服务端逻辑（拆分属 Phase 3，需独立冒烟窗口）。
- **不**批量 `rm` 任何文件——所有清理走"归档目录/压缩包 + 分批 ≤10 + 确认"流程。
