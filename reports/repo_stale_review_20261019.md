# 仓库过时面审查与治理建议（2026-10-19）

> 本次审查的**扫描面 = 受跟踪文件（4361 件）+ 现有治理闸的输出**，不把 `.venv` / `cache` /
> `research-data` 等 ignored 产物当源码（但它们会污染全仓扫描，见 §6）。
> 证据命令全部可复跑，见 §7。

---

## 0. 一句话结论

**代码本身很干净**（业务代码里 TODO/FIXME 只有 6 处，依赖方向、硬编码路径、根目录散件全绿），
**债全在"产物面"**：532 件抢救点未裁决、23 件源码未入库、5 个 tools 顶层脚本违反冻结闸、
362 份历史报告与 2185 个数据湖 JSON 躺在 git 里。
建议按「先止血（P0）→ 再清债（P1）→ 最后还技术债（P2）」三段推进，
**重点是给"扫描面"和"产物归属"定死口径，否则每轮治理都会长回来**。

---

## 1. 规模与分布（受跟踪 4361 件）

| 目录 | 件数 | 占比 | 磁盘 | 定性 |
|---|---:|---:|---:|---|
| `tracking/` | 2687 | 61.6% | 103M | 区域数据湖（含 2185 个 JSON dump） |
| `Claude/skills` | 524 | 12.0% | — | 技能资产（权威面） |
| `tools/` | 231 | 5.3% | — | CLI |
| `tests/` | 224 | 5.1% | — | 守护 |
| `output_report/` | 222 | 5.1% | 3.7M | 战役/评审**产物** |
| `reports/` | 140 | 3.2% | 3.7M | 人工审计/复盘**报告** |
| `src/wqb` | 121 | 2.8% | — | 代码 |
| `docs/` | 97 | 2.2% | — | 长期规范 |
| `world-quant-brain-mcp` | 61 | 1.4% | — | MCP 服务 |
| `attic/` | 41 | 0.9% | 12M | 归档区（29 个包，多数 ignored） |

`.git` = **92M**；另有 ignored 但占盘的 `world-quant-brain-mcp/.venv` **743M**、`cache/` **311M**、
`research-data/` 40M、`logs/` 13M。

---

## 2. P0 · 违反现行闸，本周必清

### 2.1 `tools/` 顶层 5 个脚本（S11 FAIL ×2 + S14 FAIL ×1）

```
tools/direct_submit_akVnvzX5.py   tools/direct_submit_leM0mwVA.py
tools/direct_submit_omoK1A5m.py   tools/nemesis_prescreen.py   tools/prod_watch.py
```

- 三件 `direct_submit_<alphaid>.py` **明文绕过本地「稳健性审计未确认」闸**（脚本 docstring 自陈）。
  同名的 `tools/direct_submit.py` 早在 2026-10-06 就被裁决 **DROPPED** 并登记进
  `audit_structure_baseline.json` 的 `retired_paths`（S12 拦复活）——**这三件是同类的复活形态**。
- 用户政策是「只挖不提交」；这类脚本即便有当次显式授权，留在工作区顶层就是**下一条误提的引信**。

**建议**：① 立即移出 `tools/`（迁 `attic/direct_submit_20261019/` 或 `tracking/USA/scripts/archive/`）；
② 若确需复用作模板，改写成**不带 alpha id 的通用器**并走 MCP `workflow_submit_alpha`；
③ `nemesis_prescreen.py` / `prod_watch.py` 补 `tools/THEMES.json` 归属 + `tools/README.md` 登记，
或迁进主题子目录（现行规则禁止默认塞进已有目录）。

### 2.2 23 件未跟踪源码（下次 `git clean -fd` 即失）

构成：3 件 direct_submit、9 件今日新增的 USA/EUR/KOR 参考文档
（`_usa-*-20261019.md`、`docs/reference/*20261019.md`）、`tests/unit/09_core/test_nemesis_prescreen.py`、
`output_report/SA_best_per_region_plan_20261019.md`、`reports/robustness_20261019.md`、
5 件 `tracking/KOR/reference/datasets/*.md`。

**建议**：按"是不是结论"二分——9 份字段画像/扫描文档与 KOR 数据集 md 是**结论资产**，当批入库；
`test_nemesis_prescreen.py` 若工具不入库则测试也不该入库（否则 CI 红）；
两份 20261019 报告按 §1  taxonomy 入库（命名已合规）。
**不要让"未跟踪"成为一种存放状态**——`repo_governance_check` 每天报的就是这个数。

### 2.3 `docs/reference/field-profile-ind-inst-fund-20261019.md` 命名违规（S16 在途 WARN）

`git add` 后即转 FAIL。改成 `field_profile_ind_inst_fund_20261019.md`（下划线、已带日期）。

