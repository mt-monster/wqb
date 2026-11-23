# price_signal_dl 字段画像（ASI / MINVOL1M / D1）

> 战役：ASI/D1 Power Pool Dec'26 theme（2026-11-23 ~ 12-20）
> 全字段探测：28/28（`complete=true`，禁止抽样硬闸合规）
> 拉取日期：2026-11-22；来源：`get_datafields(dataset_id=price_signal_dl, ASI, MINVOL1M, D1, filter_sharpe=false)`

## 数据集级

| 项 | 值 |
|---|---|
| 名称 | Deep Learning Price Signal Dataset |
| 类别 | model（pyramid 1.3） |
| coverage | 0.9129（PPA 三门槛 ✓） |
| alphaCount | 158（≤50 硬闸超标 → 不做 PPA 主攻，RA 单集路线） |
| valueScore | 5.0 |
| 字段数 | 28（全 MATRIX） |
| onboard | 2026-03-01（新集，蓝海窗口） |

## 字段全表（4 族 × 7，28/28）

| 字段 | 族 | 形态 | cov | ac | user |
|---|---|---|---|---|---|
| `normalized_trend_indicator_0` | trend | normalized | 0.9209 | 12 | 9 |
| `normalized_trend_indicator_1` | trend | normalized | 0.9209 | 8 | 8 |
| `normalized_trend_indicator_2` | trend | normalized | 0.9209 | 8 | 8 |
| `normalized_trend_indicator_3` | trend | normalized | 0.9246 | 7 | 4 |
| `normalized_trend_indicator_4` | trend | normalized | 0.9246 | 11 | 10 |
| `normalized_trend_indicator_5` | trend | normalized | 0.9246 | 4 | 4 |
| `normalized_trend_indicator_6` | trend | normalized | 0.9209 | 10 | 9 |
| `normalized_volume_indicator_0` | volume | normalized | 0.9228 | 2 | 2 |
| `normalized_volume_indicator_1` | volume | normalized | 0.9189 | 2 | 2 |
| `normalized_volume_indicator_2` | volume | normalized | 0.9190 | 1 | 1 |
| `normalized_volume_indicator_3` | volume | normalized | 0.9228 | 5 | 4 |
| `normalized_volume_indicator_4` | volume | normalized | 0.9228 | 4 | 4 |
| `normalized_volume_indicator_5` | volume | normalized | 0.9228 | 2 | 2 |
| `normalized_volume_indicator_6` | volume | normalized | 0.9180 | 7 | 5 |
| `raw_trend_indicator_0` | trend | raw | 0.9023 | 8 | 7 |
| `raw_trend_indicator_1` | trend | raw | 0.9023 | 7 | 6 |
| `raw_trend_indicator_2` | trend | raw | 0.9023 | 4 | 4 |
| `raw_trend_indicator_3` | trend | raw | 0.9058 | 2 | 1 |
| `raw_trend_indicator_4` | trend | raw | 0.9059 | 3 | 3 |
| `raw_trend_indicator_5` | trend | raw | 0.9059 | 5 | 5 |
| `raw_trend_indicator_6` | trend | raw | 0.9023 | 15 | 12 |
| `raw_volume_indicator_0` | volume | raw | 0.9059 | 5 | 5 |
| `raw_volume_indicator_1` | volume | raw | 0.9021 | 4 | 3 |
| `raw_volume_indicator_2` | volume | raw | 0.9022 | 1 | 1 |
| `raw_volume_indicator_3` | volume | raw | 0.9059 | 9 | 7 |
| `raw_volume_indicator_4` | volume | raw | 0.9059 | 5 | 5 |
| `raw_volume_indicator_5` | volume | raw | 0.9059 | 6 | 5 |
| `raw_volume_indicator_6` | volume | raw | 0.9012 | 5 | 4 |

**形态语义**：raw = 未调整原值（跨标的量纲不可比，禁直接横截面）；normalized = 已重标定（可直接 rank/group）。trend = 趋势类（动量/均线族）；volume = 量能类。

## 实测读数（六法体检 · 探针后回填）

> 按流水线 S1 六法（最小 6 条/字段）逐字段回填实测；矩阵族先水平、一阶差、分位、比值/信噪比。

