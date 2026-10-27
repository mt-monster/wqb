# other580 · Standardized Daily ETF Holdings —— 字段画像与首批设计

> **as_of**：2026-10-21 ｜ 区域：USA / D1 / TOP3000 ｜ 类型：MATRIX × 403（无 VECTOR）
> 金字塔：**USA/D1/OTHER ×1.4（未点亮）** ｜ 平台 α=189 / 用户=105 / `os_is_sharpe`=0.5347
> 里程碑：`S0` 已过（未判死 / 无跨区弱 / 塔未亮）→ 本文件 = `S1` 字段画像 → 首批探针待回测

## §0 为什么从这个数据集接棒（换集理由留痕）

`other571`（Viewership Attention）已在同日 **双杀封存**：IS 天花板 S=1.51（差 1.58 线 0.07）+ prod=0.9087
（平台直测 405 s）。选 `other580` 的四条依据：

1. **机制正交**：注意力 / 文本类是"预期与关注"，本集是 **ETF 申赎对成分股的机械需求**
   （creation/redemption → 被动资金必须买卖），收益来源不依赖任何文本或搜索数据。
2. **注意力族已连续四次 prod 致死**：`web_traffic_engage` 0.974–0.991 / `stock_search_trends` 0.824–0.938 /
   analyst 目标价族 0.90–0.999 / `other571` 0.9087 —— 同族第五次下注没有信息增益。
3. **论坛实证**：ETF 资金流选股「天然具有低相关性优势」（XH93773, 2026-07-06）；持仓类数据集的
   标准变换是 **流量 ÷ 存量**，「事件周期 66（季度）」（HM97321, 2026-09-03）。
4. **拥挤度极低**：α=189 / 用户=105，是候选池里除 fnd 系之外最低的一档；且 `other` 塔未点亮（×1.4）。

## §1 数据集卡片（S0 结论）

| 项 | 值 |
|---|---|
| dataset id | `other580` |
| 名称 | Standardized Daily ETF Holdings |
| category / region / delay | `other` / USA / 1 |
| 字段 | **403 × MATRIX**（无 VECTOR ⇒ 不需 `vec_*` 聚合） |
| 覆盖率 | 派生量字段 **0.83–0.92**；`count_*` 恒为 **1.0**；`oth580_*` 0.900–0.915 |
| 平台用量 | α=189，users=105（低拥挤） |
| 平台表现 | `os_is_sharpe`=0.5347（**历史用户提交的信号普遍偏弱 ⇒ 空间在"怎么用"，不在"有没有"**） |
| 塔位 | USA/D1/OTHER，multiplier=1.4，**未点亮** |
| 判死三查 | 未判死 / 无跨区弱记录 / 非 lit 塔 ⇒ **通过，可挖** |

## §2 字段全景：403 个字段只有 5 个语义族

所有字段是**同一底层面板（每股 × 每 ETF 的持股数快照）在不同加权 / 窗口 / 符号上的聚合**。
先认底层量，再认包装：

| 族 | 字段模式（按命名可穷举） | 底层量 | 窗口 | 覆盖率 | 代表字段 |
|---|---|---|---|---|---|
| **A. 绝对变化幅度**（无符号） | `change_{average, log_weighted_average, sqrt_weighted_average, count, log_weighted_count, simple_sum, weighted_sum, squared_sum, cubed_sum, skewness, variance}` + `_2` / `_5d` / `_60d` 后缀 | 跨 ETF 的 **\|Δ持股数\|** 聚合 | 5 / 20 / 60 d | 0.89–0.92（count=1.0） | `change_average`（u1/a1）、`oth580_mv_mean`（**u19/a45，全库最常用**） |
| **B. 百分比变化**（**有符号，流量÷存量**） | `percent_change_{average, mean, log_weighted_average, log_weighted_mean, sqrt_weighted_average, count, log_weighted_count, ... , variance, skewness, squared_sum}` + 窗口后缀 | 每股在各 ETF 中的 **%Δ持股**（已按持仓归一） | 5 / 20 / 60 d | 0.88–0.92（count=1.0） | `percent_change_average`（u2/a2）、`percent_change_average_5d`、`percent_change_log_weighted_mean_20d`（**注意：无无后缀的 `percent_change_log_weighted_average`，20d 版名带 `_mean_20d`**） |
| **C. 60 日持有变化** | `holding_change_{log_weighted_average, log_weighted_skewness, skewness, variance, squared_sum, sqrt_weighted_*}` | 60 日绝对变化的分布统计 | 60 d | 0.87–0.90 | `holding_change_variance`、`positive_holding_change_mean` |
| **D. 正 / 负分解**（**构造成交方向的关键**） | `positive_*` / `negative_*` × {change, percent_change, holding_change} × {average, count, sum, variance, skewness, sqrt/log-weighted} | 把 A/B/C 按**变化方向**拆分 | 5 / 20 / 60 d | count=1.0，其余 0.86–0.91 | `positive_percent_change_count`、`negative_percent_change_count`、`positive_change_average` |
| **E. 预测族** | `*_predicted` / `*_prediction` / `predicted_*`（**18 个**，实测） | 模型对持有变化的**预测值** | 5 / 20 / 60 d | 0.90–0.92 | `percent_change_average_predicted`、`holding_change_mean_predicted` |
| **F. 遗留聚合**（`oth580_*`，7 个） | `mv_mean` / `mv_sisum` / `mv_cusum` / `mv_sqsum` / `mv_skew` / `rav_vm` / `tnc_vm` | 持仓**市值**及其分布；`tnc_vm`=ETF 内换手（**cov=1.0**） | 日频 / 累计 | 0.900–0.915 | `oth580_tnc_vm`（u17/a25）、`oth580_mv_sisum`（u20/a20） |

**全字段逐条清单**（id / 覆盖率 / 用户数 / α 数 / 描述）见 §7 附录。

### 2.1 三条结构性事实（决定怎么用）

1. **8–13% 的 NaN 是结构性缺值，不是数据缺失**：这些股票**不被任何 ETF 持有**（或被持有但无变化）。
   证据：`count_*` 覆盖率恒为 1.0 —— 计数在"没有 ETF 持有"时返回 0，而派生均值返回 NaN。
   **⇒ 禁止 `ts_backfill`**：`other571` 同日实测 backfill 把 S 1.51 砸到 0.69（把陈旧变化铺进不被持有区间，
   造出假信号）。本集缺值语义更强（结构性），backfill 风险同型。
2. **A 族无符号，B 族有符号**：A 是 `|Δshares|`（描述里明写 absolute），只能度量"动了多少"，
   不能给方向；B 是 `%Δshares`（流量÷存量）才带方向。**要做多空方向，主字段必须是 B 族或 D 族的差**。
3. **D 族是按符号条件筛选后的聚合**：`positive_change_average` 只对加仓的 ETF 求均值，
   `negative_change_average` 只对减仓的 ETF 求均值。**两者相减 = 有符号的幅度不平衡**；
   两者**计数相减 = 宽度不平衡**（多少家加仓 vs 多少家减仓）。这是本数据集最干净的两个合成方向。

### 2.2 更新频率与分布特征（口径与待实测项）

- **更新频率**：数据集名含 *Daily*，且字段自带 5d/20d/60d 三种窗口 ⇒ 底层持仓快照为**日频**。
  `count_*` 为整数计数；`*_variance/skewness` 为二阶/三阶矩；`percent_change_*` 为比率（无量纲）。
  日更性质以首批回测的 `investability_sharpe` 与换手率反证（若实为周更，decay5 下 TO 会显著偏低）。
- **分布特征**：平台字段元数据不含分布（无 mean/std/min/max）。**待首批实测补**：
  ① 用正负号臂的 S 符号判断方向；② 用 `longCount/shortCount` 看分层是否单边（`nanHandling=ON` 下
  NaN 不参与）；③ 用 `margin` 与 `CONCENTRATED_WEIGHT` 判断尾部厚度；④ 用 `risk_neutralized_sharpe`
  与 raw S 的差判断是否只是风格 beta。
- **可用性**：全部 403 字段覆盖率 ≥ 0.83，**无 < 0.4 的字段**（不需要 backfill 或弃用）；
  但 `count_*` 覆盖 1.0 是因为"0 也返回"，其信息量与均值类不同 —— 不能把 count 当 level 用。

## §3 字段八问（本数据集版）

1. **这个字段在量什么？** ETF 全体对某只成分股的**持股数**及其变化，按 ETF 等权 / 对数加权 / 平方根加权聚合。
   加权口径决定谁主导：等权=每家 ETF 一票；log/sqrt=持仓大的 ETF 权重更大但被压缩。
2. **谁在制造这个数？** 两个来源叠加：① 被动 ETF 的**申赎**（creation/redemption，机械、无信息）；
   ② ETF 内部的**主动调仓/再平衡**（有信息，尤其 smart-beta 与主动 ETF）。二者不可分，是本集固有噪声。
3. **它的单位/量纲？** A 族=股数（受价格与拆股影响）；B 族=比率（可跨股比较，**优先**）；
   E 族=预测的同类量；F 族=美元市值 / 换手率。
4. **正负号意味着什么？** B 族正=净加仓（需求压力↑），负=净减仓；D 族把两个方向分开后再合成。
5. **为什么会有 alpha？** ① **需求压力**：被动资金流入 → 短期价格压力 → 延续或反转；
   ② **信息假说**：主动 ETF 加仓 = 知情交易；③ **拥挤/流动性**：ETF 高持股 → 波动与流动性溢价。
6. **什么时候失效？** 当资金流完全由指数规则驱动（大票、宽基成分）且已被套利；当流是单只 ETF 的
   一次性再平衡（D 族 dispersion 高、count 低）。
7. **和别的数据集会不会重？** 与本仓已挖的注意力 / 分析师 / 机构持股（institutions18）不同源：
   本集是**ETF 通道**，institutions18 是**13F 主动机构**。论坛实证 ETF 资金流选股低相关。
8. **怎么证伪？** 若 ① 有符号族两方向都 ≤1.0；② 换成 `risk_neutralized_sharpe` 后崩塌（纯风格）；
   ③ 首批 8 条最佳 S < 1.2 ⇒ 判死（决策表 D15 快判死：新集 8 探针无 |S|≥0.5 即死；
   本集目标是 1.58，比 D15 更严）。

## §4 首批探针（S1 census，10 条，按机制分桶）

**目的 = 字段普查**（哪个语义族带信号），不是调参。统一结构
`group_rank(ts_zscore(F, 66), subindustry)`，设置 SUBINDUSTRY/decay5/trunc0.08 —— 与 USA 控制面板一致。

> **已发批（2026-10-21）**：multisim `2uEczbf8O5bM9RL4vwFTJTZ`（10 条，SUBINDUSTRY / decay5 /
> trunc 0.08 / nanHandling ON / TOP3000 / D1）。发批前 `validate_expressions` 逮到一处字段名错误：
> **不存在无后缀的 `percent_change_log_weighted_average`**（20d 版实名 `percent_change_log_weighted_mean_20d`），
> 原 #4 已按实名替换 —— 若不校验，整批会被一个 unknown variable 连坐 CANCELLED。

