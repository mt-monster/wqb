# EUR 区域 PPA 挖掘完整报告（ml_factor_proj）

> 合并自三份原始报告：`eur_field_coverage_2026-08-05.md`（字段覆盖率核查）、`eur_ppa_mining_2026-08-05.md`（数据集选型）、`eur_template_validation_2026-08-05.md`（论坛模板全量验证）。
> 区域/池/延迟：EUR / TOP1200 / delay=1｜目标数据集：`ml_factor_proj`｜目标：挖掘可提交 PPA（Power Pool Alpha）。

---

## 一、核心结论（撤回"EUR 死路"旧判断）

此前"EUR 死路 / 数据包过期"的判断**错误，需撤回**。EUR 战役失败的真实根因不是平台无数据，而是**数据集选择错误**：32 次回测全部消耗在 4 个低覆盖或高拥挤的劣质数据集上，而平台同期提供 **178 个数据集 / 38,609 个字段**，其中 19 个满足"高覆盖 + 未拥挤"条件的数据集**从未被触碰**，7 个 alphaCount 为 0（零竞争）。

> 旧结论 `tracking/mining/eur_track_conclusion.json` 的死路判定应撤回，以 `eur_track_conclusion_revised.json` 为准。

---

## 二、平台实况与数据集体检

**EUR 平台整体指标**（EQUITY / EUR / delay=1 / TOP1200）：

| 指标 | 数值 |
|---|---|
| 可用数据集 | 178 |
| 可用字段总数 | 38,609 |
| coverage 均值 / 中位数 | 0.6616 / 0.6657 |
| coverage ≥ 0.90 | 35 个 |
| coverage 0.70–0.90 | 43 个 |
| coverage < 0.70 | 100 个 |

类别分布：model 49、other 37、pv 20、news 20、analyst 16、fundamental 14，其余为 sentiment/risk/insiders/earnings/institutions/macro/socialmedia/imbalance。

**原战役用过的 4 个数据集——事后体检**（无一满足 coverage ≥ 0.85，sharpe 天花板 0.72 是选择的直接后果）：

| 数据集 | coverage | 字段数 | 用户数 | alpha 数 | 金字塔倍率 | 判定 |
|---|---|---|---|---|---|---|
| model30 | 0.713 | 77 | 174 | **4202** | 1.3 | 极度拥挤，prod_corr 几乎必然超标 |
| pv20 | 0.6915 | 1475 | 28 | 65 | **1.1** | 覆盖率偏低 + 最低倍率 |
| news21 | **0.5266** | 47 | 8 | 9 | 1.3 | 近半标的无数据，高 tvr 是必然结果 |
| insiders12 | **0.2008** | 8 | 11 | 15 | 1.2 | 覆盖率 20%，结构性不可用 |

**关于"平台 0 字段"的误判**：原结论称 `fundamental86 / risk59 / model216 / fundamental94` 在平台上 0 字段，归因于数据包过期。实测——这四个数据集在 **EUR 区域根本不提供**（不是 0 字段，是不存在）；但它们在 **KOR 区域全部可用**（如 `fundamental94` 有 215 字段、coverage 0.8558）。这是**跨区域误推荐**，与数据包新鲜度无关。

---

## 三、EUR 未开发机会排行（coverage ≥ 0.85 / alphaCount ≤ 50 / 字段 ≥ 10）

