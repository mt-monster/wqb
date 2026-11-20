# 字段画像 → 模板映射：静态元数据 × 六法实证的集成方法

> 建立：2026-11-17 ｜ 触发：用户「有了字段全表后，要按 brain-datafield-exploration-general 做详细字段画像；
> 评估静态摘抄 vs 六法实证两种方法的好处，集成在一起，目标是作为后面匹配模板有实际作用」
> 实证样例：`tracking/KOR/reference/datasets/fund_holdings_panel.md` §9（`holder_account_total` 完整六法读数）

## 一、两种方法各自的优点（不是二选一）

| 方法 | 优点 | 局限 | 成本 |
|---|---|---|---|
| **静态元数据摘抄**<br>`get_datafields` type/cov/aC/description + 五问推定 | 零配额、**全字段可一次铺开**（156 字段也能全画）；定方向快（存量→变化率、事件→门控、VECTOR→`vec_*`） | 只是**推定**，不能当结论。实测反例：description 写"季度披露驱动"⇒推定窗口≥63d，但六法测出 66 日内 91% 的股票值变过 ⇒ 窗口下限可下调到 22d | 0 |
| **六法实证体检**<br>`brain-datafield-exploration-general` 在线最小集 / 离线包 | 给出**静态看不出的硬约束**：非零占比（是否要 `trade_when`）、更新频率（窗口下限）、分布形态（是否 winsorize/zscore）、量纲（是否 rank） | 贵（一个字段 ≈ 6–13 条仿真），**不能全字段跑**；Long Count 读数要逐条 `get_alpha_details` | 6–13 条/字段 |

**关键教训**：只做静态就把推定当结论（踩过）；只做六法跑不全（1000+ 字段集跑不起）。必须集成。

## 二、集成方法：两段式，产出「字段 → 模板白名单」

```
第一段（静态，全字段）→ 圈候选模板集合
第二段（六法，仅主信号字段）→ 裁决候选模板的准入/排除
产物 = 合法模板白名单 + 排除模板（带理由）
```

### 字段画像档案的集成表模板（落 `tracking/<R>/reference/datasets/<ds>.md`）

| 列 | 来源 | 作用 |
|---|---|---|
| 静态读数 | type/cov/aC/description + 五问**推定** | 圈候选模板 |
| 六法实测 | 在线最小集 / 离线包的 **Long Count** | 裁决准入/排除 |
| 合法模板白名单 | 两者合成 | **模板匹配的直接输入** |
| 排除模板 + 理由 | 六法反证 | 防止重复试已证伪几何 |

### 六法 → 模板裁决规则表

| 六法 | 读数 | 对模板的裁决 |
|---|---|---|
| 法1 覆盖 | Long Count / universe | <0.4 ⇒ 必须 backfill；≥0.5 ⇒ 排除 backfill |
| 法2 非零 | `F!=0` count vs 法1 count | 差异大 ⇒ `trade_when` 门控；无差异 ⇒ **排除门控** |
| 法3 频率 | `ts_std_dev(F,5/22/66)!=0` count | 高频（66日≈覆盖）⇒ 允许短窗 22d；季频（仅66日为真）⇒ 窗口≥63d |
| 法4 量纲 | `F/ts_mean(F,252)` 分布 | 跨度大 ⇒ `rank`/`ts_zscore` 去量纲 |
| 法5 中心 | `ts_mean(F,252)>0` | 单边恒正 ⇒ `ts_delta`/`ts_zscore`，**禁裸水平** |
| 法6 分布 | `zscore(F)>0/1/2` count vs 正态 50/16/2.3% | 右偏/厚尾 ⇒ 先 rank，避裸 `ts_zscore`；`ceiling` ⇒ winsorize |

## 三、实证样例：`holder_account_total`（KOR/TOP600/D1）

六法读数（批次 `2AiZ8Ulq4qN9Sk15SWiTPQK` + `15FM8WbRK4N8aqon2RyBzkY`，NONE/d0/P0Y0M0D）：

| 法 | 读数 | 静态推定 | 实测修正 |
|---|---|---|---|
| 1 覆盖 | 527/600=88% | cov 0.9553 | 吻合 |
| 2 非零 | 527→527，零≈0 | 看不出 | **排除 trade_when** |
| 3 频率 | 66日 481/527=91% | "季频⇒≥63d" | **允许 22d 短窗** |
| 4 量纲 | 63%高于年均值 | 10⁰–10³ | 中等跨度，需 rank |
| 5 中心 | 100% 恒正 + 71% 上升 | 看不出 | **用 ts_delta，禁裸水平** |
| 6 分布 | z>0 25%(正态50%)、z>2 5.7%(正态2.3%) | 看不出 | 右偏+厚尾，避裸 zscore |

