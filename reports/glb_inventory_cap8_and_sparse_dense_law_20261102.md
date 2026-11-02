# GLB 战役：可提交库存硬死在 8 颗 + 稀疏/满仓零重叠铁律（2026-11-02）

region=GLB / delay=1 / universe=MINVOL1M。目标 20 颗，当前已提交 **0 颗**，四闸全过库存 **8 颗**。

---

## 1. 结论先行

| 问题 | 答案 | 证据强度 |
|---|---|---|
| 还能从历史存量里再挖出可提交件吗 | **不能，0 颗** | 82 → 17 → 14 → 2 → 0，四层穷尽 |
| 扩篮的杠杆是什么 | **换信号概念 + 稀疏化骨架**，不是换门控 / 换窗口 / 换 else 支 | 同门控换信号 0.85、换 else 支 0.74 均证伪 |
| prod 墙的本质是什么 | **持仓稀疏度**，不是信号新颖度 | 稀疏 8/8 vs 满仓 11/11 **零重叠** |
| 处女字段是否低相关 | **不是**（techindi_model alphaCount≈0 但 prod 0.7453） | 两颗实测 |

---

## 2. 隐藏库存穷尽：四层漏斗从 82 颗砍到 0

全库 2522 条 GLB alpha，按「未提交 + `fRA='[]'` + prod 从未测 + |S|≥1.58 + F≥1.0」筛出 **82 个**候选（这是「隐藏库存」的全部）。逐层砍：

```
82  基准：未提交 + fRA='[]' + prod 未测 + IS 达标
17  剔除与篮子同信号腿族（single_bucket_ / probability_label / techindi_）
14  剔除历史已判死 / 已实测 prod 名单
 9  剔除 5 行 TO=0.00% 脏行（s15_dlrr_synth_d1 等波次；fRA='[]' 是陈旧写入，实际必挂 LOW_TURNOVER）
 7  剔除 PV pre_close30m 族 3 个（e75wqEMO / 0mYlwAK1 / j2YE6JW9）
     + predicted_quantile 族 2 个（0mY3bpM2 / P0oa0o7W，同族 O0AYlm2J=0.76 / 3qoz2G9g=0.7607）
 5  剔除与 j2Yg2q9j 共用 snt21_2neg_conf_low_394 门控的 2 个
    ⇒ xArnAJPp 实测互相关 0.869 > 0.70，直接否决；j2Yg2qnj 同门控同族
 2  只剩 QPvkPaMw 与 blOMGZzm
 0  两者 prod 实测双双 FAIL
```

B 类（`fRA=NULL` 需补 RA 判定）实测为 **0 个**。

### 两颗最后的候选实测

| alpha | 表达式核心 | S | F | TO | 2Y | sub | 篮子互相关 | prod | 直方图 |
|---|---|---:|---:|---:|---:|---:|---|---:|---|
| `QPvkPaMw` | `signed_power(group_rank(ts_zscore(ts_mean(tm_13_..._q1,2),504),country),2.5)` | 3.48 | 1.50 | 19.9% | 1.87 | 1.90 | **−0.012 ~ 0.062** | **0.7453** ✗ | 36 / 11 / 0 / 0 |
| `blOMGZzm` | `signed_power(subtract(group_rank(quantile_label_4bucket_60day_ohlcv_img_2,country),0.5),0.5)` | 2.43 | 1.69 | 14.4% | 3.02 | 2.31 | 0.32 ~ 0.62 | **0.7824** ✗ | 221 / 16 / 0 / 0 |

`QPvkPaMw` 与篮子 8 颗的相关性 **−0.012 ~ +0.062**，是史上最干净的新件（此前纪录 `78Lwa5z2` 0.151）。
它在相关性维度完美，唯一拦路是 prod 0.7453。

死路已入库：`GLB-HIDDEN-INVENTORY-EXHAUSTED-AT-8-20261102`。

---

## 3. 核心发现：prod 墙是「持仓稀疏度」的零重叠二分

把全库所有测过 prod 的 GLB 候选按骨架分成两类，取值区间**完全不相交**：

| 类别 | 骨架 | n | prod 区间 |
|---|---|---:|---|
| **稀疏** | `trade_when(rank(ts_mean(GATE,W))>0.7, SIGNAL, <0.6 或 0)` | 8/8 全过 | **0.5846 – 0.6638** |
| **满仓** | 任何无 `trade_when` 的 dense 骨架 | 11/11 全挂 | **0.7453 – 0.8318** |

分界带 `[0.6638, 0.7453]` 宽 **0.0815**，**11 + 8 = 19 个样本无一落入**。

