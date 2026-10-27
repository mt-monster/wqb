# USA · intraday_pv_feats 字段画像（2026-10-23）

> 用途：S1 字段梳理与画像（region=USA, delay=1, universe=TOP3000）。数据源 = 平台 `get_datafields(dataset_id=389)`（582 字段全量）+ 本地 `fields` 表（coverage / alpha_count / user_count）。
> 本件是**族级画像**，不是逐字段清单；逐字段数值在 `fields` 表（`dataset_id=389`）。
> 建档原因：USA 已交付 5/10（全为 analyst 塔）。所有已测量 prod 的非 analyst 族 ≥0.74（见交付日志附录 AY），
> 无现成 prod 可用池；pv 塔 USA 点亮数 = 0、乘数 1.1，且本集 79% 字段 `alphaCount = 0` ⇒ 换到本集有书面理由。

## 1. 数据集身份

| 项 | 值 |
|---|---|
| 数据集 | `intraday_pv_feats`（id=389, category=PV） |
| 字段数 | **582**，字段类型 **MATRIX × 582**（无 VECTOR/EVENT ⇒ 不需要 `vec_*`） |
| 覆盖 | 499 个 ≥0.99；29 个 0.95–0.99；17 个 0.8–0.95；35 个 0.6–0.8；2 个 <0.6 |
| 拥挤度 | **462/582（79.4%）alphaCount=0**；101 个 1–3；19 个 4–10；**最大 aC=10** |
| 用户数 | 与此同量级（绝大多数 userCount ≤ 3） |
| 频率 | 日频更新；每行是**前一交易日盘中**的统计量（intraday intervals 聚合），D1 可用 |
| 语义 | 盘中价格/成交量/买卖盘/执行质量的**当日快照统计**，不含跨日基本面信息 |

## 2. 字段族划分（按名字与语义聚类，n=582）

| 族 | n | aC=0 | 典型字段 | 语义与机制 |
|---|---|---|---|---|
| aggregate（极值/均值聚合） | 198 | 170 | `mean_high_price_return_30m_pre_close_2`、`max_bid_vwap_ratio_daily` | 区间收益/价格比值的日均或极值。**大部分是"日内某时段收益"**，直接承载动量/反转 |
| corr（跨序列相关） | 107 | 78 | `corr_last_trade_price_with_volume`、`corr_volume_with_bid_price_last_half`、`corr_vwap_with_slippage` | 价量同步性 = 知情交易/流动性提供强度；每字段是有界 [-1,1] 的日内相关 |
| momentum（日内动量） | 95 | 71 | `momentum_vwap_daily`、`momentum2_vwap_daily`、`momentum_bid_to_ask_price_ratio_last_half` | 一阶/二阶日内趋势（VWAP、价差、深度各自的高阶矩） |
| vwap/twap（成交均价） | 66 | 57 | `avg_vwap_to_last_price_ratio`、`mean_twap_vwap_ratio_daily`、`vwap_last_quarter` | 成交均价与收盘/首笔/时间均价的偏离 = 当日买压/卖压与临时冲击 |
| skew/kurtosis（分布形状） | 28 | 22 | `skew_vwap_to_last_price_ratio`、`kurtosis_vwap_interval` | 日内路径的尾部结构；尖峰=少数区间主导成交 |
| depth（买卖盘深度） | 24 | 19 | `avg_bid_ask_size_to_volume_ratio`、`mean_bid_ask_size_ratio_daily` | 盘口深度/成交量与买卖盘失衡（order-flow imbalance） |
| other | 24 | 15 | — | 命名不成族的杂项（modulo、price clock 等） |
| slippage（执行滑点） | 17 | **17** | `slippage_last_interval`、`corr_vwap_with_slippage` | 成交相对报价的滑点 = 有效价差/冲击成本 |
| interval（分区间原始量） | 16 | 9 | `last_trade_price_first_interval`、`trade_volume_last_interval` | 首/末区间原始价量，可构造日内收益与量钟偏斜 |
| spread（买卖价差） | 7 | 4 | `avg_bid_to_ask_price_ratio`、`skew_bid_to_ask_price_ratio` | 有效价差水平/分布 = 非流动性 |

## 3. 分布与可用性要点

