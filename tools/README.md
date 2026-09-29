# tools/ 通用工具索引

区域无关的战役工具链。约定：
- **退出码**：`0`=PASS/成功，`1`=FAIL/失败（可直接串进 pipeline）
- **网络工具运行环境**：MCP venv（`$WQ_PY` 或 `world-quant-brain-mcp/.venv`），自动 `os.execv` 重启，勿用系统 python
- **skill 依赖路径**：自动解析 `WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR` → `~/.qoder-cn/skills` → `~/.workbuddy/skills`，**禁止硬编码**

## 提交前闸门（构建候选池后、回测前）

| 工具 | 用途 | 取代 |
|---|---|---|
| `wave_gate.py` | 每波门禁编排：语法校验 + 5 闸 + 六维多样性 + 质量预估（EXPECTED_BLOCK 默认标注，`--quality-block` 硬拦截），一键落盘 `cache/gate_wave<N>_<ds>.{json,txt}` | `tracking/<R>/scripts/_gate_waveNN.py` 族 |
| `pool_diversity.py` | 候选池表达式结构多样性评估（算子熵/骨架配额/字段集中度/预处理/成对相似度/主导族风险，六维），`--file/--exprs/DB`，`--json` 落盘；已被 `wave_gate.py` 集成调用 | 手写多样性统计脚本 |
| `quality_predict.py` | 候选池质量预估（回测前）：三层先验预估 Sharpe/Fitness + 本地结构代理预估 SELF_CORR 风险，输出 EXPECTED_PASS/REVIEW/EXPECTED_BLOCK；`--status UNSUBMITTED` 直筛存量池，已被 `wave_gate.py` 集成调用 | 手写相关性/质量预判脚本 |
| `legacy/gate.py` | **遗留归档**：通用提交前闸门（5 闸 + 批级多样性）。**权威实现是 skill toolkit 的 `gate.py`**；本文件代码零引用（`wave_gate.py` 走 `_TOOLKIT_CANDIDATES` 加载 toolkit 版），2026-09-20 归档至 `tools/legacy/` | — |
| `legacy/backfill_backtest_dataset.py` | **一次性回填已跑完**（`backtest_results.dataset` 只填空），2026-09-28 按 §6.4 归档至 `tools/legacy/`（三维引用全 0） | — |
| `forum_recon.py` | **问题驱动论坛只读检索（recon，2026-09-28）**：单问题 → 有效文章 → 入库（`KB/community_tpl_kb.forum_recon_entries` 或 ledger `forum_recon_<qkey>`；无解落 `forum_recon_negative_*` 作「论坛无解」判死证据）。额度以查出有效文章为标准（自适应扩关键词，命中即收束）；同问题 7 天缓存；抓取核心复用 `forum_research.py`（不重复 HTTP 实现）；`--dry-run` 零副作用；退出码 0=有货 / 2=无解 | 手写论坛抓取、每次现搜不落库 |
| `expr_lint.py` | 算子签名/字段白名单快速门禁（非战役场景） | — |
| `corr_precheck.py` | 相关性墙预判（设计阶段字段重叠检查） | — |

## 回测与状态

字段级经验快照：`dataset_experience.py --region EUR --delay 1` 从 DB 导出每个已回测数据集的
`reports/dataset_experience/eur_<dataset>_campain.md`。支持 `--dataset`、`--waves`、`--dry-run`；
只读数据库，保留人工复盘段。S6 入口为 `workflow_campaign(subcommand="dataset-experience")`。

| 工具 | 用途 | 取代 |
|---|---|---|
| `mcp_7slot_batch.py` | 七槽并发回测（MCP 驱动，`--alpha-json` + `--settings-json` + `--output-csv`）。★ 2026-09-17 修正：此前本表写 `mcp_5slot_batch.py`，**该文件并不存在** | — |
| `batch_status.py` | 批次/子任务状态查询与 `--watch` 轮询（multisim 或单条） | `tracking/_scratch/check_*batch*.py`、`track_mea_super_resume.py` 轮询段 |
| `harvest_multisim.py` | multisim 收批：拉 children → 拉 alpha 详情 → 关联 expressions → 可选 upsert backtest_rows | `tracking/*/scripts/poll_wave*.py`、手写收批脚本 |
| `submit_batch.py` | 批量**派发仿真**（`POST /simulations`；`--spec` 支持逐批不同设置）。⚠ 不是把 alpha 提交上平台——那是不可逆的 `workflow_submit_alpha(confirm_submit=True)` | 31 个 `_submit_*.py` |

