# Claude/skills 写者收敛核查（2026-10-20）

**背景**：`Claude/skills/` 是 skill 权威源（SOURCE），`sync_skills.py --apply` 会把
SOURCE 同步到 6 个安装位（`~/.workbuddy`, `~/.claude`, `~/.cursor`, `~/.codex`,
`~/.cline`, `~/.agents` 下的 `skills/`）。**任何绕过 sync 直接写这些路径的操作
都会造成安装位与 SOURCE 分叉**——本轮审计要确认"唯一合法写者"这个约定在代码层面成立。

---

## 1. 结论：目前约定**基本成立**，但存在两类盲区

| 场景 | 现状 | 备注 |
|---|---|---|
| 写 6 个安装位 (`~/.<agent>/skills/**`) | ✅ 仅 `tools/sync_skills.py` | `shutil.copy2` 唯一入口（`sync_skills.py:421`） |
| 写 SOURCE (`Claude/skills/**` in repo) | ⚠️ 三个潜在写者 | 见 §2，多数是「权威↔内嵌副本」内部对齐 |
| `audit_write_targets` 是否覆盖此面 | ❌ **不覆盖** | 该闸只解析字面量路径，`Path.home()` / `expanduser()` 动态路径全部落 UNKNOWN |

---

## 2. 三个写 SOURCE 的候选（复核结果）

### 2.1 `tools/sync_skills.py` — ✅ 权威同步工具

`shutil.copy2(source / rel, dst)` 唯一写入点。目标动态取 6 个安装位。

### 2.2 `tools/sync_gem_embedded_skill.py` — ⚠️ 权威↔内嵌副本对齐（合理）

- `SKILLS_DIR = REPO_ROOT / "Claude" / "skills"`（`sync_gem_embedded_skill.py:40`）
- `EMBEDDED_ROOT = SKILLS_DIR / "brain-make-some-gem" / "scripts" / "trailSomeAlphas" / "skills"`
- 语义：SOURCE 里 `brain-make-some-gem/scripts/trailSomeAlphas/skills/**` 存在**嵌套副本**
  （供脚本运行内嵌引用），本工具把两处内容对齐，属于**权威面内部一致化**，不是分叉源。
- 判定：**保留**（写目标是 `EMBEDDED_ROOT` 而非 `SOURCE` 主根，且是明确的对齐器）。

### 2.3 `Claude/skills/pull-brain-skills/scripts/pull_skills.py` — ✅ 合规

- `copy_skill_folder(src_folder, dest_root, ...)` 通过 `shutil.copytree` 写入 `dest_root`
- 有明确保护：`is_live_dest()` 判断，若 `dest_root` 是仓库根祖先，会拒绝（`pull_skills.py:327`）
- 默认行为：写临时 staging 目录，要求人工审阅后再移到 `Claude/skills/`
- 判定：**保留**（是刻意设计的入库流程，且带保护闸）。

**综上**：目前**没有任何脚本能绕过 sync 直接污染 6 个安装位**——这是当前最关键的收敛结论。
SOURCE 面虽然存在 3 个写者，但都是**明确对齐工具或入库流程**，不构成同步分叉风险。

---

## 3. `audit_write_targets` 的盲区

**问题**：该闸通过 AST + 赋值图回溯解析路径字面量，只识别如下形态：

| 可解析形态 | 示例 |
|---|---|
| 字符串字面量 | `open("output_report/x.md", "w")` |
| `Path("literal")` | `Path("cache/x.json").write_text(...)` |
| 变量回溯 2 层 | `p = "cache"; Path(p)` |

**盲区**：`Path.home() / "..."`、`os.path.expanduser("~/.xxx")` 一类**动态 home-based 路径**
完全无法解析（`material` 为空），落 UNKNOWN。实测当前 UNKNOWN 97 条中，
**没有任何一条 target material 含 `home` / `expanduser` / `~`**——不是没写，
是根本没抓到。

**实际影响**：如果未来有人新增：

```python
# 假想的违规代码
with open(Path.home() / ".claude" / "skills" / "rogue.md", "w") as f:
    ...
```

`audit_write_targets` 会把它归为 UNKNOWN，不会阻塞提交。

### 3.1 建议（非阻塞，属后续改进）

**方案 A**：在 `audit_write_targets.py` 增加对 `Path.home()` / `os.path.expanduser()`
调用的静态识别，命中即判 UNKNOWN→VIOLATE（除 `tools/sync_skills.py` 白名单外）。

**方案 B**（更精确）：把 `Path.home()` / `expanduser()` 视为"目标动态"，
用 `_ALLOW_SUBSTRINGS` 白名单判定：路径含 `.workbuddy/skills/` 等安装位标识时，
只允许 `sync_skills.py` 命中，其它脚本判违规。

两种方案都需要在 AST 遍历阶段额外识别"Path.home / expanduser"调用节点，
比当前"字面量+赋值回溯"复杂一个量级。**本轮不做**，记录到此作为下一轮治理输入。

---

## 4. 与 §2.10 的联动（brain-alpha-judge 泄漏）

上一轮审计报告（§2.10）修的 `judge_alpha.py` 是**「写者把产物写到 SKILL_DIR/outputs」
导致安装位漂移**——那次是 skill 脚本自己污染安装位；本报告聚焦的是
「**其它脚本写安装位**」这种更隐蔽的模式。**两件事都是同一根问题**：
`Path(__file__)` / `Path.home()` 这类动态锚定，在没有 env + REPO_ROOT 双保险时
会让写目标漂移到安装位。

**统一教训**（写进 AGENTS.md 备忘）：**任何脚本要写仓库产物，必须走 env + REPO_ROOT
双保险解析**（参考 `wqb/provision/gem/pipeline_reports.py`、
`Claude/skills/brain-alpha-judge/scripts/judge_alpha.py` 的 `_resolve_outputs_dir`
模式），不得直接 `Path(__file__).parent / "outputs"` 或 `Path.home() / ".claude" / ...`。

---

## 5. 结论表

| 面 | 当前状态 | 治理闸 | 下一步 |
|---|---|---|---|
| 6 个安装位写者收敛 | ✅ 唯一合法写者 `sync_skills.py` | 无（靠代码约定） | 加静态识别 `Path.home()` 写者 |
| SOURCE (`Claude/skills/`) 写者 | ⚠️ 3 个，均已复核为合规（同步/对齐/入库） | 无 | 已在 §2 逐一确认，无需治理 |
| Skill 脚本误锚定安装位 | ⚠️ `judge_alpha.py` 曾犯，已修 | 靠代码约定 | 后续每个新 skill 参考 `pipeline_reports.py` 模式 |

**本报告不引入新的治理闸**——收敛结论已在代码层面成立，仅记录盲区留作后续改进参考。
