# KOR 因子挖掘流水线：逐层深度分析与优化点（tracking/KOR 实录）

> 本文在 `KOR因子挖掘完整流程与经验总结.md` 基础上，**对每一层（Stage ①–⑨）做代码级展开**，定位瓶颈、脆弱点与重复劳动，并给出可落地的优化方案。
> 依据：通读 `tracking/KOR/scripts/` 全部 23 个脚本 + `kor_d1_campaign_state.json`（168 键）+ `reference/*_whitelist.json`（21 个）+ `reviews/*` + `candidates/*`（120+ wave 文件）。
> 方法：先复刻每层的真实实现（含文件路径与行级机制），再诊断，最后给方案。结论区分「事实」与「建议」。

---

## 总览：九层现状评分

| 层 | 脚本 | 成熟度 | 主要短板 |
|---|---|---|---|
| ① 数据集体检 | `record_whitelist_v2.py`、`scan_aieq.py`、`kor_dataset_probe_battery.json` | 中 | 评分靠手算、白名单 schema 不统一、探针电池未接线 |
| ② 字段收割/类型预检 | `kor_scan_fields.py/2/3`、`scan_aieq.py` | 低 | 依赖外部 cache、无类型、无持久化 |
| ③ 因子生成 | `brain-makeSomeGem`(外) + `batch_validate_kor.py` | 中 | 仅语法闸、未类型感知、与预检重复 |
| ④ 分层抽样选波 | `select_wave1.py` | 中 | 仅 wave1 用、前缀分桶碰撞、无优先级 |
| ⑤ 三道预检闸 | `kor_preflight_check.py` | **高** | 子进程调用、3e 正则启发、无缓存 |
| ⑥ 回测/固化轮询 | `kor_poll_pipeline.py`、`kor_fetch_metrics.py` | 中 | --wait 单次、重复登录、无指标缓存、无配额闸 |
| ⑦ 指标评审筛选 | `review_wave1/3/5.py` | 低 | **硬编 .qoder-cn 外部 cache**、阈值散落、每波一份 |
| ⑧ 多样性/切换决策 | `kor_op_exploration_stats.py`、`kor_diversity_review_round10.md` | 低 | 静态、非累积、切换靠事后判断 |
| ⑨ 台账固化 | `record_*.py` ×13 + `_tmp_*` ×4 | 中 | 13 份近重复、直写无原子、临时探针未清 |

---

## ① 数据集体检（Data Health Check）

### 当前实现（代码实证）
- `record_whitelist_v2.py`：一次性脚本，把诊断结论手写进台账 `dataset_first_strategy_20260815` 键，含 `new_whitelist_tier1`（7 个：behavioral_signals / ai_equity_alpha / equity_forum_data / price_signal_dl / model238 / multi_source_model / model242）与 `tier2_probe`（4 个：predictive_starmine / global_seasonal_model / chart_cnn_alpha / model31）。
- 双门槛 `cov≥0.85 且 alphaCount≤50` 是**人工判断**写死的，没有自动评分器。
- `scan_aieq.py`：另起炉灶从 `get_datafields` 缓存里筛 `userCount==0`（零竞争）字段，与 `record_whitelist_v2` 是两套独立逻辑。
- `reference/kor_dataset_probe_battery.json`：已存在 `protocol/purpose/execution/scoring` 结构，但**只是参考文档，没有被任何脚本自动执行**。

### 问题诊断
1. **评分无自动化**：每次新增数据集都要手改 `record_whitelist_v2.py` 的 tier 列表，极易遗漏 KOR 合法 universe 下的蓝海。
2. **白名单 schema 不统一**（确切事实）：21 个白名单文件中，**11 个用 `fields`(list) 格式**（`kor_acquisition_model_*`、`kor_fundamental44_*`、`kor_institutions6_*`、`kor_model109/170/192/219/230/30/32/53/`、`kor_news79_*`、`kor_pv106_*`、`kor_sentiment21_*`、`kor_shortinterest3_*`），**10 个用 `verified_fields`(dict) 格式**（chart_cnn / ai_factor_transfer / analyst_earnings_ibes / ml_factor_proj / price_signal_dl 等）。`kor_preflight_check.py` L71-74 虽兼容两种，但**字段级 `type`/`coverage`/`userCount` 大多未落库**——preflight 的「类型闸」只能取到数据集级 `data_type`（L75），无法做字段级类型校验。
3. **探针电池被闲置**：已定义 `probe_battery` 却没接线成「低成本预筛」循环，导致数据集是否 dead 必须烧一整波（8 式）才发现（战役 15+ 次 dataset_switch，几乎全 dead）。

