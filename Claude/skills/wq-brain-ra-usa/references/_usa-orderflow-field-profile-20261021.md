# order_flow_imb（Institutional Order Flow Imbalance）字段画像 · 字段八问

> as_of 2026-10-21 · USA / D1 / TOP3000。数据来源：`get_datasets(category="option")` + `get_datafields(dataset_id="order_flow_imb")`（120/120 全取，无截断）。
> 状态：**Wave 1 预注册完成，待收批**。

## §0 为什么换到本集（换集依据，先留痕）

Fundamental 低拥挤档已穷尽，逐条带证据：

| 数据集 | aC | 结论 | 依据 |
|---|---:|---|---|
| fundamental67 / 93 / 69 / 91 / 21 | 52 / 85 / 231 / 475 / 154 | 已判死 | 各自档案（8 族全试、max\|S\| ≤1.25） |
| fundamental1 | 359 | **prod 轴判死（2026-10-21）** | 25 条 / 9 机制，max S 1.12；最强形态 prod **0.7817**；同轴 `board_gov_stats` S1.56 → prod 0.8508 |
| fundamental22（ESG Data） | 81 | 不可用 | 14 字段里只有 8 个过 sharpe 过滤，描述全是 `fnd22_a0_value`/`a3_value` 式的**无语义数值**，无 codebook ⇒ 无法立经济机制（违反「先归因再推进」） |
| fundamental25（Operating Metrics） | 72 | 不可用 | 8 字段里 6 个是 `fiscalyear`/`interimnumber`/`periodtypecode`/`updatetype` 等**元数据**，唯一数值字段 `metricvalue` 是不同 KPI 混排 |

⇒ 继续在 Fundamental 内推进等于在「无信号」和「不可归因」之间二选一。换到 **option 类未点亮塔**是本轮唯一有机制可解释的新面。

## §1 是什么

交易所（ISE/CBOE 系）按**参与者类型**拆分的期权成交流：把每笔成交标成 bullish（买 call / 卖 put）或 bearish（卖 call / 买 put），
再按 6 类参与者汇总成 imbalance。核心信息不是「有多少成交」，而是**谁在押方向**。

这是与 Fundamental（年度快照）、Analyst（修正）**机制正交**的一类数据：日频、由存量持仓的再配置驱动，天然带经济学上的
「知情 vs 不知情」分层。

## §2 八问

### ① 类型

**全部 120 字段 = MATRIX 标量**（`sharpe_filter_removed: 0`，平台 120 全可用）。**不需要 `vec_*` 聚合**——与 fnd1 相反，
这是本集在工程上的最大优势：表达式可直接进 `ts_*`/`group_*`。

### ② 结构（3 个正交维度的笛卡尔积）

| 维度 | 取值 | 字段数 |
|---|---|---:|
| 参与者（6 类） | `customer`（零售）、`firm`（公司自营）、`pro_customer`（专业客户）、`market_maker`（做市商）、`broker_dealer`（经纪自营）、`proprietary`（专有交易） | 6 |
| 方向 | `bullish` / `bearish` | 2 |
| 口径 | `trade_count` / `vol` / `contracts` | 3 |
| 交易所切片 | 无后缀（全样本）/ `_ise` / `_noto` / `_otm` | 4 |
| **合成量** | `*_trade_imbalance` = 标准化后的 (bull−bear) 笔数差；`*_vol_imbalance` = 标准化后的 (bull−bear) 成交量差 | 2 |

`*_vol_imbalance` 与 `*_trade_imbalance` 是**已归一化**的差值，量纲已抹平 ⇒ 可直接跨股比较，不必再做规模标准化。
原始 `bullish_*` / `bearish_*` 计数则是**规模代理**（大公司成交多），单用会退化成 size 因子，只作辅助。

### ③ 覆盖率（四档，非常整齐）

