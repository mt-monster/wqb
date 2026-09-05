---
title: RA 挖掘战役启动提示词模板（区域无关）
doc_type: prompt_template
layer: reference
region_var: $REGION
dataset_var: $DATASET
orchestrator: wq-brain-ra-pipeline
last_verified: 2026-09-04
ai_callable: true
variables:
  - name: $REGION
    desc: 战役区域（KOR/EUR/USA/IND/ASI/GBR/DEU/CHN/JPN/GLB）
  - name: $DATASET
    desc: 目标数据集（S-PRE 查表选定，或候选指定）
  - name: $DS
    desc: 同 $DATASET（流水线内简写）
  - name: $DELAY
    desc: 数据延迟（0 或 1，读 settings.json）
  - name: $UNIVERSE
    desc: 股票池（读 settings.json）
  - name: $W
    desc: 当前波号
---

# RA 挖掘战役启动提示词模板（区域无关）

> 用途：在某一 region 下开 REGULAR Alpha 挖掘战役的标准提示词。把 `$REGION` / `$DATASET` 填入即可复用。
> 编排：`wq-brain-ra-pipeline`（唯一挖掘编排 SOP）。三角分工：`wq-brain-campaign-matrix`（where 选区选集）+ `wq-brain-campaign-toolkit`（how 战役引擎）。
> 本模板只固化方法论与纪律；区域/数据集特定实证（如 KOR target_prc 判死、model25 底数）在 `region_kb` / `template_families.json` 的 evidence 里，不在此复写。

---

## 0. 一句话启动指令（AI 直接执行）

```
在 $REGION 区域开 REGULAR Alpha 挖掘战役，数据集候选 $DATASET（或让 wq-brain-campaign-matrix 选集）。
严格走 wq-brain-ra-pipeline 九步流水线（S-PRE→S6），遵守 §2 硬纪律。先做步 1 S-PRE 查表确认可挖。
```

---

## 1. 战役定位

- **区域**：`$REGION`
- **数据集**：`$DATASET`（S-PRE 查表选定）
- **战役类型**：REGULAR Alpha 挖掘（九步流水线 S-PRE→S6）
- **产物契约**：战役产物只入 `data/wqb.db`（经 `wqb-db` MCP），禁止 Agent `Write` 战役 json/csv。

---

## 2. 硬纪律（必须遵守，区域无关）

| # | 纪律 | 说明 |
|---|---|---|
| D1 | **禁止 PV×model 数据集混** | 同一表达式不能同时用 PV 数据集字段 + model 数据集字段。辅助腿只能用同数据集内部字段或非 PV 正交主题。 |
| D2 | **禁止同信号加权调参** | 组合权重仅单次设置（0.5/0.5 或 0.6/0.4 或 0.7/0.3），禁止权重网格扫描。同信号不达标换字段组合/换概念（Mode B 想法层），不调权重。 |
| D3 | **ra-pipeline 严格走 skill 链** | S2 候选池必须调 `brain-makeSomeGem`（headless_runner + priors，注入 region_kb 论坛模板），禁止手写候选池替代；S4 评审走完整链：selfcorrQuick → check_self_correlation → compute_mutual_correlation → check_correlation → 归因（get_alpha_yearly_stats + brain-explain-alphas）→ brain-alpha-robustness → brain-alpha-judge；Mode B/A 优化须走 `wq-brain-alpha-optimization-v1`，不得裸扫参数。 |
| D4 | **Mode B 资格线** | 整波最强候选 `sharpe≥1.25 且 fitness≥0.8` 才进 Mode B 组合增强/继续优化；未达判死（dead_end 回写 + wave 台账 closed），禁止进 near_pool、禁止发增强波。 |
| D5 | **拉指标一律 MCP 直调** | `get_alpha_details`（单 ID 一次调用；批量逐 ID 连续调用），禁临时 Python 脚本（`logs/_tmp_*.py`）调 brain_api 拉指标。 |
| D6 | **产物只入 wqb.db** | 读：`get_wave_result`/`get_ledger_key`/`list_expressions`/`get_field_catalog`；写：`upsert_wave_result`/`upsert_ledger_key`/`upsert_registry_empirical`/`upsert_expressions`/`upsert_field_catalog`/`upsert_gate_result`/`upsert_backtest_rows`（幂等）。 |
| D7 | **压缩后回查清单** | 上下文压缩后每波开始前须回查流程强制环节清单，防止惯性循环丢环节。 |

---

## 3. 九步流水线（S-PRE→S6）

> 每步含目的/MCP 调用/产物/失败分支。任一步 FAIL 就地回退，不允许跳过继续。

### 步 1（S-PRE）查表选区选集（必做，不跳过）
- **MCP**：`get_campaign_summary($REGION)` / `get_dead_ends($REGION)` / `get_dead_datasets($REGION)` / `get_cross_region_lessons()` / `get_ledger_key($REGION, "region_kb")` / `operator_audit` / `get_messages`
- **产物**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号
- **判据**：`$DATASET` 不在死名单、prod_corr 底数可接受（<0.7 或有组腿稀释空间）、region_kb 无"该主题已饱和"标记。

