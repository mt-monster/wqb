
---

## §5 USA 情绪族判死 + GLB 家族容量实证 + USA 塔位缺口（2026-11-06 06:10–06:25）

### 5.1 GLB `mean_last_trade_price_return_30m_pre_close_2` 族：互相关实证「全部超线」

`compute_mutual_correlation` 对 8 条跑满 **28 对**（C(8,2)=28），结果 **28/28 全部 > 0.7**，最大对 `akbWK6V5 × xA3mrqrw = 0.9858`。
`max_mutually_below_subset_size = 1`。

⇒ 这条族**实证净产出 = 1 颗**，不存在「窗口 10 能当第二颗」的可能（`LLNlZKMa` 与其余 7 条同样 >0.7）。
选取：`vRrJZMoA`（prod 0.4770，余量最大）。

### 5.2 USA `assetutilization_sentiment_polarity` 五写族：self 全过 → prod 全灭

| alpha | S | F | TO | 2Y | self | prod 实测 |
|---|---:|---:|---:|---:|---:|---:|
| `6Xd7A5V7` | 1.77 | 1.01 | 4.80% | 2.54 | **0.342** | **0.7672** ❌ 浅钉 |
| `P0od2pOp` | 1.61 | 1.18 | 5.32% | 2.06 | **0.675** | **0.8192** ❌ 深钉 |
| `pwdAPALb` | 1.75 | 1.16 | 3.06% | 2.29 | 0.520 | 未测（族已判死） |
| `E56XvX90` | 1.75 | 1.13 | 3.33% | 2.39 | 0.546 | 未测 |
| `akKqLq56` | 1.72 | 1.09 | 3.23% | 2.42 | 0.460 | 未测 |

**互相关矩阵**（关键）：

| | pwdAPALb | E56XvX90 | akKqLq56 | 6Xd7A5V7 |
|---|---:|---:|---:|---:|
| **P0od2pOp** | 0.8341 | 0.8117 | 0.7346 | **0.3540** |
| **pwdAPALb** | — | 0.9732 | 0.9556 | 0.5114 |
| **E56XvX90** | | — | 0.9272 | 0.4339 |
| **akKqLq56** | | | — | 0.5483 |

`max_mutually_below_subset = [P0od2pOp, 6Xd7A5V7]`（size 2，互相关仅 0.354）。
⇒ 互相关层面这个族**确实能出 2 颗**，但**两颗 prod 实测分别是 0.8192 / 0.7672，全部撞墙**。

### ★ 判决：USA `assetutilization_sentiment_polarity` 族判死（五个写法全部弃用）

**这是本战役第一次出现「self 全过 + 互相关算出 2 颗容量 + 两颗 prod 全灭」的三段式全灭**，
说明「族容量」和「可提交性」是两道完全独立的闸：互相关只告诉你**族内能不能共存**，
**完全不能告诉你这个族是否已被别人的池子占用**。
⇒ 流程修正：**族级去重（互相关）必须在 prod 实测之后再做才有意义**——先测 1–2 颗代表件的 prod，
确认这个族活着，再花额度算互相关矩阵。反过来先算互相关是浪费（本族 5 条互相关白算）。

### 5.3 ★ USA 塔位表（`get_pyramid_alphas` 实读，D1）

| 区域 | 已点亮（≥3） | 近亮 | 零塔数 |
|---|---|---|---:|
| **USA** | model(4) / analyst(6) | other(2) / risk(2) / institutions(1) / earnings(1) | **10**（pv, fundamental, socialmedia, news, option, macro, insiders, sentiment, shortinterest, imbalance） |
| **GLB** | model(3) / other(4) | pv(2) / earnings(1) / risk(1) / institutions(1) | 7 |
| **EUR** | model(3) / fundamental(3) / analyst(10) / imbalance(3) | pv(2) / news(1) / insiders(1) / other(2) / risk(2) / sentiment(2) | 4 |
| **ASI** | **无** | other(2) | **15（几乎全零）** |
| **KOR** | fundamental(3) / model(3) / shortinterest(4) | analyst(2) / other(1) / pv(2) | 9 |
| **HKG** | **无** | pv(1) | **14** |
| **IND** | news(4) / other(4) / pv(11) / analyst(3) / model(3) / fundamental(3) / risk(3) | insiders(1) / macro(2) / sentiment(1) / earnings(2) / institutions(1) | 3（imbalance, option, shortinterest） |
| **GBR** | model(5) / news(3) / analyst(3) / fundamental(3) | other(1) / pv(2) | 10 |
| **DEU** | 无 | institutions(1) / model(1) / other(2) / analyst(2) / fundamental(1) / sentiment(1) / shortinterest(2) | 9 |

### ★ 结论：**USA 是当前最大的塔位洼地**

