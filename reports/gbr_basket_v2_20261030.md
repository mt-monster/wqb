# GBR 篮子 v2 —— 8 条扩到 10 条（2026-10-30）

区域设置：`GBR / TOP700 / D1`。IS 区间 `2014-01-01 ~ 2023-12-31`（满足「近十年都要有数据」硬门槛）。
相关性口径：`compute_mutual_correlation(threshold=0.7, years=4)`，**1021 个日收益点**，`missing_pnl: []`。

---

## 1. 最终篮子（10 条）

| # | alpha | 塔位（平台 pyramids） | S | F | 2Y | SUB | TO | margin | prod | self-corr | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `P0gvv5gE` | ANALYST | — | 1.03 | 1.84 | — | — | — | 0.6905 ⚠陈旧 21 天 | 0.6364 | 0 |
| 2 | `9qWwZ3go` | MODEL | — | — | — | — | — | — | 0.6890 ⚠陈旧 21 天 | 0.5952 | 0 |
| 3 | `6XKwmQgE` | ANALYST | — | — | — | — | — | — | 0.5956 ⚠陈旧 21 天 | 0.4148 | 0 |
| 4 | `rKRkL9QE` | PV+FUNDAMENTAL | 2.21 | 2.05 | 2.51 | 1.77 | 8.33% | 22.31bp | 0.6783 ✅新鲜 | 0.5456 | 0 |
| 5 | `0mYoANkv` | PV+FUNDAMENTAL | — | — | — | — | — | — | **0.6932 ✅本轮实测** | 0.5210 | 0 |
| 6 | `WjOkLGWx` | PV+FUNDAMENTAL | — | — | — | — | — | — | **未测** | 0.4955 | 0 |
| 7 | `omWKpjgJ` | MODEL | — | — | — | — | — | — | **未测** | 0.3651 | 0 |
| 8 | `KPmlLE3E` | PV | — | — | — | — | — | — | **未测** | 0.3314 | 0 |
| **9** | **`xAb2OkMm`** 🆕 | **ANALYST**（乘数 **1.6**） | **2.13** | **1.71** | 1.74 | 1.23 | 9.38% | 17.17bp | **未测** | **0.3673** | **0** |
| **10** | **`xAbd9YEJ`** 🆕 | **ANALYST** | 1.59 | 1.07 | **2.16** | 1.10 | 11.78% | 9.68bp | **未测** | **0.2693** | **0** |

两条新增候选的表达式（均为**纯 ANALYST 单塔**，不占 trio×非trio 配额）：

```
xAb2OkMm  subtract(rank(est_12m_pre_raisednum_1mth), rank(est_12m_pre_lowerednum_1mth))
xAbd9YEJ  group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(est_12m_pre_low,500),105)),
          lambda_min=0, lambda_max=1, target_tvr=0.13), sector)
```

- `xAb2OkMm` 是**分析师评级上调/下调家数差**（revision breadth），落库形态 `subtract(rank, rank)`，属既定放行形态；设置 `decay 4 / REVERSION_AND_MOMENTUM / trunc 0.08 / nanHandling ON / maxTrade ON`。
- `xAbd9YEJ` 是 `est_12m_pre_low`（最低预期）的 105 日变化，平台设置 `FAST` 中性化。
- `xAb2OkMm` 平台 `checks.fail: []`，仅剩 `SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION / POWER_POOL_CORRELATION` 五项 pending；self 已在本地算得 0.3673 PASS。

## 2. 互相关体检（10×10）

- **最大配对：`0mYoANkv × WjOkLGWx = 0.5615`**，远低于 0.7。
- `pairs_over_threshold: []`、`all_below_threshold: true`、`max_subset_exact: true`、`max_mutually_below_subset` 长度 **= 10**（即 10 条全部可同时入篮）。
- 两条新增对现有 8 条的最大 |相关|：`xAb2OkMm` 为 `0.1031`（vs `rKRkL9QE`）、`xAbd9YEJ` 为 `-0.2065`（vs `WjOkLGWx`）⇒ **近乎完全正交，扩篮零相关代价**。
- 两者彼此 0.4352，同样低于 0.7。

⇒ 这是本轮最硬的结论：**篮子可以从 8 条无代价扩到 10 条，不需要放弃任何一条**。

## 3. 本轮怎么找到这两条的（可复用方法）

### 3.1 从数据集排名缓存反查「未点亮塔的未试数据集」

`tracking/GBR/reference/gbr_dataset_ranking.json`（2026-08-19，183 个数据集）按 category 汇总后，
`cov > 0` 的分布是：model 8 / analyst 8 / other 11 / news 6 / pv 4 / fundamental 4 / institutions 4 /
sentiment 3 / risk 2 / insiders 2 / shortinterest 1 / socialmedia 1 / earnings 0 / macro 0 / option 0 / imbalance 0。

其中**从未回测过**且 `cov > 0` 的只有 6 个：`socialmedia39`(0.4948) / `institutions4`(0.39) /
`institutions1`(0.3118) / `fundamental31`(0.4301) / `analyst93`(0.5926) / `analyst83`(0.3305) / `pv109`(0.3319)。

