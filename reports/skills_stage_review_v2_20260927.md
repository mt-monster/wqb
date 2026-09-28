# RA 九步流水线：逐阶段展开 · 价值评估 · 独立 Dry-Run 演练

- 日期：2026-09-27（22:50 起）
- 性质：**纯评审 + 模拟演练；未修改任何业务文件、未写库、未发平台请求**
- 权威依据：`Claude/skills/wq-brain-ra-pipeline/SKILL.md`(v2.2)、`references/decision-table.md`、`INDEX.md`、`src/wqb/workflow/registry.py`、`src/wqb/config.py`
- 独立复现：`python reports/dryrun_chain_runner_v2_20260927.py` → `reports/dryrun_chain_result_v2_20260927.json`
- ⚠ **并行说明**：本机另有会话正在撰写 `reports/ra_pipeline_stage_review_20260927.md`（112KB，含四轮真实环境复跑）。本报告为**独立第二视角**，采用不同 runner 与不同输出文件，未覆写其任何产物。

---

## 0. 研判口径与基线

### 0.1 五条判据

| 判据 | 含义 | 反例 |
|---|---|---|
| **V1 可验证产物** | 产出可被下游消费的结构化产物（DB 表 / ledger 键 / 文件包） | 只产人读文本 |
| **V2 有真实调用方** | 存在生产路径调用点 | 零调用方、仅注释提及 |
| **V3 有实证收益** | 有前后对照的量化收益记录 | 仅口头声称 |
| **V4 不可被合并** | 判断与其它步骤不重叠、不可归并 | 与另一闸同源重复拦截 |
| **V5 成本合理** | 零配额/本地可算，或有明确配额回报 | 高配额消耗换取低产出 |

### 0.2 本次实测基线（只读，2026-09-27 22:50）

```
data/wqb.db  size 277,856,256 B / 9049 行级摘要如下
  expressions       65,730   dropped 34,081 / gem 18,047 / superseded 8,085
                             selected 2,327 / pending 1,495 / backtested 1,470
                             fail 83 / gated 67 / completed 38 / submitted 31
  backtest_results   8,398
  gate_results       1,533
  wave_results         949   verdict: FAIL 572 / PARTIAL 284 / PASS 92 / NULL 1
  alphas             8,454   （已测 prod 421）
  ledger_kv          4,698
  **unconsumed 未消化 = 21,936**（gem+selected+pending+gated）
workflow 节点 18 个（导入 nodes 包后注册）
区域：config.REGIONS = 14；region profile = 13（缺 AMR）；战役目录 20（含 mining 等非区域目录）
```

**两条贯穿结论**：
1. **未消化积压 21,936 条是本链最大的结构性问题**——S2 生成速度长期高于 S3 消费速度；
2. 本轮 dry-run 中启动期两条 WARN 直接量化了它：`41 个活跃波（270 条）无 gate 记录`（门禁断链）、`80 个 pending/gated 波超 7 天未动（约 1,945 条）`。

---

## 1. 逐阶段展开（输入 / 处理 / 输出）

### 步 1 · S-PRE 查表 + 库存盘点

| 项 | 内容 |
|---|---|
| **执行者** | `wq-brain-ra-pipeline` 编排 + `mcp__wqb-db__get_*` + `tools/build_gate_prior_from_inventory.py` / `select_ra_basket.py`；节点 `inventory_scan` |
| **输入** | `$REGION`（唯一显式输入）、`references/regions/<R>.md`（13 份 profile，`entry_verdict` 裁决）、DB 四表存量、`reports/dataset_experience/*.md` |
| **处理** | ① profile 裁决（MEA=`frozen` 步 1 即拒）；② **库存盘点优先**：枚举存量 alpha → 资格门复算 → 写回 `gate_priors` → `select_ra_basket --target 20`（去参数网格/OS 撞车预筛/篮内正交/平台复核）；③ 产出率双比率分离（`conversion` 低=管道问题、`yield_rate` 低=标的问题）；④ PPA 主题门禁 |
| **输出** | universe / delay / 中性化 / 排除集 / 排除信号族 / 波号 + `gate_priors` 快照 + `cache/basket.json` |
| **失败分支** | registry 全空=新区域；候选不足才进步 2 |

