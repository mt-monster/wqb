# fundamental6（GBR / TOP700 / D1）字段画像与 10 模板池

> 目标：点亮 **GBR/D1/FUNDAMENTAL**（本季度 0/3，是 GBR 唯一还有余量的未亮塔）。
> 约束：REGULAR 提交线；近十年有数据；禁止 PV/MODEL/OTHER 两两组腿；白名单窗口
> `1/5/22/66/252/504/1008/1260`，白名单外（168/56）须给经济解释 + 实测证据。
> 本文只登记**实测过或已取证**的内容，未验证项显式标注。

---

## 0. 一句话结论（截至 2026-10-30）

`fundamental6` 是一个**纯会计科目池**（197 个 MATRIX，全是 Compustat 原始报表行项目，**没有现成比率**），
所以所有信号都必须自己 `divide`。它最大的结构特征是：**全字段同单位（货币）⇒ 同单位相除天然无量纲，
不需要任何 ε**，这直接满足 `unit_handling=VERIFY` 的硬约束。

**已实测的硬结论**：只用会计科目做分母（总资产）时，论坛「位移 + 自历史分位」骨架的产出是
**S 0.78 / eff 0.909**（capex/atq）与 **S 0.61 / eff 0.801**（cfo/atq）。eff 落在成功模板区间
（0.87–1.24 的下沿附近），说明**字段有收益承载能力、换手与 margin 都健康（TO 4%、margin 16.5bp），
缺的是信号强度**。而同骨架换成价格分母（cap）后论坛实测 S 2.36 ⇒ **缺口几乎全部在「分母有没有价格成分」**。

---

## 1. 数据集画像

| 项 | 值 |
|---|---|
| dataset id | `fundamental6` |
| GBR coverage | **0.4969**（GBR 12 个 fundamental 数据集中最高） |
| 字段数 | **197**（全 MATRIX，`platform_count=197`、`complete=true`） |
| 平台 alphaCount | 4069 |
| 字段类型 | 全部 MATRIX，**无 VECTOR** ⇒ 不需要 `vec_*` 包装 |
| 单位 | 全货币（同族）⇒ 同单位相除无量纲 |
| 数据形态 | 年度（`*y` / `*a` 后缀）+ 季度（`*q` 后缀）并存，平台按 point-in-time 前向填充成日频 |

**取数命令（已验证可复现）**
```
mcp__wq-brain-http__get_datafields(region="GBR", universe="TOP700", delay=1,
  dataset_id="fundamental6", filter_sharpe=false, max_fields=200)
# → complete:true / platform_count:197 / pages_fetched:4
```

### 1.1 覆盖率分层（字段级 coverage，实读）

**高覆盖 >0.65（可当主信号）**
`fnd6_iby` 0.7133 · `fnd6_piy` 0.7132 · `fnd6_newq_seqq` 0.7129 · `fnd6_newq_lseq` 0.7113 ·
`fnd6_cptnewq_atq` 0.7107 · `fnd6_ewq_teqq` 0.7100 · `fnd6_ibsa` 0.7074 · `fnd6_pisa` 0.7074 ·
`fnd6_newq_cheq` 0.6979 · `fnd6_revty` 0.6966 · `fnd6_newa2_seq` 0.6956 · `fnd6_newa2_oibdp` 0.6909 ·
`fnd6_newa2_oiadp` 0.6897 · `fnd6_teq` 0.6883 · `fnd6_revtsa` 0.6881 · `fnd6_ibmiiy` 0.6879 ·
`fnd6_ewq_eqrtq` 0.6851 · `fnd6_txty` 0.6850 · `fnd6_ewq_ibmiiq` 0.6838 · `fnd6_ibmiisa` 0.6835 ·
`fnd6_newa2_revt` 0.6824 · `fnd6_newa2_pi` 0.6814 · `fnd6_newq_aoq` 0.6816 ·
`fnd6_newa2_xint` 0.6808 · `fnd6_newa2_re` 0.6806

**中覆盖 0.50–0.65（论坛已验证过的一批）**
`fnd6_dpy` 0.6173 · `fnd6_cptnewq_dlttq` 0.6017 · `fnd6_newq_capsq` 0.5867 · `fnd6_newq_apq` 0.5740 ·
`fnd6_saley` 0.5570 · `fnd6_oancfy` 0.5557 · `fnd6_cptnewq_ltq` 0.5550 · `fnd6_salesa` 0.5526 ·
`fnd6_gpy` 0.5516 · `fnd6_fincfy` 0.5508 · `fnd6_oibdpy` 0.5379 · `fnd6_dfxay` 0.5368 ·
`fnd6_idity` 0.5361 · `fnd6_cptnewq_revtq` 0.5354 · `fnd6_ewq_lltq` 0.5353 · `fnd6_newa2_txp` 0.5348 ·
`fnd6_newa2_wcap` 0.5345 · `fnd6_newa2_sale` 0.5342 · `fnd6_newa2_txditc` 0.5333 · `fnd6_txdb` 0.5333 ·
`fnd6_xoprsa` 0.5325 · `fnd6_newa2_xido` 0.5322 · `fnd6_newa2_xsga` 0.5320 · `fnd6_xopry` 0.5420 ·
`fnd6_dpcy` 0.5419 · `fnd6_xacc` 0.5384 · `fnd6_rectr` 0.5471 · `fnd6_xopr` 0.5472 ·
`fnd6_newa2_rect` 0.5473 · `fnd6_nopi` 0.5476 · `fnd6_cptnewq_ceqq` 0.5458 · `fnd6_newq_dlcq` 0.5459 ·
`fnd6_newq_loq` 0.5447 · `fnd6_gpsa` 0.5441 · `fnd6_cptnewq_ibq` 0.5428 · `fnd6_newq_piq` 0.5428 ·
`fnd6_newq_rectq` 0.5569 · `fnd6_newq_rectrq` 0.5470 · `fnd6_newq_ltmibq` 0.5601 ·
`fnd6_newq_ancq` 0.5596 · `fnd6_cptnewq_actq` 0.5594 · `fnd6_newq_lctq` 0.5567 ·
`fnd6_nopisa` 0.5562 · `fnd6_chechy` 0.5560

**低覆盖 <0.35（慎用，仅供多样化，不作主信号）**
`fnd6_dvty` 0.4117 · `fnd6_dvy` 0.3216 · `fnd6_ewq_dvtq` 0.2686 · `fnd6_newa2_xrd` 0.2524 ·
`fnd6_newq_tstkq` 0.2210 · `fnd6_purtshr` 0.2141 · `fnd6_eieacy` 0.1804 · `fnd6_ivchy` 0.1627

### 1.2 拥挤度（alphaCount，尽量避开 >500）

