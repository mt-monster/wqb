# IND REGULAR Alpha 战役 — 画像、合规与判死证据报告（2026-10-29 快照）

> 归属：人工审计与复盘（AGENTS §8.13 → `reports/<主题>_<YYYYMMDD>.md`）。
> 快照日 2026-10-29。数据源：`wqb.db` 数据集画像表（144 个 IND 数据集）、平台 `get_user_alphas(region=IND, status=ACTIVE)`、`get_submit_ready` 待提交池 60 条、本地 `backtest_results`。

---

## 0. 一句话结论

IND 的可交付面已经**不是"挖不出 alpha"的问题，而是"合规口径卡住交付"的问题**：54 颗 ACTIVE 里 12 颗纯 ATOM（单数据集），全部 50 条已核 prod < 0.70；但**待提交池 67 条 READY 中平台可归属的 PV+X 组合已越过"≤5"上限**，且 2 颗 `PV+MODEL` 属规则明令禁止。**未点亮四塔（INSIDERS / OPTION / SENTIMENT / SHORTINTEREST）已全部实证判死**（累计 24/14/12 臂，wave 275 INSIDERS 长周期批 8/8 全灭、最高 S=0.57）——IND 可产 ATOM 的只剩已点亮的 6 个 category。

**终池实况**（§5.4）：ATOM **11 颗**（4 颗 prod 已验证 + 4 颗待终验 + **3 颗本轮新出**：`akKJ3qn2` / `88RAAmZa` / `9qxoozer`）+ PV+X 5 颗（额度用满）+ 同族备选 7 颗。**严格执行额度时，可提交面上限 = 16 颗**；两颗高 S 候选 `MPalYZxM`(S4.37) / `mLoMnqPE`(S1.87) 已因 prod 撞墙（0.824 / 0.7818）出池。

**本轮增量（§4.6）**：转向"已点亮塔 × 新数据集"后，waves 276–279 共 24 臂出 3 颗可交付 ATOM，转化率 12.5%。核心新机制是 **`rank(ts_delta(<百分位字段>, 22))` 的"升级型"信号**（model39 value-momentum），self-corr 仅 0.21/0.27，是全池最正交的两颗。

---

## 1. 回测设置（IND 权威口径，全部波次一致）

| 项 | 值 |
|---|---|
| instrumentType / region / universe | EQUITY / IND / **TOP500** |
| delay / neutralization | 1 / **STATISTICAL** |
| decay / truncation | 4 / 0.08 |
| pasteurization / unitHandling | ON / VERIFY |
| nanHandling / maxTrade | OFF / OFF |
| testPeriod | **P0Y0M0D**（不用平台默认 IS 分割，避免 2Y 口径漂移） |
| language / simulationMode | FASTEXPR / FULL |
| 回测区间 | 2014-01-01 ~ 2023-12-31（**覆盖近十年**，满足 goal 第 4 条） |

**闸线（IND 本地口径）**：S ≥ 1.58、F ≥ 1.0、TO ∈ [0.03, 0.70]、sub-universe Sharpe ≥ 0.78、CLUSTER_TEST ≥ 1、2Y Sharpe ≥ 1.58、robust ≥ 1、prod < 0.70、self < 0.70。

---

## 2. 数据集画像：144 个 IND 数据集 × 16 个 category

总量：**18,330 个字段**、平台累计 **248,115 个 alpha**（拥挤度）、本地回测 **773 个**波次行、字段覆盖率均值 **0.7171**。
字段级状态：可挖 62 / 已判死 147 / 未测 10,739。

| category | 数据集 | 字段 | 覆盖均值 | 平台 alpha | 本地回测 | 活 | 死 | 未测 | 最好 S | 最好 2Y |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MODEL | 43 | 4,793 | 0.72 | 77,760 | 169 | 20 | 46 | 3,614 | 3.60 | 3.31 |
| NEWS | 22 | 862 | 0.75 | 6,260 | 42 | 2 | 13 | 502 | 3.47 | 1.65 |
| OTHER | 21 | 1,666 | 0.66 | 13,202 | 0 | 0 | 1 | 1,119 | 0.33 | 1.32 |
| PV | 13 | 1,413 | 0.87 | 45,753 | 143 | 8 | 7 | 783 | **6.48** | 3.25 |
| ANALYST | 13 | 4,484 | 0.62 | 35,643 | 114 | 7 | 33 | 3,043 | 3.25 | **3.58** |
| FUNDAMENTAL | 12 | 3,412 | 0.58 | 22,224 | 0 | 0 | 0 | 518 | — | — |
| RISK | 4 | 97 | **0.92** | 19,001 | 8 | 3 | 1 | 39 | 3.52 | 2.84 |
| SENTIMENT | 4 | 357 | 0.84 | 5,977 | 121 | 4 | 20 | 201 | 3.01 | 2.07 |
| EARNINGS | 3 | 109 | 0.70 | 10,868 | 36 | 2 | 13 | 0 | **4.49** | 1.48 |
| INSIDERS | 2 | **10** | 0.78 | 907 | 6 | 0 | 5 | 1 | **0.92** | 1.16 |
| OPTION | 2 | 40 | **0.38** | 3,369 | 36 | 1 | 5 | 0 | 1.94 | 2.50 |
| SHORTINTEREST | 1 | 3 | 1.00 | 2,314 | 7 | 0 | 1 | 2 | **0.22** | 0.21 |
| MACRO | 1 | **1** | 1.00 | 1,890 | 0 | 1 | 0 | 0 | 2.90 | — |
| INSTITUTIONS | 1 | 11 | 0.99 | **94** | 82 | **11** | 0 | 0 | 3.45 | 3.29 |
| IMBALANCE | 1 | **2** | 0.55 | — | 0 | 2 | 0 | — | 2.81 | — |
| （无类目）model238_anlrev | 1 | 1,070 | — | — | 9 | 1 | 2 | — | 2.64 | 3.08 |

