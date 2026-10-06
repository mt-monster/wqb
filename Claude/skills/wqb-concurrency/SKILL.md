---
last_verified: 2026-09-29
name: wqb-concurrency
description: "回测被 429 / CONCURRENT_SIMULATION_LIMIT_EXCEEDED 卡住、回测吞吐低、孤儿模拟占槽、要弄清填槽并发口径时使用：并发上限 C 的测定、在飞数锁定原则、孤儿模拟与三类卡住根因、七槽填槽 SOP 的并发纪律。"
layer: L3
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
agent_created: true
---

# WQ Brain 并发挖掘调优

## 职责边界

- **本 skill 负责**：**并发口径与纪律**——账户级并发上限 C（Token-Bucket，C≈7）的测定方法、在飞数锁定原则、孤儿模拟与卡住根因、填槽 SOP 的**并发部分**、429 时怎么降并发。
- **本 skill 不做**：不发起回测本身（`brain-sim-alphas-in-batch-and-track` / toolkit）、不改表达式、不提交；**不管台账、复盘与选波**（那是 RA 步 1 / 步 9：写波结论 `upsert_wave_result`，选波前读 `get_latest_wave` / `tools/step_funnel.py`）。
- **上游 / 下游**：被 `brain-sim-alphas-in-batch-and-track` 与 `wq-brain-campaign-toolkit`（`pipeline.py`）引用；纪律落回调用方的执行参数（批大小 / 账户级并发上限 / 批间隔），不产出独立工件。

> **读者分层**：§1、§4、§5、§8 是**给 agent 的规则**；§2–§3 与 §7 是**给引擎维护者的实现原理**（槽位数已由 `pipeline.py` 内部锁定，agent 不要手写 runner / 一次性脚本，AGENTS.md 禁止）。

WorldQuant Brain 的「并发模拟数」是**服务端硬性上限 C**，与本地开多少线程无关：本地在飞回测数 = min(本地工作线程数, C)，超过 C 的提交拿到 `429`，白白浪费重试。

## 1. 口径与测定 C（别猜，实测）

**现行模型**（2026-08 实测）：**Token-Bucket，突发容量 C≈7，慢补充约 1 令牌 / 20–40 s**（详见 `wq-backtest-monitor` §6）；旧的固定槽位 C=5 是 2026-07 的测量，已作废。数字的唯一来源是 `src/wqb/config.py::CONCURRENCY`。

> **现行采用水位 = `slots=2`**（2026-10-06 用户定案，从实测上限 C≈7 下调）：
> ① 多条流水线 / 并行会话共用同一账号的槽位与配额，跑满上限会频繁 429 + 退避，总吞吐反而下降；
> ② 7 槽直接诱发过 2026-10-02 的 `pipeline` 主线程自锁（正解是 `acquire(nonblock=True)`，
>    cap=2 是叠加的第二重保险，见 §8.1）。
> 临时提高用 `WQB_GLOBAL_SLOTS=<n>`，不要改常量、也不要往 `pipeline.py` 传并发形参。
>
> 键位现状：`slots=2`（= 在飞 multisim 上限）、`burst_capacity=2`、`refill_sec_per_token=(20, 40)`。
> 同一表里还有保守档 `safe_instant_submits` 与 `min_batch_interval_sec=45` ——
> **目前没有代码读取这两个值**，它们是「刚遇 429 风暴 / 有孤儿占槽」时的手动保守做法
> （`WQB_GLOBAL_SLOTS=1` 且批间 ≥ 45 s，见 §8.1）。
> **cap（在飞上限）与保守档余量是两个不同的量，别当成同一个包络的两种说法。**

需要**复测** C 时（正常战役不需要）：

1. **先停掉所有本地挖矿进程**，让「自己制造的孤儿」释放槽位（见 §4）。
2. 用**挖矿脚本里真实的 `SETTINGS`** 发阶梯提交。⚠️ 常见坑：`language` 必须是 `"FASTEXPR"`（不是 `"FAST"`），用错会 **400 而非 429**，测不出 C。
3. 并发提交 N（≥ C+3）条极简表达式（如 `rank(close)`），间隔 0.2–0.3 s。
4. 观察：**首批连续 `201` 接受数 = C**（第 C+1 条起 `429`）。
   - 429 报文形如 `{"detail":"CONCURRENT_SIMULATION_LIMIT_EXCEEDED"}` —— **不含数字**，读不到限额，只能靠阶梯提交数出来。
   - `/users/self` 也**不含**并发 / 模拟限额字段（已全量遍历确认），别再查它。

## 2. 把本地在飞数锁到 C（给引擎维护者）

