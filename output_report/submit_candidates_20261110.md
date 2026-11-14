# 值得提交候选因子名单（2026-11-10 16:20 GMT+8）

> **ET 日 2026-11-10 03:23｜REGULAR 配额 0/4（剩 4）｜SUPER 0/1**
> 零提交。本表是筛选结论，不是提交授权。

## 筛选口径

| 条件 | 阈值 |
|---|---|
| 平台状态 | ≠ ACTIVE / SUPERSEDED |
| RA 形态 | S ≥ 1.58、F ≥ 1.0、平台 checks 0 FAIL |
| prod | 平台实测（`check_correlation` / `prod_peek` / `platform_sync`）、48h 内、< 0.68（留余量） |
| ΔSharpe | 预检实测 ≥ 0（**硬闸，force 不豁免**） |
| 稳健性台账 | ≠ REJECT（REJECT 优先于一切指标） |
| 塔信息 | 每颗必带「塔归属 → 当季计数 → 交后计数 → 是否新点亮 → 塔边际」 |

本地池扫描 65 颗 48h 内 prod 有效候选 → 批量拉 `is.checks[MATCHES_PYRAMID]` 算塔边际 → 18 颗能点亮新塔 → 剔除 REJECT / FAIL / 同席 → **A 档 4 颗**。

原始产物：`results/submit_pool_towers_20261110.json`、`results/submit_pool_ranked_20261110.json`。

---

## A 档 · 今日建议组合（点亮 3 座新塔 + 1 颗正交压舱）

| # | alpha | 区 | 塔归属 → 交后计数 | **新点亮** | prod（余量） | self | ΔS | 稳健 | 提交前待办 |
|---|---|---|---|---|---|---|---|---|---|
| **1** | **78Yk8VR1**（op-min 交付件，替代 E569ZE7L） | DEU | SHORTINTEREST ×1.3：**2→3** | **+1** | **0.5444（.1556）** | 0.5444 | **+0.06** | CONDITIONAL ✅ | prod 为恒等继承值，真交前 `refresh=True` |
| **2** | **E5QZ1NgJ**（op-min 交付件，替代 QPvx8M1W） | KOR | RISK ×1.3：**2→3** ＋ ANALYST ×1.6：3→4 | **+1** | **0.6192（.0808）** | 0.5927 | **+0.34** | **PASS** ✅ | **无（全项闭环，可直接点名提交）** |
| **3** | **omEdka3v** | GBR | OTHER：**2→3** ＋ SHORTINTEREST 4→5 | **+1** | 0.6026（.0974） | 0.4164 | **+0.26** | **PASS** ✅ | 答 2 腿三问 |
| **4** | **6XdkW08J** | GBR | SHORTINTEREST 4→5 ＋ MODEL 6→7 | 0 | 0.6267（.0733） | 0.3398 | **+0.23** | **PASS** ✅ | 答 2 腿三问；与 #3 互相关仅 0.153 |

> **17:45 闭环状态**：4 颗稳健性台账全部落库（`reports/robustness_20261110.md` §17:40 补审）。#2 的 prod 已 17:18 实测入权威表、稳健独立重审 PASS ⇒ **A 档唯一零待办件**。

**关键指标补充**

| alpha | S | F | 2Y 或 ladder / 限 | subU / 限 | TO | margin | ops |
|---|---|---|---|---|---|---|---|
| **78Yk8VR1** | 1.68 | 1.21 | LOW_2Y 2.27 / 1.58 | 0.86 / 0.80 | 11.3% | 11.47bp | **10** |
| **E5QZ1NgJ** | **1.86** | **1.74** | ladder 2.19 / 2.02 | 1.81 / 1.07 | 12.7% | 17.55bp | **6** |
| omEdka3v | 2.51 | 1.40 | ladder 2.37 / 2.02 | 2.46 / 1.19 | 28.2% | 6.25bp | 8 |
| 6XdkW08J | **2.60** | **1.95** | ladder 2.55 / 2.02 | 2.12 / 1.23 | 14.8% | 11.27bp | 8 |

