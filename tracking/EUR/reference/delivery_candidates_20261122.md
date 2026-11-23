# EUR 未亮塔 · 交付候选与族关系台账（2026-11-22）

> 目标：EUR/D1 交付 10 颗验证通过 regular alpha（ATOM 优先）。本文件记录**交付候选池 + 族正交关系 + prod 终验读数**。

## 1. 塔位实况（平台 `get_pyramid_alphas`，2026-11-22）

| 状态 | 塔 | 席位 |
|---|---|---|
| 满塔 | analyst 10 / model 3 / fundamental 3 / news 3 / other 3 / risk 3 / sentiment 3 / imbalance 3 | 不可投 |
| **未满（可交付）** | **institutions 0/3**、**socialmedia 0/3**、**earnings 1/3**、**insiders 2/3**、**macro 2/3**、**pv 2/3** | 11 席 |

## 2. 已过全闸候选（IS 硬闸 + prod refresh 实测，全 UNSUBMITTED）

| # | alpha | 塔位 | S | F | 2Y | TO | prod | 机制族 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | N1NGbddg | INSTITUTIONS 0/3 | 1.69 | 1.05 | 2.17 | 5.14% | **0.6872** | A：analyst EBI 修正广度 + institutions6 买家净差 |
| 2 | vRAvo8jA | INSTITUTIONS 0/3 | 1.72 | 1.06 | 2.27 | 5.18% | **0.6781** | A |
| 3 | leAXvaLn | INSTITUTIONS 0/3 | 1.78 | 1.06 | 2.10 | 5.31% | **0.6951** | A |
| 4 | A1x7E3ae | INSIDERS 2/3 | 1.84 | 1.15 | 2.25 | 5.07% | **0.6604** | A |
| 5 | RRemVOeb | INSIDERS 2/3 | 1.84 | 1.15 | 2.22 | 5.07% | **0.6615** | A |
| 6 | 2r5NgWvY | SOCIALMEDIA 0/3 | 1.65 | 1.01 | 2.07 | 5.11% | **0.6785** | A |

**A 族互相关矩阵（本地 4 年 PnL，1021 点）**：
```
        N1NGbddg vRAvo8jA leAXvaLn A1x7E3ae RRemVOeb 2r5NgWvY
N1NGbddg  1.00    0.9832   0.8482   0.9708   0.9707   0.9848
vRAvo8jA  0.9832  1.00     0.8265   0.9774   0.9776   0.9880
leAXvaLn  0.8482  0.8265   1.00     0.8024   0.8026   0.8284
A1x7E3ae  0.9708  0.9774   0.8024   1.00     0.9986   0.9773
RRemVOeb  0.9707  0.9776   0.8026   0.9986   1.00     0.9776
2r5NgWvY  0.9848  0.9880   0.8284   0.9773   0.9776   1.00
```
⇒ **`max_mutually_below_subset`（阈值 0.7）= {N1NGbddg}，规模 1**。

**★ 关键结论（可迁移）**：A 族 6 颗虽塔位各异（INSTITUTIONS×3 / INSIDERS×2 / SOCIALMEDIA×1），但**同源强腿（analyst EBI 修正广度）主导相关性 0.80–0.9986** ⇒
**换弱腿不换强腿 ⇒ 不产生新席（EUR skill §43 已证同族降相关只有 0.02–0.06）**。
⇒ 交付 10 颗的唯一路径 = **凑齐 10 个正交机制族**（每族 1 席），不是在同一骨架上扫参数。

## 3. 族清单与状态

| 族 | 机制 | 塔 | 状态 |
|---|---|---|---|
| A | analyst EBI 修正广度 + 未亮塔小腿 | INSTITUTIONS/INSIDERS/SOCIALMEDIA | ✅ 6 颗过 prod，但同族只出 1 席 |
| B | earnings6 EPS surprise（actual vs Estimize） | EARNINGS 1/3 | ❌ 7 批 58 臂参数轴封顶（2Y 1.99 / 限 2.02） |
| C | socialmedia15 新系蓝海（αC≤9） | SOCIALMEDIA 0/3 | 🔄 批8 在飞 |
| D | fund_holdings_panel 日频机构面板 | INSTITUTIONS 0/3 | ⏳ 待派 |
| E | mcr27 招聘岗位微观 | MACRO 2/3 | ❌ 数据层排除（2014–2020 零持仓，仅 3 年） |

## 7. ★★★ 正交造族路径（2026-11-22 突破，本轮最关键发现）

**问题**：A 族 6 颗同 analyst EBI 修正强腿 ⇒ 互相关 0.80–0.9986 ⇒ 同篮只出 1 席。
**答案**：用**账号内已过 prod 但未提交**的 analyst 变体作新强腿（它们不在 prod 池里 ⇒ 无重复件）：

| 新强腿 | alpha | 强腿 metric | prod | 与 A 族互相关 |
|---|---|---|---:|---|
| **L1** | `WjOAJWxd` | est_12m_**ebt** 修订广度 | 0.6806 | 0.51–0.55（对 3 颗） |
| **L2** | `qME6VWbj` | est_12m_**ebi 均值**修订 | 0.6609 | 0.56–0.63 |
| L1 × L2 | — | — | — | 0.4674 |

**L1 强腿骨架（逐字照搬）**：
```
vector_neut(
  group_neutralize(
    group_scale(
      signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks),
                                       est_12m_ebt_num_4wks_ago), market), 1.5),
      industry),
    market),
  <弱腿>)
```
弱腿原为 `group_rank(ts_mean(vec_avg(snt27_relpopularity1),66), subindustry)`（SENTIMENT 塔，relpopularity）。