### 步 2（S0）数据集体检 + 金字塔配置
- **MCP**：`workflow_campaign(stage="S0", calibrate=true, dry_run=true)` → `workflow_campaign(stage="S0", calibrate=true)` → `workflow_campaign(stage="S0")` → `get_ledger_key(key="s0_ranking")`
- **产物**：ledger `s0_whitelist` / `s0_ranking` / `*_dead`；calibrate 缓存 `s0_calibrate_$REGION`

### 步 3（S1）字段扫描 + 理解
- **MCP**：`workflow_campaign(stage="S1", dataset=$DS)` / `workflow_feature_engineering`（可选）/ `get_datafields`（字段分级风险筛查）
- **产物**：fields 表 + ledger `s1_<ds>_d<delay>` + ideas.md 路径
- **字段分级**：users≥50 只验证方向不打磨（prod_corr 必超）；users 10-49 进候选池提交前实测 prod_corr；users 0-9 优先（理论 prod≈0）；冷门字段（users≤9）占批次预算 ≥50%
- **画像消费**（若 field_profile 已回填）：读 `get_field_catalog` + field_profile 形状/语义，供 S2 模板族 mechanism_premise 双校验
- **失败分支**：字段数 <10 退回步 2 白名单外；VECTOR 比例用 get_datafields 确认，步 4 传对 data_type

### 步 4（S2）选波：概念优先生成（`brain-makeSomeGem` 强制调用）
- **MCP**：`workflow_campaign(stage="S6", subcommand="assemble-priors")` → `get_ledger_key(key="s1_${DS}_d${DELAY}")` → `workflow_gem(region=$REGION, dataset_id=$DS, delay=$DELAY, universe=$UNIVERSE, priors_file=...)` → `workflow_campaign(stage="S2", dataset=$DS, wave=$W)`
- **概念优先**：机制→1-2 个具体字段 id→一条 Implementation Example，禁止"每个字段套 rank"；必须带 priors_file（win/dead_end JSON，可省——GEM 经 load_priors(region) 从 DB 快照直读）
- **硬约束**：① 先读 win 层（region_kb.win_recipes），有胜绩则本波至少 2 槽按机制换腿；② 有信号 |Sharpe|≥1.0/PASS_CHEAP/registry 标明有 IS 但卡 prod，复合后 |S|<0.5 不再入选；③ 七槽（Token-Bucket C≈7）：≥2 跨金字塔、≥1 win 换腿、弱探针最多 1 槽；④ 时间窗口只用 1/5/22/66/252/504/1008/1260 标准窗口，其他须给经济含义；⑤ 禁止 add(A,B) 混信号；⑥ 字段角色区分（主信号/辅助信号/group/bucket）；⑦ 金字塔点亮（一个金字塔需 3 颗，均匀点塔）
- **模板族（可选但推荐）**：`--template-family <family_id>`（template_families.json），启用机制⇄数据类别匹配门 + mechanism_premise 形状+语义双校验（field_profile 已回填时生效；无画像时降级不过滤）

### 步 5（S2→S3）门禁
- **MCP**：`workflow_campaign(stage="S2", dataset=$DS, wave=$W)` / `preflight_expressions`（VECTOR auto_fix）
- **硬门**：check_batch（多样性守卫）→ check_expr_against_inspect（体检硬门：低覆盖 cr<0.4 须 ts_backfill、高偏度 |skew|>2 须 rank/winsorize、厚尾 kurt>8 须 rank/winsorize、单边恒正/负须 ts_delta/rank/bucket、稀疏事件须 trade_when）→ wave_gate（5 闸预检）
- **产物**：gate_results 表（all_pass / fail_reasons）

### 步 6（S3）七槽回测
- **MCP**：`workflow_batch_track(region=$REGION, wave=$W, dataset=$DS, concurrency=7)` / `batch_status(simulation_ids=[...])` / `create_multi_simulation`（7 批同提）/ `lookINTO_SimError_message`（统一轮询）/ `get_alpha_details`（逐 ID 拉详情）
- **产物**：backtest_results 表 + wave_results 表 + checkpoint
- **结构化摘要**：stdout_tail 精简为 structured_summary（COMPLETE/ERROR/CANCELLED 计数）

### 步 7（S4）诊断改进
- **MCP**：`workflow_campaign(stage="S4", dataset=$DS, wave=$W)` / `get_alpha_details` / `check_correlation`
- **产物**：walls 诊断 + 改进候选（Mode B/A 产出，须走 `wq-brain-alpha-optimization-v1`）
- **写入**：ledger `s4_walls_${REGION}_${W}` + salvage_pool（快达标因子自动入池）

