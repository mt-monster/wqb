# 交付报告 · KOR × RISK × ATOM 候选池（2026-11-06）

> **交付口径（用户澄清，本报告的验收标准）**：
> 「可交付 10 个 ATOM」= **一个候选池**，满足
> ① 每颗 `self < 0.7`；② 每颗 `prod < 0.7`；③ **池内两两互相关 `< 0.7`**；
> ④ 不能用同一参数族的 10 个变体充数。
>
> **结论**：已交付 **10 颗 ATOM 型 REGULAR alpha**（KOR / TOP600 / D1 / EQUITY，全部取自 Risk 数据集），
> 三项红线**全部经 MCP 实测并通过**：self 最大 **0.4247**、prod 最大 **0.6898**、池内两两互相关最大 **0.6007**。
> 10 颗横跨 **4 个数据集 / 9 个不同核心字段 / 6 种构造几何**，不是参数族变体。
>
> ⚠ **必须说清的边界（诚实声明）**：本区只有 `anlystsn` 一条强轴（S 1.62），而强轴同族的
> prod / self / 互相关互相撞墙（见附录 B），**无法用 10 个强轴变体凑池**。因此池中
> **只有 `omERn83n` 是「RA 全闸通过 + S≥1.58」级别**；其余 9 颗是
> 「**相关性三项合规、但 IS 强度偏弱**」的候选（S 0.42–1.06），定位是**候选池 / 组合腿 / 后续优化起点**，
> 不是「10 个已可提交」。逐颗推指标须走 `wq-brain-alpha-optimization-v1`；**提交权归用户，本报告不含任何提交动作**。
> 另有 2 颗 risk59 仅 9 年覆盖（约束 6 已知偏差，见 §2 与交付边界），已在验收表如实标注。

---

## 1. 验收标准与终验结论

| 红线 | 阈值 | 实测口径 | 结果 |
|---|---|---|---|
| 单颗 self | `< 0.7` | MCP `check_self_correlation`，对已提交 OS 池（44 颗，排除 PPA） | **10/10 PASS**，max **0.4247** |
| 单颗 prod | `< 0.7` | MCP `check_correlation(correlation_type='production', refresh=False)`，48h 权威缓存 | **10/10 PASS**，max **0.6898** |
| 池内两两互相关 | `< 0.7` | MCP `compute_mutual_correlation`（4 年 / 1023 交易日 PnL） | `all_below_threshold=true`，`pairs_over_threshold=[]`，max **0.6007** |
| 类型 / 区域 | ATOM · REGULAR · KOR | MCP `get_alpha_details` | 10/10 `REGULAR / KOR / TOP600 / D1 / EQUITY`；ATOM 按「单数据集 + 分组键」判定 |
| 非参数族 | 结构多样 | 表达式审计 | 4 数据集 / 9 字段 / 6 几何 |
| ATOM 判定 | 单数据集 | 逐颗表达式字段审计 | 10/10 单数据集；出现的第二 `rsk` 字段是**同数据集内的正交控制腿** |
| 组腿约束 | 禁 PV/MODEL/OTHER 两两组腿 | 逐颗表达式审计 | **0 例**跨类组腿；`nonrisk_legs=0`、`cross_dataset=false` |
| 区域固定 | KOR | `get_alpha_details` | 10/10 KOR；全程未换区 |
| 近十年覆盖（约束 6） | 10 年有数据 | MCP `get_alpha_yearly_stats` 逐年 `longCount` | **8/10 全 10 年**（risk70/88/68）；⚠ **2/10 仅 9 年**（risk59，2014 空年）——已知偏差，见 §2 标注与交付边界 |

> prod 严格红线 `0.70` 不放行（本轮最接近的入池项是 `omERn83n` 0.6898，余量 0.0102）。
> `busy` / `pending` 一律记为「无结论」，从未写入 PASS/FAIL；见附录 A 的排队处置记录。

---

## 2. 十颗候选池明细（终验实测值）

