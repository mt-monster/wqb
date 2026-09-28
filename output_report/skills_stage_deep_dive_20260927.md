# Skills 九阶段深度展开、价值评估与全流程模拟演练

> 日期：2026-09-27 · 性质：**纯评审与模拟演练，未修改任何文件/库/配置**
> 对象：`wq-brain-ra-pipeline` 九步流水线（唯一编排 SOP）及其每步映射的 skill / 节点 / 脚本
> 判据三条（全部实证，不以文档自述为准）：
> ① **漏斗定位**——去哪一跳掉得最狠（`tools/step_funnel.py` 只读推导）；
> ② **失败模式实证**——本轮实测缺陷（verdict 污染 73 行、LLM 402 假绿、`--regions all` SSL EOF、multisim 连坐、`--submit` 误读等）；
> ③ **维护成本**——重复实现 / 断链 / 无入边 / 死路分支。

---

## 0. 评审基准（先立标尺）

| 指标 | 实测值 | 来源 |
|---|---|---|
| `expressions` 总量 | 65,580（回测率 12.6%） | 全库 09-26 快照 |
| `gate_results` | 1,502 批次（全过 49.7%） | 同上 |
| `wave_results.verdict` 终态 | FAIL 567 / PARTIAL 284 / PASS 92 / NULL 1（本轮治理后） | 本轮迁移实测 |
| 端到端转化 | 65,580 → 65 提交 = **0.10%** | 同上 |
| GBR 漏斗 | 8,710 生成 → 913 放行 → 722 回测 → 65 过廉价闸 → **4 就绪**（瓶颈=过廉价闸→就绪，保留率 6.2%） | step_funnel 只读 |
| IND 漏斗 | 2,748 → 188 → 782 → 228 → **0 就绪**（批次门禁通过率仅 19.7%，表达式级 100% 放行） | 同上 |
| 测试基线 | 1,445 passed / 0 failed（本轮治理后） | pytest 实测 |

**两条贯穿结论**（沿用 09-26 评审，本轮继续成立）：
1. gate 不是瓶颈，**prod 相关性（68% 淘汰）与「过廉价闸→就绪」跳变才是**；
2. 作用点在 IS 优化/生成量的环节价值有限，**作用在结构性降相关与库存复用的环节价值最高**。

---

## 1. 逐阶段展开（输入 / 处理过程 / 输出）

### 步 1 · S-PRE 查表 + 库存盘点

**谁执行**：`wq-brain-ra-pipeline` 编排 + `mcp__wqb-db__get_*` 查询族 + `tools/build_gate_prior_from_inventory.py` / `select_ra_basket.py`；可选并行 `brain-next-move-analysis`、`brain-forum-browse`

- **输入**：`$REGION`（唯一输入）+ 区域 profile（`references/regions/<R>.md`，13 份，`entry_verdict` 裁决）+ DB 四表存量 + `reports/dataset_experience/*_campain.md` 经验台账
- **处理过程**：
  1. 读 profile → 按 front-matter 渲染本区 SOP（frozen 区步 1 即拒）；
  2. `get_campaign_summary / get_dead_ends / get_dead_datasets / get_mining_yield`（strict 口径）→ 区/集先验；
  3. **库存盘点（先清库存再开新挖）**：`build_gate_prior_from_inventory --emit-candidates --write-priors` → `select_ra_basket --target 20`（去参数网格 + OS 撞车预筛 + 篮内正交 + 平台 detail 端点复核）；
  4. PPA 主题门禁：`get_messages` 扫 Power Pool 公告，解析当期主题 region/delay/universe。
- **输出**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号；库存够则产出 `cache/basket.json` 并**短路开新挖**。
- **失败分支**：registry 全空=新区域；候选池不足才进步 2。

### 步 2 · S0 数据集体检 + 金字塔配置

**谁执行**：`mcp__wq-brain-http__workflow_campaign(stage="S0")` + `tools/campaign_intel.py s0-select` + toolkit `score_datasets.py --calibrate`