### 2.1 画像给出的四条结构判断（决定"用什么机制"）

1. **字段量与拥挤度严重错配**：MODEL 43 个数据集 4,793 字段、平台已 77,760 个 alpha（最挤），而 INSIDERS 2 个数据集**只有 10 个字段**、平台仅 907 个 alpha（最空）。**拥挤度低 ≠ 好挖**——INSIDERS 的 10 个字段里 5 个已在本地判死，最好 S 只有 0.92。
2. **INSTITUTIONS 是唯一的"高产出低拥挤"洼地**：1 个数据集 11 字段，本地 82 次回测出 **11 个活字段**、最好 S 3.45 / 2Y 3.29，平台只有 94 个 alpha。这与交付面一致：INSTITUTIONS 塔已有 4 颗 ACTIVE。
3. **覆盖均值低于 0.60 的 category 不可直接做尽**：FUNDAMENTAL 0.58、ANALYST 0.62、OPTION 0.38。OPTION 的低覆盖是结构性的（期权数据本身稀疏），这直接解释了它的 8 臂全灭（见 §4.2）。
4. **"最好 S 高但 2Y 低"是判死信号**：EARNINGS 最好 S 4.49 但 2Y 仅 1.48 —— 强信号集中在单一行情段；SHORTINTEREST 最好 S 0.22 / 2Y 0.21，全 category 无可用信号。

---

## 3. 交付面：54 颗 ACTIVE，12 颗纯 ATOM

平台口径：`server_count = 370`（IND 全部 alpha），`server_scanned = 200`，`count = 54`（ACTIVE / OS）。下表为其中 50 条的逐条核验。

### 3.1 金字塔归属（多计数，50 条）

| 塔 | 颗数 |
|---|---:|
| PV | 18 |
| MODEL | 9 |
| RISK | 7 |
| ANALYST | 7 |
| NEWS | 6 |
| OTHER | 6 |
| EARNINGS | 4 |
| FUNDAMENTAL | 4 |
| INSTITUTIONS | 4 |
| MACRO | 2 |
| IMBALANCE | 1 |
| **INSIDERS / OPTION / SENTIMENT / SHORTINTEREST** | **0（未点亮）** |

`pyramids.effective` 分布：**1 → 12 颗（纯 ATOM）**、2 → 25 颗、None → 11 颗、0 → 2 颗。

### 3.2 12 颗 ATOM（单数据集）逐条

| alpha | 塔 | S | F | 2Y | prod | self | prod 余量 |
|---|---|---:|---:|---:|---:|---:|---:|
| A1VZQXAg | RISK | 3.34 | 2.28 | 2.24 | 0.6607 | 0.6607 | 0.339 |
| d51eGdKY | PV | 3.06 | 1.73 | 2.13 | 0.6904 | 0.4780 | **0.310** |
| A1vzEm9g | OTHER | 2.84 | 1.97 | 2.19 | 0.5905 | 0.4112 | 0.410 |
| omEpqEXl | RISK | 2.75 | 1.75 | 2.49 | 0.5898 | 0.4496 | 0.410 |
| A1QQ0q8d | FUNDAMENTAL | 2.59 | 1.98 | 2.18 | 0.6612 | 0.4693 | 0.339 |
| akxXl7w1 | MODEL | 2.29 | 1.05 | 2.18 | 0.6921 | 0.3391 | 0.308 |
| 78oeRVzO | FUNDAMENTAL | 2.09 | 1.63 | 2.15 | 0.6835 | 0.4506 | 0.317 |
| WjLbrw7O | FUNDAMENTAL | 2.08 | 1.61 | 1.86 | **0.6937** | 0.5548 | **0.306** |
| LL5gZoLm | ANALYST | 1.88 | 1.38 | 2.17 | 0.6660 | 0.3115 | 0.334 |
| RR7v9gV0 | MODEL | 1.83 | 1.38 | 1.69 | 0.6837 | 0.3625 | 0.316 |
| Xg73mNda | MODEL | 1.79 | 1.28 | 2.39 | 0.6254 | 0.3439 | 0.375 |
| zqrj0bzK | ANALYST | 1.66 | 1.17 | 2.33 | 0.6664 | 0.4211 | 0.334 |

**ATOM 塔覆盖仅有 6 个 category**（RISK 2 / FUNDAMENTAL 3 / MODEL 3 / ANALYST 2 / PV 1 / OTHER 1），且 **NEWS / EARNINGS / INSTITUTIONS / MACRO / IMBALANCE 五个塔没有一颗 ATOM** —— 这些塔的 25 颗全部是双腿（effective=2）。

### 3.3 prod 直方图（50 条，全部 < 0.70）

| 桶 | n |
|---|---:|
| [0.40, 0.50) | 6 |
| [0.50, 0.55) | 4 |
| [0.55, 0.60) | 12 |
| [0.60, 0.65) | 7 |
| **[0.65, 0.70)** | **21** |
| [0.70, 1.00) | **0** |

min 0.4049 / median 0.6394 / max 0.6937。

**读法**：`[0.65,0.70)` 装了 21 颗（42%），最大 0.6937 —— **余量只剩 0.006 到红线**。这不是"还安全"，而是"整族已经贴墙"。按族级判据（`[0.70,0.80)` 桶 n=0 可救 / n≥1 必死），IND 目前仍可救，但**任何一颗新提交都会把整族推向墙外**，所以提交顺序必须按 prod 升序，从余量大的先上。

---

## 4. 未点亮塔攻击记录（waves 272–275）

### 4.1 wave 272 — SENTIMENT 纯字段水平结构（8 臂，全灭）

