# 步 1（S-PRE）细则：先读 profile → 库存盘点 → 查表 → 跨区死路 → 产出率

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 1。本文是它的细则；顺序即执行顺序。区域差异见 `regions/<REGION>.md`；论坛取证触发点见 [`forum-recon-triggers.md`](forum-recon-triggers.md)。

## 1.1 先读区域 profile（第一件事）

`Read references/regions/<REGION>.md`，按其 front-matter 与正文渲染本区专属 SOP（后续各步标注「profile」处按其覆盖执行）。
`entry_verdict` 三态的**默认含义**（profile 只写与默认不同的部分；词义见 [`GLOSSARY.md`](../../GLOSSARY.md) §2.3）：

| entry_verdict | 默认含义 | 步 1 的动作 |
|---|---|---|
| `active` | 常规九步 | 继续 |
| `probe-only` | 只允许探针批（单波探针上限见该区 profile），不开常规波 | 只走探针路径；按 profile 的探针规则进步 2 |
| `frozen` | 冻结 | **步 1 即拒**，不进步 2；唯一后门写在该区 profile 里，不得绕过 |

## 1.2 库存盘点（全流程最大分流点：先清库存，再开新挖）

依据：账户里已有大量已回测 IS alpha（快照口径见文末 as_of），其中一部分过 IS 硬闸；库存扫描的产出比新挖高一个数量级
（2026-09-07 实证：会话前半段跨四区 170 次新回测产出 0 条可提交 RA，后半段一次库存扫描产出 20 条）。

```
# 1) 枚举 + 资格门复算 + 写回过闸率先验（供步 4 GEM 消费）
python tools/build_gate_prior_from_inventory.py --regions all --emit-candidates cache/candidates.json --write-priors
# 2) 去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核
python tools/select_ra_basket.py cache/candidates.json --target 20 --out cache/basket.json
```

**分流判据（决策）**：

| 篮子状态 | 动作 |
|---|---|
| 篮子条数（只数 `prod_status=fresh_ok` 的已核条目，见下「prod 新鲜度」）≥ target **且**覆盖 ≥ 3 座**未点亮**塔 | 直接跳步 7 / 8（对篮子做稳健与提交判定），不开新挖 |
| 条数不足，或覆盖的未点亮塔 < 3 | 进步 2，**只补缺口塔** |

- **「篮子条数」的口径钉死（2026-10-01 事故教训）**：= `select_ra_basket` 四道处理**之后**的产物条数。
  **严禁用 `submit_ready` 队列行数代替**——该表是全生命周期台账（READY/DEAD/EXPIRED/SUBMITTED/SUPERSEDED），
  终态墓碑都留在里面；且 READY 行 ≠ 可提交（还要过本节约资格门复算与平台复核）。
  实证：KOR 队列 40 行里 READY=0、IND 132 行里 READY=0，按总数判断会得出「积压 40 应清库存」的反向错误结论。
- **分叉判定前先剔死（2026-10-01 落地，代码默认开启）**：`select_ra_basket` 内置
  `--exclude-dead`（**默认开启**，workflow `inventory_scan` 节点不传标志也会走到；调试才用
  `--no-exclude-dead`）：候选字段经 `fields` 表回填数据集，命中 `*_dead` ∪ `saturated_datasets`
  整集判死即剔除；族级死（dead_end 绑定）保留但计数告警；字段查不到归属 fail-open 保留。
  判据与 `wqb.profile_drift.dead_dataset_index` 同源。动机：「IS 过闸但所属集已撞 prod 墙判死」
  的候选若带进篮子，会烧完步 7 诊断链到步 8 才被挡。
