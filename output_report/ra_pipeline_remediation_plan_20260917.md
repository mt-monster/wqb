# RA 九步流水线改进方案（2026-09-17）

> 依据：`ra_pipeline_stage_audit_20260916.md`（v2 全量）、`_v3.md`（增量 + §12 schema 漂移）
> 新增实证：本轮对 `campaign` 节点三道闸做了**直接调用实测**（`logs/_tmp_gate_probe.py`，纯只读），推翻/修正了 3 条既有结论
> 状态：**批 1（P0）· 批 2（P1）· 批 3（P2）· 批 4（P3）全部已落地**（除下述两处上抛项）
>
> 落地校验（全批 DoD，实测）：`pytest tests/ -q` → **1058 passed**；
> `world-quant-brain-mcp` 包 → **82 passed**；`tools/sync_skills.py --check` → 4 个安装位全 OK；
> `logs/_tmp_gate_probe.py` 三闸实测通过；`logs/_tmp_ra_pipeline_dryrun.py`（JPN/IND）无异常。
>
> ⚠ **一处需用户决策**（已在正文标注，非本方案遗漏）：
> **#1 体检包批量生成**受数据源阻塞（本地 WebData 快照不含 JPN/DEU 白名单数据集，见 §2.5）。
>
> ✅ **#5 step-metrics 已终评并于 2026-09-17 整体下线**：结论 = **不接入 S6 各步写入**（收益为负，五条实测理由见批 3 表）。
> 处置 = **连带归档整个子系统**（用户 2026-09-17 确认）：
> - **DB**：五张表已 `DROP`（23→**18** 张）；删除前核实「全 0 行 / 无触发器 / 无外键 / 视图 `v_alpha_metrics` 不引用」，并做了文件级备份 `data/wqb.db.bak_dropstepmetrics_*`。
> - **归档** `attic/step_metrics_20260917/`（10 个文件 = 8 个原文件 + README 决策留痕 + `drop_tables.py` 删除记录）。
> - **代码面**：`wqb_db_mcp.py` 移除 **6 个 MCP 工具**（49→**43**）；`registry.py` 解除 `step_metrics` 节点注册（18→**17**）；同步更新 `test_workflow.py` / `test_skill_integrity.py` / `world-quant-brain-mcp/tests/test_tools_workflow_unit.py` / `INDEX.md` / `docs/skills_pipeline_optimization.md`。
> - **替代方案**：`tools/step_funnel.py`（只读推导，已接线步 9）。
> - **顺手修掉一个护栏缺口**：`test_docs_consistency.py` 里节点数此前是 `assert "**18 个**" in idx`（裸子串断言，节点增删时 INDEX 不改也照样通过）→ 改为**从 registry 实算**并与 INDEX 对齐（与同函数里 wqb-db 计数的守护方式一致）。

---

## 0. 前置修正：本轮实测推翻的 3 条既有结论

> 三处修正的共同效果：把"新建机制"降级为"接好已有机制"，**实施成本显著下降、优先级重排**。

| # | 既有结论（v2/v3） | 实测结果 | 修正后的问题定义 |
|---|---|---|---|
| A | "积压断链**无前置闸**"（v2 最严重项）／"背压未落，建议 GEM 加 `--max-pending`"（v3 #3） | **闸已存在**：`campaign.py:948 _run_backlog_gate`，`BACKLOG_GATE_DEFAULTS.enabled=True`，已挂 S2(`:295`)/S3(`:355`)，dry-run 也走。实测拦截 JPN（`conversion=0.0%<10%`）、EUR、IND、USA | 问题不是"没有闸"，而是 **① 执行路径绕过闸**（JPN 今日 1,640 gem/0 回测却从未被判）+ **② 计数口径漏 `gem` 状态** |
| B | "探针波 verdict 空壳"＝记录卫生问题（#13，P1） | `campaign.py:1130` 规则 B 为 `all(v == "FAIL")`；`verdict=None` → `str(None or "")=""` → **恒 False** | 空壳 verdict 会**静默关闭停止闸规则 B** → #13 由"记录卫生"升为**安全闸失效**，P0 |
| C | "#4 PARTIAL 语义错位" 与 "#13 空壳" 为两个独立问题 | 两者都作用于同一行 `all(v=="FAIL")`，**同一根因** | 合并为**停止闸输入完整性**一个修复包 |

