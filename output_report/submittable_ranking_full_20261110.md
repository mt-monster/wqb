# 全量待提交候选排序（2026-11-10 23:56 GMT+8）

> **ET 日 2026-11-10｜REGULAR 2/4 已用、剩 2｜SUPER 0/1**
> 已提交：`78Yk8VR1`(DEU)、`E5QZ1NgJ`(KOR)（18:07 两颗，点亮 DEU SHORTINTEREST / KOR RISK）。
> **本表是筛选结论，不是提交授权**（`ALLOW_ALPHA_SUBMIT=False`，提交权归用户点名）。

## 判据链（串联闸门，任一硬闸不过即一票否决）

台账 `robustness_*` → 平台 RA `failed_ra=0` → **prod < 0.7（未出数 fail-closed，无豁免）** → **ΔS ≥ 0（只看符号，同分区内比）** → 混腿三问 → 分散度软闸 → 稳健逐年 → 塔（排序项）→ 配额 → 用户点名。

数据源：`output_report/submit_candidates_20261110.md`（16:20 全池名单）、`output_report/recheck_five_20261110.md`（23:40 五颗复评）、`output_report/recheck_three_20261110.md`、`output_report/opmin_qm7kxkqv_20261110.md`、`output_report/opmin_1YWqzPGQ_20261110.md`、今日日志；本轮实时复核 `alpha_corr_cache` / `alphas.status` / `ledger_kv` / 平台详情 / `get_pyramid_alphas` / 互相关矩阵。

---

## 0 结论：推荐用掉剩余 2 席的组合

| 方案 | 组合 | 互相关 | 新点亮塔 | 代价 |
|---|---|---:|---|---|
| **A（推荐）** | **`wpo8olA6` + `omEdka3v`** | **0.0189** | **2 座**（DEU OTHER 2→3、GBR OTHER 2→3） | `omEdka3v` 需 2 腿三问、TO 28.2% |
| B 稳健优先 | `qM7KxkQV` + `6XdkW08J` | −0.0342 | 0 | 11 ops、两颗都需三问、塔边际 0 |
| C 算子/正交 | `RREPm361` + `wpo8olA6` | 0.0611 | 1 座 | `RREPm361` prod 余量仅 .0119 |
| D 原 A 档剩余 | `omEdka3v` + `6XdkW08J` | 0.1530 | 1 座 | 6XdkW08J 塔边际 0 |

**方案 A 的理由**：两颗 prod 权威缓存均在 48h 内（.6306 @21:59、.6026 @05:57）、稳健台账都 PASS、都是 8 ops、ρ 仅 .0189 近乎正交，且分别点亮两座不同的 OTHER 塔 ⇒ 塔、正交、算子、闭环四项同时最优。

---

## 1 全量排序主表

**分档口径**：S = prod 权威缓存已落 + 台账已落 + 状态干净（仅剩属性/三问等轻动作）；A = 需补 prod 终验或台账；B = 同席替代 / 降级备胎；X = 判死或已出局。

