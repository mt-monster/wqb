# other571（Wikipedia Company Page Views）字段画像 · 字段八问

> 命名：`_usa-<字段前缀>-field-profile-<asOf>.md`｜前缀 **oth571**
> 组织：按「字段八问」（1 是什么 / 2 什么类型 / 3 覆盖多少 / 4 怎么更新 / 5 分布如何 / 6 拥挤吗 / 7 出不出信号 / 8 怎么用·怎么判死）
> **as_of**：2026-10-21 ｜ 裁定：**判死（`USA-OTH571-DOUBLE-KILL`）** —— 双闸同时不过：
> ① **S 天花板 1.51**（30+ 条变体，唯一未过闸 = `LOW_SHARPE 1.51 vs 1.58`，平滑曲线在 decay10 见顶后回落）；
> ② **prod = 0.9087**（`ZYmAVRo8` 平台直测 405s，`[0.6,0.7)` 22740 条 / `[0.7,0.8)` 10619 条 ⇒ 单邻居重叠型，非族级饱和）。
> 结论：**注意力机制在 USA/D1 已被完全定价**，与 `web_traffic_engage`(0.974–0.991) / `stock_search_trends`(0.824–0.938)
> / analyst 目标价族(0.90–0.999) 同型 —— 这是连续第四个「IS 近闸 / prod 必死」的注意力类数据集。
>
> 数据集事实：USA/D1/TOP3000 ｜ 平台 **30 字段**（`sharpe_filter` 后可见 28，2 个被平台按历史 sharpe 隐藏）
> ｜ 全 **MATRIX** ｜ cov 0.538–0.597 ｜ 平台 α 总量 **约 335**（`recommend_datasets` 口径，未点亮塔）

---

## 总览

**零售关注度（retail attention）代理**：美国公司维基百科页面的浏览量。28 个可见字段是
「时间窗 × 时段 × 设备」的笛卡尔切片，**没有情绪、没有文本、没有方向**——只有「多少人在看」。

机制来源（文献）：
- **Da, Engelberg & Gao (2011), "In Search of Attention"**：零售关注度冲击 → 短期价格上行后**反转**；
- **Barber & Odean (2008)**：散户是注意力驱动的净买入者（attention-driven buying）；
- **Wikipedia 特有**：用户主动检索（不同于被动新闻推送），且覆盖全美股 60%，是**低拥挤的散户注意力纯代理**。

本数据集的字段按「窗口」分三层：**短窗（today / 7d）→ 中期（14/28/84d）→ 长窗（1y）**；
每个窗口另有 **时段**（morning 06–11 / afternoon 12–17 / evening 18–23 / night 00–05）与
**设备**（desktop / mobile）分解。**时段的最后一个字段是「N 天前那一天的切面」，不是滚动窗**——
这是本集最容易误读的一点（见 §⑤）。

## ② 什么类型 / ③ 覆盖多少 / ④ 怎么更新

| 族 | 字段数 | 类型 | cov | 更新 | 说明 |
|---|---:|---|---:|---|---|
| 日频总量 `viewstoday` | 1 | MATRIX | 0.5941 | 日频 | 当日（module 时区）总浏览 |
| 7 日滚动 `views7d` | 1 | MATRIX | 0.5973 | 日频 | 过去 7 自然日；**本集主字段（u31/a42）** |
| 14 / 28 / 84 日窗 | 3 | MATRIX | 0.593 / 0.593 / 0.584 | 日频 | 窗口末端分别落在 14 / 28 / 84 天前 |
| 1 年窗 `views1y` | 1 | MATRIX | 0.5377 | 日频（末端 = 364 天前） | 长期基线 |
| 7d 时段分解 | 4 | MATRIX | 0.5973 | 日频 | **单日切面**：`views7dmorning/afternoon/evening/night` = 7 天前那一天的 4 个时段 |
| 7d 设备分解 | 2 | MATRIX | 0.5973 | 日频 | `views7ddesktop` / `views7dmobile` = 过去 7 天按设备 |
| today 时段 / 设备 | 4 + 2 | MATRIX | 0.5941 | 日频 | `viewstoday{afternoon,evening,morning,night,desktop,mobile}` |
| 14d / 28d / 1y 切片 | 12 | MATRIX | 0.538–0.593 | 日频 | 同上，末端日期分别 14 / 28 / 364 天前 |

