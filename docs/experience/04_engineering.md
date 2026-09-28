# 04 · 工程与流程纪律

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-09-29
> 项目工程规约总纲见仓库根 `AGENTS.md`；本文只收**踩坑固化的纪律**，与 AGENTS.md 互补。

---

## 1. ★ skill 单点写入（最高频踩坑）

- **改 skill 只写仓库 `Claude/skills/`**，再 `python tools/sync_skills.py`；
  **禁止直接编辑安装位**（`~/.claude` / `~/.codex` / `~/.cursor` / `~/.workbuddy` / `.qoder-cn`）。
  → 直改安装位会被 `test_sync_skills_reports_no_drift` 判**漂移红**（2026-09-28 亲历）。
- **解析顺序权威**：`WQ_SKILLS_DIR` → `~/.claude` → `~/.codex` → 历史位（.trae-cn / .qoder-cn / .cursor / .workbuddy）→ 仓库 `Claude/skills`（兜底）。
- **并会话改 skills 源后漂移门禁会反复翻红** → 把 `python tools/sync_skills.py && git commit` **串成一条命令**压竞态窗口。
- **SKILL.md 里的 Markdown 链接不能写 `../../../docs/...`**（安装位无 `docs/`，会被 `test_markdown_links_resolve` 拦）→ **写仓库根相对路径**如 `docs/...`。
- **批量改 skill 元数据前先问「有没有嵌套同体副本」**：GEM 内嵌 `brain-feature-implementation` 不在顶层 33 个 `*/SKILL.md` 扫描范围内，漏改即被 `test_embedded_fi_copy_matches_authoritative` 抓红。
- **`last_verified` 的含义是「对照平台核实过」，不是「改过这个文件」**：批量刷新 = 伪造信号（曾把 33 个全刷成 09-26，实际只复核 13 个，已回退 20 个）。
  相关测试 `test_last_verified_not_older_than_last_commit` 用 `git log -1 --format=%cs` 做**严格 >=** 比较
  → **批量提交 SKILL.md 正文后必须同步 bump `last_verified`，且要跑一次全量测试在提交之后**。

---

## 2. DB 连接 / 写锁

- **禁裸 `sqlite3.connect`**（有静态白名单测试 `test_db_write_guards.py::TestNoNakedSqliteConnect` 守护）。
  白名单 = `db_conn.DIRECT_CONNECT_WHITELIST`，`EXCLUDE_PREFIXES=("backfill_","migrate_","triage_",…)` ⇒ **新建工具必须走 `wqb.db_conn.connect` 工厂**。
- **只读查询用 `readonly=True`**（否则 `PRAGMA journal_mode=WAL` 会改库字节）。
- **DB 并发写锁**：连接收口到 `src/wqb/db_conn.py`（WAL + `busy_timeout=60s`）；
  文件锁 mutex `src/wqb/db_write_lock.py`。
  ⚠ **mutex 不能用 DB ledger 实现**——抢锁本身是写库，自举悖论 → 用 `logs/_dblock/dbwrite.lock.json` 单文件 `O_EXCL` 原子锁。
- **`submit_ready` 等热表加 `timeout=30` + `PRAGMA busy_timeout=30000`**。
- **SQL 空集合禁拼 `IN ()`**：空 list 拼进去变 0 占位符 → `ProgrammingError: Incorrect number of bindings`。**必须先 `if ids:` 短路**。
- **DB 列名坑**：`alphas` 表是 `region_id`（数字外键）**非 `region`**、`created_at` 非 `date_created`；
  `fields` 表是 `coverage` 非 `coverage_ratio`；`datasets` 表 `name` 才是 dataset 名。`alphas` 插入必须有 `region_id` + `dataset_id`（NOT NULL）。
- **索引不能写在 CREATE SCHEMA 里**：`CREATE TABLE IF NOT EXISTS` 对已存在表是 no-op，缺列时 `CREATE INDEX` 报 `no such column: skeleton`
  → **索引移进 `_migrate()`，先补列再建索引**。
- **join 两表做分组统计前必须先验证关联键覆盖率与唯一性**：`expressions.alpha_id` 覆盖率**仅 40%**，
  用 expression 文本 join 导致 391 行→148 行、区域误归因（GLB 34→15、KOR 12→4、HKG 5→0），据此得出的结论全部撤回。

---

## 3. 闸 SEM（字段语义归类，2026-09-28 新增硬环节）

