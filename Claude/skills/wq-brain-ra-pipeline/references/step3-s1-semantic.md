# 步 3（S1）细则：字段扫描 · 结构体检 · 字段语义归类（闸 SEM）

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 3。本步回答三个问题：**字段是什么类型 / 覆盖多少（typed catalog）**、**这个数据集能不能挖（结构体检）**、**这个字段能不能当信号（语义归类）**。

## 3.1 必做：typed catalog + 两条已验证铁律

```
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S1"  dataset=$DS
```

- **产物**：`fields` 表（typed catalog）+ ledger `catalog_<ds>` / `s1_prefix_<ds>`（键契约见 `docs/ledger_keys.json`）。
- **完成定义**：`catalog_<ds>` 里 coverage > 0 的字段数 ≥ 10（见失败分支）。
- **铁律 ①（字段级覆盖审计）**：白名单数据集过 S1 后，`catalog_<ds>` 覆盖为空 → 写 `<ds>_dead` 防复用。`recommend_datasets` **不校验区域覆盖率**，只信它会选到空集。
- **铁律 ②（验活幽灵字段）**：新字段先 `create_multi_simulation(validate_fields=true)`——DB 里有记录、平台却报 `Attempted to use unknown variable` 的字段，提交层直接 COMPILE_ERROR。
- **铁律 ③（混合集的 `data_type` 与字段类型；2026-10-02 GLB analyst69 事故）**：`catalog_<ds>.data_type` 是数据集级汇总（多数票折叠），**对混合集是错的**——analyst69 在 GLB 是 VECTOR 515 + MATRIX 264（`type_distribution`），汇总成 `VECTOR`，GEM 照 VECTOR 语义生成、候选直接用裸 VECTOR 字段，闸 `[EVENT]` 24/24 全灭（同一数据集在 JPN 汇总成 MATRIX，同波号跨区两态）。规则：① 开波前看 `catalog_<ds>.type_distribution`，同时含 VECTOR 与 MATRIX 的混合集，传给 GEM 的 `data_type` 必须人工裁决为「本波要挖的字段池主类型」（挖分析师基本面估计 → MATRIX；挖评级 / 事件列表 → VECTOR 并强制 `vec_*` 包裹），不得直接吃汇总值；② 字段类型的**权威源 = typed catalog**（toolkit `_lib/wqb_store.load_catalog`，与闸 3 同源），不是 MCP `fix_vector_fields` 的回包（清单只有 300 个，缺整族）、不是本地 `fields` 表（可能没有该集记录）；③ 裸 VECTOR 的统一包裹用 `tools/lib/vector_wrap.py::wrap_naked_vectors`（幂等）；④ 波级修复的成员口径要与 gate 一致——`status IN ('gem','selected')`，只修本轮新生成的那批会漏掉旧入选的。
- 深查 / 字段质量存疑时**按需**加载 S1 三件套：[`brain-dataset-exploration-general`](../../brain-dataset-exploration-general/SKILL.md)（数据集级）→ [`brain-datafield-exploration-general`](../../brain-datafield-exploration-general/SKILL.md)（单字段 6 法）→ [`brain-data-feature-engineering`](../../brain-data-feature-engineering/SKILL.md)（字段→特征工程决策）。三件套只作深查参考；**上面两条铁律是本步必做检查项，不是参考**。

## 3.2 S1 结构性前置体检（决策表 D13；MEA / KOR 多区实证）

| 检查项 | 判据 / 动作 |
|---|---|
| 小宇宙（TOP400 / TOP500）VECTOR 字段 | 挖前必查 longCount ≥ 80（cov 0.85 但 longCount 11–16 = 伪白空间，MEA f72 实证）；以决策表 D13 为准（profile 不再有 `longcount_min` 键：它等同全局默认、且没有代码读取） |
| 稀疏事件流字段（论坛评论 / 行为 / 事件计数） | 预期 CW 1.0 结构性无解（KOR 三族实证）——先单仿真探针看 CW 再投整批；勿期望 backfill 救活 |
| 新数据集首批 | 先 1 条单仿真探针验证字段可用性（元数据类型可能标错：MEA fundamental6 标 VECTOR 实为 EVENT → 整批 ERROR） |
| 字段批内连坐预防 | 不确定字段隔离到独立小批；一个坏字段会 CANCEL 整批 8 条 |
| 低 alphaCount 白空间判定 | 小宇宙中 alphaCount ≤ 50 可能是「没人能用」而非「没人挖过」——交叉验证 userCount / longCount |

## 3.3 字段分级风险筛查（prod-corr 规避）

`mcp__wq-brain-http__get_datafields` 后按 `users` 分级（**经验阈值**，出处 [`prod-corr-avoidance.md`](prod-corr-avoidance.md) 的 GLB 2026-08 实验；已确认超标的字段族登记在 `registry_empirical` 的 dead_end 层）：

| users | 处置 |
|---|---|
| ≥ 50 | 只做信号方向验证，不投入候选打磨（prod_corr 必超） |
| 10–49 | 进候选池；提交前必须实测 prod_corr |
| 0–9 | 优先候选池（理论 prod_corr ≈ 0）；冷门字段占批次预算 ≥ 50% |

已确认超标的字段族（如 GLB techindi `predicted_first_quantile_ten_day_return_*`）不再投任何变体。

