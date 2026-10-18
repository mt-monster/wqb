# KOR 全区数据集扫描报告（找「有潜在信号」的数据集字段）

> 日期：2026-10-14　区域：**KOR**　universe：**TOP600**　delay：1
> 目标：全区扫一遍数据集，**发现有潜在信号的「数据集 → 字段」**
> 方法：两套已验证构型（SH 流量比率 / PV 特定收益）+ 裸 `multiply(rank,rank)`，8 槽/波探针，SECTOR/MARKET 双档

---

## 一、结论先行

| 结论 | 内容 |
|---|---|
| **★ 全区无新增「可提交」腿** | 扫了 **~40 个数据集**（约 19 波 / ~160 条探针）；**唯一可提交 = `rKdK2vLE`**（shortinterest38，已 ACTIVE）。|
| **★ KOR 的支配性障碍 = `prod` 墙** | **5 个数据集**能造出 IS 全闸通过（S 1.5–2.5、2Y 1.6–2.2）的候选，但 **prod 一律 0.73–0.89**（族已密）；唯一低 prod 腿 = `shortinterest38`（0.60–0.67，已点亮）。|
| **★ 有「潜在信号」但未过闸** | `other72`（区域排名 S 1.43）、`insider_feats`（内部人买卖比）、`oth695`（进口）、`oth475`（出口）、`dl_riskfree_returns`（DL 前瞻收益）。|
| **★ 判死（弱/退化）** | 见 §四（~30 个数据集）。|

---

## 二、★ 有「潜在信号」的数据集（S ≥ 1.0，值得深挖）

| 数据集（塔）| 代表字段 | 最强读数 | prod | 判词 |
|---|---|---|---|---|
| **`shortinterest38`**（SHORTINTEREST）| `vec_sum(sell_amt)/vec_sum(buy_amt)` | **S 2.04 / F 1.08 / 2Y 2.17** | **0.60–0.67 ✅** | **唯一可提交腿；已点亮（3 颗）** |
| **`insider_feats`**（OTHER）| `buy_sell_tx_count_ratio_all_60d_filled × buy_sell_ratio_top20_250d_filled`（裸 multiply）| **S 1.67 / F 1.78 / 2Y 1.68** | 0.8527 ❌ | IS 全闸过，prod 密墙 |
| **`oth695`**（OTHER）| `oth695_import_value_4`（韩国进口）| **S 1.79 / F 1.81 / 2Y 1.95** | 0.8885 ❌ | 同上 |
| **`oth475`**（OTHER）| `oth475_export_value`（韩国出口）| S 1.52 / 2Y 1.74 | 0.8691 ❌ | 同上 |
| **`pv47`**（PV）| `pv47_for_statssimple_only_spret`（特定收益，PV 构型）| **S 1.90 / F 1.16 / 2Y 1.92** | 0.7292 ❌ | 同上 |
| **`other72`**（OTHER）| `oth72_sector_rank`（区域排名）| S 1.43 / F 1.28 / 2Y 1.45 | — | 接近闸线（S 差 0.15）|
| **`dl_riskfree_returns`**（OTHER）| `probability_label3_4quantile_60day_ohlcv`（CNN 前瞻收益）| S 1.46 / F 1.34 / 2Y 1.66 | — | 接近闸线（S 差 0.12）|
| **`multifactor_return_pred`**（MODEL）| `analyst_quantile5_r120_pred`（预测收益）| S 1.05 | — | 升级带 |

---

## 三、全区数据集 → 信号地图（按类别，最强读数）

### 3.1 PV / RISK（收益分布）
| 数据集 | 最强 S | 判词 |
|---|---|---|
| `pv47`（特定收益）| **1.90** | 活（prod 被挡）|
| `pv103`（区间/MOO-MOC）| 1.28 | 判死 |
| `pv13`（地理/客户敞口）| 0.44 | 判死 |
| `pv14`（期货基差）| 0.27 | 判死 |
| `pv30`/`pv29`（PCA 分组轴）| — | 轴，非信号 |
| `oth532`（日频特定收益）| 0.65 | TO 爆 1.03 |
| `risk71`（`dsrt`）| 1.88 | **2Y ≤1.16**（钥匙失配）|
| `risk72`（延伸因子 `dsrt`）| 1.87 | **2Y ≤1.27**（同上）|
| `intraday_pv_feats`（日内价格结构）| −1.09 | 反向且弱 |

### 3.2 流量 / 持仓
| 数据集 | 最强 S | 判词 |
|---|---|---|
| `shortinterest38`（投资者买卖）| **2.04** | 活（已点亮）|
| `shortinterest3`（证券借贷）| 0.54 | 低频 |
| `insiders5`（内部人持股变动）| 0.63 | 低频 |
| `insider_feats`（内部人买卖比）| **1.67** | 活（prod 被挡）|
| `institutions6`（机构买卖家数）| 0.55 | 弱 |
| `fund_holdings_panel`（基金持仓）| 0.63 | 低频 |

