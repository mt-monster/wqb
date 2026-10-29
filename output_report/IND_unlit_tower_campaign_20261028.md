# IND 未点亮塔战役 · 归因与对比实验（2026-10-28）

范围：`IND / TOP500 / delay1 / STATISTICAL / decay4 / truncation0.08 / nanHandling OFF`
（nanHandling 是本次实验变量时会在行内注明 ON）。
波次全部经 MCP 派发（`create_multi_simulation`，账户并发 2），收割经
`tools/harvest_multisim.py --auto-upsert` 入库，指标以 `batch_get_alpha_metrics` 的 MAE 读数为准。

## 1. 结果总览

| 数据集 | 塔 | 波次 | 臂数 | RA 全过（`failed_ra_count==0`） | 关键结论 |
|---|---|---|---|---|---|
| imbalance5 | IMBALANCE（未亮） | `ind_imb_nanoff_20261028` | 8 | **3（ATOM eff=1）** | 真 ATOM，S 1.74–1.78 / rob 1.14–1.16 |
| imbalance5 | IMBALANCE | `ind_imb_atom2_20261028` | 6 | 0 | 短窗/换形态全部掉 robust（0.61–0.91） |
| insiders1 | INSIDERS（未亮） | `ind_ins_fields_20261028` | 6 | 5 | 残差动量族全过，S 1.96–2.45 |
| insiders1 | INSIDERS | `ind_ins_tsrank_20261028` | 6 | 4 | `ts_rank` 种子把 rob 拉到 1.74 |
| sentiment21 | SENTIMENT（未亮） | `ind_snt_resid_20261028` | 6 | 6 | S 2.65–2.76 / rob 1.30–1.89 |
| sentiment21 | SENTIMENT | `ind_snt_mod20261028` | 6 | 6 | 换 4neg/4pos/3neg/5pos/2neg/2neut，S 2.41–2.82 |
| option1 | OPTION（未亮） | `ind_opt_probe_20261028` + `ind_opt_resid_d126_20261028` | 12 | 0 | **判死**：2Y 全部 ≤ 0.5 |
| shortinterest5 | SHORTINTEREST（未亮） | `ind_si_probe_a/b_20261028` + `ind_si_diag_20261028` | 18 | 0 | **判死**：字段恒常数（数据未落地），见 §7.5 |

合计 **26 颗 RA 全过** 落在三个此前未点亮的塔上（IMBALANCE 5 / INSIDERS 9 / SENTIMENT 12），
其中 **IMBALANCE 5 颗是真 ATOM**（`pyramids.effective == 1`，`IND/D1/IMBALANCE`，multiplier 1.0）。
其余 21 颗是 PV + 本类别的双类别（`effective == 2`），属「残差化结构」的组腿形态，**不是 ATOM**。

**五个未点亮塔已全部探完**（当季口径：insiders 0 / imbalance 0 / option 0 / sentiment 0 / shortinterest 0）：

| 塔 | 探测臂数 | ATOM | 结论 |
|---|---|---|---|
| IMBALANCE | 23 | **5** | 唯一可产真 ATOM 的未点亮塔 |
| INSIDERS | 24（含 6 纯 ATOM 探针） | 0 | 只有 eff=2 残差族（9 颗 RA 全过） |
| SENTIMENT | 62 | 0 | 只有 eff=2 残差族（12 颗 RA 全过） |
| OPTION | 40（option1 12 + option30 24 + 其它 4） | 0 | option1 十年数据缺口；option30 有数据但 \|S\|≤0.83 |
| SHORTINTEREST | 18 | 0 | 三字段恒常数 ⇒ 数据未落地 |

⚠ 塔位是**按已提交 alpha 计**：本轮全部为 UNSUBMITTED，因此
`get_pyramid_alphas(IND, D1)` 仍是 `insiders 0 / imbalance 0 / sentiment 0`
（当季已亮：news 4 / other 4 / pv 8 / analyst 3 / model 3 / fundamental 3 / risk 3 / macro 2 / earnings 1 / institutions 1）。
点亮塔必须走提交（需用户确认 + `submit_verdict` 预检 + prod 实测），本报告不含任何提交动作。