**族 L 配方（批16）**：只换弱腿为 4 个未满塔弱腿 × EBT/EBI 两个强腿：
| 弱腿 | 目标塔 |
|---|---|
| institutions6 买家净差 ts_zscore | INSTITUTIONS 0/3 |
| insider_agg_matrix 高管净买入 ts_sum63 | INSIDERS 2/3 |
| socialmedia12 buzz bf250 | SOCIALMEDIA 0/3 |
| earnings6 EPS 预期差 ts_zscore252 | EARNINGS 1/3 |

**★ 这条路径同时解掉三个死结**：
① 强腿未提交 ⇒ prod 池无母件 ⇒ 无重复件（mcr27/news46 都死在这一点）；
② 与 A 族相关 0.50–0.63 < 0.7 ⇒ 可与 A 族同篮（多席）；
③ 塔位含未满塔 ⇒ 计入点塔收益。

### 7.1 族 L 首波读数（批16，multisim `69n4Jiq4siaIU178wvHecW`，已完）

TOP2500 / FAST / decay 4 / trunc 0.0

| alpha | 弱腿 | S | F | 2Y | sub | 闸 | 塔位 |
|---|---|---:|---:|---:|---:|---|---|
| 3q0JNnVX | institutions6 买家净差 | **2.91** | 2.08 | 2.32 | 1.25 | sub | INSTITUTIONS + ANALYST |
| qM7VRmEZ | insider_agg_matrix 高管净买 ts_sum63 | **2.91** | 2.08 | **2.34** | 1.26 | sub 1.26/限1.51 | **INSIDERS 2/3 + ANALYST** |
| 1YW0Mnjz | earnings6 EPS 预期差 | 2.91 | 2.08 | 2.34 | 1.25 | sub | — |
| WjlJ5WLo | socialmedia12 buzz | 2.40 | 1.63 | 2.33 | 1.21 | sub | — |
| pwa3L1dq / vRAPQJ1z / E5Qxdr6R | fund_holdings 边界事件 | 2.29–2.31 | 1.47 | 1.11–1.13 | 0.83 | 2 项 | — |
| rK78xrR8 | earnings6 ts_zscore 变体 | 1.57 | 0.87 | 1.12 | 0.38 | 4 项 | — |

**★ 关键**：EBT 强腿 + 4 个不同未满塔弱腿 ⇒ **S 稳定在 2.29–2.91**（强腿主导），但 **sub 比率恒定 0.43–0.51 < 0.52 闸** ⇒
**族 L 的统一卡点是 sub 比率闸，不是 S/F/2Y**。⇒ 破闸方向（批20 已派 10 臂）：
① 弱腿内层轴换（industry→subindustry/sector/cartesian）——EUR 定律「内层分组轴决定 sub 上限」；
② 强腿 signed_power 降 S（1.5→1.2/1.0）⇒ 降闸限 0.52×S；
③ 弱腿时序窗（63→132 平滑 / 22 → 累积短窗）；
④ 弱腿形态（ts_zscore 相对化 vs ts_sum 水平）。

## 8. 已排除路线（附证据）

| 路线 | 排除理由 |
|---|---|
| earnings6 换宇宙（TOP2500/CS1600） | 信号住小盘，S 2.4→1.05/0.95（58 臂） |
| earnings6 decay 轴 | d8/d16/d32 2Y 峰 1.99，限 2.02，差 0.03 不可破 |
| mcr27 招聘 | 逐年 longCount 2014–2020 = 0 ⇒ 数据层排除（优先于 prod 墙） |
| RReEEgwb（mcr27 industry 轴） | prod 0.8378，撞近重复件（直方图孤立桶 [0.5,0.6] n=1） |
| 11-21 三颗全闸件 | RReEEgwb→MACRO 已亮 + prod 墙；58geG1P1→FUNDAMENTAL+PV 满塔；E56GgqLL→FUNDAMENTAL+OTHER 满塔 |
| socialmedia15 新系 10 臂 | 全灭（\|S\| ≤ 0.54，9/10 负）⇒ 叠加 d1_ 系 = 45 字段全测 |
| fund_holdings_panel 10 臂 | 全灭（\|S\| ≤ 0.33，8/10 负）⇒ INSTITUTIONS ATOM 判死 |
| pv106 微观结构价差 | 11-12 已测：价差/成本负向，取反上限 1.01 |
| investor_activity 零售流 | 11-20 已测 85 臂：prod 0.78–0.84 + 仅 6 年数据（双卡） |
| 58EJXapM（OTHER×INSIDERS，全闸 S2.03） | prod **0.7156** ❌（孤立桶 [0.7,0.8] n=1 撞近重复件）⇒ **不占受限组腿名额** |
| 11-12 存量 20 颗清单 | techindi 族→other 满；risk 族→risk 已满 3/3；imb5 族→imbalance 满；仅 N1NGbddg 落未满塔 |

## 5. ★ 受限组腿配额管理（用户约束 3）

**规则**：PV / MODEL / OTHER 内部及互相组腿全禁；PV/MODEL/OTHER **可**与其他 category 组腿，但**这类组合合计 ≤5 个**。

**当前实际占用 = 0/5**（11-12 报告里的 5 个受限组合全为 UNSUBMITTED，未提交即未占用）：

| 已验的受限组合件 | 塔位 | prod | 处置 |
|---|---|---|---|
| 58EJXapM | INSIDERS + OTHER | 0.7156 ❌ | 不占名额（prod 未过） |

**★ 配额管理原则**：受限名额极宝贵（≤5），**只应留给已过 prod 的件**；先验 prod 再决定是否消耗名额。
优先用**非受限强腿**（FUNDAMENTAL / IMBALANCE / NEWS / RISK / SENTIMENT / EARNINGS / INSTITUTIONS / INSIDERS / SOCIALMEDIA / MACRO）造新族，不消耗受限额度。

