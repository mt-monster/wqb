# EUR 首颗全过候选：`rKRpEMWo`（三腿混合，保 ATOM）

> 2026-10-27 ｜ 平台判定实测 ｜ **未提交**（按项目政策：只挖不提交，提交权归用户）

---

## 1 结论

`rKRpEMWo` **通过全部 IS 闸 + self + prod 相关性**，`FAIL` 列表为空，`MATCHES_PYRAMID` PASS（单数据集 ATOM 合规）。

这是 EUR 战役至今第一颗走完全部闸门的 Regular Alpha。此前 6 颗候选全部止步（prod 4 颗 0.75–0.91、sub 2 颗 0.87/0.99）。

---

## 2 表达式

```
add(add(signed_power(rank(ts_backfill(value_momentum_industry_rank_float, 22)), 0.5),
        1.2 × signed_power(rank(ts_backfill(mdl25_74v, 22)), 0.5)),
    1.2 × signed_power(rank(ts_backfill(mdl25_81v, 22)), 0.5))
```

设置：

```
region=EUR  instrument=EQUITY  universe=TOPCS1600  delay=1
decay=4  neutralization=FAST  truncation=0.08
nanHandling=ON  maxTrade=ON  pasteurization=ON  unitHandling=VERIFY
```

三个字段**全部属于 `model25`** ⇒ `effective=1`，`MATCHES_PYRAMID` PASS。

---

## 3 闸门结果（平台实测）

| 闸 | 值 | limit | 结果 |
|---|---:|---:|---|
| LOW_SHARPE | **1.75** | 1.58 | **PASS** |
| LOW_FITNESS | **1.20** | 1.00 | **PASS** |
| LOW_2Y_SHARPE | **1.60** | 1.58 | **PASS** |
| LOW_SUB_UNIVERSE_SHARPE | **1.02** | 0.93 | **PASS** |
| LOW_ROBUST_UNIVERSE_SHARPE | **0.73** | 0.70 | **PASS** |
| LOW_TURNOVER / HIGH_TURNOVER | 4.76% | 1% / 70% | **PASS** |
| CONCENTRATED_WEIGHT | — | — | **PASS** |
| MATCHES_PYRAMID | — | — | **PASS** |
| **SELF_CORRELATION** | **0.352** | 0.70 | **PASS**（top1 = `blRaArVZ` 0.352） |
| **PROD_CORRELATION** | **0.594** | 0.70 | **PASS** |
| **FAIL 列表** | | | **空** |
| CLUSTER_TEST | 1.07 | 1.58 | WARNING（非 FAIL） |
| MATCHES_THEMES / OSMOSIS_ALLOCATION | — | — | WARNING（非 FAIL） |

绩效：returns **5.86%** ｜ drawdown **5.66%** ｜ margin **24.6bp** ｜ TO 4.76%

---

## 4 怎么找到的：从「sub 死结」到「三腿互补」

### 4.1 起点：sub 看似无解

`kqJAPA2l`（`signed_power(rank(bf(mdl25_6v,22)),0.5)`）S 1.85 / F 1.28 / 2Y 1.58 / rob 0.94 全过，
**唯一 FAIL = sub 0.87 / limit 0.99**。

7 条参数轴全部无效，`sub/S` 稳定在 **0.44–0.48**：

| 轴 | 变体 | sub/S |
|---|---|---:|
| 基准 | CS1600 / decay4 / trunc.08 / FAST | 0.465 |
| decay | 8 / 16 | 0.462–0.467 |
| truncation | 0.04 | 0.465 |
| universe | TOP2500 / TOP1200 | 0.342 / 0.609（S 崩到 0.92） |
| group_rank / group_scale | subindustry | 0.478 / 0.444 |
| neutralization | MARKET | 0.457 |
| **破 ATOM** | `vector_neut(sig, rank(cap))` | 0.503（且新增 `IS_LADDER_SHARPE` FAIL） |

**结论：`sub/S` 是该字段的常数，参数轴改不了。**

### 4.2 转折：`sub/S` 虽是字段常数，但**复合后的** sub/S 可以改

`model25` 有 **417 个 MATRIX 字段、cov 1.000、全部 `n_tests=0`**（今天之前只用了 1 个）。
逐字段扫描（同结构、同设置）后发现字段之间存在明确的**闸门互补**：

