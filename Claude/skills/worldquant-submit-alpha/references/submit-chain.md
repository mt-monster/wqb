# 提交链：可达状态机 · 权力分层 · 不可逆动作块

> 本文是「一颗 alpha 从模拟结果走到平台 ACTIVE」的**唯一叙述**。其他 skill / 文档写「提交判定」时只许引用本文，不再自述一套。
> 词汇（否决权威 / 放行权威、dispatch / submit、FAIL / PENDING / WARNING）见 [`GLOSSARY.md`](../../GLOSSARY.md)。
> 来源：`reports/skills_review_20260929.md` X-2、X-9、SB-03 / SB-13 / SB-14。

## 0. 不可逆动作块（本链唯一的不可逆一步）

> ⚠ **不可逆：`POST /alphas/{id}/submit`——通过即提交，无撤回。** 平台把它同时当「提交」和「提交前检查」，所以**没有零成本的 POST 探测**：
> 任何一次「试探性 POST」只要全过，就是一次真提交。
> **前置（缺一不得执行）**：① `submit_verdict` 不是 `BLOCKED`（§2 步 2）；② 资格门 Failed RA / PPA = 0（步 1）；③ `check_correlation(alpha_id, refresh=True)`
> 实测 prod < 0.7（步 3）；④ **用户明确确认**（步 5）；⑤ 本 ET 日 REGULAR 配额未满（`python tools/quota_status.py`）。
> **默认形态（预检 / 干跑）**：`workflow_submit_alpha(alpha_id=…, confirm_submit=False)`——只做本地预检并查状态，不 POST。
> **需要用户明确确认**：是（`confirm_submit=True`、`super_build.py submit`、PPA 走 web UI 都一样）。
> **执行后必须核验**：`get_alpha_details` → `status == ACTIVE` 且 `dateSubmitted` 非空。**异常**：见 §4；不盲重试，仅「异步受理未翻转」可补发一次。

## 1. 权力分层：否决权威 ≠ 放行权威

| 权力 | 谁 | 能做什么 |
|---|---|---|
| **否决权威** | 资格门、`submit_verdict`、prod 实测（步 4）、稳健性闸、边际贡献（步 4b，2026-11-08 起）、混腿审查（步 4c，2026-11-08 起）、**分散度软闸（步 4e，2026-11-08 起，`force` 可豁免）** | **只能拦，不能放**。任何一个说「不」就停（4c 的三问与 4e 属自设纪律，`force` 例外放行但留痕） |
| **纯信息** | prod 快照恒等式 `is.prodCorrelation`（步 8） | **既不拦也不放**。提交后校验「闸门读数 == 平台冻结值」，不一致只告警留痕——此时已 ACTIVE，无可回退；拿不到就跳过 |
| **放行权威** | **用户明确确认** + `workflow_submit_alpha(confirm_submit=True)` | 唯一能让 POST 发生的路径；不可逆 |

因此「`submit_verdict` 说了算」只对否决成立：它说 `BLOCKED` 就不提交；它说 `UNVERIFIABLE`（现实中最好的结果）**不是放行**，后面还有 prod 实测和用户确认。

## 2. 可达状态机

