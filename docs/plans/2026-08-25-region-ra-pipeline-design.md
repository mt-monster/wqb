# 每 Region 独立 RA Pipeline 设计稿

> 日期：2026-08-25 ｜ 状态：**设计稿，待用户决策后实施**
> 约束：只设计不实施；不强制基于 DB（实证仅作输入之一，profile 可静态声明）。

***

## 1. 背景与目标

现状：`wq-brain-ra-pipeline` 是**全区域共用**的九步骨架（S-PRE→S6），区域差异只体现在步 1 查表读出的参数（universe/delay/中性化/排除集）。问题在于：

- 区域差异**不止是参数差异**——KOR 需要 CW 预检严格闸 + 8 探针快判死，USA 需要 PROD 饱和强制拦截，ASI 需要处女地全量探针，MEA 入口即应冻结。这些是**流程变体**，当前骨架无法表达。
- 区域实证经验（死路/胜绩/有效面）散落在 DB、经验文档、skill 正文三处，开新战役时靠 LLM 记忆拼装，不可靠。

目标：**给每个 region 一套"独自的挖掘流程"** = 统一骨架 + 每 region 一份独立 profile（参数 + 流程变体声明），pipeline 执行时按 profile 渲染出该区域专属 SOP。

## 2. 核心设计原则

| 原则            | 说明                                                                                                 |
| ------------- | -------------------------------------------------------------------------------------------------- |
| 一骨架多 profile  | 九步骨架（S-PRE→S6）是共性，**不为每 region 复制一份 pipeline**（9 份维护地狱，违背 AGENTS.md 单源原则）。"独自"体现在 profile 驱动的流程变体。 |
| profile 可静态声明 | profile 内容以区域实证为初始值，但文件本身静态可读，不强制运行时查 DB。DB 实证用于**更新** profile，不是 profile 的存储前提。                   |
| 变体显式声明        | 每 region 的流程差异（跳步/加闸/改阈值/探针策略）在 profile 里显式写，不靠 LLM 临场发挥。                                          |
| 默认保守          | profile 缺失的字段回落到骨架默认值；未覆盖 region 走"通用处女地模板"。                                                       |

## 3. 总体架构

```
用户输入 region
    │
    ▼
┌─────────────────────────────────────┐
│ 路由层（ra-pipeline 步 1 增强）        │
│  加载 references/regions/<REGION>.md │
│  → 渲染该区域专属 SOP                 │
└─────────────────────────────────────┘
    │
    ▼
九步骨架（不变）◄── profile 注入 ──┐
    │                              │
    │   ┌──────────────────────────┴───┐
    │   │ Region Profile（每区一份）      │
    │   │  · 静态配置（universe/delay/    │
    │   │    中性化/universe 合法档）      │
    │   │  · 数据集红黑榜                 │
    │   │  · 信号族方向（有效面/排除族）   │
    │   │  · 流程变体（skip/override/    │
    │   │    gate 特化/探针策略）         │
    │   │  · 避坑清单（区域红灯）         │
    │   └───────────────────────────────┘
    ▼
S6 回写 → 更新 profile 的实证锚点（可选，非强制）
```

差异化只在四个点注入骨架：

| 注入点  | profile 字段                                         | 影响的步骤       |
| ---- | -------------------------------------------------- | ----------- |
| 入口裁决 | `entry_verdict`（active / probe-only / frozen）      | 步 1         |
| 生成先验 | `priors`（信号族 include/exclude、语法模式、win 配方）          | 步 4         |
| 闸门特化 | `gate_overrides`（CW/longCount/EVENT/prod\_corr 阈值） | 步 5、步 8     |
| 循环策略 | `loop_policy`（探针上限、快判死规则、停止条件）                     | 步 2、步 6、循环表 |

## 4. Region Profile Schema

