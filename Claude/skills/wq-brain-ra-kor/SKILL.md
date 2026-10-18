---
name: wq-brain-ra-kor
description: "在 KOR 区从字段体检起步挖 REGULAR alpha：字段定性 → 立机制组装骨架 → 归因 → 逐闸破法 → 算子穷举 → 终验。核心是「六步纵深 + 一圈发波闭环」：无归因不得发下一波，波次必须是因果依赖链而非并列扫参，已死轴禁入。组装环节先立经济机制（说不出收益从哪来不许组装），骨架形态由体检体征决定、壳层由机制决定，取证走论坛 + 外部金融论文双通道。仅适用 KOR/TOP600/D1。"
layer: L4
agent_created: true
allowed-tools:
- Read
- Bash
- mcp__wq-brain-http__*
- mcp__wqb-db__*
last_verified: 2026-10-18
---

# KOR 字段体检 → 组装 → 归因 → 破闸

## 职责边界

**本 skill 负责**：
- KOR 区域字段体检（六法）与信号组装
- 逐闸破法与算子穷举
- 归因分析与天花板判定

**本 skill 不做**：
- 数据集选择（→ `wq-brain-campaign-matrix`）
- 提交判定与动作（→ `submit_verdict` / `worldquant-submit-alpha`）
- 反过拟合复审（→ `brain-alpha-robustness`，破闸后）
- 跨区域迁移（换区须重扫）

**上游 / 下游**：
- 上游：`wq-brain-campaign-matrix`（数据集选择）
- 下游：`submit_verdict`（判定）→ `worldquant-submit-alpha`（提交）→ `brain-alpha-robustness`（反过拟合复审）

## 定位与边界

- **入口不是「已有信号」，是「字段体检」**——先摸清字段性格（覆盖 / 非零 / 频率 / 范围 / 中心 / 形态），再决定怎么构建、怎么修。
- **仅适用 KOR/TOP600/Delay=1**：全部杠杆档位与算子实证都在本区实测；**换区须重扫**（结构最优性逐字段实测，不可跨区照搬）。
- **负责**：字段定性 → 骨架组装 → 归因 → 逐闸破法 → 算子穷举 → 终验。产出 = 全闸候选，或**诚实的天花板判定**。
- **不做**：选数据集（→ `wq-brain-campaign-matrix`）；提交判定（→ `submit_verdict`，只有否决权）与提交动作（→ `worldquant-submit-alpha`，须用户确认）；反过拟合闸（→ `brain-alpha-robustness`，破闸**后**复审）。
- **配套**：九步通用正文在 [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)；本 skill 是其 KOR 的 L4 诊断分支。
- **本文件写方法**；实测数值 / 配方 / 逐年表 → [`references/_kor-gatebreak-evidence.md`](references/_kor-gatebreak-evidence.md)。

## 主干：六步纵深 + 一圈发波闭环

```
① 六法体检  调 L1 → 摸清字段性格            ┐
                                           │
② 组装      ★ 自建：立机制 → 定核心形态 →   │  一个信号
              选壳层 → 双通道取证            │  从零到提交
                                           │
③ 归因      判「信号衰减」还是「因子拖累」  │
                                           │
④ 破闸      每闸一根杠杆，单变量对照         │
                                           │
⑤ 算子穷举  先分组轴 → 再平滑 → 最后幂次     │
                                           │
⑥ 终验      prod/self 实测 + 反过拟合 → 交用户┘

       ↺ 发波闭环：开波前跑 ③ 归因 → 查决策表 → 写清继承/准入/收窄
         → 发波 → 收割 → 回到 ③
```

**六步是纵深**（一个信号怎么走完），**闭环是横向**（每波怎么设计）。两者独立且强制。

## 铁律总表（八条，每条只在本表定义一次）

| #     | 铁律                   | 一句话                                                       | 定义处   |
| ----- | -------------------- | --------------------------------------------------------- | ----- |
| **A** | 单边恒正取变化率             | 中心趋势单边恒正的字段 ⇒ `ts_delta`，**禁裸水平做多空**                      | ①     |
| **B** | 方向正反各测一条             | `reverse()` 与正向**不精确反号**（截断 × decay × 符号交互），猜方向系统性错       | ①     |
| **E** | 先做 raw vs RN 分解      | 报告期塌陷**先分解再修**：RN 增量 ≫ raw ⇒ 换中性化档；raw 与 RN 同步走弱 ⇒ 换机制    | ③     |
| **F** | **无归因不得发波**          | 没跑完归因不许派发下一波；归因不在链上就当它没发生                                 | 发波闭环  |
| **G** | **波次是因果依赖链**         | 下一波只在上一波优胜集合内变动，候选数 ≤ 上一波 **1/3**，不降即设计退化                 | 发波闭环  |
| **H** | **组装前必须立机制 + 双通道取证** | 说不出「收益从哪来」不许组装；禁止套固定模板                                    | ②     |
| **I** | ① 调 L1，② 自建          | 体检复用 L1 六法；组装自建（逐条核对后不用 `brain-data-feature-engineering`） | ① / ② |

## 发波闭环（每波开波前必走）

> 本区已因违反此纪律白扫十余波：归因被跳过、每波从基线重启、已知死轴反复重测。

### 1. 归因前置（铁律 F）

开波前对**上一波优胜候选**跑两个工具，缺一不可：

| 工具                       | 必答问题                                     |
| ------------------------ | ---------------------------------------- |
| `get_alpha_yearly_stats` | 逐年 S 分布如何？**S<1.0 的年份占几成**？top1 年占正收益多少？ |
| `get_alpha_pnl`          | 曲线是阶梯累积（健康）还是尖峰暴涨（可疑）？**有几段停滞 / 回撤**？    |

### 2. 归因读数 → 发波决策表

| 归因读数                   | 含义         | 下一波必须做什么                                |
| ---------------------- | ---------- | --------------------------------------- |
| 单年占正收益 >30%            | 过拟合        | **换机制族**，不做参数微调                         |
| **S<1.0 年份 ≥3 成**      | 2Y 闸结构性不可达 | ⛔ 停扫 decay / 平滑 / 门控，**换 regime 无关的机制** |
| 近年 S 断崖（S 从 2+ → <0.5） | 机制性衰减      | 换字段族（衰减是机制的，不是参数的）                      |
| 停滞段 ≥3                 | regime 依赖  | ⛔ 平滑器谱整族无效，**必须换机制**                    |
| RN 涨幅 ≫ raw 涨幅         | 因子暴露拖累     | **换中性化档**（唯一该继续扫的轴）                     |
| raw 与 RN 同步走弱          | 信号自身衰减     | 换字段族 / 机制族                              |
| 阶梯健康 + 停滞段少 + 单年 <30%  | 信号真实但强度不足  | ⭐ **此时才允许**做强度 / returns 杠杆扫描           |

