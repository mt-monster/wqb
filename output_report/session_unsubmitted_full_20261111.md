# 会话全量未提交 Alpha 汇总与今日提交排序

**时间**：2026-11-11 10:37 GMT+8 / **ET 2026-11-10 21:38**（`wqb.timeutil` 实读）
**配额**：ET 11-10 REGULAR **3/4，剩 1 席**；SUPER **1/1 已满**（`QPv88bJW` 17:49 ET）
**重置**：GMT+8 **13:00**（ET 00:00）→ ET 11-11 恢复 4 席，约 2h20m 后
> 本表是筛选结论，**不是提交授权**。按「只挖不提交」政策，提交权归用户点名。

---

## 0 汇总口径（这次是真正的全量，不是截图清单）

| 步骤 | 结果 |
|---|---|
| 会话转录提取 8 字符 id token | 2,955 个；出现 ≥8 次的 1,124 个 |
| 与评估流程交叉（`alpha_corr_cache` / `robustness_*` / `submit_*` / `submission_*`） | 185 个「会话中讨论过且进过评估」的 id |
| 加上前几轮排序清单 | 49 个，**两批去重不重叠** |
| 平台 `/alphas/{id}` 逐个核实状态 | 49 批：42 UNSUBMITTED / 7 ACTIVE；185 批：115 UNSUBMITTED / 69 ACTIVE / 1 DECOMMISSIONED |
| **合计** | **234 个会话 id：157 UNSUBMITTED、76 ACTIVE、1 DECOMMISSIONED** |
| 静态过闸（UNSUBMITTED ∧ S≥1.58 ∧ F≥1.0） | 补充集 100 颗 + 原清单 42 颗中绝大多数 |
| prod 有效（<48h）且 <0.7 | 补充集 14 颗 + 原 S 档 7 颗 |

产物：`results/unsubmitted_scan_20261111.json`、`session_tokens_20261111.json`、`session_extra_scan_20261111.json`、`session_fresh_cand_20261111.json`、`static_gates_20261111.json`。

### ★ 本轮最重要的发现：此前排序漏了 115 颗未提交 alpha

前几轮排序只覆盖用户截图里的 DEU/GBR/GLB 候选。全量扫描后补出 IND / EUR / KOR / USA 等区一批**静态全绿、prod 有效、ΔS 已测为正**的 REGULAR 候选，以及一批 **SUPER 类型**高绩效 alpha。下面分型处理。

---

## 1 分型结论

| 类型 | 代表 | 处理 |
|---|---|---|
| **REGULAR 可交** | `rKRRjM51`、`ZYQv7j2Q`、`rKRx7v6m`、`leAgQPO5` 等 | 纳入今日排序，补逐年与台账 |
| **SUPER 高绩效** | `Xg9WNRg8` 4.74/4.10、`N1NErpxo` 4.55/3.88、`A1VXlbgd` 4.46/4.41、`xAr1YZQb` 4.32/3.97、`9qxVG66r`/`0mYGQo1q` 3.95/4.55、`0mYak1nv` 2.86/3.11、`xAr1Y5gg` 2.80/2.05 | **不进 REGULAR 排序**：SUPER 是独立通道，ET 今日配额 1/1 已用满；且 SA 政策为只挖不提交 |
| **新补但稳健不合格** | `rKRx7v6m`（逐年衰减）、`leAgQPO5`（末年崩塌） | 见 §4，不推荐 |

### SUPER 那批为什么分数高却不能用
平台 `/alphas/{id}` 的 `type=SUPER`，不是 REGULAR。用户铁律「只认 RA 全闸、PPA 不算」；SUPER 走独立配额且每 ET 日仅 1 颗，今日已被 `QPv88bJW` 占用。它们应进入明日的 **SA 方案排序**，不与本表混排。

---

## 2 今日排序主表（T0 = 硬闸全绿 + prod 有效 + 台账 PASS）

