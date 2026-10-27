# USA / D1 / TOP3000 — fund_holdings_panel 字段画像（2026-10-23）

> 目标：未点亮塔（USA/D1/institutions）补足交付。取数一律**当场**读平台，旧画像/旧 DB 数字不作证。
> - `get_datasets(region=USA, delay=1, universe=TOP3000, category=institutions)` → fund_holdings_panel：
>   覆盖 **0.996**、字段 **30**、用户 **272**、**alphaCount 712**、valueScore 2、金字塔 institutions（乘数 1.0）
> - `get_datafields(dataset_id=fund_holdings_panel, USA, D1, TOP3000, limit=50)` → 单页全量 **30 条**，
>   `complete=true, pages_fetched=1, sharpe_filter_removed=0`
> - 塔位（`get_pyramid_alphas`，本季度）：**USA/D1/institutions = 0 ⇒ 未点亮**；同区已亮 = model 4、analyst 6、earnings 1
>   ⇒ 本数据集是合规的主挖掘目标（不是"已经点亮的塔"）。

## 1. 数据集级事实（拥挤度用数据集级 aC，不用字段级）

| 项 | 值 | 读法 |
|---|---|---|
| 覆盖 | 0.996 | 近全域，无稀疏覆盖墙（对比 other596 的字段级塌陷） |
| 字段数 | 30（15 基名 + 15 `_active` 镜像） | 全部 VECTOR |
| 用户数 | 272 | 介于"无人用"与"饱和"之间 |
| **alphaCount** | **712** | 是 institutions6（3,669）的 19%、fundamental2（141,883）的 0.5% ⇒ 低-中拥挤 |
| valueScore | 2 | 平台给的估值偏低；不作为否决理由（fnd93 value 4 仍无信号） |
| 金字塔 | institutions，乘数 1.0 | 乘数最低档，但**塔未点亮**，点亮收益 > 乘数差 |

**为什么不是 institutions6**（同塔、更常见）：同日实测 aC **3,669**（旧 DB 记 870 已过期）、覆盖 1.0、22 字段，
其中 11 个是 `inst6_*` 机器名；候选拥挤度是本数据集的 5.2 倍。**为什么不是 news/sentiment**：uen 已在本轮实测
判死（prod 0.76–0.78，`[0.7,0.8)` 桶 n=8/18/18），见 `_usa-us-equity-news-field-profile-20261023.md` §8.6。

## 2. 30 字段全表（aC 升序；`_active` = 剔除不活跃账户后的镜像）

| # | 字段 | 覆盖 | 用户 | **aC** | 语义（平台描述） |
|---|---|---:|---:|---:|---|
| 1 | top_weighted_transaction_number | 1.000 | 4 | **4** | 重仓（前 30% 权重）证券上的交易笔数 |
| 2 | herfindahl_index_transactions_active | 0.9897 | 7 | 9 | 交易价值集中度 HHI（活跃账户） |
| 3 | transaction_value_distribution_score_active | 0.9897 | 7 | 10 | 当日交易价值的分散度指数（0–1，越高越集中） |
| 4 | large_trade_count_50bps_active | 0.9897 | 10 | 10 | 单笔 > 基金 AUM 0.5% 的大单数（活跃） |
| 5 | top_weighted_account_number_active | 0.9954 | 10 | 11 | 把该证券当重仓（前 30%）的账户数（活跃） |
| 6 | security_holding_usd_value_active | 0.9954 | 11 | 12 | 全账户持仓美元值（活跃） |
| 7 | transaction_account_total_active | 0.9897 | 9 | 14 | 当日交易该证券的账户数（活跃） |
| 8 | transaction_value_distribution_score | 1.000 | 14 | 15 | 交易价值集中度（0–1，越高越集中） |
| 9 | security_transaction_usd_value_active | 0.9897 | 12 | 15 | 交易美元值（活跃） |
| 10 | top_weighted_account_number | 1.000 | 14 | 16 | 重仓账户数 |
| 11 | holding_value_distribution_score_active | 0.9954 | 13 | 16 | 持仓价值集中度 / 拥挤度（活跃） |
| 12 | large_trade_count_50bps | 1.000 | 16 | 18 | 单笔 > 0.5% AUM 的大单数 |
| 13 | holder_account_total_active | 0.9954 | 16 | 21 | 持有该 ISIN 的账户数（活跃） |
| 14 | herfindahl_index_holdings_active | 0.9954 | 17 | 22 | 持仓权重 HHI（活跃） |
| 15 | mean_security_weight_active | 0.9954 | 13 | 22 | 持仓账户内的平均组合权重（活跃） |
| 16 | boundary_transaction_usd_value_active | 0.9897 | 11 | 22 | 边界交易（建仓/清仓）美元值（活跃） |
| 17 | herfindahl_index_transactions | 1.000 | 23 | 29 | 交易账户间价值集中度 HHI |
| 18 | herfindahl_index_holdings | 1.000 | 16 | 30 | 持仓集中度 HHI（按账户权重） |
| 19 | holding_value_distribution_score | 1.000 | 25 | 31 | 持仓价值分布拥挤度 |
| 20 | mean_security_weight | 1.000 | 23 | 33 | 平均组合权重（仅统计持有它的账户） |
| 21 | boundary_transaction_usd_value | 1.000 | 21 | 34 | 边界交易美元值 |
| 22 | security_holding_usd_value | 1.000 | 27 | 38 | 全账户持仓美元值 |
| 23 | boundary_transaction_total_active | 0.9897 | 36 | 48 | 边界交易笔数（活跃） |
| 24 | transaction_account_total | 1.000 | 34 | 49 | 当日交易账户数 |
| 25 | security_transaction_usd_value | 1.000 | 29 | 55 | 交易美元值 |
| 26 | stable_boundary_trade_count_21d_active | 0.9897 | 43 | 56 | 21 日内无同类边界交易的"稳定"边界交易（活跃） |
| 27 | holder_account_total | 1.000 | 49 | 77 | 持有该 ISIN 的账户数 |
| 28 | boundary_transaction_total | 1.000 | 82 | 119 | 边界交易笔数（建仓/清仓） |
| 29 | stable_boundary_trade_count_21d | 1.000 | 98 | **159** | 21 日内无同类边界交易的稳定边界交易数 |
| 30 | — | — | — | — | （无第 30 个基名；基名 15 个，其余 15 个为 `_active`） |

