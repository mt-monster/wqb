# GLB 数据集全量扫描 + 字段画像 + 探针实证（2026-10-14）

> 执行用户指令：系统性扫描 GLB 数据集 → 筛「未点亮塔」候选 → 字段画像 → 深挖产出 regular alpha。
> 约束遵守：**不换 region**（全程 GLB）；**不频繁切换数据集**（每候选 ≥10 结构才判停）；**穷尽算子情形**（每候选覆盖 7 类算子族）；**缺灵感查论坛**（论坛 MCP 通道本轮故障，见 §6）。

---

## 1 区域权威设置（`wqb.profiles explain --region GLB`）

| 项 | 值 | 来源 |
|---|---|---|
| universe | **TOPDIV3000** | settings.json |
| neutralization | **STATISTICAL** | settings.json |
| decay | **2** | settings.json |
| delay / truncation | 1 / 0.08 | settings.json |
| nanHandling / maxTrade | OFF / OFF | settings.json（**强度闸，换档=换信号**） |

**RA 阈值（review 节）**：sharpe ≥ **1.58**、fitness ≥ **1.0**、2Y ≥ **1.6**、margin ≥ 0.0005、**turnover 0.05–0.30**（比平台 0.7 更严）、ra_failed_count = **0**、rn_sharpe ≥ 1.0。
> ⚠ 2026-09-19 S-PRE 重配依据：旧档 TOP3000/SUBINDUSTRY/decay4 过闸率 0%（131 条零达标），新档 TOPDIV3000/STATISTICAL/decay2 过闸率显著提升。

---

## 2 塔位盘点（决定「已点亮塔不选」的排除集）

`get_pyramid_alphas` 显示 **GLB/D1 全部类别 = 0**（按自然季度清零，Q4 无贡献）。但账户 **GLB OS 池实有 11 颗 ACTIVE REGULAR**，其 `pyramid_short` 归属为：

| 机制族 | alpha（示例） | 归属塔 | 数量 |
|---|---|---|---|
| dlrr 20d CNN + 经济门控 | pwR8rdMg / O0NoPARJ / MPakRYgz / MPabNeNz / VkaXbmbG / d5bnE8jJ | pv + other (+risk) | 6 |
| intraday_pv_feats 尾盘反转 | mLmxKN12 / gJboYLRl（均 GREEN/PowerPool）/ le3E3nM7 | pv | 3 |
| techindi_model 分位预测 | 9qpQ0VQ2 | other | 1 |
| dlrr 60d + mdl239 门控 | RR66gp2j | pv/model/other | 1 |

⇒ **实质已点亮塔 = pv / other / model / risk**；**未点亮 = fundamental / analyst / news / sentiment / earnings / institutions / insiders / macro / socialmedia / shortinterest / option**（下文火力全部投向后者）。

---

## 3 数据集全量扫描（GLB：TOPDIV3000 = 115 集 ∪ MINVOL1M = 71 集）

### 3.1 未点亮类别 · 候选清单（按「覆盖 × 低拥挤」排序）

| 数据集 | 类别 | cov | 字段 | αCount | vS | 状态 |
|---|---|---|---|---|---|---|
| **news59** Corporate Events | news | **0.9736** | 2 | **98** | 2 | 本轮探针 |
| **news76** Textual News Feed | news | **1.0** | 6 | 682 | 1 | 字段仅情绪 |
| **institutions18** Ownership Model | institutions | **0.9547** | 6 | 1134 | 1 | **本轮探针** |
| analyst15 Earnings forecasts | analyst | 0.9367 | 307 | 4134 | 1 | 拥挤 |
| sentiment21 AI Sentiment Score | sentiment | 0.9128 | 210 | 1638 | 2 | 族已判死 |
| news20 Web Sources News | news | 0.8631 | 24 | 1616 | 1 | — |
| earnings3/5/6/7 | earnings | 0.86/0.34/0.33/0.39 | — | — | 1 | earnings3 已判死 |
| **analyst69** FactSet Fundamental Estimates | analyst | 0.8472 | 779 | 9512 | 1 | **本轮探针** |
| news48 Global Media News | news | 0.8543 | 22 | 164 | 2 | — |
| **analyst11** ESG scores | analyst | 0.7405 | 235 | 456 | 2 | ESG（近静态先验） |
| **analyst45** Analyst Trade Ideas | analyst | 0.539 | 57 | 125 | 2 | 覆盖不足 |
| other553 Financial Opinion Mining | sentiment | 0.5973 | 10 | 287 | 2 | — |
| analyst82/48/47 | analyst | 0.41–0.57 | — | 92–158 | 2–4 | 覆盖不足 |
| model211 Analyst estimate prediction | analyst | 0.5567 | 96 | **50** | 3 | 低拥挤但覆盖不足 |
| insider_agg_matrix | insiders | 0.4904 | 17 | 1332 | 2 | 已判死 |