| 档 | 覆盖 | 字段例 | 用法 |
|---|---:|---|---|
| 全样本 | **0.9058** | `customer_vol_imbalance`、`firm_vol_imbalance`、`market_maker_vol_imbalance` | 主用 |
| ISE | 0.7882 | `*_ise` | 备用（只覆盖 ISE 交易所，样本偏） |
| NOTO | 0.7728 | `*_noto` | 备用 |
| OTM | **0.7701** | `*_otm` | **语义最纯的投机切片**，单独成机制，不与全样本混用 |

0.9058 已是美国期权市场的真实上限（非全美股都有活跃期权链）。**0.77–0.79 档必须 `ts_backfill` 再进 rank，否则缺失块会被 `group_rank` 踩成空头**（fnd91 的前车之鉴）。

### ④ 更新频率

日频（字段名与平台描述均为 daily）。⇒ 换手天然高（预计 20%–60%），落在平台 1%–70% 带内，且**高换手对 F 有利**
（`F = S × sqrt(returns/0.125)`）。这与 fnd1 的「年度快照 2% 换手拖死 F」正好相反。

### ⑤ 量纲 / 分布

`*_imbalance` 是 (bull−bear)/(bull+bear) 型归一化值，理论域 **[−1, 1]**，中位数随市场整体情绪漂移 ⇒ **必须做横截面
rank 或 z-score**，不能直接用绝对值。原始计数为正数、长尾（成交笔数/合约数服从重尾分布）⇒ 若用原始量必须先 `rank` 或取对数。

### ⑥ 拥挤度（alphaCount，字段级）

| 字段 | aC | uC |
|---|---:|---:|
| `customer_trade_imbalance` | 108 | 29 |
| `customer_vol_imbalance` | 89 | 51 |
| `customer_vol_imbalance_ise` | 54 | 40 |
| `customer_vol_imbalance_noto` | 29 | 20 |
| `customer_vol_imbalance_ise`/`broker_dealer_bearish_vol` | 16 | — |
| `firm_vol_imbalance` | **4** | 4 |
| `market_maker_vol_imbalance` | 23 | 17 |
| `pro_customer_vol_imbalance` | **14** | 12 |
| `proprietary_vol_imbalance` | **0** | 0 |
| `*_contracts_noto` 多数 | 0–3 | 0–2 |

**数据集级 aC = 478 / uC = 197 / valueScore = 3**（`get_datasets`）。拥挤集中在**零售**口径（customer_*），
**机构口径（firm / proprietary / pro_customer）几乎是无人区** ⇒ 机制设计应优先走「机构 vs 零售」的对照，
而不是再做一个 retail sentiment。

### ⑦ 可用性 / 陷阱

- **陷阱 1：零售方向做反**。零售 bull 情绪是**反向指标**（不知情交易者追涨）；机构口径是**正向指标**（知情者建仓）。
  两者符号相反，这一点在文献与论坛中高度一致；若不区分参与者一刀切，会把两个相反的信号平均成 0。
- **陷阱 2：做市商方向双重解释**。做市商 bull imbalance 既可读作「他们看多」，也可读作「他们吸收了零售的卖压」
  （被动持仓）。故 M5 只作**对照探针**，不作主机制。
- **陷阱 3：`_ise` / `_noto` 是样本子集**，不是独立信号；与全样本并排比较会得到「同源两份」的假多样性。
- **陷阱 4：`contracts` 口径与 `vol` 口径高度同源**（相关系数接近 1），不要当两个机制。
- **陷阱 5：覆盖率 0.77 的 OTM 字段在 `group_rank` 下会把 NaN 排到最底部** ⇒ 必须先 `ts_backfill`。

### ⑧ 可复用性

若本集成立，「按参与者类型拆分的方向流」这一结构可平移到 EUR / ASI 的期权数据；若失败，结论应指向
「美国期权方向流已被反身性抹平」，而不是「算子没调对」。

## §3 机制地图（6 个机制，按经济含义排序）

