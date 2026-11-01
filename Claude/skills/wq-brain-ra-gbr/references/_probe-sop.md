# GBR 探针派发 SOP —— 最大化「测出数据集好结果」的概率

> 来源：2026-10-13 GBR 战役 **W1–W27 约 175 条**实证（16 处女池探针 + CDS 深挖 + 23 处女集 8 探针）+ 前序 11 波 88 条 / Fundamental 3 波 24 条。
> 目标：用最小预算回答「这个数据集有没有配得上**GBR 已验证结构**的机制」，并把误杀率与连坐率压到最低。
> **与 DEU 版的三个结构性差异**（本区特有，先记住）：① **multi-sim 上限 = 8 条**（DEU 用 10 槽）；② **`LOW_2Y_SHARPE` 闸线按自身真值分档**（`2Y<1.58` ⇒ limit 1.58；`2Y≥1.58` ⇒ limit 跳 **2.02** ⇒ 实际常需 2Y ≥ 2.02）——**不是"随中性化浮动"**，换中性化只改 2Y 的数值；③ **单一 universe TOP700**（无档位可选，D0 多数数据集无字段）。

---

## 第 0 步：开批前筛选（零成本，能杀掉大部分无效探针）

1. **塔闸（GBR 第一顺位）**
   - `get_pyramid_alphas` → **只挖「未点亮塔 × ALIVE 密度」**。GBR 现状：`model 5（≥3 已点亮 → 规则排除）｜analyst 2｜other 1｜其余 12 类 0`。
   - 已点亮的塔**一律不选**（用户规则）；未点亮塔里按「ALIVE 字段数 × 平台 valueScore / alphaCount」排序。
2. **语义闸（读字段级 description，不是数据集级）**
   - 数据集级 description 会骗人。**开批前必查字段级描述**，剔除三类非信号：**标签类**（`*_label*` / `*_bucket*` / `probability_label*`）、**轴类**（`*_grouping_*` / `sector` / `rbics` 代码）、**元数据类**（时间戳 / 货币码 / SIC 码 / `*_id` / 交易笔数计数字段）。
   - GBR 实证：`dl_riskfree_returns`（40 字段全 `probability_label*`/`quantile_label*`）与 `pv29`（38 字段全 `industry_grouping_*`）**整块非信号**——查描述可零成本跳过。
3. **画像闸**（`tools/fields/field_profile.py --query --region GBR`）
   - coverage<0.6 剔除；`to_med<0.03` → DEAD_STATIC；名字含 `count/num` 且 S≤0.7 → DEAD_COUNT；`to_med>0.70` → DEAD_TURNOVER。
   - ⚠ **GBR 与 DEU 的差异**：GBR 平台 **`LOW_TURNOVER` 实测不拦低换手**（TO 0.0257 通过），因此 `review.turnover_min=0.05` 只是**筛选启发式**、不是平台闸。但「近静态」仍是**机制无用的强信号**（见下条）。
4. **★★★ 近静态闸（GBR 本轮新增判据，最高性价比）**
   - **状态量 / 评级 / 低频类数据（ESG 评级、分析师创新度、供应链占比、期权 IV 水平、网站流量排名）单字段水平信号 TO 落在 0.016~0.041 且 2Y 多负 ⇒ 任何骨架无用，直接跳过。**
   - 实证：本轮 16 个机制里 **8 个命中**（ESG 0.016 / 创新度 0.026 / 供应链 0.020 / IV 0.029…）；`other128` 高管薪酬 8 探针里多颗 TO 0.013~0.016。**开波前按机制类型预筛，可省掉约一半波次。**
5. **历史闸（最重要的单条规则）**
   - 先查 `output_report/GBR_*`、`Claude/skills/wq-brain-ra-gbr/references/*`、`.workbuddy/memory/*`：**有没有已验证结构/已判死族？禁止自造结构开荒、禁止重测已判死的族。**
   - GBR 已验证结构见第 1 步「两个结构」；已判死的类别分支（analyst 五集、fundamental 13 集、techindi、cds 外 other 全域）**不再投波次**。