USA 只有 model / analyst 两座塔点亮，**10 个零塔**（含 PV），而我们此前从未开采过任何 USA 数据集——
只做过 READY 存量池筛查。USA 门槛实测 ≤1.61（`P0od2pOp` S 1.61 无 fail），与 EUR/GBR 的 1.58 同档，
⇒ **USA 是「低门槛 × 10 个零塔 × 294 个数据集池」的最优矿区**。

### 5.4 USA 未点亮塔数据集排名（本地覆盖缓存，零配额）

`tracking/mining/field_coverage_USA_d1_TOP3000.json`：294 个数据集，其中 **120 个属未点亮塔**。

| category | dataset | cov | 字段数 | aC | 说明 |
|---|---|---:|---:|---:|---|
| **pv** | `pattern_scores` | 0.994 | 504 | 40 | 处女地，形态打分 |
| **pv** | `continuation_score` | 0.994 | 560 | 49 | 处女地，延续性打分 |
| **pv** | `intraday_pv_feats` | 0.975 | 582 | 121 | 日内量价特征 |
| **pv** | `chart_return_model` | 1.000 | 248 | 50 | 图形收益模型 |
| **fundamental** | `fundamental72` | 0.746 | 1852 | 2733 | 大集但拥挤 |
| **sentiment** | `news_transformer_scores` | 0.777 | 315 | 158 | Transformer 新闻打分 |
| **socialmedia** | `twitter_sentiment_l2` | 0.979 | 95 | 97 | 18 种情绪方法 × 15 种相关度过滤 |
| **option** | `order_flow_imb` | 0.809 | 120 | 113 | 期权订单流失衡（见 §6） |
| **news** | `event_return_model` | 0.999 | 59 | 81 | 事件收益模型 |

---

## §6 USA · `order_flow_imb`（OPTION 塔，零塔 → 出货即点亮）

### 6.1 数据集画像（`get_datafields` 实读，USA/TOP3000/D1）

**全部 MATRIX**（不需要 `vec_avg`），coverage 0.77–0.91。字段是 **参与者 × 方向 × 度量 × 变体** 的四维组合：

- **参与者**：`broker_dealer_*`（做市商/自营）、`customer_*`（客户/散户+机构）
- **方向**：`bullish_*`（买 call + 卖 put）、`bearish_*`（卖 call + 买 put）
- **度量**：`trade_count` / `vol` / `contracts` / `trade_imbalance` / `vol_imbalance`
- **变体**：无后缀（全量）/ `_ise`（ISE 交易所）/ `_noto`（不含开盘成交）/ `_otm`（仅虚值）

关键字段：`broker_dealer_trade_imbalance`（cov 0.9058 / aC 11）、`broker_dealer_vol_imbalance`（0.9058 / aC 21）、
`customer_trade_imbalance`、`customer_vol_imbalance`，以及 `_ise` / `_noto` / `_otm` 各自的镜像。

### 6.2 机制来源（★ 论文 + 论坛双证）

| 来源 | 内容 |
|---|---|
| **论文 Pan & Poteshman (2006)**, *The Information in Option Volume for Future Stock Prices*, **RFS 19(3): 871–908**（NBER WP 10925） | 核心结论：**只有非做市商（customer）的 put-call 成交量比对未来股价有预测力**；做市商（market maker）成交量比无预测力。信息含量来自知情交易者的期权建仓。**方向先验：客户看跌需求上升 → 未来收益下降** |
| 论坛《Machine Alpha 基础知识4：以期权数据为例》 | 期权类模板方法论：比较同一组内不同公司之间 call/put 的净差值 |
| 论坛《Quant101 ...Order Flow Imbalance（首选）》 | 明确点名本数据集：衡量机构/做市商/客户/专业客户的看涨 vs 看跌期权交易净差值 |
| 论坛《【Data】怎么用 imbalance》 | 确认 `option` 类的 `order_flow_imb` 是**期权资金流**，不是股票开盘板失衡（后者是 `imb1_imbalance`） |
| 论坛《时序标准化回归残差通用因子模板在 option 数据集的应用》 | `ts_regression` 剥离标的价格驱动，取期权侧异动残差 |

### 6.3 模板池（11 个结构互异，差异落在 骨架/方向/矩/参与者分解/非线性）

