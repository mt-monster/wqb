# wqb 项目并发写锁审计（2026-09-20）

> 触发事件：2026-09-20 13:16-13:47 多会话并发下 `database is locked` 事故——GBR 会话 build_wave 两次写库失败、GLB 会话 wave_gate（PID 27892）等锁 30 分钟（CPU 0.016s）。
> 方法：全库 grep `sqlite3.connect`（40+ 处）+ 进程实测（psutil）+ 事务模式抽读。

## 1. 现状图景

### 1.1 写者清单（按持锁风险排序）

| # | 写者 | 写的表 | 连接模式 | 持锁风险 |
|---|---|---|---|---|
| 1 | `pipeline.py`（batch_track 主体，detached 30-60min） | backtest_results / wave_results / ledger_kv（checkpoint） / region_kb 刷新 | CampaignStore 长生命周期连接（timeout=30+WAL） | **高**：连接活全程，若事务粒度粗则单事务跨收批+复盘多阶段 |
| 2 | `wqb-db` MCP server 的批量节点（workflow_auto_harvest / auto_review / auto_pyramid） | backtest_results / salvage_pool / wave_results | 每工具调用新建连接（wqb_db_mcp.py:54，timeout=30+WAL） | **高**：节点流程 = 网络拉取+写库交替，若不在每步后 commit 则锁跨全流程 |
| 3 | `wave_gate.py`（每波门禁） | gate_results / expressions(status) | CLI 短事务 | 中：写频率高，遇长锁即排队 |
| 4 | `build_wave.py` | expressions / waves（`_ensure_wave` INSERT） | CLI 短事务 | 中（今天即在此失败） |
| 5 | GEM `headless_runner/run.py` | expressions（一次 90-518 条） | run.py:360 **裸 connect** | 中：批量落库单事务，秒级 |
| 6 | `submit_queue.py verify` ×3 实例 | submit_ready | timeout=30，逐条 commit（tools/submit_queue.py:347） | **低**（已做对：网络在事务外、逐条落盘） |
| 7 | `scan_fields.py` / `harvest_multisim_results` | fields / backtest_results | 短事务 | 低-中 |
| 8 | `campaign_mutex.py`（互斥仲裁本体） | ledger_kv | timeout=10 | **零调用方——存在但未接线** |

### 1.2 连接配置分层（不均衡是主因之一）

| 层 | 配置 | 状态 |
|---|---|---|
| `src/wqb/store/campaign.py:79` | timeout=30 + WAL + synchronous=NORMAL | ✅ 规范 |
| `wqb_db_mcp.py:54` | timeout=30 + WAL（每调用新建） | ✅ 规范 |
| `tools/lib/wqb_db.py`（连接工厂） | WAL + busy_timeout=5000 | ✅ 但**仅 tools 局部引用** |
| `src/wqb/workflow/nodes/*.py` | **~15 处裸 `sqlite3.connect`（无 timeout → 默认 5s）** | ❌ |
| `Claude/skills/*/scripts/`（budget_planner / distill_experience / os_feedback / family_atlas / feature_engineering） | 裸 connect | ❌ |
| GEM `run.py:360`、`memory/db.py:51`、`idea_store.py:48`、`workflow/_common.py:108,722` | 裸 connect | ❌ |

### 1.3 WAL 演进史（前人审计已指出方向）

- `reports/db_schema_audit_2026-08-26.md`：当时 journal_mode=delete，**建议改 WAL** → 后已落地（今天 `-wal/-shm` 文件存在证实）。
- `output_report/skills_review_and_mining_optimization_20260912.md` R3：**「连接工厂统一 PRAGMA」建议未全面落实**——只有 tools 层接了工厂。
- `docs/submit_queue_design.md:237`：已预告「本表会被 MCP/CLI/多钩子并发写」。

### 1.4 今天事故成因链（实测证据）

1. 多会话并行：GBR 战役（本会话）+ GLB wave_gate（27892）+ submit_queue verify ×3（12000/33600/34964）。
2. **MCP server 实例积累**：7 个 wqb-db + 10 个 wq-brain-http 常驻（会话重连旧实例不退出）——连接基数放大竞争面。
3. WAL 模式下单写者串行：**某个写者的长事务（≥30min）饿死所有其他写者**——27892 以 CPU 0.016s 等锁 30 分钟为直接证据；候选长锁源 = #1/#2 的「流程级事务」（网络+写库交替不逐步 commit）。
4. 竞争写者的 busy_timeout 不一（5s/10s/30s）——短 timeout 者率先报错退出（build_wave 两次失败即此）。

## 2. 针对性方案（四层，P0→P2）

### L1 连接层统一（P0，治散）——一处工厂，全库收口

