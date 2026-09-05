---
name: brain-alpha-research-field-quality
layer: L1
description: "字段质量先验与 WebDataScope 数据包质量预筛：按 alphaCount/userCount 排序字段种子、数据包零成本预筛、区域切换预筛门禁。当任务涉及字段质量先验、数据包预筛或基于质量指标的字段/数据集选择时使用。触发词：字段质量 / 质量先验 / WebDataScope / 数据包预筛。"
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究 — 字段质量（Field Quality）

## 触发场景

字段质量先验、WebDataScope 数据包质量预筛、或基于质量指标的数据集/字段选择。

## 工作流

### 1. 字段质量先验：优先高使用量字段（2026-06-19 用户指令）

`get_datafields` 返回逐字段的 `alphaCount`（使用该字段的已提交 alpha 数）和 `userCount`（独立用户数）。

**把它们当作数据质量/信号密度先验**：按 `alphaCount` 降序（同分按 `userCount`）排字段，候选构造从分布头部开始播种——社区反复用来构建可提交 alpha 的字段，在覆盖、稳健性与经济内涵上都经过实战检验。

低使用量字段（alphaCount 只有几个）风险更高，只用于刻意的去相关/新颖性玩法，不作默认种子。

具体做法：设计任何批次前，用 `jq` 把保存的 `get_datafields` 结果按 `alphaCount` 降序排好并查看前 ~30 名——头部字段常揭示该数据集**最强的经济轴**（如 analyst14/GLB 由 `anl14_mean_ndebt_fy1`=59α 和 `anl14_*_nav_fy2` 领衔——即资产负债表/资产价值轴，而非直觉的 EPS 修正轴）。

这既提高命中率又浮现非直觉风格。仍服从全部主题/金字塔/覆盖闸门；`coverage` <0.4 的字段无论使用量多少都必须 `ts_backfill`/`group_backfill`。

### 2. WebDataScope 数据包质量预筛（2026-07-29 → 2026-08-02 增强）

挖矿目标确定 region/delay 后、调用任何模拟前，先用本地 WebDataScope 数据包（`WebData_*.zip`）做零成本预筛。

**完整 23 条规则与数据结构见 [`../brain-alpha-research/references/webdatascope-data-quality.md`](../brain-alpha-research/references/webdatascope-data-quality.md)**，排名脚本 [`tools/webdata_quality.py`](tools/webdata_quality.py)。

核心决策规则速查：
(a) 数据集甜点区 = 100≤count≤3000 且 sharpe≥1.1×区域均值；<50 不可信，>30K 饱和避开；
(b) 中性化按数据集查表（`neutralization.dataset`），不盲扫；
(c) 字段体检决定预处理（cr<0.4→backfill / 单边→变化率 / 离散→rank / 月度→长窗）；
(d) OS 退化 = IS+OS 高但 OS 低（差>0.15），降优先级；
(e) 字段分布 5 形状（point_mass/zero_inflated/ceiling/concentrated/spread），zero_inflated 需事件门控；
(f) `--recommend` 输出综合 score 排序直接决定数据集挖掘顺序。

此步与 §1 的 `alphaCount` 先验互补。

### 3. 区域切换预筛门禁（2026-08-05 用户强制纪律）

**每次切换区域回测前，必须先执行** `python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region <目标区域> --delay 1`（从 wqb-share-03/ 目录，Windows 用 python 非 python3），读取区域级中性化排名/数据集甜点区/⚠退化标记/universe 体检覆盖后，才允许在该区域提交批次。

未预筛不切区域（已记录：EUR 2026-08-05 已跑，REVERSION_AND_MOMENTUM 最优 0.668；历史违规：USA/GBR subagent 启动时未先跑，不再追究）。

## 验证清单

1. 确认字段质量先验已应用（alphaCount/userCount 排序）。
2. 确认任何模拟前已执行 WebDataScope 数据包质量预筛。
3. 确认区域切换前已强制执行区域切换预筛门禁。