⚠ **本区实战范例**（写给未来的自己）：Wave10 优胜 `e76J6Eap` 逐年 S<1.0 占 **4/10**
（2016 S=0.08、2017 S=0.02、2018 S=0.84、2023 S=0.30）⇒ LADDER ≈ 1.07，**2Y 闸在任何参数档都不可达**。
若当时继续扫 CROWDING×decay 的 decay 档，必然白烧配额。**归因先行不是仪式，是止损。**

### 3. 波次三问（铁律 G）

开波前逐条写清，缺任一条 = 设计退化，必须重写：

1. **继承**——上一波的哪条结论被写成本波的准入条件？
2. **准入**——本波禁止触碰哪些轴？（对下表）
3. **收窄**——候选数 vs 上一波候选数，比值多少？**不降即退化**。

**反模式（本区踩过）**：一边在报告写下「X 是唯一某杠杆」，一边仍派发上一波已实测更劣的同类结构
（已实测 `ts_decay_linear` S=1.13 优于 `ts_mean` S=0.89，却仍扫 `ts_mean` 窗口谱）⇒ 把已知会败的东西重复烧配额。

### 4. 已死轴清单（命中即禁入 quota）

| 死轴               | 证据                                                          |
| ---------------- | ----------------------------------------------------------- |
| `truncation` 扫描  | 多档 returns **逐位相同**（信号已被压平）；区域锁定项本就不含它                      |
| `universe` 扫描    | `get_platform_setting_options` 实测**本区唯一合法档 TOP600**，扩容被平台锁死 |
| 仿真 `decay` 单独扫   | 只动 TO（-20% 量级）不动 returns（+1% 量级）⇒ 只在与其它轴交叉时才有叠加意义           |
| 劣于同族的平滑器 / 算子窗口谱 | 同族内已分出优劣后，劣者窗口不再扫                                           |
| 跨区照搬的结构配方        | 杠杆**逐字段 / 逐族实测**，不可跨区移植                                     |
| 同波「在飞批次」的读数      | **不得**当作下一波设计依据（避免同波自我污染）                                   |

---

## ① 六法体检（★ 入口 —— 调 L1，不自建）

> **铁律 I（①部分）**：直接调 [`brain-datafield-exploration-general`](../brain-datafield-exploration-general/SKILL.md)，不重造。
> 它已有完整实现（离线优先 / 合批成本 / 最小集 6 条 / 扩展集 ≤8 条 / 类型先行 MATRIX·VECTOR·EVENT·GROUP / 每法「→交FE」映射），
> 且踩过的坑都在里面。**本节只写 KOR 特例与下游接线。**

### ★★ 0. 入口三件事（顺序不可倒，**跳步必付配额代价**）

开波前**必须**依次完成，缺任一件 = 方向可能已偏：

| 序 | 事 | 干什么 | 判据 / 产物 |
|---|---|---|---|
| **0.1** | **字段质量先验** | 按 `alphaCount` 降序（同分按 `userCount`）取 **TOP30 看轴** | ⭐ **头部字段 = 该集最强经济轴**。若头部指向的轴 ≠ 拟挖方向 ⇒ **方向本身可能已偏，先纠偏再开波** |
| **0.2** | **字段分类（以 description 为准）** | 只读 description 分类，**禁按字段名**；并**逐条记录名 vs description 的差异** | 差异表 = 被漏掉的资产。分类规则见 `_assembly-playbook.md` |
| **0.3** | **字段画像五问 + 预处理决策** | 测什么/怎么测/时间维度/为何存在/可靠性 ⇒ 推算子与窗口 | cov<0.4→backfill；季频→窗口≥63d；VECTOR→`vec_avg`；单边→变化率 |

**为什么 0.1 必须在最前**：`brain-alpha-research-field-quality` §1 明确「头部字段常揭示该数据集**最强的经济轴**」
（例：analyst14 / GLB 由资产负债表轴领衔，而非直觉的 EPS 修正轴）。

**打样实证（analyst_consensus，2026-11-16）**：αC 最高 = `estimate_count_currentliabilities_annual12`（流动负债家数，αC=4），
TOP30 里**资产负债表科目家数 + BVPS 实际值 + flash 快照家数**领衔 —— **既不是盈利轴也不是 EPS 修正轴**。
而 Wave11–13 连续三波全打在 net/eps/revenue 上 ⇒ **方向从第一波就偏了，烧了 10 条配额**。

**为什么 0.2 不能按字段名**：同集 `estimate_count_*`(132) 与 `count_*`(4) 按名前缀会被切成**两个互不相认的族**；
且窗口标记写法不统一（`four_weeks_prior_` / `_3mth_prior` / `recent_` / `flash_period_`）⇒ **按名分类会丢失四窗梯度**。
只有读 description 才还原成同一个「30 标的物 × 4 时间窗」矩阵（打样实测）。

**0.1–0.3 的产物落盘**：`tracking/<REGION>/reference/datasets/<dataset>.md`（**每数据集一份**，
生成器 `kor_build_dataset_docs.py`，含名 vs description 差异表 + 质量先验 TOP30 + 五问 + 预处理决策；
手工回填过的文档带保护，需 `--force` 才覆盖）。

**KOR 特例（其余回 L1）**：

| 差异        | 内容                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------------------- |
| **离线包退化** | WebData `dataSetList.json` 里 KOR 组合极少 ⇒ 除 `analyst25` 外多数字段 skew/kurt/freq/shape 为 **null** ⇒ **多数字段必须走在线六法** |
| **在线设置**  | `Neutralization=None` / `Decay=0` / `Test Period=P0Y0M0D`，KOR/TOP600/1                                        |
| **平台事实**  | KOR/Delay=1 **唯一合法 universe = TOP600**                                                                        |
| **不可用算子** | `ts_ir`、`ts_target_tvr_hump` 在 KOR **整批连坐 FAIL 且无报错** ⇒ 不进体检表达式                                               |
| **不可取法**  | 法 6 在线 `zscore(F)>k` 未实测 ⇒ **优先走离线形态**，离线缺则按法 1/2 的覆盖差推断                                                      |

