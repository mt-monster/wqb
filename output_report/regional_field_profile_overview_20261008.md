# 全区域字段画像总览（2026-10-08）

> 数据源：`data/wqb.db::field_profile_perf`（多区域主表，复合主键 `region+dataset+field`）
> 工具：`tools/fields/field_profile.py`｜每区只读视图：`field_profile_<region小写>`
> 生成方式：`tools/fields/field_profile.py --all-regions`（13 区一次建成，**互不串号**）

---

## 一、总览

| 指标 | 值 |
|---|---|
| 已建画像区域 | **13 个** |
| 画像总行数 | **293,060** |
| 隔离验证 | 13 个视图**全部单区纯度 100%** ✅ |
| 合计活/弱字段 | **489**（ALIVE 243 + WEAK 246） |
| 合计未测字段 | **208,199** |

**⇒ 每个区域都有独立视图，查询体验等同"每区一张独立表"，且建新区不影响已建区。**

---

## 二、各区域画像规模（按总字段降序）

| region | 总字段 | 已测 | 未测 | **ALIVE** | WEAK | 判死系 | 视图 |
|---|---:|---:|---:|---:|---:|---:|---|
| USA | 85,184 | 364 | 61,423 | **17** | 23 | 324 | `field_profile_usa` |
| EUR | 38,609 | 316 | 21,928 | **5** | 6 | 305 | `field_profile_eur` |
| KOR | 33,618 | 160 | 23,239 | **18** | 19 | 123 | `field_profile_kor` |
| **GLB** | 28,465 | 542 | 19,639 | **60** | **67** | 415 | `field_profile_glb` |
| HKG | 25,648 | 55 | 17,815 | 0 | 14 | 41 | `field_profile_hkg` |
| DEU | 22,494 | 419 | 3,225 | **2** | 28 | 389 | `field_profile_deu` |
| GBR | 15,522 | 285 | 2,823 | **19** | 9 | 257 | `field_profile_gbr` |
| ASI | 14,730 | 193 | 9,716 | **32** | 24 | 137 | `field_profile_asi` |
| **IND** | 14,334 | 206 | 10,770 | **54** | 15 | 137 | `field_profile_ind` |
| JPN | 5,849 | 107 | 5,508 | 0 | 0 | 107 | `field_profile_jpn` |
| CHN | 5,730 | 18 | 4,937 | 0 | 0 | 18 | `field_profile_chn` |
| MEA | 2,115 | 81 | 689 | **15** | 9 | 57 | `field_profile_mea` |
| AMR | 762 | 36 | 546 | 0 | 2 | 34 | `field_profile_amr` |

**★ 已测密度（已测/总字段）差异极大**：DEU 1.9%｜GBR 1.8%｜MEA 3.8%｜AMR 4.7%｜IND 1.4% ｜ vs  USA 0.4%｜KOR 0.5%｜GLB 1.9%
⇒ **DEU/GBR/MEA 的实测覆盖最充分**（战役做得深）；**USA/KOR/HKG 几乎未动**（未测池 6.1 万 / 2.3 万 / 1.8 万）。

---

## 三、★ ALIVE 排行（选区与迁移的直接依据）

| 排名 | region | ALIVE | 说明 |
|---:|---|---:|---|
| 1 | **GLB** | **60** | 全域池最大，且 WEAK 也是最多（67） |
| 2 | **IND** | **54** | S 峰值最高（见下） |
| 3 | ASI | 32 | |
| 4 | GBR | 19 | 全部集中在 `model38` 估值族 |
| 5 | KOR | 18 | 做空数据 + other 类 |
| 6 | USA | 17 | insider_matrix / intraday / order_book |
| 7 | MEA | 15 | analyst7 计数类 + pv96 |
| 8 | **EUR** | **5** | 全部是 `predicted_surprise_pct_*` |
| 9 | **DEU** | **2** | estimate_change 族 |
| — | HKG / AMR / CHN / JPN | 0 | 实测太少或未探到 |