**口径提醒**：`_active` 的覆盖 0.9897–0.9954 略低、aC 普遍更低，但**语义是被筛过的子样本**（剔除不活跃账户），
不是同一量的另一种写法。首波一律用**基名**（覆盖 1.000、账户池完整），`_active` 留作覆盖/纯度对照轴。

## 3. 字段画像结论（决定模板，不是决定"能不能挖"）

1. **全部 30 字段都是 VECTOR** ⇒ 任何直接进横截面算子（`rank`/`ts_*`）的写法都会报类型错；
   必须先 `vec_*` 降维。平台 live 的 vec 算子只有 7 个：`vec_min/vec_count/vec_sum/vec_max/vec_avg/vec_stddev/vec_range`
   （`research-data/operators_platform_20260904.json`；注意是 `vec_stddev` 不是 `vec_std_dev`，2026-10-23 实测
   `vec_std_dev` 被 preflight 判 `unknown_fields`）。
2. **两族量纲**：① 计数/账户数（`*_count*`、`*_total*`、`*_number`）——重尾、随规模漂移；
   ② 比率/指数（`herfindahl_*`、`*_distribution_score`、`mean_security_weight`）——已归一化到 [0,1]。
   ⇒ ① 类**必须**先做比率归一（除以账户数/持仓额）再 z-score，直接 `rank(raw)` 等于在赌市值；
   ② 类可直接做水平 z-score。
3. **美元额字段互相配对**：`security_transaction_usd_value`（流量）与 `security_holding_usd_value`（存量）
   同尺度可比 ⇒ 相除得到**账户级换手率**，是本数据集唯一能构造"利率型"信号的组合。
4. **`stable_boundary_trade_count_21d` 自带 21 日去重窗**（21 日内无同类边界交易才算），
   即平台已经替我们做了"耐久性过滤"——这是全表 aC 最高（159）也最"有设计感"的字段，指向持久需求冲击而非噪声调仓。
5. **`top_weighted_transaction_number` aC 仅 4**（全表最冷）+ 语义为"重仓证券上的交易"= 信心交易，
   冷门程度与机制强度不相关，值得单列一臂。
6. **无价格/收益字段**：`returns` 是内建。任何"持仓变化 vs 价格"的分解必须自带 `returns` 作为被减项，
   不能从数据集中读到价格。

## 4. 机制目录（每条给出可机械表达的量 + 文献锚）

