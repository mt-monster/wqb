---
last_verified: 2026-10-04
name: wqb-concurrency
description: "回测被 429 / CONCURRENT_SIMULATION_LIMIT_EXCEEDED 卡住、回测吞吐低、孤儿模拟占槽、要弄清七槽并发口径时使用：并发上限 C 的测定、在飞数锁定原则、孤儿模拟与三类卡住根因、七槽填槽 SOP 的并发纪律。"
layer: L3
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
agent_created: true
---

# WQ Brain 并发挖掘调优

## 职责边界

- **本 skill 负责**：**并发口径与纪律**——账户级并发上限 C（Token-Bucket，C≈7）的测定方法、在飞数锁定原则、孤儿模拟与卡住根因、七槽填槽 SOP 的**并发部分**、429 时怎么降并发。
- **本 skill 不做**：不发起回测本身（`brain-sim-alphas-in-batch-and-track` / toolkit）、不改表达式、不提交；**不管台账、复盘与选波**（那是 RA 步 1 / 步 9：写波结论 `upsert_wave_result`，选波前读 `get_latest_wave` / `tools/step_funnel.py`）。
- **上游 / 下游**：被 `brain-sim-alphas-in-batch-and-track` 与 `wq-brain-campaign-toolkit`（`pipeline.py`）引用；纪律落回调用方的执行参数（批大小 / 账户级并发上限 / 批间隔），不产出独立工件。

> **读者分层**：§1、§4、§5、§8 是**给 agent 的规则**；§2–§3 与 §7 是**给引擎维护者的实现原理**（填槽并发已由 `pipeline.py` 内部锁定，agent 不要手写 runner / 一次性脚本，AGENTS.md 禁止）。

WorldQuant Brain 的「并发模拟数」是**服务端硬性上限 C**，与本地开多少线程无关：本地在飞回测数 = min(本地工作线程数, C)，超过 C 的提交拿到 `429`，白白浪费重试。

## 1. 口径与测定 C（别猜，实测）

**现行模型**：**平台 Token-Bucket，突发容量 C≈7，慢补充约 1 令牌 / 20–40 s**（2026-08 实测；详见 `wq-backtest-monitor` §6）；旧的固定槽位 C=5 是 2026-07 的测量，已作废。⚠ **平台容量 C≈7 是平台事实，未变；但本工作区的「操作档」= 2**（2026-10-04 由 7 降为 2：多会话 / 多流水线共享同一账户池，保守留余量给并行的其它 region 流水线）。数字的唯一来源是 `src/wqb/config.py::CONCURRENCY`：`slots=2`（在飞 multisim 上限）、`burst_capacity=2`、`refill_sec_per_token=(20, 40)`。同一表里还有保守档 `safe_instant_submits=2` 与 `min_batch_interval_sec=45`——**目前没有代码读取这两个值**（它们是「刚遇 429 风暴 / 有孤儿占槽」时的手动保守做法）；`pipeline.py` 实际按 `min(2, 批数)` 同提，`WQB_GLOBAL_SLOTS` 可临时整体覆盖（`0` = 关闭仲裁）。**「平台容量 C≈7（上限）」与「本工作区操作档 2（我们主动留的余量）」是两个不同的量，别当成同一个包络的两种说法。**

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

若信号量只在 `POST` 处 `with`，轮询时信号量已释放 → 实际在飞数 = 工作线程数，会超额提交、疯狂 429。这是最隐蔽的 bug。`pipeline.py` 已按此实现（`n_slots = min(2, 批数)`），改引擎时保持。

## 3. 线程数（给引擎维护者）

在飞数 = min(工作线程, C)；要打满吞吐需**工作线程 ≥ C**，推荐 **C + 1**（多 1 个缓冲线程，随时补位）。例：C = 7 → 信号量 7、8 个工作线程。（旧文的「C=5、每数据集 3 线程 × 2 数据集」是 2026-07 的数字。）

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