**另一项副产品**：DEU 当前**通过**积压闸（conversion 10.3% ≥ 10%、pending+gated 6.6% < 30%），但其 `gem` 存量 **1,198 条（占该区表达式 72%）**从未被计数 —— 这是"漏计 `gem`"导致**假通过**的现成例证，可作为口径修正的验收样本。

---

## 1. 根因归类（6 类）

| 根因 | 说明 | 关联建议 |
|---|---|---|
| R1 执行路径绕过闸 | 闸挂在 workflow 节点，实际操作可能直调 toolkit 脚本 → 闸不触发 | #15（新） |
| R2 计数口径缺口 | `gem`/`selected` 未纳入积压比；只算 `pending`+`gated` | #3（改写） |
| R3 闸输入不完整 | `verdict` 空壳 + `PARTIAL` 语义 → 规则 B 失效 | #4 + #13（合并） |
| R4 ledger 契约漂移 | `s0_whitelist` 5 种 schema × 3 消费者假设，全线 fail-open | #14, #12, #9 |
| R5 开区清单缺项 | 体检包生成不在开区硬前置清单 | #1 |
| R6 文档/口径漂移 | D3 加法配比、signal_floor fail-open 语义、check_batch 双轨、feature_engineering 措辞 | #2, #8, #10, #11 |

---

## 2. 分四批实施

### 批 1 · P0（根因 R1/R2/R3/R4 主干）

#### P0-1 闸的路径覆盖（R1）— 新建议 #15
- **证据**：`_run_backlog_gate("JPN")` 实测 `success=False`（拦截），但 JPN 今日照常跑完整波 → 该波未经过 `campaign` 节点 S2/S3。
- **待办前置**：先查清 JPN 今日波的**实际执行入口**（`logs/` 与 ledger 可回溯），确认是 toolkit 直调还是 override 后删除。
- **改法（推荐 a）**：
  - a) 把 `signal_floor / stop_rules / backlog` 三道闸**下沉到开波唯一入口**：`Claude/skills/wq-brain-campaign-toolkit/scripts/build_wave.py` 与 `tools/wave_gate.py` 的 `main()`，使"绕过成本 > 遵守成本"；
  - b) 或在 `pipeline.py run`（S3 实跑入口）加同一组闸作第二道保险。
- **验收**：对超阈区直调 `build_wave.py` → 必须被拒（rc≠0 + 明确 error 文案）。
- **风险**：闸下沉会命中大量现存区 → 见 §4 灰度策略。

#### P0-2 背压计数口径（R2）— 改写原 #3
- **改动位置**：`src/wqb/workflow/nodes/campaign.py:1004-1010`（SQL）+ `:940 BACKLOG_GATE_DEFAULTS` + `:953-966` docstring。
- **改法**：新增 `unconsumed = gem + selected + pending + gated` 口径与 `unconsumed_ratio_max`（默认 0.30），与现有 `pending_gated_ratio_max` 并存（保留向后兼容）。
- **验收**：
  - JPN：`1688/1784 = 94.6%` → 拦截（现已被 conversion 拦住，但路径不同）
  - **DEU：`(1198+0+43+66)/1658 = 78.8%` → 拦截（当前放行 ← 本项的直接证据）**
  - 回归：`tests/unit/test_workflow_nodes.py` 相关闸断言同步更新。
- **风险**：与 P0-1 叠加后，**在库五区（JPN/EUR/IND/USA/DEU）将全部命中** → 必须先做灰度决策。

#### P0-3 停止闸输入完整性（R3）— 合并原 #4 + #13
- **改动位置**：`campaign.py:1114-1131`（规则 B 取数与判定）+ `upsert_wave_result` 写入侧校验。
- **改法**：
  1. 归一 verdict 空间：`FAIL` 与"0 达标的 `PARTIAL`"同判 fail-equivalent；
  2. **波关闭必须带 verdict**：`status='closed'` 且 `verdict` 为空 → 拒绝写入，或自动落 `verdict='FAIL'` + `key_findings=['probe/全灭波，0 存活']`；
  3. 规则 B 遇空 verdict 视为**不满足**并输出 WARN（绝不把"没写"当"通过"）。