| # | F | 族 | 机制假设 | 预期方向 |
|---|---|---|---|---|
| 1 | `percent_change_average` | B | 净申赎 → 20d 需求压力 | ±（待定） |
| 2 | `percent_change_average_5d` | B | 同上，5d 更快 | ± |
| 3 | `positive_percent_change_count - negative_percent_change_count` | D | **宽度不平衡**：多少家加仓 vs 减仓（最抗单 ETF 噪声） | + |
| 4 | `percent_change_log_weighted_mean_20d` | B | 大持仓 ETF 主导的净流（知情假说） | ± |
| 5 | `positive_change_average - negative_change_average` | D | 幅度不平衡（加仓幅度 vs 减仓幅度） | + |
| 6 | `oth580_mv_mean` | A/F | 1 日绝对变化强度（平台最常用字段的对照） | ± |
| 7 | `oth580_tnc_vm` | F | ETF 内换手水平（cov=1.0；高换手=噪声/低换手=粘性） | ± |
| 8 | `oth580_mv_sisum` | F | ETF 持仓市值水平（=ETF 持股强度，可能只是 size beta） | ± |
| 9 | `percent_change_variance` | B | 跨 ETF 分歧：高分散=单家再平衡 → 反转 | − |
| 10 | `percent_change_average - percent_change_average_predicted` | E | **意外流**：实际 − 预测 | + |

**判读规则（先归因再推进）**：
- 若有符号族（1/2/4）与宽度族（3）同向且 |S| 最高 ⇒ 机制 = **需求压力/信息**，第 2 波在 B 族做窗口与平滑。
- 若只有宽度族（3）存活 ⇒ 机制 = **广度**（多家共识），第 2 波做 count 比率与门槛。
- 若只有 dispersion（9）存活 ⇒ 机制 = **过度反应反转**，第 2 波做 event-conditioned。
- 若只有 F 族（8/7）存活且 riskNeu 崩塌 ⇒ **纯风格 beta，判死**（不留恋）。
- 若 8 条最佳 S < 1.2 ⇒ 按 D15 判死换集。

### 4.1 首批实测结果（2026-10-21，10/10 COMPLETE）

| # | α | 字段 | 族 | S | F | 2Y | SUB | TO | DD | rns |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | `MP03ro6r` | `percent_change_variance` | B·分歧 | **0.88** | 0.36 | 1.14 | 0.03 | 19.1% | **4.86%** | 0.24 |
| 6 | `j2e87bYk` | `oth580_mv_mean` | F | **0.82** | 0.21 | 0.49 | 0.57 | 52.9% | 11.2% | **0.76** |
| 8 | `9qEWnLlV` | `oth580_mv_sisum` | F | 0.82 | 0.21 | 0.53 | 0.56 | 53.4% | 10.3% | 0.74 |
| 4 | `RRA6gnE0` | `percent_change_log_weighted_mean_20d` | B | 0.71 | 0.26 | 0.92 | 0.76 | 19.6% | 6.5% | 0.01 |
| 1 | `leMKmbKl` | `percent_change_average` | B | 0.67 | 0.23 | 1.06 | 0.69 | 20.0% | 8.5% | −0.15 |
| 10 | `E5VRdXmK` | `pc_average − pc_average_predicted` | E | 0.67 | 0.22 | 1.03 | 0.67 | 21.9% | 8.2% | −0.13 |
| 2 | `omoWdMo5` | `percent_change_average_5d` | B | 0.54 | 0.13 | 0.35 | 0.43 | 34.8% | 9.5% | 0.39 |
| 5 | `P0MgVdo7` | `pos_change_avg − neg_change_avg` | D | 0.51 | 0.15 | 0.21 | −0.03 | 23.0% | 9.7% | −0.01 |
| 3 | `pwv5LAv3` | `pos_pc_count − neg_pc_count` | D | 0.33 | 0.07 | 0.27 | 0.41 | 26.6% | 13.9% | 0.03 |
| 7 | `RRA6gne0` | `oth580_tnc_vm` | F | −0.25 | −0.06 | −0.90 | −0.26 | 16.2% | 21.1% | −0.45 |

**普查结论（机制层，全部 10 条 S ≤ 0.88，无一过闸）**：

1. **B 族（有符号净流）不弱但不强**：0.67–0.71，`log_weighted_mean_20d`（大持仓 ETF 主导）优于等权，
   说明**知情成分在，但幅度不够**；5d 版（0.54）明显差于 20d ⇒ 不是短周期反转，是 20 日需求的慢衰减。
2. **D 族两个合成方向都失败**：幅度不平衡 0.51（SUB **−0.03**）、宽度不平衡 0.33（DD 13.9%）
   ⇒ "多少家 / 多大力度"都不带可交易信息，**宽度假说证伪**。
3. **预料之外流（E）零增益**：0.67 与原始 0.67 逐位相同 ⇒ 预测项不含额外信息（`percent_change_average_predicted`
   ≈ 原字段的平滑复制）。
4. **F 族是本集最强且 rns 最高**：`mv_mean` / `mv_sisum` 都是 0.82 且 **rns 0.74–0.76**（S 的 90% 来自
   非风格残差，罕见）；两者逐位近似 ⇒ **同一底层量（ETF 持仓市值/活动度）的两种包装，只占一个坑**。
   代价是 TO 53%、F 只有 0.21。
5. **分歧族（`percent_change_variance`）是唯一"低回撤"信号**：DD 4.86% / 2Y 1.14，但 **SUB 0.03**（线 0.38）
   ⇒ 信号集中在大市值，TOP3000→TOP1000 不成立；且 F 0.36 < 1。
6. **`oth580_tnc_vm` 是高换手 → 负收益**（−0.25），反号也只有 0.25，无价值。

**归因（为什么整体只有 0.5–0.9）——一个尚未测的结构缺口**：本批统一用 `ts_zscore(F, 66)`，
即**把"水平"压成"相对自身 66 日的偏离"**。但 ETF 申赎的经济含义是**持续的需求压力（水平量）**：
长期被净申购的股票，其 `percent_change_average` 本就该一直偏高 —— z-score 恰好把这类
"持续流入"抹成 0。**⇒ 第 2 波只测一件事：水平 vs 变化**（不是调参，是补测本批漏掉的归一形式）。

### 4.2 第 2 波：水平 vs 变化（归因批，8 条）

multisim `1lWseP2vw4oB8UCyAJMF6q4`，设置同上。设计矩阵（同一字段只换**归一形式**，
不引入新字段，避免变成盲扫）：

| 组 | 表达式 | 要回答的问题 |
|---|---|---|
| B 水平 | `group_rank(percent_change_average, subindustry)` | 20 日净流**水平**是否比 z-score 偏离更强 |
| B 持续水平 | `group_rank(ts_mean(percent_change_average, 22), subindustry)` | 持续流入（22 日平滑）是否才是"需求压力" |
| B 长窗变化 | `group_rank(ts_zscore(percent_change_average, 252), subindustry)` | 66 窗是否把水平信息截断（252 = 一年基期） |
| B log 水平 | `group_rank(percent_change_log_weighted_mean_20d, subindustry)` | 上批最好的 B 变体在水平形式下是否更好 |
| F 水平 | `group_rank(oth580_mv_mean, subindustry)` | 1 日活动度**水平**（不 z-score）是否直接就是信号 |
| F 22 日水平 | `group_rank(ts_mean(oth580_mv_mean, 22), subindustry)` | 平滑活动度：降 TO（53%→?）换 F，S 让多少 |
| F 长窗变化 | `group_rank(ts_zscore(oth580_mv_mean, 252), subindustry)` | 长基期是否救回被 66 窗压掉的持续性 |
| 分歧水平 | `group_rank(percent_change_variance, subindustry)` | SUB 0.03 是"变化形式"造成还是水平本身的集中度 |

**判据（预注册，先写后跑）**：任一条 S ≥ 1.2 且 SUB 过线 ⇒ 水平假说成立，第 3 波在该形式内做
窗口 / 分组壳 / 衰减；**全部 < 1.2 ⇒ 按 D15 判死 `USA-OTHER580-WEAK`**（机制弱，不是壳问题），
并把「水平 vs 变化」这条通用结论写进 playbook。

### 4.3 第 2 波实测：水平假说被证伪（8/8 COMPLETE）

| 组 | α | 表达式 | S | F | 2Y | SUB | TO | rns |
|---|---|---|---:|---:|---:|---:|---:|---:|
| B 水平 | `O0J83601` | `group_rank(percent_change_average)` | 0.63 | 0.22 | 0.85 | 0.55 | 19.3% | −0.11 |
| B 持续水平 | `e76Qj17d` | `…ts_mean(percent_change_average,22)` | **0.30** | 0.09 | **−0.06** | 0.24 | 7.6% | −0.45 |
| B 长窗变化 | `xA1bZlAJ` | `…ts_zscore(percent_change_average,252)` | 0.58 | 0.20 | 0.89 | 0.56 | 19.4% | −0.25 |
| B log 水平 | `zqrbVAKG` | `group_rank(percent_change_log_weighted_mean_20d)` | 0.70 | 0.27 | 0.73 | 0.68 | 18.9% | −0.03 |
| F 水平 | `npAPE6pd` | `group_rank(oth580_mv_mean)` | 0.76 | 0.19 | 0.22 | 0.54 | 58.1% | 0.52 |
| F 长窗变化 | `88vPwG5q` | `…ts_zscore(oth580_mv_mean,252)` | **0.86** | 0.23 | 0.58 | 0.52 | 53.4% | **0.78** |
| F 22 日水平 | `wp9brNKY` | `…ts_mean(oth580_mv_mean,22)` | **0.19** | 0.04 | **−0.42** | 0.19 | 15.6% | −0.38 |
| 分歧水平 | `zqrbVAqG` | `group_rank(percent_change_variance)` | 0.81 | 0.35 | 1.11 | 0.18 | 16.8% | 0.15 |

**归因结论（4 条，全部来自同批对照）**：

1. **"水平 > 变化"的假设被四族逐一证伪**：水平形式在每一族都**不如** z-score 形式
   （B 0.63 < 0.67、B-log 0.70 < 0.71、F 0.76 < 0.82、分歧 0.81 < 0.88）
   ⇒ **ETF 申赎在这里是"冲击"不是"累积压力"**，与「66 日事件周期」的论坛口径不矛盾：
   事件窗口是回看窗口，不是持仓期。
2. **平滑直接杀信号**：B 的 22 日均值 0.30（2Y **−0.06**）、F 的 22 日均值 0.19（2Y −0.42）
   ⇒ 该信号的生命期是 **1–20 日**，任何 >20 日的平滑都把信息抹平。**这解释了为什么 F 族 TO 53%
   却仍是全族最强 —— 换手是信号本身，不是噪声。**
3. **长窗口只对 F 有效**：z252 把 F 从 0.82 → **0.86**（rns 0.78，最高），但把 B 从 0.67 → 0.58
   ⇒ B 的记忆长度是 66 日、F 是 252 日，**两族不该共用同一个归一窗口**。
4. **分歧族的 SUB 缺口不是形式问题**：水平 0.18 / 变化 0.03，**两种形式都不过线**（线 0.35/0.38）
   ⇒ 该信号结构性集中在大市值，TOP3000→TOP1000 不成立，**判死该字段**（不是判死数据集）。

