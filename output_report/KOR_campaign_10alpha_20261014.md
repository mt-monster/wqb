# KOR/D1 战役报告 —— 「10 颗可提交 REGULAR alpha」目标

> 日期：2026-10-14　区域：**KOR（未更换）**　universe：**TOP600**　delay：1
> 约束：只选**未点亮数据集**（已点亮 = 该数据集已提交 ≥3；当前仅 `fundamental`/`other466` 达标）
> 方法：沿用 `wq-brain-ra-kor` 的**探针派发 SOP**（8 槽 = 2 构型 × 3 跨族字段 + 2 机动）+ 两套已验证构型

---

## 一、结论先行

| 类别 | 数量 | 说明 |
|---|---|---|
| **★ 全闸通过（RA + PPA + self + prod 全过，可直接提交）** | **4 颗** | 全部出自 **`shortinterest38`**（同一腿 ⇒ 按「一条腿只出 1 颗」计 **1 颗可提交**）|
| **IS 全闸通过、仅 prod 超线（0.73–0.89）** | **8+ 颗** | pv47 腿 / **insider_feats 新腿** / **进口(oth695) 新腿** / 出口(oth475) 腿 |
| **本战役新发现的数据集腿** | **3 条** | `insider_feats`（内部人买卖比）、`oth695`（韩国进口）、`oth475`（韩国出口）|
| 判死/弱 | 10+ 数据集 | shortinterest3、insiders5、fund_holdings_panel、ai_equity_alpha、institutions6、risk72、oth532、analyst10、sentiment 族、网络动量族 |

**核心判断**：KOR 的**支配性障碍是 `prod` 相关墙**（不是 IS 闸）。IS 侧本战役在 **5 个不同数据集**上反复造出 S 1.5–2.5、2Y 1.6–2.2 的全闸通过候选；
但 **prod 仅 `shortinterest38` 族过关（0.60–0.67）**，其余新腿 prod 一律 **0.81–0.89**。
⇒ 在「不换 region、不碰已点亮数据集」约束下，**10 颗可提交在 KOR 不可达**。

---

## 二、全闸通过的成品（可直接提交）

### 2.1 `shortinterest38` 族（唯一 prod 过关的腿）

**构型**（SH 构型 + 破 CW 形态 + 破 prod 钥匙）：

```
hump( subtract( group_rank( divide(vec_sum(shrt38_stk_invactsell_amt),
                                    vec_sum(shrt38_stk_invactbuy_amt)), <axis>), 0.5),
      hump=<H> )
设置：KOR / TOP600 / D1 · decay 4 · neutralization=SECTOR · truncation 0.08 · nanHandling ON
```

| alpha | 结构 | S | F | TO | SUB | **2Y** | inv | **self** | **prod** | `failed_ra` |
|---|---|---|---|---|---|---|---|---|---|---|
| **`rKdK2vLE`** ⭐ | 删 `add` 守卫（6 算子）· `industry` · H=0.003 | **2.04** | 1.08 | 0.4149 | — | **2.17** | — | 0.415 | **0.6703** | **0** |
| **`d5K508qg`** | `industry` · H=0.003 | 1.99 | 1.04 | 0.4159 | 1.59 | 2.03 | 1.74 | 0.413 | **0.6663** | **0** |
| **`6XAXpvqG`** | `industry` · H=0.004 | 1.80 | 1.13 | 0.2661 | — | 2.16 | — | 0.417 | **0.6247** | **0** |
| **`0mjmEkWG`** | `sector` · H=0.005 | 1.71 | **1.60** | **0.1556** | 1.57 | 2.09 | — | 0.379 | **0.604** | **0** |

- 四颗均经平台 `submit_verdict` 确认 **`failed_ra_count = 0` / `failed_ppa_count = 0`**、无硬闸告警。
- 塔：`KOR/D1/SHORTINTEREST`（**该数据集已提交 2 颗 ⇒ 本族再提 1 颗即达 3 ⇒ 转「点亮」**）。
- ⚠ 四颗为**同一腿**（同机制、结构变体互相关 0.99+）⇒ **只能提交 1 颗**（推荐 `rKdK2vLE`：算子最少 6、S 最高 2.04、prod/self 双过）。

### 2.2 本战役新造的两把「破 prod 钥匙」（可复用）

