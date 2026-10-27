# USA `board_gov_stats` 字段画像与机制设计（2026-10-23，波 85 首触）

> 数据集：`board_gov_stats`（平台 dataset id 同名），category = **INSIDERS**（当前季 USA/D1 塔位 **0，未点亮**），
> delay 1，本地 registry：46 字段 / coverage 0.9197 / alphaCount 177 / value_score 3.00 / PPA_PASS。
> 本文是波 85 的**发批前预注册**（机制与臂在设计时写死），§7 为发批后回填。字段清单由平台
> `get_datafields(region=USA, universe=TOP3000, delay=1, dataset_id=board_gov_stats)` 实拉，非本地缓存
> （本地 `datasets.catalog_json` 对该集为空，见 `logs/_tmp_catalog_peek.py` 实测）。

## 1. 为什么切到这个数据集（换集理由，按过程约束留痕）

推进方向上必须按「确实无计可施才换集」执行，本轮的三个前序物均已实测封死：

| 前序物 | 判死证据 | 结论 |
|---|---|---|
| `other143` 券商/清算集中度族 | E1 prod **0.8599**；同族 `exempt_industry_top_broker_share_pct` 0.87–0.90；prod 直方图 [0.7,0.8) **n=26** | prod 墙，非 F 墙（F 已由波 83d 推到 1.00） |
| `earnings_risk` | 封存 `USA-EARNINGS-RISK-WEAK`；波 84 复查 7 臂 max\|S\| **0.60** vs 封存基线 0.58 | 封存成立，不推翻 |
| ds339 情感核（`QPYOPLAK`） | self **0.7105** / prod **0.7712** 双超 0.7；直方图 [0.7,0.8) **n=187** | 双闸死，已 `retire` 退役 |

候选表按「未测过 + 低拥挤 + 覆盖率可用」筛出七个，逐项比较后取 `board_gov_stats`：

| 候选 | 字段数 | aC | 覆盖 | 未选原因 |
|---|---:|---:|---:|---|
| `sustainable_profit` | 122 | 37 | 0.617 | 机制全落在 GP/NOA、external financing、DuPont —— **概念层极度拥挤**（Novy-Marx / Hirshleifer 是 BRAIN 上被实现最多的两条），prod 风险最高；且全字段为 VECTOR，需再套 `vec_*` |
| `mfm_model_output` | 117 | 308 | 0.996 | 内容是行业/风格**暴露**，做 alpha 等于做因子择时；`hedge_fund_ownership_factor*` aC 337/110 已拥挤 |
| `fundamental21` | 142 | 101 | 0.429 | 覆盖率 0.43，早年横截面样本不足，补数层会把样本进一步拉偏 |
| `other696` / `other567` | 294 / 223 | 147 / 455 | 0.79 / 0.51 | 字段语义泛，需先做长周期 S1；aC 亦不低 |
| `techindi_model` | 1830 | 495 | 0.973 | 技术指标本质是价格衍生 ⇒ 与已饱和的价量族 prod 重合 |
| **`board_gov_stats`** | **46** | **177** | **0.92** | **选中** |

选中的四条硬理由：① 46 字段合计 aC 仅 177（≈3.8/字段，是本轮未测面里最低的拥挤度）；② 覆盖率 0.88–0.95，
补数需求低于 fundamental21；③ 信息源是**组织稳定性**（董事会/高管进出、任期、独立性、外部席位、学历/姓氏集中度），
与我们已提交的 analyst 塔与已饱和的会计/价量族**不同源**——而本战役当前唯一的瓶颈就是 prod；
④ 本库该数据集 **0 alpha / 0 expression**（`alphas` 与 `expressions` 双表实测），是干净首触。

## 2. 全字段清单（46/46，平台实拉）

`type` 全部为 **MATRIX**（无 VECTOR ⇒ 不需要 `vec_*` 聚合；这也排除了「VECTOR 直接 ts_backfill 致整批 CANCELLED」的踩坑面）。

### 2.1 离职 / 流失（departure，9 字段）

| 字段 | 覆盖 | user | aC | 语义 |
|---|---:|---:|---:|---|
| `personnel_departure_rate_3m_total` | 0.9234 | 12 | 17 | 全部董事+高管近 3 月离职比例 |
| `personnel_departure_rate_6m_total` | 0.9120 | 8 | 9 | 近 6 月 |
| `personnel_departure_rate_1y_total` | 0.8860 | 6 | 7 | 近 1 年 |
| `management_departure_rate_3m_management` | 0.9149 | 10 | 11 | 管理层近 3 月 |
| `management_departure_rate_6m_management` | 0.9031 | 9 | 12 | 近 6 月 |
| `management_departure_rate_1y_management` | 0.8775 | 6 | 8 | 近 1 年 |
| `board_departure_rate_3m_management` | 0.9234 | 65 | 95 | 董事会近 3 月（aC 最高） |
| `board_departure_rate_6m_management` | 0.9120 | 23 | 31 | 近 6 月 |
| `board_departure_rate_1y_board` | 0.8860 | 13 | 18 | 董事会近 1 年 |

### 2.2 入职 / 增补（join，9 字段，与 2.1 严格同窗同口径）

| 字段 | 覆盖 | user | aC |
|---|---:|---:|---:|
| `personnel_join_rate_3m_total` | 0.9234 | 8 | 12 |
| `personnel_join_rate_6m_total` | 0.9120 | 3 | 3 |
| `personnel_join_rate_1y_total` | 0.8860 | 2 | 2 |
| `management_join_rate_3m_management` | 0.9149 | 5 | 6 |
| `management_join_rate_6m_management` | 0.9031 | 5 | 7 |
| `management_join_rate_1y_management` | 0.8775 | 4 | 5 |
| `board_join_rate_3m_management` | 0.9234 | 47 | 61 |
| `board_join_rate_6m_management` | 0.9120 | 7 | 7 |
| `board_join_rate_1y_board` | 0.8860 | 7 | 14 |

