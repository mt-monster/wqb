# reports/ 目录索引（INDEX）

> 整理时间：2026-08-13 ｜ 整理动作：归类子目录 + 合并去重 + 精简 + 本索引生成。
> 整理前：13 个文件散落在 `reports/` 根目录；整理后：6 个子目录 + 本索引，文件按主题归组。
>
> **2026-08-23 更新**：9 份互相矛盾的 skills 审计（reports/ 6 份 + project-audit/ 1 份 + research-data/ 2 份）
> 合并为唯一现行版本 `skills_review_2026-08-23.md`，原件归档 `attic/reports_archive/2026-08-23-superseded/`。
> 后续 skills 审计**只更新该文件，不再新建报告**。

---

## 一、目录结构

```
reports/
├── 00-INDEX.md                          ← 本文件（索引 + 摘要 + 归类依据）
├── skills_review_2026-08-23.md          ← 【skills 审计】现行唯一版本（评估结论 + 整改记录）
│
├── forum-experience/                    ← 【论坛经验】WQ BRAIN 社区高赞实战帖系统总结
│   ├── ppa_forum_experience_2026-08-07.md     (PPA 挖掘经验总纲，已并入提交闸门专题)
│   ├── glb_forum_experience_2026-08-05.md     (GLB 区域挖掘经验)
│   └── alpha_templates_forum_2026-08-05.md    (论坛 Alpha 模板库 T1–T15)
│
├── eur-mining/                          ← 【EUR 区域挖掘】三份原始报告合并为 1
│   └── eur_mining_report.md                   (覆盖率核查 + 数据集选型 + 模板全量验证)
│
├── alpha-optimization-report/           ← 【Alpha 优化报告】自包含可视化报告（保持不动）
│   ├── alpha-optimization-report.html
│   ├── assets/charts.js
│   └── _shared/js/echarts.min.js              (第三方依赖，删则报告失效)
│
├── tooling-research/                    ← 【工具/数据源研究】
│   └── WebDataScope_alpha挖掘用法研究报告.html
│
├── project-audit/                       ← 【项目审计】
│   └── skills_audit_2026-08-05.md             (13 个 skill 盘点与整改路线图)
│
└── archive/                             ← 【历史快照/过期监控】
    └── mining_progress_2026-08-05_2230.md     (半小时报自动化触发的一次性快照)
```

---

## 二、各文件摘要与归类依据

### forum-experience/ppa_forum_experience_2026-08-07.md
- **原路径**：`reports/ppa_forum_experience_2026-08-07.md`
- **归类依据**：PPA（Power Pool Alpha）挖掘的社区经验总纲，属"论坛经验"主题。
- **内容摘要**：327 条检索 → 精读 42 篇高赞帖。涵盖 PPA 机制本质、信号/因子构建（ATOM 纯净信号、模板体系、操作符实战）、数据处理（中性化/降相关/时间窗）、硬闸门（prodCorr<0.7 / PP 相关≤0.5）、本地预估剪枝、主题加成与 Base 收益、组合管理、实战踩坑与工程化提速。
- **关键结论**：① 低生产相关性（ProdCorr）是最宝贵资产；② PP 相关性 >0.5 时系统会"借用" prodCorr 名义 FAIL（§1.2）；③ 我们 42 个 GLB emotion 候选全灭正是高 PC=拥挤的铁律印证；④ 换壳（换信号方向/数据）比磨参数有效。
- **本次变更**：并入 `ppa_submission_lessons` 的独有内容（见下"合并去重"），新增 §1.5「提交闸门专项」；§9 去重（去掉与 §6.4 重复的"换壳"表述）。

### forum-experience/glb_forum_experience_2026-08-05.md
- **原路径**：`reports/glb_forum_experience_2026-08-05.md`
- **归类依据**：GLB（Global 全球区域）因子挖掘的社区经验，属"论坛经验"主题。
- **内容摘要**：160 条命中 → 精读 22 篇。GLB 区域特性速览、因子构建（ATOM 单字段/行业中性化残差/反转+收益率/SuperAlpha）、数据处理流程、特征工程（降 TVR 工具箱/升 Sharpe/降 PC/换壳）、回测验证（廉价闸门/IS-Ladder 阈值/硬闸门/提交基线）、实战踩坑与数据集推荐。
- **关键结论**：GLB 回测慢需低流动性数据集 + multi-sim；只做 INDUSTRY 中性化会暴露 country bias；family prod 长期卡窄区间 = crowded，尽早换壳；附 22 篇帖子清单与可复用表达式。

### forum-experience/alpha_templates_forum_2026-08-05.md
- **原路径**：`reports/alpha_templates_forum_2026-08-05.md`
- **归类依据**：论坛 Alpha 模板合集（T1–T15），属"论坛经验"主题中的"模板库"子类。
- **内容摘要**：论坛 50 帖 + 官方入门示例抽取的 15 个可落地模板，按族分组（反转/动量、估值、差异/期限结构、信息论、情绪），每模板含作者/表达式/逻辑/泛化要点；附通用模板骨架、参数优化（爬山→帕累托）、模板族速查表、EUR 挖掘建议。
- **关键结论**：差异/期限结构族（T10）与反转族（T1/T2）算子少、字段少、PC 易低，最易过 Power Pool 闸门；`ml_factor_proj` 的 `active_return` 10 窗口天然适配 T10。

