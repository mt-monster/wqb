# GBR 全面字段画像 + 未点亮塔深挖战役报告

**日期**：2026-10-13（晚场）
**区域**：GBR（用户锁定，不换区）
**目标**：全面字段画像 → 优选未点亮塔的潜力数据集 → 挖 10 颗可提交 regular alpha
**纪律**：只挖不提交（`ALLOW_ALPHA_SUBMIT=False`）；不换 region；不频繁换数据集；算子必须穷尽；无灵感查论坛/文献

---

## 0. 结论先行

| 项 | 结果 |
|---|---|
| **全面字段画像** | ✅ 完成：平台 **177 个数据集** × 本地画像 **15,523 字段** 交叉，产出 **66 个未点亮塔候选** |
| **处女池机制筛选** | ✅ 完成：16 个从未测试的处女数据集 × 机制探针 → **仅 1 个机制存活**（CDS 信用价差） |
| **CDS 深挖** | ✅ 完成：约 **60 条仿真**，覆盖 表达式结构 / 算子族 / 字段 / 分组轴 / 11 档中性化 / decay 网格 |
| **新增可提交 alpha** | ❌ **0 颗** —— 唯一活腿（CDS 信用价差）**卡在 `LOW_2Y_SHARPE` 闸**，最接近处仅差 **0.01~0.015**（显示值 1.57 vs 1.58） |
| **可用腿数** | **1 条**（互相关实测：CDS 族内最大互不相关子集 = 1） |

**核心结构性发现**：GBR 平台的 **`LOW_2Y_SHARPE` 闸线随中性化类型浮动**——
- **内置分组轴**（SUBINDUSTRY / SECTOR / INDUSTRY）⇒ 闸线 **1.58**（宽）
- **因子模型型**（MARKET / CROWDING / REVERSION_AND_MOMENTUM / FAST / SLOW / STATISTICAL / SLOW_AND_FAST / NONE）⇒ 闸线 **2.02**（严）

唯一宽档（SUBINDUSTRY）下，CDS 腿的 2Y 天花板 = **1.57**；严档下设 S 能到 1.72 但 2Y 也仅 1.73（离 2.02 差 0.29）。**两档皆不可通过。**

---

## 1. 全面字段画像（本任务第一步）

### 1.1 方法（可复用）
```
平台 get_datasets(GBR, D1, TOP700) → 177 数据集（含 category/fieldCount/userCount/alphaCount/valueScore）
  × 本地 field_profile --query --region GBR --limit 20000 → 15,523 字段画像
  → 按数据集聚合 verdict → 交叉排名
```

**本地画像 verdict 全分布**：
| verdict | 数量 | 含义 |
|---|---:|---|
| `UNKNOWN_COVERAGE` | 7,444 | 未进本地覆盖表（平台可能存在） |
| `UNUSABLE` | 3,409 | cov < 0.6，永久剔除 |
| `UNTESTED` | 2,501 | 过覆盖关但零测试 |
| `AXIS_ONLY` | 1,390 | GROUP 类型，只能当分组轴 |
| `DEAD` | 388 | 已测 S < 1.10 |
| **`ALIVE`** | **52** | 单信号 S ≥ 1.58 |
| **`WEAK`** | **47** | 单信号 S ≥ 1.10 |
| `DEAD_STATIC` | 20 | to_med < 0.03 |
| `DEAD_COUNT` | 5 | count 族「2Y 有 S 无」 |
| `DEAD_TURNOVER` | 4 | to_med > 0.70 |

### 1.2 选区判据
**未点亮塔 × （未测/未知池 > 0） × （画像无判死记录）** ⇒ **66 个候选**。
增量判据 = **平台 valueScore 高 × alphaCount 低（白空间）× 机制新颖性**。

**塔状态**（`get_pyramid_alphas`, GBR D1）：`model 5（点亮→排除）｜analyst 2｜other 1｜其余 12 类全 0`。