**ANALYST 强腿已被 A 族占用**（6 颗互相关 0.80–0.9986）⇒ 新族必须换强腿才可能正交。

## 6. 交付候选池（2026-11-22 实测）

### 6.1 A 族（analyst 强腿 × 未满塔弱腿）——prod/self 全过，但同族只出 1 席

| # | alpha | 塔位 | S | F | 2Y | TO | prod(refresh) | self | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | N1NGbddg | INSTITUTIONS 0/3 + ANALYST | 1.69 | 1.05 | 2.17 | 5.14% | **0.6872** | 0.6595 | ✅ **唯一入篮** |
| 2 | vRAvo8jA | INSTITUTIONS + ANALYST | 1.72 | 1.06 | 2.27 | 5.18% | **0.6781** | 0.6446 | 备选席位 |
| 3 | leAXvaLn | INSTITUTIONS + ANALYST | 1.78 | 1.06 | 2.10 | 5.31% | **0.6951** | **0.6950 ⚠** | 备选（self 贴线） |
| 4 | A1x7E3ae | INSIDERS 2/3 + ANALYST | 1.84 | 1.15 | 2.25 | 5.07% | **0.6604** | 0.6016 | 备选席位 |
| 5 | RRemVOeb | INSIDERS + ANALYST | 1.84 | 1.15 | 2.22 | 5.07% | **0.6615** | 0.6014 | 备选席位 |
| 6 | 2r5NgWvY | SOCIALMEDIA 0/3 + ANALYST | 1.65 | 1.01 | 2.07 | 5.11% | **0.6785** | 0.6548 | 备选席位 |

- 6/6 平台闸全绿（failed_ra_count=0）、prod 直方图健康、逐年满仓（2r5NgWvY 已逐年核）。
- **互相关 0.80–0.9986 ⇒ 最大互不相关子集 = 1 ⇒ 同篮只出 1 席**。
- 共同最高 self 相关对象 = `O0A508p7`（账号内同族已提交件）⇒ 6 颗若全部提交会互撞。

### 6.2 MACRO 塔专项（唯一 prod 干净且未满的塔）

**发现**：`GrmmNzz0`（mcr27 招聘岗位，**已提交 ACTIVE**）prod **0.5422** / self 0.2013 / S2.65 / 2Y3.10 ⇒
**mcr27 是 EUR 唯一 prod<0.6 的信息源**（其余经典因子全在 0.78–0.89）。

| alpha | 状态 | 塔位 | S | F | 2Y | prod | 判定 |
|---|---|---|---:|---:|---:|---:|---|
| GrmmNzz0 | ACTIVE（已提交） | MACRO | 2.65 | 1.46 | 3.10 | 0.5422 | 已用掉 1 席 |
| pwadNrXv | UNSUBMITTED | MACRO | 1.81 | **0.90 ❌** | 2.16 | 0.4983 | F 不过硬闸 |
| RReEEgwb | UNSUBMITTED | MACRO | 2.18 | 1.27 | 2.62 | **0.8378 ❌** | prod 墙 |
| KPgZvxwE | UNSUBMITTED | MACRO | 2.27 | 1.28 | 2.49 | **0.7202 ❌** | 差 0.02 |

⇒ **MACRO 剩 1 席**，唯一可用杠杆是「同信息源换持仓集合降 prod」（EUR 实证第 56 条：改算子/档位/轴/参数全无效，只有换宇宙有效）。
⚠ mcr27 数据层只有 2021–2023 三年（GrmmNzz0 逐年亦如此）⇒ MACRO 席交付须接受「已提交同族件也是 3 年历史」的先例。

### 6.3 已过 prod 但塔位全满（不计交付，仅备查）

| alpha | 塔位 | S | prod | 备注 |
|---|---|---:|---:|---|
| E56GgqLL | FUNDAMENTAL 3/3 + OTHER 3/3 | 1.68 | 0.5524 | 直方图最干净 |
| 58geG1P1 | FUNDAMENTAL + PV | 1.79 | 0.5362 | PV 占受限名额 |
| ZYQmolVx | RISK + ANALYST + SENTIMENT | 2.48 | 0.6884 | effective=0（三塔组合无效） |
| O0W0w3P7 | NEWS | 2.72 | 0.6403 | 已提交 |
| mLaLllmK | OTHER | 3.98 | 0.6579 | — |

## 9. ★★★ 最终交付篮：2 席（2026-11-22 修正）

**修正说明**：此前把 `58geG1P1` 判为「不可交付」是**判据错误**——它的 `pyramids.list` 是 [FUNDAMENTAL, PV]，
FUNDAMENTAL 虽满 3/3，但 **PV 塔位 2/3 未满**（记忆塔位表明确把 `pv2` 列在「未满6个」里）⇒ 该件点亮 PV 第 3 席，**合规可交付**。

| # | alpha | 塔位（点亮目标） | S | F | 2Y | sub | TO | prod | self |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **N1NGbddg** | **INSTITUTIONS 0/3 → 1/3** + ANALYST(满) | 1.69 | 1.05 | 2.17 | 0.90 | 5.14% | **0.6872** | 0.6595 |
| 2 | **58geG1P1** | **PV 2/3 → 3/3** + FUNDAMENTAL(满) | 1.79 | 1.25 | 2.17 | 1.20 | 6.93% | **0.5362** | 0.4342 |

**篮内互相关**：`58geG1P1 × N1NGbddg = 0.0538`（几乎完全正交）⇒ `max_mutually_below_subset = {58geG1P1, N1NGbddg}`，**规模 2** ✅

**两颗的信息源完全不同**：
- N1NGbddg = analyst7 EBT/EBI 修正广度（分析师预期）× institutions6 买家净差
- 58geG1P1 = fnd72 现金流质量（CFO/资产、CFO/净利）× pv106 买卖价差门控

