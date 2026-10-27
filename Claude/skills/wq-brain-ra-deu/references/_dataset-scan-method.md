# 数据集扫描与探查方法（区域通用）

> 来源：2026-10-23 EUR 全池战役（169 集 / ~1700 条仿真）＋ 2026-10 DEU 32 波实证。
> 定位：**字段级探针 SOP（[_probe-sop.md](_probe-sop.md)）的前一层**。
> 探针 SOP 回答「这个字段强不强」，本文回答「**下一步该开哪个数据集**」。
> 顺序颠倒 = 在已经挖完的类目上空转（EUR 2026-10-23 实测代价：一整轮 category 轮转 0 产出）。

---

## 0 为什么必须先做数据集级扫描（EUR 反例）

EUR 画像池 178 个集（可挖 169 个）。按 `--priority-cats INSTITUTIONS,EARNINGS,INSIDERS,MACRO` 轮转，结果：

| 类目 | 池内集数 | 已跑完 | 结论 |
|---|---|---|---|
| INSTITUTIONS | 2 | 2 | 空 |
| EARNINGS | 2 | 2 | 空 |
| INSIDERS | 3 | 3 | 空 |
| MACRO | 1（macro10 仅 1 字段，被 `n_fields>=3` 滤掉） | 1 | 空 |

四类合计 **9 个集，全部跑完**。category 是**平台给的粗分类，不是开采进度**；
`dataset_profile` 里每个类别往往只有 1–3 个集，按类目轮转必然空转。

⇒ **选池的正确维度是「开采度」，不是「类目」。**

---

## 1 选池四档（顺序即优先级）

```
X  不可挖   n_fields < 3 ／ status=platform_empty ／ coverage 恰为 0
V  处女地   alpha_count <= 10 且 value_score >= 5
U  未点亮   我方该 category 已提交 <= 3
L  已点亮   我方该 category 已提交 > 3
```

### 1.1 ✗ `coverage == 0` 必须是「不可挖」，不是「覆盖低」

两者物理含义完全不同，混为一谈会浪费整批预算：

- `coverage = 0` ⇒ 该数据集**在这个 region × universe 里没有任何数据**。开批必然空跑。
- `coverage = 0.2~0.5` ⇒ 有数据但只覆盖部分股票，**可以挖**。

DEU/TOP500 实测：平台 92 个集里 **63 个 coverage = 0**（约 68%），可挖的只剩 29 个。
EUR/TOPCS1600 同理有一批。**这条不做，选池会多选一倍以上的废集。**

### 1.2 `alpha_count` 是唯一的「开采度」真值

平台 `alpha_count` = **全站**在该数据集上产出的 alpha 数（所有人，不只我们）。
与本地库实测完全一致（2026-10-23 EUR 逐集核对 13/13 相符）。

判据：`alpha_count <= 10 且 value_score >= 5` ⇒ 处女地。
`value_score` 是平台自带的价值评分（1–10），可当作「平台认为这块数据有没有料」的先验。

**EUR 处女地共性：覆盖率普遍低。** 这正是它们空着的原因 —— 不是没信号，是没人愿意处理脏数据。
典型：`equity_forum_data`（VS 6.0 / 全站 0 alpha / cov 0.41）、
`workforce_flow_skills`（VS 6.0 / 0 alpha / cov 0.25）、
`news_sentiment_dl`（VS 6.0 / 2 alpha / cov 0.76）。

### 1.3 覆盖率闸必须分两级

| 层级 | 作用 | 常规值 | 处女地值 |
|---|---|---|---|
| **数据集级** | 决定**要不要开这个集** | 0.8 | **0.35** |
| **字段级** | 决定**用哪些字段** | 0.6（DEU 实证值） | 0.6（不放宽） |

**不要用字段级门槛去筛数据集。** EUR 早期用集级 `avg_field_coverage >= 0.8` 一刀切，
把 21 个处女地整批判死；放宽到 0.35 后它们才进入队列。

DEU 的 `cov<0.6 剔除` 是**字段级**启发式（见 `_probe-sop.md` 第 0 步），
与本文的集级放宽**不冲突**：先按 0.35 决定开集，再按 0.6 选字段。

---

## 2 一键扫描

