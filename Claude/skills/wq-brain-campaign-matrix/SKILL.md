---
last_verified: 2026-08-22
name: wq-brain-campaign-matrix
description: "WorldQuant BRAIN alpha 挖掘的\"区域×数据集\"战役矩阵。当用户要在某区域挖 alpha / 开战役 / campaign / 查区域配置 / 看哪些数据集还没挖 / 走 region×dataset 效率工作流， 或任何新挖掘战役开始时（S0 之前）使用。把区域静态配置（合法 universe 档位、默认 neutralization、EVENT 字段规则）、数据集资产（清单 + PPA 预筛）与实证台账 （dead-ends / wins / campaign 状态）解析为预解析配置包，原样派发 S0–S6 skill 链 并把结果回写 registry。"
layer: L-PRE
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`）。

# 区域×数据集 战役矩阵（Campaign Matrix）

## 定位（一句话）

七阶段流水线（S0–S6）**之前的查表层**：输入 `region + 意图`，输出**预解析配置包**，让后续 skill 拿现成参数执行；战役结束后把实证结论**回写** registry。本 skill 只做查表与回写，**不执行任何挖掘动作**——执行仍由现有 25 个其他 skill 完成，零改动、零第二实现。

## 衔接协议

- **上游**：`wq-brain-ra-pipeline`（S-PRE 查表决策）或用户直给 `region + 意图`（REGULAR 挖矿 / SA 组合 / PPA / 复盘）。
- **数据通道（单轨 DB）**：读全走 `mcp__wqb-db__*`（`get_region_config` / `get_dead_ends` / `get_campaigns` / `get_cross_region_lessons`）；回写走 `campaign.py registry` 幂等 CLI 或会话内 `mcp__wqb-db__upsert_registry_empirical`，禁止散装 SQL。
- **输出**：预解析配置包（region/universe/delay/中性化/候选数据集等**参数**，非落盘产物；下游以参数注入，不产生中间文件）。**配置包必须包含 PROD 饱和风险标注（2026-08-23 新增，强制）**：查询 `mcp__wqb-db__get_dead_ends(region)` 中 PROD_CORRELATION 类死路，若候选数据集/信号族与已知饱和族重叠，标注 `prod_risk: high` 并附具体死路条目；同时查询 `mcp__wqb-db__search_alphas_by_sharpe(region, min_sharpe=1.58)` 获取该区域已达标 alpha 数量，≥10 且风格同质则标注 `prod_saturation: likely`。此标注供 S2 生成表达式时参考——若信号族 PROD 风险高，优先选择正交方向而非同族变体。
- **下游**：S0 健康检查（`wq-brain-ppa-mining` §1.0 硬门槛方法论 + `wq-brain-campaign-toolkit` `score_datasets.py` 执行；配置包映射为 `--campaign-dir` 与 settings/thresholds）；S6→S-PRE 闭环另一端——`wq-backtest-monitor` §14 回写 registry_empirical 后本 skill 查表自动读取最新 dead_ends/wins/campaigns。

## 数据文件（唯一 registry，单轨 SQLite）

**数据库**：`D:\coding\traeCN_project\wqb\data\wqb.db`

| 表 | 内容 |
|---|---|
| `regions` | 区域静态配置（universe 档位 / 默认 neutralization / EVENT 字段规则） |
| `datasets` | 数据集资产（清单 + 类别分布 + 高倍率集 + PPA 预筛） |
| `registry_empirical` | 实证层（`dead_end` / `win` / `orphan` / `campaign` 四层，按区域） |
| `cross_region_lessons` | 跨区域铁律（GLB emotion 死路、anl15 精确表达式封禁、非法 universe 档） |

> 2026-08-21 起**单轨数据库模式**：历史 JSON（`campaign_registry.json` + `registry/` 拆分目录）已归档到 `attic/json_archive/registry/`（只读，禁止再编辑），唯一事实源为 SQLite。**读**：`mcp__wqb-db__*` 查询工具（只读）或 `SELECT * FROM registry_empirical WHERE region=? AND layer=?`；**写**：一律走 toolkit `campaign.py registry` 幂等 CLI（见 §4 命令模板；INSERT OR REPLACE + 必填字段校验 + 自动补 dead_at/date，单事务），**禁止散装 SQL 直改**。`tools/migrate_phase2.py` 仅为历史 JSON→DB 一次性迁移工具，日常回写不经过它。

三层结构（`registry_empirical.payload` JSON 内部）：

| 层 | 键 | 内容 | 消灭的重复成本 |
|---|---|---|---|
| 静态层 | `static` | 合法 universe 档位、默认 neutralization 及实证 notes、EVENT 字段规则 | TOP1500 非法档、CHN 默认档返空类试错 |
| 资产层 | `assets` | 数据集清单 + 类别分布 + 高倍率集 + PPA 预筛说明 | 每次重拉 mcp__wq-brain-http__get_datasets、重排白空间 |
| 实证层 | `empirical` | `wins` / `dead_ends`(含 rule) / `campaigns`(status: untried/in_progress/exhausted) / `orphans` | 死路族重挖（GLB emotion、KOR value/quality）、跨会话进度丢失 |

## 工作流（五步）

### 1. 解析输入
用户给 `region`（必须）+ 意图（REGULAR 挖矿 / SA 组合 / PPA / 复盘）。意图缺省时读 `registry_empirical` 的 campaign 层（layer='campaign'）找 `untried`/`in_progress` 最高优先级项建议给用户。

**查表工具（wqb-db-mcp）**：
```
# 查区域配置
mcp__wqb-db__get_region_config(region="MEA")

