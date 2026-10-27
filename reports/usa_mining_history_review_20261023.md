# USA 挖掘历史经验复盘与优化清单（2026-10-23）

> 类型：人工复盘（AGENTS.md §8.13「人工审计与复盘 → `reports/`」）。
> 数据源：`data/wqb.db`（只读聚合）＋ `docs/experience/01~05` ＋ `docs/experience/fail_fast_rules.md`
> ＋ `output_report/USA_regular_alpha_delivery_20261021.md`。
> 快照日：2026-10-23 ｜ 区域：USA（全程未换区）｜ 口径：**严格口径 = 平台 RA 全闸 PASS ＋ prod<0.7 ＋ self<0.7 ＋ 主数据集所在塔未点亮**。

---

## 0. 取数口径与可信度标注

本文所有数字分三档，**不混用**：

| 档 | 含义 | 可直接引用？ |
|---|---|---|
| **A 硬测** | 平台返回或 DB 行级可重算（回测行、alphas 行、wave_results 行） | 可 |
| **B 推导** | 由 A 档聚合而来（比率、分布、排序） | 可，但须带样本量 |
| **C 人工记述** | 复盘文本（`wave_results.key_findings`）里的措辞与结论 | **仅作定性线索**，关键词频次**不等于客观发生率** |

**两个必须先声明的口径陷阱**（本次实测发现，影响所有历史统计）：

1. **`backtest_results.ra_failed_checks` 列的 NULL 是二义的**。AGENTS.md §8.7 规定 NULL = RA 全过，
   但同一节也规定旧缓存行在看不到 RA 项时按 `failed_checks ∩ RA` 回填 —— 落在 `failed_checks` 里的
   **WARNING / ERROR 项不会进 `ra_failed_checks`**。因此 NULL 同时表示「真全过」与「没记全 RA 项」。
   ⇒ **该列不可用于统计 RA 全过率。**
2. **可重算的口径是 `payload_json.failed_checks`**（平台原始 FAIL 名单，按 `wqb.config.RA_CHECK_NAMES` 过滤）。
   覆盖率 **1525 / 1698 = 89.8%**；缺 `failed_checks` 键的 173 行里，**`analyst_consensus` 全族 68 行**、
   `order_book_imbalance` 47 行、`intraday_pv_feats` 31 行、`earnings_sent_matrix` 9 行、`finnews_nlp_scores` 8 行，
   另有 47 行**完全无 payload**。
   ⚠ **这意味着「交付了 5 颗的那一族」恰好落在不可重算区**，而可重算区偏向 8 月前的旧波。
   ⇒ **本文的 dataset / 塔级 RA 全过率带有族间偏差**，读法见 §5 的特别提示。

---

## 1. 一页结论（TL;DR）

> **USA 的瓶颈从头到尾只有一个：prod。IS 侧的 10 倍努力换不来 1 颗可提交 alpha。**

1. **IS→可提交转化实测 15.4%**：RA 硬闸全过的 177 颗里，只有 26 颗测过 prod，其中 **prod<0.7 且 self<0.7 的只有 4 颗**。
   其余 22 颗全部撞墙（prod 0.68 → 0.99），**其中 11 颗 IS 指标相当漂亮（S 1.5–2.6 区间）**。
2. **prod 墙的分布中心在闸门外**：92 颗已测 prod 的 USA alpha 中，**≥0.8 占 44.6%**、
   0.7–0.8 占 12.0%、<0.7 仅 43.5%（其中 <0.5 只有 1 颗）。⇒ **不是尾部问题，是整体问题**。
3. **RA 全过率与可交付性脱钩，甚至反向**（本次最反直觉的发现）：
   RA 全过率最高的数据集 **全部 prod 撞墙** ——
   `web_traffic_engage` 80.0%（8/10，maxS 2.17，prod **0.9908**）、
   `other143` 59.6%（34/57，maxS 2.63，prod **0.9206**）、
   `institutions18` 30.4%（17/56，maxS 1.82，prod **0.9636**）。
   ⇒ **「数据集冷门 / alphaCount 低」完全不能预测 prod**（`docs/experience/03_region_dataset.md` §4 已列 risk70 前科，
   本次在 USA 侧再次复现）。
