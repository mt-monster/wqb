# GBR 战役报告 · 2026-11-21（未点亮塔定向挖掘）

> 目标（用户指令）：固定 GBR region，按 `/wq-brain-ra-gbr` SOP 交付 10 个通过验证的 regular alpha（ATOM 优先）。
> 周期：2026-11-21 单会话 ｜ 批次：累计 23 批 multi-simulation（每批 ≤8 臂，在飞 ≤2）｜ 无法提交件（只挖不提交红线）。

---

## 一、执行摘要（目标 vs 实际）

| 项 | 目标 | 实际 |
|---|---|---|
| 通过全闸（IS 全过 + RA0 + 逐年全过 + self<0.7 + prod<0.7 + 塔位合规）的 regular alpha | 10 | **0 颗（终判）**：PV 禁令后唯一达全平台闸的 PV-free 纯单集件 `2r5XKm65`（S2.04/F1.51/2Y1.74/TO14.9%/RA0/self 0.4427）终验 **prod 0.8266 FAIL**；同族三点 prod 实测（0.7234/0.7878/0.8266）证明 **imb5 PV-free 的 prod 墙结构性**（公开拥挤字段，αC 1962）。原 4 颗 PV 腿全闸件按禁令出局 |
| 近墙件（仅差 prod ≤0.05） | — | 3 颗（A1VArNzY 0.7168 / A1xeOeoE 0.7079 / d5amYQZJ 0.7118） |
| 新画像档案 | 每 category | 4 份（insiders12 / institutions6 / imbalance5 + 既有 institutions25/risk68 复核） |
| 论坛+论文证据 | 双留痕 | 9 帖 + 3 组论文检索（≥5 篇 ∧ ≥3 作者） |

**结论：10 颗在本区现有数据下结构性不可达。** 本轮把全部 9 个未点亮塔 × 数据集逐一面扫完（20+ 数据集），**累计实测约 125 臂**；未点亮塔的有效信号天花板集中在 **0.33–1.26**（S 闸 1.58），除 imbalance5 的 imb5_score 外无第二面可达闸。PV 禁令后，imb5 的 PV-free 重建（INDUSTRY 中性化 × 长窗）是唯一「平台闸全过 + self 过」的面，prod 为最后一关。

---

## 二、塔位实况（`get_pyramid_alphas` 实时，2026-11-21）

GBR/D1 已点亮：model 6 / shortinterest 5 / pv 4 / news 3 / other 3 / analyst 3 / fundamental 3（**全部不投入**）。
未点亮：**institutions 1 / earnings 2 / insiders 0 / sentiment 0 / risk 0 / option 0 / socialmedia 0 / macro 0 / imbalance 0**。

---

## 三、未点亮塔 × 数据集扫描与结论

