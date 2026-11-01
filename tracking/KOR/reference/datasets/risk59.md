# risk59 — Securities Lending and Short Market Dynamics（KOR / TOP600 / Delay=1）

> 画像日期：2026-10-30。数据源：MCP `get_datasets` + `get_datafields`（region=KOR, delay=1, universe=TOP600, `sharpe_filter_removed=0` ⇒ 16/16 全见）。
> 塔归属：**risk**（KOR/D1 未点亮，塔乘数 **1.3**）。category = `risk` ⇒ **不属禁止组腿域**（用户约束 5 只禁 PV/MODEL/OTHER 之间两两）。

## 1. 数据集事实

| 项 | 值 |
|---|---|
| id / 名称 | `risk59` / Securities Lending and Short Market Dynamics Dataset |
| 覆盖率 | **0.9806**（全 16 字段完全一致 ⇒ 同一张面板） |
| 字段数 | **16，全部 VECTOR**（**每个字段必须先 `vec_avg`/`vec_sum` 降维**） |
| userCount / alphaCount | 220 / **561** |
| valueScore / 塔乘数 | 2 / **1.3** |
| 拥挤度 | ⭐ **极低**：单字段 aC **13–122**，最高 `rsk59_indicativeavailability`=122；最低 `rsk59_last_rate`/`rsk59_short_momentum`=**13** |
| 本质 | **借券市场（securities lending）的实时价格、供给与空头存量**。这是「做空的成本与可行性」数据，不是做空比例的历史快照（区别于 `shortinterest38` 的披露型数据） |

⚠ **与 shortinterest38 的关键差异**：shortinterest38 是**披露口径的空头存量**（低频、有滞后）；risk59 是**借券柜台实时口径**（fee / utilization / 可借量都是市场价与报价），
⇒ 它测的是**做空需求的价格与供给的松紧**，不是"空头有多少"。这是本集唯一的机制来源，也是它拥挤度极低的原因。

## 2. 字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 字段 |
|---|---|---:|---|
| **L1 借券价格（fee）** | 借券市场的成交价：长仓方收的费 / 空头付的费 / 当日增量券的即期价 | 3 | `rsk59_bid_rate`、`rsk59_offer_rate`、`rsk59_last_rate` |
| **L2 供给松紧（utilization）** | 空头存量 ÷ 可借量；S3 预测可借数量 | 2 | `rsk59_s3utilization`、`rsk59_indicativeavailability` |
| **L3 空头存量规模** | 实时空头股数 / 金额 / 占流通比 | 3 | `rsk59_short_interest`、`rsk59_shortinterestnotional`、`rsk59_shortinterestpct` |
| **L4 覆盖天数（DTC）** | 空头存量 ÷ N 日均量（10/30/90） | 3 | `rsk59_daystocover10day`、`..._30day`、`..._90day` |
| **L5 变化率（flow）** | 已归一的变化量：DTC 日/周变化、做空动量 | 3 | `rsk59_dtcdailychg`、`rsk59_dtcweeklychg`、`rsk59_short_momentum` |
| **L6 供应商合成评分** | 拥挤度分 / 挤空风险分（多因子黑盒合成） | 2 | `rsk59_crowded_score`、`rsk59_squeeze_risk` |

**读数要点**：
- **L1/L2 是本集真正的资产**：fee 与 utilization 是**空头需求的价与量**，二者互为交叉验证（Jones-Lamont 2002 用 fee；D'Avolio 2002 用 utilization）。
- **L3/L4 是水平量**（存量 ÷ 规模），按 **F-1 定律（水平量 = 规模代理）** 直接 rank 大概率只是市值暴露 ⇒ **必须取变化率或做同源比值**。
- `shortinterestpct` 是 L3 里唯一已归一化的（占流通比），可作**阴性对照**：若它单独出强信号，说明本集在偷"规模/流动性"暴露。
- **L6 是黑盒合成**，直接当信号等于用供应商的因子；**只作方向佐证，不作主腿**。

## 3. 字段画像五问（A-1）

| 问 | 答 | 决策 |
|---|---|---|
| **测什么** | 做空侧的**价格（fee）、供给松紧（utilization）、存量（SI/DTC）与流量（ΔDTC/做空动量）** | 价格与流量优先；存量只取变化率 |
| **怎么测** | 柜台实时快照（日频） | L1/L2 可用水平（本身即价格），L3/L4 必须取变化 |
| **时间维度** | **混合**：fee/utilization 是**存量型状态量**（慢变），ΔDTC/short_momentum 是**流量** | 状态量 ⇒ 水平 + 长窗 ts_rank；流量 ⇒ 直接用或短窗 |
| **为何存在** | 借券是**有价格的稀缺资源**：可借量有限 ⇒ 空头必须付费；费用高 = 做空需求 > 供给 | 价格即信号，天然连续、有量纲 |
| **可靠性** | cov 0.9806（**2% 缺失**，落在停牌/无借券市场标的） | 需 `ts_backfill` 兜底；VECTOR 必须 `vec_avg` |

**预处理决策**：① 全部字段 `vec_avg(·)`；② L3/L4 走 `ts_delta` 或同源比值；③ fee 类无量纲（annualized percent）可直接 `rank`；
④ utilization 是 0–1 比例，可直接 `rank`/`group_rank`；⑤ 缺失用 `ts_backfill(·, 22)`。

