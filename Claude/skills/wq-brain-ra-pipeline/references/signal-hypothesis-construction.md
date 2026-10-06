# 步 4 前置细则：字段分类（L1–L3.5）与候选信号形态的科学构建（L4）

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 3 / 步 4。本文件回答**两个被混为一谈、其实必须分开的问题**：
> ① **字段分类**（这字段是什么、能不能当信号）——止于「划边界」，**不产信号**；
> ② **候选信号形态构建**（怎么从字段里长出一个可证伪的信号）——这才是产出的地方。
>
> 2026-10-01 定案（出处：`output_report/field_analysis_demo_model264_20261001.md` GBR/model264 全流程实测）。
> 反面教材：把 L3 归类当终点 → 拿到一堆干净的字段却不知道下一步做什么；或跳过 L3.5 直接拍脑袋拼表达式 → 撞上组合形态铁律。

## 0. 四层漏斗：每层的输入 / 产出 / 损耗 / 归属步

| 层 | 名称 | 输入 → 产出 | 谁执行 | 成本 | 是否产信号 |
|---|---|---|---|---|---|
| **L1** | 数据集级 | 众候选 → 白名单数据集 | 步 1–2 | 零配额 | ✗ |
| **L2** | 字段级 | 数据集 → typed catalog（类型/覆盖/users） | 步 3 `workflow_campaign(S1)` | 零配额 | ✗ |
| **L3** | 语义归类 | catalog → 信号白名单 / 非信号黑名单 | 步 3 `field_semantic_classify.py` | 零配额秒级 | ✗ |
| **L3.5** | **结构族** | 信号字段 → 同源字段族 + 角色 | 步 3 `field_semantic_classify.py`（同一命令，`families` 段） | 零配额秒级 | ✗ |
| **L4** | **机制概念** | 族 → 可证伪假设 + 表达式骨架 | 步 4（本文件的 §2–§5） | 配额从探针开始 | **✓ 唯一产信号的层** |

**关键认知**：L1–L3.5 **全部零配额、全部不产信号**。它们的作用是把「可探索空间」从 O(全部字段) 压到 O(有经济含义的族)。
**真正的配额消耗从 L4 的探针开始**——所以 L1–L3.5 一定要跑满、跑透，不要急着进 L4。

> ⚠ **L3.5 是 2026-10-01 新增的一层**。此前 L3 直接把字段交给 L4，缺了「同源字段聚族」这一步，
> 导致 model264 的 `mdl264_<指标>_l1/l2/l3/_class/_se` 被当作 380 个独立字段，
> 看不出「36 个三分类概率族」这个结构。**族是 L4 机制推理的最小单位，不是单个字段。**

### 0.1 ★ L3.5 覆盖面边界与退化路径（2026-10-01 实测，开战役前必读）

**族识别靠字段名的角色后缀**（`_l1/_l2/_l3` 三分类、`_class`、`_se`、`_q1-5`、统计量、
`_fy1-4` 预测期、`_1d/_5d/_20d` 窗口、`_up/_down` 方向、`_high/_low` 端点）。
**没有这些后缀的字段无法聚族**——这是数据集的客观命名结构，不是分类器缺陷。

全库 414 个 `s1_semantic_<ds>` 台账实测：

| 类型 | 数据集例（族数，2026-10-01 实测） | 能否聚族 |
|---|---|---|
| **角色后缀型衍生集** | `other460`(EUR **418**) / `analyst15`(ASI **258**) / `model264`(GBR **160**) / `model109`(KOR **46**) | ✅ 族丰富，L4 直接可用 |
| **原生集** | `fundamental17`(KOR，336 信号字段 → **1**) / `pv30`(690 → **0**) / `news38`(45 → **0**) / `analyst_consensus`(2298 → **0**) | ✗ 空族是**正确结果** |

⇒ **族非空约占 31%**（129/414 台账；补入期限/窗口/方向/端点四类后缀前仅 18.6%）。
因此 L4 的第一步必须先判：

```
families 非空  → 按族走五步法（§2），族是推理单位
families 为空  → 退化：用 L3 的 by_category（经济大类）当聚合轴，
                 在每个大类内做形态枚举（H1–H4），不要假装还有族
```