| 机制 | 一句话 | 主字段 | 符号假设 |
|---|---|---|---|
| **M1 零售反向** | 零售追涨 → 未来跑输 | `customer_vol_imbalance` | **负** |
| **M2 机构顺向** | 自营/专业客户建仓 → 未来跑赢 | `firm_vol_imbalance`、`pro_customer_vol_imbalance` | **正** |
| **M3 知情−不知情价差** | 机构与零售的**背离度**才是纯信号（剥离市场整体情绪） | `firm_vol_imbalance − customer_vol_imbalance` | **正** |
| **M4 投机切片** | OTM 期权是彩票需求，其方向更极端地反向 | `customer_trade_imbalance_otm` | **负** |
| **M5 做市商吸收** | 做市商被动持仓 = 对手方，方向存疑 | `market_maker_vol_imbalance` | 待验（对照） |
| **M6 情绪变化** | 不是水平，而是零售情绪的**边际转向** | `ts_delta(customer_vol_imbalance)` | **负** |

## §4 Wave 1 预注册（10 条 / 6 机制 + 2 结构对照）

### 4.1 表达式

| # | 机制 | 表达式 | 方向假设 |
|---|---|---|---|
| O1 | M1 零售反向（量） | `-group_rank(ts_mean(ts_backfill(customer_vol_imbalance, 20), 5), subindustry)` | 零售越看多 → 越空 |
| O2 | M1 零售反向（笔数） | `-group_rank(ts_mean(ts_backfill(customer_trade_imbalance, 20), 5), subindustry)` | 同上，校准口径差异 |
| O3 | M2 机构顺向 | `group_rank(ts_mean(ts_backfill(firm_vol_imbalance, 20), 5), subindustry)` | 公司自营看多 → 多 |
| O4 | M2 专业客户 | `group_rank(ts_mean(ts_backfill(pro_customer_vol_imbalance, 20), 5), subindustry)` | 专业客户看多 → 多 |
| O5 | **M3 价差** | `group_rank(ts_mean(ts_backfill(firm_vol_imbalance, 20) - ts_backfill(customer_vol_imbalance, 20), 5), subindustry)` | 知情−不知情背离 → 多 |
| O6 | M4 OTM 投机 | `-group_rank(ts_mean(ts_backfill(customer_trade_imbalance_otm, 20), 5), subindustry)` | OTM 零售追涨 → 空 |
| O7 | M4 OTM 机构 | `group_rank(ts_mean(ts_backfill(firm_vol_imbalance_otm, 20), 5), subindustry)` | OTM 机构看多 → 多 |
| O8 | M6 情绪变化 | `-group_rank(ts_delta(ts_backfill(customer_vol_imbalance, 20), 5), subindustry)` | 零售情绪抬升 → 空 |
| O9 | M5 做市商（对照） | `-group_rank(ts_mean(ts_backfill(market_maker_vol_imbalance, 20), 5), subindustry)` | 吸收零售卖压 → 做多 |
| O10 | **M3 结构对照** | `group_rank(ts_mean(ts_backfill(pro_customer_vol_imbalance, 20) - ts_backfill(customer_vol_imbalance, 20), 5), subindustry)` | 换机构腿验价差是否稳健（防「firm 腿本身没信号」） |

**为什么价差不是「混信号」**：O5/O10 的两条腿来自**同一数据集、同一构造、同一量纲**，且价差本身是一个有名字的经济量
（信息不对称溢价）；这不是把两个独立 alpha 相加，也不是调权重（权重固定 ±1，无自由参数）。

**平滑的选择**：`ts_mean(·, 5)` 放在 `group_rank` **之内**——先压日频噪声再做横截面排序，避免 rank 之后再平滑造成
「秩的移动平均」这种无经济含义的量。`ts_backfill(·, 20)` 只补短缺口（数据日频，长 backfill 会拖入陈旧值）。

### 4.2 结构判据（先于指标判定）

1. **换手**：若 10 条 TO 全部 > 60%，说明 `ts_mean 5` 不够，Wave 2 用 `ts_decay_linear(10)` 或 `hump`；
   若全部 < 3%，说明 imbalance 本身是慢变量（与「日频」描述矛盾），需回查字段更新频率。
2. **覆盖率对称性**：O1–O10 的 long/short 计数比应在 0.7–1.4；若出现 1:3 级偏斜，说明 `ts_backfill` 后仍被
   NaN 拖偏 ⇒ 改 `group_backfill`。
