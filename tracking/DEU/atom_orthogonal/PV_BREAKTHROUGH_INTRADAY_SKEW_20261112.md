# ★★突破：PV 塔首个 IS 全闸通过件（S 1.75 / F 1.01 / 2Y 1.72）（2026-11-12）

> 起点：用户问「pv 下只测了 pv20 吗」→ 发现 PV 类实有 16 个数据集 → 转 intraday_pv_feats + pattern_scores
> 路径：2 臂探针（验 cov=0）→ 10 臂变化矩波 → 10 臂pattern波 → 10 臂定向优化 → 10 臂叠加波
> 关键发现：`skew_bid_ask_size_to_volume_ratio` 是**新机制面**

## 一、核心成果：H6 / H5 双双通过全部 IS 闸

```
# H6（首选，S 最高）
ts_target_tvr_decay(group_rank(ts_zscore(skew_bid_ask_size_to_volume_ratio,252),sector),target_tvr=0.45)
```

| 项 | **H6 `A1xZ7kNW`** | **H5 `LLKadk9v`** | 闸线 |
|---|---:|---:|---|
| Sharpe | **1.75** | 1.71 | ≥1.58 ✅ |
| Fitness | **1.01** | 1.03 | ≥1.00 ✅ |
| 2Y Sharpe | **1.72** | 1.71 | ≥1.58 ✅ |
| Turnover | 26.3% | 24.0% | ≤70% ✅ |
| sub_universe | 1.04 | 1.05 | ≥0.46 ✅ |
| margin | 0.0665% | **0.0720%** | — |
| lc/sc | **185/181** | 185/180 | ✅ |
| returns | 8.74% | 8.63% | — |
| **checks.fail** | **[]** | **[]** | — |
| **checks.pass** | **8 项（含 LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE）** | 同 | — |
| checks.warning | 仅 CONCENTRATED_WEIGHT / MATCHES_COMPETITION / MATCHES_THEMES（均为 undefined 占位） | 同 | — |
| 剩余 pending | SELF / DATA_DIVERSITY / **PROD** / REGULAR_SUBMISSION / POWER_POOL | 同 | — |
| 塔 | **DEU/D1/PV，倍率 1.6，eff=1（ATOM）** | 同 | — |

**⇒ 这是本战役第一个 `LOW_SHARPE + LOW_FITNESS + LOW_2Y_SHARPE` 三项全过的 PV 塔件。**
**⇒ 此前 PV 塔 0 颗（未点亮），这是第 1 颗候选。**

## 二、机制：这是 PV 塔从未有过的面

`skew_bid_ask_size_to_volume_ratio` = **「买卖盘挂单总量 ÷ 成交量」这个比值的偏度**。

| 取值 | 含义 |
|---|---|
| 偏度高（右偏） | 少数时段挂单量远超成交 ⇒ 存在**大额挂单压着但未成交** ⇒ 潜在压力未释放 |
| 偏度低 | 挂单/成交分布均匀 ⇒ 流动性供给平稳 |

⇒ 它测的是**日内订单簿的不平衡程度**，不是价格方向、不是流动性水平、不是动量。
⇒ 与既有 PV 机制（流动性水平 Amihud / 动量 / 形态相似度）**完全正交**。
⇒ 文献支撑：Humphery-Jenner (2012) VWAP 交易、Berkman-Erench-Koch (2012) 收盘压力、Lee-Ready 订单流不平衡。

### 为什么这个字段能过闸而 pv20 不行

| | pv20 流动性面 | pv20 IBES 面 | **intraday skew** |
|---|---|---|---|
| 最高 S | 1.37 | 0.47 | **1.75** |
| margin | 不足 | — | **0.0665%** |
| 原因 | 流动性水平被充分定价 | 同源衍生、无语义 | **订单簿偏度是未被定价的微观结构** |

## 三、优化路径（可复用的完整链条）

