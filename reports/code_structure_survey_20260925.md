# wqb 代码结构梳理与清理/优化方案

> 生成日期：2026-09-25
> 方法：机器级全库遍历 + token 级引用计数（`logs/_tmp_refscan.py`）+ 子串兜底核验（`logs/_tmp_refscan_verify.py`）
> + 内容哈希去重。所有结论均二次验证，避免子串匹配高估引用。

---

## 0. 结论先行

| 维度 | 结论 |
|---|---|
| **可回收磁盘** | 本轮已回收 **≈ 1.29 GB**（`data/` 1.15G 陈旧 DB 备份 + `logs/` 0.19G 过期 pytest basetemp） |
| **已归档死代码** | 4 个受控模块 `git mv` 进 `tools/legacy/`；2 个从未入库的草稿进回收站 |
| **真·零引用 CLI 工具** | **15 个**——它们不是死代码，是「有 `__main__` 但 README 未登记」的孤儿工具，**不宜删** |
| **最严重结构债** | ① `tools/README.md` 只覆盖 44/115 工具；② `tools/` 下 2 个 `test_*.py` **从不执行**；③ `data/`、`logs/` 无保留策略，5 天回涨至 1.6G |
| **不可逆风险** | 无。磁盘操作全部走回收站；代码操作全部 `git mv`，历史可追 |

---

## 1. 仓库分层地图（清理后口径）

| 层 | 路径 | 体积 | 入库 | 规模 |
|---|---|---:|---|---|
| 核心库 | `src/wqb/` | 3.1M | ✅ | 86 个 .py / **24,912 LOC**；9 个子包（workflow/nodes 20、store 14、expression 10、research 8、modeb 5、memory 5、search 3…） |
| 工具层 | `tools/`（顶层） | 3.6M | ✅ | **115** 个 .py |
| 归档区 | `tools/legacy/` | — | ✅ | 本轮后 **18** 个（A 段 13 + B 段 1 + C 段 4） |
| 测试 | `tests/` | 3.4M | ✅ | 83 个 test 文件 / 15,349 LOC |
| Skills | `Claude/skills/` | 6.2M | ✅ | 34 个一级 skill + 2 个嵌套副本 |
| MCP 前端 | `world-quant-brain-mcp/` | **772M**（`.venv` 751M） | ✅ | 30 个顶层 .py |
| MCP 后端 | `wqb_db_mcp.py`（根） | — | ✅ | 单文件 **2,297 行** |
| 数据湖 | `tracking/` | 74M | ✅ | **2,382** 个受控文件；`tracking/mining/` 占 36M（共享湖，勿动） |
| 产出文档 | `output_report/` + `reports/` | 2.0M | ✅ | 86 + 23 个受控文件 |
| 运行时（忽略） | `data/` 472M、`logs/` 46M、`research-data/` 43M、`cache/` 2.9M、`extensions/` 2.2M、`results/` 184K、`attic/` 116K | 566M | ❌ | 全部 gitignored |

> **体积对比**：本次清理前 `data/`=1.4G、`logs/`=211M（合计 1.6G）→ 现 `data/` 472M / `logs/` 46M。
> ⚠️ 报告的 5 轮验证改动用到的 `logs/_pytest_*` basetemp（约 80M）**已于同日回收**。

**三段口径**：`data/` 1.4G → 477M；`logs/` 211M → 30M（其中保留 `logs/_async_tasks` 14M
等并发会话的运行时状态目录）。合计回收 ≈ **1.25 GB**。

---

## 2. 本轮已执行

### Tier 0-A — `data/` 陈旧 DB 备份（回收 1.15 GB）

沿用上一轮既定保留政策：**保留 live `wqb.db` + 最新一份完整备份**，其余进回收站。

| 文件 | 大小 | 日期 |
|---|---:|---|
| `data/wqb.db.bak_ghost_20260923_171212` | 227M | 09-23 |
| `data/wqb.db.bak_prewhitelist_20260923_134122` | 227M | 09-23 |
| `data/wqb.db.bak_ready2_20260923_171432` | 227M | 09-23 |
| `data/wqb_backup_prodcorr_20260923_192610.db` | 232M | 09-23 |
| `data/wqb.db.bak_prewhitelist_20260924_203425` | 235M | 09-24 |

**保留**：`data/wqb.db`（live，228M）、`data/wqb.db.bak_20260924_submit`（最新，238M）。

### Tier 0-B — `logs/` 过期 pytest basetemp（回收 0.19 GB）

