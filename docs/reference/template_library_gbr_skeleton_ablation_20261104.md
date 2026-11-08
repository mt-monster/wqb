# GBR 骨架消融规律 + 模板库（2026-11-04 W66–W76）

> 来源：W66（全灭）→ W67（单层消融）→ W68/W69（新集与 fitness）→ W70（双层骨架消融）→
> W71（shortinterest 冲塔）→ W72（analyst9 机制）→ W73（truncation 档）。
> 这是本区**第一次把「骨架层」当成独立变量做对照实验**，结论对全部 GBR 波次有效。

---

## 一、骨架规则（可直接套用，不用再测）

### R1. `group_rank(·, sector)` 默认禁用 —— 代价 −0.02 至 −0.81 Sharpe

| 数据集 | 对照（无分组秩） | 加 `group_rank(·,sector)` | ΔS | Δ2Y |
|---|---:|---:|---:|---:|
| analyst47 情绪 | 1.91 | **1.10** | **−0.81** | **−0.81** |
| analyst7 目标价均值 | 2.00 | 1.98 | −0.02 | −0.14 |
| analyst7 目标价下限 | 1.87 | 1.74 | −0.13 | −0.21 |
| analyst7 营收均值 | 1.76 | 1.66 | −0.10 | −0.16 |

**8 个对照里方向 100% 一致，无一例外。** 幅度取决于信号本身是否已是截面上界有限量：
情绪类（重尾、无界）被打 −0.81；修订比率类（已归一到 [−1,1]）只被打 −0.02~−0.13。

**替代品**：需要分组归一优先 `group_scale(·, sector)` —— analyst47 上 1.91 → 1.92（几乎无损），2Y 1.75 → 1.78。

### R2. `maxTrade ON` 是 fitness 的关键设置项

| alpha | maxTrade | TO | margin | F |
|---|---|---:|---:|---:|
| analyst47 情绪 | OFF | 27.2% | 3.3bp | 0.77 |
| analyst47 情绪 | **ON** | **19.0%** | **4.9bp** | **0.97** |
| shortinterest 供给 | OFF | 9.18% | 9.81bp | 0.92 |
| shortinterest 供给 | **ON** | 7.5% | **12.2bp** | **0.93** |

**机制**：maxTrade 削掉的是「单票超大头寸」这批高噪声交易 ⇒ 换手降、margin 升。
**副作用**：maxTrade ON + STATISTICAL + decay 2 的组合曾经把一批仿真的父任务卡在 progress 0.1（W63），但同批表达式改 maxTrade OFF 后 3 分钟跑完 ⇒ **卡死是平台侧偶发，不是 maxTrade 本身不合法**。

### R3. `ts_target_tvr_decay` 只对「快变计数型」核心必要，对「慢变比率型」核心有害

| 核心类型 | 例子 | 不加 tvr_decay | 加 tvr_decay |
|---|---|---|---|
| 慢变比率 | `divide(subtract(cur, lag), add(abs(lag),1))` | **TO 10.9% / F 1.52** | TO 11.2% / F 1.45 |
| 快变计数 | `subtract(rank(raised_1wk), rank(lowered_1wk))` | **TO 24.9% / F 0.80（挂）** | TO 12.2% / F 1.29 |

**判据**：先跑裸形态，看 TO。
- TO ≤ 18% ⇒ **不要**加 tvr_decay（加了只削 alpha）。
- TO ≥ 22% ⇒ **必须**加，target_tvr 设在 0.08–0.12。

### R4. 凸化指数与分位窗口不是敏感项，别在这里花预算

| 维度 | 取值 | S |
|---|---|---:|
| `signed_power` 指数 | 0.2 / 0.3 / 0.4 / 0.5 | 1.93 / **1.97** / 1.95 / 1.95 |
| `ts_quantile` 窗口 | 252 / 504 / 1008 | 1.80 / **1.97** / 1.78 |

504 / 0.3 是局部最优但改善量 ≤0.04。**窗口白名单只用 252 / 504。**

### R5. `signed_power` 必须作用在**已中心化**的信号上

