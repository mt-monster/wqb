# WAVE rt-insiders-w3 — `insiders1` 逐臂归因（DEU/TOP500/D1，第二批 10 臂，2026-11-17）

- 日期：2026-11-17；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集 / 目标塔：`insiders1`（塔 **INSIDERS**）；**纯 ATOM 单集**（DB `atom_flag=atom` 10/10），无第二数据集腿
- ⚠ **波号沿用**：`rt-insiders-w3` 在 2026-11-16 已有一批（multisim `2iMbL6g0l5et94o1dclIG3nj`，shares-conc 族，best 0.78，verdict=FAIL，19 条 findings 含「离散度>集中度」「机构持股方向是形态产物」两条认知修正，见 DB 行 id 2238）；本档是**同波号第二批**（multisim `3owZIsbn65bqaAR1xQo03gl`），DB 行按 merge 语义由本批更新。
- 配置（`get_alpha_details` 10/10 逐臂回显一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=**0**、truncation=0.08、nanHandling=**ON**、maxTrade=OFF、FASTEXPR、`startDate=2014-01-01`、`endDate=2023-12-31` —— 探针口径，生产档（decay4/nanOFF）四波未扫，读数只在 decay0/nanON 档内比较。
- 派发/收割（ask 转录，本档未重跑派发）：查重（11-16 旧表 10 条与本轮无一全同）；`preflight_expressions` valid=true / unknown_fields=[]（insd1_holdings/insd1_shares/insd1_valueeur 3 字段在位）；`operator_audit` safe=true（reverse/ts_av_diff/vec_count 无幽灵命中）；`create_multi_simulation` 一次 10 臂；`batch_status` 第 2 次 10/10 COMPLETE errors=0；`harvest_multisim_alphas` 一次成功；`upsert_backtest_rows` n=10（带 checks 原文）。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0（平台 LOW_SUB 限值逐臂动态，本批实读 0.37–0.60）/ TO 0.01–0.70 / margin≥5bp / CW≤0.10（平台 limit）/ failed_ra_count=0 且 checks.fail=[] / self·prod<0.70（未测 null，归相关性员）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

