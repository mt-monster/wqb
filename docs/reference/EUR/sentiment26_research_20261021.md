# sentiment26（DNS 网站热度）定向开发 — 研究依据

> 2026-10-21 ｜ 来源：平台论坛 + 外部论文 ｜ 目标：regular ATOM alpha

## 一、数据集定性

平台目录原文：**Website Popularity Ranking Dataset**（被动 DNS 流量，统计每个域名被多少独立客户端 IP 访问）。
⇒ 这是**「投资者/公众注意力」代理数据**，与 Google SVI、Similarweb 同类。

⚠️ 论坛帖子《sentiment26 突发新闻密度体会》把数据集说成了新闻密度——**错误**，以平台目录为准。

⚠️ `snt26_wq_pit` 是时间戳字段（campaign 曾跑出 2Y 1.98 的 d1 候选 `XgRJNK31`——是伪信号，弃用）。

## 二、外部论文（两个对立机制）

| 论文 | 数据 | 结论 | 方向 |
|---|---|---|---|
| **Da, Engelberg & Gao (2011) RFS** "In Search of Attention" | Google SVI | 注意力飙升 → 散户追涨 → 短期抬价 → **随后反转** | 异常注意力取**负** |
| Barber & Odean (2008) | 账户交易 | 注意力驱动买入（散户只从被注意的股票里挑） | 同上 |
| **Armstrong, Konchitchki & Zhang (2025) TAR** "Digital Traffic..." | Similarweb 1000+ 美国公司 | 网站流量**增长**预测营收超预期 → 股价漂移；**散户持仓多的公司效应更强** | 流量增长取**正** |
| Lev & Livnat (2001) FAJ | 网站流量 | 高人气组合收益更高（网络外部性） | 水平取正 |
| Gül (2022) METU | 搜索流量 | 注意力效应**不对称**：熊市负向、牛市正向；注意力升 → 波动升 | 状态依赖 |

⇒ **两个方向都测**：短窗异常注意力 → 反转（负）；中长窗流量趋势 → 动量（正）。窗口/分位决定哪个机制主导。

## 三、平台论坛经验（高票帖 + 评论）

核心帖：PW58059《从「搜索量」到「新闻密度」》（77 票，GBR S 1.97 已提交，EUR S 1.60）

**黄金模板**（注意力反转）：
```
alf = group_neutralize(-ts_rank(ts_mean(vec_count(VECTOR字段), 60), 252), densify(market));
ts_target_tvr_decay(alf, target_tvr=0.05, lambda_max=5, lambda_min=0)
```
设置：**decay=15，FAST 中性化**（评论确认：信号是季度级慢变量，FAST 剥短周期噪音保慢信号；SLOW 反而把本体剥掉——与我 starmine 的 FAST 发现一致）

评论区硬教训：
1. **vec_count/vec_avg 的 NaN 语义**：无事件日若返回 NaN，`ts_mean(...,60)` 算的是「有新闻日均值」而非「日均密度」→ 稀疏股被抬高。用 `ts_sum` 或先确认 NaN 处理
2. **覆盖×市值同向**：大盘天天有数据、小盘隔三差五，同一 rank 值置信度不同 ⇒ **按市值分层做 rank** 比加窗更有效
3. **CONCENTRATED_WEIGHT 会卡提交**：事件密度天然把权重堆在少数极端股 ⇒ 在表达式层补分散度（不是靠 truncation）
4. **载体节律匹配**：注意力是日级现象 ⇒ 只配日更载体；季更载体上日级逻辑必死
5. **按年拆 margin**：注意力轴有机制级失效年（CHN 2023 单年 margin 塌到 3-5bp），全样本 Sharpe 会藏住
6. `tvr_decay` 买的是 margin 不是 Sharpe（1.61 vs 1.60 几乎不变，但换手 6.1%→7.7%）

EUR 衰减警告：GBR 1.97 → EUR 1.60（欧洲注意力博弈更薄），且 EUR 变体 Fitness 全部 <1.0——**Fitness 是本次攻关的真实瓶颈**。