**数据集裁定：`USA-OTHER580-WEAK`（D15 判死，2026-10-21）**
两波 18 条、六族全覆盖、水平 / 变化 / 平滑 / 长窗四种归一形式都测过，
**同时覆盖 S、F、2Y 三线的最好结果是 S 0.88**（分歧族，SUB 0.03）与 S 0.86（F 族，2Y 0.58），
距 1.58 线 **1.8×**。平台 `os_is_sharpe`=0.5347 与本轮普查中位数（0.67）吻合 ⇒ **不是我们没找对壳，
是这个数据集的可交易信号本身只有 0.5–0.9 的量级**。逐字段证据见 §4.1–§4.3，不再扩波。

## §5 风险与已知陷阱

1. **不要把 A 族当方向用**：`change_average` 是绝对变化，做多"动得多的股票"没有方向含义。
2. **不要 backfill**（见 2.1）；NaN 是"不被 ETF 持有"的语义，补全会造假信号。
3. **count 字段 cov=1.0 不等于信息更全**：它把"没有 ETF 持有"记为 0，0 与"真的有 0 家变化"不可分。
4. **D 族的差要在同一窗口内配对**：`positive_change_average`（默认 20d？）与 `_5d` / `_60d` 不可混减；
   首批只用无后缀版本（同窗口），第 2 波再做窗口配对。
5. **F 族是市值/换手**，与 size、liquidity 强相关，必须看 `risk_neutralized_sharpe` 再决定去留。

## §6 论坛与文献沉淀（可复用）

- **流量 ÷ 存量**：持仓类数据集的标准变换是"流量除以存量"（shares/holdings、valueeur/holdings、
  tradesignificance/holdings），事件周期取 **66（季度）**（论坛 HM97321, 2026-09-03）。本集的 B 族
  天然就是流量÷存量，故首批直接用 B 族，窗口选 66（z-score 归一）。
- **ETF 资金流选股低相关**：跨品种数据集（ETF 资金流）在拥挤板块里天然低相关（论坛 XH93773, 2026-07-06）。
  ⇒ 本集即便 S 只到 1.6–1.7，prod 通过的概率也高于注意力族。
- **指数纳入效应**：被动资金机械买入 → 短期价格上行（论坛 MG88592, 2026-09-25）。本集的 ETF 申赎
  是同一机制的高频版本。
- **持仓类信号的有效中性化**：论坛给 insd1 类（机构持股）的实证是 `ts_rank` + COUNTRY / STATISTICAL
  中性化 S 2.4+（论坛 CG48008）；本集首批先用 USA 面板的 SUBINDUSTRY，若 S 不足则在第 2 波试
  STATISTICAL 壳（注意：USA 面板中性化档位以 `wqb.profiles explain` 为准，不得手改控制文件）。

## §7 附录：403 字段逐条清单

共 **403** 个字段（全部 MATRIX）。按语义族分组，族内按 `alphaCount` 降序。

汇总：用户数合计 **185** ／ α 数合计 **247** ／ 覆盖率区间 **0.8659 – 1.0000**。

### F 族 · 遗留聚合 `oth580_*`（7 个）

| id | cov | users | alphas | description |
|---|---:|---:|---:|---|
| `oth580_mv_mean` | 0.9153 | 19 | 45 | Equal-weight mean across ETFs of the 1-day absolute change (delta) in ETF shares held of the stock |
| `oth580_tnc_vm` | 1.0000 | 17 | 25 | The stock's value-weighted mean turnover within the ETF. |
| `oth580_mv_sisum` | 0.9153 | 20 | 20 | Total market value of the stock's position within the ETF. |
| `oth580_mv_cusum` | 0.9153 | 14 | 17 | Cumulative sum of the stock's cubed market value within the ETF. |
| `oth580_rav_vm` | 0.9029 | 10 | 10 | The stock's value-weighted mean risk-adjusted value within the ETF. |
| `oth580_mv_skew` | 0.9005 | 7 | 8 | Skewness of the stock's market value distribution within the ETF. |
| `oth580_mv_sqsum` | 0.9153 | 5 | 5 | Sum of the squared market value of the stock's position within the ETF. |

### E 族 · 预测族（18 个）

| id | cov | users | alphas | description |
|---|---:|---:|---:|---|
| `change_average_predicted` | 0.9154 | 3 | 3 | Predicted average change in holdings. |
| `average_predicted_holding_change_20d` | 0.9122 | 3 | 3 | Predicted mean change in fund holdings over a 20-day period. |
| `percent_change_log_weighted_mean_prediction` | 0.9102 | 1 | 1 | Predicted mean of percent changes weighted by logarithm. |
| `holding_change_mean_predicted` | 0.9023 | 1 | 1 | Predicted mean of changes in holdings. |
| `percent_change_average_predicted` | 0.9154 | 0 | 0 | Predicted average of percent changes in holdings. |
| `change_log_weighted_average_predicted` | 0.9131 | 0 | 0 | Predicted average change, weighted by logarithm. |
| `change_sqrt_weighted_average_predicted` | 0.9131 | 0 | 0 | Predicted average change, weighted by square root. |
| `percent_change_log_weighted_average_predicted` | 0.9131 | 0 | 0 | Predicted average of percent changes, weighted by logarithm. |
| `predicted_percent_change_sqrt_weighted_mean_5d` | 0.9131 | 0 | 0 | Predicted mean of percentage changes weighted by square root of shares over 5 days. |
| `percent_change_mean_prediction` | 0.9122 | 0 | 0 | Predicted mean of percent changes in holdings. |
| `percent_change_sqrt_weighted_mean_prediction` | 0.9102 | 0 | 0 | Predicted mean of percent changes weighted by square root. |
| `predicted_log_weighted_mean_change_20d` | 0.9102 | 0 | 0 | Predicted mean change in holdings weighted by logarithm of shares over 20 days. |
| `predicted_sqrt_weighted_mean_change_20d` | 0.9102 | 0 | 0 | Predicted mean change in holdings weighted by square root of shares over 20 days. |
| `percent_change_mean_predicted` | 0.9023 | 0 | 0 | Predicted mean of percent changes in holdings. |
| `holding_change_log_weighted_mean_predicted` | 0.9005 | 0 | 0 | Predicted mean of changes in holdings, weighted by logarithm of shares. |
| `holding_change_sqrt_weighted_mean_predicted` | 0.9005 | 0 | 0 | Predicted mean of changes in holdings, weighted by square root of shares. |
| `percent_change_log_weighted_mean_predicted` | 0.9005 | 0 | 0 | Predicted mean of percent changes in holdings, weighted by logarithm of shares. |
| `percent_change_sqrt_weighted_average_predicted_60d` | 0.9005 | 0 | 0 | Predicted average percent change over 60 days, weighted by square root. |

### D 族 · 正 / 负分解（252 个）

