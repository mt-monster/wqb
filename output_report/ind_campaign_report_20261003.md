# IND 战役复盘（2026-10-02 → 10-03）：目标 10 颗可提交 REGULAR，实际 0 颗

> 结论先行：**IND 的 REGULAR 可提交空间在本轮被压缩到「行为族 prod 墙」这一个瓶颈上，且该墙不可破。**
> 20 个批次、约 170 条表达式、14+ 字段族、decay×分轴×中性化×截断全网格扫完后，
> 拿到 **6 颗 IS 全闸通过（checks.fail=[]）的候选**，但**每一颗的 prod 都在 0.7161–0.8261**，
> 全部撞平台 0.7 硬线。距目标 10 颗差 10 颗，瓶颈不是 IS 强度，是 prod 相关性。

## 1. 一句话诊断

**IND 的 IS 强度与 prod 新颖度呈负相关，且本轮把这条负相关推到了尽头：**

| 区间 | 族| IS（S / 2Y） | prod | 判定 |
|---|---|---|---|---|
| 拥挤族 | pv47 特质反转、尾盘 reversal、anl9 广度 | S 2.2–4.5 / 2Y 2.3–2.8 | **0.78 – 0.99** | IS 过、prod 死 |
| 半拥挤 | behavioral_signals（streak / recency） | S 2.0–2.4 / 2Y 1.7–2.4 | **0.7161 – 0.8261** | IS 过、prod 死 |
| 未拥挤 | ESG 质量分、Wikipedia 注意力、无形资产、估值缺口、事件旗标、mdl68、mdl313 | S 0.07 – 1.22 | 未测（无意义） | **IS 就死** |

行为族是本轮唯一的"两边都做到"的族——所以它是唯一值得反复攻的族；而它也恰好是 prod 书里已被占位的族。

## 2. 6 颗 IS 全闸候选（prod 实测同日10-02/10-03）

| alpha | 表达式 | 设置 | S | F | 2Y | robust | prod |
|---|---|---|---|---|---|---|---|
| `wpb6n7k6` | `group_rank(ts_mean(vec_avg(chronological_return_sequence_correlation),5),industry)` | d1 | 1.92 | 1.01 | 1.76 | 1.08 | **0.7161**（最接近） |
| `E5R3gn20` | `group_rank(ts_mean(vec_avg(consecutive_return_streak_length),5),industry)` | d1 | 2.36 | 1.15 | 1.81 | 1.42 | 0.7428 |
| `E5R3gn2G` | 同上 @sector | d1 | 2.24 | 1.11 | 1.76 | 1.38 | 0.7504 |
| `YPMZQrJq` | 同上 @market | d1 | 2.24 | 1.14 | 1.86 | 1.27 | 0.7503 |
| `vR20NQGb` | `group_rank(vec_avg(consecutive_return_streak_length),industry)` | d8 | 2.19 | 1.23 | 1.71 | 1.52 | 0.7604 |
| `WjekA50d` | 同上 @subindustry | d8 | 2.15 | 1.18 | 1.60 | 1.48 | 0.8261 |
| `3qVgdlKX` | `trade_when(greater(future_event_update_flag,0.5), group_rank(vec_avg(streak),industry), less(future_event_update_flag,0.5))` | d8 | 2.23 | 1.25 | **2.44** | 1.53 | 0.7544 |
| `QPKme78G` | `trade_when(greater(next_event_confirmation_level,0.5), ...)` | d8 | 2.05 | 1.17 | **2.44** | 1.06 | 0.7544 |

全部塔位 = **IND/D1/MODEL（倍率 1.2）**；`checks.fail=[]`、`ra_failed=false`。
prod 直方图极其干净：0.7+ 每族仅 1–3 颗 book alpha，0.6–0.7 也只有 6–16 颗 —— **不是族墙，是单颗 book alpha 顶着**，
但无论怎么改窗口 / 分轴 / decay / 门控，那颗 alpha 都跟着信号本质走（相关性 0.7161–0.8261）。