| 最拥挤（回避或只做对照） | 最蓝海（值得优先试） |
|---|---|
| `fnd6_revty` 718 · `fnd6_cptnewq_atq` 653 · `fnd6_gpy` 589 · `fnd6_capxy` 579 · `fnd6_oancfy` 526 · `fnd6_dpy` 443 | `fnd6_mibn` 1 · `fnd6_miisa` 1 · `fnd6_miiy` 1 · `fnd6_newa2_xrd` 1 · `fnd6_psfixy` 1 · `fnd6_sppivy` 1 · `fnd6_newq_tstkq` 1 · `fnd6_xoproq` 1 · `fnd6_eieacy` 2 · `fnd6_ivaoq` 2 · `fnd6_ewq_mibnq` 2 · `fnd6_newq_miiq` 2 · `fnd6_newq_xoprq` 2 · `fnd6_xlr` 2 · `fnd6_txw` 3 · `fnd6_xstfws` 3 · `fnd6_psfix` 3 · `fnd6_ivacoy` 3 · `fnd6_ewq_ivaeqq` 3 · `fnd6_xoprosa` 3 · `fnd6_xoproy` 3 |

> **纪律**：拥挤度只在 **prod 阶段**考虑，不在 IS 探索阶段预筛字段。IS 阶段先找信号，
> 撞 prod 再换同族更冷门的字段。

---

## 2. 分母（价格成分）的三种来源 —— 这是本数据集最关键的结构决策

论坛帖 `44089095804439` 已证明：GBR 上**水平版估值比率几乎不产生 alpha**（`rank(EBITDA/EV)` S 仅 0.53），
必须位移化 + 自历史分位标准化才跳到 2.71；而且作者自己做了安慰剂检验：
**`Δ(1/市值)`（纯价格位移、零基本面信息）单独就有 S 1.89**。

⇒ **Δ比率的 Sharpe 里有一大块是「价格位移/反转」，不是基本面。**
本轮的资产口径实测把这块彻底剥离了：

| 分母 | 价格成分 | 塔位 | 实测 S | eff | 数据来源 |
|---|---|---|---|---|---|
| `fnd6_cptnewq_atq`（总资产） | 无 | 纯 FUNDAMENTAL | **0.78**（capex） | 0.909 | 本轮 `npv0wG7d` |
| `fnd6_cptnewq_atq`（总资产） | 无 | 纯 FUNDAMENTAL | **0.61**（cfo） | 0.801 | 本轮 `78LOglZv` |
| `cap`（PV 市值） | 有 | PV + FUNDAMENTAL | 待测 | — | 论坛 `fnd6_capxy/EV` 2.36、`fnd6_oancfy/市值` 1.65 |
| **`fnd45_mktcap`** | 有 | **纯 FUNDAMENTAL** | 待测 | — | `fundamental45`，cov 0.2981 |

### 2.1 `fnd45_mktcap` 是一个重要的结构性发现

```
mcp__wq-brain-http__get_datafields(... dataset_id="fundamental45")
→ fnd45_mktcap  type=MATRIX  coverage=0.2981  alphaCount=11
   "Market capitalization of the company at the relevant reporting time"
```

它在 **`fundamental45`（category = fundamental）** 里，是**真市值字段**。用它当分母：
- 表达式里只出现 FUNDAMENTAL 类字段 ⇒ **只登记 GBR/D1/FUNDAMENTAL 一座塔**；
- **不引入 PV 塔** ⇒ 不触碰「PV/MODEL/OTHER 两两禁混」；
- **不消耗「trio × 非 trio ≤ 5」配额**。

代价：coverage 仅 **0.2981**（且是报告时点稀疏），叠加 `fnd6` 的 0.55–0.71 后有效样本可能只剩
~150–200 只（TOP700 的 1/4）。**`CONCENTRATED_WEIGHT` 风险显著上升**——这也是 GBR 第一大杀手
（本地 20,746 条 sim 统计：GBR `CONCENTRATED_WEIGHT` 挂 54.2%，跨区均值 42.0%）。

### 2.2 `fundamental17` 判死（EV 的原始来源）

`get_datafields(dataset_id="fundamental17")` 首 15 个字段（含 `annual_ebitda_value`、
`annual_common_equity_value`、`annual_debt_to_equity_ratio`）**coverage 全为 0.0**
⇒ 论坛作者的 EV/市值 分母在 GBR 无法直接复现，必须换成 `cap` 或 `fnd45_mktcap`。

### 2.3 一个必须记住的读数陷阱

`get_datafields` 返回的 `coverage` **在 pv1 上整集全是 0.0**（`cap` / `close` / `returns` / `volume` /
`vwap` 无一例外），但这些字段显然有数据（本轮 sim 已用 `cap`）。
⇒ **GBR 的 `coverage` 列在部分数据集上不填充，`coverage=0` 不等于「无数据」。**
判「字段有没有数据」的可靠办法是**跑一条最简 sim 看 TO 与 longCount**（TO 精确等于 0.0 ⇒ 无数据，
已在 `earnings6.eps_change_percentage_value` 上验证过这个判据）。

---

## 3. 十个结构互异的模板（T1–T10）

**结构族定义**（互异性的判据在**算子骨架**，不在字段）：

| 族 | 骨架签名 | 经济含义 |
|---|---|---|
| F1 | `rank(ts_quantile(ts_av_diff(divide(F,D),N),M))` | 位移 + 自历史分位（论坛 hero 族） |
| F2 | `group_rank(divide(F,D), industry)` | 水平截面 + 行业内排序 |
| F3 | `subtract(rank(ts_delta(A,W)), rank(ts_delta(B,W)))` | 双分量差（背离 / 质量缺口） |
| F4 | `rank(divide(A, ts_std_dev(B,63)))` | 信号 ÷ 不确定性（论坛 T2） |
| F5 | `ts_ir(divide(F,D), W)` | 时序信息比率（稳定性加权） |
| F6 | `trade_when(cond, signal, -1)` | 条件门控（只在满足会计条件时下注） |
| F7 | `group_zscore(divide(F,D), industry)` | 行业内 z（对离群更敏感） |
| F8 | `rank(ts_quantile(x, M1))` 与 `rank(ts_quantile(x, M2))` 之差 | 双尺度分位共振差 |
| F9 | `if_else(greater(...), A, B)` | 分域切换（按会计状态换信号） |
| F10 | `ts_decay_linear(group_rank(...), W)` | 分组排序 + 线性衰减平滑 |

---

### T1 · 价值收益率的位移（论坛已验证骨架）｜族 F1

```
rank(ts_quantile(ts_av_diff(divide(<分子>, <分母>), 168), 56, driver=gaussian))
```
- **分子候选**：`fnd6_capxy`（资本开支）/ `fnd6_oancfy`（经营现金流，论坛 1.65、prod 0.56）/
  `fnd6_oibdpy`（论坛 1.66）/ `fnd6_gpy`（毛利，论坛 1.88，窗口 336/112）
