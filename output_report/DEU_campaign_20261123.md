# DEU Regular Alpha 战役报告（2026-11-23 / 24）

> 区域固定 **DEU**（不换区）；universe=TOP500、delay=1；目标 10 颗通过验证的 regular alpha（ATOM 优先）。
> 约束：PV/MODEL/OTHER 三者内部及相互两两禁组腿；它们与其它 category 组腿合计 ≤5；每批 multisim ≤8 臂、一次一批；只挖不提交（提交须用户确认）。
> 本报告随批次滚动更新；「已验证」= 平台 RA 全过 + S/F/2Y 过线 + prod<0.70 + self<0.70 + 十年逐年有仓。

## 1. 塔位（MCP `get_pyramid_alphas` 当季实读，2026-11-23）

| 状态 | 塔 |
|---|---|
| 已亮（≥3） | analyst 7 / model 3 / other 3 / fundamental 3 / shortinterest 5 |
| **差 1** | **insiders 2/3**（本报告交付件可使其 3/3） |
| 差 2 | institutions 1/3、sentiment 2/3 |
| 0/3 | news、option、pv、earnings、macro、risk、socialmedia、imbalance |

- sentiment 三集（snt7/snl27/snt33）实读 **2014–2018 零持仓**（`zqdRJWL8` 等逐年核）⇒ 按十年硬约束排除。
- option1 在数据集级判死清单；imbalance5/macro27/socialmedia12 覆盖率元数据 0（可逆假设，未判死）。

## 2. 交付清单（已验证，未提交）

### #1 vRApe2Av — INSIDERS × MODEL，**PASS**

| 项 | 内容 |
|---|---|
| 数据集 | `insider_agg_matrix`（INSIDERS，34 字段）+ 分析师一致预期（MODEL） |
| 核心字段 | `significant_value_1..4`、`mean_estimate_change_pct_f12m_ebitda_90d_3` |
| 算子逻辑 | **头部重大交易占比** `sig1/Σsig1..4` → `ts_mean(…,66)` → `group_rank(…,sector)`；与 `rank(ts_mean(model90,22))` 相加 → `group_zscore(…,sector)` → `signed_power(…,1.3)` |
| 回测指标 | S **1.70** / F **1.36** / 2Y **2.38** / TO 8.7% / DD 6.55% / margin 18.49bp / LC131 / SC146 |
| 闸 | RA 0；prod **0.5707** ✅；self **0.4780** ✅；2014–2023 全正；pyramids `[INSIDERS ×1.6, MODEL ×1.8]` eff2 |
| 稳健性 | PASS（recent-3 1.69/2.08/2.72，CV 0.20，衰减 1.60） |

### #2 QP0MNr5X — INSIDERS × MODEL，**CONDITIONAL**

| 项 | 内容 |
|---|---|
| 数据集 | `insider_agg_matrix` + 分析师一致预期（MODEL） |
| 核心字段 | `significant_value_1..4`、`predicted_surprise_f12m_ebitda_4`、`mean_estimate_change_pct_f12m_ebitda_14d_4` |
| 算子逻辑 | 头部重大交易占比 + 两条预期修正腿（各 `rank(ts_mean(…))`）→ `group_zscore(…,sector)` → `signed_power(…,1.3)` |
| 回测指标 | S **1.82** / F **1.11** / 2Y **2.96** / TO 23.1% / DD 5.64% / margin 7.44bp / LC127 / SC144 |
| 闸 | RA 0；prod **0.6502** ✅；self **0.5096** ✅；2014–2023 全正；pyramids eff2 |
| 稳健性 | CONDITIONAL（recent-3 CV 0.50、max/min 4.12，无 REJECT 项） |
| 与 #1 关系 | 4 年日 PnL 互相关 **0.5139** ⇒ 可同篮；同族其他变体 0.83–1.00 不可同篮 |