| # | 机制 | 机械表达 | 方向先验 | 文献锚 |
|---|---|---|---|---|
| M1 | 机构换手率（流动性冲击） | `divide(vec_sum(transaction_usd), vec_sum(holding_usd))`，63d z | **负**（高换手=非基本面交易占比高，价格压力随后反转） | Campbell–Grossman–Wang (1993) 价格压力与反转；Sias (2004) 机构羊群 |
| M2 | 持久需求冲击（耐久边界交易） | `divide(vec_sum(stable_boundary_21d), vec_sum(holder_total))` | **正**（BSS：需求曲线下移且不撤回 ⇒ 未来正收益） | Bennett–Sias–Starks (2003) 动态机构偏好 |
| M3 | 信心交易密度 | `divide(vec_sum(top_weighted_txn), vec_sum(holder_total))` | **正**（重仓账户在本证券上加/减仓 = 有信息的下注） | Gompers–Metrick (2001) 大机构持仓 |
| M4 | 持仓集中度（拥挤） | `vec_avg(herfindahl_index_holdings)` | **负**（少数账户占绝对权重 ⇒ 拥挤 + 流动性风险，未来收益低） | Dasgupta–Pratt–Zhang (2010) 集中持股与流动性 |
| M5 | 持有人广度变化 | `ts_delta(vec_avg(holder_account_total), 63)` | **负**（持有人数快速扩张 = 关注/羊群驱动的定价，随后回落） | Sias (2004)；Barber–Odean (2008) 注意力 |
| M6 | 持仓权重累积 | `ts_delta(vec_avg(mean_security_weight), 21)` | **正**（现有持有人提高平均权重 = 加仓信心） | BSS (2003) 需求移动 |
| M7 | 大单占比 | `divide(vec_sum(large_trade_count), vec_sum(transaction_account_total))` | **负**（单笔相对 AUM 过大 = 块交易/被迫抛售，短期折价） | Coval–Stafford (2007) 资金流—业绩压力 |
| M8 | 交易价值集中度（水平） | `vec_avg(transaction_value_distribution_score)` | **负**（一天交易由单一账户主导 = 信息不对称或清仓） | 集中度—流动性折价（同 M4） |
| M9 | 交易集中度的**横截面离散** | `vec_stddev(transaction_value_distribution_score)` | **负**（集中度不稳定 = 交易结构噪声） | 噪声交易者风险（De Long et al. 1990） |
| M10 | 纯持仓流量超额 | `divide(ts_delta(vec_sum(holding_usd),63), ts_delay(vec_sum(holding_usd),63)) − ts_mean(returns,63)` | **正**（剔除价格漂移后的净申购 = 纯需求冲击） | BSS (2003) 的"持股变化 − 收益"分解 |
| M11 | 机构流量的残余反转（跨区模板移植） | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(换手率,252),252,rettype=0))` | **正**（对机构流量回归后的残差反转） | IND/institutions6 已交付族的模板（本 book 内已验证形态），按"其它模板都要试"移植 |

**方向纪律**：上表方向是先验假设，不是事后拟合。若某臂只差方向而机制成立，反向必须写得出经济理由；
「反向 S 更高」本身不构成理由（`pv106` 教训）。

## 5. 模板派生（字段画像 → 算子选择，不是拍脑袋）

| 字段画像事实 | 派生出的算子决策 |
|---|---|
| 全部 VECTOR | 第一层必为 `vec_sum`（流量/计数，可加总）或 `vec_avg`（已是比率/指数，求平均）；**不用** `vec_max` 做首波（极值对单账户噪声敏感） |
| 计数字段重尾、随规模漂移 | 先 `divide(分子, 同族分母)` 做**比率**，再 `ts_zscore(,63)`；**禁止**直接 `rank(count)` |
| 比率/指数已在 [0,1] | 直接 `ts_zscore(,63)`，不加额外归一 |
| 换手率是"存量/流量"比 | `divide(ts 流量, ts 存量)` 而非 `ts_delta`（后者会放大分母波动） |
| 平台已内置 21 日耐久窗 | 该字段直接用 63d z-score，**不叠加** second filter（避免双窗过度平滑） |
| 无价格字段 | 需要价格项时只能引入内建 `returns`，且必须是**减项/回归自变量**，不能与机构腿相加（禁混信号） |
| 日频、账户级 | 窗口取 21/63；首波不取 252（除 M11 的回归模板外）——252 会吃掉 2014 初样本 |

## 6. 波 1 设计（11 臂，已派发）

设置：USA / TOP3000 / D1 / REGULAR / decay 5 / **MARKET** / trunc 0.08 / pasteurization ON /
unitHandling VERIFY / nanHandling ON / maxTrade OFF / 2014-01-01 → 2023-12-31。
（中性化为 MARKET 而非 SUBINDUSTRY：uen 波 3 的归因证明 SUBINDUSTRY 会杀掉大市值腿并压垮 SUB；
本数据集覆盖率 0.996，同样以 MARKET 起步。）

| 臂 | 机制 | 表达式 |
|---|---|---|
| A1 | M1 换手率 | `-rank(ts_zscore(divide(vec_sum(security_transaction_usd_value),vec_sum(security_holding_usd_value)),63))` |
| A2 | M2 耐久需求 | `rank(ts_zscore(divide(vec_sum(stable_boundary_trade_count_21d),vec_sum(holder_account_total)),63))` |
| A3 | M3 信心交易 | `rank(ts_zscore(divide(vec_sum(top_weighted_transaction_number),vec_sum(holder_account_total)),63))` |
| A4 | M4 集中度 | `-rank(ts_zscore(vec_avg(herfindahl_index_holdings),63))` |
| A5 | M5 广度变化 | `-rank(ts_delta(vec_avg(holder_account_total),63))` |
| A6 | M6 权重累积 | `rank(ts_delta(vec_avg(mean_security_weight),21))` |
| A7 | M7 大单占比 | `-rank(ts_zscore(divide(vec_sum(large_trade_count_50bps),vec_sum(transaction_account_total)),63))` |
| A8 | M8 交易集中度 | `-rank(ts_zscore(vec_avg(transaction_value_distribution_score),63))` |
| A9 | M9 集中度离散 | `-rank(ts_zscore(vec_stddev(transaction_value_distribution_score),63))` |
| A10 | M10 纯流量 | `rank(subtract(divide(ts_delta(vec_sum(security_holding_usd_value),63),ts_delay(vec_sum(security_holding_usd_value),63)),ts_mean(returns,63)))` |
| A11 | M11 跨区模板 | `rank(-ts_regression(ts_zscore(returns,252),ts_zscore(divide(vec_sum(security_transaction_usd_value),vec_sum(security_holding_usd_value)),252),252,rettype=0))` |

**门禁记录**（2026-10-23）：
- 本地 `wqb.expression.op_arity.check_expressions` → **11/11 PASS**；调用点数 3–8（全部 < 10 硬顶）。
- `preflight_expressions` → `valid=true`、`unknown_fields=[]`、11 个字段全部在平台目录、
  `any_changed=false`（VECTOR 包裹 0 改动）、`vector_fields` 30 条全列。
- 派发：`tools/submit_batch.py --spec tracking/USA/runs/usa_fhp_w1_spec.json`
  - 批 A（A1–A8）→ multisim `3rxfo6cn94iIb6oUitrLzGz`
  - 批 B（A9–A11）→ multisim `tAiPNbIQ4Cq9DC2H8bW2is`

## 7. 预登记判据（收批时逐条执行，不临时加码）

1. **任一臂 RA 全过**（S ≥ 1.58、F ≥ 1.0、SUB/S ≥ 0.435、2Y ≥ 1.58、TO ∈ (0.01,0.70)、CW ≤ 0.1）
   ⇒ **立即**做 `check_correlation(refresh=True)` prod 探针，不先扩同族（`risk60` 教训：扩族后才发现 prod 0.99）。
2. **SUB 是比值闸**：门槛 = 0.435 × S，抬 S 同步抬门槛；不得靠抬 S 破 SUB。
3. **归因优先于扩批**：1–2 闸不过时先判是 2Y / SUB / Fitness / 换手哪一类，再决定换窗/换壳/换字段；**不得盲扫**。
4. **D0 必读**：若所有臂换手 < 2% ⇒ 字段准静态，本集停；若裸信号换手高而重壳被压平 ⇒ 是壳压平，波 2 换中档壳。
5. **全弱判据**：11 个机制臂全部 `|S| < 0.8` ⇒ 停投本集（只在**全部**机制试过后成立）。
6. **prod 判死**：任一 RA 全过臂 prod ≥ 0.75 ⇒ 记 `dead_end`；`[0.7,0.8)` 每出现 1 颗记「拥挤族」；
   `[0.9,1]` ≥10 颗才算饱和。
7. **塔位**：本集属 USA/D1/institutions（当前 0 颗）。若某臂同时挂到已亮的 model/analyst 塔，
   该塔位**不得**作为主候选理由（用户裁定：已点亮塔不优选）。

## 8. 取证状态（诚实记录；2026-10-23 13:4x 已恢复，原故障记录保留）

- **故障期（已结束）**：`tools/forum_recon.py` 首轮 8 次搜索成功 / 48 命中 / 29 次读帖 429 / `reads_ok=0`
  ⇒ `status=error, reason_code=read_failed`，落库键 `USA/forum_recon_error_b31d31827a` / `..._c1d02058ef`。
  按 `wqb.recon_evidence` 契约，**故障不等于"论坛无解"**，当时不作判死证据、不入缓存。
  ⚠ 本条保留是为了防止后来者把"当时没查到"读成"论坛没有"。
- **恢复后（同日晚）**：MCP `search_forum_posts` + `read_forum_post` 均通了，本轮实读到 3 篇直接相关的降换手帖：
  | 帖 | 票 | 对本数据集的作用 |
  |---|---:|---|
  | 换手率是可以设计的：target_tvr 家族（KK37637） | 25 | 定位 `ts_target_tvr_{decay,hump,delta_limit}` 是**目标换手求解器**；警告「target 设得离裸换手太近 ⇒ 优化器在边界硬压」 |
  | 【机理拆解】换手率是隐形天花板（LL46807） | 23 | fitness 公式与 margin 第二关；杠杆效果排序：**源头平滑 > hump/限速器 > 拉长持有语义**；且「某些族的换手=信号本体，任何降换手都与信号单调共变」 |
  | 降低 Turnover 时，怎样避免把信号一起磨平（YX50005） | 14 | decay=平滑持续信号（过大反应变慢）/ hump=抑制小幅反复 / trade_when=控更新时点；判据是「换手降但预测能力与近期表现同时消失 ⇒ 平滑过度」 |
- **本数据集适用性判读**：第 2 篇的「换手=信号本体」正是本族波 1 的实测形态（decay 5→20 掉 40% Sharpe），
  但它留了一个出口——「hump 在窗口冻结时是唯一的 CW/换手双轴杠杆」与「拉长持有周期语义（大窗口）」，
  这两条都**不改信号排序**，只是延后交易，故波 3 以它们为主轴（§10.2）。
- 外部文献锚（§4）仍是机制来源，论坛补的是**平台实现层**（参数尺度、失效方向），两者不互相替代。

## 9. 波 1 收批（2026-10-23，multisim `3rxfo6cn94iIb6oUitrLzGz` + `tAiPNbIQ4Cq9DC2H8bW2is`）

设置：TOP3000/D1/MARKET/decay 5/trunc 0.08/2014–2023。

| 臂 | 机制 | alpha | S | F | TO | 2Y | SUB | 裁决 |
|---|---|---|---:|---:|---:|---:|---:|---|
| A1 | 换手率（水平） | `akVQ13g9` | 0.02 | 0.00 | 59.7% | −1.33 | −0.04 | 死（水平量零信息） |
| A2 | 耐久边界交易 | `88vEpqZv` | −0.23 | −0.04 | 40.1% | −0.70 | 0.22 | 死 |
| A3 | 信心交易密度 | `akVQ139v` | −0.36 | −0.07 | 47.0% | 0.05 | −0.37 | 弱（反向后 0.36，仍 < 0.8） |
| A4 | 持仓 HHI | `58jApVd5` | 0.02 | 0.00 | 11.5% | −0.06 | −0.42 | 死（低换手但零信号） |
| A5 | 持有人广度 Δ | `xA12Na7n` | 0.19 | 0.07 | 6.4% | 0.65 | 0.21 | 死 |
| A6 | 持仓权重 Δ | `58jApVmn` | **−0.59** | −0.34 | 14.1% | −0.34 | −0.54 | 弱（全表最强的"变化"臂；反向 0.59） |
| A7 | 大单占比 | `VkdmGorb` | 0.29 | 0.06 | 33.8% | 0.89 | 0.30 | 死 |
| A8 | 交易集中度 | `78ovzVp1` | −0.20 | −0.03 | 60.2% | 0.35 | −0.38 | 死 |
| A9 | 交易集中度离散 | `1Yjlp13K` | 0.10 | 0.01 | **88.2%** | −0.19 | −0.25 | 死（且换手爆表） |
| A10 | 纯持仓流量 | `bl8rQVmN` | −0.43 | −0.29 | 8.2% | −0.35 | −0.54 | **UNITS 警告**：`subtract` 第 1 项单位不符（`ts_mean(returns,63)` 是 `TSPrice`，增长比是无量纲）⇒ 该结果不可信，须改 zscore 空间重跑 |
| **A11** | **机构流量残余反转** | **`E5V8GYjP`** | **1.36** | 0.62 | **76.9%** | 1.27 | **1.25** | **唯一真信号**：S 差 0.22、F 差 0.38、TO 超 6.9pp、IS_LADDER 1.27；`risk_neutralized_sharpe = 3.49`；塔位 institutions+PV，effective 2 |

### 9.1 归因（先归因再推进）

1. **水平类一律为零**：A1 换手率 0.02、A4 HHI 0.02、A7 0.29、A8 −0.20、A9 0.10。
   ⇒ 账户级持仓/交易的**横截面结构**在 USA 已被定价干净（与 Gompers–Metrick 2001 一致：机构持股结构本身不是定价错误）。
2. **变化类有微弱信号，但量级不足**：A2 −0.23、A3 −0.36、A5 0.19、A6 −0.59、A10 −0.43。
   最强的是 A6（持有人平均权重 21d 变化）−0.59 —— 仍低于 0.8 的"值得救"线（预登记判据 5 只在**全部**臂 `< 0.8` 时才判停，而 A11 已过线，故本集不停）。
3. **信息在"条件关系"里，不在单量里**：A11 把收益对机构换手率做 252d 回归取残差，S 1.36 且风险中性后 **3.49**。
   与 uen 波 1 的结论同构（M6：语调×关注度的**联合动态**才有效，单量无效）。本数据集的可复用结论：
   **机构持仓面板的价值是"当条件变量"，不是"当信号本体"**。
4. **decay 是反向杠杆（已实测，不是推测）**：同一表达式 decay 5 → 20，S 1.36 → **0.82**（W252）/ 0.78（W126），
   TO 76.9% → 40.5%。⇒ 收益在**日频**，平滑直接抹掉 40% 的 Sharpe；换手墙不能用 decay 破。
   （这次是"先付一次代价把轴测死"，波 2 不再重复 decay 网格。）

### 9.2 波 2b 收批（2026-10-23 13:4x，9 臂 → 实际建出 8 臂：RAM 被平台拒、d60/d126 被 429 未建）

| 臂 | 设置 | alpha | S | F | TO | RET | 2Y | SUB | 关键告警 | 裁决 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| H1 | MARKET + hump 0.01 | `YPxE5L6M` | −0.30 | −0.07 | **0.0047** | −0.006 | 0.42 | 0.00 | LOW_SHARPE/LOW_FITNESS/**LOW_TURNOVER** | **持仓冻结**（见下） |
| H2 | MARKET + hump 0.02 | `omoJ68pm` | −0.30 | −0.07 | **0.0047** | −0.006 | 0.42 | 0.00 | 同上 | 与 H1 **逐位相同** ⇒ 0.01/0.02 都远超信号日变动尺度 |
| F1 | MARKET 回归窗 63 | `88vE35oa` | 1.17 | 0.48 | 0.7396 | 0.127 | 1.52 | 1.07 | LOW_SHARPE/LOW_FITNESS/HIGH_TURNOVER/IS_LADDER | W63 < W252（1.36），**长窗更优**；`risk_neutralized_sharpe=3.50` |
| S1 | MARKET 持仓增长 z − 收益 z | `78ovZ7A5` | 0.66 | 0.27 | 0.3908 | 0.0677 | 0.55 | 0.57 | 三挂 | 单位修正已生效、无 UNITS 告警，但量级仅 A6 水平 |
| S2 | MARKET 流量加速度 | `1Yjlxkbz` | 0.48 | 0.08 | 0.6908 | 0.0178 | **−1.58** | −0.12 | 四挂（含 LOW_2Y） | **死**：2Y 强负 ⇒ 加速度方向不稳定 |
| N1 | **STATISTICAL** A11 原式 | **`1YjlxYWk`** | **2.84** | **1.04** | **0.7628** | 0.1032 | **2.72** | **2.37** | **仅 HIGH_TURNOVER**（差 6.3pp） | **本族首个 RA 准全过臂** |
| N2 | STATISTICAL + hump 0.01 | `pwvMPwaj` | −0.47 | — | 0.0285 | — | — | — | 冻结 | 与 H1 同型 |
| N3 | SLOW_AND_FAST A11 原式 | `2rjXOneJ` | 2.02 | 0.53 | 0.8738 | — | 1.07 | — | LOW_FITNESS/HIGH_TURNOVER/IS_LADDER | 两轴皆劣于 STATISTICAL |

**四条实测结论（先归因，再进波 3）**

1. **中性化轴是决定性的，且 STATISTICAL 完胜**：同一表达式 MARKET 1.36 → STATISTICAL **2.84**（+109%），
   SLOW_AND_FAST 只到 2.02。STATISTICAL 臂的 `risk_neutralized_sharpe` 未报，但它在 IS 侧把 2Y 从 1.27 抬到 **2.72**、SUB 1.25 → **2.37**
   ⇒ 本族的收益确实压在**风险因子暴露**上（与 §10 的原始假设一致）。塔位仍 `institutions(×1.0) + pv(×1.1)`，effective 2。
2. **`hump` 的失败是"尺度错"不是"机制错"（本轮最重要的可复用结论）**：
   `hump` 语义是「持仓变化 < 阈值就不交易」，而信号是 `rank()` 输出，TOP3000 下相邻档差 ≈ 1/3000 ≈ **0.00033**；
   `hump=0.01` 相当于要求一天内跳 **30 个档位**才交易 ⇒ 实际效果是**冻结持仓**（TO 76.9% → 0.47%，且 0.01 与 0.02 逐位相同）。
   跨数据集佐证：`techindi_model` 波 2c 的 `hump=0.01` 同样把 TO 0.2726 打到 **0.0346**（`tracking/USA/runs/usa_tm_w1_notes.md` §9.6）。
   ⇒ **在 rank 尺度信号上 hump 必须用 1e-3 量级**，0.01 是"看起来温和、实为冻结"的陷阱。
3. **换手墙的真实缺口只有 6.3pp**，且 F=1.04 已在线上：N1 的 RET/TO = 0.1032/0.7628 = 0.135，
   只要 TO 降到 0.62 且 RET 少掉不超过 ~7%，F 仍 ≈ 1.04（F 的 S 与 RET/TO 反向抵消）。
4. **S2 死亡、F1/S1 皆弱** ⇒ 再次确认「只有**条件关系**（收益对机构换手率的回归残差）带信号」，
   水平量、变化量、加速度三条独立路径全部 < 0.7。本数据集**只挖这一条机制**，不再扩族（预登记判据 5）。

## 10. 波 2b 设计（换手 × 中性化轴，9 臂）

由上节两条事实定轴：**信号怕平滑**（decay 有害）⇒ 换手只能用**不改信号形状的 hump**；
**风险中性 S 3.49 ≫ 原始 1.36** ⇒ 因子暴露是主约束 ⇒ 中性化轴才是提 S 的正路。

| 组 | 臂 | 设计意图 | 表达式差异 |
|---|---|---|---|
| MARKET / decay 5 | H1 | hump 0.01：限单日仓位变化、保留信号排序 | `hump(rank(...A11...),hump=0.01)` |
| MARKET / decay 5 | H2 | hump 0.02（更紧） | `hump(...,hump=0.02)` |
| MARKET / decay 5 | F1 | 回归窗 252→63：本数据集是**日频账户级**，不是季频 13F，半衰期可能更短 | `ts_regression(...,63,...)` |
| MARKET / decay 5 | S1 | M10 单位修正（zscore 空间相减，无量纲） | `rank(subtract(ts_zscore(增长率,252),ts_zscore(returns,252)))` |
| MARKET / decay 5 | S2 | 流量**加速度**（A1 水平死、A6 变化最强 ⇒ 变化量族优先） | `-rank(ts_zscore(ts_delta(换手率,21),252))` |
| STATISTICAL / decay 5 | N1 | 风险模型中性化（主假设：提 S 且压换手） | A11 原式 |
| STATISTICAL / decay 5 | N2 | N1 + hump 0.01（两杠杆叠加） | A11 + hump |
| SLOW_AND_FAST / decay 5 | N3 | 另一条风险模型路径（慢/快因子分离） | A11 原式 |

**RAM 已实测不可用**：`BODY: {"settings":{"neutralization":["\"RAM\" is not a valid choice."]}}`（USA）。
`CROWDING` 按 `tracking/USA/priors/usa_priors.json` 的既有记录（USA 连续失败）本轮不碰。

**预登记裁决（波 2b 收批时逐条执行）** —— 执行结果：
- ✅ 任一臂 RA 全过 ⇒ 立刻 prod 探针：无一臂全过（N1 仅差 HIGH_TURNOVER），**prod 探针未触发**。
- ❌ 若 H1/H2 保住 S ≥ 1.3 且 TO < 70%：H1/H2 冻结（S −0.30），预登记分支作废，原因见 §9.2 结论 2。
- ✅ 若 N1/N3 把 S 抬过 1.58 但 TO 仍 > 70% ⇒ 两杠杆叠加：**命中**，波 3 做交叉。
- ⏳ 若 hump 也把 S 压到 < 1.0 ⇒ 判不可交付：本轮**不成立**（hump 用的是错尺度，还没在 1e-3 档试过），故先跑波 3 再判。

### 10.2 波 3 设计（N1 核心 × 换手效率，7 臂，2026-10-23 13:43 已派发）

设置：USA/TOP3000/**D1/STATISTICAL**/trunc 0.08/nanHandling ON/maxTrade OFF/2014–2023。
核心 = N1（`rank(-ts_regression(ts_zscore(returns,252),ts_zscore(换手率),252,rettype=0))`），算子调用 7 点，全部臂 ≤ 8 < 10。

| 组 | 臂 | 表达式壳 | 依据 |
|---|---|---|---|
| 目标换手（主） | T1 | `ts_target_tvr_hump(core, target_tvr=0.66)` | 论坛 25 票帖：target_tvr 是**内部求解器**，直接把 TO 钉到目标；0.66 给 4pp 余量 |
| 目标换手（深） | T2 | `ts_target_tvr_hump(core, target_tvr=0.58)` | 深档：若 T1 的 S 损失来自"边界硬压"，深档应更差；若更好则说明是去噪 |
| 目标换手（对照） | T3 | `ts_target_tvr_decay(core, target_tvr=0.66)` | 与 T1 同目标、不同平滑底子（decay vs hump）⇒ 分离"目标"与"底子" |
| 正确尺度 hump | H1 | `hump(core, hump=0.0005)` | ≈ **1.5 个 rank 档位**（1/3000），只滤掉无意义抖动 |
| 正确尺度 hump | H2 | `hump(core, hump=0.001)` | ≈ 3 档 |
| 正确尺度 hump | H3 | `hump(core, hump=0.002)` | ≈ 6 档，可能开始伤信号（上界探针） |
| 设置对照 | C1 | core @ **decay 8** | B 组：mild decay 是否比 hump 更便宜（波 1 只测到 decay 20，中间档空白） |

派发记录：6 臂 → `https://api.worldquantbrain.com/simulations/1ARKxP3hF4vdabm17YUSnkwo`；
C1 → `https://api.worldquantbrain.com/simulations/VL8aIbHn5bhb9BP172EEsT`。
门禁：`op_arity` 7/7 通过、调用点 8/8/8/8/8/8/7；`preflight_expressions` valid、`unknown_fields=[]`、`any_changed=false`。

