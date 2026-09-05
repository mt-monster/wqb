**Dataset**: insider_trx_matrix
**Region**: EUR
**Delay**: 1

Note: insider_trx_matrix = 内部人交易矩阵（filings 事件数据，OTHER/insider，pyramid eur_d1_other 未点亮，EUR 零死路）。cov≈0.607（事件日外=0/NA，稀疏事件）；33 字段全部 users≤49（27 cold + 6 mid），理论 prod≈0。**预处理决策**：① count 字段点质量集中 0 → 必须 ts_sum 长窗聚合（22/66）或 trade_when 条件门控提升密度；② usd_* 为美元计值与市值相关 → 先 rank / group_rank 消规模再进组合；③ 稀疏事件 → trade_when(ts_sum(x,N)>0, signal, 0) 形态合法且可在无事件日输出 0 无伪信号；④ EUR 披露规则异于 US，方向一律实测。学术实证：insider buy 事件后存在正漂移（信息优势渐进吸收）；sell 信号弱（流动性/税务动机）**谨慎取反**。

**Concept**: 内部人购买漂移慢腿（insider drift, 初始信号）
- **Mechanism**: insider 高管/董事净买入后存在数月正漂移（经典 insider trading literature）：内部人信息优势通过交易揭示，市场渐进定价。top（高层级）交易信息含量最高，用 top 交易笔数的长窗累计作为漂移强度。
- **Fields**: `total_top_buy_transaction_count`
- **Implementation Example**: `rank(ts_sum({total_top_buy_transaction_count}, 66))`
- **Direction**: buy 事件后正漂移 → long 高累计买入股（方向实测）
- **Expected Exposure**: event_drift
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide（66d 聚合覆盖提升）
- **Why not crowded**: EUR 该数据集 0 alpha；mid 字段（users 10-49）仅在 EUR 有 6 个，非 MODEL 金字塔无 prod 墙。

**Concept**: 买卖净流（net purchase strength, 进阶信号）
- **Mechanism**: 内部人整体净买入（top buy 累计 - top sell 累计）比单边笔数更能滤除流动性动机噪音；net purchase 强度与后续漂移单调。
- **Fields**: `total_top_buy_transaction_count`, `total_top_sell_transaction_count`
- **Implementation Example**: `subtract(rank(ts_sum({total_top_buy_transaction_count}, 66)), rank(ts_sum({total_top_sell_transaction_count}, 66)))`
- **Direction**: 净买入 → long（方向实测）
- **Expected Exposure**: event_drift
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide
- **Why not crowded**: dual-field 非对称 shape op1(A)-op2(B)；sell 侧不取反保留流动性噪音抵消信息，与单边 buy 骨架异质。

**Concept**: 事件门控购买信号（trade_when 密度修正, 预处理决策落地）
- **Mechanism**: 稀疏事件下大量无事件日 = 0，rank 会把非事件股与事件股混淆；用近期是否有真实活动做条件门控（22d 窗内有 buy 事件才输出漂移信号，否则 0），把事件日特征与密度正交分离。
- **Fields**: `total_buy_transaction_count`, `total_top_buy_transaction_count`
- **Implementation Example**: `trade_when(ts_sum({total_buy_transaction_count}, 22) > 0, rank(ts_sum({total_top_buy_transaction_count}, 66)), 0)`
- **Direction**: 事件后漂移 → long（方向实测）
- **Expected Exposure**: event_conditional
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium
- **Why not crowded**: trade_when 条件骨架在 EUR 未点亮数据极少见；满足稀疏事件硬门要求（zero_inflated 必须 trade_when 或 ts_ 聚合）。