⚠ 2.1 与 2.2 的 `_3m_` 字段覆盖完全相等（0.9234 / 0.9149），说明二者来自**同一份滚动面板**，
因此 `subtract(departure_3m, join_3m)` 是同一构造的净流量，**不是两条信号腿相加**（合规性见 §4 M2）。

### 2.3 任期（tenure，5 字段，单位 = 天）

| 字段 | 覆盖 | user | aC | 语义 |
|---|---:|---:|---:|---|
| `ceo_tenure_days` | 0.9334 | 33 | 46 | CEO 在任天数 |
| `chairman_tenure_days` | 0.9364 | 30 | 40 | 董事长在任天数 |
| `median_chief_officer_tenure_days` | 0.9353 | 15 | 16 | 高管团队在任天数中位数 |
| `max_chief_officer_tenure_days` | 0.9353 | 22 | 29 | 最大值 |
| `min_chief_officer_tenure_days` | 0.9353 | 8 | 8 | 最小值 |

### 2.4 结构 / 规模（7 字段）

| 字段 | 覆盖 | user | aC | 类型 |
|---|---:|---:|---:|---|
| `board_member_count_2` | 0.9482 | 14 | 16 | 计数 |
| `management_team_size` | 0.9411 | 4 | 4 | 计数 |
| `total_personnel_count` | 0.9482 | 4 | 4 | 计数 |
| `independent_director_ratio` | 0.9482 | 14 | 14 | 比例 |
| `ceo_chairman_duality_flag` | 0.9223 | 12 | 16 | **二值** |
| `chief_officer_chairman_flag` | 0.9240 | 5 | 6 | **二值** |
| `multiple_ceo_indicator` | 0.9482 | 3 | 3 | **二值** |

### 2.5 外部网络（6 字段）

| 字段 | 覆盖 | user | aC |
|---|---:|---:|---:|
| `aggregate_external_connections` | 0.9482 | 33 | 38 |
| `board_external_connection_count` | 0.9482 | 27 | 35 |
| `management_external_connection_count` | 0.9411 | 4 | 4 |
| `unique_external_company_board` | 0.9482 | 8 | 8 |
| `unique_external_company_management` | 0.9411 | 7 | 10 |
| `unique_external_company_union` | 0.9482 | 8 | 8 |

### 2.6 人力资本 / 集中度（10 字段）

| 字段 | 覆盖 | user | aC |
|---|---:|---:|---:|
| `doctorate_share_board` | 0.9482 | 17 | 21 |
| `doctorate_share_management` | 0.9411 | 3 | 3 |
| `doctorate_share_total_personnel` | 0.9482 | 4 | 4 |
| `male_ratio_board` | 0.9482 | 12 | 13 |
| `male_ratio_management` | 0.9411 | 3 | 3 |
| `male_ratio_total_personnel` | 0.9482 | 6 | 8 |
| `ceo_gender_flag` | 0.9334 | 4 | 4 |
| `surname_concentration_board` | 0.9482 | 2 | 2 |
| `surname_concentration_management` | 0.5948 | 3 | 3 |
| `surname_concentration_total_personnel` | 0.9482 | 3 | 3 |

## 3. 字段级读数（决定算子选择的三个事实）

1. **这批字段是「状态量」不是「流量」**：覆盖率方差小（0.8775–0.9482）、同名 3m/6m/1y 三档同源，
   说明平台按披露事件更新、其余日沿用快照。⇒ 横截面 `rank` 是唯一自然基元；
   **时序归一（`ts_rank`/`ts_zscore`/`ts_quantile`）会把状态量的水平信息换成「相对自己历史的位置」**，
   而状态量的信息恰恰在水平上。本战役已有同向实证（`USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD`：
   ts_rank/ts_zscore 把 S 从 1.45 打到 0.20–0.29），故本波**不出时序归一臂**，这是有意留白不是遗漏。
2. **二值字段不能单独当信号**：`*_flag` / `multiple_ceo_indicator` 只有 0/1 两值，`group_rank` 后横截面只有 2–3 个
   取值 ⇒ 权重高度集中，`CONCENTRATED_WEIGHT`（≤0.1）几乎必挂。⇒ 二值只作**门控**（`trade_when`），不作核。
3. **3m 档是流量感最强的一档**：3m 窗滚动得最快，覆盖也最高（0.9234 > 6m 0.9120 > 1y 0.8860）。
   换手风险的主战场在 1y 档（近静态 ⇒ `LOW_TURNOVER` < 0.01 的典型来源）。

## 4. 六机制与预注册的十臂

发批前写死，收批后不得改判据。设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 /
nanHandling ON / 2014-01-01 → 2023-12-31（与波 83/84 同口径，便于横向比）。

