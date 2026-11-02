# GLB 战役：三条单塔路径全灭 + 非 trio 双塔解锁（2026-11-02）

> 目标：GLB / delay 1 / MINVOL1M 挖 20 颗 REGULAR alpha（优先未点亮塔 / ATOM）
> 本轮核心：`kqNrmA9g` prod = **0.8677** ⇒ PV 单塔判死 ⇒ **三条单塔路径全部证伪**；
> 同时确认**非 trio × 非 trio 双塔组合不受「5 个组合名」上限约束**，20 颗算术解锁。

---

## 1. `kqNrmA9g`：全闸通过但 prod 0.8677 —— PV 单塔判死

```
-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 3), country)
```

设置：`MINVOL1M / d1 / decay=6 / FAST / trunc=0.05 / nanHandling=OFF / maxTrade=OFF / maxPosition=OFF`

| 指标 | 值 | 闸 |
|---|---|---|
| sharpe | **3.00** | ✅ |
| fitness | 1.40 | ✅ |
| turnover | 47.33% | ✅ |
| 2Y sharpe | 2.65 | ✅ |
| sub-universe | 1.74 | ✅ |
| returns / dd | 10.34% / 3.17% | ✅ |
| failed RA checks | **0**（12 项全 PASS） | ✅ |
| **prod correlation** | **0.8677** | ❌ |

**prod 直方图**：`n_total = 914,845`；`n[0.6,0.7) = 9`；`n[0.7,0.8) = 0`；`n[0.8,0.9) = 1`；`n[0.9,1.0) = 0`

⇒ **单钉子型（n=1）**，不是拥挤型。且 `n[0.7,0.8) = 0` —— 该区间没有任何生产 alpha，理论上"落到 0.71 就干净"，
但 n=1 说明 0.85–0.90 段被**单条**生产 alpha 独占，按 `wq-window-valley-break-prod-wall` 判据：**n≥1 ⇒ 调窗无效，直接弃族**。

### 覆盖核查（十年无空窗）

逐年 `longCount`：3946 / 4054 / 3895 / 4222 / 4633 / 4266 / 4417 / 5430 / 5208 / 4549（2014–2023）
逐年 sharpe：4.87 / 4.70 / 5.08 / 2.97 / 1.35 / 0.85 / 1.28 / 1.68 / 2.32 / 2.36（**全正**）

⇒ 数据层完全健康，**唯一失败点就是 prod**。这也排除了"晚起始字段/覆盖不足"的替代解释。

### 附带更正一条历史死路

`GLB-PVPRECLOSE-RECOMPUTE-2Y-KILL-20261027` 记录 PV pre_close 30m 族「天花板 S 2.05」。
本次证明**该天花板只对正向成立**：负号版 S 3.00、fRA 0、十年全覆盖。
⇒ **判死某族天花板时必须记录测试方向（sign）**；该族仍可作**门控腿**候选，不可作信号腿。

### ⇒ 三条单塔路径全部证伪（20 颗不能靠单塔补）

| 单塔路径 | 结论 | 证据 |
|---|---|---|
| OTHER 裸信号 | **死**（prod 地板 0.76） | 9 颗实测，最新 `9qxJgv5x` 0.7671 / n=76 重度拥挤 |
| ANALYST 单塔（ESG 年频） | **死**（指标层塌缩） | w168 **0/6**，六种结构模板 turnover 同为 9.2% |
| PV 单塔（pre_close 30m 负号） | **死**（prod 0.8677） | `kqNrmA9g`，本轮 |

已落库死路条目：`GLB-PV-SINGLE-TOWER-PROD-08677-20261102`（layer=dead_end, dead_at=2026-11-02）。

---

## 2. 战略解锁：非 trio × 非 trio 组合**不受 5 个组合名上限约束**

### 规则复述（以 2026-10-28「第三次澄清」为准）

- **禁止**：`{PV, MODEL, OTHER}` 三者间两两组腿（含 `PV+PV`）、三塔同现。
- **限 5 名**：**trio 塔 × 非 trio 数据集**（如 `PV+NEWS`）——这类组合名总量 ≤ 5。
- **只限 ≤3/组合**：不在上面两类里的组合（即**非 trio × 非 trio**）**允许**，唯一约束是每个两塔组合候选 ≤ 3。