- ✗ `signed_power(group_rank(x), 3)` —— group_rank 输出 [0,1]，立方只压中段 ⇒ S 2.33 → 0.84。
- ✓ `signed_power(subtract(rank(x), 0.5), e)` —— 中心化成 [−0.5,0.5] 再凸化。
- ✓ `signed_power(ts_quantile(x, W), 0.3)` —— ts_quantile 输出 [0,1] 但指数 <1 是**扩尾**，纯单调变换不破坏信号。

### R6. 平滑杠杆救不了 fitness —— 它是「拿 Sharpe 换 margin」

analyst47 核心（F 0.97，需 1.00）的 8 个平滑变体全部失败：

| 杠杆 | S | F | TO | margin |
|---|---:|---:|---:|---:|
| 无（对照） | **1.97** | **0.97** | 19.0% | 4.9bp |
| `ts_target_tvr_decay` 0.18 | 1.64 | 0.82 | 15.4% | 5.0bp |
| `ts_decay_linear` 5 | 1.69 | 0.84 | 16.2% | 5.0bp |
| `ts_decay_linear` 10 | 1.46 | 0.73 | 14.3% | 4.9bp |
| `winsorize` std 1.5 / 2.0 / 3.0 | 1.93 / — / — | 0.94 / — / — | 18.8% | 4.8bp |

⇒ **fitness 缺口要靠设置档（truncation / maxTrade / decay）补，不要靠算子补。**

---

## 二、模板库（按机制族归档，含判死标记）

### 族 A：分析师一致预期「水平 + 修订方向」（analyst7，已点亮塔）

| # | 模板 | 核心 | 状态 |
|---|---|---|---|
| A1 | 比率型修订（慢变） | `winsorize(rank(divide(subtract(BF(f),BF(lag)), add(abs(BF(lag)),1))), std=0.2)` | ✅ **最优骨架**（9 算子，S 1.76–2.00） |
| A2 | 广度净差（快变计数） | `group_rank(ts_target_tvr_decay(winsorize(rank(ts_backfill(subtract(rank(raised),rank(lowered)),250)),std=0.2),tvr=0.08),sector)` | ✅ 唯一需要重骨架的（12 算子，S 1.84） |
| A3 | 分位凸化 | `signed_power(ts_quantile(x,504),0.3)` | ✅ 同族等效 |
| A4 | 分歧度 `_std` | — | ❌ 17 条最高 S 1.01 |
| A5 | 意外计数 `surprisenum` | — | ❌ 最高 S 0.42 |
| A6 | 实际值 `act_12m_*_value` | — | ❌ ≤0.1 |
| A7 | 死科目 opr / roa / ent / bps / net | — | ❌ |

### 族 B：分析师情绪打分（analyst47，ATOM）

| # | 模板 | 状态 |
|---|---|---|
| B1 | `winsorize(signed_power(ts_quantile(anl47_rawsentiment,504),0.3), std=2.5)` | ✅ S 1.97 / F 0.97 / 5 算子 |
| B2 | 截面秩中心化替代分位 | ❌ 0.45（只是信息源不同但更弱） |
| B3 | 作者战绩加权 / 老化门控 / 指标-原始和分歧 / 22 日修订 | ❌ 全部 ≤0.50 |

### 族 C：一致预期「分布形态」（analyst_factor_signals，96 MATRIX 字段）

| # | 模板 | 字段 | S | 状态 |
|---|---|---|---:|---|
| C1 | 分歧度（CV）负向 | `{m}_y1_estimate_coeff_var` | −0.22 | ❌ |
| C2 | 预测偏度负向 | `{m}_y1_estimate_skewness` | 0.21 | ❌ |
| C3 | 不对称（mean−median）负向 | `{m}_y1_estimate_asymmetry` | 0.27 | ❌ |
| C4 | 长期增长外推（5 年 CAGR）负向 | `{m}_y1_cagr_5yr` | −0.10 | ❌ |
| C5 | 分歧度 66 日变化负向 | `revenue_y1_estimate_coeff_var` | −0.18 | ❌ |
| C6 | 分歧 × 偏度 交互负向 | 两字段 | −0.02 | ❌ |
| C7 | 增长久期（FY2 − FY1） | `revenue_y{1,2}_consensus_value` | −0.41 | ❌ |
| C8 | **修订（对照）** | `eps_y1_estimate_change_3mo` | **1.89 / F 1.20** | ⚠️ **2Y 0.14 ⇒ 封盘** |

