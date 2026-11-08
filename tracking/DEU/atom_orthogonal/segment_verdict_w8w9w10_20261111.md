# DEU 段落判决 — Wave 8/9/10 + analyst44 开波

> region=DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / pasteurization ON / unitHandling VERIFY
> 本段核心：**分组轴 industry + estimator 视角 + 异窗 132/11 = DEU 首颗全闸通过 ATOM**

---

## 零、本段最大成果：QPv6jLvX 全闸通过（第 6 颗交付件 / 第 4 颗严格 ATOM）

```text
group_rank(add(rank(ts_mean(vec_avg(anl93_recprofitabilityprev_estimator_profitability2), 132)),
           rank(ts_mean(vec_max(anl93_recprofitabilityprev_estimator_profitability2), 11))), industry)
```

| 闸 | 值 | 门槛 | 状态 |
|---|---:|---:|:--:|
| LOW_SHARPE | **1.59** | 1.58 | **PASS**（首次）|
| LOW_FITNESS | **1.52** | 1.0 | PASS |
| LOW_2Y_SHARPE | **2.01** | 1.58 | PASS（大幅超出）|
| LOW_TURNOVER / HIGH_TURNOVER | 0.0411 | 0.01-0.7 | PASS |
| LOW_SUB_UNIVERSE_SHARPE | 1.16 | 0.754 | PASS |
| CONCENTRATED_WEIGHT | - | - | PASS |
| **PROD_CORRELATION** | **0.6615** | <0.70 | **PASS**（余量 0.0385）|
| CLUSTER_TEST | 0.99 | 1.0 | warning（贴线但通过，failed_ra 不计）|
| **failed_ra_count** | **0** | 0 | **PASS** |

补充：returns 0.1140 / dd 0.1112 / margin 0.005543 / investability_sharpe 1.55 / investability_fitness 1.44 / risk_neutralized_sharpe 1.01 / longCount 70 / shortCount 69 / MATCHES_PYRAMID DEU/D1/ANALYST x1.8

**互相关验证（与已交付 5 颗）**：all_below_threshold=true、max_mutually_below_subset_size=6、max_subset_exact=true。
最高对 = QPv6jLvX vs E56pROb9 = **0.2387**；对 mLox6Mg2 = **-0.0969**；对 MPY9VNY9 = 0.164；对 QPvzNNGG = 0.1274；对 LLMzYrZe = 0.1290。
=> **池容量由 5 升到 6**，且 QPv6jLvX 是池中互相关最低的件之一。

---

## 一、Wave 8 判死：bucket 轴 + 外层 ts_mean 全线失败

批次 7WhFxfp54vi8PaRg6WzFBl，10/10 COMPLETE，10 REVIEW（但 failed_ra 2-3）。

| # | 设计 | alpha | S | F | 2Y | sub_u | TO | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | bucket0.1 + 外层 ts_mean **5** | GrW9YW9x | 1.49 | 1.43 | 1.64 | 1.08 | 0.0705 | 2 |
| 2 | bucket0.1 + 外层 ts_mean **22** | xAr59rEn | 1.39 | 1.28 | 1.61 | 1.01 | 0.0684 | 2 |
| 3 | bucket **0.2** | 58EY3E25 | 1.44 | 1.37 | 1.56 | 1.10 | 0.0577 | 3 |
| 4 | bucket **0.05** | mLoQJoN2 | 1.51 | 1.45 | 1.63 | 1.15 | 0.0883 | 2 |
| 5 | bucket0.1 + **max11** | VkxeqxL0 | 1.51 | 1.46 | 1.52 | 1.15 | 0.0753 | 3 |
| 6 | bucket0.1 + **avg132** | e75Eg5PE | 1.49 | 1.43 | 1.76 | 1.06 | 0.0710 | 2 |
| 7 | bucket0.1 + **avg252** | pwd3odeq | 1.44 | 1.35 | 1.64 | 1.10 | 0.0706 | 2 |
| 8 | bucket0.1 + **仅 avg66（去极值腿）** | 78Ll0LRO | 1.27 | 1.16 | 1.16 | 0.81 | 0.0662 | 3 |
| 9 | bucket0.1 + **multiply** | 9qxkbxOr | 1.45 | 1.40 | 1.51 | 1.03 | 0.0712 | 3 |
| 10 | bucket0.1 + **group_zscore** | QPv6qvpg | 1.40 | 1.32 | 1.58 | 1.01 | 0.0604 | 3 |

