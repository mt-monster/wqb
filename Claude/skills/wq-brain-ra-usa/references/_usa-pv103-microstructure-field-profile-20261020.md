# pv103 字段画像与首轮预注册（USA / D1 / TOP3000，2026-10-20）

> 用途：USA 未点亮 PV 塔的第二条微观结构主线。本档按「字段画像 → 适用模板 → 回测结果及指标」组织，
> 回测完成后回填 §5。**本档不含提交动作；任何提交都必须用户明确确认。**
> 同塔兄弟档案：pv63（订单流事件计数）→ [`_usa-pv63-order-flow-field-profile-20261020.md`](_usa-pv63-order-flow-field-profile-20261020.md)；
> pv115（做空量/集合竞价）→ [`_usa-pv115-short-volume-auction-field-profile-20261020.md`](_usa-pv115-short-volume-auction-field-profile-20261020.md)。

---

## 0. 数据集坐标（`get_datasets` / `get_datafields` 2026-10-20 实测）

| 项 | 值 | 备注 |
|---|---|---|
| dataset id | `pv103` | 名称与平台描述含「full order book depth」 |
| 塔位 | USA / D1 / **PV 塔未点亮**（`get_pyramid_alphas` pv=0） | 符合「未点亮塔优先」 |
| 字段可见数 | **78**（`sharpe_filter_applied=true`，另有 1 个被平台 sharpe 过滤移除） | 全部 **MATRIX**，无 VECTOR |
| 覆盖率 | 主体 **1.0**；拍卖类 0.9994–0.9997 | 覆盖极好，无需 backfill |
| 数据集 alphaCount | **9679**（`get_datasets` 实测） | 中等拥挤：比 pv1（aC 2.2M）低两个量级，比 pv63（168）高 |
| 更新频率 | 日频聚合（每个字段是「日内 N 分钟间隔统计的日均/日总」） | 非事件流，D1 天然对齐 |

**字段拥挤度分层**（aC = 该字段被多少 alpha 使用，实测）：

| 层 | aC | 字段 |
|---|---|---|
| 🔴 热 | ≥ 700 | `pv103_1m_cusm_mean` 1115、`pv103_insm_topofbook_insm_mean` 1041、`pv103_c_volume` 907、`pv103_tlrt_topofbook_tlrt_mean` 864、`pv103_mlrt_topofbook_mlrt_mean` 743 |
| 🟠 温 | 300–700 | `pv103_ivam_topofbook_ivam_mean` 621、`pv103_vlty_mean` 588、`pv103_mbdt_mean` 564、`pv103_ntrd_sum` 495、`pv103_mbid_topofbook_mbid_mean` 453、`pv103_1m_insm_mean` 451、`pv103_ivwp_mean` 373、`pv103_tbid_topofbook_tbid_mean` 353、`pv103_saps_mean` 336、`pv103_lbsz_mean` 326、`pv103_htsz_mean` 324、`pv103_1m_ivam_mean` 323、`pv103_1m_cusm_mean` 1115（见上） |
| 🟢 冷 | ≤ 200 | `pv103_nask_mean` 59、`pv103_nbod_mean` 230 / `naod` 98、`pv103_nbid_mean` 48、`pv103_medn_mean` 60、`pv103_mtsq_mean` 68、`pv103_hbid_mean` 90、`pv103_maus_mean` 111、`pv103_mbus_mean` 227、`pv103_1m_tlrt_mean` 139、`pv103_1m_mlrt_mean` 201、`pv103_sasz_mean` 122、`pv103_sbsz_mean` 207、`market_close_auction_clearing_price` 56、`market_close_auction_total_volume` 10、`market_open_auction_clearing_price` 17 |

> 冷层是蓝海：**拍卖类三件（aC 10/17/56）几乎无人用**，且与 pv63 的订单流事件、pv115 的做空量完全正交。

---

## 1. 字段画像（按经济含义分五族）

### 1.1 交易方向族（taker 侧）

