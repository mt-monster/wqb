# 探针 v2 三灯评分 + 数据集评分

## 数据集评分（score_datasets.py 默认模式）

公式（v3.1，4 权重，vs 缺失按 0.5）：
```
score = 0.40*coverage + crowd_penalty(alphaCount) + 0.20*min(log1p(usableFields)/log1p(1000),1) + 0.10*min(valueScore,10)/10
crowd_penalty: ac<=50 → 0.30；50→500 线性降至 0.15；500→5000 线性降至 0.02；>5000 恒 0.02（P5 分段罚）
```
（旧式 0.30/(1+log10(1+ac)) 已废：对 ac>1e4 仅降 0.25 分，被 0.4*cov 淹没，USA 实测 analyst15 ac=102072 靠 cov≈1 进 tier1。）

tier 规则（thresholds.dataset_health，v3.1）：
- 硬地板（与模式无关）：cov < coverage_hard_min(0.65) 或 usableFields < field_count_hard_min(5) → excluded
- mode=general：alphaCount 只进 score 软罚，无硬闸；mode=ppa：alphaCount ≤ alpha_count_max(50) 硬闸（tier1 超标降 tier2）
- tier_method=quantile（缺省）：非硬排除者按 score 分位分带，tier1 ≥ P(tier1_score_pct=0.8) ≈ top20%，tier2 ≥ P(tier2_score_pct=0.55)；threshold=固定阈值回退
- 保底带（tier_note 溯源，只升不降）：backfill_band(0.65≤cov<0.85 & ac≤50 & vs≥6)→tier2；probe_exception(cov≥0.9 & ac=0 & vs≥6 & 字段<硬地板)→tier2 仅限 Stage A 探针早停
- usableFields（P3）：已建 typed catalog 的数据集按目录内 cov≥0.85 字段数计，否则回退原始 fieldCount；台账 `*_dead` 数据集自动排除出排名。
- **金字塔配额（默认开）**：`apply_pyramid_quota` 保证 tier1 至少 `pyramid_quota_non_model_min`(2) 个非 MODEL。`category_weight` 夹在 0.9–1.15（`src/wqb.config.MINING`），禁止 1.3 vs 0.7 抹掉 PV/NEWS。数字见 `src/wqb.config.MINING`。

补充规则（KOR record_gate_v2 实证）：backfill_band/tier2 信号弱时强制 ts_backfill(66/120) 补偿覆盖；数据集级 cov 低但字段级 cov 高时走字段级救援；`mcp__wq-brain-http__get_datafields filter_sharpe=true` 已滤负 sharpe 字段；alphaCount 是平台级统计不分 region，局部竞争看 userCount。

## 评分前必做：calibrate 自学习校准（dry-run 人工审 → apply）

**评分权重不该用默认先验**（"零竞争=高价值"已被 EUR+GBR 证伪：ac<50 几乎全是伪白空间，强信号集中在 ac 50–1000 甜区；category=model 是富矿）。`--calibrate` 从本战役**实测回测**反学 category 权重 + 拥挤甜区，写回 `thresholds.dataset_health`。但它**不在默认流程里**（ra-pipeline SOP / `campaign.py score` 派发都不自动调），需显式跑。

**标准两步（先审后写，防异常数据污染配置）**：
```bash
# ① dry-run：只采集+计算+打印，不写 thresholds —— 人工审结果是否合理
$PY $TK/score_datasets.py --campaign-dir $CD --calibrate --dry-run
# ② 确认无异常后正式 apply（去掉 --dry-run 才写盘）
$PY $TK/score_datasets.py --campaign-dir $CD --calibrate
```