> 两颗均 **非 ATOM**（2 数据集），但为**新核**（不使用已被母件占位的 `insd1_holdings`）。任一颗提交 ⇒ INSIDERS 2/3→3/3。
> 组腿预算：MODEL（trio）× INSIDERS（非 trio）2 条，占用「trio×非 trio ≤5」中的 2。
> ⚠ **与旧 18 篮的互相关**：`vRApe2Av` vs `leadEXnl` = **0.848 > 0.70**（leadEXnl 是 18 篮成员、未提交）；`QP0MNr5X` vs leadEXnl = 0.690（贴线）。20 颗全矩阵的「互相关<0.7 最大子集」= **19 颗（排除 leadEXnl，含本报告两颗）**。⇒ 若 18 篮全部保留，`vRApe2Av` 不能入篮（只能留 QP0MNr5X）；若要保这两颗，需放弃 leadEXnl（S2.20）。这是用户级取舍，本报告不替用户决定。

## 3. 已证伪 / 作废（同族，逐条留痕）

| 候选 | 读数 | 原因 |
|---|---|---|
| 0mPKr3bq / XgaGb3J1 / VkNV0zqM / O0WO8zqq / GrmPOz05 | S1.79–2.36，prod **0.9038–0.9055** | `insd1_holdings` 五腿核已被 2026-11-21 提交母件占位；旧缓存 0.65 不是当前值 |
| 2r5MXqZ6 | S2.16/2Y2.80，prod **0.7689** | 同族 + 4 条 estimate 腿，prod 密墙 |
| 2rOW9xA6 / RRVK9oej（directional_indicator 族） | S1.82/1.86，2Y **1.58**（恰好等于闸，严格不等式 FAIL）/1.33 | prod **0.975**（refresh；孤立 0.9–1.0 桶 n=1 = 已提交母件指纹）⇒ 整族不可交付；`directional_indicator` 也是被提交池覆盖的核心 |
| leadEXnl / j2avPlgW / Jj8qWmlx / Jj8Wn2jO / 1YWeGdGz | S1.70–2.20，prod 0.56–0.65 | 与 vRApe2Av 互相关 0.85–1.00，不可同篮（可作替补） |
| E5Qrx2JG / 6XM7ARLE / 1YWnZ9rK 等 | — | pyramids effective=0（≥3 categories，PV+MODEL+…） |

## 4. INSTITUTIONS 战役进度

- 全字段画像（4 集，完整性闸 4/4 PASS）：[`institutions6`](../tracking/DEU/reference/datasets/institutions6.md)、[`institutions25`](../tracking/DEU/reference/datasets/institutions25.md)、[`fund_holdings_panel`](../tracking/DEU/reference/datasets/fund_holdings_panel.md)、[`institutions1`](../tracking/DEU/reference/datasets/institutions1.md)。
- 已测（institutions6，DEU/TOP500/D1，decay0/SUBINDUSTRY/trunc0.08/nanON）：

| 臂 | 结构 | S | F | 2Y | 判读 |
|---|---|---:|---:|---:|---|
| i1 breadth + model | (买家−卖家)/持有家数 + 2 条预期腿 | **1.15** | 0.64 | 1.46 | 全批最佳，距 S 闸 0.43 |
| i2 净流 + model | 净买入金额/机构持仓市值 + 预期腿 | 1.00 | 0.51 | 1.07 | 弱 |
| i4 低渗透 + model | −机构持股占比 + 预期腿 | 0.98 | 0.50 | 0.71 | 弱 |
| 纯本集三腿 | i1+i2+i4 | −0.29 | −0.11 | −1.14 | 稀释/符号冲突 |
| cap-bucket | i1 经 cap 桶中性化 | −0.04 | −0.01 | −1.03 | 破坏信号 |
| 自身规模桶 | i1 经机构持仓额桶中性化 | −0.13 | −0.03 | −0.97 | 破坏信号 |

