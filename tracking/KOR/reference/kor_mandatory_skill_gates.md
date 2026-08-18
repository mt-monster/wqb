# KOR 战役强制 Skill 门（MANDATORY SKILL GATES）v1.0 — 2026-08-16

> 背景：wave22-35 复盘发现 6 处 skill/mcp 利用缺口，直接造成配额浪费与卡点
> （dl_riskfree 无白名单→2次ERROR连坐；PROD墙死磕不用专项优化器；判死不查论坛；
> 1500字段人肉侦察；自相关烧API；同骨架变体连发15批）。
> 本 playbook 为战役强制纪律：**不过门不进入下一阶段**。

## G0 数据集选择门
- 必用：`wq-brain-campaign-matrix`（查区域台账/死路/胜率）+ `score_datasets.py`（三灯探针评分）。
- 禁止凭印象选数据集；新开数据集先跑探针电池（kor_dataset_probe_battery.json）。

## G1 字段白名单门（本次最大教训）
- 必用：toolkit `scan_fields.py --dataset <ds>` 落 typed catalog → `reference/kor_<ds>_field_whitelist.json`。
- **铁律：无白名单的数据集禁止发批**。字段名不得凭模式推测（实证：label3 带 `_2`/label0 不带；`ts_av` 不存在）。
- 白名单缺失清单（2026-08-16 清点）：dl_riskfree_returns、other455、insider_feats（复攻前必补）。

## G2 表达式生成门
- 必用：`alpha-expression-verifier`（语法）+ `gate.py`（5闸：字段白名单/vec包裹/毒结构/sha1缓存）。
- 必用：`build_wave.py` 选波——**强制全历史去重 + 骨架配给（linear_mix≤0.5）**，禁止手工连发同骨架变体（wave34 教训：同骨架15批边际收益≈0）。
- 新数据集首攻建议叠加：`brain-data-feature-engineering`（自动特征工程方案）替代人肉翻字段。

## G3 回测提交门
- 必用：`pipeline.py run --submit`（单批在飞/配额闸/429退避/断点续跑），8 并发上限遵守 `_concurrency_rule`。
- 自相关检查优先本地：`brain-calculate-alpha-selfcorrQuick`（省 API 配额），平台查询只做终验。

## G4 判决门
- 必用：`review_wave.py --write-ledger`（walls 诊断 + 台账回写）。
- **判死前必查论坛**：`brain-forum-browse`（目标明许参考论坛模板与idea文章；穷尽性判死必须有论坛证据，否则只能标"暂挂"）。

## G5 PROD/卡点专项门（本次卡点直接对策）
- 任一全门槛过 alpha 遇 PROD>0.7：**必须先跑 `wq-brain-alpha-optimization-v1`**（Mode A 参数层 8 候选批 / Mode B idea层字段族替换），拿到该 skill 的结论后才允许判"结构性墙"。
- 提交前质量审查：`brain-alpha-judge`（硬检查+论坛语料经验）。
- PROD 墙判别先于扩批：先查该数据集 >0.7 alpha 个数，墙薄（≤20/7.9万）优先换数据集而非死磕。

## G6 工具层基建门
- MCP/直连脚本必须对 400/401/429 有降级路径（已修：brain_api.py 分页 4xx 优雅降级，记忆 96122a23）。
- ERROR 批先疑批内连坐，用 `lookINTO_SimError_message` 下钻子任务（记忆 df1d0607），禁止盲目重发。

## 缺口修复状态表

| # | 缺口 | 修复方式 | 状态 |
|---|---|---|---|
| 1 | dl_riskfree/other455/insider_feats 无白名单 | scan 脚本+长退避后台补 | 🔄 进行中(限流) |
| 2 | optimization-v1 未用于 O0Gj6PqJ | G5 门强制 | 📋 下一批执行 |
| 3 | 论坛未查 | G4 门强制 | 📋 判死复核时执行 |
| 4 | feature-engineering 未用 | G2 门建议项 | 📋 other455 首攻执行 |
| 5 | selfcorrQuick 未用 | G3 门强制 | ✅ 已固化纪律 |
| 6 | build_wave 配给未强制 | G2 门强制 | ✅ 已固化纪律 |

## 平台事实补录（2026-08-16 实证）
- **KOR/D1 的 universe 只有 TOP600**（get_platform_setting_options 实证）：universe 切换杠杆不存在，P68 原计划的 TOP200/TOP1500 方案作废。
- KOR/D1 中性化共 11 选项：NONE/REVERSION_AND_MOMENTUM/STATISTICAL/CROWDING/FAST/SLOW/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/SLOW_AND_FAST。
- **SUBINDUSTRY 首次启用即出全门槛过 alpha**（88pZW2Vo sh2.59/2y2.27/ra=0）：中性化轨道未穷尽前不得判设置空间穷尽。
- STATISTICAL 轨 2y 崩（1.39/0.98 RA失败）：双轨对照制实证——STATISTICAL 提 IS 指标但伤 2y。
- 同设置同表达式重复提交会被平台去重为同一 alpha（批内重复式不烧额外资源）。
