# wqb_db_mcp.py 拆分：尝试、回滚与可直接执行的移交件（2026-10-04）

> 定位：P2-2 的复盘 + 下一次执行的说明书。结论与数字均为实测，非估算。
> 台账条目见 [`AGENTS.md` §8.4 第 9 项](../AGENTS.md)；工具面凭据工具 = `tools/code-audit/mcp_surface_diff.py`。

## 一、结论

**拆分本身是成功的，失败全部来自耦合面。** 现场已回滚到拆分前状态（`wqb_db_mcp.py` 2792 行，
MD5 与备份 `attic/db_mcp_pre_split_20261004/wqb_db_mcp.py.with_hook.bak` 一致）。

拆分的产物当时达到：入口 2792 → **91 行门面** + `src/wqb/db_mcp/` 8 个模块（context /
queries_waves / queries_ledger / queries_fields / mutations / step_events / workflow_bridge
+ `__init__.py`），且**MCP 工具面逐项一致**：

```
tools = 47 → 47    丢失=无  新增=无  docstring 变化=无  inputSchema 变化=无
```

## 二、四类耦合（按危险度排序，这决定了执行顺序）

> 2026-10-04 第 2 次尝试后更正：实际是**四类**，不是三类。本节是新版本；
> 每一次“再推一下”都多暴露一类，这本身就是“不能当作 Tonight 任务”的根据。

| 类 | 实测规模 | 失败形态 | 当前状态 |
|---|---|---|---|
| **① 测试隔离靠属性 patch** | **17 处 / 16 个测试文件** | **静默写生产库**（不报错） | ✅ **已消灭**：`set_db_path()/get_db_path()` + 结果层硬闸 |
| **② 断言直接读根文件源码文本/路径** | **28 文件 66 处**引用入口，**26 条断言**变红 | 响亮失败 | ❌ 待改，清单见第四节 |
| **③ 测试 patch 入口的内部符号** | **6 处**：`mod._conn`、`mod._get_ledger_raw`×5 | **最阴险**：若门面转发了同名对象，patch 打不到实现 → **测试空过（假绿）** | ❌ 待改；**防护已设计好：门面不得导出 `_*` 私有名**，让旧写法 AttributeError 响亮报出 |
| ④ 工具清单发现链 | 至少 **4 个守护**靠解析入口源码来枚举 47 个工具（`skill_lint`、`test_se_docs`、`test_skill_integrity`、`test_docs_consistency`） | 拆完它们看到 **0 个工具** → 报“17 个工具未注册”“INDEX 计数不符装饰器实数 0” | ❌ 待改（可收敛：若发现器共用一个入口清单常量，改一处即修多条） |
| ⑤ 连接白名单 | `db_conn.DIRECT_CONNECT_WHITELIST` 1 条 | 响亮失败 | ✅ 已验：`wqb_db_mcp.py` → `src/wqb/db_mcp/context.py` |
| ⑥ 常量访问 | `getattr(mod, "HARVEST_SOURCE")`、`_normalize_wave_verdict` 等 | 响亮 AttributeError | ❌ 待做：门面需导出**公开常量**（但**不得**导出 `_*` 私有函数，见③） |

①是唯一致命的数据风险（已消除）。③是第二危险类（假绿 = 守护失效但看起来在守）。②④⑥ 只会响亮地红。

### 拆分后的实测数据（两次尝试均相吻）

```
入口 2792 行 → 91 行门面 + src/wqb/db_mcp/{context,queries_waves,queries_ledger,
  queries_fields,mutations,step_events,workflow_bridge} + __init__.py
MCP 工具面：47 → 47，丢失=无 新增=无 docstring 变化=无 inputSchema 变化=无  ✅
全量测试：3059 收集里 **26 条因拆分红**（均为②③④⑥，无静默写库）
```

## 三、拆分配方（已验证可复现）

生成器逻辑（下一次照抄即可，无需重新设计）：