- **验收（单测三例）**：`(FAIL,FAIL,FAIL)`→拦截；`(FAIL,PARTIAL(0达标),FAIL)`→拦截；`(FAIL,"",FAIL)`→不拦截但输出 WARN。
- **回填**：JPN `wave1`（`closed` + `verdict=None`）补写 `FAIL` + 探针说明。

#### P0-4 ledger 契约统一（R4）— 原 #14（详见 v3 §12）
- **改动**：① 契约定为顶层 `universe`/`delay` + `datasets[]`（对齐 `s0_ranking` 的稳定风格）；② 迁移脚本 `tools/normalize_ledger_whitelist.py`（**幂等 + 原值存 `_legacy` + 断点续跑**）；③ 三消费者（`campaign_intel.py:124,129`、`score_datasets.py::_check_universe_consistency`、`campaign.py:1293`）改 **fail-closed 打 WARN**；④ 修 GBR 双重序列化；⑤ 删/修 `campaign.py:1293` 的 `filter_criteria` 死读取路径（全区域 `LIKE '%filter_criteria%'` 返回空）。
- **验收**：新增 `tests/unit/test_ledger_whitelist_schema.py` —— 遍历全区域断言 schema 唯一（DB 缺失时 skip）。
- **风险**：DEU `candidates[].override` 承载审计信息 → 迁移须映射到 `datasets[].override`，**改前先 `rg` 全仓消费者清单确认无遗漏**。

---

### 批 2 · P1（根因 R5/R6 主干 + 闸语义）

| 项 | 改动位置 | 改法与验收 |
|---|---|---|
| **#1 体检包补齐**（三连复发） | `tools/gen_field_inspect_packs.py`（**已存在**，支持 `--all/--dry-run`）；`SKILL.md` 步 2；`src/wqb/workflow/nodes/wave_gate.py:159` | ① 对 JPN 12 集 + DEU 白名单批量生成（**分批 + 429 退避**）；② SOP 步 2 把"体检包"列为开区硬前置；③ `:159` 的 warning 升为**可选 fail-closed**。验收：JPN 白名单 12 集 `enforced:true`，dry-run 步 5 显示"生效" |
| **#8 signal_floor fail-closed** | `campaign.py:1167/1179-1181` | 缺配置 → 先回落 profile/region 默认；仍缺 → WARN + 保守 floor（不静默放行）。⚠ **这是语义契约变更**：`tests/unit/test_docs_consistency.py:95` 现断言"静默放行"，须同步改 contract 文档 + 测试 |
| **#2 D3 决策表改写** | `references/decision-table.md` L47 | 删加法配比方子（`add(0.40*慢MODEL, 0.60*快PV)`），统一为结构交互口径，与步 7"禁一切加权混合"一致 |

**批 2 实施记录（2026-09-17）**

| 项 | 状态 | 实际落地 |
|---|---|---|
| #8 | ✅ 完成 | `campaign.py` 三道闸默认值 + `_run_signal_floor_gate` fail-closed（缺配置回落默认，仍缺则 WARN + 保守 floor，不再静默）；`resolve_db_path()` 替换硬编码路径（修 test 隔离）；8 区 `thresholds.json` `_doc` + toolkit contract + `test_docs_consistency.py` 同步 |
| #2 | ✅ 完成（**超范围**） | 不止 L47：D3 删配比方子并新增「组合形态铁律 / 允许的 5 类结构交互 / 已废止参数」三行；同文件 D2 L37（CW 失败→线性混合）、D6 L94（CW 规避方子）、D11 L147/157（历史配方与「已验证骨架」）一并改写。**跨 skill 另修 2 处**：`brain-how-to-pass-alpha-test`（CW 表 3 行加权混合方子）、`ppa-mining-experience`（GBR 成功案例 vRNk56mz）。`src/wqb/config.py` 的 `slow_fast_mix` 标注 `deprecated_20260913_route_a`（零代码消费者，仅存史），`test_config.py` 加断言 |
| #1 | ⚠ **部分完成 · 生成受阻** | ②（SOP 开区硬前置）✅、③（fail-closed）✅ 已落地并实测；①（批量生成）**受数据源阻塞** —— 见 §4 |

