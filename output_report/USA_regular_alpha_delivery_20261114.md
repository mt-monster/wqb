# USA Regular Alpha 挖掘交付报告 · 2026-11-14

> 战役：USA 未点亮塔挖掘（固定 USA，TOP3000/D1，ATOM 单数据集优先）。
> 纪律：只挖不提交；并发 2（每批 2 条）；PV/MODEL/OTHER 不做跨集组腿（本轮全部单集 ATOM）。
> 台账：`tracking/USA/runs/usa_campaign_ledger_20261114.md`；S0：`tracking/USA/reference/usa_s0_dataset_scan_20261114.md`。

## 1. 已完全验证（IS 全闸 + prod + **self-corr** 通过）—— **实际 3 颗**

> ⚠ **2026-11-15 更正**：下表 #2 `vRAn3xkG` **已作废**，见 §1.1。本节计 **3 颗**（#1/#3/#4）。

| # | alpha | 数据集（塔/倍数） | 核心字段 | 表达式 | S | F | 2Y | SUB | TO | prod |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | **bla2k0Jq** | `social_sent_score`（other /1.4） | `opinion_score_delta` | `tail(group_rank(ts_mean(vec_avg(opinion_score_delta),22), industry), lower=0.1, upper=0.9, newval=0)` | **1.80** | **1.25** | **1.63** | 0.90 | 0.144 | **0.5138** |
| 2 | ~~**vRAn3xkG**~~ ❌ | ~~`earnings_sent_matrix`~~ | ~~`sentiment_weighting_method1`~~ | 与 `A1xJdOmg` **表达式逐字相同**，后者 **2026-11-14 已提交、现 ACTIVE** ⇒ 本条是重跑，**self 0.9961 FAIL** | 1.97 | 1.09 | 2.18 | 1.01 | 0.093 | 0.5213→**0.9961** |
| 3 | **zqrgna91**（READY 收割） | `ai_equity_alpha`（model 塔，已点亮） | `buzz_intensity_score_2/11` 分歧 | `signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(buzz_intensity_score_2), vec_avg(buzz_intensity_score_11)), 252), 252), market), 5), 0.8)` | **2.67** | **1.66** | **1.68** | **1.47** | 0.158 | **0.6877** |
| 4 | **N1eLE1de**（READY 收割） | `ai_equity_alpha`（model 塔，已点亮） | `credit_risk_model_score_5/7` 分歧 | `ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(credit_risk_model_score_5), vec_avg(credit_risk_model_score_7)), 252), 252), subindustry), 5)` | **2.63** | **1.54** | **2.07** | **1.66** | 0.141 | **0.6916** |

设置：#1 = SUBINDUSTRY/decay3；#2 = **STATISTICAL**/decay1；#3/#4 = TOP2000/STATISTICAL/decay0。全部 trunc0.08/nanON/maxTradeOFF。
全部 `failed_ra_count=0`、invest_S/S ≥0.78、pyramids 单段（ATOM effective=1）。
#3/#4 是从本地 READY 队列收割的存量候选（2026-10-23 入队），本轮 **refresh 终验**：zqrgna91 0.6877 维持 ✓、N1eLE1de 0.6916 维持 ✓。
⚠ 另有 `YPMvZZvv`（READY，S1.79/F1.06/2Y1.68）：陈旧 prod 0.6958 → **refresh 后 0.9499 ✗**（14 天漂移 +0.25）⇒ 撞墙淘汰，**实证「prod 台账 5 天作废」**。
### 1.1 self-corr 终验结果（2026-11-15 晚，MCP 实测）与两处重复件陷阱

| alpha | self（本地，对 USA OS 池） | 池规模 | 判定 |
|---|---|---:|---|
| `bla2k0Jq` | **0.2094** | 141 / 147 | ✅ |
| `zqrgna91` | 0.2866 | — | ✅ |
| `N1eLE1de` | 0.2753 | — | ✅ |
| `vRAn3xkG` | **0.9961** | 141 / 147 | ❌ **与 ACTIVE `A1xJdOmg` 同表达式** |

