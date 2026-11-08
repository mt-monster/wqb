# KOR / institutions6 波次 1 模板池（2026-11-06）

## 为什么开这个面（最强的跨区迁移逻辑）

1. **`institutions6` 在 IND 上是本轮最大富矿**：IND READY 池 57 条里约 30 条由该集派生，
   最终产出 **14 颗全绿候选**（S 1.64–3.20，全部 self<0.7 + prod<0.7 + fRA=0）。
2. **KOR 的 `institutions6` 字段名与 IND 完全一致**，11 个字段全部 MATRIX、
   **coverage 全部 1.0**（`aggregate_equity_value_all_owners` aC 91 … `aggregate_share_count_institutions` aC 257）。
3. KOR/D1 塔位实测：shortinterest 4 / fundamental 3 / model 3 / analyst 2 / pv 2 / other 1，
   **institutions 为 0 ⇒ 未点亮**，且该组合（PV×INSTITUTIONS）不触碰禁混集合内部。
4. KOR 已有 1 颗全绿候选 `LLZ6wZO2`（S 1.99 / self 0.6760 / prod 0.6762）⇒ 该区能出货。

## 字段清单（11 个，全 MATRIX，cov 1.0）

| 字段 | aC |
|---|---:|
| `aggregate_equity_value_all_owners` | 91 |
| `aggregate_equity_value_institutions` | 119 |
| `aggregate_share_count_all_owners` | 212 |
| `aggregate_share_count_institutions` | 257 |
| `count_institutional_buyers_security` | 88 |
| `count_institutional_holders_security` | 63 |
| `count_institutional_sellers_security` | 101 |
| `market_value_institutional_shares_acquired` | 112 |
| `market_value_institutional_shares_disposed` | 62 |
| `quantity_institutional_shares_acquired` | 119 |
| `quantity_institutional_shares_disposed` | 107 |

## 10 个结构互异模板

核心骨架统一为 `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(<X>,252), 252, rettype=0))`，
即「剥离 X 暴露后的时序残差动量」。差异全部落在 **回归自变量 X 的经济含义** 与 **是否二次中性化**。

| # | 变量 X 的构造 | 差异维度 | IND 源 alpha（S） |
|---|---|---|---|
| T1 | `ts_delay(disposed / (acquired + disposed), 21)` | 卖出**占比** + 21 日披露滞后 | `E5VNe67L` **3.20** |
| T2 | `quantity_institutional_shares_disposed` | 卖出**绝对量**水平 | `KPmvEYeE` **3.07** |
| T3 | `aggregate_equity_value_institutions / (count_institutional_holders_security + 1)` | 机构**户均持仓额** | `kqNrvwA8` 2.92 |
| T4 | `ts_delay(aggregate_share_count_all_owners, 21)` | 全体股东持股总数 + 滞后 | `88vwZE17` 2.46 |
| T5 | `count_institutional_buyers_security − count_institutional_sellers_security` | 买卖**家数净差** | `npvRmKq3` 3.00 |
| T6 | `mv_acquired/qty_acquired − mv_disposed/qty_disposed` | 买卖**均价价差** | `ZYmgngv0` 2.39 |
| T7 | T2 的 X + `group_neutralize(..., industry)` | **二次行业中性化** | `KPmvEYeE` 变体 |
| T8 | `(buyers + sellers) / holders` | **换手率**比率 | `E5VNENMr` 2.78 |
| T9 | `ts_delta(aggregate_share_count_institutions / aggregate_share_count_all_owners, 66)` | 机构占比**变化率**（不用回归） | 新模板 |
| T10 | `aggregate_equity_value_institutions / aggregate_equity_value_all_owners` | 机构持股市值**占比水平**（不用回归） | 新模板 |

**互异性自检**：回归自变量覆盖「比率 / 绝对量 / 户均 / 滞后水平 / 净差 / 价差 / 换手率」七类经济学含义，
外加「二次中性化」「一阶差分」「不用回归的纯水平」三种结构差异 ⇒ 满足 ≥10 结构互异要求。

## 波次 1 已派发（2 条，批级设置单一）

- 批 id：`11DL9l5tM4DK8Tf1cvex170r`
- 设置：KOR / TOP600 / D1 / decay 4 / **STATISTICAL** / trunc 0.08 / unit VERIFY / nan ON / pasteurization ON / maxTrade OFF
- T1（算子 7）：卖出占比 + 21 日滞后 —— IND `E5VNe67L` S 3.20 原款
- T2（算子 4）：卖出量水平 —— IND `KPmvEYeE` S 3.07 原款
- `validate_expressions` 通过：`valid=true`、`unknown_fields=[]`、`unknown_soft=[]`

## 验收判据

- KOR 的 LOW_SHARPE 线需从首个回测件的 `checks.fail[].limit` 实读（IND 为 1.58，KOR 待确认）
- 任一条 |S| ≥ 1.5 ⇒ 该配方在 KOR 复刻成功，直接铺开 T3–T10
- 两条 |S| < 0.8 且 TO 落 5–30% ⇒ KOR 的机构持仓信号弱于 IND，转 `risk59`/`news79` 面
- 两条 TO > 40% ⇒ 换面

## 独立于 IND 的额外价值

IND 的 14 颗全绿里 PV×INSTITUTIONS 已占满 3 颗配额（`E5VNe67L` 3.20 / `KPmvEYeE` 3.07 / `N1eLRWML` 2.98）。
**KOR 的 PV×INSTITUTIONS 是全新配额**（0/3），同一套骨架在 KOR 出货不受 IND 配额挤压。
