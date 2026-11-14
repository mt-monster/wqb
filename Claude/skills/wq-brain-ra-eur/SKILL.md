---
name: wq-brain-ra-eur
description: "在 EUR 区挖 REGULAR alpha、调 EUR 的回测设置或阈值、查 EUR 某类数据集（区域 × 类别组合）的配方与禁区时使用：EUR 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-11-14
---

# EUR 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：EUR 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 EUR 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 EUR，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`full-coverage` 数据集必须做尽（见「全量覆盖操作纪律」）。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region EUR --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region EUR --apply
   $WQ_PY -m wqb.profiles render --region EUR --apply
   ```

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **EUR 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/EUR/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/EUR/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`full-coverage`　⛔ 2026-10-20 起废止探针式派发，数据集必须做尽（字段全量覆盖 / 模板族 ≥3 / 边界算子档穷举）；2026-10-02 的『结构性穷尽』只在探针式派发口径下成立，重开前必须重跑全量覆盖闸。已验证机制两条：① analyst7 四件套修订 surprise（14 颗 RA 全过 / 6 个 metric 族，TOP2500 + FAST + decay 40–80，最大互不相关团 7）；② 慢 MODEL 残差 × 快 PV（加权写法已被闸 5 禁止，只许条件 / 分组 / 残差三式，SUBINDUSTRY + decay4）

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | EUR | settings.json |
| universe | TOPCS1600 | settings.json |
| delay | 1 | settings.json |
| neutralization | SUBINDUSTRY | settings.json |
| decay | 4 | settings.json |
| truncation | 0.08 | settings.json |
| maxTrade | OFF | settings.json（强制 OFF） |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | ON | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |
| startDate | 2014-01-01 | settings.json |
| endDate | 2023-12-31 | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.05 | thresholds.json |
| review.turnover_max | 0.3 | thresholds.json |
| review.two_year_sharpe_min | 1.6 | thresholds.json |
| review.rn_sharpe_min | 1.0 | thresholds.json |
| near.sharpe_min | 1.2 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.5 | thresholds.json |

**循环与闸门（profile front-matter）**
- ⛔ 每波派发走**全量覆盖**：字段覆盖率 ≥ 100%、模板族 ≥ 3、边界算子档穷举（详见「全量覆盖操作纪律」）。
- 快判死：缺省（决策表 D15：新数据集 8 探针无 ／S／≥0.5 即判死）仅适用于单字段级——数据集级判死必须先通过三道覆盖闸，任何一闸未过都不允许判死该数据集
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：EUR/D1 结构性穷尽（2026-10-02 历史结论，2026-10-20 起冻结）——升 active 须出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源，或全量覆盖闸三闸均过但候选 ／S／ 全 <0.5
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙跨多个国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组有意义
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| fundamental | Fundamental | active | — | — | 557 / 41 | 54（22） | 7 / 0 | [references/fundamental.md](references/fundamental.md) |
| other | Other | active | — | — | 345 / 3 | 116（44） | 21 / 2 | [references/other.md](references/other.md) |
| analyst | Analyst | active | — | — | 311 / 22 | 20（6） | 14 / 6 | [references/analyst.md](references/analyst.md) |
| model | MODEL | active | — | — | 211 / 3 | 15（2） | 67 / 3 | [references/model.md](references/model.md) |
| pv | PV | active | — | — | 140 / 10 | 12（1） | 12 / 0 | [references/pv.md](references/pv.md) |
| risk | Risk | active | — | — | 94 / 5 | 22（3） | 8 / 1 | [references/risk.md](references/risk.md) |
| insiders | Insider | active | — | — | 65 / 6 | 3（0） | 2 / 2 | [references/insiders.md](references/insiders.md) |
| news | News-Sentiment | active | — | — | 60 / 0 | 0（0） | 17 / 0 | [references/news.md](references/news.md) |
| sentiment | News-Sentiment | active | — | — | 49 / 6 | 3（3） | 4 / 0 | [references/sentiment.md](references/sentiment.md) |
| institutions | Institutions | active | — | — | 48 / 0 | 0（0） | 4 / 0 | [references/institutions.md](references/institutions.md) |
| earnings | Earnings | active | — | — | 39 / 0 | 0（0） | 4 / 0 | [references/earnings.md](references/earnings.md) |
| socialmedia | News-Sentiment | active | — | — | 10 / 0 | 0（0） | 2 / 0 | [references/socialmedia.md](references/socialmedia.md) |
| macro | Other | active | — | — | 9 / 0 | 0（0） | 0 / 0 | [references/macro.md](references/macro.md) |

说明：另有 2060 条回测行没写数据集，无法归到组合；5 条判死 / 胜绩连类别也推断不出；证据于 2026-11-07 只读汇总。
<!-- profiles:cells-index:end -->

## 六步纵深骨架（本区覆盖）
## ⛔ 发批前塔位核对（2026-11-10 新增，发批 checklist 第一条）

**规则**：`get_datasets` 拉当前塔位 → 对照已点亮塔清单 → 数据集 category 落在已点亮塔 ⇒ **不发批、不探针、不花配额**。

- EUR D1 已点亮塔（截至 2026-11-10）：**analyst 10 / model 3 / fundamental 3 / imbalance 3**
- 即使是「补测」「重测」「换配置重试」也算投入挖掘，同样禁止
- 用户点名已点亮塔数据集时：**先报告塔位冲突再等用户确认**，不自行发批
- 事故记录：2026-11-10 连发 4 批 36 条仿真到 model354（model 3/3）与 analyst10（analyst 10/3），全部浪费


> 通用方法见 [六步纵深骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> 本节只写 **EUR 的 override**：主 skills 未覆盖的本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skills 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

### ① 六法体检 · 本区覆盖

- **回测设置以 `settings.json` 为准**：`TOPCS1600` / `SUBINDUSTRY` / `decay 4` / `maxTrade ON` / `nanHandling ON`。
  ⚠ 这是**区域缺省**，不是全部。`analyst7` 修正族与 `techindi_model` 都必须 **TOP2500 / FAST / decay 40**（详见下方 S3 例外与 ④）。
- **universe 不是禁区，是 prod–S 前沿上的平移旋钮**（2026-10-29 修订）：同一公式 TOPCS1600 → TOP2500 实测
  S 1.99→**2.57**、sub 1.37→**1.80**、2Y 2.06→2.34（并把两条 rob FAIL 修成 0 fail），但 prod 也从 0.7454 抬到 0.7794（**+0.034**）
  ⇒ **换 universe = 决定把余量花在哪个闸上**。S/sub 不足时可换，prod 已贴闸时不要换。
- **待实测**：离线体检包退化范围、不可用算子。

### ② 组装 · 本区覆盖

- **⛔ 全量覆盖闸前置**：派批前必须过 `tools/full_coverage_gate.py --gate-mode enforce`（字段/模板族/边界算子三闸），任一未过不允许送回测。
- **禁止探针式派批**：8–10 槽位必须覆盖该数据集 ≥60% 字段（配合闸 1）且 ≥3 模板族（配合闸 2），不是"双结构 × 4 字段"的稀疏派发。
- **待实测**：本区组装禁区（新信号源优先）。

### ③ 归因 · 本区覆盖

- **结构性穷尽判据（2026-10-20 起冻结）**：库存 47/47 族 prod 都不低于上限、7 战役全 exhausted 的结论**只在探针式派发口径下成立**。2026-10-20 起改用全量覆盖闸，任何判死必须**三闸全过**才允许。
- **待实测**：本区逐年 S 分布（历史 win 机制 = 慢 MODEL 残差）。

### ④ 破闸杠杆 · 本区覆盖

- **★ 闸线（本区实测）**：`LOW_SHARPE` 1.58｜`LOW_FITNESS` 1.0｜`LOW_TURNOVER` 0.01｜`HIGH_TURNOVER` 0.7｜`LOW_2Y_SHARPE` 1.58｜`LOW_SUB_UNIVERSE_SHARPE` = **0.52×S（比率闸）**｜`LOW_ROBUST_UNIVERSE_SHARPE` 0.7。
- **★ 高 S 是双刃剑**：sub 是比率闸 ⇒ `sub/S < 0.52` 时任何 S 都过不了 ⇒ **选「刚好过主闸」的 S，不追最高 S**。
- **★ F 的实操门槛（2026-10-29 量化）**：闭式 `F = S^1.5 × sqrt(vol/0.125)` 在 EUR 低波动族上等价于 **S ≥ 1.75 才过 F ≥ 1.0**（S 1.62 ⇒ F 0.87；S 1.71 ⇒ F 0.97）。
  ⇒ 卡 F 不等于结构错，先看 S 够不够；`returns` 提不动（EUR 普遍 <0.03），只能提 S。

**★ 未点亮塔：不是「数学上封闭」，是「必须换形态」**（2026-10-28/29 修订，旧记「路径数学上封闭」已作废）

旧记的闭式 `Fitness 上限 ≈ Sharpe × sqrt(returns/0.125)` **只对单腿成立**。未点亮类别单数据集硬挖确实死（97 条实证，最好 S 0.56 = 闸线 1/3），但**唯一可行形态是：

```
已点亮强腿（高 2Y，占主体） ＋ 1.2 权重的未点亮小腿（只带塔位）
```

实证：`group_neutralize(group_scale(add(<ebt 广度 2.1>, multiply(1.2, <未点亮腿>))), industry), market)`
→ 2Y 2.10–2.62、sub 1.11–1.20、`failed_ra_count=0`，pyramid 变成 `[ANALYST, <未点亮类>]`。
已用它点亮 **SENTIMENT(×1.4)** 与 **INSTITUTIONS(×1.1)**。

- **倾斜腿选塔按倍率**：sentiment **1.4** > news 1.3 ≈ analyst/model 1.3 > institutions **1.1**。
- **倾斜腿贡献**：2Y **+0.78**、sub +0.09、prod **−0.004**（≈无效）。
  ⇒ **它不增加席位数**（同基底换倾斜腿互测 0.948–0.970），只决定点亮哪个塔 + 过 2Y/sub 闸。
- **组腿规则（2026-10-29 用户新规，取代旧「跨集全禁」）**：
  - 禁区三类 = `PV` / `MODEL` / `OTHER`。**内部两两禁**（PV+PV / MODEL+MODEL / OTHER+OTHER）＋**彼此之间两两禁**（PV+MODEL / PV+OTHER / MODEL+OTHER）。
  - **可与其它 category 跨类组腿**（PV+NEWS / MODEL+FUNDAMENTAL / OTHER+ANALYST / OTHER+INSTITUTIONS …）✅
  - ⚠ **但含禁区类的跨类组合全账号仅限 5 个** ⇒ 用前先盘点已占用几个（`get_user_alphas` 读 `pyramids.list`，凡含 pv/model/other 且段数 ≥2 的计入）。
  - 等价：一条腿序列里 `PV/MODEL/OTHER` 合计最多出现 1 次。**这是本区点未点亮塔时最紧的预算**。
- ⚠ **开波前先扫库存里的成功样本**：`get_user_alphas(region=EUR, stage=OS)` 里凡是 `pyramids.list` 有两段的，都是这个形态的现成模板
  （如 `Xgojww1X` = `[RISK, NEWS]`，NEWS 腿是**新闻条数=关注度**，不是情绪极性分）。

**★ prod 杠杆实测排序**（EUR，逐项单加，同一族基准 0.7973）

| 杠杆 | Δprod | 备注 |
|---|---|---|
| **`group_scale(·, industry)`** | **−0.057** | 唯一四项同得（S/2Y/sub 全↑）；⭐ 首选 |
| 换读数（`/num` → `/num_4wks_ago`） | −0.051 | 同字段语义变体，换的是"分母" |
| 幂次 +0.4 | −0.027 | 上限 2.1（2.4 ⇒ F 0.96 FAIL） |
| cap 20 桶中性化 | −0.025 | 前置 `IS_LADDER ≥ 2.02` |
| 加 1.2 权重倾斜腿 | **+0.013** | **反效果**（别用它降 prod） |

- **`group_scale` 有读数依赖**：输入必须是「截面可比分数」（广度 / 多腿 rank 合成 / 模型预测分）⇒ 可用；
  输入是「单股时序标准化幅度」或水平量 ⇒ **破坏性**（analyst7 ebi 幅度 S 1.97→1.14；fundamental23 sub 崩到 0.63–0.76）。
- **prod 由「读数」决定，2Y 由「科目」决定**（两个独立旋钮，别混）：
  - 同读数换科目：prod 只差 0.025（扩散 ebt 0.7801 vs ebi 0.7549）。
  - 同科目换读数：prod 差 **0.10–0.13**（广度 `/num_4wks_ago` 0.653–0.675 vs 扩散指数 0.755–0.780）。
  - 2Y 同理：ebt 2.12–2.62 / dps 2.41 / gps 2.02 ≫ **ebi·eps·sal 天花板 1.46–1.57**（幅度/广度/双读数三路全撞）。
  ⇒ **2Y 不足时第一步换科目，不调结构**；**prod 不足时第一步换读数，不换科目**。

### ⑤ 算子穷举 · 本区覆盖

- **⛔ 边界算子白名单**：表达式里出现的每个算子，其参数必须落在 [references/_boundary-ops-eur.md](references/_boundary-ops-eur.md) 列出的合法档内；不在此表内的档需要**先补一次实测**、把档加进本表后再用。
- **近闸候选必须穷举 min_coverage 档**：cheap gate 已过但 RA 至少 1 项 FAIL 的候选，其表达式中每个算子的档位必须已试完边界清单里的 min_coverage 档（如 signed_power ≥3 档、ts_mean ≥2 档）。
- **机器可读版本**：`tracking/EUR/reference/boundary_ops_eur.json`（含 `poison_structures` 禁用结构清单）。
- **判定入口**：`tools/full_coverage_gate.py --near-gate`。

### ⑥ 终验 · 本区覆盖

- **⛔ 批量派 prod 前必做本地互测（2026-10-29 新增，血的教训）**：`check_correlation(type=self)` **只跟已提交池比**，
  同基底换倾斜腿的候选 self 可各报 0.51（全"通过"）而**彼此 0.948–0.970**。
  一批候选在花 prod 槽之前，必须先跑 `compute_mutual_correlation`（**纯本地/不占队列/零成本**），
  只看 `max_mutually_below_subset`；不在该集合里的候选，即使 IS 全过也不测 prod。
- **数据集级判死唯一合法路径**：三道覆盖闸全过 + 全波次 |S|<0.5 ⇒ 该数据集可入 dead_end。任一闸未过 = 未做尽、**不允许**判死。
  ⚠ **例外（覆盖率闸）**：数据集 cov < 0.85 时 sub 闸结构性不可达（`fundamental28` 1605 字段 cov 恒 0.50 → sub 0.52 vs 限 0.82），
  此类"覆盖不足"可凭 cov 直接判死，不必跑三闸。
- **判死前必查**：`tools/full_coverage_gate.py --candidates <last_wave>.json --gate-mode enforce --campaign-dir tracking/EUR --json` 输出 `ok=true` 才允许提交 `seal_dead_end`。
- **★★★ prod 拥挤预判（2026-11-09 eur15 FHP 实证）**：prod 池是**全球跨区提交**——EUR 本地字段 aC 冷 ≠ prod 干净；**论坛已公开记录的优质信号 = 生产池已占位**（FHP A1VXNQbe 全 IS 闸 fRA=0、self 0.17，prod 仍 0.8881 族级墙）。近闸候选**先测族代表 prod** 再投入全闸打磨；选题优先全球冷机制（论坛热度只作反向参考）。配套 `wq-prod-corr-read` 族代表判据（max>0.80 整族降级）。
- **判死一个「类别」前，先读该类别已出货 alpha 的 code**：`get_user_alphas` 取该类别 ACTIVE 的 id → `get_alpha_details` 读 `regular.code`。
  用它的**信号类型**（关注度 vs 极性、广度 vs 幅度）作起点。反例：news 类的成功样本用的是"新闻条数=关注度"（`mws46_ravenpack_sum_story_count`），
  而按数据集名去测情绪极性分 77 条全部 S<0.6 —— 方向本身就错。
- **升档条件**：出现 returns 达 0.05 且 prod 直方图不是密墙的新信号源，**或**三闸全过但候选 |S| 全 <0.5。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **入场**：2026-10-20 起 **full-coverage**（废止探针式派发）——数据集必须做尽：字段 100% 覆盖、模板族 ≥3、边界算子档穷举。历史 2026-10-02 判定的"结构性穷尽"（47/47 族 prod 都不低于上限、7 个战役全 exhausted）**只在探针式派发口径下成立**，本区升 active 须重跑全量覆盖闸。
- **S0 选集**：未点亮塔不是"数学封闭"，是"必须换形态"——单数据集硬挖死（97 条实证最好 S 0.56），
  但「已点亮强腿 + 1.2 权重未点亮小腿」能点亮（已实证 SENTIMENT / INSTITUTIONS）。详见 ④。
- **S3 回测**：区域缺省 TOPCS1600 / SUBINDUSTRY / decay 4 / maxTrade ON / nanHandling ON；
  ⚠ universe 是 prod–S 平移旋钮（TOP2500 抬 S/sub 也抬 prod +0.034），analyst7 与 techindi 需用 TOP2500 / FAST / decay 40。详见 ①。
- **S3 例外（已验证配方自带设置）**：`analyst7` 修订族 ATOM 必须 **TOP2500 / FAST / decay 40–80 / nanHandling ON / maxTrade ON**（与区域缺省不同）。`explain` 只回区域缺省，直发 MCP 要逐项显式传，否则跑的是另一条信号。一个 `create_multi_simulation` 只带一个 settings 块，参数名只认 snake_case——派发后读回一个子项断言 `nanHandling` / `maxTrade` 为 ON。完整配方见 [references/_atom-revision-playbook.md](references/_atom-revision-playbook.md)。
- **S4 改进**：prod 墙不是单一路径。① **残差化**（见 [EUR × fundamental](references/fundamental.md)：换维度、替换优于叠加、hump 档位；换分母在 EUR 是毒药）；② **同数据集换 metric 族**（analyst7 用 6 族出 14 颗，是最快的席位扩张）；③ **2Y/CV 修复用制度门控** `trade_when(abs(ts_zscore(<单字段水平值>, 66)) > 1.0, CORE, 0)`（`Grge2lN3` Recent-3yr CV 由 .436 降到 .366；计数门控反向）；④ decay / 平滑按形态分档（幅度 d40、广度 d80 + `ts_mean(·,5)`）。
- **S5 提交**：prod 与 self 双端点都取 max；**同族 p 变体互相关 0.97–0.99 ⇒ 每族只 1 席**，hump / decay 这类只改时序的变体全部作废（self 会爆）；「14 颗全过 ≠ 14 颗可同时提交」，analyst7 的最大互不相关团 = 7。
- **analyst 类别旧判死作废**：`analyst7` 不是 0.10 死集（旧记 299 字段是分页截断，真实 1111）；「Analyst 只能出 1 颗」「要凑 RA 腿必须离开 analyst」只对 `analyst_factor_signals` 旧结构成立。见 [references/analyst.md](references/analyst.md) 顶部覆盖说明。
（来源：EUR profile）

### ★★★★★ 数据集普查表（先读这个，跳开已判死族）

**EUR 共 173 个数据集 / 14 类**（未点亮 93 / 已测 ≈25 / 未测 60）。
全量清单 + 逐数据集判死速查（死因七分类）+ 未测集排序 见 [references/_dataset-inventory.md](references/_dataset-inventory.md)。

**组合候选清单（combo-candidate-inventory）**：EUR 版「正交骨架 × 加权饱和卫星」配方实证（含账本机制占用图、qfl 骨架、`subtract(骨架, w×rank(卫星))` 配方与 `w=0.5` 甜点） 见 [references/_combo-candidate-inventory.md](references/_combo-candidate-inventory.md)。
⇒ 开波前先读它，30 秒排除已判死族；**任何「穷尽」声明前必须重跑全量枚举**（曾经误记 21/33 个）。

### ★★★★★ 全量覆盖操作纪律（2026-10-20 定稿，废止探针式派发）

**核心口径**：一旦锁定某数据集，必须**枚举其全部字段语义维度 × 全部模板族**才算测完。**不允许"跑 10 条就换集"**。数据集级判死必须**先通过三道覆盖闸**：

| 闸 | 语义 | 判据 | 工具 |
|---|---|---|---|
| **1. 字段全量覆盖闸** | 数据集内每个字段至少出现在 1 条候选表达式里 | `coverage ≥ 1.0`（100%） | `tools/full_coverage_gate.py` |
| **2. 模板族全量闸** | 本数据集至少试跑 ≥3 个模板族 | `--min-families ≥ 3`（默认 3） | 同上 |
| **3. 边界算子穷举闸** | 表达式里每个算子的参数落在合法档；近闸候选已试完 min_coverage 档 | 见 [references/_boundary-ops-eur.md](references/_boundary-ops-eur.md) + `tracking/EUR/reference/boundary_ops_eur.json` | 同上 |

**开波顺序（不可跳步）**：

1. **反向检索**：查 `data/wqb.db::backtest_results` 里本 region 全部 RA 全过的 alpha，按 dataset 聚类、按 2Y≥1.58 排序，只从"已证明能出货"的集出发做尽（详见 MEMORY §0）。
2. **拉字段清单**：`tracking/EUR/reference/eur_<dataset>_fields.json` 或 MCP `get_datafields`；**无字段目录不允许派批**。
3. **画语义维度地图**：按经济机制（事件驱动 / 基本面 / 情绪 / 分析师 / 价量）分组，按 `alphaCount` 升序排。
4. **过覆盖闸**：`python tools/full_coverage_gate.py --region EUR --dataset <ds> --candidates <cand>.json --gate-mode enforce --campaign-dir tracking/EUR`；三闸全过才允许送 `wave_gate.py` 走回测。
   ⚠ **族闸文件名陷阱（2026-11-09 eur15 两次实测升级）**：族闸按候选文件名 stem 与首 token 两个键登记、按 **dataset 全名**查询——**候选文件 stem 必须与 dataset 全名完全一致**（`insider_matrix.json`）；含下划线数据集名的 `_wave1` 后缀变体（`insider_matrix_wave1.json`）两个登记键都不匹配（全 stem 带 `_wave1`、首 token 是 `insider`），新数据集无 DB 族历史时必然 FAIL 0/3。无下划线数据集可用 `<ds>_wave1.json`（首 token=ds 命中）。
5. **回测近闸候选**（cheap gate 过但 RA 未全过）必须启用 `--near-gate`：边界算子需已试完 min_coverage 档，否则 FAIL。
6. **判死条件**（**唯一合法**）：三闸全过 + 全波次 |S|<0.5 ⇒ 该数据集可入 dead_end；三闸任一未过 = 未做尽、不允许判死。

**⛔ 违规反例（禁做）**：
- 只跑 3-5 条表达式就换数据集 ⇒ 违反闸 1。
- 只用一种模板族（如只跑 `signed_power + group_rank`）⇒ 违反闸 2。
- 只测 `decay=4` 一档、只测 `signed_power 2.5` 一档 ⇒ 违反闸 3。
- 近闸候选未穷举 signed_power 全部档就换方向 ⇒ 违反闸 3 near_gate 分支。

**参考文件**：
- 边界算子清单（人可读）：[references/_boundary-ops-eur.md](references/_boundary-ops-eur.md)
- 边界算子配置（机器读）：`tracking/EUR/reference/boundary_ops_eur.json`
- 闸门脚本：`tools/full_coverage_gate.py`
- 已归档的探针 SOP（历史留档，**不再适用**）：`attic/probe_sop_retired_20261020/_probe-sop.md`

**EUR 设置档（平台权威 `get_platform_setting_options`）**：universe = `TOPCS1600`｜`TOP2500`｜`TOP1200`｜`TOP800`｜`TOP400`（实测 **TOPCS1600 最优**）；中性化 12 档（实测 **SUBINDUSTRY 最优**）；multi-sim **2–10 条**。
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/EUR/config/settings.json`（仿真设置）、`tracking/EUR/config/thresholds.json`（阈值）。
- **组合级**：`tracking/EUR/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region EUR
  $WQ_PY -m wqb.profiles render --region EUR --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[EUR profile](../wq-brain-ra-pipeline/references/regions/EUR.md)（入场裁决、红绿榜、证据附录）。

## ★ 2026-11-09 实战 override（techindi_model 战役，覆盖上文同名结论）

> 下文每条均为 EUR/TOP2500/D1 实测，覆盖本文件上方与之冲突的旧结论。

### 1. 设置档实况（修正「TOPCS1600 最优 / SUBINDUSTRY 最优」）

| 轴 | 旧结论 | 本轮实测 | 结论 |
|---|---|---|---|
| universe | TOPCS1600 最优 | TOP2500 全闸；**TOP1200 全灭（S1.61）**；**TOP800 更差（S1.42/2Y0.81）** | **大宇宙是必要条件**，TOP2500 ≥ TOPCS1600 |
| neutralization | SUBINDUSTRY 最优 | **CROWDING**：7/8 全闸 + sub 1.70（全池最高）+ prod 0.7289（最低） | **prod 卡墙优先 CROWDING** |
| neutralization（F 维） | — | **INDUSTRY / MARKET**：F +0.21、ret +1.04pp、S 持平 | **F 不足优先 IND/MKT**（唯一不牺牲 S 的 F 杠杆） |
| decay | 4 | 8 为甜点；**16 过度平滑**（S 崩至 1.75–2.43） | decay 8 |
| truncation | 0.08 | 0.05 / 0.08 / 0.15 **指标逐位相同** | **不是杠杆，勿再扫** |
| maxTrade | ON（settings.json） | 本轮全程 **OFF**，全闸件正常产出 | 两种都可用，按数据集定 |

### 2. ★ prod 与 S 是 U 形（不是单调）

| S | 4.29 | 3.66 | 2.90 | 2.32 | 2.28 | **2.05** | 1.96 |
|---|---:|---:|---:|---:|---:|---:|---:|
| prod | 0.8175 | 0.8134 | 0.7289 | 0.7092 | 0.6881 | **0.6476** | 0.7240↑ |

**极小值在 S ≈ 2.0–2.3。** 想破 prod 0.7 ⇒ **目标 S 锁 [2.0, 2.3]**；S 太高压不住拥挤，S 太低（<2.0）持仓过度平滑反与特定产品重合、prod 回升。

### 3. ★ 两条有效杠杆（本役唯一两个真正动过闸的）

1. **跨塔稀释**（禁混集合内 × 集合外，秩空间等权，配额 ≤5）：TO 25%→10%、ret 仅 −2.4pp、**prod −0.064**。
   三腿配方（已交付 `P0oR7vYw` / `leAnKOEA`）：
   `group_rank(add(add(group_rank(prob_P4_minus_P0,industry),group_rank(eps_revision_magnitude/ts_mean(eps_y1_estimate_coeff_var,55),industry)),group_rank(ts_backfill(eur_director_signal_value_1,66),industry)),industry)` <!-- lint:counterexample: 已交付三腿配方的历史记录，非生成端新配方 -->
   前提三缺一不可：① 主腿 S 大余量；② 稀释腿与主腿低相关且自身 prod 干净；③ 主腿 ret 厚。
2. **neutralization → CROWDING**：prod −0.0175、sub 抬到 1.70。

### 4. ★ 容量定律：可出席位 ≈ 独立底层信号数（不是字段/切面数）

- `techindi_model` 内 **2 个独立模型族**：`probability_*`（294 字段，分位概率）与 `tm_1..19_*`（399 字段，回归输出 + log-softmax），**跨族互相关仅 0.13–0.24**。
- 89 个切面（分位 × horizon × 命名方案 × 模型变体）能把互相关从 0.95 降到 0.24，但 **17 件全闸件的 0.5 最大独立集仍是 3 席**（切面不增席）。
- 加入 tm_ 族后 **3 席 → 4 席**（`MPYEEwj8` / `58EmKpkk` / `O0ALVWmJ` / `LLMvveP2`，精确解）。
- ⇒ **凑席位先换「模型族」，再换切面，最后才换稀释腿。** 判据：看该数据集有几个独立模型族，每族值 ~2 席。

### 5. ★ 选集排序修正：ret 量级先验 > aC > cov

「aC 极低 + cov 极高」**不等于**有信号。本役三集（1649 字段，aC 0–8，cov 0.95–0.998）全部首波判死，死因同型：ret 0.12–3.24% ⇒ F 天花板 0.34–0.44。

**只有两类信息能出 F≥1.0**：
- ✅ **真预测型** = 模型输出**未来收益/概率的连续值**（techindi 的 probability bucket、dl_riskfree 的 label 概率）
- ✅ **定价压力型** = 借券费率 / 拥挤度 / 资金流等直接反映供需失衡的量（risk60，ret 7.9–10.5%）

**必须排除的「伪预测型」**：字段名含 `percentile` / `rank` / `score` / `similarity` / `grade` ⇒ 静态分位排名，**TO 会低于 5%、ret 极薄**，不值得开波。已判死：`pattern_scores` / `continuation_score` / `intraday_pv_feats` / `acquisition_model`。

### 6. 族级判死优先于维度级

同族换维度**不改变 F 天花板**：内部人交易族金额维度 F 0.54（`insider_matrix`）、笔数维度 F 0.52（`insider_trx_matrix`）。一个维度穷尽判死，同族其它维度大概率同命 ⇒ **先看族实证，再决定是否开波**。

### 7. 工程铁律（本役实测踩过）

1. **category 必须实查** `get_datasets` 返回值，不能按名字推断：`insider_matrix` / `insider_feats` / `insider_trx_matrix` / `earningscall_sentiment` **实际全是 other 类**。INSIDERS 塔在 EUR 真只有 3 个集（`insider_agg_matrix` / `insiders1` / `insiders12`），EARNINGS 塔真 0 个可用集。
2. **发批必须二验** `batch_status`：曾出现返回 id 但平台 404。
3. **发批前必须 preflight**：1 个字段不存在会导致**整批** `No alpha_id in sim response`（第三批 10/10 全废）。
4. **`toolkit_static` 静态闸会拦两类写法**：① 显式加权腿混合（`0.7*A+0.3*B`，毒模式 `weighted_leg_mix_func_suffix`）整批拒绝；② `hump` 第二参数**必须命名** `hump(x,hump=0.01)`。
5. **prod 读取的三类阻塞**：① `correlation_busy` = 账号级单并发槽被别处持有（retry 240s 不会因重试加快）；② MCP `check_correlation` 120s 硬上限 vs 平台 4–8 分钟 ⇒ **超时后计算被丢弃**，需重新触发；③ `--peek` 只读缓存**不触发计算**，新件首测必须先打一次 MCP 再 peek。判据：间隔 >10 分钟仍空体 = 计算已丢弃。

### 8. 本役交付与容量实况（避免重复劳动）

- **已 2 颗全闸+prod 验证**：`P0oR7vYw`（S2.28/F1.61/2Y2.42/TO9.24%/margin13.48bp/self0.5347/**prod0.6881**）、`leAnKOEA`（S2.05/F1.39/2Y2.48/TO7.15%/margin16.13bp/self0.4625/**prod0.6476**）。
- ⚠ 二者互相关 **0.7837 > 0.7** ⇒ **只能提交其中一颗**（先提一颗，另一颗 self 必爆）。
- **33 个数据集已实测判定，仅 `techindi_model` 出货**；4 个 0 塔位 category（macro/socialmedia/earnings/institutions）**物理不可达**。
- EUR 可交付容量实测 **约 4 席** ⇒ 15 颗目标需换区或调整。



## 2026-11-11 战役新增方法论（详档见 references/_boundary-ops-eur.md）

1. **判死前穷尽度六维检查**（硬约束）：≥10 结构互异模板跨机制面 / 字段族自测 / 矩全家 / ≥2 分组轴 / 非线性门控 / ≥2 配置——单配置判死无效
2. **机制发现范式**（news20 门控族实证）：基线探针 → 方向对照（反号翻号验证）→ 阈值曲线（单调性=机制为真）→ 平滑曲线（倒 U 找峰）→ 幂次曲线（头部锐化）→ 跨集矩阵（通用性 vs 数据质量归因）
3. **跨集验证归因**：同 vendor 同类字段仅一集出信号 ⇒ 机制依赖数据质量而非结构通用性——选集时按数据质量分层，勿假设机制可移植
4. **多重检验极值回归**：单批 max|S| 是极值，跨批复测回归后才可信；nanHandling=ON 下 multiply(-1) 不严格翻号，反向验证须用同表达式跑第二配置
5. **平台偶发全批 FAIL 鉴别**：同字段同结构重试 2 条即判别（不必全批重发）
6. **★「F 不变量」修正（2026-11-11 val100 实证，覆盖 eur15 定律 #2）**：F = S×sqrt(ret/max(TO,0.125)) 中 ret/TO 不是信号不变量——它只在**秩空间重整**（group_rank 内外换轴/幂次前置）时近似守恒；**幅度空间变换会真改 F**：同一 val100 信号，group_rank(industry) ret 7.5%/F 0.61，group_neutralize(market)（保留原始幅度）ret 12.9%/F 0.74。破 F 闸第一杠杆 = 幅度保留形态（group_neutralize 替代 group_rank）+ 轻时序整形（ts_decay_linear 家族）；平台 decay 是持仓平滑，同步砍 ret 与 TO，F 不动且 S 崩。
7. **★ 近闸判死纪律补丁（2026-11-11）**：S 过闸候选在「截面算子全家（rank/group_rank×4轴/group_zscore×5轴/group_neutralize×5轴/bucket/quantile/normalize/tail/winsorize/幂次后置）× 时序重整（ts_rank/ts_zscore/ts_decay_linear/ts_quantile/SNR/去均值）× 设置轴（中性化 12 档×宇宙 5 档）」穷举完之前不允许判死；幂次放 group_rank 参数内是不变变换（白测），必须施加在 group_rank/group_neutralize **输出**上才是真杠杆。


## ★★ 2026-11-13 战役 override（未点亮塔纯 ATOM 战役：六法判据被推翻）

> 本役在 EUR 未点亮塔 7 类 36 个数据集上做了 S1（36 集判定 + 36 份字段目录 + 26 集 s1_semantic）→ S2（13 字段六法在线）→ S3（4 份机制模板）→ S4（10 波回测 + 逐波归因）。以下每条均覆盖上文同名结论。

### 1. ⛔ 六法（字段画像）读数**不能**预测可交付性（本役最重要的修正）

同一字段「NONE 中性化六法」vs「SUBINDUSTRY group_rank 后」的 S：

| 字段 | 六法 S | 中性化后 S | 衰减 |
|---|---:|---:|---|
| institutions6 `count_institutional_buyers_security` | 0.97 | **0.16** | -84% |
| pv37 `pv37_downvolume` | 0.83（F 1.12） | **0.02** | -98% |
| rsk62 `rsk62_return` | -0.07（双边） | **-1.09** | 方向反转 |
| rsk62 `rsk62_1_100_intercept` | 0.89（双边） | **0.51** | -43%（最小） |
| rsk60 `rsk60_crowding` | 0.81（双边，TO169%） | **0.41**（TO13.8%） | -49% |

**机制**：`NONE` 下 `longCount` 巨大而 `shortCount=0` 的字段，量到的是**单边市场/规模暴露（beta-like exposure）**，不是跨股票选股 alpha。一旦 `group_rank` 行业/市场相对化，持仓变**对称多空**、信号归零。

**据此改写纪律**：
1. 六法**只用于形态诊断**（类型/覆盖/频率/量纲/中心趋势/分布）与预处理决策，**不得用于可交付性判断，也不得据它排选集优先级**。
2. 可交付性一律看「行业中性化 + 横截面相对化」后的 S/sub/2Y。
3. **对称多空 + S≈0 = 纯噪声**（如 pv37 709/709、institutions6 680/682），立即淘汰，不要继续调参。
4. 唯一例外：六法阶段就 `shortCount≠0` 的双边字段衰减较小（intercept 0.89→0.51），可优先投入。

### 2. ★ 算子族的正确试错顺序：**先时序族，后截面族**（本役 5 字段实证）

pv37 `pv37_downvolume` 上的完整梯度：

| 算子族 | 表达式 | S |
|---|---|---:|
| 截面族 | `group_rank(裸值, industry / market / subindustry)` | 0.02 / 0.00 / 0.02 |
| 截面族+幂次 | `signed_power(group_rank(裸值), 1.5 / 2.0)` | 0.04 / 0.03 |
| **时序族** | `group_rank(ts_rank(ts_backfill(F,5), 66), subindustry)` | **1.89** |

⇒ **信息若编码在「相对自身历史的异常度」里，截面族全灭而时序族出强信号；反之亦然。**
**先判字段是「横截面型」还是「时序型」，再选算子族**；判反方向时，换轴/换幂次/换窗全部白测（本役在 pv37 上白测 5 条）。
判据：先跑 `group_rank(裸值)` 与 `ts_rank(裸值,66)` 各 1 条作**族探针**，再决定往哪族投入。

### 3. risk 族四集统一形态：**裸值必死，掩码/时序分位才活**

| 字段 | 裸值 S / TO | 处理后可活形态 | 处理后 S / TO |
|---|---|---|---|
| rsk68_residual_return | 0.80 / **67.2%** | `!=0` 掩码 | 0.88 / 0.57% |
| rsk70_mfm2_euetrd_strevrsl | 0.59 / 38.2% | `!=0` 掩码 | 0.88 / 0.45% |
| rsk72_top1200_dsrt | **-0.54** / 145.7% | `!=0` 掩码 | **+0.70** / 2.1% |
| rsk62_return | -0.07 / 145.7% | `!=0` 掩码 | 0.84 / 14.8% |

⇒ risk 族裸值换手 38–146% 且方向不可靠；**`!=0` 掩码是降到 0.5–2% 换手的单点杠杆**（long 常翻倍 ⇒ 重度零膨胀）。
⚠ 但掩码在**双边字段**上会毁掉空头腿（crowding 0.81→0.51、short 191→0），不可滥用。

### 4. ★ 2Y 闸的真实可达性：换窗口救不了「近两年失效」（pv37 三档实证）

| 形态 | S | TO | 2Y |
|---|---:|---:|---:|
| `ts_rank(·,66)` | 1.89 | 59.7% | **0.04** |
| `ts_rank(·,252)` | 1.90 | 53.5% | **-0.04** |
| `ts_rank(66)`+`ts_decay_linear(20)` | 1.44 | 14.9% | **0.17** |

⇒ 窗口 66→252 **不改 2Y（0.04→-0.04）**；降换手只把 2Y 抬 0.13 而 S 掉 0.45。
**结论**：`LOW_2Y_SHARPE` 1.58 是**信号时效闸**，不是形态闸。若某机制在 2022-2023 失效，任何窗口/平滑都救不回来——应立即换字段或换读数，不要投入第三波。

### 5. 本役交付实况（避免重复劳动）

- **20 颗目标在本口径（只未点亮塔 + 纯 ATOM）不可达**：36 集纯 ATOM 历史最好 S1.36（`rsk60_offer`），本役新增最好为 pv37 `ts_rank` S1.89 但 2Y=0.04。
- **已判死的三类**：earnings/macro/socialmedia 三塔（字段极薄：macro10 1 字段、socialmedia12 仅 4 可用、earnings6 仅 2 个真信号 VECTOR）；pv29/pv30 为**分组轴数据集**（pv30 447/558 是 GROUP 聚类标签）。
- **仍可投的方向**（若要继续）：pv37 之外的 pv 量能族需先做「时序族 vs 截面族」族探针；risk62 `intercept` 衰减最小（0.89→0.51）但离 1.58 仍远。

### 6. 工程铁律补录（本役实测）

1. **`create_multi_simulation` 在 429 后返回的 id 可能是幽灵**：立刻 `lookINTO_SimError_message` 回查；`status=""+"did not get through"+children 0` 有两种可能——（a）真幽灵需重发；（b）**仍在计算**（`raw.progress` 0.15/0.35 出现即真实存在）。判据看 `raw.progress` 是否存在，不要只看 error。
2. **`batch_status` 的 `kids=0` 在「收割过早」时同样出现**，不能作为丢失依据；收割前用 `lookINTO` 扫全部 id 找 `status=COMPLETE` 的批次再 harvest。
3. **`harvest_multisim_alphas` 在批次未完时返回 `n=0` 而不报错**，需自行判空。
4. **会话凭据会部分失效**：`get_datasets` 仍可用而 `/users/self/...` 与创建仿真返回 **401**；此时所有发批都会变成幽灵。修法：调 `authenticate` 重认证（返回 201/authenticated 即恢复）。


## ★★ 2026-11-13 补测 override（pv37 五族 25 臂穷尽后的算子级定律）

> 触发：用户质询「算子是否试全、是否查过论坛论文、组合依据是什么」。核查发现此前 15 个算子族中 10 族一项未试、论坛文献 0 篇，且判死越权（有 S1.89/1.90 波次却按 2Y 单独判死）。补做论坛 2 帖 + 文献 3 篇取证后，把用户点名五族补到 100%（ts_rank 3/3、ts_zscore 4/4、ts_quantile 2/2、winsorize 12/12、tail 4/4 = 25 臂），得以下定律。

### 1. ★ winsorize 是 2Y 的真杠杆，且存在甜点（必须扫全 12 档）
`group_rank(ts_rank(winsorize(F, std=X), 66), subindustry)`，F=pv37_downvolume：

| std | 0.15 | 0.25 | **0.3** | 0.35 | 0.5 | 0.65 | 1.5 | 2 | 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | **0.29** | 1.17 | **1.89** | 1.92 | 1.92 | **1.94** | 1.92 | 1.90 | 1.89 |
| 2Y | 0.33 | 0.31 | **0.32** | 0.22 | 0.20 | 0.18 | 0.11 | 0.10 | 0.02 |
| sub | 0.43 | 0.72 | 0.92 | 0.95 | **0.97** | 0.97 | 0.96 | 0.92 | 0.93 |

**单调梯度**：截尾越紧 → 2Y 越高（0.02→0.33），但 std<0.25 时 S 崩塌（0.29）。**甜点 std≈0.3**。
⇒ **近闸候选必须扫 winsorize 全 12 档找甜点，只试 std=2 会漏掉 2Y 的全部改善空间**。机制解释：近期尾部事件是 2Y 的主要污染源（与 Chen&Velikov 2022「价差/现代交易技术侵蚀异象」一致）。

### 2. ⛔ tail 与 winsorize 效果相反，不可互换
`tail(基线, lower=X, upper=1.0, newval=0)` 四档单调恶化：
| lower | 0.1 | 0.2 | 0.25 | 0.3 |
|---|---:|---:|---:|---:|
| S | 1.75 | 1.64 | 1.53 | 1.44 |
| 2Y | -0.10 | -0.18 | -0.24 | -0.36 |
| sub | 0.54 | 0.48 | 0.41 | 0.36 |

**机制**：tail 截掉下尾＝截掉空头腿 ⇒ sub 与 2Y 同步崩。winsorize 是**缩尾保腿**，tail 是**断尾毁腿**。
⇒ 事件型字段去并列块用 tail 是对的（旧纪律），但**对已连续型量能字段用 tail 会毁信号**；两者适用场景必须区分。

### 3. ★ 机制换法 > 参数微调（量化对比）
同一字段 2Y 的改善来源分解：
- 参数级（窗口/幂次/轴/换手）：2Y 0.04 → 最高 0.33（winsorize 甜点）
- **机制级（绝对量 → 成交量冲击比 `F/ts_mean(ts_delay(F,1),120)`）：2Y 0.04 → 0.50**
- **机制+幂次叠加（`signed_power(rank(冲击比),1.4)`）：2Y → 0.58（全场最高）**
⇒ **2Y 卡闸时第一动作是换机制（换读数构造），不是扫参数**。论坛帖《成交量冲击因子》的构造式在 EUR 同样有效。

### 4. ts_zscore / ts_quantile 与 ts_rank 同族等效（可互相替代，不必三族全扫）
| 族 | 最好 S | 最好 2Y |
|---|---:|---:|
| ts_rank(66) | 1.89 | 0.04 |
| ts_zscore(504) | 1.87 | 0.17 |
| ts_quantile(66) | 1.88 | 0.02 |
⇒ 三者都是「时序相对化」，读数几乎一致。**族探针只需 ts_rank 一条即可代表该族**，省 2/3 配额。

### 5. ⛔ 判死前必须闭合「中性化 × 宇宙」维（本轮程序教训）
论坛帖《全周期 sharpe 和 2y sharpe 的强对冲》原文要求：「当**全车道（窗口/结构/中性化/分组/字段机制）**都闭合、且 2y 始终结构性不达标时，才整理证据链上报裁决」。
本轮我在**中性化/宇宙仅测一档**时就下了 2Y 终判 ⇒ **程序越权，已补派 TOP2500/SUBINDUSTRY 与 TOPCS1600/STATISTICAL 两批**。
⇒ **判死 checklist 必须含「≥2 宇宙 × ≥2 中性化」**；记忆实证 TOP2500 曾把 2Y 从 2.06 抬到 2.34，这一维足以翻案，不可跳过。

### 6. ★ 2Y 与 S 的「强对冲」是**设置未闭合时的假象**（2026-11-13 11:40 修正）
~~S 最高 2.00 者 2Y 仅 0.07；2Y 最高 0.58 者 S 仅 1.84。不存在两者同时达标的形态。~~

**已被后续实验推翻**：同一表达式只换设置（TOPCS1600/SUBINDUSTRY → TOP2500/SUBINDUSTRY → TOPCS1600/STATISTICAL）：
2Y **0.58 → 1.13**、S **1.84 → 2.93**、F **0.70 → 1.05（跨过 1.0 闸）**。
⇒ **「2Y 与 S 互斥」只在设置车道未闭合时成立**。正确的表述是：
- **设置维（中性化 × 宇宙）的单次收益 > 换机制 > 全部参数级调参之和**；任何"2Y/S 互斥"结论在设置轴未跑 ≥2 档前**一律不成立**。
- **判死/判不达标的硬前置**：窗口 + 结构 + **中性化** + 分组 + 字段机制 + 换手 六车道全闭合（论坛帖1 原文），且设置轴 ≥2 宇宙 × ≥2 中性化。
- 本役教训：只闭合算子车道就下「2Y 结构性不达标」结论 ⇒ 差点错杀 2Y 可达 1.13 的字段（pv37_downvolume）。
- 仍然成立的部分：**tail 截下尾毁空头腿**、**winsorize 甜点 std≈0.3**、**机制换法（冲击比）把 2Y 从 0.04 抬到 0.50**。

### 7. ★ sub 比率闸的三个新定律（2026-11-13 pv37 六车道实证）
(1) **限值精确等于 0.52 × S**（实测 O0WawXzg S3.20/sub0.80/限1.66；VkNJwbzA S2.73/sub1.01/限1.42）⇒ 达标条件是 **sub/S ≥ 0.52**。
(2) **sub 比率与 S 严格负相关**：S1.14→0.588、S1.59→0.516、S1.72→0.517、S1.92→0.505、S2.04→0.373、S2.47→0.417、S3.96→0.25 ⇒ **「选刚好过主闸的 S」在本区被定量证实**；且 **2Y≥1.58 的形态 sub 比率必然 ≤0.37**，两者互斥。
(3) **市值分桶治不了 sub 比率，且引入 CONCENTRATED_WEIGHT**：按 `bucket(rank(cap), range="0,1,X")` 分组（X=0.05/0.1/0.2 三档全扫）后比率 0.271/0.276/0.271、robust 一律塌到 0.54、每桶可选股票骤减 ⇒ **权重集中**。⇒ 「sub 亏损源于规模倾斜」假设**被证伪**，sub 闸是更深的结构属性。

### 8. ⛔ STATISTICAL 档的 S/2Y 不可与其他档直接比较（本役再确认）
T2500/STATISTICAL 给出全场最高 S（3.96/4.53）与最高 2Y（2.48），但**同一表达式在 SUBINDUSTRY 档只有 S2.04/2Y1.13**。结合记忆「风险模型类中性化把 riskNeutralized 线当主 IS 输出」⇒ **该档的高 S/高 2Y 是另一把尺子，不能作为交付依据或跨档比较**。判定必须同档内比；标准档（SUBINDUSTRY/INDUSTRY/MARKET/COUNTRY）的读数才是可交付口径。

### 9. ⛔ 日频 OHLCV 上的「吸收（放量不跌）」机制不成立
`group_rank((close13−low10)/(high10−low10))` 单独读数 **S−0.04 / TO73.2% / 6 闸全败**；与抛压分位相乘只有 S0.64。⇒ 原因：**日频截面价不含盘中路径，无法识别「买方承接」**。此类机制需要日内快照/逐笔数据（如 intraday_pv_feats 的分时量），不能用日频 OHLCV 近似。

### 10. ★ 小宇宙先验判据（sub 闸的结构性上限可一次测出）
**做法**：把候选表达式**原样**在更小的宇宙（TOP800/TOP400）跑一遍，直接读出它在平台 sub-universe 口径下的真实表现。
**实测（pv37_downvolume）**：同一表达式 TOPCS1600 ⇒ S1.97 / 2Y1.14；TOP800 ⇒ **S0.24 / 2Y −1.40**。
⇒ **信号住在小盘/非高流动性部分 ⇒ LOW_SUB_UNIVERSE_SHARPE 是结构性上限**，任何换算子/换设置/换轴都救不回来。
**判据**：候选卡在 sub 闸时，**先跑 TOP800 一次**（1 条即可）：
- TOP800 读数接近主宇宙 ⇒ sub 是设置/形态问题，值得继续调；
- TOP800 读数塌掉 ⇒ **直接收档该字段**，不必再试市值分桶（方向恰好相反：是小盘倾向而非大盘倾向）、country/exchange 轴、换 universe 等。

### 11. ★ EUR 可用分组轴补录：exchange（2026-11-13 实测合法）
`group_neutralize` / `group_zscore` 的 `exchange` 轴在 **EUR 合法可用**（平台接受、无语法错；EUR 为多交易所宇宙）。
但实测**不改善 sub 比率**（0.286/0.300，与 subindustry 同级）⇒ 记录为可用档、**不是** sub 闸的解药。
本档已同步写入 `tracking/EUR/reference/boundary_ops_eur.json` 的 legal_axes。

### 12. ★ 族向由「字段量纲」决定，不由数据集决定（2026-11-13 risk70 vs pv37 对照实证）
| 字段类型 | 正确算子族 | 错误族的后果（实测） |
|---|---|---|
| **水平量 / 存量**（pv37_downvolume、risk60 费率、持股数） | **时序族**（ts_rank / ts_delta / ts_zscore） | 截面族全灭（pv37 group_rank 三轴 S0.00–0.02） |
| **因子暴露 / 标准化量 / 比率**（risk70 mfm2 风格暴露、beta、HHI、占比） | **截面族**（group_rank / group_neutralize） | 时序族**翻负**：S−0.10 ~ S−2.23（risk70 实测） |

**⇒ 族探针（截面族 1 臂 + 时序族 1 臂）必须逐字段跑**，且按量纲先验预判：
- 水平量 → 先时序族；因子暴露/比率 → 先截面族；
- 族向判据可与「小宇宙先验」合并为**每字段 5 臂预筛**：族探针 2 臂 + 小宇宙 1 臂 + 设置轴 2 臂。
- ⚠ 跨数据集照搬族向是本役最易犯的错（pv37 与 risk70 的正确族完全相反）。

### 13. ★ sub 比率的三种成因与对应判别动作（2026-11-13 risk70 补全）
| 成因 | 判别动作 | 典型读数 | 结论 |
|---|---|---|---|
| **① 结构性上限**（信号只在小盘） | **跑 TOP800**（1 臂） | 主宇宙 1.97 → TOP800 **0.24**（断崖） | 直接判死该字段 |
| **② 与分组轴无关**（信号本身 edge 薄） | 换 2–3 个轴各 1 臂 | 三轴 sub 比率恒定 0.35–0.38 | 换轴无用 ⇒ 改构造或换字段 |
| **③ 构造/极值造成** | `group_neutralize`（幅度保留）+ `winsorize` 细档 | 幅度保留形态通常抬 sub | 先试构造再谈换字段 |

**⇒ sub 闸排障顺序：TOP800 诊断 → 换轴（2–3 臂）→ 幅度保留/去极值构造 → 才考虑换字段。**
**另注：T2500 档的 `LOW_ROBUST_UNIVERSE_SHARPE` 天然不触发**（robust 为 null 不判），而 T1600 档会判 —— **换宇宙可解掉 robust 闸**（实测 risk70 anlystsn：T1600 时 robust 0.59/限0.70 失败，T2500 时该闸消失）。

### 14. ★ prod 墙可由**字段拥挤度**预判（2026-11-13 risk70 anlystsn 实证）
| alpha | 字段 | 字段 alphaCount | IS checks | self | prod |
|---|---|---:|---|---|---:|
| 0mPvKgJ1 | rsk70_mfm2_euetrd_anlystsn（ts_mean 252） | **115082**（risk70 最高） | **FAIL=[]** | 0.2958 ✅ | **0.8253 ❌** |

⇒ **字段自身是拥挤因子（alphaCount >10 万）时，即便 IS 全过 + self 通过，prod 仍会卡 0.8+** ⇒ 该字段的任何变换都会被同一批生产件相关。
**⇒ 选字段时把 alphaCount 当 prod 先验**：<1 千 ⇒ prod 友好；>10 万 ⇒ 预期 prod 墙，**不要把算子预算压在这里**。
**⇒ 对这类字段的正确做法：换字段（找同机制但拥挤度低的读数），而不是修 prod**。
本役反例：`risk70` 其它 mfm2 字段 aC 1.7 万–11.5 万但**全无信号**（S≤1.26 或反向）⇒ 拥挤度与信号强度不是同一维度，须分别筛。

### 15. ★ 平滑窗是 sub 闸的**单调**杠杆（2026-11-13 risk70 实测梯度）
| ts_mean 窗 | S | F | TO | sub | sub 闸限(0.52×S) | 差距 |
|---|---:|---:|---:|---:|---:|---:|
| 不平滑 | 2.97 | 1.90 | 8.26% | 1.13 | 1.54 | 0.42 |
| 5 | 2.73 | 1.67 | 6.47% | 1.06 | 1.42 | 0.36 |
| 22 | 2.27 | 1.25 | 3.56% | 1.04 | 1.18 | 0.14 |
| 66 | 2.12 | 1.12 | 2.66% | 1.03 | 1.10 | **0.07** |
| 252 | 1.59 | 0.73 | 1.79% | 0.86 | 0.83 | **通过** |

⇒ **窗越长 ⇒ TO↓、sub 比率↑、S/F↓**（S 跌破 1.58 在 252 档）。
⇒ **调 sub 闸的顺序：先扫平滑窗梯度**（单调、可预测），比换轴/换构造更有效（换轴无效、幅度保留更差、缩尾持平）。

### 16. ★★ prod 相关性由「形态罕见度」驱动，不是信号质量（2026-11-13 risk70 决定性对照）
| 形态 | prod | 说明 |
|---|---:|---|
| 纯 ts_mean(**504**) | **0.645 ✅** | 无人用 504 日平滑 ⇒ 持仓与池中典型件几乎不重叠 |
| 任意形态 + **ts_delta(1)** 快腿 | **0.826–0.829 ❌** | ts_delta(1) 是全网最常见形式 ⇒ 重新贴近生产池 |

⇒ **同一字段**（rsk70_mfm2_euetrd_anlystsn）504 形态 prod 0.645、delta 形态 prod 0.826 ⇒ 字段 alphaCount（11.5 万）虽相关，但**真正起作用的是形态**。
⇒ **破 prod 墙的唯一路径 = 换罕见形态**，具体三条罕见化手段（已验证有效）：
1. **罕见慢腿**：ts_mean(504) 优于 ts_mean(252)/ts_mean(66)；ts_rank(504) 亦罕见。
2. **罕见快腿**：**ts_delta(F,22)（月级差分）** 远比 ts_delta(F,1) 罕见 ⇒ 且同时把 S/F/ret 抬到合格区。
3. **换字段腿**：快腿换成同机制另一字段（如 momentum 暴露）⇒ 组合与池中典型件完全不同。
⇒ **交退法则**：既要 TO/ret 达标（需要快腿）又要 prod<0.7（需要罕见快腿）⇒ **只能选罕见快腿**，不能选 ts_delta(1)。 <!-- lint:counterexample -->

### 17. ★ ts_delta(F,22) 月级快腿是 EUR risk70 的最优快腿（2026-11-13 实证）
| 快腿 | 慢腿 | S | F | TO | ret | sub |
|---|---|---:|---:|---:|---:|---|
| **ts_delta(F,22)** | 252 | **2.24** | **1.28** | **7.16%** | **4.08%** | 1.10/限1.16 |
| ts_delta(F,1) | 252–756 | 1.5–1.85 | 0.73–0.94 | 5–11% | 2.7–3.3% | 0.74–0.85/限0.85–0.86 |
| ts_delta(F,2) | 504 | 1.71 | 0.84 | 9.72% | 3.04% | 0.83/限0.89 |

⇒ **机制**：日级差分是噪声放大器；**月级差分才捕捉到真实经济事件**（EUR 分析师评级/预期修正按月批量落地）⇒ 同时改善 S、F、TO、ret、sub。
⇒ **快腿参数阶梯建议**：ts_delta(1) → ts_delta(2) → **ts_delta(22)**（不要停在 1/2；22 是本区最优档）。

### 18. ★★ 两个被实证修正的常见误解（2026-11-13 risk70）
**(a) decay 是「升换手」杠杆，不是降换手杠杆**：实测 decay 4→2 时 TO 从 8.11% 升到 11.48%。⇒ **想降换手要加 decay（4→8/12），降 decay 反而放大换手**。
**(b) 慢腿平滑的增益在 504 处触顶**：慢腿 252→504→756 实测 S 略降、sub 比率略降（756 档 sub 0.74–0.75 < 504 档 0.83）⇒ **504 是本区慢腿甜点，超过 504 无增益**。

### 19. ★ 慢腿算子只允许 ts_mean / ts_rank 二选一（ts_zscore 被证伪）
| 慢腿 | S | F | 结果 |
|---|---:|---:|---|
| ts_mean(504) | 1.41–2.24 | 0.62–1.28 | ✅ 可用 |
| **ts_rank(504)** | **3.04** | **1.92** | ✅ 信号最强，但 TO 13.06% + sub 1.16/1.58 ⇒ 非交付形态 |
| **ts_zscore(504)** | **1.23** | **0.61** | ❌ 4 闸全败 |

⇒ **ts_zscore 抹掉因子的绝对水平信息，只剩截面形状 ⇒ 对因子暴露类字段是错的平滑方式**。
⇒ ts_rank 慢腿给出最高 S（3.04）但同时放大换手、削弱小宇宙表现 ⇒ 适合与**罕见慢腿**组合探索，不适合直接交付。

### 20. ★★ 慢腿甜点会被「罕见快腿」改变（2026-11-13 subfix 波实证，与第 15 条互相校正）
| 慢腿 | 快腿 | S | F | TO | ret | sub | sub 闸限(0.52×S) | sub/S 比率 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **252** | ts_delta(F,22) 0.5 | 2.24 | 1.28 | 7.16% | 4.08% | **1.10** | 1.16 | **0.491 ← 全族最高** |
| 504 | ts_delta(F,22) 0.5 | 2.28 | 1.30 | 8.39% | 4.09% | 0.98 | 1.18 | 0.430 |
| 756 | ts_delta(F,22) 0.5 | 2.18 | 1.21 | 9.36% | 3.86% | 0.91 | 1.13 | 0.417 |
| 504 | ts_delta(F,22) 0.5 @decay8 | 2.15 | 1.20 | 6.29% | 3.87% | 0.92 | 1.12 | 0.428（另 2Y 1.55 ❌）|
| 504 | **ts_rank(504)** 0.5 | 2.91 | 1.86 | 12.49% | 5.13% | 0.85 | 1.51 | 0.292 |

⇒ **第 15 条「窗越长 ⇒ sub 比率↑」在纯 ts_mean 慢腿成立，但在「罕见快腿 ts_delta(22)」下反转**：慢腿 252→504→756 使 sub/S 比率 0.491→0.430→0.417。
⇒ **正确表述：sub 比率的最优点由「慢腿 × 快腿」联合决定**。ts_delta(22) 快腿自带强信号（S 抬到 2.2+），慢腿再拉长只会把 S 与 sub 一起稀释而不改善比率 ⇒ **252 是该组合的甜点**。
⇒ **ts_rank 慢腿再次确认在 ts_delta(22) 下不可交付**（sub 比率 0.292，全族最低，且 TO 12.5% 破位）。
⇒ **decay 8 对 sub 无效**（0.92 vs 0.98 反而略降），但**把 TO 从 8.39% 降到 6.29%、2Y 从过闸掉到 1.55** ⇒ **decay 升高会伤 2Y**，不要用它换 TO。

### 21. ★ EUR risk70 罕见快腿家族的 sub 修复路径（2026-11-13 在飞波次）
**当前最佳：rK7XW2zj** = `group_rank(add(ts_mean(F,252), multiply(ts_delta(F,22), 0.5)), country)` <!-- lint:counterexample -->
- S 2.24 / F 1.28 / TO 7.16% / ret 4.08% / **self 0.3451 ✅**
- 仅 `LOW_SUB_UNIVERSE_SHARPE=1.10/lim1.16`（**差 0.06**）
- ⇒ **内部基准 S≥1.58 ✅ / F≥0.75 ✅ / TO≥4% ✅ / ret≥4% ✅ / self ✅ 全部通过，只差 sub 一线**。

**已派发的 sub 修复波（subfix2，6 臂）**：132 / 66 / 378 慢腿（反向梯度探 sub 比率天花板）、快腿权重 0.4、换 MARKET 轴、换 INDUSTRY 轴。
**判别逻辑**：sub 比率若在短慢腿（66/132）下继续升，说明信号在小宇宙有效只是被慢腿稀释 ⇒ 走短慢腿；若各档比率都在 0.49 附近封顶 ⇒ **sub 是该字段的结构属性**（第 13 条成因①），应换字段或换机制而非继续磨窗口。

### 22. ★★ 快腿权重是 sub 比率的**反向**杠杆（2026-11-13 subfix 波实证，第 21 条的补充）
| 慢腿 | 快腿权重 | S | F | TO | ret | sub | 闸限(0.52×S) | **sub/S** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 504 | 0.5 | 2.28 | 1.30 | 8.39% | 4.09% | 0.98 | 1.18 | 0.430 |
| 504 | 0.4 | 2.16 | 1.20 | 7.24% | 3.87% | 0.99 | 1.12 | 0.458 |
| 504 | **0.3** | 2.06 | 1.12 | 5.93% | 3.68% | **1.01** | 1.07 | **0.490** |
| 252 | 0.5 | 2.24 | 1.28 | 7.16% | 4.08% | 1.10 | 1.16 | **0.491** |

⇒ **快腿权重越低 ⇒ sub/S 比率越高**（0.5→0.3 时 0.430→0.490）。机制：罕见快腿贡献了大部分 S，但也贡献了大部分噪声；降权让慢腿的稳定成分占比上升，sub 小宇宙（流动性好、噪声占比低）受益更多。
⇒ **与慢腿梯度的方向相反**：慢腿加长降 sub 比率，快腿降权升 sub 比率。
⇒ **同时 2Y 转好**：0.3 权重档的 2Y 不再出现在失败清单（此前 504+0.5 的 2Y 1.55 ❌）。⇒ **降快腿权重是同时改善 sub 与 2Y 的双效杠杆**，优于加长慢腿。
⇒ **代价**：S 略降（2.28→2.06，仍远高于 1.58 闸）、ret 略降（4.09%→3.68%，内部 4% 线擦边）。
⇒ **下一步**：252 慢腿 + 0.2/0.3 权重（已派）⇒ 若 sub/S 能越过 0.52 且 S 保持 >1.58，即得首件全闸候选。
⇒ **判死线提示**：若 0.2 权重档的 sub/S 仍在 0.49–0.50 封顶不破 0.52 ⇒ 该字段的 sub 是**结构性属性**（第 13 条成因①），应换机制/换字段，停止磨窗口。

### 23. ★★★ prod 墙已被罕见快腿 ts_delta(F,22) 突破（2026-11-13 实测，独立复现第 16 条）
| 慢腿（快腿固定 ts_delta(F,22) 0.5） | S | F | TO | ret | sub/限 | self | **prod** |
|---|---:|---:|---:|---:|---|---:|---:|
| 252 | 2.24 | 1.28 | 7.16% | 4.08% | 1.10/1.16 ❌ | **0.3451 ✅** | **0.7411 ❌** |
| **504** | 2.28 | 1.30 | 8.39% | 4.09% | 0.98/1.18 ❌ | — | **0.6089 ✅** |
| 504 @decay8 | 2.15 | 1.20 | 6.29% | 3.87% | 0.92/1.12 ❌ | — | **0.6092 ✅** |

⇒ **慢腿越长 ⇒ prod 越低**（252→504：0.741→0.609）；与 ts_delta(1) 的 0.826 相比，罕见快腿 + 长慢腿组合把 prod 压到 0.61。
⇒ **self 亦不受罕见快腿影响**（0.3451，安全）。
⇒ **EUR risk70 的 prod 解法已确定：`ts_delta(F,22)` 快腿 + ts_mean(504~756) 慢腿 + SUBINDUSTRY/INDUSTRY 轴。**

### 24. ★★ sub 比率二维网格与「降 S 降闸限」算术杠杆（2026-11-13）
**网格（sub/S 比率，闸要求 ≥0.52）**
| 慢腿 \ 快腿权重 | 0.5 | 0.4 | 0.3 |
|---|---:|---:|---:|
| 132 | 0.438 (S2.76) | — | — |
| **252** | 0.491 | **0.498 ← 最高** | — |
| 378 | 0.434 | — | — |
| 504 | 0.430 | 0.458 | 0.490 |
| 756 | 0.417 | — | — |

- **慢腿 252 是绝对甜点**；132 掉到 0.438（虽 S/F/ret 最高），378/504/756 单调掉。
- **快腿权重越低 ⇒ 比率越高**（0.5→0.3 时 0.430→0.490）。
- **但全网格最高 0.498 < 0.52** ⇒ 单纯靠窗口/权重磨不过 sub。

**★ 新算术杠杆：sub 闸限值 = 0.52 × S ⇒ 降低 S 会同步降低闸限。**
例：252+0.4 的 sub 绝对值 1.09，S 从 2.19 降到 2.05 ⇒ 闸限 1.07 < 1.09 ⇒ 过闸。
⇒ **「降 S」与「提 sub 绝对值」等价**，且 S 只要 >1.58 即可 ⇒ 存在真实可行域。
⇒ **组合设计公式：长慢腿（降 prod）+ 低快腿权重（降 S、提比率）**，两者是乘积关系。

### 25. ★ 中性化档位：INDUSTRY 优于 SUBINDUSTRY（2026-11-13 单点实测，待复核）
| 档位 | S | F | TO | ret | sub/限 |
|---|---:|---:|---:|---:|---|
| SUBINDUSTRY | 2.24 | 1.28 | 7.16% | 4.08% | 1.10/1.16 |
| **INDUSTRY** | 2.28 | **1.35** | 6.57% | **4.36%** | **1.12/1.18** |
| MARKET | 1.88 | 1.08 | 6.17% | 4.10% | 0.89/0.98（+2Y ❌） |

⇒ **INDUSTRY 在 S/F/ret/sub 四项同时优于 SUBINDUSTRY**；MARKET 档明显最差（且触发 2Y 失败）。
⇒ 交付档**优先试 INDUSTRY**，SUBINDUSTRY 作为备选。（单点对照，需更多样本复核。）

### 26. ★★★★ sub 闸已突破：「降 S 降闸限」路径有效（2026-11-13 14:20 实测）
**sub 闸限值精确 = 0.52 × S ⇒ 降低快腿权重可同时降 S 与抬 sub/S 比率 ⇒ 过闸。**
| 慢腿 | 快腿权重 | S | F | TO | ret | sub | 闸限 | sub/S | checks.fail |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 504 | 0.5 | 2.28 | 1.30 | 8.39% | 4.09% | 0.98 | 1.18 | 0.430 | [sub] |
| 504 | 0.4 | 2.16 | 1.20 | 7.24% | 3.87% | 0.99 | 1.12 | 0.458 | [sub] |
| 504 | 0.3 | 2.06 | 1.12 | 5.93% | 3.68% | 1.01 | 1.07 | 0.490 | [sub] |
| 504 | 0.2 | 1.93 | 1.01 | 4.46% | 3.43% | 0.99 | 1.00 | 0.513 | [sub 差 0.01] |
| 504 | **0.15** | 1.86 | 0.95 | 3.66% | 3.29% | 0.98 | 0.97 | **0.527 ✅** | **[]** |
| 504 | **0.12** | 1.77 | 0.88 | 3.17% | 3.12% | 0.95 | 0.92 | **0.537 ✅** | **[]** |
| 504 | **0.1** | 1.72 | 0.85 | 2.84% | 3.03% | 0.94 | 0.89 | **0.547 ✅** | **[]** |
| 504 + INDUSTRY | **0.1** | 1.67 | 0.82 | 2.56% | 3.02% | 0.92 | 0.87 | **0.551 ✅** | **[]** |
| 504 + INDUSTRY | **0.15** | 1.82 | 0.94 | 3.31% | 3.32% | — | — | — | **[]** |

⇒ **sub 闸在 504 + ts_delta(22) + 权重 ≤0.15 时稳定通过**（sub/S 比率 0.527–0.551）。
⇒ **四件 checks.fail=[] 候选已产出**：VkNJ3YEJ(0.1)、9ql077re(0.15)、YPaqgZqR(0.12)、gJap9rnK(IND 0.1)、E5QJegGK(IND 0.15)。

### 27. ★★★ 平台闸线的实测真相（EUR TOP2500 档，读自 checks 全量）
| check | 平台限值 | 本役观察 |
|---|---|---|
| LOW_SHARPE | **1.58** | 与内部线一致 |
| LOW_FITNESS | **1.0** | 0.82–0.95 时结果为 **WARNING 而非 FAIL** ⇒ 平台不阻断 |
| **LOW_TURNOVER** | **0.01（1%）** | **平台只卡下限 1%，不卡上限**（HIGH_TURNOVER 限 0.7） |
| HIGH_TURNOVER | 0.7 | 从未触发 |
| LOW_SUB_UNIVERSE_SHARPE | **0.52 × S** | 精确等于 0.52×S |
| LOW_2Y_SHARPE | 1.58 | 标准档 |
| CLUSTER_TEST | 1.58 | 结果为 WARNING |
| **Returns** | **平台不检（无此 check）** | 内部 GATES_INTERNAL.returns_min=0.05 与 `brain_mixin_simulation.py:1036` 的 4% 均为**我方口径**，非平台 |

⇒ **内部 TO/ret ≥4% 的要求与平台无关**：平台只要 TO ≥1%。**TO/ret 基准是我方自设的质量线**，冲突时须向用户明示口径差。
⇒ **LOW_FITNESS 在 0.82–0.95 之间只给 WARNING** ⇒ 「checks.fail=[]」不等于 fitness 过 1.0，报告时必须同时写 F 实际值。

### 28. ★ EUR 平台硬限制备忘
- **EUR 无 TOP3000 宇宙**（`Universe TOP3000 is not available for instrument type EQUITY and region EUR`）⇒ 可用档为 TOPCS1600 / TOP2500 / TOP1200 / TOP800 等。
- **账号级 prod 相关性单并发**：并发查询互相挤掉（`correlation_busy` + `holder` 字段），须串行 + 按 `retry_after` 退避；本地 `brain_api` 有跨进程文件锁兜底。
- 平台 prod 计算需 1–5 分钟，轮询 11+ 次才出数（实测 160s）。

### 29. ★★★★ 内层分组轴（group_rank 第二参）决定 sub 上限（2026-11-13 突破）
| 内层轴 | 504 + w×d22 构造 | S | F | TO | ret | sub/限 |
|---|---|---:|---:|---:|---:|---|
| country | w=0.5 | 2.28 | 1.30 | 8.39% | 4.09% | 0.98/1.18 ❌ |
| country | w=0.2 | 1.93 | 1.01 | 4.46% | 3.43% | 0.99/1.00 ❌（差 0.01） |
| **market** | **w=0.2** | 1.82 | 0.94 | **4.18%** | 3.31% | **✅ 过闸** |
| **market** | **w=0.25** | 1.88 | 0.98 | **4.93%** | 3.43% | **✅ 过闸** |
| **market** | **w=0.3** | 1.95 | **1.04** | **5.64%** | 3.56% | **✅ 过闸** |
| market | w=0.4 | 2.06 | 1.13 | 6.94% | 3.76% | 0.99/1.07 ❌ |
| market | w=0.5 | 2.14 | 1.20 | 8.09% | 3.93% | 0.96/1.11 ❌ |
| sector | w=0.3 | 1.95 | 1.04 | 5.77% | 3.54% | 0.99/1.01 ❌ |
| sector | w=0.4 | 2.05 | 1.12 | 7.07% | 3.73% | 0.98/1.07 ❌ |

⇒ **market 内层轴比 country / subindustry / sector 显著抬 sub**：w=0.2 时 country 差 0.01 不过、market 直接过闸；w=0.3 时 market 过、sector 不过（差 0.02）。
⇒ **market 轴甜点区 w=0.2–0.3**：sub 过闸且 TO 4.18–5.64%（内部 TO≥4% 线达成）。
⇒ **教训：sub 闸的第四种成因 = 内层分组轴选择**（此前只测了「外层」中性化档 SUBINDUSTRY/INDUSTRY/MARKET，没测 group_rank 第二参）。**内层轴 ≠ 外层中性化档**，两者是正交维度，须分别扫。

### 30. ★★★ sub 闸的完整成因清单（四型，2026-11-13 补全）
| 型 | 成因 | 判别动作 | 本役证据 |
|---|---|---|---|
| ① | **信号住在小盘** | 跑 TOP800 直读 | pv37：主宇宙 1.97 → TOP800 0.24 |
| ② | **与分组轴无关**（edge 薄） | 换外层中性化档 2–3 个 | risk70 三档 sub 恒 0.35–0.38 |
| ③ | **构造/极值造成** | 幅度保留 + 去极值 | group_neutralize / winsorize 均无改善 |
| **④★** | **内层分组轴选错** | **扫 group_rank 第二参** | country ❌ → **market ✅**（w=0.2/0.25/0.3 全过） |
| ⑤ | **时序成分占比不足** | 加时序平滑/快慢混合 | 纯截面族 S2.9+ 但 sub 崩；加入 ts_mean+ts_delta 后 sub 恢复 |

⇒ **sub 排障顺序更新**：TOP800 诊断 → **扫内层分组轴** → 扫外层中性化档 → 幅度保留/去极值 → 提高时序成分占比 → 才考虑换字段。

### 31. ★★★★★ 用户硬闸口径（2026-11-13 用户明确）：**S > 1.58 且 F > 1.0 是硬闸**
**⇒ 平台把 LOW_FITNESS 在 0.82–0.95 判为 WARNING（不阻断），但我方硬闸要求 F > 1.0 ⇒ 那些件一律不算合格。**
**⇒ 「checks.fail=[]」不再等于合格**：必须同时满足 **S>1.58、F>1.0、checks.fail=[]、self<0.7、prod<0.7**。 <!-- lint:counterexample -->

**F 的构成公式（实测拟合）：`F = S × √(ret / max(TO, 0.125))`**
| alpha | S | TO | ret | F(公式) | F(平台) |
|---|---:|---:|---:|---:|---:|
| leaXWWx8 | 1.95 | 5.64% | 3.56% | 1.95×√(0.0356/0.125)=1.04 | **1.04** ✅ |
| O0WaGKAg | 1.93 | 4.84% | 3.31% | 1.93×√(0.0331/0.125)=0.99 | **0.99** ❌ |
| 2r5dLrNN | 2.28 | 8.39% | 4.09% | 2.28×√(0.0409/0.125)=1.30 | **1.30** ✅ |

⇒ **本区 TO 恒 <12.5% ⇒ F = S × √(8 × ret) ⇒ 抬 F 只有两条路：抬 S 或抬 ret。**
⇒ **夹逼约束**：sub 闸限 = 0.52×S 要求 S 不能太高；而 F>1 要求 ret（与 TO 同步）足够高。
⇒ **破夹逼的三条路**：
1. **换内层分组轴抬 sub**（market/subindustry 轴使 sub 在同样权重下过闸 ⇒ 允许更高权重 ⇒ ret/TO 更高 ⇒ F 更高）——**本役已验证**。
2. **换快腿字段**（momentum 腿无信号，实测 S 0.89 ❌ ⇒ 该字段族只有 anlystsn 有信号）。
3. **调 decay / 换慢腿长度**（decay↑ 会伤 2Y；慢腿↑ 伤 sub）。

### 32. ★ 内层轴与权重的 sub 甜点区全表（504 慢腿 + ts_delta(F,22)）
| 内层轴 \ w | 0.1 | 0.12 | 0.15 | 0.2 | 0.25 | 0.3 | 0.35 | 0.4 | 0.45 | 0.5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| country | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **market** | — | — | — | **✅** | **✅** | **✅** | ❌ | ❌ | ❌ | ❌ |
| subindustry | — | — | ✅ | ✅ | ❌ | 待测 | — | — | — | — |
| sector | — | — | — | ❌ | — | ❌ | — | ❌ | — | — |
| exchange | — | — | — | ❌ | — | — | — | — | — | — |

⇒ **market 轴把 sub 甜点区从 country 的 w≤0.15 推到 w=0.2–0.3** ⇒ 权重可提高 ⇒ TO 4.2%→5.6%、F 0.99→1.04 ⇒ **market 轴同时解 sub 与 F 两闸，是本字段的关键轴**。

### 33. ★ 负面结论（省去重复实验）
- **换快腿字段到 momentum**：S 0.89 / S 1.06（全灭）⇒ risk70 只有 anlystsn 有信号。
- **decay 8/12**：decay 8 让 2Y 从过闸掉到 1.55 ❌；decay 12 伤 sub（0.89/0.92）⇒ **decay 只保留 4**。
- **winsorize 慢腿（std=4）**：读数与不加完全相同 ⇒ 对该字段无效。
- **双层平滑快腿 `ts_delta(ts_mean(F,22),22)` / `ts_delta(ts_mean(F,44),22)`**：TO 塌到 2.5–3.4%、F 0.95–1.00 ⇒ 无效。
- **快腿加长到 44/63 日**：sub 比率掉到 0.415–0.458 ⇒ **22 日是快腿甜点**。
- **ts_rank 慢腿**：sub 比率 0.292（全族最低）⇒ 不可用。
- **外层中性化改 INDUSTRY/MARKET**：sub 反而更差（MARKET 档 S 与 sub 双降且触发 2Y）⇒ **外层固定 SUBINDUSTRY**。

### 34. ★★★★ market 轴 × 504 慢腿的**精确甜点单点**（2026-11-13 细网格实测）
| 内层轴 | w | S | F | TO | ret | sub/限 | 判定 |
|---|---:|---:|---:|---:|---:|---|---|
| market | 0.25 | 1.88 | 0.98 | 4.93% | 3.43% | ✅ | F ❌ |
| market | 0.28 | 1.93 | 1.02 | 5.36% | 3.51% | 0.99/1.00 | sub ❌ 差 0.01 |
| **market** | **0.30** | **1.95** | **1.04** | **5.64%** | 3.56% | **✅** | **★ 全闸** |
| market | 0.32 | 1.98 | 1.06 | 5.91% | 3.61% | 1.00/1.03 | sub ❌ 差 0.03 |
| market | 0.35 | 2.01 | 1.09 | 6.31% | 3.67% | 1.01/1.04 | sub ❌ 差 0.03 |
| market (378慢腿) | 0.3 | 1.74 | 0.88 | 5.17% | 3.20% | 0.89/0.90 | F+sub ❌ |
| market (132慢腿) | 0.3 | **2.42** | **1.44** | 4.26% | **4.41%** | 1.14/1.26 | sub ❌ 差 0.12 |

⇒ **w=0.30 是 market+504 的唯一同时满足 sub 过闸与 F>1 的单点**（两侧 w=0.28/0.32 都差 0.01–0.03）。⇒ 该族只有 **leaXWWx8** 一个可用点。
⇒ **132 慢腿在 market 轴上 S2.42/F1.44/ret4.41% 极强但 sub 差 0.12** ⇒ 短慢腿抬 S 抬 F 但压 sub ⇒ 降权重（0.15/0.2/0.25）是唯一出路（已派波）。
⇒ **378 慢腿两头差**（F 与 sub 同时崩）⇒ 慢腿长度在 504 附近最锋利，378/132 都更差 ⇒ **504 是唯一的慢腿甜点**（此处与第 20 条的 252 结论不同，因内层轴已换）。

### 35. ★ prod 熔断的正确处理（2026-11-13 实测）
| 现象 | 处理 |
|---|---|
| `correlation_busy` + `holder` 字段 | 账号级单并发被占 ⇒ 严格串行，**不要多进程并发查 prod** |
| `platform_unavailable` + `retry_after` | **连续 pending 触发的账号级熔断**（剩余 441–545s）⇒ 高频重试会不断累加冷却 |
| 熔断期正确做法 | **按 `retry_after` 精确等待**（`tools/prod_wait.py` 已实现：`wait = retry_after + 10`），一次成功后自动清除 |
| 平台 prod 计算耗时 | 首次触发需 1–5 分钟（实测 219s 出数），期间应停止重复查询 |

⇒ **prod 查询纪律**：单进程串行 + 按 `retry_after` 退避 + 拿到一个成功结果即恢复 ⇒ 不要用高频轮询去「抢」结果。

### 36. ★★ 快腿窗口不止 22 日：11 日同样可行（2026-11-13 更正第 17/33 条）
| 快腿窗口 | 慢腿 | w | 内层轴 | S | F | TO | sub/限 |
|---|---:|---:|---|---:|---:|---:|---|
| **11** | 504 | 0.3 | **market** | 1.96 | **1.04** | **6.74%** | **✅ 过闸** |
| **22** | 504 | 0.3 | **market** | 1.95 | **1.04** | 5.64% | **✅ 过闸** |
| 33 | 504 | 0.3 | market | 2.01 | 1.08 | 6.48% | 0.92/1.04 ❌ |
| 44 | 252 | 0.5 | country | 2.27 | 1.30 | 7.68% | 1.04/1.18 ❌ |
| 63 | 252 | 0.5 | country | 2.22 | 1.26 | 7.66% | 0.92/1.15 ❌ |

⇒ **快腿甜点是一个区间 [11, 22]，不是单点 22**；33 日起 sub 崩。
⇒ **11 日快腿 TO 更高（6.74% vs 5.64%）⇒ 内部 TO 基准更优** ⇒ 呈交优先用 11 日档。
⇒ 更正第 17 条「快腿参数阶梯 1→2→22」：**正确阶梯是 1→2→5→11→16→22→33**，11 与 22 都要试。

### 37. ★ 慢腿长度在 market 轴下的重测结论（覆盖第 20 条的 252 结论）
| 慢腿 | w=0.3 (market) | S | F | sub/限 | 判定 |
|---:|---:|---:|---:|---|---|
| 132 | 0.3 | 2.42 | 1.44 | 1.14/1.26 | sub ❌ 差 0.12 |
| 378 | 0.3 | 1.74 | 0.88 | 0.89/0.90 | F+sub 双崩 |
| **504** | 0.3 | 1.95 | 1.04 | 1.01/1.01 | **★ 唯一全闸** |
| 630 | 0.3 | 1.93 | 1.02 | 0.85/1.00 | sub ❌ |
| 756 | 0.3 | 1.96 | 1.02 | 0.87/1.02 | sub ❌ |

⇒ **换内层轴后慢腿甜点从 252 移到 504** ⇒ **慢腿甜点是「内层轴 × 慢腿」联合决定的**，不能跨轴照搬。
⇒ **132 慢腿在所有轴上都因 S 太高（2.17–2.42）⇒ sub 闸限被推高而失败** ⇒ 「短慢腿抬 S」在本字段是**反效果**。

### 38. ★★★ prod 取数被卡时先查「陈旧锁残留」（2026-11-13 实战排障）
**症状**：`correlation_busy` 且 `inflight_n: 1`，但持锁 pid 就是自己；或刚 kill 掉旧 prod 进程后新进程一直 busy。
**根因**：`logs/_dblock/` 下的三个状态文件由被杀进程留下，TTL 300s 内新进程无法获得：
| 文件 | 内容 | 清理时机 |
|---|---|---|
| `correlation.lock.json` | `owner: "<pid>@win"`（token 锁） | kill 进程后立即 |
| `correlation.inflight.json` | `items: {alpha_id: {pid, expires_at, n}}` | kill 进程后立即（TTL 300s） |
| `correlation.unavailable.json` | `streak` 熔断计数 + `until` | 熔断解除后 |
| `correlation.cooldown.json` | `until` 冷却截止 | 冷却到期后 |

**排查命令**：`python tools/_tmp_lock_peek.py`（打印 lock_dir 下 4 个文件的内容 + age）。
**处置**：确认持锁 pid 已死 ⇒ 直接删这 4 个 json ⇒ 重启**单个** prod 进程。
**纪律**：**kill 掉 prod 进程后必须清锁**，否则新进程会被自己的残留锁挡住，表现为「无限 busy」且误判为平台问题。

### 39. ★ prod 服务的账号级排队现实（2026-11-13）
| 事实 | 数值 |
|---|---|
| 单 alpha prod 计算耗时 | 首次 220–260s（平台侧异步排队） |
| 熔断触发条件 | 连续 3 次 pending ⇒ 账号级 `platform_unavailable`，冷却 600s |
| 空体 200 响应 | 平台尚未算好（**不等于失败**） |
| 正确只读端点 | `GET /alphas/{id}/correlations/prod`（`/correlations/production` 是 404） |
| 正确触发端点 | `brain_api.get_production_correlation(alpha_id)` |
| 成功出数的判据 | 返回字典含 `max` 字段；**绝不从 `records` 直方图里取 bin 值** |

⇒ **处置顺序**：先查陈旧锁 → 单进程触发 → 等 240s → 未出数则 peek 空体=继续等 → 连续 pending 3 次 ⇒ 停手等 600s 冷却（不要高频重试自锁）。

### 40. ★★★ 慢快混合模板的适用边界（2026-11-13 跨字段实证）
**模板**：`group_rank(add(ts_mean(F,SLOW), multiply(ts_delta(F,22), W)), market)` <!-- lint:counterexample -->

| 字段语义类型 | 实测 S | 判定 |
|---|---:|---|
| **可修正预期类**（分析师情绪 anlystsn） | **1.95-2.42** | 强信号 |
| 盈利能力暴露 profit | 1.22 | 差 0.36 |
| 新闻情绪暴露 newssent | 0.95 | 败 |
| 盈利质量暴露 earnqlty | 0.76 | 败 |
| 成长暴露 growth | 0.53 | 败 |
| 行业动量暴露 indmom | 0.24 | 败 |
| 股息率暴露 divyild | 0.04 | 全零 |

=> **模板只适用于「可修正预期」类字段**（分析师情绪/预期修正/持仓拥挤变化/内部人交易）。
=> **机制**：快腿捕捉「中期修正事件」；静态基本面口径（财报一年一次、股息率几乎不变）**没有修正事件可捕捉** => 全灭。
=> **换字段前的必做判断**：字段描述是否含「预期/修正/变动/拥挤变化/交易行为」语义？若只有「水平/水平值/占比」=> 该模板必然失败。
=> 与第二十七章（截面族全灭）**双族独立复核一致** => risk70 的 87 字段中只有 anlystsn 有信号。

### 41. ★ 慢腿 198 与 504 是两个「合格甜点」（2026-11-13）
| 慢腿 | 最优权重 | S 范围 | F 范围 | TO | 与另一族的互相关 |
|---|---:|---:|---:|---:|---|
| **198** | 0.20-0.30 | 2.10-2.26 | 1.15-1.29 | 3.85-5.21% | **0.696-0.719（小于 0.7 边界）** |
| **504** | 0.30-0.50 | 1.95-2.21 | 1.04-1.25 | 5.64-9.93% | 同上 |
| 144 | 0.30 | 2.38 | 1.40 | 4.29% | sub 差 0.11 |
| 378 | 0.30 | 1.74 | 0.88 | 5.17% | F+sub 双崩 |

=> **同字段下慢腿长度是解互相关的有效变量**（198 与 504 相关约 0.70，504 族内部 0.95+）。
=> 198 族 self 0.34-0.36、504 族 self 0.21 => 两族合并后 self 仍在安全区。
=> **篮子规划**：同数据集可容 2 件（198 族 1 件 + 504 族 1 件）；更多颗数必须换数据集或换因子。

### 42. ★ prod 计算耗时与内层轴相关（2026-11-13 观察）
| 内层轴 | prod 计算耗时 |
|---|---|
| country（504 慢腿） | 约 9s 命中缓存 |
| **market（504 慢腿）** | **首次 183s 成功（leaXWWx8）；其余件反复 pending 超过 240s** |

=> **market 内层轴的 prod 平台侧计算更慢** => 呈交前需预留更长等待窗口，不要用高频重试去抢（会触发账号级熔断）。

### 43. ★★★ 参数扫描不等于多因子：换分组轴只降 0.02-0.06 相关（2026-11-13）

**实证**：EUR 全池 19 件硬闸全过 alpha，全部来自 `rsk70_mfm2_euetrd_anlystsn` 单字段 × 单模板 × 参数网格（W∈{11,13,16,22} × Wt∈{0.30…0.50}）。

精确互相关矩阵（1021 点本地计算）：
| 对 | 相关 |
|---|---:|
| E5QJv9Kr × xAvg33vn | 0.9676 |
| leaXWWx8 × e7aRa62N | 0.9616 |
| leaXWWx8 × vRAgNK3w（country 轴） | 0.9464 |
| **vRAgNK3w × xAvg33vn（全池最低对）** | **0.7064** |

⇒ **全池最低对 0.7064 > 0.7，最大互相 <0.7 子集 = 1 件。**

**规则**：
1. **同字段同模板的参数变体不是多个 alpha**，只能选 1 件。产出计数时不要把参数扫描的臂数当因子数。
2. **换 `group_rank` 第二参（market→subindustry→country）只带来 0.02–0.06 的相关下降**，远不足以跨 0.7。真正降相关只有两条路：**换字段** 或 **换机制**。
3. 前文曾记「country 轴与 market 族相关 0.696–0.719 可同篮」——**该记录已作废**，实测 0.9464。

### 44. ★★ 判「没信号」还是「没调好」：看符号是否随配置翻转（2026-11-13）

**实证**：`insd1_valueeur` 三配置实测符号翻转
| 配置 | S |
|---|---:|
| TOP2500 / SUBINDUSTRY / decay4 / nan ON | **+0.42** |
| TOP2500 / INDUSTRY / nan OFF | **−0.33** |
| TOPCS1600 / MARKET / decay8 / nan OFF | **−0.24** |

**判据**：
- **符号随配置翻转 ⇒ 信号层死（纯噪声）**，停止调参。
- **同号但强度不足（如各处都在 +0.3~+0.5）⇒ 配置层可能还有救**，值得继续扫轴。

这条判据可以省掉大量「换配置再试一轮」的无效配额。

### 45. ★★ nan OFF 不是万灵药：它会砍覆盖（2026-11-13 修正旧判据）

**实证**：`net_retail_buying_selling_value_eur` 同一表达式
| nan | long/short | S |
|---|---|---:|
| ON | 429 / 1620 | **0.76** |
| OFF | 185 / 187 | **0.39** |

nan OFF 让覆盖崩掉约 77%，信号反而更弱。

**修正旧判据**（原「事件型 VECTOR 必须试 nan OFF」）：
⇒ **事件型必须做 ON/OFF 双侧对照，但 OFF 是"可能更好"而非"一定更好"。覆盖薄的字段 OFF 会更差。**
判断顺序：先看 OFF 后 long/short 数量是否还在可用量级（<500 只就要警惕），再看 S。

### 46. ★★★ 形态类因子不能慢化——与预期修正类时序结构相反（2026-11-13）

**实证**：`dynamic_upward_gap_continuation_score` 取反
| 处理 | S |
|---|---:|
| 当期（无平滑） | **0.79** |
| `ts_mean(22)` 平滑 | **0.14** |

⇒ 平滑把 S 打到 1/5.6。**形态/事件类信号住在当期，慢化即杀信号。**

**与 anlystsn 完全相反**：anlystsn 必须 `ts_mean(504)` 慢腿才有 S 1.95，当期形态只有 0.3 量级。

**规则**：模板语义决定时序结构——
- **「可修正预期」类**（分析师情绪/评级/预期）→ 慢腿越长越好，504 起步
- **「形态/形态相似度/形态延续」类** → 当期，禁止平滑
- 把慢快混合模板套到形态类字段上，等于用错误的时间常数，必然全灭

### 47. ★★ 跳空回补（gap fill）是 EUR 可用机制，但强度上限 S≈0.80（2026-11-13）

**数据集**：`continuation_score`（pv 塔，560 字段，cov 0.98–1.0，MATRIX）
**核心字段**：`dynamic_upward_gap_continuation_score`

| 变体 | S | 2Y | 备注 |
|---|---:|---:|---|
| 原式 | **−0.97** | −1.19 | sub −0.52 同向 ⇒ 非噪声 |
| `subtract(0, ...)` 取反 | **0.79** | 1.07 | 方向确认 |
| `dynamic_downward_gap` 正向 | **0.79** | 0.97 | **对称验证吻合** |
| 双方向合成 | 0.80 | 1.03 | 微增 |
| TOP800 | 0.55 | 0.45 | 小宇宙更差 |

**机制**：看涨跳空后延续分数越高 → 未来收益越低 ⇒ 跳空回补。
**强度上限**：S 在 0.80 封顶，距硬闸 1.58 差约 50%；提升手段（平滑）失效，只剩换变体/换轴。
**对称检验法**：`upward` 取反 与 `downward` 正向 得到同一 S ⇒ 真实因子；两者背离 ⇒ 拟合噪声。这是形态类数据集最快的真伪判据。

### 48. 引擎：`eur_atomic_cli.py` 已支持 nan 参数（2026-11-13）

```
jobs.json 元素 = [expr, universe, neutralization, decay, nan]
nan = 'ON' | 'OFF'，缺省 'ON'
```
**此前 payload() 硬编码 `nanHandling:'ON'`**，导致跨数据集探针无法做 nan 双侧对照——这是必须避免的方法缺陷。新数据集首波必须显式指定 nan。

### 49. ★★★ 形态集的可挖面只有「反转形态」，延续形态全灭（2026-11-13）

**已实测判死**（全部 TOP2500/INDUSTRY/d4 + ts_rank 250）：

| 形态族 | S | 类别 | 判定 |
|---|---:|---|---|
| `bullish_pennant` | 0.29 | 延续 | 判死 |
| `dead_cat_bounce` | 0.15 | 反转(伪) | 判死 |
| `bullish_rectangle` | −0.15 | 延续 | 判死 |
| `inverse_cup_handle` | −0.30 | 反转 | 判死 |
| `ascending_staircase` | −0.04 | 延续 | 判死 |
| `symm_triangle_down` | 0.15 | 中性 | 判死 |
| `continuation_v_top` | 0.47 | 延续 | 判死 |
| `breakaway_gap_down` | 0.45 | 延续 | 判死 |
| **`reversal_v_bottom` / `reversal_v_top`** | **1.37** | **反转** | ★唯一活 |
| `ts_arg_max`（事件时序） | −0.79 | 非形态 | 判死 |

**判据**：EUR 有效的是「**反转形态**」（趋势将尽），无效的是「**延续形态**」（趋势将继）。
**机制**：EUR 市场反转效应强度 > 动量效应强度，所以所有「延续/持续」语义的形态分数都被反向定价或无效。
**应用**：在 pattern_scores / continuation_score 选集时，**只挑名字含 reversal / v_bottom / v_top 的族**；pennant / rectangle / channel / staircase / scallop / cup_handle / flag 一律跳过，不要再花配额。

### 50. ★★★ ts_rank 窗口 630 是 V 反转族的峰值（2026-11-13，光滑单峰）

**完整窗口阶梯**（同字段同设置）：

| 窗口 | S | F | 2Y | sub | TO |
|---:|---:|---:|---:|---:|---:|
| 250 | 1.31 | 0.76 | 0.96 | 1.03 | 12.3% |
| 363 | 1.26 | 0.72 | 1.00 | 0.95 | 11.6% |
| 500 | 1.34 | 0.79 | 1.21 | 1.05 | 11.2% |
| 567 | 1.35 | 0.80 | 1.24 | 1.05 | 11.1% |
| **630** | **1.37** | **0.82** | **1.32** | **1.06** | **11.0%** |
| 693 | 1.35 | 0.80 | 1.30 | 1.06 | 10.9% |
| 750 | 1.32 | 0.78 | 1.25 | 1.02 | 10.9% |
| 900 | 1.29 | 0.75 | 1.20 | 0.99 | 10.8% |
| 1008 | 1.25 | 0.72 | 1.19 | 0.95 | 10.7% |
| 1260 | 1.24 | 0.71 | 1.12 | 0.94 | 10.7% |

**形状**：250→363 下凹，363→630 上升，630 见顶，630→1260 单调下降。**两侧各 ≥2 观测点支撑，是真峰值。**
**经济学**：630 交易日 ≈ 2.5 年 = EUR 形态记忆有效期。太短则统计不稳，太长则旧形态失效。
**应用**：V 反转族直接用 **630**；若要压 TO 可用 ts_zscore(630)（TO 10.2% vs 11.0%，S 只掉 0.03）。

### 51. ★★ 归一化形式不可作为独立因子（2026-11-13 MCP 权威矩阵）

| 归一化写法对比 | 相关系数 |
|---|---:|
| ts_rank vs winsorize+ts_rank | **1.0000** |
| ts_rank vs ts_quantile | **0.9998** |
| ts_rank vs ts_zscore（v_bottom 族） | 0.9871 |

⇒ **ts_rank / ts_zscore / ts_quantile / winsorize+ts_rank 四者在相关意义上完全等价**，是同一个 alpha 的四种写法。
**应用**：不要把归一化变体当作独立 alpha 计数；形态集内最多只能提 1 件。
**唯一能拉开相关的维度是宇宙**：TOPCS1600 vs TOP2500 → 0.9143（但仍 ≫0.7，不够用）。

### 52. ★★★ 形态线（pv 塔）与 rsk70（risk 塔）严格正交 —— 可打破单因子上限

MCP 权威矩阵实测，全部形态臂 vs `leaXWWx8`（rsk70 anlystsn ATOM）：

| 形态臂 | 相关系数 |
|---|---:|
| YPadQNPW | −0.0054 |
| npabZd0z | −0.0103 |
| rK7mAbqa | −0.0178 |
| 1YW5J3Zm | −0.0180 |
| vRAV5nYz | −0.0216 |
| RReL2dO0 | −0.0248 |

⇒ **全部 −0.005 ~ −0.025，严格正交。**
**战略意义**：形态线一旦破闸（S>1.58 & F>1.0 & 2Y>1.58 & prod<0.7），可与 rsk70 的 `leaXWWx8` **同时进篮子**，一次交付 2 个独立因子，跨 pv + risk 两个塔。 <!-- lint:counterexample -->
**这条打破了「同数据集只能交 1 件」的死局**——破局关键不是在同一数据集内找第二个因子，而是**跨数据集找正交机制**。

### 53. ★★★ F 的真实算法（大 TO 段）：F = S × √(ret / TO)，降 TO 同时抬 F（2026-11-13 精确验证）

**既有判据（第 17 条）只在小 TO 段成立**：`F = S×√(8·ret)` 是 `max(TO,0.125)=0.125` 的特例。

**本轮在 TO=68% 下精确验证**：
```
P05EONAK: S=1.76, ret=11.35%, TO=68.05%
实测 F = 0.72
公式 F = S×√(ret/TO) = 1.76×√(0.1135/0.6805) = 1.76×0.4084 = 0.719  ✅ 精确吻合
（若用 √(8·ret) 会得 1.68，完全错误）
```

**通用形式**：
```
F = S × √( ret / max(TO, 0.125) )
```
- TO < 12.5% 时退化为 `F = S×√(8·ret)`（既有判据）
- TO > 12.5% 时 F 与 √TO 成反比

**★★ 可复用的核心推论**：
> **降 TO 同时抬 F。** 在 S、ret 不变的前提下，TO 从 68% 降到 30%，F 从 0.72 升到 1.08（+50%）。

**应用**：
1. **F 不过闸时，第一优先是降 TO**，不是提 ret。降 TO 是唯一能同时保 S 又抬 F 的杠杆。
2. 反例警示：`ts_mean(22)` 把 TO 68%→13.2%，F 0.72→0.76（只 +0.04），因为 S 塌了 1.76→1.11。**暴力平滑虽降 TO 但杀 S，净效果几乎为零。**
3. **正确的降 TO 顺序**：decay 阶梯（0/2/4/8/12/16/24/32）→ 温和平滑（ts_mean 5/11）→ 换宇宙。decay 不改信号、只压换手，是首选。

### 54. ★★★ pv20 crowding 是 EUR 首个 S 破 1.58 且 TO 在限内的候选（2026-11-13）

```
P05EONAK
group_rank(ts_rank(subtract(0, specific_return_crowding_top2500), 630), industry)
region=EUR universe=TOP2500 delay=1 decay=8 neut=INDUSTRY trunc=0.08
```
**平台侧权威 checks**：
| 项 | 值 | 限 | 结果 |
|---|---:|---:|---|
| LOW_SHARPE | **1.76** | 1.58 | ✅ PASS |
| HIGH_TURNOVER | **68.05%** | 0.7 | ✅ PASS |
| LOW_SUB_UNIVERSE_SHARPE | **1.39** | 0.91 | ✅ PASS |
| LOW_FITNESS | 0.72 | 1.0 | ⚠️ |
| LOW_2Y_SHARPE | 0.92 | 1.58 | ⚠️ |
| CLUSTER_TEST | 1.18 | 1.58 | ⚠️ |

**机制**：`specific_return_crowding_top2500` = 按拥挤度分组构建的特异收益。**取反 = 做空近期涨得多的拥挤股**（短期反转 + 拥挤度惩罚）。
**关键设置**：**decay 8 + subtract(0,...) 同时解决两个问题**——S 从 −1.77 翻到 +1.76，TO 从 89.6% 压到 68.05%（刚好进限）。
**三条 crowding 字段同源**（top2500/top1200/notliquim 的 S 差 ≤0.03、TO 差 ≤0.1%）。
**边界**：`ts_mean` 平滑杀伤极大（22 日 → S 1.11 / TO 13.2%；66 日 → S 0.56）⇒ **该信号必须保持当期性**。

### 55. ★★ 目录里有字段 ≠ 平台可用：preflight 是选集前置闸（2026-11-13 两次整批归零实证）

**实证**：
| 字段 | 目录 JSON | 平台 preflight |
|---|---|---|
| `pv87_ann_matrix_return_on_equity_mean` | 有 | ❌ dataset-prefixed not found |
| `ann_matrix_return_on_equity_mean`（去前缀） | — | ❌ unknown_fields |
| `stddev_similarity_reversal_v_top` | 有 | ❌ unknown_fields |
| `stddev_similarity_reversal_v_top_120` | 有 | ❌ unknown_fields |

⇒ **pv87 全部 1649 字段在 EUR 未注册；V 反转族的 stddev 变体也未注册。**

**代价**：两次 `create_multi_simulation` 因单条字段不存在触发 **batch-kill**，5 臂 + 4 臂全部 CANCELLED，白烧 9 条配额。

**纪律（硬）**：`create_multi_simulation` 前**必须**跑 `preflight_expressions` 全量校验，过滤掉 unknown_fields 再派。**一条错 → 整批死。**


### 56. ★★★ prod 只对「持仓集合」敏感：七维 20 变体免疫清单（2026-11-14）

**EUR 形态线 `78YVGR3Z`（S1.61/F1.02/2Y1.59/self0.53）六闸仅剩 prod=0.7422。系统扫描七维：**

| 维度 | 变体 | prod | 结论 |
|---|---|---|---|
| 外层算子 | group_rank/group_neutralize/group_zscore | 0.7664/0.7501/0.7426 | 仅首步有效 |
| 中性化档 | SECTOR vs INDUSTRY | 0.7664=0.7664 | **免疫** |
| 分组轴 | industry/subindustry/sector | 指标全同 | **免疫** |
| 内层 sigma | 1.5/2.0/2.5 | 0.7422×3 | **免疫** |
| 叉乘分组 | ×country/×exchange/×currency | 0.7431/0.7431/0.7693 | 无效或更差 |
| 变换 tail | 5%/10% | 0.7459/0.7458 | **反向恶化** |
| **宇宙** | TOP2500/CS1600/1200/800 | 0.7422/**0.7107**/0.7310/0.7301 | **★唯一有效** |

**规则**：prod 由**持仓集合**决定。只改标准化几何（算子/档位/轴/参数/叉乘）**完全无效**；
只有改变持仓集合本身（换宇宙）或改变权重分布（tail 截尾）才动 prod。
**应用**：prod 卡墙时不要再换算子/档位/参数——直接上宇宙维度。

### 57. ★★★ TOPCS1600 是 EUR 降 prod 的最优宇宙（唯一把 prod 压到 0.71 的宇宙）

| 宇宙 | S | F | 2Y | prod |
|---|---:|---:|---:|---:|
| TOP2500 | 1.61 | 1.02 | 1.59 | 0.7422 |
| **TOPCS1600** | 1.46 | 0.92 | 1.42 | **0.7107** |
| TOP1200 | 1.26 | 0.77 | 1.47 | 0.7310 |
| TOP800 | 1.13 | 0.68 | 1.35 | 0.7301 |

**非单调**：CS 前缀 = 可投资性（capacity-selected）筛选，持仓集合与纯市值 TOP 系列本质不同。
**代价**：prod −0.0315 换 S −0.15 / 2Y −0.17，三项硬闸全破 ⇒ 需在 CS1600 上另找提指标手段。

### 58. ★★ tail 截尾：五指标同升但 prod 反升（方向用错）

| 组合 | S | F | ret | 2Y | sub | prod |
|---|---:|---:|---:|---:|---:|---:|
| 基准 TOP2500 | 1.61 | 1.02 | 5.64% | 1.59 | 1.25 | 0.7422 |
| + tail 5% | **1.64** | **1.03** | **5.84%** | **1.62** | **1.30** | 0.7459 |
| TOPCS1600 基准 | 1.46 | 0.92 | 5.51% | 1.42 | 1.07 | 0.7107 |
| + tail 5% | 1.50 | 0.94 | 5.74% | 1.45 | 1.11 | 0.7159 |

**tail 是全战役唯一让 S/F/ret/2Y/sub 五项同升的算子**（截尾去噪），且跨宇宙可叠加（CS1600 上同样 +0.04S）。
**但 prod 一律 +0.004~0.005** ⇒ 被截掉的两端恰是**与生产池低相关**的持仓。
⇒ **两杠杆互斥**：要最低 prod 就不能用 tail。**正确方向是反向截尾（保留尾部、去中间段）**——对 rank 做区间选择。

### 59. ★ trade_when 门控与 group_mean 均重伤信号（禁用）

| 算子 | S | F | 2Y |
|---|---:|---:|---:|
| trade_when(cond, Q, -1) | 1.00 | 0.47 | 0.84 |
| group_mean(ts_rank, 1, industry) | 0.36 | 0.14 | −0.22 |
| group_mean(ts_rank, 1, subindustry) | 0.83 | 0.47 | 0.56 |
| 基准 | 1.61 | 1.02 | 1.59 |

**trade_when**：未触发股票置 −1 全空，破坏横截面排序。
**group_mean**：组内均值把个股信号压成组信号，信息损失大。
⇒ 两者对**单边做空型**形态信号均不可用。

### 60. ★★ 算子场景覆盖台账（EUR 形态线，2026-11-14 完成）

| 类别 | 总数 | 已测 | 未测原因 |
|---|---:|---:|---|
| 截面 | 6 | **6** | — |
| 分组 | 11 | **10** | combo_a（COMBO 域不可用）|
| 时序 | 30 | 23 | 3 个需双字段；4 个语义不适用 |
| 变换 | 4 | **3** | bucket（range 引号触发静态闸）|

**补测变换类（0%→75%）立刻产出 tail 这个五指标同升的最优算子** ⇒ 印证「先吃透算子场景再组模板」。
