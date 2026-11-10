# 2026-11-09 候选因子总清单 · 可提交排序

> 生成时间：2026-11-09 22:5x CST（= ET 11-09 09:5x）  
> 口径：只挖不提交（`ALLOW_ALPHA_SUBMIT=False`），提交权归用户点名。  
> 判据链：台账 → 混腿 → RA → prod → ΔS → 分散度 → 稳健逐年 → 塔 → 配额 → 用户点名。  
> 实时复核：本次重查了 6 颗关键候选的 prod 缓存时龄与 3 颗台账，数据为最新。

---

## 0 一句话结论

**今日你点名/贴图的候选去重共 40 颗；ET 11-09 REGULAR 已用 2/4（`P0obGoQJ`、`akK9ooZv`），剩 2；SUPER 0/1。**

**严格按现行判据：0 颗可以「零动作直接提交」**——不是因为全被否决，而是今天两颗新提交进池后，QPvx8M1W  
所有 prod 读数都必须在提交那一颗时 `refresh=True` 终验；另有 3 颗稳健真审结论还没写进台账。  
但按「放行所需动作」分层，**前 5 颗无需任何判据豁免**，只差标准前置动作。

---

## 1 主排序表（可行动清单）

**放行档**：`A` = 无需豁免，只需标准前置（prod 终验 / 台账补登 / 三问）  
`B` = 需你明确豁免 1 道闸（CV 稳健闸）  
`C` = 需你改明令判据（ΔS 硬闸）或多道豁免  
`X` = 判死，不再考虑

