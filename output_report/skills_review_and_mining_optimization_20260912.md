# Skills 总结 · 代码审查 · Alpha 挖掘优化方案

> 2026-09-12 · 基于 `data/wqb.db` 全量数据（1,847 alphas / 11,017 expressions / 600 waves / 24.8 万 fields）+ 仓库 32 个 skills + src/wqb 七子包实测审查。
> 数据快照时点：2026-09-12 00:20 GMT+8。⚠️ 本地 `alphas` 表与平台存量存在已知偏差（本地缺外提 alpha，USA 本地 11 vs 平台约 133），涉及存量的结论以倍率级趋势为准，绝对值以 `sync_platform_alphas` 全量翻页为准。

---

## 一、Skills 全景总结（仓库 32 个）

### 1.1 分类地图

| 类别 | 数量 | Skills | 一句话定位 |
|---|---|---|---|
| **SOP 编排** | 5 | `wq-brain-ra-pipeline`、`wq-brain-campaign-matrix`、`wq-brain-campaign-toolkit`、`wq-brain-ppa-mining`、`wq-brain-superalpha` | 唯一 SOP 入口（九步 S-PRE→S6）+ 区域×数据集战役矩阵 + 战役引擎（gate/wave/ledger）+ PPA/SA 两条特殊通道 |
| **生成/回测** | 3 | `brain-make-some-gem`、`brain-sim-alphas-in-batch-and-track`、`brain-feature-implementation` | GEM 七槽生成、批量回测（断点续跑 + multi-sim 8 并发 86α/hr）、idea→表达式 |
| **研究/数据** | 8 | `brain-alpha-research` 及其 field-quality / hypothesis-first / news-sentiment 三个子方向、`brain-data-feature-engineering`、`brain-datafield-exploration-general`、`brain-dataset-exploration-general`、`alpha-template-labs-data-analysis` | 数据集/字段研究、字段质量先验、饱和数据集的假设优先挖掘、新闻情绪 6 桶框架、Labs 原始数据诊断 |
| **质量/验证** | 6 | `alpha-expression-verifier`、`brain-how-to-pass-alpha-test`、`brain-alpha-robustness`、`brain-alpha-judge`、`brain-alpha-repair`、`brain-calculate-alpha-selfcorr-quick` | 语法校验、提交闸门阈值手册、稳健性归因、参考级评审（非提交权威）、弱候选修复、本地相关性快算 |
| **优化** | 1 | `wq-brain-alpha-optimization-v1` | Mode B（想法层）+ Mode A（参数层）两模式优化器 |
| **提交** | 1 | `worldquant-submit-alpha` | 真·提交 API（覆盖 201 受理/异步失败/配额扣减的坑） |
| **运维/监控** | 3 | `wq-backtest-monitor`、`brain-next-move-analysis`、`wqb-concurrency` | 机器级进程盘点、综合日报、429/并发调优 |
| **辅助** | 5 | `brain-explain-alphas`、`brain-inspect-raw-template-create-setting`、`brain-forum-browse`、`planning-with-files`、`pull-brain-skills` | 表达式解释、模板检查、中文论坛浏览、文件化规划、skill 导入 |

另有用户级 skill（`~/.workbuddy/skills/`，不随仓库分发）：`brain-enhance-template`（模板增强命令行）等。

### 1.2 九步覆盖矩阵（SOP × skills）

| SOP 步 | 主责 skill/tool | 覆盖状态 |
|---|---|---|
| S-PRE 前置 | campaign-matrix（区域配置）、toolkit gate.py（8 闸预检） | ✅ 完整 |
| S0 选数据集 | campaign-matrix + dataset-exploration + field-quality + research | ✅ 完整 |
| S1 查表 | datafield-exploration + data-feature-engineering | ✅ 完整 |
| S2 生成 | make-some-gem（强制七槽）+ feature-implementation | ✅ 完整 |
| S3 字段分级 | tools/field_inspect_gate.py + field_profile（3.07 万行） | ✅ 完整 |
| S4 priors + 发批 | assemble-priors + sim-alphas-in-batch（BATCH8） | ✅ 完整 |
| S5 门禁 | toolkit gate.py + **wave_gate 节点（09-11 新入 MCP）** | ✅ 09-11 补齐 |
| S6 跟踪 | batch_track 节点 + wq-backtest-monitor | ✅ 完整 |
| S7 评审 | robustness + how-to-pass + selfcorr-quick | ✅ 完整 |
| S8 提交 | worldquant-submit-alpha + submit_alpha 节点 | ✅ 完整 |
| S9 复盘 | next-move-analysis + campaign_intel + forum-browse | ✅ 完整 |
| **横向：组合级分析** | — | ❌ **缺口**（见 P0-3） |
| **横向：配额调度** | — | ❌ **缺口**（见 P0-1） |

