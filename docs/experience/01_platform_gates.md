# 01 · 平台规则与硬门槛

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-10-24（§4 增补 USA 2026-10-23 复盘的 prod 分布）
>
> **现行政策提示（2026-09-30 合并时补）**：本文里「403 零成本 → 直接 POST 就是预检」的说法只对**被拒**的那一半成立——事先无从知道它会 403 还是通过，而通过的 POST 就是一次真实、不可撤销的提交。所以 `POST /alphas/{id}/submit` **只作用户确认后的真提交**（`workflow_submit_alpha(confirm_submit=True)`），**不作预检 / 探针**；提交前的检查用 `submit_verdict`（模拟层 checks）、`check_correlation`（只读 `GET correlations/prod`）与 `confirm_submit=False` 预检。全链与不可逆动作块见 [`submit-chain.md`](../../Claude/skills/worldquant-submit-alpha/references/submit-chain.md)。

---

## 1. 提交层四闸（REGULAR）

| 闸 | 阈值 | 备注 |
|---|---|---|
| `LOW_SHARPE` | ≥ **1.25**（D1）／**2.0**（D0） | 严格不等式；⚠ **1.58 是 2Y 线（`LOW_2Y_SHARPE`），不是本行**——平台 `LOW_SHARPE` 硬线 Delay-1 为 1.25（`config.PLATFORM_CHECK_LINES.low_sharpe_min`）；本仓**交付线**另按 S>1.58 要求，两条线不可互相顶替（见 `GLOSSARY.md`「Sharpe 有三条不同的线」） |
| `LOW_FITNESS` | ≥ **1.0** | 严格不等式 |
| `LOW_2Y_SHARPE` / `IS_LADDER_SHARPE` | ≥ **1.58** | 同一事实的两个载体，平台按 alpha 代际只发其一 |
| `LOW_SUB_UNIVERSE_SHARPE` | 比值闸（见 §2） | |

> ⚠ **「TO<30% ⇒ 2Y 阈值 ×0.85」在本仓未复现（2026-11-17 实测）**：判别件 `YP1ZvjWA`
> （USA/TOP3000/D1，ATOM 单数据集：仅 `discount_store_retail_score` + 豁免 `sector`）
> TO **17.7%**、2Y **1.57**，平台 `LOW_2Y_SHARPE` 仍是 `warning`、`limit=1.58`、`ra_failed=true`
> —— 若折扣成立，1.57 应过 1.343。⇒ **近闸线一律按 1.58，不要用 1.34**；若某区确要使用
> 1.343，必须先用该区 1.34–1.58 区间的 ATOM 件实测确认，不能引用外部文章。
> 另：`IS_LADDER_SHARPE` 载体同样未见折扣（`WjP07oJN`/`vRk6QNga`/`rKjRj8qj` 均 TO<30%、
> 2Y 1.57、`limit=1.58` 判 fail/warning）。详见 `docs/reference/atom_mining_playbook_20261117.md` §二。

**四者必须同时成立**。另有区域专属闸：
- `LOW_ROBUST_UNIVERSE_SHARPE`（IND，limit **1.0**）
- `CONCENTRATED_WEIGHT` ≤ 0.1
- `HIGH_TURNOVER` — ⚠ **上限区域特异**：本文旧记 0.4，**GBR/D1 实测 = 0.7**（2026-10-07，`checks.HIGH_TURNOVER limit 0.7`）。取阈值前**以本区平台返回的 limit 为准**，勿套用他区。

> **2Y 读数有两个载体（2026-10-23 实测）**：平台按 alpha 代际只发 `LOW_2Y_SHARPE` 或
> `IS_LADDER_SHARPE` **之一**，二者是**同一事实的两个读数位**（`wqb.config.RA_2Y_NAMES`
> 与 `brain-how-to-pass-alpha-test` 的检查表都这么定义）。IND/wave232 有 10/29 颗只发
> `IS_LADDER_SHARPE`（`JjP0Ja5l` ladder 2.82 = `get_alpha_details` 的 2Y 2.82）。
> ⚠ 采集层曾只认 `LOW_2Y_SHARPE` ⇒ `backtest_results` / `alphas` 的 `two_year_sharpe`
> 整列落空，字段画像 `best_2y`、提交队列、Mode B 判死规则一起失真（数据表现：
> `count_institutional_sellers_security` 的 best 2Y 被记成 **−0.15**，真值 2.87）。
> 修复（全部按“两载体同义”收口）：
> ① **采集**：`tools/harvest_multisim.py::_extract_two_year_sharpe`、`wqb_db_mcp._flatten_platform_alpha`（并透传 `is_ladder_sharpe`）；
> ② **评审**：`Claude/skills/wq-brain-campaign-toolkit/scripts/metrics_cache.py`（此前 ladder-only 的行判 `2Y_UNKNOWN`、跳过 2Y 墙）、`Claude/skills/brain-alpha-judge/scripts/judge_alpha.py`（内部 2Y 硬闸）；
> ③ **提交层**：`wqb.submit_verdict_core.SUBMIT_HARD_GATE_WARNINGS` 与 `workflow/nodes/submit_alpha.py`（ladder 的 WARNING 同属提交层硬闸）；
> ④ **修数**：`tools/data-repair/backfill_bt_two_year_from_ladder.py`（存量 `backtest_results`，默认 dry-run）、`tools/data-repair/backfill_alpha_metrics_from_platform.py`、`tools/backfill_2y_from_platform.py`。
> 回归：`test_harvest_two_year_from_ladder.py` / `test_judge_gates_match_config.py` / `test_ra_failed_checks_single_definition.py`（三处都含“只发 ladder”用例）。

### ★ 换手前置判据（SOP 标准步骤，2026-10-07 定）

> **在候选进入「候选池 / 台账 / 提交队列」之前执行，区间外一律剔除，不进池。**

```
保留区间：  TO ∈ [0.03, 0.70]
  TO < 0.03  ⇒ 剔除（近乎静态：换手过低意味着持仓几乎不动，
                往往是"数据未更新/字段近似常量/伪信号"，margin 与容量都不可信）
  TO > 0.70  ⇒ 剔除（超过平台 HIGH_TURNOVER 上限，GBR）
```

**与平台闸的关系（两者都要过，本判据更严）**

| | 平台闸 | 本前置判据 |
|---|---|---|
| 下界 | `LOW_TURNOVER` ≥ **0.01** | **≥ 0.03**（更严） |
| 上界 | `HIGH_TURNOVER` ≤ **0.7**（GBR；他区可能不同） | **≤ 0.70**（对齐） |

**执行工具**：`python to_prefilter.py --wave <波次>` 或 `--alpha-id <ID>...`
（输出 KEEP / CULL(低 TO) / CULL(高 TO) / UNKNOWN 四类，并给出逐条理由）。

**为什么放在「前置」**：TO 在回测后即已知，而 prod/self 相关性昂贵且排队 ⇒
**先用零成本判据砍掉结构性不合格项，再做昂贵检查**，可显著减少无效相关性查询与台账污染。

**历史核查（2026-10-07）**：GBR ANALYST 战役全部候选 + 最近 60 条记录，**区间内 100%、零违规**
（实际分布 TO 0.047–0.23）⇒ 该判据对既有工作无回溯影响。

### 关键判据

- **提交层严格不等式**：`value == limit` 判 **FAIL**。`VkaZYdbG` 的 `IS_LADDER_SHARPE value=1.58 == limit 1.58` → 403。
- **提交层严于 IS 层**：IS 层的 WARNING 在提交层是 FAIL（09-16 三颗 IS 全 WARNING、POST 全 403）。**更正（2026-09-30）**：旧版写的「IS 层 limit 更宽」不成立——`Vk0kLMqG` 真 POST 被 403，且提交层各 check 的 limit 与 IS 层**完全一致**（`LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`、`LOW_ROBUST_UNIVERSE_RETURNS` 逐项相同；`1YZqNxM6` 是特例，不可作通用依据；GBR `IS_LADDER` 曾记 IS 层 1.88 / 提交层 1.58，属单点观察，待复核）。→ **必须在 IS 层就把所有 check（含 WARNING）压过，否则 POST 必 403；"IS 层 PASS" ≠ 能过提交层**。
- **`CONCENTRATED_WEIGHT` 是结构性拒绝，非权重分布问题**：GBR starmine 族里 `ts_decay_linear` 平滑、连外层全市场 `rank()` 均匀化都 403；唯一过提交层的同族结构是 `trade_when` 门控。

---

## 2. ★ SUB 是比值闸，不是绝对闸

`LOW_SUB_UNIVERSE_SHARPE` 的 limit = **0.75 × sqrt(子宇宙规模 / 本 alpha 宇宙规模) × 本 alpha sharpe**（公式见 `brain-how-to-pass-alpha-test` §5）。**系数随宇宙变化，不是常数**：KOR（TOP600）实测 ≈ **0.571**（下表三处独立一致）；USA（TOP3000 → 子集 TOP1000）= 0.75×sqrt(1000/3000) = **0.433**（2026-10-01 USA 两处直查：limit/S = 0.4335 / 0.4333）；SuperAlpha ≈ 0.431；DEU profile 记 ≈ 0.47。**系数一律用 `get_alpha_details` 里本 alpha 的 `LOW_SUB_UNIVERSE_SHARPE` 的 limit / sharpe 当场算**，不要套用别区的数。下表是 KOR 的实测：

| sharpe | SUB limit | 比值 |
|---|---|---|
| 1.80 | 1.03 | 0.572 |
| 1.96 | 1.12 | 0.571 |
| 1.55 | 0.89 | 0.574 |

**⇒ 把 S 压到刚过 1.58 会同步抬高 SUB 的绝对要求，「S 越高越好」是错的。**
正确目标：`SUB/S ≥ 本区系数（KOR ≈ 0.571、USA ≈ 0.433）∧ 2Y ≥ 1.58 ∧ S ≥ 1.58 ∧ F ≥ 1.0` **同时**成立。
**低分区实测值不可外推为「墙」**：limit 随 S 线性增长，S≈0.6 时 SUB 实测 0.30 只是 `S×0.47`，S≳1.7 时该闸自动过（DEU 6 颗 ACTIVE 全部 PASS 该闸，原「DEU sub_universe 结构性墙」是伪墙，见 `regions/DEU.md`）。

**破比值闸的合规旋钮（实测有效）**：
- 分组轴换到 **`market`**（决定性，给比值）或 **`exchange`**（给 2Y）
  ⚠ **2026-10-06 DEU 实测不迁移**：在 `agent_factor_signals` 族（字段 `eps_revision_magnitude`）上，加 `market` 或把 `subindustry` 换成 `market`
  ⇒ **S 1.37→0.56~0.60、sub 0.64→≤0.21（反噬）**。原结论来自 EUR/KOR ⇒ **逐区逐族实测，勿照搬**。
