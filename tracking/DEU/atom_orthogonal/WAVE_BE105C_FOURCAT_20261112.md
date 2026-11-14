# BE105c 判决：sentiment27 attention 面首轮（2026-11-12 深夜 4）

批 4CjzFOfQ4OKbPbqyyWMviT（vec_avg 包裹 EVENT 字段）｜decay4/SUBINDUSTRY/nan ON｜10 臂 0 错误

| # | 臂 | 机制 | S | 2Y | TO |
|---|---|---|---:|---:|---:|
| 1 | E5QOQZG1 | -rank level（高关注反转，Da-Gao） | 0.35 | 0.27 | 6.8% |
| 2 | kqaEaG06 | -rank mean66 | 0.05 | −0.19 | 2.5% |
| 3 | xAvOvGdm | -rank Δ22（关注尖峰反转） | −0.03 | 0.06 | 18.4% |
| 4 | rK7p7GP9 | -rank zscore252 | 0.32 | 0.30 | 12.9% |
| 5 | leapaGWO | -relpopularity08 | **−0.71** | −1.41 | 2.0% |
| 6 | qM797GNP | -relpopularity1 Δ66 | 0.04 | −0.92 | 8.4% |
| 7 | **QP0Z0zGW** | **rank 分布 skewness** | **0.90** | **1.14** | 7.0% |
| 8 | **N1PxPz7w** | **rank 分布 kurtosis** | **0.88** | **1.12** | 7.3% |
| 9 | 78Y7Ymjx | 尖峰 ts_rank252 | −0.23 | −0.04 | 19.3% |
| 10 | 1YWkWKwW | 尖峰波动比 | 0.05 | 0.10 | 18.8% |

**关键发现**：**rank 分布的二阶矩（skewness 0.90 / kurtosis 0.88，2Y 双 1.1+，TO 7%）是本集最强机制面**——域名排名分布的偏度/峰度 = 公司网络关注结构的不对称/极端度，学术对应「关注结构稳定性溢价」（与 Fang-Peress 低关注溢价同族：排名分布越「尖峰偏斜」（少数极端域名主导），市场覆盖越窄 → 溢价）。而一阶矩（rank level/mean/zscore）全弱 ≤0.35 —— **关注度水平无信号，关注度结构有信号**。
relpopularity08 是唯一强负臂（−0.71，2Y −1.41）：复合热度越高 → 未来越差（Da-Gao 反转方向的直接证据，但负号不可提交，翻号后 = 低热度做多 ⇒ 与 skewness/kurtosis 同向）。

**升级判定**：skewness/kurtosis 双臂 0.88-0.90，落在 1.0-1.2 定向补带边缘（差 0.10-0.12）⇒ **BE105d 定向补**：二阶矩族的窗口/变换扩展（mean66/132 平滑、zscore252、rank 化、+relpopularity 负号组合、与 kurtosis 合成、结构稳定性复合分）。

## 四类战役第 1 轮汇总（5 集 × 10 机制普查）

| 集 | 首轮 max | 升级动作 |
|---|---:|---|
| institutions6 | 0.29 | BE103b 二轮（存量族 + unit 错误修复） |
| insider_agg_matrix | **0.85**（significant_value_1，2Y 1.57 双高） | **BE104b 定向补**（事件强度族） |
| sentiment27 | **0.90**（skewness，2Y 1.14） | **BE105d 定向补**（二阶矩族） |
| fund_holdings_panel | 0.54（三族 2Y 1.36-1.42） | BE106b 定向补（长窗/平滑/组合） |
| sentiment33 / insiders1 / institutions4/25 / risk60/88/72/68/71 / sentiment7 | 待普查 | BE107-111 排队 |