### 步 2 · S0 数据集体检 + 白名单

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_campaign(stage="S0")` + `campaign_intel s0-select` + toolkit `score_datasets.py --calibrate` |
| **输入** | `get_datasets` 平台清单、`get_pyramid_alphas` 实测点亮、`region_kb` win 层、`saturated_datasets`、`field_inspect_<region>_<dataset>.json` 体检包 |
| **处理** | ① 三方交叉：`recommend_datasets`（平台真实点塔）× `get_mining_yield`（严格口径）× `get_dead_datasets`（判死）；`lit=Y` 已点亮塔直接剔除；② **两步必需**：`calibrate` 反学权重与拥挤甜区（**只写 thresholds、不产排名**）→ 裸 `stage="S0"` 产 `s0_ranking`；③ 座位可达性校验（Σ`est_seats` < target → WARN）；④ 锁白名单（≥2 个非 MODEL、`category_weight` 0.9–1.15）；⑤ 饱和路由 |
| **输出** | `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` |
| **失败分支** | 配额后无非 MODEL → 写 findings；全硬排除 → 回步 1 换区 |

### 步 3 · S1 字段扫描 + 理解

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_campaign(stage="S1")`（toolkit `scan_fields.py`）+ L1 三件套 + `feature_engineering` 节点 |
| **输入** | 白名单数据集 + `get_datafields` |
| **处理** | ① typed catalog 落地 `fields` 表 + ledger `s1_<ds>_d<delay>`；② **字段级覆盖审计**（铁律①：`recommend_datasets` 不校验区域覆盖率）；③ **幽灵字段验活**（铁律②：`validate_fields=true`，避免提交层 COMPILE_ERROR）；④ `users` 分级（≥50 只验方向 / 10–49 进池必实测 prod / 0–9 优先，冷门占批 ≥50%） |
| **输出** | `field_catalog` + S1 ledger 决策 + 预处理决策（backfill/winsorize/rank/ts_event_*） |
| **失败分支** | 字段 <10 退回步 2；VECTOR 比例确认后步 4 传对 `data_type` |

### 步 4 · S2 概念优先生成（GEM）

| 项 | 内容 |
|---|---|
| **执行者** | `mcp__wq-brain-http__workflow_gem` → `brain-make-some-gem/scripts/headless_runner/run.py`（内部把 FI + DFE 两份 SKILL.md 拼进 prompt） |
| **输入** | priors 快照（`assemble-priors` 从 DB KB 确定性组装，fail-closed）+ S1 catalog + ideas 注入 + `config.json` |
| **处理** | ① priors 组装（只消费 `wins`≤6 / `dead_ends`≤12 + sha256 快照）；② **gate_priors 分流**：`by_operator_count`/`by_field_family` 进 prompt，`by_decay`/`by_neutralization` **不进**（是仿真设置，由步 6 改写）；③ LLM 概念生成（机制→1–2 字段 id→Implementation Example；复杂度预算 2–5 算子）；④ `pipeline_pregate` 落盘前预闸（quantile 归一/毒模式丢弃/hump-bucket 参数补全/非标窗口归一/同骨架封顶 `WQB_GEM_MAX_PER_SKELETON=12`）；⑤ 落 `final_expressions.json` → 入库 `expressions(status=gem/enhanced)` |
| **输出** | `expressions` 新行 + `expression_count` / `quality_estimation` / `mode_b_required` |
| **失败分支** | 401/402/403 立即抛（本轮已修）；GEM 未入库先查 `--status`；候选不足 enhance/换集 |

### 步 5 · S2→S3 门禁（含 5b prod-first）

| 项 | 内容 |
|---|---|
| **执行者** | `tools/wave_gate.py` → toolkit `gate.py check_batch_diversity` + `field_inspect_gate.py` + `campaign_intel ghost-audit` / `prod-first`；节点 `wave_gate` / `unified_gate` |
| **输入** | 本波 `expressions`（`--from-db`）+ typed catalog + 体检包 + `platform_constraints.json` + `explore_contract` + `alphas` prod 记录 |
| **处理** | ① **幽灵算子硬闸**（纯本地零配额；含幽灵算子整批 CANCELLED 连坐）；② 8 闸：语法(含元数)/白名单/VECTOR 类型/不可访问算子/毒模式/**闸6 批级多样性**/longCount/EVENT；③ **体检硬门 5 条**（低覆盖须 backfill / 高偏度须 rank / 厚尾须 rank / 单边禁水平 / 稀疏事件须 trade_when）；④ **闸 PF 骨架级 prod 死路预检**（fail-closed）；⑤ 5b：新信号族首探 prod，≥0.7 记 dead_end |
| **输出** | `gate_results`（`all_pass`/`fail_reasons`）+ `prod_first_<wave>` |
| **失败分支** | 语法 FAIL 必修；多样性 FAIL 回步 4 补骨架；repair/probe 批豁免多样性契约 |

