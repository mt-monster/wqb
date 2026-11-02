# GBR × other（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category other`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Other　**类别卡**：other

**涉及数据集**：acquisition_model、dl_riskfree_returns、insider_trx_matrix、other335、other455、other545

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GBR | 区域 settings.json |
| universe | TOP700 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 54 | 0 | 0 | 0 | 4 | 0 |

主要数据集（回测数）：other335（15）、insider_trx_matrix（12）、acquisition_model（12）、dl_riskfree_returns（8）、other545（7）

### S1 字段理解

- 数据集名会骗人：必读字段 description；稀疏高 valueScore 是陷阱
- 窗口（类别卡，均在白名单内）：daily 5/22；quarterly 66/252

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - name the priced risk first; the operator is secondary
  - 先按字段 description 判断经济含义，再套对应类别卡的思路（例：KOR other466 是财务比率 → fundamental；IND other532 是 Barra 特质收益 → 残差反转）
- **跨区结论**（KOR/EUR/DEU/GBR；negative）：other455 网络嵌入（n2v）族（证据：KOR RULES §G；EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS；DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923；GBR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize / vector_neut）入场（★ 2026-10-20 更正：'vector_neut' **平台可用**——本地算子清单缺它是假阳性，EUR 平台已用它交付 JjQmx9nm；'regression_neut' 仍非平台算子名）
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GBR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-ACQUISITION-MODEL-DEAD | acquisition_model_ma_target | acquisition_model 不再生成任何结构（各层级acquisition_likelihood/valuation/fundamental/size/credit/text全灭）；GBR M&A信号域判死 | acquisition_model | payload | <!-- lint:const-ok 证据原文 -->
| GBR-O455-N2V-PROBE-DEAD | other455_n2v_relation_pca | other455 N2V/PCA关系分量族不再生成（含其它分位/窗口组合）；GBR OTHER塔候选穷尽 | other455 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-OTHER-COMPLIANT-CEILING-20260922 | GBR OTHER-category compliant atoms (light OTHER tower) | GBR 不再投 dl_riskfree/other545/insider_trx 合规探针冲OTHER | — | keyword | <!-- lint:const-ok 证据原文 -->
| GBR-OTHER335-DIVIDEND-2Y-DEAD | other335_dividend_model | other335 dividend-model family not to be generated in GBR; GBR dividend-culture thesis did not survive 2022-23. | other335 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->

### ★ 2026-10-13 · GBR × OTHER 复访（techindi_model）：IS 全闸可复现，但「不同预测窗口 = 同一腿」

按用户「无计可施才换数据集」纪律，ANALYST 判死（见 [analyst.md](analyst.md)）后转向 OTHER（塔计数 1/3，**未点亮**）。

**配方（已验证，来自 `3qVP6pNO`）**：
`group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(add(ts_mean(ts_backfill(F,500),1), ts_mean(ts_backfill(F,500),60)), sector)),std=0.15), lambda_min=0, lambda_max=1, target_tvr=0.50), sector)`
@ **CROWDING / decay 2 / nanHandling ON / maxTrade ON / trunc 0.08**

| 字段 | alpha | S | F | TO | 2Y | sub | ra_failed |
|---|---|---:|---:|---:|---:|---:|---:|
| `tm_16_r1_r5_r10_rh_glb_d1_r10_q1` | `O0J1A88J` | **1.92** | **1.09** | 0.207 | **1.90** | 2.04 | **0** |
| `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` | `omo1EWLl` | **1.83** | **1.01** | 0.217 | **1.86** | 1.99 | **0** |

**★★ 但互相关把它们判回同一条腿**：
`compute_mutual_correlation([3qVP6pNO(已 ACTIVE), O0J1A88J, omo1EWLl])` → **0.9297 / 0.8814 / 0.9134**；`max_mutually_below_subset_size = 1`。
平台双端点核实 `O0J1A88J`：**prod 0.9297 FAIL ｜ self 0.9297 FAIL**。