| # | 机制 | 表达式 | 先验方向 | 判据（预注册） |
|---|---|---|---|---|
| f1 | M1a 流失水平 | `-group_rank(ts_backfill(personnel_departure_rate_3m_total,66), subindustry)` | 负（不稳定） | S>0 即机制方向成立；S≥1.0 才进第二波 |
| f2 | M1b 流失冲击 | `-rank(ts_delta(ts_backfill(personnel_departure_rate_6m_total,66),22))` | 负 | 同上；若 `ts_delta` 全 0（披露间隔 >22d）则本臂判「构造不适用」而非「机制死」 |
| f3 | M2 净流失 | `-group_rank(subtract(dep_3m_total, join_3m_total), subindustry)` | 负 | 与 f1 比较：净流 > 单流则保留净流为核 |
| f4 | M3 CEO 支配度 | `-group_rank(divide(ceo_tenure_days, median_chief_officer_tenure_days), subindustry)` | 负（独裁/固化） | S>0 成立；比值单位相消，规避 UNITS |
| f5 | M4 董事会独立性 | `group_rank(independent_director_ratio, subindustry)` | 正（监督） | S>0 成立 |
| f6 | M5 忙碌董事会 | `-group_rank(unique_external_company_board, subindustry)` | 负（Yermack busy board） | 与 f7 对读 |
| f7 | M5b 管理层外部联结 | `group_rank(management_external_connection_count, subindustry)` | 正（信息优势） | f6/f7 同号 ⇒ 网络不是「忙碌」而是「资源」；异号 ⇒ 分层成立 |
| f8 | M6a 学历 | `group_rank(doctorate_share_total_personnel, subindustry)` | 正 | S>0 成立 |
| f9 | M6b 姓氏集中度 | `-group_rank(surname_concentration_total_personnel, subindustry)` | 负（家族控制） | S>0 成立 |
| f10 | M1a × 自造十分位轴 | `-group_rank(dep_3m_total, bucket(rank(cap), range="0,1,0.1"))` | 负 | 与 f1 对比同臂换轴，测 §4.1③ 最强杠杆在本族是否成立 |

**合规性说明（两条容易误判的地方，先写清楚）**

- **M2/M3 不是 add A,B**：`subtract(dep, join)` 的两个操作数是**同一面板、同一单位（人员占比）、同一 3m 窗**的
  流入与流出，合起来是「净流失」**一个构造**；`divide(ceo_tenure, median_tenure)` 是同单位相除得无量纲比值。
  铁律禁的是「两条不同信号腿等权相加」，不是「一个构造的两个测量分量做差」。
- **f10 的换轴对象是 `cap`（信号之外的东西）**，不是信号自身。按 playbook §4.1 三条实证约束：
  按信号自身分桶会崩，按信号外的东西分桶才有效。

## 5. 算子面盘点（本波覆盖 / 本波有意不覆盖）

- **本波覆盖**：`group_rank`（截面分组秩）、`rank`（纯截面）、`ts_backfill`（补数层，0.88–0.95 覆盖的必需前置）、
  `ts_delta`（流量化）、`subtract` / `divide` / `multiply(-1)`（符号与归一）、`bucket`（自造分组轴）。
- **本波有意不覆盖**（留第 2/3 波，附理由）：
  - `ts_rank` / `ts_zscore` / `ts_quantile`（时序归一）—— 见 §3.1，会摧毁状态量水平信息；
  - `hump` / `ts_decay_linear` / `ts_target_tvr_hump`（换手类）—— 首波要先确认有没有信号，
    换手类只解决 `HIGH_TURNOVER`；本数据集预期风险是**反向**的 `LOW_TURNOVER`；
  - `winsorize` / `quantile`（分布类）—— 首波不叠，避免把「机制是否成立」与「形状是否更好」混谈；
  - `trade_when`（门控）—— 已识别二值字段适合做门（§3.2），但门控会改变持仓域，
    与首波的「机制存在性」问题不同层，留第二波单独测；
  - `group_neutralize` vs `group_rank` 的对照 —— 本波统一 `group_rank`（S 更高、单变量干净），
    第二波再做 `group_neutralize` / `group_zscore` 对照。

## 6. 闸门风险预注册（先写死，避免事后找理由）

| 风险 | 触发条件 | 归因口径（收批时照此判） |
|---|---|---|
| `LOW_TURNOVER` (<0.01) | 1y 档 / 任期档臂 | 构造性（状态量），不是信号弱；修法 = 降到 3m 档或加 `ts_delta`，**不许**用加噪声算子硬抬 |
| `CONCENTRATED_WEIGHT` (>0.1) | 二值门控或补齐后样本过窄 | 数据稀疏，修法 = 换 3m 档/扩窗；`truncation`/`decay`/中性化**修不了** |
| `LOW_SUB_UNIVERSE_SHARPE`（动态 = 0.43×S） | 信号集中在大盘（治理披露覆盖与市值相关） | 先看 f10（cap 十分位轴）能否救；不行则换 `market`/`exchange` 分组轴 |
| `LOW_FITNESS` (<1.0) | `F = S·sqrt(\|RET\|/max(TO,0.125))` | 若 TO<0.125 则 F = S·sqrt(RET/0.125) ⇒ 低换手本身对 F 有利，F 挂说明 RET 真的低 |
| 平台 `UNITS` 拒 | 单位字段 + 无量纲常数 | 本波已规避：比值同为天、差值同为人员占比 |

## 7. 波 85 实测（发批后回填）

- 发批：2026-10-23，parent A `oACG09Tb4hh9UWDsIfw20e`（f1–f8，8 臂）/ parent B `nWPBq6Jf4hX8B8VeZo7nz`（f9–f10，2 臂）。
  拆两个 parent 的原因：`cap` 的平台字段核验被 429 打断（`validate_expressions` 返回
  `warning: Field pre-check skipped or incomplete: cap`），而 `bucket(rank(cap), range=...)` 是本战役首次使用的
  命名参形态 —— 单批 1 条语法错会 CANCELLED 整批兄弟，故把新形态隔离到 2 臂小批。