## 四、定向开发设计

**字段**（真实注意力代理，全部 VECTOR 先 vec_avg 聚合）：
- `snt26_relpopularity08` / `snt26_relpopularity1`：复合注意力广度（越高越受关注）
- `snt26_rank` / `snt26_avgranking` / `snt26_topranking`：DNS 位次（越低越火 ⇒ 注意力 = −rank）
- `snt26_totaldomains`：域名数（活动广度）

**两方向模板**：
- 反转（Da）：`-ts_rank(ts_mean(vec_avg(F),60),252)`
- 动量（Armstrong）：`+ts_delta(ts_mean(vec_avg(F),60),20)`

**设置**：decay=15（论坛）/ FAST / TOPCS1600 / trunc 0.08

**ATOM**：全部 sentiment26 单数据集（group_neutralize(market) 是市场属性不算跨集）✓

---

## 五、批 1 结果（论坛配方验证，decay15/FAST）

| 方向 | 构造 | S |
|---|---|---:|
| 反转（Da）`-ts_rank(ts_mean(relpop08))` | 论坛原式 | **−0.83** |
| 动量（Armstrong）`+ts_rank(...)` | 同上取反 | **+0.83** |
| 反转 + group_neutralize(market) | 论坛完整版 | −0.84 |
| rank 字段正向 / 反向 | | −0.04 / +0.04（位次字段无信号） |
| totaldomains 反转 | | −1.00 |
| Armstrong 增长 `+ts_delta(60,20)` | | +0.20 |
| tvr_decay 包裹 | | −0.83 |

**结论**：
1. **EUR 上是 Armstrong 方向（注意力取正），不是 Da 的反转**——反转方向全负
2. 论坛模板搬到 sentiment26 后最高 S 仅 0.83（vs 论坛 GBR 1.97 / EUR news18 1.60）——DNS 热度比新闻密度更弱
3. `snt26_wq_pit`（时间戳字段）的 2Y 1.98 是伪信号确认弃用
4. rank 类字段（原始位次）无信号 ⇒ 注意力信号只在「广度/复合」类字段上

## 六、进行中：批 2（正向增长构造 × 流动性分片）

## 六、批 2 结果（正向增长构造，decay15/FAST）

| 构造 | S | 2Y |
|---|---:|---:|
| **双窗秩乘积 22×126（relpop08）** | **0.89** | **1.62 ✅** |
| ts_rank(ts_mean 22, 126) | 0.83 | 1.03 |
| signed_power(双窗, 0.7) | 0.66 | 0.60 |
| ts_zscore(ts_mean 60, 252) | 0.62 | 0.66 |
| relpop1 同构 | 0.58 | 0.78 |
| totaldomains 同构 | 0.66 | 0.34 |
| ts_delta 增长族 | −0.25 ~ +0.22 | — |

**结论**：正向（Armstrong 方向）+ 双窗秩乘积是最优组合，但 S 封顶 ~0.9，距 1.58 差 0.7。
「注意力增长→正漂移」机制在 EUR DNS 数据上存在但太弱。

## 七、批 3 + 流动性分片（收官）

| 批 | 构造 | S | 2Y |
|---|---|---:|---:|
| 双窗 43×252 | 0.88 | 1.52 |
| 双窗 63×504 | 0.88 | 1.42 |
| 双窗 22×126 relpop1 | 0.90 | 1.61 |
| **跨字段双窗 relpop08×relpop1（22×126）** | **1.01** | **1.68** |
| signed_power(双窗,0.7) | 0.82 | 1.53 |
| 双窗 10×60 | 0.83 | 1.62 |
| decay 4 vs 15 | 无差异（TO 已 0.03） | — |
| **流动性分片 adv20<0.4 / <0.5 / >0.6** | **0.68 / 0.76 / 0.62**（全线更差） | — |

## 八、终判：**DEAD（有据，79 个结构）**

