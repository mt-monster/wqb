# short_interest_pred · USA/D1/TOP3000 字段画像与机制库

> 数据集：`short_interest_pred`（Short Interest Forecast Signals — 次日卖空余额预测 / 实际-预测偏离）
> 区域/宇宙/Delay：USA / TOP3000 / D1 · 塔位：**SHORTINTEREST（1/3，未点亮）** · 倍率 ×1.1
> 平台规模：10 字段 · coverage 0.9987 · alphaCount 12–295（2026-03 上架）· pyramidMultiplier 1.1
> 建档：2026-11-22（wave `usa_sip_atom_20261122`）· 状态：**探测中**

---

## §0 数据集选择

| 候选 | 覆盖 | 字段 | 平台 aC | 判断 |
|---|---|---|---|---|
| **short_interest_pred** | **0.9987** | 10 | **12–295** | ✅ 选它：SHORTINTEREST 塔 1/3 未亮、覆盖接近满格、字段极冷（最热 295） |
| shortinterest24 | 0.2573 | 1 | 449 | 覆盖过低（1/4 宇宙）⇒ 横截面窄，先不投 |
| shortinterest29 | 0.8838 | 32 | 295 | 已测（68 臂 RA 全过 0，max|S| 0.79，`usa_dead_datasets.md`） |
| shortinterest3 | 1.0 | 31 | 5007 | 已测；借券费率族，`mean_loan_rate_main` prod 0.7767 墙 |
| shortinterest43 | 0.9994 | 32 | 1582 | 已测（同族 43 画像在 `references/_usa-shortinterest43-field-profile-20261115.md`） |
| us_short_sale | 1.0 | 4 | 375 | 已测（日频做空量=噪声，`usa_dead_datasets.md`） |

选它的三条理由：
1. **塔位空白**：USA/D1 SHORTINTEREST 只有 1 颗 ACTIVE（1/3），且存量 OS 池是借券费率族；
   本集是**预测/偏离**族，与存量 OS 池机制不同（self-corr 需实测，见 §2）。
2. **alphaCount 极低**：最热字段 295、多数 12–41 ⇒ 平台级蓝海，非拥挤族。
3. **信息含量先验**：卖空余额的「实际 vs 预测偏离」是学术上有独立定价力的异象
   （见 §0.4），不是简单水平量。

---

## §0.1 字段质量先验（按 `dateCreated` 全部为 2026-03-01，按 alphaCount 升序）

| 字段 | 类型 | 覆盖 | aC | uC | 描述要点 |
|---|---|---|---|---|---|
| `prior_short_interest_surprise_value` | MATRIX | 0.9987 | 12 | 10 | 上期实际−预测（美元） |
| `prior_short_interest_surprise_amount` | MATRIX | 0.9987 | 15 | 12 | 上期偏离绝对值（美元） |
| `short_interest_surprise_amount` | MATRIX | 0.9987 | 18 | 11 | 当期偏离绝对值（美元） |
| `prior_short_interest_predicted_value` | MATRIX | 0.9987 | 22 | 18 | 上期预测值（美元） |
| `short_interest_predicted_value` | MATRIX | 0.9987 | 24 | 17 | 次日预测卖空余额（美元） |
| `short_interest_surprise_value` | MATRIX | 0.9987 | 29 | 21 | 当期实际−预测（美元） |
| `prior_short_interest_surprise_ratio` | MATRIX | 0.9987 | 33 | 19 | 上期实际/预测比 |
| `prior_short_interest_predicted_change` | MATRIX | 0.9987 | 41 | 33 | 上期预测变化 |
| `short_interest_surprise_ratio` | MATRIX | 0.9987 | 76 | 50 | 当期实际/预测比 |
| `short_interest_predicted_change` | MATRIX | 0.9987 | **295** | 142 | 当期预测变化（最热） |

