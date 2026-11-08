# insider_trx_matrix · EUR / TOPCS1600 / D1 字段画像

> 类型 MATRIX · 33 字段 · cov 0.607–0.615 · category = **other**（×1.5）· αC 44
> 采集：2026-11-08 · 与 insider_agg_matrix 是**同供应商姊妹集**（同 cov 0.6149、同 OGE 模块、same signal_value 命名）——区别：本集用 **USD 金额**（agg_matrix 是股数）

## 0. 字段结构

| 族 | 字段 | 与 agg_matrix 对应 |
|---|---|---|
| **USD 金额**（本集独有） | `usd_top_direct_signal_value_2`（高管直接买入金额,Sum）等 16 支 | `top_significant_value_*` 的 USD 版 |
| 强度计数 | `total_top_buy_transaction_count` 等 12 支（OGE 强度单位） | 股数族 |
| 方向分 | `directional_indicator_score` | `directional_indicator` |
| mean_* 族 | 均值变体 | 冗余规律适用 |

**关键判断**：`usd_top_direct_signal_value_2`（高管直接显著买入金额）= 席位 1 的 `top_significant_value_2` 的 USD 语义 +「直接」过滤 + 席位池已证 88d zscore 栈。若与席位 1 互相关 <0.9（USD/股数口径差 + 直接/全体差），即第 5 席。

## 1. 探针设计（3 臂,全部用已验证 88d zscore 栈）

1. `usd_top_direct_signal_value_2`（高管直接买入 Sum）
2. `usd_top_direct_signal_value_1`（Mean 版,冗余对照）
3. `directional_indicator_score`（方向分,agg_matrix 族已死但本集是 score 版）

## 2. 实测

（待回填）

## 2. 实测（multisim `1LueB69bp4vU9qtd28vH3jY`）

| 变体 | alpha id | S | F | 2Y | sub | robust | 与席位 1 互相关 | prod |
|---|---|---|---|---|---|---|---|---|
| **usd_top_direct_signal_value_2（高管直接买入 USD Sum）** | `VkxzdXZ0` | **1.60** | 0.81 | 2.09 | 1.07 | 0.81 | **0.857**（<0.9 独立） | **0.8248 FAIL**（0.8-0.9 n=1） |
| _1（Mean 版） | `bl6z8NrZ` | 1.58 | 0.80 | 2.05 | 1.05 | 0.80 | — | — |
| directional_indicator_score | `LLMz5nmn` | 0.85 | 0.30 | 0.72 | 0.59 | 0.35 | — | 死（与 agg_matrix 族一致） |

**归因**：① USD 金额版全绿（S 1.60）且与席位 1 互相关 0.857 部分独立——USD/直接过滤是真实增量;② **但 prod 0.8248 卡墙（0.8-0.9 n=1）**——比 insider_feats 的墙更高（0.80 vs 0.84/0.80）,同一机制级墙（prod 池里的 insider 类 alpha）。③ mean 版冗余规律复现。④ 方向分死（跨集复现）。

**结论**：insider 三集（agg_matrix/insider_feats/insider_trx_matrix）的买方强度机制在 prod 池遭遇**同一个机制级墙**（0.74-0.84 随变体漂移）——prod 池已有 insider 买方强度类 alpha 占位。**第 5 席必须换机制域**（跳出 insider 买方强度）。insider_trx_matrix 归档备用。