**字段数守恒**：1 + 1 + 3 + 1 + 4 + 2 + 6 + 12 = **30**（平台总数）。可见 28 = 30 − 2（`sharpe_filter` 隐藏）。

**④ 更新语义**（关键）：
- 所有窗口都是**滚动窗**，末端带滞后（14d 窗末端 = 14 天前；1y 窗末端 = 364 天前），
  ⇒ **不存在前视**，但短窗字段（today / 7d）的"新鲜度"只到 T−1，延迟 1 的 USA 无额外代价。
- 时段 / 设备切片是**快照式单日切面**（不是滚动窗），与同名前缀的滚动窗**不可直接相减**。

## ⑤ 分布如何

- **计数型、右偏重尾**：单只股票的日浏览量跨 0 到 10^6 量级 ⇒ 裸用 rank 会被尾部支配。
  处理：`log(1 + x)` 或先 `ts_rank` / `ts_zscore` 做时序归一。
- **零值 / 缺失**：cov 0.59 ⇒ 41% 的股票-日 NaN（小盘、次新股、更名）。`nanHandling=ON` 下
  NaN 被中性化，但**缺失不是随机**（大盘覆盖更好）⇒ 与 f21 ESG 同类风险：
  **信号可能退化成"覆盖度赌注"**，必须核 `longCount/shortCount` 是否失衡。
- **量纲**：`views7dmobile / views7d` 是比率，无量纲；`log(1+views)` 是无量纲的强度分。
- **同质性风险**：28 字段高度共线（都是同一个浏览量的变换）⇒ **不是 28 个独立信号**，
  做多字段组合时必须先按相关性筛族，否则等于同信号加权（禁混信号纪律同样适用）。

## ⑥ 拥挤吗

| 指标 | 读数 | 解读 |
|---|---:|---|
| 平台 α 总量 | ~335 | 冷门（对比 analyst_factor_signals 数万、fundamental6 86 万） |
| 主字段 `oth571_views7d` | u31 / aC42 | 最拥挤的一档，仍有空间 |
| `oth571_viewstoday` | u58 / aC76 | 日频关注度被用最多 |
| `views7dmobile` | u18 / aC19 | 较冷 |
| `views1y*` / 各时段切片 | u2–u8 / aC2–aC9 | 极冷 |
| 塔状态 | `category=other`，**未点亮** | 按 USA 纪律可挖 |

**判读**：aC 42–76 的字段**不是"没人碰过"**，但比 Fundamental（f6 86 万）低 4 个数量级；
且这批 α 大概率集中在 `viewstoday` 的裸 rank 上，**加速 / 分歧 / 条件结构仍是空白**。

---

## ⑦ 出不出信号（首批 10 条，2026-10-21）

**设计纪律**：≥ 3 桶（Change / Surprise / Event-conditioned / Level）、≥ 1 HIGH 桶、
每方向都成对出反号变体（注意力→反转是文献方向，但 USA 大盘可能已被定价）。

