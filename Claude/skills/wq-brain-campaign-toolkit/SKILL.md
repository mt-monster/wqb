---
last_verified: 2026-09-15
name: wq-brain-campaign-toolkit
description: "区域无关的 WorldQuant BRAIN alpha 挖掘战役引擎（战役脚本的唯一权威实现）。 触发词：战役脚本/campaign toolkit/gate 5 闸预检/pipeline 编排/wave 选波/probe 三灯判定/ 台账/ledger/scan_fields 字段扫描/review 评审/多样性 diversity/配额 quota/断点续跑。 功能覆盖：8 闸预检（闸1 语法含算子元数/闸2 字段白名单/闸3 VECTOR 类型/闸4 不可访问算子 ts_min,ts_max/闸5 毒模式/闸6 批级多样性/闸7 longCount/闸8 EVENT 类型；+可选闸0 语义反模式，sha1 缓存）、pipeline 编排（checkpoint 断点续跑/ 回测并发走七槽填槽（wqb-concurrency §8，2026-08-25 起 7 批），见 references/poll-and-quota.md/单批在飞已废弃/ 挂起熔断 60min/429 指数退避/ET 日历日提交配额闸（REGULAR 4/日 + SUPER 1/日 + PPA 独立 `POWER_POOL_SUBMISSION` 1/日，00:00 ET 重置，三者并行不互占））、wave 构建 （全历史去重/算子树分桶/骨架配给 linear_mix≤0.5/near 加权）、数据集评分+探针 v2 三灯判定、 台账 LedgerStore（原子写/双遍重放/幂等）、typed catalog 字段扫描（dataset.id= 过滤陷阱）、 review walls 诊断+多样性审计。"
layer: L-TOOL
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---







# wq-brain-campaign-toolkit（战役引擎层）

## 1. 定位
- 本 skill 是**战役脚本的唯一权威实现**（引擎层，可运行脚本）。其他 skill 只写"何时用/怎么判"（方法论层）并指向这里，禁止在别处复制本 scripts/ 的逻辑。
- 从 `tracking/KOR` 战役工具栈抽象而来（2026-08-15，KOR 战役 15+ 轮实证）；KOR 目录脚本保留为区域历史实现。
- 上下游分工：`wq-brain-ra-pipeline`=when/what/怎么挖 → `wq-brain-campaign-matrix`=where（查表选区选集）→ **本 skill=how（战役目录内执行）**。

## 1.x 工具使用率等级（2026-08-31 v2 修正版，引导优先使用）

> 完整评估报告：`reports/toolkit_usage_review_2026-08-31.md`。按「工作区引用 + toolkit 内部 import + CLI 子命令分发」三维扫描分级，**优先使用核心工具**。

**核心工具（高使用率，优先使用）**：
| 工具 | 职责 |
|------|------|
| `campaign.py` | 战役 CLI 入口（registry/ledger 幂等写 + 子命令分发） |
| `gate.py` | 闸1–5 预检（闸编号唯一基准见 `INDEX.md`「gate.py 闸编号」） |
| `pipeline.py` | 战役编排（checkpoint 断点续跑/七槽填槽） |
| `scan_fields.py` | typed catalog 字段扫描 |
| `metrics_cache.py` | 指标缓存（避免重复拉取） |
| `distill_experience.py` | 经验蒸馏（G1：跨区铁律/红灯族/模板晋升，学习闭环） |
| `os_feedback.py` | OS 回流（G3：提交后真实表现衰减回写，学习闭环） |
| `family_atlas.py` | 家族导航（G2：信号族状态图，选波前查图） |
| `budget_planner.py` | 预算规划（七槽/提交额度分配建议） |
| `campaign_mutex.py` | 多战役互斥（波号/槽位/额度仲裁） |

**辅助工具（中使用率）**：`review_wave.py` / `score_datasets.py` / `harvest.py` / `build_wave.py` / `diversity_audit.py` / `check_ledger_sync.py`。