| 字段 | 法1水平 | 法2差分 | 法3分位 | 法4比值 | 判定 |
|---|---|---|---|---|---|
| （探针批 P0 回填） | | | | | |

## 模板准入（按字段属性推定，回测裁决）

- **normalized 族**（已重标定）：合法模板 = `group_neutralize(rank(x), industry)` / `group_zscore(x, subindustry)` / `ts_rank(x, 22)`——model 类别卡禁裸 rank(model_score)，必须组内去板块 bet
- **raw 族**：先 `ts_zscore(x, 66)` 或 `divide(x, ts_mean(x,66))` 自标准化再同上
- **组合形态（同集 ATOM）**：trend × volume 同集字段 add 合法（2026-11-20 用户裁定：ATOM 只判字段同源、算子不设限；量纲不同须先各自标准化）
- **窗口白名单**：level [22,66,252]、change [5,22]（类别卡）

## 已知风险

1. **成品因子 prod 墙**：model 类别卡——「成品模型分数的热门字段 prod 墙最硬」。本集 ac 1–15 极冷门，是主要红利；但 users 高的字段（raw_trend_6 ac=15）优先级降低
2. **JPN 子集墙**：ASI 结构性硬墙（wave12-26 共性死因 LOW_ASI_JPN_SHARPE）——探针批必带此读数
3. **2Y 闸 1.6**：ASI 阈值高于标准 1.58；趋势类信号天然慢，2Y 应是优势项

## 4. TemplatePlan（每字段一行：reading / templates / excluded / evidence）

| 字段族 | 合法模板 | 排除 | 依据 |
|---|---|---|---|
| normalized_trend_*（7） | `group_rank(group_zscore(x, country), industry)`（内层 country z + 外层 industry rank，双向各一）；`ts_rank(group_zscore(x, country), 22)` | 裸 `rank(x)`（model 类别卡禁）；`ts_mean` 平滑（信号已是重标定值，平滑无信息） | 论坛帖 45201936320919（模板2 双层 z 内层结构）+ 模型类别卡「禁裸 rank(model_score)」 |
| normalized_volume_*（7） | 同上结构（volume 族信号语义不同，方向由探针定）；`ts_delta(x, 5)` 量能变化 | 裸 `rank(x)`；未去板块直接横截面 | 同上 |
| raw_trend_*（7） | 必须先自标准化：`ts_zscore(x, 66)` 或 `divide(x, ts_mean(x, 66))` 再接外层 group_rank(country) | 直接横截面（跨币种量纲不可比——论坛「多币种卫生」条） | 论坛帖 45201936320919（多币种卫生 Do/Don't） |
| raw_volume_*（7） | 同 raw_trend 处理链 | 直接横截面 | 同上 |

**经济机制**：DL 优化的传统价量指标（趋势族=动量/均线语义，量能族=量价确认语义）。normalized 形态已跨标的可比；raw 形态须自身历史标准化。trend×volume 同集 add 合法（ATOM 字段同源裁定 2026-11-20，各自先 group_zscore 归一）。

**中性化起点**：SLOW / COUNTRY（论坛帖实测 SLOW 在 model 类抬 JPN Sharpe 显著）——覆盖区域 settings.json 的 SUBINDUSTRY 缺省，用 --set 显式传。
**Robust 保险**：主 S 控制在 1.4–2.3（论坛：>2.5 触发动态 90% 天花板陷阱）；必要时方差凸性 `ts_covariance(x,x,22)` / 收紧 trunc 0.05。

## 5. 探针计划（P0 批 8 臂，preflight 全过）

判据：cov 0.92 非稀疏 ⇒ 门控不适用；字段已是「重标定信号值」⇒ 内核近似正态 ⇒ 外层 group_rank 与 group_zscore 都试。

