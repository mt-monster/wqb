# 提交执行结果（2026-09-21，用户指定 3 颗）

## 结果

| alpha_id | 区域 | 名称 | 结果 |
|---|---|---|---|
| `d5bnE8jJ` | GLB | `GLB_liqgate_dl20d_countryrank_d10` | ✅ **已提交**（ACTIVE / stage=OS，2026-09-21T04:49:13-04:00）|
| `P02wbJAM` | ASI | `ASI_newsgate_dl20d_countryrank_d12` | ✅ **已提交**（ACTIVE / stage=OS，2026-09-21T04:50:59-04:00）|
| `88jaV5lv` | ASI | `ASI_preclose30m_reversal_newsgate_d12` | ❌ **未提交**：`REGULAR_SUBMISSION(value=4, limit=4)` 配额墙（403，**零成本未扣配额**）|

## 提交前检查（全部通过）

1. **零成本判定** `submit_verdict`：三颗均 `VERDICT: UNVERIFIABLE`（处女提交无提交层记录），模拟层 **18 条 checks / 0 FAIL / 2 良性 WARNING**（`MATCHES_COMPETITION`、`MATCHES_THEMES`）。
2. **prod/self 复核**（`check_correlation(refresh=true)`）：0.6307 / 0.6715 / 0.5093（均 <0.7）；self 0.136 / 0.000 / 0.000。
3. **描述**：三颗原先**均无名称与描述**（空描述会被平台静默丢弃）→ 已按 house style 写入三段式描述（938 / 866 / 908 字）并回读验证。

## 配额墙根因（重要）

今日 ET 日（2026-09-21）REGULAR 配额 **4/4 已用尽**，其中**前 2 颗不是本轮提交的**：

| 时间 (ET) | alpha | 区域 | 提交方 |
|---|---|---|---|
| 04:16:58 | `gJboYLRl` | GLB | 非本轮（并行会话）|
| 04:18:54 | `mLmxKN12` | GLB | 非本轮（并行会话；其 note 原就写着"等 ET 重置后提交"）|
| **04:49:13** | **`d5bnE8jJ`** | GLB | **本轮** |
| **04:50:59** | **`P02wbJAM`** | ASI | **本轮** |

**为什么没提前发现**：`GET /users/self/activities/submissions` 只返回 `{yesterday, current, previous, ytd}`
——**没有 today 字段**，`ytd.end` 停在昨天 → 据此推算"今日 0 提交、4 个空位"，实际只剩 2 个。
→ 已新增 `tools/quota_status.py`（列 `stage=OS` 按 `dateSubmitted` 数当日颗数），实测输出 `REGULAR 配额：4/4 → 剩余 0`。

## 后续动作

- **`88jaV5lv` 明日（ET 次日，12:00 GMT+8 重置后）可直接重试**：描述已写、prod 复核 0.5093 通过、verdict 无 FAIL，
  唯一阻塞是配额。本地台账已备注该状态。
- 本地已更新：`submit_ready` 中两颗粒 → `SUBMITTED`；`submission_ledger` 补 2 条；`88jaV5lv` 加配额墙备注。
  另核对确认 `mLmxKN12` 已由他处正确标记，无"已提交但仍 READY"的陈旧行（防重复提交）。
- 备份：`data/wqb.db.bak_submit3_20260921_170553`