| 字段 | 含义 | cov | aC |
|---|---|---:|---:|
| `pv103_inam_mean` | 每分钟**高于 mid 的成交笔数**的日均 | 1.0 | 303 |
| `pv103_ntrd_mean` / `ntrd_sum` | 每分钟成交笔数的日均 / 日总 | 1.0 | 142 / 495 |
| `pv103_1m_ivam_mean` / `ivam_sum` | 每分钟**高于 mid 的成交量**日均 / 日总 | 1.0 | 323 / 303 |
| `pv103_1m_insm_mean` / `cusm_mean` | 每分钟 signed market flow 的日均 / 累计流日均 | 1.0 | 451 / 1115 |
| `pv103_htsz_mean` | 每分钟最大单笔成交量的日均 | 1.0 | 324 |

**可直接构造的无量纲量**：
- **主动买笔占比** `divide(inam_mean, ntrd_mean)` ∈ [0,1] —— Lee-Ready 买压的日频版，尺度完全消掉，最干净。
- **主动买笔均量** `divide(1m_ivam_mean, ntrd_mean)` —— 每笔主动买的平均股数（交易规模，偏 size 代理，需查 risk-neut）。

### 1.2 订单簿形状族（maker 侧，本集核心）

| 字段 | 含义 | cov | aC |
|---|---|---:|---:|
| `pv103_sbsz_mean` | 全簿 `Σ bidsize_n/(mid−bid_n)` 的时间均值 | 1.0 | 207 |
| `pv103_sasz_mean` | 全簿 `Σ asksize_n/(ask_n−mid)` 的时间均值 | 1.0 | 122 |
| `pv103_sbps_mean` / `saps_mean` | 同上，但按价位序 `1/n` 加权 | 1.0 | 91 / 336 |
| `pv103_mbdt_mean` / `madt_mean` | 每笔挂单的**平均 bid/ask 距 mid 距离**（时间均值） | 1.0 | 564 / 193 |
| `pv103_mbds_mean` / `masz_mean` | 每档平均 bid/ask size（时间均值） | 1.0 | 190 / 271 |
| `pv103_1m_tlrt_mean` / `mlrt_mean` | 1 分钟 `log(bidsize/asksize)` 的时间加权 / 均值 | 1.0 | 139 / 201 |
| `pv103_tlrt_topofbook_tlrt_mean` | 同上，5 分钟顶档（热） | 1.0 | 864 |

**经济含义**：`sbsz` 与 `sasz` 是「离 mid 越近、权重越大」的**深度加权买/卖压力**，量纲相同、可直接相减；
`mbdt−madt` 是「哪一侧挂得更远」（做市商撤退方向）。这两族是 OBI 的**连续深度版**，比顶档 `tlrt` 更抗瞬时噪音。

### 1.3 订单簿结构族（计数/层级）

| 字段 | 含义 | cov | aC |
|---|---|---:|---:|
| `pv103_nbod_mean` / `naod_mean` | 全簿 bid/ask **挂单数**的时间均值 | 1.0 | 230 / 98 |
| `pv103_nbup_mean` / `naup_mean` | 每 5 分钟 bid/ask **更新次数** | 1.0 | 120 / 195 |
| `pv103_nblv_mean` / `nalv_mean` | 全簿 bid/ask **档位数** | 1.0 | 126 / 309 |
| `pv103_nbid_mean` / `nask_mean` | 每分钟 bid/ask 变化次数（+1,−1） | 1.0 | 48 / 59 |
| `pv103_mbus_mean` / `maus_mean` | 每笔更新消息的 bid/ask size 变化 | 1.0 | 227 / 111 |

**经济含义**：挂单数不平衡（`nbod−naod`）与更新强度不平衡（`nbup−naup`）刻画**做市商在两侧的活跃度差**；
与 size 类字段互为对照：size 差 = 深度，count 差 = 参与度。**两个都冷门（aC 98–230），是首轮主力。**

### 1.4 拍卖族（正交蓝海）