**★ 接线（体检读数接不上 = 体检白做）**：

| 来源                                 | 交给下游哪一步                                |
| ---------------------------------- | -------------------------------------- |
| 0.1 质量先验（TOP30 轴）                  | **②.a A-2 收益来源声明**（先确认方向 = 头部轴）        |
| 0.2 分类差异表                          | ②.b（矩阵结构 ⇒ 跨标的物广度，非单标的物强度）             |
| 0.3 五问 + 预处理决策                     | ②.b 算子与窗口（**不许自由发挥**）                   |
| cov<0.4 / 零占比高 / `zero_inflated` | ②.b 第 3、5 行（门控 + backfill，**禁裸 rank**） |
| 更新频率（季频 ≥63d）                    | ②.b 窗口下限                               |
| 中心趋势（单边恒正）                       | 铁律 A ⇒ ②.b 第 1 行                       |
| 量纲跨度                             | ②.b 第 2 行（去量纲）                         |
| 全套读数                             | ②.a A-1 五问 + A-2 收益来源声明                |

**兄弟 skill（不要重造）**：

| 需求                               | 用这个                                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| 单字段六法体检                          | [`brain-datafield-exploration-general`](../brain-datafield-exploration-general/SKILL.md)（L1） |
| 数据集级审计                           | [`brain-dataset-exploration-general`](../brain-dataset-exploration-general/SKILL.md)（L1）     |
| 字段质量先验（alphaCount/userCount、包预筛） | [`brain-alpha-research-field-quality`](../brain-alpha-research-field-quality/SKILL.md)（L1）   |
| 全量字段 typed catalog（闸 2/3 数据源）    | `wq-brain-campaign-toolkit` 的 `scan_fields.py`                                               |

⚠ **已核对并决定「不调用」的 L1**（2026-10-16，防误挂）：`brain-data-feature-engineering` ——
无 `search_forum_posts` 权限 / 产物是单层模板（无壳层抽象）/ 体征读数无下游消费 / `Expected Exposure` 只用于事后去重。
⇒ ② 自建。**但 `**Concept**` 块与 `s1_<ds>_d1` 台账契约照用**（GEM 只认这个格式）。

**★ 8 问法的适用边界（2026-11-16 裁断，防再纠结）**：按 `brain-data-feature-engineering` 第 0 步的
透明度分档，**analyst / fundamental / earnings / insiders / shortinterest 类且含标准财务词汇，
或描述覆盖率 ≥80% ⇒ 透明集 ⇒ 跳过 8 问**，走「0.1 质量先验 → 0.2 分类 → 0.3 五问 → 预处理决策」。
（打样实证：`analyst_consensus` 描述覆盖率 **300/300 = 100%**，确认透明集。）

⇒ **豁免的只有 8 问本身；0.1 / 0.2 / 0.3 三件事在任何档位都不能跳。**
黑盒集（`other*`/`model*`/`ai_*`/`ml_*`、字段名无语义、描述覆盖率 <30%）才做 8 问全问。

## ② 组装（★ 自建，禁止套模板）

> **铁律 H**：**组装不是挑一副现成骨架往里填字段。**
> **核心信号形态由 ① 的体检体征决定；壳层每一层是否存在由经济机制（收益来源）决定；灵感模板走外部双通道取证。**
> **说不出「这个字段的收益从哪来」的，不许组装。**

### ②.a 立机制（A-1 五问 + A-2 硬门，自建）

**A-1 五问定骨架方向**（每问答案直接决定 ②.b / ②.c 走向）：

| #            | 问句                             | 答案 ⇒ 骨架方向                                          |
| ------------ | ------------------------------ | -------------------------------------------------- |
| 1 **时间维度**   | 存量水平 / 流量 / 变化率？               | 存量 ⇒ `ts_delta(F,N)`（铁律 A）；流量 ⇒ 水平直接用              |
| 2 **相对性**    | 水平差异 / 排序差异？                   | 水平 ⇒ `zscore`/`ts_zscore`；排序 ⇒ `rank`/`group_rank` |
| 3 **被定价的是谁** | 广度（覆盖数 / 家数）/ 强度（修正幅度 / 评级升降）？ | 广度 ⇒ 水平即可；强度 ⇒ 必须先取变化率                             |
| 4 **有无博弈**   | 拥挤 / 存量博弈 / 需可投资性？             | 是 ⇒ 加规模轴残差化壳层（②.c 第 1、3 行）                         |
| 5 **事件性**    | 事件型稀疏（非事件期无信息）？                | 是 ⇒ `trade_when` 门控，**禁裸 rank**                    |

**A-2 收益来源声明（硬门，缺项即不许组装）**：

| 声明项        | 要求                            | 判死条件                       |
| ---------- | ----------------------------- | -------------------------- |
| **谁在被定价**  | 具体到主体（卖方分析师 / 流动性提供者 / 被动资金…） | 写不出主体 ⇒ 不是机制，是相关性          |
| **为什么会被错** | 行为偏差 / 信息摩擦 / 制度约束，点名一种       | 只能说「大家没注意」⇒ **不可用**        |
| **错了多久修复** | 落到窗口量级（数日 / 一季 / 数季）          | 无修复期 ⇒ 是水平暴露不是错误定价，**换机制** |
| **预期方向**   | 明确「被高估 ⇒ 后续跌」，不许「可能涨可能跌」      | 方向不明 ⇒ 走铁律 B 正反各测          |

**A-3 概念块（自产，供 GEM 消费）**——标记必须与 GEM 解析器一致：

```markdown
**Concept**: <机制一句话，不是字段名>
- **Fields Used**: <完整字段 id，逗号分隔>
- **Definition**: <测的是什么 + 怎么测>
- **Logical Meaning**: <谁被定价 + 为什么错 + 修复期>
- **Directionality**: <方向句，含时间窗>
- **Boundary Conditions**: <失效条件：停牌 / 覆盖变更 / 阈值失效>
- **Expected Exposure**: <momentum|reversal|value|quality|growth|lowvol|liquidity|sentiment|flow|risk|other>
- **Implementation Example**: `<模板，{占位符}用字段后缀>`
```

