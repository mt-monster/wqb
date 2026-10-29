# 01 · 平台规则与硬门槛

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-10-24（§4 增补 USA 2026-10-23 复盘的 prod 分布）
>
> **现行政策提示（2026-09-30 合并时补）**：本文里「403 零成本 → 直接 POST 就是预检」的说法只对**被拒**的那一半成立——事先无从知道它会 403 还是通过，而通过的 POST 就是一次真实、不可撤销的提交。所以 `POST /alphas/{id}/submit` **只作用户确认后的真提交**（`workflow_submit_alpha(confirm_submit=True)`），**不作预检 / 探针**；提交前的检查用 `submit_verdict`（模拟层 checks）、`check_correlation`（只读 `GET correlations/prod`）与 `confirm_submit=False` 预检。全链与不可逆动作块见 [`submit-chain.md`](../../Claude/skills/worldquant-submit-alpha/references/submit-chain.md)。

---

## 1. 提交层四闸（REGULAR）

| 闸 | 阈值 | 备注 |
|---|---|---|
| `LOW_SHARPE` | ≥ **1.58** | 严格不等式 |
| `LOW_FITNESS` | ≥ **1.0** | 严格不等式 |
| `LOW_2Y_SHARPE` / `IS_LADDER_SHARPE` | ≥ **1.58** | 同一事实的两个载体，平台按 alpha 代际只发其一 |
| `LOW_SUB_UNIVERSE_SHARPE` | 比值闸（见 §2） | |

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
| **inflight 侧车** | 同 alpha 的第二个调用照样去抢锁、照样触发 | 开轮询即标记 `correlation.inflight.json`；同 alpha 非 refresh 调用**只预读等待**（缺省 25 s），等不到返回 `busy + inflight=true`，**不二次触发**；`pending` 保留标记、其余清除 | `WQB_CORR_INFLIGHT_TTL_SEC`（300） |
| **同 alpha 等待** | 锁被同 alpha 占着也立即 busy | holder 恰为同 alpha ⇒ 等 `WQB_CORR_JOIN_WAIT_SEC`（25 s）内的预读值（`same_alpha_join`）；refresh 保持 fail-fast | `WQB_CORR_JOIN_WAIT_SEC` |
| **打点与报告** | 只有人读的一句话 | `[corr-t] {json}` 结构化打点 + `tools/probe/corr_timing_report.py` 汇总「时间花在哪 / 拿到值 vs 空手 / 谁在反复触发」 | 零平台请求 |

配套的**消费方默认值**也改了：`check_correlation(refresh=False)` 是缺省（48 h 权威缓存 → 预读
`is.prodCorrelation`，命中即返回、**零平台计算**），只有**终验**（`submit_inventory --refresh-all`、
`corr_check --refresh`、`check_corr.py --refresh`）才强制重测。预读值带 `provisional=true`
——平台存储值**测量时间不可知**，不得记成「刚测过」（会污染 48 h 保鲜判据）。

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
   → 筛查产出的是**排序队列**而非终局清单，提交当日须 `refresh=True` 复测；`get_submit_ready` 的 `READY` 只代表「**曾经**过闸」，`corr_stale=true` 的行一律当作未验证。
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

- **★ prod 无需本地单独复测（2026-10-08 用户裁定）**：`prod_gate` 节点在 `confirm_submit=True` 时会**自己实时拉取 prod**（拿不到即 fail-closed 拒发，这正是 `correlation_busy` 的成因）。
  ⇒ 提交前那次独立的 `check_correlation(refresh=True)` 属**冗余动作**：它与节点抢同一个**单并发**队列，反而更容易把端点挤爆。**跳过它不降低安全标准**（硬闸在节点内）。
  ⇒ 处置：**用户确认后**执行 `workflow_submit_alpha(confirm_submit=True)`（真提交、**不可逆**）；若节点报 `correlation_busy`，**间隔重试**（≥90s），**切勿改参数或降标准**。
  ⚠ 仅当需要**事先排序/取舍**多个候选（不打算立即提交）时，才需 `check_correlation(refresh=True)` 复测。
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
