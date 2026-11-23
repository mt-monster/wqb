# GBR / institutions25（Fund Short Selling Data，机构做空行为面板，全 VECTOR）

> 塔：**institutions**（GBR/D1 乘数 **1.4**）
> 画像日期 2026-11-19 · 数据源 `mcp__wq-brain-http__get_datafields`（GBR/TOP700/D1，`filter_sharpe=false`，不传 `max_fields`）
> 本轮实拉：`count=24` / `platform_count=24` / `returned=24` / `complete=true` / `pages_fetched=1` ⇒ 单页全量，去重字段数=平台声明数=24，**无需前缀 search 分片**。
> ⚠ 字段 id 及全部读数取本轮平台实拉，**未引用**任何审计缓存 / 历史 md 快照（平台会改目录，如 `herfindahl_index_holdings`→`herfindahl_index_transactions`）。对照发现 DB `get_field_catalog`（旧快照）αC/uC 与平台不符（例 `concentration` DB αC=1 vs 平台 3、`position_change` DB 11 vs 平台 14、`total_short_interest` DB 0 vs 平台 6），本档案一律以平台实拉为准。
> ⚠ 全部 24 字段 `coverage=0.0` 是 **GBR coverage 元数据已知盲区**，不等于无数据（见 §5 可用性三分 + §7 v8 判据）。
> ⚠ v11 逐字段 type 生成探针：本集全 24 字段为 VECTOR，探针一律 `rank(ts_backfill(vec_avg(f),250))`（须先 `vec_avg` 折叠）；不得套 MATRIX 原生 `rank(ts_backfill(f,250))`（VECTOR 未折叠类型不匹配必 FAIL）。

---

## 字段全表

> 平台实拉 24/24，按 alphaCount 降序（同 αC 按 userCount 降序）。第一列 = 平台真实字段 id（反引号）；cov = 平台 coverage 元数据（GBR 全 0，盲区）；αC = alphaCount；uC = userCount。全部 type=VECTOR、dateCreated=`2026-07-01`、pyramidMultiplier=1.4。

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `inst25_position_change` | VECTOR | 0.0 | 14 | 12 | 经理做空仓位相对上一 Position Date 的变化（占流通股 %）；本集 αC/uC 双料最高 |
| `inst25_sentiment` | VECTOR | 0.0 | 14 | 11 | 做空程度评分 0–100（基于总空头利息，相对全市场） |
| `inst25_age` | VECTOR | 0.0 | 9 | 7 | 空仓「年龄」排名 0–100（按平均空头持仓时长，越高越老） |
| `inst25_security_cover_count` | VECTOR | 0.0 | 9 | 7 | 该股在指定 position date 的平空交易笔数 |
| `inst25_security_trade_count_1mo` | VECTOR | 0.0 | 9 | 3 | 该股过去一个月的交易笔数 |
| `inst25_manager_avg_trade_length` | VECTOR | 0.0 | 7 | 7 | 经理在当日全部已平空仓的平均持仓时长（工作日） |
| `inst25_security_short_count` | VECTOR | 0.0 | 6 | 5 | 该股在指定日的卖空交易笔数 |
| `inst25_total_short_interest` | VECTOR | 0.0 | 6 | 5 | 总空头利息（占流通股 %），跨全部经理加总 |
| `inst25_trade_length` | VECTOR | 0.0 | 6 | 6 | 自开仓日的工作日数（持仓时长） |
| `inst25_activity` | VECTOR | 0.0 | 5 | 5 | 活跃度评分 0–100（相对其他证券的交易笔数） |
| `inst25_manager_position_count` | VECTOR | 0.0 | 5 | 3 | 经理组合在某日的空头仓位数 |
| `inst25_entry_position` | VECTOR | 0.0 | 4 | 4 | 经理开仓时空仓大小（占流通股 %） |
| `inst25_is_open` | VECTOR | 0.0 | 4 | 3 | 仓位是否仍开放（1=open，0=closed） |
| `inst25_position` | VECTOR | 0.0 | 4 | 4 | 经理当前申报的空仓（占流通股 %） |
| `inst25_security_trade_count` | VECTOR | 0.0 | 4 | 4 | 该股在指定日的交易笔数 |
| `inst25_security_trade_count_3mo` | VECTOR | 0.0 | 4 | 4 | 该股过去三个月交易笔数 |
| `inst25_concentration` | VECTOR | 0.0 | 3 | 2 | 前三大空仓占流通股 % 之和（position date） |
| `inst25_crowding` | VECTOR | 0.0 | 3 | 2 | 拥挤度评分 0–100（同时做空的经理多寡，越高越拥挤） |
| `inst25_manager_count` | VECTOR | 0.0 | 3 | 3 | 该股当日未平空仓的经理数（不同经理） |
| `inst25_security_avg_trade_length` | VECTOR | 0.0 | 3 | 3 | 该股当日全部未平空仓的平均持仓天数 |
| `inst25_security_trade_count_1wk` | VECTOR | 0.0 | 1 | 1 | 该股过去一周交易笔数 |
| `inst25_security_trade_count_1yr` | VECTOR | 0.0 | 1 | 1 | 该股过去一年交易笔数 |
| `inst25_security_trade_count_2yr` | VECTOR | 0.0 | 0 | 0 | 该股过去两年截至 position date 的交易笔数 |
| `inst25_security_trade_count_3yr` | VECTOR | 0.0 | 0 | 0 | 该股过去三年交易笔数 |

