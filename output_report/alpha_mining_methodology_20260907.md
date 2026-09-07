# Alpha 挖掘方法论沉淀 — 2026-09-07

本会话跨 USA / IND / KOR 三区、13 波、约 91 条表达式回测。新增可提交 RA = 0，
但产出了一批可复用的实证规律。本文只记录**有实测证据**的结论。

---

## 一、选靶：金字塔优先，而非数据集优先

`get_pyramid_alphas` 应该是 S-PRE 的**第一个**查询，不是事后复盘。

**证据**：USA w30–37 八波 0 产出。事后查 `pyramids` 字段，所有候选无一例外落在
`USA/D1/MODEL` —— 该塔当季已有 4 颗、全时 34 颗 ACTIVE，而点亮门槛只需 3 颗。
prod_correlation 0.77–0.80 很大程度是**自家 ACTIVE 造成的自相食**，不是平台拥挤。

**当季分布快照（2026-09-07）**

| 状态 | 金字塔 |
|---|---|
| 差 1 颗点亮 | IND/D1/pv (2)、KOR/D1/analyst (2)、GBR/D1/model (2) |
| 差 2 颗点亮 | USA/D1/pv、USA/D1/fundamental、USA/D1/institutions、USA/D1/earnings、GBR/D1/pv、ASI/D1/{model,other,risk}、GLB/D1/other |
| 全暗区域 | CHN、HKG、DEU |

**规则**：20 颗目标的最优路线是广度优先 —— 先点亮 12 座差 1–2 颗的塔（约 21 颗），
而不是在任何单一数据集深挖。向已点亮的塔加砖既拉高 prod 又无点塔收益。

---

## 二、三个区撞三堵不同的墙

| 区域 | 主拦路闸 | 实测数据 |
|---|---|---|
| USA | `PROD_CORRELATION` | 三种结构变体全锁 0.77–0.80 |
| IND | `LOW_ROBUST_UNIVERSE_SHARPE` (limit 1.0) | 至少 8 个信号族死在此；本会话最佳 0.44 |
| KOR | `PROD_CORRELATION` + `IS_LADDER_SHARPE` | prod 地板 0.7231 |

IND 另有 USA 从未出现的 `IS_LADDER_SHARPE`（limit 1.58, year 2/4）。

---

## 三、prod 解耦：已实测无效手段清单

**核心规律：撞车在信号层时，任何「呈现层」手术都无效。**

| 手段 | 实测 | 结论 |
|---|---|---|
| decay 调整 | USA 5→15，turnover 砍半，prod 0.802→0.776 | 持仓速度不影响 prod |
| 换分组基底 | KOR industry→PCA20，prod 0.7298→0.7231 | 分组基底不影响 prod |
| `group_neutralize(market)` | USA 0.7756→0.7735，右尾反而更密 | 市场去均值无效 |
| 换信号口径 | KOR 6 个替代分析师口径，sharpe 1.61→0.63–1.01 | 强信号与拥挤同源 |
| 加腿稀释 | KOR 三腿 prod 0.7612 > 两腿 0.7231 | 见下方修正 |
| 残差差分模板 | KOR 纯解耦器 sharpe −0.35，两腿 1.61→0.24 | 剥离共同成分=剥离信号 |

### 3.1 稀释规律（修正版）

原以为 prod 随「拥挤腿权重」线性下降。**错误**。prod 是对全体生产 alpha 取 max，
新腿可能与另一批生产 alpha 相关而把 max 顶上去。

- KOR eps 权重 1/2 → 1/3（加滑点腿）：prod **0.7231 → 0.7612**
- KOR eps 权重 1/2 → 1/3（加成本离散度腿）：prod **0.7231 → 0.7534**

**规则：稀释只在新腿本身不拥挤时才降 prod。加腿前必须先单测新腿的 prod。**

### 3.2 拆腿定位法（有效）

组合 alpha 撞墙时，先分别测每条腿的 prod，再决定动哪一层。

