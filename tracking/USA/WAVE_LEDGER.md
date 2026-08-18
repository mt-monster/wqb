# USA 战役波次台账（WAVE_LEDGER）

> **用途**：每波回测的结论层。每波回收后追加一节；下一波开跑前**必须先读本台账「下一波决策」节**再设计批次。
> **SOP 锚点**：`.qoder/skills/wqb-concurrency` §8（五槽填槽模式）第 3.5/5 步；`docs/experience/project_experience_master.md` 第十一章。
> **机器伴生**：`tracking/USA/ledger.json`（判死清单/骨架登记/最佳候选，供门禁去重与脚本消费）。
> **流程偏差记录（2026-08-16）**：波3-6 曾把结论写入散件 `runs/usa_wave3_ledger.txt` 未并入本台账，已回填修正；散件保留为原始证据。自波7 起：台账写入是回收后的阻断步骤，未写台账不得提交下一波。

## 战役硬闸门（每波筛选统一口径）

sharpe>1.58 · fitness>1 · 2y sharpe>1.6 · margin>5bp · turnover 5%–30% · RN sharpe>1 · ra_failed_count=0 · **PROD 相关性 <0.7**
配置：region=USA / universe=TOP3000 / delay=1（波4 含 D0）/ max_trade=ON / REGULAR / FASTEXPR

## 累计计数

| 指标 | 值 | 更新时间 |
|---|---|---|
| 累计波次 | 10（波10 institutions6 精调中） | 2026-08-16 |
| 累计回测条数 | 波1-9 约 352 条 + 波10 已回收 64 条（WW~FINAL 7 批），0 ERROR 连坐 | 2026-08-16 |
| 白名单 | D1 scope 649 字段 / 11 数据集（institutions6 新增 21 字段） | 2026-08-16 |
| 主攻数据集 | institutions6（decay2+signed_power 解锁，精调中） | 2026-08-16 |
| 判死数据集 | sentiment21 · news_transformer_scores · sentiment22（情绪金字塔 3 数据集 88 条）· option8 · option40（option 金字塔 88+ 条 PROD 墙）· shortinterest3（PROD 墙）· analyst44（天花板 0.45 差 3.5 倍） | 2026-08-16 |
| 数值七闸门全过 | 17 条（波3）但 PROD 0.83-0.91 全灭，**提交候选仍为 0** | 2026-08-16 |
| 最佳候选 | 6XpL2qjP（2.19/PROD 墙）；活候选 ZYEVZQw0 1.03（inst6 share 复合 d2，tv 9.9%/margin 7.2bp 双达标，精调中） | 2026-08-16 |

---

## 波1（2026-08-16）— shortinterest3 · loan_utilization_ratio 骨架族

### 批次
| 批 | multisim id | 配置摘要 |
|---|---|---|
| A | QCAUm44P4QN9WkzEip8jV9 | decay4 / SUBINDUSTRY 中性化 |
| B | UJtgA7Tw4DNb4W1sy9yVhY | loan_utilization_ratio 变体 |
| C | 2ClRKxecA59Ra3i1PNwRlfv | decay8 |
| D | 2IoAs4gI4It9vz18RyPujWe | INDUSTRY 中性化 |
| E | 1FivjA9RB5fa9CwAikOTmcS | 收尾变体 |

### 回测结论
- **最佳**：`kqP6JGkK` = `quantile(signed_power(group_zscore(ts_av_diff(vec_avg(loan_utilization_ratio), 10), subindustry), 0.5))` decay4 —— sharpe 1.39 / 2y 2.62 / RN 1.56 / tv 28.9% / margin 2.6bp（差 sharpe 与 margin 两项）
- **新骨架发现**：`A1G8Vpaw` = `reverse(quantile(ts_decay_linear(vec_avg(max_loan_rate), 10)))` decay4 —— sharpe 1.18 / **fitness 0.93** / tv 10.8% / **margin 14.4bp** / 2y 1.69 / RN 1.21 → **过 4/5 闸门，仅差 sharpe**，成为主攻骨架
- **备选**：`pwNevZQv` = borrow_activity 反转 decay8 —— margin 17bp / tv 9% / sharpe 0.92（低相关风格备选）
- 结构性发现：① shortinterest3 该骨架族 sharpe 上限约 1.39；② decay 4→8→12：sharpe 递减但 margin 递增（decay 是 margin/turnover 杠杆，不是 sharpe 杠杆）；③ INDUSTRY ≈ SUBINDUSTRY 中性化差异可忽略

### 多样性快照
- 本波算子集中在 quantile/group_zscore/ts_av_diff/signed_power/reverse/ts_decay_linear/vec_avg；字段族 = loan_utilization_ratio + max_loan_rate + borrow_activity
- 未探索：费率字段族（mean/min_loan_rate、loan_rate_volatility）、duration/count 类字段

### 下一波决策（波2 已消费）→ 已消费，波2 执行完毕
- 主攻 max_loan_rate 骨架精调 + 费率字段族首攻 + shortinterest3 收尾组合
- sentiment21 给最后一轮机会（decay=21 压换手）
- decay 继续向 8/12 探（margin 杠杆）

---

## 波2（2026-08-16）— shortinterest3 收尾 + sentiment21 终审

### 批次
| 批 | multisim id | 配置摘要 |
|---|---|---|
| F | VoSj1b4U4ZSbyXzsGCCSlW | 费率字段族（mean/min_loan_rate 等）decay4 |
| G | 3Io2Xd6Xm56o9OAqyVk0fEi | shortinterest3 组合骨架 decay4 |
| H | 3lz5tQ8QT4J28Wxv4CMaZ4N | sentiment21 decay21 |
| I | 1lDkGXfHb4y89aT7zE1e5y9 | shortinterest3 decay12 |
| J | 2qGMOGeeg56wbBbS2TP9t6R | sentiment21 decay21 |

### 回测结论
- **最佳**：`N1blNZae` —— decay12 quantile 骨架，sharpe 1.30（再次确认 sharpe 上限 ~1.3-1.4 区间）
- **sentiment21 判死**：decay=21 仍全灭，换手 >100%，日频全量刷新结构性不适合 D1/TOP3000。两波 16 条（decay 4 与 21）零存活 → 满足判死证据标准，写入 ledger.json
- shortinterest3 收尾结论：loan_utilization_ratio 骨架族已探至 sharpe ~1.39 上限；decay12 margin 继续提升但 sharpe 进一步走低 → 该族停止追加变体
- A1G8Vpaw（max_loan_rate 骨架）维持主攻：全场唯一过 4 闸门者

### 多样性快照
- 新增探索：费率字段族、decay12、decay21；骨架多样性仍偏 quantile 单系（⚠️ 风险：风格同质）
- 累计字段探索 ≈ shortinterest3 白名单 31 字段中 15 个左右，sentiment21 全量判死