**预登记裁决（波 3 收批时逐条执行）**：
- 任一臂 RA 全过（TO ≤ 0.70 且其余 17 项不新增失败）⇒ **立即** `check_correlation(refresh=True)` 双闸（prod / self < 0.7 <!-- from config.prod_corr_max -->）；不扩族。
- 若 T1/T2 的 S 保留 ≥ 2.5 且 TO ≤ 0.70 ⇒ 取 F 最高者为本族交付候选；若 prod ≥ 0.75 ⇒ 按 D0-P 判死封存。
- 若 TvR 全部 S < 2.0 而 H2/H3 的 S 保留 > 2.5 ⇒ 说明"目标求解器在边界硬压"确有其事（论坛帖的警告成立），改用固定 hump。
- 若 hump 三档 S 全部 < 1.5 ⇒ 本族换手与信号**单调共变**（论坛帖「换手=信号本体」形态）⇒ 判「fhp 残余反转族不可交付」，转同塔其它机制或换塔，不再调壳。

### 10.3 波 3 收批（2026-10-23 13:56，multisim `1ARKxP3hF4vdabm17YUSnkwo` + `VL8aIbHn5bhb9BP172EEsT`）

全部 STATISTICAL、trunc 0.08、decay 5（C1 除外）。

| 臂 | 壳 | alpha | S | F | TO | RET/TO | 2Y | SUB | RA 失败项 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| T1 | `ts_target_tvr_hump 0.66` | `xA123e9l` | 2.08 | 0.85 | 0.3924 | 0.165 | 1.97 | 1.42 | LOW_FITNESS |
| T2 | `ts_target_tvr_hump 0.58` | `gJWgbmwl` | 1.81 | 0.71 | 0.3417 | 0.155 | 1.52 | 1.26 | LOW_FITNESS, IS_LADDER |
| T3 | `ts_target_tvr_decay 0.66` | `leM5v72x` | 1.91 | 0.91 | 0.3221 | 0.227 | 1.13 | 1.43 | LOW_FITNESS, IS_LADDER |
| H1 | `hump 0.0005` | `A1QrNnbl` | 1.55 | 0.59 | 0.3227 | 0.143 | 1.13 | 0.86 | LOW_SHARPE, LOW_FITNESS, IS_LADDER |
| H2 | `hump 0.001` | `QPYNbnjg` | −0.52 | −0.14 | 0.0338 | — | −0.37 | −0.28 | 4 项（冻结） |
| H3 | `hump 0.002` | `rKdNObz3` | −0.47 | −0.12 | 0.0285 | — | −0.39 | −0.21 | 4 项（冻结） |
| **C1** | **无壳 @ decay 8** | **`RRAlbazb`** | **2.62** | **1.04** | **0.6221** | 0.158 | **2.53** | **2.11** | **无（0 项）** |
| 基准 | 无壳 @ decay 5 | `1YjlxYWk` | 2.84 | 1.04 | 0.7628 | 0.135 | 2.72 | 2.37 | HIGH_TURNOVER |