6. **★★ `ALIVE`/`WEAK` verdict 必须 in-region 复验（2026-10-14 新增铁律）**
   - `field_profile` 的 `S_sg / 2Y_sg / n_tests` **必须能在本地 `backtest_results`（region=该区）里找到对应行**；找不到 ⇒ 该 verdict 不可信。
   - **实证**：`analyst7.est_12m_pre_low` 画像标 **ALIVE S 1.90 / 2Y 2.72 / n=134**，但 GBR 库中该字段 **0 行**（用 `LIKE '%est_12m_pre_low%'` 查证）⇒ 实测水平量、广度比、SUE 型三组构造 **全部 ≤0.37**。**该 ALIVE 是画像伪影，直接投波次会白烧一批。**
   - **操作**：开波前对每个候选 ALIVE 字段跑一句
     ```sql
     SELECT COUNT(*) FROM backtest_results b JOIN expressions e ON e.id=b.expression_id
     WHERE b.region='<R>' AND e.expression LIKE '%<field>%';
     ```
     `COUNT=0` ⇒ 该 verdict 视为 UNTESTED，按探针规格重测，不得直接采信。
7. **概念族分组**：把候选字段按机制族分组（水平量 / 变化率 / 计数 / 比率 / 评级 / 情绪 / 事件 / 网络…），**每族选 1–2 个代表**（cov 最高、alphaCount 最低）。
   - 依据：**同族字段高度相关 ⇒ 测族内一个 = 测族内全部**；不同族才带新信息。
   - ⚠ **同类字段的「水平量 vs 比率」是不同族**：`est_12m_pre_raisednum_4wks`（原始计数，DEAD_COUNT 风险）与「广度比」（上调家数 ÷ 上下调家数之和，`divide` 比率形态，可活）机制不同 ⇒ **判死某数据集前必须把「比率/离散度/标准化」形态各测一次**（本区实证：analyst7 水平量与广度比均死，但这是「测过才判死」的正确顺序）。

---

## 第 0.5 步：★ 栖息地闸（2026-10-31 新增，零成本，比第 0 步更前置）

> 来源：`insider_trx_matrix` 两批 4 条全灭后的复盘。**根因不是模板选错，是这个信号在 GBR 根本没有栖息地。**

**动作**：`get_platform_setting_options()` → 看该 (region, delay) 的 **universe 全集**。

**判据**：若候选信号属于「**小票 / 非流动 / 事件驱动**」类，而该区 universe **只有大票档、无 illiquid 备选** ⇒ **结构性不可打，零仿真直接跳过**。

| 信号类型 | 栖息地要求 | GBR 能否满足 |
|---|---|---|
| 内部人交易、SUE 漂移、Amihud 非流动溢价、52 周高点、小盘反转、限价单失衡 | **必须有 illiquid / 小盘 universe** | ❌ **GBR 只有 TOP700** |
| 价值 / 质量 / 会计口径 / 分析师修正 / 大盘动量 | 大票 universe 即可 | ✅ 可打 |

**决定性实证**：同一表达式 `ts_zscore(ts_sum(total_top_buy_transaction_count,W),252)` —— USA `ILLIQUID_MINVOL1M` **S 2.89** / GBR `TOP700` **S 0.95**，**差 3.0 倍**。论坛帖 `43152032301591` 原文：「信号住在定价迟钝的非流动小票里，流动大票上不存在」。

**为什么这条最值钱**：它把「4 批仿真 + 一次论坛检索」压缩成「一次零成本查表」。**在与第 0 步同等优先级上并列执行。**

### 第 0.5b 步：★★★ 数据集级覆盖率闸（2026-10-31 新增，第五种判死形态）

> 来源：`stock_cluster_dl` 收批后顺手拉 `get_datasets(category="other")`，发现 **GBR D1 的 other category 有 41 个数据集，而我此前只在 13 个上做过判决**。剩下 29 个的 `coverage` 全为 **0.0** —— 它们在 TOP700 下平台根本无数据。而我正打算给其中 5 个（`other567` / `other169` / `other327` / `other546` / `other571`）各补 6 条探针。**那 30 条仿真全部是白烧的。**

**动作**：`get_datasets(region, delay, universe, category=<目标塔>)`，看返回列表每一项的 `coverage`。

**判据**：

| `coverage` | 含义 | 动作 |
|---|---|---|
| **= 0.0** | 该数据集在该 (region, delay, universe) 下**无任何覆盖** | **`STRUCTURAL-DEAD`，零仿真跳过，不得派探针** |
| < 0.20 | 覆盖极稀，持仓必然集中 ⇒ CW / SUB 双闸先天不利 | 仅在无更好标的时试，且先看字段级 coverage |
| ≥ 0.50 | 可正常打 | 正常 8 探针流程 |