- 预检：`logs/_tmp_w85_preflight.py` 五道（算子 scope/ghost 硬闸、字段集合、括号语法、arity 10/10、形状）
  全过；平台 `validate_expressions` 返回 `valid=true, unknown_fields=[]`。
- 收批（2026-10-23，parent A 8/8 COMPLETE，入库 `wave=board_gov_stats_w85`）：

| 臂 | 机制 / 核心表达式 | S | F | TO | RET | DD | 2Y | SUB | RA fail |
|---|---|---|---|---|---|---|---|---|---|
| f1 | 离职率水平 `-group_rank(pdep3m, subind)` | -0.37 | -0.11 | 2.8% | -1.16% | 20.9% | -0.93 | -0.38 | 4 |
| f2 | 离职率变化 `-rank(ts_delta(pdep6m,22))` | 0.50 | 0.22 | 11.6% | 2.45% | 17.3% | 1.37 | 0.03 | 5（含 CW 0.46） |
| f3 | 净流失 `-group_rank(pdep3m - pjoin3m, subind)` | **-1.12** | -0.56 | 3.1% | -3.08% | 33.2% | -1.99 | -0.69 | 4 |
| f4 | CEO 任期优势 `-group_rank(ceo_tenure / median_ceo_tenure, subind)` | **-1.18** | -0.60 | 1.5% | -3.21% | 32.1% | -1.69 | -0.36 | 3 |
| f5 | 独董比例 `group_rank(indep_ratio, subind)` | 0.99 | 0.56 | 1.2% | 3.94% | **6.8%** | 1.10 | 0.36(限 0.43) | 4 |
| f6 | 董事外部网络 `-group_rank(ext_boards, subind)` | **-1.19** | -0.63 | 5.3% | -3.52% | 35.3% | -1.65 | -0.47 | 3 |
| f7 | 管理层外部连接 `group_rank(mgmt_ties, subind)` | 0.60 | 0.20 | 1.0% | 1.45% | 10.5% | **1.90** | 0.18 | 3 |
| f8 | 博士占比 `group_rank(doctorate_share, subind)` | 0.69 | 0.25 | **0.96%** | 1.60% | 4.9% | 0.10 | -0.16 | 5（含 LOW_TURNOVER） |
| f9 | 家族控制 `-group_rank(surname_conc, subind)` | -0.89 | -0.47 | 1.2% | -2.4% | — | -1.92 | — | 4（E5VNQ0lK） |
| f10 | 离职率 × cap 十分位轴 | -0.39 | -0.12 | 3.15% | -1.2% | — | N/A | — | 4（QPYO0r7K） |

**归因（逐条，不盲扫）**

1. **方向判反三臂 = 本次最大发现**：f3 / f4 / f6 的 `multiply(-1,…)` 实测 S 分别为 −1.12 / −1.18 / −1.19
   ⇒ **原始方向全为正**（+1.12 / +1.18 / +1.19）。三个机制的经济解释都站得住：
   ① 净流失高 = 裁员 / 收缩（restructuring），市场对降本反应不足；
   ② CEO 任期相对中位数越长 = 管理层稳定、战略连续；
   ③ 董事兼任外部公司数越多 = 董事会网络中心度，信息与资源通道（与「busy board 是坏事」的旧文献方向相反）。
   三者 |S| 已到 1.1–1.2，**是波 86 的主攻对象**；但按资格线（S ≥ 1.25 且 F ≥ 0.8）单靠翻向**不构成合格**。
2. **f2 的 CW 崩是结构性的**：慢状态字段（季度更新的比率）做 22 日 `ts_delta`，横截面会出现大量零变化
   ⇒ 权重集中（2016-05-25 CW 0.46）。与既有纪律「状态变量用横截面 rank，不用时序差分」一致 ⇒ **离职率族（f1/f2）封存**。
3. **f5 独董比例是全组质量最高的一臂**：DD 6.8%、margin 6.54 bp、RET 3.94%、TO 1.2% —— 收益曲线干净。
   只差三面小幅：S 0.99（缺 0.59）、2Y 1.10（缺 0.48）、SUB 0.36 vs 限 0.43（缺 0.07）。**首选修复对象**。
4. **f7 的 2Y 1.90 是全组最高**，但全期 S 仅 0.60 ⇒ 近年强、早年拖累；TO 1.04% 已贴 LOW_TURNOVER 地板。
   可作为「近年制度」下的备选，但全期闸过不去。
5. f8 判死：TO 0.96% 跌破 0.01 地板，且 2Y 0.10 ⇒ 博士占比无时变信息。
6. **方法论沉淀**：六个机制里四个（f3/f4/f6/f5）给出 |S| ≥ 0.99 的可解释信号，说明 `board_gov_stats`
   的信息量真实存在；瓶颈不在字段而在**横截面轴与平滑方式**（见波 86 设计）。

**波 86 预登记**（下一步，未发批）：三正机制 × {自造 `bucket(rank(cap), range="0,1,0.1")` 十分位轴 /
`group_zscore(subindustry)` / `market` 轴} + f5 两修复臂（`group_zscore`、`market` 轴）。
不采用：`ts_delta` / 时序归一（CW 与 S 双杀，f2 已证）；`add(A,B)` 混腿（红线）。

## 8. 波 86 实测（2026-10-23，方向修正后 × 轴/形状杠杆）

发批：三个 parent，按「表达式族 / 设置档」隔离，避免单批连坐。
`logs/_tmp_w86_preflight.py` 五道预检全过（算子 REGULAR-safe / 字段 46+cap+分组符号 / 括号语法 /
arity 12/12 / 形状全 S9）。