### PV 塔的 3 颗同族候选（只出 1 席）

| alpha | S | F | 2Y | prod | 与 58geG1P1 |
|---|---:|---:|---:|---:|---:|
| **58geG1P1**（入篮） | 1.79 | 1.25 | 2.17 | **0.5362** | — |
| e75x1vAl | 1.72 | 1.20 | 2.03 | 0.5469 | 0.9369 |
| mL61avpx | 1.78 | 1.24 | 2.13 | 0.5423 | 0.9970 |

⇒ 三颗 fnd72 现金流变体互相关 0.93–0.997 ⇒ **PV 席只能交 1 颗**（选 58geG1P1：prod 最低 0.5362 + self 0.4342 + 2Y 2.17）。

### 第 3 席的候选方向（按成功概率排序）

| 方向 | 现状 | 下一步 |
|---|---|---|
| **insiders1**（INSIDERS 2/3 剩 1 席） | 本轮从未测（遗漏） | 模板族设计已备见 `datasets/insiders1_templates_20261122.md`（5 族），待队列恢复派发 |
| **earnings6 2Y 破闸** | 2Y 1.99 vs 限 2.02（差 0.03） | 参数轴已穷尽 58 臂；剩余可试 = presence 门控族 / 缺失模式族 |
| **PV 塔非 fnd72 新件** | pv 20 个集已摸底（pv106/pv37/pv47/pv109/pv173 等） | pv106 价差族已判弱；需新集 |
| **SOCIALMEDIA 0/3** | socialmedia12/15 纯 ATOM 已穷尽 | 只能作弱腿（A 族路径） |
| **MACRO 2/3** | mcr27 重复件墙 + 3 年数据 | 平台补历史后才可复活 |
| **EARNINGS 1/3 剩 2 席** | 同 earnings6 路径 | 同第二行 |

## 10. ★★★★ 交付篮扩到 3 席（族 M 突破，2026-11-22 晚）

### 3 席终表（全部通过平台闸 + prod + self + 逐年满仓 + 互相关）

| # | alpha | 点亮塔位 | S | F | 2Y | sub | TO | prod | self | 逐年 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | **N1NGbddg** | INSTITUTIONS 0/3 → 1/3 | 1.69 | 1.05 | 2.17 | 0.90 | 5.14% | 0.6872 | 0.6595 | 满仓 ✅ |
| 2 | **58geG1P1** | PV 2/3 → 3/3 | 1.79 | 1.25 | 2.17 | 1.20 | 6.93% | 0.5362 | 0.4342 | 满仓+全正 ✅ |
| 3 | **d5aPlXjX** | INSTITUTIONS 1/3 → 2/3 | **3.90** | **2.32** | **3.21** | **2.25** | 28.4% | **0.6820** | 0.4312 | **十年全正 S3.3–5.8** ✅ |

**篮内互相关（全部 < 0.1，极强正交）**：
```
        N1NGbddg  58geG1P1  d5aPlXjX
N1NGbddg  1.00     0.0538    0.0576
58geG1P1  0.0538   1.00      0.0407
d5aPlXjX  0.0576   0.0407    1.00
```

### 族 M 配方（本轮最重要发现）

```
group_rank(add(
  group_rank(subtract(probability_fifth_quantile_ten_day_bucket_four_15,
                      probability_fifth_quantile_ten_day_bucket_zero_15), industry),   ← techindi 强腿
  group_rank(<未满塔弱腿>, industry)),                                                     ← 决定塔位 + 决定 prod
  industry)
```
设置：TOP2500 / **CROWDING** 中性化 / decay 4 / trunc 0.0 / nan ON / maxTrade OFF

**为什么这族能同时过 sub 与 prod（此前 4 族都做不到）**：
| 族 | 强腿 | sub 比率 | prod |
|---|---|---:|---:|
| L（EBT） | analyst EBT 修正 | 0.40–0.44 ❌ | 0.74 |
| H（news46） | news46 事件流量 | 0.51 ❌ | 0.83 |
| **M（techindi）** | **techindi 概率分位** | **0.55–0.58 ✅** | **0.68 / 0.76** |
⇒ **techindi 概率分位是唯一 sub 比率 > 0.52 的强腿**（因其 PnL 天然分布在全宇宙，不偏大盘）。

**★ 新定律：同强腿换弱腿可降 prod（−0.082）**
| 弱腿 | 塔位 | prod |
|---|---|---:|
| insider_agg_matrix 高管净买入 ts_sum63 | INSIDERS + OTHER | 0.7644 ❌ |
| **institutions6 买家净差 ts_zscore120** | **INSTITUTIONS + OTHER** | **0.6820 ✅** |
⇒ 与 EUR 旧结论「换弱腿只降相关 0.02–0.06」不同：**降相关小，但降 prod 可达 0.08**（因为弱腿改变持仓集合）。
⇒ **prod 贴闸时优先换弱腿，而不是换算子/轴**。

### 剩余塔位与继续扩的方向（批24 在飞）

| 塔 | 现状态 | 篮内已占 | 剩余席位 |
|---|---|---|---|
| INSTITUTIONS | 0/3 | N1NGbddg + d5aPlXjX = 2 席 | **1** |
| PV | 2/3 | 58geG1P1 = 1 席（满） | 0 |
| INSIDERS | 2/3 | 0 | **1** |
| EARNINGS | 1/3 | 0 | **2** |
| SOCIALMEDIA | 0/3 | 0 | **3** |
| MACRO | 2/3 | 0 | **1**（mcr27 重复件墙）|

批24（techindi × 10 弱腿）目标：socialmedia12 buzz/sentiment、earnings6 EPS、fund_holdings 边界、insiders1 流量÷存量、insider_agg 董事、institutions6 三窗/轴、techindi 换 quantile 族。

