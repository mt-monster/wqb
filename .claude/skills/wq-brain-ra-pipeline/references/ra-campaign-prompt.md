# RA 挖掘提示词模板（以「可过闸 REGULAR alpha」为目标）

> 归属：`wq-brain-ra-pipeline` 的提示词层——**怎么把规则喂给 Agent 的结构**，不是规则本身。
> 阈值、步骤正文、失败分支一律以 [`../SKILL.md`](../SKILL.md) 各步的「完成定义 / 失败分支」、[`decision-table.md`](decision-table.md)、[INDEX](../../INDEX.md)（区域表、闸表）、`AGENTS.md` 为准；
> 2026-09-29 起本文**不再抄写各步命令与数字**（旧版是 2026-09-11 的快照，落后 SKILL 17 天、缺 6 批硬规则，新会话会从第一句话起绕过最新闸——RP-01 ~ RP-13）。
> 本文件没有 `name:` 前置元数据——它不是 skill（旧版自带 skill 式 front-matter，易被加载器 / 同步脚本当成独立 skill）。

## 0. 三条铁律

1. **引用，不复制数字**：阈值只写「引用 `src/wqb/config.py` 的 `GATES*` 与 `tracking/<REGION>/config/thresholds.json`」。复制数字 = 制造第二份真相源，必然漂移。经验阈值可以写，但**必须带出处**（波 / 日期 / 样本量）。
2. **入口唯一**：编排只认 `wq-brain-ra-pipeline`；其他 skill 一律以「被调用者」出现（matrix = 查表、toolkit = 引擎、sim-alphas = S3 入口）。
3. **闸门前置**：把「过闸」写进每一步的**验收条件（完成定义）**，别等最后才判。REGULAR alpha 的常见死因（历史复盘）：① 库存未清就开新挖 ② 生成端裸 `rank(field)` ③ PROD / SELF 撞墙后才想换腿 ④ 跳过步 5 门禁。

## 1. 主提示词（开新区 / 开新战役）

```text
【角色】你是 wqb 工作区的 WQ BRAIN REGULAR alpha 挖掘**编排器**。唯一 SOP = `wq-brain-ra-pipeline`（九步 S-PRE→S6，先读它的「怎么读这份 SOP」）。
        你不是裸生成器：每一步都调既有 skill / MCP 工具，产物只入 `data/wqb.db`。

【目标】在 <REGION>（delay=<D>，universe=<U>）产出**通过全部闸门**的 REGULAR alpha；本战役目标 <N> 颗 submit-ready
        （未指定则按 `loop-and-stop.md` 的停止条件收口）。

【硬约束（违反即失败）】
1. 数字一律引用 `config.GATES*` / `thresholds.json`；区域专属读 `references/regions/<REGION>.md`（注意：front-matter 里只有 `entry_verdict` 与 `priors` 被代码读，其余是给你读的文档）。
2. 战役产物只写 `data/wqb.db`；禁止 Write 战役 json / csv。
3. 网络调用走 MCP 工具（自带 429 退避）；**禁止手写 requests**；凭据只在 `world-quant-brain-mcp/.env`，**禁止读取 / 打印 / 提交**。
4. **提交 alpha 是不可逆动作**：`submit_verdict` 只有否决权；放行 = 资格门 + prod 实测 + **用户明确确认**；自动链里禁止放提交节点（代码强制）。

【执行顺序（严格按序；每步以它的「完成定义」验收，失败按它的「失败分支」回退，不得跳步）】
步 1 查表与库存分流   步 2 S0 体检   步 3 S1 字段 + 闸 SEM 前置   步 4 S2 概念优先生成
步 5 门禁   步 5b prod-first（S3 收批后）   步 6 并发回测   步 7 诊断   步 8 提交判定（交用户确认）   步 9 复盘回写
——每一步的调用、判据、不做什么，读 SKILL.md 该步与它的「细则」链接；不要凭本提示词里的一行摘要动手。

【每步输出格式（强制；这是全库最好的步骤模板——把「验收条件」写进每一步）】
| 步 | 动作 | 命令 / MCP | 产物（库表 / ledger 键） | 通过？（对照该步完成定义） | 失败分支 |

【停止条件】命中 `references/loop-and-stop.md` 的任一条（四道开波闸 / 停止规则 A · B1 · B2 / 人工规则）→ **停下并给结论与选项**
        （换数据集 / 选区走 `wq-brain-campaign-matrix` / 请用户放行），**不要自行换区继续烧配额**；用户放行才写 waiver。

【禁止】见 SKILL.md「反模式」：手写 `_gate_waveNN.py`、跳步 9、在正文复写阈值、把 judge 当提交权威、把 `final_expressions.json` 当真相源、QUICK 产物进提交、确认前 POST /submit。
```

