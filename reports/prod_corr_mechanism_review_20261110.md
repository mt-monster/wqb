# 查 prod 机制与相关代码审查（2026-11-10）

> 范围：production correlation 的取数、缓存、锁、判闸、提交链与工具层消费点。
> 方法：三路代码探索 + 关键路径逐行核验（本报告 §0 标注「已核验」的条目为亲自读码确认，其余来自静态探索，落地前需复核）。
> 触发背景：2026-11-09 夜 `9qxnYPjd` 优化轮，prod 终验连续 3 次 240s `pending`、holder 轮替、peek 8 轮空体 —— 暴露的不是候选问题，是取数机制本身的可优化点。

---

## 0 机制全貌

### 0.1 三段式（设计意图）

| 段 | 入口 | 作用 |
|---|---|---|
| ① 缓存 | `check_correlation(refresh=False)` → `_prod_corr_cached` | 48h 内权威缓存命中即返回，不占平台单并发槽 |
| ② peek | `tools/prod_wait.py --peek` | 无锁只读探测，空体 = 平台仍在算（非失败） |
| ③ 终验 | 提交那颗 `refresh=True` | 跳过缓存 + 跳过预读，强制平台重测 |

### 0.2 调用链（已核验）

```
tools_corr.py:7-12          MCP 注册 check_correlation
brain_mixin_correlation.py:882  check_correlation 编排
  :937                        _prod_corr_cached → alpha_corr_cache（48h）
  :959                        get_production_correlation(use_pre_read=not refresh)
brain_mixin_spcread.py:1101    两级锁 + inflight + join
  :1277                       _poll_production_correlation（240s 窗口 / 10-30-10s 阶梯）
  :1343                       超时 → status=pending, max=None
brain_mixin_correlation.py:1041 max 非空 → _prod_corr_store → set_corr_cache
src/wqb/workflow/nodes/submit_alpha.py:1327  _prod_gate（Step 1.6，fail-closed）
```

### 0.3 同一个 prod 的 8 类载体（互不自动同步）

| 代号 | 载体 | 谁写 |
|---|---|---|
| S1 | 平台 `GET /alphas/{id}/correlations/prod` 的 `max` + `records` | 平台 |
| S2 | `get_alpha_details().is.prodCorrelation` | 平台（提交瞬间冻结） |
| S3 | `alpha_corr_cache`（自称「全库唯一 prod 真值来源」） | `set_corr_cache` |
| S4 | `alphas.prod_correlation` / `prod_corr_source` / `corr_checked_at` | `set_corr_cache` 镜像 + 多处裸 SQL |
| S5 | `submit_ready.prod/self` | `submit_inventory` / `batch_submit_verdict` |
| S6 | checkpoint JSON（`logs/_prod_screen_*_state.json` 等） | 各工具私有 |
| S7 | `results/prod_peek_<id>.json` / `prod_wait_<id>.json` | `prod_wait.py` / `prod_peek_batch.py` |
| S8 | `check_correlation` 返回体（含 `provisional` / `from_cache` / `source`） | MCP 聚合 |

**核心结论：`_corr_cache.py:9-10` 声明的「单一权威」在读取侧只落实了一半，写入侧至少 4 条旁路。**

---

## 1 本次实测与代码的对应（已核验）

| 现象（11-09 夜） | 代码根因 | 位置 |
|---|---|---|
| 三次 240/241s `pending`、`attempts` 178–181 | `_PROD_CORR_WAIT_S = 240` 硬编码；`while True` 只按时间退出，`attempt` 无上限 | `brain_mixin_spcread.py:28, 1335-1355` |
| `inflight=true` 反复出现、同 alpha 后续请求变 busy | pending 时**故意保留** inflight 标记（TTL 300s），异常/取消路径 `result=None` 也不清 | `brain_mixin_spcread.py:1260-1273`；`correlation_slot.py:273` |
| `correlation_busy`，holder 从 `omERn83n` 轮替到 `9qxnPa01` | pending 一律写 195s 冷却 + 释放锁；外部进程排空期间本地反复抢锁 | `brain_mixin_spcread.py:1056-1085, 1274`；`correlation_slot.py:108` |
| `prod_wait --peek --tries 8` 全「空体」 | peek 只读端点不触发重算，5 类失败（HTTP≠200 / 空体 / 非 JSON / 有体无 max / 异常）走**同一重试分支** | `tools/prod_wait.py:46-77` |
| 平台详情 `is.prodCorrelation` 四颗全 None | 未提交 alpha 不回写该字段 ⇒ 预读分支不会误放行（**此处是好事**） | `brain_mixin_spcread.py:948-996` |