| 步 | 判定 | 权力 | 入口 | 结果 | 可逆 |
|---|---|---|---|---|---|
| 1 | **资格门**：`Failed RA == 0`（PPA 看 `Failed PPA`）；名单内若仍有 `PENDING`，`Failed=0` 只表示「暂无失败」，**待其算完再判** | 否决 | `wqb.config.compute_webdata_failed_counts`（`submit_verdict` 已内含；输出里的 `pending_ra` / `pending_ppa`） | 非零 → 回 ra-pipeline 步 7 修 | 是 |
| 2 | **模拟层 + 硬闸类 WARNING**：`is.checks` 无 FAIL；`LOW_FITNESS` / `LOW_SHARPE` / `LOW_2Y_SHARPE` / `IS_LADDER_SHARPE`（后两者 = `RA_2Y_NAMES` 双载体）的 WARNING 视同 FAIL | 否决 | `python tools/submit_verdict.py --alpha-id <ID>`（或 MCP `submit_verdict`；同一份实现 `wqb.submit_verdict_core`） | 见 §2.1 退出码 | 是 |
| 3 | **prod 实测 < 0.7**（`GET correlations/prod`，账号级单并发；忙时立即返回 `correlation_busy`，阻塞轮询窗口见 `WAIT_THRESHOLDS`） | 否决 | `mcp__wq-brain-http__check_correlation(alpha_id, refresh=True)`；SUPER 用 `super_build.py probe` | ≥ 0.7 → prod 墙决策表（ra-pipeline `decision-table.md` D0） | 是 |
| 4 | **稳健性闸** | 否决（**有代码读取**：结论落台账 `robustness_<alpha_id>`，`submit_verdict` 三入口读它——`REJECT` → `BLOCKED`；`CONDITIONAL` / 无记录只在 `next_step` 提示，不拦） | brain-alpha-robustness | `REJECT` → 停 | 是 |
| **4b** | **边际贡献闸**：`performance_comparison` 把候选等权叠加到其**所属分区组合**，返回 before/after。`submit_alpha` 节点 **Step 1.7** 自动跑（`confirm_submit=False` 的预检也跑） | **否决**（2026-11-08 用户明令「边际贡献为负就阻断不准提交」；此前 2026-11-04 为信息项）。`ΔSharpe<0` + `confirm_submit=True` ⇒ `blocked=True`，在 set_properties/POST 之前 return，**force 不豁免**；`available=False`（空体/超时/异常）**不阻断**（可用性缺失 ≠ 为负） | `mcp__wq-brain-http__performance_comparison(alpha_id)` | `blocked_reason` 指向「换候选或改结构使 ΔS ≥ 0」；预检阶段只出数值 + 预告 | 是 |
| **4c** | **混腿审查**：对 `regular.code` 分级 + 验「三问」。`submit_alpha` 节点 **Step 1.2** 自动跑（`confirm_submit=False` 的预检也跑，纯函数零网络，位置在 prod 闸之前以省探针槽） | **否决（两级）**：① `weight_grid`（单次 `add` 顶层 ≥2 条系数腿）/ `stack`（展平 ≥4 条腿）⇒ **一律阻断，`force` 不豁免**；② `two_leg` / `three_leg` 缺三问 ⇒ 阻断，`force=True` 可豁免留痕。判定哲学：官方只禁「**without any strong economic sense**」的跨源相加（Consultant Dos and Don'ts），不是禁 `add` 本身 | `submit_queue.mix_review(expr, narrative)`；三问经 `workflow_submit_alpha(mix_narrative={holders, polarity, prior})` 传入，每条 ≥8 字符（挡 "ok"/"n/a"） | `blocked_reason` 指向「拆成单腿重挖，或改 ≤3 腿且权重由先验固定后重跑」；预检只出 `mix_warning` 预告 | 是 |
| **4d** | **路径判决**（与 4c 同一步顺带产出，**不阻断**）：`is.checks` 里 `LOW_2Y_SHARPE` 与 `IS_LADDER_SHARPE` **互斥**，据此读平台把本颗归为单数据集（ATOM）还是多数据集 | **纯信息** | 同上（`mix_audit.data_usage` / `path` / `hint`） | `ATOM:LAST_2Y` ⇒ **不走 Ladder**，只查 Last-2Y IS Sharpe，2Y 不足直接 FAIL、无退路；`LADDER` ⇒ 2Y 不足时可逐级降线到 7Y / 10Y 窗 ⇒ 近 2 年弱不必然死。**具体线随 region/universe/delay 变**（官方示例 2.38 / 7Y 2.06 / 10Y 1.59；实测 GBR-TOP700-D1 的 2Y=1.98 可过、DEU 侧 7Y 1.751）——以该颗 checks 的实判为准，别套死数字 | — |
| **4e** | **分散度审查**：`is.selfCorrelation` ≥ **0.55**（软线）时，要求 `ΔSharpe ≥ +0.02` 才放行。`submit_alpha` 节点 **Step 1.8** 自动跑，**零额外网络请求**（复用 4b 已算的 ΔS 与 `precheck` 的 self 读数），位置在 Step 1.7 之后、set_properties 之前 | **软否决**：高相关 + ΔS 落在噪声带 ⇒ `blocked`，但 **`force=True` 可豁免留痕**（自设纪律，非平台红线；与 4c 的三问同级）。self 或 ΔS 读不到 ⇒ `unknown` **fail-open** | 无新调用（`diversity_audit` 步骤直接读 `is.selfCorrelation` + 上一步 `delta.sharpe`） | 依据：CAP ≈ (μ̄/σ̄)·sqrt(N/(1+(N-1)ρ̄))，有效宽度**饱和于 1/ρ̄** ⇒ 降 ρ 比增 N 有效；官方 Consultant FAQ「build diversity in your personal Alpha pool」+ Brain Genius「pyramids … improve Combined Alpha Performance through diversification」。阈值口径：READY 队列 self 分位 p50=0.394 / p75=0.505 / p90=0.656 ⇒ 0.55 命中 top 15–25%；ΔS 噪声 0.005–0.01，0.02 = 2–4 倍噪声。**平台线仍是 0.7**，0.55 只是自设软线 | 是 |
| 5 | **用户明确确认** | 放行的必要条件 | 人 | 未确认 → 停在这里，列出候选与证据交用户 | 是 |
| 6 | **提交** `workflow_submit_alpha(confirm_submit=True)` | **放行（不可逆）** | 本 skill §4 四态表 | 200 = 已提交；201 / 202 / 空体 200 = 异步受理 | **否** |
| 7 | **轮询与补发**：等状态离开 `UNSUBMITTED`；窗口内未翻 → 补发一次 → 再等一个窗口 → 仍未翻记 `ASYNC_STUCK` 并知会用户 | — | 窗口取 `WAIT_THRESHOLDS`（`submit_flip_wait_s` / `submit_flip_poll_s` / `submit_repost_max`） | `ACTIVE` = 完成 | — |
| 8 | **prod 快照恒等式**（提交后）：读 `is.prodCorrelation` 与步 4 闸门读数比对，`Δ>0.005` 即告警。`submit_alpha` 节点 **Step 5** 自动跑 | **纯信息**（提交已 ACTIVE，无法回退）。`available=False`（无闸门读数 / 平台未回填 / 读取失败）一律跳过 | 1 次 `get_alpha_details` | `prod_snapshot_warning` 进结果体；一致则注明「prod 闸诚实」 | 否 |
| 分支 | **PPA**：MCP 预检线不满足的合法 PPA 走 web UI 人工通道，agent 停下并交接（`ppa-handoff.md`）；**SUPER**：`super_build.py submit` 强制带 prod 闸（2026-10-18 起无豁免入口），且**第一次通过的 POST 就是真提交**，不是「预检」 | | | | |