- `signed_power` 压尾（⚠ 压尾前先看持仓对称性：会造成多空不对称而触发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`；优先试等价的 `quantile`，见 `brain-how-to-pass-alpha-test` §5b）
- 长窗 `ts_rank` / `ts_decay_linear` 平滑
- ⚠ **分组轴不是 SUB 闸的通用旋钮**：EUR 有效，KOR other466 六种轴向全灭——逐区实测

---

## 3. 配额

| 项 | 规则 |
|---|---|
| REGULAR | **4 / ET 日** |
| SUPER | **1 / ET 日** |
| PPA | **独立 1 / ET 日** |
| 重置 | 00:00 ET（= GMT+8 次日 12:00，**夏令时**；冬令时为 13:00——2026-11-01 起，以 `tools/quota_status.py` 输出为准） |

**判据**：
- **403 零成本、不扣配额**：被拒的 POST 会回带全量 checks（含真实 PROD/SELF），是唯一能看到提交层真值的地方——但**通过就是真提交**，所以这份信息只能在「用户已确认要提交」的那一次 POST 里顺带拿到，**不能靠 POST 去试**（见文首政策提示）。
- **并行会话共享同一账号配额**（09-21 误判"4 空位"实际只剩 2；09-25 被并会话打满致本会话 0 提交）。
- **403 里 `PENDING` ≠ FAIL**：403 唯一 FAIL 项是 `REGULAR_SUBMISSION value=4 limit=4`（配额用尽）；`SELF/PROD_CORRELATION` 显示 PENDING 不挡提交。
- **配额真值只能查 `tools/quota_status.py`**：`GET /users/self/activities/submissions` **没有 today 字段**（只返回 yesterday/current/previous/ytd，且 `ytd.end` 停在昨天），且计数是 **REGULAR+SUPER 合计**。
- 201 受理后**异步失败要扣额**（`N1708Mr8`）；403 与 IS 失败不扣。

---

## 4. 相关性（prod / self）

### 取数

| 项 | 方法 |
|---|---|
| **prod** | 直轮询 `GET /alphas/{id}/correlations/prod`（恒 200，**空体 = 平台在算**），`max` 即判定值；**单次计算 180–200 s**（2026-10-28 用户口径；旧记「45s ~ 12min」把排队与旧 900s 窗口混在一起了） |
| **self（本地）** | 累计 PnL **必须 diff 成日收益**再 Pearson，窗口 **4×252**（误差 < 0.001） |
| 列表 self-corr | 在 `records[i][5]` |
| **缓存（2026-10-06 改）** | 已决 prod 落 SQLite 权威表 `data/wqb.db::alpha_corr_cache`，**保鲜期 48h**，过期自动回源；**不再依赖 Redis**（旧版 Redis 未启动 ⇒ 缓存静默失效，且 TTL 7 天与 48h 纪律冲突）。命中响应带 `from_cache: true` |

**prod 端点机制**：只返回"已算好"的值，**请求不触发计算**；单账号单并发 + 异步排队 → **高频 refresh 是反效果，等的收益为零**。
→ prod 取数走只读 `GET correlations/prod`（`check_correlation`）；被拒的 POST 也会回带真实 prod 值，但**不能为此去 POST**（通过即真提交）。

### 账号级单并发槽：跨进程互斥（2026-10-22 事故与修复）

平台这个接口**每账号只有 1 个在飞**，而本仓的 prod 查询散在多个进程（MCP 常驻服务、`campaign_intel prod-first`、`super_build`、`prod_bucket_scan`、`prod_watch`、一次性脚本）。Redis 退出后跨进程互斥曾一度丢失，只剩 MCP 进程内的 `asyncio.Lock` ⇒ 进程间互不相识。

事故形态（实测，不是推演）：另一会话的 prod 队列脚本卡在 `58jgRYWX` ⇒ 账号槽被占 ⇒ 本会话查询全部拿到空体、空转到 800 s+（`vROYv3EA` 实测 1499 s 才出数、`d5K9RAMx` 593 s）⇒ **杀掉那个作业后同一条立刻出数**。另一面：`check_correlation` 原本轮询上限 3600 s，一个卡死的 alpha 能把整账号堵一小时。

| 修复点 | 做法 | 位置 |
|---|---|---|
| 跨进程互斥 | 文件 token `logs/_dblock/correlation.lock.json`（`O_CREAT\|O_EXCL` + TTL 自愈 + 按 pid 回收死持有者）。拿不到就 **fail-fast 返回 `correlation_busy`**，不排队、**不降级放行** | `src/wqb/correlation_slot.py`（`LOCK_NAME` / `DEFAULT_TTL_SEC`=**600**，须 > 单次最长持锁 ≈ 窗口 240 + 台阶 30 + 抖动） |
| 两级锁顺序 | **先**进程内 `asyncio.Lock`，**后**跨进程文件锁——顺序不可换（`db_write_lock` 把同 pid 再 acquire 当**续约**，不是互斥） | `brain_mixin_transport._try_acquire_brain_correlation_lock` |
| 缩短占槽窗口 | 轮询上限 **3600 → 900 → 120 → 240 s**（锁覆盖整个窗口：窗口多长，单次调用就占账号级单槽多久）。**2026-10-28 从 120 回调 240**：一次正常计算 180–200 s，120 比它还短 ⇒ 每条真实查询都必然 `pending`、再叠 195 s 冷却才算拿到值。超时仍按 `pending` 返回（不缓存、不判死） | `WAIT_THRESHOLDS["prod_corr_timeout_s"]` = 240，守护测试比对源码常量 `_PROD_CORR_WAIT_S` |
| 两种锁分文件 | 写库锁 `dbwrite.lock.json` 与相关性锁 `correlation.lock.json` **必须分开**：TTL 不同，共用一个文件会让短 TTL 的写锁回收长 TTL 的相关性锁 token（两个进程同时自认持有）。`_prune_expired` 已改为**按文件名精确回收**，不再扫全目录 | `src/wqb/db_write_lock.py` |

**纪律**：任何要打 prod 端点的**新工具**都必须 `with wqb.correlation_slot.slot(...)`；拿不到槽就 fail-closed 立即返回并提示稍后重跑。**不要自建第二把锁、也不要因为"我只是查一次"而不拿锁**——那正是本次事故的成因。

**2026-11-17 补（残留锁 / busy 分因）**：`acquire` 的 busy 有三种，处置**完全不同**，旧实现全塞进一个
`busy=True` ⇒ 调用方只能一律放弃：

| `reason` | 含义 | 正确处置 |
|---|---|---|
| `cooldown` | 上一轮计算刚结束、平台仍占槽；`retry_after` 是**已知时长**（195 s 或平台 Retry-After） | **等它到期再抢**（`super_build` 的 prod 闸据此在窗口内等待，最多 3 轮） |
| `token_busy` | 另一个**存活**进程持有互斥 token（附 `holder` = pid/tag/alive） | fail-fast、不排队；日志带 pid/tag 便于定位 |
| `platform_unavailable` | 账号级熔断中（连续 pending） | 直接放弃 |

实测事故：`super_build.py submit` 首跑 `attempts=0` 退出，日志只说"被其它进程占用"，真实原因是
`correlation.cooldown.json` 里一条 195 s 冷却（写入进程 pid 已死）——人工等 TTL 到期重跑即成功。
顺带加固：冷却标记**脏值自愈**——半写/非 JSON、或 `until` 超过 `max(195s, env)×3`（时钟跳变 / 被手改的
远期值）一律退役为 `.stale` 并返回 0（`clear_cooldown` 也改为改名退役，不再 `unlink`，避开 safe-delete
守卫且可追溯）。回归：`tests/unit/09_core/test_corr_slot_stale_cooldown_20261117.py` +
`tests/unit/05_submit_quota/test_super_build_prod_gate.py::test_probe_waits_out_known_cooldown_instead_of_giving_up`。

**2026-11-17 补（伪冷却：没算过也写 195 s）**：残留锁的**上游来源**同一天定位到了——

| 项 | 实测 |
|---|---|
| 谁在占槽 | `WorkBuddy/Claw` 面板「自动终验」`picksAutoVerify`（`panel_ui_js_cand.py`，`PICKS_AUTO_THROTTLE_MS = 30 min`）→ POST `/api/refresh-corr` → `wq_prod_backfill.py --alpha <id>`，slot tag `prod_backfill(<id>)` |
| 现场 | 08:36:41 acquire `prod_backfill(QP02jR9w)` → 08:37:02 release，**持槽仅 21 s**，却写满 195 s |
| 为什么是错的 | 一次真实 prod/self 计算平台侧 **180–200 s**；21 s 拿到值只能是**既有值直读**，账号槽根本没被占用 ⇒ 冷却纯属自伤：每 30 min 有 3.25 min 伪冷却，提交首跑正好撞上 |
| 修法 | `release()` 按**持槽时长**自查：`seconds` 缺省且持槽 < `WQB_CORR_MIN_HOLD_FOR_COOLDOWN`（60 s）⇒ 跳过冷却；真算过的调用必然在槽里等 ≥180 s，自动过阈值 ⇒ **阈值只能放过"没算过"的，不会放过"算过"的**。显式 `seconds=` / `cooldown=False` 的调用点语义不变（调用方优先） |
| 可观测 | 每次释放追加 `logs/_dblock/correlation.cooldown.audit.jsonl`（`action`/`tag`/`held_s`/`cooldown_s`）——下次"谁占的槽"一眼可查，不必再逆向 |

回归：`tests/unit/09_core/test_corr_slot_short_hold_20261117.py`（8 例：21 s 不写 / 200 s 照写 /
`env` 阈值可覆盖 / token 不可读时保守回退旧行为 / 显式 `seconds` 优先）。

### 2026-10-28：把「14 小时只出 56 个数」拆成四件可修的事

实测（14 h、1,020 次 busy 拒绝、117 次真正拿到槽）：槽位占用 6,988 s，其中**成功计算只有 ~16.6 min**，
其余是 195 s 冷却与超时空转；中位 10 s / p90 45 s / 最大 117 s，**成功率 48%**。

⚠ **2026-10-28 更正这组数的读法**：它是**被 120 s 窗口截断**的幸存样本——超过窗口的计算
一律记 `pending`、从不进入"成功耗时"，所以「最大 117 s」只证明窗口是 120 s，**不能**证明平台
够快。一次正常的平台计算实为 **180–200 s**（用户口径）；「中位 10 s」那半是"一个 GET 就拿到
既有值"的预读命中，而**真实计算那一半在旧窗口下几乎全部失败**。窗口已据此改 240 s
（守护：`test_prod_corr_window_covers_normal_platform_compute_time`）。

根因不是"平台慢"，而是四件事叠在一起（逐条可用 `python tools/probe/corr_timing_report.py` 复盘——
本次数字取自 2026-10-28 对 MCP 服务日志 + `alpha_corr_cache` / `correlation.cooldown.json` 时序的取证，
该日志随后已被轮转清理，**原始行不可再调**，故此处只留结论；新打点落盘后按报告工具自行复算）：

| 层 | 旧行为 | 现行为 | 开关 |
|---|---|---|---|
| **冷却按结果分流** | 无条件写 195 s（连"一个 GET 就拿到既有值"也罚 3 分钟） | `success` 只留 `settle`（5 s）；`pending` 写平台 `Retry-After`（≤195）或 195；4xx 终态 / 异常**不写** | `WQB_CORR_SETTLE_SEC` / `WQB_CORR_COOLDOWN_SEC` |
| **inflight 侧车** | 同 alpha 的第二个调用照样去抢锁、照样触发 | 开轮询即标记 `correlation.inflight.json`；同 alpha 非 refresh 调用**只预读等待**（缺省 25 s），等不到返回 `busy + inflight=true`，**不二次触发**；`pending` 保留标记、其余（**含异常/取消路径**，2026-11-10 修）清除；读改写由 `correlation.sidecar.lock.json` 保护原子性 | `WQB_CORR_INFLIGHT_TTL_SEC`（300） |
| **同 alpha 等待** | 锁被同 alpha 占着也立即 busy | holder 恰为同 alpha ⇒ 等 `WQB_CORR_JOIN_WAIT_SEC`（25 s）内的预读值（`same_alpha_join`）；refresh 保持 fail-fast | `WQB_CORR_JOIN_WAIT_SEC` |
| **账号级熔断（2026-11-10 新增）** | 平台停摆时每次调用各自空转 240 s，再叠 195 s 冷却 + inflight 残留 ⇒ 自我放大等待 | 连续 N 次 `pending` 写 `correlation.unavailable.json`；期间 `acquire` 与 `get_production_correlation` **直接短路**返回 `platform_unavailable` + `retry_after`，不抢锁不发请求；任一成功结果即清除 | `WQB_CORR_UNAVAILABLE_STREAK`（3）/ `WQB_CORR_UNAVAILABLE_SEC`（600） |
| **打点与报告** | 只有人读的一句话 | `[corr-t] {json}` 结构化打点 + `tools/probe/corr_timing_report.py` 汇总「时间花在哪 / 拿到值 vs 空手 / 谁在反复触发」 | 零平台请求 |

配套的**消费方默认值**也改了：`check_correlation(refresh=False)` 是缺省（48 h 权威缓存 → 预读
`is.prodCorrelation`，命中即返回、**零平台计算**），只有**终验**（`submit_inventory --refresh-all`、
`corr_check --refresh`、`check_corr.py --refresh`）才强制重测。预读值带 `provisional=true`
——平台存储值**测量时间不可知**，不得记成「刚测过」（会污染 48 h 保鲜判据）。

#### 2026-11-10 机制加固（审查报告 `reports/prod_corr_mechanism_review_20261110.md`）

- **peek 值落库唯一入口 = `tools/probe/prod_peek_ingest.py`**：读 `results/prod_peek_<id>.json` /
  `prod_wait_<id>.json`，以产物里的 `at`（**探测时刻**）作 `checked_at` 写 `set_corr_cache`，
  `source=prod_peek`（已登记词表）。此前三者之间**没有任何代码连接**，靠一次手工 SQL；
  正规写入口又用「写库时刻」⇒ 几天前的值今天写库就被当成 48 h 内新鲜实测。**禁止再手工 SQL 落库。**
- **来源分层**：`wqb.store.NON_REALTIME_SOURCES` = `manual / legacy / alphas_backfill /
  checkpoint_backfill / triage_local`。缓存命中若来自这些词**或根本没有 source**，
  `check_correlation` 会带 `provisional=true`，`_prod_gate` 补一次 `refresh=True` 真重测，
  重测后仍不可信则 fail-closed。`prod_peek` **不在**此列（它读的就是平台端点已算结果）。
- **唯一判据解析 = `wqb.prod_verdict.prod_verdict()` / `gate_allowed()`**：统一处理
  `provisional / from_cache / cached_at / stale / pending / busy / data_unavailable /
  platform_unavailable`，替换原先 8 份各自为政的拷贝。**缺值时 `passes=None`，调用方不得放行。**
- **fail-open 已堵**：`judge._eval_correlation` 缺值/异常改 `pass=False`（→ BLOCK）；
  `batch_submit_verdict` 检查 provenance 且 `PENDING` 不再写 `phase2_done`（否则永不再验）；
  `submit_inventory --snapshot-only` 不再强制 `fresh=True`，取数失败把 prod/self 置 None；
  `prod_saturation_gate` 缺值不再当 0.0 稀释 wall_ratio。
- **`set_corr_cache` 只在带来有效 prod/self 值时刷新 `checked_at`/`source`**：纯 records 更新
  不得把旧值「洗新」。`corr_age_hours` 统一按本地时区解释 naive 值再转 UTC 相减（修 aware+naive 误判 stale）。
- **`prod_wait.parse()` 不再扫直方图**：`max` 缺失即 None（旧实现会把 bin 上界/计数 n 当 prod）；
  peek 与带锁模式都识别 4xx / `data_unavailable` 终态立即退出；带锁模式去掉嵌套轮询。
- **单源读**：`get_alpha_corr_metrics`、`submit_queue._corr_checked_times`、
  `prod_first_screen.targets` 均优先权威表 `alpha_corr_cache`，缺条目才回落 `alphas`。
- **常量同源**：`0.7` → `config.PRODCORR_CEILING`；`48h` → `_corr_cache.CORR_FRESH_HOURS`；
  `240s` → `config.WAIT_THRESHOLDS['prod_corr_timeout_s']`（MCP 侧运行时真读，守护测试改为运行时断言）。
  `check_correlation` 新增 `timeout_s` 可覆盖单次窗口。

⚠ **刻意没做**：触发后立即释放锁、让轮询在锁外跑。锁覆盖轮询窗口正是当前正确性的来源
（同 alpha 等待靠 holder tag 识别、跨进程不重复触发靠同一把锁）；先放锁再轮询等于把
"账号级单并发"交还给平台去挡。要改这块需要先把 inflight 侧车升级为**权威的在飞登记**
（跨进程可见、含 pid 存活判定），再谈合并触发与等待——现在只做保守分流。

### 阈值与判定

- 平台**名义阈值 0.7**，但 **SUPER 判定只看 `result` 不看 `value`**：0.8094 / 0.8571 判 PASS，0.8938 / 0.9729 判 FAIL → 实际分界在 **0.86 ~ 0.89**。
- **我方铁律更严**：prod ≥ 0.7 **一律拒提**（`super_build.py` 已强制 probe + fail-closed；**无任何豁免入口**——原 `--allow-prod-above-07` 开关已于 2026-10-18 按用户判定「不合规」彻底移除）。REGULAR 同口径。
- **`PROD > 0.7` 未必 FAIL**：`N1QMJ10q` 0.7225 判 WARNING、`gJjnXv8g` 0.7864 成功 ACTIVE；同批 `omqxJmO6` 0.7255 却 FAIL → **判定非纯阈值，以平台实测值为准**（`check_correlation` 读 prod；`submit_verdict` 看模拟层）。

### 两个必知的失效场景

1. **prod 值会腐烂，必须当日实测**：实测 0.6678→0.981、同族顶高 0.5836→0.9805、`le8Y68K2` 0.6929→0.9932、`3qX6wLJQ` 库内 0.5171→实测 0.9895。
   2026-10-21 再添两例（**14 天尺度**）：`58gp1wdz` 库内 0.6738（`verified_at` 10-17）→ 实测 **0.9868**；`pw5RbrYX` 库内 0.5857 → 实测 **0.9000**。
   → 筛查产出的是**排序队列**而非终局清单；**提交当日读 48h 内可信缓存即可直接过闸**（2026-11-14 用户明令），>48h / 无缓存才 `refresh=True` 复测；`get_submit_ready` 的 `READY` 只代表「**曾经**过闸」，`corr_stale=true` 的行一律当作未验证。
   ⚠ **队列读数只认 `submit_ready` 表**：`ledger_kv` 里那份旧副本（2026-10-31 实测 KOR **72** 行 READY）
   **已不再被 `get_submit_ready` 读取**，是审计遗留物、没有生命周期；同一时刻真表只有 **1** 行（`LLZ6wZO2`）。
   两个数字差 71 倍时**以表为准**——别再翻 `ledger_kv` 找队列。
2. **本地 SELF 两个失效场景**：① 系统性低估（`N1QMJ10q` 本地 0.3972 → 平台 0.5463；`6XrJ5OvE` 本地 0.6732 vs 平台 prod 0.996）；② 对"新提交孪生体"**结构性假阴性**（`vRkAO9Xd` 本地 0.229 vs 平台 0.8392，根因是 OS PnL 池不含刚提交 alpha）。
   → **同族候选不要用本地 SELF 判活**，改用 403 视图逐颗实测。

- **SELF 极低 ≠ PROD 低**：`A1loLl2e` SELF 0.034 但 PROD 0.7671。两闸衡量对象不同（SELF = 与账号既有 ACTIVE 相关；PROD = 与全平台生产池相关）。
- **小区 PROD ≈ SELF**：IND 两值几乎相等（0.7619/0.7622、0.7558/0.7557）→ 压一个必然带动另一个。USA 则是 **PROD 独立卡死 0.86**（SELF 降 PROD 不动）。

**USA 侧分布实测（2026-10-23，n=92 已测 prod）**：`[0.8,1]` **44.6%**、`[0.7,0.8)` 12.0%、`<0.7` 仅 43.5%（其中 `<0.5` 只有 1 颗）
⇒ **分布中心在闸门外，是整体问题不是尾部**。且 **「数据集冷门 / alphaCount 低」不能预测 prod**：
`web_traffic_engage`（RA 全过率 80%）prod **0.9908**、`other143`（59.6%）0.9206、`institutions18`（30.4%）0.9636
⇒ 选集要问「机制是否经典异象」并先跑 prod 探针（详见 `03_region_dataset.md` §9）。
来源：`reports/usa_mining_history_review_20261023.md` §1/§4/§5。

---

## 5. 提交形态与预检

### submit_alpha 四形态

| # | 形态 | 处置 |
|---|---|---|
| ① | 200 + IS passed | 明确通过 |
| ② | **201 async** | 4 min 未翻状态**必须补发 POST**（否则悬空滞留队列） |
| ③ | 200 空体 | 未知，**必须轮询** |
| ④ | **403** | 零成本，回带**全量 checks**（含真实 PROD/SELF）；**这是被拒时才有的结果，不能当预检用**（通过即真提交） |

**判定只认轮询 `status=ACTIVE`。**

### 关键区别

- `GET /alphas/{id}/submit` **恒返回 404 + 空体**（对已 ACTIVE 与未提交都一样）→ 处女候选恒 `UNVERIFIABLE`；**403 只可能来自 POST**。
- **`submit_verdict` 的"提交层唯一权威"名不副实**（GET 路径恒 404），但**零成本定位卡点仍可用**：它在 404 响应里给出模拟层完整 checks + Failed RA/PPA 计数 → 不必真 POST 即可定位唯一卡墙。

### 提交前必做

- **★★ prod 无需本地单独复测（2026-10-08 用户裁定；2026-11-14 用户明令「48h 内不用 refresh 直接提交」重申）**：`prod_gate` 节点默认 `check_correlation(refresh=False)`，命中 48h 内 `alpha_corr_cache` 且 `provisional=False` 即过闸；只有缓存过期/缺失/不可信才回源（拿不到即 fail-closed，这正是 `correlation_busy` 的成因）。
  ⇒ 提交前那次独立的 `check_correlation(refresh=True)` 属**冗余动作**：它与节点抢同一个**单并发**队列，反而更容易把端点挤爆。**跳过它不降低安全标准**（硬闸在节点内）。
  ⇒ 处置：**用户确认后**执行 `workflow_submit_alpha(confirm_submit=True)`（真提交、**不可逆**）；若节点报 `correlation_busy`，**间隔重试**（≥90s），**切勿改参数或降标准**。
  ⚠ `WQB_PROD_GATE_REFRESH=1` 是强制回源开关，**用户未要求不得设置**。仅当**事先排序/取舍**多个候选、或缓存 >48h 时，才需 `check_correlation(refresh=True)`。
- **name + description（≥100 字，house style ~1200 字）必须预先写好并回读**——空描述会被平台**静默丢弃**（POST 返回 201 但被丢）。
- **REGULAR 用 `set_alpha_properties`，SUPER 必须裸 PATCH**（`set_alpha_properties` 对 SUPER 必 400）。
- ⚠ **`set_alpha_properties` 是全量覆盖接口不是局部更新**：曾清空 **115 颗 ACTIVE 的 name** 并覆写 description。改单个属性用**最小字段 PATCH** `{"tags":[...]}`，**改前先 dump 快照**。

---

## 6. SuperAlpha（SA）

| 项 | 规则 |
|---|---|
| 硬前置 | **ACTIVE REGULAR ≥ 10**（平台报 `At least 10 component alphas are required`，异步校验） |
| 组件不足时 | select 失败回得极快 → 放宽 self_gate 的梯度扫描成本 ≈ 0 |
| **self_gate 是首要放宽旋钮** | 0.65 三连废；放宽到 **0.70 十颗全过**；0.85/0.95 产物与 0.70 完全一致 → **0.70 已是全收，再放宽无收益** |

**成功配方模板**：
```
<REGION>/<主universe>/d1/trunc0.08/maxTrade OFF + dec10 + nu=SUBINDUSTRY
selection: (1+0*(prod>0))*(1-prod)*(self<0.6)*(to>0.01)*(to<0.6)
combo:     线性 1-maxCorr
```

**MEA 的 SUPER 通道已关闭**（`region=MEA type=SUPER` → 400 `Region MEA is not available`）。

### 6.1 ★ SA 提交准入分级（2026-11-18 用户定案，取代「三条件硬拦」）

旧做法把「S≥5 ∧ F≥5 ∧ prod≤0.65」当唯一门槛，导致闸门既是排序键又是准出闸：达不到就整颗不报，边际信息全丢。新判据把**平台行为**与**自设偏好**分层，自设层降级为汇报。

```
红线   = prod >= 0.70 或 IS checks 有 FAIL                     -> REDLINE    一律硬拦，不报
准入   = S >= 5.0 且 F >= 5.0 且 prod <= 0.65                    -> ADMIT      直接进提交建议
可汇报 = prod <= 0.68 且区内 Pareto 不劣：
         S >= 区内最强 S × 0.95 且 F >= 区内最强 F × 0.95        -> REPORT     可汇报，标注缺口
