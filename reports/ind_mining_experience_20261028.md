# IND alpha 挖掘会话经验总结

- 快照日：2026-10-28（Asia/Shanghai）。**本文是人工复盘（`reports/`），不是 SOP**；长期规范见 `docs/experience/` 与对应 skill。
- 范围：IND / EQUITY / TOP500 / DELAY 1 / REGULAR alpha，2026-10 月战役（含 20 颗交付池）。
- 全部数字为平台实测；标注「推断」的段落是解释，不是读数。

## 0. 一句话结论

IND 的难点不是「找不到信号」，而是 **`LOW_ROBUST_UNIVERSE_SHARPE`（rob ≥ 1.0）是几何问题**：
能过闸的几何（扣掉市场共同因子）在结构上一定把 `returns` 带进表达式，因此**永远不是 ATOM**；
能出 ATOM 的纯字段几何在 IND 小盘子宇宙上系统性偏弱。二者是同一个约束的两端。

## 1. 十条可复用结论

| # | 结论 | 证据 |
|---|---|---|
| 1 | **几何 > 字段**。同一字段换几何，Sharpe 可差 3 个点 | 实验 H：institutions 广度纯字段 `rank(F)` S −0.53 → 残差几何 S 2.56 |
| 2 | **残差几何（Form E）是本区最稳的过闸几何** | 10/10 臂 `failed_ra_count=0`，rob 1.01–2.02 |
| 3 | **残差几何必非 ATOM** | `returns` 作 `ts_regression` 因变量 ⇒ `pyramids.effective=2`（10/10） |
| 4 | **纯字段几何不可泛化** | Form D 在 `58jPrvZ1` S3.35；原样换两个字段 → S 1.01 / 0.32 |
| 5 | **ATOM–强度是同一约束两端** | 20 颗里 3 颗 ATOM（S 1.64/2.76/3.35），16 颗非 ATOM 的 S 集中在 1.94–3.20 |
| 6 | **分布「形状」比「水平」robust** | rob 均值：分布矩 1.86 > 水平 1.55 > 单一分歧量 1.01 |
| 7 | **换手由字段决定，decay 不是压换手杠杆** | 同字段 decay 126→252：TO 0.222→0.223，S −0.51、rob −0.72 |
| 8 | **`target_tvr` 要留 0.05 下偏余量** | 目标 0.40 实测 0.4116 / 0.4880，双双触发 HIGH_TURNOVER |
| 9 | **「零 fail」≠「过闸」** | `88R9LdZm` `checks.fail=[]`，但 3 项硬失败写在 `checks.warning` |
| 10 | **同族字段的残差时序高度同构** | `est_ptp` 族三臂两两 0.93/0.94 ⇒ 同族只容一颗 |

## 2. ATOM 的结构性边界（四条反证）

定义：`pyramids.effective == 1` = 单数据集归属。判据是平台返回的归属，不是表达式「看起来用了几个字段」。

| 反证 | 设计 | 实测 |
|---|---|---|
| D0 | Form E 9 颗 | 全部 `effective=2`（`returns` 计入 PV 归属） |
| E | Form D 原样换字段 | `anl4_ptp_high` S1.01 / institutions 均价差 S0.32，全闸多项失败 |
| G | 最朴素 `rank(F)` 纯字段 | 四类字段全灭：分析师点估计 S1.01、机构买卖均价差 S0.32、机构买卖广度 S−0.53、EPS surprise 0 持仓 |
| H | 同字段、同 backfill、同中性化，只差几何 | 纯字段 S−0.53（`effective=1`）vs 残差 S2.56（`effective=2`） |

**唯一同时给 ATOM 与强度的字段族是 `risk68_residual_return`**（它本身就是残差收益）。
该族已占 2 颗、族内互相关 0.6616，第 3 颗必然越线 ⇒ **ATOM 在 IND 的可挖上限已被实测钉死**（20 颗里 3 颗 = 15%）。

## 3. IND 的闸值与真瓶颈