- 在飞：8 臂（ts_backfill 252 / market-industry 轴 / ts_zscore / signed_power / ANALYST 搭档 / decay_linear）。结果待收。
- 历史：institutions6 单信号天花板 0.71–0.82（2026-10/11 前序），本批用跨集搭档把 breadth 抬到 1.15；仍需 +0.43 几何增益。
- institutions25（24 字段全 VECTOR）2026-11-03 探针 12 臂天花板 0.61；fund_holdings_panel 9 年窗口 + 0.70 天花板；institutions1 仅 2019–2023 ⇒ 三集暂不投入（保留可逆假设，不判死）。

## 5. 字段画像存档索引（本区规范路径）

| 文件 | 数据集 | 字段数 | 完整性闸 |
|---|---|---:|---|
| `tracking/DEU/reference/datasets/institutions6.md` | institutions6 | 11 | PASS |
| `tracking/DEU/reference/datasets/institutions25.md` | institutions25 | 24 | PASS |
| `tracking/DEU/reference/datasets/fund_holdings_panel.md` | fund_holdings_panel | 18 | PASS |
| `tracking/DEU/reference/datasets/institutions1.md` | institutions1 | 7 | PASS |
| `tracking/DEU/reference/datasets/insider_agg_matrix.md` | insider_agg_matrix | 34 | PASS（前序档，34/34 实测） |
| `tracking/DEU/reference/datasets/sentiment27.md` / `sentiment7.md` / `sentiment33.md` / `risk60.md` / `risk71.md` / `risk88.md` | 前序档 | — | — |

命名规则：`tracking/<REGION>/reference/datasets/<dataset_id>.md`；每字段一行、带平台实读数字；写完必须过 `tools/gates/field_profile_completeness_gate.py`。

## 6. 调优经验摘要（本轮可复用）

1. **缓存 prod 不可用于交付**：insd1_holdings 族 11-19 缓存 0.65 → 11-23 refresh 0.90（母件 11-21 提交）。交付前必须 `check_correlation(refresh=True)`。
2. **2 数据集的上限是硬约束**：平台 pyramids 只对 ≤2 category 计 effective；3 类（如 INSIDERS+INSTITUTIONS+ANALYST）eff=0，S 再高也不进塔。
3. **institutions6 的 breadth 是唯一活腿，但 cap/size 桶中性化会破坏它**（ΔS −1.19/−1.28）；慢季频信号不宜做市值桶中性化。
4. **同集多腿 add 会稀释**：i1+i2+i4 从 1.15 掉到 −0.29（符号/时段错配），与 risk60 C8+C14 等权 add 同一类失败。
5. **批纪律**：multisim ≤8 臂、一次一批；上一批 `all_terminal=True` 后再派下一批。本会话实测 10/8/4 臂批次曾长期 `progress=0.15/0.35 + child_count=0`，取消后重派才动（平台队列拥塞，不是表达式错）。
6. **数据层排除优先于信号层**：sentiment 三集 2014–2018 零持仓 ⇒ 即使 S 2.14/2Y 2.56 也直接出局（`d5WqmExJ`/`QPvK5krW`）。
7. **DEU 已提交池覆盖面很大**：`insd1_holdings`（prod 0.90）、`directional_indicator`（prod 0.975）两个「看起来是新的」核心都已有母件占位；`significant_value` 头部占比是当前少数仍干净的 insiders 核心。找新件必须先 refresh prod，不能只看 S/2Y。
8. **两座未亮塔的 PnL 正交性可利用——但前提是两条腿各自有强度**：risk60 核心（`d5aME0mx`）与 news20 腿（`LLKP3pm1`）4 年互相关 0.223，组合 `[NEWS,RISK]` 实测 S1.36/2Y2.07（`9qlemgje`）——正交性成立，但 news 腿 standalone≈0.1–0.3 ⇒ 组合只比 risk 核心高 0.02，仍不到 1.58。**正交 ≠ 有收益；先验两腿 standalone 强度再谈组合。**