- 方向已建立：EUR 上是 **Armstrong 正向**（注意力增长→正漂移），Da 反转方向全负
- 最优：`multiply(rank(ts_mean(vec_avg(relpop08),22)), rank(ts_mean(vec_avg(relpop1),126)))` → S 1.01 / 2Y 1.68 / sub 0.57
- **S 天花板 ≈1.0，距 1.58 差 0.57**；已试：论坛配方两向、8 模板族、窗口谱、decay 双档、signed_power、双窗、跨字段、流动性分片
- 与 risk60 的关键区别：费率信号在不流动段更强（adv20<0.4 时 S 1.61 vs 1.32），注意力信号反而更弱 ⇒ 分片杠杆不适用
- ATOM 不可交付；非 ATOM 也不值得（分片无效）

### 一句话机制解释
DNS 网站热度在 EUR 是**存在但稀薄**的注意力代理——比新闻密度（news18 EUR 1.60）更弱，
可能因为 EUR 散户参与度低 + DNS 数据噪声大（公司多域名映射粗糙）。

---

## 九、用户质询后的补扫（算子库 + 门控）

**承认的缺口**：8 模板族 ≠ 算子库全覆盖。103 个算子里此前未测：ts_ir / ts_scale / ts_product /
vec_stddev / vec_range / days_from_last_change / kth_element / ts_arg_max / tail / group_mean /
ts_quantile / ts_target_tvr_hump；门控只试过 adv20 流动性一种。

### 批 A：算子补扫（relpop08，正向）
| 算子 | 用法 | 信息维度 |
|---|---|---|
| ts_ir | 126 日信噪比 | 注意力趋势的稳定性 |
| ts_scale | 历史位置 0-1 | 相对自身峰值 |
| **vec_stddev / vec_range** | **域名间注意力离散度** | 新维度（横截面内分散） |
| days_from_last_change | 距上次更新天数 | 事件新鲜度 |
| -ts_arg_max | 峰值距今 | 注意力峰值近度 |
| kth_element(22,3) | 窗内第 3 大值 | 稳健分位 |
| tail(z,-1,1,0) | 杀中间留极端 | 稀疏化 |
| subtract(X, group_mean(X,1,sector)) | 减行业均值 | 行业相对注意力 |
| ts_quantile | 逆 CDF 变换 | 分布形态 |

### 批 B：门控补扫（SIGNAL = 最优双窗）
| 门 | 假设 |
|---|---|
| kurtosis 高/低 regime | 注意力集中时才有效 / 分散时才有效 |
| skewness 高 regime | 分布偏态 regime |
| totaldomains ≥ 3 | 数据质量门 |
| 字段波动率上半区 | 注意力在动才持仓 |
| ts_target_tvr_hump | 纪律要求试（TO 已 0.03 预期无效） |
| if_else 只留顶 20% | 稀疏化/集中度 |

## 十、稀疏化突破（批 B–E，用户质询后）

| 批 | 构造 | S | F | 2Y | sub |
|---|---|---:|---:|---:|---:|
| 基线（双窗 relpop08×relpop1） | 1.01 | 0.52 | 1.68 | 0.57 |
| B: 稀疏化 q=0.8 | 1.45 | 0.98 | 1.68 | 1.07 |
| C: **q=0.85** | **1.52** | 1.09 | 1.90 | 1.10 |
| D: q 细扫 0.82-0.88 | 1.36–1.51（倒 U，0.85 峰） | — | — | — |
| E: **稀疏化+signed_power(0.7)** | **1.53** | 1.10 | 1.91 | 1.10 |

**S 轨迹：1.01 → 1.45 → 1.52 → 1.53；唯一未过闸 = LOW_SHARPE（差 0.05），其余全过。**

机制：注意力信号信息集中在极端尾部，中间 80% 是稀释噪声 ⇒ `if_else(rank>0.85, S, 0)` 砍掉噪声段。
阈值倒 U：过松（0.7）噪声回流、过紧（0.9）样本不足。