- **输入**：`get_datasets` 平台清单 + `get_pyramid_alphas` 实测点亮状态 + `region_kb` win 层 + `saturated_datasets` 台账 + 本地 `field_inspect_*` 体检包存量
- **处理过程**：
  1. `campaign_intel s0-select` 三方交叉：`recommend_datasets`（平台塔状态）× `get_mining_yield`（严格口径历史产出率）× `get_dead_datasets`（判死清单）→ 候选清单带 `hist_yield_rate / maxS / fld / est_seats`；已点亮塔（lit=Y）直接剔除；跨区负先验沉底；
  2. `calibrate`（反学 category 权重+拥挤甜区，写 thresholds）→ 裸 `stage="S0"` 打分产 `s0_ranking`（两步必需，① 不产排名）；
  3. 座位可达性：Σ`est_seats` < target → `[WARN] 结构性不可达`，扩集/换区；
  4. 锁白名单 → `upsert_ledger_key(region,"s0_whitelist",…)` → **开区硬前置**：补齐 `field_insight` 体检包（缺包可 `--inspect-mode warn` 降级但必须台账记因）；
  5. 饱和路由：`alphaCount ≥1 万` 或连续 2 波模板全灭 → 强制切 hypothesis-first。
- **输出**：`s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` 台账 + 白名单数据集族。
- **失败分支**：配额后无非 MODEL → 写 findings；全硬排除 → 回步 1 换区。

### 步 3 · S1 字段扫描 + 理解

**谁执行**：`workflow_campaign(stage="S1")`（toolkit `scan_fields.py`）+ 按需加载 L1 三件套 skill + `workflow_feature_engineering`（收口后仅人读参考）

- **输入**：白名单数据集 + `get_datafields`（类型/覆盖率/users 热度）
- **处理过程**：
  1. typed catalog 落地（`fields` 表 + ledger `s1_<ds>_d<delay>`）；
  2. **字段级覆盖审计**（`catalog_<ds>` coverage>0，覆盖为空写 `<ds>_dead` 防复用）——铁律①；
  3. **幽灵字段验活**：`create_multi_simulation(validate_fields=true)`——铁律②（DB 有记录但平台 unknown variable → 提交层 COMPILE_ERROR）；
  4. users 分级：≥50 只验证不投入 / 10–49 进池必实测 prod / 0–9 优先（冷门字段占批 ≥50%）。
- **输出**：`field_catalog` + S1 ledger 决策 + `ideas_md_path`（仅 LLM/人工产出的才允许后续注入 GEM）。
- **失败分支**：字段 <10 退回步 2 白名单外；VECTOR 比例确认后步 4 传对 `data_type`。

### 步 4 · S2 概念优先生成（GEM）

**谁执行**：`mcp__wq-brain-http__workflow_gem` → `brain-make-some-gem/scripts/headless_runner/run.py`（内部调用 brain-feature-implementation / brain-data-feature-engineering 两份 SKILL.md 拼进 prompt）

- **输入**：priors 快照（`assemble-priors` 从 DB KB 确定性组装，fail-closed）+ S1 catalog + ideas 注入（仅 `source∈{s2_nested,手写}` 的文档）+ `config.json`
- **处理过程**（GEM 内部五子步）：
  1. `assemble-priors`：`wins(≤6)+dead_ends(≤12)+region_context` → `priors_snapshot_<region>`（含 sha256）；
  2. LLM 概念生成：机制 → 1–2 字段 id → Implementation Example（phased=族模板 / skeleton=代码组装保证语法）；
  3. 复杂度预算：默认 2–5 算子，8 概念 ≥3 个 ≤4 算子（859 条过闸样本：46% 过闸者 ≤4 算子）；
  4. `pipeline_pregate` 落盘前预闸：quantile 归一、毒模式丢弃、hump/bucket 参数补全、非标窗口归一、**同骨架换字段封顶**（`WQB_GEM_MAX_PER_SKELETON` 缺省 12）；
  5. 落 `final_expressions.json` → 入库 `expressions(status=gem/enhanced)`——**DB 为真相源**，json 仅中间产物。
- **输出**：`expressions` 新行 + `expression_count / quality_estimation / mode_b_required`。
- **失败分支**：401/402/403 立即抛（本轮已修，带 `--ideas-file` 绕行指引）；GEM 未入库先查 `--status <task_id>`；候选不足 enhance/扩组合/换集。

### 步 5 · S2→S3 门禁（含 5b prod-first 探针）

**谁执行**：`tools/wave_gate.py`（一键）→ toolkit `gate.py check_batch_diversity` + `field_inspect_gate.py` + `campaign_intel ghost-audit` / `prod-first`