- **分母**：`cap`（PV+FUND，有配额成本）或 `fnd45_mktcap`（纯 FUND，cov 低）
- **窗口依据**：168 ≈ 8 个月 ≈ 1.33 个 UK 半年报周期；论坛实测网格 84/28→2.07、**168/56→2.71**、252/84→2.43。
  **不在白名单，已具备经济解释 + 实测峰值证据。**
- **已死参数**：`driver`（以 `rank` 结尾时 `ts_quantile` 输出是经验分位的单调映射，gaussian↔uniform 逐位一致）。
- **已测**：资产口径 S 0.78（`npv0wG7d`）/ 0.61（`78LOglZv`）。

### T2 · 投资强度变化（投资异象）｜族 F1 的纯会计变体

```
multiply(-1, rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, fnd6_cptnewq_atq), 168), 56)))
```
- **论文**：Titman-Wei-Xie (2004) *Capital Investments and Stock Returns* —— 高资本开支 → 低未来收益。
- **待验证**：本轮 `npv0wG7d`（**正方向**）S **+0.78** ⇒ 与论文方向**相反**。
  须先做符号稳定性检查（全期 S 与 2Y 同号）再反转，不得直接翻。

### T3 · 应计异象（Sloan 1996）｜族 F1 + 双字段差

```
multiply(-1, rank(ts_quantile(ts_av_diff(divide(subtract(fnd6_iby, fnd6_oancfy), fnd6_cptnewq_atq), 168), 56)))
```
- **论文**：Sloan (1996) *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?*
- 应计 = 净利 − 经营现金流；高应计 → 低未来收益。
- 单位：`fnd6_iby`、`fnd6_oancfy`、`fnd6_cptnewq_atq` 全货币 ⇒ `subtract` 合法、`divide` 无量纲。
- **注意**：论坛帖 `43622167691287` 已记录「应计异象在 USA 实测失效」，GBR 未测 ⇒ 必须当**未验证**处理。

### T4 · 毛利率水平（Novy-Marx 2013）｜族 F2

```
group_rank(divide(fnd6_gpy, fnd6_cptnewq_atq), industry)
```
- **论文**：Novy-Marx (2013) *The Other Side of Value: The Gross Profitability Premium*.
- **预警**：这是**水平版**，论坛在 GBR 实测水平版估值比率 S 仅 0.53 ⇒ **预期低产**。
  保留它的理由是**结构多样性**（F2 族）与「毛利率 ≠ 估值」不属同一机制的证伪需求。
- 拥挤度警示：`fnd6_gpy` alphaCount 589、`fnd6_cptnewq_atq` 653 —— 高拥挤，prod 风险高。

### T5 · 留存收益 / 股东权益（内部融资能力）｜族 F2

```
group_rank(divide(fnd6_newa2_re, fnd6_newq_seqq), industry)
```
- **依据**：论坛帖 `42660089368343`（30 赞）推荐「每股留存收益变化不受规模影响，是好截面信号」。
- 覆盖率：`fnd6_newa2_re` 0.6806 / `fnd6_newq_seqq` 0.7129（双高）。
- **经济含义**：留存收益占权益比重高 ⇒ 靠内生积累而非外部融资 ⇒ 质量高、稀释风险低。

### T6 · 收入质量（应收增速 vs 营收增速）｜族 F3

```
multiply(-1, subtract(rank(ts_delta(divide(fnd6_newq_rectq, fnd6_cptnewq_atq), 252)),
                      rank(ts_delta(divide(fnd6_cptnewq_revtq, fnd6_cptnewq_atq), 252))))
```
- **依据**：应收增速持续快于营收增速 ⇒ 放宽信用条件换收入 ⇒ 后续减值风险（DSRI 思想）。
- **单位闸**：`fnd6_newq_rectq`（应收）与 `fnd6_cptnewq_atq`（总资产）同货币 ⇒ 除后无量纲；
  两个 `rank` 相减合法（`subtract(rank, rank)` 属放行形态）。
- **窗口 252**（1 年）在白名单内。

### T7 · 有效税率异常（税收规避）｜族 F2

```
multiply(-1, group_rank(divide(fnd6_newa2_txp, fnd6_newa2_pi), industry))
```
- **论文**：Dyreng-Graham-Hanlon (2010) *The Effects of Executives on Corporate Tax Avoidance*.
- `fnd6_newa2_txp`（税费）0.5348 / `fnd6_newa2_pi`（税前利润）0.6814。
- **单位闸**：同货币相除 ⇒ 无量纲。`pi` 可能为负 ⇒ 分母负值会让比率翻转，
  **须先测再判**（若噪声大，改用 `multiply(-1, group_rank(divide(txp, abs(pi)), industry))` 的绝对值变体，
  但那会引入 `abs` 对符号信息的破坏，需对比实验）。

### T8 · 经营现金流 / 净利（盈利质量）｜族 F4（信号 ÷ 不确定性）

```
rank(divide(divide(fnd6_oancfy, fnd6_iby),
            ts_std_dev(divide(fnd6_oancfy, fnd6_iby), 63)))
```
- **依据**：论坛 T2 模板「信号 ÷ 不确定性」。消融证据：分母单独 S **−1.22**（只能当调制器，不能当信号）。
- 窗口 63 是论坛原值（**不在白名单**）；若不合规可换 **66**（白名单内，与原值仅差 3 天）。
  **优先用 66**，避免再造一个白名单外窗口。
- **经济含义**：CFO 长期高于净利 ⇒ 应计少、现金流实。除以自身波动 ⇒ 奖励**稳定**的高质量，不奖励一次性的。

### T9 · 分域切换：盈利公司看价值、亏损公司看成长｜族 F9

```
if_else(greater(fnd6_iby, 0),
        rank(ts_quantile(ts_av_diff(divide(fnd6_oancfy, fnd6_cptnewq_atq), 168), 56)),
        rank(ts_quantile(ts_av_diff(divide(fnd6_revty, fnd6_cptnewq_atq), 168), 56)))
```
- **经济含义**：资产口径的现金流收益率对**盈利公司**有意义（分母为正、比率可比）；
  对**亏损公司**该比率符号会翻转，此时改用「收入/资产」的周转改善更稳健。