本表 10/10 臂经 `mcp__wq-brain-http__get_alpha_details` 逐臂实读复核，与 ask 转录**逐值一致**；表达式与 `mcp__wqb-db__list_expressions(DEU, rt-insiders-w3)` 的 2026-11-17T22:30:51 批次（id 110348–110357）逐条同序同值。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔 | RA fail（平台 checks.fail） |
|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|
| 1 | `bla9wbLK` | Δmean66÷conc66，**industry** | 1.10 | 0.91 | 0.62 | 0.14 | 8.73% | 10.97% | 19.57bp | 56/124 | INSIDERS eff1 | 5：LOW_SHARPE(1.1/1.58), LOW_FITNESS(0.91/1.0), **CW 0.5/0.1@2014-01-29**, LOW_SUB(0.14/0.52), LOW_2Y |
| 2 | `E5QKdper` | Δmean66÷conc66，**market** | 1.13 | 0.97 | 0.94 | 0.11 | 8.39% | 9.63% | 22.09bp | 64/126 | INSIDERS eff1 | 5：LOW_SHARPE, LOW_FITNESS(0.97/1.0), **CW 0.5/0.1@2014-01-30**, LOW_SUB(0.11/0.54), LOW_2Y |
| 3 | `N1POZaRE` | **Δmean22**÷conc66，sector | 0.77 | 0.50 | **1.20** | 0.06 | 21.21% | 17.84% | 8.32bp | **31**/89 | INSIDERS eff1 | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-02-03**, LOW_SUB(0.06/0.37), LOW_2Y |
| 4 | `RRergbme` | **ts_av_diff(bf(holdings,250),66)**÷conc66，sector | 0.89 | 0.61 | 0.98 | 0.31 | 11.49% | **9.39%** | 10.19bp | 83/134 | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.31/0.42), LOW_2Y（**CW pass**） |
| 5 | `XgaK0bWX` | Δmean66÷**ts_ir(bf(vec_count(shares),250),66)**，sector | 1.23 | 1.10 | 1.09 | 0.32 | 10.16% | 10.94% | 19.62bp | 61/123 | INSIDERS eff1 | 4：LOW_SHARPE(1.23/1.58), **CW 0.5/0.1@2014-01-29**, LOW_SUB(0.32/0.58), LOW_2Y（F 平台 pass） |
| 6 | `A1x3AN0l` | Δmean66÷**ts_ir(bf(vec_avg(shares),250),66)**，sector | **1.27** | **1.15** | 1.02 | 0.32 | 10.19% | 9.89% | 20.18bp | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.27/1.58), **CW 0.5/0.1@2014-01-29**, LOW_SUB(0.32/0.6), LOW_2Y（F 平台 pass） |
| 7 | `E5QKdpvP` | 裸事件频次 `rank(ts_sum(vec_count(shares),66))` | 0.77 | 0.47 | 0.91 | 0.20 | 4.65% | 14.52% | 19.94bp | **130/139（全波最宽）** | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.2/0.37), LOW_2Y（**CW pass**） |
| 8 | `KPgL1NNx` | M6 反向离散度 `rank(ts_mean(reverse(disp66),66))` | **−0.31** | −0.14 | 0.33 | 0.54 | 8.99% | **48.23%（全波最高）** | −5.86bp | 53/54 | INSIDERS eff1 | **3（全波最少）**：LOW_SHARPE, LOW_FITNESS, LOW_2Y（CW+LOW_SUB pass；sub 0.54 来自负 S 退化结构，不可作 sub 候选） |
| 9 | `YPaAebbA` | Δmean66÷**conc22**，sector | 1.16 | 0.97 | 0.75 | 0.07 | 16.19% | 10.35% | 13.86bp | 42/105 | INSIDERS eff1 | 5：LOW_SHARPE(1.16/1.58), LOW_FITNESS(0.97/1.0), **CW 0.5/0.1@2014-02-03**, LOW_SUB(0.07/0.55), LOW_2Y |
| 10 | `2r5KYww5` | Δmean66÷conc66，**subindustry** | 0.99 | 0.76 | 0.50 | 0.03 | 6.99% | 11.96% | 21.04bp | 56/134 | INSIDERS eff1 | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-01-29**, LOW_SUB(0.03/0.47), LOW_2Y |

- **平台 `status`**：10/10 = `UNSUBMITTED`（IS）。
- **本波极值**：best S **1.27**（臂6，**全战役 insiders1 系新高**：0.81→0.89→1.16→1.27）/ best F **1.15**（臂6；臂5 1.10 —— **本波两条 F 平台 pass**，此前全战役仅臂1条）/ best 2Y **1.20**（臂3）/ best sub 0.54（臂8，负 S 退化结构不可用；健康臂最高 0.32 臂5/6）/ best margin 22.09bp（臂2）/ 最低 DD 9.39%（臂4）。
- **0 达标**：10/10 臂 `failed_ra_count` 3–5，**无一条过 RA 全闸**（臂5/6 F 过但 S/CW/SUB/2Y 挂）。

### §1.1 平台实读限值

| 闸 | 平台实读 limit | 备注 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10） | ask 判读基准即此 |
| LOW_FITNESS | **1.0**；臂5 1.10 / 臂6 1.15 进 `checks.pass` | 本波 2 条过 F 闸 |
| LOW_2Y_SHARPE | **1.58** | 全臂挂 |
| CONCENTRATED_WEIGHT | **0.10**；挂闸 7 臂（臂1/2/3/5/6/9/10，value 0.5 @ 2014-01-29/30、02-03）；臂4/7/8 pass | **CW 伪影与 Δmean 分子绑定**：Δmean 分子 7 臂 7/7 挂，非 Δmean 臂（ts_av_diff/裸count/reverse-disp）3/3 pass |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂动态** 0.37–0.60：臂1 0.52 / 臂2 0.54 / 臂3 0.37 / 臂4 0.42 / 臂5 0.58 / 臂6 0.6 / 臂7 0.37 / 臂9 0.55 / 臂10 0.47；臂8 判 pass | sub≥1.0 是本地 review 线 |