4. **强度天花板是第二道墙，且先于闸门判定**：大量数据集的 max S 根本到不了 1.58（`pv106` maxS **0.00**、
   `shortinterest29` 0.79、`other596` 0.91、`pv149` 0.74、`analyst7` 0.76、`finnews_nlp_scores` 0.45）。
   ⇒ **开波前先用一条裸探针验强度**（`|S|<0.5` 直接 kill），比事后归因省 3 波。
5. **已点亮塔的代价已经真实发生**：2026-10-23 更正作废 5 颗 `ai_equity_alpha`（MODEL 塔）候选，
   严格口径从 10/10 退回 **5/10**。这是**选集环节漏了一道闸**，不是挖掘能力问题。
6. **复盘文本与客观事实脱节**：110 波复盘里只有 **15% 提到 prod**，而 prod 是 56.5% 的淘汰主因；
   反而 **55% 提到 fitness**。⇒ **复盘模板缺 prod 判读列**，导致注意力错配。
7. **数据保真度缺口**：`ra_failed_checks` 二义 + 173 行缺 `failed_checks` + 47 行无 payload
   ⇒ **跨波自动归因目前做不了**，所有闸频次统计都得手工绕。

---

## 2. 规模与产出（A 档）

| 指标 | 数值 | 来源 |
|---|---|---|
| USA 回测行 | **1698** | `backtest_results WHERE region='USA'` |
| 其中带可重算 FAIL 名单 | 1525（89.8%） | `payload_json.failed_checks` |
| **RA 硬闸全过** | **177（11.6%）** | 上者过滤 `RA_CHECK_NAMES` |
| USA 波次台账 | **110** | `wave_results WHERE region='USA'` |
| 波次结论 | FAIL **58** / PARTIAL **43** / PASS **9** | 同上 |
| 近 30 波结论 | FAIL 17 / PARTIAL 7 / PASS **6** | 按 `updated_at` |
| 已测 prod 的 USA alpha | **92** | `alphas.prod_correlation IS NOT NULL` |
| prod<0.7 | **40**（43.5%） | 同上 |
| 平台当季塔位（2026-10-23） | analyst **LIT**(6) / model **LIT**(4) / earnings 1 / 其余 13 类 0 | 平台 `get_pyramid_alphas` |
| 严格口径交付 | **5 / 10** | 交付报告 §7 |

> **口径提示**：DB 里 `alphas` 有 49 行 USA `platform_status='ACTIVE'`，但其中 10 颗 `fundamental6` +
   若干 2025 年提交属于**往季**，按「点亮 = 当季 ≥3」口径**不点灯塔**。
   ⇒ 「`fundamental` 塔 0 颗」与「DB 里 fundamental6 有 10 颗 ACTIVE」两句话同时成立，不是矛盾。

---

## 3. 失败模式的量化排序（B 档，行级 n=1525）

| 排名 | RA 闸 | 失败行数 | 占比 | 解读 |
|---:|---|---:|---:|---|
| 1 | `LOW_FITNESS` | 1284 | **84.2%** | 头号杀手：信号能出 Sharpe 但**出不来收益效率**（换手/持仓效率拖累） |
| 2 | `LOW_SHARPE` | 1257 | **82.4%** | 与 FITNESS 高度共现（同一批弱信号） |
| 3 | `LOW_2Y_SHARPE` | 1166 | **76.5%** | 远期衰减；USA 专用形态（无三区域检查） |
| 4 | `LOW_SUB_UNIVERSE_SHARPE` | 642 | **42.1%** | **比值闸**（USA 系数 ≈0.433），抬 S 会同步抬它的要求 |
| 5 | `CONCENTRATED_WEIGHT` | 223 | **14.6%** | 数据品质问题（覆盖/类型），参数修不了 |
| 6 | `HIGH_TURNOVER` | 73 | 4.8% | |
| 7 | `LOW_TURNOVER` | 54 | 3.5% | 前置判据可零成本剔除（TO<0.03） |
| 8 | `IS_LADDER_SHARPE` | 20 | 1.3% | 分组轴是最大杠杆（DEU 1.58→2.07） |

**⇒ 结构性读法**：前 3 项（FITNESS / SHARPE / 2Y）都指向**「信号本身不够」**，
共现度高、彼此不独立 ⇒ 一次修好一个闸没意义，**必须换机制或换字段族**。
第 4 项（SUB）是**比值闸**，在 S 已经够 1.58 的前提下仍会挂 ⇒ 靠「加 S」修 SUB 是错路
（`docs/experience/01_platform_gates.md` §2）。第 5 项（CW）是**唯一的数据品质型失败**。

