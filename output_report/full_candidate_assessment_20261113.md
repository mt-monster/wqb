# 全量候选全面评估 · 值得提交排序清单 v3（board `meanProdCorrelation` 口径） · 2026-11-14 12:29 GMT+8

> **只读评估，未提交任何 alpha。** 覆盖 47 颗活跃候选，整合方案 D、prod/self 终验、平台 checks、稳健台账、当季塔计数、同席互相关、混腿三问与配额。

## 0 结论

**47 颗 → 已提交 1 颗（P0）/ 可提交 4 颗（P1，全部 ops≤8）/ 待终验 10 颗（P2）/ 算子超标 11 颗（P6）/ 其它排除 21 颗。配额 ET 2026-11-13 REGULAR 2/4，剩 2 席。**

| 档 | 数量 | 定义 |
|---|---|---|
| **P0 已提交** | **1** | `wpo8olA6` 于 2026-11-13T22:59:27-05:00 提交 ACTIVE；`DEU/D1/OTHER` 2→3 点亮，不再进清单 |
| **P1 可提交** | **4** | 旧硬闸无 + 方案D 放行 + prod `refresh=True` <0.7 + self <0.7 + checks 0 FAIL + **ops≤8**；分 A 零待办 / B 待人工动作 |
| **P2 待终验** | **10** | ops≤8 且其余闸全过，但 prod 因平台熔断/账号槽占用未取得真重测值 ⇒ fail-closed，**当前不可提交** |
| **P6 算子超标** | **11** | 其余闸通过但 `operatorCount > 8` ⇒ 不合格（21:09 用户硬闸） |
| P3 终验否决 | 2 | 刷新后 prod/self ≥0.7 |
| P4 旧硬闸 | 11 | prod/self 超线、prod 未闭环、稳健台账 REJECT、ΔS<0 等 |
| P5 方案D 阻断 | 8 | 净效果 ΔS/ΔF<0 或「收益降+成本升」配对命中 |

**算子闸影响**：原 P1 候选里 `leAmmre8`(9)、`Xg9dPpp0`(9)、`Jje6mrpO`(10) 被移出；P1 现存 4 颗全部 ≤8 ops。

**★ 相对 prod 约束（软偏好，接口已更正）**：唯一基准 = `GET /consultant/boards/leader?stage=osmosis&user=<self_id>` 的 **`meanProdCorrelation` = 0.6396**（REGULAR 账户均值，submissionsCount 232）。候选 `refresh=True` 实测 prod **< 0.6396** ⇒ +5 分，不设硬闸。SUPER 同口径 `superAlphaMeanProdCorrelation` = 0.6308（54 颗；本池候选均为 REGULAR，仅列参考）。

**账户基线快照**（单行，取自 `/consultant/boards/leader?stage=osmosis&user=<self_id>`，2026-11-14T01:32:01）：

| 字段 | 值 | 用途 |
|---|---|---|
| `meanProdCorrelation` | **0.6396** | **本次相对约束主基准（REGULAR）** |
| `meanSelfCorrelation` | 0.4077 | 账户 self 均值，校准参考 |
| `superAlphaMeanProdCorrelation` | 0.6308 | SUPER 同口径参考 |
| `superAlphaMeanSelfCorrelation` | 0.5976 | SUPER self 校准参考 |
| `submissionsCount` / `superAlphaSubmissionsCount` | 232 / 54 | 均值分母 |
| `dailyOsmosisRank` | 0.300 | 当日 PnL 横截面排名（base quality 乘数） |
| `weightFactor` / `valueFactor` | 0.000 / 0.430 | 季度奖 / base 核心乘数 |
| `dataFieldsUsed` | 417 | 多样性 |

⛔ **接口更正**：上一版误用 `/users/self/alphas` 逐颗 `is.prodCorrelation`（最新提交件 .6788）当基准，已作废。旧产物 `results/submitted_regular_prod_benchmark_20261114.json` 已标 `deprecated`。账户级均值无分辨率，`tools/gates/prod_gate_audit.py` 早已定案**不进提交闸**；此处仅作评估软偏好/校准。

**值得提交前 3 席**：`omEdka3v` → `6XdkW08J` → `pwdd7Za6`。仍需你点名；agent 不自行提交。

## 1 评估口径（十维判据，硬闸优先）