3. **同源对照**：O1 vs O2（量 vs 笔数）、O3 vs O4（自营 vs 专业客户）、O5 vs O10（换腿）三组的 ΔS 若 < 0.15，
   说明「口径/参与者标签」不承载信息，只剩「零售 vs 其余」这一层 ⇒ 后续只保留价差结构。
4. **O9 的意义**：若 O9 与 O1 同号且更强，说明做市商 imbalance ≈ 零售 imbalance 的镜像，二者是同一信号的两侧，
   不能当两个机制计入多样性。

### 4.3 判死线

- **机制级**：某机制在 O1–O8 中 |S| < 0.5 且 TO 正常 ⇒ 记「该机制在美国期权方向流上无溢价」，不再为该机制扩变体。
- **数据集级**：若 6 个机制里 ≥ 5 个 |S| < 0.5，则判「按参与者拆分的期权方向流在 USA 已被反身性抹平」，
  转 option3（Moneyness Aggregates，aC 492）/ option40（aC 3200）。
- **prod 前置**（fnd1 教训，2026-10-21 新增）：**任何一条达到 S ≥ 1.2 的形态，先跑 `check_correlation(refresh=True)`**，
  再决定要不要为它抬 S。prod ≥ 0.7 的形态**不再投入**——抬 S 不会降 prod。

### 4.4 设置

USA / TOP3000 / D1 / decay 5 / truncation 0.08 / nanHandling ON / maxTrade OFF / pasteurization ON / unitHandling VERIFY /
neutralization **SUBINDUSTRY** / 2014-01-01 → 2023-12-31（与历史批次可比）。
Wave 2 若需换域，按 fnd1 实证：域改的是 F 与 SUB，不是 S 高度，故只在「S 已够、F/SUB 差一点」时才动。

## §5 实测结果

### 5.1 Wave 1（multisim `17eYNH8V94ou8IXecaQw4F8`，10/10 COMPLETE，2026-10-21）

| # | α | 核心 | S | F | TO | SUB | 2Y | rns | RA 失败项 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| O1 | `RRA6JoPz` | −`customer_vol_imb` | **−1.04** | −0.38 | 0.2119 | −0.69 | −1.02 | −0.57 | 4（S/F/SUB/2Y） |
| O2 | `npAP1lX3` | −`customer_trade_imb` | −0.87 | −0.30 | 0.2078 | −0.48 | −0.77 | −0.40 | 4 |
| O3 | `9qEWz322` | +`firm_vol_imb` | 0.27 | 0.05 | 0.2228 | −0.43 | 0.05 | −0.46 | 4 |
| O4 | `JjPQVkkl` | +`pro_customer_vol_imb` | 0.57 | 0.16 | 0.2025 | 0.38 | **1.58**（贴线算 FAIL） | **−0.06** | 3 |
| O5 | `vRO2KbbA` | +`firm−customer` | −0.32 | −0.06 | 0.2146 | −0.57 | −0.23 | −0.88 | 4 |
| O6 | `WjLeER2N` | −`customer_trade_imb_otm` | −0.40 | −0.11 | 0.1517 | −0.38 | −0.57 | −0.02 | 4 |
| O7 | `d5K126J2` | +`firm_vol_imb_otm` | 0.09 | 0.01 | 0.1413 | −0.39 | −0.45 | −0.36 | 4 |
| O8 | `j2e85Jko` | −`ts_delta(customer_vol_imb,5)` | −0.86 | −0.20 | 0.4448 | −0.73 | −0.83 | 0.03 | 4 |
| O9 | `RRA6JoOa` | −`market_maker_vol_imb` | 0.10 | 0.01 | 0.2237 | 0.19 | −0.30 | **0.58** | 3 |
| O10 | `npAP1ljE` | +`pro−customer` | −0.26 | −0.05 | 0.2146 | −0.12 | 0.20 | −0.75 | 4 |

