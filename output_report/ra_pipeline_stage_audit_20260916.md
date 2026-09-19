# RA 九步流水线逐阶段展开 · 价值评估 · Dry-Run 演练（修订版 v2）

> 日期：2026-09-16 ｜ 对象：`wq-brain-ra-pipeline`（S-PRE→S6 唯一挖掘编排 SOP）
> 依据：SOP 正文 604 行（仓库副本）+ `data/wqb.db` 实测 + 演练实录
> 演练实录：`output_report/ra_pipeline_dryrun_transcript_20260916.txt`（v2，SQL 修正后重跑）
>
> **口径声明**：价值判定基于三类证据 —— ① **实证数字**（DB 实测产出率/积压/达标数）；② **成本收益**（该步消耗配额/时间/还是零成本本地算力）；③ **是否已自我弃用或重复**（SOP 自身已标注的重复项/降级项）。判为"去除"的项均给出替代路径，不做无替代的删减。
>
> **v2 修订说明**（本次审计的自我纠错，亦是给"演练必须用真实数据校验"的示范）：
> - 修正 1：v1 称"IND `wave_results` 仅 1 条（回写严重不足）"——**错误**。系演练脚本步 9 SQL 用错列名（`wave` 应为 `wave_number`），错误被降级捕获后误读。实测 IND 98 条回写、wave92–97 全有 verdict。
> - 修正 2：v1 称"IND `signal_floor` 未声明→天花板闸形同虚设"——**错误**。脚本查了 profile md，而配置实际在 `tracking/IND/config/thresholds.json`，实测 floor=**1.2**（09-11 实证回填，29 波 p25=1.27）。IND 闸是 11 区中收紧最狠的。
> - 修正 3：v1 称"wave95/96 判 STOP_STRUCTURAL 仍开 wave97 = 闭环断裂"——**叙事不成立**。95/96 的 verdict 回写于 08-23，STOP 判定却是本次 09-16 dry-run 事后模拟的，当时并不存在。真实的问题是另一个（见 §10 问题 #6：PARTIAL 语义与规则 B 错位）。
> - 保留确认：IND `s0_ranking` 确实缺失（whitelist 703B 在、ranking 不在，选集不可复算）——v1 此条正确。

---

## 0. 一页总览

| 步 | 阶段 | 核心价值 | 判定 |
|---|---|---|---|
| 1 | S-PRE 查表 | 库存盘点 + conversion/yield 双比率 + 判死先验 | **保留深化**（算子审计并入步 5） |
| 2 | S0 数据集体检 | 三方交叉选集 + 座位可达性 + 零配额停止闸 | **保留深化**（三次 calibrate 调用精简为 1 次） |
| 3 | S1 字段扫描 | 字段 users 分级前置规避 prod_corr | **保留**（feature_engineering 降为按需） |
| 4 | S2 概念优先生成 | GEM 概念优先 + priors 注入 + 设置分流 | **保留深化**（加消化背压） |
| 5 | S2→S3 门禁 | ghost-audit 零成本防连坐 + 体检硬门 | **保留**（两套 check_batch 收敛为 1 套；补体检包） |
| 6 | S3 七槽回测 | prod-first + settings prior 自动改写 | **保留**（积压清理前置） |
| 7 | S4 诊断改进 | 预筛 8× + RN_EXPOSURE + fail-fast/过拟合 | **保留深化**（verdict 语义与停止闸对齐） |
| 8 | S4→S5 提交判定 | submit_verdict 唯一权威 + Failed-count 硬门 | **保留**（judge 三态**精简**为核对清单） |
| 9 | S6 复盘回写 | region_kb 自动刷新闭环 | **保留**（回写纪律实测良好，IND 98/98） |

**总评**：九步骨架健全——"选区→选集→生成→门禁→回测→诊断→提交→回写"闭成自增强回路（S6 回写 → S2 先验自动更新）。真正的判别力集中在 9 项机制（§10 末），其余步骤是它们的承载壳。当前缺口不在缺步骤，而在**四类断层**：S2→S3 积压（EUR 55 倍）、体检包覆盖（DEU/IND/GBR/MEA/TWN=0）、配置形态噪声（DEU 波号时间戳致 floor 统计 0 样本）、PARTIAL 语义与规则 B 错位。另有一个空转表（step_efficiency_metrics 0 行）。

**全区域漏斗实测**（2026-09-16 DB 快照）：

| 区 | 表达式总量 | 已回测 | 转化率 | 达标数 | 达标率 | 诊断 |
|---|---|---|---|---|---|---|
| DEU | 1,658 | 171 | 10.3% | 319* | 24.8% | 全区最健康（*含修复轮历史 1,288 行） |
| IND | ~903 | 190 | ~21% | 91 | 34.1% | 标的健康但 S2→S3 积压 479 条 |
| USA | 3,549 | 312 | 8.8% | 3 | 0.4% | 标的枯竭（133 ACTIVE 存量挖尽） |
| EUR | ~3,754 | 44 | 1.2% | 25 | 8.5% | **积压 55 倍，S2→S3 断链典型** |
| KOR | ~1,320 | 91 | 6.9% | 13 | 4.7% | 积压（pending 244 + gated 106） |
| GBR | ~777 | 21 | 2.7% | 0 | 0% | 停止闸教训区（180 条 0 达标） |
| MEA | 626 | 275 | 44.1% | 99 | 22.0% | 转化好但 MEA 已 frozen（零边际收益） |

---

