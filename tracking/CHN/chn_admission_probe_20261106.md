# CHN 准入探针战役记录（2026-11-06）

> 为什么开：GBR 未点亮塔空间见底（16 数据集全部画像+探针），四塔 48 臂只出 1 颗 prod 判死的 `leAgVON2`。
> CHN 是唯一「D1 全塔 0（12 category 全未点亮）+ universe 有效」的空白区。唯一合法 universe = `TOP2000U`（JPN/TOP1600、TWN/TOP500、AMR/TOP500、MEA/TOP500 全部返回 0 数据集）。

## §1 ★★★★★ 头号发现：CHN 的严闸是 2.07，不是 1.58

chn1 八臂实测 `checks.fail[].limit` 一律为：

| 检查 | CHN limit | GBR limit |
|---|---:|---:|
| LOW_SHARPE | **2.07** | 1.58 |
| LOW_2Y_SHARPE | **2.07** | 1.58（部分 0.55/0.66） |
| LOW_RETURNS | **0.08** | ≤0.0614（6 颗全过） |
| LOW_FITNESS | 1.00 | 1.00 |

⇒ 存档 `chn_news46_cross_region_campaign_20261103.md` 记的「严闸 2.07」是真实的，不是笔误。**CHN 需要 S≥2.07 且年化收益 ≥8%**，比 GBR 高一个台阶。

## §2 chn1 八臂实测（`CCeS82qA4s69vf18OYHExvI`，CHN/TOP2000U/FAST/decay5/trunc0.10）

| # | 机制 | alpha | S | F | TO | 2Y | LC | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | **短反转标尺** `-group_rank(ts_delta(close,5),market)` | `ZYQXnW2n` | **-0.45** | -0.10 | 69.4% | -1.37 | 948 | ★ 标尺极弱：CHN 5 日并非反转 |
| 2 | insider top20 20d 水平 | `78LG1Kxb` | **-1.44** | -0.93 | 7.5% | -1.51 | 482 | ★★ 最强 |
| 3 | insider all 20d−250d 价差 | `j2YV0dn5` | **-1.45** | -0.89 | 6.9% | -1.40 | 549 | ★★ 最强，独立构造同号 |
| 4 | news46 mce 慢几何 | `KPJV9wXN` | -0.99 | -0.57 | 10.2% | -1.08 | 959 | |
| 5 | news46 ens 慢几何 | `0mYGEKeG` | -1.06 | -0.66 | 11.9% | -0.52 | 951 | |
| 6 | news38 正−负 情绪差 | `pwdWl1Vb` | -0.49 | -0.22 | 15.6% | -1.12 | 449 | |
| 7 | other370 情绪 慢几何 | `omEPl9n2` | -0.44 | -0.14 | 6.9% | 0.22 | 1001 | |
| 8 | market_news_sent 慢几何 | `xArlkmem` | -0.58 | -0.20 | 6.9% | 0.05 | 985 | |

**三条判据**：

1. **CHN 短反转标尺 = 0.45**（门槛 1.5）⇒ 按「塔全空 ≠ 好挖」纪律，CHN 整体信号标尺不达标。
2. **`insider_feats` 是 CHN 唯一有实质强度的机制**：两条结构完全不同的构造（top20 水平 / all 20d−250d 价差）一致给出 −1.44/−1.45 ⇒ 高买卖比 → 未来收益低（内部人买入拥挤反转），符号可信、非噪声。
3. 新闻族可复现存档结论（mws46 慢几何 −0.99~−1.06），但量级远低于 2.07。

## §3 CHN wave2（`2UlBN7bAG4z9ck76GVMvGJd`，8 臂全 ATOM）

全部围绕 `insider_feats`（118 字段，cov 0.58，aC 7）+ 1 条 news46 反号，结构互异：

| # | 模板 | 差异维度 |
|---|---|---|
| I1 | top20 20d 水平翻号 | 单腿·水平 |
| I2 | all 250d − all 20d 价差（换位而非取负） | 双腿·一阶 |
| I3 | 5/20/60/250 四期限复合翻号 | 多期限合成 |
| I4 | top20 − all 背离翻号 | 聪明钱 vs 全市场 |
| I5 | tx_count 比值翻号 | 换信息通道（笔数非金额） |
| I6 | top20 买入/卖出**成交量**比 10d 翻号 | 换量纲（量非笔数） |
| I7 | 净内部人卖出笔数（sale−buy） | 换函数形式（计数差） |
| I8 | news46 ens 快几何翻号 | 换塔（news） |