> 平台实拉 αC 逐行：14,14,9,9,9,7,6,6,6,5,5,4,4,4,4,4,3,3,3,3,1,1,0,0（合计 124，均值 5.17）。
> 平台实拉 uC 逐行：12,11,7,7,3,7,5,5,6,5,3,4,3,4,4,4,2,2,3,3,1,1,0,0（合计 102，均值 4.25）。

---

## 3. 聚合统计（基于平台实拉读数）

| 指标 | 值 |
|---|---|
| 字段总数 | 24（全部 VECTOR，无 MATRIX/GROUP） |
| coverage 分布 | 24/24 = 0.0（GBR 元数据盲区，非无数据） |
| alphaCount 合计 / 均值 | 124 / **5.17** |
| alphaCount 最大 / 最小 | 14（`position_change`、`sentiment`）/ 0（`security_trade_count_2yr`、`_3yr`） |
| userCount 合计 / 均值 | 102 / **4.25** |
| userCount 最大 / 最小 | 12（`position_change`）/ 0（`security_trade_count_2yr`、`_3yr`） |
| dateCreated | 24/24 = `2026-07-01`（同批 onboard，蓝海程度一致；非老集死字段） |
| pyramidMultiplier | 24/24 = 1.4（institutions 塔，GBR/D1 未点亮） |
| αC=0 的字段 | 2 个（均为超长窗计数 `_2yr`/`_3yr`，冷门但非死字段——同批 2026-07 onboard） |

数据集级元数据（本轮 `get_datasets(region=GBR,universe=TOP700,delay=1,search=institutions25)` 实拉）：`id=institutions25` / `name=Fund Short Selling Data` / `category=institutions` / `fieldCount=24` / `coverage=0.0`（同盲区）/ `userCount=59` / `alphaCount=103` / `valueScore=5.0` / `pyramidMultiplier=1.4`。字段级 description 与数据集描述一致（对冲基金/资管做空持仓日频情报），无错配。

---

## 4. 字段族拆解（按经济机制分组）

| 族 | 字段 | 读数 / 机制 |
|---|---|---|
| **A 做空强度/情绪族**（信号主力） | `inst25_sentiment`(αC14)、`inst25_total_short_interest`(6)、`inst25_crowding`(3)、`inst25_concentration`(3) | 做空程度/总空头利息/拥挤/集中，0–100 评分或占流通股 %；`sentiment` 是全集并列最高 αC |
| **B 仓位流族**（变化量/水平） | `inst25_position_change`(**αC14**)、`inst25_position`(4)、`inst25_entry_position`(4)、`inst25_is_open`(4) | 经理空仓变化/水平/开仓规模/是否开放；`position_change` 是全集 αC/uC 双料最高、实测单腿/组合主力 |
| **C 持仓时长族** | `inst25_age`(9)、`inst25_manager_avg_trade_length`(7)、`inst25_trade_length`(6)、`inst25_security_avg_trade_length`(3) | 空仓年龄/持仓天数/经理均值/证券均值，工作日计；慢变量 |
| **D 交易计数族（当日/滚动窗）** | `inst25_security_trade_count`(4)、`_1wk`(1)、`_1mo`(9)、`_3mo`(4)、`_1yr`(1)、`_2yr`(0)、`_3yr`(0) | 同族不同回看窗；`_1mo` αC9 最活，超长窗 `_2yr/_3yr` αC0 |
| **E 买卖方向计数族** | `inst25_security_cover_count`(9)、`inst25_security_short_count`(6) | 平空笔数 / 卖空笔数，可构造 cover/short 比值；`cover_count` αC9 是该族最活 |
| **F 经理广度族** | `inst25_manager_count`(3)、`inst25_manager_position_count`(5) | 做空经理数 / 经理组合仓位数 |
| **G 活跃度评分族** | `inst25_activity`(5) | 0–100 相对交易活跃度评分（基于交易笔数） |

