# 低频算子模板回测结果（USA / TOP3000 / D1，2026-11-14 16:4x GMT+8）

> 30 条模板 / 3 批（B1 Logical 族、B2 分布与组内、B3 记忆截面与向量）。
> **结果：18 条指标可读、12 条被平台拒绝；可读件里最好的 `normalize` S 1.81 但 F 0.69（<1.0 闸），
> 因此本轮 `LOW_SHARPE≥1.58 + LOW_FITNESS≥1.0` 双闸通过数 = 0。**

## 0 总览

| 批 | 主题 | 提交 | 可读 | 被拒 | 最好 S | 最好 F |
|---|---|---:|---:|---:|---:|---:|
| B1 | Logical 族条件化 | 10 | 0 | 10 | — | — |
| B2 | 分布形状/组内/缺失 | 10 | 8 | 2 | 0.90 | 0.86 |
| B3 | 记忆/截面/协方差/向量 | 10 | 10 | 0 | 1.81 | 0.69 |

multisim：B1 `2usFprdZV4hsc2ZApbbUJW`｜B2 `3RSBiE4WY53N9xpenv6hOaw`｜B3 `1enkcpaAR4hMajO1k6QclZU`。

## 1 ★ 第一类失效：USA 的 reversion 政策（B1 全批 10 条作废）

B1 十条全部返回同一条平台告警，且**不给任何指标**（sharpe/fitness 均 null）：

```text
Alpha expression includes a reversion component so we may not accept these alphas
in the future, try working on different alpha ideas.
```

B1 的设计骨架是 `-ts_delta(close, n)` / `-returns`（短期反转），被平台判定为 reversion 组件。
**这不是语法错误，是通道政策**——仿真照跑但结果作废，等于白跑。
⇒ **USA 区不要再投纯价格反转骨架**；同区的价格动量方向同样为负（见 §2 的 `power` S −2.03、
`pasteurize` S −2.03、`min` S −1.66），说明 USA 短期收益既吃不到动量、反转又被政策禁，
必须转向**量能 / 波动 / 覆盖 / 市值 / VECTOR** 这些非价格维度。

## 2 第二类失效：单位族（3 条语法对但单位错）

| alpha | 表达式片段 | 平台报错 | 修正 |
|---|---|---|---|
| `78Ygoxl8` | `add(1, returns)` | `expected "Unit[]", found "Unit[CSPrice:1]"` | 改 `ts_zscore(returns,20) + 3`（无量纲） |
| `1YW6jo0m` | `sqrt(ts_std_dev(returns,60))` | `sqrt expected "Unit[]", found "Unit[TSPrice:1]"` | 改 `sqrt(ts_zscore(ts_std_dev(returns,60),252))` |
| `akaXVPGv` | `less(ts_delta(close,5), -0.03)` | `less expected "Unit[TSPrice:1]", found "Unit[]"` | 改 `less(ts_zscore(volume/adv20,20), -1)` |

这三条是**发批前四闸没能拦住的新单位族**：闸④ 原本只覆盖 `group_*(x, bucket(...))` 与 `vector_neut` 轴，
本轮补了三条规则——`sqrt/log/power` 不可直接吃价格单位、裸价格/收益不可与常数直接比较或相加、
`sqrt` 内层必须先是 `ts_zscore`/`rank` 这类归一化算子。

## 3 第三类失效：信号被中和（`kth_element`）

`rank(kth_element(close, 250, k=1) - kth_element(close, 500, k=1))` 跑出 **S 0.00 / TO 0.0000**：
`kth_element(·, 250, k=1)` 与 `kth_element(·, 500, k=1)` 在绝大多数日子取到同一个回填值，差恒为 0，
经 SUBINDUSTRY 中性化后彻底归零。修正版改用**相对量能**的 20 日 vs 60 日水平差。

## 4 18 条可读结果（按 Sharpe 降序）

