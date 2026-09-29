# 数据集评分 + 探针三灯评分（`score_datasets.py`）

> 数字只写**代码缺省**（`score_datasets.py` 与 `src/wqb/config.py::DATASET_HEALTH_SCORING`）；区域的 `thresholds.json` 可覆盖，覆盖值以区域文件为准。文档与代码不一致时**以代码为准并修文档**——旧版这里写的 P80 / P55 与 `coverage_hard_min` 0.65 是代码里从未有过的值。

## 一、数据集评分（`score_datasets.py` 缺省模式）

```
score = ( 0.40·coverage + crowd_penalty(alphaCount) + 0.20·min(log1p(usableFields)/log1p(1000), 1)
          + 0.10·min(valueScore,10)/10 + empirical_prior ) × category_weight
crowd_penalty：ac ≤ 50 → 0.30；50→500 线性降至 0.15；500→5000 线性降至 0.02；> 5000 恒 0.02（分段罚）
valueScore 缺失按中性 0.5；empirical_prior 缺省 0（经验强度先验，见 SKILL §8）
```

（旧式 `0.30/(1+log10(1+ac))` 已废：对 `ac > 1e4` 仅降 0.25 分，被 `0.4·cov` 淹没，USA 实测 analyst15 `ac=102072` 靠 `cov≈1` 进了 tier1。）

**tier 规则**（`thresholds.dataset_health`）：

- **硬地板**（与模式无关）：`coverage < coverage_hard_min`（**缺省 0.7**）或 `usableFields < field_count_hard_min`（缺省 5）→ `excluded`。个别区域覆盖了更低的值（如 AMR 的 0.5），以区域文件为准。
- `mode=general`：`alphaCount` 只进 score 软罚，无硬闸；`mode=ppa`：`alphaCount ≤ alpha_count_max`（缺省 50）硬闸（tier1 超标降 tier2）。
- `tier_method=quantile`（缺省）：非硬排除者按 score 在**本区域数据集分布内**分位分带——**tier1 ≥ P60（`tier1_score_pct` 缺省 0.6）、tier2 ≥ P30（`tier2_score_pct` 缺省 0.3）**，分位在本区域内计算，天然区域自适应；`threshold` = 固定阈值回退。
- **保底带**（`tier_note` 溯源，只升不降）：`backfill_band`（0.65 ≤ cov < 0.85 且 ac ≤ 50 且 valueScore ≥ 6）→ tier2；`probe_exception`（cov ≥ 0.9 且 ac = 0 且 valueScore ≥ 6 但字段数 < 硬地板）→ tier2，**仅限 Stage A 探针早停**。
- `usableFields`：已建 typed catalog 的数据集按目录内 `cov ≥ 0.85` 的字段数计，否则回退原始 `fieldCount`；台账 `*_dead` 数据集自动排除出排名。
- **金字塔配额**（缺省开）：`apply_pyramid_quota` 保证 tier1 至少 `pyramid_quota_non_model_min`（2）个非 MODEL。`category_weight` 夹在 0.9–1.15（`src/wqb/config.py::MINING`），禁止 1.3 vs 0.7 抹掉 PV / NEWS。

补充规则（KOR record_gate_v2 实证）：backfill_band / tier2 信号弱时强制 `ts_backfill(66/120)` 补偿覆盖；数据集级 cov 低但字段级 cov 高时走字段级救援；`mcp__wq-brain-http__get_datafields filter_sharpe=true` 已滤负 sharpe 字段；`alphaCount` 是平台级统计不分 region，局部竞争看 `userCount`。

## 二、评分前校准：`--calibrate`（先 dry-run 审，再写）

**评分权重不该用默认先验**（「零竞争 = 高价值」已被 EUR + GBR 证伪：`ac < 50` 几乎全是伪白空间，强信号集中在 `ac` 50–1000 甜区；category = model 是富矿）。`--calibrate` 从本战役**实测回测**反学 category 权重 + 拥挤甜区，写回 `thresholds.dataset_health`。**工具不自动执行它**（`campaign.py score` 与 workflow 派发都不自动调），但 **RA 步 2 的 SOP 要求显式执行**——两句话不矛盾：机器不会替你调，流程要求你调。

```powershell
& $WQ_PY "$TK/score_datasets.py" --campaign-dir $CD --calibrate --dry-run   # ① 只采集 + 计算 + 打印，不写 thresholds
& $WQ_PY "$TK/score_datasets.py" --campaign-dir $CD --calibrate             # ② 人工确认无异常后才写盘
```

**审 dry-run 输出时的两处异常 → 怎么办**（2026-08-27 USA / GBR / MEA / IND / KOR 五区域实测）：

| 现象 | 含义 | 动作 |
|---|---|---|
| 甜区 `ac` 异常巨大（如 MEA 测出 8560–21508） | 疑似拥挤度口径把区域全部 alpha 算成了数据集拥挤，甜区反转会**反向奖励超拥挤** | **不要 apply**，先查 `ac` 来源 |
| `strong_acs` 为空（无 best ≥ 1.5 的强信号，如 IND / GBR） | 甜区退回缺省 50–1000，但仍会开 `sweet_spot_enable` | 确认该区域确实要甜区逻辑再 apply |
| 无数据区域（`alphas` 表无实测，如 KOR） | 护栏跳过、不写（安全降级） | 无需处理，不会污染配置 |