**族间关系**：A/B/G 是价格无关的「机构做空行为」信号主力；C 是慢变时长；D/E 是流量计数（高换手风险）；F 是广度。本集与 `institutions6`（13F 多头披露，MATRIX 季频）**经济机制不同**——institutions25 是**做空侧**行为、日频 VECTOR，不可直接迁移 13F 模板。DB 实测最高 S=1.26 的组合为 `reverse(group_rank(ts_zscore(ts_backfill(vec_avg(inst25_crowding),66),126),...))` 与 `vec_sum(inst25_position_change)` 的跨族组合（见 §7）。

---

## 5. 可用性三分（信号 / 计数需归一 / 元数据不可用）

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可直接做信号**（有界评分/变化率/占比，折叠后即可 rank） | `activity`、`sentiment`、`crowding`、`concentration`、`age`、`total_short_interest`、`position`、`entry_position`、`position_change` | 0–100 有界评分或占流通股 %；平台实拉 αC 多为 3–14；`position_change` 组合实测 S 达 1.15（见 §7） |
| **② 计数需归一**（原始笔数/家数/天数，量纲 10⁰–10³） | `security_trade_count`+`_1wk/_1mo/_3mo/_1yr/_2yr/_3yr`、`security_short_count`、`security_cover_count`、`manager_count`、`manager_position_count`、`security_avg_trade_length`、`manager_avg_trade_length`、`trade_length` | 裸计数必须先 `vec_sum`（总量）/`vec_avg`（均值）折叠，再 `rank`/`group_rank`/`ts_zscore` 去量纲 |
| **②b 哑变量/门控** | `is_open` | 0/1 哑变量，仅作门控/分组/过滤，不作连续信号 |
| **③ 元数据不可用**（coverage 盲区，非数据缺失） | 全部 24 字段的 `coverage=0.0` | GBR 已知盲区；DB 本轮实测 61 条 GBR `code LIKE '%inst25%'` 回测 `long_count` 17–701、`both0=0`，证明有数据 ⇒ 不可据此判无数据/判死 |

---

## 6. 六法评测

| 法 | 结论 |
|---|---|
| **① 覆盖率** | 平台 `cov=0.0`（24/24）—— **GBR 元数据盲区**，非真实覆盖率。实证：本轮只读 DB 实测 GBR 61 条 `code LIKE '%inst25%'` 回测，`long_count` 17–701、`short_count` 0–701，**61/61 `long_count>0`、`both0=0`**，实际可用覆盖充足且稳定 ⇒ `density=dense`。 |
| **② 非零率** | 无法从 `cov=0` 元数据直接读；从回测反推：61 条回测中 50 条产生双边持仓（lc>0 且 sc>0）、11 条 `sc=0`（lc 均 17–389，为裸 `rank`/`vec_avg`/`vec_sum` 探针伪影），证实非零率高。评分类（activity/sentiment/crowding/age）0–100 相对排名、正负可期；占比类（position/entry_position/total_short_interest）恒正；计数类恒正。 |
| **③ 更新频率** | 全部 `dateCreated=2026-07-01`（同批新 onboard）；字段语义为 position-date 驱动 + 固定滚动窗（1wk/1mo/3mo/1yr/2yr/3yr）⇒ **日更面板**（非一次性事件）⇒ `density=dense`（日更 cov 稳）。 |
| **④ 分布形态** | 评分类（activity/sentiment/crowding/age）0–100 有界、相对排名型；占比类（position/entry_position/total_short_interest/concentration）为 % of shares outstanding（0–1 量纲）；计数类（`*_count`/`*_length`）右偏长尾 10⁰–10³，需 `rank`/`log` 压尾；`is_open` 为 0/1 二值。 |
| **⑤ VECTOR 折叠要求** | **全 24 字段为 VECTOR，必须先折叠**：`vec_avg`(均值)/`vec_sum`(求和) 才能进 `rank`/`ts_*`/`group_*`。计数族用 `vec_sum`（总量）、评分/占比族用 `vec_avg`（均值）更贴语义。本轮 `validate_expressions` 对 24 条 `vec_avg` 形态探针全部通过（分 4 批各 6/6/6/9，`valid=true`、`unknown_fields=[]`、`platform_field_count`=批次大小）；`vec_sum` 形态的 9 条计数探针亦全部通过。裸字段入式类型不匹配，必先 `vec_*`。 |
| **⑥ 量纲陷阱** | 三类量纲混在一集：评分 0–100（activity/sentiment/crowding/age）、占比 % of shares outstanding（position/entry_position/total_short_interest/concentration）、原始计数 10⁰–10³（`*_count`/`*_length`）⇒ **禁裸水平入式、禁跨族 `add` 混腿**。`is_open` 是 0/1 哑变量。统一 `vec_*` 折叠 + `rank`/`group_rank` 去量纲后再组合。 |

