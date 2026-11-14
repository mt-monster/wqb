# 全量待提交候选排序（2026-11-11 09:3x GMT+8 / ET 11-10 20:3x）

> **配额：ET 11-10 REGULAR 3/4 已用、剩 1 席｜SUPER 1/1 已用满**
> 今日已交：`78Yk8VR1`(DEU)、`E5QZ1NgJ`(KOR)、`O0W0w3P7`(EUR)、`QPv88bJW`(SUPER/ASI)
> **本表是筛选结论，不是提交授权**（提交权归用户点名）。

## 本轮相对 11-10 版的三处实质变化

| 变化 | 内容 | 影响 |
|---|---|---|
| **① `88NmN37X` prod 解锁** | 此前 6 次终验 + 两轮熔断均算不出；本轮读到权威值 **0.5541**（`check_correlation` @ 11-11 02:27） | 从 A 档升 S 档，并**取代 `qM7KxkQV`**（ρ=0.9773 同席） |
| **② `P0oolrZq` 补齐数据** | 本轮实测 ΔS **+0.69**（`GLB:1:POWER_POOL`）、逐年台账 PASS、**无混腿** | 跃居**全量第 1**：S 3.45 / F 2.37 / 6 ops 全场最优 |
| **③ 撤回对 `Jj8VQwoe` 的推荐** | 上一轮只看截图 11 颗，漏查同席互相关。实测 `Jj8VQwoe ~ wpo8olA6 = 0.7372`、`~ xAvK73Qg = 0.7619` | DEU OTHER 席三选一，`wpo8olA6` 全面胜出 ⇒ `Jj8VQwoe` 判弃 |

---

## 1 全量排序主表（S 档 = prod 权威值已落 + 台账 PASS + 状态干净）

| # | id | 区 | ops | S / F | prod（余量） | self | ΔS（分区） | 台账 | 塔边际 | 三问 |
|---:|---|---|---:|---|---|---|---|---|:---:|:---:|
| **1** | **`P0oolrZq`** | GLB | **6** | **3.45 / 2.37** | .6578（.0422） | .568 | **+0.69**（`GLB:1:PP`） | **PASS** CV .374 | 0 | **免** |
| **2** | **`wpo8olA6`** | DEU | 8 | 1.65 / 1.27 | .6306（.0694） | .5784 | +0.56（`DEU:1:PP`） | **PASS** CV .36 | **+1 OTHER ×1.8** | **免** |
| **3** | **`omEdka3v`** | GBR | 8 | 2.51 / 1.40 | .6026（.0974） | .4164 | +0.26（`GBR:1:PP`） | **PASS** CV .269 | **+1 OTHER ×1.6** | 2 腿 |
| **4** | **`88NmN37X`** | DEU | 9 | 1.79 / 1.53 | **.5541（.1459）新解锁** | .5538 | **+0.74**（`DEU:1:PP`） | **PASS** CV .162 | 0 | **免** |
| 5 | `6XdkW08J` | GBR | 8 | 2.60 / 1.95 | .6267（.0733） | **.3398** | +0.23（`GBR:1:PP`） | **PASS CV .057**（最稳） | 0 | 2 腿 |
| 6 | `RREPm361` | DEU | **5** | 2.02 / 1.25 | **.6881（.0119）⚠超政策线** | **.3275** | +0.73（`DEU:1:PP`） | PASS | 0 | 2 腿 |
| 7 | `qM7KxkQV` | DEU | 11 | 1.72 / 1.34 | .543（.157） | .5429 | +0.08（`DEU:1` 常规） | PASS | 0 | 2 腿 |

**ΔS 禁横比**：`DEU:1` 常规基准 before S≈3.32，`DEU:1:POWER_POOL` 基准 before S≈1.73，`GLB:1:PP` before S≈3.67。硬证据：`zqdvb0YE` 与 `qM7KxkQV` 日收益 ρ=1.0000，ΔS 却 +0.68 vs +0.08 ⇒ 差异 100% 来自分区。

### 排序理由

- **#1 `P0oolrZq`**：S 3.45 / F 2.37 是全场唯一「双高」（第二名 `6XdkW08J` 才 2.60/1.95）；**6 ops 全场最少**；**无混腿免三问**；与其余 8 颗互相关 **≤0.08**（对 `omEdka3v` 恰好 0.0000）完全正交；十年零负年、最低 0.49、近三年 CV 0.309。唯一短板是塔边际 0（GLB OTHER 已 4 颗、RISK 1→2）。
- **#2 `wpo8olA6`**：全池**唯一能点亮 DEU OTHER**（2→3，×1.8）且自身合格的一颗；8 ops、免三问、稳健 PASS。绩效平庸（1.65/1.27）但塔收益是结构性的。
- **#3 `omEdka3v`**：点亮 GBR OTHER（2→3，×1.6），与 `wpo8olA6` ρ=**0.019** ⇒ 两颗可同日并交、各点一座塔。代价：TO 28.2% 偏高、需 2 腿三问。
- **#4 `88NmN37X`**：prod 解锁后，对 `qM7KxkQV` **六项全胜**（ops 9<11、S 1.79>1.72、F 1.53>1.34、TO .0912<.1427、免三问、ΔS +0.74）。两颗 ρ=0.9773 属同一信号，只留这颗。
- **#5 `6XdkW08J`**：CV **0.057** 全场最稳、self .3398 很分散，但塔边际 0，作 GBR 第二席备胎。
- **#6 `RREPm361`**：5 ops 最省、self .3275 最分散、S 2.02，但 **prod .6881 已超 0.68 政策线**（余量仅 .0119），必须 refresh 后落到 .66 以下才谈提交。
- **#7 `qM7KxkQV`**：被 #4 同席取代，降为备胎（若 `88NmN37X` 提交时 prod 翻脸则递补）。

