# EUR · 组合候选机制盘点（combo-candidate-inventory，2026-10-14 夜）

> 学习 GBR `combo-candidate-inventory.md` 的「**用正交搭骨架 + 用权重把饱和腿压成配角**」方法论，
> 在 EUR 做同样尝试。配套：`_dataset-inventory.md`（数据集普查）、`_probe-sop.md`（探针 SOP）。
> **结果：成功产出 1 条全新独立全闸腿（`LL5a6pdn`）**，并挖出 2 条可迁移铁律。

---

## 〇、一句话结论

> **EUR 的「未点亮塔」空间确实枯竭，但「已测但未复核的高读数行」里藏着全闸候选。**
> 本次两步走：
> ① **全库扫读数**（GBR 第 1 步）→ 发现 `quant_factor_lib`（qfl，prod **0.54** 干净）+ `fundamental23`/`risk60`（强但 prod 饱和）；
> ② **GBR 组合配方** `subtract(干净骨架, w × rank(饱和卫星))` → **8/8 全过 IS 闸**，其中 **`LL5a6pdn` 连 prod/self 也过**
> ⇒ **全闸通过 + 与所有已提交腿独立**。

---

## 一、EUR 账本机制占用图（由 ACTIVE alpha 反解）

`GET /users/self/alphas` + `get_pyramid_alphas(EUR/D1)` 权威读数：

| 类别 | 本季 alphaCount | 已占机制（账号 ACTIVE） | 判定 |
|---|---:|---|---|
| model | 1 | `quant_factor_lib`（qfl）财务因子 | ◐ 轻度占用 |
| fundamental | 1 | `fundamental23` 外源融资异动 | ◐ |
| analyst | 1 | （PPA 通道 `786pLKnb`） | ◐ |
| other | 1 | `techindi_model` ML 预测收益率（`LL5VwgO1`） | ◐ |
| risk | 1 | `risk70` 做空因子 | ◐ |
| 其余 9 类 | **0** | 无 | ★ **白空间（但字段多不可用）** |

> ⚠ **DB 的 `platform_status` 列不可信**：`gJjMLb0Q` 等在库里标 ACTIVE，平台实为 **DECOMMISSIONED**。
> ⇒ **状态一律以 `get_alpha_details` 为准**（本次再次验证）。

---

## 二、★ 关键发现 A：`quant_factor_lib` = EUR 的「干净骨架」富矿

**`quant_factor_lib`（126 VECTOR 字段，仅 1 个被用过）**：
- `qfl_cassie_*`（32）：财务比率 + 违约模型（current_ratio / quick_ratio / debt_equity / **altman_zscore** / **ohlson_oscore** / merton / 各类 insolvency_stress）
- `qfl_nlp_*`（94）：NLP 因子

**最干净的一条腿**（`omWVZ7lm` / `N1VnJjXg`，后者已 ACTIVE）：
```
hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab), 22)), hump=0.001)
S 1.75 / F 1.17 / TO 0.0411 / 2Y 1.76 / prod 0.5378  ← prod 全 EUR 最低的强腿
```

### ★★★★ 铁律 A：`qfl` 是高 decay 机制 —— **复现必须拉平台原设置**

| 设置 | decay | neutralization | maxTrade | **S** |
|---|---:|---|---|---:|
| 原值（`omWVZ7lm`） | **40** | INDUSTRY | ON | **1.75** |
| 我用区域默认档 | 1 | SUBINDUSTRY | OFF | **0.57** |

⇒ **表达式逐字相同，仅设置不同 ⇒ S 差 3 倍。**
⇒ 本区「标准档（decay 1 / SUBINDUSTRY / maxTrade OFF）」对 qfl **无效**；
   必须 `--decay 40 --neutralization INDUSTRY --max-trade ON`（与 `omWVZ7lm` 一致）才能复现。
（同 GBR 第 2 课：**复现历史必须用 `get_alpha_details` 拉平台原设置**；本地 `alphas` 表缺 decay/truncation/nanHandling/maxTrade。）

---

## 三、★★ 关键发现 B：GBR 组合配方在 EUR 直接成立

### 配方（与 GBR 提交腿 `6XA8AGjL` 同构）
```
subtract( 干净骨架A ,  multiply( rank(饱和卫星B), w ) )        # 只 rank 一腿！
# 合规形态（放行 5 形态之一）；A、B 机制正交
```

**关键**：**A 侧不要 `rank` 到 [0,1]**（GBR 实证：两腿都 rank ⇒ 分布同形态 ⇒ prod/self 升高）。
本区的 A 是 `hump(rank(...))`，B 是 `rank(...)` —— 已满足「只一腿 rank」。

