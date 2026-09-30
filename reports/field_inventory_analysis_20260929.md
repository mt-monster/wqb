# 本地「区域 → 数据集 → 字段」库存盘点与分析（2026-09-29）

数据源：`data/wqb.db`（只读，296 MB）。全部数字为本次实测，非记忆推断。

---

## 一、这个机制存在吗？—— 存在，且是四层结构 + 一条入库链路

### 1.1 表结构（实测行数）

| 层 | 表 | 行数 | 内容 | 平台来源 | 入库工具 |
|---|---|---|---|---|---|
| L0 | `regions` | 17 | 区域静态配置：合法 universe 档位 / 默认中性化 | 人工 + `config.py` 校准 | — |
| L1 | `datasets` | 1890 | region × dataset × delay 粒度：field_count / coverage / alpha_count / category / tier | `GET /data-sets` | `discover_datasets.py` |
| L2 | `fields` | **268,714** | typed catalog：字段名 / 类型 / coverage / userCount / alphaCount / description | `GET /data-fields?...&dataset.id=X` | `scan_fields.py` / `backfill_catalogs.py` |
| L3 | `field_profile` | 30,705 | 分布画像：shape / skew / kurt / freq / pos_ratio / near_zero_ratio | WebDataScope + BRAIN Labs | `field_profile_from_labs.py`、`field_profile_backfill.py` |
| L3b | `external_fields` | 24 | 本区未收录但别的区 alpha 在用的字段 | `get_user_alphas` 反查 | `populate_external_fields.py` |
| L4 | `ledger_kv` | 4,997 | `s0_whitelist` / `s1_*` / `catalog_*` / `gate_cache_*` / `mechanism_*` | 本地沉淀 | 各 workflow 节点 |

**粒度唯一性实测通过**：`(region_id, name, delay)` 重复组 = 0；`(dataset_id, field_name)` 重复组 = 0。

**新鲜度证据**：`fields` 有 `verified` / `verified_context` / `verified_at` 三列，实测 243,114 行 `verified=1`（90.5%），`verified_context` 形如 `MEA/TOP400/D1` —— 说明每行都绑定了当时的扫描上下文，不是陈年快照。

### 1.2 入库链路（平台 → DB）

```
GET /data-sets            → discover_datasets.py        → datasets       (1890)
GET /data-fields?...&dataset.id=X
                          → scan_fields.py              → fields         (268714)
                          → 同时落 JSON: data/dataset_assets/ (112 文件) + tracking/<R>/reference/
WebDataScope / Labs 画像  → field_profile_from_labs.py  → field_profile  (30705)
get_user_alphas 反查      → populate_external_fields.py → external_fields (24)
```

`scan_fields.py` 的一个关键设计值得记住：**平台 `/data-fields` 不返回 longCount 实测值**，脚本用 `int(universe_size × coverage)` 作有效股票覆盖上界代理（脚本注释明写：估计值 < 阈值是可靠排除，估计值 ≥ 阈值 **≠** 通行证，真实值要等探针回测回写 `longCount_source=measured`）。

### 1.3 数据质量缺口（本次新发现，需处理）

| # | 问题 | 实测 | 影响 |
|---|---|---|---|
| 1 | **coverage > 1** | 95 行，集中在 MEA/pv96，最大 1.1149 / 1.089 | coverage 是 longCount 代理的因子，>1 会算错持仓上界，需 clamp 到 1.0 |
| 2 | **regions 表脏行** | 4 个非区域行：`PINGTEST` / `GLOBAL` / `ILLIQUID` / `TST`；`config.py` 有 `TWN` 但 DB 无 | 任何 `JOIN regions` 的统计会被污染 |
| 3 | **CHN/JPN/AMR 未启用** | DB 有但 `universe_legal=NULL`；且三区 `fields.verified` 全为 0 | 这些区的字段未验证，不能直接用 |
| 4 | **已登记未扫描** | 304 个 dataset `field_count>0` 但 `fields` 实测 0 行 | 门禁会因缺 catalog 抛 `FileNotFoundError`，波次崩溃 |
| 5 | **画像覆盖率低** | 30,705 / 268,714 = **11.4%**；147 个有画像的 dataset 里 USA 占 102，**KOR 只有 1 个** | 活跃区缺 shape/freq 先验，预处理只能靠猜 |
| 6 | **`field_group` 死列** | 100% `NULL` 或空串 | 不能用于分组 |
| 7 | **delay=NULL 行** | 168 行（category 也 NULL） | 未指定 delay 的登记行，无法定位 |