- `greater(x, 0)` 是合法算子（已确认）；`if_else` 已确认存在。
- **风险**：`greater(fnd6_iby, 0)` 里 `fnd6_iby` 带货币单位、`0` 无量纲 ⇒ **单位闸可能报错**
  （本轮已在 `add(total_top_buy_shares, 0.0001)` 上踩过同款坑）。
  **替代写法**：`if_else(greater(divide(fnd6_iby, abs(fnd6_iby)), 0), A, B)` —— 但 `abs(fnd6_iby)` 可能为 0。
  **更稳的替代**：用 `fnd6_iby` 与自身均值的比较 `greater(fnd6_iby, ts_mean(fnd6_iby, 252))`（同单位，合法）。
  **派发前必须先过 preflight。**

### T10 · 分组排序 + 线性衰减（低换手平滑）｜族 F10

```
ts_decay_linear(group_rank(divide(subtract(fnd6_newa2_revt, fnd6_newa2_xsga), fnd6_cptnewq_atq), industry), 22)
```
- **经济含义**：`(营收 − 销售管理费用) / 总资产` ≈ 扣除销售费用后的资产经营效率；
  再对行业内排序做 22 日线性衰减，压换手。
- **窗口 22**（1 个月）在白名单内。
- **注意**：`ts_decay_linear` 是「砍不掉低质量交易」的平滑，**按 fitness 恒等式 `F ∝ S × sqrt(margin)`，
  单纯平滑不改变 margin、只降 TO 与 returns ⇒ fitness 几乎不动**。所以这条模板的定位是
  **降换手以过 `LOW_TURNOVER` 或压 prod**，不是提 fitness。

---

## 4. 窗口白名单的用法

| 窗口 | 依据 | 状态 |
|---|---|---|
| 5 | 1 周 | 白名单 |
| 22 | 1 个月 | 白名单 |
| 66 | 1 季度 | 白名单 |
| 252 | 1 年 | 白名单 |
| 504 | 2 年 | 白名单 |
| 1008 | 4 年 | 白名单 |
| 1260 | 5 年 | 白名单 |
| **168 / 56** | **≈8 个月 / ≈2.7 个月**；168 ≈ 1.33 个 UK 半年报周期（126×4/3）；论坛实测网格峰值 84/28→2.07、**168/56→2.71**、252/84→2.43 | **白名单外，已具备经济解释 + 实测峰值证据** |
| 336 / 112 | 论坛 `fnd6_gpy/市值` 用 336/112 得 1.88（168/56 的 2 倍，保持 3:1） | 白名单外，**仅当复用同一骨架时引用论坛证据** |

> **反向警告（论坛 MY27687 提出）**：168/56 的 3:1 可能有第三个解释 ——
> **重叠窗口自相关长度**，而不是 UK 半年报节奏。`ts_av_diff` 横跨 ≥168 天，M=56 窗口里几乎没有独立样本，
> `ts_quantile` 更接近「逐股票时序标准化」。**便宜的判据**：换成
> `rank(ts_zscore(ts_av_diff(x,168), 56))` 看是否仍在 2.6–2.7；固定 N=168 只扫 M∈{28,42,56,84,112}。
> 本区暂未做这个判据 ⇒ 结论标「待证」。
> **部分已答（2026-10-30 GBR 实测）**：把位移锚从 `ts_av_diff` 换成 `ts_zscore`（同为 168 窗口的
> 标准化位移，等价于「位移幅度 ÷ 自身波动」），S 从 **1.98 → 1.70（−14%）**，方向与论坛
> EV/市值 2.71 → 2.28（−16%）一致 ⇒ **位移要用幅度，不要用 z 值**这条在 GBR 复现成立。

### 4.1 两条窗口的最优组合：252 / 84（2026-10-30 GBR 实测，同分子同骨架）

| 位移 W1 | 分位 W2 | alpha | S | F | 2Y | DD | margin | failed_ra |
|---|---|---|---|---|---|---|---|---|
| 168 | 56 | `P0oerpjp` | 1.98 | 1.70 | 2.10 | 5.75% | 22.31bp | 0 |
| **252** | **84** | **`rKRkL9QE`** | **2.21** | **2.05** | **2.51** | **5.44%** | **25.94bp** | **0** |
| 168 | **252** | `rKRkLqda` | **1.24** | 0.88 | 1.04 | 6.18% | 21.44bp | 3 |

**结论一：W1 与 W2 同步放大 1.5 倍（168/56 → 252/84）全面更优** —— S/F/2Y/DD/margin 六项同时改善。
经济解释：`fnd6_capxy` 是**年度级**变量，252 = 完整会计年度；168 ≈ 8 个月只跨 1.33 个 UK 半年报
周期，等于把两个报告期的资本开支混在一个位移里。**这条推翻论坛在该数据集上的 168/56 峰值结论**
（论坛用 EV/市值分母，价格成分的更新频率与会计年度不同步，故其最优窗口偏短）。

**结论二：W2（分位窗口）不是独立的降相关旋钮** —— W2 从 84 拉到 252（3 倍）不但没换来
「低相关的高质量变体」，反而把 S 砍到 1.24、2Y 砍到 1.04、并新增 3 项 RA 失败。
机理：`ts_quantile` 的分位是**逐股票自历史经验分布**，窗口越长，分布越平滑 ⇒ 当期位移被压到
分布中段 ⇒ 信号幅度衰减。**W2 的作用是「把位移幅度映射成稳健分位」，不是「换时间尺度」；
真正的尺度旋钮只有 W1。**
⇒ 降相关仍然只能靠 **W1 跨度 ≥3–4 倍** 或 **换位移算子**（见 §8 三轴表）。

---

## 5. 单位闸自查表（`unit_handling=VERIFY`）

| 写法 | 是否合法 | 说明 |
|---|---|---|
| `divide(货币, 货币)` | ✅ | 天然无量纲，**不需要 ε** |
| `divide(股数, 股数)` | ✅ | 同族约掉 |
| `add(带单位字段, 0.0001)` | ❌ | 必挂：`Incompatible unit for input of "add" at index 1, expected "Unit[CSShare:1]", found "Unit[]"` |
| `subtract(带单位, 带单位)` | ✅ | 同单位相减合法 |
| `greater(带单位, 0)` | ⚠️ | 未验证，**必须 preflight** |
| `subtract(无量纲, 带价格单位)` | ❌ | `earnings6` 已实证：EPS 无量纲 vs 区间边界带 `Unit[CSPrice:1]` |
| `divide(带单位, abs(带单位均值))` | ⚠️ | 语法合法但会把信号抹平（借券费率实测 S 1.89→0.61） |

**`fundamental6` 的特权**：全字段同货币单位 ⇒ **任何两个 fnd6 字段相除/相减都合法**，
这是它比 `earnings6`（同集内单位不一致）好用得多的根本原因。

---

## 6. 已证伪 / 不要重试

