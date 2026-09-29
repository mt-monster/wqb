---
name: brain-data-feature-engineering
layer: L1
description: "对已锁定的数据集做人工字段理解：分档、字段画像、按 8 问产出机制概念，写成 GEM 可摄入的 ideas（含 Implementation Example 模板）与 S1 台账（source=manual）。要为黑盒 / 半透明数据集做 S1 决策、或想让 GEM 用你写的概念时使用；workflow_feature_engineering 节点产的是确定性模板，不会被 GEM 注入。"
last_verified: 2026-09-29
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - mcp__wq-brain-http__get_datasets
  - mcp__wq-brain-http__get_datafields
  - mcp__wqb-db__get_ledger_key
  - mcp__wqb-db__upsert_ledger_key
---

# BRAIN 数据特征工程工作流

## 职责边界

- **本 skill 负责**：字段 → 特征工程决策（**由 agent 人工完成**）——字段分档、字段画像、预处理决策、按 8 问产出机制概念，并落成 GEM 可摄入的 ideas 文档与 S1 台账。
- **本 skill 不做**：**不生成最终 alpha 表达式**（那是 L2 `brain-make-some-gem`，Implementation Example 只是 `{占位符}` 模板）；**不选数据集**（没有 `dataset_id` → 回 RA 步 2，不自行挑）；不回测；不写 ledger 键 `s1_<ds>_d<delay>` 以外的 DB 表。
- **上游 / 下游**：上游 = S0 白名单内已锁定的数据集（RA 步 3 阶段）；下游 = 步 4 GEM（`s1_<ds>_d<delay>` 命中即自动注入）与 S2 字段校验。

## 两条产物路径：先选路径，别混

| | A. `workflow_feature_engineering` 节点 | B. 本 skill 正文，agent 人工完成 |
|---|---|---|
| 产出 | **确定性模板渲染**（字段画像表 + 固定 8 问框架 + `rank(ts_mean({f},66))` 式模板），不调 LLM | 你写的机制概念 + Implementation Example |
| ledger `source` | `feature_engineering_node` | **`manual`** |
| GEM 是否注入 ideas | **不注入**——注入后 GEM 一行 LLM 都不调，整波退化为模板展开 | **注入**（引擎按下表自动读取，不必传 `--ideas-file`） |
| 有效产物 | typed catalog、字段质量先验、前缀簇、`s2_field_pool`（RA 步 3 要它们） | ideas 文档 + 字段白名单 + 预处理决策 |

**`source` → 是否注入**（`gem.py::TEMPLATE_IDEAS_SOURCES` 与 `run_pipeline.py` 同口径，测试对照）：`feature_engineering_node` / `standalone` / `standalone_v2`（及以它们开头带空格或括号的写法）= 模板渲染文档，**一律不注入**；其余 `source`（`manual`、GEM 自含跑完回写的 `s2_nested`）且 `ideas_md_path` 文件存在、`pipeline_mode ≠ skeleton` → 自动注入。显式传 `ideas_file` 永远优先。**所以人工产物的 `source` 必须写 `manual`——写成 `standalone` 会被 GEM 静默忽略。**

`s1_<ds>_d<delay>` 的读取方：GEM 节点与 runner（`source` / `ideas_md_path` / `field_whitelist` / `field_prefix_summary`）、`tools/s2_field_validator.py`（表达式字段 ∈ 白名单 / 候选池）、`campaign` 节点的预检（补录 S2 合规记录）。**toolkit 的闸 1–5 不读它**（闸 2 读的是 typed catalog）。

## 输入

- **必填**：`region`、`delay`、`dataset_id`（S0 已锁定；没有 → 回 RA 步 2）、`data_category`（`get_datasets` 返回的 category）。
- **可选**：`universe`——缺省取 `config.REGIONS[<region>]["default_universe"]`（**不是**一律 `TOP3000`：KOR / AMR 是 `TOP600`、EUR `TOP2500`、JPN `TOP1600`）。

## 第 0 步：字段透明度分档（强制前置）

按语义透明度决定分析深度，避免对自解释字段集浪费分析轮次。**裁决序：黑盒 > 半透明 > 透明**——满足任一黑盒判据就按黑盒（宁可多分析，也不让 GEM 绑定池失控）；不满足黑盒、满足透明判据才是透明；其余半透明。