**验收**：S ≥ 2.07 且 R ≥ 8% 且 F ≥ 1.0 且 2Y ≥ 2.07。若本波最强 < 1.9 ⇒ CHN 按纪律判死（累计 16 臂，最强 1.45，距门槛 0.62）。

## §4 纪律沉淀

- **CHN 与 GBR 的闸不同档**：跨区移植配方前必须先读该区 `checks.fail[].limit`，不能沿用 1.58。
- CHN 默认档（存档）SUBINDUSTRY/decay4/trunc0.08；本探针统一用 FAST/decay5/trunc0.10 便于横向比较（存档实证 FAST 档会放大信号 0.36–0.90）。
- `insider_feats` 在 CHN 归属 category = **other** ⇒ 与 PV/MODEL/FUNDAMENTAL 混用会占「集合内×集合外 ≤5」额度；单集 ATOM 不占额度。

## §5 ★★★★★ wave2 实测与「翻号不对称」重大发现（2026-11-06）

`2UlBN7bAG4z9ck76GVMvGJd` 8 臂（全部为 chn1 强信号的**翻号/换位**版本），结果**全部为负**：

| # | 模板 | alpha | S | TO | LC |
|---|---|---|---:|---:|---:|
| I3 | 5/20/60/250 四期限复合翻号 | `npv62mPx` | -1.19 | 7.2% | 1380 |
| I8 | news46 ens 快几何翻号 | `0mYGExr6` | -1.13 | 15.7% | 1350 |
| I5 | tx_count 比值翻号 | `vR1YlZ2z` | -0.94 | 7.4% | 1384 |
| I1 | top20 20d 水平翻号 | `88RGQVjv` | -0.84 | 7.5% | 1439 |
| I6 | top20 成交量比翻号 | `9qxGr8Wr` | -0.78 | 7.8% | 1432 |
| I7 | 净内部人卖出笔数 | `ZYQXngA0` | -0.70 | 34.9% | 736 |
| I2 | all 250d − all 20d（换位） | `MPYgQdan` | -0.53 | 6.8% | 544 |
| I4 | top20 − all 背离翻号 | `78LG136O` | -1.39 | 7.1% | 1589 |

### ★ 决定性核对：翻号**不会**把 Sharpe 反号

| alpha | 代码 | S | PnL | longCount / shortCount |
|---|---|---:|---:|---|
| `78LG1Kxb` | `group_rank(ts_zscore(vec_avg(buy_sell_ratio_top20_20d_filled_2), 252), market)` | **-1.44** | -5,059,295 | 482 / 1439 |
| `88RGQVjv` | `-group_rank(ts_zscore(vec_avg(buy_sell_ratio_top20_20d_filled_2), 252), market)` | **-0.84** | -2,995,689 | 1439 / 482 |

两条设置完全相同（CHN/TOP2000U/D1/decay5/FAST/trunc0.10/nan ON/VERIFY），持仓多空数**精确互换**（482↔1439），但 **PnL 两条都是负的**。

⇒ **在 CHN 上「取负」不是免费的反向杠杆**：多头腿与空头腿的模拟条件不对称（A 股融券受限，空头腿成本/可借量不同）⇒ 反号后仍然亏。
⇒ **纪律更新**：任何区遇到「S 为负、想翻正」时，必须**实测反号版本**，不能按 `-S` 估算。GBR 侧此前 6 颗均为正 S，未暴露此问题。

### CHN 判决

- 累计 16 臂：chn1 最强 |S| 1.45、chn2 全部为负 ⇒ **正向可达上限 ≈ 0.84**（唯一正 S 的翻号件是 `88RGQVjv` 的镜像 `-0.84`）。
- 区域门槛 2.07 ⇒ 距门槛 **1.23**，且短反转标尺仅 0.45。
- **CHN 判死**（矩阵：门槛 2.07 / 标尺 0.45 / 16 臂最强 1.45 且不可翻号）。除非改用存档推荐的 SUBINDUSTRY/decay4 档重测（本波用 FAST，可能正是「翻号不对称」的放大源），否则不再投入。