**为什么必须显式做这一步**：

1. **它是唯一能「零仿真否定整批数据集」的闸**。第 0.5a 判的是「信号的栖息地」，这条判的是「数据的栖息地」——前者要懂机制，后者只需读一个数字。
2. **它解释了一批历史上的「莫名其妙全灭」**。`fundamental31`（0 字段）、`institutions18`（GBR 0 字段）、`analyst10`（coverage 0）、`quant_factor_lib`（190 字段 coverage 全 0）本质上都是同一个死法，此前被当成「信号弱」逐条烧探针。
3. **不做这步会双层误判**：既浪费仿真，又会把「无数据」写成「无信号」，污染机制层结论（如「OTHER 塔全灭」）。

**★ 与之配套的「数据集普查」纪律**：每进入一个新的 category 或新的塔，**第一次动就必须拉全集并数清三种数量**——`总数` / `coverage > 0 的个数` / `coverage = 0 的个数`，写进台账。GBR D1 other 的普查结果是 **41 / 12 / 29**。此前「13 个数据集」这个数字本身就是错的，导致后续所有百分比都失真。

### ★★★ GBR D1 全 category 普查基准表（2026-10-31 实测，`get_datasets(region="GBR", delay=1, universe="TOP700")` 无 category 过滤）

**总计 177 个数据集：`coverage > 0` 的 73 个，`coverage = 0.0` 的 104 个。**

| category | 总数 | coverage>0 | coverage=0 |
|---|---:|---:|---:|
| model | 46 | **22** | 24 |
| other | 41 | 12 | 29 |
| analyst | 19 | **8** | 11 |
| news | 18 | **6** | 12 |
| pv | 16 | 4 | 12 |
| fundamental | 12 | 3 | 9 |
| institutions | 5 | **4** | 1 |
| risk | 5 | 2 | 3 |
| insiders | 3 | 2 | 1 |
| sentiment | 3 | **3** | 0 |
| socialmedia | 3 | 1 | 2 |
| earnings | 2 | **0** | 2 |
| imbalance / macro / option / shortinterest | 各 1 | 0 / 0 / 0 / **1** | — |

**★★★ 这张表推翻了本区一条长期错误结论**：此前记「GBR D1 可用信号家族已穷尽」，据此判断 20 条目标不可达。**实际有 22 个 model + 8 个 analyst + 6 个 news + 4 个 institutions + 3 个 sentiment + 3 个 fundamental 共 50 个 `coverage>0` 的数据集，其中大批从未测过。**「已穷尽」= 只按「记得测过谁」组织清单，从未拉过全集。

**★★ 高优先未测处女集（coverage 高且 alphaCount 证明能出货）**

| 数据集 | category | coverage | 字段 | alphaCount | 备注 |
|---|---|---:|---:|---:|---|
| `pv29` | pv | **1.0000** | 50 | 66 | 全 `coverage 1.0` 且**低拥挤**，PV 塔 |
| `institutions6` | institutions | **1.0000** | 11 | 881 | 已测 8 探针 → `CONFIRMED-DEAD`（最高 S 0.16）|
| `risk88` | risk | **1.0000** | 1 | 544 | 仅 1 字段 |
| `news104` | news | 0.9695 | 11 | 388 | — |
| `fund_holdings_panel` | institutions | 0.9099 | 18 | 272 | — |
| `shortinterest3` | shortinterest | 0.8490 | 25 | 1569 | — |
| `news17` / `news18` | news | 0.8371 / 0.8192 | 48 / 70 | 384 / 1197 | — |
| `model53` / `model238` / `model36` | model | 0.8453 / 0.8052 / 0.7988 | 22 / 22 / 20 | 53 / 637 / 276 | — |
| `analyst48` / `analyst9` | analyst | 0.8066 / 0.7516 | 7 / 51 | 26 / 195 | — |
| `sentiment27` | sentiment | 0.8003 | 18 | 790 | — |
| `predictive_starmine` | model | 0.7113 | **631** | 4448 | 字段最多 |
| `model25` / `model26` | model | 0.6713 / 0.6057 | 97 / 436 | 24011 / 20870 | 已测部分 |