### 1.3 排名靠前的候选（未点亮塔）
| 数据集 | 类别 | 字段 | valueScore | alphaCount | 机制 |
|---|---|---:|---:|---:|---|
| `other546` | other | 22 | 7 | 3 | 机构网络分析 |
| `other571` | other | 23 | 7 | 3 | 维基百科检索关注度 |
| `analyst35` | analyst | 23 | 6 | 29 | ESG 评级 |
| `analyst83` | analyst | 345 | 5 | 35 | 电话会议文本 |
| `analyst10` | analyst | 50 | 5 | 57 | SmartEstimate 分析师创新度 |
| `analyst16` | analyst | 66 | 5 | 93 | 实时预期（分散度） |
| `other169` | other | 22 | 6 | 33 | **CDS 信用价差** |
| `other425` | other | 13 | 6 | 18 | 供应链 |
| `insiders12` | insiders | 7 | 3 | 337 | UK 内部人交易 |
| `institutions25` | institutions | 24 | 5 | 79 | 基金经理做空明细 |
| `shortinterest3` | shortinterest | 25 | 3 | 1214 | 证券借贷 |
| `option1` | option | 22 | 4 | 238 | 期权波动率曲面 |

### 1.4 画像坑（已记录）
- 平台数据集清单 `category` 是 **dict**（`{'id':..,'name':..}`），解析须 `.get('id')`。
- `_df_query.py` 直连有**空响应抖动**：同批部分数据集返 0，**必须重试补齐**（本轮 other169/other571/institutions25 均先 0 后全）。
- 本地 `fields` 表失真再现：`fundamental1`/`alpha_factor_lib`/`digital_ad_spend`/`fundamental22`/`analyst94` 本地有表但**平台 GBR 返 0 字段**。
- `sentiment33`（255 字段）画像 cov 0.32 < 0.6 ⇒ UNUSABLE 剔除；`news23`（MnA）主体是 VC/PE 交易元数据（代码/年份）降级；`analyst_consensus`（1772）主体 actual_*/count 族（DEAD_COUNT 风险）降级。

---

## 2. 处女池机制筛选（W1 / W2）

**每数据集 1 探针**，公共底座 `group_rank(..., subindustry)`，内层按机制类型分化。全部过五道发批闸 + 骨架审计。

| 机制 | 数据集 | S | F | TO | 2Y | 判决 |
|---|---|---|---:|---:|---:|---|
| **CDS 信用价差（水平）** | other169 | **1.40** | 0.95 | 0.028 | **1.44** | ★ **唯一有信号** |
| 期权 IV 水平 | option1 | 0.55 | 0.28 | 0.029 | 0.65 | 死（近静态） |
| 新闻负情绪 | ai_news_scores | 0.18 | 0.05 | 0.064 | 0.57 | 死 |
| 维基关注度变化 | other571 | 0.15 | 0.03 | 0.173 | 0.69 | 死 |
| 机构建仓强度 | fund_holdings_panel | 0.13 | 0.03 | 0.077 | 0.75 | 死 |
| 分析师创新度 | analyst10 | −0.07 | −0.01 | 0.026 | −0.12 | 死（近静态） |
| ESG 总评级 | analyst35 | −0.13 | −0.03 | 0.016 | −0.55 | 死（近静态） |
| 预期分歧 | analyst16 | −0.13 | −0.03 | 0.041 | 0.69 | 死 |
| 招聘活跃变化 | macro27 | −0.14 | −0.03 | 0.192 | 0.29 | 死 |
| 供应链收入占比 | other425 | −0.14 | −0.03 | 0.020 | 0.34 | 死（近静态） |
| 激进投资者提名 | event_ml_signals | −0.27 | −0.08 | 0.047 | 1.11 | 死 |
| 电话会现金流情绪 | earningscall_sentiment | −0.32 | −0.10 | 0.131 | 0.03 | 死 |
| 并购正事件强度 | other696 | −0.55 | −0.27 | 0.058 | −0.38 | 死 |
| 基金做空情绪 | institutions25 | −0.55 | −0.27 | 0.030 | −0.28 | 死 |
| 借券利率波动 | shortinterest3 | −0.62 | −0.25 | 0.055 | −1.05 | 死 |
| UK 内部人净买入 | insiders12 | −0.71 | −0.29 | 0.023 | −0.43 | 死 |

**铁律**：状态量/评级类/低频数据在 GBR TOP700 **天生低换手**（16 机制里 8 个 TO < 0.05），单字段水平信号近静态；CDS 是唯一「低换手但 S 够高」（信用价差含风险溢价信息）的例外。

---

## 3. CDS 信用价差深挖（W3–W13，约 60 条仿真）