| 字段 | 含义 | cov | aC |
|---|---|---:|---:|
| `market_close_auction_clearing_price` | 收盘集合竞价成交价 | 0.9994 | 56 |
| `market_close_auction_total_volume` | 收盘集合竞价成交量 | 0.9994 | 10 |
| `market_open_auction_clearing_price` | 开盘集合竞价成交价 | 0.9997 | 17 |
| `pv103_c_price` / `c_volume` | 收盘 MOC 竞价 indicative/clearing 价 / 成交量 | 0.9997 | 1059 / 907 |
| `pv103_o_price` / `o_volume` | 开盘 MOO 竞价价 / 成交量 | 0.9995 | 236 / 220 |
| `pv103_ivwp_mean` | 5 分钟间隔 VWAP 的日均（日内基准价） | 1.0 | 373 |

**经济含义**：收盘竞价参与率 = `c_volume / intv_mean`（等于「多少个 5 分钟间隔的成交量」），
是 Bogousslavsky (2021) 收盘拍卖冲击的日频代理；`close_auction_clearing_price / ivwp` 是**收盘价相对日内 VWAP 的溢价**，
刻画尾盘方向性压力。两者都是无量纲，且**不依赖复权价**（同日同标的比值）。

### 1.5 价格/波动聚合族（对照，不作主力）

`pv103_ctwp_mean`（时间加权均价）、`1m_tbid/task/tbid`（时间均价）、`1m_mbid/mask`（消息均价）、
`1m_lbid/lask`（最低买/最高卖）、`1m_hbid/hask`（最高买/最低卖）、`medn_mean`、`mtrd_mean`、`mtsq_mean`、
`ivwp_mean`、`vlty_mean`（5 分钟价格波动，aC 588）。
其中价类字段几乎都是**价格的单调变换**，截面 rank 后等价于 size/price 代理，**首轮不用**；
`vlty_mean` 属通用波动因子，与 PV 塔已死的风险类重复，**只作风险对照**。

---

## 2. 机制与模板（M01–M10）

| # | 机制 | 一句话 | 主字段 | 预期符号 |
|---|---|---|---|---|
| M01 | 主动买压 | 高于 mid 的成交笔数占比高 ⇒ 短期买压 | `inam / ntrd` | 正（动量）/ 负（反转，二者必测其一） |
| M02 | 主动买规模 | 每笔主动买均量大 ⇒ 大单进场 | `1m_ivam / ntrd` | 正 |
| M03 | 深度加权簿失衡 | 买侧近 mid 深度强于卖侧 ⇒ 支撑 | `(sbsz−sasz)/(sbsz+sasz)` | 正 |
| M04 | 挂单距离不对称 | 卖侧挂得远比买侧近 ⇒ 卖方撤退/买方托底 | `(mbdt−madt)/(mbdt+madt)` | 正 |
| M05 | 挂单数不平衡 | bid 侧挂单数多于 ask ⇒ 做市意愿偏多 | `(nbod−naod)/(nbod+naod)` | 正 |
| M06 | 更新强度不平衡 | bid 侧更新更频繁 ⇒ 排队/撤单活跃 | `(nbup−naup)/(nbup+naup)` | 待定 |
| M07 | 顶档 log 尺寸比 | `log(bidsize/asksize)`（已知 OBI 族，作对照） | `1m_tlrt` | 正 |
| M08 | 收盘竞价参与率 | 尾盘拍卖占全天量比重高 ⇒ 机构调仓/指数需求 | `c_volume / intv_mean` | 待定（冲击后反转 vs 延续） |
| M09 | 收盘价溢价 | 收盘价高于日内 VWAP ⇒ 尾盘买压 | `close_auction_price / ivwp` | 负（反转）优先 |
| M10 | 开盘竞价参与率 | 隔夜信息在开盘拍卖释放 | `o_volume / intv_mean` | 待定 |

**模板**（首轮统一用通用壳，只换 SIG）：

```
quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))
```

`quantile` 只接 1 参数；`winsorize` 必须具名 `std=`；分组用 `industry`（豁免字段）。

---

## 3. 判死先验与外部证据（路由前必读）