---

## 7. GBR v8 判据核验（cov 全 0 为何不判 excluded）

1. **排除规则原文**：cov 全 0 不得直接 `excluded`——techindi_model(399)/insiders12(74%)/analyst15(533) 均 cov=0 却有数据。cov 全 0 ⇒ `needs_probe` + NONE 探针；只有波次档案有 `lc/sc=0` 实测才可 `excluded`。
2. **本集实测反证**（本轮只读 DB 实测，命令见 §8）：GBR `backtest_results` 中 `code LIKE '%inst25%'` 的 **61 条**回测，`long_count` 17–701、`short_count` 0–701，**61/61 `long_count>0`、`both0=0`（无双边同零）**。最高 S=1.26、S>0 共 36 条——证明 VECTOR 折叠后数据真实存在，`excluded` 条件不成立。
3. **11 条 `sc=0` 的真相**：全部是 NONE 裸探针（`rank(ts_backfill(vec_avg(inst25_activity),250))` lc389、S0.55；`vec_avg(inst25_concentration)` lc255；`vec_sum(inst25_activity)` lc253；`vec_avg(inst25_crowding)` lc253；`vec_sum(inst25_security_cover_count)` lc17…）。`rank()`/`vec_*` 裸探针输出恒为正 → 引擎只建长仓 → `sc=0` 是**配置层长仓伪影**，不是无数据。同一批字段加 `group_rank(...sector)` 后立即出现双边持仓（如 `reverse(group_rank(ts_mean(vec_avg(inst25_age),66),sector))` lc609/sc300、S0.98）。⇒ 非数据层排除。
4. **波次档案旧判词**：早期档案记「institutions 塔判弱」（单腿 NONE 探针 max |S| 低）——但那是**旧配置/旧假设**下的裸探针；本轮 DB 已有 `group_rank` + 跨族组合做到 S1.26/1.19/1.15，按 v8「判死不得单一依据」，旧档案不足以 `excluded`。
5. **结论**：`verdict=needs_probe`，按 v11 逐字段 type 生成 NONE 探针。本集全 24 字段 VECTOR ⇒ 一律 `rank(ts_backfill(vec_avg(f),250))` @neutralization=NONE（须 `vec_avg` 折叠，不得用 MATRIX 原生形态）。

### NONE 探针（v11 逐字段 type 生成，neutralization=NONE）

全部 24 字段 type=VECTOR ⇒ 模板 `rank(ts_backfill(vec_avg(f),250))`（必须先 `vec_avg` 折叠）：

- `rank(ts_backfill(vec_avg(inst25_position_change),250))`
- `rank(ts_backfill(vec_avg(inst25_sentiment),250))`
- `rank(ts_backfill(vec_avg(inst25_age),250))`
- `rank(ts_backfill(vec_avg(inst25_security_cover_count),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count_1mo),250))`
- `rank(ts_backfill(vec_avg(inst25_manager_avg_trade_length),250))`
- `rank(ts_backfill(vec_avg(inst25_security_short_count),250))`
- `rank(ts_backfill(vec_avg(inst25_total_short_interest),250))`
- `rank(ts_backfill(vec_avg(inst25_trade_length),250))`
- `rank(ts_backfill(vec_avg(inst25_activity),250))`
- `rank(ts_backfill(vec_avg(inst25_manager_position_count),250))`
- `rank(ts_backfill(vec_avg(inst25_entry_position),250))`
- `rank(ts_backfill(vec_avg(inst25_is_open),250))`
- `rank(ts_backfill(vec_avg(inst25_position),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count_3mo),250))`
- `rank(ts_backfill(vec_avg(inst25_concentration),250))`
- `rank(ts_backfill(vec_avg(inst25_crowding),250))`
- `rank(ts_backfill(vec_avg(inst25_manager_count),250))`
- `rank(ts_backfill(vec_avg(inst25_security_avg_trade_length),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count_1wk),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count_1yr),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count_2yr),250))`
- `rank(ts_backfill(vec_avg(inst25_security_trade_count_3yr),250))`