### 下一波决策（波3 待执行）
1. **主攻**：max_loan_rate 骨架精调（围绕 A1G8Vpaw：窗口 5/14/21、decay 8/12、group_zscore/signed_power/ts_av_diff 变体），目标 sharpe 1.18→1.58
2. **第二数据集首攻**：候选 option8（OS sharpe 0.525，STATISTICAL 中性化 0.641）与 institutions4（OS 0.542）；需先 `get_datafields` 取字段并入 `data/fields_gate.json` 白名单（上次调用被取消，未完成）
3. **禁发**：sentiment21 任何表达式；loan_utilization_ratio 骨架族追加变体（边际≈0）
4. **风格补盲**：至少 1 批非 quantile 系骨架（如 rank 直出 / 中性化差值 / hump 模板），对抗风格同质化

---

## 波3（2026-08-16）— option8 首攻 + si3 精调（批 K-S，即收即补至 T-W，共 104 条）

### 批次
K/L = si3 max_loan_rate 精调/费率收尾；M/N/O = option8 低波异象/IV-RV价差/skew期限结构；即收即补 P/Q/R/S（option8 二轮、si3 剩余字段、put/call 精调）；T/U/V/W（put/call d8/d12、si3 新结构、SECTOR）。白名单扩至 195 字段（option8 64 字段新登记）。

### 回测结论
- **e73ZEoNz** = `reverse(quantile(divide(implied_volatility_put_30, implied_volatility_call_30)))` SUB/d4 —— sharpe 2.06/2y 2.74/RN 1.69/fit 0.95，仅差 tv 32.7% 与 margin 4.2bp → 触发 put/call 比率族主攻
- **终轮筛选（104 条）：17 条七闸门数值全过**，唯一 RA 失败项均 LOW_SUB_UNIVERSE_SHARPE；冠军 `6XpL2qjP` 2.19/fit 1.11/2y 2.62/tv 26.2%/5.2bp/RN 1.69 d8 SUBIND（yearly 10/10 全正，self-corr 0.39）
- **PROD 首检露墙**：6XpL2qjP 0.8299 FAIL；rK2Mnjom 0.8847；si3 3qpvJwVN 0.957（si3 结构性墙同步确认）
- 无效方向实证：IV-RV spread 全灭、skew 全灭、低波异象方向反转无效、hump(0.33/0.17) 变体失效

### 下一波决策（已消费）
PROD 突围：option8 D0 低竞争区（userCount 11-744，D1 的 ~1/50）+ tenor 错位 + ts_* 时序变形。

---

## 波4（2026-08-16）— option8 PROD 突围终判（批 X/Y/Z/AA/BB，40 条）

### 回测结论
- 数值闸门过 20 条：2rpooMZ5 2.19（D0 冠军）/ gJ8VVAPe 2.17 / MPGNNO56 2.17 / 88pxxb5X 2.15…
- AA tenor 错位全灭（最高 1.39）；BB ts_* 变形全灭（<0.87）；Z 批跨 tenor 组合 O0GXXq6J 2.14 仍属拥挤族
- **PROD 普检定案**：2rpooMZ5 0.8648 / gJ8VVAPe 0.8329 / MPGNNO56 0.8688 / ZYEvv6ex 0.8554 / RRmww3ad 0.8611 / j26KMdxk 0.8693 / P0GmA71W 0.9051
- **option8 put/call IV 比率族判死（结构性墙）**：PROD 0.83-0.91 全骨架超标，与 delay/中性化/骨架/decay 无关；优化器已穷尽参数层（d4/8/12）+字段族（pc10~360/skew/复合）+骨架层（5 种）+D0 低竞争区。详见经验主文档附录 C

### 第 10 轮边界多样性评估（波1-4，约 19 轮回测）
- 字段探索率：option8 24/64=38%，si3 约 30%
- 骨架：quantile+group_zscore/signed_power/group_rank/ts_decay_linear/composite/hump（失效）共 7 种
- **风格：全部波动率相对价值单一风格 → 风格多样性严重不足，必须转新风格数据集**
- 失效风险：拥挤信号族 PROD 墙（si3 0.957 / option8 0.83+）；低波异象/skew/IV-RV 实证无效
- **转向决策**：news（金字塔=0）/socialmedia（=0），事件驱动/情绪风格与波动率风格天然低相关（相关性<0.4 目标友好）

---

## 波5（2026-08-16）— news_transformer_scores 首攻（批 CC-JJ，56+8 条）

### 回测结论
- 情绪反转（contrarian）方向实证有效：XgoAZb38 0.82 / qMNJ2xE1 0.91 / vRNX7rra 0.89；正向做多净情绪全负（-0.55~-0.87）
- **致命问题**：换手率 100%+（新闻字段日变剧烈），decay4/8 压不住；ts_decay(20/30) 在 quantile 后仅微降；ts_mean(20) 能压至 13% 但信号衰减（78zR577L 0.66）
- 信号天花板：9qpO5lor 1.03（neutral typical）；反转族 0.77-0.91 → **情绪水平族信号强度不足（上限~1.0）**
- 假字段实证：negative_sentiment_mean_score_12 不存在（ERROR），已修复为 peak_score_12 → 白名单登记必须逐字段核对
- 白名单扩至 510 字段；JJ 复合批（多窗口+decay15/20）留作交叉验证

### 下一波决策（已消费）
转 sentiment22（新闻金字塔第 2 数据集）：210 字段 MATRIX cov≈1.0、userCount 0-12 极低竞争、日度聚合比 transformer 平滑。

---

## 波6（2026-08-16）— sentiment22（批 KK/LL，16 条）

### 批次
KK = 3iOTWOcN94vAabS15JGXm9BX（反转族 _253/_5 系，SUBIND d8）；LL = 4epeb3wz4yU8IpliLfJazu（变体 2/3+比率/平滑，INDUSTRY d8）。白名单新增 12 字段（D1 scope 522 字段 / 7 数据集）。

### 回测结论（2026-08-16 回收，PASS=0）
- **KK/LL（snt22 16 条中 8 条）全灭**：sharpe 全部 ≤0.41 且多数为负（MPGNrwza -0.51、1YpAMvP6 -0.59）；换手 92.8%-123.3%，换手困境与波5 预测完全一致地重演
- JJ news 复合批最佳 O0GXLggp 0.87（tv 99.1%/margin 1.7bp），仍远低于闸门；复合+decay15/20 未能突破 news 系~1.0 天花板
- 闸门评估见 `_parse_jj_kk.py`（matched 16/24，PASS=0）

### 追加回收（MM 批，情绪金字塔终判）
- MM = usa_snt22_batch_mm.txt（正向多高负面情绪）：最强 9qpOnWzq 0.66/tv 107%，全部 ra_failed；KK reverse(neg) 全负（方向与 transformer 相反），LL 全灭（最高 0.13）
- **★情绪金字塔终判：3 数据集（transformer/snt22，snt23 未测）88 条 PASS=0**，信号天花板~1.0 远低于 1.58，换手困境无解；论坛求证：「Slowly Incorporated News」ts_zscore 模板上限仅 1.10，ASI 帖条件化骨架只降 PROD 不救弱信号 → 满足切换纪律，转向新金字塔