| 写法 | 结果 | 出处 |
|---|---|---|
| 水平版估值比率（`rank(EBITDA/EV)`） | S **0.53** | 论坛 `44089095804439` |
| 位移但无自历史分位（`rank(ts_av_diff(x,168))`） | S **0.71** | 同上 |
| 自历史分位但无位移（`rank(ts_quantile(x,56))`） | S **0.95** | 同上 |
| 先 `rank` 再位移 | S **2.22**（vs 2.71） | 同上，rank 把当期截面构成混进时序 ⇒ **伪位移** |
| `ts_zscore(x,168)` 作位移锚 | S **2.28**（vs 均值锚 2.71） | 同上，位移用**幅度**不用 z 值 |
| `driver` 换档 | 逐位一致（S 2.71=2.71、PnL 相同） | 同上，**死参数** |
| `Δ(1/市值)` 安慰剂 | S **1.89**；风险中性化后仅 **0.51** | 同上，**变换层自带价格反转分量** |
| 资产口径位移（capex/atq） | S **0.78** / eff 0.909 | 本轮 `npv0wG7d` |
| 资产口径位移（cfo/atq） | S **0.61** / eff 0.801 | 本轮 `78LOglZv` |
| `fnd6_M1_accrual_sloan`（水平应计）/ `fnd6_M2_gross_profitability`（水平毛利率） | 设计即被水平版证伪，429 后**不补派** | 本轮决策 |

---

## 7. 提交前必须过的闸（GBR 实测阈值）

| 闸 | 平台 limit（本轮 `checks.fail` 实读） | 备注 |
|---|---|---|
| `LOW_SHARPE` | **1.58** | 全期 |
| `LOW_FITNESS` | **1.00** | 全期 |
| `LOW_2Y_SHARPE` | **1.58** | 本轮实读 limit 就是 1.58（TO<30% 的 ×0.85 豁免口径待复核，见 memory） |
| `CONCENTRATED_WEIGHT` | — | **GBR 第一大杀手**，本地统计挂 54.2% |
| `CLUSTER_TEST` | 1.00 | `npv0wG7d` 实测 warning 0.73 |
| `LOW_SUB_UNIVERSE_SHARPE` | — | `npv0wG7d` 实测 **pass**（0.91） |
| prod | **< 0.70** 严格不等式 | 无任何豁免入口 |
| self | **< 0.70** | — |
| 数据跨度 | **2014–2023 十年都要有 `longCount>0`** | 唯一可靠判据是 `get_alpha_yearly_stats` |

> **`eff = fitness / sharpe = sqrt(returns / max(turnover, 0.125))`** 是独立于 Sharpe 的第二条轴。
> - eff 高而 S 低 ⇒ **信号强度问题**，调骨架/换算子有意义。
> - eff 比成功模板低一个数量级 ⇒ **字段没有收益承载能力**，换字段，别扫设置。
> 本轮 capex/atq 的 **eff 0.909** 说明是前者。

---

## 8. 待补的证据缺口

1. **`fnd45_mktcap` 实际有效样本数**：coverage 0.2981 只是字段级，叠加 `fnd6` 后的交集未知。
   看 sim 的 `longCount + shortCount` 与 `CONCENTRATED_WEIGHT` 是否 pass 即可判。
2. **168/56 的 3:1 是否只是自相关长度**（MY27687 的三条便宜判据未做）。
3. **`greater(带单位字段, 0)` 是否过单位闸**（T9 依赖它）。
4. **`fnd6_newa2_txp / fnd6_newa2_pi` 在 `pi<0` 时是否离散翻转**（T7 风险点）。
5. **`fundamental45` 的十年数据跨度**：cov 0.2981 不代表 2014 年就有数据，须 `get_alpha_yearly_stats` 逐年核。

---

## 9. 实测结果矩阵（GBR / TOP700 / D1 / INDUSTRY / decay 10 / trunc 0.05 / nanHandling OFF）

### 9.1 全量探针台账

| tag | alpha | 表达式核心 | S | F | 2Y | TO | SUB | DD | margin | eff | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **CAPX_CAP** | **`P0oerpjp`** | `rank(ts_quantile(ts_av_diff(capex/cap,168),56))` | **1.98** | **1.70** | **2.10** | 8.26% | 1.70 | 5.75% | 22.31bp | **1.057** | **0** |
| CFO_CAP | `xArM96LW` | `…ts_av_diff(oancfy/cap,168)…` | 1.54 | 1.14 | 2.08 | 7.81% | 1.58 | 5.74% | 17.63bp | 0.939 | 1 |
| GP_CAP | `0mYo9Ok1` | `…ts_av_diff(gpy/cap,168)…` | 1.73 | 1.39 | 1.47 | 8.41% | 1.55 | 5.30% | 19.27bp | 0.981 | 1 |
| **CAPX_CAP_TDELTA** | **`P0oeqZap`** | `…ts_delta(capex/cap,168)…` | **1.64** | **1.32** | 1.32 | 11.21% | 1.15 | 6.61% | 14.52bp | 0.852 | 1 |
| CAPX_CAP_W66 | `pwd0onEj` | `…ts_av_diff(capex/cap,**66**),**22**…` | 0.83 | 0.47 | 0.54 | 12.63% | 0.23 | 7.29% | 6.39bp | 0.565 | 4 |
| CAPX_ATQ | `npv0wG7d` | `…ts_av_diff(capex/**atq**,168)…` | 0.78 | 0.40 | 1.23 | 4.03% | 0.91 | 17.69% | 16.49bp | 0.909 | 3 |
| CFO_ATQ | `78LOglZv` | `…ts_av_diff(oancfy/**atq**,168)…` | 0.61 | 0.28 | 0.90 | 4.08% | 0.90 | 9.53% | 12.88bp | 0.801 | 3 |
| CAPX_F45MC | `KPJeY9jl` | `…ts_av_diff(capex/**fnd45_mktcap**,168)…` | 0.36 | 0.20 | 0.04 | 12.32% | 0.27 | 15.78% | 6.33bp | 0.563 | 4 |
| **CAPX_CAP_252** | **`rKRkL9QE`** | `…ts_av_diff(capex/cap,**252**),**84**…` | **2.21** | **2.05** | **2.51** | 8.33% | 1.77 | **5.44%** | **25.94bp** | 0.873 | **0** |
| CAPX_CAP_ZSC | `kqNRXm5k` | `…ts_quantile(ts_zscore(capex/cap,**168**),**56**)…` | 1.70 | 1.33 | 2.02 | 7.98% | 1.52 | 6.67% | 19.05bp | 0.965 | **0** |
| ~~CAPX_CAP_Q252~~ | `rKRkLqda` | `…ts_av_diff(capex/cap,168),**252**…` | **1.24** | 0.88 | 1.04 | 5.86% | 0.92 | 6.18% | 21.44bp | 0.815 | 3 |
| ~~CAPX_CAP_TD252~~ | `d5Wq7RJX` | `…ts_delta(capex/cap,**252**),84…` | **0.77** | 0.45 | 0.63 | 10.90% | 0.33 | 13.11% | 7.80bp | 0.624 | 4 |
| ~~CAPX_SPLIT252~~ | `rKRkzdqm` | `…divide(ts_av_diff(capex,**252**), cap),84…` | **1.04** | 0.62 | 1.04 | 6.77% | 0.79 | 8.43% | 13.05bp | 0.769 | 3 |
| **CAPX_GRPRANK** | **`N1NM5WK8`** | `**group_rank**(ts_quantile(ts_av_diff(capex/cap,252),84)**, industry**)` | **2.05** | **1.80** | **2.26** | 8.98% | 1.68 | **5.06%** | 21.40bp | 0.893 | **0** |
| ~~CAPX_AVGCAP252~~ | `leAxRdb8` | `…ts_av_diff(capex/**ts_mean(cap,252)**,252),84…` | **1.08** | 0.68 | 1.35 | 4.10% | 0.86 | 6.30% | 24.35bp | 0.833 | 3 |
| TOBINQ_D252 | 见 §9.2 注 | `…ts_av_diff(**cap/atq**,252),84…` | 在飞 | | | | | | | | |