**内部使用工具（工作区零引用但被本目录 import / CLI 分发，必须保留）**：`assemble_priors.py`（被 build_wave/gate import + `campaign.py assemble-priors`）/ `signal_classifier.py` / `composition_validator.py` / `diversity_extract.py`（`campaign.py diversity-extract`）/ `s2_compliance_mark.py`（`campaign.py s2-mark`）/ `neutralization_sweep.py`（pipeline 兼容其产物）。**勿删**。

**确认零使用（三维全 0，2026-08-31 已归档）**：`migrate_templates`（一次性）/ `compose_signals` / `param_opt` / `ortho_prescreen` / `proxy_prescreen` / `rescue_checklist` / `calibrate_probe` / `fit_mix_weights` / `build_mix` / `adhoc` / `param_matrix` / `diversity_slots` / `composition_templates`（仅被 compose_signals 引用）——已移入 `attic/tools_archive_20260831/`。新任务一律用核心 5 工具，不要调用这些；如需回溯旧逻辑去 attic 取。

## 衔接协议（上游 / 输入 / 输出 / 下游）

- **上游**：`wq-brain-ra-pipeline`（编排器）；`brain-sim-alphas-in-batch-and-track`（S3 入口，经 subprocess 调用本引擎——唯一运行时调用方）；`wq-brain-campaign-matrix`（S-PRE 配置包 → 映射为 `--campaign-dir` 与 settings/thresholds 参数）；`wq-backtest-monitor`（S6 §14 经 `campaign.py ledger` 幂等回写）。
- **本 skill 角色**：L-TOOL 引擎层 = how；S1–S6 各阶段战役脚本的唯一权威实现，方法论层 skill 一律指向此处、禁止复制 scripts/ 逻辑。
- **输入**：战役目录 `tracking/<REGION>/`（`config/settings.json` + `config/thresholds.json` + `reference/` typed catalog）+ 子命令（`--campaign-dir` 铁律见 §4）；并发纪律引用 `wqb-concurrency` §8 七槽填槽。
- **输出（入库总原则：DB 为唯一战役真相源；禁止 Agent Write 战役 json/csv）**：S1 经 `campaign.py ledger set "s1_<ds>_d<delay>"` / `mcp__wqb-db__upsert_ledger_key`；`score_datasets.py` → ledger `s0_ranking`；白名单 `s0_whitelist`；`scan_fields.py` → `fields` 表；`diversity_extract.py` → `diversity_potential` + expressions；`build_wave.py --from-db` + `gate.py --from-db` → `expressions` / `gate_results`；`pipeline.py` → `backtest_results` + ledger `ckpt_w<W>` + `wave_results`；`review_wave.py` → ledger `review_<tag>`；`methodology_rules` 区域计数 → ledger_kv（全局规则仍用 toolkit `config/methodology_rules.json`）。静态配置 `settings.json`/`thresholds.json`/`platform_constraints.json` 仍为文件。
- **下游**：`brain-sim-alphas-in-batch-and-track`（S3 编排入口）；S4 诊断族（`brain-how-to-pass-alpha-test`/`wq-brain-alpha-optimization-v1`/`brain-alpha-robustness`）消费 review/ranking 产物；`wq-backtest-monitor`（S6）经本引擎回写台账反哺 S-PRE。

## 2. 运行环境
所有 Python 命令使用 MCP venv：`$WQ_PY`。脚本为纯标准库实现；仅 gate 闸1 需 import alpha-expression-verifier（经 `WQ_VALIDATOR_DIR` 探测）。

