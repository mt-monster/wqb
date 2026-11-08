# FINDING P84：chart_cnn_alpha 首轮 16 条定性与归因

日期：2026-11-08 · KOR / TOP600 / D1 · 数据集：chart_cnn_alpha（model · 1010 MATRIX · aC34 / uc25）

## 一、结果总表（raF = failed_ra_count）

### P84A（decay 4 / trunc 0.08 / industry）multisim JEO8qff54zEcscjjKG1ryt

| alpha | 模板 | S | F | TO | raF |
|---|---|---:|---:|---:|---:|
| mLoQ5EbK | T1 分位概率价差（eqstar4 60d） | 1.22 | 0.64 | 0.2551 | 3 |
| WjOJAvVk | T5 置信度加权概率 | **1.31** | 0.69 | 0.2665 | 3 |
| wpQWa0El | T9 leaps 100d 五分位差 | 1.00 | 0.64 | 0.1367 | 3 |
| d5WvZNRv | T12 单腿 prob4 | 0.99 | 0.39 | 0.3197 | 3 |
| 78LlzenL | T11 leaps 200d 五分位差 | 0.94 | 0.60 | 0.1322 | 3 |
| d5WvZNZX | T3 一阶差分 22 | 0.47 | 0.11 | 0.3357 | 4 |
| QPv6GwVw | T4 跨期限 malta3 60 vs 180 | 0.35 | 0.06 | 0.5518 | 4 |
| MPYVGJL8 | T8 跨模型 eqstar4 vs leapstar4b1 | −0.22 | −0.04 | 0.3315 | 5 |

### P84B（decay 22 / country）multisim 3DddQc6kL4QJc9z1fLp6UlUD —— ASI 配方全部失效

| alpha | 模板 | S | F | TO | raF |
|---|---|---:|---:|---:|---:|
| 1YN0w1Vm | T7 预测不稳定（二阶，取负） | 0.50 | 0.23 | 0.1053 | 3 |
| Jjer7Y0e | T1 equity2b2 60d + ts_rank8 | 0.27 | 0.06 | 0.3074 | 3 |
| A1VElYJW | T10 rank 加速度 | 0.24 | 0.06 | 0.1995 | 3 |
| wpQWjOXv | T2 ts_rank5 价差 | 0.22 | 0.04 | 0.3941 | 3 |
| RREP7q00 | T2 ts_rank8 价差 | 0.20 | 0.04 | 0.3113 | 4 |
| gJeLjwqM | T9 leaps + ts_rank8 | 0.03 | 0.00 | 0.2857 | 4 |
| GrW9lY05 | T1 star1b1 60d + ts_rank8 | 0.01 | 0.00 | 0.2869 | 4 |
| 58EYl3Nz | T6 预计算期望分位 rank | −0.48 | −0.14 | 0.3248 | 5 |

## 二、归因结论（三条，均可复用）

### 结论 1：ASI 的「短窗 ts_rank + 大 decay」破 prod 配方**不可跨数据集套用**

同一骨架（= 分位概率价差），在 P84A 用 decay4/裸水平得 S1.22，在 P84B 改成 ts_rank(8)+decay22 后掉到 **0.20**，
ts_rank(5) 也只有 0.22，ts_rank(10) 对预计算 rank 字段直接 **−0.48**。

**机理**：ASI 那条配方的适用前提是「原信号是**拥挤的慢变水平分量**，短窗秩只保留近 W 日相对位置、剥掉共同慢分量」。
而 chart_cnn_alpha 的 CNN 概率本身就是**已平滑的慢变量**（裸 TO 仅 0.26–0.33，远低于 ASI 那条的水平分量），
再叠 ts_rank 等于对一个已经低通滤波的序列做二次低通，信息被彻底抹掉。

**判据**：破 prod 配方启用前先看裸信号的 TO。TO > 0.6 的拥挤水平信号 → 适用短窗 ts_rank；
TO < 0.35 的慢信号 → 禁用 ts_rank，改用 decay/truncation/分组轴提纯。

### 结论 2：该数据集的信息集中在 **prob4 的横截面水平**，且置信度加权是有效增益

- 裸 prob4 单腿 S0.99；prob4 − prob0 价差 S1.22（+0.23，说明分位差带来了净增益）；
- prob4 × confscore4 加权 S**1.31**（再 +0.09，置信度维度确实携带独立信息）；
- 但一阶差分（0.47）、rank 加速度（0.24）、二阶方差（0.50）、跨模型差（−0.22）全部为噪声或反向，
  ⇒ 本集的信号是**静态水平**，不含可用的时序动态或模型间分歧信息。

### 结论 3：leaps 长窗族是唯一与 eqstar4 不共用腿的独立弱源

leaps 100d（S1.00）/ 200d（0.94）五分位差单独成立，且与 eqstar4 族字段不重叠。
若本数据集后续能出第 2 颗，应走 leaps 长窗（互相关预计低），而不是 eqstar4 的窗口变体（必撞 0.95+）。

## 三、当前定位

本数据集 **S 天花板 ≈ 1.31**，距 REGULAR 线 1.58 差 0.27。P86 只做最后一轮几何对位（sector / subindustry / market / 双桶和 / leaps 与 equity2b2 换族），
若仍不过 1.4 则按「几何定 S 天花板」判死整集，不再追加。

## 四、工具坑

- validate_expressions 参数键是 alpha_expressions；且该工具硬编码按 USA/TOP3000 取字段表，KOR 字段一律误判 unknown_fields，
  本区字段存在性只能以 get_datafields(region=KOR) 为准。
- search_forum_posts 参数键是 search_query，且当前账号下该接口 180s 无响应（两次均超时），论坛检索在本区不可用，需改用外部 web 检索。