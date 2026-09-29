---
name: brain-datafield-exploration-general
layer: L1
description: "对单个 datafield 做定性评测：覆盖率、非零率、更新频率、取值范围、中心趋势、分布形态六种方法，先查离线体检包、再用最小仿真集在线复核，并给出每法「测完怎么用」。要弄清某个字段多久更新、值域多大、能不能当信号时使用；只测不决策，测完交特征工程。"
last_verified: 2026-09-29
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# 评估新数据字段的 6 种方法

## 职责边界

- **本 skill 负责**：**单字段级**定性评测——覆盖 / 非零 / 更新频率 / 取值范围 / 中心趋势 / 分布形态六法，以及每法「测完交给谁」的映射。
- **本 skill 不做**：不选数据集（上游已定）；不做特征工程决策（→ [`brain-data-feature-engineering`](../brain-data-feature-engineering/SKILL.md)）；不生成表达式；不做全量字段收割（→「批量字段收割」一节）。
- **上游 / 下游**：上游 = [`brain-dataset-exploration-general`](../brain-dataset-exploration-general/SKILL.md) 抽出的关键字段；下游 = 特征工程第 0 / 2 步的字段画像与预处理决策、步 3 的 S1 字段白名单。

## 0. 先离线后在线；在线要合批、要算成本