```yaml
region: KOR
entry_verdict: active            # active | probe-only | frozen
one_liner: "小宇宙分析师预期变化区，大面积红灯"

static:
  universe: [TOP600]             # 合法档，禁止外推
  delay: [1]
  neutralization_default: STATISTICAL   # 或 dataset-dominant
  notes: "TOP600 小宇宙，CW/longCount 问题被放大"

datasets:
  red:    [chart_patterns, news_sentiment, ai_ml, credit_risk]   # 硬排除
  yellow: []                      # 标风险继续
  green:  [analyst_ratings, insiders, pv]                        # 优先

priors:
  signal_families_include: [analyst_revision, analyst_x_sh_mix]
  signal_families_exclude: [chart_pattern, news_emotion, ai_ml, credit_risk, glb_emotion]
  syntax_patterns: []             # 如 IND 的 scale(-rank(x))
  win_recipes:                    # 已验证配方，步 4 换腿用
    - "评级修正 × SH 混合（2 ACTIVE）"

gate_overrides:
  cw_gate: FAIL                   # WARN(默认) | FAIL —— 事件类 CW>0.5 直接毙
  longcount_min: 80
  prod_corr_early_warn: 0.7       # USA 降到 0.6

loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死，不扩批"
  stop_conditions: ["白名单被 dead_end 全覆盖"]

empirical_anchor:                 # 实证锚点（可选，S6 回写刷新）
  dead_ends_ref: "get_dead_ends(KOR)"
  last_verified: 2026-08-25
```

## 5. 逐 Region 设计

### 5.1 USA — 饱和市场正交战

- **定位**：最深最饱和。value/quality 种子全死，book 系 145 颗 ACTIVE 同族，任何经典变体 prod\_corr 必高。
- **static**：universe TOP3000（默认）/TOP1000/TOP500；delay 1/0；中性化 SUBINDUSTRY。
- **红榜**：pv1、mdl177（exhausted）、seed basics 全系。
- **信号族方向**：option9（进行中）、analyst 细分、event-driven（earnings）、news 高级情绪。
- **流程变体**：
  - 步 1 加 **PROD 饱和强制拦截**：`search_alphas_by_sharpe(USA, 1.58)` 同族 ≥10 → 该族进 exclude，步 4 GEM priors 硬排除；
  - 步 6 prod-first 每槽必查，`prod_corr_early_warn: 0.6`（比全局 0.7 更严）；
  - 步 7 Mode B 强制正交方向推荐（联动待实施的 P2-1）。
- **闸门特化**：`prod_corr_early_warn: 0.6`。

### 5.2 EUR — win 配方复用区

- **定位**：已有验证配方（`0.4×慢 MODEL 残差 + 0.6×快 PV`，SUBINDUSTRY + decay4），策略 = 换腿扩配。
- **static**：universe TOP1600/TOPCS1600/ILLIQUID\_MINVOL1M；delay 1/0。
- **流程变体**：
  - 步 4 **win 换腿权重最高**：每波 ≥2 槽按 EUR win 配方换腿（骨架已有此约束，EUR profile 将其升为强制）；
  - 步 6 设置可另探 ILLIQUID\_MINVOL1M/TOPCS1600/delay0（骨架已列，EUR 默认开启）。
- **闸门特化**：默认。

### 5.3 KOR — 小宇宙红灯区

- **定位**：TOP600 小宇宙，有效面集中在分析师预期变化；图表形态/新闻/AI/信用风险四大红灯。
- **static**：universe 仅 TOP600；delay 1；中性化 STATISTICAL。
- **红榜（硬排除）**：chart\_patterns（3 连死）、news\_sentiment（3 连死）、ai\_ml（3 连死）、credit\_risk（双死）、glb\_emotion（跨区铁律）。
- **绿榜**：analyst 系、insiders、pv。
- **流程变体**：
  - 步 2 白名单**极窄**：只留绿榜 + untried 集，配额不足时优先 analyst 族；
  - 步 3 typed catalog 必查 longCount（小宇宙放大覆盖问题）；
  - 步 5 **CW 闸升级**：事件类 CW>0.5 从 WARN 升 FAIL（KOR 事件类 CW 通病实证）；
  - 步 2/6 **8 探针快判死**：新集 8 探针无 |S|≥0.5 即判死回写，不扩批（小宇宙烧不起配额）。
