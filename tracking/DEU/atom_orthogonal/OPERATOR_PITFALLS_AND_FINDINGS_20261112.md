# 算子使用手册补充：本次踩到的命名参数与单位陷阱（可复用）

日期：2026-11-12
来源：DEU insiders 算子全覆盖补课（BE178-BE181）

## 一、命名参数陷阱（静态闸会拦，但报错信息有用）

| 算子 | 错误写法 | 正确写法 | 报错 |
|---|---|---|---|
| `ts_target_tvr_hump` | `ts_target_tvr_hump(x, 0.10)` | `ts_target_tvr_hump(x, lambda_min=0.10)` | `函数 ts_target_tvr_hump 的第2个参数必须使用命名参数 'lambda_min='` |
| `ts_target_tvr_decay` | `ts_target_tvr_decay(x, 0.10)` | `ts_target_tvr_decay(x, lambda_min=0.10)` | 同上 |
| `ts_regression` | `ts_regression(y,x,252)` | `ts_regression(y, x, 252, lag=0, rettype=0)` | 后两个是命名参数 |
| `bucket` | `bucket(rank(cap), "0,1,0.1")` | `bucket(rank(cap), range="0,1,0.1")` | range 必须命名+双引号 |
| `tail` | `tail(x, 0.25)` | `tail(x, lower=0.25, upper=1.0, newval=0)` | 三个命名属性全给 |
| `hump` | `hump(x, 0.01)` | `hump(x, hump=0.01)` | 必须命名 |

## 二、单位陷阱（本项目已踩 4 次）

| 场景 | 错误 | 根因 | 修法 |
|---|---|---|---|
| 股数字段进 add | `add(group_rank(hhi), total_buy_shares)` | `total_buy_shares` 是 `Unit[CSShare]`，group_rank 输出 `Unit[]` | 股数/金额字段先 `group_rank` 归一 |
| bucket 作分组轴 | `group_rank(x, bucket(cap, range=...))` | bucket 输出非 `Unit[Group:1]` | 内层必须 `rank(...)`：`bucket(rank(cap), ...)` |
| ts_zscore→ts_av_diff 替换 | 直接换 | 输出单位族不同（`Unit[TSShare]` vs `Unit[]`）| 换完要重测，或加包裹归一 |
| sign 作 group 键 | `group_rank(x, sign(y))` | sign 返回普通数值非 Group | 用 `bucket`/`densify` 造 Group |

## 三、本次新发现有效的算子（值得优先试）

| 算子 | 用法 | 实测效果 |
|---|---|---|
| **`group_cartesian_product`** | `group_cartesian_product(sector, bucket(rank(cap),range="0,1,0.2"))` 作复合分组轴 | **S 1.28 / sub 0.65（全族最高 sub）** |
| **`vector_neut`** | `vector_neut(B, A)` 取 B 对 A 的横截面正交残差 | S 1.30→**1.33**（+0.03）|

⚠ `vector_neut` 是 **Cross Sectional** 类（横截面正交），不是时序正交。

## 四、本次确认无效的算子（省预算）

| 算子 | 用法 | 实测 S（基线 1.30）|
|---|---|---:|
| `ts_kurtosis` | 66 日峰度 | 0.94 |
| `ts_arg_max` | 距 252 日最大值天数 | 0.95 |
| `if_else` | A>0.5 才持仓（门控）| 1.03 |
| `ts_product` | 22 日几何乘积 | 1.13 |
| `normalize` / `zscore` | 配正交化作截面层 | 1.15 |
| `ts_max_diff` | x−ts_max(x,66) | 1.16 |
| `ts_av_diff` / `ts_scale` | 偏离均值 / min-max 归一 | 1.17 |
| 多重正交化 | 两/三个 `vector_neut` 叠加 | 0.93 / 0.96（残差太小，叠加成噪声）|

## 五、纪律（写给自己）

1. **派发前跑 `operator_coverage_audit.py --checklist`**，逐类问「本信号上有没有可能出东西」。
2. **同一 dataset 内想叠加时，先试 `vector_neut` / `ts_regression` 残差**，不要只用朴素 add 就下「不可叠加」结论。
3. **命名参数算子**（`ts_target_tvr_*` / `tail` / `hump` / `bucket` / `ts_regression`）必须查 definition 再写。
4. **股数 / 金额字段参与算术前必须 `group_rank` 归一**。
5. 平台 `get_operators` 返回 103 个（REGULAR 84），`definition` 字段给出了准确签名——**写新算子前先读 definition，不要猜**。