## §2 符号指纹逐条（ask 六条）

| # | 判据 | 本波实测 | 结论 |
|---|---|---|---|
| ① | 整式取反 S(−e)≈−S(e) 即停 | **0 条取反对**（无 `multiply(-1,…)` 配对臂；臂8 的 `reverse()` 是臂内算子非镜像对照；ask 收割说明已登记「取反臂本波未排，H2 条件归下游」） | **未测**（不得据此判死/证机制在）；旁证：臂8 reverse-disp S=−0.31 ⇒ 正向 disp（不取反）在同壳下应有正读数，与 w2 disp 裸腿 0.74 方向一致，但壳不同（ts_mean vs ts_sum）非镜像 |
| ② | 去第二腿回落 1.0–1.30 | 纯 ATOM；可测裸腿=臂7（裸 vec_count 频次）0.77 **<1.0，BE176 带未触及**；臂5/6 复合 1.23/1.27 高于该裸腿 +0.46/+0.50；**分子裸腿（Δmean66）全战役从未测** ⇒ 回落带判读对照不完整 | 臂7 0.77 在带下缘之外；复合增益对照不完整（缺裸分子） |
| ③ | decay0/4/8 对照 | **仅 decay0**（10/10 平台回显）；decay4/8 四波未跑 | **未测**（D6 未达，全战役累计） |
| ④ | LC/SC<60/60 = backfill 假填充 | 警戒臂：臂3 31/89、臂8 53/54、臂9 42/105、臂1 56/124、臂10 56/134；边界：臂5/6 61/122-123 | **本轮实跑 `get_alpha_yearly_stats` ×3**（A1x3AN0l / N1POZaRE / YPaAebbA）：**全部 10/10 年 LC>0 且 SC>0**、逐年有机增长（臂6 15/44→111/184；臂3 7/24→56/146；臂9 10/34→74/168）⇒ **非 backfill 假填充**；臂1/8/10 未逐年核（盲区，同集同配置同形态） |
| ⑤ | 费率分组正反两桶 | 无 bucket/费率分桶臂 | **N/A 未测** |
| ⑥ | 首臂 S<1.58 或 sub<0.39 即停 | 臂1 S=1.10<1.58 **机械命中**；但臂6 1.27>基线 1.16（w2 XgaKMZwb，全战役新高）且 F 首次双臂过闸 ⇒ 波内有超基线进展 | 两读法并登：**机械命中 / 实质不触发**；`DEU-INSIDER-AGGMATRIX-DEAD` 0.92 不外推 insiders1；BE176 带 1.0–1.30 —— 臂6 1.27 已逼近带上缘 |

## §3 通道判读（本波三个单变量轴）

### 3.1 分组轴四点扫（同核 Δmean66÷conc66，同壳 group_rank，同配置）

| 轴 | 读数 | 来源 |
|---|---:|---|
| **sector** | **1.16**（基线） | w2 批2 臂4 `XgaKMZwb`（同核同壳同配置，跨波复现锚） |
| market | 1.13 | 本波臂2 |
| industry | 1.10 | 本波臂1 |
| subindustry | 0.99 | 本波臂10 |

⇒ **sector ≥ market(−0.03) > industry(−0.06) > subindustry(−0.17)**：三个替代轴全部低于 sector 基线 ⇒ **分组轴通道关闭判据事实成立**（ask 判据）；且与 w2 批2 的「market 外层零效应」互证——分组轴维度在 insiders1 上已扫净 4 点，sector 是局部最优。交叉验证：w1 批2 11-16 波曾证 sector vs 裸 rank 零增益（−0.03），即 sector 本身也不产生增量，只是不亏。

### 3.2 分母通道打开（事件 IR vs 静态集中度——本波唯一正增益轴）