### 步 8（S4→S5）稳健闸与提交判定
- **硬前置**：Failed-count 资格门（Failed RA == 0）
- **提交判定链**：① Failed-count 资格门 → ② `submit_verdict(alpha_id)`（唯一权威，零成本判定）→ ③ `brain-alpha-judge`（可选参考层）→ ④ 用户确认 → ⑤ `workflow_submit_alpha`
- **禁止**：submit_verdict READY 后自动 `workflow_submit_alpha`（必须用户确认）
- **产物**：提交判定（SUBMITTABLE / BLOCKED / WAIT_THEME_ROTATION）

### 步 9（S6）复盘回写
- **MCP**：`upsert_wave_result(verdict=PASS|FAIL|PARTIAL)` / `upsert_registry_empirical`（dead_end / win / campaign）/ `upsert_ledger_key(key="s6_verdict_<wave>")`
- **产物**：wave_results.verdict + registry_empirical 更新
- **闭环**：S6 回写 → 下一波 S-PRE 自动读最新 dead_ends/wins/campaigns

---

## 4. 循环与停止（步 2 → 步 9 为一波）

| 条件 | 动作 |
|---|---|
| 连续 3 波全 FAIL 且无新 dead_end | 该 region 暂停，转 `brain-nextMove-analysis` |
| 白名单被 dead_end 全覆盖 | 停止 |
| 连续 3 波 gate 通过率=0（gate_results.all_pass 全 0） | 该区信号族/数据集判死，转 `wq-brain-campaign-matrix` 换数据集，或转 `brain-nextMove-analysis` 换区域 |
| ACTIVE RA ≥10 | 可转 `wq-brain-superalpha`（先 `sa_probe --region $REGION`） |
| 配额耗尽 | 挂起提交，继续步 2 → 9 |
| 用户要求持续日循环 | 每个 NY 日先 `brain-nextMove-analysis`，再从步 1 跑；日界 21:30 ET |

---

## 5. 区域 Profile 路由

九步骨架全区域共用，区域差异通过 profile 注入（`references/regions/<REGION>.md`），四个注入点：入口裁决（entry_verdict）/ 生成先验（priors）/ 闸门特化（gate_overrides）/ 循环策略（loop_policy）。
规则：profile 与骨架正文冲突时 **profile 优先**（它是区域实证结晶）；profile 缺字段回落骨架默认；`frozen` 区域（当前仅 MEA）步 1 即拒。

---

## 6. 反模式（禁止）

- 再 invoke `brain-deepExplore` 或按其旧 S2-D/S2-M 必跑、停止闸 4 覆盖 RA
- 手写 `_gate_waveNN.py` / `w*_batches.json` / 把 GEM `final_expressions.json` 当真相源
- 手写 requests；跳过步 9；在本文件复写阈值；`combination(alpha(...))`
- 七槽全裸探针；七槽全 MODEL + 固定 COUNTRY/decay6
- 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽
- submit_verdict READY 后自动 `workflow_submit_alpha`
- 调用已废弃的 `glb_pipeline` / `gbr_pipeline` / `glb_alpha_machine`
- 直接把 `brain-feature-implementation` 当主链入口（它在 GEM 内部）
- 手写 PowerShell 命令替代 MCP 工具调用（能走 MCP 的步骤一律走 MCP）

---

## 7. Artifact 契约（战役产物只入 data/wqb.db）

| 阶段 | 入库 |
|---|---|
| S0 | ledger `s0_ranking` / `s0_whitelist` / `*_dead` |
| S1 | ledger `s1_<ds>_d<delay>` + ideas.md 路径 |
| S2 | `expressions` status=`gem`/`enhanced`；ledger idea |
| S3 | `backtest_results` / `wave_results` / checkpoint |
| S6 | `wave_results.verdict` + `registry_empirical` |

---

## 8. 字段画像与模板族（形状分流，2026-09-04 落地）

> 可选但推荐的增强层：字段画像（field_profile）+ 模板族（template_families.json 的 mechanism_premise）做"机制前提⇄字段形状"一致性校验，提高候选匹配率（实证 0%→80%）。

- **画像入库**：`tools/field_profile_backfill.py --zip <WebDataScope.zip> [--region $REGION]`（WebDataScope 口径 5 类形状：zero_inflated/point_mass/ceiling/spread/concentrated）；无 WebDataScope 时用 BRAIN Labs（`tracking/<REGION>/scripts/labs_field_profile_batch.py` + `tools/field_profile_from_labs.py`）
- **模板族配置**：`wq-brain-campaign-toolkit/config/template_families.json`，每族带 `mechanism_premise`（shape_requirement + semantic_requirement + forbidden_shape + data_category + vector_wrap）
- **GEM 消费**：`--template-family <family_id>` → 机制⇄数据类别匹配门（烧配额前拦截错配）+ mechanism_premise 形状+语义双校验（绑定池过滤）
- **闸门软闸**：`tools/wave_gate.py --template-family <family_id>` → 机制-形状一致性软闸（WARN 不阻断）
- **降级**：无画像数据集（field_profile 空）正确降级为不过滤，不阻断流水线

---

*本模板为区域无关方法论；区域/数据集特定实证见 `region_kb`（ledger_kv）与 `template_families.json` 的 evidence 字段。*
