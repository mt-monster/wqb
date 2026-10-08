# mining_ledger —— 挖掘产出的「第一落点」队列

> 目标：**会话里挖出的任何一颗 alpha，都不因上下文截断 / 会话中断 / 进程崩溃而丢失**，
> 并能在之后被盘点工具可靠地"扫到"。
> 工具：`tools/ledger/mining_ledger.py` ｜ 队列：`results/mining_ledger/alpha_ledger.jsonl`

---

## 1. 为什么需要它

**事故（2026-10-06 `58gkLAkk`）**：一颗 DEU alpha 在会话里被挖出来，只存在于对话中。
上下文一截断就找不回来；本地 `alphas` / `submit_ready` / `backtest_results` 三张表**全无此行**，
于是所有只扫本地 SQLite 的工具（`submit_inventory` / `scan_backup_ra` / `enqueue_propose`）集体失明。
最后只能靠用户事后点名 ID 才被发现并手工补录。

**为什么不直接写 `submit_ready`**：

| 阻碍 | 说明 |
|---|---|
| 要平台 ID | `submit_queue.py add` 需 alpha_id 并触发 PC 相关性计算（实测 1–5 分钟），挖掘当下往往只有表达式 |
| DB 写锁 | WAL 单写者可能被长事务占据 ≥30min（`tools/db_lock_audit.py`），挖掘侧不该去抢 |
| 需人工裁决 | 入队按用户定案必须人工/策略裁决，不能由挖掘侧自动写 |

⇒ 本工具做**零依赖、零阻塞、不碰 DB、不调平台**的第一落点。

---

## 2. 数据结构定义

单文件 append-only JSONL，**每行一个完整 JSON 对象**（`sort_keys=True`，便于 diff / 人工阅读）。

```jsonc
{
  "v": 1,                    // schema 版本
  "key": "expr:196a02c255b93b5b",   // 去重键（见 §4）
  "ts": "2026-10-07T00:25:02+08:00", // 首次入队时间
  "updated_at": "...",       // 本行写入时间（last-write-wins 的比较依据）

  "kind": "expr" | "alpha_id",       // 入队时手里有什么
  "expr": "rank(ts_zscore(f,66))",   // 规范化后的表达式（无 alpha_id 时必填）
  "alpha_id": "58gkLAkk" | null,     // 平台 ID，仿真后回填

  // settings 五元组 —— 参与去重哈希，也是后续建仿真的参数
  "region": "DEU", "universe": "TOP500", "delay": 1,
  "decay": 8, "neutralization": "SUBINDUSTRY",

  "wave": "deu_w33_m106_250",        // 来源轮次 / 波号
  "src": "chat" | "harvest" | "scan",// 产出来源
  "session": null,                   // 可选会话标识

  "state": "NEW",                    // 见 §3 状态机
  "attempts": 0,                     // 失败重试计数
  "last_error": null,
  "metrics": {}                      // 可选回填：sharpe/fitness/two_year/prod/self
}
```

### 状态机

```
NEW ──► SIM_OK ──► QUEUED ──► DONE
  │        │
  │        └──► SIM_FAIL ──► (attempts < 3 可重试) ──► SIM_OK
  │                     └──► attempts ≥ 3 ──► DEAD
  └──► DEAD（人工判死）
```

| 状态 | 含义 | 是否为"待处理" |
|---|---|---|
| `NEW` | 刚挖出（可能只有表达式，还没仿真） | ✅ |
| `SIM_OK` | 已仿真、有 alpha_id，**待入队** | ✅ |
| `SIM_FAIL` | 仿真失败，可重试 | ✅（未超上限） |
| `QUEUED` | 已入 `submit_ready` | ❌ 已闭环 |
| `DONE` | 已确认被盘点覆盖 | ❌ 已闭环 |
| `DEAD` | 判死 | ❌ 已闭环 |

> `OPEN_STATES = (NEW, SIM_OK, SIM_FAIL)` —— 三者都表示"尚未进 `submit_ready`"。

---

## 3. 入队策略：逐条 vs 批量（推荐逐条）

| 维度 | 逐条即时落盘 | 积攒 N 条后批量落盘 |
|---|---|---|
| **丢失窗口** | 单条产出时间（秒级） | N 条产出时间（可能几十分钟） |
| 崩溃 / 断电损失 | 0～1 条 | 0～N 条 |
| 上下文截断损失 | 0～1 条 | **最近 N 条**——恰是最重要、最来不及补的 |
| 单次开销 | append + fsync ≈ 1–10ms | 摊薄，N 次省 N−1 次开销 |
| 实现复杂度 | 低 | 高 |
| 并发 | 锁持有时间极短 | 一次写 N 行，持锁更久 |

**决定性论据**：批量方案的**缓冲区本身也需要持久化**，否则缓冲区就是新的丢失窗口。
而一旦给缓冲区做了持久化（WAL / 预写日志），复杂度就回到了"逐条落盘"这一档——
加了复杂度，却只换来可忽略的 fsync 开销节省。

**⇒ 推荐：逐条即时落盘**（本工具默认行为）。

补充（可选优化，当前未实现）：文件过大时做一次 **compaction**——把每个 key 的多行合并成
一行最新状态重写。**写入仍逐条**，compaction 只在读取性能明显下降时手动跑一次。

---

## 4. 去重

* 有 `alpha_id` ⇒ key = `id:<alpha_id>`（平台 ID 本身唯一）。
* 只有表达式 ⇒ key = `expr:<sha1(region|universe|delay|decay|neutralization|norm_expr)[:16]>`。

