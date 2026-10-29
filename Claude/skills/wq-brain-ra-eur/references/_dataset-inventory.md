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

### 2.1 产出可提交 alpha 的数据集（含「已占位、无剩余席位」的标注）

| 数据集 | 类别 | 机制 | 产出 | 状态 |
|---|---|---|---|---|
| **`analyst7`** | analyst | ★ 修正**广度/扩散**读数（`est_12m_<科目>_raisednum/lowerednum`），非幅度 | `E56Jea7P`(SENTIMENT 塔) / `leAXvaLn`(INSTITUTIONS 塔) / `e76xGOQO` / `LL5dmv9a` / `Grge2lN3` / `786pLKnb` | ★ **EUR 主力产源（≥6 颗）**。科目按 2Y 分层：ebt/dps/gps/pre 高（1.6–2.6），ebi/eps/sal 封顶 1.57。读数按 prod 分层：广度 0.65 / 扩散 0.78。详见 `analyst.md` |
| `analyst_factor_signals` | analyst | 分析师修正幅度 ÷ 分歧度 | `786pLKnb` | ⚠ **PPA 通道**（不算 RA），且 prod 0.9994 ⇒ **腿已死** |
| `techindi_model` | other | ML 预测收益率（分位 × horizon） | `LL5VwgO1`(CH_REG) / `e76kv2xE`(EUR, UNSUBMITTED) | ⚠ **EUR 侧已无剩余席位**（不是"无信号"）：唯一 prod 过线的结构是**双窗秩乘积** `multiply(rank(ts_mean(F,2)), rank(ts_mean(F,252)))`（`e76kv2xE` prod **0.6916** / S2.60 / 2Y1.94 / sub1.67），但它已被优化版 `LL5VwgO1` 占位——`e76kv2xE` 实测 **self 0.9980** ⇒ 锁死。其余路径（`tm_N` 模型族 + `group_scale` 幂次）4 次 prod 实测 **0.7454/0.7794/0.7819/0.8163**，幂次 0.8–2.1 全扫 S 恒 2.65–2.74（`group_scale` 把幂次影响归零）⇒ 子路径判死 |
| `predictive_starmine` | other | ARM 分析师修正模型（`arm_*`） | `RRAvGrn0`（prod **0.5437**，ACTIVE，pyramid INSIDERS+MODEL） | ⚠ **死的是「rank 水平读数」，不是数据集**：`rank(ts_backfill(arm_score_5pt_scale_2,22))` 等 6 条水平读数 S 0.10–0.49 ⇒ 死；活的是**二阶差分/极值差读数** `subtract(rank(ts_max_diff(rank(arm_secondary_earnings_component_score_3),149)), ts_rank(ts_delta(ts_delta(arm_preferred_earnings_component_score,22),22),500))` ⇒ S1.99 / prod 0.5437（已占位）|
| `fundamental23` | fundamental | 投资复合因子（`bank_assets_investment` + `intfvalld1_vbts`） | `1YNerr2X` / `e75pkq7E` | ✅ 可提交（prod 0.6896）。⚠ 换字段无用：iabs/iads/fbds/sebv 任意组合互测 **0.75–1.00**（`e75pkq7E` 与 `1YNerr2X` 相关 **1.0000**）⇒ 只 1 席 |
| `fundamental72` | fundamental | PIT 财报比率（CFO/Assets） | `rKd5lAo8`（prod 0.6747） | ✅ 可提交。其它比率（EBITDA/负债/库存/折旧）S 0.06–1.26 ⇒ 只 CFO/Assets 有效 |

### 2.2 判死数据集（按死因归类，**同族免测**）

> ⛔ **判死必须写明「死的是哪个读数 / 结构」，不许写「该数据集死」**（2026-10-29 三次同型错误换来的）：
> | 数据集 | 我判死的读数 | 实际有效的读数 | 后果 |
> |---|---|---|---|
> | `news46` | 情绪极性分（77 条全 S<0.6） | **新闻条数=关注度** `sum_story_count` | 白跑 77 条 |
> | `techindi_model` | `tm_N` + `group_scale`（prod 0.745–0.816） | **双窗秩乘积**（prod 0.6916） | 白跑 12 条；且该结构已被 `LL5VwgO1` 占位 |
> | `predictive_starmine` | ARM rank 水平读数（S 0.10–0.49） | **二阶差分/极值差**（S1.99 / prod 0.5437，已占位） | 白跑 6 条 |
>
> 判死前必做两件事：① 读 `references/<类别>.md` 里该数据集的**全部历史结论**（里面常有已过线的 prod 实测值）；
> ② `get_alpha_details` 读该数据集已 ACTIVE alpha 的 `regular.code`，看它用的是哪种**读数形态**（水平 / 变化 / 极值差 / 双窗）。