18 个 09-24 留下的 pytest basetemp / transcript 目录（每个内含数百个 `test_xxx0/` 子目录）。
**保留**：`logs/_async_tasks`（工作流异步任务状态）、`logs/_dblock` + `logs/_slots`（L1 写锁运行时状态）——三者由并发会话的 MCP 进程持续读写，删除会破坏在跑流水线。

### Tier 1 — 纯死代码归档

新增判据 **D**（写入 `tools/legacy/README.md`）：`refs=0` **且** 无 `__main__` 入口 **且** mtime ≥ 7 天。

| 文件 | 原位置 | LOC | 处置 |
|---|---|---:|---|
| `death_level.py` | `src/wqb/` | 89 | `git mv` → `tools/legacy/` |
| `calibrate_q3_alphas.py` | `tools/` | 116 | `git mv` → `tools/legacy/` |
| `corr_batch_head_candidates.py` | `tools/` | 98 | `git mv` → `tools/legacy/` |
| `n1qmj_decorrelate_variants.py` | `tools/` | 143 | `git mv` → `tools/legacy/` |
| `_align_batch_verdict.py` | `tools/`（untracked） | 31 | 回收站（从未入库，进 git 无意义） |
| `_pyramid_map.py` | `tools/`（untracked） | 161 | 回收站（同上） |

**为什么只有 6 个而不是 22 个** —— 关键教训：

> 「refs=0」≠ 死代码。`tools/*.py` 绝大多数是**命令行工具**，天然不会被任何模块 import。
> 只有**同时缺 `__main__` 入口**才算真死代码。

由此排除了 15 个 CLI 孤儿工具（下表）与 1 个并发会话在飞文件（`triage_platform_status_sweep_v3.py`，09-24 22:36 仍在写）。

---

## 3. Tier 2 — 优化方案（待确认落地）

### P1 ★★★ `tools/` 文档覆盖率仅 38%（115 个工具，README 只登记 44 个）

`tools/README.md` + `README_OPTIMIZATION.md` 合计覆盖 44 个，**71 个未登记**，其中包含高频关键工具：

`step_funnel.py`、`sync_skills.py`、`field_profile_backfill.py`、`validate_fields_batch.py`、
`preflight_wave.py`、`s2_field_validator.py`、`prod_saturation_gate.py`、`select_ra_basket.py`、
`webdata_quality.py`（859 LOC）、`field_quality_scorer_v2.py`（755 LOC）…

**建议**：给 `tools/README.md` 加「按类别索引」章节；新工具合入时要求同步登记（可做成 `tools/check_tools_readme.py` 并挂进测试）。

### P2 ★★★ 僵尸测试：`tools/` 下 2 个 `test_*.py` 从不执行

`pytest.ini` 的 `testpaths = tests world-quant-brain-mcp/tests`，**不含 `tools/`**，因此：

| 文件 | LOC | 状态 |
|---|---:|---|
| `tools/test_field_catalog_cache.py` | 221 | 从未被 pytest 收集 |
| `tools/test_gbr_batch_isolation.py` | 314 | 同上 |

**建议**：迁入 `tests/unit/`（若内容仍有效），或迁到 `tools/legacy/`（若已失效）。二选一，不留夹生状态。

### P3 ★★★ `data/`、`logs/` 缺保留策略

本轮清理距上一轮仅 5 天，`data/` 从 390M 回涨到 1.4G、`logs/` 涨到 211M。

**建议**：新增 `tools/retention.py`（dry-run 默认），策略为「`data/*.bak` 仅留最新 1 份 + 7 天以上进回收站；`logs/_pytest_*` 保留最近 3 份」。挂 cron / 每周手动跑一次。

### P4 ★★ 四工具的默认 `--zip` 指向不存在的文件

`tools/gen_field_inspect_packs.py:36`、`webdata_quality.py`、`neut_cache.py`、`s0_enhanced_screening.py`
默认均指向 `research-data/WebData_20260219_V0.10.9.zip`，但磁盘上**只有解压后的目录**
`research-data/WebData_20260219_V0.10.9/`（36M），**没有任何 `.zip`**，且这些工具只做
`zipfile.ZipFile(zip_path)`，无目录兜底 → 默认路径必然 fail。

**建议**（二选一）：① 把该目录重新打成 zip 放回原位；② 给 4 个工具加目录兜底并把
`DEFAULT_ZIP` 改成存在的路径。这也是 `.workbuddy/memory` 里反复出现「体检包本地不可达」的根因。

