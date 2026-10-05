---
name: brain-alpha-research
layer: L1
description: "做研究方法与搜索空间扩展（设置空间、范式库、论坛 / 论文模板整合、跨区陷阱）时使用；数据集 / 字段 / 新闻 / 饱和集等具体任务先看路由表，走对应专项 skill。常量只引用 config，不选集。"
last_verified: 2026-10-01
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究

## 职责边界

- **本 skill 负责**：研究方法与范式库——设置空间怎么扩、论坛 / 论文模板怎么整合与分类、研究结论怎么记录（研究者步骤）；另有一小节给维护者（改 config / 扩 `PARADIGMS`）。
- **本 skill 不做**：**不当 `src/wqb/config.py` 常量的第二作者**——区域优先级 / universe / delay / 中性化一律**引用** config；研究结论可以写，但必须标日期与失效条件；不做具体选集（S0）；不产出配置包。
- **上游 / 下游**：上游 = 研究需求；下游 = S0 / S1 的参考输入（不是流水线前置）。

## 1. 路由：先选对 skill

| 任务 | 用哪个 |
|---|---|
| 选集（在哪挖、白名单） | S0：ra-pipeline 步 2 / 决策表 D4；PPA 战役另看 `wq-brain-ppa-mining` |
| 发现数据集、类别映射 | `brain-dataset-exploration-general` |
| 探测单字段的行为（覆盖 / 分布 / 是否有信号） | `brain-datafield-exploration-general` |
| 字段 → 经济概念（特征工程） | `brain-data-feature-engineering` |
| 字段质量先验 / WebDataScope 预筛 | `brain-alpha-research-field-quality` |
| 新闻 / 情绪类数据集 | `brain-alpha-research-news-sentiment` |
| 饱和数据集（模板已被挖穿）改走假设驱动 | `brain-alpha-research-hypothesis-first` |
| 其它：设置空间扩展、范式库、论坛 / 论文模板整合、跨区陷阱 | **本 skill** |

## 2. 研究者步骤