**头部轴判读**：最热的是 `short_interest_predicted_change`（295）——「预测变化」本身已被挖过一轮；
真正冷的是 **surprise（实际 − 预测）** 与 **prior_ 上期口径**（12–33）。
⇒ 经济轴 = **预期之外的卖空余额冲击（unexpected short interest）**，不是「预测水平」或「预测变化」。

---

## §0.2 字段分类（以 description 为准）

| 族 | 字段 | 语义 | 时间性 |
|---|---|---|---|
| **S1 意外/偏离（当期）** | `short_interest_surprise_value` / `short_interest_surprise_ratio` / `short_interest_surprise_amount` | 当期实际卖空余额 − 模型预测（美元 / 比值 / 绝对值） | 日频，t 日可得 |
| **S2 意外/偏离（上期）** | `prior_short_interest_surprise_value` / `prior_short_interest_surprise_ratio` / `prior_short_interest_surprise_amount` | 上期实际 − 预测 | 日频，t−1 |
| **S3 预测水平** | `short_interest_predicted_value` / `prior_short_interest_predicted_value` | 模型次日预测卖空余额（美元） | 日频 |
| **S4 预测变化** | `short_interest_predicted_change` / `prior_short_interest_predicted_change` | 预测卖空余额的变化（Δ） | 日频 |

---

## §0.3 机制假设与模板白名单（待实证裁决）

| 机制 | 经济逻辑 | 预期符号 | 首选模板 | 排除理由/前置 |
|---|---|---|---|---|
| **M1 卖空意外（unexpected SI）** | 实际卖空余额高于模型预测 ⇒ 知情做空者提前布局 ⇒ 未来负收益 | 负 | `-rank(short_interest_surprise_ratio)` / `-group_rank(ts_zscore(...), subindustry)` | 比值类字段有零/负分母；需 `winsorize` 或 `ts_backfill` |
| **M2 意外反转（surprise reversal）** | 上期偏离在当期被修正 ⇒ 均值回复 | 与 M1 相反 | `-rank(delta(short_interest_surprise_ratio))` | 需确认 prior 与 current 的时序对齐 |
| **M3 预测变化动量** | 预测卖空余额上升 ⇒ 做空压力累积 | 负 | `-rank(ts_mean(short_interest_predicted_change, 22))` | 该字段最热（aC 295），预期拥挤 |
| **M4 卖空回补（covering）** | 卖空余额快速下降 ⇒ 回补买盘 | 正 | `rank(-ts_delta(short_interest_predicted_value, 22))` | 水平美元量纲 ⇒ 必须 rank/scale |

**禁止**：两条独立信号腿相加（`mixed_signal_ban`）；第二数据集只能以条件/分组/残差入场；
本集为 ATOM 单集，全部模板只用本集 10 字段。

---

## §0.4 证据（论坛 + 论文）

- 论文闸（`tools/research/paper_search.py --diverse`）：**32 篇 / 29 作者 ≥ 5/3，PASS**。核心：
  - 《Surprise in Short Interest》2023, Journal of Financial Markets, DOI `10.1016/j.finmar.2023.100841`
  - 《Short Interest and Stock Returns》2004, NBER w10434, DOI `10.3386/w10434`
  - 《Days to Cover and Stock Returns》2015, NBER w21166, DOI `10.3386/w21166`
  - 《Short interest, stock returns and credit ratings》2019, JBF, DOI `10.1016/j.jbankfin.2019.105617`
- 论坛（`search_forum_posts_local`，短仓/卖空关键词 79 命中）：方法论锚点
  - 135 赞《From Data Exploration to Alpha Discovery: A Practical Approach to Single-Dataset Research》
    （post `44887744717335`）——单数据集、先画像后表达式、先裸 rank/zscore 再复杂化，与本 ATOM 流程同构。
  - 《Reading Momentum Crashes (2016): Audit the Short Leg Before Adding a Regime Filter》
    （post `44687266076823`）——空头腿需单独审计，不能只看组合净 PnL。

---

## §1 字段全表（分母 = 平台 10 字段，逐字段真实 id，无通配）