### 为什么这条解开了 20 颗

现有 5 个 OTHER 系组合名已全部占满：`RISK+OTHER` / `FUND+OTHER` / `OTHER+SENT` / `EARNINGS+OTHER` / `INST+OTHER`。
若只能在这 5 名里加，两塔上限 = 5 × 3 = **15 颗**，减去已判死的 2 颗（`E5672lMG`、`6Xd8dgzL`）实际 ≤ **13 颗**。
既然三条单塔路径全灭，旧口径下 **20 颗在算术上不可能**。

而**非 trio × 非 trio 组合**（`EARNINGS+FUNDAMENTAL`、`ANALYST+NEWS`、`MACRO+INSIDERS`…）
不受 5 名上限约束，每个组合最多 3 颗，组合数不受限 ⇒ **容量不再是瓶颈**。

### 额外收益：一次点亮两座塔

塔位按 alpha 的 `pyramids.list` 逐塔计入（双塔件同时计入两座）。
GLB/D1 现有：`pv 2 / model 3 / other 3 / risk 1 / institutions 1`，其余 8 座 0，点亮门槛 = 3 颗/塔。
⇒ 一颗 `NEWS+ANALYST` 同时给 news 和 analyst 各 +1，**双塔效率是 OTHER 系组合的 2 倍**（OTHER 已亮，不产生边际塔位）。

---

## 3. 塔位账（按现存 7 颗活件全提交推算）

| 塔 | 现状 | 补件后 | 点亮？ |
|---|---|---|---|
| model | 3 | 3 | ✅ 已亮 |
| other | 3 | 10 | ✅ 已亮 |
| **pv** | 2 | ~~3~~ **2** | ❌ `kqNrmA9g` 判死 ⇒ 仍差 1 颗 |
| **risk** | 1 | **3** | ✅ 补亮（`QPvJ6KVw`+`npv9WLVE`） |
| **institutions** | 1 | **2** | ❌ 差 1 颗（`mLoqmkd5` 若过） |
| **fundamental** | 0 | **2** | ❌ 差 1 颗（`RRE3O8r1`+`d5WqeQbx`） |
| **sentiment** | 0 | **2** | ❌ 差 1 颗（`j2Yg2q9j`+`xArnqeAw` 若过） |
| earnings / analyst / news / macro / socialmedia / insiders | 0 | 0 | ❌ |

⇒ 剩余 6 个 OTHER 席位**正好**覆盖 institutions / fundamental / sentiment 三座塔各差的那 1 颗 + earnings 2 颗。

---

## 4. w169：门控发现扫描（已派发）

**核心判据（已实测）**：**门控腿选型是 prod 的第一决定因素**，信号腿与分组轴是次要因素。
同信号腿 `single_bucket_20day_..._2` @`country`：
- 门控 `fnd44_jones_cf_accruals` → prod **0.5846**
- 门控 `ern3_pre_interval` → prod **0.7204**
- 差 **0.1358**，只换门控字段。

所以本轮**固定信号腿、固定骨架、固定轴、固定设置，只换门控字段**——单变量 8 条。

- multisim：`2YUWfV4zg5jda1ezale`（location `/simulations/2YUWfV4zg5jda1ezagY7sLE`）
- 设置：`GLB / MINVOL1M / d1 / decay=10 / FAST / trunc=0.08 / nanHandling=OFF / maxTrade=OFF / maxPosition=OFF`
  （= `RRE3O8r1` / `d5WqeQbx` / `mLooqkd5` 共用、产出最稳的那一格）
- 统一骨架：
  ```
  trade_when(rank(ts_mean(<GATE>, 22)) > 0.7,
             signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5),
             0)
  ```

