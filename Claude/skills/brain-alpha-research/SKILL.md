---
name: brain-alpha-research
layer: L1
description: "研究数据集、字段、类别、universe、仿真设置与最新 alpha 挖掘方法，在不牺牲严谨性或平台兼容性的前提下扩展可搜索机会集。当任务是数据集发现、字段选择、设置空间扩展、类别映射，或把最新论文与平台/论坛指引整合进挖掘工作流时使用。"
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究

## 触发场景

数据集发现、字段选择、设置空间扩展、类别映射，或把论文/平台/论坛最新指引整合进挖掘工作流。

## 专项 skill 路由（2026-08-31 拆分）

本 skill 已拆分为多个专项 skill，按任务类型选择：

| 任务类型 | 专项 skill |
|---------|-----------|
| 新闻/情绪数据集研究 | `brain-alpha-research-news-sentiment` |
| 饱和数据集 hypothesis-first | `brain-alpha-research-hypothesis-first` |
| 字段质量先验 / WebDataScope 预筛 | `brain-alpha-research-field-quality` |
| 其他研究任务（本 skill） | `brain-alpha-research` |

## 工作流

1. 先读 [`src/wqb/research/evidence.py`](src/wqb/research/evidence.py) 理解最新设计信号。
2. 把期望的搜索扩展与 [`src/wqb/config.py`](src/wqb/config.py) 对照。缺失的区域/universe/中性化/类别/搜索 profile 先在那里补齐。
3. USA REGULAR 研究默认 universe 取 `TOP3000`。其他 USA universe 只作显式诊断或修复记录，不作常规搜索扩展。
4. 扩展中性化覆盖时，使用 `neutralization_search_order(region)` 的完整支持顺序，原始平台选项集保留在 `REGIONS`。
5. 记录新设置或想法时，注明它影响：结构多样性 / 设置多样性 / 类别覆盖 / 内存与去重 / 可观测性。
6. 研究产出捕获为**机器可读的简明记录**，不是纯散文笔记。
7. **论坛模板挖掘（2026-04-21，2026-09-05 校正落点）**。扫描论坛帖时，把每个有希望的模板对照 [`src/wqb/config.py`](src/wqb/config.py) 的 `PARADIGMS`（P1_SPREAD … P13_BUCKET_NEUT，13 条）分类。2026-04-21 论坛审计正是以此新增 P9_INFORMATION、P10_NORM_REG、P11_RESIDUAL_STRIP、P12_DISTRIBUTIONAL、P13_BUCKET_NEUT。≥50 赞的高赞模板若无法归入现有范式，先在 `PARADIGMS` 补范式名，再把模板本身写进 DB KB —— 落点是 ledger `KB/community_tpl_kb`（候选库，带 `category` / `placeholder_conventions` / `ghost_operator_advisory`）与 `KB/template_kb`（`validated` / `failed`），**不是**代码里的模板表。
   > **历史注记**：`src/wqb/expression/paradigms.py` 及其 `Template(paradigm, name, expression, …)` / `asymmetric` / `pre_op_pool_a`/`_b` / `PRE_OPS_WINDOWED` / `PRE_OPS_WINDOWLESS` 数据模型已在「remove dead modules」提交中删除。现存的只有 `config.PARADIGMS`（范式名清单）与 `config.SHAPE_CLASSES`（形状分类）。看到旧文档提这些符号，按本条改写，不要试图 import。