| 数据集 | coverage | 字段 | 用户 | alpha | valueScore | 倍率 | 类别 |
|---|---|---|---|---|---|---|---|
| **ml_factor_proj** | **1.0** | 333 | 0 | **0** | 5.0 | **1.5** | other |
| **news_sentiment_nlp** | 0.9134 | 23 | 0 | **0** | **6.0** | **1.5** | other |
| dl_riskfree_returns | 0.9429 | 133 | 6 | 14 | 4.0 | **1.5** | other |
| ai_factor_transfer | 1.0 | 20 | 0 | **0** | 4.0 | 1.3 | model |
| global_seasonal_model | 0.9886 | 449 | 0 | **0** | 5.0 | 1.3 | model |
| analyst_earnings_ibes | 0.9976 | 42 | 1 | 1 | 5.0 | 1.3 | model |
| price_signal_dl | 0.9729 | 28 | 1 | 2 | 5.0 | 1.3 | model |
| ai_equity_alpha | 0.8601 | 582 | 2 | 2 | 5.0 | 1.3 | model |
| model354 | 1.0 | 236 | 5 | 7 | 4.0 | 1.3 | model |
| continuation_score | 0.9924 | 560 | 0 | **0** | 5.0 | 1.1 | pv |
| pattern_scores | 0.9924 | 504 | 0 | **0** | 5.0 | 1.1 | pv |
| intraday_pv_feats | 0.9548 | 585 | 1 | 1 | 4.0 | 1.1 | pv |

（完整 19 条见 `tracking/mining/field_coverage_EUR_d1_TOP1200.json`）

**字段级下钻：ml_factor_proj** — 333 个字段全部为 `MATRIX` 类型，**coverage 全为 1.0**（mean = median = min = max = 1.0000），全部 userCount=0 / alphaCount=0。字段命名标准因子变化率语义（`change_1y_eps_growth`、`change_12m_alpha`、`change_20d_volume_to_price_volatility` 等），可直接套用现有 PPA 模板。满覆盖、零竞争、1.5 倍金字塔，优先级最高。

字段结构（333 个）：`change_*` 基本面/价量变化率 243 个；`mean_global_feature_0..39` 40 个（ML 潜因子均值）；`log_variance_global_feature_0..39` 40 个（ML 潜因子对数方差）；`change_*_active_return` 期限结构族 10 个窗口（1m/2m/3m/6m/9m/12m/18m/24m/36m/60m）。

---

## 四、跨区域附带发现：KOR 优先级高于 EUR

同步拉取 KOR/TOP600/D1（192 个数据集，coverage 均值 0.7046，高于 EUR 的 0.6616）。同一批优质数据集在两区收益参数差异显著：

| 数据集 | EUR 倍率 / valueScore | KOR 倍率 / valueScore |
|---|---|---|
| ml_factor_proj | 1.5 / 5.0 | **1.7 / 6.0** |
| ai_factor_transfer | 1.3 / 4.0 | **1.7 / 6.0** |
| analyst_earnings_ibes | 1.3 / 5.0 | **1.7 / 6.0** |
| price_signal_dl | 1.3 / 5.0 | **1.7 / 6.0** |

KOR 的 `ml_factor_proj` 仍只有 10 个 alpha，同样未饱和。若以金字塔收益为目标函数，**KOR 应排在 EUR 之前**。

---

## 五、数据集选型依据：为什么是 ml_factor_proj

按 `wq-brain-ppa-mining` skill §1.0 前置硬门槛（coverage≥0.85、alphaCount≤50、fieldCount≥10）在 EUR/TOP1200/delay=1 的 178 个数据集中筛选，`ml_factor_proj` 各项最优：

| 指标 | 值 | 门槛 | 判定 |
|---|---|---|---|
| coverage | 1.00 | ≥0.85 | ✅ 满分 |
| fieldCount | 333 | ≥10 | ✅ |
| alphaCount | 0 | ≤50 | ✅ 完全未开发 |
| userCount | 0 | — | ✅ 零竞争 |
| valueScore | 5.0 | — | 中上 |
| pyramidMultiplier | 1.5 | — | EUR 区最高档 |

---

## 六、论坛模板全量验证（EUR / ml_factor_proj）