| # | 字段 id | 类型 | 覆盖 | aC | 族 |
|---|---|---|---|---|---|
| 1 | `short_interest_surprise_value` | MATRIX | 0.9987 | 29 | S1 |
| 2 | `short_interest_surprise_ratio` | MATRIX | 0.9987 | 76 | S1 |
| 3 | `short_interest_surprise_amount` | MATRIX | 0.9987 | 18 | S1 |
| 4 | `prior_short_interest_surprise_value` | MATRIX | 0.9987 | 12 | S2 |
| 5 | `prior_short_interest_surprise_ratio` | MATRIX | 0.9987 | 33 | S2 |
| 6 | `prior_short_interest_surprise_amount` | MATRIX | 0.9987 | 15 | S2 |
| 7 | `short_interest_predicted_value` | MATRIX | 0.9987 | 24 | S3 |
| 8 | `prior_short_interest_predicted_value` | MATRIX | 0.9987 | 22 | S3 |
| 9 | `short_interest_predicted_change` | MATRIX | 0.9987 | 295 | S4 |
| 10 | `prior_short_interest_predicted_change` | MATRIX | 0.9987 | 41 | S4 |

---

## §2 全字段实测读数（10/10，零抽样）

> 波次 `usa_sip_atom_20261122` · 设置：USA/TOP3000/D1，SUBINDUSTRY，decay 5，trunc 0.08，
> nanHandling ON，maxTrade OFF，pasteurization ON，unitHandling VERIFY。
> 探针 = 每字段一条裸 `rank(...)`（全字段覆盖）；读数待回填。

| 字段 | 探针表达式 | Sharpe | Fitness | Turnover | 备注 |
|---|---|---|---|---|---|
| `short_interest_surprise_value` | `rank(short_interest_surprise_value)` | 0.12 | 0.01 | 0.7881 | Grm9kX60；2Y 2.47（全期弱/近端强，regime 分歧） |
| `short_interest_surprise_ratio` | `rank(short_interest_surprise_ratio)` | -0.38 | -0.04 | 0.7880 | 3q0Jz13P；2Y 2.26，同上 |
| `short_interest_surprise_amount` | `rank(short_interest_surprise_amount)` | -0.41 | -0.05 | 0.7746 | d5avdYmj；无方向量，作分组/门控候选 |
| `prior_short_interest_surprise_value` | `rank(prior_short_interest_surprise_value)` | -0.46 | -0.07 | 0.7411 | VkNeOZYV |
| `prior_short_interest_surprise_ratio` | `rank(prior_short_interest_surprise_ratio)` | -0.84 | -0.16 | 0.7436 | omaZVRzJ；2Y 0.74 |
| `prior_short_interest_surprise_amount` | `rank(prior_short_interest_surprise_amount)` | -0.91 | -0.18 | 0.7311 | wpoWL3Jl；无方向量 |
| `short_interest_predicted_value` | `rank(short_interest_predicted_value)` | -0.07 | -0.01 | 0.0341 | N1P8ALjg；水平美元量，近零 |
| `prior_short_interest_predicted_value` | `rank(prior_short_interest_predicted_value)` | -0.03 | 0.00 | 0.0333 | O0WgoRbv；近零 |
| `short_interest_predicted_change` | `rank(short_interest_predicted_change)` | -1.49 | -0.44 | 0.6862 | rK78A9z1；2Y -2.50 / RN -2.24 ⇒ **反号后 S +1.49 / 2Y +2.50，本集最强内核** |
| `prior_short_interest_predicted_change` | `rank(prior_short_interest_predicted_change)` | 0.79 | 0.17 | 0.5454 | d5avdYlv；2Y -0.56（与当期反号，须分开建族） |

---

## §3 梯度层账本

### L1 内核 × 时间尺度（同集 ATOM；SUBINDUSTRY/decay5/trunc0.08/TOP3000）

基线 = `-rank(short_interest_predicted_change)`（全字段探针最强内核，反号后 S +1.49）。