**审 dry-run 输出时重点看两处异常**（2026-08-27 USA/GBR/MEA/IND/KOR 五区域实测）：
- **甜区 ac 异常巨大**（如 MEA 测出 ac 8560–21508）：疑似拥挤度口径把区域全部 alpha 算成了数据集拥挤，甜区反转会**反向奖励超拥挤**——**勿 apply，先查 ac 来源**。
- **strong_acs 空**（无 best≥1.5 强信号，如 IND/GBR）：甜区退回默认 50–1000，但仍会开 `sweet_spot_enable`——确认该区域确实要甜区逻辑再 apply。
- **无数据 region**（alphas 表无实测，如 KOR）：走护栏跳过不写（安全降级），不会污染配置。

**数据源优先级**（实测反学类工具通用；USA 2026-08-27 实证 results/ 扫描只命中 4 个数据集）：① `alphas` 表 `list_alphas_by_region`（sharpe 直接非空，唯一可靠主源）> ② metrics 缓存 > ③ `expressions` 表（**sharpe 列恒 NULL，不可用**）> ④ `results/*.json` 文件名推断（checkpoint 被跳过，最不可靠）。归类**不信 `recovered_ds_*` 假名**（同一标号混多数据集），必须字段反查（`anl15_`→analyst15；catalog 唯一字段多数票）。

## 两段式探针（Stage A/B）
- 探针电池 8 模板见 toolkit `config/platform_constraints.json`（P1 水平正 / P2 水平镜像 / P3 差分 / P4 均值差分 / P5 衰减水平 / P6 时序自归一 / P7 动量 / P8 稀疏修复；expr 中 F 由程序替换，VECTOR 数据集自动包 vec_avg）。
- Stage A = {P1, P2, P4, P5}（信息量/成本比最高）。Stage A 评完若 EARLY_RED → 不跑 Stage B（省批）。
- 字段选取：变化/水平/质量三族（关键词族可覆盖），各族按 coverage 降序 + userCount 升序取 n//3，不足再补足。

## 三灯 v2 公式（12 参数全在 thresholds.probe_scoring_v2）
```
potential = 1.2*|sh_best| + 0.8*fit_best + 0.5*mirror(sh<-0.5) + 0.3*margin(>5bp)
          + 0.2*tvr(5-30%) + 0.2*rn(>=1.0) + 0.2*breadth(min(b,4)/4, bar=0.5) - 0.4*cw_fail
绿灯 ≥ 2.2（green_min）；黄灯 ≥ 1.2（yellow_min）；其余红灯
```
**核心原则：联合评估在最强探针单点**（margin/tvr/rn/fitness 都取 |sh| 最大那一针的值）——v1 全池 OR 会拼出"不存在的理想探针"，已废弃仅作对照。

### 特殊判定
- **Stage A 早停**：stage=A 且 max|sh| < early_red_sh(0.3) 且无镜像 → EARLY_RED，判死不跑 Stage B。
- **2Y 红灯**：|sh_best| ≥ 0.8 且 two_year_sharpe < 0.6 → 直接 RED（近 2 年衰减判死不深挖）。**仅当平台返回 two_year_sharpe 时判定；None 不判**（v1 把 None 当 0 会误判）。
- **tvr 结构性墙**：全部探针 tvr 同侧出界（全 <5% = LOW，全 >30% = HIGH）→ 绿灯封顶黄灯。LOW 配 action"先 trade_when/decay 拉 tvr 再评，限2批"（KOR multi_source_model 教训）；HIGH 配"拉长窗口/加大 decay 压 tvr"（news_sentiment_transfer 教训）。
- 绿灯带 CW 失败 → action 提示骨架直接上跨 Category rank 加法；黄灯 → 只做镜像腿与两两融合限 2 批；红灯 → 判死入台账（镜像偏强可选留 1 批镜像验证）。

### 落地动作
- `--probe-score <multisim> --dataset <ds> --stage A|B|all [--mark-dead]`：RED/EARLY_RED 且 --mark-dead 时自动写台账 `<ds>_dead`。
- `--from-json <file>`：从本地 JSON lines 指标文件离线评分（校准/复盘用，不耗配额）。