**★ 陷阱一：同表达式的 IS 件在母件上线后必然失效。** `vRAn3xkG` 的 prod 由记录值 0.5213 变成
**0.9961**（不是漂移，是与已上线的 `A1xJdOmg` 完全重合 —— 两者表达式逐字相同）。
平台按文本去重只对同一批次有效，**跨批次的判重必须自己比对表达式文本**。
连带更正：**earnings 塔第 3 颗早已由 `A1xJdOmg`（11-14 提交、ACTIVE）点亮**，
此前"提交 vRAn3xkG 可使 earnings 达 3 颗"的结论作废。

**★ 陷阱二：`self-corr` 的 `pool_size` 必须做合理性核对。**
`6XdvLPd5` 曾返回 `pool_size=4 / full_os_pool_size=7`（同期 `2rAQ6mQN` 是 141/147）——
池子近乎空时算出的 0.3533 只是"与那 4 颗不相关"，**没有意义**。
判据：`full_os_pool_size` 显著低于同区常态（USA 约 146–147）⇒ 该 self 值**作废**。
事后正是靠 `compute_mutual_correlation` 才发现 `6XdvLPd5` 与 `zqrgna91` **0.9961**（同一因子），
故 `6XdvLPd5` 一并剔除。

提交需用户点名（本报告不含提交动作）。

## 2. IS 全闸但 prod 未过 / 待验（同机制变体与储备）

| alpha | 机制 | 指标 | prod | 状态 |
|---|---|---|---|---|
| E5Q0On6m | earnings 语气反转 @SUBIND/d1 | S1.74/F1.09/2Y2.28/SUB1.01 | **0.72 ✗** | 撞墙（差 0.02，3 对手）——被 #2 的 STATISTICAL 换档解决 |
| E5Q0Xx6P | 同上 @CROWDING/d1 | S1.67/F1.00/2Y1.99/SUB0.94 | 待测 | 中性化对比第三档 |
| O0WwQdAg / QP0rZnJr | method2 同骨架 | S1.79/1.14/2.24 与 1.67/1.04/2.05 | — | 同机制（一席），机制双验证 |
| 6Xd7A5V7（READY） | earningscall trade_when | S1.77/F1.01/2Y2.54/SUB0.91 | 未测 | 族地板 0.82，预计撞墙 |
| YPMvZZvv（READY） | analyst 目标价 | S1.79/F1.06/2Y1.68/SUB0.83 | 0.6958（stale 335h）/self 0.41 | 需 refresh 终验 |
| zqrgna91（READY） | ai_equity buzz 分歧 | S2.67/F1.66/2Y1.68/SUB1.47 | 0.6877（stale 335h）/self 0.29 | 需 refresh 终验 |
| N1eLE1de（READY） | ai_equity credit 分歧 | S2.63/F1.54/2Y2.07/SUB1.66 | 0.6916（stale 335h，余量 0.008）| 需 refresh 终验 |

## 3. 近闸但未过（存档 + 归因）

| alpha | 机制 | 缺口 |
|---|---|---|
| WjlK55nN | earnings 语气反转 126 窗 | S 1.33（2Y 1.26 改善但 S 不够）——S↔2Y 跷跷板 |
| gJa7lwPg / mLaeGd1x | insider 净买卖比（SUBIND/SECTOR） | S 1.11/1.20，2Y 1.04–1.27（S 天花板 ~1.2） |
| MP6lW1Rn / mLa23gM2 | social 观点变化 22d@d1 / 66d@d1 | 2Y 1.44 / S 1.41（跷跷板） |
| d5a8pzmg | social 观点变化 22d tail0.15/0.85 | 2Y 1.42（带宽 0.1/0.9 后为 bla2k0Jq 全过） |
| N1ewm5Jw（历史） | short_interest_pred | F 0.54 结构性（日更 TO 0.66） |

## 4. 判死清单（本轮实测证据）