| 变体 | alpha | S | F | TO | 2Y | ret/TO | 判读 |
|---|---|---|---|---|---|---|---|
| `-rank(pred_change)` | RRePrQGn | 1.49 | 0.44 | 0.6862 | 2.50 | 0.088 | 最强但 TO 68.6% / F 0.44 |
| `-rank(ts_mean(...,5))` | YPaYAKRM | 1.10 | 0.38 | 0.3400 | 2.14 | 0.120 | 平滑即掉 S |
| `-rank(ts_mean(...,22))` | j2aOgRqO | 0.57 | 0.25 | 0.1266 | 0.81 | 0.189 | S 崩 |
| `-rank(ts_mean(...,66))` | 9qlkRLzo | 0.30 | 0.11 | 0.0597 | 0.46 | 0.260 | S 崩 |
| `-ts_zscore(pred_change,252)` | P05K1dJp | 1.19 | 0.32 | 0.6874 | 3.49 | 0.074 | 2Y 最高但 F 更差 |
| `-ts_zscore(ts_mean(...,22),252)` | lea10bLA | 0.81 | 0.34 | 0.1611 | 1.68 | 0.181 | — |
| `-group_rank(ts_mean(...,22),subindustry)` | akaGOqr9 | 0.49 | 0.19 | 0.1306 | 0.53 | 0.145 | 分组伤 S |
| `-group_rank(ts_zscore(ts_mean(...,22),252),subindustry)` | RRePrnRn | 0.89 | 0.36 | 0.1529 | 1.29 | 0.161 | — |
| `-rank(ts_sum(...,22))` | LLK3RALn | 0.54 | 0.23 | 0.1261 | 0.73 | 0.178 | — |
| `-rank(ts_decay_linear(...,22))` | gJaL3EJe | 0.68 | 0.29 | 0.1553 | 1.31 | 0.180 | — |

**L1 结论**：内核速度极快，平滑把 S 与 ret 同步砍掉 —— 沿平滑路径 F 上限 ~0.30，**F 闸是结构性墙**。
下一层专攻「保信号降换手」：`trade_when` 持仓门控（-1）、`hump`、双窗 `add`、粗分组。

### L2 换手墙（trade_when / hump / 双窗 / 粗分组）

| 变体 | alpha | S | F | TO | 2Y | ret/TO | 判读 |
|---|---|---|---|---|---|---|---|
| `trade_when(abs(z)>1.0, -rank(pred_change), -1)` | QP06QKz5 | 1.36 | 0.47 | 0.2253 | 2.64 | 0.122 | 换手可压、F 仍 0.47 |
| `trade_when(abs(z)>1.5, ...)` | Jj8rdQze | 0.23 | 0.04 | 0.1364 | 1.26 | 0.033 | 门太窄信号消失 |
| `trade_when(abs(z)>2.0, ...)` | lea10KG5 | 0.24 | 0.05 | 0.0873 | 1.40 | 0.052 | 同上 |
| `hump(-rank(pred_change), 0.01)` | blaA9Ozm | -0.32 | -0.08 | 0.0055 | -0.05 | — | hump 把 rank 增量全滤掉（LOW_TURNOVER 5.5%） |
| `hump(-rank(pred_change), 0.05)` | mLaQX61p | -0.32 | -0.08 | 0.0055 | -0.05 | — | 同 0.01（rank 粒度下无差别） |
| `-rank(ts_rank(pred_change,22))` | xAv5nbWw | 1.44 | 0.37 | 0.7026 | 3.46 | 0.065 | 2Y 3.46 但 TO 70.3% |
| `-ts_rank(pred_change,5)` | gJaL3ZdM | 0.93 | 0.17 | 0.8543 | 2.35 | 0.035 | TO 85% |
| `add(fast, slow66)` | Jj8rdQ1e | 0.71 | 0.25 | 0.3000 | 1.32 | 0.125 | 双窗掉 S |
| `trade_when(rank(ts_mean(pred_value,252))>0.2, ...)` | wpoWebPv | 1.38 | 0.39 | 0.6457 | 2.66 | 0.079 | 规模门无效 |
| `-group_rank(ts_mean(pred_change,5), market)` | zqdeWbeK | 1.01 | 0.34 | 0.3363 | 1.94 | 0.110 | 粗分组掉 S |