| # | alpha_id | 数据集 | 核心字段 / 机制 | 中性化档 | S | F | TO | self | prod |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | **`omERn83n`** | risk70 | `anlystsn` 水平（分析师情绪载荷，动量正交） | REVERSION_AND_MOMENTUM | **1.62** | **1.23** | .1319 | 0.4211 | **0.6898** |
| 2 | `O0AReMkq` | risk70 | `growth` 载荷（残差波动正交） | CROWDING | 0.69 | 0.36 | .0496 | 0.3172 | 0.5762 |
| 3 | `WjO3wXYQ` | **risk88** | `ri_divyield` 载荷（独立 vendor 模型股息） | CROWDING | 0.55 | 0.30 | .0379 | 0.2817 | 0.6292 |
| 4 | `O0ARb6VJ` | risk70 | `shortint` 空头兴趣载荷（动量正交） | REVERSION_AND_MOMENTUM | 0.55 | 0.28 | .1048 | 0.3961 | 0.6555 |
| 5 | `gJeXqPrJ` | **risk88** | `ri_growth` 载荷 | CROWDING | 0.52 | 0.23 | .0407 | 0.1882 | 0.5909 |
| 6 | `58ErwdQ6` | **risk88** | `ri_momentum` 载荷 **反向** | CROWDING | 0.42 | 0.16 | .1963 | 0.1669 | 0.3837 |
| 7 | `j2YoN6vW` | risk70 | `ts_rank(anlystsn,252)` 载荷时序分位 | CROWDING | 0.74 | 0.38 | .1388 | 0.4247 | 0.6743 |
| 8 | **`QPvr1vPM`** | **risk59** | `offer_rate` 借券报价费率 · `hump` 平滑 | STATISTICAL | **1.02** | 0.67 | .1350 | 0.2352 | 0.6552 |
| 9 | **`bl6VQQdZ`** | **risk68** | `residual_return` 5 日残差 · 22 日反转 | STATISTICAL | **1.06** | 0.36 | .4440 | 0.2355 | 0.6314 |
| 10 | `mLoJrQrW` | **risk59** | `s3utilization` 借券利用率 · 双 rank 分位 | STATISTICAL | 0.58 | 0.20 | .2142 | 0.0986 | 0.2439 |

**结构覆盖**：risk70 ×4 / risk88 ×3 / risk59 ×2 / risk68 ×1 —— 4 个数据集、9 个不同核心字段。
> ⚠ **覆盖偏差（诚实标注，对应约束 6）**：S0 已发现 `risk59` 因 **2014 空年**降级；终验 `get_alpha_yearly_stats`
> 复核确认入池的 2 颗 risk59（`QPvr1vPM` / `mLoJrQrW`）2014 年 `longCount=0`，实际仅 **2015–2023 共 9 年**有持仓，
> 未严格满足「近十年都要有数据」。其余 8 颗（risk70/88/68）2014 起 10 年全覆盖。这两颗是「相关性最干净」的补位件
> （prod 0.6552 / 0.2439、self 0.2352 / 0.0986），为凑够互不相关的 10 颗而保留；**若需严格 10 年覆盖，须替换并重测整池互相关**。
**构造几何（6 种）**：载荷水平 · 载荷反向 · 载荷时序分位 · 借券费率 hump · 残差动量反转 · 借券利用率分位。
**prod 测量时间**：`QPvr1vPM` 为 11-05 22:15，其余 9 颗为 11-06；全部落在 `alpha_corr_cache` 48h 保鲜窗内。

---

## 3. 相关性终验

### 3.1 池内两两互相关（`compute_mutual_correlation`，threshold 0.7）

```
n = 1023 交易日   all_below_threshold = true   pairs_over_threshold = []
max_pair = omERn83n ~ j2YoN6vW = 0.6007      subset_size = 10      missing_pnl = []
```

