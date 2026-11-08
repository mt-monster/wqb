# IND/GBR READY 池全量审计 + HKG fund_holdings_panel 判决（2026-11-06）

> 本条记录三件事：① `zq3zKgd8` 类型订正（SUPER，非 REGULAR，必须从候选池剔除）；
> ② IND READY 池 57 条全量筛完的结果；③ HKG `fund_holdings_panel` 四条探针判死。

## 一、★ 订正：`zq3zKgd8` 是 SUPER 不是 REGULAR

`get_alpha_details("zq3zKgd8")` 实读：

| 字段 | 值 |
|---|---|
| `type` | **SUPER** |
| `status` | UNSUBMITTED |
| `code` | 空串（combo 型，非表达式） |
| `settings.selectionHandling` | POSITIVE |
| `settings.selectionLimit` | 10 |
| `ra.failed_ra_count` | 0 |

⇒ 它是 SuperAlpha（selection + combo，选 10 个成分组合），**既不是 REGULAR 也不是 ATOM**。
用户硬约束「不考虑 PPA，只考虑 regular alpha 或者 ATOM」⇒ **必须从可提交清单剔除**。

**教训（跨区通用）**：`get_submit_ready` 返回的 `expr` 若是 `combo_a(alpha)` 或 `code` 为空串，
必须先 `get_alpha_details` 读 `type`；SUPER 件 S 再高也不能按 REGULAR 提交。
批量核对 11 颗其余候选：全部 `type=REGULAR` / `status=UNSUBMITTED` / `failed_ra_count=0` ✅。

## 二、IND READY 池 57 条全量筛完

方法：`get_submit_ready(region="IND")` → 按 S 降序 → 逐条 `check_self_correlation`（本地零额度）
→ self<0.7 的才进 prod 判定；已有 prod 值的直接判。

### 2.1 已全绿（self<0.7 + prod<0.7 + S≥1.58 + fRA=0 + REGULAR）

| alpha | S | F | TO | 2Y | self | prod | 骨架字段 | 塔组合 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `WjepYR7d` | 3.92 | 2.81 | 32.9% | 2.87 | 0.6562 | 0.6573 | mdl37_income + corr_last_trade | **PV+MODEL 违规** |
| `786wl6b8` | 3.86 | 2.57 | 37.2% | 2.40 | 0.6786 | 0.6897 | mdl37_news_count + corr_last_trade | **PV+MODEL 违规** |
| `d51z7PVw` | 3.26 | 2.40 | 28.9% | 2.16 | 0.6141 | 0.6141 | cap + oth532_emerging | **PV+OTHER 违规** |
| `E5VNe67L` | 3.20 | 2.52 | 25.0% | 3.00 | 0.6648 | 0.6643 | returns + inst_shares_disposed | PV × INSTITUTIONS |
| `Vkx9RbJV` | 3.14 | 2.08 | 30.4% | 2.37 | — | 0.6939 | returns + snt21_pos_mean | PV × SENTIMENT |
| `kqJkPLeO` | 3.02 | 2.40 | 22.5% | 2.36 | 0.4943 | 0.6177 | returns + anl44_eps_best | PV × ANALYST |
| `E567pmkK` | 2.93 | 1.81 | 33.9% | 2.60 | 0.4377 | 0.4924 | returns + ern3_pre_interval | PV × EARNINGS |
| `3qX6wLkP` | 2.84 | 1.74 | 34.5% | 2.41 | 0.5191 | 0.5836 | close/session + estimate_count | PV × ANALYST |
| `88vwZE17` | 2.46 | 1.73 | 23.7% | 2.60 | 0.5796 | 0.5788 | returns + aggregate_share_count | PV × INSTITUTIONS |
| `ZYQ5J7j1` | 2.40 | 1.51 | 36.7% | 2.54 | 0.4072 | 0.6693 | returns + imb5_mktcap | PV × IMBALANCE |
| `P0M6rzdx` | 2.34 | 1.47 | 30.2% | — | 0.5677 | 0.6856 | returns + volume + mcr63 | PV × MACRO |
| `2rA0e6MN` | 2.31 | 1.67 | 18.4% | 2.74 | 0.3251 | 0.4926 | returns + fnd90_game_rtn_vol | **PV+FUNDAMENTAL 违规** |
| `bl65Jk6l` | 2.19 | 1.64 | 20.9% | 2.08 | 0.4822 | 0.3464 | returns + insd1_tradesignificance | PV × INSIDERS |
| `RREn5rEa` | 2.08 | 1.54 | 19.8% | 2.45 | 0.4753 | 0.3342 | 同上 | PV × INSIDERS |
| `npvM6WvE` | 1.97 | 1.35 | 21.5% | 2.02 | 0.3785 | 0.3486 | 同上（ts_rank 版） | PV × INSIDERS |
| `MPYogx0L` | 1.87 | 1.31 | 20.3% | 2.20 | 0.4228 | 0.3159 | 同上（group_rank sector） | PV × INSIDERS |
| `58jPrvZ1` | 1.64 | 1.27 | 11.4% | 2.23 | 0.4843 | 0.5354 | mean_flash_estimate_ebt | **纯 ANALYST（ATOM）** |

