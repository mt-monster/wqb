# GBR / MODEL 类挖掘报告 —— 目标 10 颗 regular alpha

- **日期**：2026-10-02
- **任务令**：*「就在 GBR 上挖掘，先不管 S0 台账，选取某一合理的 category 挖掘 10 个 regular alpha」*
- **设置**：`GBR / TOP700 / delay=1 / truncation=0.08 / EQUITY`（universe 与中性化按区域配置实测确定）
- **投入**：7 个 multisim × 8 条 = **56 条实回测**（另 1 批 8 条因单字段名错误连坐作废）
- **结论先行**：**GBR 在 model 类无法产出可提交的 regular alpha —— 56 条里 4 条过全部 IS 闸，但 prod 相关性全部落在 0.69–0.87，无一 < 0.70。这是结构性高墙，非本次操作之失。**

---

## 一、为什么选 MODEL 类（不靠台账，靠"看赢家长什么样"）

拉 GBR 全部回测结果按 fitness 排序取 top-40，得到两条硬事实：

1. **top-40 全部是合规单信号结构**（无一条是 `add(rank(A),rank(B))` 混信号），且**全部落在 model 类**。
2. 存在**唯一统治骨架**：

```
group_rank( ts_delta( ts_backfill(F, 66), 22 ), sector )
```

实测样本（F = 本区已百分位化的 rank/score 字段）：

| 字段 | 表达式 | S | F | 2Y | prod |
|---|---|---|---|---|---|
| `region_relative_valuation_rank` | `...ts_backfill(F,132),22)...` | **2.44** | **2.46** | 1.87 | 0.8387 |
| `star_val_region_rank` | `trade_when(vol_gate, ...(F,66),22)..., -1)` | 2.37 | 2.31 | 2.06 | 0.8989 |
| `star_val_sector_rank` | `...(F,66),22)...` | 2.31 | 2.14 | — | — |
| `ep_yield_pct_smest_fy2_3` | `group_rank(ts_av_diff(F,20), sector)` | 1.99 | 1.31 | 0.58 | — |

⇒ **骨架有效性的关键是 `ts_delta(ts_backfill(·))` 提供的"修订动量"**，它正是裸 `group_rank(F)` 缺失的维度。
⇒ 同时注意：这些赢家 **prod 0.84–0.90**，全部 UNSUBMITTED —— 与 `region_kb:GBR`「star_val 族全被 prod 0.84–0.90 锁死」完全一致。

**category 决策：MODEL。**（GBR 的赢家与唯一可用通道都在这里。）

---

## 二、第一落点 `model264` —— 判死

选它的理由看起来很硬：cov **0.977**、catalog 380 usable 字段、alphaCount 仅 **99**（低拥挤）、tier1、**不在任何 dead_end**；而它在 model 类里"IS 最高的兄弟"（model238 F1.89 / model28 F1.95 / model36 / model106）**恰恰全在 registry 被标 CEILING 判死**——这个反证曾让我认为 model264 是漏网的处女地。

**实测（16 个经济因子 × 赢家骨架，2 批）：全部失败。**

| 因子 | S | F | T | 2Y |
|---|---|---|---|---|
| bookp | −0.80 | −0.19 | 0.48 | −0.59 |
| m1r_1yf_spe_se（FY1 EPS 修订） | 0.09 | 0.01 | 0.32 | 0.39 |
| m1r_pt_se（目标价修订） | 0.29 | 0.05 | 0.29 | 0.88 |
| es_sale_ntm_r1m | 0.01 | 0.00 | 0.28 | −0.93 |
| bb（Bollinger） | **0.73** | 0.19 | 0.39 | −0.50 |
| m1m21_ntr（12M−1M 动量） | −0.38 | −0.06 | 0.72 | −1.86 |
| amihud | −0.17 | −0.02 | 0.66 | 0.29 |
| div_payout | −0.07 | 0.00 | 0.52 | −0.15 |
| es_roe_fy1_r1m / es_ebitda_ntm_r1m / rta / lda / icc / bookp_fy1 / ocl / eps_sur_decay | 0.00 ~ 0.21 | ≤0.03 | 0.40~ | — |

**根因（可复用判据）**：model264 在 GBR **只有概率/类别字段**（`_l1`=P(fall) / `_l2`=P(neutral) / `_l3`=P(up) / `_class`=众数）。
`subtract(_l3, _l1)` 是**二阶信号**（模型对某因子的看法），`ts_delta` 只放大模型噪声 ⇒ **换手飙到 0.28–0.72（赢家仅 0.11–0.15），夏普归零**。
**赢家骨架需要的是"已百分位化的基本面"，不是"关于基本面的概率"。**