**三个易踩的坑**：
1. **不许为了"凑出族"硬堆后缀规则**——实测给原生集补 4 类后缀后 `fundamental17` 仅 0→1 族、
   `pv30/news38` 仍 0；继续加规则就是过拟合，聚出来的族没有经济学含义，比没有族更糟。
2. **"族为空" ≠ "要补做"**。判定台账要不要重跑，看的是**台账是否由含 L3.5 的版本生成**
   （即 `family_stats` / `families` 两个键是否存在——**直接查台账键**即可；
   不要再去找某个 `semantic_ledger` 模块做口径校验，那个模块从未落地，`ledger_has_l35` 也不存在），
   不是看族是否非空。按"族为空"判补做会让原生集**永不幂等**（每次 S1 都重跑）。
3. **空族不等于数据集没价值**——`analyst_consensus` 2298 个信号字段照样能挖，
   只是聚合轴从"族"换成"经济大类"。

## 1. L3 语义归类 + L3.5 结构族（步 3 必做，GEM 之前）

```
python tools/field_semantic_classify.py --region $REGION --dataset $DS --write-ledger
#   产出 ledger `s1_semantic_<ds>`，含三段：
#     signal_fields / blocked_fields / by_category      （L3）
#     families / family_stats                           （L3.5，2026-10-01 新增）
```

### 1.1 L3：非信号黑名单 + 经济大类

非信号黑名单（名字规则 + 描述文规则双轨）：货币/报表币种代码、汇率换算（叉乘多为恒等式）、
标识符（country / iso / ticker / cusip / isin / gvkey）、分类码与标志位、日期期间口径、股份类别标签。

**两条已付学费的教训（改动规则前必读）**：
- `is_` / `_flag$` **不能按名字子串判**——`oth466_is_ebit_oper_q`（Income Statement EBIT，users=248）被误杀，other466 上 22% 字段误判。**缩写歧义必须看描述文**。
- 裸 `\bindicator\b` / `\bflag\b` **不能判布尔位**——技术分析指标（Bollinger Bands / Negative Volume Index / **Altman Z-score** / Chaikin Money Flow）描述里都含 "indicator"，model109 误杀 51/539。**必须出现显式布尔措辞**（"indicator denoting whether" / "equals 1" / "1 if … 0 otherwise"）。

经济大类（信号字段分桶）：`valuation / profitability / growth / cash_quality / leverage_solvency /
efficiency / liquidity_risk / size_level / per_share / dividend / other`。

**技术指标大类（2026-10-01 新增，前置拦截）**：`tech_trend / tech_momentum / tech_volume / tech_volatility`。
- **为什么新增**：GBR/model264 演示中 304 个技术指标（Bollinger / ADL / Amihud / Money Flow / Stochastic）
  描述里含 `change` / `trend`，被 `growth` 规则先命中 → **全部误归「成长/趋势」**。
- **修法**：`TECHNICAL_CATEGORIES` 插在 `ECON_CATEGORIES` **之前**匹配（顺序 = 优先级）。
- **实测**：model264 修复后 `growth` 从 304 降到 248，另分出 `tech_volume 24 / tech_trend 20 / tech_momentum 12`。

### 1.2 L3.5：结构族识别（L4 的输入）

**族 = 同一底层量的不同表征**。后缀命中 `FAMILY_SUFFIX_PATTERNS` 即属族，**族键 = 剥离全部后缀后的基名**。

| 后缀 | 角色 | 说明 |
|---|---|---|
| `_l1` | `P(fall)` | 三分类概率·下跌 |
| `_l2` | `P(neutral)` | 三分类概率·中性 |
| `_l3` | `P(up)` | 三分类概率·上涨 |
| `_class` | 三分类标签 | 众数类标签 |
| `_se` | 预期口径 | 版本标识 |
| `_q1..q5` | 分位数 | |
| `_mean/_std/_min/_max/_median` | 统计量 | |

**实测（GBR/model264）**：380 信号字段 → **161 族，其中 36 个三分类概率族全部齐全**
（`max_ac` 最高 `mdl264_eps_sur_decay`=6，`max_users` 最高 `mdl264_bookp`=3）。