- **三种量纲**：① 比值类（`*_ratio*`，无量纲，中心≈1，横截面离散小）；② 相关系数类（`corr_*`，有界 ±1）；③ 价格/数量类（`*_price*`、`*_volume*`，USD 或股数，**必须先做比值或时序归一**，否则 z-score 后仍带规模）。
- **覆盖率陷阱**：按"last quarter volume clock"切分的字段覆盖仅 **0.715–0.800**（`vwap_last_quarter` 0.7997、`momentum2_vwap_last_quarter_volumeclock` 0.7154、`std_vwap_last_quarter` 0.7154）；`vwap_first_half_volume` 0.733。用它们必须配 `ts_backfill` 或接受 20–28% 的空仓。
- **单位**：平台 `unitHandling=VERIFY`。常数与有单位字段混算会触发 UNITS 警告 ⇒ 统一走"比值/相关/组内 z-score"三步，避免裸价格进 `divide` 时的单位歧义。
- **换手**：本集是**日频快照**，日内统计量每天全换 ⇒ 裸 `rank(x)` 的换手常在 0.3–0.7。实测可用配方是 `ts_decay_linear(x, 5)`（TO 0.30–0.36）+ 平台 `decay 5–10`；`hump` / `ts_target_tvr_*` 作二级降换手。
- **可用的经济机制**（与"慢速基本面"正交）：
  1. **非流动性溢价 / 流动性风险**：价差水平与价差变化（Amihud 2002；Pastor-Stambaugh 2003 流动性风险）。
  2. **订单流失衡**：买卖盘规模比（Chordia-Roll-Subrahmanyam 2002）——收盘前失衡对次日有预测力。
  3. **临时冲击反转**：收盘价相对 VWAP 的偏离（日内买压造成的临时冲击会在次日回吐）。
  4. **日内动量**：开盘 30–60 分钟收益对后市的延续（Gao-Han-Li-Zhou 2018 的横截面版本）。
  5. **知情交易 / 价量同步性**：`corr_volume_with_*_price` 高的股票，成交量集中在价格高位 = 派发。
  6. **执行成本 / 滑点**：`corr_vwap_with_slippage`、`mean_twap_vwap_ratio_daily` 作为有效价差的代理。

## 4. 已被消耗的空间（本集历史 35 条回测，勿重复）

| 批次 | 机制 | 代表表达式 | S / F / TO / 2Y | prod |
|---|---|---|---|---|
| 波 60 | 日内价量相关、峰度 argmax | `winsorize(ts_corr(...))`、`quantile(-ts_arg_max(kurtosis...))` | −0.88 … −0.02 | 未测 |
| probe_intraday2_20260919 | `corr_last_trade_price_with_volume` / `corr_vwap_with_volume` 的 `-ts_mean(..,5)` | `rank(multiply(-1, ts_mean(corr_last_trade_price_with_volume, 5)))` | 1.56 / 0.61 / 0.339 / 1.60 | 未测 |
| probe_ipv_corr_slow_20260921b | 同上 + `ts_decay_linear` 慢化 + 分组 rank | `subtract(0.5, group_rank(ts_decay_linear(corr_last_trade_price_with_volume, 10), industry))` | 1.50 / 0.91 / 0.144 / 2.06 | 未测 |
| probe_preclose_20260920 | **收盘前 30m 最高价收益**反转 | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 5), country)` | 1.66 / **1.05** / 0.334 / 2.00 | **0.7429** |
| probe_preclose_20260920 | **同族 industry 版**（≠ 上行的 corr 族） | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 5), industry)` = `levR9Vq7` | **1.84 / 0.95 / 0.3304 / 1.70** | **未测**（2026-10-23 更正：旧行误抄了 corr 族 `9qjAmw1o` 的 1.94/0.86/0.8693） |
| probe_ipv_corr_slow_20260921b | `corr_last_trade_price` 的 industry 版 | `-group_zscore(ts_decay_linear(corr_last_trade_price_with_volume, 5), industry)` = `9qjAmw1o` | 1.94 / 0.86 / 0.3551 / 1.71 | **0.8693** |
| probe_ipv_gated_20260921 | 上述 × 成交量门控 | `trade_when(...)` | 2.35 / 0.78 / 0.698 | 未测（TO 超 0.4） |

**结论**：历史上只碰了 `corr_last_trade_price_with_volume` 与 `mean_*_price_return_30m_pre_close_2` 两条腿。价差、深度、VWAP 偏离、量钟偏斜、滑点**全部未被回测**（aC=0 的字段占 79%）。已测的两条腿共同点是"收盘前 30 分钟价格路径"，prod 0.74–0.87 ⇒ 换机制，不换参数。

## 5. 波 90 设计（首次系统性机制铺开，24 条）

| 批 | 设置 | 机制（字段族） | 条数 |
|---|---|---|---|
| `usa_ipv_w90a` | SUBINDUSTRY / decay 5 | 价差水平与变化、深度、深度失衡、VWAP 偏离、VWAP 时段收益 | 12 |
| `usa_ipv_w90b` | MARKET / decay 10 | 价量同步性（bid/ask 腿）、滑点、TWAP-VWAP、VWAP 日内收益、量钟偏斜、`quantile` 壳 | 12 |

产物：`tracking/USA/runs/usa_ipv_w90a.txt` / `usa_ipv_w90b.txt` / `usa_ipv_w90_spec.json`。
预检：`validate_expressions` 24/24 通过、19 个字段平台侧确认。

## 5.1 波 90 结果与归因（2026-10-23 收批，24 条全 COMPLETE）