⇒ 平台停摆时，本地机制会**自我加锁放大等待**：一次 240s 轮询 → 195s 冷却 → inflight 残留 → busy → 再触发 240s。没有 cancel / 短路 / 全局熔断。

---

## 2 缺陷清单（按风险分级）

### P0 — 可能污染判闸值或放过不该放的候选

**P0-1　peek 值 → 权威缓存没有自动化，且时间戳语义错误**（已核验）
- 全仓 `.py` 中 `prod_peek_*` / `prod_wait_*` **只有写入方，零读取方**（`prod_wait.py:64-69, 116-117`；`prod_peek_batch.py:104-108`）。
- 「免查 prod 提交」的落库是一次手工 SQL：读 peek JSON → 写 `alpha_corr_cache`。**没有工具保证 `at` 被用作 `checked_at`**。
- 正规入口 `persist_correlation`（`_backtest.py:522`）与 `set_corr_cache`（`_corr_cache.py:286`）都用 `now()`＝**写库时刻**，不是平台测量时刻。
- `source` 用 `"no-lock peek"` / `"prod_wait_peek"`，均不在 `CORR_SOURCES` 词表（`_corr_cache.py:73-84`）；裸 SQL 可完全绕过 `normalize_corr_source`。
- 后果：一个几天前算出的 peek 值今天写库 → 48h 保鲜判据认为「刚测过」→ `_prod_gate` 缓存命中分支直接放行（`brain_mixin_correlation.py:938-957` 不带 `provisional`）。这是**合规链最大的洞**：`_prod_gate` 的 provisional 判据只认 `alpha_detail_cached`（`submit_alpha.py:1394-1396`），认不出 peek 来源。

**P0-2　`set_corr_cache` 无条件刷新 `checked_at`**（已核验）
- `_corr_cache.py:269-279`：`p = _corr_value(prod)` 越界→None；但 `recs_json="[]"` 非 None ⇒ `:278` 的 `no_valid_value` 短路**不触发**。
- SQL `:298-302`：`prod_correlation=COALESCE(...)` 保留旧值，却无条件 `checked_at=excluded.checked_at`。
- 后果：一次无效/畸形响应把**旧的 prod 值洗成「刚测过」**，污染 48h 保鲜。

**P0-3　`parse()` 会把直方图数字当成 prod**（已核验）
- `prod_wait.py:28-34`：`max` 缺失时遍历 `records` 取最大数值。平台 records 形如 `[low, high, n]`，可能返回 bin 上界 `1.0` 或计数 `n`（成千）。
- 该值直接写入 `results/prod_peek_<id>.json`，而该文件正是「免查提交」的数据源。`prod_peek_batch.py:39`、`full_template_campaign.py:632` 复用同一缺陷。

**P0-4　旁支存在 fail-open / 忽略 provenance**
- `src/wqb/workflow/nodes/judge.py:379-381, 392-399`（已核验）：`__error__` → `pass=True`；`prod_max is None` 不加 reason → `pass=True`。可产出 `READY`。
- `tools/batch_submit_verdict.py:277, 289-294, 329-384`：`refresh=False` 的缓存/预读值即可升 `SUBMIT_LAYER_VERIFIED`，完全不检查 `provisional` / `from_cache` / `stale`；且 pending 行写 `phase2_done=True` 后**永不再验**（`:296-301`）。
- `tools/verdict/submit_inventory.py:823-826`：`--snapshot-only` 强制 `fresh=True`，可把过期台账值判 `SUBMIT_NOW`。
- `tools/prod_saturation_gate.py:297-299`：缺值当 `0.0` 参与 wall_ratio，稀释撞墙比例。
- ⚠ 澄清：**`_prod_gate` 本身是 fail-closed**（`submit_alpha.py:1421-1426`，已核验），没有「拿不到就放行」。风险全在评审/队列/盘点这些旁支。

### P1 — 一致性与可靠性