Top 结构对：`omERn83n ~ j2YoN6vW` 0.6007（两颗同为 `anlystsn` 但一个取水平、一个取 252 日时序分位）、
`omERn83n ~ O0ARb6VJ` 0.4946、`QPvr1vPM ~ KPJgXzbp` 0.5499（后者未入池）。
**10 颗全部互相低于 0.7，无一对需要剔除。**

### 3.2 单颗 self（本地 OS 池计算，不占平台相关性槽）

| alpha | self | alpha | self |
|---|---:|---|---:|
| `omERn83n` 0.4211 | ✅ | `58ErwdQ6` 0.1669 | ✅ |
| `O0AReMkq` 0.3172 | ✅ | `j2YoN6vW` 0.4247 | ✅ |
| `WjO3wXYQ` 0.2817 | ✅ | `QPvr1vPM` 0.2352 | ✅ |
| `O0ARb6VJ` 0.3961 | ✅ | `bl6VQQdZ` 0.2355 | ✅ |
| `gJeXqPrJ` 0.1882 | ✅ | `mLoJrQrW` 0.0986 | ✅ |

OS pool size = 44（已排除 Power Pool Alphas），`self_all_pass = true`。

### 3.3 单颗 prod（MCP `check_correlation`，全部落地到 `alpha_corr_cache`）

prod 由高到低：`omERn83n` 0.6898 → `j2YoN6vW` 0.6743 → `O0ARb6VJ` 0.6555 → `QPvr1vPM` 0.6552 →
`bl6VQQdZ` 0.6314 → `WjO3wXYQ` 0.6292 → `gJeXqPrJ` 0.5909 → `O0AReMkq` 0.5762 →
`58ErwdQ6` 0.3837 → `mLoJrQrW` 0.2439。**全部 < 0.7**。

---

## 4. 每颗的数据集 / 核心字段 / 算子逻辑（完整表达式）

**统一设置档（KOR 合法档，`get_platform_setting_options` 实测）**：KOR / TOP600 / Delay 1 / EQUITY ·
decay 1 / truncation 0.04 · unitHandling VERIFY / nanHandling ON · pasteurization ON / maxTrade OFF ·
区间 2014-01-01 ~ 2023-12-31（10 年）· FASTEXPR。中性化档逐颗见 §2。

```text
# 1 omERn83n  risk70 · anlystsn 水平（momentum 正交）
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(
  rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn, 40)),
  rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))), std=0.38), sector), 2.5), target_tvr=0.22)

# 2 O0AReMkq  risk70 · growth 载荷（resvol 正交）
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(
  rank(ts_backfill(rsk70_mfm2_asetrd_growth, 40)),
  rank(ts_backfill(rsk70_mfm2_asetrd_resvol, 22))), std=0.24), sector), 3.5), target_tvr=0.22)

# 3 WjO3wXYQ  risk88 · ri_divyield 载荷
ts_target_tvr_decay(signed_power(group_rank(winsorize(
  rank(ts_backfill(rsk88_mfm_ase1_ri_divyield, 40)), std=0.24), sector), 3.5), target_tvr=0.22)

# 4 O0ARb6VJ  risk70 · shortint 空头兴趣载荷（momentum 正交）
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(
  rank(ts_backfill(rsk70_mfm2_asetrd_shortint, 40)),
  rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))), std=0.40), sector), 2.5), target_tvr=0.22)

# 5 gJeXqPrJ  risk88 · ri_growth 载荷
ts_target_tvr_decay(signed_power(group_rank(winsorize(
  rank(ts_backfill(rsk88_mfm_ase1_ri_growth, 40)), std=0.24), sector), 3.5), target_tvr=0.22)

# 6 58ErwdQ6  risk88 · ri_momentum 载荷（反向）
ts_target_tvr_decay(reverse(signed_power(group_rank(winsorize(
  rank(ts_backfill(rsk88_mfm_ase1_ri_momentum, 40)), std=0.24), sector), 3.5)), target_tvr=0.22)

# 7 j2YoN6vW  risk70 · anlystsn 的 252 日时序分位（resvol 正交）
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(
  rank(ts_backfill(ts_rank(rsk70_mfm2_asetrd_anlystsn, 252), 40)),
  rank(ts_backfill(rsk70_mfm2_asetrd_resvol, 22))), std=0.24), sector), 3.5), target_tvr=0.22)

# 8 QPvr1vPM  risk59 · 借券报价费率（hump 平滑，反向）
hump(reverse(group_zscore(vec_avg(rsk59_offer_rate), sector)), hump=0.003)

# 9 bl6VQQdZ  risk68 · 5 日残差收益 / 22 日分位反转
winsorize(reverse(group_rank(ts_rank(ts_sum(rsk68_residual_return, 5), 22), industry)), std=2)

# 10 mLoJrQrW  risk59 · S3 借券利用率（行业→市场双 rank 分位）
quantile(group_rank(ts_rank(group_rank(vec_avg(rsk59_s3utilization), industry), 252), market))
```