### 2.2 self 通过、prod 未知（待测）

| alpha | S | F | TO | 2Y | self | 骨架 |
|---|---:|---:|---:|---:|---:|---|
| `N1eLRWML` | 2.98 | 2.25 | 24.4% | 2.80 | 0.6586 | inst_shares_disposed, market 中性化 |
| `d5WwzROj` | 2.97 | 1.80 | 36.2% | 2.70 | 0.4502 | ern3_pre_interval reverse |
| `Xg9Evajm` | 2.93 | 1.81 | 33.9% | 2.60 | 0.4377 | 与 `E567pmkK` 近重复（reverse 对照） |
| `kqNrvwA8` | 2.92 | 2.18 | 24.2% | 2.83 | 0.6973 | aggregate_equity_value/holders |
| `npAm2mGx` | 2.81 | 2.06 | 24.5% | 2.73 | 0.6531 | inst_shares_disposed ts_rank |
| `E5VNENMr` | 2.78 | 2.03 | 24.4% | 2.50 | 0.6954 | (buyers+sellers)/holders |
| `RRELleJ1` | 2.78 | 1.68 | 33.5% | 2.57 | 0.4559 | ern3_pre_interval |
| `RRELleJz` | 2.48 | 1.42 | 33.5% | 2.28 | 0.4848 | ern3_pre_interval 无 ts_zscore |
| `qMLZG6WP` | 2.48 | 1.42 | 33.5% | 2.28 | 0.4848 | 同上 reverse（近重复） |
| `ZYmgngv0` | 2.39 | 1.69 | 22.9% | 2.23 | 0.5431 | 机构买卖均价价差 |
| `QPYjrzLG` | 2.09 | 1.25 | 28.9% | **null** | 0.5662 | volume/adv20 + mcr63（2Y 缺数据） |
| `WjLvREMZ` | 1.60 | 1.22 | 10.6% | 2.23 | 0.5009 | flash_estimate_ebt |
| `78oe3d8Q` | 1.60 | 1.21 | 10.7% | 1.98 | 0.5067 | 同上 rank 版 |

### 2.3 self 拦下（14 条判死）

`xA392Xpb` 0.7011（超线 0.0011）/ `e7QG2WJM` 0.7081 / `gJWXMXNl` 0.7208 / `JjP0Ja5l` 0.7319
/ `npvRmKq3` 0.7462 / `2rj9L9ob` 0.7617 / `d5WAzegY` 0.7696 / `1YNQO9jJ` 0.7884 / `zq8jLYoG` 0.8136
/ `A1VMzqYg` 0.8232 / `d5bm6XYx` 0.8358 / `A1VMzqJg` 0.8540 / `0mX9bpeq` 0.8536 / `88RoVq6V` 0.9986
/ `zq8wZgQO` 0.9952 / `58EbwZeN` 0.9997 / `QPbjAJOp` 0.9753

**self 通过率 = 30/57 ≈ 53% ⇒ 确认 IND 是处女池**（DEU 对照仅 1/11）。

## 三、★ 真正的瓶颈是塔组合配额，不是 self/prod