- **闸门特化**：`cw_gate: FAIL`、`longcount_min: 80`。

### 5.4 IND — 长窗结构区

- **定位**：TOP500，长窗结构 2Y Sharpe 强（mdl177 3 颗 ACTIVE）；`scale(-rank(x))` 语法破墙实证。
- **static**：universe TOP500；delay 1。
- **红榜**：anl39、qfl（死）。
- **信号族方向**：mdl177 长窗结构族；慢变量。
- **流程变体**：
  - 步 4 priors 注入语法模式 `scale(-rank(x))`（破墙实证）；
  - 步 7/8 **评审加 2Y 维度**：`two_year_sharpe` 参与 judge 权重（IND 有效面在长窗，单看 IS Sharpe 会误杀）。
- **闸门特化**：judge 增加 `two_year_sharpe` 权重项。

### 5.5 ASI — 处女地全量探针区

- **定位**：未开垦。已知线索：analyst94 OS Sharpe 0.666 近闸、analyst81 推荐榜 untried。
- **static**：**universe 档位必须** **`get_platform_setting_options`** **实测**（禁止照抄 USA）；delay 实测。
- **流程变体**：
  - 步 2 **全量探针模式**：无 win 层，金字塔配额照旧（≥2 非 MODEL），全部候选集过 `dataset_health_check` 后排优先级；
  - 步 4 无 priors 可复用 → GEM 概念优先从头生成；每波必建 baseline（首批 5 槽纯探针合法，豁免"弱探针最多 1 槽"约束一次）；
  - 步 9 强制回写：处女地每个结论都是高价值实证。
- **闸门特化**：默认。

### 5.6 GBR — 半空白参照 EUR 区

- **定位**：有 waves 记录但无死路，半空白。市场结构与 EUR 相近。
- **流程变体**：
  - 步 1 **参照 EUR profile 起步**（静态配置先试 EUR 档），win 层为空 → 探针模式；
  - delay 0 可探（骨架已列为 EUR 可选项，GBR 继承试探）。

### 5.7 HKG — 小宇宙类 KOR 区

- **定位**：半空白小宇宙，处理类 KOR。
- **流程变体**：继承 KOR 的 CW/longCount 严格闸；注意与 CHN 联动信号（A 股相关性）。

### 5.8 MEA — 冻结区

- **定位**：TOP400 全区判死（9 数据集全 exhausted），不建议再入。
- **entry\_verdict: frozen**。
- **流程变体**：
  - **步 1 入口即拒绝**：registry 全 exhausted → 直接返回"MEA 已冻结"结论 + 转 `brain-nextMove-analysis` 选新区；
  - 唯一例外：用户显式强制 → 降级 `probe-only`，只允许白名单外新集探针 1 波，且事先声明配额成本。

### 5.9 GLB — 跨区铁律区

- **定位**：跨区铁律发源地（emotion 死路、anl15 精确表达式封禁）。
- **红榜**：emotion 系（跨区铁律）、anl15 精确表达式（封禁）。
- **流程变体**：universe 档位大（TOP3000+），delay 受跨区影响需实测；步 1 必读 `cross_region_lessons`（骨架已有，GLB 升强制）。

### 5.10 CHN — 实测档位区

- **定位**：默认档返空类试错历史，static 层必须实测。
- **流程变体**：步 1 强制 `get_platform_setting_options` 实测合法档（禁止外推任何区域档位）。

### 5.11 TWN — 小宇宙类 KOR 区

- 同 HKG 处理：继承 KOR 严格闸变体，先实测档位。

## 6. 流程变体总表