| # | id | 区 | ops | S / F | prod（余量） | self | ΔS（分区） | 结算倍率 | 塔边际 | 三问 | 稳健 |
|---:|---|---|---:|---|---|---|---|---|:---:|:---:|:---:|
| **1** | **`P0oolrZq`** | GLB | **6** | **3.45 / 2.37** | .6578（.0422） | .568 | **+0.69** `GLB:1:PP` | ×1.0 | 0 | **免** | PASS CV .374 |
| **2** | **`rKRRjM51`** ⭐新 | IND | 7 | 3.34 / **2.65** | .6752（.0248⚠） | .6516 | +0.38 `IND:1:PP` | ×1.0 | 0 | **免** | **PASS** 新补 |
| **3** | **`wpo8olA6`** | DEU | 8 | 1.65 / 1.27 | .6306（.0694） | .5784 | +0.56 `DEU:1:PP` | ×1.3 | **+1 DEU OTHER ×1.8** | **免** | PASS |
| **4** | **`88NmN37X`** | DEU | 9 | 1.79 / 1.53 | **.5541（.1459）** | .5538 | **+0.74** `DEU:1:PP` | ×1.3 | 0 | **免** | PASS CV .162 |
| **5** | **`omEdka3v`** | GBR | 8 | 2.51 / 1.40 | .6026（.0974） | .4164 | +0.26 `GBR:1:PP` | ×1.2 | **+1 GBR OTHER ×1.6** | 2 腿 | PASS CV .269 |
| **6** | `6XdkW08J` | GBR | 8 | 2.60 / 1.95 | .6267（.0733） | **.3398** | +0.23 `GBR:1:PP` | ×1.2 | 0 | 2 腿 | **PASS CV .057** |
| **7** | `RREPm361` | DEU | **5** | 2.02 / 1.25 | **.6881（.0119）⚠** | .3275 | +0.73 `DEU:1:PP` | **×1.8 ATOM** | 0 | 2 腿 | PASS |
| 8 | `qM7KxkQV` | DEU | 11 | 1.72 / 1.34 | .543（.157） | .5429 | +0.08 `DEU:1` | ×1.3 | 0 | 2 腿 | PASS（被 #4 同席取代）|

**ΔS 禁横比**：DEU:1 常规 before≈3.32、DEU:1:PP before≈1.73、GLB:1:PP before≈3.67、IND:1:PP / GBR:1:PP 各为独立基准。只看符号，不比幅度。

### 排序理由（结合点塔收益）

- **#1 `P0oolrZq`**：全场唯一双高（3.45/2.37），6 ops 最省，免三问，对全篮 ρ≤0.08 完全正交，十年零负年。短板倍率 ×1.0、塔边际 0，但**今天没有既高倍率又硬闸全绿的替代**（`RREPm361` prod 贴线）。
- **#2 `rKRRjM51`（本轮新补）**：F **2.65 全场第二**、免三问、ΔS +0.38、对全篮 ρ≤0.05 完全正交；逐年十年零负年、最低 1.97、末年 3.67 高于均值 3.39、近三年 CV .243。短板是 prod 余量 .0248 / self .6516 双贴线、IND institutions 倍率 ×1.0 垫底、塔边际 0。
- **#3 `wpo8olA6` / #5 `omEdka3v`**：全池仅有的两颗「交后点亮新塔」（DEU OTHER 2→3、GBR OTHER 2→3），两者 ρ=0.019 可同日并交。**但点塔真实收益只是「已点亮金字塔数 +1」**，不是塔内绩效 ×倍率（倍率按数据集类别木桶短板结算，混数据高倍率腿作废）；本季度剩约 50 天，不紧急。
- **#4 `88NmN37X`**：prod 余量最大、ΔS 最高、免三问。staging 仍标 `BLOCKED_PROD_UNAVAILABLE`，需改判。
- **#7 `RREPm361`**：全池唯一 **ATOM ×1.8** + 5 ops 最少，但 prod .6881 余量仅 .0119，**必须先 `refresh=True`** 落到 .66 以下才谈提交。

### 结算倍率（本轮补齐 IND / EUR 档）

| 候选 | 数据集构成 | 各腿倍率 | 结算 |
|---|---|---|---|
| `RREPm361` | analyst7 单（ATOM） | DEU ANALYST 1.8 | **×1.8 满额** |
| `rKRx7v6m` | EUR sentiment + other | 1.4 / 1.5 | ×1.4 |
| `wpo8olA6` / `88NmN37X` / `qM7KxkQV` | shrt3 + X | 1.3 / 1.6~1.8 | **×1.3 锁死** |
| `omEdka3v` / `6XdkW08J` / `ZYQv7j2Q` | model 或 SI + other | 1.2 / 1.6 | ×1.2 |
| `P0oolrZq` / `rKRRjM51` / `leAgQPO5` | GLB risk / IND institutions / GBR imbalance | 1.0 | **×1.0 垫底** |
| `1YNMAA8M` | 三数据集 | — | **计 0 塔** |

