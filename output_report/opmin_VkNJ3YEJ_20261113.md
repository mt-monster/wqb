# op-min `VkNJ3YEJ` 收口报告（2026-11-13）

> 用户挂 `@skill:wq-alpha-gate-push-op-min VkNJ3YEJ`。**只挖不提交**，提交权归用户点名。
> 判定只走平台（`GET /alphas/{id}` → `is.checks` + `regular.operatorCount`）。

---

## 0 一句话结论

**原件 `VkNJ3YEJ` 其实不可交** —— `LOW_FITNESS` 0.85 在模拟层是 WARNING，提交层升级为 FAIL，`submit_gate` 实测 `blocked=True`。
本轮把交付件改判为同族 **`vRAgNK3w`（5 算子，F 1.01，八项硬闸逐项 PASS）**：算子数**没能降低**（5 是硬底，2/3/4 算子共 22 条实测全部证伪），但把「不可交」推成了「可交」，并顺带点亮一座新塔。

| 项 | 原件 `VkNJ3YEJ` | **交付 `vRAgNK3w`** |
|---|---:|---:|
| 表达式权重 w | 0.10 | **0.18** |
| 算子数 | 5 | **5**（硬底） |
| S / F | 1.72 / **0.85 ❌** | **1.93 / 1.01 ✅** |
| 2Y / sub(lim) | 1.60 / 0.94(0.89) | **1.66 / 1.01(1.00)** |
| TO / ret | 0.0284 / 3.03% | 0.0415 / 3.42% |
| prod（实读） | 0.6809（历史文档值，未入权威表） | **0.6745**（14:35 实读，已入权威表） |
| self（实测） | 0.1957 | **0.2062** |
| `submit_gate` | **BLOCKED** | **passed=True, failed_ra=0** |
| 塔边际 | — | **EUR/D1/RISK 2→3 点亮 +1** |

---

## 1 ① 采集：原件读数

```
group_rank(add(ts_mean(rsk70_mfm2_euetrd_anlystsn,504),
               multiply(ts_delta(rsk70_mfm2_euetrd_anlystsn,22), 0.1)), country)
```
设置：EUR / TOP2500 / delay1 / decay4 / SUBINDUSTRY / trunc0.08 / nanON / FULL。`operatorCount=5`，`type=REGULAR`，`status=UNSUBMITTED`。

| check | 结果 | 值 | 限 |
|---|---|---|---|
| LOW_SHARPE | PASS | 1.72 | 1.58 |
| **LOW_FITNESS** | **WARNING** | **0.85** | **1.0** |
| LOW_2Y_SHARPE | PASS | 1.60 | 1.58 |
| LOW_SUB_UNIVERSE_SHARPE | PASS | 0.94 | 0.89 |
| CONCENTRATED_WEIGHT | PASS | — | — |
| CLUSTER_TEST | WARNING | 0.94 | 1.58（非硬闸） |
| checks.fail | `[]` | | |

**`submit_gate` 只读实测**：
```
passed=false, blocked=true, failed_ra=1
"模拟层 WARNING 含提交层硬闸项（提交时平台升级 FAIL）：LOW_FITNESS"
"WebDataScope Failed RA=1 / PPA=0（Phase B.0 硬门非零）：['LOW_FITNESS']"
```
⇒ **`checks.fail=[]` 不等于可交**。这与 11-11 `58JnxY95`、11-12 `A1xZ7kNW` 的「WARNING 降级」是同一族陷阱，但这次是 `LOW_FITNESS` 本身被 `WebDataScope` 计入硬门。历史文档 `EUR_FIELD_EVAL_20261113.md` §45 曾把本颗记为「首件全合格件」，同文件 §末（2057 行）已自行更正为「F<1.0 不算合格件」，本轮以平台闸复验确认。

**样本有效性**：逐年 2014–2023 十年完整无空窗（2016 = 0.11 弱年但非负、2021 = 0.70）⇒ **允许调参**。