**为什么这 4 颗（17:45 更新为最终 id）**
- **#1 78Yk8VR1**：全场 prod/self 双余量最厚（.1556），单数据集 ATOM 免三问，10 ops（原 12）；CONDITIONAL 根因已查明 = 2021 年德国借券市场无波动，非选样过拟合，且逐年与基线逐位相同 ⇒ `robustness_78Yk8VR1` 已落库。
- **#2 E5QZ1NgJ**：prod 余量从 .0313 扩到 **.0808**、S/F/ladder/sub/CLUSTER 全面优于原件、6 ops、免三问、独立重审 **PASS**（CV 0.247）⇒ **零待办**。
- **#3 omEdka3v**：GBR other 只差一颗；ΔS +0.26、self 0.416、稳健 PASS（CV 0.269），与 #4 互相关 0.153 ⇒ 两颗可同日并交。软标记：2023 Sharpe 由 3.09 降至 1.54、单年 margin 3.87bp。
- **#4 6XdkW08J**：塔边际 0，但指标最强（S2.60/F1.95）、**稳健 CV 0.057 全场最稳**、prod 余量 .073、ΔS +0.23、与 #3 正交 ⇒ 第 4 席压舱件。

**ΔS 分区提醒**：#1 是 `EQUITY:DEU:1`，#2 是 `EQUITY:KOR:1:POWER_POOL`，#3/#4 是 `EQUITY:GBR:1:POWER_POOL`。按铁律只能各自看符号，**禁止横比数值**。

---

## B 档 · 同席替代（不可与 A 档并交）

| alpha | 区 | 塔归属 → 交后计数 | 塔边际 | prod（余量） | self | ΔS | 稳健 | 不能并交 / 降级原因 |
|---|---|---|---|---|---|---|---|---|
| **RREPm361** | DEU | ANALYST ×1.8：6→7（已亮） | 0 | 0.6881（.0119） | **0.3275** | **+0.73** | **PASS**（CV .322） | 塔边际 0、需 2 腿三问；但**全面优于 1YNMAA8M**，是 B 档第一顺位 |
| kqNAz9pP | DEU | SHORTINTEREST 2→3 | **+1** | 0.5154 | 0.5071 | +0.06 | NO_RECORD | 与 E569ZE7L 互相关 **0.7368**（同席）。仅作 #1 备胎 |
| qMLJjleO | GBR | OTHER 2→3 | **+1** | 0.6574 | 0.2288 | +0.11 | NO_RECORD | 与 omEdka3v 互相关 0.158（异席），但 #3 交完 other 已亮 ⇒ 塔边际归零；可作 #4 替代 |
| j2Y7qlA5 / 9qxnNkeq / RREwqrNa | DEU | SHORTINTEREST 2→3 | **+1** | .53–.67 | — | 未测 | 9qxnNkeq REJECT | 与 E569ZE7L 互相关 0.35–0.93 |
| ZYQv7j2Q / 58EdlON6 / LLM0ePj2 / O0AX7Zw1 / zq3nNGp8 | GBR | OTHER 2→3 | **+1** | .62–.66 | — | 部分 + | 未审 | 同一 `loaned_share_*` 族，互相关 **0.50–0.9485**，只能选 1 颗 |
| **1YNMAA8M** | DEU | MODEL 3→4 / ANALYST 6→7 | 0 | 0.6951（.0049） | **0.6946** | +0.43 | PASS | **已被 RREPm361 取代**：prod/self 双贴线、S 1.58 贴线、8 ops、与已 ACTIVE 的 bl6AvMkN 互相关 0.5128 |
| rKRx7v6m | EUR | SENTIMENT 3→4 / OTHER 3→4 | 0 | 0.6756 | 0.4279 | +0.39 | NO_RECORD | 塔边际 0、与今晨已提交的 0mY1QPEv 同源；需补审 + 三问 |