## 4. A-2 收益来源声明

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | **做空者（informed shorts）与借券中介（prime broker / agent lender）**。借券费率是做空方为建立空头必须支付的价格。 |
| **为什么会被错** | 两条独立但同向的机制：**① 卖空约束导致高估**（Miller 1977）—— 借券费高 / 可借量紧 ⇒ 悲观者无法充分表达 ⇒ 价格高于基本面；**② 知情做空的需求价格**（Jones & Lamont 2002）—— 空头愿意付高费说明其信息强度高。两者都指向**高 fee / 高 utilization ⇒ 后续负收益**。 |
| **错了多久修复** | 数周–数季：约束型高估随基本面兑现或借券供给放松而修正；Jones-Lamont 的月度组合持有期即为 1 个月，D'Avolio 的 utilization 效应按季度显现。⇒ 主窗 **22**，辅窗 **66**。 |
| **预期方向** | **fee↑ / utilization↑ ⇒ 后续跌**（做空）；**squeeze_risk↑ / crowded_score↑ ⇒ 后续涨**（挤空：空头被迫回补）。两组方向**必须各测一条**（铁律 B）。 |
| **失效条件** | ① **KOR 卖空禁令期**（2020-03~2021-05 全面禁空、2023-11 起再度全面禁空）⇒ 该窗内 fee/utilization 无经济含义或数据停滞，**逐年 S 必须逐段看**；② 借券费被平台/供应商截尾（hard-to-borrow 股票被剔除）⇒ 信号在高费端被截断；③ VECTOR 聚合口径（`vec_avg` vs `vec_max`）改变 fee 的含义。 |

## 5. 双通道取证

| 通道 | 状态 | 证据 |
|---|---|---|
| **A｜平台论坛** | ✅ **已查（2026-10-30）** | `tools/forum_recon.py`，question_key **`c82242fab5`**（问句：证券借贷费率/借券利用率/覆盖天数 能否作为 KOR 空头拥挤与预期收益的信号），`found=true` / 3 篇 / 1 轮命中即收束 |
| **B｜外部文献** | ✅ 形态锚点已定 | Jones & Lamont (2002, *RFS*「Short sale constraints and stock returns」) 用借券费做空头约束代理；D'Avolio (2002, *JFE*「The market for borrowing stock」) 用 utilization 刻画供给松紧；Engelberg–Reed–Ringgenberg (2018, *JF*) 指出**借券费的时间序列二阶矩（方差）比水平/变化率更可预测**。⚠ 三者均非 KOR 样本 ⇒ **只作假说与形态依据，不作本区证据** |

### 5.1 A 通道逐条裁决（3 篇）

| # | 文章 | 判定 |
|---|---|---|
| 1 | 证券借贷基础概念贴 | ❌ 术语解释，无表达 |
| 2 | 做空数据与 short interest 用法 | ❌ 讲的是披露型 SI（≈ 本区 `shortinterest38`），与本集的柜台实时口径不同源 |
| 3 | **《贷款费率的时间序列方差》**（64 赞，`43624312881943`） | ⭐ **唯一可用且是本集的正解** —— 给了**已提交**的单数据集 ATOM 模板与完整消融 |

### 5.2 转移模板（post #3，原文可复现）

```
reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), exchange))
```
ASI 实测 `npK8Vx1M`：**S 1.89 / F 1.54 / TO 14.1% / margin 13.4bp / 2Y 1.63 / subU 1.66 / prod 0.6648 / self 0.20**，
10 年逐年全正（最弱 2019 = 1.02）。

**该贴给出的消融读数（直接作为本区的对照实验设计）**：

| 消融 | 读数 | 含义（贴主自己的解释） |
|---|---|---|
| `ts_delta(x,22)` 反向 | **0.09** | 方向本身不是信号 ⇒ **变化率安慰剂** |
| 除以横截面均值做 CV 归一 | **0.61** | 信号活在**绝对尺度**里（跨股票价差有意义），归一即毁 |
| `group_rank` 替 `group_zscore` | **0.71 vs 1.89** | 秩化丢掉尾部幅度 ⇒ 本族**必须用 zscore 保幅度** |
| 窗口 5 / 22 / 66 / 252 | 1.81 / **1.89** / 1.46 / 1.09（TO 40.6 / 14.1 / 8.2 / 5.7%） | 22 ≈ 一个月的自然尺度；短窗胜率不抵换手 |
| `ts_std_dev` 替 `ts_covariance` | **1.98（更高）但 robust 比 1.70 < 1.78 ⇒ FAIL** | ⭐ **robust 闸是比率闸**：`LOW_ROBUST_UNIVERSE_SHARPE.limit ≈ 全样本 S × 0.9`；`ts_std_dev` 的 √ 凹变换放大**小票尾部权重**，全样本看着更高、截断后塌；`ts_covariance` 保持凸性 ⇒ 免票过闸 |

**机制解释（贴主版）**：借券费的水平差异是"贵/便宜"，而**费的方差**是"这只票的做空成本有多不确定"——
不确定性高的票，做空方要求的补偿高、持仓意愿低，价格被系统性抬高 ⇒ **方差↑ ⇒ 后续跌**（所以模板里是 `reverse`）。

### 5.3 双通道裁决

| 情形 | 判定 |
|---|---|
| A 有模板、B 有机制、且**指向同一机制** | ⭐ **最高优先级组装**（按 A-1 五问自建骨架，用 B 的机制句定方向与持有期） |
| 冲突 | 无：A 的「方差↑ ⇒ 跌」与 B 的「二阶矩可预测」同向；A 的「变化率无效」与 Miller/Jones-Lamont 的**水平**机制也不矛盾（水平 ≠ 一阶差分） |
| 未验证项 | ① KOR 是否也有"方差 > 水平"的排序；② `vec_avg` 聚合后 fee 的方差是否仍承载"不确定性"含义（**VECTOR 字段的方差 = 跨快照聚合后的日度方差，不是跨做市商离散度**）⇒ 本波必须实测 |

