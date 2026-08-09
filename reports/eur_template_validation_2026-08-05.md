# EUR / ml_factor_proj 论坛模板全量验证报告

> 生成时间：2026-08-05 | 数据集：`ml_factor_proj`（EUR / TOP1200 / D1）
> 设置：neutralization=INDUSTRY, decay=4, truncation=0.08, test_period=P0Y0M, pasteurization=ON
> 队列：e8a(10)→瞬态失败→拆 e10a(5)/e10b(5)；e8b(7)✅；e9(2)→瞬态失败→e11(2)✅；e6a/e6b 因 `ts_entropy` 级联 CANCEL
> 覆盖：论坛 14 个模板中的 **13 个可访问模板**（T13 信念熵因算子不可访问未能验证）

---

## 0. 一句话结论

**期限结构（差异）族 T10 在 EUR/ml_factor_proj 上唯一突破 Power Pool 闸门**：
`T10v_12_1`（`twelve_month` 减 `1m` 的 active_return 行业标准化差）**Sharpe=1.14、Fitness=0.61、TVR=16.1%、回撤=7.0%**，
是 19 条仿真中唯一 Sharpe≥1.0 的模板。其余族（估值/反转/预期质量）在该数据集上信号微弱（|Sharpe|≤0.54）。

---

## 1. 全模板结果表（按 Sharpe 降序）

| 模板 | 族 | 映射后的表达式（节选） | Sharpe | Fit | TVR | 状态 |
|---|---|---|---|---|---|---|
| **T10v_12_1** | 差异/期限结构 | `gz(sub(gz(chg_twelve_month_active_return,ind), gz(chg_1m_active_return,ind)),ind)` | **1.14** | 0.61 | 16.1% | ✅ **过 PP Sharpe 闸** |
| T14_semivar | 信息论/半方差 | `-ts_std_dev(change_1m_active_return, 30)` | 0.54 | 0.28 | 8.9% | 接近 |
| T1v_cf | 反转/Delta | `-ts_delta(change_3y_cashflow_to_price, 66)` | 0.50 | 0.22 | 13.7% | |
| T10_term | 差异/期限结构 | `gz(sub(gz(chg_60m_active_return,ind), gz(chg_1m_active_return,ind)),ind)` | 0.43 | 0.14 | 14.5% | |
| T10v_60_3 | 差异/期限结构 | `gz(sub(gz(chg_60m,ind), gz(chg_3m,ind)),ind)` | 0.23 | 0.06 | 12.0% | |
| T12_qual2 | 差异/预期质量 | `if_else(greater(chg_3m_revision_fy2_eps,0), ts_rank(chg_dispersion...,60),0)` | 0.14 | 0.02 | 17.3% | |
| T6_eymom | 估值/盈利收益率动量 | `group_rank(ts_rank(change_1y_eps_to_price,60), industry)` | 0.10 | 0.01 | 23.1% | |
| T7v_divpeg | 估值/PEG(除法) | `-group_zscore(divide(chg_1y_eps_to_price, chg_1y_eps_growth), ind)` | 0.06 | 0.00 | 42.1% | ⚠ TVR 过高 |
| T7_peg | 估值/PEG(减法) | `-group_zscore(subtract(chg_1y_eps_to_price, chg_1y_eps_growth), ind)` | 0.04 | 0.00 | 7.4% | |
| T15_vol | 情绪/量稳 | `-ts_std_dev(change_20d_volume_to_price_volatility, 10)` | -0.00 | -0.00 | 23.7% | ≈0 |
| T3_opearn | 反转/盈利动能 | `ts_rank(change_1y_eps_growth, 252)` | -0.05 | -0.00 | 13.6% | |
| T5_base | 估值/基础排名 | `group_rank(ts_rank(change_1y_eps_growth,252), industry)` | -0.04 | -0.00 | 15.4% | ≈0 |
| T11_dupont | 差异/杜邦 | `gz(sub(ts_zscore(chg_1y_eps_growth,250), ts_zscore(chg_3y_cashflow_to_price,250)), ind)` | -0.14 | -0.02 | 13.7% | |
| T12_qual | 差异/预期质量 | `if_else(greater(abs(chg_dispersion...),0.001), ts_scale(chg_3m_revision_fy2_eps,60),0)` | -0.13 | -0.02 | 16.0% | |
| T2v_mom | 反转/小而稳 | `-change_fama_french_momentum * ts_std_dev(change_fama_french_momentum,30)` | -0.08 | -0.01 | 16.0% | |
| T2_small | 反转/小而稳 | `-change_1y_eps_growth * ts_std_dev(change_1y_eps_growth,30)` | -0.49 | -0.21 | 11.2% | |
| T1_drev | 反转/Delta | `-ts_delta(change_1y_eps_growth, 66)` | -0.36 | -0.09 | 15.6% | |
| T10v_24_9 | 差异/期限结构 | `gz(sub(gz(chg_24m,ind), gz(chg_9m,ind)),ind)` | -0.21 | -0.05 | 10.9% | |
| T10v_36_6 | 差异/期限结构 | `gz(sub(gz(chg_36m,ind), gz(chg_6m,ind)),ind)` | -0.62 | -0.26 | 13.0% | |
| T13_entropy | 信息论/信念熵 | `signed_power(ts_entropy(field,144), 0.618)` | — | — | — | ⛔ **算子不可访问** |

> 字段缩写：`gz`=group_zscore，`chg_*_active_return`=ml_factor_proj 的 10 窗口 active_return 族，`sub`=subtract。