> `eff = √(returns / max(turnover, 0.125))`。`eff ≥ 0.85` 视为字段有承载能力。

### 9.1b ★★ 机理定论：这个族的引擎是「分母上价格的位移」，分子只是权重

同一骨架、同一设置，只改**分子与分母的结合方式**：

| 构造 | 展开式 | alpha | S | 相对损失 |
|---|---|---|---|---|
| `Δ(F / P)` | `ΔF/P − F·Δ(1/P)` | `rKRkL9QE` | **2.21** | — |
| `Δ(F) / P` | `ΔF/P` | `rKRkzdqm` | **1.04** | **−53%** |
| 纯价格安慰剂 `Δ(1/P)` | `−ΔP/P²` | 论坛值（168/56） | 1.89 | 论坛 `P0oerpjp` 2.71 → 掉 30% |

**⇒ 只要把「分母自身的位移项」拿掉，Sharpe 立刻少一半。** 论坛的安慰剂单独就做到 1.89，
说明 `P0oerpjp` 的 1.98 里几乎全部是 `Δ(1/cap)` 贡献，`fnd6_capxy` 只提供「哪些股票的
价格下跌更值得买」这一层横截面权重。

**这条解释了两件此前分开看的事**：
- 为什么**换分子只能降到 0.8421** —— 所有分子共享同一个 `Δ(1/cap)` 主成分；
- 为什么**纯会计分母（总资产）天花板 0.78** —— 那里没有 `Δ(1/P)` 项。

**⚠ 由此产生的风险判断（写进提交决策）**：本族在数学上高度接近**价格反转因子**。IS 的
2.21 是真实回测值，但 **prod 相关性才是它真正的生死闸** —— 生产池里价格反转类 alpha 极多。
⇒ 提交前必须拿到 prod 实测值，不得用「基本面因子应该低相关」的先验替代。

### 9.2 ★ 降相关轴实测（4 年日收益，1021 点；2026-10-30 更新）

| 对 | 改动维度 | 相关 | 判定 |
|---|---|---|---|
| `P0oerpjp` × `0mYo9Ok1` | **只换分子**（capex→毛利） | **0.8421** | ✗ |
| `P0oerpjp` × `kqNRXm5k` | 换算子（av_diff→**zscore**），同窗口 168/56 | **0.8968** | ✗ |
| `P0oerpjp` × `P0oeqZap` | **换位移算子**（av_diff→`ts_delta`） | **0.5901** | ✓ |
| `P0oerpjp` × `pwd0onEj` | **换窗口尺度**（168/56→66/22） | **0.5522** | ✓ |
| `P0oerpjp` × `rKRkL9QE` | 窗口同步 ×1.5（168/56→252/84） | **0.7510** | ✗（仅超 0.051） |
| **`rKRkL9QE` × `kqNRXm5k`** | 窗口 252/84 avdiff × 168/56 zscore | **0.6099** | **✓** |
| `rKRkL9QE` × `P0oeqZap` | 算子 + 窗口双改 | **0.7546** | ✗ |
| `kqNRXm5k` × `P0oeqZap` | — | 0.4273 | ✓ |
| **`rKRkL9QE` × `N1NM5WK8`** | **换横截面变换** `rank`→`group_rank(·,industry)` | **0.9651** | ✗✗ |
| `kqNRXm5k` × `N1NM5WK8` | 同上（相对 zscore 腿） | 0.5826 | ✓ |

**⇒ 修正后的六条结论**：
1. **换分子在位移族里等于没换**（0.8421）。原因是共享 `Δ(1/cap)` 主成分（见 §9.1b）。
2. **换算子在长窗口下失效，不是通用杠杆** —— `ts_delta` 在 168/56 还能给 1.64（相关 0.59），
   但撑到 252/84 就崩到 **0.77**。机理：`ts_delta` 只比两个单日快照（相隔 12 个月、且中间的
   会计报告期已错位），噪声随窗口单调放大；`ts_av_diff` 比「当前 vs 整段基线」，窗口越长越稳。
   ⇒ **换算子只在短窗口可用，且必须先验证该窗口下强度不掉。**
3. **换窗口尺度降相关最狠但杀强度**（0.55 / S→0.83）。1.5 倍跨度只能换到 0.751，要 <0.70
   需要 **≥3–4 倍跨度**，而 3 倍以上强度就没了。
4. **分位窗口 W2 不是降相关轴**（见 §4.1）：84→252 只把 S 打崩（1.24），相关没换到。
5. **★ 分组轴不能与中性化轴重合**。设置已是 `neutralization=INDUSTRY` 时，
   `group_rank(·, industry)` 把持仓在行业内铺平、随后行业中性化再把行业均值抹掉，两步互相抵消
   ⇒ 实测相关 **0.9651**、S 2.21→2.05（几乎没换位置）。**要用分组轴降相关，分组维度必须
   与中性化维度正交**（如中性化 INDUSTRY 时用 `subindustry`/`sector`，或反过来）。
6. **分母一旦平滑，强度立刻掉**。把 `cap` 换成 `ts_mean(cap,252)`（学年派口径的「年初市值」）
   ⇒ `leAxRdb8` S **1.08**（vs 2.21）。⇒ **当期价格位移是这个族的全部引擎，任何平滑都在拿掉信号。**

**⇒ 本族有效秩 = 3（2026-10-30 晚修正；原判「=2」已过时）**

八条轴全部试过（换分子 / 换算子×2 / 换位移窗口 / 换分位窗口 / 换分母平滑 / 换分组轴 / 分子位移），
加上后来发现的**倒数比 `Δ(cap/F)` 反向簇**，最终成立的互不相关三角是：