| 档位 | 判定标准（满足其一） | 分析深度 |
|---|---|---|
| **黑盒集** | `other*` / `model*` / `ai_*` / `ml_*` 等评分型 / 投影型字段集；或字段名无语义（如 `q1s3_x87`）；或字段描述覆盖率 < 30% | 第 3 步 8 问**全问** |
| **透明集** | fundamental / analyst / earnings / insiders / shortinterest 类且字段名含标准财务词汇（eps / revenue / ebitda / estimate / revision / holder …）；或描述覆盖率 ≥ 80% 且描述均值 > 5 词 | **跳过 8 问**：字段画像 → 预处理决策 → 白名单 |
| **半透明** | 介于两者之间（如 pv / risk 系） | 只问 1 / 2 / 7 三问（不变量 / 变化 / 相对位置） |

跨档例：`model109` 的描述覆盖率即使 ≥ 80%，`model*` 前缀已满足黑盒判据 → 按黑盒。依据：2026-09-01 价值审计——8 问对透明集边际价值低（103 个 s1 键里透明集的分析内容高度模板化），对黑盒集（`other455` 类 1500 个无语义字段）是刚需。

## 第 1 步：锁定数据集

`mcp__wqb-db__get_ledger_key(region, "s0_whitelist")` 命中时，数据集必须在 `datasets` 内——**不在则报出冲突并停**，交回 RA 步 2，不越白名单分析；未命中（无战役目录的临时分析）跳过校验。

## 第 2 步：字段画像

- `mcp__wq-brain-http__get_datafields(region, dataset_id, universe, delay)` 取 id / description / type / coverage / userCount；更新频率与分布形态取体检包 `tracking/mining/field_inspect_<region>_<ds>.json` 的 `metadata`（不在包内的区域就没有，写「未知」）。
- **先剔非信号字段**：`s1_semantic_<ds>`（步 3 的 `field_semantic_classify.py`）里的 blocked 名单不进画像、不进概念。
- 对将进概念的字段回答五问：测的是什么？怎么测的？时间维度（瞬时 / 累计 / 变化率）？为何存在？可靠性如何？——不要求对所有字段逐个展开。

## 第 3 步：8 问 → 机制概念（有预算）

1. 不变（稳定性）　2. 变化（速率 / 加速度 / 波动）　3. 异常（偏离幅度与显著性）　4. 交互（**只落成条件 / 分组 / 同源价差，不把第二数据集当并列项相加**）　5. 结构（构成 / 比例）　6. 累积（记忆 / 衰减）　7. 相对（排名 / 归一 / 相对位置）　8. 本质（第一性原理）。对应关系见 [`concept-taxonomy-map.md`](../wq-brain-ra-pipeline/references/concept-taxonomy-map.md)。

**预算（缺省，经验值，不是硬闸）**：全部概念 **8–12 个**（半透明 ≤ 6）；每个概念 **1–2 个字段**；每问 ≤ 2 个概念；同一字段至多进 2 个概念。理由：概念数无上限会组合爆炸（KOR / fundamental17 首波：黑名单字段仅占 9.9% 却吃掉 49.4% 的生成预算），且与 GEM 铁律 1「机制 → 1–2 个字段 → 一个 Implementation Example」、铁律 6 / 7 的「8 个概念」量级一致。

## 第 4 步：概念块（GEM 摄入契约）

每个概念写成下面的块。**GEM 解析器认这几个标记**（`pipeline_reports.extract_template_blocks`）：以 `**Concept**:` 开头；块内必须有 `- **Implementation Example**: \`模板\``，整份文件一个这样的块都没有 → 直接报错「No **Concept** blocks with **Implementation Example** found」；模板是 Python format 语法，`{占位符}` 必须是数据集字段的**后缀**（规则见 [`brain-feature-implementation`](../brain-feature-implementation/SKILL.md)「模板语法」），对不上的模板被丢弃并打印 `[validate] 丢弃 …`。`**Expected Exposure**` 行不写会被按关键词推断补上（`(inferred)`），**请自己写**——闸 6 的收益来源多样性读它；取值沿用 `pipeline_reports._EXPOSURE_KEYWORDS`：momentum / reversal / value / quality / growth / lowvol / liquidity / sentiment / flow / risk / other。

窗口只用标准窗口 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260；不写加权拼腿（`0.5*a + 0.5*b`、`add(multiply(…), multiply(…))` 会被闸 5 拦）。示例（半透明集 `pv1`，只问 1 / 2 / 7 三问；字段都是 `pv1` 的真实字段）：

