# GBR 挖掘经验总结（2026-10-28 轮次）

> 范围：GBR / TOP700 / D1 / REGULAR。目标：点亮未点亮塔（PV 1/3、OTHER 1/3，其余 0/3）。
> 本文只记录**本轮实测到的事实**与由此得出的可复用规则；未验证的推测单独标注。

---

## 0. 一句话结论

**GBR 的瓶颈不是"区域产出弱"，而是 prod 相关性墙。**本轮把 IS 指标推到 S2.15 / F1.11 / 2Y1.85 / SUB1.80 / RA 零失败（历史最佳），但 prod 仍在 0.7343–0.7945 之间，**全部无法提交**。已测的 GBR 所有信号族（≥5 个数据集、≥3 座塔、10+ 个变体）**100% 卡 prod**。

---

## 1. 本地库读数的三个坑（必须先修，否则结论反）

### 1.1 `alphas.region_id` / `universe` 不可信，唯一权威是 `payload_json.settings.region`
本地 `alphas` 表含 15 个 region_id、1.8 万条。查询漏 `WHERE region_id=` 会捞到别的区。
更隐蔽的是**同 dataset 名跨区混行**：按 `dataset` 聚合看到 `fundamental72` maxS=1.84/F1.26/2Y1.58（205 行），像是 FUNDAMENTAL 塔的现成 ATOM 候选；逐条 `get_alpha_details` 才发现 `qM03xKG2` 的 `settings.region=EUR`、`universe=TOPCS1600` —— 是 EUR 的战绩。GBR 本区 `fundamental72` 的判死记录（best 0.55、CW 墙）才成立。

**规则**：任何"某数据集/某塔在本地有高分"的判断，必须逐条 `get_alpha_details` 复核 `settings.region` + `ra.pyramid_short`。

### 1.2 `backtest_results` 没有 `universe` 列
列清单：`id, expression_id, alpha_id, status, sharpe, fitness, turnover, margin, returns, drawdown, two_year_sharpe, sub_universe_sharpe, long_count, short_count, pnl, book_size, ra_failed_checks, created_at, region, wave, dataset, code, payload_json, risk_neutralized_sharpe`。
表达式字段叫 **`code`**（不叫 expression）。universe 只在 `payload_json` 里。
`payload_json` 解析时注意 `settings` 可能是 **str** 而非 dict，必须先 `isinstance` 判断。

### 1.3 本地 `dataset` 列 ≠ 平台塔位
`backtest_results.dataset` 是**本地组合集分组名**。反例：GBR `shortinterest3` 分组下最高分 `KPrmWlwN`（S1.62/2Y1.89/failed_ra_count=0）表达式只有 `pv47_spret` 单字段，`pyramid_short=pv` —— **属 PV 塔，不是 SHORTINTEREST 塔**；反过来 shortinterest3 真字段实测最高只有 S0.80。

**塔位唯一权威 = `get_alpha_details` 的 `ra.pyramid_short` 与 `pyramids.list`。`get_datasets` 的 category 也不等于塔位。**

---

## 2. 修正"GBR 产出弱"的错误结论

按 `payload_json.settings.region=="GBR"` 过滤得 **496 行**，其中 S≥1.58 且 F≥1.0 共 **33 条**。

**但这 33 条全部落在已满的 MODEL 塔**（model109 估值族 / `ep_yield_pct_smest_f12m` / `forward_pe_mean_f12m` / `tm_16`），对点亮 PV / OTHER / FUNDAMENTAL 无直接帮助。

⇒ 此前的"GBR 弱"判断由三重错误叠加造成：① 本地库跨区污染 ② 字段选错 ③ 形状选错。**区域不是瓶颈，字段+形状才是**；但**塔层错配**才是真正卡住点塔的结构问题。

---

## 3. GBR 已验证形状配方（本轮最重要的可复用资产）

```
形状甲（低换手 TO 0.10-0.27）：group_rank(ts_av_diff(ts_backfill(F, W1), W2), industry|subindustry)
形状乙（hump 限速 TO 0.10）：  hump(group_rank(ts_delta(ts_backfill(F, 132), 22), sector), hump=0.0012)
配套设置：decay 12 / INDUSTRY 或 SUBINDUSTRY / truncation 0.10 / nanHandling OFF / maxTrade OFF
```

### 3.1 hump 阈值必须与信号量级匹配（硬规则）
`group_rank` 输出在 **[0,1]**，所以 `hump=0.0012` 合理。把同一数值用在量级大得多的 `group_neutralize(group_scale(signed_power(rank(F),1.5)))` 上，`hump=0.006` 会把 S 从 1.73 打到 **0.09**（`WjO8zxOo`，灭 94% 收益）。