| 死因 | 判据 | 命中数据集 |
|---|---|---|
| **TO 爆炸** | 探针 TO > 0.7 | `insiders1`(1.52–1.61)｜`socialmedia15`(1.23–1.33)｜`news20`(0.88–1.24, cov 0.963)｜`news54`(1.44)｜`news18`(0.73–0.94)｜`earnings_sent_matrix`(1.61)｜`insider_agg_matrix`(1.43)｜`analyst40`(1.50–1.63)｜`pv37`(0.46–1.28)｜`intraday_pv_feats`(1.15)｜`insider_trx_matrix`(0.88–1.67)｜**`earningscall_sentiment`(1.07–1.57)** |
| **returns 不足**（F 闸数学封顶） | 反算 `returns < 3.5%` | `fund_holdings_panel`(2.33%)｜`macro27`(2.27%)｜`analyst4`(1.4%)｜`imbalance5`(2.66%)｜`insider_feats`(3.9%)｜`dl_riskfree_returns`(3.8%) |
| **S 不足** | 双结构最好 S < 0.5 | `analyst45`(0.36)｜`analyst9`(0.45)｜`sentiment7`(0.43)｜`other553`(≈0)｜`analyst11`(≤0.1)｜`other571`(≤0.44)｜`other545`(≤0.63)｜`other315`(≤0.16) |
| **近静态** | 探针 TO < 0.02 | `pv106`（价差水平，且符号为负）｜`pv13` 图特征(0.012–0.086)｜`other455` node2vec-PCA(**0.010–0.012**) |
| **噪声型（平滑即杀）** | 不平滑有 S、平滑即崩 | `continuation_score`(+0.56 → −0.79)｜`analyst69`｜`ai_news_scores` |
| **元数据 / 无信号字段** | cov≥0.5 字段全为标识类 | `other567`(地址/编码)｜`other128`(sector/ticker)｜`pv109`(无 cov≥0.5)｜`pv173`(`*_unit_name`)｜`other384`(cov 全 <0.5)｜`investor_activity`(cov 全 <0.5)｜**`news54`**(40 字段=时间戳/标志位/原始文本，仅 1 数值字段)｜**`earnings6`**(4 个数字字段 cov 仅 0.5258) |
| **数据伪影** | S 异常高 + TO 打满 | `pv106.transaction_cost_estimate`(S 11.18 / TO 1.0 / 2Y 0) |
| **机制存在但近期断档**（2026-10-18） | 2Y Sharpe < 0 | `institutions6`（广度版 S 0.86 但 **2Y −0.30**；数量/金额版 S 为负）|
| **prod 池永久锁定**（2026-10-18） | 同族三次结构改动 prod 变化 <0.04 | `analyst_factor_signals`「修正幅度÷分歧度」全族（prod 0.9231 / 0.8907 / 0.9260，最近邻=自家 PPA `786pLKnb`）|
| **覆盖率结构性不足**（2026-10-29 新增） | cov < 0.85 ⇒ sub 闸不可达（不必跑三闸） | `fundamental28`（1605 字段但 **cov 恒 0.50** → sub 0.52 vs 限 0.82）｜`earnings_sent_matrix`(0.51)｜`macro27`(0.33)｜`imbalance5`(0.55)｜`socialmedia15`(0.34) |
| **信号层判死**（2026-10-29 新增，已排除覆盖率因素） | 多结构 × 多中性化实测 \|S\| 天花板 < 1.0 | **news**：`news73`(16 条 0.58) / `news17`(8 条 0.44) / `news_sentiment_nlp`(6 条 0.17)｜**sentiment**：`sentiment21`(14 条 × subind/country 两轴 0.36) / `sentiment27`(11 条 0.39)｜**institutions**：`institutions6`(22 条 × FAST/SUBIND 两档 0.56) / `fund_holdings_panel`(6 条 0.52)｜**pv**：`intraday_pv_feats`(订单流/买卖价差 11 条 0.44) / `pattern_scores`(形态相似度 6 条 0.72) / `pv37`(涨跌量拆分 6 条 −0.49)｜**other**：`analyst45`(众包观点含目标价隐含涨幅 6 条 0.40) / `dl_riskfree_returns`(分位概率 6 条 0.46) / `global_seasonal_model`(6 条全负) / `ai_equity_alpha`(prod 0.8052) |
| **杠杆不适用**（2026-10-29 新增） | 结构本身可过但某杠杆破坏性 | `risk70` 风格暴露：TO 0.009–0.021 ⇒ vol 过低 ⇒ F 卡 0.83–0.95，结构性不可达（除 `anlystsn`）｜`fundamental23` + `group_scale`：sub 崩到 0.63–0.76（水平量读数禁用 group_scale）|

### 2.3 已测但**非判死**（信号带 / 未穷尽）

| 数据集 | 最好读数 | 缺口 | 备注 |
|---|---|---|---|
| `sentiment27` | S 1.33 / returns **5.68%** | S 缺 0.25 | **天花板第 5 次确认**（结构/轴/幂次/平滑/L2 级联/vec 聚合/16 包装算子全试） |
| `stock_search_trends` | S 0.76 / TO 0.92 | returns 2.7% | Google Trends 注意力 |
| `other460` | 历史最好 S 0.77 | 未挖 | 1393 字段「未来趋势下跌概率」，OTHER ×1.5，全未开采 |
| `analyst7`（幅度读数 × ebi/eps/sal） | S 1.63–1.97 | 2Y 顶 1.46–1.57 | 三路（幅度/广度/双读数）+ 倾斜 W0.3–2.0 + 时序窗 20/35/60 + decay 10–80 全扫 ⇒ **科目天花板**，非结构问题 |

> ⚠ 已从本表移除：`dl_riskfree_returns`（已归入 2.2 信号层判死）、`pattern_scores`（已判死）。
> 旧表两处自相矛盾（同一集既在 2.2 又在 2.3），以 2.2 为准。

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