---

## 2. 按族的判定

| 族 | 最佳 Sharpe | 判定 | 说明 |
|---|---|---|---|
| **差异/期限结构 (T10)** | **1.14** | ★★★ 推荐 | 唯一过 PP 闸门；窗口对敏感（见 §3） |
| 信息论/半方差 (T14) | 0.54 | ★★☆ 可保留 | active_return 波动率反转，中性偏正 |
| 反转/Delta (T1) | 0.50 (cashflow) / -0.36 (eps) | ★★☆ 看字段 | 字段选择决定正负；cashflow 变化方向有效 |
| 差异/预期质量 (T12) | 0.14 | ★☆☆ 弱 | 条件算子可用，但信号薄 |
| 估值 (T5/T6/T7/T11) | ≤0.10 | ☆☆☆ 弱 | `change_*` 基本面字段在本数据集截面区分度低 |
| 情绪/量稳 (T15) | ≈0 | ☆☆☆ 无 | 波动率字段无信号 |
| 信息论/信念熵 (T13) | — | ⛔ 阻断 | `ts_entropy` 在本账户/区域 "inaccessible or unknown" |

---

## 3. 关键发现：T10 期限结构极度依赖窗口对

同一「长期减短期 active_return」范式，Sharpe 随窗口跨度剧烈变化：

```
12m − 1m  →  +1.14   ← 唯一过闸，近月 vs 近一年
60m − 1m  →  +0.43
60m − 3m  →  +0.23
24m − 9m  →  -0.21
36m − 6m  →  -0.62   ← 长跨度反而强反转
```

**结论**：该数据集上的信号是**短周期（1m~12m）动量/期限结构效应**，不是长周期宏观差异。
长跨度（36m/24m vs 6m/9m）出现**反向**信号，说明长窗口 active_return 已趋于均值、截面噪音主导。

---

## 4. Power Pool 闸门逐条核对（针对胜出者 T10v_12_1）

| 闸门 | 阈值 | T10v_12_1 | 结论 |
|---|---|---|---|
| Sharpe | ≥ 1.0 | **1.14** | ✅ |
| 唯一 operator 数 | ≤ 8 | 2（group_zscore, subtract） | ✅ |
| 唯一 data field 数 | ≤ 3 |（2 个 active_return 窗口） | ✅ |
| Turnover | 5%~20% | 16.1% | ✅ |
| Power Pool Correlation | < 0.5 | 需提交时计算（暂无同类 PP alpha，预期低） | ⏳ 提交时验证 |
| prod_corr / self_corr | < 0.7 / < 0.5 | 需提交时计算 | ⏳ 提交时验证 |

→ **T10v_12_1 满足可静态核验的全部硬闸门，是进入提交流程的优先候选。**

---

## 5. 操作层教训（对后续挖掘至关重要）

1. **一个 fatal operator 会级联 CANCEL 整个 multisimulation**：e6a/e6b 因 T13 的 `ts_entropy` 报错，**全部 20 条被 CANCEL**，一条有效结果都没拿到。务必把“不确定是否可用”的算子（if_else/ts_entropy 等）**隔离到独立小批次**。
2. **瞬态 "try again" 平台故障会整批命中**：e8a(10)/e9(2) 连报 2 次 "try again"，而同窗口提交的 e8b(7) 全 COMPLETE —— 证明表达式本身合法，是平台抖动。拆成 **5 条/批**（e10a/e10b/e11）后全部成功。
3. **`create_multi_simulation` 要求 ≥2 条表达式**：单条提交会直接报错。
4. **`ts_entropy` 在本账户/区域不可用**（"inaccessible or unknown operator"）—— 论坛高赞的「信念熵」模板（T13, 94 赞）在本环境无法落地，需换数据集或换算子（如用 `ts_std_dev` 近似不确定性）。
5. **MCP 会话串行化**：多个轮询/提交并发会争抢同一 MCP 会话导致响应串台；所有提交与 fetch 必须**串行**执行。

---

## 6. 下一步建议（衔接"挖 3 个 PPA"原目标）

- **已验证的 1 个候选**：`T10v_12_1`（Sharpe 1.14）可直接进入提交闸门（prod_corr/self_corr/PC 校验后 submit，打 `PowerPoolSelected` 标签）。
- **凑齐 3 个去相关 PPA 的两条路**：
  - **(A) 同族深挖**：在 T10 内扫描更多窗口对 + decay（2/4/8）+ neutralization（SUBINDUSTRY/COUNTRY/SECTOR），找 2 个与 T10v_12_1 **互相去相关**（self_corr<0.5）且 Sharpe≥1.0 的变体。风险：同族变体天然高相关，可能 PC>0.5。
  - **(B) 换数据集补另外 2 族**：估值/反转/熵在本数据集弱，但 `news_sentiment_nlp`（valueScore 6.0）、`pattern_scores` 等 EUR 高价值数据集可能让 T6/T13/T15 出信号。建议用 `tools/eur_field_coverage.py` 体检后另开战役。
- **T13 替代方案**：用 `ts_std_dev(change_fama_french_momentum, 120)` 等波动率代理近似"不确定性放大"，替代不可用的 `ts_entropy`。

> 数据资产：`tracking/mining/rows_mlfp_{e8b,e10a,e10b,e11}.json` 含全部 19 条仿真实测指标；`tools/mine_eur_mlfactor.py` 的 `RAW_BATCHES` 已固化上述全部模板映射，可一键复跑。
