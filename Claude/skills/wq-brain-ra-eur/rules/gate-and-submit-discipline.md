# EUR 闸门纪律（gate-and-submit-discipline）

> **as_of**：2026-11-12 ｜ 来源：RJ 系列波（risk/pv/earnings/institutions/socialmedia 五塔实测，约 152 臂）
> 本文只写**闸门层**的 EUR 实证规律；机制选型见 `../references/<category>.md`。

## 1. LOW_SUB_UNIVERSE_SHARPE 是「S 的比率闸」，不是独立闸

**实测（2026-11-12，两臂精确复现）**：

| alpha | S | SUB | 平台 limit | SUB/S |
|---|---:|---:|---:|---:|
| `Jj8EWEeA`（risk68 edadv） | 1.60 | 0.27 | 0.83 | **0.17** |
| `2r5zXz9N`（edadv + news46） | 1.87 | 0.53 | 0.97 | **0.28** |

⇒ `limit = 0.519 × S`。**必须 SUB/S ≥ 0.52**。
⇒ 提升 S 会同步抬门槛——这是**耦合闸**，不能靠单点提 S 过关。

**结构性推论（选字段的第一道筛）**：
流动性/规模代理型字段（成交额、事件流量计数）天然依赖小盘股 ⇒ SUB 比率只有 0.05–0.28 ⇒ **结构性不过闸，换骨架无效**。
反向成立的类型：持仓集中度（HHI，SUB/S 1.28）、残差反转（SUB/S 0.70–0.92）——这类在子宇宙内同样有区分度。

## 2. self 是比 prod 快得多的第一道筛（顺序纪律）

**正确顺序**：
```
IS 全闸 → check_self_correlation（本地） → compute_mutual_correlation（本地） → check_correlation(production) 终验
```

| 工具 | 成本 | 备注 |
|---|---|---|
| `check_self_correlation` | **零平台配额，秒级** | 走本地增量缓存 |
| `compute_mutual_correlation` | **零平台配额，秒级** | 本地 PnL 相关 |
| `check_correlation(production)` | 账号级**单并发槽**，2–5 分钟/颗 | 最稀缺，放最后 |

**实证收益（2026-11-12）**：靠 self 本地筛否决 6 颗（0.71 / 0.74 / 0.93 / 0.94 / 0.95 / 0.98），省掉 6 次 prod 白跑。

## 3. prod 熔断有累加机制：一次只测一颗

**实测**：连续 `pending` 超时会把账号级熔断冷却从 177s → 450s → 598s **累加**。
⇒ **必须一次只测一颗**，等结果落 `alpha_corr_cache` 再测下一颗。
⇒ `inflight=true` 时**不要重新触发**（重复触发只会把自己顶成 busy）。
⇒ 拿到任一成功结果即提前清除熔断。

## 4. prod 是「带符号最大值」

负 Sharpe 版本测出的低 prod 是假象（历史实证：`qM7M2b6P` 负向 0.4725 → 正向 0.7952）。
测 prod 前先确认 alpha 方向正确。

## 5. `checks.fail=[]` 不等于可交付

`fetch_metrics.py --brief` 的 `fails=[]` 只读 `checks.fail`，**不含 `checks.warning`**。
S/F/2Y/CLUSTER 在 warning 档同样阻断提交。必须用 `submit_verdict` 查完整 checks。

## 6. 交付篮子：互相关全对 <0.7 + 组腿配额

- 篮子成员互相关**严格不等**小于 0.7（`compute_mutual_correlation(threshold=0.7)` 取最大独立集）。
- 组腿约束：禁止 PV / MODEL / OTHER 内部及相互之间两两组腿；可与其它 category 组腿，**此类组合总计 ≤ 5 个**。
- 判定口径：一条表达式里出现 **≥2 个禁区类**（PV/MODEL/OTHER）即违规。
  - 实证通过：`VkxWmpYG`（OTHER+ANALYST+NEWS，仅 1 禁区类）、`N1P02YwL`（MODEL+RISK，仅 1）。
  - 实证剔除：`leAnKOEA` / `P0oR7vYw`（techindi OTHER × insider_matrix OTHER = 2 禁区类）。

## 7. ★ EUR 生产池饱和（2026-11-12 实证，选件第一约束）

**现象**：IS 层能过闸的件很多（本地库 365 颗满足 S≥1.58 / F≥1 / 2Y≥1.58 / SUB-S≥0.52 / TO 5–30% / margin≥5bp），
但 **prod 层大面积撞墙**：本轮实测 17 颗候选，11 颗 FAIL（0.71–0.89），仅 10 颗 REGULAR 通过。

**两条已被实证的失败规律**：

