# INSIDERS 二次攻坚 · Step 2 预备设计（未测字段与设置轴）

> 待 BE130 双批（MARKET / CROWDING）收割后派发。目的：把 34 字段中剩余未测面与设置轴一次扫清。

## A. 字段可访问性探针（4 臂，必须先做）

从未跑过的 agg 字段共 17 个，其中 4 个已知不可访问。先用 4 臂探针验剩余高危字段：

| 臂 | 字段 | 说明 |
|---|---|---|
| 1 | `top_significant_value_2` | 高管大额榜第 2 位 |
| 2 | `directional_significant_value_2` | 方向大额榜第 2 位 |
| 3 | `top_directional_significant_value_2` | 高管×方向×大额第 2 位 |
| 4 | `avg_secondary_top_buy_shares` | 直接交易高管平均买 |

构造统一：`group_rank(ts_sum(<field>, 66), sector)` / avg 类用 `ts_mean`。

**判据**：任一臂 FAIL ⇒ 该字段不可访问（整批连坐，必须单独探）；全 PASS ⇒ 4 字段可进正式波。

## B. 设置轴扫描（3 批 × 6 臂）

同一组 6 个表达（冠军 + 5 个已验最优变体）分别跑三个设置档：

| 批 | decay | pasteurization | 假设 |
|---|---|---|---|
| B1 | **0** | ON | 该族 TO 仅 5.9%，decay4 可能过度平滑，decay0 保留原始时序锐度 |
| B2 | **2** | ON | 中间档（冠军族 pv20×insd 的冠军档就是 decay2）|
| B3 | 4 | **OFF** | pasteurization 关掉后不压制极端值，可能提 S 但伤 CONC |

6 个表达 = 冠军（cap桶三正交）/ 活动加速比替换 / 高管平均比替换 / Top2 集中度替换 / SV2 替换 / 逐腿归一（已知会超 CONC，作对照）

## C. 机制补充（若 A 探针通过）

| 机制 | 构造 | 依据 |
|---|---|---|
| 高管大额榜合成 | Σ66(SV1 + top_significant_value_2) | CMP 2012：高管专属交易更知情 |
| 方向大额榜合成 | Σ66(directional_significant_value_2 + 3) | 方向调整后的持续性大额 |
| 直接交易高管平均比 | avg_secondary_top_buy / avg_secondary_top_sell | 最内层交易者（直接持股高管）|
| 活动加速比 × 集中度 | multiply(D, H) | 突压 × 集中 = 高信念突袭 |

## D. 判读纪律（沿用）

- 任一臂 **S ≥ 1.45** ⇒ 该机制有效，进定向补
- 超冠军 **1.40 / 2Y 1.54** ⇒ 换主腿，重跑 CONC 与塔归属检查
- 全 ≤ 1.40 ⇒ 该轴关闭，写证书
- **CONC 必须 < 0.1**（150 臂已证：逐腿归一必超，等权/分桶结构才干净）