**★★ 命名陷阱（新反例）**：`analyst_earnings_ibes`（coverage 0.9966 / 42 字段 / alphaCount 1080）名字像 IBES 分析师预测，**但 42 个字段全部是价量数据**（`closing_price_dlr{1,2,3}` / `*_total_return` / `market_capitalization` / `shares_outstanding` / `trading_volume` / `volume_weighted_avg_price`），无一分析师字段。**归入已判死的价量族，零仿真跳过。** ⇒ 数据集名不可作为机制判据，必须逐字段读 description。

---

## 第 1 步：探针批构造（8 槽 = 2 结构 × 3 跨族字段 + 2 机动）

> GBR 的 multi-sim **上限 8 条**（DEU 为 10）。**2 结构 = 本区已验证的赢家**——只测一个结构会错杀字段（结构与字段的匹配是**字段属性**，逐字段不同）。

**★★★ 并发受限时的分批纪律（2026-10-31 新增，本区最易犯的错）**

面板写「**每波探针位上限 2**」，而判死纪律是「**8 探针无 S≥0.5 才判死**」。两句话合起来只有一种正确读法：

> **2 条/批 × 连发 4 批 = 8 探针。**　「每批 2 条」**不等于**「2 条就能判死」。

- 用户级并发限制（如「`create_multi_simulation` 限 2 条」）只约束**单批宽度**，不降低**判死所需总样本量**。正确适配 = **多批串接**，不是缩批。
- 每批跑完后**立刻发下一批**，不要等前一批的结论——4 批凑的是「同一数据集的 4 个不同构造」，彼此独立。
- **2 探针就下判死结论 = 违反 D15**，且和 2026-10-13 那次「1 探针判死 16 个处女集」是同一个错，只是量级从 1 变成 2。

**8 探针的最小分配（2 条/批 ⇒ 4 批）**：

| 批 | 内容 | 说明 |
|---|---|---|
| 1 | 结构 A × 2 个跨族字段 | house 底座，水平量形态 |
| 2 | 结构 A × 剩 2 个跨族字段 | 补齐族覆盖 |
| 3 | 结构 B × 2 个字段 | techindi 配方（**必跑，否则是「只测一个结构」**）|
| 4 | 2 机动槽 | `vec_max`（VECTOR 数据集）/ `reverse`（方向不明）|

**降级通道**：若某数据集语义明显无关（第 0 步已判标签/轴/元数据）⇒ 可 0 探针跳过，但**必须写明跳过理由**；若只跑了 2 条就被外部约束中断 ⇒ 判死结论**必须打 `PROBE-KILLED` 标签**（见第 2 步），并写进待补课清单。

**★★★★ 模板多样性下限（用户级硬约束，2026-10-31 补）**

**数据集级考察（从首探针到「判死 / 出腿」）必须覆盖 ≥10 个结构互异的模板**，来源需标注 `forum` / `paper` / `自建`。

- **区分两个层级**：单批 8 槽（2 结构 × 3 字段 + 2 机动）是**探针形状**；10 模板是**数据集级的完整考察量**。8 探针 ≠ 10 模板——探针批只是第一轮，后续深化要继续补结构。
- **「互异」的判据落在**：骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换 / 窗口族。**换窗口、换常数不算新模板。**
- **为什么**：模板单一会把「骨架选错」误判成「字段没信号」。饱和数据集尤其致命——同族变体全灭 ≠ 机制不成立。
- **豁免**：`skip_diversity_gate` 只豁免**批级**结构多样性闸，**不豁免**数据集级的 10 模板要求。探针批可以 2 条，但**不得 2 条就停止考察**。
- **补充来源**：`search_forum_posts` / `read_forum_post`（平台论坛模板与踩坑）、平台 ideas 文档、`web_search` 查学术文献的因子定义与方向先验。

**本轮反例**：`other250` 12 个字段只用了 2 个模板（`reverse(ts_delta(rank(...)))` 系）⇒ 星级质量族、价格带族、水平量形态、结构 B 全未测，却已记「判死」。

**两个结构（GBR 已验证）**：