| 闸 | IND 线 | 备注 |
|---|---|---|
| LOW_SHARPE | 1.58 | |
| LOW_FITNESS | 1.0 | |
| LOW_2Y_SHARPE | 1.58 | 弱年聚集在 2015 / 2021 |
| LOW_SUB_UNIVERSE_SHARPE | 1.0 | |
| **LOW_ROBUST_UNIVERSE_SHARPE** | **1.0** | **真瓶颈**，绝大多数「近闸」卡在这里 |
| HIGH_TURNOVER | 0.40（硬线） | 平台实测换手系统性高于 target |
| SELF / PROD 相关性 | < 0.70 | prod 单并发槽，常被并行会话占满 |

**读闸口径**：只有 `ra.failed_ra_count == 0` 才算过闸。`checks.fail` 可能是空数组而硬失败落在
`checks.warning`（`88R9LdZm`：LOW_SHARPE 1.15 / LOW_FITNESS 0.73 / IS_LADDER_SHARPE 三项全在 warning 里）。

## 4. 几何库（按实测过闸率排序）

1. **Form E（本区主力）**
   `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(F, 252), 252, rettype=0))`
   设置：`decay 126 / STATISTICAL / truncation 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling OFF / maxTrade OFF / 2014-01-01→2023-12-31 / FULL`
   实测：10/10 过闸，S 1.94–3.02，rob 1.01–2.02。
2. **Form D（单点成功，不可泛化）**
   `signed_power(subtract(group_rank(divide(subtract(ts_backfill(F,22), ts_mean(ts_backfill(F,22),252)), add(abs(ts_mean(ts_backfill(F,22),252)),1)), sector), 0.5), 3)`
   只在 `58jPrvZ1`（flash EBT 年度估计离散度）成功。
3. **`rg_grdev`（已判死）**
   `signed_power(subtract(group_rank(dev(F,252), sector), 0.5), 3)`，4 臂 rob 0.89/0.57/0.22/0.35，全灭。
4. **Form A / B（首 10 颗用）**：残差 → `ts_target_tvr_hump` / `ts_decay_linear` 平滑，`decay 6 / INDUSTRY`。

## 5. 事件 / 稀疏字段的处理规则

- **`ts_backfill` 窗口必须 > 事件间隔**：季度事件 ⇒ ≥ 252。反例 `MPYRxon9`（`eps_change_percentage_value`，
  季度事件、平均间隔 ~63 交易日）用 `ts_backfill(...,60)` ⇒ 序列带空隙 ⇒ 秩化后几乎无持仓（S 0.0 / TO 0.0）。
- **VECTOR 字段必须先 `vec_*` 聚合**再进时序算子。
- **`earnings6` 在 IND 判死**：VECTOR 经 `vec_avg` 后 2/2 臂 zero-trade，把 `ts_backfill` 拉到 252 仍是 0 持仓
  ⇒ 根因不是回填窗口，是该数据集在本区结构性不可用。
- 事件型字段的换手天然偏低，容易撞 `LOW_TURNOVER`（0.01），要靠 `ts_delta` / `ts_zscore` 提频。

## 6. 并发与派发纪律

- **并发上限 = 2**（账号级，唯一来源 `wqb.config`）。`multisim` 每条表达式各占一槽 ⇒ **每批最多 2 条表达式**。
- 一条语法错会连坐整批（`CANCELLED`）。发批前必须过 `preflight_expressions`（字段存在性 + VECTOR 自动修复）。
- 断点续跑去重键**必须含全部设置档**，否则同表达式不同 decay 会被误判为已跑。
- 收割必须同时传 `multisimulation_id` 与 `multisimulation_location`。
- `batch_status` 只接收 simulation / multisim ID，**不接受 alpha id**。

## 7. 相关性取数纪律（prod / self）

- prod 只能用 MCP `check_correlation(correlation_type=production)`，**禁止临时 requests 脚本**。
- 三态处置：有值 → 判闸；`correlation_busy` → 按顶层 `retry_after` 退避重试；`pending` →
  请求已被接受但 ~120s 轮询窗口内无值，过几分钟重试。
- **`last_known` 是陈旧值，判闸不得使用**。本轮实测 `age_hours≈276–280`、`stale=true`，
  与实时值可能差 0.4（历史教训 `j2eo0oMO`）。