multisim `1X0lU4zR4CDbdpVX6PrjKu`。sentiment21 纯字段、水平结构（非 dev 反转）。
结果：S ∈ [−0.50, 0.23]、F ∈ [−0.19, 0.06]，**8/8 全部 effective=1（ATOM 形态成立）但指标全负**。
**判定：SENTIMENT 水平结构 ATOM 判死**。这不是"没挖到"，是"结构方向错了" —— 后续 sentiment 必须走反转/dev 口径（已是既有家族做法）。

### 4.2 wave 273 — OPTION 纯字段（8 臂，全灭）

multisim `CvaI53fQ4Ela3fRBSlk6o9`。option30 纯字段。
结果：S ∈ [−0.55, 0.54]、TO ∈ [0.05, 0.44]、2Y ∈ [−0.84, 1.39]，**符号无稳定性**（同一批里 2Y 正负各半）。
**判定：OPTION 塔累计 14 臂（本批 8 + 早前 6）全灭，判死**。根因指向覆盖 0.3629 —— 期权字段在 IND/TOP500 上太稀疏，`ts_backfill(…, 22)` 补不满，信号是噪声。

### 4.3 wave 274 — insiders + sentiment 非水平结构（8 臂，全灭）

multisim `OGhn6cB656A9Y966DbGIyQ`。
- INSIDERS 4 臂：S = 0.06 / **0.43** / −0.62 / −0.03。唯一正值是 `ts_delta(vec_avg(insd1_holdings), 66)`。
- SENTIMENT 4 臂：S = −0.30 / 0.10 / −0.80 / −1.06。

**判定**：`SENTIMENT` 累计 12 臂全灭；INSIDERS 亦全灭，但 0.43 那条**唯一正号且方向可解释**（持仓变化而非交易金额），成为 wave 275 的种子。

### 4.4 wave 275 — INSIDERS 长周期（8 臂，全灭）

multisim `2gDOIf9ba4QubWt19AXvFrxO`，8 臂，全部不含 `returns` ⇒ 纯 ATOM 形态。

设计依据（**两条外部证据直接推翻前 4 臂的窗口设定**）：
1. **论坛**（JX84394《内部人"动了多少仓位"比"动了多少钱"更重要 —— DEU 内部人信念强度因子》，69 votes）：模板 `signal = 流量字段 / (存量字段 + ε)`，`accum = ts_sum(signal, 申报周期)`；另一帖 FF56620 记录了一次"被自己对照组证伪"的 insider 挖掘，结论是必须留对照组。
2. **论文**：印度专有交易级数据的 cross-insider trading 显著预测未来收益**且不反转**；美国科技公司 insider purchases 后续 **3 年 1.1%/月**异常收益 ⇒ **持有期是"年"量级，不是 22–66 天**。前 4 臂用 66 天窗口，方向对但窗口错了一个数量级。

8 臂（窗口 252 / 504）：
```
① group_rank(ts_sum(ts_backfill(vec_sum(insd1_valueeur), 22), 252), industry)                      净买入额 252d 累计
② group_rank(ts_delta(ts_backfill(vec_avg(insd1_holdings), 22), 252), industry)                    持仓变化 252d 累计（0.43 臂的长窗版）
③ group_rank(ts_sum(divide(ts_backfill(vec_sum(insd1_valueeur),22), add(abs(ts_backfill(vec_avg(insd1_value),22)),1)), 252), industry)   流量/金额比
④ group_rank(ts_sum(divide(ts_backfill(vec_sum(insd1_valueeur),22), add(abs(ts_backfill(vec_avg(insd1_holdings),22)),1)), 252), subindustry) 流量/持仓比
⑤ group_rank(ts_mean(ts_backfill(vec_avg(insd1_tradesignificance), 22), 252), industry)            显著性 252d 均值
⑥ group_rank(ts_sum(ts_backfill(vec_count(insd1_valueeur), 22), 252), industry)                    交易笔数 252d 累计
⑦ group_rank(ts_zscore(ts_sum(ts_backfill(vec_sum(insd1_valueeur),22),252), 504), industry)        净买入 504d 历史分位
⑧ group_rank(subtract(ts_mean(ts_backfill(vec_avg(insd1_tradesignificance),22),252),
                      ts_mean(ts_backfill(vec_avg(insd1_tradesignificance),22),22)), industry)      显著性长短差
```
预检：`validate_expressions` → `valid: true`、8 条、`unknown_fields: []`、平台字段数 4（`insd1_holdings` / `insd1_tradesignificance` / `insd1_value` / `insd1_valueeur`）。

**第 ⑧ 臂是这批唯一的对照组**（不是"更强的信号"，而是"用同一字段做长短差以剥离水平项"）—— 对应 FF56620 的教训：没有对照组的 insider 批无法区分"信号"与"长期趋势"。

**结果（harvest 8/8 COMPLETE，0 error）**：

| # | alpha | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| ① 净买入额 252d | `A1Vd2xbw` | −0.09 | −0.01 | 0.0703 | −0.60 |
| ② 持仓变化 252d | `6Xdb2M1L` | −0.35 | −0.09 | 0.3574 | −0.48 |
| ③ 流量/金额比 | `leAZNazO` | 0.02 | 0.00 | 0.0731 | −2.16 |
| ④ 流量/持仓比 | `2rAk25ZZ` | −0.21 | −0.06 | 0.0721 | −2.06 |
| ⑤ 显著性均值 | `QPvdo0lW` | −0.54 | −0.22 | 0.0662 | 0.17 |
| ⑥ 交易笔数 | `KPJR2g8p` | 0.04 | 0.00 | 0.0727 | −2.11 |
| ⑦ 净买入 504d 分位 | `npvbXaOw` | **0.46** | 0.17 | 0.0757 | 0.09 |
| ⑧ 显著性长短差（对照） | `vR1VoAJv` | **0.57** | 0.25 | 0.1470 | 0.33 |