### 3.3 ANALYST / MODEL（预测/修正/评分）
| 数据集 | 最强 S | 判词 |
|---|---|---|
| `analyst4`（修正幅度 REV）| **1.38** | 弱（2Y 0.79）|
| `analyst9`（修正广度）| 1.09 | 弱（TO 0.048）|
| `analyst10`（surprise）| 0.26 | 判死 |
| `analyst_base_ref`（SUE/E-P）| 0.63 | 弱 |
| `analyst46`（观点评分）| 0.42 | 判死 |
| `analyst11`（ESG）| 0.01 | 判死 |
| `multifactor_return_pred`（预测收益）| 1.05 | 升级带 |
| `multi_source_model` | 0.96 | 弱 |
| `global_seasonal_model` | 0.86 | 弱 |
| `analyst_revision_horizons`（修正广度）| 0.76 | 弱 |
| `predictive_starmine`（下调计数）| 0.74 | 弱 |
| `chart_cnn_alpha` | −0.41 | 判死 |
| `other72`（区域排名）| 1.43 | 接近闸线 |
| `model36/53/28/32/31/250`（信用/违约/动量）| 0.18–0.71 | 弱 |
| `model109`（修正/diffusion）| 0.84 | 弱 |
| `model110`（综合分）| 0.68 | 弱 |
| `model313`（无形资产）| 0.37 | 弱 |
| `model170`（隐含估值）| −0.08 | 弱 |
| `ai_equity_alpha`（模型因子）| 0.81 | 弱 |
| `quant_factor_lib`（信用）| 0.10 | 弱 |
| `behavioral_signals`（salience）| 0.57 | 弱 |
| `price_signal_dl`（DL 趋势/量能）| 0.99 | 弱 |
| `acquisition_model`（M&A）| −0.17 | 判死 |

### 3.4 NEWS / SENTIMENT / 其它
| 数据集 | 最强 S | 判词 |
|---|---|---|
| `oth695`（韩国进口）| **1.79** | 活（prod 被挡）|
| `oth475`（韩国出口）| 1.52 | 活（prod 被挡）|
| `oth327`（利率敏感度）| 0.76 | 弱 |
| `oth335`（股息模型）| 0.65 | 弱 |
| `oth436`（股息模型）| 0.53 | 弱 |
| `news_sentiment_transfer`（情绪）| 0.44 | 弱 |
| `oth545`/`oth546`（网络动量）| 整批 ERROR | 不可用 |
| `equity_forum_data`/`oth571`（论坛/维基）| 整批 ERROR | 不可用 |
| `shortinterest5`（涨跌停）| 0.0 | **常量退化** |
| `imbalance5`（SHIELD-OIL）| 0.80 | 弱 |
| `macro63`（指数成分）| 0.0 | **常量退化** |
| `other106`（KOSPI 指数）| 0.15 | 弱 |
| `other323`（股本）| 0.03 | 弱 |

---

## 四、结构性结论（本会话新增铁律）

1. **KOR 的支配性障碍 = `prod` 墙**（不是 IS 闸）。5 个数据集能造出 IS 全闸通过候选（S 1.5–2.5），但 prod 一律 0.73–0.89（族已密）。
2. **两套已验证构型的字段类型前提**：
   - **SH 构型**（`hump(subtract(group_rank(divide(vec_sum(A),vec_sum(B)),industry),0.5),hump=0.003)`）只吃「**日频活跃**流量/比率」字段（TO>0.2）；
   - **PV 构型**（`vector_neut` 三腿乘积 + `ts_kurtosis(X,140)`）只吃「**日频特定收益序列**」；
   - **裸 `multiply(rank(A),rank(B))`**（第三形态）= 内部人买卖比的赢家。
3. **`ts_kurtosis` 钥匙边界**：只「日频特定收益」有效；总收益（`one_day_total_return`）S 0.14；% 单位 specific return（`rsk7x_dsrt`）2Y ≤1.27。
4. **「冷门 ≠ 有信号」「结构独特 ≠ 可用」**：低 alphaCount 数据集多弱；常量字段（价格限制/指数成分）S=0.0。
5. **中性化档 = 2Y 开关**：新族先并行 SECTOR + MARKET（insider 族 SECTOR 2Y 1.18 → MARKET 2Y 1.68）。

---

*数据来源：`data/wqb.db` 台账 + 平台 `get_alpha_details` / `check_correlation` 实测。*

---

## 附录 D：破 prod 墙专项（d250–d256，7 波）—— prod 0.8885 → **0.7098**（差 0.0098）

**同数据（`oth695` 韩国进口）、同机制（`event_conviction_ratio` 族），只换分组轴：**

```
tail(winsorize(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20),
                           bucket(rank(cap), range="0,1,0.2")), std=2),
     lower=0.2, upper=0.8, newval=0.5)      # KOR/TOP600/D1 · decay4 · MARKET · trunc0.08
⇒ `9qEYRMQr`  S1.91 / F2.18 / TO0.0367 / 2Y2.27 / CW✅ / **prod 0.7098**
```

### 杠杆排序（全实测，务必按序用）
| 杠杆 | 效果 | 判定 |
|---|---|---|
| **换分组轴为连续桶 `bucket(rank(cap))`** | prod **0.8885 → 0.7098**（粒度 0.2 最优，0.25→0.7171、0.1→0.7189、0.19→0.7178）| ★**唯一有效** |
| `trade_when(volume>0)` 门控 | 2Y 1.81→**2.15**，prod 不动（0.8092/0.7108）| 仅抬 2Y |
| `vector_neut(·, cap/adv20/dadv)` 残差化 | **S 掉到 0.27/0.83/1.04** | ❌ 禁用 |
| `ts_rank`/`ts_zscore`/`ts_decay_linear` | TO 0.19 或 CW=1.0 | ❌ 禁用 |
| `quantile(ts_sum)` | 与 `ts_sum` 逐位相同（单调变换）| 等价 |
| `group_zscore` 替 `group_rank` | S 1.37（掉 0.5）| ❌ |
| `tail` 分位收窄（q≤0.15）| S 掉到 1.49–1.67 | ❌ |
| `group_rank(x, g, weight)` 三参 | **ERROR 连坐** | ❌ 不可用 |
| `vec_max`/`vec_sum` vs `vec_avg` | **逐位相同** | 该字段 vec 聚合退化 |

### 剩余候选（冲最后 0.0098）
设置层 decay(2/6/8) / truncation(0.05/0.10/0.15) / pasteurization / nanHandling；**出口腿 `oth475` 同族同结构**（可直接注册第二条腿）。