### 3.1 塔级 RA 全过率（**注意 §0 的族间偏差**）

| 塔 | 回测行 | RA 全过 | 率 | 当季塔位 |
|---|---:|---:|---:|---|
| INSTITUTIONS | 63 | 18 | **28.6%** | 未点亮（0） |
| OTHER | 343 | 63 | 18.4% | 未点亮（0，×1.4） |
| RISK | 22 | 4 | 18.2% | 未点亮（0） |
| INSIDERS | 30 | 3 | 10.0% | 未点亮（0） |
| PV | 218 | 19 | 8.7% | 未点亮（0，×1.1） |
| MODEL | 582 | 44 | 7.6% | **已点亮** |
| ANALYST | 16 | 1 | 6.2% | **已点亮**（且族内数据不可重算） |
| OPTION | 25 | 1 | 4.0% | 未点亮（0，×1.3） |
| SHORTINTEREST | 78 | 0 | **0%** | 未点亮（0） |
| FUNDAMENTAL | 30 | 0 | **0%** | 未点亮（0，×1.1） |
| EARNINGS | 10 | 0 | 0% | 未点亮（1，差 2） |

**⇒ 值得注意的两点**：
① **FUNDAMENTAL / SHORTINTEREST 的 RA 全过率精确为 0**（前者 30 行，后者 78 行）——
   这两族在 USA 是**强度层**死透（不是闸门问题），**不建议再投**，与 §9.1 的 fundamental 全线判死一致。
② INSTITUTIONS（28.6%）与 OTHER（18.4%）的 RA 全过率最高，**但两族的 prod 全部撞墙**
   （`institutions18` 0.9636、`other143` 0.9206）⇒ 再次印证 §1.3 的脱钩。

---

## 4. prod 墙：真正的淘汰主因（A 档）

### 4.1 分布（n=92 已测 prod 的 USA alpha）

| 区间 | 颗数 | 占比 |
|---|---:|---:|
| [0, 0.5) | 1 | 1.1% |
| [0.5, 0.6) | 5 | 5.4% |
| [0.6, 0.7) | 34 | 37.0% |
| [0.7, 0.8) | 11 | 12.0% |
| **[0.8, 1]** | **41** | **44.6%** |

⇒ **56.5% 已过 0.7 红线**，44.6% 在 0.8 以上。**分布中心在闸门外**，
与 `docs/experience/02_signal_patterns.md` §8 的「prod 淘汰 68%／端到端 0.10%」同向。

### 4.2 RA 全过 → 可提交的实际转化

```
RA 硬闸全过（payload 口径）           177 颗
  ├─ prod 已测                          26 颗（14.7% 被走到相关性环节）
  │    ├─ prod<0.7 且 self<0.7            4 颗   ← 转化率 4/26 = 15.4%
  │    └─ 撞墙                          22 颗（prod 0.68 → 0.99）
  └─ prod 未测                         151 颗（多数在 IS 阶段已被停）
```

**4 颗双过的 alpha**：`O08EjLVp`（prod 0.5626 / self 0.3321，**已 ACTIVE**，`ai_equity_alpha`）、
`YPx89bQJ`（0.6803）、`58jr102k`（0.6818）、`d5KzLo7v`（0.6964 / self 0.2438，READY 待确认）。
⚠ 后 3 颗全属 `ai_equity_alpha` = **MODEL 塔** ⇒ 按用户规则不可计入交付。
⇒ **严格口径 5 颗（全部 analyst 族）之外，可用未点亮塔的合格品只有 `d5KzLo7v` 一颗候选。**

### 4.3 「IS 漂亮但 prod 撞墙」的实测样本（22 颗里最贵的几个）

| alpha | prod | self | 族 | 说明 |
|---|---:|---:|---|---|
| `A1Qr9Y8W` | **0.9917** | — | risk60 | S 2.39 / F 5.24 / 2Y 3.88 / SUB 1.12 / **RA 全过** ⇒ 教科书级 IS 信号，prod 直接归零 |
| `RRAlbazb` | 0.9369 | 0.5314 | fhp | TO 0.6221 / S 2.62 / F 1.04 / 2Y 2.53 ⇒ IS 侧已达交付标准 |
| `RR6JkEpd` | 0.9377 | 0.7256 | — | self 也撞 |
| `zqrGqVXo` | 0.8092 | — | insider_matrix | 冠军 S 9.25 的族 |
| `78jZmqJO` | 0.9518 | 0.9518 | — | self=prod 的同源孪生 |