---

## 四、各区头部活/弱字段（Top 3）

### GLB（最强区）
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `single_bucket_20day_return_estimate_ohlcv_im` | **4.65** | **4.80** | 0.163 |
| ALIVE | `probability_label1_2quantile_20day_ohlcv_img` | 4.09 | 5.02 | 0.121 |
| ALIVE | `probability_label4_5quantile_20day_ohlcv_img` | 4.05 | 3.53 | 0.289 |

### IND
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `corr_last_trade_price_with_volume` | **6.48** | 3.25 | 0.382 |
| ALIVE | `corr_vwap_with_volume` | 4.68 | 2.35 | 0.348 |
| ALIVE | `corr_twap_with_volume` | 4.52 | 2.42 | 0.352 |

**⇒ IND 的 `intraday_pv_feats` 是全画像库 S 最高的族**（价量相关性），但换手偏高（0.35~0.38）。

### GBR
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `region_relative_valuation_rank` | 2.44 | 1.87 | 0.053 |
| ALIVE | `star_val_region_rank` | 2.37 | 2.06 | 0.124 |
| ALIVE | `star_val_sector_rank` | 2.31 | 1.93 | 0.129 |

**⇒ GBR 的活字段全部来自 `model38`（相对估值排名），换手低、2Y 稳** —— 与 DEU 的 estimate_change 机制完全不同。

### KOR
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `oth466_q_cni_xtp_si` | 2.37 | 1.77 | 0.130 |
| ALIVE | `shrt38_stk_invactsell_qty` | 2.35 | 1.38 | 0.298 |
| ALIVE | `shrt38_accum_sell_qty` | 2.27 | 1.74 | 0.150 |

**★ 注意**：**做空数据（`shortinterest38`）在 KOR 是 ALIVE，但在 DEU 是族级否证（S 全负）** ⇒ 跨区差异的典型例证。

### USA
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `eur_aggregated_value_1` | **4.30** | **5.65** | 0.063 |
| ALIVE | `mean_trade_volume_30m_pre_close_2` | 2.35 | — | 0.698 |
| ALIVE | `avg_rest_time_bid_filled_lvl1` | 2.34 | 0.74 | 0.054 |

### MEA
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `quarterly_net_income` | 2.19 | 3.24 | 0.033 |
| ALIVE | `est_q_dps_raisednum_1mth` | 2.13 | 2.04 | 0.049 |
| ALIVE | `est_q_net_raisednum_1mth` | 2.12 | 2.65 | 0.047 |

**★ 注意**：`analyst7` 的**计数类**在 DEU 是 `DEAD_COUNT` 判死形态（S 高但 2Y 崩），在 **MEA 却是 ALIVE（S2.12 / 2Y2.65）** ⇒ 又一处跨区差异。

### EUR
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `predicted_surprise_pct_f12m_revenue_4` | 2.09 | — | 0.069 |
| ALIVE | `predicted_surprise_pct_f12m_earnings_5` | 2.06 | 0.53 | 0.076 |
| ALIVE | `predicted_surprise_pct_f12m_ebitda_5` | 1.91 | — | 0.068 |

### DEU
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| ALIVE | `netprofit_y1_estimate_change_3mo` | 1.70 | 1.66 | 0.081 |
| ALIVE | `eps_y1_estimate_change_3mo` | 1.67 | 2.14 | 0.087 |
| WEAK | `mean_estimate_change_pct_f12m_earnings_14d_4` | 1.57 | 1.44 | 0.192 |

### HKG（0 ALIVE，但 14 WEAK）
| verdict | 字段 | S | 2Y | to |
|---|---|---:|---:|---:|
| WEAK | `anl94_find` | 1.33 | — | 0.037 |
| WEAK | `anl39_epschngin` | 1.28 | **2.66** | 0.031 |
| WEAK | `quantile_label_1bucket_20day_ohlcv` | 1.24 | 1.75 | 0.092 |