| 腿 | alpha | S | F | 2Y | 与另两腿相关 |
|---|---|---|---|---|---|
| `Δ(F/cap)` 正向簇 · 长窗 | `rKRkL9QE` | 2.21 | 2.05 | 2.51 | 0.6099 / 0.5139 |
| `Δ(F/cap)` 正向簇 · zscore 中窗 | `kqNRXm5k` | 1.70 | 1.33 | 2.02 | 0.6099 / 0.2901 |
| `Δ(cap/F)` **倒数反向簇** | `0mYoANkv` | 1.89 | 1.54 | 2.08 | 0.5139 / 0.2901 |

**`compute_mutual_correlation` 对 7 条全闸候选（`rKRkL9QE` / `0mYoANkv` / `6XdxzNb5` /
`kqNRXm5k` / `88RAnmAX` / `9qxoa3mx` / `P0oerpjp`）跑全矩阵，返回
`max_mutually_below_subset_size = 3` 且 `max_subset_exact = true`**
⇒ **这个数据集内最大互不相关团恰好是 3 条，第四条一定撞 0.72+**（最近的是
`rKRkL9QE` × `P0oerpjp` = 0.751、`0mYoANkv` × `88RAnmAX` = 0.772）。

**⇒ 单靠 `fnd6 ÷ cap` 这一族刚好能点亮一塔（3 颗），一颗不多。** 想再点一塔必须换数据集。

**同簇「近重复」实测（换字段真的等于没换）**：

| 对 | 相关 | 原因 |
|---|---|---|
| `9qxoa3mx` × `88RAnmAX` | **0.9584** | 普通股权益 `cptnewq_ceqq` vs 总权益 `ewq_teqq`，同一量只换单位 |
| `kqNRXm5k` × `P0oerpjp` | **0.8968** | 同 capex/cap 168/56 的 zscore vs av_diff |
| `0mYoANkv` × `6XdxzNb5` | **0.8903** | 互为倒数（`Δ(cap/RE)` vs `Δ(RE/cap)`），同一颗 |

**两簇的互相关只有 0.29–0.67，簇内互相关 0.75–0.96** ⇒ 真正能凑团的维度是**簇归属**
（把价格放分母还是放分子），不是换字段、不是换算子。

### 9.3 `P0oerpjp` 十年归因（`get_alpha_yearly_stats` 实读）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 1.97 | 3.38 | 3.61 | 1.72 | 2.28 | **0.74** | 2.11 | **0.22** | 2.15 | 2.09 |
| returns | 6.94% | 12.86% | 16.68% | 6.41% | 10.04% | 3.35% | 13.42% | 1.01% | 13.09% | 8.74% |
| DD | 2.22% | 1.90% | 1.83% | 3.04% | 1.65% | 4.50% | 3.80% | 5.21% | 2.69% | 2.36% |
| longCount | 208 | 210 | 209 | 237 | 233 | 218 | 191 | 219 | 245 | 238 |

**十年全正、longCount 191–245 全部 >0（十年门槛过）**。最弱 2021 年 0.22，最强 2016 年 3.61。
单年最大 PnL 占比 18%（2016），**无单年行情依赖**。最大回撤发生在 2021 年（5.21%），不是 2020 疫情年。

### 9.4 `P0oerpjp` 平台闸全表

```
pass : LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT
       / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST / MATCHES_PYRAMID
warn : MATCHES_THEMES / OSMOSIS_ALLOCATION
fail : （空）
塔位 : GBR/D1/PV (×1.4) + GBR/D1/FUNDAMENTAL (×1.6)，effective 2，pyramid_short = "pv/fundamental"
self : 0.5570（最像 WjAV89jG 0.557；池 18 只，剔 3 只 PowerPool）
prod : 待测（账号级单并发被外部进程长期占用）
```

> **配额提醒**：`P0oerpjp` 用 `cap`（PV）+ `fnd6_*`（FUNDAMENTAL），属「trio × 非 trio」，
> **占用 ≤5 配额中的 1 个**。同族的 `P0oeqZap` / `0mYo9Ok1` / `xArM96LW` 也都用 `cap`，
> 若全部提交会吃掉 4/5。**⇒ 同族只应挑 2–3 条最强的进，其余用非价格分母或无价格模板补位。**

---

## 10. 2026-10-30 晚补：平台闸全表实读 + 四条误判更正

### 10.1 ★ 三腿 `is.checks` 全表（`GET /alphas/{id}` → `is.checks`，零成本实读）

| check | 平台 limit | `rKRkL9QE` | `0mYoANkv` | `kqNRXm5k` |
|---|---|---|---|---|
| LOW_SHARPE | **1.58** | 2.21 ✓ | 1.89 ✓ | 1.70 ✓ |
| LOW_FITNESS | **1.0** | 2.05 ✓ | 1.54 ✓ | 1.33 ✓ |
| LOW_TURNOVER | 0.01 | 0.0833 ✓ | 0.1166 ✓ | 0.0798 ✓ |
| HIGH_TURNOVER | 0.7 | 0.0833 ✓ | 0.1166 ✓ | 0.0798 ✓ |
| CONCENTRATED_WEIGHT | — | ✓ | ✓ | ✓ |
| LOW_SUB_UNIVERSE_SHARPE | **1.05 / 0.90 / 0.81** | 1.77 ✓ | 1.12 ✓ | 1.52 ✓ |
| IS_LADDER_SHARPE | **2.02（三者同一档）** | 2.51 ✓（余量 24%） | 2.08 ✓（余量 3%） | **2.02 ✓（零余量）** |
| CLUSTER_TEST | 1.0 | 2.25 ✓ | 1.42 ✓ | 1.64 ✓ |
| SELF / DATA_DIVERSITY / PROD / POWER_POOL / REGULAR_SUBMISSION | — | PENDING | PENDING | PENDING |

**两条可复用的口径**：
- **`LOW_SUB_UNIVERSE_SHARPE` 的 limit = 0.4743–0.4765 × sharpe**（三腿实测 1.05/2.21=0.4751、
  0.90/1.89=0.4762、0.81/1.70=0.4765；两位小数取整解释了离散）。与已知的 DEU 0.4743 同源。
- **GBR/D1/TOP700 的 `IS_LADDER_SHARPE` limit 恒为 2.02**，不是常见的 1.58/1.75。
  `kqNRXm5k` 的 2.02 是**恰好压线**过的，任何重跑抖动都可能翻。

### 10.2 ★★ 更正一：日志里的 `computed: true` 不是「平台已开始算」

`brain_mixin_spcread._poll_production_correlation._meta()` 里：