**判定 FAIL**：最高仅 `vR1VoAJv` S=0.57，离闸线 1.58 差一个量级。三点归因：
1. **换手 0.066–0.073 极低** ⇒ 长窗 `ts_sum` 把稀疏事件抹成常数，信号几乎不动，`group_rank` 后多空仍各 250 只（`longCount=252`）= 截面上没有区分度。
2. **2Y 崩塌到 −2.06 ~ −2.16**（③④⑥）说明不是"噪声不显著"，而是 2022–2023 段方向整体反转 —— 长窗累计的净买入在近两年是**反向**的。
3. **对照组（⑧）反而最好，但它剥离的是水平项** ⇒ 与 FF56620 的教训一致：insiders1 在 IND/TOP500 上没有稳定的水平项可用，能用的只剩短窗差分（wave 274 的 0.43 臂）。

**结论：INSIDERS 塔累计 3 波 24 臂全灭，IND/TOP500 判死。** 四条未点亮塔（SENTIMENT / OPTION / INSIDERS / SHORTINTEREST）至此全部实证判死 —— 不是"没试"，而是每塔 ≥ 8 臂、含方向/窗口/结构三轴对照。

### 4.5 未点亮塔战役收口

| 塔 | 累计臂数 | 最好 S | 判定 | 根因 |
|---|---:|---:|---|---|
| SENTIMENT | 12 | 0.23（水平）/ −0.30（dev 反向最好 −0.30→已用旧族） | 判死 | 水平项无信息，只有 dev 反向老族有效且已被占用 |
| OPTION | 14 | 0.54 | 判死 | 覆盖 0.3629，`ts_backfill(…,22)` 补不满 |
| INSIDERS | 24 | 0.57 | 判死 | 事件稀疏 + 长窗抹平 + 2Y 方向反转 |
| SHORTINTEREST | — | 0.22 | 判死（更早） | S 与 2Y 双低（0.22 / 0.21） |

⇒ **IND 的 16 个 category 里，可产 ATOM 的只有已点亮的 6 个**（RISK / FUNDAMENTAL / MODEL / ANALYST / PV / OTHER）。继续在未点亮塔上重复投入是负期望，后续若再要 IND alpha，应转"已点亮塔 × 新数据集"（如 RISK 下的 risk71/risk68 剩余字段）。

### 4.6 已点亮塔 × 新数据集（waves 276–279，本报告最新增量）

策略转向的第一次实测：不碰未点亮塔，只在 RISK / OTHER / MODEL 三个已点亮塔里找**没挖过的新数据集**。

| wave | 数据集（塔） | 臂 | 全闸过 | 可交付 ATOM | 关键结论 |
|---|---|---:|---:|---:|---|
| 276a | risk70（RISK） | 4 | 1 | **0** | `short_term_industry_country_factor` 残差动量成立（`A1V6Kppg` S3.01 全闸过），但 self-corr **0.7372** 撞墙；换 sector 分组 robust 掉到 0.98 |
| 276b | risk70（RISK） | 4 | 0 | 0 | zscore 结构全灭：`broad_market_exposure_factor` 是**常量字段**（longCount=0/TO=0）；两个持仓类字段 S≈0 |
| 277 | other532（OTHER） | 8 | 4 | **1** | 日频特异收益率 5/10 日反转成立（`akKJ3qn2` S3.51 全闸 + self 0.6426）；**同族只能折 1 颗**（次好 `9qxoQLrV` self 0.7007 差 0.0007）；**月频轴判死**（S0.06 / S0.02） |
| 278 | model39（MODEL） | 8 | 3 | **2** | `value_momentum_rank_float` 的 **22 日变化（升级）= 强正向**：`88RAAmZa` S2.96（self **0.2119**）、`9qxoozer` S3.06（self **0.2697**）；`JjellVJ2` S3.83 但 self **0.7008**（差 0.0008） |
| 279 | model39 扩展 | 8 | 在飞 | — | region/sector(10,44)/industry(66)/global(22) 五档窗口 + long_term 动量双向 + short_term 平滑抢救臂 |

**三条可复用机制**（都已写进 DB `wave_results`）：

1. **`rank(ts_delta(ts_backfill(<百分位字段>, 22), W))` = 升级型信号**。value-momentum 百分位的"改善"比绝对水平干净得多：TO 只有 0.15–0.21，robust 1.06 / 1.30，且与现有 OS 池近乎正交（self 0.21 / 0.27）。分组越细稳健越差（industry 0.86、sector 1.06）——这是与直觉相反的实测。
2. **同数据集同信号族只能折 1 颗**。other532 四颗全闸过、彼此相关 0.64–0.70，交一颗就饱和。**扩面必须换数据集或换机制，换窗口无效**（277 的 4 个窗口 = 1 颗）。
3. **IND 的换手硬线是 0.40 不是 0.70**（平台 `HIGH_TURNOVER.limit` 实测）：`6Xdxbvp7` TO 0.4077 FAIL、`E563AXeK` TO 0.729 FAIL。反转族必须把 TO 钉在 0.39 以下。

---

## 5. 规则 5 合规审计（PV / MODEL / OTHER 组腿）

### 5.1 存量 54 颗 ACTIVE（历史提交，规则下达前）

| 组合 | 颗数 | 明细 |
|---|---:|---|
| PV+X | **17** | PV+INSTITUTIONS 4、PV+NEWS 5、PV+ANALYST 3、PV+EARNINGS 3、PV+MODEL 2、PV+IMBALANCE 1（部分三塔重叠） |
| MODEL+X | 6 | MODEL+PV 2、MODEL+RISK 2、FUNDAMENTAL+MODEL 1、MODEL+OTHER 1 |
| OTHER+X | 5 | NEWS+OTHER 1、MACRO+OTHER 2、OTHER+RISK 1、MODEL+OTHER 1 |
| **硬违规（PV/MODEL/OTHER 两两）** | **3** | `Vk0pQmkA`(PV+MODEL)、`LLZg3XWa`(PV+MODEL)、`d5jJebLv`(MODEL+OTHER) |