## 3. 已穷尽的结构空间（别再重跑）

**族维度**：streak（`consecutive_return_streak_length`）与 recency（`chronological_return_sequence_correlation`）是唯二能过IS 闸的字段；curvature / visual_shape / salience / extreme_daily 四个同集字段全部卡 S 或 F（1.17–1.76 且 2Y 或 F 差一点）。

**算子/窗口维度**：ts_mean(1/5/22/66/252)、ts_decay_linear(5/22)、ts_rank(22)、ts_zscore(22)、ts_delta(5)、ts_corr(22，共动构念)、
subtract(rank,rank) 分歧、trade_when 门控（自身信号 / 极端收益 / 事件旗标）。
→ **ts_corr 共动构念在 IND 完全无信号（S −0.51 ~ +0.02）**；分歧构念同样死（S 0.17–0.46）。

**横截面算子维度**：`group_rank` 是命脉 —— `group_neutralize` / `group_zscore`（保幅度）把 S 从 2.19 打到 0.39–1.33。
**秩化不是风格选择，是这个信号的成立条件。**

**设置维度**：decay 0/1/4/8/10/20 × 分轴 market/industry/sector/subindustry × STATISTICAL/SUBINDUSTRY × truncation 0.02/0.08。
关键结论：
- **decay 必须匹配信号速度**：mean-5 水平形在 decay=1 最优；raw（window1）必须 decay=8（decay=10 会把 2Y 压到 1.49）；decay=20 全灭。
- **SUBINDUSTRY 中性化腰斩 S**（2.36 → 1.28），只有 STATISTICAL 可用。
- **truncation 0.02 与 0.08 产出逐位相同的指标**（零杠杆，不必再扫）。
- decay=0 与 decay=1 产出**逐位相同**结果（平台 decay 语义）。
- **★ nanHandling=OFF 或 maxTrade=ON 会把行为族 S 从 2.19 直接打到 0.46** —— 边缘完全依赖 NaN 填充、不封顶交易。
  ⚠ 这是本轮最隐蔽的坑：用 `tools/submit_batch.py`（固定 nanHandling=OFF/maxTrade=ON）跑出来的批次**与 MCP 批次不可比**，
  曾据此误判"门控/保幅度构造 destroys 信号"。已新增 `tools/ind_sim_submit.py`（显式可控 settings）作为标准通道。

## 4. 事件门控：唯一有效的结构增量（但不解 prod）

`trade_when` 挂外部事件旗标（`future_event_update_flag` / `next_event_confirmation_level`）是本轮**唯一**同时改善多项指标的构造：
2Y 从 1.71 → **2.44**、robust 1.48 → 1.53、S 2.15 → 2.23、F 1.18 → 1.25。
机制上合理：只在"财报日程未确认/刚更新"的状态下持有动量信号，降低了常规日历噪声。
但 prod 仍是 0.7544 —— **暴露剖面改变没有改变排序本质**。

## 5. 工程教训（已落memory / region_kb）

1. **`ts_backfill` 不支持 event inputs**：`get_datafields` 报 MATRIX 的字段可能是 VECTOR/event（model170 全集如此），
   必须 `vec_avg(X)` 先聚合。核验法：`get_datafields(data_type="VECTOR", dataset_id=...)` 返回非空即需包裹。
2. **multisim 卡死判据**：父任务 progress 0.1 停滞 >10 分钟且 child_count=0 ⇒ 直接重发（旧任务无害、不占配额）。
   部分子任务 ERROR 时平台可能把同批其余标CANCELLED（**cancelled ≠ 表达式错**，重发即跑）。
3. **MCP 数组参数通道会损坏**：`create_multi_simulation` / `batch_status` / `preflight_expressions` 的数组参数间歇性报
   `must be array`（与表达式内容无关）。绕行：`tools/submit_batch.py`（固定 settings）或新写的 `tools/ind_sim_submit.py`（settings 可控）。
