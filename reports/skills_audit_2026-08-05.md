# 项目 Skills 盘点与优化审计

> 审计日期：2026-08-05 ｜ 审计范围：当前项目 `wqb` 的全部 13 个 skill
> 数据依据：逐文件读取 13 个 `SKILL.md` + 实际路径探测（`worldquant_alpha` / `src/wqb` / `reference/` / `deliverables/` / 各 skill 脚本是否真实存在）

---

## 〇、总览：13 个 skill，三大阵营

| # | Skill（目录名） | 位置 | 行数 | 状态 | 领域 | frontmatter 键 |
|---|---|---|---|---|---|---|
| 1 | brain-alpha-orchestrator | 工作区 | 46 | 启用 | WQ 挖掘·编排 | `name` |
| 2 | brain-alpha-research | 工作区 | 52 | 启用 | WQ 挖掘·研究 | `name` |
| 3 | brain-alpha-repair | 工作区 | 43 | 启用 | WQ 挖掘·修复 | `name` |
| 4 | brain-alpha-robustness | 工作区 | 100 | 启用 | WQ 挖掘·稳健性 | `name` |
| 5 | alpha-template-labs-data-analysis | 工作区 | 100 | 启用 | WQ 挖掘·Labs 数据 | `name` |
| 6 | wq-brain-ppa-mining | 用户级 | 266 | 启用 | WQ 挖掘·PPA 方法论 | **`title`** |
| 7 | wq-backtest-monitor | 用户级 | 145 | 启用 | WQ 挖掘·监控/审计 | `name` |
| 8 | worldquant-submit-alpha | 用户级 | 97 | 启用 | WQ 挖掘·提交 | `name` |
| 9 | wqb-concurrency | 用户级 | 74 | 启用 | WQ 挖掘·并发调优 | **`title`** |
| 10 | code-optimization | 用户级 | 143 | **disable** | 通用·代码冗余 | `name` |
| 11 | dead-code-cleanup | 用户级 | 185 | **disable** | 通用·死代码 | `metadata` 块 |
| 12 | gold-analysis | 用户级 | 307 | **disable** | 通用·黄金分析 | `metadata` 块 |
| 13 | jin10-news | 用户级 | 66 | **disable** | 通用·金十快讯 | **无 name/title** |

**结论性发现（先讲最重要的）**：

- **WQ 挖掘知识被两套 skill 栈重复维护**：① 工作区 5 个（`brain-alpha-*` + labs），强依赖 `src/wqb` Python 包 + `wqb` CLI + `reference/*.md`；② 用户级 `wq-brain-ppa-mining`，是同一套知识的 "MCP 轻量版重述"。两者重叠度高、各维护一份，极易漂移。
- **`worldquant_alpha/` 项目在整机不存在**（全盘 `find` 无结果）。用户级栈里 `wq-backtest-monitor`、`worldquant-submit-alpha`、`wqb-concurrency` 引用的 `worldquant_alpha/deliverables/tools/*`、`wd_lib_wrapper.py`、`worldquant_alpha/.env`、各类脚本**全部是死链**。
- **工作区 5 个 `brain-alpha-*` skill 在 3 个目录三重复制**：`.workbuddy/skills/`、`.zcode/skills/`、`wqb-share-03/.trae/skills/`。改一处不会同步，是最大的可维护性隐患。
- **4 个通用 skill 全部 `disable`，且引用本机不存在的路径/项目**（`/root/.openclaw/...`、Flask-DDD 项目、黄金数据源），在本 WQ 项目中是孤儿。

---

## 一、跨 skill 的系统性问题（最高优先级）

### 1.1 双轨 WQ 挖掘栈 → 知识双份维护
工作区 5 个 skill（数据集选择/中性化/闸门/WebDataScope 预筛/算子审计）与用户级 `wq-brain-ppa-mining`（同名主题、同套闸门、同套 API 约束、同套 WebDataScope 预筛）高度重叠。同一段 "IS_LADDER 阈值严格 >1.58 / prod_corr<0.7 / coverage≥0.85" 在两边各写一遍。

### 1.2 `worldquant_alpha/` 全局死链（阻断可用性）
`wq-backtest-monitor` §8/§12/§13 引用的 `worldquant_alpha/deliverables/tools/{build_md_report,gen_report,lint_submit_gate,probe_concurrency,build_html_report}.py`、`deliverables/templates/standard_backtest_report_template.md`、`deliverables/framework/wq_backtest_monitor_framework.md`；`worldquant-submit-alpha` 引用的 `worldquant_alpha/.env`、`wd_lib_wrapper.py`、`wd_lib/api/alphas.py`、`results/gen_pass_cheap_list.py`；`wqb-concurrency` 引用的 `worldquant_alpha/diag_concurrency.py` —— **全部 MISS**。

