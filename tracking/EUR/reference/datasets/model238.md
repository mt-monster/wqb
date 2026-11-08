# model238 · EUR / TOPCS1600 / D1 字段画像（SmartHoldings）

> 类型 MATRIX · 44 字段（基版 + `_d1` 延迟一日版）· cov 0.78（基）/ **0.96（_d1）** · category = **model**（×1.3）· αC 26
> 采集：2026-11-08 · 论坛帖 `40847481080087`（MY82844）提示 institutions6 @ CROWDING 在 GLB 可行——本集是「机构持仓概率模型」

## 0. 字段结构（4 分组 × 4 分量 × 2 时效 = 全排列）

| 分组 | global / region / country / sector / industry |
|---|---|
| 分量 | owner（Smart Holdings 主分）/ change（持仓动量）/ screening（风格适配）/ peer_concentration（拥挤度,反向语义） |
| 时效 | 基版（cov 0.78）/ `_d1`（cov 0.96——**d1 版覆盖更高,主力用 d1**） |

**机制假设**：
1. **机构持仓动量**（`change` 分量）：机构增持概率上升 → 后续超额（聪明钱跟随,与 institutions6 buyers 0.95 同向但模型分更干净）
2. **拥挤反转**（`peer_concentration`）：高拥挤 → 反转（论坛帖的 reversal 语义）
3. **风格适配**（`screening`）：机构偏好的风格特征 → 机构持续买入

## 1. 探针设计（5 臂,d1 版,存量直读——本集也是存量态字段）

1. `rank(mdl238_global_change_rank_d1)` 裸读数（已是 rank 语义,无需再标准化）
2. `rank(mdl238_region_change_rank_d1)`
3. `reverse(rank(mdl238_global_owner_rank_d1))`（拥挤反转）
4. `rank(mdl238_region_screening_rank_d1)`（风格适配,αC=7 最热）
5. `rank(mdl238_industry_rank_d1)`（主分,行业相对）

@ FAST / decay 15（model 分是合成因子——behavioral_signals 实证合成因子吃时序不吃截面,先 FAST 对照）/ TOPCS1600

## 2. 实测

（待回填）

## 2. 实测

### 2.1 首探针（multisim `1EyL1igjg5018RcsAXwR1rF`，FAST/decay15）——全战役最强原始读数

| 变体 | alpha id | S | F | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|
| **industry_rank_d1（行业相对主分）** | `QPvzv11M` | **2.06** | **1.51** | 2.30 | 0.52（闸 1.09） | 0.53 | CW/sub/robust |
| **region_screening_rank_d1（风格适配）** | `d5WzKNNJ` | **2.00** | **1.50** | 2.17 | 0.49 | 0.54 | CW/sub/robust |
| global_change_rank_d1（动量） | `JjezP66n` | 1.53 | 0.84 | 1.66 | 0.45 | **−0.09** | sub/robust |
| region_change_rank_d1 | `pwdGv99j` | 1.53 | 0.84 | 1.66 | 0.45 | −0.09 | 同上（与 global 逐位同） |
| 拥挤反转 reverse(owner) | `bl6z8ee6` | 0.45 | — | — | — | — | 死 |

**归因**：① 主分/screening 的信息在行业相对位（2.06/2.00），但模型分集中持仓→CW+sub/robust 差；② 动量分信息弱且 robust 为负——「机构增持动量」已在价格里；③ 拥挤反转死。

### 2.2 ⚠ SLOW_AND_FAST 中性化归因（multisim `2FfuF93MC5dsb0NoWpI7weF`）

`industry_rank_d1` 在 S&F 下 S 2.06→0.70-0.76（三变体全崩）——**FAST 是本集唯一正确中性化**（模型分的 alpha 载在慢轴上，S&F 把它剥掉了；与 behavioral_signals 的「合成因子吃 FAST」教训一致但方向相反）。**此前的批次设计失误**：第二批错误地在 S&F 下跑修复，作废。