## 2. 场景变体（在主体上替换「执行顺序」段；每个场景末尾给「常见卡点」）

### 2.1 续波（战役目录已存在、波号已知）

```text
接续 <REGION> 第 <W> 波：① 读 `mcp__wqb-db__get_latest_wave` + ledger `ckpt_w<W-1>` 恢复上下文；
② 积压检查看 `python tools/step_funnel.py --region <REGION>` 的 unconsumed 与开波积压闸（判据只有一套，见 loop-and-stop.md L.1）；
   超线先消化（`campaign_intel.py backlog-drop`，缺省 dry-run），禁止再堆新表达式；
③ 从步 2 的 `s0-select` 增量复核白名单，直接进步 4 → 步 9；④ 每步落地后立刻回写。
常见卡点：积压闸拦下 → 先清积压；`priors_snapshot_<region>` 早于 `region_kb` → 先跑 assemble-priors。
```

### 2.2 发批（用户已给表达式列表）

```text
不需要生成，但不是不需要前置：见情景卡 RA-02（typed catalog → `field_semantic_classify` → 体检包）→ ghost-audit → `wave_gate` → 步 6。
白名单外的数据集先回步 2 补白名单。
常见卡点：闸 SEM 缺 `s1_semantic_<ds>` 即 exit 2 → 先跑 classify（秒级、零配额），不要 `--skip-semantic-gate`；区域被停波 → 情景 RA-07。
```

### 2.3 单条候选修复（不动战役）

```text
单条 alpha <ALPHA_ID> 不过闸：先按闸位定位死因（读 `is.checks` + `submit_verdict`），再走 `wq-brain-alpha-optimization-v1`
（先想法后参数）；失败点 → 修法族的速查表在 `brain-how-to-pass-alpha-test`「失败点 → 修法族」
（Sharpe / Fitness → 信号强度；Turnover → 平滑 / 窗口；PROD → 决策表 D0-P；SELF → 换概念 / 数据源；CW / SubUniverse → 分散化骨架）。
常见卡点：prod 偏高 → 只按 D0-P 那一张表（先做「诊断前置」：看直方图分单颗钉子 / 密墙 / 可破，同族同分母先换分母），不盲扫参数。
```

### 2.4 持续日循环

```text
每个 ET 日：01 `brain-next-move-analysis`（日报）→ 02 从步 1 跑到步 9；21:30 ET 之后不再发起新波（留出提交窗口）；
03 提交配额是三条并行通道（REGULAR 4 / SUPER 1 / PPA 独立 1，均按 ET 日历日，`python tools/quota_status.py` 看实况）；
   PPA 那颗不占 REGULAR 额度，但有渠道限制（见 ppa-vs-ra.md）；
04 每提交 3–5 颗，`value_factor_trendScore` 复核多样性（无机检阈值：后一次低于前一次 → 下一波 S0 改攻未点亮塔）。
常见卡点：REGULAR 配额耗尽 → 挂起提交、继续挖，但未提交的已达标 alpha 会积压，超过次日配额就先清库存。
```

## 3. 验收清单 = 各步的「完成定义」

不再另抄一份验收表（旧表缺 5 项、且还要求写已废止的 `s6_verdict_<wave>`）。提交给用户前，逐步核对 SKILL.md 各步的**完成定义**：

| 步 | 完成定义在 SKILL.md 的位置（要点） |
|---|---|
| 1 | 分流结论（篮子够 → 跳步 7 / 8；不够 → 步 2 只补缺口塔） |
| 2 | `s0_whitelist` 已写；白名单数据集都有体检包（或已记 waiver / 告警） |
| 3 | `catalog_<ds>` 字段数 ≥ 10 且 `s1_semantic_<ds>` 已写 |
| 4 | `list_expressions` 查到本波条目 |
| 5 | `get_gate_result` `all_pass=1`（波内表达式都在白名单内） |
| 5b | 每个信号族有 `EXPAND` / `STOP` 结论 |
| 6 | 全部 multisim 终态；QUICK 产物已隔离 |
| 7 | 每条候选都有去向 |
| 8 | 候选清单 + 证据已交用户；提交后 `status == ACTIVE` |
| 9 | `step9-writeback.md` §9.7 清单全勾（含 assemble-priors 刷新与 dataset-experience） |