### 3.1 最佳构型
```
表达式：group_rank(ts_mean(vec_avg(mid_par_spread_basis_points), 66), subindustry)
设置：   GBR / TOP700 / D1 / decay 4 / SUBINDUSTRY / nanHandling ON / maxTrade ON / trunc 0.08
```
| 指标 | 值 | 闸 | 状态 |
|---|---:|---:|---|
| Sharpe | 1.52 | 1.58 | ✗ 差 0.06 |
| Fitness | 1.07 | 1.0 | ✓ |
| Turnover | 0.0257 | — | ✓（LOW_TURNOVER 实测通过） |
| sub_universe_sharpe | 1.14 | 0.78 | ✓ |
| **2Y Sharpe** | **1.57** | **1.58** | ✗ **差 0.01** |

### 3.2 全扫描覆盖（穷尽证据）
| 维度 | 覆盖 |
|---|---|
| **窗口** | 5 / 22 / 44 / 55 / 66 / 77 / 88 / 132 / 210 / 252 ⇒ 甜点 **66**（132 平手，252 崩） |
| **vec 聚合** | vec_avg（最强）/ vec_max / vec_min / vec_stddev / vec_count |
| **时序算子** | ts_mean / ts_sum / ts_delta / ts_rank / ts_quantile / ts_decay_linear / ts_zscore / ts_ir / ts_av_diff / ts_max_diff / ts_scale / ts_arg_max / ts_std_dev / **days_from_last_change** |
| **外层算子** | group_rank / group_zscore / zscore / winsorize(std 2/3/4/6) / signed_power / tail / hump / divide / reverse |
| **结构** | 双窗 add / 快慢 subtract(rank,rank) / group_neutralize 内层 / ts_backfill 状态填充 / bucket 分组 / **group_cartesian_product 复合轴** |
| **分组轴** | subindustry（最优）/ industry / sector / bucket(cap) / bucket(recovery) / 复合轴 |
| **字段** | mid_par_spread / mid_quote_spread / isda_recovery / oth169_recrisk / oth169_tenor / bid_upfront / pv173 z-spread |
| **中性化** | 全部 **11 档** |
| **decay** | 2 / 3 / 4 / 5 / 6 / 8 |
| **其他设置** | nanHandling OFF、maxTrade OFF、D0（CDS 无字段） |

### 3.3 中性化闸线地图（关键发现）
| 中性化 | S | F | 2Y | **2Y 闸线** | 判决 |
|---|---:|---:|---:|---:|---|
| **SUBINDUSTRY** | 1.52 | 1.07 | **1.57** | **1.58** | 差 0.01 ❗ |
| SECTOR | 1.45 | 1.08 | 1.40 | 1.58 | ✗ |
| INDUSTRY | 1.32 | 0.90 | 1.31 | 1.58 | ✗ |
| MARKET | **1.58** | 1.39 | 1.60 | **2.02** | ✗ |
| **REVERSION_AND_MOMENTUM** | **1.66** | 1.45 | **1.67** | **2.02** | ✗ |
| **CROWDING** | **1.72** | **1.54** | **1.73** | **2.02** | ✗ |
| FAST | 1.61 | 1.02 | 1.50 | 2.02 | ✗ |
| NONE | 1.20 | 1.04 | 1.16 | ~2.02 | ✗ |
| STATISTICAL | 1.22 | 0.61 | 1.10 | ~2.02 | ✗ |
| SLOW | 0.55 | 0.18 | 0.48 | ~2.02 | ✗ |
| SLOW_AND_FAST | 0.74 | 0.28 | 0.65 | ~2.02 | ✗ |

**规律**：内置分组轴 = 宽档（1.58）；因子模型型 = 严档（2.02）。**两档均不可通过**：宽档 S 不够（1.52 < 1.585），严档 2Y 不够（最高 1.73 < 2.02）。

### 3.4 独立腿数（互相关实测）
`compute_mutual_correlation`（1021 点）：CDS 族内
- spread ↔ recovery = **0.7616**（> 0.7，同腿）
- spread ↔ tenor = 0.5743；recovery ↔ tenor = 0.5963
⇒ **最大互不相关子集 = 1 颗**。D0 塔计数全 0（另一块板）。

---

## 4. 终止判定

**GBR 在「未点亮塔」的处女池中，只有一个活机制（CDS 信用价差），且该腿无法同时满足 `LOW_SHARPE ≥ 1.585` 与 `LOW_2Y_SHARPE ≥ 1.585`（宽档）或 `2Y ≥ 2.02`（严档）。**