## §6 2026-11-08 修补战役：FITNESS 修补成功但 prod 深钉（两阶段教训）

### 背景

`3qoGezVQ`（内部人净买入 avg_buy−avg_sell × 冷腿，S1.73/F0.96 仅差 FITNESS 0.04）。Fitness = S·√(R/max(TO,0.125))，实测 R≈5.0% ⇒ 只需 TO ≤ 15% 即可过 F≥1.0。

### 过程

1. **8 臂大批两连灭**（gbrf1 `2tWRLoeP24pTcqI1e7zE3unF`、v2 `3jMGj03bl572cBQUzS9ZOu5`）：8/8 子任务 FAIL、无 message、无 alpha_id；父任务 ERROR。**同表达式在 2 臂小批中全部存活** ⇒ 判定 8 臂大批当前有平台侧风险，GBR 改 2 臂滚动。
2. **判别探针法**（1 旧验证表达式 + 1 新表达式同批）：旧臂复现 S1.63 ⇒ 非表达式问题；新臂 `58E2dQZX`（tvr0.14）S1.70/F1.06/TO12.07% **全闸零失败**。
3. f3 四个 2 臂小批：f3a（tvr0.12/0.10）→ `rKRnajx8` S1.71/F1.07、`P0oAL7kJ` S1.73/F1.09 全零失败；f3d（66d 窗口 tvr0.14 + 252d tvr0.14 复刻）→ `P0oALL17` **S1.74/F1.10/TO11.95%/2Y2.68/sub1.77** 全零失败（66d 窗口反而最强）。
4. **互相关 0.988-0.999** ⇒ 四颗同信号只能取 1；择优 `P0oALL17`，self 0.2941 过。
5. **prod = 0.8384 ≥ 0.70 ⇒ 判死**。`insider_agg_matrix` 族是深钉 prod：`3qoGezVQ`（原始）0.9615 附近、修补版 0.8384，几何/窗口修补只能从 0.95+ 移到 0.84，过不了 0.70。

### 结论

- **FITNESS 修补技术路线完全成熟**：`ts_target_tvr_decay(core, target_tvr≈0.10-0.14)` 把 TO 压到 11-12%，F 从 0.96 → 1.06-1.10，S 不降反升（1.73→1.70-1.74）。任何「只差 F 一档」的候选都该先跑这个。
- 但 **prod 墙不随几何修补移动**（与 KOR 中性化扫档经验相反）——insider 族 prod 是机制级常数。同族多臂在互相关 0.99 下只有 1 次机会，先看同族有没有已提交/prod 已知的钉子再派。
- f3b（secondary/top 子集）与 f3c（directional）若收割出全闸件，因与 f3a/d 同数据集不同字段族，prod 可能同钉；先互相关，≠同族才值得烧 prod。

## §7 2026-11-08 ★★★★★ 第 7 颗成立：bl6KwjwK（starmine 修订广度 × COLD）

| 项 | 值 |
|---|---|
| 表达式 | `add(multiply(2, group_rank(ts_zscore(subtract(analyst_upward_revision_count_fy1_revenue_7d_4, analyst_downward_revision_count_fq1_revenue_7d_5), 66), sector)), reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))` |
| 机制 | 分析师 FY1 收入上修净广度（修订漂移，Womack/Chan 系）为主腿，冷腿（贷出股数反转）2:1 加权 |
| 指标 | **S 1.89 / F 1.06 / TO 17.11% / R 5.34% / 2Y 2.80 / sub 1.18 / LC 442 / DD 3.08%** |
| 闸 | `checks.fail = []`（零失败）、`ra.failed_ra_count = 0` |
| 互相关 | vs 6 颗篮子：0.2226/0.4578/0.1596/−0.0219/0.4142/0.0085 **全 < 0.70** |
| self | **0.1767** ✓ |
| **prod** | **0.4582 ✓（< 0.70）** |
| 塔位 | GBR/D1/SHORTINTEREST(1.2) + GBR/D1/MODEL(1.4)，effective 2 |
| 算子数 | add/multiply(2)/group_rank(2)/ts_zscore(2)/subtract/vec_sum/reverse = 9 ≤ 12 ✓ |