### 下一波决策（波7 已消费）
1. sentiment22 裸反转族已证伪；若继续攻 news/snt22，**必须先套 ts_decay_linear(20+)/ts_mean 强平滑**再回测（波5 已证 ts_mean(20) 能压换手至 13% 但信号衰减，需测更长窗口/复合平滑），否则停止追加该风格变体
2. 禁发：sentiment21 任何表达式；option8 put/call IV 比率族；si3 拥挤骨架族（PROD 墙）；snt22/news 裸反转族（无平滑，边际≈0）——**例外**：下方「论坛模板采用审计」节的翻案批 NN（8 条，已过四重门禁）作为一次性证据链闭环允许执行，结果回写后该例外即失效
3. 风格约束：情绪/事件风格仍是唯一合规方向；若强平滑后仍封顶~1.0，转 socialmedia 金字塔或查论坛求助（满足切换纪律：模板多样性穷尽+论坛无计可施后再换）
4. 提交前置：任何数值七闸门全过的候选必须先过 PROD<0.7 再进 robust/过拟合测试（波3-4 教训：17 条全过仍全灭）

---

## 波7（2026-08-16，PP/QQ 在飞）— option40 蓝海首攻

### 批次
选集依据：recommend_datasets + userCount<1000 + quality_score → 命中 option40（703 用户/2540 alpha，乘数 1.3，未点亮 option 金字塔）；新登记 19 字段。风格：IV 低波异象/期限结构/IV-HV 价差/skew/Greeks，与情绪、option8 put-call 完全不同。
NN = 3uLGkq3GU5k4bLl6MfNwwjs（IV 族 8 骨架，SUBIND d5）；OO = 1533GbenS59t8BGzPzUkvB5（差异骨架，INDUSTRY d8）；即收即补 PP = 4crexdcXh4Tlb2B15w1WiPEo（skew 反向+期限强化，SUBIND d5）、QQ = 1KKwmse0r4wnbD5f1ol5Phr（skew 长 tenor 60/90/150，MARKET d6）、RR（见追加批节）。门禁全过。

### 回测结论（NN/OO 16 条已回收）
- **冠军 VkGQvdOw 1.06**（-ivcall10/ivcall360 期限结构倒挂，tv 8.4%✅，RN 0.90）
- **强信号方向实证**：E5GnZVk9 skew(put-call)/ivmean = -1.66/fit -1.06/tv 9.6% → 反向(call-put)待验（PP/QQ 在攻）
- IV 水平族弱（±0.3）；theta/gamma 无效；ts_delta(IV) 上行 -0.61 方向确认
- **结论：opt40 skew+期限结构族信号未封顶，换手/保证金全过，值得深挖**

### 追加回收（PP/QQ/RR，24 条 → option40 PROD 墙定案）
- **PP/QQ 数值冠军**：O0Gd05Ng 1.88 / 78zP8Ko2 1.84 / 3qpmqn9N 1.6x（30d skew 族），全部 RN 过、tv 6-10%✅、margin 11-17bp✅
- **PROD 普检**：O0Gd05Ng 0.8306 / 3qpmqn9N 0.8369 / 78zP8Ko2 null / VkGQ1LK5 0.8787（120d skew）/ VkGQvdOw 0.9018（期限结构）→ **全部超标**
- **RR 长 tenor 强化**（group_zscore/ts_rank/504 窗口）：VkGQ1LK5 1.61 / wpa7KAVd 1.58 / j26k2joo 1.58，但 sub_universe_sharpe 仅 0.22-0.59 全 RA failed；IV-HV 价差 0.6、days_from_last_change -1.16 无效
- **★定案：option40 IV 衍生族（水平/skew/期限结构）PROD 0.83-0.90 结构性墙，与 option8 同构**；蓝海 userCount 低不保证 PROD 低（信号经济含义拥挤）

### 终审回收（翻案批 + SS 标准曲面，16 条 → option 类金字塔整体判死）
- **翻案批**（1ucdKHbeH4uicmWlIcznlaO，8 条）：ts_target_tvr_decay 语法修复（命名参数 lambda_min/lambda_max/target_tvr）后运行成功；wpa7q0JY 1.53/fit 1.03/tv 4.8%/m 23.6bp/RN 1.25、QPGRMw2M 1.52/fit 1.02/tv 6.0%/m 18.8bp/RN 1.32 —— **sharpe 差 0.05 且 subU 0.24-0.28 仍 RA failed**；残差差分全部无效（-0.34~0.4）；vec_max 1.13-1.18 不足
- **SS 标准曲面 Greeks**（I9IWveYx5gl94KtCdAr1aX，8 条）：theta/vega/gamma/delta 结构信号全灭（最高 0.18）
- **★option 类金字塔判死（两数据集 88+ 条）**：IV 衍生族 PROD 墙 0.83-0.91 + subU 结构性低（信号与平台重叠）+ 三武器（tvr_decay/残差差分/vec_max）无法解封；标准曲面 Greeks 弱信号 → 证据链闭环，翻案批例外失效，option8/si3/option40 永久封存
- 教训：蓝海 userCount 不保证 PROD 低；sub_universe_sharpe 是 PROD 墙的先行指标（低 subU ⇒ 必高 PROD）

### 追加批（RR，在飞，14:25 提交前登记）
RR = `usa_opt40_batch_rr.txt`（8 条）：opt40 skew 反向(call-put)/ivmean 长窗口变体——ts_decay_linear(21) 强平滑 + group_zscore/group_rank/ts_rank(504)，含 put/call 波动率差(273d)。multisim id 待提交后回填。

### 下一波决策（波8 已消费）
1. ✅ 翻案批/SS 已回收：option 类金字塔整体判死（证据链闭环）
2. **波9 方向：新金字塔 + 非价格/非波动率信号**。候选：macro38 已拉字段（但技术指标 userCount 60-420 属拥挤，弃）；优先 analyst 预期类/事件类/资金流类蓝海数据集（userCount<300 + 金字塔未点亮 + 风格与价格动量低相关）
3. 禁发：情绪族任何数据集、option8/option40/si3 IV 族、group_vector_neut/hump、snt22/news 裸反转族
4. 提交前置：数值七闸门全过 → PROD<0.7 → robust/过拟合（顺序不可颠倒）

---

## 论坛模板采用审计 + PROD 墙翻案批（2026-08-16，波7 待执行）

### 审计结论（论坛经验文档 vs 全部批次表达式 grep 核对）
| 论坛模板 | 出处 | 战役采用情况 |
|---|---|---|
| ts_zscore 算子（时序标准化包裹） | 帖3/帖6 | ✅ 已用 17 处（批 f/h/i/m/p/q/r/s/s1/s4/bb） |
| **残差差分模板** `ts_zscore(A,63) - ts_zscore(group_neutralize(A,sector),63)` | 帖3 高出货量通用模板 | ❌ 0 次落地（group_neutralize 仅 4 处且全在 hump 实验内） |
| **ts_target_tvr_decay**（帖8 实测 prod corr 0.90→0.77） | 帖8 | ❌ 0 次落地 |
| **vec_avg→vec_max** 换聚合（实测 PC 0.7288→0.6967） | 论坛降PC实战 | ❌ 0 次落地 |

