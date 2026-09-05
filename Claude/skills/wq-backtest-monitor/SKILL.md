---
last_verified: 2026-08-24
name: wq-backtest-monitor
description: "WorldQuant BRAIN PPA alpha 挖掘任务的\"监控 / 盘点 / 效率分析\"框架。当用户要求 \"盯回测任务 / 看任务情况 / 盘点挖掘任务 / 查历史回测 / 从 python 进程角度分析 / 回测效率如何 / 哪些 alpha 可提交\"等任何监控 WQ 挖掘的场合触发。提供：机器级 Python 进程第一视角枚举与分类、逐任务并发模型+进度、回测效率结论、**逐候选提交核查 (四关审计)**、**在飞任务 ETA 预期完成时间**、提交验证四关层级、并发令牌桶模型、监控盲区分类。"
layer: L6
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
version: "1.1"
agent_created: true
---

## 持久化铁律（DB 单轨）

战役产物只写入 `data/wqb.db`（经 `wqb.store` / `mcp__wqb-db__*`）。**禁止**把 `final_expressions.json` / `alpha_list.json` / `candidates/*.json` / `cache/*batches*.json` / `results/*.csv` 当交接真相源；Agent 禁止 Write 这些文件。静态配置与凭证除外。








# WQ PPA 挖掘 · 监控 / 验证 / 并发 框架

当用户要"盯回测 / 盘点挖掘任务 / 看回测效率 / 评测可提交 alpha"时，按下述框架产出完整分析。

## 衔接协议
- **上游**：S5 落地——`worldquant-submit-alpha`（REGULAR/PPA）与 `wq-brain-superalpha`（SUPER；status=ACTIVE 后纳入 OS 监控）。
- **本 skill 角色**：S6 监控复盘——提交核查四关审计/ETA/判停依据；§14 台账回写形成 S6→S-PRE 闭环。
- **下游**：`wq-brain-campaign-matrix`（S-PRE 查表自动读取最新 dead_ends/wins/campaigns）。

> 日常战役由 pipeline 托管（进程识别与判停见 §13）；「进程枚举/并发模型/效率分析/盲区排查」仅故障排查时执行
> （`Get-CimInstance Win32_Process` 全量枚举为发现入口；SCAN/MINING/MCP-SVC/TRACKER 分类与五类盲区细节已删，需要时查 attic 归档）。

## 5. 提交验证 · 四关层级（PASS_CHEAP ≠ 可提交）

| 关 | 内容 | 本链现状 |
|----|------|----------|
| ① 研究仿真 IS 廉价闸门 | S>1.58/F>1.0/TVR∈[0.05,0.30]/M>10bp/Ret>0.05 + 近闸 | ✅ PASS/PASS_CHEAP 候选 |
| ② 生产仿真 OOS | 样本外稳健 | ❌ 未跑 |
| ③ 生产相关性 PROD_CORRELATION + 自相关 | WQ 真正提交闸门，仅进 `found_alphas` 者记录 prod_corr | ✅ 仅 1 个 `YPgAa3WR`(prod_corr=0.5325) 跨过；其余无 prod_corr 字段=生产关从未验 |
| ④ 平台 submittable + 真实提交 | 平台判定 + 实际落平台 | ❌ 0 个（no_submit=True） |

**结论**：`PASS_CHEAP` = "廉价研究仿真闸门通过"，**不是"可提交"**。报告里这类候选必须标注「研究仿真 IS 闸通过、提交未验证」，不得称"可提交 alpha"。取证函数 `collect_verified_pids()`（取 `found_alphas` 的 pid）。

## 6. 并发模型 · Token-Bucket（C=7，非固定槽位）

- 突发容量 **C≈7**，慢补充 ~1 令牌/20–40s。安全包络：瞬时提交 **≤6** 绝对安全；持续高频需 **≥15–20s** 间隔一个。同账号 ≥8 在 <2s 内齐射必 429。
- 错峰 + 每进程 `submit_gate` 下曾安全跑过 ≤10 路并发零 429。
- 最佳实践：① multi-sim 批量（1 令牌换 8 回测）② 显式 submit_gate（瞬时≤6/批间≥45s/429 退避）③ 429 backoff ④ 禁齐射（同账号并发进程≤6）⑤ 断点续跑 checkpoint。
- 当前真正瓶颈 = **信号发现不是吞吐**（并发批次首步 Sharpe 远低于闸门）。

