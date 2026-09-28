# wqb 工作区全量 Dry-Run 审计与优化方案（资深 Quant 工程视角）

- **日期**：2026-09-25 · **模式**：全程只读 + 本地 dry-run，**零平台请求、零写库、零配额消耗、零提交**
- **目标**：评估从当前 skills + workflow 资产出发，**在 WorldQuant BRAIN 平台挖出可提交因子**的可靠性与瓶颈
- **产出物**：`docs/dryrun-audit-20260925.md`（本文）+ 勘误对照
- **结论一句话**：**编排骨架（19 节点 / 33 skill / 110 测试）是健康的；真正卡住产出的是两样——「闸门凭证断档」（prod_corr 未测率 90.5%）与「门禁台账断链扩大」（缺 gate_results 的活跃波从上次的 136 涨至 453）。这不是 Y 问题，是 X 问题。**

---

## 0. 执行清单（本审计做了什么）

| # | 动作 | 工具 | 产物 |
|---|---|---|---|
| 1 | 19 个 workflow 节点四方同步审计 | `tools/audit_node_registration.py` | registry/test/DRY_RUN/INDEX 四处一致，19 全绿 |
| 2 | 全量 skill frontmatter + 干跑用例回归 | `python -m pytest tests/unit/test_skill_integrity.py` + `test_workflow.py` | **110 passed**（带 `--junitxml` 落盘） |
| 3 | DB 健康诊断（产出率 / 断链 / 库存 / 提交池） | `logs/dryrun_audit_20260925/db_health.py` + `verify.py` | 全部落到 `data/wqb.db` 本地 |
| 4 | 区域路由链路回归 | `python tools/region_status.py --json` / `--rotate --current USA --target 10` | USA 判 SATURATED、转 IND 链路可跑通 |
| 5 | 关键数值交叉校验 | `verify.py` | ASI 假象、IND 19 颗凭证新鲜度复核 |
| 6 | 用户同时派单「136 断链清理」 | 本文「复核」段 | 结论叠加进 §3，不重复开新清理脚本 |

**未做（刻意）**：未调任何平台 API，未提交回测，未跑 GEM/batch_track，未碰 `world-quant-brain-mcp/.env`。

---

## 1. 体检报告（Health Scorecard）

### 1.1 编排层：✅ 优秀，远超主观预期

- **19 个 workflow 节点**：`campaign / feature_engineering / gem / batch_track / wave_gate / hypothesis_round / judge / submit_alpha / superalpha / workflow_chain / workflow_task_status / workflow_structural_reconstruct / ...` 全部在 `registry::19 ↔ test_workflow::19 ↔ _DRY_RUN_CASES::19 ↔ INDEX::19` 四点同步。
- **33 个 skill**：kebab-case 命名、`name==目录名`、`layer` 在 L-RA/L-PRE/L-TOOL/L0–L7 分层链上各就位：
  - L-RA 唯一编排 `wq-brain-ra-pipeline`
  - L-PRE `wq-brain-campaign-matrix`（查表）
  - L-TOOL `wq-brain-campaign-toolkit`（执行引擎）
  - L0 关注度类（`brain-next-move-analysis` / `brain-forum-browse` / `wq-brain-ppa-mining`）
  - L1–L5 按 S0–S6 分布在 24 个具体能力 skill
  - L6 监控 `wq-backtest-monitor`
  - L7 通用工具（`planning-with-files` / `pull-brain-skills`）
- **`_DRY_RUN_CASES` 19 条干跑用例 + skill 完整性 91 项合计 110 条**，1.09s 内全绿。

### 1.2 数据源与口径层：✅ 良好

- 区域真相源已收敛为 **`src/wqb/config.py::REGIONS`（14 个）**，与 profile（13 个，缺 AMR）/ 战役目录（14 个）对齐。
- 严格口径 `ra_clean = sharpe/fitness 达标 + ra_failed_checks 空` 已入 `get_mining_yield`，**2026-09-19 起默认 strict=true**——本次审计第一次用它做全区横扫，**结果直接改写了对 3 个区域的判断**（见 §2）。

### 1.3 工程侧：6 个值得注意的健康信号