| Region | entry      | 步1        | 步2     | 步4               | 步5       | 步6             | 步7/8        |
| ------ | ---------- | --------- | ------ | ---------------- | -------- | -------------- | ----------- |
| USA    | active     | +PROD饱和拦截 | <br /> | priors排饱和族       | <br />   | prod-first 0.6 | Mode B 强制正交 |
| EUR    | active     | <br />    | <br /> | win换腿强制≥2槽       | <br />   | 可探三档设置         | <br />      |
| KOR    | active     | <br />    | 白名单极窄  | <br />           | CW升FAIL  | 8探针快判死         | <br />      |
| IND    | active     | <br />    | <br /> | +scale(-rank(x)) | <br />   | <br />         | judge加2Y权重  |
| ASI    | probe-only | 实测档位      | 全量探针   | 无priors从头        | <br />   | 首波探针豁免         | 强制回写        |
| GBR    | probe-only | 参照EUR     | 探针模式   | <br />           | <br />   | <br />         | <br />      |
| HKG    | probe-only | 实测档位      | 类KOR   | <br />           | 类KOR CW闸 | <br />         | <br />      |
| MEA    | **frozen** | 入口即拒      | <br /> | <br />           | <br />   | <br />         | <br />      |
| GLB    | active     | 铁律升强制     | <br /> | 排emotion/anl15   | <br />   | <br />         | <br />      |
| CHN    | probe-only | 强制实测档位    | <br /> | <br />           | <br />   | <br />         | <br />      |
| TWN    | probe-only | 实测档位      | 类KOR   | <br />           | 类KOR CW闸 | <br />         | <br />      |

## 7. 实施选项（三选一，待决策）

### 方案 A：DB profile 层（改动 DB）

- 做法：`regions` 表加 `pipeline_profile` JSON 列（或 `registry_empirical` static 层加 profile 键），matrix 步 2 查表时一并读出，ra-pipeline 步 1 注入。
- 优点：与现有查表层一体，S6 回写天然刷新 profile；单轨 DB 纪律一致。
- 缺点：DB schema 变更 + 迁移；profile 评审不直观（要查库）；违背"可以不基于 db"的轻量诉求。
- 工作量：中（schema + campaign.py registry 扩键 + matrix/ra-pipeline 各一段）。

### 方案 B：文档 profile（推荐）

- 做法：`wq-brain-ra-pipeline/references/regions/<REGION>.md` 每区一份（YAML front-matter 存 schema 字段 + 正文写变体理由），ra-pipeline 主 SKILL.md 步 1 加"加载区域 profile"路由段；DB 实证仅作 profile 的**更新来源**（S6 回写时顺带刷新 `empirical_anchor`），运行时不强依赖。
- 优点：不改 DB、skill 自包含、每区 SOP 可直接评审/迭代；符合"可以不基于 db"；与 references/decision-table.md 现有模式一致。
- 缺点：DB 与 profile 双源（用 `empirical_anchor.last_verified` 缓解：profile 落后于 DB 时提示刷新）。
- 工作量：中偏小（11 份 profile 文档 + 主 SKILL.md 路由段 + 4 个注入点说明）。

### 方案 C：每 region 独立 skill

- 做法：`wq-brain-ra-pipeline-kor` 等 11 个 skill，INDEX.md 注册。
- 优点：最"独自"。
- 缺点：9+ 份骨架复制，维护地狱，直接违背 AGENTS.md 单源原则与"brain-deepExplore 废止并入"的历史决策。**不推荐**。

**推荐：方案 B**（或 B+A 混合：文档为准，DB 存镜像供 matrix 查表标注）。

## 8. 待用户决策点

1. **覆盖范围**：11 个 region 全做，还是先做 6 个重点（USA/EUR/KOR/IND/ASI/MEA）？
2. **实施方案**：A / B / C（推荐 B）？
3. **profile 粒度**：只写参数差异（轻），还是含流程变体（本稿默认，重一点但才有"独自流程"的意义）？
4. **MEA 冻结态**：是否接受"入口即拒绝"的硬冻结，还是保留 probe-only 后门？
5. **与中断任务的衔接**：P2-1（正交方向推荐）与 P3（日报饱和度）未实施完，USA profile 的 Mode B 强制正交依赖 P2-1——是先补完 P2/P3 再实施本方案，还是并行？
6. **未同步副本**：此前 P0/P1 改动还在 trae-cn/qoder-cn 单副本未三向同步，实施本方案前是否先同步+validate？