⇒ **techindi 的「预测窗口 (r1/r5/r10) × 分位桶 (q2_p1 / q1)」不构成独立腿**；`3qVP6pNO` 已占该腿 ⇒ **OTHER 塔在 techindi 上无第 2 条腿**。
⇒ 该池的「未采 ALIVE 字段」（`r5_q1` 单信号 1.81 / `r10_q1` 1.75）虽 S/F 全闸，**仍是同腿**，不产生新增可提交槽位。
⇒ 反向桶弱变体（`q4_p1`）：S −0.37 / −0.90（方向反 + sub_LOW）。

**★ 选池判据在本塔的推论**：techindi_model 是**单一模型的多头输出**（同一 CNN/回归模型换预测窗口与分位桶）⇒ 对「一条腿一颗」的 RA 规则而言，**整池只值 1 颗**。凡「同一模型 × 多参数输出」形态的数据集，先做互相关聚类再谈「字段数」。

### 2026-10-13 晚场 · other169（CDS）深挖 —— GBR 处女池唯一活机制，但撞 2Y 墙

**发现路径**：全面画像（177 平台数据集 × 15,523 画像字段）→ 66 未点亮塔候选 → 16 机制探针筛选 → **只有 other169 的 CDS 信用价差活**。

**最佳构型（IS 近失，卡 LOW_2Y_SHARPE）**：
```
group_rank(ts_mean(vec_avg(mid_par_spread_basis_points), 66), subindustry)
@ GBR / TOP700 / D1 / decay 4 / SUBINDUSTRY / nanHandling ON / maxTrade ON / trunc 0.08
S 1.52（闸 1.58）｜ F 1.07 ✓ ｜ TO 0.0257（LOW_TURNOVER 实测通过）｜ sub 1.14 ✓ ｜ 2Y 1.57（闸 1.58，差 0.01）
```
机制解读：`mid_par_spread_basis_points` = CDS 中间价差（bp）。**正向 S** ⇒ 宽价差 → 高后续回报（信用风险溢价 / 深度反转，与 GBR value-tilt 一致）。全平台仅 aC=6（纯白空间）。

**★★★ 中性化闸线地图（区域级铁律，见 SKILL.md）**：本腿在 11 档中性化下实测——
| 中性化 | S | F | 2Y | 2Y 闸线 |
|---|---:|---:|---:|---:|
| **SUBINDUSTRY / SECTOR / INDUSTRY**（内置轴） | 1.52 / 1.45 / 1.32 | 1.07 / 1.08 / 0.90 | **1.57 / 1.40 / 1.31** | **1.58（宽）** |
| MARKET | 1.58 | 1.39 | 1.60 | 2.02 |
| **REVERSION_AND_MOMENTUM** | 1.66 | 1.45 | 1.67 | 2.02 |
| **CROWDING** | 1.72 | 1.54 | 1.73 | 2.02 |
| FAST / STATISTICAL / NONE / SLOW / SLOW_AND_FAST | 1.61 / 1.22 / 1.20 / 0.55 / 0.74 | — | 1.50 / 1.10 / 1.16 / 0.48 / 0.65 | ~2.02 |

⇒ **升 S 的因子中性化（CROWDING/R&M 把 S 推到 1.66~1.72）同时把 2Y 闸线抬到 2.02**。宽档下 2Y 天花板 1.57；严档下 2Y 最高 1.73。**两档皆不可通过。**

**全扫描穷尽（~65 条仿真）**：窗 5/22/44/55/66/77/88/132/210/252（甜点 66）；vev 聚合 avg/max/min/stddev/count；时序算子 mean/sum/delta/rank/quantile/decay_linear/zscore/ir/av_diff/max_diff/scale/**arg_max**/**days_from_last_change**/std_dev；外层 rank/zscore/zscore/winsorize(std2-6)/signed_power/tail/hump/divide/reverse；结构 双窗 add / 快慢 subtract / group_neutralize 内层 / ts_backfill / bucket / **group_cartesian_product**；分组轴 subindustry/industry/sector/bucket(cap)/bucket(recovery)/复合轴；字段 mid_par_spread/quote_spread/recovery/recrisk/tenor/upfront/pv173。**无一提过 base。**

