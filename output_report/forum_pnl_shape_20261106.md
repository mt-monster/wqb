# 论坛检索：「改变 PnL 形状 / 降 Prod Correlation」方法盘点

- 检索日期：2026-11-06
- 触发问题：`qMLOooX1`（KOR/TOP600/R&M，双腿 `ts_av_diff` × `multiply`，6 ops）第三批 `group_cartesian_product` 复合轴全部无效，外层四条 pnl 逐位相同 —— 论坛里有什么方法能真正改变 pnl？
- 模式：只读 explore（未发帖、未回测、未提交）
- 读取：7 次搜索 + 12 篇正文/评论区深读；所有标题、票数、评论均取自论坛 MCP 返回，未作外推补写

---

## 一、论坛的第一判据：PC 认的是 PnL 曲线形状，不是信号内容

| 帖 | 主张 |
|---|---|
| `36680834830743`《降低Alpha的Prod Correlation：实用技巧与案例分享》评论区 ZZ47696 | 「PROD_CORR 比的是两条 PnL 曲线的**形状**相似度，不是信号内容相似度」；`rank`/`quantile`/`signed_power`/换分组都是**保序变换**，不改变每天多空的相对排序 ⇒ PnL 曲线形状几乎不变 |
| `39118594803095`《关于降Prod Correlation的实践（一）》评论区 ZZ47696（v35 6 探针） | 同 kernel 的 `quantile(gaussian/uniform)`、`signed_power(0.5)`、`normalize`、`quantile(cauchy)×2` 全部实测：PC 死钉 **0.699~0.709**，无一条结构逃生。结论「真杠杆只剩两条：**换数据集 / 换 kernel**（改变 pnl 形状本身）」 |
| `43451338187287`《控制 prod correlation：先问改动改变的是持仓构成，还是只改了权重》(22 票) | 「平滑、非线性变换、换中性化方式本质都是**改了权重但不改持仓子集**，对 PC 压制效果基本可忽略」 |
| `43806236797463`《相关性超标时该换的是信号族，不是参数》(21 票) 评论区 SD17531 | 有效性排序：**换数据集字段 > 换处理维度 > 换区域 > 换参数**；越往后越只改权重不改构成 |

**与我们 30 条实测的吻合度**：极高。删一腿 / `multiply→add` / `ts_av_diff→ts_rank` 确实改变了 pnl，但 prod 从 0.6941 跳到 0.7170–0.8147 ⇒ **「改变 pnl」≠「降 prod」，必须改对形状**。

## 二、为什么我们的复合轴四条外层全是 no-op（机制解释）

`43667882062871`《双重中性化 vs. group_cartesian_product》(14 票) 明确指出 gcp 的价值在 **`industry × country` 这类正交维度**，并点名适用场景是 **ASI / EUR / GLB 等多国家区域**。

对照我们第三批用的四种组合：

| 组合 | 在 KOR 的实际含义 | 外层结果 |
|---|---|---|
| `gcp(sector,industry)` | sector 与 industry 是**嵌套层级**，笛卡尔积 ≡ 较细的 `industry` | 与基线外层 `industry` 同分组 ⇒ 逐位相同 |
| `gcp(market,sector)` / `gcp(sector,market)` | KOR 单一国家区域，market/country 近乎常数组 ⇒ ≡ `sector` | 同上（被平台 R&M 中性化吸收） |
| `gcp(market,industry)` | ≡ `industry` | 同上 |

`36680834830743` 评论区另有一条直接对应：「若平台中性化已设 SUBINDUSTRY，表达式里再套 `group_neutralize(x, subindustry/industry/...)` 是**恒等变换**，指标逐位相同；要『内细外粗』才有效」。

⇒ **根因：我们选的两轴全在同一条嵌套链上，笛卡尔积退化成其中较细的一个，没有产生新分组轴。** 不是 gcp 算子没用，是轴选错了。`34452515590039`《降低 ProdCorrelation 的常用方法》第 4 条也只说「若用了 gcp，尝试不同的**分组类别**（exchange / country / market / industry / subindustry）」，同样强调换类别而非换组合顺序。

## 三、论坛给出的方法清单（按「是否改持仓构成」分档）

### A 档：改持仓子集 —— 论坛公认真正有效

1. **稀疏字段门控**（`43451338187287` 首推）：
   `trade_when(greater(rank(ts_backfill(SPARSE_FLAG,130)),0.5), MAIN_SIGNAL, nan)`
   要点：稀疏腿**只做条件、绝不做乘法腿**；作用是把主信号限制在信息优势期内，直接换掉持仓子集。