⇒ **一个 44.6% 的墙摆在面前，IS 侧再优化 10 倍的期望收益仍然接近 0。**

---

## 5. 数据集层：RA 全过率与可交付性脱钩（关键结论）

| 数据集 | 回测行 | RA 全过 | 率 | max S | prod（实测） | 结局 |
|---|---:|---:|---:|---:|---|---|
| `web_traffic_engage` | 10 | 8 | 80.0% | 2.17 | **0.9908**（0/4 过线） | ❌ 判死 |
| `other143` | 57 | 34 | 59.6% | 2.63 | **0.9206**（0/4） | ❌ 判死（用了 8 波） |
| `institutions18` | 56 | 17 | 30.4% | 1.82 | **0.9636**（0/4） | ❌ 判死 |
| `ai_equity_alpha` | 25 | 7 | 28.0% | 2.57 | 0.64–0.69 ✅ | ⚠ **唯一真交付路径，但 MODEL 已点亮** |
| `chart_return_model` | 28 | 6 | 21.4% | **1.46** | — | ❌ 强度不足（期限错配） |
| `techindi_model` | 49 | 10 | 20.4% | 2.16 | 0.7947 | ❌ |
| `risk60` | 22 | 4 | 18.2% | 2.39 | **0.9917** | ❌ 判死 |
| `insider_matrix` | 61 | 9 | 14.8% | **9.25** | 0.8092（3/4 过线） | ⚠ 冠军撞墙，族内仍有余量 |
| `multifactor_return_pred` | 84 | 13 | 15.5% | 2.10 | — | ⚠ |
| `continuation_score` | 91 | 7 | 7.7% | 1.36 | — | ❌ 强度不足 |
| `pv20` | 46 | 3 | 6.5% | 1.44 | — | ❌ |
| `pv106` | 10 | 0 | 0% | **0.00** | — | ❌ 字段是空列 |
| `shortinterest29` | 68 | 0 | **0%** | 0.79 | — | ❌ 强度死 |
| `multi_horizon_alpha` | 119 | 0 | **0%** | 1.16 | — | ❌ 强度死 |
| `other596` | 29 | 0 | 0% | 0.91 | — | ❌ 强度死 |
| `fundamental14` | 20 | 0 | 0% | 0.84 | — | ❌ 强度死 |

**三条可复用的判据**：

- **判据 A（新的）**：**「RA 全过率」不能用作选集指标**。它衡量的是「信号强不强」，而交付的卡口是
  「机制在生产池里拥不拥挤」。两者在 USA 呈**反向**。⇒ 选集要问的是**机制是否经典异象**，
  不是数据集是否冷门。
- **判据 B**：**max S < 1.58 的数据集直接出局**（`pv106` 0.00 / `shortinterest29` 0.79 / `other596` 0.91 /
  `multi_horizon_alpha` 1.16 / `fundamental14` 0.84 / `chart_return_model` 1.46）。
  ⇒ **开波前 1 条裸探针**（`|S|<0.5` kill，0.5–1.0 需改机制）比事后归因省 3 波。
- **判据 C**：**prod 实测必须前移到第 1 波**。历史代价：`other143` 用了 **8 波**、`risk60` 用了 **3 波**
  才测出 prod 撞墙 ⇒ **13/110 波（11.8%）的波次预算投在事后证明结构撞墙的族上**。
  ⇒ 改法：**每族先花 1 颗探针的 prod 额度**（不占回测槽），prod ≥0.75 即刻封族，再决定是否开波。

---

## 6. 塔层：已点亮塔的代价（已实际发生）

- 2026-10-23 更正作废 5 颗 `ai_equity_alpha` 候选（`YPx89bQJ` / `58jr102k` / `zqrgna91` / `j2eoKKEj` / `N1eLE1de`），
  严格口径 10/10 → **5/10**。
- **根因不是挖得不好，而是选集环节漏闸**：扩挖时按「字段数 1108 / 机制可组合性」选集，
  **没走 `campaign_intel s0-select`（自带已亮塔剔除）**；已亮塔检查直到提交前才想起。
- **已固化的对策**（Task #55）：S0 选集即剔已亮塔，`--include-lit` 才保留。
  **但补挖 4 颗的执行侧仍需每波核对**（`campaign_intel.py pyramid --region USA --delay 1` 快照写进 S0 产物）。