**结论（判死）**：
1. **外层 ts_mean 是负杠杆**：同结构无外层 -> 1.50（2rAeQQJY），外层 5 -> 1.49，外层 22 -> **1.39**。外层平滑把 S 压掉 0.11。
2. **外层 ts_mean 没能修 CW**：2rAeQQJY 的 CONCENTRATED_WEIGHT 失败在加外层平滑后依然存在（failed_ra 仍为 2）。
3. **分桶粒度单调**：0.05 -> 1.51 / 0.1 -> 1.50 / 0.2 -> 1.44。越细分越好，但天花板仍低于 industry 轴。
4. **去掉极值腿全崩**（1.27 / 2Y 1.16）=> 极值腿（vec_max）是 analyst93 机制不可或缺的组成部分，不是装饰。
5. bucket 轴唯一优点：prod 0.6967 过闸。但代价是 S 天花板 1.51 且 CW 未解 => **不如 industry 轴（prod 0.6615 + S 1.59 + CW 通过）**。

---

## 二、Wave 9：industry 轴 × 窗口网格（关键转折）

批次 1AV7zDsY4uKckKM6aOhEBp，10/10 COMPLETE，10 REVIEW。

| # | 设计 | alpha | S | F | 2Y | sub_u | TO | dd | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | industry 66/**5** (analyst) | d5WvgP0x | 1.53 | 1.43 | 1.58 | 1.15 | 0.0496 | 0.1126 | 1 |
| 2 | industry 66/**11** (analyst) | N1N8q2Rq | 1.56 | 1.47 | 1.70 | 1.17 | 0.0426 | 0.1083 | 1 |
| 3 | industry **132/22** (analyst) | 9qxkb272 | 1.56 | 1.47 | **2.02** | 1.09 | 0.0358 | **0.0991** | 1 |
| 4 | industry 252/22 (analyst) | Xg9MPOol | 1.37 | 1.21 | 1.63 | 1.16 | 0.0351 | 0.1229 | 1 |
| **5** | **industry 66/5 (estimator)** | **omEZAkNE** | **1.57** | **1.49** | 1.69 | **1.23** | 0.0492 | 0.1026 | **1** |
| 6 | **market** 66/5 | 9qxkb2X1 | 1.56 | **1.57** | 1.49 | 1.23 | 0.0407 | 0.1352 | 2 |
| 7 | group_zscore industry | GrW9Y7lQ | 1.52 | 1.46 | 1.57 | 1.14 | 0.0391 | 0.1258 | 2 |
| 8 | multiply industry | 3qoJ329g | 1.44 | 1.32 | 1.33 | 1.09 | 0.0497 | 0.1272 | 2 |
| 9 | max x2 加权 industry | bl6AVKRr | 1.48 | 1.36 | 1.26 | 1.17 | 0.0558 | 0.1156 | 2 |
| 10 | **sector** 66/5 (analyst) | JjerYnEO | 1.57 | 1.55 | 1.56 | 1.11 | 0.0484 | 0.1314 | 2 |

**结论**：
1. **estimator 视角 > analyst 视角**：同为 66/5 + industry，estimator 1.57 vs analyst 1.53 => **+0.04**。两个视角是同一经济量的不同评价者，estimator（模型推断）比 analyst（人工预测）更平滑、噪声更低。
2. **market 轴 S 不差（1.56/F 1.57 最高）但 2Y 塌到 1.49** => market 轴破坏时序稳定性，不能用于 2Y 硬闸。
3. **multiply / 加权 / group_zscore 仍是负杠杆**（1.44-1.52，2Y 1.26-1.57），与 Wave 5 结论一致。
4. omEZAkNE 的 **CLUSTER_TEST 是 pass**（列表在 pass 里），优于 d5WvgnA2 的 0.97 贴线；prod 实测 **0.6767 通过**，仅卡 LOW_SHARPE 0.01。

---

## 三、Wave 10-A：estimator 132/11 突破 1.58

批次 3ABHO369F4Y6akR7swADLhe，10/10 COMPLETE。

| # | 设计 | alpha | S | F | 2Y | sub_u | TO | margin | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **4** | **E 132/11 industry** | **QPv6jLvX** | **1.59** | **1.52** | **2.01** | 1.16 | 0.0411 | 0.005543 | **0** |
| 2 | E 132/22 industry | wpQW1M9Q | 1.57 | 1.49 | **2.09** | 1.08 | 0.0359 | 0.006247 | 1 |
| 3 | E 66/22 industry | 78LlQEo2 | 1.57 | 1.49 | 1.86 | **1.23** | 0.0377 | 0.005947 | 1 |
| 7 | E66avg + A11max | akKGlqa6 | 1.57 | 1.49 | 1.71 | 1.16 | 0.0423 | 0.005325 | 1 |
| 1 | E 66/11 industry | VkxeEgdw | 1.55 | 1.46 | 1.66 | 1.17 | 0.0423 | 0.005245 | 1 |
| 8 | A66+A11+E132 三腿 | LLM36AK6 | 1.54 | 1.46 | 2.03 | 1.01 | 0.0351 | 0.006407 | 1 |
| 9 | A66avg+E11max+E132avg | 6XdN1vMK | 1.54 | 1.46 | 2.02 | 1.04 | 0.0353 | 0.006395 | 1 |
| 6 | A66avg + E11max | e75EKo5N | 1.53 | 1.43 | 1.74 | 1.15 | 0.0427 | 0.005134 | 1 |
| 10 | E 66/5 **market** | qMLVdo51 | 1.51 | 1.50 | 1.46 | 1.19 | 0.0407 | 0.006059 | 2 |
| 5 | E **252**/22 industry | rKR8LvRo | 1.38 | 1.22 | 1.55 | 1.18 | 0.0352 | 0.005583 | 2 |