**合成产物**：
- 合法模板白名单 = `group_rank(ts_delta(F, 22|66), sector|industry)`
- 排除模板 = `trade_when` 门控（零≈0）/ `ts_backfill`（覆盖88%）/ 裸水平 group_rank（单边恒正）/ 裸 ts_zscore（右偏厚尾）

**可迁移性**：同集 `count_institutional_holders_security`、`holder_account_total_active` 等**存量型广度字段**可直接套用此白名单，不必重新六法全跑（除非 cov/类型显著不同）。

## 四、两个工程坑（写进 skill 已同步）

1. **裸常数 UNITS 错**：`add(带单位字段, 0.0001)` / `abs(F)>1` / `ts_mean(F,252)>10` 报
   `expected Unit[...], found Unit[]`，预检查不出。正解：防除零直接 `divide`（同单位相除无量纲）；
   量纲/中心用同字段派生量（`F/ts_mean(F,252)`、`ts_mean(F,252)>ts_mean(F,1008)`）；阈值 0 可用。
2. **无离线包要挂 waiver**：KOR 4 集无 `field_inspect_kor_*.json`，按 skill §0 走在线并挂
   `waiver_inspect_KOR_all`（`NO_INPUT_AVAILABLE` + evidence），不静默跳过。

## 五、如何使用（给后续战役）

1. S1 字段扫描：对全字段做静态摘抄（type/cov/aC/description + 五问推定）。
2. 选出将当主信号的字段（每集 ≤3–5 个），对其跑六法最小集（6–13 条）。
3. 按本文章裁决表把每法读数转成"准入/排除"，填入字段档案集成表。
4. **S2 组模板时直接查白名单**，不再从零试模板；每次试了白名单外的模板要在档案追加排除理由。
5. 六法体检批不入库、不算战役波次（skill 规定），只读 Long Count 写档案。

## 六、★ 画像之后怎么组模板/alpha：论坛实证的「症状→模板」查表（2026-11-17）

**论坛工具诊断（2026-11-17）**：`search_forum_posts` 连续 3 次 30s 超时，但 `read_forum_post`
直读已知 article_id **完全正常（秒回）**——这是工具层的 partitioned failure（搜索路径坏、读取路径好），
不是「论坛不可达」。**纪律**：search 超时别急着改结论或写 forum_recon_negative；
先试 `read_forum_post` 直读归档里记的 article_id（本仓记忆/`gbr-unlit-tower-exhausted.md` 常存真实 id）。
本次直读 LC97552 新鲜度门帖 id=**43358755666967**（24赞），拿到全文（此前只有二手摘要）。来源：
- LC97552《【Alpha Idea】机构参与"新鲜度门"》id=43358755666967（24赞，IND/TOP500）— **本次 full text 直读**
- LC97552《CONCENTRATED WEIGHT 系统性排查与修复手册-1》2026-06-04（66 赞/29 评）→ `02_signal_patterns.md` §14
- 组合形态铁律 + 破闸旋钮 → `02_signal_patterns.md` §1–§2
- 结构-指标映射（KOR 实测）→ `02_signal_patterns.md` §"双腿价差"段

### 核心：模板不是凭空试，是「画像症状 → 查表 → 选模板」

| 画像症状（来自六法/静态） | 论坛/本仓实证的模板动作 | 依据 |
|---|---|---|
| **覆盖率 <40%** | **立即换数据集**（最高 ROI，别在算子上浪费变体） | 66赞手册 §14.2；本仓 fhp 流量族 0.8–33% 覆盖全部数据层排除 |
| **VECTOR 类型** | 先 `vec_*` 转标量 + `ts_backfill` | 66赞手册 §14.2；skill 类型先行 |
| **CONCENTRATED_WEIGHT FAIL**（持仓集中） | **`ts_backfill` 补覆盖率**，不是调 decay/truncation/中性化 | 66赞手册：KOR shortinterest38 实测降换手53%对CW零效果，补时间覆盖直接 PASS |
| **IS_LADDER / 2Y 不过** | `trade_when` 流动性门控（不是信号窗口）；或双层平滑 `add(短窗,长窗)`；⚠ 不要叠多个门 | 02 §2；HKG O0r7lJ1J ladder 1.56→2.08 |
| **分布右偏/厚尾**（法6） | `rank`/`ts_rank`/`group_rank` 均匀化；右尾用 `log`/winsorize；避裸 `ts_zscore` | 66赞手册 §14.3 分布控制 |
| **信号弱（S 不够）但结构干净** | 换**分组轴**（sector→industry→subindustry 逐档）或换**算子几何**，不是扫窗口/常数 | 02 §2 轴族最大杠杆；DEU 89 波墙一次推平 |
| **需要造正交变体**（降 self/prod） | 同一持仓腿 + 互斥 `trade_when` 触发时段 | 02 §6：同源字段 trade_when 正交化 SELF 0.31→0.23 |
| **多字段想合成一个信号** | 只能走**单一经济含义的价差** `subtract(rank(A),rank(B))` 或条件门控；⛔ 禁 `add` 等权拼腿 | 02 §1 组合形态铁律（wave189/190 七条"漂亮但违规"全废） |

