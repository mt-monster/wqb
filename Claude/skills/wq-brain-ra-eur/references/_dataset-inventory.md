# EUR 数据集全量普查与已测状态（2026-10-14）

> **用途**：开新战役 / 选数据集前**先读本表**，直接跳过已判死族，避免重复投波次。
> **口径**：`GET /data-sets?category=<C>&region=EUR&delay=1&universe=TOPCS1600&instrumentType=EQUITY`（**不带 `limit`**；带 `limit=100` 会 HTTP 400）。
> **铁律**：任何「穷尽」声明前必须重跑全量枚举——2026-10-14 复核发现本区**共 173 个数据集**（早期误记为 21/33 个）。

---

## 一、EUR 数据集总量（平台权威枚举）

| 类别 | 数据集数 | 本季塔状态 | 纳入挖掘？ |
|---|---:|---|---|
| model | 46 | **已点亮** | ❌ 排除 |
| other | 36 | 未点亮 | ✅ |
| news | 20 | 未点亮 | ✅ |
| pv | 20 | 未点亮 | ✅ |
| analyst | 16 | **已点亮** | ❌ 排除 |
| fundamental | 13 | **已点亮** | ❌ 排除 |
| risk | 5 | **已点亮** | ❌ 排除 |
| sentiment | 5 | 未点亮 | ✅ |
| insiders | 3 | 未点亮 | ✅ |
| earnings | 2 | 未点亮 | ✅ |
| institutions | 2 | 未点亮 | ✅ |
| macro | 2 | 未点亮 | ✅ |
| socialmedia | 2 | 未点亮 | ✅ |
| imbalance | 1 | 未点亮 | ✅ |
| **合计** | **173** | 已点亮 4 类 / 未点亮 10 类（**93 个数据集**） | — |

> ⚠ 「已点亮塔」按**平台类别**判定，且**按自然季度清零**（2026Q4：MODEL/FUNDAMENTAL/ANALYST/RISK 各 1 颗）。
> 曾误把 PV/News/Other 当「已点亮」而整块排除 —— 务必先跑 `get_pyramid_alphas` 确认。

---

## 二、已测数据集（≈25 个）与判死速查

### 2.1 产出可提交 alpha 的数据集（**唯二**）

| 数据集 | 类别 | 机制 | 产出 | 状态 |
|---|---|---|---|---|
| `analyst_factor_signals` | analyst | 分析师修正幅度 ÷ 分歧度 | `786pLKnb` | ⚠ **PPA 通道**（不算 RA），且 prod 0.9994 ⇒ **腿已死** |
| `techindi_model` | other | ML 预测收益率（分位 × horizon）× **双窗秩乘积** | `LL5VwgO1` | ★ **CH_REG (RA), ACTIVE** |

### 2.2 判死数据集（按死因归类，**同族免测**）

| 死因 | 判据 | 命中数据集 |
|---|---|---|
| **TO 爆炸** | 探针 TO > 0.7 | `insiders1`(1.52–1.61)｜`socialmedia15`(1.23–1.33)｜`news20`(0.88–1.24, cov 0.963)｜`news54`(1.44)｜`news18`(0.73–0.94)｜`earnings_sent_matrix`(1.61)｜`insider_agg_matrix`(1.43)｜`analyst40`(1.50–1.63)｜`pv37`(0.46–1.28)｜`intraday_pv_feats`(1.15)｜`insider_trx_matrix`(0.88–1.67)｜**`earningscall_sentiment`(1.07–1.57)** |
| **returns 不足**（F 闸数学封顶） | 反算 `returns < 3.5%` | `fund_holdings_panel`(2.33%)｜`macro27`(2.27%)｜`analyst4`(1.4%)｜`imbalance5`(2.66%)｜`insider_feats`(3.9%)｜`dl_riskfree_returns`(3.8%) |
| **S 不足** | 双结构最好 S < 0.5 | `analyst45`(0.36)｜`analyst9`(0.45)｜`sentiment7`(0.43)｜`other553`(≈0)｜`analyst11`(≤0.1)｜`other571`(≤0.44)｜`other545`(≤0.63)｜`other315`(≤0.16) |
| **近静态** | 探针 TO < 0.02 | `pv106`（价差水平，且符号为负）｜`pv13` 图特征(0.012–0.086)｜`other455` node2vec-PCA(**0.010–0.012**) |
| **噪声型（平滑即杀）** | 不平滑有 S、平滑即崩 | `continuation_score`(+0.56 → −0.79)｜`analyst69`｜`ai_news_scores` |
| **元数据 / 无信号字段** | cov≥0.5 字段全为标识类 | `other567`(地址/编码)｜`other128`(sector/ticker)｜`pv109`(无 cov≥0.5)｜`pv173`(`*_unit_name`)｜`other384`(cov 全 <0.5)｜`investor_activity`(cov 全 <0.5) |
| **数据伪影** | S 异常高 + TO 打满 | `pv106.transaction_cost_estimate`(S 11.18 / TO 1.0 / 2Y 0) |
| **机制存在但近期断档**（2026-10-18 新增） | 2Y Sharpe < 0 | `institutions6`（广度版 S 0.86 但 **2Y −0.30**；数量/金额版 S 为负。见 `_probe-sop.md` §9⑥）|
| **prod 池永久锁定**（2026-10-18 新增） | 同族三次结构改动 prod 变化 <0.04 | `analyst_factor_signals`「修正幅度÷分歧度」全族（prod 0.9231 / 0.8907 / 0.9260，最近邻=自家 PPA `786pLKnb`）。见 `_probe-sop.md` §9⑤ |