| 契约                  | 要求                                                                                                               |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 占位符                 | `{xx}` 必须是本数据集字段的**后缀**，对不上会被 GEM 丢弃                                                                             |
| 窗口                  | 只用标准窗口 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260                                                                 |
| **禁加权拼腿**           | `0.5*a+0.5*b`、`add(multiply(…),multiply(…))` 被闸 5 拦                                                              |
| **禁「跨字段等权相加」（★ 2026-11-16 实证补强）** | `add(rank(字段A), rank(字段B))` **同样被拦**（`POISON:equal_weight_leg_add`）—— **秩化 ≠ 豁免**：闸门按「顶层实参 ≥2 条互不相等、各自引用数据字段的信号腿」判定，与是否 `rank`/`group_rank` 归一化无关。**放行**：① `subtract(rank(A),rank(B))`（两腿**同源**同一数据集 + **单一经济含义**）② `add(ts_mean(x,22),ts_mean(x,66))`（同一字段仅窗口差异 = 单信号多窗平滑）③ 换算子几何 `group_rank`/`group_zscore`/`ts_quantile`。**「多字段合成一个机制」的正解 = 价差（背离）或条件门控，不是相加**。 |
| `Expected Exposure` | **必写**，不写被关键词推断补 `(inferred)`                                                                                    |
| 落盘                  | `manual_KOR_delay1__ideas.md` + 台账 `s1__d1`，**`source` 必写 `manual`**（写 `standalone` 会被 GEM 静默忽略） |
| 概念预算                | 一 dataset **≤6 个**（KOR 小宇宙配额紧张）；每概念 1–2 字段；同一字段至多进 2 个概念                                                         |

⚠ **KOR 专属陷阱**：`analyst` 类字段名含 eps/revenue/estimate 等标准财务词，**看起来自解释**，
但本区实测 `analyst_factor_signals` 59 个字段里**有效仅约 2 个**
⇒ **「字段名自解释」≠「在本区可用」**，透明类字段**仍必须跑 ①**，不许因名字清楚直接组装。

### ②.b 体检体征 → 核心信号形态（查表，不许自由发挥）

**每行都要能指回 ① 的某个读数，指不回的形态不许用。**

| ① 体检读数                 | 核心信号形态                                 |
| ---------------------- | -------------------------------------- |
| 单边恒正 + 有界小量纲           | `ts_delta(F,N)` 变化率（铁律 A）              |
| 近正态、连续                 | `rank(F)` / `zscore(F)`，无预处理           |
| `zero_inflated` / 事件稀疏 | `trade_when(<事件条件>, <信号>, -1)`，禁裸 rank |
| 季频更新                   | 窗口 ≥63d；短窗被 NaN 污染时按季频取 252            |
| cov<0.4                | 必须 `ts_backfill(F,N)` 前置               |
| 覆盖广度型字段                | 同字段多窗 `rank` 乘积（**广度 × 持续性**）          |
| 强度型字段                  | `ts_delta` 后多窗乘积（**修正幅度 × 修正加速度**）     |
| VECTOR                 | 先 `vec_avg` / `vec_max` 等 `vec_*` 降维   |

### ②.c 壳层按机制选层（**不是四层全上**）

> 每一层是否存在由 A-1 第 4 问决定。**机制上无关 ⇒ 不加壳**（加壳 = 引入非目标暴露，毁 S）。

| 经济机制             | 需要加的壳层                                              |
| ---------------- | --------------------------------------------------- |
| 小市值 / 流动性差，需可投资性 | `vector_neut(·, power(rank(<规模>), pow))`            |
| 事件型信号，非事件期不该持仓   | `trade_when(greater(rank(<流动性>), T), ..., -1)`      |
| 收益可能只是行业轮动       | `group_neutralize(·, <行业轴>)` + `bucket(rank(<规模>))` |
| 分布有极端尾部、挤权重      | `tail(·, lower, upper, newval)`                     |
| **机制上与上述无关**     | **不加壳**                                             |

⚠ **换粗轴是无损轴，可优先试**：中性化 `subindustry < industry < sector`（sector 饱和），换粗轴常使 robust 与 S **同升**。
⚠ **别把壳层当信号**：壳层只解决 investability / 行业暴露 / 稀疏持仓；**S 的来源只能是核心信号**。

### ②.d 外部取证（组装前必做，**双通道**）

> **论坛是辅助，不是唯一来源。** 只查论坛 ⇒ 有模板但不知机制是否本区成立；只查论文 ⇒ 机制自洽但可能落不到平台算子上。

**通道 A｜BRAIN 论坛 → 给可落地的表达模板**

| 步骤        | 工具                                                                            |
| --------- | ----------------------------------------------------------------------------- |
| 搜机制模板     | `search_forum_posts(search_query="<机制关键词> 模板")`                               |
| 读正文 + 评论  | `read_forum_post(article_id="")`（正文在 `post.body`）                         |
| 术语 / 算子核对 | `get_glossary_terms`、`get_documentations` / `get_documentation_page(page_id)` |
| 判死取证纪律    | `seal_dead_end` 的 `forum_recon` 闸 fail-closed：**工具故障 ≠ 论坛无解**                 |

**通道 B｜外部金融研究与论文 → 给机制 + 方向句 + 持有期**

| 步骤      | 工具                       | 说明                                                         |
| ------- | ------------------------ | ---------------------------------------------------------- |
| 机制假说与实证 | **`domain_search`**      | 一句话高层意图；**把 A-1 五问的答案写进 query**（写「覆盖**广度变化**」而非笼统的「分析师数据」） |
| 补充单点事实  | `WebSearch` / `WebFetch` | arXiv / NBER / SSRN / 期刊摘要页，取**摘要 + 结论段**                  |

⚠ **`domain_search` 昂贵**（远端规划 + 多源检索 + 高延迟）⇒ **每个机制只调一次**；查一个定义用 `WebSearch` 即可。

**通道 B 的检索纪律**：