| id | cov | users | alphas | description |
|---|---:|---:|---:|---|
| `negative_change_count` | 1.0000 | 6 | 7 | Count of ETFs holding the stock that show a negative 20-day absolute change in shares |
| `positive_change_count` | 1.0000 | 4 | 6 | Number of ETFs holding the stock with a positive 20-day absolute change in shares held |
| `negative_percent_change_count` | 1.0000 | 3 | 4 | Number of ETFs holding the stock with a negative 20-day percent change in shares held |
| `positive_percent_change_count` | 1.0000 | 3 | 4 | Number of ETFs holding the stock with a positive 20-day percent change in shares held |
| `positive_percent_change_sqrt_weighted_squared_sum` | 0.9043 | 2 | 4 | Sum of squared positive percent changes weighted by square root. |
| `positive_change_weighted_sum` | 0.9043 | 2 | 3 | Sum of positive changes weighted by shares or value. |
| `negative_change_log_weighted_count` | 1.0000 | 2 | 2 | Count of negative changes weighted by logarithm. |
| `negative_change_log_weighted_count_2` | 1.0000 | 1 | 2 | Weighted count (sum of log‑position weights) of ETFs with negative 5‑day absolute changes in shares held for the stock |
| `positive_change_count_2` | 1.0000 | 2 | 2 | Number of ETFs with positive 5‑day absolute changes in shares held for the stock (equal‑weight count) |
| `positive_change_count_60d` | 1.0000 | 1 | 2 | Count of positive changes in holdings over 60 days. |
| `positive_change_log_weighted_count` | 1.0000 | 2 | 2 | Count of positive changes weighted by logarithm. |
| `positive_change_variance_60d` | 0.8755 | 2 | 2 | Variance (equal-weight across ETFs) of positive 60-day absolute changes in ETF shares held |
| `negative_change_count_5d` | 1.0000 | 1 | 1 | Number of ETFs with negative 5-trading-day absolute changes in shares held (equal-weight count) |
| `negative_percent_change_count_60d` | 1.0000 | 1 | 1 | Count of negative percent changes in holdings over 60 days. |
| `negative_sqrt_weighted_change_count_20d` | 1.0000 | 1 | 1 | Count of negative changes in holdings weighted by square root of shares over 20 days. |
| `positive_log_weighted_change_count_5d` | 1.0000 | 1 | 1 | Count of positive changes in holdings weighted by logarithm of shares over 5 days. |
| `positive_percent_change_sqrt_weighted_count` | 1.0000 | 1 | 1 | Sum of sqrt weights (sqrt of ETF position size) for ETFs with positive 20-day percent changes in shares held |
| `positive_change_simple_sum` | 0.9096 | 1 | 1 | Sum of positive changes in holdings. |
| `positive_change_sqrt_weighted_cubed_sum_2` | 0.9096 | 1 | 1 | Sum of cubed positive changes, weighted by square root. |
| `positive_change_sqrt_weighted_simple_sum` | 0.9096 | 1 | 1 | Sum of positive changes, weighted by square root. |
| `positive_percent_change_average` | 0.9096 | 1 | 1 | Equal‑weight mean of positive 5‑day percent changes in ETF shares held across ETFs |
| `negative_change_cubed_sum_5d` | 0.9089 | 1 | 1 | Sum of cubed negative changes in holdings over a 5-day period. |
| `positive_change_average` | 0.9043 | 1 | 1 | Equal-weight mean of positive 20-day absolute changes in ETF shares across ETFs holding the stock |
| `positive_change_log_weighted_sum` | 0.9043 | 1 | 1 | Sum of positive changes weighted by logarithm of shares or value. |
| `negative_change_sqrt_weighted_squared_sum` | 0.9029 | 1 | 1 | Sum of squared negative changes weighted by square root. |
| `negative_percent_change_average_20d` | 0.9029 | 1 | 1 | Mean of negative percentage changes in holdings over a 20-day period. |
| `negative_percent_change_sqrt_weighted_squared_sum_20d` | 0.9029 | 1 | 1 | Sum of squared negative percentage changes weighted by square root of shares over 20 days. |
| `positive_holding_change_cubed_sum` | 0.8909 | 1 | 1 | Sum of cubes of positive changes in holdings. |
| `positive_change_skewness` | 0.8896 | 1 | 1 | Skewness of positive changes in holdings. |
| `positive_change_log_weighted_variance` | 0.8894 | 1 | 1 | Log-of-position-size weighted variance of positive 20-day absolute changes in ETF shares held in the stock |
| `negative_holding_change_sqrt_weighted_cubed_sum` | 0.8876 | 1 | 1 | Sum of cubes of negative changes in holdings, weighted by square root of shares. |
| `negative_holding_change_sqrt_weighted_squared_sum` | 0.8876 | 1 | 1 | Sum of squares of negative changes in holdings, weighted by square root of shares. |
| `negative_change_log_weighted_variance` | 0.8873 | 1 | 1 | Log-of-position-size weighted variance of negative 20-day absolute changes in ETF shares held in the stock |
| `positive_percent_change_log_weighted_skewness_20d` | 0.8869 | 1 | 1 | Skewness of positive percentage changes weighted by logarithm of shares over 20 days. |
| `positive_percent_change_log_weighted_skewness_2` | 0.8723 | 1 | 1 | Log-weighted skewness across ETFs of positive 60-day percent changes in ETF shares held |
| `negative_change_sqrt_weighted_variance_60d` | 0.8700 | 1 | 1 | Variance of negative changes over 60 days, weighted by square root. |
| `negative_change_count_60d` | 1.0000 | 0 | 0 | Count of negative changes in holdings over 60 days. |
| `negative_change_sqrt_weighted_count_60d` | 1.0000 | 0 | 0 | Sum of sqrt-share weights (not a literal count) for ETFs with negative 60-day absolute changes in shares held for the stock |
| `negative_holding_change_log_weighted_count` | 1.0000 | 0 | 0 | Count of negative changes in holdings, weighted by logarithm of shares. |
| `negative_percent_change_count_5d` | 1.0000 | 0 | 0 | Number of ETFs with negative 5-trading-day percent changes in shares held (equal-weight count) |
| `negative_percent_change_log_weighted_count` | 1.0000 | 0 | 0 | Count of negative percent changes in holdings, weighted by logarithm of shares. |
| `negative_percent_change_log_weighted_count_20d` | 1.0000 | 0 | 0 | Sum of log weights (log of ETF position size) for ETFs with negative 20-day percent changes in shares held |
| `negative_percent_change_log_weighted_count_5d` | 1.0000 | 0 | 0 | Weighted count (sum of log‑position weights) of ETFs with negative 5‑day percent changes in shares held for the stock |
| `negative_percent_change_sqrt_weighted_count` | 1.0000 | 0 | 0 | Sqrt-of-position-size weighted count (sum of sqrt weights) of ETFs with negative 20-day percent changes in shares held in the stock |
| `negative_percent_change_sqrt_weighted_count_2` | 1.0000 | 0 | 0 | Sum of sqrt‑weights (square root of ETF position size) for ETFs with negative 5‑day percent changes in shares held |
| `negative_percent_change_sqrt_weighted_count_60d` | 1.0000 | 0 | 0 | Count of negative percent changes over 60 days, weighted by square root. |
| `negative_sqrt_weighted_change_count_5d` | 1.0000 | 0 | 0 | Sum of sqrt‑weights (square root of ETF position size) for ETFs with negative 5‑day absolute changes in shares held |
| `positive_change_log_weighted_count_60d` | 1.0000 | 0 | 0 | Count of positive changes over 60 days, weighted by logarithm. |
| `positive_change_sqrt_weighted_count` | 1.0000 | 0 | 0 | Sqrt-of-position-size weighted count (sum of sqrt weights) of ETFs with positive 20-day absolute changes in shares held in the stock |
| `positive_holding_change_sqrt_weighted_count` | 1.0000 | 0 | 0 | Count of positive changes in holdings, weighted by square root of shares. |
| `positive_percent_change_count_2` | 1.0000 | 0 | 0 | Number of ETFs with positive 60-day percent change in shares held |
| `positive_percent_change_count_5d` | 1.0000 | 0 | 0 | Number of ETFs with positive 5‑day percent changes in shares held |
| `positive_percent_change_log_weighted_count` | 1.0000 | 0 | 0 | Sum of log weights (log of ETF position size) for ETFs with positive 20-day percent changes in shares held |
| `positive_percent_change_log_weighted_count_5d` | 1.0000 | 0 | 0 | Sum of log‑weights (log of ETF position size) for ETFs with positive 5‑day percent changes in shares held |
| `positive_percent_change_log_weighted_count_60d` | 1.0000 | 0 | 0 | Count of positive percent changes over 60 days, weighted by logarithm. |
| `positive_percent_change_sqrt_weighted_count_2` | 1.0000 | 0 | 0 | Count of positive percent changes, weighted by square root. |
| `positive_percent_change_sqrt_weighted_count_3` | 1.0000 | 0 | 0 | Count of positive percent changes in holdings, weighted by square root of shares. |
| `positive_sqrt_weighted_change_count_5d` | 1.0000 | 0 | 0 | Sqrt-weighted count (sum of square roots of ETF position shares) of ETFs with positive 5-trading-day absolute changes in shares held |
| `positive_change_average_5d` | 0.9096 | 0 | 0 | Mean of positive 5‑day absolute changes in ETF shares held for the stock (equal‑weight) |
| `positive_change_cubed_sum_5d` | 0.9096 | 0 | 0 | Sum of cubed positive changes in holdings over a 5-day period. |
| `positive_change_sqrt_weighted_squared_sum_2` | 0.9096 | 0 | 0 | Sum of squared positive changes, weighted by square root. |
| `positive_change_squared_sum_2` | 0.9096 | 0 | 0 | Sum of squared positive changes in holdings. |
| `positive_log_weighted_change_cubed_sum_5d` | 0.9096 | 0 | 0 | Sum of cubed positive changes in holdings weighted by logarithm of shares over 5 days. |
| `positive_log_weighted_change_squared_sum_5d` | 0.9096 | 0 | 0 | Sum of squared positive changes in holdings weighted by logarithm of shares over 5 days. |
| `positive_log_weighted_change_sum_5d` | 0.9096 | 0 | 0 | Sum of positive changes in holdings weighted by logarithm of shares over 5 days. |
| `positive_percent_change_cubed_sum` | 0.9096 | 0 | 0 | Sum of cubed positive percent changes in holdings. |
| `positive_percent_change_log_weighted_cubed_sum_5d` | 0.9096 | 0 | 0 | Sum of cubed positive percentage changes weighted by logarithm of shares over 5 days. |
| `positive_percent_change_log_weighted_simple_sum` | 0.9096 | 0 | 0 | Sum of positive percent changes, weighted by logarithm. |
| `positive_percent_change_log_weighted_squared_sum_2` | 0.9096 | 0 | 0 | Sum of squared positive percent changes, weighted by logarithm. |
| `positive_percent_change_simple_sum` | 0.9096 | 0 | 0 | Sum of positive percent changes in holdings. |
| `positive_percent_change_sqrt_weighted_cubed_sum` | 0.9096 | 0 | 0 | Sum of cubed positive percent changes, weighted by square root. |
| `positive_percent_change_sqrt_weighted_squared_sum_2` | 0.9096 | 0 | 0 | Sum of squared positive percent changes, weighted by square root. |
| `positive_percent_change_sqrt_weighted_sum_5d` | 0.9096 | 0 | 0 | Sum of positive percentage changes weighted by square root of shares over a 5-day period. |
| `positive_percent_change_squared_sum_2` | 0.9096 | 0 | 0 | Sum of squared positive percent changes. |
| `negative_change_average_5d` | 0.9089 | 0 | 0 | Mean of negative changes in holdings over a 5-day period. |
| `negative_change_log_weighted_simple_sum` | 0.9089 | 0 | 0 | Sum of negative changes, weighted by logarithm. |
| `negative_change_log_weighted_squared_sum` | 0.9089 | 0 | 0 | Sum of squared negative changes, weighted by logarithm. |
| `negative_change_squared_sum_2` | 0.9089 | 0 | 0 | Sum of squared negative changes in holdings. |
| `negative_change_sum_5d` | 0.9089 | 0 | 0 | Sum of negative changes in holdings over a 5-day period. |
| `negative_log_weighted_change_cubed_sum_5d` | 0.9089 | 0 | 0 | Sum of cubed negative changes in holdings weighted by logarithm of shares over 5 days. |
| `negative_percent_change_average_5d` | 0.9089 | 0 | 0 | Equal‑weight mean of negative 5‑day percent changes in ETF shares held across ETFs |
| `negative_percent_change_cubed_sum_5d` | 0.9089 | 0 | 0 | Sum of cubed negative percentage changes in holdings over a 5-day period. |
| `negative_percent_change_log_weighted_cubed_sum_2` | 0.9089 | 0 | 0 | Sum of cubed negative percent changes, weighted by logarithm. |
| `negative_percent_change_log_weighted_simple_sum` | 0.9089 | 0 | 0 | Sum of negative percent changes, weighted by logarithm. |
| `negative_percent_change_log_weighted_squared_sum_2` | 0.9089 | 0 | 0 | Sum of squared negative percent changes, weighted by logarithm. |
| `negative_percent_change_sqrt_weighted_cubed_sum_5d` | 0.9089 | 0 | 0 | Sum of cubed negative percentage changes weighted by square root of shares over 5 days. |
| `negative_percent_change_sqrt_weighted_squared_sum` | 0.9089 | 0 | 0 | Sum of squared negative percent changes, weighted by square root. |
| `negative_percent_change_sqrt_weighted_sum_5d` | 0.9089 | 0 | 0 | Sum of negative percentage changes weighted by square root of shares over 5 days. |
| `negative_percent_change_squared_sum_5d` | 0.9089 | 0 | 0 | Sum of squared negative percentage changes in holdings over a 5-day period. |
| `negative_percent_change_sum_5d` | 0.9089 | 0 | 0 | Sum of negative percentage changes in holdings over a 5-day period. |
| `negative_sqrt_weighted_change_cubed_sum_5d` | 0.9089 | 0 | 0 | Sum of cubed negative changes in holdings weighted by square root of shares over 5 days. |
| `negative_sqrt_weighted_change_squared_sum_5d` | 0.9089 | 0 | 0 | Sum of squared negative changes in holdings weighted by square root of shares over 5 days. |
| `negative_sqrt_weighted_change_sum_5d` | 0.9089 | 0 | 0 | Sum of negative changes in holdings weighted by square root of shares over 5 days. |
| `positive_change_sqrt_weighted_average_2` | 0.9086 | 0 | 0 | Weighted mean (square root of ETF position size) of 5‑day absolute changes in ETF shares held (delta) among ETFs with positive changes |
| `positive_log_weighted_change_mean_5d` | 0.9086 | 0 | 0 | Log‑weighted mean of positive 5‑day absolute changes in ETF shares held |
| `positive_percent_change_log_weighted_average` | 0.9086 | 0 | 0 | Weighted mean (log of ETF position size) of 5‑day percent changes in ETF shares held, using only ETFs with positive changes |
| `positive_percent_change_sqrt_weighted_mean_5d` | 0.9086 | 0 | 0 | Weighted mean (square root of ETF position size) of 5‑day percent changes in ETF shares held, using only ETFs with positive changes |
| `negative_change_sqrt_weighted_average_2` | 0.9079 | 0 | 0 | Average of negative changes, weighted by square root. |
| `negative_log_weighted_change_mean_5d` | 0.9079 | 0 | 0 | Weighted mean (log of position size) of 5‑day absolute changes in ETF shares held (delta) among ETFs with negative changes |
| `negative_percent_change_log_weighted_mean_5d` | 0.9079 | 0 | 0 | Mean of negative 5‑day percent changes in ETF shares held for the stock, weighted by the log of each ETF’s position size |
| `negative_percent_change_sqrt_weighted_average` | 0.9079 | 0 | 0 | Average of negative percent changes, weighted by square root. |
| `positive_change_cubed_sum` | 0.9043 | 0 | 0 | Sum of cubed positive changes in holdings. |
| `positive_change_log_weighted_squared_sum` | 0.9043 | 0 | 0 | Sum of squared positive changes weighted by logarithm of shares or value. |
| `positive_change_sqrt_weighted_cubed_sum` | 0.9043 | 0 | 0 | Sum of cubed positive changes weighted by square root. |
| `positive_change_sqrt_weighted_squared_sum` | 0.9043 | 0 | 0 | Sum of squared positive changes weighted by square root. |
| `positive_change_sqrt_weighted_sum` | 0.9043 | 0 | 0 | Sum of positive changes weighted by square root of shares or value. |
| `positive_change_squared_sum` | 0.9043 | 0 | 0 | Sum of squared positive changes in holdings. |
| `positive_log_weighted_change_cubed_sum_20d` | 0.9043 | 0 | 0 | Sum of cubed positive changes in holdings weighted by logarithm of shares over 20 days. |
| `positive_percent_change_average_20d` | 0.9043 | 0 | 0 | Mean of positive percentage changes in holdings over a 20-day period. |
| `positive_percent_change_cubed_sum_20d` | 0.9043 | 0 | 0 | Sum of cubed positive percentage changes in holdings over a 20-day period. |
| `positive_percent_change_log_weighted_cubed_sum` | 0.9043 | 0 | 0 | Sum of cubed positive percent changes weighted by logarithm. |
| `positive_percent_change_log_weighted_squared_sum` | 0.9043 | 0 | 0 | Sum of squared positive percent changes weighted by logarithm. |
| `positive_percent_change_log_weighted_sum` | 0.9043 | 0 | 0 | Sum of positive percent changes weighted by logarithm of shares or value. |
| `positive_percent_change_sqrt_weighted_cubed_sum_20d` | 0.9043 | 0 | 0 | Sum of cubed positive percentage changes weighted by square root of shares over 20 days. |
| `positive_percent_change_sqrt_weighted_sum` | 0.9043 | 0 | 0 | Sum of positive percent changes weighted by square root. |
| `positive_percent_change_squared_sum` | 0.9043 | 0 | 0 | Sum of squared positive percent changes in holdings. |
| `positive_percent_change_weighted_sum` | 0.9043 | 0 | 0 | Sum of positive percent changes weighted by shares or value. |
| `positive_change_log_weighted_average` | 0.9032 | 0 | 0 | Average of positive changes weighted by logarithm. |
| `positive_change_sqrt_weighted_average` | 0.9032 | 0 | 0 | Sqrt-of-position-size weighted mean of positive 20-day absolute changes in ETF shares held in the stock across ETFs |
| `positive_percent_change_log_weighted_mean_20d` | 0.9032 | 0 | 0 | Mean of positive percentage changes weighted by logarithm of shares over 20 days. |
| `positive_percent_change_sqrt_weighted_mean_20d` | 0.9032 | 0 | 0 | Mean of positive percentage changes weighted by square root of shares over 20 days. |
| `negative_change_average` | 0.9029 | 0 | 0 | Equal-weight mean of negative 20-day absolute changes in ETF shares across ETFs holding the stock |
| `negative_change_cubed_sum_20d` | 0.9029 | 0 | 0 | Sum of cubed negative changes in holdings over a 20-day period. |
| `negative_change_sqrt_weighted_cubed_sum` | 0.9029 | 0 | 0 | Sum of cubed negative changes weighted by square root. |
| `negative_change_squared_sum` | 0.9029 | 0 | 0 | Sum of squared negative changes in holdings. |
| `negative_change_weighted_sum` | 0.9029 | 0 | 0 | Sum of negative changes weighted by shares or value. |
| `negative_log_weighted_change_cubed_sum_20d` | 0.9029 | 0 | 0 | Sum of cubed negative changes in holdings weighted by logarithm of shares over 20 days. |
| `negative_log_weighted_change_squared_sum_20d` | 0.9029 | 0 | 0 | Sum of squared negative changes in holdings weighted by logarithm of shares over 20 days. |
| `negative_log_weighted_change_sum_20d` | 0.9029 | 0 | 0 | Sum of negative changes in holdings weighted by logarithm of shares over 20 days. |
| `negative_percent_change_cubed_sum` | 0.9029 | 0 | 0 | Sum of cubed negative percent changes in holdings. |
| `negative_percent_change_log_weighted_cubed_sum` | 0.9029 | 0 | 0 | Sum of cubed negative percent changes weighted by logarithm. |
| `negative_percent_change_log_weighted_squared_sum` | 0.9029 | 0 | 0 | Sum of squared negative percent changes weighted by logarithm. |
| `negative_percent_change_log_weighted_sum` | 0.9029 | 0 | 0 | Sum of negative percent changes weighted by logarithm of shares or value. |
| `negative_percent_change_sqrt_weighted_cubed_sum_20d` | 0.9029 | 0 | 0 | Sum of cubed negative percentage changes weighted by square root of shares over 20 days. |
| `negative_percent_change_sqrt_weighted_sum` | 0.9029 | 0 | 0 | Sum of negative percent changes in holdings, weighted by square root. |
| `negative_percent_change_squared_sum` | 0.9029 | 0 | 0 | Sum of squared negative percent changes in holdings. |
| `negative_percent_change_sum_20d` | 0.9029 | 0 | 0 | Sum of negative percentage changes in holdings over a 20-day period. |
| `negative_sqrt_weighted_change_sum_20d` | 0.9029 | 0 | 0 | Sum of negative changes in holdings weighted by square root of shares over 20 days. |
| `negative_change_log_weighted_average` | 0.9018 | 0 | 0 | Log-position-size–weighted mean of negative 20-day absolute changes in ETF shares across ETFs holding the stock |
| `negative_change_sqrt_weighted_average` | 0.9018 | 0 | 0 | Average of negative changes weighted by square root. |
| `negative_percent_change_log_weighted_average` | 0.9018 | 0 | 0 | Log-of-position-size weighted mean of negative 20-day percent changes in ETF shares held in the stock |
| `negative_percent_change_sqrt_weighted_mean_20d` | 0.9018 | 0 | 0 | Mean of negative percentage changes weighted by square root of shares over 20 days. |
| `positive_change_skewness_5d` | 0.8945 | 0 | 0 | Skewness of positive changes in holdings over a 5-day period. |
| `positive_change_variance_5d` | 0.8945 | 0 | 0 | Variance of positive changes in holdings over a 5-day period. |
| `positive_percent_change_variance_5d` | 0.8945 | 0 | 0 | Variance across ETFs of positive 5-trading-day percent changes in shares held (equal-weight) |
| `positive_change_log_weighted_variance_2` | 0.8943 | 0 | 0 | Variance of 5‑day absolute changes in ETF shares held (delta) among ETFs with positive changes, weighted by log of position size |
| `positive_percent_change_log_weighted_variance_5d` | 0.8943 | 0 | 0 | Variance of 5‑day percent changes in ETF shares held among ETFs with positive changes, weighted by log of position size |
| `positive_percent_change_sqrt_weighted_variance_5d` | 0.8943 | 0 | 0 | Variance of positive 5‑day percent changes in ETF shares held, weighted by the square root of ETF position size |
| `positive_sqrt_weighted_change_variance_5d` | 0.8943 | 0 | 0 | Variance across ETFs of positive 5-trading-day absolute changes in shares held, weighted by the square root of ETF position size |
| `positive_change_sqrt_weighted_skewness` | 0.8939 | 0 | 0 | Skewness of 5‑day absolute changes in ETF shares held (delta) among ETFs with positive changes, weighted by the square root of position size |
| `positive_log_weighted_change_skewness_5d` | 0.8939 | 0 | 0 | Skewness of positive changes in holdings weighted by logarithm of shares over 5 days. |
| `positive_percent_change_skewness_5d` | 0.8931 | 0 | 0 | Skewness of positive percentage changes in holdings over a 5-day period. |
| `negative_change_skewness_5d` | 0.8930 | 0 | 0 | Skewness of negative changes in holdings over a 5-day period. |
| `negative_change_variance` | 0.8930 | 0 | 0 | Variance (equal‑weight) of negative 5‑day absolute changes in ETF shares held across ETFs |
| `negative_percent_change_variance_5d` | 0.8930 | 0 | 0 | Variance across ETFs of negative 5-trading-day percent changes in shares held (equal-weight) |
| `negative_change_sqrt_weighted_variance_2` | 0.8928 | 0 | 0 | Variance of 5‑day absolute changes in ETF shares held (delta) among ETFs with negative changes, weighted by the square root of position size |
| `negative_log_weighted_change_variance_5d` | 0.8928 | 0 | 0 | Variance across ETFs of negative 5-trading-day absolute changes in shares held, weighted by the log of ETF position size |
| `negative_percent_change_log_weighted_variance_2` | 0.8928 | 0 | 0 | Variance of negative 5‑day percent changes in ETF shares held, weighted by the log of ETF position size |
| `negative_percent_change_sqrt_weighted_variance_5d` | 0.8928 | 0 | 0 | Variance across ETFs (restricted to those with negative 5‑day percent changes in shares held) weighted by the square root of ETF position size |
| `negative_change_sqrt_weighted_skewness_2` | 0.8924 | 0 | 0 | Skewness of negative changes, weighted by square root. |
| `negative_log_weighted_change_skewness_5d` | 0.8924 | 0 | 0 | Skewness of negative changes in holdings weighted by logarithm of shares over 5 days. |
| `negative_percent_change_skewness_2` | 0.8913 | 0 | 0 | Skewness of negative percent changes in holdings. |
| `positive_percent_change_log_weighted_skewness` | 0.8913 | 0 | 0 | Skewness of positive 5‑day percent changes in ETF shares held, weighted by the log of ETF position size |
| `positive_percent_change_sqrt_weighted_skewness_2` | 0.8913 | 0 | 0 | Skewness of 5‑day percent changes in ETF shares held among ETFs with positive changes, weighted by the square root of position size |
| `positive_change_log_weighted_simple_sum_60d` | 0.8909 | 0 | 0 | Sum of positive changes over 60 days, weighted by logarithm. |
| `positive_holding_change_cubed_sum_alt` | 0.8909 | 0 | 0 | Sum of cubes of positive changes in holdings (alternate calculation). |
| `positive_holding_change_log_weighted_cubed_sum` | 0.8909 | 0 | 0 | Sum of cubes of positive changes in holdings, weighted by logarithm of shares. |
| `positive_holding_change_log_weighted_squared_sum` | 0.8909 | 0 | 0 | Sum of squares of positive changes in holdings, weighted by logarithm of shares. |
| `positive_holding_change_mean` | 0.8909 | 0 | 0 | Mean (equal-weight across ETFs) of positive 60-day absolute changes in ETF shares held |
| `positive_holding_change_sqrt_weighted_cubed_sum_alt` | 0.8909 | 0 | 0 | Sum of cubes of positive changes in holdings, weighted by square root of shares (alternate calculation). |
| `positive_holding_change_sqrt_weighted_cubed_sum_alt_2` | 0.8909 | 0 | 0 | Sum of cubes of positive changes in holdings, weighted by square root of shares (alternate calculation). |
| `positive_holding_change_sqrt_weighted_squared_sum` | 0.8909 | 0 | 0 | Sum of squares of positive changes in holdings, weighted by square root of shares. |
| `positive_holding_change_squared_sum` | 0.8909 | 0 | 0 | Sum of squares (equal-weight across ETFs) of positive 60-day absolute changes in ETF shares held |
| `positive_percent_change_cubed_sum_2` | 0.8909 | 0 | 0 | Sum of cubes of positive percent changes in holdings. |
| `positive_percent_change_cubed_sum_alt` | 0.8909 | 0 | 0 | Sum of cubes of positive percent changes in holdings (alternate calculation). |
| `positive_percent_change_log_weighted_cubed_sum_60d` | 0.8909 | 0 | 0 | Sum of cubed positive percent changes over 60 days, weighted by logarithm. |
| `positive_percent_change_log_weighted_cubed_sum_alt` | 0.8909 | 0 | 0 | Sum of cubes of positive percent changes in holdings, weighted by logarithm of shares (alternate calculation). |
| `positive_percent_change_log_weighted_squared_sum_3` | 0.8909 | 0 | 0 | Sum of squares of positive percent changes in holdings, weighted by logarithm of shares. |
| `positive_percent_change_mean` | 0.8909 | 0 | 0 | Equal-weight mean of 60-trading-day percent changes in ETF shares held, considering only ETFs with positive changes |
| `positive_percent_change_sqrt_weighted_cubed_sum_2` | 0.8909 | 0 | 0 | Sum of cubes of positive percent changes in holdings, weighted by square root of shares. |
| `positive_percent_change_sqrt_weighted_cubed_sum_alt` | 0.8909 | 0 | 0 | Sum of cubes of positive percent changes in holdings, weighted by square root of shares (alternate calculation). |
| `positive_percent_change_sqrt_weighted_squared_sum_alt` | 0.8909 | 0 | 0 | Sum of squares of positive percent changes in holdings, weighted by square root of shares (alternate calculation). |
| `positive_percent_change_squared_sum_3` | 0.8909 | 0 | 0 | Sum of squares of positive percent changes in holdings. |
| `positive_change_log_weighted_average_60d` | 0.8898 | 0 | 0 | Log-weighted mean of 60-trading-day absolute changes in ETF shares held, considering only ETFs with positive changes |
| `positive_holding_change_sqrt_weighted_average` | 0.8898 | 0 | 0 | Sqrt-weighted (by sqrt of ETF position size) mean of 60-trading-day absolute changes in ETF shares held, considering only ETFs with positive changes |
| `positive_percent_change_log_weighted_average_60d` | 0.8898 | 0 | 0 | Log-weighted mean across ETFs of positive 60-day percent changes in ETF shares held |
| `positive_percent_change_sqrt_weighted_average` | 0.8898 | 0 | 0 | Sqrt-weighted mean of 60-trading-day percent changes in ETF shares held, considering only ETFs with positive changes |
| `positive_change_variance` | 0.8896 | 0 | 0 | Variance of positive changes in fund holdings. |
| `positive_percent_change_variance` | 0.8896 | 0 | 0 | Variance (equal-weight) of positive 20-day percent changes in ETF shares across ETFs holding the stock |
| `negative_percent_change_log_weighted_skewness_5d` | 0.8894 | 0 | 0 | Skewness of 5‑day percent changes in ETF shares held among ETFs with negative changes, weighted by log of position size |
| `negative_percent_change_sqrt_weighted_skewness_5d` | 0.8894 | 0 | 0 | Skewness of 5‑day percent changes in ETF shares held among ETFs with negative changes, weighted by the square root of position size |
| `positive_change_sqrt_weighted_variance` | 0.8894 | 0 | 0 | Variance of positive changes weighted by square root of shares or value. |
| `positive_percent_change_log_weighted_variance` | 0.8894 | 0 | 0 | Log-of-position-size weighted variance of positive 20-day percent changes in ETF shares held in the stock |
| `positive_percent_change_sqrt_weighted_variance` | 0.8894 | 0 | 0 | Variance of positive percent changes weighted by square root. |
| `positive_change_log_weighted_skewness` | 0.8890 | 0 | 0 | Skewness of positive changes weighted by logarithm of shares or value. |
| `positive_sqrt_weighted_change_skewness_20d` | 0.8890 | 0 | 0 | Skewness of positive changes in holdings weighted by square root of shares over 20 days. |
| `positive_percent_change_skewness` | 0.8887 | 0 | 0 | Skewness of positive percent changes in holdings. |
| `negative_change_average_60d` | 0.8876 | 0 | 0 | Mean (equal-weight) of negative 60-day absolute changes in ETF shares held across ETFs holding the stock |
| `negative_change_cubed_sum_60d` | 0.8876 | 0 | 0 | Sum of cubed negative changes in holdings over 60 days. |
| `negative_holding_change_cubed_sum` | 0.8876 | 0 | 0 | Sum of cubes of negative changes in holdings. |
| `negative_holding_change_log_weighted_cubed_sum` | 0.8876 | 0 | 0 | Sum of cubes of negative changes in holdings, weighted by logarithm of shares. |
| `negative_holding_change_log_weighted_cubed_sum_alt` | 0.8876 | 0 | 0 | Sum of cubes of negative changes in holdings, weighted by logarithm of shares (alternate calculation). |
| `negative_holding_change_log_weighted_squared_sum` | 0.8876 | 0 | 0 | Sum of squares of negative changes in holdings, weighted by logarithm of shares. |
| `negative_holding_change_sqrt_weighted_cubed_sum_alt` | 0.8876 | 0 | 0 | Sum of cubes of negative changes in holdings, weighted by square root of shares (alternate calculation). |
| `negative_holding_change_squared_sum` | 0.8876 | 0 | 0 | Sum of squares of negative changes in holdings. |
| `negative_percent_change_average_60d` | 0.8876 | 0 | 0 | Equal-weight mean of 60-trading-day percent changes in ETF shares held, considering only ETFs with negative changes |
| `negative_percent_change_cubed_sum_2` | 0.8876 | 0 | 0 | Sum of cubes of negative percent changes in holdings. |
| `negative_percent_change_cubed_sum_60d` | 0.8876 | 0 | 0 | Sum of cubed negative percent changes over 60 days. |
| `negative_percent_change_log_weighted_cubed_sum_3` | 0.8876 | 0 | 0 | Sum of cubes of negative percent changes in holdings, weighted by logarithm of shares. |
| `negative_percent_change_log_weighted_cubed_sum_alt` | 0.8876 | 0 | 0 | Sum of cubes of negative percent changes in holdings, weighted by logarithm of shares (alternate calculation). |
| `negative_percent_change_log_weighted_squared_sum_3` | 0.8876 | 0 | 0 | Sum of squares of negative percent changes in holdings, weighted by logarithm of shares. |
| `negative_percent_change_sqrt_weighted_cubed_sum` | 0.8876 | 0 | 0 | Sum of cubes of negative percent changes in holdings, weighted by square root of shares. |
| `negative_percent_change_sqrt_weighted_cubed_sum_alt` | 0.8876 | 0 | 0 | Sum of cubes of negative percent changes in holdings, weighted by square root of shares (alternate calculation). |
| `negative_percent_change_sqrt_weighted_squared_sum_2` | 0.8876 | 0 | 0 | Sum of squares of negative percent changes in holdings, weighted by square root of shares. |
| `negative_percent_change_squared_sum_2` | 0.8876 | 0 | 0 | Sum of squares of negative percent changes in holdings. |
| `negative_change_skewness` | 0.8875 | 0 | 0 | Skewness of negative changes in holdings. |
| `negative_change_variance_20d` | 0.8875 | 0 | 0 | Variance of negative changes in holdings over a 20-day period. |
| `negative_percent_change_variance_20d` | 0.8875 | 0 | 0 | Variance of negative percentage changes in holdings over a 20-day period. |
| `negative_change_sqrt_weighted_variance` | 0.8873 | 0 | 0 | Sqrt-of-position-size weighted variance of negative 20-day absolute changes in ETF shares held in the stock |
| `negative_percent_change_log_weighted_variance` | 0.8873 | 0 | 0 | Variance of 20-day percent changes in ETF shares held among ETFs with negative percent changes, weighted by the log of ETF position size |
| `negative_percent_change_sqrt_weighted_variance` | 0.8873 | 0 | 0 | Variance of negative percent changes weighted by square root. |
| `negative_change_log_weighted_skewness` | 0.8869 | 0 | 0 | Skewness of negative changes weighted by logarithm. |
| `negative_change_sqrt_weighted_skewness` | 0.8869 | 0 | 0 | Skewness of negative changes weighted by square root. |
| `positive_percent_change_sqrt_weighted_skewness` | 0.8868 | 0 | 0 | Skewness of positive percent changes weighted by square root. |
| `negative_percent_change_skewness` | 0.8863 | 0 | 0 | Skewness of negative percent changes in holdings. |
| `negative_holding_change_log_weighted_average` | 0.8862 | 0 | 0 | Log-weighted (by log of ETF position size) mean of 60-trading-day absolute changes in ETF shares held, considering only ETFs with negative changes |
| `negative_holding_change_sqrt_weighted_average` | 0.8862 | 0 | 0 | Sqrt-weighted mean across ETFs of negative 60-day absolute changes in ETF shares held |
| `negative_percent_change_log_weighted_average_60d` | 0.8862 | 0 | 0 | Log-weighted mean of 60-trading-day percent changes in ETF shares held, considering only ETFs with negative changes |
| `negative_percent_change_sqrt_weighted_average_2` | 0.8862 | 0 | 0 | Average of negative percent changes in holdings, weighted by square root of shares. |
| `negative_percent_change_log_weighted_skewness` | 0.8844 | 0 | 0 | Skewness of negative percent changes weighted by logarithm. |
| `negative_percent_change_sqrt_weighted_skewness` | 0.8844 | 0 | 0 | Skewness of negative percent changes weighted by square root. |
| `positive_change_skewness_60d` | 0.8755 | 0 | 0 | Skewness of positive changes in holdings over 60 days. |
| `positive_percent_change_variance_2` | 0.8755 | 0 | 0 | Variance (equal-weight across ETFs) of positive 60-day percent changes in ETF shares held |
| `positive_change_sqrt_weighted_variance_60d` | 0.8754 | 0 | 0 | Variance of positive changes over 60 days, weighted by square root. |
| `positive_holding_change_log_weighted_variance` | 0.8754 | 0 | 0 | Log-weighted variance across ETFs (weights = log of position size) of positive 60-day absolute changes in ETF shares held |
| `positive_percent_change_log_weighted_variance_2` | 0.8754 | 0 | 0 | Variance of positive percent changes in holdings, weighted by logarithm of shares. |
| `positive_percent_change_sqrt_weighted_variance_2` | 0.8754 | 0 | 0 | Variance of positive percent changes in holdings, weighted by square root of shares. |
| `positive_holding_change_log_weighted_skewness` | 0.8749 | 0 | 0 | Skewness of positive changes in holdings, weighted by logarithm of shares. |
| `positive_holding_change_sqrt_weighted_skewness_alt` | 0.8749 | 0 | 0 | Skewness (sqrt-weighted by position size) of positive 60-day absolute changes in ETF shares held |
| `positive_percent_change_skewness_2` | 0.8738 | 0 | 0 | Skewness (equal-weight across ETFs) of positive 60-day percent changes in ETF shares held |
| `positive_percent_change_sqrt_weighted_skewness_60d` | 0.8723 | 0 | 0 | Skewness of positive percent changes over 60 days, weighted by square root. |
| `negative_holding_change_skewness` | 0.8702 | 0 | 0 | Skewness of negative changes in holdings. |
| `negative_holding_change_variance` | 0.8702 | 0 | 0 | Variance of negative changes in holdings. |
| `negative_percent_change_variance` | 0.8702 | 0 | 0 | Variance of negative percent changes in holdings. |
| `negative_holding_change_log_weighted_variance` | 0.8700 | 0 | 0 | Variance of negative changes in holdings, weighted by logarithm of shares. |
| `negative_percent_change_log_weighted_variance_3` | 0.8700 | 0 | 0 | Log-weighted variance across ETFs of negative 60-day percent changes in ETF shares held |
| `negative_percent_change_sqrt_weighted_variance_2` | 0.8700 | 0 | 0 | Sqrt-weighted variance across ETFs of negative 60-day percent changes in ETF shares held |
| `negative_holding_change_log_weighted_skewness` | 0.8693 | 0 | 0 | Skewness of negative changes in holdings, weighted by logarithm of shares. |
| `negative_holding_change_sqrt_weighted_skewness` | 0.8693 | 0 | 0 | Skewness of negative changes in holdings, weighted by square root of shares. |
| `negative_percent_change_skewness_3` | 0.8680 | 0 | 0 | Skewness (equal-weight across ETFs) of negative 60-day percent changes in ETF shares held |
| `negative_percent_change_log_weighted_skewness_2` | 0.8659 | 0 | 0 | Skewness of negative percent changes in holdings, weighted by logarithm of shares. |
| `negative_percent_change_sqrt_weighted_skewness_2` | 0.8659 | 0 | 0 | Skewness of negative percent changes in holdings, weighted by square root of shares. |