| 对象 | 证据 | 结论 |
|---|---|---|
| risk70 三重 bucket 族（pwdAPALb/E56XvX90/akKqLq56） | prod 0.7541/0.7519/0.7034 | 全族撞墙（2026-10-28 产物），不再投 |
| earningscall 情绪族（P0od2pOp / 6Xd7A5V7） | prod 0.8192 / 0.7672 | 撞墙（历史地板 0.80–0.82 复证） |
| **YPMvZZvv**（READY，analyst 目标价） | 陈旧 prod 0.6958 → refresh **0.9499** | **14 天漂移 +0.25**，撞墙；「台账 5 天作废」实证 |
| news97（Seeking Alpha 情绪，105 字段） | 6 探针（5pos 反向/5neg 正向/2dts 分散度/SECTOR/22−66 变化量）max |S| 0.91 | 探针级判死（媒体情绪已套利） |
| ai_news_scores（transformer 新闻情绪） | pos 反向 −0.35 / neg 正向 0.51 | 探针级判死 |
| other623（TextBlob 极性） | 正反 0.17 / −0.24 | 探针级判死 |
| insider_matrix tail 迁移 | 净比 1.11→1.04；agg 0.43 | tail 不可迁移到流量型 |
| insider_agg_matrix | 6 臂 max |S| 0.50 | 弱（D15 压线） |
| institutions20 短卖占比 | 正向 −0.59 / 反向 0.85 | 强度不足（日频做空量=噪声，复证） |
| earnings_sent NTR / NEG 概率位 | −0.13 / −0.11 | 概率位无信号（信号在加权聚合口径） |
| earnings27 分析师邮件词频 | 正反 0.21 / 0.62 | 弱（cov 0.26） |
| earnings7 | 40 字段全为财季编码/EPS/股息金额，无 surprise 组件 | 无可用信号面，不投 |

**新闻媒体情绪闭环**：news97 / other623 / ai_news_scores 共 8 探针全灭（max |S| ≤0.51）
⇒ **管理层自述语气有效（earnings_sent_matrix）、媒体转述情绪无效**。

## 5. 可复用经验（已写入 skill `_usa-tail-extreme-2y-recipe-20261114.md`）

1. **tail 极值裁剪是 2Y 闸解药**（低换手慢信号族）：earnings 语气 2Y 1.03→2.28；方向依族而变（workforce 族相反），必须逐族实测。
2. **中性化换档是 prod 破壁器**：SUBINDUSTRY→STATISTICAL 使 earnings 语气族 **prod 0.72→0.52 且 S 1.74→1.97（+13%）**（USA 首个量化证据，推翻「STATISTICAL 只提 S」的旧印象）。
   ⚠ **但 STATISTICAL 伤 SUB 是普遍现象**：social 线 SUB 0.90→0.70（破闸）、risk70 SUB 0.99→0.69（破闸）⇒ **earnings_sent 是 SUB 幸存者（1.01）**，换档需逐族验 SUB 三闸。
   ⇒ **中性化最优逐族而异**：earnings→STATISTICAL；social→SUBINDUSTRY；risk70→CROWDING。
3. **带宽逐族相反**：earnings（稀疏事件）0.15/0.85 最优；social（日频高覆盖）0.1/0.9 最优。
4. **no-op 清单**：winsorize 外层、normalize 外层、truncation 0.08→0.04、densify(industry) 外层——逐位相同。
5. **信号指纹**：social 观点**变化量有效、水平无效**；earnings 语气**66 日长窗反转有效、22 日无效**；概率位无效。
6. **迁移边界**：tail 骨架只适合「慢累积 + 两端承载信息」型；流量/比率型（insider/institutions20）不可迁移。

## 6. 交付缺口与后续

- **目标 20 颗 vs 实交 4 颗全验证**。原因量化：本轮共 **13 颗 IS 全闸**（failed_ra=0），其中 **9 颗撞 prod 墙**
  （risk70×3: 0.75/0.75/0.70；earningscall×2: 0.82/0.77；earnings@SUBIND 0.72；earnings@CROWDING 0.73；YPMvZZvv 0.95；6Xd7A5V7 0.77），
  4 颗过线（0.51/0.52/0.69/0.69）。**USA prod 墙命中率 69%**，与历史「墙占 65–72%」一致。
- 剩余 16 颗的可行路径（按 ROI 排序）：
  1. **中性化换档重测存量**：本轮证明 STATISTICAL 可使 prod −0.20（earnings 族）；READY/历史候选里 prod 0.70–0.78 的族值得逐族三档重测；
  2. **每集一席 × 新数据集**：news/option/shortinterest 塔仍 0，但本轮已排除新闻情绪全族与日频做空量；
     剩余方向 = option 塔 vol surface（option6/9，拥挤度高）、shortinterest 塔月频口径（shortinterest43 未测）；
  3. **收割而非重挖**：本地 READY 队列本轮已收割 2 颗（zqrgna91/N1eLE1de），继续清队列比新开波便宜。