---

## 二、字段有什么特点

### 2.1 类型决定算子（最重要的一条）

| type | 行数 | 占比 | 平均 coverage | 算子约束 |
|---|---|---|---|---|
| **MATRIX** | 192,559 | 71.7% | 0.746 | 可直接 `rank` / `ts_*`，主力信号源 |
| **VECTOR** | 62,644 | 23.3% | 0.637 | **必须 `vec_*` 聚合**（`vec_sum`/`vec_avg`/`vec_count`）后才能用，裸用编译错 |
| **GROUP** | 13,282 | 4.9% | 0.875 | **只能做分组轴**（`group_rank`/`group_zscore`/`group_neutralize`），不可当信号值 |
| SYMBOL | 206 | 0.1% | 0.402 | 不可直接运算 |
| UNIVERSE | 23 | — | 0.884 | 不可直接运算 |

→ 23% 的字段（VECTOR）如果忘记包 `vec_*` 就是纯浪费；5% 的字段（GROUP）根本不该进信号池，只该进分组轴池。

### 2.2 覆盖度两极分化

| 档 | 行数 | 占比 |
|---|---|---|
| A ≥ 0.90 | 104,795 | 39.0% |
| B 0.70–0.90 | 63,602 | 23.7% |
| C 0.50–0.70 | 56,212 | 20.9% |
| D 0.30–0.50 | 20,704 | 7.7% |
| E < 0.30 | 23,401 | 8.7% |

按类型看，GROUP 平均 0.875 最高，**VECTOR 0.637 是洼地** —— VECTOR 字段在 longCount 代理（`universe_size × coverage`）下最容易跌破 80 阈值。

### 2.3 冷热度：57% 的字段是 alphaCount=0，但这**不是**机会信号

- `alphaCount`：min 0 / 均值 61.5 / max 708,528（极度长尾）
- `userCount`：min 0 / 均值 15.2 / max 65,145
- **`alphaCount=0 且 userCount=0` 的字段 = 153,446 个，占 57.1%**

这里有一条已固化的机制条目（`ledger_kv: mechanism_field_alphacount_zero_is_desert`，2026-09-09），原文要点：

> `alphaCount=0` 有两种截然不同的含义：① 处女地（字段强但没人发现）② 荒漠（字段弱所以没人挖）。
> **禁止把 alphaCount=0 当作选字段的正面信号。**

证据与反证：
- **反例（荒漠）**：EUR wave155 / `ml_factor_proj`，6 个 alphaCount=0 字段 Sharpe 全部 ≤0.20（fcf_growth −0.14 / consensus −0.19 / leverage −0.21，7/7 全灭）。数据集 description 明写「projection features for **US** equities」。
- **反证（高 alphaCount 也强）**：`dl_riskfree_returns` 的 ohlcv 族 alphaCount 高但 Sharpe 2.2–2.6 真实强。
- **结论**：字段级 alphaCount 与字段强度**无负相关，反而可能正相关**（强字段被挖得多）。

正确做法：选 alphaCount **中等偏高（10–50，被验证有 alpha 但未到饱和）** 且信号内容与已有持仓不同的字段；若坚持探 0 字段，必须先有字段强度的**独立证据**（coverage / description 的经济含义 / `region_kb` 先验）。

### 2.4 语义：typed catalog 不回答「能不能当信号」

`fields` 表只回答「什么类型、覆盖多少、多少人用」，**不回答「这字段能不能当信号」**。这层由 `field_semantic_classify.py` 补。

实证教训（KOR/fundamental17，2026-09-28）：步 3 只做 scan_fields 就进 GEM，348 条产物里 **49.4% 落在「货币代码 / 汇率叉乘」这类非信号字段**上（三角套汇恒等式、字符串分类码），71% 是废产物。

### 2.5 画像（仅 11.4% 有）—— 决定预处理

