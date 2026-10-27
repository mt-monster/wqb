# 算子可用性实测台账（wqb）

> 从 `MEMORY.md` 外移的明细。判定新算子前先读本表，**不要重复踩坑**。

## 1 判定方法论

- **★★★ `preflight_expressions` 的 `unknown_fields` 会把算子误报为未知字段**：测 `greater(...)` 返回 `unknown_fields:["greater"]`，但仿真完全正常。它只校验**字段存在性**，会把逻辑算子（greater/less/and/or/if_else/not）当字段查。
  ⇒ **判定算子能否用必须真跑仿真**，不能只看 preflight。
- **★★★「genius」= Level 等级，不是算子名**：平台算子表有 `Level` 列，取值 `base` / `genius`。**算子全集 103 = base 85 + genius 18**。搜"genius 算子"必然 0 结果。
- **★ `level=null` ≠ 不可用**：API 返回里 level=null 的那批（多为 genius 级）实测全部可用（null 只代表 documentation 缺失）。

## 2 genius 级 18 个（USA/TOP3000 实测 18/18 可用）

`pasteurize`｜`ts_returns` / `ts_kurtosis` / `ts_ir` / `ts_max_diff` / `ts_target_tvr_decay` / `ts_target_tvr_hump`｜`vector_neut`｜`vec_min` / `vec_count` / `vec_max` / `vec_stddev` / `vec_range`｜`tail`｜`group_count` / `group_std_dev` / `group_sum` / `group_cartesian_product`

## 3 调用陷阱

- **★★ `vector_neut` 两参数须量纲兼容**：`vector_neut(close, volume)` 报 `Incompatible unit CSPrice vs CSShare`；改 `vector_neut(rank(close), rank(volume))` 通过。**实战最优形态 = `vector_neut(x, rank(cap))`**（连续投影降 prod，优于分桶 group_neutralize，无桶边界跳变）。
- **★★ `tail` 必须用命名参数**：`tail(x, 0, 100, 0)` 报 `Required attribute "upper" must have a value`；改 `tail(x, lower=0, upper=100, newval=0)` 通过。
- **★★ `tail` 语义**：`tail(x, lower, upper, newval)` = 把 **[lower, upper] 区间内**的值替换为 newval（不是保留）。`lower=0, upper=0.85, newval=0` = 砍掉低分 85% 保留尾部；写反得到补集，S 直接翻负（实测 −1.07）。
- **★ `ts_zscore` 必须带窗口参数**：`ts_zscore(cap)` 报错，用 `ts_zscore(cap, 252)`。
- **★ UNITS warning 不阻塞**：有量纲字段加无量纲常数（`add(group_std_dev(close, industry), 0.01)`）报 `UNITS: expected Unit[CSPrice:1], found Unit[]`，**仿真照常完成出结果**。
- **★ REVERSION_COMPONENT warning**：含反转组件（如 `-ts_delta(close,5)`）平台警告「may not accept these alphas in the future」⇒ 长期策略避开纯反转。
- **★★ 一条坏表达式毒死整批**：`unknown variable` / `inaccessible operator` / `Incompatible unit` 任一出现 ⇒ **整批** CANCELLED（含同批健康表达式）。派发前必 `preflight_expressions` + 本地 BAD_TOKENS 过滤。

## 4 确认不可用

- `regression_neut`（不存在，用 `vector_neut`）
- `arc_sin`（inaccessible；整批 5 条全废）
- `rank_by_side`（inaccessible；`group_rank(x, sign(x))` 也不行，Group 单位不匹配）
- `ts_median`（幽灵算子，toolkit 静态闸拦下）

## 5 Group 类

- `group_count(1, sector)` 裸用跑通。
- `if_else(greater(group_count(1, industry), 5), ...)` 覆盖过滤门控跑通（S 1.34）。
- 配合 `group_std_dev` 跑通（S 1.37）。
- ⇒ `group_count` 适合做**组内覆盖度过滤 / 组内分歧度分母**。