### 2.3 已测但**非判死**（信号带 / 未穷尽）

| 数据集 | 最好读数 | 缺口 | 备注 |
|---|---|---|---|
| `sentiment27` | S 1.33 / returns **5.68%** | S 缺 0.25 | **天花板第 5 次确认**（结构/轴/幂次/平滑/L2 级联/vec 聚合/16 包装算子全试） |
| `dl_riskfree_returns` | S 1.40 / F 0.71 / returns 3.8% | 需 S ≥ **1.81** | 单分位 ≠ 更好（与 techindi 相反）；已测 11 条 |
| `stock_search_trends` | S 0.76 / TO 0.92 | returns 2.7% | Google Trends 注意力 |
| `pattern_scores` | ≤0.52 | — | 形态相似度 |

---

## 三、未测数据集（60 个，按「字段数 × 低拥挤」排序）

> 判据：`flds` = 平台字段数；`αC` = alphaCount（越低越空旷）。**已点亮类别（model/fundamental/analyst/risk）不列**。

| 数据集 | 类别 | flds | αC | 机制初判 |
|---|---|---:|---:|---|
| `pv87` | pv | 1649 | 885 | 大 PV（拥挤） |
| `pv20` | pv | 1475 | 585 | 大 PV（拥挤） |
| `pv30` | pv | 558 | 283 | ★ **GROUP 聚类轴 + MATRIX PCA 因子载荷** |
| `sentiment21` | sentiment | 210 | 681 | 情绪（TO 风险） |
| `news23` | news | 136 | 103 | ★ **PE/VC 创投数据**（融资额/基金管理规模） |
| `news7` | news | 118 | 293 | 事件（TO 风险） |
| `pv173` | pv | 105 | 25 | ❌ 已测＝元数据判死 |
| `news17` | news | 88 | 92 | 事件 |
| `pv29` | pv | 80 | 164 | ★ **GROUP 统计聚类轴** |
| `earnings6` | earnings | 66 | 1617 | 拥挤 |
| `other384` | other | 66 | 42 | ❌ 已测＝低覆盖判死 |
| `news31` | news | 53 | 104 | 事件 |
| `news21` | news | 47 | 1262 | 事件（拥挤） |
| `investor_activity` | pv | 47 | 9 | ❌ 已测＝低覆盖判死 |
| `macro27` | macro | 33 | 472 | ❌ 已判死（returns 2.27%） |
| `insider_matrix` | other | 33 | 73 | 内部人矩阵（与 insider_feats 同族？） |
| `workforce_flow_skills` | other | 33 | 0 | 劳动力数据（cov 0.25 低） |
| `euro_equity_imbalance` | other | 31 | 129 | 订单失衡（cov 0.31 低） |
| `event_sentiment_signals` | other | 26 | 22 | 事件情绪 |
| `sentiment26` | sentiment | 19 | 461 | 情绪 |
| `other296` | other | 19 | 56 | 财报电话会（VECTOR 稀疏 ⇒ TO 风险） |
| `other546` | other | 13 | 13 | 未知 |
| `other250` | other | 12 | 22 | 未知 |
| `event_relation` | other | 12 | 2 | 事件网络 |
| `institutions6` | institutions | 11 | 90 | 机构持仓 |
| `other335` | other | 10 | 2207 | 拥挤 |
| `insiders12` | insiders | 8 | 201 | 内部人 |
| `socialmedia12` | socialmedia | 6 | 1072 | 社交（拥挤） |
| `search_interest` | other | 5 | 7 | 搜索兴趣（与已判死的 stock_search_trends 同族） |
| `stock_cluster_dl` | other | 5 | 1 | DL 聚类 PCA（cov 低） |
| … | | | | 其余多为 1–4 字段的微型集 |

**未测集合的结构性判断**：以 **news 事件型（TO 爆炸族）+ PV 拥挤族 + 微型/低覆盖集** 为主；
其中**唯一的机制性新机会 = `pv29`/`pv30` 的「统计聚类 GROUP 轴」**（可作**新颖分组轴**，是工具箱中「换轴」杠杆的原料）。

> ⚠ **2026-10-18 修正**：`pv30` 的统计聚类 GROUP 轴（平台实测 195 个 cov=1.0 字段）**已实测，对 prod 无效**——
> `KPmnqaGg` prod **0.9260**（比 industry 基线的 0.9231 更高），且 S 1.78→1.60、2Y 1.89→1.46、robust 1.23→0.85。
> ⇒ **「换轴」不是 prod 杠杆，且对本族全面劣化**，不要再投。详见 `_probe-sop.md` §9④。

---

## 四、使用方式

1. 开波前：本表 + `_probe-sop.md` 的「失败模式预筛」⇒ 30 秒排除已判死族；
2. 若要用 `pv29`/`pv30` 的聚类轴：注意 GROUP 字段**不能当信号字段**（只能当 `group_*` 的第 2 参），且必须先取平台实时类型；
3. 每收一批就**回写本表**（把新判死集并入 §2.2，把新读数并入 §2.3）。