| shape | 行数 | 平均 coverage | 含义 |
|---|---|---|---|
| spread | 16,694 | 0.753 | 分布展开，可直接 rank |
| **zero_inflated** | 12,243 | 0.665 | **0 值堆积** → 裸 rank 会把 0 堆在中位数，必须先 `ts_backfill` 或去零 |
| ceiling | 988 | 0.589 | 有上界截断 |
| unknown | 581 | 0.293 | — |
| concentrated | 131 | 0.079 | 极稀疏 |
| point_mass | 68 | 0.047 | 几乎全同值 |

| freq | 行数 |
|---|---|
| **quarterly** | 10,670 (34.8%) |
| daily | 8,367 |
| semi-annual | 5,423 |
| monthly | 3,205 |
| weekly | 3,040 |

→ quarterly 主导（35%）意味着**慢变量居多**。`field_count_strategy_layered_v1` 明确禁止「慢×慢」组合（KOR 实证全灭），成功配方是快×慢（KOR 评级修正慢 × SH 短周期快 → S=1.91 / 2y=2.52）。

---

## 三、举例：以挖掘因子为目标的完整分析链（KOR 真实例）

### 步骤 0｜定位：挖哪个塔

选塔优先律：已点亮塔不再优先提交，优先「未点亮塔」。
KOR 已点亮 = analyst 6 / fundamental 3 / model 4 / other 6 / pv 3；**未点亮 = sentiment / news / insiders / institutions / macro / risk / shortinterest 等**。
⚠ 判定唯一权威 = 平台 `get_pyramid_alphas`，**本地 `alphas` 表不能做塔级统计**（`date_submitted` 全库仅 2.7% 非空，塔归属 ≠ `datasets.category`）。

→ 候选：`mmp_nlp_sentiment`（521 字段，cov 0.6187，alphaCount 仅 10，极冷）。
⚠ 注意：它 `category=OTHER`，**塔归属须查平台 pyramid**，不能从 category 推。

### 步骤 1｜数据集级分诊

```
mmp_nlp_sentiment (KOR/D1)  fc=521  cov=0.6187  alphaCount=10  category=OTHER
```
S0 硬闸（cov≥0.85 & alphaCount≤50 & fieldCount≥10）：cov 不过 —— 这是 PPA 开战役门槛；RA 走另一套，但 cov 偏低要记住（横截面薄）。

### 步骤 2｜类型 → 算子约束

实测：**521 个全是 MATRIX，0 个 VECTOR**。
→ 好消息：全部可裸用 `rank` / `ts_*`，**不需要 `vec_*` 包装**，也不用担心 longCount 塌方。若这里是 VECTOR 主导，工作量完全不同。

### 步骤 3｜覆盖度分档 → 可用字段池

```
A ≥0.9 :  51
B 0.7-0.9: 195
D 0.3-0.5: 275      ← 无 C 档
```
KOR universe = TOP600（唯一合法档）。D 档 longCount 代理 = 600 × 0.35 ≈ 210，横截面偏薄，容易 `CONCENTRATED_WEIGHT` FAIL。
→ **初筛池 = A + B = 246 个**。

### 步骤 4｜饱和度 → 排除「荒漠」陷阱

```
alphaCount = 0 : 512 个 (98.3%)
alphaCount 1-5 :   9 个
```
⚠ **这一步如果按「没人挖 = 机会」选字段，会把 512 个弱字段全选进来**，直接踩 `mechanism_field_alphacount_zero_is_desert`。
→ 改用「coverage + description 经济含义」作独立证据，从 9 个有 alpha 的 + A 档高覆盖里挑：

| 字段 | cov | ac | 判读 |
|---|---|---|---|
| `avg_bullish_topic_score` | 0.893 | 3 | 看多主题均分 — 有方向性 |
| `mad_bearish_topic_score` | 0.893 | 1 | **MAD = 分歧度**，比均值更有信息量 |
| `max_bullish_tone_score` | 0.893 | 1 | 极值而非均值，避开平滑 |
| `average_bearish_mention_score` | 0.893 | 1 | 看空提及 |
| `advertisement_mention_total` | 1.0 | 2 | 计数类，经济含义弱 → 降权 |
| `analyst_reference_count_sum` | 1.0 | 0 | 计数类 + ac=0 → 排除 |