**#2 的实测依据（探针 `logs/_tmp_gate_mix_probe.py`，零成本）**：直接调 `gate.py::check_one`，7 种加权混合写法（星号中缀 / 加号中缀 / func 权重在前 / func 权重在后 / 等权 / 旧 D6 方子 / 旧 GBR 案例形）**全部命中闸5 block**，7 种结构交互写法**全部 PASS**。即：旧决策表会让 Agent 产出**必被闸5拒绝**的整批表达式（不是"风格建议"，是硬拦截）。

### 批 3 · P2（口径与空转清理）— **已落地**

> 实施中实测出 **3 处原判断需修正**（下表标 ⚠）。共同倾向：问题比原描述**更轻或更重但不同**，
> 因此 3 项的处置都偏离了原计划字面（详见各行）。

| 项 | 状态 | 实际落地与修正 |
|---|---|---|
| **#5 step_efficiency_metrics** | ⚠ **改为"标注"未删** → **2026-09-17 追加终评：不接入** | **原判断有误**：并非"无人消费"。实测 ① 该表确为 **0 行**，但 ② `step_quality_metrics` / `step_gain_metrics` **也全是 0 行**（整个 step-metrics 子系统从未被调用）；③ 它不是死代码 —— `step_metrics` **已在 `registry.py:286` 注册为 workflow 节点**，并经 `wqb_db_mcp.py:2090` 暴露为 MCP 工具 `workflow_step_metrics`，另有 `INDEX.md` / `docs/skills_pipeline_optimization.md` 文档。→ **按「无消费者」删除会误删一个已注册、已暴露、已文档化的能力**。<br>**★ 终评（是否接入 S6 各步写入）= 不接入，收益为负**：<br>① 唯一自动入口 `tools/step_metrics_collector.py::collect_from_checkpoint()` 是 **TODO 空壳**（恒返回空 dict）→ 无任何自动数据源，唯一填充方式是**调用方自己编数**；<br>② 9 个质量指标**全部可从既有表实时推导**（`expressions`/`gate_results`/`backtest_results`/`wave_results`+ledger）→ 写进新表 = **重复存储、双真相源**（本项目已多次被多源漂移咬过）；<br>③ 6 个增益指标（`avoided_backtests`/`saved_time`/`saved_tokens`/`saved_api_calls`/`reduced_invalid_simulations`/`avoided_submits`）是**反事实估算、无客观来源** → 写入即制造不可验证数字，与「报数前必须核实」「禁止推测记账」纪律冲突；<br>④ `token_count`/`api_calls` 在 MCP 层同样无源；<br>⑤ `campaign_summary` 表与被**所有战役提示词**引用的 `get_campaign_summary` 工具**同名但无关**（后者读 `wave_results`）→ 表里有数据更误导。<br>**→ 替代方案（已落地）**：`tools/step_funnel.py` —— 把同一视图做成**只读推导**（单一事实源、不落新表），并在步 9 复盘入口接线。实测即刻产出真结论：KOR 瓶颈 = S3 回测→过廉价闸（3.99%）；USA = 过廉价闸→就绪（0/3）；**JPN = 268 条过闸但 0 条回测**（S3 断链）。<br>**→ 已标注**：子系统已**整体归档**（`attic/step_metrics_20260917/`，含 README 与复活前提）；`tests/unit/test_step_funnel_p5.py` 含守卫用例（归档文件齐备、原位无残留、5 表已 DROP、节点已注销；若将来真实现了自动采集会提醒重审结论）。 |
| **#6 DEU 波号归一** | ✅ 完成（**危害表述已推翻**） | **原判断有误**：审计称"时间戳波号致 floor 统计 0 样本 → floor 恒 0.5"。实测 ① 污染**确实存在但只在 `expressions` 表**：20 行 / 全部 DEU / 全 `analyst93` / `status=gated` / 5 个时间戳（2026-09-13 同一分钟，各 4 条）；**其他 6 区为 0**。② floor 闸读 `backtest_results.wave`（无污染），实测 `batches=2 / max_sh=1.7 / verdict=ok` → **闸工作正常**。③ `thresholds.json` 里 DEU `_evidence` 的"样本 0 波"指的是**回填 p25 需 ≥8 波的样本门槛**，非闸失效。→ 按"口径卫生"处置：新增 `src/wqb/wave_id.py`（形态契约）+ 写入侧护栏（`mcp_batch_writer.py` 两处）+ 迁移 `tools/normalize_wave_ids.py`（已执行：20 行归一 `unlabeled_<ds>_<ts>`，DB 已备份，幂等复核 0 残留） |
| **#7 步 2 三次 calibrate** | ✅ 完成（**"无增量"表述部分推翻**） | **原判断部分有误**：实测 `cmd_calibrate` **只写 thresholds.json、不产出排名**，排名由 `cmd_score` 产出 → **第 3 次调用是必需步，不是冗余**。故未删第 3 步，改为澄清「2 步必需 + 1 步可选」：把 `dry_run=true` 的预览降级为**可选**（仅新区/校准可疑时做），并写明为何第 3 步不能删（防止后人误删） |
| **#10 check_batch 口径收敛** | ✅ 完成（**实为三口径**） | 实测不止双口径：① 正文散文列 5 条判据（含 dual-field + 13 范式）；② `wqb.expression.validator.check_batch` 只实现 **4** 条形状闸且**全仓零调用方**；③ 唯一可执行的是 toolkit `gate.py:check_batch_diversity`（自学习契约 + exposure 多样性 + 家族天花板）。→ 收敛为**单一权威**（可执行闸），validator 降级为"方法论参考"，删除末尾双口径注 |
| **#12 文档口径微修** | ✅ 完成（**发现一个真 bug**） | ① **priors 键**：不止大小写不一致 —— 实测 6 区（CHN/DEU/EUR/GBR/IND/USA）**同时存在大小写两键且 payload 不同**：大写是 campaign 节点的 **cache marker**（~2033 B），小写是 `assemble_priors.py` 的**真实 payload**（2.5–7 KB）。消费侧读小写故数据无误，但**按大写查会拿到不含 `wins` 的缓存标记** → 已把 cache key 独立命名为 `assemble_priors_cache_<REGION>`（读写两侧同步），并迁移 6 个存量键（已执行 + 备份）。② **signal_floor 权威位置**已在正文写明；③ 顺带修正过期数字：**13/13** 区已配（AMR ASI CHN DEU EUR GBR GLB HKG IND JPN KOR MEA USA），旧文档记「11 区」漏计 AMR/GLB |