---

## 2 席位互斥图（本轮实测 9×9 互相关，4 年日收益）

| 席位 | 候选 | 互相关 | 胜出 | 理由 |
|---|---|---|---|---|
| **DEU OTHER** | `wpo8olA6` / `xAvK73Qg` / `Jj8VQwoe` | .7409 / .7372 / .7619 | **`wpo8olA6`** | 8 ops 最少、稳健 PASS、免三问、prod 已落 |
| **DEU SI+INSIDERS** | `88NmN37X` / `qM7KxkQV` / `d5a2aO7v` / `zqdvb0YE` | **.9773**（88~qM7）；zqdvb0YE~qM7 **1.0000** | **`88NmN37X`** | 六项全胜 + prod 已解锁 |
| **GBR OTHER** | `omEdka3v` | — | `omEdka3v` | 该席唯一 |
| **GBR SI+MODEL** | `6XdkW08J` | 与 omEdka3v .153 | `6XdkW08J` | 不同席，可共存 |
| **GLB** | `P0oolrZq` | 对全篮 ≤.08 | `P0oolrZq` | 完全正交 |
| **DEU ANALYST** | `RREPm361` / `1YNMAA8M` | 对全篮 ≤.17 | `RREPm361` | 1YNMAA8M prod/self 双贴线 |

**最大互不相关子集（<0.5）**：`wpo8olA6`、`qM7KxkQV`、`omEdka3v`、`6XdkW08J`、`P0oolrZq`、`RREPm361`（6 颗，精确解）。
⚠ 若用 `88NmN37X` 替换 `qM7KxkQV`，则 `wpo8olA6 ~ 88NmN37X = 0.5007` 略超 0.5 线（超 0.0007，平台 self 闸是 0.7，实务可接受）。

---

## 3 塔信息逐颗（铁律：每颗必带五要素）

**当季现值**（`get_pyramid_alphas` 本轮实测，点亮 = ≥3）：

| 区/D1 | 已亮 | 差 1 颗（=2） | 真空 |
|---|---|---|---|
| DEU | analyst 6、model 3、shortinterest 3 | **other 2** | insiders 0、news 0、fundamental 1、institutions 1、sentiment 1 |
| GBR | model 6、shortinterest 4、pv 4、analyst 3、fundamental 3、news 3 | **other 2** | risk/sentiment/insiders/earnings 全 0 |
| GLB | other 4、model 3 | pv 2 | risk 1、earnings 1、institutions 1、其余 0 |
| EUR | analyst 10、other 3、sentiment 3、model 3、fundamental 3、imbalance 3 | pv 2、insiders 2、risk 2、**news 2** | earnings 0 |

| id | 塔归属 | 当季现值 | 交后 | 新点亮 | 倍率 |
|---|---|---|---|:---:|---|
| `P0oolrZq` | GLB RISK + OTHER | 1 / 4 | 2 / 5 | ❌ | RISK ×1.0、OTHER ×1.2（已亮） |
| **`wpo8olA6`** | DEU SI + **OTHER** | 3 / **2** | 4 / **3** | **✅** | **OTHER ×1.8** |
| **`omEdka3v`** | GBR SI + **OTHER** | 4 / **2** | 5 / **3** | **✅** | **OTHER ×1.6** |
| `88NmN37X` | DEU SI + INSIDERS | 3 / 0 | 4 / 1 | ❌（差 2） | INSIDERS ×1.6 |
| `6XdkW08J` | GBR SI + MODEL | 4 / 6 | 5 / 7 | ❌ | 无增量 |
| `RREPm361` | DEU ANALYST | 6 | 7 | ❌ | 无增量 |
| `qM7KxkQV` | DEU SI + INSIDERS | 3 / 0 | 4 / 1 | ❌ | 无增量 |

⇒ **全池仍只有 `wpo8olA6` 与 `omEdka3v` 各带 +1 塔，且分属不同区、ρ=0.019，可同日并交。**

---

## 4 A 档（缺 prod 终验或台账，今晚不可交）

