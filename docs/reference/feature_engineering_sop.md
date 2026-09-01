# 标准化特征工程流程（SOP，六阶段）

> **定位**：每个挖掘波次（wave）的特征工程执行规范。字段理解 → 字段筛选 → 预处理决策 →
> 表达式生成 → 质量预估 → 候选池优化，六阶段顺序执行、逐阶段留痕。
> **配套模板**：[feature_engineering_template.md](feature_engineering_template.md)（波级文档，逐阶段对应 §1–§6）。
> **背景**：USA Wave 13-28 实战暴露三大问题——① 字段筛选依赖历史经验无量化依据；
> ② SELF_CORRELATION 无预估导致高质量候选提交时才被 BLOCK（78jZmqJO corr=0.9518）；
> ③ 同数据集反复套模板导致信号同质化（214 个 UNSUBMITTED 中 123 个被本地预估判死）。
> 本 SOP 即针对这三点的结构性修复。最后更新：2026-09-01（S1 前缀聚类与 S2 候选字段池强制化）

---

## 流程总览

```
阶段1 字段理解 → 阶段2 字段筛选 → 阶段3 预处理决策 ─┐
                                                      ├→ ledger_kv s1_<ds>_d<delay>（唯一汇合点）
阶段4 表达式生成（S2，自动读 ledger 注入）────────────┘
     ↓
阶段5 质量预估（回测前本地拦截，零配额）
     ↓
阶段6 候选池优化与门禁（wave_gate.py）→ 七槽填槽回测 → 复盘回写
```

**总纪律**：
- 每阶段产出必须落库或落波级文档，禁止只留在对话记忆
- 白名单外不 generate、不 simulate（S0 数据集白名单 + S1 字段白名单双层）
- S1 必须生成 `s1_prefix_<dataset>` 前缀聚类摘要，S2 必须生成 `s2_field_pool_<dataset>` 候选字段池
- GEM 必须消费 `s1_<dataset>_d<delay>.field_whitelist`；该白名单应优先来自 `s2_field_pool_<dataset>`
- 预估工具是**拦截器不是优选器**：能拦高相关/饱和，挑不出尾部赢家，达标仍需实测

---

## 阶段 1：字段理解

| 项 | 内容 |
|---|---|
| 执行者 | `brain-data-feature-engineering` skill（S1）/ `brain-datafield-exploration-general` |
| 数据源 | `mcp__wq-brain-http__get_datafields`、field_catalog 表、`docs/reference/news_bucket_field_map.md` 等字段地图 |
| 产出 | 字段画像表（测什么/怎么测/时间维度/业务背景/信号方向假设）+ 数据集故事 + `s1_prefix_<dataset>` 前缀聚类摘要 |
| 通过标准 | 每个候选字段有**经济学含义**与**方向假设**，不是照抄平台 description；字段规模过大时必须输出前缀聚类摘要而非全量字段清单 |

**八问驱动**（skill 内置）：不变量/变化/异常/交互/结构/累积/相对/本质——每问至少检视一遍，
生成特征概念后记录逻辑含义与边界条件。

**前缀聚类摘要（强制）**：字段数较大时，S1 不再输出全量字段清单，必须基于 field catalog 生成
`s1_prefix_<dataset>`，至少包含 `top_clusters`、`risk_clusters`、`sample_fields`、`coverage_mean/median`。
该摘要写入 `ledger_kv`，供 S2 派生候选字段池与后续审计复用。

**反模式**：跳过字段理解直接套模板（Wave 23-26 analyst_consensus/pv_tech/pattern_scores 全灭的根因之一：
不了解字段语义就批量套 rank/ts_zscore）。

## 阶段 2：字段筛选

| 项 | 内容 |
|---|---|
| 执行者 | 人工 + 量化证据（本阶段不可纯凭经验） |
| 数据源 | `get_datafields`（覆盖率/更新频率）、`get_datasets`（alphaCount 竞争）、field_catalog、`tools/quality_predict.py` 字段族先验 |
| 产出 | 入选字段表（带依据数值）+ 淘汰字段表（带原因） + `s2_field_pool_<dataset>` 候选字段池 |
| 通过标准 | 入选字段覆盖率 ≥0.6、更新频率匹配 delay、非同源堆叠；候选字段池必须优先来自 `s1_prefix_<dataset>` 的非风险簇代表字段 |

**量化筛选标准**（逐字段留证据）：
1. **覆盖率** ≥0.6（低于则信号稀疏，回测易出 SUB_UNIVERSE 问题）
2. **更新频率**：daily 字段适配 delay1 短线逻辑；季度慢变量只做长窗口/门控
3. **平台竞争**：数据集 alphaCount 过高（>数万）且字段族已有存量达标 alpha → 族饱和预警
4. **历史先验**：字段族历史回测均值远低于闸门 → 需要结构创新理由才入池
5. **同源检查**：同模型输出的多个字段（如 `*_1/*_2/*_3` 系列）最多选 1-2 个，
   组合必撞 SELF_CORRELATION