**判读逻辑**：情绪类字段里「分歧度（mad/mad 类）」和「极值（max/min）」比「均值（avg）」信息量高——均值会被平滑掉，分歧度才是横截面差异的来源。这与 `field_count_strategy_layered_v1` 的 diversity 维度（operator 多样性）一致。

### 步骤 5｜语义归类 → 剔除非信号

```
python tools/field_semantic_classify.py --region KOR --dataset mmp_nlp_sentiment
```
实测输出：
```
信号字段 516 (99.0%)  |  非信号黑名单 5 (1.0%)
经济大类：other 494 / dividend 22（冷门 users<=9 占 100%）
非信号：标识符/国别交易所代码 5 例
  例: avg_raising_stake_topic, median_raising_stake_topic, min_advertising_tone_text_score
```
→ 这 5 个必须进黑名单，否则 GEM 会产废产物。

### 步骤 6｜画像 → 预处理选择（**当前缺口**）

`mmp_nlp_sentiment` 在 `field_profile` 里**没有任何记录**（KOR 全区只有 1 个数据集有画像）。
→ 若决定挖，需先用 Labs 补画像；补到后按 shape 选预处理：
- `zero_inflated` → 先 `ts_backfill(x, 66)` 再 `rank`，**禁止裸 rank**
- `freq=daily` → 属快变量，可与 other466 的季度慢变量做 **L3 正交组合（快×慢）**，这是 ledger 里记录的成功配方

### 步骤 7｜自家回测史反查（零成本最强先验）

```
PYTHONPATH=src python tools/field_signal_mine.py --region KOR --top 20
PYTHONPATH=src python tools/field_signal_mine.py --region KOR --pairs --min-abs-sharpe 1.0
```

**关键对照**：

| 数据集 | 自家回测数 | 历史 max\|S\| | 平台 alphaCount |
|---|---|---|---|
| `mmp_nlp_sentiment` | **0** | **None** | 10 |
| `other466` | 28 | **2.37** | 4597 |

→ `mmp_nlp_sentiment` 是**零证据未探区**，不是已证伪的荒漠。这与「alphaCount=0」给出的信号完全不同——**自家回测史是比平台 alphaCount 更硬的证据**，因为它测的是「我在这区用这字段能不能出信号」。

**字段级榜（KOR top，实测）**：

| field | n | max\|S\| | hits | bestF |
|---|---|---|---|---|
| `oth466_bs_assets_tot_q` | 22 | 2.37 | 19 (86%) | 2.14 |
| `oth466_q_cni_xtp_si` | 1 | 2.37 | 1 | 2.14 |
| `residualized_return_asia_minvol1m` | 15 | 2.20 | 14 | 0.83 |
| `shrt38_stk_invactsell_amt` | 11 | 2.15 | 10 | 1.86 |
| `oth466_is_ptx_inc_norm_q` | 4 | 2.11 | 4 | 1.81 |
| `eps_estimate_4wk_change` | 40 | 1.78 | 37 | 1.64 |

**字段对榜（这才是关键）**：

```
2.37  n=1  oth466_bs_assets_tot_q × oth466_q_cni_xtp_si
      signed_power(ts_rank(group_rank(divide(oth466_q_cni_xtp_si, oth466_bs_assets_tot_q), market), 504), 0.5)
2.15  n=9  shrt38_stk_invactbuy_amt × shrt38_stk_invactsell_amt
2.11  n=1  oth466_bs_assets_tot_q × oth466_is_ptx_inc_norm_q
1.90  n=9  oth466_bs_assets_tot_q × oth466_is_oper_inc_q
1.78  n=27 eps_estimate_4wk_change × ts_backfill
```

**最重要的一条洞察**：单字段榜里 `oth466_q_cni_xtp_si` 只有 n=1、看不出价值；但它作为「分子」与 `oth466_bs_assets_tot_q`（分母）成对时给出 **2.37** —— 这恰好就是已 ACTIVE 的 **KOR `wpZkk1Mp`**（prod 0.6476 / self 0.187，MATCHES_PYRAMID KOR/D1/FUNDAMENTAL ×1.6）。
→ **单字段榜会系统性漏掉「成对机制」信号**（工具 docstring 明写：HKG model238 screening×owner 背离对 S=1.39，两条单字段探针都平庸）。选字段必须看 pairs，不能只看单字段。