|     # | id             | 区 / 塔动作                     |                ΔS | prod（余量 / 时龄）                   |     self | 稳健台账                                              | 档     | 放行前置动作                                                 | 点亮新塔 |
| ----: | -------------- | --------------------------- | ----------------: | ------------------------------- | -------: | ------------------------------------------------- | ----- | ------------------------------------------------------ | ---- |
| **1** | **`P0oolrZq`** | GLB / RISK 1→2              |         **+0.69** | **.6578**（.0422 / **31.7h 有效**） |     .568 | 真审 **PASS** CV.309；台账 `NO_RECORD` 需补登             | **A** | ① prod `refresh=True` 终验 ② 补登 PASS 台账                  | ❌    |
| **2** | **`vR11NmNr`** | IND / INSTITUTIONS 1→2      |             +0.35 | .674（**101.6h stale 作废**）       |     .663 | 真审 **PASS** CV.270（全场最稳、10/10 正年）；`NO_RECORD` 需补登 | **A** | ① prod 终验**必须成功** ② 补登台账                               | ❌    |
| **3** | **`RREPm361`** | DEU / ANALYST 5→6（已亮，零贡献）   |      +0.73（PP 分区） | **.6881**（.0119 / **24.7h 有效**） | **.328** | 真审 CONDITIONAL（末段 −43%）；`NO_RECORD` 需补登           | **A** | ① prod 终验 ② 补登 ③ 三问（two_leg）④ 重测 ΔS                    | ❌    |
| **4** | **`omERn83n`** | KOR / **RISK 2→3**          |             +0.10 | .6898（**77.7h stale 作废**）       |     .421 | CONDITIONAL CV.581 贴 0.60（已落库）                    | **A** | prod 终验必须成功                                            | ✅    |
| **5** | **`ZYQ116ln`** | KOR / **PV 2→3**            |             +0.24 | .6981（**余量 .0019** / 33.2h 有效）  | **.143** | CONDITIONAL CV.459（已落库）                           | **A** | prod 终验（余量太薄，**大概率 FAIL**）                             | ✅    |
|     6 | `akKGqOmx`     | KOR / **RISK 2→3**          |             +0.42 | .5459（**48.9h 刚过期**）            | **.155** | **REJECT** CV.804（2021 平年 0.01）                   | **B** | 豁免 CV 闸 + prod 终验 + 落 REJECT 台账                        | ✅    |
|     7 | `RREwqrNa`     | DEU / **SHORTINTEREST 2→3** | +0.08（历史，**须重测**） | .6684（.0316 / 22.3h）            | **.263** | **REJECT** CV .677–.829                           | **B** | 豁免 CV 闸（**57 种结构已证不可修**）+ 重测 ΔS + prod 终验              | ✅    |
|     8 | `mL617YPx`     | EUR / **PV 2→3**            |        0.000（零贡献） | .5421（**.1579 余量最大**）           |     .450 | **REJECT** CV.641（2 轮 repair 16 变体同判）             | **B** | 豁免 CV（难度最高）+ 解释零 ΔS                                    | ✅    |
|     9 | `RREOz5qn`     | DEU / **MODEL 2→3**         |         **−0.02** | .5834（.1166 / 最新）               |     .584 | **PASS**                                          | **C** | **两道**：豁免 ΔS 硬闸（须改 11-08 明令判据）+ 分散度软闸                  | ✅    |
|    10 | `P0oR7vYw`     | EUR / **OTHER 2→3**         |         **−0.01** | .6881（.0119）                    |     .535 | **PASS** CV.232（10/10 正年）                         | **C** | 豁免 ΔS 硬闸 + prod 终验 + 三问                                | ✅    |
|    11 | `leAnKOEA`     | EUR / OTHER（与 10 同席 ρ.7837） |         **−0.01** | .6476 无权威值（终验挂起）                |     .462 | CONDITIONAL + CLUSTER 1.54 WARNING                | **C** | 同 10 + 补 prod 权威读数                                     | ✅    |
|    12 | `QPvzNNGG`     | DEU / SHORTINTEREST         |         **−0.05** | .6777（.0223）                    |     .678 | PASS CV.311                                       | **X** | ΔS 最负之一 + self 贴线；与 `RREOz5qn` ρ.8711 同席且各项更弱          |      |
|    13 | `N1NGbddg`     | EUR / INSTITUTIONS          |         **−0.10** | .6872（.0128）                    |     .660 | 含 2020 负年                                         | **X** | ΔS 最负 + 负年，硬闸                                          |      |
|    14 | `LLZ6wZO2`     | KOR / oth466                |            0.0000 | .6762                           |     .676 | 旧账                                                | **X** | 分散度 blocked（self≥.55 且 ΔS<+.02）                        |      |
|    15 | `qMLOooX1`     | KOR / analyst10             |             +0.23 | 79.7h stale                     |        — | **REJECT** max/min 5.30（2021→23 单调衰减）             | **X** | 台账 REJECT，`blocked=True`                               |      |
|    16 | `d5Wvpmbx`     | KOR / risk68                |    **+0.47 全池最强** | **.9081 FAIL**                  |        — | CONDITIONAL                                       | **X** | prod 硬闸（自家 `kqN92KpK` 进池把同族从 .6906 顶上来）                |      |
|    17 | `rKRRjM51`     | IND / PV                    |             +0.38 | 74.0h stale                     |     .652 | —                                                 | **X** | 与 `vR11NmNr` ρ **.9485** 同席，各项更弱                       |      |
|    18 | `A1VGKqOe`     | GLB / OTHER                 |             +0.53 | 97.6h stale                     |     .565 | —                                                 | **X** | 与 `P0oolrZq` ρ **.7622** 同席，各档弱一档                      |      |
|    19 | `LLMzYrZe`     | DEU                         |                 — | —                               |        — | CONDITIONAL                                       | **X** | 被 `QPvzNNGG` 支配（同席更弱）                                  |      |
|    20 | `leA5JeP7`     | EUR / insiders              |                 — | —                               |        — | —                                                 | **X** | **SUPERSEDED**：优化版 `9qxdnV72`（4 ops）已于 11-06 提交 ACTIVE |      |

> ΔS 只能**同分区内看符号**：#1–6、#14–18 多在 `EQUITY:XXX:1:POWER_POOL`（基准 1.73–3.56），  
> #9/#12 在 `DEU:1` 常规（3.30）、#10/#11/#13 在 `EUR:1` 常规（5.48）。**跨区横比大小无意义**。

---

## 2 与「优先点亮未点亮的塔」指令的冲突（需你终审）

你 11-09 明令优先点未亮的塔。按当季 ACTIVE 账复核，**A 档里只有 #4 / #5 能点亮**，  
而 B/C 档几乎颗颗能点亮——即「严守判据」与「塔优先」给出不同顺序：