**离线优先（零配额）**：体检包 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`（`tools/gen_field_inspect_packs.py` 产出，只覆盖 ASI / CHN / EUR / GLB / JPN / KOR / USA 七区）里每个字段的 `metadata` 已含 `coverage_ratio` / `skewness` / `kurtosis` / `frequency` / `distribution_shape` / `min_window` / `recommended_decay` / `recommended_truncation`，另有 `advices`：

```powershell
& $WQ_PY -c "import json; d=json.load(open('tracking/mining/field_inspect_<region>_<ds>.json',encoding='utf-8'))['fields']['<ds>']['<field>']; print(d['metadata']); print(d['advices'])"
```

六法里**法 1（覆盖）、法 3（频率）、法 6（分布形态）在包里有现成答案**；法 2、4、5 没有直接对应。缺包 / 区域不在包内 → 在线。

**在线最小仿真集**（一个字段全跑六法 ≈ 15 条仿真 ≈ 2 批，**别对整个数据集逐字段全跑**——1000+ 字段的集只对 dataset-exploration §1 抽出的 Top-N 字段在线复核）：

| 集 | 内容 | 条数 |
|---|---|---|
| **最小集（一批）** | 法 1、法 2、法 3 的 N = 5 / 22 / 66、法 4 的 X = 1 | 6 |
| 扩展集（再一批，仅对将当主信号的字段） | 法 4 的 X = 10 / 100、法 5 的 X = 0 / 1、法 6 的 2–3 个刻度 | ≤ 8 |

- **合批**：`mcp__wq-brain-http__create_multi_simulation`（单次 2–10 条，本仓库标准批 8 条）。**multisim 是连坐语义**——批内任一条 ERROR，其余全部 CANCELLED（toolkit §11）；且该入口有**静态门禁**（语法 / 不可访问算子 / 毒模式），任一条不过就整批拒绝。所以只用**已在平台算子目录（103 个）里的算子**、只写本仓库文法认得的语法（**没有 `? :` 三元**——原帖的 `datafield != 0 ? 1 : 0` 会被拒，比较式本身就返回 0 / 1，直接写 `datafield != 0`）；字段类型没把握（VECTOR / EVENT）先做**单条**探针（`rank(field)` → `rank(vec_avg(field))`），再合批。
- **设置**：Neutralization `None`、Decay `0`、Test Period `P0Y0M0D`（「无测试期」的规范写法；旧文的 `P0Y0M` 也被接受，`P6Y` 是真实 6 年测试期，别混）；region / delay / universe 与目标战役一致（`config.REGIONS[<R>]`）。看 IS Summary 的 **Long Count** 与 **Short Count**。
- **不入库**：手工 `create_multi_simulation` 不经 `workflow_batch_track` / `harvest_*`，不写 `backtest_results`，不进战役统计（除非你自己去 harvest）；与在跑的战役批**共用账户并发上限**，先 `workflow_task_status` 看有没有批在跑。结论写进对话 / `reports/`，不要为它们造战役波。

## 法 1：基础覆盖率
- **表达式**：`datafield`（VECTOR 先 `vec_*` 聚合，见「类型先行」一节；下同）
- **解读**：覆盖率 % ≈（Long Count + Short Count）/ 股票池大小（IS Summary 里的 Universe Size）。
- **→ 交 FE**：`coverage < 0.4` → 必须 `ts_backfill` / `group_backfill`（体检硬门检查 1）；写进 FE 第 2 步字段画像的「覆盖率」与预处理决策。

## 法 2：非零值覆盖率
- **表达式**：`datafield != 0`
- **解读**：剔除零值后的真实覆盖。与法 1 的计数差大 = 字段大量为 0（缺失与真零区分开）。
- **→ 交 FE**：零占比高（体检 `distribution_shape` = `zero_inflated` / `point_mass`）是**稀疏事件**——用 `trade_when` 门控，不要直接 `rank`（体检硬检查会拦）。

## 法 3：更新频率
- **表达式**：`ts_std_dev(datafield, N) != 0`，N = 5 / 22 / 66
- **解读**：把它读作「最近 N 天内值变过」，N 越大越容易为真。**日更**字段：三个 N 的计数都≈覆盖；**季更**字段：N = 66 时计数接近覆盖，N = 22 约 1/3，N = 5 更低；周更 / 月更介于其间。
- **→ 交 FE**：频率决定**窗口下限**——读体检包的 `min_window`；硬门的代码口径是 daily ≥ 22（流量 / 事件类 daily 字段降为 5）/ weekly ≥ 52 / monthly ≥ 120 / quarterly ≥ 252（WebDataScope 规则 13 的 21d / 63d 是理论下限，见 field-quality 的规则文档）。低频字段换手天然低，走低换手轨道。

## 法 4：取值范围
- **表达式**：`abs(datafield) > X`，X = 1 / 10 / 100（按量纲继续放大）
- **解读**：X = 1 时计数≈覆盖 → 字段落在 [-1, 1]（已归一化）；逐档放大 X 直到计数归零，得到量纲。
- **→ 交 FE**：量纲跨度大 → 用 `rank` / `ts_zscore` / `ts_rank` 去量纲，**不要**把不同量纲的字段直接相加（尺度支配 = 事实上的混信号）；有界 [-1, 1] 的评分类字段可直接 `rank`。

## 法 5：中心趋势
- **表达式**：`ts_mean(datafield, 252) > X`（252 = 1 年；要 4 年典型值用 `ts_mean(datafield, 1008)`）
- **解读**：X = 0 看是否为正；逐档 X = 1 / 10 找中心尺度。**不要用 `ts_median`**——它是幽灵算子，用了会取消整批 multisim；均值受偏态影响，偏态大时与法 6 / 体检 `skewness` 对照读。
- **→ 交 FE**：单边（恒正 / 恒负）字段先取变化率（`ts_delta` / `ts_returns`）或 `ts_zscore` 再用（体检 advice「单边恒正 → 变化率 / 排名」）。

## 法 6：分布形态
- **离线首选**：体检包 `distribution_shape`（`point_mass` / `zero_inflated` / `ceiling` / `concentrated` / `spread`）+ `skewness` / `kurtosis`。
- **在线复核**：`zscore(datafield) > k`，k = -1 / 0 / 1 / 2。与正态参考比（**占覆盖的比例**：k = -1 → 84%，0 → 50%，1 → 16%，2 → 2.3%）：k = 0 远低于 50% → 右偏；k = 2 远高于 2.3% → 右尾厚。旧文用的 `scale_down` **不在本账号 103 个已验证算子里**（用它需先 `get_operators` 确认可用；未确认前不进 multisim）。这条在线读法**没有在本仓库实测过**（平台不可达），以离线形态为准。
- **→ 交 FE**：形态直接决定预处理：`ceiling` / `concentrated` → `winsorize` / `rank`；`zero_inflated` / `point_mass` → `trade_when`；厚尾 → `ts_zscore` 之前先截尾（`recommended_truncation` 可参考）。

## 类型先行：MATRIX / VECTOR / EVENT / GROUP（先看 `get_datafields` 返回的 `type`）

| `type` | 规则 |
|---|---|
| MATRIX | 直接用，**不要**包 `vec_*`（闸 3 报 `[TYPE]`） |
| **VECTOR** | 最内层**必须**先 `vec_*`（缺省 `vec_avg`；计数 / 求和类用 `vec_sum`；目录内还有 `vec_max` / `vec_min` / `vec_count` / `vec_stddev` / `vec_range`）再进 `rank` / `ts_*` / `winsorize`。裸用 → 平台 HTTP 400 `winsorize does not support event inputs`（报错措辞里的 event 指 VECTOR 输入，见 `fix_vector_fields` 的说明）。自动修复：`mcp__wq-brain-http__fix_vector_fields` / `preflight_expressions(auto_fix_vector=true)` |
| **EVENT**（`type==EVENT`） | 闸 8 直接 FAIL。**平台没有 `ts_event_*` 系列**（KOR wave16 实测 8/8 ERROR；旧文推荐的 `ts_event_sum/count/mean` 不存在）——先做**单条探针**（toolkit §11：`rank(field)` → 逐层加），探通再放量 |
| GROUP | 只作 `group_*` 算子的分组参数，六法不适用 |

**旧文（2026-09-29 前）与此相反**：它写「VECTOR 直接用、不要 `vec_*`、`winsorize` 安全」「EVENT 先 `ts_event_*` 转成 VECTOR」——两条都被闸 3 / 闸 8 与平台报错否定（KOR 的 short-interest / special-returns / insider / news 数据集，字段元数据标 VECTOR 却裸用 `winsorize`，整批报错），已更正。

## 批量字段收割：指针 + 一个陷阱

本 skill 适合**单字段定性**。全量字段收割走 `wq-brain-campaign-toolkit` 的 `scan_fields.py`，落 typed catalog（DB `fields` 表 / `reference/<region>_<dataset>_fields.json`：type / coverage / userCount / alphaCount）——它是 toolkit 闸 2 / 3 的数据源。

| 症状 | 原因 | 规避 |
|---|---|---|
| `GET /data-fields` 带 `dataset=<id>` 返回全宇宙（10000 条上限） | 平台**静默忽略**裸 `dataset=` | 用 `dataset.id=<id>`（KOR 2026-08-15 实测）。MCP `get_datafields` 已封装（传 `dataset_id`），只在手写 REST 时会踩 |

## 验证清单（每项写产物）

1. **先离线**：回报里有该字段体检包的 `metadata`（或注明该区 / 该集不在包内）。
2. **在线有成本意识**：只跑了最小集（一批 6 条）；扩展集只对将当主信号的字段跑；没有为整个数据集逐字段全跑。
3. **类型已核**：字段 `type` 已写明，VECTOR 已 `vec_*`、EVENT 已单条探针；表达式里没有 `ts_median` / `ts_event_*` / `scale_down`。
4. **每法有去向**：每个结论带「→ 交 FE 的哪一步」（覆盖 → backfill、频率 → 窗口下限、形态 → 预处理）。

## references

| 文件 | 何时读 |
|---|---|
| [`reference.md`](reference.md) | 要看六法的出处、MATRIX / VECTOR 两种写法对照、原帖的验证例时 |
