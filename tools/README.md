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
| `gate.py` | 战役统一提交前闸门（5 闸 + 批级多样性，权威实现在 skill toolkit） | — |
| `expr_lint.py` | 算子签名/字段白名单快速门禁（非战役场景） | — |
| `corr_precheck.py` | 相关性墙预判（设计阶段字段重叠检查） | — |

## 回测与状态

| 工具 | 用途 | 取代 |
|---|---|---|
| `mcp_7slot_batch.py` | 七槽并发回测（MCP 驱动，`--alpha-json` + `--settings-json` + `--output-csv`）。★ 2026-09-17 修正：此前本表写 `mcp_5slot_batch.py`，**该文件并不存在** | — |
| `batch_status.py` | 批次/子任务状态查询与 `--watch` 轮询（multisim 或单条） | `tracking/_scratch/check_*batch*.py`、`track_mea_super_resume.py` 轮询段 |
| `harvest_multisim.py` | multisim 收批：拉 children → 拉 alpha 详情 → 关联 expressions → 可选 upsert backtest_rows | `tracking/*/scripts/poll_wave*.py`、手写收批脚本 |
| `submit_batch.py` | 批量提交（`--spec` 支持逐批不同设置） | 31 个 `_submit_*.py` |

## 探针编排（新数据集首探）

| 工具 | 用途 | 取代 |
|---|---|---|
| `probe_batch_mode.py` | 2+6 探针批模式：L0（2 条）快速判死 → L1（6 条）信号确认，真实回测（入库→pipeline→DB 拉指标） | 手写 8 探针表达式 + 手动判定 |
| `tiered_probe.py` | 三层探针编排器：L0 判死 → L1 确认 → L2 ModeA 变体自动升级；组合腿快腿轮换（fast_pool 多样性）；慢腿预处理轮换（raw/reverse/ts_decay_linear） | 手写 ModeA 变体波 |

> `wave_gate.py --probe-mode` 只做门禁阶段探针分配标记（结构预判），真实回测判死走 `probe_batch_mode.py` / `tiered_probe.py`。

## SUPER alpha 流水线

| 工具 | 用途 | 取代 |
|---|---|---|
| `sa_probe.py` | 组件池探针：≥10 ACTIVE REGULAR 硬前置，GO/BLOCKED | `probe_kor_sa.py`、`tracking/_scratch/probe_sa2_*.py` |
| `super_build.py` | select / status / probe / submit 四子命令全流程 | `track_mea_super.py` / `_resume` / `_submit` 三件套 |

## 提交判定

| 工具 | 用途 | 取代 |
|---|---|---|
| `submit_verdict.py` | 提交层判定双视图：模拟 checks + `GET /alphas/{id}/submit`（403 盲区拦截，零配额） | 手写 GET/POST submit 探针 |
| `triage_prodcorr_batch.py` | prod_corr 族级抽样（提交层预筛 → 族去重 → 串行抽测，checkpoint 续跑，结果写 `logs/_triage_prodcorr.json`） | 逐条手查 correlations/prod |
| `persist_prod_corr.py` | 把上面的 checkpoint 回填 `alphas` 的 prod/self 相关性（只填 NULL、幂等、默认 dry-run 加 `--apply`；支持 `--source` 溯源与 `--overwrite`）。**运行手册：每轮 S3 批次后跑 triage → 再跑本工具落库**，0.6 预警线才有过程数据 | 手工 UPDATE |
| `query_alpha_metrics.py` | 本地库直查 alpha 全指标（`--coverage` 看填充率；`--region/--max-prod/--max-self/--min-sharpe/--source` 筛候选；`--csv` 导出）。**候选筛选零配额，免打平台 `check_correlation`** | 逐条打平台 correlations API |

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

## 代码体检 / 清理

| 工具 | 用途 | 取代 |
|---|---|---|
| `scan_deadcode.py` | 死代码只读扫描：未用 import + 死定义（排除注册式装饰器 @mcp.tool()/@fixture 等反射调用）；支持 `--path` 单文件/子目录、`--out` JSON 报告 | `tracking/_scratch/_scan_deadcode*.py` |
| `fix_bom.py` | BOM(U+FEFF) 剥离修复：默认 `--dry-run` 列出含 BOM 的 .py；`--apply` 才修（备份 + CJK 数量校验 + ast.parse 校验） | `tracking/_scratch/_fix_bom.py` |
| `clean_unused_imports.py` | 清理未用 import：默认 `--dry-run` 列出；`--apply` 才删（**跨文件 re-export 校验**防 SHAPE_CLASSES 误删 + `.bak_imp` 备份 + ast.parse 校验）；可 `--report` 接 scan_deadcode 的 JSON | `tracking/_scratch/_clean_unused_imports.py` |
| `audit_node_registration.py` | **新增/修改 workflow 节点必跑**：审计「四处同步」——① registry.py 注册与 NodeMeta 签名 ② `test_registry_lists_all_core_nodes` 期望集合 ③ `_DRY_RUN_CASES` 用例表 ④ INDEX.md 节点计数。`--node X` 单节点自检；退出码 1 = 有漂移并列出全部缺口 | 改一处跑一次测试的往返 |

> 三者均遵循 dead-code-cleanup skill 红线：**默认只读/dry-run，删除动作必须显式 `--apply`**。原稿已归档 `attic/tools_archive/_2026-08-28_*`。

## MCP 体检

| 工具 | 用途 |
|---|---|
| `mcp_ping.py` | MCP 服务连通性 + 调用时长测试：对 `.mcp.json` 全部服务做 stdio 握手（initialize/tools/list）+ 只读探针真实调用计时（wq-brain-http 3 个平台只读探针 / wqb-db 4 个 DB 查询）。`--service X` 单服务、`--full` 附全工具注册清单、`--timeout N` 握手超时。退出码 0=全过 / 1=有失败。零配额消耗（探针全部无副作用） |
| `start_wq_mcp.py` | 启动/确保 `wq-brain-http` MCP 服务在 8876 可用（防"论坛工具找不到"） | `--check` / `--wait N` | — |

## 纪律（AGENTS.md §9）

1. **禁止新建** `_gate_*` / `check_*batch*` / `probe_*sa*` / `_submit_*` / `track_*_super*` 类一次性脚本；先用本索引查工具。
2. 缺参/缺能力 → 改对应工具加参数（保持 `--help` 自文档），不写新脚本。
3. 一次性排障探针仍可写 `tracking/_scratch/`，但完成即归档 `attic/`，不留在活跃目录。

## 相关参考

- 战例权威实现：`~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/`（`WQ_TOOLKIT_DIR`）
- 平台 API 封装：`world-quant-brain-mcp/brain_api.py`（`BrainApiClient`，自带 429 退避/Redis 缓存）