| 排序依据         | 建议两颗                    | 点塔结果                                                             |
| ------------ | ----------------------- | ---------------------------------------------------------------- |
| **严守判据（推荐）** | `P0oolrZq` + `vR11NmNr` | 0 塔点亮（GLB/RISK 1→2、IND/INSTITUTIONS 1→2）                         |
| **塔优先（需容错）** | `omERn83n` + `ZYQ116ln` | **点亮 2 塔**（KOR/RISK、KOR/PV）；但两颗 prod 一个 stale、一个余量 .0019，终验失败风险高 |
| **塔优先（需豁免）** | `RREwqrNa` + `akKGqOmx` | **点亮 2 塔**（DEU/SHORTINTEREST、KOR/RISK）；需两道 CV 豁免                 |

塔账（当季 ACTIVE，非累计）：`ASI/OTHER` 已由 `P0obGoQJ` 点亮；`DEU/MODEL 2`、`DEU/SHORTINTEREST 2`、  
`KOR/PV 2`、`KOR/RISK 2`、`EUR/OTHER 2` 都差 1 颗点亮；`GLB/RISK 1`、`IND/INSTITUTIONS 1` 差 2 颗。

---

## 3 全量覆盖：你今天发来的 40 颗，逐批归属

| 批次                   |   颗数 | 清单                                                                                                             | 归属                                                                                                      |
| -------------------- | ---: | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| ① 10 颗 label 族       |   10 | `P0obGoQJ`★ `kqNMPNEk` `78LrnNK5` `9qx3NbLq` `vR1bvrez` `P0obZQpq` `ZYQ9Akn3` `WjORvn6d` `rKRwRjdj` `1YN0XrYX` | **1 颗已提交**（P0obGoQJ）；5 颗 CLUSTER_TEST 淘汰（1.55/1.43/1.45/0.92/0.83）；其余 4 颗同族 ρ .73–.996 锁死 ⇒ **9 颗永久出局** |
| ② 4 颗 DEU            |    4 | `QPvzNNGG` `RREwqrNa` `LLMzYrZe` `RREPm361`                                                                    | #12 / #7 / #19 / #3                                                                                     |
| ③ 7 颗 GBR·EUR        |    7 | `6XAe27eL` `Grge2lN3` `rKd5lAo8` `A1Q729Ll` `mL617YPx` `ZYAJZL93` `N1NGbddg`                                   | 前 3 颗**已 ACTIVE**；`A1Q729Ll`↔`e76xGOQO` ρ.9342、`ZYAJZL93`↔`786pLKnb` ρ.9717 同族锁死；余 #8 / #13             |
| ④ 截图 5 颗 GBR 网格      |    5 | `akK9ooZv` `88RxORpX` `ZYQv7j2Q` `O0AX7Zw1` `58EdlON6`                                                         | **1 颗已提交**（akK9ooZv）；其余 4 颗与它 ρ .68–.95 ⇒ **永久出局**                                                      |
| ⑤ op-min 单颗          |    1 | `leA5JeP7`                                                                                                     | #20 SUPERSEDED                                                                                          |
| ⑥ 截图 5 颗 GLB/IND/KOR |    5 | `P0oolrZq` `vR11NmNr` `akKGqOmx` `rKRRjM51` `A1VGKqOe`                                                         | #1 / #2 / #6 / #17 / #18                                                                                |
| ⑦ 截图 2 颗 EUR         |    2 | `P0oR7vYw` `leAnKOEA`                                                                                          | #10 / #11（后者截图首字母是小写 `l`）                                                                               |
| ⑧ 3 颗 DEU 复评         | +1 新 | `RREOz5qn`（另 2 颗重复）                                                                                            | #9                                                                                                      |
| ⑨ 截图 5 颗 KOR         |    5 | `d5Wvpmbx` `ZYQ116ln` `qMLOooX1` `omERn83n` `LLZ6wZO2`                                                         | #16 / #5 / #15 / #4 / #14（首颗截图大写 V，平台实为小写 v）                                                            |

**今日已提交（ET 11-09）**：`P0obGoQJ`（ASI，prod .5973 / ΔS +.730 / 点亮 ASI·OTHER）、  
`akK9ooZv`（GBR，prod .6282 / ΔS +.710 / 三问已答）。两颗 Step 5 prod 恒等式 Δ=0.0000。  
另 `3qompGeZ`（SUPER，GBR，S4.42/F4.27/prod .6221）在 11:25 点名提交，但 `dateSubmitted` 落在 **ET 11-08**，占的是昨天的 SUPER 配额。

---

## 4 建议执行（用掉剩余 2 配额）

**方案 A（严守判据，推荐）**：`P0oolrZq` → `vR11NmNr`

