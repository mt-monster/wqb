# 数据集挖掘经验索引（跨区）

更新：2026-10-30。本目录按 `<region小写>_<dataset>_campain.md` 命名（历史文件沿用 `campain`
拼写，勿改）。每个文件限定**该轮设置与时间范围**的实测结论，不外推为数据集全历史结论。

管理方式：`brain-dataset-mining-experience` 技能。主流程 S6 更新，下一轮 S-PRE / S1 / S2 读取。
数据以 DB 为权威；**自动块是统计证据，块外是经审查的中文机制复盘**。无新数据时刷新幂等，
人工复盘不会被覆盖。

---

## GBR（D1 / TOP700）

2026-10-30 新增 6 份。GBR 侧的核心背景：183 个数据集中「既未判死又 coverage>0」
的未点亮塔数据集实读为 **0**，因此这批文件的主题是**判死 + 唯一量产线**，不是新发现。

| 数据集 | 文件 | 结论类型 | 核心经验 |
|---|---|---|---|
| **fundamental6** | [gbr_fundamental6_campain.md](gbr_fundamental6_campain.md) | ★ **唯一量产线** | `divide(fnd6_<科目>, cap)` 跨量纲族 13 条 S≥1.58 全闸通过；3 条已测 prod 0.6577–0.6932（**薄余量 0.007–0.042**）；`effective=2` 同时点 PV+FUNDAMENTAL 两塔；扩招必须换财务科目不许换窗口 |
| analyst83 | [gbr_analyst83_campain.md](gbr_analyst83_campain.md) | 判死（6 模板 / 5 族） | 电话会议语言数据；最好 S 0.29 = 闸 18.4%，`R/TO` 0.095 ⇒ F 上限 0.089 = 闸 8.9%；七种 VECTOR 折叠都救不回来 |
| other384 | [gbr_other384_campain.md](gbr_other384_campain.md) | 判死（6 模板 + E11） | 电话会议 Q&A；`coverage 0.82` + `tier STANDARD` + 倍率 1.7 三个「该挖」信号同时成立仍全灭 |
| fundamental45 | [gbr_fundamental45_campain.md](gbr_fundamental45_campain.md) | 判死（2 探针） | 同源姊妹集；双模型分歧 S −0.57 / 双重差分 S −0.17（**负信号**）；`alpha_count 0` + 倍率 2 是诱因而非证据 |
| techindi_model | [gbr_techindi_model_campain.md](gbr_techindi_model_campain.md) | 判死（prod 饱和） | `tm_16` self 0.87–1.0 自锁 / `tm_17` prod 0.7343–1.0；IS 侧很强（180 行 / 26 波 / maxS 1.91 / max2Y 2.08）⇒ **指标够、生产池撞墙**的典型 |
| other47 | [gbr_other47_campain.md](gbr_other47_campain.md) | 判死（8 模板） | SEMrush 流量 + Google Ads；**两个元数据陷阱**：数据集 description 被 "BBID↔RIC" 文案污染、同集内字段前缀不统一（4 带前缀 / 5 裸名） |
| fundamental93 | [gbr_fundamental93_tax_deferred_20261031.md](gbr_fundamental93_tax_deferred_20261031.md) | 判死（4 探针） | 递延税费用族 17 字段（全 MATRIX / 全 `coverage 0.0`）；**持仓仅 118–142 只 = 17%–20%** ⇒ 连带触发 `CONCENTRATED_WEIGHT` 硬闸（0.13/0.15 vs limit 0.1）；★ **`coverage: 0.0` 只能判「有没有数据」，「够不够」必须看 `longCount+shortCount`**（对照 fundamental86 的 83% 可用）|

合并证据：`analyst83` + `fundamental45` + `other384` = **16 条电话会议语言数据回测，0 达标**，
失败方向一致（水平弱、变化更弱、分歧/覆盖转负）⇒ 判死落在**机制族**，不是单个数据集。

---

## EUR（D1）

2026-09-25 批次（wave245–254，6 主数据集 57 条回测 / 53 个实际使用字段，合格 Regular 仍为 0）。

