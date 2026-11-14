# 判死：shortinterest3 的次级维度全无信息（BE147）

日期：2026-11-12
multisim `1zaICTbQS5fwcKqr17dma29`（10 臂）

## 实测：10 臂全灭

| 腿 | alpha | S | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|
| 最低费率 | E5Q1V0eG | 1.11 | 1.43 | 0.64 | 3 |
| S3+借券期限 | 58Jxj7kX | 1.09 | 1.22 | 0.40 | 4 |
| 借券期限 | zqdZrwR1 | 0.98 | 1.32 | 0.44 | 4 |
| S3+费率波动 | 88NbvkeX | 0.95 | 0.83 | 0.35 | 4 |
| 波动率变化 | xAvq1wdb | 0.93 | 1.19 | 0.53 | 3 |
| 费率波动率 | pwamvJlb | 0.83 | 0.88 | 0.35 | 4 |
| 交易笔数 | RReMAZ1a | 0.80 | 0.91 | 0.20 | 4 |
| 波动+期限 | leadM6WO | 0.43 | 0.26 | 0.12 | 4 |
| 费率波动单腿 | blaX82QM | **−1.12** | −2.43 | −0.69 | 4 |
| 借券期限单腿 | LLKW5bG9 | **−0.79** | −1.39 | −0.60 | 4 |

## 判死结论

**shortinterest3 只有两个字段有 alpha：`shrt3_bar`（借券需求评分）与 `max_loan_rate_p5_d1`（最高借券利率）**，两者已分别用于已交付件 `78Yk8VR1`(d5a2vxzY) 与 `qM7KxkQV`。

次级维度全部无效：
- `loan_rate_volatility_p5_d1`（费率波动率）→ 单腿 **−1.12**
- `average_loan_duration_days_p5_d1`（借券期限）→ 单腿 **−0.79**
- `transaction_count_p5_d1`（交易笔数）→ 单腿弱
- `min_loan_rate_p5_d1`（最低费率）→ 1.11

⇒ **SHORTINTEREST 塔在 DEU D1 已挖尽**（含 25 字段中的核心 2 个 + 4 个次级维度全测）。

## 合并判死清单（本战役）

| 数据集/族 | 判死依据 |
|---|---|
| **RISK**（rsk60_crowding / rsk60_offer / lending_fee_bid_rate）| 单腿 −0.24/−0.86，组合 1.04-1.37 |
| **SHORTINTEREST 次级维度**（volatility/duration/count/min_rate）| 单腿 −1.12/−0.79，组合 ≤1.11 |
| **insiders 非 holdings 维度**（valueeur/shares比/significance/price）| 全灭，最高 1.29 |
| **OTHER（other455 竞争PCA）** | 1.21，弱于关系PCA |
| **SENTIMENT（域名热度）** | 单腿 0.72，组合 1.37 |