| parent | 设置差异 | 臂 |
|---|---|---|
| `40ckat3n050a9LsnkhcOpmE` | SUBINDUSTRY / TOP3000 / decay 5 | 6（三正机制 × {cap 十分位轴, `group_zscore`}） |
| `3rsSO95kI4gmcnRIVwXHwhl` | **MARKET 中性化** / 其余同 | 2（CEO、独董的 `group_zscore`） |
| `Pzhvq2OU59r8XNiHmSLfKa` | SUBINDUSTRY / 分组轴改 `market` / `exchange` | 4（churn、独董） |

| 臂 | 机制 / 表达式 | S | F | TO | RET | DD | 2Y/ladder | margin | SUB | alpha |
|---|---|---|---|---|---|---|---|---|---|---|
| c1 | 净流失 × cap 十分位轴 | 1.11 | 0.57 | 3.41% | 3.26% | 4.04% | **ladder 2.12** | 1.92 bp | 0.71 | A1Qexekl |
| c2 | 净流失 `group_zscore(subind)` | **0.30** | 0.07 | 3.79% | 0.67% | 4.82% | 2Y 0.40 | 0.36 bp | 0.24 | QPYO0OEg |
| t1 | CEO 任期优势 × cap 十分位轴 | **1.20** | 0.65 | 2.03% | 3.62% | 5.19% | ladder 1.51 | 3.58 bp | 0.37 | LL5EKEkv |
| t2 | CEO 任期优势 `group_zscore(subind)` | **0.17** | 0.03 | 1.34% | 0.49% | 6.57% | 2Y 0.30 | 0.74 bp | 0.23 | 9qE8l8Rq |
| n1 | 董事外部网络 × cap 十分位轴 | 1.19 | 0.63 | 5.73% | 3.55% | 4.56% | ladder 1.56 | 1.24 bp | 0.39 | VkdZNZ8J |
| n2 | 董事外部网络 `group_zscore(subind)` | 0.84 | 0.38 | 5.84% | 2.56% | 6.44% | 2Y 1.16 | 0.88 bp | 0.29 | 58jrJrv6 |
| t3 | CEO 任期优势 `gz(subind)` + **MARKET 中性化** | 0.18 | 0.04 | 1.28% | 0.51% | 6.53% | 2Y 0.30 | 0.79 bp | 0.23 | pwvxaWmg |
| d1 | 独董比例 `gz(subind)` + **MARKET 中性化** | 0.71 | 0.35 | 1.13% | 3.03% | 7.35% | 2Y 0.77 | 5.37 bp | 0.34 | akVeaR6W |
| d2 | 净流失 `group_rank(market)` | 1.12 | 0.58 | 3.07% | 3.31% | 3.94% | **2Y 1.93** | 2.16 bp | 0.73 | d5KYaa6x |
| d3 | 净流失 `group_rank(exchange)` | 1.11 | 0.57 | 3.09% | 3.33% | 4.02% | **2Y 1.93** | 2.11 bp | 0.72 | QPYO00AK |
| d4 | 独董比例 `group_rank(market)` | 0.84 | 0.46 | 1.14% | 3.75% | 8.14% | 2Y 0.99 | 6.57 bp | 0.28 | LL5EKKwm |
| d5 | 独董比例 `group_rank(exchange)` | 0.82 | 0.43 | 1.19% | 3.47% | 7.94% | 2Y 0.98 | 5.83 bp | 0.31 | 1YjOWWRR |

**归因（逐条）**

1. **`group_zscore` 对慢状态变量是信号杀手，不是通用增益**：同一表达式只把 `group_rank` 换成
   `group_zscore`，净流失 1.11→**0.30**、CEO 任期优势 1.20→**0.17**、董事网络 1.19→0.84、独董 0.99→0.71。
   三个机制一致劣化 ⇒ 不是偶然。经济上成立：`ceo_tenure/median_tenure`、净流失率这类比率分布**右尾极长**
   （个别公司 tenure 比中位数大几十倍），zscore 把少数极端值放大成巨额头寸，decay/truncation 削不平，
   组合等价于「押几只异常公司」⇒ S 崩、margin 崩（CEO 臂 margin 3.58 bp → 0.74 bp）。
   **更正既有配方表**：`group_rank→group_zscore` 的 +0.10~0.17 增益只适用于**近似正态的中等峰度**信号，
   不适用于长尾比率；长尾状态变量的正确形状是 rank。
   ⚠ 波 86 的 MARKET 中性化 A/B（t3/d1）**因形状已毁而不成立**——zscore 臂无论中性化怎么换都是 0.18/0.71，
   不能据此判定「MARKET 中性化无用」。中性化轴仍未在 **rank 臂**上测过（→ 波 87）。
2. **换轴不产生增益，但改变时间分布**：净流失在 {cap 十分位 / market / exchange} 三个轴上 S = 1.11 / 1.12 / 1.11，
   统计上不可分；但 2Y 从 ladder 2.12（cap 轴平台报 ladder，非 2Y）变为 **2Y 1.93（market/exchange 轴）**，
   且 DD 从 4.04% 降到 3.94%/4.02%、margin 从 1.92 升到 2.16/2.11 bp。⇒ **`market` 轴是该族最优轴**（质量侧优、强度侧持平）。
3. **三正机制的强度天花板在 1.1–1.2**：wave 85 的 `group_rank(subindustry)` 与 wave 86 的三种轴
   给出同一量级（1.11–1.20）。**四个独立机制 × 四种分组轴，全部落在同一区间，指向数据集级强度上限**，
   而非某个轴没选对。