2. **定义域产生 NaN 的非线性**：`39118594803095` 楼主用 `arc_sin`（定义域 [-1,1]，越界变 NaN）改变 long/short count，评论区 AM12075 点破机理「**使 pnl 曲线形状得到较大改变**」；ZZ47696 补充「arc_sin 能降 PC 是因为它作用在原始 alpha 值上、实质改了信号内容；保序形变平替走不通」。同帖评论区 JC31003 报 `group_zscore(densify(market))` 在 EUR/news18 上 PC 0.97→0.36、self 0.97→0.30、S 2.32→2.45（**单例，未实证**）。
3. **非嵌套的复合轴**：`43667882062871` 的 country×industry；`39210414994967` 类介绍帖与 `34116476806679` 里 EUR 用 `gcp(country,market)`；`37473718017175`(ASI) 用 `gcp(country, densify(bucket(rank(cap))))`。⇒ **必须有一轴是 cap/volume/exchange/风险桶这类非嵌套维度**。

### B 档：改信号的时间指纹（中等强度，有正反案例）

4. **缩短 temporal 窗口**：`41939553020567`《改 ts_min_diff 窗口》(23 票) 实测 126→63，S 2.12→2.16、PC 降到 0.7 以下；评论区解释为「压缩信号记忆长度，偏离已有集群的持仓周期」。该帖还说明**先试缩窗口而不是先换中性化**。
5. **指数加权平滑替代等权**：`41105473931927`《KOR exp-MA 平滑降 Prod Correlation》报 KOR/TOP1200 上 `ts_decay_exp_window` 使 PC 0.78→0.52、Fitness 仅微降；`41939553020567` 评论区 LY43440 独立附议。
6. **换读数结构（L1）**：`42659822656663`《mm 结构把 corr 从 0.86 压到 0.67》(30 票) —— `ts_max_diff(ts_backfill(X,22),W) - ts_av_diff(ts_backfill(X,22),W)` 换掉「计数类」读数，TO 0.162→0.036、PC 0.856→0.666，作者结论「降 corr 优先换**字段构造/读数据的方式**，而不是堆外层平滑」。
7. **中性化与 universe 作为组合旋钮**：`37009797997207`(IND, 17 票) 称 RAM / FAST / SLOW 大幅降 PC；`42659822656663` 报只有 CROWDING 能同时保住 CLUSTER 与区域 Sharpe；`34452515590039` 第 3 条「尝试不同的中和设置」。

### C 档：论坛内部就被证伪 —— 不要再烧额度

- **保序形变**：`quantile(driver=gaussian/uniform/cauchy)`、`signed_power(x,0.5)`、`normalize(useStd)`、单纯换 group 维度 ⇒ PC 只在 0.66–0.71 窄带抖 ±0.04（`36680834830743`、`39118594803095` 评论区）。
- **线性加权 / 调权重 t**：`39118594803095` 评论区 TL89486 单变量实测 t=1.0→2.0，PC 0.7596→0.7880（**微涨**），Self Corr 却掉 0.147 ⇒ 「t 是 self-corr 旋钮，不是 PC 旋钮」。
- **掺一条中等 PC 的腿稀释**：同帖 ZZ47696 闭式判据 `PC_c=(a+w·b)/sqrt(1+w²+2wρ)`，w*=b/a 处取**极大** sqrt(a²+b²)；要 PC 下降需 `w>2ab/(a²−b²)`，且掺腿必须 `PC≤0.3` 且 margin 不低于主腿一半，否则「PC 闸过了、Fitness 闸关上」。
- **换中性化 ≠ 一定降 PC**：`41939553020567` 实测 STATISTICAL→INDUSTRY/SUBINDUSTRY 反而更拥挤。
- **过度优化警告**：`19524526933655` 唯一评论「当您优化的目的仅仅是降低 corr，就可能过拟合了」。

### D 档：判定「pnl 到底变没变」的本地方法

`43300341649687`《用本地 PnL 自相关聚类…》(51 票)：拉各 alpha 的 pnl → 转成日收益 → 本地算相关矩阵 → union-find 按 **0.9** 聚类，同簇只查一个 PC。文中原话「同一个模板换个 group 字段、换个时间窗口、换个中性化，日收益率相关性可能高到 0.95 以上，本质是同一个信号的不同包装」。我们已有 `compute_mutual_correlation`，正好是这套判据的本地实现，且零 prod 额度。

---

## 四、与本地实证冲突的地方（禁止跨族外推）