### 批 4 · P3 — **已落地**

| 项 | 状态 | 实际落地与修正 |
|---|---|---|
| **#9 s0_ranking 补建** | ✅ 改为「显式化 + 给命令」 | **实测修正**：并非只有 IND 缺 —— 10 区有**非空** `ranking[]`（ASI CHN DEU EUR GBR GLB HKG JPN KOR USA，35–294 条），`IND`/`AMR` **完全没有该行**。（附注：审计所称「10 个有记录的区域」**正确**；本轮早前一次探针因读错子键（读 `datasets` 而非 `ranking`）一度误判为"JPN/DEU 空排名"，已纠正。）补建需跑 S0 打分（**平台只读调用**），未擅自执行；改为消除 fail-open —— `tools/campaign_intel.py s0-select` 原先 `rk.get("ranking") or []` 让"排名缺失"与"无 tier"不可区分，现**显式 WARN** 并给出补建命令 |
| **#11 feature_engineering 收口** | ✅ 完成 | 步 3 正文由「字段理解用 `workflow_feature_engineering`」改为**「按需 / 仅人读参考 / 禁注入 GEM」**，并补一段说明**为什么**：该节点产出是确定性模板渲染（8 问框架 + `rank(ts_mean({f},66))`），注入 GEM 会让 GEM 一行 LLM 都不调、整波退化为模板展开（GBR `intraday_pv_feats` 实证） |
| **judge 精简** | ✅ 完成（**发现并修一个 fail-open**） | 由"三态"改为**三态 + 逐闸清单**（附加字段，保契约）：新增 `checklist`（事实清单）与 `degraded_gates` + `warning`。**根因**：`_compute_final_verdict` 只对 `platform_check`/`correlation` 的 `pass=False` 判 BLOCK，而降级闸多返回 `pass=True, unavailable=True` → **全部闸取不到数时仍输出 `verdict=READY` 且旧返回体看不出缺闸**（已实测复现）。`checklist`/`degraded_gates` 已一并落台账，`workflow_judge` 工具与 ra-pipeline 正文同步 |

