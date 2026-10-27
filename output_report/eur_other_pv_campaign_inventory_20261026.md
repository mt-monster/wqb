# EUR · OTHER 与 Price Volume(PV) 数据集 campaign 跑动盘点

> 数据源：`results/full_template_campaign_results.json`（123 集 / 4003 条 α）、
> `data/wqb.db::dataset_profile`（EUR 169 集）、`results/full_template_campaign_checkpoint.json`
> 口径：判定取 `verdict`；`S@2Y` = max-S 那颗自己的 2Y（区分「同一颗」还是「分属两颗」）；prod 取 `prod_top`
> 时间：2026-10-26 15:50

---

## 1 一句话结论

| 类别 | 集数 | 有 α 的集 | α 消耗 | S≥1.58 命中 | 命中率 | **可交付** |
|---|---|---|---|---|---|---|
| **OTHER** | 37 | 19（51%） | **845**（占全池 21%） | **31**（占全池 60%） | **3.7%** | **0** |
| **PV** | 20 | 1（5%） | **59**（占全池 1%） | **0** | **0%** | **0** |
| （全 EUR 对照） | 169 | 56 | 4003 | 52 | 1.3% | 0 |

**OTHER 是命中率最高的类别（3.7%，全池 3 倍），却交付为零** —— 31 条命中有 19 条来自
无效样本（`other315` 晚起 2022）、12 条撞 prod 墙（0.85 / 0.91）。

**PV 是几乎没开过的类别** —— 20 个集只有 1 个跑过（59 条 α，占预算 1%），
而且它在 campaign 排序里位于 **128–165 / 169**，物理上轮不到。

---

## 2 OTHER：37 个集

### 2.1 全清单（按 maxS 降序）

| 数据集 | 字段 | cov | 判定 | α | maxS | S@2Y | max2Y | joint | prod | yp |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| `other315` | 32 | 0.52 | **INVALID_SAMPLE** | 87 | **2.91** | 0.0 | 1.42 | 0 | 0.4675 | FRAGILE(2022/2y) |
| `techindi_model` | 798 | 1.00 | **ALIVE** | 51 | **1.91** | 2.05 | 2.13 | **5** | 0.8511 ✗ | OK(2014/10y) |
| `dl_riskfree_returns` | 133 | 0.94 | BORDERLINE | 65 | **1.69** | 1.51 | 1.96 | 0 | 0.9114 ✗ | OK(2014/10y) |
| `news_sentiment_nlp` | 23 | 0.91 | DEAD | **141** | 1.20 | 1.10 | 1.70 | 0 | — | OK(2014/10y) |
| `other571` | 30 | 0.76 | DEAD | 71 | 0.99 | 1.30 | 1.99 | 0 | — | 未测 |
| `insider_matrix` | 33 | 0.61 | DEAD | 52 | 0.98 | 0.98 | 1.51 | 0 | — | 未测 |
| `other545` | 4 | 0.54 | DEAD | 16 | 0.92 | 0.13 | 0.74 | 0 | — | 未测 |
| `other635` | 6 | 0.62 | DEAD | 19 | 0.92 | 0.15 | 0.77 | 0 | — | 未测 |
| `other424` | 3 | 0.69 | DEAD | 19 | 0.83 | −0.40 | 0.98 | 0 | — | 未测 |
| `acquisition_model` | 15 | 0.75 | DEAD | 31 | 0.78 | 0.03 | 1.00 | 0 | — | 未测 |
| `search_interest` | 5 | 0.78 | DEAD | 12 | 0.77 | 0.16 | 0.29 | 0 | — | 未测 |
| `insider_trx_matrix` | 33 | 0.61 | DEAD | 45 | 0.72 | 1.39 | 1.55 | 0 | — | 未测 |
| `stock_search_trends` | 6 | 0.54 | DEAD | 16 | 0.70 | −0.08 | 0.90 | 0 | — | 未测 |
| `other296` | 19 | 0.56 | SPLIT | 38 | 0.66 | 0.11 | 1.88 | 0 | — | 未测 |
| `ai_news_scores` | 105 | 0.79 | DEAD | 46 | 0.64 | −0.43 | 1.00 | 0 | — | 未测 |
| `other455` | 1500 | 0.96 | DEAD | 60 | 0.61 | 1.99 | 1.99 | 0 | — | 未测 |
| `equity_forum_data` | 8 | 0.41 | DEAD | 10 | 0.57 | 0.98 | 1.03 | 0 | — | 未测 |
| `event_relation` | 12 | 0.58 | DEAD | 33 | 0.43 | 1.66 | 1.87 | 0 | — | 未测 |
| `stock_cluster_dl` | 5 | 0.46 | DEAD | 33 | 0.29 | −0.12 | 0.52 | 0 | — | 未测 |