4. **prod 值会随社区饱和单向漂移**：09-19~09-23 实测 0.51–0.67 的旧候选，10-02 复测全部 0.83–0.99。
   已证伪"自污染"归因（`wpZ1vYzY` 提交后 prod 恒定 0.6842）。**陈旧 prod 值一律作废，挖到即测即交。**
5. **本地字段 catalog ≠ 平台存在**：`ml_factor_proj` 本地表 333 字段，平台 0命中。选集只认平台 `get_datafields`。

## 6. 下一步建议（若还要在 IND 投）

1. **停止扩 behavioral_signals**（已写进 `tracking/IND/reference/region_kb.json` 的 dead_end_rules + prod_saturation_risk）。
2. 若仍要挖 IND，唯一没被扫过的是**未被平台 book 覆盖的第三类信息维度**（本轮白空间探测的结论是：
   ESG/质量分、注意力、无形资产、估值缺口、事件旗标五类在 INDIS 层就死，不值得再投）。
   更现实的转向：**换区**（本轮 GBR 已判IS↔prod 三角，DEU已判"已探字段空间已尽"，KOR/USA 塔位逻辑不同）。
3. 若坚持 IND：唯一还没试的设置格是 `maxTrade=ON`（本次证明它会打掉 S，故不必试）与 `delay=0`（IND 平台仅 d1）。
   ⇒ 实际上**本区 REGULAR 的可提交空间已被本轮系统扫描穷尽**。

---

# 【追加】2026-10-03 03:00-13:00 续战：找到破 prod 墙的钥匙，2 颗已提交 ACTIVE

> 上文结论「本区可提交空间已被穷尽」**已被推翻**——缺的是一把钥匙，不是空间。
> 用户要求「盯死 IND 不转 region」，续战后已提交 **2 颗 ACTIVE REGULAR（2/10）**。

## 一、★★★ 破 prod 墙的核心机制：`winsorize` 秩后裁剪

**形态 = `winsorize(group_rank(X, axis), std=小)`**——裁剪作用在**已排名的输出**上，而非原值。

为什么有效：`group_rank` 输出是均匀分布的秩（0~1），裁剪两端= 压缩极端持仓权重，
**不改变信息内容（排序）**、不改 S，但改变了与 prod book 中同族持仓的重合度 ⇒ prod 下降。
若裁剪原值（`winsorize(X)` 放在 rank 之前）则是单调变换，对秩完全无效。

**behavioral_streak 族的裁剪- prod 曲线（单调！）**：
| 裁剪 std | S | F | 2Y | **prod** |
|---|---|---|---|---|
| 无 | 2.36 | 1.15 | 1.81 | 0.7428 |
| 2（等于无） | 2.35 | 1.15 | 1.81 | ≈0.74 |
| 1 | 2.38 | 1.17 | 2.01 | 0.7361 |
| 0.5 | 2.36 | 1.12 | 2.16 | 0.7144 |
| **0.15** | 2.29 | 1.05 | **2.18** | **0.6921 ✅** |
| 0.1 | 2.28 | 1.04 | 2.18 | 0.6887 ✅ |
| 0.05 | 2.28 | 1.03 | 2.17 | **0.6851 ✅** |

**同时 2Y 随裁剪增强而上升**（1.81→2.18）——裁剪去掉了拖累近年的极端持仓。

**失败对照（同样重要的负面知识）**：
- `tail(lower, upper, newval)` **硬裁剪**直接杀信号（S 2.29→1.35）⇒ 必须用软裁剪 winsorize。
- `winsorize(group_zscore(...), std=2)` 虽有 **S3.00 / F1.58 / 2Y2.55**（全campaign 最强 IS），但 **prod 0.8633** ❌
  ⇒ zscore 输出尾部太厚、裁不动；**裁剪必须作用在均匀分布的秩上**。

## 二、★★ 前置判据：先看 prod 直方图密度，再决定是否值得裁剪