**批 4 附带修复（不在原计划内，实测发现）**：`world-quant-brain-mcp/tests/test_tools_workflow_unit.py::test_workflow_list_nodes_shape`
硬编码 `count == 11`，而 `registry.py` 工作区已有 **188 行**节点注册增量（属前序会话未提交工作，非本次引入）→ 实际 **18** 个节点。
该断言已改为显式列举 18 个节点名（既不放过漂移，也不因新增节点而假红）。

---

## 2.5 批 2 阻塞项：体检包数据源边界（2026-09-17 实测）

> 原 #1 的验收标准写的是「JPN 白名单 12 集 `enforced:true`」。实测发现**该目标无法由本地数据达成**，
> 原因是数据源不是流程问题。以下为实测数据，供决策（补数据包 / 换区域 / 接受降级）。

**① 生成是纯离线的，无 429 风险**（推翻原计划的「分批 + 429 退避」）：

`tools/gen_field_inspect_packs.py` 只读本地 `research-data/WebData_20260219_V0.10.9.zip`（36.9 MB）
+ 调 `tools/webdata_quality.py --export-expr`，**不发任何平台请求、不耗配额**。原计划担心的限流不存在。

**② 但本地快照的区域/数据集覆盖严重落后于本期选集**：

| 维度 | 实测值 |
|---|---|
| 快照覆盖区域 | 仅 **ASI / CHN / EUR / GLB / JPN / KOR / USA** 七区（9 个 `region×delay` 组合） |
| 快照数据集条目 | 160 条，去重后 **125 个数据集名** |
| **DEU** | 快照内 **0 条目**（该区根本没有） |
| JPN 白名单 12 集 | 落在快照内 **0 集** |
| DEU 白名单 9 集 | 落在快照内 **0 集**（`model26`/`model109` 存在但仅在**其他区域**下） |
| KOR 白名单 20 集 | 落在快照内 **0 集**（KOR 快照只有归 `analyst25`，而该集不在白名单） |

**结论**：JPN / DEU / KOR 等本期活跃战役的选集（`news_sentiment_nlp`、`model307`、`insider_matrix`、
`other545`、`price_signal_dl` …）**全部晚于该 2026-02-19 快照**，因此这些区域的体检包
**无法在本地生成**。当前 320 个体检包的分布（HKG 172 / USA 104 / EUR 19 / CHN 11 / GLB 6 / ASI 5 /
JPN 2 / KOR 1）也印证：覆盖集中在快照内的老区域。

**三条可选出路**（需用户决策）：

| 选项 | 做法 | 代价 |
|---|---|---|
| a. 补数据源（推荐） | 用 WebDataScope 浏览器扩展对 JPN/DEU 重新导出数据包 → 放入 `research-data/` → 重跑 `gen_field_inspect_packs.py` | 需人工操作扩展；一次性 |
| b. 接受降级 | 这些区域显式 `--inspect-mode warn` 跑，并在 ledger 记「无体检包」原因 | 预处理约束仍无把关（现状），但**不再静默** |
| c. 收紧到有包的区 | 开新战役优先选快照内区域（USA/EUR/HKG…） | 与点塔/配额策略冲突 |

**③ 另发现两项附属缺口**（同属"开区前置未落"）：