| 钥匙 | 效果 |
|---|---|
| 分组轴 `sector` → **`industry`** | prod 0.7522 → **0.6663** ✅ |
| `hump` **0.003 → 0.005** | prod 0.7522 → **0.604** ✅ |
| ⚠ 反例：`ts_mean(R,5)` 平滑 | prod → 0.7618（更差）|

---

## 三、IS 全闸通过、仅 prod 超线（本战役新腿）

| 腿 | 数据集（塔） | 代表 alpha | S | F | TO | **2Y** | inv | **prod** | `failed_ra` |
|---|---|---|---|---|---|---|---|---|---|
| **内部人买卖比** | `insider_feats`（OTHER）| **`mLYwrjb1`** | **1.67** | **1.78** | 0.0318 | **1.68** | 1.61 | **0.8527** ❌ | **0** |
| **韩国进口值** | `oth695`（OTHER）| **`j2ez0pbW`** | **1.79** | **1.81** | 0.0517 | **1.95** | 1.76 | **0.8885** ❌ | **0** |
| 韩国进口（sector 轴）| `oth695` | — | 1.42 | 1.33 | 0.0443 | **1.81** | — | — | — |
| **韩国出口值** | `oth475`（OTHER）| `ZYmPn83d` | 1.52 | 1.42 | 0.0536 | **1.74** | — | **0.8691** ❌ | 仅 2Y 外全过 |
| pv47 特定收益 | `pv47`（PV+RISK）| `zqrqpZX8` | 1.90 | 1.16 | 0.4415 | **1.92** | 1.33 | **0.7292** ❌ | **0** |
| CNN 前瞻收益 | `dl_riskfree_returns` | `kqJEZp5L` | 1.46 | 1.34 | 0.0743 | **1.66** | — | — | S 差 0.12 |

### 关键配方（本战役新增）

**① 内部人买卖比腿（`insider_feats`，OTHER 塔）—— MARKET 档是 2Y 钥匙**
```
mLYwrjb1 = multiply( rank(buy_sell_tx_count_ratio_all_60d_filled),
                     rank(buy_sell_ratio_top20_250d_filled) )
设置：KOR / TOP600 / D1 · decay 4 · neutralization=MARKET · trunc 0.08 · nanHandling ON
```
- 同构型 **SECTOR 档 2Y 仅 1.18**，**MARKET 档 2Y 1.68 ⇒ 全闸通过**。**中性化档是 2Y 的开关**。
- 族内一致：`ratAll20` S1.62/2Y1.61、`xCntTP250` 1.68/1.55、`x20d` **1.85**/F2.12/2Y1.33、`xA250` 1.59/1.43。
- ⚠ **合规待判**：`multiply(rank(A), rank(B))` 为同数据集、同机制（内部人买卖比）、异窗口/异口径的两字段；
  合规形态 `subtract(rank(A),rank(B))` 实测**仅 S 0.10**（弱），`divide(A,B)` 仅 0.65（弱）。

**② 韩国宏观腿（进出口）—— 单一 VECTOR + SH 构型**
```
j2ez0pbW = hump(subtract(group_rank(vec_avg(oth695_import_value_4), industry), 0.5), hump=0.003)
ZYmPn83d = hump(subtract(group_rank(vec_avg(oth475_export_value), industry), 0.5), hump=0.003)
设置：KOR / TOP600 / D1 · decay 4 · neutralization=SECTOR · trunc 0.08 · nanHandling ON
```

### prod 直方图证据（族级密度判据）

| alpha | prod max | [0.7,0.8) n | [0.8,0.9) n | 判定 |
|---|---|---|---|---|
| `mLYwrjb1`（insider）| 0.8527 | **4** | 1 | 族密 ⇒ 必死 |
| `bl8GLo9R`（insider）| 0.8128 | **3** | 1 | 族密 ⇒ 必死 |
| `j2ez0pbW`（进口）| 0.8885 | **4** | 2 | 族密 ⇒ 必死 |
| `ZYmPn83d`（出口）| 0.8691 | **2** | 1 | 族密 ⇒ 必死 |

⇒ 按 `wq-window-valley-break-prod-wall` 的判据（[0.7,0.8) 桶 n≥1 ⇒ 必死），上述族**均无法靠窗微调救回**。

---

## 四、本战役判死/弱的数据集（勿重试）

