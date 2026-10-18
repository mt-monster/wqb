# Skills 层级规划审查：RULES / CONFIG / REFERENCES / SCRIPTS

> **as_of**：2026-10-18 ｜ **审查范围**：`Claude/skills/`（45 个 skill）+ profiles 生成层（`src/wqb/profiles/`）+
> `docs/experience/` 经验库 + `tracking/<R>/config/` 控制层 + 本轮 USA 两战役实测。
> **方法**：读代码契约（`render.py` / `check_structure` / `skill_lint` / `test_profiles_layer`）→ 跑守护测试取读数 →
> 查机器层（sqlite）覆盖度 → 对照 `CONTRACT.md` 第 6 条与 `project_layout_audit_20261014` §6 命名规范。
> **证据口径**：本文所有「实测」均带命令或测试读数；无实测的判断标「待核」。

---

## 0. 结论速览

**四层划分本身是对的**（RULES 放规则 / CONFIG 放可改控制值 / REFERENCES 放实证 / SCRIPTS 放可执行），
问题不在分层，而在**层与层之间的义务没有落成机械闸**，导致三类实测漂移：

| # | 问题 | 证据 | 建议 |
|---|---|---|---|
| P0-1 | **references 命名规则只在代码里**，文档层无任何说明 ⇒ 已产生 **7 个孤儿分支文件**（DEU 2 / GBR 5），本轮 USA 也差点再犯（2 个战役文件无 `_` 前缀） | `test_profiles_layer::test_region_skills_exist_and_match_cells_and_settings` 实测红 | P0-1 |
| P0-2 | **字段画像三层并行且互相矛盾**：机器层 `field_profile_usa` 对 analyst44 只有 **8 条**早期单测记录（best_s 最高 `anl44_best_eps` 1.54），文档层实测是「17 配对里 eps 最强、背离族才是真腿」；`field_semantic_type` 对 USA **完全空白**（仅 GBR 有 15522 行） | sqlite 实测 | P0-2 |
| P1-3 | **区域 SKILL.md 混入手写实证叙事**（USA SKILL.md 内嵌「2026-10-14，16 波/64 条实测」速查表），违反 `CONTRACT.md:6`「实证叙事、事故、区域细节放 references/」 | `SKILL.md:163-180` | P1-3 |
| P1-4 | **references 无索引层**：类别卡有生成表，战役/专题文档靠 SKILL.md 手写段落引流 ⇒ 新文档默认检索不到 | 结构实测 | P1-4 |
| P2-5 | **一次性脚本无归口**：本轮 campaign 的 `submit_*.py` / `recheck_pc.py` 落在 `tracking/USA/campaign_*/tmp/`，与 `tracking/<R>/scripts/`（AGENTS §8.13 规定的家）并存 | 目录实测 | P2-5 |

---

## 1. 四层现状盘点（实测）

| 层 | 单一事实源 | 生成 / 维护方式 | 机械闸 | 体量 | 达标 |
|---|---|---|---|---|---|
| **RULES** | `Claude/skills/<skill>/SKILL.md`；跨 skill 契约 = `CONTRACT.md`；路由 = `INDEX.md`；术语 = `GLOSSARY.md` | 区域 skill 的 SKILL.md = `render.py` 生成块（`region-panel` / `cells-index`）+ 手写正文 + `profiles:manual` 保留块 | `test_skill_integrity` / `test_skill_boundaries` / `skill_lint`；体量目标 ≤250 行（USA 185 行 ✅） | 45 skill / USA 164K | ✅ 良好 |
| **CONFIG** | `tracking/<R>/config/{settings,thresholds,cells}.json`；方法论 = `wq-brain-campaign-toolkit/config/methodology_rules.json` | 手改 → `profiles check` → `render --apply` 渲进 SKILL.md 生成块；**覆盖值必须带 `_evidence`**（波号/alpha id/日期），无证据校验不通过 | `test_profiles_layer`（cells 合法性 + 区域面板与 settings 一致）/ `profile_drift_check.py` | 14 区 × 3 文件 | ✅ **四层里最扎实** |
| **REFERENCES** | `references/<cells类别>.md`（组合分支，含 `cell-panel` 生成块）+ `references/_*.md`（跨类别补充）；跨区域经验 = `docs/experience/`（01-05 + 3 篇方法论） | 类别卡随 cells 渲染；补充文档手写 | `check_structure()`：**非类别名且无 `_` 前缀 ⇒ 孤儿分支文件** | USA 12 篇 / experience 8 篇 | ⚠ 见 P0-1/P0-2 |
| **SCRIPTS** | skill 自带 `scripts/`（15 个 skill 有）；区域探针脚本的家 = `tracking/<R>/scripts/`（AGENTS §8.13）；仓库级引擎 = `tools/` | 手写 | `test_skill_hooks_and_tools_guard`（skill 内脚本引用真实存在） | 15 skill 带 scripts | ⚠ 规则只在生成器与 AGENTS，未进 CONTRACT（P2-5） |

