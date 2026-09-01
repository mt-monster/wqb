# 区域/模板知识库（Region & Template KB）

> 建库：2026-08-25。DB 单轨：真相源在 `data/wqb.db` 的 `ledger_kv` 表，本文档是**使用协议与索引**，不承载内容本体。
> 定位：**蒸馏层**——每个区域"怎么挖"的一页知识卡 + 跨区域已验证的通用模板。明细层见 registry_empirical，波次层见 wave_results。

---

## 1. 与既有建设的关系（回顾）

| 既有建设 | 层次 | 与本 KB 的关系 |
|---|---|---|
| `docs/experience/wq_alpha_mining_knowledge_base.md` | 方法层（流程/算子/提交/效率） | 互不替代：那份讲"怎么挖 alpha"，本 KB 讲"这个区/这个模板挖成过什么" |
| `docs/reference/economic_alpha_template_library.md` | 模板理论层（T1-T12 经济学骨架） | 本 KB 的 `template_kb` 只收**有跨区实证**的模板（T-KB-01~10），理论骨架仍看那份 |
| `cross_region_lessons` 表 | 跨区铁律（9 条） | 铁律已吸收进 region_kb.dead_patterns 与 template_kb.iron_law |
| `registry_empirical`（win/dead_end/campaign 层） | 明细层 | KB 的 win_recipes/dead_patterns 是其蒸馏，evidence 字段回指 entry_id |
| `docs/experience/2026-08-22-full-campaign-history-retro.md` | 复盘文档 | GBR/HKG/ASI/GLB 知识卡的来源（这四区无 registry 行） |
| `docs/experience/` 各专题 retro | 单战役复盘 | KB 的上游；KB 是它们的可机读浓缩 |

## 2. 键布局（ledger_kv）

| 键 | 内容 | 规模 |
|---|---|---|
| `<REGION>/region_kb` | 区域知识卡 ×9（EUR/IND/KOR/MEA/USA/GBR/HKG/ASI/GLB） | 每卡一页 JSON |
| `KB/template_kb` | 通用模板 T-KB-01~10（含 2 个负模板），**已验证层** | 单键 |
| `KB/community_tpl_kb` | 社区模板**候选库**（2026-08-25 从《完整版》docx 提炼 131 个；2026-08-31 合并《续集》增量） | 141 个 TPL / 19 大类 + 占位符约定表 + `ghost_operator_advisory` 幽灵算子警示表 |
| `KB/kb_index` | 索引 + 读写协议 + 来源清单 | 单键 |

合成桶 `KB` 与批次模拟器的 `BATCH` 桶同类：无区域上下文的全局知识挂合成桶。

**community_tpl_kb（候选层）**：社区论坛馈赠的模板骨架，结构化字段 `{tpl_id, name, category, skeleton, params, example, usage, notes, status}`，全部 `status=candidate_unverified`（未经本工作区战役实证），占位符替换规则见键内 `placeholder_conventions`（原帖 `<field/>` 尖括号风格 ≡ `{field}` 花括号风格）。键内 `ghost_operator_advisory` 登记幽灵算子→已验证等价映射（人读全文见 `docs/reference/community_tpl_library_sequel.md` §十八）：**取骨架前必须先查该表，含幽灵/未验证算子的骨架替换等价算子或先 `validate_expressions` 实测，否则整批 ERROR/CANCELLED**。与 template_kb 的关系：候选层 → 回测验证后把区域证据回写进该模板的 `validated`/`failed` 字段，≥2 区验证（或 1 区强证据）后按 T-KB-NN 晋升入 template_kb；长期全 failed 的候选按"模板动态管理闭环"（GLOBAL/region_kb.methodology）降级/剔除。

## 3. Schema

**region_kb**：
```
region / updated_at / tier                    — 定位一句话
settings_proven                               — 已验证设置（universe/delay/中性化/caveat）
active_alphas                                 — 台账 ACTIVE id 列表
win_recipes[]                                 — {name, skeleton, evidence, metrics, settings}
dead_patterns[]                               — 死路模式（一行一模式，不复制 registry entry 列表）
open_threads[]                                — 当前战线/未开 campaign
notes[]                                       — 区域特性（定价效率/结构性边界等）
```

**template_kb**：
```
templates[] = {
  id (T-KB-NN), name, mechanism,              — 经济机制
  skeleton, params,                           — 骨架与参数
  validated: {region: 证据},                   — 哪些区验证过（骨架优先从这里取）
  failed:     {region: 原因},                  — 哪些区死过（移植前必看）
  iron_law, source                            — 铁律 + 证据回指
}
```

## 4. 使用协议

### 4.1 读（agent / 人）