### 1.3 工作区 skill 三重复制（`.workbuddy` / `.zcode` / `wqb-share-03`）
`brain-alpha-research`、`brain-alpha-orchestrator` 等 5 个在 3 处各有一份完整副本（含 `references/`）。无单一真相源（single source of truth），编辑会分裂。

### 1.4 提交职责被 3 个 skill 分散覆盖
"提交 alpha + 四关审计" 在 `worldquant-submit-alpha`（整篇）、`wq-backtest-monitor` §5/§10（四关层级 + 逐候选审计）、`brain-alpha-orchestrator` §14（预提交稳健性门）各写一份，口径各自为政。

### 1.5 并发/令牌桶知识重复
`wqb-concurrency`（整篇）与 `wq-backtest-monitor` §6（Token-Bucket C=7）讲的是同一件事。

### 1.6 数据集体检脚本双副本
`wq-brain-ppa-mining/scripts/dataset_health_check.py`（20490 B）与 `wqb/tools/eur_field_coverage.py` 是同源近重复脚本，维护两份。

### 1.7 frontmatter schema 不统一
- 部分用 `name:`（kebab-slug，与目录同名），部分用 `title:`（`wq-brain-ppa-mining`、`wqb-concurrency`），`jin10-news` **完全没有 name/title**（仅有 `disable: true`）。
- 目录名 vs frontmatter 不一致：`wq-brain-ppa-mining` 的 `title` 是 "WQ Brain PPA Alpha 挖掘方法论 (WebDataScope 增强版)"；`wqb-concurrency` 的 `title` 是 "WQ Brain 并发挖掘调优"。

### 1.8 长 SKILL.md 用"日期追加"累积，流程即补丁日志
工作区 `orchestrator` 步骤编号 `14→14a→15→15a~15e→16→17→18→18a→19`；`research` 步骤 `14→14a~14e→15→15a~15e→16`，每步都是 "2026-04-21/07-29/08-02/08-04/08-05 新增"。正文是时间线补丁而非稳定程序，新人难读、易自相矛盾。

### 1.9 硬编码平台数据会漂移
`wq-brain-ppa-mining` §8（区域实证：倍率/中性化/数据集表）+ §9.1（各 region universe 全表）全部硬编码，而平台 `get_platform_setting_options` 可运行时拉取。硬编码必过期（该 skill 自己多处标注"实测/已作废"）。

### 1.10 冗余元数据文件
`gold-analysis`、`jin10-news` 同时含 `_meta.json` 与 `_skillhub_meta.json`（双份）；`code-optimization` 含 `_user_meta.json`；这些与 frontmatter 信息重叠。

### 1.11 提交了 `.pyc`
`wq-brain-ppa-mining/scripts/__pycache__/` 已提交进 skill 目录，应 gitignore/删除。

---

## 二、逐 skill 审计（命名 / 职责单一性 / 复用性 / 配置冗余 / 文档完整性 / 依赖合理性 / 可维护性 + 改进点）

### 【工作区级栈】