1. AST 取全部顶层函数（含装饰器行范围）与顶层常量。
2. 分组：`context`（共享状态 + 8 个工具函数）/ `queries_waves` / `queries_ledger` /
   `queries_fields` / `mutations` / `step_events` / `workflow_bridge`。
   ⚠ **写路径 + 收割 + 轮转 + 判死 + 相关性必须合成一个 `mutations` 模块**：`--plan` 的
   组间 DAG 检测出 `mutations ↔ harvest`、`rotation ↔ mutations` 互引成环，拆开就是包内
   循环 import（服务启动即挂）。**环检测必须作为写盘前的硬门**，不能靠人眼看。
3. 函数体逐字节搬运；唯一的等价替换是 `str(DB_PATH)` → `get_db_path()`。
4. 顶层常量按"被哪个组用"自动归位；多组用 → `context`。
5. 子模块 blanket import 原文件的 import 段（宁多勿漏），跨组符号显式 `from .<组> import`。

### 三个必须遵守的约束（每个都是踩过之后写下来的）

- **不要把 `DB_PATH` 放进子模块的 import 表**：按值导入等于抄一次陈值，`set_db_path()` 之后
  子模块仍读旧路径 —— 与①同类的静默错位。宁可让误读者 `NameError` 响亮报出。
- **门面必须用 PEP 562 `__getattr__` 实时委托 `DB_PATH`**，不要 `from .context import DB_PATH`：
  有测试是"`set_db_path()` 之后再读 `mcp.DB_PATH`"来校验写入目标的。
- **`_GuardedModule` 的 `__class__` 交换只能条件安装**（`sys.modules.get(__name__)`）：测试用
  `spec_from_file_location` 载入且不注册进 `sys.modules`，写 `sys.modules[__name__]` 会 KeyError。

## 四、下一次要改的清单（按文件归组；含实测行号）

| 文件 | 要改什么 |
|---|---|
| `src/wqb/db_conn.py:36` | ✅已验：`DIRECT_CONNECT_WHITELIST` 的 `wqb_db_mcp.py` → `src/wqb/db_mcp/context.py` |
| `wqb_db_mcp.py`（门面） | 需补导出**公开常量**（`HARVEST_SOURCE`、`_GATE_DECISIONS`…按实际 getattr 决定）；**不得导出 `_*` 私有函数** |
| `tests/unit/08_forum_recon/test_dead_end_forum_gate.py:193,213,229,249,269` | ③类：`monkeypatch.setattr(mod, "_get_ledger_raw", …)` → 改 patch `wqb.db_mcp.mutations._get_ledger_raw`（被调用处，patch context 无效） |
| `tests/unit/02_workflow/test_mining_efficiency_guards.py:154,155` | ③类：`db_mcp._conn` / `db_mcp._get_ledger_raw` 同上 |
| `tests/unit/07_docs_skills/test_skill_integrity.py:121` | ④类：工具注册表发现链（现报 17 个 wqb-db 工具未注册） |
| `tests/unit/07_docs_skills/test_se_docs.py:75,550,1063` | ④类：“wqb-db 没有工具 get_mining_yield”、`KeyError: 'upsert_expressions'`、L608-610 是另一个模块（无需改） |
| `tests/unit/07_docs_skills/test_skill_lint.py:127,218` | ④类：`KeyError: 'get_region_config'`（从入口 AST 收集签名）+ baseline 不再陈旧 |
| `tests/unit/07_docs_skills/test_docs_consistency.py:546,548` | ④类：“INDEX 基准段 wqb-db 计数与装饰器实数 0 不符” |
| `tests/unit/01_store_db/test_ledger_key_catalog.py:79` | ②类：`"wqb_db_mcp.py" in keys["region_rotation"]["write"]` → `src/wqb/db_mcp/mutations.py` |
| `docs/ledger_keys.json` | ②类：4 处 owner/ref 写着 `wqb_db_mcp.py` |
| `tests/unit/06_wave_pipeline/test_wave_verdict_enum.py:105-111` | ②类：改扫 `src/wqb/db_mcp/*.py`（**断言强度不变**：仍是“不得有第二权威”） |
| `tests/unit/03_gem/test_gem_provenance_p1p2p3.py:392,395,439,442` | ②类：L444 `IndexError`（解析入口拿 upsert 签名） |
| `tests/unit/01_store_db/test_n30_wave_results_writers.py:63,64` | ⑥类：`getattr(mod, "HARVEST_SOURCE")` |
| `tests/unit/06_wave_pipeline/test_wiring_fixes_20260915.py:9,292,295` | ②类：`test_normalize_wave_verdict_rules` |
| `tests/unit/09_core/test_index_tables.py` | ②类：跑 `python tools/index_tables.py --apply`（入口变动会改生成表） |