- **遗留风险**：`insider_agg_matrix` 属 INSIDERS 塔（未点亮，×1.1）；若按「DS 列表」而非「平台类别」判断，
  其 DB 行 `pyramid_multiplier=1.5` 实为 **D0 值**（USA/D1/insiders 真值 **1.1**）⇒ **别用 DB 行的乘数判塔位**。

---

## 7. 机制层：USA 已验证 / 已证伪的构造（C 档，但有 A 档读数支撑）

### 7.1 已验证有效

| 机制 | 证据 | 关键条件 |
|---|---|---|
| **平行模型对同一目标的分歧** | `ai_equity_alpha` 5 颗 S 2.19–2.67 / prod 0.64–0.69 | 两条腿都是「对收益的预测」 |
| **分析师修正的量级/偏度结构** | 前 5 颗交付（S 1.61–2.05） | 单数据集、单概念、非加权混腿 |
| **decay 5→8 的换手杠杆** | `fhp` 波 3：TO 0.7628→0.6221，S 仅 −8%，F/2Y/SUB 不动 | 只在**已过强度线**的族上用 |
| **unisiverse/中性化轴重排** | `usa_cma_w3`：MARKET 优于 SUBINDUSTRY | 逐档实测，**非单调** |

### 7.2 已证伪（别再试）

| 路线 | 证伪读数 | 通用结论 |
|---|---|---|
| **同模型多配置分歧** | `chart_return_model` 四组配置分歧 \|S\| ≤ 0.49 且正负无序 | **分歧腿必须来自「信息源不同」的模型**；同模型同数据只改正则/窗口 = 抽样噪声 |
| **文本分类器之间的分歧** | `other635` 5 个分歧臂全负（最好 −0.86，取反 +0.86） | 差分提取的是分词/词典标注差异，经济含义退化为「事件强度」⇒ 方向反、RN 塌成风格 |
| **经典异象（借券费率/交易成本/流动性溢价）** | `risk60` prod 0.9917；`pv106` maxS 0.00（字段空列） | 「冷门数据集 + 经典异象」**不提供相关性优势** |
| **新闻语气/极性方向** | `news_transformer_scores` 波 88/89 全灭（max \|S\| 0.50） | 两种极性强度都预测负收益 ⇒ 机制是**关注度/热度**，不是语气方向 |
| **1-bar 期限的预测字段** | `chart_return_model` `_t100` 臂 S 1.22 / F 0.37 / 2Y **−0.01** / TO 57% | D1 最早次日成交 ⇒ 1-bar 预测在可交易时点前已衰减，只剩高换手 + 近零 2Y |
| **fundamental 域全线** | 20+ 数据集，最高 fnd1 S 1.17；塔级 RA 全过率 **0%** | 字段退化（映射/元数据/覆盖 0.429）或强度不足 |
| **混合权重 / 等权混腿** | 110 波复盘仅 1 波提及 | 铁律已生效，**不是当前瓶颈**（这条不用再查） |

### 7.3 尚未验证的空白（下一步的候选空间）

- `insider_agg_matrix`（INSIDERS 未点亮）：USA 侧 17 字段全是「金额量级」族 + 唯一方向量 `directional_indicator_2`，
  **USA 零回测**；跨区证据显示金额量级族在 EUR 仅 3 条死臂、在 GLB/DEU 全灭 ⇒ **是 virgin territory，但方向不明**。
- `insider_matrix`（INSIDERS 未点亮）：冠军 `zqrGqVXo` S 9.25 但 prod 0.8092；族内 3/4 颗 prod<0.7 ⇒ **族内还有余量**。
- `earnings_sent_matrix` / `fundamental110` / `fund_holdings_panel` / `institutions18`（INSTITUTIONS 塔 RA 全过率最高 28.6%）
  —— 但 `institutions18` prod 0.9636 ⇒ **换族不换机制**。

---

## 8. 波次层：复盘质量本身的问题（C 档，110 波文本统计）

| 关键词 | 命中波次 | 占比 | 对照客观事实 |
|---|---:|---:|---|
| fitness | 60 | 55% | 客观失败率 84.2%（头号）⇒ 关注度**偏低** |
| 2Y | 32 | 29% | 客观 76.5% ⇒ 关注度**严重偏低** |
| 换手 | 30 | 27% | 客观 4.8% ⇒ 关注度**严重偏高** |
| 归因/机制 | 29 | 26% | — |
| 平滑/衰减 | 23 | 21% | — |
| SUB | 23 | 21% | 客观 42.1% ⇒ 偏低 |
| 结构性/天花板/封存/判死 | 21 | 19% | — |
| **prod** | **16** | **15%** | **客观 56.5% 撞墙 ⇒ 严重偏低** |
| 分组轴 | 9 | 8% | 破 IS_LADDER 的最大杠杆 ⇒ 偏低 |
| 等权/混腿 | 1 | 1% | 铁律已生效 |