| # | 桶 | α | 表达式 | S | F | 2Y | SUB | TO | ret | riskNeu S |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Change | QPYKp7ew | `-group_rank(ts_zscore(log(1+oth571_views7d), 66), subindustry)` | −1.36 | −0.73 | −1.78 | −0.87 | 20.95% | −5.97% | −1.45 |
| 2 | Change（反号） | GrgO5lEx | `group_rank(ts_zscore(log(1+oth571_views7d), 66), subindustry)` | **1.36** | **0.73** | **1.78** | 0.87 | 20.95% | 5.97% | 1.45 |
| 3 | Surprise | WjLe27wG | `-group_rank(ts_av_diff(log(1+oth571_viewstoday), 22), subindustry)` | −1.37 | −0.69 | −2.15 | −0.91 | 22.89% | −5.78% | −1.29 |
| 4 | Surprise（反号） | zqrbnkwV | `group_rank(ts_av_diff(log(1+oth571_viewstoday), 22), subindustry)` | **1.37** | 0.69 | **2.15** | **0.91** | 22.89% | 5.78% | 1.29 |
| 5 | Surprise | Vkd0b7q0 | `-group_rank(ts_zscore(log(1+oth571_views7d)-log(1+oth571_views84d), 66), subindustry)` | −1.23 | −0.63 | −1.52 | −0.57 | 19.96% | −5.22% | −1.36 |
| 6 | Surprise（反号） | mLY6WjA2 | `group_rank(ts_zscore(log(1+oth571_views7d)-log(1+oth571_views84d), 66), subindustry)` | 1.23 | 0.63 | 1.52 | 0.57 | 19.96% | 5.22% | 1.36 |
| 7 | Dispersion（设备分歧） | P0Mgm76x | `-group_rank(ts_zscore(oth571_views7dmobile/(oth571_views7d+1), 66), subindustry)` | −1.19 | −0.56 | −1.56 | −0.54 | 24.39% | −5.35% | −1.12 |
| 8 | Level（长期关注度） | mLY6Wjz2 | `group_rank(ts_rank(log(1+oth571_views1y), 252), subindustry)` | 1.07 | 0.57 | 1.44 | 0.58 | 17.33% | 4.84% | 0.85 |
| 9 | Event-conditioned（时段） | 3qjVvl6O | `-group_rank(ts_zscore(oth571_views7devening/(oth571_views7d+1), 66), subindustry)` | −1.04 | −0.43 | −1.35 | −0.52 | 26.12% | −4.51% | −0.75 |
| 10 | Event-conditioned（HIGH） | E5VRPlrR | `group_rank(trade_when(ts_zscore(log(1+oth571_viewstoday),22) > 1.5, -ts_rank(log(1+oth571_views7d),66), -1), subindustry)` | 0.96 | 0.49 | 1.30 | 0.40 | 5.98% | 3.29% | 0.52 |

multisimulation id：`3hshvE13Z4gQbOr1cJ8rlFUL`（USA/D1/TOP3000，SUBINDUSTRY，decay 5，truncation 0.08）
｜ 平台区间 2014-01-01 → 2023-12-31 ｜ 塔：`USA/D1/OTHER` multiplier 1.4

**读数**（2026-10-21 实测）：

1. **注意力在 USA 是动量，不是反转** —— §⑧ 规则 1 命中。三组配对（7d z-score / today vs 22 日均 / 7d−84d）
   **全部对称**：负号族 S −1.04…−1.37 与正号族 S +0.96…+1.37 镜像，且正号统一胜出。
   设备分歧腿（#7）与 evening 时段腿（#9）也是**负号为正收益**的形态 ⇒ 这两个"分歧"信号实为
   **正号腿的反向表达**，应改写成 `+group_rank(views7dmobile/(views7d+1))` 族再测。
2. **两闸之差是量级问题，不是方向问题**：#4 `zqrbnkwV` S 1.37（差 0.21）/ F 0.69（差 0.31）、
   2Y **2.15**（超线 0.57）、SUB **0.91**（线 0.59）、riskNeu 1.29（远高于 0.3 的风格 beta 线）。
   ⇒ 唯二的短板是 S 与 F，而 F 是 S 的**乘法函数**（见下）。
3. **F = S × sqrt(ret / max(TO, 0.125)) 已在两条腿上验算**（#4: 1.37×√(0.0578/0.2289)=0.688；
   #2: 1.36×√(0.0597/0.2095)=0.726，平台读数 0.69 / 0.73）。两条推论：
   - **TO < 0.125 的平滑对 F 零收益**（分母封顶），"降换手"本身不救 F；
   - 要到 F 1.0 @ S 1.58 需 **ret/TO ≥ 0.40**，而 #4 当前 0.2525 ⇒ 需 +59% 的收益-换手比。
   ⇒ 杠杆是**保收益的平滑**（`ts_mean` / `ts_decay_linear` 叠在已证方向），不是单纯压换手。
4. **覆盖度赌注风险未兑现**：longCount/shortCount = 1293/1724（#4）、1268/1748（#2），
   两侧同量级 ⇒ `nanHandling=ON` 下 41% NaN 没把信号压成单边持仓。
5. **条件结构（#10）的边际翻倍但宽度不足**：TO 从 22.9% → **5.98%**，margin 从 5.05bp → **11.01bp**
   （2.18×），但 S 掉到 0.96、SUB 掉到 0.40（未过线）——阈值 1.5σ 太紧、持仓日太少。
   若继续这条线：降阈值到 1.0σ 或改软门控（`ts_rank(...) * weight`），而不是加仓。