| id | 区 | ops | S/F | 缺口 | 判定 |
|---|---|---:|---|---|---|
| `xAvK73Qg` | DEU | 11 | **2.04/1.77** | **prod 未出数**（本轮实测返回空）；台账 CONDITIONAL（2017=**0.22** 近乎零收益年、十年 CV .501） | OTHER 席绩效最高但被 `wpo8olA6` 取代；prod 出数后可复议 |
| `9qlz29Oe` | DEU | 12 | 1.86/1.34 | prod .47 未落权威表；台账 **CONDITIONAL 最差**（2017 负年、2023=0.30、近三年 CV .638） | 不推荐 |
| `d5a2aO7v` | DEU | 8 | 1.66/1.36 | prod 首测 + 台账 NO_RECORD | 同族 ρ≈1，被 `88NmN37X` 取代 |
| `zqdvb0YE` | DEU | 9 | 1.72/1.34 | 同上 | 与 `qM7KxkQV` ρ=**1.0000**，纯重复 |
| `Jj8VQwoe` | DEU | 12 | 1.65/1.24 | 台账 CONDITIONAL（2016=−0.52）、CLUSTER .91 WARNING | **判弃**：同席 ρ .7372 被 `wpo8olA6` 取代 |
| `d5a2vxzY` | DEU | 12 | **1.60/1.08 双贴线** | self .6038 最挤、末年 1.12 回落 | 不推荐 |
| `1YNMAA8M` | DEU | 8 | 1.58/1.36 | prod .6951 / self .6946 **双贴线** | 被 `RREPm361` 取代 |
| `LLMv6joe` | DEU | 15 | 1.65/1.17 | 15 ops、prod 未测 | SUPERSEDED |

## 5 X 档（判死 / 已出局，不占排序位）

| 类别 | id |
|---|---|
| 台账 **REJECT** | `mL617YPx`、`9qxnNkeq`、`RREwqrNa`、`qMLOooX1` |
| **ΔS < 0 硬闸** | `KPJ1rG0j` −.07、`leAnKOEA` −.02、`P0oR7vYw` −.02、`RREOz5qn` −.02、`QPvzNNGG` −.05、`N1NGbddg` −.10 |
| **prod ≥ 0.7** | `d5Wvpmbx` .9081；EUR risk60 族 `qML2RxrZ` .8608 / `ZYQVJj8n` .8707 / `2rAVV7ew` .9156 |
| 平台 checks FAIL | `gJe2a8wJ` CONCENTRATED_WEIGHT；`2rAVV7ew` LOW_SHARPE |
| **已 ACTIVE** | `vR1oxZA3`(SUPER)、`zq3eb7No`、`rKRx2Alj`、`78Yk8VR1`、`GrW9OxmG`、`bl6AvMkN`、`E5QZ1NgJ`、`O0W0w3P7`、`QPv88bJW`(SUPER)、`0mY1QPEv`、`P0obGoQJ`、`akK9ooZv`、`d5WGG5bg` |
| 同族 SUPERSEDED | `mLovbnm2`、`2rAYpJKx`、`E569ZE7L`、`QPvx8M1W`、`1YWqzPGQ`、`KPgKPRAx`、`P05JWgdw`、`leA5JeP7` 及 57+46 条 op-min 变体 |

---

## 6 执行建议

### 今天（ET 11-10，剩 1 席）— 二选一

| 取向 | 选 | 理由 | 代价 |
|---|---|---|---|
| **绩效优先（推荐）** | **`P0oolrZq`** | S 3.45/F 2.37 碾压全场、6 ops 最省、免三问、与全篮正交、prod 余量 .0422 | 塔边际 0 |
| 塔点亮优先 | `wpo8olA6` | 点亮 DEU OTHER ×1.8，塔内 3 颗同享倍率 | S 1.65/F 1.27 平庸 |

### 明天（ET 11-11，4 席）建议序列

1. `wpo8olA6`（+1 塔 DEU OTHER，免三问）
2. `omEdka3v`（+1 塔 GBR OTHER，需 2 腿三问）
3. `88NmN37X`（prod 已解锁，免三问；staging 需从 `BLOCKED_PROD_UNAVAILABLE` 改判）
4. `6XdkW08J` 或 `P0oolrZq`（取决于今天交了哪颗）

### 提交前必做
- prod 一律 `refresh=True` 终验（台账 48h 作废）；`RREPm361` 余量 .0119 尤其危险
- 2 腿候选补三问（holders / polarity / prior 各 ≥8 字符）
- 三段式属性（name / tags ≤5 / description ≥100 词）
- 提交后复核 `status=ACTIVE` + 塔计数 + prod 快照恒等式

---

## 7 数据来源

本轮实时复核：平台 `/alphas/{id}` 详情（11+11 颗）、`alpha_corr_cache` 权威 prod/self 与时龄、`ledger_kv robustness_*`、`get_pyramid_alphas` 当季塔账、`get_pyramid_multipliers` 倍率、`compute_mutual_correlation`（9 颗 × 4 年，1023 个日收益点）、`mcp_preflight_once.py`（7 颗 ΔS/混腿/闸门）、`get_alpha_yearly_stats`（P0oolrZq / xAvK73Qg 新补台账）。

**本轮零提交**，未改 config / 挖掘闸；新增台账 2 条（`robustness_P0oolrZq`=PASS、`robustness_xAvK73Qg`=CONDITIONAL）。
