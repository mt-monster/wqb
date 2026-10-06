# 待提交候选队列设计（回测过闸 → 持久化 → 按日配额取用）

> 目标：解决「每轮回测完找到可提交的 alpha，但不一定当天提交，之后就遗忘」。
> 状态：**核心已实现** —— `tools/submit_queue.py`（已在 `tools/README.md` 登记）。

---

## 一、问题定义

回测（S3）产出候选 → 提交决策（S5）之间存在**时间断层**：

- 每日 REGULAR 配额只有 **4 颗**、SUPER 只有 **1 颗**；
- 一回测往往产出十几到上百条达标候选，**当天吃不下**；
- 剩下的候选若只留在对话/日志里 → 次日必忘。

本质：缺一个**持久化、可排序、可复检的待提交队列**。

---

## 二、现状审计（为什么不能直接沿用旧队列）

库里已有 `ledger_kv` 的 `submit_ready` 键（11 条，按区域），但**完全不可用**：

| 区域 | 实际内容 | 问题 |
|---|---|---|
| ASI / CHN / GBR / HKG / JPN / USA | `[]` | 空 |
| DEU / MEA | `{updated, candidates:[...]}` | dict，字段名 `alpha` |
| EUR | `[{id, note, status}]` | 6 条**全是作废态**（PROD_SATURATED 等）却从不清理 |
| KOR | `[{alpha_id, date, expr, ...}]` | 已标记 SUBMITTED 的**仍留在队列** |
| IND | `{basket_mutual_corr, blocked:[...]}` | **根本没有 `candidates` 键** |

**四类硬伤**：
1. **schema 各区不一致**（list / dict / 无候选键），无法机读；
2. **字段名混乱**（`alpha` / `alpha_id` / `id`）；
3. **无清理机制**：提交/作废的条目永久滞留；
4. **无时效**：相关性测过一次就当永久有效 —— 这是最危险的一条（见 §五）。

→ 结论：弃用旧 `ledger_kv('submit_ready')`，改用规范化的独立表。

---

## 三、设计原则

1. **单一事实源**：过闸候选只存 `submit_ready` 表，`alphas` 表保持全量存量（含未过闸者）。
2. **未过闸者不进队列**：硬闸（sharpe / fitness / 2Y / turnover / PROD / SELF）任一不过 → 标 `DEAD`，默认视图不可见，仅留审计。
3. **相关性必须带时效**：每条记录记 `verified_at`，超期强制复检。
4. **机读优先**：字段统一、带索引、可按 SQL 排序/筛选。
5. **写操作可 dry-run**：`add-many` / `verify` / `retire` 均支持 `--dry-run`。

---

## 四、数据模型

独立表 `submit_ready`（`CREATE TABLE IF NOT EXISTS`，加索引）：

```sql
CREATE TABLE submit_ready (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    alpha_id       TEXT NOT NULL,
    region         TEXT NOT NULL,
    universe, delay, decay, neutralization,   -- 设置快照
    expr           TEXT,                      -- 表达式（提交/复核用）
    sharpe, fitness, turnover, two_year,
    sub_universe, cluster_test,               -- IS 派生指标
    prod, self,                               -- 相关性
    gate           TEXT,                      -- 见下
    verified_at    TEXT, verified_by TEXT,    -- 时效与来源
    towers         TEXT,                      -- pyramids JSON（塔归属/乘数）
    family         TEXT,
    status         TEXT DEFAULT 'READY',      -- READY/DEAD/EXPIRED/SUBMITTED
    added_at TEXT, note TEXT,
    UNIQUE(alpha_id, region)
);
CREATE INDEX ix_sr_region_status ON submit_ready(region, status);
```

### `gate` 取值

| gate | 含义 | 可否提交 |
|---|---|---|
| `SUBMIT_LAYER_VERIFIED` | IS 达标 且 PROD/SELF 均已测且 <0.7 | ✅ 可直接提 |
| `IS_ONLY` | IS 达标，但 PROD/SELF 未测 | ⚠️ 提交前**必须**先 `verify` |
| `FAIL:<原因>` | 硬闸未过（LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE / HIGH_TURNOVER / PROD / SELF） | ❌ 状态自动置 `DEAD` |