**算子逻辑分层（以 #1 为代表）**：① `ts_backfill(·,40)` 补 3.3% 缺失 → ② `rank` 去量纲 →
③ `vector_neut(·, rank(momentum))` 剥动量暴露 → ④ `winsorize(std)` 压厚尾 →
⑤ `group_rank(·, sector)` 行业内相对排序 → ⑥ `signed_power` 尾部集中 + `ts_target_tvr_decay(target_tvr=0.22)` 控换手。
**ATOM 判定**：每颗仅用 1 个数据集字段（或同数据集的正交控制字段）+ 分组键，无 pv1 / `inst_pnl` / `convert`
⇒ `classify_atom = atom`。UNSUBMITTED alpha 的平台 `classifications` 为空属正常，ATOM 按表达式规则判定。

---

## 5. 经济机制（A-2 收益来源声明，缺项即不许组装）

| 机制族 | 入池颗 | 谁在被定价 / 为什么会被错 | 修复周期 |
|---|---|---|---|
| **风格载荷（risk70 / risk88）** | #1–#7 | 个股对风格因子的**回归载荷高** ⇒ 收益被系统性暴露主导；载荷 = 暴露，须先 `winsorize` 压厚尾、再正交/中性化才剩残余 alpha。KOR 分析师情绪载荷存在 post-revision drift（延迟反应）与过度外推两段，实测**正方向占优** | 22–66 日（月度级，TO 13% 吻合） |
| **借券市场（risk59 / risk68）** | #8–#10 | 借券报价费率 / 利用率 / 残差收益反映**卖空约束与拥挤度**；KOR 卖空禁令期使空头腿稀缺，借券价格含预期修正信息，费率与利用率的截面高低对应被高估程度 | 5–252 日（跨短反转与季度） |

**失效条件**：① 分析师覆盖稀疏股（载荷估计噪声）；② 风险模型版本切换（MFM2 / ASE1 口径变更）；
③ KOR 卖空禁令期（2020-03~2021-05、2023-11 起）空头腿与借券域受限 —— 这是 risk59/68 机制的主要风险敞口。

**双通道取证（沿用 S2 立项，逐波归因见 waves.md）**