> ③类为何必须按“被调用处”patch：`from .context import _conn` 是**按名绑定**，
> 所以 patch `context._conn` 影响不到 `mutations._conn`。这也是建议门面**不导出私有名**的原因：
> 导出就会把“响亮报错”变成“空过”。

## 五、执行顺序（照做即可，每步都可回滚）

```powershell
# 0) 先确认基线绿（当前有若干并行会话造成的红，先记下别混进来）
python -m pytest tests/ -q --tb=no

# 1) 工具面基线
python tools/code-audit/mcp_surface_diff.py --tag before

# 2) 备份入口（git 之外的硬备份，因为它有未提交改动）
Copy-Item wqb_db_mcp.py 'attic\db_mcp_pre_split_<YYYYMMDD>\wqb_db_mcp.py.bak'

# 3) 按第三节配方生成 src/wqb/db_mcp/ + 门面，跑工具面比对（必须 47=47）
python tools/code-audit/mcp_surface_diff.py --tag after

# 4) 先改 ③（1 行），再按第四节把 ② 的 26 条逐个改到"新路径/新扫描范围"，
#    注意：是改断言的**目标位置**，不是放宽断言强度
python tools/index_tables.py --apply

# 5) 全量 + 守护 + MCP 包
python -m pytest tests/ -q --tb=short
python tools/audit_structure.py
Push-Location world-quant-brain-mcp; .venv\Scripts\python.exe -m pytest tests/ -q; Pop-Location

# 6) 回归不过就整块回滚（门面 + 包目录一起撤，别留半迁移状态）
```

## 六、本次附带产生的数据污染（已闭环，留此备考）

拆分配方试跑期间，①类缺陷暴露无遗：失败的那次全量运行把测试数据写进了生产 `data/wqb.db`。

| 表 | 行 | 处置 |
|---|---|---|
| `registry_empirical` | 2（`KOR-GATE-DEAD`、`KOR-LEGACY-DEAD`） | 双条件 DELETE（id + `created_at LIKE '2026-10-04%'`） |
| `wave_results` | 9（本轮新建且 `candidates/batches/full_payload` 全 NULL） | DELETE（"真实波次必有候选与批次"是删除前置条件） |
| `wave_results` | 3（KOR 11/12/97，2026-09-01 创建的真行被覆盖） | **未编造 verdict**：剔掉泄漏的测试夹具项（KOR/12 的 `"a","b"`）+ 追加 `data_caveat` |
| `ledger_kv` | 5 | 同窗核对，未删 |

备份：`data/wqb.db.bak_pre_p22_cleanup_20261004`（311 MB，sqlite 在线备份 API）；
另有 10-02 的 308 MB 备份为第二恢复路径。复查谓词：
`SELECT … WHERE updated_at LIKE '2026-10-04T03:33%' AND created_at = updated_at AND candidates IS NULL …`

**同期不属于本次的写入**（已逐条归属，避免误账）：非枚举 verdict
`KOR/s2_oth466_d33 = MIXED_NO_SUBMIT`、`tools/tmp_eur_*.py` 的裸 sqlite 与未登记 ledger 键、
`tools/_kor_d33_writeback.py`、`tools/_tmp_anl69_fields.py` 的盘符路径 —— 均来自并行会话。

## 七、下一步建议

1. ②③类共 26 条，改动机械且**失败可见**，适合单独一轮做完（预计一次会话内可闭环）。
2. 不要在同一次改动里既拆文件又做别的结构性移动 —— ②类断言的定位依赖"只有拆分动了"。
3. `wqb_db_mcp.py` 拆完后，§8.13 的 `tools/` 主题下沉可复用同一套配方
   （生成器 + DAG 硬门 + 逐条归属 + 可回滚提交切分）。