---

## 2. 逐层评估

### 2.1 RULES — 判定正确，两处需收口

**做对的部分**：① 区域 skill 的控制值与正文**物理分离**（生成块 vs 手写），重渲只刷生成块、不动正文；
② `profiles:manual` 保留块给了「区域内手写补充」一个合法位置；③ 体量有目标（≤250 行）且实测达标。

**问题 1（P1-3）｜实证叙事寄生在 RULES 层**：`wq-brain-ra-usa/SKILL.md:163-180` 内嵌
「未点亮塔实证速查（2026-10-14，16 波 / 64 条实测）」整节 + 最优候选数值，与 `CONTRACT.md:6`
「实证叙事、事故、区域细节放 `references/`」相悖。后果不只是风格问题——**它没有 `as_of` 字段**
（CONTRACT 要求快照类事实带 `as_of` 与失效条件），半年后无人知道这批数字是否还有效。

**问题 2｜责任边界靠注释维持**：没有任何测试断言「SKILL.md 手写区不得出现实测数字」。生成块有 `check`，
手写区是自由地带 ⇒ RULES 层会持续被实证内容侵蚀。

### 2.2 CONFIG — 判定正确，是全仓最佳实践

`cells.json` 的**覆盖值必须带 `_evidence`** 是关键设计：既让控制值可被程序消费，又让每个数字可追溯到波号/alpha id。
14 区共用同一 resolver（`explain` / `render` / `check` / `sync-cells`），单一事实源成立。

**待核的小问题**：区域控制值分散在三份文件（`settings.json` 仿真设置 / `thresholds.json` 阈值 / `cells.json` 组合覆盖），
新人不跑 `explain` 难以判断「该改哪个」——建议在 CONTRACT 的 CONFIG 段加一句三文件分工表（不改代码，纯文档）。

### 2.3 REFERENCES — 机制正确，但有两处实测缺陷

**做对的部分**：类别卡命名 = `cells.json` 的 category ⇒ **配置与文档用同一套键**，机器可校验；
`cell-panel` 生成块保证卡里的数据表与 cells 同步。

**问题 1（P0-1）｜命名规则只在代码里**：`_is_supplementary()`（`render.py:774`）用 `_` 前缀区分
「组合分支」与「跨类别补充」，但 CONTRACT / INDEX / 任一 SKILL.md 都没写这条。
实测后果：`test_profiles_layer` 长期红，7 个孤儿（DEU 2 / GBR 5）。本轮我自己新写的 2 个战役文件
（`unlit-tower-campaign-20261014.md` / `analyst-campaign-20261017.md`）也踩中——**已修为 `_` 前缀**。
注意 `project_layout_audit_20261014` §5 给的处置建议是「跑 `render --apply`」，**该建议无效**（render 只生成块，
不认领孤儿），正确处置是重命名或登记为 cells 类别。

**问题 2（P0-2）｜字段画像三层并行、结论互相矛盾**（本次最值得处理的发现）：

| 层 | 载体 | analyst44 的状态 |
|---|---|---|
| 机器层 | sqlite `field_profile_usa`（**85,184 行**） | 仅 **8 条**，全是早期单信号探针（`n_tests=1`），best_s 最高 `anl44_best_eps` 1.54 |
| 语义层 | sqlite `field_semantic_type`（15,522 行） | **USA 空白**（只有 GBR 有数据） |
| 文档层 | DEU `_field-profile.md`（视图+九类 verdict）/ GBR `_field-profile-playbook.md`（快照）/ 本轮新增 USA `_usa-mining-playbook-20261018.md`（散文表） | 300 字段画像 + 17 配对 + 回测结论齐全 |

⇒ **矛盾实证**：查库会得到「`anl44_best_eps` 是 analyst44 最强字段（1.54）」，
而本轮 60 波实测是「单指标 eps 修正 prod 0.7775 撞墙、**背离族才是可交付腿**」。
**下一位挖掘者若只查 DB 会做出与文档相反的决策**——这是分层设计最典型的失效模式：
事实源没有随文档层一起更新。

**问题 3（P1-4）｜无索引层**：类别卡有生成表，但战役/专题/快照文档只能靠 SKILL.md 手写段落引流
（USA 现在是我手写了两行链接）。文档一多就必然检索不到。

### 2.4 SCRIPTS — 分层正确，规则未成文

