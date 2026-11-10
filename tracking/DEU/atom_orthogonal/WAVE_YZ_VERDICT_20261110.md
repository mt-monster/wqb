# DEU 第三席：波 Y / Z 判死台账（2026-11-10 上午末）

## 一、波 Y：insider 族（insider_matrix + insider_trx_matrix）—— 判死

**选族依据**：DEU D1 金字塔 `insiders = 0`（**塔未点亮**）；
`insider_matrix` / `insider_trx_matrix` 的 cov = 1.0 / 0.5344；
OS 池 Vk65zLzG（insiders/model 塔）已出货过一件 ⇒ 证明 insiders 信息面在 DEU 有定价力。

10 条（S -0.58 ~ +0.58，2Y -1.59 ~ +1.59），全部判死：

| 候选 | S | 2Y | longCount | 字段 |
|---|---:|---:|---:|---|
| ZYQO5WKd / wpQ0mJjl | 0.58 | 1.59 | 130 | directional_indicator_score（正/反） |
| wpQ0mJa6 | -0.58 | -1.59 | 260 | directional_indicator_score（反） |
| 9qxNvApe | 0.55 | 0.92 | 131 | eur_signal_value_2 |
| omExp9NJ | -0.45 | -1.32 | 262 | eur_signal_value_3（反） |
| VkxA9Y7V | -0.23 | -0.30 | 263 | eur_signal_value_4（反） |
| N1NYw57g | -0.39 | -0.32 | 261 | total_sell_transaction_count（反） |
| 2rA30nlw | -0.21 | -0.30 | 263 | eur_aggregated_value_2（反） |
| A1VoWOGw | 0.25 | 0.54 | 126 | eur_director_signal_value_2 |
| 58EPbqlN | -0.02 | 0.09 | 131 | total_buy_transaction_count |

### ★ 判据 MQ：成对出现的 lc 差异（130 vs 260）不是符号翻转，是**样本集分裂**

同一字段的正/反两版 longCount 呈 1:2 分布（130 vs 260）⇒ 不是「同一批股票的信号取反」，
而是**加负号改变了 NaN 传播路径**：`ts_backfill` 填的是缺失值，加负号后 `ts_delta` 的
有效起点不同，导致**进入截面排序的股票集合不同**（一半样本退出）。

⇒ **判读提醒**：看到正反成对、lc 恰好接近 1:2 时，**不能当作「方向反了，翻转即可」**
（那是判据 MG 的前提：同一批样本）。必须先核对 longCount 是否一致。

### 归因
德国上市公司内部人交易事件**极稀疏**（多数股票多数年份无内部人交易披露），
backfill 后的「变化加速度」主要反映**数据缺失模式**而非交易行为 ⇒ 无横截面定价力。
（与短兴趣族的差别：借券报价每日都有，内部人交易是事件驱动 ⇒ 两者在 DEU 命运完全不同。）

**外部文献对照**（本轮查得）：
- MDPI《Insider Trading Signals Across Industries》(2026)：内部人**买入比卖出更有信息量**
  （buy-sell asymmetry），银行股最强、科技股最弱 —— 逐行业差异大；
- 论坛《insider × institution 相对强弱的全景对比》(57 赞)、《Data 慎用 insiders：8-K 文本内部人成交》(31 赞)
  提示 insider 数据的信噪比问题；
- 论坛《Attention 稀缺性：insider_agg_matrix 内部人交易信号》(29 赞) —— 已有前人尝试该数据集。

## 二、波 Z：dl_riskfree_returns（厂商 ML 前瞻收益预测）—— 判死

10 条（S -0.37 ~ +0.37，2Y -0.99 ~ +0.93），全部判死，符号混乱 ⇒ 真噪声。

**字段**：cov = 1.0 的厂商模型输出 —— `quantile_label_*bucket_{5,20,60}day_ohlcv`（连续回归预测的
前瞻市场中性收益）、`probability_label*_*quantile_*day_ohlcv`（分位桶对数概率）。