| 纪律                 | 要求                                                        |
| ------------------ | --------------------------------------------------------- |
| **只取可证伪的机制**       | 必须给**方向句 + 持有期 + 适用域**；只给相关系数不给机制 ⇒ 不采                    |
| **警惕文献偏误**         | 因子动物园多在 USA 样本；**KOR 是小宇宙、制度不同** ⇒ 先当**假说**，不当模板          |
| **不可迁移的结论显式标记**    | 论文自带 "US only" / "NYSE" / "large cap" 限定 ⇒ **在概念块写明**，防照搬 |
| **时效性 + 复现状态**     | 优先近 5 年；被后续复现推翻的经典异象**不作默认依据**                            |
| **失败即记录**          | 查不到 ≠ 无此机制，**记进战报**（已查渠道 / 检索式 / 结论），避免下波重复空转             |
| **A-2 硬门不因有论文而放宽** | 论文给的是机制，**不是本区证据**；仍须本区实测                                 |

**双通道裁决（对不上必须裁决，不得跳过）**：

| 情形                | 处置                                        |
| ----------------- | ----------------------------------------- |
| **A、B 指向同一机制**    | ⭐ 优先组装（论坛给表达、论文给方向句与持有期）                  |
| A 有模板、B 无机制支撑     | 可组装但**降优先级**，标「经验模板，机制未验证」，A-2 从严         |
| **B 有机制、A 无对应表达** | ⭐ **最有价值** —— 按 A-1 五问**自建骨架**，用论文的机制句定形态 |
| **A、B 机制矛盾**      | ⛔ 不组装；先查样本差异，**矛盾未解不得进入 ③**               |

⚠ **两通道结论都只作起点，必须本区实测** —— 跨族照搬可反向（本区实测 `bucket(rank(cap))`
在一个族 0.89→0.71 ✅，另一族 0.73→0.83 ❌）；论文的 USA 结论同样不保证在 KOR 成立，**这是文献偏误，不是例外**。

**三者分工**：论文给「机制 + 方向句 + 持有期」，论坛给「可落地的表达模板」，
A-3 概念块给「本区的机制定义与落地记录」。冲突时在 `Logical Meaning` 里写清
「本区实测 vs 论坛模板 vs 论文结论」的三方差异，并注明采信哪一个、为什么。

### ②.e 组装硬规则

| 规则                   | 要点                                                              |
| -------------------- | --------------------------------------------------------------- |
| **同字段多时间窗 = 单信号结构化** | 合规（不属混信号）                                                       |
| **多字段组合只走条件门控**      | `add`/`multiply` 相加不同机制字段 = **混信号违规**；`trade_when`/`if_else` 合规 |
| **条件字段须机制正交**        | 频段 / 机制不同的字段用 AND 门常双杀；先单测门控收益再上                                |
| **组装顺序敏感**           | `group_neutralize` 在 `group_rank` **之前**；`tail` 在其后             |
| **乘积的腿要同机制**         | 不同机制字段相乘 = 噪声占优（本区实测 S 掉到 0.02–0.28）                            |
| **一字段一条腿**           | 跨数据集同机制 = 同一条腿 ⇒ 一条腿只出 1 颗，不铺量                                  |

**② 的产出（交给 ③）**——三样缺一不许进 ③：
① **表达式**（能指回 ②.b 某一行）② **A-2 收益来源声明**（谁 / 为什么错 / 多久修复 / 什么方向）
③ **加了哪几层壳、依据哪条机制**（②.c）。

## ③ 归因（先判类型，再选杠杆）

> 归因不只是第三步的事后复盘，**它同时是发波前置闸**（铁律 F）——不发波就不归因，本节就当它没发生。

| 归因类       | 工具                                                       | 判读 → 处置                                      |
| --------- | -------------------------------------------------------- | -------------------------------------------- |
| 时期        | `get_alpha_yearly_stats`                                 | 逐年 S；**S<1.0 年份占比 ≥3 成 ⇒ 2Y 结构性不可达**         |
| **单年集中度** | `get_alpha_yearly_stats` 分年 PnL 加总                       | top1 年占正收益 >30% ⇒ 过拟合指纹，换机制                  |
| **曲线形态**  | `get_alpha_pnl`（长序列会降采样）                                 | 阶梯累积 = 健康；尖峰暴涨 = 可疑；**长期停滞段 ≥3 ⇒ regime 依赖** |
| **因子暴露**  | `get_alpha_pnl` 的 `investability-constrained-pnl` / RN 列 | 逐年 `因子暴露贡献 = raw 增量 − RN 增量`                 |
| 行业 / 市值分位 | 导出 PnL                                                   | 收益集中少数行业 ⇒ 只是行业轮动；集中于极端市值分位 ⇒ 结构性问题          |

**铁律 E**：报告期塌陷**先做 raw vs RN 分解，再决定修什么**——
RN 增量 ≫ raw 增量（因子贡献为负）⇒ 纯 alpha 没坏 ⇒ **换中性化档**；
raw 与 RN 同步走弱 ⇒ 信号本身衰减 ⇒ 换字段 / 机制族。

⇒ 读数统一落到「发波闭环」的**归因读数 → 发波决策表**（本节不重复该表）。

## ④ 破闸杠杆图谱（每闸一根，KOR 实测）

| 闸 / 症状        | 杠杆                                                  | 方向                               |
| ------------- | --------------------------------------------------- | -------------------------------- |
| 报告期塌陷         | 先 raw vs RN 分解（铁律 E）                                | RN ≫ raw ⇒ 换中性化档                 |
| **中性化档**      | **换族必重扫 11 档**（逐族择优，勿照搬）                            | 本战役峰度族 REVERSION_AND_MOMENTUM 最优 |
| LOW_SHARPE    | decay 降（S↑）/ 加正交腿                                   | decay↓ 推高 S，同时推高 inv 门槛          |
| LOW_FITNESS   | **tail 收紧**（0.2/0.8→0.25/0.75）纯改善                   | 0.92→0.95                        |
| IS_LADDER（2Y） | **decay 调至峰值**（S↔2Y 权衡）                             | 本战役峰值 decay=3                    |
| **IS 推全过**    | **★ `group_neutralize(·, sector)`**（剥行业暴露）          | 综合改善 F 与 2Y、清 failed_ra          |
| INVESTABILITY | vector_neut 幂次调至甜蜜区；**过高触发 ladder window 跳变致 2Y 崩** | 本战役 0.80–0.85 甜区，≥0.9 跳变         |
| prod          | **先判 n 判据**：`[0.7,0.8)` 桶 n≥1 ⇒ 密墙别扫窗口；n=0 才可扫      | 见下                               |

**F 公式反推缺口**：`F = S × √(returns / max(TO, 0.125))` ⇒ 先判缺口归属 S / TO / returns 哪一档，再选杠杆。

