# USA / fundamental17 字段画像（S1 级 · 2026-10-30）

> 数据集元数据：402 字段 / cov 0.8346 / userCount 2545 / alphaCount 34967 / valueScore 1
> 区域 USA / D1 / TOP3000 ｜ 类别 fundamental ｜ 塔位：FUNDAMENTAL（当前计数 0）
> 本画像结论：选它作 FUNDAMENTAL 塔开波靶，**主机制刻意避开 valuation-momentum**（registry 判死风险，见 §6）。

---

## 1. 为什么选 fundamental17 而不是其他 fundamental 集

| 候选 | 处置 | 理由 |
|---|---|---|
| `fundamental17` | ✅ **本波靶** | 402 字段、cov 0.8346、valueScore 1；字段语义**全部可读**（有明确经济含义），无「Value of the field」式不透明 codebook；含三大正交机制族（成长 / 质量 / 估值） |
| `fundamental67` | ❌ 整集黑名单 | 12 字段中 7 个是前瞻标签（`fnd67_predict_label` / `fnd67_y_pred_prob_0..4`）⇒ 未来信息泄漏 |
| `fundamental22` | ❌ 不可用 | 14 字段全 VECTOR，描述全是 codebook 位置（"Value of the field"）⇒ 语义不透明，无法构造有经济含义的模板 |
| `fundamental91` | ⏸ 未侦察 | 407 字段但 `search="margin"` 返 0 ⇒ 命名体系未知，需换搜索词 |
| `fundamental6` / `fundamental2` | ❌ 极拥挤 | aCnt 881064 / 144800，994 alpha/字段 ⇒ prod 撞墙风险极高 |

---

## 2. 机制族 A —— 成长（Growth）★ 首选开波族

论坛依据（帖 `43153154839831`，1 赞，远低于 50 赞线，机制可采纳）：
**「成长外推反转」** = De Bondt & Thaler (1985) 市场过度反应 + Lakonishok-Shleifer-Vishny (1994) 投资者线性外推 + La Porta et al. (1997) 成长股收坏消息 / 价值股收好消息。帖内明确写 **USA 适用**（"机构主导、beta 分化大的市场（EUR/USA）方向一致"）。

| 字段 | cov | uCnt | aCnt | 描述 | 备注 |
|---|---:|---:|---:|---|---|
| `fnd17_arevchg` | .8961 | 71 | 183 | 营收同比变化 % | ★ 主候选 |
| `fnd17_ttmrevchg` | .8498 | 70 | 212 | TTM 营收同比 % | ★ 主候选（TTM 口径更稳） |
| `fnd17_revchngyr` | .8931 | 93 | 263 | 最近季度 vs 去年同期 % | 季度节奏 |
| `fnd17_revchngin` | .8974 | 74 | 224 | 最近季度 vs 上季度 % | 环比，噪声大 |
| `fnd17_revchngyri` | .9644 | 15 | 50 | 营收变化 % YTD | 极冷门 |
| `fnd17_revtrendgr` | .7834 | 30 | 94 | 5 年营收增长率 | ★ 长周期 |
| `fnd17_revtrend10` | .6482 | 26 | 50 | 10 年营收增长率 | ★ 长周期（覆盖低） |
| `fnd17_revgrpct` | .8517 | 45 | 123 | 3 年营收增长率 % | ★ 帖内「3 年是甜点」 |
| `fnd17_tcprgspe` | .5657 | 13 | 39 | 3 年 EPS CAGR | ★★ 极冷门（uCnt 13），天然低相关 |
| `fnd17_epstrendgr` | .5289 | 10 | 23 | 5 年 EPS 增长率 | ★★ 极冷门 |
| `fnd17_epstrend10` | .4644 | 9 | 19 | 10 年 EPS CAGR | ★★ 极冷门但 cov 低 |
| `fnd17_nitrendgr` | .5293 | 12 | 13 | 5 年净利润 CAGR | ★★ 极冷门 + aCnt 仅 13 |
| `fnd17_ghcspea` | .9285 | 85 | 212 | 年 EPS 同比 %（vs 上一财年） | 覆盖最好 |

**机制要点（来自论坛帖，可直接复用）**：
1. `ts_backfill(x, 20)` —— 财报按季度披露且滞后，回填 20 天保证连续覆盖；
2. **稳健聚合用中位数而非均值** —— 财报发布瞬间的一次性项目（重组/减值）会剧烈扰动均值。⚠️ `ts_median` 是**幽灵算子**（19 个之一）⇒ **必须换等价实现**：`ts_mean` 近似，或 `ts_quantile(x, 20, driver="gaussian")`，或 `winsorize` 后取 mean；
3. `group_zscore(x, subindustry)` —— 消除行业间成长性差异（科技 vs 公用），得到「行业内相对增速」；
4. 方向：**负号做空高增长**（做多被悲观情绪打压的低增速股）；
5. 触发 `trade_when(ts_delta(backfill,5) > 0, ...)` —— 只在增速改善日更新仓位；⚠️ 帖内自承 trade_when 把 2Y 从 1.68 打到 1.55，**须与 decay 配合**。