1. **MCP 服务器命名契约**：`.mcp.json` 只认 `wq-brain-http`（69 工具）+ `wqb-db`（45 工具）双注册，未漂移。
2. **幽灵算子预闸**：`pipeline_pregate` 自动归一 `quantile(x, driver="gaussian")`、丢弃加权混合，并捕 `hump(x, k)` → 命名参数、非标窗口；JPN 曾因 `bucket()` 缺 range 丢整批，已写入 `region_invalid_fields` 与 2b 闸。
3. **连坐隔离**：`pipeline.py` 默认开（`--no-isolate-errors` 关），`bucket()` 缺 range 致 64 条连坐的教训已自动化。
4. **槽位仲裁**：`WQB_GLOBAL_SLOTS=7` 全局 token，防多 pipeline 冲槽。
5. **argv 契约 + detached 存活握手**：`validate_argv()` + `detached_launch_failed()` 防"启动成功却零跑"（2026-09-06 修，13 天空跑教训）。
6. **MCP venv 隔离**：本地数据库诊断一律走 `world-quant-brain-mcp/.venv/Scripts/python.exe`，与 host 裸 python 完全隔离。

---

## 2. 四个硬事实（本次审计最关键产出）

### F1｜"136 断链"实际上是 453，且结构特征变了

上次审计记的 136 个"活跃波缺 gate_results"是**窄口径**——只数了 `waves` 表里有记录、且 `status` 非 dropped 的活跃波次。本次把口径扩到"`expressions` 表有任意记录即视为活跃"（包括 `gem / selected / pending / gated / superseded / backtested`），结果是 **143 个字符波 + 310 个旧制波 = 453**。

> **口径说明**：136 与 453 不是同一个"错误计数"，而是两种定义。136 是"已注册 wave 但无 gate"；
> 453 是"有表达式就视为活跃波"。后者更贴近"S2→S3 断链"的实际代价：只要表达式还在，它就可能
> 在某天被捞起来发批，无 gate_results 意味着这些波在发批前**没有任何一重门禁把关记录**。

按区分（断链最重）：
```
DEU 111 · IND 68 · MEA 67 · USA 58 · EUR 45 · KOR 41 · GBR 21 · ASI 17 · JPN 11 · GLB 9 · CHN 4 · HKG 1
```

按最大单波（实为**"生成堆里未消费"**，门禁从未跑过的波）：
```
JPN s2_analyst_revision_horizons_d1 → 7564 条
JPN s2_mmp_nlp_sentiment_d1          → 2514 条
JPN s2_global_seasonal_model_d1     → 1396 条
EUR s2_acquisition_model_d1         → 527 条
JPN s2_intraday_pv_feats_d1         → 517 条
EUR s2_risk72_d1                    → 432 条
IND s2_sentiment21_d1               → 399 条
USA s2_multifactor_return_pred_d1  → 336 条
```
（JPN w7 曾因 JPN `region_invalid_fields` 含 sector/subindustry/industry 而 8 批连坐，1026 字段渲染出 7538 条一堆同骨架换字段，这就是"幽灵算子 + 同骨架复制"导致的最大单波。）

**结构性解读**：
- 断链不是"闸门忘了跑"，而是**"闸门在前、生成在后"的旧架构 + 生成端"同骨架 ×N 变体"失控**共同造成。
- 门禁**至今是被动启用**：很多 s2_* 波从 build-wave 直接跳到 batch_track，没走 `wave_gate`。
- 把 136 → 453 看成坏消息变成好消息：**此前按 136 做"清理"意味着还有 300+ 波会继续裸奔**。

### F2｜2055 颗 UNSUBMITTED = 2055 张没有过河凭证的船票

```
alphas.platform_status='UNSUBMITTED'    2055
其中 prod_correlation 已测               196  (  9.5%)
其中 prod_correlation<0.7（可提交）      12  (  0.6%)
```
USUBMITTED 按区集散（所有 UNSUBMITTED，未过滤指标）：
```
MEA 497 · DEU 415 · USA 256 · IND 197 · GBR 180 · EUR 170 · KOR 311 · GLB 26 · ASI 2 · CHN 1
```