**其它 CDS 字段**：`mid_quote_spread`（1.50/1.06/1.56）、`isda_assumed_recovery_percent`（1.53/1.11/1.42）、`oth169_recrisk`（1.44/0.99/1.51）、`reverse(days_from_last_change)`（1.39/1.03/1.33，价差变动新鲜度另机制）。**互相关：spread↔recovery 0.7616（>0.7 同腿）⇒ CDS 族最大互不相关子集 = 1 颗。**

**未点亮塔处女池 16 机制筛选全表**（每集 1 探针，公共底座 `group_rank(..., subindustry)`）：仅 CDS 活；余 15 个（ESG 评级 / 分析师创新度 / 预期分歧 / UK 内部人 / 基金做空情绪 / 借券利率波动 / 维基关注度 / 供应链占比 / 新闻负情绪 / 并购事件 / 电话会情绪 / 激进投资者事件 / 机构建仓 / 期权 IV / 招聘活跃）其中 **8 个 TO < 0.05 近静态**（状态量/评级类在 GBR TOP700 天生低换手），S 全在 −0.71~0.55。

**工程坑**：`tail` 只接 **1 个位置参 + 命名参**（`tail(x, lower=..., upper=..., newval=...)`）；位置参写法（`tail(x,0.1,0.9,0.5)`）⇒ 整批 ERROR（连坐）。

### 2026-10-13 深夜 · 处女池「8 探针」正式深挖（W14–W27，110 条）—— 全域封闭

**起因**：用户指出「16 数据集仅 1 探针即判死」违反 D15。补做 **23 个处女数据集 × 4–10 构造 = 110 条**，结论：**除 CDS 外无第二活机制**（全部 ≤0.90）。

| 数据集（类别） | 探针 | 最好 S | 判死 |
|---|---:|---:|---|
| `option1` 期权 IV 曲面（option）| 8 | 0.55 | ✓ |
| `fund_holdings_panel` 机构资金流（institutions，cov 0.93）| 8 | 0.39 | ✓ |
| `insiders12` UK 内部人（insiders）| 4 | 0.71（反向净买入）| ✓ |
| `shortinterest3` 证券借贷（shortinterest）| 4 | −0.89（贷出市值）| ✓ |
| `institutions25` 基金做空（institutions）| 2+6 | 0.81（反向情绪）| ✓ |
| `event_ml_signals` 事件旗标 / `ai_news_scores` / `macro27` | 2/2/2 | 0.24 / 0.08 / 0.11 | ✓ |
| `news3` 道琼斯新闻情绪（news）| 8 | 0.30 | ✓ |
| `other571` 维基关注度（other）| 8 | 0.37（异常关注度）| ✓ |
| `other696` 电话会事件计数（other）| 8 | 0.48 | ✓ |
| `earningscall_sentiment` 电话会极性（other）| 8 | 0.42 | ✓ |
| `other128` 高管薪酬/信心（other）| 8 | 0.29（多近静态 TO 0.013~0.016）| ✓ |
| `other546` 机构网络 / `other635` 标题神经情绪 / `pv71` 网络关系 | 3/1/1 | −0.39 / −0.26 / −0.11 | ✓ |
| `risk68` 特异风险 / `pv13` PageRank·HITS / `analyst16` 预期分歧 | 3/2/3 | −0.69 / 0.11 / 0.38 | ✓ |
| **`search_interest` Google 检索兴趣（other）** | 2+8 | **0.90**（全池最高；2Y 0.10）| ✓ |
| `sentiment27` 网站流量排名（sentiment，cov 0.79）/ `imbalance5` / `socialmedia5` | 6/1/1 | 0.34 / 0.11 / 0.12 | ✓ |

