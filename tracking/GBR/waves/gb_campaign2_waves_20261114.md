# GBR 未点亮塔第二轮战役波次档案（campaign2）

Region: GBR / TOP700 / D1（锁定）　开设：2026-11-14　前置：`reports/dataset_experience/gbr_unlit_campaign2_survey_20261114.md`
口径：只挖 D1 未点亮塔类别主腿（earnings6 / order_book_imbalance 双主线）；已亮塔可作从腿；挖到六维证伪为止。
设置档（本档与 profile 一致）：SUBINDUSTRY / decay 4 / truncation 0.08 / maxTrade OFF / pasteurization ON / unitHandling VERIFY / nanHandling ON。
并发纪律：在飞 multisim ≤2，上一批 terminal 再发下一批；每批 ≤8。

## 0. 第 0 步零成本复查结论（2026-11-14）

- **ern6 SUE 裁决**：`2rAo7mm8`（SUE×借券双腿件，FAST 档）平台实读 S1.74/F1.10/TO0.108/2Y2.78/sub1.81、checks.fail=[]、ra_failed=0、pyramids=SHORTINTEREST+EARNINGS(effective 2)。**十年逐年全正无空窗**（2014 lc430→2023，最弱 2020 S0.34/pnl+128k）⇒ **推翻 11-04 报告「earnings6 五年空窗数据集级否决」**——该否决只对 `P0gbMLz7`（divide 分母近零致持仓塌缩的特定表达式）成立。
- **双墙归因**：prod 0.8595（DB）+ self 0.7745。self 墙来源 = `3qoGxkqZ`（pv103 主腿 + **同一条 loaned_share_count_main 腿**，11-08 已提交 OS）⇒ **共享借券腿是 self 墙根因**；破法 = 纯 ATOM 化（earnings6 单集，self 池无同类持仓）。prod 墙 = FAST 档下机制拥挤，破法 = 中性化档扫（本区实证：估值+借券族 SLOW 0.63 vs SUBINDUSTRY 0.74，极差 0.11 是 prod 杠杆）。
- 论坛情报（SUE 主题检索，2026-11-14）：**事件驱动字段半衰期决定窗口**（帖子 41995684467479：SUE 别盲用 ts_rank(252)，否则拟合噪声）⇒ 本轮 SUE 窗口全部 ≤66d；SUE 2.0 帖（40296127975063）证「反应不足窗口数月级」但 GBR 实测 252d z 版（2rAo7mm8 腿）prod 0.86 拥挤 ⇒ 短窗变体是差异化方向。

## Wave 1 · ern6 纯 ATOM 破墙（批 1：SUE × 短窗结构变体）

- multisim: `2fGfk04zQ4jibAu1129on4kS`（2026-11-14 提交，@SUBINDUSTRY/decay4/trunc0.08）
- 设计：8 结构互异（sector 组内均值 / sector z / 线性衰减 / industry z / 时序自分位 / trade_when 事件门控 / winsorize+subindustry / 振幅归一比值），SUE = `vec_avg(ern6_actual_eps) − vec_avg(ern6_estimated_eps)`，backfill 66（对齐事件半衰期）。
- ATOM 合规：全部单集 earnings6，无任何豁免外字段；无 returns/close/volume/cap。
- **读数（8/8 全灭，归因清楚）**：

| alpha | 结构 | S | F | 2Y | TO | 判定 |
|---|---|---:|---:|---:|---:|---|
| 9qloNb9r | sector 组内 mean22 | 0.50 | 0.37 | -0.01 | 0.046 | 弱 |
| WjlkvnNo | sector z66（短窗） | **-0.36** | -0.17 | 0.06 | 0.313 | 反号 |
| N1PMYqnE | ts_decay_linear 21 | 0.66 | 0.71 | 0.19 | 0.073 | 弱 |
| j2aLqW1E | industry z66 | **0.68** | 0.77 | 0.31 | 0.076 | 弱（本批最高） |
| LLKe0qkn | ts_rank 126 | 0.46 | 0.40 | 0.52 | 0.098 | 弱 |
| xAvMJ9Rl | trade_when 事件门控 | 0.28 | 0.16 | -0.02 | 0.045 | 弱 |
| VkNnAqOb | winsorize+subindustry z66 | -0.33 | -0.15 | 0.16 | 0.310 | 反号 |
| e7aAXgrp | 振幅归一比值 | 0.29 | 0.21 | 0.06 | 0.064 | 弱 |