**结论**：
1. *** 最优窗口对 = 长均值 132 + 短极值 11 ***。E 视角 + industry 轴下：
   - 66/11 -> 1.55；**132/11 -> 1.59**；132/22 -> 1.57；66/22 -> 1.57；252/22 -> 1.38
   => **均值腿有最优值 132（约 6 个月）**，不是越长越好：252 会掉 0.21。
2. **极值腿的最优窗口依赖均值腿长度**：均值腿 66 时最优极值腿 5（1.57 > 66/11 的 1.55）；均值腿 132 时最优极值腿 11（1.59 > 132/22 的 1.57）。
   => 两腿的时间尺度要拉开一个**固定倍率约 12 倍**，倍率本身比绝对窗口更重要。
3. **跨视角混合中性偏负**：E66avg+A11max = 1.57（约等于纯 E），A66avg+E11max = 1.53（低于纯 E）；三腿全部掉到 1.54。=> 再次验证「第三腿稀释」与「混合不增益」。
4. **2Y 由均值腿窗口决定**：132/22 -> 2.09、132/11 -> 2.01、66/22 -> 1.86、66/11 -> 1.66。均值腿越长 2Y 越强；极值腿只影响 S。

---

## 四、analyst44 Wave 1 判死诊断（10/10 REJECT）

批次 25Sti06SH512cHa2z2UJfrx，10/10 COMPLETE，**全部 REJECT**。