---

# ★★★★★★★★★★★★ 附录 E：**破 prod 墙成功 —— KOR 第二颗全闸通过 alpha `88voYna7`**

```
88voYna7 = trade_when(greater(rank(adv20), 0.6),
              tail(winsorize(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20),
                                        bucket(rank(cap), range="0,1,0.2")), std=2),
                   lower=0.2, upper=0.8, newval=0.5), -1)
```
**设置**：KOR / TOP600 / D1 · decay 4 · **neutralization=MARKET** · truncation 0.08
· pasteurization ON · nanHandling ON · maxTrade OFF

| 闸 | 值 | 限 | |
|---|---|---|---|
| `failed_ra_count` / `failed_ppa_count` | **0 / 0** | — | ✅ |
| S / F / TO | **1.86 / 2.19 / 0.0269** | — | ✅ |
| SUB | **1.82** | — | ✅ |
| **2Y（IS_LADDER_SHARPE）** | **2.10** | 1.58 | ✅ |
| **investability** | **1.86** | 1.302 | ✅ |
| CW / CLUSTER | PASS | | ✅ |
| **prod** | **0.6977** | 0.70 | ✅ **破闸** |
| **self** | **0.2305** | 0.70 | ✅ |
| 塔 | **KOR/D1/PV(1.4) + KOR/D1/OTHER(1.6)** | | **双塔 effective 2** |
| **`all_passed`** | **true** | | ✅ |

## ★★★ 破 prod 墙的三段配方链（通用杠杆，缺一不可）

| 段 | 内容 | prod |
|---|---|---|
| ① 结构（换族） | `event_conviction_ratio` 族（论坛 252 赞帖骨架） | 0.8885 |
| ② **分组轴 = 连续桶 `bucket(rank(cap), range="0,1,0.2")`**（不是 sector/industry） | 连续分位桶改变持仓结构 | **0.7098** |
| ③ **★ 第二维度门控 `trade_when(greater(rank(adv20), 0.6), <信号>, -1)`** | 相对阈值门控只持高流动性部分 | **0.6977 ✅** |

### 门控阈值曲线（实测）
`>0.3` → 0.7064 ｜ `>0.5` → 0.7017 ｜ **`>0.6` → 0.6977 ✅** ｜ `>0.7`/`>0.8` prod 未回算

### 关键教训（勿重试）
- `vector_neut` 残差化**杀 S**（0.27–1.04）⇒ 禁用；
- `trade_when(volume>0)`（无阈值）只抬 2Y、不压 prod ⇒ **门控必须用相对阈值 `rank(adv20)`**；
- `group_rank(x, g, weight)` 三参形态 **平台 ERROR**（整批连坐）；
- `bucket` 只能作 `group_rank` 的分组参（独立成 alpha ⇒ ERROR）；`range` 内不能有空格；
- `vec_max`/`vec_sum` 与 `vec_avg` 在该字段上逐位相同（聚合退化）；
- `truncation` 在 TOP600（<500 只）下**不触发**，改它无效。

⇒ **「prod 被挡」的标准处置顺序 = 换族 → 换连续桶分组轴 → 加 `rank` 阈值门控**（三步实测 0.89 → <0.70）。

---

# ★★★★★★★★★★★★ 附录 F：**`xA16pzQJ` 已优化并提交（ACTIVE）**

**最终提交件（9 算子，无损压缩自 10 算子）**
```
trade_when(greater(rank(adv20), 0.6),
  tail(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20),
                  bucket(rank(cap), range="0,1,0.2")), lower=0.2, upper=0.8, newval=0.5), -1)
KOR / TOP600 / D1 · decay 4 · MARKET · truncation 0.08 · pasteurization ON · nanHandling ON
```
`status=ACTIVE` · `stage=OS` · `dateSubmitted=2026-10-14T10:34:01-04:00` · `failed_ra=0` · `failed_ppa=0` · `checks.pending=[]`
**S 1.86 / F 2.19 / TO 0.0269 / SUB 1.82 / 2Y 2.10 / inv 1.86 / CW✅ / CLUSTER✅ / self 0.2308 / prod 0.6976**
returns 0.1728 · DD 0.1087 · margin 0.012863 · long 97 / short 473
**塔：KOR/D1/PV(1.4) + KOR/D1/OTHER(1.6) ⇒ 双塔 effective 2**
`name = KOR_R_oth695_convratio_001` · `color = BLUE`

## 算子压缩（逐算子消融实证）
| 变体 | 算子数 | S | F | 2Y | prod | 判定 |
|---|---|---|---|---|---|---|
| `88voYna7` 基线 | 10 | 1.86 | 2.19 | 2.10 | 0.6977 | — |
| **`xA16pzQJ`（删 `winsorize`）** | **9** | **1.86** | **2.19** | **2.10** | **0.6976 ✅** | ★**逐位相同 ⇒ 无损，采纳并提交** |
| `VkdjjgqA`（删 `tail`）| 9 | 1.76 | 2.00 | 2.09 | — | 保留 |
| `bl8ZGzJ6`（删两者）| 8 | 1.76 | 2.00 | 2.09 | **0.8503 ❌** | **`tail` 是压 prod 核心算子，必留** |

**★ 两条压缩铁律**：① `winsorize` 在本信号上已饱和（std 1.5/2/2.5/3 读数逐位相同）⇒ 可无损删；
② **删 `tail` ⇒ prod 0.6976 → 0.8503（+0.15）** ⇒ `tail` 是 prod 墙关键算子，任何压缩不得动它。

---

## 附录 G：提交后继续挖掘（d263–d266）—— 第二条腿的配方迁移测试