逐颗前置检查：

```
1. check_correlation(<id>, production, refresh=True)   # 终验；>0.7 立即放弃
2. 补登 robustness_<id> = PASS                        # 现为 NO_RECORD，真审结论在 robustness_20261109.md §18:3x
3. mcp_preflight_once.py <id>                          # 今日两颗进池后重测 ΔS，确认仍 ≥0
4. get_pyramid_alphas                                  # 复核塔账
5. 用户明确点名 → 提交
```

`P0oolrZq` 是唯一「prod 读数有效 + 余量 .042 + ΔS +.69 + CV .309 + mix none」五项齐全的，  
终验成功率最高，应占第 1 个配额。`vR11NmNr` 稳健最稳（CV .270、10/10 正年）但 prod 已 101.6h 作废，  
**当前账号级相关性槽 busy（retry ~144s），必须先等终验成功**。

**方案 B（塔优先）**：`omERn83n` + `ZYQ116ln` —— 能点亮 2 塔，但两颗 prod 都需终验，  
且 `ZYQ116ln` 余量仅 .0019，今日两颗新提交进池后大概率已过 0.7 ⇒ **不建议作为主方案**。

**方案 C（一道豁免换点塔）**：豁免 `RREwqrNa` 的 CV 闸。它是全场「一道豁免即可放行」且  
self .263 最低、塔 2→3 点亮；但 57 种结构已证 CV 不可修，且**豁免后必须重测 ΔS**（台账挡住时没算，  
今日两颗进池可能把 +.08 漂移成负）+ prod 终验。流程预设在  
`tracking/DEU/atom_orthogonal/submit_staging_RREwqrNa.json`。

---

## 5 五个高频误判（今天全部复现过）

| 误判                 | 正解                                                                                 |
| ------------------ | ---------------------------------------------------------------------------------- |
| 截图 Δ 为负就否          | 面板口径与平台**符号相反**，已两次复现（5 颗截图 −.08~−.20，平台 +.35~+.69）；必须 `performance_comparison` 复核 |
| prod 低 ⇒ ΔS 正      | 两个不同的池：prod 比**第三方**，ΔS 比**自己池**。`RREOz5qn` prod 最净 .5834 却 ΔS −.02                |
| ΔS 高 ⇒ 不拥挤         | `d5Wvpmbx` ΔS +.47 全池最强，prod **.9081 FAIL** 照样判死                                   |
| RA 全过 / 截图「就绪」⇒ 可提 | 截图只跑 submit_gate + ΔS，漏 prod / 台账 / 逐年；4 个「就绪」里 2 判死 2 待补                          |
| 标签「可点新塔」           | 只认 `get_pyramid_alphas` 当季 ACTIVE（按季度重置）；截图 5 颗全标可点塔，实际只有 1 颗能点                    |

另：截图 id 读错三次（`1`/`l`、`V`/`v`），凡是形近字符先试小写/数字变体。

---

## 6 附：今日派生但不在你点名清单内的候选

