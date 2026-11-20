# GBR / risk68（Forecast Data，风险因子/流动性权重面板，全 MATRIX）

> 塔：**risk**（GBR/D1 乘数 **1.3**）
> 画像日期 2026-11-19 · 数据源 `mcp__wq-brain-http__get_datafields`（GBR/TOP700/D1，`filter_sharpe=false`，不传 `max_fields`）
> 本轮实拉：`count=5` / `platform_count=5` / `returned=5` / `complete=true` / `pages_fetched=1` ⇒ 单页全量，去重字段数=平台声明数=5，**无需前缀 search 分片**。
> ⚠ 字段 id 全部取本轮平台实拉，**未引用**任何审计缓存 / 历史 md 快照。
> ⚠ 全部 5 字段 `coverage=0.0` 是 **GBR coverage 元数据已知盲区**，不等于无数据（见 §5 可用性三分 + §7 v8 判据）。
> ⚠ v11 修正：本集全 MATRIX，探针用原生 `rank(ts_backfill(f,250))`，**不得套 `vec_avg`**（VECTOR 算子，套 MATRIX 类型不匹配必 FAIL）。

---

## 字段全表

> 平台实拉 5/5，按 alphaCount 降序。第一列 = 平台真实字段 id（反引号）；cov = 平台 coverage 元数据（GBR 全 0，盲区）；αC = alphaCount；uC = userCount。全部 type=MATRIX、dateCreated=`2026-07-01`、pyramidMultiplier=1.3。

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `rsk68_residual_return` | MATRIX | 0.0 | 367 | 224 | 单日特质收益（实际收益减 β×市场收益），decimal 表达；本集 αC 最高、uC 最高 |
| `rsk68_weight_volatility_short` | MATRIX | 0.0 | 192 | 111 | 短期波动率估计，decimal 表达 |
| `rsk68_beta` | MATRIX | 0.0 | 152 | 96 | 欧洲资产相对区域流动性加权市场收益的 β（无单位），长滚动窗（约 504 交易日）估计 |
| `rsk68_weight_dadv` | MATRIX | 0.0 | 131 | 93 | 美元平均日成交量（SMA $ADV），作流动性权重（dollar 单位） |
| `rsk68_weight_edadv` | MATRIX | 0.0 | 121 | 85 | 指数衰减美元平均日成交量（EMA $ADV），作流动性权重（dollar 单位） |

> 平台实拉 αC 逐行：367 / 192 / 152 / 131 / 121；uC 逐行：224 / 111 / 96 / 93 / 85。

---

## 3. 聚合统计（基于平台实拉读数）

| 指标 | 值 |
|---|---|
| 字段总数 | 5（全部 MATRIX，无 VECTOR/GROUP） |
| coverage 分布 | 5/5 = 0.0（GBR 元数据盲区，非无数据） |
| alphaCount 合计 / 均值 | 963 / **192.6** |
| alphaCount 最大 / 最小 | 367（`rsk68_residual_return`）/ 121（`rsk68_weight_edadv`） |
| userCount 合计 / 均值 | 609 / **121.8** |
| userCount 最大 / 最小 | 224（`rsk68_residual_return`）/ 85（`rsk68_weight_edadv`） |
| dateCreated | 5/5 = `2026-07-01`（同批 onboard；非老集死字段） |
| pyramidMultiplier | 5/5 = 1.3（risk 塔，GBR/D1 未点亮） |
| αC=0 的字段 | 无（全部 ≥121，是相对活跃的字段集） |

数据集级元数据（本轮 `get_datasets(GBR,TOP700,D1,search=risk68)` 实拉）：`id=risk68` / `name=Forecast Data` / `category=risk` / `fieldCount=5` / `coverage=0.0`（同盲区）/ `userCount=381` / `alphaCount=796` / `valueScore=2.0` / `pyramidMultiplier=1.3`。
> 注：数据集 description 是模板串（描述订单簿 tick 统计），与 5 个风险模型字段不符，属平台描述错配——以字段级 description 为准。

---

## 4. 字段族拆解（按经济机制分组）

