# 轮询 / 熔断 / 并发 / 退避 / 提交配额

> 数字的**唯一来源**：轮询与卡住阈值 = `src/wqb/config.py::WAIT_THRESHOLDS`（`sim_stall_min` / `sim_timeout_min`），并发 = `config.CONCURRENCY`；toolkit 的 `_lib/poller.py::DEFAULT_POLL` 与它们的一致性由 `tests/unit/07_docs_skills/test_wait_thresholds.py` 守。文档按键名引用，不另抄一份会漂的数字。

## 1. 轮询与熔断（`_lib/poller.py`，`thresholds.json` 的 `poll` 节可覆盖）

| 参数 | 缺省 | 含义 |
|---|---|---|
| `init_interval` | 20 s | 初始轮询间隔 |
| `backoff_factor` | 1.5 | 指数退避因子 |
| `max_interval` | 120 s | 间隔封顶 |
| `stall_minutes` | = `WAIT_THRESHOLDS.sim_stall_min` | progress 连续无变化判 `STALLED`（KOR waveT 卡 24 h 的教训） |
| `timeout_minutes` | = `WAIT_THRESHOLDS.sim_timeout_min` | 总超时 |

`TERMINAL = {COMPLETE, ERROR, CANCELLED}`。`COMPLETE` → 自动拉全量 child alpha 指标；`ERROR` → **全量 child 逐个取 error**（`[:8]` 截断是历史 bug，会漏 > 8 批次的错误定位）。

## 2. 并发：七槽填槽

**现行规则只有一条**：每轮最多 7 批（`config.CONCURRENCY['slots']`；`pipeline.py` 内部 `n_slots = min(7, 批数)`）×`_multi_sim_batch_size`（缺省 8）条同提、统一轮询、**即收即补**保持槽位常满；SOP 全文与账户级仲裁见 `wqb-concurrency` §8。`stage_submit_poll` 用线程池并行提交 + 轮询，`--max-rounds > 1` 启用多轮即收即补，`--serial` 一次只提 1 批（排障）。**旧的「单批在飞」规则与固定 5 槽模型已废止**（历史见 CHANGELOG：当时 CANCELLED 的真根因是批内坏表达式连坐兄弟批，不是平台禁止并发 multisim）。

战役目录外的一次性临时批跑不在此列（用 `brain-sim-alphas-in-batch-and-track`）。

## 3. 429 退避（三处各管一段，别混）

| 谁 | 口径 |
|---|---|
| toolkit 传输层 `_lib/api.py::_open_with_retry` | HTTP 429：5 s 起 ×2 倍增，最多 5 次，**优先遵守 `Retry-After`**；`api_call` 的外层退避（同口径）是第二道 |
| MCP 工具（`create_multi_simulation` 等） | 内建 `Retry-After` + 指数退避 |
| 手写 runner（**不该有**：AGENTS.md 禁止一次性脚本 / 手写 requests） | 仅作原理说明见 `wqb-concurrency` §4 |

退避后仍 429 = 账户级槽位被占（孤儿模拟 / 另一条流水线），**降并发用 `WQB_GLOBAL_SLOTS=<n>`**（账户级仲裁，见 `wqb-concurrency` §8.1），不是改 `pipeline.py` 的形参。

## 4. ET 日历日提交配额（`pipeline.py quota`）

- 三条**并行、互不占用**的通道，均 **00:00 ET 重置**（夏 / 冬令时对应 GMT+8 的 12:00 / 13:00，由 `wqb.timeutil` 计算）：`REGULAR_SUBMISSION` 4 / 日；`SUPER_SUBMISSION` 1 / 日；PPA 独立的 `POWER_POOL_SUBMISSION` 1 / 日。旧「48 h 滚动」口径已废止（08-12 一次 48 h 内提交 6 颗全成功证伪）。
- **读额度用 `python Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py --campaign-dir <DIR> quota`，不要靠 `POST /submit` 的响应去读**——POST 就是一次真实提交（RA 红线）。`quota` 数的是 `/users/self/alphas?stage=OS` 里 `dateSubmitted` 落在当日 ET 日的条数（该端点的 `activities/submissions` 只有 yesterday / current / previous / ytd 快照、没有 today，故不用），**不区分通道**：SUPER / PPA 也计入 `used`，所以它是 REGULAR 剩余额度的**保守上界**，精确的分通道读数只在提交响应里（`needs-platform`：需要在有账号的环境里核对）。
- MCP 的 `get_submission_quota` 已于 2026-08-25 移除，**不要依赖它**。硬闸 FAIL 的提交**不消耗**配额（status 保持 UNSUBMITTED）。
- SUPER 的 1 / 日由提交层（`tools/submit_verdict.py` / `super_build.py`）单独把关，`quota` 只看 REGULAR 上限（`thresholds.submit_quota.limit`，缺省 4）。

**配额闸与回测发起是两个独立机制**：`pipeline.py` 的提交配额闸**缺省关闭**（`quota_cfg()['enabled']` = `False`，2026-08-26 用户指令；`tests/unit/01_store_db/test_sd_engine_contracts.py` 钉住），所以配额耗尽**不会**中止回测发起，RA 循环「配额耗尽 → 挂起提交，继续步 2→9」成立。只有区域 `thresholds.json` 显式 `submit_quota.enabled=true` 才会在 `remaining ≤ 0` 时中止（退出码 2），`--force` 越过（它不提交 alpha、也不消耗任何配额，只是不中止回测发起）。

## 5. 凭证与缓存

单进程单登录（`Api` 实例复用，multisim 分支与 per-alpha 循环共享）；凭证链见 SKILL §2。`metrics_cache` 读穿缓存另说：`cache/metrics/<alpha_id>.json` 命中即返、损坏静默回源、写盘原子；`CAMPAIGN_NO_CACHE=1` 或 `--refresh` 强制回源。