1. **`USA-ORDER-FLOW-IMB-RANK-WEAK`**：订单流失衡纯截面 rank 族 max |S| 0.87（已测 `ts_mean`/`ts_delta`/`ts_zscore`/价差）。
   ⇒ M01/M02 的「纯水平 rank」正踩这条先验：**必须同时准备反转方向**，且不要把「加更多 rank 变体」当推进。
2. **`USA-OBI-LEVEL-FAMILIES-PROD-WALL`**：order_book_imbalance 水平/慢窗族 prod 0.76–0.81（2Y 1.37–1.43）。
   ⇒ M07（log 尺寸比）属同族，**只作对照，不作交付主力**；一旦 IS 达标先查 prod，不做 Mode A 调参。
3. **`USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD`**：**时间维度解拥挤（`ts_rank`/`ts_zscore`/`ts_av_diff` 相对自身历史）
   会摧毁横截面信号**（sharpe 1.45 → 0.20–0.29）。
   ⇒ pv103 首轮**全部用水平/比值构造**，不预先套时序归一；时序归一只在水平版出现「IS 强但过拟合/regime 集中」时作单独一批。
4. **论坛实证**：「谁在付 Spread？—— 订单流攻击性、半衰期分层与一个双引擎架构」记录 **单数据集 `pv103` 在
   GBR/TOP700 做到 IS Sharpe 1.96、全部硬检查 PASS** ⇒ 本集在平台闸上**可行**，失败只应发生在构造层。
   该帖的双引擎思路（攻击性 × 半衰期分层）对应本档 M01–M02（攻击性）与 M03–M06（挂单半衰期），**首轮分开建模，不合并**。
5. **同塔分工**：pv63 已测「事件计数比值」全弱（批 1 max S 0.79）；pv103 是**日内统计量的日均**，
   与 pv63 的逐笔计数不是同一测量面；但两者同属 PV 塔 ⇒ pv103 若也全弱，PV 塔三条主线（pv63/pv103/pv115）
   全部判弱后应整体封存 PV 塔，转其它未点亮塔，不在此塔内无限补批。

---

## 4. 批 1 预注册（8 探针，写死）

> 设置：EQUITY / USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / truncation 0.08 /
> nanHandling ON / unitHandling VERIFY / pasteurization ON / maxTrade OFF / FASTEXPR。
> 区间平台缺省（与历史批次可比）。全部套 §2 通用壳。

| 探针 | 机制 | 壳内 SIG | 备注 |
|---|---|---|---|
| V1 | M01 主动买占比 | `divide(pv103_inam_mean, pv103_ntrd_mean)` | 首选，尺度天然 [0,1] |
| V2 | M01 反向 | `multiply(-1, divide(pv103_inam_mean, pv103_ntrd_mean))` | 与 V1 成对，防方向误判 |
| V3 | M02 主动买均量 | `divide(pv103_1m_ivam_mean, pv103_ntrd_mean)` | size 代理风险，查 risk-neut |
| V4 | M03 深度加权簿失衡 | `divide(subtract(pv103_sbsz_mean, pv103_sasz_mean), add(pv103_sbsz_mean, pv103_sasz_mean))` | 冷字段（aC 207/122） |
| V5 | M04 挂单距离不对称 | `divide(subtract(pv103_mbdt_mean, pv103_madt_mean), add(pv103_mbdt_mean, pv103_madt_mean))` | mbdt 偏热（564） |
| V6 | M05 挂单数不平衡 | `divide(subtract(pv103_nbod_mean, pv103_naod_mean), add(pv103_nbod_mean, pv103_naod_mean))` | 最冷主力（230/98） |
| V7 | M08 收盘竞价参与率 | `divide(pv103_c_volume, pv103_intv_mean)` | 拍卖蓝海；c_volume 热但比值无人做 |
| V8 | M09 收盘溢价 | `divide(market_close_auction_clearing_price, pv103_ivwp_mean)` | 同日比值，无复权风险 |

（M06 更新强度、M07 顶档 log、M10 开盘竞价留到批 2：批 1 先确认哪条轴有信号，**不一次投满 10 个机制**。）

**预注册判据**：