⚠ **与 §4 的张力（必须实测裁决）**：A-2 的 Miller/Jones-Lamont 讲的是**水平**（高费 ⇒ 负收益），
post #3 讲的是**方差**（高费方差 ⇒ 负收益），且它自己的 `ts_delta` 安慰剂只有 0.09。
⇒ 本波同时放**水平腿**与**方差腿**做同波对照，谁强留谁，**不许两个都留后加权合成**。

## 6. 候选设计（wave 201，5 腿 = 模板核 2 向 + 3 对照）

| # | 表达式 | 角色 | 对应消融 |
|---|---|---|---|
| **T1** | `hump(reverse(group_zscore(ts_covariance(vec_avg(rsk59_offer_rate), vec_avg(rsk59_offer_rate), 22), sector)), hump=0.003)` | ⭐ **模板核（主方向）** | post #3 原式（`exchange`→`sector`，加 KOR 冠军壳 `hump`） |
| **T2** | `hump(group_zscore(ts_covariance(vec_avg(rsk59_offer_rate), vec_avg(rsk59_offer_rate), 22), sector), hump=0.003)` | **方向对侧**（铁律 B） | 同式不加 `reverse` |
| **T3** | `hump(reverse(group_zscore(ts_std_dev(vec_avg(rsk59_offer_rate), 22), sector)), hump=0.003)` | **robust 比率闸对照** | `ts_std_dev` 对 `ts_covariance` |
| **T4** | `hump(reverse(group_zscore(ts_delta(vec_avg(rsk59_offer_rate), 22), sector)), hump=0.003)` | **安慰剂**（预期 ≈ 0） | `ts_delta` 对 `ts_covariance` |
| **T5** | `hump(group_rank(vec_avg(rsk59_offer_rate), sector), hump=0.003)` | **水平腿**（A-2 的 Miller 机制） | 水平对二阶矩 |

**本波要回答的三个问题**（不发散）：
1. KOR 上「方差 ⇒ 负收益」是否成立（T1 vs T2 的方向裁决 + T4 安慰剂必须 ≈ 0）；
2. 信号是否也在**水平**里（T5）——若 T5 强于 T1，则 §4 的 Miller 机制才是本区主机制，改走水平族；
3. `ts_std_dev` 是否同样被 robust 比率闸拦（T3 的 robust 读数 vs T1）。

⚠ **壳层说明**：全部腿同加 `hump=0.003`（KOR 冠军壳、控制换手），**同波内一致** ⇒ 不影响腿间比较；
不加 `tail`/`vector_neut`（本机制不含市值/流动性博弈，见 §3 A-1 第 4 问 = 否）。
⚠ **留作救援（不合成本波）**：`divide(vec_avg(rsk59_offer_rate), vec_avg(rsk59_bid_rate))`（同源买卖价差比率）、
`vec_avg(rsk59_last_rate)`（aC=13，最不拥挤的成交价）、`vec_avg(rsk59_s3utilization)`（供给口径交叉验证）、
`vec_avg(rsk59_squeeze_risk)`（正向挤空腿）。任一条**单腿**在本波读数上分不出高下时才进下一波。

## 7. 实测记录（wave 201，2026-10-30 全部收批）

### 7.1 全波读数（KOR/TOP600/D1，STATISTICAL/decay=4，5 腿）

| 腿 | 表达式要点 | alpha | S | F | 2Y | TO | subU | margin |
|---|---|---|---|---|---|---|---|---|
| **T1** 模板核（`ts_covariance` 反向） | `hump(reverse(group_zscore(ts_covariance(vec_avg(offer_rate),vec_avg(offer_rate),22),sector)))` | `58ENXrLz` | **0.14** | 0.04 | −0.10 | .1481 | 0.38 | .000154 |
| **T2** 方向对侧（同式去 reverse） | 同上不 reverse | `Xg9X0Vkz` | **−0.27** | −0.10 | −0.04 | .1479 | −0.47 | −.000287 |
| **T3** robust 比率闸对照（`ts_std_dev`） | `hump(reverse(group_zscore(ts_std_dev(vec_avg(offer_rate),22),sector)))` | `2rAP3EJY` | **0.39** | 0.17 | 0.48 | .1165 | 0.61 | .000426 |
| **T4** 安慰剂（`ts_delta`） | `hump(reverse(group_zscore(ts_delta(vec_avg(offer_rate),22),sector)))` | `LLMO0eRe` | **0.04** | 0.00 | −0.20 | .2725 | 0.18 | .000020 |
| **T5** 水平腿（Miller 机制） | `hump(group_rank(vec_avg(offer_rate),sector))` | **`j2YNqoNZ`** | **−1.02** | −0.65 | **−1.76** | .1253 | −0.86 | −.000814 |

**§7.1.1 T5「空批」实为收割滞后（2026-10-30 06:15 观测 → 06:24 收批，已于 06:28 平台复核）**：
T5 单独成批（multisim `W8E0i9EN571byFVkztEg9x`，n=1）。轮询第 9 分钟 `batch_status` 曾返回
`parent_status=COMPLETE` / `child_count=0` / `children=[]`，`harvest_multisim_alphas` 同步报
`No children found (multisim may still be processing)`。**但该批随后正常派生并完成**，产出 `j2YNqoNZ`：
平台 `get_alpha_details` 实测 S −1.02 / F −0.65 / 2Y −1.76 / subU −0.86 / TO .1253 /
long 297 short 329 / `ra_failed_checks` 含 LOW_SHARPE·LOW_FITNESS·CONCENTRATED_WEIGHT·
LOW_SUB_UNIVERSE_SHARPE·LOW_2Y_SHARPE（CW 项无 value/limit 字段，按 fail 处理）。