**第 2 波（同向修正，不换概念）**：multisim `dsFNse6H4Bkbvj118eMiwhQ`，10 条 = ts_rank 归一（66/252）、
`ts_mean` 平滑（5/10 天）、7d / 28d 长窗 z-score（252 / 126）、比值形式（today / 22d 均值）、
`group_neutralize` 壳、`ts_decay_linear(10)`、双窗 ts_rank 差。**全部取正号**。

| α | 结构 | S | F | 2Y | SUB | TO | ret |
|---|---|---|---:|---:|---:|---:|---:|---:|
| ZYmAVRo8 | `ts_decay_linear(ts_zscore(log(1+today),66),10)` | **1.51** | **1.05** | 1.92 | 0.88 | 10.56% | 6.08% |
| A1QvXRkg | `ts_mean(ts_zscore(log(1+today),66),10)` | 1.49 | **1.03** | 1.94 | 0.90 | 8.77% | 5.96% |
| 3qjVmME0 | `ts_rank(log(1+today),252)` | 1.49 | 0.89 | 1.89 | 0.90 | 18.69% | 6.71% |
| 78o6PkxQ | `ts_rank(log(1+today),66)` | 1.44 | 0.77 | 2.06 | 0.90 | 21.52% | 6.22% |
| XgRJZj1m | `ts_mean(ts_zscore(log(1+today),66),5)` | 1.43 | 0.95 | 1.89 | 0.82 | 13.08% | 5.75% |
| omoWj1VE | `ts_zscore(log(1+views7d),252)` | 1.36 | 0.81 | 1.60 | 0.81 | 17.84% | 6.28% |
| XgRJZjKl | `ts_zscore(today/mean22(today),66)` | 1.28 | 0.62 | 2.05 | 0.77 | 22.69% | 5.27% |
| KPmrAKLl | `ts_zscore(log(1+views28d),126)` | 1.21 | 0.64 | 1.05 | 0.67 | 19.43% | 5.41% |
| vRO27KmA | `group_neutralize(zscore(today,66), subind)` | 1.16 | 0.33 | 2.55 | 0.76 | **47.40%** | 3.82% |
| leMKwLV2 | `ts_rank(today,22) - ts_rank(today,66)` | 0.81 | 0.36 | 1.15 | 0.21 | 14.84% | 2.92% |

**第 2 波结论（F 公式的实证兑现）**：

1. **平滑是唯一有效杠杆，且有甜区**：`ts_mean` 5d → 10d 把 F 从 0.95 推到 **1.03**、TO 从 13.1% 压到 8.8%，
   而收益几乎不掉（5.75% → 5.96%）——正是 F 公式里 `max(TO,0.125)` 封顶的"免费区间"。
   `ts_decay_linear(10)` 更强：S **1.51** / F **1.05** / TO 10.56% / ret 6.08%。
   ⇒ 两条都只剩 **LOW_SHARPE** 一闸（1.49–1.51 vs 1.58），差距 0.07–0.09。
2. **`group_neutralize` 壳不可用**：TO 飙到 47.4%、`CONCENTRATED_WEIGHT` 警告、F 0.33 —— `group_rank`
   的截面对称性是必需的，不要为了"更干净的中性化"换掉它。
3. **"加速度"（双窗 ts_rank 差）最差**（S 0.81）：注意力变化率的二阶量噪声过大，别再试。
4. **窗口单调性**：短窗（today）> 7d > 28d > 1y；而**同一字段的归一窗口**以 66 天最佳
   （44 / 126 / 252 都不如 66，见第 3 波）。⇒ 信号源固定 = `viewstoday`，唯一旋钮 = 平滑长度。

**第 3 波**：multisim `AOV1l4Fj53r8MyZYy7HggZ` —— 在已验证结构上只调平滑（15 / 22 天）、
组合平滑（decay10→mean5）、today−7d 残差、zscore 窗口 44 / 126、`group_zscore` 壳、`sector` 分组。