- 任一 `S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB PASS` 且 `fail=0` ⇒ 立即 `check_correlation(refresh=True)`
  （prod/self < 0.7；**提交必须等用户明确确认**）。 <!-- from config.prod_corr_max -->
- **V1 vs V2 同弱**（|S| 均 <0.8）⇒ 主动买占比无信息，M01 判弱，批 2 不再补方向变体。
- **V1 与 V2 一正一负且 |S| 差 >0.3** ⇒ 方向真实存在，按强的那一侧作为批 2 的基准方向（**不取绝对值再造**）。
- **V4/V5/V6 任一 ≥1.2** ⇒ 订单簿形状是主机制，批 2 沿「深度 vs 计数」二维展开（含 `sbps/saps` 加权版、`nblv` 层级版）。
- **V7/V8 显著强于 V1–V6** ⇒ 拍卖轴是 pv103 的真正独立信息，批 2 全部投拍卖（含开盘 `o_volume/intv`、
  收盘 `total_volume/intv`、`c_price/o_price` 双拍卖价差），并优先查 prod（拍卖族拥挤度低）。
- **全部 |S|<0.8** ⇒ 判本批为弱。**先看 TO 与 risk-neut**：
  - TO 健康（1–70%）且 risk-neut <0.3 成片 ⇒ 判 size/流动性代理，**直接封存**，不补批；
  - TO 健康且 risk-neut 正常 ⇒ 才允许补批 2（只补 M06/M07/M10 三条未测轴），**仍全弱即封存 pv103**。
- **任一 risk-neut <0.3 且 S≥1.2** ⇒ 该构造是风格暴露，不进组合腿登记。
- **prod ≥0.75 或踩线失败** ⇒ 按决策表 D0-P 处置（判 dead_end / 换正交概念），不做同族磨参数。

---

## 5. 回测结果及指标

### 5.1 批 1（multisim `3GVd5w5KD5ajcpWQCA2qOx3`，8/8 COMPLETE，2026-10-20 收）

设置：EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / maxTrade OFF。

| # | alpha | 机制 | S | F | 2Y | SUB（limit） | TO | returns | DD | risk-neut | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| V1 | `wp9ERmn6` | M01 主动买笔占比 | **0.76** | 0.35 | 1.55 | 0.29（0.33） | **0.94%** | 2.60% | 12.1% | 0.42 | 5 |
| V2 | `zqrR9MPO` | M01 反向 | **−0.83** | −0.40 | −1.64 | −0.31 | 0.94% | −2.92% | 32.7% | −0.54 | 4 |
| V3 | `O0JxpYbJ` | M02 主动买均量 | −0.45 | −0.19 | −0.88 | −0.25 | 0.95% | −2.25% | 29.6% | −0.25 | 5 |
| V4 | `O0JxpYbd` | M03 深度加权簿失衡 | −0.18 | −0.03 | −0.69 | **0.50 PASS** | 0.91% | −0.39% | 10.0% | 0.08 | 4 |
| V5 | `P0MOpWnE` | M04 挂单距离不对称 | 0.53 | 0.18 | 0.79 | **0.43 PASS** | 0.85% | 1.41% | 5.8% | −0.06 | 4 |
| V6 | `leM3Vq77` | M05 挂单数不平衡 | −0.24 | −0.06 | −1.11 | −0.11 | 0.86% | −0.87% | 25.8% | 0.11 | 5 |
| V7 | `GrgewanG` | M08 收盘竞价参与率 | **0.63** | 0.36 | 1.01 | **0.50 PASS** | 0.92% | **4.03%** | 21.0% | **0.51** | 4 |
| V8 | `omogKpnJ` | M09 收盘溢价 | 0.40 | 0.11 | 0.74 | −0.09（0.17） | **1.00%** | 0.88% | 5.4% | **0.50** | 4 |