**RREPm361 vs 1YNMAA8M（同为 DEU、塔边际同为 0、同需三问）**

| 项 | **RREPm361** | 1YNMAA8M |
|---|---|---|
| 算子 | **5** | 8 |
| S / F | **2.02** / 1.25 | 1.58 / 1.36 |
| self | **0.3275** | 0.6946 |
| prod 余量 | **.0119** | .0049 |
| ΔS（`:1:POWER_POOL`） | **+0.73**（1.73→2.46） | +0.43 |
| 稳健 | PASS（CV **.322**、近三年均值 2.19、无负年） | PASS（末段三年单调降 2.96→2.19→1.25） |

⇒ 六项全胜。**若第 4 席不想给零塔增量的 `6XdkW08J`，首选换 `RREPm361`；`1YNMAA8M` 降为次次备胎。** 唯一共同短板：DEU/D1 的 ANALYST 已 6 颗（lit），交进去塔维度零收益。

---

## C 档 · 明确排除

| alpha | 原因 |
|---|---|
| mL617YPx（EUR PV 2→3） | 稳健台账 **REJECT**（台账优先于一切指标） |
| 9qxnNkeq（DEU SHORTINTEREST 2→3） | 稳健台账 **REJECT** |
| gJe2a8wJ（GBR） | 平台 `CONCENTRATED_WEIGHT` FAIL |
| KPJ1rG0j / leAnKOEA / P0oR7vYw（EUR 四颗截图） | ΔS −0.07 / −0.02 / −0.02，**硬闸阻断、无豁免入口** |
| 截图 EUR 四颗中的 INSIDER 标签 | 平台 `get_datasets` 实查 insider_matrix category = **other**，实为 OTHER+OTHER 组腿违规 |
| 已 ACTIVE：zq3eb7No、bl6AvMkN、0mY1QPEv | 不可重复提交 |

---

## 塔布局与后续方向

**当季计数（15:49 实测）**

| 区 | 已点亮（≥3） | 差 1 颗（=2） | 真空（0–1） |
|---|---|---|---|
| EUR/D1 | analyst 10、model 3、fundamental 3、imbalance 3、**sentiment 3、other 3**（今晨 0mY1QPEv 点亮） | **risk 2、insiders 2、pv 2** | news 1；earnings/institutions/socialmedia/macro 0 |
| DEU/D1 | analyst 6、model 3 | **shortinterest 2**（A 档 #1 补） | other 2、sentiment 1、fundamental 1、institutions 1；其余 0 |
| GBR/D1 | model 6、shortinterest 4、pv 4、analyst 3、fundamental 3、news 3 | **other 2**（A 档 #3 补） | risk/sentiment/institutions/insiders/earnings/option/socialmedia/macro/imbalance 全 0 |
| KOR/D1 | analyst 3、fundamental 3、model 3、shortinterest 4 | **risk 2**（A 档 #2 补）、pv 2 | insiders 1、other 1；其余 0 |

**下一轮该挖什么**：今天 A 档交完，DEU shortinterest / KOR risk / GBR other 三座都会亮。剩余性价比最高的空位 = **EUR risk、insiders、pv 各差一颗**（当前干净候选只有被 REJECT 的 mL617YPx，需新挖），以及 **GBR/D1 九座全 0 真空塔**（Xg9dPpp0 / 9qxNbxJx / npvEe7ra / rKRx0M2m 这批能把 GBR risk 从 0 推到 1，但要攒够 3 颗才亮）。

---

# 附：E569ZE7L 的 CONDITIONAL 能否修复？（16:30 结论）

## 结论：**不需要修，也不建议修**