- self-corr 与最终提交由用户确认后执行（红线：只挖不提交）。self-corr 工具受 30s 客户端超时限制，
  需分批/预热缓存后补测。

---

## 7. 2026-11-15 增补：news 塔收口 + 收割池全量

### 7.1 news 塔：14 臂 / 3 集 / 12 结构互异模板 → F 闸结构性天花板（PROVISIONAL）

| 集（category=news） | 臂 | 最高 S | 最高 F | 备注 |
|---|---|---|---|---|
| `news48`（22 VECTOR） | 6 | **1.18**（注意力稀释反向） | 0.36 | 情绪 0.39 · 新颖度 0.99 · 覆盖度 0.85 · 分歧 0.66 · **稀释 1.18** |
| `event_return_model`（59 MATRIX，DL 预测） | 6 | 0.77（三期限集成） | **0.34** | 水平 0.72 ≫ 差分 0.15；跨期限分歧 −0.54→**+0.54**；invest ratio **1.234** |
| `news84`（23 MATRIX） | 2 | 0.65 | 0.31 | 异常覆盖度（aC 4）0.65 · 偏度 0.57 |

**判定依据是定量而非印象**：`F ≥ 1` 在 `TO≤0.125` 下等价于 `S×sqrt(ret) ≥ 0.3536`；
news 族最佳臂 `1.18×sqrt(0.0325)=0.213`（差 1.66 倍）、最佳 F 臂 `0.77×sqrt(0.0281)=0.129`（差 2.74 倍），
而交付对照 `1.97×sqrt(0.0383)=0.386` ✓。需 **S≈1.9–2.4** 才可能过闸，12 个模板最高仅 1.18。
⇒ **F 闸天花板，PROVISIONAL**（D2 字段族 6/22·6/59·2/23、D4 仅 1 分组轴、D6 仅 1 配置，按判死六维**不得**终判死，
也不得据此封 news 塔或作邻接集先验）。完整读数见 `tracking/USA/runs/usa_campaign_ledger_20261114.md` §13。

**三条可复用归因**：
1. **四闸同号负值 ⇒ 先 `reverse()` 再判死**。`58J92waN` S −0.54 / 2Y −0.55 / SUB −0.55 / invest −0.63，
   取反后 `omavk0Yn` **+0.54** 精确镜像 —— 那不是"弱"，是"符号反了"。
2. **模型输出类数据集：水平值 ≫ 变化量**（0.72 vs 0.15）。DL 已消化时序，再差分只放大噪声；与通用直觉相反。
3. **同模型内 ensemble 增益有限**（三 horizon 集成 0.77 vs 单 20d 0.72）：真正分散化要**换信息源**，不是同模型多字段平均。

### 7.2 收割池：38 条 IS 全闸干净的存量候选（零仿真配额）

`batch_submit_verdict --region USA --limit 40` 实测：**UNVERIFIABLE 38 / BLOCKED 2 / ERROR 0**。

Top（按 S 排序，`-` = prod 未测）：

| alpha | S | F | TO | 2Y | SUB | prod | 备注 |
|---|---|---|---|---|---|---|---|
| `Xg9WNRg8` | 4.74 | 4.10 | 0.166 | 5.46 | 2.90 | 0.6493 | SA 式 `generate_stats/self_corr` 组合权重式，非普通 regular alpha |
| `kqNb1g5d` | 3.32 | 3.29 | 0.173 | 3.65 | 1.76 | 0.6915 | board_gov vector_neut |
| `88R7JMxX` / `78L0meRx` | 3.43 | 3.02 | 0.250 | 3.69 | 1.72 | - | 同族（vector_neut 参数序互换），实质一颗 |
| `1YNl3p5R` | 2.61 | 2.38 | 0.134 | 2.83 | 2.00 | 0.6011 | SA 式组合同上 |
| `6XdvLPd5` | 2.65 | 1.63 | 0.161 | 2.13 | 1.43 | 0.6852 | ai_equity credit_risk + bucket 中性化 |
| `58EqmQEN` | 2.52 | 1.85 | 0.126 | 2.77 | 1.66 | 0.6192 | institutions20 |
| `QPvrZW7X` | 2.45 | 1.77 | 0.106 | 2.77 | 1.85 | **0.5289** | institutions20，**余量最厚** |
| `omEw8PNb` | 2.42 | 1.56 | 0.101 | 2.10 | 2.03 | 0.5745 | institutions20 |
| `2rAQ5G0N` | 2.40 | 2.04 | 0.213 | 2.59 | 1.04 | 0.6500 | insider_trx 22d−126d 差 |
| `KPJwQzex` | 2.28 | 1.45 | 0.090 | 2.26 | 1.92 | 0.5733 | institutions20 |
| `MP6l68aa` ①② | 2.20 | 1.28 | 0.064 | **3.17** | 1.22 | 0.6897 | insider_matrix 净比，**self 0.2955 已测** |
| …另 27 条 | 1.60–2.10 | 1.02–1.96 | | 1.65–3.65 | | 多未测 | 完整表见台账 §14 |