| α | 结构 | S | F | 2Y | SUB | TO | ret | DD |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| O0J8dwZv | `group_rank(ts_decay_linear(z66,10), sector)` | 1.48 | **1.07** | 1.88 | 0.87 | 10.24% | 6.50% | 10.44% |
| 1YjZ3VoW | `group_rank(ts_decay_linear(z66,15), subind)` | **1.50** | 1.05 | 1.90 | 0.87 | 8.63% | 6.07% | 8.65% |
| 3qjVmY7Q | `group_rank(ts_decay_linear(z126,10), subind)` | 1.48 | 1.04 | 1.69 | 0.86 | 9.45% | 6.21% | **7.30%** |
| pwv5bJ8g | `group_rank(ts_decay_linear(z66,22), subind)` | 1.47 | 1.01 | 1.74 | 0.85 | 7.18% | 5.92% | 7.97% |
| YPxM3wAW | `group_rank(ts_mean(ts_decay_linear(z66,10),5))` | 1.47 | 1.01 | 1.81 | 0.84 | 8.76% | 5.86% | 8.83% |
| LL5Zobk9 | `group_rank(ts_mean(z66,15), subind)` | 1.45 | 0.99 | 1.78 | 0.83 | 7.03% | 5.78% | 8.52% |
| XgRJZwp1 | `group_rank(ts_decay_linear(z44,10), subind)` | 1.45 | 0.98 | 1.93 | 0.82 | 11.33% | 5.69% | 10.83% |
| RRA6xZdo | `group_rank(ts_mean(z66,22), subind)` | 1.40 | 0.94 | 1.58 | 0.71 | 5.76% | 5.59% | 7.66% |
| akVxm2Ox | `group_rank(ts_decay_linear(zscore(today−7d),10))` | 1.28 | 0.66 | 1.70 | 0.65 | 18.19% | 4.84% | 11.81% |
| omoWjwKJ | `group_zscore(ts_decay_linear(z66,10), subind)` | 1.25 | 0.54 | 1.96 | 0.68 | 19.85% | 3.64% | 3.47% |

**第 3 波结论（S 的天花板已探到）**：

1. **平滑曲线已到顶并回落**：decay 10 → 15 → 22 对应 S 1.51 / 1.50 / 1.47（TO 10.6% / 8.6% / 7.2%）。
   `ts_mean` 同形更差。⇒ **S ≈ 1.51 是本结构上限**，再压换手只会伤信号；差闸 0.07 不是平滑能补的。
2. **`group_rank(..., subindustry)` 是负贡献**：去掉它的 ZYmAVRo8（1.51）> 任何带 group_rank 的变体（≤1.50），
   但 F 反而 `sector` 分组最高（1.07）——分组壳买的是截面稳健性，不是 Sharpe。
3. **残差化（today − views7d）被证伪**：S 1.28、TO 18.2%、F 0.66。7d 里含 today，相减放大噪声。
4. **`group_zscore` 壳被证伪**：TO 19.9%、`CONCENTRATED_WEIGHT` 触发、F 0.54。z-score 不截尾 ⇒ 集中持仓（与 wave2 `group_neutralize` 同型故障）。
5. **zscore 归一窗口 66 最优**（44 → 1.45、126 → 1.48）；**126 的收益/回撤比最好**（DD 7.30%、S 1.48）——若后续要拼组合腿，它是低回撤首选。

**第 4 波（2026-10-21，结构杠杆而非平滑）**：两条并行 —— `3pd009bvE4yrabTxQDBtOG4`（SUBINDUSTRY 6 条）
+ `3BNg1J4ES4Oh90617Mr4eTv`（**MARKET 中性化** 4 条）。动因：riskNeu S（1.66–1.72）> raw S（1.50）
⇒ 风格暴露在拖累，中性化档位是本族最后一个未测杠杆。

| α | 结构 | S | F | 2Y | SUB | TO | riskNeu |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 88vPW0lo | `backfill(...,66)` → z66 → decay10 | 0.69 | 0.27 | 1.66 | 0.52 | 18.7% | 0.59 |
| wp9b7djl | `backfill(...,252)` → z66 → decay10 | 0.67 | 0.26 | 1.67 | 0.48 | 18.7% | 0.58 |
| E5VRnjlL | `ts_rank(backfill(...,66),252)` → decay10 | 1.28 | 0.77 | 1.63 | 0.74 | 13.6% | 1.44 |
| WjLerZPk | `hump(decay10, 0.01)` | **−0.27** | −0.07 | −0.98 | −0.22 | 2.4% | 0.03 |
| wp9b7dYl | zscore(**22**) → decay10 | 0.94 | 0.31 | **2.60** | 0.60 | 25.7% | 0.86 |
| E5VRnjvL | zscore(**252**) → decay10 | 1.22 | 0.69 | 1.65 | 0.63 | 16.1% | 1.29 |
| N1eVE22L | MARKET 壳 · base | 0.96 | 0.48 | 1.34 | 0.67 | 19.3% | 1.26 |
| omoWjxP2 | MARKET 壳 · backfill66 | 0.75 | 0.36 | 1.22 | 0.69 | 18.0% | 0.75 |
| kqJgpz86 | MARKET 壳 · rank(backfill) | 0.83 | 0.52 | 1.15 | 0.57 | 12.9% | 1.35 |
| d5K1JNYg | MARKET 壳 + `group_rank(subind)` | 1.29 | 1.01 | 1.49 | 0.92 | 9.4% | 1.68 |