副产品：`sentiment27` 实际就是 `snl27_*` 字段族，本地 190 条回测里**最高 S 只有 1.33 / F 0.92**，
与既有「snl27 天花板 1.33」判死结论一致 ⇒ **SENTIMENT 塔确认无现成路径**。

### 3.2 全库扫「全闸通过但未提交」的存量候选（最高产的一步）

```sql
SELECT alpha_id, dataset_id, sharpe, fitness, two_year_sharpe, sub_universe_sharpe, turnover, ...
FROM alphas
WHERE region_id=7
  AND sharpe>=1.58 AND fitness>=1.0 AND two_year_sharpe>=1.58 AND turnover<=0.70
  AND (sub_universe_sharpe IS NULL OR sub_universe_sharpe >= 0.4743*sharpe)
  AND (stage IS NULL OR stage!='OS') AND date_submitted IS NULL
  AND (status IS NULL OR status NOT IN ('ACTIVE','SUBMITTED','OS','SUPERSEDED'))
```

返回 **303 条**（其中无 `+` 的纯单数据集 217 条）。这是此前一直没做过的视角——
一直在「新开波挖新字段」，而库里躺着现成的过闸候选。

### 3.3 ★ 关键陷阱：`region_id=7` 混入 EUR / GLB，必须用 `alphas.universe` 二次过滤

对这 303 条抽样做 `get_alpha_details` + 本地 `universe` 列交叉核验，发现：

| alpha | `alphas.universe` | 平台实读 region | 结论 |
|---|---|---|---|
| `RR6KEmwn` | TOPCS1600 | EUR | ✗ 排除 |
| `XgJe9oAa` | TOPCS1600 | EUR / TOPCS1600 | ✗ 排除（且 `LOW_ROBUST_UNIVERSE_SHARPE` 0.56 < 0.7 FAIL） |
| `LLZrMGoa` | TOPCS1600 | EUR | ✗ 排除 |
| `58geEpK5` | TOPCS1600 | EUR | ✗ 排除 |
| `P0oerpjp` | TOP700 | GBR | ✓ |
| `xAb2OkMm` | TOP700 | **GBR / TOP700 / D1** | ✓ |

那 4 条 `fnd72_pit_or_*` 看着是「纯 FUNDAMENTAL 不占配额、可点亮 FUNDAMENTAL 塔」的理想货，
实际全是 **EUR**，而且 `robust_universe_sharpe` 0.53–0.64 全部低于 0.7 闸。
⇒ **`region_id` 不可作为区域判据，`alphas.universe`（TOP700 vs TOPCS1600）才是本地可用的过滤器**；
最终仍以 `get_alpha_details.settings.region` 为准。

### 3.4 `fnd6_capxy / cap` 族的 4 条已过闸变体：不建议进篮

`P0oerpjp`(168/56) / `QPveQvOg`(二阶差分) / `N1NM5WK8`(+group_rank industry) / `9qxoa3mx`(cap/ceq 反向)
全部 `failed_ra 0`、S 1.59–2.06、F 1.35–1.80，但：

1. 都是 **PV+FUNDAMENTAL**（含 `cap`）⇒ 每条吃掉 1 个 trio×非trio 配额，而配额已用 4/5；
2. 与已入篮的 `rKRkL9QE` 同核（同分母 `cap` + 同位移算子），换窗口/换二阶只会得到 >0.7 的相关。

⇒ 保留 `rKRkL9QE` 作该族代表，其余 4 条**不入篮**。

## 4. 仍待补的 prod（账号级单并发，最大瓶颈）

未测 5 条：`WjOkLGWx`（**FUNDAMENTAL 点塔关键**）、`omWKpjgJ`、`KPmlLE3E`、`xAb2OkMm`、`xAbd9YEJ`。
陈旧需刷新 2 条：`P0gvv5gE`（0.6905，余量 0.0095）、`9qWwZ3go`（0.6890，余量 0.011）。
近墙需复测 1 条：`0mYoANkv`（0.6932，余量 0.0068）。

本轮三次尝试均被兄弟会话占用（holder 依次为 `O0Jgd7Y7` → `vROPEJ8w`），未抢到槽。

## 5. 提交后的塔位效果（提交前平台实读 `model 5 / analyst 3 / pv 1 / other 1`）

- **PV 1 → 5**（`rKRkL9QE` + `0mYoANkv` + `WjOkLGWx` + `KPmlLE3E`）✅ 点亮
- **FUNDAMENTAL 0 → 3**（`rKRkL9QE` + `0mYoANkv` + `WjOkLGWx`）✅ 点亮，**依赖 `WjOkLGWx` 过 prod**
- ANALYST 3 → 5（+`P0gvv5gE` +`6XKwmQgE`，再加 2 条新候选可到 7）
- MODEL 5 → 7（+`9qWwZ3go` +`omWKpjgJ`）
- OTHER 仍 1 ❌（本季度 GBR OTHER 塔已结构性判死）
