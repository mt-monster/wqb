# 项目 Skills 盘点与优化审计

> 审计日期：2026-08-05 ｜ 审计范围：当前项目 `wqb` 的全部 13 个 skill
> 数据依据：逐文件读取 13 个 `SKILL.md` + 实际路径探测（`worldquant_alpha` / `src/wqb` / `reference/` / `deliverables/` / 各 skill 脚本是否真实存在）

---

## 〇、总览：13 个 skill，三大阵营

| # | Skill（目录名） | 位置 | 行数 | 状态 | 领域 |
|---|---|---|---|---|---|
| 1 | brain-alpha-orchestrator | 工作区 | 46 | 启用 | WQ 挖掘·编排 |
| 2 | brain-alpha-research | 工作区 | 52 | 启用 | WQ 挖掘·研究 |
| 3 | brain-alpha-repair | 工作区 | 43 | 启用 | WQ 挖掘·修复 |
| 4 | brain-alpha-robustness | 工作区 | 100 | 启用 | WQ 挖掘·稳健性 |
| 5 | alpha-template-labs-data-analysis | 工作区 | 100 | 启用 | WQ 挖掘·Labs 数据 |
| 6 | wq-brain-ppa-mining | 用户级 | 266 | 启用 | WQ 挖掘·PPA 方法论 |
| 7 | wq-backtest-monitor | 用户级 | 145 | 启用 | WQ 挖掘·监控/审计 |
| 8 | worldquant-submit-alpha | 用户级 | 97 | 启用 | WQ 挖掘·提交 |
| 9 | wqb-concurrency | 用户级 | 74 | 启用 | WQ 挖掘·并发调优 |
| 10 | code-optimization | 用户级 | 143 | **disable** | 通用·代码冗余 |
| 11 | dead-code-cleanup | 用户级 | 185 | **disable** | 通用·死代码 |
| 12 | gold-analysis | 用户级 | 307 | **disable** | 通用·黄金分析 |
| 13 | jin10-news | 用户级 | 66 | **disable** | 通用·金十快讯 |

**结论性发现**：
- **WQ 挖掘知识被两套 skill 栈重复维护**：① 工作区 5 个（`brain-alpha-*` + labs），强依赖 `src/wqb` + `wqb` CLI + `reference/*.md`；② 用户级 `wq-brain-ppa-mining`，是同一套知识的 "MCP 轻量版重述"。重叠度高、各维护一份，极易漂移。
- **`worldquant_alpha/` 项目在整机不存在**（全盘 `find` 无结果）。用户级栈里 `wq-backtest-monitor`、`worldquant-submit-alpha`、`wqb-concurrency` 引用的 `worldquant_alpha/deliverables/tools/*`、`wd_lib_wrapper.py`、`worldquant_alpha/.env`、各类脚本**全部是死链**。
- **工作区 5 个 `brain-alpha-*` skill 在 3 个目录三重复制**：`.workbuddy/skills/`、`.zcode/skills/`、`wqb-share-03/.trae/skills/`。改一处不会同步，是最大的可维护性隐患。
- **4 个通用 skill 全部 `disable`，且引用本机不存在的路径/项目**（`/root/.openclaw/...`、Flask-DDD 项目、黄金数据源），在本 WQ 项目中是孤儿。

---

## 一、跨 skill 的系统性问题（最高优先级）