**已验证配方**（KOR 唯一破 prod 墙的配方）：
```
trade_when(greater(rank(adv20), T),
  tail(group_rank(ts_sum(vec_avg(FIELD), 20), bucket(rank(cap), range="0,1,0.2")),
       lower=0.2, upper=0.8, newval=0.5), -1)
```

### 迁移结果（**配方对 `oth695` 专属**）
| 腿 | bucket+门控 | bucket 无门控 | 判词 |
|---|---|---|---|
| `oth475` 出口 | 1.46 / 2Y 1.33 | sector 1.52 / **2Y 1.96**（**prod 0.844**）；bucket 1.42 / 2Y 1.42 | **两难判死** |
| `insider_feats` | top20_10d 1.43 / 2Y 1.50；+门控 1.32 / **2Y 2.17** | top5_60d 1.30 / 0.67 | S 与 2Y 不可兼得 |
| `dl_riskfree_returns` | probQ3+门控.4 **S1.58** / 2Y1.34 | probQ3 **S1.63**/F1.76/2Y1.13；+sector 1.56/2Y1.61（**prod 0.867**）| prod 挡 |
| `pv47_spret` | −0.26 / 2Y −0.83 | — | 配方不适配（收益序列 × 累积求和 = 噪声）|
| `other72` | 0.82 / 2Y 1.20 | 0.97 / 1.16 | 弱 |

**★ 结论**：`bucket(rank(cap),0.2)` + `trade_when(rank(adv20)>T)` 只在**慢变强度型字段（贸易流/持仓强度）**上同时过 2Y 与 prod；
`oth695`（韩国进口强度）是 KOR 唯一满足的字段。收益序列、概率场、计数比、区域排名迁移后均被 2Y 或 prod 挡。

**KOR 当前已提交 2 颗**：`rKdK2vLE`（shortinterest38）、`xA16pzQJ`（oth695，双塔 PV+OTHER）。
**下一条腿需引入新机制（非贸易流）**。

---

## 附录 H：「换机制」路线实测（d267）—— 两条候选机制双双判死 + **KOR 已饱和**

### ① `other106`（OSPI CA 指数权重 / 自由流通因子）—— 判死（近静态型）
| 字段 | S | 备注 |
|---|---|---|
| `oth106_ospi_ca_eq_capping_factor_nxt` | **−0.01** | CW 1.0 |
| `oth106_ospi_ca_eq_free_float_factor_nxt` | **−0.20** | CW 0.991 |
| `oth106_ospi_ca_eq_index_share_cls` | **−0.32** | |
| `oth106_ospi_ca_eq_capping_factor_cls` | **0.04** | CW 0.167 |

**原因**：cov = 0.404 且因子**仅在指数调仓日变化** ⇒ 属「近静态型」字段（与「网络/嵌入/权重型 → 近静态」失败指纹一致）。

### ② `insider_feats` 两腿组合（合规形态）—— 全负判死
`divide(top20_10d, top5_60d)` −0.11 ｜ `ts_corr(top20_10d, top5_250d, 22)` −0.41 ｜ `subtract(rank,rank)` −0.11
**原因**：单腿 `top20_10d` 尚可（S1.43），但两腿组合互相抵消 ⇒ **计数型字段不适合组合**。

### ⚠ 新增工程铁律
**MATRIX 字段误套 `vec_avg` ⇒ 整批 CANCELLED**（本轮第 8 条；`insider_feats` 是 MATRIX）
⇒ 混合数据集批次里，**每个字段的 `vec_*` 包裹必须按该数据集 `dataType` 逐个确认**。

## ★★ KOR 饱和判定
破墙配方已系统性迁移测试 **7 条腿**：`oth695`✅已提交 ｜ `oth475` 出口两难 ｜ `insider_feats` 组合全负 ｜
`dl_riskfree` prod 挡 ｜ `pv47` 负 ｜ `other72` 弱 ｜ `other106` 近静态判死
⇒ **KOR 可提交产出 = 2 颗已封顶**（`rKdK2vLE` + `xA16pzQJ`）；**继续在 KOR 换数据集的边际收益已趋零**。

---

## 附录 I：ATOM 因子挖掘战役（机制→模板映射，d268–d270）

**目标**：ATOM 因子 ⇒ **一个 alpha 只用一个机制族的一个字段**（天然满足禁混信号）。

### 机制 → 模板映射（16 族，按数据性质匹配）
| 族 | 模板 | 依据 |
|---|---|---|
| M5 预期估计变动率 | `F` 或 `ts_mean(F,22)` | **禁用 `ts_sum`**（变动率累积会摧毁信号，实测 0.95→0.02）|
| M4 模型评分分量 | `F` | 已是模型输出，不做时间聚合 |
| M6 修正广度计数 | `ts_delta(F,22)` | 计数水平受市值偏差，差分才是信号 |
| M7 估值比率 | `ts_zscore(F,252)` | 重尾正偏，按自身历史标准化 |
| M10 预期水平值 / M16 相对指数超额 | `ts_mean(F,22)` | 慢变水平 |
| M3 相对排名百分位 / M2 评级水平 / M11 增长率 / M13 其它 | `F` | 已是 rank/水平 ⇒ **不再套 rank** |
| M1 评级变动 | `ts_delta(F,22)` | 变动型 |
| M9 价格技术位 | `ts_zscore(F,22)` | 相对位置 |
| M12 标志位 | `F` | 离散 ⇒ **禁用 winsorize/signed_power** |
| M8 意外度 | `ts_backfill(ts_mean(F,22),66)` | 稀疏事件型，先 backfill |

**共用「持仓结构层」（不引入新经济机制，不破坏 ATOM）**：
`group_rank(<inner>, bucket(rank(cap), range="0,1,0.2"))` + `tail(..., 0.2, 0.8)` +（按需）`trade_when(greater(rank(adv20), 0.6), ..., -1)`

