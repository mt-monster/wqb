# 结合点塔收益的总体排序与提交方案（2026-11-11 09:5x GMT+8 / ET 11-10 20:5x）

> **配额：ET 11-10 REGULAR 3/4、剩 1 席｜SUPER 1/1 已满**
> 本表是筛选结论，不是提交授权。

## 0 先纠正一个根本性误判：塔倍率不是「点亮后乘绩效」

本轮读平台论坛两篇高赞文（`44770798147735` ATOM 篇 55 赞 / `43561782887575` Base Payment 篇 65 赞）确认了真实机制：

| 机制 | 内容 | 对排序的影响 |
|---|---|---|
| **倍率按数据集类别结算** | Dynamic Pyramid Multiplier 是 **Base Payment 的 Quality Factor 组成**，按 `Region × Delay × Dataset Category` 的全平台拥挤度定档（冷门 1.3–1.8，pv1 垫底 1.0） | 倍率属于 **Quality 维度**，不是乘在 Sharpe 上的收益系数 |
| **★ 木桶短板效应** | 一条表达式混用多个数据类别时，**倍率按最低的那个算** | 混数据候选的高倍率腿**完全作废** |
| **★ 三数据集以上计 0 塔** | 混入 ≥3 个 Dataset Category ⇒ **直接计为 0 个 Pyramid** | `1YNMAA8M` 应直接淘汰 |
| **ATOM 红利** | 单数据集（仅豁免 6 个分组字段）⇒ 免 IS-Ladder、只看 2Y；`[Power Pool + ATOM]` 不占纯 PP 每日 1 个配额 | 单数据集候选天然拿满倍率 |
| **Base 四维度** | Quality / Quantity / Self Growth / Value，**等权平均**（教学模型） | 点塔只影响 Quality 侧的金字塔计数，不能与倍率混算 |

### ⇒ 点塔收益的正确定位

**点亮一座塔 ≠ 塔内 alpha 绩效 × 倍率。** 因为：
- `wpo8olA6` 是 `other47 + shortinterest3` 混数据，木桶短板把它锁在 **SI ×1.3**。点亮 DEU OTHER（×1.8）**对它自己的结算倍率毫无帮助**。
- DEU OTHER 塔现有 2 颗（`2rmGAPqN` = INSTITUTIONS+OTHER、`58gkLAkk` = MODEL+OTHER）**也都是混数据**，同样被各自最低档锁住。

**点塔的真实收益 = 「已点亮金字塔数量 +1」**，作用于 Genius 等级评定与 Quality 侧的金字塔维度，是**独立计数项**，不是倍率乘法。本季度还剩约 50 天，点塔不紧急但不可跨季（跨季清零）。

---

## 1 每颗候选的实际结算倍率（本轮逐字段查证数据集）

| 候选 | 区 | 数据集构成 | 纯度 | 各腿倍率 | **结算倍率** |
|---|---|---|---|---|---|
| **`RREPm361`** | DEU | `analyst7` 单（est_12m_ebi_median / ebt_mean / ebt_mean_4wks_ago） | **ATOM** | ANALYST 1.8 | **×1.8 满额** |
| **`d5a2vxzY`** | DEU | `shortinterest3` 单（max_loan_rate + mean_loan_rate） | **ATOM** | SI 1.3 | ×1.3 满额 |
| `wpo8olA6` | DEU | other47 + shortinterest3 | 混 2 | 1.8 / **1.3** | **×1.3**（高腿作废） |
| `88NmN37X` | DEU | insiders1 + shortinterest3 | 混 2 | 1.6 / **1.3** | **×1.3** |
| `qM7KxkQV` | DEU | shortinterest3 + insiders1 | 混 2 | **1.3** / 1.6 | **×1.3** |
| `9qlz29Oe` | DEU | shortinterest3 + news20 | 混 2 | **1.3** / 1.8 | **×1.3** |
| `Jj8VQwoe` | DEU | shortinterest3 + other47 | 混 2 | **1.3** / 1.8 | **×1.3** |
| `xAvK73Qg` | DEU | shortinterest3 + other47 | 混 2 | **1.3** / 1.8 | **×1.3** |
| `omEdka3v` | GBR | techindi_model + shortinterest3 | 混 2 | 1.6 / **1.2** | **×1.2** |
| `6XdkW08J` | GBR | model38 + shortinterest3 | 混 2 | 1.5 / **1.2** | **×1.2** |
| `P0oolrZq` | GLB | risk60 + dl_riskfree_returns | 混 2 | **1.0** / 1.2 | **×1.0 垫底** |
| **`1YNMAA8M`** | DEU | predictive_starmine + analyst_factor_signals + analyst15 | **混 3** | — | **计 0 个金字塔** |