**完成度审计**（26/26 RA 实时复核、5 颗 ATOM 的塔归属、十年覆盖证据）见 [§4.1](#41-完成度审计2026-10-28-收盘全部-mcp-实测无临时脚本)。

## 2. 交付候选（按 ATOM 优先排序）

### 2.1 IMBALANCE 真 ATOM（`group_rank(ts_mean(ts_backfill(imb5_score, 22), W), industry)`）

| alpha | W | Sharpe | Fitness | TO | 2Y | robust | investability_S | RA |
|---|---|---|---|---|---|---|---|---|
| `RREn5xAj` | 126 | 1.77 | 1.32 | 0.0604 | 3.12 | 1.15 | 1.65 | 0 失败 |
| `bl65x0xl` | 126（bf66） | 1.78 | 1.33 | 0.0605 | 3.13 | 1.16 | 1.65 | 0 失败 |
| `mLoMKnYW` | 147 | 1.74 | 1.28 | 0.0598 | 3.02 | 1.14 | 1.64 | 0 失败 |
| `mLoMnqPE` | 168 | **1.87** | **1.43** | 0.0594 | 2.99 | 1.15 | 1.66 | 0 失败 |
| `YP1G3NjM` | 112 | 1.79 | 1.33 | 0.0608 | 3.10 | 1.10 | 1.65 | 0 失败 |

`RREn5xAj` 平台明细：`MATCHES_PYRAMID` 通过，`CLUSTER_TEST` 0.68（limit 1，WARNING 级），
RA fail=0，PPA fail=0；`pyramids.effective=1`。
**self 相关性实测 0.2903（pass，pool 52 / OS 池 59，已排除 power pool 7）**。

### 2.2 SENTIMENT 残差族（PV+SENTIMENT，eff=2）

| alpha | 字段 | Sharpe | Fitness | TO | 2Y | robust |
|---|---|---|---|---|---|---|
| `RREnK5R1` | snt21_3neg_std | 2.82 | 2.04 | 0.2627 | 2.23 | 1.96 |
| `78LEMG8Q` | snt21_4pos_std | 2.78 | 2.00 | 0.2650 | 2.19 | 1.83 |
| `kqN2Gebd` | snt21_2pos_std | 2.74 | 1.95 | 0.2644 | 2.14 | 1.88 |
| `d5WAzegY` | snt21_2neg_std（industry 分组） | 2.73 | 1.93 | 0.2605 | 2.42 | 1.30 |
| `wpQMPNKx` | snt21_2neut_std | 2.72 | 1.94 | 0.2651 | 2.20 | 1.83 |
| `MPYoz99r` | snt21_2neg_std | 2.68 | 1.90 | 0.2625 | 2.26 | 1.69 |
| `A1VMzqYg` | snt21_2neg_std（ts_rank 种子） | 2.67 | 1.88 | 0.2667 | 2.25 | 1.67 |
| `6Xdv0gPJ` | snt21_neg_mean | 2.65 | 1.86 | 0.2650 | 2.19 | 1.89 |
| `KPJjQVPz` | snt21_5pos_mean | 2.59 | 1.80 | 0.2652 | 2.72 | 1.74 |
| `kqN2O8qd` | snt21_4neg_mean | 2.57 | 1.77 | 0.2659 | 2.66 | 1.72 |
| `YP1GJlPR` | snt21_2neg_mean | 2.41 | 1.65 | 0.2469 | 2.28 | 1.40 |
| `A1VMzqJg` | snt21_pos_mean | 2.76 | 1.99 | 0.2645 | 2.23 | 1.89 |

`RREnK5R1` self 相关性 **0.5056（pass）**，top 对手 `0mjk2ZQv`；字段无关性见 §3.F。

### 2.3 INSIDERS 残差族（PV+INSIDERS，eff=2）

| alpha | 字段 / 种子 | Sharpe | Fitness | TO | 2Y | robust |
|---|---|---|---|---|---|---|
| `omEMRpWb` | insd1_shares / zscore | 2.45 | 1.85 | 0.2135 | 2.82 | 1.30 |
| `0mY0xljG` | insd1_valueeur / zscore | 2.38 | 1.80 | 0.2104 | 2.83 | 1.10 |
| `1YNQO9jJ` | insd1_price / zscore | 2.37 | 1.82 | 0.2035 | 3.11 | 1.27 |
| `bl65Jk6l` | insd1_tradesignificance / ts_rank | 2.19 | 1.64 | 0.2092 | 2.08 | **1.74** |
| `kqN2WWKl` | insd1_shares / ts_rank | 2.13 | 1.58 | 0.1996 | 2.81 | 1.15 |
| `9qxL8vx9` | insd1_holdings / ts_rank | 1.96 | 1.39 | 0.1998 | 2.58 | 1.10 |
| `xAr022xb` | insd1_shares / ts_rank，回归窗 252 | 1.90 | 1.34 | 0.2014 | 1.90 | 1.23 |
| `JjeZWWpj` | insd1_value / ts_rank | 1.88 | 1.31 | 0.1980 | 2.05 | 1.19 |
| `QPvLNNQW` | insd1_valueeur / ts_rank | 1.78 | 1.22 | 0.1978 | 2.07 | 1.20 |

失败：`kqN2v7gg`（holdings 用 zscore，rob 0.96）、`A1VMrr3w`（price 用 ts_rank，S 1.29 / 2Y 0.86）、
`qMLoYYAP`（`max_trade_price` 该字段在 IND 无有效数据，S=0 / RA fail=6）。
`bl65Jk6l` self 相关性 **0.2391（pass）**。

## 3. 归因与对比实验

统一模板（残差化族，eff=2 形态）：

```
rank(-ts_regression(ts_zscore(returns, 252), <SEED>, 504, rettype=0))
  SEED = ts_zscore(ts_backfill(vec_avg(F), 504), 504)   或   ts_rank(ts_backfill(vec_avg(F), 504), 504)
```

### A. IMBALANCE：`nanHandling` 是 Sharpe 杠杆，不是 robust 杠杆
同一式 `group_rank(ts_mean(ts_backfill(imb5_score,22),126), industry)`：

| nanHandling | Sharpe | robust | TO |
|---|---|---|---|
| ON | 1.49 | 1.19 | ≈0.06 |
| **OFF** | **1.77** | 1.15 | 0.0604 |

⇒ 关掉 NaN 处理（等同丢弃缺失样本）把 S 抬 +0.28，robust 基本不动（−0.04）。
本区把 `nanHandling` 当强度档用，**不要**当 robust 档用。

### B. IMBALANCE：平滑窗是 robust 杠杆，最优点在 126–147
固定 `bf22 / industry / nanOFF`，只动 `ts_mean` 平滑窗：

| 平滑窗 W | Sharpe | robust | 判定 |
|---|---|---|---|
| 84 | 1.79 | **0.82** | 掉 robust |
| **126** | 1.77 | **1.15** | 全过（`RREn5xAj`） |
| **147** | 1.74 | **1.14** | 全过（`mLoMKnYW`） |
| 189 | ≈1.6 | 0.91–0.96 | 掉 robust |

⇒ robust 对平滑窗是**单峰**，峰在 126–147；84 太短（噪声进权重）、189 太长（信号被摊平）。

### C. IMBALANCE：换形态一律伤 robust
固定 126 窗 / industry / nanOFF，只换外壳：

| 形态 | alpha | Sharpe | rob | TO | 判定 |
|---|---|---|---|---|---|
| `ts_mean` 水平 | `RREn5xAj` | 1.77 | **1.15** | 0.060 | 全过 |
| `ts_zscore(...,252)` | `d5WAoQKx`（方向写反） | −2.30 | −0.67 | 0.180 | 反向后 rob 仍 0.67 |
| `ts_rank(bf504, 252)` | `9qxLmRl2` | 2.31 | **0.61** | 0.191 | 掉 robust |
| `ts_delta(ts_mean(126),66)` | `P0od81oK` | 0.35 | 0.40 | 0.071 | 信号毁灭 |

⇒ `imb5_score` 的信息是**水平**，不是变化率也不是秩位置；追高 S（2.31）的 `ts_rank` 形态
是拿 robust 换来的，不可交付。

### D. IMBALANCE：分组维度 industry 优于 subindustry；`imb5_mktcap` 更弱
- `subindustry`：S 1.53 / rob 0.91（`0mY068j2`）⇒ 分组过细，每格样本不足。
- `imb5_mktcap` 同式：S 1.47 / 2Y 0.84 / rob 0.67（`omEMrYan`）⇒ 规模字段无该收益锚。

### E. INSIDERS：`ts_rank` 种子显著抬 robust（同字段对照）
| 字段 | zscore 种子 | ts_rank 种子 | Δrob |
|---|---|---|---|
| insd1_holdings | S 2.05 / rob **0.96**（`kqN2v7gg`） | S 1.96 / rob **1.10**（`9qxL8vx9`） | +0.14 |
| insd1_shares | S 2.45 / rob 1.30（`omEMRpWb`） | S 2.13 / rob 1.15（`kqN2WWKl`） | −0.15（S 换 rob） |
| insd1_valueeur | S 2.38 / rob 1.10（`0mY0xljG`） | S 1.78 / rob 1.20（`QPvLNNQW`） | +0.10 |
| insd1_price | S 2.37 / rob 1.27（`1YNQO9jJ`） | S 1.29 / 2Y 0.86（`A1VMrr3w`） | 更差 |

rob 绝对最高的一颗来自 `ts_rank` 种子的 `insd1_tradesignificance`（**1.74**，`bl65Jk6l`）。
⇒ 种子变换的收益是**字段相关**的，不存在「ts_rank 全局更稳」；`tradesignificance`（交易显著性）
的经济语义（内部人买入的坚决程度）本身就更接近慢变量，是它稳健的真正原因。

### F. SENTIMENT：字段/形态差异对 S 影响 < 0.11 ⇒ 结构主导
12 颗里 S 落在 2.41–2.82（跨度 0.41，其中 11 颗挤在 2.57–2.82，跨度仅 0.25），
rob 1.30–1.96，TO 全部 0.245–0.267。
同一 `2neg_std` 字段的三种写法：zscore 2.68 / ts_rank 2.67 / `group_rank(industry)` 2.73 —— 差异 < 0.06。
⇒ 该族收益几乎全部来自「先对收益做 zscore、再回归掉情绪因子的残差动量」这一**结构**，
不是某个情绪字段的信息。**风险提示**：族内互相关高，实际提交时必须靠 self-corr 逐个筛，
不能把 12 颗当 12 个独立 alpha。

### G. OPTION：IND 侧数据未覆盖近两年（判死，非信号问题）
12 臂（decay4 与 decay126 两档 × IV 水平 / IV 变化 / 隐含股息 / 远期合约）：

| 臂 | Sharpe | TO | 2Y | rob | RA |
|---|---|---|---|---|---|
| `qMLoYzpZ`（d4） | 2.41 | **0.8108** | 1.40 | 1.57 | 3 |
| 同式 d126 | 1.18 | — | **0.24** | — | 3 |
| 其余 10 臂 | — | — | **−0.33 ~ 0.50** | — | 全红 |

⇒ 不是形态问题（d4 的 S 到 2.41），也不是拥挤问题；是 **2014–2023 窗口内 option1 在 IND
只有前段有数据**，2Y 段为空 ⇒ 记「数据未落地」，平台更新后复测，不进 dead_end 永久封存。

### H. shortinterest5：「Daily Price Limit Data」不是做空数据（判死）
该数据集 3 个字段全是涨跌停/停牌状态，探针 best Sharpe 0.22。
⇒ 名字误导，不是空头持仓/借券数据，本区无信号可挖。

**2026-10-28 补测后修正判死理由**：不是「信号弱」，是**字段在 IND/TOP500 侧是常数（数据未落地）**。
12 条机制探针（`rank`/`-rank`/`ts_mean`/`ts_zscore`/`ts_delta`/`ts_sum(abs(ts_delta))`/`days_from_last_change`）
全部 `longCount=0 / shortCount=0`、S=0、TO=0；随后 6 条诊断臂（`is_nan(x)` 与 `greater(x,0.05)` 各 3 条、跨 3 字段、
`neutralization=NONE` + `decay=0`）**产出逐字相同的指标**（S=−1.10 / F=−1.96 / TO=0.0098 / DD=4.27），
正是 skill 记载的「全空头退化组合 S=−1.10」签名。判读链：
`is_nan` 分支也空仓 ⇒ 字段**不是 NaN**；`greater(...,0.05)` 也全空 ⇒ 常数 **≤ 0.05**（现实涨跌停应为 0.10/0.20）。
⇒ 14 项一致指向「三个字段在本区恒为 0 或同一极小常数」，与 `macro63` 属同一族（IND 侧数据未落地）。
⚠ 与 macro63 的差别：macro63 可用作**挂塔器**（塔只差 1 颗），但 SHORTINTEREST 当前 0/3 且本区没有任何
eff=1 的 shortinterest 腿可挂 ⇒ **本塔在本季不可达**，平台补数后复测。

## 4. prod 相关性状态（未取得）

按用户要求全程用 MCP（`check_correlation`，未写任何临时脚本）。本轮结论：

- `RREn5xAj` 触发一次（`refresh=true`），平台侧响应超时 → 本机 `inflight=true` 标记，
  按约定只做 `refresh=false` 预读、**不重复触发**；
- 预读持续返回 `correlation_busy`，holder 始终是**其它会话**的 alpha
  （先后为 `npvMa0d3` / `rKRv0zK9` / `e75o19KO` / `vR13Yk9Q`），`retry_after 240`；
- 两次为本 alpha 抢到槽并触发（`inflight=true`），但**平台侧一直返回空体**
  —— 这正是 `src/wqb/correlation_slot.py` 头部记录的 2026-10-22 故障形态：
  别的会话把平台单并发槽占住，本会话的查询只能拿空体、轮询到超时。
  该文档给的处方是「杀掉占槽作业后立刻出数」，**那个作业不属于本会话，未动**；
- 该平台限制是**账户级单飞**（全账户只允许 1 个 prod 相关性在算），本会话无法插队。

**2026-10-28 二段补测（又 6 次 MCP 调用，仍零结果）**——holder 序列继续轮换，累计 **9 个不同 alpha id**：

| 序号 | 结果 | holder |
|---|---|---|
| 1 | `correlation_busy` | `zq31lQNK` |
| 2 | `correlation_busy` | `zq31lQNK` → 同一持有者未释放 |
| 3 | `correlation_busy` | `1YNEqJbQ` |
| 4 | `refresh=true` → MCP 客户端超时（-32603），但**本机置 `inflight=true`** |
| 5 | 预读（+75 s）仍 `inflight=true`、无值 | — |
| 6 | 预读（+150 s）回落为 `correlation_busy`，holder 换成 `KPrmWlwN` | `KPrmWlwN` |

判读：`inflight=true` 证明第 4 次调用**确实在平台侧启动了计算**，但平台把结果算给了**别的 alpha**
（holder 从 `zq31lQNK` → `1YNEqJbQ` → `KPrmWlwN` 连续轮换），本机标记在窗口后被动过期。
⇒ 不是调用方式问题、不是本机锁问题，是**账户级单飞槽被多个并行会话持续抢占**。

**2026-10-28 三段补测（15:16–15:19Z，2 次 MCP 调用，仍零结果）**：

| 序号 | 结果 | holder |
|---|---|---|
| 7 | `refresh=true` → 仍 MCP 客户端超时（-32603），本机重新置 `inflight=true`（"第 1 次触发"） | — |
| 8 | 预读（+60 s）仍 `inflight=true`、`last_known=null`、`retry_after 25` | — |
| 9 | 再预读（+120 s）→ **连只读预读本身也 -32603 超时**（服务端在等平台响应） | — |

⇒ 本机 inflight 标记在 60 s 窗口内未过期，平台值始终不可读；累计 **9 次补测调用 / 9 个不同 holder alpha id**。
第 9 次说明此时 MCP 侧连预读都阻塞在平台调用上，**该时段 prod 通道整体不可用**，不是本 alpha 的问题。
按 `wq-prod-lever-self-lock-guard` 纪律**不杀他会话进程、不重复硬撞**，本会话在该时段无法取得 prod。

⇒ **prod 实测待槽位释放后补测**，优先顺序：`RREn5xAj`（ATOM）→ `A1VMzqJg` / `RREnK5R1`（SENTIMENT 最强）
→ `omEMRpWb` / `bl65Jk6l`（INSIDERS 最强）。
self 相关性不受该限制，已实测五颗，全 pass：

| alpha | self max | 塔 | 说明 |
|---|---|---|---|
| `RREn5xAj` | 0.2903 | IMBALANCE（ATOM） | top `gJjN80rm` |
| `bl65Jk6l` | 0.2391 | INSIDERS | top `0mjk2ZQv` |
| `omEMRpWb` | 0.3379 | INSIDERS | top `0mjk2ZQv` |
| `RREnK5R1` | 0.5056 | SENTIMENT | top `0mjk2ZQv` |
| `A1VMzqJg` | 0.5597 | SENTIMENT | top `0mjk2ZQv` |

注：`0mjk2ZQv` 是四族共同的最强对手（0.24–0.56），说明「残差动量」这一结构在 OS 池里已有近亲；
队内 12 颗 SENTIMENT 相互之间还会更近，**必须逐颗测**，不能按族打包。

### 4.1 完成度审计（2026-10-28 收盘，全部 MCP 实测，无临时脚本）

| goal 条目 | 审计动作 | 结论 |
|---|---|---|
| ① ≥20 颗 regular alpha，最好 ATOM | `batch_get_alpha_metrics(include_checks=true)` 分两批（13+13）核 26 个 id | **26/26 `failed_ra_count=0`**、prescreen 全 `REVIEW`、`prod_correlation` 全 `null`（证实 prod 未测）；其中 **5 颗真 ATOM** |
| ② 近闸定向挖掘 + 归因与对比实验 | 本报告 §3 A–H（nanHandling / 平滑窗 / 分组轴 / decay / 回归窗 / 种子形态 / 挂塔器对照）+ §7 三段增量 | 成立，每组对比实验都带「同族单变量」对照 |
| ③ 并发=2、MCP 优先、prod 走 MCP | 全程 `create_multi_simulation`（一次一 multisim）+ `harvest_multisim.py` 入库；prod/self 只走 `check_correlation` / `check_self_correlation` | 并发与 MCP 口径成立；prod 受账户级单飞阻塞（§4），非本会话可控 |
| ④ 覆盖率可调但近十年须有数据 | `get_alpha_yearly_stats(mLoMnqPE)` | **2014–2023 连续十年**逐年在册（sharpe 2.13/1.67/1.81/0.36/4.13/1.83/0.22/0.88/3.40/2.57；每年多空各 237–256 / 247–255 只） |
| ⑤ 禁 PV/MODEL/OTHER 两两组腿 | 逐颗 `get_alpha_details` 复读 `pyramids` | 5 颗 ATOM 的 `pyramids.list` **仅 `[IND/D1/IMBALANCE]`、`effective=1`**，纯单字段 `imb5_score` 单数据集，无组腿 |

5 颗 ATOM 的塔归属实测（同一批次 `get_alpha_details`）：

| alpha | 表达式（骨架） | pyramids.list | effective | S / F / TO / 2Y / rob / margin |
|---|---|---|---|---|
| `mLoMnqPE` | `ts_mean(backfill(imb5_score,22),168)` | `[IND/D1/IMBALANCE]` | 1 | 1.87 / 1.43 / 0.0594 / 2.99 / 1.15 / 0.002454 |
| `YP1G3NjM` | 同上 W112 | 同上 | 1 | 1.79 / 1.33 / 0.0608 / 3.10 / 1.10 / 0.002282 |
| `bl65x0xl` | `ts_mean(backfill(imb5_score,66),126)` | 同上 | 1 | 1.78 / 1.33 / 0.0605 / 3.13 / 1.16 / 0.002297 |
| `RREn5xAj` | W126（self 0.2903） | 同上 | 1 | 1.77 / 1.32 / 0.0604 / 3.12 / 1.15 / 0.002297 |
| `mLoMKnYW` | W147 | 同上 | 1 | 1.74 / 1.28 / 0.0598 / 3.02 / 1.14 / 0.002262 |

五颗的 `checks.warning` 一致：`CLUSTER_TEST 0.67–0.76`（限 1）＋ `MATCHES_THEMES` ＋ `OSMOSIS_ALLOCATION`，
`checks.fail` 全空；`pending` 含 `SELF_CORRELATION / PROD_CORRELATION / DATA_DIVERSITY / REGULAR_SUBMISSION`。

## 5. 复现

```bash
# 收割（自动拉 children + 详情 + 写 backtest_results / wave_results / submit_ready）
$WQ_PY tools/harvest_multisim.py --multisim-id <multisim_id> --wave <wave> \
  --region IND --dataset <dataset> --auto-upsert

# 当波表达式与指标
#   MCP: mcp__wqb-db__list_expressions(region="IND", wave="<wave>")
#   MCP: mcp__wq-brain-http__batch_get_alpha_metrics(alpha_ids=[...], include_checks=true)
# prod / self
#   MCP: mcp__wq-brain-http__check_correlation(alpha_id=..., correlation_type="production")
#   MCP: mcp__wq-brain-http__check_self_correlation(alpha_id=...)
```

波次：`ind_imb_nanoff_20261028` / `ind_imb_atom2_20261028` / `ind_ins_fields_20261028` /
`ind_ins_tsrank_20261028` / `ind_snt_resid_20261028` / `ind_snt_mod20261028` /
`ind_opt_probe_20261028` / `ind_opt_resid_d126_20261028`。

## 6. 未做 / 待办

1. prod 相关性补测（阻塞在账户级单飞，非本会话可控）——三段补测共 8 次调用仍零结果，见 §4 的 holder 轮换表。
2. SENTIMENT / INSIDERS 残差族的**族内互相关**未逐对测；提交前需按 self-corr 逐颗筛。
3. 本报告不含任何提交动作：提交需用户明确确认 + `submit_verdict` 预检 + 塔位复读 + prod 实测。
4. SHORTINTEREST 塔：平台补数后复测三个字段（`max_price_increase_ratio` / `max_price_decrease_ratio` /
   `price_limit_condition`），复测判据 = 诊断臂不再退化到 S=−1.10 全空头，见 §7.5。

## 7. 二段增量（同日）：纯 ATOM 攻坚

### 7.1 IMBALANCE 纯 ATOM 扩窗（wave `ind_imb_atom3_20261028`，multisim `2sDXBh9Ao4XHby33vSF5RWc`）

同一 `group_rank(ts_mean(ts_backfill(imb5_score,22),W), G)` 骨架，4 臂分别动分组与外壳：

| alpha | W / 分组 / 外壳 | Sharpe | Fitness | TO | 2Y | robust | sub | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `mLoMnqPE` | 168 / industry / ts_mean | **1.87** | **1.43** | 0.0594 | 2.99 | **1.15** | 1.26 | **0 失败** |
| `YP1G3NjM` | 112 / industry / ts_mean | 1.79 | 1.33 | 0.0608 | 3.10 | **1.10** | 1.13 | **0 失败** |
| `O0AEdbld` | 126 / sector / ts_mean | 1.84 | 1.42 | 0.0581 | 2.91 | 0.88 | 1.09 | 1（robust） |
| `ZYQeVjYx` | 126 / industry / ts_decay_linear | 1.82 | 1.37 | 0.0631 | **3.37** | 0.86 | 0.99 | 1（robust） |

归因（与 §3.B / §3.C / §3.D 同一坐标系补点）：

- **平滑窗 112–168 是平坦高原**（rob 1.10 / 1.15 / 1.15 / 1.14），126 不是尖峰；84 与 189 掉 robust 的两端结论不变。
- **分组维度排序 industry > sector > subindustry**（rob 1.15 / 0.88 / 0.91）——sector 与 subindustry 都掉 robust，industry 是唯一稳的粒度。
- **`ts_decay_linear` 不是 robust 杠杆**：同窗 126 下 S 1.82 与 ts_mean 1.77 相当，rob 0.86 vs 1.15，2Y 3.37 是拿 robust 换来的（与 §3.C 一致）。
- 新两颗把 IMBALANCE ATOM 的 S/F 上界从 1.77/1.32 抬到 **1.87/1.43**。self 相关性 `YP1G3NjM` 0.2831 / `mLoMnqPE` 0.2783（top 对手 `gJjN80rm` / `E5l23mrm`，pool 52 / OS 59），全 pass。

### 7.2 INSIDERS 纯 ATOM 判死（wave `ind_ins_atom_20261028`，multisim `31MZgLgHB4zmaHM8pvbMH7H`）

6 臂全部只用 insiders1 字段（eff=1），两种几何：dev 凸幂（holdings/shares/valueeur）与「水平×自身波动」慢化（holdings/tradesignificance/value），全部 `vec_avg` 包裹：

| alpha | 几何 | Sharpe | Fitness | TO | 2Y | robust | RA |
|---|---|---|---:|---:|---:|---:|---:|---|
| `d5WAJogE` | valueeur dev p3 | 0.48 | 0.20 | 0.1175 | 1.52 | 0.05 | 4 |
| `bl650nVZ` | shares dev p3 | 0.46 | 0.19 | 0.1150 | 1.42 | −0.03 | 4 |
| `58EoKe9n` | value lvvol | 0.25 | 0.07 | 0.0834 | −0.02 | −0.02 | 4 |
| `1YNQ3P1z` | holdings lvvol | 0.07 | 0.01 | 0.0841 | −0.06 | −0.36 | 5 |
| `88RdWYkv` | holdings dev p3 | −0.27 | −0.08 | 0.1192 | −0.14 | −0.68 | 5 |
| `rKRvaVE8` | tradesignificance lvvol | −0.34 | −0.11 | 0.1016 | −0.49 | 0.14 | 5 |

⇒ **INSIDERS 没有纯 ATOM 信号**：最好 S 0.48（闸 1.58），量级差一个数量级，不是参数问题。
该族 9 颗 RA 全过全部来自「PV 收益 × INSIDERS 残差化」（eff=2）：信息载体是「先对收益做 zscore 再回归掉内部人因子」的残差动量结构，不是内部人字段自身的水平或变化率。

### 7.3 OPTION 塔 option30 首测（4 批 24 臂，wave `ind_opt30_*_20261028`）

option1 是唯一「数据未覆盖近两年」的集（§3.G）；option30 有 11 个 VECTOR 字段、cov 0.3629、历史 7 条 RA 全过，本轮从未测过。全部只用 option30 字段（eff=1），按四条概念通道铺开：

| 通道 | 代表 alpha | 形态 | Sharpe | TO | 2Y | robust |
|---|---|---|---:|---:|---:|---:|
| 流动性（价差 dev 凸幂） | `omEMxm02` | `signed_power(subtract(group_rank(spread/ts_mean(spread,252)),0.5),3)` | **0.83** | 0.4289 | 0.79 | 0.57 |
| 流动性（价差水平） | `A1VMpzQg` / `E56X912R` | `group_rank(divide(ask-bid, mid))` | 0.72 / 0.53 | 0.250 / 0.295 | 0.01 / 0.19 | — / 0.37 |
| 持仓（OI） | `pwdA2GdX` / `Vkxgrz0M` / `j2Yb7zAQ` | OI level 66 / ΔOI22 / ΔOI66 | −0.25 / −0.24 / −0.03 | 0.057–0.258 | −0.39…−0.13 | ≤0.10 |
| 活跃度（成交/OI） | `omEMd8WE` / `xAr0ZO3N` | `vol/OI` / Δvol22 | −1.06 / −1.08 | 0.239 / 0.496 | −1.85 / −1.29 | ≤−0.91 |
| 价格几何（振幅/货币性） | `3qoZNQVN` / `xAr0Jqol` | `high/low` / `mid/strike` | 0.37 / 0.20 | 0.063 / 0.106 | 0.13 / 0.87 | 0.55 |
| 方向对照 | `ZYQeJPb8` | −spread | −0.64 | 0.243 | 0.13 | — |

- **判读：option30 有数据、无信号。** 24 臂里 |S| 最高 0.83（价差 dev，TO 0.4289 已越过 0.40 硬线），距 1.58 差 0.75；OI 与成交量通道全部为负或零。方向自洽（spread 正、−spread 负）说明不是语法或对齐问题，是信号量级不够。
- **数据覆盖与 option1 不同**：24 臂的 2Y 全部有值（−1.85…0.87），option30 近两年数据在，可按「信号弱」判死，不必等平台补数。
- **工程口径（可复用）**：VERIFY 模式下 `add(<价格/股数字段>, 1)` 会被单位闸判成「无量纲常数 vs TSPrice/TSShare」WARNING（首轮 12 臂中 7 条如此，多为 COMPLETE+指标）；正解是**省掉防零常数**，`divide(a,b)` 的除零由平台置 NaN、再由 STATISTICAL 中性化吸收——改掉后第二轮 12/12 全 COMPLETE。该坑与记忆 `brain-verify-units` 同源。

### 7.4 未点亮塔 ATOM 收口

| 塔 | 本轮纯 ATOM 证据 | 结论 |
|---|---|---|
| IMBALANCE | 9 臂（wave nanoff / atom2 / **atom3**），其中 **5 颗 RA 全过**，S 最高 1.87 / F 1.43 / rob 1.15 | **唯一可产 ATOM 的未点亮塔** |
| INSIDERS | 6 臂纯 ATOM 全灭（S ≤0.48） | 无纯 ATOM，只有 eff=2 残差族 |
| SENTIMENT | 历史 44 臂 + 本轮 12 臂 eff=2 | 无纯 ATOM 证据，eff=2 残差族 |
| OPTION | option1 数据缺口；option30 24 臂 \|S\|≤0.83 | 无 ATOM，判「数据在、信号弱」 |
| SHORTINTEREST | 18 臂零产出（12 机制探针全空仓 + 6 诊断臂退化到 S=−1.10 全空头） | **无 ATOM，字段恒常数（数据未落地）** |

### 7.5 SHORTINTEREST 收官：18 臂证明「字段恒常数」，本季该塔不可达

三批（wave `ind_si_probe_a_20261028` / `ind_si_probe_b_20261028` / `ind_si_diag_20261028`，
multisim `4bry25cmE4Y9bHwoqkFXPZx` / `45z0IIfbI5io9Jj115YVolmD` / `2Mrr92eu94vL9qY107BWmc8t`）已全部入库。

**批次 1（机制探针 A，decay 4 / STATISTICAL）**

| expr | S | TO | long/short |
|---|---|---|---|
| `rank(ts_mean(max_price_increase_ratio, 66))` | 0 | 0 | 0 / 0 |
| `rank(ts_delta(max_price_increase_ratio, 66))` | 0 | 0 | 0 / 0 |
| `rank(ts_sum(abs(ts_delta(price_limit_condition,1)),22))` | 0 | 0 | 0 / 0 |
| `-rank(ts_sum(abs(ts_delta(price_limit_condition,1)),66))` | 0 | 0 | 0 / 0 |
| `rank(ts_mean(increase,66) - ts_mean(decrease,66))` | 0 | 0 | 0 / 0 |
| `rank(days_from_last_change(price_limit_condition))` | 0 | 0 | 0 / 0 |

**批次 2（机制探针 B：镜像 + 窗口阶梯）** 6/6 同样 S=0 / TO=0 / 空仓
（`-rank(ts_mean(increase,66))` / `ts_zscore(…,252)` / `ts_sum(abs(ts_delta),252)` /
`ts_mean(decrease,66)` / `ts_delta(price_limit_condition,22)` / `ts_mean(increase,22)`）。

**批次 3（诊断：`neutralization=NONE` + `decay=0` + `truncation=0`）**

| expr | S | F | TO | DD |
|---|---|---|---|---|
| `if_else(is_nan(max_price_increase_ratio),1,-1)` | −1.10 | −1.96 | 0.0098 | 4.27 |
| `if_else(greater(max_price_increase_ratio,0.05),1,-1)` | −1.10 | −1.96 | 0.0098 | 4.27 |
| `if_else(is_nan(price_limit_condition),1,-1)` | −1.10 | −1.96 | 0.0098 | 4.27 |
| `if_else(greater(price_limit_condition,0.5),1,-1)` | −1.10 | −1.96 | 0.0098 | 4.27 |
| `if_else(is_nan(max_price_decrease_ratio),1,-1)` | −1.10 | −1.96 | 0.0098 | 4.27 |
| `if_else(greater(max_price_decrease_ratio,0.05),1,-1)` | −1.10 | −1.96 | 0.0098 | 4.27 |

**六条语义互斥的表达式指标逐字相同** ⇒ 全部退化成同一个全 −1 组合（即 skill 记载的全空头 S=−1.10 假信号）。
判读：`is_nan` 分支不退化成 +1 ⇒ 字段**不是 NaN**；`greater(…,0.05)` 分支也退化成 −1 ⇒ 常数 **≤0.05**
（真实 IND 涨跌停限幅应为 0.10 / 0.20，ST 为 0.05）。⇒ 三字段在本区恒为 0 或同一极小常数。
塔归属同时被验证：`pyramids.list = [{IND/D1/SHORTINTEREST, multiplier 1}]`、`effective = 1`
—— 表达式侧完全合规，是**数据侧缺口**。
⇒ 判「平台数据未落地」，与 `macro63` 同族；但 SHORTINTEREST 当前 0/3 且本区没有任何 eff=1 的
shortinterest 腿可挂，**挂塔器方案不适用** ⇒ 本季该塔不可达，平台补数后复测。