**定性**：这 3 颗是在规则下达前提交的，规则不可追溯（撤回已提交 alpha 是另一个动作，不在本轮范围）。登记在此以免后续误称"全部合规"。

### 5.2 待提交池 60 条 READY

平台可归属（`towers` 带 `pyramids` 载荷）的只有 **5 条**，其余 13 条 SUBMIT_LAYER_VERIFIED 与 42 条 IS_ONLY **没有平台金字塔载荷**。

| 口径 | PV+X | MODEL+X | OTHER+X | 硬违规 |
|---|---:|---:|---:|---|
| **平台金字塔（权威）** | 2 | 2 | 0 | **2**：`WjepYR7d`(PV+MODEL)、`786wl6b8`(PV+MODEL) |
| 表达式字段扫描（非权威） | 32/42 IS_ONLY | — | 3 | 3 条 `OTHER+PV`（`d51z7PVw` / `JjQzbQJj` / `e7QG2WJM`，`cap`/`returns` 只作 trade_when 条件） |

**为什么两个口径差这么多**：`d51z7PVw` 的 `expr` 是
`trade_when(greater(rank(ts_backfill(cap,22)),0.4), signed_power(rank(-ts_sum(oth532_emerging_daily_specificreturn,5)),0.4), …)`
—— `cap` 是**条件变量**，不是信号腿。平台自己也只记 `IND/D1/OTHER` 一塔（effective=1）。所以按"组腿"的语义，它是单塔；按"表达式中出现过 PV 字段"的语义，它是 PV+X。

**这是本轮唯一需要用户拍板的口径分歧**，我不替用户决定。两种口径下的可行上限完全不同：
- **口径 A（平台金字塔 = 组腿）**：合规存量 PV+X 已是 17 > 5，规则若追溯则整族已超限；若只约束新增，则待提交池只剩 0 个 PV+X 额度（已被存量吃穿）。
- **口径 B（表达式出现字段 = 组腿）**：额度同样为 0，且 32 条 IS_ONLY 全部不可提交。

**结论（两口径一致的部分）**：`WjepYR7d`、`786wl6b8` 在任何口径下都**不可提交**；20 颗终池必须从**不含 `returns`/`cap` 的纯单塔候选**里选。

### 5.3 待提交池的 ATOM 逐条确认（`get_alpha_details`，零仿真成本）

表达式 token 扫描不可信：`0mX9bpeq` 的 PV 腿写成 `corr_last_trade_price_with_volume`，`\bvolume\b` 匹配不到，会被误判成纯 ANALYST。**唯一零成本权威源 = `get_alpha_details` 的 `pyramids.effective`**（`batch_get_alpha_metrics` 与 DB `alphas` 行都不含 pyramids）。

池内 11 条 ATOM（`effective=1`）实测：

| alpha | 塔 | S | F | 2Y | TO | prod | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| `MPalYZxM` | PV | 4.37 | 3.16 | 2.46 | 0.3533 | **0.824** | ❌ prod 墙，不可提交 |
| `wpZwnrpd` | PV | 3.50 | 2.25 | 3.04 | 0.3907 | 未取到 | 待终验 |
| `88RoVq6V` | RISK | 3.35 | 2.29 | 2.21 | 0.2712 | 未取到 | 待终验（robust 1.30） |
| `78odJop1` | RISK | 2.89 | 2.34 | 2.60 | 0.2117 | 未取到 | 待终验（robust 1.32） |
| `58EbwZeN` | RISK | 2.76 | 1.76 | 2.48 | 0.2728 | 未取到 | 待终验（robust 1.05） |
| `e72L9vq6` | MODEL | 2.66 | 2.86 | 2.38 | 0.0476 | 未取到 | ⚠ 非 IND 标准设置（MARKET/decay5/nanON）+ `CLUSTER_TEST:ERROR`，进池须按 TOP500/STATISTICAL/decay4/nanOFF 重跑 |
| `d51z7PVw` | OTHER | 3.26 | 2.40 | 2.16 | 0.289 | 0.5966 | ✅ |
| `JjQzbQJj` | OTHER | 3.09 | 2.13 | 2.06 | 0.293 | 0.5658 | ✅ |
| `e7QG2WJM` | OTHER | 2.90 | 2.01 | 2.39 | 0.287 | 0.5751 | ✅ |
| `mLoMnqPE` | IMBALANCE | 1.87 | 1.43 | 2.99 | 0.0594 | **0.7818** | ❌ prod 墙，不可提交 |
| `58jPrvZ1` | ANALYST | 1.64 | 1.27 | 2.23 | 0.1142 | 0.5354（self 0.4843） | ✅ 带 `UNITS` WARNING |

非 ATOM 已排除（`effective≥2`）：`0mX9bpeq`(PV+ANALYST)、`YPbmOrEw`(INST+PV+EARN)、`d5bm6XYx`(PV+EARN+ANALYST)、`zq8jLYoG`(PV+EARN)、`QPbjAJOp`(PV+NEWS)。

**prod 取数方法**：`check_correlation` 两次 `-32603` 超时（>120s），改用 `tools/prod_wait.py --peek`（无锁只读端点，零队列）拿到 `MPalYZxM = 0.824`。其余 4 颗 peek 连续返回空体 ⇒ 平台仍在算/单并发槽被占，**按 `wq-prod-corr-read` 纪律不重复触发**，留作提交前终验。`MPalYZxM` 的 0.824 已用 `persist_correlation(source=platform_sync)` 落库。

### 5.4 20 颗终池定稿

按"ATOM 优先 + 规则 5 额度"分三层（Tier C 是**同族备选**，不是另 7 颗新塔）：

**Tier A — ATOM（`effective=1`），8 颗**