**反模式**：
- "上一波用了这个字段所以继续用"——必须补当期证据
- 同模型系列字段全入池再两两组合（USA 214 存量中 52 条 score≥0.99 的同质对即此产物）

## 阶段 3：预处理决策

| 项 | 内容 |
|---|---|
| 执行者 | 人工决策，skill 生成 ideas 时同步产出 |
| 产出 | 字段→预处理链映射表 + 决策依据 |
| 通过标准 | 硬性规则检查清单全过（见模板 §3）+ **写入 ledger** |

**硬性规则**（违反即表达式层失败）：
- EVENT 字段禁 winsorize（`ts_event_*` 或裸 rank）
- VECTOR 字段必须 `vec_*` 聚合（`tools/lib/vector_wrap.py` 幂等包裹）
- 稀疏字段先 `ts_backfill`；非平稳字段 `rank`/`ts_zscore`
- 需要截面标准化时优先 `group_zscore`/`group_rank`（同时满足多样性闸门要求）

**入库（强制）**：`mcp__wqb-db__upsert_ledger_key(region, "s1_<dataset>_d<delay>", {...})`，
含 `field_whitelist`、`candidate_field_pool`、`field_prefix_summary` 与 `preprocessing`。
其中 `field_whitelist` 必须优先等于 `s2_field_pool_<dataset>` 中的候选字段池；S2 启动自动注入，不存在绕过通道。

## 阶段 4：表达式生成

| 项 | 内容 |
|---|---|
| 执行者 | `brain-makeSomeGem` skill（S2，headless_runner 入口） |
| 输入 | ledger 注入的 ideas/字段白名单 + `--priors-file`（win/dead_end JSON，RA 战役必带） |
| 产出 | `final_expressions.json` → expressions 表（经 `build_alpha_list.py`） |
| 通过标准 | 概念优先（机制→字段）、每条 1-2 字段、骨架配额达标；字段绑定必须受 `s1_<dataset>_d<delay>.field_whitelist` 约束 |

**生成纪律**：
1. **概念优先**：先写经济机制（收益来源假设），再绑 2-3 个字段；禁止"每字段套 rank/ts_zscore"式遍历
2. **字段数**：每条表达式 1-2 个字段（多字段 = 过拟合 + 相关性双重风险）
3. **骨架配额**（`build_wave.py` 强制）：linear_mix ≤50%，事件门控/分组结构 ≥20%
4. **全历史去重**：防配额浪费（KOR 实测 11% 配额浪费于重复表达式）
5. **同信号禁调权重**：同信号族不达标必须换字段组合（Mode B），禁止权重网格扫描
6. **字段池约束**：GEM 只能优先从 `s1_<dataset>_d<delay>.field_whitelist` 绑字段；该白名单应来自 `s2_field_pool_<dataset>`，禁止绕过候选字段池自由发挥

## 阶段 5：质量预估（回测前本地拦截）

| 项 | 内容 |
|---|---|
| 执行者 | `tools/pool_diversity.py` + `tools/quality_predict.py`（2026-08-27 落地，2026-08-31 分层阈值升级） |
| 成本 | 零平台配额（纯本地结构分析 + 历史先验） |
| 产出 | 六维多样性报告 + 逐候选分层判定（DIRECT_SUBMIT/COMBO_CANDIDATE/WEAK_SIGNAL/EXPECTED_BLOCK/HARD_REJECT） |
| 通过标准 | 无 `[GROUP-DOMINANCE]`/`[HOMOG]` 风险；EXPECTED_BLOCK 全部有处理记录 |

**命令**：
```powershell
python tools/pool_diversity.py --region <R> --wave <N> --dataset <DS>
python tools/quality_predict.py --region <R> --wave <N> --dataset <DS>
# 存量池体检：
python tools/quality_predict.py --region <R> --status UNSUBMITTED
```

**分层阈值体系（2026-08-31 新增）**：

| 层级 | 判定 | 阈值 | 用途 |
|:---|:---|:---|:---|
| **DIRECT_SUBMIT** | 优选线达标 | S≥1.58, F≥1.0, prod_corr<0.7 | 直接提交 |
| **COMBO_CANDIDATE** | 候选池达标 | S≥1.0, F≥0.8, T≤0.4, prod_corr<0.7 | 组合腿候选 |
| **WEAK_SIGNAL** | 弱信号 | S 0.5-1.0 或 F 0.3-0.8 | 谨慎考虑 |
| **EXPECTED_BLOCK** | 相关性超标 | prod_corr≥0.7 | 需组合稀释 |
| **HARD_REJECT** | 硬拒绝 | S<0.5 或 F<0.3 | 直接丢弃 |

**分层判定逻辑**（相关性优先，避免高 Sharpe 信号被 Turnover 误杀）：
1. 相关性检查（prod_corr ≥ 0.7）→ EXPECTED_BLOCK
2. 硬拒绝线（S<0.5 或 F<0.3）→ HARD_REJECT
3. 优选线（S≥1.58 且 F≥1.0）→ DIRECT_SUBMIT
4. 候选池线（S≥1.0 且 F≥0.8 且 T≤0.4）→ COMBO_CANDIDATE
5. 其他 → WEAK_SIGNAL