1. **双轨 WQ 挖掘栈 → 知识双份维护**：工作区 5 个 skill 与用户级 `wq-brain-ppa-mining`（同名主题、同套闸门、同套 API 约束、同套 WebDataScope 预筛）高度重叠。同一段 "IS_LADDER>1.58 / prod_corr<0.7 / coverage≥0.85" 在两边各写一遍。
2. **`worldquant_alpha/` 全局死链（阻断可用性）**：`wq-backtest-monitor` §8/§12/§13、`worldquant-submit-alpha`、`wqb-concurrency` 引用的 `deliverables/tools/*.py`、`wd_lib_wrapper.py`、`wd_lib/api/alphas.py`、`results/gen_pass_cheap_list.py` —— **全部 MISS**。
3. **工作区 skill 三重复制**（`.workbuddy` / `.zcode` / `wqb-share-03`）：5 个在 3 处各一份完整副本（含 `references/`），无单一真相源。
4. **提交职责被 3 个 skill 分散覆盖**：`worldquant-submit-alpha`（整篇）、`wq-backtest-monitor` §5/§10、`brain-alpha-orchestrator` §14 各写一份，口径各自为政。
5. **并发/令牌桶知识重复**：`wqb-concurrency`（整篇）与 `wq-backtest-monitor` §6（Token-Bucket C=7）讲同一件事。
6. **数据集体检脚本双副本**：`wq-brain-ppa-mining/scripts/dataset_health_check.py` 与 `wqb/tools/eur_field_coverage.py` 同源近重复。
7. **frontmatter schema 不统一**：部分 `name:`、部分 `title:`（`wq-brain-ppa-mining`、`wqb-concurrency`），`jin10-news` **完全无 name/title**。
8. **长 SKILL.md 用"日期追加"累积**：orchestrator 步骤 `14→14a→15→15a~15e→16→…→19`；research 步骤同理，正文是时间线补丁而非稳定程序。
9. **硬编码平台数据会漂移**：`wq-brain-ppa-mining` §8（区域实证表）+ §9.1（universe 全表）硬编码，平台 `get_platform_setting_options` 可运行时拉取。
10. **冗余元数据文件**：`gold-analysis`/`jin10-news` 双 `_meta.json`+`_skillhub_meta.json`；`code-optimization` 含 `_user_meta.json`。
11. **提交了 `.pyc`**：`wq-brain-ppa-mining/scripts/__pycache__/` 已进 skill 目录，应 gitignore/删除。

---

## 二、逐 skill 审计（仅列关键问题 / 改进，省略通用"规范/OK"项）

**【工作区级栈】**
- **1. brain-alpha-orchestrator**（46 行）：编排路由层（重依赖 reference + src/wqb）。⚠️ 依赖的 `wqb` CLI 命令已实测存在但未在 frontmatter 声明 `requires`；步骤是"日期追加"补丁日志。→ 加 `requires`；超长步骤外置；与 `wq-brain-ppa-mining` 明确分工。
- **2. brain-alpha-research**（52 行）：研究（数据集/字段/论坛模板/WebDataScope 预筛）。WebDataScope 规则与 orchestrator 重复；`tools/webdata_quality.py` 路径用 `../../../tools/` 需核对；步骤 15 极长。→ WebDataScope 预筛抽到单一 `reference/` 共用。
- **3. brain-alpha-repair**（43 行）：修复候选（降换手/提覆盖/降相关/轨迹恢复），聚焦，与 robustness 边界清晰。→ 去重与 orchestrator/robustness 的相关性内容。
- **4. brain-alpha-robustness**（100 行）：提交前稳健性/归因审计，质量高（Phase A–D + 决策表）。→ 四关审计与 `wq-backtest-monitor`/`worldquant-submit-alpha` 互引去重。
- **5. alpha-template-labs-data-analysis**（100 行）：Brain Labs 原始数据分析。⚠️ 引用 `mcp__wqb-mcp__*` 工具名，但本机常驻 MCP 为 `world-quant-brain-mcp`（端口 8876），命名空间实际可能为 `mcp__wq-brain__*`，**不匹配会失效**。→ 核对并统一 MCP 工具命名空间。

**【用户级 · WQ 挖掘栈】**
- **6. wq-brain-ppa-mining**（266 行）★ 重点整改：PPA 完整工作流，与工作区 5 个 skill 高度重叠（MCP 版重述）。frontmatter 用 `title:` 非 `name:`；自带 `dataset_health_check.py` 与 `eur_field_coverage.py` 双副本；§8/§9.1 硬编码倍率/universe 表会漂移；含大量"修订/作废"历史叙述。→ ① 改 `name:`；② 注明"与 brain-alpha-* 互补而非替代"；③ 双脚本二选一（建议保留 `tools/` 下并改引用）；④ §8/§9.1 改运行时拉取；⑤ 历史叙述收 `changelog.md`；⑥ 删 `__pycache__/`。
- **7. wq-backtest-monitor**（145 行）：监控/盘点/四关审计/并发。⚠️ 引用 `worldquant_alpha/deliverables/tools/*` 等**全部死链（项目不存在）**，报告生成工具实际不可用；§6 令牌桶与 `wqb-concurrency` 重复。→ 报告工具迁到 `wqb/tools/`；并发章节与 `wqb-concurrency` 合并；四关审计互引。
- **8. worldquant-submit-alpha**（97 行）：真正提交 alpha（PATCH→POST→轮询），质量高。⚠️ 引用 `worldquant_alpha/.env`、`wd_lib_wrapper.py`、`wd_lib/api/alphas.py` 等**死链**（`wd_lib_wrapper` 是提交核心依赖，缺失则无法独立运行）；Python 环境假设过时（vnpystudio，违反运行时隔离）。→ 明确 `wd_lib_wrapper` 来源；改托管 venv；与 monitor 提交审计互引。
- **9. wqb-concurrency**（74 行）：测定并发上限 C + 信号量包整条 run_backtest。frontmatter 用 `title:`（不一致）；引用 `worldquant_alpha/diag_concurrency.py` 死链；与 monitor §6 重复并发知识。→ 与 monitor 并发章节合并；统一 frontmatter。

