# mcr27 第二形态：prod 破墙方向记录（2026-11-22）

> 背景：RReEEgwb（jobscreated÷挂岗时长，trade_when 门控 + ts_quantile 252 + group_zscore(industry)）
> 全闸但 prod 0.8378 —— prod 池已有「jobscreated 单字段核」占位。
> 按 atom-internal-add-for-prod 经验：单字段形态被占位时，**add 组合造新 PnL 形态是唯一未试的 prod 破法**。

## 第一波探针（multisim `OZ5qQ4SH4Ml8V21biyJt6ZR`，在飞）

| 臂 | 核 | 假设 |
|---|---|---|
| A | ajnet÷mean_days_job_active | 净增速度：新字段核 + 新分母 ⇒ 双重罕见化 |
| B | jobsremoved÷mean_days_job_closed | 撤岗速度（反向机制） |
| C | rank(ajnet) | 秩化净额（去量纲） |
| D | ts_delta(jobsactive,66) | 存量变化（流量替代） |
| E | created÷num_jobs_active | 建岗率 |
| F | 原核换 subindustry | 轴对照 |

## 降 prod 候选手法（第二波候选，若第一波有 S≥1.0）

1. **add 双字段核**：`add(zscore(created 腿), zscore(removed 反向腿))` —— 同集多字段 add 合法（ATOM 保持，论坛帖 44770798147735）
2. **罕见快腿**：ts_delta(F,22) 月级差分（EUR risk70 实证最优快腿）
3. **罕见慢腿**：ts_mean(504)（无人用的长平滑）
4. **换宇宙**：TOPCS1600（EUR 降 prod 实证最优宇宙，唯一压到 0.71）

## 交付约束

- MACRO 塔 2/3，仅剩 1 席：本集最多交 1 颗
- prod 红线 0.7 无豁免（严格不等式）