### 2.1 `submit_verdict` 状态与退出码

| verdict | 含义 | 退出码 | 下一步 |
|---|---|---|---|
| `BLOCKED` | 模拟层 FAIL / 硬闸类 WARNING / Failed-count 非零 / 提交层 403 / 未知响应 | **1**（未捕获异常同样 1：fail closed） | 修复并重新回测；**不绕过**（`force`、直接 POST 探测都不可取） |
| `UNVERIFIABLE` | 模拟层干净，但提交层没有信息（`GET /submit` 恒 404） | **10** | 走步 3；**不是放行** |
| `ALREADY_SUBMITTED` | 已 `ACTIVE` / `SUBMITTED` | **11** | 不要再 POST；如需回写走 S6 |
| `SUBMITTABLE` | 模拟层干净且 `GET /submit`=200 | 0 | **现实中不会出现**（GET 恒 404），仅防御分支；文档与上游条件不得写「等 SUBMITTABLE」 |

以 `$?==0` 放行的脚本是错的：UNVERIFIABLE 曾经也是 0（2026-09-29 前）。路由请读退出码，且**只把 1 / 10 / 11 当作有信息的结果**。

## 3. 提交层信息来源：各能回答什么、会不会真提交

| 来源 | 能回答 | 会真提交吗 |
|---|---|---|
| `GET /alphas/{id}/submit` | **什么都回答不了**：本平台恒 `404` + 空体（2026-09-26 实测：未提交与已 ACTIVE 的同样 404）。不要用它做任何判定 | 否 |
| `POST /alphas/{id}/submit` | 提交层真相：200 / 201·202 / 403（带全量 `is.checks` 与真因） | **是——通过即提交** |
| `get_alpha_details(alpha_id).is.checks` | 模拟层各检查的 `PASS` / `FAIL` / `WARNING` / `PENDING`；`status` / `dateSubmitted` | 否 |
| `submit_verdict` 输出 | 上面两类模拟层信息 + 资格门 + 硬闸类 WARNING 的合成判定（**否决**用） | 否 |
| `check_correlation(refresh=True)` | prod / self 相关性实测（异步排队，已决结果缓存 **48 小时**，落 SQLite 权威表 `alpha_corr_cache`；终验用 `refresh=True`） | 否 |
| `performance_comparison(alpha_id)` | **仅未提交候选**：候选叠加到所属分区组合前后的 before/after（提交前预览）。**已提交后恒 `400 Bad Request`**——2026-11-04 实测 20/20 已提交（HKG/DEU/USA/GBR/GLB/EUR/KOR/IND/ASI/MEA 九区抽样）全 400，3/3 未提交全 200 ⇒ **平台自定位为「提交前预览」，不是事后归因工具**，别拿它做 OS 归因（OS 归因走 `get_alpha_pnl` / 逐年 stats） | 否 |