### 3.2 形状对任何字段都能降 TO，但 F 的上限由字段决定
`leAX9Rj2`（`v_shape_reversal` + 已验证形状）TO 0.1248 —— 形状确实把换手压到 0.125，但 S 只有 −1.06（翻正仅 1.06）。
⇒ **形状只解决换手这一半，信号强度必须来自字段。**

### 3.3 形状是字段特异的，不能无脑移植
把形状乙（`ts_delta`+`sector`+`hump`）从 `region_relative_valuation_rank`（慢变估值，S2.34/F2.28/2Y1.85）移植到 `tm_17`（快变技术指标）→ **S 0.85 / F 0.34 / 2Y 0.40**（`d5WLvk82`）。
⇒ 慢变结构化分数适合 `ts_delta`+`hump`；快变指标适合 `ts_av_diff`+`group_rank`。

---

## 4. fitness 公式与降换手杠杆（论坛证实）

论坛 `43583631005719`《机理拆解：换手率是隐形天花板》给出：

```
fitness = sharpe × sqrt(ret / max(tvr, 0.125))
```

- **降换手杠杆实测排序：源平滑（ts_mean / decay） > hump > 拉长持有周期语义**
- **`decay` 12 / 16 / 20 输出可逐位相同 ⇒ decay 轴已饱和**，别浪费批槽
- 警告：`hump` 会滤掉小信号造成覆盖损失；"换手=信号本体"的信号族与低换手门槛**结构性互斥**
- 反解示例：`JjeKzgq2`（S1.60/ret5.18%/tvr0.1749）要 F≥1.0 需 `tvr ≤ 0.129` **且** ret 保持 ≥5.18%，单靠 hump 达不到

---

## 5. 字段拥挤度（GBR/TOP700/D1 精确 search 实测）

| 字段 | 数据集 | alphaCount | userCount |
|---|---|---|---|
| `tm_16_r1_r5_r10_rh_glb_d1_r10_q1` | techindi_model | **7579** | 512 |
| `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` | techindi_model | 281 | 131 |
| `tm_15_..._d10_q1` | techindi_model | 471 | 223 |
| `tm_17_..._ah3_d10_q1` | techindi_model | 471 | 214 |
| `tm_8_..._d10_q1` | techindi_model | 432 | 198 |
| `tm_19_..._ah3_d10_q1` | techindi_model | 370 | 169 |
| `tm_18_..._ah3_d5_q1` | techindi_model | 185 | 66 |
| `tm_18_..._ah3_d10_q1` | techindi_model | 85 | 58 |

⇒ **同一模型不同期限拥挤度差 27 倍**（tm_16 r10 7579 vs r5 281）。

### 5.1 a-S 同向律（并延伸到 prod）
低拥挤 = 低信号。`tm_18_r10`（a=85）实测 S 只有 **0.67**（`O0AaVvvY`）。
⇒ 想换低拥挤字段降 prod，会同时把信号打掉。**这不是可选菜单，是同一根轴的两端。**

---

## 6. 降 prod 的尝试与"钉死"判据

### 6.1 四条路全败
| 手法 | 实例 | 结果 |
|---|---|---|
| 换 hump 阈值 | 0.002 → 0.006 | 信号灭（S0.09） |
| 残差化（对同族做 `ts_regression`） | tm_17 对 tm_16_r5 | 两模型近共线，残差只是噪声（S0.88/F0.28） |
| 换 decay / 中性化 | decay10 + INDUSTRY | TO 降了但 S 降更多（1.73→1.46） |
| 降拥挤度换字段 | tm_18_r10（a=85） | S0.67 |

### 6.2 ★ "钉死"判据（来自 `wq-window-valley-break-prod-wall`，本轮正面撞上）
查候选 prod 直方图 **`[0.7, 0.8)` 桶的 n 值**：
- **n = 0** ⇒ 该族存在过线窗口，值得扫窗口网格
- **n ≥ 1** ⇒ 单钉子卡死，无论怎么调都过不了

本轮实测：
| 候选 | prod | n([0.7,0.8)) | 判定 |
|---|---|---|---|
| `npvVQ8WE` | 0.7343 | **5** | 钉死 |
| `88R1XNo7` | 0.7736 | **4** | 钉死 |
| `rKRX8Jd1` | 0.7919 | **3** | 钉死 |
| `3qoLJb16` | 0.7945 | **3** | 钉死 |

### 6.3 ★★ 窗口轴（W2）同时驱动 2Y 与 prod，且方向相反 ⇒ 无谷
固定 `F = tm_17_..._ah3_d10_q1`、`ts_backfill(...,126)`，只改 `ts_av_diff` 的 W2：

