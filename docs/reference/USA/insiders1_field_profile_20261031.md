# USA / insiders1 字段画像（Global Insider Trading Data）

> 生成时间：2026-10-31（wave283 / wave284 实测后回填）
> 数据来源：`get_datafields(dataset_id="insiders1", region="USA", universe="TOP3000", delay=1, filter_sharpe=false)` 实时拉取（45/45 字段，`complete: true`, `platform_count: 45`）
> 实测回测：wave283（12 条）+ wave284（14 条）= **26 条 USA 回测，零 ERROR**
> 目的：为后续不同机制（事件流异常度 / 信念强度 / 集群度 / 绩效归因）奠定字段角色底账

---

## 0. 数据集定位

| 项 | 值 | 说明 |
|---|---|---|
| 数据集 id | `insiders1` | Global Insider Trading Data |
| category | **INSIDERS** | ⇒ 目标塔 USA/D1/INSIDERS |
| 平台塔倍率 | **1.1**（`pyramids.list` 实测） | 与 board_gov_stats 同档；注意 DB `datasets` 表同名列有多行且倍率不一致（1.1/1.2/1.3/1.5/1.8），**以平台 `pyramids.list` 为准** |
| 字段数 | 45（MATRIX 29 + VECTOR 16） | 见 §1 |
| 平台覆盖率 | 比率族 0.7842 / 逐笔族 0.756 / checkpoint 族 0.4488 | |
| 平台 alphaCount | 386（DB `datasets` 行） | 中等拥挤 |
| USA 历史回测 | **wave283 前为零** | 真·未测靶子 |
| 回测区间 | 2014-01-01 ~ 2023-12-31 | 近十年全覆盖 |

---

## 1. 字段族分类（45 字段）

### 族 A — 平台预聚合比率（MATRIX，cov 0.7842，**本集唯一有效族**）

| 字段 | uCnt | aCnt | 语义 | wave283/284 实测 S |
|---|---|---|---|---|
| `buy_to_sell_amount_ratio_1wk` | 40 | 49 | 近 1 周买/卖金额比 | 0.17（TOP1000） |
| `buy_to_sell_amount_ratio_2wk` | 28 | 32 | 近 2 周 | 未测 |
| `buy_to_sell_amount_ratio_1mo` | 80 | 109 | 近 1 月 | 1.12 |
| `buy_to_sell_amount_ratio_2mo` | 38 | 47 | 近 2 月 | 1.07 |
| `buy_to_sell_amount_ratio_qtr` | 102 | 161 | 近 1 季 | **1.15（族内最佳）** |
| `buy_to_sell_amount_ratio_6mo` | 144 | 189 | 近 6 月 | 1.17 |
| `buy_to_sell_amount_ratio_1yr` | 112 | 161 | 近 1 年 | 1.14 |
| `buy_to_total_amount_ratio_1wk` | 49 | 58 | 买/总额（剥离卖压） | 未测 |
| `buy_to_total_amount_ratio_2wk` | 20 | 22 | 同上 | 未测 |
| `buy_to_total_amount_ratio_1mo` | 35 | 39 | 同上 | 未测 |
| `buy_to_total_amount_ratio_2mo` | 21 | 23 | 同上 | 未测 |
| `buy_to_total_amount_ratio_qtr` | 59 | 70 | 同上 | 1.14 |
| `buy_to_total_amount_ratio_6mo` | 43 | 50 | 同上 | 0.19（裸 ts_zscore） |
| `buy_to_total_amount_ratio_1yr` | 55 | 62 | 同上 | 1.12 |

**族 A 结论（wave283/284 共 11 条实测）**：
- ✅ **有效**：直接截面 `group_rank` 后 `winsorize(std=2)` ⇒ S 1.07–1.17、checks.fail 空、TO 1.6–4.4%、margin 2.6–5.8bp、inv_S 1.11–1.17
- ❌ **无效**：对自身基线再 `ts_zscore`（二次标准化，S 0.98–1.52 区间但 SUB 塌到 0.37–0.38）
- ❌ **无效**：一阶差分 `ts_delta`（S 0.26）、二阶方差 `ts_std_dev`（S −0.58）
- ⚠️ **族内天花板 ≈1.17**（14 条模板 S 分布 0.98–1.17，闸线 1.58）

### 族 B — 逐笔申报（VECTOR，cov 0.756，**需 vec_* 聚合**）