### C 族 · 60 日持有变化（13 个）

| id | cov | users | alphas | description |
|---|---:|---:|---:|---|
| `holding_change_sqrt_weighted_count` | 1.0000 | 1 | 1 | Count of changes in holdings, weighted by square root of shares. |
| `holding_change_variance_20d` | 0.8970 | 0 | 0 | Variance across ETFs of the 20-trading-day absolute change (delta) in ETF shares held for the stock, equal-weighted across ETFs |
| `holding_change_log_weighted_cubed_sum` | 0.8948 | 0 | 0 | Sum of cubes of changes in holdings, weighted by logarithm of shares. |
| `holding_change_log_weighted_squared_sum` | 0.8948 | 0 | 0 | Sum of squares of changes in holdings, weighted by logarithm of shares. |
| `holding_change_sqrt_weighted_cubed_sum` | 0.8948 | 0 | 0 | Sum of cubes of changes in holdings, weighted by square root of shares. |
| `holding_change_sqrt_weighted_cubed_sum_alt` | 0.8948 | 0 | 0 | Sum of cubes of changes in holdings, weighted by square root of shares (alternate calculation). |
| `holding_change_sqrt_weighted_squared_sum` | 0.8948 | 0 | 0 | Sqrt-weighted sum of squares across ETFs of 60-day absolute changes in ETF shares held |
| `holding_change_squared_sum` | 0.8948 | 0 | 0 | Sum of squares of changes in holdings. |
| `holding_change_log_weighted_average` | 0.8930 | 0 | 0 | For the stock on the given date, the log-share–weighted mean 60-day change in ETF shares held across ETFs holding the stock |
| `holding_change_variance` | 0.8839 | 0 | 0 | Variance (equal-weight) of 60-day absolute changes in ETF shares held across ETFs holding the stock |
| `holding_change_skewness` | 0.8836 | 0 | 0 | Skewness (equal-weight) of the distribution of 60-day absolute changes in ETF shares held across ETFs holding the stock |
| `holding_change_log_weighted_skewness` | 0.8830 | 0 | 0 | Log-weighted skewness across ETFs of 60-day absolute changes in ETF shares held |
| `holding_change_sqrt_weighted_skewness` | 0.8830 | 0 | 0 | Skewness of changes in holdings, weighted by square root of shares. |

