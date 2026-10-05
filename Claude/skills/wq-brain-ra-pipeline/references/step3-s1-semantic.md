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
#   产出 ledger `s1_semantic_<ds>`：
#     signal_fields / blocked_fields / by_category     （L3 语义归类）
#     families / family_stats                          （L3.5 结构族，2026-10-01 新增）

# 批量补跑（2026-10-01 新增；清历史欠账用）：
python tools/field_semantic_classify.py --region $REGION --all --write-ledger
#   默认只跑「有 catalog ∧ 有字段 ∧ 未判死」的活跃集；已有台账的跳过。
#   --dry-run 只列清单 / --force 连已有也重跑。
```

**时间朝向提示（2026-10-04 新增；只提示、不拦截）**：输出里有 `-- 时间朝向提示 --` 一段与台账的 `orientation_stats`：把信号字段标成 `realized`（`actual_*` / `reported_*`，已实现、事后）/ `forecast`（`mean_estimate_*` / `forecast_*` / `consensus_*`，预测、前瞻）/ `mixed`（surprise 之类，两类都命中）。**字段族名要逐词读**：同一数据集里已实现与预测是两个完全不同的信号源——GLB analyst_consensus 前 16 条全灭，真因是选了 `actual_*`（已实现、无预测力），换成 `mean_estimate_*` 后同结构大幅提升；当时被误诊成「窗口不匹配」，多烧了一轮。两类并存时先各出 1 批探针比较，别默认从 `actual_*` 起手。口径是名字词元锚定 + 描述开头，不会拦任何字段（`actual − estimate` 的 surprise 是合法构造）。

**归类口径**（`tools/field_semantic_classify.py` 内可改）：非信号黑名单 = 货币 / 报表币种代码、汇率换算（叉乘多为恒等式）、标识符（country / iso / ticker / cusip / isin / gvkey）、分类码与标志位、日期期间口径、股份类别标签；信号字段按经济大类分桶（valuation / profitability / growth / cash_quality / leverage_solvency / efficiency / liquidity_risk / size_level / per_share / dividend）**+ 技术指标大类**（tech_trend / tech_momentum / tech_volume / tech_volatility）。

> **★ 2026-10-01 两处扩展**（出处：`output_report/field_analysis_demo_model264_20261001.md`）：
> ① **技术指标大类前置**——此前 304 个技术指标（Bollinger / ADL / Amihud / Money Flow / Stochastic）因描述含 `change`/`trend` 被 `growth` 规则抢走，全部误归「成长/趋势」；`TECHNICAL_CATEGORIES` 现插在 `ECON_CATEGORIES` **之前**匹配。实测 `growth` 从 304 → 248，另分出 `tech_volume 24 / tech_trend 20 / tech_momentum 12`。
> ② **L3.5 结构族**——把同源字段（`<前缀>_l1/_l2/_l3/_class/_se`）聚成族，`families` 段输出。**族是 L4 机制推理的最小单位，不是单个字段**。实测 GBR/model264：380 信号字段 → 161 族，其中 **36 个三分类概率族全部齐全**。
>
> **完整方法论（四层漏斗定义、L4 形态构建五步法、三源验证、合规红线）见** [`signal-hypothesis-construction.md`](signal-hypothesis-construction.md)。**L3/L3.5 只划边界、不产信号；信号来自 L4**——不要把本步的字段池当终点。

**fail-closed 的真实范围（单重 + 两处生成侧消费，2026-10-01 修复后）**：

| 位置 | 行为 | 由谁保证 |
|---|---|---|
| 步 5 `tools/wave_gate.py` 闸 SEM | 缺 `s1_semantic_<ds>` → **exit 2 整波阻断**并打印生成命令；命中黑名单字段的表达式**直接剔出候选** | **代码**（`tests/unit/04_gates/test_semantic_gate_failclosed.py`：删闸即红） |
| 步 4 GEM 字段池（`build_economic_field_pool` / `build_candidate_field_pool`） | 建池前按 `s1_semantic_<ds>.blocked_fields` **剔除非信号字段**，payload 带 `semantic_filter` 元数据 | **代码**（`tests/unit/01_store_db/test_semantic_field_pool_filter.py`），**fail-open**：台账缺失即不剔（过滤是减负，不是把关） |
| 步 3 S1 节点（`workflow_campaign(stage="S1")`） | 附带一次语义覆盖检查：缺台账 → 自动跑 `field_semantic_classify.py --write-ledger`（本地零配额秒级） | **代码**（`tests/unit/02_workflow/test_s1_semantic_autoclassify.py`），**fail-open**：脚本失败只 warning |

> ★ **2026-10-01 断流修复（止血 A + 通气 B）**：此前 `s1_semantic_<ds>` 只被步 5 闸 SEM 消费，**
> 生成侧完全不读**——等于「先生成后治理」，非信号字段照样进表达式直到闸才被剔。
> 实测 `IND/insiders1` 的字段池含 `transaction_currency_code` / `insd1_gvkey`（22.2% 是垃圾）。
> 同时实测语义台账覆盖极低：**catalog 697 个 vs s1_semantic 33 个（4.7%）**，EUR/IND/GLB/JPN 全为 0
> ——闸 SEM 在多数区域只能靠「阻断」而非「过滤」生效。
> 现修：① 字段池建池前剔除非信号字段（`POOL_BUILDER_VERSION` 3→4，旧池强制重建）；
> ② S1 默认附带语义归类。**A 依赖 B**——`semantic_filter.ledger=False` 的地方过滤不生效，
> 必须先把该集的语义台账跑出来。

> ★ **清历史欠账（存量批量补跑）**：全区域实测 **409 个活跃集 / 380 个待跑**，一次清掉：
> ```
> for R in USA KOR GBR EUR IND GLB ASI DEU JPN CHN HKG AMR MEA; do
>   python tools/field_semantic_classify.py --region $R --all --write-ledger
> done
> ```
> 口径 =「有 catalog ∧ 有字段 ∧ 未判死」——**幽灵键必须排除**：实测 249 个 `cache_*` 前缀
> 的 catalog 键在 `fields` 表零字段（如 IND/cache_earnings3），只按「有 catalog 键」选会把
> 37% 的工作量浪费在跑不出结果的键上。判死排除复用 `wqb.profile_drift.dead_dataset_index`
> （禁另写一份判死口径）。

> ⚠ 产物是「字段池」，不是 ideas——严禁把本步结果当 `ideas.md` 注入 GEM（同 3.4）。本步约束的是**哪些字段可用**，不是**怎么组合**。

## 3.6 失败分支

| 症状 | 判据 | 处置 |
|---|---|---|
| 字段数太少 | coverage > 0 的字段 < 10 | 回步 2：把该集移出白名单并记因；**< 5 → 仅条件腿**（只作辅助腿 / 事件探针） |
| VECTOR 比例高 | `get_datafields` 确认 | 步 4 必须传对 `data_type` |
| `catalog_<ds>` 覆盖为空 | 铁律 ① | 写 `<ds>_dead`，换集 |
| wave_gate 报缺 `s1_semantic_<ds>` | exit 2 | 跑上面的 classify 命令；不要 `--skip-semantic-gate` 蒙混 |
| 字段池的 `semantic_filter.ledger` 为 `false` | 该集语义台账缺失 | 过滤未生效（fail-open）；跑 `field_semantic_classify.py --write-ledger` 补齐后重建池 |