⚠ **教训（写给下一次）**：`parent COMPLETE + children []` 与 `No children found` **不能**当作「没有 alpha」；
平台收割存在滞后，判「无读数」前必须等 pipeline 自身轮询结束（本次 9 分钟不够），
且必须用 `get_alpha_details(alpha_id)` 或 wave 行回写来确认，而不是只信 `batch_status` 的中间态。
我一度据此写成「T5 无 alpha」，是**错误取证**，已按实测改正。

KOR 闸线：S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / CW ≤ 0.1 / subU ≥ 0.05；换手甜区 .075–.136。
5 腿全部 `REJECT`（`batch_get_alpha_metrics.prescreen`）；其中 T5 的 |S| 最大（1.02），`2Y` 反向即 **+1.76**。

### 7.2 归因（铁律 F：逐年 + 单年集中度 + 十年覆盖）

#### 7.2.1 协方差族最强腿 T3 `2rAP3EJY`（`get_alpha_yearly_stats`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | **无数据** | 0.22 | **1.87** | −0.46 | 0.82 | 0.23 | −0.07 | 0.06 | 0.72 | 0.23 |
| TO | 0 | .1269 | .1191 | .1116 | .1108 | .1120 | .1355 | .1163 | .1088 | .1076 |
| PnL(万) | 0 | 15.1 | **112.6** | −25.1 | 53.9 | 16.8 | −5.9 | 3.4 | 45.5 | 14.2 |

三条读数，条条独立判死：

1. **S<1.0 的年份 9/9（100%）** ⇒ 2Y 闸（≥1.58）**在任何参数档都结构性不可达** —— 全年最好的 2016 也只有 1.87，其余八年全 < 0.9。按发波决策表：⛔ 停扫 decay / 平滑 / 门控，**换机制族**。
2. **单年集中度 48.9%**（2016 的 112.6 万 / 全期 230.4 万）⇒ >30% 的过拟合指纹。剔除 2016 后全期 PnL 仅 117.8 万、S 掉到 0.2 量级。
3. **2014 整年零数据**（longCount=0 / PnL=0，数据自 2015 起）⇒ 有效历史 2015–2023 = **9 年**，不满足用户口径「近十年都要有数据」。

> ⚠ **这三条判死的是「协方差/方差族」，不是数据集**——见 §7.2.2。同一波的 T5 水平腿推翻了下游的整塔闭合结论。

#### 7.2.2 ★ 水平腿 T5 `j2YNqoNZ`（同一波，`get_alpha_yearly_stats` + `get_alpha_pnl`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S（原向） | **无数据** | −0.69 | **+0.74** | **−2.02** | −0.73 | −0.96 | −0.74 | **−1.52** | **−1.42** | **−1.80** |
| TO | 0 | .1504 | .1420 | .1356 | .1378 | .1340 | .1443 | .1265 | .0802 | .0769 |
| PnL(万) | 0 | −35.7 | +32.2 | −92.5 | −45.6 | −47.0 | −43.5 | −75.4 | −69.7 | −96.4 |

读法与 T3 相反，**方向做反才是真相**：

1. **8/9 年为负**，且 2021–2023 逐年走强（−1.52 / −1.42 / −1.80）⇒ 反向即近年 S ≈ +1.4~+1.8。
   平台回填的 `two_year_sharpe = −1.76` ⇒ **反向 ≈ +1.76，越过 1.58 闸**。
2. **单年集中度低**：最大单年 |PnL| = 2017 的 92.5 万 / 全期 473.7 万 ≈ **19.5%**（< 30% 过拟合线）；
   2016 是唯一正年（+32.2 万）且量级小 ⇒ 不是靠一年行情。
3. **PnL 曲线单调同向累积**（2015 起持续下台阶至 −474 万），无锯齿、无单段暴涨 ⇒ 是系统性暴露，不是尖峰。
4. **2014 仍零数据**（与 T3 同）⇒ **十年覆盖该数据集本身不达标**（数据自 2015 起，9 年）。
   但用户口径允许「覆盖率可动态调整」，而平台仿真窗口本就是 2014-01-01~2023-12-31；
   2014 无数据使 2Y/全期读数不受影响（2Y 只看 2022–2023），**故十年覆盖仅限制「可提交性」，不限制继续挖**。

**结论**：risk59 的**一阶矩（借券费率水平）有信号，二阶矩（方差/协方差）没有**。
这直接呼应 §4 的 Miller 机制假说（卖空约束下悲观观点进不了价格 ⇒ 高费率股被高估 ⇒ 后续跑输）——
但**方向是「高费率 ⇒ 跑输」，与 §4 预设的「水平族方向」一致，只是需要 `reverse` 落地**。

**遗留障碍**：CW fail（`CONCENTRATED_WEIGHT`，反向不改善），S 全期仅 ≈ +1.02（差 0.56），F ≈ 0.65（差 0.35）。
按 KOR 读数三分法（S 1.0–1.58）**不判死**，属「构型没找对」，继续升级构型。

### 7.3 三条对照的裁决