| 时机 | 动作 |
|---|---|
| **S-PRE 开战役前（必读）** | `get_ledger_key(region, "region_kb")` + `get_ledger_key("KB", "template_kb")`：dead_patterns 命中的方向直接跳过；win_recipes 是配方扩展首选 |
| **S2 生成先验注入（ra-pipeline 步 4）** | 组装 priors.json：region_kb.win_recipes + template_kb（validated 含本区）→ `wins`（≤6）；region_kb.dead_patterns + template_kb（failed 含本区）→ `dead_ends`（≤12）；DB 为空才用 region profile 静态 priors 兜底。community_tpl_kb 不进 priors |
| **Mode B Step B1 找骨架** | 读 template_kb：优先 validated 含本区的模板；跨区移植看 failed 与 iron_law（T-KB-07 教训：GBR 赢配方 KOR 全灭）；已验证层无匹配时，退到候选层 `get_ledger_key("KB", "community_tpl_kb")` 按 category 检索骨架，占位符按 placeholder_conventions 替换，**并先查键内 `ghost_operator_advisory` 做幽灵算子替换** |
| **配额决策** | region_kb.open_threads 里 untried campaign 优先于已 exhausted 方向 |
| **提交判定** | region_kb.notes 里的区域提交陷阱（如 IND 的 -rank 语法、本地 prod_corr 偏低） |

MCP 调用示例：
```
get_ledger_key(region="KOR", key="region_kb")
get_ledger_key(region="KB",  key="template_kb")
get_ledger_key(region="KB",  key="kb_index")
```

### 4.2 写（更新纪律）

| 事件 | 动作 |
|---|---|
| S6 / review_wave 后 | `upsert_ledger_key(region, "region_kb", ...)` 更新 open_threads（读旧值→改→写回） |
| 新 alpha ACTIVE | win_recipes 追加一条（name/skeleton/evidence/metrics/settings） |
| 新死路模式确认 | dead_patterns 追加一行（明细仍走 registry dead_end 层，KB 不复制） |
| 新模板获得 ≥2 区实证或 1 区强证据 | template_kb.templates 追加（id 递增 T-KB-NN） |
| 社区模板回测验证后 | 把区域证据回写 community_tpl_kb 该模板的 validated/failed；达标后晋升 template_kb |
| 任何写入 | 更新 updated_at |

写示例：
```
upsert_ledger_key(region="KOR", key="region_kb", value={...更新后的完整 JSON...})
```

### 4.3 三层分工（勿混淆）

- **KB（蒸馏层）**：怎么挖这个区 / 用什么模板 —— 人读 + agent 决策
- **registry_empirical（明细层）**：哪条表达式死/赢/哪个数据集 campaign 状态 —— `get_dead_ends` / `get_campaigns`
- **wave_results（波次层）**：每波结果台账 —— `list_wave_results` / `get_latest_wave`

KB 不复制明细，只做蒸馏与回指（evidence 字段）。

## 5. 当前快照（2026-08-25 建库时点）

| 区域 | tier | ACTIVE | 核心配方 |
|---|---|---|---|
| KOR | 主力（目标 10） | 3 | 评级修正×SH 跨周期混合；PV 主导+表达式层 sector |
| IND | 最富 submit_ready（31 待判） | 4 | mdl177 长窗结构（2y 2.2-3.6）；scale(-rank) 破 robust 墙 |
| EUR | Mode B 深挖（81 波） | 2 | 慢 MODEL×快 PV 混合；FCF 镜像稀释破 PROD 墙 |
| MEA | 收官 | 4 | 修正广度去 revision 腿；EPS+Net 修正动量组合 |
| USA | SA 达成 / RA 饱和 | 1 (SUPER) | SA selection+combo（SUBINDUSTRY） |
| GBR | 达成 | 4 | starmine 四向价值；delta66 双差分 |
| HKG | 终止转 ASI | 0 | —（价值天花板 1.22+prod 0.806） |
| ASI | 探针区 | 0 | —（2 untried campaigns） |
| GLB | 早期达成 | 1 | COUNTRY 分组三区域检查解法 |

模板库要点：T-KB-01 慢×快混合是唯一五区验证配方；T-KB-02 镜像反转（-rank 语法）；T-KB-03/04 两种破 PROD 墙路径；T-KB-09/10 为负模板（探针天花板/稀疏事件墙）。

## 6. 维护责任

- 每次战役 S6 回写时同步更新对应 region_kb（读改写，幂等 upsert）
- 每月对照 `get_region_overview` 校快照漂移（active 数/wave 数）
- 本文档只在协议变更时修改，不追内容（内容以 DB 为准）