### 优化方案
- **O1（P0）自动数据集评分器** `score_datasets.py`：直连 `get_datasets`（region=KOR, universe=TOP600），对全部数据集算综合分 = `w1·coverage + w2·(1/alphaCount) + w3·log(fieldCount) + w4·turnover_feasibility_proxy`，输出 `reference/kor_dataset_ranking.json`（按分排序 + Tier 标注）。取代手写 tier。
- **O2（P0）统一白名单 schema**：固定为单一种 canonical 格式，每条字段带 `{id, type, coverage, userCount, alphaCount}`，并附 `dataset/data_type/region/universe/delay`。旧 21 份写个一次性迁移脚本转格式。
- **O3（P1）接线探针电池**：`score_datasets.py` 在打分后，对 Top-N 候选自动跑 `probe_battery`（小批量 4–8 式）预筛，dead 的当场标记 `xxx_dead` 进台账，**不占用正式 wave 配额**。

---

## ② 字段收割与类型预检（Field Harvest & Type Pre-check）

### 当前实现（代码实证）
- `kor_scan_fields.py` / `kor_scan_fields2.py` / `kor_scan_fields3.py` 三份**几乎同构**：`cache_dir = r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7'`（L3），glob 该目录 `*.txt`，用 `re.findall(r'"id":\s*"([a-z0-9_]{8,})"', txt)` 抽字段 id，再按命名规则（q5/confscore4/star6/长窗口）手工挑候选。
- `scan_aieq.py` 同样读该外部 cache。
- **关键事实**：三者都只抽 `id` 字符串，**从未调用 `get_datafields` 取 `type` 列**；字段类型判断完全缺席于本层。

### 问题诊断
1. **强依赖外部会话 cache**：`.qoder-cn\cache\...\task-4d7` 是某次 agent 工具的临时目录，换会话/清缓存即失效，且路径硬编码绝对路径，不可移植。
2. **无类型信息 → 类型预检被后置且退化为正则**：正是因为这层没拉 type，`kor_preflight_check.py` 的「事件字段须 vec_* 包裹」闸（L99-117）只能靠正则启发式猜裸字段，wave2 `acquisition_model` 24/24 ERROR 的根因就在这里——类型在生成前未知。
3. **无持久化**：每次都重新 glob+正则，重复 I/O；字段集不落库，下游无法复用。
4. **三份脚本重复**：`kor_scan_fields2/3` 仅换了候选命名过滤词，应合并为一个带 `--dataset/--filter` 参数的脚本。

### 优化方案
- **O4（P0）统一字段扫描器** `scan_fields.py --dataset <id>`：调用 `get_datafields`（带 `type/coverage/userCount`），输出 `reference/kor_<dataset>_fields.json`（含类型），**取代 4 份 cache 依赖脚本**。
- **O5（P0）类型感知**：扫描结果写入 typed catalog；preflight 闸 3e 改为「字段.type==VECTOR ⇒ 必须经过 vec_* 包裹」的**数据驱动判定**，不再正则猜。
- **O6（P1）字段集持久化 + 复用**：catalog 作为 Stage ③④ 的输入，避免重复抽取。

---

## ③ 因子生成（Alpha Generation）

### 当前实现（代码实证）
- 生成由外部 LLM 技能 `brain-makeSomeGem` 完成，产物 `final_expressions.json`。
- `batch_validate_kor.py`：导入 `alpha-expression-verifier` 的 `ExpressionValidator`，**只做语法校验**（L14-22），有效表达式写入 `candidates/kor_pattern_scores_valid_exprs.json`。
- 现象：`validate_wave2v2.py` / `validate_wave3.py` 是 `batch_validate_kor.py` 的**逐波复制**，路径硬编码到各自 wave 文件。

### 问题诊断
1. **语法闸与白名单/类型闸分裂**：`batch_validate_kor.py` 只挡语法，字段白名单与类型要到 Stage ⑤ preflight 才查。中间生成的候选可能含未验证字段/错类型，直到提交前才暴露——浪费生成环节。
2. **重复验证器调用**：`batch_validate`（语法）与 `preflight`（语法再次 + 白名单 + 类型）两次调 `ExpressionValidator`，逻辑重复。
3. **生成非类型感知**：LLM 拿不到字段 type，持续产出 event 字段直套 `rank/ts_*`（wave2 事故）。
4. **逐波复制校验脚本**：`validate_wave2v2/3` 与 `batch_validate_kor` 同构，应参数化。