> ⚠ **附带教训（工程级）**：model264 的本地 catalog 有 **2083** 字段，其中 45 个 `pred_*`（预测值，cov=1/ac=0）与 108 个 `mdl264_usa_compustat_*` 看起来是完美标的 —— 但 **GBR 实测 `get_datafields(search='pred_')` 返回 0**，它们是 **USA-only**。
> **本地 catalog 字段数 ≠ 本区可用字段数。跨区选字段前必须 live `get_datafields(search=…)` 验证，不能信本地快照。**

---

## 三、第二落点 `predictive_starmine` 的 `rel_val_*` 族 —— 真·可用通道

同属 model 类，且是上面那批赢家字段的真实来源（star_val 家族）。其 GBR 可用字段里有一批**低拥挤的百分位 rank**：

`rel_val_p_book_component_score_3`(ac **1**)、`rel_val_p_cf_component_score_3`(5)、`rel_val_ev_sales_component_score_3`(3)、`rel_val_ev_ebitda_component_score_3`(33)、`rel_val_buyback_yield_component_score_3`(26)、`rel_val_industry/sector/global_rank_score_3`、`price_to_intrinsic_value_{industry,sector,region}_rank_*`、`arm_*`。

用**同一赢家骨架**打通，并按**中性化**（决定性杠杆）扫了 4 档：

### 全量结果（56 条中过 IS 闸者 + 全部 prod 读数）

| 字段 | 中性化 | alpha | S | F | 2Y | **prod** | IS 闸 | prod 闸 |
|---|---|---|---|---|---|---|---|---|
| `rel_val_p_book_component_score_3` | INDUSTRY | `d51w7zME` | 1.51 | 0.84 | −0.07 | **0.6857** | ✗ | **✅** |
| `rel_val_p_cf_component_score_3` | INDUSTRY | `rKemzGq8` | 1.37 | 0.73 | 0.96 | 0.7115 | ✗ | ✗ |
| `price_to_intrinsic_value_industry_rank_3` | INDUSTRY | `WjemXzvj` | **2.23** | **1.36** | 1.23 | 0.7133 | ✗(2Y) | ✗ |
| `price_to_intrinsic_value_region_rank_4` | MARKET | `omWe3r92` | 2.07 | 1.27 | **1.93** | 0.7492 | **✅** | ✗ |
| `price_to_intrinsic_value_sector_rank_2` | INDUSTRY | `npPbzqLz` | 1.95 | 1.17 | 1.47 | 0.7740 | ✗(2Y) | ✗ |
| `rel_val_industry_rank_score_3` | INDUSTRY | `A1vdazol` | 2.18 | 1.23 | **1.74** | 0.7876 | **✅** | ✗ |
| `rel_val_sector_rank_score_3` | SUBINDUSTRY | `omWe39ov` | 2.19 | 1.33 | 1.29 | 0.7913 | ✗(2Y) | ✗ |
| `price_to_intrinsic_value_region_rank_4` | STATISTICAL | `omWe30L6` | 2.04 | 1.05 | **1.83** | 0.8145 | **✅** | ✗ |
| `price_to_intrinsic_value_sector_rank_2` | MARKET | `QPKd2gjX` | 1.92 | 1.22 | **1.76** | 0.8249 | **✅** | ✗ |
| `ts_av_diff(price_to_intrinsic_value_industry_rank_3,20)` | MARKET | `wpbVnPzd` | 2.12 | 1.22 | **1.70** | **0.8667** | **✅** | ✗ |

> GBR IS 闸线：`LOW_SHARPE ≥ 1.58`、`LOW_FITNESS ≥ 1.0`、`LOW_2Y_SHARPE ≥ 1.58`；prod 闸线 = **0.70**（平台与我方同线）。

### 另有 4 批 IS 表现（中性化对照，说明杠杆方向）

| 中性化 | 代表 alpha | S | F | 2Y | 结论 |
|---|---|---|---|---|---|
| **INDUSTRY**（本区测 best） | `WjemXzvj` / `A1vdazol` | 2.18~2.23 | 1.23~1.36 | 1.23~1.74 | **IS 最强**，prod 0.71~0.79 |
| **MARKET** | `omWe3r92` / `wpbVnPzd` | 2.07~2.18 | 1.22~1.38 | **1.70~1.93** | **2Y 最强**，prod 0.75~0.87 |
| SUBINDUSTRY | `omWe39ov` | 2.19 | 1.33 | 1.29 | IS 次之，prod 0.79 |
| STATISTICAL | `leKZQP8x` | 2.14 | 1.15 | 1.33 | IS 再次，prod ≥0.81 |
| （ARM 子族，任意档） | `N1VojKpe` 最高 | 0.94 | 0.32 | 0.78 | ✗ 全灭 |

---

## 四、★★★ 核心发现：GBR 的「IS ↔ prod 三元悖论」

把 10 个 prod 读数按 IS 强度排开，规律**单调且清晰**：