**教训**：C1–C4 四条在学术上有明确先验（DMS 2002 / CDG 2013 / La Porta 1996），**但先验成立 ≠ GBR TOP700 十年样本上成立**。

### 族 D：借券供给（shortinterest3，未点亮塔）

| # | 模板 | S | 状态 |
|---|---|---:|---|
| D1 | 借券存量长窗分位（负向） | **1.54** | ✅ 塔内最强，但差 0.04 |
| D2 | 借券市值供给（负向） | 1.42 | ⚠️ |
| D3 | 供给 252 日 z 分位（负向） | 1.30 | ⚠️ |
| D4 | 拥挤度 = 供给秩 × 费率秩（负向） | 1.12 | ❌ |
| D5 | 平均单笔规模（供给/笔数）（负向） | 0.75 | ❌ |
| D6 | 供给 22 日动量（负向） | 0.24 | ❌ |
| D7 | 借贷久期（负向） | 0.39 | ❌ |

**方向铁律**：「供给 / 数量」类字段必须取负（`multiply(-1, ·)`）。W65 用正号时同一信号变 −1.42。

### 族 E：分析师覆盖度（analyst9，51 VECTOR 字段，alphaCount 0–87 极低拥挤）

| # | 模板 | 经济机制 | 状态 |
|---|---|---|---|
| E1 | 覆盖度水平负向 | 被忽视公司效应（Arbel-Strebel 1983） | 待测（W72） |
| E2 | 覆盖度 22 日变化正向 | 投资者认知（Merton 1987） | 待测 |
| E3 | 净修订广度 / 覆盖度 正向 | 修订广度归一化 | 待测 |
| E4 | 修订强度（净/总）正向 | 同 E3 的有界版 | 待测 |
| E5 | 无变化比例负向 | 分析师惰性/粘性 | 待测 |
| E6 | 未过滤净修订正向 | 含被排除分析师 | 待测 |
| E7 | 双源共识（快照净修订） | 数据源交叉验证 | 待测 |
| E8 | 覆盖度 × 净修订 交互 | 冷门股修订更值钱 | 待测 |

**VECTOR 处理铁律**：先 `vec_sum / vec_avg` 转标量，再套 `ts_backfill` / `rank`。
直接对 VECTOR 用 `winsorize` / `days_from_last_change` ⇒ `does not support event inputs`，**整批连坐 CANCELLED**。

---

## 三、设置档速查（GBR）

| regime | decay | neut | trunc | maxTrade | 适用 |
|---|---:|---|---:|---|---|
| **ATOM 短兴趣 / 情绪** | 2 | STATISTICAL | 0.05–0.08 | **ON** | fitness 差距大时首选 |
| **ATOM 修订比率** | 0 | FAST | 0.10 | OFF | 换手已低，不要平滑 |
| **快变计数（广度）** | 0 | FAST | 0.10 | OFF | 必须配 tvr_decay 在表达式里 |
| 通用兜底 | 0 | FAST | 0.10 | OFF | 未探索的新集 |

**已验证可用 neutralization**：FAST / CROWDING / SECTOR / SUBINDUSTRY / STATISTICAL / INDUSTRY / MARKET / REVERSION_AND_MOMENTUM。
**不可用**：COUNTRY（GBR 是单一国家，报错）。
**已验证可用 decay**：0 / 1 / 2 / 4 / 15 / 16；**truncation**：0.05 / 0.06 / 0.08 / 0.10。

---

## 四、算子预算（上限 12，越少越好）