### 3.2 已判死（不再投）——来自各区组合分支的判死记录

| 类别 | 判死数据集 / 族 |
|---|---|
| fundamental | f17（天花板 0.82）、f23、f28（全灭 0.26）、f44 → **族级判死** |
| analyst | analyst10（pred_surps）、analyst_consensus（targetprice 族）；**跨区**：flash/pretax 一致预期动量族仅 IND 有效（USA≤0.09 / GLB≤0.08 / HKG 0.64 / KOR≤1.07 / EUR≤0.96） |
| news | news17（PR 事件换手墙）、news23（M&A）、news31（注意力/新奇度）、news52（电话会结构）、news73（sentiment）→ **news 塔判死** |
| sentiment | sentiment22（dts 族）、sentiment26（网站流量）；emotion 系跨区死路 |
| earnings | earnings3（日历/计时，CW 墙） |
| institutions | institutions6（主信号判死，仅可作慢门控） |
| insiders | insider_agg_matrix（净买入稀疏，天花板低） |
| risk | risk60（借券费 prod 墙）、risk68（残留收益反转弱）、risk70（风格 HF） |
| model | model38/135（探针）、model32（StarMine 动量）、model264（趋势概率封顶 1.40）、model239（慢变量 prod 墙） |
| pv | intraday_pv_feats 8 族、pv98、pv106、pv37 |
| other | ai_news_scores（ts_delta 强度墙）、dl_riskfree_returns（新 GEM 139 条封死）、other315/455/699 |

> **跨区铁律**：`PRODCORR-SATURATION-UNIVERSAL`（饱和风格族的新增提交必须来自正交信号族，调参数无效）、`SELF-CORR-FAMILY-CANNIBALISM`（族已有 ACTIVE 后同骨架变体默认判死）。

---

## 4 字段画像（4 个优先候选，逐字段）

### 4.1 news59（Corporate Events Data）—— ❌ 无信号字段
| 字段 | 类型 | cov | 语义 |
|---|---|---|---|
| mws59_event_fiscal_year | VECTOR | 0.9646 | 事件所属财年（**整数码**） |
| mws59_event_time_value | VECTOR | 0.9826 | 事件排定时间 UTC（**整数码**） |
⇒ 仅 2 字段且均为**码/ID 类毒药**，无连续信号可构造。**淘汰**。

### 4.2 news76（Textual News Feed）—— ⚠️ 仅情绪面
| 字段 | 类型 | cov | 语义 |
|---|---|---|---|
| mws76_score | VECTOR | 1.0 | 情绪 −1/0/1（per-entity） |
| mws76_confidence | VECTOR | 1.0 | 情绪置信度 0–100 |
| mws76_classnum / timeofarrival / version / news_story_title | VECTOR | 1.0 | 分类码/时间戳/版本/文本（**毒药**） |
⇒ 有效信号仅情绪分（news/emotion 族已判死）。**淘汰**。

