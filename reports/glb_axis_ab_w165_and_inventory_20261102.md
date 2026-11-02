# GLB 中性化轴 A/B 结案 + 库存重建（2026-11-02）

> 承接 `reports/glb_neutralization_axis_breakthrough_20261102.md`（全库轴统计）。
> 本文回答该报告留下的两个问题：①轴结论能不能直接套到具体信号族？②当前真正的提交瓶颈在哪？

---

## 1. w165 单杠杆 A/B 结案：轴效应是「族依赖」的

**设计**：w162+w163 的 6 条最优表达式**逐字符原样**，唯一变量 `neutralization` 由
`STATISTICAL` 改为 `SUBINDUSTRY`。其余设置（decay=10 / trunc=0.08 / maxTrade=OFF /
maxPosition=OFF / nanHandling=OFF）完全一致。
multisim `43Yjm15tC4q1afxqZ6RtONX`，6/6 COMPLETE。

### 1.1 INST 门控族：严格对照 ⇒ SUBINDUSTRY 更差

| 表达式 | STATISTICAL (w163) | SUBINDUSTRY (w165) | Δ 2Y |
|---|---|---|---|
| `num_held W66 + probability_label1_2@market` | `QPvQ1v3g` S2.35/F1.13/**2Y1.51**/sub2.09/**fRA1** | `A1V31oOe` S1.90/F1.17/**2Y1.19**/sub1.85/**fRA3** | **−0.32** |
| `num_held W66 + single_bucket_20day@country` | `bl69Y6RN` S2.27/F1.05/**2Y1.30**/sub1.98/**fRA1** | `WjOgjvak` S1.93/F1.10/**2Y1.39**/sub1.80/**fRA2** | +0.09 |

`A1V31oOe` 额外挂 `LOW_GLB_EMEA_SHARPE`(0.58) + `LOW_GLB_APAC_SHARPE`(0.92)：
换轴把原本只差 0.07 的近闸件变成三处失败。

⇒ **对 INST 门控族，SUBINDUSTRY 反向**。门控族判封。

### 1.2 SENTIMENT 门控族：4/4 全净

| alpha | 骨架 | S | F | TO | 2Y | sub | fRA |
|---|---|---|---|---|---|---|---|
| **`j2Yg2q9j`** | snt W66 + probability_label1_2quantile@country | **2.73** | **2.02** | 14.69% | **2.85** | **2.22** | **0** |
| **`58Ev8PLN`** | snt W22 + probability_label1_2quantile@country | 2.52 | 1.54 | 18.89% | 2.83 | **2.26** | **0** |
| **`xArnAJPp`** | snt W66 + quantile_label_4bucket@country | 2.26 | 1.47 | 17.48% | 2.47 | 1.78 | **0** |
| **`j2Yg2qnj`** | snt W22 + quantile_label_4bucket@country | 2.04 | 1.13 | 21.30% | 2.23 | 1.84 | **0** |

塔位均为 `GLB/D1/OTHER` + `GLB/D1/SENTIMENT`。
**注意**：snt 族在 w163 没有 STATISTICAL 对照，所以这是「增益证据」而非严格 A/B。

### 1.3 修正上一轮过强口径

上一轮结论「GLB 后续所有波次默认轴改为 FAST 或 SUBINDUSTRY，禁用 STATISTICAL」需要收窄为：

> **默认轴**可用全库统计定（STATISTICAL 干净率 1.04% vs SUBINDUSTRY 28.84% / FAST 36.43%）；
> 但**单族层面**必须做单杠杆 A/B，因为同表达式在不同轴上的 2Y 可以反向移动 0.32。

---

## 2. 新瓶颈：族内互相关，不是 prod 墙

对 w165 四颗净件 + 已有 `Xg9rMdvl` 共 5 颗 snt 族件跑
`compute_mutual_correlation(threshold=0.7, years=4)`：

- `max_mutually_below_subset` = `[Xg9rMdvl, xArnAJPp]`，**size = 2**，`max_subset_exact = true`
- 该对相关 **0.6906**（余量 0.0094，比 prod 48h 漂移还薄）
- 最大对：`Xg9rMdvl ↔ 58Ev8PLN` = **0.9804**
- `j2Yg2q9j ↔ xArnAJPp` = 0.869、`58Ev8PLN ↔ j2Yg2qnj` = 0.863、`Xg9rMdvl ↔ j2Yg2qnj` = 0.844

⇒ **四颗全净件的真实净增量约 +0~1，不是 +4。**

**必须建立的新口径**：评估一波成果要同时报两个数——
「全净件数」（fRA=0）与「可叠进篮子的净件数」（受族内互相关约束）。前者是产能，后者是库存。

### 代表件选择

`j2Yg2q9j` 在 S / F / 2Y / TO 四项全面优于已验 prod 的 `Xg9rMdvl`：

| | S | F | 2Y | TO | prod |
|---|---|---|---|---|---|
| `j2Yg2q9j` | 2.73 | 2.02 | 2.85 | 14.69% | 待测 |
| `Xg9rMdvl` | 2.44 | 1.47 | 2.69 | 19.06% | **0.6512 ✓** |

替换条件：`j2Yg2q9j` prod 通过。

---

## 3. 库存重建：最大互不相关篮 5 → 10

合并三表（`alphas` / `alpha_corr_cache` / `submit_ready`）的 prod/self，扫
`backtest_results.region='GLB' AND ra_failed_checks='[]' AND sharpe≥2.30 AND fitness≥1.20 AND two_year_sharpe≥2.00`：

- GLB 全净 2Y≥2.0 件：**67 颗 / 49 个族**
- 剔除 prod≥0.70 与 self≥0.70 后仍活：**29 个族**

对 13 颗主候选跑 `compute_mutual_correlation(threshold=0.7)`：
`max_subset_exact = true`，**最大互不相关篮 = 10 颗**。

| # | alpha | 组合 | 轴 | S | F | TO | 2Y | sub | prod |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `QPvJ6KVw` | RISK+OTHER | FAST | 3.19 | 1.59 | 28.97% | 3.43 | 1.84 | **0.6385 ✓** |
| 2 | `npv9WLVE` | RISK+OTHER | SUBIND | 3.08 | 1.42 | **60.83%** | 3.19 | 2.38 | **0.6638 ✓** |
| 3 | `RRE3O8r1` | FUND+OTHER | FAST | 2.89 | 1.73 | 16.02% | 2.13 | 1.71 | **0.6479 ✓** |
| 4 | `d5WqeQbx` | FUND+OTHER | FAST | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | **0.5846 ✓** |
| 5 | `Xg9rMdvl` | OTHER+SENT | SUBIND | 2.44 | 1.47 | 19.06% | 2.69 | 2.22 | **0.6512 ✓** |
| 6 | `LLMaXwv6` | **PV 单塔** | FAST | 2.78 | 1.42 | 36.54% | 2.99 | 1.51 | 待测 |
| 7 | `9qxJgv5x` | **OTHER 单塔** | FAST | 2.38 | 1.36 | 5.10% | 3.01 | 1.60 | 待测 |
| 8 | `E5672lMG` | RISK+OTHER | SUBIND | 2.43 | 1.81 | 11.82% | 3.15 | 2.27 | 待测 |
| 9 | `6Xd8dgzL` | EARNINGS+OTHER | SUBIND | 2.67 | 1.56 | 20.92% | 3.31 | 2.32 | 待测 |
| 10 | `mLoqmkd5` | INST+OTHER | FAST | 2.76 | 1.89 | 13.76% | 2.73 | 2.10 | 待测 |

被排除（互相关 >0.7）：`xArRX6Lb`（↔`9qxJgv5x` 0.9102）、`0mYl5r11`（↔`6Xd8dgzL` 0.9783）、
`QPvnbd0g`（多对 0.70–0.87）。

### 3.1 两颗免配额单塔件（结构性关键）

| alpha | 塔位（平台 `pyramids.list`） | 结论 |
|---|---|---|
| `LLMaXwv6` | `GLB/D1/PV`（倍率 1.0） | PV 塔现 2/3 ⇒ 提这颗即点亮 |
| `9qxJgv5x` | `GLB/D1/OTHER`（倍率 1.2） | OTHER 已点亮，纯免配额库存 |

两者 `checks.fail = []`，AMER / EMEA / APAC 三处区域闸**全过**
（此前 8 颗 PV 件全部卡 `LOW_GLB_EMEA_SHARPE`，6 个轴都救不了 —— 说明这是**信号族**属性，
而 `mean_high_price_return_30m_pre_close_2` 这一族没有该问题）。

`LLMaXwv6` 覆盖 `get_alpha_yearly_stats`：2014–2023 **十年全有数据**（longCount 5298–7176、pnl 全正）。
`9qxJgv5x` 同为十年全覆盖，但 **2020 年 sharpe −1.41 / pnl −224,360**（全年亏损），属稳健性瑕疵。

### 3.2 配额账

两塔组合上限：**5 个组合名 × 每名 ≤3 颗 = 15 颗**；单塔（`len(combo)==1`）不占配额。

| 组合名 | 已用 | 上限 | 余量 |
|---|---|---|---|
| RISK+OTHER | 3（`QPvJ6KVw`/`npv9WLVE`/`E5672lMG`） | 3 | **满** |
| FUND+OTHER | 2（`RRE3O8r1`/`d5WqeQbx`） | 3 | 1 |
| OTHER+SENT | 1（`Xg9rMdvl`） | 3 | 2 |
| EARNINGS+OTHER | 1（`6Xd8dgzL`） | 3 | 2 |
| INST+OTHER | 1（`mLoqmkd5`） | 3 | 2 |
| （单塔） | 2（`LLMaXwv6`/`9qxJgv5x`） | ∞ | — |

组合名已用满 **5/5** ⇒ 后续两塔只能在这 5 个名字里加，**不能再开新组合名**。
两塔余量合计 7 颗 ⇒ 两塔上限 15 颗不变；**单塔是唯一能超过 15 的路径**。

---

## 4. prod 实测汇总（本轮）

| alpha | prod | n[0.7,0.8) | 判定 |
|---|---|---|---|
| `QPvQ1v3g` | 0.505 | 0 | PASS |
| `bl69Y6RN` | 0.4994 | 0 | PASS |
| `0mYz113v` | 0.4763 | 0 | PASS |

三颗近闸件的卡点**纯为 2Y/ladder，不是 prod 墙**。

---

## 5. 待办与开放问题

1. **提交授权**（阻塞，2026-11-01 五次问卷均超时自动选中，不算授权）
2. `LLMaXwv6` / `9qxJgv5x` / `E5672lMG` / `6Xd8dgzL` / `j2Yg2q9j` / `mLoqmkd5` 的 prod 待测
3. w166（`1FdeUgb6Z5i7at8duivkFuw`，同 6 条 + FAST）在飞，用于补全轴 A/B
4. **点亮 SENTIMENT 塔**需 3 颗，但 snt 族内互相关只允许 1–2 颗 ⇒ 需要换 snt 字段（而非换窗口）造新的去相关α
5. 日配额 **4 颗/天** ⇒ 即便全授权，10 颗篮需 3 天

---

## 附：本轮产物

- `results/_tmp_scan2y_glb.py` 全库扫 GLB 全净 2Y≥2.0
- `results/_tmp_merged.py` 三表合并 prod/self 得 29 个活族
- `results/_tmp_dsmap.py` / `_tmp_ds1786.py` 候选→数据集映射（发现 `dataset_id=1786` 是 `_unknown` 占位符，DB 塔归属不可信）
- 台账 `glb_axis_ab_w165_20261102`
- `wave_results` GLB/165 verdict=PASS n_pass=4