## 探针编排（新数据集首探）

S2选波沿用toolkit `build_wave.py`：`--size`为容量；预定实验使用
`--selection-contract-key`读取DB机制/对照清单，按ID与原式核对，不固定8条。
使用说明及延后项审计见[选波实验清单](../Claude/skills/wq-brain-campaign-toolkit/references/selection-plan.md)。

| 工具 | 用途 | 取代 |
|---|---|---|
| `probe_batch_mode.py` | 2+6 探针批模式：L0（2 条）快速判死 → L1（6 条）信号确认，真实回测（入库→pipeline→DB 拉指标） | 手写 8 探针表达式 + 手动判定 |
| `tiered_probe.py` | 三层探针编排器：L0 判死 → L1 确认 → L2 ModeA 变体自动升级；组合腿快腿轮换（fast_pool 多样性）；慢腿预处理轮换（raw/reverse/ts_decay_linear） | 手写 ModeA 变体波 |

> `wave_gate.py --probe-mode` 只做门禁阶段探针分配标记（结构预判），真实回测判死走 `probe_batch_mode.py` / `tiered_probe.py`。

## SUPER alpha 流水线

| 工具 | 用途 | 取代 |
|---|---|---|
| `sa_probe.py` | 组件池探针：≥10 ACTIVE REGULAR 硬前置，GO/BLOCKED | `probe_kor_sa.py`、`tracking/_scratch/probe_sa2_*.py` |
| `super_build.py` | select / status / probe / submit 四子命令全流程；**submit 内置 prod 闸（2026-09-25）：probe max≥0.7 或超时一律拒提（fail-closed），豁免须 `--allow-prod-above-07`** | `track_mea_super.py` / `_resume` / `_submit` 三件套 |

## 提交判定