| 论坛说法 | 我们 `qMLOooX1` 的实测 | 处理 |
|---|---|---|
| `ts_rank` 能降 PC（`41105473931927` 评论） | 双腿 `ts_av_diff→ts_rank` S 升到 1.99，prod **0.6941→0.7170 反升** | 以本地为准 |
| `signed_power(x,0.5)` 五项全改善、PC −0.034（`39118594803095` 评论） | 本族 `signed_power(BASE,0.5)` S1.86/F1.54，prod 未取 | 待 prod 恢复再判 |
| 换 group 维度能降 PC（`34452515590039`） | 外层 gcp 恒等、内层损 2Y | 论坛自己也说只在 ±0.04 抖 |
| 缩窗口能降 PC（`41939553020567`） | 窗口 126 指标全面更优（`O0ARePNY`），**prod 未取** | 这是最值得补测的一条 |

论坛帖子按 skill 纪律**默认未实证**，只作方向候选，不得当作 win 回写。

---

## 五、对本条 alpha 的可执行清单（待验证，本轮未派发）

按「改持仓构成优先」排序，均需先过 ④b 全量算子过审 + 本地 op_arity 校验：

1. **非嵌套复合轴**：内层改 `gcp(bucket(rank(cap), range="0,1,0.2"), sector)` / `gcp(exchange, sector)` / `gcp(sector, bucket(rank(adv20)))`，外层保持 `industry` 不动 —— 这是补上第三批选错的那一轴。
2. **稀疏门控**：找 anl10 / KOR 里的稀疏事件字段做 `trade_when(..., MAIN, nan)`，只作条件腿；按 §0 组合形态铁律属于 `trade_when` 允许形态。
3. **mm 读数替换**：`ts_av_diff(X,126) → ts_max_diff(X,126) - ts_av_diff(X,126)`，双腿同换或只换一腿做单变量对照；直接命中 `42659822656663` 的 0.19 降幅案例。
4. **指数平滑**：`ts_av_diff(ts_decay_exp_window(X,126,factor=0.3), 126)` 一类，测时间指纹改变。
5. **平台设置层**：`REVERSION_AND_MOMENTUM` → `CROWDING` / `STATISTICAL` / `FAST`（`37009797997207`、`42659822656663`），注意这属于换设置，须单独一批、不可与表达式改动混在同一批归因。
6. **先补数据**：prod 端点恢复后优先取 `O0ARePNY`(窗口126) 与 `mLodAxwE`(内层gcp) 的 prod，再决定值不值得开第四批。

**前置纪律**：批候选花 prod 槽前必先 `compute_mutual_correlation` 与基线做日收益互测；若 ≥0.9 直接判为同一 pnl，不必查 prod（`43300341649687` 的 0.9 阈值）。

---

# 附录：六方向实测（2026-11-06 16:2x–16:4x，8 批 52 条）

> 用户指令「所有方向持续推进」。基线 `qMLOooX1`：KOR/TOP600/D1/R&M/decay4/trunc0.08，S 1.94 / F 1.74 / 2Y 1.76 / sub 1.71 / TO 0.0972 / pnl 10,400,371 / 6 ops / ATOM / prod 0.6941。
> 批次：`2UdFHoauQ5jsbwPepTInrFp`、`3zTFgb3B59z8XpLtRcyFOO`、`mfYnf2aS5e09gb1dAZ8nSSB`、`140EMv6Zh4Eea1718X6OM87x`、`4qlojb3955cBa3eUfqJaPjM`、`4ltOQ31Za595b1KsRZbFblI`、`2nrES3ejm4KD9Q514k0T6wvo`、`2xF46S3v24lx9dfYYkMm894`。全部 0 error。

## 结果总表

