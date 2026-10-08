# 循环与停止：开波闸 · 停止规则 · 放行 · 循环触发

> 主 SOP 见 [`../SKILL.md`](../SKILL.md)「循环与停止」。**一波 = 步 2 → 步 9**（波的词义见 [`GLOSSARY.md`](../../GLOSSARY.md)）。
> 闸的清单与逃生口的**唯一来源**是 [INDEX](../../INDEX.md) 的两张生成表（`GATE_REGISTRY` / `waiver.GATE_POLICIES`）；阈值的缺省值在 `src/wqb/workflow/nodes/campaign.py` 的 `*_DEFAULTS`，区域覆盖写在 `tracking/<REGION>/config/thresholds.json` 的 `diversity.*`。
> 本文只写**每条规则拦什么、数字例、命中后做什么、谁能放行**。旧文把这些塞进一个 ≈2000 字的表格单元，并夹着会过期的状态（「GBR 至 09-30」）——状态不再写在这里，查 `python tools/waiver.py list --region <R>`。

## L.1 开波前的四道自动闸（`workflow_campaign(stage="S2"/"S3")` 与 `batch_track` 前置；只读 DB、零配额、干跑也走）

| 顺序 | 闸 | 判定对象 | 口径与缺省 | 数字例 | 命中 → 动作 |
|---|---|---|---|---|---|
| 0 | **catalog 前置闸** | 数据集是否有 typed catalog | 缺目录即拒（失败从「gate 时崩」提前到「开波前拒」） | JPN 白名单 12 集缺 10 | 回步 3 跑 S1 补 catalog，或把该集移出白名单 |
| 1 | **signal_floor（信号天花板）** | region（带 `dataset` 时为 region × dataset） | 最近 `min_batches`（缺省 2）个**波**的 max\|sharpe\| < `max_sharpe_floor`（缺省 0.5；区域覆盖：IND 1.2 / USA 0.9 / MEA 1.2，均取各区 max\|sharpe\| 的 p25、样本 ≥ 8 波、只上调不下调）。证据不足 `min_batches` 个波不判；整节缺失 → **fail-closed 回落缺省**并 `warning`，仅 `enabled:false` 才放行 | GBR 跑满 180 条回测、max\|sharpe\| = 1.04、达标 0，按自己的配置本该在第 2 批停 | 换 universe / 数据集 / 区域，不要绕过 |
| 2 | **stop_rules（停止规则）** | 见 L.2 | 见 L.2 | 见 L.2 | 见 L.2 |
| 3 | **backlog（积压）** | region | `conversion`（已回测 ÷ 已生成）< 0.10 **且**总量 ≥ 200 → 拦；`pending+gated` 占比 > 0.30 且总量 ≥ 200 → 拦；**未消费**占比（`gem+selected+pending+gated`）> 0.30 **默认只报不拦**（`unconsumed_enforce=false`，灰度） | GLB 0%、EUR 1%、GBR / ASI 3%、CHN / KOR 7%、USA 9% 都曾在违反时继续开新波 | 先消化近闸积压，再开新波；清理走 `python tools/campaign_intel.py backlog-drop --region $REGION`（缺省 dry-run，`--apply` 写库）；**判据只有这一套**（旧文另有 `conversion<10%` 与步 6 的 `2 倍` 两套说法，已并入此表）；禁止无脑新建表达式堆库 |