**四条结论（含一条跨数据集可复用律）**

1. **`ts_target_tvr_*` 在本族会"过度执行"**：目标 0.66 实测落在 **0.3924**（比目标低 41%），目标 0.58 → 0.3417。
   论坛 25 票帖警告的「目标设得离裸换手太近 ⇒ 优化器在边界硬压」方向被验证，但表现更糟：
   它不是"压不动"，而是**一路压穿**，代价 S 2.84 → 2.08（−27%）、F 1.04 → 0.85（跌破 1.0）。
   ⇒ **target_tvr 只适合"从高换手降到低换手一个量级"的场景，不适合本族只差 6pp 的微调**。
2. **`hump` 的可用区间比预想还窄一个数量级**：0.0005（≈1.5 个 rank 档位）就已经把 TO 砍 58%、
   S 砍 45%；0.001 起直接冻结（TO 0.0338）。⇒ 本族的日收益**就藏在 <0.0005 的逐日档位变动里**，
   任何"只交易大变化"的限速器都在切信号本体。这正是论坛 23 票帖说的「某些族的换手 = 信号本体，
   任何降换手机制都与信号单调共变」——**本族已确认属该形态**。
3. **唯一便宜的杠杆是"浅 decay"**：decay 5 → 8 拿到 TO −18%（0.7628 → 0.6221，余量 7.8pp）、
   S −8%（2.84 → 2.62）、**F 不动（1.04 → 1.04）**、2Y 2.72 → 2.53、SUB 2.37 → 2.11，**RA 0 失败**。
   但它是**窄台**：decay 20 已实测把 S 打到 0.82（§9.1 结论 4），中间档（10/12）未经实测，不要外推。