### 优化方案
- **O7（P0）合并为单一 Gate 步骤**：生成后跑一次 `gate.py`（语法 + 白名单 + 类型三合一），取代 `batch_validate` + `preflight` 两步。`preflight` 保留为「提交前最终确认」仍可独立调用。
- **O8（P1）类型感知生成**：把 Stage ② 的 typed catalog 注入 LLM 提示词（MATRIX/VECTOR 分流指令），从源消除 event 盲废。
- **O9（P2）校验脚本参数化**：`validate_wave*.py` 合并为 `gate.py --wave <n> --file <path>`。

---

## ④ 分层抽样选波（Stratified Wave Selection）

### 当前实现（代码实证）
- `select_wave1.py`：按表达式**前缀**分 9 桶（C1–C9），`PER_BUCKET=8`，字段集合去重，不足则回填，单波上限 48。
- 分桶逻辑是 `startswith` 匹配（L18-33）：`ts_delta`→C1、`subtract(ts_delta`→C4、`subtract(rank`→C2/C8、`multiply(rank`→C3、`divide(subtract`→C6、`add(multiply(rank(ts_delta`→C9、`subtract`→C5/C9。

### 问题诊断
1. **前缀分桶碰撞**：`ts_delta` 同时命中 C1（裸）与 C4（`subtract(ts_delta`），`subtract` 同时命中 C2/C8 与 C5/C9——C4/C5/C9 的归属是「谁先匹配」决定的，**分桶语义混乱**，分层抽样保多样的目标打折扣。
2. **纪律退化**：该脚本**仅用于 wave1**（`pattern_scores`）；wave17V 之后的后期 wave 直接内联生成、不再走选波，导致后期「多腿加权 + vec_avg」风格高度同质（战役多样性复盘指出算子探索率仅 ~12%）。
3. **无优先级**：每桶等权取前 8，未利用历史 near-miss（上一波 sh>1.0 的字段/算子应优先放大）。

### 优化方案
- **O10（P1）鲁棒分桶**：解析表达式的**算子树根/前两节点**而非 naive `startswith`，消除 C1/C4、C5/C9 碰撞；桶定义抽到可配置表。
- **O11（P1）全 wave 复用 + 优先级**：`build_wave.py` 接管所有 wave，输入候选 + 历史 near-miss 权重（来自台账），对接近门槛的字段/算子加权抽样。
- **O12（P2）单数据集平衡**：同一 wave 内跨数据集均衡，避免单数据集占满。

---

## ⑤ 三道预检闸（Preflight Gates）— 最成熟层

### 当前实现（代码实证）
- `kor_preflight_check.py`：闸1 语法（subprocess 调 `verify_expr.py`，L46-53）、闸2 字段白名单（L90-93）、闸3a MATRIX 禁 vec_*（L95-98）、闸3e VECTOR 事件字段须 vec_* 包裹（L99-117，正则剥离 vec_* 后查裸字段）、闸3b 不可访问算子 `ts_min/ts_max`（L118-121）、闸3c `quantile` 仅 1 参（L122-135）、闸3d 禁用模式（L136-142）。退出码 0/1 门禁。设计本身**是该战役最值得保留的资产**。

### 问题诊断
1. **每表达式一次子进程**：闸1 对 N 个表达式各 `subprocess.run([sys.executable, VERIFY_SCRIPT, expr])`（L48）——N 次 Python 进程启动，wave 大时显著慢。`batch_validate_kor.py` 已是 `import ExpressionValidator` 直接调，preflight 却退回子进程，不一致。
2. **闸3e 正则启发脆弱**：靠剥 `vec_*` 文本判断裸事件字段，对嵌套/别名会误判；应改为 Stage ② typed catalog 的数据驱动判定（见 O5）。
3. **默认白名单仅 chart_cnn**：`DEFAULT_WHITELIST` 写死 chart_cnn（L19），其他数据集需手动 `--whitelist`，易忘。
4. **无结果缓存**：同表达式重跑整轮重算。

### 优化方案
- **O13（P1）消除子进程**：preflight 直接 `from validator import ExpressionValidator`（与 batch_validate 一致），速度数量级提升。
- **O14（P1）白名单按数据集自动派生**：`--dataset <id>` 自动定位 `reference/kor_<dataset>_field_whitelist.json`，去掉默认硬编码。
- **O15（P2）数据驱动 3e + 结果缓存**：接 typed catalog；同表达式 pass/fail 落 `cache/preflight_cache.json` 幂等跳过。