> **signal_floor 参数的权威位置** = `tracking/<REGION>/config/thresholds.json` 的 `diversity.signal_floor`（**不在** `references/regions/*.md` 的 profile 里——profile 只写区域画像）。实测 13/13 区域均已配该节（AMR / ASI / CHN / DEU / EUR / GBR / GLB / HKG / IND / JPN / KOR / MEA / USA；TWN 有 profile 但没有 `tracking/TWN/` 目录，不在此列）。注意：`_evidence` 里「样本 0 波」指的是回填需 ≥ 8 波的样本门槛未达（故不上调 floor），**不是**该区闸失效。 <!-- lint:counterexample: 同上：以 TWN 为例说明「profile 有但目录缺」不计入 13/13 实测样本 -->
>
> 两个易混点：① `signal_floor` 看的是**最近两个波**的 max\|sharpe\|，不是全历史（取全历史会让闸永不触发——GBR 全局 max 1.04 > floor，哪怕最近 10 批都是 0.3）；② `signal_floor` 拦的是「**信号缺席**」，`stop_rules` 拦的是「**撞墙型或重复失败**」，两者正交（stop_rules 只在 evidence 里标 `wall` / `signal_absent`）。

## L.2 停止规则（stop_rules；三条，对象不同，别混）

计数的「**轴**」= region × dataset；「**可计数 FAIL**」= `wave_results.verdict == FAIL`，且**不是** UNKNOWN、**不是**零配额 FAIL（有 `gate_results` 无 `backtest_results`）、**不是**产出了新 dead_end 的 FAIL 波（这两类豁免可分别在 `diversity.stop_rules.exempt_zero_cost_waves` / `exempt_dead_end_waves` 关闭）。

| 规则 | 对象 | 判据（缺省；`stop_rules.*` 可调） | 数字例 | 命中动作 |
|---|---|---|---|---|
| **A 区级产出** | region | `backtest_results` 中 sharpe 非空的行 ≥ `yield_min_backtests`（100）**且** sharpe>1.58 且 fitness>1.0 的行数 = 0（`meets_internal_line`，见 GLOSSARY） | GBR 0/327 | 该区停：换区（`wq-brain-campaign-matrix`），或用户显式指令放行 |
| **B1 同轴熔断** | 开波时带的那个 dataset 轴 | 该轴最近 `consecutive_fail_waves`（3）个 closed 波**连续**可计数 FAIL → 拒开该轴；**换数据集 / 换轴计数清零** | 同一 `fundamental17` 连续 3 波 FAIL → 拒；改开 `analyst44` 照常 | 换数据集 / 换轴；或 `brain-next-move-analysis` 复盘该轴 |
| **B2 区级多轴停** | region | 最近 `axis_window`（8）个 closed 波内**无任何 PASS**，且**全部**为 FAIL 的不同轴数 ≥ `distinct_fail_axes`（4） → 停区（多轴探索已证伪） | 8 波里 4 个不同数据集全 FAIL、0 PASS → 停区 | 换区，或用户显式指令放行 |

- **撞墙型 FAIL**（波内 max\|sharpe\| ≥ signal_floor 的 floor）**照样计数**，但输出会附路由提示：优先 prod-first 探针 / 换 universe / 换池，而不是停区。
- **窗口按波的开始时刻取**（该波首次入库表达式的时间），补记旧波结论不会把旧波顶进窗口。`evidence.recent_closed_waves` 列出窗口内的波号。
- **回落口径**：`axis_scope:false`、schema 不齐、或窗口内所有波都推不出 dataset 轴时，回落旧口径「区最近 K 波 verdict 全 FAIL」；可选更严口径 `strict_no_pass:true` = 最近 K 波无任何 PASS 即停。verdict 为空 / 不可识别（UNKNOWN）**不据此拦截**，只 WARN——请补写（探针 / 全灭波也应写 FAIL，别留空壳 closed 记录）。
- **人工规则（没有代码判定，别当成自动拦截）**：① 「连续 3 波 `gate_results.all_pass` 全 0」→ 该信号族 / 数据集判死，转 `wq-brain-campaign-matrix` 换数据集或 `brain-next-move-analysis` 换区；② 「白名单被 dead_end 全覆盖」→ 停止。这两条是判断，不是闸。

## L.3 用户显式要求继续：放行（waiver）而不是绕过

放行协议的唯一叙述在 [`AGENTS.md`](../../../../AGENTS.md) §8.1.2（`src/wqb/waiver.py`，CLI `tools/waiver.py`）。要点：