① `58J72oQN` 与 `MP6l68aa` 同表达式两写法，须去重。② prod 余量仅 0.0103，提交前必须 `check_correlation` 刷新。

**必须声明的三条口径**：
1. **这 38 条是既有存量**（波次 `usa_probe_20261115`，18:07 入队、18:26 统一重验），**不是本战役新挖**；
   本战役新增仍为 **4 颗**，两者不得混算。
2. **`UNVERIFIABLE` ≠ 可提交**：只代表模拟层 FAIL 0 + Failed-count 0，**prod/self 未确认**。
   多数 `prod` 为未测或龄期 250–400h（远超 48h 保鲜），prod 漂移实测 +0.25/14 天 ⇒ 提交前必须刷新。
3. **`submit_ready.gate='SUBMIT_LAYER_VERIFIED'` 不能当放行依据**：GET /alphas/{id}/submit 平台恒 404，
   该标签只说明"查过且拿到 404"。反例 `E56YX80G` 标签 VERIFIED 但实测 **BLOCKED**
   （`CONCENTRATED_WEIGHT` 0.1523 vs 0.1、`LOW_SUB_UNIVERSE_SHARPE` 1.36 vs 1.54）。同表 `towers` 列全为 `[]`，亦不可用。

### 7.3 ★ 闸清单纠错：`CONCENTRATED_WEIGHT` 必须常驻（不是新知识，是执行缺口）

限值 **0.1**（单票权重集中度），属 RA check 集、进 Failed-count 资格门。
⚠ **该闸在 `docs/experience/02_signal_patterns.md` §14 早已有完整破局手册**（论坛 66 赞 + KOR 实证），
本轮漏的是**我的开波闸清单**，不是知识缺口 —— 记录以免后人误当新发现。
`E56YX80G` 即反例（CW 0.1523/0.1 FAIL）。闸清单固定为 **S / F / 2Y / SUB / TO / CW / invest_S·S / prod / self**。
本轮交付 4 颗反查均 **FAIL 0**（`CONCENTRATED_WEIGHT` 因 20 分位 rank 天然分散而通过），交付完整性成立。

### 7.4 ★ 当前可交付清单：7 颗全量双向核验后剩 **6 颗**（2026-11-15 晚定稿）

单项闸（IS FAIL 0 + prod<0.70 + self<0.70 + CW）+ **篮内互相关 < 0.5** 双证：

| alpha | 数据集 | S | F | 2Y | SUB | TO | prod | self | 来源 |
|---|---|---|---|---|---|---|---|---|---|
| `bla2k0Jq` | social_sent_score 变化量 | 1.80 | 1.25 | 1.63 | 0.90 | 0.144 | **0.5138** | 0.2094 | 本战役 |
| `zqrgna91` | ai_equity buzz 分歧 | 2.67 | 1.66 | 1.68 | 1.47 | 0.158 | 0.6877 | 0.2866 | 本战役（收割） |
| `N1eLE1de` | ai_equity credit_risk 分歧 | 2.63 | 1.54 | 2.07 | 1.66 | 0.141 | 0.6916 | 0.2753 | 本战役（收割） |
| `MP6l68aa` | insider_matrix 净比 | 2.20 | 1.28 | **3.17** | 1.22 | **0.064** | 0.6897 | 0.2955 | 收割池 |
| `2rAQ6mQN` | insider_trx 22d−126d | 2.38 | 2.02 | 2.57 | 1.04 | 0.214 | **0.6415** | 0.2264 | 收割池 |
| `kqNb1g5d` | board_gov_stats | 3.32 | 3.29 | 3.65 | 1.76 | 0.173 | 0.6972 | 0.6835 | 收割池 |