**⇒ 复盘模板的三处失配**：
① **prod 缺席**（15% vs 56.5%）—— 复盘只写 IS 侧，导致每波结论「IS 达标 ⇒ 候选」，
   而 prod 才是真淘汰主因；
② **换手被过度关注**（27% vs 4.8%）—— 换手在 USA 只占 4.8% 的失败行，
   复盘却常以换手为结论主语（`docs/experience/05_antipatterns.md` §2 说的「同族连提」才是换手相关真问题）；
③ **分组轴被低估**（8%）—— 它是 USA 唯一实测有效的 IS_LADDER 杠杆。

**⇒ 复盘模板应固定四列**：① 强度上限（max S 及其来源）② 机制方向与证伪条件
③ **prod 读数（含未测的显式标记）** ④ 闸缺口排序（差值而非是否 FAIL）。

---

## 9. 数据保真度与工具链缺口（P0）

### 9.1 回测载荷：原始 checks 没有落库

- `payload_json` 是**扁平行**（`sharpe`/`fitness`/`failed_checks`/…），**平台原始 checks 数组未保留**
  ⇒ ① 平台给每个 check 的 `limit`/`value` 没有留痕；② 无法还原「差多少」；
  ③ 无法重算「比值闸系数」（SUB 的 limit/sharpe 只能靠事后单查）。
- 后果直指本次复盘：**§3 的闸频次能算，§4 的 prod 转化只能靠 `alphas` 侧凑**，
  **§5 的 dataset 级 RA 全过率被 §0 的族间偏差污染**。

### 9.2 `ra_failed_checks` 的二义 NULL

AGENTS.md §8.7 的 fallback（`failed_checks ∩ RA`）会漏掉 RA 项的 WARNING / ERROR
⇒ **列 NULL ≠ RA 全过**。⇒ 写入方必须按 §8.7 用 `compute_webdata_failed_counts(checks)["ra_failed_names"]` **现算**，
不得用 payload 兜底。**这条已在 §8.7 写了，落地还没做。**

### 9.3 提交队列的骨架签名会抹掉分组参数

`d5KzLo7v` 被误标 `PROD_SIBLING`（骨架比对 `tail(winsorize(group_rank(ts_zscore(F,N),G),std=2),...)`
**不含 G 的取值**）⇒ 与 `zqrGqVXo`（`subindustry`）被判同族，而 `d5KzLo7v` 用 `market`（prod 0.6964 vs 0.8092）——
**分组轴是 USA 最有效的 prod 杠杆，却被 dedup 抹掉了**。⇒ 骨架签名必须含**分组轴 + 全部设置档**。

---

## 10. 优化清单（按优先级，含验证方式）

### P0 — 影响终局产出

| # | 优化项 | 依据 | 落地位置 | 验证方式 |
|---|---|---|---|---|
| **P0-1** | **prod 探针前移到第 1 波**：每族先花 1 颗探针的 prod 额度（不占回测槽），prod ≥0.75 ⇒ 封族，不开整波 | 13/110 波（11.8%）投在事后撞墙族；`risk60` 用 3 波才测出 0.9917 | 新增 `prod_probe` 门禁（`campaign_intel` 或 wave 计划阶段） | 下一族开波时记录「探测→封族」耗时；目标：撞墙族波次占比 < 5% |
| **P0-2** | **落库原始 checks**：`payload_json` 增存平台 checks 数组（name/result/limit/value），或至少存 RA 项快照 | 173/1698 行缺 FAIL 名单；limit/value 无留痕 | `src/wqb/store/_backtest.py`（`upsert_backtest_rows`） | 重跑一次收批后 `payload_json` 含 `checks`；历史行不可回填，**只对新波生效** |
| **P0-3** | **`ra_failed_checks` 写入方改为现算**（`compute_webdata_failed_counts`），删掉 payload 兜底路径 | NULL 二义使该列不可统计 | `src/wqb/store/_backtest.py::ra_failed_names` | 加单测：故意构造含 RA-WARNING 的行，写库后该列**非空** |
| **P0-4** | **选集判据从「数据集冷门」改成「机制是否经典异象」** | §5 判据 A：RA 全过率与可交付性反向 | `campaign_intel s0-select` 的排序键 + 画像模板的选集段 | 下一族选集时写明「机制 ≠ 经典异象」的理由，事后核对 prod |