### 实测结果（28 个结构）
| 波次 | 内容 | 最佳 |
|---|---|---|
| d268 | 14 族机制匹配模板（纯 ATOM，无门控）| M5 `ts_mean` S0.94 / 2Y1.57 |
| d269 | Top 6 族 + 门控 + M5 三种聚合 | **M13_raw S1.02**；M5_raw S0.95/2Y1.56；**M5_sum S0.02** |
| d270 | 纯净 M5 族（299 字段）子轴 8 个 | **`analyst_revision_percentile_score_long_3` S1.05** / `_medium_2` S1.00 |

### 结论
**`analyst_revision_horizons` 在 KOR 的 S 天花板 ≈ 1.05**，2Y 天花板 ≈ 1.57；距闸（S≥1.58）差 ~0.5。
已测 28 种结构（>10 种纪律门槛）⇒ **该数据集判死（KOR）**。
**新铁律**：`ts_sum` 用在「变动率」字段上会摧毁信号（0.95 → 0.02）。
**下一步**：转 `analyst11`（ESG/治理新机制）或 `analyst_consensus`（2325 VECTOR 大池）。

---

## 附录 J：KOR Analyst 类 ATOM 战役总结（d268–d273，**3 数据集 / 52 结构**）

| 数据集 | 字段 | 结构数 | S 天花板 | 2Y 天花板 | 判定 |
|---|---|---|---|---|---|
| `analyst_revision_horizons` | 1026 | 28 | **1.05**（`analyst_revision_percentile_score_long_3`）| 1.57 | 判死 |
| `analyst11`（ESG） | 210 | 16 | 0.79（CW=1.0 挡）；平滑后 S 转负 | 1.13 | 判死 |
| `analyst_consensus` | 2343 | 8 | **0.89**（`estimate_count_*` 变动）| **2.03**（`actual_net_value` ts_delta66）| 判死 |

**★ 结论**：KOR Analyst 类在 ATOM 框架下 **S 天花板 ≈ 1.05**，距闸（1.58）差 ~0.5；**2Y 普遍 1.5–2.0**（时序稳定性够，缺横截面预测力）。
**★ 对照**：KOR 唯一破闸的 `xA16pzQJ` 来自 `oth695` **贸易流强度**（慢变强度型），不是 analyst 类。
**⇒ ATOM 框架本身有效**（语法/CW/2Y 都可控）；瓶颈是 **KOR analyst 数据的横截面 alpha 强度**。
**⇒ 下一步**：把已验证配方迁移到其它类别的「慢变强度型」字段，或换 region。

### 沉淀的可复用资产
1. **description 聚类法**（词干匹配 + 完整同义词表 + 「其它」族必抽检）—— 已写入 `docs/reference/KOR_analyst_field_profiling.md`
2. **机制→模板映射表**（16 族，按数据性质选时序算子）
3. **CW=1.0 修复配方**：去 `tail` + `winsorize(std=4)`（d272 验证有效）
4. **`ts_sum` 禁用于变动率字段**（0.95 → 0.02）
5. **dataType 必须逐个查**（VECTOR 漏 `vec_avg` / MATRIX 误套 ⇒ 整批废，本轮踩 3 次）

---

## 附录 K：横截面预测力攻坚（d274–d274c，论坛经验驱动，2026-10-14）

### K.1 论坛调研结论（BRAIN 中文论坛，6 帖精读）

| 来源帖 | 核心经验 | 落地情况 |
|---|---|---|
| analyst10 预期差模板（51 赞/24 评） | ① 同口径单维差分（FY2−FY1）；② **先各腿 zscore 再相减**防高波动股统治截面；③ quantile(driver="cauchy") 抗重尾；④ 覆盖率匹配 + trade_when(覆盖数>3)；⑤ 回填窗口 63/126/252 需对照 | 全部移植进 d274（S1a/S1b/S2/S3） |
| 数据集子分类与中性化匹配（12 赞） | Analyst-Estimates → SECTOR/FAST；Analyst-Ratings → REVERSION_AND_MOMENTUM/MARKET | 设置层杠杆，留待破 S 闸后用 |
| analyst4 修正节奏（29 赞） | 方向比幅度干净：净修正人数差 > 绝对金额变动 | S3 广度净差率 |
| analyst94 目标价（29 赞） | 目标价"光束方向"（变化趋势）> 绝对上行空间 | KOR 无 analyst94，用 fwd P/E 期限结构替代（S7） |
| 上调预期次数优化 | group_rank(市值桶) > group_neutralize；先中性化再排名更差 | 已在本壳层（bucket(rank(cap))）中体现 |
| 评论区实测注脚 | ① 双版本陷阱（v1 减 v2 混入修订噪声）；② CHN 八腿全灭 vs JPN 水平值可出货 ⇒ region 特异性极强；③ ts_rank(slope,252) 抓修正动能 | d274 全部避开版本混搭 |

### K.2 d274 单信号波（12 条，均套用 xA16pzQJ 破 prod 壳：trade_when(adv20)+tail+bucket(rank(cap))+ts_backfill 120）

