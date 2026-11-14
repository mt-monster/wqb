# DEU 战役五轮检查点审计（2026-11-10 15:53 checkpoint）

## ★ 核心恢复：候选池扩容，RREPm361 复活为全清待授权

对 2026-11-08 遗留篮子的三颗全闸 ATOM 重新终验（self 本地重算 + prod 平台刷新 + submit gate 预检 + 边际贡献）：

| alpha | 数据集 | S | F | 2Y | prod(refresh) | self | delta S | 终判 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| RREPm361 | analyst7 | 2.02 | 1.25 | 1.82 | 0.6881 PASS（余量 0.012 贴线） | 0.3275 PASS | +0.73 正向 | 全清，待用户授权 |
| QPvzNNGG | predictive_starmine | 1.70 | 1.30 | 2.18 | 0.6777 PASS | 0.6779 PASS | -0.04 稀释 | 硬闸阻断（稀释铁律，force 不豁免） |
| QPv6jLvX | analyst93 | 1.59 | 1.52 | 2.01 | 0.992 FAIL（新算非缓存） | 0.5227 | - | prod 撞死（生产池已入同构件） |

RREPm361 稳健性审计（本轮补齐，已落账 robustness_RREPm361）：
- 逐年 S（2014-2023）：3.06 / 2.43 / 1.28 / 2.40 / 1.52 / 1.06 / 2.10 / 3.01 / 2.26 / 1.29
- 零负年、零空窗、最低年 1.06；近三年均值 2.19；3y 总体 CV = 0.322（<0.40 即 PASS 带）
- 表达式（5 算子）：group_rank(add(ts_zscore(est_12m_ebt_mean,240), ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago),66)), sector)
- prod 余量仅 0.012，提交前一刻必须再 refresh；若届时 >0.70 按铁律作废重排。

1YNMAA8M / E569ZE7L 复核：gate PASS、ΔS +0.43 / +0.06 均非稀释，结论不变。

## 当前全清待授权池（3 颗）
| 顺位 | alpha | 数据集 | S | delta S | prod 余量 | 备注 |
|---|---|---|---:|---:|---:|---|
| 1 | RREPm361 | analyst7 | 2.02 | +0.73 | 0.012 | 零负年，自相关最低 0.33 |
| 2 | 1YNMAA8M | analyst7+analyst15 | 1.58 | +0.43 | 0.005 | MODEL+ANALYST 双塔 |
| 3 | E569ZE7L | shortinterest3 | 1.68 | +0.06 | 0.156 | 稳健性 CONDITIONAL（CV 0.626） |

QPvzNNGG（S1.70）被稀释铁律挡，除非用户明示豁免。

## DEU D0 新矿脉（本检查点探明）
- get_platform_setting_options：DEU 支持 delay=0（TOP500）；
- get_pyramid_alphas：DEU/D0 全塔 0 颗（完全未点亮）；
- get_datasets(DEU, delay=0)：70 个数据集可用（model216 cov0.71/45f/ac97、analyst44 cov0.77/319f/ac81、fund_holdings_panel cov0.88、shortinterest3 cov0.77 等）；
- D0 与 D1 是不同分区（ΔS 各自可比），D1 判死不自动传导；ATOM 可在此重新开矿。
- 待用户确认：region 未换满足 goal，但 delay0 是否属「换数据集」边界 —— 列入待裁定。

## 台账动作
- wqb-db：robustness_RREPm361 (PASS) / submit_verdict_QPvzNNGG (BLOCKED_MARGINAL_DILUTION) / submit_verdict_QPv6jLvX (DEAD_PROD_WALL)
- 本文件 = checkpoint 审计记录