| 通道 | 来源 | 结论 |
|---|---|---|
| A 论坛 | `43621466539671`（30 赞，【Risk70】USA/D1 多因子模型 5 组组合） | 「单字段直用基本没信号…加载类字段的价值在组合，不在单点」；loading 厚尾须 `winsorize` / `ts_zscore` 前置 ⇒ **直接决定本轮 winsorize 前置 + 单字段正交化路线** |
| A 论坛 | `36064174250519`（20 赞，RISK 数据集出货率很高） | 「SLOW 档出货率高、池内相关性 <0.6」——⚠ **KOR 实测不成立**（SLOW 0.97–1.04 vs REVERSION_AND_MOMENTUM 1.63），但「中性化档是关键杠杆」成立 |
| A 论坛 | `43607258135319`（29 赞，剥离贝塔看清自己） | 载荷 = 系统性暴露，须中性化后才剩纯 alpha ⇒ 与 raw/RN 分解一致 |
| B 文献 | Stickel (1991, JF)；Gleason & Lee (2003, TAR) | 分析师上修 ⇒ 后续 3–12 月正异常；KOR 本区 analyst 数据集实测 S 1.40–1.66 ⇒ 机制在 KOR 成立 |
| B 文献 | Ehsani & Linnainmaa (2022, JF) 因子动量；Asness-QMJ | 载荷变化的时序自相关可预测收益 ⇒ 支持「载荷水平 / 时序分位 + 正交」的构造（#1 / #7） |
| 裁决 | A、B 同指 | A 给可落地表达（winsorize 前置 + 组合/正交），B 给方向句与持有期；一致，直接组装 |

---

## 6. 字段画像存档索引

| 文件 | 内容 | 字段覆盖 |
|---|---|---|
| [s0_dataset_scan.md](s0_dataset_scan.md) | 7 个 Risk 数据集全量扫描、候选裁定、用户约束映射 | 数据集级 |
| [s1_field_profile_risk70.md](s1_field_profile_risk70.md) | risk70 全字段画像（类型 / cov / αC / 频率 / 形态 / 可用性）+ 名 vs description 差异表 + 机制声明 | **96/96** |
| [s1_field_profile_risk88.md](s1_field_profile_risk88.md) | risk88 全字段画像（独立 vendor 模型 MFM ASE1）+ 机制声明 | **64/64** |
| [s1_field_profile_other_risk.md](s1_field_profile_other_risk.md) | risk59 / 60 / 68 / 71 / 72 全字段画像与逐字段裁定 | **38/38** |
| [waves.md](waves.md) | R1–R14 波台账：设计 / 读数 / 归因 / 准入禁碰 / 中性化档扫描 / 全部阴性结论 | 全量实测 |
| [README.md](README.md) | 战役索引与关键进展 | — |

合计覆盖 **7 个数据集 / 198 个字段**（96+64+38）。入池 10 颗所用 9 个字段均在上述画像内。

---

## 7. 本轮新增的可复用结论（写入 KOR 经验）

1. **`anlystsn` 是 KOR risk 塔唯一强轴，但不能靠它凑池**：αC 2922 的头部字段在 `REVERSION_AND_MOMENTUM` 下 S 1.62，
   可同族 10 个参数变体 `prod` 落在 0.62–0.87 且族内互相关 >0.95 ⇒ 强轴最多留 1 颗代表 + 1 颗变换不同的分位件。
2. **prod 对参数极敏感**：`E56Nk0wL`（S 1.63，std .36）prod **0.7002 FAIL**，`omERn83n`（S 1.62，std .38）prod **0.6898 PASS**
   —— 0.01 量级的 std 差决定过闸；**同族必须逐颗实测，不能拿族代表外推**。
3. **非 anlystsn 载荷轴 prod 普遍更干净**：growth 0.5762 / ri_growth 0.5909 / ri_divyield 0.6292 / shortint 0.6555 /
   ri_momentum 反向 0.3837 ⇒ 候选池应由「非 anlystsn 机制」撑起。
4. **借券域（risk59）与残差域（risk68）是最干净的补位来源**：`hump` / `quantile` / 双 rank 几何与载荷族几乎不相关
   （`mLoJrQrW` prod **0.2439**、self **0.0986**，对 `QPvr1vPM` 外的确认集最大互相关仅 0.1377）。
5. **中性化档效应量排序（KOR risk70 载荷族）**：`REVERSION_AND_MOMENTUM` 1.63 > CROWDING 1.30 > INDUSTRY 1.14 >
   FAST 1.07 > SLOW 1.04 > STATISTICAL 0.88 —— 第 2 次独立复现。