| # | 表达式骨架 | 测什么 |
|---|---|---|
| 1 | group_zscore(normalized_trend_indicator_0, country) | trend 族水平基线（COUNTRY 轴） |
| 2 | group_rank(group_zscore(normalized_trend_indicator_0, country), industry) | 内层country+外层industry（论坛模板2） |
| 3 | group_zscore(normalized_volume_indicator_0, country) | volume 族水平基线 |
| 4 | group_rank(group_zscore(normalized_volume_indicator_0, country), industry) | volume 同构对照 |
| 5 | ts_zscore(raw_trend_indicator_0, 66) | raw 自标准化水平 |
| 6 | ts_zscore(raw_volume_indicator_0, 66) | raw volume 自标准化 |
| 7 | group_rank(ts_delta(normalized_trend_indicator_0, 5), country) | trend 短窗变化（动量方向） |
| 8 | group_rank(ts_delta(normalized_volume_indicator_0, 5), country) | volume 短窗变化 |

设置统一：ASI/MINVOL1M/D1、SLOW 中性化、decay 4、trunc 0.08、maxTrade ON（论坛起点档）。方向不明的族正反双向由 P1 补。

## 6. P0 探针实测读数（2026-11-22，8 臂 + 4 补充臂）

设置：ASI/MINVOL1M/D1、SLOW、decay4、trunc0.08、maxTrade ON。

| # | 表达式 | alpha | S | F | TO | JPN | 2Y | Robust-S/Ret |
|---|---|---|---|---|---|---|---|---|
| 1 | `group_zscore(normalized_trend_indicator_0, country)` | XgaMajj8 | 0.20 | 0.03 | 21.7% | 0.04 | 0.34 | 0.06/0.0011 ✗ |
| 2 | `group_rank(group_zscore(normalized_volume_indicator_0, country), industry)` | 9qlkGLAe | 0.09 | 0.01 | 16.6% | **−0.74** | −0.90 | ✓/✓ |
| 3 | `ts_zscore(raw_volume_indicator_0, 66)` | 0mP5NgW1 | 0.20 | 0.03 | 19.6% | −0.17 | −0.49 | ✗/✗ |
| 4 | `group_rank(ts_delta(normalized_volume_indicator_0, 5), country)` | rK780gYm | 0.47 | 0.09 | 27.6% | −0.45 | 0.07 | 0.26/0.0055 ✗ |
| 5 | `group_rank(ts_delta(normalized_volume_indicator_1, 5), country)` | YPaYE9Wl | **0.59** | 0.11 | 35.4% | −0.41 | 0.41 | 0.49/0.0111 ≈ |

**平台行为发现（重要）**：trend_i 与 volume_i 提交返回**同一 alpha ID**（实读 code 均为 volume 版）⇒ 该集有效独立信号 = **7 条**（4 族×7 实际是 trend/volume 孪生 × raw/normalized 两形态）。全字段探测分母按 7 个独立信号计。

**归因**：
1. **变化形态 >> 水平形态**：delta5 族 S 0.47–0.59，水平族 0.09–0.20 ⇒ 信号载体是变化量
2. **字段号单调**：vol_0 delta5 0.47 → vol_1 delta5 0.59（2..6 待测）
3. **JPN 全负（−0.74~0.04）**：结构性墙，与本区历史死因（wave12-26 LOW_ASI_JPN_SHARPE）同构
4. 水平形态 group_rank 后 Robust 反而 PASS（9qlkGLAe）——但 S 0.09 无意义

**通道坑（登记）**：`create_multi_simulation` 2 条批在本区域 6/6 全 FAIL（无错误详情），同表达式同设置单发重派 COMPLETE ⇒ multisim 序列化问题。应急链路 = 单发 POST `/simulations`（brain_client）。**平台去重伪影**：不同表达式（trend vs volume）返回同一 alpha id，归因只认实读 `code`。

## 7. 梯度 L1–L4 汇总 + JPN 破闸检索（2026-11-22）

冠军骨架：`group_rank(ts_av_diff(normalized_volume_indicator_6, 22), country)`，INDUSTRY 中性化。