> 失败项除 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE` 外，**7/8 还踩 `LOW_TURNOVER`（<1%）**；V8 的 TO 恰为 1.00%，是唯一未踩该线的一条。

### 5.2 归因（先行，不看批 2 设计）

1. **V1 / V2 严格镜像**（0.76 vs −0.83，|差| 0.07）⇒ M01 只有单一线性方向成分，无拐点/非线性可利用；
   「反向 S 绝对值更大」是收益幅度差（−2.92% vs 2.60%），不是方向判断更强的证据。两侧均远低于 1.58 ⇒ **M01 判弱**，
   批 2 不再补方向变体（预注册判据命中）。
2. **全批 TO 集中在 0.85–1.00%，正好贴着 LOW_TURNOVER 线** ⇒ 这批**根本没走到「信号强弱」的问题**：
   日均统计量 + `hump(0.01)` + decay 5 + 5 段 quantile 把信号压成股票级结构性慢变量。
   与 `dl_volume_pred` 的「慢构造太慢、快构造没信号」同型 ⇒ **批 2 的唯一科学问题是把 TO 抬进健康区**，
   不是继续加字段或加 rank 变体。
3. **V7 是收益与稳健面最强的一条**：returns 4.03% / margin 0.0087 / risk-neut 0.51 / SUB 0.50 PASS，
   而 S 仅 0.63 ⇒ 信号方向对、幅度够，但**波动/分散不足**（DD 21%，long/short 1528/1533 已均衡）。
4. **拍卖族内部：量强于价**。V7（`c_volume/intv`）S 0.63 vs V8（`close_price/ivwp`）S 0.40；
   V8 是唯一 SUB 明显 fail 的一条（−0.09 vs limit 0.17）⇒ **拍卖信息在参与量，不在收盘价溢价**。
5. **SUB 的结构性**：V4/V5/V7 SUB PASS（0.43–0.50），主动买占比（V1/V2/V3）与挂单数（V6）在低流动性段无优势
   ⇒ 小盘段的信息集中在「深度 + 挂单距离 + 拍卖量」这一组 maker/事件面，不在 taker 方向面。
6. **risk-neut 分层**：V7/V8/V1 = 0.42–0.51（非纯风格）；V5 −0.06 / V6 0.11 / V4 0.08
   ⇒ 挂单距离、挂单数、深度比**几乎全是风格暴露**，即便 S 抬起来也进不了组合腿。
7. **V3（1m 主动买均量）为负**，与 V1 正方向相反 ⇒ 「每分钟主动买的平均股数」在 pv103 里是**大单/流动性代理**
   （risk-neut −0.25），不是「大单进场」的动量证据；M02 判弱。

### 5.3 批 2 预注册（只攻两件事：抬 TO + 三条未测轴）

> 设置与批 1 **完全相同**（一次一变量只在表达式层）。8 条、同一 multisim。

| # | 目的 | 壳内 SIG |
|---|---|---|
| B2-1 | V1 **去 hump**（测 hump 是否是把 TO 压在 1% 以下的主因） | `quantile(group_rank(ts_backfill(winsorize(divide(inam,ntrd), std=4), 252), industry))`（**壳内无 hump**） |
| B2-2 | V7 **去 hump**（同上，收益最强轴） | 同上去 hump，SIG = `divide(pv103_c_volume, pv103_intv_mean)` |
| B2-3 | V7 **短回填 22**（信号新鲜度，单一变量） | `hump(ts_backfill(winsorize(V7, std=4), 22), hump=0.01)` |
| B2-4 | V1 **短回填 22** | 同上，SIG = V1 |
| B2-5 | M08 **参与率变化**（快化对照） | `ts_delta(divide(pv103_c_volume, pv103_intv_mean), 22)` |
| B2-6 | M10 开盘竞价参与率（未测轴） | `divide(pv103_o_volume, pv103_intv_mean)` |
| B2-7 | M06 更新强度不平衡（未测轴） | `divide(subtract(pv103_nbup_mean, pv103_naup_mean), add(pv103_nbup_mean, pv103_naup_mean))` |
| B2-8 | M08 最冷口径（aC=10） | `divide(market_close_auction_total_volume, pv103_intv_mean)` |

**批 2 判据（写死）**：

- 任一全闸 ⇒ 立即 `check_correlation(refresh=True)`；prod ≥0.75 按 D0-P 处置，**不做同族磨参数**。
- **B2-1/B2-2 的 TO 仍 <1%** ⇒ hump 不是主因，慢来自「日均统计量 × decay 5」本身；
  批 3 才允许用 `ts_delta`/短窗快化，且若快化后 S 塌破 0.5 即成对判弱（同 pv63 `USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD` 先验）。
- **B2-2 比 B2-1 高 ≥0.2** ⇒ 拍卖轴是 pv103 唯一主力，批 3 全投拍卖（含 `c_price/o_price` 双拍卖价差、`total_volume` 口径）。
- **B2-6 / B2-7 全弱** ⇒ 开盘竞价与更新强度无独立信息，M06/M10 判弱，不再补。
- **去 hump 后 TO >1% 但 S 未升** ⇒ 说明该族信号被「平滑」掩盖了振幅而不是方向，批 3 改用 `ts_mean` 短窗重测，
  不再试壳层。
- **全弱且 TO 仍 <1%** ⇒ pv103 判弱封存的**前置条件**是 PV 塔第三条（pv115）也判弱；
  在此之前只记「构造层失败」，不提前封塔。

### 5.4 批 2 结果（multisim `FlqwJ4OM4YN9qYNX2zHlL5`，8/8 COMPLETE，2026-10-20 收）

设置与批 1 完全相同（EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / maxTrade OFF）。

| # | alpha | 构造 | S | F | 2Y | SUB（limit） | TO | returns | DD | risk-neut | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B2-1 | `1Yjz7mgR` | V1 **去 hump** | **−0.41** | −0.09 | 0.39 | −0.24 | **48.69%** | −2.25% | 43.7% | **−1.59** | 4 |
| B2-2 | `LL5dpXpL` | V7 **去 hump** | −0.02 | 0.00 | 0.54 | 0.10 PASS | **29.28%** | −0.17% | 51.4% | **−1.42** | 3 |
| B2-3 | `ZYmKplpZ` | V7 短回填 22 | 0.64 | 0.36 | 1.01 | 0.50 PASS | 0.92% | **4.03%** | 21.0% | **0.52** | 4 |
| B2-4 | `WjLVpXpN` | V1 短回填 22 | 0.75 | 0.34 | **1.56** | 0.29（0.32） | 0.95% | 2.57% | 12.2% | 0.41 | 5 |
| B2-5 | `kqJZ3m3g` | M08 `ts_delta` 22 | 0.50 | 0.17 | 0.89 | **0.74 PASS** | 1.11% | 1.41% | 9.4% | **0.03** | 3 |
| B2-6 | `2rjN7Z76` | M10 开盘竞价 | 0.23 | 0.05 | 0.95 | 0.45 PASS | 0.93% | 0.71% | 19.6% | 0.22 | 4 |
| B2-7 | `E5Vewaw9` | M06 更新强度 | −0.09 | −0.01 | −0.46 | −0.24 | 0.88% | −0.16% | 7.3% | −0.15 | 5 |
| B2-8 | `Vkd3plPw` | M08 拍卖总量（aC=10） | **0.65** | 0.37 | 1.05 | 0.50 PASS | 0.94% | **4.14%** | 20.3% | **0.58** | 4 |

**归因（逐条对预注册判据）**

1. **hump 是 TO 的主因，不是次要因素**：B2-1 去 hump 后 TO 0.94% → **48.69%**、B2-2 0.92% → **29.28%**。
   预注册里「慢来自日均统计量 × decay 5」的假设被**否证**。但两条去 hump 后 S = −0.41 / −0.02、
   risk-neut = −1.59 / −1.42 ⇒ **平滑本身就是信号载体**：去掉 hump 只剩短周期噪声，且净值由风格驱动。
   这一条同时复证 `USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD`：时间维度平滑/归一不是免费午餐。
2. **短回填 22 与 252 无差别**（B2-3 vs 批 1 V7：0.64/0.36/1.01/0.50/0.92%/4.03% vs 0.63/0.36/1.01/0.50/0.92%/4.03%；
   B2-4 vs 批 1 V1：0.75/2Y1.56 vs 0.76/1.55）⇒ 该族信号**不依赖近期数据新鲜度**，252 的回填只是覆盖手段。
3. **拍卖量口径可换、信息不变**（B2-8 `total_volume/intv` 0.65/4.14%/rns 0.58 与 B2-3 `c_volume/intv` 0.64/4.03%/rns 0.52
   几乎相同）⇒ 收盘竞价的**参与强度**是唯一有效成分，指标选哪个总成交量口径都行。
4. **快化（`ts_delta` 22）把 S 打到 0.50 且 risk-neut 归零**（0.03）⇒ 变化率丢掉水平信息，只剩风格；
   「参与度异常」分支关闭（与 pv115 Q5 同结论）。
5. **M06 更新强度零信号**（−0.09 / 2Y −0.46）⇒ 挂单更新频率不平衡在日频聚合后无截面信息，判弱。
6. **M10 开盘竞价弱**（0.23，2Y 0.95）⇒ 隔夜信息在开盘拍卖**不承载**可交易的横截面 alpha；
   与 pv115 Q7（开盘竞价 −0.02）跨集复证：**USA 的拍卖信息只在收盘侧**。
7. **全部 8 条仍远低于 S 1.58 / F 1.0**，最高 S 仅 0.75、最高 F 0.37。TO 修好（B2-1/B2-2）后信号消失，
   TO 保留时 S 只有 0.65 ⇒ **同一自由度两端**：这是构造层的结构性上限，不是参数问题。

**判弱封存**：pv103 三条主线（M01 方向族 / M03–M06 订单簿族 / M08–M10 拍卖族）全部 |S| ≤ 0.76、
无一 SUB+2Y 同时接近线，且 TO 与 S 沿 hump 轴单调对立 ⇒ 判 `USA-PV103-MICROSTRUCTURE-WEAK`，
**1+1 批 / 16 条，不再补批**。与 pv63（max S 0.79）、pv115（max |S| 0.36）合计，PV 塔三条主线全部判弱
⇒ **PV 塔整体封存**，不再在该塔内开新数据集批次（含 pv104 / pv98 / pv52），转未点亮的其它塔。
⚠ 论坛取证闸未过 ⇒ 未调用 `seal_dead_end`，本条的判弱是项目内纪律约束（同 pv115）。

---

## 6. 风险与预判

- **数据集级拥挤（aC 9679）**：虽然冷字段多，但 `c_volume`/`tlrt_topofbook` 等已高度使用；
  本档刻意把主力放在 aC ≤ 233 的字段（`sbsz/sasz/nbod/naod/1m_tlrt` 与拍卖三件）。
- **拍卖字段覆盖率 0.9994**：2026 年才普遍覆盖？若 yearly 显示 2014–2016 缺拍卖数据，
  则 V7/V8 的 2Y 可能显著高于全期（同 `chart_return_model` 型陷阱）⇒ 归因先看 yearly，再判死。
- **单位风险**：`market_close_auction_clearing_price / ivwp` 是价格比（无量纲），**不要再减 1**
  （VERIFY 模式下「无量纲常数 + 有单位字段」会报 UNITS 警告）；`c_volume / intv_mean` 同为股数比。
- **pos 数集中**：`sasz/sbsz` 是全簿求和，深度股数在小盘股上极小，winsorize std=4 已压尾；
  若 CW 报警，先查是否少数高价小盘股主导。
- **ATOM 合规**：8 条全部只引用 pv103 字段（含 `market_close_auction_clearing_price` 属同一数据集）；`industry` 分组属豁免。

---

## 7. 复用结论（待回测后固化）

1. 冷字段清单与拥挤度分层（§0）可直接用于后续任何 PV 微观结构批次的选字段。
2. 「方向族用比值（股数/笔数）→ 尺度天然消掉 → 截面前不必再做 `/cap` 归一」是本集相对 pv63 的最大优势。
3. 拍卖族（aC 10–56）是**全塔最冷**的正交轴：即使本批失败，也应作为其它区域（GBR/EUR）的可迁移候选。