`CONDITIONAL` 在提交链里是 **fail-open**：`submit_verdict` 读到它不改判、只在 `next_step` 提示；`workflow_submit_alpha` 的 `submit_gate` 只拦 **REJECT**。实测 16:18 预检 `E569ZE7L` 的 `submit_gate.passed=true / blocked=false / robustness.verdict=CONDITIONAL` ⇒ **这颗现在就能交**。

它是 A 档 #1，且优势全在「这颗身上」：prod .5444 / self .5444 双余量 .1556、单数据集 ATOM 免三问、DEU/D1/SHORTINTEREST 2→3 点亮新塔、ΔS +0.06。任何修复都等于换件，这些要全部重测。

## 若仍要把它升到 PASS：量化门槛

Recent-3yr = **[0.55, 2.64, 1.88]**（2021/22/23），均值 1.690、总体 sd 0.864 ⇒ **CV 0.511**、**max/min 4.80**。要同时进 PASS 带（CV < 0.40 且 max/min ≤ 3）：

- 唯一解是把 **2021 从 0.55 抬到 ≥ 0.88（+60%）**：此时 CV ≈ 0.400、max/min ≈ 3.00，刚好压线；
- 压 2022 无效（把 2.64 降到 1.65 后 CV 仍 0.427，落 CONDITIONAL）；
- ⇒ **必须让 2021 单年变强，且不能让 2022 明显变弱**。

而实测所有变体的 2021 **只降不升**（0.18 ~ 0.55），方向与门槛相反。

## 为什么在原信息源内已证伪（四层修复阶梯走到第 4 档）

| 档 | 已做 | 结果 |
|---|---|---|
| 1 · 换字段（L1 信息源） | 波 AF：借券费率 / 费率波动 / 出借股数 / 贷款久期 / 交易笔数 10 条 | `E569Xd91` 与 E569ZE7L 互相关 **0.7095 超线**；费率腿 2021 为 **−0.07 负年** |
| 2 · 换组合算子（L2） | 波 AI 乘积 → AJ/AK/AL 加法/乘法 → AM 差值 | 差值结构确实把 2021 从 −0.09 救到 **+0.18~0.25**，但另一年弱值浮出 ⇒ max/min **7.83~14.28**，全部 REJECT |
| 3 · 换轴 / 窗口 / tvr（L3+L4） | **repair 第 1 轮 Wave X：10 个变体**（market/country 轴、backfill 264/504/66、第二窗口 66/88、target_tvr 0.02/0.04） | **全部 REJECT**；2021 更差 0.18~0.46，max/min 恶化到 **7.65~15.22**。基线 264/132 + subindustry 是族内唯一 max/min<5 的结构 |
| 4 · 2021 短窗口专项 | 波 AN 10 条（132/66、66/44、88/44、132/88、66/22…），sim `3j6Xeb1kz4WTbu232ZcS8po` | **仍在平台队列 progress 0.1（全局拥堵），未回收** ⇒ 按「停摆勿判死」留待下次，但前 3 档全灭使先验很低 |
| 5 · 放宽闸 | 仅用户明确指令 | 不需要（见上） |

**根因**：2021 年德国借券市场几无波动，借券评级变化信号当年信息量不足。这是**数据环境特性**，不是选样或结构问题 —— 表达式四层里 L2/L3/L4 已穷尽，L1 同源字段也全撞 2021 或互相关超线。

## 唯一还开着的路 = 换信息源补 2021（等于新挖，不是修这颗）

`PROBE6_VERDICT_20261110.md` 探针：**`6Xd5zoQP`（analyst10 创新分）2021 年 S = 3.11**，恰好补借券族共同弱年；`9qxNJdOq`（sentiment33）2023 年 S=2.32 补费率腿失效年。

代价：① 变成组合腿，违反「生成端禁加权混信号 / 只认三形态」；② 塔归属从 SHORTINTEREST 单塔 ATOM 变成多塔，**2→3 的点亮不再保证**；③ prod / self / ΔS / 互相关 / 稳健性全部重跑。**这是一颗新 alpha，不是 E569ZE7L 的修复版。**