---

## ⑥ 回测提交与固化轮询（Submit & Polling）

### 当前实现（代码实证）
- `kor_poll_pipeline.py`：`--multisim <id> [--wait N]`；COMPLETE→调 `kor_fetch_metrics.py` 拉指标；ERROR→逐 child 取 error（L64-72）。`--wait N` 仅睡 N 秒后**复查一次**（L97-101）。
- `kor_fetch_metrics.py`：支持 `<alpha_id>...` 与 `--multisim=<id>` 两种入口；multisim 分支登录一次取 children/alpha（L44-58），随后**再次登录**跑 per-alpha 循环（L62-64）；逐 `GET /alphas/{id}` 取 is 指标（L66-95），输出 JSON lines。
- `record_dayclose.py` 记录：「连续三批 CANCELLED 根因 = 平台日模拟配额耗尽」。

### 问题诊断
1. **`--wait` 只轮询一次**：非阻塞等待，要手动反复跑；无指数退避、无轮询到 terminal 的循环。
2. **重复登录**：`kor_fetch_metrics.py` 在 multisim 分支登录一次、per-alpha 循环又登录一次（L47 与 L62）；`kor_poll_pipeline.py` 的 `--wait` 重查时**新建 Api 再登录一次**（L99）。每进程多次认证，浪费且易触发限流。
3. **无指标缓存（高影响）**：每次 review 都重 `GET /alphas/{id}`。同 alpha 被多个 wave/review 引用时反复拉，**浪费 API 配额且慢**；这也是 review 被迫依赖外部 `.qoder-cn` cache 的诱因之一。
4. **无配额闸**：`record_dayclose` 已记录「配额耗尽→CANCELLED」，但提交路径无任何预检；应提交前查 `get_submission_quota`/当日 sim 计数，超阈值熔断。

### 优化方案
- **O16（P0）`--wait` 改轮询循环 + 退避**：`kor_poll_pipeline.py` 内 `while not terminal: sleep(backoff); poll()`，直到 COMPLETE/ERROR 或超时，免去手动重跑。
- **O17（P0）单进程单登录 + 复用 opener**：去掉 multisim 分支的二次登录；`--wait` 重查复用已登录 Api。
- **O18（P0）指标本地缓存** `cache/metrics/<alpha_id>.json`：`kor_fetch_metrics.py` 命中即返、未命中才拉，所有 review 复用 → 配额与耗时双降。
- **O19（P1）提交前配额闸**：提交脚本先查当日 sim/submit 余量，超阈暂停并告警（落实 `record_dayclose` 的教训）。

---

## ⑦ 指标评审与达标筛选（Review & Screening）— 最脆弱层

### 当前实现（代码实证）
- `review_wave1.py` / `review_wave3.py` / `review_wave5.py` 三份**结构同构**：硬编码 `SRC = r"C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\XXXX.txt"`（外部 agent cache，L4/L5），硬编码 `WAVE*_IDS` 集合，从 dump 里抽指标，按门槛 `sharpe>1.58 & fitness>1.0 & two_year_sharpe>1.6 & margin>0.0005 & 0.05<turnover<0.30 & failed_ra_count==0` 筛 candidates/near，写 `reviews/kor_waveN_review.json`。

### 问题诊断（最严重）
1. **硬依赖外部会话 cache（致命）**：`SRC` 指向 `.qoder-cn\cache\...\task-4d7\*.txt`——这是某次 agent 工具的临时 dump，**换会话即不存在**，且 `.txt` 非结构化（需 `t.find('{')` 切 JSON，见 `validate_wave2v2`/`scan_aieq` 同类写法）。评审步骤因此**不可复现、不可迁移**。
2. **阈值散落三处**：同一套门槛在 wave1/3/5 各抄一份，改一处需改三处，易漂移。
3. **每波一份脚本**：wave1/3/5 各一文件，新增 wave 就复制，与 select 的退化同源。
4. **未接台账**：candidates/near 只落 `reviews/`，未自动回写 `kor_d1_campaign_state.json` 的 `submit_ready`/`qualified_alphas`。

### 优化方案
- **O20（P0）评审消费指标缓存**：`review_wave.py --multisim <id>` 直接读 Stage ⑥ 的 `cache/metrics/`（按 alpha id），**彻底移除 `.qoder-cn` 硬依赖**，可复现可迁移。
- **O21（P0）阈值集中配置**：`config/thresholds.json` 一份，所有评审引用；新增 `IS_LADDER`/`LOW_2Y_SHARPE` 等闸门统一维护。
- **O22（P1）单脚本通用化 + 自动回写台账**：`review_wave.py` 取代 wave1/3/5 三份；输出自动 merge 进 `submit_ready`/`qualified_alphas`。

