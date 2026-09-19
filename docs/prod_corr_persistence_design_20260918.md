# 回测指标全量落库方案（prod/self 相关性等）

> 2026-09-18 诊断与设计。目标：**回测完成即落库全部平台指标**，复盘/查询直接读本地库，不再每次打平台 API。

## 1. 现状诊断

### 1.1 表结构（data/wqb.db，4211 行 alphas / 4284 行 backtest_results）

```
alphas（15+ 列，含软删除/判死扩展）
  alpha_id UNIQUE | expression | region_id FK | dataset_id FK
  universe | delay | neutralization
  sharpe | fitness | margin | turnover | two_year_sharpe
  is_ladder_sharpe          ← 2026-08-29 新增
  prod_correlation | self_correlation
  status（本地语义）| platform_status（平台语义）| stage | alpha_type | date_submitted
  soft_deleted / disposition / dead_reason / dead_at

backtest_results
  alpha_id | expression_id FK | region | wave | dataset | code
  sharpe | fitness | turnover | margin | returns | drawdown
  two_year_sharpe | sub_universe_sharpe | risk_neutralized_sharpe
  long_count | short_count | pnl | book_size
  ra_failed_checks JSON | payload_json | status | created_at
```

### 1.2 实测填充率（问题量化）

| 指标 | alphas 填充 | 判定 |
|---|---|---|
| sharpe / fitness | 97.0% / 96.8% | ✅ 正常 |
| turnover / two_year_sharpe | 94.9% / 86.0% | ✅ 正常 |
| margin | 74.2% | ⚠️ 偏低 |
| **prod_correlation** | **270 / 4211 = 6.4%** | ❌ **核心缺口** |
| **self_correlation** | **103 / 4211 = 2.4%** | ❌ **核心缺口** |
| is_ladder_sharpe | 52 / 4211 = 1.2% | ❌ 缺口 |
| sub_universe_sharpe | **alphas 表无此列** | ❌ 缺列 |
| risk_neutralized_sharpe | 66 / 4284 = 1.5% | ❌ 缺口 |
| long_count / returns / drawdown | 2.9% / 2.0% / 2.0% | ❌ 缺口 |

### 1.3 根因（三处断链，全部经代码确认）

**断链 A — `tools/mcp_batch_writer.py::DirectDBWriter._call_mcp`（第 263-285 行）**
`upsert_backtest_rows` 分支只写 9 列，且**根本不写 alphas 表**：
```python
"INSERT OR REPLACE INTO backtest_results "
"(alpha_id, region, wave, dataset, code, status, sharpe, fitness, turnover, created_at)"
```
→ margin / 2Y / sub_universe / prod / self 全部丢失。

**断链 B — `wqb_db_mcp.py::harvest_multisim_results`（第 1140-1155 行）**
row 构造只含 sharpe/fitness/turnover/margin/2Y/sub_universe/failed_checks，
**无 prod_correlation / self_correlation / is_ladder_sharpe / risk_neutralized_sharpe**。
（`tools/harvest_multisim.py::_to_backtest_rows` 已在 09-02 补齐相关字段，
但 MCP 侧这条并行路径未同步 → 走 MCP 收批时相关性仍丢。）

**断链 C — 相关性检查结果无处可落**
`check_correlation(alpha_id, 'production'/'self')` 返回的 `max_correlation`
只进内存/`logs/_triage_prodcorr.json`，需人工跑 `persist_prod_corr.py` 才回填。
→ 没有「检查即落库」的自动路径。

### 1.4 已有的正确实现（可复用）

- `src/wqb/store/_backtest.py::upsert_backtest_rows`（第 13-147 行）：**已完整**
  ——写 backtest_results 全列 + 同步 upsert alphas 全指标（含 prod/self correlation）。
- `src/wqb/store/_backtest.py::upsert_alpha_from_platform`：提交后回写平台详情。
- `tools/harvest_multisim.py::fetch_alpha_details`：**已能提取**
  prod/self correlation、is_ladder、sub_universe、concentrated_weight、cluster_test
  （`is.prodCorrelation` → 回退 `checks[PROD_CORRELATION]`）。
- `tools/sync_platform_alphas.py`：平台→本地批量对齐（含 prod/self）。
- `tools/persist_prod_corr.py`：checkpoint → alphas.prod_correlation 回填。

