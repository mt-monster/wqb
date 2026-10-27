# EUR 未点亮塔：25 颗 IS 全过候选 + prod 地板分析

> 2026-10-27 ｜ 目标：未点亮塔（FUNDAMENTAL / OTHER / PV / RISK / NEWS / …）产出 10 个 Regular Alpha
> 约束：**不换 region**（EUR only）｜ ATOM 非必需 ｜ 已点亮塔（MODEL / ANALYST）候选不提交
> 全部数据为平台实测（`get_alpha_details` 的 `is.checks[]` + `check_correlation`）

---

## 0 结论先行

| 指标 | 结果 |
|---|---|
| **IS 全过候选** | **25 颗**（FUNDAMENTAL 18 / OTHER 7），全部 `FAIL` 列表为空 |
| **prod 实测** | 5 颗，最低 **0.7408**，最高 0.7971（门槛 0.70） |
| **prod 达标** | **0 颗**（未点亮塔范围内） |
| 唯一 prod<0.70 | `rKRpEMWo` **0.594**，但属 **MODEL 塔（已点亮）** |

**核心判断：EUR 未点亮塔的 prod 地板 ≈ 0.74。** 已试尽 6 条降 prod 路径（见 §4），全部未能突破。

---

## 1 二十五颗 IS 全过候选

### 1.1 跨集混合（5 颗，S 2.49–2.78，F 1.92–2.23）

结构 `add(add(sig(基本面), w1×sig(技术)), w2×sig(预测))`，EUR/TOP2500/decay4/FAST/trunc0.08。
跨集 ⇒ 破 ATOM ⇒ 需过 `IS_LADDER_SHARPE`（2.02）而**免 `LOW_2Y_SHARPE`**。

| alpha | 构造 | S | F | sub/lim | IS_LADDER | CLUSTER |
|---|---|---|---:|---|---|---|
| `zq3Kk39K` | bank + 0.7·tm_16 + 0.7·pred141 | **2.78** | **2.23** | 1.58/1.44 | 2.43 ✓ | 3.96 ✓ |
| `2rA8lAJY` | bank + tm_16 | 2.68 | 2.15 | 1.47/1.39 | 2.41 ✓ | 3.56 ✓ |
| `JjeM7ede` | iabs + tm_16 | 2.68 | 2.15 | 1.47/1.39 | — | — |
| `QPvZ7vaK` | bank + 0.5·vbts + tm_16 | 2.59 | 2.02 | 1.56/1.35 | 2.67 ✓ | 3.24 ✓ |
| `MPYM7Ypr` | bank + ti13 | 2.49 | 1.92 | 1.35/1.29 | — | — |

### 1.2 四腿正交（3 颗，S 2.01–2.36）

在主结构上叠「机构买入家数」（cov 1.00）或「社媒情绪」（cov 0.85）作为第 4 条正交腿。

| alpha | 构造 | S | F | sub/lim |
|---|---|---|---:|---|
| `mLowovpX` | CORE3 + 0.3·inst_buy | **2.36** | **1.83** | 1.39/1.23 |
| `P0oQoVQL` | CORE3 + 0.5·inst_buy | 2.11 | 1.59 | 1.27/1.10 |
| `1YNkNMeW` | CORE3 + 0.5·scl12_sentiment | 2.01 | 1.39 | 1.24/1.04 |

### 1.3 OTHER 塔 · techindi_model（7 颗，S 1.67–1.93）

结构 `add(sig(tm_16 或 predicted_*), w×sig(predicted_*))`，EUR/TOPCS1600。

| alpha | 主腿 | S | F | 2Y | sub/lim | rob |
|---|---|---|---:|---:|---|---:|
| `QPvZEQXX` | tm_16 + pred_ten_day_15 | **1.93** | **1.27** | 2.19 | 1.34/1.02 | 0.95 |
| `akKjoOvw` | tm_16 + 0.5·15 + 0.5·tm_19 | 1.93 | 1.27 | 2.19 | 1.34/1.02 | 0.95 |
| `N1NxAO97` | tm_16 + pred_one_day_17 | 1.91 | 1.25 | 2.07 | 1.19/1.01 | 0.95 |
| `LLMVgYj9` | pred_five_day_141 **单腿** | 1.89 | 1.25 | 2.07 | 1.32/1.00 | 0.90 |
| `78L7zeWL` | pred_five_day_14 单腿 | 1.88 | 1.19 | 2.13 | 1.31/1.00 | — |
| `Xg9modra` | pred_one_day_13 单腿 | 1.74 | 1.08 | 2.23 | 1.11/0.92 | 0.89 |
| `qML9NQ12` | pred_one_day_14 单腿 | 1.67 | 1.04 | 2.07 | 1.04/0.89 | 0.88 |

### 1.4 FUNDAMENTAL 塔 · fundamental23（10 颗，S 1.69–1.73）