```markdown
**Concept**: 量能冲击后的短期反转
- **Fields Used**: returns, volume, adv20
- **Definition**: 成交量相对 20 日均量放大的日子里，短期涨跌幅的反向信号
- **Logical Meaning**: 放量冲击后的价格反应过度，5 日内部分回归
- **Directionality**: 近 5 日涨得越多，做空权重越大
- **Boundary Conditions**: 停牌 / 涨跌停日的量能失真
- **Expected Exposure**: reversal
- **Implementation Example**: `trade_when(rank({volume} / {adv20}) > 0.8, -rank(ts_zscore({returns}, 5)), -1)`

**Concept**: 收益波动的低波稳定性
- **Fields Used**: returns
- **Definition**: 66 日收益率波动越小越稳定
- **Logical Meaning**: 低波动股票被风险厌恶型资金持续偏好
- **Directionality**: 波动越低，多头权重越大
- **Boundary Conditions**: 波动骤降可能是停牌而非稳定
- **Expected Exposure**: lowvol
- **Implementation Example**: `-rank(ts_std_dev({returns}, 66))`

**Concept**: 成交量相对自身一年历史的位置
- **Fields Used**: volume
- **Definition**: 当日成交量在过去 252 日中的时序排名
- **Logical Meaning**: 相对自身历史的活跃度，剔除股票间的规模差异
- **Directionality**: 越接近一年高位，越拥挤
- **Boundary Conditions**: 新上市不足 252 日的股票排名失真
- **Expected Exposure**: liquidity
- **Implementation Example**: `-rank(ts_rank({volume}, 252))`
```

## 第 5 步：落盘与台账（强制，先文件后台账）

- **ideas 文档**写 `data/gem_runs/output_report/manual_<REGION>_delay<D>_<ds>_ideas.md`（GEM 的报告根 `GEM_REPORT_ROOT`；`data/` 已 gitignore，`WQB_GEM_DATA_ROOT` 可覆盖）。**不要**写 `./output_report/`（那是审计报告目录，与 CWD 有关）；`manual_` 前缀避开 GEM 重跑时清理的 `gem_…` / 无前缀旧名，也和节点产物的 `fe_` 前缀区分。
- **台账**：`mcp__wqb-db__upsert_ledger_key(region, "s1_<DATASET_ID>_d<DELAY>", value)`（key 不可用 `_` 前缀；同 (region, dataset, delay) 重跑覆盖，upsert 幂等）：

```json
{"dataset": "<DATASET_ID>", "region": "<REGION>", "delay": <DELAY>, "universe": "<UNIVERSE>",
 "ideas_md_path": "<上一步文件的绝对路径>", "field_whitelist": ["<完整字段 id>", ...],
 "preprocessing": {"<字段 id>": "backfill|winsorize|rank|zscore|trade_when", ...},
 "concept_count": <概念数>, "source": "manual", "generated_at": "<ISO 时间戳>"}
```

**主从关系**：ledger 是事实源，ideas 文档是它指向的载荷。`field_whitelist` 用**完整字段 id**（不是后缀），引擎用它收窄绑定池，概念里出现白名单外的字段会告警并降级；`preprocessing` **只作记录**（没有代码读它，真正执行预处理的是体检硬门与 GEM 的规则）。战役目录内也可用 toolkit CLI：`campaign.py --campaign-dir <CD> ledger set "s1_<ds>_d<delay>" '<json>'`。S0 换数据集 / 换 delay 时，新的 S1 覆盖对应键，无需删除。

## 验收（每项写产物）

1. **分档已写明**：回报里有档位与依据（黑盒 / 透明 / 半透明，命中哪条判据）。
2. **概念块可被解析**：文档里每个概念都有 `**Concept**:` 与 `- **Implementation Example**:`；概念数在预算内；每个块带 `**Expected Exposure**`、字段 id 与方向；`Implementation Example` 的占位符都对得上真实字段后缀，窗口是标准窗口。
3. **台账已写且可读**：`mcp__wqb-db__get_ledger_key(region, "s1_<ds>_d<delay>")` 返回 `source == "manual"`，`ideas_md_path` 指向的文件存在。
4. **没有越界**：字段全部来自白名单内数据集与 `field_whitelist`；blocked 字段没进任何概念。

## references

| 文件 | 何时读 |
|---|---|
| [`OUTPUT_TEMPLATE.md`](OUTPUT_TEMPLATE.md) | 写完整分析报告（执行摘要 / 字段解构 / Q1–Q8 概念 / 实现考量）时的**唯一提纲**；SKILL 不再复述一遍 |
| [`reference.md`](reference.md) | 想看 8 问的思维方式与设计理念时 |
| [`examples.md`](examples.md) | 想看一个完整的教学案例（**虚构数据集**，不是真实字段）时 |