**跨区/跨窗口先验（帖内原话，可作方向先验）**：1 年增速噪声大反转弱；**3 年 = 「真实成长性 vs 过度外推」甜点**；5 年成长性收敛明显、反转收益衰减。

---

## 3. 机制族 B —— 质量与利润率变化（Quality / Margin Drift）

**核心结构：同一利润率指标的「当前 vs 历史」成对字段** ⇒ 可直接做**利润率变化**（质量改善 / 恶化），与估值、与成长都正交。

| 当前口径 | 历史口径 | 用途 |
|---|---|---|
| `fnd17_tcpngmpoq` 营业利润率-最近季 (cov .9004) | `fnd17_tcpngmpoa` 第1历史财年 (.9010) / `fnd17_2tcpngmpoa` 第2历史财年 (.8957) | 营业利润率**同比变化** |
| `fnd17_tcpngmtpq` 税前利润率-最近季 (.9025) | `fnd17_aptmgnpct` 第1历史年 (.9030) / `fnd17_aptmgnpct2` 第2历史年 (.8976) | 税前利润率变化 |
| `fnd17_tcpngmpnq` 净利率-最近季 (.9025) | `fnd17_tcpngmpna` 第1历史年 (.9030) / `fnd17_a2netmrgn` 第2历史年 (.8976) | 净利率变化 |
| `fnd17_qgrosmgn` 毛利率-最近季 (.7501) | `fnd17_agrosmgn` 第1历史年 (.7370) / `fnd17_agrosmgn2` 第2历史年 (.7317) | 毛利率变化 |
| `fnd17_ttmopmgn` 营业利润率 TTM (.8993) | `fnd17_ry5ngmpo` 5年平均 (.7910) | TTM vs 5年均值的**回归幅度** |
| `fnd17_ngmpnmtt` 净利率 TTM (.9003) | `fnd17_margin5yr` 5年平均 (.7992) | 同上 |
| `fnd17_8_ttmgrosmgn` 毛利率 TTM (.7759, uCnt 12) | `fnd17_grosmgn5yr` 5年均值 (.6380) | 冷门 + 回归幅度 |

**冷门趋势族（uCnt 9–18，prod 低相关红利）**：
`fnd17_gmntrendgr` 5年毛利率增长率 (uCnt 18 / aCnt 40) ｜ `fnd17_npmtrendgr` 5年净利率增长率 (uCnt 11 / aCnt 14) ｜ `fnd17_csptrendgr` 5年资本开支 CAGR (uCnt 17 / aCnt 31)

**「利润率向 5 年均值回归」机制**：这正是帖内「盈利增长均值回归」的近亲，但走的是**利润率**而非增长 ⇒ 与成长外推反转**低相关**，是第二条独立路径。

---

## 4. 机制族 C —— 估值（Valuation）⚠️ 高 prod 撞墙风险，慎用

registry 条目 `USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL` 原文：
> forward E/P z-score ... **PROD 0.9289 with ~2.9k production alphas >0.7 -> valuation-momentum is fully saturated in USA**
> rule: only a mechanism orthogonal to value/momentum could be re-probed, and must be **prod-first checked** before any Mode A

| 字段 | cov | uCnt | aCnt | 描述 |
|---|---:|---:|---:|---|
| `fnd17_ebitda2ev` | .9350 | 375 | **3129** | EBITDA / EV, current ⚠️ 极拥挤 |
| `fnd17_ev2ebitda_cur` | .7872 | 219 | 1146 | EV / EBITDA, current |
| `fnd17_2_ev2ebitda_cur` | .7872 | 374 | **2555** | EV / EBITDA, current（**多版本**） |
| `fnd17_3_ev2ebitda_cur` | .8089 | **20** | **30** | EV / ebitda, current ★★ 极冷门 |
| `fnd17_ebitda2ev_ttm` | .9241 | 292 | 2316 | EBITDA / EV, TTM |
| `fnd17_ebitda2ev_a` | .9327 | 161 | 802 | EBITDA / EV, 用上一财年 EBITDA |
| `fnd17_ev2rev_cur` | .8134 | 186 | 876 | EV / Revenue, current |
| `fnd17_ev_cur` | .9385 | 182 | 789 | **Current Enterprise Value**（市值+净债） |
| `fnd17_ebitda2ev` / `fnd17_ev2ebitda_cur` / `fnd17_3_ev2ebitda_cur` | — | — | — | ★ **多版本同口径 ⇒ 可做「重述差 / 版本分歧」** |
| `fnd17_apenorm` | .6926 | 61 | 138 | 标准化 P/E, 最近财年 |
| `fnd17_apeexclxor` | .6695 | 70 | 125 | P/E（剔非经常项） |
| `fnd17_histrelpe` | .6006 | 109 | 333 | 历史相对 P/E |

