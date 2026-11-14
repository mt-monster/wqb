# insiders ATOM：字段画像与硬约束（先看清盘面）

日期：2026-11-12
用户指令：「锁定 insiders 挖掘 ATOM」

## 一、两个数据集的覆盖率事实

| 数据集 | 类型 | 字段数 | 覆盖率 | 覆盖宽度 |
|---|---|---:|---|---|
| `insiders1` | VECTOR | 8 | **全部 0.5343** | 约 267 只（TOP500 × 53.4%）|
| `insider_agg_matrix` | MATRIX | 34 | 32 个 0.5342 + 2 个 1.0000 | 同上 / 2 个全样本 |

**关键判断：两者覆盖率几乎相同（0.5343 vs 0.5342）⇒ 同一底层事件源的两个视图。**
- `insiders1` = 逐笔交易流（VECTOR）
- `insider_agg_matrix` = 聚合加工面（MATRIX，已按「显著度」排序取前 4 大单笔）

这解释了为什么「跨这两个数据集组合」历史上能到 2.36：
**互补的不是独立信息源，而是同一事件的两种加工视角**（逐笔变化 vs 集中度）。

## 二、ATOM 的硬约束（三条，全部来自实测）

| # | 约束 | 后果 | 证据 |
|---:|---|---|---|
| 1 | **单数据集** | 只能用 `insiders1` 或 `insider_agg_matrix` 之一 | 平台 ATOM 判定口径 |
| 2 | **禁 `cap` 桶** | `bucket(rank(cap))` 引入 PV 塔 ⇒ 变双塔 ⇒ 失去 ATOM | 实测 K1 塔 = PV+INSIDERS |
| 3 | **横截面宽度固定 267 只** | 无法通过扩大宇宙提升信噪比 | 覆盖率 53.4% |

其中第 2 条的代价很实在：`cap` 桶曾把 sub 从 0.63 拉到 0.90（历史实测）。

## 三、insiders1 的 8 个字段（可用 6 个）

| 字段 | 语义 | ATOM 可用 |
|---|---|---|
| `insd1_holdings` | 交易后总持股 | ✅ 主力 |
| `insd1_shares` | 本次交易股数 | ✅ |
| `insd1_value` | 交易金额（原币）| ✅ 但单位 CSPrice |
| `insd1_valueeur` | 交易金额（欧元）| ✅ 单位 CSPrice |
| `insd1_price` | 交易价 | ✅ 单位 CSPrice |
| `insd1_tradesignificance` | 显著度 1-3 | ✅ |
| `insd1_gvkey` | 公司 ID | ❌ 无信号 |
| `transaction_currency_code` | 币种码 | ❌ 无信号 |

**注意单位**：`value` / `valueeur` / `price` 都是价格/金额单位，参与算术前必须 `group_rank` 归一（本项目已因这条踩坑 4 次）。

## 四、insider_agg_matrix 的 34 个字段（可用 30 个）

| 字段族 | 代表 | 历史单腿 |
|---|---|---:|
| 显著值（前4大单笔）| `significant_value_1..4` | HHI 0.86 |
| 方向指标 | `directional_indicator` / `_2` | 0.59 |
| 买卖股数（总额）| `total_buy/sell_shares` | 未单测 |
| 买卖股数（均值）| `avg_buy/sell_shares` | 未单测 |
| 高管维度 | `*_top_*` | 0.73-0.83（判死）|
| 次级方向 | `directional_significant_value_*` | 2 个不可访问 |

## 五、已派基线三波

| 波 | 内容 |
|---|---|
| BE185 `PPAIJ52W` | insiders1 六字段 × 三形态单腿矩阵（10 臂）|
| BE186 `3IRA2k2M` | insider_agg_matrix 九字段单腿 + 组合（10 臂）|
| BE187 `4fl2cQcv` | 闸5 合规（同形态多窗）vs 跨形态对照（10 臂）|

## 六、判据纪律（本轮确立）

**终判一律用 `submit_verdict`，不用 `checks.fail`。**

证据（2026-11-12 三轮对照）：
| alpha | checks.fail | submit_verdict |
|---|---|---|
| 78YWrjgZ | `[]` | **BLOCKED**（LOW_SHARPE 1.29, LOW_FITNESS 0.93）|
| P05Nb7rw | `[]` | **BLOCKED**（3 项）|
| MP6OgoPr | `[]` | 待重判 |

⇒ `submit_verdict` = 模拟层 checks + **Failed-count 资格门** + 区域阈值，是唯一权威。