实际按 multisim ≤10 条上限拆成 **3 批 × 8 条**（`4fngdjck…` / `1wREHQby…` / `1eYntJ1i…`）；原 12/12 两批被平台 400 拒绝（`A maximum of 10 simulations`），而派发器仍打印 `ALL SUBMITTED` ⇒ **批大小必须 ≤10，且不能以退出码判断成功**。

| 批 | 设置 | 最好结果 | 结论 |
|---|---|---|---|
| a | SUBINDUSTRY / decay 5 | `9qE8dXdr` 0.58 / 0.25 / 0.27；`6XAZolZE` 0.65 / 0.33 / 0.06 | 价差水平、深度、深度失衡**整体无效**（16 条里 11 条负） |
| b | SUBINDUSTRY / decay 5 | `E5VN8vPr` 1.28 / 0.48 / 0.40（= 已测 `mean_vwap_return_30m_pre_close_2` 的镜像） | 其余 7 条 −1.6 … 0.48 |
| c | MARKET / decay 10 | `JjPoW3x2` **1.85 / 0.58 / 0.6345**；`2rj9XGwb` 1.78 / 0.55 / 0.6336；`j2eoPV8E` 1.32 / 0.84 / 0.33 | 价量同向性（volume×bid/ask price）**Sharpe 最强但换手 0.63**，F 结构性不足 |

**三条归因（不是"信号不存在"，是"结构不匹配"）**

1. **符号是可推断的、不是新信息**：本集全部构造都是组内去均值（`group_zscore` / `subtract(0.5, group_rank)`），对整式取负 ⇒ 持仓与 PnL 精确取负、Sharpe 精确反号。故波 90 里 −1.61 / −1.14 / −1.13 这类**不是废结果**，它们的镜像就是 +1.1 … +1.6；但镜像**只在 |S| ≥ 1.58 时才值得重跑**（`momentum_vwap_daily` −1.61 是唯一达标者，TO 0.4058 差 0.006 过线）。
2. **换手是这批机制的真墙，不是 Sharpe**：`corr_volume_with_bid/ask_price` S 1.85/1.78 但 TO 0.63，`F = S·√(RET/TO)` ⇒ 要 F≥1 需把 TO 砍到 ~0.21 或把 S 再抬 70%。这类"同向性水平量"天生高频，直接放弃比调参便宜。
3. **`ts_decay_linear` 窗长存在 F 的最优点**：`F` 的分母在 TO 处取 `max(TO, 0.125)`。本族 TO 从 0.355（窗 5）降到 0.144（窗 10）时 S 从 1.94 掉到 1.50、F 从 0.86 升到 0.91；再往 22 走（`2rwv5MjP`）S 只剩 1.27、TO 0.0997 已跌破地板 ⇒ **继续降换手反而压 F**。甜区在 **TO ≈ 0.13–0.16**，对应 `ts_decay_linear(...,10)`。

## 5.2 波 91 设计（承接归因，16 条 / 2 批）

| 批 | 设置 | 假设 | 条数 |
|---|---|---|---|
| `usa_ipv_w91a` | SUBINDUSTRY / decay 5 | **`mean_*_price_return_30m_pre_close_2` 族是可提交性最高的一支**：`levR9Vq7`（industry，decay 5）S 1.84 / F **0.95** / TO 0.3304 / 2Y 1.70 / SUB 1.14，**只差 F 0.05**；用 `quantile` 壳压尾 + 换轴（sector / subindustry）+ 同族换字段（vwap / last_trade / post_open / low）把 F 推过 1.0 | 8 |
| `usa_ipv_w91b` | SUBINDUSTRY / decay 5 | `corr_last_trade_price` 族 S 1.50 / F 0.91 / TO 0.144 **只差 S 0.08**，按实测增益库用 `quantile`（+0.10）与 `signed_power` 指数 0.3（+0.03）抬 S；另测 `divide(vwap_last_interval, vwap_first_interval)`（1.32/0.84/0.33）与 `momentum_vwap_daily` 镜像（|S| 1.61，TO 需从 0.4058 压到 <0.40） | 8 |

> ⚠ `corr_last_trade_price` 族 prod 已实测 0.8693（industry）/ 0.8739（country）⇒ 即便 w91b 过闸，它也**只作为 F/S 壳的技术验证**，不指望可提交；真正押注在 w91a 的 `mean_high_price_return` 支（country 版 prod 0.7429、industry 版**未测**）。

论坛取证：2026-10-23 用 `tools/forum_recon.py` 就该问题检索 4 轮，24 条候选**读帖全部失败**（平台 429）⇒ 记 `USA/forum_recon_error_dedada46b4`，**属工具故障、不作无解证据**，待平台恢复后重跑同一问题。

## 6. 存档索引

- 本件：`Claude/skills/wq-brain-ra-usa/references/_usa-intraday-pv-feats-field-profile-20261023.md`
- 逐字段数值：`data/wqb.db::fields where dataset_id=389`
- 历史回测：`data/wqb.db::backtest_results where region='USA' and dataset='intraday_pv_feats'`
- 波 90 任务：`tracking/USA/runs/usa_ipv_w90_spec.json`
