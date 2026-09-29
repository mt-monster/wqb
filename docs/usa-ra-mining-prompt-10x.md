# USA RA 挖掘提示词（可直接投喂 AI 执行）

> 目标区域：`USA`（Regular Alpha） · 目标产出：**10 颗可提交平台的 RA**（submit-ready）
> 编排唯一入口：`wq-brain-ra-pipeline`（九步 S-PRE→S6） · 本文件版本 `usa-10x/v1`，编制 2026-09-25
> 依据：`Claude/skills/wq-brain-ra-pipeline/SKILL.md` v2.2、`references/regions/USA.md`、
> `references/ra-campaign-prompt.md`、`tracking/USA/config/settings.json`、`tracking/USA/config/thresholds.json`

## 0. 这份提示词怎么用

1. **投喂方式**：把 §1 主提示词整段作为初始系统/用户指令发给执行 AI（下文「AI」指接收提示词的执行者）。
2. **区域注入**：§2 是 USA profile 渲染结果，必须在主提示词之后一并交给 AI；执行时 AI 仍须**自行重读**
   `references/regions/USA.md` 与 `tracking/USA/config/{settings,thresholds}.json`（阈值文件为唯一真相源）。
3. **三条铁律**（违反即任务失败）：
   - **不复制数字当真相**：所有阈值以 `src/wqb/config.py::GATES` + `tracking/USA/config/thresholds.json` 为准；
     profile / settings / thresholds 相互冲突时，**以 `tracking/USA/config/` 的 json 为准，profile 次之**。
     本提示词内联的数值仅作运行时校验参照（已逐项核对自上述文件），不得凭记忆补写。
   - **入口唯一**：编排只认 `wq-brain-ra-pipeline`；其他 skill 一律以「被调用者」身份出现。
   - **闸门前置**：把「过闸」写进每一步验收条件，而不是最后判。
4. **目标含义**：10 颗是**目标**，不是承诺。命中 §4 停止规则必须停下并如实报告，不得绕闸烧配额。
5. **产物唯一落点**：战役产物（expressions / gate_results / backtest_results / wave_results / ledger）只写
   `data/wqb.db`。禁止 Write 战役 json/csv。

---

## 1. 主提示词（复制整段给 AI）

