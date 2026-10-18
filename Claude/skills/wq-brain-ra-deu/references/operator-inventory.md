# 算子覆盖与未用算子归因（DEU 审计，2026-10-14）

> 数据源：`tools/gates/operator_coverage_audit.py --checklist`（REGULAR 84 个）× 台账 `backtest_results` 全量表达式。

## 一、总账

| 项 | 数 |
|---|---|
| 平台 REGULAR 可用算子 | **84** |
| DEU 台账实际使用 | **68** |
| **未使用** | **16** |
| 其中**全库（所有区域）从未使用** | **6**（`greater_equal, kth_element, less_equal, not, sqrt, ts_product`）|

## 二、未用 16 个的四类归因

### A. 有等价/更优替代（5）——不需要用
| 算子 | 等价形式 | 为什么用替代品 |
|---|---|---|
| `inverse(x)` | `divide(1, x)` | divide 可加 epsilon 防除零 |
| `sqrt(x)` / `power(x,y)` | **`signed_power(x, y)`** | 平台文档明示 sqrt/power 对**负值或非整数指数丢符号**；我们的字段有负值 |
| `ts_product(x,d)` | `ts_sum(log(x), d)` | 几何均值/复利语义等价，数值更稳 |
| `group_sum(x,g)` | `group_mean(x,g)` | sum 引入**规模泄露**（组越大值越大），mean 更合规 |

### B. 语义/类型不匹配（4）——场景不适用
| 算子 | 为什么 |
|---|---|
| `densify(g)` | 作用于 **GROUP 类轴**（压桶）；我们只把现成轴直接传给 `group_*`，未做多轴合并 |
| `ts_step(1)` | 日期计数器（时间索引），**不是信号构造** |
| `ts_count_nans(x,d)` | 窗口 NaN 计数 = **数据质量属性**，非经济信号（同类：`count_*` 字段）|
| `not(x)` | 逻辑取反；用 `trade_when`/`if_else` + 反向比较（`less`）实现更清晰 |

### C. 阈值边界变体（4）——连续值上无增量
- `greater_equal` ≡ `greater`（已用 202 次）/ `less_equal` ≡ `less`：连续分布上仅阈值单点差异。
- **`equal` / `not_equal` 有真场景**：离散标签的**状态变化检测**（`not_equal(f, ts_delay(f,1))` = 事件发生）——已补测（见三）。

### D. 真未试构造（3）——已补测
- `kth_element(x, d, k=...)`：第三种回填策略
- `last_diff_value(x, d)`：**事件驱动核心**（最近一次「不同值」= 上次变化幅度），与用过的 `days_from_last_change`（多久前变化）配套
- `ts_kurtosis(x, d)`：**时序尾部风险**（与我们做过的**跨分析师分布偏度**是不同的构造）

## 三、补测结果（WANL82 / WANL83）

| 构造 | 读数 | 判定 |
|---|---|---|
| `not_equal` 事件门控 `trade_when` | 0.55 | 无信号 |
| `ts_count_nans`（数据质量） | 0.50 | 无信号 |
| 评级变化幅度 × 新鲜度 | 0.31 | 无信号 |
| `ts_product(add(stars,1),21)` | 0.08 | 无信号 |
| `last_diff_value(stars/rv,252)` | 0.05 / 0.01 | 无信号 |
| `ts_kurtosis(rv/gsfa,252)` | −0.06 / −0.09 | 无信号 |
| `kth_element(Q1,252,k=1)` | **1.18** | **= ts_backfill 版同值 ⇒ 语义等价** |
| `kth_element(stars,252,k=1)` | 0.19 | — |

**⇒「未用算子」不构成信号缺口。**

## 四、★ 两条硬性工程结论

1. **`kth_element` 的 `k` 必须具名**：位置写法报 `Required attribute "k" must have a value`，且**连坐整批 CANCELLED**；`k=1` 才通过。
2. **本地 `op_arity` 与平台签名不一致（待修）**：本地判 `k` 为位置参数并**拒绝 `k=`**，平台运行时**要求 `k=`** ⇒ 本地闸会误拦合法表达式。**实操：本地闸拒绝但写法符合平台文档时，以平台实测为准（发 1 条探针定夺，别整批发）。**

## 五、发批纪律要点（本轮新增）

- 引入**从未用过的算子**时：先发 **1–2 条探针批**验证签名与语义，**不要**直接混入 10 条主批（一条错 = 整批 CANCELLED）。
- `preflight_expressions` 服务不可用时：用直连 `/data-fields` 核字段存在性 + 类型，并在**本地**核算子是否在 REGULAR 清单内。