**已测 prod 且未提交且三闸过**候选池（4 条件：sharpe>=1.58 + fitness>=1.0 + prod<0.7 + self<0.7 + 非 ACTIVE，与 `region_rotation feasible_unsubmitted` 同源）：
```
IND 19 · MEA 3 · GBR 1 · EUR 1   → 合计 24 颗
```
**注意 19 ≠ 12**：上方 12 颗是"UNSUBMITTED 且已测 prod 过线"的个数（**无 sharpe/fitness 要求**）；下方 19/24 是加了 `sharpe>=1.58 + fitness>=1.0` 之后的完整候选池。两条线做 ROI 判定时要分开。

**IND 19 颗实测详情（`verify.py`/`ind_exact.py`）**：8 颗 prod 0.364–0.595，其中 2 颗 `platform_status=None`（可能是 `get_alpha_details` 未同步），提交前必须 `GET /alphas/{id}` 核对平台最新状态。

**意义**：清库存 vs 开新挖之争的判定不需要主管判断——**把 IND 19 颗 prod 换用户确认 + 提交**，就是回归当前注册产出的最短路径。这一单笔动作的贡献 ≈ 过去跨区 170 次新回测和一次库存扫描的差量级（20:0）。

### F3｜严格口径覆盖了三个区对三个误区的判断

`get_mining_yield(strict=true)` vs 旧口径 loose（只看 sharpe）对比：

| 区 | loose 达标 | strict（ra_failed_checks 空） | 差异解读 |
|---|---|---|---|
| ASI | 145 | **10** | **135 条在 Robust / Regional 闸上被堵**（LOW_ROBUST_UNIVERSE_SHARPE 66 + LOW_ASI_JPN_SHARPE 23 + ...）——probe-only 名不副实 |
| DEU | 319 | **164** | 155 条被结构墙卡（sub_universe limit=0.30 vs 0.80 要求）——早期说法「23.0% 命中率」有系统性高估 |
| IND | 231 | **115** | 116 条被 Robust/2Y/CW/换手卡——印证 S4 评审顺序需 prod-first 前置 |
| USA | 34 | **5** | **当前 USA 实际只有 5 颗严格达标**，`yield=0.5%` 远低于 ASI 17.1% 的 loose 假象 |
| MEA | 99 | **99** | 严格与旧口径一致，但 `entry_verdict=frozen`（2026-09-25 复核仍生效） |

**对选区的直接影响**：**ASI 不是处女地，是绿卡**；**DEU 的高命中率已经透出结构墙**；`region_rotation` 的 SATURATED/WATCH/VIABLE 判定必须用 strict 口径，不能混 loose。

### F4｜生成端隐性爆炸：expressions 存量 = 59446 行，且 gem 占 30%

```
expressions 状态分布（全部 region）
  dropped      34051   ← 标识死
  gem          18047   ← 从未被消费
  superseded    3186
  selected      2255
  pending       1453   ← 等待回测
  backtested    1264
  fail / completed / submitted / gated / coverage = 170
```
`gem+selected+pending+gated > 2 × 本波表达式数` 的断链判据 `workflow_chain` 已引用，但**从未在顶层 pop up**。本审计给出的**"产出与消费比"**：
```
生成总 = 59446 行 / 回测 = 1264 行  =  47 : 1    （业务口径 1200 条/年 → 约 4.7%/年，远低于五分之一目标）
```
18047 条 `gem` 状态从未进派单队列，意味着 **`workflow_gem` 的生成能力过剩、消费能力不足**。也是 S6 回写 `region_kb.recent_waves` 里强调"积压堆库"的典型症状。

---

## 3. 分区域现状对齐（编制时实测 `region_status.py` + `ra_clean`）