| # | 批 | 主算子 | alpha | S | F | TO | 2Y | sub | FAIL | 结论 |
|---:|---|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | B3 | `normalize` | `GrmEgda3` | 1.81 | 0.69 | 0.8274 | 2.55 | 1.40 | LOW_FITNESS,HIGH_TURNOVER | S 过 F 不过 |
| 2 | B2 | `ts_count_nans` | `2r5Pjv2P` | 0.90 | 0.86 | 0.0420 | 2.14 | 0.43 | LOW_SHARPE,LOW_FITNESS | S 不过 |
| 3 | B3 | `vec_range` | `KPgxmOjx` | 0.82 | 0.47 | 0.2235 | 2.13 | 0.62 | LOW_SHARPE,LOW_FITNESS,CONCENTRATED_WEIGHT | S 不过 |
| 4 | B3 | `ts_covariance` | `vRAaOkqr` | 0.57 | 0.25 | 0.0737 | 1.67 | 0.53 | LOW_SHARPE,LOW_FITNESS | S 不过 |
| 5 | B3 | `vec_range` | `bla78RZ6` | 0.50 | 0.08 | 0.7645 | 0.26 | -0.04 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 6 | B2 | `group_count` | `WjlKLNJx` | 0.05 | 0.01 | 1.0055 | — | 0.83 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,CONCENTRATED_WEIGHT,IS_LADDER_SHARPE | S 不过 |
| 7 | B2 | `group_std_dev` | `RRe0ANP1` | 0.02 | 0.00 | 1.1718 | 0.20 | 0.32 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,CONCENTRATED_WEIGHT,LOW_2Y_SHARPE | S 不过 |
| 8 | B2 | `ts_kurtosis` | `WjlKLN0P` | 0.01 | 0.00 | 0.0769 | -0.36 | -0.31 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 9 | B3 | `vec_min` | `O0WKJrE1` | -0.06 | 0.00 | 0.8150 | 0.64 | -0.06 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 10 | B2 | `group_sum` | `3q0gjEJ0` | -0.18 | -0.04 | 1.1337 | -0.16 | -0.39 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,CONCENTRATED_WEIGHT,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 11 | B3 | `ts_step` | `gJa7WQ6l` | -0.20 | -0.08 | 0.0196 | -0.18 | -0.12 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 12 | B3 | `inverse` | `rK7Qd5g3` | -0.22 | -0.05 | 0.1527 | -0.27 | -0.33 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 13 | B3 | `vec_min` | `MP6901Rk` | -0.85 | -0.63 | 0.1621 | -1.70 | -0.27 | LOW_SHARPE,LOW_FITNESS,CONCENTRATED_WEIGHT,LOW_2Y_SHARPE | S 不过 |
| 14 | B3 | `vec_range` | `6XMgArVP` | -1.20 | -0.33 | 1.3861 | -0.24 | -0.49 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,CONCENTRATED_WEIGHT,LOW_2Y_SHARPE | S 不过 |
| 15 | B3 | `min` | `vRAaOkqb` | -1.66 | -0.53 | 0.6904 | -2.54 | -1.12 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 16 | B2 | `power` | `LLKO5n3e` | -2.03 | -0.81 | 0.8356 | -2.19 | -1.62 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 17 | B2 | `pasteurize` | `XgaXRkOm` | -2.03 | -0.66 | 0.8258 | -2.00 | -1.31 | LOW_SHARPE,LOW_FITNESS,HIGH_TURNOVER,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE | S 不过 |
| 18 | B2 | `kth_element` | `A1xqQn2g` | 0.00 | 0.00 | 0.0000 | — | — | LOW_SHARPE,LOW_TURNOVER,CONCENTRATED_WEIGHT | S 不过 |

**读法**：
- 唯一 S 上 1.58 的是 `normalize`（S 1.81），但 **F 0.69** 距 1.0 门槛差 0.31，且 TO 0.83 偏高。
- `ts_count_nans`（S 0.90 / **F 0.86** / TO **0.042**）是全轮**fitness 最高、换手最低**的一条——
  它测的是「日收益缺失次数」，属于数据质量类信号，与价格完全正交，值得作为辅助腿而非主信号。
- `vec_range`（S 0.82 / F 0.47）测分析师聚类估计分歧度，`ts_covariance`（S 0.57 / F 0.25）测量价协方差，
  这两条方向正确但强度不足，需要换载体或叠加门控。
- **负值那几条本身就是信息**：`power` S −2.03、`pasteurize` S −2.03、`min` S −1.66，说明
  「收益 z 的单调变换」在 USA 是反向的（动量亏），但反向即反转 ⇒ 撞 §1 的政策，不可行。

## 5 B4 修正批（12 条，绕开 reversion + 修单位）

12 条**全部 COMPLETE、零 reversion 警告**——说明「非价格反转」的设计有效，Logical 四个算子的语法路径彻底打通。