> ⚠ **族键必须剥离「全部」后缀，不能遇第一个后缀就返回**。首版实现遇 `_class` 提前返回，
> 导致 `mdl264_eps_sur_decay_l1` 与 `..._class` 落进**不同族**，三分类族只认出 6 个（应为 36）。
> 这是 L3.5 最容易写错的地方。

### 1.3 fail-closed 边界（不要高估 L3 的强制力）

| 位置 | 行为 | 由谁保证 |
|---|---|---|
| 步 5 `wave_gate.py` 闸 SEM | 缺 `s1_semantic_<ds>` → **exit 2 整波阻断**；命中黑名单字段的表达式**直接剔出** | **代码**（`test_semantic_gate_failclosed.py`） |
| 步 4 GEM `economic_field_pool_check` | 建于 `build_economic_field_pool` / `build_candidate_field_pool`（含回退路径），**已读 `s1_semantic_<ds>` 并剔除黑名单字段**（2026-10-01 修复，fail-open：缺台账即放行） | **代码**（`test_semantic_field_pool_filter.py`；`POOL_BUILDER_VERSION≥4`） |
| 步 1 S1 自动补账 | S1 后缺 `s1_semantic_<ds>` 会自动补跑语义归类（零配额） | **代码**（`test_s1_semantic_autoclassify.py`） |

**两处生成侧消费已接通**：① 字段池过滤（本条）② S1 自动补账。缺台账时两处都 fail-open（放行 + 告警），故**覆盖率仍是要点**——存量已由 `field_semantic_classify.py --all` 补到 100% 活跃集。`--skip-semantic-gate` 仍是闸 SEM 的逃生口，须先有 `semantic` waiver。

### 1.4 选波侧的族/探针纪律（2026-10-01 修复，见 SKILL.md 步 4）

| 位置 | 行为 | 由谁保证 |
|---|---|---|
| 步 4 选波「每族 cap」 | `build_wave` 从 DB `expressions.family` 读族（`--from-db` 主路径）→ 每族限量 | **代码**（`test_build_wave_family_probe.py`） |
| 步 4 选波「探针先于扩批」 | 某族**全库尚无已回测行** → 本波该族 cap 收紧为 `WQB_PROBE_CAP`（默认 1）；有回测行则正常扩批 | **代码**（同上；`WQB_PROBE_GATE=off` 可关） |
| family 落库 | GEM 落库时从 `final_expressions_meta.json` 带入 `expressions.family`；`upsert_expressions` 用 `COALESCE` 保底（不带 family 的回写不覆盖原值） | **代码** |
| L3.5 族结构进字段池 | `s2_field_pool_<ds>` payload 带 `families`/`family_stats`（只含池内族），供 GEM 概念优先 | **代码**（`POOL_BUILDER_VERSION=5`） |

> ⚠ **存量限制**：`family` 由 GEM 落库时带入，**2026-10-01 之前生成的表达式 family 列为空**（无法从 `skeleton` 列反推——两者维度不同：`skeleton`∈{single,group,ratio,linear_mix,event_gated}，family∈{cs_rel,ts_chg,anomaly,...}）。存量波次的族 cap 因此不生效；新波次起生效。

> ⚠ **L3/L3.5 产物是「字段池」，不是 ideas**——严禁当 `ideas.md` 注入 GEM（同 [`step3-s1-semantic.md`](step3-s1-semantic.md) §3.4 / §3.5）。

## 2. L4：候选信号形态的构建五步法（本文件核心）

**从族出发，不从字段出发。** 一个族先想「它表征什么经济量」，再想「怎么把这个量变成可交易的方向」。

### 步 A：族 → 经济量（命名）

对每个族问：**这个族测的是什么**？答不出经济含义的族**直接跳过**（不投任何配额）。

> 例：`mdl264_<指标>_l1/l2/l3` = 「该底层指标未来趋势方向的**三分类概率**」。
> 这解释了一个族为什么会同时有 `_l1/_l2/_l3`——它们是同一个预测模型的三个输出槽。

### 步 B：枚举信号形态（合规优先）

对识别出的结构，**先看它天然支持什么形态**，而不是先写表达式再想办法合规。四种范式：