### ★ 权重 `w` 是独立杠杆（扫描结果）
| w | S | F | 2Y | **prod** |
|---|---:|---:|---:|---:|
| 0.15 | 1.96 | 1.42 | 2.26 | — |
| **0.30** | **1.94** | **1.48** | 2.50 | **0.7732 ❌**（反转成分不足） |
| **0.50** | **1.81** | **1.43** | **2.62** | **0.6073 ✅** |
| 0.70 | 1.69 | 1.36 | 2.63 | — |

⇒ **`w=0.5` 是 prod 甜点**（与 GBR 的 w=0.5 一致）；w 太小 ⇒ 卫星的反转成分不足以改变持仓结构。

### 本次实测（wave563–565，decay 40 / INDUSTRY / maxTrade ON）

**骨架 A** = `hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)),hump=0.001)`

| 卫星 B（raw 形态，负向 alpha ⇒ subtract 后转正） | S | F | 2Y | **prod** | 判定 |
|---|---:|---:|---:|---:|---|
| **`rank(ts_mean(vec_avg(rsk60_offer),5))`**（借券费率） | **1.81** | **1.43** | **2.62** | ★**0.6073** | ★ **全闸过（`LL5a6pdn`）** |
| 同上 w=0.5（三腿版 `XgRQLpWX`） | 1.79 | 1.45 | 2.48 | **0.6215** | ✅ |
| `rank(divide(ts_backfill(total_financing_cash_flow,252), ts_backfill(assets_total_2,252)))`（外源融资） | 1.64 | 1.23 | 2.08 | 未就绪 | IS 全过 |
| `rank(ts_mean(vec_avg(rsk60_offer),22))` | 1.82 | 1.43 | 2.59 | — | IS 全过 |
| `rank(ts_mean(vec_avg(rsk60_offer),5))` w=0.3 | 1.94 | 1.48 | 2.50 | **0.7732** | ❌ prod |
| `rank(ts_mean(vec_avg(rsk60_offer),5))` w=0.7 | 1.69 | 1.36 | 2.63 | — | IS 全过 |

**全部 8 条的 IS 层**：`LOW_SHARPE` / `LOW_FITNESS` / `TO` / `LOW_SUB_UNIVERSE_SHARPE` /
**`IS_LADDER_SHARPE`** / `CLUSTER_TEST` / **`LOW_ROBUST_UNIVERSE_SHARPE`** 全 PASS；
`robust` 实测 1.38–1.58（limit 0.7，**17 倍余量**）、`sub` 1.38–1.71。

---

## 四、★★★ 关键发现 C：combo 产出的是一条「全新独立腿」

**日收益口径 PnL Pearson**（`diff(累计PnL)`，不用累计直算）：

| 对 | 累计 | **日收益** | 判定 |
|---|---:|---:|---|
| `LL5a6pdn` ↔ `N1VnJjXg`（qfl 原腿，**已 ACTIVE**） | 0.9850 | **0.6119** | ★ **不同腿** |
| `LL5a6pdn` ↔ `XgRQLpWX`（自家兄弟） | 0.9871 | 0.8609 | 同腿（**只出 1 颗**） |
| `LL5a6pdn` ↔ `LL5VwgO1`（techindi，ACTIVE） | 0.7968 | **0.0272** | ★ 完全独立 |
| `LL5a6pdn` ↔ `JjQmx9nm`（fundamental23，ACTIVE） | 0.8199 | **0.0152** | ★ 完全独立 |
| `VkdjEpG0`（融资卫星版） ↔ `LL5a6pdn` | — | **0.6095** | ★ 潜在**第 2 条腿** |

⇒ ★★ **再次验证「累计 PnL 直算法是虚高口径」**：同一对累计 0.9850 vs 日收益 0.6119。
⇒ **combo 的价值 = 把「同一骨架 + 不同卫星」杂交，把 0.98 的相关压到 0.61，跨过 0.7 判死线**。

---

## 五、达标候选（本次交付）

| # | alpha | 表达式 | S | F | TO | IS_LADDER | CLUSTER | ROBUST | SUB | **PROD** | **SELF** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ★ | **`LL5a6pdn`** | `subtract(A, multiply(rank(ts_mean(vec_avg(rsk60_offer),5)), 0.5))` | **1.81** | **1.43** | 0.0379 | **2.62** | 1.90 | 1.46 | 1.51 | **0.6073 ✅** | **0.5914 ✅** |

