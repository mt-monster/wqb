# 提交执行结果（2026-09-22，用户指定 4 颗）

## 结果：3 成功 / 1 硬失败

| alpha_id | 区域 | 名称 | 结果 |
|---|---|---|---|
| `88jaV5lv` | ASI | `ASI_preclose30m_reversal_newsgate_d12` | ✅ **已提交** ACTIVE/OS @ 2026-09-22T08:22:59-04:00 |
| `pwR8rdMg` | GLB | `GLB_dl20d_pastloser_gate_d10` | ✅ **已提交** ACTIVE/OS @ 2026-09-22T08:25:46-04:00 |
| `VkaXbmbG` | GLB | `GLB_dl20d_shortpressure_gate_d10` | ✅ **已提交** ACTIVE/OS @ 2026-09-22T08:28:07-04:00 |
| `0mXA6jYG` | GLB | `GLB_dl20d_newsfocus_gate_d10` | ❌ **未提交**：提交层 `PROD_CORRELATION=0.8168 ≥ 0.7`（403，零成本）|

配额：今日 REGULAR **3/4**（用 3，余 1）。

## ★ 关键发现：同族兄弟连续提交会推高后来者的 prod 相关

`0mXA6jYG` 的 prod 相关变化：

| 时点 | prod | 说明 |
|---|---|---|
| 2026-09-21 16:32（库内记录）| 0.672 | 当时 <0.7，看起来可提交 |
| **2026-09-22 20:34（提交时实测）** | **0.8168** | **在同族 `pwR8rdMg`(20:25) 与 `VkaXbmbG`(20:28) 提交后** |

四颗中三颗 GLB 共享同一 base 信号（`single_bucket_20day_return_estimate_ohlcv_img_2` + `group_rank(...,country)`），
仅 **门控不同**（过去输家 / 融券费率 / 新闻关注度）。同族兄弟进入生产池后，第三颗的 prod 相关被推到 0.8168。
其余 IS checks 全 PASS（LOW_SHARPE 1.98 / LOW_FITNESS 1.10 / SUB_UNIVERSE 1.62），self-corr 仅 **0.449**（PASS）。

**→ 新纪律：同族（共享 base signal）候选一次最多提交 1 颗；若必须连提，按"IS 强度降序"排**——
本次正是该顺序保住了更强的 `pwR8rdMg`(S3.81) 与 `VkaXbmbG`(S3.52)，只损失最弱的 `0mXA6jYG`(S1.98)。

## 执行前的检查（全过）

| 项 | 结果 |
|---|---|
| 配额实况（`tools/quota_status.py`）| 0/4 → 4 可用 ✅（上次事故后新增此工具，本次首次实战）|
| prod/self 复核 | 3 颗 GLB 无名称无描述 → **已补写三段式描述**（981/977/915 字）并回读验证；`88jaV5lv` 昨日已写（908 字）|
| 互相关系数（note 实测）| `VkaXbmbG × 0mXA6jYG = 0.41`、`0mXA6jYG × d5bnE8jJ = 0.45` → 批内 self 层无冲突 |

## 工程注意

- 三次成功的 POST 都返回 **`{"success": false, "reason": "Non-JSON submit response", "status_code": 200, "raw": ""}`**
  —— 这是平台的**异步受理**形态（HTTP 200 + 空体），**不是失败**；必须以轮询到的 `status=ACTIVE` 为准。
- 提交脚本全程增量落盘（`logs/_submit4_result.json`），且"轮询查询失败"不判定为"提交失败"
  —— 上次（09-21）正是靠这条纪律才没误判与重复提交。

## 后续

- `0mXA6jYG` 待 prod 回落 <0.7 或有新的去相关门控后再提；已在 `submit_ready` 标 `BLOCKED` 并记录原因。
- 同族 GLB（`MPakRYgz`/`QPbEkvzw`/`MPabNeNz`/`A1Nn2vPQ`）prod 现同样受本次提交影响，**需重验后再议**。
- 台账已更新：`submit_ready` → SUBMITTED 58 / READY 9 / BLOCKED 2；`submission_ledger` 补 3 条；
  备份 `data/wqb.db.bak_submit4_20260922_203802`。