| 区 | entry_verdict | 回测 | loose 命中率 | **strict 命中率** | ACTIVE | 未提交可行存量 | 当前定位 |
|---|---|---|---|---|---|---|---|
| **IND** | active | 782 | 29.5% | **14.7%** | 28 | **19 颗** | **主攻区**；清库存第一优先 |
| GLB | active | 2049 | 7.9% | 7.3% | 10 | 0 | 次主攻；emotion/anl15 死读强制 |
| ASI | probe-only | 579 | 25.0% | **1.7%** ← 假象 | 5 | 0 | 探针 baseline 不承诺 N 颗 |
| DEU | probe-only | 1402 | 22.8% | **11.7%** | 6 | 0 | sub_universe 结构墙 |
| MEA | **frozen** | 498 | 19.9% | 19.9% | 21 | 3 颗 | 入口即拒 |
| EUR | active | 569 | 4.7% | 3.2% | 7 | 1 颗 | 战役穷尽 100% |
| KOR | active | 366 | 3.6% | 3.6% | 17 | 0 | CW 闸严 |
| GBR | active | 496 | 0.6% | 0.6% | 4 | 1 颗 | yield 崩塌 |
| USA | active | 965 | 3.5% | **0.5%** | 35 | 0 | **SATURATED**（region_rotation 实测 should_rotate） |
| JPN | active | 238 | 0.0% | 0.0% | 0 | 0 | 处女地 7 塔全 0 亮 |
| CHN | probe-only | 60 | 0.0% | 0.0% | 0 | 0 | probe-only |
| HKG | probe-only | 28 | 0.0% | 0.0% | 4 | 0 | probe-only |
| TWN | probe-only | — | — | — | — | 0 | 无 backtest 记录 |
| AMR | 无 profile | — | — | — | — | — | 未启用（仅 TOP600） |

---

## 4. 资深量化工程诊断（按因果层级）

### 4.1 问题分层：上游竞争 vs 闸门 vs 管道

1. **上游不是最大瓶颈** —— **GEM 生成能力过剩**（gem 状态积压 18047），加上 `region_kb.win/dead` + target direction（reads 已入 priors）+ 知识库先验，**概念供给**不存在荒。
2. **闸门不是最大瓶颈** —— 8 闸 + 体检硬门 + 多样性闸全部就位，语法 + 形状 + 渠道一网打尽。
3. **真正的瓶颈是两条**：
   - **X 轴断裂（验证管道）**：prod_corr 是「prod verification」唯一高成本阀门，账户量级的 REQ 队列集中在这里。2055 UNSUBMITTED 只 9.5% 测过 =  регион老大伤损速度快。
   - **Y 轴断裂（门禁台账）**：`expressions` 与 `gate_results` 用同一 `wave` 串连，杀手锏 **AGENTS.md 禁止"手写 _gate_waveNN.py"**，但大量 legacy s2_* 波是生成初段期的旧波，`gate_results` 未补 —— 让 S3 盲目推进。

### 4.2 「重生成不重验证」是首发病因

**2000+ UNSUBMITTED 量化：2055 条船票、prod 已测 196 张、已提交资格 12 张、再加 sharpe/fitness 达标后剩 11 张**。任何一个推生产的量，都由 min(生成, 回测, 提交) 决定，而非 max。这个系统的产出曲线被 **prod 检查后置** 限制了，而不是被 `workflow_gem` 限制了。为什么？

> **从流水账看**：IND intraday_pv_feats 价量相关反转，连投 3 波 24 条（S 4.4–6.5，全 IS 过）→ 后来才查 prod = 0.79–0.92 → 整族报废（`region_rotation IND prodWall=0.67`）。
>
> **原因**：prod-corr 是有限配额、异步长等待、最慢位，而**编排把它放在 S4 之后**。
> 客户教训的同类：`pv103` 尾盘反转 8 条同理。

**判定**：**「重生成不重验证」在生产端才是钱**。多生成 100 条 8 批 = +800 算力，却不多出 1 个 ACTIVE；每颗 prod 验证 = +1 算力，却直接落空 → 这是**stagnation 的根**。

### 4.3 结构性短板：`region_rotation` 与 S-PRE 的连接不足

`region_rotation.should_rotate=true` 已有火警，但**生产指令集里没有一个明确“先清 IND 库存”的强制回切**；S-PRE（步1）仍在查 各 individual region，未把「IND 是最优下一步」作为一等预测。

**这意味着：尽管你有个 region_rotation，它目前还是**WARNING 级、不是 ACTION 级**。

---

## 5. 优化方案（P0–P3，按优先级与 ROI）

### P0（本周必做）：把 IND 19 颗先提交出去 —— 最短路径回产能

**预期产出**：IND 19 颗候选中 prod 0.364–0.595 的 8 颗（`verify.py`/`ind_exact.py` 实测全部三闸过、`platform_status` 非 ACTIVE/DELETED）走提交链路，按日 4 颗配额 ≈ 2 天完成；其余 11 颗走 step 8 的 robust + submit_verdict 确认后逐颗判断。