| 结构 | alpha | 机制 | S | F | 2Y | subU | 判定 |
|---|---|---|---|---|---|---|---|
| S1a FY2−FY1 双腿zdiff | j2eRVvGZ | 期限结构 | −0.18 | −0.06 | −0.62 | −0.23 | 死 |
| S1b FY2−FY1 原始差 | LL5aK2J2 | 期限结构 | 0.07 | 0.02 | −0.29 | 0.13 | 死 |
| S2 pred_surps+cauchy | XgRQa338 | 预测惊喜 | 0.21 | 0.08 | 1.12 | −0.05 | 死 |
| S3 EBITDA 广度净差率 | RRAQev0n | 方向>幅度 | 0.34 | 0.17 | 0.45 | 0.39 | 弱 |
| S4 SmartEstimate Δ30d | ZYm3X68d | 修正动量 | −0.03 | 0.00 | −0.12 | −0.11 | 死 |
| S5 惊喜−离散度 | MP0R6V86 | Diether 异象 | 0.08 | 0.02 | 0.19 | −0.07 | 死 |
| S6 F24M−F12M 增速斜率 | 2rjzGMe6 | 期限斜率 | 0.37 | 0.20 | 0.37 | 0.42 | 弱 |
| S7 fwd P/E 期限结构 | kqJra9nd | 估值结构 | 0.51 | 0.25 | 0.21 | 0.70 | 弱 |
| S8 FY1 盈利收益率 | ZYm3XbM0 | 价值 | −0.01 | 0.00 | 0.39 | −0.05 | 死 |
| S9 PEG 行业百分位反转 | ZYm3Xb11 | 价值 | −0.16 | −0.05 | 0.11 | −0.28 | 死 |
| **S10 revenue_revision_component_medium** | MP0RgeOn | ARM 分量 | **0.66** | **0.44** | 0.35 | 0.37 | **最强单信号** |
| S11 recommendation_change_medium | omo5PL06 | 评级变动 | 0.03 | 0.00 | −1.39 | −0.13 | 死 |

### K.3 d274b/c 组合波（rank 等权叠加 → 横截面 S 提升 56%）

| 结构 | alpha | S | F | 2Y | subU | PPA | 判定 |
|---|---|---|---|---|---|---|---|
| C1 rev+PE期限 | LL5aERzn | 0.56 | 0.34 | 0.29 | 0.62 | ✗ | 估值腿稀释 |
| **C2 rev+F24M斜率** | rKdg93L1 | 0.87 | 0.72 | 1.04 | 0.79 | ✗ | 双腿正交确认 |
| C3 三重+PE | MP0RdlOM | 0.68 | 0.52 | 0.45 | 0.74 | ✗ | 同上稀释 |
| D1 C2+preferred | bl8ZrMER | 0.70 | 0.50 | 0.08 | 0.62 | ✗ | preferred 拖累 |
| **D2 C2+secondary** | **RRAQlMl0** | **1.03** | **0.87** | 0.29 | **0.95** | **✓** | **全区 analyst 类首个 S>1** |
| D3 C2+pct_score | leMO5dgl | 0.76 | 0.58 | 0.45 | 0.63 | ✗ | — |
| D4 C2+sales_float | gJWOgWjm | 0.97 | 0.80 | **0.53** | 0.80 | ✗ | 2Y 最稳 |
| D5 cov1 rev 变体对 | j2eRoJEk | 0.93 | 0.75 | 0.42 | 0.96 | ✗ | — |
| D6 C2+rev_long_term | bl8Zr7aq | 1.01 | 0.86 | 0.01 | 0.96 | **✓** | 2Y 塌陷 |

### K.4 结论与铁律

1. **单信号天花板确认**：论坛全部招数（双腿zdiff/cauchy/广度/离散度/价值反转）在 KOR 单信号上限 ≈ 0.66 —— 「数据横截面区分度不足」结论经 12 结构复验成立。
2. **破局靠组合**：`rank(revenue_revision_component_medium) + rank(growth_f24m_vs_f12m_earnings_smartestimate_short) [+ rank(secondary_earnings_revision_component_medium_term_51)]` → S 0.66→1.03，F 0.44→0.87，PPA 通过。
3. **估值类（S7/S8/S9）与评级变动（S11）在 KOR 全灭** —— 与 forum「CHN surps 水平型全灭」的 region 特异性注脚一致。
4. **剩余瓶颈转移**：LOW_SHARPE(1.58)/LOW_FITNESS(1.0)/IS_LADDER(2Y) —— D2 的 2Y=0.29 是最大短板；下一杠杆 = 复合信号的 ts_delta（修正动能二阶）+ decay 扫描 + 子分类中性化（SECTOR/FAST）。

---

## 附录 L：d275 全参数攻坚（66 结构，S 1.03 → 1.56，2026-10-14/15）

### L.1 战役路径（每波的关键发现）

| 波 | 变量 | 最佳 | 关键发现 |
|---|---|---|---|
| d274 | 单信号+组合 | RRAQlMl0 S1.03/F0.87 | 组合破局（rev+slope+secondary） |
| d275-E | 中性化×decay×trunc | decay2: S1.10/F0.97 | **decay 是杠杆**；SECTOR/FAST/SUBIND 全不如 MARKET；trunc 无感 |
| d275-F/H/I | cov1 分量 + bf×decay 网格 | cov1rev+bf120: S1.18/F1.03 | **cov=1.0 的 `revenue_revision_component_medium_term_3` 优于 cov0.75 的 `_medium`**；decay 单调（d0-1 S 峰，d2 F 峰） |
| d275-J/K/L/M | **tail 放松** | tail0.1/0.9+bf40: S1.50/F1.17/2Y0.90 | **tail 松紧是 S↔2Y 权衡旋钮**：0.2/0.8→1.29，0.1/0.9→1.50，0.05/0.95→S降/2Y升(1.12)，0/1→CW 失败 |
| d275-N/O/P/Q | **newval 微扫** | nv0.65: **S1.56/F1.22** | newval 0.4→1.44, 0.5→1.50, 0.6→1.54, **0.65→1.56**, 0.7→1.54（峰值 0.63–0.67 平台） |

### L.2 冠军配方（`xA10Pm8J`，未提交——提交权归用户）