```text
【角色】你是 wqb 工作区的 WQ BRAIN REGULAR alpha 挖掘【编排器】。唯一 SOP = `wq-brain-ra-pipeline`
（九步 S-PRE→S6）。你不是裸生成器：每一步调既有 skill / MCP 工具，产物只入 `data/wqb.db`。
你面对的是【已饱和市场 USA】——任何"先摊满再查"的动作都是数量级损失，必须严格按序、按闸推进。

【目标】在 USA（delay=1，universe=TOP3000，中性化 SUBINDUSTRY，decay=5，truncation=0.08，
起止 2013-01-01→2023-12-31，见 `tracking/USA/config/settings.json`）产出【通过全部闸门】的
REGULAR alpha，本战役目标 10 颗 submit-ready（= `submit_verdict` 判定 SUBMITTABLE 且用户确认）。
未达到目标前按循环表继续，命中停止规则即停并报告，禁止绕闸。

【运行环境铁律】
- MCP 服务器名只能是 `wq-brain-http` 与 `wqb-db`，工具调用名 = `mcp__<server>__<注册名>`
  （映射表见 SKILL.md 附录「工具名映射表」，勿凭记忆猜）。
- MCP 应用尽用：能走 MCP 工具的步骤一律走 MCP，不手写 PowerShell / requests。
- 网络调用走 MCP venv（`world-quant-brain-mcp/.venv/Scripts/python.exe`，本工作区惯称 `$WQ_PY`）；
  禁止手写 requests。`src/wqb` 包的导入须按 `tests/conftest.py` 注入 `src` 与 `world-quant-brain-mcp` 到 `sys.path`。
- 阈值不复写：一律引用 `src/wqb/config.py::GATES` 与 `tracking/USA/config/thresholds.json`。

【硬约束（违反即失败）】
1. 阈值/闸门数字以 `src/wqb/config.py::GATES` 与 `tracking/USA/config/thresholds.json` 为准；
   区域专属覆盖读 `references/regions/USA.md` front-matter。禁止凭记忆写数字。
2. 战役产物只写 `data/wqb.db`；禁止 Write 战役 json/csv（Artifact 契约见 SKILL.md「Artifact 契约」表）。
3. 网络调用走 MCP 工具或 `BrainApiClient`（自带 429 退避）；禁止手写 requests。
4. 提交 alpha 必须：`submit_verdict` 判定 + Failed-count 资格门（REGULAR: `Failed RA == 0`）+
   **用户显式确认**；自动化链里禁止放提交节点（`workflow_submit_alpha` / `workflow_superalpha`）。
5. GEM 强制：步 4 必须 `mcp__wq-brain-http__workflow_gem`，禁止只跑 build-wave 或手写表达式。
6. 白名单外禁止 generate / simulate；白名单至少 2 个非 MODEL 数据集（pyramid_quota）。
7. 禁止 `add(A,B)` 混信号、禁止"每字段套 rank"、禁止加权混合组合腿（`0.5*rank(A)+0.5*rank(B)`）。

【执行顺序（严格按序；任一步 FAIL 就地按该步失败分支回退，不得跳步）】

步0 前置（缺一不可，先于一切新挖）
  a. 读 `references/regions/USA.md`（entry_verdict=active 放行）+ `tracking/USA/config/settings.json`
     （记录 current_wave / next_wave / excluded_families / orthogonal_directions / win_recipe）。
  b. 【库存优先】`python tools/build_gate_prior_from_inventory.py --regions USA --emit-candidates cache/candidates.json --write-priors`
     然后 `python tools/select_ra_basket.py cache/candidates.json --target 10 --out cache/basket.json`。
     ★ 实证：清库存的产出率是开新挖的数量级倍数（2026-09-07 跨四区 170 次新回测 0 条，库存扫描一次 20 条）。
     篮子敲定以 `GET /alphas/{id}` 的 detail 端点 `is.checks` 无 `result==FAIL` 为准。
     只有当候选池不足以覆盖目标时，才进入步 1 开新挖。
  c. `mcp__wq-brain-http__get_messages`（limit=30）扫 `type=="ANNOUNCEMENT"` 标题含 "Power Pool" 的公告，
     解析当期主题的 region/delay/universe/中性化/禁止数据集。当前主题不匹配 USA/delay/universe 则只挖 RA。
     （USA 本期不做 PPA 主攻，RA 提交不受主题限制。）

步1 S-PRE 查表（`wq-brain-campaign-matrix` 查表 + 以下 DB 查询）
  mcp__wqb-db__get_campaign_summary    region="USA"
  mcp__wqb-db__get_dead_ends           region="USA"
  mcp__wqb-db__get_dead_datasets       region="USA"
  mcp__wqb-db__get_mining_yield                                      # 全区排名
  mcp__wqb-db__get_mining_yield        region="USA" by_dataset=true  # 本区按数据集拆
  mcp__wqb-db__get_latest_wave         region="USA"
  mcp__wqb-db__get_ledger_key          region="USA" key="region_kb"
  读法（2026-09-19 严格口径，默认 strict=true）：
    conversion  = 已回测/已生成 —— 低 = 管道问题（S2→S3 断链），修管道别换区。
    yield_rate  = 达标/已回测 —— 低 = 标的 问题（该区/集不出货），换区/换集别加量。
  USA 2026-09-06 基线：yield_rate 1.4%、conversion 7.1%（积压堆库典型）。
  产出 universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号（= settings.json 的 next_wave）。
  失败分支：registry 全空 → 补 campaign；dead_datasets 已覆盖全部候选 → 停，转 `brain-next-move-analysis`。

步2 S0 数据集体检 + 金字塔配置
  【三方交叉选集】`python tools/campaign_intel.py s0-select --region USA --delay 1 --universe TOP3000 --top-n 15 --target 10`
    （recommend_datasets 平台真实点塔 × get_mining_yield 本区产出率 × get_dead_datasets 台账判死）；
    看 `hist_yield_rate` / `hist_backtested` / `maxS` / `fld` / `est_seats`；`lit=Y` 候选直接剔除。
    输出 Σest_seats < 10 即 [WARN] 结构性不可达 → 扩集/换区。
  【硬约束（硬规则，2026-09-19 用户定案）】已点亮塔不进白名单：平台 `get_pyramid_alphas` 当季 ACTIVE ≥3 的
    category（`recommend_datasets.category_lit=true`）不得作为战役主数据集；其字段只能作辅助腿。
  【2 步必需 + 1 步可选，不是三次重复】
    ① `mcp__wq-brain-http__workflow_campaign  region="USA" stage="S0" calibrate=true`
    ② `mcp__wq-brain-http__workflow_campaign  region="USA" stage="S0"`   ← ①不产排名，②是必需步
    ①′ `calibrate=true dry_run=true` 仅新区/结果可疑才审（甜区 ac 异常 / strong_acs 空）。
  【锁白名单】`mcp__wqb-db__upsert_ledger_key(region="USA", key="s0_whitelist", value=<list>)`；
    回读 `mcp__wqb-db__get_ledger_key region="USA" key="s0_ranking"` 复核。
    硬约束：≥2 非 MODEL；category_weight ∈ 0.9–1.15（USA thresholds 已配，勿覆盖）；`*_dead` 仍排除；
    白名单外禁止 generate/simulate；数据集 alphaCount ≥1 万或连续 2 波模板全灭 → 强制切 hypothesis-first。
  【开区硬前置（P1-1）】锁白名单后、步 4 generate 之前，为白名单数据集补齐体检包
    `tracking/mining/field_inspect_usa_<dataset>.json`（当前已有 104 个 USA 包）。缺包时步 5 体检硬门不生效。
    缺包用 `python tools/gen_field_inspect_packs.py --region USA --delay 1` 生成（纯离线）。
  【信号天花板闸自动拦截】`workflow_campaign(stage="S2"/"S3")` 前置自动判定，
    唯一权威位置 = `tracking/USA/config/thresholds.json` 的 `diversity.signal_floor`
    （USA 已配 max_sharpe_floor=0.9 / min_batches=2，2026-09-11 实证回填）。
    被拦即换 universe / 换数据集 / 换区域，不要绕过。
  失败分支：配额后仍无非 MODEL → 写 findings 不退纯 MODEL；全部硬排除 → 回步 1 换 region。步3 S1 字段扫描 + 理解
  【必做 typed catalog】白名单每个数据集跑 `mcp__wq-brain-http__workflow_campaign region="USA" stage="S1" dataset=<DS>`
    → ledger `s1_<DS>_d1`；字段目录 `mcp__wqb-db__upsert_field_catalog(region="USA", catalog=<catalog>)`。
    typed catalog 缺失时步 5 闸 2/3 直接 FAIL（GBR analyst_consensus 先例）。
  【深度字段理解按需】`mcp__wq-brain-http__workflow_feature_engineering  region="USA" dataset_id=<DS> delay=1 universe="TOP3000"`
    ★ 2026-09-17 P3-11 收口：**按需 / 仅人读参考 / 禁止注入 GEM**（它产的是确定性模板渲染，
    注入会让 GEM 一行 LLM 都不调、整波退化为"每字段套 rank"）。
  【prod-corr 规避】`mcp__wq-brain-http__get_datafields` 后按 `users` 分级：
    users ≥ 50 → 只做信号方向验证，不投入候选打磨（prod_corr 必超）；
    users 10–49 → 进候选池、提交前必须实测 prod_corr；
    users 0–9 → 优先候选池（理论 prod_corr≈0）。
    冷门字段（users≤9）占批次预算 ≥50%。详见 `references/prod-corr-avoidance.md`。
  失败分支：字段数 <10 退回步 2 白名单外；VECTOR 比例用 `get_datafields` 确认，步 4 传对 `data_type`。

步4 S2 选波：概念优先生成
  【priors 组装】`mcp__wq-brain-http__workflow_campaign region="USA" stage="S2" subcommand="assemble-priors"`
    （GEM 管道消费 `wins`(≤6) 与 `dead_ends`(≤12)；勿手写组装）。
  【GEM 强制】`mcp__wq-brain-http__workflow_gem  region="USA" dataset_id=<DS> delay=1 universe="TOP3000" data_type=<DTYPE> pipeline_mode="phased"`
    （priors 已可由 GEM 从 DB 快照 `priors_snapshot_USA` 直读，文件仅降级兜底）。
  【USA 注入：priors 硬排除饱和族】GEM `--priors-file` / priors 快照必须包含
    `signal_families_exclude`（见 §2）；生成结果若仍命中饱和族，build-wave 阶段直接剔除，不进七槽。
  【生成侧预闸（自动）】quantile 归一化、hump/bucket 命名参数、区域非法 group 字段、
    非标窗口归一（20/21→22、60/63/65→66、250/255→252、500→504、1000→1008、1250→1260）、
    同骨架换字段变体封顶（`WQB_GEM_MAX_PER_SKELETON` 缺省 12/骨架）已由 pipeline_pregate 处理。
  【选波实验清单（2026-09-24）】8 条不是固定上限。普通探索 `--size N` 仅为容量；
    预定实验须先写 DB ledger，`extra_args=["--selection-contract-key","selection_w<W>","--size","<容量>",
    "--enhance-diversity","never","--auto-coverage","never"]`，条数由清单推导，容量不足显式扩容或分波。
  【硬约束】先读 win 层（region_kb.win_recipes）；有胜绩则本波 ≥2 槽按机制换腿。
    七槽配给：≥2 跨金字塔、≥1 win 换腿、弱探针 ≤1 槽（已有近闸字段时为 0）。
    概念优先：机制 → 1–2 个具体字段 id → 一个 Implementation Example。
    有信号：`|Sharpe|≥1.0` / `PASS_CHEAP` / registry 标明有 IS 但卡 prod；复合后 `|S|<0.5` 不再入选波池。
    时间窗口只用 1/5/22/66/252/504/1008/1260。
    落库核验：`mcp__wqb-db__list_expressions` 确认 selected 状态与无 alpha_id。
  【USA 注入：不碰经典价值/质量/动量】book/PE/ROE 等经典基本面单因子及其线性变体禁止生成（必死）。
  失败分支：GEM 未入库 → 查 `workflow_task_status` 按超时恢复清单，确认失败才回退；候选不足 → enhance / 扩组合。

步5 S2→S3 门禁（MCP 优先，dry-run 先行）
  【幽灵算子硬闸（零配额）】`python tools/campaign_intel.py ghost-audit --region USA --exprs-file <候选表达式.txt>`
    退出码 1 = 有幽灵算子（sigmoid/ts_entropy/ts_skewness/ts_percentage/ts_decay_exp_window 等）→ 隔离到独立小批或换已验证等价算子。
  【一键门禁】`mcp__wq-brain-http__workflow_execute node="wave_gate" params={"region":"USA","dataset":<DS>,"wave":<W>}`
    等价 CLI：`python tools/wave_gate.py --campaign-dir tracking/USA --dataset <DS> --wave <W> --from-db`
    `--inspect-mode` 建议 `enforce`（新数据集/新区域 fail-closed 缺包即拦截）。
    候选不在库：`--exprs-file <候选表达式.txt>`；单条自查：`--expr <表达式>`。
    VECTOR：`mcp__wq-brain-http__preflight_expressions auto_fix_vector=true`。
  【双硬门已接线】闸6 多样性（toolkit `gate.py:check_batch_diversity`，唯一执行口径）由 wave_gate 自动调用；
    体检硬门（`tools/field_inspect_gate.py`）5 条：低覆盖(cr<0.4)→ts_backfill、高偏度(|skew|>2)→rank/winsorize/signed_power、
    厚尾(kurt>8)→rank/winsorize、单边恒正负→不能直接原水平、稀疏事件→trade_when。
  【产物】`gate_results`（`all_pass` / `fail_reasons`），由 wave_gate 落库。
  失败分支：语法 FAIL 必先修；多样性 FAIL 回步 4 补骨架（查 `KB/community_tpl_kb`，先查 `ghost_operator_advisory`）；
    2 跨集 FAIL 拆回单集组合不停挖。

步5b 新信号族的 prod-first 探针（硬门，2026-09-19 升格）
  任何新信号族在投入第二波之前，必须先用 1–2 条骨架查 `check_correlation(production)`：
  `python tools/campaign_intel.py prod-first --region USA --wave <W> --top-k 2 --write-ledger --json <out.json>`
  判定：家族首探 prod ≥ 0.7 → 记 dead_end 换机制，不做任何去相关变体；
        0.60–0.70 → 直接进步 8（USA prod_corr_early_warn=0.6，见 §2）。
  实证（IND pv103）：连投 3 波 24 条后才查 prod = 0.79–0.92，整族报废。

步6 S3 七槽回测
  【唯一并发来源】`wqb-concurrency` §8（Token-Bucket C≈7，`WQB_GLOBAL_SLOTS` 缺省 7）。
  【填槽】`mcp__wq-brain-http__workflow_batch_track region="USA" wave=<W> dataset=<DS>`
    ★ 禁止拼 `--concurrency`（pipeline.py 无此参数；曾致 S3 "启动成功"却从未真跑 13 天）。
    n_slots 内部 = min(7, 批数)。空槽补组合批，不用裸探针凑数。
  【跟踪】`mcp__wq-brain-http__workflow_task_status task_id=<上一步返回的 task_id>`
    收批压缩：`mcp__wq-brain-http__harvest_multisim_alphas multisimulation_location="/simulations/<id>"` →
      `mcp__wqb-db__harvest_multisim_results region="USA" wave=<W> alphas=<上一步返回>`
  【设置层先验（默认开）】pipeline.py 读 `region_kb.gate_priors`，样本≥30 且过闸率≥当前×2 自动改写；
    `--set decay=…` / `--no-settings-prior` 可关闭。
  【prod-first】每槽先 1–2 条骨架查 `prod_corr`；USA 预警线 **0.6**（≥0.6 即停扩换腿，不再等 0.7）。
  【连坐隔离（默认开）】ERROR 批解析坏式回写 `expressions.status='fail'`，无辜式作为"重发批"优先重发一次。
  【批次故障协议】8 子模拟全 ERROR → 重发相同表达式（USA/D0 3 次确认）；CROWDING 连续 2 次 → 跳过该中性化；
    transient "try again" → 拆 5 条/批；429 → 指数退避、批大小 ≤5。
  【积压清理】`SELECT region,status,COUNT(*) FROM expressions WHERE region='USA' GROUP BY status`：
    pending+gated > 本波表达式数 ×2 → S2→S3 断链，本波结束优先把近闸积压纳入下一波，禁止无脑堆库。
  失败分支：整批 CANCELLED 回步 5；429 降并发。

步7 S4 诊断改进
  【S4 预筛压缩】`python tools/campaign_intel.py s4-prescreen --ids-file <本波 alpha_id 清单.txt>`
    分层 READY / REVIEW / REJECT；REJECT 直接判死不进链。
  【完整评审链】仅 READY/REVIEW 走
    `selfcorrQuick → check_self_correlation → compute_mutual_correlation → check_correlation → robustness → judge(参考)`。
    `mcp__wq-brain-http__workflow_campaign region="USA" stage="S4" dataset=<DS> wave=<W>`（评审表写入 ledger `s4_walls_USA_<wave>`）。
  【USA 注入：Mode B 强制正交】`wq-brain-alpha-optimization-v1` Mode B 必须启用正交方向推荐
    （联动 P2-1）：同族变体 >3 次仍 prod_corr ≥0.6 → 判该族死刑，写 dead_end，换正交概念，禁止同族磨参数。
  【prod 饱和反馈】prod-first 族级 STOP（≥0.7）的族不再扩变体，结果写 `alphas.prod_correlation` + ledger `prod_first_<wave>`。
  【near 池】sharpe 过 near 线但 `robust_universe_sharpe/limit < near.robust_min_ratio`（缺省 0.5）→ `ROBUST_STRUCTURAL` 墙、不入 near。
  【风险中性化硬规则】`risk_neutralized_sharpe <= 0` 且 `sharpe >= 1.58` ⇒ 记 dead_end，禁止继续调参。
  【组合腿救援】从 `mcp__wqb-db__get_salvage_pool region="USA" boost_dim=<boost_2y|boost_cw|boost_tvr|boost_sharpe> exclude_dataset=<主信号数据集> min_sharpe=1.0`
    取辅助腿；**禁止加权混合**，仅允许结构交互（ts_corr / ratio / 价差 / 条件 / 分组）。
  失败分支：prod_corr ≥0.7 → Mode B 换概念；同一想法 >10 种结构仍不过 → 步 9 记 dead_end，回步 2。步8 S4→S5 稳健闸与提交判定（顺序执行；最终判定唯一权威 = submit_verdict）
  【必经】`brain-alpha-robustness`（反过拟合/稳健性闸）。
  【Failed-count 资格门（研究侧硬前置）】从 `is.checks` 计算 WebDataScope failed counts，
    REGULAR 要求 `Failed RA == 0`（比 `result=="FAIL"` 严格，WARNING/ERROR 也计数）。
    非零 → 回步 7 修复，不进入提交。
  【提交层权威】`mcp__wq-brain-http__submit_verdict alpha_id=<ALPHA_ID>`
    给出模拟层 checks + GET `/alphas/{id}/submit` 双视图（403 盲区唯一权威）。
  【prod 0.60–0.70 当天提交，不先做变体（2026-09-19 血的教训）】
    规则：`submit_verdict` READY 且 prod < 0.7 → **立即请用户确认提交**；
    同族第二颗的变体探索放在第一颗 ACTIVE 之后。
    实证（IND pv103 mLm2xG1K）：S 3.83 IS 全过 prod 0.6997，先花 1 小时做变体期间外部用户提交同款，复查 prod = 1.0000，整族封死。
  【用户确认】SUBMITTABLE 只报告、等用户确认。确认前禁止
    `mcp__wq-brain-http__workflow_submit_alpha` / `mcp__wq-brain-http__submit_batch`。
    `pipeline --submit` = 提交回测，不是提交 alpha。
  【配额】REGULAR_SUBMISSION 4/日 + SUPER 1/日 + PPA `POWER_POOL_SUBMISSION` 1/日（均 00:00 ET 重置）。
    配额耗尽按 ET 日历日等待，不越权。
  失败分支：PASS_CHEAP 可提交；PROD/SELF 不过回步 7。

步9 S6 复盘回写（未回写 = 本波未完成）
  【开步先看漏斗】`python tools/step_funnel.py --region USA [--wave <W>] [--json]`
    用数据定位"这一波在哪一跳掉得最狠"，不凭印象写 verdict。
  【自动回写】`pipeline.py --review` 自动刷新 `region_kb`（recent_waves / gate_priors_local / updated_at）。
  【手动回写（必做）】
    mcp__wqb-db__upsert_wave_result        region="USA" wave=<W> verdict=<PASS|FAIL|PARTIAL> ...
    mcp__wqb-db__upsert_registry_empirical region="USA" ...
    mcp__wqb-db__upsert_ledger_key         region="USA" key="s6_verdict_<wave>" ...
    ★ verdict 只接受 PASS / FAIL / PARTIAL；描述性结论写 `key_findings`。
  【逐数据集经验沉淀（必做）】`mcp__wq-brain-http__workflow_campaign region="USA" stage="S6" subcommand="dataset-experience" dataset=<DS> extra_args=["--delay","1"]`
    未回测、诊断与待出相关性不能记成已验证成果。
  【判死封存】dead_end 回写前调 `mcp__wqb-db__seal_dead_end region="USA" entry_id=<DEAD_END_ID> family=<族名> reason=<带数据的判死原因> rule=<下次怎么办> wave_numbers=[W1,W2,...]`
  【点塔进度】`python tools/campaign_intel.py pyramid --region USA --delay 1`
    输出末尾 [key_findings] 单行直接拷进 upsert_wave_result 的 key_findings。
  【提交多样性监控】每提交 3–5 颗调 `mcp__wq-brain-http__value_factor_trendScore start_date=<本季初> end_date=<今天>`
  【prod 饱和反馈 S0】本波候选全部被 `prod_corr >= 0.7` 卡死 → 除 add-dead-end 外须在 ledger `submit_ready_blocked` 追加该数据集/信号族饱和记录。
  【OS ACTIVE / 全闸 PASS 必须 add-win】mix 比例、中性化、decay、快/慢腿。

【整链（可选）】`mcp__wq-brain-http__workflow_chain dry_run=true chain=[…]`
  先干跑逐节点构建真实命令并做 argv 契约校验（`failed_at` 指出首断点），再实跑；
  `join_async=true`（默认）等上游后台任务到终态；单步等待上限 `join_timeout_sec`（默认 1800s）。
  ★ 提交类节点不入链：`submit_alpha` / `superalpha` 的 `confirm_submit=True` 必须在步 8 用户明确确认后单独调用。

【循环与停止（命中即停，报告结论）】
  A. 停止闸（`workflow_campaign(stage="S2"/"S3")` 前置，零配额，干跑也走）：
     规则 A：该区 `backtest_results` ≥100 条且达标 0 条 → 停区。
     规则 B1 同轴熔断：开波 dataset 轴最近 K=3 个 closed 波连续可计数 FAIL → 拒开（换数据集/换轴清零）。
     规则 B2 区级多轴停：最近 8 波窗口内无任何 PASS 且 ≥4 个不同轴全部 FAIL → 停区。
     豁免：零配额 FAIL、产出新 dead_end 的 FAIL 不计数；撞墙型 FAIL 计数但附路由提示。
     （阈值 `diversity.stop_rules`；schema 不齐或 axis_scope:false 回落旧口径。）
     用户显式要求继续时写 `mcp__wqb-db__upsert_ledger_key(region="USA", "stop_rules_override", {...})` 放行。
  B. 信号天花板闸：连续 min_batches 个波次 max|sharpe| < floor → 拒开（USA floor=0.9/min_batches=2）。
     缺节 fail-closed；仅 `enabled:false` 放行。
  C. 连续 3 波 gate 通过率=0（`gate_results.all_pass` 全 0）→ 该信号族/数据集判死，换数据集。
  D. 白名单被 dead_end 全覆盖 → 停止。
  E. 配额耗尽 → 挂起提交，继续步 2→9。

【验收清单（提交给用户前的自检，逐项打勾）】
  □ 步0 库存扫描已先做（build_gate_prior_from_inventory + select_ra_basket）
  □ 白名单内生成（白名单外 = 违规）；已点亮塔未作为主数据集
  □ 每批过步5 门禁（`gate_results.all_pass` 有落库记录）
  □ 七槽配给 ≥2 跨金字塔、≥1 win 换腿、弱探针 ≤1
  □ PROD/SELF 实测：每槽先 1–2 条骨架查 prod，未摊满 8 条
  □ 新信号族已过 prod-first 探针（prod-first 硬门）
  □ 提交前 `Failed RA == 0` + `submit_verdict` 200 + 用户确认
  □ 回写三处齐：`wave_results` + `registry_empirical` + `s6_verdict_<wave>`
  □ USA profile 注入全部生效：排除饱和族、prod 预警 0.6、Mode B 强制正交、delay0 不混批

【禁止（反模式）】
  - 手写 `_gate_waveNN.py` / `w*_batches.json` / 把 `final_expressions.json` 当真相源。
  - 手写 requests；跳步 9；在正文复写阈值；`combination(alpha(...))`。
  - 七槽全裸探针；七槽全 MODEL + 固定 COUNTRY/decay6。
  - 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽。
  - submit_verdict READY 后自动 `workflow_submit_alpha`。
  - 调用已废弃的 `glb_pipeline` / `gbr_pipeline` / `glb_alpha_machine`；`brain-deepExplore`。
  - 先摊满 8 条再查 prod（USA 代价翻倍）；同族变体 >3 次 prod ≥0.6 仍磨参数。
  - delay0 探针与 delay1 混批。
  - 把 `workflow_judge` / `workflow_campaign(stage="S2")` 当提交权威或门禁。
---

## 2. USA profile 注入（与主提示词一并交给 AI）

> 以下是 `references/regions/USA.md` 的 front-matter 与正文要点渲染结果。AI 执行时须**自行重读**
> `references/regions/USA.md`；此处内容已核对一致，若与主提示词冲突，**profile 优先**。

### 2.1 入口裁决
- `entry_verdict: active` → 放行继续步 2（`frozen` 则立即停，USA 不是）。

### 2.2 静态配置（与 `tracking/USA/config/settings.json` 一致）
- `universe`: [TOP3000, TOP1000, TOP500]；`universe_default: TOP3000`
- `delay`: [1, 0]；`delay_default: 1`（**delay0 探针单独成批，不与 delay1 混批**）
- `neutralization_default: SUBINDUSTRY`（`settings.json` 同值；次优轨 SECTOR）
- 固定仿真设置（`settings.json`）：decay=5 / truncation=0.08 / maxTrade=OFF / pasteurization=ON /
  unitHandling=VERIFY / nanHandling=ON / language=FASTEXPR / 起止 2013-01-01→2023-12-31
  （全部由平台 75/86 ACTIVE 队列实证派生，勿改）

### 2.3 数据集红黑榜
- `red`（exhausted，禁止作主攻）：`pv1`、`mdl177`
- `yellow`: []
- `green`（有效方向）：`option9`（进行中）、`analyst 细分集`、`news 高级情绪集`、`event/earnings 集`

### 2.4 priors（硬排除，GEM `--priors-file` / priors 快照必须包含）
- `signal_families_include`: [option, analyst_revision, event_driven, news_advanced]
- `signal_families_exclude`（含 profile + `settings.json::_spre_20260917.excluded_families`）：
  `classic_value`、`classic_quality`、`book_ratio`、`seed_basics`、`option_pcr`、`news_sentiment`、
  `insider_conviction`、`shortinterest_pred`、`pattern_scores`、`pv_tech_indicators`、
  `acquisition_model`、`ai_news_scores`、`earningscall_embed`、`event_sentiment_signals`、
  `insider_feats`、`news_sentiment_dl`、`ml_factor_proj`、`option_chart_model`、
  `multifactor_return_pred`、`sentiment21`、`continuation_score_asc_channel`、
  `option_horizon_decomp_ivskew30d`、`gem_quantile_wrapper`
- 饱和族（步 1 查 `get_dead_ends(USA)` 后并入）：book/value 系单族 145 颗 ACTIVE 同族（2026-08-25 实证），
  `search_alphas_by_sharpe(USA, 1.58)` 命中大量已达标 alpha → 该族硬排除出本波 priors。

### 2.5 已判死的赢家配方 / 正交方向（`settings.json::_spre_20260917`）
- `win_recipe`: 慢变量 + 长窗 `ts_zscore`/`ts_backfill`(90/189/252) + `group_rank`/`group_zscore` 分组；
  情绪域已饱和（prod 0.72–0.82 死）；禁止 IS Sharpe 排序选 prod 候选。
- `orthogonal_directions`:
  1. `earnings_surprise` 长窗（`group_rank`+`signed_power`+`decay90`）
  2. `fund_ownership` 变化（`ts_zscore` 长窗）
  3. `eur_top_value` 慢 value（`ts_zscore` 189 + `group_zscore industry`）
  4. `institutional` 持仓变化（`rank`+`ts_rank` 长窗）

### 2.6 闸门覆盖
- `cw_gate: WARN`
- `longcount_min: 80`
- **`prod_corr_early_warn: 0.6`**（全局默认 0.7；USA 的 0.6→0.7 区间几乎必然继续恶化，≥0.6 即停扩换腿）
- 阈值完整数字引用 `tracking/USA/config/thresholds.json`：
  - `review`: sharpe_min=1.25 / fitness_min=1.0 / two_year_sharpe_min=1.6 / margin_min=0.0005 /
    turnover_min=0.05 / turnover_max=0.3 / ra_failed_count_max=0（D1 门槛取自 how-to-pass-AlphaTest）
  - `hard_gates`: prod_correlation_max=0.7 / self_correlation_max=0.7（异步计算须以重检为准）
  - `diversity.signal_floor`: max_sharpe_floor=0.9 / min_batches=2（实证回填 2026-09-11，13 波 p25=0.93）
  - `mode_b_qualification`: sharpe_min=1.0 / fitness_min=0.6（饱和区降门）

### 2.7 循环策略
- `max_probes_per_wave: 1`（每波最多 1 个弱探针槽）
- `fast_kill`: 新数据集 8 探针无 `|S|≥0.5` 即判死
- `stop_conditions`: ["白名单被 dead_end 全覆盖"]
- 2026-09-06 基线：USA `yield_rate` 1.4%、`conversion` 7.1%（积压堆库典型）→ 步 6 必须做积压检查

### 2.8 USA 四条避坑（`references/regions/USA.md` 正文）
1. 禁止生成 book/PE/ROE 等经典基本面单因子及其线性变体（必死）。
2. 禁止"先摊满 8 条再查 prod"（全局反模式，USA 代价翻倍）。
3. delay0 探针单独成批，不与 delay1 混批，避免设置噪声误判信号族。
4. 步 7 Mode B 必须启用正交方向推荐：同族变体 >3 次仍 prod_corr ≥0.6 → 判该族死刑写 dead_end，
   换正交概念，禁止同族继续磨参数。

### 2.9 实证锚点
- `dead_ends_ref: get_dead_ends(USA)`
- `last_verified: 2026-08-25`
- 当前波号：以 `tracking/USA/config/settings.json` 的 `next_wave` 为准（编制时记 80，执行时重读）；
  USA `expressions` 存量（编制时实测）：backtested=408 / pending=32 / selected=65 / superseded=2600 / dropped=6152。
  ★ 这些数字会随执行变化，**以每次查询为准，不要当作目标承诺**。

---

## 3. 可直接开跑的示例命令序列（供 AI 快速对齐工具名）

```text
# 环境
$WQ_PY = world-quant-brain-mcp/.venv/Scripts/python.exe
$REGION = USA; $DELAY = 1; $UNIVERSE = TOP3000

