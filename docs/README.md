# WQB 知识库索引

> 本目录是 WorldQuant BRAIN Alpha 挖掘项目的结构化知识库。
> 最后整理：2026-08-31。维护规则：新增文档归入对应子目录，并更新本索引。

---

## 目录结构

```
docs/
├── README.md                              ← 本文件（索引与导航）
├── experience/                            ← 经验总结类
│   ├── project_experience_master.md         项目经验总纲（10章，325行）
│   ├── wq_alpha_mining_knowledge_base.md    挖掘方法知识库（10章，374行）
│   └── region_template_kb.md                区域/模板知识库使用协议（内容在 DB ledger_kv）
├── reference/                             ← 参考速查类
│   ├── operators_notes.md                   WQ BRAIN 全算子速查表（87条）
│   ├── community_tpl_library_sequel.md      社区模板库续集手册（141 TPL + 幽灵算子映射表）
│   ├── feature_engineering_sop.md           标准化特征工程流程 SOP（六阶段）
│   └── feature_engineering_template.md      特征工程文档模板（波级六节式）
├── architecture/                          ← 架构与结构类
│   └── project_structure_analysis.md        项目目录结构分析（含迁移状态）
├── tutorials/                             ← 教程课件类
│   └── 课件.md                              5个 Skill 实操课件（含实验全过程）
└── plans/                                 ← 历史计划类
    └── 2026-08-02-wqb-src-reconstruction.md src/wqb/ 包重建实施计划
```

---

## 文档导读

### 一、经验总结（experience/）

#### 1. 项目经验总纲 `experience/project_experience_master.md`
**定位**：项目全部经验的单一真相源，按主题结构化归档。
**内容**（10章）：
1. WorldQuant BRAIN 平台核心规则（闸门体系/PPA规则/API约束）
2. 数据集体检方法论（硬门槛/区域优先级/高价值数据集）
3. Alpha 构造方法论（预处理/三阶流水线/14模板/已验证配方）
4. 提交实战经验（流决策树/探测协议/幽灵提交识别）
5. 回测效率与并发模型（batch内并行/槽位上限/故障处理）
6. 回测纪律与监控框架（转向时机/断点续跑/进程监控）
7. 论坛研究通路（直连Zendesk/MCP工具/铁律）
8. 运行环境备忘（Python/MCP/GitHub/沙箱限制）
9. GLB 挖掘进展（stage1结果/无效数据集/已验证alpha）
10. 文件索引（全项目文档导航）

**适用场景**：新战役启动参考、问题排查、经验传承。

#### 2. 挖掘方法知识库 `experience/wq_alpha_mining_knowledge_base.md`
**定位**：验证有效的可复用挖掘方法、技巧与流程知识。
**内容**（10章）：
1. 挖掘流程总览（Step 0-5 决策树）
2. 数据集选择方法（评分模型/避坑清单/跨区域陷阱/全区域universe固化表）
3. 算子使用技巧（预处理决策树/窗口规律/中性化选择/turnover自适应/trade_when模板）
4. 提交策略（决策树/PPA vs RA/探测协议/幽灵提交）
5. 回测效率优化（并发模型/故障处理/MCP会话管理）
6. 监控分析框架（进程监控/回测效率分析要素）
7. 论坛研究方法（直连通路/高价值帖子挖掘/铁律）
8. 工具与脚本索引（核心工具/API封装/MCP工具）
9. 经验教训汇总（7致命错误+5效率陷阱+5信号构建陷阱）
10. 待验证方向

**适用场景**：挖掘流程标准化、新人上手、避坑参考。

#### 2b. 区域/模板知识库 `experience/region_template_kb.md`
**定位**：每区域"怎么挖"的知识卡 + 跨区域已验证通用模板的**使用协议**（内容本体在 `data/wqb.db` ledger_kv：`<REGION>/region_kb` ×9 区、`KB/template_kb` T-KB-01~10、`KB/kb_index`）。
**内容**（6章）：与既有建设的关系回顾 / 键布局 / Schema / 读写协议（S-PRE 必读、S6 回写、Mode B 找骨架）/ 三层分工（KB 蒸馏层 vs registry 明细层 vs wave 波次层）/ 建库快照。
**适用场景**：开战役前查区域配方与死路模式、优化时取已验证骨架、跨区移植前查 failed 记录。
**MCP 入口**：`get_ledger_key(region, "region_kb")` / `get_ledger_key("KB", "template_kb")`。

### 二、参考速查（reference/）

#### 3. 算子速查表 `reference/operators_notes.md`
**定位**：WQ BRAIN 平台全部可用算子的分类速查。
**内容**：87 条算子，按 7 类分类（Arithmetic/Logical/Time Series/Cross Sectional/Vector/Transformational/Group），含使用计数、Scope（COMBO/REGULAR/SELECTION）、Level（base/genius）。
**关键信息**：
- 已验证可用算子：rank(6次)/scale(4)/ts_backfill(9)/ts_zscore(7)/ts_mean(4)/subtract(6)/group_rank(3)/group_zscore(2)/vec_avg(2)/signed_power(2)/ts_rank(1)/ts_decay_linear(1)
- 幽灵算子清单（平台上不存在）：ts_entropy/ts_percentage/ts_skewness/ts_median 等 17 个