IND 全池 57 条里约 30 条是 `institutions6` 主骨架：
`rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(X, 252), 252, rettype=0))`
⇒ 全部落在 **PV × INSTITUTIONS** 单个塔组合上，按「每个两塔组合候选 ≤3」直接封顶。

按配额重排后 IND 合规上限：

| 塔组合 | 已占 | 配额 | 余量 |
|---|---:|---:|---:|
| PV × INSTITUTIONS | 2 | 3 | **1** |
| PV × ANALYST | 2 | 3 | **1** |
| PV × INSIDERS | 4 | 3 | **超 1 ⇒ 砍 `MPYogx0L`(1.87)** |
| PV × EARNINGS | 1 | 3 | 2 |
| PV × SENTIMENT | 1 | 3 | 2 |
| PV × IMBALANCE | 1 | 3 | 2 |
| PV × MACRO | 1 | 3 | 2 |
| 纯 ANALYST（ATOM） | 1 | 不限 | 不限 |

⇒ 待测 prod 的三颗选择依据：`N1eLRWML`(2.98) 补 PV×INSTITUTIONS 第 3 颗；
`d5WwzROj`(2.97) 补 PV×EARNINGS 第 2 颗；`kqNrvwA8`(2.92) 为 PV×INSTITUTIONS 备选。

## 四、HKG `fund_holdings_panel` 判死

wave1 四条探针 2/2 + 2/2 全 COMPLETE，**全部归属 `HKG/D1/INSTITUTIONS`**（multiplier 1.4）：

| alpha | 构造 | S | F | TO | 2Y | sub | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `3qoGgeZP` | `group_rank(holder_account_total, subindustry)` | **0.42** | 0.24 | **1.65%** | **0.50** | **0.69** | 3 |
| `6XdGgevL` | `group_rank(vec_avg(boundary_transaction_total), subindustry)` | 0.28 | 0.09 | 28.7% | 0.39 | 0.59 | 3 |
| `E56moGeP` | `group_rank(vec_avg(security_transaction_usd_value), subindustry)` | 0.17 | 0.04 | 36.1% | 0.19 | 0.40 | 3 |
| `O0A6KGxR` | `group_rank(herfindahl_index_holdings, subindustry)` | −0.35 | −0.13 | **2.24%** | −0.04 | −0.14 | 4 |

判死依据：四个结构互异骨架（计数 / 边界交易额 / 交易额 / 集中度 HHI）|S| **全部 ≤ 0.42**，
距 HKG 的 1.58 线差 1.16 以上。TO 谱系落「慢变结构描述符」（1.65–2.24%）⇒ 按既有三档判据判死。

**唯一留用**：`3qoGgeZP`（holder_account_total，TO 1.65%，2Y 0.50，sub 0.69）——
sub/S = 1.64、2Y/S = 1.19，信号在各子宇宙上分布均匀 ⇒ 可作未来 2:1 配方的**冷腿**候选
（参照 `loaned_share_count_main` 504 长窗冷腿贡献 +0.8~1.09 Sharpe 的实证）。
但冷腿本身 |S| 需 ≥0.5 才有希望，0.42 偏低，列为最低优先级备选。

## 五、候选池现状（剔除 SUPER 与塔混违规后）