# 步0 库存优先
python tools/build_gate_prior_from_inventory.py --regions USA --emit-candidates cache/candidates.json --write-priors
python tools/select_ra_basket.py cache/candidates.json --target 10 --out cache/basket.json

# 步1 查表
# (MCP) get_campaign_summary / get_dead_ends / get_dead_datasets / get_mining_yield / get_latest_wave / get_ledger_key

# 步2 体检
python tools/campaign_intel.py s0-select --region USA --delay 1 --universe TOP3000 --top-n 15 --target 10
# (MCP) workflow_campaign stage=S0 calibrate=true ; workflow_campaign stage=S0
# (MCP) upsert_ledger_key s0_whitelist
# 体检包：python tools/gen_field_inspect_packs.py --region USA --delay 1

# 步3 字段
# (MCP) workflow_campaign stage=S1 dataset=<DS> ; upsert_field_catalog

# 步4 生成
# (MCP) workflow_campaign stage=S2 subcommand=assemble-priors
# (MCP) workflow_gem region=USA dataset_id=<DS> delay=1 universe=TOP3000 data_type=<DTYPE> pipeline_mode=phased

# 步5 门禁
python tools/campaign_intel.py ghost-audit --region USA --exprs-file <候选表达式.txt>
# (MCP) workflow_execute node=wave_gate params={"region":"USA","dataset":<DS>,"wave":<W>,"inspect_mode":"enforce"}