### 提交层硬门槛（与平台一致，写在 `LIM` 常量）

```
sharpe >= 1.58    fitness >= 1.0     two_year >= 1.58
turnover <= 0.4   prod < 0.7        self < 0.7
```

> 注：这些都是**提交层**阈值，**严于 IS 层**。IS 视图里 `LOW_SHARPE` 显示 WARNING 的 alpha，在提交层可能直接 FAIL —— 判定必须用提交层口径（本工具已按提交层判定）。

---

## 五、关键设计决策

### 决策 1：用独立表，而非 `ledger_kv`

| | `ledger_kv` JSON blob | 独立表 |
|---|---|---|
| 查询 | 只能整取后手解析 | SQL 索引查询、排序、聚合 |
| schema 一致性 | 靠自觉（已失控） | DDL 强制 |
| 并发/幂等 | 无 | `UNIQUE` + `ON CONFLICT` 幂等 upsert |

### 决策 2：相关性必须带时效（最重要）

**原因**：一旦你提交了任何别的 alpha，生产池就变了 → 之前测到的 PROD 会失效。
实测教训（本仓库）：EUR 的 `le8Y68K2` 曾测 prod 0.6929（过关），9-14 刷新后变 **0.9932** → 直接作废。

因此：
- 每条记 `verified_at`；
- `verify --max-age-days N`（默认 7）自动筛出过期项复检；
- 复检后变坏 → `DEAD`（PROD/SELF 不过）或 `EXPIRED`（其它闸退化）。

### 决策 3：优先级公式

```
priority = fitness × tower_multiplier + (相关性余量) × 0.5
相关性余量 = (0.7 − prod) + (0.7 − self)
```

- **fitness 为主**（平台最看重的质量指标）；
- **乘塔倍率**（DEU 1.4–2.0 最高，ASI/GLB/IND 最低档）；
- **相关性余量加成**：越接近 0.7 越危险，余量大者优先；
- 符合既有定规：**已点亮塔优先级最低**（乘数低 + 无新增量）。

---

## 六、工具 CLI（`tools/submit_queue.py`）

| 子命令 | 作用 | 备注 |
|---|---|---|
| `init` | 建表（幂等） | — |
| `add --alpha-id X [Y...]` | 从**平台**拉指标 + PROD/SELF 入队 | 走 MCP venv；自动判 gate |
| `add-many --region R --min-sharpe --min-fitness --max-prod` | 从**本地 `alphas` 表**离线批量导入 | **零配额**；`--dry-run` |
| `verify [--region R] [--max-age-days 7] [--no-sync]` | 复检过期项的相关性 + **RA 硬闸 + add 混腿**，变坏则标记；开跑前**先自动退役已 ACTIVE**（离线 alphas 表 + 平台 OS 列表） | `--dry-run`；逐条落盘（网络中途挂掉不丢已验行）；相关性接口失败的行**保留旧值跳过**，不会拿 None 覆盖 |
| `sync [--region R] [--offline]` | 把平台已 ACTIVE / DECOMMISSIONED / 已提交的 READY 行退役为 `SUBMITTED` | `--offline` 只查本地 `alphas` 表（零配额） |
| `regrade [--region R]` | **离线复判**现有 READY 行（RA 硬闸 / add 混腿 / prod 兄弟），闸门规则升级后清洗历史队列 | 零配额；`--dry-run` |
| `list [--region R] [--top N] [--all-status]` | 列出候选（默认仅 READY，按优先级） | 带塔归属显示 |
| `pick [--region R]` | 输出最优先 1 条完整记录（供提交） | — |
| `retire --alpha-id X --status SUBMITTED\|DEAD\|EXPIRED` | 退役 | `--dry-run` |

---

## 七、钩子挂载点：为什么是 S3 收批，而不是 S5

**结论：入队（捕获）挂在 S3 收批；判定升级挂在 S4→S5 的 `submit_verdict`；退役挂在 S5 提交成功。三者职责分离。**

### 为什么不能挂在 S5

