# wqb 项目结构审计与治理建议

> 审计日期：2026-10-16　审计范围：全仓库静态结构 + 全量测试（3422 用例）
> 结论摘要：架构分层清晰、核心业务功能健康；**存在 1 个 P0 已破坏项 + 若干架构债**，按优先级处置。

---

## 一、结构梳理

### 1.1 四层架构

| 层 | 位置 | 规模 | 职责 |
|---|---|---|---|
| 调用入口 | `Claude/skills/` 47 个 | 328 篇 md | 九步流水线入口，人读 SOP |
| MCP 服务 | `world-quant-brain-mcp/` | 39 文件 / 39394 行 | HTTP 常驻服务（8000/8001），`brain_api` 门面 |
| 规范核心 | `src/wqb/` | 120 文件 / 35663 行 | **唯一可安装包**，域常量单一事实来源 |
| 工具脚本 | `tools/` | 210 文件 / 58700 行 | CLI 脚本集合，不打包 |
| 测试守护 | `tests/` | 212 文件 / 33410 行 | 3422 用例，`07_docs_skills` 为防漂移硬闸 |

真实源码合计 **581 个 py 文件 / 约 16.7 万行**；文档 700+ 篇 md。

### 1.2 体积分布

| 目录 | 体积 | 版本控制 |
|---|---|---|
| `.venv` | 743 MB | gitignored |
| `data/wqb.db` | 421 MB | gitignored |
| `cache/`（probe.db 283M） | 309 MB | gitignored |
| `tracking/` | 102 MB | **2637 文件已追踪** |
| `research-data/` | 40 MB | gitignored |

⚠ git 追踪 4191 个文件，其中 **tracking 占 2637（63%）**——版本库主体是战役数据而非源码。

### 1.3 测试健康度

```
3422 passed-ish: 3405 通过 / 17 失败 / 26 跳过
```

**17 个失败全部位于治理守护类测试**，业务逻辑测试全绿：

- `07_docs_skills/*` 10 个（skill 文档守护）
- `09_core/*` 4 个（核心约束、时间炸弹）
- `01_store_db` 1 个（DB 写入守卫）
- 其余 2 个（skill 边界 / lint）

---

## 二、P0 — 已破坏，需立即修复

### `Claude/skills/wq-brain-ra-kor/SKILL.md` 脱离生成器管控

**三个症状，同一根因**：

1. **YAML frontmatter 被 Markdown 转义污染** —— 导致 4 个守护测试红
   ```
   现状（错误）              应为
   \---                     ---
   \- Read                  - Read
   mcp\_\_wq-brain-http\__*  mcp__wq-brain-http__*
   ```
   对照 `wq-brain-ra-gbr/SKILL.md` 为干净格式。

2. **含未来日期 `2026-11-16` 未登记** —— 触发 `test_time_bombs` 红

3. **丢失生成器 marker 块** —— `render.plan(['KOR'])` 直接抛异常
   ```
   ValueError: 缺生成块标记 <!-- profiles:region-panel:start --> / ...:end -->
   ```

**为什么严重**：记忆铁律明确记载 `wq-brain-ra-<区小写>` 是 `src/wqb/profiles/render.py` 的**生成物，不是手写 skill**。该文件现已：
- 生成器跑不动 ⇒ 该区 skill 无法再被统一渲染/更新
- 5 个守护测试持续红 ⇒ 掩盖真实回归

**修复路径（二选一）**：
- **A（推荐）**：该文件正文含 KOR 专属的「六步纵深」骨架（`layer: L4`，与其余 13 区的 `L-RA-R` 不同），若属有意定制 ⇒ 把骨架固化进生成器的 `_FIELDCHECK_REGIONS` 分支，再由生成器重新渲染，恢复 marker 块。
- **B**：若确为一次性编辑事故 ⇒ 从 git 恢复该文件的 frontmatter 与 marker 块，再跑 `render --apply` 验证幂等（`plan()` 的 `old != new` 必须为 `False`）。

⚠ 禁止仅在文件层面补 frontmatter —— 生成器下次 `--apply` 会再次覆盖或崩溃。

---

## 三、P1 — 架构债

### 3.1 sys.path 注入 794 处

| 目录 | 注入处 |
|---|---|
| `tools/` | 462 |
| `tests/` | 289 |
| `world-quant-brain-mcp/` | 37 |
| `src/` | 6 |

`pyproject.toml` 已声明 `src/wqb` 为可安装包（`pip install -e .`），注释中也承认这是为了「不必靠 259 处 sys.path 注入」。但存量注入已达 794 处且未清理 —— 声明与现状脱节。

**建议**：新脚本一律不再注入；存量按目录分批清理（先 `src/` 6 处 → `world-quant-brain-mcp/` 37 处），`tools/` 与 `tests/` 因脚本直跑特性可后置，但需在 AGENTS.md 明确「只剩 CLI 直跑场景允许注入」。