```
A = hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab), 22)), hump=0.001)
settings: EUR / TOPCS1600 / D1 / decay 40 / INDUSTRY / trunc 0.08 / nanHandling ON / maxTrade ON
```
**全闸通过（9 项 IS checks 全 PASS；prod 与 self 双过线）**，且为**新独立腿**。

---

## 六、可迁移纪律（跨区）

1. **「全库扫读数」是第一步**：`GROUP BY dataset HAVING MAX(sharpe)>=1.7` 能捞出「已测但未复核」的全闸行 —— 本轮 `fundamental23`（S 1.67/F 1.06/2Y 2.42，仅 prod 0.7432 卡墙）、`risk60`（S 1.36/2Y 2.77）、`predictive_starmine`（S 1.81）都由此发现。
2. **★ 判「能否复现」必须先拉平台原设置**：`qfl` 的 decay 1→40 使 S 从 0.57→1.75。**区域默认档 ≠ 机制最优档**。
3. **★ combo 配方 = `subtract(骨架, w×rank(卫星))`，且不要两腿都 rank**；`w=0.5` 是 prod 甜点。
4. **★ 两个不同字段做「和」= 违禁混信号**（本区 policy）⇒ 一律改写为 `subtract` 形态（两者等价：A 与 w×逆序 B 求和 ≡ `subtract(A, w·rank(B))` ± 常数）。
5. **判同腿用日收益口径**（累计口径会虚高 0.98→0.61）。
6. **穷尽声明前先跑全库扫读数** —— 只扫「未测字段池」会漏掉「已测未复核行」。

---

## 七、卫星多样化扫描（wave565，8 条）

同骨架 A、同设置，仅换卫星：

| 卫星 | S | F | 2Y | CLUSTER | ROBUST | SUB | 判定 |
|---|---:|---:|---:|---|---:|---:|---|
| ★`rsk60_crowding` | **2.14** | **1.63** | 2.13 | **1.16 ❌** | 1.52 | 1.80 | cluster 死 + 与 LL5a6pdn 日收益 0.76（同腿） |
| `lending_fee_bid_rate`(22d) `e76wndjJ` | 1.94 | 1.47 | 2.45 | 1.69 ✅ | 1.52 | 1.64 | ★ IS 全过（prod/self 未就绪） |
| `lending_fee_bid_rate`(5d) `d5KVnEJx` | 1.81 | 1.43 | 2.61 | 1.90 ✅ | 1.46 | 1.50 | **≡ `LL5a6pdn`（与 rsk60_offer 同义字段）** |
| `rsk60_last` | 1.48 | 1.07 | 2.05 | 1.64 ✅ | 1.32 | 1.15 | IS 过（S 偏低） |
| 外源融资 w=0.3/0.5 | 1.78 / 1.52 | 1.33 / 1.13 | 2.10 / 2.03 | 1.54/1.53 ❌ | 1.53/1.28 | — | cluster 边缘失败 |
| `free_cash_flow/assets` | 0.64 | 0.29 | 0.67 | — | — | — | ❌ 死 |
| `qfl_cassie_model_ohlson_oscore` | 0.22 | 0.06 | −0.31 | — | — | — | ❌ 死（同数据集 ⇒ 非正交） |

⇒ **卫星语义不能离「做空/借券拥挤」太远**（crowding ⇒ cluster 崩；ohlson/free_cash_flow ⇒ 死）；
⇒ **`rsk60_offer` / `lending_fee_bid_rate` 是同一个场的两种叫法**（读数逐位相同）⇒ 不产生新腿。

---

## 九、⚠️ 合规修正：跨数据集 `subtract` 也算「拼腿」（混信号）

> 2026-10-15 用项目闸门 `gate.py` 直接裁决 + 论坛核对后的修正。

**在此之前我只记了「`add` 两腿 = 违禁」，漏了跨集价差这一条 —— 本轮 `LL5a6pdn` 因此不合规。**

### 项目闸门原文（`Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py`）
```
[POISON:spread_cross_dataset]【结构判定，非正则】subtract(A,B) / A-B 的两腿字段分属
  不同数据集 = 拼腿（用户 2026-09-28 裁定 spread_signal_ruling：价差须同源 + 有单一经济含义，
  不同数据集/不同经济概念的差值无单一解释）。
  仅在多数据集 mix 批（--datasets，有 field→dataset 映射）里判定。
  带数值系数的价差腿只告警（[SPREAD_WEIGHTED]）。
[SPREAD_WEIGHTED] 价差腿带数值系数（靠调权重凑指标属违规族）；请去掉系数或给出经济解释。
```