### P1 — 影响单波效率与复盘质量

| # | 优化项 | 依据 | 落地位置 | 验证方式 |
|---|---|---|---|---|
| **P1-1** | **探针前置**：开波前 1 条裸探针验强度，\|S\|<0.5 直接 kill | `pv106` 0.00 / `shortinterest29` 0.79 / `other596` 0.91 / `multi_horizon_alpha` 1.16 | 画像模板 §「预注册判据」+ 波计划 | 每波记录探针读数与是否 kill |
| **P1-2** | **复盘模板固定四列**（强度上限 / 机制方向与证伪条件 / **prod 读数（含未测标记）** / 闸缺口排序） | §8：prod 只在 15% 复盘出现，客观 56.5% | `review_wave.py` 的 key_findings 生成 + 复盘模板 | 下一批复盘抽查 prod 列覆盖率 ≥ 80% |
| **P1-3** | **提交队列 dedup 签名含分组轴与全部设置档** | §9.3：`d5KzLo7v` 误判 | `tools/submit_queue.py dedup` | 用 `d5KzLo7v`（market）vs `zqrGqVXo`（subindustry）做回归用例，**必须判不同族** |
| **P1-4** | **塔位快照写进 S0 产物**（每波） | §6：漏这道闸已造成 5 颗作废 | `campaign_intel pyramid` 输出并入 S0 产物 | 每波 S0 产物含 pyramid 快照 |
| **P1-5** | **换手前置判据常态化**（TO ∈ [0.03, 0.70]） | `fhp` 波 3 TO 0.7628 撞闸；LOW_TURNOVER 3.5% | `to_prefilter.py` 接入波收批 | 收批后自动标注越界行 |
| **P1-6** | **USA 已判死数据集清单落 `tracking/USA/reference/` 并被 S0 自动剔除** | §5 表格 + 交付报告 §9.1/§9.2/§9.3（fundamental 全线 / risk60 / pv106 / other143 / other635 / chart_return_model / chart_model_alpha / pv149 / news_transformer_scores …） | `tracking/USA/reference/usa_dead_datasets.md` + S0 过滤 | 下一族选集时该清单命中数 > 0 即拦下 |

### P2 — 沉淀与治理

| # | 优化项 | 依据 | 落地位置 |
|---|---|---|---|
| **P2-1** | **把 USA 10 月的新实证补进经验库**（`docs/experience/01~05` 最后更新 2026-09-29） | op_arity fail-closed 修复（已在 04 §14.6）、insider_matrix 画像、other635/chart_return_model 判死、载荷 schema 分裂、本文 §4–§5 | `docs/experience/` 新增小节或并入 02/05 |
| **P2-2** | **经验库补一条「选集不看 RA 全过率」的铁律** | §5 判据 A | `docs/experience/05_antipatterns.md` §7 清单 |
| **P2-3** | **本报告的结论落 `tracking/USA/reference/` 区域层** | `docs/experience/` 是跨区层，USA 专属读数应进区域层 | `tracking/USA/reference/` |
| **P2-4** | **清理本轮 `logs/_tmp_*.py` 只读探针** | AGENTS.md §6 第 4 条：临时脚本用完即弃 | `logs/` |

---

## 11. 立即可执行的下一步（按当前状态）

当前严格口径 **5/10**，还差 4 颗，全部必须落在**未点亮塔**（USA/D1：earnings 1、fundamental 0、
**insiders 0**、institutions 0、macro 0、news 0、option 0、other 0、pv 0、risk 0、sentiment 0、
shortinterest 0、socialmedia 0）。

按本报告的结论，优先级如下（**每族都按 P0-1 先探 prod**）：

1. **`insider_agg_matrix`（INSIDERS，×1.1）** —— USA 零回测、字段族全新、塔未点亮。
   ⚠ 已知风险：USA 只有「金额量级」族，无有符号买卖额；唯一方向量是 `directional_indicator_2`。
   ⇒ **P0-1 探针必做**（1 颗，先验 prod）。