**结论：缺口不在 schema 也不在 CampaignStore，而在三条平行写入路径没接上。**

## 2. 实现方案

### 2.1 设计原则

1. **单一写入口**：所有回测行写入统一走 `CampaignStore.upsert_backtest_rows`，
   禁止平行实现（`DirectDBWriter` 改为薄委托）。
2. **列扩展过 `_add_column`**：幂等迁移，禁止裸 `ALTER TABLE`。
3. **检查即落库**：相关性检查函数返回前直接写库，不依赖人工回填。
4. **NULL-only 回填**：回填工具不覆盖已有值（保留平台权威值）。
5. **dry-run 默认**：所有写库动作默认预览，`--apply` 才落盘。

### 2.2 改动清单

| # | 文件 | 改动 | 目的 |
|---|---|---|---|
| 1 | `src/wqb/store/_schema.py` | `alphas` 补列：`sub_universe_sharpe`、`returns`、`drawdown`、`long_count`、`short_count`、`concentrated_weight`、`cluster_test`、`prod_corr_source`、`corr_checked_at` | 补齐查询所需维度 |
| 2 | `src/wqb/store/_backtest.py` | `upsert_backtest_rows` 的 alphas upsert 段补写新列；新增 `persist_correlation(alpha_id, prod, self, source)` 方法 | 回测即落全指标 |
| 3 | `wqb_db_mcp.py` | `harvest_multisim_results` row 构造补 corr/ladder/risk_neut；新增 `persist_correlation` 工具 | MCP 路径不再丢指标 |
| 4 | `tools/mcp_batch_writer.py` | `DirectDBWriter.upsert_backtest_rows` 改为 `DELETE`+委托（或直写全列） | 消除平行实现 |
| 5 | `tools/harvest_multisim.py` | 收批后调用 `persist_correlation` 落库相关性 | 收割即带相关性 |
| 6 | `tools/persist_prod_corr.py` | 支持 self_correlation + source 标记，扩展 checkpoint 格式 | 存量回填 |
| 7 | `tools/query_alpha_metrics.py`（新） | 本地统一查询：按 region/阈值/相关性筛候选 | 免打平台 |

### 2.3 新增列 DDL

```sql
-- alphas 补列（可空，不破坏既有数据）
ALTER TABLE alphas ADD COLUMN sub_universe_sharpe DECIMAL(8,4);
ALTER TABLE alphas ADD COLUMN returns DECIMAL(8,4);
ALTER TABLE alphas ADD COLUMN drawdown DECIMAL(8,4);
ALTER TABLE alphas ADD COLUMN long_count INTEGER;
ALTER TABLE alphas ADD COLUMN short_count INTEGER;
ALTER TABLE alphas ADD COLUMN concentrated_weight DECIMAL(6,4);
ALTER TABLE alphas ADD COLUMN cluster_test DECIMAL(6,4);
-- 相关性溯源：区分"平台同步"与"本地抽测"，避免两个来源混判
ALTER TABLE alphas ADD COLUMN prod_corr_source TEXT;   -- platform_sync | triage_local | manual
ALTER TABLE alphas ADD COLUMN corr_checked_at TIMESTAMP;
```

### 2.4 关键契约

**`persist_correlation(alpha_id, prod=None, self_=None, source=..., overwrite=False)`**

```
行为：
  - alpha 不存在 → 返回 {"skipped": "not_found"}
  - overwrite=False（默认）→ 只填 NULL 列，已有值不动
  - overwrite=True → 平台权威值覆盖本地估算值
  - 同时写 corr_checked_at = now
  - 任一值非 [0,1] 区间 → 拒绝写入（防空值/None 污染）
幂等：重复调用零变化。
```

**来源优先级**（查询时应据此判读）：
1. `platform_sync`（`sync_platform_alphas`）—— 平台权威，最高
2. `manual` —— 人工确认
3. `triage_local`（本地 OS PnL 池抽测）—— **已知结构性盲区**：
   对近期提交的孪生体失明会低估（实证 vRkAO9Xd 本地 0.229 vs 平台 0.8392）。
   故本地值**高可信、低不可信**。

## 3. 验证方案