⇒ **建议：直接交 E569ZE7L，把「2021 弱年」作为已查明的 soft_flag 写进三段式 description 留审计痕迹**，这符合 skill Phase D 第 3 条「PASS 带 CONDITIONAL 软标记要如实带上」。

---

# 附二：A 档 #1 的 op-min 替换（17:05）

**`E569ZE7L` → `78Yk8VR1`：算子 12 → 10，零损失。**

```text
a = ts_backfill(vec_avg(shrt3_bar), 132);
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(a,264)), rank(ts_delta(a,132))), target_tvr=0.03), subindustry)
```

`ts_backfill(vec_avg(shrt3_bar),132)` 在原式里重复 2 次 ⇒ FASTEXPR 变量赋值合并（赋值本身不计数）省 2 个调用点。实测 **S/F/TO/margin/sub/2Y/CLUSTER 逐位相同、逐年 [0.55, 2.64, 1.88] 逐位相同、塔归属 DEU/D1/SHORTINTEREST ×1.3 相同** ⇒ prod .5444 / self .5444 / ΔS +0.06 / 稳健 CONDITIONAL 全部继承。按「算子数 = 硬指标」，**A 档 #1 改用 `78Yk8VR1`**。

**7 算子件 `KPgKPRAx` 不采纳**：删第二窗口腿后 IS checks 8 项全 PASS、S1.62 / F1.14 / sub .89 / 2Y 2.28、ΔS +0.64、免三问，看着更优；但**逐年 2021 从 0.55 塌到 0.18 ⇒ max/min 14.28（REJECT 档）**，self 升到 0.5627，prod 未测。⇒ 只看 IS checks 会误采纳，压缩件必须同时查逐年。

**10 ops 是「不恶化 2021」前提下的下限**：批 1 十个删除/替换通道中，删 tvr_decay → F/sub 双 FAIL；删单侧 rank → WARNING 或 FAIL；删 backfill → S1.49 + CW FAIL；删 group_rank → S1.12；`rank→zscore` → S.82 全崩；`group_rank→group_zscore` → 三 FAIL；`vec_avg→vec_sum` 指标几乎相同但 2021 更差（.49）且不省算子 ⇒ 全部回滚。

**未回收**：decay 2 / 8 设置收敛两批（`AJXdXfyt4gRc5T7I7PWZhx`、`1OawvJfuQ56W95URo2cTVwW`）平台队列 0/0 terminal 停摆；`78Yk8VR1` 的 prod peek 持续空体。按「停摆勿判死」留待下次，不影响定案（信号逐位相同）。

---

# 附三：A 档 #2 的 op-min 替换（17:35）

**`QPvx8M1W` → `E5QZ1NgJ`：算子 7 → 6，prod 余量放大 2.6 倍。**

```text
group_neutralize(subtract(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,300),sector),
                          group_rank(ts_delta(rsk68_weight_dadv,66),sector)), industry)
```

改法只有一处：**删掉 `hump(..., hump=0.003)` 限速器**。实测：

| 项 | QPvx8M1W（原） | **E5QZ1NgJ（交付）** |
|---|---|---|
| 算子 | 7 | **6** |
| S / F | 1.67 / 1.54 | **1.86 / 1.74** |
| IS_LADDER / 限 | **2.02 / 2.02（零余量）** | **2.19 / 2.02** |
| sub / CLUSTER | 1.64 / 1.28 | **1.81 / 1.49** |
| **prod（余量）** | 0.6687（.0313） | **0.6192（.0808）** |
| self | 0.6447 | **0.5927** |
| ΔS（`:1:POWER_POOL`） | +0.28 | **+0.34** |
| 塔 | RISK + ANALYST | **不变，RISK 2→3 仍点亮** |