### 为什么 starmine 能出：

- 108 个 upgrade/downgrade 修订计数字段，字段级 aC 0–17 ⇒ 生产池几乎没人用（低 prod 根因）。
- cov 双档：0.946（主）/0.603（备用编号字段）⇒ 覆盖达标。
- 机制 = 修订广度漂移（每周 7d 窗口净上修），与动量/情绪机制相关性低 ⇒ 对篮子互相关最高仅 0.4578。

### 同批对照（降级不追）

- `P0oAV7Vp`（升级比率 up/(up+down)）S0.90 —— 比率面弱于净广度面。
- `leANm5zN`（7d 升降级净计数）S0.83、`vR1oQpJa`（90d 净计数）S1.40 —— 均不过 S 线，修订计数面收敛于 FY1 收入修订。

### 论坛情报（先行核实）

- 「EUR_TOPCS1600__D1_news18 不好搞」（2400 表达式均值 S 0.05）⇒ news18/news50 降级，未浪费批次。
- 评论「勤换中性化、处理换手 margin 就上来了」与本次 tvr 修补配方一致。

## §8 2026-11-08 ★★★ 交付篮子 0.5 口径核定（全局标准落地）

用户 11-08 两次指令：**多 alpha 组合互相关全对 <0.5 是全局标准**。对 7 颗全闸件跑 `compute_mutual_correlation(threshold=0.5)`：

| 超线对 | 相关 |
|---|---:|
| 3qoGxkqZ ↔ ZYQXZj73 | 0.5449 |
| 3qoGxkqZ ↔ RRE5Mwkn | 0.5132 |

⇒ **最大独立集 = 6**（平台精确解 `max_mutually_below_subset_size = 6`）：`RRE5Mwkn / ZYQXZj73 / QPvbxjXw / rKRPAWv9 / leAgQPO5 / bl6KwjwK`。
⇒ `3qoGxkqZ`（S 2.48/F 1.33/prod 0.6729）虽然单颗最强之一，但与两颗篮内件超 0.5 ⇒ **移出交付篮**（保留为换防备件）。

### 组合配额更新（派发前置检查）

- 集合内×集合外组合类型已用满 5：`PV+SHORT`、`OTHER+SHORT`、`SENTIMENT+PV`、`RISK+PV`、`SHORT+MODEL`。
- 新的组合只能走**集合外×集合外**（SHORTINTEREST/ANALYST/NEWS/SENTIMENT/IMBALANCE/INSTITUTIONS/INSIDERS 之间），或**单数据集 ATOM**（不占配额）。
- `SHORT+MODEL` 已有 1 席（bl6KwjwK），同组合上限 3，还有 2 席。

## §9 2026-11-08 starmine 扩面实测：其余修订面全线弱于 FY1 收入面（数据集收敛）

sm3 四臂（全部 × COLD 2:1，SHORTINTEREST+MODEL 组合第 2/3 席试探）：

| 臂 | 机制面 | alpha | S | F | 判定 |
|---|---|---|---:|---:|---|
| ebitda 14d 净修订 | FY1 EBITDA 上修−FQ1 下修 | `LLMwPOQv` | 1.27 | 0.63 | 不过 S 线 |
| earnings 30d 净修订 | FQ1 earnings | `j2YJ5zge` | 1.25 | 0.51 | 不过 S 线 |
| ebitda 30d 净修订 | FY1/FQ1 EBITDA | `npvl1wEd` | 0.93 | 0.39 | 弱 |
| ebitda 7d × earnings 混合 | 混科目 | `88RZm5Lq` | 0.76 | 0.34 | 弱 |

⇒ **predictive_starmine 收敛**：仅 FY1 收入修订净广度（bl6KwjwK）一席，其余科目面（EBITDA/earnings）信号强度系统性低一档（1.25-1.27 vs 1.89）。不再扩面，SHORTINTEREST+MODEL 组合维持 1/3 席。