- `tracking/JPN/` 与 `tracking/DEU/` **都没有 `catalog/`（`scan_fields.py` 产物）** ——
  `gate.py` 因此直接 `FileNotFoundError` 退出（实测 JPN/`news_sentiment_nlp`）。
  这是**比体检包更靠前**的断点：连白名单闸都跑不起来。建议纳入批 3。
- `src/wqb/workflow/_common._skill_roots()` 解析顺序实测为
  `~/.claude/skills` > `~/.codex/skills` > `~/.qoder-cn/skills` > `~/.cursor/skills` > `~/.workbuddy/skills`
  > 仓库 `Claude/skills` —— **仓库副本优先级最低**。故任何 skill 改动必须 `tools/sync_skills.py` 才生效，
  否则运行时会继续读旧副本（本轮实测 `gate.py` 被从 `.qoder-cn` 加载即为此故）。

---

## 3. 验收标准（每批 DoD）— **全项复验通过**

| 检查项 | 命令 | 期望 | **实测结果（2026-09-17）** |
|---|---|---|---|
| 单测全绿 | `pytest tests/ -q` | 全通过 | ✅ **1109 passed / 9 skipped**（含本次新增 6 个测试文件） |
| MCP 包单测 | `world-quant-brain-mcp/.venv/Scripts/python -m pytest tests/ -q` | 全通过 | ✅ **82 passed**（含更新后的 18 节点断言） |
| skill 多目标同步 | `python tools/sync_skills.py --check` | 无漂移 | ✅ claude / codex / cursor / workbuddy 四安装位全 OK |
| 演练回归 | `DRY_REGION=JPN\|IND python logs/_tmp_ra_pipeline_dryrun.py` | 输出与预期一致 | ✅ 两区跑通；步 8 价值判定行已更新为"P3 已落地" |
| 闸实测 | `python logs/_tmp_gate_probe.py` | DEU 假通过消除 | ✅ `unconsumed_enforce: False`（灰度）+ USA 弹出"[灰度·未拦截] 未消费积压=3197/3549（90%）"；DEU signal_floor `batches=2 / max_sh=1.7 / ok` |
| 加权混合实测 | `python logs/_tmp_gate_mix_probe.py` | 文档与闸一致 | ✅ 7 种加权混合写法**全被闸5 block**、7 种结构交互**全 PASS** |
| 干跑契约 | `workflow_campaign(stage="S2", dry_run=True)` | 不 subprocess、不写库 | ✅ wave_gate 节点 4 档 `inspect_mode` 干跑均 `success=True` 且过 argv 契约校验 |

---

## 3.5 本轮新增/修改文件清单

**新增（10）**

| 文件 | 用途 |
|---|---|
| `src/wqb/wave_id.py` | 波号形态契约（`is_timestamp_wave` / `normalize_wave_id` / `wave_kind`） |
| `tools/normalize_wave_ids.py` | 裸时间戳波号回填（dry-run 默认 + 备份 + 幂等，**已执行 20 行**） |
| `tools/migrate_priors_cache_key.py` | priors 撞键改名（**已执行 6 键**） |
| `tests/unit/test_inspect_mode_failclosed_p1p1.py` | 体检硬门缺包策略（8 用例） |
| `tests/unit/test_wave_id_contract_p2p6.py` | 波号契约（19 用例） |
| `tests/unit/test_priors_cache_key_p2p12.py` | priors 键不撞名（6 用例） |
| `tests/unit/test_judge_checklist_p3.py` | judge 清单 + degraded 闸（10 用例） |
| `logs/_tmp_gate_mix_probe.py` | 闸5 加权混合实测探针（只读） |
| `tools/step_funnel.py` | 步级漏斗 S2→S6 只读推导（替代空转的五张 step_* 表） |
| `tests/unit/test_step_funnel_p5.py` | 漏斗口径 + 只读性守卫（12 用例；含"若采集器真被实现则提醒重审"） |
| `tests/unit/test_campaign_prompt_commands_p4.py` | 战役提示词 CLI 命令契约护栏（39 用例，两层校验） |
| `output_report/ra_pipeline_remediation_plan_20260917.md` | 本方案（含全部落地记录） |