| 族 | 字段 | 读数 / 机制 |
|---|---|---|
| **A 市场模型族**（风险因子主力） | `rsk68_residual_return`(αC**367**)、`rsk68_beta`(152) | β 与特质收益：residual_return = 实际收益 − β×市场收益（decimal），β 为流动性加权市场模型暴露（无单位、~504 日滚动窗）；两者是 CAPM 类分解的核心输出，`residual_return` 是全集最活跃字段 |
| **B 波动率族** | `rsk68_weight_volatility_short`(αC192) | 短期波动率估计（decimal），可作风险刻度或分母（residual_return/vol 构造信息比率） |
| **C 流动性权重族** | `rsk68_weight_dadv`(αC131)、`rsk68_weight_edadv`(121) | SMA/EMA 美元平均日成交量（dollar 单位），作流动性权重；同一量的两种平滑（简单均值 vs 指数衰减），不可当成两个独立信号腿 |

**族间关系**：A/B 是风险模型输出（无单位或 decimal），C 是美元量纲的流动性权重。本集是**风险模型/流动性权重**面板（日频 MATRIX），与价格/成交量原始数据、与 institutions25（做空 VECTOR）经济机制不同。典型用法：`residual_return` 作信号主腿，`weight_volatility_short` 作波动率归一分母，`weight_dadv`/`weight_edadv` 作流动性加权或门控（见 §5/§7 实测）。

---

## 5. 可用性三分（信号 / 计数需归一 / 元数据不可用）

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可直接做信号**（无单位/decimal、已归一形态） | `rsk68_residual_return`(αC367)、`rsk68_beta`(152)、`rsk68_weight_volatility_short`(192) | 特质收益（decimal，零均值截面）、β（无单位）、短期波动率（decimal，正值）——三者量纲已归一，可直接 `rank`/`group_rank`/`ts_zscore`；`residual_return` 是 GBR 回测中的主信号腿（历史最高 S=1.82） |
| **② 量纲需处理**（dollar 单位权重，10⁶–10⁹） | `rsk68_weight_dadv`(131)、`rsk68_weight_edadv`(121) | 美元平均日成交量，量纲 10⁶–10⁹ 且右偏长尾，必须 `rank`/`log` 去量纲；语义是**流动性权重**而非独立信号，宜作加权/门控/分母，不与 A/B 裸水平 `add` 混腿 |
| **③ 元数据不可用**（coverage 盲区，非数据缺失） | 全部 5 字段的 `coverage=0.0` | GBR 已知盲区；GBR 107 条 `code LIKE '%rsk68%'` 回测 `long_count` 316–911、`short_count` 0–569，107/107 无双边同零（both0=0；13 条 `sc=0` 行 lc 均 668–911 >0，属配置伪影）证明有数据 ⇒ 不可据此判无数据/判死 |

---

## 6. 六法评测

| 法 | 结论 |
|---|---|
| **① 覆盖率** | 平台 `cov=0.0`（5/5）—— **GBR 元数据盲区**，非真实覆盖率。实证：GBR `backtest_results` 中 107 条 `code LIKE '%rsk68%'` 回测，`long_count` 316–911、`short_count` 0–569，**107/107 无 lc=0 且 sc=0、both0=0**，实际可用覆盖充足且稳定 ⇒ `density=dense`。 |
| **② 非零率** | 无法从 `cov=0` 元数据直接读；从回测反推：107 条回测中 94 条产生双边持仓（lc>0 且 sc>0）、13 条 `sc=0`（lc 均 668–911，属配置伪影），证实非零率高。`residual_return` 为零均值截面收益（正负各半），`beta`~1，`volatility_short`/`dadv`/`edadv` 恒正。 |
| **③ 更新频率** | 全部 `dateCreated=2026-07-01`（同批新 onboard）；字段语义为日频面板（1 日特质收益、~504 日滚动 β、SMA/EMA $ADV、短期波动率）⇒ **日更面板**（有固定滚动窗，非一次性事件）⇒ `density=dense`（日更 cov 稳）。 |
| **④ 分布形态** | `residual_return` 零均值截面 decimal（近对称、尾部略厚）；`beta` 无单位围绕 1 聚集；`weight_volatility_short` 正值右偏 decimal；`weight_dadv`/`weight_edadv` 美元额右偏长尾 10⁶–10⁹，需 `rank`/`log` 压尾。 |
| **⑤ VECTOR 折叠要求** | **全 5 字段为 MATRIX，无需且不得用 `vec_*` 折叠**（与 institutions25 全 VECTOR 相反）：直接进 `rank`/`ts_*`/`group_*`。`vec_avg` 是 VECTOR 专用算子，套在 MATRIX 上类型不匹配必 FAIL（v11 实测 risk68 5 字段 MATRIX 探针套 vec_avg 2/2 FAIL）。本轮 `validate_expressions` 对 5 条 MATRIX 原生探针 `rank(ts_backfill(f,250))` 全部通过（`valid=true`、`fields_checked=5`、`unknown_fields=[]`、`platform_field_count=5`）。 |
| **⑥ 量纲陷阱** | 三类量纲混在一集：无单位（`beta`）、decimal（`residual_return`/`volatility_short`）、美元额（`weight_dadv`/`weight_edadv`，10⁶–10⁹）⇒ **禁裸水平跨族 `add` 混腿**。`weight_dadv`/`edadv` 是 dollar 单位（非 shares、非 log 收益），`residual_return` 是 decimal（非 %）。统一 `rank`/`group_rank`/中性化去量纲后再组合；`dadv` 与 `edadv` 是同一量的两种平滑，勿当独立腿。 |