## 7. 工作纪律（跨项目铁律）

1. 转向时机：每轮验证超 10 种不同结构仍无满意效果才考虑转向。
2. 断点续跑：只把拿到 pid 的确定结果算"已完成"。
3. label 碰撞：用完整字段名，勿截断导致不同字段同名覆盖。
4. universe 合法性：TOP500/1000/2000/3000 合法；TOP800/1500/2500/5000 非法（400 拒）。
5. 提交标准：PASS_CHEAP 候选不得称可提交。
6. 监控第一视角：必须机器级进程枚举为发现入口。

## 8. 产出物分类标准

- 报告 `.md`（report/audit/status/inventory/candidates）= 输出到用户项目目录的 `reports/` 或临时文件。
- 新监控脚本应在 `tools/` 按统一规范新建。
- 用户的 `scan_*.py`、平台 `results/` 数据、基础设施 `*.py` = 不归类、原地保留
- **红线**：绝不动在跑进程的 checkpoint 与脚本（如 v52b 的 checkpoint 与 scan 脚本）

## 10. 提交核查（强制章节，每次汇报不可省略）

每次"盯回测/看进度/盘点"时，必须产出逐候选 Alpha 的提交状态审计：

**核查四关**：
| 关 | 内容 | 取证方式 |
|----|------|----------|
| ① 研究仿真 IS | S/F/M/Ret/TVR 近闸 | checkpoint `results[].status` (PASS_CHEAP / CHECK_PENDING) |
| ② 生产仿真 OOS | 样本外稳健 | 是否跑过 OOS simulation（通常 0） |
| ③ 生产相关性 | PROD_CORRELATION + SELF_CORRELATION | checkpoint `found_alphas[]` (含 prod_corr/self_corr/robust/risk_neut) |
| ④ submittable + submit | 平台判定 + 真实落平台 | 脚本 `no_submit`? / 是否显式 submit |

**输出格式**：
- 三级分类表：✅ 已正式提交 / ✅ 回测完成待提交 / 🔶 仍需进一步验证
- 逐候选明细表：pid / 任务 / S / 已完成验证项 / 缺少步骤 / 操作建议
- 结论必须明确："N 个候选，0 已提交，0 待提交，N 个仍需验证"
- **绝不称 PASS_CHEAP 为"可提交"**；`YPgAa3WR` 是最接近者但缺 OOS+submittable+submit（仍需 3 项）

## 11. ETA 预期完成时间（强制章节，每次汇报不可省略）

**每个在飞挖掘任务必须给出墙钟 ETA**：

- **ds 舰队**：从 `*_progress_*.log` 取 done/total/elapsed_sec → remaining÷(done÷elapsed) → +now → 格式 `MM-DD HH:MM`
- **tri_track 独立账号**：分片完成数 ÷ 总分数，每分片 ~300s(实测 miner log) × 剩余 ÷ CONCURRENCY
- **v52b 等无进度日志者**：标注 **未知** 并注明原因（仅写 checkpoint、无进度日志）→ 建议补 progress 日志
- **置信度标注**：运行 <30min = 低 / 30–60min = 中 / >60min = 较高
- **开放型任务**（如 tri_track 字段遍历无固定总数）：ETA 开放，报实时吞吐 + "至字段表耗尽或手动停止"

**输出格式**：在飞任务 ETA 汇总表（任务 / 当前进度 / 预期完成 / 置信度），包含 ds 舰队全部 7 路 + tri_track + v52b。

## 12. 标准报告结构（唯一标准依据）

所有"盯回测 / 看进度 / 盘点"类报告统一采用四层递进骨架，不得自创结构、不得遗漏强制章节（提交核查三级分类、在飞 ETA）：