| 项 | 内容 |
|---|---|
| 键 | `waiver_<gate>_<region>_<wave\|all>`；本文相关的 `<gate>`：`stop_rules`（规则 A / B1 / B2）、`backlog`、`region_gates`（整体降级：CLI `--gate-mode warn|off`） |
| 谁能批 / 最长有效期 | 这三个闸**只有用户**能批；`stop_rules` / `backlog` ≤ 30 天，`region_gates` ≤ 7 天。到期不续 = 自动失效（`expires_at` 必填） |
| 怎么写 | `python tools/waiver.py new --gate stop_rules --region <R> --reason-code USER_INSTRUCTION --reason "<用户指令原话>" --approved-by user --days <n> --write`（校验通过才写；agent 也可用 `mcp__wqb-db__upsert_ledger_key`，值的形状由闸拦截时的提示给出） |
| 旧键 | `stop_rules_override` / `backlog_gate_override`（`{reason, until}`）仍被识别；**缺 `until` = 永久放行并告警 NO_EXPIRY**——新写入一律用新键 |
| **signal_floor 与 catalog 闸** | **没有专门的 waiver 闸**：要么换 universe / 数据集 / 区域（首选），要么在 `thresholds.json` 把 `diversity.signal_floor.enabled` 设 false 并在台账记理由。不要靠 `--gate-mode warn` 蒙混 |
| 红线（不可豁免） | 提交前的用户确认、凭据、平台限额——见 `waiver.RED_LINES` |

放行的效果会打在 gate 结果的 `waiver` 字段与横幅里，并进报告的 `waivers`；`WQB_WAIVER_MODE=enforce`（或 `--waiver-mode enforce`）时，CLI 逃生开关缺 waiver 直接 exit 2。

**CLI 直调的日期**：直接调 `build_wave.py` / `tools/wave_gate.py` 时，开波闸缺省 **2026-10-11 及以前只告警，2026-10-12 起拦截**（exit 2；到期表见 `docs/time_bombs.json`；解析顺序 `--gate-mode` > 环境变量 `WQB_GATE_MODE` > 按日期缺省）。workflow 节点一律拦截。放行停波区域写 waiver，不要靠 `--gate-mode warn` 绕过。

## L.4 继续 / 转向的路由（循环里的其它条件）

| 条件 | 动作 |
|---|---|
| 本区 ACTIVE REGULAR ≥ 10 | 可转 [`wq-brain-superalpha`](../../wq-brain-superalpha/SKILL.md)（先 `mcp__wq-brain-http__sa_probe(region=$REGION)`，返回 `GO` / `BLOCKED`）。10 是**平台**对 SUPER 组件数的下限（`selectionLimit ≥ 10`，报错原文 "At least 10 component alphas"；须同一 region、已 ACTIVE），不是经验值 |
| REGULAR 当日配额耗尽（ET 日历日，`python tools/quota_status.py`） | 挂起**提交**，继续步 2 → 9；但**未提交的已达标 alpha 会积压**——积压超过下一个 ET 日的配额（REGULAR 4）就该优先清库存（步 1 §1.2）而不是继续开新波 |
| 用户要求持续日循环 | 每个 ET 日先 `brain-next-move-analysis`，再从步 1 跑一波；**21:30 ET 之后不再发起新波**（留出提交窗口）。21:30 与配额 00:00 ET 重置不是同一件事：前者是「什么时候停止开新波」的操作约定，后者是配额换日的平台事实 |
| PPA 主题匹配 | 走 PPA 分支，见 [`ppa-vs-ra.md`](ppa-vs-ra.md) |

**可选外壳**：曾有 `ralph_daily_loop.py` / `ralph_runner.py`，已归档到 `attic/ra_pipeline_shell_20260928/`（零运行痕迹；循环体仍是上面九步，不是第二套 SOP）。