| 来源                              | id                                                                                                                                              | 状态                                                                                                                                                                                                                                                                    |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RREwqrNa` op-min 57 种结构        | `LLMv6joe`（15 ops 零损失）、`JjeAPgKj`（B 门控 CV .615 全场最佳）、`P0oRoRPJ`（14 ops IS 最好但 CV .838）、`npvjOZQz`、`zq3xP1LX`、`A1VpgM5l`、`P0oRXwzJ`、`kqNwL1Gk` 等 | 全部 **SUPERSEDED**；CV 上限 .615 仍 ≥.60，且 prod/self/ΔS 未测、与原件同族高相关 ⇒ 不宜换将                                                                                                                                                                                                 |
| KOR 非 ATOM 组合线                  | `QPvx8M1W`（PASS，ΔS +.28，self .645）、`E56jA0AP`（CONDITIONAL CV.428）、`9qxnYPjd`（PASS CV.322，优于母件）                                                  | 三颗均**欠 prod 读数**（账号级死锁），未提交；若要纳入排序需先补 prod                                                                                                                                                                                                                            |
| SA / SUPER 线                    | `N1NErpxo`（S4.55/F3.88/prod .6176）、`3qompGeZ`（已提交）、`A1VXlbgd`（prod .6938 余 .006）                                                                | 今日按 `S>4.5 & F>4.5 & prod<0.65` 新判据 **0 颗达标**；GBR 三角冲突已定量封死（F≥4.5 需 limit≥20 ⇒ prod .775）                                                                                                                                                                             |
| **补问 3 颗 EUR risk60**（23:1x 截图） | `qML2RxrZ` / `ZYQVJj8n` / `2rAVV7ew`（截图 id 有误：`zYQVJj8n`→`ZYQVJj8n`、`2rAWW7eW`→`2rAVV7ew`）                                                      | **判死，不进排序**：今天 14:4x EUR 挖掘战役已做过 IS 选优，但从未进提交评审链（台账全 `NO_RECORD`）。本次实测 prod **0.8608 / 0.8707 / 0.9156 全 FAIL**；互测 ρ .979–.995 ⇒ 三颗只有 1 席；`2rAVV7ew` 另有 `fRA=1`（LOW_SHARPE 1.56<1.58）。`qML2RxrZ` 稳健 CV .237 PASS 也救不了 prod。详见 `reports/robustness_20261109.md` §23:1x |

---

**留痕**：`reports/robustness_20261109.md`（§0–§9、§18:3x、§19:4x、§21:2x、KOR 21:53/22:32/22:34、§22:2x）、  
`output_report/opmin_rrewqrna_20261109.md`（补章 1–3）、`output_report/SA_triple_gate_S45_F45_P065_20261109.md`。  
**本清单未提交任何 alpha。**

---

## 更新（2026-11-10 02:2x CST）：第 3 颗已提交，配额剩 1

用户点名「提交」并定判据「同等绩效下算子越少越好是**硬指标**」⇒ 交付件取 7-ops 最优件 `rKRx2Alj`，不是 8-ops 原件。

| 项 | 值 |
|---|---|
| id / 名称 | `rKRx2Alj` / `DEU_R_anlrev3_01` |
| 状态 | **ACTIVE**，`stage=OS`，`dateSubmitted=2026-11-09T13:18:39-05:00` |
| 通道 | REGULAR / **RA**（`is_ppa=false`，非 PPA） |
| 算子 | **7**（平台 `regular.operatorCount`；`multiply` 变参 + `ts_sum`） |
| 指标 | S1.95 / F1.80 / 2Y2.23 / `IS_LADDER_SHARPE` PASS（2.23≥2.02）/ `failed_ra=0` |
| 相关性 | prod **0.6561**（闸门 = 平台冻结 `is.prodCorrelation`，Δ**0.0000**）/ self 0.5634 / ΔS **+0.68** |
| 塔 | `DEU/D1/MODEL`(1.8) + `DEU/D1/ANALYST`(1.8)，effective=2 |
| 台账 | `robustness_rKRx2Alj` = CONDITIONAL（近3 [3.07,2.30,1.29] CV .328；软标记 2023 末段衰减） |
| 混腿 / 标签 | `kind=none` 免三问；平台未挂 `PowerPoolSelected`（`disposition=absent`） |

提交链全步：`submit_gate passed` → `mix none` → `quota 2/4` → `prod 0.6561`（from_cache 02:09:45、`provisional=false`）→ `ΔS +0.68` → `diversity fail-open` → `set_properties`(7 ops) → POST **201** → verify **ACTIVE** → prod 快照 Δ0 → tag_disposal。
`refresh=True` 终验被账号级单并发槽挡回（holder `MPYEEwj8`，retry 240s），但 `last_known` 是 02:09:45 本轮**实算**值、age 0.14h、`stale=false`、`inflight=false` ⇒ 按纪律未重复触发，用该权威读数；Step 5 恒等式已验证诚实。

**同族处置**：`mLovbnm2`(8 ops) 与 `2rAYpJKx`(7 ops) 互相关≈1 ⇒ **SUPERSEDED，永久出局**。
`tracking/DEU/atom_orthogonal/submit_staging_rKRx2Alj.json` 已建；原 `submit_staging_mLovbnm2.json` 保留但失效。

**配额**：ET 11-09 REGULAR **3/4 已用、剩 1**（`P0obGoQJ` / `akK9ooZv` / `rKRx2Alj`）；SUPER 0/1。
剩余 1 个配额按原清单仍建议 `P0oolrZq`（A 档，需 prod 终验 + 补登 `robustness_P0oolrZq`）。

> 本文原尾部「本清单未提交任何 alpha」已由本节取代。