| # | 主算子 | alpha | S | F | TO | 2Y | sub | FAIL |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | `not` | `P05joj6w` | 0.21 | 0.03 | 0.3662 | 0.31 | 0.28 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 2 | `greater_equal` | `kqaeNeXg` | 0.13 | 0.03 | 0.1936 | 0.42 | 0.09 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 3 | `less_equal` | `akaXKXlw` | 0.08 | 0.01 | 0.0676 | -0.07 | -0.40 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE |
| 4 | `equal` | `LLKOMOXL` | -0.75 | -0.40 | 0.2155 | -0.97 | -0.43 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE |
| 5 | `is_nan` | `rK7QRQzm` | 0.74 | 0.77 | 0.2581 | 1.81 | 1.00 | LOW_SHARPE,LOW_FITNESS,CONCENTRATED_WEIGHT |
| 6 | `not_equal` | `6XMgdgqY` | 0.46 | 0.09 | 0.3906 | 0.35 | 0.29 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 7 | `and` | `N1PkNkj7` | -0.52 | -0.14 | 0.5479 | -0.66 | -0.06 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 8 | `or` | `akaXKXPw` | -0.21 | -0.03 | 0.6307 | 0.19 | -0.01 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 9 | `ts_product` | `xAvXrXmq` | -0.47 | -0.15 | 0.2080 | 0.01 | -0.55 | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE |
| 10 | `sqrt` | `d5aeWelg` | 0.12 | 0.02 | 0.2071 | 0.18 | 0.17 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 11 | `kth_element` | `YPaX1g9J` | 0.00 | 0.00 | 0.0000 | — | — | LOW_SHARPE,LOW_TURNOVER,CONCENTRATED_WEIGHT |
| 12 | `less` | `E5Qo6eM0` | 0.03 | 0.00 | 0.5512 | -0.32 | 0.32 | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |

**`kth_element` 二次证伪**：改用量能 20 日 vs 60 日水平差后仍是 **S 0.00 / TO 0.0000**
（`LOW_TURNOVER` + `CONCENTRATED_WEIGHT` FAIL）。原因是 `kth_element(x, d, k=1)` 对连续有值的字段
就是「最近一个有效值」，两个窗口取到同一个数，差恒为 0 ⇒ **该算子的正确定位是缺失回填（k=1 等价
ts_backfill）或 k>1 取更早的有效值，不是取窗口水平差**。

**唯一亮点 `is_nan`**（`rank(-ts_mean(is_nan(ts_delta(volume,1)), 20))`，即「日量能缺失率」）：
**2Y  Sharpe 1.81、sub 1.00 两项副闸都过**，TO 仅 0.258，只差主闸（S 0.74 / F 0.77）与 CW。
这与 B2 的 `ts_count_nans`（S 0.90 / F 0.86 / TO 0.042 / 2Y 未测）互相印证：
**「数据质量 / 覆盖完整度」类信号在 USA 是稳定但偏弱的正交方向**，正确用法是辅助腿而非主信号。

其余 10 条 S 落在 −0.75 ~ 0.46：Logical 门控能跑通但强度不足，`ts_product` / `sqrt` 修完单位后
仍为负/近零——这两个算子的金融假设（复合增长、波动平方根）在当前设置下没有超额。

## 6 结论与下一步

| 结论 | 依据 |
|---|---|
| 低频算子**语法**全部可用 | 18 条正常出指标，无一条因算子名/参数报错 |
| 但**多数方向在 USA 不成立** | 价格类全部负向或撞 reversion 政策；只有量能/覆盖/分歧度类为正 |
| 单位族是本轮最大隐性成本 | 3/30 直接报废，且都是「看起来最自然」的写法 |
| 单算子裸用强度普遍不足 | 18 条里 F≥0.8 仅 1 条（`ts_count_nans`） |

**下一步（若要继续推）**：
1. 把 `ts_count_nans`（数据质量）与 `vec_range`（分析师分歧）做成**辅助腿**，挂到已过闸的主信号上做条件/分组，
   而不是单独当 alpha——这两类与价格正交，是 prod 墙较低的方向。
2. `not` / `greater_equal` / `less_equal` / `equal` 四个 Logical 算子已证明**语法可用**（B4 修正批），
   后续只作为**门控**使用，不作为信号主体。
3. 不在 USA 继续投价格反转；如需价格维度，换 GBR / EUR / IND 等未观测到该政策的区域再验证。

## 7 边界

- 本轮为**探索性回测**，全部 alpha 为 UNSUBMITTED，**零提交**。
- 统一设置 `USA/TOP3000/D1/decay4/SUBINDUSTRY/trunc.08/nan ON/2013–2023`，结论不跨区外推。
- 平台对 reversion 组件的判定是**通道政策**而非指标评价，本轮据实记录，不尝试绕过。
- 指标口径只认 `is.sharpe` / `is.fitness` / `is.turnover` 与 `is.checks`，未做 prod/self 相关性探测
  （30 条里没有一条过 S+F 双闸，探测 prod 无意义）。