⚠️ **纪律**：valuation 族只允许用**冷门版本**（`_3_` 后缀 uCnt 20）或**多版本分歧**构造，**禁止**直接复用 GBR 的 `ts_av_diff(ebitda2ev, 252)` 骨架（那正是 valuation-momentum 位移）。

---

## 5. 机制族 D —— 盈利意外 / SUE（需 analyst 数据集，本集不可用）

论坛帖 `3583773514015`（76 赞，**超 50 赞线 ⇒ 不抄其表达式**）讲 SUE（标准化盈利意外）因子，机制本身成熟但需要分析师预期数据 ⇒ 落在 ANALYST 塔，不属 fundamental17。fundamental17 无「预期」类字段（已逐条读 description 确认）⇒ 本集做不了 SUE。

---

## 6. 派发前必查清单（每次开 fundamental17 波次都要跑）

1. **本地既有台账三查**：`grep -r "fundamental17" docs/ reports/ Claude/skills/` —— 有命中先读「已证伪 / 失败边界 / 判死」章节；
2. **逐条读 description 三分类**：① 明确经济含义且非前瞻 → 可用；② 含 future / forward-looking / target / label / prediction → 黑名单；③ 语义不透明（"Value of the field"）→ 只做探针；
3. **本地算子签名闸** `wqb.expression.op_arity.check_expressions`；
4. **VECTOR 预检** `preflight_expressions(dataset_id="fundamental17")` ⇒ `any_changed == false`（fundamental17 字段均为 MATRIX，但新版本前缀字段 `_2_` / `_3_` / `_8_` 需实测确认类型）；
5. **覆盖门槛**：`longCount + shortCount ≥ 0.35 × 3000 = 1050`（近十年都有数据）；cov 低于 0.6 的字段（`epstrend10` .4644 / `tcprgspe` .5657 / `qdebteps` .5685 / `epstrendgr` .5289 / `nitrendgr` .5293 / `nitrendgr` .5293）优先放探针位而非主线位。

---

## 7. 开波建议（10 个结构互异模板的机制分配）

| 模板族 | 机制 | 字段 | 经济含义 |
|---|---|---|---|
| A1 成长外推反转（反向） | 3 年营收增速取负 + 行业内标准化 | `fnd17_revgrpct` | 明星成长股过度定价 |
| A2 成长外推反转（EPS 版） | 3 年 EPS CAGR 取负 | `fnd17_tcprgspe` ★冷门 | 同上，EPS 口径 |
| A3 成长加速度 | 营收同比的时序一阶差 | `fnd17_arevchg` | 增速二次加速 |
| A4 TTM vs 年更分歧 | 增速口径分歧 | `fnd17_ttmrevchg` vs `fnd17_arevchg` | 财报更新频率差 |
| B1 利润率改善 | 营业利润率当前 vs 上年 | `fnd17_tcpngmpoq` / `fnd17_tcpngmpoa` | 经营质量改善 |
| B2 净利率改善 | 净利率当前 vs 上年 | `fnd17_tcpngmpnq` / `fnd17_tcpngmpna` | 盈利能力提升 |
| B3 毛利率回归 | TTM 毛利率 vs 5 年均值 | `fnd17_8_ttmgrosmgn` / `fnd17_grosmgn5yr` | 利润率向均值回归 |
| B4 毛利率趋势 | 5 年毛利率增长率 | `fnd17_gmntrendgr` ★冷门 | 结构性改善 |
| C1 估值版本分歧 | 多版本 EV/EBITDA 之差 | `fnd17_ev2ebitda_cur` vs `fnd17_3_ev2ebitda_cur` | 数据供应商分歧 = 不确定性 |
| D1 盈利质量 | 净利率 TTM vs 5 年均值回归 | `fnd17_ngmpnmtt` / `fnd17_margin5yr` | 质量回归 |

⚠️ 全部模板必须**只用 fundamental17 单数据集字段**（ATOM 合规），且**禁止**引入 `close` / `returns` / `adv20` / `cap`。

---

## 8. 已排除的字段类型（本集画像中发现）

- 前瞻 / 标签类：本集**未发现**（与 fundamental67 的差别就在这里）—— 但仍须逐波复核；
- 语义不透明：本集**未发现**（与 fundamental22 的差别）—— 但 `fnd17_*` 中 `histrelpe` / `apennorm` 描述偏简略，属「只做探针」档；
- 覆盖不足：见 §6 第 5 条列出的 7 个低 cov 字段。