| # | 问题 | 位置 | 影响 |
|---|---|---|---|
| P1-1 | `provisional` 由 `.get('provisional', True)` 拼出，上游契约里不产出该字段 | `brain_mixin_correlation.py:1025, 1029` | 上游某天显式带 `provisional=False`，判闸语义静默反转 |
| P1-2 | 强制重测后 `:1414` 重算 `provisional`，但 `:1436-1445` 的 allowed 判定不再检查它 | `submit_alpha.py`（已核验） | 理论残留放行口 |
| P1-3 | 单源读未落实：`get_submit_ready` 值取 S5、时间戳只查 S4、跳过权威 S3 | `wqb_db_mcp.py:468-495`；`store/submit_queue.py:1488-1491` | S3 有新鲜值却被标 `no_timestamp`/stale |
| P1-4 | `get_alpha_corr_metrics` 只读 `alphas`；`triage_prodcorr_batch.py:61-62` 裸 SQL 不写 source/时间戳/S3 | `wqb_db_mcp.py:1570-1589` | 与「S3 唯一权威」矛盾，历史行长期漂移 |
| P1-5 | 240s 两份独立字面量（MCP `_PROD_CORR_WAIT_S` vs `config.WAIT_THRESHOLDS`），只靠正则守护测试比对 | `brain_mixin_spcread.py:28`；`config.py:599`；`tests/.../test_wait_thresholds.py:36-43` | 改配置不影响 MCP；docstring `:1106` 还写「1 hour」 |
| P1-6 | 无取消机制；异常/取消时 `result=None` ⇒ inflight 不清除，残留 300s | `brain_mixin_spcread.py:1253-1273` | 同 alpha 后续全 busy |
| P1-7 | `prod_wait.py` 不区分 4xx 终态：peek 重试到 `tries` 用完，带锁模式对 `data_unavailable` 重试 45 分钟；且外层 20s/320s 套内层 240s = 嵌套轮询 | `prod_wait.py:51-76, 119-120`（已核验） | 终态错误被当成排队 |
| P1-8 | `corr_age_hours` 对 aware 时间戳 + naive `datetime.now()` 相减抛 TypeError → 返回 None → stale | `_corr_cache.py:122-146`（已核验） | 有效时间戳被误判无缓存（fail-closed，但造成无谓重测） |
| P1-9 | `use_pre_read` 被重载成 `refresh` 开关，连带关掉 inflight join 与 same-alpha join | `brain_mixin_spcread.py:1160, 1167, 1201` | 只想「别预读」的直连调用方失去 join；`refresh=True` 撞锁直接 busy |
| P1-10 | 预读 `is.prodCorrelation` 只 `float()`，无 `[0,1]` 值域校验，直接进入判闸 | `brain_mixin_spcread.py:980-986`；`brain_mixin_correlation.py:1020, 1042` | 异常值可造错误 PASS/FAIL |
| P1-11 | `0.7` 硬编码 ≥10 处、`48h` 三处独立实现 + 两套时间解析 | `submit_alpha.py:45`、`judge.py:30`、`super_build.py:132`、`wqb_db_mcp.py:1547` 等 | 目前数值巧合，改一处必漂移 |
| P1-12 | 跨进程锁在模块缺失/异常时降级为「仅进程内锁」放行；sidecar 读-改-写非原子 | `brain_mixin_transport.py:377-422`；`correlation_slot.py:287-305` | 多进程并发打平台相关性接口（正是该模块记录的事故形态） |
| P1-13 | 48h 保鲜只由「写库时刻」决定，`_prod_gate` 不校验 `cached_at` | `submit_alpha.py:1419, 1435`（已核验） | 与 P0-1 叠加成完整绕过链 |

### P2 — 可维护性

- **8 份 `check_correlation` 返回体解析拷贝**，字段名四套（`checks.production.max_correlation` / 顶层 `max_correlation` / `correlation.max` / `get_production_correlation().max`）；**5 套 prod 闸判据**（`submit_alpha` / `super_build` / `judge` / `batch_submit_verdict` / `submit_inventory`），策略互不相同。
- **3 份 `parse()`**（`prod_wait.py`、`prod_peek_batch.py` 复用、`full_template_campaign.py` 自抄）。
- 文档与实现不符：`brain_mixin_spcread.py:1106` 的「1 hour」；`submit_alpha.py:1463` 称 `prod_gate_audit` 是「400+ 请求」而实际 ≤ ~22 GET（`prod_gate_audit.py:112`）；`select_ra_basket.py:161` 自称「更严」但 `PROD_FRESH_DAYS=2` 同为 48h。
- `last_known`（含 `max` / `age_hours` / `stale`）原样透传给 Agent，注释反复声明「不可判闸」但无机器护栏（`mcp_core.py:408, 447`）。
- `prod_gate_audit.py` 核对结论：**账户级事后审计、不接提交路径**（已核验设计意图），分工声明正确，仅请求数注释夸大。