> 「提交层视图」一词只指第一行那个死端点；其余都直接说来源名。

## 4. 与本链相关的必读细节（不重复正文）

- **POST 四态表 / 补发护栏 / 配额 403** → [`../SKILL.md`](../SKILL.md)「响应处置」与 [`scenarios.md`](scenarios.md)。
- **混腿口径的官方依据（步 4c 为什么长这样）**：`Consultant Dos and Don'ts`（2026-09-18）唯一相关条款是
  「**DO NOT add an existing Alpha from one data source to enhance the signal from another data source
  without any strong economic sense**」——禁的是「无经济含义的拼接」，**有强经济含义的跨源组合是允许的**；
  平台 9 项提交测试（Fitness/Sharpe/Turnover/Weight/SubUniverse/Self/Prod/IS-Ladder/Bias）**无一检查表达式结构**。
  故本链只硬拦「结构上答不出经济含义」的两类（权重网格 / ≥4 腿堆叠），2–3 腿交给三问（经济含义是不是真的）。
  真正的官方红线是「incorporate noise to reduce production correlation」——**为降 prod 而加噪**，与加腿本身无关。
- **ATOM 的免费判别法**：看 `is.checks` 里出现的是 `LOW_2Y_SHARPE`（单数据集）还是 `IS_LADDER_SHARPE`（多数据集），
  两者互斥。ATOM 只查 Last-2Y，2Y 弱就真死；多数据集可退到 7Y / 10Y。这也是「混信号有时更好过闸」的原因。<!-- 2026-11-08 -->
- **配额模型（ET 日历日、来源、复检）与点塔优选** → [`quota-and-tower.md`](quota-and-tower.md)。
- **★ 为什么「margin 闸」与「近段 Sharpe 排序键」没有进这条链（2026-11-08 实证否决）**：
  用 124 颗已提交 USA alpha 的真实 OS 数据检验「哪种提交标准真的影响 Combined Alpha Performance」，两条当时的直觉提案都被否掉，记在这里防止以后重犯：

  | 提案 | 实测 | 结论 |
  |---|---|---|
  | 加 **margin 闸**（分区域 bp 阈值） | `ρ(margin, os_sharpe125) = +0.068`（无预测力）；`ρ(margin, −Turnover) = **+0.922**`；`margin ≈ Returns/(504×Turnover)` 逐颗误差 <1% ⇒ **定义上就是 Returns/TO 的函数**，不是独立信息。且 READY 队列 183 颗中 `margin<8bp` 占 **62%**、`<5bp` 占 35% ⇒ 设闸即大面积误伤 | **不加** |
  | 用 **「2023 起 Sharpe」/ 近 2 年 Sharpe 做排序键** | `ρ(two_year_sharpe, os_sharpe125) = **−0.146**`（反向）；`Sharpe +0.007`、`Fitness +0.003`、`sub_universe −0.057`、`returns −0.010` ⇒ **所有 IS 读数对 OS 的秩相关都在 ±0.15 以内** | **不用** |

  唯一有预测力的是 **OS 自身**：`ρ(os60, os125)=+0.564`、`ρ(os125, os全期)=+0.639`；数据集层面组间 `R²=0.010`（无可继承性）。
  ⇒ 因此这条链能改善 CAP 的只剩三件事：**数量（稀释速度）、ρ̄（有效宽度）、ΔSharpe（唯一直接测组合的量）**。步 4b 与 4e 正是后两者的载体。
  复跑：`python tools/gates/margin_predictive_power.py`。
- **★ Q4 计入窗口**：官方 Brain Genius「Alphas submitted in the **last month of the quarter** may not count towards the Combined Alpha Performance used to compute Genius levels at the end of the quarter, since the metric takes some weeks to compute」。
  Q4 = 10/11/12 ⇒ **最后一个月的指 12 月**，不是 11 月。**11 月提交的全部计入 Q4**；12 月提交的仍算 eligibility 与 VF，但 CAP 顺延到 Q1。
- **PPA 人工交接单** → [`ppa-handoff.md`](ppa-handoff.md)。
- **MCP 不可用时的 REST 兜底** → [`fallback-rest.md`](fallback-rest.md)（凭据只读进程环境变量，不读 `.env`）。