### 结构-指标映射（论坛+本仓 KOR 实测，组模板时按缺哪项选结构）

| 想要改善的指标 | 选这个结构 |
|---|---|
| 提 **S**（全期强度） | `ts_rank` 双腿价差 |
| 提 **2Y**（近年） | `原始比率价差` / 流动性 `trade_when` 门 |
| 提 **稳健**（subU/CW） | `group_rank(·, industry)` 包裹 |
| 三项同时抬 | `慢×快价差` `subtract(group_rank(慢腿),group_rank(快腿))`（KOR 实测 S1.23→1.30/F0.89→0.94/2Y1.33→1.87） |

### 两条铁律（写模板前先过）
1. **一阶优先、算子 ≤3**，禁二阶套二阶（论坛实证 VF 0.9→0.1）。
2. **论坛给的算子名必须过 GHOST 校验 / `get_operators`**——66赞手册点名的 `ts_decay_exp_window`/`exp_window` 已下线，用了连坐整批 CANCELLED。

### ★ 活教材：LC97552 新鲜度门（本次 full text 直读，方法论比配方更值钱）

**抽象模板**（去掉具体字段/窗口，作者给的"可泛化接口"）：
```
trade_when(ts_arg_max(<PARTICIPATION_MEASURE>, G) < T,
    signed_power(ts_quantile(divide(<BUYER_FLOW>, ts_mean(<HOLDER_BASE>, M)), W, driver=gaussian), p),
    -1)
```
固定件（骨架勿删）：`ts_arg_max→trade_when` 门控链 + `divide(buyer, ts_mean(holder,M))` 比值核 + `ts_quantile(W,gaussian)` 自锚定分位。
可换接口：`PARTICIPATION_MEASURE`（任意参与人数计数）、`BUYER_FLOW`（增持者数/净买入）、`HOLDER_BASE`（持有人基数）、G/T/p（**需按数据披露节奏重扫**）。

**最重要的结论（用法边界 > 算子本身）**：
- `ts_arg_max` **作信号 = 摧毁器**（864/958/1097 反复验证：假信号多、时序噪声大）；
- `ts_arg_max` **作门控条件 = 冠军机制**（新鲜度阈值）。
⇒ 同一个算子换"用在哪一层"，成败相反。这解释了为什么我们过去试 ts_arg_max 作信号全灭。

**五代数维演进 = 一条完整证伪链**（50 批 414 次模拟，同字段族换骨架）：
侦察 `divide(buyers,holders)` 裸比值（结构不可行）→ ① `ts_corr(buyers,holders,66)` S0.38 证伪 → ② 美元净流 S0.44 证伪 → ③ 渗透率 S0.20 证伪 → ④ sellers 反向 S0.71 证伪 → **冠军：新鲜度门 S1.62/F1.37/2Y2.47（18项全PASS，已 OS）**。
⇒ **模板探索的正解**：同族内把「骨架维度」（比值/相关/流量/渗透/反向/门控）逐个证伪，而不是在同一骨架上扫窗口/常数。
**四条探索轴**（作者实测排序）：① 门控轴 G∈[66,180]×T∈[22,45]，66/33 与 90/33 甜点，66/22 崩到1.02、G≥120 单调衰减；② 分母轴 `ts_mean(B,72)` 是 FT>1.0 首破点（ts_sum 1.02 弱）；③ 凸化轴 `signed_power(1.6)`+W840 gaussian = 18 PASS；④ 曲线健康轴——分母窗增大→平滑度降、S升，{S≥1.58 ∧ np≥0.6 ∧ 2021>0 ∧ wTO≥5%} 四条件不可同时达（结构性跷跷板）。
**移植边界（作者原话）**：门控 G/T 在其它慢披露计数类区（GBR/EUR institutions）"系数必重扫、机制可推断"——本仓 GBR 实测**不可平移**（大盘覆盖饱和使门控变量无区分度），KOR fhp 30 臂也未复现；机制依赖"机构覆盖不足的小盘+慢披露"。

### 完整决策链（把本文件前面两段接起来）