| # | 门控字段 | 数据集 | 类别 | 经济机制 | 目标席位 |
|---|---|---|---|---|---|
| 1 | `count_institutional_buyers_security` | institutions6 (cov 1.0) | INSTITUTIONS | 买方机构数 = 建仓广度 | INST+OTHER |
| 2 | `inst18_fundownershipv2_num_held` | institutions18 (cov 0.9547) | INSTITUTIONS | 持仓机构数 = 拥挤/覆盖 | INST+OTHER |
| 3 | `dividend_per_share_declared` | fundamental23 (cov 0.9579) | FUNDAMENTAL | 分红宣告 = 成熟价值型 | FUND+OTHER |
| 4 | `assets_total_2` | fundamental23 (cov 0.9603) | FUNDAMENTAL | 总资产 = 规模 | FUND+OTHER |
| 5 | `ern3_pre_reptime` | earnings3 (cov 0.9068) | EARNINGS | 上次报告时刻（盘前/盘后信息扩散） | EARNINGS+OTHER |
| 6 | `ern3_all_delay_1_pre_reptime` | earnings3 (cov 0.9067) | EARNINGS | 全市场统一报告时刻 | EARNINGS+OTHER |
| 7 | `snt22_2neg_conf_low_396` | sentiment22 (cov 1.0) | SENTIMENT | 负向低置信（= 不确定性） | OTHER+SENT |
| 8 | `snt22_5neg_mean_420` | sentiment22 (cov 1.0) | SENTIMENT | 负向情绪均值 | OTHER+SENT |

预检：**8/8 合法，0 未知字段**（`preflight_expressions`，零配额）。

**失败门控黑名单（组篮前必查）**：
`ern3_pre_interval` 0.7599 → 本轮复现 0.7204；`nws73_headlines` 0.8124；`rsk60_offer` 0.7954；
`snt21_2neg_conf_up` 0.754；`scl12_sentiment` 0.719。

**现有干净门控（4 个已全部用掉）**：
`fnd44_jones_cf_accruals` 0.5846、`fnd44_perc_accruals` 0.6479、`vec_avg(rsk60_crowding)` 0.6385/0.6638、
`snt21_2neg_conf_low_394` 0.6585。

---

## 5. 非 trio 候选池盘点（w170 的前置调研）

按 `field_profile_full`（GLB，cov ≥ 0.50）统计：

| 类别 | 最强数据集 | 字段数 | 平均覆盖 | ALIVE | 未测 | 备注 |
|---|---|---|---|---|---|---|
| **NEWS** | `news73` | 22 | **1.0** | **2** | 17 | `nws73_headlines` ALIVE S 2.46 / sub 2.43（但作**门控**实测 0.8124，只能作信号腿） |
| NEWS | `news31` | 44 | 0.826 | 1 | 36 | `delay_adjusted_relevance_score` S 2.09 但 2Y −0.40 |
| NEWS | `news7 / 20 / 48 / 46 / 76` | 35 / 23 / 19 / 14 / 6 | 0.87 / 0.88 / 0.92 / 0.90 / 1.0 | 0 | 大量 | 多为 VECTOR，需 `vec_*` |
| **ANALYST** | `analyst_consensus` | 1443 | 0.760 | 0 | 1288 | 池子最大 |
| ANALYST | `analyst10` | 167 | **0.973** | 0 | 156 | 高覆盖 |
| ANALYST | `analyst69 / 15 / 11` | 739 / 307 / 235 | 0.87 / 0.94 / 0.74 | 0 | 几乎全未测 | |
| MACRO | `macro27` | **13** | 0.702 | 0 | 5 | 字段太少，是硬约束 |
| SOCIALMEDIA | `socialmedia12` | **2** | 0.651 | 1 | 0 | 字段太少 |
| INSIDERS / SHORTINTEREST / IMBALANCE | — | 0（cov≥0.5 无字段） | — | — | — | 覆盖太低 |

⇒ **非 trio 双塔的现实主力 = `NEWS×ANALYST`**（两座都是 0，一次点亮两塔，池子最富）。
备选：`NEWS×FUNDAMENTAL`、`NEWS×EARNINGS`、`ANALYST×EARNINGS`（都是非 trio × 非 trio，合法）。

**待解决的前提问题**：非 trio 信号腿的 prod 相关性未知。OTHER 能过是因为
`dl_riskfree_returns`（图像模型预测）天然独立；NEWS/ANALYST 是大众数据，prod 可能偏高。
w170 必须以「非 trio 信号腿 × 非 trio 门控」做小批探针先验证 prod，再谈扩量。

