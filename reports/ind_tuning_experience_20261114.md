# IND 调优经验 · 2026-11-14

> 人工复盘 → reports/。所有条目带证据（alpha id / 实测数字），可复用。

## 1. 残差化 decay 阶梯（IND 通用杠杆）

| 场景 | 杠杆 | 证据 |
|---|---|---|
| HIGH_TURNOVER(0.40) 唯一败闸 | decay 4→126 | YPaXr1Pw TO 0.832→MP69RYAk 0.244，failed_ra 1→0，S 4.79→2.98 |
| robust 贴线 0.99（差 0.01） | decay→8 角点 | E5QoA0EK 0.99 FAIL → rK7Qm6ld 1.04 PASS |
| decay 过头 | 63/126 | d5aeAg2x S 1.43/robust 0.55（强度塌陷），角点区间 [8,63) |
| 两头贴线无解 | — | 1YW6Qz6X robust 0.99 + 终验 prod 0.7214，弃 |

## 2. 同字段形态决定生死（残差化 vs 裸）

同一字段：残差形态 S 2.0–3.1 vs 裸形态 max 0.74（21 条全灭）。IND 的 institutions6 / earnings3 / sentiment21 全部如此。**判死前必须先测残差形态**，否则误杀活字段。

## 3. 空转算子（rank 之后）

- `winsorize(rank(x))` / `quantile(rank(x))` 逐位≈原 rank（KPgxRY9z≡E5QoA0EK）：**rank 化后再截尾/重排是空转**，截尾必须放在 rank 之前。
- `quantile(..., driver="gaussian")` 的 `gaussian` 被 preflight 误判 unknown_field：假阳性，人工放行。

## 4. 工具与数据陷阱

| 陷阱 | 证据 | 正确用法 |
|---|---|---|
| `get_datafields(max_fields=null)` | 5/5 集只返 1 条、complete=false | 不传 max_fields 或传 ≥platform_count；必须 filter_sharpe=False |
| DB dataset_profile 过期 | model77 DB 348 字段/cov 0.85 vs 平台 23 字段/cov 0.40 | 选集必 MCP 实读复核 |
| 塔快照漂移 | 11-14 已亮 7 座 vs 11-05 记 10 座 | 每轮战役现查 get_pyramid_alphas() |
| VECTOR 字段 cov 语义 | earnings11 cov 0.4992 是历史累计覆盖 | 可用性看探针 longCount/shortCount |
| UNITS 警告 | vRAa0jbd add(share, 0.0001) 量纲不匹配 | 除法防零用 add(y,0.0001) 会触发 UNITS 警告，仍可跑但不干净；换 divide 前置 min-clamp 待验证 |

## 5. 合规面计算（交前先算）

IND 双塔候选的合规篮大小 = min(同骨架互相关子集, 跨 trio 配额)。本轮：G1 9 锚 → 3（互相关 0.72–0.95）；异族 4 颗 → +2（sent21/ern3 各 1，同族第 2 颗互相关 0.96/0.98 只能进 1）；配额 5 封顶。**新战役开波前先估这个数，再决定波数预算。**

## 6. 判死回写清单（已落 DB）

IND-SENT21-BARE-DEAD / IND-ATOM-BARE-STRUCT-DEAD / IND-EARN11-VECTOR-META-DEAD / IND-MDL77-ESG-WEAK-DEAD / IND-OTHER323-STATIC-DEAD（forum_recon 均 waived：非论坛可解的数据实测判死）。