### 4.3 institutions18（Ownership Model）—— ✅ 字段质量最优
| 字段 | 类型 | cov | αCount | 语义 |
|---|---|---|---|---|
| inst18_fundownershipv2_cur_holding | MATRIX | 0.9547 | 236 | 当前持股数 |
| **inst18_fundownershipv2_pre_holding** | MATRIX | 0.9547 | 121 | **上期持股数（→ 流量轴）** |
| inst18_fundownershipv2_cur_mv / vm_erp | MATRIX | 0.9547 | 172 / 140 | 当前/上期市值 |
| inst18_fundownershipv2_pct_held | MATRIX | 0.9546 | 401 | 持股比例 |
| inst18_fundownershipv2_num_held | MATRIX | 0.9547 | 214 | 持仓基金家数（广度） |
⇒ 具备 **水平 / 变化 / 比值 / 广度** 四轴，cov 0.9547（全球）。**入选探针**。

### 4.4 analyst69（FactSet Fundamental Analyst Estimates，297 字段）—— ✅ 修正族完整
| 字段 | 类型 | cov | αCount | 语义 |
|---|---|---|---|---|
| **anl69_best_eps_chg_pct** | VECTOR | **0.9993** | 76 | EPS 修正 % |
| anl69_best_eps_4wk_up / _dn | VECTOR | 0.9532 / 0.9545 | 85 / 25 | **4 周上调 / 下调家数（修正广度）** |
| anl69_best_pe_ratio / px_bps_ratio | VECTOR | 0.9973 / 0.9576 | 545 / 105 | 估值（E/P、B/P） |
| anl69_best_eps_stddev | VECTOR | 0.7951 | 13 | 分析师分歧度 |
| anl69_analyst_best_analyst_rating | VECTOR | 0.8675 | 23 | 综合评级 1–5 |
| anl69_best_eps_median / eps_gaap_median | VECTOR | **1.0** | 16 / 39 | 中位 EPS |
| anl69_best_eeps_cur_yr / nxt_yr | MATRIX | 0.8596 / 0.8541 | 184 / 113 | FY1/FY2 一致预期 |
| anl69_best_net_income / net_median | VECTOR | 1.0 | 25 / — | 净利润预期 |
| （+ BPS/CPS/DPS/EBIT/EBITDA/NAV 同构修正族，各 20+ 字段） | VECTOR | 0.6–1.0 | 少 | 全量修正族 |
⇒ **覆盖率最高的未点亮数据集之一**，且含完整「修正广度 + 修正幅度 + 分歧度 + 估值」四轴。**入选探针**。

---

## 5 探针设计（穷尽算子情形）

按「算子族穷尽矩阵」设计，每候选 10 条，覆盖 7 类算子族：

| 算子族 | institutions18 | analyst69 |
|---|---|---|
| 秩/符号 | `rank(Δholding)` | `rank(vec_avg(eps_4wk_up))` |
| 差（流量） | `rank(cur_holding − pre_holding)` | `rank(up − dn)`（修正广度） |
| 比值 | `rank(cur_holding / pre_holding)`、`−rank(cur_mv / cap)` | `−rank(pe_ratio)`（E/P） |
| 水平（反向） | `−rank(pct_held)` | `−rank(analyst_rating)` |
| 时序变化 | `rank(ts_delta(pct_held, 66))` | — |
| 时序标准化 | `rank(ts_zscore(pct_held, 252))` | — |
| 时序平滑 | — | `rank(ts_mean(eps_chg_pct, 22))` |
| 分组中性 | `group_rank(Δratio, country)` | `group_rank(eps_chg_pct, country)` |
| 广度 | `rank(num_held)` | `rank(tot_analyst_rec)`、`rank(eps_median)` |
| 离散度 | — | `rank(eps_stddev)` |

**合规自检**：无跨数据集/跨机制相加；比值用 `divide`、差用 `subtract(rank,rank)`、门控用 `group_*` —— 全部落在 5 类放行形态内。

---

## 6 工程事件