### 判死证据链缺口
option8/si3 有 17 条数值七闸门全过但 PROD 0.83-0.91 判死，依据是中性化/decay/窗口/delay 穷尽；但论坛救援工具箱中降幅最大的三武器（ts_target_tvr_decay/残差差分/vec_max）均未实测 → **判死证据不充分，设一次性翻案批**。

### 翻案批 NN（已过四重门禁，待提交）
文件：`runs/usa_prodwall_retrial_batch_nn.txt`（8 条：option8 put/call 比率 ts_target_tvr_decay×2 + 残差差分×2；si3 max_loan_rate ts_target_tvr_decay vec_avg/vec_max×2 + loan_utilization_ratio 残差差分×2）。
**翻案判定规则**：任一武器使 PROD<0.7 且数值闸门保持 → 该数据集解封、武器入主攻工具箱；三武器全灭（PROD 仍>0.7 或数值闸门崩）→ 维持判死，证据链闭环封存。结果必须回写本节 + ledger.json。

---

## 波9（2026-08-16）— analyst44（Integrated Broker Estimates）首攻

### 批次
选集依据：recommend_datasets（score 83.89 / dataset_usage 6.67 低竞争）+ analyst 金字塔未点亮（乘数 1.2）+ 风格与已判死的波动率/情绪/借贷完全独立。新登记 37 字段（EPS/EBITDA/ROE/ROA/Sales 等 BEst 共识值，coverage 0.87-0.98，userCount 4-36 极蓝海）。
- TT = 3JJ7of9NN4oC9OVX7kcKYS8（修正动量 8 骨架，SUBINDUSTRY/d8）
- UU = RsPDYc9c4HL94jeI1TetV4（多指标修正 + group_rank/ts_zscore 骨架，INDUSTRY/d12）
- VV = 1JWSfb27e55fbW3ArHOxIuc（修正率/加速度/强平滑，MARKET/d4）

### 回测结论（24 条已回收，PASS=0 → 判死）
- **全灭**：sharpe 最高 0.45（WjArQLLd 63d 修正 / LLGoaMom 126d / 58pK0Emo nxt 63d 平滑），21d 修正仅 0.06-0.11，增长修正 -0.33、加速度 -0.55、修正率 ≈0
- **结构性结论**：① consensus 共识值日变稀疏，21d 修正多数为 0 → 信号含量不足；② RN 全部为负（-0.18~-0.65）→ 共识修正与行业中性收益结构不匹配；③ turnover 2.5-12% 低（符合共识低频特性）但无信号；④ 3 中性化 × 3 decay 全灭 → 非配置问题
- **★analyst44 判死：consensus 修正类信号天花板 ~0.45**，距闸门 1.58 差 3.5 倍；earnings yield（EPS/close）需引入 63282 用户拥挤价格字段且破坏单数据集纪律，放弃

### 下一波决策（波10）
1. 切换 institutions6（Institutions and Beneficial Stake Ownership，679 用户/3155 alpha，pyramid 1.0）——机构持股/资金流风格，与全部已判死风格独立
2. 禁发：analyst44 consensus 修正/水平/增长任何表达式；option8/option40/si3 IV 族；情绪族；snt22/news 裸反转
3. 提交前置不变：数值七闸门 → PROD<0.7 → robust/过拟合

---

## 波10（2026-08-16）— institutions6（Institutions and Beneficial Stake Ownership）

### 批次
选集依据：机构持股/资金流风格与全部已判死风格独立（679 用户/3155 alpha，pyramid 1.0）；新登记 21 字段（13F 持股/买卖量，MATRIX cov 1.0）。
- WW/XX/YY = 3 批 24 条（reverse 买入占比/净买家/时变，SUBIND/INDUSTRY d4-8）——最强单信号 VkGQgZ95（reverse quantity 买入占比 0.95/2y 2.05/RN 0.65）但 margin 0.9bp/subU 0.3 fail
- ZZ/Z2/Z3 = 3 批 24 条（decay 8/12/16 阶梯，SUBIND）——sharpe 天花板 ~1.00（rK2am328/KPGAaAvz share ownership−quantity 复合）；fitness 天花板 0.60（e73MJpzp value ownership−count 复合，margin 4.16bp 近达标但 tv 2.35%<5%）
- STAT = 1zNNx8eb54VtaEnd1A3zQQA（8 条，STATISTICAL 中性化终验）——**无解锁**：count 复合 0.96→0.42 大幅受损、share 复合 1.00→0.88；唯一亮点 reverse 净买家 vRN70RQw margin 7.1bp/2y 2.41（sharpe 0.70）
- FINAL = VvXiPbyQ4oBakcckRQOiMQ（8 条，decay2 + signed_power/market_value/num 口径终验）

### 回测结论（截至 FINAL 批，64 条 PASS=0）
- **★结构性矛盾破解**：share 复合在 d8-16 时 tv 8.6%✅但 margin 仅 1.0-3.8bp✗（count/quantity 二选一）；**d2+signed_power 后 tv 9.9%✅ + margin 7.2bp✅ 双达标**（ZYEVZQw0 = signed_power(share−quantity买入占比, 0.5) d2：sharpe 1.03 / fit 0.55 / 2y 2.01 / RN 0.65 / subU 0.37 差限值 0.08）——此前"margin-tv 结构性矛盾"结论仅在 decay≥8 区间成立，**decay2 打开新维度**
- 新天花板：sharpe 1.03（ZYEVZQw0）/ fitness 0.59（mL5nOo22 signed_power value−count d2，margin 28.4bp/subU 0.53✅ 但 tv 3.42% 仍 <5%）
- 弱信号实证：count 占比 direct（0.43）、market_value 占比 reverse（0.79，2y 1.30 差）、inst6_value−market_value 复合（0.83，2y 1.39 差）
- 未达 3 倍判死线（1.58/1.03 = 1.53 倍）+ 出现解锁维度 → **不能判死，进入精调**

### 下一波决策（波10b 精调）
1. **主攻**：ZYEVZQw0 骨架精调——signed_power 指数（0.3/0.7/1.5/2.0）× share/value 水平 × quantity/count/market_value 买入占比 × decay2/1；目标 sharpe 1.03→1.58
2. 禁发：analyst44/option/sentiment/si3 全系；institutions6 count 占比 direct 族（0.43 弱）
3. 提交前置不变：数值七闸门 → PROD<0.7 → robust/过拟合


### 精调批回收（TUNE/T1/T2，24 条，累计 96 条 PASS=0）
- **TUNE = 1CcZ1TgWQ4CvbxeuU6tPqmJ**（8 条，signed_power 指数矩阵 0.3/0.5/0.7/1.5/2.0）：**5 档指数指标完全相同（1.03/0.55/9.9%/7.2bp/2y 2.01）——signed_power 是单调变换，被外层 quantile 完全抵消**；真正解锁变量是 decay2，指数维度实测无效
- **T1 = aInFTd2m54Zc2eEvZbZar0**（8 条，TOP3000/decay1：share 复合 × SUBIND/INDUSTRY、num reverse、value 复合、share−count、双水平复合、count 差 reverse）：sharpe 0.70-1.04，**margin 全崩回 0.0-0.1bp**（d2 时 7.2bp）→ decay1 是负贡献，decay2 为 margin 唯一解锁点
- **T2 = 1RYSQiaC4ZkaVhWBp8euRD**（8 条，TOP1000/decay2 核心骨架 8 条）：sharpe 0.03-0.55、margin 0.0-0.1bp 全灭 → **TOP1000 universe 对 institutions6 负贡献**（机构信号在 TOP1000 上无边际）