**★ 三坑（本轮踩中）**：
1. **字段类型错标 ⇒ 整批 FAIL 连坐**：`count_negative_*` 平台实为 **MATRIX**，本地/缓存字段表错标 **VECTOR** ⇒ 误用 `vec_sum/vec_avg` ⇒ 3 条非法 ⇒ 8 条整批 FAIL。**纪律：VECTOR/MATRIX 必须取平台实时 `get_datafields`，不信本地表/缓存 dump。**
2. **`vector_neut` 不在 GBR 平台算子清单**（op-lint 拒批）；当前 102 个算子清单为准。
3. **骨架审计 R2（单体模板 ≤60%）连拦 3 波** ⇒ 按纪律**重组骨架**（不得用 `--param-sweep` 绕过多字段 sweep）。

### 2026-10-14 凌晨 · CDS 家族第二腿发现 + 2Y 闸线分档破解（W-A~W-H，约 50 条）

**起因**：按新定的 [probe-sop.md](_probe-sop.md) 补「双结构纪律」——此前 39 数据集筛选只用 house 底座（结构 A），未用 techindi 配方（结构 B）。

**① 结构 B（techindi 配方）复访 8 个非 CDS 强字段 ⇒ 全部仍弱**（search_interest 0.73 / 维基 0.43·2Y1.68 / 机构做空 −0.02 / IV 0.41 / 新闻恐惧 −0.19 / 内部人 −0.01）⇒ **非 CDS 池在双结构下确认无救**。

**② ★★ 新发现：`isda_assumed_recovery_percent`（回收率）在 sector 轴上是**独立于价差的更强腿**——
| 构型 | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| `group_rank(ts_mean(vec_avg(recovery),88), sector)` @ **CROWDING** | **1.86** | **1.72** | 0.035 | **1.82** |
| 同上 @ FAST（w88） | 1.84 | 1.23 | 0.073 | 1.57 |
| 同上 @ CROWDING（w22） | 2.01 | 1.41 | 0.0755 | 1.79 |
| `...recovery...66, sector` @ MARKET | 1.73 | 1.56 | 0.025 | 1.68 |
| 对照：价差 `...spread...66, sector` @ CROWDING | 1.53 | 1.40 | 0.030 | 1.53 |
⚠ **但互相关实测 spread↔recovery = 0.7616（>0.7）⇒ 仍是同一条腿**，不产生第二颗。

**③ ★★★ 2Y 闸线「分档」破解（本区最重要的机制结论，详见 [SKILL.md](../SKILL.md) ②）**：
显示 limit 是**「当前正在卡的那一档」**：`2Y<1.58 ⇒ limit 1.58`；`2Y≥1.58 ⇒ limit 2.02`（完美阶跃，15 个样本）。
⇒ **真正过闸需 2Y ≥ 2.02**；例外是**高换手 alpha 档位更低**（techindi TO 0.207 以 2Y 1.90 通过）。
⇒ 本腿 TO 天花板 ≈0.04（信号天然慢，`ts_target_tvr_decay(target_tvr=0.5)` 也拉不动，decay 0/1/2 无差）⇒ **进不了高换手低档**。
**本腿最好成绩：S 1.86 / F 1.72 / 2Y 1.82（CROWDING + sector 轴 + recovery w88）⇒ 2Y 差 0.20。**

**④ 逐条读 limit 的方法**（判定强制步骤）：
```python
aj = GET /alphas/{id}; i = aj["is"]   # metrics 在 is.sharpe / is.turnover / is.twoYearSharpe
lim = [c for c in i["checks"] if c["name"]=="LOW_2Y_SHARPE"]  # 含 value + limit
```
⚠ `harvest` 的 `2Y_OK/2Y_DEAD` 用静态 1.58 阈值，**对严档会误判**。

