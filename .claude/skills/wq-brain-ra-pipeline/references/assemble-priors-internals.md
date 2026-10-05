# assemble-priors 内部映射（供核对；**勿手写组装**）

> 主 SOP 步 4 用 `workflow_campaign(stage="S2", subcommand="assemble-priors")` 确定性组装 priors，落 `<campaign>/priors/<region>_priors.json` 与 DB 快照 `priors_snapshot_<region>`（含 sha256；sha 不写进文件本体）。
> 本文是 `Claude/skills/wq-brain-campaign-toolkit/scripts/assemble_priors.py::assemble_priors_dict` 的人读版，用来回答「为什么这条先验没进 prompt」。**出入以代码为准，发现出入请修本文。**
> （2026-09-29 按代码重写：旧文写成「`GLOBAL/region_kb.templates[]` → wins」「`methodology[]` / `signal_family_rules[]` → region_context」，代码里**没有**这两条；
> 反过来，真正承载 S6 回写的 `registry_empirical` win / dead_end 层旧文一个字没提。）

## 取数映射

**`wins`**（去重，合计 ≤ 6；`banned=true` 的条目不注入；按序取，先到先占名额）：

| # | 来源 | 进 prompt 的形状 |
|---|---|---|
| ① | `region_kb.forum_templates[]`（论坛验证模板，含完整表达式 + 实测指标；最高优先级） | `id=name` · `key="expr=… \| metrics=…(前 4 项) \| 变体: …(前 2 个)"` |
| ② | `region_kb.win_recipes[]` | `id=name` · `key=skeleton` · `evidence` |
| ③ | **`registry_empirical` 的 `win` 层**（按登记先后**倒序**：新的先取；两种 payload 写法都认：`id / what / key` 与 `example_id / mechanism / evidence`） | `id` · `what` · `key` · `evidence` |
| ④ | `KB/template_kb` 中 `validated[<本区>]` 非空的模板 | `key="skeleton=…; iron_law=…"` |
| ⑤ | `region_kb.active_alphas[]`（活跃 ACTIVE alpha，补充胜绩） | `key="ACTIVE alpha (详见 region_kb)"` |
| — | 以上全空 → 本区 profile front-matter 的静态 `win_recipes`（仅 DB KB 空时的种子） | — |

**`dead_ends`**（去重，合计 ≤ 12）：① `region_kb.dead_patterns[]`（机制级死路，字符串直传，**名额有限时先保机制级**）→ ② **`registry_empirical` 的 `dead_end` 层**（数据集 / 家族级；倒序；`family` + `reason`）→ ③ `KB/template_kb` 中 `failed[<本区>]` 非空的模板 →（全空时）profile 的 `signal_families_exclude`。

**`region_context`**：`region_kb.tier` / `settings_proven` / `notes`（取前 6，GEM 只渲染前 4）/ `operator_usage_stats`。
**`gate_priors`**（来自 `tools/build_gate_prior_from_inventory.py --write-priors`）：`by_operator_count` / `by_field_family` 渲染进 GEM prompt（表达式层能作用）；`by_decay` / `by_neutralization` 是仿真设置，**不进 prompt**，assemble 只把它们落成只读的 `settings_prior` 快照，真正改写发生在步 6 的 `pipeline.py run`（显式 `--set` 钉住的维度不动）。
**`skeleton_field_matrix`**：`KB/operator_principle_kb` 存在时才有（字段特性 × 算子原理 → 有效 / 死 / 正交提示；末尾恒带一条「加权混信号 = 闸 5 poison」的死路）。

## 截断可见，不是静默丢弃

超过名额的条目列在 `_meta.truncated`（`wins` / `dead_ends` 各一份 id 清单）。新封存的死路排在 registry 层前面（倒序），所以不会再出现「字母序截断 → 新死路永远进不了 GEM」（2026-09-27 R18）。
**看到 `truncated` 非空 = 有先验被挤出 prompt**：是机制枯竭之外的另一个原因，评估要不要清理陈旧条目，而不是加大名额。

## 不进 priors 的

`KB/community_tpl_kb` **不进 priors**（候选未实证，注入稀释 concept-first）。它服务两个场景：步 5 多样性 FAIL 回步 4 补骨架时按 `category` 检索换腿参考（占位符按 `placeholder_conventions` 替换）；Mode B Step B1 找骨架。
**取骨架前必查键内 `ghost_operator_advisory`**：含幽灵 / 未验证算子的骨架必须替换为已验证等价算子（映射表见键内与 `docs/reference/community_tpl_library_sequel.md` §十八）或先 `preflight_expressions` 实测，否则整批 ERROR / CANCELLED。这是步 4 的独立必做项，步 5 失败分支重复引用。

## 生命周期闭环：S6 写什么 → 下一次 S2 读到什么

| S6 回写 | 落点 | 下一次 assemble-priors |
|---|---|---|
| 判死：`seal_dead_end(...)`（或 `campaign.py registry add-dead-end`） | `registry_empirical` `dead_end` 层 | 进 `dead_ends` ②（倒序，新封存者靠前） |
| 胜绩：`upsert_registry_empirical(layer="win", …)`（或 `campaign.py registry add-win`） | `registry_empirical` `win` 层 | 进 `wins` ③ |
| 波后评审：`pipeline.py --review` | `region_kb` 的 `recent_waves` / `gate_priors_local` / `updated_at` | `gate_priors` 与区域上下文自动变新 |
| `region_kb.win_recipes` / `dead_patterns` / `forum_templates` / `template_kb` | **没有脚本写入方**（`docs/ledger_keys.json`：`template_kb` 与 `operator_principle_kb` 登记为 orphan；`region_kb` 的这几个数组靠人工 / agent 维护） | 读取方容忍缺失 |

**S6 回写之后必须再跑一次 assemble-priors** 刷新快照（GEM 对 stale 快照只 WARN 不阻断）——这是步 9 完成定义的一部分。
profile 静态 priors 仅作 DB 空时的种子，不再手工更新。

> 键契约（写入方 / 读取方 / 缺失行为）见 `docs/ledger_keys.json`：`priors_snapshot_<region>`、`assemble_priors_cache_<region>`、`region_kb`、`template_kb`、`community_tpl_kb`。