---

## 3 优化建议（按 ROI 排序）

### 第一批：堵住合规洞（改动小、收益最大）
1. **新增 `tools/prod_peek_ingest.py`**：读 `results/prod_peek_<id>.json`，以 `at` 为 `checked_at` 调 `set_corr_cache`（该参数已支持，`_corr_cache.py:251, 286`），`source="prod_peek"`；带 `--dry-run` 与值域/时效校验。**消灭手工 SQL**。
2. `CORR_SOURCES` 增加 `prod_peek`（`_corr_cache.py:73-84`）；`_prod_gate` 的 provisional 判据（`submit_alpha.py:1394-1396`）把它与 `legacy` / `manual` / `unknown` 一并纳入「不可直接放行」，或单独设「非实时来源」集合。
3. 修 `set_corr_cache`：仅当 `p is not None or s is not None` 时才刷新 `checked_at`；纯 records 更新走独立分支（`_corr_cache.py:278, 302`）。
4. 修 `parse()`：`max` 缺失直接返回 None，不扫 records；直方图单独解析（`prod_wait.py:28-34`）。

### 第二批：统一判据与单源读
5. 抽公共 `prod_verdict(corr_result) -> {value, usable, provenance, age_hours, reason}`，统一处理 `provisional/from_cache/cached_at/stale/pending/busy/data_unavailable`，替换 8 份解析；`batch_submit_verdict._phase2_outcome`、`corr_check._query`、`judge._eval_correlation` 优先。
6. 堵 fail-open：`judge.py:379-381, 392-399` 缺值改 `pass=False`（或让 `_compute_final_verdict` 计入 `unavailable`）；删 `submit_inventory.py:823-826` 的强制 `fresh=True`；`batch_submit_verdict` 检查 provenance 且 pending 不写 `phase2_done`。
7. 单源读：`wqb_db_mcp.py:1574`、`submit_queue.py:1489`、`prod_first_screen.py:105,283,457`、`prod_saturation_gate.py:261` 全改走 `get_corr_authoritative[_batch]`，让 `corr_stale` 与判闸值同源。
8. 阈值/保鲜常量收敛到 `wqb.config`（`0.7` / `48h` / `240s`），MCP 侧 import 而非字面量；`corr_age_hours` 统一转 UTC 或统一 naive。

### 第三批：可用性与平台停摆韧性
9. 给 `check_correlation` 加**可配置超时 + 取消入口**：`_PROD_CORR_WAIT_S` 改读 `WAIT_THRESHOLDS`，`tools_corr.py` 暴露 `timeout_s`；`finally` 里无条件清 inflight（异常路径用独立标志）。
10. **全局熔断**：检测到连续 N 次 `pending` 或 holder 持续轮替时，写账号级 `prod_unavailable_until`，期间所有调用直接返回 `status=platform_unavailable`，不再各自耗 240s —— 直接解决 11-09 夜的 3×241s 空转。
11. `prod_wait.py` 识别 `data_unavailable` / 4xx 立即退出；带锁模式去掉嵌套轮询（内层已有 240s 窗口，外层只按 `retry_after` 退避）；产物补 `source` / `status` / `histogram`。
12. `_corr_release_plan` 参考 `computed` 分流，`pending` 且 `saw_empty=False` 时不写满 195s 冷却；`platform_retry_after` 在成功后清除。

### 附：文档校正
`brain_mixin_spcread.py:1106`（1h→240s）、`submit_alpha.py:1463`（400+→≤22 GET）、`select_ra_basket.py:161`（删除「更严」）。

---

## 4 边界澄清（避免误改）

