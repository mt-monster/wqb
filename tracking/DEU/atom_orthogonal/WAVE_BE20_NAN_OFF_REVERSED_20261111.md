# BE20 结论：nanHandling=OFF 是反向杠杆（假设被证否）

## 一、四臂对照结果（sim 2E3jn95GZ5f5aMmI3Lwy2tN，nan_handling=OFF）

| 臂 | alpha | S | F | TO | sub | 2Y | nan=ON 对照 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | Jj8VWkNl | **0.18** | 0.04 | 0.2965 | 0.09 | 0.26 | P05JM61x S1.46 | 崩 -1.28 |
| 2 | 78YkvrNZ | **0.18** | 0.04 | 0.2958 | 0.03 | 0.28 | QP010j5W S1.52 | 崩 -1.34 |
| 3 | d5a236bY | **0.14** | 0.03 | 0.1818 | 0.12 | -0.21 | wpo83GXx S1.40 | 崩 -1.26 |
| 4 | E5QZ8Mp9 | **0.70** | 0.43 | 0.2376 | 0.27 | 1.31 | qM7KxkQV S1.72 | 崩 -1.02 |

**全部四臂暴跌，无例外。nanHandling=OFF 不是提分杠杆，而是反向杠杆。**

## 二、机制解释

关键差异在于表达式是否使用 `ts_backfill` / `vec_avg` 做缺失填充：

| 类型 | 表达式特征 | nan=ON | nan=OFF |
|---|---|---|---|
| 我此前的探针 | 一律 `ts_backfill(vec_avg(FIELD), 132)` | 填充有效，S 1.40-1.72 | **填充失效，S 0.14-0.70** |
| 已交付 ATOM 件 | 直接用原始字段（est_12m_ebt_mean 等） | 未测 | 靠 OFF 剔除缺失股票 |

所以 `ts_backfill` 与 `nanHandling` 是互补关系，不是独立维度：
用了 ts_backfill 就必须配 nan=ON；没做填充、靠原始字段的表达式才适合 nan=OFF。

## 三、对第 10 颗的影响

**假设被证否，第 10 颗维持不可行结论**（nws20 族 S 上限 1.52 的公式级证明仍成立）。
本战役定格 **9 颗**（4 严格 ATOM + 5 regular）。

## 四、设置层仍有两个未测维度

1. **neutralization**：已交付件里 FAST 与 SUBINDUSTRY 并存，FAST 可能对某些族更优；
2. **decay**：已交付件有 decay=0（zq3eb7No / RREPm361 都是 0），而我用的都是 4。
   decay=0 意味着不做额外平滑，配合表达式自身的 ts_target_tvr_decay 可能更好。

注意：decay=0 会让 TO 升高，需配合 F 公式验算是否仍过闸。