**篮内互相关**（4 年 / 986 点）：最大对 `zqrgna91`↔`N1eLE1de` **0.4289**，其余 < 0.25；
`max_mutually_below_subset` = **6**（上表 6 颗全部互相 < 0.5，可整篮提交）。

⚠ **余量告警（提交前必须当次 refresh）**：`kqNb1g5d` prod 余量 **0.0028**、self 余量 0.0165；
`N1eLE1de` prod 余量 0.0084；`MP6l68aa` prod 余量 0.0103。

**剔除**：`vRAn3xkG`（与 ACTIVE `A1xJdOmg` 同表达式）、`6XdvLPd5`（与 `zqrgna91` 互相关 0.9961）、
`QPvrZW7X`（prod 0.9609 FAIL，陈旧台账记 0.5289）。
**institutions20 同族**（`KPJwQzex` 0.5733 / `omEw8PNb` 0.5745 / `58EqmQEN` 0.6192）共享同一空头因子，
`QPvrZW7X` 撞 0.96 后预计同命，**不再为它们耗相关性槽位**。

**口径**：本战役新增交付 = **3 颗**；收割池新增 = **3 颗**；合计 **6 颗**（目标 20，缺口 14）。

---

## 8. 2026-11-15 末轮增补：近十年闸 + 全池聚类（清单再收紧）

### 8.1 ★ `bla2k0Jq` 近十年闸未过（§7.5 第三道闸，此前一直漏跑）

`get_alpha_yearly_stats` 逐年实测：

| alpha | 有效年 | 逐年 `longCount>0 && shortCount>0 && pnl>0` | 结论 |
|---|---|---|---|
| **`bla2k0Jq`** | **6/10** | **2014–2017 四年 `lc=0 / sc=0 / pnl=0`（完全空仓）**，2018 才建仓 | ⚠️ **不建议作首选交付** |
| `zqrgna91` | 10/10 | 全正，逐年 S 1.64–4.21 | ✓ |
| `N1eLE1de` | 10/10 | 全正，逐年 S 1.07–4.29 | ✓ |
| `MP6l68aa` | 10/10 | 全正（2014 S 0.41 偏弱） | ✓ |
| `2rAQ6mQN` | 10/10 | 全正，但 2014 仅 76/91 持仓、S 0.03（覆盖极薄） | ✓ 带备注 |
| `kqNb1g5d` | 10/10 | 全正且强，逐年 S 0.99–5.52 | ✓ 最健康 |

**为什么平台 RA 闸全过却抓不到**：官方 9 项测试**不含覆盖年数**，且 Weight 测试从「alpha 开始建仓」起算、
Sharpe 排除零持仓日 ⇒ 空仓年既不稀释也不触发 FAIL（见 `docs/experience/02_signal_patterns.md` §4 空仓年前置）。
这正是 §7.5 把「近十年」单列为第三道闸的原因 —— **只看全期指标会把 6 年样本的 alpha 当 10 年优质候选**。
`bla2k0Jq` 的 S1.80/F1.25/2Y1.63 全部来自 2018–2023，OS 应按 1.3–1.6 打折预估。

⇒ **交付清单口径**：`bla2k0Jq` 降级为「备选（有效样本 6 年）」，
**首选 5 颗** = `zqrgna91` / `N1eLE1de` / `MP6l68aa` / `2rAQ6mQN` / `kqNb1g5d`。
本战役新增仍记 3 颗（其中 1 颗降级），收割池新增 3 颗。

### 8.2 ★★ 全池「一族一席」聚类：31 条 IS-clean 只剩 6 个独立新族

把剩余 31 条 `UNVERIFIABLE` 做 `compute_mutual_correlation`（4y / 986 点，阈值 0.5）：

| 互相关 | 组 |
|---|---|
| **1.000** | `88R7JMxX` ≡ `78L0meRx`（参数序互换） |
| **0.9982 / 0.9983 / 0.9694** | `2rAQ5G0N`≡`QPvqzKjX`；`akKq92aO`≡`N1eLE1de`(已交付)；`KPgYg8Nk`≡`MP6l68aa`(已交付) |
| 0.895 / 0.847 / 0.840 | `58EqmQEN`·`j2YdKN3Q`·`KPJwQzex`（institutions20 同族） |
| 0.734 / 0.621 / 0.588 | `ZYaweYl0`·`3q0YZPqg`·`mLaJ1Zq5`（earnings 语气反转族，与 ACTIVE `A1xJdOmg` 同骨架） |
| 0.762 / 0.658 · 0.835 · 0.719 · 0.532 | shortinterest 贷款利率族 · `E56YodoJ`/`6Xd3lqnL` · `0mYopJ7r`/`P0oe533W` · `QPvex8G5`/`mLokaQJ5` |

