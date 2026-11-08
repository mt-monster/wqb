# KOR × insiders wave290/291 归因与改进（2026-11-06）

## 1. wave290 批 A：库藏股族 → ⛔ 机制判死

批 `1EVOpgcSV4wO8D7kldBktIz`，8/8 COMPLETE，error 0。设置 R&M / d4 / trunc 0.08 / nanH OFF。

| alpha | 表达式 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| qMLOj8QK | ts_delta(vec_avg(trsy_ratio),55) sector | 0.51 | 0.19 | .2340 | 0.21 |
| mLodjpEp | ts_delta(vec_avg(trsy_ratio),250) sector | 0.55 | 0.21 | .1988 | -0.28 |
| RRE97MG0 | vec_avg(trsy_ratio) 水平 sector | 0.43 | 0.17 | .1224 | -0.70 |
| 3qo1lw8z | ts_rank(vec_avg(trsy_ratio),250) sector | 0.57 | 0.27 | .1375 | -0.31 |
| P0ox7Nk7 | divide(trsy, 1-trsy) 对数比 sector | **-0.88** | -0.47 | .1218 | 0.37 |
| MPYd7OJ6 | ts_delta(vec_max(trsy_ratio),55) sector | 0.40 | 0.13 | .2329 | 0.08 |
| npvm79Ll | ts_av_diff(vec_avg(trsy_data),250) sector | 0.05 | 0.01 | .1276 | -0.26 |
| vR1ZjqK3 | ts_delta(vec_sum(trsy_real_ratio),55) industry | 0.39 | 0.12 | .2429 | 0.60 |

**读数**：max|S| = 0.88、max|2Y| = 0.70。预置判据（max|S|<0.8 且 max|2Y|<1.0）实际以 max|S|=0.88 轻微越线，但**无一条接近 1.3**，8 个结构互异模板（水平/季度差分/年度差分/时序分位/对数比/vec_max/股数口径/未去重+industry）全部落在 0.05–0.88。

**归因**：
1. 库藏股比例在 KOR **不是可交易的信息**——回购在韩国有强制注销与披露要求，动作一旦公告即被完全定价，且库藏股比例年际变化极小（TO 0.12–0.24 说明信号几乎不动）。
2. 对数比变换（P0ox7Nk7）拿到 -0.88，是唯一越 0.8 的读数，但 2Y 仅 0.37 ⇒ 全样本有效、近两年失效，属「旧制度红利」，无提交价值。
3. 唯一有 2Y 的是 vR1ZjqK3（0.60）但与 S 0.39 同时弱 ⇒ 该族两端口都不成立。
⇒ **库藏股族判死，不扫窗口、不换分组轴**（8 模板已覆盖主要几何）。

## 2. wave290 批 B：控制权集中度族 → ⭐ 挖到强负向信号

批 `1gWiweg6z4js9BdyEikMcTd`，8/8 COMPLETE，error 0。

| alpha | 表达式 | S | F | TO | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---|
| e75Nzaw6 | group_rank(vec_avg(source_ratio), sector) | **-1.55** | -1.29 | .1296 | **-2.05** | ⭐ 取负即 1.55/2.05 |
| rKR9j73J | group_rank(vec_avg(tnc), sector) | 1.51 | 1.22 | .1298 | **0.08** | ⛔ 2Y 结构性不可达 |
| vR1ZjA3d | ts_std_dev(vec_avg(source_ratio),250) sector | -1.17 | -0.81 | .0524 | -1.31 | 取负 1.17/1.31（弱于 e75） |
| akKe7aZ5 | ts_delta(vec_avg(source_ratio),250) sector | -1.15 | -0.58 | .1896 | -0.12 | 差分轴弱 |
| j2YojaEk | ts_delta(vec_avg(tnc),250) sector | 0.84 | 0.34 | .1990 | -0.91 | 二维同弱 |
| xArVjv8w | ts_rank(vec_avg(tnc),250) sector | 0.68 | 0.31 | .1381 | -0.55 | 弱 |
| 88RVlNdV | ts_delta(vec_avg(real_ratio),55) sector | -0.07 | -0.01 | .2362 | -1.04 | 无信号 |
| wpQ3jogx | ts_std_dev(vec_sum(tnc),66) industry | 0.05 | 0.01 | .0678 | 0.22 | 无信号 |