## 11. 潜在 5 席（批25 新增 2 颗全闸件，2026-11-22 深夜）

| # | alpha | 弱腿 | 点亮塔位 | S | F | 2Y | sub | sub/S | TO | prod | self |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | N1NGbddg | analyst EBT × institutions6 | INSTITUTIONS 0→1/3 | 1.69 | 1.05 | 2.17 | 0.90 | 0.53 | 5.1% | 0.6872 ✅ | 0.6595 ✅ |
| 2 | 58geG1P1 | fnd72 × pv106 | PV 2→3/3 | 1.79 | 1.25 | 2.17 | 1.20 | 0.67 | 6.9% | 0.5362 ✅ | 0.4342 ✅ |
| 3 | d5aPlXjX | techindi × institutions6 | INSTITUTIONS 1→2/3 | 3.90 | 2.32 | 3.21 | 2.25 | 0.58 | 28.4% | 0.6820 ✅ | 0.4312 ✅ |
| 4 | **XgaO2WOa** | techindi × **insiders1 流量÷存量** | **INSIDERS 2→3/3** | **3.89** | **2.40** | 2.87 | 2.22 | 0.57 | 26.4% | pending | 待验 |
| 5 | **rK7nJ5nE** | techindi × **socialmedia12 buzz** | **SOCIALMEDIA 0→1/3** | 2.58 | 1.41 | 2.57 | 1.55 | 0.60 | 29.9% | pending | 待验 |

**互相关矩阵（4 年 1021 点）**：
```
             N1NGbddg  58geG1P1  d5aPlXjX  XgaO2WOa  rK7nJ5nE
N1NGbddg       1.00     0.0538    0.0576   -0.0513    0.0313
58geG1P1      0.0538    1.00      0.0407    0.0420   -0.0003
d5aPlXjX      0.0576    0.0407    1.00      0.6297    0.5989
XgaO2WOa     -0.0513    0.0420    0.6297    1.00      0.6807
rK7nJ5nE      0.0313   -0.0003    0.5989    0.6807    1.00
```
⇒ **全部 < 0.7**（合规红线）⇒ 5 颗可同篮。⚠ `rK7nJ5nE × XgaO2WOa = 0.6807` 贴线（同 techindi 强腿），
若按更严的 0.5 内部标准则最优子集 = {rK7nJ5nE, N1NGbddg, 58geG1P1}（3 颗）。

**★ insiders1 首次出货**：`XgaO2WOa` 用 `ts_sum(divide(multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance)), vec_sum(insd1_holdings)), 44)` ——
即「内部人交易金额 × 显著性 ÷ 持股总量」的 44 日累积（**流量÷存量**，正是 70 赞 DEU 专帖的核心构造）。
⇒ 之前 11-20 会话把 insiders1 纯 ATOM 判 S1.01，本轮证明它作为**弱腿**在 techindi 强腿下能出 S3.89。

## 12. ★ 纯 ATOM 缺口补齐（用户 2026-11-22 二次重申「优先做 ATOM」）

自查后发现的真实缺口：

| 数据集 | 塔 | 之前族数 | 动作 | 状态 |
|---|---|---:|---|---|
| **insiders1** | INSIDERS 2/3 | **0** | 5 族设计 → 5 臂派发（T1 流量÷存量 / T2 累积水平 / T3 事件密度 / T4 相对历史 / T5 显著性×笔数） | 🔄 在飞 |
| **institutions6** | INSTITUTIONS 0/3 | 2 | 需补 3 族（水平型 / 差分型 / 事件密度） | ⏳ 待派 |
| **socialmedia15** | SOCIALMEDIA 0/3 | 2 | 需补 3 族（事件密度 / 缺失模式 / 差分） | ⏳ 待派 |

## 13. ★★★ 最终定稿：4 席交付篮 + 1 席待验（2026-11-22 深夜）

### 4 席（全验证通过，未提交）

| # | alpha | 数据集 | 点亮塔位 | S | F | 2Y | sub | TO | prod | self | 逐年 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | **N1NGbddg** | institutions6 × analyst7 | **INSTITUTIONS 0→1/3** | 1.69 | 1.05 | 2.17 | 0.90 | 5.1% | 0.6872 | 0.6595 | 满仓 ✅ |
| 2 | **58geG1P1** | fnd72 × pv106 | **PV 2→3/3（满）** | 1.79 | 1.25 | 2.17 | 1.20 | 6.9% | 0.5362 | 0.4342 | 十年全正 ✅ |
| 3 | **d5aPlXjX** | techindi × institutions6 | **INSTITUTIONS 1→2/3** | 3.90 | 2.32 | 3.21 | 2.25 | 28.4% | 0.6820 | 0.4312 | 十年全正 S3.3–5.8 ✅ |
| 4 | **XgaO2WOa** | techindi × insiders1 | **INSIDERS 2→3/3（满）** | 3.89 | 2.40 | 2.87 | 2.22 | 26.4% | 0.6770 | 0.3776 | **十年全正 S2.1–6.5** ✅ |

**篮内互相关**：5/6 对 < 0.06，`d5aPlXjX × XgaO2WOa = 0.6297`（同 techindi 强腿，< 0.7）⇒ 四颗可同篮。
**点亮合计**：INSTITUTIONS 0→2/3、PV 2→3/3、INSIDERS 2→3/3。

### 1 席待验

| alpha | 弱腿 | 塔位 | S | F | 2Y | sub | 互相关 vs 4 席 | prod |
|---|---|---|---:|---:|---:|---:|---|---|
| **rK7nJ5nE** | socialmedia12 buzz | SOCIALMEDIA 0→1/3 | 2.58 | 1.41 | 2.57 | 1.55 | 0.031/−0.000/0.599/0.681 全 <0.7 | **pending**（外部进程 Grm7oV9P 长期占 prod 槽） |