1. 单元测试：`tests/unit/test_store.py` 增补 `persist_correlation` 用例
   （NULL-only / overwrite / 边界值拒绝 / 幂等）。
2. 回归：`pytest tests/ -q`（根 313 用例须全绿）。
3. 一致性核对：随机抽 20 条 alphas，比对 `backtest_results` 与 `alphas` 同名字段。
4. 填充率复测：改动后重跑 §1.2 统计，prod_correlation 应从 6.4% 显著上升。

## 4. 收益

- 复盘/查询走本地库 → **零平台配额消耗**，避免相关性检查占单并发队列。
- 候选筛选（prod≤0.7 / self≤0.7 / PPAC≤0.5）可直接 SQL，无需逐条打 API。
- 消除"本地有指标但查询时缺失"的口径漂移（同一 alpha 两个数据源不一致）。

## 5. 实施状态（2026-09-18 当日落地）

| # | 文件 | 状态 | 说明 |
|---|---|---|---|
| 1 | `src/wqb/store/_schema.py` | ✅ 已上线 | alphas +9 列 +2 索引，已对 `data/wqb.db` 实际迁移（实测列/索引齐备） |
| 2 | `src/wqb/store/_backtest.py` | ✅ 已上线 | `upsert_backtest_rows` 补写新列（INSERT 29 列）；新增 `persist_correlation` |
| 3 | `wqb_db_mcp.py` | ✅ 已上线 | `harvest_multisim_results` 补 corr/ladder/risk_neut/收益/持仓透传 + checks 回退取值；新增 MCP 工具 `persist_correlation`、`get_alpha_corr_metrics` |
| 4 | `tools/mcp_batch_writer.py` | ✅ 已上线 | `DirectDBWriter` 简化为 `_get_store()` 薄委托；新增 `persist_correlation` 分支；CampaignStore 不可达时**显式抛错**（禁止静默降级） |
| 5 | `tools/harvest_multisim.py` | ✅ 已上线 | `_to_backtest_rows` 补 risk_neut/returns/drawdown/long/short；收批后调 `persist_correlation(source='platform_sync')` |
| 6 | `tools/persist_prod_corr.py` | ✅ 已上线 | 支持 self + `--source`/`--overwrite`；[0,1] 校验；兼容多种 checkpoint 键名 |
| 7 | `tools/query_alpha_metrics.py` | ✅ 新建 | `--coverage` 填充率 / 多维筛选 / CSV 导出 |

**验证结果**：
- 单测：`tests/unit/test_store.py` 18 passed（新增 4 个用例：全指标落库 / NULL-only / overwrite+校验 / 幂等）。
- 全量回归：`pytest tests/ -q` → **1183 passed, 7 failed**；7 个失败经 stash 对照确认为**改动前既存失败**（test_workflow registry / skills 漂移 / docs 计数 / toolkit 同步），与本次改动无关。
- 端到端：临时库实测 upsert 全指标 → alphas 九列齐落；persist_correlation 五态（首次/NULL-only/overwrite/越界拒/不存在）全部符合契约；`DirectDBWriter` 委托链路正常写入 alphas（原实现只写 backtest_results 9 列）。

**遗留**：
- 「检查即落库」目前覆盖 harvest 两条路径（MCP + CLI）。**triage 抽测路径仍写 checkpoint**，
  需跑 `persist_prod_corr.py --apply` 落库（未改 triage 脚本本身，避免影响其续跑状态机）；
  后续可在 triage 写完 checkpoint 处直接调用 `persist_correlation`。
- 存量 270 条有 prod 值的记录 `prod_corr_source` 为 NULL（历史数据无溯源信息），
  不做回填猜测；新写入一律带 source。

**生效前提**：`wqb-db` MCP 服务须重启，新工具（`persist_correlation` / `get_alpha_corr_metrics`）
才会在会话工具表里出现（工具表在会话启动时构建，共 43 → 45）。

**存量填充率说明**：改动只作用于**今后**的写入路径；4211 行历史数据的口径不会自动变化
（仍为 prod 6.4% / self 2.4%）。需要历史回填须跑
`persist_prod_corr.py --apply`（依赖 triage checkpoint）或 `sync_platform_alphas.py --apply`（平台对齐）。