**【通用 / 独立（全部 disable）】**
- **10. code-optimization**（143 行）：扫描 Python 冗余重构，自洽。假设 Flask+DDD 项目，与本 WQ 无关，是孤儿。→ 注明适用范围；`_user_meta.json` 合并进 frontmatter。
- **11. dead-code-cleanup**（185 行）★ 文档范本：死代码清理（5 阶段 + 红线），质量最佳，可作其他 skill 范本。仅 `metadata:` 块写法不一致。
- **12. gold-analysis**（307 行）：黄金走势分析，与本 WQ 无关。`gold-analysis --full` 未绑定本地脚本，无实际工具交付；`_meta.json`+`_skillhub_meta.json` 双份。→ 合并元数据；或删除；金十数据源可与 `jin10-news` 合并为"金融数据源" skill。
- **13. jin10-news**（66 行）★ 最不规范：frontmatter **无 `name`/`title`，仅 `disable: true`**；引用 `/root/.openclaw/workspace/scripts/...`（Linux 路径，Windows 错误）；x-token "参考 TOOLS.md" 未随附。→ 补 `name`/`description`；修正路径；废弃则删除。

---

## 三、优先级整改路线图

### P0（立即，阻断可用性）
1. **修复 `worldquant_alpha` 死链**：把依赖的工具迁移到 `wqb/tools/` 并改引用，或在 frontmatter 显式标注"依赖外部 `worldquant_alpha` 项目（本机未安装）"。
2. **`jin10-news` 补 frontmatter + 修路径**（或删除）。
3. **工作区 skill 三重复制**：确立单一真相源（建议 `.workbuddy/skills/` 为权威），`.zcode/`、`wqb-share-03/.trae/` 改为 symlink 或删除副本。

### P1（重要，一致性与去重）
4. **统一 frontmatter schema**：全部用 `name:`（kebab-slug = 目录名）；`wq-brain-ppa-mining`、`wqb-concurrency` 改 `title:`→`name:`；`jin10-news` 补 `name:`。
5. **双轨 WQ 栈去重**：明确 `brain-alpha-*`（CLI 重栈）与 `wq-brain-ppa-mining`（MCP 轻栈）互补，通用知识抽到共享 reference。
6. **提交职责收敛**：四关审计只在一处写权威版，其余互引。
7. **并发知识合并**：`wqb-concurrency` 与 `wq-backtest-monitor` §6 合并。
8. **统一双脚本**：`dataset_health_check.py` vs `eur_field_coverage.py` 二选一。
9. **长 SKILL.md 重构**：orchestrator/research 的"日期追加"步骤抽 `changelog.md`。

### P2（打磨）
10. 删 `wq-brain-ppa-mining/scripts/__pycache__/`。
11. 合并冗余元数据（`_meta.json`+`_skillhub_meta.json` → frontmatter）。
12. `wq-brain-ppa-mining` §8/§9.1 硬编码表改为运行时拉取。
13. 4 个 disable 通用 skill：标注适用范围（code-optimization/dead-code-cleanup 可保留为范本）或清理（gold-analysis/jin10-news 视使用频率）。

---

## 四、一句话总结

现有的 WQ 挖掘知识**分散在 9 个 skill（工作区 5 + 用户级 4）且双份维护**，其中 3 个用户级 skill 依赖一个**整机不存在的 `worldquant_alpha` 项目**而不可用；工作区 5 个 skill 又在 **3 个目录三重复制**。优先做三件事：**修死链、立单一真相源、统一 frontmatter 与去重**——这比继续往 skill 里追加日期段落收益大得多。