两个关键点：

1. **settings 五元组必须参与哈希** —— 同一表达式换 region / universe / delay / decay /
   neutralization 是**不同**的 alpha。
2. **表达式规范化**：去掉**字符串字面量之外**的所有空白，**不改大小写**（FASTEXPR 大小写敏感）。
   - 为什么要"删"而不是"压缩"空白：换行/缩进/手打空格不同时，压缩后仍可能不等
     （`rank( ts_zscore(f, 66) )` ≠ `rank(ts_zscore(f, 66))`），会被当成两颗不同 alpha。
   - 为什么要保护引号内：`bucket(..., range="0, 1, 0.1")` 里的空格是**语义的一部分**，
     删掉会变成另一个表达式。

`add` 时若 key 已存在 ⇒ 打印 `[dedup]` 并跳过（`--force` 可强制追加一行）。

---

## 5. 扫描侧

```bash
python tools/ledger/mining_ledger.py scan            # 列出待处理（按时间序）
python tools/ledger/mining_ledger.py scan --json     # 机器可读
```

* **断点续扫**：`load()` 先把所有行按 key 归并（**后写覆盖前写**，`updated_at` 比较），
  再筛 `OPEN_STATES`。已 `QUEUED` / `DONE` / `DEAD` 的**永远不会再被扫出**——
  中断后重跑 `scan` 天然从断点继续，不重复处理。
* **已处理标记**：处理完追加一行新状态（`mark --state ...`）。append-only 不改旧行，
  因此崩溃在"处理完成"与"标记完成"之间时，最坏情况是**重跑一次**（幂等），不会丢。
* **失败重试**：`mark --state SIM_FAIL` 会 `attempts += 1`；`attempts >= 3` 自动转 `DEAD`
  （`--keep-open` 可保留）。`scan` 对超上限的 `SIM_FAIL` 不再列出。

**推进到 `submit_ready`（闭环的关键一步）**：

```bash
python tools/ledger/mining_ledger.py promote                       # dry-run（默认）
python tools/ledger/mining_ledger.py promote --apply --approved-by <你>
```

把「有 alpha_id 且待处理」的记录用 `wqb.store.submit_queue.enqueue` **本地入队**（不调平台、不占配额）。
入队成功后自动追加 `QUEUED` 行。此后 `submit_inventory` 就能扫到它。

> ⚠ `--apply` 必须带 `--approved-by`：入队按用户定案须人工/策略裁决。
> 本工具**绝不提交 alpha**，也不触碰 `ALLOW_ALPHA_SUBMIT`。

---

## 6. 兜底

| 故障 | 处理 |
|---|---|
| 主文件写入失败（OSError / 锁超时） | 自动改写 `<path>.fallback.jsonl`，stderr 告警；两者都失败返回退出码 **3** |
| 多次追加同一 key | 天然幂等：`add` 去重跳过；需改状态用 `mark` 追加一行（last-write-wins） |
| 坏行（JSON 解析失败 / 缺 key） | 跳过并计数，不整体崩；`scan` / `stats` 显示「坏行 N」 |
| 并发多写者 | `<path>.lock` + `O_EXCL` 自旋锁（指数退避 0.01→0.2s，默认等 30s）；崩溃残留的锁超 60s 自动清除 |
| 进程在 write 中途崩溃 | `O_APPEND` 单行写入 + `fsync`；最坏留一个不完整行，被判为坏行跳过，其余行完好 |
| 上下文截断 / 会话中断 | 队列在磁盘上，与会话无关 —— 这正是它的存在理由 |

---

## 7. 运行与自检

```bash
# 自检（临时目录跑完整闭环，不碰真实队列）——8 项
python tools/ledger/mining_ledger.py selftest

# 入队：只有表达式
python tools/ledger/mining_ledger.py add --expr "rank(ts_zscore(f,66))" \
    --region DEU --universe TOP500 --delay 1 --neutralization SUBINDUSTRY --decay 8 \
    --wave deu_w33 --src chat

# 入队：已有平台 ID
python tools/ledger/mining_ledger.py add --alpha-id 58gkLAkk --region DEU

# 仿真结果回填
python tools/ledger/mining_ledger.py mark --key <key> --state SIM_OK --alpha-id <id> \
    --metrics-json '{"sharpe":1.75,"fitness":1.42,"two_year":2.07}'

python tools/ledger/mining_ledger.py scan
python tools/ledger/mining_ledger.py stats
```

自检覆盖：①写入读回 ②按 key 去重 ③settings 参与哈希 ④状态推进 last-write-wins
⑤断点续扫（DONE 不再扫出）⑥失败重试上限 ⑦并发追加不丢行（8 线程×30 条）⑧坏行容错。

---

## 8. 会话纪律（最重要的一条）

**挖掘侧每产出一颗 alpha，立刻 `add`，不等批、不等仿真结果、不等"复盘时再补"。**

- 只有表达式 ⇒ `add --expr ...`（state=NEW）；拿到 ID 后 `mark --state SIM_OK --alpha-id ...`。
- 已有 ID ⇒ 直接 `add --alpha-id ...`。
- 会话结束前跑一次 `scan`，确认没有遗漏在"待处理"里的项。

理由：上下文截断是**随时发生**的，不是按 N 条发生的。落盘成本 ≈ 毫秒级，
漏一颗的代价是它永久从所有盘点里消失。
