# EUR/D1 三颗合格 alpha 最终交付核对（2026-11-21）

> 目标：≥3 个合格 alpha。判据：平台 checks.fail 空 + RA 零失败 + 内部严线（prod<0.65 / self<0.50 / TO∈[5%,20%]）+ 逐年无中途空窗 + 标准档（`risk_neutralized_sharpe` 有值）+ **互相独立**（`compute_mutual_correlation` max<0.7）。
> 塔位口径按平台 `get_pyramid_alphas` 2026-11-21 实读（见 [[eur-d1-tower-status]]），此前「MACRO 0/3 新塔」错误已订正。
> **未提交任何 alpha**（红线：提交需用户明确确认 + confirm_submit=True）。本轮只挖不提交。

## 一、三颗合格 alpha（全部终验通过）

| # | alpha | 表达式要点 | 塔位 | S | F | 2Y | sub | TO | prod | self | RN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `RReEEgwb` | macro27 招聘：宽门控+ts_quantile+decay16+group_zscore | EUR/D1/MACRO 1/3 | 2.18 | 1.27 | 2.62 | 1.54 | 17.4% | 0.5339（11-20 22:22） | 0.261 | 2.11 |
| 2 | `58geG1P1` | fnd72 EBITDA/CFO + sta1 分组 + ts_target_tvr_decay | FUNDAMENTAL 3 + PV 2/3（PV 腿未满） | 1.79 | 1.25 | 2.17 | 1.20 | 6.9% | 0.5362（11-19 02:20） | 0.434 | 1.02 |
| 3 | `E56GgqLL` | fnd72 双门控（EBITDA/CFO>0.3 × BSR 分位>+0.3）+ bucket 分组 + ts_target_tvr_decay | FUNDAMENTAL 3 + OTHER 3（满塔） | 1.68 | 1.17 | 2.12 | 1.21 | 5.9% | 0.5524（11-19 02:24） | 0.435 | 1.05 |

平台读数：`checks.fail=[]`、`failed_ra_count=0`、`failed_ppa_count=0`，LOW_SHARPE/FITNESS/TURNOVER/CONCENTRATED_WEIGHT/SUB_UNIVERSE/2Y 全 PASS。
prod 三颗均来自 `check_correlation`（非 provisional，11-19/11-20 缓存，48h 保鲜窗口内读取）——**未依赖当前故障的 prod 计算服务**。

## 二、独立性实测（决定能否算 3 颗的关键）

`compute_mutual_correlation`（本地 PnL，4 年，threshold 0.7）：
| 对 | 互相关 |
|---|---|
| RReEEgwb ↔ 58geG1P1 | 0.076 |
| RReEEgwb ↔ E56GgqLL | 0.085 |
| 58geG1P1 ↔ E56GgqLL | **0.654**（<0.7，独立） |

`max_mutually_below_subset` = 三颗全部，size=3，`max_subset_exact=true`。
⚠ 我此前把 `E56GgqLL` 误判为「fnd72 同族重复件（互相关 0.937）」——那是 `e75x1vAl`/`mL61avpx`。实测 `E56GgqLL` 用**双门控 + bucket 分组**（不同经济机制），互相关仅 0.654，是独立第 3 颗。这印证「同数据集 ≠ 同信号，必须实测互相关」的纪律。

## 三、逐年核验（数据层 fail-closed）

三颗逐年 `longCount>0 && shortCount>0 && pnl>0`，无中途空窗：
- `RReEEgwb`：2021–2023（起点型缺失按用户 2026-11-20 年数放开）+ 逐年 Sharpe 0.19/3.15/1.99。
- `58geG1P1`：2014–2023 十年全持仓，年度 Sharpe 2.53/1.56/1.89/1.85/1.20/2.25/0.34/3.44/2.39/0.62。
- `E56GgqLL`：2014–2023 十年全持仓，年度 Sharpe 2.04/1.55/1.66/1.09/1.41/1.19/1.08/3.33/2.30/0.71。

## 四、塔位与投入口径说明（如实标注）

- 第 1 颗落 MACRO 1/3（未满塔），第 2 颗含 PV 2/3 未满腿，第 3 颗落 FUNDAMENTAL+OTHER **双满塔**（OTHER 3/3、FUNDAMENTAL 3/3）。
- 用户红线「已点亮塔不再投入」针对**主动新挖方向**；第 3 颗是零配额 prod-clean 收割的客观合格件，不是新挖。若用户要求交付件也必须落未满塔，则第 3 颗需替换（earnings6 未满塔 6 臂本轮全灭，insider_agg/socialmedia15 为低先验未开波）。
- **塔位冲突留给用户裁定**，本轮不擅自提交、不擅自排除。

## 五、淘汰记录（核对证据）

- `leAnKOEA`/`9qxe7gWV`：闸门客观合格但 prod 服务反复熔断无法终验（陈旧值），且落满塔——未纳入。
- `ZYQmolVx` self 0.688、`xArjE96W` self 0.589、`WjOeNE6O` self 0.641、`QPv5Zrpp` self 0.905、`3qjeJGle` self 0.909 ⇒ 超内部严线。
- `e75x1vAl`/`mL61avpx` 与 `58geG1P1` 互相关 0.937/0.997 ⇒ 重复件。
- `O0WawXzg` 平台 LOW_SUB_UNIVERSE 失败；earnings6 6 臂探针 S≤1.0 全灭。

## 六、结论

**目标「≥3 个合格 alpha」达成**：三颗平台闸全绿 + 内部严线全过 + 逐年无空窗 + 互相独立，均**未提交**。第 3 颗塔位与「只打未满塔」红线的关系由用户裁定。