## 3. 战役目录契约
`tracking/<REGION>/` 必须含：
- `config/settings.json`：仿真设置（region/universe/delay/neutralization/decay/truncation/maxTrade/pasteurization...）+ `_multi_sim_batch_size` + `_concurrency_rule`
- `config/thresholds.json`：规范形态为六节（review / near / quick_scan / probe_scoring_v2 / hard_gates / dataset_health）+ 可选节（`diversity` / poll / submit_quota）。**KOR / IND / DEU 现为混合形态**（2026-09-12 更新：顶层扁平键 `sharpe_min` 等保留；`quick_scan`/`hard_gates` 已于 2026-09-11 补齐；`probe_scoring_v2` 仍缺——**刻意**，补齐会改 S0 评分行为，需单独实证后再引入）——读阈值必须两版兼容。完整 schema 与两版对照 → [references/campaign-dir-contract.md](references/campaign-dir-contract.md)
- `reference/`：typed catalog（`<region>_<dataset>_fields.json`）与 `<region>_generation_constraints.json`
- 完整 schema 与目录布局 → [references/campaign-dir-contract.md](references/campaign-dir-contract.md)

## 4. 调用约定（铁律）
1. 所有脚本统一 `--campaign-dir <路径>`（缺省=当前工作目录）。
2. **region 只从 `config/settings.json.region` 派生**，并校验与战役目录名一致（不一致即报错；测试可用 `CAMPAIGN_SKIP_DIR_CHECK=1` 跳过）。禁止从目录名或命令行猜 region。
3. 凭证走环境变量链：`WQ_USERNAME`/`WQ_PASSWORD` → `BRAIN_CREDENTIALS`（JSON 路径）→ `~/.brain_credentials` → `MCP_CONFIG_FILE` / `~/.brain_mcp_config.json`。
4. verifier 走 `WQ_VALIDATOR_DIR`（缺省自动探测 alpha-expression-verifier skill 的 scripts/）。
5. 平台级约束只有一份：`config/platform_constraints.json`；区域 ranking/catalog/rules 计数入库。
6. **Agent 持久化只走 `mcp__wqb-db__*` 或本引擎 CLI；禁止 Write/Copy 战役 json/csv。** `build_wave`/`gate`/`wave_gate`/`pipeline` 走 `--from-db`。

## 5. 快速开始（典型流程）
```bash
PY=$WQ_PY
TK=$WQ_TOOLKIT_DIR
CD=<CAMPAIGN_DIR>   # 如 tracking/KOR
# 评分前先校准（实测反学 category 权重+拥挤甜区）：先 dry-run 人工审、确认无异常再 apply
# 详见 references/probe-scoring-v2.md「评分前必做：calibrate 自学习校准」
$PY $TK/score_datasets.py --campaign-dir $CD --calibrate --dry-run   # 审：甜区 ac 是否异常巨大 / strong_acs 是否空
$PY $TK/score_datasets.py --campaign-dir $CD --calibrate             # 确认无异常后才写 thresholds
$PY $TK/score_datasets.py --campaign-dir $CD
$PY $TK/scan_fields.py --campaign-dir $CD --dataset <ds>
$PY $TK/score_datasets.py --campaign-dir $CD --probe-plan <ds> --fields 6
$PY $TK/build_wave.py --campaign-dir $CD --from-db --dataset <ds> --wave 01A
$PY $TK/gate.py --campaign-dir $CD --dataset <ds> --from-db --wave 01A
$PY $TK/gate.py --campaign-dir $CD --dataset <ds> --from-db --wave 01A --fix
$PY $TK/pipeline.py --campaign-dir $CD run --dataset <ds> --wave 01A --dry-run
$PY $TK/pipeline.py --campaign-dir $CD run --dataset <ds> --wave 01A --submit --review --write-ledger
$PY $TK/pipeline.py --campaign-dir $CD run --dataset <ds> --wave 01A --submit --max-rounds 3 --review --write-ledger
# 评审 / 三灯 / 多样性 / 台账 / 配额
$PY $TK/review_wave.py --campaign-dir $CD --multisim <id> --tag 01A --write-ledger
$PY $TK/score_datasets.py --campaign-dir $CD --probe-score <multisim> --dataset <ds> --stage A
$PY $TK/diversity_audit.py --campaign-dir $CD
$PY $TK/campaign.py --campaign-dir $CD ledger keys
$PY $TK/pipeline.py --campaign-dir $CD quota
```