| 骨架 | 算子数 | 说明 |
|---|---:|---|
| `winsorize(signed_power(ts_quantile(f,W),e), std=s)` | 3 | 最省，analyst47 用这个 |
| `winsorize(rank(f), std=s)` | 2 | 最省，水平型信号 |
| `winsorize(rank(divide(subtract(BF(f),BF(l)), add(abs(BF(l)),1))), std=0.2)` | 9 | 比率型修订标准骨架 |
| 上一行 + `group_rank(·, sector)` | 10 | **不推荐**（R1） |
| 上一行 + `ts_target_tvr_decay(·, tvr=0.1)` + `group_rank` | 12 | 只给快变计数用（R3） |

**超预算时优先删**（按删除代价从低到高）：`group_rank` → `add(...,1)` 兜底 → `abs()` → 重复的 `ts_backfill`（改成外层统一 backfill）。

---

## 附录 A（2026-11-04 下半场追加）：R7–R10 + 新数据族 F/G

### R7 σ-of-rev：修订类信号的分母应当用「修订序列自身的波动」（SUE 式标准化）

同一 `est_12m_pre_mean` 3 月修订核心，只改分母，得到**单调阶梯**：

| 分母 | alpha | 算子 | S | F | SUB | margin |
|---|---|---:|---:|---:|---:|---:|
| `add(abs(lag), 1)` 滞后水平 | `1YNX8LQW` | 9 | 2.00 | 1.52 | 0.95 | 13.2bp |
| `ts_std_dev(level, 252)` 水平波动 | `mLomEeZK` | 8 | 2.10 | 1.56 | 1.19 | 12.6bp |
| **`ts_std_dev(rev, 252)` 修订波动** | **`omEW1Mbk`** | **10** | **2.21** | **1.73** | **1.26** | **13.8bp** |

标准化写法：
```
R = subtract(ts_backfill(f,500), ts_backfill(f_lag,500))
winsorize(rank(divide(R, ts_std_dev(R, 252))), std=0.2)
```

**含义**：分子是本次修订，分母是「该公司平常的修订幅度」⇒ 输出「这次修订有多反常」。
除以滞后水平只做量纲归一；除以修订波动才做**信噪比归一**。对应 SUE（Bernard–Thomas 1989/1990）。

**适用边界（W76/W78 实测）**：只在「修订幅度量级跨公司异质大」的核心上起效 ——
`pre_mean` 3 月 **+0.21 S** ＞ `sal_mean` 4 周 **+0.13 S** ＞ `pre_low` 4 周 **−0.06 S**（轻微有害）。
`pre_high`（目标价上限）本身是死字段（S 1.42 / F 0.77 / 2Y 0.87），不必再投。

### R8 分组归一用 `group_zscore` / `group_scale`，禁用 `group_rank`

平台论坛 EUR `fund_holdings_panel` 实战帖（article_id 41049370096663，votes 22）实测最佳式：
```
ts_decay_linear(group_zscore(vec_avg(stable_boundary_trade_count_21d), sector), 20)
```
→ EUR S 0.93 / 2Y 2.28；反序 `group_zscore(ts_decay_linear(...), sector)` 与 decay 窗 20/60 变体全部略差（S 0.91–0.93）。

- **顺序**：先分组归一、再时序平滑（与我在 GBR 得到的 R1 结论一致方向：分组层放在时序层内侧）。
- **算子选择**：`group_zscore` **保留幅度信息**、`group_rank` 只留排序。
  R1 已证 `group_rank` 在 analyst47 上 −0.81 S、在 analyst7 上 −0.02～−0.13 S，8 个对照方向 100% 一致损害。
  ⇒ 需要分组归一时的优先序：`group_zscore` ＞ `group_scale` ＞ `group_neutralize` ＞＞ `group_rank`（默认禁用）。
- **分组轴**：`sector` 优于 `subindustry`（W78 实测 `F3_subind` S 0.71 vs `sector` 1.36，几乎腰斩）。

### R9 日频流水类数据集必须重平滑才能进换手闸

`fund_holdings_panel`（18 VECTOR 字段，字段级 cov 0.8912–0.9286）是**日频账户级交易流水**：

