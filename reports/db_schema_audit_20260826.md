# 数据库对接体检与代码对应评估

> 审计对象：`data/wqb.db`（本地 SQLite，23.7 MB，更新于 2026-08-26 14:09）
> 活动 DB 层代码：`wqb_db_mcp.py`（MCP 服务）+ `src/wqb/store/campaign.py`（`CampaignStore`）
> 审计日期：2026-08-26

## 一、核心结论（先给结论）

**当前数据库在运行上是可用的**——20 张表全部存在且有数据、外键引用干净（无悬空引用）、`busy_timeout=5000` 已设。但存在一个**架构级治理缺陷**：

> **数据库的真实 schema 由一份「已归档、本应废弃」的包（`attic/db_layer_archive/`，原 `database/` 包）拥有，而活动代码路径（`CampaignStore.ensure_schema()`）只声明了其中 10 张表。**

直接后果：
1. 正在运行的 MCP 服务所依赖的 3 张关键表（`wave_results` / `registry_empirical` / `cross_region_lessons`）**不在活动代码的 `ensure_schema()` 里**——它们今天之所以能用，纯粹是因为库文件是从旧包迁移过来的「历史遗留」。一旦删除 `data/wqb.db` 重新 bootstrap，9+ 个 MCP 工具会直接报 `no such table`。
2. `get_region_config` 存在 **代码↔schema 漂移**（读取一个不存在的 `config` 列）。
3. 存在 5 张 **孤儿/废弃表**（0 行，无活动读写）。
4. `wave_number` 在 3 张表里 **类型不一致**（INTEGER vs TEXT）。

---

## 二、表结构总览（20 张表）

| 表 | 行数 | 活动代码声明(`ensure_schema`) | 被活动代码读写 | 备注 |
|---|---|---|---|---|
| `regions` | 7 | ✅ | ✅ | 仅 7 区域；EUR 配置列为 NULL |
| `datasets` | 291 | ✅ | ✅ | |
| `fields` | 23 570 | ✅ | ✅ | |
| `waves` | 276 | ✅ | ✅ | `wave_number` = **TEXT** |
| `expressions` | 5 477 | ✅ | ✅ | `wave` = **TEXT** |
| `backtest_results` | 250 | ✅ | ✅ | |
| `diversity_potential` | 3 | ✅ | ✅ | |
| `ledger_kv` | 1 280 | ✅ | ✅ | |
| `gate_results` | 151 | ✅ | ✅ | `created_at`/`updated_at` = TEXT 无默认 |
| `alphas` | 295 | ✅ | ✅ | |
| **`wave_results`** | 278 | ❌ **仅归档 schema** | ✅ (`wqb_db_mcp.py`) | **MCP 关键表**；`wave_number`=**INTEGER** |
| **`registry_empirical`** | 240 | ❌ **仅归档 schema** | ✅ (`wqb_db_mcp.py`) | **MCP 关键表** |
| **`cross_region_lessons`** | 10 | ❌ **仅归档 schema** | ✅ (`wqb_db_mcp.py`) | **MCP 关键表** |
| `campaign_state` | 4 | ❌ 仅归档 schema | ✅ (`tools/`) | 活表，被 `build_progress_ledger.py` 等使用 |
| `campaign_states` | 0 | ❌ 仅归档 schema | ❌ | **孤儿表** |
| `diversity_evaluations` | 0 | ❌ 仅归档 schema | ❌ | **孤儿表** |
| `expression_operators` | 0 | ❌ 仅归档 schema | ❌ | **孤儿表** |
| `operators` | 0 | ❌ 仅归档 schema | ❌（疑似） | **孤儿表** |
| `submissions` | 0 | ❌ 仅归档 schema | ⚠️ `tools_spc.py` 引用但 0 行 | 接线但从未写入 |
| `sqlite_sequence` | 14 | 系统表 | — | AUTOINCREMENT 序列 |

> 真实 schema 定义位置：`attic/db_layer_archive/schema.sql` + `schema_phase2.sql`（原 `database/` 包）。该包在 2026-08-23 已被判定「无活动代码引用」并归档——但**它仍是 `data/wqb.db` 物理 schema 的唯一权威来源**，这一矛盾未在归档时消除。

---