## 6. 子命令一览
| 脚本 | 职责 | 关键参数 | 细节文档 |
|---|---|---|---|
| scan_fields.py | typed catalog 字段扫描 | --dataset / --limit / --zero-comp | campaign-dir-contract |
| score_datasets.py | 数据集评分 / 探针计划 / 三灯评分 | --probe-plan / --probe-score / --stage | probe-scoring-v2 |
| gate.py | **8 闸 + 可选闸0**：闸1 语法(含算子元数)/闸2 白名单/闸3 类型/闸4 不可访问算子/闸5 毒模式/闸6 批级多样性/闸7 longCount(`--sanity-longcount`)/闸8 EVENT(`--sanity-event-type`)，+sha1 缓存（--fix 自动裹 vec_*） | --dataset / --file / --expr / --fix / --sanity-longcount / --sanity-event-type / --sanity-all / --gate0 | gate-rules |
| build_wave.py | 选波后处理（去重/分桶/配给/near；**不生成**表达式，`--file` 来自 makeSomeGem）+ 多样性增强（默认开启）+ **选波权威化**（2026-09-12：picked 写 selected 的同一事务里，本波落选且仍为 gem/pending/enhanced 的行归档 superseded，dropped/selected/gated 与已回测行不碰；要重选同波先用 `mcp__wqb-db__set_expression_status` 改回 gem） | --file / --wave / --size / --enhance-diversity always\|auto\|never / --auto-coverage auto\|always\|never（never = 契约签发/注入/自愈三处全关） | gate-rules |
| pipeline.py | 端到端编排 + 配额闸；**装载 settings 后按 `region_kb.gate_priors` 实测过闸率改写 decay/neutralization（settings prior，2026-09-15 ①）**；收批后自动刷新 `region_kb`（③）；中止路径 rc=2（⑥） | run / quota；--submit / --dry-run / --no-settings-prior；--set K=V 钉住维度 | poll-and-quota |
| review_wave.py | walls 诊断 + 台账回写；`rn_sharpe ≤ review.rn_sharpe_min`（缺省 0）判 `RN_EXPOSURE` 墙、不进候选（⑦） | --multisim / --alphas / --write-ledger | gate-rules |
| metrics_cache.py | 指标读穿缓存 | --multisim= / --refresh | poll-and-quota |
| diversity_audit.py | 多样性审计（latest+history） | --no-ledger | ledger-schema |
| diversity_extract.py | 单数据集多样性榨取（L1/L2/L3 三轮） | --dataset / --rounds / --size / --max-ppac | gate-rules |
| distill_experience.py | **经验蒸馏器（G1 学习闭环）**：registry win/dead 模式归纳 → 跨区铁律/红灯族/模板晋升；--apply 落库 | --apply / --json | — |
| os_feedback.py | **OS 回流（G3 学习闭环）**：拉平台 OS 表现，对比 IS 指标，衰减回写 win 降权标记 | --apply | — |
| family_atlas.py | **家族导航（G2）**：信号族粒度全局状态机（untried→has_signal→near_gate→active→dead→os_decay），选波前先查图 | --all / --state / --json | — |
| budget_planner.py | **预算规划器（#3）**：七槽填槽建议 + ET 日提交额度 + READY 候选提交排序 | --submit-plan / --json | — |
| campaign_mutex.py | **多战役互斥（#7）**：波号 CAS 分配 / 槽位预算 TTL 仲裁 / 提交额度共享账本 | status / alloc-wave / take-slots / quota-reserve | — |
| campaign.py ledger | 台账统一 CLI | keys/get/set/mark-dead/add-wave/set-verdict/submit-ready/backup | ledger-schema |
| campaign.py registry | registry 实证层统一 CLI（幂等写+结构校验） | add-dead-end/add-win/upsert-campaign/add-orphan/list/get；--dry-run/--extra/@file.json。⚠ **必填参数**：`add-dead-end` 需 `--id --family --reason --rule`；`add-win` 需 `--id --what --key` —— 只给 `--extra @file.json` 会 argparse 报错（错误字段名在 extra 里也只当附加，不替代必填） | ledger-schema |
| campaign.py wave | wave_results 台账统一 CLI（幂等写+一键导入） | upsert/import/get/list；--finding 可重复；--dry-run | ledger-schema |