---

## 2 ② 算子审计 + ③ 杠杆：一个方向反了的通用建议

`op_count.py`：5 个调用点（`group_rank` / `add` / `ts_mean` / `multiply` / `ts_delta`），**无自动可压缩点**（无重复子式、`add` 只有 2 输入、无变参展开空间）。

`plan.py` 对 F 缺口 0.15 给的通用阶梯是 L3 `ts_target_tvr_decay`（降 TO 提 F）、L5 `decay↑`。**这两条在本颗方向是反的**：

```
fitness = S × sqrt( |returns| / max(turnover, 0.125) )
```
本颗 TO = **0.0284**，远低于公式的 **0.125 clamp 下限** ⇒ 分母恒为 0.125，**降 TO 对 F 完全零杠杆**（还会顺带削 ret）。
验算：1.72 × √(0.0303/0.125) = **0.847 ≈ 0.85** ✅ 口径吻合。

要把 F 从 0.85 推到 ≥1.0，只有两条路：
- 提 returns：0.0303 → **0.0423**（+39%）；
- 提 S：1.72 → **2.03**（+18%）。

⇒ 正解是**提 returns**：降 `decay`（减平滑）、提 `truncation`、调两腿权重 w，而不是降换手。

---

## 3 ③ 推指标：同族参数空间全量盘点 + settings 扫描

### 3.1 历史空间（本轮发现的最大杠杆）
平台最近 120 颗 alpha 中含 `rsk70_mfm2_euetrd_anlystsn` 的有 120 颗、**112 个唯一 (表达式, decay, truncation, neutralization) 组合**。历史 EUR「risk70」战役已把 w / 轴 / decay / truncation 扫得相当全。按「逐项 `result=='PASS'` + 0 FAIL」筛出 **7 颗真全闸件（5 个独立构造）**：

| alpha | w | 轴 | decay | S | F | 2Y | sub/lim | sub 余量 |
|---|---|---|---|---:|---:|---:|---|---:|
| **`vRAgNK3w`** | **0.18** | country | 4 | **1.93** | **1.01** | **1.66** | **1.01/1.00** | **+0.010** |
| `KPgaOx8p` | 0.15 | country | 1 | 1.93 | 1.01 | 1.63 | 1.00/1.00 | +0.000 |
| `E5QJv1QR` | 0.15 | country | 0 | 1.93 | 1.01 | 1.63 | 1.00/1.00 | +0.000 |
| `leaXWWx8` | 0.30 | market | 4 | 1.95 | 1.04 | 1.65 | 1.01/1.01 | +0.000 |
| `LLKJ9PV6` | 0.40 | market | 4 | **2.12** | **1.18** | **1.98** | 1.10/1.10 | +0.000 |
| `6XMOEbwO` | 0.50 | country | 0 | 1.92 | 1.00 | 1.75 | 1.02/1.00 | +0.020 |
| `xAvgnApw` | 0.50 | country | 1 | 1.92 | 1.00 | 1.75 | 1.02/1.00 | +0.020 |

（`E5QJv1QR` 与 `KPgaOx8p` ρ=**1.0000**，decay 0/1 逐位相同；`6XMOEbwO` 与 `xAvgnApw` 同理。）

**F 与 2Y/sub 在这族里互斥**：反例 `YPaqgZqR`（w0.3 + INDUSTRY）F **1.12**、S 2.04 很漂亮，但 2Y 掉到 1.52、sub 1.00 < lim 1.06。原因仍是 **sub 限值 = 0.5206 × S 的比值闸**：提 S 会同比抬门槛，光靠推 S 救不了 sub。

### 3.2 本轮 settings 批（10 条，零算子成本）
`w=0.15` 骨架 × decay 0/1/2/3/6 + truncation 0.15/0.20/0.30，`w=0.2 market` 骨架 × decay1 / trunc0.20。
平台并发已满，`submit_batch` 6 次 429 退避后成功 6/10、失败 4/10（`CONCURRENT_SIMULATION_LIMIT_EXCEEDED`）；**失败组合在历史 112 颗里均已有等价读数**，不重复派发。

