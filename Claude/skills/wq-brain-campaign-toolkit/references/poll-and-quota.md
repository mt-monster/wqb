# 轮询 / 熔断 / 并发 / 提交配额

## 轮询退避参数组（thresholds.json 可加 "poll" 节覆盖）
| 参数 | 默认 | 含义 |
|---|---|---|
| init_interval | 20s | 初始轮询间隔 |
| backoff_factor | 1.5 | 指数退避因子 |
| max_interval | 120s | 间隔封顶 |
| stall_minutes | 60 | progress 60 分钟无变化判 STALLED（KOR waveT 卡 24h 教训） |
| timeout_minutes | 360 | 总超时 |

TERMINAL = {COMPLETE, ERROR, CANCELLED}。COMPLETE → 自动拉全量 child alpha 指标；ERROR → **全量 child 逐个取 error**（[:8] 截断是历史 bug，会漏 >8 批次的错误定位）。

## 单批在飞规则（已废弃，2026-08-16 起由填槽模式取代；2026-08-25 更新为七槽）
~~串行提交循环：上一批到 TERMINAL 才提下一批。根因：平台对同账号并发 multisim 会让后到批无错误信息地 CANCELLED~~。
**纠正（2026-08-16）**：当时 CANCELLED 的真根因是**批内坏表达式 ERROR 连坐取消兄弟批**（KOR 批X实证本身也是级联现象），并非平台禁止并发 multisim。四重门禁（tools/expr_lint.py）后实证：5 批 multisim 同提全部被接受且同步 COMPLETE，连续 2 波 80 条 0 连坐。**新铁律：每轮 7 批×8 条同提（2026-08-25 更新 5→7）、统一轮询、即收即补保持槽位常满**，SOP 全文见 `wqb-concurrency` SKILL.md §8。batch_size 仍读 settings `_multi_sim_batch_size`（默认 8）。**pipeline.py 已改造为七槽填槽并发实现（2026-08-21 起，2026-08-25 更新 5→7）**：`stage_submit_poll` 用 ThreadPoolExecutor 并行提交+轮询 N 批（N=min(5, 批数)），支持单轮（默认）与多轮即收即补（`--max-rounds>1`）两种模式。
战役目录外的一次性临时批跑不在此列（可用 brain-simAlphasinBatch-and-track 多批并发）。

## 429 指数退避
api_call 包装：HTTP 429 时 sleep 5s 起、×2 倍增、最多 5 次重试；非 429 直接抛。

## ET 日历日提交配额（pipeline quota 子命令）
- 提交配额 = **REGULAR 4 颗/ET 日历日 + SUPER 1 颗/ET 日历日**，**00:00 ET（= 12:00 GMT+8）重置**。旧"48h 滚动"口径已废止（08-12 一次 48h 内提交 6 颗全成功证伪）。
- `submission_quota()` 按 ET 日历日（简化口径 UTC-4）聚合 `/users/self/activities/submissions` 统计当日已提交数；取不到 activities 时回退按 OS alphas 的 `dateSubmitted` ET 日聚合。
- MCP 的 `mcp__wq-brain-http__get_submission_quota` 已于 2026-08-25 移除，**不要依赖它**；剩余额度从 submit 响应 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 的 `value/limit` 读（value 从 0 起计数，limit=4/1）。
- ⚠️ **SUPER 提交上限 1/日独立于 REGULAR 4/日**——本闸只看 REGULAR；SUPER 由提交层（`tools/submit_verdict.py`/submit 响应）单独把关。
- 硬闸 FAIL 的提交**不消耗**配额（status 保持 UNSUBMITTED）。
- pipeline run 默认在配额耗尽时中止，`--force` 强行继续（会用光当日额度，慎用）。

## 凭证与登录
单进程单登录（Api 实例复用，multisim 分支与 per-alpha 循环共享）；凭证链见 SKILL.md §4。metrics_cache 读穿缓存：cache/metrics/<alpha_id>.json 命中即返、损坏静默回源、写盘原子；`CAMPAIGN_NO_CACHE=1` 或 `--refresh` 强制回源。