**L2 结论**：`trade_when` 是唯一有效的保信号降换手武器，但 S-F 前沿仍为 **S 1.36 / F 0.47**；
F≥1.0 需 ret/TO ≥ 0.44（当前 0.122），差 3.6 倍 ⇒ 快信号在 F 公式下不可救。

### L3 慢速水平/变化 + 同集多字段组合（ATOM）

| 变体 | alpha | S | F | TO | 2Y | ret/TO | 判读 |
|---|---|---|---|---|---|---|---|
| `-rank(Δ252(value)/mean252)` | YPaYpGvl | 0.51 | 0.21 | 0.0714 | 0.28 | 0.31 | 慢但 S 弱 |
| `-rank(Δ66(value)/mean66)` | kqa932PO | 0.36 | 0.12 | 0.1118 | 0.41 | 0.118 | — |
| `-rank(value/mean252)` | j2aOZb6k | 0.55 | 0.24 | 0.0798 | 0.50 | 0.30 | — |
| `-rank(ts_zscore(value,252))` | qM7VAojK | 0.40 | 0.15 | 0.0876 | 0.38 | 0.19 | — |
| `-rank(Δ252(prior_value)/mean)` | omaZKMq5 | 0.54 | 0.23 | 0.0690 | 0.35 | 0.34 | — |
| `-rank(surprise_ratio − prior)` | 9qlkwLXK | -0.86 | -0.23 | 0.6846 | -1.14 | — | 反号且快 |
| `-rank(ts_mean(surprise_rev,22))` | LLK3pA71 | -0.12 | -0.03 | 0.1498 | 0.39 | -0.05 | — |
| `-rank(change×surprise_ratio)` | gJaL1Ejg | 0.02 | 0.00 | 0.5772 | 0.26 | — | 组合无效 |
| `-rank(change/(|value|+1))` | 58JYwol1 | 1.32 | 0.35 | 0.7133 | 2.73 | 0.072 | UNITS warning |
| `-rank(change − prior_change)` | wpoWRMYx | 1.45 | **0.55** | 0.6047 | 1.23 | 0.144 | F 最高但 2Y 1.23 挂 |

**L3 结论**：慢速水平族 S 0.36–0.55，组合族最高 F 0.55。
**三层 30 臂合并判读：S-F 前沿 = S1.49/F0.44（TO68.6%）或 S1.45/F0.55（TO60.5%，2Y1.23）**；
F≥1.0 需 ret/TO≥0.44，实测最高 0.34（且该臂 S 0.54）⇒ **F 闸结构不可达**。

---

## §4 判死/停投结论（PROVISIONAL）

- **结论**：`short_interest_pred` 的 **fast 机制（predicted_change / surprise）信号层不可交付**；
  slow 水平机制（|S|≤0.55）更弱。30 臂 / 3 层（全字段探针 10 + 内核 10 + 换手 10 + 慢速组合 10）。
- **未达数据集级判死要件**：D1 结构互异模板 ~12、D2 字段族 4/4 全测、D3 矩 4/4、D5 非线性 3 条，
  但 **D4 分组轴仅 2（subindustry/market）**、**D6 配置仅 1 套** ⇒ 按 §7.6 只能记 **PROVISIONAL**，
  **不得**引用为邻接数据集/族的先验，**不得**据此宣布 SHORTINTEREST 塔关闭。
- **停投理由（可逆）**：F 公式下 ret/TO 差 3.6 倍，继续调参只能改换手/S，改不了 F 的量纲。
- **重开条件**：若平台下调 F 线 / 允许 maxTrade 强制降换手 / 该字段族出现新的慢速衍生字段。