战役目录（`tracking/<REGION>/`）内的正式 wave 回测走七槽填槽（§8）；退避 / 熔断参数化由 toolkit `pipeline.py` 内部提供（缺省值与 `poll` 节覆盖见 `wq-brain-campaign-toolkit/references/poll-and-quota.md`）。

## 8. 🌟 七槽填槽模式（并发纪律）

**实证**：7 个 multisim（各 8 条）同时提交全部被接受且 ~90 秒同步 COMPLETE，连续多波 0 ERROR / 0 连坐。旧「多批 multisim 会 CANCELLED」的结论实为批内坏表达式连坐所致，门禁后已可安全并行。

**SOP（并发部分）**：

1. **提交前门禁**：每批表达式先过 `tools/wave_gate.py`（RA 步 5；含 toolkit `gate.py`），确认算子签名 / 字段白名单 / 单位语义合规，杜绝批内 ERROR 连坐。
2. **7 批同提**：`mcp__wq-brain-http__create_multi_simulation`（异步模式）每轮同时提交 7 批 × 8 条；**禁止串行「提交 → 等完 → 再提」**（槽位利用率仅 ~14%）。**`validate_fields` 分场景**：**验活探针**（新字段先验活幽灵字段，RA 步 3）用 `true`；**正式批**用 `false`（避免预检超时）。
3. **统一轮询与收批**：用 `mcp__wq-brain-http__harvest_multisim_alphas` 一次取回 multisim 全部子 alpha 详情（含 `checks`；把旧的「`lookINTO_SimError_message` → children → `get_alpha_details` 逐 ID」三段链压成 2 次调用），再 `harvest_multisim_results` 入库；批内 ERROR 的定位用 `lookINTO_SimError_message`。**不用 `get_user_alphas`**：它按时间排序拉摘要列表，无法保证目标 ID 全在里面，也可能不含完整 `checks`。
4. **即收即补**：任一批 COMPLETE 立即回收筛选，空槽当轮补新批，保持 7 槽常满，单轮吞吐 ×7。
5. **批间间隔**：缺省不设（七槽同提）；遇 429 时按 §8.1 降账户级并发，并把批间隔拉到 ≥ 45 s（令牌约 1 个 / 20–40 s 补充）。

**台账与复盘不在本 SOP 里**：写波结论（`upsert_wave_result`）、「未写结论不得开下一波」、选波前读 `get_latest_wave` / `step_funnel`、多样性评估，都是 RA 步 1 / 步 9 的事。现行的「台账同步门」= 开波三道区域闸（DB 判定）+ `tools/step_funnel.py`；`check_ledger_sync.py`（`tools/` 与 toolkit 各一份）校验的是 `runs/` 批次字母与 `WAVE_LEDGER.md`——**文件时代**的做法，仅当战役目录仍保留这些文件时才有意义。

**注意**：提交配额（ET 日历日 REGULAR 4 + SUPER 1 + PPA 1）与回测并行槽位是**两个独立机制**：`pipeline.py` 缺省不因提交额度中止回测发起（区域 `thresholds.submit_quota.enabled=true` 才启用该闸，见 toolkit `references/poll-and-quota.md` §4）。

### 8.1 账户级槽位仲裁（跨进程；`_lib/slots.py`）

`pipeline.py` 每个进程各自把并发锁在 `min(2, 批数)`；**两条流水线同跑**（IND w171 + JPN w8 实测）在飞 10–13 个 multisim，超过账户级 C≈7，此前只能靠 429 退避被动兜底。现由 toolkit `_lib/slots.py` 做主动仲裁：