| 工具 | 用途 | 取代 |
|---|---|---|
| `prod_first_screen.py` | **区域未提交存量的 prod 首筛**（prod-first 纪律的机械执行）：枚举区域内 IS 合格 & 未提交的 alpha → 逐条测 prod（`refresh=true`，服务端计算）+ self（本地）→ **断点续跑**（state 文件，prod 取不到不入 state 下次重试）→ 测得的数值**回写 `alphas.prod_correlation/self_correlation/corr_checked_at`** → 输出「prod<0.7 可提交清单」。★ 背景：全库 370 颗未提交存量里只 97 颗测过 prod、仅 6 颗 <0.7（瓶颈是 prod 不是 IS）；**ASI 95 颗从未测过**故优先。**需 MCP venv 的 Python 跑** | 手工逐条查相关性 |
| `quota_status.py` | **当日提交配额实况（ET 日口径）**：列 `stage=OS` 按 `dateSubmitted` 倒序数**今日（ET）**已提交颗数 → REGULAR 用量/剩余。★ 2026-09-21 事故配套：`GET /users/self/activities/submissions` **只有 yesterday/current/previous/ytd 快照、缺 today**，据此判断当日配额必然误判（实测当日已用 2 个仍显示“昨日 5”）→ 撞 `REGULAR_SUBMISSION(4/4)` 配额墙。**需 MCP venv 的 Python 跑** | 手数控制台提交记录 |
| `submit_verdict.py` | 提交层判定双视图：模拟 checks + `GET /alphas/{id}/submit`（403 盲区拦截，零配额）。★ 出 `SUBMITTABLE` 时**自动把待提交队列该条升级为 `SUBMIT_LAYER_VERIFIED`**（`mark_verified`，2026-09-20） | 手写 GET/POST submit 探针 |
| `os_decay_benchmark.py` | **IS→OS 衰减基准与选品定标**：从 OS 缓存计算保留率分位（ACTIVE / DECOMMISSIONED 双队列）、IS→期望 OS 映射、目标 OS 反推所需 IS，并固化「**IS 对 OS 无预测力**」的决定性检验（n=124：corr(IS,保留率)=+0.001、负 OS 比例恒 ~22%）→ `data/os_decay_benchmark.json`。`--for <IS>` 供选品时查期望 OS 区间 | 口头经验「IS 到 OS 会衰减」 |
| `os_decay_benchmark.py` | **IS→OS 衰减基准与选品定标**：从 OS 缓存计算保留率分位（ACTIVE / DECOMMISSIONED 双队列）、IS→期望 OS 映射、目标 OS 反推所需 IS，并固化「**IS 对 OS 无预测力**」的决定性检验（n=124：corr(IS,保留率)=+0.001、负 OS 比例恒 ~22%）→ `data/os_decay_benchmark.json`。`--for <IS>` 供选品时查期望 OS 区间 | 口头经验「IS 到 OS 会衰减」 |
| `os_report.py` | **已提交 alpha 的 OS（样本外）表现报表**：列表 `stage=OS` 拿全集 → 逐条详情取 `os` 块（`sharpe/sharpe60/sharpe125/returns/drawdown/fitness/osISSharpeRatio`，本地缓存+断点续跑）→ markdown 报表 + CSV。产出「ACTIVE 且 OS Sharpe<0」清单（首要处置对象）、近 60 日恶化榜、Cluster/PowerPool 交叉。★ 知识：**列表端点只带 `osISSharpeRatio`，OS 全量指标只在详情端点**（已验证 `osISSharpeRatio × IS.sharpe = os.sharpe`）。**需 MCP venv 的 Python 跑** | 手查控制台 / 逐条拉详情 |
| `triage_prodcorr_batch.py` | prod_corr 族级抽样（提交层预筛 → 族去重 → 串行抽测，checkpoint 续跑，结果写 `logs/_triage_prodcorr.json`） | 逐条手查 correlations/prod |
| `persist_prod_corr.py` | 把上面的 checkpoint 回填 `alphas` 的 prod/self 相关性（只填 NULL、幂等、默认 dry-run 加 `--apply`；支持 `--source` 溯源与 `--overwrite`）。**运行手册：每轮 S3 批次后跑 triage → 再跑本工具落库**，0.6 预警线才有过程数据 | 手工 UPDATE |
| `query_alpha_metrics.py` | 本地库直查 alpha 全指标（`--coverage` 看填充率；`--region/--max-prod/--max-self/--min-sharpe/--source` 筛候选；`--csv` 导出）。**候选筛选零配额，免打平台 `check_correlation`** | 逐条打平台 correlations API |
| `submit_queue.py` | **待提交候选队列**：把回测过闸的 alpha 持久化到独立表 `submit_ready`，解决"找到可提交项但不当天提交就遗忘"。子命令 `init` / `add`（平台拉指标+相关性）/ `add-many`（离线从 `alphas` 批量导入）/ **`dedup`**（按骨架去重，同区域同骨架只留最优 N 条，其余标 `SUPERSEDED`）/ **`retag`**（按当前规范**重算全队列** `suggested_tags`，规范/解析器升级后回填；`--dry-run`）/ `verify`（相关性时效复检 + **RA 硬闸 + add 混腿**，过期变坏标 EXPIRED/DEAD，开跑前自动退役已 ACTIVE）/ **`sync`**（退役平台已 ACTIVE/已提交的 READY 行，`--offline` 零配额）/ **`regrade`**（离线复判 READY 行：RA 硬闸 / 加权混腿 / prod 兄弟）/ `list`（按优先级排）/ `pick`（取最优先 1 条）/ `retire`（退役）。★ 未过硬闸者自动标 `DEAD` 并从默认视图剔除；★ 2026-09-20 补三坑：RA FAIL（robust/sub-universe/CW/ladder…）不进 READY；加权混腿口径 = gate.py 闸5；同骨架兄弟 prod≥0.7 且本条未测 → `PROD_SIBLING` 判死；SUBMITTED/DEAD 终态粘性（harvest 再入队不复活）+ 排除平台 ACTIVE；`IS_ONLY` 表示 IS 达标但相关性待测，提交前必跑 `verify`。★ 骨架去重复用权威实现 `wqb.expression.skeleton::structural_signature`，`add-many` 默认开启（`--no-dedup` 关，`--max-per-skeleton N` 调） | 手写备忘 / `ledger_kv('submit_ready')` 旧临时队列（**2026-09-20 已归档并删除**，见 `logs/archive_ledger_submit_ready_*.json`） |
| `alpha_properties.py` | **Alpha 属性（name/color/tags）审计与规范化**。规范单一事实源 = `src/wqb/alpha_properties.py`（含平台**实测**的 color 硬枚举 5 值 `GREEN/BLUE/RED/YELLOW/PURPLE`，其余 400），文档 `docs/alpha_properties_spec.md`，审计证据 `reports/alpha_properties_audit_20260920.md`。子命令 `audit`（只读：name 形态/color 分布/tag 合规统计 + 告警清单）· `normalize`（**默认 dry-run**，`--apply` 才写：按 type/`PowerPoolSelected` 判定 `CH_*`、按表达式字段反查补 `SRC_<dataset>`、`--fix-color` 空色→`BLUE`；**不改 name**、**无条件保留 `RETIRE_*` 等已有标签**）。★ 全部 10 区域 ACTIVE(115) 已 `--apply` 规范化 | 手工逐颗改属性 |
| `restore_alpha_props.py` | **事故恢复**：1966 `set_alpha_properties` 全量覆盖曾清空 name / 覆写 description。从 `logs/_os_alphas_raw.json`（事故前转储，221 条）复原 name+regular/selection/combo description。**最小字段 PATCH**（只发要恢复的键，不碰 tags/color）。默认 dry-run，`--apply` 写 | 手工重写描述 |
| `name_missing.py` | 给仍缺 name 的 ACTIVE 补**唯一规范名**（`{REGION}_{R\|S}_{family}_{id尾6位}`；family 由表达式字段反查 SRC 推断）。**必须用 id 短码做后缀**（同族同源会撞名）。默认 dry-run，`--apply` 写 | 手工命名 |
| `finalize_props.py` | **SUPER 命名优化 + 超 5 标签瘦身**（规范化收尾）。SUPER 用 `<REGION>_S_<N>comp_<id6>`（`selectionLimit` 得组件数）；超 5 标签收紧到 ≤5，**必保 `CH_*`/`SRC_*`/`RETIRE_*`/`WAIT_*`**（运维/留痕标记不可砍）。精确 PATCH；默认 dry-run，`--apply` 写 | 手工 |