| # | alpha | 区/宇宙/中性化 | S | self | prod | 塔组合 |
|---|---|---|---:|---:|---:|---|
| 1 | `E5VNe67L` | IND/TOP500/STATISTICAL | 3.20 | 0.6648 | 0.6643 | PV×INSTITUTIONS |
| 2 | `Vkx9RbJV` | IND/TOP500/STATISTICAL | 3.14 | — | 0.6939 | PV×SENTIMENT |
| 3 | `kqJkPLeO` | IND/TOP500/STATISTICAL | 3.02 | 0.4943 | 0.6177 | PV×ANALYST |
| 4 | `E567pmkK` | IND/TOP500/STATISTICAL | 2.93 | 0.4377 | 0.4924 | PV×EARNINGS |
| 5 | `3qX6wLkP` | IND/TOP500/STATISTICAL | 2.84 | 0.5191 | 0.5836 | PV×ANALYST |
| 6 | `ZYQmolVx` | EUR/TOP2500/FAST/decay1 | 2.48 | 0.6884 | 0.6884 | OTHER×RISK×ANALYST |
| 7 | `88vwZE17` | IND/TOP500/STATISTICAL | 2.46 | 0.5796 | 0.5788 | PV×INSTITUTIONS |
| 8 | `ZYQ5J7j1` | IND/TOP500/STATISTICAL | 2.40 | 0.4072 | 0.6693 | PV×IMBALANCE |
| 9 | `P0M6rzdx` | IND/TOP500/STATISTICAL | 2.34 | 0.5677 | 0.6856 | PV×MACRO |
| 10 | `xArjE96W` | EUR/TOP2500/FAST/decay22 | 2.28 | 0.5893 | 0.5907 | OTHER×RISK×ANALYST |
| 11 | `bl65Jk6l` | IND/TOP500/STATISTICAL | 2.19 | 0.4822 | 0.3464 | PV×INSIDERS |
| 12 | `RREn5rEa` | IND/TOP500/STATISTICAL | 2.08 | 0.4753 | 0.3342 | PV×INSIDERS |
| 13 | `2rAlGNk6` | HKG/TOP800/SECTOR | 1.97 | 0.1794 | 0.5245 | **纯 PV（ATOM）** |
| 14 | `npvM6WvE` | IND/TOP500/STATISTICAL | 1.97 | 0.3785 | 0.3486 | PV×INSIDERS |
| 15 | `LLZ6wZO2` | KOR/TOP600/STATISTICAL | 1.99 | 0.6760 | 0.6762 | **纯 OTHER（ATOM）** |
| 16 | `P0g88dzW` | EUR/TOPCS1600/SUBINDUSTRY | 1.82 | 0.4504 | 0.5421 | FUNDAMENTAL×STATISTICAL |
| 17 | `A1QZYa1l` | EUR/TOPCS1600/INDUSTRY/decay40 | 1.81 | 0.5914 | 0.6073 | FUNDAMENTAL×RISK |
| 18 | `58jPrvZ1` | IND/TOP500/STATISTICAL | 1.64 | 0.4843 | 0.5354 | **纯 ANALYST（ATOM）** |

**剔除**：`zq3zKgd8`（SUPER）/ `WjepYR7d` `786wl6b8`（PV+MODEL）/ `d51z7PVw`（PV+OTHER）/
`2rA0e6MN`（PV+FUNDAMENTAL）/ `MPYogx0L`（PV×INSIDERS 超配额，且 S 最低）。

**18 颗合规候选**，其中 4 颗为纯单数据集 ATOM。

## 六、待用户裁决

1. 「集合内 × 集合外组合**类型**总量 ≤5」中的「类型」指**组合种类数**还是**候选条数**？
   当前已用 7 种（PV×INSTITUTIONS / ANALYST / SENTIMENT / EARNINGS / IMBALANCE / MACRO / INSIDERS），
   若按种类 ≤5 则须砍到 5 种（意味着放弃 2 类，损失约 3–5 颗候选）。
2. `WjepYR7d`(3.92) / `786wl6b8`(3.86) 是 IND 池最强两颗，但骨架是 PV+MODEL（禁混集合内两两）。
   是否确认永久弃用，还是允许作为历史存量破例提交？

## 七、GBR READY 池：31 条里已有 5 颗全绿（零额外汇总）

`get_submit_ready(region="GBR")` 直接带回了 `self` 与 `prod` 两个字段，
筛出**已同时满足 self<0.7 + prod<0.7 + S≥1.58 + fRA=0 的 5 颗**：

| alpha | S | F | TO | 2Y | self | prod | 骨架来源 |
|---|---:|---:|---:|---:|---:|---:|---|
| `d51O1kOX` | 1.97 | 1.29 | 8.1% | 1.71 | **0.1129** | 0.6793 | analyst7 `est_12m_pre_raisednum` |
| `blORMJwm` | 1.91 | 1.24 | 7.9% | 1.62 | **0.0623** | 0.6950 | analyst7 `est_12m_pre_raisednum_4wk` |
| `3qV7Q2dO` | 1.77 | 1.07 | 12.3% | null | 0.3669 | 0.6596 | predictive_starmine `smest_price_ratio_fy2_revenue_3` |
| `RR62bMje` | 1.67 | 1.02 | 12.6% | 1.86 | 0.6066 | 0.6573 | predictive_starmine `ep_yield_pct_smest_f12m` |
| `mL68wNOK` | 1.63 | 1.07 | 12.8% | null | 0.4979 | 0.6608 | model28 `sm_structural_multiple_credit_structural_leve` |

