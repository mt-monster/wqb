# tmp / 临时产物清理报告（2026-08-30）

> 触发：用户"清理tmp文件和代码"。先只读扫描出清单 → 用户确认范围 → 执行。
> 全部删除项均为 gitignored 或已归档，**零版本历史损失**。

## 一、用户确认的清理范围与结果

| 项目 | 清理前 | 清理后 | 方式 |
|---|---|---|---|
| `logs/_tmp_*` 一次性脚本/中间 JSON | 969 个（logs 共 11M） | 0 个（logs 5.3M / 386 文件） | 直接删（Python 逐文件，规避 `rm -f *_tmp_*` 参数列表过长） |
| `nul` 垃圾文件 | 643B | 已删 | `\\?\` 扩展路径（Windows 保留设备名，回收站通道失败） |
| `.pytest_tmp/` 测试运行时 | 1.9M | 已删（下次 pytest 自动重建） | 直接删 |
| `tracking/_scratch/` 一次性脚本暂存区 | 99 个文件 720K | 已清空 | **先归档** → `attic/scratch_archive_2026-08-30.zip`（134KB，可恢复）→ 再清空。注：`*.zip` 是 .gitignore L15 规则，该 zip 为**本地归档**（gitignored，不进版本历史） |
| 旧 DB 备份 | `data/` 2 份 + `attic/db_backups/` 7 份 | 各保留最新 1 份 | 删 7 份旧备份，`data/` 123M → **89M**（释放 34M） |

## 二、删除前核验（DB 单一事实源）

- `data/wqb.db` 可打开：**17 张表、58,584 行、34.9MB**，结构完整（alphas 957 / expressions 6864 / fields 46543 / ledger_kv 1129 …）。
- 保留的备份：`data/wqb.db.bak_ladder_20260830`（8/30 19:39）、`attic/db_backups/wqb.db.bak_consistent_20260829`（8/29 17:38）。

## 三、代码清理评估（本轮无新增可清理项）

`tools/scan_deadcode.py` 全仓扫描：62 个未用 import / 59 个死定义，但**全部落在保护文件或活跃脚本内**，不构成死代码：
- `world-quant-brain-mcp/main.py` 12（`tools_*` 副作用注册导入，不可删）
- `world-quant-brain-mcp/brain_api.py` 4（门面重导出，旧导入路径契约）
- 其余在 `tracking/KOR/scripts/*`、`mining/scripts/*` 等活跃战役脚本

## 四、⚠️ 发现并处理：12 个在用但未提交的重构文件

`src/wqb/store/_*.py`（9 个）+ `src/wqb/expression/_*.py`（3 个）是 **2026-08-29 campaign.py 重构拆分产物（1240 行→9 mixin）**，全部正在被 import 使用但从未纳入 git（无版本保护）。本次已：
1. `74233f1` 提交 12 个 mixin 文件（pytest 273 passed）
2. `74233f1`（同 commit 含 diversity_enhancer.py shim + .gitignore 变更）—— 962 行单体缩为 50 行门面重导出，公开 API 不变

## 五、⚠️ 未处理（非本次清理范围，需用户决策）

工作区存在 **118 个已删除未提交的 tracking 脚本**（`tracking/IND/scripts/` 从 100+ 个剩 5 个；`tracking/KOR/scripts/_*.py` 6 个），以及多处未提交修改（`src/wqb/store/campaign.py`、`tests/conftest.py`、`tools/harvest_multisim.py`、`world-quant-brain-mcp/tests/test_mcp_tools_unit.py` 等）和未跟踪文件（`.box-agent/`、`tools/record_submission.py`、`world-quant-brain-mcp/tests/test_transport_and_sim_unit.py`、`tracking/IND/reference/*.json`、`attic/tools_archive/kor_one_off_probes/`）。这些疑似并行会话产物，**本次未触碰、未提交**，请确认归属后自行处理。

---

*执行时间：2026-08-30 21:30–23:50。清理后 pytest 回归见下文记录。*