### 7.1 S 与 prod 正相关
| alpha | S | prod |
|---|---:|---:|
| KPJoJp21 | 4.19 | 0.7992 ❌ |
| omEWJz3l | 3.42 | 0.8069 ❌ |
| vR1EKMmQ | 3.81 | 0.7810 ❌ |
| QPvxRG7G | 3.22 | 0.8160 ❌ |
| RRE6j9E0 | 3.09 | 0.8600 ❌ |
| 58EJXapM | 2.03 | 0.7156 ❌ |
| mLaLllmK | 3.98 | 0.6579 ✅ |
| N1NGbddg | 1.69 | 0.6872 ✅ |
⇒ **高 S 件更容易撞池**（能在生产池拿高 S 的机制往往已被自己提交过），但**不是绝对**（mLaLllmK 3.98 反而 0.6579 通过）。
⇒ 选件顺序应「S 适中优先测」，不要把最好的 prod 配额花在高 S 件上。

### 7.2 同族产能被自身提交占满
| 族 | 剩余库存 | self 实测 | 结论 |
|---|---|---|---|
| analyst7 修订 | 5 颗低 prod 件（3qjeJGle/JjeL53gx/d5WEm1LY/QPv5Zrpp/78LKlOw1） | **0.846–0.967 全 FAIL** | 被 10 颗已提交件占位，产能耗尽 |
| fnd72 现金流 | 9 颗双确认件 | 内部互相关 **0.95–1.00** | 独立集只能取 1（已取 mL617YPx） |
| techindi probability | 大量 | prod 0.74–0.83 | 撞已提交的 mLaLllmK / 6XMmE0EL |
| insider_agg_matrix | leA5JeP7 (prod 0.6498) | — | 被判死族，未验 |

**⇒ 判据：选一个族之前，先查该族已提交件数量。已提交 ≥3 颗的族，剩余产能基本为零，不要再投入。**

### 7.3 可用杠杆与无效杠杆
| 杠杆 | 效果 | 证据 |
|---|---|---|
| 换中性化 MARKET→INDUSTRY | **−0.052**（0.7051→0.6529） | 6XMmE0EL |
| 缩 universe TOP2500→TOP1200 | 单独无效（0.7051→0.7041），与换中性化合用才见效 | 同上 |
| 换桶对 / 版本号 | **−0.19**（0.849→0.658） | 历史台账 |
| 加大 decay | **反向 +0.40**（0.54→0.945） | 禁用 |
| ts_rank 窗口 / group 算子 / 分组轴 / truncation | ≤0.04 | 无效 |


## 8. ★ATOM 是交付的硬口径（2026-11-12 用户纠正「我希望你挖的是ATOM」）

**口径定义**：ATOM = 信号字段全部来自**单一数据集**。分组轴字段（如 `sta1_allc5` 属 pv29）不计入信号腿，但必须披露。

**实测教训（2026-11-12）**：交付 17 颗后用户指出要 ATOM，逐字段核对后发现**只有 5 颗是真 ATOM**，12 颗是跨数据集混腿。
偏差根源：补数量阶段把「能过闸」排在「是否 ATOM」之前，库存挖掘时见组合腿能过 prod 就直接收。

**纪律**：
1. ATOM 作为**硬条件**先筛，混腿件单独记账、不计入交付数。
2. 表达式定型后必须做**字段→数据集反查**（`fields` JOIN `datasets`）再声明 ATOM；字段名前缀相同不代表同集，
   例如 `buy_sell_ratio_all_250d_filled` 属 `insider_feats`（OTHER），不是 imbalance5。
3. **group_* 的第二参数 ≠ 信号腿**，但也需披露；若该轴来自禁区类（PV/MODEL/OTHER），不影响合规但要在交付文档写明。
4. 跨数据集件的合规判定：数**禁区类个数**（PV/MODEL/OTHER），≥2 才违规；1 个（如 OTHER+ANALYST）合规。

**已核实的易错映射（EUR）**：
| 字段 | 实际数据集 | 类别 |
|---|---|---|
| `sta1_allc5` | pv29 | PV（常作分组轴）|
| `buy_sell_ratio_all_250d_filled` | insider_feats | OTHER |
| `imb5_score` | imbalance5 | IMBALANCE |
| `revenue_revision_magnitude` / `eps_revision_magnitude` | analyst_factor_signals | ANALYST |
| `eur_director_signal_value_1` | insider_matrix | OTHER |
| `probability_*` | techindi_model | OTHER |
| `rsk68_beta` / `rsk60_offer` | risk68 / risk60 | RISK |
| `rsk70_mfm2_*` / `momentum_factor_exposure` | risk70 | RISK |
| `oth553_est_estvalue` | other553 | SENTIMENT |

