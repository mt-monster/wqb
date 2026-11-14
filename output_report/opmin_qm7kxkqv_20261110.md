# `qM7KxkQV` op-min｜11 → 8 算子，6 批 57 条仿真（2026-11-10 21:1x）

> 用户带 `wq-alpha-gate-push-op-min` 点名。指标**本来已全过**（DEU 战役 BEST 件，9/9 PASS、零 fail），
> 故跳过 ③ 杠杆推指标，直接进 ④ 压算子（用户 11-10 铁律「算子数 = 硬指标」）。

## 0 结论

| 项 | 结果 |
|---|---|
| 算子 | **11 → 9 逐位无损 → 8 全闸通过** |
| 全闸 | 全部定案候选 `failed_ra=0`、`checks.fail=[]`、9 项 PASS **含 `CLUSTER_TEST`** |
| 免费杠杆 | **decay 4→8**：TO 0.143→0.09、F 1.34→1.46~1.54、margin 12→**20bp**、S 不降反升 |
| prod | 原件 `qM7KxkQV` 首测 **0.543 / `all_passed=true`**；新 id 终验被平台 inflight 卡住，**交付前必须补** |
| 提交 | **未提交**；staging 未改；待用户点名定颗 |

## 1 起点（平台实测）

```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 220), sector),
   group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings), 132), 252), sector)
), market)
```

- DEU/TOP500/D1/**decay 4**/SUBINDUSTRY/trunc0.08/**nanON**/2014-01-01~2023-12-31
- 平台 `regular.operatorCount = 11`（本地 `op_count.py` 记 10，一元负号算 `reverse` 的口径差）
- S1.72 / F1.34 / 2Y2.43 / sub0.92 / TO0.1427 / margin **12.15bp**
- `failed_ra=0`；9 项 PASS；`MATCHES_COMPETITION` / `MATCHES_THEMES` WARNING（信息项）
- self **0.5429**；prod 首测 **0.543**（`all_passed=true`，余量 0.157）
- ΔS **+0.08**（`EQUITY:DEU:1` **常规**分区；三颗压缩件落在 `POWER_POOL` 分区，**不可横比**，见 §7.1）；`mix_audit two_leg` 未拦；逐年 10/10 正年、最低 **0.84**、近3 [1.82,2.27,2.69]
- 塔 `DEU/D1/SHORTINTEREST` × `INSIDERS`（effective 2）

⚠ **区域档案 `tracking/DEU/config/settings.json` 是 nanOFF / startDate 2013**，与本件不符 ⇒ 所有批次**显式传** decay/nanHandling/startDate，否则不可比。

## 2 无损压缩链（11 → 9，PnL 逐位相同）

| 改写 | alpha | 平台 ops | 指标 |
|---|---|---:|---|
| 原件 | `qM7KxkQV` | 11 | S1.72/F1.34/2Y2.43/sub0.92 |
| `add(reverse(A),B)` → `subtract(B,A)` | `1YWqZ25X` | **10** | 逐位相同，PnL 8,949,602 完全相同 |
| 再删外层 `group_zscore(·, market)` | **`zqdvb0YE`** | **9** | 逐位相同，PnL 8,949,334（差 268/8.9M = 浮点）；9/9 PASS；self 0.5428；逐年逐位相同 |

⇒ **`group_zscore(·, market)` 在本结构上是数学 no-op**（两腿已经是 sector 内分组排序的 [0,1] 有界量，market 全域做 z-score 不改变截面序）。
⇒ `zqdvb0YE` 是最干净的压缩件：少 2 算子、零指标损失、prod/self/逐年证据链可继承原件。

## 3 逐算子消融（哪些不能删）