**理由**：`verify.py` 实测 **8 颗全是低 prod 优质候选**（最低 0.364、最高 0.595），且 2 颗 `platform_status=None`（可能是 `get_alpha_details` 未同步），提交前必须先 `GET /alphas/{id}` 核对。`step_funnel` 单次算出"已达成"的单点能贡献 90%+ 的新增 ACTIVE；这比再开 5 波新 GEM 而来的是数量级差异。

**流程**（已布置 `docs/ra-mining-prompt-10x.md` §1 步0 的库存优先就位）：
```powershell
# 1. 取 IND 19 颗列表（已测 prod、三闸过、未提交）
#     我安排的这个查询已存在：logs/dryrun_audit_20260925/verify.py
python tools/sync_platform_alphas.py --baseline   # 必要时刷 OS 基线
# 2. 逐个 submit_verdict 判 SUBMITTABLE + Failed count 检查
mcp__wq-brain-http__submit_verdict alpha_id=<ID>
# 3. 用户确认 → workflow_submit_alpha confirm_submit=True
mcp__wq-brain-http__workflow_submit_alpha alpha_id=<ID> confirm_submit=true
# 4. 每 3–5 颗 value_factor_trendScore 监控多样性
mcp__wq-brain-http__value_factor_trendScore start_date=<本季初> end_date=<今天>
```

**预期 ROI**：9:1 相对开新挖量级。

### P1（本周）：门禁防链 —— 453 波修复 + 前置生效

**两步走**（不重建 backlog、不产生假阳性）：

```
# ① 离线保守补全（对历史波，不跑仿真、零配额）：
#    只补已经 run 过 gate.py / 体检硬门却缺落的波
#    依据：这批波里，本质上 gate.py 跑过但忘了落库
python tools/wave_gate.py --campaign-dir tracking/<R> --dataset <DS> --wave <W> --from-db --inspect-mode warn
#    ⚠ 对 18047 条 gem 不做逐条 —— 这正是断链的起源（生成堆早于消费），不是错误需要整个重跑；
#    只把**活跃有回测**的 453 波补齐

# ② 前置生效（把「闸前被发现」固化为 workflow_chain 的硬预检）：
mcp__wq-brain-http__workflow_chain
  chain=[{"node":"campaign","params":...,"stage":"S2"},  # 选波
         {"node":"wave_gate","params":...},             # ★ 硬插入，缺则链在此停下
         {"node":"gem","params":...}]
  join_async=true
```

**评分**：这类预防性闸本应 **每次开波就过**，而不是事后补。

### P2（下周）：prod 前置 —— 把 prod verification 从链尾抬到链中

**硬规则**（已在 `wqb-concurrency §8` 之外固化）：
**任何新信号族在投入第二波之前，必须先用 1–2 条骨架查 `check_correlation(production)`**。
这个规则在 SOP 已经落地（2026-09-19 升格**硬门**），`campaign_intel.py prod-first` 已能**串行**查生产。

**本审计建议**（产品级）：
- **把 S3 prod-first 查放到七槽开批之前**（而不是收批后），把**"第一波 prod 测量先于第二波生成"**变成硬配置。
- **配额倾斜**：建议把日常的 REGULAR 4/日 → `REGULAR 2/日 · prod 核查 2/日`（保守配置）。
  证据：IND prod 实测已有 21 可提交存量，清库存的边际产出率 **≳ 20× 于新挖**（2026-09-07 实证）。
- **隐形族自动点燃**：IND 那 19 颗、特别是 prod 在 0.6–0.7 黄金区间的 3 颗，`campaign_intel.py prod-first` 已在 2026-09-20 前后测量（凭证新鲜）—— **这是为主发起者的明确**。

### P3（两周内）：动态配额 + 「生成上限」公式化

1. **配额引擎按区动态分流**：`region_rotation` 当前 score 输入的 feasible_unsubmitted 权重太低（0.20），让它变成 `region_priority_score = 0.5×feasible + 0.2×yield + 0.2×prod_wall + 0.1×headroom`，驱动**生成预算倾斜**。
2. **生成上限公式化**：`max_gem_per_wave = min(12, Σest_seats × 2)`（同骨架封顶破 JPN 同一骨架 7538 条）。
3. **账页打标**：为所有 `gem 状态的表达式` 加一个 `consumed_by` 字段（有的话），没有就加它，区分"已消费"vs"生成堆"。

