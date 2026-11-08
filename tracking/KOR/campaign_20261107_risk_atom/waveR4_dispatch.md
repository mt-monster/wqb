# Wave R4 派发（风险量族 · 按 R2 归因结论）

> 归因依据：`akKQ7jkR`（srisku−srisk 收缩幅度）是 R2 中**唯一 2022/2023 均为正**（1.79 / +0.58）的线；
> 反转族 2023 集体失效（-1.0/-1.8/-1.11）⇒ 禁入反转窗口谱，改挖风险量。

## 8 条
1. `subtract(0.5, group_rank(ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 66), sector))`（算子 4）
2. `subtract(0.5, group_rank(ts_mean(divide(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22), sector))`（算子 4）
3. `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_srisk, 66), sector))`（算子 3）
4. `subtract(0.5, group_rank(ts_delta(rsk70_mfm2_asetrd_srisk, 22), sector))`（算子 3）
5. `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_resvol, 66), sector))`（算子 3）
6. `subtract(0.5, group_rank(ts_zscore(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 252), sector))`（算子 4）
7. `subtract(0.5, group_rank(ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22), industry))`（算子 4）
8. `subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_squeeze_risk), 22), sector))`（算子 4）

- preflight valid=true
- multisim: `38uLSu9yk5jBcy85jk0fOQR`
- 设置：KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08
- 仿真≠提交