| 序 | 维度 | 判据 | 来源 |
|---|---|---|---|
| 1 | 台账 / 旧硬闸 | REJECT、prod≥0.7 或超线、self≥0.7、prod 未闭环 ⇒ 先排除（REJECT 优先于一切指标） | 12:20 全篮子 + 本轮重读 |
| 2 | 方案 D | 净效果 ΔS≥0 且 ΔF≥0；仅「ΔRet<0 且成本升」追加阻断 | `performance_comparison` 20:1x 实测 |
| 3 | prod | **必须 `refresh=True` 真重测值 <0.7**；缓存/预读只许证伪不许放行 | 本轮 8 颗实测 |
| 4 | self | 本地 OS PnL 池重测 <0.7 | 本轮 28 颗 |
| 5 | 平台 checks | `is.checks` FAIL=0、`CONCENTRATED_WEIGHT`=PASS、status=UNSUBMITTED | 本轮 31 颗重读 |
| 6 | 稳健台账 | PASS > 无记录/ CONDITIONAL（后两者需审计声明） | `ledger_kv` |
| 7 | 混腿三问 | 2–3 腿需答三问（holders/polarity/prior 各 ≥8 字符）；`mix=none` 免 | `submit_queue.mix_review` |
| 8 | 塔 / 同席 / 配额 | 当季 ≥3 才点亮、同席 ρ≥0.7 让位、REGULAR 剩 3 席 | `get_pyramid_alphas` / 4y PnL / `quota_status` |
| 9 | **算子数（硬闸）** | **`regular.operatorCount ≤ 8` 才合格**；>8 一律移出可提交清单，同等绩效下越少越好 | `GET /alphas/{id}` 平台实值 |
| 10 | **相对 prod（软偏好）** | 候选 `refresh=True` 实测 prod **< `meanProdCorrelation` 0.6396** ⇒ +5 分；不满足不排除 | `/consultant/boards/leader?stage=osmosis&user=<self_id>` 单行 |

优先级分（仅 P1 排序，**满分 105**）= 终验闭环30 + prod余量20 + self余量15 + 稳健10 + 三问5 + 塔边际10 + 质量5 + **算子5**（≤3ops=5 / 4–5ops=4 / 6–8ops=2）+ **相对prod5**（低于基准才得）。**不按纯质量分排**：稳健已闭环、prod/self 余量、算子精简、低于已提交件 prod 优先。

## 2 ★ 值得提交排序清单（P1 4 颗）

| # | alpha | 级 | 优先级 | 区 | S/F | ops≤8 | prod 旧→新 | vs 基准 0.6396 | self 旧→新 | 稳健 | 三问 | ΔS/ΔF/ΔRet | 塔归属→现值→交后→新点亮 | 塔增量 | 待办 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **`omEdka3v`** | B | **70.2** | GBR | 2.51/1.40 | 8 ✓ | 0.6026→**0.6026** | ✓ 0.6026 | 0.492→**0.416** | PASS | 需答 | +0.59/+0.25/+0.0028 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | 1 | 三问 |
| 2 | **`6XdkW08J`** | B | **59.2** | GBR | 2.60/1.95 | 8 ✓ | 0.6267→**0.6267** | ✓ 0.6267 | 0.340→**0.339** | PASS | 需答 | +0.42/+0.34/+0.0020 | SHORTINTEREST 4→5 否(已亮) / MODEL 6→7 否(已亮) | 0 | 三问 |
| 3 | **`pwdd7Za6`** | B | **53.8** | GBR | 1.69/1.04 | 8 ✓ | 0.6238→**0.6238** | ✓ 0.6238 | —→**0.416** | 无记录 | 免 | +0.30/+0.20/-0.0052 | SHORTINTEREST 4→5 否(已亮) / PV 4→5 否(已亮) | 0 | 稳健声明 |
| 4 | **`RREPm361`** | B | **51.2** | DEU | 2.02/1.25 | 5 ✓ | 0.6881→**0.6881** | ✗ 0.6881 ≥ 基准 | 0.688→**0.327** | PASS | 需答 | +0.73/+0.31/+0.0080 | ANALYST 6→7 否(已亮) | 0 | 三问；prod贴线 |

**解读**：原首推 `wpo8olA6` 已于 2026-11-13T22:59:27-05:00 提交 ACTIVE 并点亮 `DEU/D1/OTHER`，已出清单；现首推 `omEdka3v`（8 ops / 稳健 PASS / 点亮 GBR/OTHER），次选 `6XdkW08J`（8 ops / 五项全达标 / 稳健 PASS）。`leAmmre8` 虽质量分 72 更高，但 **9 ops 超闸**且稳健无记录、prod .6887 贴线、ΔTO +0.0382 ⇒ 移出。