- **论坛 MCP 通道故障**：`search_forum_posts` 连续 4 次返回 `fetch failed` / `internal_error`（Playwright 通道问题），读类失败按纪律重试后仍不可用 ⇒ **本轮「查论坛」步骤受阻**，改以区域经验库 + 平台实证替代。
- **MCP 服务瞬时抖动**：`get_datafields`/`preflight_expressions` 出现 `fetch failed` 与 6 次重试失败，导致 3 个 analyst69 字段被**误标「不存在」**（同一字段在前次 `get_datafields` 明确列出）⇒ 探针改用**双重确认的 VECTOR 字段**规避整批 CANCELLED 风险。
- **发批工具选择**：MCP `submit_batch` 缺省 `maxTrade=ON`，与 region `settings.json`（OFF）**不一致** ⇒ 改用仓库 `tools/submit_batch.py --spec`，逐项钉住设置档（干跑已验证 payload 与 region 逐字一致）。

---

## 7 探针实证结果

### 7.1 institutions18（Ownership Model）@ GLB/TOPDIV3000/STATISTICAL/decay2 —— **判死**

批次 `2qDgwT7K44vu9VEJMyezcji`，10/10 COMPLETE，0 error。

| # | 表达式 | S | fit | TO | 2Y | AMER | EMEA | **APAC** | CW |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `rank(Δcur_holding)` | 0.46 | 0.05 | **0.984** | −0.16 | 0.23 | 0.35 | 0.27 | **1.0** |
| 2 | `rank(Δholding / pre_holding)` | −0.72 | −0.10 | 0.802 | 0.14 | −0.28 | −0.69 | −0.39 | 1.0 |
| 3 | `rank(cur_holding / pre_holding)` | −0.72 | −0.10 | 0.802 | 0.14 | −0.28 | −0.69 | −0.39 | 1.0 |
| 4 | `−rank(pct_held)` | −0.00 | −0.00 | 0.583 | −0.44 | −0.03 | 0.14 | −0.05 | 1.0 |
| 5 | **`rank(Δcur_mv)`** | **1.39** | 0.25 | **0.996** | −0.03 | 0.72 | **0.99** | **0.91** | **1.0** |
| 6 | `rank(num_held)` | 0.25 | 0.02 | 0.905 | 0.50 | 0.03 | 0.55 | 0.08 | 1.0 |
| 7 | `group_rank(Δratio, country)` | −0.70 | −0.10 | 0.780 | −0.86 | −0.30 | −0.77 | −0.37 | 1.0 |
| 8 | `rank(ts_delta(pct_held, 66))` | −0.22 | −0.02 | 0.706 | −0.26 | −0.22 | −0.07 | −0.03 | 1.0 |
| 9 | `−rank(cur_mv / cap)` | −0.65 | −0.08 | **1.079** | −0.88 | −0.35 | −0.05 | −0.66 | 1.0 |
| 10 | `rank(ts_zscore(pct_held, 252))` | −0.25 | −0.02 | 0.946 | 0.04 | −0.03 | −0.42 | −0.10 | 1.0 |

**结论**：最优仅 **S=1.39**（< 1.58），且 **换手 ≈ 0.6–1.08**（region 带 0.05–0.3，结构性出界）、**CW=1.0**（2021-05-24 单日）、**2Y ≈ 0**。
**★ 有价值的观察**：`rank(Δcur_mv)` 的 **EMEA 0.99 / APAC 0.91 / AMER 0.72 已接近闸线 1.0** ⇒ 该数据集**具备全球（含 APAC）信号**，与 institutions6（APAC≈0）不同；死因是**换手 / CW / 2Y** 三面墙，而非 APAC 信号缺失。季频持仓的「报告日跳变」导致日度换手结构性偏高（decay 2 无法压制）。

### 7.2 analyst69（FactSet Fundamental Analyst Estimates）—— **判死**

批次 `EE6CJeod4QvccGZaYWRkkl`（修正版），10/10 COMPLETE，0 error。