## 1. 步 1（S-PRE）查表：区域先验 + 库存盘点

### 输入
- 唯一驱动输入：`region`（如 IND/DEU）
- 静态输入：`references/regions/<R>.md`（12 份 profile，front-matter 含 entry_verdict / priors / gate_overrides / loop_policy）
- 动态输入：DB `campaign_summary` / `dead_ends` / `dead_datasets` / `cross_region_lessons` / `mining_yield`；账户库存（`expressions` + `backtest_results`）

### 处理过程
1. **读 profile 入口裁决**：`active` / `probe-only` / `frozen`（MEA=frozen 即拒，唯一后门见该区 profile）。
2. **库存盘点（先于一切新挖）**：`build_gate_prior_from_inventory --regions all`（枚举存量 IS alpha → 资格门复算 → 写回过闸率先验，供步 4 GEM 消费）→ `select_ra_basket --target 20`（去参数网格 + OS 撞车预筛 + 篮内正交 `compute_mutual_correlation` + 平台复核 `is.checks` 无 FAIL）。只有候选池不足以覆盖目标金字塔时才进步 2。
3. **算子审计（ghost-op guard）**：`operator_audit` 拉平台实时算子表 vs catalog，幽灵算子替换表回 `docs/reference/operators_notes.md`。
4. **PPA 主题门禁**：`get_messages(limit=30)` 扫 Power Pool 公告，解析当期主题 region/delay/universe 精确匹配；不匹配的达标候选标 YELLOW + WAIT_THEME_ROTATION。
5. **先验查询五连**：campaign_summary / dead_ends / dead_datasets / cross_region_lessons / mining_yield（全区排名 + 本区按集拆）。
6. **产出率二分诊断**：`conversion`（已回测/已生成）低 = 流水线问题（S2→S3 断链，修管道别换区）；`yield_rate`（达标/已回测）低 = 标的问题（换区换集，别加生成量）。

### 输出
universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号（未落盘，供步 2 消费）；库存篮 `cache/basket.json`（足量则直接跳步 8）。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **库存盘点**（先清库存再开新挖） | ★★★ **保留并强化** | 实证是数量级差异：2026-09-07 跨四区 **170 次新回测产出 0 条**可提交 RA，同日**一次库存扫描产出 20 条**。成本几乎为零（本地 SQL + 本地互相关不占平台配额），收益最高 |
| **conversion / yield_rate 双比率** | ★★★ **保留** | 唯一能把"流水线断链"与"标的本身不出货"分开的判据，直接决定"修管道 vs 换区"。**实测命中**：IND conversion ~21%（积压型断链）但 yield 34.1%（标的全区最优）→ 正确动作是清积压而非换区 |
| **判死台账（dead_ends / dead_datasets）** | ★★★ **保留** | 零成本复算；DB 实测 dead_end 总量：EUR 110 / KOR 76 / IND 53 / USA 27 / GBR 27 / DEU 30。直接避免重复踩死路 |
| **算子审计（ghost-op guard）** | ★★ **降级：并入步 5** | 与步 5 `campaign_intel ghost-audit` 同源（均围绕平台 ghost_ops 清单）。步 1 审一次、步 5 再审一次属重复。建议步 1 只保留"新会话首次/catalog 变更"触发，实体裁判定留在步 5 dispatch 前 |
| **PPA 主题匹配门禁** | ★★ **保留但降级为"提交时门禁"** | 主题轮动无公开时间表（两次实证 PURE_POWER_POOL_THEME 不过，只能等轮换）；把不可控的外部时序当开工前置会阻塞主线。改为：开工不阻塞，步 8 提交前判 WAIT_THEME_ROTATION 即可 |
| 可选并行（next-move / forum-browse） | ★ | 不产出配置，仅侦察价值；按需调用，不进主链 |

---

## 2. 步 2（S0）数据集体检 + 金字塔白名单

### 输入
region + delay + universe（S-PRE 产物）；候选数据集；`registry_empirical` win 层；台账 `s0_ranking` / `s0_whitelist` / `*_dead`。

### 处理过程
1. **三方交叉选集**：`campaign_intel s0-select` = 平台点塔 `recommend_datasets`（pyramid 端点实测，非本地推断）× `mining_yield`（本区历史产出率先验）× `get_dead_datasets`（台账判死）。产出"未点亮塔 × 高产出 × 未判死"候选，判死自动沉底。
2. **评分与校准**：`score_datasets.py`（0.4*cov + 分段拥挤惩罚 + 0.2*字段丰富度 + 0.1*valueScore）；`calibrate=true` 自学习校准（先 dry-run 人工审甜区异常再 apply）。
3. **评分增强**（P0/P2/P3/P5/P6）：empirical_prior（实测 ceiling_ratio 拉向过闸概率）、饱和集自动 excluded、universe 一致性守卫、饱和区 model 封顶 1.0 + score/pyramid_view 双榜、calibrate token 去重。
4. **硬约束**：win 层配方族必进候选；pyramid_quota ≥2 非 MODEL；category_weight 0.9–1.15；*_dead 排除；饱和路由（alphaCount≥1 万或连续 2 波模板全灭 → 强制 hypothesis-first）。
5. **座位可达性（P1）**：每候选 est_seats（同族高互相关只算 1 座）；Σest_seats < target → `[WARN] 结构性不可达` → 扩集/换区而非打磨。
6. **override 审计（P4）**：手工捞回判死集必须带 `override:{reason,auto_tier,auto_excluded_by}`，否则报 override-gap 不予锁定。
7. **零配额停止闸前置**：规则 A（回测 ≥100 且达标 0 → 停区）/ 规则 B（最近 3 个 closed 波 verdict 全 FAIL → 停区）+ 信号天花板闸（最近 min_batches 波 max|Sharpe| < floor → 拒开波）。默认 enabled=True（`STOP_RULES_DEFAULTS`），区域 thresholds 可覆盖。
8. 锁白名单：`upsert_ledger_key(region,"s0_whitelist",...)`。