- `_prod_gate`（Step 1.6）**已 fail-closed**，不要改成「拿不到值就放行」；优化目标是让它**能识别更多不可信来源**，而不是放宽。
- `confirm_submit=False` 预检完全不读 prod（`submit_alpha.py:479`），是有意设计。
- Step 5 单颗恒等式是信息项、不阻断（`submit_alpha.py:732-750, 1448-1493`），与账户级 `prod_gate_audit.py` 分工正确，不要合并。
- 「已提交短路」跳过整段 gate（`submit_alpha.py:344-365`）是幂等设计；若本地状态错判需另加平台状态复核，不动短路本身。
- 平台 prod 是**账号级单并发**，任何「并发测多颗」的优化都必须保留锁；`--peek` 无锁只读是刻意例外，不得改成触发重算。

---

## 5 关键文件索引

| 层 | 文件 |
|---|---|
| MCP 注册 | `world-quant-brain-mcp/tools_corr.py`、`mcp_core.py` |
| 编排 / 缓存读写 | `world-quant-brain-mcp/brain_mixin_correlation.py` |
| 平台轮询 / 锁 / inflight | `world-quant-brain-mcp/brain_mixin_spcread.py`、`brain_mixin_transport.py` |
| 跨进程 sidecar | `src/wqb/correlation_slot.py`、`src/wqb/db_write_lock.py` |
| 权威缓存 | `src/wqb/store/_corr_cache.py`、`src/wqb/store/_backtest.py` |
| 提交闸 | `src/wqb/workflow/nodes/submit_alpha.py`、`src/wqb/submit_verdict_core.py` |
| 工具层 | `tools/prod_wait.py`、`prod_peek_batch.py`、`corr_check.py`、`batch_submit_verdict.py`、`verdict/submit_inventory.py`、`gates/prod_gate_audit.py` |
| 守护测试 | `world-quant-brain-mcp/tests/test_corr_db_cache_unit.py`、`tests/unit/07_docs_skills/test_wait_thresholds.py` |

---

## 6 落地记录（2026-11-10，用户指令「落地所有建议」）

### 6.1 已实现（逐项对应 §3）

| 建议 | 实现 | 位置 |
|---|---|---|
| 1 peek 落库工具 | 新增 `prod_peek_ingest.py`：以产物 `at` 作 `checked_at`、三重校验、`--dry-run`/`--all`/`--json` | `tools/prod_peek_ingest.py` |
| 2 来源登记 + 闸识别 | `CORR_SOURCES` 加 `prod_peek` + 4 条历史别名；新增 `NON_REALTIME_SOURCES`；`_prod_gate` 加 `_cache_source_untrusted`，缓存命中也带 `provisional` | `store/_corr_cache.py`、`store/__init__.py`、`nodes/submit_alpha.py`、`brain_mixin_correlation.py` |
| 3 checked_at 条件刷新 | `has_value` 门控 SQL `CASE WHEN`，纯 records 更新不触碰时间戳/来源；mirror 也只在有值时写 | `store/_corr_cache.py:set_corr_cache` |
| 4 parse 修复 | `max` 缺失即 None + `[0,1]` 值域校验；`full_template_campaign` 改 import 复用 | `tools/prod_wait.py`、`tools/full_template_campaign.py` |
| 5 唯一判据 | 新增 `prod_verdict()` / `gate_allowed()`；接入 judge / corr_check / batch_submit_verdict | `src/wqb/prod_verdict.py` |
| 6 堵 fail-open | judge 缺值→`pass=False`→BLOCK；phase2 查 provenance 且 PENDING 不写 `phase2_done`；snapshot-only 不再强制 fresh、取数失败置 None；saturation 缺值不当 0.0 | `nodes/judge.py`、`tools/batch_submit_verdict.py`、`tools/verdict/submit_inventory.py`、`tools/prod_saturation_gate.py` |
| 7 单源读 | 三处优先权威表、缺则回落 alphas | `wqb_db_mcp.get_alpha_corr_metrics`、`store/submit_queue._corr_checked_times`、`tools/prod_first_screen.targets` |
| 8 常量收敛 | `0.7`→`PRODCORR_CEILING`；`48h`→`CORR_FRESH_HOURS`；`240s`→`WAIT_THRESHOLDS`（MCP 运行时真读 + fallback）；`corr_age_hours` 统一 UTC | `config` 消费点、`store/submit_queue.py`、`brain_mixin_spcread.py` |
| 9 可配置窗口 + inflight 清理 | `check_correlation(timeout_s=)` 透传 `max_wait_seconds`；finally 改「非 pending 即清」覆盖异常/取消路径 | `tools_corr.py`、`brain_mixin_correlation.py`、`brain_mixin_spcread.py` |
| 10 账号级熔断 | `correlation.unavailable.json` + `note_pending_streak`/`clear_unavailable`/`unavailable_remaining`；`acquire` 与 `get_production_correlation` 短路返回 `platform_unavailable` | `src/wqb/correlation_slot.py`、`brain_mixin_spcread.py`、`brain_mixin_correlation.py` |
| 11 prod_wait 韧性 | 4xx / `data_unavailable` 终态早退；去嵌套轮询（按 `retry_after` 退避）；产物补 `source`/`status`/`histogram`；批量版同步 | `tools/prod_wait.py`、`tools/prod_peek_batch.py` |
| 12 冷却分流 | `pending` 且 `computed=False` 不写冷却；Retry-After 步长压制加 `retry_after_active`（空体后解除，变量保留供 meta） | `brain_mixin_spcread.py` |
| 附 文档校正 | 1h→240s 阶梯；400+→≤22 GET；删除「更严」不实注释 | `brain_mixin_spcread.py`、`nodes/submit_alpha.py`、`tools/select_ra_basket.py` |
| 额外 P1-1/P1-8/P1-12 | `provisional` 由上游显式产出；未知 `correlation_type` 底层校验（防假通过）；sidecar 读改写加 `_sidecar_lock` 原子保护 | `brain_mixin_spcread.py`、`brain_mixin_correlation.py`、`correlation_slot.py` |