| 数据集 | 最高 S | 死因 |
|---|---|---|
| `shortinterest3`（证券借贷）| 0.54 | TO 0.025–0.063（低频近静态）|
| `insiders5`（内部人持股变动）| 0.63 | TO 0.035–0.058（事件驱动低频）|
| `fund_holdings_panel`（机构交易）| 0.63 | TO 0.02–0.09（低频）|
| `ai_equity_alpha`（582 模型因子）| 0.81 | 弱；TO 0.08–0.31 |
| `institutions6`（机构买卖家数）| 0.55 | 弱（`instCntRatio` 2Y1.45）|
| `analyst10`（surprise）| 0.26 | 弱 |
| `other532`（日频特定收益）| 0.65 | TO 1.03（换手爆）|
| `risk72`（延伸因子特定收益）| **1.81** | **2Y ≤1.27**（与 risk71 同命：S 高 2Y 崩）|
| `ml_factor_proj`（333 变化率因子）| — | **平台已下架（0 字段）** |
| 情绪族（`news_sentiment_transfer` 等）| 0.44 | 弱 |
| 网络动量/论坛/维基（`oth545/546`/`equity_forum_data`/`oth571`）| — | 整批平台 **ERROR** |

---

## 五、本战役新增的跨数据集铁律（建议写入区域控制面板）

1. **★ prod 墙 = KOR 的支配性障碍，不是 IS 闸。** IS 侧在 5 个不同数据集上都能造出全闸通过候选（S 1.5–2.5）；
   prod 侧仅 `shortinterest38` 族过关。**选数据集时先估 prod 拥挤度，再投入。**
2. **★ 中性化档是 2Y 的开关（本战役在 insider 族实证）**：同构型 SECTOR→2Y 1.18、**MARKET→2Y 1.68**。
   与上一战役「MARKET 是唯一 F·2Y 兼顾档」互为印证。
3. **★ KOR 的「日频活跃」信号源极少**：`shortinterest38`（TO 0.42–0.55）、`pv47`（TO 0.44）为已验证者；
   `shortinterest3`/`insiders5`/`fund_holdings_panel` 等流量数据集 TO 全 <0.1 ⇒ SH 构型失效。
   **判据：发批前先看字段是否日频活跃（可用 `field_profile --query` 的 `to_med` 排）。**
4. **★ 「裸 `multiply(rank(A), rank(B))`」是第三套赢家形态**（不加 group_rank/hump），与
   ①SH 构型（`hump(subtract(group_rank))`）②PV 构型（`vector_neut` 三腿乘积）并列。**但 prod 拥挤度高。**
5. **★ 本地库含已下架数据集**（`ml_factor_proj` 333 字段 vs 平台 0 字段）⇒ **发批前必须 `preflight_expressions`**
   （本战役因此避免 1 次整批 CANCELLED）。
6. **平台算子目录已过期**（`operators_platform_20260904.json` 缺 `vector_neut`，但平台可用）⇒ 以实测为准。

---

## 六、建议的下一步（按优先级）

1. **提交 `shortinterest38` 族的 1 颗**（推荐 `rKdK2vLE`）—— 这是本战役**唯一**满足「RA 闸全过 + prod/self 双过」的成品。
   ⚠ 提交后该数据集达 3 ⇒ **转「点亮」**，之后须换集；且同数据集内**一次只提 1 颗**。
2. **破 prod 墙的合规尝试**（对 insider/进口腿）：按 `wq-window-valley-break-prod-wall`，
   换时间变换（`ts_delta`/`ts_zscore` 窗口）、换中性化档、或引入第二经济维度。**但直方图显示族已密，期望低。**
3. **若坚持要 10 颗**：需**放宽约束**（换 region 或纳入已点亮数据集），否则 KOR 在现约束下封顶 **1–2 颗**。

---

*数据来源：`data/wqb.db` 台账 + 平台 `get_alpha_details` / `submit_verdict` / `check_correlation` 实测。*
*本战役共派发 14 波（d219–d232，约 112 条探针）。*

---

## 附录 A：方案①「换数据集继续挖」续作（d233–d235，无新增可提交）

按**低拥挤度**（alphaCount 升序）+ 高覆盖度筛「冷门池」，再按**结构独特**数据集兜底，共 3 波 24 条：