### ★★★★ 2026-10-31 · OTHER 数据集「判死」证据强度复核（本轮最重要的元结论）

**背景**：本轮把「OTHER 塔 13 个数据集全灭」当成结论去汇报，复核后发现**多数不成立**——根因是把用户「`create_multi_simulation` 2 条/批」的**单批宽度**误当成**判死样本量**。判死纪律（D15）要求 **≥8 探针 + 双结构**。

**判死标签三档**（定义见 [_probe-sop.md](_probe-sop.md) 第 2 步）：`PROBE-KILLED`（不可信，<8 探针）/ `CONFIRMED-DEAD`（≥8 探针双结构）/ `STRUCTURAL-DEAD`（+ 跨区对照）。

| 数据集 | 本轮/历史探针数 | 字段覆盖 | 最好 S | 原标签 | **应改标签** |
|---|---:|---|---:|---|---|
| `insider_trx_matrix` | **4**（4 个机制族）| 4/33 字段，但**机制族覆盖 4/4** | 0.95 | 判死 | ✅ **`STRUCTURAL-DEAD`** — 跨区对照 USA `ILLIQUID_MINVOL1M` 2.89 vs GBR `TOP700` 0.95，差 3.0× |
| `insider_matrix` | 0（同源继承）| — | — | 判死 | ✅ **`STRUCTURAL-DEAD`** — 与上条同源、同 33 字段、覆盖率 0.6061 vs 0.6005 |
| `dl_riskfree_returns` | ≥8（历史波）| 40 字段**全标签类** | — | 判死 | ✅ **`CONFIRMED-DEAD`** — 第 0 步语义闸零成本判死，合规 |
| `other47` | **8**（8 模板）| 9/18 = 50% | 未记录 | 判死 | ✅ **`CONFIRMED-DEAD`** — 本区**唯一合规**的探针判死 |
| **`other250`** | **8**（5 机制族 / 3 换手档）| **5/12** | **0.34** | 判死 | ✅ **`CONFIRMED-DEAD`（2026-10-31 已补满）** — 水平量 TO 2.1–2.7% / techindi 12% / 变化率 45–62% 三档全灭 |
| `other567` / `other169` / `other327` / `other546` / `other571` | **0 有效** | — | — | 判死 | ✅ **`STRUCTURAL-DEAD`（2026-10-31 改判）** — 全部 `coverage = 0.0`，GBR TOP700 下平台无数据。**原计划各补 6 探针 = 30 条仿真白烧，已撤销** |
| **`stock_cluster_dl`** | **8**（5 结构 × 2 字段）| 5/5（含 `_9` coverage 1.0）| **0.14**（最高 \|S\| 0.23）| — | ✅ **`CONFIRMED-DEAD`（2026-10-31 首测即满 8 探针）** — 水平量 / 变化率 / techindi / `ts_av_diff`252 / `ts_zscore`252 五结构全灭，换手档 2.98%–24.10% |
| **`other545`** | **8**（2026-10-31 首测）| 3/3 信号字段（`_mktcap` 作分母）| **0.30** | — | ✅ **`CONFIRMED-DEAD`** — 见下方专节；★ 附带发现 SUB 0.70/0.71（全会话最高）但主 S 为负 |
| `news48`（D0） | 2 | 2/22 字段 | 0.08 | 判死 | ⚠️ **`PROBE-KILLED`**（D0 已由 USA 31 批独立证伪，见 SKILL.md，故 D0 结论不变，但 **news48 在 D1 未被测过**）|
| `other455` / `other384` / `order_book_imbalance` / `euro_equity_imbalance` / `other699` | 历史（未核）| — | — | 判死 | ❓ **待核**：查 `backtest_results` 计该数据集行数，≥8 才升 `CONFIRMED-DEAD` |

**★★★★ 2026-10-31 · OTHER 塔数据集普查（本轮推翻「13 个」这个基数）**