## 6.x S0 评分机制增强（2026-09-14，P0–P6）

`score_datasets.py` 评分 = `(0.4·cov + crowd_penalty(ac) + 0.2·breadth + 0.1·valueScore + empirical_prior) × category_weight[0.9~1.15]`；分位分层 tier1≥P60 / tier2≥P30。**新参数默认 OFF/中性**（`empirical_weight=0.0`、饱和项需 `saturated_datasets` 台账才生效），无台账时行为与旧版逐条一致；区域经 `thresholds.json` 的 `dataset_health` 节 opt-in。canonical 默认见 `src/wqb/config.py` 的 `DATASET_HEALTH_SCORING`。

| 项 | 机制 | 开关（dataset_health） | 数据源台账 |
|---|---|---|---|
| P0 经验强度先验 | `score()` 叠加 `empirical_prior`=`empirical_weight`·clamp(ceiling_ratio)，把目标从「干净+低拥挤」拉向「过闸概率」 | `empirical_weight`(0=关) / `empirical_prior_neutral` | `dataset_empirical_prior` |
| P2 饱和再验证降级 | 命中集自动降 `excluded` 且不被保底带复活 | `saturation_demotion_enable` | `saturated_datasets` |
| P3 universe 一致性守卫 | `s0_ranking`/`s0_whitelist`.universe ≠ `settings.universe` → `[WARN]`，提示重生成+白名单复核 | 常开 | 读 `settings.json`.universe |
| P5 饱和拍平 model | `_region_saturated` 时 model 类 `category_weight` 封顶 1.0 | `flatten_model_when_saturated` | 由 `saturated_datasets` 非空推导 |
| P6 calibrate token 去重 | `_expr_fields` 去重 + 剔除 group 变量关键字，根治甜区污染 | 常开（calibrate 内） | — |

**信号分 vs 点塔分（P5 拆分）**：`s0_ranking.ranking[].score`=信号强度榜（哪个集能出好 alpha）；`pyramid_view`=点塔战略榜（哪个集点亮金字塔，pyr_value 驱动）。两榜语义分离：选集先看信号分定候选，再用点塔分排提交优先级，勿相加或混排。

**新增台账键**（`make_ledger_store(ctx)` 读写，均 region-scoped）：

- `dataset_empirical_prior` — calibrate 产出：`{region, gate_sharpe, updated, priors:{ds:{best_sharpe, ceiling_ratio, observations}}}`，`ceiling_ratio`=best_sharpe/gate_sharpe。
- `saturated_datasets` — prod 饱和事实：`{datasets:{ds:{reason}}}`；score 据此降级，P5 据此拍平 model。
- `seat_model`（campaign_intel `s0-select` 读）— `{seats:{ds:est_seats}, seats_per_dataset_default:2}`；同族高互相关只算 1 座位。
- `s0_whitelist.candidates[].override`（P4）— 手工捞回自动判死/排除集时须写 `{reason, auto_tier, auto_excluded_by}`。

## 6.y 接线修复落地（2026-09-15，审计 ①③⑥⑦）