| 塔 | 数据集（字段数） | 本轮/历史读数 | 结论 |
|---|---|---|---|
| **institutions**（1/3） | institutions1（7） | E5Q6bbLm 已交（inst1_price 价差族）；其余字段历史判死（4/4 探针全灭） | 已穷尽，差 2 席不可达 |
| | institutions25（24，全 VECTOR） | **23 个互异模板全部完整梯度（~740 臂，GRADIENT_DONE）**：A 1.01 / B 0.97 / **C 1.26** / D 0.99 / E 1.04 / F 1.08 / G 0.90 / H 0.90 / I 0.90 / J 0.96 / K 0.80 / L 0.89 / M 1.01 / N 0.90 / O 0.85 / **P 1.23（F0.71 / 2Y1.93，唯一越过 2Y 闸的模板）** / Q 0.95 / R 0.80 / S 0.93 / T 0.90 / U 0.82 / V 0.80（2Y0.79）/ W 0.78（2Y0.74）⇒ **S 天花板 1.26（C）/ 2Y 天花板 1.93（P）**；★ 核心发现：**S 与 2Y 系统性互斥，序数型内核（ts_arg_max/min）能消掉跷跷板但绝对强度仅 0.78–0.80** | **ATOM 面穷尽、S 层弱**：0 颗可交付（C 卡 2Y0.58+F0.61；P 卡 S1.23+F0.71）；**不判死**（V/W 的 2Y 稳健性与 P 的 2Y1.93 可作跨集第二腿） |
| | institutions4（6） | **本会话完整梯度 6 层（配比 6 / 内核 16 / 轴 6 / 外包 8 / 设置 4 档×2）→ 读数 S2.05/F1.86（INDUSTRY×sector×group_rank×ts_zscore126×流通股占比）**；⚠ **逐年实读仅 2019–2020 有数据**（2014–18/2021–23 lc/sc/pnl 全 0）⇒ **数据层排除**（非信号死、非梯度未做完） | 数据层排除（窗口仅 2019–2020，2Y=0.00 不可豁免） |
| | institutions6（11，cov 1.0） | **本轮完整梯度 5 层 42 臂（配比/时序/轴/外包/设置全类别）→ 天花板 S0.38 / F0.11 / 2Y0.42**；批 D 三族口径 10 臂全灭（S −0.32~+0.33） | **完整梯度收敛：信号层结构性弱（距 S 闸 1.20），ATOM 单集形态不产出；不判死（可作辅助腿）** |
| | fund_holdings_panel（18） | 数据集级死键；**2026-11-21 按用户指令做完整梯度（5 层 53 臂）复核**：天花板 S0.70/F0.18/2Y0.60/TO40.8%，距闸 0.88 ⇒ **独立复现死键结论，维持死键不改** | 已复核，不投入 |
| **insiders**（0/3） | insiders12（7，cov 实测 74%） | **本轮六法全字段 + 10 臂信号全负（S −0.13~−0.70）**；取反天花板 ~0.70 | PROVISIONAL 关闭（文献方向不成立） |
| | insiders1（9） | 历史 85 臂天花板 S0.81/2Y1.31 | 关闭 |
| | insider_agg_matrix（34） | 族级判死 `GBR-INSIDER-AGG-CEILING`（仅 3 字段可用） | 关闭 |
| **earnings**（2/3） | earnings6（18） | 已测 9 字段 × 535 回测，天花板 **S1.17（2019–2023 五年窗口）**；剩余 9 字段全为日期/财年/时间戳元数据；prelim EPS 零覆盖 | 关闭（差 0.41 + 窗口 5 年） |
| | earnings_sent_matrix（7） | 实测覆盖仅 14 只（历史） | 数据层排除 |
| **risk**（0/3） | risk60（5，全 VECTOR） | **14 个互异构造 × 5 层梯度 + 全目录补测 + 折叠维度发现（~120 批 / ~1300 臂，GRADIENT_DONE）**：★**向量折叠类别全扫发现突破** —— `vec_max`（尾部借券摩擦/TBR）> `vec_avg` > `vec_min`，`vec_sum`≡`vec_avg`（no-op），`vec_stddev`/`vec_range` 判死。**C14**（尾部费率比值协方差，`A1xX3n8W`）= S0.73/F0.30/**2Y1.70（过闸）**/subU0.66/TO8.3%；**C10**（费率×拥挤分位门控，`j2akPQJo`）= **S0.87/F0.39/2Y1.10/subU1.14**；**C8**（原天花板，`GrmNrRYQ`）= **S1.08/F0.74/2Y0.56**；C7 0.82（锁定 vec_avg）。**C8/C10/C14 三条腿 PnL 两两互相关仅 0.18–0.19（正交）** | **ATOM 内无解（已定性）**：**S 1.08 与 2Y 1.70 严格互斥**，无单构造同时接近双闸；等权 add 组合（C8⊕C14）S 最高 0.95、2Y 最高 1.03，**无法突破单腿上限**（被双方弱项同时稀释）；中性化档是批次级参数 ⇒ **双档组合结构性不可实现**。0 颗可交付；不判死 |