**判定分布**：`DEAD 16` / `SKIPPED_LOW_COV 16` / `ALIVE 1` / `BORDERLINE 1` /
`INVALID_SAMPLE 1` / `SPLIT 1` / `SKIPPED_TOO_FEW_FIELDS 1`

### 2.2 产出归因：31 条命中，0 条可交付

| 来源 | 命中数 | 为什么不算 |
|---|---:|---|
| `other315` | **19** | 首年 2022 / 仅 2 年 ⇒ 样本无效（`INVALID_SAMPLE`），任何闸位调参无意义 |
| `techindi_model` | 6 | prod **0.8511** ⇒ prod 墙（joint=5 是全 EUR 最好的形状，仍出不去） |
| `dl_riskfree_returns` | 6 | prod **0.9114** ⇒ prod 墙 |
| 其余 16 集 | **0** | maxS 全部 < 1.5 |

### 2.3 预算效率：76% 沉没

- 19 个有 α 的集共消耗 **845 条**
- 其中 maxS < 1.5 的 16 个集消耗 **642 条 = 76%**，零产出
- 最大单点浪费：`news_sentiment_nlp` **141 条 α**，maxS 仅 1.20（占 OTHER 预算 17%）
  次大：`other571` 71 条（0.99）、`dl_riskfree` 65 条（有产出）、`other455` 60 条（0.61）

> 141 条 α 停在 1.20，是因为 `news_sentiment_nlp` 的字段是日频文本分数，
> 而 `d1_va` 型变化量构造（该集最强族）在文本分数上会放大噪声。
> 这是「形态 × 字段性质错配」，不是字段没信号。

### 2.4 质量闸覆盖：这才是最该补的洞

| 闸 | 已测集数 | 缺口 |
|---|---|---|
| 年度画像 yp | **4 / 19** | 15 个集不知道是否 fragile —— `other315` 就是栽在这里 |
| prod | **3 / 19** | 16 个集的候选从未测过 prod |
| 设置轴扫 | **1 / 19** | 已知流水线缺陷（按集级 max_s 判），已修为按 α 判 |

---

## 3 PV：20 个集

### 3.1 全清单

| 数据集 | 字段 | cov | 判定 | α | maxS | 备注 |
|---|---:|---:|---|---:|---:|---|
| `pv87` | 1649 | 0.50 | DEAD | **59** | 0.93 | **唯一跑过的集**（低覆盖波 + E1） |
| `pv173` | 105 | 0.33 | SKIPPED_LOW_COV | 0 | — | |
| `investor_activity` | 47 | 0.16 | SKIPPED_LOW_COV | 0 | — | |
| `pv109` | 25 | 0.44 | SKIPPED_LOW_COV | 0 | — | |
| `univ1` | 6 | 1.00 | SIM_FAIL | 0 | — | universe 旗标集（`topdiv3000`/`minvol1m`），冒烟时确认 NO_DATA |
| `pv141` | 2 | 0.50 | 未跑 | 0 | — | 字段 < 3，结构性排除 |
| `pv47` | 2 | 1.00 | 未跑 | 0 | — | 字段 < 3 |
| `univ2` | 1 | 0.67 | 未跑 | 0 | — | 字段 < 3 |
| `pv149` | 1 | 1.00 | 未跑 | 0 | — | 字段 < 3 |
| **`pv20`** | **1475** | 0.69 | 未跑 | 0 | — | 未测字段 **735** |
| **`intraday_pv_feats`** | **585** | 0.95 | 未跑 | 0 | — | 未测字段 **578** |
| **`continuation_score`** | **560** | 0.99 | 未跑 | 0 | — | 未测字段 **545**，aCnt 仅 35 |
| **`pattern_scores`** | **504** | 0.99 | 未跑 | 0 | — | 未测字段 **499**，aCnt 仅 27 |
| `pv30` | 558 | 0.82 | 未跑 | 0 | — | |
| `pv37` | 251 | 1.00 | 未跑 | 0 | — | |
| `pv29` | 80 | 0.56 | 未跑 | 0 | — | 在待复跑队列（低覆盖波已暂停） |
| `pv13` | 73 | 0.65 | 未跑 | 0 | — | aCnt 332 |
| `pv1` | 24 | 1.00 | 未跑 | 0 | — | aCnt **44048**，字段是 `adjfactor/adv20/cap` ⇒ 天生破 ATOM |
| `pv106` | 15 | 1.00 | 未跑 | 0 | — | slippage/spread 族 |
| `pv103` | 9 | 0.98 | 未跑 | 0 | — | |

