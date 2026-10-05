# tracking/mining/ — 共享挖掘数据湖

> **不是区域目录。** `tracking/` 下的 14 个大写三字母目录（`KOR` / `EUR` / `USA` …）才是区域。
> 本目录是**跨区域共享**的体检包与扫描产物池，被 S0–S5 多步复用。
>
> AGENTS.md §1 已声明「勿改动/移动」——本文件是该声明的**索引**，说明里面到底是什么。

## 为什么它平铺在这里（历史原因）

本目录曾同时承担三件事，历史上被逐步塞入，**从未做过子目录化**：

1. S0/S1 的**字段体检包**（`tools/field_inspect_gate.py` 的输入）
2. S2–S4 的**扫描/回测产物池**
3. 少量战役报告（`DEU_D1_*`、`experiment_log.md`）

2026-09 起 `tools/` 已按 `THEMES.json` 下沉、`tracking/<REGION>/scripts/` 已收编区域脚本，
但本目录**刻意保持平铺**——它是数据湖，按文件名前缀自解释比按目录分层更易被工具 glob。
**这是取舍，不是遗漏。**

## 内容构成（1052 文件 / 37.7 MB，其中 JSON 1046）

| 前缀 | 数量 | 是什么 | 谁消费 |
|---|---:|---|---|
| `field_inspect_*` | 490 | **S1 字段体检包**：`{region_delay, neutralization, delay, source, fields}` | `tools/field_inspect_gate.py`（体检硬门） |
| `result_*` | 360 | S2–S4 扫描/回测产物（`result_opt*` / `result_m*` / `result_gbr_*` / `result_submit_*` / `result_nlp_*` / `result_datafields_*` …） | 战役回写、`review_wave` 诊断 |
| `kor_glb_*` | 45 | KOR/GLB 主题变体池产物 | 区域战役回写 |
| `field_coverage_*` | 14 | 字段覆盖率汇总（按 `<REGION>_d_<UNIVERSE>`） | S0 选集、`brain-alpha-research*` |
| `res_mlfp_*` | 14 | MLFP 因子包扫描结果 | Mode B 组合 |
| `rows_mlfp_*` | 13 | MLFP 扫描行 | Mode B 组合 |
| `forum_*` | 5 | 论坛取证快照 | `tools/forum_recon.py` |
| `datasets_*.json` | 3 | 数据集元信息快照（analyst / model / option） | S0 选集参考 |
| 其余（`sentiment_*` / `risk_*` / `option_*` / `children_*` 等） | 102 | 专项扫描产物 | 专项战役 |
| `*.md`（6 个） | 6 | `DEU_D1_TOP500_*` 报告、`experiment_log.md`、`t10v_12_1_submission.md` | DEU 战役复盘 |

**全部为 JSON 产物，无代码。** 少量文件带 UTF-8 BOM（实测前 200 个中 3 个），
读取须用 `encoding="utf-8-sig"`，用 `utf-8` 会抛 `JSONDecodeError`。

## 硬约束

- **§1 禁止改动/移动**。它是跨区共享数据湖，改名会让 20+ 处引用同时断链
  （`AGENTS.md`、`README.md`、`docs/README.md`、4 个 skill、pipeline 的
  `step2-s0.md` / `step5-gates.md` / `scenarios.md` 等）。
- **历史教训**：`21a0e2f` 曾对本目录做瘦身（-248 个参数 dump），
  证明它会被误当成可清理对象。瘦身前先跑
  `git grep -l 'tracking/mining' -- '*.py' '*.md'` 看引用面。
- **2026-10-05 已确认零缺失目录**：受控索引与磁盘完全一致
  （历史上有过 15 个文件「已删未提交」的幽灵索引，见 `f3f3e17`）。

## 相关入口

| 关注点 | 去哪 |
|---|---|
| 字段体检硬门 | `tools/field_inspect_gate.py` |
| 本目录的归属规划 | `tools/THEMES.json`（`tracking` 条目） |
| 数据湖生成器 | `tracking/reference/tooling/generate_manifest.py`（`MANIFEST.json` 当前未生成；注意它会把 >500 KB 文件 zip 到 `tracking/archive/large/`） |
| 目录治理规则 | AGENTS.md §1（职责表）、§8.13（命名/归属） |

维护本目录时：**先查引用、再动手**；产出就地带区域前缀（`field_inspect_eur_*`），
不要发明新的顶层类别。