---

## ⑧ 多样性复盘与数据集切换决策（Diversity & Switch）

### 当前实现（代码实证）
- `kor_op_exploration_stats.py`：glob `candidates/kor_wave*.json`，正则抽算子，对比硬编码 `all_ops` 集合（L23-32），算出 `exploration_rate`（战役 ~12%）。静态、一次性。
- `kor_diversity_review_round10.md`：人工写的多样性量化复盘（算子探索率/字段探索率/模板骨架/信号风格）。
- 数据集切换：由 `record_*.py` 在每波 verdict 后手动 `waveXX_dataset_switch` 标记，属**事后反应式**。

### 问题诊断
1. **非累积**：`kor_op_exploration_stats.py` 每次重扫 candidates，不写入台账，无法看趋势（探索率是否随 wave 提升）。
2. **切换靠事后判断**：数据集是否 dead 要烧一整波才发现，无「预判→小批量探针→再决定」的自动闭环（与 O3 呼应）。
3. **算子盲区未驱动生成**：`unused_ops`（如 `ts_regression.resid`/`signed_power`/`trade_when`/`bucket`）列出却没回流到 Stage ③ 的 LLM 提示。

### 优化方案
- **O23（P1）多样性进台账**：每波跑完自动把「用过的算子集/字段集/骨架」写 `kor_d1_campaign_state.json` 的 `waves[].exploration`，累积出探索率曲线。
- **O24（P1）切换决策自动化**：规则化——「当前数据集 best<0.8 且已测 ≥40 式 且 论坛无解」⇒ 触发 `score_datasets.py` 取下一个蓝海 + 跑 `probe_battery` 预筛，再决定是否开正式 wave。
- **O25（P2）盲区回流生成**：把 `unused_ops` 注入 LLM 下一轮提示，强制探索未用算子。

---

## ⑨ 台账固化（Ledger Persistence）

### 当前实现（代码实证）
- 13 份 `record_*.py`（`record_p10`/`record_dayclose`/`record_cw_manual`/`record_whitelist_v2` + 9 份 wave verdict 记录），每份都是 `json.load(大JSON)` → 改 1–2 键 → `json.dump`。
- 4 份临时探针 `_tmp_w22gh/i/j/kl.py` 仍留在 `scripts/`。
- 写入直接 `json.dump(open(P,'w'), ...)`（如 `record_p10.py` L21），**无原子写**；台账 168 键，中断即可能损坏。
- 编码统一 `utf-8-sig`（正确，避 BOM 坑）。

### 问题诊断
1. **13 份近重复脚本**：维护成本高，改键名/结构要改 13 处。
2. **非原子写（风险）**：直接覆盖写，进程被中断（战役常跑整夜）→ 168 键台账损坏，战场记忆丢失。
3. **临时探针未清**：`_tmp_*` 4 份应删，污染 `scripts/`。

### 优化方案
- **O26（P0）统一台账 CLI** `kor_ledger.py`：子命令 `add-wave / set-verdict / add-whitelist / mark-dead / set-quota`，内部**原子写**（`tmp + os.replace`）+ 键存在性校验 + schema 守卫。取代 13 份。
- **O27（P1）删临时探针**：清理 `_tmp_w22*`，纪律写入 `polling_tooling_freeze`（已有）扩展为「scripts/ 禁临时文件」。

---

## 跨层系统性问题（3 类）

**A. 硬编码外部会话路径（最高危）**
`kor_scan_fields*.py`、`scan_aieq.py`、`review_wave1/3/5.py` 共 7 处硬编 `C:\Users\MENGTAO\.qoder-cn\cache\...\task-4d7`。这是某 agent 工具的临时 cache，换会话即失效、不可复现。→ 统一改为「本地 typed catalog + 指标缓存」（`reference/` + `cache/`），如 O4/O18/O20。

**B. 无端到端编排与断点续跑**
9 层是人工顺序跑的独立脚本，无 driver、无 checkpoint。长任务（整夜多波）中断只能靠台账手动续。→ `kor_pipeline.py` 配置驱动串联 ③→④→⑤→⑥→⑦→⑨，每步落 checkpoint 可 resume（呼应全局 user memory 的「断点续跑」纪律）。