### ★institutions6 判死定案（96 条 PASS=0，维度全穷尽）
1. 已穷尽配置矩阵：**4 中性化（SUBIND/INDUSTRY/STATISTICAL）× 7 decay 档（1/2/4-16）× 2 universe（TOP3000/TOP1000）× 21 字段全口径（share/value/quantity/count/num/market_value）× 全骨架（水平/占比/差值/净买家/双水平复合）× signed_power 指数（实测无效）**
2. 天花板：sharpe 1.03（ZYEVZQw0）/ fitness 0.59（mL5nOo22）/ subU 0.53，距闸门 1.58 差 1.53 倍；虽未达 3 倍结构性线，但**配置空间已数学穷尽 + 论坛求证无新招（仅数据集知识帖/工具帖）** → 按"模板多样性已穷尽且无计可施"条款判死
3. 核心教训：① decay2 是 margin/tv 双解锁点，但 sharpe 天花板由 13F 低频信息含量决定；② 单调变换（signed_power 等）在 quantile 外层完全失效；③ TOP1000 无增量
4. **禁发**：institutions6 任何表达式（share/value/quantity/count/num/market_value 全口径）

### 下一波决策（波11）：切换 order_book_imbalance
1. **数据集**：order_book_imbalance（imbalance 金字塔唯一数据集，24 用户/198 字段/42 alpha/pyr 1.4，极蓝海）——订单流失衡微结构风格，与全部已判死风格（情绪/期权/借贷/分析师/机构持股）独立；198 字段全 VECTOR 型
2. **前置**：198 字段登记 fields_gate.json（VECTOR 型需 vec_* 聚合包裹，注意 GROUP 位门禁）；imbalance 类骨架（净失衡/多档失衡）首发探针批
3. 禁发延续：analyst44/option/sentiment/si3/institutions6 全系
4. 提交前置不变：数值七闸门 → PROD<0.7 → robust/过拟合

---

---

## 波11（2026-08-16）— order_book_imbalance 探针 + 双数据集混合（AA~AJ 十批 80 条，AK 在途）

### 批次与结论
| 批 | multisim | 内容 | 结论 |
|---|---|---|---|
| AA | 4pwNeBd3o50N8NE5zZF7Bmt | imbalance 占比/auction/spread 族探针 | 全灭：占比族 |sharpe|≤0.7 且 tv 35-62% 超高；spread 负向 -0.61（流动性溢价方向）；executed 占比 RN 1.03 但 IS 0.15 |
| AB | tN7zj3pP5bNamIxi0o0123 | 慢变字段族（twa 深度/fill_prob/rest_time/dark-lit/impact/spread ts_mean5） | **dark/lit 暗池占比发现 0mpZQ0A6：0.51/RN 1.44/RN fit 0.68/tv 11.7%/2y -0.59**；fill_prob 族 RN 1.17-1.18 但 2y -1.21 负；market impact 单独 0.24 |
| AC | 4uiSlDcoH4my9aYaiTKsD2J | market impact 精调（原始/ts_decay4/16/reverse/减 spread/加权/乘 spread） | **impact−mean_relative_spread 净效应 VkGQl72G：0.60/tv 5.8%/RN 0.64 为波11 单信号最强**；children 核对修正认知（0mpZQ0A6 实为 dark/lit，非 impact） |
| AD | 2dT7dn3u04V2bt4ymZHQwqv | dark/lit 精调（ts_decay4/16/reverse/count/notional 口径/nonaddressable）+ impact/spread 变体 | 全灭：**dark/lit 族天花板 0.51 确认**（decay4/16 降至 0.43-0.48，count 口径 -0.66 反向、notional -0.40 弱，仅 volume 口径有效）；impact−time_weighted_spread 0.18 弱；impact/spread 比值 0.57 未超差值 |
| AE | 4GB7Nddfu4vxa7m81oG5V3D | 双亮点复合（add/multiply）+ 未测字段族（auction dislocation/intraday vol/VWAP spread/修改强度） | **复合正反馈首次出现：dark/lit × (impact−spread) 乘法 0.66/RN 1.29/tv 8.6%（波11 新高）**，加法 0.63；其余字段族全灭（auction dislocation -0.57、vol -0.01、VWAP spread 0.10） |
| AF | 2lXu7g47G4VGaYFdGcYKfyU | 三重复合（×fill_prob/×executed）+ 权重变体（2×impact−spread）+ 差异信号 + spread 动量 | **vRN7eLab（dark×impact×executed 三成员）0.71/RN 1.63/RN fit 0.85/tv 12.3%**，RN 闸门已过但 IS 0.71 差；2×impact−spread 权重变体 0.57 |
| AG | 3aXpmIbcV54q9DtrmdLazRO | ★双数据集混合首发（obim×analyst44 8 条，decay8/SUBIND） | **混合放大实证：O0GdnYJ1（EPS 63d 修正 + dark/lit 加法）=0.81 波11 新高（+59% vs 单信号 0.51/0.45）**，乘法 0.80；earnings yield 类（需 close 价格字段）未测 |
| AH | 44qsMC8MP550bOHoYKU3Z4c | 混合精调1（21d/差异/executed 三成员/ask 方向，decay8） | 全灭：21d 0.71 < 42/63d；差异信号破坏（-0.32）；executed 三成员反降（0.76）；**EBITDA 63d 与 EPS 63d 指标完全相同（0.81）——consensus 各指标高度冗余** |
| AI | 2LgXfbads4BAbevToKgUigM | 混合精调2（decay4 + 窗口扫描 21/42/63/84/126d + adv20 归一化） | **★波11 冠军 QPGRE2RM（EPS 42d 修正 + dark/lit）=0.88/fit 0.44/tv 15.0%/cluster 0.81/RN 0.85/2y -0.08**；窗口 42d 最优（21d=0.71 < 42d=0.88 > 63d=0.81 > 84d=0.71 > 126d=0.68）；adv20 口径全弱（-0.19/-0.41） |
| AJ | 29tszl13X4oH9V41ObOonbp | 混合精调3（decay16 慢变 + impact−spread 组合变体） | decay 阶梯平坦（冠军 d4=0.82/d8=0.81/d16=0.79）→ **decay 非解锁变量**；impact−spread 加法 0.63 未超乘法 0.66；bid−ask executed 差 0.18 弱 |
| AK | 2U4usi4K35jx93J1dUH3w8Iq | 冠军精调矩阵 + 强成分混入（si3/inst6 × obim，decay4/SUBIND） | **★RRmxpwxa（si3 借贷利用率 10d 变化 + dark/lit）=0.94 波11 新高 / RN 2.16 / RN fit 0.93（RN 双闸门全过）/cluster 1.02/tv 23.4%**——强成分混入首验成功；INDUSTRY 组标准化 0.90 微增益（2y 0.02 转正）；EBITDA 42d 与 EPS 42d 指标完全相同（冗余三连证）；nxt_yr 前瞻 0.65 弱；2×EPS 加权 0.80；**inst6×obim 0.78 反稀释（< 纯 inst6 1.03）** |
| AL | 2JJjFxaSQ4JBaFROHLWSJ4n | si3×obim 追批（窗口 5/15d + 费率反转 + 乘法 + 三成员 + d1 口径，decay4/SUBIND） | **★乘法>加法突破：kqPpZqxz（loan_util 10d × (impact−spread)）=1.09 波11 新高 / 2y 1.06（首次大幅转正）/fit 0.56/tv 18.8%/RN 1.34**；MPGvLPMo（×dark/lit 乘法）1.03/RN 1.99；1Yp3zYqz（15d 加法）0.96/RN 2.19/fit 1.00；费率反转混入 0.65 弱；d1 口径 0.91 |
| AM | 38Rybe9zs5cdb9l183q5RFId | 乘法族精调（INDUSTRY/窗口 5/15d/三成员/dark 15d/费率/新借贷量/单 impact，decay4/SUBIND） | **★RRmx1VKa（loan_util 15d × (impact−spread)）=1.10/2y 1.07/fit 0.60（波11 fitness 新高）/tv 16.5%/RN 1.39**——窗口 10→15d 微升；三成员乘法 1.00 反稀释；单 impact 0.59 弱（差值结构必需）；费率反转/新借贷量成分全灭（0.48/0.53） |
| AN | 1kv0Sa4hL4uh8AeJICMQ0t3 | 乘法冠军终调（INDUSTRY/窗口 12/20d/加权/ts_delta/d1/mean_rate/impact 平滑，decay4/SUBIND） | **★xAN7NPkb（INDUSTRY 组标准化版）=1.13/2y 1.08/fit 0.64/drawdown 5.3%（三指标波11 新高）**；窗口 10-20d 平坦（1.09-1.13）；ts_delta 1.02/mean_rate 0.65 弱；加权/平滑/d1 均无效 |
| AO | 3bTeOGgGC5cMbqWaOHXlOmB | 乘法族 decay2 矩阵（波10 教训：decay2 是 margin/tv 双解锁点，冠军/窗口/×dark 双口径/平滑） | **全灭：decay2 未解锁 margin（0.0-0.1bp），sharpe 1.05-1.17 未超 decay4 冠军（ZYEV7PM1=1.17 最佳）；×dark/lit 乘法 decay2 2y 崩（0.27/0.39）；平滑变体 0.96 → 波10 "decay2 解锁 margin" 教训仅限 institutions6，不可推广** |