| 层 | 臂 | S | F | 2Y | JPN | 结论 |
|---|---|---|---|---|---|---|
| L0 基线 | v6 d5 | 0.93 | 0.27 | 0.93 | 0.22 | 起点 |
| L1 算子族 | avdiff22 | 0.95 | 0.35 | 1.13 | 0.16 | 全指标↑，SLOW 档 |
| L2 中性化 | avdiff22 INDUSTRY | 1.23 | 0.73 | 2.08 | 0.03 | 2Y 过闸，JPN 仍 0 |
| L3 分组轴 | avdiff22 market/IND | 1.29 | 0.88 | 1.19 | 0.01 | F 峰，2Y 掉 |
| L3 字段5 | v5 avdiff22 country | 1.27 | 0.73 | 2.27 | 0.03 | 2Y 最强 |
| L4 exchange 轴 | v5 avdiff22 exchange | 1.29 | 0.74 | 2.34 | **0.03** | sub 0.87，JPN 不救 |
| L4 方差凸性 | cov(x,x,22) exchange | 1.03 | 0.88 | 1.58 | 待测 | margin 22.5bp |

**JPN 结构墙结论**：40+ 臂（4 形态族 × 全字段 × 5 分组轴 × 4 中性化档 × 窗口轴）JPN 恒在 0.01–0.22，与历史 wave12-26 完全同构。按 D15 只记 PROVISIONAL，**不写数据集级判死**（用户红线）；但可判定 `price_signal_dl` 的 volume-shock 机制在 ASI 无日本定价力。

**论坛 JPN/单区破闸三源（2026-11-22 核验全文）**：
1. 帖 44713280965527（18 赞，GLB/EMEA 十余批）：单腿结构站级微调无效（54-alpha 扫描全灭）；修复力在**正交辅助腿**——双尺度复合体（慢腿长窗+平方扛 F/Margin，快腿窗=1+内层 country+无平方扛区域分）；分组层最大单一杠杆=内层 exchange 去均值(+0.58)；两腿分组必须交叉（sector×exchange）
2. 帖 44888868944023（ZH41150）：**流动性残差** `vector_neut(signal, sqrt(20日均成交额))` 使 KOR 波动信号 S 0.99→2.17、保留率 37%→75%；帖子明说 ASI 某集 47/47 全部卡此项——风险模型波动/规模信号最易卡
3. 帖 45201936320919（官方 ASI 课）：内层 country z + SLOW 档 + 主 S 勿超 2.5

**当前验证**：双尺度正交腿 add(slow22+fast1) 两变体已派（MCP 通道）。若不救 JPN → 转向 JPN 高覆盖数据集（论坛推荐 model77 / fundamental23 / analyst69 / shortinterest3）。

## 8. 双尺度正交腿验证（论坛帖①方法）— JPN 终判

按论坛帖 44713280965527 的双尺度复合体（慢腿长窗 + 快腿窗1 内层 country、两腿分组交叉）：

| alpha | 表达式 | S | F | 2Y | sub | JPN | Robust |
|---|---|---|---|---|---|---|---|
| d5aPkw5x | `add(gr(avdiff(vol6,22),country), gr(ts_delta(vol6,1),industry))` | **1.61 ✓** | 0.95 | **2.36 ✓** | **1.10 ✓** | **0.06 ✗** | 85% |
| Wjlx1mjx | `add(gr(avdiff(vol6,22),industry), gr(ts_delta(vol6,1),country))` | 1.60 ✓ | 0.94 | 2.04 ✓ | 1.17 ✓ | 待测 | — |

**结论**：双尺度把主指标全部救过闸（S/F/2Y/sub），但 JPN 仍 0.06。跨越 60+ 臂（4 形态族 × 全 7 字段 × 5 分组轴 × 4 中性化 × 窗口轴 × 双尺度 × 方差凸性）JPN 从未超 0.22 ⇒

**PROVISIONAL 机制层判定**：price_signal_dl 的 volume-shock 机制在 ASI/JPN 无定价力。非数据集级判死（不写死键，符合用户红线），但停止在本集继续投入。论坛帖①的"正交腿修复力"只适用于"有信号但被平滑压住"的场景（EMEA），本集 JPN 是"根本无信号"，正交腿无效。

**换集理由（用户要求说明）**：JPN 破闸三法（双尺度/流动性残差思路/分组轴）+ 60+ 臂梯度全试，JPN 恒 0.01–0.22；本集信息源级无日本定价力，继续投入是烧配额。转 JPN 高覆盖集（论坛推荐：fundamental23/17、analyst69、shortinterest3；⚠ model77 在 ASI/MINVOL1M 实测 0 字段不可用）。