| 删除对象 | 结果 | 判定 |
|---|---|---|
| A 腿 `ts_backfill` | S1.59/F1.17/2Y2.56，`failed_ra=0` 但 `CLUSTER_TEST 0.97 WARNING` | 可删，指标降 |
| B 腿 `ts_backfill` | S1.47/F0.90 ⇒ `LOW_SHARPE`+`LOW_FITNESS` FAIL | **承重，不可删** |
| 两处都删 | S1.29/F0.73 + ladder FAIL | 崩 |
| 内层 `group_rank(·,sector)` → `rank` | S0.69/F0.41、`CONCENTRATED_WEIGHT` FAIL、longCount 23 | **sector 轴承重** |
| 外层 → `rank` / 无 | 与 `zqdvb0YE` 同族，最终取「无外层」 | 可删 |
| `vec_avg` → `vec_sum` | S1.60/F1.21（非等价，VECTOR 聚合口径变） | 不采纳 |
| `ts_delta` → `ts_zscore` | S1.36/F0.85 FAIL | 不采纳 |

## 4 8-ops 天花板与 decay=8 免费杠杆

**8-ops 骨架** = A 腿无 `ts_backfill`、B 腿保留，其余同 9-ops。D 批把 bf 窗(44/66/88/110)、内层轴(sector/market)、`ts_delta` 窗(200/220/240)、`ts_rank` 窗(126/252) 全组合后，**decay=4 的 8-ops 天花板是 `MP6j0ge6` S1.65/F1.24**（9/9 PASS）。

**⑤ 设置收敛发现 decay=8 是免费大杠杆**（不占算子）：

| 骨架 | decay | alpha | S | F | 2Y | TO | margin | 闸 |
|---|---:|---|---:|---:|---:|---:|---:|---|
| 9-ops | 4 | `zqdvb0YE` | 1.72 | 1.34 | 2.43 | .1427 | 12.15bp | 9/9 |
| 9-ops | 2 | `gJaYeV9g` | 1.74 | 1.08 | 2.40 | .2249 | 7.77bp | 9/9 |
| 9-ops | **8** | **`YPaj1obw`** | **1.74** | **1.46** | **2.49** | **.0906** | **19.52bp** | 9/9 |
| 8-ops | 4 | `MP6j0ge6` | 1.65 | 1.24 | 2.44 | .1527 | 11.26bp | 9/9 |
| 8-ops | **8** | **`2r51AowN`** | 1.68 | **1.41** | 2.47 | .0975 | **17.94bp** | 9/9 |

⇒ decay 2 把 F 打到 1.08（TO 翻倍）；decay 8 把 TO 砍 36%、F +0.12~0.17、margin +7~8bp，S 不降。**margin 达到 MZ45384 的 15bp 目标**，与本日 CPPAP 治理结论同向。

## 5 F 批：decay=8 回头重扫（设置变了，最优窗也变）

| label | alpha | ops | S | F | 2Y | sub | TO | margin | fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F1 bf66 sector | `YPaja5n6` | 9 | 1.78 | **1.54** | 2.28 | 0.88 | .0936 | 20.07bp | 0 |
| F2 bf66 market | `akaraLMW` | 9 | 1.77 | 1.53 | — | — | .0889 | **21.09bp** | 0 |
| F3 bf88 sector | `LLKPK9q9` | 9 | 1.76 | 1.50 | — | — | .0921 | 19.79bp | 0 |
| **F4 bf110 sector** | **`88NmN37X`** | 9 | **1.79** | 1.53 | 2.37 | **0.95** | .0912 | 20.06bp | 0 |
| F5 bf110 market | `YPaja5m6` | 9 | 1.76 | 1.50 | — | — | .0868 | 20.95bp | 0 |
| F6 bf44 market | `O0W1WrkJ` | 9 | 1.74 | 1.51 | — | — | .0930 | 20.22bp | 0 |
| F7 bf66 market | `88NmN36o` | 8 | 1.65 | 1.37 | — | — | .0928 | 18.60bp | 0 |
| F8 bf88 sector | `wpo8oYzl` | 8 | 1.63 | 1.34 | — | — | .0958 | 17.51bp | 0 |
| **F9 bf110 sector** | **`d5a2aO7v`** | **8** | 1.66 | 1.36 | **2.58** | 0.92 | .0947 | 17.86bp | 0 |
| F10 bf44 market | `gJaYaQoO` | 8 | 1.63 | 1.36 | — | — | .0971 | 17.88bp | 0 |