## 3.4 深度字段理解（`workflow_feature_engineering`）：按需 · 仅人读 · **禁注入 GEM**

该节点产出的是**确定性模板渲染**（8 问框架 + `rank(ts_mean({f},66))`），**不含 LLM 推理**。把它当 ideas 喂给 GEM，GEM 会一行 LLM 都不调、整波退化为模板展开（GBR intraday_pv_feats 实证）。因此：
① 不是必做项（节点与 runner 已主动跳过 `source ∈ {feature_engineering_node, standalone*}` 的模板文档）；② 产物仅供人读；③ 禁止注入 GEM（需要覆盖须显式传 `ideas_file`）。生成侧的唯一入口是步 4 的概念优先 GEM + priors 注入。

## 3.5 字段语义归类（闸 SEM；GEM 之前必做；本地、零配额、秒级）

**为什么**：typed catalog 只回答「类型 / 覆盖 / 多少人在用」，**不回答「这字段能不能当信号」**。KOR/fundamental17 首波跳过语义归类的代价：348 条产物里 49.4% 落在货币代码 / 汇率叉乘这类**非信号字段**上（语法全对、语义全废，语法闸与 `gate.py` 都拦不住），而黑名单字段仅占全部字段 9.9%（37/373）。

```
python tools/field_semantic_classify.py --region $REGION --dataset $DS --write-ledger
#   产出 ledger `s1_semantic_<ds>`：signal_fields / blocked_fields / by_category
```

**时间朝向提示（2026-10-04 新增；只提示、不拦截）**：输出里有 `-- 时间朝向提示 --` 一段与台账的 `orientation_stats`：把信号字段标成 `realized`（`actual_*` / `reported_*`，已实现、事后）/ `forecast`（`mean_estimate_*` / `forecast_*` / `consensus_*`，预测、前瞻）/ `mixed`（surprise 之类，两类都命中）。**字段族名要逐词读**：同一数据集里已实现与预测是两个完全不同的信号源——GLB analyst_consensus 前 16 条全灭，真因是选了 `actual_*`（已实现、无预测力），换成 `mean_estimate_*` 后同结构大幅提升；当时被误诊成「窗口不匹配」，多烧了一轮。两类并存时先各出 1 批探针比较，别默认从 `actual_*` 起手。口径是名字词元锚定 + 描述开头，不会拦任何字段（`actual − estimate` 的 surprise 是合法构造）。

**归类口径**（`tools/field_semantic_classify.py` 内可改）：非信号黑名单 = 货币 / 报表币种代码、汇率换算（叉乘多为恒等式）、标识符（country / iso / ticker / cusip / isin / gvkey）、分类码与标志位、日期期间口径、股份类别标签；信号字段按经济大类分桶（valuation / profitability / growth / cash_quality / leverage_solvency / efficiency / liquidity_risk / size_level / per_share / dividend）。

**fail-closed 的真实范围（单重 + 一项人工约定，不是「双重」）**：

| 位置 | 行为 | 由谁保证 |
|---|---|---|
| 步 5 `tools/wave_gate.py` 闸 SEM | 缺 `s1_semantic_<ds>` → **exit 2 整波阻断**并打印生成命令；命中黑名单字段的表达式**直接剔出候选** | **代码**（`tests/unit/04_gates/test_semantic_gate_failclosed.py`：删闸即红） |
| 步 4 GEM `economic_field_pool_check` | 自己用 `build_economic_field_pool` 建字段池（缓存命中则沿用旧池），**并不读 `s1_semantic_<ds>`**，也不会因它失败 | **无代码保证**——不要以为 GEM 侧已过滤 |

「把语义干净的字段重排回 GEM 字段池」（写 `s2_field_pool_<ds>`）目前**没有任何命令**实现，属人工约定；它不是安全网。**最容易被绕过的一处就是这里**——过滤只在闸 SEM 才真正落地。

**模式**：`--semantic-gate {off,warn,enforce}` / `WQB_SEM_MODE`，**缺省 `enforce`**。`off`（= `--skip-semantic-gate`）是唯一逃生口，必须显式传、会打印醒目告警，且须先有 `semantic` waiver（AGENTS.md §8.1.2）；`warn` = 缺台账仅告警（黑名单剔除仍生效）。三个同构闸的缺省不同（SEM enforce / 体检 warn / 区域闸按日期），见 [INDEX 总表](../../INDEX.md)。

> ⚠ **产物是「字段池」，不是 ideas**——严禁把本步结果当 `ideas.md` 注入 GEM（同 3.4）。本步约束的是**哪些字段可用**，不是**怎么组合**。

## 3.6 失败分支

| 症状 | 判据 | 处置 |
|---|---|---|
| 字段数太少 | coverage > 0 的字段 < 10 | 回步 2：把该集移出白名单并记因；**< 5 → 仅条件腿**（只作辅助腿 / 事件探针） |
| VECTOR 比例高 | `get_datafields` 确认 | 步 4 必须传对 `data_type` |
| `catalog_<ds>` 覆盖为空 | 铁律 ① | 写 `<ds>_dead`，换集 |
| wave_gate 报缺 `s1_semantic_<ds>` | exit 2 | 跑上面的 classify 命令；不要 `--skip-semantic-gate` 蒙混 |