| 数据集 | 文件 | 完成数 | 核心经验 |
|---|---|---:|---|
| news46 | [eur_news46_campain.md](eur_news46_campain.md) | 5 | 均值语气/新颖度/影响排序差与年度变化均弱，停止本轮结构 |
| news50 | [eur_news50_campain.md](eur_news50_campain.md) | 8 | VECTOR 聚合及分类器分歧无合格信号；冷门与类型合规不足以保证收益 |
| fundamental23 | [eur_fundamental23_campain.md](eur_fundamental23_campain.md) | 18 | 融资依赖有强度，前四个强候选 prod 均超 .7；Mode B2 盈利暴露剥离仍 prod .7432 |
| fundamental17 | [eur_fundamental17_campain.md](eur_fundamental17_campain.md) | 14 | 8 主假设＋4 水平对照＋2 口径复验；利润水平 S 1.13、标准化利润水平 S 1.18、修正差额 S −.50 |
| other455 | [eur_other455_campain.md](eur_other455_campain.md) | 4 | 客户网络月收益 2 主假设＋2 对照；最高 S .32 / RN −.07 |
| other460 | [eur_other460_campain.md](eur_other460_campain.md) | 8 | MODEL 方向概率四组配对，最高 S .07；2Y 全负 |
| pv1（辅助） | [eur_pv1_campain.md](eur_pv1_campain.md) | 已含 other455 的 4 条 | `returns` 仅作公开基线；同参数不保证持仓掩码一致 |

未完成/待核实：wave250 年度均态候选的相关性仍未核实；wave253 的 4 条已产生 alpha 并收割，
但平台子任务终态为 WARNING，**不能表述为检查全通过**。

---

## KOR / DEU / USA

| 区域 | 数据集 | 文件 | 说明 |
|---|---|---|---|
| KOR | shortinterest38 | [kor_shortinterest38_campain.md](kor_shortinterest38_campain.md) | 卖空类机制与破闸配方 |
| DEU | shortinterest3 | [deu_shortinterest3_campain.md](deu_shortinterest3_campain.md) | 本目录最厚的一份（66 KB），含完整模板与逐条归因 |
| USA | analyst_consensus | [usa_analyst_consensus_campain.md](usa_analyst_consensus_campain.md) | 分析师一致预期族（41 KB） |

---

## 使用纪律

1. **先读本索引，再决定要不要读单集文件**。索引的「结论类型」列区分了「量产线」与「判死」，
   两者用法完全不同：前者找扩招方向，后者找禁用边界。
2. **判死文件不是「这个数据集没用」，而是「这条机制在这个区这条设置下没用」**。
   每条判死都写明了限制条件（模板数 / 探针数 / 设置档），重启前必须满足文件里列的
   「后续边界」前提。
3. **`backtest_results` 才是权威台账**。GBR 的 `analyst83` / `fundamental45` / `other47` /
   `other384` 四集回测**未入库**（实读 0 行），证据仅在本目录文件与 `registry_empirical`
   payload 里 —— 复用时先补 `upsert_backtest_rows`。
4. **归集候选不要用 `alphas.dataset_id`**：会混区（`region_id` 同病）且会把多数据集族记成
   单一假 id（`fnd6_/cap` 族被记成 `dataset_id=291`，真实为 368）。
   用 `backtest_results.dataset` 或表达式里的字段名归集。

---

## GBR（D1 / TOP700）— 2026-11-08 增补 5 份

背景：GBR 四塔（model/news/analyst/fundamental）经用户授权放开后挖尽；SHORTINTEREST 塔 11-08 由用户提交 RRE5Mwkn+bl6KwjwK 点亮。交付篮口径 = 互相关全对 <0.5（用户全局标准）。

| 数据集 | 文件 | 结论类型 | 核心经验 |
|---|---|---|---|
| **predictive_starmine** | [gbr_predictive_starmine_campain.md](gbr_predictive_starmine_campain.md) | ★ **新量产线** | 108 个修订计数字段 aC 0-17 冷门；FY1 收入净广度 × COLD 出货（bl6KwjwK S1.89/prod 0.4582）；比率/EBITDA/earnings 面全低一档；冷门筛选器 `aC≤20 且 cov≥0.6` |
| multifactor_return_pred / model109 | [gbr_multifactor_return_pred_model109_campain.md](gbr_multifactor_return_pred_model109_campain.md) | 判死（全量终审） | cov 是**数据源级平的**（0.4806/0.478 单值），无高覆盖冷门字段；LC 预计 ~330 |
| news50 | [gbr_news50_campain.md](gbr_news50_campain.md) | 判死（双向弱） | mws50_* 4 字段双向 ±0.7 内；GBR NEWS 塔终局 = nws17 唯一出货 |
| analyst48 | [gbr_analyst48_campain.md](gbr_analyst48_campain.md) | 判死（无机制） | 7 字段全为指数构造元数据 |
| （跨区方法论） | [../tracking/CHN/chn_admission_probe_20261106.md](../../tracking/CHN/chn_admission_probe_20261106.md) | ★★★ 方法论 | CHN 闸 2.07 / 翻号不对称（必须实测反号）/ insider 族 prod 深钉 / 0.5 交付篮口径 / get_datafields offset 失效用 max_fields |

另见：`tracking/GBR/session_assets_prodtable_multisim_20261108.md`（prod 表 v2 + multisim 注册表 + 跨区闸值速查）。
