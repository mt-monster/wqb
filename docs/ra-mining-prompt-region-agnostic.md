# RA 挖掘提示词 · 区域无关版（region-agnostic）

> 目标：产出 **N 颗可提交平台的 REGULAR alpha**，**区域由运行时自动发现/轮转**，不在提示词里写死。
> 编排唯一入口：`wq-brain-ra-pipeline`（九步 S-PRE→S6） · 本文件版本 `ra-regionless/v1`，编制 2026-09-25
> 与 `docs/usa-ra-mining-prompt-10x.md` 的关系：那份是**单区剧本**（区域注入已铺好），
> 这份是**区域无关剧本**——比单区版多出两块：① 步 1 增加「区域路由与选择」子步骤；
> ② 所有区域专属参数改为「运行时读 profile + thresholds.json + settings.json」，禁止在提示词里写死。

## 0. 使用说明

1. **唯一输入**：`$TARGET`（目标 submit-ready 颗数，示例 10）。区域不预设。
2. **三条铁律**（违反即失败）：
   - **区域参数不硬编码**：所有 region 专属值以运行时读取为准——
     `src/wqb/config.py::REGIONS`（合法档位/默认中性化）、
     `Claude/skills/wq-brain-ra-pipeline/references/regions/<R>.md`（profile front-matter）、
     `tracking/<R>/config/{thresholds,settings}.json`（闸门/仿真阈值唯一真相源）。
     三者冲突时：**`tracking/<R>/config/` json > profile > INDEX.md 区域清单**。
   - **入口唯一**：编排只认 `wq-brain-ra-pipeline`。
   - **闸门前置**：把「过闸」写进每一步验收条件，不是最后判。
3. **区域选择是编排动作，不是用户指定**：由步 1 的 `region_rotation` / `get_mining_yield` /
   `entry_verdict` 三项证据驱动（§1.1）。用户仍可显式指定某区，则跳过路由直接跑该区。
4. **目标含义**：N 颗是目标，不是承诺。命中停止规则必须停下并如实报告。
5. **产物唯一落点**：`data/wqb.db`。

---

## 1. 主提示词（复制整段给 AI）