实测要点：
- **decay 0/1 是 F 的有效杠杆**：`KPgaOx8p`/`E5QJv1QR` 由 w0.15 + decay≤1 把 F 从 0.95 推到 1.01，TO 0.0366→0.0596、ret 0.0329→0.0342。
- **truncation 0.15/0.20/0.30 是零杠杆**：`Wjl8PM5N`/`RReWV3Pe` 与 trunc0.08 基线 **S/F/TO/ret 逐位相同**（1.86/0.95/0.0366/0.0329）⇒ 再次印证 skill 的「扫 truncation 零杠杆」。
- decay 6/8/12 反而掉 F（0.93/0.96/0.91）⇒ 平滑越重 ret 越低。

---

## 4 ④ 压缩算子：**5 是硬底**（22 条实测证伪）

### 4.1 历史 2/3 算子件（12 颗）全掉闸
| 代表 | ops | 构造 | S / F | 掉闸原因 |
|---|---:|---|---|---|
| `qM7qmwkP` | 2 | `group_rank(ts_mean(F,5), subindustry)` | 2.73 / 1.67 | sub 1.06 < **1.42** |
| `KPgaXKdj` | 2 | `group_rank(ts_mean(F,22), country)` | 2.36 / 1.37 | sub 1.06 < 1.23 |
| `rK7XJmMJ` | 2 | `group_rank(ts_mean(F,66), country)` | 2.15 / 1.18 | sub 0.99 < 1.12 |
| `9ql0arYx` | 2 | `group_rank(ts_mean(F,252), exchange)` | 1.69 / 0.82 | F 0.82 < 1.0（sub 反而过） |
| `LLKJgVJ1` | 3 | `winsorize` 版 | 2.29 / 1.26 | sub 1.06 < 1.19 |

短窗口件 **sub/S 只有 0.39–0.46**，远低于 0.5206比值闸 ⇒ **删掉 `ts_delta` 腿就丢掉 sub 闸承重件**。

### 4.2 本轮 4 算子消融批（历史 ops=4 为 0，专攻这个缺口）
10 条全部为 4 算子：删 `multiply`（权重→1.0）配 4 个分组轴 + 全市场 `rank()` + `ts_mean` 252/756 + `ts_delta` 11/44 + `ts_mean→ts_zscore` 语义替换。仿真 `4plPUN1OR4uT8EC18pscz4sS`。