**适用场景**：表达式编写时查算子签名、确认算子可用性、规划算子探索率。

#### 3a. 社区模板库续集手册 `reference/community_tpl_library_sequel.md`
**定位**：《Alpha模板手册·社区模板库篇（续集）》（用户上传 alpha模板.docx）的人读全文参考卡，机器可读候选层在 `KB/community_tpl_kb`（141 TPL/19 大类，2026-08-31 合并续集增量）。
**内容**：17+2 个部分的模板骨架与参数速查表、**幽灵算子→已验证等价映射表**（§十八，入批前必查）、附加模板（IND 情感/速度加速度差分）、模板群动态管理方法论、与挖掘流程的集成点速查。
**适用场景**：Mode B B1 / ra-pipeline 步 5 补骨架时查候选模板；含幽灵算子骨架替换等价算子后再入批。

#### 3b. 特征工程流程与模板 `reference/feature_engineering_sop.md` + `reference/feature_engineering_template.md`
**定位**：每波挖掘的特征工程执行规范（字段理解→筛选→预处理决策→表达式生成→质量预估→候选池优化六阶段）+ 波级文档模板。
**内容**：SOP 含逐阶段执行者/数据源/产出/通过标准/反模式，与 S0-S6 战役流水线映射；模板含〔必填〕节与量化证据表格（入选/淘汰字段、预处理决策、BLOCK 处理、复盘钩子）。
**适用场景**：新波开始前复制模板到 `tracking/<REGION>/feature_engineering_wave<N>_<ds>.md` 填写；配套工具 `tools/pool_diversity.py`/`quality_predict.py`/`wave_gate.py`。

### 三、架构与结构（architecture/）

#### 4. 项目目录结构分析 `architecture/project_structure_analysis.md`
**定位**：项目目录组织分析、问题诊断、目标结构树、迁移执行状态。
**内容**（9章）：当前目录清点→功能分类→职责边界→问题风险→目标结构树→迁移指引→执行状态。
**当前状态**：2026-08-09 已完成目录清理（见 §9 更新），原 2_reference/ 已删除归档，wqb-share-03/ 已归档，__pycache__ 已清理。

**适用场景**：理解项目结构、规划目录调整、排查文件归属。

### 四、教程课件（tutorials/）

#### 5. Skill 实操课件 `tutorials/课件.md`
**定位**：5 个 BRAIN 挖矿 Agent Skill 的完整实操教程。
**内容**（5章+附录）：
1. 准备工作（目录结构/数据包三层结构/MCP配置）
2. 添加 MCP（工具链按流程顺序速查表）
3. 修改技能（WebDataScope 研究过程/Skill修改清单）
4. 测试提示词（逐条拆解如何被 Skill 接住）
5. 实验过程与结论（28批/280次模拟/9数据集/最终达标alpha）
- 附录：5 Skill 协作链路 mermaid 图/Failed RA 计数口径/幽灵算子清单

**核心成果**：`3qePVw3Z`（USA/TOP3000/D1, Sharpe 1.74, ProdCorr 0.593, 全指标达标）。
**十大教训**：中性化先验看样本量、风险族中性化是放大器、ProdCorr死区破局靠形态凸性等。

**适用场景**：学习 Skill 使用方法、理解挖掘实验全流程、参考提示词模板。

### 五、历史计划（plans/）

#### 6. src/wqb/ 重建计划 `plans/2026-08-02-wqb-src-reconstruction.md`
**定位**：从 5 个 SKILL.md 反向推断并重建 `src/wqb/` Python 包的实施计划。
**内容**：推理来源（13个SKILL引用映射）→文件结构（6子包15模块）→分步实施任务清单。
**当前状态**：已执行完成（src/wqb/ 包已落地，含 config/expression/research/search/memory/submit 子包）。

**适用场景**：理解 src/wqb/ 包的设计思路与模块职责。

---

## 知识库与其他目录的关系

| 目录 | 关系 | 说明 |
|---|---|---|
| `reference/` | 互补 | 机器库经验(machine_lib_experience)、USA D0 经验、news 系列等专题经验文档 |
| `reports/` | 互补 | 按日期归档的专题报告（PPA提交教训/论坛经验/EUR体检/模板库等） |
| `tracking/mining/` | 数据源 | 挖掘批次结果JSON、字段覆盖率、平台universe固化数据 |
| `tools/` | 工具源 | 数据体检/论坛研究/批量提交等可执行工具 |
| `.workbuddy/memory/` | 原始日志 | 每日工作记录（经验总纲的素材来源） |
| `archive/` | 归档 | 清理出的重复/废弃文件（2_reference/WebDataScope旧版等） |

---

## 维护规则

1. **新增文档**：归入对应子目录，更新本索引的导读部分。
2. **经验更新**：优先更新 `experience/` 下的两个总纲文档，不另开散文件。
3. **过期内容**：在文档头部标注"最后更新"日期，过期内容不删除但加注 `[已过时]`。
4. **跨文档引用**：使用相对路径（如 `[算子速查](../reference/operators_notes.md)`）。
5. **与 reports/ 的分工**：`docs/` 放结构化知识，`reports/` 放按日期的专题报告。