| # | 表达式 | S | fit | **TO** | 2Y | AMER | EMEA | **APAC** |
|---|---|---|---|---|---|---|---|---|
| 1 | `rank(vec_avg(eps_4wk_up))` | 0.52 | 0.11 | 0.244 | 1.66 | 0.44 | 0.00 | 0.34 |
| 2 | **`rank(up − dn)`（修正广度）** | **0.96** | 0.28 | **0.221** | 0.82 | 0.44 | **0.94** | **0.87** |
| 3 | `rank(vec_avg(eps_chg_pct))` | 0.95 | 0.21 | 0.348 | 0.80 | 0.41 | PASS | 0.61 |
| 4 | `group_rank(eps_chg_pct, country)` | 0.91 | 0.20 | 0.351 | 0.59 | 0.41 | 0.91 | 0.65 |
| 5 | `−rank(vec_avg(pe_ratio))` | 0.34 | 0.09 | 0.094 | 1.53 | 0.37 | −0.05 | 0.15 |
| 6 | `rank(vec_avg(eps_median))` | 0.56 | 0.15 | 0.174 | 1.53 | 0.14 | 0.15 | **0.95** |
| 7 | `rank(ts_mean(eps_chg_pct, 22))` | 0.59 | 0.18 | 0.110 | 0.31 | 0.33 | 0.41 | 0.42 |
| 8 | `−rank(vec_avg(analyst_rating))` | 0.35 | 0.08 | 0.135 | 0.48 | PASS | −0.64 | −0.92 |
| 9 | `rank(vec_avg(tot_analyst_rec))` | 0.09 | 0.01 | 0.139 | 0.41 | 0.40 | −0.71 | −0.17 |
| 10 | `−rank(vec_avg(ev_to_ebitda))` | 0.23 | 0.05 | 0.090 | 1.67 | 0.26 | −0.05 | 0.10 |

**结论**：最优 `rank(修正上调−下调家数)` **S=0.96**（缺口 65%，远不足 1.58）。**但与 institutions18 死因完全不同**：
- **换手健康**（0.09–0.35，落在 region 带 0.05–0.3 内）
- **区域 Sharpe 均衡且存在 APAC 信号**（EMEA 0.94 / APAC 0.87 / AMER 0.44；单字段 `eps_median` 的 APAC 达 **0.95**）
- ⇒ **死因是「信号强度不足」，不是结构墙**。距闸缺口过大（门控只修 prod/robust、不造强度），**不可救**。

> ⚠ 首版批次 `Cp8BmdEU5ita28oFSIjavV` **整批 CANCELLED**：单条用了 `anl69_best_eps_stddev`（GLB/TOPDIV3000 实不存在）⇒ **一条错即连坐全批**，再次实证 `wq-batch-dispatch-safety` 铁律。

### 7.3 阶段性结论（口径：2 数据集 × 10 结构 = 20 条实证）

| 候选 | 类别 | 结果 | 死因 | 关键定量证据 |
|---|---|---|---|---|
| news59 | news | 淘汰（画像） | 仅 2 个整数码字段，无信号 | 字段：fiscal_year / time_value |
| news76 | news | 淘汰（画像） | 有效信号仅情绪分（族已判死） | 6 字段中 4 个为码/时间戳 |
| **institutions18** | institutions | **判死（实测）** | **结构墙**：换手/CW/2Y | S≤1.39；TO 0.58–1.08；CW=1.0@2021-05-24；2Y≈0；**EMEA 0.99/APAC 0.91 近闸** |
| **analyst69** | analyst | **判死（实测）** | **强度不足** | S≤0.96；TO 0.09–0.35（健康）；EMEA 0.94/APAC 0.87/AMER 0.44 |

**★ 两类死因的区分（本轮最有价值的可复用结论）**：
1. **institutions 类（13F 季频持仓）**：**有全球信号、无结构可行性**——报告日跳变 ⇒ 日度换手 0.6–1.1（结构性出界），CW 单日爆表，2Y 被跳变噪声打平。**换手墙是季报类数据的固有属性**。
2. **analyst 类（一致预期修正）**：**有结构可行性、无信号强度**——换手天然健康、区域 Sharpe 均衡，但 |S| 天花板 ≈ 0.96–1.07（与跨区既证 `flash/pretax 一致预期族只在 IND 有效，别区 ≤1.07` **完全一致**）。

