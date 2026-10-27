# USA INSIDERS 字段画像（insider_agg_matrix / insider_trx_matrix）

- **as_of** 2026-10-22（平台 `get_datafields` 实测，USA / DELAY 1 / TOP3000）
- **区域 / 设置基线**：USA · TOP3000 · D1 · SUBINDUSTRY · decay 5 · truncation 0.08 · nanHandling ON
- **用途**：objective 步 2 的字段画像存档；本文件同时记录 INSIDERS 类别的判死依据与论坛可复用结论
- **结论先行**：`insider_agg_matrix` 的 value 族在美国**结构性不可用**（3 臂峰值 S 0.92）；
  `insider_trx_matrix` 只剩 **recipe-2（secondary）计数族**是低拥挤正交空间，其命运由
  `LOW_SUB_UNIVERSE_SHARPE` 决定（见 §7）

## 1. 为什么从 analyst 切到 INSIDERS

| 理由 | 证据 |
|---|---|
| analyst 族已被 prod 墙全覆盖 | `pw5RbrYX` 0.9000 / `leKKGb9l` 0.9014 / `58gp1wdz` 0.9868 / `Vk6QLx3Y` 0.8262 / `wpZJPRql` 0.7429；对照 `e76xgXkM` 0.5532 证明探针本身有效 |
| INSIDERS 塔未点亮 | 美国本季点亮塔 = analyst 6 / model 4 / earnings 1，INSIDERS 不在其中 ⇒ 可回测 |
| 已交付 5 颗全部是 analyst 修正类概念 | `omoK1A5m`/`akVnvzX5`/`gJWoaJqv`/`kqJLawqP`/`e76xgXkM` 全是 EPS/营收预期修正族 ⇒ 内部人交易与之**机制正交**，prod 冲突风险低 |
| 论坛给出已验证的存活骨架 | post 43152032301591：`ts_zscore(ts_sum(field, W), 252)`，zscore ≫ rank，跨字段比值/价差全死 |

## 2. `insider_agg_matrix`（dataset id 379，INSIDERS，delay 1）

数据集级：coverage 0.7672 · alphaCount **8** · tier PPA_PASS · value_score 4 · 17 个字段全 MATRIX。

| 字段 | aC | uC | 语义 | 判读 |
|---|---|---|---|---|
| `significant_value_1/2/3/4` | 5 / 3 / 3 / 0 | — | 显著交易金额（买/卖 × 均值/合计） | **金额族 = 规模污染** |
| `directional_significant_value_1/2/3/4` | 2 / 2 / 0 / 1 | — | 同上但带方向符号 | 同上 |
| `top_significant_value_1/2/3/4` | 0 / 0 / 1 / 5 | — | 高管（高置信）显著交易金额 | 同上 |
| `top_directional_significant_value_1/2/3/4` | 6 / 2 / 0 / 0 | — | 高管 + 方向 | 同上 |
| `directional_indicator_2` | 6 | — | 聚合交易的净方向指标 | 唯一非金额腿，尚未跑出信号 |

字段级 coverage 全为 0.7716（同构，无覆盖差异可利用）。

### 2.1 Wave 50 实测（3 臂完成，2026-10-22）

| 臂 | 表达式骨架 | S | F | 2Y | TO | alpha |
|---|---|---|---|---|---|---|
| L1_lvl | `group_rank(backfill(directional_significant_value_1,66), subindustry)` | **0.92** | 0.50 | 0.55 | 4.93% | `WjLYPQXG` |
| T1_slow | `group_rank(ts_decay_linear(同字段, 66), subindustry)` | 0.74 | 0.32 | 0.64 | 3.06% | `6XAGrajL` |
| T2_top | `group_rank(ts_zscore(backfill(top_directional_significant_value_1,66),252), subindustry)` | **0.15** | 0.03 | 0.60 | 3.43% | `xA1lYQMb` |
| T3_agg | `group_rank(add(add(D1,D2),add(D3,D4)), subindustry)` | 在飞 | | | | — |