- **起因**：步 3 只做了 `scan_fields`（typed catalog：类型/覆盖/users），**没做字段经济含义归类**就直接进 GEM，
  导致 KOR/fundamental17 首波 348 条里 **49.4% 是货币代码/汇率三角套汇恒等式**，总废产物 **71%**。
- **三层固化（缺一不可）**：
  1. `tools/field_semantic_classify.py --region R --dataset DS --write-ledger` → ledger `s1_semantic_<ds>`
  2. `tools/wave_gate.py` **闸 SEM（fail-closed）**：缺台账 → **exit 2 整波阻断**；命中黑名单字段的表达式**直接剔出候选**。唯一逃生 `--skip-semantic-gate`（打印醒目告警）
  3. 回归 `tests/unit/test_semantic_gate_failclosed.py`（9 条）
- **闸 SEM 曾只在内存剔除、未落库** → `gate.py`/`pipeline.py` 按 `expressions.status` 取数，172 条语义垃圾照样进批 → 已修（`from_db` 时 `UPDATE expressions SET status='dropped'`）。
- **`gate_results.all_pass` 列恒为 0** 与 `report_json.gate.all_pass=true` 打架（停止规则 C 会误杀）→ 已修（末尾用真实 verdict 覆盖写一次）。
- ⚠ **边界**：本步产物是**字段池，不是 ideas** —— 严禁当 `ideas.md` 注入 GEM（会让 GEM 退化为「每字段套 rank」）。
- **池约束是 GEM 产物质量的第一杠杆**（同一 GEM 引擎，仅换池）：
  | 指标 | fundamental17 首波（无池） | risk70（28 字段池） |
  |---|---|---|
  | 落在池内 | 3.2% | **87.4%** |
  | 含行业哑变量/货币码 | 49.4% | **4.8%** |
  | 不同骨架数 | 12 | **91** |

---

## 4. workflow 节点注册

- **新增/修改 workflow 节点 → 四处必须同步**（漏一处测试即红）：
  ① `src/wqb/workflow/registry.py`（register + NodeMeta，与 `run()` 签名逐字一致）
  ② `tests/unit/test_workflow.py::test_registry_lists_all_core_nodes` 期望集合
  ③ `tests/unit/test_skill_integrity.py::_DRY_RUN_CASES` 干跑用例表
  ④ `Claude/skills/INDEX.md` workflow 节点计数
  → **一次跑完全部检查**：`python tools/audit_node_registration.py`（退出码 1 = 有漂移并列出全部缺口）。
- ⚠ **`audit_node_registration.py` 只校验 registry 元数据 vs `run()` 签名，不覆盖 `tools_workflow.py` 自动注入的参数**
  → `gem→batch_track` 链自动插入 `prod_family_gate` 而 `wave_gate.run()` 无此形参，链必 TypeError 且守护零命中。已单列 `tests/unit/test_wave_gate_auto_insert_contract.py`。
- **argv 契约校验**：拼子进程命令的节点必须过 `_common.validate_argv(cmd)`
  → 起因：`batch_track` 给 `pipeline.py run` 拼了个不存在的 `--concurrency 7`，argparse exit=2，而 detached 分支不看退出码 → **S3 每次"启动成功"却从未真跑，证据在 `stderr.log` 里躺了 13 天**。
- **detached 存活握手**：后台启动后必须过 `_common.detached_launch_failed()`——秒退或 stderr 非空即判失败（"启动即死"不能再被吞成 `success=True`）。
- **dry-run 契约**：全部节点统一「走完零成本前置 → 构建出命令/请求计划 → 到此为止」，不 subprocess、不写库、不建目录。干跑失败**必须带得出 `error`**（禁止 `success=False + error=None`）。

---

## 5. MCP 服务

- **`@mcp.tool()` 装饰器后不能插模块级代码**（两次亲历）：插在装饰器与 `def` 之间 → ① `SyntaxError`；② 装饰器被私有 helper 抢走、目标函数失去注册（`test_no_private_function_is_an_mcp_tool` 逮到）。
  → **往 `wqb_db_mcp.py` 插函数必须插在目标函数「之后」**。改后需**重启 MCP**，核对 `@mcp.tool()` 计数（wqb-db = 44）与 INDEX 一致。
- **MCP 新增工具需重启服务才在会话可见**（工具表在会话启动时构建）。
- **MCP 服务器命名只能是 `wq-brain-http` 与 `wqb-db`**——所有 skill 调用前缀是 `mcp__wq-brain-http__*` / `mcp__wqb-db__*`，改名即全线失配。
- **MCP 排障链**：工具搜不到 = 服务端没起；`mcp_core.py` 默认 `MCP_PORT=8000` 而 `~/.workbuddy/mcp.json` 指向 **8876**；
  streamable-http 需先 `initialize` 拿 `Mcp-Session-Id` → `notifications/initialized` → `tools/list`，响应是 SSE 分块须用 `json.JSONDecoder().raw_decode` 逐块解析 `data: ` 前缀。