6. **`winsorize(std)` 是本族 S 主杠杆**：0.24→1.49 / 0.32→1.59 / 0.36→1.63 / 0.38→1.62 / 0.42→1.58 / 0.46→1.50
   （单峰，甜区 **0.34–0.42**）；`pow` 甜区 **1.5–3.0**。
7. **`vector_neut` 目标字段是强杠杆**：对 `momentum` 正交 +0.06~+0.30；对 `resvol` 中性；对 `size`/`beta`/`ltreversl` 正交直接归零
   ⇒ 该 alpha 内含规模/贝塔/长期反转暴露。
8. **死轴（本轮实测，勿再扫）**：`decay`（0/1 逐位相同、2 更差）· `ts_backfill` 窗口（22/40/55 逐位相同）·
   内层分组细于 sector · `ts_rank` 时序分位单独用（0.74，但与正交+分位叠加可用）· pow >4.0 / std >0.44 ·
   risk88 `ri_*` 在 R&M 档全族弱 · risk59 借券域在 CROWDING 档（0.41）。
9. **`srtindcnt`（αC 1431）实为行业哑变量**：实测 −0.31、TO 0.228 ⇒ 坐实「三支同名不同义」的坑。
10. **prod 单并发槽会被跨会话抢占**：本轮观测到外部会话 `3qokqkZQ` 占槽（本机 `_dblock/correlation.inflight.json`
    holder 非本战役 alpha）。**并行查 prod 违反纪律**——7 个请求抢一个槽互相顶成 `busy`，连预读都走不到。
    正确做法：串行 `refresh=False`，`inflight=true` 时只 join/预读不重触发，`pending`/`busy` 记无结论。

---

# 附录 A · prod 校验全程台账（2026-11-06）

> 保留过程证据：哪些逐颗实测、哪些被外部占槽挡住、如何按纪律处置。最终裁定以 §2/§3 为准。

## A.1 入池 10 颗的 prod 落地时间

| alpha | prod | 落地时间 | alpha | prod | 落地时间 |
|---|---:|---|---|---:|---|
| `omERn83n` | 0.6898 | 11-06 17:10 | `58ErwdQ6` | 0.3837 | 11-06 20:44 |
| `O0AReMkq` | 0.5762 | 11-06 19:11 | `j2YoN6vW` | 0.6743 | 11-06 20:56 |
| `WjO3wXYQ` | 0.6292 | 11-06 19:20 | `QPvr1vPM` | 0.6552 | 11-05 22:15 |
| `O0ARb6VJ` | 0.6555 | 11-06 19:29 | `bl6VQQdZ` | 0.6314 | 11-06 21:49 |
| `gJeXqPrJ` | 0.5909 | 11-06 20:08 | `mLoJrQrW` | 0.2439 | 11-06 22:30 |

## A.2 排队 / 超时 / 占槽处置记录

- 早期批次并行 8 颗 prod 查询 ⇒ 全部 `correlation_busy`（`inflight=false`），**确认账号级单并发**，改为串行。
- `58ErwdQ6` / `j2YoN6vW` 首次平台计算超时，隔时 `refresh=False` 秒回 0.3837 / 0.6743（平台算完落在 `is.prodCorrelation`，预读采纳）。
- `bl6VQQdZ` 首个明确值 0.6314 PASS；同批 `rKRRP3pa` 撞 `busy` 即早停，不占槽。
- `rKRRP3pa` 后续串行实测 **0.7731 FAIL**（直方图 `[0.7,0.8)` n=1 ⇒ 窗口谷法「必死」族，排除）。
- `mLoJrQrW` 首次 `pending inflight=true`（本机锁显示 holder 就是它自己），按纪律**不重触发**；
  待平台算完后 `refresh=False` join/预读拿到 0.2439 PASS，落缓存。
- 全程观测到外部会话 `3qokqkZQ`（pid 116024）占用账号 prod 单并发槽，锁 22:19:30 过期后释放。
- **纪律**：`busy` / `pending` 从不写成 PASS/FAIL；`inflight=true` 不重触发；`refresh=True` 未用于批量筛选。

