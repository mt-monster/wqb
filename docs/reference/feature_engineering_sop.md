# 标准化特征工程流程（SOP，六阶段）

> **定位**：每个挖掘波次（wave）的特征工程执行规范。字段理解 → 字段筛选 → 预处理决策 →
> 表达式生成 → 质量预估 → 候选池优化，六阶段顺序执行、逐阶段留痕。
> **配套模板**：[feature_engineering_template.md](feature_engineering_template.md)（波级文档，逐阶段对应 §1–§6）。
> **背景**：USA Wave 13-28 实战暴露三大问题——① 字段筛选依赖历史经验无量化依据；
> ② SELF_CORRELATION 无预估导致高质量候选提交时才被 BLOCK（78jZmqJO corr=0.9518）；
> ③ 同数据集反复套模板导致信号同质化（214 个 UNSUBMITTED 中 123 个被本地预估判死）。
> 本 SOP 即针对这三点的结构性修复。最后更新：2026-08-27

---

## 流程总览

```
阶段1 字段理解 → 阶段2 字段筛选 → 阶段3 预处理决策 ─┐
                                                      ├→ ledger_kv s1_<ds>_d<delay>（唯一汇合点）
阶段4 表达式生成（S2，自动读 ledger 注入）────────────┘
     ↓
阶段5 质量预估（回测前本地拦截，零配额）
     ↓
阶段6 候选池优化与门禁（wave_gate.py）→ 五槽填槽回测 → 复盘回写
```

**总纪律**：
- 每阶段产出必须落库或落波级文档，禁止只留在对话记忆
- 白名单外不 generate、不 simulate（S0 数据集白名单 + S1 字段白名单双层）
- 预估工具是**拦截器不是优选器**：能拦高相关/饱和，挑不出尾部赢家，达标仍需实测

---

## 阶段 1：字段理解

| 项 | 内容 |
|---|---|
| 执行者 | `brain-data-feature-engineering` skill（S1）/ `brain-datafield-exploration-general` |
| 数据源 | `mcp__wq-brain-http__get_datafields`、field_catalog 表、`docs/reference/news_bucket_field_map.md` 等字段地图 |
| 产出 | 字段画像表（测什么/怎么测/时间维度/业务背景/信号方向假设）+ 数据集故事 |
| 通过标准 | 每个候选字段有**经济学含义**与**方向假设**，不是照抄平台 description |

**八问驱动**（skill 内置）：不变量/变化/异常/交互/结构/累积/相对/本质——每问至少检视一遍，
生成特征概念后记录逻辑含义与边界条件。

**反模式**：跳过字段理解直接套模板（Wave 23-26 analyst_consensus/pv_tech/pattern_scores 全灭的根因之一：
不了解字段语义就批量套 rank/ts_zscore）。

## 阶段 2：字段筛选

| 项 | 内容 |
|---|---|
| 执行者 | 人工 + 量化证据（本阶段不可纯凭经验） |
| 数据源 | `get_datafields`（覆盖率/更新频率）、`get_datasets`（alphaCount 竞争）、field_catalog、`tools/quality_predict.py` 字段族先验 |
| 产出 | 入选字段表（带依据数值）+ 淘汰字段表（带原因） |
| 通过标准 | 入选字段覆盖率 ≥0.6、更新频率匹配 delay、非同源堆叠 |

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
含 `field_whitelist` 与 `preprocessing`。S2 启动自动注入，不存在绕过通道。

## 阶段 4：表达式生成

| 项 | 内容 |
|---|---|
| 执行者 | `brain-makeSomeGem` skill（S2，headless_runner 入口） |
| 输入 | ledger 注入的 ideas/字段白名单 + `--priors-file`（win/dead_end JSON，RA 战役必带） |
| 产出 | `final_expressions.json` → expressions 表（经 `build_alpha_list.py`） |
| 通过标准 | 概念优先（机制→字段）、每条 1-2 字段、骨架配额达标 |

**生成纪律**：
1. **概念优先**：先写经济机制（收益来源假设），再绑 2-3 个字段；禁止"每字段套 rank/ts_zscore"式遍历
2. **字段数**：每条表达式 1-2 个字段（多字段 = 过拟合 + 相关性双重风险）
3. **骨架配额**（`build_wave.py` 强制）：linear_mix ≤50%，事件门控/分组结构 ≥20%
4. **全历史去重**：防配额浪费（KOR 实测 11% 配额浪费于重复表达式）
5. **同信号禁调权重**：同信号族不达标必须换字段组合（Mode B），禁止权重网格扫描

## 阶段 5：质量预估（回测前本地拦截）

| 项 | 内容 |
|---|---|
| 执行者 | `tools/pool_diversity.py` + `tools/quality_predict.py`（2026-08-27 落地） |
| 成本 | 零平台配额（纯本地结构分析 + 历史先验） |
| 产出 | 六维多样性报告 + 逐候选 EXPECTED_PASS/REVIEW/EXPECTED_BLOCK 判定 |
| 通过标准 | 无 `[GROUP-DOMINANCE]`/`[HOMOG]` 风险；EXPECTED_BLOCK 全部有处理记录 |

**命令**：
```powershell
python tools/pool_diversity.py --region <R> --wave <N> --dataset <DS>
python tools/quality_predict.py --region <R> --wave <N> --dataset <DS>
# 存量池体检：
python tools/quality_predict.py --region <R> --status UNSUBMITTED
```

**EXPECTED_BLOCK 处理**：
- 相关性代理分 ≥0.7（撞存量 alpha）→ 回 Mode B 换字段组合，**禁止调权重重试**
- 字段族饱和（存量同族 ≥30）→ 换数据集或换信号族
- 处理记录写入波级文档 §5 表格

**能力边界（如实）**：预估基于三层先验 Bayes 收缩，预测的是**均值不是尾部**——
PASS=0 不代表没有赢家，只代表先验证据不足；它的价值是拦截必死候选省配额。

## 阶段 6：候选池优化与门禁

| 项 | 内容 |
|---|---|
| 执行者 | `tools/wave_gate.py`（编排器）→ 五槽填槽回测（`pipeline.py`/`wqb-concurrency` §8） |
| 产出 | gate_results 表记录（语法+5闸+六维多样性+质量预估）+ 入批计划 |
| 通过标准 | 语法全过 + 5 闸 all_pass；`--quality-block` 时无 EXPECTED_BLOCK |

**命令**：
```powershell
python tools/wave_gate.py --campaign-dir tracking/<R> --dataset <DS> --wave <N> --from-db --quality-block
```

**入批后**：五槽填槽回测 → 收批入 backtest_results 表 → 波结论写 `wave_results` +
WAVE_LEDGER.md（单入口）→ 复盘回填波级文档 §7（预估 vs 实际偏差），判死/胜绩提炼进
`registry_empirical`（`campaign.py registry` 幂等 CLI）。

---

## 与七阶段战役流水线的映射

| 本 SOP 阶段 | 战役流水线 | 工具/入口 |
|---|---|---|
| 前置白名单 | S0 体检 | `score_datasets.py`、ledger `s0_whitelist` |
| 阶段 1-3 | S1 字段理解 | `brain-data-feature-engineering` → ledger `s1_<ds>_d<delay>` |
| 阶段 4 | S2 生成 + S3 前置 | `brain-makeSomeGem` → `build_wave.py` → expressions 表 |
| 阶段 5 | S3 预检（新增本地层） | `pool_diversity.py` + `quality_predict.py` |
| 阶段 6 | S3 门禁 + 回测 | `wave_gate.py` → 五槽填槽 |
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