设置全部为 USA/TOP3000/D1/decay5/trunc0.08/nanON/maxTradeOFF/SUBINDUSTRY（§4.4），金字塔 USA/D1/OPTION ×1.3。
**CW 全 10 条 PASS**，TO 全部落在 0.14–0.44（无一触发 LOW/HIGH_TURNOVER）。

### 5.2 归因：符号判错 + 信息只在散户腿

1. **M1「零售反向」被证伪，数据是动量族**。O1/O2/O8 三条独立字段/形态全部落在 S −0.86 ~ −1.04，
   而 rank 结构的多空近似对称 ⇒ **镜像后 ≈ +1.04 / +0.87 / +0.86**。
   与论坛 HD24383（2026-07-22）「order_flow_imb 是动量信号不是反转信号，不要加负号」**独立吻合**。
   ⇒ 本集符号约定从「负」改为「正」，M1 更名 **M1′ 零售顺向**。
2. **机构腿不是 alpha，是风格 beta**。O4 +0.57 但 `rns = −0.06`（风险中性化后归零 ⇒ 全部收益来自风格暴露）；
   O3 firm +0.27 同样低。**判 M2 无独立溢价**。
3. **价差形态互相抵消**。O5 `firm−customer` −0.32、O10 `pro−customer` −0.26 ⇒ 两腿不是可加信息；
   这也反证「零售腿是唯一携带方向信息的腿」（减去它就变负）。
4. **做市商腿是「被风格压着」的弱信号**。O9 原始 S 仅 0.10 但 **rns 0.58 > 原始 S**（全场唯一），
   说明存在一个负向风格暴露在压制它；水平太低（0.58 低于 0.8 可用线），不做主线，留作多样性备选。

### 5.3 真正的墙是 F 不是 S（算术判定，决定要不要继续投）

F = S × √(returns / max(TO, 0.125))。O1 镜像：S 1.04、returns 2.88%、TO 0.212 ⇒ **F/S = 0.365**。

| 假设 | 结果 |
|---|---|
| 维持 F/S=0.365，要 F=1.0 | 需 **S ≈ 2.0**（当前 1.04 的近 2 倍） |
| 把 TO 压到 0.125 地板（其余不变） | F 仅 0.50 |
| 只补 S 到 1.58（F/S 不变） | F ≈ 0.58，仍 FAIL |

⇒ **数据集级瓶颈是「2.9% 收益 vs 21% 换手」的配比**，抬 S 一倍才有意义。论坛三条独立样本也印证：
ZH34713 的 8 条（TOP1000，混 option3/8/9/40）S 0.51–1.63、F 0.53–1.04，**最高 F 也只有 1.04**。

### 5.4 与论坛实证的口径差（不要把别人的数字当本集可达上限）

| 来源 | 设置 | 构造 | 结果 |
|---|---|---|---|
| HD24383 | USA/**TOP1000**/D1/decay4/INDUSTRY/trunc0.05 | 单集 `ts_delta(...,5)` | TVR>20%，未给 S/F |
| ZH34713 | USA/**TOP1000**/D1/**STATISTICAL** | **混 4 个 option 集**、stage 多段合成 | S≤1.63、F≤1.04 |
| 本波 | USA/**TOP3000**/**SUBINDUSTRY** | **单数据集**、无混合 | S≤1.04（镜像后）、F≤0.38 |

三处差异（universe / 中性化域 / 是否混合）任一都可能解释 0.5 个 S 的落差；**混数据集属本仓禁项**，
所以本集的天花板应按本波的 1.04 记，不按论坛的 1.63 记。

## §6 Wave 2 预注册（6 条；只回答「1.04 能不能被合格手段抬到 1.6+」）