**归因**：① 论坛「SUE 短窗（半衰期）」建议在 ern6 上**证伪**——`ts_backfill(66)` 对稀疏事件 VECTOR 太短，抹掉信号；原始强件（2rAo7mm8）用的是 **252d z、无 backfill**。② 纯 ATOM SUE @SUBINDUSTRY 弱（最高 0.68 < 1.1），复证 11-09 T 波「纯 ATOM 全崩」结论 ⇒ SUE 强度依赖配置轴与组合腿。**行动**：批 2 回到 252d-z 原结构，测「换久期腿破 self 墙」+「原腿对照」。

## Wave 1 · 批 2（252d 原结构 × 久期新腿/loaned 对照腿，@SUBINDUSTRY/decay4/trunc0.08）

- multisim: `3GhJN8W057SbVbMQy4FUWp`
- 设计：臂1-5 = SUE×`average_loan_duration_days_main`（11-09 实证的合格第二短腿，OS 池 3qoGxqZ 未用 ⇒ 解 self 墙假设）；臂6 = 纯 SUE 252d 对照；臂7-8 = SUE×loaned_share_count_main 原 leg 对照（sector/industry 轴，验证批间可复现性 + industry 轴是否已避开 3qoGxqZ 的 sector 轴持仓）。
- ⚠ 组腿口径：earnings6（未点亮塔）× shortinterest3（已点亮塔，允许作从腿）；非 PV/MODEL/OTHER 互混，合规。
- **读数（SUE 纯腿崩、原 loaned 腿臂 1.04-1.07）**：

| alpha | 臂 | S | F | 2Y | TO | sub | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| blapejGr | 久期腿 sector | 0.31 | 0.08 | 0.75 | 0.160 | 0.18 | 久期腿太弱 |
| A1x6oljX | 久期腿 industry | 0.32 | 0.08 | 0.78 | 0.171 | 0.24 | 同 |
| 1YWvrweQ | 久期腿 backfill250 | 0.41 | 0.12 | 0.81 | 0.151 | 0.34 | 同 |
| gJavnj6K | 久期腿 winsorize | 0.31 | 0.08 | 0.75 | 0.160 | 0.18 | 同（与 blapejGr 逐位近同） |
| 0mPo1wq8 | 久期腿 ts_rank | 0.32 | 0.08 | 0.74 | 0.160 | 0.18 | 同 |
| leaxojd8 | **纯 SUE 252d 对照** | **-0.65** | -0.44 | -0.15 | 0.357 | -0.87 | 反号崩 |
| wpo60jqQ | loaned 腿 sector·等权 | **1.04** | 0.59 | 1.23 | 0.092 | 1.46 | 弱 |
| blapejXr | loaned 腿 industry·2:1 | **1.07** | 0.60 | 1.22 | 0.103 | 1.52 | 弱 |

**归因（三条硬结论）**：
1. **纯 SUE 252d 在 SUBINDUSTRY 下反号（-0.65）**，而 2rAo7mm8 同表达式在 **FAST 档 + decay5 + trunc0.1** 下 S1.74 —— **SUE 是配置层信号**（中性化档决定生死）。批 1（短窗）+ 批 2（长窗）纯腿全灭 ⇒ 「纯 ATOM SUE」假设证伪，ern6 必须走组合腿+FAST 档路线。
2. **久期腿不行**：五臂 0.31-0.41，比 loaned 腿（1.04+）弱 2 倍+，11-09 survey 说它「能过闸」不成立于本组合。**「换久期腿解 self 墙」假设证伪**。
3. loaned 腿在 SUBINDUSTRY/decay4 下只有 1.04-1.07（vs FAST 下 1.74）⇒ 复证第 1 条：**配置轴是第一杠杆**。industry 轴 (1.07) 略优于 sector (1.04)，sub 1.52 健康。

**行动（批 3）**：同表达式回 FAST 档（decay5/trunc0.1 复刻 2rAo7mm8 配置），只变轴与权重，验证「FAST 档下 industry 轴 + 新 SUE 变体」能否既保 S1.7+ 又破 self 0.77（3qoGxqZ 是 sector 轴 loaned 腿 + pv103 主腿；换 industry 轴 + earnings 主腿 → 持仓差异双源）。

## Wave 1 · 批 3（FAST 档复刻 × 轴变体，@FAST/decay5/trunc0.1）

- multisim: `2KLnZpcUU53oa1rQnPByQwD`
- **读数（6/8 全闸级：S 1.72-1.74、ra_failed=0）**：