**台账终态（2026-11-08 14:5x）**：交付篮（0.5 口径）= 6 颗；第 8 颗方向转离 starmine。

## §10 2026-11-08 news50 / analyst48 判死记录

**analyst48**（7 字段 aC26 cov0.807）：字段全为索引元数据（divisor/成员数/标识符/return_code），无信号价值 ⇒ 数据集级死。

**news50**（37 字段 mws50_*，aC 361，cov 0.691）：用 rKRPAWv9 同款慢几何模板（tvr0.05/decay15/trunc0.05）测 4 字段 × 双向：

| 字段 | 反号 S | 翻正 S |
|---|---:|---:|
| mws50_ess（情绪分） | −0.44 | —（未翻，反号已弱） |
| mws50_qmb | +0.55 | +0.65* |
| mws50_ens | −0.65 | +0.69* |
| mws50_nip | −0.69 | +0.65* |

（* 翻正批 = ens/nip 正向 +nip 正向；双向 S 均在 ±0.7 内 ⇒ **双向都弱，信号强度不足**，非方向问题。）⇒ news50 判死。

**News 家族 GBR 终局**：nws17（rKRPAWv9 在篮）是唯一出货面；nws18（论坛 2400 表达式 S0.05）、nws20（0.82）、news50（±0.7）、news104（0.81/0.90 amp 弱）全灭。NEWS 塔不再扩。

**台账终态（2026-11-08 15:1x）**：交付篮（0.5 口径）6 颗；累计探针约 200 条。第 8 颗仍缺——下一步候选：multifactor_return_pred（648f aC288 cov0.464，MODEL 塔）、model109（542f aC877 cov0.469），或把 COLD 打到 analyst9 其余 est 字段（SHORTINTEREST+ANALYST 新组合，不占配额）。

## §11 2026-11-08 15:2x ★ 平台 GBR 仿真通道异常，按纪律停手

analyst9 修订广度批（SHORTINTEREST+ANALYST 新组合，预检过）两批父+子任务全部 ERROR（无 message）；原样重派 0.1→ERROR；**连当日多次成功的 COLD 单腿判别探针也 0.1→ERROR** ⇒ 表达式无关，平台 GBR 仿真通道时段性异常。

**处置**：停手不烧批次；待平台恢复后重派 `results/_call_a9retry.json`（2 臂：anl9_s_numup−numdn 66d、anl9_daily_numup−numdn 66d × COLD）与 `results/_call_envprobe.json`（COLD+裸 analyst9 判别对）。

**本日收官统计**：交付篮（0.5 口径）6 颗不变；news50 六臂双向判死、analyst48 判死、starmine 扩面收敛；第 8 颗候选（analyst9 修订广度 × COLD）表达式已备好等窗口。

## §12 2026-11-08 15:0x 平台关闭期的画像储备（仿真零消耗）

- **f3b/f3c**：仍卡 10%（排队中，未死）。
- **multifactor_return_pred**（648f）：首 120 字段 aC 中位数 **0**、cov 中位 0.43——极冷但覆盖不足（篮内件池 LC 450+ 靠 cov 0.75+；cov 0.48 ⇒ LC 预计掉到 ~250-300，S 先验弱）。**降级为备选**。
- **model109**（542f）：aC 中位 4、cov 中位 0.47——同样冷而稀。备选。
- **analyst9**（51f）：修订广度族（s_numup/dn cov0.80、daily_numup/dn cov0.74）覆盖率合格 ⇒ **第 8 颗首选不变**。
- 重派文件已去重更新：`_call_a9retry.json` = [s 快照 66d 净广度 × COLD, daily 比率版 × COLD]（sm3 已测的 ebitda 臂已剔除）。

**等待策略**：30 分钟自我提醒复查平台；恢复后顺序 = 探针 → analyst9 批 → 0.5 互相关 → self → prod。

## §13 2026-11-08 15:1x analyst9 修订广度机制：论坛先验核查（派发前铁律执行）

按「用机制前先查论坛」铁律检索，**机制获多篇独立帖验证**：