- **核查引用面必须同时用完整名 + 短名 grep**：用 `mcp__wq-brain-http__search_forum_posts` 得零命中 → 误判「MCP 未接入」，改用短名 `search_forum_posts` 才找到真身。

---

## 6. 回测 / 批跑

- **脚本必带 checkpoint**（断点续跑）；异常数据集不进 checkpoint 需可重跑补回；**ckpt 缓存旧失败结果会卡住**（清 `ckpt_w*` 后重跑即过）。
- **`CONCURRENT_SIMULATION_LIMIT_EXCEEDED`**：批量建仿真互相挤兑，前序大实验未清干净时后续全被拒
  → **重跑前必须先清掉 checkpoint 的 `error` 条目**（否则脚本判定"已完成"直接跳过）；pipeline 首次失败会留 `ckpt_w<wave>`，重跑必须加 `--fresh`。
- **勿在未清遗留仿真任务时开新批**（IND 曾 36 min 全废）。
- **pipeline 应避免 n=1 批**：单条 unit 错 → WARNING 非终态 → poll 永久挂死。
- **`nohup ... &` 在 bash 工具里会被 shell 退出带走** → 用工具级 `run_in_background`。
- **收批与 pipeline 轮询不要并发**：`GET /simulations/{multisim_id}` 在**并发读同一 multisim 时返回 404**（不是 409/423）。
  实证：CLI 收批那一刻 pipeline 正在轮询同一批 → 21 个 ID 里 20 个 404；kill 掉 pipeline 后同样 ID 重跑全部 200。
  → **先确认 pipeline 已退出，再跑收批工具**。
- **multi-sim children 返回裸 simulation ID**（无 `/simulations/` 前缀）→ 直接拼 base_url 变非法主机（`api.worldquantbrain.com2UGF...`）报 **SSL EOF 假象**；瞬态 SSL EOF 重试即过。
- **异步任务查询**一律用 `mcp__wq-brain-http__workflow_task_status`（认 `<id>.json` 与 `<id>/meta.json` 两套布局），不要 shell 出去翻 `logs/_async_tasks/`。
- **`explore_contract` 自学习多样性契约到期会拦发批**（fail-closed，正确行为）：
  ① 第一次报 `[DIVERSITY-EXPIRED] 契约已消费满 10/10 批 → 自动续约新契约，请重跑闸门`；
  ② 第二次报 `[batch_gates] 已完成（checkpoint），跳过。ok=False` —— 上一轮把 `ok=False` 写进了 checkpoint。
  **正确处置**：`pipeline.py` 的 checkpoint 存在 **DB** `ledger_kv/<REGION>/ckpt_w<wave>`（**不是** `tracking/*/results/` 文件；只有传 `--checkpoint-dir` 才落文件）
  → 先重跑 `workflow_execute(node="wave_gate")` 按新契约校验，再**清掉该波 checkpoint**
  （`DELETE FROM ledger_kv WHERE region=? AND key='ckpt_w<wave>'`，前提是该波尚未提交任何回测），然后重发批即成功。
  ⚠ **不要用 `--gate-mode warn` 或裸 `--skip-diversity-gate` 绕过**——这类失败不是真实的多样性不足。

---

## 7. 测试

- **全量 pytest 失败若信息带 `[safe-delete]` 即环境噪声，不是回归**：沙箱守卫在累计删除数越阈值后拦截所有含删除动作的子进程 CLI。
  定性环境性假失败的**四条硬证据**（缺一不可）：① 失败报错文本全部同一条；② 涉及业务断言的失败 0 个；③ 涉事测试文件单独跑通过；④ 上一提交钩子已实跑全量通过。
- **summary 行常被守卫提示截断** → 改用 `--junit-xml=` 解析统计。
- ⚠ **不要用 `--basetemp` 指向仓库内目录**（会让扫描型测试如 `test_docs_consistency` 炸，曾误报 42 failed）。
- **守护测试必须配反向负例（防假绿）**：`test_no_bare_tool_or_node_counts_outside_index` 曾靠「行内含 INDEX/唯一基准即放行」的关键字豁免让过时计数逃逸
  → 改为语境约束正则 + 取消豁免 + 新增 `test_bare_count_guard_is_not_vacuous()`（4 条历史逃逸样本必命中）。