| # | 机制 | alpha | S | F | 2Y | **TO** | dd |
|---|---|---|---:|---:|---:|---:|---:|
| 6 | 双域修订（netprofit+ebitda）| N1N86q0o | **0.52** | 0.13 | 0.70 | **0.7198** | 0.3208 |
| 4 | -NetDebt/EBITDA | omEZvA86 | 0.11 | 0.01 | -0.30 | 0.6876 | 0.3594 |
| 2 | FCFPS/EPS | 0mY5d9Oq | 0.07 | 0.01 | -0.44 | 1.0897 | 0.4214 |
| 10 | ROE x FCFPS 交互 | pwd3EoXj | 0.05 | 0.01 | 0.61 | 1.2394 | 0.7694 |
| 5 | DPS/EPS | QPv6jqZg | 0.01 | 0.00 | 0.55 | 0.5445 | 0.5011 |
| 8 | TBVPS + ts_mean 66 | A1VEbY9E | -0.15 | -0.04 | 0.20 | **0.0250** | 0.2639 |
| 9 | 广度门控 netprofit/sales | 88RXr7oq | -0.20 | -0.05 | -0.95 | 0.2327 | 0.3300 |
| 1 | ROE 裸水平 | xAr5Q9Al | -0.21 | -0.03 | -0.43 | **1.4790** | 0.6092 |
| 3 | NetProfit/Sales | npvroYxz | -0.28 | -0.06 | -0.66 | 0.4978 | 0.3882 |
| 7 | EBITDA surprise | A1VEbY9l | -0.28 | -0.06 | 1.01 | 0.5345 | 0.7723 |

**根因归因（不是机制错，是缺时序聚合）**：
- analyst44 全字段是 **VECTOR event 型**，vec_avg 在原始日频事件上聚合 => 每天都有新值 => **TO 0.50-1.48 全线爆表**（除 TBVPS 0.025）。
- 对比 analyst93 的成功件：**全部带 ts_mean(..., 66/132) 长窗**。analyst44 Wave 1 十条全是裸水平/裸比率，**一条 ts_mean 都没有**。
- 唯一有正 S 的 N1N86q0o（0.52）恰好是**双域 rank 相加**（内部自带一次截面 rank 平滑）；这佐证「需要先抹平 event 噪声」的假设。
- A1VEbY9E（TBVPS 已带 ts_mean 66）TO 只有 0.025 但 S -0.15 => **TBVPS 水平维度本身无截面预测力**，不是平滑问题。

**=> Wave 11 设计**：同样 10 个机制全部加 ts_mean(..., 132/66/252) 长窗 + 换 industry 轴，做纯净的「长窗能否救活」诊断。

---

## 五、本段新增可复用结论

1. *** **三层杠杆的最优组合 = estimator 视角 x industry 轴 x 132/11 异窗**。单看每层增量：estimator +0.04、industry +0.02、132/11 相对 66/22 +0.02，合计把 S 从 1.50（sector 66/22 analyst）推到 **1.59**。
2. *** **均值腿窗口决定 2Y，极值腿窗口决定 S**：均值腿 66->132 使 2Y 从 1.66 升到 2.01；极值腿 22->11 使 S 从 1.57 升到 1.59。两轴近乎正交。
3. *** **bucket 轴 + 外层 ts_mean 是死路**：外层平滑压 S 0.11 且不修 CW；要 prod 过闸用 industry（0.6615）而不是 bucket（0.6967），因为 industry 同时保住了 S 与 CW。
4. ** **market 轴是不可用轴**：S/F 可以很高（1.56/1.57）但 2Y 塌到 1.49，触碰 2Y 硬闸。
5. ** **极值腿不可删**：bucket 轴上删掉 vec_max 腿 S 从 1.50 掉到 1.27、2Y 从 1.61 掉到 1.16。信息互补是机制核心。
6. ** **VECTOR event 字段没有 ts_mean 长窗就必然换手爆表**：analyst44 十条 TO 0.50-1.48；analyst93 加 66/132 后 TO 0.036-0.049。这是「流量 vs 存量」判据在 VECTOR 数据上的具体化。
7. ** 同一经济量的两个度量视角（analyst vs estimator）互相关高达 0.9487，不构成两颗独立 ATOM；但 estimator 视角本身强 0.04，应优先选 estimator。