| 字段 | uCnt | aCnt | 语义 | 实测 |
|---|---|---|---|---|
| `insd1_value` | 126 | 292 | 交易总金额（原币） | T05/T07/T09 主腿，均负 |
| `insd1_valueeur` | 124 | 284 | 交易总金额（欧元） | 未测 |
| `insd1_shares` | 166 | 384 | 成交股数 | T06/T07 主腿，均负 |
| `insd1_holdings` | 283 | 952 | 交易后总持股（**存量**） | 分母，conviction ratio 用 |
| `insd1_price` | 148 | 300 | 成交价（区间报则取下限） | T09 分母 |
| `insd1_tradesignificance` | 224 | 522 | 交易重要性评分（1 低 ~ 3 高） | T08 权重，S −0.65 |
| `insd1_gvkey` | 263 | 566 | Compustat 全球公司码 | 元数据，非信号 |
| `max_trade_price` | 9 | 9 | 区间报的上限价 | 未测 |
| `transaction_currency_code` | 7 | 8 | ISO 币种码 | 元数据，非信号 |

**族 B 结论（wave283 5 条实测）**：
- ❌ **conviction ratio（论坛帖 43178926004887 的 DEU 模板）在 USA 全灭**：
  - `value/holdings` S **−0.85**、`shares/holdings` S **−0.92**
  - 机理：USA 的 `insd1_holdings` 存量口径与 DEU `inst1_holdings` 不同（DEU 是 Directors' Dealings 逐笔申报后持仓；USA 是 Form 4 汇总持仓），**跨区照搬失败**
- ❌ **差值型** `subtract(value, shares)` S −0.44 —— 量纲不兼容（UNITS warning: expected `Unit[CSPrice:1,CSShare:1]` found `Unit[CSShare:1]`）且金额−股数无量纲意义
- ❌ **集群度代理** `value/price` S −0.53 —— 退化回股数规模暴露
- ❌ **显著性加权** `value×significance` S −0.65 —— 乘积把两个同号因子叠成规模暴露
- ⚠️ **ε 加法陷阱复现**：`add(vec_sum(insd1_holdings), 0.0001)` ⇒ UNITS warning（expected `Unit[CSShare:1]`, found `Unit[]`），虽为 warning 非 FAIL，但会伴随信号失真

### 族 C — checkpoint 交易绩效（VECTOR，cov 0.4488，**本波未测，机制空白**）

| 字段 | uCnt | aCnt | 语义 |
|---|---|---|---|
| `txn_amount_checkpoint` | 45 | 49 | 基准点交易金额 |
| `txn_days_checkpoint` | 18 | 19 | 基准点交易天数 |
| `txn_di_checkpoint` | 35 | 37 | 基准点交易方向指标 |
| `txn_return_long_checkpoint` | 14 | 15 | 基准点多头交易收益 |
| `txn_return_mean_checkpoint` | 36 | 40 | 基准点平均交易收益 |
| `txn_return_short_checkpoint` | 11 | 11 | 基准点空头交易收益 |
| `txn_return_variance_checkpoint` | 40 | 45 | 基准点交易收益方差 |
| `txn_sharpe_long_checkpoint` | 17 | 18 | 基准点多头夏普 |
| `txn_sharpe_ratio_checkpoint` | 20 | 22 | 基准点交易夏普（**wave283 T11 测过，S 弱**） |
| `txn_sharpe_short_checkpoint` | 10 | 11 | 基准点空头夏普 |

### 族 D — 内部人自身绩效快照（MATRIX，cov 0.3407–0.4263，**全未测**）

| 字段组 | uCnt | aCnt | 语义 |
|---|---|---|---|
| `mean_return_all / long / short` | 13–16 | 14–19 | 平均收益（全体/多头/空头） |
| `mean_sharpe_all / long / short` | 4–37 | 5–41 | 平均夏普 |
| `weighted_return_all / long / short` | 8–18 | 8–20 | 加权收益 |
| `weighted_sharpe_all / long / short` | 10–23 | 14–27 | 加权夏普 |

**族 D 是本集最大的未测机制空间**：它直接回答「这家公司的内部人过去做得怎么样」——JMZ(2003) 的绩效评价视角（内部人自己赚到的超额收益），而非单笔交易视角。cov 偏低（0.34–0.43）但有独立的机制含义。

---

## 2. 本集数据「三个脾气」（来自实测，非文档转述）