**KOR 中性化 11 档**（`get_platform_setting_options` 实测合法）：
NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST。
**默认别用 MARKET**——逐族实测择优。

**prod 墙处置顺序**：换族 → 换连续桶分组轴（`bucket(rank(<规模>))`）→ 加 rank 阈值门控（`trade_when(rank(<流动性>)>T)`）。
⚠ **每桶必实测、不可跨族照搬**（`bucket(rank(cap))` 在 oth695 是 0.89→0.71 ✅，在 pv47 是 0.73→**0.83** ❌）。

## ⑤ 算子穷举（顺序 = 先分组轴，再时序平滑，最后幂次）

对照 103 算子目录补未试家族。⚠ **当格局是「IS 全过 + prod 墙」时，族内穷举算子通常无新杠杆 ⇒ 及时止损转下一族。**

本战役峰度族实测（详见 evidence）：`group_neutralize(sector)` 是唯一突破；`group_zscore` 有害；
`signed_power` 在秩积上 no-op；`ts_mean`/`ts_decay_linear`/`hump` 毁 S；`trunc` 小改等价可删；门控阈值上调毁 S。

## ⑥ 终验

- `check_correlation(alpha_id)`（prod）+ `check_self_correlation(alpha_id)`（self，本地不占配额）。
- **Phase C 反过拟合**（`brain-alpha-robustness`）：Recent-3yr 强度 / CV_Sharpe / 衰减比 / 平年 / max-min 比。
- **prod n 判据**：`check_correlation` 直方图 `[0.7,0.8)` 桶 n≥1 ⇒ 结构性密墙。
- **提交权归用户**（`worldquant-submit-alpha` 确认后才走 `POST submit`）。

## KOR 平台事实与工程坑

- **发批前三闸**：`ensure_safe_for_dispatch` + 新算子 2 条小批验存在性 + 字段 `get_datafields` 实名核对；本地库含已下架数据集 ⇒ **必跑 `preflight_expressions`**。
- **不可用算子**：`ts_ir`、`ts_target_tvr_hump`（整批连坐 FAIL 且无报错）。
- **禁混信号**：多字段组合只走 `trade_when`/`if_else`；`add`/`multiply` 相加不同机制字段 = 违规（同字段多窗口合规）。
- **「已点亮」= 数据集级已提交 ≥3 颗**，只排除该数据集；**不要按塔排除**——红的是「已试结构」，不是字段或塔。名单查 `get_submit_ready(region="KOR")`。
- **宇宙是单一国家**（`config.REGION_COUNTRY_SCOPE`）⇒ country 轴中性化 / 分组等于全市场，别用。
- **僵尸批次判据**：`progress` 非空（如 0.35/0.9）**只是慢，不是僵尸**（会自行 COMPLETE）。
- **`get_user_alphas` 不支持 `order=-sharpe`**（400）；`results[].datasets` 在 KOR 为空 ⇒ **解析 `code` 字段前缀**归组；返回体积极大 ⇒落盘再解析；`batch_get_alpha_metrics` 对新建 alpha 全返回 null ⇒ 逐个 `get_alpha_details`。
- batch 工具 `nan_handling` 参数**被静默忽略**（提交 ON、回读恒 OFF）⇒ 该维度不可经此工具调。
- 比较不同 pow 的 2Y **必须先核对 ladder window 是否同档**（过高 pow 会跳档），否则比较无效。
- 长批后 `lookINTO` 报 HTTP 401 ⇒ `authenticate` 重认证即恢复。
- `performance_comparison` **不是风险因子归因工具**（端点是 merged performance check）⇒ 风险因子暴露走 `get_alpha_pnl` 的 `risk-neutralized-pnl` 列。
- 平台算子目录可能过期 ⇒ **以实测为准**。

## Resources

> 脚本一律在**仓库根**执行，`$WQ_PY` = `world-quant-brain-mcp/.venv` 的解释器（登记见 `docs/env_and_switches.md`）。

**参考文档（`references/`，按需加载，别一次全读）**

| 文件                                                                    | 什么时候读                             |
| --------------------------------------------------------------------- | --------------------------------- |
| [`_probe-sop.md`](references/_probe-sop.md)                           | 设计 / 派发探针前：8 槽配比、构型分工、读数三分法、多样性三闸 |
| [`_dataset-scan-sop.md`](references/_dataset-scan-sop.md)             | S0 选集：数据集评分与排除口径、离线体检包退化范围        |
| [`_workflow-pipeline.md`](references/_workflow-pipeline.md)           | 把六步接回九步骨架：每步产物与落库位置               |
| [`_kor-gatebreak-evidence.md`](references/_kor-gatebreak-evidence.md) | **要具体数值 / 配方 / 逐年表时**             |
| [`_kor-campaign-log.md`](references/_kor-campaign-log.md)             | 判断「这条结论还有效吗」（历史层 + §0 裁决表）        |
| `references/<类别>.md`（11 份）                                            | 进入某个「区域 × 类别」组合时——清单见下方「组合分支」表    |

**脚本（家 = `tracking/KOR/scripts/`，AGENTS.md §8.13）**

| 命令                                                                          | 用途                                       |
| --------------------------------------------------------------------------- | ---------------------------------------- |
| `$WQ_PY tracking/KOR/scripts/kor_s0_scan.py`                                | S0 数据集评分 → `logs/_kor_s0_whitelist.json` |
| `$WQ_PY tracking/KOR/scripts/kor_pool_rank.py `                  | 候选池按「还差哪道闸」排序（只读文件，不占配额）                 |
| `$WQ_PY tracking/KOR/scripts/scan_diversity.py --audit <批次>`                | 发批前多样性三闸（族数 / 未用算子 / 算子数）                |
| `$WQ_PY tracking/KOR/scripts/scan_diversity.py --build <字段> --all-families` | 反向：按 9 族骨架生成扫描网格                         |
| `$WQ_PY tracking/KOR/scripts/gate.py --dataset  --file `    | KOR 提交前统一闸门（语法 / 白名单 / 类型 / 禁用算子 / 毒模式）  |
| `$WQ_PY tools/fields/field_profile.py --query --region KOR`                 | 字段画像（coverage / to_med / S 分档）           |
| `$WQ_PY tools/webdata_quality.py --zip  --region KOR --fields `   | 离线体检包生成（KOR 仅 `analyst25` 完整）            |
| `$WQ_PY tools/submit_batch.py`                                              | 批量派发仿真（**不是**提交 alpha）                   |

