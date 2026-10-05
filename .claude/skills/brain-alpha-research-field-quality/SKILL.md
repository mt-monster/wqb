---
name: brain-alpha-research-field-quality
layer: L1
description: "字段质量先验与 WebDataScope 数据包预筛：要用 alphaCount / userCount 判断字段或数据集质量、跑数据包零成本预筛、切换区域回测前做预筛时使用。只作 S0 的前置参考，不替代 S0 体检。触发词：字段质量 / 质量先验 / WebDataScope / 数据包预筛。"
last_verified: 2026-10-05
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---



# BRAIN Alpha 研究 — 字段质量（Field Quality）

## 职责边界

- **本 skill 负责**：WebDataScope 数据包质量预筛（**S-PRE，纯离线**：低覆盖 / 高偏度 / 厚尾 / 单边 / 稀疏事件）；`alphaCount` / `userCount` 作为字段 / 数据集质量先验的**读法**；区域切换预筛的判定顺序与留痕。
- **本 skill 不做**：不产出战役选集、不回测、不提交；**只作 S0 的前置参考，不替代 S0 体检**。
- **上游 / 下游**：上游 = 本地 WebData 快照（`research-data/WebData_20260219_V0.10.9.zip` 与 `tools/gen_field_inspect_packs.py` 产出的体检包）；下游 = S0 选集参考、RA 步 5 的体检硬门。


<!-- last_verified 核实范围（2026-10-05）：核实 references/webdatascope-data-quality.md 的**工具调用链路**——tools/webdata_quality.py 存在且 --help 实测通过，正文 14 处命令示例的 flag与其 argparse 定义逐条吻合，全部有效（读包底层走 tools/lib/pack_reader.py::open_pack，是调用关系而非替代关系）。规则 1–8 的平台侧口径未重新对照平台，下次用到规则前需重新核对。 -->
## 1. 字段质量先验：先验用于「选方向」，进入造批要服从 RA 步 3

> **受 ra-pipeline 步 3（§3.3 字段分级风险筛查）约束。** 2026-06-19 的用户指令「按 alphaCount 降序、从分布头部播种」是当时的口径，之后被 2026-08 的 GLB 实验实测限定：高使用量字段 prod_corr 必超。两段话不矛盾的读法是**分阶段**：

| 阶段 | 怎么用 `alphaCount` / `userCount` |
|---|---|
| **选集 / 研究方向发现** | 高使用量 = 覆盖、稳健、经济内涵经过社区实战检验的**先验**；头部字段常揭示该数据集**最强的经济轴**（例：analyst14 / GLB 由 `anl14_mean_ndebt_fy1`=59α 与 `anl14_*_nav_fy2` 领衔——资产负债表 / 资产价值轴，而非直觉的 EPS 修正轴） |
| **字段级投入（造批）** | 按 RA 步 3 的 `users` 分级：≥ 50 只做信号方向验证；10–49 进候选池、提交前必须实测 prod_corr；0–9 优先候选池，**冷门字段占批次预算 ≥ 50%**（经验阈值，出处 `prod-corr-avoidance.md`） |
| **饱和数据集** | 不叠加本先验（那正是 hypothesis-first 的适用域：模板空间已被挖穿，头部字段只会撞 prod 墙） |

- 取数：`mcp__wq-brain-http__get_datafields(dataset_id=…, region, delay, universe)` 返回逐字段 `alphaCount` / `userCount` / `coverage`，在对话里按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴；不依赖 `jq`，也不散写 SQL。
- 仍服从全部主题 / 金字塔 / 覆盖闸门；`coverage` < 0.4 的字段无论使用量多少都必须 `ts_backfill` / `group_backfill`（体检硬门检查 1）。

## 2. WebDataScope 数据包预筛

目标 region / delay 确定后、调用任何模拟前，先用本地数据包做零成本预筛。**完整 26 条规则与数据结构**见 [`references/webdatascope-data-quality.md`](references/webdatascope-data-quality.md)，排名脚本 `tools/webdata_quality.py`：

```powershell
& $WQ_PY tools/webdata_quality.py --zip research-data/WebData_20260219_V0.10.9.zip --region <REGION> --delay 1
```