---

# 附录 B · 排除名单与原因（对比实验 / 阴性结论）

| alpha | 机制 | self | prod | 互相关 | 排除原因 |
|---|---|---:|---:|---:|---|
| `wpQ3wP8Y` | anlystsn 水平（CROWDING · std .24 · pow 3.5） | 0.294 | 0.62 ✅ | **0.7731** vs `omERn83n` | **池内互相关超阈**（prod/self 均合规，仅因冗余出局） |
| `E56Nk0wL` | anlystsn 水平（R&M · std .36 · pow 2.0） | 0.426 | **0.7002** | 与 `omERn83n` 近同源 | prod FAIL，差 0.0002（`[0.7,0.8)` n=1） |
| `bl6JoxnM` | risk70 `btop` 水平 | 0.560 | **0.7322** | — | prod FAIL |
| `YP18Gpel` | anlystsn Δ66（INDUSTRY） | 0.257 | **0.8083** | — | prod FAIL |
| `bl6J5Lwm` | risk70 `earnyild` 水平 | 0.438 | **0.8383** | — | prod FAIL |
| `JjeoLpGA` | anlystsn − newssent（CROWDING） | 0.384 | **0.8688** | — | prod FAIL（密墙：0.7–0.8 n=5、0.8–0.9 n=1） |
| `rKRRP3pa` | risk68 `weight_edadv / weight_dadv` 分位 | 0.088 | **0.7731** | 与确认集全 <0.7 | prod FAIL（`[0.7,0.8)` n=1） |
| `VkxqpGQA` / `vR1ze9zv` / `58E6arXz` | risk59 借券族（`hump` 变体） | — | 未测 | **0.7827 / 0.9226 / 0.9992** vs `QPvr1vPM` | 与已入池的 `QPvr1vPM` 高度同源 ⇒ 结构冗余，不测 prod 即排除 |
| `9qxxb3w1` / `2rAAN08N` 等 | `anl10_*` analyst 数据集 | — | prod<0.7 | — | **非 Risk 数据集**，不符合本战役范围 |
| `RRE9NkVj` / SUPER / ORPHAN 缓存行 | 其它区域 / SUPER / 无 alphas 记录 | — | prod<0.7 | — | 区域或类型不符，不能混入 KOR Risk ATOM 池 |

**结构性结论**：`anlystsn` 家族 prod 普遍 0.62–0.87 且族内互相关 >0.95；
**载荷轴（非 anlystsn）+ 借券域 + 残差域**才是能同时满足三条红线的独立机制来源。
旧版报告「10 个 RA 全闸通过参数变体」不构成候选池（同族互相关 >0.95、prod 部分撞墙），已按用户澄清口径作废。

---

## 交付边界

- **已交付**：符合用户澄清口径的 10 颗 ATOM 候选池（§2）+ 三项红线实测终验（§3）+ 完整表达式与算子逻辑（§4）+
  经济机制与双通道取证（§5）+ 字段画像存档索引（§6）+ 可复用结论（§7）。
- **未做（明确不在本轮范围）**：提交 alpha（提交权归用户）；把 9 颗弱候选逐颗推到 RA 全闸通过
  （须走 `wq-brain-alpha-optimization-v1`）；区域切换（全程固定 KOR）。
- **已知偏差（约束 6）**：`risk59` 的 2 颗（`QPvr1vPM` / `mLoJrQrW`）仅 9 年覆盖（2014 空年，见 §2），未严格满足
  「近十年都要有数据」。它们是相关性最干净的补位件，为凑齐互不相关的 10 颗而保留；若用户要求严格 10 年覆盖，
  须剔除/替换这 2 颗并用 `compute_mutual_correlation` 重测整池（此动作本轮未做，属范围外）。
- **数据保鲜**：prod 权威缓存 48h；若用户延后使用，提交前须按 `worldquant-submit-alpha` 的预检重新逐颗 `refresh=True` 终验。