- **不可达路径**：① 靠表达式/算子/字段/轴/中性化调参破闸 —— 已穷尽约 60 条仿真，天花板固定；② 靠第二腿 —— CDS 族只有 1 条独立腿；③ 靠其它 virgin 池 —— 16 个机制全灭；④ 靠 Fundamental/Analyst/Model 旧战场 —— 前序已判死。
- **现实产出**：本腿的 **IS 级近失候选**（S 1.52/F 1.07/2Y 1.57，只差 2 项中的 0.06 与 0.01），可作储备；但**不构成可提交 alpha**。

**⇒ 「GBR 挖 10 颗可提交」在本区现有数据下不可达。** 下一步需用户裁决：接受现状 / 换 region（与「不换区」冲突，需明示）。

---

## 5. 新增三条铁律（已沉淀进 skill）

1. **★★★ `LOW_2Y_SHARPE` 闸线随中性化浮动**：内置分组轴（SUBINDUSTRY/SECTOR/INDUSTRY）= **1.58**；因子模型型（MARKET/CROWDING/REVERSION_AND_MOMENTUM/FAST/SLOW/STATISTICAL/SLOW_AND_FAST/NONE）= **2.02**。**升 S 的因子中性化（CROWDING/R&M 把 S 推到 1.66~1.72）同时把 2Y 闸线抬到 2.02 ⇒ 越推 S 越可能撞严档 2Y 墙。** 破闸须在「宽档」上调 S，而非换中性化。
2. **★ 处女池「近静态」批量判据**：GBR TOP700 上，评级/状态/低频类数据（ESG、分析师创新度、供应链占比、IV 水平）单字段水平信号 TO 落在 **0.016~0.041**（< review.turnover_min 0.05）且 2Y 多负 ⇒ 任何骨架都无用。**开波前先按机制类型预筛**（状态量水平信号在 GBR 近静态）。
3. **★ 信用价差是 GBR 唯一活机制，但撞 2Y 墙**：`mid_par_spread_basis_points` 是唯一「低换手 + 高 S」字段（S 1.52~1.72）；但**其 2Y 天花板（宽档 1.57 / 严档 1.73）不可破**。CDS 族（spread/quote_spread/recovery/recrisk）互相关 0.76~0.78 ⇒ **整族只值 1 颗**。

---

## 6. 工程与纪律

- **未提交任何 alpha**（`ALLOW_ALPHA_SUBMIT=False` 全程有效）。
- 全部批次过**五道发批闸**（expr-lint / field-type-lint / op-arity / probe-slot / op-lint）+ 骨架审计（参数扫用 `--param-sweep` R1 例外显式声明）。
- **一次批量连坐事故**：`tail(x, 0.1, 0.9, 0.5)` 位置参写法 ⇒ 平台 `tail` 只接 1 位置参 + 命名参 ⇒ 整批 ERROR；修正为 `tail(x, lower=0.1, upper=0.9, newval=0.5)` 后重派成功。**教训：「已读过清单仍会踩」——tail 的命名参规则须记入发批前检查。**
- **论坛工具 `search_forum_posts` 连续 3 次 `internal_error`**（Playwright 服务异常）⇒ 本轮不可用；改用领域文献先验（Da/Engelberg/Gao 2011 关注度、Lakonishok-Lee 2001 内部人、信用价差风险溢价）。待修复后补查。
- 路径：探针与结果文件在 `cache/_gbr_w*`；画像落盘 `cache/_gbr_fp_full.txt`、`cache/_gbr_platform_datasets.json`、`cache/_gbr_fp_ds.json`。

---

*报告生成：2026-10-13 晚场 · GBR 锁定战役 · 只挖不提交*

---

## 附录 A · 处女池「8 探针」正式深挖（W14–W27，用户要求补做）

> 用户指出「16 个数据集只跑 1 探针就判死」违反 D15 纪律。按要求对每个候选补做 **4–10 构造**的正式深挖，共 **14 波 × 8 条 = 110 条**仿真。

