---
name: brain-dataset-exploration-general
layer: L1
description: "对已在 S0 白名单（或用户点名）的某一个数据集做数据集级审计：画像（字段数 / 覆盖 / 拥挤度）、字段分类落台账、按覆盖与使用量抽样深挖关键字段。用户要审计某个数据集、给数据集字段分类、探索新数据集时使用；选集走 S0，单字段评测走 datafield-exploration。"
last_verified: 2026-09-29
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# 数据集探索专家工作流

## 职责边界

- **本 skill 负责**：对**一个**数据集做数据集级审计——画像 → 字段分类落台账 → 关键字段抽样 → 审计结论。
- **本 skill 不做**：不选集（选集 = RA 步 2 / S0）；不做单字段深度评测（→ [`brain-datafield-exploration-general`](../brain-datafield-exploration-general/SKILL.md)）；不做特征工程决策；**不逐字段撰写「增强描述」**；**区域 / universe 档位一律引用 `src/wqb/config.py`（`REGIONS[<R>]`）与 `get_platform_setting_options`，本文不维护区域表**（各区状态看 INDEX「区域清单」与 `regions/<R>.md`）。
- **上游 / 下游**：上游 = S0 白名单内的数据集，或用户点名的候选（没有白名单、用户也没点名 → 先走 RA 步 2 选集）；下游 = 步 3 的 `s1_semantic_<ds>`、`brain-datafield-exploration-general`、特征工程。

## 1. 先定范围：分类永远全量，深挖只做代表字段

数据集可以有 1000+ 个字段（JPN analyst 1026），**不能逐个字段编目 / 写描述 / 仿真**：

- **分类**（§3）用本地脚本，零配额、秒级——**永远全量**。
- **深挖**（§5）只做**代表字段 ≤ 12 个**（缺省，经验值，可按需调）：每个语义大类取 `coverage` 最高、同分取 `userCount` 最高的 1–2 个，再加 3 个**冷门候选**（`userCount` 0–9 且 `coverage ≥ 0.4`——RA 步 3 §3.3 的冷门优先）。
- **描述**：平台字段描述以平台为准；本 skill 不产「增强描述」，对代表字段最多在审计结论里各写一行注释。

## 2. 画像（一次 `get_datasets` + 一次 `get_datafields`）

```
mcp__wq-brain-http__get_datasets       region=<R>  delay=<D>  universe=<U>  [category=…]   # fieldCount / alphaCount / userCount / pyramidMultiplier
mcp__wq-brain-http__get_datafields     region=<R>  dataset_id=<ds>  universe=<U>  delay=<D> # 逐字段 type / coverage / userCount / alphaCount
mcp__wq-brain-http__get_documentations / get_documentation_page                              # 数据集文档（页名以目录返回为准）
```

- `<U>` 取 `config.REGIONS[<R>]["default_universe"]`；D0 或其它档位用 `get_platform_setting_options` 核实，**不凭记忆**。
- **universe 传错的症状**：`get_datasets` **静默返回 0 条**（假阴性，数据其实存在），手写 `/data-fields` 则报 500（`wq-brain-ppa-mining` §11）——**先怀疑 universe，再怀疑该区没有数据**。
- 画像要写的：字段数、`coverage` 分布（< 0.4 的字段占比）、平台 `alphaCount` / `userCount`（拥挤度五条轴怎么读见 [`brain-alpha-research-field-quality`](../brain-alpha-research-field-quality/SKILL.md) §2）、所在 category 是否已点亮（S0 的 `recommend_datasets`）。

## 3. 字段分类：落点，以及全库的几套分类法

```powershell
python tools/field_semantic_classify.py --region <R> --dataset <ds> --write-ledger
```

产物 = ledger `s1_semantic_<ds>`（signal 白名单 / blocked 黑名单 + 经济大类）——**这是唯一有下游消费者的分类**：RA 步 3 的完成定义要求它，`wave_gate` 缺它整波 exit 2。脚本读 DB `fields` 表，所以要先有字段目录（步 3 的 `workflow_campaign(stage="S1", dataset=<ds>)`）。经济大类偏财报口径（价格收益 / 估值 / 盈利 / 成长 / 现金流 / 杠杆 / 效率 / 流动性风险 / 规模 / 每股 / 分红 共 11 类 + `other`，与 `tools/field_semantic_classify.py::ECON_CATEGORIES` 逐项对齐），非财报数据集（news / pv / model）大多落 `other`——**看 signal / blocked 的分界即可**。