### 步骤 8｜形态合规（铁律）

`wpZkk1Mp` 的形态 `signed_power(ts_rank(group_rank(divide(A,B), market), 504), 0.5)` 是合规的，因为它是**单信号结构化**：
- `divide(A,B)` = 单一价差信号（税前利润 / 总资产 = 资产回报率），有经济含义，**不是两条独立信号腿相加**
- `group_rank(..., market)` = 换分组轴（第 4 闸破 SUB 比值闸的决定性旋钮）
- `ts_rank(..., 504)` 长窗平滑 + `signed_power(..., 0.5)` 压尾

**禁止**：`add(A,B)` / `0.4A+0.6B` / 等权 `0.5A+0.5B`（属同一违规族）；禁止靠增删腿数或扫描混合权重修不达标的信号。
**唯一合规方向 = Mode B**：换字段组合 / 换信号概念 / 换算子几何 / 换分组轴，或单信号结构化（`ts_scale`、`subtract(rank A, rank B)` 有经济含义的价差、`group_rank`/`group_zscore`/`ts_quantile`、事件门控 `trade_when`/`if_else`、SuperAlpha combo）。

### 可复用判定顺序（决策树）

```
1. 选塔（平台 get_pyramid_alphas，未点亮优先）→ 定 category/dataset
2. dataset 级分诊：cov / alphaCount / fieldCount
3. 类型分布 → 算子约束（VECTOR 必包 vec_*；GROUP 只做分组轴）
4. coverage 分档 → 建可用池（longCount 代理 = universe_size × cov，<80 排除）
5. alphaCount 分档 → 只取 10-50 中等偏热；0 值字段必须配独立证据
6. 语义归类 → 剔非信号字段
7. 画像 shape/freq → 定预处理（zero_inflated → ts_backfill；freq → 快/慢配对）
8. field_signal_mine（含 --pairs）→ 自家回测史先验，这是最硬的证据
9. 出表达式 → 形态合规检查（禁混信号调参）
10. 提交 → 四闸（S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.571×S）+ prod/self ≤0.7
```

---

## 四、建议动作（按优先级）

| P | 动作 | 命令 / 位置 |
|---|---|---|
| P0 | clamp `coverage>1` 的 95 行（MEA/pv96） | 一次性 UPDATE，或在上游 `scan_fields.py` 写入时 clamp |
| P0 | 清理 `regions` 脏行（PINGTEST/GLOBAL/ILLIQUID/TST），补 `TWN` | DB 维护脚本 |
| P1 | 补 304 个「已登记未扫描」dataset 的 catalog | `python tools/backfill_catalogs.py --apply` |
| P1 | 补活跃区（KOR/GBR/EUR）字段画像——KOR 目前只有 1 个数据集有 | Labs 批量画像 → `field_profile_from_labs.py` |
| P2 | `field_group` 死列要么填要么删 | schema 清理 |
| P2 | 若决定挖 `mmp_nlp_sentiment`：先 `field_profile` 补画像，再按 L1_probe（8 条上限，max\|S\|<0.7 判死） | `field_count_strategy_layered_v1.L1_probe` |

---

## 附：本次用到的命令

```bash
# 字段语义归类
python tools/field_semantic_classify.py --region KOR --dataset mmp_nlp_sentiment

# 字段级 / 字段对历史信号先验（零回测成本）
PYTHONPATH=src python tools/field_signal_mine.py --region KOR --top 20
PYTHONPATH=src python tools/field_signal_mine.py --region KOR --pairs --min-abs-sharpe 1.0 --top 12

# 字段质量 8 维评分
python tools/field_quality_scorer_v2.py --dataset <ds> --region <R> --fields-file fields.json --min-score 0.6

# 数据集信息轴识别（top 字段词根聚类 → 主导经济轴）
python tools/field_axis.py --input data_ref/all_fields.json --dataset <ds>
```