### B 族 · 百分比变化（有符号）（63 个）

| id | cov | users | alphas | description |
|---|---:|---:|---:|---|
| `percent_change_average_5d` | 0.9139 | 1 | 3 | Mean across ETFs of 5-trading-day percent changes in shares held (equal-weight) |
| `percent_change_count_20d` | 1.0000 | 1 | 2 | Number of ETFs contributing valid per-ETF 20-day percent-change observations for the stock (equal-weight count) |
| `percent_change_log_weighted_count` | 1.0000 | 1 | 2 | Log-weighted count (sum of log of ETF position shares) of ETFs holding the stock when computing the 5-trading-day percent change in shares held |
| `percent_change_average` | 0.9082 | 2 | 2 | Equal-weight mean of 20-day percent changes in ETF shares held in the stock across ETFs |
| `percent_change_count` | 1.0000 | 1 | 1 | Number of ETFs holding the stock that have a valid 5‑day percent change in shares held |
| `percent_change_log_weighted_count_2` | 1.0000 | 1 | 1 | Count of percent changes in holdings, weighted by logarithm of shares. |
| `percent_change_log_weighted_count_20d` | 1.0000 | 1 | 1 | Sum of log weights (log of ETF position size) across ETFs contributing per-ETF 20-day percent changes in shares held |
| `percent_change_count_2` | 1.0000 | 0 | 0 | Count of percent changes in holdings. |
| `percent_change_sqrt_weighted_count` | 1.0000 | 0 | 0 | Sqrt-of-position-size weighted count (sum of sqrt weights) across ETFs for the stock’s 20-day percent changes in shares held |
| `percent_change_sqrt_weighted_count_2` | 1.0000 | 0 | 0 | Weighted count (sum of square‑root‑position weights) of ETFs contributing 5‑day percent changes in shares held for the stock |
| `percent_change_sqrt_weighted_count_3` | 1.0000 | 0 | 0 | Count of percent changes in holdings, weighted by square root of shares. |
| `percent_change_cubed_sum_5d` | 0.9139 | 0 | 0 | Sum of cubed percentage changes in holdings over a 5-day period. |
| `percent_change_log_weighted_cubed_sum_2` | 0.9139 | 0 | 0 | Sum of cubed percent changes, weighted by logarithm. |
| `percent_change_log_weighted_simple_sum` | 0.9139 | 0 | 0 | Sum of percent changes, weighted by logarithm. |
| `percent_change_log_weighted_squared_sum_5d` | 0.9139 | 0 | 0 | Sum of squared percentage changes weighted by logarithm of shares over 5 days. |
| `percent_change_sqrt_weighted_cubed_sum_2` | 0.9139 | 0 | 0 | Sum of cubed percent changes, weighted by square root. |
| `percent_change_sqrt_weighted_squared_sum_5d` | 0.9139 | 0 | 0 | Sum of squared percentage changes weighted by square root of shares over 5 days. |
| `percent_change_sqrt_weighted_sum_5d` | 0.9139 | 0 | 0 | Sum of percentage changes weighted by square root of shares over 5 days. |
| `percent_change_squared_sum_5d` | 0.9139 | 0 | 0 | Sum of squared percentage changes in holdings over a 5-day period. |
| `percent_change_sum_5d` | 0.9139 | 0 | 0 | Sum of percentage changes in holdings over a 5-day period. |
| `percent_change_log_weighted_mean_5d` | 0.9116 | 0 | 0 | Weighted mean (log of ETF position size) of 5‑day percent changes in ETF shares held across all ETFs |
| `percent_change_sqrt_weighted_average_2` | 0.9116 | 0 | 0 | Square‑root‑weighted mean of 5‑day percent changes in ETF shares held across ETFs holding the stock |
| `percent_change_cubed_sum` | 0.9082 | 0 | 0 | Sum of cubed percent changes in holdings. |
| `percent_change_log_weighted_cubed_sum` | 0.9082 | 0 | 0 | Sum of cubed percent changes weighted by logarithm. |
| `percent_change_log_weighted_squared_sum` | 0.9082 | 0 | 0 | Sum of squared percent changes weighted by logarithm. |
| `percent_change_log_weighted_sum` | 0.9082 | 0 | 0 | Sum of percent changes weighted by logarithm of shares or value. |
| `percent_change_sqrt_weighted_cubed_sum` | 0.9082 | 0 | 0 | Sum of cubed percent changes weighted by square root. |
| `percent_change_sqrt_weighted_squared_sum` | 0.9082 | 0 | 0 | Sum of squared percent changes weighted by square root. |
| `percent_change_sqrt_weighted_sum` | 0.9082 | 0 | 0 | Sum of percent changes weighted by square root of shares or value. |
| `percent_change_squared_sum` | 0.9082 | 0 | 0 | Sum of squared percent changes in holdings. |
| `percent_change_weighted_sum` | 0.9082 | 0 | 0 | Sum of percent changes in holdings, weighted by shares or value. |
| `percent_change_log_weighted_mean_20d` | 0.9062 | 0 | 0 | Mean of percentage changes weighted by logarithm of shares over 20 days. |
| `percent_change_sqrt_weighted_average` | 0.9062 | 0 | 0 | Sqrt-weighted mean of per-ETF 20-day percent changes in ETF shares held across all ETFs holding the stock |
| `percent_change_variance_5d` | 0.9018 | 0 | 0 | Variance across all ETFs holding the stock of the 5-day percent change in their shares held (equal-weighted across ETFs) |
| `percent_change_log_weighted_variance_5d` | 0.9012 | 0 | 0 | Variance across ETFs of 5-trading-day percent changes in shares held, weighted by the log of ETF position size |
| `percent_change_sqrt_weighted_variance_2` | 0.9012 | 0 | 0 | Variance of 5‑day percent changes in ETF shares held for the stock, weighted by the square root of each ETF’s position size |
| `percent_change_skewness_5d` | 0.9002 | 0 | 0 | Skewness of percentage changes in holdings over a 5-day period. |
| `percent_change_log_weighted_skewness_2` | 0.8980 | 0 | 0 | Skewness of 5‑day percent changes in ETF shares held, weighted by the log of ETF position size |
| `percent_change_sqrt_weighted_skewness_2` | 0.8980 | 0 | 0 | Skewness of percent changes, weighted by square root. |
| `percent_change_variance` | 0.8970 | 0 | 0 | Equal-weight variance of 20-day percent changes in ETF shares held in the stock across ETFs |
| `percent_change_log_weighted_variance` | 0.8965 | 0 | 0 | Variance of 20-day percent changes in ETF shares held across all holding ETFs, weighted by the log of ETF position size |
| `percent_change_sqrt_weighted_variance` | 0.8965 | 0 | 0 | Variance of percent changes weighted by square root. |
| `percent_change_skewness` | 0.8962 | 0 | 0 | Skewness of percent changes in fund holdings. |
| `percent_change_cubed_sum_2` | 0.8948 | 0 | 0 | Sum of cubes of percent changes in holdings. |
| `percent_change_cubed_sum_alt` | 0.8948 | 0 | 0 | Sum of cubes of percent changes in holdings (alternate calculation). |
| `percent_change_log_weighted_cubed_sum_3` | 0.8948 | 0 | 0 | Sum of cubes of percent changes in holdings, weighted by logarithm of shares. |
| `percent_change_log_weighted_cubed_sum_alt` | 0.8948 | 0 | 0 | Sum of cubes of percent changes in holdings, weighted by logarithm of shares (alternate calculation). |
| `percent_change_log_weighted_squared_sum_60d` | 0.8948 | 0 | 0 | Sum of squared percent changes over 60 days, weighted by logarithm. |
| `percent_change_mean` | 0.8948 | 0 | 0 | Mean (equal-weight) of 60-day percent changes in ETF shares held across ETFs holding the stock |
| `percent_change_sqrt_weighted_cubed_sum_60d` | 0.8948 | 0 | 0 | Sum of cubed percent changes over 60 days, weighted by square root. |
| `percent_change_sqrt_weighted_simple_sum_60d` | 0.8948 | 0 | 0 | Sum of percent changes over 60 days, weighted by square root. |
| `percent_change_sqrt_weighted_squared_sum_2` | 0.8948 | 0 | 0 | Sum of squares of percent changes in holdings, weighted by square root of shares. |
| `percent_change_squared_sum_2` | 0.8948 | 0 | 0 | Sum of squares of percent changes in holdings. |
| `percent_change_log_weighted_skewness` | 0.8942 | 0 | 0 | Skewness of percent changes weighted by logarithm. |
| `percent_change_sqrt_weighted_skewness` | 0.8942 | 0 | 0 | Skewness of percent changes weighted by square root. |
| `percent_change_log_weighted_average_60d` | 0.8930 | 0 | 0 | Average of percent changes over 60 days, weighted by logarithm. |
| `percent_change_sqrt_weighted_average_60d` | 0.8930 | 0 | 0 | Sqrt-weighted mean across ETFs of 60-day percent changes in ETF shares held |
| `percent_change_variance_2` | 0.8839 | 0 | 0 | Equal-weight variance of 60-trading-day percent changes in ETF shares held across all ETFs holding the stock |
| `percent_change_skewness_2` | 0.8835 | 0 | 0 | Skewness (equal-weight) of the distribution of 60-day percent changes in ETF shares held across ETFs holding the stock |
| `percent_change_log_weighted_variance_2` | 0.8834 | 0 | 0 | Log-weighted variance of 60-day percent changes in ETF shares held across ETFs holding the stock |
| `percent_change_sqrt_weighted_variance_3` | 0.8834 | 0 | 0 | Sqrt-weighted variance across ETFs of 60-day percent changes in ETF shares held |
| `percent_change_log_weighted_skewness_3` | 0.8814 | 0 | 0 | Skewness of percent changes in holdings, weighted by logarithm of shares. |
| `percent_change_sqrt_weighted_skewness_3` | 0.8814 | 0 | 0 | Sqrt-weighted skewness across ETFs of 60-day percent changes in ETF shares held |