15 个 skill 带 `scripts/`（多为单文件验证器）；区域 skill 原则上不放脚本，探针脚本家 = `tracking/<R>/scripts/`
（`render.py` 的 KOR 段已写明，AGENTS §8.13 亦有）。例外：`wq-brain-ra-deu/scripts/` 存在但规则未登记 ⇒
后来者会以为区域 skill 可以带脚本。

**问题（P2-5）**：本轮一次性脚本（`submit_base_payment_top3.py` / `recheck_pc.py` / `submit_and_recheck.py`）
落在 `tracking/USA/campaign_20261017/tmp/`，既非 `tracking/<R>/scripts/`（约定的家）也非 `tools/`（可复用引擎），
**没有可检索入口**。它们承载的是「提交链路实战」知识，价值高于一次性流水账。

---

## 3. 建议（按优先级）

### P0-1 references 命名规则成文 + 清孤儿

1. 在 `CONTRACT.md` 的 REFERENCES 段写死两条命名：**组合分支 = `references/<cells 类别名>.md`（须含 `cell-panel` 生成块）**；
   **其余一切文档 = `references/_<主题>.md`**。附一句「新增战役/专题文档直接用 `_` 前缀，render 不会认领也不会误判」。
2. 修 7 个孤儿：DEU 2 个 + GBR 5 个（**归属并发会话，本轮按治理纪律未代改**；正确处置是重命名为 `_` 前缀 + 更新引用）。
3. 修正 `project_layout_audit_20261014` §5 第 3 条的处置建议（`render --apply` 对孤儿无效）。

### P0-2 字段画像回灌义务（收益最高）

1. **RA 步 9（回写）加一条硬要求**：战役中产生的字段级结论（哪个字段/族有效、什么类型、覆盖率、代表 S）
   必须回灌 `field_profile_<region>`；语义类型结论回灌 `field_semantic_type`。
   入口已存在：`tools/field_profile_backfill.py`、`tools/field_semantic_classify.py`、`tools/category_field_triage.py`。
2. 加一个 gate（可用 `audit_structure` 的模式）：**主力数据集在 `field_semantic_type` 缺失 ⇒ 警告**，
   避免「文档写完了、库还是空的」。
3. 本轮 USA analyst44 的 8 条陈旧记录应回灌替换（现库内 best_s 与文档结论矛盾，见 §2.3）。

### P1-3 区域 SKILL.md 的实证段迁 references/

把 USA SKILL.md:163-180 那节整体迁到 `references/_unlit-tower-campaign-20261014.md`（文件已存在），
SKILL.md 只留一行指针 + `as_of`。这样 RULES 层回到「只放规则」，实证有 `as_of`、可被 references 索引收编。

### P1-4 references 索引块

在 `render.py` 加一个 `references:index` 生成块：自动列出 `references/_*.md`（文件名 + 首行标题 + 一句话摘要）。
好处：新增文档自动出现在 SKILL.md，不需要手写链接；顺带让 P0-1 的命名违规在生成时就可见。

### P2-5 一次性脚本归口 + 脚本规则成文

1. 战役一次性脚本统一放 `tracking/<R>/campaign_<date>/scripts/`（campaign 目录内、可检索、与 `tracking/<R>/scripts/` 的
   区域公共脚本分层），并在 `tracking/<R>/README.md` 登记入口。
2. CONTRACT 的 SCRIPTS 段写清：**skill 自带 scripts/ 仅放该 skill 的验证器；区域探针/战役脚本家 = `tracking/`**；
   DEU 的例外需登记或迁走。

---

## 4. 本轮实测读数（可复现）

| 命令 | 读数 |
|---|---|
| `pytest tests/unit/09_core/test_profiles_layer.py -q` | 修复前 `1 failed`（7 孤儿：DEU 2/GBR 5 + USA 2）；修复 USA 后仍 `1 failed`（DEU 2/GBR 5，非本轮改动） |
| `pytest tests/unit/07_docs_skills/{test_docs_consistency,test_experience_kb_refs,test_skill_lint}.py -q` | 本轮新增文档相关全绿；余 1 红为**他人债**：IND `expr-gate` 新增违规 + superalpha 基线陈旧 |
| `python tools/skill_lint.py`（`const-literal`） | 本轮文档 1 处「门槛数字 1.58 抄写」⇒ 已改为引用 `PLATFORM_CHECK_LINES.low_2y_sharpe_min` |
| sqlite `field_profile_usa` | 85,184 行；analyst44 仅 8 行（`n_tests=1`，best_s 最高 `anl44_best_eps` 1.54） |
| sqlite `field_semantic_type` | 15,522 行，**仅 GBR**；USA 空白 |

## 5. 与既有审计的关系