信号量必须包住**整条** `run_backtest`（提交 `POST` + 轮询 `Location` 直到完成），而**不只是 `POST` 那一瞬间**：

```python
def run_backtest(self, expr, settings, ...):
    with self._sub_sem:          # ← 最外层，覆盖 post + 轮询全程
        ...                      # POST /simulations，429 短退避重试；轮询 prog_url 直到完成
        return {"platform_id": alpha_id, ...}
self._sub_sem = threading.Semaphore(C)   # C 取自 config.CONCURRENCY['slots']，不要硬编码
```

若信号量只在 `POST` 处 `with`，轮询时信号量已释放 → 实际在飞数 = 工作线程数，会超额提交、疯狂 429。这是最隐蔽的 bug。`pipeline.py` 已按此实现（`n_slots = min(CONCURRENCY['slots'], 批数)`），改引擎时保持。

## 3. 线程数（给引擎维护者）

在飞数 = min(工作线程, C)；要打满吞吐需**工作线程 ≥ C**，推荐 **C + 1**（多 1 个缓冲线程，随时补位）。例：cap = 2 → 信号量 2、3 个工作线程。（旧文的「C=5、每数据集 3 线程 × 2 数据集」是 2026-07 的数字。）

## 4. 🚨 孤儿模拟占槽（最阴的坑）

`TaskStop` / 强杀本地 Python 进程时，**服务端已提交的回测仍在跑**，一直占用账户的 C 个槽位，新提交全部 429（t = 0 就被占满）。

- 这些孤儿**无法查询也无法取消**（`GET /simulations` 405，`/users/self/simulations` 404），只能等它们**在服务端自己跑完**才释放（拥堵下每条数分钟）。
- 应对：对 429 做**短退避重试**（MCP 工具与引擎已内置，口径见 toolkit `references/poll-and-quota.md` §3），**绝不因限流丢弃候选**；提交成功数会随孤儿释放自然回升。
- ⚠️ 探测并发时自己提交的探针回测也会变成孤儿，释放前会占满槽位、让后续 mining 初期全 429——这是自找的延迟，耐心等其释放，**不要再 `TaskStop`**（会制造更多孤儿）。

## 5. 判定卡住的三类根因

| 现象 | 根因 | 对策 |
|---|---|---|
| `rank(close)` 也卡 0.1%–0.35% 进度零进展 | WQ 全局集群拥堵（排队） | 只能等；缩短 `testPeriod` 仅降单任务算力、不降排队 |
| 提交全 429、接受数 0 | 孤儿模拟占满 C 个槽 | 短退避重试，等孤儿释放 |
| 提交全 400 | `SETTINGS` 非法（如 language / unitHandling 互斥） | 用脚本真实 SETTINGS 复测 |

「卡住」的判据分两层，别混：**在飞回测**（引擎 poller）progress 连续 `WAIT_THRESHOLDS.sim_stall_min`（60 分钟）无变化判 `STALLED`、总时长超 `sim_timeout_min`（360 分钟）判超时；**兼容 CLI**（`batch_simulator.py` 的 CSV 进度）看 `brain-sim-alphas-in-batch-and-track` 的规则。

## 6. 凭据

