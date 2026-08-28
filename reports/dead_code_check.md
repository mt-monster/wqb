# 无用文件 / 代码排查报告（2026-08-23）

排查范围：活动代码目录 `src/ world-quant-brain-mcp/ tools/ pipeline/ mining/ polling/` 及根 `.py`（排除 `attic/ tracking/ logs/ research-data/ extensions/ .venv/`）。
方法：AST 静态解析（122 个文件）+ 跨模块引用图 + 交叉验证。

## 一句话结论
**代码库在「未使用 import / 死函数」维度整体干净**，没有可大规模清理的冗余。
真正需要处理的点只有 **1 个语法损坏文件**（`gen_v5.py`，已归档）。此前初判的「2 个被废弃模块」经复核实为活动代码（见第二节），**无需处理**。其余为「合法但零散」的独立脚本。

---

## 一、确认损坏（建议修复或删除）

| 文件 | 问题 | 引用情况 | 建议 |
|---|---|---|---|
| `mining/scripts/gen_v5.py` | **语法错误**：第 36 行 `os.path.join(... "alpha_list_usa_d1_sentiment_v5.json"` 缺右括号 | 无代码 import，仅被一条 memory 笔记提及 | **已处置**：2026-08-23 `git mv` 至 `attic/mining_archive/gen_v5.py`（保留可恢复，活动树不再含损坏文件） |

> 其余 121 个文件均能正常 `ast.parse`，**全库仅此一处语法损坏**。

## 二、复核更正：pipeline 两个模块 **并非死代码**（不归档）

> ⚠️ **更正（2026-08-23）**：初版将此二模块判为「被废弃的设计备选、建议归档」，经复核 **属误判**。
> 实际引用链：`tracking/_scratch/run_gbr_batch8.py`（**已 `git` 追踪的活动脚本**，GBR 第 8 批回测启动器，注释写明"实际提交版"）执行 `from pipeline.core.mcp_integrated_pipeline import create_pipeline`；而 `mcp_integrated_pipeline.py` 又引用 `mcp_direct.py`。
> 因此二者经此构成**活动引用链**，属活跃基础设施，**不可归档**（归档会破坏 `run_gbr_batch8.py` 的导入）。

| 文件 | 说明 | 状态 |
|---|---|---|
| `pipeline/core/mcp_direct.py` | `DirectMCPClient` / `get_direct_client` MCP 直连方案 | 被 `mcp_integrated_pipeline.py` 引用 → **活跃** |
| `pipeline/core/mcp_integrated_pipeline.py` | `MCPIntegratedPipeline` 备选管线 | 被 `tracking/_scratch/run_gbr_batch8.py` 直接 import → **活跃** |

> 对照：活跃的还有 `campaign_pipeline.py`、`campaign_discipline.py`、`diversity_integrated_monitor.py`（经 `pipeline/core/__init__.py` 再导出）。
> **教训**：今后判「死代码」须把 `tracking/_scratch/` 纳入引用图（用 `git ls-files` 确认其被追踪），不能仅凭 `docs/` 引用即判废弃。

## 三、误报澄清（避免误删）

以下维度经严格验证**无误删必要**，列出以防误判：

1. **未使用 import**：初扫 36 条、再验 10 条，全部为 `from __future__` 指令、`# noqa: F401` 显式再导出、或多行 import 续行被正则误抓 —— **0 条真实冗余**。
2. **死函数**：初扫 321 条，几乎全为类方法（经 `self.x()` / `@mcp.tool()` 注册表 / 字典映射调用，不以 `Name` 节点出现）与 pytest 测试目标、CLI 入口 —— **均为误报，非死代码**。
3. **`src/wqb/research/*`**：被 `tests/unit/test_research.py` 引用（扫描未纳入 `tests/` 导致初判为孤立）—— **活跃，非死代码**。

## 四、合法但零散的独立脚本（非无用，仅提示整理）

`mining/scripts/diagnostics/*.py`（7 个）、`mining/scripts/harvest_*.py`、`enum_mdl177.py`，以及 `tools/build_progress_ledger.py`、`tools/fetch_all_universes.py` 等：
- 它们**无 `if __name__` 守卫、不被其他模块 import**，但本就以 `python xxx.py` 直接运行 —— 属正常 standalone 工具/一次性脚本。
- 不是「无用代码」，但若想进一步收敛目录，可仿照已落地的 `tools/` 工具化纪律，把高频复用的 harvest/diagnostics 脚本收编为 `tools/` 下带 CLI 的工具。

## 五、本次未纳入的上下文
- `tracking/`（数据湖）、`attic/`（已归档）、`logs/`、`research-data/`、`extensions/` 按计划排除。
- `~/.workbuddy/skills/` 下的「重复 basename 文件」属技能仓库（仓库之外、无 git），不在本次提交/清理范围。
- `git status` 中 `reports/*` 大量 `D` 与 `tools/skills_audit_linkcheck.py` 等删除为你 08-23 整合的未提交改动，非本次发现。

---
**结论性建议**：需要优化的点极少。唯一确认无用且已处置的是 `gen_v5.py`（已归档至 `attic/mining_archive/`）。此前初判的 `mcp_direct.py` / `mcp_integrated_pipeline.py` 经复核为活动代码，**不归档**。其余（未使用 import / 死函数 / research 模块）均无清理必要。