**归因（必须成立才判死）**：三条臂的换手（3–5%）与 2Y（0.55–0.64）都稳定，说明信号不是噪声，而是
**幅度本身没有横截面信息**。`*_significant_value_*` 是「金额 × 显著度」的强度量，大市值公司的内部人
交易天然绝对值更大 ⇒ 截面载荷落在市值/流动性而非信息上，SUBINDUSTRY 中性化后残余极小。
这与论坛两次独立证伪一致：

- 本仓：USD 金额族美国死两次（E5 −0.13、C7 0.13）
- GLB 姊妹集 `insider_agg_matrix` 全死（Δ测试 0.08 / 0.02 / 0.32）

**判定：`insider_agg_matrix` 价值族 = `dead_end`（结构性）**。峰值 S 0.92 距 1.58 闸差 0.66，
且同为金额族的四条腿互相关极高，继续换窗口/换算子只会在 0.7–0.9 区间打转。
剩余未跑腿 `directional_indicator_2`（净方向）机制上不属金额族，留待 §7 一并裁决。

## 3. `insider_trx_matrix`（29 字段，coverage 0.7642 / 0.7715）

字段分三层，**拥挤度极不对称**——只有 recipe-2 层是空的：

### 3.1 base recipe（OGE 基础聚合）—— 已被 9 月论坛批打满，现 2–3 倍拥挤

| 字段 | aC | uC | 语义 |
|---|---|---|---|
| `total_buy_transaction_count` | **399** | 142 | 全部买入事件强度合计 |
| `total_top_buy_transaction_count` | **211** | 100 | 高管买入合计 |
| `mean_buy_transaction_count` | 179 | 64 | 每事件均值 |
| `mean_top_buy_transaction_count` | 117 | 53 | 高管每事件均值 |
| `total_sell_transaction_count` | 80 | 39 | 全部卖出合计 |
| `total_top_sell_transaction_count` | 38 | 20 | 高管卖出合计 |
| `mean_secondary_sell_transaction_count` | 38 | 25 | （recipe 2，见 3.2） |
| `directional_indicator_score` | 19 | 9 | 聚合交易净方向得分 |

### 3.2 recipe-2（`secondary` = 备选聚合口径）—— **低拥挤正交空间**

| 字段 | aC | uC | 语义 |
|---|---|---|---|
| `mean_secondary_buy_transaction_count` | **63** | 34 | recipe 2 买入，每事件均值 |
| `mean_secondary_sell_transaction_count` | **38** | 25 | recipe 2 卖出，每事件均值 |
| `total_top_secondary_buy_transaction_count` | **32** | 21 | 高管 + recipe 2 买入合计 |
| `mean_top_secondary_sell_transaction_count` | **16** | 8 | 高管 + recipe 2 卖出均值 |
| `total_top_secondary_sell_transaction_count` | **11** | 5 | 高管 + recipe 2 卖出合计 |
| `total_secondary_sell_transaction_count` | **7** | 6 | recipe 2 卖出合计 —— **全表最低** |

⚠ 无 `total_secondary_buy_transaction_count`（合计口径只有 sell / top-buy / top-sell 三个）。
recipe-2 与 base recipe 是**同一批事件的不同聚合**，不是不同事件源 ⇒ 二者相关会高，
但 base recipe 已 399 个 α 用过，**新提交撞 prod 的概率主要来自 base 层**。

### 3.3 USD 金额族（10 字段，aC 1–17）—— 机制上同 `insider_agg_matrix` 金额族

`usd_{direct,primary,secondary,tertiary,quaternary}_signal_value` 与 `usd_top_*` 全族。
低 aC 只是没人用，不是有信号：买入/卖出各自只有 1–2 个 α 试过。**沿用 §2.1 的规模污染结论，不再投。**

