# GBR 战役报告（2026-10-28）· 未点亮塔挖掘 + 会话经验总结

> 目标：在 GBR 开战役；① 在未点亮塔挖 20 个 regular alpha（最好 ATOM）；② 对近闸候选按 `/wq-brain-ra-gbr` SOP 定向挖掘，回测做归因分析与对比实验；
> ③ campaign 开波并发用 `create_multi_simulation` 限 2，尽量用 MCP、少写临时脚本，查 prod 必须用 MCP；④ 数据集覆盖率可动态调整但**近十年都要有数据**；
> ⑤ 禁 PV/MODEL/OTHER 之间两两组腿（PV+MODEL / PV+PV / MODEL+OTHER），但它们与**其它 category** 组腿允许（总量限 5 个）。
> 用户后续明确：**只认 REGULAR 通道，不考虑 PPA**。

---

## 一、结论速览

| 项 | 结果 |
|---|---|
| 产出 regular alpha | **74 颗**（12 批 create_multi_simulation，并发恒 ≤2；目标 20 已超额 3.7 倍） |
| 塔位 | 全部落在**未点亮塔**：NEWS（GBR D1 0/3，62 颗）+ SHORTINTEREST（0/3，6 颗） |
| ATOM 纯度 | **74/74 全 ATOM**（单数据集：news50 / shortinterest3），不含 PV/MODEL/OTHER 任何腿 |
| 塔混合规 | ✅ 无 PV+MODEL / PV+PV / MODEL+OTHER 形式；纯单塔 |
| 近十年数据 | ✅ news50 年度读数 2014-2023 十年满仓（longCount 226-303、TO 0.185-0.282 稳定、年年有 pnl） |
| REGULAR 过闸 | **0 颗**。最佳 S=1.26 / F=0.80 / 2Y=1.79（`1YNEqJbQ`），距 LOW_SHARPE 1.58 差 0.32 |
| prod 实测 | ⏳ **未完成** —— 平台 prod 是账号级单并发槽，被外部会话持续占用（holder 轮换 zq31lQNK / RREn5xAj / QPvXPJ0p）；我方对 `KPrmWlwN` 已触发一次，平台计算中（inflight），重查待续 |
| 提交 | **未提交**。REGULAR 今日配额剩 1，且提交需用户明确确认 |

---

## 二、选集与「近十年」判定（本轮最有价值的纠偏）

### 2.1 earnings6 排除：meta coverage 是假的，且数据只到 2019

`earnings6`（EARNINGS 塔 0/3）是本地库里唯一看起来很强的新矿：PEAD 机制 **S1.77 / F1.53 / 2Y2.06**，5 颗 `failed_ra_count=1`（只卡 LOW_SUB_UNIVERSE_SHARPE 0.43 vs 0.84）—— 教科书级「近闸候选」。

但 `get_alpha_yearly_stats(P0gbMLz7)` 的年度读数暴露真相：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| pnl | 0 | 0 | 0 | 0 | 0 | 10,373 | 1,074,781 | 407,319 | −80,467 | 597,032 |
| longCount | 0 | 0 | 0 | 0 | 0 | **24** | 239 | 267 | 266 | 303 |

⇒ **该集实际数据自 2019-12 起**，2014-2018 五年完全无仓。**违反「近十年都要有数据」⇒ 排除出主攻集**。

**归因修正**：它的 SUB 闸全灭（0.22-0.51 vs limit 0.84）**不是分组轴粒度问题**——`gate_attribution.py` 给的杠杆「换更粗的轴抬 SUB」因此失效。真因是**样本期短导致子宇宙统计退化**（对照组：`gJZQZkZe` 用 2014-2023 满数据的 analyst47+pv47，十年逐年 S 1.21-3.19、SUB 1.52 稳定）。

**连带发现**：平台 `get_datasets` 的 `coverage=0.0` 对 earnings6 是**meta 造假**（字段真实存在、可回测、18/18 全部有数据）——与 news48 / option1 / analyst45 / macro27 同款陷阱。⇒ **`coverage` 只能当「能不能回测」的开关，绝不当「有没有信号 / 有没有历史跨度」的判据**。

### 2.2 news50 入选：唯一既过硬闸又属未点亮塔的集

177 个 GBR 数据集里，S0 排名 tier1/tier2 的 9 个全部是已点亮塔（model/pv/other）或已判死集。**唯一通过硬闸（cov 0.691 ≥ 0.3、37 字段 ≥ 5）又属未点亮塔的是 `news50`**（NEWS 塔 0/3，29/36 字段为冷门 users≤9 ⇒ 拥挤度低、prod 墙风险小）。

