# 步 9（S6）复盘回写：原理 / 运行机制评估与优化建议

> 评估日期：2026-10-02 | 方法：全部结论均核对真实代码（`路径:行号`），未采信文档自述
> 评估范围：步 9 = 一波（步 2→步 9）的收尾回写阶段 = S6

---

## 一、原理：它要解决什么问题

步 9 是**九步链的唯一闭环点**。前面 8 步全在往外「花」——生成表达式、过闸、回测、评审、提交；步 9 把这一波的**结论**写回库，让**下一波**的先验自动变新。

核心设计意图（三条）：

1. **让先验变新**：把 verdict / 判死 / 胜绩 / 饱和写进台账，下一次 `assemble-priors` 组装时自动读入 → GEM 生成时就带着「哪些族已经死了、哪些配方有效」。
2. **单一结论源**：一波的结论**只有** `wave_results.verdict` 一个来源（2026-09-28 去重，废止 `s6_verdict_<wave>` 等旧键），避免多写分叉。
3. **失败也要留痕**：判死（`dead_end`）、饱和（`saturated_datasets`）、经验（`dataset_experience/*.md`）都是「负知识」的沉淀，防止下一波重复撞同一面墙。

**完成定义**：`step9-writeback.md §9.7` 的清单**全勾**，缺任何一项 = 本波未完成。

---

## 二、运行机制：有序八步（执行顺序即编号）

| # | 动作 | 调用 | 产物 | 落地位置 |
|---|---|---|---|---|
| ① | 看漏斗（只读） | `tools/step_funnel.py --region $R [--wave $W]` | 瓶颈定位 | `step_funnel.py:117 build_funnel` |
| ② | 判 verdict | §9.3 判定表 | PASS/PARTIAL/FAIL | `wave_results_contract.py:43 normalize_verdict` |
| ③ | 点塔进度 | `campaign_intel.py pyramid` | `[key_findings]` 行 | — |
| ④ | 写波结论 | `upsert_wave_result` | **`wave_results.verdict` = 唯一结论源** | `wave_results_contract.py:139` |
| ⑤ | 判死 / 胜绩 | `seal_dead_end` / `upsert_registry_empirical(win)` | `dead_end` / `win` 层 | `wqb_db_mcp.py:2195` |
| ⑥ | 饱和反馈 | `campaign_intel.py mark-saturated --write-ledger` | ledger `saturated_datasets` | `campaign_intel.py:1211` |
| ⑦ | 逐数据集经验 | `workflow_campaign(S6, dataset-experience)` | `reports/dataset_experience/*.md` | `src/wqb/research/dataset_experience.py` |
| ⑧ | 刷新先验快照 | `workflow_campaign(S2, assemble-priors)` | `priors_snapshot_<region>` | `assemble_priors.py:512` |

### 2.1 三个关键机制的代码实况

**(a) verdict 归一化 + 单一实现**
`normalize_verdict`（`wave_results_contract.py:43-74`）把 `FAIL_xxx：…` / `CLOSED_DEAD_END_…` / `8/8 RED` / `全灭` 等形态归一到三态枚举；无法辨认时返回 `{"error", "suggestion"}` 且**不写库**。
👍 关键优点：写入方（`wave_results_contract`）与读取方（停止规则 B，`campaign.py:22` 导入同一函数）**共用一份实现**，无双真相源。

**(b) 判死取证闸（fail-closed）**
`seal_dead_end` → `_forum_recon_gate`（`wqb_db_mcp.py:2160`）→ `wqb.recon_evidence.verify_evidence`（`recon_evidence.py:166`）：两层判定 =「声明层 `found=false`」+「按 `question_key` 回 ledger 核对，且不能被更新的『有货』记录推翻」。
- 放行**唯一**条件：可靠的「论坛无解」负结果。
- 有货 / 故障（`found=null`）/ 缺失 / 无法核对 → **一律拒绝且不沉降、不写库**。
- 病根记录在案：2026-09-29 实证 5 条 recon 记录里 **2 条是工具故障**，被记成 `found=false` → 「工具坏了 ≡ 论坛无解」→ 误把活路判死。现在的设计正是为堵这个洞。
- 绕过只有 `force_seal=True` / `require_forum_recon=False` 两条，**都要人工确认、都留痕**。
👍 这是本阶段设计质量最高的部分：单一实现（`recon_evidence.py` 被写入方 / 节点 / 判死闸 / 统计方共用）、失败模式有真实事故背书。

