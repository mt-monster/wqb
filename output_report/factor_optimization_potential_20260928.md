# 因子优化与提交潜力分析报告

> 生成时间：2026-09-28 11:37 | 数据源：`data/wqb.db`（submit_ready / alphas / backtest_results / expressions）

---

## 一、执行摘要

| 维度 | 数量 | 关键发现 |
|---|---|---|
| READY 可提交 | **2 颗** | 均为 IS_ONLY，需跑相关性校验 |
| BLOCKED 提交层被拒 | **5 颗** | 4 颗因 prod 被推高，1 颗双闸同时超线 |
| 高指标未提交（S≥1.58, F≥1.0） | **40 颗** | 瓶颈：IND prod 墙、MEA self 墙 |
| 高 Sharpe backtest 候选 | **30 颗** | 超高 S 但高换手，需降 TO |
| 需优化 fitness | **2 颗** | EUR 区，F<1.0 |
| 需优化 prod | **20 颗** | 几乎全部 IND，prod>0.7 |
| 需优化 self | **6 颗** | 全部 MEA，self>0.7 |
| 需优化 2Y | **20 颗** | 2Y<1.58 或 NULL |

---

## 二、READY 候选（2 颗 IS_ONLY，需相关性校验）

| alpha_id | 区域 | S | F | 2Y | TO | 中性化 | 状态 |
|---|---|---|---|---|---|---|---|
| np8VGNz3 | USA | 2.32 | 1.60 | 1.78 | 0.114 | STATISTICAL | 需 prod+self 校验 |
| VkGJ73eA | USA | 1.70 | 1.15 | 1.91 | 0.112 | INDUSTRY | 需 prod+self 校验 |

**建议**：跑 `batch_submit_verdict.py --phase2-prod` 做 prod+self 终验。若双闸 <0.7 则升级 SUBMIT_LAYER_VERIFIED。

---

## 三、BLOCKED 候选（5 颗，提交层被拒但有回升可能）

### 3.1 立即可重试（prod 仅微超线）

| alpha_id | 区域 | S | F | prod | self | 超线幅度 | 建议 |
|---|---|---|---|---|---|---|---|
| **A1Nn2vPQ** | GLB | 3.73 | 3.22 | 0.7079 | 0.123 | **仅超 0.0079** | prod 一回落立即重试；名称/描述已写好 |
| **xA392Xpb** | IND | 3.18 | 2.00 | 0.7019 | 0.691 | 双闸同时超 0.0019 | 等 prod 回落 |

### 3.2 需等 prod 回落（同族挤压）

| alpha_id | 区域 | S | F | prod | 原因 |
|---|---|---|---|---|---|
| 0mXA6jYG | GLB | 1.98 | 1.10 | 0.8168 | 同族 pwR8rdMg/VkaXbmbG 提交后推高 |
| 3qX6wLJQ | IND | 3.07 | 2.34 | 0.9895 | 同族 3qX3Mp6O 入池后推高 |
| 3qX6wLkP | IND | 2.84 | 1.74 | 0.9805 | 同上，同族挤压最强实证 |

**建议**：A1Nn2vPQ 是**最优先重试对象**——prod 仅超线 0.0079，且 S=3.73/F=3.22 是 BLOCKED 中指标最好的。

---

## 四、高指标未提交候选（40 颗，S≥1.58, F≥1.0）

### 4.1 按区域分布

| 区域 | 数量 | 主要瓶颈 |
|---|---|---|
| IND | 24 | prod>0.7（20 颗） |
| MEA | 14 | self>0.7（6 颗）+ 2Y NULL（8 颗） |
| EUR | 2 | fitness<1.0 |

### 4.2 IND 区高 Sharpe 候选（prod 墙）

| alpha_id | S | F | 2Y | TO | prod | 优化方向 |
|---|---|---|---|---|---|---|
| ZY7VoZq1 | 3.60 | 2.40 | 3.09 | 0.349 | 0.8617 | 降相关 |
| np7GW0oz | 3.59 | 2.39 | 3.08 | 0.336 | 0.7307 | 降相关 |
| Xg7ZZlNa | 3.52 | 2.86 | 2.84 | 0.247 | 0.8577 | 降相关 |
| MP7vxw9n | 3.30 | 2.31 | 3.21 | 0.296 | 0.9432 | 降相关 |
| gJjNlRMJ | 3.26 | 2.56 | 1.89 | 0.253 | 0.8245 | 降相关 |
| kqjppmaK | 3.22 | 2.63 | 2.71 | 0.229 | 0.9868 | 降相关 |
| LL7oRebn | 2.92 | 2.09 | 2.87 | 0.258 | 0.9312 | 降相关 |
| mLjnnzKE | 2.90 | 2.40 | 2.14 | 0.184 | 0.5951 | **prod<0.7 但 self=0.53 未终验** |

**mLjnnzKE 是 IND 区唯一 prod<0.7 的高指标候选**，但 self=0.53 未做平台终验。建议优先跑相关性校验。

### 4.3 MEA 区高 Sharpe 候选（self 墙 + 2Y NULL）