---

## 6. 修订后的 20 颗算术

```
OTHER 系双塔（5 个组合名，已满）
  已确认 5 颗（prod < 0.7）：QPvJ6KVw 0.6385 / npv9WLVE 0.6638 / RRE3O8r1 0.6479
                              d5WqeQbx 0.5846 / j2Yg2q9j 0.6585
  prod 待回 2 颗：xArnqeAw / mLoqmkd5
  w169 门控扫描 8 条 → 期望补 4–6 席
  ⇒ OTHER 系可望 11–13 颗

非 trio 双塔（组合数不限，每个 ≤3）
  NEWS×ANALYST 做主攻（一次点亮 news + analyst 两座）
  其余 7–9 颗从这里出
  ⇒ 20 颗在算术上可达，前提是非 trio 信号腿能过 prod
```

**塔位可达集**（若 NEWS×ANALYST 成）：
other / model / risk / institutions / fundamental / sentiment / news / analyst = **8 座**，
pv 差 1、earnings / macro / socialmedia / insiders 需另配。

---

## 7. 提交授权（仍缺，最关键阻塞）

**confirmed 可提交库存 = 5 颗**，全部 prod < 0.7 且 fRA = 0：

| # | alpha | 塔组合 | S | F | TO | 2Y | sub | prod |
|---|---|---|---|---|---|---|---|---|
| 1 | `QPvJ6KVw` | RISK+OTHER | 3.19 | 1.59 | 28.97% | 3.43 | 1.84 | **0.6385** |
| 2 | `npv9WLVE` | RISK+OTHER | 3.08 | 1.42 | 60.83% | 3.19 | 2.38 | **0.6638** |
| 3 | `RRE3O8r1` | FUND+OTHER | 2.89 | 1.73 | 16.02% | 2.13 | 1.71 | **0.6479** |
| 4 | `d5WqeQbx` | FUND+OTHER | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | **0.5846** |
| 5 | `j2Yg2q9j` | OTHER+SENT | 2.73 | 2.02 | 14.69% | 2.85 | 2.22 | **0.6585** |

**最紧的两对互相关**（本地 4 年日收益，阈值 0.7）：
- `RRE3O8r1 ↔ d5WqeQbx` = **0.6741**（余量 0.0259）
- `j2Yg2q9j ↔ xArnqeAw` = 0.6555（余量 0.0445，xArnqeAw 尚未确认可提）
- `QPvJ6KVw ↔ npv9WLVE` = 0.5393

⇒ 前两条必须**相邻提交并立即读回平台 self**。

**提交红线**：`workflow_submit_alpha(confirm_submit=True)` 需用户明确授权；
问卷超时自动选中（`explicitUserConfirmation: false`）不算授权。2026-11-01 起已连续 5 次问卷超时，
本轮**不再发问卷**，只在此处正文请示。

---

## 8. 本轮新增/修正的死路与规则

| 条目 | 类型 | 内容 |
|---|---|---|
| `GLB-PV-SINGLE-TOWER-PROD-08677-20261102` | 新增 dead_end | PV 单塔判死 + 三条单塔路径全灭 + `kqNrmA9g` 全指标 |
| `GLB-GATE-CHOICE-DECIDES-PROD-AND-OTHER-SINGLE-TOWER-CONFIRMED-20261102` | 既有 | 门控选型是 prod 第一决定因素 |
| `GLB-OTHER-TOWER-PROD-FLOOR-076-20261101` | 既有 | OTHER 裸信号 0.76 地板 |
| `GLB-PVPRECLOSE-RECOMPUTE-2Y-KILL-20261027` | **修正** | 「天花板 S 2.05」只对**正向**成立 |

---

## 9. 待完成

- [ ] `xArnqeAw` / `mLoqmkd5` prod 结果（在飞，约 400s/颗）
- [ ] w169 收批（8/8）+ 按门控类别归因清洗度
- [ ] 若 w169 门控有幸存者 → 组篮 + 重跑 8 颗的互相关矩阵
- [ ] w170 非 trio 探针（NEWS×ANALYST）——**必须先验证非 trio 信号腿的 prod**
- [ ] 提交授权（用户回复）