**结论**：九步纵向链路已闭环（含 09-11 补齐的步 5 MCP 节点），**横向能力有两处空白**——组合级正交分析与多通道配额调度。这两个空白恰好对应当前两大瓶颈（PROD/SELF 撞墙、配额空转）。

---

## 二、项目代码审查

### 2.1 架构分层（健康度总评：**良好**）

```
src/wqb/                    七个子包
├── expression/   语法/算子/多样性增强（validator、op_arity、diversity_enhancer）
├── memory/       idea 台账 + 事件（idea_store、idea_ledger）
├── modeb/        Mode B 变换引擎（并行工作流开发中）
├── research/     证据/假设挖掘/新闻字段分类
├── search/       调度器 + 失败记忆（scheduler、failure_memory）
├── store/        DB 湖 12 个访问模块（_schema 单点建表）
└── workflow/     8 节点 registry（campaign/feature_eng/gem/batch_track/judge/
                  submit_alpha/superalpha/wave_gate）+ executor + mode_b
tools/            104 个 CLI（有 README 索引，退出码 0/1 可串 pipeline）
Claude/skills/    32 个 skill（仓库真相源，sync_skills 推 4 安装位）
data/wqb.db       17 表数据湖
tests/            23 文件 / 727 tests，11.8s 全绿
```

**优点**：测试覆盖扎实且新增了文档-代码一致性回归（首跑即拦截 10 个真实缺陷）；store 层单点 schema；tools 退出码约定统一；技能根解析已单源化（09-11）。

### 2.2 发现与风险（按严重度）

| # | 发现 | 证据 | 影响 | 建议 |
|---|---|---|---|---|
| R1 | **`expressions.dataset` 列脏标 4,596 行**——区域名（USA/KOR/IND/EUR/MEA/CHN）被写进 dataset 列 | `SELECT COUNT(*)…dataset IN ('USA',…)` = 4596 | 数据集级开采深度分析失真（如"IND 75 条 S≥1.58"其实 dataset 未知） | 一次性清洗（region 字段回填）+ store 写入口加枚举校验 |
| R2 | **gate_results.report_json 顶层 schema 不统一**，287 份失败报告结构化解析 0/287 可用（成功版有 `syntax/gate` 节点，失败版结构不同） | 逐份 JSON 解析实测 | "哪道闸杀最多"无法可持续聚合，闸门调优靠猜 | 统一 report schema（`{wave, dataset, checks:[{name,result,detail}]}`），写 gate.py 时同步改 |
| R3 | **sqlite 连接无 WAL / busy_timeout**（memory/db.py:51、idea_store.py:48、store/campaign.py:79 均裸 `sqlite3.connect`） | grep 实测 | 多进程并行工作流写同库有锁冲突风险（当前确有多会话并行） | 连接工厂统一 `PRAGMA journal_mode=WAL; busy_timeout=5000` |
| R4 | **提交台账疑似断链**：09-08 后无新记录；75 条中 53 条是 09-07 历史回补，真实新提交 ≤22 条 | submission_ledger 按日分布 | 要么配额在空转（见 P0-2），要么提交后未回写 → 状态盲区，双闸预检会低估 | 核对平台 `dateSubmitted` 反推；`worldquant-submit-alpha` 提交成功路径强制回写 |
| R5 | **本地 alphas 表与平台存量偏差大**（USA 本地 11 ACTIVE vs 平台约 133） | 本地 DB vs 记忆实证 | SELF/PROD 本地预检系统性低估；点塔/SA 池判断失真 | `tools/sync_platform_alphas.py` 常态化（每日 automation） |
| R6 | **脏树 ~50 文件**（Mode B / multidim / EUR·KOR 阈值 / config.py TOP600 等）属并行工作流未提交 | git status | 多写者互相覆盖风险（本轮已实证一次：assemble_priors 被并发改写） | 按 09-11 新增 §7 提交纪律尽快切分提交 |
| R7 | CHN 44 条回测 avg\|S\|=1.68 却 0 条 S≥1.58，口径可疑（可能非同标准） | backtest_results 抽查 | 低优先；疑 CHN 走 PPA/其他通道口径 | 单独核查 CHN 结果口径 |