## 4. 论坛可复用结论（三条，已改写为纪律）

1. **post 43273417454487（2026-09-05，17 赞）· 稀疏事件不能用 `ts_backfill`**：
   内部人交易 / 公告 / 新闻属**稀疏事件流**，`ts_backfill` 会把一次性事件向后铺几十天，
   造出僵尸持仓与假稳态。正确做法是 `to_nan(x, value=0, reverse=true)`（把 0 变 NaN，让 ts 算子跳过
   无事件日）+ **显式 decay** 吸收事件冲击。`ts_backfill` 只适用于慢变量（资产负债表、股本）。
   ⇒ 本条已用于 wave 51 的表达式构造。
2. **post 43152032301591（2026-09-01，43 赞）· 高管买入 vs 买压**：
   - 存活骨架 = `ts_zscore(ts_sum(field, W), 252)`；**zscore 必胜 rank**（rank 0.61 vs zscore 2.25，
     排序抹掉峰值幅度）
   - 窗口梯度 21 ≈ 42 > 63 > 126 > 252（短窗欠反应更强）
   - 跨字段比值/价差形态**全死**（0.22 / 0.03 / −0.13 / 0.01）⇒ 不要做 buy/sell 价差合成
   - USD 金额族死两次（−0.13 / 0.13）
   - 卖出异常值 −0.79，反号仍不过 ⇒ **买卖不对称，卖出侧不可镜像使用**
   - 最终三颗 `P07VmG5x` / `LL7QYG8n` / `e7zjZ31E`：S 3.06 / 2.89 / 2.63，prod 0.686 / 0.542 / 0.611
3. **post 43467688159511（2026-09-14，29 赞）· 内部人交易观察**：
   买入是纯信号，卖出夹杂流动性动机；**多高管集群买入最强**；相对金额（对薪酬/财富）> 绝对金额。
   ⇒ 解释了 §2.1 为何金额腿全部失败、以及为何应优先 `top_*`（高置信=高管）腿。

## 5. 平台硬约束（2026-10-22 实测，`get_platform_setting_options`）

USA/D1 合法 universe **只有** `TOP3000 / TOP2000 / TOP1000 / TOP500 / TOP200 / TOPSP500`。

> ⚠ **没有 `ILLIQUID_MINVOL1M`，也没有 `MINVOL1M`**（GLB 有 MINVOL1M/MINVOL10M，ASI 有 MINVOL1M/MINVOL10M，
> EUR 有 TOPCS1600；USA 都没有）。论坛作者靠切到 `ILLIQUID_MINVOL1M` 把子宇宙 Sharpe 抬到 2.14–2.28，
> **这条修复在美国不可复现**——若走 `/wq-brain-ra-usa` 流程，只能在 TOP3000 上硬扛子宇宙闸。

## 6. 拥挤度地图（决定「新提交撞不撞 prod」）

| 层 | aC 区间 | 判断 |
|---|---|---|
| base recipe 计数 | 80–399 | 已被 9 月批打满，新 α 与既有 prod 池高度重叠 |
| recipe-2（secondary） | **7–63** | 最空；但同事件不同聚合，与 base 层相关不低 |
| USD 金额 | 1–17 | 空，但机制已证死 |
| `insider_agg_matrix` 价值族 | 0–6 | 空，但机制已证死（§2.1） |

## 7. 裁决：recipe-2 计数族 × 子宇宙闸 —— **结构性判死**（2026-10-22 实测）

Wave 51（4 臂）就是为了回答**一个结构问题**，而不是为了碰运气：

> 在 TOP3000 + SUBINDUSTRY + decay 5 下，`ts_zscore(ts_sum(count, W), 252)` 的
> **SUB/S 比率**是多少？（原写法在外层套了 `to_nan`；该算子是已登记幽灵算子，且计数零值本就加性中性，故去掉）