#### 1. brain-alpha-orchestrator（46 行 / 5 个 reference）
- **命名**：规范（slug = 目录名）。
- **职责单一性**：作为"编排者"宽泛是预期的，但 19 步里塞了数据集选择、中性化遍历、新闻 6 桶框架、假设挖掘、算子审计、WebDataScope 预筛、PPA 主题匹配、表达式硬门——几乎全靠 "去读 reference/*.md"，自身是薄壳。可接受，但应点明 "本 skill 是路由层"。
- **复用性**：重依赖 `reference/` 文档与 `src/wqb` 包，复用率高。
- **配置冗余**：无自身配置；依赖运行时 `config.py`。
- **文档完整性**：正文短；长步骤（如 18a PPA 主题、19 硬门）非常长且易过期。
- **依赖合理性**：依赖 `wqb` CLI（`plan`/`doctor`/`operator-audit`/`research`/`settings`/`validate-session-pack`/`prepare-session-pack`/`news-refresh-portfolio`）——**已实测这些命令确实存在于 `src/wqb/cli.py``**，依赖有效，但**未在 frontmatter 声明 `requires`**。
- **可维护性**：步骤编号是追加日志，建议拆出 `changelog.md`，主流程稳定化。
- **改进**：① frontmatter 加 `requires: [src/wqb CLI, reference/*.md]`；② 超长步骤外置子文件；③ 与 `wq-brain-ppa-mining` 明确分工（CLI 重栈 vs MCP 轻栈），避免双份维护。

#### 2. brain-alpha-research（52 行 / 7 个 reference）
- **命名**：规范。
- **职责单一性**：数据集/字段/设置研究 + 论坛模板挖掘 + WebDataScope 预筛，偏宽但尚属"研究"范畴。
- **复用性**：大量复用 `references/{webdatascope-data-quality,forum-template-library,backtest-experience-archive,asi-methodology,jump-decay-methodology,news_sentiment_playbook}.md`。
- **配置冗余**：WebDataScope 规则（8–23）与 `orchestrator` §17/§18 重复；`tools/webdata_quality.py` 路径用 `../../../tools/...` 需核对是否对应 `wqb/tools/`。
- **文档完整性**：步骤 15 单步极长（WebDataScope 全维预筛），内容已远超合理长度。
- **依赖合理性**：重依赖 `src/wqb/research/*`、`expression/*`（已实测存在）。
- **可维护性**：同 orchestrator 的"日期追加"问题（14/14a–14e/15/15a–15e/16），且为全栈最长。
- **改进**：把 WebDataScope 预筛规则抽到单一 `reference/webdatascope-data-quality.md`（已存在本地副本），orchestrator 与 research 共用，删除双份；正文拆为"研究任务清单 + 外部索引"。

#### 3. brain-alpha-repair（43 行 / 1 个 reference）
- **命名**：规范。
- **职责单一性**：修复候选（降换手/提覆盖/降相关/轨迹恢复），聚焦，与 robustness "诊断 vs 修复" 边界清晰。
- **复用性**：引用 orchestrator 的 `webdatascope-failed-gates.md`。
- **文档完整性**：step 2 的"5 轴旋转 + 6 武器"表较长，建议外置（已部分在 `references/repair-order.md`）。
- **依赖合理性**：合理。
- **可维护性**：较好（正文短）。
- **改进**：去重与 orchestrator/robustness 的相关性内容；保持 repair-order.md 单一来源。

#### 4. brain-alpha-robustness（100 行 / 1 个 reference）
- **命名**：规范。
- **职责单一性**：提交前稳健性/归因审计，聚焦，质量高（Phase A–D + 决策表完整）。
- **复用性**：引用 orchestrator 的 `webdatascope-failed-gates.md`；与 repair 衔接已写明。
- **文档完整性**：很完整。
- **依赖合理性**：依赖 MCP 论坛/平台工具，合理。
- **可维护性**：较好。
- **改进**：与 `wq-backtest-monitor` §5/§10 的"四关审计"互引而非各写；与 `worldquant-submit-alpha` 的硬闸门口径对齐。

#### 5. alpha-template-labs-data-analysis（100 行）
- **命名**：长但 kebab-slug 规范。
- **职责单一性**：Brain Labs 原始数据分析（提交前），聚焦。
- **文档完整性**：硬规则引用 orchestrator §19（`check_expr_against_inspect`）——跨 skill 耦合。
- **依赖合理性**：⚠️ 引用 `mcp__wqb-mcp__*` 工具名，但本机常驻 MCP 服务为 `world-quant-brain-mcp`（端口 8876），工具前缀实际可能是 `mcp__wq-brain__*`。**工具命名空间若不匹配会失效**，需核对。
- **可维护性**：OK。
- **改进**：核对并统一 MCP 工具命名空间；显式声明对 orchestrator §19 的依赖。

### 【用户级 · WQ 挖掘栈】

#### 6. wq-brain-ppa-mining（266 行）★ 重点整改对象
- **命名**：目录名规范，但 frontmatter 用 **`title:`** 而非 `name:`，且 title 与目录不一致（应为 `name: wq-brain-ppa-mining`）。
- **职责单一性**：PPA 挖掘完整工作流——与**工作区 5 个 skill 高度重叠**，是 "MCP 版重述"。
- **复用性**：自带 `scripts/dataset_health_check.py`（与 `wqb/tools/eur_field_coverage.py` 双副本）；引用 `tools/webdata_quality.py`、`tools/eur_field_coverage.py`、常驻 MCP。
- **配置冗余**：§8 区域实证（硬编码倍率/中性化/数据集）+ §9.1 universe 全表 **全部硬编码**，会漂移；与 research skill 的 WebDataScope 知识重复。
- **文档完整性**：很完整，但含大量 "2026-08-05 修订/作废" 历史叙述，干扰主线。
- **依赖合理性**：依赖 MCP 常驻（合理）；`WQB_WORKSPACE` 探测 + 双脚本副本是冗余。
- **可维护性**：中——改动需同步工作区栈对应知识（双份维护）。
- **改进（P0/P1）**：
  1. frontmatter 改用 `name:`，与目录一致。
  2. 与工作区栈明确分工：本 skill = "MCP 轻量版"，frontmatter 注明"与 brain-alpha-* 互补而非替代"，通用知识抽到共享 reference。
  3. 删除/统一双脚本（`dataset_health_check.py` 与 `eur_field_coverage.py` 二选一，建议保留 `tools/` 下那份并改引用）。
  4. §8/§9.1 硬编码表改为运行时拉取（`get_platform_setting_options` / 体检工具），去掉漂移源。
  5. 历史修订叙述收进 `changelog.md`。
  6. 删除 `scripts/__pycache__/`。

#### 7. wq-backtest-monitor（145 行）
- **命名**：规范。
- **职责单一性**：监控/盘点/效率/四关审计/并发模型/报告——多职责但围绕"监控"内聚尚可。
- **复用性**：⚠️ 引用 `worldquant_alpha/deliverables/tools/*`、`templates/*`、`framework/*` —— **全部死链（项目不存在）**，报告生成工具实际不可用。
- **配置冗余**：§6 令牌桶与 `wqb-concurrency` 重复。
- **文档完整性**：很完整（13 节），但工具引用失效。
- **依赖合理性**：重依赖不存在的 `worldquant_alpha` 工具 → 实际不可执行报告生成。
- **可维护性**：死链是硬伤。
- **改进**：① 把报告工具真实位置改到 `wqb/tools/`（现有 `mine_eur_mlfactor.py`/`mlfp_gate.py`/`mcp_py`）或移植并改引用；② 并发章节与 `wqb-concurrency` 合并；③ 四关审计与 `worldquant-submit-alpha`/`brain-alpha-robustness` 互引。

#### 8. worldquant-submit-alpha（97 行）
- **命名**：规范（slug）。
- **职责单一性**：真正提交 alpha（PATCH description → POST submit → 轮询），聚焦，质量高（坑位列举详尽）。
- **复用性**：⚠️ 引用 `worldquant_alpha/.env`、`wd_lib_wrapper.py`、`wd_lib/api/alphas.py`、`results/gen_pass_cheap_list.py` —— **死链**（`wd_lib_wrapper` 是提交核心依赖，缺失则本 skill 无法独立运行）。
- **文档完整性**：非常完整。
- **依赖合理性**：写 "运行环境用 `D:\softwares\vnpystudio\python.exe`（managed python 缺 requests）" —— 过时：可在托管 venv 安装 `requests`，且违反运行时隔离规则。
- **可维护性**：内容好，但环境假设过时 + 依赖死链。
- **改进**：① 明确 `wd_lib_wrapper` 来源（迁移到 `wqb/tools` 或说明）；② Python 环境改托管 venv；③ 与 monitor §5/§10 提交审计互引去重。

#### 9. wqb-concurrency（74 行）
- **命名**：目录名规范，但 frontmatter 用 **`title:`**（不一致）。
- **职责单一性**：测定并发上限 C + 信号量包整条 run_backtest + 孤儿模拟，聚焦。
- **复用性**：引用 `worldquant_alpha/diag_concurrency.py`、`wd_lib_wrapper.py`（死链）；与 monitor §6 重复并发知识。
- **文档完整性**：完整（含诊断表）。
- **依赖合理性**：知识本身可独立，代码引用次要。
- **可维护性**：中等。
- **改进**：① 与 monitor 并发章节合并；② 统一 frontmatter schema；③ 标注 `wd_lib_wrapper` 来源。

### 【通用 / 独立（全部 disable）】

#### 10. code-optimization（143 行 / disable）
- **命名**：规范。
- **职责单一性**：扫描 Python 冗余并重构，聚焦。
- **复用性**：自带 `scripts/scan_redundancy.py` + `references/redundancy_patterns.md`，自洽。
- **依赖合理性**：假设 Flask+DDD 项目（`shared/`、`api_success()`），**与本 WQ 项目无关**，是孤儿（disable）。
- **文档完整性**：完整；引用 `docs/biz/REDUNDANCY_ANALYSIS_REPORT.md`（特定项目路径）。
- **改进**：保留但注明适用范围；`_user_meta.json` 合并进 frontmatter。

#### 11. dead-code-cleanup（185 行 / disable）★ 文档范本
- **命名**：规范。
- **职责单一性**：死代码清理（5 阶段 + 红线），聚焦，质量最佳。
- **复用性**：独立（依赖 autoflake/vulture/pyflakes/eradicate，走托管 venv）。
- **依赖合理性**：通用，无项目特定，OK。
- **文档完整性**：非常完整、可操作性强，可作其他 skill 的文档范本。
- **改进**：仅 `metadata:` 块写法与其他 skill 顶层字段不一致，建议统一；其余无需大改。

#### 12. gold-analysis（307 行 / disable）
- **命名**：规范。
- **职责单一性**：黄金走势分析，聚焦（但与本 WQ 项目无关）。
- **复用性**：引用大量外部数据源（金十/Kitco/Bloomberg/CFTC），**但 `gold-analysis --full` 命令未绑定任何本地脚本**，无实际工具交付。
- **文档完整性**：极完整（框架详尽），但方法论孤本、无脚本配套。
- **配置冗余**：`_meta.json` + `_skillhub_meta.json` 双份元数据。
- **改进**：合并双元数据；若不再使用考虑删除；其金十数据源可与 `jin10-news` 合并为"金融数据源" skill。

#### 13. jin10-news（66 行 / disable）★ 最不规范
- **命名**：⚠️ **frontmatter 无 `name`/`title`，仅 `disable: true`** —— 命名规范缺失。
- **职责单一性**：金十快讯获取/分析，聚焦。
- **复用性**：引用 `/root/.openclaw/workspace/scripts/...`（**Linux root 路径，在 Windows 环境错误**）；x-token "参考 TOOLS.md"（未随附）。
- **文档完整性**：中等。
- **依赖合理性**：路径与环境全错（Linux vs Windows），脚本不在本项目。
- **可维护性**：差（孤儿 + 路径错误 + 缺 frontmatter）。
- **改进**：① 补全 `name`/`description` frontmatter；② 修正脚本路径到本项目（或提供脚本）；③ 若废弃则删除。

---

## 三、优先级整改路线图

### P0（立即，阻断可用性）
1. **修复 `worldquant_alpha` 死链**：`wq-backtest-monitor`、`worldquant-submit-alpha`、`wqb-concurrency` 的脚本/工具引用全部失效。→ 把依赖的工具迁移到 `wqb/tools/` 并改引用，或在 frontmatter 显式标注 "依赖外部 `worldquant_alpha` 项目（本机未安装）"。
2. **`jin10-news` 补 frontmatter + 修路径**（或删除）。
3. **工作区 skill 三重复制**：确立单一真相源（建议 `.workbuddy/skills/` 为权威），`.zcode/`、`wqb-share-03/.trae/` 改为 symlink 或删除副本。

### P1（重要，一致性与去重）
4. **统一 frontmatter schema**：全部用 `name:`（kebab-slug = 目录名）；`wq-brain-ppa-mining`、`wqb-concurrency` 改 `title:` → `name:`；`jin10-news` 补 `name:`。
5. **双轨 WQ 栈去重**：明确 `brain-alpha-*`（CLI 重栈）与 `wq-brain-ppa-mining`（MCP 轻栈）的互补关系，通用知识（闸门/universe/API 约束/WebDataScope 预筛）抽到共享 reference，两边引用。
6. **提交职责收敛**：四关审计只在一处写权威版，`worldquant-submit-alpha` / `wq-backtest-monitor` §5/§10 §10 / `brain-alpha-orchestrator` §14 互引。
7. **并发知识合并**：`wqb-concurrency` 与 `wq-backtest-monitor` §6 合并。
8. **统一双脚本**：`dataset_health_check.py` vs `eur_field_coverage.py` 二选一。
9. **长 SKILL.md 重构**：orchestrator/research 的"日期追加"步骤抽 `changelog.md`，主流程稳定化。

### P2（打磨）
10. 删 `wq-brain-ppa-mining/scripts/__pycache__/`。
11. 合并冗余元数据（`_meta.json`+`_skillhub_meta.json` → frontmatter）。
12. `wq-brain-ppa-mining` §8/§9.1 硬编码表改为运行时拉取。
13. 4 个 disable 通用 skill：标注适用范围（code-optimization/dead-code-cleanup 可保留为范本）或清理（gold-analysis/jin10-news 视使用频率）。

---

## 四、一句话总结
现有的 WQ 挖掘知识**分散在 9 个 skill（工作区 5 + 用户级 4）且双份维护**，其中 3 个用户级 skill 依赖一个**整机不存在的 `worldquant_alpha` 项目**而不可用；工作区 5 个 skill 又在 **3 个目录三重复制**。优先做三件事：**修死链、立单一真相源、统一 frontmatter 与去重**——这比继续往 skill 里追加日期段落收益大得多。