- **臂5/臂6（Δmean66÷shares-IR）1.23/1.27 vs w2 批2 臂4（Δmean66÷conc66）1.16**：分子、壳、轴（sector）、配置**完全相同，仅分母块不同**（`ts_sum(max÷sum valueeur,66)` → `ts_ir(bf(vec_avg/vec_count(shares),250),66)`）⇒ **跨波单块交换对照**：S +0.07/+0.11、F +0.09/+0.14、sub +0.06、DD −0.6pp。三波 S 演进 1.16→1.23→1.27 同向。
- **臂5 vs 臂6（分母统计量单变量对）**：vec_count 1.23/1.10 vs vec_avg 1.27/1.15 ⇒ **Δ−0.04 S / −0.05 F**：事件计数代理不优于股数水平 IR；shares 轴内 vec_avg 为优。
- **臂7（裸 vec_count 频次）0.77**：裸事件频次远低于复合 1.23/1.27 ⇒ 频次本身不是信号，作分母的 IR 归一化才是。
- ⚠ 分母块交换含 3 个 token 差异（字段 valueeur→shares、统计 ts_sum(max÷sum)→ts_ir、bf250 有无）——是**通道级对照**，不是单 token 消融；shares 裸 IR 腿未测。

### 3.3 窗口轴两点（分子窗 / 分母窗各一）

- **分子窗 66→22**（臂3 vs w2 臂4 基线）：S 1.16→0.77（**−0.39**）、TO 9.81%→21.21%（**翻倍**）、margin −11bp ⇒ 快窗损 S 且毁换手；66 是分子窗局部最优（126 未测）。
- **分母窗 66→22**（臂9 vs w2 臂4 基线）：S 1.16→1.16（**持平 +0.00**）、TO 9.81%→16.19%（+6.38pp）、margin 19.31→13.86bp（−5.45bp）⇒ 分母慢窗不增 S 但毁 TO/margin，无理由用 22。

## §4 稀释铁律

| 复合/形态 | 读数 | 对应已测腿 | 差 | 判定 |
|---|---|---|---|---|
| 臂5/6 Δmean66÷shares-IR | 1.23/1.27 | 臂7 裸 count 0.77（分母侧） | **+0.46/+0.50** | 非稀释（复合 > 已测裸腿）；但分子裸缺 ⇒ 归因不完整 |
| 臂3 Δmean22（快分子窗） | 0.77 | w2 臂4 Δmean66 1.16 | −0.39 | **窗变快=损**（同核单变量） |
| 臂9 conc22（快分母窗） | 1.16 | w2 臂4 conc66 1.16 | +0.00（TO/margin 恶化） | **零增益 + 次级恶化** |
| 臂8 reverse-disp | −0.31 | w2 disp 裸 0.74（壳不同） | 壳混杂 | 不可判稀释（无镜像对）；其 DD 48.23% 与负 S 是本波最差结构 |
| 臂4 ts_av_diff+bf250 | 0.89 | 无同核裸对照 | — | 独立机制首测：**唯一 CW pass 的 Δmean 族近亲**（bf250 修 CW），DD 全波最低 |

- 本波零乘法复合、零 bucket ⇒ 稀释铁律直接对象为零；无一条复合低于其已测对应腿。

## §5 宽度塌缩 / CW / 数据层

- **0 条 data_excluded**：年度分年 3/3 臂 10/10 年 LC/SC>0、7/10 臂 pnl 为正（最大 +11.49M 臂9）、TO 4.65–21.21% 全部 <0.70 ⇒ **数据存在且可交易**。
- **CW 挂闸 7 臂与 Δmean 分子绑定（本波最干净的形态指纹）**：Δmean 分子 7 臂（1/2/3/5/6/9/10）**7/7 挂** CW 0.5@2014-01-29~02-03；非 Δmean 臂（4 ts_av_diff+bf250 / 7 裸 count / 8 reverse-disp）**3/3 pass**。挂点全部落在样本首月（与 11-16 旧批 designNotes 预登记的建仓伪影日期一致）。⇒ **CW 伪影是 Δmean66 分子的家族属性**（首月稀疏覆盖期的 Δ 结构尖峰），不是分母/轴属性——臂4 证明 bf250 可以修掉它（S 0.89、DD 9.39%、CW pass），但 Δmean66+bf250 本身未测。
- 臂8 DD 48.23%：reverse 结构的负 S 退化，表达层；不构成数据层或信号死（其镜像正向未测）。

## §6 塔位判读（点塔相关性）