⚠ **脚本不放技能目录**：技能目录是 `tools/sync_skills.py` 的同步面，副本装到安装位后读不到仓库内的
`template_families.json` / `tracking/KOR/reference/*.json` ⇒ 必然跑不通（2026-10-15 迁出，见 `tracking/KOR/scripts/README_NEW_TOOLING.md`）。

**面板 / 阈值 / 组合覆盖（改控制的入口）**

```bash
$WQ_PY -m wqb.profiles explain --region KOR             # 每个生效值带来源层
$WQ_PY -m wqb.profiles check --region KOR               # 校验（改完必先跑）
$WQ_PY -m wqb.profiles render --region KOR --apply      # 重渲生成块
$WQ_PY -m wqb.profiles sync-cells --region KOR --apply  # 刷新判死 / 胜绩
```

**MCP 工具 · 平台侧 `wq-brain-http`**：`get_datafields`（字段实名核对）、`preflight_expressions`（发批前必跑）、
`get_platform_setting_options`（合法设置档，别照搬别区）、`batch_create_simulations` / `batch_status`、
`get_alpha_details`（新建 alpha 逐个拉）、`get_alpha_pnl`（`risk-neutralized-pnl` 列做归因）、`get_alpha_yearly_stats`、
`search_forum_posts` / `read_forum_post` / `get_glossary_terms`（取证通道 A）、
`check_correlation`（prod）、`check_self_correlation`（self，本地不占配额）、`submit_verdict`（只有否决权）。

**MCP 工具 · 台账侧 `wqb-db`**：`get_dead_ends`、`list_wave_results` / `get_latest_wave`、`get_submit_ready`、
`get_cross_region_lessons`、`upsert_wave_result` / `upsert_registry_empirical` / `seal_dead_end`（判死回写，取证闸 fail-closed，绕过须人工确认）。

**兄弟 skill**：`wq-brain-ra-pipeline`（九步编排）、`wq-brain-campaign-matrix`（选区选集）、`wq-brain-campaign-toolkit`（战役执行引擎）、
`wq-operator-playbook-by-gate`（按闸挑算子）、`brain-alpha-robustness`（Phase C 反过拟合）、
`worldquant-submit-alpha`（提交，须用户确认）、`wqb-concurrency`（槽位纪律）。

<!-- region-scaffold:nav:start -->

| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **KOR 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/KOR/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/KOR/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。

<!-- region-scaffold:nav:end -->

## 区域控制面板

**入场状态**：`active`　TOP600 小宇宙：排除口径 = 数据集级已提交 ≥3 颗（名单查 get_submit_ready(region=KOR)），不按塔排除——pv / risk / analyst 里红的是「已试结构」而非字段，pv47+risk68 换构型即出 failed_ra=0；支配性障碍 = prod 墙（IS 全闸可过、新腿 prod 恒 0.73–0.89；族级判据 = check_correlation 直方图 0.7–0.8 桶 n≥1 ⇒ 密墙别扫窗口）；结构性约束 = 2Y 与 IS 因输入频率此消彼长、会计质量与财务基本面族 S 天花板 0.61，CW 闸升级 FAIL

| 回测设置           | 值           | 来源            |
| -------------- | ----------- | ------------- |
| instrumentType | EQUITY      | settings.json |
| region         | KOR         | settings.json |
| universe       | TOP600      | settings.json |
| delay          | 1           | settings.json |
| neutralization | STATISTICAL | settings.json |
| decay          | 4           | settings.json |
| truncation     | 0.08        | settings.json |
| pasteurization | ON          | settings.json |
| unitHandling   | VERIFY      | settings.json |
| nanHandling    | OFF         | settings.json |
| maxTrade       | OFF         | settings.json |
| language       | FASTEXPR    | settings.json |
| visualization  | false       | settings.json |
| startDate      | 2013-01-01  | settings.json |
| endDate        | 2023-12-31  | settings.json |

| 阈值                                      | 值          | 来源                          |
| --------------------------------------- | ---------- | --------------------------- |
| Mode B 主闸（sharpe / fitness）             | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min                       | 1.58       | thresholds.json             |
| review.fitness_min                      | 1.0        | thresholds.json             |
| review.turnover_min                     | 0.01       | thresholds.json             |
| review.turnover_max                     | 0.7        | thresholds.json             |
| review.two_year_sharpe_min              | 1.0        | thresholds.json             |
| near.sharpe_min                         | 1.0        | thresholds.json             |
| diversity.signal_floor.max_sharpe_floor | 0.5        | thresholds.json             |

**循环与闸门（profile front-matter）**

- 每波探针位上限：1
- 快判死：新数据集 8 探针无 ／S／≥0.5 即判死回写，不扩批（小宇宙烧不起配额）
- 停止条件：白名单被 dead_end 全覆盖
- 闸门特化（文档级）：cw_gate=FAIL、longcount_verdict=FAIL——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**

- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用

## 组合分支（区域 × 类别）

| 类别            | 分组             | 状态     | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件                                                       |
| ------------- | -------------- | ------ | ---- | ---- | ---------- | ------------- | ------- | ---------------------------------------------------------- |
| analyst       | Analyst        | active | —    | —    | 175 / 13   | 2（2）          | 10 / 0  | [references/analyst.md](references/analyst.md)             |
| fundamental   | Fundamental    | active | —    | —    | 171 / 20   | 8（2）          | 6 / 5   | [references/fundamental.md](references/fundamental.md)     |
| shortinterest | ShortInterest  | active | —    | —    | 81 / 5     | 25（20）        | 0 / 0   | [references/shortinterest.md](references/shortinterest.md) |
| pv            | PV             | active | —    | —    | 40 / 0     | 0（0）          | 7 / 0   | [references/pv.md](references/pv.md)                       |
| insiders      | Insider        | active | —    | —    | 27 / 0     | 0（0）          | 1 / 0   | [references/insiders.md](references/insiders.md)           |
| news          | News-Sentiment | active | —    | —    | 27 / 0     | 0（0）          | 4 / 0   | [references/news.md](references/news.md)                   |
| risk          | Risk           | active | —    | —    | 24 / 0     | 0（0）          | 3 / 0   | [references/risk.md](references/risk.md)                   |
| sentiment     | News-Sentiment | active | —    | —    | 18 / 0     | 0（0）          | 3 / 0   | [references/sentiment.md](references/sentiment.md)         |
| other         | Other          | active | —    | —    | 10 / 0     | 4（2）          | 36 / 7  | [references/other.md](references/other.md)                 |
| model         | MODEL          | active | —    | —    | 2 / 0      | 4（4）          | 12 / 0  | [references/model.md](references/model.md)                 |
| institutions  | Institutions   | active | —    | —    | 0 / 0      | 0（0）          | 1 / 0   | [references/institutions.md](references/institutions.md)   |