稀疏组（全过）：`d5WqeQbx` 0.5846 / `leA0X7lA` 0.6022 / `xArnqeAw` 0.6335 / `QPvJ6KVw` 0.6385 /
`RRE3O8r1` 0.6479 / `9qxR097o` 0.6502 / `j2Yg2q9j` 0.6585 / `npv9WLVE` 0.6638

满仓组（全挂）：`QPvkPaMw` 0.7453 / `O0AYlm2J` 0.76 / `3qoz2G9g` 0.7607 / `mLoqmkd5` 0.7694（multiply 弱加权）/
`blOMGZzm` 0.7824 / `KPrqZ2bN` 0.8134 / `78Lwa5z2` 0.8234 / OTHER 裸信号族 0.8032–0.8318

### 这把「稀疏化」从技巧升为硬前置

此前只知道「`trade_when` 比 `multiply` 好」（1 对 1，0.65 vs 0.7694）。现在它是全库零重叠的二分：
**dense 骨架的 prod 地板（0.7453）高于阈值 0.0454，稀疏骨架的天花板（0.6638）低于阈值 0.0362。**
这不是参数层能调的距离，是结构层分界。

已入库：`GLB-PROD-SEPARATION-SPARSE-VS-DENSE-20261102`（layer=win）。

### 由此产生的直接推论

**处女字段 ≠ 低 prod。** `techindi_model` 1818 字段、`alphaCount` 0–1、本地全 UNTESTED，但
`QPvkPaMw` 用它做 dense 骨架仍然 0.7453。prod 拥挤度来自**骨架**，不来自字段。
反之，用极拥挤的 `dl_riskfree_returns` 字段（`single_bucket_*`，alphaCount 22585）做稀疏骨架，
prod 反而 0.58–0.66。

---

## 4. 塔组合名额账：OTHER 信号腿只剩 6 个席位

`{PV, MODEL, OTHER}` 三者间禁两两混合（含 PV×PV）；trio × 非 trio 允许但**组合名总量 ≤5**，已满 5 个：

| 组合名 | 已用 | 上限 | 剩余 |
|---|---:|---:|---:|
| `FUND+OTHER` | 3（RRE3O8r1 / d5WqeQbx / leA0X7lA） | 3 | **0** |
| `RISK+OTHER` | 2（QPvJ6KVw / npv9WLVE） | 3 | **1** |
| `OTHER+SENT` | 2（j2Yg2q9j / xArnqeAw） | 3 | **1** |
| `EARNINGS+OTHER` | 1（9qxR097o） | 3 | **2** |
| `INSTITUTIONS+OTHER` | 0 | 3 | **3** |
| 合计 | 8 | — | **6** |

**纯 PV / 纯 MODEL / 纯 OTHER 单塔不占配额**（平台 `pyramids.list` 单元素已坐实）；
**非 trio × 非 trio（如 `RISK+FUND` / `INST+FUND` / `NEWS+RISK`）不受 5 名上限约束**，
只受「每组合候选 ≤3」，这是点亮未亮塔（INSTITUTIONS / NEWS / ANALYST / SOCIALMEDIA / INSIDERS / MACRO）的合法通道。

---

## 5. 下一波（w175）设计：6 条模板已预检通过

机制：**把 `techindi_model` 的正交信号（互相关 ≈ 0.05）套进 `trade_when` 稀疏骨架**，
直接检验「稀疏化能否救 `QPvkPaMw` 那条 0.7453」这个假设。6 条模板填满全部 6 个剩余名额。

| # | 信号腿（techindi_model） | 变换 | 门控（新字段） | 组合 |
|---|---|---|---|---|
| 1 | `tm_13_..._d10_q1` | `signed_power(group_rank(ts_zscore(ts_mean(x,2),504),country),2.5)` | `rsk68_weight_dadv`@22 | RISK+OTHER |
| 2 | `tm_13_..._d10_q2` | 同 1（换字段） | `inst18_fundownershipv2_pct_held`@22 | INST+OTHER |
| 3 | `predicted_third_quantile_ten_day_return` | `group_rank(ts_zscore(ts_mean(x,5),252),country)` | `market_value_institutional_shares_acquired`@66 | INST+OTHER |
| 4 | `predicted_fifth_quantile_ten_day_return` | `group_zscore(ts_rank(x,66),country)` | `aggregate_equity_value_institutions`@22 | INST+OTHER |
| 5 | `tm_13_..._d5_q3` | `group_rank(ts_delta(x,22),country)` | `ern3_all_delay_1_pre_interval`@22 | EARNINGS+OTHER |
| 6 | `predicted_first_quantile_ten_day_return` | `signed_power(subtract(group_rank(x,country),0.5),0.5)` | `ern3_next_interval`@66 | EARNINGS+OTHER |

预检：`valid=true`，12 个字段全部命中，无 VECTOR 需包裹，`any_changed=false`。