### eur-mining/eur_mining_report.md
- **原路径（三份合并）**：`reports/eur_field_coverage_2026-08-05.md` + `reports/eur_ppa_mining_2026-08-05.md` + `reports/eur_template_validation_2026-08-05.md`
- **归类依据**：三份均围绕 EUR 区域 `ml_factor_proj` 数据集的 PPA 挖掘（覆盖率核查→选型→模板验证），是同一战役的连续三段，合并为单一完整报告。
- **内容摘要**：① 撤回"EUR 死路"旧判断（根因是数据集选错，非无数据）；② EUR 平台实况与 4 个劣质数据集体检；③ EUR 未开发机会排行（19 个高覆盖低拥挤数据集，ml_factor_proj 满分零竞争）；④ KOR 优先级高于 EUR；⑤ ml_factor_proj 选型依据与字段结构；⑥ 论坛 14 模板全量验证（T10v_12_1 Sharpe 1.14 唯一过 PP 闸）；⑦ 操作教训（fatal operator 级联 CANCEL / 瞬态故障 / ts_entropy 不可用）；⑧ 工具与行动建议。
- **关键数据**：EUR 178 数据集/38609 字段；ml_factor_proj coverage 1.0/333 字段/alphaCount 0/倍率 1.5；T10v_12_1 Sharpe 1.14、Fit 0.61、TVR 16.1%、回撤 7.0%、2 算子 2 字段。

### alpha-optimization-report/alpha-optimization-report.html
- **原路径**：`reports/alpha-optimization-report/`（子目录，本次未动）
- **归类依据**：Alpha 优化专题的可视化报告，自包含（HTML + `assets/charts.js` + `_shared/js/echarts.min.js` 第三方依赖）。
- **内容摘要**：Alpha 优化过程的交互式图表报告（940 行 HTML + ECharts 渲染）。
- **处理说明**：保持原样不动；`echarts.min.js` 为第三方库，删除会导致报告失效，故保留。

### tooling-research/WebDataScope_alpha挖掘用法研究报告.html
- **原路径**：`reports/WebDataScope_alpha挖掘用法研究报告.html`
- **归类依据**：WebDataScope 工具/数据源的用法研究，属"工具/数据源研究"主题。
- **内容摘要**：WebDataScope 在 Alpha 挖掘中的用法研究报告（HTML 格式）。

### project-audit/skills_audit_2026-08-05.md
- **原路径**：`reports/skills_audit_2026-08-05.md`
- **归类依据**：对项目全部 13 个 skill 的盘点审计，属"项目审计"主题。
- **内容摘要**：13 个 skill 总览（三大阵营）、系统性问题（双轨栈重复维护 / `worldquant_alpha` 死链 / 三重复制 / 提交职责分散 / 并发知识重复 / frontmatter 不统一 / 硬编码漂移等 11 项）、逐 skill 审计、P0/P1/P2 整改路线图。
- **本次变更**：精简——删除逐 skill 的"命名/职责/复用/配置/文档/依赖/可维护"七维填充性文字（"规范/OK"类），保留全部关键发现（死链、MCP 命名空间不匹配、硬编码漂移、disable 孤儿）与整改路线图；约 230→150 行。

### archive/mining_progress_2026-08-05_2230.md
- **原路径**：`reports/mining_progress_2026-08-05_2230.md`
- **归类依据**：半小时报自动化触发的**一次性进程监控快照**，属"历史快照/过期监控"，归入 archive 不再作为活跃报告。
- **内容摘要**：某次半小时报的 Python 进程盘点（MCP-SVC / SCAN / WATCHDOG 视角）+ 回测效率结论。

---

## 三、合并去重说明

| 合并动作 | 并入方（保留） | 被合并方（删除） | 保留的关键信息 |
|---|---|---|---|
| EUR 三报告合一 | `eur-mining/eur_mining_report.md` | `eur_field_coverage_2026-08-05.md`、`eur_ppa_mining_2026-08-05.md`、`eur_template_validation_2026-08-05.md` | 全部覆盖率结论、机会排行表、T10 验证全表、操作教训、行动建议 |
| PPA 提交经验并入 | `forum-experience/ppa_forum_experience_2026-08-07.md`（§1.5） | `ppa_submission_lessons_2026-08-05.md` | 轮动区域主题闸门（帖 JY35270/SF94303）、铃铛通知（MY22315/KJ42842）、6 条教训、**⚠️ MCP submit_alpha 只认常规闸门（Sharpe<1.3 无法提交 PPA）**、T10v_12_1(A1G6QpOQ) 修正结论、具体帖子 ID（SL49683/JY35270/MY22315/FD69320/XW90844/QQ68782） |

---

## 四、精简说明

- **`skills_audit_2026-08-05.md`**：逐 skill 七维分析中大量"规范/OK"填充文字压缩为"角色 + 关键问题/改进"，保留全部死链、MCP 命名空间不匹配、硬编码漂移、disable 孤儿等结论与 P0/P1/P2 路线图（约 230→150 行）。
- **`ppa_forum_experience_2026-08-07.md`**：§9 去掉与 §6.4 重复的"换壳"表述，保留 42 个 GLB 候选的独有印证。
- **保留未精简**：`glb_forum_experience`（结构紧凑、数据完整）、`alpha_templates_forum`（T1–T15 表达式为核心价值，删则失模板）、`alpha-optimization-report`（自包含可视化，内含第三方依赖）。

---

## 五、安全声明

- 所有合并/精简均**只去重、不丢关键数据**：数值结论、帖子 ID、闸门阈值、候选代号（T10v_12_1 / A1G6QpOQ / qMNZX1o1 等）、数据集指标（ml_factor_proj coverage 1.0 等）原样保留。
- 移动用 `git mv`、删除用 `git rm`、合并新版用 `git add`，保留版本库历史可追溯。
- `archive/` 仅作归类存放，原文件内容未改动。