| 结构 | 表达式骨架 | 来源 / 适用 |
|---|---|---|
| **A · house 底座** | `group_rank(ts_mean(vec_avg(F), N), subindustry)`（MATRIX 去掉 `vec_avg`） | 本轮 39 数据集筛选底座；通用首选，N=22/66 |
| **B · techindi 配方** | `group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(add(ts_mean(ts_backfill(F,500),1), ts_mean(ts_backfill(F,500),60)), sector)), std=0.15), lambda_min=0, lambda_max=1, target_tvr=0.50), sector)` @ **CROWDING / decay 2** | [other.md](other.md) `3qVP6pNO` 赢家配方（双窗 + 残差化 + tvr_decay）|

**6 个字段 = 跨概念族代表**（不是同族 6 个）；VECTOR 字段在结构内用 `vec_avg`。
**2 个机动槽**：
- VECTOR 数据集 → 留给 **`vec_max`**（聚合算子是独立搜索维度）；
- 语义方向不明的字段 → 留给 **`reverse`**（GBR 实证：`days_from_last_change` 原始 S −1.39，反向即 +1.39——**方向本身就是信息**）。

**发批前六闸（逐条过，缺一即整批连坐）**：

| # | 闸 | 命令 / 要点 |
|---|---|---|
| ① | 值型自检 | `dispatch` 内置 `expr-lint` |
| ② | 元数检查 | `op_arity.ensure_safe_for_dispatch`（`dispatch` 内置 `op-arity`） |
| ③ | **字段类型（GBR 最易踩）** | **VECTOR/MATRIX 必须取平台实时 `get_datafields`，不得信本地表或缓存 dump**。⚠ GBR 实证：`count_negative_*` 平台实为 **MATRIX**、本地表错标 **VECTOR** ⇒ 误用 `vec_*` ⇒ **整批 FAIL** |
| ④ | 算子存在性 | `op-lint`（GBR 平台清单 **102 个**）。⚠ `vector_neut` **不在** GBR 清单；`tail` 只接 **1 位置参 + 命名参**（`tail(x, lower=, upper=, newval=)`，位置参写法整批 ERROR） |
| ⑤ | 骨架多样性 R2 | `tools/fields/skeleton_panel.py audit --path <f> --region GBR`（**单模板 ≤60%**；多字段 sweep 也须重组骨架，**不得用 `--param-sweep` 绕过**；已锁字段参数扫才可声明 `--param-sweep`） |
| ⑥ | 探针台账 | `probe-slot`（每波探针位上限 2，见 SKILL.md 面板） |

> 合规模板（5 放行形态必用满）：`add`（同字段双窗）/ `divide`（比率）/ `subtract(rank,rank)`（行业内相对）/ `if_else`·`trade_when`（门控）/ `group_rank`·`group_zscore`（组内标准化）。**禁止两条独立信号腿相加**；算子数 <10。

---

## 第 2 步：读数三分法（**GBR 闸线与 DEU 不同，务必按本区口径**）

| 双结构最好读数 | 动作 |
|---|---|
| **S≥1.58 且 2Y ≥ 本档闸线** | 全闸验证：`get_alpha_details`（全 checks）→ prod/self 双端点 → **PnL 互相关去重** |
| **S 1.0–1.58** | **不判死**——「结构没找对」信号带。升级：窗扫描（N∈{5,22,55,66,77,132,252}）、轴扫描（subindustry/sector/industry/bucket/复合轴）、算子微调（`ts_rank`/`ts_decay_linear`/`winsorize` std/`signed_power`） |
| **S<0.5（双结构都）** | 判死；同族字段免测。**判死前自检两问：真的用了两个结构吗？字段真的跨概念族吗？** |

**★★★ 判死标签三档（2026-10-31 新增，写台账时必须带标签）**

判死结论必须附**证据强度**，否则后续波次会把「没测够」当成「测过了」，永久封掉一条活路。

| 标签 | 条件 | 后续动作 |
|---|---|---|
| `PROBE-KILLED` | 探针 **< 8** 条、或只测了 1 个结构 | **不可信**，不进 dead_end；写进「待补课」清单，下波优先补满 8 探针 |
| `CONFIRMED-DEAD` | **≥8 探针**、**双结构都跑过**、跨族字段覆盖、最好读数 S<0.5 | 可进 `dead_end`，同族字段免测 |
| `STRUCTURAL-DEAD` | `CONFIRMED-DEAD` **且**有跨区/跨宇宙对照证据（同表达式在别的区/更大 universe 能活） | 可进 `dead_end`，**并注明「仅在 <region> 限定，不外推」** |