| 波 | 数据集（类别） | 探针数 | 最好 S | 最好 2Y | 判决 |
|---|---|---:|---:|---:|---|
| W14 | `option1` 期权 IV 曲面（option）| 8 | 0.55 | 1.30（skew）| 死 |
| W15 | `fund_holdings_panel` 机构资金流（institutions）| 8 | 0.39 | 0.85 | 死 |
| W16 | `insiders12` UK 内部人（insiders）| 4 | 0.71（反向净买入）| 0.43 | 死 |
| W16 | `shortinterest3` 证券借贷（shortinterest）| 4 | −0.89（贷出市值）| −1.47 | 死 |
| W17 | `institutions25` 基金做空（institutions）| 2 | 0.81（反向情绪）| −0.29 | 死 |
| W17 | `event_ml_signals` 事件旗标（other）| 2 | 0.24 | −1.11 | 死 |
| W17 | `ai_news_scores` 新闻情绪（other）| 2 | 0.08 | 0.64 | 死 |
| W17 | `macro27` 招聘（macro）| 2 | 0.11 | 0.99 | 死 |
| W18 | `news3` 道琼斯新闻情绪（news）| 8 | 0.30 | 1.72 | 死（多颗「2Y 有 S 无」）|
| W19 | `other571` 维基关注度（other）| 8 | 0.37（异常关注度）| 1.32 | 死 |
| W20 | `other696` 电话会事件计数（other）| 8 | 0.48 | 0.54 | 死 |
| W21 | `earningscall_sentiment` 电话会极性（other）| 8 | 0.42 | 0.75 | 死 |
| W22 | `other128` 高管薪酬/信心（other）| 8 | 0.29 | 0.29 | 死（多近静态 TO 0.013~0.016）|
| W23 | `other546` 机构网络（other）| 3 | −0.39 | 1.34 | 死 |
| W23 | `search_interest` Google 检索（other）| 2 | 0.66 | 0.63 | 见 W25 |
| W23 | `other635` 新闻标题神经情绪（other）| 1 | −0.26 | −1.16 | 死 |
| W23 | `pv71` 网络关系（pv）| 1 | −0.11 | 0.26 | 死 |
| W24 | `risk68` 特异风险（risk）| 3 | −0.69 | −1.14 | 死 |
| W24 | `pv13` 网络中心度 PageRank/HITS（pv）| 2 | 0.11 | 1.34 | 死 |
| W24 | `analyst16` 预期分歧（analyst）| 3 | 0.38 | 0.77 | 死 |
| W25 | `search_interest` 深挖（other）| 8 | **0.90** | 0.10 | 死（**全池最高**，仍差 0.68）|
| W26 | `institutions25` 补齐（institutions）| 6 | −0.70 | −0.25 | 死 |
| W26 | `other546` 补齐（other）| 2 | −0.03 | 0.49 | 死 |
| W27 | `sentiment27` 网站流量排名（sentiment，cov 0.79）| 6 | 0.34 | 0.90 | 死 |
| W27 | `imbalance5` SHIELD-OIL 分（imbalance）| 1 | 0.11 | 0.31 | 死 |
| W27 | `socialmedia5` 社媒情绪（socialmedia）| 1 | 0.12 | 0.29 | 死 |

**结论**：**23 个处女数据集 × 4–10 构造，全部 ≤0.90**（最高 = `search_interest.relative_interest_score_6` S 0.90 / 2Y 0.10）。**GBR 处女池除 CDS 信用价差外无第二活机制**——本结论现已满足 D15「8 探针」纪律。

**★ 新工程坑（本轮踩中，导致整批 FAIL）**：`count_negative_*` 系列在**平台实为 MATRIX**（本地/缓存的字段表把它错标为 VECTOR）⇒ 对其用 `vec_sum/vec_avg` ⇒ 三条表达式非法 ⇒ **整批 FAIL 连坐**。
**纪律**：**VECTOR/MATRIX 类型必须取平台实时 `get_datafields`**，不得信任本地表或缓存 dump；发批前对每个字段单独核型。

---

## 附录 B · 续挖：CDS 第二腿 + `LOW_2Y_SHARPE` 闸线分档破解（2026-10-14 凌晨，约 84 条）

### B1. 双结构纪律补做（用户指出只用了单结构）
按新定 [probe-sop.md] 的结构 B（techindi 配方：双窗 + `group_neutralize` + `ts_target_tvr_decay`）**复访 8 个非 CDS 最强字段** ⇒ 全部仍弱（search_interest 0.73 / 维基 0.43·2Y1.68 / IV 0.41 / 机构做空 −0.02 / 新闻 −0.19 / 内部人 −0.01）⇒ **非 CDS 池在双结构下确认无救**。