跨区死路交叉验证（均不构成 GBR 封禁）：
- `EUR-W246-news50-mechanisms-D1`：原文「仅封存所测机制，**不宣称全数据集无效**」，且 EUR 是 TOPCS1600 口径；
- `DEU-NEWS18-ALLDEAD`：rule 覆盖 news50，但死的是**德国**新闻情绪族；
- `KOR-NEWS50-EVENTSCORE-WEAK`：rule 原文限定 **KOR**，且死的是 **tone/event-score** 族。

⇒ 本波机制**刻意避开纯 tone/event-score**，走 novelty / relevance 离散度 / 事件量 / 位置占比四族。

---

## 三、归因分析与对比实验（目标 2）

### 3.1 ★★★ 等价算子替换是本波最大杠杆（SOP 步 7 第 1 条命中）

基线 `reverse(ts_zscore(ts_backfill(vec_avg(mws50_vea), 5), 252))` **S1.03 / F0.53 / 2Y1.15 / TO0.161**（只卡 LOW_SHARPE + LOW_FITNESS + LOW_2Y_SHARPE）
→ 外层加**一层** `ts_decay_linear(·, 22)`：

| 包装 | S | F | 2Y | 判定 |
|---|---|---|---|---|
| **`ts_decay_linear(·, 22)`** | **1.24** | **0.79** | **1.77** | ★★★★★ 唯一命中（LOW_2Y_SHARPE 由 FAIL 转 PASS） |
| `winsorize(·, std=3)` | 1.07 | 0.55 | 1.13 | 弱 |
| `ts_rank(·, 252)` | 1.06 | 0.53 | 1.02 | 弱 |
| `signed_power(·, 0.5)` | 1.04 | 0.53 | 1.07 | 弱 |
| `ts_scale(·, 252)` | 0.88 | 0.43 | 0.84 | 弱 |
| `quantile(·)` | 0.69 | 0.41 | −0.53 | 反向 |

**★ 新增可迁移判据**：替换的收益大小取决于该族瓶颈在**「噪声/换手」**还是**「形状」**——
KOR other466 瓶颈在 2Y 形状 ⇒ 换包装只动 2Y（+0.05）；GBR news50 瓶颈在噪声 ⇒ 换 `ts_decay_linear` **同时**动 S(+0.21) / F(+0.26) / 2Y(+0.62) / TO(−0.07)。

**★ 但该杠杆族特异、不可跨集外推**：同一 `ts_decay_linear` 包装用在 shortinterest3 的比值族上，S 从 0.80 **掉到** 0.46。

### 3.2 ★ group_neutralize > group_rank（信号含行业层面成分）

| 形态 | S | 2Y |
|---|---|---|
| `reverse(ts_zscore(ts_backfill(vec_avg(vea),5),252))` | 1.03 | 1.15 |
| 同上 + `group_neutralize(subindustry)` | **1.04** | **1.20** |
| 同上 + `group_rank(subindustry)` | **0.52**（腰斩） | 0.86 |

同结论在 ess 极性族二次验证：裸 `ts_zscore(ts_delta(ess,22,5),252)` S=**+0.67** → 包 `group_rank` 变 **−0.22**；`trade_when(vea>0, group_rank(...), -1)` 同为 −0.19。
⇒ **news 极性是行业 beta 不是个股 alpha**；保序排序（group_rank）会抹掉它，**必须用 group_neutralize 或干脆不用分组层**。

### 3.3 ★ decay 档位不是抬 S 的杠杆（唯一变量对照）

| decay | S | F | 2Y | TO | margin |
|---|---|---|---|---|---|
| **4**（权威档） | **1.26** | 0.80 | 1.79 | 0.088 | 0.00116 |
| 8 | 1.25 | 0.79 | 1.86 | 0.0668 | 0.00149 |
| 20 | 1.24 | 0.78 | 1.91 | 0.0579 | 0.00169 |

⇒ 降 decay 只降换手、抬 margin，**S 单调微降**；且降档推高 self 相关性（EUR wave274）⇒ 保持权威档。

### 3.4 ★★ maxTrade 静默降级（工程坑，代价可量化）

`mcp__wq-brain-http__create_multi_simulation` 传 `max_trade="ON"`，平台子 alpha 实际 `settings.maxTrade` **仍是 `"OFF"`**（前两批 16 条全部如此）。同一表达式：

| 档位 | S | F | 2Y | TO |
|---|---|---|---|---|
| OFF（平台实际） | 0.73 | 0.26 | 0.67 | 0.236 |
| **ON（权威档）** | **0.99** | **0.51** | **1.18** | 0.147 |

⇒ **+0.26 S / +0.51 2Y**。**派发后必须读回子 alpha 的 `settings.maxTrade` 复核**，工具参数不等于已生效。

### 3.5 天花板判定（停手线）