# 查死路清单
mcp__wqb-db__get_dead_ends(region="MEA")

# 查战役清单（按状态过滤）
mcp__wqb-db__get_campaigns(region="MEA", status="in_progress")

# 查跨区铁律
mcp__wqb-db__get_cross_region_lessons()
```

### 2. 查表生成配置包
从 registry 读出并组装为一份配置包（直接贴给用户/后续 skill）：

```
region=KOR  universe=TOP600  delay=1  neutralization=STATISTICAL(或数据集 dominant)
排除：dead_ends 中命中的信号族（引用 rule）
候选数据集：campaigns 中 status=untried 的集（SA 意图优先 news/sentiment/insiders/shortinterest 非同质族）
注意：EVENT 字段禁 winsorize → ts_event_* 或裸 rank
```

配置包**不替代** `wq-brain-ppa-mining §1.0` 的实时体检（cov≥0.85/alphaCount≤50/fields≥10）——矩阵存的是快照结论，PPA 候选集仍须逐集过体检。

### 3. 派发（不改下游）
按 `wq-brain-ra-pipeline` 九步 SOP 把配置包交给 MCP 化链：步 2 S0 体检（`mcp__wq-brain-http__workflow_campaign` stage="S0"）→ 步 3 S1 字段扫描（`workflow_campaign` stage="S1" + `workflow_feature_engineering`）→ 步 4 S2 选波（`workflow_gem` + `workflow_campaign` stage="S2"）→ 步 5 门禁（`workflow_campaign` stage="S2" + `preflight_expressions`）→ 步 6 S3 七槽回测（`workflow_batch_track`）→ 步 7 S4 诊断（`workflow_campaign` stage="S4"）→ 步 8 提交判定（`submit_verdict` + 用户确认后 `workflow_submit_alpha`）→ 步 9 S6 复盘回写（`upsert_wave_result` / `upsert_registry_empirical`）。

### 4. 回写（强制，战役结束或关键发现时）
写 `data/wqb.db` 的 `registry_empirical` 表（**禁止再编辑 `attic/json_archive/registry/` 归档 JSON**），**一律走 toolkit `campaign.py registry` 幂等 CLI**（`C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts\campaign.py`，相对工作区根可写 `tracking/<REGION>` 战役目录）。命令模板（**先 `--dry-run` 试跑，无误后去掉重跑**；INSERT OR REPLACE 幂等，重复跑无副作用）：

```bash
# 新死路 → layer=dead_end（payload 含 reason 带数据 / rule 下次怎么办 / dead_at 自动补当天 / salvage）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> registry add-dead-end \
    --id MEA-PV106-SPREAD-DEAD --family "pv106 spread" \
    --reason "<带数据理由>" --rule "<下次怎么办>" --salvage "<可抢救方向>" --dry-run