- **输入**：本波 `expressions`（`--from-db`）+ typed catalog + 体检包 + `platform_constraints.json` + `explore_contract` 契约 + `alphas` 表 prod 记录
- **处理过程**：
  1. **幽灵算子硬闸**（纯本地零配额，先拦——含幽灵算子整批 CANCELLED 连坐）；
  2. `gate.py` 8 闸：语法(含元数)/字段白名单/VECTOR 类型/不可访问算子/毒模式/**闸6 批级多样性**（唯一执行口径，判据三源：自学习契约+收益来源多样性+家族天花板）/longCount/EVENT；闸 2b 区域非法 group 字段；
  3. **体检硬门**：低覆盖须 ts_backfill / 高偏度须 rank / 厚尾须 rank / 单边水平禁用 / 稀疏事件须 trade_when；
  4. **闸 PF（prod-first 前置）**：骨架级指纹（前 2 个算子调用名）查 prod 史——已探死拦整波（fail-closed）、已探明干净放行、新指纹 WARN；
  5. 5b 新信号族 prod-first 探针：族首探 prod ≥0.7 记 dead_end 换机制，不做去相关变体。
- **输出**：`gate_results`（`all_pass`/`fail_reasons`）+ 台账 `prod_first_<wave>`。
- **失败分支**：语法 FAIL 必修；多样性 FAIL 回步 4 补骨架（可查 `KB/community_tpl_kb`，先查 ghost advisory）；repair/probe 批豁免多样性契约。

### 步 6 · S3 七槽回测

**谁执行**：`workflow_batch_track` / toolkit `pipeline.py run`（并发唯一来源 `wqb-concurrency` §8）

- **输入**：过闸批次 + `settings.json` + `region_kb.gate_priors`（设置层先验）
- **处理过程**：
  1. 装载 settings → `apply_settings_prior`：by_decay/by_neutralization 样本 ≥30 且过闸率 ≥当前×2 自动改写本波设置（GBR decay 3.9%→28.3% lift×7.2 实证）；显式 `--set` 钉住不动；
  2. 七槽填槽（Token-Bucket C≈7，multi(8) 86.1 α/hr = single 1.59×）；账户级槽位仲裁（`logs/_slots/` token 文件，跨进程 WQB_GLOBAL_SLOTS=7）；
  3. 发批（batch_size≤8）→ 轮询 → **连坐隔离**（解析 ERROR 子模拟定位坏式 → 回写 fail → 无辜式作重发批优先下槽）；
  4. 收批压缩：`harvest_multisim_alphas` + `harvest_multisim_results`（18 次调用链→2 次）；
  5. 积压检查：pending+gated > 2× 本波 → S2→S3 断链，禁止无脑新建堆库。
- **输出**：`backtest_results` + `wave_results` + `ckpt_w<W>` checkpoint + `expressions.status=backtested`。
- **失败分支**：故障协议表（8 子全 ERROR 重发 / CROWDING 跳过 / fatal 算子隔离 / 429 退避 / took-too-much-resource 是真问题去 backfill）。

### 步 7 · S4 诊断改进

**谁执行**：`workflow_campaign(stage="S4")`（`review_wave.py`）+ `campaign_intel s4-prescreen / prod-first` + `brain-how-to-pass-alpha-test` + `wq-brain-alpha-optimization-v1`（Mode B 70%/Mode A 30%）

- **输入**：本波 `backtest_results` alpha_id + `thresholds.review` + OS 衰减基线（`alphas.os_*`）
- **处理过程**：
  1. **s4-prescreen 分层**：REJECT（全灭）直接判死不进链，只对 READY/REVIEW 走完整链（效率 ≈8×）；
  2. `review_wave` walls 诊断 + `RN_EXPOSURE` 墙（risk_neutralized ≤0 且 sharpe≥1.58 ⇒ 就是那个暴露本身，判 dead_end 禁调参）+ near 池拒收结构性死信号（robust ratio<0.5 不入 near）；
  3. **prod-first 探针（收批后必调）**：每信号族最强 1 条串行探平台 prod，STOP(≥0.7) 族不再扩变体；
  4. `os_calibration`：expOS = IS×0.358（USA 124 例），只作期望值参考不抬阈值（IS/OS Spearman 仅 +0.086）；
  5. 卡闸辅助腿检索：`get_salvage_pool boost_*`，**禁止加权混合**（仅结构交互）。
- **输出**：ledger `s4_walls_<region>_<wave>` + `salvage_pool` + review payload + 换概念/换腿决策。
- **失败分支**：prod ≥0.7 → Mode B 换概念；同一想法 >10 结构不过 → 步 9 记 dead_end 回步 2。

### 步 8 · S4→S5 稳健闸 + 提交判定

**谁执行**：`brain-alpha-robustness`（S4→S5 必经）+ `mcp__wq-brain-http__submit_verdict`（唯一权威）+ `worldquant-submit-alpha`（确认后执行）

- **输入**：达标候选 + `is.checks` 全量 + WebDataScope failed-counts 规则
- **处理过程**：
  1. Failed-count 资格门：REGULAR 要求 Failed RA==0（WARNING/ERROR 也计数），比 `result=="FAIL"` 严格；
  2. `submit_verdict` 零成本判定（模拟层 checks + GET submit 双视图；`degraded_gates` 非空 ⇒ verdict 不可作依据）；
  3. **prod 0.60–0.70 当天提交不做变体**（pv103 血的教训：1 小时内被外部同款封死整族）；
  4. 报告 SUBMITTABLE → **等用户确认**，确认前禁止任何提交调用；
  5. POST 四形态处置：①200 通过→轮询 ACTIVE；②201 异步→4min 未翻状态 re-POST；③200 空体=未知→必须补发；④403 零成本带回全量 checks 据此判死。
- **输出**：`submit_ready` 台账 + ACTIVE alpha（配额 REGULAR 4 + SUPER 1 + PPA 1，三者并行）。
- **失败分支**：PROD/SELF 不过回步 7；配额耗尽挂起提交继续步 2→9。

### 步 9 · S6 复盘回写

**谁执行**：`tools/step_funnel.py`（开步看漏斗）+ `upsert_wave_result / upsert_registry_empirical / upsert_ledger_key` + `campaign_intel pyramid` + `dataset-experience` + `seal_dead_end`

- **输入**：本波四表存量 + ledger + 平台塔状态
- **处理过程**：
  1. `step_funnel` 定位本波掉得最狠的一跳（只读，不凭印象写 verdict）；
  2. `upsert_wave_result`：verdict **只接受 PASS/FAIL/PARTIAL**（MCP 层归一+拒绝；直写路径本轮已堵——`DirectDBWriter` 注入归一，描述性值进 `key_findings`）；
  3. 判死封存：先 `seal_dead_end` 沉降候选入 salvage_pool，再记 dead_end（残值回填）；
  4. **region_kb 自动刷新**（pipeline `--review` 内置）：`recent_waves`（近 20 波）+ `gate_priors_local` + `updated_at` → 下一波先验自动变新；
  5. `campaign_intel pyramid` 点塔进度进 key_findings；`dataset-experience` 逐集中文经验沉淀；
  6. prod 饱和反馈 S0：全族 prod 卡死 → `submit_ready_blocked` 追加饱和记录，下轮 S0 按拥挤降优先级。
- **输出**：`wave_results.verdict` + `registry_empirical` + `s6_verdict_<wave>` + `reports/dataset_experience/*.md`。
- **失败分支**：停止闸 B1/B2 机械判定（同轴 3 连可计数 FAIL 熔断 / 窗口内 ≥4 轴全 FAIL 停区；零配额与产出新 dead_end 的 FAIL 波豁免；用户显式 override 写台账留痕）。

---

## 2. 逐阶段价值评估（保留优化 vs 精简去除 + 依据）

### 汇总表

| 阶段 | 判定 | 核心依据（实证） |
|---|---|---|
| 步 1 S-PRE | **保留并深入优化** | 09-07 实证：170 次新回测 0 产出 vs 一次库存扫描 20 条（数量级差异）；严格口径防先验高估（IND 旧口径 34% 实际可提交 0） |
| 步 2 S0 | **保留优化，但饱和路由分支待决** | 已点亮塔剔除治本（IND 7 集 197 条 0 候选）；座位可达性防结构性浪费；**饱和路由指向 hypothesis-first 是死路**（catalog 仅 1 文件、无生成器、dry-run 唯一 FAIL） |
| 步 3 S1 | **保留（两条铁律落点）+ 已去除模板注入** | 覆盖审计+幽灵字段验活是提交层 COMPILE_ERROR 的唯一前置拦截；`workflow_feature_engineering` 模板注入已实证让 GEM 零 LLM 退化（GBR intraday_pv_feats）→ 该路径已去除（节点与 runner 双跳过） |
| 步 4 S2 GEM | **保留并深入优化（当前最优先）** | 65,580 条的来源；但 LLM 402 曾使 S2 实际不可用于新生成 → 本轮已修不可重试错误 + `--ideas-file` 旁路固化；pregate 同骨架封顶治 7538 条同质堆（JPN 实证） |
| 步 5 门禁 | **保留（最硬守门员）** | IND 批次级通过率 19.7%（多样性闸才是真实作用点）vs 表达式级 100%——说明闸 6 批级口径不可删；闸 PF 把 prod 检查前移（IND 24 条报废教训）；**已知断链：约 1300 条 `s2_*` 命名表达式无 gate 记录**（待用户决策） |
| 步 6 S3 | **保留，`--submit` 默认值已修** | 回测率 12.6% → S2→S3 断链是真实积压（GBR unconsumed 86.3%）；连坐隔离自动化/槽位仲裁/收批压缩均高价值；`submit=True`→`False`（D8）治"提交回测"被误读为"提交 alpha" |
| 步 7 S4 | **部分精简：保留 prescreen/prod-first，压缩 Mode A** | "优化 IS 几乎不产生终局价值"（prod 墙 68% 淘汰、Mode A 实测仍撞 0.84–0.85）；s4-prescreen 8× 效率保留；RN_EXPOSURE 硬规则保留（HKG 7 条 6 条假信号实证）；`brain-alpha-repair` 仅配方查表 → 并入 optimization-v1 参考即可 |
| 步 8 S4→S5 | **保留（终局执行层）** | 65 颗 ACTIVE 的唯一路径；四形态补发闭环是本轮硬知识（3 颗悬空 >24h 教训）；PPA 主题闸两次不过 → 等轮换，重试无效（不删，标 WAIT_THEME_ROTATION） |
| 步 9 S6 | **保留，枚举治理已闭环** | verdict 治理后终态 FAIL 567/PARTIAL 284/PASS 92，读取端归一使停止规则 B 熔断判据恢复有效；step_funnel 恒不填五张 `step_*` 空表（裁定）；`brain-dataset-mining-experience` 是正面样板 |

### 精简/去除明细（跨阶段）

| 项 | 处置建议 | 依据 |
|---|---|---|
| `workflow_feature_engineering` 的 ideas 注入路径 | **已去除**（保留人读参考） | GEM 零 LLM 退化实证；节点/runner 已双跳过 `source∈{feature_engineering_node, standalone*}` |
| 饱和路由 → `brain-alpha-research-hypothesis-first` | **二选一**：补假设目录生成器，或摘除路由改"连续 2 波全灭→换集" | 死路分支留着 = 假熔断保险丝 |
| `brain-alpha-research-field-quality` / `news-sentiment` / `alpha-template-labs-data-analysis` | **摘除或并入**（无入边+零产出+引用失效） | `WebData_*.zip` 实为目录、CLI 不存在、DEU 0 覆盖 |
| `brain-alpha-repair` | 并入 optimization-v1 作附录 | 43 行纯查表，命中 0 边界词 |
| `wqb.expression.validator.check_batch` 双口径 | **已收敛**（P2-10） | 全仓零调用方，只留方法论参考 |
| 五张 `step_*` 空表 | **裁定恒不填** | 反事实估算无客观来源；步级视图用 step_funnel |
| `planning-with-files` hooks | 收敛触发条件 | 全局注入在 WQ 任务产生副作用 |
| `pull-brain-skills --dest` | 待修：加 layer/命名校验 | 默认直写权威目录无守卫 |
| GEM `config.json` 明文凭据 | **待用户决策**迁 `.env` | 安全卫生，非功能缺陷 |
| 游离 skill（`brain-enhance-template` / `wqb-test-failure-triage`） | **待用户决策**收编或排除 | 有价值但不在 skill 树权威清单 |

---

## 3. 全流程模拟演练（GBR / 零修改）

> 演练设定：用户指令「继续在 GBR 挖」。**以下全部为推演**：不调平台、不写 DB、不改文件；
> 带处标注〔实证〕的数字来自本轮 step_funnel 只读读取，带〔假设〕的为演练推演值。

### 演练总览（九步实际走位）

| 步 | 演练结局 | 原因 |
|---|---|---|
| 1 S-PRE | **走完，触发短路** | 库存足够（7518 未消化），不开新挖 |
| 2 S0 | **跳过**（库存路径不需要白名单） | 快捷入口：发批路径直接进步 5 |
| 3 S1 | **跳过**（不产新 catalog） | 同上 |
| 4 S2 | **跳过**（零 LLM 消耗） | 库存篮子替代新生成 |
| 5 门禁 | **执行**：20→16 条 | 多样性/体检/幽灵三闸各拦少量 |
| 6 S3 | **执行**：16 条七槽回测 | 断点续跑就位 |
| 7 S4 | **执行**：2 条进 prod 探针，1 生 1 死 | prod-first 前移 |
| 8 S4→S5 | **停在用户确认前** | SOP 铁律 |
| 9 S6 | **执行**：PARTIAL 回写 + 先验自动刷新 | 闭环 |

### 逐步推演

**步 1 S-PRE**
- 输入快照〔实证〕：GBR `expressions` 8,710 条，unconsumed 7,518（86.3%）；`wave_results` FAIL 71 / PARTIAL 10 / PASS 3；`submit_ready`=4。
- 处理：读 `GBR.md` profile（entry_verdict=active）→ `get_mining_yield --region GBR`（strict 口径）→ **库存盘点**：`build_gate_prior_from_inventory --regions GBR --emit-candidates --write-priors`（注意 D4 修复后默认即本区，不会触发 `all` 并发 SSL EOF）→ `select_ra_basket --target 20`。
- 输出变化〔假设〕：`cache/candidates.json` ≈180 条资格行 → 篮内正交去重 → `basket.json` 20 条；`gate_priors` 台账刷新（过闸率先验，供未来波次消费）。
- **价值判定落地**：S-PRE 保留判定的活证明——它把本次战役从"重新生成一波注定低产的表达式"改写为"复用库存 20 条"，省掉 S2 的 LLM 全链与 4/5 的重复门禁消耗。**短路成功**。
- 停止闸预检〔实证→假设〕：B1 同轴检查——GBR 最近 closed 波若连续 3 个可计数 FAIL 会拒开波；但本次走**发批快捷入口**（用户已给篮子→直接步 5），不触发开波闸；如实记录该豁免依据到台账。

**步 5 门禁**
- 输入〔假设〕：篮子 20 条（以 `--exprs-file` 传入，不依赖 wave 命名，避开 s2_* 断链问题）。
- 处理：ghost-audit → `wave_gate.py --campaign-dir tracking/GBR --exprs-file …`（闸 1–5 + 闸 6 多样性 + 体检硬门 + 闸 PF）。
- 输出变化〔假设〕：4 条被拦（1 条含未验证算子、2 条同 exposure 批级多样性 FAIL、1 条低覆盖无 ts_backfill）→ 16 条过；`gate_results` +1 批次（all_pass=0 或 1 取决于整批口径）。
- **价值判定落地**：闸 6 批级口径是本步唯一产生真实拦截的闸（对照 IND 表达式级放行率 100%）——**不可精简**；闸 PF 对库存旧式给出 WARN（骨架无 prod 记录），提示步 7 探针必做。

**步 6 S3**
- 输入〔假设〕：16 条过闸 + `settings.json`（GBR 现行 decay/中性化）。
- 处理：`apply_settings_prior` 查 `gate_priors_local`（GBR decay 维度样本若 ≥30 且 lift≥2 → 自动改写并打印 lift 行；本演练假设无命中，维持现设置）→ 七槽填槽（16 条 = 2 批 batch8）→ 发批轮询 → 收批压缩 2 次调用入库。
- 输出变化〔假设〕：`backtest_results` +16 行；`expressions.status` 16 条 `selected→backtested`；`ckpt_w<新>` 写 checkpoint（中断可续跑——用户铁律）。
- **价值判定落地**：断点续跑/槽位仲裁/收批压缩三个高价值优化全部落在这一步；S2→S3 断链治理（积压检查）再次确认"本波只回测库存、不新增生成"，阻止 unconsumed 比率进一步恶化。

**步 7 S4**
- 输入〔假设〕：16 行回测结果，2 条过廉价闸（S>1.58 & F≥1.0），其余 14 条 REJECT 直接判死不进链。
- 处理：s4-prescreen 分层 → 对 2 条走 `prod-first` 探针（串行、单并发、`--probe-timeout 600`）→ 结果〔假设〕：候选 A 族 prod=0.55（干净→EXPAND）；候选 B prod=0.74（STOP→记 dead_end，**不做去相关变体**——铁律：bucket/门控/平滑实证破不了 prod 墙）。
- 输出变化〔假设〕：`alphas.prod_correlation` 2 行回填；ledger `prod_first_<w>` 新键；候选 B 经 `seal_dead_end` 沉降入 `salvage_pool`。
- **价值判定落地**：prod-first 前移是本轮价值最高的新增（对照 IND 价量反转连投 3 波 24 条后才撞墙的旧账）；RN_EXPOSURE 墙与 near 池过滤在本例未触发但保持常开。

**步 8 S4→S5**
- 输入〔假设〕：候选 A（S 2.1 / F 1.2 / prod 0.55 / robust 过）。
- 处理：Failed-count 资格门（Failed RA==0）→ `submit_verdict` → 假设返回 READY 且无 `degraded_gates` → **报告用户并停在确认前**。
- 输出变化〔假设〕：`submit_ready` 台账该行状态 READY；无任何 POST。
- **价值判定落地**：三重防呆（资格门/verdict 权威/用户确认）在演练中无一可跳过——步 8 判定"保留"无争议；prod 0.55∈(0.5,0.7) 属"当天提交不做变体"窗口。

**步 9 S6**
- 输入〔假设〕：本波 16 回测 / 2 过廉价闸 / 1 就绪 / 1 dead_end。
- 处理：`step_funnel --region GBR --wave <新>`（瓶颈定位）→ `upsert_wave_result verdict=PARTIAL`（枚举校验：1/2 路径就绪→PARTIAL 而非 PASS；描述写 `key_findings`）→ `upsert_registry_empirical`（若 A 最终 ACTIVE 则 add-win）→ `campaign_intel pyramid` 进 key_findings → `dataset-experience` 补中文复盘 → pipeline `--review` 自动刷新 `region_kb.recent_waves / gate_priors_local`。
- 输出变化〔假设〕：`wave_results` +1 行（verdict=PARTIAL，通过归一校验）；`region_kb.updated_at` 前移；下一波 S-PRE 读到的先验即含本次。
- **价值判定落地**：步 9 是唯一让九步成"环"的步骤——region_kb 自动刷新使步 1/4/6 的先验无需人工回写即更新；verdict 枚举闸保证停止规则 B 计数真实。**保留，且本轮治理（写入端归一+拒绝）正是它的修复成果。**

### 演练总账

- 实际执行 5 步（1/5/6/7/8/9），跳过 3 步（2/3/4，因库存短路）——**这正是步 1 价值的直接度量**：一次短路省掉约 60–70% 的平台与 LLM 消耗。
- 唯一新增平台相关消耗：2 次 prod 探针（串行零并发风险）+ 2 批回测。
- 全程零文件/零 DB 变更（演练声明兑现）。
- 演练暴露的 2 个待决事项：① 约 1300 条 `s2_*` 断链表达式是否回填门禁记录（本次演练用 `--exprs-file` 绕开，但长期应回填）；② 停止闸对"发批快捷入口"无拦截覆盖——是否给快捷入口也加 B1 预检，待用户定。

---

## 4. 审阅清单（请确认）

1. **阶段判定**：九步中 7 步"保留/保留优化"、1 步"部分精简"（S4）、1 项死路分支待决（饱和路由）——是否认可？
2. **摘除候选**：`brain-alpha-research-field-quality` / `news-sentiment` / `alpha-template-labs-data-analysis` / `brain-alpha-repair` 四个摘除/并入建议——是否执行？
3. **饱和路由**：补 hypothesis-first 生成器（成本高）vs 摘除路由改"换集"（成本低）——选哪个？
4. **此前三项待办**（未动）：游离 skill 收编 / GEM `config.json` 迁 `.env` / 1300 条断链回填——哪些立项？
5. **新发现**：发批快捷入口是否纳入停止闸 B1 预检？