> ⚠ **VECTOR trap 注**：`vec_avg` 是 VECTOR 折叠算子，本集全 VECTOR 必须套用；反过来 **不得**把 MATRIX 原生形态 `rank(ts_backfill(f,250))` 套在 VECTOR 上（未折叠类型不匹配必 FAIL，与 risk68 全 MATRIX 集的情况恰好相反）。本轮 `validate_expressions` 对上列 24 条全部通过。不得因某探针 `sc=0` 判字段死——11 条 `sc=0` 行 `lc` 均 >0，属配置层伪影。

---

## 8. 本轮实测命令与读数（可复核）

- 平台全量：`get_datafields(region=GBR,dataset_id=institutions25,universe=TOP700,delay=1,filter_sharpe=false,不传max_fields)` ⇒ `count=24 / platform_count=24 / returned=24 / complete=true / pages_fetched=1`；24 行 id/type/cov/αC/uC/dateCreated/pyramidMultiplier 见 §字段全表。
- 数据集元数据：`get_datasets(region=GBR,universe=TOP700,delay=1,search=institutions25)` ⇒ `fieldCount=24 / alphaCount=103 / userCount=59 / coverage=0.0 / valueScore=5.0 / pyramidMultiplier=1.4`。
- 快照对照：`get_field_catalog(region=GBR,dataset=institutions25)` 为旧快照（αC/uC 与平台不符），本档案一律取平台实拉。
- 探针校验：`validate_expressions(alpha_expressions=[24 条 VECTOR vec_avg 探针],region=GBR,universe=TOP700,delay=1)` 分 4 批（6/6/6/6）+ 计数族 `vec_sum` 9 条，全部 `valid=true`、`unknown_fields=[]`、`unknown_soft=[]`、`builtin_fields=[]`、`fields_checked`=批次 24 字段全覆盖。
- DB 读数（只读 `data/wqb.db`，`mode=ro` URI，本轮实跑 `python logs/_tmp_inst25_profile_db.py`，2026-11-19）：
  - `SELECT ... FROM backtest_results WHERE region='GBR' AND code LIKE '%inst25%'` ⇒ **61 行**；`lc 17–701 / sc 0–701 / both0=0 / sc=0 共 11 行 / sharpe>0 共 36 行 / max sharpe=1.26 / lc>0 共 61 行`。
  - top S：`crowding`+`position_change` 跨族组合 S=1.26(lc531/sc378)、1.19(527/383)、`position_change` 组合 1.15(519/391)、`reverse(group_rank(ts_mean(vec_avg(inst25_age),66),sector))` 0.98(609/300)。
  - 11 条 `sc=0` 行（sharpe,lc,sc,code 前缀）：0.55/389/0 `rank(ts_backfill(vec_avg(inst25_activity),250))`；0.47/255/0 `vec_avg(inst25_concentration)`；0.53/254/0 `ts_zscore(vec_sum(inst25_activity),66)!=0`；0.52/253/0 `divide(vec_sum(inst25_activity),vec_sum(inst25_activity))`；0.37/253/0 `vec_sum(inst25_activity)`；0.47/253/0 `vec_avg(inst25_activity)`；0.48/253/0 `vec_avg(inst25_crowding)`；0.51/216/0 `ts_zscore(vec_sum(inst25_concentration),22)!=0`；0.49/164/0 `ts_zscore(vec_sum(inst25_position_change),22)!=0`；0.23/34/0 `divide(vec_sum(inst25_position_change),...)`；0.21/17/0 `vec_sum(inst25_security_cover_count)`——全为裸探针长仓伪影。
  - `backtest_results WHERE region='GBR' AND dataset='institutions25'` ⇒ **0 行**（本集历史回测按 code 命中、dataset 标签为 NULL/复合，与 risk68 同类现象）。
  - 表达式使用计数（GBR `code LIKE '%inst25_<f>%' AND sharpe IS NOT NULL`）：`activity` 18 / `position` 13 / `position_change` 13 / `concentration` 7 / `total_short_interest` 6 / `crowding` 5 / `security_cover_count` 5 / `security_short_count` 4 / `age` 3 / `security_avg_trade_length` 2 / `sentiment` 2 / `is_open` 1 / `manager_avg_trade_length` 1 / `manager_count` 1 / `security_trade_count` 1 / `_1mo` 1 / `_1wk` 1 / `entry_position` 0 / `manager_position_count` 0 / `_1yr` 0 / `_2yr` 0 / `_3mo` 0 / `_3yr` 0 / `trade_length` 0。
  - ⚠ 本轮实时读数为 61 行（早期档案记 53/86 行，live DB 持续变化，以本轮为准）。