1. **《分析师盈利预期修正广度：盈利动能的横截面代理》**——直接背书 up/down 家数广度设计：「比单分析师修正幅度更稳健，广度更能反映一致预期的方向性变化」。伪代码 breadth = up/down 或 up/(up+down) ⇒ 我的两臂（净差 + 比率）正好是它的两种形态。
2. **《分析师共识的三种读法：水平、修订与扩散》**——强调**扩散（diffusion）抓共识变化的质量**：十人各上修 2% ≠ 两人上修 10%。
3. **《上修之后，分歧有没有一起收敛》**——上修×分歧收敛 = 可信度筛选（interaction 想法，若首批出货可做第二波）。
4. **《分析师数据字段的有效信号挖掘策略》**——rank(ts_sum(up−down, 22)) 聚合变体（备选第三波）。

**⚠️ 跨区警示**：《分析师修订字段在东亚市场是弱信号（KOR 三批 32 槽）》——KOR 修订族结构性弱（S 0.23-0.52）。GBR 与 KOR 不同市场（starmine 广度在 GBR 出了 S1.89），但若 a9 首批全弱，**按此证据直接收敛，不再磨**。

⇒ **a9 首批设计维持不变**（净差 66d + 比率版，× COLD），恢复后即派；dispersion-converge 交互与 ts_sum 22d 留作第二/三波备选。

## §14 2026-11-08 15:2x 备选集全量终审：multifactor_return_pred / model109 钉死降级

用 max_fields 放开拿全量（绕过 offset 不生效的包装坑）：**multifactor_return_pred 648 字段 covMax=0.4806、model109 542 字段恒 cov=0.478** —— 两个数据集的覆盖是**数据源级平的**，无任何高覆盖冷门字段。降级判定从首 120 抽样升级为全量证据，正式钉死。

⇒ **第 8 颗唯一主线 = analyst9 修订广度批**（论坛先验已核），恢复后即派。工具坑记录：get_datafields 的 offset 在 MCP 包装里不生效，翻全量要用 max_fields=platform_count。

## §15 2026-11-08 15:3x ★★★ 跨区诊断：异常是 GBR region 专属，非账号/平台级

DEU/TOP500 同时刻 2 臂通用探针（short-reversal + volume ts_rank，纯内置字段）：**COMPLETE**，两臂真出货（`E56MWYA9` S0.87/LC193、`WjORQnkN` S1.61/LC190——量级符合 DEU 冷腿标尺 0.84 的既有认知，未翻案）。

⇒ 同一账号、同一分钟：DEU 正常 vs GBR 7 连 ERROR + f3b/f3c 卡 10% ⇒ **GBR 数据面/仿真队列 region 级异常**。

**含义**：
1. GBR 异常可能不会随平台整体恢复而自愈，恢复时间不可预测 ⇒ 15:29 提醒继续探 GBR（原 prompt 已含）。
2. f3b/f3c 卡 10% 与 GBR 异常同源。
3. 若 GBR 长时间不恢复，**转区挖矿成为一个真实选项**（EUR/DEU 仿真通道健康）——但 DEU 冷腿标尺 0.84 已判死、EUR analyst 塔已点亮（10）且未获用户授权放开 ⇒ **转区需用户决策，不擅自扩大**。

**当前决策树**：GBR 恢复 ⇒ analyst9 批（第 8 颗主线）；GBR 长期不恢复 ⇒ 向用户报告转区选项，等指示。

## §16 2026-11-08 15:3x 恢复后执行序列全量预备（wave-2 预检通过）

analyst9 4 臂矩阵全部预检就绪，恢复后两批连发：

| 文件 | 臂 | 状态 |
|---|---|---|
| `_call_a9retry.json` | ① s_numup−dn 66d 净差 × COLD ② daily 比率版 × COLD | ✅ 预检过 |
| `_call_a9w2.json` | ③ daily_numup−dn 66d 净差 × COLD ④ s 22d 快窗 × COLD | ✅ 预检过（本轮） |

（原 4 臂中 ②③④ 曾在 ERROR 批里未真正运行，全部保留待测。）

**恢复后标准流程**：探针 COMPLETE ⇒ 连发两文件 ⇒ 收割 ⇒ 全闸件 0.5 互相关 vs 篮子 ⇒ self ⇒ prod。

