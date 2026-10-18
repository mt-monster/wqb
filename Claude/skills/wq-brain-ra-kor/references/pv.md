# KOR × pv（组合分支）

> 回到 [KOR 区域流程](../SKILL.md) · [KOR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/KOR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region KOR --category pv`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：PV　**类别卡**：pv

**涉及数据集**：continuation_score、intraday_pv_feats、pattern_scores、pv106、pv30

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | KOR | 区域 settings.json |
| universe | TOP600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 40 | 0 | 0 | 0 | 7 | 0 |

主要数据集（回测数）：pv106（32）、intraday_pv_feats（8）

### S1 字段理解

- 各区可用性差异大：先查本区有没有 pv1（JPN TOP1600 没有，close / adv20 / returns 不可用）
- intraday_pv_feats 目录字段 ≠ 平台可用字段：先单字段探针再成批
- 窗口（类别卡，均在白名单内）：daily 1/5/22；monthly 66

### S2 生成

- **避**：pv106 流动性天花板 1.1；pv30 聚类标签无信号；图表形态族三连死（RULES §G）
- **类别通用原语**（类别卡，跨区）：
  - continuation vs reversal: short-horizon pattern vs longer mean
  - intraday vs overnight: session-specific pressure
  - volume-conditioned return: price move that happened on unusual volume
  - fast+slow interaction must be ONE coherent signal (ratio / ts_corr / conditional), never a weighted sum of two legs
  - volatility regime: high-vol vs low-vol period signal divergence
  - liquidity shock: volume spike vs historical average (ts_zscore of volume)
  - price efficiency: bid-ask spread or price impact proxy
- **跨区结论**（IND/GLB/ASI；negative）：日内价量相关反转 / 尾盘反转 IS 很强，但裸用 prod 0.79–0.99；只有加门控才可能破墙（见全局杠杆 subset_gate）（证据：IND intraday_pv_feats prod 0.79–0.92、pv103 外部孪生 1.0（IND profile）；GLB / ASI 门控模板（2026-09-21 实证）） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（JPN/IND/GBR/USA；negative）：日内微观结构的非反转机制普遍弱（max ／S／ 约 1.0，或撞 fitness 墙）（证据：JPN w8 16 条 max／S／ 1.02；USA-IPV-CORR-PRECLOSE-FITNESS-WALL-20260921；GBR-INTRADAY-MICRO-WEAK；IND 未点亮塔实证） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/GBR/DEU/AMR；negative）：图表形态族（pattern_scores / continuation_score / chart_cnn）（证据：KOR 三连死（chart_cnn 1.51 → continuation 0.34 → pattern_scores 0.49）；GBR-SIMPLE-STRUCTURE-DEAD；DEU-PATTERN_SCORES-PROBE-DEAD-20261002；AMR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用加权混合（0.4*rank(A) + 0.6*rank(B) / add(multiply(0.4,A),multiply(0.6,B))）
- **禁止**（类别卡）：禁止使用 ts_entropy / ts_skewness（幽灵算子）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize）入场（原举例 regression_neut / vector_neut 均已被平台移除，2026-10-10 op-lint 实测）
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region KOR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| KOR-CONTINUATION-SCORE-DEAD | continuation_score chart-pattern similarity | white space does not imply signal; do not re-mine continuation_score on KOR | continuation_score | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-CONTINUATION-SCORE-PROBE-DEAD | continuation_score chart pattern | KOR 图表形态延续族 (chart_cnn_alpha/continuation_score) 均判死; 形态相似度信号 KOR 天花板~0.34, 不再优先挖 | continuation_score | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-PATTERN-SCORES-PROBE-DEAD | pattern_scores 图表形态 | KOR 图表形态延续族 (chart_cnn/continuation/pattern_scores) 全部判死, 不再挖形态类数据集 | pattern_scores | inferred | <!-- lint:const-ok 证据原文 -->
| KOR-PV106-LIQUIDITY-BELOW-LINE | pv_liquidity_spread | pv106 spread/liquidity premium signal caps at ~S1.1 in KOR; do NOT re-mine plain rank(multiply(cost_gap, spread)) varian | pv106 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-PV106-LIQUIDITY-WEAK | pv106 | pv106不再投任何变体 | pv106 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-PV30-LABEL-TRAP | group_label_as_signal | GROUP 型数据集（字段大多为聚类整数标签）禁止把标签字段包裹 rank/ts_*/days_from_last_change 当信号用；标签只能作 group_* 算子的分组维，且分组维字段必须是平台 GROUP 类型（MATRIX 数 | pv30 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-WAVE96-UNLIT-BARE-SIGNAL-DEAD | intraday_pv_feats/risk59/shortinterest38/mmp_nlp_sentiment b | do not re-probe these 4 datasets with bare rank/vec_avg skeletons; need multi-field combos or event-persistence designs  | intraday_pv_feats | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-09~13 会话实证（100+ 条实验）：**`pv47` 是 PV 类别的活路（5/6 闸）**

上文判死记录覆盖 5 个数据集（continuation_score / pattern_scores / pv106 / pv30 / intraday_pv_feats）；
**`pv47`、`pv103`、`pv13`、`pv14`、`pv149`、`pv20` 均不在判死名单**。本会话实测——

#### ★ 核心构型（当前 KOR 未点亮塔唯一「5 项硬闸过 4 项」的解）

```
BASE = multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 160))),
                rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 132))),
                rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 252))))