- **self 与本地互相关不占平台槽**：`check_self_correlation` / `compute_mutual_correlation` 本地计算，可先用来筛。
- 本轮 prod 连续 6 轮 `correlation_busy`：单并发槽被并行会话长期占用。退避轨迹
  `retry_after` 114.1 → 180 → 50.3 → 98.5 → 62.0 s；两次在抢槽窗口返回 `-32603`（调用超时）。
  处置：不跳测、不用旧值，等槽空出后按序补测。

## 8. 互相关与族内饱和

- **20 颗池 190 对全部 < 0.70**，最大对 0.6699（`E5VNe67L ↔ KPmvEYeE`）。
- **同几何换字段的边际收益在第 9 颗后趋零**：残差几何把 `returns` 这个共同因子留在分母里，
  同族字段的残差时序高度同构（池内 9 颗两两 0.42–0.63）。
- 同族硬冲突实例：`Vkx9RbJV ↔ leAqNPX7 0.8425`、`ZYQ5J7j1 ↔ 88RowlOW 0.8581`、
  `est_ptp` 族 `78Lbx868/LLManLZ1 ↔ omowNkL2 0.9301/0.9406`、`1YjrRqeW ↔ 58jPrvZ1 0.9884`。
  ⇒ **同族只容一颗**；扩池要靠换族，不是换字段。

## 9. 逐数据集判死清单（IND / D1 / TOP500）

| 数据集 | 结论 | 依据 |
|---|---|---|
| `earnings6` | 判死 | VECTOR `vec_avg` 后 2/2 臂 zero-trade（`bookSize=0`） |
| `earnings11` | 判弱不判死（ATOM 可达、强度低） | 35 字段中已用 6：4 颗 ATOM 的 \|S\| 全 ≤0.43（`ern11_document_sentiment` 0.43 最好），同一字段进 Form E 能到 1.15 ⇒ 情绪类单字段 rank 在 IND 上限很低 |
| `news_sentiment_transfer` | 判死 | 两批 16 臂全灭 |
| `option1` | 判弱不判死（ATOM 可达） | 本轮塔内共 10 颗（option1 8 + option30 2）：ATOM 6 颗但 S 上限 0.44，Form E 最好 1.03；**覆盖率不是约束**——换到 cov 0.5177 的 `opt1_price_high/low` 后 S 仍 −0.29、换手反破 0.40 |
| `option30` | 唯一 ALIVE 臂 S1.29 / F0.62，四闸齐挂 | |
| `sentiment26` | 18 字段全 DEAD/UNUSABLE | |
| `macro63` | 单字段 `mcr63_membership`，binary membership | 强结果全部靠 `add(PV残差, membership)`，违反禁混信号 |
| `insiders5` | 唯一字段 `insd5_nm_kor` 是韩文人名 VECTOR | |
| `shortinterest5` | 3 字段实为涨跌停比率 / 可交易状态 | 历史最佳 S 0.22 |
| `imbalance5` | 实际只有 2 字段（`imb5_score` / `imb5_mktcap`） | `imb5_score` alphaCount 14186，高度饱和 |
| `risk68` | 强（`rsk68_residual_return` 是唯一 ATOM+强度双全字段） | 族内互相关 0.6616，第 3 颗越线 |
| `risk70` | 35 字段，22 个 sector_exposure 是慢变量（换手风险） | |
| `risk71` | 3 条 ra=0 但与既有 risk 族互相关 >0.7 | 不可交付 |
| `institutions6` | 11 字段，本轮已出 10 颗（含 2 ATOM） | ATOM 形态可达但弱：`qMLoZ332` S 0.72、`GrWpvxxx` S −0.03；4 颗 ra=0 的高分件（S 2.9–3.0）全是 Form E、eff=2；族内 self 最紧 0.6648 |

## 10. 下一阶段资源盘点（未点亮塔）