```
静态全量摘抄（全字段，零配额）→ 圈候选模板方向
        ↓
六法实测（仅主信号字段）→ 定硬约束（覆盖/非零/频率/分布/量纲）
        ↓
症状→模板查表（上表）→ 选具体骨架 + 结构-指标映射定几何
        ↓
过组合形态铁律（禁 add 等权拼腿 / op≤3 / 算子实名）
        ↓
定向回测（一族一席、对比实验、先归因再推进）
        ↓
画像档案追加「该模板实测读数 + 有效/无效裁决」→ 下次查表更准
```

这把「论坛经验」从"读过就算"变成画像卡上的可执行查表项。

## 七、★ 全字段覆盖实测的意外发现：VECTOR 元数据 coverage 严重高估（2026-11-17）

对 `fund_holdings_panel` 全 30 字段跑法1（Long Count/600）后发现：
- **MATRIX 存量族**：元数据 cov 0.9553 ↔ 实测 527/600=88% —— 吻合，可信。
- **VECTOR 流量族**：元数据 cov 统一标 0.887（88.8%），但实测有效覆盖 **0.8%–33%**：
  聚合类（herfindahl_transactions/transaction_account/value_dist）199/600=33%、
  security_transaction 116、boundary_total 20、stable_boundary 15、boundary_usd 10、top_weighted_trans 8、large_trade **5**。
- **根因**：元数据 `coverage=0.887` 是"有该字段记录"的比例，不是"当天有非零值"的比例。稀疏事件型 VECTOR 绝大多数日子是空值。
- **影响**：这是"必须在线实测法1"的铁证——只看元数据会以为流量族覆盖良好，
  实际 0.8%–33% 的覆盖根本无法支撑全截面 alpha，且天然导致高换手+集中持仓（W4 五条 VECTOR 臂 TO 0.96–1.20 全爆、CW=1.0）。
- **规则**：VECTOR 字段的元数据 coverage **仅供排序，不作可用性判据**；必须用法1 Long Count 实测，
  <0.05（如 large_trade 5/600）直接数据层排除，0.05–0.4 只能作门控条件，>0.4 才进主信号模板匹配。
  完整数据见 `tracking/KOR/reference/datasets/fund_holdings_panel.md` §10。

相关：[[field-selection-rules]]、[[signal-structure-and-f-gate]]、brain-datafield-exploration-general SKILL.md「静态 × 六法集成」节。

## 八、★ 定向挖掘「每步查论坛」纪律（2026-11-19 用户指令）

用户原话：「你在做定向挖掘时，每一步都要查一下论坛有无相应的解决方案，再决策下一步怎么走」。
这把证据闸从「**开波前一次**」（EVID-FORUM / [[forum-paper-evidence-gate]]）升级为「**每个决策点一次**」。

**执行规格**：
1. **什么算「一步」**：每次要决定「继续同族 / 换杠杆 / 换字段 / 收口」之前，都是一步。典型决策点：
   探针波读数归因后、设置轴选型前、破闸杠杆选择前、prod 读数出来后、判死/收口前。
2. **查什么（按缺口症状选词）**：
   | 当前缺口 | 检索词（`search_forum_posts_local`，确定性通道） |
   |---|---|
   | prod 撞墙 | `production correlation` / `prod correlation` / `correlation reduce` |
   | F 不足 | `fitness` / `turnover` / `low sharpe` |
   | TO 异常 | `turnover` / `operators reduce turnover` |
   | S 天花板 | 数据集名 + 机制词（`institutional` / `holdings` / `ownership`） |
   | 形态选择 | 字段语义词（`bounded` / `event` / `sparse`）+ `template` / `模板` |
3. **判据**：命中帖必须给出「用/不用 + 理由」一行，写进当波报告；无命中记 `no_result`（`search_reliable=true` 才算无结果）。
4. **不重复**：同一步长内（同一决策点）不重复检索同一组词；跨波可复用 7 天内命中帖。

**本纪律首例执行（EUR institutions6，2026-11-19）**：
- 缺口=prod 0.8257 + F 数学约束；检索命中官方 **[BRAIN TIPS] How to Deal with High Production Correlation**：
  原文「换数据源或经济逻辑是最可靠的解；调窗口/权重/中性化本身很少能造出真正低相关的 alpha」；
- 另命中 **Operators used to reduce turnover**（25 赞）：降 TO 算子清单——但本族 TO 7.3% 已低于 12.5% 下限，**不适用**；
- 决策：institutions6 不再开新波，GrmbwmmO 存档等 prod 池漂移；若继续只允许「持仓集合改变型」杠杆（与本仓 §16.3 prod 限投档一致）。