- 把 `tools/lib/wqb_db.py` 提升为规范连接工厂（移入 `src/wqb/store/_conn.py`，tools 层保留 re-export）：
  ```python
  def connect(db=DB_PATH, timeout=60.0):
      conn = sqlite3.connect(db, timeout=timeout)
      conn.execute("PRAGMA journal_mode=WAL")      # 幂等
      conn.execute("PRAGMA busy_timeout=60000")    # 全库统一 60s
      conn.execute("PRAGMA synchronous=NORMAL")
      return conn
  ```
- 替换全部裸 connect（清单见 §1.2 ❌ 行，约 20 处）：workflow/nodes 15 处 + skills 5 处 + GEM run.py + memory 两处。
- 效果：所有写者在锁上排队 60s 而非 5s 即报错——今天的 build_wave 失败直接消失。
- 验收：`grep -rn "sqlite3.connect"` 仅允许出现在工厂文件与 wqb_db_mcp.py。

### L2 事务纪律（P0，治长锁）——两条硬规则 + 审计探针

- **规则 1：网络调用绝不进入写事务**。模式 = fetch(网络) → commit → fetch → commit（`submit_queue.py verify` 已是范本，317-352 行）。重点排查：workflow_auto_harvest / auto_review / auto_pyramid 三个节点与 pipeline.py 收批路径——凡「conn 开着拉平台 API」的循环改为每步 commit。
- **规则 2：批量写分片 commit**（≤500 行或 ≤2s/事务）。GEM 518 条落库、harvest 批量 upsert 适用。
- **审计探针**：新增 `tools/db_lock_audit.py`——每 30s 起 `BEGIN IMMEDIATE` 探针记录「等待时长 + 当时活跃写者」（结合 `logs/_slots/` token 与进程枚举），锁等待 >10s 即告警落台账 `db_lock_events`。常态化运行后可精确定位长锁源（今天靠进程 CPU 反推，探针可直接钉死）。

### L3 写锁调度（P1，治并发重叠）——把 campaign_mutex 接线 + 与 slots 合流

- `campaign_mutex.py`（零调用方）升级为 **DB 写锁 token**：`acquire-db-write --ttl 120`，用 `ledger_kv` 行 CAS + TTL 自愈（进程崩溃自动过期，与现有设计一致）。
- 五大写者强制接线（workflow 节点内置、CLI 显式 import）：`batch_track(pipeline)` / `wave_gate` / `build_wave` / `harvest*` / `GEM 落库`。
- **与 `logs/_slots/`（`_lib/slots.py` 账户级槽位 token）合流为同一套文件 token 机制**，加一类 `db-write` token——避免两套仲裁并行。
- 语义保持 soft：TTL 自愈、抢不到则指数退避（10s→20s→40s，上限 60s×3 后报错并提示竞争者 PID）。

### L4 会话级治理（P0 止血 + P2 治本）

- **P0 止血**：清理 WAL 积压 `PRAGMA wal_checkpoint(TRUNCATE)`（无写者窗口执行）；删除 13:13 的 stuck shm 备份文件。
- **P0 止血**：wqb_db_mcp.py / main.py 启动时清理孤儿实例——psutil 检测「同 cmdline 且 PPID 已死/超龄」的旧 server，自动 kill + 日志（今天 7+10 个实例就是来源）。
- **P2 错峰**：战役写库计划表进 ledger（region×wave×预计写窗口），多会话开工前 `campaign_mutex status` 查表避让；AGENTS.md 增补「多会话开战役先跑 mutex status」纪律。
- **P2**：`submit_queue verify` 等「可延迟任务」加随机延迟抖动（0-90s），避免多会话整点同时起跑。

## 3. 实施顺序与验收

| 优先级 | 动作 | 验收标准 |
|---|---|---|
| P0 今天 | L1 工厂收口 + L4 孤儿清理 + WAL checkpoint | `sqlite3.connect` 仅 2 处（工厂 + MCP）；探针 1h 零 FAIL |
| P1 本周 | L2 两规则排查三节点 + L3 五写者接线 mutex | 探针记录中最长写事务 <5s；多会话并行开战役零 `database is locked` |
| P2 | 错峰日历 + verify 抖动 | 连续一周 db_lock_events 空表 |

## 4. 遗留观察（不影响方案）

- `_platform_category`（workflow/_common.py:108）为只读连接，WAL 下读写不互斥，风险可忽略但顺手收口。
- `campaign_mutex.acquire_slots` 的 SLOTS_TOTAL=7 与 `_lib/slots.py` 的 `WQB_GLOBAL_SLOTS=7` 语义重复，合流时以文件 token 版为准。
- store 层 27 处 `.commit()` 粒度已合规（写即 commit），无需改动。