1. **平台预聚合 = 已平滑**。族 A 的比率是平台滚动算好的，直接截面比较即得信号（S 1.15）；再叠时间维算子（zscore/delta/std_dev/decay）只会抹掉截面区分度。**这与 insider_trx_matrix 族完全相反**——那族是稀疏脉冲流，必须先 `ts_sum` 聚强度。
2. **族 A 的时间维算子全部有害**。delta / std_dev / zscore / decay_linear 相对裸 group_rank 分别：S 0.26 / −0.58 / 0.98–1.04 / 1.03。
3. **族 B 是「逐笔金额」而非「强度」**。`insd1_value` 混公司规模，且 `insd1_holdings` 存量口径在 USA 不可比 ⇒ 一切需要「除以自身存量」的构造在 USA 这套数据上失效。

---

## 3. 字段角色底账（供后续机制选择）

| 角色 | 字段 | 建议用法 | 已知边界 |
|---|---|---|---|
| **主信号（已验证）** | `buy_to_sell_amount_ratio_{qtr,6mo,1yr}` | `winsorize(group_rank(ts_backfill(x,252), industry), std=2)` | S 天花板 ≈1.17；子宇宙 SUB 0.62–0.79 |
| **主信号（同强度替代）** | `buy_to_total_amount_ratio_{qtr,1yr}` | 同上 | 与买/卖比几乎同强度 ⇒ 不是独立信号 |
| **辅助/机制空白** | 族 D（12 个内部人绩效快照） | 待测：直接用、或做 group 轴、或与族 A 残差化 | cov 0.34–0.43；uCnt/aCnt 极低 ⇒ prod 应天然低 |
| **机制空白** | 族 C 剩余 9 个 checkpoint 字段 | 待测：`txn_return_variance`（内部人决策方差）、`txn_di_checkpoint`（方向一致性） | `txn_sharpe_ratio_checkpoint` 已测 S 弱 |
| **判死** | 族 B 全部逐笔字段 | 不可作主腿 | conviction ratio / 差值 / 集群度 / 显著性加权 四种构造全负 |
| **判死** | `insd1_gvkey` / `transaction_currency_code` / `max_trade_price` | 元数据 | 非信号字段 |

---

## 4. 平台/设置约束（USA/D1）

- **合法 universe 仅 6 档**：TOP3000 / TOP2000 / TOP1000 / TOP500 / TOP200 / TOPSP500
  ⇒ 论坛帖 43152032301591 的「换 ILLIQUID_MINVOL1M 解 SUB」杠杆在 USA **不可用**（平台直接报错）
  ⇒ 实测 TOP1000 比 TOP3000 更差（wave283：TOP1000 S 0.05/0.17 vs TOP3000 S 1.15）
- 本波全部实测 settings：`TOP3000 / SUBINDUSTRY / decay 5 / truncation 0.08 / nanHandling ON / maxTrade OFF / pasteurization ON / unitHandling VERIFY / FASTEXPR`
- 塔位：全部 `USA/D1/INSIDERS`（mult 1.1），**单数据集、无跨集腿 ⇒ 塔位纯净**

---

## 5. 下一步机制方向（未测，按优先级）

1. **族 D 内部人绩效快照**（12 字段全未测）—— 机制正交于「交易事件流」，且 uCnt/aCnt 极低 ⇒ prod 天然低。这是 INSIDERS 塔最有希望的一枪。
2. **族 C 的方差/方向字段** —— `txn_return_variance_checkpoint`（内部人决策方差）可做「内部人犹豫程度」，机制上与族 A 的「买/卖比」正交。
3. **跨数据集残差化**（insiders1 腿 + 其他数据集腿）—— 按已验证纪律：**主腿必须信息量更大**，insiders1 腿 S ≤1.17 属「信息量小」，只能当残差腿不能当主腿；且 trio 塔内部（PV/MODEL/OTHER）禁混，INSIDERS 不在 trio 内故允许，但每组合候选 ≤3。

---

## 6. 相关文件

- 回测台账：`data/wqb.db` → `backtest_results` where `region='USA' AND dataset='insiders1'`（wave 283: 12 行 / wave 284: 14 行）
- 波次结论：`wave_results` where `region='USA' AND wave_number IN ('283','284')`
- 算子签名闸：`logs/_tmp_arity_insiders1_w283.py`（12/12 PASS）、`logs/_tmp_arity_insiders1_w284.py`（14/14 PASS）
- 落库脚本：`logs/_tmp_store_w283.py`、`logs/_tmp_store_w284.py`
