# EUR REGULAR Alpha 提交清单 — 17 颗已确认 + 4 颗待测（2026-11-12 22:10）

> 已确认 = 四重验证全通过（IS 全闸 + 互相关 <0.7 + self <0.7 + **prod <0.7 实测**）
> ⚠ 只挖不提交，提交权归用户。

## A. 已确认 17 颗（按 prod 从低到高 = 建议提交顺序）

| 序 | alpha | S | 2Y | SUB/S | TO | prod | 塔/机制 |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | **mL617YPx** | 1.82 | 2.23 | 0.68 | 6.8% | **0.5421** | fundamental：fnd72 现金流（ATOM）|
| 2 | **E56GgqLL** | 1.68 | 2.12 | 0.72 | 5.9% | **0.5524** | fundamental×imbalance |
| 3 | **xArjE96W** | 2.28 | 2.32 | 0.54 | 10.8% | **0.5907** | **risk**：rsk68_beta 门控+vector_neut |
| 4 | **N1P02YwL** | 1.81 | 2.62 | **0.83** | 3.8% | **0.6073** | **risk**：qfl×risk60 |
| 5 | O0W0w3P7 | 2.72 | 3.31 | 0.52 | 28.3% | 0.6403 | news：news46（**已 ACTIVE**）|
| 6 | **WjOeNE6O** | 2.90 | 2.15 | 0.66 | 10.6% | 0.6411 | imbalance：imb5×买卖比（ATOM）|
| 7 | **6XMmE0EL** | 2.35 | 1.70 | 0.80 | 32.5% | 0.6529 | other：techindi 极端分位差（ATOM）|
| 8 | **mLaLllmK** | 3.98 | 1.93 | 0.56 | 29.1% | 0.6579 | other：techindi 概率分位差（ATOM）|
| 9 | **qME6VWbj** | 1.76 | 1.65 | 0.57 | 5.0% | 0.6609 | analyst：ebi 均值修订（ATOM）|
| 10 | **78L5GaeZ** | 3.02 | 2.55 | 0.57 | 13.8% | 0.6662 | other×analyst |
| 11 | **rKRx7v6m** | 3.22 | 2.07 | 0.57 | 18.9% | 0.6756 | other×sentiment |
| 12 | **VkxWmpYG** | 2.15 | 2.33 | 0.67 | 14.0% | 0.6800 | other×analyst×news |
| 13 | **WjOAJWxd** | 2.36 | 2.67 | 0.54 | 8.0% | 0.6806 | analyst：ebt 修订（ATOM）|
| 14 | **JjeNJ00O** | 2.60 | 2.31 | 0.61 | 19.9% | 0.6813 | **risk**×imbalance |
| 15 | **N1NGbddg** | 1.69 | 2.17 | 0.53 | 5.1% | 0.6872 | analyst×institutions |
| 16 | **zq3Yrb3G** | 2.87 | 2.10 | 0.52 | 18.4% | 0.6872 | **risk**×analyst |
| 17 | **YP1baJrv** | 2.23 | 2.00 | **0.70** | 19.7% | **0.6999** | other：tm_17 动量族 |

⚠ **序 17 `YP1baJrv` prod=0.6999 仅差阈值 0.0001，提交前必须 `refresh=True` 重测**。

## B. 待测 4 颗（IS 全闸 + self 极干净，prod 计算中）
| alpha | S | 2Y | SUB/S | TO | self | 机制 |
|---|---:|---:|---:|---:|---:|---|
| **rKRXK30a** | 2.57 | 2.06 | **0.70** | 14.9% | 0.116 | tm_16 signed_power(rank) 动量（ATOM）|
| **e75bblkp** | 2.44 | 2.14 | **0.74** | 21.5% | 0.000 | tm_19 动量×rsk70 残差 |
| **A1VLR6Yd** | 2.09 | 2.05 | 0.67 | 4.6% | 0.127 | buy_sell_ratio_top20（ATOM）|
| **omEadgW5** | 2.21 | 2.10 | 0.64 | 4.8% | 0.130 | buy_sell_ratio_top5（ATOM）|

## C. 点塔
| 塔 | 提交前 | 提交后 |
|---|---|---|
| **risk** | 2/3 | **3/3 点亮**（N1P02YwL / zq3Yrb3G / JjeNJ00O / xArjE96W）|
| **institutions** | 0/3 | 1/3（N1NGbddg）|

## D. 提交前自查
```
1. submit_verdict(alpha_id)                                   # 完整 checks（含 warning）
2. check_correlation(alpha_id, correlation_type='production', refresh=True)
   └ MCP 超时则：python tools/prod_wait.py <id> --minutes 45   # 后台，落库后 MCP 命中缓存
```