---

## 3. P1 · 结构性债（本月）

### 3.1 抢救点 887 件独有 / 532 件 PENDING —— 全仓最大一笔债

按目录分布：**tracking 242 · tests 180 · output_report 27 · tools 24 · Claude 22 · reports 18 ·
docs 14 · mcp 5**。已裁决 355 件，剩 532 件无人看过。

其中 **538 件的 blob 在 main 里根本没有对应件**（不是"换了位置"，是真分叉或真删除），
所以**无法机械判定**，只能逐件读。但可以先做两轮"机械降载"：

1. **目录级 ARTIFACT**：`tracking/mining/`、`tracking/prod_probe/`、`tracking/_scratch/`、`tracking/PPA_USA/`
   下的 JSON dump，以及 `tracking/*/runs/*.txt` 派发记录 —— 现行 `ARTIFACT_DIR_RULES` 已经这么判了，
   只是没写进 fixture。**加一批目录级 override，可一次性消掉大部分 tracking 的 242 件**。
2. **测试件比对**：180 件 tests 里，凡 main 有同名且**新版本覆盖同断言**的，判 DROPPED 并写明
   "由 `tests/…::<新测试>` 覆盖"；只有"断言被删了"的才需要真的读一遍决定要不要回迁。

做完这两轮，需要人读的应能压到 **100 件以内**，那时再逐件裁决才现实。

### 3.2 `tracking/` 的 2185 个 JSON 与"数据湖=运行产物"自相矛盾

`snapshot_adjudicate` 把 `tracking/mining/` 判为 **ARTIFACT（可重跑）**，但它同时在 git 里躺着（103M）。
**"可重跑"和"入库"是互斥的定性**——可重跑的东西不该占版本库。

**建议**：给 `tracking/` 立一条硬口径——`config/`、`reference/`（结论面）、`cells.json`、`settings.json`、
`thresholds.json` 入库；`mining/`、`prod_probe/`、`runs/`、各类 `*_fields.json` / `field_inspect_*`
**移出 git**（gitignore + 保留生成脚本 + 在 `tracking/README.md` 写"重跑命令"）。
预计可减掉一半以上的 tracking 体积，并让 S18 的"索引面"读数降一个量级。

### 3.3 362 份历史报告（output_report 222 + reports 140）

最早的 `20260805`、9 月约 100 件、10 月约 90 件。抽样查引用的结果**不支持整批归档**：

| 报告 | 活文档引用数 |
|---|---:|
| `db_concurrent_write_lock_audit_20260920.md` | 8 |
| `alpha_properties_audit_20260920.md` | 3 |
| `code_structure_survey_20260925.md` | 2 |
| `decommission_cause_analysis_20260920.md` | 0 |
| `d9_status_backfill_rollback_20260928.json` | 0 |

**建议**：先跑一次"引用扫描"，把 **0 引用且 ≥30 天**的迁 `attic/reports_pre202610_<日期>/`
（保留索引 README 说明"从哪来、为什么留"），有引用的原地不动。
同时给 `output_report/` 定一个**保留窗口**（如 90 天），超窗自动进 attic —— 现在 186→222 件还在涨。

### 3.4 跨 skill 复制 4 组（S6 WARN）

- `helpful_functions.py` ×3（feature-implementation / inspect-raw / GEM 内嵌）—— **3 份内容全同**，
  却分散在三个 skill：`validator.py` 已有"单一来源 + 四处一起改"的纪律，`helpful_functions.py` 没有。
- `ace_lib.py` ×2、`diversity_enhancer.py` ×2、`validator.py` ×4（含 2 份 GEM 内嵌，设计内）。

**建议**：`helpful_functions.py` 与 `diversity_enhancer.py` 补进 `sync_gem_embedded_skill.py` 式的
同步器（或至少加一条"逐字节镜像"的 pytest，抄 `test_validator_copies_are_byte_identical...` 的写法）；
`ace_lib` / `load_credentials` / `skill_roots` 三组属**有意分叉**（DIVERGED_ALLOWLIST 已登记），保持现状但要在
allowlist 里把"为什么各自演化"写全，避免后人当成 drift 去合并。

---

## 4. P2 · 技术债（排期做，不阻塞）

