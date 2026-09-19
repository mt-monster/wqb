# wqb 候选库全量盘点与抢救战报（2026-09-15）

## 一、总览

| 阶段 | 结果 |
|---|---|
| 全库候选 | 3,940 条 |
| 判定死局并软删除 | **2,877 条**（可恢复） |
| 抢救池（平台 UNSUBMITTED、非 MEA） | **602 条** |
| 其中 IS 闸干净 | 236 条 |
| **双闸均过、可提交** | **0 条** |

## 二、死局判定与软删除（2,877 条）

软删除 = 本地 `alphas` 表打 `soft_deleted` 标记（新增 `soft_deleted / soft_deleted_at / soft_delete_reason` 三列），**可逆**，不动平台数据。

| 死因 | 条数 |
|---|---|
| IS 弱（sharpe<1.0 或空） | 2,553 |
| MEA 止损（沿用既有定规） | 313 |
| 平台 DECOMMISSIONED | 11 |

恢复方式：`UPDATE alphas SET soft_deleted=0 WHERE ...`

> 关键方法：**平台 `status` 是最廉价的死活判据** —— 一次轻量 GET 即可，无需等待 8–10 分钟的 PROD 计算。

## 三、抢救池 602 条的挡路闸分布

| 挡路闸 | 条数 |
|---|---|
| IS_LADDER_SHARPE | 272 |
| LOW_SHARPE | 90 |
| LOW_ROBUST_UNIVERSE_SHARPE | 61 |
| CONCENTRATED_WEIGHT | 35 |
| LOW_2Y_SHARPE | 10 |
| LOW_SUB_UNIVERSE_SHARPE | 8 |
| HIGH_TURNOVER | 3 |

**IS 闸无 FAIL = 236 条**；存在 FAIL = 366 条（可多命中）。

## 四、236 条清洁候选的双闸实测（按 fitness 前 30）

**双闸均过 = 0 条。**

- SELF 普遍 **0.53–0.99**，多数已超 0.7；
- PROD 有返回的全部落在 **0.81–0.86**（0.7354 / 0.8134 / 0.8199 / 0.8577 / 0.8617）；
- 多数 PROD 返回 None（平台侧未就绪），非本地问题。

代表样本：

| 候选 | 区域 | sharpe | fitness | SELF | PROD |
|---|---|---|---|---|---|
| qMja95Q2 | IND | 4.26 | 3.97 | 0.7353 | 0.7354 |
| ZY7VoZq1 | IND | 3.60 | 2.40 | 0.8628 | 0.8617 |
| xAj78Vnm | IND | 3.14 | 2.24 | 0.6464 | 0.8199 |
| Vk7QjZOG | IND | 2.95 | 2.07 | 0.6453 | 0.8134 |
| ZY0MOMGj | DEU | 1.90 | 1.95 | 0.7422 | 0.8577 |

## 五、IND 八候选「其它优化能否救」结论

IND 锁死：universe 仅 TOP500、delay 仅 1 → 只能动 neutralization / decay / truncation / 表达式平滑。

1. **WjPjXARx = 死局**：表达式为 `(SUPER)`，本身即 SuperAlpha → `COMPONENT_ALPHA_AUTHORIZATION` 结构性失败，不可修。
2. **5 个 LOW_ROBUST_UNIVERSE_SHARPE = 结构性不可救（终审确认）**：基线 `STATISTICAL` 已是**最优**，换 10 个中性化档位**全部劣化**（例 blj0mgPK：基线 0.91 → SLOW_AND_FAST 0.62 / FAST 0.58 / INDUSTRY 0.40 / SUBINDUSTRY 0.32 / SECTOR 0.31 / CROWDING 0.08 / MARKET·NONE ≈ 0）。
   - 根因：收益来自非流动性小票，robust universe 一剔除即崩 = STOP_STRUCTURAL。
3. **2 个 CONCENTRATED_WEIGHT（vRj7arVw 0.1599 / 1Yw36X56 0.1720，限 0.1）**：降 truncation（0.08→0.04/0.02/0.01）机制上最可能奏效，但受 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED` 阻塞，**结论待补**。

## 六、「变换 universe 降 PROD」实证（USA N1QMJ10q）

**路径成立，但非单调，必须逐档实测。**

| universe | sharpe | fitness | PROD | IS 状态 |
|---|---|---|---|---|
| TOP3000（基线） | 2.42 | 1.47 | 0.7225 | — |
| **TOP1000** | 1.53 | 0.78 | **0.6149** ✅ | 仅 WARNING，无 FAIL |
| TOP500 | 0.99 | 0.40 | 0.5422 | **FAIL**（IS 被摧毁） |
| TOP2000 | 1.92 | 1.05 | **1.0** ❌ | 无 FAIL 但 PROD 反升 |

→ 缩小 universe 可降约 0.11 的 PROD，但过小会摧毁 IS，过大反而升 PROD。**降 PROD 首选 TOP1000 档**。

## 七、总结论

**抢救池已基本枯竭。** 602 条里 236 条 IS 干净，但双闸无一能过；366 条被 IS 闸挡住，且以 `IS_LADDER_SHARPE`(272) + `LOW_SHARPE`(90) 为主 —— 属 IS 强度不足的**结构层**问题，参数微调救不回来。

唯一出路：**新挖不同质信号**（与现有 book / 生产池低相关的新骨架）。

## 八、工程要点

- 平台列表接口**各 status 过滤各限 1,000 条**（UNSUBMITTED 拉到 1,100 即 400），逾此只能逐条 GET。
- `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`：批量建仿真会互相挤兑；失败的 `error` 会写进 checkpoint，**重跑前必须先清掉 error 条目**，否则脚本判定"已完成"直接跳过。
- 平台 PROD 实测约 33–35s/个（此前 8–10 分钟是网络重试所致）。
- 提交前必须 PATCH ≥100 词英文描述（空描述静默丢弃）；**同步 403 = 零成本**，可安全连探。