- 若 SUB/S ≳ 0.5（S 2.0 时 SUB ≥ 1.0）⇒ recipe-2 族可继续，扩窗 / 换 top 腿 / 换中性化
- 若 SUB/S ≈ 0.3（论坛在 TOP3000 实测 0.71 sub @ S≈2.3）⇒ **USA 内部人计数族整体判死**，
  因为子宇宙闸要求 S ≥ 3.2，而论坛全平台最优也只有 3.06，且那条还用了美国没有的 ILLIQUID 宇宙

已跑过的其他探针见：`insider_matrix` 原始事件 10 臂（`_usa-atom-delivery-log-20261020.md` 附录 AJ，
因换手/CW 判死）、波 48/50、GLB 姊妹集三值全死。

### 7.1 实测结果（波 51b，4 臂已出 2 臂）

平台先否掉了论坛骨架的 `to_nan(x, value=0, reverse=true)` 包装
（`Attempted to use inaccessible or unknown operator "to_nan"`）——**平台只有 `is_nan` / `if_else`，没有 `to_nan`**。
对 `ts_sum` 而言零值本就只是加法中性，去掉包装语义不变，故实际骨架为
`ts_zscore(ts_sum(<count>, W), 252)`。

| 臂 | alpha | S | F | 2Y | TO | SUB | **SUB 限额** | **SUB/S** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `total_top_secondary_buy_transaction_count` W=21 | `9qEGm29x` | **2.67** | **2.79** | 3.19 | 19.0% | 0.69 | 1.16 | **0.26** |
| 同上 W=42 | `GrgQxKEJ` | 2.55 | 2.73 | 3.15 | 13.9% | 0.82 | 1.10 | **0.32** |

**关键平台口径更正**：`LOW_SUB_UNIVERSE_SHARPE` 的 `limit` **不是固定 0.97，而是 `0.43 × S`**
（S 2.67 → 1.16；S 2.55 → 1.10）。因此可提交的充要条件是 **SUB/S ≥ 0.43**，与 S 绝对值无关。

**裁决**：SUB/S = 0.26–0.32 < 0.43，且窗口加倍只把比率从 0.26 抬到 0.32（<0.43 仍不过）。
这与论坛在 TOP3000 测得的 insider 流约 0.31 完全一致，也与本仓 `insider_matrix`（0.43×S 全不过）同源。
⇒ **USA 内部人计数族（含 recipe-2）判死：不是信号弱，是覆盖只集中在少数有内部人交易的票上，
子宇宙一加权就打回原点。** 换窗 / 换中性化都不改这个比率（它们是同一批票的同一批事件）。

**可复用结论**
1. SUB 闸要按 **SUB/S ≥ 0.43** 判，不要背 0.97 这个绝对值——它会随 S 浮动。
2. **事件型稀疏信号（内部人交易、回购、评级变动）天然 SUB/S 低**：收益只存在于有事件的少数票。
   这类信号在 USA 无解，因为 USA/D1 没有 `ILLIQUID_MINVOL1M` 子宇宙可选（只有 TOP3000/2000/1000/500/200）。
3. `to_nan` 是论坛常用但平台上**不存在**的算子；`wqb.expression.op_arity.check_expression`
   当时对未知算子跳过（幽灵算子归 `operator_audit` 管），所以 arity 通过 ≠ 平台可用。
   **2026-10-23 起该闸已 fail-closed**：目录外算子直接报 `[UNKNOWN_OP]`、幽灵报 `[GHOST]`，
   发批前跑 `ensure_safe_for_dispatch` 即覆盖存在性；catalog 过期时先跑
   `tools/refresh_operator_catalog.py`（见 `docs/experience/04_engineering.md` §14.6）。

### 7.2 宇宙杠杆（波 51c）：**SUB/S 与 S 是同一枚硬币** —— 双边证据闭合