KOR 实例：单腿 eps 0.8341、两腿(eps+价差) 0.7231 → 定位到 eps 是撞车方、价差腿在稀释。
此前在 USA 花三波调 decay/中性化/市场去均值，全部作用在呈现层，白费。

---

## 四、「剥离共同成分 = 剥离信号」（三次独立验证）

信息载体是横截面水平的信号，任何剥离共同成分的操作都会剥离信号本身。

1. **USA 时间维度解拥挤**：`ts_rank(.,252)` 0.20、`ts_zscore` 0.24、`ts_av_diff` 0.29
   —— 对照原式 1.45。而横截面维度（`group_neutralize`/sector 残差）保住 1.44–1.50。
2. **USA 水平 vs 价差**：三腿水平叠加 returns 0.079 / prod 0.80；镜像 q5−q1 价差
   returns 0.042 / prod 0.578。**让水平值收益高的性质正是让它拥挤的性质。**
3. **KOR 残差差分**：`ts_zscore(A,w) − ts_zscore(group_neutralize(A,g),w)`
   纯解耦器 sharpe −0.35，两腿版 1.61 → 0.24。

---

## 五、fitness 的算术结构

`fitness = sharpe × √(|returns| / max(turnover, 0.125))`

- turnover 降到 **0.125 以下地板生效**，再降收益为零。USA w34 把 turnover 推到
  0.059–0.094 是纯浪费。
- 地板生效后 `fitness = sharpe × 2.83 × √returns`。若 sharpe 取硬门 1.58，
  则 fitness ≥ 1.0 需要 **returns ≥ 0.050**。

### 5.1 两种降 turnover 的效果天差地别

| 作用位置 | turnover | returns | sharpe |
|---|---|---|---|
| 最终仓位向量（`decay` 设置） | −49% | −5% | −12% |
| 原始信号（`ts_mean` 平滑） | −41% | −19% | −21% |

**decay 只平滑持仓路径，不破坏每日截面排序；`ts_mean` 会破坏。**

---

## 六、等权 > 手调权重（三次独立验证）

1. **USA w36**：同字段三腿，等权 1.64/0.83/2Y2.62 vs 手调 0.5/0.3/0.2 的 1.43/0.79/2Y2.25
2. **KOR `WjPEg2zd` 权重族**：0.5/0.5 得 1.78 > 0.45/0.55 得 1.78 > 0.4/0.6 得 1.76 > 0.35/0.65 得 1.70（单调，等权在端点最优）
3. 手调权重在拟合样本内噪声，去掉自由参数后样本外反而更好。

---

## 七、腿数最优点在 2–3

| 案例 | 1 腿 | 2 腿 | 3 腿 | 4 腿 |
|---|---|---|---|---|
| IND IV+G | 0.87 / 0.39 | **1.72** | 0.63 | — |
| KOR eps+价差 | 1.19 | 1.61 | **1.63** | 1.13 |
| USA 水平叠加 | — | — | **1.64** | — |

超过最优点腿间互相抵消。腿间互补是非线性的（IND: 0.87 + 0.39 → 1.72）。

---

## 八、分组轴的选择（摩擦类信号）

**bucket(区间五分位) >> PCA 统计行业 > 通用 industry**

同为 IND 的 IV+G 两腿结构，只改分组轴：

| 分组轴 | sharpe |
|---|---|
| `bucket(rank(归一化区间), "0,1,0.2")` | **1.72** |
| `india_top500_method4_group10`（PCA） | 0.73 |
| `industry` | 0.27 |

**摩擦类信号必须按摩擦水平自身分组，按行业分组无效。**

另：同一信号只改分组轴，PCA(+0.39) vs industry(−0.25)，Δ=0.64 且符号相反 —— 
PCA 统计行业分类（从历史收益做主成分提取）在集中度高的市场携带真实信息。

---

## 九、工具缺陷与检测技巧

### 9.1 `submit_verdict` 处女提交盲区