```bash
# ① 拉平台实时画像（必须；本地表 coverage 大量为 0/占位值）
#    MCP get_datasets(region=DEU, universe=TOP500, delay=1) 的 results 存成 JSON
$WQ_PY <skill>/scripts/dataset_scan.py --region DEU --from-json cache/deu_datasets.json \
        --out cache/deu_scan_ranked.json

# ② 只要处女地名单
$WQ_PY <skill>/scripts/dataset_scan.py --region DEU --from-json cache/deu_datasets.json --virgin-only

# ③ 离线退化模式（仅看结构，不要信 coverage）
$WQ_PY <skill>/scripts/dataset_scan.py --region DEU --db data/wqb.db
```

⚠ **离线模式会误判**：DEU `datasets` 表 193 行里 121 行的 `coverage` 为空/0，
`value_score` 大量写死为 10（占位）。用它选池会把 104 个集标成处女地（真值是 5 个）。
脚本在离线模式会打印告警；**选池一律走 `--from-json`。**

### DEU 2026-10-23 实扫基线（as_of：GET datasets DEU/TOP500/delay1）

| 档 | 数量 | 名单 |
|---|---|---|
| 总 | 92 | — |
| **X** | **63** | coverage=0，不开 |
| **V** | **5** | `other250`(0.61,cov充足) `other384`(0.21) `other699`(0.51) `other545`(0.53) `stock_cluster_dl`(0.45) |
| **U** | 20 | `institutions4` `insiders1` `insider_trx_matrix` `institutions1` `sentiment33` `other532` `other47` `fundamental45` `insider_matrix` `sentiment7` `fund_holdings_panel` `order_book_imbalance` `insider_agg_matrix` `other455` `institutions6` `sentiment27` `risk60` `shortinterest3` `dl_riskfree_returns` `fundamental6` |
| **L** | 4 | `pv109` `pv29` `pattern_scores`（PV 已点亮） |

⇒ DEU 的真实开局顺序：**5 个处女地 → 20 个未点亮 → 4 个已点亮**。

---

## 3 字段级扫描（选定集之后）

### 3.1 先拉全字段清单，再按语义归维度

**字段名不可作为语义依据，description 才是唯一依据。** 顺序固定：

1. `dump_ds_full.py` 拉平台真实字段名（本地画像有幽灵字段）
2. 按 description 归纳语义维度
3. 按 `alpha_count` 升序（同集内最冷门的字段优先）
4. 每维度取 1–2 个代表（覆盖率最高 + alpha_count 最低）
5. 画「字段 × 模板族」地图，再派批

反例（EUR 2026-10-23）：`rsk62_beta_1_100_mts` 光看名字像 level，description 写 momentum ⇒ 实为 change 型；
`rsk62_1_100_ksrs` 名字看不出含义，description 是 ratio ⇒ level_ratio。**靠名字推 = 选错模板。**

### 3.2 形态六分类 + 强模式清单

`change` / `level_ratio` / `event_date` / `count` / `discrete_rating` / `skip` / `other`

**先清 15 类样板噪声**（`"on the observation date"`、`"the value of"`、`"for the company"` …），
再只认强模式，否则整集误判：

| 形态 | 强模式（description 或字段名出现才算） |
|---|---|
| `discrete_rating` | cutpoint / threshold / percentile / quartile / decile / grade / rating / tier |
| `event_date` | **只认** `date of` / `announcement date` / `next earnings` / `days since` |
| `count` | `num_` / `_count` / `number of` |
| `change` | `change` / `delta` / `growth` / `momentum` / `revision` |

⚠ 裸 `date` / 裸 `rank` / 裸 `score` **会整集误判**：
- EUR `sentiment26` 的 description 普遍带 "on the observation date" ⇒ 裸 `date` 把整集判成 event_date，字段从 122 压到 16；
- `"domain rank distribution"` / `"attention breadth score"` ⇒ 裸 `rank`/`score` 把连续量判成评分型。

### 3.2.1 先验映射必须用实测矩阵校准（2026-10-24，1,364 条实证）

**`FORM_FAMILIES`（形态 → 模板族白名单）是先验写死的，不校准就等于「自适应」只是自说自话。**

取证方法：派发文件 `cache/_camp_<ds>_<tpl>_*.txt` 的行数与 results 里该 (ds,tpl) 的 alpha 数
**150/198 组严格相等** ⇒ 对这 150 组做按位对齐，反查表达式所含字段 → 取形态。

