# EUR 20 颗 REGULAR Alpha 提交清单（2026-11-12 定稿）

> **按 prod 友好度排序**：已确认 prod<0.7 的排前（按 prod 从低到高），未测的排后（按 S 从低到高，因 S 与 prod 正相关）。
> 机器可读版（含表达式全文）：`results/eur_basket_20_submitlist.json`
>
> ⚠ **本清单只挖不提交，提交权归用户。**
> ⚠ prod 值 >48h 的需提交前 `check_correlation(refresh=True)` 复测（今日实测 prod 漂移明显）。

## 一、prod 已确认 <0.7（11 颗，优先提交）

| 序 | alpha | S | 2Y | SUB/S | TO | margin | prod | 塔 |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **mL617YPx** | 1.82 | 2.23 | 0.68 | 6.8% | 17.6bp | **0.5421** | fundamental |
| 2 | **N1P02YwL** | 1.81 | 2.62 | **0.83** | 3.8% | **41.5bp** | **0.6073** | risk |
| 3 | O0W0w3P7 | 2.72 | 3.31 | 0.52 | 28.3% | 3.6bp | 0.6403 | news（已 ACTIVE）|
| 4 | **WjOeNE6O** | 2.90 | 2.15 | 0.66 | 10.6% | 9.6bp | **0.6411** | imbalance |
| 5 | **6XMmE0EL** | 2.35 | 1.70 | 0.80 | 32.5% | 3.8bp | **0.6529** | other |
| 6 | **mLaLllmK** | 3.98 | 1.93 | 0.56 | 29.1% | 6.2bp | **0.6579** | other |
| 7 | **qME6VWbj** | 1.76 | 1.65 | 0.57 | 5.0% | 18.5bp | **0.6609** | analyst |
| 8 | **rKRx7v6m** | 3.22 | 2.07 | 0.57 | 18.9% | 8.9bp | **0.6756** | other×sentiment |
| 9 | **VkxWmpYG** | 2.15 | 2.33 | 0.67 | 14.0% | 9.5bp | **0.6800** | other×analyst×news |
| 10 | **WjOAJWxd** | 2.36 | 2.67 | 0.54 | 8.0% | 14.6bp | **0.6806** | analyst |
| 11 | **N1NGbddg** | 1.69 | 2.17 | 0.53 | 5.1% | 18.7bp | **0.6872** | analyst×institutions |

## 二、IS 全闸 + self <0.7，prod 待测（9 颗）

| 序 | alpha | S | 2Y | SUB/S | TO | margin | 塔 |
|---:|---|---:|---:|---:|---:|---:|---|
| 12 | E56GgqLL | 1.68 | 2.12 | 0.72 | 5.9% | 20.4bp | fundamental×imbalance |
| 13 | 58EJXapM | 2.03 | 2.26 | 0.55 | 5.4% | 12.0bp | imbalance |
| 14 | JjeNJ00O | 2.60 | 2.31 | 0.61 | 19.9% | 5.4bp | **risk**×imbalance |
| 15 | 78LNnA88 | 2.74 | 2.32 | **0.74** | 24.4% | 5.4bp | other |
| 16 | zq3Yrb3G | 2.87 | 2.10 | 0.52 | 18.4% | 6.6bp | **risk**×analyst |
| 17 | 78L5GaeZ | 3.02 | 2.55 | 0.57 | 13.8% | 12.1bp | other×analyst |
| 18 | RRE6j9E0 | 3.09 | 1.86 | 0.64 | 18.4% | 6.1bp | other |
| 19 | QPvxRG7G | 3.22 | 2.38 | 0.62 | 20.8% | 8.4bp | other |
| 20 | vR1EKMmQ | 3.81 | 2.16 | 0.56 | 27.7% | 7.1bp | other |

## 三、验证状态汇总

| 项 | 结果 |
|---|---|
| 数量 | 20 颗（19 REGULAR + 1 ACTIVE） |
| IS 全闸 | 20/20 |
| 互相关（19 颗 REGULAR） | **全对 <0.7，overCount=0，零挤出** |
| self | 19/19 通过 |
| 组腿合规 | 无 ≥2 禁区类；跨 category 组合 5 个（=上限） |
| prod | 11 颗已确认 <0.7；9 颗待测 |

## 四、点塔效果

| 塔 | 提交前 | 提交后 |
|---|---|---|
| **risk** | 2/3 | **3/3 点亮**（N1P02YwL / zq3Yrb3G / JjeNJ00O） |
| **institutions** | 0/3 | 1/3（N1NGbddg） |

## 五、提交前必做的两件事

1. **prod 复测**：`check_correlation(alpha_id, correlation_type='production', refresh=True)`。
   - 若 MCP 因 120s 超时报错 → 改用 `python tools/prod_wait.py <id> --minutes 45`（后台跑），
     结果落库后 MCP 即可命中缓存（`from_cache=true`）。
   - 大盘已证规律：**S≥3.3 的件 prod 失败率显著偏高**，优先提交序 1–11。
2. **完整 checks**：`submit_verdict(alpha_id)` 查 `checks.warning`（`fails=[]` 不代表可提交）。