**这是探针批**（目的：单假设证伪/证实），按纪律不受「≥10 个结构互异模板」约束。

门控选型遵循两道判据：① 需区域均衡 —— `rsk68_weight_dadv` cov 1.0、`aggregate_equity_value_institutions`
cov 1.0、`market_value_institutional_shares_acquired` cov 1.0、`ern3_*` cov 0.81–0.91；
② 避开门控同源 —— 6 个门控字段与篮子 8 颗使用的 5 个门控字段（`rsk60_crowding` /
`fnd44_perc_accruals` / `fnd44_jones_cf_accruals` / `snt21_2neg_conf_low_394` / `assets_total_2` /
`ern3_pre_reptime`）**无一重复**。

---

## 6. w172 / w173（PV 单塔，零配额）

### w172 收批：10/10 COMPLETE，712s，n_pass=0 / n_near=1

multisim `3ttEmScHe4TpcnL74OxLOJ3`。10 颗全是 `pyramids.list` 单元素 `GLB/D1/PV`（PV 单塔、零配额）。

唯一净件 **`78Lwa5z2`**（P7）：S 2.61 / F 1.08 / TO 21.54% / 2Y 1.62 / sub 1.23 / `fRA=0`，
`group_rank(...,exchange)` + **FAST 中性化**把 AMER / EMEA / APAC 三项全部修好
（对照 `A1Vwgp7Q` 用 `group_zscore(...,country)` 仍卡 EMEA 0.84）。
但 prod **0.8234 FAIL**，直方图 7 / 0 / 1 / 0 —— 单点型。与篮子 8 颗 max corr 仅 **0.151**，
精确最大独立集 8→9（`max_subset_exact=true`）⇒ PV 单塔在相关性维度完全可行，唯一拦路是 prod。

> 注：`78Lwa5z2` 属于**满仓组**，按第 3 节铁律本就不该期待它过 prod。

### w173 在飞（异常：进度冻结）

multisim `cPzls6H84GMbAEUKxidxo7`，10 条 PV 模板：`corr_*_with_volume` 族（4 条）、
`pv106` 交易成本族（3 条）、`pv37` 跨时间窗 VWAP（2 条）、`pv98` lag 结构（1 条）。
设置 `MINVOL1M / delay1 / decay10 / FAST / trunc0.08 / maxTrade=OFF / maxPosition=OFF / nanHandling=OFF`。

**观测**：已运行 1047s+，`child_count=0`、平台 `raw.progress` 长期冻结在 **0.35**，
`harvest_multisim_alphas` 返 `No children found`。对照 w172 同规模批次 712s 全出。
判读为**批次疑似挂起**（不是慢）。若继续冻结，下一步处置：放弃该批，改拆成 2 个 5 条小批重派。

**受此阻塞**：w175（6 条已预检通过的模板）按「前批在飞禁发下一批」纪律**不能派发**。

---

## 7. 提交顺序方案（self 池只增不减，顺序即成败）

平台 self-correlation 是**相对于当前已提交 OS 池**计算的，而池只增不减 ⇒ 后提交的件会面对更大的池。
本地已测 self（对现有 OS 池）：

| 提交序 | alpha | local self | 篮内最大互相关 | 点亮作用 |
|---:|---|---:|---|---|
| 1 | `npv9WLVE` | **0.6644**（余量仅 0.0356） | 0.5393（QPvJ6KVw） | RISK 1→2 |
| 2 | `QPvJ6KVw` | 0.6120 | 0.5393（npv9WLVE） | RISK 2→**3 ✅点亮** |
| 3 | `leA0X7lA` | 0.5110 | 0.307（最低） | FUND 0→1，F 2.29 全篮最高 |
| 4 | `9qxR097o` | 0.5596 | 0.5477 | EARNINGS 0→1 |
| 5 | `xArnqeAw` | 0.4665 | 0.6555 | SENT 0→1 |
| 6 | `j2Yg2q9j` | 0.5520 | 0.6555 | SENT 1→2 |
| 7 | `d5WqeQbx` | 0.4597 | **0.6741** | FUND 1→2 |
| 8 | `RRE3O8r1` | 0.4955 | **0.6741** | FUND 2→**3 ✅点亮** |

**原则**：self 余量最薄的先提（池小时风险最小）；互相关最高的对（`RRE3O8r1↔d5WqeQbx` 0.6741，
`j2Yg2q9j↔xArnqeAw` 0.6555）必须**相邻提交并立即读回平台 self**，任何一颗读回超 0.68 就停手。

### 8 颗全部提完后的 self 上界（可精确预判）

self = `max(自身对现有 OS 池的 local self, 与其余 7 颗的篮内最大互相关)`，因为新提交件只增池不删池：