---

## 三、从挖掘 alpha 角度的优化方案（核心）

### 3.1 实证基础：钱和算力都花在哪了，产出在哪

**① 配额利用率——最大的浪费在提交端**

| 指标 | 实测 | 判读 |
|---|---|---|
| PPA 通道提交（`POWER_POOL_SUBMISSION` 1/ET 日，闸最宽松） | **0 次**（ledger 全量 75 条：REGULAR 72 + SUPER 3，无一条 PPA） | ★ 白给配额从未动用；纪律（"当天先提 PPA"）已写进记忆，但管道从未落地 |
| SUPER 通道 | 3 次 | 明显低用（KOR/USA 已满足 ≥10 ACTIVE 前置） |
| 近 12 天 REGULAR 提交 | 09-01:7、09-02:3、09-08:2，**09-09 起 3 天 0 条** | 每天空转 4+1+1=6 个名额，3 天 ≈ 18 个名额蒸发 |

**② 区域投入-产出（backtest_results 实测）**

| 区 | 回测数 | S≥1.58 命中率 | waves 投入 | 判读 |
|---|---|---|---|---|
| IND | 267 | **36%** | 88 | 产出王，应继续加注 |
| MEA | 450 | 22% | 78 | 健康但本季 SUPER 通道关闭（400） |
| USA | 214 | 10% | 126 | 中等；SA 池已饱和（SELF/PROD 双闸无共同可行域） |
| KOR | 276 | 4.7% | 86 | 低效 |
| EUR | 202 | 4% | **141**（全库最高） | ★ 严重低效：投入第一、产出倒数 |
| GBR | 180 | **0%**（max\|S\|=1.04） | 39 | ★ 信号天花板问题，非流程问题——换方向，别再跑 |
| HKG | 16 | 0% | **7**（38 条表达式） | ★ 点塔 A 档目标（HKG/D1/SHORTINTEREST）投入严重不足 |
| ASI/GLB/CHN | 14/5/12 波 | 0% | 少 | GLB 情绪族 42 候选已全灭（PROD 0.82–0.86），战略性放弃存量打法 |

**③ 数据集开采深度**（93 个 dataset，剔除脏标后）

头部集中：`multifactor_return_pred` 643、`multi_horizon_alpha` 611、`predictive_starmine` 456、`ai_equity_alpha` 450、`pattern_scores` 359 —— 头部 5 个 dataset 吃掉约 45% 表达式量，且均属 MODEL 类主流方向（记忆实证：主流方向信号级饱和）。**历史规律：已 ACTIVE 的 20 条 IND 全走冷门数据集（pv106/transaction_cost/anl9/oth696/fnd86/mdl177）**——产出在长尾，算力在头部。

### 3.2 优化方案

#### P0（本周，直接换回提交产出）

**P0-1 · 三通道配额调度器（新 skill + automation）**
现状是"有候选才提交、没人值守就空转"。建 `tools/quota_dispatch.py`（或 skill `wq-brain-quota-dispatch`）：每日 ET 开盘后按 **PPA(1) → REGULAR(4) → SUPER(1)** 顺序扫描可提交池（gate_results 全过 + selfcorr-quick 预检 + 描述 ≥100 字），自动生成提交清单。配 WorkBuddy automation 每日 12:00 GMT+8 跑一次。**预期收益：仅 PPA 通道一项，每年多出 ~365 次宽松闸提交机会；消灭 18 名额/3天 级别的空转。**