此前全部百分比都建立在「OTHER 塔 13 个数据集」上，**这个数字是错的**。`get_datasets(region="GBR", delay=1, universe="TOP700", category="other")` 实际返回 **41 个**：

| 分层 | 个数 | 明细 |
|---|---:|---|
| **总数据集** | **41** | — |
| **`coverage > 0`（有数据，可打）** | **12** | `other455` 0.9381 / `dl_riskfree_returns` 0.7645 / `insider_matrix` 0.6061 / `insider_trx_matrix` 0.6005 / `other250` 0.5206 / `other47` 0.5171 / **`other545` 0.4878** / `stock_cluster_dl` 0.4739 / `other699` 0.3439 / `other384` 0.214 / `order_book_imbalance` 0.1798 / `euro_equity_imbalance` 0.1568 |
| **`coverage = 0.0`（平台无数据）** | **29** | `acquisition_model` / `ai_news_scores` / `earningscall_sentiment` / `event_ml_signals` / `event_relation` / `event_sentiment_signals` / `news_sentiment_nlp` / `other128` / `other169` / `other296` / `other315` / `other323` / `other327` / `other335` / `other424` / `other425` / `other436` / `other546` / `other566` / `other567` / `other571` / `other635` / `other696` / `other734` / `other78` / `search_interest` / `stock_search_trends` / `techindi_model` / `workforce_flow_skills` |

**⇒ 12 个有覆盖的数据集里，结论分布**：
- `STRUCTURAL-DEAD` **2**：`insider_trx_matrix` / `insider_matrix`（栖息地：GBR 只有 TOP700）
- `CONFIRMED-DEAD` **8**：`other47` / `other250` / `stock_cluster_dl` / `other545` / `dl_riskfree_returns` / `other455` / `other384` / `other699`
- 历史判死待核 **2**：`order_book_imbalance` / `euro_equity_imbalance`
- **待打 0 个**

**★★★ 结论：OTHER 塔在 GBR D1 已全域穷尽**，且这个结论这次建立在「41 个全集普查 + 12 个有覆盖者逐一判决」上，不是「记得测过谁」。

**★ 反例（本轮最大的浪费苗头）**：`other567` / `other169` / `other327` / `other546` / `other571` 曾被列为「待补 6 探针 × 5 = 30 条仿真」。**它们 `coverage` 全是 0.0**——补探针只会得到一堆 `turnover 0% / pnl 0` 的空结果，然后把「无数据」误记成「无信号」。**每次动新 category 的第一件事是数 `总数 / coverage>0 / coverage=0`。**

### ★★★★★ 2026-10-31 · `other545`（Linked Firms Momentum / NEMO 2.0）8 探针完整账本

**字段**（4 个，**全 VECTOR**，必须 `vec_avg` 折叠）：

| 字段 | 语义 | 用途 |
|---|---|---|
| `oth545_score` | NEMO 2.0 综合分（7 个网络动量信号的聚合）| 主信号 |
| `oth545_pln_omen` | NLP 文本挖掘关联的网络动量 | 主信号 |
| `oth545_mpd` | 机器学习动态价格动量 | 主信号 / 对照 |
| `oth545_mktcap` | 市值（USD）| **规模分母，不是信号** |

**设置**：`INDUSTRY` + decay 10 + trunc 0.05 + `nanHandling ON` + `maxTrade OFF` + `unit_handling VERIFY`，全部 GBR/TOP700/D1。