| 步骤 | 动作 | 结果 |
|---|---|---|
| 1 | 单字段水平矩（industry 轴，无平滑） | S 1.72 / F 0.59 / 2Y 1.45（fails=[]，但 F 与 2Y 是 warning） |
| 2 | **换分组轴 industry→sector** | S **1.81** / F 0.66 / 2Y 1.51（S +0.09、sub +0.14） |
| 3 | **加 `ts_target_tvr_decay` 降换手** | TO 65.7%→24-26%，**F 0.66→1.01-1.03、2Y 1.51→1.71-1.72** |
| 4 | 完成 | **三项全过** |

### ★两条关键方法（与既有经验一致，本次再次验证）

1. **降换手必须用 `ts_target_tvr_decay`（EUR 有效），不能用 `tvr_hump`**（EUR 无效）。
   本波 `tvr_decay τ=0.40/0.45` 直接把 F 从 0.66 抬到 1.03/1.01，同时 2Y 反而从 1.51 升到 1.71/1.72。
   ⇒ **降换手不必牺牲 S**（S 只从 1.81 掉到 1.75，−0.06），这与 institutions 塔「S–F 零和」的结论**相反**。
   ⇒ 差别在于：institutions 用的是 `ts_mean`（抹平信号），本波用的是 `tvr_decay`（只压调仓频率、保留信号形态）。
2. **分组轴 sector 优于 industry**（本字段），与 institutions 塔「industry 最优」相反 ⇒ **分组轴无全局最优，必须逐字段实测**。

### 反例：`ts_mean` 与 `ts_decay_linear` 都不如 `tvr_decay`

| 手段 | S | F | TO | 2Y | 结论 |
|---|---:|---:|---:|---:|---|
| `mean12` | 1.52 | 1.09 | 15.5% | 1.62 | F 最高但 **S 不过闸** |
| `mean16` | 1.40 | 1.07 | 12.8% | 1.64 | S 更差 |
| `decay44` | 1.12 | 0.79 | 9.0% | 1.29 | 全面差 |
| **`tvr_decay .45`** | **1.75** | **1.01** | 26.3% | **1.72** | ✅ **唯一三项全过** |

⇒ 同是降换手，`ts_mean` 把 TO 压到 15% 但 S 掉到 1.52；`tvr_decay` 只压到 26% 却保住了 S 1.75。
⇒ **降换手的正确目标不是「换手越低越好」，而是「换手刚好低于闸线、同时保住信号」**。

## 四、相关性状况

| 对 | 相关 |
|---|---:|
| H6 ~ H5 | **0.9984** |
| H6 ~ mean12 版 | 0.924 |
| H6 ~ G9（无平滑对照） | 0.8733 |
| H6 ~ D7（industry 版） | 0.8412 |

⇒ 本组 5 件高度同源，**最大独立集只有 1 席** ⇒ **只能出 1 个 alpha**。
⇒ 选 H6（S 1.75 最高）还是 H5（F 1.03 / margin 0.072% 更优）需权衡：
  - 提交看 S：H6 更优；
  - F 与 margin 看：H5 略优。

## 五、待办（提交前必须完成）

| 项 | 状态 |
|---|---|
| IS 全闸 | ✅ **已过（8 项 pass，fail=[]）** |
| 内部互相关 | ✅ 已测（同源，占 1 席） |
| **PROD 相关性** | ❌ **未查（pending）** |
| SELF 相关性 | ❌ 未查（pending） |
| 与既有 17 颗篮子的相关 | ❌ 未测 |
| 提交授权 | ❌ **需用户明确许可** |

## 六、附带：pattern_scores 首轮结论（未进候选）

最高 P8「对称三角下行 正号」S 0.63 / F 0.30；**V-bottom 相似度是反向信号**（P4 正号 −0.82）。
TO 仅 11.7-20.5%（低换手优势），方向已探明（wedge/tri_dn 取正、v_reversal 取负），二轮值得做组合。