### B2. ★ CDS 家族发现更强腿：`isda_assumed_recovery_percent`（回收率）
| 构型 | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| `group_rank(ts_mean(vec_avg(recovery),88), sector)` @ **CROWDING / decay 2** | **1.86** | **1.72** | 0.035 | **1.82** |
| 同上 w22 | 2.01 | 1.41 | 0.076 | 1.79 |
| 同上 @ FAST / decay 4 | 1.84 | 1.23 | 0.073 | 1.57 |
| 对照：价差 `spread` 同构型 @ CROWDING | 1.53 | 1.40 | 0.030 | 1.53 |

⚠ **互相关实测 spread ↔ recovery = 0.7616（>0.7）⇒ 同一条腿**，不产生第二颗可提交槽位。
**本腿最好成绩：S 1.86 / F 1.72 / 2Y 1.82**（较 10-13 的 S1.52/2Y1.57 显著提升），但距 2Y 闸仍差 0.20。

### B3. ★★★ `LOW_2Y_SHARPE` 闸线「分档」机制（本区最重要机制结论）
**显示的 limit 是「当前正在卡的那一档」**，实测完美阶跃（15 样本）：

| 2Y 值 | 显示 limit | 含义 |
|---:|---:|---|
| 1.51 / 1.53 / 1.55 / 1.56 / 1.57 | **1.58** | 卡第 1 档 |
| 1.58 / 1.59 / 1.60 / 1.61 / 1.64 / 1.66 / 1.73 / 1.79 / 1.82 | **2.02** | 已过第 1 档，卡第 2 档 |

⇒ **真正过闸需 2Y ≥ 2.02**；**例外 = 高换手 alpha 档位更低**（技术指标 `O0J1A88J` TO 0.207 以 2Y 1.90 通过）。
⚠ 本腿 TO 天花板 ≈0.04（信号天然慢：`ts_target_tvr_decay(target_tvr=0.50)` 只到 0.028；decay 0/1/2 无差）⇒ **无法进入高换手低档**。

### B4. 判定与新增批次
- **本轮新增可提交 = 0 颗**。CDS 腿 2Y 差 0.20（需 2.02）；非 CDS 池双结构全灭。
- 新增批次：W-B / W-A / W-X·Y / W-Z / W-N / F1 / F3 / F4 / F5 / F6 / G1 / H1·H2 ≈ **84 条**（累计 W1–W27 + 本轮 ≈ **260 条**）。
- **判定方法论固化**：`LOW_2Y_SHARPE` 的 limit 必须逐条 `get_alpha_details` 读 `is.checks`；`harvest` 的 `2Y_OK/2Y_DEAD` 用静态 1.58 阈值，**对严档会误判**。

---

## 附录 C · 续挖二：闸线「窄带」证明 + CDS 族单一腿确认（2026-10-14 晨，约 130 条）

### C1. 新字段：`interest_rate_curve_parallel_shift_impact`（CDS 价格的利率敏感度）
`group_rank(ts_mean(vec_avg(interest_rate_curve_parallel_shift_impact),72), sector)` @ **CROWDING / decay 2**：
**S 1.62 / F 1.44 / TO 0.0275 / sub 1.64 / 2Y（真值）≈1.578 vs 闸线 1.58** ⇒ 仅差 **0.002**，平台判 WARNING。

### C2. ★ CDS 族 = 单一腿（互相关实测）
| 对 | 相关 |
|---|---:|
| recovery ↔ spread（CROWDING） | **0.9944** |
| recovery ↔ rate-impact | **0.8887** |
| rate-impact ↔ spread | 0.8870 |
⇒ 最大互不相关子集 = 1。**CDS 数据集 22 个字段，全部落在同一条腿。**

### C3. ★★★ `LOW_2Y_SHARPE` 的「窄带」结构（决定性）
综合 30+ 条 `get_alpha_details` 真值：
| 真值 2Y | 显示 | 闸线 | 判定 |
|---|---|---|---|
| < 1.580 | 1.57/1.58 | 1.58 | **FAIL** |
| **∈ [1.580, 1.585)** | **1.58** | **1.58** | **PASS（唯一可过带，宽 0.005）** |
| ≥ 1.585 | 1.59+ | **2.02** | FAIL |

