# KOR Analyst ATOM 战役 · Wave A1（2026-11-07 开波）

## 为什么开 analyst 塔（换塔理由，非频繁切换）
1. **KOR Risk 塔已挖透**：12 波、约 60 条表达式、7 个 risk 数据集全覆盖，唯一强轴 anlystsn 用尽。
   详见 `tracking/KOR/campaign_20261107_risk_atom/campaign_status_20261107.md`。
2. **经济驱动同源**：risk70 里唯一 S1.62 的字段是 `asetrd_anlystsn`（分析师情绪载荷）⇒
   「分析师预期」是 KOR 唯一被实证有效的经济机制，analyst 塔有更纯的同族数据。
3. analyst 塔乘数 1.6（KOR 并列最高档），塔未点亮。

## 数据集选型（KOR analyst 类别共 17 个）
| 集 | cov | 字段 | users | aC | valueScore | 判读 |
|---|---:|---:|---:|---:|---:|---|
| **analyst_consensus** | 0.6899 | **2343** | 157 | **300** | 5.0 | **选中**：字段池最大 + aC 仅 300（极白）+ vs 5.0 |
| analyst16 | 0.6526 | 109 | 127 | 293 | 5.0 | 备选（Real Time Estimates，白） |
| analyst44 | 0.773 | 540 | 480 | 1366 | 4.0 | 备选（Integrated Broker Estimates） |
| analyst_factor_signals | 0.577 | 59 | 113 | 186 | 4.0 | 备选（预置因子信号） |
| analyst11 | 0.5831 | 210 | 51 | 75 | 6.0 | 描述是 RIC/BBID 映射，非信号，弃 |
| analyst15 | 0.5255 | 304 | 987 | 22634 | 1.0 | 饱和（aC 2.3 万），弃 |
| analyst10 | 0.7306 | 640 | 417 | 872 | 3.0 | 2026-11-06 已开过波，先不碰 |

## 字段画像（analyst_consensus）
- 类型分布：**VECTOR 2325 / MATRIX 18** ⇒ 几乎全部必须 `vec_*` 包裹（同 risk59 打法）。
- 家族（按 id 子串计数）：`estimate` 1367、`actual_` 548、`surprise` 286、`count` 157、`eps` 185、`rev` 149、`div` 96、`bvps` 72、`roe` 54、`ebitda` 46、`targetprice` 12。
- 覆盖分档：surprise 族 **0.800–0.803**（最高）/ targetprice 族 0.8037 / avg_ 与 count_ 与 *_prior 族 0.6382 / actual_ 族 0.62–0.80。
- 多版本后缀：`_fxadj`（汇率/拆股调整）、`_tribes`、`_2` `_3`（不同口径）⇒ **版本层不是等价改写**，需各打裸探针（沿用 analyst10 的教训）。

## Wave A1 · 10 个结构互异模板（全部单数据集 ⇒ ATOM）
记号 longHigh(x) = subtract(group_rank(x, sector), 0.5)；longLow(x) = subtract(0.5, group_rank(x, sector))

| # | 机制 | 几何 | 算子 | 表达式 |
|---|---|---|---:|---|
| A1-01 | PEAD 盈余惊喜水平 | 截面秩（sector） | 4 | longHigh(vec_avg(mean_surprise_value_net2)) |
| A1-02 | PEAD 双指标合取 | 两腿相乘（非 add） | 9 | longHigh(net2) × longHigh(revenue_annual12) |
| A1-03 | PEAD 时序平滑 | ts_mean 66 后截面 | 5 | longHigh(ts_mean(vec_avg(mean_surprise_value_net2),66)) |
| A1-04 | 4 周盈利预测修正 | 归一化差分 | 8 | longHigh((est − est_4wk) / (\|est_4wk\|+1)) |
| A1-05 | 3 月盈利预测修正 | 归一化差分（长窗） | 8 | longHigh((est − est_3mth) / (\|est_3mth\|+1)) |
| A1-06 | 分析师覆盖扩张（关注度） | ts_delta 66 | 5 | longHigh(ts_delta(vec_avg(count_net_income_estimates),66)) |
| A1-07 | 低覆盖溢价 | 水平秩 | 4 | longLow(vec_avg(count_net_income_estimates)) |
| A1-08 | 预测分歧度（低分歧溢价） | 变异系数 | 8 | longLow(stdev_3mth / (\|avg_3mth\|+1)) |
| A1-09 | 目标价低离散（强共识） | 离散/中位 | 7 | longLow(stddev_tp / (median_tp+1)) |
| A1-10 | 目标价上偏斜（乐观尾部） | max/median | 7 | longHigh(max_tp / (median_tp+1)) |

**模板多样性自检**：10 个模板在 6 个维度上互异 ——
① 经济机制（PEAD / 修正 / 覆盖 / 分歧 / 目标价）5 类；② 矩（水平 / 差分 / 二阶离散）3 类；
③ 时序加工（无 / ts_mean / ts_delta）3 类；④ 组合方式（单腿 / 双腿相乘）2 类；
⑤ 方向（longHigh / longLow）2 类；⑥ 归一化（无 / \|分母\|+1）2 类。⇒ 满足「≥10 个结构互异模板」。

## 设置
KOR / TOP600 / D1 / EQUITY · **REVERSION_AND_MOMENTUM** · decay 1 · truncation 0.04 · unitHandling VERIFY · nanHandling ON · pasteurization ON · maxTrade OFF · 2014-01-01~2023-12-31
（沿用 omERn83n 已验证档：RAM 在 KOR 对 Fitness 明显更好，R12 实测 F 0.93→1.22）

## 派发
- 脚本：`tools/mcp_7slot_batch.py`（项目正规 MCP 批量客户端）
- `--batch-size 8 --max-in-flight 2`（并发 2，符合约束）
- preflight：`valid=True` / `unknown_fields=[]` / `any_changed=False`
- 输出：`waveA1_results.csv`

## 判读预案
- 任一 S≥1.58 且 F≥1.0 且 2Y≥1.58 ⇒ 进交付队列，逐颗查 self/prod + 逐年覆盖。
- 若 PEAD 族（A1-01/02/03）最强 ⇒ 沿 surprise 族（286 字段）扩产。
- 若修正族（A1-04/05）最强 ⇒ 沿 *_prior / avg_ 族扩产。
- 全灭 ⇒ 换 analyst16 / analyst44 / analyst_factor_signals。