## 存量池卫生（门禁断链 / 积压裁决）

| 工具 | 用途 | 取代 |
|---|---|---|
| `backfill_gate_plan.py` | 无门禁波规划器（只读）：按 catalog 可行性把无 gate_results 的组分成 A 可立即补门禁（`--commands-file` 出逐组 wave_gate 命令）/ B 缺 catalog / C dataset 为 NULL / D 区目录缺失 | 手写 LEFT JOIN 逐区盘 |
| `backfill_catalogs.py` | 补缺失 typed catalog：枚举白名单缺集（scan_fields 走平台 API，**零配额**）→ `--apply` 逐个生成。2026-09-17 实测 JPN 10/10 成功（2m45s） | 手工逐集跑 scan_fields |
| `backfill_skeletons.py` | 为存量表达式回填骨架签名（`structural_signature`；只填 NULL、幂等、dry-run 默认）。写入侧已自动计算，此工具是一次性回填 | — |
| `pick_backlog_representatives.py` | 积压按骨架去重挑代表 → 直接产出 `mcp_7slot_batch.py --alpha-json` 可消费的清单；`--gate-filter` 先用当前门禁全量筛（失败者不回测），`--drop-list` 落盘失败者 id；**`--apply-drop`** 把失败者标 `dropped`（纪律终态）——三守卫：必须配 `--gate-filter` + `--db-backup`、只动 `alpha_id IS NULL` 且状态未变者、分批 rowcount 校验 + ledger 台账留痕 | 手工挑候选 / 手改状态 |

## 战役情报（S0 选集 / 点塔进度 / S4 预筛 / 幽灵算子）

| 工具 | 用途 | 取代 |
|---|---|---|
| `campaign_intel.py s0-select` | S0 选集增强：recommend_datasets（平台真实点塔）× mining_yield（历史产出率）× dead_datasets（判死清单）三方交叉 → 「未点亮塔 × 高产出 × 未判死」候选清单 | Agent 逐个调 MCP 再人工拼结论 |
| `campaign_intel.py pyramid` | 点塔进度快照：各 catalog 点亮状态/乘数/还差几颗（S6 回写时调，输出 `[key_findings]` 单行供直接嵌入 wave_result） | 手工查 pyramid 端点 |
| `campaign_intel.py s4-prescreen` | S4 预筛压缩：批量拉指标 → READY/REVIEW/REJECT 分层，REJECT 直接判死不进 S4 链 | 逐条 get_alpha_details 进 S4 链 |
| `campaign_intel.py ghost-audit` | 幽灵算子硬闸：检测表达式是否含平台不认的算子（S2 产物入库后、wave_gate 前调，防整批 CANCELLED 连坐） | 手写算子比对 |