旧文的四个维度（业务职能 / 数据类型 / 更新频率 / 层级）只是**写审计结论时的阅读辅助**，没有机器落点；数据类型来自 `get_datafields` 的 `type`，更新频率来自体检包 `frequency`。全库共有下面几套分类法，互相不替代：

| 分类法 | 维度 | 用在哪 | 落点 |
|---|---|---|---|
| **S1 语义**（本 skill 的落点） | signal / blocked + 10 个经济大类 | 闸 SEM、GEM 字段池 | ledger `s1_semantic_<ds>` |
| 新闻 5 家族 | direction / attention / dispersion / event_type / peer_context | news / sentiment 数据集的配对设计 | `tracking/taxonomies/…`（[`news-sentiment`](../brain-alpha-research-news-sentiment/SKILL.md) §2） |
| dfe 8 问 ↔ GEM 概念位 ↔ hypothesis 12 类 | 三套本体互相映射 | 特征工程 ideas、GEM 生成配额、饱和集假设目录 | 见 [`concept-taxonomy-map.md`](../wq-brain-ra-pipeline/references/concept-taxonomy-map.md) |

## 4. 评分：只留指针，不手算

数据集级评分与拥挤罚**不在本 skill 里算**：执行 = toolkit `score_datasets.py`（S0，`workflow_campaign(stage="S0")`），公式、阈值、缺省以 `wq-brain-campaign-toolkit/references/probe-scoring-v2.md` 与 `score_datasets.py` 的常量为准；PPA 战役另有硬闸（`wq-brain-ppa-mining` §1）。旧文里的 `0.30/(1+log10(1+alphaCount))` 公式、「vs 缺失按 0.3」、tier2「cov ≥ 0.85 / ac ≤ 200 / fc ≥ 5」已被 v3.1（分段拥挤罚、分位分层、硬地板）取代，**不要再用**。

## 5. 关键字段抽样

按 §1 选出的代表字段，走 [`brain-datafield-exploration-general`](../brain-datafield-exploration-general/SKILL.md)：**先离线体检包、再最小仿真集**。不对整个数据集逐字段仿真。

## 6. 调研：默认不查论坛

论坛检索默认**不做**（token 黑洞，见 RA 的论坛触发表）。只有满足触发条件才查——判死复开、机制枯竭——走 `python tools/forum_recon.py --question "<决策问题>" --out kb`（[`forum-recon-triggers.md`](../wq-brain-ra-pipeline/references/forum-recon-triggers.md)）。**不要**为数据集审计加载 `brain-forum-browse`（它是只读浏览，不是审计工具）。平台官方文档（`get_documentations`）不受此限。

## 7. 审计结论怎么写

- **机器可读的只有 `s1_semantic_<ds>`**（§3）与步 3 写的 `catalog_<ds>`；其余都是给人读的结论，写在对话里，需要留档时写 `reports/dataset_audit_<REGION>_<ds>.md`（**不是事实源**，事实源在 DB）。结论模板见 [`reference.md`](reference.md)。
- **Alpha 思路**只写**机制假设**（一句话经济叙事 + 该用哪一类数据当主 / 辅信号），**不写表达式**——表达式走 RA 步 4 的概念优先生成。

## 验证清单（每项写产物）

1. **范围已定**：结论里写明「分类 = 全量 N 个字段；深挖 = 代表字段 K 个（≤ 12）」，没有逐字段编目。
2. **画像有读数**：字段数、`coverage < 0.4` 占比、`alphaCount` / `userCount`、category 点亮状态；universe 取自 `config.REGIONS`（或 `get_platform_setting_options`），不是手写表。
3. **分类已落台账**：`mcp__wqb-db__get_ledger_key(region, "s1_semantic_<ds>")` 能读到（或注明字段目录尚未扫描、先跑步 3 的 S1）。
4. **调研有触发理由**：没有无理由的论坛检索；若查了，写明命中的是哪条触发。

## references

| 文件 | 何时读 |
|---|---|
| [`reference.md`](reference.md) | 要写审计结论（模板）、查 MCP 工具速查、找平台文档页时 |