- **prod 新鲜度（2026-10-03 落地，代码默认开启）**：`select_ra_basket` 只读 `alphas.prod_correlation` /
  `corr_checked_at`，给每条打 `prod_status`：`fresh_ok`（近 `--prod-max-age-days`（缺省 2）天内测过且 < 上限）/
  `fresh_blocked` / `stale_ok` / `stale_blocked` / `unmeasured`，并写进 `basket.json`（`prod_correlation` /
  `prod_checked_at` / `prod_age_days`）。库内记录 prod ≥ 上限的（`*_blocked`，不论新旧）直接剔除、不再送进限流的
  相关性队列（`--keep-prod-blocked` 仅调试）。**「库存足够 → 跳步 7 / 8」的条数只数 `fresh_ok`**；`stale_ok` /
  `unmeasured` 的值作废——实证 IND 旧候选 09-19~23 实测 prod 0.51–0.67，10-02 复测**全部** 0.83–0.99（社区同族
  alpha 持续进 book，只升不降），按旧值数篮子会把「库存足够」判错。要把 stale 的算进来，先对它们
  `check_correlation(refresh=True)` 重测（平台单并发、45 s ~ 12 min / 条，别一次排几十条），用
  `mcp__wqb-db__persist_correlation` 落库后再跑一遍本工具。`workflow_inventory_scan` 节点的返回里有
  `prod_checked_count`（= `fresh_ok` 条数）。

- 篮子敲定的口径 = **资格门 `Failed RA == 0`**（`wqb.config.compute_webdata_failed_counts`；比「无 FAIL」严格，WARNING / ERROR 也计），细节取自 `get_alpha_details(alpha_id).is.checks`。
  `submit_verdict` 对处女提交只会给 `UNVERIFIABLE`（`GET /submit` 恒 404），**不构成可提交依据**——见提交链 [`submit-chain.md`](../../worldquant-submit-alpha/references/submit-chain.md)。
- `compute_mutual_correlation`（本地算 PnL、不占平台相关性配额）**必须先**用它去同族冗余与 OS 撞车，再进限流队列。
- `cache/candidates.json`、`cache/basket.json` 是**可丢弃的中间文件**（不作事实源；战役产物只入 `data/wqb.db`，见主文「文件的分类」）。

## 1.3 查表（MCP，region 作用域）

```
mcp__wqb-db__get_campaign_summary  region=$REGION
mcp__wqb-db__get_dead_ends         region=$REGION
mcp__wqb-db__get_dead_datasets     region=$REGION
mcp__wqb-db__get_mining_yield                                    # 全区排名（选区/选集的最硬先验）
mcp__wqb-db__get_mining_yield      region=$REGION  by_dataset=true   # 本区按数据集拆
```

`reports/dataset_experience/<region>_<dataset>_campain.md`（`campain` 是既定文件名，非笔误）由 `brain-dataset-mining-experience` 维护：**仅在 region / delay / universe 与证据范围一致时继承**结论；
文件不存在则以上面的 DB 查表为准。（步 3 用其字段级失败边界选字段，步 4 的机制文档引用相关 wave / alpha 并说明新假设。）

## 1.4 跨区死路（必做；region 作用域查询会系统性漏掉别区已判死的集）

实证代价：KOR 选 risk70 做主攻集，跑完 114 条回测（best S = 0.87 / 0 near）才发现 `IND-RISK70-NO-SIGNAL` 与 `GLB-RISK70-STYLE-HF-MINVOL1M-FASTKILL` 早已存在——risk70 是跨三区独立复现的死族。

```
mcp__wqb-db__get_dead_ends                 # 不传 region = 全区死路清单；对每个候选数据集在结果里找 family / entry_id 命中
mcp__wqb-db__get_cross_region_lessons
python tools/campaign_intel.py s0-select --region $REGION --delay $DELAY --universe $UNIVERSE   # 输出带 [跨区弱:REG:maxS@bt] 标记
```

（不要再用 `LIKE '%ds%'` 直扫 sqlite：`model1` 会误命中 `model109`。）

| 情形 | 处置 |
|---|---|
| **跨区死族**：≥ 2 区**独立复现**的 dead_end | **排除**：不进白名单，不论本区评分多高 |
| **跨区弱**：同集在其它区 ≥ 16 条回测且 max\|S\| < 1.0（`s0-select` 的 `[跨区弱…]`） | **降权**：排在健康集之后、判死之前 |
| 某集仅在 1 区弱 | 降权，**不排除** |