| 塔 | 当前 | 可用字段 | 判断 |
|---|---|---|---|
| RISK | 1/3（池内 2 颗） | risk68 5 / risk70 35 / risk88 1 | 已达 11 行；字段最丰富 |
| INSTITUTIONS | 1/3（池内 6 颗） | institutions6 11（cov≈0.99） | 已达 10 行（2 ATOM），注意族内互相关 |
| SENTIMENT | 0/3（池内 1 颗） | sentiment21 105 + **sentiment23 105（从未挖）** | 已达 10 行（2 ATOM）；分布矩字段仍未挖 |
| IMBALANCE | 0/3（池内 1 颗） | imbalance5 **仅 2 字段** | 结构性 ≤3，需证据化上限 |
| EARNINGS | 1/3 | earnings3 8（date）/ earnings11 35（RavenPack VECTOR）/ earnings6 判死 | 已达 12 行；ern11 是主战场但单字段 S≤0.45 |
| MACRO | 2/3 | macro63 **仅 1 字段**（binary） | 结构性 ≤2，需证据化上限 |
| OPTION | 0/3 | option1 28 / option30 12（cov 0.34–0.52） | 已达 10 行；判断正确（期望低：ATOM 上限 0.44） |
| **INSIDERS** | 0/3 | **insiders1 9 字段（cov 0.3877，alphaCount 206–410）** | 已达 10 行；新资源、低拥挤，但无买卖方向字段，0.3877 覆盖易 zero-trade |
| SHORTINTEREST | 0/3 | shortinterest5 **3 字段**（涨跌停比率/可交易状态） | 结构性 ≤4，需证据化上限 |

**本轮覆盖结果（2026-10-28，`unlit28` + `unlit28b` 共 67 行，详见 `output_report/ind_unlit_tower_expansion_20261028.md`）**：

| 塔 | 已挖 | ATOM | 达标（≥10） |
|---|---|---|---|
| EARNINGS | 12 | 6（4 有效） | ✅（有效 10；另 2 颗 earnings6 空转） |
| RISK | 11 | 0 | ✅ |
| INSIDERS | 10 | 0 | ✅（最强 `88R90qk7` 仅差 2Y 0.14） |
| INSTITUTIONS | 10 | 2 | ✅ |
| SENTIMENT | 10 | 2 | ✅ |
| OPTION | 10 | 6 | ✅ |
| IMBALANCE | 2 | 1 | ❌ 字段级上限 |
| SHORTINTEREST | 1 | 0 | ❌ 字段级上限 |
| MACRO | 1 | 0 | ❌ 字段级上限 |

三条结构性上限已证据化（`get_datasets` / `get_datafields` 实测）：MACRO 仅 1 字段、SHORTINTEREST 仅 3 字段（涨跌停比率 + 交易状态）、IMBALANCE 仅 2 字段（`imb5_mktcap` 等同 PV 市值）。**「每塔 10 颗」对本区这三塔物理不可达**，应改写目标为「可用字段穷尽」。

**当季目录复核（2026-10-28，收尾时再取一次）**：`get_datasets(region="IND", delay=1, universe="TOP500")` 返回 64 个数据集，`category=macro` / `shortinterest` / `imbalance` **各只有 1 个数据集**（字段 1 / 3 / 2），没有任何未探索的替代来源；同一时点 `get_pyramid_alphas({})` 的 IND/D1 塔位 `option/sentiment/shortinterest/insiders/imbalance` 仍为 0、`macro` 2 / `earnings` 1 / `risk` 3 / `institutions` 1 未满。⇒ 三条上限是**平台目录事实**，不是本轮挖掘深度不足。

## 11. 方法论层面（下次别再走弯路）

1. **先判「几何」再判「字段」**。同一批失败臂先看是不是几何性问题（rob 全低 = 几何问题，不是参数运气）。
2. **判死要用分母**。说「这个族扫完了」之前必须盘点：字段全集、几何全集、设置档全集。
3. **不要用 `checks.fail=[]` 当结论**，也不要用陈旧 `last_known` 当 prod 判据。
4. **不混信号、不靠权重调参**：`add(A,B)` 两个信号相加在 IND 上既过不了 rob，也过不了 prod。
5. **塔位口径以 `get_pyramid_alphas()` 当季为准**，且「已有候选」不等于「已点亮」——点亮要求 3 颗。
6. **ATOM 不是挑出来的，是几何决定的**。要 ATOM 就只能在纯字段几何里找，接受强度损失。