| alpha_id | S | F | 2Y | TO | prod | self | 优化方向 |
|---|---|---|---|---|---|---|---|
| 9qXxdJgr | 2.35 | 2.64 | NULL | 0.035 | 0.8073 | 0.8073 | 降 self+prod |
| 9qXx8Xa2 | 2.29 | 2.67 | NULL | 0.037 | 0.7335 | 0.7335 | 降 self+prod |
| Vk7xMM15 | 2.18 | 2.47 | NULL | 0.036 | 0.8595 | 0.8595 | 降 self+prod |
| j2jYVVzW | 2.12 | 2.38 | NULL | 0.034 | 0.8621 | 0.8621 | 降 self+prod |
| P07oWb9K | 2.19 | 2.30 | 3.24 | 0.031 | 0.9206 | 0 | prod 墙 |
| GrlWAwzO | 2.10 | 2.16 | 3.09 | 0.030 | 0.9348 | 0 | prod 墙 |

**MEA 区特征**：TO 极低（0.03-0.05），F 高（2.1-2.7），但 self/prod 双高。6 颗 self>0.7 的候选需要正交化或子集组合。

### 4.4 EUR 区低 fitness 候选

| alpha_id | S | F | 2Y | TO | 优化方向 |
|---|---|---|---|---|---|
| 0mR093K1 | 1.70 | 0.94 | NULL | 0.095 | 提 fitness |
| 78ZE0bxx | 1.65 | 0.95 | NULL | 0.097 | 提 fitness |

---

## 五、高 Sharpe backtest 候选（30 颗，需降换手）

这些候选来自 GEM/brain-make-some-gem pipeline，Sharpe 极高但换手率也极高：

| alpha_id | S | F | TO | 表达式摘要 |
|---|---|---|---|---|
| O0NwW6oR | 6.48 | 3.71 | 0.797 | rank(-ts_zscore(corr_last_trade_price_with_volume, 66)) |
| d5b8a90w | 6.45 | 3.65 | 0.798 | group_rank(-ts_zscore(corr_last_trade_price_with_volume, 66), bucket(rank(cap))) |
| 58z7JGv6 | 5.78 | 3.06 | 0.812 | rank(-ts_rank(corr_last_trade_price_with_volume, 22)) |
| A1NJVm3e | 5.19 | 3.55 | 0.472 | rank(-ts_mean(corr_last_trade_price_with_volume, 3)) |
| WjbwO0Gk | 4.88 | 3.22 | 0.464 | rank(-ts_decay_linear(corr_last_trade_price_with_volume, 5)) |

**特征**：全部基于 `corr_last_trade_price_with_volume` 或其变体（corr_vwap/corr_twap/corr_bid），TO 0.35-0.81。这是**同一信号族的过拟合变体簇**，需：
1. 降换手（增大 decay / 加 truncation / 换 longer window）
2. 或只保留 1-2 颗做正交化组合

---

## 六、优化建议优先级

### P0（立即行动）

1. **A1Nn2vPQ 重试提交**：GLB S=3.73/F=3.22，prod 仅超线 0.0079，名称/描述已写好。prod 一回落即直接 POST。
2. **mLjnnzKE 相关性校验**：IND S=2.90/F=2.40，prod=0.5951 已 <0.7，self=0.53 需平台终验。若通过则升级 READY。
3. **np8VGNz3 / VkGJ73eA 相关性校验**：2 颗 READY IS_ONLY 跑 `--phase2-prod`。

### P1（本周内）

4. **IND 区降相关策略**：20 颗 prod>0.7 的高 Sharpe 候选，需：
   - 与已提交 alpha 做互斥结构（不同字段/不同中性化/不同 universe）
   - 或做子集组合降 prod
5. **MEA 区降 self 策略**：6 颗 self>0.7 候选，需正交化或 trade_when 门控
6. **backtest 高 TO 候选降换手**：5 颗 corr_last_trade_price_with_volume 族，TO 0.35-0.81，需 decay/window 调优

### P2（中期优化）

7. **EUR 区提 fitness**：2 颗 F<1.0 候选，需调整 decay/中性化
8. **20 颗低 2Y 候选稳健性提升**：2Y<1.58 或 NULL，需延长测试期或调整参数

---

## 七、关键洞察

1. **IND 是最大的未开发金矿**：24 颗高 Sharpe 候选全部卡在 prod 墙。IND 已有 20 颗 ACTIVE REGULAR，但仍有大量高指标候选因 prod 未消化。
2. **GLB 有立即可重试的候选**：A1Nn2vPQ prod 仅超线 0.0079，是"临门一脚"。
3. **MEA 区 self 墙突出**：6 颗候选 self>0.7，但 TO 极低（0.03-0.05），说明信号本身低换手但高自相关——需结构创新。
4. **backtest 超高 Sharpe 候选是同一信号族**：corr_last_trade_price_with_volume 的变体簇，TO 0.35-0.81，存在过拟合风险，不宜直接提交。
5. **READY 池几乎枯竭**：仅 2 颗 IS_ONLY 待校验，说明 auto-review 已持续消化队列。需补充新的挖掘波次。