---

## 7. GBR v8 判据核验（cov 全 0 为何不判 excluded）

1. **排除规则原文**：cov 全 0 不得直接 `excluded`——techindi_model(399)/insiders12(74%)/analyst15(533) 均 cov=0 却有数据。cov 全 0 ⇒ `needs_probe` + NONE 探针；只有波次档案有 `lc/sc=0` 实测才可 `excluded`。
2. **本集实测反证**（本轮只读 DB 实测，命令见 §8）：GBR `backtest_results` 中 `code LIKE '%rsk68%'` 的 **107 条**回测，`long_count` 316–911、`short_count` 0–569，**107/107 无双边同零（both0=0、sc0 且 lc0 = 0）**。最高 S=1.82；`sharpe>0` 共 95 条——证明 MATRIX 字段数据真实存在，`excluded` 条件不成立。
3. **sc=0 行的真相**：`short_count=0` 的 13 行 lc 均 >0（668–911），含MATRIX 原生 NONE 探针 `rank(ts_backfill(rsk68_residual_return,250))`（lc=832、S=0.69）与 `rank(ts_backfill(rsk68_beta,250))`（lc=833、S=0.65），其余为 `ts_rank`/`if_else`/`group_rank`/`ts_quantile`/`trade_when`/`log`/`divide`/`delta`/`std_dev` 形态。多头侧数据充足，属 `rank()` 长仓配置伪影（配置层），**非数据层排除**——这正是 v11 强调「不得因某探针 sc=0 就判字段死」的实证。
4. **cov=0 的真相**：纯 GBR coverage 元数据盲区，不是数据缺失——107 条双边/单边千/百量级持仓回测即铁证。数据集级 `get_datasets` 亦报 `coverage=0.0`，但 `alphaCount=796`/`userCount=381` 说明平台上有大量用户在用。
5. **结论**：`verdict=needs_probe`，按 v11 逐字段 type 生成 NONE 探针。本集全 5 字段为 MATRIX ⇒ 一律用原生形态 `rank(ts_backfill(f,250))` @neutralization=NONE，**不套 `vec_avg`**。

### NONE 探针（v11 逐字段 type 生成，neutralization=NONE）

全部字段 type=MATRIX ⇒ 模板 `rank(ts_backfill(f,250))`（无 `vec_avg`）：

- `rank(ts_backfill(rsk68_residual_return,250))`
- `rank(ts_backfill(rsk68_beta,250))`
- `rank(ts_backfill(rsk68_weight_volatility_short,250))`
- `rank(ts_backfill(rsk68_weight_dadv,250))`
- `rank(ts_backfill(rsk68_weight_edadv,250))`

> ⚠ **MATRIX trap 注**：`vec_avg` 是 VECTOR 专用折叠算子，对 MATRIX 语义误用、类型不匹配必 FAIL（v11 实测 risk68 5 字段 MATRIX 探针套 vec_avg 2/2 FAIL）；已全部改为原生形态。本轮 `validate_expressions` 对上列 5 条全部通过。不得因 `rsk68_beta` / `rsk68_residual_return` 探针 `sc=0` 判字段死——两行 lc=832/833 证明数据存在，属配置层伪影。

---

## 8. 本轮实测命令与读数（可复核）