| # | 假设类型 | 构造 | 合规性 | 适用族结构 |
|---|---|---|---|---|
| **H1** | **净方向**（主形态） | `subtract(rank(A_hi), rank(A_lo))` | ★ **单一价差**，白名单放行 | 有 `P(up)`/`P(fall)` 对偶槽 |
| **H2** | 门控复用 | `trade_when(A_mid < 0.5, 净方向, -1)` | ★ 事件门控，非拼腿 | 有「中性/不确定」槽 |
| **H3** | 分布分歧 | `ts_stddev(...)` / 概率交叉项 | ⚠ 需检查是否退化为简单结构 | 有完整概率分布 |
| **H4** | 跨族一致性 | 多族净方向 → `group_zscore` 后取符号一致 | ★ 分组轴，非拼腿 | ≥ 3 个同质族 |

**合规红线（判合规看本质，不看是否命中正则）**：
- **禁止任何两条独立信号腿相加**——`add(A,B)`、`0.4A+0.6B`、等权 `0.5A+0.5B` **同属违规族**。
- **H1 为什么合规**：`P(up) − P(fall)` 是**同一个经济量（该指标的净方向）**的对偶两侧，
  且**同数据集、同族**——属白名单明确放行的 **单一价差信号**，不是「两条信号相加」。
  落地边界见 [`concept-taxonomy-map.md`](concept-taxonomy-map.md) 第 4 行（RT-04）与 [`step7-diagnose.md`](step7-diagnose.md) §7.7。
- **跨数据集 `subtract` 被闸 5 `spread_cross_dataset` 拦**——价差只在同源同集时成立。
- **辅助腿只能以条件 / 分组 / 残差三式入场**（H2/H4 即此），不得作并列信号项相加。

### 步 C：避开已判死结构（零成本，必做）

在写第一批表达式之前，拿骨架去过三道已有的筛子——**这一步能省掉整批配额**：

1. **L1 内部实证**：`docs/experience/02_signal_patterns.md` §5/§6/§11 + `get_dead_ends` / `get_dead_datasets`。
2. **判死粒度认知**：判死记录的是**族**不是**集**。`GBR-SIMPLE-STRUCTURE-DEAD` 判的是「简单结构」（`rank(f)` / `ts_delta(f,5)`），
   `GBR-PROD-SATURATED` 判的是某个字段族——**不代表整个数据集不能挖**。
3. **本区 profile 的 `gate_overrides`** 与 `registry_empirical` 的 dead_end 层。

> model264 实测：L1 命中 2 条族级/结构级判死 → 结论是「**唯一约束是结构级的，其余方向开放**」，
> 直接指明了 H1–H4 必须避开简单排名/时序，而不是判死整集。

### 步 D：三源验证「有据可依」（分层，成本递增）

**外部文献说有这个因子 ≠ 它在 BRAIN 上能过闸。** 验证顺序按可信度与平台贴合度分层：

| 层 | 信息源 | 能回答 | 成本 | 工具 |
|---|---|---|---|---|
| **L1** | 项目内部实证 | 本项目已实测过的形态是否有效、判死边界 | **零** | `docs/experience/`、`registry_empirical` |
| **L2** | BRAIN 中文论坛 | 别人试过吗、踩了什么坑、换手多少、破墙配方 | 低 | `tools/forum_recon.py`、`brain-forum-browse` |
| **L3** | 开源学术（arXiv/SSRN） | 机制叫什么、经济学先验、有无已被证伪 | 低 | `arxiv_api.py --concepts`、`concept_extract.py` |

**做法：L1 先跑（免费，能直接判死一部分）→ L2 按需 → L3 仅用于机制命名。**

- **L2 的三种结局必须分清**（`src/wqb/recon_evidence.py` 单一实现）：
  `found=true` → 入库；`found=false` → **可靠的负结果，本身即判死证据**；
  `found=null` / `status=error` → **工具故障，不是无解，不入缓存**。
  看退出码：**0=有产出 / 2=可靠无解 / 1=工具故障**。⚠ 退出码 1 永远不是取证。
- **L3 的硬边界（外发纪律）**：查询词发往 `export.arxiv.org`，**只发通用关键词**，
  **不发**未公开表达式 / 数据集名 / 字段名 / alpha id。产出**只用于给形态起名、给经济学故事、扩 Mode B 想法池**，
  **绝不允许直接搬运论文表达式**——会撞平台闸。