| 对照 | 读数 | 裁决 |
|---|---|---|
| **方向（T1 vs T2）** | T1 0.14 / T2 −0.27 | reverse 方向「更好」但两者都远离零档；T2 的副指标更差（subU −0.47、F −0.10）⇒ **不存在可用的方向性**，不是「反向做就行」 |
| **代数形式（T3 vs T1）** | `ts_std_dev` 0.39 > `ts_covariance` 0.14 | 论坛模板的 `ts_covariance(x,x)` 构造**没有增量**——二阶矩信息全在 `ts_std_dev` 里，`cov(x,x)` 只是把同一样本再乘一遍自己、放大了尾部。ASI 上的方差配方**不可移植到 KOR** |
| **安慰剂（T4）** | 0.04，且 TO .2725（**出换手带 2 倍**） | 安慰剂同时不达 S 与换手 ⇒ 本波的读数**不是换手造成的假象**，是信号本身没有 |

### 7.4 预注册判死标准 vs 实际

预注册（§6）：4 腿 `max|S| < 0.8` 或 `max|2Y| < 0.8` 或全部 CW > 0.1 ⇒ 机制判死、闭合数据集、不扫 decay/窗口/中性化。
实际：**协方差族 4 腿** `max|S| = 0.39`、`max|2Y| = 0.48` ⇒ 两条判死线同时命中，
**但同一波的第 5 腿（水平腿 T5）|S| = 1.02 / |2Y| = 1.76 越过了判死线**，故裁决必须分族：

- ✅ **协方差 / 方差族判死**：`ts_covariance(x,x)`、`ts_std_dev`、`ts_delta` 三支全部 < 0.4。
  不再扫其 `decay` / 平滑器 / 中性化档 / 窗口谱（已死轴）。
- ⛔ **数据集级判死不成立**（我 06:20 时据 4 腿写下的「risk59 闭环判死」是错的，已在 §7.2.2 改正）：
  水平族（`group_rank(vec_avg(offer_rate))` 的反向）是全波最强腿，`2Y` 反向 **+1.76**。
- 救援清单（§6 末）**仍不启用**，但理由变了：它们与 T5 同为**一阶矩**族，而一阶矩族**没有死**——
  只是本波先要解决 T5 的 CW 与强度问题，同族换聚合口径须等主腿构型定稿后再说（避免同波多点开花）。

### 7.5 RISK 塔整塔闭合（同批取证，非本波实测）

| 数据集 | cov | 字段 | aC | 历史回测 | 最佳读数 | 判据 |
|---|---|---|---|---|---|---|
| risk59 | .98 | 16 | 463 | 本波 5 腿 | 协方差族 max\|S\| 0.39；**水平腿 \|S\| 1.02 / 2Y 反向 +1.76** | **不判死**：方差族死、一阶矩族活（wave 202 续挖）；2014 无数据 ⇒ 十年覆盖不达标，只限制可提交性 |
| risk71 | .67 | 7 | 250 | 16 | S 2.20 但 **TO .829 / 2Y −0.92**；全族最佳 2Y = **0.16** | 2Y 结构性死；且唯一强腿是 `residualized_return_asia_minvol1m`（收益型字段，与 PV 族同源） |
| risk60 | .82 | 5 | 662 | 8 | bestS 0.18 | 已判死（3 条 dead_end） |
| risk68 | 1.0 | 5 | 193 | 0 | — | 纯风险暴露（beta/size 类），非信号 |
| risk70 | .98 | 87 | 6112 | 96 | — | Axioma 式风险暴露矩阵，9 成字段是暴露量不是信号 |
| risk88 | .97 | 64 | 1205 | 0 | — | 同为风险暴露族 |
| risk72 | .60 | 40 | 39 | 3 | bestS 0.00 | 无 live 字段 |

⇒ **RISK 塔其余 6 个数据集闭合；risk59 例外继续挖**（原写「整塔闭合」已被 §7.2.2 推翻）。
即：RISK 塔仍有 1 个活口 = risk59 的一阶矩族，其余（risk71/60/68/70/88/72）不再派发波次。

⚠ `risk71` 的 `residualized_return_asia_minvol1m` 家族若要复用，必须先解决两点：① 2Y 全族 ≤0.16；
② 它是收益型字段，与已提交 PV 族大概率同分母 ⇒ prod 相关性风险。本条只作记录，**不构成下一步建议**。

## 8. wave 202（同一数据集，因果链续挖）—— 2026-10-30 发波

**波次三问（铁律 G）**

1. **继承**：T5 是全波唯一越过判死线的腿（|S| 1.02 / |2Y| 1.76），本波只在其邻域变动；
   方差族（T1–T4）继承为**已死轴**，本波 0 条。
2. **准入（禁碰）**：`ts_covariance` / `ts_std_dev` / `ts_delta` 三支；`decay` 扫描（已死轴）；
   `truncation` 扫描（锁定）；`universe`（唯一合法 TOP600）；救援清单四个字段（等同族多点开花，暂缓）。
3. **收窄**：候选 5 → **3**（只保留单变量对照）。

**3 腿设计（每条只动一个变量 vs T5）**

| 腿 | 表达式 | 动的变量 | 想解决什么 |
|---|---|---|---|
| **A** 基线反向 + CW 破法 | `hump(subtract(0.5, group_rank(vec_avg(rsk59_offer_rate), sector)), hump=0.003)` | 方向（reverse）+ 居中 | 验证反向是否给出 ≈+1.0/+1.76；同时按 `_probe-sop.md` 的**唯一 CW 破法**居中进 hump |
| **B** 保强度 | `hump(reverse(group_zscore(vec_avg(rsk59_offer_rate), sector)), hump=0.003)` | `group_rank` → `group_zscore` | 秩化丢掉了强度信息，zscore 保留极端值幅度 |
| **C** 降噪 | `hump(subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_offer_rate), 22), sector)), hump=0.003)` | 加 22 日时间聚合 | 借券费率日频抖动大；KOR 实证「降频聚合后再排序」可同时提 S 与压 TO |