---

## 3 席位互斥（本轮实测互相关，4 年日收益）

| 席位 | 成员 | ρ | 胜出 |
|---|---|---|---|
| **IND INSTITUTIONS+PV** | `rKRRjM51` ~ `vR11NmNr` | **.9485** | `rKRRjM51`（S/F/ΔS/self 四项全胜），另一颗 SUPERSEDED |
| **GBR OTHER（tm_15 簇）** | `ZYQv7j2Q`~`58EdlON6` .9485、~`O0AX7Zw1` .8325、`O0AX7Zw1`~`qMLJjleO` .7886 | .63~.95 | 簇内只留 `ZYQv7j2Q`（逐年最佳） |
| **GBR OTHER 跨簇** | `omEdka3v` ~ `ZYQv7j2Q` | **.5182** | `omEdka3v`（ΔS +0.26>+0.09、prod 更低、与簇更正交）|
| **DEU OTHER** | `wpo8olA6`~`xAvK73Qg` .7409、~`Jj8VQwoe` .7372 | .74 | `wpo8olA6` |
| **DEU SI+INSIDERS** | `88NmN37X`~`qM7KxkQV` .9773 | .98 | `88NmN37X` |
| **全篮正交** | `P0oolrZq` / `rKRRjM51` / `rKRx7v6m` / `leAgQPO5` | ≤.16 | 互不挤占 |

**最大互不相关子集（<0.5，精确解）**：`rKRRjM51`、`ZYQv7j2Q`、`rKRx7v6m`、`leAgQPO5`、`P0oolrZq`、`wpo8olA6`（6 颗）。
但其中 `rKRx7v6m` / `leAgQPO5` 稳健不合格（§4），实际可交子集为剩下 4 颗 + `omEdka3v` / `88NmN37X`。

---

## 4 新补但**不推荐**提交（本轮逐年实证）

| id | 表面数据 | 逐年实况 | 判定 |
|---|---|---|---|
| `rKRx7v6m` EUR 3.22/2.14, ΔS +0.39, self .4279 | 看着很强 | 前四年均值 **5.18** → 后四年 **1.78**（衰减 66%）；2020=**1.04**、2023=**1.69** 贴/破 1.58 线；近三年单调下滑 | **CONDITIONAL，不交** |
| `leAgQPO5` GBR 2.16/1.18, self **.1061**, ΔS +0.54, 5 ops 免三问 | 分散度全场最佳 | 末年 2023=**0.62**（不足闸线一半）、2019=1.06；CLUSTER 0.85/1.00 WARNING；prod .6866 贴线 | **CONDITIONAL，不交** |
| `WjOeNE6O` EUR 2.90/1.85, 5 ops | 无台账 | CLUSTER 1.23/1.58 WARNING；self=prod=.6411（疑占位需重测）；无 ΔS / 无逐年记录 | A 档待补 |
| `ZYQ116ln` KOR 3 ops | 算子最少 | F 1.10 贴线、prod .6981 贴线、台账已 CONDITIONAL | A 档 |
| `vR11NmNr` IND 3.29/2.58 | 稳健 PASS | 与 `rKRRjM51` ρ=.9485 同席，四项皆劣 | SUPERSEDED |

台账已写入：`robustness_rKRRjM51`=PASS、`robustness_vR11NmNr`=PASS(注明 SUPERSEDED)、`robustness_rKRx7v6m`=CONDITIONAL、`robustness_leAgQPO5`=CONDITIONAL、`robustness_ZYQv7j2Q`=PASS。

---

## 5 A 档（今晚不可交：缺 prod 终验 / self / 台账 / 三问 / 同席）

`ZYQv7j2Q`（GBR 席备选，逐年 CV .229 最佳但 ΔS +0.09、prod 缓存已近 48h）、`xAvK73Qg`（prod 本轮**已解锁 .6433**，但 11 ops、2017=0.22、同席被取代）、`O0AX7Zw1`、`58EdlON6`、`qMLJjleO`、`WjOeNE6O`、`9qlz29Oe`、`d5a2aO7v`、`zqdvb0YE`、`Jj8VQwoe`、`d5a2vxzY`、`1YNMAA8M`、`LLMv6joe`、`j2Y7qlA5`、`kqNAz9pP`。

## 6 X 档（判死 / 不占位）

