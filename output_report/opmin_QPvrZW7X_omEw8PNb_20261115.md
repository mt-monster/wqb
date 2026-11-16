# `QPvrZW7X` / `omEw8PNb` 优化报告：算子压到 7 / 5，但 prod 早已超线

- 日期：2026-11-15
- 区域 / 设置：USA / TOP3000 / D1 / decay 8 / **SLOW_AND_FAST** / trunc 0.08
- 实跑 14 条仿真（1 批 8 条 multisim + 6 条 per-item settings）

## 1 结论

| 目标 | 结果 |
|---|---|
| 压算子 | **成功且零损失**：`QPvrZW7X` 9→**7**、`omEw8PNb` 7→**5**（变量合并，指标逐位相同） |
| 推全闸 | 原本就全过（唯一 WARNING 是 omE 的 CLUSTER 1.16） |
| **能否提交** | **不能**。两颗的 prod 实测 **0.9609 / 0.8002**，远超 0.7 |

> **关键纠正**：外部引用的 `prod .5289 / .5745` 来源是 `alpha_corr_cache.source=prod_artifact`、`created_at=2026-11-02`，**已过期 13 天**（>48h 作废）。今天用与原件**信号逐位相同**的变量合并孪生重测，得 .9609 / .8002。

## 2 压缩（第 0 步：重复子式合并）

两式里 `ts_mean(divide(executed_short_position_share_sum, aggregate_trade_share_count_regular_hours), 22)` 各出现 **两次**，是白送的算子数。

```text
# QPvrZW7X：9 → 7
core = ts_mean(divide(executed_short_position_share_sum, aggregate_trade_share_count_regular_hours), 22);
multiply(subtract(ts_zscore(core, 126), ts_zscore(core, 504)), rank(aggregate_trade_share_count_regular_hours))

# omEw8PNb：7 → 5
core = ts_mean(divide(executed_short_position_share_sum, aggregate_trade_share_count_regular_hours), 22);
subtract(ts_quantile(core, 126, driver="gaussian"), ts_quantile(core, 504, driver="gaussian"))
```

| 原 id | 原件 ops | 合并后 id | 合并后 ops | 指标 | prod |
|---|---:|---|---:|---|---|
| QPvrZW7X | 9 | **`E5QaWr0P`** | **7** | S2.45/F1.77/TO.1064/sub1.85/2Y2.77/clu2.12 **逐位相同** | **.9609** |
| omEw8PNb | 7 | **`xAvz8m9J`** | **5** | S2.42/F1.56/TO.1013/sub2.03/2Y2.10/clu2.35 **逐位相同** | **.8002** |

## 3 脱相关尝试（全部失败）

| 变体 | oc | S | sub | 2Y | **prod** | 判定 |
|---|---:|---|---|---|---|---|
| A1 = QP 合并（zscore 差 + rank 门） | 7 | 2.45 | 1.85 | 2.77 | **.961** | ✗ |
| A2 去掉 rank 门 | 5 | 2.33 | 1.90 | 2.25 | **.866** | ✗ |
| A3 quantile-gaussian 差 + rank 门 | 7 | **2.57** | 2.03 | 2.54 | **.894** | ✗ |
| A4 `ts_rank` 差（无门） | 5 | 2.43 | 1.89 | 2.23 | **.771** | ✗ |
| A5 = omE 合并 | 5 | 2.42 | 2.03 | 2.10 | **.800** | ✗ |
| A7 单窗口（3 ops） | 3 | 0.59 | 0.33 | 1.18 | — | ✗ S 崩 |
| C1 QP 换 TOP1000 | 7 | 1.80 | 0.93 | 1.61 | — | ✗ sub FAIL |
| C2 QP 换 TOP500 | 7 | 1.09 | 0.92 | 1.91 | — | ✗ 三闸 FAIL |
| C4 omE 换 TOP1000 | 5 | 1.83 | 0.84 | 1.06 | — | ✗ sub/2Y FAIL |
| C5 omE 换 TOP500 | 5 | 1.18 | 0.64 | 1.37 | — | ✗ 四闸 FAIL |
| C3/C6 delay 0 | — | — | — | — | — | 字段在 D0 不可用（unknown variable） |

**最低 prod 也只有 .771**（`ts_rank` 差版），仍在 0.7 之上。`rank(...)` 门不是冗余——去掉它 prod 从 .961 升到 .866 的同时 S 掉 0.12，两头都亏。

## 4 判断

该族（`executed_short_position_share_sum ÷ aggregate_trade_share_count_regular_hours` 的快慢差）**已经在美国生产池里**，任何等价改写都在 `.77–.96` 区间。

- 不是「优化不够」，是**同源**：prod 反映的是与已提交 alpha 的信息重合，不是指标好坏。
- 缩宇宙（TOP1000/500）与 delay 0 两条路都被闸或字段挡住。
- 唯一可能的出路是换信息源（换分母字段 / 换另一个 activity 度量），那是**重做一个 alpha**，不是优化这两颗。

## 5 产物

- `E5QaWr0P`（7 ops）、`xAvz8m9J`（5 ops）、`6XMqVY3P`、`akaPZWMR`、`leazORkl`、`j2awR71O` 等全部留档，**均不提交**；其中 `xAvz8m9J` 可作为「omE 族 5 算子等价件」在任何后续复用场景直接取用。
- 本轮 **零提交**。