结构 `add(sig(主腿), 0.7~0.85×sig(fnd23_intfvalld1_vbts))`，EUR/**TOP2500**。

| alpha | 主腿 | S | F | 2Y | sub/lim |
|---|---|---|---:|---:|---|
| `mLowboV5` | `bank_assets_investment` | 1.73 | 1.06 | 2.42 | 0.91/0.90 |
| `LLMV7l3e` | `fnd23_intfvalld1_iabs` | 1.73 | 1.06 | 2.42 | 0.91/0.90 |
| `mLowbo55` | bank（vbts 0.75） | 1.72 | 1.04 | 2.44 | 0.91/0.89 |
| `A1VjPVGE` | bank（1.2/0.9） | 1.72 | 1.04 | 2.44 | 0.91/0.89 |
| `O0AQ75g7` | `..._iads` | 1.72 | 1.05 | 2.43 | 0.90/0.89 |
| `ZYQPnQK1` | bank（vbts 0.8） | 1.71 | 1.03 | 2.45 | 0.91/0.89 |
| `0mYOEYpq` | bank（vbts 0.85） | 1.69 | 1.01 | 2.46 | 0.91/0.88 |
| `0mYOwK52` | `..._fbds` | 1.69 | 1.02 | 2.29 | 0.89/0.88 |
| `QPvZKbdr` | `..._sebv` | 1.69 | 1.02 | 2.12 | 0.92/0.88 |
| `kqNEgo58` | `..._sedv` | 1.69 | 1.02 | 2.12 | 0.92/0.88 |

> 注意：`sebv`/`sedv`/`iads` 的 S/2Y 与 bank 高度相似（1.69/2.12~2.43），说明这四个字段可能是同一报表的相邻科目 ⇒ **self corr 需实测**，可能只能出 1–2 席。

---

## 2 prod 实测：地板 0.74

| alpha | 结构 | S | **prod** | 直方图（>0.7 对手） |
|---|---|---:|---:|---:|
| `zq3Kk39K` | 跨集三腿 | 2.78 | **0.7508** | 5 颗 |
| `P0oQoVQL` | 4 腿正交 | 2.36 | **0.7408** | 8 颗 |
| `QPvZEQXX` | techindi 混合 | 1.93 | **0.7481** | 2 颗 |
| `mLowboV5` | fund23 单腿+辅 | 1.73 | **0.7971** | 15 颗（成片） |

**S 从 1.73 到 2.78 全部试过，prod 无一低于 0.74** ⇒ prod 与信号强度无关。

对比：`rKRpEMWo`（model25 合成因子，S 1.75）prod **0.594**，是全 EUR 唯一 <0.70 的。

---

## 3 为什么 model25 能到 0.594

`model25` 的 `value_momentum_industry_rank_float` 是**多因子合成的行业内排名**（不是单一财务科目）。
生产池里没有任何单一 alpha 与「合成排名」高相关 ⇒ prod 天然低。

已确认**未点亮塔里不存在同类字段**：
- `fundamental28` 的 1605 个字段全是原始科目（`fnd28_anlev_value_*`），合成型关键词命中 **0**
- `fundamental23` 的 1662 个字段同理（`fnd23_intfvalld1_*` 全是报表科目缩写）
- `pv87` 的 `ann_matrix_*` 是分析师估算统计量（high/low/mean/median），非合成排名
- `other455` 是 node2vec+PCA 图因子，但全弱（S −0.46~0.39）

---

## 4 已否证的 6 条降 prod 路径

| # | 路径 | 具体 | 结果 |
|---|---|---|---|
| 1 | 换字段 | 40+ 字段宽扫（fundamental23 30 个 / techindi 20 个 / other455 18 个 / pv87 10 个） | 同族 Δprod ≤0.05 |
| 2 | 同集混合 | fund23 6 变体 / techindi 4 变体 | 0.797 / 0.748 |
| 3 | 跨集混合 | 基本面 × 技术 × 预测 | 0.7508（S 2.78） |
| 4 | 多腿正交 | 4 腿（+机构/社媒） | 0.7408（S 2.36） |
| 5 | 另类数据当主腿 | 社媒/机构做主体 | 信号太弱（S 1.58 / **F 0.71**） |
| 6 | 破 ATOM（市值中性化） | `vector_neut(rank(cap))` / `group_neutralize(bucket(rank(cap)))` | sub 未修好且新增 IS_LADDER FAIL |

---

## 5 已标死的集（省后续投入）

| 集 | 塔 | 证据 |
|---|---|---|
| `other455` | OTHER | 18 个字段全弱（S −0.46~0.39） |
| `pv87` | PV | 10 个字段全弱（S 0~0.67） |
| `pv20` | PV | 字段为 `adv*`/`alternative_slippage_*`（流动性成本，非信号） |
| `fundamental31` / `ml_factor_proj` | — | **幽灵集**（平台认证 0 字段） |

**PV 塔在 EUR 基本无解**（5 个集全部标死或弱）。

---

## 6 工程结论（可复用）

1. **`sub/S` 是字段常数**（7 条参数轴全在 0.44–0.48），但**复合后可改**：混入偏小票的弱字段可把 ratio 抬到 0.53+。
2. **`limit = 0.535 × S`**（EUR）⇒ 不是「ratio 越高越好」，而是「sub ≥ 0.535×S」的联合条件；S 略降会让 limit 同步降，可能反而过关。
3. **universe 是硬条件不是可选项**：`CORE3`（fund23+techindi 混合）在 TOP2500 上 S 2.78，在 TOPCS1600 上**连纯结构都 FAIL**。
4. **低覆盖腿会废掉整批**：cov < 0.7 的字段在 TOP2500 上 NaN 过多 ⇒ 整批 ERROR。三次踩坑（`P1_fund` / `J_leg4` / `N_altmain`）。**提交前必须 preflight + 覆盖率门槛 ≥0.85**。
5. **破 ATOM 免 2Y 但需过 IS_LADDER**（2.02）：对 2Y 不足而 ladder 稳健的组合是净收益；对不稳健构造是负收益。

---

## 7 交付建议

**A. 若必须凑 10 个**：从 §1.3（techindi 7 颗）与 §1.4（fund23 10 颗）中各取，但**需先测 self corr**（同字段族可能 >0.7 只能出 1–2 席），且 prod 均不达标。

**B. 若接受 prod 现实**：25 颗 IS 全过候选可直接作为「待 prod 改善」的库存；一旦平台生产池变化或找到新机制，可重新测。

**C. 若可放宽 region**：`rKRpEMWo` 的配方（合成因子 + 弱辅腿）在 GBR/KOR/IND 的生产池完全不同，prod 有机会 <0.70。