```
trade_when(greater(rank(adv20), 0.6),
  tail(group_rank(add(add(
    rank(ts_backfill(revenue_revision_component_medium_term_3, 40)),
    rank(ts_backfill(growth_f24m_vs_f12m_earnings_smartestimate_short, 40))),
    rank(ts_backfill(secondary_earnings_revision_component_medium_term_51, 40))),
    bucket(rank(cap), range="0,1,0.2")), lower=0.1, upper=0.9, newval=0.65), -1)
```
KOR/TOP600/D1 · decay1 · MARKET · trunc0.08

| 指标 | 值 | 闸 | 判定 |
|---|---|---|---|
| Sharpe | **1.56** | 1.58 | ✗ 差 0.02 |
| Fitness | **1.22** | 1.0 | ✓ |
| 2Y ladder | 0.80 | 1.58 | ✗ 差 0.78 |
| sub-universe | 1.35 | 0.53×S | ✓ |
| investability | 1.19 | — | ✓ |
| risk-neutralized | 1.11 | — | ✓ |
| PPA 检查 | — | — | ✓ 全过 |
| CLUSTER_TEST | — | 1 | ✓ |

### L.3 参数地图（champion 家族，S/F/2Y）

| 变体 | S | F | 2Y |
|---|---|---|---|
| bf20 tail0.1/0.9 nv0.5 | 1.39 | 1.04 | 0.93 |
| bf40 tail0.1/0.9 nv0.5 | 1.50 | 1.17 | 0.90 |
| bf40 tail0.1/0.9 nv0.6 | 1.54 | 1.20 | 0.81 |
| **bf40 tail0.1/0.9 nv0.65** | **1.56** | **1.22** | 0.80 |
| bf40 tail0.1/0.9 nv0.7 | 1.54 | 1.21 | 0.79 |
| bf40 tail0.12/0.88 nv0.6 | 1.50 | 1.14 | 0.70 |
| bf40 tail0.08/0.92 nv0.5 | 1.38 | 1.02 | 0.73 |
| bf60 tail0.05/0.95 nv0.5 | 1.21 | 0.85 | 1.12 |
| bf40 tail0.05/0.95 nv0.6 | 1.27 | 0.91 | 1.14 |
| bf40 tail0/1 nv0.5 | 0.63 | 0.36 | 1.33（CW 失败） |
| bf60 d2 nv0.6 | 1.40 | **1.34** | 0.79 |
| bf40 d2 nv0.65 | 1.52 | **1.50** | 0.70 |
| bf40 nv0.65 + sector zscore | 1.24 | 0.82 | 0.80 |
| bf40 nv0.65 + multiply 复合 | 1.22 | 0.84 | 0.76 |
| bf40 nv0.65 + 第4腿 primary_profit | 1.04 | 0.88 | 0.20 |
| bf40 nv0.65 + 第4腿 breadth | 队列中未回 | — | — |
| bf40 nv0.65 + 流动性交互 | 0.92 | 0.62 | 0.23 |

### L.4 结论

1. **KOR 分析师类新天花板：S 1.56 / F 1.22 / 2Y 0.80**（66 结构参数穷举）。距全闸差 SHARPE 0.02 + IS_LADDER 0.78。
2. **尾部门控是新杠杆族**：`tail` 的 lower/upper/newval 三参数同时管 S 与 2Y，0.1/0.9 + nv0.65 是 S 峰；0.05/0.95 是 2Y 峰——两峰不可兼得。
3. **IS_LADDER 是真墙**：要求全部滚动 2Y 窗 ≥1.58，本族最好 0.9；破它需要**机制正交的第二腿**（非同类 ARM 分量叠加，叠加已饱和在 3 腿）。
4. 候选池状态：`xA10Pm8J`(S1.56)、`WjL6NjqG`(nv0.63, 1.56)、`omoM9Knv`(nv0.6, 1.54)、`RRAn2ame`(d0, 1.54)、`wp9MnQjQ`(d2, F1.49) —— 全部 UNSUBMITTED，留待用户决策。

---

## 附录 M：系统性数据集扫描 + 字段画像（d276，2026-10-15，48 结构）

### M.1 S0 全量数据集扫描（87 个）

| 分类 | 数量 | 数据集 |
|---|---|---|
| 全量 | 87 | — |
| **已点亮排除** | 2 | `shortinterest38`(5 提交)、`other466`(5 提交) |
| 已判死/已分诊 | 22 | 字段数<3 / 结构性退化 / 饱和 / 低频近静态 / 双构型全灭 |
| **候选** | **63** | 白名单 `logs/_kor_s0_whitelist.json` |

评分模型与排除清单见 `Claude/skills/wq-brain-ra-kor/references/_dataset-scan-sop.md`。
**核心先验**：`alphaCount` 是 prod 墙密度最可靠的单因子代理（d219–d232：5 个数据集出 IS 全闸，prod 只过 1 个族）。

### M.2 入选数据集与字段画像摘要

| 数据集 | 字段数 | 机制族 | 拥挤度 | 画像结论 |
|---|---|---|---|---|
| `fundamental90` | 39 | 舞弊评分/盈利质量/现金流/资产结构/营运账龄/成长 | 多数 aCnt **0–7** | 白空间最佳，**7 个正交子族** |
| `other395` | 368 | 应计比率网格（总应计/t统计/波动/持续性/资产扩张/自由裁量/R²）| **>90% aCnt≤3** | KOR 最白，但 **S 天花板 0.61** |
| `fundamental44` | 12 | 舞弊检测（mscore/fscore/benford/重述概率）| aCnt 36–118 | **全灭**：取值近乎二值 |
| `other452` | 46 | 税务应计/递延税 | aCnt 0–5 | `deferred_tax_liability` S 0.26 活 |
| `other401` | 57 | GAME 治理（pscore/盈余平滑/相对波动）| aCnt 0–33 | pscore 为唯一正向计分腿 |