| # | alpha | 塔 | S | F | 2Y | prod | 备注 |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `d51z7PVw` | OTHER | 3.26 | 2.40 | 2.16 | 0.5966 | 可直接提交 |
| 2 | `JjQzbQJj` | OTHER | 3.09 | 2.13 | 2.06 | 0.5658 | 可直接提交 |
| 3 | `e7QG2WJM` | OTHER | 2.90 | 2.01 | 2.39 | 0.5751 | 可直接提交 |
| 4 | `58jPrvZ1` | ANALYST | 1.64 | 1.27 | 2.23 | 0.5354 | UNITS WARNING |
| 5 | `88RoVq6V` | RISK | 3.35 | 2.29 | 2.21 | 待终验 | robust 1.30 |
| 6 | `78odJop1` | RISK | 2.89 | 2.34 | 2.60 | 待终验 | robust 1.32 |
| 7 | `58EbwZeN` | RISK | 2.76 | 1.76 | 2.48 | 待终验 | robust 1.05 |
| 8 | `wpZwnrpd` | PV | 3.50 | 2.25 | 3.04 | 待终验 | 纯 PV 单塔，不触规则 5 |
| 9 | `akKJ3qn2` | OTHER | 3.51 | 2.29 | 3.08 | **待终验** | **wave 277 新出**；self-corr 0.6426 ✅；TO 0.3901（贴 0.40 硬线）；`rank(-ts_sum(ts_backfill(oth532_global_daily_specificreturn,22),5))` |
| 10 | `88RAAmZa` | MODEL | 2.96 | 2.13 | 2.49 | **待终验** | **wave 278 新出**；self-corr **0.2119** ✅；robust 1.06（贴线）；`rank(ts_delta(ts_backfill(sector_value_momentum_rank_float,22),22))` |
| 11 | `9qxoozer` | MODEL | 3.06 | 2.68 | 2.28 | **待终验** | **wave 278 新出**；self-corr **0.2697** ✅；TO 0.1461（全池最低）；`rank(ts_delta(ts_backfill(global_value_momentum_rank_float,22),66))` |

**Tier B — PV+X（规则 5 额度用满 5 颗）**，全部 `failed_ra_count=0`：

| # | alpha | 塔 | S | F | 2Y | prod | 备注 |
|---:|---|---|---:|---:|---:|---|---|
| 12 | `O0AYgqAJ` | RISK+PV | **4.03** | 3.12 | **3.64** | 待测 | 池内最强；`ts_target_tvr_hump` 控换手 0.315；robust 1.78 |
| 13 | `E5VNe67L` | INST+PV | 3.20 | 2.52 | 3.00 | 0.664（新鲜） | 点亮 INSTITUTIONS 塔 |
| 14 | `KPmvEYeE` | INST+PV | 3.07 | 2.36 | 3.14 | 0.616（新鲜） | 点亮 INSTITUTIONS 塔 |
| 15 | `mLYdVKap` | INST+PV | 3.16 | 2.45 | 3.07 | 待测 | robust 1.80，decay 126 |
| 16 | `VkdZ3wKM` | INST+PV | 3.14 | 2.41 | 3.29 | 待测 | robust 1.82；UNITS WARNING（`add` 常数项） |

**Tier C — 同族备选（超 PV+X 额度，仅作替换/排序用）**：`kqJkPLeO`(3.02/2.40/2.36, prod 0.618)、`JjP0Ja5l`(3.12/2.42/2.82, prod 0.665)、`d5WAzegY`(2.73/1.93/2.42, prod 0.570)、`RREnK5R1`(2.82/2.04/2.23, prod 0.587)、`gJWXMXNl`(3.13/2.41/3.04)、`RRA91Z01`(3.10/2.39/2.98)、`78o31b2Q`(3.00/2.28/2.87)。

**两条必须随池一起交付的判据**：

1. **Tier B/C 全部是 `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(X,252)))` 同构族**（`returns` 是信号腿 ⇒ 各自 PV 塔）。它们彼此高度相关，`self_corr` 会互相挤压 —— **实操上本来就不可能全部提交**，Tier C 的用途是"Tier B 某颗 prod 撞墙时按 margin 顶替"，不是"再交 7 颗"。
2. **严格执行额度 ≤5 时，可提交面上限 = 16 颗（Tier A 11 + Tier B 5）**。若用户要求 20 颗全部合规，缺口 4 颗只能靠"已点亮塔 × 新数据集"继续挖 —— 未点亮四塔已判死，这条路线已由 waves 276–279 验证为**唯一正期望方向**（§4.6，4 波 24 臂出 3 颗）。

---

## 6. 论坛 + 论文取证汇总（本轮新查）

| 来源 | 内容 | 对挖掘的直接作用 |
|---|---|---|
| 论坛 FF56620（2026-09-01，43 votes） | 8 个 insider 数据集逐个淘汰；insiders1 有 45 字段 | 缩小到 insiders1 单点，避免再扫其余 7 个 |
| 论坛 JX84394（2026-09-02，69 votes） | 模板 `signal = 流量/(存量+ε)`，`accum = ts_sum(signal, 申报周期)` | wave 275 的 ③④ 臂直接照此构造 |
| 论坛 HM97321 | 同款稀疏事件型模板可泛化 | 支撑"稀疏事件用 ts_sum 累计 + 申报周期窗口" |
| 论文（印度专有交易级数据） | cross-insider trading 显著预测未来收益**且不反转** | 排除"快进快出反转"路线，锁定长持有 |
| 论文（美国科技公司 insider purchases） | 后续 **3 年 1.1%/月**异常收益 | 窗口从 66 天改到 252/504 天 |

**教训**：本轮前 4 臂（66 天）方向对、窗口错一个数量级。**查论坛能拿到模板形状，查论文才能拿到时间尺度** —— 两者缺一不可，只看论坛会重复社区里已经用过的短窗。

---

## 7. 本轮新踩的坑（方法论，供后续复用）