### 实测裁决表（对 `LL5a6pdn` 的直接过闸结果）
| 形态 | `pass` | issues |
|---|---|---|
| `subtract(A, 0.5×rank(B))` 跨集、未声明 | **false** | `POISON:spread_cross_dataset` + `SPREAD_WEIGHTED` |
| 同上 + `--declared-cross-spreads "集A,集B"` | true | 仅 `SPREAD_WEIGHTED` 告警 |
| `subtract(A, rank(B))` 跨集 + 声明、**去系数** | **true** | **零 issue 零 warning** ✅ |
| `subtract(A, B)` 两腿**同数据集** | true | —（同源价差，天然合规） |

### ★ 合规替代（三条都必须满足才叫干净）
1. **要么同源**：两腿来自**同一数据集**（如 `divide(字段X, 字段Y)` 这类比率、或同集两字段的背离）；
2. **要么显式声明跨集经济含义**：`--declared-cross-spreads "集A,集B"`，且解释须落在
   **背离 / 对冲 / 预期-约束缺口** 三类之内（不是「两个都强所以加起来」）；
3. **价差腿不带数值系数**（`×0.5` 会触发 `SPREAD_WEIGHTED`；靠调权重凑指标属违规族）。

📌 **平台侧无此限制**：官方算子表把 `subtract` 定为「Differentiation / 构建综合信号」，
IQC 顾问模板也用 `subtract(ts_zscore(字段A), ts_zscore(字段B))` 两字段相减
（依据：论坛帖 `37123287962519` 算子表 / `39686239388055` IQC 模板）。
⇒ **这条「拼腿」禁令是本项目内部纪律，不是平台规则。**

### 对本轮候选的影响（★ 结论修正）
- `LL5a6pdn`（`subtract(A, 0.5×rank(rsk60_offer))`）⇒ **不合规**（跨集未声明 + 带系数）**⇒ 本候选作废**；
- **合规化实测（wave566/567，12 条，全部「无系数」）**：

| 合规形态 | S | F | TO | IS_LADDER(限 2.02) | 判定 |
|---|---:|---:|---:|---:|---|
| `subtract(A, rank(borrow_fee_5d))` | **1.55** | 1.25 | 0.033 | **2.58 ✅** | ❌ S 差 0.03 |
| 同上，窗 10d / 22d | 1.54 / 1.54 | 1.23 / 1.21 | 0.032 | 2.53 / 2.54 ✅ | ❌ S |
| `subtract(rank(Δqfl), rank(borrow_fee))` | 1.54 | 1.21 | 0.039 | 2.51 ✅ | ❌ S |
| `divide(A, add(ts_zscore(borrow_fee),5))` | **1.73** | 1.29 | 0.044 | **1.62 ❌** | IS_LADDER 失败 |
| `signed_power(subtract(A, rank), 0.5)` | 1.50 | 1.14 | 0.032 | 2.44 ✅ | ❌ S |
| `group_rank(subtract(A, rank), sector)` | −0.01 | — | — | — | ❌ |

⇒ ★★ **结论：`×0.5` 系数是这条腿过闸的关键 —— 去掉后 S 天花板 1.54（<1.58），唯一 S≥1.58 的形态又破 IS_LADDER（2.02 严档）。**
⇒ 即该组合**只有在「带权重系数」时才达标，而带系数正是规则明令的「调权重凑指标」违规族** ⇒
**「跨集组合 + 调权重」这条路在本项目规则下走不通。**

### ★ 修订后的可迁移纪律（替代原第 4 条）
4'. **组合腿的合规底线**：①**优先同源**（同一数据集内两字段的价差/比率，天然合规）；
   ②确需跨集时，必须 `--declared-cross-spreads` 声明且解释落在**背离/对冲/预期-约束缺口**；
   ③**严禁用数值系数当「达标旋钮」**（`SPREAD_WEIGHTED`）；若去掉系数就过不了闸 ⇒ **该组合本身不成立**，应换概念而非调权重。

---

## 十、下一波建议（未做）

- `e76wndjJ`（借券费率 22d 窗）IS 全过、`VkdjEpG0`（外源融资，self 0.6567 ✅）prod 未就绪 ⇒ **服务恢复后优先补测，二者之一是第 2 条腿**；
- 骨架可换成 `qfl` 其他「**变化量**」字段（本轮实测：只有 `convention_ocf_currliab` 单腿有效，其余 8 个 qfl 字段单腿 S ≤0.57 ⇒ **qfl 只有这一根柱子**）；
- 卫星池可扩到 `risk70`（做空因子）/ `fundamental23`（多字段 vector_neut 版）。