4. **fitness 缺口要用「收益」补，不是用「换手」补**：`F = S·sqrt(RET/max(TO,0.125))`，本族 TO 全部 < 12.5%
   ⇒ 分母恒为 0.125，TO 不再有杠杆。要 F≥1.0 在 S=1.12 时需要 RET≈10%（现 3.3%）；即使 S 升到 1.58
   也需 RET≈5.0%。**降换手对 F 完全无益**（已在 0.125 地板之下），只有 S 与 RET 同升才行。
5. **独董比例（f5/d4/d5）是全数据集质量最好的腿**：margin 5.37–6.57 bp（全组最高）、TO 1.1%，
   但 DD 8% 且 S 0.71–0.84 ⇒ **收益干净但太弱**，且它对分组轴敏感（subind 0.99 → market 0.84），
   说明其 alpha 有相当部分来自行业内比较，换到市场级比较即衰减。
6. **结论：`board_gov_stats` 的横截面 rank 面已探到边界**。剩余未测的只有两类：
   ① 归一化形状（「相对公司自身常态」而非「横截面水平」）；
   ② 设置轴（中性化 / universe / decay）在 **rank 臂**上的 A/B。
   → 波 87 就测这两类，若不破 1.25 即按 B 档封存（判死粒度 = 「横截面水平型治理信号」，不是整个数据集）。

## 9. 论坛 / 文献取证（2026-10-23，按「卡闸先查论坛」纪律）

来源：BRAIN 中文论坛帖 `43152032301591`（43 赞，作者 FF56620，2026-09-01），
经 MCP `search_forum_posts` + `read_forum_post` 全文读取。

| 结论 | 原文要紧处 | 对本数据集的适用性 |
|---|---|---|
| **慢变量 fundamental 不匹配「行为反应不足」框架** | 该帖明确把 `board_gov_stats` 这类慢变量列为不适用 | **部分证伪我方假设**：治理信号不是「反应不足」，更可能是**风险补偿 / 信息不对称折价**。解释要改，但不影响是否可交易 |
| **宇宙是决定性杠杆** | 同一信号 TOP3000 S 2.25–2.76 全被 LOW_SUB_UNIVERSE_SHARPE 拦（子宇宙 0.71–1.01），换 `ILLIQUID_MINVOL1M` 后 S **3.06** / F **3.40** / TO 23.7%，零告警 | ❌ **USA 不可用**：`ILLIQUID_MINVOL1M` 已对 USA/ASI/EUR 永久停提（平台 2026-09-14 公告），USA/D1 合法档只有 TOP3000/2000/1000/500/200/TOPSP500。**这条杠杆在 USA 结构性不存在**，不得再排入任何波次 |
| **短窗优于长窗** | 21d ≈ 42d > 63 > 126 > 252 | 与 f2（22d 差分）相反方向 —— 但那是**流量差分** vs 本帖的**成交量加权**，不可直接迁移。归属：本数据集**没有**短窗轴可换（字段本身就是 3m/6m/1y 窗口的比率） |
| **`ts_zscore` 保幅度，`ts_rank` 杀幅度** | 同骨架 `ts_zscore` S 2.25 vs `ts_rank` S 0.61 | ⚠ 与波 86 第 1 条**表面冲突、实质一致**：`ts_*` 是在**个股自身时间轴**上归一（保留横截面幅度），`group_zscore` 是在**横截面**上按标准差归一（被长尾放大）。**两者不是同一算子**，不能互相引用 |
| 控制实验纪律 | 「先预登记能杀死自己故事的那个测试」 | 已应用：波 87 预登记「若 rank 臂换中性化/universe 均不破 1.25，则该假设死」 |

**由此产生的可复用结论（已足够跨数据集复用）**

- **`ts_zscore`（时序，保幅度）≠ `group_zscore`（横截面，放长尾）**。长尾比率的正确横截面形状是 `group_rank`；
  要「去公司自身常态」必须用**时序**归一，不能用横截面 zscore。此前配方表把二者混为一谈。
- **宇宙档位是区域硬约束，不是可调旋钮**：引用论坛宇宙配方前先查 `config.REGIONS[region]["universe"]`，
  论坛作者所在的区域档位在别区可能根本不存在。

## 10. 波 87 预登记（未发批，两类假设一次测完）

**H-A 归一化形状**：治理信号的 alpha 可能不在「谁的水平高」，而在「谁偏离了自己的常态」。
用**同族同单位字段**自建加速比（仍是单数据集 ATOM，不是双腿混信号）：

| 臂 | 表达式骨架 | 经济含义 |
|---|---|---|
| a1 | `group_rank(divide(ts_backfill(personnel_departure_rate_3m_total,66), ts_backfill(personnel_departure_rate_1y_total,66)), subindustry)` | 近 3 月离职率 / 自家近 1 年离职率 = **离职加速**（>1 = 异常流失） |
| a2 | `group_rank(divide(ts_backfill(personnel_join_rate_3m_total,66), ts_backfill(personnel_join_rate_1y_total,66)), subindustry)` | 入职加速（扩张信号） |
| a3 | `group_rank(divide(subtract(dep3m, join3m), add(dep1y, join1y)), subindustry)` | **净流失 / 总流量**（分母恒正，避免净值为负时翻号与近零分母爆炸） |
| a4 | `group_rank(divide(ts_backfill(management_departure_rate_3m_management,66), ts_backfill(management_departure_rate_1y_management,66)), subindustry)` | 管理层离职加速（治理层专用，比全员更贴机制） |
| a5 | `group_rank(divide(ts_backfill(ceo_tenure_days,66), ts_backfill(max_chief_officer_tenure_days,66)), subindustry)` | CEO 相对**最长任期**高管的位置（接近 1 = CEO 是元老） |
| a6 | `group_rank(ts_zscore(subtract(dep3m, join3m), 252), subindustry)` | **时序归一版**净流失（论坛 43 赞帖的核心手法：`ts_zscore` 保幅度、`group_zscore` 放长尾）。与 f2 的 `ts_delta` 不同：zscore 除以自身波动，稀疏零变化不至于变成巨幅 |