**(c) 饱和反馈的「先预览后落库」**
`mark-saturated` 缺省**只打印 dry-run**，必须显式 `--write-ledger` 才写 `saturated_datasets`（`campaign_intel.py:1236-1242`）。消费方已接线：S0 打分 `apply_saturation_demotion` / P5 拍平读它（`config.py:71-74`），`profile_drift.dead_dataset_index` 也读（`profile_drift.py:139`）。
⚠ 历史坑：旧文档教写 `submit_ready_blocked`，但 **S0 从未读过那个键**，只有 `step_funnel` 计数 → 反馈实际断链。2026-09-29（RA-113 / IX-20）才补上正确入口。

### 2.2 漏洞：两个「证据质量」问题（P1）

**问题 A：verdict 的 `suggestion` 不读近池，是纯文本启发式**
- `suggest_verdict(verdict)`（`wave_results_contract.py:93-120`）**签名只有一个字符串参数**，没有 `conn` / near 池 / candidates。
- 判定表语义是「PARTIAL = 0 达标但 **≥1 条进 near 池**」，但 suggestion 只靠文本命中 `NEAR|YELLOW|近闸|基线|突破|黄灯` 才推 PARTIAL → **是启发式而非证据**。
- 佐证：同文件里的**证据版**函数 `verdict_from_counts(n_pass, n_near)`（`:84`）**在全仓库零调用方**（已 grep 确认）。
- 影响面：写入路径（upsert）靠文本猜；**但** `pipeline --review` 自动路径 `auto_upsert_from_review`（`_lib/wave_results.py:216`）**用真实计数**推 verdict（`n_cand>0 → PASS / n_near>0 → PARTIAL / else FAIL`，`:278-284`）——即自动路径是证据驱动的，只有「手写自由文本被拒后拿 suggestion」这条兜底路径是启发式。**风险等级：中（有自动路径兜底，但文档没写清两条路径的证据质量差异）。**

**问题 B：方案 B（step_events）的 S6 埋点空缺**
`step_events` 封闭词表 12 类（`step_events.py:33-46`），但**实际埋点只有 3 处**（`campaign.py:237` cache_hit、`judge.py:142` mode_b_blocked、`batch_track.py:464` batch_error_cascade/cancelled）；**9 类无任何写入方**。
与步 9 直接相关：
- `region_kb_refreshed`（第 ⑧ 步的 S6 指标，`step_eval.py:426-430`）**无写入方** → S6 的 gain 指标恒为 `n/a`。
- `seal_dead_end`（第 ⑤ 步，docstring 自述「S6 判死标准动作」）**无 `salvage_collected` 埋点**。
**风险等级：中**——方案 B 是 2026-09-30 新增的**旁路观察面**，不影响回写正确性，但「S6 步级评估」目前只有 T1 只读推导可用（`verdict_nonempty_rate` / `wave_span_days` 依赖 `wave_results.verdict` 非空），事件面是空的。

### 2.3 漏洞：三个「执行强度」问题

**问题 C：完成定义清单无机器校验（P1，最大结构风险）**
`§9.7` 六项清单（含 ⑥⑦⑧）**没有任何代码强制**。已 grep `src/wqb/workflow/nodes/` + `tools/`：无 step9 完成度校验节点。
- 唯一软约束：GEM 对 stale 快照**只 WARN 不阻断**（`gem.py:135-193` `_priors_snapshot_freshness`，`:489-492` 只 append 进 `warnings`）。
- 这与文档自述「MUST BE done by step 9」不匹配：**漏做 ⑥⑦⑧ 不报错**，只是下一波带着旧先验跑。
- 有真实事故证据：`§9.7` 第⑥项记录 GBR 实测「快照停在 09-19，而 `region_kb` 已 09-25、`registry_empirical` 已 09-26 → 落后 8 天，本波结论不回流」——**这正是无校验的后果**。