## 3 P2 待终验（10 颗，按质量分；当前不可提交）

| alpha | 区/分 | ops≤8 | prod 旧值(未终验) | self 重测 | 稳健 | 三问 | 方案D | 塔归属→现值→交后→新点亮 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `pwdLp9z6` | GBR/82 | 8 ✓ | 0.6483 | 0.420 | 无记录 | 需答 | 放行 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | 同席让位后备 |
| `mLaLllmK` | EUR/60 | 5 ✓ | 0.6579 | 0.100 | 无记录 | 免 | 放行 | OTHER 3→4 否(已亮) | prod 待补测 |
| `omExeqLb` | GBR/59 | 8 ✓ | 0.6143 | 0.420 | 无记录 | 需答 | 放行 | SHORTINTEREST 4→5 否(已亮) / MODEL 6→7 否(已亮) | prod 待补测 |
| `WjOeNE6O` | EUR/56 | 5 ✓ | 0.6411 | 0.641 | 无记录 | 需答 | 放行 | IMBALANCE 3→4 否(已亮) / OTHER 3→4 否(已亮) | prod 待补测 |
| `rKRRjM51` | IND/53 | 7 ✓ | 0.6752 | 0.653 | PASS | 免 | 放行 | INSTITUTIONS 1→2 否 / PV 11→12 否(已亮) | prod 待补测 |
| `rKRx7v6m` | EUR/52 | 7 ✓ | 0.6756 | 0.338 | CONDITIONAL | 需答 | 放行 | SENTIMENT 3→4 否(已亮) / OTHER 3→4 否(已亮) | prod 待补测 |
| `1YNMAA8M` | DEU/48 | 8 ✓ | 0.6951 | 0.695 | PASS | 免 | 放行 | MODEL 3→4 否(已亮) / ANALYST 6→7 否(已亮) | prod 待补测 |
| `2r5MqmVJ` | EUR/45 | 8 ✓ | 0.6740 | 0.239 | 无记录 | 免 | 放行 | EARNINGS 1→2 否 | prod 待补测 |
| `Jj8qXO5m` | EUR/45 | 8 ✓ | 0.6663 | 0.245 | 无记录 | 免 | 放行 | EARNINGS 1→2 否 | prod 待补测 |
| `d5apEYRx` | EUR/41 | 8 ✓ | 0.6887 | 0.231 | 无记录 | 免 | 放行 | EARNINGS 1→2 否 | prod 待补测 |

⛔ 这 10 颗的 prod 值均为 11-11/11-12 旧缓存（`computed=False`），按铁律不得据此放行。熔断/账号槽恢复后跑 `py results/_final_verify_prod_after_cooldown_20261113.py` 续跑，再跑 `py results/_reliable_submit_list_20261113.py` 更新清单。

## 4 排除清单（32 颗，含算子超标 P6）