4. **可复用律（建议进 `docs/experience/02_signal_patterns.md`）**：
   「日频 rank 信号的换手通常是信号本体；先试 **decimal 级浅 decay（+3 档）**，
   `hump` 的起点必须按 1/N 估（TOP3000 ⇒ 1e-4 量级），
   `ts_target_tvr_*` 只在需要**跨量级**降换手时用」。

**波 3 收批时的临时裁决**：`RRAlbazb` = 交付候选（RA 17 项 0 失败；`self=0.5314` < 0.7 <!-- from config.self_corr_max --> **通过**；prod 待平台出数）。
预登记条件「RA 全过 ⇒ 立即 prod 双闸」已执行：prod 端点首次连查 441s 空体（`status=pending`，
**当时不判死**，按纪律隔时重查）；self 已过。

### 10.4 prod 裁决（2026-10-23 14:10，**判死**）

| 项 | 实测 |
|---|---|
| prod_correlation | **0.9369** |
| `[0.7,0.8)` 直方图 | **n = 1855** |
| `[0.8,0.9)` | n = 261 |
| `[0.9,1.0]` | n = 14 |
| 生产池总样本 | 2,580,606 |
| self_correlation | 0.5314（< 0.7，通过） |

**裁决：`USA-FHP-RESIDUAL-REVERSAL-PROD-SAT` —— 按 D0-P 判死，本数据集停止主数据集挖掘。**