| 形态 | 先验白名单 | 实测最强 | 实测最弱 | 判定 |
|---|---|---|---|---|
| `discrete_rating` | lvl_rk, lvl_zs, lvl_qt | **d1_va 1.18 / 均值 0.82 / ≥1.0 占 20%** | **lvl_rk 0.05 / 均值 −0.32**；dw −0.09；ed_rk 0.09 | **先验完全反了** |
| `level_ratio` | lvl_*, pp, dw（跳过 d1/d2） | **d1_rk 1.14 / ≥1.0 占 10%** | **dw 0.72 / ≥1.0 占 0%** | **一半错** |
| `change` | d1, d2, ed, lvl_rk | d1_rk 0.84 | ir_pl 0.51 | 方向对，整体无信号 |
| `count` | lvl_rk, dw, pp | ed_rk / dw / lvl_rk 1.37–1.39 | ir_pl 0.66 | 方向对 |
| `other` | 全交叉 | lvl_rk 1.62；**pp 1.60 / 均值 1.08 / ≥1.0 占 68%** | d2_rk 0.73 | **信号主产区，但门控没对它开** |
| `skip` | 空集 | d1_va 0.87 | dsp_rk 0.38 | 先验正确 |

**三条修正**：
1. `discrete_rating` 白名单 → `{d1_va, d2_rk, d1_rk, lvl_zs}`，剔除 `lvl_rk` / `dw` / `ed_rk` / `ir_pl`。
2. `level_ratio` 把 `d1_rk` / `d1_va` 加回白名单；`dw` 降为非首选。
3. 稀疏门控 `pp` / `tl` 应从 `GATED_CATS={SENTIMENT, SOCIALMEDIA}` 扩展到 `other` 形态字段
   （它是唯一产出接近门槛 alpha 的形态）。

⚠ **分类器覆盖率是更大问题**：`other` 形态样本量 37–66/模板，而具体形态只有 5–30
⇒ 大半字段落不到具体形态，先验对它们完全不起作用。

### 3.3 离线 LLM 语义打标（跨集复用）

```bash
$WQ_PY tools/export_fields_for_tagging.py     # 导出正则判 other 的字段
$WQ_PY tools/gen_llm_field_tags.py            # → cache/field_form_llm.json
```

格式 `{"数据集.字段": {"form": "...", "conf": 0.0-1.0, "why": "..."}}`，**conf >= 0.7 才采信**。
EUR 全池 35,105 条打标、17,715 条 conf>=0.7。campaign 内按 mtime 热加载。

**不要为每个数据集手写分类器** —— 语义族是跨集共享的，规则库 + 置信度阈值就够了。

### 3.4 字段预算（控成本）

| 模式 | 每集代表字段上限 | 说明 |
|---|---|---|
| 全量模板族 | **8** | `FULL_FIELD_CAP` |
| 探针 | 12 | `PROBE_FIELD_CAP` |

EUR 实测：单集 8 字段 × 11 模板族 ≈ 55–61 条仿真，约 1 小时跑完；
不设上限时 `risk62` 按 19 字段派了 134 条（2.5 倍成本，同一批模板）。

---

## 4 派发纪律（跳一条 = 整批 CANCELLED）

三类错误会让**整批**（含同批健康表达式）一起废掉：

```
unknown variable      ← 字段名错 / 幽灵字段 / 名字被截断
inaccessible operator ← 算子在该 region 不可用
Incompatible unit     ← 量纲不匹配
```

- 全局黑名单 `cache/bad_tokens.json`，派发前过滤 + 整批 FAIL 后剔除黑名单重派一次。
- 手工派发（MCP）也必须先跑 `preflight_expressions`（带 `dataset_id`）。
- **字段名绝不可截断后用于构造表达式**（DEU WANL42 实测浪费 10 槽）。

---

## 5 读数与判死

### 5.1 候选必须逐 alpha 判，不能看集级 max

集级 `max_S` 与 `max_2Y` **常来自不同的 alpha**，拼起来会造出假的「距交付最近」。

正确做法：遍历 `alphas[]`，逐颗 `S >= 1.5 且 2Y >= 1.58`，再核 `sub >= 0.53 x S`（EUR）。

### 5.2 读数三分法（沿用 `_probe-sop.md` 第 2 步）

| 双结构最好读数 | 动作 |
|---|---|
| S>=1.58 且 2Y>=1.58 | 全闸验证 → PnL 互相关去重（一腿只出 1 颗） |
| **S 1.0–1.58** | **不判死** —— 「结构没找对」信号带，升级窗 / 轴 / 算子 |
| S<0.5（双结构都） | 判死；同族字段免测 |

### 5.3 ★ 单一设置点判死 = 最大假阴性来源

`1.2 <= max_S < 1.58` 的集必须补扫设置轴，否则会把「换个设置就过闸」的集判死：