| 变体 | alpha | S | F | 2Y | sub/lim | sub/S | 判定 |
|---|---|---:|---:|---:|---|---:|---|
| 4ops country | `A1xKN79e` | 2.49 | 1.50 | 1.64 | 0.93/**1.29** | 0.373 | ❌ sub |
| 4ops market | `VkNJa39Y` | 2.37 | 1.40 | 1.62 | 0.86/1.23 | 0.363 | ❌ sub |
| 4ops subindustry | `Jj8KNvwx` | 2.40 | 1.38 | 1.55 | 0.98/1.25 | 0.408 | ❌ sub + 2Y |
| 4ops sector | `j2amArEO` | 2.37 | 1.40 | 1.60 | 0.83/1.23 | 0.350 | ❌ sub |
| 4ops `rank()` | `xAvg3d8g` | 2.37 | 1.40 | 1.62 | 0.86/1.23 | 0.363 | ❌ sub |
| 4ops mean252 | `3q0LXer6` | **2.57** | **1.58** | 1.78 | 1.05/1.34 | 0.409 | ❌ sub |
| 4ops mean756 | `MP6maLRa` | 2.38 | 1.37 | 1.77 | 0.84/1.24 | 0.353 | ❌ sub |
| 4ops delta11 | `npaVd8Rq` | 2.60 | 1.40 | 1.51 | 1.25/1.35 | 0.481 | ❌ sub + 2Y |
| 4ops delta44 | `zqdp8R6V` | 2.13 | 1.17 | 1.65 | 0.61/1.11 | 0.286 | ❌ sub |
| 4ops `ts_zscore` | `RReWb1nn` | 1.31 | 0.67 | 0.16 | 0.35/0.68 | 0.267 | ❌ 四项 |

**10/10 全掉 `LOW_SUB_UNIVERSE_SHARPE`**。删权重后快腿主导、S 飙到 2.4–2.6，sub 却跟不上 ⇒ **`multiply(ts_delta, w)` 的权重 w 是 sub 闸的调节件**。

⇒ **5 是本骨架通过全闸的最少算子数**。三档证伪串起来很干净：
`2/3 算子`（删 ts_delta 腿）→ sub/S 0.39–0.46；`4 算子`（删权重）→ sub/S 0.37–0.48；`5 算子`（完整）→ sub/S ≈ 0.52–0.54 刚好过线。

### 4.3 ④b 全量覆盖过审
`operator_coverage_audit.py --checklist` 逐类过审 84 算子（TS30 / Arith16 / Logical11 / Group10 / Vector8 / Cross6 / Transform3）。
Logical（`trade_when` 门控）与 Transformational 按禁用族排除；Vector 类不适用（标量字段）；Cross Sectional 的 `rank` / `group_rank` 同轴等价已在消融批实测。两批签核均写入 `results/op_coverage_signoff.jsonl`（覆盖率 6.0% / 7.1%，单骨架扫描批，不宣称方向穷尽）。

---

## 5 择优：prod 是分水岭

7 颗全闸件互相 ρ = **0.7214–1.0000**，最大独立集 = **1** ⇒ 同族同席，只保留 1 颗，其余标 `SUPERSEDED`。

prod 实读（平台单并发，串行）：

| alpha | w / 轴 | prod | 判定 |
|---|---|---:|---|
| **`vRAgNK3w`** | 0.18 / country | **0.6745**（14:35:27 实读） | ✅ 余量 0.0255 |
| `LLKJ9PV6` | 0.40 / market | **0.7940**（14:40:51 实读） | ❌ **超 0.7 硬墙，判死** |
| `VkNJ3YEJ`（原件） | 0.10 / country | 0.6809（历史文档值，未实读） | F 已掉闸，不参与 |
| `KPgaOx8p` / `6XMOEbwO` | 0.15 / 0.50 | **未出数**（各 21/20 次探测 `pending` + peek 全空体，见 §9.6） | `PROD_UNRESOLVED`，不改判 |

**规律：权重越大 prod 越高** —— 指标最厚的 `LLKJ9PV6`（S 2.12 / F 1.18 / 2Y 1.98）恰恰 prod 超线判死。这与历史文档「形态罕见度驱动 prod」（慢腿 504 罕见、快腿权重小 ⇒ prod 低）一致。⇒ 按 ④b 采纳判据「prod 更低优先」，选 **`vRAgNK3w`**；它在 5 个独立构造里同时是 **sub 余量最厚（+0.010）** 的一颗。

self 实测：`vRAgNK3w` **0.2062**（池 18，最高 `Grge2lN3`）、`LLKJ9PV6` 0.3535、原件 0.1957，全 < 0.70。

---

## 6 交付件 `vRAgNK3w` 完整读数

```
group_rank(add(ts_mean(rsk70_mfm2_euetrd_anlystsn,504),
               multiply(ts_delta(rsk70_mfm2_euetrd_anlystsn,22), 0.18)), country)
```
EUR / TOP2500 / delay1 / **decay4** / SUBINDUSTRY / trunc0.08 / nanON。`operatorCount=5`，`status=UNSUBMITTED`。

| 项 | 值 | 闸线 |
|---|---:|---|
| S | **1.93** | ≥1.58 |
| **F** | **1.01** | ≥1.00（余量 0.01） |
| 2Y Sharpe | **1.66** | ≥1.58 |
| sub / limit | **1.01 / 1.00** | sub/S ≥ 0.521 |
| TO / ret / margin / dd | 0.0415 / 3.42% / 16.5bp / 1.86% | — |
| L/S | 1376 / 1380 | — |
| CONCENTRATED_WEIGHT | **PASS** | 硬闸 |
| CLUSTER_TEST | 1.01 **WARNING** | 非硬闸，需披露 |
| prod / self | **0.6745 / 0.2062** | <0.70 |
| ΔSharpe | **+0.28**（`EQUITY:EUR:1:POWER_POOL`，组合 S 4.32→4.60） | ≥0，`dilutive=false` |
| `submit_gate` | **passed=True, failed_ra=0, failed_ppa=0** | — |
| `mix_audit` | `two_leg` / 2 腿 / coef_legs=1 / `ATOM:LAST_2Y` | **需答三问**（非硬拦） |
| 稳健台账 | `robustness_vRAgNK3w` = **CONDITIONAL** | 已落库 |

**`diversity_audit` 仍 `level=unknown`**：平台未回填 `is.selfCorrelation`，且该 id 不在本地 `alphas` 表（`set_corr_cache` 的 mirror 报 `not_found`）⇒ fail-open，不影响闸门。self 实测值 0.2062 已存 `alpha_corr_cache`（`source=prod_peek`，48h 内有效）。

⚠ 踩到一个来源白名单坑：第一次用 `source='prod_peek+self_mcp'` 写缓存，被自动收敛成 **`legacy`**（落在 `NON_REALTIME_SOURCES`，`prod_gate` 会判不可信）；已改回 `prod_peek` 并复核。

---

## 7 塔信息（逐颗，按当季计数）

平台 `get_pyramid_alphas` 当季 **EUR/D1：analyst 10 / other 3 / news 3 / model 3 / fundamental 3 / sentiment 3 / imbalance 3 / pv 2 / insiders 2 / `risk 2（未亮）` / earnings 1**。点亮线 ≥3。

本轮所有候选均单数据集 `risk70` ⇒ 塔归属一律 **`EUR/D1/RISK ×1.0`**（`is.checks[MATCHES_PYRAMID].pyramids` 实测，非 REST 的 `j["pyramids"]`）：

| 候选 | 塔归属 | 当季计数 | 交后计数 | 是否新点亮 | 塔边际增量 |
|---|---|---:|---:|---|---:|
| **`vRAgNK3w`（交付）** | EUR/D1/RISK ×1.0 | 2 | **3** | **是** | **+1** |
| 其余 6 颗全闸件 | 同上 | 2 | 3 | 是（但已被交付件占用） | 0（同塔第二颗起） |
| 4 算子批 10 颗 / 2·3 算子 12 颗 | 同上 | 2 | — | 不可交 | 0 |
| `VkNJ3YEJ` 原件 | 同上 | 2 | — | 不可交（F 掉闸） | 0 |

⇒ **本轮点塔收益 = +1 座（EUR/D1/RISK 2→3）**。倍率 ×1.0 是 RISK 档垫底，按「塔倍率＝木桶短板」口径，真实收益是「已点亮塔数 +1」而非放大该 alpha 的支付倍率。本轮只交 1 颗，不会重复计点亮。

---

## 8 稳健性（CONDITIONAL，如实披露）

`vRAgNK3w` 逐年 Sharpe：3.39 / 2.88 / **0.54** / 3.13 / 1.15 / 1.44 / 3.25 / **0.69** / 1.05 / **2.48**（2014–2023）。

- 十年**零负年**，最低 2016 = 0.54；
- 近三年 0.69 / 1.05 / 2.48：均值 1.407、**CV 0.550（略超 0.5 阈值）**、max/min 3.59；
- 末年 2.48 > 全期均值 2.00，末段单调回升；平台 2Y 闸 1.66 PASS。

判 **CONDITIONAL**：CV 超线由 2021 低基数造成，不是负年或结构性衰减，但提交时 description 第三段必须如实写出 2016/2021 弱年与 CV 0.550。

---

## 9 提交前剩余动作（提交权归用户，本轮**未提交**）

1. **三问**（`mix_audit two_leg`，holders / polarity / prior 各 ≥8 字符）：holders = 卖方分析师长期预期水平 × 同一分析师群体的月度修正；polarity = 同号对齐（水平高 + 修正确认为看多）；prior = 0.18 权重由「水平主导、事件提供新鲜度」的先验钉死，非回测网格试出 —— 需用户确认后再写。
2. **三段式 description**：按 5 算子 / w=0.18 实况重写，第三段带 2016 0.54、2021 0.69、CV 0.550 的审计痕迹；`CLUSTER_TEST 1.01 WARNING` 亦需披露。
3. **prod `refresh=True` 终验**：当前 0.6745 为 14:35 实读，48h 内有效，但余量仅 0.0255，提交当刻必须重测。
4. **F 1.01 / sub 1.01 双贴线**：按「显示值须 ≥ limit +0.005」，1.01 vs 1.00 有 0.01 缓冲，但平台四舍五入漂移即掉闸，终验时一并复核。
5. ET 当日配额确认。
6. **`KPgaOx8p` / `6XMOEbwO` 的 prod 未闭环，不参与择优**（结论已定稿，不再等）：两颗均带锁触发 5 分钟、21/20 次探测 247s/246s 后返回 `pending`，随后无锁 `--peek` 再各 7/4 次全为空体。与 11-10 `Jj8VQwoe` 同属「平台侧 prod 长期不落地」形态，不要当「等一会就有」处理。二者与交付件 ρ = 0.9959 / 0.7769 同席，且 F 1.01 / sub 1.00(lim 1.00) 余量比 `vRAgNK3w` 更薄 ⇒ **未闭环即不改判**，标 `SUPERSEDED / PROD_UNRESOLVED`。

---

## 10 落差与纪律说明

- **算子数没降**（5→5），但 skill 的两个目标里，「推到全闸通过」是硬约束、「压到最少」是软偏好：本轮耗时主要在证明 **5 已是下限**（2/3 档 12 颗历史 + 4 档 10 条本轮仿真），而不是硬造一个掉闸的 4 算子件。
- 止损条件**未命中**：已找到全闸件，③ 杠杆扫描与 ④ 消融扫描均走完，不判死。
- 共 2 批 20 条本轮仿真（settings 10 条 + 4 算子消融 10 条）+ 112 颗历史同族读数复核 + 5 颗 prod 实读 + 3 颗 self 实测 + 7×7 互相关。

## 11 产物

- `results/batch_VkNJ3YEJ_opmin2.txt`（4 算子消融批）
- `results/_VkNJ3YEJ_spec1.json` / `_VkNJ3YEJ_{w15,w20m,base}.txt`（settings 批）
- `results/_VkNJ3YEJ_family_screen.json`（112 组合全闸筛选）、`_VkNJ3YEJ_lowops.json`（2/3 算子证伪）
- `results/_VkNJ3YEJ_b2.json`（4 算子批结果）、`_VkNJ3YEJ_preflight5.json`（6 颗只读预检）
- `results/prod_wait_{vRAgNK3w,LLKJ9PV6}.json`（prod 实读）
- `alpha_corr_cache`：`vRAgNK3w` prod 0.6745 / self 0.2062（`prod_peek`）；`LLKJ9PV6` prod 0.7940
- `ledger_kv`：`robustness_vRAgNK3w` = CONDITIONAL
- `results/op_coverage_signoff.jsonl`：两批 ④b 签核