**修改（主要）**：`tools/wave_gate.py`（`--inspect-mode` + fail-closed）、`src/wqb/workflow/nodes/wave_gate.py`（透传 + `inspect_status` 自报）、`src/wqb/workflow/registry.py`（`inspect_mode` 入 `optional_params`）、`src/wqb/workflow/nodes/campaign.py`（priors cache key 改名）、`src/wqb/workflow/nodes/judge.py`（`build_checklist`）、`tools/mcp_batch_writer.py`（写入侧波号护栏）、`tools/campaign_intel.py`（缺 ranking 显式 WARN）、`src/wqb/config.py`（`slow_fast_mix` 标 deprecated）、`tests/unit/test_config.py`、`tests/unit/test_docs_consistency.py`、`Claude/skills/wq-brain-ra-pipeline/{SKILL.md,references/decision-table.md,references/ppa-mining-experience.md,references/ra-campaign-prompt.md}`、`Claude/skills/brain-how-to-pass-alpha-test/SKILL.md`、`world-quant-brain-mcp/tests/test_tools_workflow_unit.py`

**数据变更（均已备份，可回滚）**：`data/wqb.db` → `.bak_waveid_20260917_005411`（20 行波号）、`.bak_priorskey_20260917_005549`（6 个 ledger key）；另 `.bak_prewhitelist_20260917_004128`（P0-4 白名单迁移）

---

## 4. 风险与灰度策略（须先决策）

**核心风险**：P0-1 + P0-2 一旦生效，实测**在库五区全部命中**（JPN/EUR/IND/USA/DEU）→ 等价于**全池停摆**。这不是 bug，是"积压确实已超限"的真实反映，但会立即阻断当前挖掘节奏。

**建议两阶段灰度**（避免一刀切）：

| 阶段 | 时长 | 行为 |
|---|---|---|
| 阶段 1：观察 | 3 天 | 新口径只 **WARN 计数**（不拦截），产出"若开闸会拦哪些区"的清单 |
| 阶段 2：执行 | — | 经你确认清单后切 fail-closed；对**明确要继续挖**的区写 `backlog_gate_override`（带 reason + until）留痕放行 |

**回滚**：ledger 迁移存 `_legacy` 原值 + DB 文件级备份；闸逻辑改动可经 `thresholds.json` 的 `enabled=false` 单区关闭。

---

## 5. 工程纪律（贯穿全部批次）

- **skill 改动**：只改 `Claude/skills/` 源 → `python tools/sync_skills.py` 同步全部安装位 → `--check` 守护（`tests/unit/test_audit_fixes.py`）。
- **workflow 节点**：`registry.py` 的 `required_params`/`optional_params` 必须与 `run()` 签名一致（`tests/unit/test_skill_integrity.py` 守护）。
- **回测/迁移脚本**：**一律带断点续跑 / checkpoint**（硬性约定），写 `logs/_tmp_*.py` 或 `tools/`。
- **提交前**：`pytest tests/ -x` + 硬编码密钥扫描（pre-commit）。
- **MCP**：服务器命名固定 `wq-brain-http` / `wqb-db`；改 MCP 后需重启会话。

---

## 6. 建议执行顺序

```
批1 (P0) ──► 批2 (P1) ──► 批3 (P2) ──► 批4 (P3)
  │
  ├─ P0-3 / P0-4 可先行（局部、低风险、无全池影响）
  ├─ P0-1 / P0-2 须等灰度决策（影响全池）
  └─ 批2 的 #1 体检包与批1 独立，可并行
```

**若只做一件事**：做 P0-3（停止闸输入完整性）—— 成本最低（约 20 行 + 3 个单测），却直接修复"空壳 verdict 静默关闭停止闸"这一**假安全**问题，且无全池停摆风险。

---

*本方案基于 2026-09-17 00:30 `data/wqb.db` 快照与 `campaign.py` 源码实测。闸道实测脚本 `logs/_tmp_gate_probe.py` 全程只读。方案未实施任何改动。*