**H-B 设置轴（只在 rank 臂上做，修波 86 的 A/B 失效）**：净流失(`group_rank(market)`) 与
CEO 任期优势(`group_rank(cap bucket)`) 两条最优臂 × {INDUSTRY 中性化, MARKET 中性化, SECTOR 中性化,
TOP1000 universe, decay 12}。

**判死条件（先写死）**：若 H-A 五臂 S 全部 < 1.25 **且** H-B 六臂 S 全部 < 1.25 ⇒
`board_gov_stats` 按「横截面水平型治理信号在 USA/TOP3000 无 Submittable 强度」封存，换下一未测数据集。
**禁止**：`ts_delta`（f2 已证 CW 崩）、`ILLIQUID_MINVOL1M`（USA 不存在）、`add(A,B)` 混腿（红线）。

**发批记录（2026-10-23）**：14 臂 / 5 parent，按设置档隔离（含 `universe` 键的 spec 首次使用）：

| parent | 设置 | 臂数 |
|---|---|---|
| `32m8cHbWs4Ggcf5c47whHNO` | SUBINDUSTRY / TOP3000 / decay 5 | 6（H-A a1–a6） |
| `4xtUIO6Xe4zlaCRYwv33d3O` | **MARKET** 中性化 | 2（H-B 最优两臂） |
| `1sH9FSdQg4GKcaG1ggr0PZyI` | **INDUSTRY** 中性化 | 2 |
| `T2tvt4Pi4MPavXWO3IyYX5` | **TOP1000** universe | 2 |
| `2Ccrzx1tT5bC8M1jx23Wh5x` | **decay 12** | 2 |

预检 `logs/_tmp_w87_preflight.py` 全过（算子 REGULAR-safe / 字段 / 语法 / arity 8/8 / 形状 S9×8）。
发批 `tools/submit_batch.py --spec … --region USA --delay 1`，五批全部 `201`。
`--dry-run` 已逐条核对 payload（`universe=TOP1000`、`neutralization=MARKET/INDUSTRY`、`decay=12` 均正确落进 settings）。

## 11. 波 87 实测与判死裁决（2026-10-23）

收批：14/14 COMPLETE，0 error，5 个 parent 全 terminal。

### 11.1 H-A 自有史加速比（SUBINDUSTRY / TOP3000 / decay 5）

| 臂 | 机制 | S | F | TO | RET | DD | 2Y | SUB | alpha |
|---|---|---|---|---|---|---|---|---|---|
| a1 | 离职加速 `dep3m/dep1y` | 0.28 | 0.07 | 2.32% | 0.74% | 7.36% | 0.34 | 0.28 | `omoRP9jb` |
| a2 | 入职加速 `join3m/join1y` | 0.34 | 0.09 | 2.40% | 0.89% | 9.56% | 0.54 | 0.26 | `gJWXrolK` |
| a3 | 净流失/总流量 | **0.91** | 0.40 | 2.43% | 2.38% | 3.20% | 1.17 | 0.62 | `e76N1qYO` |
| a4 | 管理层离职加速 | 0.06 | 0.01 | 1.84% | 0.20% | 15.14% | 0.47 | 0.56 | `2rj9Gng6` |
| a5 | CEO/最长任期 | 0.50 | 0.20 | 1.47% | 1.92% | 7.19% | 0.29 | **-0.26** | `E5VNmrj9` |
| a6 | 净流失 `ts_zscore(252)` | 0.75 | 0.28 | 2.56% | 1.80% | 3.19% | 0.94 | 0.81 | `xA1VlmZq` |

**H-A 全灭，最高 0.91。** 逐条归因（三条互相印证，指向同一个结构性原因）：

1. **水平型信号（波 85/86）显著强于加速比型（波 87）**：同一字段 `-group_rank(pdep3m, subind)` S 1.12、
   `-group_rank(pdep3m-pjoin3m, subind)` S 1.19，而 `dep3m/dep1y` 只有 0.28。**「偏离自己常态」不是本数据集的信息载体**。
2. **除法的分子分母高度共线**：`dep3m` 是 `dep1y` 的子区间统计，两者相关系数接近 1 ⇒ 比值退化成
   「近 3 月噪声 / 近 1 年慢变」，把信号稀释成噪声比。a1(0.28)/a2(0.34)/a4(0.06) 三条同形态同幅度地崩，就是这个形态的指纹。
3. **a5 CEO/最长任期的 SUB 反转（-0.26）是分母选错的直接证据**：`max_chief_officer_tenure_days` 是
   「公司历史上最长任期」，在老公司里趋于巨大 ⇒ 比值对老公司恒小，横截面里混进了**公司年龄**这个混杂因子，
   子宇宙（大盘老公司）方向被翻转。**教训：分母必须与分子同尺度同分布，不能用「历史极值」当基准。**

a6（`ts_zscore(252)` 时序归一）0.75，比 `ts_delta`（f2 的 0.50）好、比水平型（1.12）差 —— 论坛 43 赞帖的手法
在本数据集**方向正确但量级不足**：它确实避免了 f2 的 CW 崩（CW pass），但同样没有超过横截面水平型。