**数据源优先级**（实测反学类工具通用；USA 2026-08-27 实证 `results/` 扫描只命中 4 个数据集）：① `alphas` 表 `list_alphas_by_region`（`sharpe` 直接非空，**唯一可靠主源**）> ② metrics 缓存 > ③ `expressions` 表（**`sharpe` 列恒 NULL，不可用**）> ④ `results/*.json` 文件名推断（checkpoint 被跳过，最不可靠）。归类**不信 `recovered_ds_*` 假名**（同一标号混多数据集），必须字段反查（`anl15_` → analyst15；catalog 唯一字段多数票）。

## 三、两段式探针（Stage A / B）

- 探针电池 8 个模板在 `config/platform_constraints.json` 的 `probe_battery`：P1 水平正 `rank(F)` / P2 水平镜像 `multiply(rank(F),-1)` / P3 差分 `rank(ts_delta(F,5))` / P4 均值差分 `rank(ts_av_diff(F,10))` / P5 衰减水平 `ts_decay_linear(rank(F),5)` / P6 时序自归一 `rank(ts_zscore(F,66))` / P7 动量 `rank(ts_delta(F,22))` / P8 稀疏修复 `rank(ts_backfill(F,66))`；`F` 由程序替换，VECTOR 数据集自动包 `vec_avg`。（下文「探针 P1–P8」专指这一组模板。）
  窗口口径：5 / 22 / 66 是周 / 月 / 季；**P4 的 10 有 KOR model219 实测依据**（`numrevy1` 靠它从 0.3 → 1.08），属证据支持的例外，其余不要再引入非标窗口。
- **Stage A** = {P1, P2, P4, P5}（信息量 / 成本比最高）。Stage A 评完若 `EARLY_RED` → 不跑 Stage B（省批）。
- 字段选取：变化 / 水平 / 质量三族（关键词族可覆盖，见 `field_family_keywords`），各族按 coverage 降序 + userCount 升序取 `n//3`，不足再补足。

## 四、三灯 v2（参数全在 `thresholds.probe_scoring_v2`）

```
potential = w_sharpe·|sh_best| + w_fitness·fit_best + w_mirror·[存在 sh<-0.5 的镜像] + w_margin·[margin>5bp]
          + w_tvr·[tvr∈[tvr_low,tvr_high]] + w_rn·[rn≥rn_bar] + w_breadth·min(b,4)/4 − cw_penalty·[best 带 CW 失败]
绿灯 ≥ green_min；黄灯 ≥ yellow_min；其余红灯
```

`b` = `|sh| ≥ breadth_bar` 的探针数。**核心原则：联合评估在最强探针单点**（`margin` / `tvr` / `rn` / `fitness` 都取 `|sh|` 最大那一针的值）——v1 全池 OR 会拼出「不存在的理想探针」，已废弃仅作对照。权重与阈值的**当前值以 `thresholds.probe_scoring_v2` 和 `score_v2()` 为准**（不同区域可不同；本文不抄，避免与配置漂移）。

三灯里的 `margin > 5bp` / `tvr 5–30%` / `rn ≥ rn_bar` 是**探针筛选口径**，与内部严线（`config.GATES_INTERNAL`：margin > 10bp、换手 5–20%）和 `RN_EXPOSURE`（评审用，`rn ≤ 0` 判墙）**不是同一套**：探针阶段宽、评审阶段严，别互相套用。

### 特殊判定

- **Stage A 早停**：`stage=A` 且 `max|sh| < early_red_sh`（缺省 0.3）且无镜像 → `EARLY_RED`，不跑 Stage B。
- **2Y 红灯**：`|sh_best| ≥ red_2y_sh_abs_min` 且 `two_year_sharpe < red_2y_max` → 直接 RED（近 2 年衰减，不深挖）。**仅当平台返回 `two_year_sharpe` 时判定；`None` 不判**（v1 把 `None` 当 0 会误判）。
- **tvr 结构性墙**：全部探针 `tvr` 同侧出界（全 < `tvr_low` = LOW，全 > `tvr_high` = HIGH）→ 绿灯封顶黄灯。LOW：先 `trade_when` / `decay` 拉 tvr 再评，限 2 批（KOR multi_source_model 教训）；HIGH：拉长窗口 / 加大 `decay` 压 tvr（news_sentiment_transfer 教训）。

### 动作建议（`score_v2` 打印的 `action`，已与「禁止拼腿」对齐）

| 灯 | 动作 |
|---|---|
| 绿灯 | 深度挖掘：单信号结构变体 / FE 假设族 / 参数精磨；**不拼腿** |
| 绿灯带 CW 失败 | 深挖，用**事件门控 / group 分组 / 同源价差**修 CW；不要加权或等权拼腿（闸 5 全局禁止） |
| 黄灯 | 只做镜像腿（同一信号取反）与同源价差，限 2 批 |
| 红灯 | 判死入台账，不回头（镜像偏强可选留 1 批镜像验证）；判死判据以 RA 决策表为准，探针红灯只是「这个数据集首探无信号」 |

> 旧版（含代码打印的 `action`）曾写「绿灯带 CW 失败 → 骨架直接上跨 Category rank 加法」「黄灯 → 两两融合」——这两条恰是闸 5 禁止的拼腿，2026-09-29 已从代码与文档同时改掉。

### 落地动作

- `--probe-score <multisim> --dataset <ds> --stage A|B|all [--mark-dead]`：RED / EARLY_RED 且 `--mark-dead` 时自动写台账 `<ds>_dead`。
- `--from-json <file>`：从本地 JSON lines 指标文件离线评分（校准 / 复盘用，不耗配额）。
