# 战役台账 schema（LedgerStore）

台账后端：默认 SQLite `ledger_kv` 表（`data/wqb.db`，`make_ledger_store` 默认 sqlite，见 `_lib/ledger.py` SqliteLedgerStore）；JSON 版 `<campaign>/<region>_d1_campaign_state.json` 仅历史兼容（2026-08-21 起已归档，不再维护）。

## LedgerStore 原语
- `load()` / `atomic_save(d)`：写前自动 `.bak` 滚动备份；tmp+os.replace 原子写。
- `update(mutator)`：**双遍重放**——load → mutator(d) → 重新 load（捕获并行会话间隙写入）→ mutator(fresh) 重放 → atomic_save。防并行会话互相覆盖。
- **幂等 mutation 纪律**：同名键覆盖、列表去重追加（这样双遍重放才安全）。
- schema 守卫：空 key 或 `_` 前缀 key 拒绝写入（`_` 前缀保留给本地约定）。

## 键命名约定
| 键模式 | 内容 | 写入方 |
|---|---|---|
| `campaign` / `settings` / `notes` | 战役标识、仿真设置快照、杂注 | 建战役时 |
| `waves[]` | {wave, dataset, note, added_at} | ledger add-wave |
| `<dataset>_dead` | {dataset, reason, dead_at, dead_count, salvage?} | ledger mark-dead / score_datasets --mark-dead |
| `wave<N>_verdict` / `wave<XXx>_verdict` | 逐波评审结论 {multisim(s), result, conclusion, reviewed_at} | ledger set-verdict |
| `review_<tag>` | 评审快照（review_wave --write-ledger / --tag）。value schema：`{total: int, candidates: [{id, sharpe, fitness, ...}], near: [...], walls_count: {...}, next_moves: [{priority, reason, action}], reviewed_at}`——candidates/near 为列表（空=无达标），消费方按字段而非整串解析 | review_wave --write-ledger |
| `wave<N>_dataset_switch` | {date, from, to, reason, protocol} 数据集切换记录 | 人工/ledger set |
| `submit_ready[]` | {id, note, queued_at} 达标待提交缓冲池（错峰释放额度） | review_wave --write-ledger |
| `near_pool[]` | {tag, at, near:[{id, sharpe, walls}]} 近门槛池 | review_wave --write-ledger |
| `diversity_audit_latest` / `diversity_history[]` | 多样性审计最新值 + 累积趋势 | diversity_audit |
| `polling_tooling_freeze` 等 `*_note`/`*_freeze` | 战役纪律固化记录 | 人工 |

## CLI（campaign.py ledger / 直接 _lib.ledger 不支持，走 campaign.py）
```
campaign.py --campaign-dir <DIR> ledger keys
campaign.py --campaign-dir <DIR> ledger get <key>
campaign.py --campaign-dir <DIR> ledger set <key> '<json>'
campaign.py --campaign-dir <DIR> ledger mark-dead <ds> --reason "..." [--salvage "..."]
campaign.py --campaign-dir <DIR> ledger add-wave <wave> --dataset <ds> [--note "..."]
campaign.py --campaign-dir <DIR> ledger set-verdict <wave> --json '<json 或 @相对战役目录的文件路径>'
campaign.py --campaign-dir <DIR> ledger submit-ready <alpha_id> [--note "..."]
campaign.py --campaign-dir <DIR> ledger backup
```

## 与 registry（campaign-matrix）的边界
台账 = 战役内逐波细节（verdict/near_pool/submit_ready/diversity_history）；registry = 跨会话结论（dead_ends/wins/campaigns 状态）。逐波 verdict **不进** registry；数据集判死结论在战役结束后由 campaign-matrix 回写流程提炼进 `registry_empirical` 表（带 rule + dead_at + salvage）。