| 变体 | W2 | 分组轴 | 中性化 | S | F | 2Y | SUB | prod | n_fail |
|---|---|---|---|---|---|---|---|---|---|
| `npvVQ8WE` | 40 | industry | INDUSTRY | 2.02 | 1.06 | **1.36** | 1.59 | **0.7343** | 1 |
| `3qoLJb16` | 22 | subindustry | SUBINDUSTRY | 2.13 | 1.05 | **1.75** | 1.75 | **0.7945** | 0 |
| `rKRX8Jd1` | 22 | subindustry | INDUSTRY | 2.13 | 1.05 | 1.73 | 1.73 | 0.7919 | 0 |
| `88R1XNo7` | 22 | industry | SUBINDUSTRY | **2.15** | **1.11** | **1.85** | **1.80** | 0.7736 | **0** |

**读法**：
1. **W2 是 2Y 的开关**：40 → 1.36（FAIL）；22 → 1.73~1.85（PASS）。**中性化与分组轴对 2Y 几乎无影响**（1.75 vs 1.73）。
2. **W2 也是 prod 的开关，但方向相反**：22 时 prod 0.77-0.79，40 时 0.73。**沿 W2 轴 2Y 与 prod 单调对立，不存在同时满足的谷。**
3. `88R1XNo7` 是全场 IS 最佳（S2.15/F1.11/2Y1.85/SUB1.80/RA 零失败），仍因 prod 0.7736 无法提交。

### 6.4 2Y 的直接归因：单一年份 2023
`npvVQ8WE` 逐年（W2=40 版）：
2014 2.01 / 2015 2.32 / 2016 2.36 / 2017 2.40 / 2018 3.56 / 2019 1.77 / 2020 2.70 / 2021 1.12 / **2022 2.61** / **2023 −0.14**（ret −0.45%）。

**2023 单年把 2Y 从 ~1.85 拉到 1.36。**持仓数 2023 为 399/415，健康 ⇒ 是 **regime 切换问题，不是数据覆盖问题**。
⇒ 任何 GBR 候选卡 `LOW_2Y_SHARPE` 时，先跑 `get_alpha_yearly_stats` 看是否单年崩塌；若是，先试缩短响应窗口（W2→22）而不是换字段。

---

## 7. OTHER 塔的结构性真相（本轮最有用的塔层发现）

`recommend_datasets` + `pyramid_summary` 给出 GBR 权威塔层表：

| 塔 | 现有 | 还需 | 倍率 |
|---|---|---|---|
| **sentiment** | 0 | 3 | **1.7**（最高） |
| news / fundamental / other / pv | 0 / 0 / **1** / **1** | 3 / 3 / **2** / **2** | 1.6 |
| insiders / option / model(已亮) | 0 | 3 | 1.5 |
| institutions | 0 | 3 | 1.4 |
| analyst(已亮) | 3 | 0 | 1.6 |
| earnings / risk / socialmedia / macro | 0 | 3 | 1.3 / 1.3 / 1.3 / 1.3 |

**关键**：`other` 塔只有 **3 个数据集** —— `techindi_model`（已用，即 tm_17）、`acquisition_model`、`dl_riskfree_returns`。
⇒ 要点亮 OTHER，必须用后两个各产 1 颗。这同时天然满足"同塔 N 颗须来自不同数据集的信号腿"（否则互相关超阈）这一结构约束。

**`pv` 塔还需 2 颗**；`fundamental` 有 **12 个数据集**可选（`fundamental72` 552 字段 / `fundamental6` 197 / `fundamental17` 135 / `fundamental93` 17 / `fundamental89` 42 / `fundamental1` 124 / `digital_ad_spend` 6 等）。

---

## 8. 低拥挤 ≠ 可用：`alpha_factor_lib` 是真空集

`alpha_factor_lib`（Equity Alpha Factor Library，82 个 VECTOR 字段，u24/a34，拥挤度只有 model109 的约 1/200）看起来是理想盲区。实测：

- 82 个字段 **全部 `coverage = 0.0`**
- `group_rank(ts_av_diff(ts_backfill(vec_avg(free_cash_flow_to_market_cap),126),40), industry)` ⇒ **`longCount=4` / `shortCount=4`**，全市场只有 4 多 4 空，DD 50%，CONCENTRATED_WEIGHT 0.5 FAIL
- `change_free_cash_flow_to_market_cap` 同批：S0.09

⇒ **`coverage=0` 有两种情况，必须区分**：① meta 造假（earnings6 / news48 / option1 / analyst45 / macro27 属此类，字段真实存在）② **真空集**（`alpha_factor_lib` 属此类）。判据只有一个：**跑一条仿真看 `longCount`**，不要用平台 coverage 或 alphaCount 判断。

---