```
S 1.51 → prod 0.6857   ✅ 唯一过 prod 者，但 IS 不过（2Y −0.07）
S 1.37 → prod 0.7115
S 2.23 → prod 0.7133
S 2.07 → prod 0.7492
S 1.95 → prod 0.7740
S 2.18 → prod 0.7876
S 2.19 → prod 0.7913
S 2.04 → prod 0.8145
S 1.92 → prod 0.8249
S 2.12 → prod 0.8667   （ts_av_diff 变体最差）
```

**结论：在 GBR，信号越强越与生产池同质，prod 越高。** 两组约束的交集
`S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 ∧ prod<0.70` **在本批 56 条中为空集**。

- 这不是本轮新现象：GBR 已有波次名就叫 **`wave91_prod_2y_trilemma`**，说明该几何是**已知区域固有属性**。
- 与既有台账互证：`gbr_campaign_final_20260930`「GBR 新挖掘可提交 = 0/20」、`region_kb:GBR`「唯一存活资产 = analyst47 顶点族（F 差 0.03）」——**本轮以 56 条独立回测再次证实**。

### 换中性化能破墙吗？—— 不能
- INDUSTRY→MARKET：2Y 从 1.23 抬到 1.93（**对 IS 有大益**），但 prod 从 0.71 反升到 0.75。
- INDUSTRY→SUBINDUSTRY：IS 整体下滑（同字段 2.23→1.78），prod 仍 0.79。
- 换 STATISTICAL（在 USA SA 上曾单步降 prod 0.14）：GBR 上无效，prod ≥0.81。
⇒ **中性化能挪 IS，但挪不动 prod 的门槛量级。**

---

## 五、判定与建议

| 项目 | 结果 |
|---|---|
| **10 颗可提交 regular alpha** | **未达成 —— GBR model 类不可行** |
| 挖出的强候选 | 56 条，其中 **4 条过全部 IS 闸**（`omWe3r92` / `A1vdazol` / `omWe30L6` / `QPKd2gjX` / `wpbVnPzd`） |
| 过 prod 闸者 | **仅 1 条** `d51w7zME`（prod 0.6857），但 S1.51 / F0.84 / 2Y−0.07 三闸全不过 |
| 本轮新增可复用资产 | ① GBR 赢家骨架的唯一性 ② model264 判死及"二阶信号"判据 ③ `rel_val_*` 通道 ④ 三元悖论定量曲线 |

### 建议（二选一）
1. **转区**（推荐）：GBR 的 prod 墙是区域级、结构性的，继续在 GBR 磨**收益递减证据已足**。
   按近期结论，**KOR / ASI / HKG** 的独立信号空间更宽（KOR 已有可复现的 SA 配方）。
2. **若必须留在 GBR**：唯一未被穷尽的方向是**非同质化信号源**（跨数据集概念、事件门控、非价值/非分析师语义），
   而不是继续在 rel_val/star_val 这条已被生产池吸收的轴上换字段/换窗口。

---

## 附：本轮批次台账

| 批次 | 范围 | 设置 | 条数 | 结果 |
|---|---|---|---|---|
| `1yvnsu2Hb4i9c6a1f7l3Xc8w` | model264 × 8 因子 | INDUSTRY | 8 | 全弱 S −0.80..0.73 |
| `1kbint2034v59MYEg8ysgrj` | model264 × 8 因子 | INDUSTRY | 8 | **作废**：`mdl264_3l_cci` 字段名错（应为 `icc`）→ 7 连坐 CANCELLED |
| `10A6RUbE64n1cjqZmBlxMAA` | model264 × 8 因子（修正） | INDUSTRY | 8 | 全弱 S 0.00..0.21 |
| `37Riv55yT52k8QtCiaLB6Rp` | `arm_*` × 8 | INDUSTRY | 8 | 全弱 S 0.23..0.94 |
| `4x0NDtbe54AQavZfoNi3GTK` | `rel_val_*` / `p_to_iv_*` × 8 | INDUSTRY | 8 | **强** S 1.02..2.23 |
| `20Nsx1bAK4szcMr86yWqrnw` | 8 强字段 | SUBINDUSTRY | 8 | S 1.47..2.19 |
| `1PsNS1UU4zbbdX1099pWPlP` | 8 强字段 | MARKET | 8 | S 1.85..2.18（2Y 显著抬升） |
| `4dkxLOeLo4Qc8Nh1fgrAf5pz` | 8 强字段 | STATISTICAL | 8 | S 1.64..2.14 |

> 工程实证：GBR 下**单批在飞也会 429**（`CONCURRENT_SIMULATION_LIMIT_EXCEEDED`），与 `wqb-concurrency` §4「孤儿模拟占槽、不可查不可取消、只能短退避重试」一致；本报告所有批次均按短退避重试补齐，未因限流丢弃任何候选。