```python
'computed': bool(saw_empty) or attempt > 1 or (time.time() - start_time) >= 2.0,
```

⇒ **只要轮询超过 1 次就恒为 True**。此前把 `computed: true` 读成「平台已进入计算」是误判，
它只证明「我们发过请求并收到了空体」。

### 10.3 ★★ 更正二：`Retry-After: 1` 被当成轮询间隔下界 ⇒ 自造饥饿

```python
if 0 < _ra <= 30: platform_retry_after = _ra
...
_wait = min(poll_fast[=10], platform_retry_after[=1.0])   # → 1.0s
```

平台对空体回 `Retry-After: 1`，客户端遂按 **1.0s + ±15% 抖动**去轮询 ⇒ 实测
**240 秒打了 175 次**，两轮共 350+ 次全部空响应。给平台的计算窗口被自己的轮询挤掉了。

**修法**：任何 prod 轮询必须设**硬性 40s 下限**（`logs/_tmp_prod_floor.py`），
`mcp check_correlation` 的 120s 客户端超时也会把服务端计算打断在半路。

### 10.4 ★★ 更正三：`is` 段**没有** `prodCorrelation` 键 —— 零成本旁路不存在

`GET /alphas/{id}` 的 `is` 键集实读（5 条候选一致）：

```
bookSize, checks, drawdown, fitness, investabilityConstrained,
longCount, margin, pnl, returns, riskNeutralized, sharpe,
shortCount, startDate, turnover
```

**没有 `prodCorrelation`、没有任何 `*corr*` 键**。⇒ MCP 里 `use_pre_read=True`
那条「预读平台已算好的 prod 值」的优化，对**未提交的 IS alpha 永远不可能命中**；
它只对已提交（OS）alpha 有效。要拿 prod 只有 `/alphas/{id}/correlations/prod` 一条路。

**同时得到两个附带事实**：
- `is.riskNeutralized` 是**真值不是 null**（此前 REST 直读为 null 的印象来自别的字段）：

| alpha | raw S | **riskNeut S** | riskNeut F | 保留率 | investable S | investable F |
|---|---|---|---|---|---|---|
| `rKRkL9QE` | 2.21 | **1.93** | 1.40 | **87%** | 1.93 | 1.66 |
| `kqNRXm5k` | 1.70 | **1.45** | 0.91 | **85%** | 1.64 | 1.24 |
| `0mYoANkv` | 1.89 | **1.02** | **0.51** | **54%** | 1.48 | 1.06 |

  ⇒ **`0mYoANkv` 是三者中风险因子载荷最重的一条**（风险中性化后 F 只剩 0.51），
  它的 1.89 里有近一半是可被既有风格因子解释的成分。这削弱了它作为「第三条独立腿」的价值，
  **提交优先序应排到第三**。
- `pyramids` 在 REST 原始响应里确为 `null`，塔位必须走 MCP `get_alpha_details` 或 `get_pyramid_alphas`。

### 10.5 ★ 更正四：`max_prod ≥ max_self`（可用的下界推断）

prod 池 = 全平台生产池；self 池 = 我自己已提交的 OS 池。**我的 OS alpha 本身也在生产池里**
⇒ prod 池 ⊇ self 池 ⇒ **`max_prod ≥ max_self`**。

| alpha | self（本地实测） | prod 的下界 |
|---|---|---|
| `rKRkL9QE` | 0.5456 | **≥ 0.55** |
| `0mYoANkv` | 0.5210 | **≥ 0.52** |
| `kqNRXm5k` | 0.4399 | **≥ 0.44** |

⇒ `rKRkL9QE` 离 0.70 红线只剩 **0.15 的余量上限**，撞墙风险是真实的，不能用「基本面因子
应该低相关」的先验替代实测。

**但也要看到另一面**：`PROD_CORRELATION` 是平台在**提交时**才判的 check（现在是 `PENDING`）。
⇒ **提交动作本身就是唯一的 prod 测量，且失败是非破坏性的**（平台拒绝提交，alpha 保持
未提交状态，不会消耗塔位与配额）。所以「等 prod 再决定」与「提交即测」的代价差，
只是**成功则不可逆**这一条。

### 10.6 `decay` 是分族参数，不是全局参数

同一 reversal 表达式（`reverse(rank(ts_quantile(ts_av_diff(divide(cap, fnd6_cptnewq_ceqq), 252), 84, driver=gaussian)))`）：

| decay | S | F | 2Y | failed_ra |
|---|---|---|---|---|
| 10 | 1.56 | 1.31 | 1.55 | 2（LOW_SHARPE + IS_LADDER_SHARPE）|
| **6** | **1.59** | **1.35** | **1.89** | **0** |

**reversal 族用 decay 6，flow 族用 decay 10**。对换手 ~10% 的 reversal 腿，decay 6 让 2Y 涨 0.34、
ladder 闸自动消失。这不是「调参找过拟合」，是换手与半衰期的匹配问题：
reversal 信号的半衰期更短，decay 10 会把有效信息平滑掉。

### 10.7 P/B 比 P/A 强，但两个权益口径是同一颗

| 分母字段 | S | 说明 |
|---|---|---|
| `fnd6_cptnewq_ceqq`（普通股权益，cov 0.5458） | **1.56**（decay 10） | 最佳 |
| `fnd6_ewq_teqq`（总权益，cov 0.71） | 1.67（decay 6） | 可用，但与上面相关 **0.9584** |
| `fnd6_cptnewq_atq`（总资产） | 1.44 | 弱 8% |

⇒ **P/B 优于 P/A 约 8%**，但两个权益字段**只应取一条**（换字段在这个族里等于没换）。

### 10.8 干净安慰剂：纯资产增长（无任何价格成分）判死

`LLMekGMn` = `reverse(rank(ts_quantile(divide(ts_av_diff(fnd6_cptnewq_atq, 252), fnd6_cptnewq_atq), 84, driver=gaussian)))`
—— 用 `divide(Δ资产, 资产)` 做成**无量纲**的纯会计增长率，完全不碰价格：

**S −0.12 / F −0.02 / 2Y −0.62 / failed_ra 4**（LOW_SHARPE、LOW_FITNESS、
LOW_SUB_UNIVERSE_SHARPE、LOW_2Y_SHARPE 全挂，CLUSTER_TEST warning −0.53）

而**同一个 `fnd6_cptnewq_atq` 一旦进入价格分母就做到 1.44–1.59** ⇒ 与 §9.1b 互相印证：
**引擎是 `Δ(1/价格)`，基本面分子只提供横截面权重。**

**附带**：纯基本面 alpha 只登记 **`fundamental` 单塔**（`effective = 1`，`pyramid_short = "fundamental"`），
**不占 trio × 非 trio 的 ≤5 配额** —— 但信号本身无效，这条路走不通。