| alpha | 变体 | S | F | 2Y | TO | sub | ra |
|---|---|---:|---:|---:|---:|---:|---:|
| rK7Q1331 | industry×industry 轴 | 1.72 | 1.05 | 2.70 | 0.117 | 1.84 | 0 |
| WjlKEqqk | subindustry×industry | 1.73 | 1.06 | 2.69 | 0.117 | 1.84 | 0 |
| MP69jWW8 | sector×industry | 1.72 | 1.05 | 2.71 | 0.117 | 1.84 | 0 |
| pwaQqXX6 | ts_rank 主腿 | **1.74** | 1.10 | 2.79 | 0.109 | 1.81 | 0 |
| bla7YkkR | 窗 504 | 1.74 | 1.10 | 2.79 | 0.108 | 1.81 | 0（与 252 逐位同） |
| zqdXvMMd | decay_linear 10 | 1.74 | 1.10 | 2.78 | 0.108 | 1.81 | 0 |
| RRe0J33o | group_zscore 双标 | **-1.18** | -0.57 | -1.25 | 0.144 | -0.26 | 4 |
| vRAaKqMw | loaned 腿 backfill66 | 0.59 | 0.18 | 1.26 | 0.161 | 0.90 | 3 |

- **归因**：① FAST 档假设验证——同表达式 SUBINDUSTRY -0.65 → FAST +1.74，**SUE 是配置层信号**；② 窗 252/504 与 decay_linear 平滑零差异（信息在长期水平不在路径）；③ group_zscore（非保序双标准化）毁信号；④ loaned 腿必须 504 窗（66 窗掉 1.1 S）。
- **self 实测（rK7Q1331）**：0.8211 FAIL——仍撞 3qoGxqZ，**换 industry 轴没破墙（比 sector 版 0.7745 更高）** ⇒ **借券腿主导 PnL，分组轴不改变持仓结构**。与 11-14 实测「loaned 腿单独 prod 0.93」合并结论：**loaned_share_count_main 腿本身 = self+prod 双拥挤源**。

## Wave 1 · 批 4（FAST 档纯 SUE ATOM + 权重梯度，@FAST/decay5/trunc0.1）

- multisim: `1ZaKkD46Y4oSchevri5JUhB`
- 假设：纯 SUE @ FAST（无借券腿）= ATOM 合规 + self 天然干净（OS 池无 earnings 主腿件）+ prod 远离借券拥挤区。臂1-4/7-8 = 纯腿六变体；臂5-6 = 权重梯度 5:1/3:1（降借券腿占比能否压 self）。
- **读数（纯腿全灭 + self 地板实证）**：

| alpha | 臂 | S | F | 2Y | TO | ra |
|---|---|---:|---:|---:|---:|---:|
| vR1Xk31w | 纯 SUE sector | **-0.89** | -0.36 | -0.39 | 0.467 | 4 |
| 6XMgnGbY | 纯 SUE industry | **-0.96** | -0.40 | -0.57 | 0.467 | 4 |
| pwaQqWgv | 纯 SUE 裸 rank | -0.44 | -0.11 | -0.60 | 0.352 | 5 |
| j2aN5VQo | 纯 SUE ts_rank | -0.84 | -0.33 | -0.27 | 0.468 | 4 |
| akaXrR3w | 5:1 权重 | **1.70** | 1.07 | 2.80 | 0.112 | **0** |
| A1xqRLdX | 3:1 权重 | **1.73** | 1.09 | 2.79 | 0.110 | **0** |
| LLKOP8eL | 纯 SUE 窗 504 | -0.85 | -0.34 | -0.42 | 0.467 | 4 |
| 9qlgzGo1 | 纯 SUE trade_when | -0.81 | -0.31 | -0.79 | 0.455 | 5 |

- **self 实测**：pwaQqXX6（批3 ts_rank 版）0.7742 FAIL；akaXrR3w（5:1）0.7709 FAIL。**权重 2.5 倍只降 self 0.004** ⇒ **self 地板 ~0.77 由 loaned 借券腿钉死**（全部撞 3qoGxqZ），参数空间不可达 0.7。

### Wave 1 收口 · earnings6 组合族 PROVISIONAL 判死（本篮配置内）