**问题 D：dataset-experience 文件名拼写固化错误（P3）**
写手 `src/wqb/research/dataset_experience.py:223` 生成 `f'{region.lower()}_{ds}_campain.md'`——**`campain` 少一个 g**。已固化进 **8 个现有产物** + 路由测试断言（`test_dataset_experience.py:88/109`）。属历史技术债，改名成本 > 收益，建议文档标注即可。

**问题 E：`_recent_closed_waves` 缺独立回归测试（P2）**
停止规则 B 的窗口选取（`campaign.py:1401` `_recent_closed_waves`）有一个高危修正：2026-09-27 R22 前按 `COALESCE(updated_at, created_at)` 排序，**给旧波补记结论会把旧波顶进「最近 3 波」窗口**（KOR 91c 事故 → 区域停波被错误解除）。现改为按波的**开始时刻**（`waves.created_at`）。
→ 这个修正价值极高，但**未发现专门的回归测试文件**（仅可能被 `test_stop_rules_axis_scope.py` / `test_p0_fixes_20260927.py` 间接覆盖）。

---

## 三、结论：是否需要优化

**总评：设计层成熟、执行层有缺口。** 步 9 的「做什么」（单一结论源 / fail-closed 取证 / 只读推导）是九步链里设计得最扎实的一段；欠的是**「做了没有」的强制力**与**两处证据/埋点的断链**。

| 优先级 | 问题 | 建议 | 目标文件 | 成本 |
|---|---|---|---|---|
| **P1** | 完成定义无机器校验（问题 C） | 新增只读校验工具 `tools/step9_audit.py --region $R --wave $W`：按 §9.7 六项逐条查（`wave_results` verdict 非空且 closed / key_findings 含点塔行 / dead_end 与 win 存在性 / saturated / 每个回测集的 md 新鲜度 / `priors_snapshot` 时间戳 ≥ 回写时间），输出缺项清单；挂到波收尾（可先 `--enforce warn`） | `tools/step9_audit.py`（新） | 中 |
| **P1** | `suggestion` 证据不实（问题 A） | ①文档写清「自动路径按计数、手写兜底按文本」两条证据质量差异；②让 `suggest_verdict` 可选接收 near 计数（`suggest_verdict(verdict, n_near=None)`），有计数时按判定表判、无计数才退回文本 | `wave_results_contract.py:93` + `step9-writeback.md §9.3` | 低 |
| **P2** | `_recent_closed_waves` 缺回归测试（问题 E） | 补 `test_recent_closed_waves_orders_by_start_time`：造两波，给旧波补记 PASS，断言它**不**进窗口（守护 R22 修正） | `tests/unit/06_wave_pipeline/` | 低 |
| **P2** | 方案 B 的 S6 埋点空缺（问题 B） | 在 `seal_dead_end`（写 `salvage_collected`）与 `assemble-priors` 节点（写 `region_kb_refreshed`）补埋点，让 S6 gain 指标不再恒 `n/a` | `wqb_db_mcp.py` + `campaign.py` | 低 |
| **P3** | `campain` 拼写（问题 D） | 改造成本 > 收益（8 产物 + 测试断言），建议在 `dataset_experience.py` docstring 与 `§9.1 ⑦` 标注「历史拼写，勿改」 | 文档 | 极低 |

**不建议优化的部分**（已验收合格，勿动）：
- verdict 单一实现共用（无双真相源）✅
- 判死取证闸 fail-closed ✅（设计精良，有事故背书）
- `profile_drift` 钩子 fail-open + 幂等 + 限 win/dead_end 两层 ✅
- `dataset-experience` 只读 DB + 保留人工块 + 原子写 + 并发检测（sha256 证零写入）✅
- `mark-saturated` 先预览后落库 + S0 已接线 ✅