**跨区横比另读 [`docs/experience/03_region_dataset.md`](docs/experience/03_region_dataset.md)**（12 区过闸率排序 + MEA / IND / DEU 停投结论）：profile 管「这个区怎么配」，03 管「这个区值不值得挖」，两者互补——后者拦的是「在某区死磕其实全区垫底」这类决策错误。

## 1.5 产出率读法（两个比率含义不同，别混）

| 比率 | 定义 | 低意味着 | 动作 |
|---|---|---|---|
| `conversion` | 已回测 / 已生成 | **流水线**问题（S2→S3 断链，生成远超回测吞吐） | 修管道、先清积压（`conversion < 10%` 的区先清积压再开新波），别换区 |
| `yield_rate` | 达标 / 已回测 | **标的**问题（该区/集本身不出货） | 换区 / 换集，别加生成量 |

- **严格口径**（默认 `strict=true`）：达标 = sharpe / fitness 过线 **且 `ra_failed_checks` 为空**（= `ra_clean`，词义见 GLOSSARY）；另给 `prod_clean` / `prod_blocked` / `prod_wall_ratio`。`yield_rate_loose` 是旧口径对照（IND 旧口径 34% 而严格口径 12.6%，其中已测 prod 的 86% 撞墙——选区先验曾被系统性高估）。
- **累计**产出率为 0 且已测 ≥ 100 的区，不要再投槽位（100 是样本量下限，对应停止规则 A 的 `yield_min_backtests`，见 [`loop-and-stop.md`](loop-and-stop.md)）。
- 数字快照（as_of 2026-09-06，**loose 口径，仅作历史对照**）：IND 35.7% / MEA 19.9% / KOR 4.2% / EUR 2.0% / USA 1.4% / GBR 0%（180 条回测零达标）。当前值查 `get_mining_yield`，不要抄这行。
- 详细口径见 [`wq-brain-campaign-matrix`](../../wq-brain-campaign-matrix/SKILL.md)。

## 1.6 PPA 主题门禁（仅当本战役含 PPA 分支）

1. `mcp__wq-brain-http__get_messages(limit=30)`，扫 `type == "ANNOUNCEMENT"` 且标题含 "Power Pool" 的公告。
2. 解析当期主题：region / delay / universe / 中性化集合 / 禁止数据集 / 有效时间。
3. **PPA 提交必须精确匹配主题**；不在当期主题的达标候选由 agent 手工标 `YELLOW + WAIT_THEME_ROTATION`（**没有代码实现**，记入本波 `key_findings`；它与提交期的 web UI 主题窗口核对是两道不同的门，后者见 [`ppa-handoff.md`](../../worldquant-submit-alpha/references/ppa-handoff.md)）。RA 常规提交不受主题限制。
4. **每次 S-PRE 实时重扫，禁止复用 settings 快照**（实证：GLB/D1 Liquid Aug'26 主题到期后 settings `_ppa_theme` 仍写「匹配，可继续」）；新主题的准入条件会变，读公告原文。

## 1.7 产物与失败分支

- **产物**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号——**落 `settings.json`，并在步 2 写 ledger `s0_ranking` / `s0_whitelist`**（键契约见 `docs/ledger_keys.json`）。
- **失败分支**：registry 全空 = 新区域 → 进步 2，并在步 9 写 campaign；`get_dead_datasets` 已覆盖全部候选 → 停止，转 `wq-brain-campaign-matrix` 选区（`brain-next-move-analysis` 只提供日报输入，不产出配置）；库存足够 → 跳步 7 / 8（见 1.2）。

> as_of 2026-09-29：本文不含会漂移的库存绝对数；要数字请现查（`get_mining_yield` / `build_gate_prior_from_inventory.py` 的汇总输出）。