### 剩余可扩席位

| 塔 | 定稿后 | 剩余 | 可用路径 |
|---|---|---|---|
| INSTITUTIONS | 2/3 | **1** | techindi × institutions6 换窗（60/250）/ 换轴（subindustry） |
| SOCIALMEDIA | 0/3（rK7nJ5nE 待验占 1） | 2–3 | techindi × scl12_sentiment / scl15 新字段 |
| EARNINGS | 1/3 | **2** | techindi × earnings6 / earnings_sentiment |
| MACRO | 2/3 | 1 | 平台补 mcr27 历史后复活 |
| PV / INSIDERS | 3/3 满 | 0 | — |

### 用户「优先 ATOM」的最终答复

**纯 ATOM 面 51 族全覆盖**（见 `template_family_exhaustion_20261122.md` §11）：
- 8 个未亮塔数据集 × 5–9 族，族内最好 S ≤ 1.35（除 mcr27 S2.77 被数据层+重复件双墙）；
- **ATOM 可交付 = 0 颗**，这是实测结论不是推断；
- 但 **ATOM 判死的弱数据集作弱腿仍能出 S 2.58–4.55**（insiders1 → S3.89、socialmedia12 → S2.58）
  ⇒ 4 席全部是「techindi/analyst 强腿 + ATOM 判死集弱腿」的组腿件，**没有一席是纯 ATOM**。

## 14. ★★★★ 6 席定稿 + techindi 强腿互相关饱和（2026-11-22 深夜续）

### 14.1 6 席篮（互相关最大对 0.6807 < 0.7，全部 fRA=0，全 UNSUBMITTED）

| # | alpha | 数据集 | 点亮塔位 | S | F | 2Y | sub | TO | prod |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | N1NGbddg | institutions6 × analyst7 | INSTITUTIONS 0→1/3 | 1.69 | 1.05 | 2.17 | 0.90 | 5.1% | 0.6872 ✅ |
| 2 | 58geG1P1 | fnd72 × pv106 | PV 2→3/3 满 | 1.79 | 1.25 | 2.17 | 1.20 | 6.9% | 0.5362 ✅ |
| 3 | d5aPlXjX | techindi × institutions6 | INSTITUTIONS 1→2/3 | 3.90 | 2.32 | 3.21 | 2.25 | 28.4% | 0.6820 ✅ |
| 4 | XgaO2WOa | techindi × insiders1 | INSIDERS 2→3/3 满 | 3.89 | 2.40 | 2.87 | 2.22 | 26.4% | 0.6770 ✅ |
| 5 | rK7nJ5nE | techindi × socialmedia12 | **SOCIALMEDIA 0→1/3** | 2.58 | 1.41 | 2.57 | 1.55 | 29.9% | **pending** |
| 6 | WjlxGbRG | techindi × earnings_sent_matrix | **EARNINGS 1→2/3** | 3.09 | 2.03 | 2.76 | 2.08 | 23.8% | **inflight** |

### 14.2 ★★★ techindi 强腿互相关饱和 = 4 件（硬结论）

`compute_mutual_correlation` 8 件矩阵（1021 点）实测两两：

| 对 | 互相关 |
|---|---:|
| d5aPlXjX × rK7nJ5nE | 0.5989 |
| d5aPlXjX × XgaO2WOa | 0.6297 |
| WjlxGbRG × d5aPlXjX | 0.6445 |
| XgaO2WOa × WjlxGbRG | 0.6519 |
| rK7nJ5nE × WjlxGbRG | 0.6580 |
| **XgaO2WOa × rK7nJ5nE** | **0.6807（最大）** |
| **WjlxGbRG × pwapKq9g** | **0.7050 ❌** |
| **pwapKq9g × E5Q2eZ9G** | **0.7329 ❌** |
| **WjlxGbRG × E5Q2eZ9G** | **0.7664 ❌** |

⇒ `max_mutually_below_subset(0.7)` 稳定停在 **6**，第 7 件（同强腿）一律越线。
⇒ **同一强腿最多产出 4 个互相关合规的 alpha**；第 5 件起必须换强腿。这是可迁移的容量律（与「换弱腿只改 PnL 形状 0.02–0.06」同源）。

### 14.3 Wave A（INSTITUTIONS 最后 1 席）失败归因

| alpha | 弱腿 | S | F | 2Y | sub | TO | 失败原因 |
|---|---|---:|---:|---:|---:|---:|---|
| pwapKq9g | boundary_transaction_total / holder_account_total | 3.97 | 2.09 | 2.61 | 2.48 | **36.7%** | 互相关 0.705/0.733 + **TO 超 EUR 评审带 30%** |
| E5Q2eZ9G | security_transaction_usd_value / security_holding_usd_value | 3.53 | 1.74 | 3.19 | 2.14 | **39.0%** | 互相关 0.766/0.733 + TO 39% |

- 两者 `failed_ra_count=0`（平台全闸），**但入不了交付篮**；
- 根因：fund_holdings_panel 是季频披露 ⇒ 66d/252d z 栈在中频衰减里翻动，TO 比 institutions6 弱腿高 8–10pp；
- ⇒ INSTITUTIONS 最后 1 席**不能用 techindi × 任何季频弱腿**填，只能另起一条强腿。

### 14.4 下一阶段强腿候选（按可交付性排序）

| 强腿候选 | 塔位余量 | 依据 | 状态 |
|---|---|---|---|
| **socialmedia12（scl12_sentiment / scl12_buzz）** | SOCIALMEDIA 2 席 | 作弱腿已出 S2.58；6/6 字段画像 + 5 族设计已归档 | **Wave B 在飞**（`o2HYt79o4wL9fq1dF7HqZah`，B1–B5） |
| earnings6（TOP2500 重测） | EARNINGS 1 席 | TOP800 天花板 2Y 1.99/限 2.02；TOP2500 限值降为 1.58 | 待派 |
| institutions6 | INSTITUTIONS 1 席 | 纯 ATOM 上限 S0.95（11-06 实测），作强腿不足 | 降级 |
| mcr27 | MACRO 2 席 | 数据层排除（近十年数据不满） | 关闭 |

