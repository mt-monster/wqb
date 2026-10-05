---
last_verified: 2026-09-29
name: wq-brain-campaign-matrix
description: "区域已定、要看这个区有哪些数据集 / 哪些信号族已判死 / 战役挖到哪一步时使用：把 region + 意图查成预解析配置包，并提供 registry 回写的 schema 与命令模板。整链挖掘走 wq-brain-ra-pipeline；选区（哪个区好）走 brain-next-move-analysis。"
layer: L-PRE
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__get_region_config
  - mcp__wqb-db__get_dead_ends
  - mcp__wqb-db__get_campaigns
  - mcp__wqb-db__get_cross_region_lessons
---

# 区域×数据集 战役矩阵（Campaign Matrix）

## 职责边界

- **本 skill 负责**：①给定 region（+ 意图）查 registry，输出**预解析配置包**（参数，不落盘）；②**拥有 registry 的 schema 与写入规范**（layer 表、必填字段、ID 命名、幂等 CLI 模板）。
- **本 skill 不做**：不执行任何挖掘动作；**不选区**（`region` 是入口参数——缺了就回问用户，或转 `brain-next-move-analysis` / `python tools/region_status.py --rotate`）；不决定「何时回写、写什么」（触发时机与调用序列 = RA 步 9，那里持有写入工具）；不替代 S0 体检；不编排九步——用户已给区域与数据集就不必先来这里，整链走 `wq-brain-ra-pipeline`。
- **上游 / 下游**：上游 = ra-pipeline 的 S-PRE 步或用户直给 `region + 意图`；下游 = 配置包交还 ra-pipeline 步 2（S0 体检）；另一端 = RA 步 9 回写后，本 skill 下一次查表即读到。

## 存储地图（唯一一张；「层」一词只指 `registry_empirical.layer` 列）

| 概念 | 存放 | 读 | 写 |
|---|---|---|---|
| 区域静态配置（合法 universe / delay 档位、默认中性化） | `regions` 表（`universe_legal` / `delay_legal` / `neutralization_default`）；**权威清单是 `src/wqb/config.py::REGIONS`** | `get_region_config` | 表行在该区首次入库时由 `CampaignStore` 自动建；档位内容以 `get_platform_setting_options` 实测为准并写进 `config.REGIONS`，**不外推别区档位** |
| 数据集资产（类别 / 字段数 / 覆盖 / 拥挤度 / tier） | `datasets` 表（`catalog_json` 为 typed catalog） | 字段级 `mcp__wqb-db__get_field_catalog`；数据集清单以平台 `mcp__wq-brain-http__get_datasets` 为准（本地表是缓存） | `tools/discover_datasets.py` / `tools/fetch_dataset_assets.py`（直连入库）；字段级由 toolkit `scan_fields.py` |
| 死路（dead_end） | `registry_empirical` · `layer='dead_end'` | `get_dead_ends` | RA 步 9 §9.5（`seal_dead_end`）或 CLI `add-dead-end` |
| 胜绩（win） | `registry_empirical` · `layer='win'` | assemble-priors / SQL | RA 步 9 §9.6 或 CLI `add-win` |
| 数据集战役进度 | `registry_empirical` · `layer='campaign'`（`status` ∈ untried / in_progress / exhausted） | `get_campaigns` | CLI `upsert-campaign` |
| 403 后的孤儿 alpha | `registry_empirical` · `layer='orphan'` | SQL | CLI `add-orphan` |
| 跨区铁律 | `registry_empirical` · `layer='cross_region'`（旧表 `cross_region_lessons` **已废弃**，数据已迁入） | `get_cross_region_lessons` | 无写入规范（迁入数据，勿新写） |
| 逐波结论 / 战役台账 / 提交队列 | `wave_results` / `ledger_kv` / SQL 表 `submit_ready` | 见 toolkit `references/ledger-schema.md` | **不进 registry**（`registry` = 跨会话结论；逐波细节属战役台账） |

`registry_empirical` 与 `region_kb`（ledger 键）**没有谁派生谁**：assemble-priors 把二者**并列合并**成 GEM 的 priors（registry 的 win / dead_end 层 + `region_kb` 的论坛模板 / 配方 / 死路模式 / 过闸率先验，见 RA [`assemble-priors-internals.md`](../wq-brain-ra-pipeline/references/assemble-priors-internals.md)）。S6 只写 registry；`region_kb` 的 `recent_waves` / `gate_priors_local` 由 `pipeline.py --review` 自动刷新，其余数组靠人工维护。**回写后必须再跑一次 assemble-priors**，先验才会更新。

## 工作流

### 1. 解析输入并查表