10/10 全 `failed_ra=0`、9 项 PASS 含 `CLUSTER_TEST`。

## 6 逐年代价（诚实记录）

| 件 | 逐年 Sharpe 2014→2023 | 最低年 | 近 3 年 |
|---|---|---:|---|
| 原件 / `zqdvb0YE`（d4） | 1.45/1.89/1.30/**0.84**/1.40/2.43/1.09/1.82/2.27/2.69 | **0.84** | 1.82/2.27/2.69 |
| `88NmN37X`（d8, 9ops） | 1.69/1.87/1.38/**0.57**/1.41/2.58/1.69/1.87/2.13/2.74 | 0.57 | 1.87/2.13/2.74 |
| `d5a2aO7v`（d8, 8ops） | 2.01/1.29/1.26/**0.61**/1.29/2.64/1.45/**1.00**/2.51/2.71 | 0.61 | 1.00/2.51/2.71 |

⇒ decay=8 让 **2017 早年由 0.84 变 0.57~0.61**（早年软标记、非近 3 年），10/10 仍零负年；近 3 年更强、margin 更高。若要保住 2017 的 0.84 与「逐位无损」，应选 decay=4 的 `zqdvb0YE`。

## 7 定案候选（待用户点名，提交权归用户）

**2026-11-10 21:5x 补算 ΔS**：用户指出上版漏了判据链第 5 步 ⇒ 三颗逐颗跑 `tools/gates/mcp_preflight_once.py`（只读精简预检）。

| 顺位 | id | ops | decay | S/F | 2Y/sub | self | margin | **ΔS（分区）** | mix_audit | 理由 |
|---:|---|---:|---:|---|---|---:|---:|---|---|---|
| **1** | **`d5a2aO7v`** | **8** | 8 | 1.66/1.36 | 2.58/0.92 | 0.5450 | 17.86bp | **+0.64**（`DEU:1:POWER_POOL`） | `none` 免三问 | **算子最少且全闸通过**（用户铁律），ΔS 硬闸过 |
| 2 | `88NmN37X` | 9 | 8 | **1.79/1.53** | 2.37/0.95 | **0.5538** | 20.06bp | **+0.74**（同左，全场最高） | `none` 免三问 | 指标最优；self 贴 0.55 但 ΔS≥+0.02 ⇒ 分散度不拦 |
| 3 | `zqdvb0YE` | 9 | 4 | 1.72/1.34 | 2.43/0.92 | 0.5428 | 12.15bp | **+0.68**（同左） | `none` 免三问 | **逐位无损**压缩，证据链最完备，2017 不退化 |

### 7.1 ★ ΔS 两套基准：同一条 PnL 相差 8 倍

| 对象 | 分区 | ΔS |
|---|---|---:|
| 原件 `qM7KxkQV` | `EQUITY:DEU:1`（**常规**，组合基准 S≈3.30） | **+0.08** |
| 三颗压缩件 | `EQUITY:DEU:1:POWER_POOL`（基准 S≈1.73） | +0.64 / +0.74 / +0.68 |

`zqdvb0YE` 与原件的日收益互相关 **ρ = 1.0000**（同一条 PnL），ΔS 却是 +0.68 vs +0.08 ⇒ **差异 100% 来自分区基准，不是信号变强**。这是 11-08 明令「两套基准只能各自看符号、禁横比」的最强实证。**不能据此说压缩让组合增量提升 8 倍**；三颗同在 PP 分区内的 0.10 幅度差亦只作参考——硬闸按符号判、不看幅度 ⇒ 三颗并列通过，**不改变「算子数 = 硬指标」的排序，#1 仍是 8 ops 的 `d5a2aO7v`**。

### 7.2 补测的其余判据