### ★si3×obim 乘法族 margin 结构性障碍定案（AO 批回收后）
- **证据链**：乘法族全部批次 margin 0.0-0.6bp（decay4 8 批 32 条）vs decay2 矩阵 0.0-0.1bp（AO 批 8 条）→ **decay 全档无 margin 维度**；sharpe 1.03-1.17 与 decay 阶梯无关；窗口 5-20d 平坦
- **定案**：乘法族（做空需求变化 × 市场冲击净效应）为低频借贷信号，多头/空头平均日收益差被微结构成分稀释至 ~0 → **margin 天花板结构性，非配置问题**；与 institutions6（decay2 解锁 7.2bp）形成对照：解锁变量是数据集特性而非 decay
- **结论**：si3×obim 混合路线判死（67 条实证：AG~AO 八批 64 条 + 探针），冠军 xAN7NPkb 1.13/2y 1.08 留档观察（若后续 margin 维度有新思路可复活）；混合流程保留（expr_lint 门控/批命名/台账），仅本骨架族判死

### ★双数据集混合策略（用户 2026-08-16 授权，流程已融合）
1. **动机**：analyst44 判死时"earnings yield 需价格字段破坏单数据集纪律"被放弃（波9 天花板 0.45 差 3.5 倍）；波11 微结构亮点（dark/lit 0.51、impact−spread 0.60）与基本面风格正交 → 用户授权允许混入两个数据集字段构造经济学意义 alpha
2. **规则**：① 上限 2 个数据集（expr_lint.py 已加双数据集门控：字段→数据集归属追踪，>2 拦截，恰好 2 个标 [MIX]）；② 经济学意义优先（知情交易确认/估值×流动性/信息×微结构）；③ 混合批命名规范 `usa_<ds1>_<ds2>_batch_<tag>.txt`（本波统一 usa_mix_batch_<tag>.txt）；④ 单数据集纪律仍为默认，混合为显式授权扩展；⑤ 已判死数据集可作混合成分（judged dead 指单数据集信号不足，非字段无信息）
3. **混合实证结论（AG~AJ 四批 32 条）**：① 混合放大成立——EPS 修正(0.45)×dark/lit(0.51) 加法复合 0.81-0.88，优于任何单信号；② 窗口 42d 是最优解锁变量（21→42→63→84→126d 呈倒 U）；③ decay 4/8/16 平坦非解锁；④ consensus 指标（EPS/EBITDA/nxt）在混合中仍高度冗余；⑤ 已判死数据集可作成分的路线未验证（AK 批 si3×obim / inst6×obim 在途）

### ★2y check 改名调查定案（LOW_2Y_SHARPE → IS_LADDER_SHARPE）
- **现象**：AG/AH/AI/AJ 批 32 条 alpha 的 checks 中均无 LOW_2Y_SHARPE（2y 显示 null），纯数据集批（WjArQLLd 0.49 / vRN7eLab -0.44）正常 → 一度怀疑 analyst44 数据覆盖不足
- **定案**：dump 对比确认 **IS_LADDER_SHARPE 与 LOW_2Y_SHARPE 占据 checks 同一槽位**（REGULAR_SUBMISSION 之后），纯 analyst44/纯 obim 均有 LOW_2Y_SHARPE，混合批均有 IS_LADDER_SHARPE（QPGRE2RM=-0.08 / O0GdnYJ1=-0.27）→ 平台对新回测启用新检查名（In-Sample Ladder Sharpe），非数据缺失；`_wait_sims.py` 已兼容两者
- **实质问题**：混合 alpha 的 2y 为负（-0.08~-0.28），与纯微结构（-0.44）同性质 → IS 后期（近 2 年）表现弱是信号问题，记录在案待 sharpe 达标后处理
- **数据覆盖反证**：analyst44 本地数据包完整（7730 观测/覆盖 2014-2023/稳健），WjArQLLd 纯 analyst44 2y=0.49 → 覆盖无忧