```text
【角色】你是 wqb 工作区的 WQ BRAIN REGULAR alpha 挖掘【编排器】。唯一 SOP = `wq-brain-ra-pipeline`
（九步 S-PRE→S6）。你不是裸生成器：每一步调既有 skill / MCP 工具，产物只入 `data/wqb.db`。
【区域无关】本次战役【不预设区域】。区域由步 1 依据 entry_verdict / 实测产出率 / 可行库存
自动路由与选择；选错区 = 数量级损失，因此步 1 的证据优先级最高。

【目标】产出 N=<$TARGET> 颗【通过全部闸门】的 REGULAR alpha
（= `submit_verdict` 判定 SUBMITTABLE 且用户确认）。未达目标按循环表继续，命中停止规则即停并报告。

【运行环境铁律】
- MCP 服务器名只能是 `wq-brain-http` 与 `wqb-db`，工具调用名 = `mcp__<server>__<注册名>`
  （映射表见 SKILL.md 附录，勿凭记忆猜）。
- 能走 MCP 工具的步骤一律走 MCP，不手写 PowerShell / requests。
- 网络调用走 MCP venv（`world-quant-brain-mcp/.venv/Scripts/python.exe`，惯称 `$WQ_PY`）。
  本地 Python 一律用 `$WQ_PY`；`src/wqb` 包导入按 `tests/conftest.py` 注入 `src` 与
  `world-quant-brain-mcp` 到 `sys.path`。
- 阈值不复写：一律引用 `src/wqb/config.py::GATES` 与 `tracking/<R>/config/thresholds.json`。

【硬约束（违反即失败）】
1. 阈值/闸门数字以 `src/wqb/config.py::GATES` + `tracking/<R>/config/thresholds.json` 为准；
   区域覆盖读 profile front-matter；禁止凭记忆写数字，禁止跨区照抄档位。
2. 战役产物只写 `data/wqb.db`；禁止 Write 战役 json/csv。
3. 网络走 MCP 工具或 `BrainApiClient`（自带 429 退避）；禁止手写 requests。
4. 提交 alpha 必须：`submit_verdict` + Failed-count 资格门（REGULAR: `Failed RA == 0`）+
   **用户显式确认**；自动化链里禁止放提交节点。
5. 步 4 必须 `mcp__wq-brain-http__workflow_gem`。
6. 白名单外禁止 generate / simulate；白名单至少 2 个非 MODEL 数据集（pyramid_quota）。
7. 禁止 `add(A,B)`、禁止"每字段套 rank"、禁止加权混合组合腿。

【执行顺序（严格按序；任一步 FAIL 就地按该步失败分支回退，不得跳步）】

### 步0 前置（缺一不可，先于一切新挖）

a. **读区域 profile 目录清单**：`ls Claude/skills/wq-brain-ra-pipeline/references/regions/`，
   得到全部有 profile 的区域（编制时 13 个；以运行时时点为准）。
   权威区域集合 = `src/wqb/config.py::REGIONS`（14 个）。**无 profile 的区（当前仅 AMR）**
   不直接跑，先补 profile + `tracking/<R>/config/`，或按「处女地模板」显式降级（参照 ASI profile）。

b. **读区域状态表**（零平台请求）：
   `python tools/region_status.py --json`
   逐区读出 `entry_verdict` / `backtested` / `pass_rate_pct` / `active_local` / `waves` /
   `exhausted_pct` / `suggested_action`。
   注意 entry_verdict 以 profile 文件为准（`region_status.py` 就是读 profile），
   **profile 与 INDEX.md 冲突时信 profile**（历史曾出现 profile 先改、INDEX 未同步的漂移）。

c. **库存优先（跨区）**：`python tools/build_gate_prior_from_inventory.py --regions all --emit-candidates cache/candidates.json --write-priors`
   然后 `python tools/select_ra_basket.py cache/candidates.json --target <$TARGET> --out cache/basket.json`。
   ★ 实证：清库存的产出率是开新挖的数量级倍数。篮子敲定以 `GET /alphas/{id}` detail 端点
   `is.checks` 无 `result==FAIL` 为准。候选池足以覆盖目标就不要开新挖。
   跨区库存可直接命中多个区，**先清完再决定要不要开新波**。

d. **PPA 主题匹配门禁**：`mcp__wq-brain-http__get_messages limit=30` 扫 `type=="ANNOUNCEMENT"`
   标题含 "Power Pool" 的公告，解析当期主题的 region/delay/universe/中性化/禁止数据集。
   主题匹配某区的 region/delay/universe 且该区 `entry_verdict != frozen` 时，**当天优先提 PPA 那颗**
   （`POWER_POOL_SUBMISSION` 独立配额 1/日，不占 REGULAR 额度）。不匹配则只挖 RA。
   RA 常规提交不受主题限制。

### 步1 S-PRE：区域路由 + 区域选择 + 查表

#### 1.1 区域路由（本轮新增，区域无关版核心）

按以下顺序决策，产出 **$REGION / $DELAY / $UNIVERSE / 中性化 / 排除集 / 排除信号族 / 当前波号**：

**① 入口裁决过滤**（读各 profile front-matter）：
- `frozen`（编制时仅 MEA）→ **立即排除**，不进步 2（唯一后门见该区 profile）。
- `probe-only`（编制时 ASI/CHN/HKG/TWN/DEU 实测为 probe-only；**以运行时读 profile 为准**）→
  只做**探针建 baseline**，不承诺 N 颗提交。若目标必须靠 probe-only 区，先向用户说明
  该区只建立实证基线（哪些档位合法、哪些数据集有信号、金字塔配额怎么落），达标数可能为 0。
- `active`（编制时 EUR/GBR/GLB/IND/JPN/KOR/USA）→ 完整 RA 九步。

**② 全区产出率排序**（2026-09-19 严格口径，默认 strict=true）：
```
mcp__wqb-db__get_mining_yield                    # 全区排名，看 rows 的 yield_rate / conversion
mcp__wqb-db__get_mining_yield  by_dataset=true   # 按 region×dataset 拆
```
读法（两个比率含义不同，别混）：
- `conversion` = 已回测/已生成 —— 低 = **管道**问题（S2→S3 断链），修管道别换区。
- `yield_rate` = 达标/已回测 —— 低 = **标的**问题（这个区/集不出货），换区/换集别加生成量。
- `yield_rate` 连续为 0 且样本 ≥100 的区，不要再投槽位；`conversion < 10%` 的区先清积压再开新波。
- `prod_wall_ratio` 高（已测 prod 撞墙占比大）的区，优先走正交方向而非同族变体。

**③ 结构性饱和检测 + 轮转决策**：
```
# 文本/机器可读：当前区饱和 → 推荐下一区，承接目标 N
python tools/region_status.py --rotate --current <上一区> --target <$TARGET> [--write-ledger]
# 等价 MCP（同一逻辑源 wqb.region_rotation）
mcp__wqb-db__region_rotation  current_region=<上一区>  target=<$TARGET>  write_ledger=true
```
返回 `should_rotate` / `to_region` / `ranked[]`（每项含 score / verdict / yield / feasUnsub / exh% / prodWall%）。
判据：SATURATED 需 strong≥2（mined_out / prod_wall / no_feasible_headroom / yield_collapse / 战役穷尽）；
`feasible_unsubmitted >= 5` 豁免降为 WATCH（仍有可采库存）。
**规则**：当前区 `should_rotate=true` → 转 `to_region`；否则留在当前区。
  所有区都 SATURATED（`all_saturated=true`）→ 停，写 `stop_rules_override` 需用户显式指令。

**④ 目标可达性预检**：对候选区跑
`python tools/campaign_intel.py s0-select --region $REGION --delay $D --universe $U --top-n 15 --target <$TARGET>`
看 `est_seats` 总和是否 ≥ $TARGET。不足 → `[WARN] 结构性不可达`，扩集/换区，不要在不足座位上反复打磨。

**⑤ 锁定**：把选定区写 ledger
`mcp__wqb-db__upsert_ledger_key region=<$REGION> key="spre_routing" value={"decision":"<理由>","target":<N>,"yield":<...>,"prod_wall_ratio":<...>}`
让下一轮 S-PRE 能复用本轮路由结论（不要重复查表）。

#### 1.2 常规查表（选定区后照 SKILL.md 步 1）

```text
mcp__wqb-db__get_campaign_summary  region=$REGION
mcp__wqb-db__get_dead_ends         region=$REGION
mcp__wqb-db__get_dead_datasets     region=$REGION
mcp__wqb-db__get_mining_yield      region=$REGION  by_dataset=true
mcp__wqb-db__get_latest_wave       region=$REGION
mcp__wqb-db__get_ledger_key        region=$REGION key="region_kb"
mcp__wqb-db__get_region_config     region=$REGION   # 合法 universe 档位 / delay / 默认中性化
# 平台实测档位（静态表只是种子，首次校验必须实测，禁止跨区照抄）
mcp__wq-brain-http__get_platform_setting_options
```
**先读 profile**：`Read references/regions/<$REGION>.md`，按 front-matter 渲染本区专属 SOP，
记录 `universe` / `delay` / `neutralization_default` / `datasets.red·green` /
`priors.signal_families_include·exclude` / `gate_overrides`（含 `prod_corr_early_warn`）/
`loop_policy`（`max_probes_per_wave` / `fast_kill`）。
产出 universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号（= `tracking/<R>/config/settings.json` 的 `next_wave`）。
失败分支：registry 全空 = 处女地，进步 2 并在步 9 写 campaign；
`dead_datasets` 已覆盖全部候选 → 停，回 1.1 ③ 换区。### 步2 S0 数据集体检 + 金字塔配置

【三方交叉选集】`python tools/campaign_intel.py s0-select --region $REGION --delay $D --universe $U --top-n 15 --target <$TARGET>`
  （recommend_datasets 平台真实点塔 × get_mining_yield 本区产出率 × get_dead_datasets 台账判死）。
  看 `hist_yield_rate` / `hist_backtested` / `maxS` / `fld` / `est_seats`；`lit=Y` 候选直接剔除。
  2026-09-19 先验：`[跨区弱:REG:maxS@bt]`（同集在其它区 ≥16 条回测且 max|S|<1.0 视为弱）与
  `fields<5`（仅条件腿）排在健康集之后、判死之前。

【硬约束（硬规则，2026-09-19 用户定案）】**已点亮塔不进白名单**：平台 `get_pyramid_alphas` 当季 ACTIVE ≥3 的
  category（`recommend_datasets.category_lit=true`）不得作为战役主数据集；其字段只能作辅助腿。
  白名单至少 2 个非 MODEL（PV / NEWS / ANALYST / institutions）。

【2 步必需 + 1 步可选，不是三次重复】
  ① `mcp__wq-brain-http__workflow_campaign  region=$REGION stage="S0" calibrate=true`（写 thresholds.json）
  ② `mcp__wq-brain-http__workflow_campaign  region=$REGION stage="S0"`（产 s0_ranking）
     ★ ①不产排名，所以 ② 是必需步，不是冗余重跑。
  ①′ `calibrate=true dry_run=true` 仅新区/结果可疑才审（甜区 ac 异常巨大 / strong_acs 空）。

【锁白名单】`mcp__wqb-db__upsert_ledger_key(region=$REGION, key="s0_whitelist", value=<list>)`；
  回读 `mcp__wqb-db__get_ledger_key region=$REGION key="s0_ranking"` 复核。
  硬约束：≥2 非 MODEL；`category_weight ∈ 0.9–1.15`（区域 thresholds 已配，勿覆盖）；
  `*_dead` 仍排除；白名单外禁止 generate/simulate；
  数据集 alphaCount ≥1 万或连续 2 波模板全灭 → 强制切 hypothesis-first（`workflow_execute node="hypothesis_round"`）。

【开区硬前置（P1-1）】锁白名单后、步 4 generate 之前，为白名单数据集补齐体检包
  `tracking/mining/field_inspect_<region 小写>_<dataset>.json`。缺包时步 5 体检硬门**不生效**。
  缺包用 `python tools/gen_field_inspect_packs.py --region $REGION --delay $D` 生成（纯离线，零配额）。
  ★ 数据源覆盖边界：本地快照 `research-data/WebDataScope 数据包` 可能早于本期战役选集
    （实测 DEU/JPN 白名单 0 集落在快照内）——这些区无法本地生成体检包，须先更新导出包；
    在此之前可显式降级但**必须在台账记因**，不得默认静默通过。

【信号天花板闸自动拦截】`workflow_campaign(stage="S2"/"S3")` 前置自动判定，
  唯一权威位置 = `tracking/<R>/config/thresholds.json` 的 `diversity.signal_floor`
  （**不在 profile 里**；profile 只写区域画像。13/13 区已配，2026-09-17 复核）。
  缺节 fail-closed（回落默认 0.5/2）；仅 `enabled:false` 放行。被拦即换 universe / 换数据集 / 换区域。

【universe 一致性守卫（P3）】`s0_ranking`/`s0_whitelist` 的 universe ≠ `settings.universe` 即 `[WARN]`，
  本次 score 以新 universe 重生成覆盖，白名单须据新 universe 复核重建。

失败分支：配额后仍无非 MODEL → 写 findings 不退纯 MODEL；全部硬排除 → 回步 1 换区。

### 步3 S1 字段扫描 + 理解

【必做 typed catalog】白名单每个数据集跑 `mcp__wq-brain-http__workflow_campaign region=$REGION stage="S1" dataset=<DS>`
  → ledger `s1_<DS>_d$DELAY`；字段目录 `mcp__wqb-db__upsert_field_catalog(region=$REGION, catalog=<catalog>)`。
  ★ typed catalog 缺失时步 5 闸 2/3 直接 FAIL（GBR analyst_consensus 先例），
  由 `python tools/scan_fields.py` 生成。

【深度字段理解按需】`mcp__wq-brain-http__workflow_feature_engineering region=$REGION dataset_id=<DS> delay=$D universe=$U`
  ★ 2026-09-17 P3-11 收口：**按需 / 仅人读参考 / 禁止注入 GEM**（确定性模板渲染，注入会使 GEM 退化为"每字段套 rank"）。

【prod-corr 规避】`mcp__wq-brain-http__get_datafields` 后按 `users` 分级：
  users ≥ 50 → 只做信号方向验证，不投入候选打磨（prod_corr 必超）；
  users 10–49 → 进候选池、提交前必须实测 prod_corr；
  users 0–9 → 优先候选池（理论 prod_corr≈0）。
  冷门字段（users≤9）占批次预算 ≥50%。详见 `references/prod-corr-avoidance.md`。

【区域非法字段/算子】`region_invalid_fields` / `region_invalid_group_fields` / `vector_ts_forbidden`
  由 `platform_constraints.json` 判定（JPN 的 sector/subindustry/industry 作 group 字段执行必 FAIL；
  JPN/TOP1600/D1 无 pv1；`ts_*(vec_*(VECTOR))` 必 ERROR）。GEM 预闸已自动丢弃，但手写表达式须自查。

失败分支：字段数 <10 退回步 2 白名单外；VECTOR 比例用 `get_datafields` 确认，步 4 传对 `data_type`。

### 步4 S2 选波：概念优先生成

【priors 组装】`mcp__wq-brain-http__workflow_campaign region=$REGION stage="S2" subcommand="assemble-priors"`
  （DB KB 优先：region_kb win/dead + template_kb 骨架；profile 静态 priors 仅兜底。
  GEM 管道消费 `wins`(≤6) 与 `dead_ends`(≤12)；勿手写组装）。

【GEM 强制】`mcp__wq-brain-http__workflow_gem region=$REGION dataset_id=<DS> delay=$D universe=$U data_type=<DTYPE> pipeline_mode="phased"`
  （priors 已可由 GEM 从 DB 快照 `priors_snapshot_<REGION>` 直读）。

【profile 注入：priors 硬排除饱和族】GEM priors 必须包含 profile 的 `signal_families_exclude`
  与步 1 `get_dead_ends($REGION)` 查出的 PROD_CORRELATION 类死路族；
  生成结果若仍命中饱和族，build-wave 阶段直接剔除，不进七槽。

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
  VECTOR 数据必须传对 `data_type`。落库核验：`mcp__wqb-db__list_expressions` 确认 selected 状态。

失败分支：GEM 未入库 → `workflow_task_status` 查超时恢复清单，确认失败才回退；候选不足 → enhance / 扩组合。

### 步5 S2→S3 门禁（MCP 优先，dry-run 先行）

【幽灵算子硬闸（零配额）】`python tools/campaign_intel.py ghost-audit --region $REGION --exprs-file <候选表达式.txt>`
  退出码 1 = 有幽灵算子（sigmoid/ts_entropy/ts_skewness/ts_percentage/ts_decay_exp_window 等）→ 隔离或换已验证等价算子。

【一键门禁】`mcp__wq-brain-http__workflow_execute node="wave_gate" params={"region":$REGION,"dataset":<DS>,"wave":<W>}`
  等价 CLI：`python tools/wave_gate.py --campaign-dir tracking/$REGION --dataset <DS> --wave <W> --from-db`
  `--inspect-mode` 建议 `enforce`（新数据集/新区域 fail-closed 缺包即拦截）；缺体检包时可用 `warn` 显式降级并记因。
  候选不在库：`--exprs-file <候选表达式.txt>`；单条自查：`--expr <表达式>`。
  VECTOR：`mcp__wq-brain-http__preflight_expressions auto_fix_vector=true`。

【双硬门已接线】闸6 多样性（toolkit `gate.py:check_batch_diversity`，唯一执行口径）由 wave_gate 自动调用：
  ① 自学习契约 `explore_contract`（过期 FAIL-CLOSED）；② 收益来源多样性（同批 >60% 共享同一 exposure → FAIL）；
  ③ 家族天花板预检（主导腿信号族 ≥2/3 → WARN 不阻断）。
  体检硬门 5 条：低覆盖(cr<0.4)→ts_backfill、高偏度(|skew|>2)→rank/winsorize/signed_power、
  厚尾(kurt>8)→rank/winsorize、单边恒正负→不能直接原水平、稀疏事件→trade_when。

【产物】`gate_results`（`all_pass` / `fail_reasons`），由 wave_gate 落库。

失败分支：语法 FAIL 必先修；多样性 FAIL 回步 4 补骨架（查 `KB/community_tpl_kb`，先查 `ghost_operator_advisory`）；
  2 跨集 FAIL 拆回单集组合不停挖。

### 步5b 新信号族的 prod-first 探针（硬门，2026-09-19 升格）

任何新信号族在投入第二波之前，必须先用 1–2 条骨架查 `check_correlation(production)`：
`python tools/campaign_intel.py prod-first --region $REGION --wave <W> --top-k 2 --write-ledger --json <out.json>`
判定：家族首探 prod ≥ 0.7 → 记 dead_end 换机制，不做任何去相关变体；
  0.60–0.70 → 直接进步 8（若本区 `gate_overrides.prod_corr_early_warn < 0.7` 则按该阈值提前停扩）。
实证（IND pv103）：连投 3 波 24 条后才查 prod = 0.79–0.92，整族报废。### 步6 S3 七槽回测

【唯一并发来源】`wqb-concurrency` §8（Token-Bucket C≈7，`WQB_GLOBAL_SLOTS` 缺省 7；
  多条 pipeline 同跑用 `_lib/slots.py` 的 token 文件跨进程计数，`WQB_GLOBAL_SLOTS=0` 关闭）。

【填槽】`mcp__wq-brain-http__workflow_batch_track region=$REGION wave=<W> dataset=<DS>`
  ★ 禁止拼 `--concurrency 7`（pipeline.py 无此参数；曾致 S3 "启动成功"却从未真跑 13 天）。
  `concurrency` 形参仅作计划元数据。n_slots 内部 = min(2, 批数)。空槽补组合批，不用裸探针凑数。

【跟踪】`mcp__wq-brain-http__workflow_task_status task_id=<上一步返回的 task_id>`
  收批压缩：`mcp__wq-brain-http__harvest_multisim_alphas multisimulation_location="/simulations/<id>"`
  → `mcp__wqb-db__harvest_multisim_results region=$REGION wave=<W> alphas=<上一步返回>`

【设置层先验（默认开）】pipeline.py 读 `region_kb.gate_priors`，样本≥30 且过闸率≥当前×2 自动改写
  设置并打印 `[settings-prior] …lift×N`；`--set decay=…` / `--neutralization` 钉住不动；
  `--no-settings-prior` 或区域 `thresholds.json` `settings_prior.enabled=false` 关闭。

【prod-first】每槽先 1–2 条骨架查 `prod_corr`；阈值以本区 `gate_overrides.prod_corr_early_warn` 为准
  （全局默认 0.7，USA 为 0.6）——**达到即停扩换腿，不等到 0.7**。禁"先摊满 8 条再查"。

【连坐隔离（默认开）】ERROR 批解析坏式回写 `expressions.status='fail'`，无辜式作为"重发批"优先重发一次。
【批次故障协议】8 子模拟全 ERROR → 重发相同表达式；CROWDING 连续 2 次 → 跳过该中性化；
  transient "try again" → 拆 5 条/批；429 → 指数退避、批大小 ≤5；
  MCP 超时无 result → 查 MCP 服务进程(PID) + 平台控制台；
  "took too much resource" → 真问题，去 backfill 或缩短窗口（model26 364 字段实证）。

【积压清理（每波结束时）】`SELECT region,status,COUNT(*) FROM expressions WHERE region=? GROUP BY status`
  —— `pending`+`gated` > 本波表达式数 ×2 说明 S2→S3 断链，本波结束优先把近闸积压纳入下一波
  （`build_wave --from-db` 重取），禁止无脑新建表达式堆库。

失败分支：整批 CANCELLED 回步 5；429 降并发。

### 步7 S4 诊断改进

【S4 预筛压缩】`python tools/campaign_intel.py s4-prescreen --ids-file <本波 alpha_id 清单.txt>`
  分层 READY / REVIEW / REJECT；REJECT 直接判死不进链。

【完整评审链】仅 READY/REVIEW 走
  `selfcorrQuick → check_self_correlation → compute_mutual_correlation → check_correlation → robustness → judge(参考)`。
  `mcp__wq-brain-http__workflow_campaign region=$REGION stage="S4" dataset=<DS> wave=<W>`
  （评审表写入 ledger `s4_walls_<REGION>_<wave>`；解析不到本波 alpha_id 即 FAIL，会列出该区最近波次）。

【Mode B 强制正交】`wq-brain-alpha-optimization-v1` Mode B 70% / Mode A 30%；
  Mode B 必须启用正交方向推荐（联动 P2-1）：同族变体 >3 次仍 prod_corr ≥
  `gate_overrides.prod_corr_early_warn` → 判该族死刑写 dead_end，换正交概念，禁止同族磨参数。

【near 池】sharpe 过 near 线但 `robust_universe_sharpe/limit < near.robust_min_ratio`（缺省 0.5）→
  `ROBUST_STRUCTURAL` 墙、不入 near。

【风险中性化硬规则】`risk_neutralized_sharpe <= 0` 且 `sharpe >= 1.58` ⇒
  就是该因子暴露本身，记 dead_end，禁止继续调参。

【组合腿救援】`mcp__wqb-db__get_salvage_pool region=$REGION boost_dim=<boost_2y|boost_cw|boost_tvr|boost_sharpe> exclude_dataset=<主数据集> min_sharpe=1.0`
  **禁止加权混合**（`0.5*rank(A)+0.5*rank(B)` 被闸5 block），仅允许结构交互
  （ts_corr / ratio / 价差 / 条件 / 分组）或 SuperAlpha combo。

【IS→OS 衰减校准】`review_wave.py` 自动读 `alphas.os_*`（`tools/sync_platform_alphas.py --baseline` 刷新），
  给每行 `expOS`；仅参考，不抬高 IS 阈值。

失败分支：prod_corr ≥ 阈值 → Mode B 换概念；同一想法 >10 种结构仍不过 → 步 9 记 dead_end，回步 2。

### 步8 S4→S5 稳健闸与提交判定（顺序执行；最终判定唯一权威 = submit_verdict）

【必经】`brain-alpha-robustness`（反过拟合/稳健性闸）。
【Failed-count 资格门（研究侧硬前置）】从 `is.checks` 计算 WebDataScope failed counts，
  REGULAR 要求 `Failed RA == 0`（WARNING/ERROR 也计数，比 `result=="FAIL"` 严格）。
  非零 → 回步 7 修复，不进入提交。
【提交层权威】`mcp__wq-brain-http__submit_verdict alpha_id=<ALPHA_ID>`
  （模拟层 checks + GET `/alphas/{id}/submit` 双视图，403 盲区唯一权威）。
【prod 0.60–0.70 当天提交，不先做变体（2026-09-19 血的教训）】
  `submit_verdict` READY 且 prod < 0.7 → **立即请用户确认提交**；同族第二颗的变体探索放在
  第一颗 ACTIVE 之后。实证（IND pv103 mLm2xG1K）：S 3.83 IS 全过 prod 0.6997，先做变体期间
  外部用户提交同款，复查 prod = 1.0000，整族封死。
【用户确认】SUBMITTABLE 只报告、等用户确认。确认前禁止
  `mcp__wq-brain-http__workflow_submit_alpha` / `mcp__wq-brain-http__submit_batch`。
  `pipeline --submit` = 提交回测，不是提交 alpha。
【配额三通道】REGULAR_SUBMISSION 4/日 + SUPER 1/日 + PPA `POWER_POOL_SUBMISSION` 1/日
  （均 00:00 ET 重置）。配额耗尽按 ET 日历日等待。
失败分支：PASS_CHEAP 可提交；PROD/SELF 不过回步 7；配额耗尽挂起。

### 步9 S6 复盘回写（未回写 = 本波未完成）

【开步先看漏斗】`python tools/step_funnel.py --region $REGION [--wave <W>] [--json]`
  五张 `step_*` 表恒 0 行且不应填充（自动采集是 TODO 空壳）。
【自动回写】`pipeline.py --review` 自动刷新 `region_kb`（recent_waves / gate_priors_local / updated_at）。
【手动回写（必做）】
```
mcp__wqb-db__upsert_wave_result        region=$REGION wave=<W> verdict=<PASS|FAIL|PARTIAL> ...
mcp__wqb-db__upsert_registry_empirical region=$REGION ...
mcp__wqb-db__upsert_ledger_key         region=$REGION key="s6_verdict_<wave>" ...
```
  ★ verdict 只接受 PASS / FAIL / PARTIAL；描述性结论写 `key_findings`（`FAIL_xxx：…` 会被归一化）。
【逐数据集经验沉淀（必做）】`mcp__wq-brain-http__workflow_campaign region=$REGION stage="S6" subcommand="dataset-experience" dataset=<DS> extra_args=["--delay",str($D)]`
  未回测、诊断与待出相关性不能记成已验证成果。
【判死封存】dead_end 回写前 `mcp__wqb-db__seal_dead_end region=$REGION entry_id=<DEAD_END_ID> family=<族名> reason=<带数据的判死原因> rule=<下次怎么办> wave_numbers=[W1,W2,...] forum_recon={"question_key": "<qkey>", "found": false}`（fail-closed 取证闸：`question_key` 取自收批时 `forum_recon_wave` 落的记录或手动 `forum_recon --out negative`；工具故障 ≠ 论坛无解，闸不认；绕过须人工确认，见 RA 步 9 §9.5）
【点塔进度】`python tools/campaign_intel.py pyramid --region $REGION --delay $D`
  输出末尾 [key_findings] 单行直接拷进 upsert_wave_result。
【提交多样性监控】每提交 3–5 颗调 `mcp__wq-brain-http__value_factor_trendScore start_date=<本季初> end_date=<今天>`
【prod 饱和反馈 S0】本波候选全部被 prod 墙卡死 → 除 add-dead-end 外须在 ledger `submit_ready_blocked` 追加饱和记录，
  下一轮 S0 读取后按拥挤处理。
【OS ACTIVE / 全闸 PASS 必须 add-win】mix 比例、中性化、decay、快/慢腿。

【整链（可选）】`mcp__wq-brain-http__workflow_chain dry_run=true chain=[…]`
  先干跑逐节点构建真实命令并做 argv 契约校验（`failed_at` 指首断点）；`join_async=true`（默认）
  等上游后台任务到终态；单步等待上限 `join_timeout_sec`（默认 1800s）。
  ★ 提交类节点不入链：`submit_alpha` / `superalpha` 的 `confirm_submit=True` 必须在步 8 用户确认后单独调用。### 跨区循环与停止（区域无关版专用）

**跨区承接目标（关键机制）**：$TARGET 是**全区**目标，不是单区目标。某区达到"该区已充分开采 /
结构性饱和"（`region_rotation.should_rotate=true`）但全区未达标时：
1. 调 `mcp__wqb-db__region_rotation current_region=$REGION target=$TARGET write_ledger=true`，
   得到 `carry_target`（该区已达标数在全区目标中的剩余部分）；
2. 转 `to_region`，从步 1 重跑该区（步 2 起照常）；
3. 目标按 `carry_target` 递减，直到全区累计达标 ≥ $TARGET 或触发全局停止。

**全区停止规则**（任一命中即停，如实报告，不绕闸）：

| # | 条件 | 动作 |
|---|---|---|
| 1 | `region_rotation.all_saturated=true` | 停。所有候选区结构性饱和，写 ledger `region_rotation`，需用户显式指令才继续 |
| 2 | 全区累计 submit-ready ≥ $TARGET | 达成目标，停并报告 |
| 3 | 当前区信号天花板闸拦截（连续 min_batches 波次 max\|S\| < floor） | 换 universe / 换数据集 / 换区；本区换区仍被拦 → 停止规则 1 |
| 4 | 当前区同轴连续 K 波可计数 FAIL，或窗口内 ≥4 个不同轴全 FAIL 且无新 dead_end | 该轴/该区暂停，转下一区（`region_rotation`） |
| 5 | 当前区连续 3 波 gate 通过率=0（`all_pass` 全 0） | 该信号族/数据集判死，换数据集；换不动则换区 |
| 6 | 当前区白名单被 dead_end 全覆盖 | 转下一区（`region_rotation`） |
| 7 | 配额耗尽 | 挂起提交，继续步 2→9（00:00 ET 重置） |

停止闸阈值引用 `tracking/<R>/config/thresholds.json` 的 `diversity.stop_rules` / `diversity.signal_floor`；
用户显式要求继续时写 `mcp__wqb-db__upsert_ledger_key(region=$REGION, "stop_rules_override", {...})` 放行。

【验收清单（提交给用户前的自检，逐项打勾）】
  □ 步0 库存扫描已先做（build_gate_prior_from_inventory + select_ra_basket），跨区命中已清完
  □ 区域路由已落 ledger `spre_routing`（决策+理由+target），未凭印象选区
  □ `region_rotation` / `get_mining_yield` / `entry_verdict` 三项证据均已消费
  □ 白名单内生成；已点亮塔未作为主数据集；白名单 ≥2 非 MODEL
  □ 每批过步5 门禁（`gate_results.all_pass` 有落库记录）；typed catalog + 体检包就位
  □ 七槽配给 ≥2 跨金字塔、≥1 win 换腿、弱探针 ≤1（且 ≤ 本区 `max_probes_per_wave`）
  □ PROD/SELF 实测：每槽先 1–2 条骨架查 prod；新信号族已过 prod-first 硬门
  □ 提交前 `Failed RA == 0` + `submit_verdict` 200 + 用户确认
  □ 回写三处齐：`wave_results` + `registry_empirical` + `s6_verdict_<wave>`
  □ 全区目标承接正确：carry_target 已递减，未重复计同一颗 alpha
  □ 命中停止规则时已停下并报告，未绕闸烧配额

【禁止（反模式）】
  - 手写 `_gate_waveNN.py` / `w*_batches.json` / 把 `final_expressions.json` 当真相源。
  - 手写 requests；跳步 9；在正文复写阈值；`combination(alpha(...))`。
  - 七槽全裸探针；七槽全 MODEL + 固定 COUNTRY/decay6。
  - 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽。
  - submit_verdict READY 后自动 `workflow_submit_alpha`。
  - 调用已废弃的 `glb_pipeline` / `gbr_pipeline` / `glb_alpha_machine`；`brain-deepExplore`。
  - **跨区照抄档位**（ASI 曾因照抄 USA 档位返空类试错；各区 `static.universe` 必须实测）。
  - **绕过 entry_verdict**（MEA=frozen 硬拒；probe-only 区承诺 N 颗提交）。
  - 把 `workflow_judge` / `workflow_campaign(stage="S2")` 当提交权威或门禁。
  - `region_rotation` 已判 `should_rotate=true` 仍留在饱和区磨参数。

---

## 2. 区域路由速查（编制时实况，仅供参照；执行时必须以运行时读取为准）

> 以下为 2026-09-25 实测 `tools/region_status.py --json` 与 profile 读值的快照。
> **不要把它当真相源**；AI 第一步就是重跑这些命令拿最新值。

| region | profile entry_verdict | 回测 | 命中率 | ACTIVE | waves | exh% |
|---|---|---|---|---|---|---|
| ASI | probe-only | 579 | 34.7% | 5 | 69 | 0% |
| CHN | probe-only | 60 | 0.0% | 0 | 17 | 0% |
| DEU | probe-only | 1402 | 23.0% | 6 | 150 | 0% |
| EUR | active | 569 | 5.1% | 7 | 257 | 100% |
| GBR | active | 493 | 1.0% | 4 | 72 | 0% |
| GLB | active | 2049 | 11.9% | 10 | 114 | 0% |
| HKG | probe-only | 28 | 0.0% | 4 | 10 | 0% |
| IND | active | 782 | 32.6% | 28 | 155 | 95% |
| JPN | active | 238 | 0.0% | 0 | 24 | 0% |
| KOR | active | 366 | 3.8% | 17 | 91 | 77% |
| MEA | **frozen** | 498 | 19.9% | 21 | 78 | 100% |
| TWN | probe-only | —（无 backtest 记录） | — | — | — | — |
| USA | active | 965 | 6.9% | 35 | 172 | 100% |
| AMR | 无 profile | — | — | — | — | — |

> 编制时 `region_rotation --current USA --target 10` 实测：should_rotate=true，转 IND（score=0.5173，
> feasUnsub=21，exh%=95%，prodWall%=0.67，verdict=WATCH）。

**关键提示**：probe-only 区（ASI/CHN/DEU/HKG/TWN）**不承诺 N 颗提交**，其产出率数字（如 ASI 34.7%、
DEU 23.0%）按旧口径（只算 sharpe）统计；严格口径 `ra_failed_checks` 全过的才是 submit-ready。
编制时轮转推荐 IND 是因为它有 21 颗未提交可行存量（实测），这比任何单区产出率都更硬。

---

## 3. 各 profile 静态配置速查（执行时须重读，禁止照抄）

| region | universe（profile） | delay | neutralization_default | 关键提示 |
|---|---|---|---|---|
| EUR | TOP1600/TOPCS1600/ILLIQUID_MINVOL1M | [1,0] | SUBINDUSTRY | win 配方：0.4 慢 MODEL 残差 + 0.6 快 PV，decay4；换腿扩配 |
| GBR | TOP700 | [1,0] | SUBINDUSTRY | TOP700/D1/SUBINDUSTRY 为 region_kb settings_proven；delay0 可探 |
| KOR | TOP600 | [1] | STATISTICAL | 有效面=分析师预期变化；图表/新闻/AI/信用四大红灯；CW 闸升级 FAIL |
| GLB | TOP3000 | [1] | SUBINDUSTRY | 跨区铁律发源地：emotion 死路 + anl15 精确表达式封禁；大宇宙跨区组合 delay 需实测 |
| IND | TOP500 | [1] | SUBINDUSTRY | TOP500 长窗结构区：2Y Sharpe 强，`scale(-rank(x))` 破墙语法实证 |
| JPN | TOP1600/TOP1200 | [1,0] | MARKET | 平台实测档位；D1 共 7 塔全 0 亮；白名单 10 集 6 塔覆盖；`ts_*(vec_*(VECTOR))` 必 ERROR；sector/subindustry/industry 作 group 字段执行必 FAIL |
| MEA | TOP400 | [1] | STATISTICAL | **frozen**：9 数据集全 exhausted，入口即拒 |
| DEU | TOP500/TOP300 | [1,0] | SUBINDUSTRY | 全域 16 类 0 alpha 处女地；sub_universe 结构性墙（limit≈0.47×sharpe，DEU 需 0.8，实测仅 0.30）|
| ASI | 实测（MINVOL1M/MINVOL10M/TOP500）| [1] | SUBINDUSTRY | 处女地全量探针；analyst94 近闸（OS 0.666）、analyst81 untried |
| USA | TOP3000/TOP1000/TOP500 | [1,0] | SUBINDUSTRY | 饱和区；prod_corr_early_warn=0.6；禁经典 value/quality/momentum |
| HKG | 实测 | [1] | STATISTICAL | 半空白小宇宙，处理类 KOR（CW/longCount 严闸） |
| TWN | 实测 | [1] | STATISTICAL | 小宇宙类 KOR；半导体权重股集中度注意 |
| CHN | 实测（TOP2000U）| [1,0] | 实测后定 | 默认档返空类试错前科，static 必须实测 |

★ `src/wqb/config.py::REGIONS` 的 universe/delay 是**平台实测**值（2026-09-22 更新过，
  如 ASI 档位、AMR TOP600、EUR 移除 ILLIQUID_MINVOL1M）；profile 里的 `universe: []` 表示
  **必须 get_platform_setting_options 实测**，两者不冲突时以 config.py + 平台实测为准。

---

## 4. 编制校验记录

| 校验点 | 结论 |
|---|---|
| 主编排入口 | `wq-brain-ra-pipeline` v2.2，last_verified 2026-09-24 |
| 区域权威清单 | `src/wqb/config.py::REGIONS`（14 个）；profile 13 个（缺 AMR） |
| 区域路由工具 | `tools/region_status.py`（--json / --rotate）与 `mcp__wqb-db__region_rotation`（同源） |
| 轮转判据 | `src/wqb/region_rotation.py`（SATURATED/WATCH/VIABLE；feasible_reprieve_min=5） |
| 轮转实测 | `--current USA --target 10` → should_rotate=true，转 IND（score=0.5173，feasUnsub=21） |
| 严格产出率口径 | `get_mining_yield(strict=true)`：ra_clean = sharpe/fitness 达标且 ra_failed_checks 空 |
| 单区版参照 | `docs/usa-ra-mining-prompt-10x.md`（USA profile 已铺好的剧本） |
| 提交判定权威 | `mcp__wq-brain-http__submit_verdict`（唯一）；`workflow_judge` 仅参考层 |
| 提交需用户确认 | `confirm_submit=True` 禁止入自动链 |

> **免责边界**：本提示词是可执行编排剧本，不是产出承诺。$TARGET 是目标；
> 命中跨区停止规则（all_saturated / 信号天花板 / 同轴熔断 / 区级多轴停 / gate 连续 0 通过 /
> 白名单判死全覆盖 / 配额耗尽）即按规则停下并如实报告，不得绕闸。
> 平台硬闸（prod/self 相关性、robust、2Y、CW、换手、longCount、Failed RA=0）最终判定以
> 平台 `is.checks` 与 `submit_verdict` 为准，本工作区不替代平台权威。