prod 17:18 实测已入 `alpha_corr_cache`（`prod_peek`）。命中 skill ④b「prod 贴线时低 prod 变体优先」；同时印证 `hump` 限速器在累积型信号上零和（降 TO 的同时削 alpha）。

**5 算子件 `xAvK6b0q` 待验**：再删 `group_neutralize`，S1.78 / F1.73 / **ladder 2.29** / CLUSTER 1.55 全 PASS、self .5654、ΔS +0.33、塔不变、免三问；但 prod peek 连测三轮空体（平台仍在算）⇒ 按「压缩变体必须复检 prod」暂不采纳，出数后若更低则按算子数硬指标升级。

**★ 3 算子件 `P05JWgdw` 判死**：删 risk 腿后只剩 3 算子、全闸 PASS（S1.79 / 2Y1.69），但**塔只剩 KOR/D1/ANALYST ⇒ RISK 2→3 点不亮，塔边际 +1→0**。压缩必须回查塔归属，不能只看 ops 与 IS checks。

**两批 20 条其余结论**：`ts_av_diff→ts_zscore` S1.49 WARN；`ts_ir` 全崩；`ts_delta→ts_zscore` (`j2a5vodk`) 与 252 窗 (`RReJ36Wa`) 全 PASS 但不省算子且 prod 未测；删左 `group_rank`、删 `subtract→add` 全崩（**极性承重**）；`ts_delta` 126/21 窗口均 ladder WARN；subindustry 轴 ladder 退化。

**待闭环**：`xAvK6b0q` / `RReJ36Wa` / `j2a5vodk` 的 prod；所有压缩件的 `robustness_<id>` 仍是 NO_RECORD（基线 PASS 不可继承，提交前须补审）。

---

# 附四：闭环总账（17:45）

| 项 | 原状态 | 闭环结果 |
|---|---|---|
| E569ZE7L 的 decay 2/8 批次 | 0/0 terminal「停摆」 | **假停摆**。`batch_status.py` 按 multisim children 计数，单条仿真 children=0 被误读成 0/0；原始 `/simulations/{id}` 实为 `status=COMPLETE` + `alpha` 字段。已回收 `wpo8KX0v`(d2) / `3q0MQYq0`(d8)：三档 S/F 逐位相同、CV 0.511/0.514/0.513 全落同一 CONDITIONAL 带 ⇒ **decay 零杠杆，保持 d4**。 |
| DEU 波 AN（2021 短窗口专项） | 平台队列 | **仍未回收**：`/simulations/3j6Xeb1kz4WTbu232ZcS8po` 返回 `progress=0.1` + `Retry-After: 5`，无 children ⇒ 确实在算。按「停摆勿判死」留待下次；前 3 档修复阶梯全灭，先验低。 |
| `78Yk8VR1` prod | peek 空体 | **18:15 实读闭环**：平台恢复后 peek 第 4 次出数 **0.5444**，与恒等继承预测逐位相同；已用 `CampaignStore.set_corr_cache` 入权威表（`prod_peek` @18:15:29）。提交时 `prod_gate` 命中缓存放行，提交后 `prod_snapshot` 平台冻结值 0.5444、delta 0.0。 |
| `E5QZ1NgJ` prod | 已实测 | **闭环**：0.6192 @17:18:36 已入 `alpha_corr_cache`（`prod_peek`）。 |
| `xAvK6b0q` / `RReJ36Wa` / `j2a5vodk` prod | 待验 | **平台侧阻塞，不判死**：peek 三轮空体；`check_correlation` 对 xAvK6b0q 轮询 187s 返回 `pending / inflight=true / last_known=null`（16 次尝试）。工具明示 inflight 时不得重新触发，否则顶成 busy。留待平台恢复。 |
| 4 颗 A 档稳健性台账 | NO_RECORD / 待补 | **全部落库**：`DEU/robustness_78Yk8VR1`=CONDITIONAL（恒等继承）、`KOR/robustness_E5QZ1NgJ`=**PASS**(CV .247)、`KOR/robustness_xAvK6b0q`=PASS(CV .280，带 prod 未闭环 soft_flag)、`GBR/robustness_omEdka3v`=PASS(CV .269)、`GBR/robustness_6XdkW08J`=**PASS**(CV .057 全场最稳)。报告见 `reports/robustness_20261110.md` §17:40。 |
| A 档提交前待办 | 4 颗均需补件 | **#2 零待办**；#1 仅 `refresh=True`；#3/#4 仅答 2 腿三问。 |