- 平台 `pyramids` 逐臂实读 **10/10 = DEU/D1/INSIDERS×1.6（effective=1）**、`ra.pyramid_short` 10/10 = `insiders` ⇒ **塔归属 = insiders 10/10 臂**（点塔入口全部成立）。
- **点位 ≠ 点亮**：10/10 臂 RA fail≥1 ⇒ 本批实际点亮 INSIDERS 塔 **0 颗**，塔计数不变。
- 纯 ATOM：无第二塔位申请。

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`**（维持全战役口径）。依据：

1. **判死六维盘点**：
   | 维 | 现状 | 判定 |
   |---|---|---|
   | D1 结构互异模板 ≥10 | 本波单波互异机制约 5（Δmean÷conc 族、Δmean÷shares-IR、ts_av_diff÷conc、裸事件频次、reverse-disp）；**累计战役（BE176 30 + w1 两批 20 + atom-w1 9 + w2 两批 20 + w3 两批 20 + 本批）互异机制 >10** | 累计 ✓ |
   | D2 字段族自测 | **首次达成**：holdings（多波）/ valueeur（多波）/ **shares（11-16 旧批 + 本波臂5/6/7）** / price（w1 批2）/ tradesignificance（w1 批2 + atom-w1）——5 个可测信号字段全部有平台实测；`insd1_value` 按台账规则被 valueeur 替代（ARMTABLE §一：须先归一币种）、gvkey/currency 归编码标签 ⇒ 11-16 旧批所记「price/value/tradesignificance 未测」已被 11-17 各批闭合 | **✓ 达（首次）** |
   | D3 矩全家 | 水平 ✓（臂7）、一阶差 ✓（Δmean 族、臂4 av_diff）、二阶波动 ✓（w1 批2 ts_ir + 本波 shares-IR）、比值 ✓（全部 ÷ 构造） | ✓ |
   | D4 分组轴 ≥2 | 本波单波 4 轴（sector/industry/market/subindustry，§3.1）+ bucket（11-16 旧批） | **✓ 达（单波）** |
   | D5 非线性 ≥1 | group_rank / ts_av_diff / reverse / ts_rank / trade_when（11-16 旧批，负） | ✓ |
   | D6 配置 ≥2 | 全战役五波仅 decay0/nanON 一套；生产档 decay4/nanOFF 未扫 | **✗（唯一未达维）** |
   ⇒ **判死资格缺维从 D2+D6 缩到只剩 D6**；按 AGENTS §7.6 仍**不得判死/封集/作邻接集先验**（D6 未补，且信号仍在单调爬升，无判死动机）。
2. **数据层无排除**（§5）。
3. **信号层在爬升且 F 首次过闸**：best S 0.81→0.89→1.16→1.27 单调向上（跨四批），F 1.15 已过平台闸、S 距闸仅 0.31 —— **最接近闸的一波**，判死无据。
4. **DB 侧一致**：`get_dead_ends(DEU)`（前两 ask 实读）不含 insiders1；`DEU-INSIDER-AGGMATRIX-DEAD` 不外推。
5. 路线层：BE176 上限带 1.0–1.30 —— 臂6 1.27 **逼近带上缘**（带宽内的最后一段），未破顶。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90` / `verdict_from_counts`：n_pass=0 / **n_near=2**）：

- **臂6 `A1x3AN0l`（S 1.27）**：S≥1.2 ✓ + 距 S 闸 1.58−1.27=**0.31 ✓** + CW 0.5 vs 0.1 差 0.40 ✓（边界）+ sub 0.32 距平台动态限 0.6 差 0.28 ✓；F 1.15 平台 pass；2Y 1.02 距闸 0.56 ✗。
- **臂5 `XgaK0bWX`（S 1.23）**：S≥1.2 ✓ + 距 S 闸 **0.35 ✓** + CW 差 0.40 ✓ + sub 0.32 距 0.58 差 0.26 ✓；F 1.10 平台 pass。
- **机械命中出名额（如实登记）**：臂9 `YPaAebbA` S 1.16、F 0.97 **距 F 闸 0.03** ✓；臂2 `E5QKdper` S 1.13、F 0.97 距 F 闸 0.03 ✓ —— 但按「≤2 条按 S 降序」排在臂6/臂5 之后出名额。臂3 2Y 1.20 距闸 0.38 ✓ 但 S 0.77 靠后。
- **稳健性**：n_near≥1 的判定不依赖任何单一口径（臂5/6 同时命中 S≥1.2 与 S-gap≤0.4 双条件）⇒ PARTIAL 稳健。
- ⚠ 本行 (DEU, rt-insiders-w3) verdict 由 11-16 批 FAIL 更新为本批 PARTIAL（merge 语义，ask 指定落库）；11-16 批结论保留在旧 findings。