---

## 9. 小结

institutions25 = 24 字段全 VECTOR 的**做空侧机构行为**面板（2026-07-01 同批 onboard，institutions 塔 ×1.4）。平台 cov 全 0 是 GBR 盲区；GBR 本轮 61 条回测（lc 17–701、sc 0–701、both0=0、max S=1.26）证明数据真实存在，**不可 `excluded`**（无 lc/sc 双边同零的数据层实测）；判 `needs_probe`，用 v11 逐字段 type 生成的 24 条 VECTOR `vec_avg` NONE 探针确认配置伪影 vs 真信号。`position_change`/`sentiment`(αC14) 是主力信号腿，`crowding`/`age` 组合实测 S 达 1.26/0.98；全 VECTOR **必须 `vec_avg`/`vec_sum` 折叠**（不得套 MATRIX 原生形态）、统一 `rank` 去量纲、禁跨族裸水平混腿。`density=dense`（日更面板、覆盖稳定）。

---

## 11. 2026-11-21 · 纯 ATOM 配置档网格 + 同集双字段组合（用户「ATOM 优先」指令）

> 前置裁定：历史最优 S1.26（MPYNLJ5k 等）都是 **FAST 档 + 跨集 add**（`loaned_share_count_main` / `transaction_count_main` 属已点亮 shortinterest 塔）⇒ **不是 ATOM、且违反已亮塔红线**，不能作为交付依据。本节只测**纯 inst25 单腿 + 同集字段**。

### 网格（4 批 10 臂，表达式固定 2 条最优内核）

| 批 | 设置档 | 表达式内核 | S | F | 2Y | TO | RA |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | **INDUSTRY** | quantile 内核 | 0.94 | 0.52 | 0.42 | 14.5% | 3 |
| 1 | INDUSTRY | av_diff 内核 | 0.95 | 0.53 | 0.40 | 13.8% | 3 |
| 2 | **SECTOR** | quantile | 0.76 | 0.41 | 0.16 | 13.3% | 3 |
| 2 | SECTOR | av_diff | 0.77 | 0.42 | 0.12 | 12.7% | 3 |
| 3 | **FAST** | quantile | **1.10** | 0.47 | 0.44 | 20.7% | 3 |
| 3 | FAST | av_diff | 1.09 | 0.47 | 0.39 | 19.8% | 3 |
| 4 | SUBINDUSTRY | `add(crowding, position_change)` | 0.61 | 0.31 | 0.49 | 11.8% | 3 |
| 4 | SUBINDUSTRY | `multiply(crowding, position_change)` | **−0.40** | −0.13 | −0.72 | 22.2% | 4 |
| 4 | SUBINDUSTRY | `add(crowding, sentiment)` | 0.56 | 0.27 | 0.26 | 10.1% | 3 |
| 4 | SUBINDUSTRY | `add(position_change, sentiment)` | 0.58 | 0.29 | 0.36 | 8.8% | 3 |

> 内核 = `reverse(group_rank(vector_neut(ts_quantile(vec_sum(inst25_position_change),66), ts_backfill(vec_sum(inst25_crowding),66)), industry))`（quantile 版）/ `ts_av_diff` 版。

### 结论：纯 inst25 ATOM 面收敛（PROVISIONAL，不判死）

1. **单腿各档天花板**：**FAST 1.10**（本轮新高，略超 SUBINDUSTRY 历史 1.08）> SUBINDUSTRY 1.08 > INDUSTRY 0.95 > SECTOR 0.77 > MARKET 0.70 > STATISTICAL 0.57 > CROWDING 0.03。
2. **同集双字段组合劣于单腿**：`add` 两腿稀释到 0.56–0.61（crowding 与 position_change 同向但信息重叠）；`multiply` 反号 −0.40（乘法复合误杀空头端，与论坛「乘法门控误杀」实证同源）。
3. **结构判定**：24/24 字段已进回测 × 7 个中性化档 × 单腿/双字段组合均 ≤1.10，距 S 闸 1.58 差 **0.48**⇒ **该集在 GBR 当前几何与配置下无 S≥1.58 的 ATOM 形态**。
4. **不判死**（用户红线「轻易不判死」）：这是 **ATOM 面收敛（PROVISIONAL）**，不是数据集死——24 字段跨 3 个机制族（持仓变化/拥挤度/情绪），未来若出现新几何或作为**辅助腿**（条件/分组/残差式入场，见 §7.7 允许清单）仍有价值；历史 S1.26 已证明它在跨集组合里能贡献边际。
5. **交付结论**：inst25 不产出 tar 闸 ATOM 件；institutions 塔的席位仍靠 institutions1（ZYaQdNO1 已 ACTIVE 1/3）。