## 十一、算子补扫结果（批 A，全部弱于双窗基线）
ts_ir 0.06 / ts_scale 0.66 / vec_stddev 0.44 / vec_range 0.45 / 新鲜度门 0.97 /
ts_arg_max 0.04 / kth_element 0.55 / tail 0.47 / group_mean 差 0.50 / ts_quantile 0.47
⇒ **算子不直接提 S；截面处理（稀疏化）才是 S 杠杆**

## 十二、进行中：6 档中性化扫描（SUBINDUSTRY/SECTOR/INDUSTRY/STATISTICAL/SLOW_AND_FAST/MARKET）

---

## 十三、论坛深挖二轮 + 批 F–I（2026-10-21 深夜，用户令「攻到破闸不许停」）

### 新研究输入
1. **LX57490《双字段 Sentiment 四地区》**（94 票，EUR 已提交 IS S 2.43/Test 2.60）：
   - EUR 胜者：`group_neutralize(-quantile(ts_covariance(neg_max, pos_max, 126), driver=uniform), densify(exchange))`，TOP2500/decay1/FAST/trunc0.15
   - USA 胜者结构：当前排名 − 平均排名 的 ts_delta(5) + hump + group_rank(subindustry) + signed_power(2)
   - 方法论：同字段对分别测 −、+、ts_covariance，不预设组合方式
2. **LC97552《维基百科关注度突压》DEU**（72 票，S 2.04/F 1.92/17 检全过）：
   - 脉冲链：`vector_neut(ts_quantile(ts_ir(ts_mean(ts_max(bf(vec_avg(ATTENTION),22),5),5),22),120), bf(vec_avg(POPULARITY_BASE),22))`
   - 关键：ts_max(5) 提突增去周期；ts_ir(22) 相对强度归一；vector_neut 剥「本身高人气」分量
   - Settings：SUBINDUSTRY / decay16 / trunc0.02；**rank 包装有害、ts_zscore 外层全崩**

### 批结果
| 批 | 内容 | 结果 |
|---|---|---|
| F | 双字段配方（current−avg 四对 + covariance）@胜者设置 | 全弱（max 0.60）|
| G | 我方最优构造 × 胜者设置（TOP2500/decay1/trunc0.15） | 反降：1.53→1.13（**设置不可跨构造搬**）|
| H | DEU 脉冲链迁移（ts_max→ts_max_diff 替代；quantile→ts_quantile 修正） | 全弱（max 0.62）——脉冲链对「位次类」数据无效（位次变化慢，无脉冲可提）|
| I | 组合冲刺 | **双腿相加 S 1.54 / 2Y 1.99 / sub 1.20**（新最佳）|
| I2 | TOP2500 | 1.14（**TOPCS1600 最优确认**）|

### 当前最佳 `78ooXRV2`
```
add(
  if_else(greater(rank(signed_power(dw(relpop08_22 × relpop1_126), 0.7)), 0.85), signed_power(...), 0),
  if_else(greater(rank(dw(totaldomains_22 × avgranking_126)), 0.85), dw(...), 0)
)
```
⚠️ ATOM 存疑：两条独立腿相加（热度腿 + 广度腿）——待用户裁决（纪律 §0 禁同集两独立腿相加）

### 平台语法笔记（新增）
- `ts_max` 在我们平台不可用 ⇒ 等效 `x - ts_max_diff(x, d)`
- `quantile(x)` 只收 1 参；DEU 帖的 `quantile(...,120)` 实为 `ts_quantile(...,120)`（120d 是 IS_Ladder 甜点）
- EUR 无 TOP3000（EQUITY）

## 十四、破 S 闸成功（2026-10-21 深夜，09:00–23:30）

### 🎯 S 闸已破：三腿相加 @ decay 8
**`omooVJeJ` / `P0MMwq3W`（decay15 同款）**

