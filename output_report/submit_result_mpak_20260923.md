# 提交结果：MPakRYgz（2026-09-23）

## 结论

**成功**：`MPakRYgz` → **ACTIVE / stage=OS**（submitted 2026-09-23T05:28:13-04:00），name `GLB_dl20d_valuegate_d10`。
首次 POST 即 `{"success": true, "reason": "IS checks passed"}`，20 秒内翻 ACTIVE。

## 全闸 checks

| 闸 | 结果 | value / limit |
|---|---|---|
| LOW_SHARPE | PASS | 3.15 / 1.58 |
| LOW_FITNESS | PASS | 2.25 / 1.0 |
| LOW_TURNOVER / HIGH_TURNOVER | PASS | 0.136 / 0.01 · 0.7 |
| LOW_SUB_UNIVERSE_SHARPE | PASS | 2.34 / 1.1 |
| IS_LADDER_SHARPE | PASS | 2.69 / 2.02 |
| LOW_GLB_AMER / EMEA / APAC_SHARPE | PASS | 1.18 / 1.33 / 2.80（limit 均 1）|
| CLUSTER_TEST | PASS | 1.92 / 1.58 |
| **SELF_CORRELATION** | **PASS** | **0.6604 / 0.7** |
| **PROD_CORRELATION** | **PASS** | **0.6604 / 0.7** |
| REGULAR_SUBMISSION | PASS | 2 / 4 |
| MATCHES_COMPETITION / THEMES | WARNING（不阻断）| — |

## 前置动作

1. **补写描述**：原先 `desc_len=0`（无名称无描述）→ 按 house style 写入 `GLB_dl20d_valuegate_d10`
   + 三段式描述（含数据依据与算子依据），回读验证通过。
2. **实时双闸复验**：原始端点轮询 30 秒命中 —— prod **0.6604** / self **0.6606**，与提交层实测（0.6604/0.6604）
   **完全吻合** → 再次印证"提交前探针可信"。

## 意义：GLB dl20d 族「解封」完成

该族 09-22 因同族兄弟连续提交，prod 被顶到 0.81/0.71/1.0（三例全 403），当时被我标记为族级封锁。
今日复验证明**那是暂时性挤压（约 1 天消退）**：本颗与 `MPabNeNz` 均已回落到 0.66–0.67。
`ledger_kv[GLB/family_block_glb_dl20d]` 已更新为 recovered，纪律修订为：
**同族一次只提 1 颗；被顶超线的兄弟等回落后可再提（实测约 1 天）**。

## 剩余额度

今日 REGULAR **3/4**（LLNgdpw2、3qX3Mp6O、MPakRYgz），**剩 1 席**；SUPER 1/1 已用完。
剩余候选：`MPabNeNz`（同族，prod 0.6746 / self 0.6747，可提但余量仅 0.025，且与本颗同族 → 建议错开或缓提）。