完整字段画像（每字段 cov / aCnt / 语义方向 / 推荐模板）见 `docs/reference/KOR_dataset_field_profiling_20261015.md`。

### M.3 d276 八波结果（48 结构）

| 波 | 变量 | 最佳 | 关键发现 |
|---|---|---|---|
| A | fundamental44 舞弊族（8 腿）| S 0.10 | **全灭**：模型评分类在 KOR 截面无梯度 |
| B | fundamental90 连续比率（6 腿）| `grossprofit_asset` **S 0.61** | **方向必须实测**：`icfroe_5y` −0.62 / `receivable_days` −0.36 |
| C | 方向修正 + 2/3 腿组合（8）| S 0.58 | 组合只抬 2Y（0.97），S 不动 |
| D | pv47 + `trade_when(adv20)` 门控 0.3/0.5/0.7/0.85（4）| S 0.42 | **门控在 pv47 族使 S 崩塌**（1.90→0.42）|
| E | pv47 + `bucket(rank(cap))` / `hump`（4）| `omoMKXbJ` **S 1.53** | S 恢复 + PPA 全过，但 **prod 0.8321 变差** |
| F | pv47 + 盈利腿组合（4）| S 0.94 | **跨族组合稀释**（季度腿拉低日频信号）|
| G | other395/452 + `ts_sum` 时序壳（6）| S 0.61 | 时序聚合不救季度字段 |
| H | pv47 + tail newval 微扫（4）| S 1.53 保持 | tail 放松在 pv47 族无效（0.6/0.65 → 1.13/1.18）|

### M.4 最佳候选 `omoMKXbJ`（未提交——提交权归用户）

```
vector_neut(trade_when(greater(rank(adv20), 0.1),
  tail(group_rank(multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 140))),
                       rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 132))),
                       rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 252)))),
                   bucket(rank(cap), range="0,1,0.2")), lower=0.2, upper=0.8, newval=0.5), -1),
  power(rank(rsk68_weight_dadv), 0.5))
```
KOR/TOP600/D1 · decay4 · **MARKET** · trunc0.08

| 闸 | 值 | 限 | 判定 |
|---|---|---|---|
| LOW_SHARPE | **1.53** | 1.58 | ✗ 差 0.05 |
| LOW_FITNESS | **0.94** | 1.0 | ✗ 差 0.06 |
| IS_LADDER_SHARPE | 0.97 | 1.58 | ✗ 差 0.61 |
| sub-universe | 1.39 | 0.53×S | ✓ |
| investability | 1.14 | 0.70×S | ✓ |
| risk-neutralized | 1.86 | — | ✓ |
| CW / TO / CLUSTER | — / 0.38 / 0.97 | — | ✓ |
| **PPA 检查** | — | — | **✓ 全过（failed_ppa_count=0）** |
| **SELF_CORRELATION** | **0.3212** | 0.7 | **✓** |
| **PROD_CORRELATION** | **0.8321** | 0.7 | ✗ |

`failed_ra_count = 3`（KOR 至今最小），双塔 RISK(1.3)+PV(1.4) effective 2。

### M.5 三条新铁律（已写入 skill）

1. **「模型评分/舞弊概率」类在 KOR 截面无区分度** —— 尽管 cov 0.898，取值近乎二值。**开波前看取值分布是否连续，不是看 cov。**
2. **方向必须实测** —— 新字段族首波正反双向各一条（2 槽成本省一整轮）。
3. **KOR 会计质量/财务基本面族 S 天花板 = 0.61** —— 32 结构穷举确认，季频字段不值得再投配额。

### M.6 ★ 重要修正：`bucket(rank(cap))` 破 prod 墙**不是普适杠杆**

先前结论「换连续桶是唯一压 prod 有效」**只在 `oth695` 贸易流强度族成立**。在 `pv47` 峰度族实测**反而变差**：

| 构型 | IS | prod | 判定 |
|---|---|---|---|
| `oth695` + bucket | S1.91/2Y2.27 | 0.7098→0.6977 | ✅ 有效 |
| `pv47` 基准 | S1.90/2Y1.92 | 0.7275–0.7716 | 基线 |
| `pv47` + bucket(0.2) | S1.53/2Y0.97 | **0.8321** | ❌ 变差 |
| `pv47` + 门控 0.85 | S1.90→**0.42** | — | ❌ S 崩塌 |
| `pv47` + hump 0.005 | S1.53→**0.76** | — | ❌ S 崩塌 |
| `pv47` + 盈利腿 | **0.83** | — | ❌ 跨族稀释 |
| `pv47` + tail nv0.6/0.65 | 1.13/1.18 | — | ❌ 低于基准 |

⇒ **三步处置顺序（换族 → 换连续桶 → 加门控）不变，但每步必须实测、不可跨族照搬。**
⇒ 判族级命运用 `check_correlation` 直方图：`[0.7,0.8)` 桶 n≥1 ⇒ 密墙（本轮 pv47 该桶 n=35）。

### M.7 结算

**10 颗全闸 alpha 的目标未达成。** KOR 可提交产出仍封顶 **2 颗**（`xA16pzQJ` + `rKdK2vLE`，均已 ACTIVE）。
原因：① TOP600 小宇宙配额紧；② `pv47`/`risk` 峰度族 prod 是真密墙（窗口/POW/门控/分组轴/尾部门五路穷举后 0.7275–0.8321）；③ 剩余白空间（`other395` 应计网格等）S 天花板 0.61。
**未达成 10 颗的诚实归因 = prod 墙 + 季频字段天花板，不是配额或方法问题。**