| 方向 | 结论 | 最佳点 |
|---|---|---|
| **① 非嵌套复合轴** | **有效，修正第三批结论** | `9qx8Ang9` gcp(exchange,sector)：S1.93/F1.72/**2Y1.91**/sub1.69/pnl 10,289,422 / `failed_ra=0` / **ATOM 保持** / 8 ops（平台 `operatorCount`，2026-11-06 复核；早期记为 7 系笔误）|
| **② L1 读数（mm / 缩窗 / 平滑）** | **mm 毁灭，但窗口曲线补出峰** | `58ErqdXJ` W189：S1.94/F1.73/**2Y1.87**/sub1.73 / `failed_ra=0` / 6 ops |
| **③ 稀疏门控** | **10/10 全灭** | 最好 S1.20，最差 −0.06 |
| **④ 换中性化（4 档）** | **全部劣于 R&M** | FAST 1.73｜CROWDING 1.71｜STATISTICAL 1.50｜SLOW_AND_FAST 1.40 |
| **⑤ 外层截面形变** | **★ 本轮最大赢家** | `1YNOoA9z` `tail(BASE,-0.1,0.1,0)`：S1.94/**F1.78**/**2Y1.93**/sub1.70/TO0.1069/**pnl 10,911,369** / `failed_ra=0` / **ATOM** / 7 ops |
| **⑥ prod 终验** | **平台停摆，未取到** | 见下 |

## 关键机制

1. **嵌套 vs 非嵌套轴**：`0mYxKJQk` gcp(currency,sector) 的 pnl 与基线**逐位相同**（KOR 单国 currency 常数）；换 exchange / cap 桶 / 冷门 PCA cluster 后 pnl 落在 10,181,825–10,429,524。⇒ 论坛 `43667882062871` 的「正交维度」判据成立，第三批「复合轴无用」应改写为「**嵌套轴无用**」。
2. **ATOM 分水岭**：`exchange` 属豁免分组字段 ⇒ `effective=1` 保 ATOM；`cap` / PCA 轴引入 PV ⇒ `effective=2` 丢 ATOM（尽管 `WjO3W5nZ` 2Y 高达 2.43）。细桶 ×sector 两档掉 `IS_LADDER`。
3. **恒等算子实锤**：`normalize(BASE,useStd=true)` 与 `group_zscore(BASE,market)` 与基线日收益相关 **1.0000**，`group_zscore(x,market) ≡ zscore(x)` 再验证；`quantile(cauchy)` 把 S 砸到 1.27（与论坛 ZZ47696 一致）。
4. **论坛案例不可跨族外推**：mm 结构（论坛 PC 0.856→0.666）在本族 S 0.63–0.67；稀疏门控（论坛首推）在本族全灭；换中性化（论坛 IND/GLB 有效）在本族全劣。本族 **R&M + `ts_av_diff` + `multiply` 双腿**是甜点区。
5. **arc_sin/arc_tan/tanh/sigmoid 本账号无权限** ⇒ 论坛唯一实证「改持仓子集且降 PC」的非线性路径不可用；本轮用 `tail` 达到了同类效果（中段压 0 ⇒ 换掉持仓子集，pnl +4.9%）。

## 决定性限制：仍是同一席位

`compute_mutual_correlation`（4 年日收益）：

- 第一批 10 颗（含基线 / 126 / 189 / 各轴变体）两两 **0.8702–0.9958**，与基线 0.8807–0.9954。
- 形变批 9 颗与基线：`1YNOoA9z` **0.9857**、`GrWXn5AP` 0.9991、`qMLOnJoA` 0.9745、`ZYQgjv31` 0.9292、`WjO3N26j` 0.9116、`E56NqPWr` 0.9020；最低的一对是 `E56NqPWr`×`WjO3N26j` 0.8404。
- 两次 `max_mutually_below_subset`（阈值 0.7）**都只剩 1 颗**。

⇒ 按 §1「换窗口/分组/中性化/幂次=同席」，**52 条实验没有产出新席位，全部是同一席位的更优参数点**。任何提交清单里这些候选只能选一颗。

## 交付候选（按当前证据排序，均未提交）

| alpha | 表达式要点 | ops | S/F/2Y/sub | TO | self | prod |
|---|---|---|---|---|---|---|
| **`1YNOoA9z`** | `tail(BASE,-0.1,0.1,0)` | 7 | **1.94/1.78/1.93/1.70** | 0.1069 | **0.3767 PASS** | **待补** |
| `58ErqdXJ` | 双腿窗口 189 | 6 | 1.94/1.73/1.87/1.73 | 0.0990 | 未测 | 待补 |
| `9qx8Ang9` | gcp(exchange,sector) | 8 | 1.93/1.72/1.91/1.69 | 0.0988 | 0.3891 PASS | **0.6832 PASS** |
| `qMLOooX1`（基线） | W250 | 6 | 1.94/1.74/1.76/1.71 | 0.0972 | 0.3939 | 0.6941 |

`1YNOoA9z` 是本轮唯一「S 持平、F/2Y 双升、零 RA 失败、ATOM 保住、self 通过」的点，代价仅 +1 op 与 TO +0.0097。

## 18:25 prod 复测（端点已恢复，非全账号停摆）

- **端点状态**：`alpha_corr_cache` 17:00–17:53 陆续有 6 颗成功写回（`E56Nk0wL` 0.7002 / `omERn83n` 0.6898 / `JjeoLpGA` 0.8688 / `YP18Gpel` 0.8083 / `xArVj27g` 0.9532），⇒ 16:08–17:00 的停摆已结束，剩余问题是**本簇候选的平台侧计算排队**。锁 holder 依次为 `bl6J5Lwm`（并行会话）。
- **★ `9qx8Ang9` prod = 0.6832 PASS**（`prod_wait --peek`，18:12，结果文件 `results/prod_peek_9qx8Ang9.json`）。相对基线 `qMLOooX1` 0.6941 **降低 0.0109** ⇒ **非嵌套复合轴 `gcp(exchange,sector)` 是本轮唯一实测能降 prod 且全闸不劣的杠杆**（7 ops、ATOM 保持、2Y 1.91、零 RA 失败）。这修正了第三批「gcp 对降 prod 无效」的结论：无效的是**嵌套轴**（sector×industry / market×sector），非嵌套轴有效。
- **仍排队**：`1YNOoA9z`、`58ErqdXJ`、`O0ARePNY`、`mLodAxwE`。三次 `check_correlation(refresh=False)` 各 240s 全返 `pending / inflight=true`（attempts 184–187），`prod_wait --peek` 多轮全空体。按纪律**未重派、未判死**。
- **按论坛 `43300341649687` 的 0.9 判据，本簇只需 1 个 PC**：5 颗两两互测 0.87–0.996 与基线同席位，已取到代表值 0.6832 与基线 0.6941 ⇒ 整簇 prod 量级已定性在 0.68–0.70，**继续消耗 prod 槽不改变「同席位只能选一颗」的结论**。仅在用户点名某颗准备提交时，才对那颗 `refresh=True` 终验（prod 缓存 48h 作废）。

**未提交任何 alpha**；提交权归用户且须点名。

---

## 19:5x 追补：`9qx8Ang9` 算子压缩（skill `wq-alpha-gate-push-op-min`）

**基线**：`9qx8Ang9`，8 调用点 / 平台 `operatorCount=8`，全闸 PASS（`failed_ra=0`）、ATOM effective=1、self 0.3891、prod 0.6832（余量 0.0168，**最紧的闸**）。

### 压缩结果（11 条实验：10 条 multisim + 1 条单条变量版）

| 候选 | 改写 | ops | S/F/2Y/sub | 全闸 | prod |
|---|---|---|---|---|---|
| **`leAEYLM8`** ★ | `gcp(exchange,sector)`→`exchange` + 窗口 250→**189** | **6** | 1.93/1.72/1.81/**1.75** | 0 fail | **0.6856 PASS** |
| `1YNOR6rW` | `a = gcp(exchange,sector);` 变量合并重复子式 | 7 | 1.93/1.72/1.91/1.69（**逐位相同**） | 0 fail | 0.6832（互测 1.0000 推出） |
| `78L3KpQx` | 纯 `exchange` 轴、W250 | 6 | 1.94/1.74/1.78/1.75 | 0 fail | 0.6953 |
| `leAEYLK8` | 删外层 `group_neutralize` | 7 | 1.74/1.53/1.64/1.54 | 0 fail | 未取 |
| `9qx8AnKe` | 一腿 gcp、一腿 sector | 7 | 1.92/1.71/1.84/1.69 | 0 fail | ≈0.6832（互测 0.9958） |
| `gJeX5YWK` | 纯 exchange + 删外层 gn | 5 | 1.71/1.50/1.48/1.56 | **1 fail** | — |
| `78L3rk62` / `P0oxbJMw` / `2rA9x1j6` | **两腿 `group_rank` 合并成单次** | 6 | S **1.23–1.28** | **3 fail** | — |
| `rKR9w1dm` | `group_rank`→`rank` + 外层 gcp | 7 | 1.38/0.99/0.76 | **3 fail** | — |

### 三条硬判据

1. **重复子式变量合并是零损失压缩**：`group_cartesian_product(exchange,sector)` 在原式中出现 2 次，`a = ...;` 后平台 `operatorCount` **8→7**，S/F/2Y/sub/TO/pnl **逐位相同**，本地日收益互测 **1.0000** ⇒ prod 必然仍是 0.6832，无需花 prod 槽。⚠ 变量表达式**不能进 multisim**（会卡死），必须单条 `create_simulation`。
2. **两次 `group_rank` 相乘承重，不可合并为单次**：3 条「先 `multiply` 后 `group_rank`」全部崩到 S 1.23–1.28 / 3 fail；`group_rank→rank` 同样 3 fail ⇒ 两腿各自组内归一后再相乘是这一席位的骨架。
3. **`gcp` 的 sector 维是可删的，代价由窗口补偿**：`gcp(exchange,sector)`→`exchange` 省 2 ops，但 W250 版 prod 0.6832→0.6953（+0.0121，余量只剩 0.0047）；把窗口调到 **189** 后 prod 回到 **0.6856**（仅 +0.0024），且 sub 1.69→1.75、TO 0.0988→0.0970 双改善，唯一代价 2Y 1.91→1.81（仍高于 limit 1.58 有 0.23 余量）。

### 定案

**推荐 `leAEYLM8`（6 ops）取代 `9qx8Ang9`**：
```
group_neutralize(multiply(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,189),exchange),
                          group_rank(ts_av_diff(anl10_smartest_net_fy1_pred_surps_v1,189),exchange)),industry)
```
全闸 PASS / self **0.3899** / prod **0.6856** / ATOM effective=1 / KOR/TOP600/D1/R&M/decay4/trunc0.08。省 **2 ops** 换 prod +0.0024，按「余量换算子数」采纳。

若坚持 prod 绝对最低，则选 `1YNOR6rW`（7 ops、prod 0.6832、指标逐位等同基线）。**两者同席位（互测 0.9546），只能交付一颗**；`9qx8Ang9` / `1YNOR6rW` / `78L3KpQx` 在本轮标 `SUPERSEDED`。

⑤ 设置收敛未跑：decay/trunc 会改 pnl ⇒ 贴线 prod 会漂移，而收益集中在已充裕的 F(1.72)/2Y(1.81)，风险收益比不划算。若要点名提交，须对所选那颗 `check_correlation(refresh=True)` 终验（prod 缓存 48h 作废）。

批次 `results/batch_9qx8ang9_opmin.txt`（10 条，multisim `2hWH7371s5j6a6WpRq7vXZm`，0 error）；签核 `results/op_coverage_signoff.jsonl` session `9qx8ang9-opmin`（④b checklist 全量过审，覆盖率 7.1% ⇒ 仅「已用算子集合内穷尽」）。

**20:24 更新：用户点名「免查prod提交」，`leAEYLM8` 已提交并 ACTIVE**（ET 07:23:59，stage=OS）。免查实现 = 把 `prod_wait --peek` 读到的平台实测 0.6856 写入 48h 权威缓存后 `check_correlation(refresh=False)` 命中，零算力重算。稳健性判 **CONDITIONAL**（2023 年 S 0.64 末段衰减，CV 0.640 / max-min 5.42 按用户明确指令放宽，见 `reports/robustness_20261106.md`）。遗留风险：prod 余量 0.0144 薄过，须用 OS 表现复核。


---

## 2026-11-07 `omERn83n` op-min 战役（KOR / rsk70 分析师情绪 ⊥ 动量）

**基线（9 ops，prod 0.6898，余量 0.0102）**：
```
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(
  rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn,40)),
  rank(ts_backfill(rsk70_mfm2_asetrd_momentum,22))),std=0.38),sector),2.5),target_tvr=0.22)
```
设置 KOR/TOP600/D1/decay1/R&M/trunc0.04/nanON。

### 三批 30 条 + 一批 8 条（ERROR 重派 6 条）实测

| 结论 | 证据 |
|---|---|
| **① `ts_target_tvr_decay(·,0.22)` 是 no-op** | `N1NJJ5vL`（带）与 `bl6rrW5m`（删）S/F/2Y/sub/TO **逐位相同 1.62/1.23/2.27/1.31/0.1319**。根因：TO 0.1231 < target 0.22，未触发。⇒ 删 −1 算子零损失 |
| **② `ts_backfill` 是 dead-weight** | 窗口 21/63/126/252 **全部逐位相同**（`xAr22GOq`/`P0oYYzK`…/`2rAXX686`）⇒ 字段无长缺口；再删两处：5-op `78LvMKAO` ≡ 7-op `N1NJ350E`（1.60/1.29/2.01/1.33/0.1231 逐位同），5-op `xAr2Wm6n` ≡ 7-op `j2YPxdEE`（1.65/1.31/2.28/1.32/0.1313 逐位同）⇒ **删 −2 算子零损失** |
| **③ `winsorize` 承重不可删** | 删后 `mLo00x9p` S 1.34 / F 0.94（2 fail）。std 甜点 **0.38**：0.30→1.49、0.25→1.46、0.50→1.51、1.0→1.34 |
| **④ 内层两个 `rank` 不可删** | 删双 rank（`mLo01xR5`）S **0.65** / 5 fail ⇒ `vector_neut` 要求两腿先归一 |
| **⑤ `vector_neut` 承重不可删** | 删后 `VkxmmYJ8` S 1.19 / 2 fail |
| **⑥ `signed_power` 与分组轴强交互** | sector 轴：删 → 1.62→**1.65**（增益）；exchange 轴：删 → 1.68→**1.60**（减益）。⇒ 轴与幂次必须联合定 |
| **⑦ 轴排序：exchange > sector** | 8-op `zq322JzK`（exchange）S **1.68** / F 1.33 / sub **1.38** / TO 0.1206，优于 sector 同构 1.65。`group_zscore` 1.49、`gcp(exchange,sector)` 1.54 均劣 |
| **⑧ 换第二腿（正交轴）全崩** | newssent 1.27｜indmom 0.47｜strevrsl 0.40｜shortint 0.58｜earnqlty 0.25｜ltrevrsl 0.13｜dsrt 1.36 ⇒ momentum 是唯一可用第二腿 |
| **⑨ `tail` 无增益** | `npveQORz`（tail,-0.1,0.1,0）≡ E1 逐位同 1.60；`d5W33lwx` 1.61 |

### 达标候选（全部 fail=[] / ATOM `KOR/D1/RISK` effective=1 / 2Y 走 `LOW_2Y_SHARPE`）

| alpha | 算子 | 轴 | S | F | 2Y | sub | TO | prod | self |
|---|---|---|---|---|---|---|---|---|---|
| `zq322JzK` | 8 | exchange | **1.68** | 1.33 | 2.22 | **1.38** | 0.1206 | **0.688** | 0.379 |
| `9qxddA0K` | 8 | sector | 1.65 | 1.31 | **2.28** | 1.33 | 0.1312 | 待测 | — |
| `xAr2Wm6n` | **5** | sector | 1.65 | 1.31 | **2.28** | 1.32 | 0.1313 | 待测 | — |
| `78LvMKAO` | **5** | exchange | 1.60 | 1.29 | 2.01 | 1.33 | 0.1231 | ≡E1 | — |

**prod 墙诊断**：`zq322JzK` prod 0.688，直方图 `0.6–0.7` 仅 **4 颗**、`0.5–0.6` 71 颗 ⇒ 墙由极少数第三方生产 alpha 顶住；self 最高仅 0.3785（`npPVP253`）⇒ **不是自己池，换结构收益有限，本质需换信息源**（与 §11 判据一致）。

### ★★ 反直觉发现：`signed_power` 指数是 prod 的单调降压旋钮（exchange 分组下）

| `signed_power` 指数 | alpha | S | F | 2Y | sub | TO | **prod** | 余量 |
|---|---|---|---|---|---|---|---|---|
| 2.5（8-op 有 backfill） | `zq322JzK` | 1.68 | 1.33 | 2.22 | 1.38 | 0.1206 | 0.688 | 0.012 |
| 2.5（6-op） | `WjOo0v7j` | 1.67 | 1.32 | 2.22 | 1.38 | 0.1206 | — | — |
| 2.0 | `E568L9lR` | 1.66 | 1.32 | 2.17 | 1.37 | 0.1213 | — | — |
| **3.0** | `QPvNgw7g` | **1.68** | **1.32** | 2.25 | **1.38** | 0.1202 | **0.6723** | 0.028 |
| **4.0** | `6Xdo27P5` | **1.68** | 1.30 | 2.28 | 1.37 | 0.1201 | **0.6393** | 0.061 |
| **5.0** | `0mYNaq9q` | 1.67 | 1.28 | 2.27 | 1.35 | 0.1210 | **0.6047** | **0.095** |
| 3.0 + std0.42 | `YP1E96nq` | 1.67 | 1.31 | **2.40** | 1.35 | 0.1205 | — | — |
| 3.0 + std0.34 | `kqNWYdbk` | 1.62 | 1.25 | 2.14 | 1.33 | 0.1200 | — | — |

**结论**：指数 2.5→5.0，**prod 0.688→0.6047（−0.083）**，而 S 几乎不动（1.68→1.67）、F 1.33→1.28、sub 1.38→1.35。
⇒ **「prod 随极值集中度单调上升」的旧判据在 exchange 分组下失效**：此处幂次放大的是**组内（2 个交易所内）**权重分布，而非跨组集中度，因此集中度指标不升反降；被顶住的那颗第三方 alpha 与「温和权重」版本更像。
⚠ 待第二例验证才能升为通则。指数 4.0 是当前**性价比最优点**（S 不变、余量 6×）；5.0 余量更大（0.095）但 F/sub 已开始掉。

### 指数曲线探底（sp 6/8 + std0.42×sp4）

| 指数 | alpha | S | F | 2Y | sub | 备注 |
|---|---|---|---|---|---|---|
| 6.0 | `P0oYbNKw` | 1.64 | 1.24 | 2.23 | 1.32 | S 开始掉 |
| 8.0 | `pwdMkm3v` | **1.58** | 1.18 | 2.12 | 1.26 | **触 LOW_SHARPE 闸**（<1.585）|
| std0.42 × sp4 | `A1Vr59EX` | 1.66 | 1.28 | **2.42** | 1.33 | 2Y 最高但 S/F/sub 均降 |

⇒ **S 曲线在 3.0–4.0 见顶（1.68），4.0 之后单调下滑，8.0 掉闸**。prod 则全程单调下行（0.688→0.6047）。
⇒ 可取区间 = 指数 **4.0**（S 峰值 + prod 0.6393）或 5.0（prod 0.6047，S −0.01）。

### ★ 定案：`6Xdo27P5`（6 ops，取代 9 ops 的 `omERn83n`）

```
signed_power(group_rank(winsorize(vector_neut(rank(rsk70_mfm2_asetrd_anlystsn),
  rank(rsk70_mfm2_asetrd_momentum)), std=0.38), exchange), 4)
```

| 指标 | `omERn83n`（9 ops） | **`6Xdo27P5`（6 ops）** | Δ |
|---|---|---|---|
| Sharpe | 1.62 | **1.68** | +0.06 |
| Fitness | 1.23 | **1.30** | +0.07 |
| 2Y | 2.27 | **2.28** | +0.01 |
| sub_universe | 1.31 | **1.37** | +0.06 |
| Turnover | 0.1319 | **0.1201** | −0.012 |
| Drawdown | — | 0.0379 | — |
| **prod** | 0.6898 | **0.6393** | **−0.0505（余量 0.0102→0.0607，6 倍）** |
| self | — | **0.3339** | 最高对手 npPVP253 |
| 闸门 | fail=[] | **fail=[]** | 全过 |
| ATOM | effective=1 | **effective=1** | KOR/D1/RISK ×1.3 |

设置：KOR/TOP600/D1/decay1/REVERSION_AND_MOMENTUM/trunc0.04/nanON。

**撤销清单（同席位，均标 SUPERSEDED）**：`zq322JzK`(8op 0.688)｜`QPvNgw7g`(6op sp3.0 0.6723)｜`0mYNaq9q`(6op sp5.0 0.6047)｜`9qxddA0K`/`xAr2Wm6n`(sector 1.65)｜`78LvMKAO`(5op 1.60)｜`WjOo0v7j`/`E568L9lR`/`YP1E96nq`/`kqNWYdbk`/`A1Vr59EX`/`P0oYbNKw`/`pwdMkm3v`。
**未提交**（遵 `ALLOW_ALPHA_SUBMIT=False`，提交权归用户；prod 0.6393 有效 48h，终验须 `refresh=True`）。

### 提交结果（2026-11-07 02:59 ET 2026-11-06）

**`6Xdo27P5` 已提交成功**：`status=ACTIVE`、`stage=OS`、`dateSubmitted=2026-11-06T13:59:38-05:00`。
属性：`KOR_R_rsk70anmom_01`｜`BLUE`｜tags `CH_REG` / `SRC_risk70` / `CORR_060`（平台自动追加的 `PowerPoolSelected` 已清除）。

提交链各步：
| 步 | 结果 |
|---|---|
| submit_gate | passed；failed_ra=0 / failed_ppa=0；robustness 台账 `CONDITIONAL`（已录） |
| quota_gate | ET 2026-11-06 REGULAR 2/4 → 剩余 2（提交后 3/4） |
| prod_gate | **0.6393 < 0.7 过闸**（缓存 @2026-11-07T02:44:32，按用户指令免复查） |
| marginal | 分区 `EQUITY:KOR:1:POWER_POOL` ΔSharpe **+0.15** / ΔFitness +0.13 ⇒ 正向分散（信息项） |
| submit | HTTP **201** async accepted → verify **ACTIVE** |

**稳健性**：10 个 IS 年全正（最小 0.61），近 3 年 1.66 / 3.86 / 0.85 均值 2.123；CV 0.734 与 max/min 4.54 由 2022 年 3.86 高离群驱动，记为 soft_flags，判 CONDITIONAL（详见 `reports/robustness_20261106.md`）。
