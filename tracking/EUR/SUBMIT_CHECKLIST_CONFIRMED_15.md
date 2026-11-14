# EUR REGULAR Alpha 提交清单 — 已确认 15 颗（2026-11-12 21:45）

> **全部通过四重验证**：IS 全闸（S/F/2Y/SUB-S/TO/margin）+ 互相关 <0.7 + self <0.7 + **prod <0.7**。
> 机器可读（含表达式全文）：`results/eur_basket_confirmed.json`
> ⚠ 只挖不提交，提交权归用户。prod 值均为 2026-11-12 实测。

## 按 prod 从低到高（建议提交顺序）

| 序 | alpha | S | 2Y | SUB/S | TO | prod | 塔/机制 |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | **mL617YPx** | 1.82 | 2.23 | 0.68 | 6.8% | **0.5421** | fundamental：fnd72 现金流质量（ATOM）|
| 2 | **E56GgqLL** | 1.68 | 2.12 | 0.72 | 5.9% | **0.5524** | fundamental×imbalance：fnd72×imb5 |
| 3 | **N1P02YwL** | 1.81 | 2.62 | **0.83** | 3.8% | **0.6073** | **risk**：qfl×risk60 借券费率 |
| 4 | O0W0w3P7 | 2.72 | 3.31 | 0.52 | 28.3% | 0.6403 | news：news46 事件流量（**已 ACTIVE**）|
| 5 | **WjOeNE6O** | 2.90 | 2.15 | 0.66 | 10.6% | 0.6411 | imbalance：imb5×买卖比（ATOM）|
| 6 | **6XMmE0EL** | 2.35 | 1.70 | 0.80 | 32.5% | 0.6529 | other：techindi 极端分位差（ATOM）|
| 7 | **mLaLllmK** | 3.98 | 1.93 | 0.56 | 29.1% | 0.6579 | other：techindi 概率分位差（ATOM）|
| 8 | **qME6VWbj** | 1.76 | 1.65 | 0.57 | 5.0% | 0.6609 | analyst：ebi 均值修订（ATOM）|
| 9 | **78L5GaeZ** | 3.02 | 2.55 | 0.57 | 13.8% | 0.6662 | other×analyst：techindi×revenue_revision |
| 10 | **rKRx7v6m** | 3.22 | 2.07 | 0.57 | 18.9% | 0.6756 | other×sentiment：techindi×snt26 |
| 11 | **VkxWmpYG** | 2.15 | 2.33 | 0.67 | 14.0% | 0.6800 | other×analyst×news |
| 12 | **WjOAJWxd** | 2.36 | 2.67 | 0.54 | 8.0% | 0.6806 | analyst：ebt 修订（ATOM）|
| 13 | **JjeNJ00O** | 2.60 | 2.31 | 0.61 | 19.9% | 0.6813 | **risk**×imbalance：−rsk60_offer×imb5 |
| 14 | **N1NGbddg** | 1.69 | 2.17 | 0.53 | 5.1% | 0.6872 | analyst×institutions：analyst7×inst6 |
| 15 | **zq3Yrb3G** | 2.87 | 2.10 | 0.52 | 18.4% | 0.6872 | **risk**×analyst：rsk68_beta 门控 |

## 点塔效果（提交后）
| 塔 | 提交前 | 提交后 |
|---|---|---|
| **risk** | 2/3 | **3/3 点亮**（N1P02YwL + zq3Yrb3G + JjeNJ00O）|
| **institutions** | 0/3 | 1/3（N1NGbddg）|
| news / other / analyst / fundamental / imbalance / sentiment | 已点亮 | 已点亮 |

## 提交前自查（两步）
```
1. submit_verdict(alpha_id)        # 查完整 checks（含 warning，fails=[] 不代表可提交）
2. check_correlation(alpha_id, correlation_type='production', refresh=True)   # prod 复测
   └ 若 MCP 超时：python tools/prod_wait.py <id> --minutes 45（后台）→ 落库后 MCP 命中缓存
```

## 缺口与补充进展
目标 20 颗，已确认 15 颗，缺 5 颗。补充来源：`predictive_starmine`（MODEL 塔，仅 3 颗已提交 = 非饱和族）两波 20 臂在跑：
- P1：8 个 ALIVE 字段 ATOM（best_sub 1.12–1.42）
- P2：ac=0 未使用字段（`arm_score_change_7d_3` / 上下修净差 / `predicted_surprise_fy2_*`）

## 本轮被 prod 淘汰的候选（17 颗实测，FAIL 11 颗）
| alpha | S | prod | 主因 |
|---|---:|---:|---|
| zq378ELo | 1.64 | 0.8887 | institutions ATOM，被已提交件占用 |
| RRE6j9E0 | 3.09 | 0.8600 | techindi 同源 |
| 78LNnA88 | 2.74 | 0.8391 | techindi 同源 |
| QPvxRG7G | 3.22 | 0.8160 | techindi 同源 |
| omEWJz3l | 3.42 | 0.8069 | techindi×rsk68 |
| KPJoJp21 | 4.19 | 0.7992 | techindi 同源 |
| vR1EKMmQ | 3.81 | 0.7810 | techindi 同源 |
| QP0kYMqr | 2.95 | 0.7476 | risk×news |
| pwd2Za1g | 3.97 | 0.728 | techindi 同源 |
| 58EJXapM | 2.03 | 0.7156 | 内部人+imb |
| mLoGVenK | 2.89 | 0.7125 | techindi×rsk68 |

⇒ **规律：techindi probability 同源件（与已提交的 mLaLllmK / 6XMmE0EL 撞池）prod 普遍 0.78–0.86；机制不同族的件 0.54–0.69 通过。**