## 三、问题逐项评估

### P0 — Schema 所有权分裂 / bootstrap 脆弱性（潜伏，未爆发）

- **现象**：`CampaignStore.ensure_schema()` 只 `CREATE TABLE IF NOT EXISTS` 了 10 张表；`wave_results` / `registry_empirical` / `cross_region_lessons` / `campaign_state` 这 4 张**仅**由归档 schema.sql 创建。
- **触发条件**：删除 `data/wqb.db` 后重新启动 MCP（或全新 clone 未带库文件）→ `ensure_schema()` 重建的库**缺这 4 张表** → 以下工具运行时崩溃：
  - `get_wave_result` / `list_wave_results` / `get_latest_wave` / `upsert_wave_result`
  - `get_dead_ends` / `get_campaigns` / `upsert_registry_empirical`
  - `get_cross_region_lessons`
  - `get_campaign_summary` / `get_region_overview`（内部查 `wave_results`）
  - `tools/wave_results_writer.py` / `tools/split_registry.py` / `tools/migrate_phase2.py` 等 6 个脚本
- **严重度**：★ 今天不发作（库文件在），但是一颗**随时会爆的雷**——任何清理/迁移/CI 重新初始化都会触发。

### P1 — `get_region_config` 代码↔schema 漂移（已发作，静默）

- **代码**（`wqb_db_mcp.py:185-186`）：
  ```python
  result = dict(row)
  return _parse_json_fields(result, ["config"])
  ```
- **事实**：`regions` 表**没有 `config` 列**（已实测 `no such column: config`）。真实配置列是 `universe_legal` / `delay_legal` / `neutralization_default`。
- **后果**：`_parse_json_fields` 对不存在的 `config` 是 no-op；工具返回的 region dict 里 `universe_legal` 等是**未解析的原始字符串**（且 EUR 这 3 列本身为 NULL，见下）。即该工具「声明返回区域配置，实际不解析真实配置列，还去找一个不存在的列」。
- **数据佐证**：`regions` 仅 7 行，且 EUR 的 `universe_legal`/`delay_legal`/`neutralization_default` 全为 NULL，ASI/IND/EUR 的 `neutralization_default` 为 NULL → 区域配置种子数据严重缺失。

### P2 — 孤儿/废弃表（5 张，0 行）

`campaign_states`、`diversity_evaluations`、`expression_operators`、`operators`、`submissions` —— 在活动代码中无确认读写（`submissions` 仅被 `world-quant-brain-mcp/tools_spc.py` 提及但库内 0 行，属「接线未用」）。它们占用 schema 但无数据、无价值，且同样只由归档 schema 创建。属**技术债/废弃特性残留**。

### P2 — `wave_number` 类型不一致

| 表 | 列 | 实测类型 |
|---|---|---|
| `wave_results` | `wave_number` | **integer** |
| `waves` | `wave_number` | **text** |
| `expressions` | `wave` | **text** |

同一语义字段在 3 张表里用两种类型。当前因 wave 编号为纯整数、Python 比较宽松未暴露问题，但 `ORDER BY wave_number` 在 TEXT 列上对非定宽编号会错误排序，且跨表 JOIN 存在隐式类型转换隐患。

### P3 — 并发与完整性配置

- `journal_mode = delete`（SQLite 默认，**非 WAL**）：MCP 每个工具调用都 `sqlite3.connect()` 新建连接，写并发时仅靠 `busy_timeout=5000` 兜底，高并发写易触发间歇性 `database is locked`。**建议改为 WAL**。
- `foreign_keys = 0`：外键约束不生效。实测外键引用**当前干净**（orphan backtest=0，orphan alphas=0），但库不阻止未来写入悬空引用。
- `synchronous = 2` (FULL)：安全性高、写入略慢，可接受。

---

## 四、风险评级汇总

| 级别 | 问题 | 现状 |
|---|---|---|
| **P0** | Schema 所有权分裂 → bootstrap 后 9+ 工具崩 | 潜伏未爆 |
| **P1** | `get_region_config` 读不存在的 `config` 列，区域配置未解析/缺失 | 已静默发作 |
| **P2** | 5 张孤儿/废弃表（0 行） | 现存技术债 |
| **P2** | `wave_number` INTEGER/TEXT 混用 | 现存隐患 |
| **P3** | `journal_mode=delete`（非 WAL）、`foreign_keys=0` | 优化项 |