六维举证：D1 结构互异模板 ≥10（三批累计 24 臂：8 短窗 + 5 久期腿 + 8 FAST 轴变体 + 3 纯腿）✓；D2 字段族：actual/estimated EPS 对（核心）+ x_dividend（11-13 已测 0.45 弱）+ 其余为日期/元数据族（非信号，画像在档）✓；D3 矩全家：水平 ts_zscore ✓ / ts_rank ✓ / ts_decay_linear ✓ / 比值（振幅归一）✓ / trade_when 门控 ✓；D4 分组轴：sector/industry/subindustry 三轴 ✓；D5 非线性：winsorize ✓ / trade_when ✓ / 权重 multiply 梯度 ✓；D6 配置：SUBINDUSTRY/decay4/trunc0.08 + FAST/decay5/trunc0.1 两套 ✓。
**死因归因（机制层）**：earnings 塔活机制 = SUE×loaned 双腿 @FAST——但 loaned 腿 = self 0.77 地板（OS 3qoGxqZ 占位）+ prod 0.86 拥挤；纯 SUE 任何档位反号（SUE 单腿无溢价，组合溢价由借券腿主导）。**复活条件**（非本波范围）：出现一条非 loaned 的合格从腿（久期腿已证伪 0.31-0.41），或 OS 池 3qoGxqZ 退役。

## Wave 2 · order_book_imbalance trade 分类组开采（批 5：暗池/碎片化份额比）

- multisim: `7Zj9P7uU4Zy8AFpblizHhx`（@SUBINDUSTRY/decay4/trunc0.08）
- 数据集换防理由：earnings6 PROVISIONAL 判死（见上），P2 order_book_imbalance 是 11-11 明确「不判死、226/240 未测」的唯一大池。
- 机制模板（经济含义）：dark/lit/bilateral/nonaddressable 四分类份额比 = 流动性碎片化与价格发现质量代理（Cont-Kukanov-Stoikov 隐藏流动性成本；dark share ↑ → 信息环境差 → 溢价）。方向先测双向（臂1 正 / 臂2 反）。
- ATOM 合规：全部单集 order_book_imbalance。
- **读数（8/8 全灭，暗池/碎片化份额比机制弱）**：

| alpha | 臂 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| akaXkvq6 | dark share 正向 w22 | -0.31 | -0.12 | -0.68 | 0.077 |
| LLKOLJA6 | dark share 反向 w66 | 0.24 | 0.10 | 1.04 | 0.044 |
| rK7QKXvo | bilateral 占比 sector | 0.44 | 0.21 | 0.15 | 0.047 |
| KPgxPajN | dark share z252 | 0.17 | 0.04 | 0.34 | 0.394 |
| 0mPnmv0G | bilateral/nonaddressable | -0.13 | -0.06 | 0.02 | 0.076 |
| YPaXPqGJ | dark/lit notional industry | **0.50** | 0.25 | 0.50 | 0.045 |
| wpoXpgMd | nonaddressable 反向 sector | -0.54 | -0.28 | -0.94 | 0.030 |
| qM7eMqq1 | dark share ts_rank252 | -0.11 | -0.02 | 0.27 | 0.480 |

**归因**：份额比机制正反双向均弱（最强 0.50），且 nonaddressable 反向 -0.54 与 11-11 的 -0.56 一致（真噪声方向）。**信号不在"量"的份额结构里**。剩余两个未扫维度：① auction 组（closing_auction_dislocation / auction_order_imbalance，11-11 只测过 2 个字段裸水平 0.32）——竞价错位是**价格类**信号（bps 量纲，非量份额）；② spread/执行质量组（time_weighted_spread 反向 11-11 测过 0.32）。批 6 攻 auction 价格族 + spread 变体。

## Wave 2 · 批 6（auction 价格族 + spread 执行质量族）

- multisim: `4peBUvbJA4Iiagb19rGHPPh`（@SUBINDUSTRY/decay4/trunc0.08）
- **读数（8/8 全灭，最高 0.57）**：

| alpha | 臂 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| pwaQwK1X | dislocation_last 反向 mean22 | 0.22 | 0.07 | 0.72 | 0.141 |
| d5ae5Rlx | dislocation_1min 反向 sector | -0.43 | -0.20 | -0.42 | 0.113 |
| 9qlgq7A2 | auction_imbalance_pct_adv 正向 | -0.06 | -0.01 | 0.25 | 0.089 |
| P05j0OwW | dislocation_last z252 industry | **0.57** | 0.22 | 0.48 | 0.239 |
| XgaXg82l | tw_spread_bps 反向 w66 | -0.53 | -0.31 | -0.08 | 0.019 |
| 2r5PrNaN | mean_rel_spread sector 正向 | **0.57** | 0.32 | 0.31 | 0.020 |
| d5ae5REY | dislocation_5min z252 | 0.28 | 0.04 | 0.14 | **0.712 TO 爆** |
| rK7QKPJa | final_spread Δ66 反向 | -0.62 | -0.26 | -0.66 | 0.227 |