**为什么必须分档**：本轮 `insider_trx_matrix` 属 `STRUCTURAL-DEAD`（跨区对照 2.89 vs 0.95，证据最硬）；但同一轮里 `other250` / `other567` / `other169` / `other327` / `other546` / `other571` 都只跑了 **2 探针**就被当成「判死」记下来 —— 实际全是 `PROBE-KILLED`，**在「OTHER 塔 13 个数据集全灭」这个结论里，多数是不可信的误杀**。一次标签混用，等于永久关掉整片搜索空间。

**★★★ GBR 特有：`LOW_2Y_SHARPE` 闸线地图（本区最重要的读数口径）**

| 中性化类型 | 闸线 | 本区实测 |
|---|---:|---|
| **内置分组轴**（SUBINDUSTRY / SECTOR / INDUSTRY） | **1.58（宽）** | CDS 腿 SUBINDUSTRY 2Y=1.57 ⇒ 差 0.01 |
| **因子模型型**（MARKET / CROWDING / REVERSION_AND_MOMENTUM / FAST / SLOW / STATISTICAL / SLOW_AND_FAST / NONE） | **2.02（严）** | CROWDING 2Y=1.73、R&M 2Y=1.67 ⇒ 均差 0.29+ |

- ⚠ **升 S 的因子中性化同时抬 2Y 闸线**（CROWDING 把 S 推到 1.72，2Y 闸线同时升到 2.02）⇒ **破闸必须在「宽档（内置轴）」上调 S，严禁换中性化凑 S。**
- ⚠ **GBR 平台 `LOW_SHARPE` 实测闸线 = 1.58**（非 config 的 delay1=1.25）。
- ⚠ **真值须 ≥ 闸线 + 0.005**（平台把 ladder 四舍五入到 2 位再严格比较）。
- **2Y 要单独看**：S 高 2Y 低 = 早衰（GBR 实证：`news3` 多颗 2Y 1.44~1.72 但 **S≈0**，属「2Y 有 S 无」形态，不可用）。

**★★ 两种 GBR 特有判死形态（读数时识别）**
1. **「F 墙（不变量型）」**：族内 `S 与 1/√TO 严格同向` ⇒ `F = S×√(returns/max(TO,0.125))` 是经济不变量，全参数空间 F 恒定（实证 `analyst47` F 恒 0.96~0.97，只差 `LOW_FITNESS` 0.04 却扫不上去）。
2. **「2Y 有 S 无」**：2Y 高（≥1.4）但 S≈0（≤0.3）⇒ 信号只反映最近 2 年行情，不可用。

---

## 第 3 步：出闸后去重（一条腿只出 1 颗）

- `GET /alphas/{id}/recordsets/pnl` 取两条 PnL 求 Pearson——**零平台配额**的互相关；或用 `compute_mutual_correlation`（本地计算，不占配额）。
- **同机制跨数据集 = 同一条腿**；换结构 / 换字段 / 换轴**不产生新腿**。
  - GBR 实证①：techindi 三字段互相关 **0.88~0.93**（同一模型的多输出）⇒ 整池只值 1 颗。
  - GBR 实证②：CDS 族 `spread ↔ recovery` **0.7616**（>0.7 同腿）⇒ 整族最大互不相关子集 = **1**。
- `self` 相关池**包含自己未提交的 alpha**：self max 高先看驱动记录是不是自己建的，再判「被占用」。
- **GBR 硬墙是 prod 不是 IS**（区域级结论）：IS 全闸候选常被 `PROD_CORRELATION` 拦（实证 techindi `O0J1A88J` prod/self 双 0.9297）。

---

## 预算参考

| 目的 | 成本 |
|---|---|
| 单数据集生死判定 | 1 批（8 条，双结构 × 跨族字段）|
| 数据集「正式判死」（D15 纪律） | **≥8 探针**（可分 1–2 批覆盖 4–8 构造）|
| 潜力确认（1.0–1.58 带） | +1~2 批（窗/轴/算子扫描）|
| 冲闸 | 2–5 批 |
| **判死一条错误路径的隐形成本** | 整个战役的期望产出——**所以第 0 步零成本筛选最值钱** |

---

## 本会话反例清单（GBR 实测，每条都是真金白银）