---

## 五、修复建议（仅建议，未执行——本次为评估）

1. **统一 schema 单一事实源（解 P0）**：把 `wave_results` / `registry_empirical` / `cross_region_lessons` / `campaign_state` 的 DDL **并入活动代码**（`src/wqb/store/campaign.py` 的 `ensure_schema()`，或新建 `src/wqb/store/schema.py` 作为 20 表完整 DDL），并正式移除归档 `database/` 包对物理库的所有权。这样重新 bootstrap 也能得到完整 schema。
2. **修复 `get_region_config`（解 P1）**：改为解析真实列 `universe_legal`/`delay_legal`/`neutralization_default`，并补一份 regions 种子迁移（填充全部 10 区域、EUR 缺失配置）。
3. **清理孤儿表（解 P2）**：删除 `campaign_states`/`diversity_evaluations`/`expression_operators`/`operators`/`submissions`，或在代码里正式接线——否则从归档 schema 中移除其 DDL。
4. **统一 `wave_number` 类型（解 P2）**：全库统一为 `TEXT`（或全 `INTEGER`），并迁移既有数据。
5. **启用 WAL（解 P3）**：`PRAGMA journal_mode=WAL`（库位于本地磁盘，满足 WAL 前提），保留 `busy_timeout`；视情况 `PRAGMA foreign_keys=ON`（需先核验历史数据无违例）。

---

## 六、审计命令留痕（可复现）

```bash
# 表/列/行数/索引
python - <<'PY'
import sqlite3
con=sqlite3.connect("data/wqb.db"); c=con.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print([r[0] for r in c.fetchall()])
# ...PRAGMA table_info / PRAGMA journal_mode 等
PY

# 关键依赖定位
grep -rn "CREATE TABLE.*wave_results" src/ tools/ world-quant-brain-mcp/ attic/db_layer_archive/

---

## 七、修复记录（2026-08-26）

用户要求修复 P1/P2/P2/P3（即原报告条目 2/3/4/5；P0 schema 单一事实源未做）。备份：`data/wqb.db.bak.20260826_234131`。

| 条目 | 修复内容 | 状态 |
|---|---|---|
| **2 (P1)** 代码 | `wqb_db_mcp.py:get_region_config` 的 `_parse_json_fields(result, ["config"])` → `["universe_legal", "delay_legal"]`，解析真实 JSON 列 | ✅ |
| **2 (P1)** 种子 | 填充 EUR（universe/delay/neut 全 NULL）→ config.py 值；填充 ASI（空数组+NULL neut）→ config.py 值；新增 GLB/HKG/DEU 三地区（docstring 列明的 10 区域补齐）。保留 USA/KOR/MEA/IND/GBR 原值不改动 | ✅ |
| **3 (P2)** 孤儿表 | DROP `campaign_states`/`diversity_evaluations`/`expression_operators`/`operators`/`submissions`（均 0 行、活动代码无引用，且非 `campaign_state` 活表） | ✅ |
| **4 (P2)** 类型统一 | `wave_results.wave_number` INTEGER → TEXT（282 行保留，CAST 转文本）。理由：`waves.wave_number` 含非数值子波标签（如 `11b`），只能 TEXT；故统一为 TEXT 消除 INTEGER/TEXT 跨表类型错配 | ✅ |
| **5 (P3)** WAL | `PRAGMA journal_mode=WAL`（持久化，已验证重开仍为 wal）；活动连接并发锁风险降低 | ✅ |
| **5 (P3)** 外键 | 在 `wqb_db_mcp.py:_conn()` 与 `src/wqb/store/campaign.py:CampaignStore.__init__` 的连接建立处加 `PRAGMA foreign_keys=ON`（每连接生效，非持久 pragma）。迁移后 `PRAGMA foreign_key_check` 无违例 | ✅ |

**未做**：P0（schema 单一事实源）——`wave_results`/`registry_empirical`/`cross_region_lessons`/`campaign_state` 仍仅由归档 `attic/db_layer_archive/schema.sql` 创建；bootstrap 脆弱性依旧，建议后续并入活动代码。
```