1. **对照 config，只引用不改**：区域参数在 `config.REGIONS[<R>]`（`universes` / `default_universe` / `delays` / `neutralizations`）；范式名清单 `config.PARADIGMS`（13 条）；形状类 `config.SHAPE_CLASSES`（`{S1, S4, S5, S9}` 四类）。缺项 → 写成研究记录（步 5），**不要直接改 config**（判据见 §4）。
2. **USA REGULAR** 研究默认 universe = `TOP3000`；其它 USA universe 只作显式诊断或修复记录，不作常规搜索扩展。
3. **扩展中性化覆盖**：用 `wqb.config.neutralization_search_order(region)` 的完整顺序，平台原始选项集保留在 `REGIONS`。
4. **记录新设置 / 想法**时注明它影响哪一维：结构多样性 / 设置多样性 / 类别覆盖 / 内存与去重 / 可观测性。
5. **研究产出写成机器可读的简明记录**，字段沿用 `wqb.research.evidence.Evidence`：`source`、`source_type`（现有值 `platform` / `measurement`；论文来源用 `paper`）、`category`、`design_implication`、`actionable_rule`、`date`；再加两项本 skill 的要求：`applies_to`（区域 / universe / delay / 数据集范围）与 `expires_when`（失效条件）。**落点**：给用户看的研究结论写 `reports/` 下的 Markdown；要变成**规则**的才交维护者（§4）加进 `EVIDENCE_REGISTRY`——不要把散文笔记当结论。
6. **论坛模板整合**：论坛帖里的模板经 `python tools/forum_recon.py --question "<决策问题>" --out kb` 入库（**`KB/community_tpl_kb.forum_recon_entries[]` 的唯一写入方**，按 post_id 幂等合并；触发点与额度见 ra-pipeline `forum-recon-triggers.md`）。每个有希望的模板对照 `config.PARADIGMS` 分类；**≥ 50 赞**且归不进现有范式 → 先记研究记录，由维护者补范式名。检索 / 导出：`python tools/kb_templates.py --json [--category c --search kw]`；`--emit-ideas` 产出的是**确定性模板**——直接注入 GEM 会让它一行 LLM 都不调（ra-pipeline 步 4 不允许），只作**人读参考**，或经 LLM 改写后再注入。**不要手写 `KB/template_kb`**（它目前没有写入方代码，`docs/ledger_keys.json` 登记为 orphan）。
7. **算子覆盖**：论坛模板用了语法生成器不认识的算子，先用 `get_operators` 核对它在当前平台真实存在，再谈扩展；**幽灵算子**（平台不存在，用了整批静默失败）的权威清单 = `config.GHOST_OPERATORS`（`mcp__wq-brain-http__operator_audit` 可批量查），替换表在 ledger `KB/community_tpl_kb.ghost_operator_advisory`——含幽灵算子的模板按替换表改写或弃用。
8. **形状覆盖**：入库前用 `wqb.expression.validator.classify_shape(expr)`（及 `_shape_signature`）给模板分类，核对每个范式至少有一个代表形状；缺形状变体时记研究记录（`op1(A) - op2(B)` / `A - op2(B)` / `rank(A) vs group_rank(B, g)` 等非对称骨架，两侧前置算子的取值约定写清，不冻结成唯一写法）。**`check_batch` 不是门禁**——它零调用方、只作方法论参考；批级多样性的真门禁是 toolkit `gate.py` 闸 6（`check_batch_diversity`）。
9. **数据契约断流诊断法**（2026-10-01 沉淀，本方法论在步 3 / 步 4 各命中一次真 bug）：
   - **症状族**：某条纪律「文档写了、gate 有、但就是不生效」，或某字段/标签「prompt 里有、DB 里无、消费侧读不到」。
   - **四端排查（缺一即漏）**：① **写入侧**（谁写这个数据？写了没？）② **回退路径**（主路径写了，回退路径是不是绕过了？）③ **缓存版本**（内容变了但 version 没 bump → 旧缓存继续被消费）④ **消费侧入口**（消费方到底读不读这个键？）。
   - **取证铁律**：判定「生效/失效」**必须查真实数据**（DB 行数、字段填充率），不能只看代码「看起来对」。例：`family` 标签在 GEM 侧有产出、prompt 侧有引用，但 DB `expressions` 表**根本没有该列** → 选波族配额 100% 静默失效（全库 15650 行 family 空）。
   - **写入口保底**：新增一个会被多处回写的列，**UPDATE 必须用 `COALESCE(?, col)` 保底**——否则任何不带该列的调用点（回测回写 / gate 回写）都会把它覆盖成 NULL。本条踩过：`build_wave` 回写 selected 时漏带 family → 选完波 family 全丢。
   - **静态标注 vs 动态判定**：纪律若「每波动态变化」（如「探针先于扩批」），**选波时实时判定**优于落库时静态打标（`atom_flag` 的教训：静态标注依赖 field_map，常失败→全库 0 行）。
   - **★ 返回值契约漂移（第 5 端，2026-10-01 命中）**：函数返回类型变了，**调用方没同步解包** → 值被当标量塞进 URL / 拼进表达式 → 下游恒定失败。
     典型：`forum_research.resolve_id` 返回 **三元组** `(post_id, is_community_post, url)`，而 `forum_recon` 写 `pid = fr.resolve_id(...)`
     → URL 变 `/community/posts/('33036...', True, 'https://...').json` → **404 InvalidEndpoint** → 读帖 100% 失败。
     **危害放大器**：这类失败常被下游**静默吞掉**（重试器不重试 4xx、解析层见非 200 返回 `None`），
     最终表现成 `read_failed` 这类**与"真无解"无法区分的假象**——是「故障 ≠ 无解」纪律最防不住的一族。
     **排查法**：凡「某通路 100% 失败且无异常堆栈」，先**打印原始 HTTP 状态与最终 URL**（诊断脚本范式：`tools/diag_forum_read.py`），
     别只看聚合统计；修好后在**适配层**解包并兼容旧契约，配一条断言「下游收到的是标量」的守护测试。

## 3. 平台约束：只留指针（各有唯一出处）