**规则速查**（数值以规则文档与 `tools/webdata_quality.py` 为准）：(a) 数据集甜点区（离线提交量 `count`）100 ≤ count ≤ 3000 且 sharpe ≥ 1.1 × 区域均值，< 50 不可信；(b) 中性化按数据集查表，不盲扫；(c) 字段体检决定预处理（cr < 0.4 → backfill / 单边 → 变化率 / 离散 → rank / 月度 → 长窗）；(d) OS 退化 = IS 高而 OS 低（差 > 0.15）→ 降优先级；(e) 分布 5 形状（point_mass / zero_inflated / ceiling / concentrated / spread），zero_inflated 需事件门控；(f) `--recommend` 的综合 score 决定挖掘顺序。

### 拥挤度阈值：五个数，五条轴，别混

| 用途 | 轴 | 阈值 | 出处 |
|---|---|---|---|
| 离线甜点 / 饱和（质量先验） | 数据包里的社区提交量 `count` | 100–3000 甜点；< 50 不可信；> 30000 饱和（打分 ×0.5） | `webdata_quality.py` |
| S0 打分的拥挤罚（软） | 平台 `alphaCount` | ≤ 50 → 0.30；50→500 线性降到 0.15；500→5000 降到 0.02；> 5000 恒 0.02 | `score_datasets.py` / `probe-scoring-v2.md` |
| RA 饱和路由 | 平台 `alphaCount` | ≥ 1 万，或连续 2 波模板全灭 → 切 hypothesis-first | ra-pipeline 步 2 约束 #6（经验值） |
| PPA 硬闸 | 平台 `alphaCount` | ≤ 50（`mode="ppa"`） | `wq-brain-ppa-mining` §1 |
| 校准甜区（opt-in） | 平台 `alphaCount` | 50–1000 | toolkit `--calibrate` |

### 数据包区域覆盖边界（2026-09-17 实测——先看这条再决定能不能预筛）

本地 `WebData_20260219_V0.10.9.zip` **只覆盖 7 个区域：ASI / CHN / EUR / GLB / JPN / KOR / USA**（9 个 `region × delay` 组合，160 条数据集记录、去重 125 个数据集名）。**DEU / IND / GBR / MEA / TWN 等在该包内没有任何条目**——对它们跑预筛只会得到空结果，**不是脚本问题，也不是「忘了跑」**；同一限制也影响体检包生成（`gen_field_inspect_packs.py` 读同一 ZIP）。

**判定顺序**：① 确认目标区域在包内（先用 `--zip` 跑一次看有没有该区的条目）→ ② 在 → 按本节预筛 → ③ **不在** → 改走平台侧（`workflow_campaign(stage="S0")` 的 `recommend_datasets` + `get_datafields`），或先更新 WebDataScope 导出包；并**登记免预筛理由**（下节命令，`--source exempt`）。

## 3. 区域切换预筛门禁（用户 2026-08-05 定的纪律）

**切换区域回测前先预筛**（数据包覆盖的区域）：跑 §2 的命令，读区域级中性化排名、数据集甜点区、⚠ 退化标记与 universe 体检覆盖，再提交批次；包不覆盖的区域按 §2 的判定顺序免预筛并留痕。EUR 2026-08-05 已按此跑过：REVERSION_AND_MOMENTUM 最优 0.668。

**机器自检（工具级，未接入 workflow 节点）**——ra-pipeline 步 2 的前置里调用：

```powershell
& $WQ_PY tools/prescreen_gate.py --region <R>                                             # exit 0 = PASS / 1 = BLOCK
& $WQ_PY tools/prescreen_gate.py --region <R> --record --source webdata_quality --summary '{"neutralization_top":"<NEUT>"}'
& $WQ_PY tools/prescreen_gate.py --region <R> --record --source exempt --summary '{"exempt":"数据包不覆盖该区域"}'
```

判据 = ledger 键 `prescreen_<R>` 存在，或战役目录 `reference/webdata_prescreen_<R>.json` 存在；`--record` 写前一个键（幂等）。它是**自检工具，不是 workflow 节点里的闸**——BLOCK 时先预筛或登记豁免，不要靠别的 waiver 绕过。

## 验证清单（每项写产物）

1. **字段先验已应用**：笔记 / 回报里有前 ~30 字段表（`alphaCount` / `userCount` / `coverage`）与 users 分级标注；饱和数据集显式写「不适用」。
2. **模拟前已预筛**：`webdata_quality.py` 输出的区域级中性化排名表 / 数据集甜点区已读；或该区不在包内且已登记豁免。
3. **切区已过自检**：`prescreen_gate.py --region <R>` 返回 exit 0（PASS）；ledger 存在 `prescreen_<R>` 键（`mcp__wqb-db__get_ledger_key(region, "prescreen_<R>")` 可读）。