### 波11 阶段结论与下一步
- 双数据集混合实证链：加法（0.88/0.94）→ 乘法（1.03/1.09/1.10）→ **INDUSTRY 组标准化冠军 xAN7NPkb = 1.13/2y 1.08/fit 0.64/drawdown 5.3%**；窗口 10-20d 平坦；ts_delta/d1/加权/平滑/mean_rate 全部无效（ts_av_diff + 差值结构是唯一定式）
- **★混合路线定案（AO 批回收后）**：si3×obim 乘法族 margin 结构性天花板（0.0-0.6bp，decay2/4 全档验证）→ 波11 判死；冠军 xAN7NPkb 1.13 留档；**混合策略流程本身保留**（用户授权项，expr_lint 门控 + 台账规范已融合），后续可与其他数据集组合复用
- **波11 累计**：AA~AO 十五批 120 条回收（PASS=0）；战役累计 672 条回测
- **下一步（波12）**：① Round20 多样性评估（已到期，z10k/z11d）→ 确定下一数据集方向；② canvas 五槽填槽落地报告更新；③ 按 Round20 结论启动新金字塔（候选：宏观/估值类蓝海数据集，避开已判死 7 族）

## 波12（2026-08-16）：macro38 技术面探针

### 启动决策（Round20 评估产出）
- **数据集**：macro38 (Technical Ratings Model) — os_is_sharpe 0.5392（候选最高）/ 1371 用户蓝海 / 宏观金字塔未点亮（need 3）/ 技术面风格与全部已判死族（情绪/期权/借贷/分析师/机构/微结构/混合）独立
- **字段登记**：56 字段全部通过 sharpe 过滤 → 已登记 fields_gate.json (MATRIX 型，signal/direction/strength 三维 + 聚合信号 + 价格字段)
- **骨架设计**：技术评级共识方向（overall_signal/percent）、方向×强度乘法、期限结构（MACD 快慢背离 / MA 多头排列）、专有指标确认（trendspotter）、margin 预检对照（percent_change 水平 vs ts_av_diff 变化）

### 批次与结果
| 批 | multisim | 内容 | 结论 |
|---|---|---|---|
| AP | 18SROS4J04PPayJ1c9tpVSmg | 技术面探针 8 条（共识/百分位/方向×强度/短期变化/MACD 背离/MA 排列/trendspotter/价格动量），decay4/SUBIND | **回收：信号存在但换手超高 + margin 结构性弱**。短期共识 5d 变化 88pW3aJW=1.09/2y 1.35（最高）但 tv 56.5%✗；方向×强度 xAN7YPGl=1.05/2y 1.02 但 tv 37.6%✗；overall 共识 pwNbPVGo=0.70/tv 15.5%✅（方向正确）；MACD/MA 期限结构 0.49-0.64 弱；percent_change 动量 -1.37 负向（反转候选）；**margin 全族 0.0-0.1bp（评级类信号 margin 结构性弱，同 si3×obim 性质）** |
| AQ | 4Epou92eI4go98E3EnJ2QxO | 换手控制追批 8 条（窗口 10/20d、decay 平滑、中期/长期共识、共识×强度、全共识动量、动量反转），decay4/SUBIND | **回收：动量反转是 macro38 最强信号**。reverse(percent_change) d5ZJOrz2=1.37/2y 1.37/fit 0.64（波12 最高，信号稳定）但 tv 58.5%✗/margin 0.44bp✗；短期变化窗口越长越弱（5d 1.09→10d 0.93→20d 0.70）；ts_decay 平滑压 tv 到 16.4% 但信号稀释到 0.76；medium/longterm 慢变 tv 达标但弱（0.70/0.44）；**margin 两批 16 条全 0.0-0.4bp → 评级类信号族 margin 结构性弱定案方向** |
| AR | 1S1dDK3k64VpcxNeBxFTaNB | 边际字段族探针 8 条（ADX/BB/CCI/PARA/MAHILO 信号 + ADX 强度 + BB 复合 + BB 变化），decay4/SUBIND | **回收：macro38 信号显著，MAHILO/ADX/CCI 三族 tv 达标**。MAHILO 88pWjO3a=1.33/fit 0.74/2y 1.31/tv 29.0%✅（波12 冠军，距闸门 1.19 倍）；ADX xAN73eNp=1.26/fit 0.70/2y 1.17/tv 24.4%✅；CCI 40d 3qpmXEl6=1.23/2y 1.51（2y 接近闸门）但 tv 33.9% 微超；BB kqPponj8=1.00/tv 20.9%✅；PARA 0.96/BB 变化 0.17 弱；**margin 三批 24 条全 0.0-0.6bp → 评级类信号族 margin 结构性弱确认，但 sharpe 1.33 距闸门仅 1.19 倍（非 3 倍结构性线）→ 不能判死，进入精调** |
| AS | JlRyFlB4EBciCkCSrDDOg (d4 主批 6 条) + 1vh3JaeuN5bSaGYbi95gEsd (d2 单条) + 2gN0o5x14CW8UjzNoVyBSH (d8 单条) | 冠军骨架精调 8 条（MAHILO decay2 margin 解锁/MAHILO×强度/MAHILO×ADX 强度/ADX×强度/CCI decay8/CCI×强度/MAHILO+ADX 加法/MAHILO 5d 变化），混合 decay | **回收：decay2 是 macro38 sharpe 解锁点（非 margin）**。MAHILO decay2 1Yp3ZxwX=1.46/fit 0.76/2y 1.53/tv 36.6%（sharpe/2y 接近闸门，tv 微超）；MAHILO+ADX 加法 d4 E5GnRa09=1.34/fit 0.78/tv 26.5%✅；MAHILO 5d 变化 P0GLglqw=1.31/2y 2.14（2y 超闸门）但 tv 57.1%✗；CCI decay8 稀释到 0.96；**decay2 解锁维度因数据集而异（inst6=margin / macro38=sharpe）**；margin 四批 32 条全 <1bp → 评级类信号族 margin 结构性弱确认 |
| AT | 1brTKFcgo4rvaAt4AtZ39h1 (d2 主批 6 条) + H2E61gX34FzbPzfsoRiBUI (d3 单条) + 1CVbUWaO94IQbmMfcmVWBSu (d1 单条) | MAHILO decay2 精调 8 条（decay3 压 tv/×MAHILO 强度/×ADX 强度/INDUSTRY 组标准化/+ADX 加法/×BB 信号/ts_mean5 平滑/decay1 对照），混合 decay | **回收：decay2 是 sharpe/2y 最优**。MAHILO+ADX 加法 decay2 1Yp3j7zz=1.47/2y 1.57/fit 0.75（波12 冠军，距闸门 1.07/1.02 倍）但 tv 37.8% 微超；decay 阶梯 1/2/3/4 = 1.45/1.46/1.39/1.33，tv 44.4%/36.6%/32.0%/29.0%（decay4 唯一 tv 达标）；×强度/组标准化/平滑均无效；**margin 五批 40 条全 <1bp → 评级类信号族 margin 结构性弱定案；sharpe 距闸门仅 1.07 倍 → 未判死，进终验** |
| AU | stat:2utckl7zA5hkc8hQGEMFDNs / d2:3y0zhDaMn57qc6heP2LD971(重提) | 终验 8 条（STATISTICAL 中性化 + MAHILO+ADX+CCI 三成员 + 组标准化 + 强度加权），decay2 | **★AU-stat 突破：STATISTICAL 中性化 1Yp3N7dX=1.71/2y 1.87/fit 0.78（sharpe/2y 双双破闸门 1.58/1.6）**但 tv 34.05% 微超/margin 0.42bp 弱；AU-d2 回收：ts_mean3 xAN7v0am=1.45/2y1.43、+BB O0GdWEaY=1.45/2y1.47、组标准化 ak1maqqw=1.34，均低于 STAT；**STATISTICAL 是 macro38 唯一破闸门路径** |
| AV | d3:2fIItJ3yt4FOckf1h0kVEInS / d4:4q5JDaLR4yz8CJzrwabuIZ / d2:3jjkHMawg4Z9bjrA7nZFi3L | STAT 冠军精调 8 条（decay3/4 压 tv、ts_mean3 平滑、+CCI/BB 三成员、×strength、winsorize、MAHILO 单成员对照），全 STAT | **★回收：三指标同时达标者出现**。YPv3aOwq（MAHILO+ADX STAT decay3）=**1.65/2y 1.80/fit 0.79/tv 29.97%✅**（sharpe/2y/tv 三项达标，仅剩 fit 0.79<1.0 + margin 0.46bp）；GrGjmx8x（+CCI 三成员 d2）=**1.79/2y 1.98/fit 0.82**（战役新高）但 tv 35.4%✗；vRN7A6Jw（×strength）2y 2.09 最高；decay3 是 tv 达标拐点（d2 35.4%→d3 29.97%）；**margin 六批 48 条全 <1bp → 评级类信号族 margin 结构性弱铁证** |
| AW | nOryde8H5is9Fl5nfLWgDr | STAT 冠军 fit 提升 8 条（三成员+decay3、×strength、组标准化 INDUSTRY/SUBIND、+direction、四成员、winsorize），全 STAT decay3 | **回收：fit 提升全灭，macro38 判死定案**。fit 天花板 0.82（AV GrGjmx8x），AW 批 0.60-0.80 无一人超越；A1GXL7dW（四成员）=1.61/fit 0.80/tv 27.5%✅ 最接近；**fit 0.79-0.82 距 1.0 差 1.22-1.27 倍 + margin 0.46bp 距 5bp 差 10.9 倍 → 双结构性墙**；sharpe/2y/tv 可达标（YPv3aOwq 1.65/1.80/29.97%✅）但 fit/margin 不可解锁 |