**EXPECTED_BLOCK 处理**：
- 相关性代理分 ≥0.7（撞存量 alpha）→ 回 Mode B 换字段组合，**禁止调权重重试**
- 字段族饱和（存量同族 ≥30）→ 换数据集或换信号族
- 处理记录写入波级文档 §5 表格

**COMBO_CANDIDATE 处理**（2026-08-31 新增）：
- 标记为组合腿候选，进入组合优化流程
- 优先与 prod_corr<0.3 的其他候选组合（稀释相关性）
- 组合策略详见 `docs/reference/combination_optimization_strategy.md`

**能力边界（如实）**：预估基于三层先验 Bayes 收缩，预测的是**均值不是尾部**——
PASS=0 不代表没有赢家，只代表先验证据不足；它的价值是拦截必死候选省配额。

## 阶段 6：候选池优化与门禁

| 项 | 内容 |
|---|---|
| 执行者 | `tools/wave_gate.py`（编排器）→ 七槽填槽回测（`pipeline.py`/`wqb-concurrency` §8） |
| 产出 | gate_results 表记录（语法+5闸+六维多样性+分层质量预估）+ 入批计划 |
| 通过标准 | 语法全过 + 5 闸 all_pass；`--quality-block` 时无 EXPECTED_BLOCK/HARD_REJECT |

**命令**：
```powershell
python tools/wave_gate.py --campaign-dir tracking/<R> --dataset <DS> --wave <N> --from-db --quality-block
```

**门禁报告格式（2026-08-31 新增）**：
```
[qp   ] 质量预估: DIRECT=2 COMBO=8 WEAK=15 BLOCK=5 HARD=3（拦截 8 条计入 FAIL）
[done ] 语法 22/22, gate all_pass=True passed=22/22 质量预估 D/C/W/B/H=2/8/15/5/3 => PASS
```

**分层结果解读**：
- **D (DIRECT_SUBMIT)**: 优选线达标，可直接提交
- **C (COMBO_CANDIDATE)**: 候选池达标，可作为组合腿
- **W (WEAK_SIGNAL)**: 弱信号，需谨慎考虑
- **B (EXPECTED_BLOCK)**: 相关性/饱和度超标，需 Mode B 处理
- **H (HARD_REJECT)**: 硬拒绝线以下，直接丢弃

**入批后**：七槽填槽回测 → 收批入 backtest_results 表 → 波结论写 `wave_results` +
WAVE_LEDGER.md（单入口）→ 复盘回填波级文档 §7（预估 vs 实际偏差），判死/胜绩提炼进
`registry_empirical`（`campaign.py registry` 幂等 CLI）。

---

## 与七阶段战役流水线的映射

| 本 SOP 阶段 | 战役流水线 | 工具/入口 |
|---|---|---|
| 前置白名单 | S0 体检 | `score_datasets.py`、ledger `s0_whitelist` |
| 阶段 1-3 | S1 字段理解 | `brain-data-feature-engineering` → ledger `s1_<ds>_d<delay>` + `s1_prefix_<ds>` |
| 阶段 4 | S2 生成 + S3 前置 | `brain-makeSomeGem` + ledger `s2_field_pool_<ds>` → `build_wave.py` → expressions 表 |
| 阶段 5 | S3 预检（新增本地层） | `pool_diversity.py` + `quality_predict.py` |
| 阶段 6 | S3 门禁 + 回测 | `wave_gate.py` → 七槽填槽 |
| 复盘 | S4-S6 | judge / 优化器 / `wq-backtest-monitor` + registry 回写 |

## 反模式清单（血泪汇总）

| 反模式 | 实证案例 | 本 SOP 对策 |
|---|---|---|
| 字段筛选只凭历史经验 | Wave 23-26 四数据集全灭 | 阶段 2 量化证据表必填 |
| SELF_CORRELATION 无预估 | 78jZmqJO corr=0.9518 提交才 BLOCK | 阶段 5 相关性代理分 |
| 同模型系列字段全组合 | 214 存量中 52 条 score≥0.99 同质对 | 阶段 2 同源检查 |
| 同信号调权重变体 | 纪律明令禁止 | 阶段 4/5 BLOCK→Mode B |
| 跳过预估直接烧配额 | 配额浪费于必死候选 | 阶段 5 强制零配额预检 |
| 文档只写策略不写依据 | Wave 28 之前文档无法审计 | 模板〔必填〕节 + 淘汰原因表 |
| 单字段阈值过严误杀组合潜力股 | IND 112 回测仅 3 个达标且全被拒 | 阶段 5 分层阈值（COMBO_CANDIDATE） |
| 高 Sharpe 信号被 Turnover 误杀 | wpjvE8W5 S=2.61 但 T=0.79 被 HARD_REJECT | 阶段 5 判定顺序优化（相关性优先） |