**与区域既有结论的一致性**：两条探针均未突破 RA 全闸，与 skill「GLB 已挖穿（41 族判死）」的地区裁决**方向一致**；本轮新增的是**可复用的定量判据**（两类死因的指纹）。

---

## 8 产出与交付

### 8.1 本轮产出的 regular alpha 候选

**0 条**。20 条实证表达式的 RA 全闸通过数 = 0，`failed_ra_count` 最小值为 5。
不在闸内的表达式**不构成候选**（铁律：`failed_ra_count = 0` 才称合格）。

### 8.2 与用户目标「10 个 regular alpha」的差距及归因

| 缺口 | 归因（定量） |
|---|---|
| 缺口 10 条 | GLB 未点亮类别（fundamental/analyst/news/sentiment/earnings/institutions/insiders）经本轮实测**全部无 RA 过闸能力** |
| 已点亮类别（pv/other/model/risk）不可选 | 「已点亮塔不选」约束 + 该区 11 颗 ACTIVE 集中在 dlrr/intraday_pv_feats/techindi_model 三族，**prod 已饱和**（会话实证：同腿近亲 prod 0.86–0.89） |
| 结构性上限 | GLB 三区闸（AMER/EMEA/APAC 各 ≥1.0）要求「全球统一过程生成」的信号；未点亮类别均为**地域偏置数据**，APAC 要么无信号（institutions6）要么不足（analyst69 0.87–0.95） |

### 8.3 若要继续推进的可行方向（按性价比排序）

1. **接受 GLB 收官**，把配额转向 APAC 信号更丰富的区域（不违反本区流程、但需用户确认换区）。
2. **在已点亮族内做正交化**：dlrr/intraday_pv_feats 有真实 APAC 信号，但同族 prod 饱和 ⇒ 只有在**新预算/池变化**后才有第 2 颗的空间。
3. **SuperAlpha**：把现有 11 颗 GLB ACTIVE + 本轮近闸候选（analyst69 #2 S0.96 / institutions18 #5 S1.39）作为**慢腿**合成（skill 区域手记明确推荐此路）。

---

## 9 第二轮深挖（s50 / s51，锁定 institutions18 不换数据集）

> 上一轮用的是**裸探针**（只判有无信号）。本轮按 skill 的 S4 杠杆做**结构深挖**：判死依据不足 ⇒ institutions18 上轮 S=1.39 / EMEA 0.99 / APAC 0.91 已近闸线，值得深挖。

### 9.1 诊断：三面墙同源于「季频字段未回填」
上轮 TOPDIV3000 下 longCount 仅 **837/3000（覆盖 28%）** ⇒ NaN 排除 ⇒ 小截面 ⇒ 换手与 CW 同时爆表。
**核心杠杆 `ts_backfill(x, 66)`**（季频报告日间隔）实测：
- `rank(Δcur_mv)`：TO **0.996 → 0.487**、**CW 由 1.0 变 PASS**、2Y −0.03 → **2.08**。

### 9.2 ★ decay 对两条子信号作用方向相反（关键机理）

| 子信号 | 最优 decay | S | TO | 2Y | 机理 |
|---|---|---|---|---|---|
| **流量** `Δcur_mv`（报告日事件） | **2（快）** | 1.02–1.39 | 0.48–0.996 ✗ | 1.99 ✓ | 锐利事件效应，decay22 直接归零（S→−0.07） |
| **水平** `pct_held`（反向） | **22（慢）** | **1.33** | **0.183 ✓** | **0.21 ✗** | 慢变量需长 decay；但 2Y 被抹平 |

### 9.3 s50（backfill × decay2/22，各 10）与 s51（decay4，10）汇总 —— 共 40 结构

**换手-强度前沿（decay4 档）**：