## §17 2026-11-08 15:3x 转区预备：EUR 未点亮塔画像（仅画像，不派发，等用户决策）

GBR 故障 55min+，提前为转区选项做画像预备（EUR 通道健康已证）：

**EUR/D1 塔位**：analyst 10（lit）、model 3（lit）、fundamental 3（lit）、imbalance 3（lit）已点亮；**news 1、sentiment 2、pv 2、insiders 2、other 2、risk 2 未点亮**；socialmedia/macro/earnings/institutions = 0。

**候选数据集画像**：

| 数据集 | 画像 | 初判 |
|---|---|---|
| sentiment26（17f，snt26_*） | dltcc **cov1.0**/a59、relpopularity 0.75/a91-103、skewness/top10rank 0.75/a16-31 | ★ 可挖：注意力/人气族，冷门字段多 |
| news36（15f，mws36_*） | 全字段 cov **0.77 统一**、aC **0-26 全冷门**（novelty/sentiment_confidence/key_event） | ★★ 最符合「冷门字段族」筛选器 |
| news29（12f） | EUR 无字段（0 条） | ❌ 排除 |
| sentiment21（210f） | aC3791 拥挤 | 暂缓 |

⇒ **若用户授权转区**：首选 news36（冷门+高覆盖+未点亮 NEWS 塔，bl6KwjwK 同款打法）+ sentiment26 辅助线。转区需用户明确授权，未获授权前不动。

## §18 2026-11-08 15:3x EUR 转区线修正：无 COLD 冷腿，news36 改 ATOM 路线

预检抓到关键事实：**`loaned_share_count_main` 在 EUR 不存在**，且 EUR **没有 shortinterest category**（数据集清单为空）⇒ GBR 的 COLD 2:1 配方**无法平移到 EUR**（与 ASI 同款约束）。

**修正后的 EUR news36 路线 = 单集 ATOM**（不需要伙伴腿，且不占组合配额）：

| # | 机制 | 形态 |
|---|---|---|
| 1 | 正负情绪短语净差 | 66d zscore·sector |
| 2 | novelty 水平 | 66d zscore·sector |
| 3 | novelty 反号慢几何（注意力反转，Da et al.） | SLOWGEO·tvr0.05 |
| 4 | 新颖度期限差（newest−oldest span） | 66d zscore·sector |

文件：`_call_n36apf.json`（预检✅）/ `_call_n36atom.json`（派发就绪）。表达式中 `loaned_share_count_main` 版本（`_call_n36.json`）**作废勿发**。

**EUR 转区线终态**：news36 ATOM 4 臂就绪；sentiment26（dltcc cov1.0）为第二波候选。GBR analyst9 4 臂同就绪——**两区任一恢复/授权即出第 8 颗**。

## §19 2026-11-08 15:4x EUR sentiment26 线就绪（转区预备全部完成）

sentiment26（17 字段 snt26_*，cov 0.58-1.0，aC 7-103）4 臂预检通过（`_call_s26.json`）:

| # | 机制 | 字段 |
|---|---|---|
| 1 | dltcc 水平（**cov 1.0** 最高覆盖字段） | snt26_dltcc |
| 2 | relpopularity1 人气衰减 | 66d Δ·252 zscore |
| 3 | skewness 偏度 | 252d |
| 4 | top10pctrankingavg 头部排名反号 | 252d（注意力反号，参照 GBR snt27 同族 S−0.75） |

**EUR 转区包终态**：news36 ATOM 4 臂（`_call_n36atom.json`✅）+ sentiment26 4 臂（`_call_s26.json`✅）= 8 臂两批，用户授权即连发。

**台账等待期工作全部完成**（§1-§19）。下一事件：16:30 提醒探 GBR。

## §20 2026-11-08 15:4x 论坛/公告核查：官方无本轮故障通告

检索 BRAIN 论坛「simulation ERROR / 平台故障公告」：无 2026-11-08 当日公告；相关帖均为历史经验（2025-12 multi_sim ERROR 排查、2026-07 create_multi_simulation 超时）。⇒ 本轮 GBR region 故障**未被官方通告**，恢复时间只能靠探针实测。16:30 提醒继续。