### 波12 判死定案（2026-08-16）
- **macro38 (Technical Ratings) 七批 56 条穷尽**：sharpe 最高 1.79（GrGjmx8x）、2y 最高 2.09（vRN7A6Jw）、tv 可达标（27-30%），**但 fit 天花板 0.82（距 1.0 差 1.22 倍）+ margin 天花板 0.62bp（距 5bp 差 8 倍）双结构性墙**
- **定式**：MAHILO+ADX(+CCI) 加法 + STATISTICAL 中性化 + decay2/3 是最优骨架；STATISTICAL 是唯一破 sharpe/2y 闸门路径（SUBIND/INDUSTRY/MARKET 均 ≤1.47）
- **margin 结构性弱根源**：技术评级信号（B/S/H 三态 + 1-5 强度）是低频离散信号，价格冲击极小 → margin 天花板 <1bp，与 si3×obim 混合族同性质
- **fit 天花板根源**：技术评级信号间高度相关（MAHILO/ADX/CCI/BB 均趋势跟踪），复合加权无法突破信息含量上限
- **保留资产**：冠军 YPv3aOwq（1.65/2y1.80/tv29.97%✅）留档；STATISTICAL 中性化对技术面数据集的有效性已验证（可复用到其他技术/价格类数据集）
- **下一步（波13）**：切换新金字塔数据集。候选：earnings4（盈余漂移，事件驱动风格）/ news52（新闻情绪，文本风格）——均与已判死 8 族（情绪/期权/借贷/分析师/机构/微结构/混合/技术评级）独立
| AT | ZUfMz4N45i8bed1aPOMkzHx | ★3-5 数据集混合探针 8 条（用户授权放宽上限，lint --max-datasets 5）：3ds 加法/乘法（si3+obim+macro38）、4ds 加法/乘法（+analyst44 EPS）、5ds 加法（+inst6）、2ds 乘法对照、obim 成分变体（dark/lit vs impact-spread），decay4/SUBIND | **回收：5 数据集加法 LLGoZ29L=1.27/fit 0.67/2y 0.90/tv 18.0%✅ 为混合族新高（超 2ds 对照 1.13）**；4ds 加法 ak1mxg7w=1.21/fit 0.68；3ds 乘法 XgoZJO7b=1.03；**成分增加单调提升 sharpe（2ds 1.13→3ds 1.03→4ds 1.21→5ds 1.27，加法路线）但 margin 全族 0.5-0.7bp 无改善**；乘法路线 3ds 1.03/4ds 1.09 均低于加法；obim 成分 dark/lit vs impact-spread 无显著差异 |

---

## 每 10 波全量多样性评估（独立成章）

> 触发条件：累计波次达 10 的整数倍，或回测轮次达 10 轮边界。内容：算子探索率、字段探索率、骨架多样性、风格多样性、预处理分布、收益来源归因、失效风险、skills 优化项。

**第 10 轮边界评估（波1-4）**：已内联于波4 节。核心结论：风格单一（全波动率相对价值）+ 两数据集 PROD 墙 → 强制转向情绪/事件风格。

**Round10 全量评估（波1-7，批次 A→OO，~26 轮 ≈208 条）**：详见 `runs/usa_diversity_review_round10.md`。核心：数据集探索率 3.4%（8/237，情绪超配）、字段 ~11%、算子 ~16%（ts_entropy/days_from_last_change/winsorize 未试）；收益归因：信号上限由数据集信息含量决定，骨架只能逼近不能突破；skills 已落地：选集 SOP（userCount<1000 蓝海优先）+ 情绪族判死标准。下 10 轮主攻 option40，备选 macro38/imbalance5。下次全量评估：波17 或 Round20。

**Round20 全量评估（波8-11，批次 PP→AO，~44 轮 ≈352 条）**：详见 `runs/usa_diversity_review_round20.md`。核心：① 收益归因升级——每条路线撞不同类型的墙（红海族=PROD 墙 / 低频弱信号族=信息含量墙 / 混合族=margin 结构性墙 0.0-0.6bp），margin 墙与数据集特性绑定（inst6 d2 解锁 7.2bp vs si3×obim 全档无效）；② 探索率：数据集 4.6% / 字段 ~16% / 算子 ~19%，obim 198 字段仅探 ~35；③ 风格 7 类仍缺技术面/宏观/盈余漂移/事件；④ skills 落地：混合流程融合（expr_lint 门控+命名+台账）、2y 双名称兼容、乘法定式、判死粒度升级（骨架族级）；⑤ 建议新增 margin 预检规则（新数据集首发批混入水平/变化信号对照）。**波12 决策：主攻 macro38（Technical Ratings），备选 earnings4/news52；禁用已判死 8 数据集全系 + 情绪类 + si3×obim 混合骨架族**。