| 字段 | 单独 S | 单独 2Y | 单独 sub/S | 角色 |
|---|---:|---:|---:|---|
| `value_momentum_industry_rank_float` | **2.53** | 1.75 | 0.458 | **主腿**（提供 S 与 F，F 达 2.04） |
| `mdl25_74v` | 0.41 | 0.52 | **1.463** | **抬 sub**（信号偏小票） |
| `mdl25_81v` | 0.25 | 1.30 | 0.880 | **抬 2Y** |
| `mdl25_01v` | 0.29 | 1.43 | 1.034 | 抬 sub（次选） |
| `mdl25_22v` | 1.86 | 1.62 | 0.468 | 与 6v 同质 |

**弱字段不是废字段。** `mdl25_74v` 单独看是 DEAD（S 0.41），但它偏小票，恰好补上主腿「偏大票」的短板。

### 4.3 权重规律（实测）

**74v 权重 ↑**：sub 升、2Y 升、rob 升、S 微降

| 74v 权重 | S | 2Y | sub/limit | ratio | rob |
|---:|---:|---:|---|---:|---:|
| 0（纯主腿） | 2.53 | 1.75 | 1.16 / 1.34 | 0.458 | — |
| 1.0 | 2.07 | 1.43 | 1.10 / 1.10 | 0.531 | 0.87 |
| 1.2 | 2.05 | 1.45 | 1.12 / 1.09 | 0.546 | — |
| 1.5 | 2.02 | 1.48 | 1.14 / 1.07 | 0.564 | 0.90 |

**81v 权重 ↑**：2Y 升、sub 与 rob 降

| 81v 权重 | S | 2Y | sub/limit | rob |
|---:|---:|---:|---|---:|
| 1.0 | 1.82（1.0/1.0 三腿） | 1.58 == limit → FAIL | 1.03 / 0.97 | 0.74 |
| **1.2** | **1.75** | **1.60 PASS** | **1.02 / 0.93** | **0.73** |
| 2.0 | 1.69 | 1.88 | 0.91 / 0.90 | **0.42 FAIL** |

⇒ 双辅腿各管一个闸，**权重 1.2/1.2 是可行域中心**。

---

## 5 同批产出的另外三颗（IS 全过，余量更足，prod 待测）

| alpha | 变体 | S | F | rob | 2Y | sub / limit | CLUSTER |
|---|---|---:|---:|---:|---:|---|---:|
| `0mYOdaoq` | 74v 1.5 / 81v 1.0 | **1.79** | **1.23** | **0.78** | 1.59 | 1.06 / 0.95 | 1.09 |
| `leAp2Nxx` | 74v 1.5 / 81v 1.2 | 1.74 | 1.18 | 0.75 | **1.61** | 1.04 / 0.92 | 1.02 |
| `zq3KjLaR` | 74v 1.8 / 81v 1.2 | 1.71 | 1.15 | 0.76 | **1.61** | 1.05 / 0.91 | **0.97** |

三颗 `FAIL` 均为空。`0mYOdaoq` 的 rob 余量最大（0.78），`zq3KjLaR` 的 CLUSTER_TEST 最低（0.97）。

---

## 6 为什么 prod 只有 0.594（此前候选 0.75–0.91）

| 候选 | 主字段 | prod |
|---|---|---:|
| `JjejYA3e` | `snt26_relpopularity1` | 0.7534 |
| `RREJewKz` | `oth335_combined_all_region_hedge` | 0.8290 |
| `vROPXLNa` | `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` | 0.8511 |
| `VkdeWGgw` | `quantile_label_1bucket_5day_ohlcv_2` | 0.9114 |
| **`rKRpEMWo`** | **`value_momentum_industry_rank_float` + `mdl25_74v` + `mdl25_81v`** | **0.594** |

前四颗的主字段都是**已在生产池中的成熟因子**（技术指标模型分、综合对冲分、OHLCV 标签）。
`model25` 的 417 个字段**从未被挖过**（`n_tests=0`）⇒ 与现有生产 alpha 天然低相关。

**这条是降 prod 的正统路径：「挖没人挖过的字段」，而不是「改造已挖过的字段」。**

---

## 7 未做的事（按政策）

- **未提交**。`ALLOW_ALPHA_SUBMIT=False` 全局锁有效，提交权归用户。
- 若要提交，需用户点名该 alpha；提交前建议再跑一次 `check_correlation(refresh=True)` 确认 prod 未漂移（memory §1：prod 台账 5 天作废）。
- `CLUSTER_TEST 1.07` 是 WARNING（非 FAIL），但若平台后续收紧到 FAIL，则需再降簇。