### 步 6 · S3 七槽回测

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_batch_track` / toolkit `pipeline.py run`（并发唯一来源 `wqb-concurrency` §8） |
| **输入** | 过闸批次 + `settings.json` + `region_kb.gate_priors` |
| **处理** | ① **settings prior 改写**（`min_n=30` 且过闸率 ≥ 当前×2 才改写；显式 `--set` 钉住不动）；② **七槽填槽**（Token-Bucket C≈7；multi(8) 86.1 α/hr = single 1.59×）；③ **连坐隔离**（ERROR 子模拟定位坏式 → 回写 fail → 无辜式重发批优先下槽）；④ 账户级槽位仲裁（`logs/_slots/` token，`WQB_GLOBAL_SLOTS=7`）；⑤ 收批压缩（18 次调用链→2 次）；⑥ 积压检查（pending+gated > 2× 本波 → 断链告警） |
| **输出** | `backtest_results` + `wave_results` + `ckpt_w<W>` + `expressions.status=backtested` |
| **失败分支** | 故障协议表（8 子全 ERROR 重发 / fatal 算子隔离 / 429 退避 / took-too-much-resource 去 backfill） |

### 步 7 · S4 诊断改进

| 项 | 内容 |
|---|---|
| **执行者** | `review_wave.py` + `campaign_intel s4-prescreen / prod-first` + `brain-how-to-pass-alpha-test` + `wq-brain-alpha-optimization-v1`；节点 `campaign(S4)` / `auto_review` / `structural_reconstruct` |
| **输入** | 本波 `backtest_results` alpha_id + `thresholds.review` + OS 衰减基线 |
| **处理** | ① **s4-prescreen 分层**（REJECT 直接判死，只存活者走完整链，效率 ≈8×）；② **walls 诊断**：`RN_EXPOSURE` 墙（risk_neutralized ≤0 且 sharpe≥1.58 ⇒ 就是那个暴露本身，判 dead_end 禁调参）+ near 池拒收结构性死信号（robust ratio<0.5）；③ **prod-first 探针**（族首 → STOP 后不扩变体）；④ OS 衰减校准（expOS = IS×0.358，仅参考不作排序）；⑤ 卡闸辅助腿检索 `salvage_pool boost_*`（禁加权混合） |
| **输出** | `s4_walls_<region>_<wave>` + `salvage_pool` + review payload + 换概念/换腿决策 |
| **失败分支** | prod ≥0.7 → Mode B 换概念；同想法 >10 结构不过 → 步 9 记 dead_end 回步 2 |

### 步 8 · S4→S5 稳健闸 + 提交判定

| 项 | 内容 |
|---|---|
| **执行者** | `brain-alpha-robustness`（必经）+ `mcp__wq-brain-http__submit_verdict`（唯一权威）+ `worldquant-submit-alpha` |
| **输入** | 达标候选 + `is.checks` 全量 + WebDataScope failed-counts |
| **处理** | ① Failed-count 资格门（RA 要求 `Failed RA == 0`，比只看 `result=="FAIL"` 严格）；② `submit_verdict` 零成本判定（`degraded_gates` 非空 ⇒ 不可作依据）；③ prod 0.60–0.70 当天提交不做变体；④ 报告 SUBMITTABLE → **等用户确认**；⑤ POST 四形态处置（200 通过 / 201 异步 4min 未翻状态 re-POST / 200 空体必须补发 / 403 零成本带回全量 checks） |
| **输出** | `submit_ready` 台账 + ACTIVE alpha（REGULAR 4 + SUPER 1 + PPA 1，三者并行） |
| **失败分支** | PROD/SELF 不过回步 7；配额耗尽挂起提交继续步 2→9 |

### 步 9 · S6 复盘回写

| 项 | 内容 |
|---|---|
| **执行者** | `tools/step_funnel.py` + `upsert_wave_result / upsert_registry_empirical / upsert_ledger_key` + `campaign_intel pyramid` + `dataset-experience` + `seal_dead_end`；节点 `campaign(S6)` / `auto_pyramid` / `auto_harvest` |
| **输入** | 本波四表存量 + ledger + 平台塔状态 |
| **处理** | ① `step_funnel` 只读定位瓶颈（**不凭印象写 verdict**）；② `upsert_wave_result` verdict **强制枚举**（MCP 层归一+拒绝；直写路径已堵）；③ 判死封存（先 `seal_dead_end` 沉降入 salvage_pool，再记 dead_end）；④ **region_kb 自动刷新**（`recent_waves` 近 20 波 + `gate_priors_local` + `updated_at`）；⑤ `pyramid` 点塔进度进 key_findings；⑥ `dataset-experience` 逐集经验沉淀 |
| **输出** | `wave_results.verdict` + `registry_empirical` + `s6_verdict_<wave>` + `reports/dataset_experience/*.md` |
| **失败分支** | 停止闸 B1/B2 机械判定（同轴 3 连可计数 FAIL 熔断 / 窗口内 ≥4 轴全 FAIL 停区；零配额与产出新 dead_end 的 FAIL 波豁免） |

---

## 2. 逐阶段价值评估

### 2.1 汇总表

| 步 | 判定 | 保留理由（V1–V5 中最强者） | 精简/修正项 |
|---|---|---|---|
| 1 S-PRE | **★★★ 保留深化** | **V3**：09-07 实证 170 次新回测 0 产出 vs 一次库存扫描 20 条（数量级）；**V5**：零配额 | `inventory_scan` 节点未入 SOP 正文；`latest_wave` 对字符串波号排序弱 |
| 2 S0 | **★★★ 保留深化** | **V3**：已点亮塔剔除治本（IND 7 集 197 条 0 候选）；两步 calibrate→score **非冗余**（calibrate 只写 thresholds 不产排名，实测确认） | 可选项 `calibrate --dry-run` 属条件触发，日常可跳；**体检包 5 区为 0**（DEU/IND/GBR/MEA/TWN）→ 该区硬门空转 |
| 3 S1 | **★★★ 保留深化** | **V1/V4**：typed catalog 是闸 2/3/8 的判据来源（缺目录 stage_gate 直接 FAIL）；**V3**：幽灵字段验活避免整批连坐；users 分级直接决定 prod 规避 | `feature_engineering` 作"字段理解"用时 **V1/V3 双不通过**（确定性模板渲染、无 LLM；GBR 实证注入 GEM 致零 LLM 调用）→ 已收口为"仅人读" |
| 4 S2 | **★★★ 保留深化（当前最优先）** | **V1**：65,730 条 expressions 的唯一来源；**V3**：gate_priors 分流治"prompt 改不了 decay"根因（GBR decay14 过闸 28.3% vs decay4 3.9%，而三波仍跑 decay4 → 0/44） | **产能过剩**：未消化 21,936 条；生成侧预闸仍漏 `hump` 命名参数（09-25 单日 12 次） |
| 5 门禁 | **★★★ 保留（精简展示层）** | **V3**：幽灵硬闸防连坐、闸 PF 骨架级预检（同字段不同骨架 prod 0.76–0.82 vs 0.46–0.57）；**V5**：纯本地零配额 | `[opcat]`/质量预估**只打印不判定**（自称硬闸却进不了 `all_pass`）→ 噪声；`validator.check_batch` 零生产调用方且判据不同 → 建议 deprecated；**5 区体检硬门空转** |
| 6 S3 | **★★★ 保留** | **V5**：七槽 ×7 吞吐（实测 86.1 vs 54.3 α/hr）；**V3**：连坐隔离（JPN 一条 `bucket()` 缺 range 致整批连坐丢 64 条）、settings prior 直接改设置 | **SOP 指定的 `batch_track` 入口不跑停止/天花板/积压三闸**（只有 `campaign(S3)` 跑）→ 闸覆盖有缺口 |
| 7 S4 | **★★ 部分精简** | **V3**：prescreen ≈8× 效率；`RN_EXPOSURE` 硬规则（HKG w4 七条里六条为假信号） | **Mode A 参数层收益低**（实证仍撞 prod 0.84–0.85）→ 压缩；`RN_EXPOSURE` 行仍进 near/salvage 池（应一并排除） |
| 8 S4→S5 | **★★★ 保留** | **V1**：65 颗 ACTIVE 唯一路径；**V3**：四形态补发闭环（3 颗曾悬空 >24h） | `src/wqb/config.py::compute_webdata_failed_counts` 有第三份与生产口径**相反**的实现（生产 failed_ra=3 vs config 0）→ 陷阱 |
| 9 S6 | **★★★ 保留** | **V1/V4**：唯一让九步成"环"的步骤（region_kb 自动刷新使步 1/4/6 先验无需人工回写）；verdict 枚举闸保证停止规则 B 真实 | 五张 `step_*` 表已下线但文档残留引用；**存量 verdict 非枚举行**（历史遗留）已由本轮治理回填 |

### 2.2 精简 / 去除明细

| 项 | 处置 | 依据 |
|---|---|---|
| `wqb.expression.validator.check_batch` | **去除或 deprecated** | V2 不通过：全仓零生产调用方；且只实现 4 条形状闸、判据与 `gate.py:check_batch_diversity` 不同 → 双口径误读风险 |
| 五张 `step_*` / `*_summary` 表 | **清理文档残留** | 实测 DB 中不存在（step-metrics 子系统 09-17 已下线归档） |
| `[opcat]` / 质量预估的"FAIL"打印 | **精简**：并入 `all_pass` 或改为 INFO | V1：自称硬闸却不参与判定 → 噪声 |
| 步 3 `feature_engineering` 作字段理解 | **已收口**（保留人读参考） | V1/V3 双不通过；禁止注入 GEM |
| 饱和路由 → `brain-alpha-research-hypothesis-first` | **二选一**：补生成器 or 摘路由 | 该 skill 的 catalog 仅 1 文件、无生成器 → 路由是死路 |
| 无入边 L1 三个 skill（field-quality / news-sentiment / labs-data-analysis） | **摘除或并入** | 无入边 + 零产出 + 引用失效（`WebData_*.zip` 实为目录；CLI 不存在） |
| `brain-alpha-repair` | **并入 optimization-v1** | 43 行纯配方查表 |
| `planning-with-files` hooks | **收敛触发条件** | 全局注入在 WQ 任务产生副作用 |
| `pull-brain-skills --dest` | **加 layer/命名校验** | 默认直写权威目录无守卫 |

### 2.3 需修正的缺口（D 级）

| # | 缺口 | 证据 | 建议 |
|---|---|---|---|
| D1 | S2/S3 产能失衡 | unconsumed **21,936**；启动期 WARN 点名 80 波 1,945 条超 7 天未动 | 给 S2 加"S3 实测吞吐"准入配额 |
| D2 | 5 区体检硬门空转 | 334 个包中 DEU/IND/GBR/MEA/TWN = 0 | 开新区即 `--inspect-mode enforce` |
| D3 | 门禁断链 | 启动期 WARN：41 个活跃波 / 270 条表达式无 `gate_results` | 用 `wave_gate.py --wave` 回填（已支持字符串波号） |
| D4 | 停止闸覆盖不全 | `batch_track` 入口不跑三闸，SOP 却指定它作步 6 入口 | 把三闸下沉到 `batch_track`，或改 SOP 指向 |
| D5 | 双份 Failed-count 实现口径相反 | `config.py` 8 项 vs `mcp_core.py` 17 项；同一组 checks 得 0 vs 3 | 删除/转发第三份 |
| D6 | 生成侧预闸漏 `hump` | 09-25 单日仍 12 次 | 生成侧加硬约束，不靠门禁兜底 |
| D7 | `RN_EXPOSURE` 行仍可入 near/salvage | near 池只排除 `ROBUST_STRUCTURAL` | 一并排除 |

---

## 3. 独立 Dry-Run 演练

### 3.1 演练设置

- **输入域**：`REGION=GLB`、`DS=model264`、`DELAY=1`、`UNIVERSE=TOP3000`、`WAVE=s2_mdl264_trendprob_d1`
- **引擎**：`src/wqb/workflow/executor.py::execute(node, params, dry_run=True)`（与生产同一实现）
- **契约**：走完零成本前置 → 构建命令/请求计划 → 到此为止；不 subprocess、不写库、不建目录
- **覆盖**：16 个正例（九步全覆盖）+ 5 个负例（故意错误参数）
- **新增护栏**：本 runner 内置**零副作用探针**——演练前后各取 DB mtime/size/六表行数 + 仓库六个关键目录的文件数与最新 mtime，逐项比对

### 3.2 逐阶段：输入 → 输出变化 → 价值判定

| # | 阶段 | 节点 | 干跑 | 构建出的真实命令（节选） | 价值判定落地 |
|---|---|---|---|---|---|
| 1 | 步1 S-PRE 库存盘点 | `inventory_scan` | OK | `build_gate_prior_from_inventory.py --regions GLB --emit-candidates cache/candidates.json --write-priors` | **V3 活证明**：先清库存再开新挖，省掉 S2 全链 |
| 2 | 步2 S0 打分 | `campaign` | OK | `score_datasets.py --campaign-dir <repo>/tracking/GLB` | 三方交叉选集 + 座位可达性 |
| 3 | 步3 S1 字段 | `feature_engineering` | OK | `feature_engineering.py --region GLB --dataset model264 --delay 1 --universe TOP3000 --category MODEL …` | 保留为**人读**（禁入 GEM） |
| 4 | 步4 S2 priors | `campaign` | OK | `campaign.py --campaign-dir … assemble-priors` | 先验唯一上游化 |
| 5 | 步4 S2 GEM | `gem` | OK | `run.py --config <skillroot>/…/config.json --data-type …` | ⚠ **LLM 可达性干跑验证不了**（假绿盲区） |
| 6 | 步4 S2 选波 | `campaign` | OK | `build_wave.py --campaign-dir … --dataset model264 --wave s2_mdl264_trendprob_d1 --from-db` | 去重/分桶/骨架配给 |
| 7 | 步5 门禁 | `wave_gate` | OK | `wave_gate.py --campaign-dir … --region GLB --dataset model264 --wave … --from-db` | 8 闸 + 体检硬门 + 闸 PF |
| 8 | 步5 合并门禁 | `unified_gate` | OK | 流程计划：`ghost_operator_gate` → `diversity_gate` → `field_inspect_gate` → `unified_gate_check` | 四闸串接 |
| 9 | 步6 S3 回测 | `batch_track` | OK | `pipeline.py --campaign-dir … run --dataset model264 --wave … --max-rounds 3 --review --write-ledger` | ⚠ **此入口不跑三闸**（D4） |
| 10 | 步7 S4 诊断 | `campaign` | OK | `review_wave.py --campaign-dir … --alphas … --tag … --write-ledger` | walls + RN 墙 |
| 11 | 步7 S4 评审 | `auto_review` | OK | `campaign_intel.py s4-prescreen --ids-file logs/_tmp_s4_ids_…txt` | ≈8× 效率 |
| 12 | 步7 S4 结构变体 | `structural_reconstruct` | OK | `plan_only`（action=report） | 结构层重构入口 |
| 13 | 步8 判定(参考层) | `judge` | OK | `plan_only`（不解析 brain_client，避免触网） | 参考层定位清晰 |
| 14 | 步9 S6 复盘 | `campaign` | OK | `campaign.py --campaign-dir … --wave …` | verdict 枚举 + key_findings |
| 15 | 步9 点塔回写 | `auto_pyramid` | OK | `campaign_intel.py pyramid --region GLB --delay 1` | 点塔进度 |
| 16 | 步9 自动收批 | `auto_harvest` | OK | 流程计划：`auto_harvest` → `auto_link` → `auto_upsert` → `auto_report` | 收批压缩 |

**结果：正例 16/16 通过。**

### 3.3 负例验证（干跑不是假绿）

| 负例 | 结果 | 回传 error |
|---|---|---|
| S4 波号不存在 | 已拦 | `no backtest alphas for GLB/s2_nonexistent_d1` |
| 未注册区域 `XYZ` | 已拦 | `Cannot resolve campaign_dir for region=XYZ. Set WQB_CAMPAIGN_DIR or WQB_WORKSPACE_ROOT…` |
| `wave_gate` 缺 dataset | 已拦 | `Missing required params: ['dataset']` |
| `gem` 缺 universe | 已拦 | `Missing required params: ['universe']` |
| `batch_track` 缺 wave | 已拦 | `Missing required params: ['wave']` |

**5/5 被拦且均带可诊断 error**（无 `success=False + error=None` 的静默失败）。

### 3.4 零副作用验证（本 runner 内置探针）

| 检查项 | 演练前 | 演练后 | 结论 |
|---|---|---|---|
| `data/wqb.db` mtime | 1790508208095483100 ns | **同值** | 未写库 |
| `data/wqb.db` size | 277,856,256 | **同值** | 未写库 |
| `expressions` / `backtest_results` / `gate_results` | 65,730 / 8,398 / 1,533 | **同值** | 未写库 |
| `wave_results` / `alphas` / `ledger_kv` | 949 / 8,454 / 4,698 | **同值** | 未写库 |
| 仓库六目录（logs/tracking/data/reports/cache/output_report）文件数与 mtime | — | **零变化**（`tree_changed: {}`） | 未建目录/文件 |

**`db_changed: false` / `tree_changed: {}`** —— 零副作用严格成立。

### 3.5 干跑无法覆盖的环节（诚实声明）

1. **GEM 的 LLM 可达性**：干跑只构建命令，验证不了 LLM 余额/通道；已知余额不足时表现为误导性的 `no meta.json within 90s`，**干跑会显示假绿**。
2. **步 8 的 `submit_verdict` 与真实提交**：按设计不入演练（提交类必须用户显式确认）；本次用 `judge`（参考层）代位。
3. **步 1 库存篮的平台复核**：依赖 `GET /alphas/{id}`，干跑不触网。
4. **步 5b prod-first 探针**：网络依赖，未演练。
5. **口径非精确转化率**：`step_funnel` 各步取各自表存量、时间窗不一，链上数值可能不单调，仅用于定位瓶颈。

---

## 4. 演练暴露的现场信号（真实读取，非推演）

启动期两条 WARN 是本次演练最有价值的实况输出：

```
[wave-key-check] WARN: 41 个活跃波（270 条表达式）无 gate_results 记录（门禁断链或未执行）。
  Top: GLB/probe_glb_w1..w5_20260921 (各 8 条)
[wave-ttl-check] WARN: 80 个 pending/gated 波超 7 天未动（约 1,945 条表达式积压）。
  Top: IND/s2_news79_d1(55条), IND/s2_news_sentiment_transfer_d1(382条), IND/170(34条) …
```

这两行把 §2.3 的 D1/D3 从"静态统计"升级为"运行时可观测"，也印证了护栏本身有效。

---

## 5. 审阅清单

| # | 事项 | 我的建议 | 需你决策 |
|---|---|---|---|
| 1 | 九步判定：8 步 ★★★ 保留、步 7 部分精简 | 认可则无需动作 | ☐ |
| 2 | S2 加"S3 实测吞吐"准入配额（治 21,936 积压） | **优先做**（唯一作用在真实瓶颈上的改动） | ☐ |
| 3 | 打开启 `--inspect-mode enforce` 补 5 区体检空转 | 做（低风险、fail-closed） | ☐ |
| 4 | 回填 270 条断链波的门禁记录（启动期 WARN 已点名） | 做（`wave_gate.py --wave` 已支持字符串波号） | ☐ |
| 5 | 把停止/天花板/积压三闸下沉到 `batch_track` | 做（补 SOP 指定入口的闸缺口） | ☐ |
| 6 | 去除/标注 `validator.check_batch` 与五张 `step_*` 残留 | 做（纯清理，无功能影响） | ☐ |
| 7 | 4 个无入边/失效 skill 摘除或并入 | 需你拍板范围 | ☐ |
| 8 | 饱和路由：补 hypothesis-first 生成器 vs 摘路由 | 需你选路线 | ☐ |

> 备注：本报告与并行会话的 `reports/ra_pipeline_stage_review_20260927.md` 互为独立第二视角（不同 runner、不同输出文件、未互相覆写）。若两报告结论冲突，建议以**可复现的运行结果**为准而非文字表述。