# 胜绩 → layer=win（key = 可复用配方）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> registry add-win \
    --id <ID> --what "<做了什么>" --key "<可复用配方>" --date 2026-08-21

# 数据集进度 → layer=campaign（status 三值迁移 untried→in_progress→exhausted + note 一句话）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> registry upsert-campaign \
    --dataset <ds> --status exhausted --note "<一句话>"

# 403 拒后的 UNSUBMITTED 孤儿 → layer=orphan（勿提交，等 web 控制台手动清理）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> registry add-orphan --ids a1,a2,a3

# 写后立即验证（同一入口，无需另写查询脚本）
$WQ_PY campaign.py --campaign-dir tracking/<REGION> registry get --layer dead_end --id MEA-PV106-SPREAD-DEAD
```

说明：`--region` 默认取战役区域无需传；**必填字段（--id/--family/--reason/--rule 等）必须在命令行显式给**（argparse 强制，防 @file 遗漏导致 payload 缺字段）；`--extra @file.json` 用于补充可选字段（如 salvage/dead_at/自定义扩展字段），走 UTF-8 文件通道防 PowerShell 引号转义（中文安全）；命名参数与 @file 同键时命令行优先。

回写要求与回测 checkpoint 同级纪律：**只记有跨会话价值的结论，不记过程性噪声**。

### 5. 扩区
需要新开区域（EUR/ASI/GLB/CHN）时：从 `fresh_datasets_7region.json` 复制该区 summary 到 assets 层，static 层用 `mcp__wq-brain-http__get_platform_setting_options` 实测合法档位（**禁止照抄 USA 档位**），empirical 层初始化为空 + 该区已知死路。

## 硬规则

1. **registry 是唯一事实源**：记忆/分析报告中的区域结论若与 registry 冲突，以更新 registry 为准，不允许两边各自演化。
2. **死路 rule 优先于用户直觉**：命中 `dead_ends` 的族要在配置包里显式排除并引用 rule 出处（如 KOR-VALUE-QUALITY-SEEDS），即使用户点名也要先提示实证依据。
3. **静态层档位不外推**：某区域合法 universe 档只对该区域有效；JPN 不是合法区域。
4. **幂等写**：registry 写库一律走 `campaign.py registry` 幂等 CLI（INSERT OR REPLACE + 必填字段校验 + 单事务，UNIQUE(region, layer, entry_id) 保证可重复跑），禁止散装 SQL 直改与改归档 JSON。

## registry 与战役台账的边界

- **registry（本 skill）= 跨会话结论**：`registry_empirical` 表的 dead_ends / wins / campaigns 状态 / orphans。**逐波 verdict、submit_ready、near_pool、diversity_history 进战役台账（`ledger_kv` 表，`wq-brain-campaign-toolkit` 的 LedgerStore SQLite 后端），不进 registry**。
- registry schema 约定：`dead_ends[]` 每条含 `dead_at`/`salvage`；region 级可增 `poison_patterns[]`（**仅区域特有**；平台级见 toolkit `config/platform_constraints.json`，引用不复制）与 `submit_ready[]`（达标缓冲池镜像）。
- 台账写回一律走 toolkit `campaign.py ledger` 幂等 mutation（原子写 + 双遍重放），**禁止 record_*.py 式直改**（已淘汰）；registry 写回一律走 `campaign.py registry`（§4 模板），**禁止散装 SQL**。战役结束后由本 skill 的 §4 回写流程把判死结论提炼进 `registry_empirical`（带 rule + dead_at + salvage）。

### S6→S-PRE 闭环（自动反哺）

**S6 负责回写，本 skill 负责读取**：S6 `wq-backtest-monitor` §14 每次复盘后把波级结果写入 `wave_results`（战役台账）、把 dead-end/win 提炼进 `registry_empirical`（均走 toolkit 幂等 CLI）；本 skill（S-PRE）下次查表即自动读到最新 `dead_ends` / `wins` / `campaigns` 状态，无需人工同步——S6 回写与 S-PRE 查表由此闭环，未回写的复盘视为未完成。