---

## 五、★★★★★ 跨区对照：三个直接可用的发现

### 发现 1（已实测验证）：`predicted_surprise_pct_*` 是**跨区差异**，不是形式问题
| 区域 | 形式 | verdict | S |
|---|---|---|---:|
| EUR | **`_pct_` 百分比版** | ALIVE ×5 | **2.09** |
| DEU | 绝对版（W198 实测） | 失败 | 0.74 |
| **DEU** | **`_pct_` 百分比版** | **34/35 未测** | — |

**★ W199 已实测验证（推翻上述直觉）**：用**同一套框架**在 DEU 补测 10 条 pct 变体，
**全部失败（S −0.12~1.04）**。同名字段对照：`..._pct_f12m_earnings_5` **EUR S2.06 → DEU S0.82**；`..._pct_f12m_revenue_4` **EUR S2.09 → DEU S0.69**。

**⇒ 真实原因是跨区机制差异，不是形式差异**；**同字段同框架跨区可差 1.2~1.3 个 Sharpe** ⇒ **「机制有效」是区域属性，不是字段属性**。
**跨区对照是「提出假设」的工具，不是结论。**

### 发现 2：同机制跨区可能完全反向
| 机制 | 在某区 | 在另一区 |
|---|---|---|
| `shortinterest`（借券/做空） | **KOR：ALIVE（S2.35）** | **DEU：族级否证（S −0.07~−0.74）** |
| `analyst7` 计数类 | **MEA：ALIVE（S2.13 / 2Y2.04）** | **DEU：`DEAD_COUNT` 判死** |

**⇒ 「某区内判死的族」不可外推到其他区。**

### 发现 3：⚠️ 高 S 陷阱 —— `dl_riskfree_returns` 标签族
GLB（S4.65 / 2Y4.80）、ASI（S3.58 / 2Y4.44）的高 S 字段大量来自 `dl_riskfree_returns`：
`single_bucket_*` / `probability_label*` / `quantile_label*`。

**这些是分位数/概率**桶标签**（非信号）** —— DEU 画像已明确标注为假信号。**其他区的高 S 同样不可当真**，须先核对 `fields.description` 确认是真实字段还是标签。

---

## 六、用法速查

```bash
PY="/d/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe"

# 盘点所有区域
$PY tools/fields/field_profile.py --list

# 建/更新某区（只影响该区）
$PY tools/fields/field_profile.py --build --region GLB

# 一次建全部
$PY tools/fields/field_profile.py --all-regions

# 查询某区
$PY tools/fields/field_profile.py --query --region GLB --verdict ALIVE
$PY tools/fields/field_profile.py --query --region EUR --min-s 1.5

# 或直接 SQL（每区一个视图）
# SELECT * FROM field_profile_glb WHERE verdict='ALIVE' ORDER BY best_s_sg DESC;
```

---

## 七、下一步建议（按数据支持度排序）

| 优先 | 动作 | 依据 |
|---|---|---|
| **1** | **去 GLB**（60 ALIVE + 67 WEAK，未测池 1.96 万） | 画像库最强的区，且本区未做过战役 |
| **2** | **去 IND**（54 ALIVE，S 峰值 6.48） | `intraday_pv_feats` 价量相关族 S 极高 |
| ~~3~~ | ~~DEU 补测 pct 版~~ | **已执行并证否**（W199：10 条全失败，S≤1.04）⇒ 该方向已排除 |
| 4 | 去 GBR（19 ALIVE，低换手估值族） | 换手 0.05~0.13，2Y 稳 |
| 5 | EUR 开战役（5 ALIVE + 数据包可预筛） | 已有明确靶子 |

**⚠ 共同纪律**：任何区的高 S 字段，开批前先核 `description` —— **排除 `*_label*` / `*_bucket*` 类标签**，它们不是信号。