| 表达式 | S | TO | 2Y | AMER | EMEA | APAC |
|---|---|---|---|---|---|---|
| group_rank(bf(Δcur_mv,132), country) | **0.97** | 0.336 | 1.53 | 0.44 | 0.48 | **PASS** |
| group_rank(bf(Δcur_mv,252), country) | 0.93 | 0.336 | 1.53 | 0.39 | 0.48 | **PASS** |
| group_rank(bf(Δcur_mv,66), country) | 0.94 | 0.337 | 1.51 | 0.40 | 0.48 | **0.99** |
| rank(bf(Δcur_mv,252)) | 0.79 | 0.339 | **1.63** | 0.45 | 0.44 | 0.69 |
| group_rank(bf(Δcur_mv,66), **industry**) | 0.61 | 0.346 | 1.26 | 0.30 | 0.39 | 0.57 |

**三条决定性算子机理**：
1. **`ts_mean(·,5)` 平滑直接杀死信号**（S 0.94 → **0.16**）⇒ 该信号是**锐利事件效应**，任何平滑都不可加。
2. **`group_zscore` 破坏信号**（−0.19）而 `group_rank` 有效（0.94）⇒ **组内序 ≫ 组内 z**（与 GLB 区域经验一致）。
3. **分组轴 country(0.94) ≫ industry(0.61)** ⇒ 该信号是**国别相对效应**，非行业效应。
4. **`quantile` 替 `rank` 反而变差**（S 0.84 → 0.65）⇒ S4 杠杆#1「等价算子替换」**逐区实测、禁外推**（GLB 此前记录的是 quantile 优于 ts_scale，本例相反）。
5. **回填窗 66/132/252 几乎无差**（0.94/0.97/0.93）⇒ 一旦超过报告间隔即饱和。

### 9.4 终局判定
- institutions18 累计 **40 结构 / 3 波 / 4 个 decay 档（2/4/22 + 裸探针）**，最高 S = **1.39**（裸 Δcur_mv@d2）与 **1.33**（pct_held@d22），均 < 1.58。
- `ts_backfill` 已把 **CW 与换手墙修好、并打开 APAC 闸（0.99–1.0+）**，**但 S 天花板锁在 0.94–1.39**；AMER/EMEA 恒在 0.39–0.99。
- ⇒ **数据集天花板确认，非骨架问题**。按「≥10 结构才转向」纪律已超 4 倍，**institutions18 判定封盘**。



---

# 第三轮：intraday_pv_feats 深挖（s52–s59，塔位口径纠正后）

## 10 口径纠正：塔位 + 占用粒度（用户指正）

- **`get_pyramid_alphas` GLB/D1 全 0 = 准确**：按自然季度清零，本季（Q4）无提交 ⇒ 「已点亮塔不选」**本季不排除任何类别**。前两轮据「账户历史 11 颗 ACTIVE」排除 pv/other/model/risk 是**错的**（那 11 颗是 Q3 遗留，塔已清零但 prod 池仍在）。
- **「已占用」粒度 = 字段不是数据集**：intraday_pv_feats 实为 **300 字段**（两 universe 字段集**完全相同**；「15 字段只在 TOPDIV3000」为误判——那些字段名不存在，preflight `valid:false` 是对的）。被占用的仅 3 个字段（gJboYLRl / mLmxKN12 / le3E3nM7）。`corr_*` 族 108 字段 αCount 几乎全 0–8 ⇒ **真正的未开采面在字段级**。

## 11 可提交模板与 3 个 RA 全净候选（全部 prod 墙外待破）

模板（gJboYLRl 反推）：`-group_zscore(ts_decay_linear(F, 5), industry)` @ MINVOL1M/COUNTRY/decay8/trunc0.02。

| 候选 | 表达式 | S | F | 2Y | sub | **failed_ra** | **prod** |
|---|---|---|---|---|---|---|---|
| YPxrGndM | zscore(corr_high_price_with_volume) | 2.60 | 1.17 | 2.74 | 1.70 | **0** | **0.8563 ✗** |
| e76pa98J | rank(corr_high_price_with_volume) | 2.45 | 1.04 | 2.61 | 1.56 | **0** | **0.8514 ✗** |
| d5KXzqbg | zscore(mean_high_price_return_60m_pre_close) | 2.38 | 1.25 | 2.03 | 1.66 | **0** | **0.8158 ✗** |