## §8 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

1. `A1x3AN0l`（S 1.27）：全战役新高、F 1.15 pass、DD 9.89%、年度画像最优（2017 仅 −0.14、2023 1.55、宽度 15/44→111/184 有机）。缺口 = CW 0.5@2014-01-29（Δmean 分子首月伪影，臂4 证明 bf250 可修）+ sub 0.32/0.6 + 2Y 1.02。**先测 prod/self**（归相关性员；prod 雷在核心不在搭档）。
2. `XgaK0bWX`（S 1.23）：同族 vec_count 变体，F 1.10 pass；与臂6 同壳同分子仅分母统计量差（Δ0.04）⇒ prod 高度相关，测一条可外推另一条的相关性风险等级（但须按臂分别测）。

## §9 newLever 登记

**入册 1 条（通道级，带跨波单块对照）**：**「Δmean66 分子的分母通道：事件 IR(shares, bf250) 优于静态集中度(valueeur)」** —— 改造（ts_ir(bf(vec_avg(shares),250),66)）vs 裸对照（ts_sum(max÷sum valueeur,66)，w2 批2 臂4）：S +0.11（1.16→1.27）/ F +0.14（1.01→1.15）/ sub +0.06 / DD −0.61pp；同波 vec_count 变体复现同向（+0.07）。caveats：①分母块含 3 token 差异（字段/统计/backfill），是通道级不是单 token 消融；②仅 decay0/nanON/SUBINDUSTRY 档；③获胜臂仍挂 CW 0.5 与 sub 0.32；④prod/self 未测；⑤shares 裸 IR 腿未测（复合 vs 裸分母的归因部分开放）。
（对照：w2 批已入册的「conc×fresh 乘法」与本条是不同层级的杠杆——那条是乘法交互，本条是分母通道替换。）

## §10 绿芽 / 死轴 / 终态

**绿芽（活体结构）**：
1. `A1x3AN0l` Δmean66÷shares-IR-avg（S 1.27 全战役新高 / F 1.15 pass / 年度画像最优 / CW 缺口仅首月伪影）——**全战役最强 insiders1 系结构**。
2. `XgaK0bWX` 同族 vec_count 变体（1.23/1.10 pass）——臂6 的近亲复现，prod 测试的第二个对象。
3. `RRergbme` ts_av_diff+bf250（S 0.89 / **CW pass** / DD 9.39% 全波最低 / sub 0.31）——**Δmean 族近亲中唯一 CW 干净**，是 CW 修复路线的实证起点。
4. `E5QKdpvP` 裸事件频次（0.77 / 宽度 130/139 全波最宽 / CW pass）——频次腿健康但弱，作分母才有效。

**死轴**：
1. 分组轴替代点：industry（−0.06）/ market（−0.03）/ subindustry（−0.17）全部低于 sector 基线 ⇒ 通道关闭（sector 局部最优，四点扫净）。
2. 快分子窗 22：S −0.39 且 TO 翻倍 ⇒ 66 局部最优（126 未测，但 w2 已证 126 在 IR 分子上损 S）。
3. 快分母窗 22：S 持平但 TO +6.4pp / margin −5.5bp ⇒ 无增益。
4. 裸事件频次作主信号：0.77 且臂内被复合全面超越 ⇒ 频次只配当分母。
5. reverse-disp（M6 反向）：−0.31 / DD 48.23% 全波最差 ⇒ 该形态死（正向 disp 未在本壳测，镜像是缺口非死证）。