- 平台全量：`get_datafields(region=GBR,dataset_id=risk68,universe=TOP700,delay=1,filter_sharpe=false,不传max_fields)` ⇒ `count=5 / platform_count=5 / returned=5 / complete=true / pages_fetched=1`；5 行 id/type/cov/αC/uC/dateCreated/pyramidMultiplier 见 §字段全表。
- 数据集元数据：`get_datasets(region=GBR,universe=TOP700,delay=1,search=risk68)` ⇒ `fieldCount=5 / alphaCount=796 / userCount=381 / coverage=0.0 / valueScore=2.0 / pyramidMultiplier=1.3`。
- 探针校验：`validate_expressions(alpha_expressions=[5 条 MATRIX 原生探针],region=GBR,universe=TOP700,delay=1)` ⇒ `valid=true / expressions=5 / fields_checked=5 / unknown_fields=[] / unknown_soft=[] / platform_field_count=5`。
- DB 读数（只读 `data/wqb.db`，`mode=ro` URI，本轮实跑，2026-11-19 复核）：
  - `SELECT ... FROM backtest_results WHERE region='GBR' AND code LIKE '%rsk68%'` ⇒ **107 行**；`lc 316–911 / sc 0–569 / both0=0 / sc=0 共 13 行 / sharpe>0 共 95 行 / max sharpe=1.82`。
  - 13 条 `sc=0` 行（code 前缀, lc, sc, sharpe）：`rank(ts_backfill(rsk68_residual_return,250))` 832/0/0.69；`rank(ts_backfill(rsk68_beta,250))` 833/0/0.65；`ts_rank(rsk68_residual_return,5)` 668/0/0.77；`rank(if_else(not_equal(rsk68_residual_return,0),...))` 832/0/0.69；`group_rank(ts_decay_linear(rsk68_residual_return,60),subindustry)` 691/0/0.63；`rank(ts_quantile(rsk68_weight_volatility_short,22))` 904/0/0.74；`rank(ts_backfill(ts_sum(ts_delay(rsk68_residual_return,20),200),250))` 911/0/0.85；`trade_when(rsk68_weight_dadv>ts_mean(...),rank(-rsk68...))` 898/0/0.86；`rank(ts_backfill(-ts_std_dev(rsk68_beta,60),250))` 832/0/0.78；`rank(ts_backfill(-ts_delta(rsk68_weight_volatility_short,20),250))` 903/0/0.71；`rank(ts_backfill(divide(rsk68_weight_edadv,rsk68_weight_dadv),250))` 903/0/0.82；`group_rank(ts_backfill(-ts_quantile(rsk68_beta,252),250),industry)` 787/0/0.75；`rank(ts_backfill(-log(rsk68_weight_edadv),250))` 904/0/0.79。
  - `... AND short_count=0 AND long_count=0` ⇒ **0 行**（无双边同零）。
  - `expressions WHERE region='GBR' AND expression LIKE '%<f>%' AND sharpe IS NOT NULL` 字段使用计数（子串 LIKE）：`residual_return` 91 / `beta` 26 / `volatility_short` 12 / `weight_dadv` 13 / `weight_edadv` 6。
  - `backtest_results WHERE dataset='risk68' AND region='GBR'` ⇒ **16 行**（其余按 code 命中、dataset 标签为 NULL/复合）。
  - `vec_avg` + rsk68：GBR expressions 0 / backtest_results 0（历史未跑过 vec_avg 形态）。
  - ⚠ 复核更正：早期 md 曾写「GBR 91 条回测、2 条 sc=0、dataset=risk68 0 行」、当日早版写「99 条/6 条 sc=0/8 行」——本轮实拉为 **107 条、13 条 sc=0、dataset=risk68 16 行**，已按本轮读数更正（live DB 持续新增，读数随时间递增属正常）。

---

## 9. 小结

risk68 = 5 字段全 MATRIX 的**风险模型/流动性权重**面板（2026-07-01 同批 onboard，risk 塔 ×1.3）。平台 cov 全 0 是 GBR 盲区；GBR 107 条回测（lc 316–911、sc 0–569、both0=0、max S=1.82）证明数据真实存在，**不可 `excluded`**（无 lc/sc 双边同零的数据层实测）；判 `needs_probe`，用 v11 逐字段 type 生成的 MATRIX 原生 NONE 探针确认配置伪影 vs 真信号。`residual_return`(αC367) 是主力信号腿、`weight_volatility_short` 可作波动率归一、`weight_dadv`/`edadv` 是美元额流动性权重（须 rank/log 去量纲、勿当独立腿）；全 MATRIX **不得套 `vec_avg`**、禁跨族裸水平混腿。`density=dense`（日更面板、覆盖稳定）。
