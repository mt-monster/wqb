# BE98 设计档：NEWS 塔事件流量计数（EUR 唯一非模型胜件的同源机制，2026-11-12）

> 触发：DEU **NEWS 塔 = 0**（17 个 news 数据集），而 news50/news18 携带真正的「事件流量计数」字段。
> 关键边界：DEU 的 news50 在 WAVE_BE38 是按**情绪/事件情绪通道**判死的（0.29-0.79），
> **计数面从未测过**；而 EUR 侧同源机制（`vec_avg(ravenpack_sum_story_count)` S 2.72 / prod 0.6403、
> `rp_story_event_count` S 2.15）是 EUR 唯一逃出 prod 地板的非模型信号。
> ⇒ 这是「同数据、不同字段维度」的真空档，不是重试。

## 字段（get_datafields 实测，非画像）

| 记号 | 字段 | 数据集 | 类型 | cov | ac |
|---|---|---|---|---:|---:|
| A | mws50_rp_story_event_count | news50 | VECTOR | 0.7644 | 2 |
| B | multi_entity_story_event_count | news18 | VECTOR | 0.9788 | 5 |
| C | story_event_record_count | news18 | VECTOR | 0.6965 | 5 |

## 10 臂（算子 3-7，均 ≤12）

| # | 构造 | 机制 |
|---|---|---|
| 1 | group_rank(ts_sum(vec_sum(A),66),sector) | 裸流量基线（无 tail，测并列块伤害量） |
| 2 | tail(winsorize(group_rank(ts_sum(vec_sum(A),66),sector),std=2),lo=.25,hi=1,nv=0) | 记忆配方：tail 掐并列块 |
| 3 | 同上，窗 22 | 短窗流量 |
| 4 | 同上，窗 252 | 长窗流量 |
| 5 | tail(...B 窗 66...) | 高覆盖替代字段（cov 0.98） |
| 6 | tail(ts_zscore(ts_sum(vec_sum(B),22),252)) | 流量**变化**（zscore 化） |
| 7 | tail(...C 窗 66...) | 第三计数变体 |
| 8 | tail(divide(ts_sum(vec_sum(A),22),add(ts_sum(vec_sum(A),252),0.0001))) | 流量**加速**（短/长比） |
| 9 | multiply(-1, tail(...A 窗 66...)) | 关注度→反转（方向对立假设） |
| 10 | tail(add(ts_sum(vec_sum(A),66),ts_sum(vec_sum(B),66))) | 双字段合成（稳健性） |

设置：DEU/TOP500/D1，decay4，SUBINDUSTRY，trunc0.08，nan ON（事件型若要试 OFF 留 L2）。

## 判读线（协议 v2 L1）

- max |S| ≥1.2 ⇒ L2 满波（窗阶梯 + 设置档 nan ON/OFF × 中性化）；
- 1.0-1.2 ⇒ 定向 10 臂（字段族 4 个 + 窗 3 档 + 矩 3 档）；
- <1.0 ⇒ NEWS 塔计数面判死，出 v2 证书（并写明「情绪面 BE38 已判死 + 计数面本波判死」两段）。