| 项 | 现状 | 建议 |
|---|---|---|
| S1 sys.path 自举 | **183 处**（tools 脚本直跑需要） | 收敛成一个 `tools/_bootstrap.py` 或 pyproject console_scripts；新增脚本禁止再写第三行 `sys.path.insert` |
| S16 命名存量违规 | 40 条（基线内 WARN） | 维持"触碰即改"棘轮；本次顺手清掉 `output_report/IND_*_ideas_v2.md` 那一批（同模板，一次改完） |
| 死代码 | 3 个高置信零引用：`_is_embedded`(audit_skill_drift)、`_pyra`(sync_platform_alphas)、`_sub_args`(probe/category_probe) | 删掉；`_pyra` 若是为将来留的钩子就补注释说明 |
| `attic/` 41 件仍受跟踪 | 6 个包被 `attic/*` + `!` 豁免 | 归档区定位是"不删只归"，但**实体不必进 git**：留索引 README，实体从索引移除（`git rm --cached`） |
| 超长函数 | `reports/…/run_realenv.py::_main_body` 786 行 / cc 377、`tools/wave_gate.py::main` 736 行 / cc 249、`build_wave.py::main` 727 / cc 308 | 这三个是全仓最难的维护点；`wave_gate.py` 与 `build_wave.py` 还在活跃使用，建议拆 `main` 的参数解析与调度 |

---

## 5. 代码健康度（这部分是好的，别误伤）

- 业务代码里 `TODO/FIXME/HACK` **只有 6 处**（src 2 / tools 3 / tests 1），且都写了原因
  （如 `step_metrics_collector.collect_from_checkpoint()` 是 TODO 空壳——**这个值得单独记一条债**：
  唯一自动采集入口恒返回空 dict，step_funnel 至今无自动数据源）。
- 全绿项：S2 依赖方向（src 不引用 tools）、S4 无本机绝对路径、S7 根目录无散件、
  S9 声明目录存在、S10 13 个区域目录齐整、S12 无已下架路径复活、S13 非区域目录已登记、
  S17 顶层 16 目录全部声明、S20/21 索引一致且无裸扩展名件。
- pytest 3425 passed / 22 skipped（0 红）。

---

## 6. 扫描卫生（这套不改，下次审查还会被脏数据带偏）

1. **`.venv` 743M 在仓库内**（已 ignore，但污染每一次全仓 grep）：本次统计 `TODO` 命中 3969 处，
   其中 **3963 处来自 `world-quant-brain-mcp/.venv/Lib/site-packages`**（sklearn / statsmodels）。
   建议把 `.venv` 迁出仓库（或用 pyproject 声明解释器），并给所有审计脚本加
   `.venv|node_modules|cache/|research-data/` 排除。
2. **统一扫描面 = `git ls-files`**：`audit_dead_code` / `audit_file_sizes` / `doc_path_refs`
   若以文件系统为输入，会把 ignored 产物当源码。改成以索引为输入，读数立刻可信。
3. `audit_file_sizes.py` 当前在 `main()` 里 **KeyError: 'max_cc'** 直接崩（Top-15 那段）→ 顺手修掉，
   否则这个工具等于没有。
4. 6 个安装位镜像（`.claude/.codex/.cline/.agents/.cursor/.workbuddy` 下共 1891 个被 ignore 的源码件）
   是设计内的（`sync_skills.py`），但 `repo_governance_check` 会把它们列进"被 gitignore 排除的源码类文件"
   的告警里，每次都刷屏 —— 建议按 `S15` 的结论（`.claude/skills` 是联接同址）直接豁免安装位。

---

## 7. 证据命令（可复跑）

```bash
python tools/audit_structure.py                        # FAIL=3 WARN=4
python tools/code-audit/repo_governance_check.py       # 未跟踪源码 23 + 抢救点独有 887
python tools/code-audit/snapshot_adjudicate.py --json  # PENDING 532
python tools/audit_dead_code.py                        # 死代码 3
python tools/audit_skill_drift.py                      # 跨 skill 复制 4 组
python tools/audit_file_sizes.py                       # 超长函数（当前报错，见 §6.3）
git ls-files | wc -l && du -sh .git                    # 4361 件 / 92M
```

---

## 8. 建议的执行顺序（每步都可独立验证）

| # | 动作 | 预期收益 | 风险 |
|---|---|---|---|
| 1 | 5 个 tools 顶层脚本归位/归档 | S11/S14 由 FAIL 转 OK | 低（direct_submit 有授权记录，归档不删） |
| 2 | 23 件未跟踪源码二分入库 | 「git clean 即失」风险归零 | 低 |
| 3 | PENDING 目录级降载（tracking dump + tests 覆盖比对） | 532 → ~100 | 中（需逐批核对后再写 fixture） |
| 4 | `tracking/` dump 移出 git | 仓库体积减半、S18 读数降量级 | 中（须先确认脚本能重跑） |
| 5 | 0 引用且 ≥30 天的报告进 attic | 报告面消肿 | 低（先跑引用扫描） |
| 6 | helpful_functions / diversity_enhancer 单一来源 | 消除 3 份全同副本 | 低 |
| 7 | sys.path 收敛 + audit_file_sizes 修崩 + 扫描面改 git ls-files | 工具有效性恢复 | 低 |