1. **1 探针判死 → 违反 D15，需补做 8 探针**：W1/W2 对 16 个处女数据集只跑 1 探针即判死，用户指出后补做 W14–W27（110 条）——结论未变（仍只有 CDS 活），但**过程不合规**。**新数据集判死必须 ≥8 探针。**
2. **字段类型错标 ⇒ 整批 FAIL**：`count_negative_*` 平台实为 MATRIX、本地/缓存表错标 VECTOR ⇒ 误用 `vec_*` ⇒ 3 条非法 ⇒ **8 条整批 FAIL**。**类型必须取平台 `get_datafields`。**
3. **`vector_neut` 不在 GBR 算子清单** ⇒ op-lint 拒批（清单 102 个）。
4. **`tail` 位置参写法整批 ERROR** ⇒ 命名参 `lower=/upper=/newval=`。
5. **骨架 R2 连拦 3 波**（单模板 62%~75% > 60%）⇒ 必须**重组骨架**（换外/内层算子），**不得用 `--param-sweep` 绕过多字段 sweep**。
6. **用错设置复现历史 alpha**：曾按区域缺省（decay 4 + SUBINDUSTRY）重跑，而记录实为 **decay 2 + STATISTICAL** ⇒ 只到 1.34（记录 1.95）。**复现历史 alpha 必须拉它自己的 settings。**
7. **`ts_backfill` 用在事件型字段上**：只适状态量；事件量会抹频率（GBR 实证 `ts_mean` 在事件型数据上 S 1.44→0.73）。
8. **只测一个结构**：本轮探针底座单一（house）⇒ 若某字段在 techindi 配方下更强会被错杀——**双结构是保底纪律**。
9. **★★★ 2 探针判死（2026-10-31，与第 1 条同源复发）**：用户限「`create_multi_simulation` 2 条/批」后，把「单批宽度」误当成「判死样本量」，`other250`（12 字段只看 2 个）、`news48` D0、`other567` / `other169` / `other327` / `other546` / `other571` 全部 2 探针即记判死 ⇒ **「OTHER 塔 13 数据集全灭」多数是误杀**。**「每波探针位 2」× 「判死需 8 探针」= 必须连发 4 批。**
10. **★★★ 跳过栖息地闸（2026-10-31）**：`insider_trx_matrix` 直接派了 2 批 4 条才去翻论坛，才发现 GBR 只有 TOP700、信号住非流动小票。**`get_platform_setting_options()` 一次调用就能在 0 仿真成本下判死。**第 0.5 步是为这条反例写的。
11. **★★ 结论表述滑坡（2026-10-31）**：「2 个字段全灭」被写成「数据集判死」，并据此停止搜索。**字段数 ≠ 数据集判死依据**；写结论时必须同时写「测了几个字段 / 占该数据集字段总数的比例 / 覆盖了几个机制族」。**覆盖率 < 50% 的负面结论一律不得称「判死」。**
12. **★★★ 不做数据集级覆盖率普查（2026-10-31）**：整个会话都在「13 个 OTHER 数据集」这个错误基数上做百分比，而 `get_datasets(category="other")` 实际返回 **41 个**；其中 **29 个 `coverage=0.0`**（TOP700 下无数据），我却计划给其中 5 个各补 6 条探针 = **30 条仿真白烧**。**根因是只按「记得测过谁」组织清单，而不是按平台返回的全集组织。**⇒ 每进一个新 category，第一件事是 `get_datasets` 拉全集数清 `总数 / coverage>0 / coverage=0`，再谈判死比例。

---

## 并发受限下的派发节奏（2026-10-31 补）

用户级约束常见为「`create_multi_simulation` 每批 ≤2 条」。适配方式：

1. **宽度受限 ⇒ 长度补偿**：2 条/批，但同一数据集连发 4 批，凑满 8 探针。
2. **不要在批间等结论**：4 批是 4 个不同构造，彼此独立，串行等待纯浪费墙钟。
3. **`batch_status` 收批后立刻发下一批**，把「收批」和「发批」交替进行，而非「发-等-收-再发」。
4. **账号级 7 槽与兄弟会话共享** ⇒ 429 是常态，不是失败；隔 30–60s 重试即可。
5. **判死前先数批**：`已发批数 × 2 ≥ 8` 才允许写 `CONFIRMED-DEAD`。
