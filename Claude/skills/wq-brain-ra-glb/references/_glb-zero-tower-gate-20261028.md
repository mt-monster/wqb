# GLB 零塔门控路线 · 2026-10-28 战役实证

> **as_of**：2026-10-28 ｜ **战役**：GLB w92–w151（~75 条仿真派发，2618 行本地回测，平台权威校正 526 条 / 323 条实际变化）
> **定位**：本文件是 GLB 区的**手写专题**（`references/` 下 `_` 前缀 = 非 render 生成，SKILL.md 重渲不会覆盖）。
> 它回答三个问题：① GLB 还能挖什么？② 哪些路已被证伪、别再烧槽？③ 平台阈值与设置档在 GLB 的**实测值**是多少。
> 相关：[`../rules/six-step-glb-override.md`](../rules/six-step-glb-override.md)（六步覆盖）· [`../rules/gate-and-submit-discipline.md`](../rules/gate-and-submit-discipline.md)（闸门与提交纪律）
>
> **现行政策提示（2026-09-29）**：本文件 §4.1 / §4 的表达式表是**历史实盘货架记录**（哪些已提交/已实测的真实数据），
> 不是配方教学——加权 / 等权拼腿自 2026-09-13 起被路线 A 与闸 5 禁止；新用途一律改写成条件 / 分组 / 残差三式（见主 skill 铁律）。

---

## 0. 一句话结论

**GLB 仍有活矿，但活矿不在「零塔字段当信号腿」，而在「零塔字段当门控腿 × dl_riskfree 当信号腿」。**
三个从未测过的零塔（ANALYST / INSIDERS / MACRO）作**信号腿**全部全灭；同一个零塔字段改当**门控腿**，在 7 个零塔域上全部产出 S2.2–4.8 的可提交候选。

---

## 1. ★ 新出货机制：零塔门控腿 × dl_riskfree 信号腿（7 个零塔域全部有效）

**形态**（零塔字段做 `trade_when` 门控，dl_riskfree 的 `single_bucket_*_return_estimate_ohlcv_img` 做信号腿）：

```
trade_when(rank(ts_mean(<零塔字段>, 22)) > 0.7,
           signed_power(subtract(group_rank(<dl_riskfree 信号腿>, <country|exchange>), 0.5), 0.5),
           rank(ts_mean(<零塔字段>, 22)) < 0.6)
```

**实测逐颗**（全部 fRA=0、稳健性 PASS）：

| 零塔门控字段 | 门控数据集 | 塔位 | alpha_id | S / F / 2Y |
|---|---|---|---|---|
| `market_value_institutional_shares_disposed` | institutions6 | institutions/other | `e75pvoNz` | **4.81** / 4.19 / **5.56** |
| 同上 | institutions6 | institutions/other | `npvJaGa3` | 4.75 / 4.10 / 5.49 |
| `ern3_pre_interval` | earn3 | earnings/other | `JjewWlvx` | 3.07 / 1.58 / 4.00 |
| 同上 | earn3 | earnings/other | `9qxvmnlq` | 3.05 / 1.59 / 4.06 |
| `fnd44_jones_cf_accruals` | fnd44 | other/fundamental | `YP1rzw2J` | 2.95 / 1.77 / 2.17 |
| `snt21_2neg_conf_up` | snt21 | other/sentiment | `xAr6WLLp` | 2.77 / 1.46 / 2.45 |
| 同上 | snt21 | other/sentiment | `E567NKnL` | 2.70 / 1.39 / 2.38 |
| `scl12_sentiment` | socialmedia12 | socialmedia/other | `qML1wg3Z` | 2.31 / 1.16 / 3.38 |
| `nws73_headlines` | news73 | other/news | `VkaXa9dA` | 2.24 / 1.35 / 2.55 |
| `vec_avg(rsk60_crowding)` | risk60 | risk/other | `QPvJ6KVw` | 3.19 / 1.59 / 3.43 |