## 15. ★★★★★ 交付容量终判：EUR = **5 席**（2026-11-22 深夜，全部实测）

### 15.1 本轮后 4 批全部出局（读数与死因）

| 批 | 内容 | 读数 | 死因 |
|---|---|---|---|
| Wave A `2YS1AegLS4Cyczpa4Z53aBG` | techindi × fund_holdings_panel ×2 | `pwapKq9g` S3.97/F2.09/2Y2.61；`E5Q2eZ9G` S3.53/F1.74/2Y3.19，均 fRA=0 | 互相关 **0.705/0.733/0.766**；TO **36.7%/39.0%**（>EUR 评审带 30%） |
| Wave B `o2HYt79o4wL9fq1dF7HqZah` | socialmedia12 **纯 ATOM 五族** | S 0.04 / 0.07 / 0.39 / 0.40 / 0.38 | 该集作强腿无定价力 |
| Wave C `3DD5Vq5aV4i0aQZZEEg7otq` | techindi × earnings6 ×4 | S 4.78/4.65/4.80/4.79，F≈3.0，2Y≈3.1，fRA=0 | 互相关 **0.768–0.803**（彼此 0.9188）；TO 34–36%；四臂读数几乎相同 ⇒ 弱腿信息量≈0 |
| Wave D `RM7rTeof4iPcEwXpVbStm4` | 新强腿探针 3 + 组腿 2 | imbalance 0.61/0.47；model182 0.33；组腿 0.98/0.84 | 两个「冷门」候选作为强腿均达不到 1.58 的一半 |

### 15.2 强腿候选全景（EUR，全部已实测）

| 强腿 | 最佳 S | 2Y | sub/S | prod | 可交付席数 |
|---|---:|---:|---:|---|---|
| **techindi 概率分位差** | **4.80** | 3.1–3.2 | 0.57 | 0.68 | **3**（4 件互相关合规，第 4 件 WjlxGbRG prod 0.752 出局） |
| analyst7 EBI 修正广度 | 1.84 | 2.10–2.27 | **0.40–0.44** ❌ | 0.66–0.70 | **1**（sub 比率结构死，无法组腿） |
| fnd72 × pv106 | 1.79 | 2.17 | 0.67 | 0.54 | **1**（族内变体互相关 0.94–0.997） |
| earnings6（双 EPS） | 2.4@TOP800 | **1.99 / 限 2.02** ❌ | — | — | 0（58 臂穷尽） |
| earnings_sent_matrix | 仅作弱腿有效 | — | — | 拉高 prod 至 0.752 | 0 |
| institutions6 | 0.95 | 0.04 | 0.55 | — | 0 |
| fund_holdings_panel | ≤1.0（6 族） | — | — | — | 0 |
| socialmedia12 | **0.40**（5 族） | 1.6 max | — | — | 0 |
| socialmedia15 | 6 族全灭 | — | — | — | 0 |
| insiders1 | 1.01 | 1.30 | — | — | 0 |
| mcr27 | 2.77 | 3.03 | — | 0.766+ | 0（数据层 <10 年 + 重复件墙） |
| **euro_equity_imbalance** | **0.61** | 1.18 | 0.77 | — | 0（组腿后仅 0.98） |
| **model182（网络动量）** | **0.33** | 0.65 | 2.0 | — | 0（组腿后仅 0.84） |
| news18 | 0.66 | — | — | — | 0 |
| macro10 / macro27 | 1 字段 / 数据层排除 | — | — | — | 0 |

⇒ **EUR 未亮塔名义 11 席，实际可达 5 席**。缺口不是"没挖够"，而是**每个塔只有 1–2 个数据集、且这些数据集自身信号强度不足或与唯一强腿同源**。

### 15.3 组腿配额（rule 3）账目

| # | alpha | 组合类型 | 是否计入 PV/MODEL/OTHER 配额 |
|---|---|---|---|
| 1 | N1NGbddg | institutions6 × analyst7 | 否（ANALYST×INSTITUTIONS） |
| 2 | 58geG1P1 | fnd72 × pv106 | **是（PV）** |
| 3 | d5aPlXjX | techindi × institutions6 | **是（OTHER）** |
| 4 | XgaO2WOa | techindi × insiders1 | **是（OTHER）** |
| 5 | rK7nJ5nE | techindi × socialmedia12 | **是（OTHER）** |
| — | WjlxGbRG（prod 0.752 出局） | techindi × earnings_sent_matrix | 不计（未交付） |

⇒ 已用 **4/5**，剩 1 席。**后续任何扩席只能走 analyst / news / sentiment / fundamental 强腿（零配额）**，否则第 6 席即触配额上限。

### 15.4 第 5/6 席 prod 结果：**两颗都撞单件（0.7134 / 0.752）**

| alpha | 塔位 | S | 2Y | prod | 直方图指纹 | 判定 |
|---|---|---:|---:|---:|---|---|
| rK7nJ5nE | SOCIALMEDIA 0→1/3 | 2.58 | 2.57 | **0.7134 ❌** | `[0.6,0.7)` 32 对 / `[0.7,0.8)` **1 对** / min −0.5491 | 撞单个近重复件 ⇒ **可修** |
| WjlxGbRG | EARNINGS 1→2/3 | 3.09 | 2.76 | **0.7520 ❌** | `[0.6,0.7)` 85 对 / `[0.7,0.8)` **1 对** / min −0.5298 | 同上 ⇒ 可修 |