**第 4 波结论（5 条新证伪，双杀裁定不变）**：

1. **`ts_backfill` 对本字段是污染不是补全**：S 1.51 → **0.69**（66）/**0.67**（252），两个窗口同向崩塌。
   原因：本字段是**变化量**，NaN 的语义是"该股不被任何 ETF 持有"（结构性缺值），
   backfill 把陈旧变化铺进"不被持有"的区间 ⇒ 造出持续存在的假信号。
   **⇒ 对事件/变化量字段，覆盖不足先看 NaN 语义，禁止无脑 backfill。**
2. **`hump(0.01)` 直接摧毁信号**（S −0.27、TO 2.4%）：信号半衰期短于 hump 门槛，
   持仓被冻结在错误方向上。**⇒ hump 只适用于慢变量；快衰减信号用 decay，不用 hump。**
3. **换中性化不解决 0.07 的缺口**：MARKET 壳 S 0.96（比 SUBINDUSTRY 的 1.51 低 0.55）；
   即使叠加 `group_rank(subind)` 也只回到 1.29。**riskNeu > raw 说明风格暴露确实是拖累，
   但换壳**（MARKET）**买不回截面内的 alpha** —— alpha 来源是"行业内相对"，不是"全市场相对"。
4. **短窗口买 2Y、输全期**：zscore 22 的 2Y **2.60**（全波最高）但 S 0.94、CW 触发；
   252 窗口 S 1.22。**66 仍是唯一兼顾全期与近期的窗口**（1.51 / 1.92）。
5. **`ts_rank` 是唯一抗 backfill 的归一**：rank(backfill66, 252) 把被 backfill 砸到 0.69 的信号
   拉回 **1.28**（F 0.77）——但仍在 1.58 线下，且低于无 backfill 的 1.51。**救不回来。**

⇒ 与 ① 的 prod 0.9087 合并成 **双杀**：IS 天花板 1.51 差 0.07，prod 超线 0.21，两条路都无剩余杠杆。

## ⑧ 怎么用·怎么判死

**机制判据（先归因再推进）**：
1. 若**正号**族胜出 ⇒ 注意力是**持续买入压力**（散户净买入），走 Change/Level 的慢变量；
   **→ 2026-10-21 实测命中此条**：方向固定为正号，后续只在"归一 / 平滑 / 窗口"三个旋钮上推进。
2. 若**负号**族胜出 ⇒ 文献方向成立，下一步做 **Event-conditioned**（只在关注度冲击日建仓，
   降换手、提 SUB）；本次未发生，但 #10 的 margin 翻倍提示条件结构本身有效，别丢弃。
3. 若两方向都 ≤ 1.0 ⇒ 注意力在 USA **已被定价**，把本集降为「辅助门控腿」（不单独出 α）；本次未触发。

**已确认的用法**：
- 主字段簇 = `viewstoday`（Surprise：today vs 22 日均）+ `views7d`（Change：66 日 z-score）；
  两者都能独立到 S≈1.36–1.37，**同源度高，最多出 1–2 颗**，不要当成两个独立信号凑数。
- 设备/时段切片只作**比率腿**（`mobile / total`、`evening / total`），且方向取正号；
  单独用会掉到 S≈1.0–1.2。
- 长窗 `views1y` 的 `ts_rank` 是**慢变量基线**（S 1.07 / TO 17.3% / margin 5.6bp），
  适合做别的腿的**分母 / 中性化基准**，不适合单独提交。

**判死口径**：数据集级 `dead_end` 需 8 统计族全试 + 全波最强 |S| 低于判死线
（[rules/signal-mining-workflow.md](../rules/signal-mining-workflow.md) §八）；本页首批 10 条只作探针级，
**未判死**（最强 S 1.37，超过 1.25 的字段级观察线）。