### 输出
ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead`。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **s0-select 三方交叉** | ★★★ **保留深化** | 把 S0 从"本地 alphaCount 推断饱和"升级为"平台 pyramid 端点实测点亮"，直接服务主攻未点亮塔目标；判死自动沉底。DEU 09-16 凌晨判死 continuation_score 后下一次 s0-select 即时沉底——先验新鲜度直接兑现 |
| **座位可达性 `est_seats`** | ★★★ **保留** | Σest_seats < target 即报"结构性不可达"——把"在不足座位上反复打磨"这一隐性浪费显式化；DEU 单骨架困局（SA 差 4 组件）正是缺这个视角的代价 |
| **停止规则闸 + 信号天花板闸** | ★★★ **保留并修两个坑** | 纯 DB 零配额、干跑也走，是唯一能拦住"GBR 跑满 180 条回测达标 0 条"这类沉没成本的机制。**坑 1**：`max_sharpe_floor` 兜底只在"有节缺字段"时生效，整节缺失/enabled:false 静默放行（fail-open）——**坑 2（本次新发现）**：DEU floor 统计"样本 0 波"是因 DEU wave_number 为时间戳形态（如 1789243887），统计脚本不识别 → floor 恒 0.5 形同虚设，需先归一化波号形态再统计 |
| **饱和路由** | ★★★ **保留** | alphaCount≥1 万集结构性饱和（DEU model25/28 记忆实证：116 候选全 five-factor 同骨架 SELF 0.9+）→ 强制 hypothesis-first 是唯一出路 |
| **P3 universe 一致性守卫** | ★★★ **保留** | coverage/alphaCount 跨 universe 不可比，分位线错位会导致"看着过了实际没过" |
| **empirical_prior (P0)** | ★★ **保留** | 把评分目标从"数据干净"拉向"能过闸概率"；需 thresholds opt-in，推广未完 |
| **override 审计 (P4)** | ★★ **保留** | 防"无解释的手工捞回"，治理价值 > 产出价值 |
| **三次 `workflow_campaign(calibrate/dry_run/实跑)`** | ⚠ **精简为 1 次** | 三次串行调用拉长 S0 耗时；calibrate 反学的 category_weight 已被 P5 封顶逻辑部分覆盖。建议仅保留 `calibrate=true dry_run=true` 一次人工审，确认后直接锁白名单 |
| **score 公式本身** | ★★ **保留（冻结）** | 四因子权重无严格验证，但分位 tier 带兜底 + 六件套补丁后实用性可接受；不建议继续加因子 |

---

## 3. 步 3（S1）字段扫描 + 理解

### 输入
dataset（白名单内）/ delay / universe。

### 处理过程
1. `workflow_campaign(stage="S1")` → scan_fields 建 **typed catalog**（MATRIX/VECTOR/EVENT 类型 + 覆盖 + users）。
2. **字段分级风险筛查**（prod-corr 规避）：`users ≥50` 只做信号方向验证不入候选池；`10–49` 进候选池但提交前实测 prod_corr；`0–9` 优先池且占批次预算 ≥50%；已确认超标族（GLB techindi predicted_*）零投入。
3. 可选深查：datafield/dataset exploration；`workflow_feature_engineering` 独立调用出 ideas（回写 `s1_<ds>_d<delay>`，标 source）。
4. 失败分支：字段数 <10 退回白名单（探针例外：cov≥0.9 & ac=0 & valueScore≥6 & fields<5 → tier2 Stage-A 单批早停）；VECTOR 比例用 get_datafields 确认，步 4 必须传对 data_type。

### 输出
`fields` 表 + `field_catalog` + ledger `s1_<ds>_d<delay>`（含 ideas_md_path + source 标注）。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **typed catalog（scan_fields）** | ★★★ **保留** | 元数据标错 VECTOR 实为 EVENT → 整批 ERROR（MEA fundamental6 实证）；VECTOR 必先 vec_* 聚合、EVENT 禁 winsorize——类型错配是批级连坐第二大来源。IND 已有 21 份 catalog / 323KB 可复用，边际成本低 |
| **字段 users 分级** | ★★★ **保留** | 在**生成之前**规避 prod_corr 高发区，比生成后靠相关性剪枝便宜得多（后者要付回测与限流成本）。GLB 42 候选全灭于 PROD 0.82–0.86 的教训反向证明必要性 |
| **字段数 <10 守卫** | ★★ **保留** | DEU 白名单实测会真实触发（other545 4 字段、other699 7 字段均 <10）；规则不近人情但成本一致——薄集撑不起七槽多样性，早拦早换 |
| **`workflow_feature_engineering` 独立调用** | ⚠ **降为按需** | SOP 2026-09-15 ② 已实证：该类文档是**确定性模板渲染**（8 问框架 + `rank(ts_mean({f},66))`），注入 GEM 后 GEM 一行 LLM 都不调、整波退化为模板展开（GBR intraday_pv_feats 实证）。它曾是必做项，现已由节点与 runner 主动跳过 → 正文应同步降级为"按需、仅人读参考、禁注入"，避免误导 |

---

## 4. 步 4（S2）选波：概念优先生成

### 输入
dataset / delay / universe / data_type（typed catalog 产物）；`priors_snapshot_<region>`（assemble-priors 确定性组装）；win 层。

### 处理过程
1. **assemble-priors**：wins ≤6（GLOBAL templates + region win_recipes + template_kb validated）+ dead_ends ≤12（dead_patterns + template_kb failed + profile 排除族）+ region_context（methodology + signal_family_rules）；落 DB 快照，取代手写三读。
2. **gate_priors 分流**（2026-09-15 ①）：by_operator_count / by_field_family 进 GEM prompt（表达式层能作用）；by_decay / by_neutralization **不进 prompt**，由步 6 pipeline settings prior 直接改写仿真设置。
3. **GEM 概念优先生成**（pipeline_mode=phased 缺省）：机制 → 1–2 个具体字段 id → Implementation Example；禁止"每个字段套 rank"；生成侧预闸（quantile 归一化无损变换 + 丢弃加权混合毒模式）。
4. **ideas 注入规则**：source ∈ {feature_engineering_node, standalone*} 的模板渲染文档跳过，走概念优先自含生成；显式 ideas_file 可覆盖。
5. **build-wave 选波**：去重/分桶/骨架配给七槽（Token-Bucket C≈7）：≥2 跨金字塔、≥1 win 换腿、弱探针 ≤1 且仅当本波无近闸字段。

### 输出
`expressions(status=gem/enhanced)` + ledger idea + `priors_snapshot_<region>`。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **概念优先 GEM + priors 注入** | ★★★ **保留（最高价值生成机制）** | 禁止"每个字段套 rank"，强制机制→字段→示例链路，是避免产出同质化模板堆的唯一结构性保障；quantile 预闸根治闸 4 ARITY 312 次命中 |
| **gate_priors 分流** | ★★★ **保留** | 修了一个真实长期 bug：此前全塞 prompt → LLM 改不了 decay，S3 永远用固定值（GBR decay=4 实测 3.9% n=408 vs decay=14 28.3% n=46，却三波仍跑 decay4 → **0/44**）。分流后设置层由 pipeline.py 直接改写 |
| **ideas 注入规则修正** | ★★★ **保留** | 阻断确定性模板文档污染 GEM（GBR 实证） |
| **七槽多样性配给** | ★★★ **保留** | KOR wave96–103 八波单字段裸探针 64 条 0 达标 vs wave91c/104 复杂模板即出 2 RA——槽位纪律直接决定产出 |
| **win 换腿 ≥1** | ★★ **保留** | win 配方家族扩展产出率比盲探高一个数量级；但 D11 警示：主导腿不变 → SELF≥0.9 结构性死路，必须换主导信号源 |
| **生成量 vs 消化量** | ⚠ **加背压闸（新增建议）** | 实测 IND：status=gem 370 条未消费，backtested 仅 168 → 生成远超回测吞吐；EUR 积压 55 倍。**建议**：步 4 前先读积压，pending+gated 超阈值时不再生成新表达式，改为清库存（步 1 判据在步 4 的落地） |
| **diversity-extract 可选项** | ★ **从正文移除** | 正文自述"不强制先行、不替代 GEM"；D7 引用条件（≥15 且低 PPAC≥0.7 且新颖度≥0.8）极少同时满足——半弃用状态，归档到决策表附录 |

---

## 5. 步 5（S2→S3）门禁

### 输入
候选表达式集（DB expressions 或 --exprs-file）。

### 处理过程
1. **ghost-audit**（纯本地零配额）：幽灵算子检测（sigmoid/ts_entropy/ts_skewness/ts_percentage/ts_decay_exp_window...），退出码 1 = 隔离到独立小批或换已验证等价算子。
2. **check_batch 多样性**（toolkit `gate.py:check_batch_diversity` 契约式自学习闸 + 收益来源多样性 + 家族天花板）。
3. **wave_gate**（仓根 tools/）：闸 1–5（语法/字段白名单/VECTOR 包裹/ts_min-max/quantile 单参）+ 闸 7/8 数据质量 + **体检硬门 5 条**（低覆盖 cov<0.4 须 ts_backfill；高偏度 |skew|>2 须 rank/winsorize/signed_power；厚尾 kurt>8 须 rank/winsorize；单边恒正负禁原始水平；稀疏事件须 trade_when）。
4. 体检包数据源 `tracking/mining/field_inspect_<region小写>_<ds>.json`（当前 320 包，318 非空：HKG 172 / USA 104 / EUR 19 / CHN 11 / GLB 6 / ASI 5 / JPN 2 / KOR 1；**DEU/IND/GBR/MEA/TWN = 0**）。
5. MCP 等价节点 `workflow_execute(node="wave_gate")`（dry-run 契约 + argv 契约校验）。

### 输出
`gate_results`（all_pass / fail_reasons / report_json）。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **ghost-audit 前置** | ★★★ **保留（ROI 最高的一步）** | 零成本、零配额，且失败模式是**整批 CANCELLED 连坐**（ts_entropy 曾致 20 条全 CANCEL）。一次拦截的收益 = 整批回测配额 |
| **门禁链整体拦截效果** | ★★★ **保留** | DB 实测 fail 分布：EUR 134/243 批（55%）、IND 46/55（84%）、GBR 36/47（77%）、KOR 48/96（50%）、DEU 37/223（17%）。高 fail 率区 = 前置拦截在真实工作；DEU 低 fail = 生成质量已收敛。门禁是配额保护的第一层 |
| **体检硬门** | ★★★ **保留并补齐（当前部分失效）** | 5 条硬门都是把"回测后才发现"前移到"回测前"。**但 DEU/IND/GBR/MEA/TWN 体检包=0** → SOP 明说"缺体检包时本闸不生效"，即低覆盖/厚尾/稀疏事件在这些区一路裸奔到仿真——DEU 是当前最活跃战区（09-16 凌晨仍在跑 W-O/N/D 系列），这是最急的补洞点 |
| **多样性闸** | ★★ **保留但收敛口径** | 当前存在**两套**：`wqb.expression.validator.check_batch`（方法论口径）与 `gate.py:check_batch_diversity`（实跑口径），SOP 自承"两者判据不同，不要以为调了前者就过了闸"。双口径是认知负担与误判源，建议收敛为一套可执行实现 + 一份只读说明 |
| **--skip-diversity-gate 逃生门** | ★★ **保留** | repair 批合理例外 |
| **闸 7/8 数据质量** | ★★ **保留** | 约 17% 死路属结构性缺陷，可静态拦截 |

---

## 6. 步 6（S3）七槽回测

### 输入
gate 通过批次；settings.json（中性化/decay/truncation，可能被 settings prior 改写）。

### 处理过程
1. `workflow_batch_track` → pipeline.py run：n_slots=min(7,批数) 内部锁定；**settings prior 默认开**（region_kb gate_priors 的 by_decay/by_neutralization 中样本≥30 且过闸率≥当前×2 的格子自动改写本波设置并打印 lift；显式 --set 钉住的不动）。
2. **prod-first**：每槽先 1–2 条骨架查 prod_corr，≥0.7 停扩换腿。
3. **批次级故障协议**：8 全 ERROR→重发；CROWDING 连续 2 次→跳过该中性化；fatal 算子→隔离小批；瞬态→拆 5 条/批；429→指数退避；"took too much resource"→真问题（backfill/缩窗）。
4. **收批压缩**：`harvest_multisim_alphas`（18 次调用链压 2 次）+ `harvest_multisim_results` 入库。
5. **积压监控**（波末只读 SQL）：pending+gated > 本波表达式数 ×2 → S2→S3 断链警示，下一波优先 build_wave --from-db 消化近闸积压。
6. S2-COMPLIANCE 已降级为提示；pipeline 中止路径统一 rc=2。

### 输出
`backtest_results` / `wave_results` / checkpoint（断点续跑）。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **prod-first** | ★★★ **保留** | 每波 40 条测 IS、近闸再查 prod，会浪费 39 条在已知 prod 墙上；先查骨架是数量级的配额节省 |
| **settings prior 自动改写** | ★★★ **保留** | GBR decay 实证的落地侧；"无 lift 不改写"的保守语义正确 |
| **批次级故障协议表** | ★★★ **保留** | 每行都有实证编号（USA/D0 三次、ts_entropy、e10a/e10b、b87/b92/b93、model26）；"先归因再决定重发/跳过/拆批"避免盲目重试烧配额 |
| **argv 契约校验 + detached 存活握手** | ★★★ **保留** | `--concurrency 7` 拼给没有该参数的脚本 → argparse exit=2 + detached 不看退出码 = "S3 启动成功却从未真跑"，证据在 stderr 躺了 13 天——三件套防三类"假成功" |
| **积压清理** | ⚠ **前置到步 1/步 4（当前仅在波末提示）** | 实测 IND pending+gated=479 vs backtested=190；EUR gated 2,229+pending 231 vs backtested 44（积压 55 倍）。规则早已有但只在波末提示太晚；应作为步 1/步 4 的准入条件（积压超阈值→不再生成，先清库存） |
| **S2-COMPLIANCE 降级为提示** | ✅ **正确的精简（已执行）** | 闸 2/3 的真保障是 typed catalog，重复的中止路径只制造假失败与 --force 滥用 |

---

## 7. 步 7（S4）诊断改进

### 输入
本波 alpha_id（wave 标签精确解析）+ 指标（sharpe/fitness/2y/margin/tvr/is.checks/risk_neutralized_sharpe）。

### 处理过程
1. `workflow_campaign(stage="S4")` → review_wave.py --alphas --tag --write-ledger（解析不到即 FAIL，干跑也 FAIL）。
2. **s4-prescreen 预筛**：批量拉指标分层 READY/REVIEW/REJECT；REJECT（全灭）不进链，只对存活者走 selfcorrQuick → check_self_correlation → compute_mutual_correlation → check_correlation → robustness → judge 完整链。
3. **RN_EXPOSURE 硬规则**（已接线进 walls()/passes()）：risk_neutralized_sharpe ≤0 且 sharpe≥1.58 ⇒ 该 alpha 就是它声称的因子暴露，直接 dead_end 禁调参。
4. **辅助腿检索**：`get_salvage_pool(boost_dim=boost_2y|cw|tvr|sharpe, exclude_dataset=主集, min_sharpe=1.0)`。
5. **组合形态合规（2026-09-13 定案）**：禁任何加权混合（gate 闸 5 block），仅允许结构交互（ts_corr/ratio/价差/条件/分组）或 SuperAlpha combo。
6. 优化走 `wq-brain-alpha-optimization-v1`（Mode B 概念 70% / Mode A 参数 30%）；`brain-alpha-repair` 只作配方查表。
7. **prod 验证串行泳道**：本地检查全批先跑、prod 队列恒 1 在飞、等待期插本地活（7 天缓存 + refresh 终验）。
8. **fail-fast 机器判定**（`_lib/rules.py::classify_failure`）：七信号 → STOP_STRUCTURAL / RETRY_FIXABLE / INCONCLUSIVE。

### 输出
分层结论 + ledger `s4_walls_<region>_<wave>` + salvage_pool 更新 + 改进候选。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **s4-prescreen 预筛压缩** | ★★★ **保留** | 8 条候选从 8 次逐条评审压到 1 次预筛 + 仅存活者进链，**评审效率约 8×**，且 REJECT 直接判死省掉最贵的平台相关性调用 |
| **RN_EXPOSURE 硬规则** | ★★★ **保留（判别力最强的一条）** | `risk_neutralized_sharpe ≤ 0` 且 `sharpe ≥ 1.58` ⇒ 不是超额是暴露。实证：HKG w4 七条里六条 RN 在 −0.33~−0.57 而 raw sharpe 非零；w3 的 `O0roWEM7`（RN 0.96 ≈ raw 1.17）是约 150 次回测中**唯一**真信号。这条把"看起来达标"与"真超额"分开 |
| **fail-fast + 过拟合机器判定** | ★★★ **保留** | 演练实测非真空：wave97=RETRY_FIXABLE、wave96/95=STOP_STRUCTURAL（七信号命中明细见 §11）；把"要不要止损"从人的判断变成表的判断 |
| **判死结果未回灌停止闸** | ⚠ **补闭环（真实缺口，但非 v1 所述形态）** | 真实问题不是"判死仍开波"（时间线证明 95/96 判定当时不存在），而是：**规则 B 只认 verdict==FAIL，而 0 达标的 PARTIAL 不计入**——wave96 verdict=PARTIAL（达标 0）却放行 wave97。0 达标连续多波时停止闸咬不住。修法：规则 B 增加"达标数=0 也算 fail-equivalent"子条件，或 verdict 枚举增加量化判据 |
| **组合形态合规** | ★★★ **保留（但须同步修 D3）** | 防过拟合 + 防同源正则毒模式；**矛盾**：决策表 D3 仍教"跨金字塔用 win 配比 add(0.40*慢MODEL, 0.60*快PV)"——与"禁任何加权混合"直接冲突（DEU 09-16 凌晨 gate5_weighted_mix_policy 显示平台约束已回滚 v1.2 收紧）。修法：D3 改写为"仅结构交互或 SA combo"，旧加法配方标注历史口径已废弃 |
| **Mode B/A 配比 70/30** | ★★ **保留** | KOR wave96–104 背书；D12 镜像反转（EUR fcf_to_price sh−1.9→镜像 1.91）是高价值细则 |
| **prod 串行泳道** | ★★ **保留** | prod 相关性调用是最贵的平台资源之一；恒 1 在飞 + 等待期插本地活是吞吐与配额的正确折中 |
| **brain-alpha-repair 只作配方查表** | ✅ **已正确降权** | — |

---

## 8. 步 8（S4→S5）稳健闸与提交判定

### 输入
S4 存活候选 alpha_id；is.checks。

### 处理过程
1. **Failed-count 资格门**（研究侧硬前置）：从 `is.checks` 计算 WebDataScope failed counts（WARNING/ERROR 也计数，比 result==FAIL 严格）；REGULAR 要求 Failed RA==0；非零回步 7。
2. **submit_verdict（唯一权威）**：模拟层 checks + `GET /alphas/{id}/submit` 双视图（403 盲区唯一权威）；SUBMITTABLE 只报告、等用户确认。
3. **brain-alpha-judge（可选参考层）**：PPA 主题匹配/相关性人工核对清单 + VF trend score 参考；READY/REVIEW/BLOCK 三态仅参考。
4. 用户确认后 → `workflow_submit_alpha` / `submit_batch`（配额 REGULAR 4/ET 日 + SUPER 1 + PPA 1，00:00 ET 重置）。

### 输出
SUBMITTABLE 判定 + 用户确认记录 + 提交结果。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **submit_verdict 唯一权威** | ★★★ **保留** | 覆盖 403 盲区与"模拟层 PASS 但提交层拒"的不一致（"以为走 PPA 实走 REGULAR"的 blRnKEk6 案例即靠它穿透）；**必须保留"仅报告、等用户确认"** |
| **Failed-count 资格门** | ★★★ **保留** | 比 result==FAIL 严格（WARNING/ERROR 也计数）；201 受理后异步失败=扣配额，此门是防"静默扣配额"的唯一手段 |
| **brain-alpha-judge 三态输出** | ⚠ **精简** | judge 已于 **2026-08-31 自我弃用最终判定角色**，代码里已无提交路径。**保留其三项真实职能**（PPA 主题/相关性人工核对清单、value-factor trend score、点塔优选排序），**去掉三态输出**以免与 submit_verdict 并存造成二次权威 |
| **robustness 稳健闸** | ★★★ **保留** | 反过拟合必经，且本仓已可复用 overfit_signals 做机器化 |

---

## 9. 步 9（S6）复盘回写

### 输入
本波全部结果（backtest_results + gate_results + 提交状态）。

### 处理过程
1. **自动部分**（pipeline --review）：写 wave_results + 自动刷新 region_kb（recent_waves 近 20 波摘要 / gate_priors_local 本地重算过闸率 / updated_at）。
2. **手动部分**：upsert_wave_result（verdict 强制枚举 PASS/FAIL/PARTIAL，描述性结论进 key_findings）；registry_empirical（win：OS ACTIVE/全闸 PASS 必须 add-win 含 mix 比例/中性化/decay/快慢腿）；ledger `s6_verdict_<wave>`。
3. **seal_dead_end（先沉降再封存）**：失败候选入 salvage_pool（收集宽）→ dead_end.salvage 回填残值列表；动用侧守 mode_b_qualification（动用严）。
4. **点塔进度回写**：`campaign_intel.py pyramid` → key_findings 嵌塔进度，下一波 S0 直接消费平台真实塔状态。
5. **提交多样性监控**：每 3–5 颗提交调 `value_factor_trendScore`（VF 定 base payment 档位，防同质化降权）。
6. **T+1 IS→OS 衰减归因**（可选）：performance_comparison 写回 wave_result。
7. **prod 饱和反馈 S0**：候选全灭于 PROD≥0.7 → `submit_ready_blocked` 追加数据集饱和记录 → 下一轮 S0 按拥挤降级。

### 输出
`wave_results.verdict` / `region_kb` 刷新 / `registry_empirical` / ledger 全家。

### 价值评估

| 项 | 判定 | 依据 |
|---|---|---|
| **region_kb 自动刷新** | ★★★ **保留（最高价值闭环）** | 使下一波步 4 assemble-priors 与步 6 settings prior 读到的**总是最新**，把"人工回写才更新"的依赖彻底移除。DEU 09-16 凌晨一夜 6 条判死，下一波 GEM prompt 即时包含 |
| **回写纪律** | ★★★ **保留（实测良好，v1 结论修正）** | DB 实测全库 532 波有 verdict（IND 98/98 含 wave92–97 全部回写）——"未回写视为本波未完成"纪律执行率高，v1"仅 1 条"系演练脚本 SQL 列名错误所致 |
| **seal_dead_end 先沉降再封存** | ★★★ **保留** | 判死不丢残值，salvage 池承接组合救援；"收集宽、动用严"分层设计合理。DEU salvage 已有实际沉淀（insider 卖出系、oth47 镜像窗口族等） |
| **pyramid 进度回写** | ★★★ **保留** | 与 S0 三方交叉首尾呼应（S6 写 → S0 读），点塔战略数据闭环；DEU 塔 MODEL 6/3 已亮、OTHER/SI 2/3、INSIDERS 1/3 的投向决策直接由它驱动 |
| **prod 饱和反馈环** | ★★★ **保留** | DEU analyst93 拥挤族（gJQdpNoK 0.8038/9qVmQjKq 0.7598 实测）→ submit_ready_blocked → 白名单降级——SOP 里最接近"闭环控制"的设计 |
| **VF trendScore 监控** | ★★ **保留** | 收入机制挂钩（Quantity 强次线性边际 ~6.5%/颗，堆数量低 ROI）；每 3–5 颗一次频率合理 |
| **T+1 衰减归因** | ★ **保留为可选** | 实际消费率低（无系统性执行证据）；不必推广 |

---

## 10. 精简/去除建议汇总（可执行，按优先级）

| # | 建议 | 类型 | 依据 | 风险 |
|---|---|---|---|---|
| 1 | 步 5 两套 `check_batch` 收敛为一套可执行 + 一份只读说明 | **收敛** | 双口径易误判"调了前者就过了闸" | 中（需确认实跑口径不被改） |
| 2 | D3 决策表改写：删除/废弃加法配比方子，统一为结构交互口径 | **修矛盾** | D3"加法优先"vs 步 7"禁加权混合"直接冲突；平台约束 v1.2 已收紧 | 低 |
| 3 | 补 DEU/IND 体检包（活跃战区优先） | **修复** | DEU/IND/GBR/MEA/TWN=0，体检硬门在这些区静默失效 | 低 |
| 4 | step_efficiency_metrics 表落地或删除 | **治理** | 0 行空转；本报告漏斗分析已证明三表 JOIN 可覆盖 | 低 |
| 5 | 步 1 算子审计降频为"catalog 变更触发"，与步 5 ghost-audit 去重 | **去重** | 同源同实现 | 低 |
| 6 | 规则 B 增加"达标数=0 的 PARTIAL 也计入 fail-equivalent"子条件 | **补闭环** | wave96 PARTIAL（0 达标）放行 wave97——0 达标连续多波时停止闸咬不住 | 低 |
| 7 | DEU 波号形态归一（时间戳→序号）后重算 signal_floor 样本 | **修复** | DEU floor 恒 0.5（样本 0 波）系 wave_number 时间戳形态不被统计识别 | 低 |
| 8 | 步 4 消化背压：积压超阈值不再生成，先清库存 | **新增** | IND gem 370 vs backtested 168；EUR 积压 55 倍 | 中（需定阈值） |
| 9 | 步 2 三次 calibrate 调用精简为 1 次 | **精简** | 收益被 P5 封顶覆盖 | 低 |
| 10 | signal_floor 整节缺失改为拒绝开波（fail-open→fail-closed） | **加固** | 整节缺失/enabled:false 静默放行与停止闸使命矛盾 | 低 |
| 11 | IND `s0_ranking` 补建（whitelist 在、ranking 缺，选集不可复算） | **修复** | 本次 DB 实测确认缺失 | 低 |
| 12 | feature_engineering 正文明确"按需、仅人读参考、禁注入" | **降权** | 确定性模板渲染退化 GEM（GBR 实证） | 低 |

> **不建议去除**（本 SOP 的实际判别力所在，共 9 项）：库存盘点、conversion/yield 双比率、s0-select 三方交叉、座位可达性、RN_EXPOSURE、ghost-audit、prod-first、submit_verdict、region_kb 自动刷新。其余步骤多数是它们的承载壳。

---

## 11. Dry-Run 演练实录（IND，纯只读，v2 修正后重跑）

脚本：`logs/_tmp_ra_pipeline_dryrun.py`（已修正步 9 SQL 列名错误）｜ 实录：`output_report/ra_pipeline_dryrun_transcript_20260916.txt`
约束：**只读 DB 与文件，不 subprocess、不写库、不建目录、不触平台**。

### 逐步输入 → 输出 → 价值判定

| 步 | 关键输入（实测） | 演练输出/判定 | 价值判定 |
|---|---|---|---|
| 1 | profile `entry_verdict=active`；yield **34.1%**；conversion **33.9%**；pending+gated **479** | conversion 低 → **S2→S3 断链** | 应先**清库存**而非开新挖；判死台账 53 条 IND dead_end 可零成本复用 |
| 2 | `s0_whitelist` 存在(703B)；**`s0_ranking` 缺失**；近 3 波 maxS 2.04/1.28/1.05 | 规则 B 未命中 → 放行 | 白名单已沉淀但 ranking 缺失致选集不可复算；信号天花板闸**生效**（thresholds.json floor=1.2，v1 查错位置） |
| 3 | typed catalog **21 份 / 323 KB** | 字段分级可复用 | 高价值，边际成本低 |
| 4 | `status=gem` **370**；priors 快照存在(2034B) | 生成 > 消化 | 需背压（建议 #8） |
| 5 | gated 309 / gem 370；**体检包 0 个** | **体检硬门不生效** | 低覆盖/厚尾/稀疏事件裸奔到仿真（建议 #3） |
| 6 | pending+gated 479 vs backtested 190 | **断链确认**（>2× 本波量） | 吞吐是瓶颈；积压规则仅波末提示太晚（建议 #8/#10 联动） |
| 7 | wave97 n=9 maxS=2.04；wave96 n=8 maxS=1.28；wave95 n=8 maxS=1.05 | **wave97=RETRY_FIXABLE**（weight_concentration_high）<br>**wave96=STOP_STRUCTURAL**（subuniverse_repeat_fail + weight_concentration_high）<br>**wave95=STOP_STRUCTURAL**（pnl_backhalf_decay + fitness_persistent_miss + subuniverse_repeat_fail） | 判定有效且**非真空**；**但注意**：这是本次 09-16 事后模拟判定，95/96 波当时（08-23/24）的 verdict 是 FAIL/PARTIAL 已回写——事后 fail-fast 与当时 verdict 之间的口径差即建议 #6 的由来 |
| 8 | ProdCorr 下限示例 (y=.95,k=.85) = **0.643** | 未超限 → 仍需实测 | 该式只能"确定性劝退"，不能"确定性放行"——submit_verdict 实测不可省 |
| 9 | **wave_results 98 条**（v1 误报 1 条，系 SQL 列名错误）；最近 5 条：149=PARTIAL, 3=FAIL, 2=FAIL, 148=FAIL, 147=FAIL | 回写纪律实测良好 | v1"回写严重不足"结论**撤销**；region_kb 自动刷新价值不受影响 |

### 演练暴露的真实问题（v2 修正后重新梳理，按严重度）

1. **积压断链无前置闸**（最严重）：IND conversion 33.9% / pending+gated 479 vs backtested 190；EUR 55 倍积压。按 SOP 自身判据正确动作是清积压修管道，但步 4 仍会无节制生成——积压判断只在波末以只读 SQL 提示，没有牙齿。
2. **体检硬门在活跃区静默失效**：IND/DEU 体检包=0（DEU 是当前最活跃战区）。低覆盖/厚尾/稀疏事件裸奔到仿真，等价于把 CONCENTRATED_WEIGHT、LOW_TURNOVER 等结构性失败留到回测后才发现。
3. **PARTIAL 语义与规则 B 错位**：wave96 verdict=PARTIAL（0 达标）不计入"全 FAIL"停止条件——0 达标连续多波时停止闸咬不住。这不是"判死没回写"（回写良好），而是 verdict 枚举粒度粗于停止闸需求。
4. **配置形态噪声**：DEU wave_number 时间戳形态（如 1789243887）使 signal_floor 统计"样本 0 波"→ floor 恒 0.5；IND s0_ranking 缺失致选集不可复算。都是"配置存在但形态不被消费方识别"的静默失效。
5. **演练脚本自身的教训**（元问题）：v1 的三个错误论断全部源于"降级捕获 + 未核对原始 SQL 错误"——SQL 报错被 `q()` 降级成 `[SQL-ERR]` 后，`len(err_list)=1` 被读成"仅 1 条回写"。**演练结论必须以能通过最简单交叉核验的查询为据，降级路径必须显式暴露而非静默吞掉。**

---

*本报告基于 SOP 仓库副本（604 行）与 `data/wqb.db` 2026-09-16 实测。v2 修订均已用独立查询复核。dry-run 全程未修改任何生产数据、未触平台 API、未占用任何配额。*