- **ΔS 硬闸（Step 1.7）**：三颗全为正，无一票否决。
- **混腿**：三颗 `kind=none legs=0 path=LADDER blocked=False` ⇒ 免三问（原件为 `two_leg`）。⚠ `legs=0` 说明识别器未把 `subtract` 计腿，提交时仍建议按两腿备好三问文本。
- **分散度软闸（Step 1.8）**：预检 `unknown / fail-open`（平台未回填 `is.selfCorrelation`）；本地实测 self 0.5450 / **0.5538** / 0.5428。`88NmN37X` 虽 ≥0.55，但三颗 ΔS 均 ≥+0.64 远超 +0.02 ⇒ 按「self≥0.55 **且** ΔS<+0.02」判据**三颗均不拦**。
- **同族实测**（`compute_mutual_correlation(years=4, threshold=0.7)`）：`qM7KxkQV↔zqdvb0YE` **1.0000**｜`↔88NmN37X` 0.9773｜`↔d5a2aO7v` 0.9346｜`88NmN37X↔d5a2aO7v` 0.9540；`max_mutually_below_subset_size=1` ⇒ **确实只能留 1 颗**，其余（含原件）标 `SUPERSEDED`。ρ=1.0000 同时是「逐位无损压缩」的日收益级硬证据。
- **配额**（本次实时 `_local_today_quota()`）：ET **2026-11-10** REGULAR **2/4 已用、剩 2**（今日已交 `78Yk8VR1` / `E5QZ1NgJ`）；SUPER 0/1。11-09 的 3 颗已翻篇。

**换将前置**（若选 1 或 2）：
1. `prod refresh=True` 终验 —— 本轮平台账号级相关性槽持续 `inflight`，`zqdvb0YE` / `YPaj1obw` 多次重查均未拿到值；原件 0.543 只能作参考，**不可继承**。
2. 补登 `robustness_<新id>` 真审（新 id 是 `NO_RECORD`）。
3. 同步 `SUBMIT_STAGING_INDEX_20261110.md` 第 2 行（alpha_id / expression / metrics / correlations / description 五处）。
4. **ΔS 已实测并录入上表**；提交当日池子若变化再跑一次预检即可。混腿仍按 `two_leg` 备好三问文本。
5. 塔账：`DEU/D1/SHORTINTEREST` × `INSIDERS`，INSIDERS 0→1（未点亮）。

## 8 工程记录

- 6 批 **57 条**仿真，零 ERROR；批 A 首次 13 条被平台 `A maximum of 10 simulations can be included in a multi-simulations` 拒 ⇒ 拆 10+3。
- 每批派发前过三闸（`op_arity` + 括号配平 + `bucket` 单位闸）+ `operator_coverage_audit.py --expr-file` + `results/op_coverage_signoff.jsonl` 签核（④b 逐类过审）。
- **踩坑**：D 批 D0 误把 `sector` 传成 `ts_rank` 窗口参数，会整批连坐 ⇒ 修正为正确复现式，并新增「窗口位不得是轴名」自检 + 重签核。
- **踩坑**：`/tmp` 路径在 Windows Python 内不可见，`open('/tmp/...')` 补丁静默失效 ⇒ 改在工作区 `results/_batch_qm7_d.json` 内修正。
- **踩坑**：prod 槽 `inflight=true` 时**不可重复触发**（只会顶成 busy），本轮只做隔时重查 join，未强行刷新。
- 表达式/签核/批次数据：`results/_batch_qm7_{a,b,c,d,f,decay}.{json,txt}`、`results/op_coverage_signoff.jsonl`。
- **未提交**任何 alpha；未改 `config.py` / 挖掘闸 / staging。

---

## 9 提交尝试（2026-11-10 22:0x–22:3x）：用户点名 `88NmN37X`，**未提交**

用户指令「提交88NmN37X」。所有前置均已备妥，唯 **prod 硬闸拿不到权威读数**，按「prod≥0.7 无豁免 + 未出数 fail-closed」不得提交。

### 已完成的提交前置