说明：另有 101 条回测行没写数据集，无法归到组合；证据于 2026-10-04 只读汇总。

## 本区流程差异（相对九步骨架）

> **本节只写「当前有效、已裁决」的结论**（含流程差异 / 硬闸 / 实证判据，≤30 行）。
> **历史层与作废依据**见 [`references/_kor-campaign-log.md`](references/_kor-campaign-log.md)（§0 裁决表，作废项就地标 ⛔）；
> **数值 / 配方 / 逐年表**见 [`references/_kor-gatebreak-evidence.md`](references/_kor-gatebreak-evidence.md)；
> **带日期的一次性产出**（候选 alpha id、已提交颗数、波次 verdict）**优先查台账**，不在文档维护——命令见日志文末「查台账」表。
> ⚠ **该表自带实测覆盖边界**：KOR 台账回写在 **2026-10-04/05 之后就断了**，10-09~10-15 的战役（d219–d282）本地无行 ⇒ 那段以日志正文为唯一记录。
> 铁律 A/B/E/F/G/H/I **一律以正文「铁律总表」与各节为唯一出处**，本表只作速查索引（曾因两处并存而出现编号重复与定义漂移）。

**【硬闸】违反即整批报废或判死错误，无补救**

1. **发批前三闸**：`ensure_safe_for_dispatch` + 新算子 2 条小批验存在性 + 字段 `get_datafields` 实名核对；本地库含已下架数据集 ⇒ **必跑 `preflight_expressions`**。
2. **禁混信号**：多字段组合只走 `trade_when` / `if_else` 条件门控；`add` / `multiply` 相加不同机制字段 = 违规（同字段多窗口 = 单信号结构化，合规）。
3. **「已点亮」= 数据集级已提交 ≥3 颗**，只排除该数据集；**不要按塔排除**。名单查 `get_submit_ready(region="KOR")`。

**【方法】速查索引（定义见正文）**

1. **铁律 A / B**（单边恒正 ⇒ `ts_delta`；方向正反各测，`reverse()` 不精确反号）—— 定义见① 与「铁律总表」。
2. **铁律 E / F / G**（先 raw vs RN 分解；无归因不得发波；波次因果依赖链且候选数 ≤ 上波 1/3）—— 定义见 ③ 与「发波闭环」。
3. **铁律 H**（组装前立机制 + 论坛与外部论文双通道取证，说不出收益来源不许组装）—— 定义见 ②.a / ②.d。
4. **铁律 I**（① 调 L1 六法、② 组装自建，不用 `brain-data-feature-engineering`，只照用其输出契约）—— 定义见 ① / ② 节头。
5. **手写批次必过多样性三闸**：`$WQ_PY tracking/KOR/scripts/scan_diversity.py --audit <批次>`（族数 ≥2 / 未用算子 ≥2 / 单条算子数 <10）。**判死前先自检「真的双构型？真的跨族？」**——只测一个构型会错杀。
6. **两套已验证构型按字段形态分工、不可互换**：PV 构型（日频收益分布型 MATRIX）／ SH 构型（VECTOR 比率流量型）；第三形态 = 裸 `multiply(rank(A),rank(B))`（合规待判）。骨架全文见 [`references/_probe-sop.md`](references/_probe-sop.md)。
7. **换族 / 换壳层必重扫 11 档中性化，不要默认 MARKET**——最优档是**结构特异**的：同一 `pv47` 族，旧结构（decay 4）最优 MARKET，新结构（decay 3 + `group_neutralize(sector)` + tail 0.25/0.75 + pow 0.85）最优 REVERSION_AND_MOMENTUM。
8. **analyst 类字段「名字自解释」≠ 本区可用**——`analyst_factor_signals` 59 字段实测有效仅约 2 个，仍须跑①。

**【实证】数值与战例，查证用**

1. **prod 墙三步处置顺序**（换族 → 换连续桶分组轴 → 加 rank 阈值门控）**每步必实测、不可跨族照搬**：`bucket(rank(cap))` 在 `oth695` 贸易流族 0.89→0.71 ✅，在 `pv47` 峰度族 0.73→**0.83** ❌（且 2Y掉到 0.97）⇒ 同一杠杆跨族可反向。
2. **族级命运判据**：`check_correlation` 直方图 `[0.7,0.8)` 桶 **n≥1 ⇒ 密墙，别扫窗口**；n=0 才可扫 W。
3. **结构性结论**：KOR 强信号与 prod 白空间互斥（IS 全过的族 prod 撞墙，prod 干净的族 S 不过闸）⇒ 单区可提交产出封顶；全破需换 region 或引入机制正交第二族。
4. **returns 缺口只用中性化档解**：KOR `truncation` 多档 returns 逐位相同、`universe` 唯一 TOP600 被平台锁死、仿真 `decay` 只动 TO 不动 returns ⇒ **returns 唯一活轴是中性化档**；实测 `STATISTICAL`(ret .0569/TO .082) < **`CROWDING`(ret .0615/TO .065)**，`CROWDING × decay12` → ret .0638 / margin .00236 / TO .054。⚠ **CROWDING 压 2Y、FAST 提 2Y(1.53)** ⇒ **2Y 与 returns 是对立轴，选档即取舍**。

## 改控制

- **区域级**：`tracking/KOR/config/settings.json`（仿真设置）、`tracking/KOR/config/thresholds.json`（阈值）。
- **组合级**：`tracking/KOR/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence`写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：
  ```bash
  $WQ_PY -m wqb.profiles check --region KOR
  $WQ_PY -m wqb.profiles render --region KOR --apply
  ```
- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[KOR profile](../wq-brain-ra-pipeline/references/regions/KOR.md)（入场裁决、红绿榜、证据附录）。