| 理由 | 说明 |
|---|---|
| **语义矛盾** | S5 **就是**提交动作本身。等提交完再入队 = "提交后才记录"，而要解决的恰恰是"**没提交的**别忘" |
| **丢失时间窗** | S4 之前那段时间（可能跨天、可能 S4 根本没跑）正是遗忘发生的地方 |
| **无批量语义** | S5 是逐条提交；S3 收批是一次几十上百条的**批量**入口，批量入队成本最低（离线、零配额） |

### 为什么 S3 是正确的最早时点

1. **相关性可测的最早点**：`PROD_CORRELATION` 需要 alpha 已完成模拟（S3 产出），S3 之后才能测；
2. **唯一的批量入口**：`harvest_multisim.py` 是 S3 收批的规范工具；
3. **S4 不产生新对象**：实测 `S4 = review_wave.py`，纯诊断（从 `backtest_results` 读本波 alpha），**不重新模拟**。

### 三段式职责表

| 阶段 | 入口 | 队列动作 | 状态变化 |
|---|---|---|---|
| **S3 收批** | `tools/harvest_multisim.py` | **批量入队**（捕获，防遗忘） | 新增 → `IS_ONLY` / `SUBMIT_LAYER_VERIFIED`；硬闸不过 → `DEAD` |
| **S4→S5 判定** | `tools/submit_verdict.py`（单条，出 `SUBMITTABLE`/`BLOCKED`） | **状态升级** + 刷新 `verified_at`（✅ 已接线） | `IS_ONLY` → `SUBMIT_LAYER_VERIFIED`；`BLOCKED` → 不改（保持） |
| **S5 提交成功** | `nodes/submit_alpha.py` | **退役** | → `SUBMITTED` |

**核心原则：捕获（capture）与判定（verdict）分离** —— 捕获要最早最全，判定要最严最终，各自挂在语义正确的位置。

### ✅ Mode A/B 变体已被覆盖（2026-09-20 核实，非盲区）

先前担心 S4 的 Mode A/B 变体走独立管线会漏掉。**实测核实：不会漏。**

`tools/modeb_improvement_pipeline.py` 的职责是**只生成表达式并写入 `expressions` 表**
（`insert_wave()` → `status='selected'`），**它本身不回测**。这些表达式随后走**标准 S3 批量回测路径**
（`mcp_7slot_batch` / `batch_track` → 收批 `harvest_multisim.py`）——**收批钩子自动生效**。

→ 结论：**S3 收批一处钩子即覆盖全部回测来源**（wave 表达式、Mode A/B 变体、探针批）。

## 七之二、推荐日常流程

### ① 每轮回测后（S3 收批时）—— 已自动化，一般无需手动
```bash
# 收批即自动入队（无需手动跑）：
#   python tools/harvest_multisim.py --multisim-id XXX --auto-upsert --wave N --region IND
#   → 内部自动调 enqueue_from_alphas(...)，打印 [queue] N 条过闸候选

# 仅在需要补录/重扫时手动跑（离线、零配额）：
python tools/submit_queue.py add-many --region IND --min-sharpe 1.58 --min-fitness 1.0 --dry-run
# 对未测相关性的（IS_ONLY）补测
python tools/submit_queue.py verify --region IND --max-age-days 7
```

### ② 每个 ET 日开始（配额重置后）
```bash
python tools/submit_queue.py list --region IND --top 5      # 看今天该提谁
python tools/submit_queue.py pick --region IND               # 取最优先 1 条
```

### ③ 提交成功后（必做，否则队列会永远留着已提交的）
```bash
python tools/submit_queue.py retire --alpha-id <ID> --status SUBMITTED
```

### ④ 每周/每月维护
```bash
python tools/submit_queue.py verify --max-age-days 7        # 全区域复检
python tools/submit_queue.py list --all-status              # 审计作废项
```

---

## 八、已实现 vs 待办

### ✅ 已实现（核心 + 两个自动钩子，2026-09-20）
- `submit_ready` 表 + 索引 + 幂等 upsert
- 七个 CLI 子命令（init / add / add-many / verify / list / pick / retire）
- 提交层硬闸判定（含 DEAD 自动剔除）
- 相关性时效 + 复检
- 优先级排序 + 塔倍率
- 已登记 `tools/README.md`