| 档 | alpha | 区/分 | ops | prod | self | 方案D | 排除原因 | 塔归属→现值→交后→新点亮 |
|:---:|---|---|---:|---|---|:---:|---|---|
| P6 | `xAvK73Qg` | DEU/71 | 11 ✗ | 0.6433 | 0.557 | 放行 | 算子数 11 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed）；同席 ρ≥0.7 让位（后备） | SHORTINTEREST 5→6 否(已亮) / OTHER 3→4 否(已亮) |
| P6 | `E56GgqLL` | EUR/43 | 24 ✗ | 0.5524 | 0.435 | 放行 | 算子数 24 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | FUNDAMENTAL 3→4 否(已亮) / OTHER 3→4 否(已亮) |
| P6 | `78L5GaeZ` | EUR/43 | 10 ✗ | 0.6662 | 0.461 | 放行 | 算子数 10 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | ANALYST 10→11 否(已亮) / OTHER 3→4 否(已亮) |
| P6 | `zq3Yrb3G` | EUR/61 | 15 ✗ | 0.6872 | 0.687 | 放行 | 算子数 15 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | RISK 3→4 否(已亮) / ANALYST 10→11 否(已亮) / SENTIMENT 3→4 否(已亮) |
| P6 | `rKRx0M2m` | GBR/48 | 11 ✗ | 0.6232 | 0.443 | 放行 | 算子数 11 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | SHORTINTEREST 4→5 否(已亮) / RISK 0→1 否 |
| P6 | `O0A6Qz7p` | GBR/64 | 10 ✗ | 0.6984 | 0.678 | 放行 | 算子数 10 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 |
| P6 | `leAmmre8` | GBR/72 | 9 ✗ | 0.6887 | 0.262 | 放行 | 算子数 9 > 8（≤8 才合格） | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 |
| P6 | `RREGX1kd` | GBR/54 | 9 ✗ | 0.5940 | 0.369 | 放行 | 算子数 9 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | SHORTINTEREST 4→5 否(已亮) / ANALYST 3→4 否(已亮) |
| P6 | `LLM0e20m` | GBR/53 | 11 ✗ | 0.5386 | 0.404 | 放行 | 算子数 11 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） | SHORTINTEREST 4→5 否(已亮) / NEWS 3→4 否(已亮) |
| P6 | `Xg9dPpp0` | GBR/60 | 9 ✗ | 0.4000 | 0.279 | 放行 | 算子数 9 > 8（≤8 才合格） | SHORTINTEREST 4→5 否(已亮) / RISK 0→1 否 / FUNDAMENTAL 3→4 否(已亮) |
| P6 | `Jje6mrpO` | GBR/53 | 10 ✗ | 0.5565 | 0.329 | 放行 | 算子数 10 > 8（≤8 才合格） | SHORTINTEREST 4→5 否(已亮) / RISK 0→1 否 / FUNDAMENTAL 3→4 否(已亮) |
| P3 | `88NmN37X` | DEU/62 | 9 ✗ | 0.9540 | 0.954 | 放行 | prod 终验 0.9540 ≥ 0.7 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 |
| P3 | `ZYa6x531` | EUR/49 | 8 | 0.9229 | 0.199 | 放行 | prod 终验 0.9229 ≥ 0.7 | EARNINGS 1→2 否 |
| P4 | `d5a2aO7v` | DEU/39 | 8 | — | — | 数据缺失 | prod 未闭环 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 |
| P4 | `ZYQv7j2Q` | GBR/74 | 8 | 0.8159 | 0.816 | 放行 | prod 0.8159 超线；self 0.816 超线 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 |
| P4 | `LLMv6joe` | DEU/28 | 15 ✗ | — | — | 放行 | prod 未闭环 | SHORTINTEREST 5→6 否(已亮) |
| P4 | `zqdvb0YE` | DEU/36 | 9 ✗ | — | — | 放行 | prod 未闭环 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 |
| P4 | `mL617YPx` | EUR/68 | 14 ✗ | 0.5421 | 0.450 | 阻断 | submit_gate BLOCKED: ['robustness 台账判定 REJECT（brain-alpha-robustness 否决）：Recent-3；稳健台账 REJECT | FUNDAMENTAL 3→4 否(已亮) / PV 2→3 点亮 |
| P4 | `xArjE96W` | EUR/-29 | 14 ✗ | 0.5907 | — | 阻断 | ΔS=-0.03 硬闸 | RISK 3→4 否(已亮) / ANALYST 10→11 否(已亮) / SENTIMENT 3→4 否(已亮) |
| P4 | `N1P02YwL` | EUR/-33 | 9 ✗ | 0.6073 | — | 阻断 | ΔS=-0.05 硬闸 | RISK 3→4 否(已亮) / MODEL 3→4 否(已亮) |
| P4 | `qME6VWbj` | EUR/-49 | 5 | 0.6609 | — | 阻断 | ΔS=-0.03 硬闸 | ANALYST 10→11 否(已亮) |
| P4 | `VkxWmpYG` | EUR/-65 | 11 ✗ | 0.6800 | — | 阻断 | ΔS=-0.04 硬闸 | ANALYST 10→11 否(已亮) / NEWS 3→4 否(已亮) / OTHER 3→4 否(已亮) |
| P4 | `WjOAJWxd` | EUR/-67 | 10 ✗ | 0.6806 | 0.645 | 阻断 | ΔS=-0.01 硬闸 | ANALYST 10→11 否(已亮) / SENTIMENT 3→4 否(已亮) |
| P4 | `N1NGbddg` | EUR/-78 | 12 ✗ | 0.6872 | 0.660 | 阻断 | ΔS=-0.12 硬闸 | INSTITUTIONS 0→1 否 / ANALYST 10→11 否(已亮) |
| P5 | `qM7KxkQV` | DEU/61 | 11 ✗ | 0.5430 | — | 阻断 | 方案D 阻断：returns | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 |
| P5 | `d5a2vxzY` | DEU/36 | 12 ✗ | 0.6039 | — | 阻断 | 方案D 阻断：returns | SHORTINTEREST 5→6 否(已亮) |
| P5 | `9qlz29Oe` | DEU/50 | 12 ✗ | 0.4700 | — | 阻断 | 方案D 阻断：returns | SHORTINTEREST 5→6 否(已亮) / NEWS 0→1 否 |
| P5 | `ZYQ116ln` | KOR/75 | 3 | 0.6981 | 0.212 | 阻断 | 方案D 阻断：returns | PV 2→3 点亮 |
| P5 | `Jj8VQwoe` | DEU/64 | 12 ✗ | 0.6124 | — | 阻断 | 方案D 阻断：returns | SHORTINTEREST 5→6 否(已亮) / OTHER 3→4 否(已亮) |
| P5 | `6XMmE0EL` | EUR/58 | 5 | 0.6529 | 0.249 | 阻断 | 方案D 阻断：fitness | OTHER 3→4 否(已亮) |
| P5 | `JjeNJ00O` | EUR/62 | 10 ✗ | 0.6813 | — | 阻断 | 方案D 阻断：returns | RISK 3→4 否(已亮) / IMBALANCE 3→4 否(已亮) |
| P5 | `YP1baJrv` | EUR/62 | 9 ✗ | 0.6999 | — | 阻断 | 方案D 阻断：returns | RISK 3→4 否(已亮) / OTHER 3→4 否(已亮) |

## 5 全量 47 颗总表

| # | alpha | 档 | 区 | S/F | ops≤8 | D | prod(✓<0.6396) | self | 稳健 | 三问 | 塔归属→现值→交后→新点亮 | 结论 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `qM7KxkQV` | P5 | DEU | 1.72/1.34 | 11 ✗ | 阻断 | 0.5430(旧) | — | PASS | 需答 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 | 方案D 阻断：returns |
| 2 | `RREPm361` | P1 | DEU | 2.02/1.25 | 5 ✓ | 放行 | **0.6881**✗ | 0.327 | PASS | 需答 | ANALYST 6→7 否(已亮) | 三问；prod贴线 |
| 3 | `d5a2vxzY` | P5 | DEU | 1.60/1.08 | 12 ✗ | 阻断 | 0.6039(旧) | — | CONDITIONAL | 需答 | SHORTINTEREST 5→6 否(已亮) | 方案D 阻断：returns |
| 4 | `wpo8olA6` | P0 | DEU | 1.65/1.27 | 8 ✓ | 放行 | **0.6306**✓ | 0.578 | PASS | 免 | SHORTINTEREST 5→6 否(已亮) / OTHER 3→4 否(已亮) | 已于 2026-11-13T22:59:27-05:00 提交 ACTIVE（ET 11-13 22:59），已出清单；DEU/D1/OTHER 塔 2→3 点亮 |
| 5 | `omEdka3v` | P1 | GBR | 2.51/1.40 | 8 ✓ | 放行 | **0.6026**✓ | 0.416 | PASS | 需答 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | 三问 |
| 6 | `6XdkW08J` | P1 | GBR | 2.60/1.95 | 8 ✓ | 放行 | **0.6267**✓ | 0.339 | PASS | 需答 | SHORTINTEREST 4→5 否(已亮) / MODEL 6→7 否(已亮) | 三问 |
| 7 | `rKRRjM51` | P2 | IND | 3.34/2.65 | 7 ✓ | 放行 | 0.6752(旧) | 0.653 | PASS | 免 | INSTITUTIONS 1→2 否 / PV 11→12 否(已亮) | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 8 | `88NmN37X` | P3 | DEU | 1.79/1.53 | 9 ✗ | 放行 | **0.9540**✗ | 0.954 | PASS | 免 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 | prod 终验 0.9540 ≥ 0.7 |
| 9 | `d5a2aO7v` | P4 | DEU | 1.66/1.36 | 8 ✓ | 数据缺失 | —(旧) | — | — | 免 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 | prod 未闭环 |
| 10 | `9qlz29Oe` | P5 | DEU | 1.86/1.34 | 12 ✗ | 阻断 | 0.4700(旧) | — | CONDITIONAL | 需答 | SHORTINTEREST 5→6 否(已亮) / NEWS 0→1 否 | 方案D 阻断：returns |
| 11 | `2r5MqmVJ` | P2 | EUR | 1.74/1.03 | 8 ✓ | 放行 | 0.6740(旧) | 0.239 | — | 免 | EARNINGS 1→2 否 | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 12 | `ZYa6x531` | P3 | EUR | 1.74/1.01 | 8 ✓ | 放行 | **0.9229**✗ | 0.199 | PASS | 免 | EARNINGS 1→2 否 | prod 终验 0.9229 ≥ 0.7 |
| 13 | `Jj8qXO5m` | P2 | EUR | 1.74/1.03 | 8 ✓ | 放行 | 0.6663(旧) | 0.245 | — | 免 | EARNINGS 1→2 否 | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 14 | `d5apEYRx` | P2 | EUR | 1.77/1.05 | 8 ✓ | 放行 | 0.6887(旧) | 0.231 | — | 免 | EARNINGS 1→2 否 | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 15 | `ZYQv7j2Q` | P4 | GBR | 2.64/1.57 | 8 ✓ | 放行 | 0.8159(旧) | 0.816(旧) | PASS | 需答 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | prod 0.8159 超线；self 0.816 超线 |
| 16 | `ZYQ116ln` | P5 | KOR | 1.86/1.10 | 3 ✓ | 阻断 | 0.6981(旧) | 0.212(旧) | CONDITIONAL | 免 | PV 2→3 点亮 | 方案D 阻断：returns |
| 17 | `xAvK73Qg` | P6 | DEU | 2.04/1.77 | 11 ✗ | 放行 | 0.6433(旧) | 0.557 | CONDITIONAL | 需答 | SHORTINTEREST 5→6 否(已亮) / OTHER 3→4 否(已亮) | 算子数 11 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed）；同席 ρ≥0.7 让位（后备） |
| 18 | `Jj8VQwoe` | P5 | DEU | 1.65/1.24 | 12 ✗ | 阻断 | 0.6124(旧) | — | CONDITIONAL | 需答 | SHORTINTEREST 5→6 否(已亮) / OTHER 3→4 否(已亮) | 方案D 阻断：returns |
| 19 | `1YNMAA8M` | P2 | DEU | 1.58/1.36 | 8 ✓ | 放行 | 0.6951(旧) | 0.695 | PASS | 免 | MODEL 3→4 否(已亮) / ANALYST 6→7 否(已亮) | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 20 | `LLMv6joe` | P4 | DEU | 1.65/1.17 | 15 ✗ | 放行 | —(旧) | — | — | 免 | SHORTINTEREST 5→6 否(已亮) | prod 未闭环 |
| 21 | `zqdvb0YE` | P4 | DEU | 1.72/1.34 | 9 ✗ | 放行 | —(旧) | — | — | 免 | SHORTINTEREST 5→6 否(已亮) / INSIDERS 1→2 否 | prod 未闭环 |
| 22 | `mL617YPx` | P4 | EUR | 1.82/1.25 | 14 ✗ | 阻断 | 0.5421(旧) | 0.450(旧) | REJECT | 免 | FUNDAMENTAL 3→4 否(已亮) / PV 2→3 点亮 | submit_gate BLOCKED: ['robustness 台账判定 REJECT（brain-alpha-robustness 否决）：Recent-3；稳健台账 REJECT |
| 23 | `E56GgqLL` | P6 | EUR | 1.68/1.17 | 24 ✗ | 放行 | 0.5524(旧) | 0.435 | — | 免 | FUNDAMENTAL 3→4 否(已亮) / OTHER 3→4 否(已亮) | 算子数 24 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 24 | `xArjE96W` | P4 | EUR | 2.28/1.45 | 14 ✗ | 阻断 | 0.5907(旧) | — | — | 免 | RISK 3→4 否(已亮) / ANALYST 10→11 否(已亮) / SENTIMENT 3→4 否(已亮) | ΔS=-0.03 硬闸 |
| 25 | `N1P02YwL` | P4 | EUR | 1.81/1.43 | 9 ✗ | 阻断 | 0.6073(旧) | — | — | 免 | RISK 3→4 否(已亮) / MODEL 3→4 否(已亮) | ΔS=-0.05 硬闸 |
| 26 | `WjOeNE6O` | P2 | EUR | 2.90/1.85 | 5 ✓ | 放行 | 0.6411(旧) | 0.641 | — | 需答 | IMBALANCE 3→4 否(已亮) / OTHER 3→4 否(已亮) | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 27 | `6XMmE0EL` | P5 | EUR | 2.35/1.02 | 5 ✓ | 阻断 | 0.6529(旧) | 0.249(旧) | — | 免 | OTHER 3→4 否(已亮) | 方案D 阻断：fitness |
| 28 | `mLaLllmK` | P2 | EUR | 3.98/2.21 | 5 ✓ | 放行 | 0.6579(旧) | 0.100 | — | 免 | OTHER 3→4 否(已亮) | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 29 | `qME6VWbj` | P4 | EUR | 1.76/1.07 | 5 ✓ | 阻断 | 0.6609(旧) | — | PASS | 免 | ANALYST 10→11 否(已亮) | ΔS=-0.03 硬闸 |
| 30 | `78L5GaeZ` | P6 | EUR | 3.02/2.35 | 10 ✗ | 放行 | 0.6662(旧) | 0.461 | — | 需答 | ANALYST 10→11 否(已亮) / OTHER 3→4 否(已亮) | 算子数 10 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 31 | `rKRx7v6m` | P2 | EUR | 3.22/2.14 | 7 ✓ | 放行 | 0.6756(旧) | 0.338 | CONDITIONAL | 需答 | SENTIMENT 3→4 否(已亮) / OTHER 3→4 否(已亮) | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 32 | `VkxWmpYG` | P4 | EUR | 2.15/1.49 | 11 ✗ | 阻断 | 0.6800(旧) | — | — | 需答 | ANALYST 10→11 否(已亮) / NEWS 3→4 否(已亮) / OTHER 3→4 否(已亮) | ΔS=-0.04 硬闸 |
| 33 | `WjOAJWxd` | P4 | EUR | 2.36/1.61 | 10 ✗ | 阻断 | 0.6806(旧) | 0.645(旧) | — | 免 | ANALYST 10→11 否(已亮) / SENTIMENT 3→4 否(已亮) | ΔS=-0.01 硬闸 |
| 34 | `JjeNJ00O` | P5 | EUR | 2.60/1.35 | 10 ✗ | 阻断 | 0.6813(旧) | — | — | 需答 | RISK 3→4 否(已亮) / IMBALANCE 3→4 否(已亮) | 方案D 阻断：returns |
| 35 | `N1NGbddg` | P4 | EUR | 1.69/1.05 | 12 ✗ | 阻断 | 0.6872(旧) | 0.660(旧) | — | 需答 | INSTITUTIONS 0→1 否 / ANALYST 10→11 否(已亮) | ΔS=-0.12 硬闸 |
| 36 | `zq3Yrb3G` | P6 | EUR | 2.87/1.65 | 15 ✗ | 放行 | 0.6872(旧) | 0.687 | — | 需答 | RISK 3→4 否(已亮) / ANALYST 10→11 否(已亮) / SENTIMENT 3→4 否(已亮) | 算子数 15 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 37 | `YP1baJrv` | P5 | EUR | 2.23/1.19 | 9 ✗ | 阻断 | 0.6999(旧) | — | — | 需答 | RISK 3→4 否(已亮) / OTHER 3→4 否(已亮) | 方案D 阻断：returns |
| 38 | `rKRx0M2m` | P6 | GBR | 2.29/1.56 | 11 ✗ | 放行 | 0.6232(旧) | 0.443 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / RISK 0→1 否 | 算子数 11 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 39 | `pwdd7Za6` | P1 | GBR | 1.69/1.04 | 8 ✓ | 放行 | **0.6238**✓ | 0.416 | — | 免 | SHORTINTEREST 4→5 否(已亮) / PV 4→5 否(已亮) | 稳健声明 |
| 40 | `pwdLp9z6` | P2 | GBR | 2.26/1.19 | 8 ✓ | 放行 | 0.6483(旧) | 0.420 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed）；同席 ρ≥0.7 让位（后备） |
| 41 | `O0A6Qz7p` | P6 | GBR | 2.18/1.52 | 10 ✗ | 放行 | 0.6984(旧) | 0.678 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | 算子数 10 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 42 | `leAmmre8` | P6 | GBR | 2.97/1.40 | 9 ✗ | 放行 | **0.6887**✗ | 0.262 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / OTHER 2→3 点亮 | 算子数 9 > 8（≤8 才合格） |
| 43 | `omExeqLb` | P2 | GBR | 2.43/1.78 | 8 ✓ | 放行 | 0.6143(旧) | 0.420 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / MODEL 6→7 否(已亮) | prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 44 | `RREGX1kd` | P6 | GBR | 1.65/1.09 | 9 ✗ | 放行 | 0.5940(旧) | 0.369 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / ANALYST 3→4 否(已亮) | 算子数 9 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 45 | `LLM0e20m` | P6 | GBR | 1.75/1.17 | 11 ✗ | 放行 | 0.5386(旧) | 0.404 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / NEWS 3→4 否(已亮) | 算子数 11 > 8（≤8 才合格）；prod 未取得 refresh=True 实测值（账号级熔断/槽占用，fail-closed） |
| 46 | `Xg9dPpp0` | P6 | GBR | 1.97/1.44 | 9 ✗ | 放行 | **0.4000**✓ | 0.279 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / RISK 0→1 否 / FUNDAMENTAL 3→4 否(已亮) | 算子数 9 > 8（≤8 才合格） |
| 47 | `Jje6mrpO` | P6 | GBR | 2.37/1.58 | 10 ✗ | 放行 | **0.5565**✓ | 0.329 | — | 需答 | SHORTINTEREST 4→5 否(已亮) / RISK 0→1 否 / FUNDAMENTAL 3→4 否(已亮) | 算子数 10 > 8（≤8 才合格） |

## 6 ★ 本轮刷新推翻的旧结论

| 项 | 旧（12:20） | 本轮实测 | 影响 |
|---|---|---|---|
| `88NmN37X` prod | .5541 | **.9540** | ≥0.7 无豁免；self 亦 .9540 ⇒ 双闸排除 |
| `RREPm361` self | .6879 | **.3275** | 旧缓存高估 .36，解除分散度风险 |
| `wpo8olA6` self | 缺失 | **.5784** | 补齐缺口，A 级成立 |
| `EUR/D1/RISK` 塔计数 | 2 | **3** | 已点亮，本轮无塔边际增量；可新点亮塔 3→**2 座** |
| `DEU/D1/SHORTINTEREST` | 3 | **4** | 同塔已亮 |
| 当期 themes | — | 31/31 `MATCHES_THEMES` WARNING | 全池无当期主题资格（不影响 RA，影响 CPPAP） |
| 算子数 | 未设闸 | **≤8 才合格**（21:09 硬闸） | 47 颗里 26 颗 >8 ops（11 颗因此单独出局，其余已因其它闸排除）；P1 全部 ≤8 |
| 相对 prod 基准 | 误用逐颗 `is.prodCorrelation` .6788 | **board `meanProdCorrelation` 0.6396**（REGULAR，n=232；SUPER 同口径 0.6308） | 新增相对约束；旧口径作废 |

## 7 边界与纪律

- ΔS 只在**同一分区**内可比（8 个分区），不得跨区横比；`F=S×√(ret/max(TO,.125))` 四量共线。
- prod 保鲜 48h；贴线件（余量<0.02）提交前须再 `refresh=True` 一次。
- 塔倍率按数据集类别取**最低档**，点亮只认 `get_pyramid_alphas` 当季 ACTIVE ≥3；季度重置。
- 2–3 腿需答三问；`weight_grid`/`stack` 硬拦且 force 不豁免。
- **算子数 = 硬指标**：只认 `regular.operatorCount` 平台实值（不用正则数函数名），**≤8 才合格**；同等绩效下越少越好，压缩顺序 = 变量合并 → 多参展开 → 无损改写 → 有损消融。
- **相对 prod 为软偏好，不是硬闸**（用户措辞「最好小于」）：只把 `refresh=True` 实测值与board 的 `meanProdCorrelation` 比较；`refresh=False` 缓存/预读值一律不参与。要升成硬闸：在 `build()` 里把 `below_bench=False` 加入 `blockers`；SUPER 口径把 `BENCH` 换成 `BENCH_SUPER`（0.6308）。
- 基准口径（唯一正确）：`GET /consultant/boards/leader?stage=osmosis&user=<self_id>`，`results[0]` 单行；与 `tools/gates/prod_gate_audit.py` 同源。该端点的 `stage` 被平台忽略（osmosis/OS/IS 返回体相同），`meanProdCorrelation` 是 **N=232 已提交件的账户均值**，单颗候选最多推动 (1−0.6396)/233 ≈ 0.0015 ⇒ **无分辨率、不进提交闸**，仅作评估软偏好与口径校准。
- **只挖不提交**：本清单是「可提交」判定，POST 权归用户点名。
- 平台熔断（连续 pending 触发账号级保护）导致 23 颗 prod 未终验，均按 fail-closed 处理，不凭旧缓存放行。

## 8 产物

- `output_report/reliable_submit_list_20261113.md`（终验分级清单）、`output_report/full_basket_scheme_d_20261113.md`（方案 D 全篮子裁决）
- `results/full_candidate_assessment_20261113.json`（本报告机读版）
- 实测数据：`results/final_verify_{prod,self,meta}_20261113.json`；脚本 `results/_full_candidate_assessment_20261113.py`