**两个反转**：
1. `RREPm361` 从第 6 跃升 —— 它是全池**唯一「ATOM + 高倍率 ×1.8」**，且 5 ops 最少。
2. `P0oolrZq` 从第 1 下滑 —— S 3.45/F 2.37 虽全场最高，但 GLB RISK 是**垫底 ×1.0**，混数据又锁死另一腿的 1.2。

---

## 2 总体排序（Quality 代理 = Fitness × 结算倍率，兼顾 Value 与塔计数）

| # | id | 区 | ops | S / F | 倍率 | **F×倍率** | prod | self | ΔS | 稳健 | 塔计数 | 硬闸 |
|---:|---|---|---:|---|---|---|---|---|---|---|:---:|:---:|
| **1** | **`P0oolrZq`** | GLB | 6 | **3.45/2.37** | ×1.0 | **2.37** | .6578 ✅ | .568 | +0.69 | PASS | 0 | **全绿** |
| **2** | **`6XdkW08J`** | GBR | 8 | 2.60/1.95 | ×1.2 | **2.34** | .6267 ✅ | **.3398** | +0.23 | **PASS CV .057** | 0 | 全绿 |
| **3** | **`RREPm361`** | DEU | **5** | 2.02/1.25 | **×1.8** | **2.25** | **.6881 ⚠** | **.3275** | +0.73 | PASS | 0 | **prod 贴线** |
| **4** | **`88NmN37X`** | DEU | 9 | 1.79/1.53 | ×1.3 | 1.99 | **.5541 ✅** | .5538 | **+0.74** | PASS | 0 | 全绿 |
| **5** | **`omEdka3v`** | GBR | 8 | 2.51/1.40 | ×1.2 | 1.68 | .6026 ✅ | .4164 | +0.26 | PASS | **+1 GBR OTHER** | 全绿 |
| **6** | **`wpo8olA6`** | DEU | 8 | 1.65/1.27 | ×1.3 | 1.65 | .6306 ✅ | .5784 | +0.56 | PASS | **+1 DEU OTHER** | 全绿 |
| 7 | `qM7KxkQV` | DEU | 11 | 1.72/1.34 | ×1.3 | 1.74 | .543 ✅ | .5429 | +0.08 | PASS | 0 | 被 #4 同席取代 |
| 8 | `9qlz29Oe` | DEU | 12 | 1.86/1.34 | ×1.3 | 1.74 | .47 | .4552 | +0.08 | **CONDITIONAL 最差** | 0 | 稳健瑕疵 |
| 9 | `d5a2vxzY` | DEU | 12 | 1.60/**1.08** | ×1.3 | 1.40 | .6039 | **.6038** | +0.07 | CONDITIONAL | 0 | 双贴线 |
| ✗ | `xAvK73Qg` | DEU | 11 | 2.04/1.77 | ×1.3 | 2.30 | **未出数** | .5424 | +0.09 | CONDITIONAL | (+1) | **prod fail-closed** |
| ✗ | `Jj8VQwoe` | DEU | 12 | 1.65/1.24 | ×1.3 | 1.61 | .6124 | .5645 | +0.05 | CONDITIONAL | (+1) | 同席 ρ.7372 被取代 |
| ✗ | `1YNMAA8M` | DEU | 8 | 1.58/1.36 | **0 塔** | **0** | .6951 | .6946 | — | — | **0** | **三数据集计 0 塔** |

> **F×倍率只是排序代理，不是收益预测**。论坛明确：倍率如何映射到归一化 Quality 分数未经核实，不能把 Quality 分直接乘倍率。此处仅用于「同等绩效下高倍率更优」的相对判断。

---

## 3 提交方案

### 今天（ET 11-10，剩 1 席）→ **`P0oolrZq`**

理由：
- **硬闸全绿**：prod .6578（余量 .0422）、self .568、ΔS +0.69、稳健 PASS、**无混腿免三问**
- **绩效全场最高**：S 3.45 / F 2.37，对 Self Growth 与 Value 两个维度都是实质拉动
- **完全正交**：与其余 8 颗 ρ ≤ 0.08（对 `omEdka3v` 恰 0.0000），不挤占任何席位
- 6 ops，算子数硬指标优秀
- 唯一短板倍率 ×1.0，但**今天没有既高倍率又硬闸全绿的替代**（`RREPm361` prod 贴线）

### 明天（ET 11-11，4 席）建议序列

| 顺位 | id | 动作 | 拿到什么 |
|---|---|---|---|
| 1 | **`RREPm361`** | **先 `refresh=True` 终验 prod**，落到 .66 以下才交 | 唯一 ATOM ×1.8 + 5 ops 最省 |
| 2 | **`wpo8olA6`** | 补三段式属性，免三问 | **点亮 DEU OTHER**（金字塔计数 +1） |
| 3 | **`omEdka3v`** | 备 2 腿三问 | **点亮 GBR OTHER**（计数 +1） |
| 4 | **`88NmN37X`** | staging 从 `BLOCKED_PROD_UNAVAILABLE` 改判 | ΔS +0.74 最高、免三问 |

若 `RREPm361` refresh 后 ≥0.7 ⇒ 放弃，第 4 顺位递补 `6XdkW08J`（CV .057 全场最稳）。

### 为什么不今天点塔
点塔收益是**金字塔计数**（Quality 侧独立项），本季度还剩约 50 天，且 `wpo8olA6`/`omEdka3v` 明天照样能点。而今天这 1 席若给它们，等于用掉最高绩效候选（`P0oolrZq`）的窗口——它 prod 余量 .0422 也不算宽，拖到明天未必还在。

---

## 4 对后续挖掘的方向性结论（比本轮排序更重要）

1. **停止堆 DEU 混数据候选**。本轮 8 颗 DEU 候选里 7 颗是 `shortinterest3 + X` 混数据，**全部被 SI ×1.3 锁死**，高倍率腿（OTHER 1.8 / NEWS 1.8 / INSIDERS 1.6）一律作废。这是系统性浪费。
2. **优先 ATOM + 高倍率类别**。DEU 的 ANALYST/OTHER/NEWS/MODEL/FUNDAMENTAL/SENTIMENT 都是 ×1.8，只要保持单数据集就能满额结算。`RREPm361`（analyst7 单）就是范本。
3. **严禁三数据集**。`1YNMAA8M` 混了 predictive_starmine + analyst_factor_signals + analyst15 ⇒ 计 0 塔，prod/self 再漂亮也无 Pyramid 收益。
4. **12 座差 1 颗的塔里 10 座无候选**（EUR NEWS ×1.4、USA OTHER ×1.4、KOR PV ×1.4 倍率最高），是下一轮定向挖掘的首选方向。

---

## 5 数据来源

平台论坛 `44770798147735` / `43561782887575`（倍率机制）；`/data-fields` 逐字段查数据集（17 个字段，GBR 需 TOP700、GLB 需 MINVOL1M）；`get_pyramid_multipliers` 倍率表；`get_pyramid_alphas` 当季计数；`alpha_corr_cache` 权威 prod/self；`compute_mutual_correlation` 9×9；`mcp_preflight_once.py` 7 颗；`ledger_kv robustness_*`。

**本轮零提交。**