| # | 结构 | 表达式 | alpha | S | F | 2Y | **SUB** | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | 综合分行业水平 | `group_rank(vec_avg(oth545_score), industry)` | `58E7xaJN` | −0.07 | −0.01 | −0.16 | **0.70** | 4.51% |
| 2 | 综合分行业 22 日改善 | `group_rank(ts_delta(vec_avg(oth545_score), 22), industry)` | `N1NW0gPg` | −0.12 | −0.03 | −0.32 | **0.71** | 7.11% |
| 3 | 纯 ML 价格动量 | `rank(vec_avg(oth545_mpd))` | `qMLk8gv1` | 0.14 | 0.04 | **−0.80** | 0.21 | 9.86% |
| 4 | 纯 NLP 网络动量 | `rank(vec_avg(oth545_pln_omen))` | `QPvrMEqQ` | **0.21** | 0.08 | **0.91** | 0.16 | 6.02% |
| 5 | 网络动量 − 价格动量 | `subtract(rank(pln_omen), rank(mpd))` | `E5601le0` | 0.03 | 0.00 | 0.86 | 0.02 | 7.97% |
| 6 | 综合分 − 市值（规模残差）| `subtract(rank(score), rank(mktcap))` | `rKR6YjPo` | **0.30** | **0.13** | −0.26 | 0.37 | 6.32% |
| 7 | 综合分 252 日时序 z | `rank(ts_zscore(vec_avg(oth545_score), 252))` | `KPJY3V8N` | 0.17 | 0.05 | −0.07 | 0.18 | 9.82% |
| 8 | 综合分 66 日均值 | `rank(ts_mean(vec_avg(oth545_score), 66))` | `N1NW0Kj8` | 0.18 | 0.05 | −0.03 | 0.31 | **2.51%** |

**判死读数（满 8 探针）**：最高 S **0.30**（#6），8 个结构里 2 个为负、1 个近零（0.03）、5 个落在 0.14–0.30。**无一接近 0.5 判死阈值，更远低于 1.58 提交闸。**

**★★★ 唯一有价值的正面线索：`SUB = 0.70 / 0.71` 是全 GBR 会话最高，同时主 S 为负（−0.07 / −0.12）。**

- 这不是「信号弱」，是「**信号住在更小的票里**」——子宇宙表现优异、全宇宙被大票稀释/反向。
- **这正是第 0.5a 栖息地闸说的情形**：GBR 只有 TOP700、无更小 universe 可下沉 ⇒ 结构性不可用。
- **记录价值**：若未来 GBR 开放 TOP500 以下档位（或搬到 USA `ILLIQUID_MINVOL1M` 重测），`oth545_score` 是**值得第一个重试的字段**。GBR 内的结论不外推。

**★★ 另一条负面教训（强化既有第 10 条铁律）**：`oth545_mktcap` 是**市值**，§1 已经反复验证「价值族做横截面信号弱一个数量级」。本轮 #6「分数 − 市值排名」拿到全波最高 S 0.30，**但它的经济含义是「小盘倾斜」，不是「网络动量 alpha」**——市值排名的贡献大于分数本身。这类「用市值当腿」的构造在 GBR TOP700 上等于赌小盘，而 GBR 只有大盘 ⇒ 上限很低。

**★★ 待补课清单（2026-10-31 全面重写）**

| 优先 | 对象 | 待补 | 说明 |
|---|---|---|---|
| — | **（无）** | — | OTHER 塔 12 个有覆盖数据集已全部判决；29 个 `coverage=0` 无需探针 |

**⇒ OTHER 塔在 GBR D1 战役结束。** 若仍要点亮 OTHER 塔（需 3 条，现有 1 条），只剩三条路：①提交已有 1 条以外的非 OTHER 塔 alpha 换取名额（不解决 OTHER 本身）；②等数据集更新（`coverage` 由 0 变正）；③换区（OTHER 塔在 USA/GLB 有 illiquid universe）。**不要再在 GBR 的 OTHER category 里开新波。**

**★★ 判死台账写法要求（新增）**：每行必须写清「探针数 / 覆盖了几个字段 / 覆盖了几个机制族 / 最好读数 / 标签」。**只写「判死」三个字的行一律视为无效台账**——下一波无法判断是真死还是没测够。

<!-- profiles:manual:end -->