- `region`（**必须**）+ 意图（`regular` 挖矿 / `sa` 组合 / `ppa` / `review` 复盘）。缺 `region` → 回问用户；用户只说「挖点什么」→ 转 `brain-next-move-analysis`（日报 / 金字塔态势）或 `python tools/region_status.py --regions <R1,R2> --json` 比较后让用户定。缺意图 → 默认 `regular`，并读 campaign 层里 `status ∈ {untried, in_progress}` 的数据集作候选（campaign 层没有优先级字段，不要编排序）。
- 区域覆盖（哪些区有 profile / 战役目录、`entry_verdict`）只看 [INDEX §区域清单](../INDEX.md)——**`entry_verdict=frozen` 的区直接拒绝**，不出配置包。

| 调用 | 返回 | 空结果的含义 |
|---|---|---|
| `mcp__wqb-db__get_region_config(region)` | `regions` 行（`universe_legal` / `delay_legal` / `neutralization_default`） | `{"error": "region not found"}` = 该区还没入过库：不是「没有配置」，先按 INDEX 的开新区检查表补齐 |
| `mcp__wqb-db__get_dead_ends(region)` | `dead_end` 层条目（`payload` 含 `family` / `reason` / `rule` / `dead_at`） | `[]` = 没登记过死路（不等于没有死路，见 profile 与 `region_kb.dead_patterns`） |
| `mcp__wqb-db__get_campaigns(region, status)` | `campaign` 层条目（`payload.dataset` / `status` / `note`） | `[]` = 没登记过数据集进度，候选集须从 S0 排名而来 |
| `mcp__wqb-db__get_cross_region_lessons()` | `cross_region` 层铁律（GLB emotion 死路、非法 universe 档等） | — |

### 2. 组装配置包

配置包是**参数**（贴给用户或注入下游），不产生文件。字段与来源：

| 字段 | 来源 / 口径 |
|---|---|
| `region` / `mode` / `entry_verdict` | 入口参数；`entry_verdict` 取 profile（INDEX 区域清单） |
| `universe` / `delay` | `get_region_config`，须落在 `universe_legal` / `delay_legal` 内；profile 的 `settings_proven` 优先 |
| `neutralization` | profile `settings_proven` 优先，否则 `neutralization_default`（无「数据集 dominant」一说——设置调优是步 6 的 `--set` / `--neutralization` 实验，不在这里定） |
| `excluded_families[]` | `dead_ends` 里命中候选的族，每条带 `id` + **原样引用 `rule`** |
| `candidate_datasets[]` | campaign 层 `untried` / `in_progress` 的集。**是待 S0 筛选的超集，不是白名单**：已点亮塔的剔除、win 族与跨区弱先验的并入、体检硬门，全由 S0（RA 步 2）执行，本 skill 不重复实现 |
| `prod_risk` | `high`：候选数据集 / 信号族与某条 `dead_end`（`reason` 含 PROD_CORRELATION 类墙）重叠，并附该条 `id`；否则 `none` |
| `prod_saturation` | `likely`：`tools/region_status.py --regions <R> --json` 的 `pass_ge_158 ≥ 10`；`no`：< 10；`unknown`：该区没有回测记录。**口径只此一处**（next-move §5.5 同源，勿另写第三份实现）。这两个标注只作 S2 的方向提示（信号族 PROD 风险高时优先正交方向）；撞墙后怎么处置只看 RA 决策表 [D0-P](../wq-brain-ra-pipeline/references/decision-table.md) |

> **⚠ 选集铁律（2026-10-02 实证，开波前必读）**
> 1. **硬地板是区域动态的**：逐区配在 `tracking/<R>/config/thresholds.json::dataset_health`（`coverage_hard_min` / `field_count_hard_min` / `alpha_count_max` / `tier1_score_pct`），另有 `src/wqb/config.py` 的**全局绝对底**。实测差异：USA `0.65/5/50/P80`、GBR `0.65/10/1000`、EUR `0.6/10/1500`、DEU/IND/KOR `0.5/5/1500`。**禁止凭记忆跨区套用，禁止把某个区的 whitelist note 当通用口径。**
> 2. **硬地板 ≠ S0**：真 S0（`score_datasets.py`）是 6 道叠加 = 硬地板 + `assign_quantile_tiers`（tier1≥本区 **P60** / tier2≥**P30**，区域自适应）+ `crowd_band` 保底 + `category_weight` + `empirical_prior` + `saturation_demotion`。**禁止手写几行 filter 冒充 S0**（读本地 `datasets` 缓存更差——是过期快照）。**唯一权威 = 跑 `score_datasets.py --campaign-dir tracking/<R>`，读它写的 ledger `s0_ranking`**（含 `tier` / `score` / `pyramid_view`）。反例（真实踩坑）：手写 `cov≥0.6 & ac≤1500 & flds≥10` 选出 4 个目标，权威 S0 一跑 3 个是 `excluded`，3 个 GEM 白跑。
> 3. **白名单 = 三重交集**：`S0 tier1/tier2` ∩ **非 registry dead_end** ∩ **本区未测**（`backtest_results` 零行）。⚠ **S0 榜只剔 `_dead` ledger 键**（EUR 仅 4 个），**不读 registry 的 `dead_end` 层**（EUR 137 条）⇒ 只信 S0 榜会把区域级判死族当候选（EUR 的 news17/20/31/48、model354、analyst_earnings_ibes 在 S0 里是 tier1 alive）。
> 4. **TRI 闸（`s1_triage_<region>`）与 S0 是两道独立闸**，会互相否决（S0 tier 却 TRI `block` / TRI ★ 却 S0 `excluded`）——**落地前两闸都要过**。跨区"未测"最容易被误当"机会"，用本三重交集过一遍再开 GEM。

