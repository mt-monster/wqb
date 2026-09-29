# prod 相关性总纲：怎么测 · 怎么读 · 已确认的族 · 证据

> 2026-09-29 改写为**总纲**（skills 审查 RC-01 ~ RC-07）。旧版是 2026-08-05 的 GLB 实验流水账，教了「用 POST / GET `/submit` 触发 prod 计算」——**那是危险的过期指令**：
> `GET /alphas/{id}/submit` 在本平台恒 404，`POST` 通过就是**真实且不可撤销的提交**。prod 一律用 `check_correlation`（只读 `GET correlations/prod`）。
> **本文只回答三件事**：① 怎么测（含排队纪律）② 拿到值之后怎么读 ③ 哪些族已确认撞墙。**「拿到 prod 值后下一步做什么」只有一张表：[`decision-table.md`](decision-table.md) D0-P**——本文、步 5b、闸 PF、步 7、步 8、区域 profile 都只引用它，不再各写一套。

## 1. 怎么测：排队纪律（强制）

平台 prod 计算是**异步排队**（候选 vs 全平台生产池 4 年日收益的相关，通常 1–5 分钟；前几次查询返回空 body 属正常），且**每账户仅允许 1 个在飞**——多候选串行等待是 S4 链的主要时间黑洞。

| 事实 | 出处 |
|---|---|
| `check_correlation` 内置阻塞轮询（间隔 `prod_corr_poll_s` = 30 s，最长 `prod_corr_timeout_s` = 3600 s）；账号级单并发，忙时**立即**返回 `correlation_busy`（fail-fast） | `wqb.config.WAIT_THRESHOLDS` |
| 同一 alpha 的已决结果缓存 **7 天**——**仅在有 Redis 时**（键 `prod_corr:<alpha_id>`）。Redis **只是可选缓存**：无 Redis 功能不受影响，只是不缓存、每次都排队；「等死」的原因是上一行的 30 s × 120 次阻塞轮询与账号级单并发，不是 Redis。`pending` / `correlation_busy` / `data_unavailable` **不缓存**；命中缓存的响应带 `from_cache: true` | `brain_mixin_correlation.py`、`brain_mixin_transport.py`（`_get_cached_data`：无 `redis_client` 直接返回 None） |
| `correlation_busy` 带 `retry_after`（缺省 180 s，环境变量 `BRAIN_CORRELATION_BUSY_RETRY_AFTER_SECONDS`） | `brain_mixin_transport.py` |
| **提交前终验必须 `refresh=True`** 强制回源——本地 / 缓存的 prod 值会随平台 prod 池变动快速漂移（0.6997 → 1.0000 一小时内发生过） | `incidents.md` I-2 |

**三种返回怎么处置**（这是环境事实的唯一一处；how-to-pass / robustness 都指向这里）：

| 返回 | 含义 | 动作 |
|---|---|---|
| 命中缓存（`from_cache: true`） | 7 天内的已决结果（仅有 Redis 时会有） | 直接用；**提交前终验**仍须 `refresh=True` 回源 |
| `pending` | 轮询超时（≥ 1 h）仍无数据 | 视为**未决**：不据此放行、不据此判死；隔一段时间再查一次，再空则向用户报错，**不得编造数字** |
| `correlation_busy` | 账号级单并发已被占用（fail-fast，立即返回） | 按 `retry_after` 等待后**串行**重试；不要另起并行进程去抢 |

**`refresh=True` 的量化**（防止拉长平台队列）：每个 alpha 的每个决策点**至多 1 次**——用于提交前终验；同一 alpha 两次 refresh 至少间隔 **5 分钟**（经验值：平台 prod 计算通常 1–5 分钟，间隔内的重复请求只会撞上在飞的那一个）。

**批量候选调度（串行泳道 + 本地并行）**：
1. 全批先跑完本地检查（selfcorrQuick / mutual / 逐年归因——不占平台队列，可并行）。
2. 仅本地预过者排入 prod 泳道，队列永远保持**恰好 1 个在飞**：提交 A → 等待期做 A 的归因 / 稳健性材料 → A 回来（自动入缓存）立即提交 B。
3. 必挂候选（本地 self / mutual 已 > 0.7）**禁烧平台队列**；全批回收后统一进 judge。
4. 会话压缩 / 重开后重验同一 alpha，先查缓存（`from_cache: true`），命中则不重新排队。
5. S3 收批后的族级首探用 `python tools/campaign_intel.py prod-first`（串行、进程锁 `data/.prod_first.lock`、单条硬超时 600 s、`--top-k` 缺省 3，每族最强 1 条）——它已内置本节纪律，不要另起并行进程。