- **§1 背景概述**：任务范围、账号、时间窗。
- **§2 分析维度**：进程盘点（§1–§2）/ 并发进度（§2）/ 效率结论（§3）/ 漏斗 / 四关审计（§10）/ ETA（§11）/ 失败归因 / 监控盲区（§4）贯穿。
- **§3 核心发现**：汇总 + 分维 + 全局视图 + 逐项核查。
- **§4 结论与建议**：结论先行 / 问题 / 行动 / 风险。

报告产出使用通用工具（Read/Bash/Grep/Glob）按本框架直接生成。

## 13. 战役 pipeline 进程识别与判停

- `wq-brain-campaign-toolkit` 的 `pipeline.py` 进程归入 **SCAN/MINING 分类**（战役目录内端到端回测宿主），命令行特征 `pipeline.py --campaign-dir`。
- **判停依据** = poll 熔断参数组：progress **60min 无变化判 STALLED**、总超时 360min（参数可被 thresholds.json `poll` 节覆盖）；`STALLED/TIMEOUT` 即判停，不等"看起来没动静"。
- **进度取证** = 批级 checkpoint（`<campaign>/results/pipeline_<wave>_checkpoint.json`，含 batches[].status/multisim/alphas），**不是终端 tail**；ETA 章节的 checkpoint 取证法与本节对齐（剩余批数 × 单批平均耗时）。

## 14. 台账回写（S6→S-PRE 闭环，战役模式下强制）

复盘报告产出后，必须把实证结论回写战役台账，形成 S6→S-PRE 闭环；不回写则 `wq-brain-campaign-matrix` 下次查表读不到最新死路/胜绩，闭环断裂：

1. **波级结果**：经 `wq-brain-campaign-toolkit` 的 campaign 子命令把 done 数 / 最佳 Sharpe / 通过率写入 `wave_results` 台账；无战役目录的临时/跨区场景可用 `mcp__wqb-db__upsert_wave_result` 直写（入库总原则：DB 为结构化真相源，复盘报告文件仅为呈现层）。
2. **数据集层结论**：dead-end（结构穷尽 + 论坛无解）与 win（可复制设置组合）回写 registry（`data/wqb.db` 的 registry_empirical 表）；会话内轻量回写可用 `mcp__wqb-db__upsert_registry_empirical`（战役目录内仍走 toolkit 幂等 CLI 以保留必填字段校验）。
3. **会话内即时落账**：`mcp__wqb-db__upsert_ledger_key` 写 ledger_kv（如 submit_ready 增量），避免只改文件不落库。
4. **方法论规则计数**：若本波在 build_wave 阶段消费了 `tracking/<REGION>/reference/methodology_rules.json`
   的 active 规则，回写 `times_applied +1`；本波达标再 `times_succeeded +1`，`confidence` 按成功率更新。
   规则不回写计数即无法自我校准，等同未消费。
5. **闭环生效**：回写后 `wq-brain-campaign-matrix`（S-PRE）下次查表自动读到最新实证；未回写的复盘报告视为未完成。

### 14.1 verdict 必填（硬约束）

`wave_results.verdict` 为空的记录**不算复盘完成**。2026-08-23 实测：133 条 wave 记录中 97 条 verdict
为空，EUR/GBR/HKG/ASI 四区 68 条全空——数据写进去了、结论没写，下一轮查表读不到任何可复用信息。

每波 upsert 必须带 `--verdict`，取值 `PASS`（有候选过内部严线）/ `FAIL`（全灭）/ `PARTIAL`（部分近闸）。

### 14.2 命令模板

```powershell
# $WQ_PY 见 INDEX.md；$WQ_TOOLKIT_DIR = ~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts
$CD = "tracking/$REGION"
& $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD wave upsert --wave $W --verdict PARTIAL --extra @notes.json
& $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-dead-end --extra @dead.json
& $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-win      --extra @win.json
& $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD ledger set-verdict --wave $W --verdict PARTIAL
```

中文/JSON 参数一律走 `@file` 文件通道（AGENTS.md §5），不要用引号直接传参。
自检：回写后 `mcp__wqb-db__get_wave_result region=$REGION wave_number=$W` 的 `verdict` 字段必须非空。

- 修改报告结构前先与用户确认。