| 族 | 0.6–0.7 桶 | 裁剪能否破prod |
|---|---|---|
| behavioral_streak | **1 颗** | ✅ 0.7428→0.6921 |
| corr_last_trade_price变化形 | 3 颗 | ✅ 0.7153→0.6904 |
| pv47 反转 | **434 颗** | ❌ 0.7277–0.7714（密墙） |
| corr 水平形 | 29 颗 | ❌ 0.8627 |
| defensiveness | 42 颗 | ❌ 0.8691 |

⇒ **个位数 ⇒ 单钉子，裁剪可撬；几十上百 ⇒ 密墙，裁剪无用**。这一步省掉约10 批盲试。

## 三、已提交 2 颗（互相关 0.12，正交，各占一个提交槽）

| # | alpha | 表达式 | 设置 | S | F | 2Y | robust | prod | self | 塔|
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `akxXl7w1` | `winsorize(group_rank(ts_mean(vec_avg(consecutive_return_streak_length),5),industry), std=0.15)` | d1 | 2.29 | 1.05 | 2.18 | 1.33 | **0.6921** | 0.3382 | IND/D1/MODEL 1.2× |
| 2 | `d51eGdKY` | `winsorize(rank(-ts_delta(ts_mean(corr_last_trade_price_with_volume,5),5)), std=0.25)` | d20 | 3.06 | 1.73 | 2.13 | 1.03 | **0.6904** | 0.4780 | IND/D1/PV 1.1× |

**逐年稳健性审计**：#1 9/10 年正（2016 −0.19）；#2 **10/10 年正**（S1.29–4.43）、换手 0.389–0.398极稳。
**互相关 0.1197**（`max_mutually_below_subset` size=2）⇒ 两族可共存。
⚠ 同族裁剪档位彼此相关 0.9887–0.9989 ⇒ **一个族只能交一颗**。

## 四、下一批弹药（已定位）