| 处理 | alpha | TO | S | F |
|---|---|---:|---:|---:|
| 无平滑（W77） | `58EgZj9X` / `QPvK1Y5w` 等 8 臂 | **75.8%–111.0%** | −1.48 ～ 0.42 | ≤0.05 |
| `group_zscore(sector)` + `decay 20`（W78） | `WjOej1Mo` | **48.0%** | 1.36 | 0.42 |
| `group_zscore(subindustry)` + `decay 20` | `QPvKPZJG` | 93.2% | 0.71 | 0.11 |

**规律**：`decay 20` 只把 TO 从 ~87% 压到 48%，仍高于 30% 上限 ⇒ 该类数据需要 **decay ≥60 或 decay + `ts_mean(·,66)` 双平滑**（W80 在验）。
**判据**：拿到新数据集先看 TO，TO > 60% 的日频流水类不要指望单层 decay 够用。

### R10 闸限口径修正：`sub_universe_sharpe` 在 GBR/TOP700 的实际限是 **0.95**

此前台账记的 0.25 是错的。平台 `LOW_SUB_UNIVERSE_SHARPE` 在 `leAvoJr7`（sub=0.94）上报 fail、`limit=0.95`。
但 `rKROZQW1`（sub 同为 0.94）平台未报 fail ⇒ 该检查可能按子宇宙重算、与 `metrics.sub_universe_sharpe` 不完全同值。
**处置**：`sub ∈ [0.90, 0.95)` 一律记为「疑似挂闸」，不得算作通过；`sub ≥ 0.95` 才安全。

### 新数据族 F：INSTITUTIONS `fund_holdings_panel`（18 VECTOR，cov 0.8912–0.9286）

| 字段 | cov | ac | 语义 | 实测 |
|---|---:|---:|---|---|
| `stable_boundary_trade_count_21d` | 0.9286 | 57 | **无先前边界交易账户的新建/清仓笔数**（真正的新进者） | **唯一有效**；`group_zscore+decay20` → S 1.36 |
| `boundary_transaction_total` | 0.9286 | 51 | 边界交易总笔数（建仓+清仓，无方向） | 与成交金额之比（换手强度）S −1.48 ⇒ 取反 **+1.48** |
| `stable_boundary_trade_count_21d_active` | 0.8912 | 45 | 同上，限主动型基金 | 未测 |
| `transaction_account_total` | 0.9286 | 38 | 当日交易的账户家数 | **全族死**（论坛同证 `holder_account_total` S −0.88） |
| `security_transaction_usd_value` | 0.9286 | 40 | 成交金额（USD） | 仅作分母 |
| `herfindahl_index_transactions` | 0.9286 | 33 | 账户间成交额 HHI（0–1） | S 0.14（死） |
| `top_weighted_transaction_number` / `_active` | 0.9286/0.8912 | 13/**0** | 信心持仓交易笔数 | S 0.36（弱） |
| `large_trade_count_50bps` | 0.9286 | 9 | 单笔 >0.5% AUM 的大单笔数 | S 0.40（弱） |
| `transaction_value_distribution_score` | 0.9286 | 13 | 成交额分散度（0–1） | 未测 |

**注意**：无「带符号净流入」字段 ⇒ 一切方向必须靠**占比/相对量**构造，不能直接读净买卖。
**建议算子链**：`ts_decay_linear(group_zscore(vec_avg(f), sector), ≥60)`（4 算子，极省预算）。

### 新数据族 G：SENTIMENT `sentiment7`（3 VECTOR，cov 0.5766–0.5819，ac 16–45）

| 字段 | cov | ac | 语义 |
|---|---:|---:|---|
| `snt7_views` | 0.5766 | 45 | Wikipedia 页面日浏览量 |
| `snt7_all_languages_views` | 0.5819 | 37 | 全语言浏览量 |
| `snt7_timestamp` | 0.5766 | 16 | 记录日期（YYYYMMDD），不可算术 |

**文献先验**：Moat et al. (2013) 维基百科使用量领先股价变动；Da–Engelberg–Gao (2011) 注意力上升 ⇒ 短期买入压力后反转 ⇒ **注意力异常取负向**。
**风险**：cov 仅 0.577（TOP700 里 42% 无数据）+ 只有 3 字段 ⇒ 多样性只能靠变换，不能靠字段。W79 首次开波。