- **改测试让它绿是反模式**：判据不是"谁写的"，而是该值是否有**多重权威佐证**。
- **随机量的断言边界一律按 `uniform` 满幅推导**，别写死常数
  （`test_retry_wait_exponential_backoff` 上界写死 9.0 漏算 0.0112，20 万样本实测 **1.4% 误报失败率** → 按公式推导上界后 30 连跑 0 flaky）。
- **临时验证脚本用完即弃，永久断言进 `tests/`**（`logs/_tmp_verify_*.py` 留着会变成"过期且会失败的第二个真相源"）。
- **失败诊断 7 步**：完整 traceback → 根因聚类（不逐条修）→ **端到端最小复现** → 区分"测试期望过时"（改测试）vs"代码回归"（改代码）→ 查状态文件 → 新失败定性 → 沉淀固化。

---

## 8. Git 与提交

- **绝不 `git add -A`**，用显式路径清单；按主题拆笔；**并行工作流的改动不进自己的 commit**。
- **提交前必须跑删除量聚合**（09-05 靠此救回 `mining/scripts/` 被完全清空的 14 个脚本）。
- **提交前必扫密钥**：`.env` / `config.json` / `sk-` / `AKIA` / `ghp_` / `xoxb_` / `PRIVATE KEY` / `password`。凭据文件提交前先 `git check-ignore -v` 验一遍。
- **git 僵死 index（unmerged 但无 MERGE_HEAD）**：`git reset`（mixed，**只清 index 不动工作区**）→ checkout/pull 成功，170+ 未提交修改零丢失。
- **`.git/index.lock` 陈旧锁**应重命名为 `.stale_*` 而非删除，保留可回滚。
- **重命名用 `git add -u` + `git add`** 让 git 识别 R100。
- **bash 多行提交信息**：`@'...'@` 是 PowerShell 语法，bash 会把 `@` 当普通字符拼进词导致 subject 变 `@ xxx`
  → **Bash 传多行提交信息必须用 `git commit -F <file>` 或 `$'...'`**。
- ★★ **`--no-verify` 的合法前提（已固化判据，勿滥用）**：
  曾因 `src/wqb/db_write_lock.py` 每次写锁都 `os.unlink()` 清理 `logs/_dblock/dbwrite.lock.json`，
  全量套件的子进程测试把**同一文件**的删除在本会话累积到 **167 次 > 守卫阈值 50** → 守卫拦 unlink → 子进程 rc=1 → 断言失败。
  定性**环境性假失败**的**四条硬证据（缺一不可）**：
  ① 全部失败的报错文本是同一条 `SAFE_DELETE_BULK_CONFIRM_REQUIRED`（实测 31 个失败全同一条）；
  ② 涉及**业务断言**的失败 **0 个**；
  ③ 涉事测试文件**单独跑通过**（24 passed）；
  ④ 上一提交的钩子已在同工作区实跑全量通过，且本批暂存集**纯数据/文档、无任何被测试导入的 .py 改动**。
  守卫计数按 **turn** 累积、本会话已饱和、无法本轮归零 → 经用户明确授权后才可用 `--no-verify`，并把上述定性写进提交信息。
  ⚠ **与 pytest 收尾删 `pytest-of-<user>/garbage-*` 的区别**：那条可用 `--basetemp` 规避；这条是**业务代码自身的 unlink**，无法用 `--basetemp` 规避，只有换轮次或 `--no-verify`。
- **并行会话共存纪律（提交时）**：① **不 add、不 commit、不 delete** 任何非本轮范围的已跟踪改动；
  ② 重写提交前先用 `md5sum` 指纹留底、重写后 `md5sum -c` 校验一致；
  ③ 用 `commit-tree` + `update-ref` 而非 `reset --hard`（后者会毁掉并行改动）。

---

## 9. 并发会话纪律

- **陌生失败先 `git status --porcelain` + mtime 判归属，非己所写勿擅动**。
- **"长时间无 mtime 变化"不能证明会话停摆**；**Edit 前必须重读文件最新内容**。
- **追加记忆日志必须先读尾部再 Edit 追加，禁止整文件 Write**（会覆盖并行会话内容）。
- **清理产物时只删自己明确产生的**（靠 mtime + 命名后缀判归属）。
- 提交前重跑 `sync_skills --check`；跨会话的未提交改动留给 owner 提交。

---

## 10. 数据漂移通则

- **写路径归一与读取方解释不一致**是经典根因（三套 wave verdict 分类器实测分歧 32/72 行）
  → 必须同改**所有写入方 + 唯一消费方 + 分类器同答测试**。