- 目录 `<repo>/logs/_slots/` 下**每个在飞 multisim 一个 token 文件**（内容 pid / multisim id / 时间戳）；提交前 `acquire()` 数活 token，≥ cap 则轮询等待，拿到即写 token；进入终态后 `release()` 删 token。
- **陈旧 token**（进程已死，或超过 max_age 秒）自动回收，避免崩溃残留占坑；任何异常都降级为「不仲裁」（打印 warn），**绝不阻断提交**。
- 环境变量：`WQB_GLOBAL_SLOTS`（账户级 cap，缺省 2；`0` = 关闭仲裁）、`WQB_SLOTS_DIR`（目录）。
- **429 时怎么降并发**（可执行手段，RA 步 6 的故障表只保留指向这里的一句）：① 等待退避（MCP 内建 `Retry-After` + 指数）；② 设 `WQB_GLOBAL_SLOTS=<n>` 降账户级并发（保守档 2）；③ 批大小 ≤ 5。**注意**：外部往 `pipeline.py` 传非 2 的并发形参**只会收到 warning，不会降并发**（并发在 pipeline 内部锁定）。

### 8.2 🌟 多会话并行挖掘（同一账户多开时怎么不打架）

**问题**：同一 WQ 账户下**多个 WorkBuddy 会话同时在挖 alpha**（用户常态）。账户级 C≈7 是**全局共享**的，两个会话各按满槽提交（历史缺省 7）= 在飞 14 → 稳定 429 风暴；而 `pipeline.py` 内的 `min(2, 批数)` 只锁**本进程**，看不见隔壁会话。

**根因三层（按修改收益排序）**：
1. **跨进程无仲裁**（最常见）：裸脚本（`_submit_single.py` 这类）既不读也不写 `logs/_slots/`，会与 pipeline 叠加超 C。已修：
   - `pipeline.py` 路径 → 自带 `slots.acquire/release`（`_lib/slots.py`），天然仲裁。
   - 自写脚本 → **必须 `from _lib import slots` 并在 run_backtest 最外层 `acquire()`**；做不到写 token 时至少**只读** `_live_foreign_slots()` 把本地并发降到 `max(1, cap - foreign)`，并加 429 指数退避（1→2→4→8→16→32s，尊重 `Retry-After`）。`logs/_submit_single.py` 已按「只读 + 退避 + `--cap`/`--slice`」实现，可作模板。
2. **服务端孤儿占槽**（最阴，见 §4）：`TaskStop` 强杀后服务端回测仍在跑、占满 C，**本地读 slots 显示 0 占用但提交仍 429** —— 这就是「外部已占=0 却持续 429」的判定依据。对策：**绝不再 TaskStop**、纯退避等释放（拥堵下数分钟），**不因 429 丢候选**。
3. **配额 vs 槽位两码事**：提交配额（ET 日 REGULAR 4 + SUPER 1）不影响回测并行；回测 429 永远别误判成「配额用完」。

**多会话分配的标准做法（按推荐度排序）**：
| 方案 | 做法 | 适用 |
|---|---|---|
| **A. 统一走 pipeline**（首选） | 各会话都通过 `pipeline.py` / toolkit 发回测 → 自动共享 `logs/_slots/` 仲裁，无需手动调参 | 常规战役 wave（多数情况） |
| **B. 人工切分账户预算** | 设 `WQB_GLOBAL_SLOTS`；N 个会话各设 `≈ 7/N`（2 会话 → 各 3–4；3 会话 → 各 2–3），**两端都必须设**，否则设的一侧让出、没设的一侧仍吃满 7 | 会话用了自写脚本 / 混合路径 |
| **C. 分工到数据面** | 各会话**挖不同数据集 / 不同机制维度**（如本会话 amt 族、隔壁 V 族），从源头减少同族重复；配合 A 或 B | 长期多会话并行（用户现状，推荐叠加） |

**硬纪律（多会话通用）**：
- **绝不 `TaskStop` / 强杀挖矿进程**（制造孤儿，见第 2 层）；要停就让其自然跑完，或优雅退出（脚本收到信号先释放自己 token）。
- **批间 ≥ 45 s**（令牌慢补充档），429 后拉长到 ≥ 60 s。
- **每个会话在日志开头打印 `[slots] cap / 外部已占 / 本脚本并发` 诊断行**，一眼可见是否叠加。
- 判断「该不该等」：先 `live_tokens()` 看本地占用，再看提交是否 t=0 即 429（→ 孤儿/邻居占槽，退避等）；两者都空还 429，则大概率全平台拥堵，同样只能等。