## 9. `acquisition_model` 有真数据，但形状要用"水平"而非"差分"

`acquisition_model`（15 个 VECTOR 字段，a15-624 / u9-298）分两类：
- **M&A 目标可能性**：`global/region/industry/sector/country_percentile_acquisition_likelihood`（a18-32，最低拥挤）
- **构成分项**：`valuation / company_size / credit_quality / fundamental_factor / text_factor` 的 global 与 region 百分位

实测（GBR/TOP700/D1，decay12/SUBINDUSTRY/trunc0.1/nanOFF/maxTradeOFF）：
| 形态 | 表达式 | S | F | 2Y | SUB | longCount | 塔位 |
|---|---|---|---|---|---|---|---|
| **差分** | `group_rank(ts_av_diff(ts_backfill(vec_avg(global_percentile_acquisition_likelihood),126),22), subindustry)` | 0.78 | 0.37 | −0.02 | 0.28 | **216** | **other ✓** |
| 差分（文本因子） | 同上换 `global_text_factor_percentile_rank` | −0.14 | −0.03 | −0.63 | −0.13 | — | other |

⇒ **`longCount=216` 证明数据是真的**（不像 alpha_factor_lib 的 4）。但 `ts_av_diff` 扣掉了水平值 = 扣掉了 M&A 目标溢价本身（水平效应），只剩噪声。
⇒ **待验证假设**：M&A 机制应按**水平**建模（Cremers-Nair-John 2009：高收购概率 → 高预期收益），即 `group_rank(ts_backfill(vec_avg(F), 22), subindustry)`。

---

## 10. `dl_riskfree_returns`：133 个 ML 分位预测字段

字段命名 `probability_label{K}_{N}quantile_{D}day_{feature}`，`_ohlcv` 变体 coverage=1.0。
结构上天然适合 **log-odds 多空**：同一期限、同一分位桶的 `label_top − label_0` = 上下行概率对数比。这是合规形态（非混信号）。

实测 `group_rank(ts_backfill(subtract(probability_label1_2quantile_5day_ohlcv, probability_label0_2quantile_5day_ohlcv), 5), subindustry)` ⇒ **S0.92 / F0.44 / 2Y0.05 / SUB0.89 / TO0.1315**（`rKRXn1Z9`）—— 偏弱，但 coverage 健康。

---

## 11. 其它工程教训

1. **`progress=0.35` 不是卡死信号**。`lookINTO_SimError_message` 报 `progress:0.35` 的仿真，过几分钟可能已是 `status=COMPLETE`。**不要据此判孤儿**——直接 `GET /simulations/{id}` 看 `status`/`alpha`。本轮曾误判 2 条为孤儿（实际都跑完了）。
2. **`batch_create_simulations` 才按参数落 `maxTrade`**；`create_multi_simulation` 会静默丢弃 `maxTrade`（传 ON 实际仍为 OFF），必须读回 `settings.maxTrade` 复核。
3. **`mcp__wq-brain-http__get_datafields` 的 `data_type="MATRIX"` 会漏掉纯 VECTOR 数据集**（`alpha_factor_lib` 82 字段全 VECTOR，MATRIX 查询返回 0）。`filter_sharpe=true` 对无 OS/IS Sharpe 数据的字段集不生效（返回 `sharpe_filter_applied: false`）。
4. **单位校验**：`unit_handling=VERIFY` 下不能给带单位字段加无量纲常数（`add(total_top_buy_shares, 0.0001)` 整条 WARNING 失败）。比值一律同单位相除。
5. **平台 prod 计算是账号级单并发**，批量候选不要并发触发，也不要反复 `refresh=True`（会把自己的队列重排死）。顺序：`refresh=False`（48h 缓存）→ 平台已算好的 `is.prodCorrelation` → 才回源，且只回一次。

---

## 12. 下一步建议（按期望收益排序）

1. **OTHER 塔**：`acquisition_model` 水平形态（M1/M2 在飞）+ `dl_riskfree_returns` 换期限/换分位桶。这两条是 OTHER 塔唯一剩余弹药。
2. **FUNDAMENTAL 塔**（12 数据集、倍率 1.6、0/3）：优先 `fundamental1`(u40/a69) / `fundamental89`(u8/a13) / `fundamental6`(u197) / `fundamental17`(u135)。注意 `fundamental72` 以**原始资产负债表行项目**为主（VECTOR/MATRIX 混杂、需自己做同单位比值）。
3. **sentiment 塔**（倍率 1.7 最高）：完全未探，`sentiment27`（790 alphas）是最大集。
4. **不要再在 tm_ / techindi_model 族上花槽**：IS 已到顶（S2.15/F1.11/2Y1.85），prod 结构性钉死（n=3~5）。