> 设置：neutralization=INDUSTRY, decay=4, truncation=0.08, test_period=P0Y0M, pasteurization=ON。
> 队列：e8a(10)→瞬态失败→拆 e10a(5)/e10b(5)；e8b(7)✅；e9(2)→瞬态失败→e11(2)✅；e6a/e6b 因 `ts_entropy` 级联 CANCEL。
> 覆盖：论坛 14 个模板中的 **13 个可访问模板**（T13 信念熵因算子不可访问未能验证）。

### 一句话结论

**期限结构（差异）族 T10 在 EUR/ml_factor_proj 上唯一突破 Power Pool 闸门**：`T10v_12_1`（`twelve_month` 减 `1m` 的 active_return 行业标准化差）**Sharpe=1.14、Fitness=0.61、TVR=16.1%、回撤=7.0%**，是 19 条仿真中唯一 Sharpe≥1.0 的模板。其余族（估值/反转/预期质量）在该数据集上信号微弱（|Sharpe|≤0.54）。

### 全模板结果表（按 Sharpe 降序）

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

### 按族判定

| 族 | 最佳 Sharpe | 判定 | 说明 |
|---|---|---|---|
| **差异/期限结构 (T10)** | **1.14** | ★★★ 推荐 | 唯一过 PP 闸门；窗口对敏感（见下） |
| 信息论/半方差 (T14) | 0.54 | ★★☆ 可保留 | active_return 波动率反转，中性偏正 |
| 反转/Delta (T1) | 0.50 (cashflow) / -0.36 (eps) | ★★☆ 看字段 | 字段选择决定正负；cashflow 变化方向有效 |
| 差异/预期质量 (T12) | 0.14 | ★☆☆ 弱 | 条件算子可用，但信号薄 |
| 估值 (T5/T6/T7/T11) | ≤0.10 | ☆☆☆ 弱 | `change_*` 基本面字段在本数据集截面区分度低 |
| 情绪/量稳 (T15) | ≈0 | ☆☆☆ 无 | 波动率字段无信号 |
| 信息论/信念熵 (T13) | — | ⛔ 阻断 | `ts_entropy` 在本账户/区域 "inaccessible or unknown" |

### 关键发现：T10 期限结构极度依赖窗口对

同一「长期减短期 active_return」范式，Sharpe 随窗口跨度剧烈变化：

```
12m − 1m  →  +1.14   ← 唯一过闸，近月 vs 近一年
60m − 1m  →  +0.43
60m − 3m  →  +0.23
24m − 9m  →  -0.21
36m − 6m  →  -0.62   ← 长跨度反而强反转
```

**结论**：该数据集上的信号是**短周期（1m~12m）动量/期限结构效应**，不是长周期宏观差异。长跨度（36m/24m vs 6m/9m）出现**反向**信号，说明长窗口 active_return 已趋于均值、截面噪音主导。

### Power Pool 闸门逐条核对（针对胜出者 T10v_12_1）

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

## 七、操作层教训（对后续挖掘至关重要）

1. **一个 fatal operator 会级联 CANCEL 整个 multisimulation**：e6a/e6b 因 T13 的 `ts_entropy` 报错，**全部 20 条被 CANCEL**，一条有效结果都没拿到。务必把"不确定是否可用"的算子（if_else/ts_entropy 等）**隔离到独立小批次**。
2. **瞬态 "try again" 平台故障会整批命中**：e8a(10)/e9(2) 连报 2 次 "try again"，而同窗口提交的 e8b(7) 全 COMPLETE —— 证明表达式本身合法，是平台抖动。拆成 **5 条/批**（e10a/e10b/e11）后全部成功。
3. **`create_multi_simulation` 要求 ≥2 条表达式**：单条提交会直接报错。
4. **`ts_entropy` 在本账户/区域不可用**（"inaccessible or unknown operator"）—— 论坛高赞的「信念熵」模板（T13, 94 赞）在本环境无法落地，需换数据集或换算子（如用 `ts_std_dev` 近似不确定性）。
5. **MCP 会话串行化**：多个轮询/提交并发会争抢同一 MCP 会话导致响应串台；所有提交与 fetch 必须**串行**执行。