2. **`insider_matrix`（INSIDERS）** —— 族内 3/4 颗 prod<0.7，冠军 S 9.25；
   `d5KzLo7v`（prod 0.6964 / self 0.2438，RA 全过）**已在提交队列 READY**，**只差用户确认** ⇒
   **这是当前唯一一颗「零新增回测即可入册」的候选**，应优先取得确认。
3. **`earnings_sent_matrix` / `earnings` 塔** —— 当季差 2 颗即点亮，×1.2，**塔收益最大**。
4. `other`（×1.4）/ `sentiment`（×1.4）/ `option`（×1.3）—— 乘数高但需避开已撞墙的 `other143`/`other635` 机制。

---

## 附录 A：复现命令（只读）

> 本轮探针脚本是一次性的，已按 `AGENTS.md §6` 规则 4 清理；下面三段是**自包含**的口径，
> 粘贴到临时 `.py` 后 `python -X utf8 <file>` 执行即可（§0 说明为何不走 `ra_failed_checks` 列）。

**A-1 规模与波次分布**

```python
import sqlite3
c = sqlite3.connect("file:data/wqb.db?mode=ro", uri=True)
print(c.execute("SELECT COUNT(*) FROM backtest_results WHERE region='USA'").fetchone())
print(c.execute("SELECT COUNT(DISTINCT wave) FROM backtest_results WHERE region='USA'").fetchone())
print(c.execute("SELECT verdict,COUNT(*) FROM wave_results WHERE region='USA' GROUP BY verdict").fetchall())
```

**A-2 RA 硬闸全过率（可信口径：`payload_json.failed_checks` ∩ `wqb.config.RA_CHECK_NAMES`）**

```python
import json, sqlite3, sys
sys.path.insert(0, "src")
from wqb.config import RA_CHECK_NAMES
RA = set(RA_CHECK_NAMES)
c = sqlite3.connect("file:data/wqb.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
tot = with_p = ra_pass = 0
for r in c.execute("SELECT dataset, payload_json FROM backtest_results WHERE region='USA'"):
    tot += 1
    if not r["payload_json"]:
        continue
    try:
        fc = json.loads(r["payload_json"]).get("failed_checks")
    except Exception:
        continue
    if fc is None:
        continue
    with_p += 1
    if not [n for n in fc if n in RA]:        # 空 = RA 硬闸全过
        ra_pass += 1
print(tot, with_p, ra_pass, f"{ra_pass/with_p:.1%}")   # 1698 / 1525 / 177 / 11.6%
```

**A-3 prod 墙分布 + RA→prod 转化**

```python
# prod 墙：alphas.prod_correlation 分桶（只统计 prod_correlation 已实测的行）
#   SELECT
#     CASE WHEN prod_correlation>=0.8 THEN '>=0.8' WHEN prod_correlation>=0.7 THEN '0.7-0.8'
#          WHEN prod_correlation>=0.6 THEN '0.6-0.7' WHEN prod_correlation>=0.5 THEN '0.5-0.6'
#          ELSE '<0.5' END AS bucket, COUNT(*)
#   FROM alphas WHERE region_id=1 AND prod_correlation IS NOT NULL GROUP BY bucket;
#   -- 实测：>=0.8 41 / 0.7-0.8 11 / 0.6-0.7 34 / 0.5-0.6 5 / <0.5 1
# 转化率：RA 全过子集 ∩ prod_correlation<0.7 ∩ self_correlation<0.7 ⇒ 4/26 = 15.4%
```

**A-4 塔位快照（平台真相，非 DB）**

```bash
python tools/campaign_intel.py pyramid --region USA --delay 1
```

## 附录 B：本文引用的既有文档

- `docs/experience/01_platform_gates.md` —— 四闸、SUB 比值律、配额、相关性取数、点塔口径
- `docs/experience/02_signal_patterns.md` —— 组合形态铁律、破闸旋钮、IS→OS 衰减、漏斗真相、轴层数扫描
- `docs/experience/03_region_dataset.md` —— 区域画像、已判死数据集清单、跨区死路检查
- `docs/experience/04_engineering.md` —— 工程纪律、闸 SEM、op_arity fail-closed（§14.6）
- `docs/experience/05_antipatterns.md` —— 反模式与已证伪路径
- `docs/experience/fail_fast_rules.md` —— 七信号、`classify_failure`、换手前置判据
- `output_report/USA_regular_alpha_delivery_20261021.md` —— 交付清单、已点亮塔更正、§9 补挖记录