⇒ **7 个零塔域（FUNDAMENTAL / INSTITUTIONS / EARNINGS / SENTIMENT / SOCIALMEDIA / NEWS / RISK）全部有效**，
每域 3–6 颗，共 **40+ 颗 fRA=0 候选**。
⇒ 换信号腿期限（5day ↔ 20day）只改 2Y，不改塔位 ⇒ 可按需选余量。

**为什么成立**：强度来自**跨集门控**（门控腿提供经济子集、信号腿提供截面基座），不是零塔字段自身的预测力。
零塔字段只负责「在哪个经济子集里持仓」，因此**它不需要自己有 alpha**。

**推论（对选波的操作含义）**：当要找「未点亮塔」时，**优先找有强信号腿可配的零塔数据集**（本区 = dl_riskfree / techindi），
而不是找「零塔自己的预测字段」—— 后者已被三域证伪。

---

## 2. ★ 已证伪：零塔字段当**信号腿**（结构性，三个域全灭）

| 零塔 | 数据集 | 覆盖 | 实测 | 根因 |
|---|---|---|---|---|
| **INSIDERS** | `insider_agg_matrix` | cov 0.4904 | `pwdrEbwj` S−1.0/TO 2.1562 fRA=9；`omE5z0K2` S−1.55/TO 1.9558 fRA=8；`A1VZbmkY` S−0.18 fRA=9 | 内部人买卖是**随公司规模变化的原始计数** ⇒ 量纲不可跨股票比较；换手爆炸 |
| **MACRO** | `macro27`（招聘岗位，33 字段全 VECTOR） | cov 0.2–1.0 | `O0AP5xVJ` S−0.42；`Xg9Q2rjX` S−0.43；`88R9aZJz` S−0.24；`vR1M53A3` S−0.42 | 招聘景气**不传导到个股截面收益** |
| **ANALYST** | analyst15 / analyst69 / analyst_factor_signals / analyst_revision_horizons | — | w142–w145 共 16 条全灭（S 最高 1.04，多为负） | 预期修正幅度 / 方向 / 趋势斜率在 GLB 无信息量 |

⇒ **「零塔 × 零塔」这条形态在 GLB 整体不成立**（三个从未测过的域全灭 = 不是运气问题）。
⇒ 零塔字段的正确用法是**门控腿**，不是信号腿（见 §1）。

---

## 3. ★ 已证伪：RISK 域信号腿（**category 级** prod 饱和）

| 数据集 | alpha_id | prod |
|---|---|---|
| risk60 | `88R9ARkm` | **0.9026** |
| risk60 | `YP1KZbJq` | **0.9423** |
| risk60 | `O0APedMJ` | 0.8886 |
| risk60 | `P0oaeG9L` | 0.8028 |
| risk68 | `3qX23qk0` | 0.8617 |
| risk68 | `78N208vQ` | 0.8821 |
| risk68 | `LLN2qLm1` | 0.8634 |
| risk70 | `gJeO7PKK` | 0.8856 |

⇒ **三个不同数据集、六种信号形态，prod 全部落在 0.80–0.94** ⇒ 这是 **category 层面的拥挤**，不是某个字段的问题。
⇒ RISK 域**只能当门控腿**（`QPvJ6KVw` 即此形态，prod 0.6385 干净）；**当信号腿的路整体关闭**。

### 3.1 CW 是 `rsk60_offer`（VECTOR）形态的**结构性属性**

40 颗 `rsk60_offer` 候选**全部卡 `CONCENTRATED_WEIGHT`**，且六种改法逐一证伪：

| 改法 | 实测 |
|---|---|
| 换外层 `group_rank` | `3qXzWLKe` S2.75→**1.46**、fRA 1→**4**（反更差） |
| 幂律压尾 `power(x,0.5)` | `rKObq6Qo` fRA=1（CW） |
| 换轴族 `sector` | `88jO0kA7` fRA=1（CW） |
| 换字段组合 `offer − lending_fee_bid_rate` | `rKObq6mm` S2.79 但 fRA=1（CW） |
| 换中性化/截断（FAST + trunc 0.08） | `88R9ARkm` S3.21 但 fRA=1（CW） |
| 换 VECTOR 字段 `rsk60_last` | `9qj9OJdo` fRA=1（CW） |