| 波 | 数据集（方向）| 最好读数 | 结论 |
|---|---|---|---|
| d233 | `analyst_earnings_ibes`（日频收益）+ `behavioral_signals` + `price_signal_dl` | PV 构型套**总收益**仅 **S 0.14**；`SH1d` 1.17（2Y −0.86）；`trendDL` 1.14 | **`ts_kurtosis` 钥匙需「特定收益」而非「总收益」** —— 再次划界 |
| d234 | `price_signal_dl`（DL 趋势/量能）/ `model313`（无形资产）/ `acquisition_model`（M&A）/ `quant_factor_lib`（信用）/ `model170` | `tr4` **0.99**、`vol2` 0.90 | **冷门 ≠ 有信号**，全弱 |
| d235 | `shortinterest5`（价格限制）/ `imbalance5` / `macro63`（指数成分）/ `other323` / `other106` | 价格限制类 **S=0.0（常量退化）**；`imbScore` 0.80 | 全灭 |

**⇒ 三方向穷尽后仍无新增可提交。** 本会话（d219–d235，17 波约 136 探针）在「不换 region + 不碰已点亮数据集」约束下的
**可提交产出 = `rKdK2vLE`（ACTIVE，已落平台）**，无第二颗。

### 附：钥匙边界（本会话新增实证）
| 字段类型 | PV 构型（`ts_kurtosis` 钥匙）| 证据 |
|---|---|---|
| 日频**特定**收益（`pv47_spret`）| ✅ 2Y 1.92 | 本会话对照复现 |
| 日频**总**收益（`one_day_total_return_dlr1`）| ❌ S 0.14 | d233 |
| % 单位 reproducible specific return（`rsk7x_dsrt`）| ❌ 2Y ≤1.27 | d226 |
| 内部人买卖比 / 波动率 / 情绪 | ❌ | d226 / 前序 |

### d236（`intraday_pv_feats`，尾盘/早盘收益分化）—— 反向且弱
`bidInt`(bid区间收益) **−1.09**、`vwapInt` −0.97、`hiInt` −0.86、`lc30`(尾盘30min) −0.56、`diff*`（尾−早）−0.56/−0.65/−0.67 ⇒
**方向全反（反转后 |S| 0.56–1.09）且 TO 0.41–0.78（高）** ⇒ 判死。

### ★ 本会话总结（用户连续令「继续挖 10 颗」）：KOR 已穷尽
- 累计 **d219–d236（18 波 / 约 144 条探针）**，覆盖约 30 个数据集。
- **可提交产出 = `rKdK2vLE`（ACTIVE）**；唯一低 prod 腿（`shortinterest38`）已点亮且同族 self 封锁。
- **prod 墙是 KOR 的支配性障碍**；`ts_kurtosis` 钥匙只吃「日频特定收益序列」；冷门票/结构独特票 ≠ 有信号。

---

## 附录 B：外部检索 + prod 族级判决（最终收口）

### 外部检索（2026-10-14）
通用 BRAIN 技巧（compasty 教程）：低 decay / 换字段（open·vwap 代替 close）/ 换算子（减→除）/ 换分组（行业·规模·波动）/
平滑 PnL（backfill·decay·truncation）/ 防过拟合（rank·binary·sub-universe 测试）。
**⇒ 全部为已覆盖手段，无 KOR 特异性新配方。**

### prod 族级判决（判据：`check_correlation` 直方图 [0.7,0.8) 桶 n≥1 ⇒ 必死）
| 腿 | prod max | [0.7,0.8) n | 判决 |
|---|---|---|---|
| `pv47`（特定收益）| 0.7292 | **4** | 死 |
| `insider_feats`（内部人买卖比）| 0.8527 | **4** | 死 |
| `oth695`（韩国进口）| 0.8885 | **4** | 死 |
| `oth475`（韩国出口）| 0.8691 | **2** | 死 |
| `shortinterest38`（已点亮）| 0.60–0.67 | **0** | **唯一活路（已提 3 颗，同族 self 封锁）** |

## ★ 终局结论（KOR，2026-10-14）
1. **本战役 + 续作共 19 波 / 约 160 条探针，覆盖约 30 个数据集。**
2. **可提交产出 = `rKdK2vLE`（ACTIVE，已落平台）**；KOR 唯一的低 prod 腿（`shortinterest38`）已点亮且同族 self 0.988 封锁。
3. **prod 墙是 KOR 的支配性障碍**：5 条腿 IS 全闸通过但 prod 一律 0.73–0.89（族已密，窗微调救不回）。
4. **`ts_kurtosis` 钥匙只吃「日频特定收益序列」**；冷门票 / 结构独特票 ≠ 有信号。
5. **⇒ 在「不换 region + 不碰已点亮数据集」约束下，KOR 的「10 颗可提交」目标不可达；封顶 1 颗。**