其余（过红线但无边际）                                          -> NO_EDGE    不报，仅留档
prod 未实测                                                    -> UNMEASURED 待测，不判死
```

判定顺序 **REDLINE > ADMIT > REPORT > NO_EDGE**。

**三条必须遵守的口径**：

1. **红线不可降级**。`prod ≥ 0.70` 是平台提交校验（`check_correlation` 返回 `passes_check=false`），不是我们的策略分支——放宽只会得到一次必然被拒的 POST。IS checks 的 FAIL 同理。这一层永不出现在「可汇报」名单里。
2. **区内基线取 maxS / maxF 两个独立值**，允许来自不同 alpha。实测 IND 最强 S 属 `pw52P3jb`（5.43）、最强 F 属 `QPbjxMYw`（5.74）；若合并成「最强那一颗的 S 和 F」，基线会虚高，REPORT 永久无法命中。
3. **「比昨天强」不能当判据**。2026-11-17 基准件 `pwa8mYvV`（GBR S5.05/F5.18/prod .6548）本身只是 3/3 的边缘件，而同账户存在 `KPg60XNp`（KOR S5.96/F7.50/prod **.5475**，11-15 提交）这种高一档的件。以低档件为靶会形成向下竞争，必须对**区内最强**比。

**判据的实际约束力（2026-11-18 首轮验证，9 颗候选）**：REDLINE 3 颗（`Jj8p9Zb2` .7360 / `d5axMLxx` .7311 / `qM7lKoYj` .7575）、UNMEASURED 4 颗、NO_EDGE 2 颗（`E5QEZrl1` S5.02 < 5.43×0.95=5.16）、ADMIT 0 颗、REPORT 0 颗。`E5QEZrl1` 在旧记里是「排序第一」，新判据下判 **NO_EDGE** —— 因为它 F 6.51 虽高，S 5.02 低于区内最强 7.5%，属横向替换而非升级。**这正是本判据要挡的东西。**

**工具**：`tools/super/sa_grade.py`（离线，零平台调用、零配额）。输入候选指标 JSON + 已 ACTIVE SUPER 基线 JSON，输出 `ADMIT/REPORT/REDLINE/NO_EDGE/UNMEASURED` 分级表；判据常量在文件头部，改判据只改那几行。

---

## 7. 点塔（Pyramid）

- **点亮定义 = 该塔下当前自然季度提交 ≥ 3**。每个自然季度首日计数清零（2026-10-01 实证：GLB 的 10 颗 ACTIVE 全是 Q3 提交，Q4 一颗不算）；`get_pyramid_alphas` 缺省返回当前季度，查上一季须显式传 `start_date` / `end_date`。旧版写的「90 天滚动窗口」没有代码实现，已更正。
- **唯一权威数据源 = 平台 `get_pyramid_alphas`**（按季度返回 region/delay/category 计数）。
- ⚠ **本地 `alphas` 表不能做塔级统计**（两次踩坑）：
  - 不可用 `datasets.category` 推塔归属——本地 KOR 47% ACTIVE 的 `category=None`，且塔归属来自平台 pyramid 匹配，与数据集 category **不等价**。
  - 不可用 `date_submitted` 判提交——该字段全库仅 **2.7%** 非空。
- **塔归属由表达式字段的 category 决定**，不是数据集名也不是数据集 category：`WjPPjVQd` 主信号是 shortinterest55 却挂 HKG/D1/PV（因表达式含 `volume`/`adv20`/`vwap`）。
- **Cluster Alpha 的 `pyramids = null`，不参与点塔**（徽章在 `classifications`，数值在顶层 `is.checks`）。
- **MEA 不在金字塔体系内**（212 格中 MEA 格数 = 0），提交不计点亮也无 multiplier。
- **已点亮塔不再优先提交 REGULAR**，其候选最多作 SA 组腿；优先提交归属**未点亮塔**的候选。

---

## 8. universe / 中性化合法档位

| 区域 | 合法 universe | 备注 |
|---|---|---|
| **IND** | **仅 `TOP500`** | 无档可换 |
| KOR | `TOP600` | CLUSTER_TEST limit = 1.0 |
| DEU | **仅 `TOP500`** | ⚠ **2026-10-06 实测更正**：`TOP300` 报 `Universe TOP300 is not available for instrument type EQUITY and region DEU` ⇒ **原记载「TOP500 / TOP300」有误**，DEU 无第二档位可换 |
| USA | `TOP500` / `TOP1000` / `TOP2000` / `TOP3000` | 降 PROD 首选 **TOP1000** |
| EUR | 6 档 | |
| GLB | `MINVOL1M` | |

- ⚠ **`TOP800` / `TOP1500` / `TOP2500` / `TOP5000` 均非法**（平台 400）。合法档实测：`TOP500`/`TOP1000`/`TOP2000`/`TOP3000`。
- ⚠ **JPN 不支持 `industry` / `sector` / `subindustry` 分组**（闸 2b 硬拒绝），cluster 变体线在 JPN 必被拒。
- **缩小 universe 可降 PROD 但非单调，必须逐档实测**（USA `N1QMJ10q`）：TOP3000 0.7225 → **TOP1000 0.6149 ✅** → TOP500 0.5422（FAIL，IS 被摧毁）→ TOP2000 反升 **1.0**。

---

## 9. 幽灵算子 / 幽灵字段

### 幽灵算子（10 个，取模板骨架前必查 ghost advisory）

```
group_normalize, sigmoid, ts_decay_exp_window, ts_entropy, ts_max,
ts_median, ts_min, ts_min_max_cps, ts_percentage, ts_skewness
```
外加 **`negate`**（合法替代 `multiply(-1, X)`）。
→ 用了整批 ERROR/CANCELLED。**权威以本仓 `operators_verified.json`(103) + KB advisory 为准，论坛口径不可信**。

### 幽灵字段

- **幽灵字段 alpha 在提交层 `COMPILE_ERROR`，根本不可提交**（旧认知"可提交但不可复现"是错的）：
  `COMPILE_ERROR: Attempted to use unknown variable "change_6m_rating_revision"`。
- ⚠ **不可用 DB `fields` 表判定字段存活**：幽灵字段在 `create_multi_simulation(validate_fields=true)` 报 unknown 并整批取消，但 fields 表仍标有效。
  → **库存盘点必须以 `validate_fields` 或实跑探针验字段**。

---

## 10. 其他平台硬约束

- **`color` 是硬枚举仅 5 值**：`GREEN` / `BLUE` / `RED` / `YELLOW` / `PURPLE`（ORANGE/TEAL/GRAY 一律 400 `"X" is not a valid choice.`）。
- `tags` 与 `name` 零约束（tags 100 字符/30 个、name 256 字符均接受）。
- **平台可控属性只有**：name / color / tags / hidden / favorite / regular.description。
- **已 ACTIVE 的 alpha 不可重复提交**（`status=ACTIVE` 且 `GET /submit` 返回 404）。
- **DECOMMISSIONED 由 WQ 单方面裁定，顾问无退役入口**：`retire/decommission/deactivate/...` 全 404；`PATCH {"status":"DECOMMISSIONED"}` → 200 但**服务端静默忽略**。`hidden` ≠ 退役（仍 ACTIVE、仍在生产 book 跑）。→ 只能打 `RETIRE_<YYYYMMDD>` 标签。
- **`WeightFactor` 唯一入口 = `GET /users/self/consultant`**（含 weightFactor/valueFactor/meanProdCorrelation/meanSelfCorrelation）。
- **平台列表接口每个 status 过滤各限 1000 条**（UNSUBMITTED 拉到 1100 即 400），超出只能逐条 GET。
- **PPA 决定性闸 = `MATCHES_THEMES`**（WARNING = 未命中即不能走 PPA，重试无效，只随主题轮换翻转）。`PURE_POWER_POOL_THEME` 命中条件是"区域组"不是 dataset category。
- **`CLUSTER_TEST` 门槛**：默认 ≥ 1.58；**KOR / JPS / TWN / HKG / IND / GBR / DEU ≥ 1.0**。判定用 check 自带 `limit` 而非按区域名硬编码。
- **OS 数据可得性**：**只有 USA 有 `os.sharpe`**（其余 9 区 73 颗全 null）。OS 全量指标只在详情 `GET /alphas/{id}` 的 `os` 块，列表接口只带 `osISSharpeRatio`。

---

## 11. investability 是第 2 号门槛（仅次于 fRA=0），不是事后参考项

**这条闸不在平台 RA check 里，平台不拦，但它是「Sharpe 真不真」的分水岭。**

`investability_sharpe`（`invest_S`）只统计**落在可投资权重上限内的那部分 PnL**。若信号集中在
流动性差/权重受限的尾部股票上，S 可以很高而 invest_S 接近 0 ⇒ **Sharpe 是构造出来的，不是可交易的**。

**判据（人工闸）：`invest_S / S ≥ 0.70`。**

**USA 实测（2026-10-28，9 颗全部 fRA=0 的候选）**：

| 族 | 代表 alpha | S | invest_S | 比值 | 判定 |
|---|---|---:|---:|---:|---|
| `insider_trx_matrix` / `insider_matrix` | d5KPPrxx | 3.13 | 0.25 | **0.080** | 否 |
| 同上 | 88v2XRm7 | 2.73 | 0.34 | **0.125** | 否 |
| 同上 | E56XEpV9 | 2.21 | 0.07 | **0.032** | 否 |
| `analyst_consensus` | wpbagVMY | 2.03 | 2.20 | **1.084** | **可通过** |
| `ai_equity_alpha` | zqrgna91 | 2.67 | 2.70 | 1.011 | 可通过 |

⇒ **8/9 颗被这条闸砍掉**，其中包括全库 Sharpe 最高的 3.13。**insider 族（`insider_trx_matrix`、
`insider_matrix`）是 invest 重灾区（0.03–0.12），它的高 Sharpe 一律不可信**。
⇒ 相反 `analyst_consensus` / `ai_equity_alpha` 天然 0.95–1.08，是「可投资性」安全族。

**作业纪律**：
1. 候选排序固定为 ① `failed_ra_count == 0` ② `invest_S / S ≥ 0.70` ③ 塔位合规 ④ 互相关/prod。
   **指标（Sharpe/fitness）只排第 5** —— 先按 Sharpe 挑会稳定地选中 invest 已死的 insider 族。
2. `batch_get_alpha_metrics` 是唯一直接返回 `investability_ratio` 的入口，一次 ≤20 颗。
3. 判死要落库：`python tools/submit_queue.py retire --region USA --status DEAD --alpha-id <id> --note "INVEST_DEAD: ratio=..."`（**单颗一次，`--alpha-id` 不是 nargs**）。

### 11b. investability 是「数据集族属性」，不是单颗运气 —— 可用它做选集先验

**2026-10-28 新增实测（`earnings_chart_dl` 8 颗，EARNINGS 塔，同一骨架）**：

| alpha | 字段 | S | invest_S | 比值 |
|---|---|---:|---:|---:|
| QPvLvee5 | close_return_quantile_1_1day | 1.61 | 1.39 | **0.863** |
| 2rAbAEPP | open_return_quantile_1_1day | −2.11 | −1.82 | **0.863** |
| YP1G1Zdl | (A 组门控变体) | 1.51 | 1.19 | **0.788** |
| gJeEevvg | prob_quantile_2_bucket_1_5day | 0.34 | 0.26 | 0.765 |
| akKqKJ35 | prob_quantile_2_bucket_1_20day | 0.23 | 0.21 | 0.913 |
| LLMAMeee | (A 组门控变体) | 0.28 | −0.04 | −0.143 |
| xAr0rMMN | (A 组门控变体) | 0.39 | −0.12 | −0.308 |
| YP1G1ZZR | prob_quantile_2_bucket_1_50day | −0.26 | −0.27 | 1.039 |

**同族内 5/8 颗比值 ≥ 0.76**（含最强的两颗 0.863）⇒ **该族整体可投资性健康**，瓶颈不在 invest 而在 fitness。
对比 insider 族 9 颗里 8 颗 0.03–0.12 ⇒ **invest 比值在族内高度一致，是数据集/机制层面的属性**。

**推论（可直接用于选集）**：
- 某族一旦实测出 `invest_S/S < 0.3`，**该族后续候选不必逐颗复测，整族视为 invest 死**；
- 某族实测 ≥ 0.75 ⇒ 后续候选可按常规口径（fitness/2Y/相关性）继续推，不必反复回测 invest；
- 只有**跨族新机制**才需要重新实测（`batch_get_alpha_metrics` 一次 ≤20 颗，成本低）。
- **异常值要看符号**：比值落在 [−1, 0] 说明 invest_S 与 S 反号（信号主要集中在不可投资部分且方向相反），
  比「接近 0」更糟（实测 LLMAMeee −0.143 / xAr0rMMN −0.308，都是门控稀释后的弱信号）。

## 12. `LOW_FITNESS` 的直接反解式：`turnover ≤ returns × Sharpe²`

`fitness = Sharpe × sqrt(|returns| / max(turnover, 0.125))`，令 `F ≥ 1` 反解 ⇒

> **`turnover ≤ returns × Sharpe²`**（当反解值 < 0.125 时改用 0.125 作为分母下限）

**这是判断「这颗候选还能不能救」最快的一步**：把已有的 S / ret / tvr 代进去，看 tvr 需要降到多少。
若需要的 tvr 已经低于信号自身的换手下限（信号更新频率决定），**判死，不要浪费仿真槽**。

**USA 实测校准（2026-10-28，`earnings_chart_dl` 族）**：

| alpha | S | ret | tvr 现状 | F 现状 | F≥1 需 tvr ≤ | 结论 |
|---|---:|---:|---:|---:|---:|---|
| 2rAbAEPP 取反 | 2.11 | 9.81% | 0.7194 | 0.78 | **0.4368** | 可救（只差换手）|
| QPvLvee5 | 1.61 | 5.34% | 0.6292 | 0.47 | **0.1384** | 不可救（需压到 0.14，信号是日频）|

**关键推论**：**高换手 alpha 很难过 fitness 闸**。turnover 0.6+ 在 S=1.6 时要求 returns ≥ 15.4%
（0.6×1.6²），S=2.1 时要求 ≥ 26.5%。⇒ **turnover > 0.45 的候选，只有 returns ≥ 11%（S=1.6）或
≥ 20%（S=2.1）时才有机会，否则在 fitness 这一项上基本已判死，不必等回测就能预筛**。
反过来，`hump`/长平滑/deep decay 把 turnover 压到 0.05–0.2 之后，fitness 会突然变得容易达标
（这也是结论 20 里 `hump=0.0001` 使 fitness 完全由 returns 驱动的原因）。

**排查顺序**：看到 `LOW_FITNESS` 先算 `ret × S²`：
1. `ret×S² ≥ 0.45` ⇒ 换手偏高，但**先看 margin**（见 §12b）：margin < 5 bps 就直接判死，
   否则走**横截面筛选**（只留强信号名）而非 decay/hump/平滑；
2. `0.2 ≤ ret×S² < 0.45` ⇒ 需同时抬 Sharpe 或抬 returns，要先换结构（分组轴/中性化）；
3. `ret×S² < 0.2` ⇒ **结构性判死**，换字段/换数据集，不要再调参。

### 12b. ★ 降换手有两类杠杆，只有一类能救 fitness（Wave 119 实证修正）

上表的反解式只说明「tvr 出现在分母」，**并不说明压低 tvr 就能抬 fitness**。要看压 tvr 的代价：

| 杠杆 | 算子类别 | 对 turnover | 对 returns | 对 margin (ret/tvr) | 对 Sharpe | 对 fitness |
|---|---|---|---|---|---|---|
| `decay`（设置层） | 时间衰减 | ↓ | ↓（等比） | **≈不变** | 略↓ | **救不了** |
| `hump` | **Time Series**：限制输入的**变化量级** | ↓ | ↓（等比） | **≈不变** | 略↓ | **救不了** |
| `ts_mean` / `ts_decay_linear` 平滑 | 时间平滑 | ↓↓ | ↓↓ | ≈不变 | **↓↓** | **反而更差** |
| **横截面筛选**（`trade_when(rank(...)>阈值, α, -1)`、`bucket` 只留极端档） | **改变组合构成** | ↓ | ↓（只砍掉非极端名） | **↑（真提升）** | 视信号质量 | **唯一可能救** |

⚠ **`hump` 不是「置零弱势股」，别把它当 margin 杠杆**。官方定义
（`docs/reference/operators_catalog.json`）：`hump(x, hump=0.01)` category = **Time Series**，
description = *"Limits amount and magnitude of changes in input (thus reducing turnover)"* ——
它限制的是**同一条持仓的时间变化量**，与 `decay` 同类，**买的还是同一批股票，只是换手慢一点**。

**实测证据（`earnings_chart_dl` / `open_return_quantile_1_1day` 取反，USA TOP3000 D1）**：

| 配置 | S | ret | tvr | F |
|---|---:|---:|---:|---:|
| decay 5（原始） | 2.11 | 9.81% | 0.7194 | 0.78 |
| decay 10 | 1.86 | 9.28% | 0.5276 | 0.78 |
| decay 20 | 1.60 | 8.20% | 0.3834 | 0.74 |
| ts_mean(5) @decay20 | — | — | 0.2611 | 0.48 |
| ts_mean(22) @decay20 | 0.85 | — | 0.1116 | 0.47 |
| ts_mean(66) @decay20 | 0.54 | — | 0.0642 | 0.23 |

turnover 降了 47%（decay5→20）而 **fitness 纹丝不动**；换成平滑后 turnover 降 85%，fitness 反而从 0.78 跌到 0.23。

**根本原因**：`fitness = S × sqrt(ret/tvr)`，而 `ret/tvr` 就是 **margin（每单位交易额赚多少）**，是**信号本身的属性**。
decay / hump / 平滑只是把同一条持仓序列按比例缩小（交易和收益同比例降），持仓股票没变 ⇒ margin 不变；
平滑还额外引入滞后 ⇒ Sharpe 降。
⇒ **`fitness ≈ Sharpe × sqrt(margin)`。fitness 低只有两个真因：① margin 太低 ② Sharpe 太低。
任何「只是让同一批股票换手慢一点」的杠杆（decay / hump / 平滑）都不改这两个量，永远是无效动作。**

**正确动作**：fitness 卡住时先看 `margin`（`get_alpha_details` 的 `metrics.margin` 直接给，
过闸 alpha 常规 5–15 bps）：
- margin < 5 bps ⇒ 信号本身赚不动交易成本 ⇒ **判死换字段**，不要调 decay/hump/平滑；
- margin ≥ 5 bps 但 fitness 低 ⇒ 问题在 Sharpe，走换分组轴/中性化/换结构；
- 想提 margin 只能**改变组合构成**：横截面只留强信号名（`trade_when` 阈值 / `bucket` 极端档），
  持仓数变少但每仓更值钱 —— 这是唯一「少交易但每次更值钱」的路线。
  代价：持仓集中度上升 ⇒ 需同时盯 `CONCENTRATED_WEIGHT` 与 `LOW_SHARPE`。

## 13. VECTOR 事件型字段：裸 `vec_avg` 会同时撑爆换手与集中度

`earnings6`（EARNINGS，52 字段 **100% VECTOR**，"daily snapshots of international corporate events"）
在 USA TOP3000 D1 实测 8 条（EPS surprise = `ern6_actual_eps` − `ern6_estimated_eps`）：

| 表达式骨架 | S | turnover | CONCENTRATED_WEIGHT | fRA |
|---|---:|---:|---:|---:|
| `rank(subtract(vec_avg(actual), vec_avg(est)))` | −0.82 | **1.1100** | **0.4406** | 6 |
| `ts_zscore(同上, 252)` | −1.06 | 1.1094 | 0.4425 | 6 |
| `ts_rank(同上, 252)` | −0.56 | 1.1290 | 0.4220 | 6 |
| `ts_rank(同上, 504)` | −0.77 | 1.1157 | 0.4220 | 6 |

三处同时爆表：`HIGH_TURNOVER` 1.11–1.13（上限 0.7）、`CONCENTRATED_WEIGHT` 0.42–0.44（上限 0.10，超 **4.4 倍**）、`LOW_SHARPE`。

**根因**（不是权重写法问题）：`vec_avg(F)` 对事件型 VECTOR 的聚合 =
「当前事件窗口内所有事件的均值」。窗口内容逐日变化（新事件进入、旧事件滚出）
⇒ 聚合值**每天整体重算**，不是静态快照 ⇒
① turnover ≈ 1.1（等于每天把仓位换一遍）；
② 只有近期有事件的名字存活 ⇒ 横截面过薄 ⇒ 单名权重爆表。

**修法**：`ts_backfill(vec_avg(F), 126)` 把事件值结转成慢变可持有序列
（与 02_platform_gates 结论 27 的冠军栈同款）。
**判据**：任何 VECTOR 字段进入 `ts_*` / `rank` / `group_*` 之前，
必须「先 `vec_avg`、再 `ts_backfill`」——**只做 `vec_avg` 不够**。

**连带纪律**：`CONCENTRATED_WEIGHT` 首次出现在诊断里时，先查**覆盖率与每日存活名数**，
不要先怀疑权重写法。稀疏面板（事件集 / 低覆盖集）的集中度问题靠调算子救不回来，得换数据集。

**数据集级附注**：`earnings6` 的 52 个字段里只有 4 个是数值信号
（`ern6_actual_eps` / `ern6_estimated_eps` / `eps_change_percentage_value` / `eps_change_absolute_value`，
后两者 alphaCount 仅 2/3，拥挤度近乎为零），其余 48 个是 URL / 口令 / 电话 / 时区 / 交易所等元数据。
`earnings7` 同类（38 字段全 VECTOR，同样以元数据为主）。
⇒ 「低 alphaCount + 低拥挤」不等于「可挖」，**先剔除元数据字段再评估字段池厚度**。

## 14. ★ prod 读数的可信度分级：「指标全闸」不蕴含「可提交」（2026-10-31 KOR 三例实证）

**三个独立案例，形态完全相同**——`is.checks` 全 PASS（`fail=[]`）、纯格、ATOM，然后 prod 判死：

| alpha | 区 | S | prod 实读 | 曾被记成的「唯一卡点」 | 结局 |
|---|---|---:|---:|---|---|
| `leA22za2` | KOR | 1.92 | **0.8377** | 覆盖率 / 自设约束 | D0-P 判死 |
| `d5WmEarw` | KOR | 1.99 | **0.8395** | 同上 | D0-P 判死 |
| `leAk66xx` | KOR | 1.77 | **0.8711** | **「只差用户约束 4（2018 前无数据）」** | D0-P 判死，**约束之争就此 moot** |

> **铁律**：向用户请求任何「放宽覆盖率 / 放宽自设约束」之前，**先把新鲜 prod 取到手**。
> 缺的那一道闸往往是**还没去取的那一个数**，不是已经知道的那条限制。

### 14.1 prod 读数可信度分级（从高到低）

| 档 | 形态 | 可否作闸 |
|---|---|---|
| A | `check_correlation(refresh=False)` 命中 48h 内 `alpha_corr_cache`，来源可信（`provisional=False`），或 `refresh=True` 实测，`stale=false`、有源 | ✅ **可直接作提交判定，无需回源** |
| B | 缓存命中但 `provisional=True`（预读值 / `NON_REALTIME_SOURCES` / 无来源标记） | ⚠ 只许证伪；节点自动补一次 `refresh=True` 才能放行 |
| C | `stale=true`（> 48h） | ⛔ 不可作闸（prod 漂移猛，48h 作废） |
| D | `prod_corr_source=NULL` / `corr_checked_at=NULL`（**无源旧值**） | ⛔ 不可作闸，等同未知 |
| E | 文档 / 台账里手写的 prod 值 | ⛔ **可被实测证伪**，见下 |

**E 档实证（KOR shortinterest38）**：`mLmGQEq9` 文档记 **.6011** → 实测 **.935**；
`E5pjx9q0` 文档记 **.6002** → 实测 **.8105** ⇒ 路线图所称「真正可承重 2 颗」**全灭**。
**D 档实证**：同族 **16 行**标「prod clean」但两个来源字段全 NULL。

### 14.2 本地缓存 < 0.70 ≠ prod clean（库存不是金矿）

KOR 队列 **19 行**本地 prod 落在 **.57–.70**（看着全都过线），
**同族新鲜读数却是 .81–.935**。⇒ 库存里任何 `prod < 0.70` 的行，
**必须先做族级新鲜核对**，否则会把死族当「零配额就能扩池」的金矿。

### 14.3 族级直方图：一次平台读判整族

`[0.7,0.8)` 桶 **n ≥ 1 ⇒ 整族必死**（不是「这一条不行」）：
`leAk66xx` n=5 / `pwdoY39V`（pv106 唯一过闸）n=1 / shortinterest38 族 n=5。
⇒ 族代表测一次即可决定整族去留，**不必逐条费 prod 槽**
（与 `wq-window-valley-break-prod-wall` 的「n=0 可救 / n≥1 必死」同一判据）。

### 14.4 刀锋档建议复核（非强制，2026-11-14 用户明令后降级）

prod 落在 **.6886–.6958**（余量 **.004–.011**）的候选可**建议**用户复核，但 48h 内可信缓存仍按现值直接过闸，不得擅自 `refresh=True`。
另：prod 单槽是**账号级、跨会话竞争**（`holder: corr:get_production_correlation(...)`，retry 240s）
⇒ 被占时读 `last_known`、不重复触发；**仿真槽独立于 prod 槽**，prod 被占不影响派波。

## 15. `submit_ready.status` 是本地队列态，不是平台裁决（2026-10-31 KOR 163 行收口）

`EXPIRED` + `gate=IS_ONLY` + `towers=[]` 的真实含义 =
**「从未做过提交层核验、从未做过塔位归属」**——**既不是候选，也不是死**。
把它当「已判死」会漏掉供给，把它当「可提交」会送上 prod 墙。

**零配额收口手法 = 抽样 + TO 签名聚类**：
KOR 163 行队列里 25 行 prod<0.70，用 **4 次** `get_alpha_details` + TO 签名（.1744–.189）
与同形 EXPIRED/IS_ONLY 判掉 **19 行**（6 行直接取证、13 行签名聚类）⇒ **省 19 次平台读**。

**两条附带教训**：

1. **标签与数值不一致时信数值**：两行标 `SELF_BLOCKED`，self 却仅 **.1967 / .1970**（远低于 0.7）
   ⇒ 真问题是 prod 贴线（且 stale）+ 塔已满，不是 self。
2. **高分簇未必是 REGULAR**：KOR `ds=1150` 簇 S **3.62–4.98**、本地 `alpha_type=NULL`，
   实为 **COMBO / SELECTION / SUPER**（`combo_a(alpha)` / `generate_stats`+`self_corr`、
   `selectionHandling=POSITIVE` / `selectionLimit=10`）⇒ **不计入 REGULAR 金字塔**。
   盘点 REGULAR 供给前必须按**表达式形态 + settings** 剔掉这三类，否则会把 4.98 当成「已有高分可提交」。

> 区域完整实证与逐条出处见
> [`tracking/KOR/reference/kor_session_lessons_20261031.md`](../../tracking/KOR/reference/kor_session_lessons_20261031.md) §2 / §8.2。

---

## 16. ★ IS 窗是平台硬定的（只能变窄不能平移）；`coverage` 是截面口径，不是时间口径（2026-10-31 KOR 实测）

### 16.1 IS 窗硬定：请求被接受 ≠ 窗口被采纳

KOR/D1 的 IS 窗由平台硬定 **2014-01-01 → 2023-12-31**。两轮干净差分：

| 轮 | 请求体 start/end | 回执 | 子 alpha 落库 `settings.startDate/endDate` |
|---|---|---|---|
| 1 | 未显式传（剖面 2013/2023） | — | **2014-01-01 / 2023-12-31**（起日被钳到数据起点） |
| 2 | **显式 2015-01-01 / 2024-12-31** | **HTTP 201** + `settings_source=explicit` + `settings_used` 逐字回显 2015/2024 | **2014-01-01 / 2023-12-31**（静默改回硬窗） |

⇒ **平台接受请求并回显你的设置，但落库时替换成硬窗**。两条独立佐证排除「去重造成」：
第 1 轮与既有基线返回同一 alpha id `QPvr1vPM`（表达式与设置逐字相同 ⇒ 平台去重），
第 2 轮表达式不同、未去重，仍取得同一窗口。

**可执行结论（三条）**：
1. 「时段不够十年」**不要试移动窗口**，直接按平台硬窗计年数；KOR 十年合规 = 2014–2023 全覆盖，2014 空的集即判 9 年。
2. IS 窗这条自由度的实际边界 = **只能变窄，不能平移**（接受 2013→2014 的钳位，不接受任何越过 2023-12-31 的 end）。
3. 数据起点空缺（如 risk59 面板 2015 起 = 9 年）**任何表达式杠杆都造不出来**，唯一出路是请用户放宽年限约束。

⚠ **区域口径**：硬窗的具体日期是 KOR/D1 实测值，**换区必须重测**；但「回执回显 ≠ 落库生效」这条**核验方法**跨区通用
——凡声称改了窗口的实验，都要回读子 alpha 的 `settings`，不能只看请求体或 201。

### 16.2 「近十年都要有数据」不能用 `coverage` 判

`coverage` 是**截面覆盖**（当日有多少标的有值），**与时间跨度无关**。两个反例：

| 数据集 | coverage | 逐年 `longCount>0` | 判读 |
|---|---|---|---|
| sentiment26 | .356（低） | **7/10 年** | 覆盖低但时间上断续 ⇒ 不满足十年 |
| macro63 | **1.0**（满） | **10/10 年 longCount=0** | 覆盖满却**从未产生持仓** ⇒ 同样不满足 |

⇒ **判据只有一条**：`get_alpha_yearly_stats` 逐年核 `longCount>0 && shortCount>0`（需要收益的再加 `pnl>0`）。
这与 `AGENTS.md` §7.5 五道闸的第 3 条「近十年」是同一口径的两半：**coverage 决定要不要 backfill，逐年 longCount 决定够不够十年**。
把 coverage 当时间口径会同时犯两类错：放走 macro63 这种「满覆盖零持仓」的集，错杀低覆盖但逐年连续的集。

**★ 2026-11-19 用户放宽年限约束**（原话「一定要求有十年不合理，可以适当放宽」）：
- **放宽口径**：交付件逐年核验覆盖**最近九年（2015–2023）**即可；缺失只允许发生在**序列起点**（数据起点型缺失，供应商决定），**中途空窗仍不合格**（sentiment26 的 7/10 断续仍判不合格）。
- **依据**：IS 硬窗 2014–2023 由平台给定，数据起点由供应商决定，任何表达式杠杆都造不出来（§16.1 第 3 条）；把「十年」当硬闸会把数据起点晚一年的优质集误杀。
- **落点**：EUR `fund_holdings_panel`（2015–2023 九年满仓、2014 零持仓）的**数据层排除据此撤销**——它只剩 prod 墙（0.8887）。

**★ 2026-11-20 用户再次放开年限约束**（原话「我的九年要求先放开」）：
- **口径**：**年数下限整体撤除**——数据从任意年份开始均可交付；**唯一保留的数据层硬排除 = 序列中途的空窗年**（起点型缺失一律不构成排除理由）。
- **落点**：EUR `macro27`（网上招聘，EUR 仅 2021–2023 三年）的**数据层排除撤销**，改判为**信号层近闸候选**
  （S1.47/F0.81/2Y1.77/prod 0.7462，落 MACRO 塔 0/3）⇒ 重新投入定向破闸（decay 阶梯 + 核/窗/宇宙矩阵）。
- **不变**：S/F/2Y/sub/invest/prod 闸照旧；逐年核验仍要查（但只查「中途空窗」）。

### 16.3 ★★ 近闸即查 prod（2026-11-19 用户指令「指标近闸就查 prod 提前判断要不要继续投入」）

**结论：合理，且已接入流程**。prod 是独立于 IS 三闸（S/F/2Y）的第二道墙——实测三例：sent_matrix 4 颗全闸件 prod 0.871–0.923 全灭、fund_holdings zq378ELo 全闸除 prod 0.8887、insider 净买入 0.76–0.80。IS 打磨再久也过不了 prod，早查能省整波配额。

**执行规格（三护栏）**：

1. **触发条件（量化「近闸」）**：S≥1.38 ∧ F≥0.8 ∧ 2Y≥1.38 ∧ sub/S≥0.52 ∧ TO 在 [5%,20%]——即三闸各自缺口 ≤0.2。太早查（S~1.0）会把「形态未定型」误判成「信息源拥挤」。
2. **只查族代表**：同族多臂持仓高度重叠，查 1–2 个代表即可。prod 是账号级单并发槽（1–5 min/次，连续 pending 触发 600s 熔断），全臂扫描会挤占其他会话。
3. **结果三档决策**：
   | prod 读数 | 决策 | 动作 |
   |---|---|---|
   | **≥0.85** | **停族** | 换字段/换数据集；同族变体不再投入（sent_matrix 0.87–0.92 四连灭） |
   | **0.70–0.85** | **限投** | 只许**改变持仓集合**的杠杆：换宇宙、罕见慢/快窗（ts_mean 504 / ts_delta 22）、平滑；**禁止**在保序形变（中性化档/分组轴/幂次/叉乘）上继续烧配额（实测每维仅动 0.015–0.03） |
   | **<0.70** | **放行** | 投入全闸打磨；交付前仍须 `refresh=True` 终验（prod 会漂移，0.67→0.92 实测） |

**附加两条**：
- 高 prod 只否证**这个形态**，不否证字段：同字段仍有未测持仓集合改变型形态时（rsk70 实证 ts_delta(1) 0.826 → ts_mean(504) 0.645），归「限投」而非「停族」。
- 与 `prod_first_skeleton_v1`（每槽先 1–2 条骨架查 prod）兼容：那条管「S 弱时早筛」，本条管「近闸时必查」，两者都指向「别等全闸做完才第一次碰 prod」。

## 17. ★ 边际贡献闸（2026-11-13 演进史；**现行口径见 §18 方案 D**）

用户口径：「表格里所有指标在提交 alpha 变正向才比较好，把这个也加进标准约束」。
经 16 颗活跃候选实测校准后，用户选定 **分级硬闸**（而非五项全硬拦）。

### 方向定义（唯一事实源：`src/wqb/workflow/nodes/submit_alpha.py::MARGINAL_*`）

| 指标 | 方向 | 达标 | 违反时处置 |
|---|---|---|---|
| `sharpe` | 越大越好 | Δ ≥ 0 | **净效果层硬闸阻断**（2026-11-08 铁律） |
| `returns` | 越大越好 | Δ ≥ 0 | **配对判据**：仅当 ΔTO>0 或 ΔDD>0 时硬拦 |
| `fitness` | 越大越好 | Δ ≥ 0 | **净效果层硬闸阻断**（2026-11-13 追加） |
| `turnover` | **越小越好** | Δ ≤ 0 | 仅 `soft_warnings` |
| `drawdown` | **越小越好** | Δ ≤ 0 | 仅 `soft_warnings` |

⚠ 不能一律要求「Δ 变正」：换手升高、回撤扩大是**变差**。

### 闸行为

- 任一硬项 `Δ < 0` ⇒ `hard_blocked=True` ⇒ Step 1.7 在 `set_properties` / POST **之前** `return`，
  `blocked=True`，**`force` 不豁免**。预检（`confirm_submit=False`）只出数值 + 顶层 `marginal_warning` 预告。
- `available=False`（空体 / 超时 / 异常 / 无分区归属）**不阻断**：可用性缺失 ≠ 为负。
- `dilutive` 仍保留 `ΔSharpe<0` 原语义，供 Step 1.8 分散度软闸与历史调用方复用；
  新增字段 `hard_blocked / hard_failures / hard_failures_detail / soft_warnings / direction_ok / direction_rule`。
- ΔS 仍**只能在同一分区内比符号**，禁止横向排序（见 §2、节点 docstring 遗留风险③）。

### 为什么不把成本指标设硬闸

16 颗活跃候选实测（`results/_marginal_allmetrics_20261113.json`）：

| 判据 | 达标 |
|---|---:|
| ΔSharpe ≥ 0 | 16/16 |
| ΔFitness ≥ 0 | 16/16 |
| ΔReturns ≥ 0 | 9/16 |
| ΔTurnover ≤ 0 | **6/16** |
| ΔDrawdown ≤ 0 | 14/16 |
| 五项按方向全达标 | **3/16** |

新增一条信号腿几乎必然抬高组合换手（10/16 如此）；分散化 alpha 常以「收益略降、波动降更多」
换取 Sharpe 上升。全硬拦会**系统性拒绝分散化来源**，正是 Step 1.7 docstring 第②条已警告的遗留风险。

按方案 D（分层 + 配对）**12/16 可交**；拦下 4 颗真恶化：
`ZYQ116ln` / `JjeNJ00O` / `YP1baJrv` / `qM7KxkQV`；放行 3 颗分散化补偿：`vRAgNK3w` / `Wjl8Z20O` / `O0A6Qz7p`。
`omEdka3v`（ΔRet +0.0028）、`wpo8olA6`（+0.0015）、`6XdkW08J`（+0.0020）仍可交。

### Fitness 为什么也升为硬项（2026-11-13 追加）

- 对称性：`sharpe/fitness/returns` 同为「越大越好」的正向族，只拦两个是口径缺口。
- 零误伤：16 颗活跃候选 ΔFitness<0 为 **0 颗**，加入后 9/16 可交的裁决**逐颗不变**。
- 捕捉复合成本：`F = S×√(ret/max(TO,0.125))`。存在 ΔS>0、ΔRet>0、ΔTO>0 但 ΔF<0 的情形
  （构造例：S 3.0→3.1、ret .080→.081、TO .13→.20 ⇒ F 2.353→1.973，ΔF −0.381），
  即「换手成本吃掉收益改善」，只有 Fitness 能直接反映。
- ⚠ 已知取舍：Fitness 复合了 Turnover，因此 ΔTO 大幅上升会**经 ΔFitness 间接硬拦**，
  与「成本指标只告警」的初衷部分重叠。若要完全避免，把 `fitness` 从
  `MARGINAL_HARD_BLOCK_METRICS` 移除即可（常量集中、改动可逆）。

### 追溯

今日 17:44 已提交的 `P059RmzM` 的 ΔReturns = −0.0040，**按新闸会被拦**；提交不可逆，
仅标注为「新闸生效前的历史提交」，不改终态、不追溯撤销。

同步面：节点代码 + `tests/unit/05_submit_quota/test_submit_marginal_{contribution,wiring}.py`
（388 passed）+ `worldquant-submit-alpha/references/submit-chain.md` 步 4b（项目级 / 用户级双份）。


## 18. 方案 D「分层 + 配对」（2026-11-13 19:5x 拍板；**零死区版，已被 §18.1 v2 取代**）

用户追问「换手不是越小越好吗，为什么会有反例，怎么匹配这几个指标才是最佳方案」⇒ 发现
`F = S×√(ret/max(TO,0.125))` 使 `sharpe/fitness/returns/turnover` 四量共线，原「三项正向指标全硬拦」
对同一信息三重把关；且 ΔTO 单独看是软告警、复合成 ΔF 却硬拦，口径自相矛盾。

### 三层结构（唯一事实源 `submit_alpha.MARGINAL_*`）

1. **净效果层（唯一硬闸）**：`ΔSharpe ≥ 0` 且 `ΔFitness ≥ 0`。二者已把收益、波动、换手压缩成比值。
2. **配对判据（仅 ΔReturns<0 时启用）**：`ΔReturns<0` **且** (`ΔTurnover>0` 或 `ΔDrawdown>0`)
   ⇒ 双重恶化，追加阻断；`ΔReturns<0` 但成本同步下降 ⇒ **分散化补偿**，放行并记 `pair_rule.offset=True`。
3. **归因层（纯软告警）**：`ΔTurnover` / `ΔDrawdown` 单独变差只写 `soft_warnings`，不设闸。

### 为什么 ΔReturns 不能单独硬拦

`performance_comparison` 的 before/after 是把候选**等权叠加到分区已提交组合**的结果，不是候选自身指标。
`ΔRet<0` 常只是「新腿收益低于池均值」的机械摊薄，低相关分散化来源几乎必然如此。16 颗实测里被原闸
误伤的 3 颗健康分散化：`vRAgNK3w`（ΔS +0.28 / ΔF +0.22 / ΔRet −0.0040 / ΔTO **−0.0160** / ΔDD −0.0019）、
`Wjl8Z20O`、`O0A6Qz7p`；今日已提交的 `P059RmzM` 同形态。硬拦 ΔRet = 系统性拒绝「合格但不突出」的新机制
（Step 1.7 docstring 遗留风险②）。

### 方案对比（16 颗活跃候选实测）

| 方案 | 可交 | 评价 |
|---|---:|---|
| A 原 S+F+Ret 全硬拦 | 9/16 | 误伤 3 颗健康分散化 |
| B 五项全按方向 | 3/16 | 连首推 `omEdka3v` 都拦 |
| C 只 S+F | 16/16 | 闸形同虚设（本池 ΔS/ΔF 恰全 ≥0） |
| **D 分层 + 配对（现行）** | **12/16** | 拦 4 颗真恶化、放行 3 颗补偿 |

⚠ **局限**：本池 ΔS/ΔF 恰好全 ≥0，净效果层在样本内没有区分度，D 的分辨力主要来自配对判据；
需跨区多批样本再验证。另「闸放行」≠「推荐提交」，排序仍以全篮质量分与塔倍率为准。

**同步面**：`src/wqb/workflow/nodes/submit_alpha.py`（常量 + 判定 + docstring + Step 1.7 文案）、
两个 `05_submit_quota` 测试文件（新增「分散化补偿放行」「配对触发硬拦」「真提交放行」用例）、
`worldquant-submit-alpha/references/submit-chain.md` 步 4b（项目级 + 5 安装位）、
`MEMORY.md` §0、`output_report/marginal_gate_v2_20261113.md` §7。

---

## 18.1 ★★★ 现行口径：方案 D **v2 严格档**（2026-11-16 09:5x 用户明令「分层阈值再调严格一点」）

### 为什么改：零死区在噪声里抛硬币

平台实测同一 `EQUITY:DEU:1` 分区（before S 3.52 / F 3.05 / Ret 10.13% / TO 13.53% / DD 2.64%）
两颗候选的边际贡献：

| alpha | ΔSharpe | ΔFitness | ΔReturns | ΔTurnover | ΔDrawdown | 旧零死区 | v2 严格档 |
|---|---:|---:|---:|---:|---:|---|---|
| `akaWd90w` | **+0.06** | **+0.02** | −0.09pp | +0.13pp | −0.09pp | ❌ pair_rule 硬拦 | ✅ `pass_offset` |
| `kqamAeRg` | **+0.06** | **+0.01** | −0.09pp | +0.17pp | −0.10pp | ❌ pair_rule 硬拦 | ✅ `pass_offset` |

两颗**净效果双双为正**（组合 Sharpe 3.52→3.58），却因为「ΔRet 为负 0.09pp 且 ΔTO 为正 0.17pp」
被当成「收益降 + 成本升」双重恶化否决。0.09pp / 0.17pp 完全在噪声量级 —— 这是抛硬币弃件，
不是质量把关。官方侧同向证据：`Consultant Submission Tests` 九项里**没有**边际贡献项；
`Clear these tests before submitting` 原话 "low correlation is more important than minor increase
in performance"；`Brain Genius` 明说点塔通过分散提升 CAP。

### 四层判定（唯一事实源 `submit_alpha.MARGINAL_*`）

| 层 | 条件 | 结果 |
|---|---|---|
| **L0 死区** | `|ΔS| ≤ 0.02` ∧ `|ΔF| ≤ 0.02` ∧ `|ΔRet| ≤ 0.3pp` | `verdict="neutral"`，放行且不出软告警 |
| **L1 净效果** | `ΔS < −0.05` **或** `ΔF < −0.05` | 硬拦（`net_block`，force 不豁免） |
| **L2 配对** | `ΔRet ≤ −0.5pp` **且**（`ΔTO ≥ +1.5pp` **或** `ΔDD ≥ +0.5pp`） | 硬拦（`pair_block`） |
| **L3 归因** | `ΔTO` / `ΔDD` 单独变差 | 只写 `soft_warnings` |

严格档 vs 宽松档（本次刻意砍半）：净效果容差 **0.05 vs 0.10**｜配对收益 **−0.5pp vs −1.0pp**｜
配对换手 **+1.5pp vs +3.0pp**｜配对回撤 **+0.5pp vs +1.0pp**｜死区 **0.02/0.3pp vs 0.03/0.5pp**。
噪声实测上限约 ΔRet 0.1pp、ΔTO 0.3pp ⇒ 门槛仍有 5 倍以上安全边际，不会误杀。

### 两条接线要点（v2 与旧版最容易改错的地方）

1. **`run()` 只认 `hard_blocked`，不再 `or dilutive`**。旧版 `if _hard or marginal.get("dilutive")`
   会让「ΔS=−0.001」直接阻断 —— 容差带形同虚设。`dilutive`（ΔS<0）现仅作排序键与
   Step 1.8 分散度输入。
2. **不设「点亮塔」豁免通道**。点塔有官方经济依据，但豁免等于允许为凑塔位降质量门槛，
   与「调严」指令冲突 ⇒ 塔信息只作排序键，不进闸门；确需豁免时报用户个案裁定。

### 判定标签（`verdict`）

`net_block` / `pair_block` / `neutral` / `pass_offset` / `pass`；阈值经 `thresholds` 字段随每次
结果透出，便于审计（`test_thresholds_are_exposed_and_strict` 锁死取值）。

**同步面**：`submit_alpha.py`（常量区 + `_marginal_contribution` 判定 + `run()` Step 1.7 接线 +
docstring/plan 文案）、
`tests/unit/05_submit_quota/test_submit_marginal_contribution.py`（新增 `_Deadzone` / `_MildNegative` /
`_PairWorsened` / `_AkaWd90wSnapshot` / `_KqamAeRgSnapshot` 五组用例）、
`test_submit_marginal_wiring.py`（新增 `test_noise_level_returns_does_not_block` 反回归用例）、
`MEMORY.md` §1。

---

## §X 相关性闸的两条口径纠正（2026-11-15 KOR 实测）

### X.1 `prod` 是**平台全局生产池**，不是本账号 OS 池 ⇒ `self` 不能预筛 `prod`

硬证据（同一天、同一账号、KOR）：

| alpha | self（本地 OS 池，32 条参与） | prod（平台） | 结论 |
|---|---:|---:|---|
| `3qokqkZQ` | **0.270** | **0.8495** | self 极低而 prod 撞墙 |
| `zq3eAMbV` | 0.085 | 同族 `leA1gqMn` = 0.9579 | 同上 |
| `akKGb8w9` | 0.338 | 同族 `rKR8wXZE` = 0.7827 | 同上 |
| `78LpqZYQ` | 0.477 | **0.697** ✅ | 唯一双低 |

量化口径：`check_correlation(production)` 返回的直方图**合计 10 万级 pair 计数**，
而本账号 KOR OS 池只有 **49** 条 ⇒ prod 的对照池远大于本账号。
⇒ **纪律**：① 不许用 `check_self_correlation` 预筛 prod（会漏掉 0.85 的墙）；
② 判 prod 只能 `check_correlation(correlation_type='production')` 实测；
③ 查历史值时先看**同子族**的已知 prod（同族一条撞墙 ≈ 整族撞墙），再决定要不要烧那一次平台计算；
④ 平台相关性**每账号仅 1 个在飞**，且可能被 `corr:prod_backfill(...)` 后台任务占住 ⇒ 返回 `correlation_busy` 时按 `retry_after` 等，不要重触发。

### X.2 `checks.warning` 也计入 `failed_ra_count` ⇒ 「全闸」= fail 与 warning 都空

实测：`58g6lPkX` 的 `LOW_INVESTABILITY_CONSTRAINED_SHARPE` = **1.99**，limit **2.02**（差 1.5%），
平台把它放在 `checks.warning` 桶，但 `ra.failed_ra_count` 仍为 **1**、`ra.ra_failed = true`。
同批 `dl_riskfree_returns` 18 条里 **8 条**因此不过闸（investability 1.65–1.91 vs ~2.02）。
⇒ 判「全闸」必须 `len(checks.fail) + len(checks.warning) == 0`（`MATCHES_COMPETITION` / `MATCHES_THEMES` 除外，
它们是信息项不是阈值项）；只看 `checks.fail` 会把 8 条误判成可提交。

---

## 19. ★★★ Genius tie-breaker「六维」—— 用户 2026-11-16 10:2x 明令纳入考评

### 19.1 官方口径（唯一事实源：`brain-genius` 文档 §Criteria，2026-09-18 版）

**六维不是"Genius 六维评分"这种笼统说法，而是官方 tie-breaker 六项**，原文在
*"What happens if more consultants qualify for a level than there are available spots?"*：

| 序号 | 官方原文 | 方向 | 可操作含义 |
|---|---|---|---|
| T1 | Avg distinct Operators\*/Alpha | **越低越好** | 单件算子越少越好 |
| T2 | Avg distinct Fields/Alpha | **越低越好** | 单件字段越少越好 |
| T3 | Total distinct Operators\* | **越高越好** | 引入未用算子加分 |
| T4 | Total distinct Fields | **越高越好** | 引入未用字段加分 |
| T5 | Maximum Simulation Streak | 越高越好 | 连续仿真天数，与选件无关 |
| T6 | Community leader（论坛 ≥100 字符帖的赞 + 成功推荐） | 越高越好 | 与选件无关 |

\* 官方脚注：`ts_backfill` / `group_backfill` **不计入** T1/T3 的算子计数。

**判定方式**：先是三项 eligibility 阈值（① 季度提交信号数 ② 塔数 ③ Combined Alpha Performance），
**同档达标者之间按「六项排名之和」排序**。官方原话："Eligibility criteria are thresholds,
not rankings. Meeting the thresholds, whether narrowly or by a wide margin, is the same.
Hence they are relatively easy to achieve, compared to the tie breaker criteria."

### 19.2 为什么六维直接等于钱

tiebreak → Genius 等级 → 数据/算子权限（Gold 50%/45%、Expert 61%/63%、Master 78%/78%、
Grand Master 100%/100%）＋**季度付款档位**（`brain-genius` 原文：Master "$2,000 or more"、
Grand Master "80x or more, upwards of $8,000 or more"）。⇒ 六维是"能不能摸到更高付款档"的临门一脚。
另外官方明说 "Formulating a higher number of pyramids can potentially improve both the Value Factor
and Combined Alpha Performance **through diversification**" ⇒ **塔与六维方向一致，不冲突**。

### 19.3 ★ 权重不对称（本条的实践核心）

- **T1/T2 是平均值** ⇒ 单颗权重 `1/(N+1)`（当前 **N=386**），单件 ΔT1 只到 **0.010–0.020** 量级（相对 0.2%–0.4%）⇒
  **几乎不改变 tiebreak 排名**，属**软成本**。
- **T3/T4 是总数** ⇒ +1 就是确定性收益（62→63，按 103 分母约 +1.6%）⇒ **对 tiebreak 敏感**，属**硬收益**。

⇒ **可操作判据（四条）**：
1. 同绩效**优先 distinct ops / fields 更少**的件（压 T1/T2）；
2. **优先引入未用过的算子/字段**（提 T3/T4）；未用算子池见 §19.4.2 与 `MEMORY.md`（当前 38 个）；
3. **纯堆算子但全是旧算子 = 双重伤害**（T1 变差、T3 不动），这是最该先砍的形态；
4. **六维整体不设硬闸**（tiebreak 不是提交闸）；**但 T1 可按用户指令单独设为 ceiling 硬闸**，见 §19.4.2（`--t1-ceiling`，exit 3 阻断）。

**优先级**：**塔 eligibility（≥3 才计入）> 六维 tiebreak**。先保证点塔，再在同一塔档内比六维。

### 19.4 取数与基线（2026-11-16 10:2x 实测）

MCP **没有** Genius tiebreak 端点（`get_leaderboard` 只给 valueFactor / dataFieldsUsed /
submissionsCount / meanProd / meanSelf）；平台 REST 侧 `/users/self/competition/genius`、
`/users/self/genius`、`/users/self/activities/genius`、`/genius/leaderboard` **全部 404**。
⇒ 落为仓库正式 CLI **`tools/super/genius_tiebreak.py`**（`--compute` / `--alphas` / `--probe` / `--json`），
它拉全量 OS alpha（`regular.code` 在原始 REST 的 `regular` 子对象里，MCP 才拍平到顶层），
用 `wqb.expression.atom.extract_fields` + 算子正则自行统计。

账户基线（**2026-11-19 00:0x 用平台面板真值标定，取代此前所有版本**）：

**★★★★★ 统计窗口＝当季，不是累计**（用户 2026-11-19 提供 Genius 面板截图定案，
此前 11-18 的「累计」结论**作废**）。三条铁证：

1. 面板标题写死 `2026-04, October 1st, 2026 - December 31st, 2026`（＝ 2026-Q4）；
2. **Q4 REGULAR 的 distinct 算子 = 54 ＝ 面板 `Operators used`**（全生命周期是 64/65）—— 精确命中；
3. 领导板 `dataFieldsUsed = 435` 是**另一个指标**（生命周期），与面板 `Fields Used = 227` 并存。
   11-18 拿 `dataFieldsUsed` 反推「T4 不归零」是**把两个指标混为一谈**。

| 项 | 平台面板真值（2026-Q4） | 本地复算（`--compute --window quarter --panel`） | 差 |
|---|---:|---:|---:|
| 窗口 | 2026-10-01 … 2026-12-31 | 同 | — |
| N（REGULAR） | 141 | 140（本地库少 1 颗） | −1 |
| **T1** Operators per Alpha | **5.73** | **5.7214** | −0.009（−0.15%） |
| **T2** Fields per Alpha | **2.07** | **2.0857** | +0.016（N=141 时 2.071） |
| **T3** Operators used | **54** | **54** | **0（精确）** |
| **T4** Fields Used | **227** | **228** | +1（0.4%） |
| **T5** Max simulation streak | **130** | 平台无端点 | — |
| **T6** Community activity | **10.3** | 平台无端点 | — |

### 19.4.1 ★★★★★ 四个口径的精确算法（已标定）

| 维度 | 算法 | 关键细节 |
|---|---|---|
| **T1** | `distinct( 命名调用 ∪ 算术中缀 ∪ 比较中缀 )`，**剔除 backfill** | ⚠ **一元负号也算 `subtract`**（如 `-group_rank(...)`）。不加这一条会系统性低估 **0.13/alpha**（5.5929 vs 5.7214）。⚠ 不是 named-only（低 1.2）、也不是中缀按次数累加（高 0.09） |
| **T2/T4** | distinct **字段** | ⚠ **只剔分组键** `market/sector/industry/subindustry/country/exchange/currency`；**base 行情字段（close/volume/returns/cap/adv20…）照常计入**。旧版把 base 一起剔 → T4 224 / T2 1.99（错） |
| **T3** | distinct **命名算子**，剔除 backfill | 本地与面板**精确相等**（54），是最可靠的锚点 |
| **T5/T6** | streak / community | 与选件无关；平台无端点，只能人工看面板 |

⚠ 平台**没有**任何端点暴露六维（`/users/self/genius`、`/consultant/genius`、
`/users/self/competition/genius|leaderboard` 全部 **404**；`get_leaderboard` 只给
`dataFieldsUsed`/`submissionsCount`/`meanProd`/`meanSelf`）⇒ 只能本地从
`GET /alphas?stage=OS` 的 code 自算，并用面板数对标定。

### 19.4.1.1 ★★★ 季初归零的两条战略后果

1. **T3/T4 每季重置可重赚** ⇒ 未用算子不是「一次性资本」。Q4 未用 **49**（扣掉不计入 T3 的
   backfill 与 SUPER 专用 `combo_a` ⇒ **46 个可赚**）；另有 **11 个算子上季用过、本季未用**
   （`equal`,`generate_stats`,`group_mean`,`is_nan`,`log`,`normalize`,`reduce_max`,`scale`,
   `self_corr`,`sign`,`ts_arg_max`）⇒ **本季可以重新赚一次 T3**。正确节奏是**每季重新铺一批
   覆盖多算子/多字段的件**。
2. **T1 也在季初归零** ⇒ 每季**第一颗**的 ops 直接决定当季 T1 起点（交一颗 9 算子件即 T1=9.0）。
   **每季应先用低 ops 件铺底**，再补高 T3 件抬多样性。

### 19.4.2 ★★★ 把 T1 设为首要条件：怎么做（2026-11-18 用户指令）

**先看杠杆再定规则**：T1 是**平均值（存量）**，单颗的边际是固定的
`ΔT1 = (ops_new − T1_old) / (N+1)`，N=386 ⇒ 单件只 0.010–0.020（相对 0.2%–0.4%）。
所以「T1 首要」不可能靠"挑一颗"实现，必须做成**逐颗上限 + 字典序排序**两层：

| 层 | 规则 | 实现 |
|---|---|---|
| **L1 硬闸（首要条件）** | 候选 distinct ops（归一口径）超过 `ceiling` ⇒ 直接 BLOCK，不看绩效 | `genius_tiebreak.py --alphas <ids> --t1-ceiling <float>` → **exit 3** |
| **L2 字典序排序** | 全闸通过件按 `ops 升 → fields 升` 排，第一名标 `PRIMARY` | `genius_tiebreak.py --alphas <ids> --primary t1` |
| L3 报告 | 每颗必列 `ops / ops_named_only / ΔT1 / T3新增 / T4新增` | 同上输出 |

**ceiling 取值与 T1 的关系（当季口径：N=141，T1_old=5.73）**：

| ops | ΔT1 | T1_new | 建议档 |
|---:|---:|---:|---|
| 4 | −0.0121 | 5.7179 | **唯一能降 T1 的档**（ops < 5.73） |
| 6 | +0.0019 | 5.7319 | A 档首选 |
| 7 | +0.0090 | 5.7390 | A 档 |
| 9 | +0.0232 | 5.7532 | B 档 |
| 11 | +0.0374 | 5.7674 | C 档 |
| 13 | +0.0516 | 5.7816 | D 档上限 |
| ≥15 | ≥+0.066 | ≥5.796 | 原则上不交 |

**⚠ 两个必须知道的反直觉点**：
1. **只有 ops < T1_old（5.73）才能降 T1**，而现实里的像样信号几乎都在 9–13 ⇒ **T1 只可能被"少恶化"，不可能被"优化"**。真正的 T1 战略是**长期把 ops 压到 6 以下**，而不是在候选间挑。
2. **T1 与 T3 直接对冲**：每引入 1 个未用算子 T3 +1，同时 T1 +1/(N+1)=+0.0071。当前换算 **T3 +1 ≈ +1.6% 收益 vs ΔT1 +0.0071（≈ T1 相对 +0.12%）** ⇒ **T3 仍划算**，但若 ceiling 收到 6 以下，"加新算子换 T3"这条路就基本关闭。

**★ 季初重置的用法**：因为 T1 每季归零，`ΔT1` 公式里的 `T1_old` 在季初是 0，
所以**每季最有价值的动作是「先用 ops ≤ 6 的件铺底」**——铺 5 颗 6-ops 件后 T1 才 6.0，
此时再交一颗 13-ops 的高 T3 件只把 T1 推到 7.17，代价可控；反过来先交 13-ops，
后续每颗低 ops 件都在"往回拉"。**顺序决定当季 T1 曲线。**

⚠ 已作废：11-18 那份「T1–T4 是累计口径、未用算子是一次性资本」的结论**错误**——
它把领导板 `dataFieldsUsed`（生命周期指标）当成了 T4。见 §19.4 的三条铁证。
⚠ `VERIFIED_SAFE_OPERATORS` 运行时为空（`len()==0`，靠 config 状态注入）⇒ **不要拿它当算子过滤器**，
否则会把所有算子算成 0（本次踩过，第一版候选全 `ops=0`）。
⚠ 平台 `regular.operatorCount` 是**调用次数**（含重复），官方 tiebreak 要的是 **distinct**，不能直接拿来当 T1。

### 19.5 报告模板（与塔六元组同表）

`id | 塔六元组 | ops | fields | ΔT1 | ΔT2 | T3 新算子 | T4 新字段 | 六维结论`

T5/T6 写 `n/a（与选件无关）`，不得静默省略。