**终态**：
- 波 **PARTIAL**（0 达标 / 2 近闸）；best S **1.27**（`A1x3AN0l`，全战役新高）/ best 2Y **1.20**（`N1POZaRE`）/ best F **1.15 平台过闸**（臂6，臂5 亦过）。
- 数据集 `insiders1` = **provisional**（不判死、不 data_excluded、不封集）；**D2 首次达成，判死资格缺维只剩 D6**；S 四批单调爬升 0.81→0.89→1.16→1.27，逼近 BE176 带上缘 1.30。
- 塔：INSIDERS **10/10 臂归属**，**实际点亮 0**。
- 提交链**未推进**（0 达标；near 件 prod/self null）。
- **取证：不需要新论坛取证**（卡点 = CW 首月伪影修复、D6 配置档、prod 测试，全部本地/账号可行动）。

**下一步（按优先级）**：
1. near 件先测 prod/self（A1x3AN0l 优先；XgaK0bWX 次之）；
2. **CW 修复对照**：`ts_backfill` 加进 Δmean 分子（臂4 形态迁移：`divide(ts_delta(ts_mean(ts_backfill(vec_avg(holdings),250),66),66), ts_ir(...))`）——验证 CW 0.5→pass 且 S≥1.27 保持；
3. 配置维补生产档 decay4/nanOFF（D6，全战役唯一缺维）；
4. 分子裸腿对照：`group_rank(rank(ts_delta(ts_mean(vec_avg(holdings),66),66)),sector)`（全战役最大归因缺口，把 +0.46 与通道增益坐实）；
5. shares 裸 IR 腿对照：`group_rank(rank(ts_ir(ts_backfill(vec_avg(insd1_shares),250),66)),sector)`；
6. 分子窗 126（66 的对侧未测点，仅需 1 臂）；
7. 不再重复：industry/market/subindustry 轴（已扫净）、22 窗两侧、裸频次主信号、reverse-disp。

## §11 证据通道与盲区

**实跑核验（本档，全部只读）**：
- `mcp__wq-brain-http__get_alpha_details` ×10（10/10 success）：code/settings/metrics/ra/checks.fail（value·limit·date）/checks.pass/pyramids.list 逐臂取回，与 ask 转录逐值一致；pyramids 10/10 = DEU/D1/INSIDERS×1.6 eff1；臂5/6 LOW_FITNESS 在 checks.pass。
- `mcp__wq-brain-http__get_alpha_yearly_stats` ×3（A1x3AN0l / N1POZaRE / YPaAebbA）：指纹④查证（§2-④）。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w3)`：20 条（11-16 批 id 109922–109931 + 本批 110348–110357 与臂序同序同值，atom_flag=atom 10/10）。
- `mcp__wqb-db__get_wave_result(DEU, rt-insiders-w3)`：读得 id 2238（11-16 批 FAIL 版，19 条 key_findings 在案——本批落库时原样保留）。
- 判定表已读：`src/wqb/wave_results_contract.py:79-90`。
- 前两 ask 实读存档引用：`get_dead_ends(DEU)` 无 insiders1；w1/w2 批2 档案与 DB 行。

**盲区（如实登记，不猜不补）**：
1. decay4/8 与 nanOFF 未扫（D6，全战役五波欠账，唯一判死资格缺维）。
2. 分子裸腿（Δmean66）与 shares 裸 IR 腿从未测 ⇒ 臂5/6 增益与臂7 对照的归因不完整。
3. 分子窗 126 未测（66/22 已扫，缺对侧）。
4. prod/self 全 null（归相关性员）。
5. 年度分年仅 3 臂（臂6/3/9）；臂1/8/10 等未逐年核（同集同配置，假填充风险低但未实证）。
6. 指纹①取反对 0 条（ask 已知未排，H2 条件归下游）；指纹⑤ bucket 未测。
7. CW 伪影的 bf250 修复只是臂4 旁证（av_diff≠Δmean），Δmean66+bf250 本身未测。
8. 波号复用：本批与 11-16 批共用 wave 号 rt-insiders-w3，DB 行两批 findings 并存、verdict FAIL→PARTIAL——两批读数以各自档案为准。