| 约束 | 唯一出处 |
|---|---|
| universe / delay / 中性化的合法值 | `config.REGIONS` 与 `mcp__wq-brain-http__get_platform_setting_options`（**不凭记忆**；档位随平台更新，2026-09-22 重探后旧的「COUNTRY 中性化仅 EUR/GLB/ASI/MEA」「Delay 0 仅 USA/EUR/CHN/GBR/DEU」两句都已不成立） |
| 「支持」vs「数据广」 | `delays` 里有 0 只说明**平台接受** D0，不说明该区 D0 数据丰富——数据情况以 S0 体检为准 |
| `/data-fields` 四参齐全、非法 universe 报 500、`get_datasets` 一次给全数据集指标、TLS 抖动 | `wq-brain-ppa-mining` §11（症状 → 原因 → 处置表） |
| 区域优先级 | `config.REGION_PRIORITY`（USA 3 / EUR、KOR、GLB 2 / 其余 1）；选区用 `region_rotation` 与 `s0-select`，**不用**本 skill 的观测 |
| 离线包 ★★★ 不等于平台可用；跨区误推荐 | `wq-brain-ppa-mining` §5.1 |

2026-08-05 的区域快照（HKG 209 / KOR 192 / EUR 178 个数据集、「未开发首选 `ml_factor_proj`」等）**已移出**——它带日期与失效条件，放在 `wq-brain-ppa-mining/references/region-snapshots-2026-08.md`；「EUR 死路」的旧判断已撤回（那是选集错误，不是区域无解）。

## 4. 维护者步骤（改 config / 扩范式）

- **新增 vs 修正**：只有「**新增**且经平台实测」才可写进 config（实测来源：`get_platform_setting_options` 的返回，或 `python tools/fetch_all_universes.py` 批量固化——它读服务端 `.env`，日常不用）。**修正 / 撤回**既有常量是用户裁决，skill 不自作主张。
- 扩 `config.PARADIGMS` / `_OP_ARITY` 前先过 §2 的步 6–8；改完跑 `tests/unit/09_core/test_research.py`。
- 要让一条研究结论成为规则：在 `src/wqb/research/evidence.py` 的 `EVIDENCE_REGISTRY` 加一条 `Evidence`（其 `actionable_rule` 必须指向**真实存在的执行点**，不要写「由 X 强制」而 X 不强制）。

## 5. 验证（可执行）

（历史文档里的 `wqb research` / `wqb settings` 命令**不存在**——仓库没有该 CLI。）

```powershell
& $WQ_PY -c "import sys; sys.path.insert(0,'src'); from wqb.research.evidence import EVIDENCE_REGISTRY as R; [print(e.date, e.category, '|', e.actionable_rule) for e in R]"
& $WQ_PY -c "import sys; sys.path.insert(0,'src'); from wqb.config import REGIONS, neutralization_search_order; print(REGIONS['USA']['default_universe']); print(neutralization_search_order('USA'))"
& $WQ_PY -m pytest tests/unit/09_core/test_research.py -q
```

**期望**：第一条逐行打印证据（日期 / 类别 / 可执行规则）；第二条先打印 `TOP3000`，再打印 USA 的完整中性化顺序（11 项）；第三条全绿。USA 默认 universe 不是 `TOP3000`、或中性化顺序被截短，即为回归。

## 6. references（何时读）

| 文件 | 何时读 |
|---|---|
| [`references/forum-template-library.md`](references/forum-template-library.md) | 做论坛模板分类时（A–E 体系与使用规则） |
| [`references/asi-methodology.md`](references/asi-methodology.md) | 研究 ASI 区的 robust 达标路径时（含 2026-08 的历史结果；§8.2–§8.3 的等权拼腿已被政策禁止，只读不复用） |
| [`references/backtest-experience-archive.md`](references/backtest-experience-archive.md) | 找 2026-08 的 KOR / ASI / USA option 回测经验时（历史档案） |
| [`references/alpha-inspiration-usa-d1-shortinterest-insiders.md`](references/alpha-inspiration-usa-d1-shortinterest-insiders.md) | 找 USA/D1 的 short-interest / insiders 类模板灵感时（历史提炼，未按现行流程复核） |
| [`references/jump-decay-methodology.md`](references/jump-decay-methodology.md) | 研究 `jump_decay` 时——**推测性文档 [未验证]**，该算子当前账号不可用 |
| [`references/sources.md`](references/sources.md) | 研究来源优先级 |
| WebDataScope 26 条规则 | 已移到 `brain-alpha-research-field-quality/references/webdatascope-data-quality.md` |