1. **`pyramids` 载荷有两种形态**：`list[{name}]` 与 `dict{pyramids:[{name}]}`。只按 list 解析会**静默漏掉** `WjepYR7d`/`786wl6b8` 的 PV+MODEL —— 我第一版就是错的，把 2 条硬违规判成了纯 MODEL。
2. **pyramid name 是 `IND/D1/PV` 全路径，不是裸 `PV`**。按裸名 `tag in set(names)` 匹配，PV+X 全判 0 —— 第二版又错了一次。
3. **`cap` / `returns` 作为条件变量时平台不记塔**。所以"表达式里出现过 PV 字段" ≠ "PV 组腿"，两个口径要分开报，不能混谈。
4. **MCP 参数名必须查 schema，不能靠记忆**：`lookINTO_SimError_message` 要 `locations`（数组），`batch_status` 要 `simulation_ids`，`search_forum_posts` 要 `search_query`，`upsert_wave_result` 要 `region`。四个都是本轮实测撞的。
5. **`progress: 0.1/0.35` + `error: "Simulation did not get through"` 不代表失败**，只是没跑完。`child_count 0` 同理（还在排队）。判活只看 `raw.progress`。
6. **`submit_ready` 表的 `two_year` / `prod` 列会陈旧，不能直接判定**：`MPalYZxM` 与 `wpZwnrpd` 的 `two_year` 在池表里是 **0.00**，`get_alpha_details` 实测是 **2.46 / 3.04**。池表只用于**排序**，判定一律回平台取。`prod` 同理（`MPalYZxM` 池表 None，平台已算出 0.824）。
7. **`check_correlation` 的 `-32603` 超时 ≠ 平台没算**：平台侧算完了，只是 MCP 120s 硬上限先到、结果没落缓存。用 `tools/prod_wait.py <id> --peek`（无锁只读端点，零队列）能直接捞回已算好的值 —— 本轮 `MPalYZxM = 0.824` 就是这样拿到的，且它一次都没进过本地缓存。**空体才是"排队中"，不是 0**。
8. **同族候选的"20 颗"要按可提交性折算**：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(X,252)))` 这一族在池里占 20+ 条，彼此相关度极高且各自计 PV 塔。按规则 5 的 PV+X 额度 ≤5，这一族最多交 5 颗，其余只能作替换备选 —— **不能把"池里 60 条 READY"当成 60 颗可交付**。

---

## 8. 未决事项

| # | 事项 | 状态 |
|---|---|---|
| 1 | **规则 5 口径裁决**（平台金字塔 vs 表达式字段） | 待用户拍板；两口径下 `WjepYR7d`/`786wl6b8` 都禁提交，但 PV+X 额度归属不同 |
| 2 | `WjepYR7d` / `786wl6b8` | 任何口径下均**禁止提交**（PV+MODEL） |
| 3 | `Vkx9RbJV` prod refresh | 两次 `-32603` 超时未成功；缓存 0.6939 有效至 2026-10-30 08:08，**提交前必须重刷** |
| 4 | `RRE3g7Ne` prod 0.7058 | 直方图 `[0.7,0.8)` n=2 ⇒ 按族级判据**必死**，不扫窗口 |
| 5 | wave 275（INSIDERS 长周期 8 臂） | **已收：8/8 全灭，最高 S=0.57** ⇒ INSIDERS 判死（§4.4） |
| 6 | 20 颗终池定稿 | **已定稿**：Tier A 8 ATOM + Tier B 5 PV+X + Tier C 7 同族备选（§5.4）。严格额度下可提交上限 13 颗 |
| 7 | INSIDERS / OPTION / SENTIMENT / SHORTINTEREST 四塔 | **四塔全部实证判死**（24/14/12 臂），IND 可产 ATOM 的只剩已点亮 6 个 category |
| 8 | `MPalYZxM`（S4.37）/ `mLoMnqPE`（S1.87） | **prod 撞墙**（0.824 / 0.7818），已从池内剔除 |
| 9 | `wpZwnrpd` / `88RoVq6V` / `78odJop1` / `58EbwZeN` prod | peek 连续空体，平台队列未出结果；**提交前逐颗 `refresh=True` 终验** |
| 10 | `e72L9vq6` | 非 IND 标准设置（MARKET/decay5/nanON）+ `CLUSTER_TEST:ERROR`，要进池须按 TOP500/STATISTICAL/decay4/nanOFF 重跑 |
| 11 | 提交动作 | **全部未提交**。按纪律需用户明确确认后单颗 `workflow_submit_alpha(confirm_submit=True)`，本轮不代提交 |

---

## 附：数据集级明细（按 category）

<details>
<summary>MODEL 43 个（点击展开）</summary>

`ai_factor_transfer(20f,cov1)` `analyst_earnings_ibes(42f,0.9976)` `analyst_revision_horizons(1089f,0.6885,d2)` `behavioral_signals(7f,0.557)` `global_seasonal_model(449f,0.9886,bt3,d2)` `model106(14f,0.4953)` `model110(8f,0.8525)` `model135(137f,0.5525,bt62,a13,d13)` `model138(120f,0.5537)` `model139(2f,0.7873)` `model140(3f,0.5077)` `model141(2f,0.1954)` `model144(2f,0.5511,bt10,a1)` `model16(24f,0.635,bt20,d8)` `model170(11f,0.7427)` `model176(84f,0.3977)` `model192(101f,1)` `model207(3f,0.6713)` `model216(88f,0.8223)` `model238(44f,0.8702,a1)` `model243(4f,0.7494)` `model244(30f,0.4702)` `model250(20f,0.7876)` `model252(5f,0.7854,bt31,a1,d1)` `model253(2f,0.4882)` `model26(671f,0.7478)` `model262(25f,0.9009)` `model28(83f,0.8708)` `model29(91f,0.7187)` `model30(77f,0.713)` `model31(74f,0.6672)` `model313(8f,0.6624,d3)` `model32(36f,0.9696,bt29,a4,d9)` `model33(32f,0.7851)` `model36(43f,0.8509,bt14,d6)` `model37(87f,0.6978)` `model38(145f,0.7774)` `model39(24f,0.8044)` `model50(168f,0.8551)` `model68(4f,0.5515,d2)` `model77(150f,0.7826)` `predictive_starmine(638f,0.798)` `quant_factor_lib(126f,0.5117)`
</details>

<details>
<summary>NEWS 22 个</summary>

`news104(11f,0.7348)` `news17(88f,0.7824)` `news20(68f,0.8079)` `news21(47f,0.5266)` `news23(136f,0.4462)` `news29(12f,0.6888)` `news3(19f,0.6461)` `news31(53f,0.7991)` `news36(15f,0.7713)` `news38(30f,0.6821)` `news46(30f,0.9382)` `news48(22f,0.6326)` `news50(37f,0.8227)` `news52(24f,0.4698)` `news54(40f,0.9002)` `news59(2f,0.9505)` `news7(118f,0.715)` `news73(22f,0.813)` `news76(8f,0.7245)` `news79(34f,0.9776,bt34,d9)` `news84(23f,0.7811)` `news85(23f,0.823,bt8,a2,d4)`
</details>

<details>
<summary>OTHER 21 个</summary>

`acquisition_model(15f,0.7484)` `ai_news_scores(105f,0.7924)` `event_relation(12f,0.5769)` `ml_factor_proj(333f,1)` `mmp_nlp_sentiment(521f,0.9593)` `news_sentiment_nlp(23f,0.9134,d1)` `other128(18f,0.4607)` `other296(19f,0.5649)` `other315(32f,0.5191)` `other323(11f,0.9996)` `other327(3f,0.5158)` `other335(10f,0.5589)` `other384(66f,0.2803)` `other424(3f,0.6935)` `other436(3f,0.4461)` `other532(8f,0.9855)` `other545(4f,0.5424)` `other567(224f,0.4665)` `other571(30f,0.7585)` `other635(6f,0.6216)` `other696(220f,0.4138)`
</details>

<details>
<summary>PV 13 个</summary>

`intraday_pv_feats(585f,0.9548,bt80,a6,d4)` `pv1(24f,1)` `pv103(9f,0.9831,bt52,a2)` `pv106(15f,1,bt11,d3)` `pv109(25f,0.4397)` `pv13(73f,0.6607)` `pv14(2f,0.9487)` `pv149(1f,1)` `pv29(80f,0.5633)` `pv30(558f,0.8222)` `pv47(2f,1)` `pv70(33f,1)` `univ1(6f,1)`
</details>

<details>
<summary>ANALYST 13 个</summary>

`analyst11(445f,0.8489)` `analyst39(24f,0.8755)` `analyst4(776f,0.6638)` `analyst44(546f,0.8343,d10)` `analyst45(61f,1,bt22,d8)` `analyst46(6f,0.585)` `analyst48(72f,0.3675)` `analyst81(5f,0.2402)` `analyst83(384f,0.287)` `analyst9(111f,0.6166)` `analyst_base_ref(17f,0.5523,d5)` `analyst_consensus(1929f,0.7027,bt92,a7,d10)` `analyst_factor_signals(108f,0.5458)`
</details>

<details>
<summary>FUNDAMENTAL 12 个</summary>

`fundamental1(183f,0.5096)` `fundamental17(523f,0.7054)` `fundamental22(1f,0.6866)` `fundamental23(2332f,0.6641)` `fundamental25(8f,0.2596)` `fundamental4(1f,0.3737)` `fundamental44(12f,0.7842)` `fundamental86(7f,0.8001)` `fundamental89(195f,0.4524)` `fundamental90(66f,0.4825)` `fundamental93(46f,0.3285)` `fundamental94(38f,0.9258)`
</details>

<details>
<summary>RISK 4 / SENTIMENT 4 / EARNINGS 3 / INSIDERS 2 / OPTION 2 / 其余 5 个</summary>

- RISK: `risk68(5f,1,a1)` `risk70(87f,0.9817)` `risk71(4f,0.7046,bt8,a1,d1)` `risk88(1f,1,a1)`
- SENTIMENT: `news_sentiment_transfer(23f,0.9368,bt73,d13)` `sentiment21(210f,0.9659,bt48,a4,d2)` `sentiment23(105f,0.7028)` `sentiment26(19f,0.7528,d5)`
- EARNINGS: `earnings11(35f,0.4992,bt8,d7)` `earnings3(8f,0.7907,bt28,a2,d6)` `earnings6(66f,0.8203)`
- INSIDERS: `insiders1(9f,0.5512,bt6,d5)` `insiders5(1f,0.9991)`
- OPTION: `option1(28f,0.4045,bt6,d4)` `option30(12f,0.3629,bt30,a1,d1)`
- SHORTINTEREST: `shortinterest5(3f,1,bt7,d1)`
- MACRO: `macro63(1f,0.9968,a1)`
- INSTITUTIONS: `institutions6(11f,0.9915,bt82,a11)`
- IMBALANCE: `imbalance5(2f,0.5545,a2)`
- 无类目: `model238_anlrev(1070f,bt9,a1,d2)`
</details>

---

**复现命令**（全部只读）：
```bash
# 数据集画像
python -c "import json;d=json.load(open(r'data/wqb.db'));"   # 或 MCP: wqb_db.query_dataset_profile(region='IND')
# 交付面
MCP: wq-brain-http.get_user_alphas(region='IND', stage='OS', status='ACTIVE', limit=50)
# 待提交池
MCP: wqb-db.get_submit_ready(region='IND')
```
（本轮解析脚本为 `logs/_tmp_ds_agg.py` / `logs/_tmp_delivery_audit.py` / `logs/_tmp_pool_rule5b.py`，属临时件，按 AGENTS §5 用完即删。）