ALPHA = trade_when(greater(rank(adv20), 0.1), scale(BASE, shortscale=0.5), -1)
设置：KOR / TOP600 / D1 · decay 4 · **neutralization=MARKET** · trunc 0.08 · nanHandling ON
塔：KOR/D1/PV(1.4) ← 0 计数
```

| alpha | S | F | TO | SUB | 2Y | investability / 限 | self |
|---|---|---|---|---|---|---|---|
| **`O08jNNKd`** | **1.97** | **1.12** | 0.461 | 1.58 | 1.58 | **1.28 / 1.38** | — |
| `58gePWJM`（纯 BASE）| 1.88 | 1.03 | 0.509 | 1.52 | **1.59** | 1.20 / 1.32 | **0.36** ✅ |
| `d51MWeZ2`（过滤 0.05）| 1.83 | 1.00 | 0.479 | 1.52 | **1.92** | 1.16 / 1.28 | — |

#### ★★ 两条关键机理（本会话实证，跨族可参考但**禁外推**）

1. **`ts_kurtosis` 是 2Y 的钥匙**：把 PV 未点亮塔的 2Y 天花板从 **1.15 抬到 1.59（+38%）**。
   形态 `multiply(rank(-ts_kurtosis(X,160)), rank(-ts_rank(X,132)), rank(-ts_rank(X,252)))`（同字段多窗 ⇒ 合规）。
   **成立条件：X 必须是「日频收益/价量分布型」字段**（峰度 = 收益尾部风险 = 2022–23 熊市防御轴）；
   套到情绪/事件/结构类字段上全部失效（4 个跨族数据集验证：S 0.0~0.92）。
2. **`MARKET` 是 KOR 唯一「F 与 2Y 兼顾」的中性化档**：同族实测 STATISTICAL F0.85/2Y1.51、INDUSTRY 1.10/1.20、
   SECTOR 1.09/1.50、**MARKET 1.03/1.59**。另两档未试档更差：CROWDING（F1.02/2Y1.42，inv 保留率 59%）、
   REVERSION_AND_MOMENTUM（F0.82/2Y1.50，保留率 57%）。

#### ⚠ 唯一剩余障碍：`LOW_INVESTABILITY_CONSTRAINED_SHARPE`（**机制级，78 条实验判定**）

- 该项 **限 = 0.70 × S** ⇒ 需「保留率 ≥ 70%」；`pv47_spret` 族稳定在 **57–65%**。
- **提 S 无用**（限同步抬高）；**KOR D1 只有 `TOP600` 一个 universe**（`get_platform_setting_options` 实测）⇒ 无法换档位。
- **已试无效**：流动性过滤 8 档（adv20>0.05 → 2Y 1.92 但 inv 1.16；adv20>0.1 → inv 1.28 但 2Y 1.58；**两者无交点**）、
  市值过滤（方向相反）、`scale(longscale)`（平台只对 short 端生效）、流动性/市值中性化、truncation 0.02/0.15、decay 1/8。
- **根因**：特质收益反转的 alpha 来源**就在小票上**（向非流动股提供流动性）—— 过滤越强 alpha 越少。**这是机制属性**。

#### 其它实测（勿重试）

- **降 TO 七手段全部等比例杀 S**：`ts_mean` / decay / `hump` / `ts_decay_linear` / 长窗口（462/1008/2016 全不降 TO）/
  `trade_when` 门控（TO 0.82→0.12 但 S 2.65→0.80）/ `ts_target_tvr_decay`（TO→0.225 但 S→0.67）。
  **唯一成功的是 `multiply(rank(A), rank(B))` 双腿乘积**（TO 0.82→0.41 且保住 S）。
- **`pv103`（收盘集合竞价 14:30–14:30，7 字段 cov 1.0）** 套同一模板 ⇒ 最高 S **1.28**（`inTRI`），判死。
  平台字段名 = `session_1430to1430_{final_trade_price, initial_trade_price, market_value, max/min_trade_price, total_traded_volume, volume_weighted_avg_price}`。
- **KOR 不可用算子**：`ts_ir`、`ts_target_tvr_hump`（整批连坐 FAIL 且**无报错**）。
- **发批前三闸**：`ensure_safe_for_dispatch`（元数违规整批连坐）+ 新算子 2 条小批验存在性 + 字段 `get_datafields` 实名核对。
- **僵尸批次判据修正**：`children=0` 且 `progress` 非空（0.35/0.9）**只是慢，不是僵尸**（实测卡 0.35 约 25 分钟后自行 COMPLETE）；
  multi-sim location 约 **24h 过期 ⇒ 当天收割**。

**未试的 PV 数据集**：`pv13`(36/882/cov 0.819，含 GROUP 分组轴 + 地理收入敞口)、`pv149`(2/3)、`pv29`、`pv20`(6/16，元数据无用)。
**已实测判死**：`pv103`（收盘竞价，8 条最高 S 1.28）、`pv14`（期货基差 `lastclose/close`，8 条最高 S 0.27）。

#### ★★★★★★★★★★ RA 全闸通过（2026-10-13 里程碑）

```
zqrqpZX8 = vector_neut( trade_when(greater(rank(adv20), 0.1),
                     scale(multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 140))),
                                    rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 132))),
                                    rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 252)))), shortscale=0.5), -1),
                     power(rank(rsk68_weight_dadv), 0.5) )