### 2.3 group_backfill 修复批（用户提示 `group_backfill` 解 CW；`2cY3xfdPh4wgcyy1740d8CST` 因缺 lookback 参数全 ERROR 作废；`2rsSym9N25e1akXQd6apL1y` 为修正版 FAST 档，进行中）

| 变体 | 设计 |
|---|---|
| `group_backfill(winsorize(主分,4), subindustry, 66, std=4)` | 组内 66d 回填补 NaN→分散持仓 |
| `group_backfill(group_scale(...), country, 66)` | 行业内 scale 后国家回填 |
| 完整栈 + backfill 前置 | zscore 栈打底 |

### 2.4 ★ group_backfill 破 CW（multisim `11eRZ56AZ5hX9zM7HtCyBVB`，FAST/decay15）

| 变体 | alpha id | S | F | 2Y | sub | robust | CW | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| backfill(subindustry) | `QPvz0eOw` | 2.05 | 1.47 | 2.33 | 0.65 | 0.59 | **PASS** | sub/robust |
| **backfill(scale→country)** | **`P0oz5eYE`** | **2.12** | **1.54** | 2.40 | 0.57 | 0.56 | **PASS** | sub/robust |
| 完整栈+backfill | `e75GaAVg` | 2.01 | 1.41 | 2.21 | 0.54 | 0.51 | FAIL | CW/sub/robust |

**归因**：① group_backfill 补 NaN 缺口分散持仓——CW 解决（2.06 首探针的 CW FAIL 在 backfill 后 PASS）;② S 反而抬升（2.06→2.12）——回填把组内信号加回来了;③ 剩余 sub 0.57/robust 0.56——模型分的 alpha 集中在头部股票,子宇宙外贡献 PnL。修复方向：quantile 整形（均匀化截面分布）。已提交。

⚠ 工程坑复盘：`group_backfill(x, group, d, std=)` 第 3 位置参数 `d`（lookback）必填——漏了导致 3 连 ERROR（`Required attribute "lookback"`）。

### 2.5 quantile 整形（multisim `TrLL5eJD5epbCzWBssrPv0`）——S 2.16 但 sub/robust 不动

| 变体 | alpha id | S | F | sub | robust |
|---|---|---|---|---|---|
| quantile(gaussian) | `wpQGoApQ` | **2.16** | 1.61 | 0.59 | 0.59 |
| quantile(uniform) | `GrWzmNrQ` | 2.05 | 1.47 | 0.65 | 0.59 |
| market backfill | `akKza8kw` | 2.07 | 1.49 | 0.56 | 0.54 |

**归因**：quantile 整形抬 S 不抬 sub/robust——**sub/robust 差不是分布问题，是信号位置问题**（alpha 集中在头部股票，sub-universe/robust universe 不含头部）。正解=换窄宇宙（TOP1200/TOP800 与信号所在段一致）。已提交双宇宙批。

### 2.6 窄宇宙崩盘（multisims `72zxF3sz4s8aI1LFRqOKCy`/`3JTYONgYe573aeo2fCu0SNd`）——sub/robust 之谜破解

TOP800 S=0.34、TOP1200 S=0.72（对比 TOPCS1600 的 2.12）——**信号根本不在头部，而在 TOPCS1600 的中尾部**（窄池切掉了信号段）。sub 闸差的根因修正：**sub-universe Sharpe 0.57 是因为信号在子宇宙外的中小盘**——这不是能靠 universe 修复的，是 sub/全宇宙结构性分布。

**model238 终判**：S 2.16（quantile gaussian 版）但 sub 0.59/robust 0.59 双卡（sub 比率闸 1.15、robust 0.7），全杠杆已试（backfill/quantile/分组/universe 四轴）。**结构性卡死——模型信号在中尾部股票，sub/robust 宇宙不含它。归档：S 2.16/F 1.61/2Y 2.35 的"半全绿"候选（CW 已修，sub/robust 结构性不可修）。**