| 变体 | EUR 实证 |
|---|---|
| universe 换宽 | TOPCS1600 → TOP2500，低波动族 S 1.56 → **1.81** |
| `neutralization=SUBINDUSTRY` | sub 0.78 → 0.93、rob 0.55 → 1.13，几乎不损 S |
| `neutralization=CROWDING` | 论坛实测 2Y 1.15 → 2.17 |

⚠ **但这三条都不是普适规律**：同一 EUR 战役里 `sentiment26` 换 TOP2500 后 S 1.62 → **1.28**、
SUBINDUSTRY 1.62 → 1.07、CROWDING 1.62 → 0.71。**设置轴必须族内实测，不可跨族外推。**

### 5.4 ★★★ 结构硬天花板指纹 = 8 条轴全在基准点取极大

EUR `LL5zM9aL` 实证（S1.62/F1.05/sub1.10/rob1.00/prod0.56，仅 ladder 1.58==门槛不过）：
19 个变体、8 条轴（decay / truncation / neutralization / universe / 内层窗 / backfill / ts_scale / 门控 q）**无一超过基准**。

⇒ 出现这个指纹就**立即封存，别再调**。此时唯一出路是换结构或换数据集，
继续微调只会烧预算（该族又烧了 19 条才确认）。与论坛《HKG 生存指南》
「两分量 IS_Ladder Y2 天花板 1.58，必须四分量」一致。

---

## 6 跨区不可迁移清单（2026-10-23 全部有反例）

这几条曾经被当成通用杠杆，实测证明是**族属性**：

| 杠杆 | 成立场景 | 反例 |
|---|---|---|
| `vector_neut(x, rank(cap))` 降 prod | 内层是**时间平滑的水平量**、未做截面秩归一（LL5zM9aL：S1.62/prod0.56） | 内层已 `ts_quantile/ts_rank` 归一 ⇒ 纯中性；news 族 rob **0.46 FAIL** |
| `tail/if_else` 门控提 S | 信号集中在极端尾部（+0.51） | `other553` 2Y −0.33、`news_nlp` rob 0.12 |
| `ts_scale` 修近期衰减 | 水平量型信号 | 「秩 + 门控」型：S 1.62 → **0.48**，2Y → 0.03 |
| universe 换宽提 S | 信号宽度敏感的低波动族 | `sentiment26`：1.62 → 1.28 |

**判据**：用前先判「内层有没有做过截面秩归一」+「基线 rob 是否 >= 1.0」；
两条不满足就别用，先把 rob 测出来再说。

---

## 7 DEU 落地差异（相对 EUR）

| 项 | EUR | DEU |
|---|---|---|
| universe | TOPCS1600 | **TOP500** |
| neutralization | FAST | **SUBINDUSTRY** |
| nanHandling / maxTrade | ON / ON | **OFF / OFF** |
| startDate | 2014-01-01 | **2013-01-01** |
| 集级覆盖闸（常规 / 处女地） | 0.8 / 0.35 | 0.8 / 0.35 |
| 字段级覆盖闸 | 0.8 | **0.6**（DEU 实证：cov<0.6 占 77.6%） |
| 内部 review 的 2Y 线 | 1.58 | **1.0**（`thresholds.json`；平台 RA 硬线仍是 1.58） |
| `CLUSTER_TEST` 门槛 | 1.58 | **1.0** |
| 已知唯一有效机制 | — | 「已标准化的预期变化率」（`*_estimate_change_*`） |
| 已知唯一有效框架 | — | 双窗 1/210 + 单桶轴 `bucket(rank(ts_mean(bf,252)), "0,1,0.05")` |

⚠ DEU 的 `universe=TOP500` 只有 500 只票 ⇒ **universe 换宽的杠杆空间极小**（EUR 是 1600→2500）。
DEU 破 S 应优先走「结构 / 双窗 / 轴」，不要指望换 universe。

⚠ DEU 是单国家宇宙（`config.REGION_COUNTRY_SCOPE`）⇒ `country` 轴中性化 = 全市场，**不要用**。

---

## 8 一句话流程

```
选集（dataset_scan：X 排除 → V 优先 → U 次之 → L 降权）
  → 拉全字段清单（dump_ds_full）
  → 按 description 归语义维度 + LLM 打标
  → 每维度 1–2 代表字段（上限 8）
  → 字段 × 模板族地图
  → 派发前三闸（preflight / op_arity / 类型+单位）
  → 读数三分法 + 逐 alpha 判
  → 1.0–1.58 不判死，先扫设置轴
  → 8 轴全取极大 ⇒ 封存换集
```