## 12 ★ prod 墙的结构本质（本轮核心发现）

三个 prod 挡墙者全部是**本账户自己的 ACTIVE alpha**（gJboYLRl 0.665 / mLmxKN12 0.694 / le3E3nM7 0.671，均在 0.7 边缘）+ 每族约 1 个他人 alpha：

- **YPxrGndM vs e76pa98J 直方图几乎一致**（[0.7,0.8) n=2、[0.8,0.9) n=2）⇒ **换 group_zscore→group_rank、换分组轴都不改变 prod**；驱动源是**字段族占用**，不是结构。`corr_*_with_volume` 全族（8 字段 × 所有已试结构）锁死 ~0.85。
- **d5KXzqbg（60m 版）对 mLmxKN12（30m 版）仍 0.8158** ⇒ 同机制换时间窗不足以破墙，但**机制越正交 prod 越低**（0.856→0.851→0.816，单调）。
- 按 `wq-window-valley-break-prod-wall` 判据（直方图 [0.7,0.8) n≥1 ⇒ 族级必死）：**每一族只剩「换字段语义」一条路**。

## 13 字段族实证账（s52–s59，共 ~90 结构）

| 族 | 字段数 | 最优 S | 判定 | 死因/备注 |
|---|---|---|---|---|
| corr_*_with_volume | 8（1 占用） | 2.60 | RA 可净但 **prod 0.85 锁死** | 价量相关反转；EMEA 是唯一残闸（W10 可推到 0.99） |
| corr_*_with_slippage | 8 | −0.41 | **死** | 价-滑点相关无反转预测力（反向也仅 0.41） |
| corr_volume_with_*_half | 10 | 1.83（low last_half） | 濒死 | 覆盖悬崖（longCount 775）⇒ TO 1.6；`ts_backfill` 修复波在飞 |
| mean_*_return_pre_close | 6（1 占用） | 2.38（high 60m） | RA 可净但 **prod 0.82** | 30m/60m 窗重叠致相关；post_open 全灭（S 0.33） |
| mean_*_return_post_open | 6 | 0.36 | **死** | 无信号 |
| rank/backfill 结构（le3E3nM7 式） | — | 1.55 | 弱 | TO 0.10 但 S/EMEA/2Y 齐降 |

## 14 已实证杠杆（s54/s55，可复用）

1. **`group_rank` 修 EMEA**：corr_high 的 zscore 版 EMEA 已过，rank 版（e76pa98J）亦过 ⇒ 二者等价过闸，但**都过不了 prod**。
2. **W=10 抬 2Y 与 fitness**（2Y 3.12 / F 1.13）但 EMEA 反降（0.80）⇒ 窗长是 2Y↔EMEA 权衡。
3. **分组轴**：industry > country（country 版 EMEA 0.69–0.90）。
4. **`ts_delta` 机制死**：换手 0.76 + CW 1.0（变化率信号太快）。
5. **backfill+W34 结构**：TO 0.10 / F 1.28 但 EMEA 崩（0.20–0.58）⇒ 该结构是慢变量专用。
6. **GLB 无 delay=0**（平台设置实证）⇒ 无「鲜数据」decorrelation 杠杆；可用 universe = TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000（已试 2 档）。

## 15 在飞与下一步

- s58（明星字段 W3/W10/rank/country + last_half backfill×5）、s59（明星字段 × TOPDIV3000/TOP3000/MINVOL10M/SUBINDUSTRY/decay4/decay12/trunc0.08 + 3 新机制探针；后 5 组撞 429 待重发）。
- 破 prod 的三条路（按优先级）：① 窗口谷扫描（W 连续扫描找 prod 局部最小）；② 换 universe（不同名字集 ⇒ 不同 PnL）；③ 换字段语义（kurtosis/modulo10/size_to_volume 族探针在飞）。