| 项 | 机制 | 开关 / 台账 |
|---|---|---|
| ① settings prior | `_lib/region_kb.py::apply_settings_prior`：读 `region_kb.gate_priors`（缺则 `gate_priors_local`）的 `by_decay` / `by_neutralization`，格子样本 ≥`min_n`(30) 且过闸率 ≥ 当前设置 ×`min_lift`(2.0) 才改写；显式 `--set`/`--neutralization` 钉住的维度不动。GEM prompt 只再渲染 operator-count / field-family（`economic_priors.py`），设置维度不进 prompt。 | `thresholds.json` `settings_prior{enabled,min_n,min_lift,dims}`；CLI `--no-settings-prior` |
| ③ region_kb 波后刷新 | `stage_review` 写完 wave_results 后 `refresh_after_wave`：`recent_waves`（近 20 波）+ `gate_priors_local`（本地 backtest_results 重算 by_neutralization/op_count/field_family，无 decay）+ `updated_at`。定向 upsert，不整区重写。 | 常开（异常不阻断） |
| ⑥ S2-COMPLIANCE 降级 | `s2_compliance_w<wave>` 缺失只打印 `[S2-COMPLIANCE] 无合规记录（仅提示，不阻断）`，不再 `--force`；`s2_compliance_mark.py` / `campaign.py s2-mark` 保留为可选标记。`pipeline.py` 全部中止路径 `sys.exit(2)`。 | — |
| ⑦ rn 墙 / 停止规则 / verdict 枚举 | `review_wave.rn_exposure()` 进 `walls()`/`passes()`；停止规则由节点层 `campaign.py::_run_stop_rules_gate` 按 DB 判定（区 backtested≥100 且 passed=0；最近 3 closed 波全 FAIL），ledger `stop_rules_override{reason,until}` 放行；`mcp__wqb-db__upsert_wave_result` 归一/拒绝非枚举 verdict。 | `thresholds.review.rn_sharpe_min`；`thresholds.diversity.stop_rules{enabled,yield_min_backtests,consecutive_fail_waves}` |

## 7. 闸 7-8：数据质量预检（2026-08-25 落地）

在 5 基础闸（语法/字段白名单/VECTOR 类型/不可访问算子/毒模式）之后追加两个**数据质量闸**，实证动机：约 17% 死路属结构性缺陷（longCount 过低、EVENT 字段误用时间序列算子），可事前静态拦截。

| 闸 | 检查 | 判定 | 启用参数 |
|---|---|---|---|
| 闸 7 longCount | 表达式引用的 VECTOR 字段在 typed catalog 中的 `longCount` | `0 ≤ longCount < 80` → WARN（小宇宙区域如 KOR/HKG/TWN 按 profile 升级 FAIL） | `--sanity-longcount` |
| 闸 8 EVENT 类型 | 字段 `type==EVENT` 但表达式未使用 `ts_event_*` 算子 | FAIL（EVENT 字段禁 ts_* 通用时序算子，铁律） | `--sanity-event-type` |

`--sanity-all` = 闸 7+8 全开；输出 JSON 新增 `sanity_gates` 字段。CW（持仓集中度）为回测后动态指标，**不进静态闸**，在步 7 评审与 KOR 等区域 profile 的 `cw_gate` 覆盖中处理。

## 7.x fail-fast：失败性质判定（2026-09-13 落地）

步 7 评审除 walls 诊断外，先判定**失败性质**再决定是否继续投入（机器实现 `_lib/rules.py::classify_failure`，接入 `recommend_next_wave`）：

- **无效努力七信号**：Sharpe 卡 0.7–0.9 / PnL 后半段衰减 / 换变体无本质变化 / Fitness 始终不达标 / Sub-universe 反复失败 / Weight concentration 偏高 / 过线后 Similarity 爆表。**命中 ≥2 项 → 结构性，止损换方向**。
- **可修复**：仅卡参数层墙（2Y/MARGIN/TVR/CW/FITNESS）→ 新增「可修复失败」推荐（priority 65），杠杆 = decay / neutralization / gate / 换历史位置表达。
- **结构性**：命中远期衰减/变体不变/相似度墙，或信号太弱（`max_sharpe<1.0`）→ 富化既有「结构层重构」推荐，停止该家族。

判据全文（含阈值表与反向纪律）见 [`docs/experience/fail_fast_rules.md`](docs/experience/fail_fast_rules.md)；规则条目 `failure_nature_classifier_v1` / `no_effort_seven_signals_v1` 在 `config/methodology_rules.json`。纪律：**AI/自动化只做研究效率（整理/统计/打标/复盘），不自动提交、不刷规则**。