**禁用**：`POST /alphas/{id}/submit` 探测（真提交）；`GET /alphas/{id}/submit`（恒 404，什么都回答不了）。

## 2. 怎么读：判据

- **平台线**：prod < 0.7 才可提交（`wqb.config` 的平台线；本文不复写数字之外的阈值）。**拿到值之后怎么办 → D0-P。**
- **字段分级**（`get_datafields` 后立即做；**经验阈值**，出处 GLB 2026-08 实验）：

| `users` | 处置 |
|---|---|
| ≥ 50 | 只做信号方向验证，不投入候选打磨（prod_corr 必超） |
| 10–49 | 进候选池；提交前必须实测 prod（`check_correlation`） |
| 0–9 | 优先候选池（理论 prod_corr ≈ 0——生产池无同类）；冷门字段占批次预算 ≥ 50%；热门字段只用于族方向验证（每族 ≤ 1 批） |

- **通则**（GLB 双墙的提炼，同 USA other566 / risk65 验证）：**信号强度、可打磨性、prod_corr 三者不可兼得**——强信号必被生产池套牢；冷门字段信号衰减大（sharpe 0.91–1.65 vs 热门 1.8–2.9，社区 userCount 与信号强度正相关）；中间地带（users 18–49）常带 fit / AMER / 2Y 的**结构性缺口**（窗口 / decay 修不了）。`users > 30K` 的饱和数据集与 `users > 50` 的热门字段强信号 = prod_corr 高危（WebDataScope 规则 15 同源）。
- country 分组 / 长窗只修复子域与 margin，**不降 prod_corr**。

## 3. 已确认撞墙的族（提交实测；不再投任何变体）

登记位置：`registry_empirical` 的 `dead_end` 层（先 `forum_recon` 软核对再 `seal_dead_end`，见 `step9-writeback.md` §9.5）；下表是速查，**当前值以库为准**。

| 族 | 数据集 / 字段 | users | prod_corr | 出处 |
|---|---|---|---|---|
| GLB techindi 预测收益 | `techindi_model` `predicted_first_quantile_ten_day_return_*`（qMNZX1o1 = `first_quantile_ten_day_return_techindi6_2`：country 分组 + `ts_rank` 300 窗 + winsorize / backfill + decay15） | 97 | **0.7686** ❌ | GLB 提交被拒（2026-08-05） |
| USA | other566 | — | 0.86 | 历史提交 |
| USA | risk65 | — | 0.98 | 同上 |
| USA | fnd91 | — | 0.73–0.89 | 同上 |
| USA | option40 skew 族 | — | 0.75+ | 同上 |
| IND | intraday_pv_feats 价量相关反转 | — | 0.79–0.92 | 连投 3 波 24 条后才查，整族报废（`incidents.md` I-14） |

**待验证**（**推测，未触发实测**，别当成已确认）：`techindi_model` 的 `first_quantile_ten_day_return_41`（users 62，同族高概率 > 0.7）。

## 4. 证据附录：GLB 双墙实验（2026-08-05；**历史，该族已判「已穷尽-规避」**）

- 三层字段的最终结果：

| 字段层级 | users | 结果 |
|---|---|---|
| 热门（6_2 / 41 / 19_1） | 60–97 | 全 PASS 可打磨，但 **prod_corr > 0.7**（6_2 实测 0.7686） |
| 中间（16_1 / 17_1 / 5 / 25） | 18–40 | **fit / AMER / 2Y 结构性缺口**：`techindi16_1`（users 40）在 300–450 窗 × decay 14–16 全扫，sh 2.0–2.07 但 fit 0.96–0.98（差 0.02–0.04）、AMER fail、2Y 1.43–1.51（差 0.09–0.17），与窗口 / decay 无关 |
| 冷门（4 / tech1_1 / 24 / 23 / 3 / 22） | 0–4 | 信号弱（0.9–1.65；最佳 `_23` 1.65，仍远低于 1.58 线的安全裕度） |

- **结论**：GLB pred 系信号族在 prod_corr < 0.7 约束下**无候选来源**；10 个 PPA 达标目标在 GLB 当前不可达；批次 b10–b19 已存档。**算力方向**：新 PPA 主题窗口（非 pred 系）/ 新数据包的冷门数据集 / 其他区域（KOR / ASI）的 PPA 主题匹配。
- **「GLB 黄金配方」仅作历史**：`group_rank(ts_rank(ts_backfill(winsorize(F, std=5), 60), W), country)` @ FAST / trunc0.04，W=300 + decay15 → margin 5.0–5.1 bp 全 PASS（qMNZX1o1）。**该族已判死；且 margin 5.0–5.1 bp 低于内部严线 `GATES_INTERNAL.margin_bp_min`（= 10）**——不得作为新字段的「直接套用配方」。