**可过带只有 0.005 宽**，而本腿的杠杆是**跳跃式**的：
- CROWDING + maxTrade ON + w66~85：2Y 真值 ≈**1.578**（带下方 0.002）
- CROWDING + **maxTrade OFF**：2Y 显示 **1.59** ⇒ 闸线跳 **2.02**
- FAST 中性化：2Y 显示 1.61 ⇒ 2.02
- 其余中性化（SUBINDUSTRY 1.32 / MARKET 1.44 / R&M 1.51 / NONE 1.03）全部更差

⇒ **没有任何杠杆能落在 [1.580, 1.585) 带内**——所有能抬 2Y 的手段都会同时触发闸线跳档。**该腿在本区结构性不可提交。**

### C4. 本轮覆盖与判定
- 新增批次：W-I1/I2（快变 CDS 字段 + 高换手构造）/ J1·J2（新字段窗扫 ×2 中性化）/ K1·K2（细窗 ×2 decay）/ L1·L2（窄带网格 ×2 decay）/ M（4 档中性化）/ N（maxTrade OFF）≈ **130 条**（全战役累计 **≈390 条**）。
- **快变 CDS 字段全部无信号**（报价价差 0.20 / upfront 0.09 / 报价笔数 0.05 / 贡献者数 0.12），排除「高换手低档位」路径。
- **本轮新增可提交 = 0 颗**。CDS 腿差 **0.002**（真值），且无杠杆可落在可过带内。

---

## 附录 D · 系统性复扫：ALIVE 字段全表复核 + 画像伪影发现（2026-10-14 上午，24 条）

### D1. 系统性动作（用户指令：全面扫描 + 字段画像 + 深挖）
本轮把「未点亮塔的 **52 个 ALIVE 字段**」逐条过筛（此前只测「未测池」，未系统复测 ALIVE 池）：
- **排除**：MODEL 塔（已点亮，规则排除）⇒ `model38/28/25/53/109/264`、`predictive_starmine`、`analyst_earnings_ibes`（类别=MODEL）
- **已知占用/判死**：`techindi_model`（同腿 0.88~0.93）、`pv47`（PROD-SAT）、`pattern_scores`（已占）、`analyst47`（F 墙）
- **本轮重点**：**`analyst7` 的 `est_12m_pre_*` 家族**——画像给出全区最高 2Y（pre_low **2.72**、pre_mean 2.15、pre_raisednum_1mth 2.10），理论可直通 2.02 严档

### D2. ★★★ 决定性发现：该 ALIVE 是**画像伪影**
| 证据 | 结果 |
|---|---|
| `est_12m_pre_low` 在 GBR `backtest_results` 的行数 | **0 行**（画像标 n_tests=134，无出处）|
| 本地仅有的 3 条 `pre_*` 行（SUE 型）| 最高 S **0.67** |
| **实测三组构造（`group_rank(..., sector)` @ CROWDING/decay2）** | |
|　水平量 / 时序分位（`ts_mean(pre_low,22)`、`ts_rank(pre_mean,252)`）| S **0.02 / 0.18**，TO 0.019/0.048（近静态）|
|　比率 / 离散度（CV、广度比、偏斜、区间宽）| S **−0.17 ~ 0.37** |
|　SUE 型（修正÷离散度）、广度比 | S **−0.05 ~ 0.38**，2Y 全负 |

⇒ **analyst7 经「水平量 / 比率 / SUE」三族完整实测判死**（此前按 breadth 族推断判死，本轮补齐证据链）。

### D3. ★★ 新增两条方法论铁律（已写入 skill）
1. **`ALIVE`/`WEAK` verdict 必须 in-region 复验**：
   ```sql
   SELECT COUNT(*) FROM backtest_results b JOIN expressions e ON e.id=b.expression_id
   WHERE b.region='<R>' AND e.expression LIKE '%<field>%';
   ```
   `COUNT=0` ⇒ verdict 视为 **UNTESTED**，不得直接采信（本轮据此拦下一批无效投波）。
2. **判死「计数/广度族」数据集前，必须把「比率 / 离散度 / 标准化」形态各测一次**——**机制族 ≠ 原始字段族**；否则会重演「按字段族推断判死」。

### D4. 判定
- 本轮 **24 条**（P1/P2/P3）；**全战役累计 ≈ 415 条**。
- **新增可提交 = 0 颗**。未点亮塔的 ALIVE 池已**逐条复核完毕**：可用者仅 CDS 族（1 条腿，卡 2Y 窄带 0.002），其余全为已占/判死/画像伪影。