`submit_status: 404` + `prepost_unverifiable: true` 时，`submit_checks` 为空、
`PROD_CORRELATION` 仅在 `pending`，工具据此给出 SUBMITTABLE。

**实例**：IND `qMja95Q2` 判 SUBMITTABLE，实测 prod 0.7354 不过。

**铁律：凡 `prepost_unverifiable: true`，SUBMITTABLE 不可信，必须先跑 `check_correlation`。**

### 9.2 `batch_get_alpha_metrics` 对 UNSUBMITTED 全返回 null

并据此把全部候选归入 `prescreen.REJECT`，会误导 S4 预筛。
已验证 `get_alpha_details` 对同一 alpha 返回完整指标。改用 `get_alpha_details`
或 `harvest_multisim_alphas`。

### 9.3 `get_mining_yield` 的口径

`yield_rate` 判据仅 `|sharpe|≥1.58 且 fitness≥1.0`，**不含 prod_correlation**。
IND 的 35.7% 不等于 35.7% 可提交 —— 实测 3 条 IND 高分存量 prod 0.735/0.862/0.825 全不过。

### 9.4 「指标逐位相同」= 新加变量完全无效

- USA truncation 0.05 vs 0.08：指标含 pnl 逐位相同 → 权重从未触顶，truncation 是死轴
- IND 加滑点腿：`P0Zn2llM` 与 `wpY5Zzzd` 含 pnl 逐位相同 → 该字段在 IND 退化

### 9.5 `lookINTO_SimError_message` 的误报

运行中的模拟报 `"Simulation did not get through"` 但 `raw.progress` 有值。
以 `raw.progress` / `raw.status` 为准。

### 9.6 本地 `fields` 表是跨区域超集

含平台在目标 region/universe 不提供的字段（如 `funda_regime_5d_5bucket_confidence_2`
在 USA/TOP3000/D1 不存在），也含属于其他 dataset 的字段。
**建波前必须过 `validate_expressions` + `wave_gate` 双重校验。**

---

## 十、字段可移植性警告

同一字段跨区域信息含量可差到「零 vs 最优」：

`group_buy_slippage / group_sell_slippage`
- **KOR**：最佳第三腿（1.63/1.46，`failed_ra_count=0`）
- **IND**：完全退化，贡献为零

**跨区域复用字段前必须实测。**

---

## 十一、闸门契约是区域特异的

多样性注入契约的 `required_operators` 与 `skeleton_quota` 按区域签发：

- **IND**（2026-08-23）：`[ts_corr, ts_kurtosis, bucket, trade_when]`，
  `skeleton_quota: {ratio: 1, event_gated: 1}`
- **KOR**（2026-09-03）：`[bucket, if_else, ts_corr, ts_kurtosis]`，每批 ≥2 个互异 (算子,字段) 组合
- **USA**（2026-08-26）：`group_backfill/group_cartesian_product/group_count/group_mean/
  group_neutralize/group_scale/group_std_dev/group_sum/ts_arg_max/ts_arg_min/ts_av_diff`

骨架分类器是**优先级顺序匹配**（`_lib/common.py:167`）：
`trade_when|if_else` → event_gated；`group_` → group；`divide(` → ratio；
`add|multiply` → linear_mix；else → single。
含 `divide(` 的表达式若同时含 `group_`，会被归为 group 而非 ratio。

---

## 十二、本会话最接近提交的候选

| alpha | 区域 | 指标 | 唯一阻塞 |
|---|---|---|---|
| `E5vql38G` | KOR | 1.61 / 1.45 / 2Y 2.46 / sub 1.63 / self 0.239，9 闸全过 | prod 0.7231（超 0.023） |
| `WjPEg2zd` | KOR | 1.78 / 1.64 / 2Y 2.08 | prod 0.7298 |
| `e79nxMw6` | IND | 1.72 / 0.82 / 2Y 1.54 | robust 0.31、sub 0.09 |
| `O0rnokog` | USA | 1.50 / 1.11 / 2Y 2.32 / returns 0.0791 | prod 0.7735 |