设置沿用 wave 201：KOR/TOP600/D1 · STATISTICAL · decay 4 · trunc 0.08。发批前已过
`preflight_expressions(dataset_id=1150)`（3/3 valid，字段实名核对通过）。

**预注册判读标准**：
- 任一腿 S ≥ 1.58 且 2Y ≥ 1.58 ⇒ 进全闸验证（重点 INV / CW）→ prod/self → 提交判定；
- S 1.3–1.58 ⇒ 继续构型（KOR 三分法），下一轴 = `industry` 分组 or `vec_max` 聚合；
- 三腿全部 S < 1.0 ⇒ 反向不能复现 T5 的镜像 ⇒ 说明 −1.02 里有**非线性**成分（hump × decay × 符号），
  记录后本族降级，转 news104。

⚠ **同日已发现并修复的工程事故**：`tracking/KOR/data/wqb.db` 使 toolkit `_walk_up(campaign_dir)`
把战役目录认成工作区根，pipeline 写在孤儿库、`wqb-db` MCP 写根库（见 §7.1.1 后的台账条目与本波发波命令的
`WQB_DB_PATH` 钉死）。**纪律：pipeline 发波必须显式钉 `WQB_DB_PATH=<repo>/data/wqb.db`。**

## 9. wave 203（同数据集强度推进，2026-10-30）—— 近闸定向挖掘

**为什么是这一波**：wave 202 的 `QPvr1vPM` 是**全 KOR 近期记录里唯一 2Y 过闸**的腿
（S 1.02 / F 0.67 / **2Y 1.80** / TO 0.135 / subU 0.95 / margin 8.52bp / inv 0.91），
闸缺口只剩 **S（1.02→1.58，+55%）** 一条；F 由同一读数机械决定（`F=1.58×sqrt(.0576/.135)=1.03`），
⇒ 本波的唯一目标 = **抬幅度**，不动方向、不动数据集、不动换手结构。

**波次三问（铁律 G）**

1. **继承**：`QPvr1vPM` 的壳层 `hump(reverse(group_zscore(vec_avg(F), sector)), hump=0.003)` 整层冻结；
   方向裁决（reverse 有效）、二阶矩判死（§7.4）继承为**准入禁碰**。
2. **准入（禁碰）**：`ts_covariance`/`ts_std_dev`/`ts_delta` 三支；`decay` 扫描；`truncation`；`universe`；
   任何两字段相加；任何一阶矩以外的机制族。
3. **收窄**：候选 3 → **3，但搜索空间从「3 种结构」收成「1 个赢家 × 3 个单变量突变」**（每腿只改一处）。

**3 腿设计（每腿恰好一个单变量 vs `QPvr1vPM`）**

| 腿 | 表达式 | 动的唯一变量 | 机制假设（为什么会更响） |
|---|---|---|---|
| **S1** | `hump(reverse(group_zscore(vec_max(rsk59_offer_rate), sector)), hump=0.003)` | 聚合 `vec_avg`→`vec_max` | 借券费是**稀缺资源的报价分布**：空头真正要付的是**当日最贵那一档**；均值把尾部（hard-to-borrow）磨平了，而强约束恰好只在尾部 |
| **S2** | `hump(reverse(group_zscore(vec_avg(rsk59_last_rate), sector)), hump=0.003)` | 字段 `offer_rate`→`last_rate`（aC 13，全表最不拥挤） | `offer_rate` 是**报价**（含做市 markup），`last_rate` 是**成交价** ⇒ 更接近空头真实付费的均衡价，噪声更小 |
| **S3** | `hump(reverse(group_zscore(vec_avg(rsk59_offer_rate), subindustry)), hump=0.003)` | 分组轴 `sector`→`subindustry` | SOP「换细轴是无损轴」：sector 在 KOR 已饱和，同行业内借券费差异才是纯股票层面的做空约束 |

**预注册判读**：
- 任一腿 S ≥ 1.58 且 2Y ≥ 1.58 ⇒ 直接进全闸（重点 CW/CLUSTER/inv）→ prod/self → 提交判定；
- S 1.3–1.58 ⇒ 该腿的变量记为正贡献，下一波只在该腿上再突变一处；
- 三腿全部 S ≤ 1.1 ⇒ 一阶矩族的幅度上限 ≈1.0，**本族降级**，risk59 转 §6 救援清单（`s3utilization`/买卖价差比率）或整体停投。
- ⚠ 三条腿**都不许**在本波内做二次加权合成（混信号铁律）。

### 9.1 ⚠ 台账更正：wave 203 的 3 条 risk59 腿**从未派发**（2026-10-30 复核）

`list_expressions(wave=203)` 实测：wave 203 是**混合波**——4 条 `news_sentiment_transfer` 腿（有 alpha_id、
TO≈1.09 全灭，即后来 wave 208 又被判死集拦下的同一批机制）+ 3 条本文件预注册的 risk59 腿
（`vec_max` / `last_rate` / `subindustry`，`status=pending`、`alpha_id=null`）。
`get_wave_result(203)` 的读数（max|S| 0.57 / max 2Y 0.54）**全部来自 news 腿，不含任何 risk59 读数**。
⇒ **本文件 §9 的 S1/S2/S3 假设至今未测**，不得把 wave 203 的 FAIL 当成它们的结论。
候选去向：wave 213（若 wave 212 显示字段/机制比分组轴更关键，则优先补 `vec_max` 与 `last_rate`）。