两件逐年均已验满仓（rK7nJ5nE 2014–2023 pnl 全正 144k–1.44M；WjlxGbRG 十年满仓）。

**修复动作**：按「孤立高桶 n=1 = 单件冲突，换弱腿/换窗可躲」的判据，派 `VB8xw9qh4se9irIuSO1sX9`（5 臂）——
techindi 强腿**不动**（塔位不变），只换弱腿形态：buzz 120d bf+z250 / buzz ts_rank250 / buzz ts_mean66 / buzz 一年比值 / sentiment 120d bf+z250。
目标：S 保持 ≥1.58 的同时把 prod 压回 0.68 带（同强腿兄弟件实测 0.677–0.682）。

**prod 槽争用诊断（可复用）**：`correlation_busy` 的 `holder` 形如 `corr:<tool>(<alpha_id>)`；
`logs/_dblock/correlation.lock.json` 的 `owner` 可能是**本机 MCP 进程 pid**（本轮 24924），
因为多会话共用 `127.0.0.1:8000` HTTP 服务 ⇒ 表现为"自己占自己的槽"。
判据：读 `logs/_dblock/correlation.inflight.json` 的 `expires_at`（epoch），到期后 lock 自动轮转为 `.stale`；
**禁止手删锁**。连续 pending 会触发账号级熔断 `platform_unavailable`（本轮实测 600s 窗口），期间工具不发请求。

### 15.5 ★★★ 修复批结果（`VB8xw9qh4se9irIuSO1sX9`，5 臂全闸）——「撞单件」配方首个成功案例

强腿不动（techindi 概率分位）、只换 socialmedia12 弱腿形态：

| 弱腿形态 | alpha | S | F | 2Y | sub | TO | 与 4 席最大互相关 |
|---|---|---:|---:|---:|---:|---:|---:|
| buzz 120d bf + z250 | WjlxL7Yd | 2.59 | 1.39 | 2.68 | 1.51 | 29.2% | 0.6516 ✅ |
| buzz ts_rank250 | blaK8jx6 | 2.67 | 1.41 | 2.49 | 1.55 | 31.3% | 0.6776 ✅ |
| **buzz ts_mean66** | **vRAoOjYb** | **2.11** | **1.27** | **2.16** | **1.16** | **21.9%** | **0.6406 ✅（余量最大）** |
| buzz 一年比值 | 3q02jl1Z | 3.58 | 2.03 | 3.00 | 1.97 | 36.9% | **0.7491 ❌** |
| sentiment 120d bf + z250 | P05AM7xq | 2.59 | 1.38 | 2.52 | 1.44 | 29.1% | 0.6828 ✅ |

`max_mutually_below_subset(0.7)` = **6** = {N1NGbddg, 58geG1P1, d5aPlXjX, XgaO2WOa, **WjlxL7Yd**, **vRAoOjYb**}；
且 `WjlxL7Yd × vRAoOjYb = 0.6802`（两者也能共存）。
⇒ **修复批把一个 prod 0.7134 的死件变成了 2 个可共存候选**（原 rK7nJ5nE 的互相关 0.6807 vs XgaO2WOa 被换成 0.6406）。

⚠ **但 rule 3 组腿配额只剩 1 个名额**（OTHER×SOCIALMEDIA 已有 rK7nJ5nE 计 1，其出局后名额回补 1）⇒ 只能取一。
**选定 `vRAoOjYb`**：TO 21.9% 最接近 EUR 评审带（≤30%）、互相关余量最大、S 2.11 稳过 1.58 闸。
`WjlxL7Yd` 作平替（S 更高 2.59，但 TO 29.2% 更贴上限、互相关余量更小）。

**`vRAoOjYb` 逐年持仓（2026-11-22 平台 `get_alpha_yearly_stats` 实读）**：

| 年 | pnl | longCount | shortCount | S | 年 | pnl | longCount | shortCount | S |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 2014 | 1.08M | 1274 | 1342 | 2.76 | 2019 | 0.94M | 1380 | 1449 | 3.32 |
| 2015 | 0.91M | 1323 | 1400 | 2.00 | 2020 | **3.5k** | 1353 | 1409 | 0.01 |
| 2016 | 0.77M | 1319 | 1401 | 2.10 | 2021 | 0.58M | 1456 | 1506 | 1.58 |
| 2017 | 0.94M | 1436 | 1515 | 3.45 | 2022 | 0.79M | 1437 | 1466 | 1.45 |
| 2018 | 0.93M | 1426 | 1500 | 2.82 | 2023 | 1.16M | 1369 | 1388 | 3.58 |

⇒ 十年 pnl **全正**（2020 仅 3.5k 但非零），longCount 1274–1456 / shortCount 1342–1515 全 >0 ⇒ **数据层排除不适用，十年满仓条件满足**。
⚠ 2020 pnl 3.5k / S 0.01 是**全市场效应**（与族 A 交付件 2020 走弱同源），非零持仓 ⇒ 不是空仓年。

**self 闸（本地 `check_self_correlation`，不占平台槽）已过**：`max_correlation = 0.5103 < 0.7`，
最高相关 `vRAOWYra` 0.5103 / `kqJOQgnk` 0.3748 / `Wjl6JJQO` 0.3363；
EUR OS 池 21 只（全池 28，排除 Power Pool 7）——池规模合理，非「7«147 作废」情形。

**唯一剩余项**：`vRAoOjYb` 的 prod 实测——会话恢复后两次撞 `corr:get_production_correlation(pwaplg5g)` 占槽
（锁文件 owner pid 从 24924 变为 29968 = MCP 服务重启，holder 是平台 job id 非我 alpha），
inflight `expires_at=1795347731`（约 2026-11-22 19:42），按规则不重触发、不手删锁，等自然到期后单次回读。