**P0-2 · 提交回写闭环**
`worldquant-submit-alpha` 成功路径强制写 submission_ledger（含 PPA 类型枚举值），失败路径记 FAIL + 原因；每日与平台 `dateSubmitted` 对账（复用 R5 的同步工具）。没有这条，P0-1 的调度器就是盲飞。

**P0-3 · 组合正交地图（九步横向缺口 → 新工具）**
PROD/SELF 撞墙的本质是**逐 alpha 试错**，缺组合视角。建 `tools/book_orthography_map.py`：拉全量 ACTIVE（平台翻页）→ 两两 PnL 相关矩阵 → 聚类出"信号簇"→ 可视化空白象限 → 输出"与现有 book 相关性 <0.3 的可挖方向"清单，反哺 campaign-matrix 的 dataset 选点。这是打穿 PROD 0.7 硬闸唯一系统性的路（记忆实证：存量候选要么 SELF 0.81–0.87、要么 PROD 0.73–0.82，逐颗试错已证明无解）。

#### P1（两周内）

**P1-4 · 区域投入再平衡**
- EUR：141 波 / 4% 命中 → **冻结新波**，存量候选走 P0-1 调度器消化；
- HKG/D1/SHORTINTEREST（A 档塔）：7 波 → 加注到 30+ 波，借 `field-quality` 先验选 SHORTINTEREST 字段种子，wave_gate 的 `signal_floor` 用窄截面低值（0.5）起步；
- GBR/D1/MODEL：**停止模板遍历**（180 条 max|S|=1.04 证明天花板），改走 `brain-alpha-research-hypothesis-first`（饱和数据集假设优先工作流，skill 已就位但从未在该区启用）；
- IND：继续加注（36% 命中），重点从 model32/model252 转向未开采冷门 dataset（呼应历史规律）。

**P1-5 · 数据集记分板（campaign-matrix 的动态化补丁）**
建 `tools/dataset_scoreboard.py`：按 `expressions.dataset`（R1 清洗后）× waves 数 × S≥1.58 命中率 × 距上次尝试天数，输出"饱和/欠开采/未动"三色榜。S0 选数据集时强制先查榜，防止再往 `multifactor_return_pred` 这类已饱和 dataset 倾倒算力。

**P1-6 · R1 脏标清洗 + 写入口校验**（数据集记分板的前置）
**P1-7 · R2 report_json 统一 schema**（闸门调优从猜变看）
**P1-8 · R3 sqlite WAL**（连接工厂 3 处统一）

#### P2（本月）

**P2-9 · OS 归因闭环**：`backfill_alpha_metrics` 已有雏形 → 加"OS 衰减率 → 生成端先验降权"映射（哪类结构 OS 掉得狠，GEM 七槽就少给槽位），让 S9 复盘真正反哺 S2。
**P2-10 · 多账号并发**：已实测 multi(8)=86.1 α/hr vs single 54.3；tabbit 模式（独立账号 CONCURRENCY3）验证过可行性 → 第二账号可再 +50% 吞吐，优先喂 P1-4 的 HKG 加注。
**P2-11 · R5 平台同步常态化**：WorkBuddy automation 每日跑 `sync_platform_alphas.py`。

### 3.3 落地顺序与依赖

```
P0-2 回写闭环 ─→ P0-1 配额调度器 ─→ 每日 automation
P1-6 脏标清洗 ─→ P1-5 数据集记分板 ─→ P1-4 区域再平衡（选点依据）
P0-3 正交地图 ──────────────────→ 反哺 campaign-matrix 选点
P1-7/P1-8 可并行随改随提
```

**一句话总纲**：纵向九步链路已经闭环，下一步的产出弹性不在"再修流程"，而在 **① 把白给的配额（PPA/SUPER/空转）接回来，② 把组合级正交性变成选点依据，③ 把算力从饱和头部 dataset/低效区域搬到长尾冷门 dataset 和 A 档塔**。

---
*附：本报告数据均可复现——SQL 见 `data/wqb.db`（expressions / backtest_results / gate_results / submission_ledger / waves 五表）；skills 清单见 `Claude/skills/INDEX.md`。*