完整样例（KOR / regular；数据集名与条目为**格式示意**，真值以查表为准）：

```
region=KOR  mode=regular  entry_verdict=active
universe=TOP600  delay=1  neutralization=STATISTICAL          # get_region_config 的合法档内；profile settings_proven 优先
excluded_families:
  - {id: KOR-VALUE-QUALITY-SEEDS, rule: "<原样引用 registry 的 rule>"}
candidate_datasets:                                            # 超集，交 S0 体检
  - {dataset: model219, status: untried}
  - {dataset: news12,   status: in_progress}
prod_risk=none  prod_saturation=unknown                         # region_status 无回测记录时为 unknown
```

配置包**不替代** S0 体检：矩阵存的是快照结论，体检方法按模式分——RA 走 RA 决策表 D4 / 步 2，PPA 走 `wq-brain-ppa-mining` §1.0；配置包写明 `mode` 供下游选。

### 3. 交还，不派发

配置包做完就交还 `wq-brain-ra-pipeline` 步 2。**本 skill 不重复九步派发链**（旧版复制的那条链已与 ra-pipeline 不同步，两处维护必漂移）。

### 4. 回写规范（本 skill 拥有 schema；何时写、写什么归 RA 步 9）

**一张表、两个入口、一份校验**（`src/wqb/registry_contract.py`）：MCP 可用时用 RA 步 9 的调用（`seal_dead_end` / `upsert_registry_empirical`）；无 MCP 或批量回写时用带校验的 CLI。**不要两边各写一遍。**

| layer | 必填 | 常用可选 | `entry_id` 命名 |
|---|---|---|---|
| `dead_end` | `id` `family` `reason`（带数据）`rule`（下次怎么办） | `salvage` `dead_at`（缺省补当天）`forum_recon` | `<REGION>-<数据集或族>-<症状>-DEAD`，全大写连字符，区域内唯一（`KOR-WAVE99-XXX-DEAD`） |
| `win` | `id` `what`（信号概念）`key`（设置与骨架，**不记混合比例**） | `date` `evidence` | `<REGION>-<族>-WIN` |
| `campaign` | `dataset` `status` | `note`（一句话） | = 数据集名 |
| `orphan` | `id`（alpha_id） | — | = alpha_id |

CLI 模板（PowerShell 续行用反引号；**先 `--dry-run` 校验，无误后去掉重跑**，幂等）：

```powershell
& $WQ_PY "$WQ_TOOLKIT_DIR/campaign.py" --campaign-dir tracking/<REGION> registry add-dead-end `
    --id <REGION>-<DS>-<症状>-DEAD --family "<族>" --reason "<带数据理由>" --rule "<下次怎么办>" --dry-run
& $WQ_PY "$WQ_TOOLKIT_DIR/campaign.py" --campaign-dir tracking/<REGION> registry add-win `
    --id <ID> --what "<信号概念>" --key "<设置与骨架>"
& $WQ_PY "$WQ_TOOLKIT_DIR/campaign.py" --campaign-dir tracking/<REGION> registry upsert-campaign `
    --dataset <ds> --status exhausted --note "<一句话>"