## §21 2026-11-08 15:5x ★★★★ 交付篮终审快照：发现两颗已被提交（用户自行操作）

对 6 颗交付篮做提交前终审快照（get_alpha_details），发现：

| alpha | status | dateSubmitted |
|---|---|---|
| RRE5Mwkn | **ACTIVE** | **2026-11-08 02:00 美东** |
| bl6KwjwK | **ACTIVE** | **2026-11-08 02:00 美东** |
| ZYQXZj73 / QPvbxjXw / rKRPAWv9 / leAgQPO5 | UNSUBMITTED | — |

⇒ **用户在 11-08 下午自行提交了 RRE5Mwkn 与 bl6KwjwK**（本会话从未执行提交流程；当时「暂不提交」的问卷默认项不代表用户真实意愿，用户显然自己动手了）。

**金字塔实测（提交后）**：shortinterest **0→3 点亮** ✅、pv 2→4、model 3→6（+3 来源待核：非本会话产出，可能为用户提交的其他存量件）、news 3、analyst 3、fundamental 3。

**篮子更新**：可提交余 4 颗（ZYQXZj73 / QPvbxjXw / rKRPAWv9 / leAgQPO5）。0.5 口径矩阵在去掉已提交两颗后无变化（原矩阵里它们与其他四颗全 <0.5）。

**SHORTINTEREST 塔已点亮** ⇒ 依赖 COLD 腿的新组合价值重估：COLD 腿关联的 SHORTINTEREST 塔已亮，未来新组合改用其他塔位更优；存量 COLD 配方候选仍可继续（点亮已不增收益，但塔配额不变）。

## §22 2026-11-08 16:48 恢复后复核：第 13 连 ERROR，提醒重设

Runtime 恢复（16:48）后探针：**ERROR（第 13 连）**，故障窗口 ~110 分钟。原 16:31 提醒因 Runtime 恢复丢失，已重设 60 分钟节奏（含最新事实与"顺延不再报用户"的修正——转区问卷已在 15:4x 摆出且未获授权，静默等待用户主动指示）。

## §23 2026-11-08 16:5x EUR 试发（用户指令「重新生成试下」）：news36 判死，sentiment26 在飞

GBR 重试探针第 15 连 ERROR（用户指令下重试，确认故障仍在）⇒ 按用户「试下」语义转 EUR 通道试发：

- **news36 ATOM 4 臂 COMPLETE**：S 0.02-0.28 全弱（最好 0.28 = 闸 18%，与 analyst83 判死同型）⇒ **news36 判死**。alpha：GrWNMP3G / YP1O262W / E56Mg1gL / QPvA2Mnr。
- **sentiment26 4 臂在飞**（`3AK7Q7eqC4U8ccGZQbuXcJD`，35% 处）。

**交叉验证再次确认**：GBR ERROR vs EUR COMPLETE 同账号同分钟 ⇒ region 级故障结论稳固。

## §24 2026-11-08 17:0x sentiment26 收割：EUR 两条初探线全部判死

sentiment26 4 臂 COMPLETE（`3AK7Q7eqC4U8ccGZQbuXcJD`）：

| # | 机制 | alpha | S | 判定 |
|---|---|---|---:|---|
| 1 | dltcc 水平（cov1.0） | `gJe5RNd0` | 0.45 | 弱 |
| 2 | relpopularity1 人气衰减 | `pwdkVb3g` | 0.48 | 弱 |
| 3 | skewness | `A1V5gXEw` | 0.33 | 弱 |
| 4 | top10rank 反号 | `QPvA2R6W` | -0.09 | 弱 |

⇒ **EUR 初探收官**：news36（max 0.28）+ sentiment26（max 0.48）双判死。EUR 未点亮塔的冷门数据集**首层试探**完成，均为弱信号面。EUR 剩余可试：news50（GBR 同名集 EUR 版 aC466）、news31（aC1178）等中拥挤集，但先验不强。

**总战况**：第 8 颗仍缺。GBR analyst9 4 臂就绪等恢复；EUR 初探 8 臂判死（冷门≠有信号，再次验证）；16:52 提醒已重设 ~17:52 触发。