| # | 问题 | 表达式 | 依据 |
|---|---|---|---|
| P1 | 镜像是否真为 +1.04？ | `group_rank(ts_mean(ts_backfill(customer_vol_imbalance, 20), 5), subindustry)` | 符号测量的唯一一次确认；rank 结构应近似对称，但 truncation/decay 可能不完全 |
| P2 | 5 日窗是否太短？ | `group_rank(ts_mean(ts_backfill(customer_vol_imbalance, 20), 22), subindustry)` | 零售仓位是慢变量；长窗若抬高 S 说明 Wave 1 被日频噪声稀释 |
| P3 | 论坛的 z-score 口径是否更优？ | `group_rank(ts_zscore(ts_backfill(customer_vol_imbalance, 60), 60), subindustry)` | HD24383「改用 ts_zscore 或 ts_delta，TVR 升到 10–20%，SC 降到 <0.7」 |
| P4 | 组宽是否压了 S/F？ | `group_rank(ts_mean(ts_backfill(customer_vol_imbalance, 20), 5), industry)` | SUBINDUSTRY ≈15 只/组，z 噪声大；fnd1 Q5 实测宽组抬 F |
| P5 | 论坛模板直译效果？ | `group_rank(ts_mean(winsorize(ts_backfill(customer_vol_imbalance, 60), std=4), 5), subindustry)` | HD24383 模板的 winsorize+backfill60 两要素 |
| P6 | 只在「高信念日」交易能否抬 F？ | `trade_when(ts_rank(abs(ts_backfill(customer_vol_imbalance, 20)), 22) > 0.8, group_rank(ts_mean(ts_backfill(customer_vol_imbalance, 20), 5), subindustry), -1)` | 收益/换手配比问题 ⇒ 条件化交易是唯一「提收益密度」的合格手段（非调参） |

**判死线（先写再跑，防止事后找理由）**：
- 若 P1–P6 的 **max S < 1.3** ⇒ 判「单数据集 TOP3000 天花板 ≈1.0」，本集**不再开 Wave 3**，转 option3 / option40。
- 若某条 **S ≥ 1.3 但 F < 0.8** ⇒ 只允许再用 1 条 sim 做 decay 22 / truncation 0.04 的 F 实验；仍不过则判死。
- 若某条 **S ≥ 1.2** ⇒ 立即 `check_correlation(refresh=True)`（§4.3 prod 前置），prod ≥ 0.7 不再投入。

---

## §7 Wave 2 实测与数据集裁定（2026-10-21；预注册在 §6，先写后跑）

**multisim `36srcs1mC5bNbJS1gbM0RxAt`，6/6 COMPLETE，0 error。** 全部同设置（USA/TOP3000/D1/decay 5/
SUBINDUSTRY/trunc 0.08/nanHandling ON，2014-01-01→2023-12-31），只有表达式不同。

| # | 形态 | α | S | F | TO | SUB | 2Y | rns |
|---|---|---|---:|---:|---:|---:|---:|---:|
| P1 | `mean 5` / subindustry | `RRA6R5qj` | **1.04** | 0.38 | 0.2119 | 0.69 | 1.02 | 0.57 |
| P2 | `mean 22` / subindustry | `wp9bpNOQ` | 0.71 | 0.29 | **0.0953** | 0.29 ❌ | 0.66 | 0.47 |
| P3 | `ts_zscore(bf60,60)` | `vRO2RY9a` | **1.06** | 0.30 | 0.3612 | 0.88 | 1.05 | **0.03** |
| P4 | `mean 5` / **industry** | `KPmrPV6N` | **1.05** | 0.40 | 0.2085 | 0.69 | 1.06 | 0.58 |
| P5 | `winsorize(bf60,std=4)` + `mean 5` | `zqrbqAo1` | 1.00 | 0.36 | 0.2100 | 0.65 | 1.00 | 0.47 |
| P6 | `trade_when` 事件门控 | `Vkd0kMlG` | 0.34 | 0.09 | 0.1070 | 0.65 | **−0.22** | 0.29 |

### 7.1 归因：五个旋钮全部无效，这不是参数问题

1. **窗口**：5 日 → 22 日，S 1.04 → 0.71，同时 TO 0.212 → 0.095。
   **换手与收益同向下降，F 不改善（0.38 → 0.29）**。
   ⇒ 本集的收益是「短周期不平衡修正」，平滑不是压噪声，是**把信号本身压掉**。
   这与论坛 option 集「`ts_decay_linear 120` 把 F 从 0.74 抬到 1.39」**方向相反**——
   「平滑能救 F」不是通用规律，取决于信号的时间尺度。**别跨集照搬。**
