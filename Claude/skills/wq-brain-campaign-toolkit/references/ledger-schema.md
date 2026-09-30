# 战役台账（ledger_kv）：后端、原语、键目录、CLI

## 1. 后端

台账 = SQLite `data/wqb.db` 的 **`ledger_kv` 表**（`(region, key)` 唯一，`value` 为 JSON）。`make_ledger_store(ctx)` 缺省返回 `SqliteLedgerStore`（`_lib/ledger.py`）；**JSON 后端**（`<campaign>/<region>_d1_campaign_state.json`）**已弃用**（2026-08-21 起归档、不再维护，只为历史兼容保留类）。

原语（SQLite 后端）：

- `load()`：读出本区全部键值。
- `update(mutator)`：**单事务**内 `load → mutator(d) → 写回`（SQLite 行级锁替代了 JSON 后端的「双遍重放」）。
- `backup_now()`：把本区全部键值导出为 JSON 快照（`campaign.py ledger backup`）。
- **幂等 mutation 纪律**：同名键覆盖、列表去重追加，重复执行无副作用。
- schema 守卫：空 key 或 `_` 前缀 key 拒绝写入（`_` 前缀留给本地约定）。

（`.bak` 滚动备份、`atomic_save`（tmp + `os.replace`）与「双遍重放」（捕获并行会话间隙写入）是**JSON 后端**的机制，随该后端一并弃用。）

## 2. 键目录：单一来源是 `docs/ledger_keys.json`

不要在这里再抄一份键表。`docs/ledger_keys.json` 登记**每一个**键：`status`（`active` / `legacy` / `deprecated` / `external`）、用途、**写入方**、**读取方**、缺失时的行为、刷新方式；`tests/unit/01_store_db/test_ledger_key_catalog.py` 守：代码或文档里出现的键必须登记；有读取方而无写入方的键必须登记 `orphan` 且登记必须仍为真（一旦补上写入方就得删登记）；已废止的键只能出现在带「废止 / 历史」字样的行；登记的代码引用必须真实存在并含该键字面量。**新增 / 改名 / 废弃一个键 = 先改这份目录**（键里的 `<x>` 是占位符）。

键的家族按前缀分（详见目录）：`s0_*` / `s1_*` / `s2_*`（各阶段产物）、`review_<tag>` / `near_pool` / `salvage_pool`（评审）、`prod_first_<wave>` / `prod_family_*` / `xr_probe_*`（prod 探针）、`region_kb` / `priors_snapshot_<region>`（先验）、`ckpt_w<wave>`（pipeline checkpoint，取代旧的 checkpoint 文件）、`waiver_<gate>_<region>_<wave>`（逃生口留痕）、`saturated_datasets` / `dataset_empirical_prior`（S0 反馈与先验）等。

**已废止 / legacy 的键（仍可能在旧数据里见到，新写入不要用）**：

| 键 | 状态 | 替代 |
|---|---|---|
| `wave<N>_verdict` / `wave<XXx>_verdict`（`campaign.py ledger set-verdict` 写的） | 废止 | **`wave_results.verdict`**（`campaign.py wave upsert --verdict …` 或 MCP `upsert_wave_result`）——逐波结论的唯一真相源，不再双写；CLI 命令仍会写旧键，但每次打印废止提示 |
| `s6_verdict_<wave>` | 废止 | 同上 |
| `submit_ready`（ledger 列表 `{id, note, queued_at}`） | legacy 审计副本 | **提交队列是 SQL 表 `submit_ready`**（S3 收批自动入队、提交后自动退役；MCP `get_submit_ready` / `tools/submit_queue.py list` 读它）。ledger 键没有生命周期、不会退役，**不要拿它当待提交清单** |
| `submit_ready_blocked` | 废止 | `saturated_datasets`（写入口 `campaign_intel.py mark-saturated`） |
| `wave<N>_dataset_switch` | legacy | 数据集切换记录，只读 |

## 3. CLI（`campaign.py --campaign-dir <DIR> ledger …`；不支持直接 import `_lib.ledger` 写库）

```
ledger keys                                      # 列键（含类型 / 条数）
ledger get <key>                                 # 读
ledger set <key> '<json>' | @file.json           # 整值写；@ 后接绝对路径或相对战役目录的文件（中文 / 多行 JSON 走文件）
ledger mark-dead <ds> --reason "…" [--salvage "…"]   # 写 <ds>_dead
ledger add-wave <wave> --dataset <ds> [--note "…"]   # 追加 waves[]
ledger backup
# 已废止（仍可执行，每次打印提示）：ledger set-verdict …、ledger submit-ready …
```

**`ledger set` 是整值覆盖**：写 `s0_whitelist` 这类多方共用的键会抹掉别人写的内容（2026-09-25 事故），共享键用 MCP `upsert_ledger_key` 的 `mode="merge"`（`replace` / `append` 是另两种模式；`append` 会拒绝对非列表值追加）。

## 4. 与 registry 的边界

台账 = 战役内逐波细节（评审快照 / 近闸池 / 多样性历史 / 检查点 / 先验快照）；`registry_empirical` = 跨会话结论（dead_ends / wins / campaigns 状态 / orphans，schema 与写入规范见 `wq-brain-campaign-matrix` §4）。**逐波 verdict 不进 registry**（进 `wave_results`）；数据集判死的**结论**在战役结束后由 RA 步 9 提炼进 `registry_empirical`（带 rule + dead_at + salvage），战役内的 `<ds>_dead` 只是过程标记。

## 5. 文件时代的同步校验（`check_ledger_sync.py`）

`tools/` 与 toolkit `scripts/` **各有一份**同名脚本，二者校验的都是 `runs/` 批次字母与 `WAVE_LEDGER.md` 的一致性——**文件时代**的做法；DB 单轨后只有战役目录仍保留这些文件时才有意义。**现行的「台账同步门」= 开波三道区域闸（DB 判定）+ `tools/step_funnel.py`**（RA 决策表 D8）。