## 10. wave 212（借券费「价量合成」与分组轴，2026-10-30 发波）

**为什么是这一波**：wave 202 的 `QPvr1vPM` 仍是全线唯一 S≥1.0 且 2Y≥1.8 的腿。
本波不再扫单字段形态（§9 已把单字段三个方向排好队，且 rank/zscore/ts_mean 已证伪两个），
改问**「价与量能不能合成一个更强的约束度量」**——这是 D'Avolio (2002) 的原命题：
fee 是空头**愿意支付的价格**，utilization 是**实际占用比例**，两者同时高才是真约束。

**强度算术（先把杠杆想清楚，再花槽位）**：
`F = S·√(R/max(TO, .125))`，实测 `R=.0576 / TO=.135 ⇒ F=.67`。
⇒ **S 一旦到 1.58，F 机械地到 1.03**（同 R/TO），且若 TO 掉进 .125 以下（分母封顶），
只要 R 仍 ≥ .05，F 也会自动过。**本波唯一目标仍是 S，且不许用换手换 S。**

**4 腿（每腿回答一个不同问题，互不为变体）**

| 腿 | 表达式 | 问的问题 | 机制假设 |
|---|---|---|---|
| **P1** | `hump(reverse(add(group_zscore(vec_avg(rsk59_offer_rate), sector), group_zscore(vec_avg(rsk59_s3utilization), sector))), hump=0.003)` | 价 + 量 合成 | D'Avolio 原命题：费高**且**占用高 = 约束最紧 ⇒ 后续跌最狠。两个 zscore 无量纲 ⇒ `add` 不触 unitHandling |
| **P2** | `hump(reverse(subtract(group_zscore(vec_avg(rsk59_offer_rate), sector), group_zscore(vec_avg(rsk59_s3utilization), sector))), hump=0.003)` | 价 − 量 背离 | 「价高但券还多」= 中介**惜借**（预期未来更紧）⇒ 比单纯高价更隐蔽的约束信号 |
| **P3** | `hump(reverse(group_zscore(vec_avg(rsk59_offer_rate), industry)), hump=0.003)` | 分组轴 sector→industry | 单变量对照 `QPvr1vPM`：借券费是**行业内**相对约束，sector 太粗 |
| **P4** | `hump(reverse(group_zscore(vec_avg(rsk59_s3utilization), sector)), hump=0.003)` | utilization 独立成腿 | 量的**第二机制**（D'Avolio 主变量）。若单独出信号 = 一颗新的 ATOM，且与 P1 的差值就是"合成的增量" |

**预注册判读**
- 任一腿 S ≥ 1.58 且 2Y ≥ 1.58 ⇒ 全闸（CW/CLUSTER/inv）→ prod/self → 提交判定；
- **P1 vs P4** 的差值 = 价量合成的增量。若 P1 > max(P2,P3,P4) + 0.15 ⇒ 「合成」是正贡献，下一波沿合成走；
  若 P1 与 P4 持平 ⇒ 增量全来自 utilization，fee 是冗余的 ⇒ 下一波只打 utilization 自己的几何；
- 四腿全部 S ≤ 1.1 ⇒ 一阶矩族（含价量合成）幅度上限 ≈1.0 确认 ⇒ risk59 主攻结束，
  转 §6 救援清单的**最后两个未测点**（`vec_max` / `last_rate`，wave 213）后整族降级；
- ⚠ P1 与 P4 嵌套（P4 是 P1 的一个分量），这是刻意的**可归因设计**，不是"重复腿"。

## 11. wave 212 实测（价量合成 / 分组轴 / utilization）—— 一阶矩族收口（2026-10-30）

KOR/TOP600/D1 · STATISTICAL · decay 4 · trunc 0.08 · unitHandling VERIFY · nanHandling OFF。
gate：`total=4 passed=3 failed=1`（P1 `add` 双腿被 `[POISON:equal_weight_leg_add]` 拦，id 85223 置 dropped）。
**实发 3 腿**（2 批：n=3 / n=3，串行 1 槽 ⇒ 并发 1 ≤ 2）。

| 腿 | 表达式 | S | F | TO | margin | 判 |
|---|---|---|---|---|---|---|
| P2 | `hump(reverse(subtract(z(vec_avg(offer_rate),sector), z(vec_avg(s3utilization),sector))), .003)` | 0.55 | 0.25 | .1384 | 4.14 bp | 价−量价差 = **稀释** |
| P3 | `hump(reverse(z(vec_avg(offer_rate), **industry**)), .003)` | **0.96** | 0.60 | .1279 | 7.77 bp | 换 industry 轴**略弱**于 sector（QPvr1vPM 1.02 / .135 / 8.52 bp） |
| P4 | `hump(reverse(z(vec_avg(s3utilization), sector)), .003)` | **0.09** | 0.02 | .1273 | 0.71 bp | utilization 在 KOR **无信号** |

`wave_results` id=1683 / verdict **FAIL** / max\|S\|=0.96 / max 2Y=1.40 / candidates 0 / near 0。

### 11.1 归因（决定性：价量合成的前提不成立）

- **utilization 单独 S 0.09** ⇒ D'Avolio「费高**且**占用高」命题的第二分量在 KOR 信息量≈0。
  推论（数学，不是经验）：乘法交互（P5）与 utilization 门控（P6）**不可能产生增量**——调制变量本身无信号
  ⇒ 两腿（id 85230 / 85231）**发波前 kill，未消耗仿真槽**。这是本波最有价值的阴性结论：
  **「价量合成」在 KOR 失败的原因不是合成方式，而是第二分量不存在。**