## 情景卡

### 情景 WC-A　新一轮开波后全 429、接受数 0

- **前置状态**：刚 `TaskStop` 过上一个挖矿进程，或另一条流水线在跑。
- **步骤**：① 不再 `TaskStop`；② `logs/_slots/` 看有几个活 token（两条流水线同跑会超 7）；③ 短退避重试等孤儿释放；④ 仍卡 → `WQB_GLOBAL_SLOTS=6` 并拉开批间隔 ≥ 45 s。
- **完成定义**：接受数随孤儿释放回升，没有候选因限流被丢弃。
- **反例**：把 429 当「表达式有问题」去改式子；强杀进程「清场」。

### 情景 WC-B　同事问「我该开几个线程」

- **步骤**：告诉对方**别开**——七槽由 `pipeline.py` 内部锁定，外部传并发形参只收 warning；要提高吞吐只能保证 7 槽常满（即收即补），而不是加线程。
- **反例**：手写 runner 并把信号量只包在 `POST` 上。

### 情景 WC-C　「我多个会话同时在挖，怎么防 429」

- **判定顺序**：① `logs/_slots/` 有几个活 token（本地叠加）→ ② 提交是否 **t=0 即 429**（是 → 服务端孤儿或邻居会话占槽，非表达式问题）→ ③ 是否走了裸脚本而非 pipeline。
- **标准答复**：走 §8.2 三方案——**A 统一 pipeline**（自动仲裁）→ **B 设 `WQB_GLOBAL_SLOTS≈7/N` 于所有会话** → **C 各会话挖不同数据集/机制维度**。叠加纪律：never TaskStop、批间 ≥45 s、开头打印 slots 诊断行。
- **反例**：只在一个会话设 `WQB_GLOBAL_SLOTS`（另一侧仍吃满 7，等于没设）；把 429 当表达式错误改式子；强杀进程「清场」制造更多孤儿。

### 情景 WC-D　「本地 slots 显示 0 占用，但提交一直 429」

- **根因**（本区实测，2026-10-04）：不是本地进程，是**服务端孤儿模拟**占满 C（此前多次 timeout 截断收割 + 大批派发造成）。
- **步骤**：① 纯退避重试（1→2→4→8→16→32 s），**绝不 TaskStop**；② 用探针（一条极简表达式 `rank(close)`）测试是否 201；③ 201 一旦出现即说明孤儿释放，正常派发。
- **完成定义**：探针 201，接受数回升，无候选因限流丢弃。

### 情景 WC-E　「多会话查 prod 相关性，每次都等很久」

- **先问一句**：是**真慢**还是**没缓存**？这两者的修法完全不同。
- **根因**（2026-10-04 定位）：prod 结果的缓存后端此前**只有 Redis**；本机 Redis 常未启动
  → `redis_client=None` → `_get_cached_data/_set_cached_data` 读写**全 no-op**
  → 每次查询都重打平台**单账号单并发**接口（每颗 1-5 分钟），多进程还抢同一把锁
  （拿不到 → `correlation_busy`，等 180 s）。对照：**self 相关性有文件缓存**
  （`world-quant-brain-mcp/downloads/os_pnl_pool_<region>_<universe>_delay<N>.pkl`）所以秒回。
- **修法（2026-10-04 已落地）**：prod 缓存改**两级 Redis → wqb 库**。
  `check_correlation` 命中 `data/wqb.db::alpha_corr_cache` 即直接返回，不再打平台；
  平台算成功后同时写回该表。**独立表**（不挂 `alphas`）是因为仿真 alpha 不在 `alphas` 里。
- **并行时的省时纪律**：先用**免费**的 `check_self_correlation`（本地 PnL 池计算）筛掉不达标的，
  只对少数候选查 prod；已有值的直接 `CampaignStore.get_corr_cache(id)` 读库，别重查。
- **反例**：把 prod 慢当成「平台坏了」；对同一批 alpha 反复查而不落库；
  用 `refresh=True` 做无差别刷新（那是**强制作废缓存**，代价是重新排队）。