**agent 不读取 `.env`**（AGENTS.md）、不打印凭据、不把口令放命令行——凭据只由脚本 / MCP 服务自己从环境变量（标准名 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`）加载。给脚本作者的提示：后台任务的 cwd 不一定是项目目录，加载 `.env` 用相对 `__file__` 的绝对路径，别依赖 `cd` 或 `os.path.abspath(".")`。

## 7. 战役场景：参数化退避

战役目录（`tracking/<REGION>/`）内的正式 wave 回测走填槽（§8）；退避 / 熔断参数化由 toolkit `pipeline.py` 内部提供（缺省值与 `poll` 节覆盖见 `wq-brain-campaign-toolkit/references/poll-and-quota.md`）。

## 8. 🌟 填槽模式（并发纪律）

**实证**：7 个 multisim（各 8 条）同时提交全部被接受且 ~90 秒同步 COMPLETE，连续多波 0 ERROR / 0 连坐。旧「多批 multisim 会 CANCELLED」的结论实为批内坏表达式连坐所致，门禁后已可安全并行。

**SOP（并发部分）**：

1. **提交前门禁**：每批表达式先过 `tools/wave_gate.py`（RA 步 5；含 toolkit `gate.py`），确认算子签名 / 字段白名单 / 单位语义合规，杜绝批内 ERROR 连坐。
2. **7 批同提**：`mcp__wq-brain-http__create_multi_simulation`（异步模式）每轮同时提交 7 批 × 8 条；**禁止串行「提交 → 等完 → 再提」**（槽位利用率仅 ~14%）。**`validate_fields` 分场景**：**验活探针**（新字段先验活幽灵字段，RA 步 3）用 `true`；**正式批**用 `false`（避免预检超时）。
3. **统一轮询与收批**：用 `mcp__wq-brain-http__harvest_multisim_alphas` 一次取回 multisim 全部子 alpha 详情（含 `checks`；把旧的「`lookINTO_SimError_message` → children → `get_alpha_details` 逐 ID」三段链压成 2 次调用），再 `harvest_multisim_results` 入库；批内 ERROR 的定位用 `lookINTO_SimError_message`。**不用 `get_user_alphas`**：它按时间排序拉摘要列表，无法保证目标 ID 全在里面，也可能不含完整 `checks`。
4. **即收即补**：任一批 COMPLETE 立即回收筛选，空槽当轮补新批，保持 7 槽常满，单轮吞吐 ×7。
5. **批间间隔**：缺省不设（N 槽同提，N = `CONCURRENCY['slots']`）；遇 429 时按 §8.1 降账户级并发，并把批间隔拉到 ≥ 45 s（令牌约 1 个 / 20–40 s 补充）。

**台账与复盘不在本 SOP 里**：写波结论（`upsert_wave_result`）、「未写结论不得开下一波」、选波前读 `get_latest_wave` / `step_funnel`、多样性评估，都是 RA 步 1 / 步 9 的事。现行的「台账同步门」= 开波三道区域闸（DB 判定）+ `tools/step_funnel.py`；`check_ledger_sync.py`（`tools/` 与 toolkit 各一份）校验的是 `runs/` 批次字母与 `WAVE_LEDGER.md`——**文件时代**的做法，仅当战役目录仍保留这些文件时才有意义。

**注意**：提交配额（ET 日历日 REGULAR 4 + SUPER 1 + PPA 1）与回测并行槽位是**两个独立机制**：`pipeline.py` 缺省不因提交额度中止回测发起（区域 `thresholds.submit_quota.enabled=true` 才启用该闸，见 toolkit `references/poll-and-quota.md` §4）。

### 8.1 账户级槽位仲裁（跨进程；`_lib/slots.py`）

`pipeline.py` 每个进程各自把并发锁在 `min(CONCURRENCY['slots'], 批数)`；**两条流水线同跑**（IND w171 + JPN w8 实测）在飞 10–13 个 multisim，超过账户级 C≈7，此前只能靠 429 退避被动兜底。现由 toolkit `_lib/slots.py` 做主动仲裁：

- 目录 `<repo>/logs/_slots/` 下**每个在飞 multisim 一个 token 文件**（内容 pid / multisim id / 时间戳）；提交前 `acquire()` 数活 token，≥ cap 则轮询等待，拿到即写 token；进入终态后 `release()` 删 token。
- **陈旧 token**（进程已死，或超过 max_age 秒）自动回收，避免崩溃残留占坑；任何异常都降级为「不仲裁」（打印 warn），**绝不阻断提交**。
- 环境变量：`WQB_GLOBAL_SLOTS`（账户级 cap，缺省 2；`0` = 关闭仲裁）、`WQB_SLOTS_DIR`（目录）。
- **429 时怎么降并发**（可执行手段，RA 步 6 的故障表只保留指向这里的一句）：① 等待退避（MCP 内建 `Retry-After` + 指数）；② 设 `WQB_GLOBAL_SLOTS=<n>` 降账户级并发（要更保守就设 1；**大于现行 cap 的值是升并发，不是降**）；③ 批大小 ≤ 5。**注意**：外部往 `pipeline.py` 传与 `CONCURRENCY['slots']` 不同的并发形参**只会收到 warning，不会降并发**（并发在 pipeline 内部锁定）。

## 情景卡

### 情景 WC-A　新一轮开波后全 429、接受数 0

- **前置状态**：刚 `TaskStop` 过上一个挖矿进程，或另一条流水线在跑。
- **步骤**：① 不再 `TaskStop`；② `logs/_slots/` 看有几个活 token（两条流水线同跑会超出 cap）；③ 短退避重试等孤儿释放；④ 仍卡 → `WQB_GLOBAL_SLOTS=1` 并拉开批间隔 ≥ 45 s。
- **完成定义**：接受数随孤儿释放回升，没有候选因限流被丢弃。
- **反例**：把 429 当「表达式有问题」去改式子；强杀进程「清场」。

### 情景 WC-B　同事问「我该开几个线程」

- **步骤**：告诉对方**别开**——槽位数由 `pipeline.py` 内部锁定，外部传并发形参只收 warning；要提高吞吐只能保证槽位常满（即收即补），而不是加线程。
- **反例**：手写 runner 并把信号量只包在 `POST` 上。