### A 族 · 绝对变化幅度（无符号）（50 个）

| id | cov | users | alphas | description |
|---|---:|---:|---:|---|
| `change_log_weighted_count_2` | 1.0000 | 2 | 6 | Weighted count (sum of log‑position weights) of ETFs contributing 5‑day absolute changes in shares held for the stock |
| `change_count` | 1.0000 | 4 | 5 | Number of ETFs holding the stock contributing 20-day absolute changes in shares held |
| `change_log_weighted_count_60d` | 1.0000 | 1 | 5 | Count of changes in holdings over 60 days, weighted by logarithm. |
| `change_count_60d` | 1.0000 | 3 | 4 | Count of ETFs contributing 60-day absolute changes in shares held for the stock (equal-weight count) |
| `change_log_weighted_count` | 1.0000 | 3 | 3 | Log-of-position-size weighted count (sum of log weights) across ETFs for the stock’s 20-day absolute changes in shares held |
| `change_count_5d` | 1.0000 | 2 | 2 | Number of ETFs contributing 5‑day absolute changes in shares held (delta) for the stock (equal‑weight count) |
| `change_log_weighted_average` | 0.9062 | 2 | 2 | Log-position-size–weighted mean of 20-day absolute changes in ETF shares across all ETFs holding the stock |
| `sqrt_weighted_change_count_5d` | 1.0000 | 1 | 1 | Sqrt-weighted count (sum of square roots of ETF position shares) of ETFs contributing to 5-trading-day absolute changes in shares held |
| `change_sum_5d` | 0.9139 | 1 | 1 | Sum of changes in holdings over a 5-day period. |
| `change_log_weighted_average_2` | 0.9116 | 1 | 1 | Weighted mean (log of ETF position size) of 5‑day absolute changes in ETF shares held (delta) across all ETFs |
| `change_average` | 0.9082 | 1 | 1 | Equal-weight mean of 20-day absolute changes in ETF shares across ETFs holding the stock |
| `log_weighted_change_skewness_5d` | 0.9004 | 1 | 1 | Skewness of 5‑day absolute changes in ETF shares held, weighted by the log of ETF position size |
| `change_sqrt_weighted_count` | 1.0000 | 0 | 0 | Count of changes weighted by square root of shares or value. |
| `change_average_2` | 0.9139 | 0 | 0 | Mean of 5‑day absolute changes in ETF shares held (delta) across all ETFs, equal‑weight |
| `change_cubed_sum_5d` | 0.9139 | 0 | 0 | Sum of cubed changes in holdings over a 5-day period. |
| `change_log_weighted_cubed_sum_2` | 0.9139 | 0 | 0 | Change in holdings, summed as cubes with logarithm weighting. |
| `change_log_weighted_simple_sum` | 0.9139 | 0 | 0 | Sum of changes, weighted by logarithm. |
| `change_sqrt_weighted_cubed_sum` | 0.9139 | 0 | 0 | Change in holdings, summed as cubes with square root weighting. |
| `change_sqrt_weighted_simple_sum` | 0.9139 | 0 | 0 | Change in holdings, summed with square root weighting. |
| `change_squared_sum_2` | 0.9139 | 0 | 0 | Sum of squared changes in holdings. |
| `log_weighted_change_squared_sum_5d` | 0.9139 | 0 | 0 | Sum of squares of 5‑day absolute changes in ETF shares held for the stock, weighted by the log of each ETF’s position size |
| `sqrt_weighted_change_squared_sum_5d` | 0.9139 | 0 | 0 | Sum of squared changes in holdings weighted by square root of shares over 5 days. |
| `sqrt_weighted_change_mean_5d` | 0.9116 | 0 | 0 | Weighted mean (square root of ETF position size) of 5‑day absolute changes in ETF shares held (delta) across all ETFs |
| `change_cubed_sum` | 0.9082 | 0 | 0 | Sum of cubed changes in fund holdings over the period. |
| `change_log_weighted_cubed_sum` | 0.9082 | 0 | 0 | Sum of cubed changes weighted by logarithm of shares or value. |
| `change_log_weighted_squared_sum` | 0.9082 | 0 | 0 | Sum of squared changes weighted by logarithm of shares or value. |
| `change_log_weighted_sum` | 0.9082 | 0 | 0 | Sum of changes weighted by logarithm of shares or value. |
| `change_sqrt_weighted_squared_sum` | 0.9082 | 0 | 0 | Sum of squared changes weighted by square root of shares or value. |
| `change_sqrt_weighted_sum` | 0.9082 | 0 | 0 | Sum of changes weighted by square root of shares or value. |
| `change_squared_sum` | 0.9082 | 0 | 0 | Sum of squared changes in holdings over the period. |
| `change_weighted_sum` | 0.9082 | 0 | 0 | Sum of changes in holdings weighted by shares or value. |
| `sqrt_weighted_change_cubed_sum_20d` | 0.9082 | 0 | 0 | Sum of cubed changes in holdings weighted by square root of shares over 20 days. |
| `change_sqrt_weighted_average` | 0.9062 | 0 | 0 | Sqrt-of-position-size weighted mean of 20-day absolute changes in ETF shares held in the stock across ETFs |
| `change_variance` | 0.9018 | 0 | 0 | Variance across ETFs of 5‑day absolute changes in ETF shares held (delta), equal‑weight |
| `change_sqrt_weighted_variance_2` | 0.9012 | 0 | 0 | Variance of 5‑day absolute changes in ETF shares held for the stock, weighted by the square root of each ETF’s position size |
| `log_weighted_change_variance_5d` | 0.9012 | 0 | 0 | Variance of 5‑day absolute changes in ETF shares held for the stock, weighted by the log of each ETF’s position size |
| `change_skewness_2` | 0.9010 | 0 | 0 | Skewness of changes in holdings. |
| `change_sqrt_weighted_skewness` | 0.9004 | 0 | 0 | Skewness of 5‑day absolute changes in ETF shares held, weighted by the square root of ETF position size |
| `change_skewness` | 0.8965 | 0 | 0 | Skewness of changes in fund holdings over the period. |
| `change_sqrt_weighted_variance` | 0.8965 | 0 | 0 | Variance of 20-day absolute changes in ETF shares across ETFs holding the stock, using square-root–of–position-size weights |
| `log_weighted_change_variance_20d` | 0.8965 | 0 | 0 | Variance of changes in holdings weighted by logarithm of shares over 20 days. |
| `change_log_weighted_skewness` | 0.8960 | 0 | 0 | Skewness of changes weighted by logarithm of shares or value. |
| `sqrt_weighted_change_skewness_20d` | 0.8960 | 0 | 0 | Skewness of changes in holdings weighted by square root of shares over 20 days. |
| `change_average_60d` | 0.8948 | 0 | 0 | Mean (equal-weight) of 60-day absolute changes in ETF shares held across ETFs holding the stock |
| `change_cubed_sum_60d` | 0.8948 | 0 | 0 | Sum of cubed changes in holdings over 60 days. |
| `change_log_weighted_cubed_sum_60d` | 0.8948 | 0 | 0 | Sum of cubed changes in holdings over 60 days, weighted by logarithm. |
| `change_simple_sum_60d` | 0.8948 | 0 | 0 | Sum of changes in holdings over 60 days. |
| `change_sqrt_weighted_average_60d` | 0.8930 | 0 | 0 | Average change in holdings over 60 days, weighted by square root. |
| `change_log_weighted_variance_60d` | 0.8834 | 0 | 0 | Variance of changes in holdings over 60 days, weighted by logarithm. |
| `change_sqrt_weighted_variance_60d` | 0.8834 | 0 | 0 | Variance of changes in holdings over 60 days, weighted by square root. |


---
**存档索引**：本文件 = `Claude/skills/wq-brain-ra-usa/references/_usa-other580-field-profile-20261021.md`
｜ 上游选集依据 = `_usa-fundamental-dataset-scan-20261019.md` + `recommend_datasets(USA/D1/TOP3000)`
｜ 同批换集理由 = `_usa-oth571-field-profile-20261021.md`（双杀封存）