**归因**：竞价错位 z252（0.57）与 spread 水平（0.57）双双封顶——与份额比族（0.50）、11-11 已测字段（0.56）同一量级。**三族一致 0.5-0.57 天花板 = 该集结构性封顶签名**（与 analyst47「四几何收口 1.32-1.35」同型：读数信息量到位即封顶）。批 7 = 最后一个未测族（深度微观结构组 fill_prob/rest_time/duration/notional 改进），按 D2 纪律扫完。

## Wave 2 · 批 7（深度微观结构族：fill_prob / rest_time / duration / 价格改进，逆向选择机制）

- multisim: `3dmg389774yAcC29kftej7Y`（@SUBINDUSTRY/decay4/trunc0.08）
- 机制：fill_prob 高 + 存续短 = 知情交易压力（adverse selection）→ 反向；EBBO 驻留时长 = 竞争强度 → 行业内正向。
- **读数（7/7 全灭，最高 0.52；1 臂 unit 错被平台拦）**：

| alpha | 臂 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| YPaXPOeJ | fill_prob_ask 反向 | 0.06 | 0.01 | 0.71 | 0.064 |
| npawplEE | rest_time_ask_filled 正向 | **0.52** | 0.28 | 0.33 | 0.042 |
| 2r5Prx38 | fill_prob_bid_lvl3 反向 | -0.54 | -0.30 | -0.47 | 0.041 |
| A1xq15od | duration EBBO industry | 0.39 | 0.17 | 0.43 | 0.029 |
| d5ae56Ng | notional 改进比 | — | — | — | 平台拒：notional 是 Unit[CSPrice] 量纲，add(., 0.01) 单位不兼容 |
| QP0mPAwQ | quote_to_trade 反向 | 0.28 | 0.11 | 0.50 | 0.053 |
| xAvXAoJb | ebbo_filled_pct z252 | 0.45 | 0.19 | 0.53 | 0.168 |
| 3q0gqO8P | pct_cancelled 反向 | 0.45 | 0.22 | -0.13 | 0.052 |

### Wave 2 收口 · order_book_imbalance PROVISIONAL 判死（单集 ATOM 形态）

六维举证：D1 结构互异模板：三批 23 臂（8 份额比 + 8 auction/spread + 7 微观结构）+ 11-11 已测 14 字段 ⇒ ≥30 有效结构 ✓；D2 字段族：trade 分类四族全测 ✓ / auction 四字段 ✓ / spread 族 ✓ / fill_prob ✓ / rest_time ✓ / duration ✓ / ebbo 比率族 ✓（未逐一测的仅同族 lvl2-5 重复变体，无新机制）；D3 矩全家：水平 mean22/66 ✓ / zscore ✓ / ts_rank ✓ / Δ ✓ / 比值 ✓；D4 分组轴：裸 / sector / industry ✓；D5 非线性：reverse 方向对照 ✓ / 比值非线性 ✓；D6 配置：SUBINDUSTRY/decay4/trunc0.08 单档（11-11 已补 CROWDING/REV/industry/subindustry 四档对照，方向一致）✓。
**死因（信号层）**：**四大字段族全部封顶 0.44-0.57**（11-11 字段族 0.56 / 份额比 0.50 / auction 0.57 / spread 0.57 / 微观结构 0.52），正反双向对称 ⇒ 与 analyst47 同型的**结构性封顶签名**：GARCH 类量纲压缩后的 L1-L3 订单簿日频聚合在 TOP700 横截面上无超额信息。距 1.58 闸差 1.0+，任何结构/参数动作不可达。
**保留**：本判死为**单集 ATOM 形态**判死；作为组合腿与其它塔（如 news）的交互未在本轮范围（用户约束跨塔组合 ≤5 配额，优先级让位给更强的主腿候选）。

## Wave 2 补 · 双主线全灭后的候选复核与战役收口（2026-11-14 晚）

双主线（earnings6 / order_book_imbalance）六维证伪完毕。P3 macro27（F 墙 0.66 vs 要求 1.0，sub 0.17 覆盖弱）与 P4 备胎（event_ml 0.52 / stock_search TO 墙 / insiders12 顶 1.04 / option1 顶 1.40）均为**已实测收口的远闸资产**（11-13 X1/Z 波 + 11-11 普查），无新维度可扫 ⇒ 不再派波。**GBR D1 未点亮塔可挖空间在本轮约束下确认知竭**：前轮（11-08/11-13/14）已把 28 集 + other 塔重点集全部探针收口，本轮双主线深挖补齐了最后两个「未穷尽」标注（order_book 226 未测字段 × 4 字段族、ern6 复活路径），全部六维证伪。