**C. 配额/成本意识薄弱**
提交路径无配额闸；指标反复重拉；数据集 dead 靠整波试错。→ O16/O18/O19 + O3 的预筛闭环，把「每死一个数据集 = 烧一整波」降为「小批量探针即判」。

---

## 优先级优化路线图

| 优先级 | 编号 | 优化项 | 预期收益 |
|---|---|---|---|
| **P0** | O20/O21 | 评审去外部 cache + 阈值集中 | 可复现、可迁移，消除最大脆弱点 |
| **P0** | O18 | 指标本地缓存 | API 配额↓、review 耗时↓数量级 |
| **P0** | O4/O5 | 统一字段扫描 + typed catalog | 消除 event 盲废根因、类型预检数据驱动 |
| **P0** | O1/O2/O3 | 数据集自动评分 + schema 统一 + 探针预筛 | 数据集发现从 trial-by-fire 转低成本预筛 |
| **P0** | O26 | 统一台账 CLI + 原子写 | 防台账损坏、降维护成本 |
| **P1** | O7/O13/O14 | 单 Gate 合并 + preflight 去子进程 + 白名单自动派生 | 提速、减重复、防漏闸 |
| **P1** | O16/O17/O19 | 轮询循环+退避 / 单登录 / 配额闸 | 提交稳定、防 CANCELLED 浪费 |
| **P1** | O10/O11 | 鲁棒分桶 + 全 wave 复用 + 优先级 | 真正保多样、放大 near-miss |
| **P1** | O22/O23/O24 | 评审通用化+回写台账 / 多样性进台账 / 切换自动化 | 决策数据驱动、累积可观测 |
| **P2** | O8/O9/O12/O15/O25/O27 | 类型感知生成 / 校验参数化 / 跨数据集平衡 / preflight 缓存 / 盲区回流 / 清临时 | 收尾打磨 |

---

## 建议落地的统一工具骨架（供决策）

```
tracking/KOR/
  config/
    thresholds.json          # O21 集中门槛
    settings.json            # region/universe/delay/neut/decay 等固化
  reference/
    kor_<dataset>_fields.json   # O4 typed catalog（取代 scan_fields* + 外部 cache）
    kor_dataset_ranking.json    # O1 自动评分输出
  cache/
    metrics/<alpha_id>.json      # O18 指标缓存
    preflight_cache.json         # O15
  scripts/
    score_datasets.py   # O1+O3 评分+探针预筛
    scan_fields.py      # O4 取代 scan_fields*/scan_aieq
    gate.py             # O7 语法+白名单+类型 三合一
    build_wave.py       # O10/O11 选波
    kor_poll_pipeline.py # O16/O17 轮询循环+退避+单登录
    kor_fetch_metrics.py # O18 指标缓存
    review_wave.py      # O20/O21/O22 通用评审+回写台账
    kor_ledger.py       # O26 原子写 CLI
    kor_pipeline.py     # 跨层编排+断点续跑
```

> 保留并强化：`kor_preflight_check.py` 的三道闸设计（仅改造调用方式）、`polling_tooling_freeze` 纪律、`utf-8-sig` 台账编码、168 键战场记忆模式。

---

## 结论

该 KOR 战役的**流程骨架是对的**（体检→白名单→生成→选波→预检→轮询→评审→多样性→台账），且沉淀了极具价值的实战纪律（双门槛破互斥、三道预检闸、`utf-8-sig` 台账、战场记忆、配额耗尽教训）。主要问题集中在**工程化与可复现性**：

1. **最大风险**是 7 处硬编 `.qoder-cn` 外部 cache（Stage ②⑦），导致字段扫描与评审不可复现——优先 O4/O18/O20 解决。
2. **最大浪费**是数据集 dead 靠整波试错 + 指标反复重拉（Stage ①⑥）——优先 O1/O3/O18 解决。
3. **最大脆弱**是 13 份 record 脚本直写非原子（Stage ⑨）——优先 O26 解决。
4. 预检闸（Stage ⑤）本身设计优秀，仅需工程改造（去子进程、数据驱动 3e）。

按 P0 六项落地后，该流水线可从「依赖特定会话 cache 的手工链路」升级为「本地缓存驱动、可断点续跑、配额感知」的标准挖掘工程，且对所有区域（USA/GLB/MEA）通用。

---

*本文逐层展开基于 `tracking/KOR/` 真实代码（23 脚本 + 168 键台账 + 21 白名单），所有「事实」均标注了脚本/行级依据，「建议」以 O 编号与 P0/P1/P2 优先级区分。*