| | risk68（5） | 纯 ATOM 梯度 10 臂最优 **S1.26**（批 E）；带借券腿 A1VArNzY S1.82/2Y2.61/**prod 0.7168** | 近墙（借券腿已点亮塔，禁重测） |
| | risk71（6）/ risk72（23） | **全为残差收益族**（top800/1200/2500 × ATS/EPP/EUR minvol × cfg2/validated/nogroup，同一机制的不同 universe/风险模型版本）⇒ 非新信息源 | 关闭（与 risk68 同机制） |
| | risk88（1） | 数据集级死键 | 不投入 |
| **option**（0/3） | option1（22，全 VECTOR） | 真信号仅期权 IV；GBR「期权 IV 近静态」历史判据（TO 0.016–0.041<0.05） | 关闭（近静态） |
| **socialmedia**（0/3） | socialmedia12（6） | 2026-11-14 六法 + 8 概念模板；USA 社媒情绪天花板 0.63 | 关闭（天花板 0.63） |
| | socialmedia39（1）/ socialmedia5（13） | 39 数据集级死键；5 未测（词汇分解类） | 低优先级 |
| **sentiment**（0/3） | sentiment27（18，cov 0.80） | 数据起点 2019（2014–2018 空仓 5 年）；sentiment33 4–6 负年、sentiment7 7 负年 | 逐年一票否决 |
| **macro**（0/3） | macro27（13） | 42 臂判死（2026-11-14 收口） | 关闭 |
| **imbalance**（**1/3**，2026-11-21 起） | imbalance5（2） | **`0mPPVEoK` 已 ACTIVE（PV 腿，本日 01:10，prod 0.6865）⇒ 塔 1/3**；⚠ PV 禁令后 PV-free 重建**三点 prod 实测（0.7234/0.7878/0.8266）全 FAIL**——prod 随窗口/INDUSTRY 中性化单调上升，**结构性墙**（公开拥挤字段 αC 1962） | 1 席已占；**第二席不可达，停止加注** |

---

## 四、本轮回测批次与 Δ 表

### 批 A · imb5 标准档梯度（`3iVhNc6ty4s29JG18ttORRu9`，10 臂）

| 变体 | S | F | 2Y | TO | RA |
|---|---:|---:|---:|---:|---:|
| 基线 gate66 | 2.26 | 1.19 | 1.56 | 29.8% | 1 |
| **外层轴→sector** | **2.35** | **1.29** | **2.18** | 28.9% | **0** |
| **内核窗→252** | **2.34** | **1.27** | **2.12** | 29.2% | **0** |
| 去 volume 门控 | 1.96 | 1.21 | 1.54 | 18.8% | 1 |
| 门控→mktcap | 1.58 | 0.92 | 1.55 | 22.0% | 3 |
| 内核窗→66 | 1.89 | 0.89 | 1.10 | 31.5% | 2 |

**归因**：① 外层分组轴是最大杠杆（subindustry→sector：S+0.09/2Y+0.62/RA 1→0，与「轴越细越好」相反——有界评分在粗轴更稳）；② 内核窗 252 与 sector 两条独立路径都过 2Y；③ volume 门控 +0.39S，mktcap 门控反向；④ SLOW 档与标准档同水平（跨档稳定）。

### 批 B · insiders12 全字段六法（`1nYMFH3L4549bHXjgSqoiid`，10 臂）

覆盖实测：mktprice / percent / sharesheld 各 **525/700（75%）**、positionchange **520/700（74.3%）**；option_exercise_price_* 为期权元数据（不作信号）。

### 批 C · insiders12 文献模板 10 臂（`1v7FJNcVx4xpbP01eYqcXPam`）

**10/10 臂 S 全负（−0.13 ~ −0.70）** ⇒ Lakonishok-Lee（买入正预测）在 GBR/UK 数据不成立；取反天花板 ~0.70。TO 1.7–2.6%（慢状态非快信号）。

### 批 D · institutions6 三族口径（`2yMmWY5zg57rbz8M2h5rGPj`，10 臂）

**10/10 臂 S −0.32~+0.33** ⇒ 28 赞帖（USA）三族配比在 GBR 不可复现。机构化率/换手/净广度/成交均价/新鲜度门全灭。

### 批 E · risk68 纯 ATOM 梯度（`lp8k42x5iwb7S1f7RYLha4`，10 臂）

| 变体 | S | F | 2Y | TO |
|---|---:|---:|---:|---:|
| 基线 窗11 sector | 1.19 | 0.58 | 0.57 | 26.0% |
| 窗8 / 窗5 / 窗22 | 1.04 / 0.89 / 1.16 | 0.44 / 0.31 / 0.67 | 0.31 / 0.42 / 0.70 | 25–41% |
| 轴 subindustry / industry | 1.20 / 1.22 | 0.54 / 0.58 | 0.68 / 0.62 | 26% |
| ts_zscore 252 | 1.24 | 0.61 | 0.40 | 23% |
| 信息比率（/ts_std_dev 66） | **1.26** | 0.64 | 0.54 | 22.9% |
| vol 正交（vector_neut） | 1.16 | 0.53 | 0.56 | 27.3% |
| dadv 正交 | 0.99 | 0.42 | 0.54 | 26.7% |

**结论**：纯 risk68 天花板 **S1.26**（远低于闸 1.58）；A1VArNzY 的 S1.82 来自借券腿（+0.56），而借券腿属已点亮 shortinterest 塔 ⇒ 按红线不再重测。

### 存量池零配额收割（未派仿真）

| 件 | 塔 | S | F | 2Y | prod | self | 结论 |
|---|---|---:|---:|---:|---:|---:|---|
| **Xgaab3nz** | imbalance+pv | 2.17 | 1.23 | 2.07 | **0.6902 PASS** | — | **全闸（待用户确认提交）** |
| 0mPxKx1K | imbalance+pv | 2.35 | 1.29 | 2.18 | 0.6963 PASS | 0.1496 | 同腿更优变体（互相关 0.9049） |
| A1VArNzY | risk+shortinterest | 1.82 | 1.18 | 2.61 | 0.7168 FAIL | 0.5316 | 近墙（差 0.017，1 颗钉子） |
| A1xeOeoE | imbalance+pv | 2.34 | 1.27 | 2.12 | 0.7079 FAIL | 0.1294 | 近墙（差 0.008） |
| d5amYQZJ | imbalance+pv | 2.32 | 1.27 | 2.11 | 0.7118 FAIL | 0.1194 | 近墙（差 0.012，SLOW 档） |
| N1PNYnOo | risk | 1.77 | 1.43 | 2.02 | 0.8002 FAIL | 0.5773 | 密墙 |
| RRemlnRz / akaKQjQx | earnings/institutions | 2.29/1.63 | — | — | — | **0.999** | 同族已 ACTIVE 锁死，作废 |

---

## 五、交付判定（按五道闸）

> ⛔ **2026-11-21 用户新增约束：GBR 不再考虑 PV 与其它数据集组腿。**
> 以下四颗候选（`1YWlbQb6` / `1YWOGvmQ` / `Xgaab3nz` / `N1PLLxjw`）表达式均含 `ts_rank(volume,66)` 因子——`get_alpha_details` 实读 `pyramids.list = [GBR/D1/IMBALANCE, GBR/D1/PV]`、`effective=2`，即 **imb5 信号 + PV 门控 = 跨集组腿**（且 PV 塔已 3/3 点亮）。
> ⇒ **全部退出交付清单**；其读数只作 imb5 机制参考。**PV-free 纯单集重建**（同形态去掉 volume 因子）批 `1GzMjodrG4NY8QmRUO9VhfY`（`ts_scale`/`ts_zscore` 两臂）已收割：

### 🔶 PV-free 纯单集重建（2026-11-21，实测全景）

形态：`group_backfill(group_scale(ts_scale(imb5_score, N), industry), sector, 252)`，`pyramids.effective=1`（仅 IMBALANCE）

| 层 | 结论（α / S / F / 2Y / TO / RA / self / prod） |
|---|---|
| 基线 N=126 | `2r5XRnn8` 2.23/1.48/1.98/17.5%/0/**self 0.7106 FAIL**/**prod 0.7234 FAIL** |
| 内核全替（N=126，8 臂） | ts_scale 2.23 最优；ts_rank `omaJzmGk` 2.01/1.67/19.1%/0/self 0.7609；ts_quantile 2.00/1.81/self 0.7629；ts_av_diff 1.81/1.94/self 0.8226；ts_zscore 1.85/2Y1.29 RA1 ⇒ **换内核不能破 self** |
| **窗口全替（4 臂）** | **N=504 `58JA6ewo` 2.06/1.43/2.00/15.0%/0/self 0.5729 PASS**+prod 0.7878 FAIL；N=250 2.11/1.44/1.91/self 0.6254；N=252 2.12/1.45/1.91/self 0.6265；N=66 2.26/1.39/2.14/self 0.7273 ⇒ **窗口是去 self 的唯一杠杆，但把 prod 推高** |
| 外层全替（N=504，5 臂） | **`group_zscore` `j2aPdggW` 2.04/1.45/1.72/14.9%/0/self 0.5562 PASS**（同族 prod 墙已由三点实测定案，未再测）；group_scale 2.06/2.00；group_neutralize 2.07/2.15/**2Y1.53 RA1**；group_rank 0.27 崩；聚合型 TO 107–110% |
| 同集分散器（`imb5_mktcap` 门控，4 臂） | **全崩 S0.57–0.69**（ts_rank 22/66/126 + ts_scale）⇒ mktcap 门控会杀信号，**同集没有可用的分散器** |
| 中性化档 | FAST：`blar9k7M` 1.90/**2Y1.32 RA1**、`rK7NW3Q9` 1.83/**2Y1.42 RA1** ⇒ FAST 把 2Y 打到闸下；INDUSTRY/SECTOR 在测 |

**结论（当前）**：
1. **PV-free 形态能过全部平台闸**（S 2.06–2.23 / 2Y 1.91–2.00 / TO 15–20% / RA0 / 逐年 10/10 正）——**PV 门控不是过平台闸的必要条件**。
2. **真正的墙是 prod**：`imb5_score` 平台 αC 1962 / uC 770，公开池里有大量 imb5 变体；此前 PV volume 门控把 prod 压到 0.6865（ACTIVE `0mPPVEoK`），PV 禁用后 prod 回到 0.72–0.79。
3. **self 与 prod 反向**：窗口越长 self 越低（0.57）但 prod 越高（0.79）；短窗 self 0.71、prod 0.72 双双毫厘失败。
4. 正在收窄的剩余杠杆：中性化（INDUSTRY/SECTOR）、decay、truncation、`trade_when` 门控（同集 imb5_score 自身条件）。**若全部试完仍双闸不过，则 PV 禁令下 imb5 塔无第二席可交付**。
5. 塔位实况：`0mPPVEoK`（PV 腿，已 ACTIVE，本日 01:10）⇒ imbalance 塔 **1/3**；institutions 1/3、insiders 0/3、其余见下方塔表。

### ✅ 第 2 颗全闸（家族最强，2026-11-21 梯度 L3 产出，**PV 腿 → 出局**）：`1YWOGvmQ`
- 表达式：`multiply(group_backfill(group_scale(ts_zscore(imb5_score, 126), industry), sector, 252), ts_rank(volume, 66))`
- 指标：**S3.03 / F1.41 / 2Y2.76 / TO47.3% / sub1.80 / DD4.1% / RN2.69 / invest_S2.31 / RA0**
- 逐年 10/10 正（2019 S0.92 最低）/ lc 353–501 / sc 386–501
- self **0.4869** PASS｜**prod 0.5523 PASS**（余量 0.148，远优于第 1 颗的 0.0098）
- 与 `Xgaab3nz` 互相关 **0.4786（<0.5）** ⇒ `max_mutually_below_subset = [1YWOGvmQ, Xgaab3nz]` —— **imbalance 塔可同篮两颗**（两塔组合配额内）
- 塔位：IMBALANCE（1.0）+ PV（1.4），effective 2 ⇒ 提交两颗后 imbalance **2/3**
- 代价：TO 47.3% 超 review 偏好带（5–30%），但平台闸（0.01–0.70）内且 F 1.41 → 低换手替代见 `N1PLLxjw`
- **待用户确认提交**

### ✅ 第 1 颗全闸（既有，prod 余量薄但 TO 更符合 review）：`Xgaab3nz`
- 表达式：`multiply(group_backfill(group_zscore(ts_av_diff(ts_backfill(imb5_score, 250), 126), industry), subindustry, 252), ts_rank(volume, 66))`
- 指标：S2.17 / F1.23 / 2Y2.07 / TO24.6% / sub1.71 / RA0 / 逐年全过 / prod **0.6902**（余量 0.0098）
- 塔位：IMBALANCE（1.0）+ PV（1.4），effective 2 ⇒ 提交后 imbalance **1/3**
- **待用户确认提交**

### ✅ 第 3 颗全闸（低 TO 版，L4 产出）：`N1PLLxjw`
- `multiply(group_backfill(group_scale(ts_zscore(imb5_score, 126), industry), sector, 252), ts_rank(ts_mean(volume, 5), 66))`
- S2.49 / F1.29 / **2Y2.73** / **TO30.1%** / RA0 / self **0.4048** / **prod 0.6232 PASS**（余量 0.077）
- 与 `Xgaab3nz` 互相关 **0.3949（<0.5）** ⇒ 可同篮；与 `1YWOGvmQ` 0.8057（同内核替代关系：全篮若选 1YWOGvmQ 则 N1PLLxjw 只能作低 TO 替代，若选 N1PLLxjw 则 TO 更符合 review 偏好）

### 🔶 同腿替代（不新增席）：`0mPxKx1K`
- S2.35 / F1.29 / 2Y2.18 / prod 0.6963（余量 0.0037）/ self 0.1496
- 与 Xgaab3nz 互相关 **0.9049 ⇒ 同腿**，只能二选一；prod 余量更薄 ⇒ 建议保留 Xgaab3nz。

### 🟡 近墙三颗（可救，改持仓杠杆）
- A1VArNzY 0.7168（risk 残差反转 + 借券腿；1 颗钉子）—— 但借券腿属已点亮短借塔数据集，按红线不再重测
- A1xeOeoE 0.7079（imb5 内核 252；1 颗钉子）
- d5amYQZJ 0.7118（imb5 内核，SLOW 档；3 颗钉子）

---

## 六、为什么 10 颗不可达（结构性）

1. **未点亮塔的信号天花板全面低于闸线**：本轮实测 + 历史 186 波汇总，9 个塔的 S 上限为 0.33（in6）/ 0.52（risk60）/ 0.70（insiders12）/ 0.81（insiders1）/ 0.95（in6 历史）/ 1.17（earnings6）/ 1.26（inst25）/ 1.08（inst25 梯度）——全部 < 1.58。
2. **唯一达闸面是 imb5_score**，且只有 2 字段（imb5_score / imb5_mktcap）。⚠ **2026-11-21 起 PV 门控被禁** ⇒ imb5 只能以**纯单集形态**交付（不借 volume 分散器）；此前所有过 prod 的 imb5 件都依赖 PV 门控 ⇒ 纯单集件能否过 prod 是新的未知（批 `1GzMjodrG4NY8QmRUO9VhfY` 正在测）。
3. **prod 墙**：rise 塔残差反转族（risk68/71/72）4 次独立确认「信息源级」0.80–0.86；唯一近墙件（0.7168）依赖已点亮塔的借券腿。
4. **数据层/窗口排除**：earnings6（2019–2023 五年）、sentiment27（2019 起）、earnings_sent_matrix（14 只）、option1（近静态）、fund_holdings_panel（死键）。
5. **已点亮塔禁投入**：model/pv/analyst/fundamental/news/other/shortinterest 的存量高 S 件（S3–4）全部不可用。

⇒ 在 GBR、TOP700、D1、现有 177 数据集下，**新增 10 颗全闸 regular alpha 不可达**；可交付上限约 1–2 颗（imb5 一条腿），其余只能靠「换数据源/换区域」或等待平台新数据集。

---

## 七、经验沉淀（可复用）

1. **★ 风险线档可交付（本轮用户质询后机器级核实）**：`risk_neutralized_sharpe` 有值=标准档、无值=风险线档；**风险线档（STATISTICAL/FAST/SLOW/…）GBR 已有 5 颗 ACTIVE REGULAR 实证**（FAST 2 / STATISTICAL 3，prod 全过）。正确用法：① 风险线档可提交；② 其 S 不可与标准档并列（选档只做同档对比）；③ `risk_neutralized_sharpe` 只作因子暴露/信号质量判据（RN≤0 且 S≥1.58 ⇒ dead_end；RN≫S ⇒ 残差化可增益）。**已修正旧记忆与 eur-institutions6 档案。**
2. **★ 跨区配方不可搬运（第三次实证）**：in6 三族口径（USA 28 赞）在 GBR 10 臂全灭；insiders 文献方向（US）在 GBR/UK 全负。
3. **★ 有界评分型字段的轴选择反向**：imb5_score（0–1）在 **sector（粗轴）** 优于 subindustry（细轴），与「轴越细 S 越高」的既有 GBR 结论相反——按字段类型分辨，不跨族外推。
4. **★ 同腿变体识别必用互相关**：0mPxKx1K 与 Xgaab3nz 表达式不同（ts_zscore vs ts_av_diff、不同 decay/truncation）但互相关 0.9049 ⇒ 同腿。**同族已 ACTIVE 件会锁死所有变体**（RRemlnRz/akaKQjQx self 0.999）。
5. **队列事实**：GBR multi-sim 端到端 5–15 分钟（本会话实测，p75 以上），两批并行时第二批排队更久；**在飞 ≤2 是正确节奏**（2026-11-21 用户最新约束：并发 = 2）。
6. **六法全字段成本**：7 字段 × 2 批（法1 + 聚合变体）可完成覆盖裁决；VECTOR 必须 `vec_*` 折叠。
7. **★ PV 禁令（2026-11-21 用户明令，GBR）**：PV 不得与其它数据集组腿（含 `multiply(signal, ts_rank(volume,66))` 加权门控）；判据 = `pyramids.effective>1` 且 list 含 `GBR/D1/PV` ⇒ 出局。imb5 四颗全闸件全部因此出局。
8. **★ PV-free 重建揭示 prod 墙的真实结构**：`imb5_score` αC 1962/uC 770，公开池大量同族变体 ⇒ 裸 score 几何 prod 0.72–0.79；PV volume 门控原本是 prod 稀释器（0mPPVEoK 0.6865）。**同集分散器 `imb5_mktcap` 否证（S 崩 0.57–0.69）**。
9. **★ 去相关杠杆排序（imb5 实测）**：**窗口（N≥250 把对 ACTIVE 的 self 从 0.71 压到 0.57）> 中性化档（INDUSTRY 进一步压到 0.44）>> 内核替换（全部 0.76–0.82，反向）**；但 **窗口与 prod 反向**（N=504 prod 0.79 > N=126 0.72）⇒ self 与 prod 需分杠杆解决。
10. **★ 混塔只产出一个后就换模板（2026-11-21 用户明令）**：`effective≥2` 的混塔模板产出 1 颗即封口，不再做同模板变体/第二席；改换新模板（新机制/新数据集/新塔）。单塔（effective=1）ATOM 模板不受限。
11. **★ 梯度「全类别」的实证价值（fhp 案例）**：L4 外层全替在 fhp 上找到 +0.21 的单层增益（`group_scale`），L5 decay8 再 +0.17 ⇒ 若不按全类别扫，会错记「天花板 0.32」；但起点太低（L1 最强 0.22），最终仍只到 0.70 ⇒ **梯度救结构不救弱信号**。

---

## 八、交付物清单

| 交付物 | 路径 |
|---|---|
| 本报告 | `output_report/GBR_campaign_20261121.md` |
| insiders12 画像（全 7 字段 + 六法 + 10 臂实证） | `tracking/GBR/reference/datasets/insiders12.md` |
| institutions6 画像（全 11 字段 + 三族口径 + 10 臂） | `tracking/GBR/reference/datasets/institutions6.md` |
| imbalance5 画像（全 2 字段 + 梯度 Δ 表 + 全闸件） | `tracking/GBR/reference/datasets/imbalance5.md` |
| fund_holdings_panel 完整梯度档案（5 层 53 臂 + 数据窗口体检 + GRADIENT_DONE） | `tracking/GBR/waves/wave20261121_gradient_fund_holdings_panel.md` |
| 既有画像（复核） | `tracking/GBR/reference/datasets/institutions25.md`、`risk68.md` |
| GBR skill 新规（PV 禁止组腿，3d） | `Claude/skills/wq-brain-ra-gbr/SKILL.md` |
| 全闸候选 | **0 颗（终判）**：PV-free 最优件 `2r5XKm65`（S2.04/F1.51/2Y1.74/TO14.9%/RA0/self 0.4427 PASS）终验 **prod 0.8266 FAIL**；同族三点 prod 实测定性结构性墙 |

---

## 九、建议下一步

1. **用户确认后，提交 `2r5XKm65`**（前提：prod 实测 <0.70）⇒ imbalance 塔 **2/3**，多塔乘数 +1.0；与已 ACTIVE 的 `0mPPVEoK` 互相关 0.4427，可同篮。
2. **imb5 第二席已用尽**：同数据集其余几何（`YPaEAMzA`）与 `2r5XKm65` 互相关 0.9123（同腿），不得再作第二颗；第三席需新机制。
3. 近墙三颗（A1xeOeoE / d5amYQZJ / A1VArNzY）全部含 PV 腿或已点亮塔 ⇒ **按 PV 禁令与新规搁置**。
4. 若要继续 GBR 新增产能：只能换**新数据集面**（等平台 onboard）或转 **SUPER alpha**（塔位按 selection 计，现有 SUPER 已 5 颗 ACTIVE）。
5. fhp（fund_holdings_panel）已完成完整梯度复核（天花板 S0.70）⇒ **维持死键，不再投入**。