## 区域态势与轮转（饱和检测 → 转区继续挖）

| 工具 | 用途 | 取代 |
|---|---|---|
| `region_status.py` | 区域状态记分板（本地 DB 驱动、零平台请求）：逐区回测量/sharpe 达标/命中率/ACTIVE/波次/战役 exhausted% + entry_verdict + 建议动作；`--json` 机读 | `brain-next-move-analysis §5.5` 区域饱和手算 |
| `region_status.py --rotate --current <R> --target <N>` | **区域轮转决策**：当前区证实结构性饱和→按证据（产出率/可行库存/prod 墙/战役穷尽/profile）排序推荐下一区并承接目标 N；`--write-ledger` 幂等写 `ledger_kv(<R>,region_rotation)`；`--json` 机读 | 人工逐区查表拼“换哪个区”结论 |

> 轮转判定/打分逻辑的**单一事实源** = `src/wqb/region_rotation.py`（纯函数，`tests/unit/test_region_rotation.py` 守护）；CLI（`region_status.py --rotate`）与 MCP（`mcp__wqb-db__region_rotation`）同源。关键纪律：`alphas.prod_correlation` 只对做过相关核查的 alpha 有值，**NULL prod ≠ 可行**（会假阳性），可行集/prod 墙仅在 measured 子集上判定，薄样本回 `data_caveat`；仍有未提交可行存量（feasible_unsubmitted≥`feasible_reprieve_min`）则豁免降级为 WATCH。

## 数据修复（一次性回填，幂等）

| 工具 | 用途 | 取代 |
|---|---|---|
| `backfill_expression_dataset.py [--apply]` | 修复 `expressions.dataset` 被写成 region 名（7,434/13,855 行，2026-09-15 审计）与 `backtest_results.dataset` 缺失：waves→datasets / wave 标签 / gate_results 三路解析，未解析者置 NULL；默认干跑，`--apply` 先备份再写 | 手写 UPDATE SQL |
| `migrate_wave_verdict_enum.py [--dry-run]` | `wave_results.verdict` 归一到 PASS/FAIL/PARTIAL（前缀/关键词规则，原文入 key_findings 首条）；写入侧 `mcp__wqb-db__upsert_wave_result` 已同规则强制 | 人工改行 |
| `backfill_check_columns.py [--apply]` | 回填 **checks 派生列**（`cluster_test` / `concentrated_weight` / `sub_universe_sharpe`）。★ 2026-09-19 修复配套：`harvest_multisim._pick_checks` 此前找的 4 条路径全落空（真实位置是**顶层 `is.checks`**）→ `cluster_test` 一度 0/4,926。本工具用平台详情补齐存量：默认 scope=ACTIVE、只填 NULL、幂等、断点续跑（state 文件）、dry-run 默认。**需用 MCP venv 的 Python 跑** | 逐条手查详情 |

## Cluster Alpha（低门槛区刻意版；依据帖 43562853669655）

| 工具 | 用途 | 取代 |
|---|---|---|
| `build_cluster_variants.py` | 生成**刻意版** cluster 变体：从区域存量信号（默认 `gated`）按骨架去重后套文章配方 —— `cross`=rank(group_mean(SIG,cap,industry))、`equal`=group_normalize 等权行业、`guard`=group_count 防薄行业、`timing`=轮动×择时（区域级）。产出**逐条过当前门禁**（注入 `_region` 触发闸2b），只输出通过者；settings 强制 `neutralization=MARKET`（行业中性化=按构造删掉 cluster 结构）。**JPN 硬拒绝**（闸2b 实测 industry/sector/subindustry 不可用，整批连坐） | 手写 cluster 表达式 |

## 代码体检 / 清理