### ★ 归因：为什么「存量持股集中度」是强负向

| 项 | 内容 |
|---|---|
| 被定价的是什么 | 内部人/关联方的**存量控制权集中度**（去重持股比例），不是交易行为 |
| 方向为何是负 | KOR 财阀（재벌）结构下，控股家族持股越集中，**少数股东治理折价**越大：关联方交易、隧道效应（tunneling）、继承安排都会侵蚀小股东价值 ⇒ 集中度是**代理成本**的代理变量 |
| 与已交付 2 颗的关系 | kqNv1xRk/RRE9NkVj 走的是**交易流量的横截面分歧度**（谁在动、动得一致吗）；本族走**存量结构**（谁持有、持有多集中）⇒ 机制正交，self 风险低 |
| 与 tnc 的关系 | tnc（关联方数量）S 1.51 但 2Y 0.08 ⇒ 关联方「数量」是慢变量（几年不变），全样本漂移来自早年制度差异；而 source_ratio「比例」的 2Y 达 -2.05 ⇒ **比例含信息、数量不含** |
| 2Y 为何极强 | 2020 后 KOR 治理改革（商法修订、Stewardship Code）抬高少数股东话语权 ⇒ 高集中度折价被加速重定价 |

## 3. wave291 改进波次（目标：把 1.55 推过 1.58）

批 A `NyKcKc5x4O6aOKvGUy8FwK` / 批 B `3vxhrG7Vu4qtcdPO16pJOkO`（各 8 条，R&M / d4 / trunc 0.08 / nanH OFF）

| # | 结构 | 改进维度 |
|---|---|---|
| A1 | subtract(0.5, group_rank(vec_avg(source_ratio), sector)) | 基线，确认方向 |
| A2 | ... group_rank(..., industry) | 分组轴 industry |
| A3 | ... group_rank(..., market) | 分组轴 market |
| A4 | group_neutralize(subtract(0.5, group_rank(..., sector)), industry) | 双层中性化（wave287 实证 S+0.17/F+0.16/prod-0.043 五项同向） |
| A5 | 换 source_real_ratio（未去重 raw 口径） | 字段口径 |
| A6 | 换 real_ratio（去重 raw 口径） | 字段口径 |
| A7 | 降维换 vec_max | 向量降维算子 |
| A8 | 内层加 ts_mean(...,22) 平滑 | 时序平滑 |
| B1 | 降维换 vec_sum | 向量降维算子 |
| B2 | 内层换 ts_rank(...,250) | 时序分位几何 |
| B3 | 分组轴 subindustry | 分组轴 |
| B4 | 外层 group_neutralize(..., sector)（反序双层） | 中性化顺序 |
| B5 | group_rank(vec_avg(tnc), industry) | 救 tnc 的 2Y |
| B6 | group_rank(vec_avg(tnc), market) | 救 tnc 的 2Y |
| B7 | group_neutralize(group_rank(vec_avg(tnc), sector), industry) | 救 tnc 的 2Y |
| B8 | subtract(0.5, group_rank(divide(vec_avg(source_ratio), add(vec_avg(tnc),1)), sector)) | 人均集中度（复合轴） |

## 4. 预置判据

- A1 必须复现 S ≈ 1.55 / 2Y ≈ 2.05（否则说明取负方向错，全批作废重判方向）。
- 任一结构 S ≥ 1.58 且 2Y ≥ 1.58 ⇒ 立刻查 self-corr（对已提交池）+ prod，转 S5。
- 全批 max|S| < 1.45 ⇒ source_ratio 族天花板已定，不再扫参数。