**Concept**: 内部人层级分歧（director vs executive, 冷门 usd 金额方向）
- **Mechanism**: director（董事圈层）与 top executive（高管圈层）交易信号方向背离时蕴含信息：内部层级对私有信息接近度不同，意见分歧后股价向信息优势方收敛。
- **Fields**: `usd_direct_signal_value_2`, `usd_top_direct_signal_value_2`
- **Implementation Example**: `subtract(rank(ts_sum(ts_backfill({usd_direct_signal_value_2}, 66), 66)), rank(ts_sum(ts_backfill({usd_top_direct_signal_value_2}, 66), 66)))`
- **Direction**: 层级分歧 → 向高信号圈层收敛（方向实测）
- **Expected Exposure**: behavioral_disagreement
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium（usd 家族 cold users 0-9, ts_backfill 提覆盖）
- **Why not crowded**: usd_direct 家族 27 个 cold 字段从未被 EUR 使用；金额信号先 rank 消市值规模再差分，满足预处理决策。

**Concept**: 大额交易金额漂移（usd top 信号慢窗, 冷门）
- **Mechanism**: 内部人交易的美元金额（top_primary 层）代表实际资本承诺：金额越大的买入隐含更强的信息确信；慢窗累计捕获大额 insider 押注的漂移。
- **Fields**: `usd_top_primary_signal_value`
- **Implementation Example**: `rank(ts_mean(ts_backfill({usd_top_primary_signal_value}, 22), 66))`
- **Direction**: 大额买入 → long（方向实测）
- **Expected Exposure**: event_drift
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium
- **Why not crowded**: users 0-9 冷门字段，金额信号方向与笔数信号正交（大额少次 vs 小额高频），六维收益来源分离。

**Concept**: 买入强度近期加速（ts_delta 事件动量）
- **Mechanism**: 内部人交易常成串发生（cluster），近期买入节奏加快（66d 累计的 5d 增量）预示后续披露窗口仍将有正面信息流入；事件动量捕捉漂移的时变强度。
- **Fields**: `total_top_buy_transaction_count`
- **Implementation Example**: `rank(ts_delta(ts_sum({total_top_buy_transaction_count}, 66), 5))`
- **Direction**: 加速买入 → long（方向实测）
- **Expected Exposure**: event_acceleration
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 与慢窗水平信号（C1）骨架不同（ts_delta 二阶形态），批内形成 窗口/骨架多样性；同字段多窗处理体现预处理差异。

**Concept**: 行业相对内部人强度（group_sum 行业正交, 契约算子）
- **Mechanism**: 内部人交易有强行业季节性与同步性（年报窗口/监管日历）；扣除行业平均买入强度后，行业内相对超配买入的股票才具截面区分度，同时压低行业因子暴露。
- **Fields**: `total_top_buy_transaction_count`
- **Implementation Example**: `subtract(rank(ts_sum({total_top_buy_transaction_count}, 66)), rank(group_sum(ts_sum({total_top_buy_transaction_count}, 66), industry)))`
- **Direction**: 行业相对买入 → long（方向实测）
- **Expected Exposure**: industry_relative
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide
- **Why not crowded**: group_sum 契约算子满足 explore_contract_EUR；行业相对形态与裸 rank 收益来源分离（跨 section 归因维度差异）。

**Concept**: 双窗漂移共识（22/66 双窗 mix）
- **Mechanism**: 短窗（22d）捕获近期披露潮，长窗（66d）捕获稳定持仓倾向；两窗共识的股票同时具备事件新鲜度与持续信息优势，权重结构参照 EUR win recipe 的 0.4/0.6 线性混合形状迁移（同数据集双字段窗组合，不跨 catalog）。
- **Fields**: `total_top_buy_transaction_count`, `total_buy_transaction_count`
- **Implementation Example**: `add(multiply(rank(ts_sum({total_top_buy_transaction_count}, 22)), 0.5), multiply(rank(ts_sum({total_buy_transaction_count}, 66)), 0.5))`
- **Direction**: 双窗买入共识 → long（方向实测）
- **Expected Exposure**: event_drift
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 线性 mix 形状在 OTHER 金字塔无历史占用；top vs 全量口径组合（层级配比）非套壳单字段。