归因（三条，第 3 条为跨数据集可复用律）：

1. **IS 全绿也挡不住 prod**：RA 17 项 0 失败、S 2.62 / F 1.04 / 2Y 2.53 / SUB 2.11 / TO 0.6221，
   生产池里仍有 1855 颗在 `[0.7,0.8)`、14 颗在 `[0.9,1.0]`。**这是"机制已被定价干净"的形态，
   不是"这次没调到好壳"的形态**（decay 5→8 已经把 TO 压了 18pp、S 只掉 8%，壳层已无余量）。
2. **"机构持仓面板当条件变量"这条机制本身拥挤**：波 1 的 A11 结论是「面板的价值是当条件变量、不是当信号本体」，
   而"用收益对机构换手率做长窗回归取残差并反向"恰恰是学术上最标准的做法 ⇒ 拥挤度必然高。
   **冷门数据集（aC 低）不等于冷门机制**（与 risk60 的 `lending_fee_bid_rate` aC=168 却 prod 0.9917 同构）。
3. **可复用律（建议进 `docs/experience/02_signal_patterns.md`）**：
   「USA 未点亮塔的产能瓶颈是 **prod 墙**，不是 IS 墙。家族在拿到第一个 `S ≥ 2.0` 的臂时就该
   **先探 prod**（哪怕 F 还差 0.1、TO 还超 6pp），再决定是否投资换手/形状修复。
   反例代价：本族 IS 侧花了 3 波 27 臂（含 2 波纯壳层调参），prod 一票否决。」