```
| 闸 | 值 | 限 | |
|---|---|---|---|
| **`failed_ra_count`** | **0** | — | ✅ **RA 全闸通过** |
| **`failed_ppa_count`** | **0** | — | ✅ |
| Sharpe / Fitness | **1.90 / 1.16** | 1.58 / 1.00 | ✅ |
| Turnover | 0.4415 | 0.70 | ✅ |
| Sub-universe S | **1.71** | ~0.94 | ✅ |
| **2Y (ladder)** | **1.92** | 1.58 | ✅ |
| **investability** | **1.33** | 1.33 | ✅（保留率 70.0%）|
| **self** | **0.397** | 0.70 | ✅ |
| **prod** | **0.7292** | 0.70 | ❌ 最后一道墙 |
| 塔 | KOR/D1/RISK(1.3) + KOR/D1/PV(1.4) | **effective 2** | 两个 0 计数塔 |

**第二颗 `KPmPa3xl`（pow 0.75）**：S1.87 / F1.17 / TO0.429 / 2Y1.80 / inv1.34、**failed_ra_count = 0**、self 0.397 ✅、prod 0.7485 ❌。

**★ 破墙三要素（缺一不可）**：
1. `ts_kurtosis(spret, **140**)`（防御腿；**K 窗口决定 2Y**：132→1.50、**140→2.02**、150→2.00、160→1.47）
2. `trade_when(rank(adv20)>0.1)` + `scale(·, shortscale=0.5)`（流动性过滤 + 空端缩放）
3. **`vector_neut(·, power(rank(rsk68_weight_dadv), pow))`**（残差到美元 ADV 轴 —— 保留率的钥匙）
   pow 档位与两闸：0.25 → 2Y 2.02 / inv 67.2%；**0.5 → 2Y 1.92 / inv 70.0% ✅**；
   0.75 → 2Y 1.80 / inv 71.7% ✅；1.0 → 2Y 1.56 / inv 73.2%。
   ⇒ **pow=0.5 是 2Y 与 investability 的交点。**

**下一步（破 prod 墙）**：按 `wq-window-valley-break-prod-wall` skill，先取 prod 直方图 [0.7,0.8) 桶 n 值判族级命运
（n=0 可救 / n≥1 必死）；再扫 `ts_rank` 的第二/三窗与 pow 微调（0.55/0.6/0.65）找谷底。

#### ★★ 轴强度前沿（2026-10-13 实测）：investability ↔ 2Y **严格反向**

neut 轴越**强**，investability 越高但 2Y 越低（因为 2022–23 的防御性收益 = 非流动性溢价）：

| neut 轴 | S | 2Y | investability / S |
|---|---|---|---|
| `rank(rsk68_weight_dadv)`（pow 1.0）| 1.83 | 1.47 | **73.2% ✅** |
| `power(rank(dadv), 0.5)` | 1.86 | 1.53 | 居中 |
| `power(rank(dadv), 0.25)` | 1.90 | **1.58** | 67.4% ❌ |
| `rank(adv20)` | 1.71 | 1.53–1.56 | 66.9% ❌ |

**两颗最优（各差一点）**：
- **`bl8YA7OK`**：S1.83 / F1.16 / TO0.422 / SUB1.64 / **inv 1.34 ✅（73.2%）** / **ppa_failed=0** / **仅差 2Y（1.47，差 0.11）** / 塔 RISK+PV effective 2。
- `omom7Jan`：S1.90 / F1.11 / TO0.456 / **2Y 1.58（差 0.01）** / inv 1.28（限 1.33，差 0.05）。

**已证反向的补 2Y 手法**：`group_rank(neut信号, bucket(rank(股息)))` ⇒ 2Y **0.47**（不可用）。
**待试**：pow∈(0.25,1.0) 细扫求交点；`trade_when` 条件式补 2Y；低 S 档（低限 ⇒ inv 更易过）。

#### ★★★★★★ 破墙（2026-10-13）：`vector_neut` 到 RISK 的美元 ADV 轴 —— **investability 首次通过**

```
几何 = vector_neut( trade_when(greater(rank(adv20),0.1), scale(BASE, shortscale=0.5), -1),
                    rank(rsk68_weight_dadv) )