8. **算子分类覆盖检查**。论坛模板用了不在 `grammar._OP_ARITY` 里的算子时，它同样不在语法生成器里。**扩展 `_OP_ARITY` 前，先用 MCP `get_operators` 核对该算子在当前平台真实存在。**17 个已确认的幽灵算子（平台不存在，用了整批静默失败）清单与可用算子扩展白名单见 [`docs/reference/operators_notes.md`](docs/reference/operators_notes.md)（幽灵算子段）。论坛模板引用幽灵算子时，用替换表改写或弃用。
9. **形状覆盖检查（2026-04-22，2026-09-05 校正落点）**。论坛模板的二元组合器用了两个不同前置算子、单侧包裹或跨层组合器时，语法与 KB 应原生支持该形状。入库前先分类形状：`wqb.expression.validator.classify_shape(expr)` / `_shape_signature(expr)` 可分类任意已解析表达式，形状枚举在 `config.SHAPE_CLASSES`（S1/S4/S5/S9/S0）。核对目标形状在每个范式至少有一个代表模板；缺该形状变体时，在 `KB/community_tpl_kb` 补一条非对称骨架（`op1(A) - op2(B)` / `A - op2(B)` / `rank(A) vs group_rank(B,g)`），并在条目里写清两侧前置算子的取值约定，不要把前置算子冻结成唯一写法。
   > 步 5 的多样性守卫 `validator.check_batch` 正是按 shape signature 判重（≥2 shape signatures），所以形状覆盖不是文档洁癖，是过闸条件。
10. **全区域 universe / delay / 中性化固化表（2026-08-09 平台实测）**。数据集研究时**必须使用平台实测的合法值**，禁止猜测 universe 档位。完整固化表现在以 `src/wqb/config.py` 的 `REGIONS`（`universes`/`default_universe`）为唯一权威；抓取脚本 `tools/fetch_all_universes.py`（`OPTIONS /simulations` → 解析）。关键约束：(a) **COUNTRY 中性化仅 EUR/GLB/ASI/MEA 支持**；(b) **MEA 中性化最少**（仅6种，无 STATISTICAL/FAST/SLOW）；(c) **Delay=0 仅 USA/EUR/CHN/GBR/DEU**。
11. **API 实测约束（2026-08-05 沉淀，勿再踩）**。(a) `GET /data-fields` 必须 `instrumentType+region+delay+universe` 四参齐全，缺 universe → 400；(b) `universe` 传非法档位 → **500**（不是 400）；(c) **`get_datasets` 直接返回 coverage/fieldCount/userCount/alphaCount/valueScore/pyramidMultiplier**，比逐字段聚合快约 2 个数量级 → 数据集级体检优先走它；(d) 直连 API 的 `category` 是 dict，MCP 已扁平化为 str，需归一；(e) 沙箱到 api.worldquantbrain.com 有 TLS 抖动，常驻 MCP(localhost:8876) 共享会话更稳。
12. **区域优先级与 EUR 死路撤回（2026-08-05 实证）**。(a) **区域优先级修正为 HKG ≈ KOR > EUR**——HKG 209 数据集/cov均值 0.6958/倍率 1.8(最高)；KOR 192 数据集/cov 0.7046/倍率 1.7；EUR 178 数据集/cov 0.6616/倍率仅 1.3-1.5（系统性偏低）。(b) **原"EUR 死路"判断是错的，已撤回**——EUR/TOP1200/D1 实际有 178 数据集/38609 字段，coverage 均值 0.6616，35 个 ≥0.90。原战役 32 次回测只用了 4 个劣质数据集(model30 cov.713但4202 alpha极度拥挤 / news21 cov.53 / insiders12 cov.20)，无一满足 cov≥0.85。(c) **19 个高覆盖未开发数据集**（cov≥.85 & alpha≤50 & fields≥10），首选 `ml_factor_proj`（333字段全MATRIX/coverage全部1.0/0用户0alpha/valueScore 5.0/倍率1.5）。
13. **跨区域误推荐陷阱（2026-08-05 强化）**。`fundamental86/risk59/model216/fundamental94` 不是"0 字段"，而是 **EUR 区域根本不提供**；它们在 **KOR 全部可用**（fundamental94 有 215 字段 cov .8558）。属跨区域误推荐，与数据包过期无关。**判定某数据集不可用前，先换区域查一遍**。离线包 ★★★/☆☆☆ 只代表离线匹配度，**严禁**据此推断平台数据可用性。

## 验证清单

1. 运行 `wqb research` 确认新证据出现且带设计含义。
2. 运行 `wqb settings` 确认扩展的设置空间可打印。
3. 确认 USA 默认搜索顺序仍是 `TOP3000`，USA 中性化覆盖与平台支持一致。
4. 确认 §10-§13（universe 固化/API 约束/区域优先级/跨区陷阱）在规划时被读取消费。