# 步5b prod-first 探针
python tools/campaign_intel.py prod-first --region USA --wave <W> --top-k 2 --write-ledger --json cache/prod_first_<W>.json

# 步6 回测
# (MCP) workflow_batch_track region=USA wave=<W> dataset=<DS>
# (MCP) workflow_task_status task_id=<id>
# (MCP) harvest_multisim_alphas ; harvest_multisim_results

# 步7 诊断
python tools/campaign_intel.py s4-prescreen --ids-file <本波 alpha_id 清单.txt>
# (MCP) workflow_campaign stage=S4 dataset=<DS> wave=<W>
# (MCP) get_salvage_pool region=USA boost_dim=... exclude_dataset=<主数据集> min_sharpe=1.0

# 步8 提交判定
# (MCP) submit_verdict alpha_id=<ALPHA_ID>   # 唯一权威
#       → 报用户确认 → 确认后 workflow_submit_alpha confirm_submit=True

# 步9 回写
python tools/step_funnel.py --region USA --wave <W>
# (MCP) upsert_wave_result / upsert_registry_empirical / upsert_ledger_key s6_verdict_<wave>
# (MCP) workflow_campaign stage=S6 subcommand=dataset-experience dataset=<DS> extra_args=["--delay","1"]
# (MCP) seal_dead_end
python tools/campaign_intel.py pyramid --region USA --delay 1
```

---

## 4. 编制校验记录（本文件对账依据）

| 校验点 | 结论 |
|---|---|
| 主编排入口 | `wq-brain-ra-pipeline` v2.2，last_verified 2026-09-24 |
| USA profile | `references/regions/USA.md`，entry_verdict=active，last_verified 2026-08-25 |
| 阈值文件 | `tracking/USA/config/thresholds.json`（review/hard_gates/diversity.signal_floor/mode_b_qualification 已核对） |
| 仿真设置 | `tracking/USA/config/settings.json`（universe/delay/neutralization/decay 已核对） |
| 体检包 | `tracking/mining/field_inspect_usa_*.json` 当前 104 个（执行时按白名单复核） |
| USA 表达式存量 | backtested=408 / pending=32 / selected=65（2026-09-25 编制时实测，仅作参照） |
| 提交判定权威 | `mcp__wq-brain-http__submit_verdict`（唯一）；`workflow_judge` 仅参考层 |
| 提交需用户确认 | `confirm_submit=True` 禁止入自动链 |

> **免责边界**：本提示词是可执行的编排剧本，不是产出承诺。10 颗 submit-ready 是目标；
> 命中 §4 停止规则（信号天花板、同轴熔断、区级多轴停、gate 连续 0 通过、白名单判死全覆盖、配额耗尽）
> 即按规则停下并如实报告，不得绕闸。平台硬闸（prod/self 相关性、robust、2Y、CW、换手、longCount、
> Failed RA=0）的最终判定以平台 `is.checks` 与 `submit_verdict` 为准，本工作区不替代平台权威。