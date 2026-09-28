# 提交执行结果（2026-09-23，用户指定的 4 颗定稿清单）

## 结果：**2 成功 / 3 失败**（配额用 2/4）

| 序 | alpha_id | 区 | 结果 |
|---|---|---|---|
| 1 | `mLjnnzKE` | IND | ❌ **COMPILE_ERROR**（非相关性闸）|
| 2 | **`LLNgdpw2`** | ASI | ✅ **已提交** ACTIVE/OS @ 2026-09-23T01:21:06-04:00 |
| 3 | `3qX6wLkP` | IND | ❌ 403 `PROD_CORRELATION=0.9805` |
| 4 | **`3qX3Mp6O`** | IND | ✅ **已提交** ACTIVE/OS @ 2026-09-23T01:26:37-04:00 |
| 备 | `xA392Xpb` | IND | ❌ 403 `SELF=0.7019` + `PROD=0.7019`（双闸同时超线，仅超 0.0019）|

## ★ 两个重要发现

### 1. 幽灵字段 = **根本不可提交**（修正既有认知）

`mLjnnzKE` 的 403 回带：

```
COMPILE_ERROR: "Expression error: Attempted to use unknown variable \"change_6m_rating_revision\".
                Clone to re-simulate and see more details."
```

**修正**：本仓 ledger 里曾把这类 alpha 记为「prod-clean 存量、**可提交但不可复现/不可改进**」——**实测是连提交都过不了**
（平台提交时要重新编译表达式，不存在的字段直接 FAIL）。
→ 幽灵字段（`change_6m_rating_revision` 等）的 alpha 应直接判死，不该再进候选池。
涉及清单（ledger 原记）：`mLjnnzKE` / `xAj77zlg` / `blj0mgPK` / `1Yw33mO6`。

### 2. 同族挤压的**最强实证**：提交一颗，顶死兄弟

`3qX3Mp6O` 提交入池后，同族（族C，共用 `-ts_mean(corr_last_trade_price_with_volume,5)`）的两颗被瞬间顶超线：

| alpha | 提交前 prod | 提交后实测 | 结果 |
|---|---|---|---|
| `3qX6wLkP` | 0.5836 | **0.9805** | 403 |
| `xA392Xpb` | 0.6458 / self 0.6913 | **0.7019 / 0.7019** | 403（双闸同时超线 0.0019）|

→ 同族**只能取 1 颗**这条纪律再次被验证（昨天的 GLB dl20d 族是 0.81/0.71/1.0，今天是 0.98/0.70）。
今天的执行**正确地按此纪律排序**：族C 只提交了 `3qX3Mp6O`，另两颗成为族内互斥淘汰。
已写 `ledger_kv[IND/family_block_ind_pvcorr_c]`。

## 新增：`submit_alpha` 的第 4 种响应形态

| 形态 | 含义 | 处置 |
|---|---|---|
| `success:true` + 200 "IS checks passed" | 明确通过 | 轮询 → ACTIVE |
| **`success:true` + 201 "Accepted (async); IS checks still computing"** | **异步受理**（本次首次见到）| 轮询；4 分钟后仍 UNSUBMITTED 则补发（本次补发即得 403 真实原因）|
| `success:false` + 200 "Non-JSON submit response" + 空体 | 异步受理、结果未知 | 同上 |
| `success:false` + 403 + failing IS checks | 明确失败（零成本，回带全量 checks）| 记录原因，换下一颗 |

## 当前状态与后续

- 今日配额 **2/4 已用，剩 2 席**（ET 日重置于 12:00 GMT+8）
- `submit_ready`：SUBMITTED 61 / READY 2 / BLOCKED 6
- **候选池已基本清空**：BLOCKED 6 + 今日淘汰 3（mLjnnzKE/3qX6wLkP/xA392Xpb）
  → 要用掉剩余 2 席，需要**新候选**：建议从 **ASI 93 颗未测池**（`tools/prod_first_screen.py`，dry-run 已见 S3.5+/2Y4.4+ 强候选）或 MEA 存量中筛
- 备份：`data/wqb.db.bak_submit23_20260923_133807`