| # | id | 区 | ops | S/F | prod（余量 / 缓存） | self | ΔS（分区） | 台账 | 塔边际 | 档 | 放行前置 |
|---:|---|---|---:|---|---|---|---|---|:---:|:---:|---|
| **1** | **`wpo8olA6`** | DEU | **8** | 1.65/1.27 | **.6306**（.0694 / 21:59 实读） | .5784 | **+0.56**（`DEU:1:PP`） | PASS CV .36 | **+1**（OTHER 2→3） | **S** | 无硬缺口；补三段式属性 |
| **2** | **`omEdka3v`** | GBR | 8 | 2.51/1.40 | **.6026**（.0974 / 05:57） | .4164 | +0.26（`GBR:1:PP`） | PASS CV .269 | **+1**（OTHER 2→3） | **S** | 2 腿三问 |
| 3 | `6XdkW08J` | GBR | 8 | **2.60/1.95** | .6267（.0733 / 12:20） | .3398 | +0.23（`GBR:1:PP`） | **PASS CV .057**（全场最稳） | 0 | **S** | 2 腿三问 |
| 4 | `qM7KxkQV` | DEU | 11 | 1.72/1.34 | **.543**（**.157** 最厚 / 21:13） | .5429 | +0.08（`DEU:1` 常规） | **PASS CV .157** | 0（INSIDERS 0→1） | **S** | 2 腿三问；建议改交 8ops 件 |
| 5 | `RREPm361` | DEU | **5** | 2.02/1.25 | .6881（**.0119** / 20:00） | **.3275** | **+0.73**（`DEU:1:PP`） | PASS（记录单薄） | 0（ANALYST 6→7） | **S** | 2 腿三问；prod 必须终验 |
| 6 | `88NmN37X` | DEU | 9 | **1.79/1.53** | **无权威值**（6 次终验 / 两轮熔断） | .5538 | **+0.74**（`DEU:1:PP`） | PASS CV .162 | 0（INSIDERS 0→1） | A | **prod 服务本身算不出**；staging/干跑全备妥 |
| 7 | `9qlz29Oe` | DEU | 12 | 1.86/1.34 | .47（用户给值，**未落权威表**） | .4552 | +0.08（`DEU:1`） | **CONDITIONAL 最差**（CV .638、2017 负年、2023 = 0.30） | 0（NEWS 0→1） | A | prod 终验 + 三问 + 稳健瑕疵披露 |
| 8 | `d5a2aO7v` | DEU | **8** | 1.66/1.36 | 未测 | .5450 | +0.64（`DEU:1:PP`） | **NO_RECORD** | 0 | A | prod 首测 + 补台账 + staging |
| 9 | `zqdvb0YE` | DEU | 9 | 1.72/1.34 | 未测 | .5428 | +0.68（`DEU:1:PP`） | **NO_RECORD** | 0 | A | 同上；逐位无损件，证据链较完备 |
| 10 | `Jj8VQwoe` | DEU | 12 | 1.65/1.24 | .6124（无缓存） | .5645 | **+0.05 最薄**（`DEU:1`） | CONDITIONAL（2016 −0.52） | +1 但**同席失效** | A | **判弃**：与 #1 ρ **.7372** |
| 11 | `d5a2vxzY` | DEU | 12 | **1.60/1.08 双贴线** | .6039（无缓存） | **.6038 最高** | +0.07（`DEU:1`） | CONDITIONAL（末年 1.12） | 0 | A | prod 终验 + 三问；S/F 贴线 |

> **ΔS 两套基准禁横比**：`DEU:1` 常规基准 S≈3.30 vs `DEU:1:POWER_POOL` 基准 S≈1.73。硬证据：`zqdvb0YE` 与 `qM7KxkQV` 日收益 **ρ=1.0000**（同一条 PnL），ΔS 却 +0.68 vs +0.08 ⇒ 差异 100% 来自分区，不是信号变强。

### B 档 · 同席替代 / 降级备胎（不进主排序）

| id | 区 | 降级原因 |
|---|---|---|
| `1YNMAA8M` | DEU | prod .6951(.0049) / self .6946 双贴线；被 `RREPm361` 六项全胜取代；塔边际 0 |
| `xAvK6b0q` | KOR | 5 ops、ladder 2.29 全 PASS，但 prod 三轮空体；**同族 `E5QZ1NgJ` 已 ACTIVE ⇒ 席位锁死** |
| `kqNAz9pP` / `j2Y7qlA5` | DEU | 与已提交 `78Yk8VR1` 同族（ρ .737–.926），仅作备胎；`kqNAz9pP` 台账 NO_RECORD |
| `qMLJjleO` / `ZYQv7j2Q` / `58EdlON6` / `LLM0ePj2` / `O0AX7Zw1` / `zq3nNGp8` | GBR | 同一 `loaned_share_*` 族，互相关 .50–.9485，只能选 1；`omEdka3v` 已是该席最优 |
| `rKRx7v6m` | EUR | 塔边际 0、与已提交 `0mY1QPEv` 同源、台账 NO_RECORD |
| `RREwqrNa` | DEU | 异席但 23 ops、prod .6684、**台账 REJECT**（CV .677–.829，57 种结构已证不可修） |

### X 档 · 判死 / 已出局（不占排序位）