**仍开着的口子（唯一）**：`xAvK6b0q`（5 ops）的 prod。若出数且 < 0.6192，按「算子数=硬指标」升级为 A 档 #2 交付件；当前维持 `E5QZ1NgJ`。

**工程坑（已记入记忆）**：`tools/prod_peek_ingest.py` 迁至 `tools/probe/prod_peek_ingest.py`（需 `PYTHONPATH=src`，产物路径解析成 `tools/results/`）；改用 `wqb.store.CampaignStore.set_corr_cache(...)` 直接写更稳。KOR/GBR 新 alpha 的 REST `/recordsets/yearly-stats` 会返回非 JSON，改用 MCP `get_alpha_yearly_stats` 可正常取回。

---

# 附五：18:17 已提交 A 档前两颗（用户点名）

| # | alpha | 名称 | 区 | 状态 | dateSubmitted（ET） | prod 闸 / 平台冻结值 | 塔边际兑现 |
|---|---|---|---|---|---|---|---|
| 1 | **`78Yk8VR1`** | `DEU_R_shrt3accel_01` | DEU | **ACTIVE** | 2026-11-10T05:16:33-05:00 | 0.5444 / 0.5444（delta 0.0） | **DEU/D1/SHORTINTEREST 2→3 点亮** ✅ |
| 2 | **`E5QZ1NgJ`** | `KOR_R_anl10rsk68_01` | KOR | **ACTIVE** | 2026-11-10T05:13:53-05:00 | 0.6192 / 0.6192（delta 0.0） | **KOR/D1/RISK 2→3 点亮** ✅；ANALYST 3→4 |

两颗均走 `201 async_accepted → verify ACTIVE`（异步受理分支，非失败）。POST 响应 201，`prod_snapshot` 闸门读数与平台冻结值逐位一致。

**提交前闸全过**：`submit_gate` 0 FAIL、`mix_audit kind=none` 免三问、`quota_gate` ET 11-10 0/4、`prod_gate` 命中 48h 内权威缓存（非 provisional）、`ΔS` 分别 +0.06（`:1`）/ +0.34（`:1:POWER_POOL`）、稳健性台账 CONDITIONAL / PASS 均已落库。

**属性**：color BLUE；tags `CH_REG` + `SRC_shrt3` / `SRC_anl10`+`SRC_rsk68` + `W20261110`；三段式 description 各 ≥100 词。#1 的第三段按要求如实带上 2021 弱年（recent3 0.55/2.64/1.88、CV .511、max/min 4.80、8 个窗口变体同年退化）作为审计痕迹。平台未追加 `PowerPoolSelected`。

**塔计数复核（提交后实测）**：DEU/D1 `shortinterest 3`（lit）、`analyst 6`、`model 3`；KOR/D1 `risk 3`（lit）、`analyst 4`、`shortinterest 4`、`pv 2`。**两颗合计点亮 2 座新塔**。

**本地库对齐**：`alphas.status` 由 harvest 留下的 UNSUBMITTED 手工改为 ACTIVE 并回填 prod；`submission_ledger` 补写两条 ACTIVE 记录。

**配额**：ET 2026-11-10 REGULAR 尚余 2 位（`#3 omEdka3v` / `#4 6XdkW08J` 仅需答 2 腿三问即可提交）。