- **`s0_whitelist` 存在 schema 漂移 × 消费者错配 → 全线 fail-open**：同一 ledger 键 5 种形态（`candidates[]`/`whitelist[]`/`datasets[]`/`other`/非 dict），
  3 个消费者各自在不同区域子集外静默失效；GBR 还是双重 JSON 序列化
  → 统一 schema + **消费者改 fail-closed 打 WARN** + 加单测遍历全区域断言 schema 唯一。
- **状态文件陈旧会掩盖真实漂移**：`normalize_ledger_whitelist` 报"已完成跳过"，实际是 `logs/_state_*.json` 陈旧 → 环境/数据类失败**先查状态文件**，必要时 `--fresh --apply`。
- **演练脚本的 SQL 错误被降级吞掉会把错误数据当结论** → 降级路径必须显式暴露（`[SQL-ERR]` 不得静默）。
- **每次 dry-run 至少逮住一个"文档说 A、数据是 B"的口径错位**（键名大小写、JSON 结构、配置位置）。
- **`signal_floor` 权威位置是 `tracking/<R>/config/thresholds.json`**，不是 profile md。

---

## 11. 死代码判定三原则

1. **子串 grep 会系统性高估引用**（ledger key 字符串命中不算 import）→ 须 token 级计数 + 人工判别。
   同理：`grep -rl` 会误算指向 HOME 的 `~/.brain_mcp_config.json`（10 处"引用"全是这个）。
2. **dotted token（`from wqb.research.selection_contract import`）须按 `.`/`/` 切分**，否则把活模块误判死代码。
3. **`refs=0` ≠ 死代码**，须再看有无 `__main__`（有 = 未登记 CLI，不能删）。

→ 据此把 22 个疑似收敛到 6 个。

---

## 12. 其他踩坑

- **凭证三级发现链**：`~/.brain_credentials` → `~/.brain_mcp_config.json` → 项目 `world-quant-brain-mcp/.env`。
  原 `load_creds()` 无 `os.path.exists` 检查，单点文件消失即全链路瘫痪（09-08 事故）。
- **`~/.brain_mcp_config.json` 被写入 UTF-8 BOM 会让认证全线失败**；`brain_config.py` 曾 `import logging` 却从未定义 `logger`，错误路径抛 `NameError` 掩盖真因。
- **`Api.post(path, payload_dict)` 的 payload 是 dict 不是 JSON bytes**；`POST /simulations` 必须同时带 `"language":"FASTEXPR"` 与 `settings.instrumentType:"EQUITY"`（缺任一 400）；`brain_client._request()` 返回 httpx `Response`（要 `.status_code` + `.json()`）。
- **`Retry-After` 可能是浮点串 `"1.0"`**，`int()` 需 `float()` 包装。
- **SSL 断连（SSLEOFError）会导致误报"仍 UNSUBMITTED"**，须单独复核 status；MCP venv 的 requests 偶发 SSLEOFError 重试即可，不是凭据问题。
- **DELETE datasets 前必须查 waves / expressions / backtest_results 三处引用**（45 个 `recovered_ds_*` 占位被 98 wave / 1,926 expressions / 214 backtest_results 引用）。
- **权限/清理**：PowerShell `Add-Type`/COM 回收站方案被沙箱拦截 → 用 Python `send2trash`。
- **备份一律放 `attic/`**（skills 树内 `.bak_*` 会被 sync 忽略又被 integrity 测试扫到）。
- **bash heredoc 写含反斜杠正则时 `\b` 会被吞成控制字符 0x08** → 用 `chr(92)` 拼接。
- **`grep -v "^\["` 会误滤掉以 `[` 开头的轮询行**。
- **勿在 win 上用 `os.uname`**（需 hasattr 守卫）。
- **权威计数必须用前缀 glob**（`^field_inspect_deu_`），否则 `grep -ci "_deu_"` 会匹配旧产物（把 DEU 体检包误报成 29/30，实际 inspect=0 / coverage=1）。
- **文档与代码谁先动，另一侧必须同批跟改**（09-11 教训：给 ra-pipeline 补了"步 5 不在 MCP"，半天后新增节点又改成"有节点" → 自己制造漂移）。
- **S6→S2 闭环必须手动闭合**：回写后**必须**重跑 `workflow_campaign(stage=S2, subcommand=assemble-priors)` 刷 `priors_snapshot_<region>`，否则 GEM 读 8 天前先验（GBR 实测快照 09-19 vs KB 源 09-25）。