| 步 | 内容 | 结果 |
|---|---|---|
| 1 | `robustness_88NmN37X` 真审 | **PASS**（近3 [1.87,2.13,2.74] CV **0.162**、CVsample 0.199、10/10 正年、衰减比 1.53、max/min 1.47；软标记 2017 S=0.57） |
| 2 | `submit_staging_88NmN37X.json` | 已建：name `DEU_R_shrtinsd_01`、三段式 description、tags `CH_REG`/`SRC_shortinterest_insiders`/`CORR_MID`（未预置 `PowerPoolSelected`）、expression/settings/metrics/gates、两腿三问文本 |
| 3 | `confirm_submit=False` 干跑 | **全绿**：`submit_gate passed`（failed_ra=0、robustness PASS）→ `mix_audit none` → `ΔS +0.74`（`DEU:1:POWER_POOL`）→ `diversity fail-open` → set_properties/submit skipped |
| 4 | 源码复核 | `submit_alpha.py` Step 1.6 prod 闸**仅在 `confirm_submit=True` 时执行**，`pending/busy/超时一律 fail-closed`，`force` 不豁免 ⇒ 熔断期不会误放行 |

### ★ prod 为何拿不到（完整诊断链）

| # | 尝试 | 结果 |
|---:|---|---|
| 1 | `refresh=True` 240s | `pending` / `inflight=true` / **`last_known=null`** |
| 2 | `refresh=false` join | `platform_unavailable`（连续 pending 触发账号级熔断，剩余 547s） |
| 3 | 等熔断窗口 + join | `pending` / `inflight=true`（21 次轮询） |
| 4 | 两条只读旁路 | 本地 `alpha_corr_cache` **0 命中**；平台详情 `is.prodCorrelation = None` |
| 5 | 槽状态 | `correlation_busy`，holder `corr:get_production_correlation(RREPm361)` |
| 6 | 锁身份 | `logs/_dblock/correlation.lock.json` pid **13448** = `python tools/prod_wait.py RREPm361 --minutes 12`（22:14:29 启动）⇒ **另一会话的合法占用**，按纪律不杀进程、不擅改锁；token TTL 600s 自愈 |
| 7 | 该脚本结束后重试 | 锁 token 已释放，但**账号级熔断再次触发**（剩余 422s） |

⇒ 不是「prod 值超 0.7」，而是**这颗 alpha 至今从未算出过 prod 值**。原件 `qM7KxkQV` 的 0.543 **不可继承**（不同 id、不同 cache 记录），也不能拿同族 ρ=0.9773 推断。

### 结论

- **未提交**，`88NmN37X` 仍为 `UNSUBMITTED` / `stage=IS`；平台零改动。
- 前置成果全部保留（台账 PASS、staging、干跑全绿、三问文本）。平台恢复后只需补一次 `check_correlation(refresh=True)` 拿到 <0.7 的值，即可直接 `confirm_submit=True`。
- 剩余配额 ET 2026-11-10 REGULAR **2/4 剩 2**（今日已交 `78Yk8VR1` / `E5QZ1NgJ`）；SUPER 0/1，未消耗。
| 8 | 22:39 熔断解除后重试 | `correlation_busy`，holder 已换为 `corr:get_production_correlation(78Yk1A2L)` ⇒ **锁在正常轮转**，但其它会话正持续批量查 prod，账号唯一单并发槽被连续占用；继续盲等只会撞上下一个 holder ⇒ **停止尝试**，交用户决定 |

**停止条件**：6 次 prod 尝试、约 45 分钟等待、账号级熔断两轮；非本 alpha 的服务不可得，且不能靠删锁 / 杀进程 / 继承原件读数绕过（prod 闸 fail-closed 且无豁免入口）。

**用户决策（22:4x）**：选择「暂不安排，我说一声再跑」⇒ **不建自动重试任务**，保持现状。触发语＝「重试提交」；届时先确认其它会话的 prod 查询已停，再补一次 `check_correlation(refresh=True)`，拿到 <0.7 即直接 `confirm_submit=True`，前置无需重做。

**23:2x 干净窗口复测**：相关性锁空闲、熔断 sidecar 已清、`inflight` 为空、无其它 holder 的理想条件下重跑 `refresh=True` → 仍 `pending` 244s / **`last_known=null` / `inflight=true`**（20 次轮询）。⇒ **根因收窄为平台 prod 相关性服务本身算不出这颗的值**，不再是槽争用或本地熔断。当前 `inflight=true` 表示平台侧仍在计算；按纪律**不重复触发** `refresh=True`，下次应先 `refresh=false` join 查结果。
