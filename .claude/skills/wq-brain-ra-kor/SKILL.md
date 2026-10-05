---
name: wq-brain-ra-kor
description: "在 KOR 区挖 REGULAR alpha、调 KOR 的回测设置或阈值、查 KOR 某类数据集（区域 × 类别组合）的配方与禁区时使用：KOR 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-05
---

# KOR 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：KOR 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 KOR 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 KOR，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region KOR --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region KOR --apply
   $WQ_PY -m wqb.profiles render --region KOR --apply
   ```

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　TOP600 小宇宙：2026-10-03 起唯一活路 = other466 财务比率族（fundamental 塔，等价算子替换 signed_power→quantile 后全闸过）；分析师 / insiders / pv / 图表 / 新闻 / AI / 信用 / risk 全红灯；结构性约束 = 2Y 与 IS 因输入频率此消彼长，CW 闸升级 FAIL

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | KOR | settings.json |
| universe | TOP600 | settings.json |
| delay | 1 | settings.json |
| neutralization | STATISTICAL | settings.json |
| decay | 4 | settings.json |
| truncation | 0.08 | settings.json |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | OFF | settings.json |
| maxTrade | OFF | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |
| startDate | 2013-01-01 | settings.json |
| endDate | 2023-12-31 | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.01 | thresholds.json |
| review.turnover_max | 0.7 | thresholds.json |
| review.two_year_sharpe_min | 1.0 | thresholds.json |
| near.sharpe_min | 1.0 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.5 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：1
- 快判死：新数据集 8 探针无 ／S／≥0.5 即判死回写，不扩批（小宇宙烧不起配额）
- 停止条件：白名单被 dead_end 全覆盖
- 闸门特化（文档级）：cw_gate=FAIL、longcount_verdict=FAIL——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| analyst | Analyst | active | — | — | 175 / 13 | 2（2） | 10 / 0 | [references/analyst.md](references/analyst.md) |
| fundamental | Fundamental | active | — | — | 171 / 20 | 8（2） | 6 / 5 | [references/fundamental.md](references/fundamental.md) |
| shortinterest | ShortInterest | active | — | — | 81 / 5 | 25（20） | 0 / 0 | [references/shortinterest.md](references/shortinterest.md) |
| pv | PV | active | — | — | 40 / 0 | 0（0） | 7 / 0 | [references/pv.md](references/pv.md) |
| insiders | Insider | active | — | — | 27 / 0 | 0（0） | 1 / 0 | [references/insiders.md](references/insiders.md) |
| news | News-Sentiment | active | — | — | 27 / 0 | 0（0） | 4 / 0 | [references/news.md](references/news.md) |
| risk | Risk | active | — | — | 24 / 0 | 0（0） | 3 / 0 | [references/risk.md](references/risk.md) |
| sentiment | News-Sentiment | active | — | — | 18 / 0 | 0（0） | 3 / 0 | [references/sentiment.md](references/sentiment.md) |
| other | Other | active | — | — | 10 / 0 | 4（2） | 36 / 7 | [references/other.md](references/other.md) |
| model | MODEL | active | — | — | 2 / 0 | 4（4） | 12 / 0 | [references/model.md](references/model.md) |
| institutions | Institutions | active | — | — | 0 / 0 | 0（0） | 1 / 0 | [references/institutions.md](references/institutions.md) |

说明：另有 101 条回测行没写数据集，无法归到组合；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **S0 选集**：白名单只留绿榜（other466）与 untried 新集；按「信息维度是否已在 prod book 里」排序，别只看 coverage / alphaCount / valueScore（稀疏覆盖的高 valueScore 是陷阱）。analyst 族不再作主数据集；红榜数据集即使用户点名，也先提示死路出处。
- **S1 字段**：typed catalog 双查，每个字段都要 longCount 与 type；longCount 低于 80 的 VECTOR 字段进观察名单（profile 要求按 FAIL 处理，代码里闸 7 仍是 WARN，由执行者把关）。
- **S2 生成**：从 [KOR × fundamental](references/fundamental.md) 出发（当前唯一活路）；事件类数据集平台没有 ts_event_*，先单条探针确认字段能进标准算子。
- **S3 回测**：新数据集只给 8 条探针预算，没有 |S| 达 0.5 的就判死回写，不扩批、不换设置重试（小宇宙烧不起配额）；实证只有 delay 1，不外推 delay 0。
- **S4 改进**：判「不可能 / 天花板」前先扫等价算子替换（KOR 的「不可能三角」就是 signed_power 造成的）；CW 超过 0.5 判死不回炉（profile 要求，步 7 人工执行）；输入频率决定 2Y 与 IS 此消彼长——只有 shortinterest38 一个族的证据，作选区先验。
- **S5 提交**：同族一次只提 1 颗（兄弟连提会把后来者 prod 顶高）；prod 与 self 两个端点都实测。
（来源：KOR profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/KOR/config/settings.json`（仿真设置）、`tracking/KOR/config/thresholds.json`（阈值）。
- **组合级**：`tracking/KOR/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region KOR
  $WQ_PY -m wqb.profiles render --region KOR --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[KOR profile](../wq-brain-ra-pipeline/references/regions/KOR.md)（入场裁决、红绿榜、证据附录）。