| 类别 | id |
|---|---|
| 台账 **REJECT** | `mL617YPx`、`9qxnNkeq`、`RREwqrNa`、`qMLOooX1` |
| **ΔS < 0 硬闸** | `KPJ1rG0j` −.07、`leAnKOEA` −.02、`P0oR7vYw` −.02、`RREOz5qn` −.02、`QPvzNNGG` −.05、`N1NGbddg` −.10、`LLZ6wZO2` 分散度 |
| **prod ≥ 0.7** | `d5Wvpmbx` .9081；EUR risk60 族 `qML2RxrZ` .8608 / `ZYQVJj8n` .8707 / `2rAVV7ew` .9156 |
| 平台 checks FAIL | `gJe2a8wJ` CONCENTRATED_WEIGHT；`2rAVV7ew` 另 `LOW_SHARPE` |
| 已 ACTIVE（不可重复） | `78Yk8VR1`、`E5QZ1NgJ`、`d5WGG5bg`、`0mY1QPEv`、`zq3eb7No`、`bl6AvMkN`、`rKRx2Alj`、`P0obGoQJ`、`akK9ooZv` |
| 同族 SUPERSEDED | `mLovbnm2`、`2rAYpJKx`、`E569ZE7L`、`QPvx8M1W`、`1YWqzPGQ`、`KPgKPRAx`、`P05JWgdw`、`leA5JeP7`、`LLMv6joe` 及 57+46 条 op-min 变体 |

---

## 2 塔信息逐颗明细（用户 15:30 明令：每颗必带五要素）

**当季现值**（`get_pyramid_alphas` 本轮实测，点亮 = 计数 ≥3）：

| 区/D1 | 已亮（≥3） | 差 1 颗（=2） | 真空（0–1） |
|---|---|---|---|
| DEU | analyst 6、model 3、**shortinterest 3** | **other 2** | insiders 0、news 0、fundamental 1、institutions 1、sentiment 1 |
| GBR | model 6、shortinterest 4、pv 4、analyst 3、fundamental 3、news 3 | **other 2** | risk/sentiment/insiders/earnings/… 全 0 |
| KOR | **risk 3**（今日点亮）、analyst 4、shortinterest 4、fundamental 3、model 3 | pv 2 | insiders 1、other 1 |
| EUR | analyst 10、other 3、sentiment 3、model 3、fundamental 3、imbalance 3 | **pv 2、insiders 2、risk 2** | news 1 |

| id | 塔归属（`is.checks[MATCHES_PYRAMID]`） | 当季计数 | 交后 | 新点亮 | 塔边际 |
|---|---|---|---|:---:|---:|
| `wpo8olA6` | DEU OTHER + SHORTINTEREST | 2 / 3 | **3** / 4 | **✅ OTHER** | **+1** |
| `omEdka3v` | GBR OTHER + SHORTINTEREST | 2 / 4 | **3** / 5 | **✅ OTHER** | **+1** |
| `6XdkW08J` | GBR SHORTINTEREST + MODEL | 4 / 6 | 5 / 7 | ❌ | 0 |
| `qM7KxkQV` | SHORTINTEREST + INSIDERS | 3 / 0 | 4 / 1 | ❌（1/3） | 0 |
| `RREPm361` | ANALYST | 6 | 7 | ❌ | 0 |
| `88NmN37X` / `d5a2aO7v` / `zqdvb0YE` | SHORTINTEREST + INSIDERS | 3 / 0 | 4 / 1 | ❌ | 0 |
| `9qlz29Oe` | SHORTINTEREST + NEWS | 3 / 0 | 4 / 1 | ❌ | 0 |
| `Jj8VQwoe` | SHORTINTEREST + OTHER | 3 / 2 | 4 / **3** | ✅（**但与 #1 同席 ρ.7372 ⇒ 实际 0**） | 0 |
| `d5a2vxzY` | SHORTINTEREST（ATOM 单塔） | 3 | 4 | ❌ | 0 |

⇒ **全池只有 `wpo8olA6` 与 `omEdka3v` 各能带来 +1 塔，且属不同区、互相关 .0189，可同日并交。**

---

## 3 提交前前置动作矩阵

