# Wave F 收割（insd5 tnc 窗口阶梯）— 2026-11-07

settings: KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · nan OFF
两批: `1oMV9efS553M9NKMQw4DYbM`(8条) + `1xLodWbw24yibaJ1dDIhdTLK`(2条) · 10/10 COMPLETE · 0 error

| # | 机制 | alpha | S | F | 2Y | TO | raFail |
|---|---|---|---:|---:|---:|---:|---:|
| F-01 | ts_mean(vec_stddev(tnc),22) | RRElPgpa | 1.28 | 1.03 | 1.75 | 0.0588 | 1 |
| F-02 | ts_mean(vec_stddev(tnc),5) | 3qokJN7e | 1.30 | 1.06 | 1.76 | 0.0600 | 1 |
| F-03 | ts_mean(vec_stddev(tnc),66) | P0oYKVpM | 1.28 | 1.03 | 1.73 | 0.0584 | 1 |
| F-04 | ts_mean(vec_stddev(tnc),126) | e75VEjON | 1.28 | 1.03 | 1.76 | 0.0582 | 1 |
| F-05 | ts_mean(vec_stddev(tnc),252) | YP1EYepJ | 1.20 | 0.94 | 1.64 | 0.0582 | 2 |
| F-06 | winsorize 后置（stddev W22） | npverEgE | 1.29 | 1.04 | 1.74 | 0.0582 | 1 |
| F-07 | ts_mean(vec_stddev(trsy_tnc),22) | 2rAXeYL8 | 0.00 | – | – | 0.0 | 5 |
| F-08 | ts_mean(vec_stddev(trsy_tnc),66) | omEJZdl2 | 0.00 | – | – | 0.0 | 5 |
| F-09 | **ts_mean(vec_avg(tnc),22)** | **npvermqE** | **1.57** | **1.33** | **1.75** | **0.0543** | **1** |
| F-10 | ts_mean(vec_stddev(tnc),22) subindustry | omEJZRr2 | 1.14 | 0.76 | 1.33 | 0.0524 | 3 |

## 归因
1. **stddev 臂整体弱于 avg 臂**：`vec_stddev(tnc)` 正向臂只有 1.20–1.30，而 `vec_avg(tnc)` 水平式 1.57。
   ⇒ 有效信息是「关联方交易数量的**水平**」，不是「截面内分布的离散度」。
2. **stddev 臂窗口平坦**：W5/22/66/126 全部 1.28–1.30，W252 降到 1.20 ⇒ 无峰、无局部最优簇，判该臂天花板 ~1.30。
3. `trsy_tnc`（库藏股族 cov 0.8728）S=0.00 / raFail=5 ⇒ **该字段在 KOR 是空值系**，整族不可用。
4. winsorize 放 group_rank **之后**只把 1.28→1.29（+0.01），改变权重几何的效果有限；放之前则幂等（已证）。
5. subindustry 分组弱于 sector（1.14 vs 1.28），与 risk 族结论一致：KOR 上 sector 是最优分组轴。

## 结论
- 主线锁定 `subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 22), sector), 0.5)` = **npvermqE**
  S 1.57 / F 1.33 / 2Y 1.75 / TO 0.0543，`ra.ra_failed_checks = [LOW_SHARPE]` 单闸，差 **0.01**。
- 下一步不是换机制，而是**同一机制的杠杆位移**：窗口 / decay / truncation / 中性化（Wave H + 设置档扫描）。