## 7. 缺口与下一步（如实）

- **目标 10 颗，当前 2 颗已验证**；缺口 8。
- **RISK 线索（最高 ROI）**：`d5aME0mx`（risk60，S1.34/F1.22/2Y2.00，**prod 0.6884 ✅ / self 0.3068 ✅**，10 年满仓，仅 LOW_SHARPE+CW 两闸）——只差 S +0.24。
  - 已测：`leanG5Pe`（C8+MODEL 双预期腿）S**1.39**/F1.07/**2Y1.36**（S +0.05 但 2Y −0.64）；`wpodG2kx`（C8+单 90d 预期腿）S**1.48**/F1.33/**2Y0.87**。⇒ **加 MODEL 腿抬 S 但毁 2Y**，risk60 的 S↔2Y 跷跷板未破。
  - 在飞：C8+ANALYST(eps) / C8+C14+ANALYST（`1HYle29oG4xu9Z1ZylyvCjB`）；若仍不过，则 risk60 记为「ATOM+MODEL 双路皆不可达，需换信息源」。
- **NEWS×RISK 交叉（两座未亮塔）已测，未过闸**：`9qlemgje`（nws20 事件情绪 delta + risk60 核心）S**1.36**/F1.00/**2Y2.07**/RA2；`ZYa8MkAx`（M&A 情绪腿）S**1.31**/F0.93/2Y1.53/RA4。risk60 核心单独 S1.34 ⇒ **news 腿只贡献 +0.02 S**（其 standalone 强度≈0.1–0.3），组合无法到 1.58。两座 0/3 塔的「正交组合」路径证伪（不是相关性问题，是 news 腿本身无强度）。
- 结论：在「排除已亮塔数据集 + 十年硬约束 + prod/self<0.70」下，本轮可交付面 = **2 颗**。若要继续冲 10 颗，需要新信息源（未在 DEU 提交池出现过的数据集）或放宽十年/已亮塔约束。
- 其余下一批：8 臂 news20（情绪/事件冲击）；8 臂 institutions backfill/zscore；8 臂 insiders top/directional（新机制，注意 directional_indicator 已被 prod 0.975 覆盖）；macro27（招聘）；socialmedia12。
- 若各批最好 S 仍 <1.58，则 DEU 在「排除已亮塔数据集 + 十年硬约束」下的可交付面≈2 颗，需用户决定是否放宽（例如接受 2019+ 短窗的 sentiment，或接受已亮塔的存量件）。
- **未提交任何 alpha**；提交须用户确认 + `submit_verdict` + prod/self 终验。

### 7.1 交接：下一棒可直接重跑的命令

```text
# 交付件复核（零仿真）
mcp__wq-brain-http__get_alpha_details("vRApe2Av" / "QP0MNr5X")
mcp__wq-brain-http__check_correlation(alpha_id=..., correlation_type="production", refresh=True)
mcp__wq-brain-http__check_correlation(alpha_id=..., correlation_type="self")
mcp__wq-brain-http__get_alpha_yearly_stats(...)
mcp__wq-brain-http__compute_mutual_correlation(["vRApe2Av","QP0MNr5X"], 0.7, 4)

# 已收（2026-11-23）
# [NEWS×RISK] 9qlemgje S1.36/2Y2.07 / ZYa8MkAx S1.31/2Y1.53 —— 未过 S 闸

# 后续 2 臂批（一次一批；>2 臂在本账号调度不动）
logs/_tmp_risk_batch8.json   # 取前 2 条：C8+MODEL / C8+C14+MODEL
logs/_tmp_news_batch8.json   # 前 2 条：nws20 事件情绪 / M&A 情绪 + MODEL
logs/_tmp_insiders_top2.json # 前 2 条：top_significant 占比 / top_directional 占比 + MODEL
logs/_tmp_macro_batch8.json  # 前 2 条：招聘活跃度 / 招聘净增 + MODEL
```