**对交付计数的影响**：严格口径仍为 **5 / 10**，本族 0 交付。
institutions 塔仍 0 颗 ACTIVE、未被消耗（塔位仍可选，但**本数据集停投**）。

**未封存说明**：`dead_end` 写入走 `seal_dead_end` 的论坛取证闸（prod 墙属"非论坛可解"场景，
需 `require_forum_recon=False` 或可靠 `no_result` 取证），按纪律不由 Agent 自行放行；
本轮先落画像与波次台账，封存动作待取证/人工确认后补。

## 11. 归档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-fund-holdings-panel-field-profile-20261023.md`
- 表达式：`tracking/USA/runs/usa_fhp_w1_exprs.txt`（11 臂）
- 波 2b：`usa_fhp_w2b_mkt.txt` / `_stat.txt` / `_saf.txt` / `_ram.txt` + `usa_fhp_w2b_spec.json`
- 波 3：`usa_fhp_w3_stat.txt`（6 臂）/ `usa_fhp_w3_d8.txt`（1 臂）+ `usa_fhp_w3_spec.json`
- 派发件：`tracking/USA/runs/usa_fhp_w1_batch_a.txt` / `usa_fhp_w1_batch_b.txt` / `usa_fhp_w1_spec.json`
- 同塔对照与选集依据：`_usa-fundamental-universe-scan-20261023.md`、`_usa-us-equity-news-field-profile-20261023.md` §8.6
- 交付总表：`output_report/USA_regular_alpha_delivery_20261021.md`
