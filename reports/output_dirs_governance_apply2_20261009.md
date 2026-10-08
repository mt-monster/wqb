# 输出目录治理 · 第二轮落地收尾（2026-10-09）

> 上游：[`output_dirs_governance_review2_20261008.md`](output_dirs_governance_review2_20261008.md)（第二轮复核，提出 A–H 共 8 项）
> 与 [`output_dirs_governance_apply_20261008.md`](output_dirs_governance_apply_20261008.md)（第一轮落地）。
> 本文只记**第二轮复核之后**又做了什么、以及**为什么有三项不做**。

## 0. 一句话结论

A / B / C / F / G 已落地并全部入闸；**D / E / H 不做**（理由与触发条件见 §4）。
当前闸门读数：`audit_structure FAIL=0 WARN=4`、`doc_path_refs BROKEN 0`、`pytest 3156 passed`。

## 1. 已落地（逐项带 commit）

| 项 | 动作 | 验证读数 | commit |
|---|---|---|---|
| **A** | `tracking/` 顶层 4 个日期带杠文件改名（`2026-10-06_robustness.md` → `robustness_20261006.md` 等）+ 同步 `DEU_category_mining_status_20261006.md` 里的引用 | `doc_path_refs BROKEN 0`；git 记为 R（保住历史） | `48eb39e` |
| **B** | `cache/eur_analyst_fields_report.md`（44 969 字节）迁出 gitignore 区 → `output_report/eur_analyst_fields_report_20261007.md` | 文件进入受控树，不再会被 `git clean` 带走 | `0e45a25` |
| **F** | 新增 **S16 报告/产物命名闸**（棘轮：新增违规 FAIL，15 条存量入基线），扫面含 `output_report` / `reports` / **`tracking/*.md` 顶层** | `FAIL=0`；`WARN` 仅报 15 条基线存量；新测试 `test_audit_structure_s16.py` **15 passed** | `48eb39e` |
| **C** | 裁决台账新增**改名识别**（blob 相等 + 归一化词干相同 ⇒ 判 `DROPPED`「改名，件未丢失」） | **PENDING 527 → 514**，13 条全部人工抽样复核为真改名；新增 3 条守卫测试 | `f676a72` |
| — | **孤儿 skill 防护**：7 项宿主原生 skill（`wq-batch-dispatch-safety`、`wq-operator-playbook-by-gate`…）永不进入归档清单 | `git log --all -- Claude/skills/<name>` 在这 7 项上**零提交**；新增机械判定 `_never_in_repo_history` + 守卫测试 | `b1fc1cd` |
| **G** | `selfcorr_quick_out/` 空目录 | 复核时已不存在，无需动作 | — |

### 关于 C：为什么值得单独立一条

`PENDING` 的语义是「**没人看过**」。把「已改名入库」算进去，是台账自己制造欠债。
2026-10-08 的实测正是如此：一批文件按命名规范整改（`2026-08-26` → `20260826`、日期移到末尾）后，
旧名仍留在抢救点快照里，而 main 里已是新名 ⇒ 台账凭空多出 13 条 PENDING。

判据设了两道闸，缺一不可：

1. **blob 逐字相等** —— 证明件没丢，只是换了位置/名字；
2. **归一化词干相同** —— 阻止「同内容模板文件」冒充改名（空 `__init__.py`、同模板头这类成片同 blob 件），
   否则改名识别就退化成「机器替人判不回迁」，那正是本台账明确不做的事。

抽出复核的 13 条：11 条是日期位移（`reports/db_schema_audit_2026-08-26.md` → `..._20260826.md`）、
1 条是目录+文件名同时变（`world-quant-brain-mcp/docs/MCP_TEST_REPORT_20260913.md` → `world-quant-brain-mcp/MCP_TEST_REPORT.md`），
**零误判**。

## 2. 顺带修掉的两个真 bug（不在原计划里）

| 文件 | 问题 | commit |
|---|---|---|
| `tools/fields/field_profile.py` | `DESC_SQL` 裸写 `FROM fields`。`fields` 表**没有 region 列**（须经 `dataset_id` 关联），裸写 ⇒ 跨区查询**静默串区**，不报错、结果错 | `4a9ae8e` |
| `tools/skill_lint.py` | 含尖括号的**占位**脚本路径（`<repo 外>/x.py`）被判「脚本不存在」——词法切开后残留 `外>/x.py`，是假阳性；它曾真的拦下一次提交 | `4a9ae8e` |

## 3. 当前闸门读数（2026-10-09）

```
[audit_structure] FAIL=0  WARN=4
  WARN S16 报告命名规范: 基线内存量违规 15 个（§8.13：存量不强制回改，改一个就请从基线移出）
  WARN S13 tracking 非区域目录: 1 项登记项磁盘已不存在（PPA_USA，可从 NON_REGION_DIRS 清）
  WARN S6 skills 漂移: 4 组已知跨 skill 复制（已登记基线）
  OK  S11 tools 顶层冻结 / S14 README 登记 150/150 / S12 无复活 / S7 根无散件
doc_path_refs : BROKEN 0（基线 0）｜ UNTRACKED 0
pytest        : 3156 passed, 22 skipped
```

## 4. 不做的三项（含触发条件）

| 项 | 现状 | 不做的理由 | 什么时候该做 |
|---|---|---|---|
| **D** `reports/` 结构混杂 | 主题子目录与散件并存 | 纯观感问题，不影响检索之外的任何功能；改结构要同步动所有引用 | 出现「找不到某份报告」的实际投诉时，按主题归档一次 |
| **E** `output_report/` **160 个全平铺** | 写方 4 处：`complexity_scan.py`、`os_report.py`、`refs_scan.py`、`src/wqb/workflow/nodes/feature_engineering.py` | 批量分区 = 同时动 160 个路径 + 全部引用，收益只是观感。**命名这件事已被 S16 机械化守住**（新增违规直接 FAIL），分区可等有真实检索需求再做 | 需要按区域归档/清理旧波次产物时 |
| **H** `cache/` 385 MB / 3 096 件 | **296 MB 是单件** `cache/_probe/probe.db`（2026-09-29），其余 3 095 件合计约 89 MB | 删除是**破坏性动作**，未经确认不执行；且 `probe.db` 是否可重跑只有使用者知道 | 确认 `probe.db` 可重跑后**单删这一件**，即释放 77%；其余 89 MB 不值得动 |

## 5. 本轮沉淀的三条提交纪律（踩过才写）

1. **一条命令只提交一组**：沙箱 safe-delete 预算按**命令**累计，钩子把 `TMPDIR` 放进仓库内 ⇒
   同一条命令里连跑多组会被**假失败**（实测 12 组连跑，后 4 组假失败）。
2. **暂存集必须校验**：`git add -A -- <paths>` 后比对 `git diff --cached --name-only`，
   与目标集不等就 `git reset` 中止 —— 否则会吞进别人的在途文件（实测一组吞进 21 个别组文件）。
3. **并行会话的在途改动会污染 pytest**：钩子跑的是**工作树**，别人改到一半的文件会让我的提交变红。
   提交前先看 `git status -uall`，不是我的文件一律不进暂存集，也**不用 `--no-verify` 绕过**。