| 工具 | 用途 | 取代 |
|---|---|---|
| `scan_deadcode.py` | 死代码只读扫描：未用 import + 死定义（排除注册式装饰器 @mcp.tool()/@fixture 等反射调用）；支持 `--path` 单文件/子目录、`--out` JSON 报告 | `tracking/_scratch/_scan_deadcode*.py` |
| `fix_bom.py` | BOM(U+FEFF) 剥离修复：默认 `--dry-run` 列出含 BOM 的 .py；`--apply` 才修（备份 + CJK 数量校验 + ast.parse 校验） | `tracking/_scratch/_fix_bom.py` |
| `clean_unused_imports.py` | 清理未用 import：默认 `--dry-run` 列出；`--apply` 才删（**跨文件 re-export 校验**防 SHAPE_CLASSES 误删 + `.bak_imp` 备份 + ast.parse 校验）；可 `--report` 接 scan_deadcode 的 JSON | `tracking/_scratch/_clean_unused_imports.py` |
| `audit_node_registration.py` | **新增/修改 workflow 节点必跑**：审计「四处同步」——① registry.py 注册与 NodeMeta 签名 ② `test_registry_lists_all_core_nodes` 期望集合 ③ `_DRY_RUN_CASES` 用例表 ④ INDEX.md 节点计数。`--node X` 单节点自检；退出码 1 = 有漂移并列出全部缺口 | 改一处跑一次测试的往返 |

> 三者均遵循 dead-code-cleanup skill 红线：**默认只读/dry-run，删除动作必须显式 `--apply`**。原稿已归档 `attic/tools_archive/_2026-08-28_*`。
>
> 另有 skill 资产同步（不属清理类）：
> | 工具 | 用途 | 取代 |
> |---|---|---|
> | `sync_gem_embedded_skill.py` | 同步 GEM 引擎内嵌的两份 skill 副本到顶层权威版：`brain-feature-implementation/SKILL.md` 与 `brain-data-feature-engineering` 的 `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md`（同名文件不许互相矛盾；**它们不会被拼进 LLM prompt**，2026-09-29 更正，2026-09-26 前内嵌 FI 停在 49 行旧英文稿）。`--check` 只校验（退出码 1 = 漂移）、`--apply` 覆盖写入。**绝不动内嵌 `scripts/`**（`ace_lib`/`validator` 是引擎硬依赖），也不创建 dfe 的 `SKILL.md`。由 `tests/unit/test_gem_skill_paths.py` 守护 | 手动复制 |

## MCP 体检

| 工具 | 用途 |
|---|---|
| `mcp_ping.py` | MCP 服务连通性与调用计时；`--service X` 单服务、`--full` 工具清单、`--timeout N` 每次请求写入及响应的等待上限。显式调用：`--call TOOL --args-file args.json` 或 `--calls-file calls.json`（`[{"tool":"...","args":{}}]`）。工具错误退出码 1；超时退出码 2，包含 method/tool/request_id/outcome_unknown/retry_safe=false，废弃连接且停止后续调用。超时不证明远端未执行，先核对任务/DB再决定重试。默认探针只读；显式调用具有所选工具的效果。 |
| `start_wq_mcp.py` | 启动/确保 `wq-brain-http` MCP 服务在 8876 可用（防"论坛工具找不到"） | `--check` / `--wait N` | — |

## 平台台账同步

| 工具 | 用途 |
|---|---|
| `sync_platform_alphas.py` | 把平台 OS 池（已提交 alpha）全量同步进本地 `alphas` 表，含 **OS（样本外）指标**（`os_sharpe`/`os_fitness`/`osISSharpeRatio`/`os_sharpe60-500` 等 15 列）。解决「平台 228 个已提交 vs 本地台账 94」的漏记缺口（2026-09-20 实测漏 134 条）。`--dry-run` 只报告差异、`--baseline` 打印 OS 衰减基线、`--region X` 限定统计视角。走 MCP venv（brain_api），零配额（只读平台） |

## 纪律（AGENTS.md §9）

1. **禁止新建** `_gate_*` / `check_*batch*` / `probe_*sa*` / `_submit_*` / `track_*_super*` 类一次性脚本；先用本索引查工具。
2. 缺参/缺能力 → 改对应工具加参数（保持 `--help` 自文档），不写新脚本。
3. 一次性排障探针仍可写 `tracking/_scratch/`，但完成即归档 `attic/`，不留在活跃目录。

## 相关参考

- 战例权威实现：`~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/`（`WQ_TOOLKIT_DIR`）
- 平台 API 封装：`world-quant-brain-mcp/brain_api.py`（`BrainApiClient`，自带 429 退避/Redis 缓存）