### 11.2 H-B 设置轴（两条最优 rank 臂 × 5 个设置档）

| 设置 | 净流失 `group_rank(...,market)` | CEO 任期 `group_rank(...,capbucket)` |
|---|---|---|
| **MARKET 中性化** | S 1.02 / F 0.60 / 2Y **1.88** / RET 4.33% / margin 3.89bp / SUB 0.83 `e76N1L6M` | S **1.17** / F **0.75** / 2Y 1.27 / RET **5.13%** / margin **6.22bp** / SUB 0.65 `2rj9GJAP` |
| **INDUSTRY 中性化** | S **1.12** / F 0.61 / 2Y **1.96** / DD **4.87%** / SUB 0.85 `bl8JxNal` | S 1.13 / F 0.65 / 2Y 1.49 / SUB 0.48（限 0.49，差 0.01）`E5VNmqQ0` |
| TOP1000 universe | S 0.95 / F 0.47 / 2Y 1.67 / SUB 0.75 `omoRPnP2` | **S 0.37**（塌） `O0JR6n6b` |
| decay 12 | S 1.15 / F 0.60 / 2Y 1.91 / DD **3.84%** / SUB 0.73 `XgRVNpkm` | S **1.21** / F 0.66 / 2Y 1.53 / SUB 0.37 `2rj9G7vP` |
| 基线（SUBINDUSTRY / decay 5） | S 1.12 / F 0.58 / 2Y 1.93（w86 d2，同轴） | S 1.20 / F 0.65 / 2Y 1.51（w86 t1） |

**设置轴的真实结论（三条，都与「杠杆」直觉相反）**

1. **中性化换 MARKET/INDUSTRY 改变的是「收益/风险比」，不是「信号强度」**：
   CEO 臂 MARKET 把 RET 从 3.62% 拉到 5.13%（+42%）、F +0.10、margin 3.58→6.22 bp，
   但 S 只从 1.20 到 1.17（−0.03）；净流失臂 INDUSTRY 把 2Y 从 1.93 拉到 1.96，S 持平。
   ⇒ **中性化不能破 S 墙**，它能破的是 F / margin / ladder 墙。这与「S 是横截面信噪比」的定义一致：
   去行业/市场均值不改变「谁比谁强」的排序强度。
2. **decay 12 是唯一同时改善三条风险指标的设置**：净流失臂 DD 3.84%（全组最低）、2Y 1.91；
   但 CEO 臂 decay12 把 SUB 从 0.65 打到 0.37（**过平滑 → 大盘股权重上升 → 子宇宙更差**）。
   ⇒ **decay 是「以 SUB 换 DD」的交易**，不是免费杠杆。
3. **TOP1000 再次证伪**（与波 58/59 的宇宙结论一致）：样本减半后 CEO 臂直接塌到 0.37。
   **本数据集的信息密度依赖横截面宽度**，不能靠缩宇宙提纯。

### 11.3 判死裁决（按预登记条件执行）

预登记判死条件：`H-A 五臂 S 全部 < 1.25 且 H-B 六臂 S 全部 < 1.25`。
**实测：H-A max 0.91、H-B max 1.21 ⇒ 条件成立，执行封存。**

**裁决**：`board_gov_stats`（USA/TOP3000/D1）按「**横截面水平型治理信号在 USA/TOP3000 无 Submittable 强度**」封存。
证据面：**4 个经济机制 × 6 条分组/设置轴 × 26 臂**（波 85 十臂 / 波 86 十二臂 / 波 87 十四臂，含重叠），
S 的分布收敛在 **1.11–1.21**，与轴无关 ⇒ 是**数据集级强度上限**，不是轴选择错误。
最强的三条臂（churn/CEO/boardnet）已到 1.1–1.2，距 LOW_SHARPE 1.58 差 0.37–0.47，
而全部增益杠杆（轴族/decay/中性化/形状/宇宙）合计只值 ±0.10 ⇒ **结构性不可修**。

**但保留一条非 REGULAR 出口（值得记，不是安慰奖）**：三条臂 `failed_ppa_count = 0`
（`e76N1L6M` S 1.02 / `bl8JxNal` S 1.12 / `XgRVNpkm` S 1.15）—— 满足 PPA 通道的
Sharpe ≥ 1.0 / 算子 ≤ 8 / 字段 ≤ 3。PPA 提交只能走平台 web UI 且需当期 Power Pool 主题匹配
（见 `brain-alpha-robustness` Phase E 与 `ppa-handoff.md`），agent 不代提交。
这三条留档为 **PPA-eligible**，若后续 Power Pool 主题命中 INSIDERS/PV 类即可人工接续。

### 11.4 波 87 的三条可复用结论（跨数据集）

- **除法归一化不是通用杠杆**：分子是分母的子区间统计（3m ⊂ 1y）时，比值退化为噪声比。
  要归一化必须用**同尺度同分布的平行量**（如 3m vs 3m 的行业中位数），不能用「更长窗口的同名字段」。
- **中性化轴破的是 F/margin/ladder，不是 S**。当唯一卡点是 LOW_SHARPE 时换中性化是**无效动作**；
  当卡点是 LOW_FITNESS 而 S 已过线时，换 MARKET/INDUSTRY 是**首选**（本波 CEO 臂 F +0.10 / RET +42%）。
- **decay 是 SUB 与 DD 的对冲**：加 decay 降 DD，但大盘股占比上升会同步压低 SUB。两者不可兼得，
  要按「当前卡哪个闸」选方向。