⇒ 与主 skill `wq-operator-playbook-by-gate` §1 的「`truncation`/`decay`/中性化/平滑**修不了 CW**」一致，GLB 提供 40 颗实证。
⇒ **CW 只在 MATRIX 型 RISK 字段上没有**（`gJeO7PKK` fRA=0、`LLMaXwv6` fRA=0）⇒ 解法是**换信号腿类型**，不是修 CW。

---

## 4. ★ PV 域：两条出货机制 + 一个可破闸的中性化技巧

### 4.1 纯 PV 单塔（**纯单塔 ⇒ 塔位最干净**，提 1 颗即点亮 PV 塔）

| alpha_id | 表达式 | S / F / 2Y | prod |
|---|---|---|---|
| `mLmxKN12` | `-1.0*group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 5), country)` | 2.99 / 1.69 / 2.92 | **0.694** ✓ |
| `kqNrmA9g` | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 3), country)` | **3.00** / 1.40 / 2.65 | 待测 |
| `LLMaXwv6` | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 8), country)` | 2.78 / 1.42 / **2.99** | 待测 |
| `WjOQX8rj` | `multiply(-1, group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 5), country))` | 2.83 / 1.37 / 2.81 | 0.8885 ✗ |

⇒ 共 **29 颗纯 PV 单塔 fRA=0** 候选（`mean_high` 族 20 / `corr_ltpv` 族 8 / `corr_hpv` 族 1），
全部塔位 = `pv`（**不含 OTHER** ⇒ 提 1 颗 ⇒ PV 2→3 点亮，且不违反三塔互斥）。

### 4.2 ★ `INDUSTRY → FAST` 中性化可破 `LOW_GLB_EMEA_SHARPE`（区域闸）

`submit_ready` 里的 8 颗 PV 候选 prod 0.477–0.5624 干净、self 干净、2Y 全过，平台权威却统一 **fRA=1**、
失败项全是 `LOW_GLB_EMEA_SHARPE`（value 0.58–0.59 vs limit 1.0）—— 因为它们用 `INDUSTRY` 中性化。
**换 `FAST` 中性化 ⇒ fRA=0、12 硬闸全 PASS**（`WjOQX8rj` / `kqNrmA9g` / `LLMaXwv6`）。
⇒ 这是「FAST 中性化是区域闸通用解」的**第三次独立验证**（前两次 `LLMjNkl1→npvJaGa3`、`3qobj3pX→E567NKnL`），**首次在 PV 域**。

### 4.3 `last-trade` 路径不要碰（复现既有结论）

`mLoRxww1`（`mean_last_trade_price_return_30m_pre_close_2` + FAST）仍卡 `LOW_GLB_EMEA_SHARPE`（S2.25）
⇒ 与 `references/pv.md` 既有结论「**last-trade 路径在 9 种中性化下都不行（0.58–0.93）**」一致 —— **独立复现**。
⇒ PV 域只走 **high-price 路径**。

---

## 5. ★ GLB 平台阈值实测值（写死字面量会误判）

| 闸 | 平台实测 limit | 说明 |
|---|---|---|
| `IS_LADDER_SHARPE` / `LOW_2Y_SHARPE` | **2.02** | ⚠ **不是 1.58**：GLB 的 ladder 阈值比通用值高。8 颗 PV 候选 2Y 1.93–2.01 全部因此 FAIL |
| `HIGH_TURNOVER` | **0.7** | ⚠ 不是 0.4：实测 TO 0.4163 PASS、TO 0.7643 FAIL |
| `CONCENTRATED_WEIGHT` | 0.1 | 严重超限时 value 可达 **1.0**（极端集中，不是「略微超限」） |
| `LOW_SUB_UNIVERSE_SHARPE` | 比值闸 | `0.75 × √(子宇宙/全宇宙) × alpha Sharpe`，系数逐区实测 |
| `LOW_GLB_AMER/EMEA/APAC_SHARPE` | 1.0 | **区域闸**，`FAST` 中性化是通用解（§4.2） |