参考：平台上已 ACTIVE 的最高 prod 是 GBR `A1G7o1EE` 的 **0.6971** —— 0.7 是硬线，无容差。

---

## 十三、KOR insiders5 —— 本会话唯一「干净」的信号族（w177–179）

`KOR/D1/INSIDERS` 当季 0 颗，全暗塔。insiders5 = 韩国本土内部人交易披露，53 字段全 VECTOR。

### 13.1 两条独立候选都确认不拥挤

| alpha | 机制 | sharpe | fitness | 2Y | **prod** | **self** |
|---|---|---|---|---|---|---|
| `d5OnWkEX` | 特别关系人数量变动 | 1.23 | 0.89 | 0.91 | **0.6056** ✓ | **0.109** ✓ |
| `58QLEnqN` | 库存股占比变动（回购） | 1.15 | 0.85 | 1.53 | **0.62** ✓ | **0.179** ✓ |

两条 `all_passed: true`。韩国内部人/库存股是本土特有披露，全球量化用得少 ——
**既有信号又不拥挤**。

### 13.2 局面性质的区别（本会话最重要的战略判断）

| 族 | 问题 | 可解性 |
|---|---|---|
| USA 水平叠加 / KOR eps×价差 | 信号强但解不开拥挤 | **不可解**（四种手段全失败） |
| KOR insiders | 不拥挤但信号不够强 | **可解**（常规挖掘问题） |

**优先投入「不拥挤但信号弱」的族，而不是「信号强但拥挤」的族。**

### 13.3 持股水平层 >> 交易事件层

| 层 | 覆盖 | 代表字段 | sharpe | 2Y |
|---|---|---|---|---|
| 持股水平层 | 0.87–0.9996 | `insd5_tnc` / `insd5_trsy_ratio` | 1.23 / 1.15 | 0.91 / **1.53** |
| 交易事件层 | 0.7318 | `insd5_vol_chg` / `insd5_ghc_tr` | 0.60 / 0.60 | **−0.34 / −0.19** |

事件稀疏导致样本外不稳（2Y 为负），印证 KOR profile 的事件类数据集警告。

### 13.4 VECTOR 配对规律

单腿 VECTOR → `longCount` 126–161、`CONCENTRATED_WEIGHT` FAIL 1.0（w174 实测）。
配非 VECTOR 腿（pv106 价差）→ `longCount` 315–319、CW PASS。
**且价差腿不只是修 longCount：纯 insiders 两腿只有 0.76，配价差腿后 1.11–1.23。**

### 13.5 去重/未去重字段对是同一份数据

`insd5_trsy_ratio` 与 `insd5_trsy_real_ratio` 指标逐位相同（含 pnl 7030743）；
`insd5_ratio` 与 `insd5_real_ratio` 逐位相同（pnl 5166604）。
**后续不要同时投这两组** —— 浪费槽位。

### 13.6 腿间互补需要机制正交

`tnc` + `trsy_ratio` 三腿 = 1.11 < `tnc` 单机制 1.23 —— 同一数据集内的两个所有权指标
是部分冗余，不是互补。对照 IND `IV + G`（0.87 + 0.39 → **1.72**，机制正交）。

---

## 十四、分组轴选择规则（三区实证归纳）

**分组轴要匹配信号的经济性质：**

| 信号性质 | 最优分组轴 | 证据 |
|---|---|---|
| 摩擦 / 流动性类 | `bucket(信号自身分位)` | IND: bucket 1.72 >> PCA 0.73 >> industry 0.27 |
| 基本面 / 所有权类 | PCA 统计行业 | KOR 回购: PCA 1.15 > bucket 1.05；tnc bucket 版 0.67（2Y −0.29） |

通用 `industry` 在两类信号上都不是最优。PCA 统计行业分类（从历史收益做主成分提取）
在集中度高、集团交叉持股普遍的市场（IND / KOR）比 GICS 式业务分类更贴近真实协动结构。