| alpha | local self | 篮内最大互相关 | **提交后 self 上界** | 余量 |
|---|---:|---:|---:|---:|
| `npv9WLVE` | 0.6644 | 0.5393 | **0.6644** | 0.0356 |
| `RRE3O8r1` | 0.4955 | 0.6741 | **0.6741** | **0.0259** ⚠ |
| `d5WqeQbx` | 0.4597 | 0.6741 | **0.6741** | **0.0259** ⚠ |
| `j2Yg2q9j` | 0.5520 | 0.6555 | **0.6555** | 0.0445 |
| `xArnqeAw` | 0.4665 | 0.6555 | **0.6555** | 0.0445 |
| `QPvJ6KVw` | 0.6120 | 0.5393 | **0.6120** | 0.0880 |
| `9qxR097o` | 0.5596 | 0.5477 | **0.5596** | 0.1404 |
| `leA0X7lA` | 0.5110 | 0.3070 | **0.5110** | 0.1890 |

⇒ **8 颗全部可提交，无一超线**，最薄余量 0.0259（`RRE3O8r1` / `d5WqeQbx`）。
已实测复核 `npv9WLVE`：`check_self_correlation` = **0.6644**（pool_size 16，full 18，排除 2 个 power pool），
最大冲突对象 `LLMWkXp6` 0.6644；加入 QPvJ6KVw 后其 0.5393 不会顶过 0.6644。

按今日余量 3 颗计算，最优是 **①`npv9WLVE` ②`QPvJ6KVw` ③`leA0X7lA`**：两颗就能把 RISK 点亮（3 颗门槛），
第三颗投给全篮 F 最高（2.29）且互相关最低（0.307）的 `leA0X7lA`。

---

## 8. 待用户裁定

1. **提交授权（最关键，已 9 次未获答复）**：8 颗四闸全过，今日曾余 3 颗额度。禁止再发问卷，只能正文请示。
2. 是否认可主攻方向从 OTHER 转向「techindi_model 正交信号 × 稀疏化」+「PV 单塔」。
3. 塔组合「每组合候选 ≤3」是否放宽 —— 不放宽则 OTHER 信号腿只剩 6 个席位。
4. `leading gap`（起始晚型前段空窗）是否除名 —— 更严口径下篮会降为 3–4 颗。
5. `macro27` 是否允许先做覆盖探针（论坛明写该族有效历史集中 2019—2023）。

---

## 附录：8 颗篮子四闸状态（NOW 2026-11-02 12:59）

| # | alpha | 塔组合 | S | F | TO | 2Y | sub | prod | self | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `QPvJ6KVw` | RISK+OTHER | 3.19 | 1.59 | 28.97% | 3.43 | 1.84 | 0.6385 | 0.6120 | 0 |
| 2 | `npv9WLVE` | RISK+OTHER | 3.08 | 1.42 | 60.83% | 3.19 | 2.38 | 0.6638 | 0.6644 | 0 |
| 3 | `RRE3O8r1` | FUND+OTHER | 2.89 | 1.73 | 16.02% | 2.13 | 1.71 | 0.6479 | 0.4955 | 0 |
| 4 | `d5WqeQbx` | FUND+OTHER | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | 0.5846 | 0.4597 | 0 |
| 5 | `j2Yg2q9j` | OTHER+SENT | 2.73 | 2.02 | 14.69% | 2.85 | 2.22 | 0.6585 | 0.5520 | 0 |
| 6 | `xArnqeAw` | OTHER+SENT | 2.74 | 1.42 | 21.24% | 2.36 | 1.87 | 0.6335 | 0.4665 | 0 |
| 7 | `leA0X7lA` | FUND+OTHER | **3.41** | **2.29** | 14.44% | 2.72 | 1.94 | 0.6022 | 0.5110 | 0 |
| 8 | `9qxR097o` | EARNINGS+OTHER | 2.56 | 1.50 | 9.55% | 2.72 | 1.32 | 0.6502 | 0.5596 | 0 |

篮子内最大互相关 `RRE3O8r1↔d5WqeQbx` = **0.6741**（余量 0.0259），精确最大独立集 = 8（`max_subset_exact=true`）。

塔位账（GLB/D1 现 `pv 2 / model 3 / other 3 / risk 1 / institutions 1`，门槛 3 颗）：
8 颗全提后 **RISK 3 ✅点亮**、**FUNDAMENTAL 3 ✅点亮**、SENTIMENT 2（差 1）、
EARNINGS 1（差 2）、INSTITUTIONS 1（差 2）、PV 2（差 1）、NEWS / ANALYST / MACRO / SOCIALMEDIA / INSIDERS 各 0（差 3）。