---

## 八、下一步建议（衔接"挖 3 个 PPA"原目标）

- **已验证的 1 个候选**：`T10v_12_1`（Sharpe 1.14）可直接进入提交闸门（prod_corr/self_corr/PC 校验后 submit，打 `PowerPoolSelected` 标签）。
- **凑齐 3 个去相关 PPA 的两条路**：
  - **(A) 同族深挖**：在 T10 内扫描更多窗口对 + decay（2/4/8）+ neutralization（SUBINDUSTRY/COUNTRY/SECTOR），找 2 个与 T10v_12_1 **互相去相关**（self_corr<0.5）且 Sharpe≥1.0 的变体。风险：同族变体天然高相关，可能 PC>0.5。
  - **(B) 换数据集补另外 2 族**：估值/反转/熵在本数据集弱，但 `news_sentiment_nlp`（valueScore 6.0）、`pattern_scores` 等 EUR 高价值数据集可能让 T6/T13/T15 出信号。建议用 `tools/eur_field_coverage.py` 体检后另开战役。
- **T13 替代方案**：用 `ts_std_dev(change_fama_french_momentum, 120)` 等波动率代理近似"不确定性放大"，替代不可用的 `ts_entropy`。

---

## 九、工具与行动建议

**工具 `tools/eur_field_coverage.py`**：零第三方依赖（仅标准库），双通道设计——
- **MCP 通道（默认）**：复用常驻 `world-quant-brain-mcp` 服务（`127.0.0.1:8876`）已建立的稳定会话，规避沙箱到 `api.worldquantbrain.com` 的 TLS 抖动。
- **直连通道（`--mode direct`）**：用 `.env` 凭据自行 Basic Auth，对 429/5xx 与链路异常做指数退避重试。

```bash
python tools/eur_field_coverage.py --region EUR --delay 1 --universe TOP1200          # 数据集级覆盖率
python tools/eur_field_coverage.py --region EUR --universe TOP1200 --dataset-fields ml_factor_proj  # 字段级下钻
python tools/eur_field_coverage.py --region KOR --universe TOP600 --mode direct         # 换区域/走直连
```

EUR 合法 universe 白名单：`TOP2500 / TOP1200 / TOP800 / TOP400 / TOPCS1600 / ILLIQUID_MINVOL1M`。

**API 实测约束（踩坑）**：① `GET /data-fields` 必须 `instrumentType + region + delay + universe` 四者齐全；② `universe` 传非法档位 → 500（非 400）；③ `get_datasets` 直接返回 `coverage/fieldCount/userCount/alphaCount/valueScore/pyramidMultiplier`，比逐字段聚合快约两个数量级；④ 直连 API 的 `category` 是 dict，MCP 返回的是 str，需归一化。

**总体行动建议**：
1. 撤回死路结论，以 `eur_track_conclusion_revised.json` 为准。
2. 建立开战役前置门槛：coverage≥0.85、alphaCount≤50、fieldCount≥10，不达标不消耗回测配额（EUR 战役前若执行可直接避免 32 次无效回测）。
3. 重开 EUR 战役，起点 `ml_factor_proj` → `news_sentiment_nlp`（valueScore 6.0）→ `global_seasonal_model`。
4. **优先考虑 KOR**：相同数据集倍率 1.7 vs EUR 1.5，且 KOR 已有 12 个 COMPLETE 未取回的仿真结果待处理。

> 数据资产：`tracking/mining/rows_mlfp_{e8b,e10a,e10b,e11}.json` 含全部 19 条仿真实测指标；`tools/mine_eur_mlfactor.py` 的 `RAW_BATCHES` 已固化上述全部模板映射，可一键复跑；完整 19 条机会排行见 `tracking/mining/field_coverage_EUR_d1_TOP1200.json`。