| id | prod 终验 | 稳健台账 | 三问 | staging/属性 | 互相关 | 塔复核 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `wpo8olA6` | ✅ 权威缓存 21:59（建议提交当刻 `refresh=True`） | ✅ PASS | 免（`kind=none`） | ⚠ 需补三段式 name/tags | ✅ 已测 | ✅ |
| `omEdka3v` | ✅ 05:57（48h 内；建议 refresh） | ✅ PASS | **需 2 腿** | 需属性 | ✅ 已测 | ✅ |
| `6XdkW08J` | ✅ 12:20（platform_sync） | ✅ PASS | 需 2 腿 | 需属性 | ✅ 已测 | ✅ |
| `qM7KxkQV` | ✅ 21:13 | ✅ PASS | 需 2 腿 | 需属性 | ✅ 已测 | ✅ |
| `RREPm361` | ⚠ **余量 .0119，必须 refresh** | ✅ PASS（记录单薄） | 需 2 腿 | 需属性 | ✅ 已测 | ✅ |
| `88NmN37X` | ❌ **平台算不出（阻塞中）** | ✅ PASS | 免三问（已备文本） | ✅ 已建、干跑全绿 | ✅ 已测 | ✅ |
| `9qlz29Oe` | ❌ 无权威表 | ⚠ CONDITIONAL | 需 2 腿 | 需属性 | ✅ 已测 | ✅ |
| `d5a2aO7v` / `zqdvb0YE` | ❌ 首测 | ❌ NO_RECORD | 免三问 | ❌ 未建 | ✅ 已测 | ✅ |
| `Jj8VQwoe` / `d5a2vxzY` | ❌ 无权威表 | ⚠ CONDITIONAL | 需 2 腿 | 需属性 | ✅ 已测 | ✅ |

**prod 服务现状**：今晚 6 次终验 + 两轮账号级熔断；23:2x 在「锁空闲 / 熔断清 / inflight 空」的干净窗口下 `refresh=True` 仍 pending 244s ⇒ **平台侧算不出新值**。⇒ 排序里「prod 权威缓存已落」是硬优势，未落表的候选今晚基本不可交；下次先 `refresh=false` join，勿重复触发。

---

## 4 推荐执行顺序（剩余 2 席）

1. **`wpo8olA6`** — 补三段式属性（name / tags ≤5 / description ≥100 词）→ `confirm_submit=False` 干跑 → `confirm_submit=True`。prod 命中 21:59 权威缓存，预计可过。
2. **`omEdka3v`** — 备 2 腿三问（holders / polarity / prior，各 ≥8 字符）→ 属性 → 干跑 → 提交。
3. 若任一 prod 终验 ≥0.7 ⇒ 立即放弃，按顺位递补 `6XdkW08J` → `qM7KxkQV`。
4. 提交后复核：`status=ACTIVE`、塔计数、prod 快照恒等式、`alphas.status` / `submission_ledger` 两张本地表同步。

---

## 5 五个高频误判（本轮再次验证）

| 误判 | 正解 |
|---|---|
| 截图 Δ 为负就否 | 面板口径曾与平台相反；必须 `performance_comparison` / `mcp_preflight_once.py` 复核 |
| ΔS 数值大 = 信号强 | 两套分区基准不同，**只能同分区内看符号**，禁横比（ρ=1.0000 的两颗差 8 倍） |
| prod 低 = 增量高 | prod 对第三方池、ΔS 对自己池；`RREOz5qn` prod .5834 却 ΔS −.02 |
| 平台 checks 全 PASS = 稳健合格 | `9qlz29Oe` 全 PASS 但 2017 负年、2023 崩到 .30、CV .638 |
| 标签「可点新塔」 | 只认 `get_pyramid_alphas` **当季**计数 ≥3；`DEU_OS_INVENTORY` 用全历史反推曾算错 |

---

## 6 数据来源与状态

- 实时复核（本轮）：`alpha_corr_cache` 权威读数与时龄、`alphas.status` 全部 UNSUBMITTED、`ledger_kv robustness_*`、平台详情 S/F、`get_pyramid_alphas` 当季塔账、`compute_mutual_correlation(6 颗, 4y)`。
- 互相关关键值：`wpo8olA6~omEdka3v` **.0189**｜`omEdka3v~6XdkW08J` .153｜`qM7KxkQV~88NmN37X` **.9773（同族只留 1 颗）**｜`RREPm361` 对全篮 ≤.17｜最大独立子集 = 5。
- **本表零提交**，未改 config / 挖掘闸 / staging（除 `88NmN37X` 已有的那份）。