### P5 ★★ WebDataScope 插件源码两份冗余（2.2M）

`research-data/WebDataScope-1.5.0/` 的 102 个文件与 `extensions/webdatascope/` **逐字节相同**
（`diff -rq` 唯一差异是后者多一个 `workflows/`）。两者均未被任何 `.py` 按路径引用（是人类手动装载到浏览器的扩展包）。

**建议**：确认 `extensions/webdatascope` 为在用副本后，回收 `research-data/WebDataScope-1.5.0/`。本轮**未动**——浏览器已加载的扩展源风险由用户确认。

### P6 ★★ `info_data.bin` 两份完全相同（14.8M ×2）

`world-quant-brain-mcp/config/info_data.bin` 与 `research-data/WebData_20260219_V0.10.9/data/oth/info_data.bin`
MD5 一致。前者由 `brain_mixin_transport.py:105` 读取（缺失时优雅降级）；后者是离线数据包副本。

**建议**：保留前者，后者随 P5 一并处理。

### P7 ★★ Skill 嵌套副本

`Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-feature-implementation/`
是一级 `Claude/skills/brain-feature-implementation/` 的副本：`scripts/` 下 5 个文件完全相同
（`validator.py` 70K、`ace_lib.py` 55K…），仅 SKILL.md 不同。同类还有
`brain-inspect-raw-template-create-setting/ace_lib.py` == `brain-sim-alphas-in-batch-and-track/scripts/ace_lib.py`（55K）。

**建议**：改为在 SKILL.md 里用相对路径引用一级 skill，删除嵌套副本；否则改脚本时两边必漂。

### P8 ★★ 全套件在本地全跑是 flaky 的（非回归，需知道）

**现象**：`pytest tests/ -q` 全量结果不稳定（1411✓ / 1377✓+34✗ / 1378✓+33✗ 三次数值各异）；
但把失败文件单独跑**全绿**（`test_build_wave_selection.py` 22/22、`test_slots_arbitration.py` 2/2）。

**根因**（两条并存）：
1. `logs/_slots`、`logs/_dblock`、`logs/_async_tasks` 是**进程级共享状态**，运行中的 MCP 服务与 pytest 争用；
2. 本执行环境的批量删除守卫（`[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED]`）会在跑批后
   截获子进程删除操作，把守卫文本混进 subprocess stdout，破坏 `assert 'xxx' in out` 型断言。

**建议**：给 `dblock`/`slots`/`async_tasks` 的测试加 `tmp_path` 隔离（目前至少有部分直接写仓库级 `logs/`）；
别把全套件的偶发红当成回归——先看单文件是否绿。

### P9 ★ `src/wqb` 未打包（已决策维持现状）

`pyproject.toml` `py-modules = []` + `tests/conftest.py` 的 `sys.path.insert` 是既有机制，非权宜；改动面大、收益低。维持。

### P10 ★ 根级临时产物与废弃宿主目录

- `findings.md` / `progress.md` / `task_plan.md`（planning-with-files 产物）+ `alpha模板.docx` —— 均 gitignored；建议归档进 `attic/`。
- `.box-agent/`、`.box-agent-scratch/`、`.kimi-code/` —— 已弃用 AI 宿主的残留（`.box-agent` 近期仍有 task-registry 写入，本轮**未动**）。

### P11 ★ `cache/` 内部重复

`candidates_eur.json` == `cand_EUR_20260920.json`（122K）、`candidates_gbr.json` == `cand_GBR_20260920.json`（51K）。量小（cache 共 2.9M），随 P3 一并清理即可。

---

## 4. 备忘录：引用分析的可靠做法（本轮固化）

1. **不要用子串 grep 判「零引用」**。`tools/pipeline_integration.py` 在
   `diversity_extract.py` 里被 grep 到，但命中处是 **ledger key 字符串**
   `pipeline_integration_{dataset}`，不是 import。
2. **token 级计数同样有坑**：务必把 dotted token（如 `wqb.research.selection_contract`）
   按 `.` 切分后再索引，否则会漏掉真实 import（本轮首跑就因此误判 `selection_contract.py` 为死代码）。
3. **`refs=0` 之后必须再看有无 `__main__`**，区分「库模块」与「未登记 CLI 工具」。
4. **内容哈希去重**（125 组重复）比同名/同尺寸可靠，能同时暴露 DB 备份、`.bin`、vendored JS 的冗余。