⇒ **行数 ≠ 候选数**。扣重复后，与已交付件独立的新增代表件仅 6 条：
`Xg9Ymw1b` / `YP1ww82o` / `58EqmQEN` / `MPYwqvLn` / `0mYopJ7r` / `QPvex8G5`。
**平台 prod 单并发槽消耗从 31 次降到 6 次（省 80%）**，方法已写入
`docs/experience/02_signal_patterns.md` §20。

### 8.3 新增代表件 prod 实测（两条已完成，全部 FAIL）

| alpha | prod 实测 | 判定 |
|---|---|---|
| `YP1ww82o` | **0.7754** | ❌ FAIL |
| `Xg9Ymw1b` | **0.9559** | ❌ FAIL（0.9–1.0 桶 n=1，与 `QPvrZW7X` 同形态） |
| `58EqmQEN` | 平台计算 inflight 未回值 | 待取；台账 0.6192 已 stale 359h，**不得判闸** |
| `MPYwqvLn` | 被并行会话 `corr:prod_backfill(E569ZE7L)` 占槽 | 待取；self 0.3292 PASS（池 141/147），近十年 10/10 有持仓但 2017 pnl 负 |
| `0mYopJ7r` / `QPvex8G5` | 未测 | 待下一轮 |

`Xg9Ymw1b` 的 `get_alpha_details` 侧证 IS 面完全干净（checks.fail=[]、**CW PASS**、
`pyramids.effective=1`、S2.04/F1.08/2Y2.14/SUB0.95/TO0.0721），仍被单个 prod alpha 打掉
⇒ **一族一席之后 prod 墙依然是主瓶颈**，收割池不是"捡钱"。

**结论**：本轮扩样没有增加可交付件；清单维持 §8.1 的**首选 5 颗 + 备选 1 颗**。

---

## 9. 2026-11-16 增补：`e7adKz7g` 全闸通过（第 7 颗，earnings 塔第 3 颗）

**构造**：`tail(group_rank(ts_mean(subtract(positive_sentiment_probability_3, negative_sentiment_probability_3), 66), subindustry), lower=0.15, upper=0.85, newval=0)`
设置：USA/TOP3000/D1/**SUBINDUSTRY**/decay1/trunc0.08/nanON/maxTradeOFF

| 闸 | 读数 | 判定 |
|---|---|---|
| IS FAIL / Failed RA / PPA | 0 / 0 / 0 | ✅ |
| S / F / TO | 1.72 / 1.00 / 0.0477 | ✅（F 恰在 1.0 线） |
| 2Y / SUB | 2.08 / 0.91（limit 0.748） | ✅ |
| 近十年 | 10/10 双边持仓，2016 单负年（−291,450） | ⚠️ 族级 regime |
| self / prod | **0.5496 / 0.6753** | ✅✅ |

**机制**：earnings 电话会概率三元组的**净语气**（POS−NEG，66 日均值 + industry→subindustry 组内排序 +
tail 0.15/0.85 修剪 + SUBINDUSTRY 中性化）。是 `method1/2` 聚合音调的**概率空间表示**，
且是本会话唯一推进塔位计数的件：**提交即点亮 USA/D1/EARNINGS 塔（2→3）**。

**三条可复用经验**（详见台账 §16）：
1. **SUB 缺口的有效杠杆 = 分组轴下移**：industry→subindustry（同中性化同字段）让 SUB 0.69→0.91；
   「提 S 抬 SUB 门槛（0.435×S）」的律意味着降 S 反而更容易过 SUB。
2. **概率三元组净语气（POS−NEG）> 回归型聚合音调（method1/2）**：S 1.95/1.72 vs 1.79/1.67。
3. **族级负年 regime**：三个不同字段表示在同一年（2016）全负 ⇒ 是数据性质不是单颗缺陷，
   交付报告须按「单负年」标注而非当缺陷。