**判定分布**：`DEAD 1` / `SKIPPED_LOW_COV 4` / `SIM_FAIL 1` / **`未跑 14`**

### 3.2 为什么 PV 基本没跑：排序位次 + 点亮口径错误（已更正）

> ★ **2026-10-26 16:00 更正**：本节初版写「PV 被标已点亮（6 个提交）」，**这是错的**。
> 点亮口径 = **同一 region/delay/赛季（自然季度）下该 category 提交 ≥3**，数据源唯一权威是
> 平台 `get_pyramid_alphas`（默认返回当前季度快照）。
> 平台当季实测（EUR / D1）：`pv=1 ｜ other=1 ｜ model=3 ｜ analyst=5 ｜ fundamental=2 ｜ risk=2 ｜ insiders=1`
> ⇒ **EUR 真正已点亮只有 ANALYST(5) 与 MODEL(3)**；PV=1、OTHER=1 **都未点亮**，离点亮只差 2 颗。
> 「6 个提交」是旧 `lit.py` 统计**全部历史 OS alpha**（无时间过滤）得到的**累计值**，不可用。

即便如此，PV 排在队尾的**机制**仍成立，只是原因有三层：

1. `lit.py` 用累计值 ⇒ 把 pv 从 1 虚报成 6，判成「已点亮」并降权；
2. `pipeline.py` 把**整个 counts 字典**传给 `all_datasets(lit_cats=counts)`，而该函数把**字典的每个键**
   都当「已点亮」⇒ 等价于「凡有过 1 个提交的类别（PV/OTHER/MODEL/ANALYST…）全部降权」，
   只有 0 提交的类别被优先；
3. 阈值比较写成 `> 3`（=4 才亮），官方是 `≥3`。

三条叠加后 PV 的位次是 **128–165 / 169**，而 campaign 每波只取 6–12 集、`done` 停在 123 ⇒ 轮不到。

修正后（lit = {ANALYST, MODEL}）PV 内各集位次显著上移：
`pv30 → 40`、`pv13 → 56`、`other455 → 59`、`earningscall_sentiment → 49`、`pv20 → 70`、`pv37 → 71`、`other335 → 79`。

**所以 PV 的「0 命中」是「没测」，不是「测了不行」。** 这是两类数据里最重要的区别。

### 3.3 唯一跑过的 `pv87`：59 条全沉没，但 E1 给了方向

- 59 条 α，maxS **0.93**（`lvl_rk`），0 条 ≥1.5
- 但 E1 同字段配对实测：`group_rank(lvl_rk, market)` 相对裸 `lvl_rk` **Δ 均值 +0.156**，
  最高从 0.60 → **0.81**；两个 lvl_rk≈0 的字段被拉到 0.79
- 结论：**pp 抬地板不抬天花板** ⇒ 它能把「被归一化方式误杀」的字段救回来，
  但救不到 1.58。PV 要出东西，还是得靠**字段本身有信号**

### 3.4 PV 的字段语义风险（必须说明）

`pv1` 的 24 个字段是 `adjfactor / adv20 / cap` 这类基础量 —— 按 ATOM 规则，
`returns/close/volume/vwap/cap/adv20` 属于**隐形破 ATOM** 的字段，拿它做单数据集 alpha 会丢塔。
`univ1` 的字段是 universe 旗标（`topdiv3000`/`minvol1m`/`top3000`），当信号用必然 NO_DATA（已实测）。