**最值得先做的一件事**：P1 的 `step9_audit.py`。理由——问题 A/B/D/E 都是「局部、低风险」；唯独问题 C 是**结构性**：整个步 9 的闭环价值（下一波先验变新）**完全押在 agent 自律上**，而 GBR 的 8 天延迟已证明这条链会静默退化。一个只读校验器能把「本波未完成」从「靠自觉」变成「跑一条命令就知道」。

---

## 四、落地记录（2026-10-02 当日执行完毕）

**结论：5 项缺口（P1×2 / P2×2 / P3×1）全部落地，测试与文档同步完成。**

| 缺口 | 落地物 | 验证 |
|---|---|---|
| **P1-C** 完成定义无机器校验 | 新增 `tools/step9_audit.py`（只读 6 项校验：`wave_row` / `key_findings` / `dead_end_win` / `saturated` / `dataset_experience` / `priors_snapshot`；`--enforce warn\|strict`，硬失败退出码 1） | 新测 `tests/unit/10_toolkit_scripts/test_step9_audit.py` 15 条；实跑 KOR/EUR/IND 正确暴露真实缺口（KOR 快照早于回写 2h、EUR/IND 缺经验文件） |
| **P1-A** `suggest_verdict` 证据不实 | `src/wqb/wave_results_contract.py::suggest_verdict(verdict, n_pass, n_near)` 支持可选计数 → 有计数走 `verdict_from_counts`（`evidence="counts"`/`high`），无计数退回文本（`evidence="text"`）；`upsert_wave_result` 加 `n_pass`/`n_near` 透传；`wqb_db_mcp.py` MCP 工具同步加参 | `test_p1_fixes_20260927.py` 新增 2 条（`test_suggest_verdict_prefers_counts_evidence_over_text` / `test_upsert_passes_counts_to_suggestion`），18 条全绿 |
| **P2-E** `_recent_closed_waves` 缺回归测试 | 新增 `tests/unit/06_wave_pipeline/test_recent_closed_waves_window.py` 6 条，守护 R22（按 `waves.created_at` 排序，补记旧波不进窗口） | 6 条全绿 |
| **P2-B** 方案 B 的 S6 埋点空缺 | `wqb_db_mcp.py::seal_dead_end` 写 `salvage_collected`（仅 `salvaged_count>0`，`dedupe_key=seal_dead_end:<entry_id>`）；`campaign.py::run(assemble-priors)` 成功分支写 `region_kb_refreshed`（`dedupe_key=assemble-priors:<YYYYMMDD>`）。均走 `safe_record_event`（永不抛） | 新测 `tests/unit/06_wave_pipeline/test_s6_events_instrumentation_20261002.py` 7 条全绿（含旁路不阻塞、幂等、0 条不记） |
| **P3-D** `campain` 拼写 | `src/wqb/research/dataset_experience.py` 加注释「历史拼写、稳定契约、勿单点改」；`step9-writeback.md §9.1 ⑦` 同注 | `skill_lint.py` 新增 0；`index_tables.py --check` 一致 |

**附带文档同步**：`step9-writeback.md §9.3`（两档证据质量）/`§9.4`（`n_pass`/`n_near` 入参）/`§9.5`（沉降旁路记账）/`§9.7`（`step9_audit.py` 机检）；`SKILL.md` 步 9 完成定义引用校验器；`references/tool-index.md` 第 9 行；`sync_skills.py` 已同步（9 文件 / 4 安装位）。

**验证汇总**：定向 46 条全绿；相邻目录 338 条全绿；`tests/unit/07_docs_skills/` 782 条全绿；`skill_lint` 新增 0；`index_tables --check` OK。

**未做（有意保留）**：`step9_audit.py` 未强制挂进波收尾节点（当前 `--enforce warn` 手动/CI 调用）——与评估「先 warn 后 strict」的建议一致，待积累若干波的真实误报率后再决定是否升级为阻断。