⇒ **判定必须读平台 `checks[].limit`，不得用字面量**（`thresholds.json` 的 `review.two_year_sharpe_min=1.6`、
`review.turnover_max=0.3` 是**内部宽松筛**，平台线更严 ⇒ 内部过关的，平台仍可能 FAIL）。

---

## 6. ★ GLB 设置档（**按信号族分档**，不要套区域默认）

区域默认档（`settings.json`：TOPDIV3000 / STATISTICAL / decay 2）是 2026-09-19 **按旧信号族过闸率**校准的。
2026-10-28 这轮的实测给出**按族分档**的矩阵：

| 信号族 | universe | neutralization | decay | 依据 |
|---|---|---|---|---|
| 零塔门控 × dl_riskfree | **MINVOL1M** | **FAST** | 6 | `npvJaGa3` S4.75、`YP1rzw2J` S2.95（10 年稳健 PASS） |
| PV 尾盘反转（high-price 路径） | **MINVOL1M** | FAST | 6 | `mLmxKN12` S2.99 prod 0.694、`LLMaXwv6` S2.78 |
| techindi 连续回归输出 | MINVOL1M | STATISTICAL | **10** | `JjeEMEdl` S5.95（**但 prod 0.75–0.80 偏高，慎用**） |
| 区域默认档（**仅旧族**） | TOPDIV3000 | STATISTICAL | 2 | 2026-09-19 过闸率校准（TOPDIV3000 27.5% / STATISTICAL 77.6% / decay2 90.9%） |

⇒ **新族不得直接套区域默认档**（`pv.md` 自己也写「只在 MINVOL1M」⇒ 面板与分支卡本就自相矛盾，本轮以 MINVOL1M 实测为准）。

---

## 7. 本战役的工程教训（与 skill 无关，但每个 agent 都会踩）

1. **平台 prod 相关性是账号级单并发队列**，批量并发会互相排队并触发 API 429 ⇒ 一次只盯 1–3 颗，串行低频（见 `wqb-concurrency` §9）。
2. **prod 是「持仓形态」的属性，不是「信号」的属性** ⇒ 同一表达式族仅换中性化，prod 从 0.694 跳到 0.8885。
   ⇒ **破闸顺序固定：① 修 RA 闸 → ② 重测 prod → ③ 再算互相关 → ④ 才能进篮子**。
3. **同 category 内 prod 差异极大**（PV 域 0.694 ~ 0.9898）⇒ 不能按族推断，必须逐颗实测。
4. **本地回测库必须有 `ra_failed_checks` / `two_year_sharpe` / `pyramid_short` 三个字段**，否则：
   - 平台把 RA 失败记在 `ra.ra_failed_checks` + `checks.warning`，而 `checks.fail` **恒为空**
   ⇒ 只取 `checks.fail` 会把「只差一闸」的候选显示成 fRA=0 ⇒ **直接误导提交筛选**（本轮实测：40 颗被误判）。
5. **收割器的写入必须 `commit`**（`close()` 会回滚未提交事务）⇒ 否则日志报 `written=True` 而库里零行（本轮丢失 169 条）。

---

## 8. 可复用弹药（2026-10-28 校正后）

- **134 颗合规且 fRA=0** 的候选（47 颗因 PV/MODEL/OTHER 混塔被剔除），覆盖 **10 个未点亮塔**
  ⇒ `results/glb_submit_ammunition_20261028.json`
- 组合分支索引表（render 生成，证据截至 2026-10-04）的「prod 已测（低于上限）」存量：**pv 43(11) / other 48(9) / model 1(0) / risk 10(0)**
  ⇒ 括号第二个数 = **prod 已确认低于上限的可复用池**，选波时应优先复用，别重挖。
