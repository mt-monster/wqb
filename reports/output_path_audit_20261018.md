# 产物输出规则与路径治理审计

> 审计日期：2026-10-18　范围：AGENTS.md 约定 + 代码硬编码 + 磁盘实证
> 结论：**规则体系完备且多数已被守卫覆盖**；存在 **1 个 P0 落点失控（已第 3 次复发）** + 若干清理缺口。

---

## 一、约定的产物输出规则（现行）

来源：AGENTS.md §8.13「目录归属与命名规范」、§8.4 台账、S7/S11/S16 守卫。

| 产物类型 | 唯一落点 | 命名 | 守卫 |
|---|---|---|---|
| 战役 / 评审**产物**（workflow 自动产出、工具直写） | `output_report/` | snake_case + `YYYYMMDD` 作后缀 | S16 规则⑤（禁 `.py`）、⑦（子目录 kebab） |
| **人工**审计 / 复盘 / 演练 / 价值评估 | `reports/<主题>_<YYYYMMDD>.md` | 同上 | S16 规则⑥ |
| 长期规范 / SOP / 速查 | `docs/` | **不要求带日期** | S16 规则⑥例外 |
| 可复用 CLI | `tools/` + `tools/README.md` 登记一行 | snake_case | S7 白名单 + S11 主题归属 |
| 一次性 / 会话草稿脚本 | `logs/_tmp_*.py`（用完即删） | `_tmp_` 前缀 | S7 |
| 区域专属探针 | `tracking/<REGION>/scripts/`，用完进 `scripts/archive/` | — | S7 |
| 运行期断点（续跑） | `results/` | `*_checkpoint.json` | ⚠ **移动会破坏续跑** |
| 运行期缓存 | `cache/` | — | `tools/retention.py` |
| 日志 | `logs/` | — | `clean_logs.py` |
| 归档（**归档而非删除**） | `attic/<主题>_<YYYYMMDD>/` | 日期化目录 | §7 |

### 边界判据（消除两头分流的关键一条）

> **凡 workflow / 战役自动产出** → `output_report/`
> **凡人工撰写的审计 / 评审 / 复盘 / 演练 / 价值评估** → `reports/`

⚠ 判据是「谁产出」而非「内容像什么」。已记载的反例：`output_report/ra_pipeline_stage_audit_20260916.md`
通篇是审计内容，应属 `reports/`。

### 命名例外（既定、不要"顺手修正"）

- `campain` 是既定文件名非笔误（`dataset_experience.py` 生成 + `step9_audit.py` 校验 + 多 skill 引用）
- `*_ideas.md` / `*_campain.md` 机器产物不强制带日期（消费方依赖同名覆盖）
- 区域码大写开头（`KOR_`/`GBR_`…）豁免 snake 检查，纯英文大写（`ANALYST_`）不豁免
- `reports/` 一层子目录 4 条进 `S16_DIR_LEGACY` 只登记不回改

---

## 二、实测：代码里的路径硬编码分布

扫描 `src/` `tools/` `world-quant-brain-mcp/`（排除 `.venv`）：

| 目录 | 引用处 |
|---|---|
| `tracking/` | 209 |
| `results/` | 103 |
| `reports/` | 91（去重后 35，含外部论文 URL 误匹配如 `reports/2000/tr371.pdf`） |
| `logs/` | 87 |
| `cache/` | 75 |
| `output_report/` | 30 |

`output_report/` 的写方含 AGENTS.md 点名的三个工具直写件：
`archive_submit_ready.py`(2) / `complexity_scan.py`(1) / `run_grouped_tests.py`(2)。

---

## 三、P0 — 落点失控：仓库根长出技能树副本（已第 3 次复发）

### 现象

根目录出现 **`wq-brain-ra-usa/`**：466 文件 / 6.1 MB / **48 个子目录**，mtime `2026-10-17 22:50`。

- 与 `Claude/skills/` 的 48 个子目录数相同，`INDEX.md` 内容一致 ⇒ **是整棵技能树的完整副本**
- `git` 未追踪（0 文件）、`.gitignore` 无对应条目
- 零引用，却能被后来者误当成「在用的技能源」

### 根因（代码层面已定位）

`tools/sync_skills.py::resolve_install_roots()` 用 `_is_repo_root_or_ancestor()` 拦截危险安装位：

```python
resolved = candidate.resolve()
repo = REPO_ROOT.resolve()
return resolved == repo or repo.is_relative_to(resolved)
```

**只判「安装位 == 仓库根」或「安装位是仓库根的祖先」，不判「安装位是仓库根的子孙」。**

实测：

| 候选安装位 | blocked |
|---|---|
| `.`（仓库根） | ✅ True |
| `..`（祖先） | ✅ True |
| `wq-brain-ra-usa`（仓库内子目录） | ❌ **False** |
| `Claude/skills/wq-brain-ra-usa` | ❌ **False** |

⇒ 当 `WQ_SKILLS_DIR`（或等价变量）被指到仓库内任一子目录时，同步会把 `Claude/skills/<name>/`
逐个铺成 `<安装位>/<name>/`，整棵技能树落进仓库。

### 这不是新 bug —— 源码注释自记载已复发

`sync_skills.py` 第 123 行注释原文：

> 于是**仓库根长出整棵技能树**（`wq-brain-ra-usa/SKILL.md`、`alpha-expression-verifier/` …）。
> 实测发生过两次（2026-10-14 同一形态复发）……