---

## 12. 2026-11-21 · 完整梯度终态（5 层 68 臂，GRADIENT_DONE）

> 背景：用户质询「institutions25 有无经过完整的梯度流程」⇒ 核实为**未做**（§11 只是设置档网格 + 同集双字段，不是 5 层全类别梯度）⇒ 本轮补做。档案：`tracking/GBR/waves/wave20261121_gradient_institutions25.md`

| 层 | 覆盖 | 最优 | 关键读数 |
|---|---|---|---|
| §7.10.0 体检 | 2 探针 | — | **2014–2023 十年均有 lc/pnl**（2014 lc295 → 2023 lc305）⇒ 窗口合格 |
| **L1 信号构造** | 23 臂 / **24/24 字段** | `reverse(activity)` | **23/23 全为负 S（−0.38~−0.96）⇒ 全族统一反向**；镜像后 activity 0.82 / manager_avg_trade_length 0.71 / entry_position 0.64 |
| **L2 内核** | 16 臂（15/16 可测） | **`ts_rank`**（S0.81 / 2Y+0.22） | 无内核超 ts_zscore 0.82；ts_rank 以 S−0.01 换 2Y+0.27；ts_product/days_from_last_change 反转后仍负 |
| **L2b 窗口** | 4 臂 | **窗 66**（S0.86/2Y0.32） | ΔS+0.05；250/504/750 同档 0.79–0.81 |
| **L3 轴** | 6 臂 | **`subindustry`**（S0.88/2Y0.54） | 细轴 2Y 最高（与 imb5「粗轴好」相反 ⇒ 按族实测）；market≡exchange≡country 逐位相同 |
| **L4 外包** | 7 臂 | `group_rank`（S0.88） | **全 ΔS 负**；group_scale/zscore 把 2Y 抬到 0.95–0.98 但 S 崩到 0.51–0.55、TO 翻倍 51% |
| **L5 设置** | 8 臂（4 档×2 轴）+ 4 臂重扫 | **`FAST`**（S1.01，ΔS+0.13） | INDUSTRY 0.79–0.81 / SECTOR 0.64–0.66 / decay8 0.77–0.80（但 F0.43/TO12.4% 是内部严线最优）；L5-R 内核重扫确认 **ts_rank 仍最优** |

**终态（可写死）**：
- **纯 ATOM 天花板 = S1.01 / F0.37 / 2Y0.30 / TO23.7%**（FAST × `group_rank(ts_rank(ts_backfill(vec_avg(inst25_activity),250),66), industry)` × reverse），**距 S 闸 0.57 / F 闸 0.63 / 2Y 闸 1.28**。
- 备选：SUBINDUSTRY 基线（S0.88 / F0.39 / **2Y0.54** / TO19.8%）；decay8（S0.80 / F0.43 / TO12.4%）。
- **判据升级**：D1–D6 六维全部有实测（结构互异模板 20+ / 24/24 字段 / 矩与水平比 / 轴 6 / 非线性 rank+quantile / 配置 5 档）⇒ **天花板从 PROVISIONAL 升级为可写死**；`gradient_gate` = **GRADIENT_DONE**（dom=24 / arc_layers=7 / arc_rows=9）。
- **不判死**：信号层强度不足（非数据集死），按 §7.7 仍可作辅助腿（条件/分组/残差式入场）。
- 与 §11 历史网格的一致性：历史 FAST 1.10 ≈ 本轮 FAST 1.01（差异来自内核/构造不同），**完整梯度独立复现了 ATOM 天花板 ~1.0**。

---

## 13. 2026-11-22 · 模板穷尽终判（**23 个互异模板 × 完整 5 层梯度 + L5-R，~740 臂**）