**三个自动钩子（消除人工遗漏）**
1. **收批自动入队** —— `tools/harvest_multisim.py` 在 `--auto-upsert` 完成 upsert 后，
   自动调 `enqueue_from_alphas(region, min_sharpe=1.58, min_fitness=1.0)`；
   可用 `--no-queue` 关闭。队列记账失败**不阻断收批**。
2. **提交自动退役** —— `src/wqb/workflow/nodes/submit_alpha.py` 的 `_finalize()` 在
   `submitted && success` 时自动 `retire(alpha_id, 'SUBMITTED')`；失败只记 warning。
3. **判定自动升级**（2026-09-20 新增）—— `tools/submit_verdict.py` 出 `SUBMITTABLE` 时，
   自动 `mark_verified(alpha_id)` 把该条升级为 `SUBMIT_LAYER_VERIFIED` 并刷新
   `verified_at`；`UNVERIFIABLE`/`BLOCKED` 时**不动队列**（已实测验证守卫生效）。

**并发注意**：`connect()` 已设 `busy_timeout=30s` —— 本表会被 MCP 服务 / CLI / 多个钩子
同时写，无超时会直接 `database is locked`（实测踩到过）。

**架构**：核心逻辑收在 `src/wqb/store/submit_queue.py`（single source of truth），
CLI / harvest / 提交节点三方共用，判定口径不会漂移。

### 📋 待办（可选增强）
1. **次日提醒**：`brain-next-move-analysis` 日报中嵌入 `list` 输出；
2. **配额感知**：`list` 时按当日剩余配额（4/1）截断显示条数。

### ✅ 已完成（2026-09-20 追加）
- **骨架去重**（防止队列堆同族）：新增 `skeleton` 列 + `dedup_siblings()` + CLI `dedup` 子命令。
  - 复用权威实现 `wqb.expression.skeleton::structural_signature`（字段→F、数字→N、算子按"后紧跟 ("识别），
    与 `tools/pool_diversity.py` / `tools/backfill_skeletons.py` 同一口径。
  - 规则：**同区域内同骨架只留优先级最高的 N 条**（默认 N=1），其余标 `SUPERSEDED`
    （与硬闸失败的 `DEAD` 区分，便于审计）。
  - `enqueue_from_alphas` **默认开启去重**；`--no-dedup` 可关、`--max-per-skeleton N` 可调。
  - 实测：全区域一次去重标 **72 条 SUPERSEDED**（IND 最大一族 9 条 → 只留 1）。
- **旧 `ledger_kv('submit_ready')` 已作废**：12 个键先**全量归档**到
  `logs/archive_ledger_submit_ready_<ts>.json`（48.9KB，含 MEA 18 / EUR 6 / KOR 2 / DEU 4 条零散候选），
  再从库中删除。随后**以 `alphas` 为权威源全区域重建**队列（106 条 READY）。

### ✅ 三个坑已补（2026-09-20 下午，`tests/unit/01_store_db/test_submit_queue_gates.py` 27 例回归）

首版上线当天用 IND 实战暴露三个坑，全部收口在 `src/wqb/store/submit_queue.py`（三方共用，口径不漂移）：