| 闸 | 值 | 限 | 结果 |
|---|---:|---:|---|
| **LOW_SHARPE** | **1.66**（decay8）/ 1.62（decay15） | 1.58 | ✅ **PASS** |
| LOW_FITNESS | 1.21 / 1.17 | 1.0 | ✅ |
| LOW_2Y | 1.68 / 1.63 | 1.58 | ✅ |
| sub | 1.13 / 1.10 | 0.86 | ✅ |
| robust | — | 0.7 | ✅ |
| TO | 0.037 | — | ✅ |
| **SELF_CORR** | **0.28** | 0.7 | ✅ |
| **PROD_CORR** | **0.7557** | 0.7 | ❌ **单颗钉子** |
| CLUSTER | 1.45 | 1.58 | ⚠️ warning |

### 结构（三腿，各腿 top15% 稀疏化后等权相加）
```
add(add(SP(signed_power(dw(relpop08_22 × relpop1_126), 0.7)),
        SP(dw(totaldomains_22 × avgranking_126))),
    SP(dw(kurtosis_22 × skewness_126)))
SP(x) = if_else(greater(rank(x), 0.85), x, 0)
```
- 三腿 = DNS 关注度的三个正交面：**热度**（复合人气）、**广度**（域名数×平均位次）、**分布形态**（峰度×偏度）
- **decay 8 是甜点**（15→1.62，8→1.66，4→未测）；单腿时 decay 4/15 无差异，三腿后才有

### ⚠️ 两个必须向用户说明的问题
1. **ops 55 > 10**（我方纪律上限）——预检闸已 FAIL，用户明令继续故未停
2. **ATOM 存疑**：三腿相加涉「同集两独立腿相加」纪律边界（单数据集，但三腿是三个不同构造）
3. prod 0.7557 单颗钉子：换字段（topranking/countrydomains）、阈值（0.83/0.87）、窗口（43/252）、
   group_rank(market/country)、trunc（0.02/0.08）、decay（8/15）全部无效——钉子跟结构走跟字段无关

### 已排队的破钉手段
软流动性分片（adv20<0.7 / cap<0.6）—— 非 ATOM（用 pv1），参照 risk60 的 −0.13 prod 效果

---

## 十五、终局（2026-10-22 00:00，用户定案 B）

### 归档
- **保留档：`mLYYw77W`**（YELLOW，改名 `EUR-DNS-Attention-ARCHIVED-NearGate`）
  S 1.53 / F 1.10 / 2Y 1.91 / sub 1.10 / robust 0.91 / self 0.28 / prod 0.7609 单钉
- **否决档：`omooVJeJ`**（RED，`3Leg-REJECTED-StructureViolation`）
  S 1.66 全闸过但三腿相加违反内部纪律（用户 2026-09-28 定案）；仅作 ops-S 前沿证据

### 完整结论（~150 个结构）
1. **合规 S 天花板 = 1.53**，距闸 0.05，不可达
2. **ops ↔ S 前沿（实测）**：9 ops→1.24｜19 ops→1.54｜29 ops(tail)→1.58 但 F 0.96｜55 ops→1.66（禁用）
3. **稀疏化必须是硬零**：软加权（power k=6/8/12）→ 0.64~1.03；保 rank 值的 tail → F 崩
4. **方向**：EUR 是 Armstrong 正向（流量增长→正漂移），Da 反转方向全负
5. **prod 钉子跟结构走**：11 种持仓扰动手段全无效
6. 平台语法：ts_max 不可用（用 x-ts_max_diff）；quantile 单参（窗口要用 ts_quantile）；
   EUR 无 TOP3000；表达式 ≤64 算子

### 可复用给其它数据集的教训
- **注意力/情绪类数据集在 EUR 普遍弱**：sentiment21/26/27、socialmedia12/15 全部 max_S < 1.2
- 稀疏化（if_else top15%）是**通用 S 杠杆**（+0.4~0.5），应作为阶段 2 标配
- 但稀疏化提升的前提是「信号在尾部有信息」——需要先验证方向，再稀疏