### 步 E：探针配给（配额从这里才开始）

**形态确定后先探针、后扩批**，不要一上来就投整批：

1. 每族取 **1–2 条最强探针**（单仿真），判据 `|sharpe| ≥ 0.5` 才扩批。
2. **探针前先跑步 5b prod-first**（步 5b 定义在 [`../SKILL.md`](../SKILL.md)）——避免整族撞 prod 墙后才查。
3. 探针骨架必须**互相不同构**（形状 / exposure 差异），否则整批同质化 → 闸 6 `check_batch_diversity` FAIL。
4. **不补参数变体凑数**（同 [`step4-generation.md`](step4-generation.md)）——机制换腿才是扩容正途。

> model264 实测成本估算：36 个三分类族 × 8 探针，`|S|≥0.5` 才扩批，**配额成本可控**。

## 3. 与既有分类学的对应（不要贴三套标签）

生成链上有三套概念分类学并存（dfe 8 问 / GEM 概念位 / hypothesis 12 类），
本文件的 L3.5 族角色与 L4 假设类型**是第四、第五个视角**，**必须通过桥表映射**，不要各自贴标签。

- 桥表：[`concept-taxonomy-map.md`](concept-taxonomy-map.md)（权威，测试守 `test_concept_taxonomy_map.py`）。
- **一次生成只挂一套主分类**：dfe 产出 ideas 时以 `dfe_question` 为主分类，`hypothesis_class` 作副标签。
- **L4 假设若进入假设优先流程**（饱和数据集路由），`hypothesis_class` 必须在
  `hypothesis_miner.HYPOTHESIS_CLASSES` 的 12 类里，否则 `load_catalog` 抛错。
  H1 净方向 → `dispersion` 或 `under_reaction`；H2 门控 → `event_conditional`；H4 跨族 → `cross_dataset`。

## 4. 反模式（每条：因 X 发生过 Y → 改用 Z）

- **把 L3 归类当终点**：拿到干净字段池却不知下一步 → 归类划边界，**信号来自 L3.5 族的 L4 推理**。
- **跳过 L3.5 直接写表达式**：380 字段当 380 个独立信号 → **从族出发**（36 个三分类族）。
- **族键遇首个后缀即返回**：三分类族只认出 6/36 → **剥离全部后缀**。
- **技术指标不前置拦截**：304 个技术指标被 `growth` 抢走 → `TECHNICAL_CATEGORIES` 排在 `ECON_CATEGORIES` 前。
- **H1 写成 `add(P(up), -P(fall)）` 或加权**：被判违规 → 用 `subtract(rank(A), rank(B))`，**它是单一价差不是拼腿**。
- **直接搬 arXiv 论文表达式**：撞平台闸 → L3 只取机制命名与经济学故事。
- **把 `forum_recon` 的工具故障当无解**：误把活路判死 → 退出码 1 不是取证，看 `recon_evidence` 三态。
- **L1–L3.5 没跑透就进 L4 烧配额**：这三层全零成本 → 跑满再进探针。

## 5. 快速上手清单（每次开战役照抄）

```
# 步 3（零配额，必做满）
python tools/field_semantic_classify.py --region $REGION --dataset $DS --write-ledger
#   → 看 blocked_fields（黑名单）、by_category（经济大类含 tech_*）、families（★三分类族数）

# 步 3.5 之间（零配额，本文件 §2 步 C）
#   → 读 docs/experience/02_signal_patterns.md §5/§6/§11；get_dead_ends / get_dead_datasets
#   → 确认判死是族级还是集级

# 步 4 之前（零配额，§2 步 D）
python tools/forum_recon.py --question "<形态描述>" --dry-run    # 先看检索计划
python tools/forum_recon.py --question "<形态描述>"              # 实跑，产出入库（含负结果）
#   → 仅当需要机制命名时：arxiv_api.py "<通用关键词>" -c q-fin --concepts

# 步 4（配额从探针开始，§2 步 E）
#   → 每族 1–2 条最强探针，|S|≥0.5 才扩批；先跑步 5b prod-first
```