另有 `xAb2OkMm` S 2.13 / self 0.3689 / **prod 0.8338** ⇒ 早已判死深钉。

⇒ **教训**：`get_submit_ready` 的返回体本身就带 `self` / `prod` 字段，
有值的候选可以**零成本直接判定**，不必先跑 `check_self_correlation`。
派发前的第一步应是「先读回包里已有的 self/prod」，只对缺失的补测。

### 7.1 ★ 订正：`check_self_correlation` 不是纯本地计算

批量测 GBR 6 条时全部返回 `self: null`，原始返回体是：
`{"error": "429 Client Error: Too Many Requests for url: https://api.worldquantbrain.com/alphas/<id>"}`

⇒ 该工具**需要打平台接口拉 alpha 的 pnl**，会与其他任务抢账号级并发槽。
**判据**：`self: null` 必须区分「429 限流（可重试）」与「该 alpha 确实无 pnl 缓存」；
遇到 429 时不要重试、不要叠加，等占用槽位的后台任务结束后再补测。

## 八、塔位现状（`get_pyramid_alphas` 实读，塔内 ≥3 视为点亮）

| 区域/D1 | 已点亮塔 | 未点亮塔 | 未点亮数量 |
|---|---|---|---:|
| **HKG** | 无（pv 仅 1，未到 3） | analyst/earnings/fundamental/model/imbalance/insiders/institutions/macro/news/socialmedia/other/shortinterest/risk/sentiment | **14** |
| **GBR** | model(5) / news(3) / analyst(3) / fundamental(3) | earnings/institutions/insiders/risk/option/socialmedia/macro/shortinterest/imbalance/sentiment | **10** |
| **KOR** | shortinterest(4) / fundamental(3) / model(3) | analyst(2)/pv(2)/other(1)/earnings/imbalance/insiders/institutions/macro/news/socialmedia/risk/sentiment | 9 档未到 3 |
| **IND** | pv(11)/news(4)/other(4)/analyst(3)/model(3)/fundamental(3)/risk(3) | **imbalance(0) / option(0) / shortinterest(0)** | **3** |

⚠️ HKG 连 pv 都只有 1 ⇒ **HKG 实际一个塔都未点亮**；GBR 已点亮 4 个塔。

**IND 仅剩三个未点亮塔**，而候选池里的 `ZYQ5J7j1` 使用 `imb5_mktcap`（imbalance 塔），
`P0M6rzdx` 使用 `mcr63_membership`（macro 塔）⇒ 提交这两颗可直接点亮 IND/IMBALANCE 并推进 IND/MACRO。

## 九、并入后的完整候选池（25 颗）

在第六节 18 颗基础上新增：

| alpha | 区 | S | self | prod | 塔组合 | 备注 |
|---|---|---:|---:|---:|---|---|
| `KPmvEYeE` | IND | 3.07 | 0.6086 | 0.6162 | PV×INSTITUTIONS | 补齐该组合第 3 颗 |
| `JjQzbQJj` | IND | 3.09 | 0.5088 | **0.5658** | **PV+OTHER 违规** | 与 `d51z7PVw` 同类，弃用 |
| `d51O1kOX` | GBR | 1.97 | 0.1129 | 0.6793 | 待核 | analyst7 ATOM 候选 |
| `blORMJwm` | GBR | 1.91 | 0.0623 | 0.6950 | 待核 | 余量仅 0.005 |
| `3qV7Q2dO` | GBR | 1.77 | 0.3669 | 0.6596 | 待核 | 2Y null |
| `RR62bMje` | GBR | 1.67 | 0.6066 | 0.6573 | 待核 | |
| `mL68wNOK` | GBR | 1.63 | 0.4979 | 0.6608 | 待核 | 2Y null |

⇒ **25 颗合资格**（含 4 颗纯单数据集 ATOM：`2rAlGNk6` / `LLZ6wZO2` / `58jPrvZ1` + GBR analyst7 两颗）。