> 背景：用户指令「**ATOM 并没有穷尽，只是对当时用的模板穷尽了**，那就再换一个模板持续做梯度，且换了模板之后要做完整的梯度流程」⇒ §12 的 1.01 只是**模板 A 的**天花板，不是数据集天花板。本轮把 L1 里 23 条互异构造（单字段水平 / 计数窗 6 种 / 比值 2 种 / 残差组合 / 方向比）**逐条跑完各自完整 5 层 + L5-R**。

### 23 模板天花板全表

| 模板 | 构造 | 天花板 S | F | 2Y | 终态形态 |
|---|---|---:|---:|---:|---|
| **C** | `position_change ⊖ crowding` 同集残差组合 | **1.26** | 0.61 | 0.58 | FAST × ts_delta126 × industry |
| **P** | `security_trade_count_3yr` | **1.23** | **0.71** | **1.93** | FAST × **group_scale** × ts_av_diff250 × subindustry |
| F | `position_change` 单腿 | 1.08 | — | — | FAST |
| E | `age` | 1.04 | — | — | FAST |
| A | `activity` | 1.01 | 0.37 | 0.30 | FAST × ts_rank66 × subindustry |
| M | `is_open` | 1.01 | 0.53 | 0.04 | FAST × ts_delta250 × market |
| D | `entry_position` | 0.99 | — | — | FAST |
| B | `vec_sum(position_change)` | 0.97 | — | — | FAST |
| J | `security_trade_count_1wk` | 0.96 | 0.51 | 0.54 | FAST × ts_std_dev504 |
| Q | `manager_count` | 0.95 | 0.47 | 0.14 | FAST × ts_sum250 × industry |
| S | `sentiment` | 0.93 | 0.56 | 0.48 | 基线 × ts_ir66 × industry |
| G / H / I / N / T | concentration / trade_length / avg_trade_length / crowding / TSI | 0.90 | 0.42–0.57 | −0.07–0.54 | 各族 |
| L | `position` | 0.89 | 0.53 | 0.39 | 基线 |
| O | `security_trade_count_2yr` | 0.85 | 0.40 | 0.28 | FAST × ts_mean126 × market |
| U | `security_trade_count_3mo` | 0.82 | 0.50 | 0.39 | decay8 × ts_std_dev66 |
| K / R / V | 当日计数 / manager_position_count / `divide(1mo,1yr)` | 0.80 | 0.39–0.42 | 0.25–**0.79** | 各族 |
| W | `divide(cover, short)` | 0.78 | 0.44 | **0.74** | 基线 × ts_arg_min504 × industry |

### 终判

- **S 天花板 = 1.26（模板 C）**；**2Y 天花板 = 1.93（模板 P，唯一越过 2Y 闸 1.58 的形态）**。
- **交付 = 0 颗**：C 卡 2Y（0.58，差 1.00）+ F（0.61，差 0.39）；P 卡 S（1.23，差 0.35）+ F（0.71，差 0.29）。
- ★★ **本数据集最深的结构性结论：S 与 2Y 系统性互斥**。C（S1.26/2Y0.58）从 S 侧、P（S1.23/2Y1.93）从 2Y 侧各自逼近，但**无模板同时满足 S≥1.58 ∧ 2Y≥1.58**。
- ★ **V/W 证明互斥不是绝对的**：序数型内核（`ts_arg_max` / `ts_arg_min`）给出 **2Y/S ≈ 0.95–0.99**（V 0.80/0.79、W 0.78/0.74）——**跷跷板被消掉，但绝对强度只有 0.78–0.80**。这是「要么强但不稳、要么稳但不强」的量化证据。
- **状态**：ATOM 面穷尽 + S 层弱 ⇒ **不判死**（用户 2026-11-19 明令「轻易不判死」）。**可用价值 = 跨集第二腿**：P（2Y1.93）、V/W（2Y 稳健、TO 3–4%）适合做 regular 组合的 2Y 稳定腿，不作单集主信号。
- **梯度验收**：`gradient_gate` = GRADIENT_DONE（23 模板 / 每模板 ≥5 层 / L5-R 全跑）。
- **方法论沉淀**（可迁移到其它数据集）：① 内核算子**按族且按窗口长度**选（D 计数族四个窗各有不同冠军）；② **外层算子与「内核是否已无量纲」强耦合**——ts_ir / ts_arg_* / divide 型只能用 `group_rank`，纯水平型才可换 `group_scale`（P 是唯一成功案例：+0.10S / +0.95 2Y）；③ 设置档不是普遍杠杆——**差分/波动型内核吃 FAST，水平/序数型内核吃基线或 decay8**；④ 5 次内核翻转全部发生在换设置基线之后 ⇒ **L5-R 必做**。