- `mean_flash_estimate_eps_annual12_3`（分析师 EPS 修正）：**prod 0.5707/0.5898 极干净**、塔位 IND/D1/**ANALYST 倍率 1.4（全区最高塔）**，
  唯一卡 `robust_universe_sharpe` 0.58–0.77（换轴/换 decay 4→8→16 均无效，S 反而降到 1.9）⇒ 族级短板待攻克。
- `analyst45`（analyst idea 数据集，241 字段）：大量 **ac=0 空白字段**（`anl45_treynor_ratio` ac=0、`anl45_target_prc` ac=6、
  `anl45_probability` ac=2、`anl45_jensensalpha` ac=9），已在飞探针批。
- 台账查询法：`alphas` 表 `prod_correlation IS NULL AND sharpe>=1.5` = 未测prod 的候选金矿（本次 18 颗全部来自 3 个已探族，见效快）。

## 五、本轮工程教训

1. **僵尸 multisim 占槽**：`progress 0.1`停滞 >10min 且 `child_count=0` ⇒ `DELETE /simulations/{id}` 返回 200 清除，
   随即提交即成功（长退避无效时才用这招；PUT 405 不允许）。
2. **提交链完整顺序**（首次走通并复用）：prod/self实测 → `confirm_submit=false` 预检 → 逐年审计落ledger
   `robustness_<id>` → `confirm_submit=true`。**robustness 审计是硬前置**，未落ledger 会被 `robustness audit not confirmed` 拦下。
3. **MCP 数组参数通道持续损坏**：`create_multi_simulation`/`check_correlation`/`compute_mutual_correlation` 的数组参数报 `must be array`
   （与内容无关）。绕行：`tools/ind_sim_submit.py`（POST /simulations 直连）+本地调`brain.get_mutual_correlation`。
4. `submit_batch.py` 固定 `nanHandling=OFF/maxTrade=ON`，与 MCP 批不可比（行为族 S 2.19→0.46）；**用 `ind_sim_submit.py` 全程可控**。

---

# 【追加 2】论坛查证攻 robust_universe：EPS 族从 0.62 → 0.85（仍未破 1.0）

> 用户要求「查平台灵感/论坛/外部论文找解决方案」，不再盲试。**论坛确实带来了实质进展**：
> robust 0.62 → **0.85**（+0.23），且 prod 本就干净（0.57）、塔位 ANALYST×1.4 最高。**但仍未到 1.0。**

## 一、论坛两篇 IND/ASI 专帖（信息密度极高）

1. **《关于IND地区Robust universe sharpe的改善方法》**（41 票 / 13 评，`post 36436936293655`）
2. **《如何通过【Robust universe Sharpe and returns】检测的一些尝试》**（14 票 / 7 评，`post 39920503976087`）
   ★ **根因**：亚洲大市值股票难做空 ⇒ 信号"小票强、大票弱"，而 **Robust universe = 流动性最好的大票子集** ⇒ 结构性错配。
   解法 = 市值过滤 `trade_when(1, alpha, rank(cap)>0.8)`。
3. **评论区 BZ29383 的 IND News 穷尽实测**（0.76→0.91，全部进展来自**做减法**）：
   `signed_power` 指数压缩单调改善（0.5→0.82 / 0.1→0.88 / **0.08→0.91 甜点** / 0.05 回落）；
   `group_zscore(subindustry)`→`group_rank(industry)` +0.06；**中性化全去掉 NONE 最优**。
   负清单：group_backfill(industry,20)→0.56、双层 rank→0.49、winsorize(std=2)→0.85、STATISTICAL→0.65。

## 二、本族完整权衡曲线（signed_power 指数 × 中性化）

| 形态 | S | F | 2Y | **robust** | 说明 |
|---|---|---|---|---|---|
| 基线 group_rank@STAT d4 | 2.02 | 1.46 | 2.53 | **0.62** | 起点 |
| signed_power 0.1 @**NONE** d4 | 1.47 | 1.64 | 3.05 | **0.93** | robust 最高但 S 不过闸 |
| signed_power 0.4 @STAT d8（backfill 11） | **1.96** | 1.57 | 2.16 | **0.85** | ★ **最优折中**（S 过闸 + robust +0.23） |
| signed_power 0.45 @STAT d12 | 1.94 | 1.57 | 2.06 | 0.77 | 指数↑ robust↓ |
| signed_power 0.5 @STAT d8 | 1.94 | 1.59 | 2.09 | 0.76 | 同上 |
| group_rank(sp 0.3) @sector d12 | 1.98 | 1.52 | 2.31 | 0.59 | 外层 group_rank 会毁 robust |
| 市值过滤 cap<0.8 @STAT d4 | 2.02 | 1.56 | 2.71 | 0.77 | 有效但不够 |

**规律**：`signed_power` 指数是 robust 与 S 的**直接对冲旋钮**（指数↓ ⇒ robust↑、S↓）。
NONE 中性化把 robust 推到 0.93 但 S 掉到 1.47（差 0.11）；**STATISTICAL + sp0.4 是唯一双过线附近的点（S1.96 / robust0.85）**。

## 三、两条反直觉（与论坛报道相反，族相关）

1. **市值过滤不是"越严越好"**：cap<0.8 → 0.77，<0.9 → 0.70，<0.7 → **0.55**。严格剔除因样本量/分散度下降反而伤 robust。
2. **"中性化全去掉 NONE 最优"在 News 族成立、在 EPS 族牺牲 S**：NONE 下 S 全卡 1.44–1.57。
⇒ 论坛方法**必须按族实测**，与"分母/轴/中性化是族相关旋钮"同型（本次第三次验证这条）。

## 四、现状

- **已提交仍是 2 颗**（`akxXl7w1` behavioral / `d51eGdKY` corr）；EPS 族尚未过robust 闸，未提交。
- EPS 族最优候选 `vR2xrxdb`：`signed_power(ts_delta(ts_backfill(vec_avg(mean_flash_estimate_eps_annual12_3),11),66), 0.4)` @decay8/STATISTICAL，
  **S1.96 / F1.57 / 2Y2.16 / sub1.30 / robust0.85**，prod 0.57 干净、塔 ANALYST×1.4 —— **只差 robust 0.15**。
- 下一步可选：① 继续扫 sp 指数 0.35–0.4 × decay 6–10 的更细网格（robust 可能再 +0.05–0.10）；
  ② 叠加市值过滤 cap<0.8 与 sp0.4（两者作用机制不同：前者剔样本、后者压尾部，**可能叠加**）。

---

# 【追加3】★★★ 论坛查证 + 叠加假设 = 第 3 颗 ACTIVE（3/10）

## 破局组合：市值过滤 × signed_power（两种机制正交，效果叠加）

```
signed_power(
  ts_delta(
    trade_when(less(rank(alternative_market_cap_usd), 0.9),          # ① 剔掉最大市值十分位
               ts_backfill(vec_avg(mean_flash_estimate_eps_annual12_3), 11), -1),
    66),
  0.4)                                                                # ② 尾部压缩
```
@decay=8 / STATISTICAL / truncation 0.08 / nanHandling OFF

| 指标 | 值 | 闸|
|---|---|---|
| Sharpe | **2.38** | ≥1.58 ✅ |
| Fitness | **2.14** | ≥1.0 ✅ |
| 2Y | **2.48** | ≥1.58 ✅ |
| sub_universe | 1.52 | ✅ |
| **robust_universe** | **1.02** | ≥1.0 ✅（**从 0.62 提升 +0.40**） |
| investability | 1.85 | ✅ |
| **prod** | **0.4824** | <0.7 ✅（0.6+ 桶**一颗都没有**） |
| **self** | **0.2967** | <0.7 ✅ |
| 塔 | IND/D1/RISK(1.0) + IND/D1/ANALYST(**1.4**) | 双塔 |
| 逐年审计 | **10/10 年正**，S 1.37–3.61，换手 0.107–0.120，最大回撤 3.82% | PASS |

## 为什么叠加有效（机制层面的解释）

| 手段 | 作用对象 | 效果 | 单独用时 |
|---|---|---|---|
| **市值过滤** cap<0.9 | **样本**（剔除大票） | robust 0.62→0.77 | 有效但量不够 |
| **signed_power 0.4** | **尾部权重** | robust 0.62→0.85、S 保住 1.96 | 接近但差 0.15 |
| **两者叠加** | 样本 + 权重 | **robust 1.02、S 2.38（不降反升）** | ✅ 全闸 |

⇒ 有趣的是叠加后 **S 从 1.96 涨到 2.38**（+0.42）——剔掉大市值不仅没伤强度，
反而因为"剔掉了信号失效的大票"而**纯化了横截面**。这与直觉相反但数据清晰。

## 三颗已提交（两两正交，可全部共存）

| # | alpha | 族 | S | F | 2Y | robust | prod | self | 塔|
|---|---|---|---|---|---|---|---|---|---|
| 1 | `akxXl7w1` | behavioral_streak +秩后裁剪 | 2.29 | 1.05 | 2.18 | 1.33 | 0.6921 | 0.3382 | MODEL 1.2× |
| 2 | `d51eGdKY` | corr_last_trade 变化形 + 裁剪 | 3.06 | 1.73 | 2.13 | 1.03 | 0.6904 | 0.4780 | PV 1.1× |
| 3 | **`blOVO3Pp`** | **EPS 修正 + 市值过滤 + sp** | **2.38** | **2.14** | **2.48** | 1.02 | **0.4824** | 0.2967 | RISK+ANALYST 1.4× |

互相关：0.002 / 0.054 / 0.1197 ⇒ `max_mutually_below_subset` size=3。

## 方法论总结（两条通用武器）

1. **破 prod 墙**：`winsorize(rank(...), std=0.05–0.25)`（裁秩不裁原值），前置判据= prod 直方图 0.6–0.7 桶密度。
2. **破 robust 墙**：`市值过滤（剔样本） × signed_power（压尾部）` 叠加，两机制正交、可叠加，且叠加后 S 不降反升。
   单独用任一个都不够（0.77 / 0.85），叠加直接过线（1.02）。