## 8. 纪律
1. **原子写**（tmp+os.replace）；台账一律走 `make_ledger_store(ctx)` 工厂（默认 SQLite 后端 `SqliteLedgerStore`，存 `data/wqb.db` 的 `ledger_kv` 表；旧 JSON 后端 `LedgerStore` 保留但已弃用）。双遍重放 + 幂等 mutation，禁止 record_*.py 式直改。
2. **单进程单登录**；429 指数退避（5 次，5s 起倍增）。
3. 不动战役数据：candidates/results/reviews/reference/台账只按脚本既定产物写入；手工编辑先备份。
4. 禁止第二权威实现；record_*.py 一次性脚本模式已淘汰。
5. 提交配额是稀缺资源：未过 gate 不提交；pipeline 默认只干跑，显式 `--submit` 才烧配额；`--force` 才越过配额闸。
6. **单轨数据库模式**（2026-08-21 起）：历史 JSON（campaign_state / registry / wave_results）已归档到 `attic/json_archive/`，唯一事实源为 `data/wqb.db`。台账读写走 `make_ledger_store(ctx)`（默认 sqlite）；registry 写一律走 `campaign.py registry` 幂等 CLI（散装 SQL/dao 直改仅限读），见 `_lib/registry.py`。
7. **选波/填槽优先级（与 `wq-brain-ra-pipeline` 步 4/步 6、`src/wqb.config.MINING` 对齐）**：
   1. 开波先读 registry **win** 层。有胜绩则至少 `win_replay_slots_min` 槽按该**机制换腿**（EUR 实证：`0.40` 慢 MODEL 残差 × `0.60` 快 PV），设置跟 win（中性化/decay），禁止只穷举同金字塔换字段。
   2. 每波至少 `cross_pyramid_slots_min` 槽引入非 MODEL 成分。S0 `apply_pyramid_quota` 默认开启，白名单至少 2 个非 MODEL；`category_weight` 夹在 0.9–1.15。
   3. 有信号字段先做组合（同集或跨金字塔慢×快）。有信号 = `|Sharpe|≥1.0` / `PASS_CHEAP` / registry 标明有 IS 但卡 prod（腿禁用 ≠ 整集判死）。复合后 `|S|<0.5` 不再占槽。
   4. **prod-first**：每槽先 1–2 条骨架查平台 `prod_corr`；≥0.7 停扩、换腿（Mode B）。禁止先摊满 8 条再查 prod。
   5. 弱探针最多 1 槽，且仅当本波尚无近闸字段。反模式：七槽同时打 7 个未证明信号的新数据集裸探针；七槽全纯 MODEL。
   6. 跨集 gate 白名单失败 → 合并 catalog 再过闸；仍失败则拆成慢腿批 + 快腿批同波对照，不停挖。
   `type=strategy` 规则会在 `build_wave`/`pipeline` 打印 `[rules][strategy:…]`。

8. **新增/修改 workflow 节点 → 四处必须同步**（2026-09-18 固化）：
   workflow 节点住在 `src/wqb/workflow/`，但**注册信息散在四处**，漏一处测试即红：

   | # | 位置 | 要改什么 |
   |---|---|---|
   | ① | `src/wqb/workflow/registry.py` | `register()` 调用 + `NodeMeta`；**`required_params`/`optional_params` 必须与 `run()` 签名逐字一致**（唯一例外 `_context` / `dry_run`） |
   | ② | `tests/unit/test_workflow.py` | `test_registry_lists_all_core_nodes` 的期望节点集合（加节点则加一条 + 注释写日期与阶段） |
   | ③ | `tests/unit/test_skill_integrity.py` | `_DRY_RUN_CASES` 干跑用例表（参数须零副作用） |
   | ④ | `Claude/skills/INDEX.md` | workflow 节点计数（`test_docs_consistency.py` 机械守护） |

   **一次跑完全部检查**，不要"改一处跑一次测试"：
   ```bash
   python tools/audit_node_registration.py            # 列出四处全部缺口，退出码 1 = 有漂移
   python tools/audit_node_registration.py --node X   # 新增节点后单节点自检
   ```
   干跑契约：节点必须「走完零成本前置 → 构建出命令/请求计划 → 到此为止」，不 subprocess、
   不写库、不建目录；干跑失败必须**带得出 `error`**（禁止 `success=False` + `error=None`）。
   ★ 战例：`alpha_booster` 只做了 ①，②③ 漏同步 + NodeMeta 漏 `forum_refresh` → 3 个测试红；
   `gem` 的 meta 漏 `batch_size` 同样被 ① 的签名比对逮到。