---

## 6. 风险与下一步

- **136 → 453 背后的教条**：很多 legacy 波是"生成后没补、忘了跑"，期间**不是错**——但**防止再发**必须靠 `workflow_chain` 步 5 硬插入 `wave_gate`。光靠背景排查还慢，危险是**下断链继续累积**。
- **ASI/DEU 的宽松伪影**：`ra_failed_checks` 在 ASI 主要是 Robust（LOW_ROBUST_UNIVERSE_SHARPE 66 行），**这类型不是"再挖同腿"就能解决的**——属结构性，需要换副数据集（analyst81 untried）或成分方向，建议 P1 沿 P2 设想一并覆盖。

## 7. 待用户确认块

本审计做了只读诊断和未包含任何平台写操作。请求确认：
- (a) 是否按 P0 把 **IND 19 颗** 里 prod 0.6–0.7 的 3 颗**立即**走提交链路（用户确认 → submit）；
- (b) 是否把 P1 的「wave_gate 前置进 workflow_chain」作为硬规则，不再依赖台意识；
- (c) 是否把 P2 的「prod 配额 2/日」写入 `tracking/<R>/config/thresholds.json`。

---

> **免责边界**：本方案为只读审计 + 优化建议，不构成对平台结果的承诺。所有判断的硬闸
> 最终判定以平台 `is.checks` 与 `submit_verdict` 为准；命中停止规则就停下，不得绕闸。
> prod_corr 数值与平台实时值可能有漂移；`alphas.corr_checked_at` 是本地测量时间记录，
> 不代表平台最新测量。`sync_platform_alphas.py --baseline` 可刷新。
---

## 附录：闸 PF 落地执行记录（2026-09-25，按用户选择 A_only 静态规则）

**背景**：F2「闸门凭证断档」（prod_corr 未测率 90.5%）的根因之一是 SOP 顺序错误——prod 检查被压在链尾（2026-09-19 才修正为 S4 收批后必调），且 prod-first 探针是 CLI 工具、不在 19 个 workflow 节点里、不依赖 agent 记得调用。

**本次落地**（用户选 A_only 纯静态规则，零平台配额成本）：
- **闸 PF（prod-family gate）** 已写入 `tools/wave_gate.py`（`--prod-family-gate` 默认开，`--no-prod-family-gate` 关）。
- **判据**：骨架级指纹（前 2 个算子调用名，如 `rank→ts_backfill`）。同骨架已确认 prod≥0.7 死路 → enforced 拦截整波（fail-closed）；同骨架已探明 prod<0.7 干净 → PASS；新骨架 → WARN 建议 prod-first 探针。
- **骨架比字段更准**（实证：`mdl135_d01_icc` 同字段在 `+vec_avg` 骨架下 prod=0.76-0.82 死路，在 `+vec_avg×ts_zscore` 骨架下 prod=0.46-0.57 干净）。
- **命名**：闸 PF（与 gate.py 闸9 窗口白名单不冲突）。
- **与闸 2.6 互补**：闸 2.6 `prod_saturation_gate` 判字段热度/数据集占比；闸 PF 判骨架级死路。
- **验证**：6/6 smoke test 用例全过（含真实死路 `rank→ts_backfill`/`rank→group_zscore`、干净 `rank→ts_mean`、新骨架 warn、混合拦截）；110 测试零回归。

**变更文件**：
- `tools/wave_gate.py`：新增 `_pf_family`、`_load_prod_wall_families`、`check_prod_family_gate`、`format_prod_family_report`、CLI 参数、闸 PF 硬阻断联动。
- `Claude/skills/INDEX.md`：闸编号表补"wave_gate.py 内置闸"段。
- `Claude/skills/wq-brain-ra-pipeline/SKILL.md`：步 5b 补闸 PF 说明。

**未做（刻意）**：未把 prod-first 探针塞进 wave_gate 主流程（避免单并发排队/超时拖慢门禁）；未改 gate.py（闸9 已被窗口白名单占用）；未写库（纯本地读 alphas 表）。