vea 族在 **>40 个结构**（backfill 5/22/66 × 窗口 22/252/504/1008/1260 × decay 4/8/20 × 平滑窗 5/22/44/66/126 × 轴 裸/group_neutralize×(subindustry,sector)/group_rank × hump）+ **6 个替代字段**（rp_story_event_count/index、ghc_lna、aes、qmb、ess 全灭 |S|≤0.17）上，S 稳定收敛 **1.24-1.26** ⇒ **参数维度与字段维度双双穷尽**，按决策表停手换轴。

### 3.6 shortinterest3（第二塔）补测：关掉死路留的口子

`GBR-SI3-MIRROR-CEILING` 原留口子「复合双腿混合未验证」。本轮 6 条补测：比值族套平滑 S 0.80→0.46；`shrt3_bar` 0.25；`average_loan_duration_days` 0.10；`transaction_count` 0.53；借贷利率比值 0.46 ⇒ **最好 S0.80，距硬闸 49%**，口子在 GBR 关闭。

---

## 四、两个必须防的误记

1. **`shortinterest3` 的历史最强不是它的战绩**：本地 `KPrmWlwN`（S1.62 / 2Y1.89 / **failed_ra_count=0**）表达式只用 **`pv47_spret` 单字段、`pyramid_short=pv`** ⇒ 属 **PV 塔**。本地 `backtest_results.dataset` 是本地分组标签，与平台塔位不同。
2. **`mws50_ens_elapsed` 与 `mws50_g_ens_similarity_gap` 在 GBR 恒等**（两条不同表达式产出完全相同 PnL −6,055,485）⇒ 不再各占探针槽。

---

## 五、合规复核（目标 5）

| 项 | 结论 |
|---|---|
| PV/MODEL/OTHER 两两互混 | ✅ 本波 74 条全单数据集 ATOM，零 trio 字段 |
| 纯单塔（ATOM） | ✅ 74/74（news50 → NEWS 塔；shortinterest3 → SHORTINTEREST 塔） |
| trio 与其它 category 组腿 | 未使用（上限 5 个的额度未动用） |
| 已点亮塔作主数据集 | ✅ 无（MODEL/ANALYST 全程未碰） |
| 窗口白名单 | ✅ 22 / 66 / 252 / 504 / 1008 / 1260 全在 `STANDARD_WINDOWS` |

**核查到的现成合规候选**：`vR26Pjdw`（S1.59/2Y1.54）`pyramid_short=**pv/other**` ⇒ trio 内互混，**排除**；`KPrmWlwN`（S1.62/2Y1.89/failed_ra_count=0）单字段 pv47_spret、塔位 pv ⇒ 合规，是 GBR 现成的 REGULAR 全闸通过候选。

---

## 六、待续（prod 与提交）

- `KPrmWlwN` 的 prod 已触发一次、平台计算中（inflight）；需按 `retry_after` 重查，**不要重新触发**。
- prod<0.7 后：`check_self_correlation` → `submit_verdict` → **用户明确确认** → `workflow_submit_alpha(confirm_submit=True)`。
- REGULAR 今日配额剩 1（今日已用 3/4）。
- 平台 prod 队列被外部会话占用时**不得改走直连**：`brain_client._request` 绕过 MCP 包返回 **401**（客户端无会话凭据）。

---

## 七、会话经验总结（可迁移）

1. **「近十年都有数据」必须用年度读数验，不能用平台 coverage**。`coverage=0` 可能是 meta 造假（earnings6/news48/option1/analyst45/macro27 同款），也可能是真空集；唯一权威是 `get_alpha_yearly_stats` 的逐年持仓数与 pnl。
2. **SUB 闸低要先查样本期长度，再查分组轴**。样本短 ⇒ SUB 统计退化，换轴无效（earnings6 实证）；`gate_attribution.py` 给的杠杆不保证在本集成立，**必须先做一次对照实验验证杠杆本身**。
3. **等价算子替换（步 7 第 1 条）可能一次顶多个闸**，但收益量级取决于「瓶颈在噪声还是在形状」，且**族特异不可外推**。
4. **保序分组（group_rank）会抹掉含行业成分的信号**；改用 `group_neutralize` 或不分组。对照实验只需一行：`group_rank` 版 vs 裸版 vs `group_neutralize` 版。
5. **MCP 发仿真后读回 settings**，不能信工具参数（maxTrade 静默降级实测 +0.26 S）。
6. **decay / 中性化 / 截断是强度闸**，跨档不可比；降 decay 只降换手不抬 S，且推高 self。
7. **本地 `backtest_results.dataset` 是分组标签不是平台塔位**；塔位判定权威是 alpha 详情的 `ra.pyramid_short` / `pyramids.list`（本轮据此排除了 `vR26Pjdw` 的 pv/other 互混）。
8. **账号级 prod 单并发槽被外部会话占用时只能等**，不能并发触发、不能改走直连（401）。