| # | 模板名 | 骨架 | 算子 | 经济机制 |
|---|---|---|---:|---|
| OFI1 | Customer 失衡水平（原版） | `-group_rank(ts_mean(customer_vol_imbalance,22), sector)` | 2 | Pan-Poteshman 核心：客户看跌净需求 → 负向 |
| OFI2 | 做市商 vs 客户分歧 | `group_rank(subtract(ts_mean(cust_vol_imb,22), ts_mean(bd_vol_imb,22)), sector)` | 5 | 知情(customer) − 非知情(做市商) = 纯净知情成分 |
| OFI3 | Put-Call 量比 | `-group_rank(ts_mean(divide(cust_bearish_vol, add(cust_bearish_vol,cust_bullish_vol)),22), sector)` | 6 | 论文原式的比率版 |
| OFI4 | 虚值看涨需求 | `group_rank(ts_zscore(cust_bullish_vol_otm,252), sector)` | 3 | Xing-Zhang-Zhao (2010)：OTM call 成交量预测力最强 |
| OFI5 | 笔数-金额背离 | `group_rank(subtract(ts_zscore(cust_trade_imbalance,252), ts_zscore(cust_vol_imbalance,252)), sector)` | 6 | 散户笔数多/单笔小 vs 机构单笔大 |
| OFI6 | 时序回归残差 | `group_rank(ts_regression(cust_vol_imb, close, 252, rettype=0), sector)` | 3 | 论坛残差模板：剥离股价驱动后的期权异动 |
| OFI7 | 失衡动量 | `group_rank(ts_delta(ts_mean(cust_vol_imb,22),22), sector)` | 4 | 客户情绪的边际变化 |
| OFI8 | 失衡分歧度 | `group_rank(reverse(ts_std_dev(cust_vol_imb,66)), sector)` | 4 | 客户内部分歧 → 不确定性折价 |
| OFI9 | 过期周效应 | `group_rank(ts_mean(cust_vol_imb,5), sector)` | 2 | 论坛《Option-Expiration Week Effect》 |
| OFI10 | 逆向失衡熵 | `reverse(ts_entropy(cust_vol_imb,144))` | 2 | 论坛《逆向失衡熵值挖掘》 |
| OFI11 | 覆盖度加权失衡 | `group_rank(multiply(ts_mean(cust_vol_imb,22), rank(ts_add(cust_bull_vol,cust_bear_vol))), sector)` | 7 | 期权活跃度高时信号更可信 |

### 6.4 已派发

批 `4k0srL6dP51l9dZAx90zHnB`（USA/TOP2000/D1/decay 0/STATISTICAL/trunc 0.08/nan ON/VERIFY/pasteurization ON/maxTrade OFF）：
- `-group_rank(ts_mean(customer_vol_imbalance, 22), sector)`（OFI1，2 算子）
- `group_rank(subtract(ts_mean(customer_vol_imbalance, 22), ts_mean(broker_dealer_vol_imbalance, 22)), sector)`（OFI2，5 算子）

`validate_expressions` 通过：`valid=true`、`unknown_fields=[]`。

### 6.5 ★★★★★ 第一批收批：**论文的方向先验被数据推翻**

批 `4k0srL6dP51l9dZAx90zHnB`，2/2 COMPLETE、0 error。

| alpha | 模板 | 表达式符号 | S | F | TO | 2Y | sub | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `LLM8qEbm` | OFI1 | **带负号** `-group_rank(ts_mean(cust_vol_imb,22), sector)` | **−0.93** | −0.27 | 21.28% | −0.67 | −0.41 | 3 |
| `QPvWqOrp` | OFI2 | 正号 `group_rank(cust_vol_imb − bd_vol_imb, sector)` | **+0.73** | 0.19 | 21.37% | 0.69 | 0.33 | 4 |

**读法**：OFI1 带负号得 −0.93 ⇒ **不带负号是 +0.93**。

⇒ **本数据集上，客户看涨失衡是正向预测收益的**——与 Pan & Poteshman (2006) 在美股期权上「客户看跌需求 → 负收益」的方向**相反**。

**为什么反着也要记录，而不是当成噪声**：
1. |S| 0.93 与 0.73 都是**正常量级的有向信号**，不是 0.1–0.3 的噪声（噪声档在本战役的标准是 |S|<0.3）。
2. TO 21.3% 落在**常规有效区（5–30%）**，不是刷新率噪声档（40%+），也不是慢变描述符档（<5%）。
3. 两条**独立构造**（单腿水平 / 双腿差值）给出**同向正号**（+0.93 与 +0.73）⇒ 不是单点偶然。

**可能的解释**：数据集的 `*_imbalance` 定义是「(bullish − bearish) / 总」还是「bearish / 总」未在字段描述中明确；
若实际是后者，则符号自然翻转。**结论按实测走，不按论文先验走。**

### 6.6 第二批（已派发 `axKJvfuU4LhbauOHZA5lav`）

- `group_rank(ts_mean(customer_vol_imbalance, 22), sector)`（OFI1 **翻号确认**，预期 ≈ +0.93）
- `group_rank(ts_zscore(customer_bullish_vol_otm, 252), sector)`（OFI4 虚值看涨需求，Xing-Zhang-Zhao 2010 的 OTM 版）

两者结构与字段变体都不同（全量失衡 vs 仅虚值看涨），设计上互相关应显著低于 0.7。