- **P2 0.55 < P3 0.96 < QPvr1vPM 1.02** ⇒ 任何引入 utilization 的形态都是纯稀释，台阶单调。
- **P3 vs QPvr1vPM（同壳单变量 sector→industry）**：S −0.06 / TO −.0071 / margin −0.75 bp
  ⇒ **细分组轴不带来强度，回退 sector**（与 SOP「换细轴是无损轴」在**维度**上无损、在**幅度**上有损不矛盾）。

### 11.2 族收口判定

一阶矩（水平）族已测形态：`sector` **1.02**（QPvr1vPM）· `industry` 0.96 · `utilization` 0.09 · `价−量` 0.55
⇒ **上界 1.02 确认**。与 wave 201 的二阶矩族（方差/协方差/差分，上界 0.39）合并后，
**risk59 三条形态轴（level / variance / delta）全部完成**。

剩余未测点仅 §9.1 的 `vec_max` / `last_rate` / `subindustry` 三条 ⇒ **wave 213 已发**；
若仍 ≤1.1 ⇒ risk59 整族降级、risk 塔关闭（与 `risk68.md` §9.1 的塔级结论合并）。

## 12. wave 213 实测（§9.1 三条从未派发的腿）—— risk59 整族收口（2026-10-30）

设置同 wave 212。3 腿实发（2 批 n=2 / n=1，串行 1 槽）。

| 腿 | 表达式 | S | F | TO | margin | 判 |
|---|---|---|---|---|---|---|
| 213-a | `hump(reverse(group_zscore(vec_max(offer_rate), sector)), .003)` | 1.02 | 0.67 | .1351 | 8.53 bp | **与 QPvr1vPM（vec_avg 版 1.02 / .135 / 8.52 bp）逐项相同** ⇒ 该字段当日档位近乎唯一，`vec_max` ≡ `vec_avg`，**聚合换不出强度** |
| 213-b | `hump(reverse(group_zscore(vec_avg(last_rate), sector)), .003)` | **1.04** | 0.67 | .1428 | 8.41 bp | ★ **本族新高**（S +0.02 / **2Y 2.02**），但 TO 升到 .1428 ⇒ F 仍 .67（F 只看 S/TO/R 之比） |
| 213-c | `hump(reverse(group_zscore(vec_avg(offer_rate), subindustry)), .003)` | 0.70 | 0.36 | .1281 | 5.22 bp | 细轴第三次更差（sector 1.02 > industry 0.96 > subindustry 0.70）⇒ **轴越细越弱，结论与 212-P3 一致且更陡** |

`wave_results` wave=213 → closed，max\|S\|=**1.04**、max 2Y=**2.02**、candidates 0 / near 2。

### 12.1 结论：risk59 整族收口，risk 塔关闭

1. **上界 = 1.04**（`d5W8Pn7X`，`last_rate` 版），距闸 **+52%**；F .67 → 需 1.0，
   即便把 TO 压到 .125 封顶（同 S/R）也只有 F .716 ⇒ **S 是唯一活口且差得太远**。
2. **三条单变量轴全部试完**：聚合（`vec_avg` → `vec_max`，平手）· 字段（`offer_rate` → `last_rate`，+0.02）
   · 分组（sector → industry → subindustry，单调更差）⇒ **没有任何一条能把 S 抬 50%**。
3. 与 wave 201 合并：**三条形态轴（level 1.04 / variance 0.39 / delta 0.04）全部实测完成**。
4. ⇒ **risk59 降级为「近闸素材」（`last_rate` 版 S 1.04 / 2Y 2.02 留档），不再投配额**；
   **risk 塔关闭**（合并 `risk68.md` §9.1 与 roadmap §4 的 level 族禁令）。

### 12.2 唯一未试且不建议独自尝试的杠杆（写死，避免后人反复提）

**缩短 IS 窗口**（`startDate` 2013 → 2018）：`last_rate` 版 2Y=2.02 远高于全样本 1.04，
说明近年强度是长样本的约 2 倍。这条能一次改写 S 与 2Y，但**违反用户约束 4 的十年样本精神**
（且 LADDER/2Y 同源会让读数失去独立性）⇒ 需用户明确授权才做，本波**不做**。

## 13. risk 塔最终台账（KOR/TOP600/D1）

| 数据集 | 形态 | 结果 | 波次 |
|---|---|---|---|
| risk59 | level（fee / utilization / 分组轴 / 聚合） | **上界 1.04** | 201–213 |
| risk59 | variance / covariance / delta | 上界 0.39 | 201 |
| risk68 | — | 4/4 全灭，max\|S\| 0.50，2Y 6/10 年 <1.0 | 194 |
| risk72 | — | 0 槽（5 字段同 description，同量拷贝） | 193b |
| risk88 | — | `ri_*` 风格载荷 | 历史 |
| risk60 / risk71 | — | 已判死（crowding / residual reversal） | 历史 |

**塔结论：KOR risk 塔在 unpit 状态下无可用攻击面 ⇒ 关闭。** 唯一可复用资产 = `last_rate` 版
`hump(reverse(group_zscore(vec_avg(rsk59_last_rate), sector)), hump=0.003)`（S 1.04 / 2Y 2.02 / TO .1428 / margin 8.41bp），
仅在出现「跨塔弱相关腿」时才值得拿出来做组合分量。