### 6.2 新增守护测试（60 项，全过）

- `tests/unit/09_core/test_prod_corr_hardening_20261110.py`（15）：checked_at 不被洗新 / 时区 / 词表 / parse / ingest
- `tests/unit/09_core/test_prod_verdict_20261110.py`（21）：唯一判据的来源分层与 fail-closed
- `tests/unit/09_core/test_corr_resilience_20261110.py`（12）：熔断 / sidecar 原子性 / 短路 / timeout 透传
- `tests/unit/05_submit_quota/test_prod_gate_nonrealtime_20261110.py`（12）：非实时来源强制重测与残留 provisional 拦截

### 6.3 契约变更（旧测试同步更新）

| 旧断言 | 新契约 | 文件 |
|---|---|---|
| judge 相关性不可用 → `pass=True` | → `pass=False` + BLOCK | `tests/unit/02_workflow/test_workflow.py` |
| 正则比对 `_PROD_CORR_WAIT_S = 240` 字面量 | 运行时断言与 config 同源（更强） | `test_wait_thresholds.py`、`test_correlation_slot.py` |

### 6.4 配套回写

- `docs/experience/01_platform_gates.md`：新增「2026-11-10 机制加固」小节 + 熔断表格行 + inflight 异常清理口径
- `docs/env_registry.json`：登记 `WQB_CORR_UNAVAILABLE_SEC` / `WQB_CORR_UNAVAILABLE_STREAK`，`tools/index_tables.py --apply` 重生成嵌入表
- `src/wqb/corr_timing.py`：`platform_unavailable` 进 `NO_VALUE_EVENTS`（不进 `PLATFORM_EVENTS`——它没发请求）

### 6.5 未落地项（明确留口）

- `submit_inventory.fetch_corr` / `triage_prodcorr_batch` / `campaign_intel` / `backfill_prod_corr` 的解析拷贝未全部替换为 `prod_verdict`（已替换风险最高的 judge / corr_check / phase2 三处；其余为盘点/统计用途，不直接判闸）。
- `brain_mixin_transport` 跨进程锁模块缺失时的「降级放行」保留原语义（已有 `degraded` 标记）；改成 fail-closed 会影响单进程宿主，需单独评估。
- `use_pre_read` 与 `refresh` 的语义重载保留（解耦需改签名并盘点全部直连调用方）。

### 6.6 生效前提

⚠ **MCP 服务需重启**才生效（`.mcp.json` 指向 `world-quant-brain-mcp/main.py`，HTTP 常驻）。
本次改了 `brain_mixin_spcread.py` / `brain_mixin_correlation.py` / `tools_corr.py`，
重启前运行的服务仍是旧逻辑。重启走 `tools/start_wq_mcp.py --all`。