注释**明确点名了 `wq-brain-ra-usa`**，与当前目录名完全一致 ⇒ 本次（10-17）是**第 3 次**，
且既有守卫（只拦根/祖先）对这一形态**从未生效**。

同类既往归档：`attic/kor_skill_install_stale_20261015/`（含 `SKILL.md.bak-replace`）。

### 修复建议

1. **扩守卫**：`_is_repo_root_or_ancestor()` 增补「子孙」判定——
   `resolved.is_relative_to(repo)` 亦应 blocked（安装位落在仓库内同样会污染工作树）。
   建议改名为 `_is_repo_related()` 并覆盖三种关系：相同 / 祖先 / 子孙。
2. **清理现存副本**：按 §7「归档而非删除」移到 `attic/sync_strays_20261018/`，
   **不要直接删**（需保留证据以定位是谁把安装位指错了）。
3. **加闸**：把「仓库根不得出现非约定顶层目录」纳入 `audit_structure` S7 白名单的
   **磁盘面**检查（现 S7 取 git 跟踪面 ⇒ 未追踪的 `wq-brain-ra-usa` 结构性失明）。
   ⚠ 判据取磁盘而非跟踪面 —— 与 AGENTS.md 已记载的「伞的失效判据取磁盘」同坑。

---

## 四、P1 — 运行期目录无容量闸

| 目录 | 规模 | gitignore | 清理工具 |
|---|---|---|---|
| `cache/` | 1315 文件 / **309 MB**（`_probe/probe.db` 283 MB） | ✅ | `retention.py` |
| `logs/` | 1751 文件 / 13 MB | ✅ | `clean_logs.py` |
| `results/` | 236 文件 / 7.0 MB（160 个 `*.json` checkpoint） | ✅ | ❌ **无** |

- `retention.py` 覆盖 `data/ cache/ logs/`，**不覆盖 `results/`**。
- `results/` 是续跑断点区（`backfill_longcount.py`、`batch_submit_verdict.py`、`prod_blocked_recheck.py`
  硬编码引用），AGENTS.md 明示「移动会破坏续跑」⇒ **不能靠移动解决，只能靠容量闸**。

**建议**：`retention.py` 增补 `results/` 策略（按 mtime + 命名 `*_checkpoint.json` 回收，
但**永不删在跑批次的活跃断点**——需与续跑状态联动，保守起见默认只报告不删）。

---

## 五、P2 — 文档 / 注释里的历史路径死指针

代码引用了已不存在的产物路径（不影响运行，但误导后来者）：

| 失效引用 | 出处 | 现状 |
|---|---|---|
| `python reports/opswap_driver.py` | `tools/legacy/opswap_driver.py` 第 11–12 行 docstring | 脚本已迁到 `tools/legacy/`，docstring 未同步 |
| `output_report/diff_t4.py` | `audit_structure.py` 第 1521 / 1601 行注释 | 是**历史反例记载**（已被规则⑤拦下），非活跃引用 |
| `output_report/reports` | 同上 | 历史引用，`output_report/` 现无一层子目录 |

核实结果：`output_report/` 下 **0 个 `.py`**、**0 个一层子目录** ⇒ S16 规则⑤⑦ 实际执行良好。

**建议**：docstring 与注释里的路径纳入 `doc_path_refs.py` 扫描面；迁移脚本时同步改用法示例。

---

## 六、P3 — 受控豁免（维持现状，不要动）

`reports/` 一层子目录 9 个，风格两套并存：

- kebab（5）：`eur-mining` `forum-experience` `gbr-campaign-final` `project-audit` `tooling-research`
- snake（2）：`dataset_experience` `forum_alpha_research`
- `_refs` 消歧后缀（2）：`ra_pipeline_stage_review_20260927_refs` `skills_review_20260929_refs`

后 4 条已在 `S16_DIR_LEGACY` 登记豁免并带代价证据（生成器写名 / 脚本自引用 / 同名消歧）。
AGENTS.md 已裁定**不做 snake 化**（会造成 20+ 处死指针）。⇒ 维持现状。

---

## 七、处置优先级

| 优先级 | 事项 | 动作 |
|---|---|---|
| **P0** | 仓库根 `wq-brain-ra-usa/` 技能树副本 | ① 扩 `_is_repo_root_or_ancestor` 到子孙判定 ② 归档而非删除 ③ S7 取磁盘面 |
| P1 | `results/` 无容量闸 | `retention.py` 增补 `results/` 策略（默认只报告） |
| P2 | docstring 历史路径死指针 | 纳入 `doc_path_refs.py`；迁移时同步示例 |
| P3 | `reports/` 命名两套 | 维持（`S16_DIR_LEGACY` 受控豁免） |

---

## 附：审计方法

- 约定：`AGENTS.md` §8.13 / §8.4 / S7 / S11 / S16 条目
- 硬编码：`grep -rhoE "<dir>/[A-Za-z0-9_/.-]*"` over `src/ tools/ world-quant-brain-mcp/`（排除 `.venv`）
- 守卫缺口：直接实例化 `tools/sync_skills.py` 调 `_is_repo_root_or_ancestor()` 实测四种候选
- gitignore / 追踪：`git check-ignore` + `git ls-files`
- 规模：`du -sh` + `find | wc -l`