- `project_layout_audit_20261014` §3/§6 已定目录组织与命名规范，本文**不重复其结论**，只补「skills 四层义务」这一维。
- 该报告 §5 第 3 条把孤儿归因为「未跑 render --apply」——本文更正：render 不处理孤儿，须重命名。
- 该报告把 DEU/GBR/USA 的孤儿归给「并行会话」——本文核实归属（DEU 2 / GBR 5 仍红，USA 2 已由本轮修复）。
---

## 6. 专项评估：是否该按 `rules/ config/ references/ scripts/` 目录治理每个 region？

> 问题（2026-10-18）：USA skill 是否应按四目录建结构，并推广为「每个 region 独有的挖掘结构」。

### 6.1 结论

**不建议在 skill 内新建四目录**——四层职责已经由**不同载体**各自承担且有机械闸守护，
新建目录会与生成器/单一事实源/测试链正面冲突。
但**「每区独有挖掘结构」这个诉求成立**，且已部分实现——正确载体是
`SKILL.md 生成块` + `references 文件族` + `tracking/<R>/`，**不是目录**。

### 6.2 现状实证：14 区形态高度一致，差异来自「有没有开战役」

| region | cells 类别 | references 篇数 | SKILL 行数 | 子目录 | tracking 资产 |
|---|---:|---:|---:|---|---|
| USA | 10 | 13 | 186 | references | 全套（**无 scripts/**） |
| KOR | 11 | 17 | **563** ⚠ | references | 全套（含 scripts/） |
| GBR | 14 | 21 | **315** ⚠ | references | 全套（含 scripts/） |
| DEU | 11 | 16 | 252 ⚠ | references + **scripts/** ⚠ | 全套（含 scripts/） |
| TWN | **0** | **0** | 122 | **无** | **空目录** |
| amr/chn/jpn | — | 2–3 | 149–159 | references | — |

⇒ **形态差异 = 战役历史差异，不是设计差异**。TWN 无 references 是因为它从未开战役（`tracking/TWN/` 为空）。

### 6.3 为什么不该建目录（逐层证据）

| 层 | 现有载体 | 若新建目录的后果（实测依据） |
|---|---|---|
| RULES | `SKILL.md` | `render.py:735/788` 硬编码 `d / "SKILL.md"`；生成块（`region-panel`/`cells-index`）+ 保留块（`profiles:manual`）双向管理；`test_skill_integrity` / `test_skill_boundaries` / `skill_lint` 三重守护 ⇒ 新目录 = 与生成器争夺同一份事实源 |
| CONFIG | `tracking/<R>/config/*.json` | `profiles explain/render/sync-cells` 全部按 `config_dir_of(r)` 解析；覆盖值强制 `_evidence`；AGENTS §1 已把 tracking/ 定位为**区域数据资产层** ⇒ 搬进 skill 会复制事实源并断掉整条 profiles 链 |
| REFERENCES | `references/<类别>.md` + `references/_*.md` | `render.py:746/804/829` 三处硬编码 `d / "references"`；孤儿判据也在这 ⇒ 缺的是**索引**（§3 P1-4），不是目录 |
| SCRIPTS | skill 内 `scripts/` = 本 skill 验证器；区域探针/战役脚本家 = `tracking/<R>/scripts/`（AGENTS §8.13） | DEU 的 skill-local `scripts/`（3 个一次性扫描脚本 + 47KB JSON）是**未登记例外**，该迁走而不是把它升级成"每区都有 scripts/" |

### 6.4 该做的 4 件事（把「独有结构」变成可检索、可校验）

| # | 动作 | 解决什么 |
|---|---|---|
| **A** | `render.py` 加 `references:index` 生成块：自动列出 `references/_*.md`（文件名 + 首行标题 + 一句话摘要） | 「有文件但检索不到」；新增文档自动出现在 SKILL.md，不靠手写链接 |
| **B** | 每区 SKILL.md 固定四段「区域结构声明」：六步覆盖 / references 文件族 / 探针脚本家 / 与 tracking 的关系（前三段生成、末段手写） | 14 区形态一眼可比；差异显式化而非隐形 |
| **C** | 归一 4 处越界：DEU `scripts/` → `tracking/DEU/scripts/`；GBR 315 行 / KOR 563 行超体量（实证段下沉 references）；TWN 显式声明「未开战役」或冻结；USA `tracking/USA/scripts/` 补建（探针脚本无家） | 消除 4 处不一致 |
| **D** | 差异化只落 `cells.json`（控制值）+ references 内容（实证），**不落目录** | 保住 render/check/test 三条链按「类别名 + `_` 前缀」解析的约定 |

### 6.5 附带的真实痛点（比 skill 内目录更值得治）

`tracking/USA/` 根层散落 **22 个 `feature_engineering_wave*.md` + 若干 wave json/log**，与 `config/ references/ results/ reviews/` 并列。
⇒ 区域资产层**内部**才是当前结构治理的主要战场（skill 内加目录解决不了它）。