---

## 十、库存优先：从"生成 alpha"转向"筛选存量"（2026-09-07 下半场）

### 10.1 触发这次转向的事实

本会话前半段跨 USA / IND / KOR / HKG 四区跑了约 **170 次新回测，可提交 RA 产出 = 0**。
同一时刻，账户平台上的 IS alpha 库存是：

| region | IS alpha 数 | region | IS alpha 数 |
|---|---|---|---|
| USA | ≥10000 | ASI | 2613 |
| EUR | ≥10000 | GBR | 2489 |
| GLB | 5251 | CHN | 318 |
| IND | 5163 | HKG | 290 |
| KOR | 4205 | JPN/TWN/AMR | 0 |

**总库存 ≥ 3 万条**。按平台自己的 RA 资格门复算，头部约 **12% 零硬闸失败**。
结论：瓶颈从来不是生成，是"在存量里定位同时满足硬闸 + prod + self 的那一小撮"。

### 10.2 被漏掉的标量：`ra.failed_ra_count`

此前每次只读 `get_alpha_details` 的 `checks.fail` 数组，漏掉了 MCP 已经算好的标量
`ra.failed_ra_count`——它是 WebDataScope `background.js::getAlphaCheckStates` 的逐字移植
（实现在 `world-quant-brain-mcp/mcp_core.py::_slim_checks`），正是 SOP 步 8.1 的资格门。

判定规则比"只看 `result == FAIL`"**严格**：

```
计入失败 ⟺ result != "PASS" and result != "PENDING"     # WARNING / ERROR 都算
```

被计数的 17 项：`HIGH_TURNOVER, LOW_TURNOVER, LOW_FITNESS, LOW_RETURNS, LOW_SHARPE,
LOW_GLB_{AMER,APAC,EMEA}_SHARPE, LOW_ASI_JPN_SHARPE, IS_LADDER_SHARPE, LOW_2Y_SHARPE,
LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE,
LOW_INVESTABILITY_CONSTRAINED_SHARPE, LOW_ROBUST_UNIVERSE_RETURNS, CONCENTRATED_WEIGHT`

**排除 SuperAlpha**：`settings` 含 `selectionHandling` / `componentActivation`、`regular.code` 为空、
`pending` 含 `SUPER_SUBMISSION` 与 `NON_SELF_SUPER_ALPHA` —— 不算 RA。

### 10.3 最重要的发现：prod 拦路虎往往是自己已提交的 alpha

生产池**包含自己的 OS alpha**，所以"未提交的孪生兄弟"必然被自己的已提交版本挡死。

| 对 | 本地互相关 | 该候选实测 prod |
|---|---|---|
| `O0GWvzbp` ~ `6XpMb0aG`（ACTIVE） | 0.9524 | **0.9522** |
| `wpEdWonx` ~ `xAdL5vmN`（ACTIVE） | 0.9849 | — |
| `1YmJPkYz` ~ `xAzxopVW`（未提交孪生） | 0.9979 | 0.9529 |

第一行四位小数吻合 —— prod 的 max 就是它与自己已提交版本的相关性。

**工程含义**：这类失败可以**零成本预测**。`compute_mutual_correlation` 在本地算 PnL、
不占平台相关性配额，返回完整 NxN 矩阵与 `max_mutually_below_subset`。
把候选池与账户 OS 池一起算一遍，任何对 OS 超阈的候选在进队列前就能丢掉。

**正确的队列顺序**（此前是反的）：

```
候选池
  → [免费] 与 OS 池 NxN 互相关 → 丢掉与自己已提交 alpha 超阈的（必失败）
  → [免费] 幸存者内部互相关     → 丢掉同族调参变体（只留最大互不相关子集）
  → [限流] check_correlation prod 队列（单并发 1-5 min/条，结果缓存 7 天）
```

### 10.4 `add(A,B)` 调参的量化代价

MEA 三条同族候选的实测互相关：