- **台账 REJECT**：`mL617YPx`、`9qxnNkeq`、`RREwqrNa`、`qMLOooX1`
- **ΔS<0 硬闸**：`KPJ1rG0j` −.07、`leAnKOEA` −.02、`P0oR7vYw` −.02、`RREOz5qn` −.02、`QPvzNNGG` −.05、`N1NGbddg` −.10
- **prod ≥0.7**：`d5Wvpmbx` .9081、`qML2RxrZ` .8608、`ZYQVJj8n` .8707、`2rAVV7ew` .9156
- **已 ACTIVE（76 颗中的会话相关者）**：`O0W0w3P7`、`E5QZ1NgJ`、`78Yk8VR1`、`QPv88bJW`(SUPER)、`vR1oxZA3`(SUPER)、`zq3eb7No`、`rKRx2Alj`、`GrW9OxmG`、`bl6AvMkN`、`0mY1QPEv`、`P0obGoQJ`、`akK9ooZv`、`d5WGG5bg`
- **同族 SUPERSEDED**：`mLovbnm2`、`2rAYpJKx`、`E569ZE7L`、`QPvx8M1W`、`1YWqzPGQ`、`KPgKPRAx`、`P05JWgdw`、`leA5JeP7` 及 100+ op-min 变体

---

## 7 怎么提交

### 现在（ET 11-10，剩 1 席）→ `P0oolrZq`

硬闸全绿、免三问、绩效碾压、完全正交、prod 余量 .0422。倍率 ×1.0 是短板，但今天没有兼顾高倍率的合格替代。

### GMT+8 13:00 后（ET 11-11，恢复 4 席）→ 建议序列

| 顺位 | id | 拿到什么 | 前置动作 |
|---:|---|---|---|
| 1 | `rKRRjM51` | F 2.65 全场第二 + 完全正交 + 免三问 | prod 06:43 缓存较新，仍建议 refresh |
| 2 | `wpo8olA6` | **点亮 DEU OTHER ×1.8**（金字塔计数 +1） | prod 缓存 11-10 21:59，需 refresh |
| 3 | `omEdka3v` | **点亮 GBR OTHER ×1.6**（+1） | 备 2 腿三问；prod 缓存 11-10 05:57 需 refresh |
| 4 | `88NmN37X` | prod 余量最大、ΔS +0.74、免三问 | staging 从 `BLOCKED_PROD_UNAVAILABLE` 改判 |

- 若 `RREPm361` refresh 后 prod 落到 .66 以下 ⇒ 用唯一 ATOM ×1.8 替换第 4 顺位。
- 四颗两两相关：`rKRRjM51` 对全篮 ≤.05、`wpo8olA6`~`omEdka3v` .019、`88NmN37X`~`wpo8olA6` .5007（超 0.5 仅 0.0007，平台 self 闸为 0.7，实务可接受）。
- 若点塔优先，把顺位 2/3 提到 1/2；两座塔分属不同区、ρ=.019，可同日并交。

### 提交前必做

1. prod 一律 `refresh=True` 终验（台账 48h 作废；`RREPm361` 余量 .0119 尤其危险）
2. 2 腿候选补三问（holders / polarity / prior 各 ≥8 字符）
3. 三段式属性（name / tags ≤5 / description ≥100 词）
4. 提交后复核 `status=ACTIVE` + 塔计数 + prod 快照恒等式

### 点塔收益的诚实定位（承接上一轮）

点亮一座塔 = **已点亮金字塔数量 +1**（Genius / Quality 侧独立计数项），**不是**塔内 alpha 绩效乘倍率。倍率按数据集类别结算，混数据取最低（木桶短板），混 ≥3 类别计 0 塔。因此本季度点塔有价值但不紧急，`wpo8olA6` / `omEdka3v` 明天交照样能点。

---

## 8 数据来源与变更

平台 `/alphas/{id}` 234 次状态核实、`get_pyramid_alphas` 当季计数、`get_pyramid_multipliers` 全区倍率、`compute_mutual_correlation` 两轮 8×8（4 年 1023 点）、`get_alpha_yearly_stats` 5 颗逐年、`alpha_corr_cache` 权威 prod/self 与时龄、`ledger_kv` 全部 `robustness_*` / `submit_*`、会话转录全文正则提取。

**本轮零提交、零平台写操作**（除 5 条本地稳健台账）。新增文件：本报告 + `results/session_*_20261111.json` / `unsubmitted_scan_20261111.json` / `static_gates_20261111.json`。