2. **标准化**：`ts_zscore(·,60)` 把 S 抬到 1.06，但 rns 掉到 **0.03**、TO 翻到 0.36。
   ⇒ 这点增益是噪声/风格混合，**不可用作主形态**。
3. **分组域**：industry 1.05 vs subindustry 1.04（rns 0.58 vs 0.57，F 0.40 vs 0.38）。
   ⇒ 域在 ±0.01 内不动，与 fnd1「换域改 F 与 SUB、不改 S 高度」也不完全一致——这里连 F 都不动
   ⇒ **本集没有域杠杆可拉**。
4. **缩尾**：`winsorize(std=4)` 1.00，**比不缩尾还低 0.04**。
   ⇒ imbalance 已是比率型有界量，缩尾只削掉真实极端信息。
5. **事件门控**：`trade_when(|imbalance| 22 日 rank > 0.8)` 把 S 打到 0.34、2Y 打成 **−0.22**。
   ⇒ 「极端不平衡日」不是信息更浓的日，而是噪声最大的日。**这一族的条件化路线判死。**

**rns 的读法**：P1/P4 的 rns 0.57–0.58 ≈ raw S 的 55%，说明信号主体不是风格暴露
（对照 O4 的 rns −0.06），即「零售顺向」确有真实成分——**只是太弱**。

### 7.2 F 墙的算术（本集最贵的结论，可直接复用到下一集）

实测 `F/S = 0.30/1.06 = 0.283`（P1 为 0.365，P4 为 0.381）。

- 现状：`ret 2.88% / TO 21.2% / S 1.04` → `F 0.38`。
- **把 TO 压到 12.5% 地板**：`F/S = sqrt(0.0288/0.125) = 0.480`，同 S 下 F 只有 **0.50**。
- **要到 F = 1.0 且 S = 1.58**：需 `sqrt(|ret|/0.125) = 0.633` ⇒ **年化收益 5.0%**，
  是现在的 **1.74 倍**；若只压换手不提收益，需要 **S ≈ 2.71**。

⇒ **换手只是分母，收益率才是分子。** margin 只有 2.7 bp（`0.000272`）的形态，
压换手压到地板也过不了 F 闸。**选下一集先看「能不能做出 ≥5% 年化收益」，再看 S**
——这与「先找 S ≥ 1.58」的直觉相反。

### 7.3 数据集裁定

判死线第一条：「若 P1–P6 的 max S < 1.3 ⇒ 判『单数据集 TOP3000 天花板 ≈1.0』，本集不再开 Wave 3」。

实测 **max |S| = 1.06 < 1.3** ⇒ **判死成立**。两波合计 **16 条 sim / 7 个机制**：

| 机制 | 最优 \|S\| | 判定 |
|---|---:|---|
| M1 零售反向（量） | 1.04 | 方向被证伪（实为顺向，镜像 ≈ +1.04） |
| M1 零售反向（笔数） | 0.87 | 同 M1 |
| M2 机构顺向 | 0.57 | 无独立溢价（rns −0.06） |
| M3 知情−不知情价差 | 0.32 | 价差相互抵消 |
| M4 OTM 投机切片 | 0.40 | 弱 |
| M5 做市商吸收 | 0.10（rns 0.58） | 风格压制下的弱信号，不足以当主线 |
| M6 情绪变化 | 0.86 | 同 M1，镜像 |
| Wave 2 六变体（窗/标准化/域/缩尾/门控） | 1.06 | 全部无效 |

⇒ **`order_flow_imb` 在 USA/TOP3000/SUBINDUSTRY 下判 `dead_end`**：
按参与者拆分的期权方向流已被反身性抹平，天花板 ≈1.06，F 结构性不可达（§7.2）。
**不再开 Wave 3。** 切换目标 = [`_usa-option3-field-profile-20261021.md`](_usa-option3-field-profile-20261021.md)
（其 §4 已先写死判死线，再跑）。