& $WQ_PY "$WQ_TOOLKIT_DIR/campaign.py" --campaign-dir tracking/<REGION> registry get --layer dead_end --id <ID>   # 写后立即验证
```

- 必填项必须在命令行显式给（argparse 强制）；`--extra @file.json` 补可选字段（UTF-8 文件通道，中文安全），命名参数与 `@file` 同键时命令行优先。
- **只记有跨会话价值的结论。** 正例：带 `rule` 的 dead_end、可复用的 win 配方、数据集 `exhausted`。反例：单波 FAIL、单条 alpha 没过闸、参数扫描结果（这些进 `wave_results` / 台账）。
- 不编辑 `attic/json_archive/` 里的历史 JSON（registry 已是 SQLite 单轨，那些文件已删除）。

### 5. 扩区

开新区的检查表只在 [INDEX §开新区检查表](../INDEX.md) 维护（落点：`config.REGIONS`、`tracking/<R>/config/`、RA profile、INDEX 区域清单，及各自的验证命令）。本 skill 只负责其中「区域静态配置」一项：档位**实测**（`mcp__wq-brain-http__get_platform_setting_options`），**禁止照抄 USA 档位**。

## 硬规则

1. **registry 与别处结论冲突时以 registry 为准**，并在发现处修正来源文档；不允许两边各自演化。
2. **死路 `rule` 要显式排除并引用出处**（如 KOR-VALUE-QUALITY-SEEDS）。用户点名要挖时：**先提示一次实证依据**；用户坚持则执行，并在该波 `key_findings` 记「用户覆盖 <dead_end id>」（与 RA 一致：用户显式指令 > 决策表，但依据必须让用户看见）。
3. **静态档位不外推**：某区的合法 universe 只对该区有效；区域集合以 `config.REGIONS` 为准，覆盖情况看 INDEX。**禁止凭记忆断言某区「非法」或「未启用」**——回代码常量与 INDEX 核对。
4. **直改 registry 一律走上面两个入口**（含校验）；散装 SQL 只读。

## 常见失败与处置

| 现象 | 含义 | 处置 |
|---|---|---|
| `get_region_config` 回 `region not found` | 该区从未入库；或 `region` 拼错 / 不在 `config.REGIONS` | 核对 INDEX 区域清单；确属新区 → 走开新区检查表；不要自造档位 |
| 缺 `region` | `region` 是入口参数，本 skill 不选区 | 回问用户，或转 next-move / `region_status --rotate` |
| 该区 `entry_verdict=frozen` | 步 1 即拒 | 不出配置包；后门见 RA `references/scenarios.md` 情景 RA-08 |
| registry 与 profile 结论冲突 | 事实层与文档层不一致 | 以 registry 为准，修 profile；两边都缺证据则标 `unknown` 并让 S0 实测 |
| 回写被拒：`缺必填字段: ['rule']` | 契约要求 dead_end 带 `rule` | 补上「下次怎么办」；MCP 与 CLI 是同一份校验，换入口没用 |
| MCP 写入返回 `entry_id 与 payload.id 不一致` | 传参写错了 | 两处写成同一个 ID（campaign 层是数据集名） |
| `prod_saturation=unknown` | 该区没有回测记录 | 不是「无饱和」，交 S0 / 首探去测 |

## 情景卡

### 情景 MX-1　「在 KOR 挖点 regular」的查表

- **前置状态**：用户给了 `region=KOR`，没给数据集。
- **步骤**：① 看 INDEX：`entry_verdict=active` → 继续；② `get_region_config("KOR")` 取档位；③ `get_dead_ends("KOR")` 取命中的族与 `rule`；④ `get_campaigns("KOR", status="untried")` 取候选；⑤ `region_status.py --regions KOR --json` 取 `pass_ge_158` 填 `prod_saturation`；⑥ 组装配置包，交 RA 步 2。
- **分支**：`frozen` → 拒绝；`get_campaigns` 空 → 候选交给 S0 排名，不自己编。
- **完成定义**：配置包含上表全部字段，`excluded_families` 每条带 `rule`，且明确写「候选是超集」。
- **反例**：把 `untried` 当白名单直接开波（绕过 S0 的点亮塔 / 体检约束）；配置包里省掉 `prod_risk`。

### 情景 MX-2　用户点名要挖已判死的族

- **前置状态**：用户说「就挖 `<族>`」，而 `get_dead_ends` 命中 `KOR-...-DEAD`。
- **步骤**：① 原样告诉用户该条的 `reason` 与 `rule`（一次）；② 用户坚持 → 执行；③ 该波 `key_findings` 记「用户覆盖 KOR-...-DEAD」；④ 波后按结果决定是否更新该条 `rule`。
- **完成定义**：用户看过依据，覆盖被记录。
- **反例**：静默照办，或静默拒绝。

### 情景 MX-3　波后回写一条新死路

- **前置状态**：某族在 3 波内全部撞 prod 墙，RA 步 9 已判死。
- **步骤**：① 先 `--dry-run` 校验：`registry add-dead-end --id KOR-XXX-PRODWALL-DEAD --family "<族>" --reason "<带数据>" --rule "<下次怎么办>" --dry-run`；② 去掉 `--dry-run` 落库（或走 RA 步 9 的 MCP 调用）；③ `registry get --layer dead_end --id …` 验证；④ 再跑一次 assemble-priors。
- **完成定义**：`get` 能读回，且 `priors_snapshot_<region>` 不早于本次回写。
- **反例**：只写 `reason` 不写 `rule`（配置包无从引用）；写完不刷新 priors。