| 差异 | 互相关 |
|---|---|
| 权重 0.5/0.5 → 0.6/0.4 | **0.9883** |
| 第二腿 `ts_delta` → `ts_zscore` | 0.82 / 0.83 |

把权重挪 0.1 只改变 alpha **1.2% 的方差**。`max_mutually_below_subset` 大小 = 1：
三条里只能出一条。这就是 CLAUDE.md 禁止 `add(A,B)` 混信号调参的量化理由——
它制造"三条 alpha 的外观"和"一条 alpha 的实质"，并且每条都要单独占用限流的 prod 队列。

### 10.5 self 相关性是一个会收紧的约束

`check_correlation` 返回的 `full_os_pool_size` 显示账户已有 **21 条 OS alpha**。
self 相关性对这 21 条算，而**每提交一条池子就大一格**。

所以"20 条可提交 RA"不是 20 个独立判定：第 20 条要同时躲开 21 条历史 OS
**加上**前面 19 条新提交的。候选必须按**互不相关子集**整体选取，不能逐条贪心，
否则挖到第十几条会突然全线卡 self。

### 10.6 `/users/self/alphas` 的两个硬限制

- **offset 上限 1000**：`offset > 1000` 返回 HTTP 400 + **list 体**（不是 dict）
  `["Cannot display more than the first 1,000 alphas. Apply filters to narrow results and see more."]`。
  直接 `j.get()` 会抛 `AttributeError: 'list' object has no attribute 'get'`。
- **count 封顶 10000**：USA/EUR 都显示 10000，并非真实总数；分区后累加才是真实库存。

**真正的服务端过滤**只有：`settings.region`、`dateCreated>`、`dateCreated<`、`order`、`stage`、`hidden`。
`type` / `status` / `is.sharpe>` 传了也不缩减 —— MCP 包装层里 `region` 与 `status` 是**客户端过滤**
（见 `brain_mixin_simulation.py` 的 `api_params` 构造），写进 params 会被平台忽略。

**完整枚举配方**：按 `settings.region` 分区，每区 `order=-is.fitness` 翻前 1000 条；
需要该区全枚举时再用 `dateCreated` 窗口递归二分至每窗 ≤1000。

### 10.7 `submit_verdict` 假阳性（第二次复现）

`submit_status: 404` + `prepost_unverifiable: true` 时 `submit_verdict` 报 **假 SUBMITTABLE**。
本日在 MEA `Jj7ee6nO` / `omqEE1pn` 上二次复现（首次是 IND `qMja95Q2`，判 SUBMITTABLE 但实测 prod 0.7354）。

**规则**：`submit_verdict` 的 SUBMITTABLE 不算数，必须另跑
`check_correlation(refresh=true)` 看 `all_passed` 才作准。

### 10.8 HKG wave 4：拥挤度与信号强度的受控对照

wave 3（shortinterest2 成交/持仓类，uc 中高）→ sharpe 1.17，`risk_neutralized_sharpe` 0.96，prod 0.7158。
wave 4（shortinterest3 借贷利率/久期，uc 0–12）→ 7/7 全灭，最高 sharpe 0.51，
`risk_neutralized_sharpe` 分布 0.79 / 0.11 / −0.33 / −0.41 / −0.50 / −0.57。

同数据集族、同分组轴（`hk_equity_pca_method4_group20`）、同设置，唯一变量是字段拥挤度。
**六个负的 risk_neutralized 说明这些低拥挤字段的方向性全部来自风险因子暴露，不是 alpha。**
"冷门 = 未被挖"与"冷门 = 无效"，在 shortinterest 族里是后者。

### 10.9 区域禁令

**MEA 已被平台禁用**（2026-09-07 用户告知）：既不新挖，也不提交存量。
已实测全闸通过的 `Jj7ee6nO`（prod 0.632 / self 0.6086 / `all_passed: true`）随之作废。
所有候选池筛选与 prod 队列必须在排序阶段就过滤 `region == "MEA"`，避免浪费单并发的相关性配额。