（rsk68_weight_dadv = risk68 的美元 ADV，cov 1.0）
```
| 闸 | 值 | 限 | |
|---|---|---|---|
| LOW_SHARPE | **1.83** | 1.58 | ✅ |
| LOW_FITNESS | **1.16** | 1.00 | ✅ |
| LOW_TURNOVER | 0.4217 | 0.70 | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | **1.64** | ~0.94 | ✅ |
| **LOW_INVESTABILITY_CONSTRAINED_SHARPE** | **1.34** | 1.281 | ✅ **通过（保留率 73.2%）** |
| **`ppa_failed_count`** | **0** | | ✅ |
| IS_LADDER_SHARPE (2Y) | **1.47** | 1.58 | ❌ 差 0.11 |
| 塔 | **KOR/D1/RISK(1.3) + KOR/D1/PV(1.4)** | effective **2** | 两个 0 计数塔 |

**机理（关键）**：`vector_neut` 剥离信号对「流动性/小票」的暴露 ⇒ 保留率 **57–65% → 73.2%**，investability 首次通过。
**但代价**：2Y 被封顶 **~1.45–1.49**（无 neut 时可达 1.92）—— 因为 **2022–23 KOR 的防御性收益本身就来自非流动性溢价**。
⇒ **2Y 与 investability 是同一枚硬币的两面**（同由非流动性溢价驱动）⇒ 必须在两者间找交点。

**轴强度阶梯实测**（越强越削 2Y）：`rsk68_weight_dadv`（原始，2Y 1.23）> `rank(dadv)`（2Y 1.47）> `rank(edadv)`（1.46）；
`rank(rsk68_weight_volatility_short)` 反而把 2Y 削到 0.62（波动轴不适合作残差）。

**下一轮方向**：① 更弱的 neut 轴（`power(rank(dadv),0.5)` / `quantile(dadv)`）求平衡点；
② 用**非流动性无关的防御轴**（如 analyst48 股息族，2Y 1.84）做 `group_rank` 分组补 2Y；③ kurtosis 窗口细扫。

#### ★★★ 决定性检查（2026-10-13）：三颗候选**除 investability 外全部闸都过**

| alpha | self | **prod** | S | F | TO | 2Y | investability / 限 |
|---|---|---|---|---|---|---|---|
| **`58gePWJM`** | **0.360** | **0.691** ✅ | 1.88 | 1.03 | 0.509 | **1.59 ✅** | **1.20 / 1.32** |
| `O08jNNKd` | 0.355 | **0.669** ✅ | **1.97** | **1.12** | 0.461 | 1.58（差 0.01）| 1.28 / 1.38 |
| `JjPVeW7n` | 0.366 | **0.670** ✅ | 1.83 | 1.00 | 0.485 | **1.61 ✅** | 1.12 / 1.28 |

⇒ **prod（0.67–0.69）与 self（0.36）双端点全部通过** ⇒ 这不是 prod 墙，**唯一卡点就是 investability**。
⇒ `58gePWJM` 是**只差一项**的候选（gap 0.12）。

#### ☑ investability 穷尽度：**115 条实验 / 7 大类杠杆 / 全部失败**

| 杠杆类 | 结果 |
|---|---|
| 结构 | 多窗乘积 / 幂变换 `signed_power` / 纯多 / 纯空 / `if_else` 条件翻转 / 残差 —— 全败（`sp_half` 保留率反降到 61%）|
| 中性化（11 档全试）| 最优 MARKET（保留率 65%）；CROWDING 59%、REV_AND_MOM 57% |
| 过滤 | 移除式 `trade_when`（inv +0.07 但 2Y −0.03）/ 加权式 `×rank(adv20)`（S→1.05）/ 外部条件翻转（S→−0.65）|
| 设置层 | decay 1/8、truncation 0.02/0.15、nanHandling、**`maxTrade=ON`（S 1.88→1.28）**、**`maxPosition=ON`（平台拒绝：`not available for region KOR`）** |
| 市值/流动性中性化 | `group_neutralize` 到桶 / `vector_neut` —— 无变化 |
| universe | KOR D1 **只有 TOP600** |
| 外部配方 | 顾问公开 prompt 的 investability 配方实测全败 |

**结论**：`LOW_INVESTABILITY`（限 = 0.70×S，保留率恒 57–65%）是本族**机制级**障碍 ——
特质收益反转的 alpha 来源就在小票上，无论怎么改结构/设置都不动。

#### 外部 investability 配方实测失败（2026-10-13，勿重试）

**来源**：外部检索（论坛工具 `search_forum_posts` 连续 4 次报 `unexpected error`，已不可用 ⇒ 改走 WebSearch）。
某 BRAIN 顾问公开 system prompt 宣称 investability 标准配方是 `EXPR * rank(adv20)` 或 `if_else(adv20 > 阈值, EXPR, -EXPR)`。
**在 KOR `pv47_spret` 上实测（d196，8 条，MARKET/decay4/trunc0.08）全部劣于基准**：

| 配方 | S | 2Y | vs base |
|---|---|---|---|
| base（无过滤）| **1.88** | **1.59** | — |
| `EXPR * (rank(adv20)+0.5)`（软化版）| 1.59 | 1.40 | −0.29 |
| `EXPR * rank(adv20)` | 1.05 | 0.95 | −0.83 |
| `if_else(adv20>0.5, EXPR, 0)`（消除式）| 0.69 | 0.98 | −1.19 |
| `if_else(adv20>0.5, EXPR, -EXPR)` | −0.65 | −0.26 | — |
| `if_else(cap>0.5, EXPR, -EXPR)` | −0.08 | 0.42 | — |
| `if_else(adv20>0.7, EXPR, -EXPR)` | −1.54 | −1.23 | — |

⇒ **条件翻转（if_else … −EXPR）在本族严重反向**；流动性加权（× rank(adv20)）与移除式一样杀 S。
⇒ **外部通用配方不迁移到 KOR/pv47 —— 再次印证「杠杆族相关」**。

**同批检索的两条有用确认**：
- `Fitness = Sharpe × √(Returns / max(Turnover, 0.125))` —— **TO < 12.5% 不再提升 fitness**（与本会话 `tvrd20/25` 观测一致）。
- 有外部文档称 `ts_kurtosis` 在 FastExpr 不可用 —— **与 KOR 实测不符**（本会话该算子批全部成功，S 最高 2.75），**以平台实测为准**。
<!-- profiles:manual:end -->