### 3.2 五个巨型文件

| 文件 | 行数 |
|---|---|
| `tools/audit_structure.py` | 2136 |
| `world-quant-brain-mcp/labs_data_analysis_agent.py` | 2062 |
| `src/wqb/workflow/nodes/campaign.py` | 2021 |
| `tools/wave_gate.py` | 1718 |
| `src/wqb/workflow/nodes/gem.py` | 1627 |

`campaign.py` / `gem.py` 是 workflow 节点主实现，承载多个 stage；`audit_structure.py` 承担全仓库结构审计，天然庞大但应拆分为「检查项集合 + 执行器」。

**建议**：优先拆 `campaign.py`（按 stage 拆子模块），`audit_structure.py` 拆为规则表 + runner。设定 1500 行预警线并纳入守护测试。

### 3.3 tracking/ 入版本库比例过高

2637 个文件（63%）是战役 candidates/results/reviews，属**工作产物**。`tracking/.gitignore` 已排除 bulk data lake 与部分运行时账本，但 curated 结构仍全量入库。

**建议**：明确「入版本库的只应是可复现战役的配置与结论（config/、reviews/），中间态 candidates/results/ 应排除」，或改用独立归档策略。

---

## 四、P2 — 治理工具碎片化

### 4.1 六个 audit 脚本并存

```
tools/audit_dead_code.py
tools/audit_file_sizes.py
tools/audit_node_registration.py
tools/audit_skill_drift.py
tools/audit_structure.py
tools/step9_audit.py
```

治理工具自身缺乏统一入口。

**建议**：合并为 `tools/audit.py` 单一入口 + 子命令（`--dead-code` / `--file-sizes` / `--node-registration` / `--skill-drift` / `--structure`），各检查项作为插件注册。

### 4.2 快照裁决台账积压

`test_governance_gates_selfcheck` 报：**总数 852，PENDING 517（61%）** —— 抢救点独有源码超半数无人裁决。

**建议**：台账积压会持续触发守护失败。要么补裁决（517 件工作量大），要么把「PENDING 不算失败」的判据改宽，避免守护长期红灯失效。

### 4.3 双轨同源漂移风险

- 人读：`docs/experience/*.md` 9 篇
- 机器：`Claude/skills/wq-brain-campaign-toolkit/config/methodology_rules.json` 24 条规则

**建议**：已有 `test_experience_kb_refs.py` 守护，但仅校验引用存在性。建议增强为「规则条目 ↔ 文档章节」双向可追溯校验。

---

## 五、P3 — 环境与卫生

### 5.1 解释器分叉（今日实测踩坑）

用根 python 跑 pytest ⇒ 9 个 collection error（缺 pandas/pydantic/mcp/requests）；
用 `world-quant-brain-mcp/.venv` 跑 ⇒ 3422 用例正常收集。

铁律已写入 AGENTS.md，但**无强制机制**。

**建议**：在 `conftest.py` 顶部加解释器断言，非指定 venv 直接报错退出，把约定变成硬闸。

### 5.2 运行期残留

- 2309 个 `.pyc` / 285 个 `__pycache__`（已 gitignore，但占 817 KB）
- `--timeout` 插件未安装，导致 `pytest --timeout=600` 直接报错退出

**建议**：`--timeout` 写入 `pyproject.toml` 的 dev 依赖并在 AGENTS.md 注明；pyc 定期清理。

### 5.3 工作区未提交

- 5 个已修改（AGENTS.md、Claude/skills/INDEX.md、3 个 skill 文件）
- 67 个未跟踪文件

**建议**：提交前跑 pre-commit 三闸（`repo_governance_check.py --warn` + `doc_path_refs.py` + `audit_destructive_default.py`），不得 `--no-verify`。

---

## 六、处置优先级

| 优先级 | 事项 | 影响 |
|---|---|---|
| **P0** | KOR SKILL.md 回归生成器管控 | 解 5 个红 + 恢复该区渲染能力 |
| P1 | 拆 `campaign.py` / `audit_structure.py` | 降维护成本 |
| P1 | 明确 tracking 入库边界 | 版本库瘦身 |
| P2 | 合并 6 个 audit 脚本 | 治理统一入口 |
| P2 | 裁决台账 517 PENDING 处置 | 守护恢复有效 |
| P3 | conftest 加解释器断言 | 避免踩坑 |
| P3 | 提交前跑 pre-commit 三闸 | 合规 |

---

## 附：审计方法

- 结构：`find` / `du` 静态统计（排除 `.venv`）
- 测试：`world-quant-brain-mcp/.venv` 下 `pytest -q`，结果解析自 `logs/test-results.xml`
- 生成器幂等：`src/wqb/profiles/render.py::plan(['KOR'])`
- 双轨同源：`methodology_rules.json` 与 `docs/experience/` 对照