⇒ **PV 里有约 5 个集属于「能跑但产出无意义」**（`pv1`/`univ1`/`univ2`/`pv47`/`pv149`），
真正值得跑的是 `pv20` / `intraday_pv_feats` / `continuation_score` / `pattern_scores` / `pv30` / `pv37` / `pv13`。

---

## 4 未跑机会池

| 类别 | 未跑集 | 字段合计 | 其中「高价值未测字段」 |
|---|---:|---:|---|
| OTHER | 4（全部在待复跑队列） | 298 | `insider_feats` 43 个未测字段 |
| **PV** | **11（可跑但从未选中）** | **4134** | **2357**（pv20 735 + intraday_pv_feats 578 + continuation_score 545 + pattern_scores 499） |

补充：`earningscall_sentiment`（167 字段，平台 aCnt 4800）与 `other335`（aCnt 2211）虽然未跑，
但平台已挖得很透，预期低；`insider_feats` 平台只挖了 52 条、118 字段里 43 个未测，是 OTHER 侧最后一块。

---

## 5 GLB 侧这两类的可跑量

| 类别 | GLB 集数 | cov≥0.6 且字段≥3 | 已在当前队列 |
|---|---:|---:|---|
| OTHER | 25 | **15** | `techindi_model`(1818 字段)、`other455`(1500) |
| PV | 16 | **9** | `pv30`(150)、`pv37`(80) |

当前 GLB 战役 8 个集队列：`other455, pv30, pv37, techindi_model, model135, chart_cnn_alpha,
predictive_starmine, risk70` —— 其中 OTHER 2 / PV 2。进度 **done=0/8**，正在跑 `chart_cnn_alpha`。

> ⚠ **GLB 的覆盖率不可信，开大波前必须验**：上一轮 26 个集里有 **11 个 NO_DATA**
> （另有 14 个 SKIPPED_LOW_COV、1 个字段不足），包括 `news73`（cov=1.0）、`news76`（cov=1.0）、
> `fundamental44`（0.82）、`analyst11`（0.74）。
> 高 cov 也会 NO_DATA ⇒ GLB 的 `dataset_profile` 是从 `field_profile_perf` 汇总来的，
> 字段在 EUR/USA 有效不代表 GLB 有效。建议先用 `pv37`（80 字段、cov 1.0）单集验证再放大。

---

## 6 建议（按性价比排序）

**P0 · 开 PV 的 11 个可跑集**（这是一整类「未测」资产）
只跑 `pv20 / intraday_pv_feats / continuation_score / pattern_scores / pv30 / pv37 / pv13` 七个，
排除 `pv1`/`univ1`/`univ2`/`pv47`/`pv149`（字段语义破 ATOM 或无数据）。
理由：`pattern_scores`(aCnt 27) 与 `continuation_score`(aCnt 35) 是全池**平台挖掘最浅**的两个大集，
`intraday_pv_feats` 578 个字段从没测过。这是唯一还没被否证的路径。

**P1 · 补 OTHER 的 yp 与 prod 缺口**（成本极低，1 次 API/集）
15 个有 α 的集缺 yp。`other315` 的教训是：先算 yp 再谈闸，否则会把 2 年样本的 2.91 当成宝。

**P2 · 单独攻 `techindi_model` 的 prod 墙**
它是全 EUR 唯一 `joint=5`、S 1.87–1.91、F 1.20–1.25 的集，只卡 prod 0.8511。
用手工验证过的设置轴（`SLOW_AND_FAST` 在 `quant_factor_lib` 上给过 +0.23 S）重扫，
但注意 prod 会同步上升 —— 需要先算 S–prod 前沿再判断可达性。

**P3 · OTHER 剩 4 个集复跑**（低优先）
`insider_feats` 值得（43/118 未测）；`earningscall_sentiment`(aCnt 4800)、`other335`(2211) 预期低。

**不做**：`news_sentiment_nlp` 这种 141 条停在 1.20 的集，问题在「形态 × 字段性质错配」，
在模板层已改为 `signed_power(dw,0.7)`，但不值得单独重跑 —— 让新模板在下一次全量时自然覆盖。