| 坑 | 现象 | 修法 |
|---|---|---|
| **1. 没过滤 RA FAIL** | 36 条 `LOW_ROBUST_UNIVERSE_SHARPE` 的 IND 候选进了 READY——队列只看 S/F/2Y/turnover，平台 RA 硬闸（robust / sub-universe / CW / IS ladder / investability…）一概不看 | `RA_HARD_FAILS` + `ra_fail_of()`：`gate_of(..., ra_failed_checks, expr)` 任一硬闸 FAIL → `FAIL:RA:<name>` / DEAD。`enqueue_from_alphas` 子查询带 `backtest_results` 最新一条 `ra_failed_checks`；CLI `_fetch` 从平台 `is.checks` 取 `result==FAIL` 名单 |
| **2. 没过滤加权混腿 / 已判死家族** | `add(multiply(0.4,A), multiply(0.6,B))` 与"裸主腿撞 prod 墙 0.8 的同骨架兄弟（prod 未测）"都能以 IS_ONLY 进 READY | ① `is_add_mix()` **口径 = toolkit gate.py 闸5 全口径**（结构判定 ≥2 系数腿 ∪ 三条正则 `weighted_signal_mix` / `weighted_leg_mix_func_prefix|suffix`）；等权 `add(rank,rank)`、`subtract(rank,rank)` 按用户 2026-09-13 路线 A **不拦**；实测 107 条真实队列行与闸5 **0 条不一致**。括号不平衡（上游截断到 110 字符的 516 条 `alphas.expression`）时结构判定按已见实参判、正则兜底。② `_prod_wall_sibling()`：同区域同骨架兄弟已实测 prod≥0.7 且本条 prod 未测 → `FAIL:PROD_SIBLING(id=prod)` / DEAD；本条实测 prod<0.7 时 `mark_verified` 可复活 |
| **3. 已 ACTIVE 的还在 READY；retire 后 harvest 再 enqueue 复活** | 全区 40 条 READY 里 20 条平台已 ACTIVE；`_upsert` 的 `ON CONFLICT ... status=excluded.status` 把 SUBMITTED/DEAD 覆盖回 READY | ① `_upsert` 终态粘性：`status IN ('SUBMITTED','DEAD')` 时 status/note 保持不变（READY 行仍刷新指标）；② `enqueue_from_alphas` 排除 `platform_status IN ('ACTIVE','DECOMMISSIONED')` 与 `date_submitted IS NOT NULL`，并在同一事务里把已提交者退役；③ `retire_platform_done()`（离线）/ `retire_active(ids)`（平台 OS 列表）→ CLI `sync`，`verify` 开跑前自动调 |

| **4. 批量入队覆盖平台实测值**（补坑当天实战新暴露） | `verify` 刚写回 3qX3Mp6O prod **0.6437**（3 颗新 ACTIVE 推高了它），并行的 `add-many --region IND` 立刻用 `alphas` 表旧值 0.4853 覆盖回去，`verified_at` 也被刷新成假新鲜 | `enqueue_from_alphas` 标 `verified_by='alphas'`，并**跳过** `verified_by ∈ PLATFORM_VERIFIED_BY = (API, verify, submit_verdict)` 与终态行——批量入队只「捕获」，平台实测值只由 `add`/`verify`/`mark_verified` 改 |

清洗实录（2026-09-20）：READY 40 → **9**（sync 退役 20 已 ACTIVE；regrade 判死 加权混腿 3 + prod 兄弟 8）；IND 5 条 `SUBMIT_LAYER_VERIFIED` 原样保留。

顺手修的三个 CLI bug：`_bootstrap_venv` 在 venv 子进程里会再拉起一层（路径大小写比较失败），已加 `WQB_SQ_BOOTSTRAPPED` 环境标记 + `normcase`；`verify` 的 cutoff 用 UTC 而 `verified_at` 是本地 naive 串，字符串比较导致当天验过的行永不复检（`--max-age-days 0` → "待复检 0 条"），已改同口径；Windows 上 `os.execv` 不是进程替换（父进程立刻 rc=0 退出、子进程后台继续、`&&` 后续命令抢跑、输出丢失），已改 `subprocess.call` 同步等待透传 rc。

已知未改（记录）：`_backtest.py` 把空 `failed_checks` 存成 NULL，NULL 同时表示"0 FAIL"与"未采集"；队列按"无 FAIL"处理，与 `wqb_db_mcp` 的 `ra_clean` 口径一致，但严格说不可区分。

---

## 九、与既有设施的关系

| 设施 | 角色 |
|---|---|
| `alphas` 表 | 全量存量（含未过闸），队列的数据来源 |
| **`submit_ready` 表** | **过闸待提交队列（本设计新增）** |
| `submission_ledger` | 已提交台账（写后事实，75 条） |
| `submit_verdict.py` | 单条提交层判定 |
| `persist_prod_corr.py` | 批量回填相关性（本工具的 `verify` 直接查平台，互补） |
| `query_alpha_metrics.py` | 只读筛选（本工具的 `add-many` 是它的"落库"动作） |
| `ledger_kv('submit_ready')` | **已弃用**（schema 失控） |