**归因**：与已判死的 `global_seasonal_model`（449 字段 cov=0，模型置信桶）同源 ——
**厂商模型的输出在 DEU 截面无定价力**（既可能是模型在 DEU 上无泛化，也可能是生产池已覆盖）。

**判据 MR（跨区通用）**：
- 「模型输出型数据集」在 DEU 一律判死（global_seasonal_model 已判死，本波再次验证）；
- **cov=1.0 不能证明有信息量** —— cov 只说明字段有值，不说明值有预测力
  （news104 cov 0.963 全灭、dl_riskfree_returns cov 1.0 全灭）；
- 判据优先级：**先看信号强度（S），再看覆盖，最后才看 cov**。

## 三、DEU 机制族搜索的完整覆盖图（本轮终）

| 塔 | 状态 | 本轮结论 |
|---|---|---|
| ANALYST | 6 颗（已点亮） | ❌ 三腿族被 rKRx2Alj 整体锁死（族内 self 全 ≥0.70） |
| MODEL | 3 颗（已点亮） | ❌ 禁混集合内，不开波 |
| OTHER | 2 颗 | ❌ 禁混集合内 |
| FUNDAMENTAL | 1 颗 | ❌ fundamental6 封盘（信号集中 oiadpq + 该字段被生产池占据） |
| SHORTINTEREST | 2 颗 | ✅ **本轮唯一新机制成立**：借券需求加速度反转，8+ 颗四闸全过，族容量 1 席（E569ZE7L） |
| SENTIMENT | 1 颗 | ❌ attention 族强度-覆盖不可兼得（snt7 强但 2019 起 / snl27 弱） |
| INSIDERS | 0 颗 | ❌ 波 Y 全灭（内部人事件极稀疏，backfill 后信号反映缺失模式） |
| INSTITUTIONS | 1 颗 | ❌ institutions6 S ≤ 0.35（早前判死） |
| NEWS | 0 颗 | ❌ 波 N/U/V 三数据集交叉验证全灭（RavenPack 事件情绪无定价力） |
| RISK | 0 颗 | ❌ risk60 与 shortinterest3 同机制且更弱（判据 MF） |
| EARNINGS | 0 颗 | ❌ earningscall_sentiment cov=0（无供数） |
| MACRO | 0 颗 | ❌ macro27 cov=0（无供数） |
| OPTION | 0 颗 | ❌ option1 / option_chart_model cov=0 |
| SOCIALMEDIA | 0 颗 | ❌ socialmedia12 cov=0 / socialmedia39 cov 0.27 |
| IMBALANCE | 0 颗 | ❌ imbalance5 cov=0 / order_book_imbalance cov 0.21~0.23（太稀疏） |
| — | — | ❌ 内置价格字段（波 W）S ≤ 0.94；dl_riskfree_returns（波 Z）ML 预测全灭 |

⇒ **DEU 域内可交付上限 = 4 颗**（2 颗已 ACTIVE + 1YNMAA8M + E569ZE7L）。
要往第 5 颗走，**必须放开「不得换 region」过程约束**（goal 明文，需用户修改）。

## 四、本轮新增判据

| 编号 | 判据 | 要点 |
|---|---|---|
| MQ | 正反成对 + lc 接近 1:2 ⇒ 样本集分裂，非符号翻转 | 翻转前必须核对 longCount 是否一致；否则会把「缺失模式」误读成「方向反了」 |
| MR | cov=1.0 不证明有信息量 | news104 cov 0.963 全灭 / dl_riskfree_returns cov 1.0 全灭；判据优先级 S > 覆盖 > cov |
| MS | 模型输出型数据集在 DEU 一律判死 | global_seasonal_model + dl_riskfree_returns 双验证 |
| MT | 事件驱动 vs 日频数据在 DEU 命运不同 | 借券（每日）能出货；内部人交易（事件驱动）无定价力 |