## 9. 台账落盘（单轨 DB 模式）

**wave 结果台账**：每波回收后写入 `wave_results` 表（不再手写 `wave<N>_results.json`）。**AI 回写一律走 `campaign.py wave` CLI**（`tools/wave_results_writer.py` Python API 仅保留给引擎内部程序化写入）：

```bash
# 一键导入现成 wave<N>_results.json 入库（幂等，重复跑无副作用；默认 status=closed）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> wave import --file results/wave63_results.json

# 手填/更新 wave 结论（--finding 可重复多条；--candidates/--batches 用 @file.json 数组；upsert 为整行覆盖）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> wave upsert --wave 63 \
    --focus "..." --context "..." --verdict "..." --status closed \
    --finding "..." --finding "..."

# 写后立即验证（同一入口，无需另写查询脚本）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> wave get --wave 63
```

**WAVE_LEDGER.md 快照**：人工可读快照，从数据库生成（覆盖写，勿手改）。

```bash
# 导出 WAVE_LEDGER.md 快照
python tools/export_wave_ledger_md.py --region MEA
```

**战役台账（ledger_kv）**：`review_wave.py --write-ledger` 已默认走 `make_ledger_store(ctx)`（sqlite 后端），写入 `ledger_kv` 表。

**查询工具（wqb-db-mcp）**：
```
# 查 wave 结果
mcp__wqb-db__get_wave_result(region="MEA", wave_number=49)
mcp__wqb-db__list_wave_results(region="MEA", status="closed", limit=10)
mcp__wqb-db__get_latest_wave(region="MEA")

# 查台账
mcp__wqb-db__get_ledger_key(region="MEA", key="submit_ready")
mcp__wqb-db__list_ledger_keys(region="MEA")
mcp__wqb-db__get_submit_ready(region="MEA")
mcp__wqb-db__get_dead_datasets(region="KOR")

# 查 alpha
mcp__wqb-db__get_alpha_by_id(alpha_id="QP7er8qp")
mcp__wqb-db__list_alphas_by_wave(region="MEA", wave_number=49)
mcp__wqb-db__search_alphas_by_sharpe(region="MEA", min_sharpe=1.5, limit=10)

# 综合查询
mcp__wqb-db__get_campaign_summary(region="MEA")
mcp__wqb-db__get_region_overview()
```


## 工具化纪律（tools/ 通用工具，勿再写一次性脚本）

本 toolkit 提供战役目录内的执行原语；**跨区域通用的高频同构操作在项目 `tools/`**，
两者分工固定，不要在 toolkit 内复制一份：

| 场景 | 用这个 |
|---|---|
| 每波门禁（语法 + 闸1–5 + 闸7/8 + 体检硬门，一键落盘） | `tools/wave_gate.py`（内部会调本 toolkit 的 `gate.py`；2026-09-11 起亦有 MCP 节点 `workflow_execute` node="wave_gate"） |
| 批次状态查询/轮询 | `tools/batch_status.py` |
| 提交层判定（403 盲区） | `tools/submit_verdict.py` |
| 批量提交 | `tools/submit_batch.py` |
| SA 组件池探针 / SUPER 组套 | `tools/sa_probe.py`、`tools/super_build.py` |

工具索引与参数见 `tools/README.md`；缺参数就改工具（保持 `--help` 自文档），
反复新建一次性脚本即说明工具化不彻底（AGENTS.md §6）。