§7.1 留下的最后一个未测杠杆是「换小宇宙」：TOP3000 上 SUB 只覆盖大盘一侧，
若把宇宙收到 TOP1000/TOP500，子宇宙≈全场，SUB/S 理论上应趋近 1。实测（同一表达式
`ts_zscore(ts_sum(total_top_secondary_buy_transaction_count, 42), 252)`）：

| 宇宙 | alpha | S | F | 2Y | TO | SUB | **SUB/S** | CW | 失败项 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| TOP3000 | `GrgQxKEJ` | **2.55** | **2.73** | 3.15 | 13.9% | 0.82 | **0.32** | 过 | SUB |
| TOP1000 | `gJWrLbN0` | 0.54 | 0.34 | 0.61 | 11.6% | 0.50 | **0.93** | 0.50 | S/F/2Y/CW |
| TOP500 | — | 0.31 | 0.18 | **−0.60** | 10.1% | 0.30 | **0.97** | 0.50 | S/F/2Y/CW |

**读数**：宇宙一收窄，SUB/S 立刻从 0.32 跳到 0.93→0.97（假设完全成立），
**代价是信号本身归零**（S 2.55 → 0.54 → 0.31，2Y 转负）。

⇒ 这不是「构造没做好」，而是**该信号 100% 存在于小盘侧**：
- TOP3000 上信号强但 SUB（大盘子宇宙）无信号 → 若判可提交，等于**声称一个只在小盘有效的策略能在大盘上复制**，平台这一闸正是为此设的。
- 收窄到大盘后 SUB 合格，但**根本没有信号可交付**。

**双边证据闭合，本族判死不再有残余杠杆。** 这比 §7.1 的「比率不够」更强：
它是「**信号与子宇宙在空间上互斥**」，任何平滑/窗口/中性化/宇宙重排都不可能同时满足两侧。
USA/D1 也没有 `ILLIQUID_MINVOL1M` 这类「把小盘变成全场」的宇宙选项（只有 TOP3000/2000/1000/500/200）。

**顺带测掉的卖侧**（波 51b 另 2 臂，同一骨架、字段换成卖出计数）：
`mean_secondary_sell_transaction_count` S **−1.24** / `total_secondary_sell_transaction_count` S **−0.95**。
镜像取正后也只有 0.95–1.24 < 1.58 ⇒ **卖侧是买侧的弱镜像，没有独立信息**，不能当第二条交付线。

**最终裁决（2026-10-22）**：insider 计数族（`insider_trx_matrix` recipe-2 + `insider_matrix`/`insider_agg_matrix` 同源）
在 USA/D1/TOP3000 **结构性判死**，理由从「SUB/S 不够」升级为「**信号与可交付宇宙互斥 + 卖侧镜像不足**」。
不再开波、不再加变体；未来只有「非计数的全新 insider 机制」（如持仓变动速度、跨公司内部人网络）才允许重入。

## 8. 字段可用性总表（供后续波选择）

| 能不能用 | 字段 | 理由 |
|---|---|---|
| ✅ 唯一候选 | `total_top_secondary_buy_transaction_count` | 最低拥挤 × 高管 × 买入（三重利好）+ recipe-2 |
| ✅ 次选 | `mean_secondary_buy_transaction_count` | 样本更多（aC 63），均值口径抗单笔异常 |
| ⚠ 备选 | `total_secondary_sell_transaction_count` / `total_top_secondary_sell_transaction_count` | 全表最空，但卖出侧论坛证死（−0.79，反号不过） |
| ❌ 弃用 | 全部 `usd_*` | 规模污染，美国死两次 / GLB 死一次 |
| ❌ 弃用 | `insider_agg_matrix` 全部 `*_significant_value_*` | 同金额族；wave 50 峰值 S 0.92 |
| ⚠ 未测 | `directional_indicator_score` / `directional_indicator_2` | 非金额腿，机制独立，但 aC 19/6 已有人用 |
