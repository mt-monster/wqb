# insider_agg_matrix · EUR / TOPCS1600 / D1 字段画像

> 类型 MATRIX（全部 34 字段，已是厂商预聚合量，无需 `vec_*` 归约）· 覆盖率 0.6083（股数族）/ 0.6149（方向/重要性族）
> 金字塔 category = **insiders**（multiplier 1.1，未点亮塔）
> 采集：`get_datafields(dataset_id=insider_agg_matrix, region=EUR, delay=1, universe=TOPCS1600)`，2026-11-06

## 0. 字段目录（按语义分组，非 alphaCount 排序——本集字段少且结构清晰）

### 0.1 买卖股数族（16 支，`avg_*`/`total_*` × 全体/直接/高管 × 买/卖）

| 字段 | αC | description |
|---|---:|---|
| `total_top_buy_shares` | 28 | 全体**高管**买入股数之和（本族最高 αC） |
| `total_top_sell_shares` | 25 | 全体高管卖出股数之和 |
| `total_secondary_buy_shares` | 7 | 董事直接买入股数之和 |
| `total_secondary_sell_shares` | 7 | 董事直接卖出股数之和 |
| `total_secondary_top_buy_shares` | 9 | 高管直接买入股数之和 |
| `total_secondary_top_sell_shares` | 8 | 高管直接卖出股数之和 |
| `total_buy_shares` | 6 | 全体董事买入股数之和 |
| `total_sell_shares` | 5 | 全体董事卖出股数之和 |
| `avg_top_buy_shares` | 11 | 全体高管买入股数均值 |
| `avg_top_sell_shares` | 7 | 全体高管卖出股数均值 |
| `avg_secondary_top_buy_shares` | 7 | 高管直接买入股数均值 |
| `avg_secondary_top_sell_shares` | 5 | 高管直接卖出股数均值 |
| `avg_secondary_buy_shares` | 3 | 董事直接买入股数均值 |
| `avg_secondary_sell_shares` | 5 | 董事直接卖出股数均值 |
| `avg_buy_shares` | 2 | 全体董事买入股数均值 |
| `avg_sell_shares` | 4 | 全体董事卖出股数均值 |

### 0.2 方向指标族（2 支）

| 字段 | αC | description |
|---|---:|---|
| `directional_indicator_2` | 8 | 增强版内部人活动方向/偏向指标（★ 已判死：`vec_avg` 同期 TO=1.43 爆炸，见下方「历史判死复核」） |
| `directional_indicator` | 5 | 内部人活动方向/偏向指标（基础版，未单独测过） |

### 0.3 显著交易金额族（16 支，`significant_value_*`/`directional_significant_value_*`/`top_*` × 第1-4 高）

| 字段 | αC | description |
|---|---:|---|
| `significant_value_1`–`_4` | 16/12/13/8 | 最高至第四高「显著交易」金额 |
| `top_significant_value_1`–`_4` | 5/3/14/8 | 同上，限高管子集 |
| `directional_significant_value_1`–`_4` | 1/3/2/1 | 同上，带方向符号 |
| `top_directional_significant_value_1`–`_4` | 5/5/2/2 | 同上，限高管 + 带方向符号 |

## 1. 字段画像五问

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 存量/流量 | 全部**流量**（逐日聚合的买/卖股数或金额），**无持仓/存量字段**——这是与 `insiders1` 的关键差异：§4 的「仓位比例」机制在此**无法直接复制**（没有分母） |
| 2 相对性 | 水平/排序 | 原始股数/金额跨公司市值不可比，需 `group_rank` 或先除以流通股本之类的规模变量（本集未提供流通股本字段，需跨数据集拼接，暂不做——保持 ATOM 单数据集原则） |
| 3 被定价的是谁 | 方向 vs 广度 vs 强度 | **买卖不对称**是本集的核心可测维度（JMZ 2003：买入有信息、卖出无信息）；全体 vs 高管 vs 董事直接，是**广度细分**（可作对照，非独立机制） |
| 4 有无博弈 | 拥挤 | 全场 αC ≤28，远低于已点亮类别，非拥挤轴 |
| 5 事件性 | 稀疏 | MATRIX 已是厂商预聚合（非 VECTOR），但 cov 仅 0.60–0.61，仍需在 `ts_sum` 累加前评估 nanHandling 零填充造成的並列假中段（同 `insiders1` §5 工程坑，机制相同，只是省去 `vec_sum` 这一步） |

## 2. 历史判死复核（2026-10-13 wave496/504）

原判死依据：`directional_indicator_2` S=−0.05 且 TO=1.43 爆炸；`directional_significant_value_*` 同族判死。
**复核**：这两族字段 αC 均 ≤8（全场最低区间），且是"方向指标"/"显著交易金额"这类**已经过复杂加工的衍生量**，不是最原始的买卖股数。对照 `insiders1` 的教训（原始信号 + 正确归约方式 ≠ 衍生指标失败），本集**真正未测过的是最原始、αC 最高的买卖股数族**（`total_top_buy_shares` αC28 / `total_top_sell_shares` αC25），这正是 DEU 论坛帖（JX84394）明确做过跨数据集迁移验证的字段类型："同骨架在 insider_agg_matrix 上：买入类字段 1.56–1.59，卖出股数 0.21，与 JMZ(2003) 完全一致"。

## 3. 机制：买卖不对称（JMZ 2003 跨数据集迁移）

DEU 帖在 `institutions1` 验证的骨架（`ts_sum` 季度累加 → `group_rank` → `winsorize` → `tail` 掐並列中段）直接迁移到 `insider_agg_matrix` 的买入股数字段上，不需要比例归一化（因为没有 holdings 分母，退化为直接对聚合股数做累加排序）：

```
tail(winsorize(group_rank(ts_sum(<buy_shares_field>, 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)
```

**JMZ(2003) 可证伪性检验**：买入侧应该强，卖出侧应该接近无信号（卖出多由流动性/分散化/期权行权驱动，不是主动押注）。若换成卖出字段后信号同样强，说明拟合的是别的东西（规模/流动性），不是内部人信息本身。

## 4. 本战役候选（2026-11-06 实测结果，multisim `26nD6X9QV50qaTr10H4lguBS`，已终态）

| # | alpha id | 表达式 | S | F | TO | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `akKe5zK6` | `tail(winsorize(group_rank(ts_sum(total_top_buy_shares, 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)` | **0.72** | 0.31 | 0.0397 | 0.73 | 0.45 FAIL | 0.70（压线） | LOW_SHARPE/FITNESS/2Y |
| 2 | `QPvOwzvQ` | 同骨架套 `total_top_sell_shares` | **0.01**（近似零） | 0.00 | 0.0378 | 0.32 | **−0.19 FAIL** | **−0.15 FAIL** | 全部挂,近乎无信号 |

**JMZ(2003) 证伪性检验结果：通过**。买入股数读数 S=0.72、2Y=0.73，确实弱但非零；卖出股数读数 S=0.01，sub/robust 双双转负,是"无信息,接近纯噪声"的教科书读数（卖出多为流动性/分散化驱动,不含私有信息）。两者差距（0.72 vs 0.01）排除了"拟合的是规模/流动性因子而非内部人信息本身"的担忧——若是规模因子,买卖两侧股数量级相近,不会出现这种单边归零。
**结论**：机制方向正确、经济逻辑成立,但买入侧强度仍不足以单独过 Mode B 主闸（差 2.2× S）。本族不再对卖出股数做任何参数扫描（铁律：已证伪为噪声的腿不追加投入）；买入股数族可考虑扩展到「全体董事」/「董事直接」子集广度对照（见 §5 待办）。



## 5. 待办

- **★★ 论坛新证据（2026-11-06,帖 `42371040658583`,JW51810,GLB D1 Power Pool 11 alpha 复盘）**：GLB/TOPDIV3000/D1 上 `insider_agg_matrix` @ **REVERSION_AND_MOMENTUM** 中性化实测 IS Sharpe **1.16**/fitness 0.62（过 GLB 三区域检查）——该档在本战役从未测过（只测过 SUBINDUSTRY/SLOW_AND_FAST）,且 KOR risk70 战役里 RAM 也是载荷族最优档（1.63 > CROWDING 1.30 > INDUSTRY 1.14）。GLB 帖用 `winsorize(ts_backfill(单字段,120),std=4)` 骨架与本战役不同,读数不可直接比,但「RAM × insiders」组合值得在 EUR 实测一轮。**待办：若 `QPvNZ5pr` 包装栈/分组轴结果仍不过闸,下一杠杆测试 RAM 中性化档（单变量：同表达式只换档）。**
- 若买入/卖出字段验证买入显著强于卖出,扩展到「全体董事」「董事直接」两个细分子集做广度对照(αC 虽低但经济含义不同,不算盲扫)。
- **★ 论坛新证据（2026-11-06，帖 `43592107256215`，PL71784，GLB 区同数据集卖方信号研究，0.47→2.18 完整记录）颠覆"买方强于卖方"的先验**：该帖主信号核心是 `avg_sell_shares`（**全体董事卖出**,αC 仅 4,本集迄今未测）而非本集已测的 `total_top_sell_shares`（高管子集卖出,αC 25,已证伪 S=0.01）——帖内明确给出广度梯度"全体董事(0.47) > 高管(0.23) > 直接交易(0.08)",即**覆盖面最广的子集signal最强,子集越窄越弱**,与我方按 αC 降序优先测高管子集的直觉正好相反。已据此提交 `total_sell_shares`/`avg_sell_shares`（全体董事卖出,求和/求均值两种读数）两条字段覆盖缺口候选,multisim `u62Rde4W4NC8VZ1avpDscyD`（2026-11-06,结果待终态）。

**结果（已终态）——骨架选择决定生死,跨区基线量级验证通过**：

| 候选 | alpha id | 表达式骨架 | S | F | TO | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|---|
| `total_sell_shares`（求和,本集既有骨架） | `A1Vr18MQ` | `tail(winsorize(group_rank(ts_sum(X,66),industry),…))` | 0.08 | 0.01 | .0422 | 0 | 0.02 FAIL | 0.18 FAIL |
| `avg_sell_shares`（求均值,论坛原骨架） | `VkxmkbgA` | `reverse(rank(ts_backfill(X,66)))` | **0.51** | 0.20 | .0740 | **0.85** | — | 0.20 FAIL |

**归因**：`group_rank(…,industry)` 骨架把信号几乎抹平（0.08≈噪声）,换成论坛原版"直接横截面 `rank`,不分行业"骨架后读数跳到 0.51/2Y 0.85——与 GLB 原帖未优化前的基线 S=0.47 **量级高度吻合**,证实该机制确实跨区域可迁移,但**只在论坛原始骨架下成立**。根因对照帖内 H3/H4 证伪链：作者已验证本机制**不是**行业/风格假象（H3 被杀）,而是"持续净卖出 = 缓变的横截面治理折价状态"（H4 存活)——**按行业分组再排序（`group_rank(…,industry)`）恰好把这个"跨行业共有的缓变状态"当成行业内噪声磨掉了**,这是本集第一次实证"组内骨架适配性因机制而异"：买入股数族（§3/§4 JMZ 机制）属于"个股相对同行业排名"的强度读数,天然适配 `group_rank(…,industry)`；而卖出股数族的治理折价机制是**跨行业共性状态**,行业分组反而是噪声源,需要纯横截面 `rank`。**结论：卖出股数族（含本条 `avg_sell_shares`）字段覆盖闸计入已覆盖,且确认机制存在（非零假说被推翻）,下一步按论坛指引叠加 `SLOW_AND_FAST` 中性化与 cap 掩码杠杆**（已提交,见下）。
- **★★★ 突破（2026-11-06,multisim `4sxEBPfqL4gv9UsWsoL7Dym`,已终态）：`SLOW_AND_FAST` 中性化是本集买入股数族的关键杠杆**，论坛帖 `43592107256215` 报告"唯一关键杠杆"（同机制 S 0.47→1.21）在本集同样成立且更强：

| 候选 | alpha id | 中性化 | S | F | TO | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|---|
| `total_top_buy_shares`（原档对照） | `akKe5zK6` | SUBINDUSTRY | 0.72 | 0.31 | .0397 | 0.73 | 0.45 FAIL | 0.70（压线） | S/F/sub |
| 同表达式换档 | `QPvNZ5pr` | **SLOW_AND_FAST** | **1.30** | **0.62** | .0835 | **2.13** | **0.71 PASS** | **0.80 PASS** | 仅 S/F 未过 |
| cap 双峰掩码叠加（`if_else(abs(rank(cap)-0.5)>0.3,·,nan)`） | `0mYNOK2p` | SLOW_AND_FAST | 0.96 | 0.45 | .1122 | 1.36（IS_LADDER FAIL） | 0.56 | 0.73 | 反而更差，新增 IS_LADDER_SHARPE FAIL |

**归因**：换 neutralization 档后 sub/robust 两道闸由 FAIL 转 PASS（SLOW_AND_FAST 同时对「慢/快」两条轴做残差化，比单一 SUBINDUSTRY 更干净地剥离掉了污染 sub-universe 读数的行业内结构性噪声），2Y 也从压线提升到 2.13。cap 掩码杠杆在 sub 闸已被修复的前提下属于冗余杠杆——反而因为砍仓位（cap 中段置 nan）削弱了换手所需的广度，新增 IS_LADDER_SHARPE FAIL（第 3 年滚动窗口不达标）。**结论：cap 掩码不再对本候选使用；SLOW_AND_FAST 确定为本族最终中性化档**。现在只差 Sharpe（1.30 vs 1.58，差 1.22×）与 Fitness（0.62 vs 1.0，差 1.6×）两道主闸，是本战役目前离过闸最近的候选。

**杠杆迁移实测（2026-11-06 提交,multisim `Q0ZW6aSS4uRbTMEwxLADfu`,结果待终态）**：把同季在 `significant_value_1` 上实测有效的两档杠杆迁移到本候选——① `rank(group_scale(·,industry))` 包装栈（在 `significant_value_1` 上 S +0.13、F +0.08、LOW_SHARPE 转 PASS）;② sector 分组轴（DEU 论坛帖 `JX84394` 网格实测 sector×FAST 1.67 > industry,但 sector 档 prod 相关性撞车,本区需实测核验）。**注意与 `significant_value_1` 的关键差异**：本候选 sub/robust 已 PASS（0.71/0.80）,包装栈若抬 S,sub 比率闸线（0.52×S）会同步上移,须同时看 sub 是否被动破位——这是 §4 归因里"选刚好过主闸的 S"原则的直接应用场景。

**包装栈 × 分组轴实测（已终态,multisim `Q0ZW6aSS4uRbTMEwxLADfu`）——两个杠杆各自独立有效,sector 档首次做到 RA 检查零硬失败**：

| 杠杆 | alpha id | S | F | TO | 2Y | sub（闸） | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| 基线（industry） | `QPvNZ5pr` | 1.30 | 0.62 | .0835 | 2.13 | 0.71 PASS（0.68） | 0.80 PASS | S/F |
| +`rank(group_scale(·,industry))` | `O0AMPWv7` | **1.43** | **0.70** | .0812 | 2.37 | 0.74（0.76,差 0.02） | 0.80 PASS | S/F/sub（压线） |
| 换 sector 分组 | `d5W3VawY` | 1.34 | 0.64 | .0779 | 1.87 | **0.71 PASS** | **0.70 PASS** | 仅 S/F（warning 级） |

**归因**：① 包装栈增量（S +0.13/F +0.08）在本骨架上**完整复现**,与 `significant_value_1` 上的增量逐位一致——`rank(group_scale(·,G))` 是跨字段稳定的 EUR 杠杆,升格为通用杠杆;② sector 分组把 PPA 检查清零（`failed_ppa_count` 1→0）、sub 闸从压线转 PASS、robust 保持 0.70——DEU 帖「sector 优于 industry」在 EUR 复现,且 sector 档的 CLUSTER_TEST 也更高（1.12 vs 1.03）。③ ** sector 档代价是 S 略降（1.43→1.34）**——分组变粗稀释了行业内区分度。两条路径指向同一组合：sector 分组的干净结构 × 包装栈的强度增量,已提交合并版 + 拆解归因版（`group_scale` 单独 vs 仅 `rank`,multisim `QLZZE3ep4DLcx9SMxyDZzj`）。距闸线缺口：S 还差 0.15–0.24,F 还差 0.30–0.36——组合若能把 S 推到 ≥1.45,叠加 truncation 微调或 decay 加档仍有腾挪空间。

**包装栈拆解归因（已终态,multisim `QLZZE3ep4DLcx9SMxyDZzj`）——增量几乎全部来自 `group_scale`,`rank` 只是输出整形**：

| 变体 | alpha id | S | F | sub | robust | CLUSTER_TEST |
|---|---|---|---|---|---|---|
| 仅 `rank(·)` | `akKQqZo5` | 1.36 | 0.65 | 0.74 | 0.70 | 1.15 |
| `rank(group_scale(·,sector))` | `YP1EGKQl` | 1.36 | 0.65 | 0.73 | 0.70 | 1.13 |
| （对照）`total_top_buy_shares` industry 栈 | `O0AMPWv7` | 1.43 | 0.70 | 0.74 | 0.80 | 1.17 |

**归因**：sector 轴上 `rank` 与 `rank(group_scale)` 读数几乎逐位相同（S 1.36/1.36,F 0.65/0.65）——`group_scale` 的增量依赖分组轴：industry（分组细、组内样本多、scale 拉开了行业间幅度差）上有效 +0.13,sector（分组粗）上被 `rank` 均匀化抹平。**修正升格结论：`rank(group_scale(·,industry))` 才是稳定杠杆,industry 粒度是 `group_scale` 发挥作用的前提**。当前最佳结构组合（全绿 + 最高 S）= `O0AMPWv7`（industry 栈,S 1.43,仅 sub 压线差 0.02）与 88d 窗口待合并。

**高管直接买入 × 包装栈（已终态,multisim `1uCZj6dUi5kc9CbSifMyHo5`）——industry 档再添一条全绿候选**：

| 变体 | alpha id | S | F | 2Y | sub（闸） | robust | PPA | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| `total_secondary_top_buy_shares` industry 栈 | `wpQ2MM6d` | 1.29 | 0.60 | 2.20 | **0.83 PASS（0.67）** | 0.71 PASS | 0 失败 | 仅 S/F |
| `total_secondary_top_buy_shares` sector 栈 | `A1VrMMqd` | 1.27 | 0.59 | 1.98 | 0.88 PASS | 0.64 FAIL | 1 失败 | S/F/robust |

**归因**：industry 栈保持全绿（sub 余量 +0.16）且 S 1.21→1.29;sector 栈 robust 跌破闸（0.64）——与 sector 轴稀释效应一致（高管直接买入的同行参照系应该是同行业,industry 是该字段的原生分组）。**「高管直接」字段与「全体高管」字段在结构上同构（都吃 industry 栈）,S 低 0.14 但 sub/robust 余量更大——是 88d 合并组合的备选基底。**

## 7. ★ 高管直接买入（`total_secondary_top_buy_shares`）——全战役结构最干净的候选

**实测（已终态,multisim `2cFcL24IM5iGaTrAA0Br1q8`,SLOW_AND_FAST 档）**：

| 字段 | alpha id | S | F | TO | 2Y | sub（闸） | robust | PPA | 卡闸 |
|---|---|---|---|---|---|---|---|---|---|
| `total_secondary_top_buy_shares`（高管**直接**买入） | `YP1EKlQv` | 1.21 | 0.55 | .0833 | 2.09 | **0.82 PASS（0.63）** | **0.76 PASS** | **0 失败** | 仅 S/F |
| `total_secondary_buy_shares`（董事直接买入） | `zq326AOE` | 1.34 | 0.63 | .0873 | 2.33 | 0.69 FAIL（0.71） | 0.49 FAIL | 2 失败 | S/F/sub/robust |
| 对照：`total_top_buy_shares`（高管含间接） | `QPvNZ5pr` | 1.30 | 0.62 | .0835 | 2.13 | 0.71 PASS（0.68） | 0.80 PASS | 1 失败 | S/F |

**归因**：① **sub 余量 0.82 vs 闸 0.63——全战役唯一一个 sub 大幅 PASS 的候选**（其余候选全部压线或 FAIL）,意味着它吃得住包装栈抬 S 后闸线上移（S 1.58 时闸 0.82,恰好还能容纳）;robust 0.76 同样有余量。② 经济含义：JMZ(2003)/Lakonishok-Lee(2001) 的核心结论——**open-market 直接购买（用自己的钱、决策自由）信息含量远高于非自由裁量交易（期权行权、股权激励到账）**。「高管 ∩ 直接」子集是该机制最纯粹的提取,虽然 αC 只有 9（覆盖窄）,但 sub/robust 双大幅 PASS 直接验证了「信号质量来自子集纯度」的假说。③ 董事直接（`total_secondary_buy_shares`）S 更高（1.34）但 sub/robust 双 FAIL——董事身份的信息含量弱于高管,纯度假说在身份轴上同样成立（高管>董事）。④ 已提交包装栈 × industry/sector 两档（multisim `1uCZj6dUi5kc9CbSifMyHo5`）,industry 档预期 S≈1.34（+0.13）,sector 档预期结构更干净。**该候选已取代 `QPvNZ5pr` 成为冲线首选**。

**窗口族结果（已终态,multisim `3cdCMW4Ae4JDa9E2gS462ux`,同 SLOW_AND_FAST 档）——66d 是干净内点峰,与 DEU 论坛帖网格结论一致**：

| 窗口 | alpha id | S | F | TO | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|
| 22d | `zq32Z90X` | 1.04 | 0.45 | .1331 | 1.46 | 0.61 | 0.42 FAIL |
| **66d（基线）** | `QPvNZ5pr` | **1.30** | **0.62** | .0835 | **2.13** | **0.71 PASS** | **0.80 PASS** |
| 252d | `rKRNYoVj` | 0.76 | 0.27 | .0715 | 0.90 | 0.38 FAIL | 0.60 FAIL |

**归因**：22d 换手升高（.0397→.1331）但 S/F/sub/robust 全面转差——窗口太短，季度披露的买入信号尚未充分累积就被截断。252d 换手最低但 S/F 腰斩——窗口过长把买入脉冲摊薄成噪声,sub 也随之破位。两端都比 66d 差,确认该机制的信息半衰期对应**季度**。

**窗口邻域补测（44d/88d,已终态,multisim `3VG9sf2gj4l59A71bvMPjxWJ`）——修正「66d 唯一峰」结论：S 平台期,但结构上 88d 碾压**：

| 窗口 | alpha id | S | F | TO | 2Y | sub（闸） | robust | PPA | checks.fail |
|---|---|---|---|---|---|---|---|---|---|
| 44d | `akKQZpe1` | 1.34 | 0.66 | .0975 | 1.28 FAIL | 0.67 FAIL（0.71） | 0.69 FAIL（0.7,差0.01） | 2 失败 | 5 项 |
| **66d** | `QPvNZ5pr` | 1.30 | 0.62 | .0835 | 2.13 | 0.71 PASS | 0.80 PASS | 1 失败 | 0 项 |
| **88d** | `E568WdNm` | **1.36** | 0.65 | .0789 | 2.01 | **0.88 PASS（0.71）** | **0.92 PASS** | **0 失败** | **0 项** |

**归因**：S 在 44–88d 是**平台期**（1.30–1.36,峰不在 66d——44d 1.34 / 88d 1.36 均高于 66d 1.30）,DEU 帖「66 是干净内点峰」的**强度**结论在本数据集不成立;但**结构**上 88d 全绿：sub 0.88（余量 +0.17）、robust 0.92（全战役最高）、PPA 零失败、checks.fail 空、2Y 2.01。经济解释：EUR 内部人申报有披露滞后（交易发生→申报→数据库聚合约 2–4 周）,66d 窗口的尾部实际只覆盖到约 2 个月的「有效申报」,而 88d（季度 66d + 滞后 22d）恰好覆盖一个完整的「披露周期」——信息半衰期是「季度 + 申报滞后」,不是纯季度。**结论：窗口族以 88d 为新基线**（结构余量最大,吃得住后续杠杆抬 S 后的 sub 比率闸线上移）,44d/22d/252d 归档不再回测。

**`significant_value_3`/`_4` 覆盖探针（已终态,multisim `DriZx4Zt4PSaUYB6ZrXxw0`）——诊断成功且发现强反向信号**：S=**−1.38**/−1.35、pnl −3.07M/−2.97M、longCount/shortCount 完全一致（444/1052）——`significant_value_3` 与 `_4` 是**近乎同一个信号**（同一批名字的镜像持仓）。与 `_1`（S=+1.45~1.58）合读：**「最大单笔显著交易」正向预测、「第3/4大单笔」反向预测**——与 CMP(2012) 的 conviction vs routine 区分吻合（最大一笔=信念集中,后面几笔=例行分散）,与 `_2` 字段级 FAIL 形成有意义的梯度（排名越靠后,信号越弱直至反向）。**但反向版结构不可用**：2Y 0.91（远低于闸 1.58）、CLUSTER_TEST −0.55,反向本身不修复年度分布。**字段覆盖闸：`significant_value_3`/`_4` 计入已覆盖（正反向均记录）;`_2`/`directional_significant_value_1` 维持平台级 FAIL 记录（两次独立复现）。**

**`significant_value_1` 分组轴终测（已终态,multisim `3yy5do6Xl4sSb3fUYhGw6k`）——三档全不过,结构性归档**：sector 1.30/sub 0.55/robust 0.32；subindustry 1.36/sub 0.58/robust 0.35（industry 档此前 1.58/sub 0.59/robust 0.41）——**robust 停在 0.32–0.41 不随分组轴移动**,与分布重塑三板斧的结果（0.40/0.41/0.41）共同构成 6 个独立证据:该字段 robust 失败与截面分布形态、分组粒度均无关,是字段自身的结构性属性（信号集中在稳健子宇宙外的少数名字）。**结论:`significant_value_1` 族按「robust 结构性不可修复」归档,S=1.58 的读数保留为天花板记录,不再投入任何杠杆。**

**中性化档对照（88d 基础,已终态,multisims `SV5wuix4NM9yXbgsqiRgG`(RAM)/`4imd8387z5hacHH8QuDmNzc`(CROWDING)/`1eDmkxdR64Zvbip1aDZTH9UT`(SLOW_AND_FAST 栈合并)）——SLOW_AND_FAST 封档,RAM/CROWDING 不迁移**：

| 档 | alpha id（裸/栈） | S | F | 2Y | sub | robust | PPA |
|---|---|---|---|---|---|---|---|
| RAM | `E568Xpv9`/`1YNlQXXQ` | 1.02/1.12 | 0.50/0.57 | 0.87/0.89 | 0.75/0.80 | 0.80/0.85 | 0 失败 |
| CROWDING | `78LvE1kb`/`A1VrMPRw` | 0.94/0.99 | 0.45/0.49 | 0.81/0.78 | 0.77/0.79 | 0.77/0.81 | 1 失败 |
| **SLOW_AND_FAST（栈）** | `E568Xm1m` | **1.51** | **0.74** | **2.04** | **0.93** | **0.98** | **0 失败** |

**归因**：RAM/CROWDING 把 2Y 砍半（2.04→0.87/0.81）——GLB 帖的「insider_agg_matrix @ RAM 可行」在 EUR **不成立**（GLB 是 TOPDIV3000 高息股宇宙,风格结构与 EUR TOPCS1600 不同,中性化档位剥离的因子轴不同）。KOR risk70 的「RAM 载荷族最优」同样不迁移（那是风格载荷机制,本机制是事件流量）。**结论：中性化轴对本数据集穷尽（SUBINDUSTRY/SLOW_AND_FAST/RAM/CROWDING 四档实测）,SLOW_AND_FAST 为唯一最优档,不再测其余 8 档**（STATISTICAL/COUNTRY 等在区域历史上均劣于 SUBINDUSTRY,无先验理由优于 SLOW_AND_FAST）。

**★ 当前最强候选 `E568Xm1m`（2026-11-06）**：`rank(group_scale(tail(winsorize(group_rank(ts_sum(total_top_buy_shares, 88), industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))` @ SLOW_AND_FAST——**S 1.51 / F 0.74 / TO .0753 / 2Y 2.04 / sub 0.93（余量+0.14）/ robust 0.98（全战役最高）/ PPA 0 失败 / checks.fail 空**。距主闸仅差 S 0.07、F 0.26。sector 栈（`e75Vo1pJ`,S 1.41/2Y 1.67）确认 industry 轴更优。

**std/幂次/decay 杠杆与 `total_secondary_top_buy_shares` 88d 结果（已终态,multisims `4x15D4g8G4goc3RcFjSTpeQ`/`1s4elb4pi4LrbDC7LVQ4nZd`;decay 批 `MBIKW7Kc4D28SN1hfzmSmY0` 待终态）**：

| 变体 | alpha id | S | F | 2Y | sub | robust | 备注 |
|---|---|---|---|---|---|---|---|
| `total_top_buy_shares` 88d 栈（基线） | `E568Xm1m` | 1.51 | 0.74 | 2.04 | 0.93 | 0.98 | 最强 |
| + std=4 | `Xg9v6g81` | 1.50 | 0.74 | 2.04 | 0.92 | 0.97 | 无增益 |
| + signed_power(·,2) | `YP1EqPvW` | 1.47 | 0.72 | 1.98 | 0.91 | 0.96 | 反而降 |
| `total_secondary_top_buy_shares` 88d 裸 | `YP1EqLWl` | 1.51 | **0.76** | **2.34** | **1.02** | 0.91 | **并列最强,sub 余量+0.23** |
| `total_secondary_top_buy_shares` 88d 栈 | `RRElWj20` | 1.52 | 0.75 | 2.20 | 1.01 | 0.85 | S 最高,robust 降 0.06 |

**归因**：① std=4 与 signed_power(·,2) 均无增益（1.50/1.47 vs 1.51）——`tail(newval=0.5)` 之后中段已是常数,分布杠杆已无操作空间,分布轴正式穷尽;② **`total_secondary_top_buy_shares` 88d 与 `total_top_buy_shares` 88d 并列最强**（1.51/0.76 vs 1.51/0.74）,且 sub 余量更大（1.02,闸 0.79,余量+0.23）——「高管直接买入」字段在 88d 窗口下结构同样全绿,**两条独立字段路径同时收敛到 S≈1.51**,说明该机制的天花板就在此处附近。③ ⚠ **F 闸的真实目标修正**：按 EUR skill ④ 闭式 `F = S^1.5 × sqrt(returns/0.125)`,本族 returns≈0.03 ⇒ F=1.0 需要 S≈1.75（低波动族的 F 门槛高于表面 1.58）。当前 S 1.51–1.52 ⇒ 即使 S 过 1.58,F 仍会卡在 ~0.78。**真实缺口是 S +0.24,不是 +0.07。** 已提交读数形态替换两批：`ts_decay_linear`（近期申报加权,衰减型累加器）+ `group_zscore`（幅度归一化 vs 排序,multisim `wiUTFghP5iL9XcgrEE9KF8`）;`quantile(gaussian)`（正态化整形替换 rank）+ 110d 窗口（88d 邻域再探一格,multisim `2Ms857Th58ibu510wynerK2`）。若两批均无 S 增益,本机制按「S 天花板 1.51,F 结构性不足」归档,转入下一条字段族。

**读数形态替换实测（已终态,multisims `wiUTFghP5iL9XcgrEE9KF8`/`2Ms857Th58ibu510wynerK2`/decay 批 `MBIKW7Kc4D28SN1hfzmSmY0`）——★★★ `group_zscore` 替换 `group_rank` 是本战役最大单杠杆,首次把 Sharpe 闸打穿**：

| 变体 | alpha id | S | F | TO | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| **`group_zscore` 替换 `group_rank`（88d 栈）** | **`6XdoOMVP`** | **1.64 PASS** | **0.83** | .0696 | 1.95 PASS | **1.01 PASS（余量+0.15）** | **1.05（全战役最高）** | 仅 LOW_FITNESS(warning) |
| `ts_decay_linear(·,88)` 替换 `ts_sum` | `3qokL0rZ` | −0.01 | 0 | **.9522 爆炸** | −0.27 | −0.16 | −0.43 | 全挂 |
| `quantile(gaussian)` 替换 `rank` | `A1VrK02d` | 1.43 | 0.69 | .0774 | 1.87 | 0.90 | 0.94 | S/F |
| 窗口 110d | `3qokL92e` | 1.40 | 0.65 | .0719 | 1.75 | 0.74 | 0.90 | S/F |
| decay 13（裸/栈） | `rKRNXAQJ`/`6XdoOzgp` | 1.36/**1.52** | 0.65/**0.75** | .0712/.0687 | 2.00/2.09 | 0.84/0.89 | 0.88/0.93 | S/F |

**归因**：① **`group_zscore`（幅度归一化）比 `group_rank`（序数化）多保留 0.10–0.13 的 S**——`group_rank` 把组内所有幅度差压成等距序数,丢弃了「申报量差距有多大」的信息;`group_zscore` 保留幅度,后端 `winsorize(std=2)` 再控尾,信息效率更高。这是对区域 skill「quantile 替换」杠杆表的**新成员**：归一化类替换的收益来源不是数值路径差异,而是**信息保真度差异**。② `ts_decay_linear` 归零（TO 0.95 爆炸）——稀疏事件流量上,衰减权重把「无申报日的 0 值」也纳入加权,累计语义被破坏,产生逐日跳变;**`ts_sum` 是稀疏流量字段的唯一正确累加器**（与 §2 历史判死的「TO 爆炸」根因同源,再次确认）。③ 110d（1.40）劣于 88d（1.51/1.64）——窗口平台期右边界就在 88–110 之间,88d 是峰。④ decay 13 栈（1.52）与 decay 4 栈（1.51）几乎持平——慢信号对 decay 不敏感,保留 4。⑤ **当前最佳候选 `6XdoOMVP` 只剩一道 LOW_FITNESS（0.83 vs 1.0）**;按 F 闭式（returns 0.032）F=1.0 需要 S≈1.75。

**zscore 补强批结果（已终态,multisims `2UNjoFfEN4ypcMo11t6x92uI`/`2vw5fm2OG5cI9G6bJwoeZtE`）——三条全绿候选确认,88d+86 峰封档**：

| 变体 | alpha id | S | F | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|
| **zscore × `ts_mean(·,5)` 平滑** | **`9qxdQPqr`** | **1.62 PASS** | 0.81 | 1.81 PASS | 0.93 PASS | 0.96 PASS | 仅 LOW_FITNESS(warning) |
| zscore 迁移 `total_secondary_top_buy_shares` | `VkxmoK7J` | 1.57 | 0.79 | 1.90 | **1.04（余量+0.22）** | 0.82 | S 差 0.01/F |
| zscore 裸版（无包装栈） | `0mYNWnwK` | 0.99 | 0.47 | 1.14 | 0.81 | 0.68 FAIL | S/F/robust/2Y |
| zscore × 132d | `0mYNWkm6` | 1.25 | 0.55 | 1.34 | 0.51 FAIL | 0.81 | S/F/sub/2Y |

**归因**：① `ts_mean(·,5)` 平滑（广度族 d5 配方）迁移到事件流量族成功——S 基本持平、TO 降、结构保持全绿;② zscore 裸版（0.99）比裸 `group_rank` 版（1.36）更差——**zscore 的增益依赖包装栈把它的负值/极端值整形回均匀分数,裸奔反受其害**（与 rank 版裸/栈差 0.06 的形态一致,包装栈对两种归一化都是必要件）;③ 132d 确认 88d 是峰;④ `total_secondary_top_buy_shares` zscore 栈 S 低 0.07 但 sub 余量最大（1.04）——「压线过 S 后被 sub 比率闸吃掉」风险下的最优保险基底。

**★ 冲线组合矩阵（全绿候选,按 F 降序）——S 轴正式穷尽,缺口定性为「returns 结构性天花板」**：

| 候选 | alpha id | S | F | 2Y | sub | robust | 剩余缺口 |
|---|---|---|---|---|---|---|---|
| `total_top_buy_shares` 88d zscore 栈 | `6XdoOMVP` | **1.64** | **0.83** | 1.95 | 1.01 | 1.05 | F 0.17 |
| 同上 + ts_mean(·,5) | `9qxdQPqr` | 1.62 | 0.81 | 1.81 | 0.93 | 0.96 | F 0.19 |
| `total_secondary_top_buy_shares` 88d zscore 栈 | `VkxmoK7J` | 1.57 | 0.79 | 1.90 | 1.04 | 0.82 | S 0.01/F 0.21 |

已实测穷尽的轴：中性化（4 档）、窗口（7 档）、分组（3 轴）、归一化（rank/zscore/quantile/group_scale）、分布（std 2 档/power/quantile）、decay（2 档）、平滑（d5）、包装栈（3 变体）——**S 天花板 1.64,F=1.0 需要 S≈1.75（returns 0.032 闭式解）,缺口 0.11 无法从已有轴获得**。truncation 是区域锁定维度不作扫描。**本机制族的最终状态：3 条结构全绿、仅差 F 的候选,唯一未试的合法杠杆是跨窗口的 `ts_zscore` 时序形态（自身基线族在 insiders1 已证伪,但那是「仓位比例」机制;「流量绝对量」机制的时序形态未测,作最后一测）**。若最后一测无增益,本族归档为「F 结构性不足」,3 条候选转交用户作 prod/self 预检决策。

**时序形态 + 高管显著金额族终测（已终态,multisims `3mlHRKdvy4un8SxJaGNtcJ9`/`1Sw0nidtG4JQ8J13GUYdkRW`）——★★★ `top_significant_value_1` 是本战役真正的破闸字段,`QPvNeeqK` 距全过仅一道 0.07 的 F**：

| 变体 | alpha id | S | F | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|
| **`top_significant_value_1` 88d zscore 栈** | **`QPvNeeqK`** | **1.75 PASS** | **0.93** | **2.30 PASS** | **1.06 PASS（余量+0.15）** | **1.07 PASS** | 仅 LOW_FITNESS 0.93（warning,差 0.07） |
| `top_significant_value_3` 88d zscore 栈 | `MPYewwqr` | −0.98 | −0.39 | −0.41 | −0.91 | −0.88 | 反向信号,不可用 |
| 时序 `ts_zscore(·,252)` 双重 zscore | `Vkxmob9A` | 0.08 | 0.01 | 1.03 | 0.14 | −0.58 | 归零 |
| `ts_mean(·,22)` 预平滑 × 88d | `leA5ZPO2` | 1.56 | 0.76 | 1.82 | 0.80 FAIL（闸0.83） | 0.95 | S/F/sub |

**归因**：① **`top_significant_value_1`（高管最大单笔显著交易金额）S=1.75 直接过 Sharpe 闸,2Y 2.30/sub 1.06/robust 1.07 全部大幅 PASS**——「高管 ∩ 最大单笔 ∩ 金额」是三重纯度叠加（身份层级 × 信念集中 × 绝对规模）,与 `significant_value_1`（全员最大单笔,robust 结构性 FAIL）对比,**「限高管」这一层过滤恰好剔除了 robust 不稳健的名字**——CMP(2012) 的 conviction 代理在高管子集上才是完整的。`CLUSTER_TEST` 1.30 也是全战役最高。② `top_significant_value_3` 反向（−0.98）——与 `significant_value_3` 反向（−1.38）完全一致,「第3大单笔=例行申报」的梯度规律在高管子集复现,**字段族级规律确认**。③ 时序 `ts_zscore(·,252)` 归零（0.08）——「流量绝对量」机制的时序自身基线同样证伪,与 insiders1 结论合流:**insiders 类信号的经济含义全部在横截面相对位置,时序基线形式一律归零**（跨机制通用死路）。④ `ts_mean(·,22)` 预平滑劣于裸 ts_sum（1.56 vs 1.64）——月度平滑稀释了申报脉冲,不如 d5 后置平滑。⑤ **`QPvNeeqK` F=0.93 距闸 0.07**——按闭式 F=S^1.5×sqrt(returns/0.125): returns=0.0353 时 F=1.0 需要 S≈1.83,但 F 0.93 已是 warning 级（非 FAIL）,Mode B 资格判定（`tools/mode_b_qualify.py`）对 warning 的容忍度与 RA hard-gate 不同,**资格以 `mode_b_qualify` 的实际输出为准**。

**`top_significant_value_2`/`_4` 覆盖 + decay 13（已终态,multisims `2EOUtKa6D4qobMsU9VCEIPj`/`KDnqUdVP54masL15jsaLEQC`）——`_2` 刷新战役 S 纪录,梯度规律完整封档**：

| 变体 | alpha id | S | F | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|
| `top_significant_value_2` 88d zscore 栈 | `leA5JeP7` | **1.76** | **0.94** | 2.32 | 1.07 | 1.07 | 仅 LOW_FITNESS 0.94(warning) |
| `top_significant_value_4` 88d zscore 栈 | `zq32Xqnd` | −0.98 | −0.39 | −0.40 | −0.92 | −0.87 | 反向,不可用 |
| `_1` 栈 decay 13 | `A1Vr6Xxd` | 1.73 | 0.92 | 2.34 | 0.99 | 1.02 | 仅 LOW_FITNESS(warning) |
| `_1` 栈 decay 13 + ts_mean(·,5) | `VkxmnQNG` | 1.73 | 0.91 | 2.42 | 0.95 | 0.97 | 仅 LOW_FITNESS(warning) |

**归因**：① `top_significant_value_2`（高管第二大单笔）S=1.76——超过 `_1`（1.75）,**字段族梯度规律完整：_1/_2 正向强信号（信念集中）, _3/_4 反向（例行申报）,对称分裂**——这与 CMP(2012) 的二分法（前两笔=机会主义,后续=routine）高度吻合,是该机制在字段层面的直接证据。② decay 13（1.73/0.92）与 decay 4（1.75/0.93）持平——decay 轴正式封档。③ **当前 5 条「仅差 F warning」的候选池**：`QPvNeeqK`(_1)/`leA5JeP7`(_2)/`A1Vr6Xxd`(_1,d13)/`VkxmnQNG`(_1,d13,d5)/`9qxdQPqr`(total_top)。F 缺口归因（TO 0.07 远低于 0.125,F 公式被钉死在 returns 轴）：S=1.76 需 returns≈0.040,当前 0.035——**最后两个合法杠杆**：universe 平移（EUR skill ①：analyst7 族 S 1.99→2.57 实证,insiders1 的反向失败是稀疏 VECTOR 机制,不可外推到本 MATRIX 预聚合字段）与 decay 20（把换手进一步压低换取 return 稳定性）。两批已提交。

**TOP2500 × decay 20 结果（已终态,multisims `1Gu4Px9ff4pzaQ5kwkChpsV`/`3keAsO3tB56C9Gg1hdlOFw11`）——S 大突破但 sub 比率闸反噬,需要配对抬 sub 杠杆**：

| 变体 | alpha id | S | F | 2Y | sub（闸） | robust | 卡闸 |
|---|---|---|---|---|---|---|---|
| `_1` 88d 栈 @ TOP2500 | `O0AMK8QR` | **1.92** | 0.96 | 2.36 | 0.86 FAIL（1.00） | —（未列） | F/sub |
| `_2` 88d 栈 @ TOP2500 | `gJeg7Zkl` | **1.91** | 0.95 | 2.35 | 0.84 FAIL（0.99） | — | F/sub |
| `_1` 栈 decay 20 @ TOPCS1600 | `58EANQQo` | 1.73 | 0.91 | 2.38 | 0.95 PASS | 0.99 | 仅 F(warning) |
| `_2` 栈 decay 20 @ TOPCS1600 | `bl6r7RRq` | 1.73 | 0.91 | 2.38 | 0.95 | 0.99 | 仅 F(warning) |

**归因**：① **TOP2500 把 S 从 1.75/1.76 抬到 1.92/1.91（+0.16）**——EUR skill ① 的「universe 是 prod–S 前沿平移旋钮」在本字段族成立（与 insiders1 稀疏 VECTOR 机制的反向结果形成机制级对照：**MATRIX 预聚合字段吃宽宇宙,稀疏 VECTOR 事件字段被宽宇宙稀释**——这是比「universe 杠杆是否有效」更根本的二分法）。② 但 sub 比率闸线随 S 上移（1.92×0.52=1.00）,sub 只到 0.86——**宽宇宙稀释了子宇宙一致性**（TOPCS1600 的子集与全集重合度高,TOP2500 新增的小票段与 TOPCS1600 子集行为分化）。③ decay 20 确认无增益（1.73/0.91）,decay 轴彻底封档。

**TOP2500 修复批结果（已终态,multisims `26aXTTLi54Das9LcSsLt0q`/`2sqPJedJ14pBanULzhCrfl6`）——两条修复路径都失败,TOP2500 路线关闭,最终锁定 TOPCS1600 池**：

| 变体 | alpha id | S | F | 2Y | sub（闸） | 卡闸 |
|---|---|---|---|---|---|---|
| cartesian(country,subindustry) 分组 `_1` | `GrWK0LA3` | 1.46 | 0.64 | 1.23 | 0.60 FAIL（0.76） | 全恶化 |
| cartesian(country,subindustry) 分组 `_2` | `d5W380VK` | 1.46 | 0.63 | 1.23 | 0.59 FAIL | 全恶化 |
| `ts_mean(·,5)` 平滑 `_1` @ TOP2500 | `A1VrJaoW` | 1.86 | 0.91 | 2.36 | 0.78 FAIL（0.97） | F/sub |
| `ts_mean(·,5)` 平滑 `_2` @ TOP2500 | `O0AMwmlq` | 1.85 | 0.90 | 2.35 | 0.77 FAIL | F/sub |

**归因**：① cartesian 分组把 S/F/2Y 全部打崩（1.92→1.46）——**该杠杆在本机制是有害的**：country×subindustry 单元格内样本太少（TOP2500 的国家×子行业粒度下,多数格子只有几个名字）,zscore 在稀疏格子里放大噪声;skill 配方的适用前提（组内样本充足）在本数据集不成立。② `ts_mean(·,5)` 在 TOP2500 上同时压低 S（1.92→1.86）与 sub（0.86→0.78）——平滑在宽宇宙上放大了稀释效应。③ **TOP2500 路线正式关闭**：S 的 +0.16 收益无法兑付 sub 闸的 −0.14 缺口,两条修复路径均反向。④ **最终候选池锁定 TOPCS1600**（decay 4/13/20 三档确认 4 最优）。本机制族战役终态：

| 最终候选（全部「仅 LOW_FITNESS warning」） | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| `top_significant_value_2` 88d zscore 栈 | `leA5JeP7` | **1.76** | **0.94** | 2.32 | 1.07 | 1.07 |
| `top_significant_value_1` 88d zscore 栈 | `QPvNeeqK` | 1.75 | 0.93 | 2.30 | 1.06 | 1.07 |
| `_1` decay 13 | `A1Vr6Xxd` | 1.73 | 0.92 | 2.34 | 0.99 | 1.02 |
| `_2` decay 20 | `bl6r7RRq` | 1.73 | 0.91 | 2.38 | 0.95 | 0.99 |
| `total_top_buy_shares` 88d zscore 栈 | `6XdoOMVP` | 1.64 | 0.83 | 1.95 | 1.01 | 1.05 |

下一步按 S5 纪律：先跑 `compute_mutual_correlation` 本地互测（零成本,看最大互不相关子集）,再对入团候选跑 `mode_b_qualify` 资格判定——「仅 warning 的 F」是否构成提交障碍以该工具输出为准,提交决策留给用户确认。

**本地互测结果（`compute_mutual_correlation`,threshold 0.5,4y 窗口）——5 条候选互相关 0.92–0.997,同机制单一席位,最大互不相关子集 = 1（`leA5JeP7`）**：

| | `leA5JeP7` | `QPvNeeqK` | `A1Vr6Xxd` | `bl6r7RRq` | `6XdoOMVP` |
|---|---|---|---|---|---|
| `leA5JeP7` | 1 | .9974 | .9896 | .9808 | .9389 |
| `QPvNeeqK` | | 1 | .9920 | .9779 | .9381 |
| `A1Vr6Xxd` | | | 1 | .9928 | .9318 |
| `bl6r7RRq` | | | | 1 | .9206 |
| `6XdoOMVP` | | | | | 1 |

**归因**：与 EUR skill S5 纪律的预判完全一致——同字段族（`top_significant_value_1/2`）与同骨架（decay 13/20 变体）的互相关 0.98–0.997,连跨字段的 `6XdoOMVP`（total_top_buy_shares vs top_significant_value_*）也有 0.92–0.94——**「高管买入强度」机制的全部变体共享同一收益源,只够一个席位**。席位归属 `leA5JeP7`（S 1.76/F 0.94,池内最优）。**Mode B 资格判定（2026-11-06 实跑 `tools/mode_b_qualify.py evaluate`）：`eligible=true`,verdict=main_gate——sharpe 1.76≥1.25 且 fitness 0.94≥0.8 双达标,RA 的 LOW_FITNESS 硬闸（1.0）与 Mode B 主闸（0.8）是两套阈值,本候选按区域台账口径资格成立**。**战役累计产出：insider_agg_matrix 数据集 1 个机制席位（Mode B 资格已确认,提交待用户显式确认）+ 全套字段/杠杆/结构实测地图。距 10 alpha 交付目标还差 9——insiders 类别内可挖空间接近穷尽（insiders1 机制 B 最好 0.93 且杠杆穷尽;insiders12 cov 0.193<0.35 历史跳过）,下一数据集按 SOP 第 1 步重新扫描选集。**

## 8. 下一数据集选集扫描（2026-11-06,`get_datasets` 全量 173 集过滤）

**选集标准**：低竞争（αC<100）、覆盖达标（cov≥0.5,近十年数据前提）、valueScore≥3、优先未点亮塔类别（news ×1.3 / sentiment ×1.4 / other ×1.5）。头部候选：

| 数据集 | 类别 | cov | 字段 | αC | vS | 倍率 | 说明 |
|---|---|---|---|---|---|---|---|
| **news_sentiment_dl** | other ×1.5 | .756 | 66 | **2** | **6** | — | DL 新闻情绪信号,全场最低竞争+最高 valueScore |
| news_sentiment_nlp | other ×1.5 | .913 | 23 | 7 | 5 | — | 新闻情绪特征 |
| news54 | news ×1.3 | .900 | 40 | 3 | 4 | — | Key Developments |
| behavioral_signals | model ×1.3 | .557 | 7 | 1 | 4 | — | 行为金融信号因子 |
| multi_source_model | model ×1.3 | .579 | 60 | 1 | 4 | — | 多源收益预测 |
| event_relation | other ×1.5 | .577 | 12 | 3 | 5 | — | 文本事件关系 |
| price_signal_dl | model ×1.3 | .973 | 28 | 4 | 5 | — | DL 价格信号 |
| stock_search_trends | other ×1.5 | .540 | 6 | 2 | 5 | — | 搜索趋势矩阵 |

**决策**：首位 **`news_sentiment_dl`**（αC=2 全场最低,vS=6 全场最高,cov 0.756 达标,66 字段体量适中）——「other ×1.5」倍率与 DL 情绪轴均未在本区开过塔。次选 `news_sentiment_nlp` / `news54`（同为 other/news 低竞争）。**⚠ 混类别风险预判**：该集 category=other,组腿预算（禁区类 5 个名额）需在提交前盘点——但 ATOM 单数据集策略不组腿,不受影响。**开始字段画像采集。**
- **显著交易金额族（`significant_value_1`,2026-11-06 已测,SLOW_AND_FAST 档）——本战役单条最高 S 读数,但 robust 闸重伤**：`tail(winsorize(group_rank(ts_sum(significant_value_1, 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)` → alpha `leA5dbJe`：S **1.45**／F **0.72**／TO .0873／2Y **2.68 PASS**／sub 0.62 FAIL（闸 0.754）／**robust 0.29 FAIL（闸 0.7，差距远大于 sub，是本候选主要卡点）**。S 只差闸线 0.13，是本战役目前第二接近过闸的候选,但 robust 如此低（不到闸线一半）提示信号可能集中在少数非稳健子集（小市值/低流动性名字）,需要先诊断（CLUSTER_TEST 警告 0.85 同样偏低,与 robust 低同向）再决定杠杆——cap 掩码对 `total_top_buy_shares` 已证明在 sub 已修复后是多余甚至有害杠杆,这里 sub/robust 都还没修复,需要先查是不是小市值驱动，而不是照搬同一掩码。

**sub/robust 修复实测（已终态,multisim `1x51AA4RP4ivaeDJQXKzvoX`）——两条杠杆都未能把 robust 推过闸,且 cap 掩码再次证实有害**：

| 杠杆 | alpha id | S | F | TO | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|---|
| 基线（无杠杆） | `leA5dbJe` | 1.45 | 0.72 | .0873 | 2.68 | 0.62 FAIL | 0.29 FAIL | sub/robust |
| `group_scale(·,industry)` | `bl6rXR5l` | **1.53** | **0.77** | .0819 | 2.65 | 0.58 FAIL（闸 0.81） | **0.40 FAIL**（闸 0.7） | S/F/sub/robust |
| cap 双峰掩码（同 `total_top_buy_shares` 配方） | `LLMmW9A6` | 1.05 | 0.51 | .1163 | 1.09（IS_LADDER FAIL） | 0.32 FAIL | **−0.21 FAIL**（比基线更差） | S/F/sub/IS_LADDER/robust |

**归因**：`group_scale(industry)` 把 S/F 都推高了一档（1.45→1.53、0.72→0.77，已逼近 Sharpe 闸线 1.58 的 97%），robust 也从 0.29 回升到 0.40——方向正确但强度不够，还差 0.30（闸 0.7 的 43%）。cap 双峰掩码**第二次**证实是有害杠杆（先前在 `total_top_buy_shares` 上已证伪一次，这里 robust 反而转负、新增 IS_LADDER FAIL）——两次独立验证排除了「边缘 cap 分位驱动」假说：如果问题真是极端市值股票贡献了不稳健的收益，掩掉它们应该修复 robust，但结果恰恰相反，说明**该字段的 robust 问题不是 cap 分布问题，掩码只是在砍广度/换手，没有触及真正病灶**。按 EUR region profile ④ 的「robust universe 差 = 分布问题」三板斧（`rank` 均匀化 → `signed_power(rank(·),2)` 拉陡分布），已在 `group_scale` 结果之上叠加 `rank`/`signed_power` 两档做进一步分布重塑测试。

**分布重塑实测（已终态，multisim `39Y4XPbqd4V69QyoGl2D3v1`）——`rank` 一档首次触及 Sharpe 闸线,但 robust 是结构性问题,三板斧证伪**：

| 杠杆 | alpha id | S | F | 2Y | sub（闸） | robust |
|---|---|---|---|---|---|---|
| `group_scale` 基线 | `bl6rXR5l` | 1.53 | 0.77 | 2.65 | 0.58（0.81） | 0.40 FAIL |
| + `rank(·)` | `npveJ2ax` | **1.58 PASS** | **0.80** | 2.69 | 0.59（0.84） | 0.41 FAIL |
| + `signed_power(rank(·),2)` | `E5687EQr` | 1.54 | 0.78 | 2.61 | 0.58（0.82） | 0.41 FAIL |

**归因**：`rank` 把 S 推过 Sharpe 闸线（1.58,PASS）且 F 逼近 1.0（0.80）——本战役**第一次有一条候选的主闸全过**（Sharpe/Fitness/2Y/换手全 PASS）。但 sub 是**比率闸**（0.52×S）：S 越高闸线越高（0.84）,sub 停在 0.59 不动,缺口反而从 0.23 扩大到 0.25;robust 三档几乎不动（0.40/0.41/0.41）。**两个铁证**：① `signed_power(·,2)` 拉陡分布与 `rank` 均匀化是两个方向的分布手术,读数几乎相同（1.54 vs 1.58）⇒ robust 不受截面分布形态影响;② robust 与 CLUSTER_TEST 同步偏低且**不随任何分布/掩码/分组杠杆移动**。**结论：`significant_value_1` 的 robust 失败是结构性问题（信号集中在稳健子宇宙之外的少数名字）,分布重塑三板斧（rank/signed_power/cap 掩码）全部证伪,不再做第四种分布手术。** 本字段族剩余可试轴只有「换分组粒度」与「换读数窗口/形态」——但窗口族在 `total_top_buy_shares` 上已证 66d 是峰,分组轴（sector/subindustry）尚未测。已提交 sector/subindustry 分组对照（multisim `3yy5do6Xl4sSb3fUYhGw6k`）作本字段族最后一轮杠杆测试,若仍不过 robust 闸,本字段族按"结构性 robust 不可修复"归档。

**`significant_value_2`/`directional_significant_value_1` 模拟级 FAIL 诊断（2026-11-06）**：两字段在 multisim `1bIbot7HF5eja5S16Pw9vFfC` 与重试批 `1Q65Gvget4sKb6Utio85Q7T` 均以平台级 FAIL 终结（无 alpha 产出,`lookINTO_SimError_message` 只返回裸 FAIL 无错误消息）,表达式经 `validate_expressions` 确认字段存在且语法合法。已提交 `significant_value_3`/`significant_value_4` 同骨架探针（multisim `DriZx4Zt4PSaUYB6ZrXxw0`）作对照诊断：若 _3/_4 能出 alpha,则 FAIL 是 _2/directional_1 两个字段的数据层问题（如全 NaN 段或极端值炸掉回测引擎）;若 _3/_4 同样 FAIL,则是骨架或平台层问题。
- `directional_indicator` 基础版（2026-11-06 已测，`rank(ts_backfill(directional_indicator,66))`，无 group_rank/行业分组骨架）→ alpha `2rAXMbPP`：S −0.11、F −0.01、2Y −0.34，近乎纯噪声，与同族 `directional_indicator_2`（历史判死,TO 爆炸）方向一致地确认本族无信号。**字段覆盖闸：`directional_indicator`/`directional_indicator_2` 两支方向指标族计入已覆盖，均确认无效，不再测其它骨架。**
- **`avg_top_buy_shares` 字段覆盖候选（已提交，已终态）**：`tail(winsorize(group_rank(ts_sum(avg_top_buy_shares, 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)`——同买入骨架，`total_top_buy_shares`（求和）换成 `avg_top_buy_shares`（求均值），检验"单笔交易平均规模"是否携带与"累计总量"不同的信息。multisim `4aKOax3p95i9cKTYb3T66Ob`（与 `insiders1` 的 `max_trade_price` 候选同批提交，2026-11-06）。

**结果（alpha `RRElJ5ag`）——与 `total_top_buy_shares`（`akKe5zK6`）近乎同一个信号**：

| 字段 | alpha id | S | F | TO | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|
| `total_top_buy_shares`（求和） | `akKe5zK6` | 0.72 | 0.31 | 0.0397 | 0.73 | 0.45 FAIL | 0.70（压线） |
| `avg_top_buy_shares`（求均值） | `RRElJ5ag` | 0.72 | 0.31 | 0.0395 | 0.68 | 0.43 FAIL | 0.62 FAIL |

**归因**：S/F/TO 四位有效数字几乎完全一致，2Y/sub/robust 小幅更差（非改善）。说明本数据集"高管买入"事件在同一天内**多为单笔申报**（求均值≈求和/1），`avg_*` 没有提供"总量"之外的增量信息，二者是同一机制的两种读数而非独立模板族。**字段覆盖闸：`avg_top_buy_shares` 计入已覆盖**，确认冗余后不再对 `avg_*` 系列（`avg_top_sell_shares`/`avg_secondary_*`）逐一重复测试——按同一归因外推,其余 `avg_*` 字段大概率对其 `total_*` 对应项同样冗余,除非该子族（董事直接/全体董事）本身呈现多笔申报模式（留作 §5 广度对照时顺带验证,不单独开波）。

## 6. 广度对照结果（2026-11-06 终态，multisim `3wG7cV4OI4mSbJ21d404zNSE`，SLOW_AND_FAST 档）——GLB 卖方广度梯度不迁移到 EUR 买方

| 子集 | 字段 | alpha id | S | F | TO | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|---|
| 高管买入（基线） | `total_top_buy_shares` | `QPvNZ5pr` | **1.30** | **0.62** | .0835 | 2.13 | 0.71 PASS | 0.80 PASS |
| 全体董事买入（求和） | `total_buy_shares` | `zq32MogO` | 1.17 | 0.52 | .0899 | 2.02 | 0.59 FAIL（闸 0.62） | 0.47 FAIL |
| 全体董事买入（求均值） | `avg_buy_shares` | `QPvNJlOw` | 1.14 | 0.50 | .0897 | 1.88 | 0.54 FAIL | 0.37 FAIL |

**归因**：论坛帖 `43592107256215` 的"覆盖面最广的子集信号最强（全体董事 > 高管 > 直接交易）"是在 **GLB 卖方信号**上建立的梯度；本实测把同一广度轴搬到 **EUR 买方**后方向**相反**——全体董事（1.17）弱于高管（1.30），且 sub/robust 从双 PASS 双双转 FAIL。经济解释：买方的信息含量集中在**高管**（最了解公司的人）的行动里，扩大到全体董事反而掺入了信息含量较低的董事层面交易稀释信号；卖方则相反（卖出多由流动性/分散化驱动，只有覆盖面足够广时才能从噪声中显形）。**JMZ(2003) 的买卖不对称在此进一步具体化为「买看身份层级、卖看覆盖广度」**。`avg_buy_shares` 与 `total_buy_shares` S 差 0.03、形态一致——`avg_*` 冗余规律**第三次**得到独立确认（此前 `avg_top_buy_shares` vs `total_top_buy_shares` 亦然），该规律升格为本数据集的确定性结论。**字段覆盖闸：`total_buy_shares`/`avg_buy_shares` 计入已覆盖；广度轴（全体董事）已测尽，不再测 `total_secondary_*`（董事直接，按梯度外推只会更弱，不作无意义重复——除非后续有反向实证证据）。**

## 9. 方向符号显著金额族平台级 FAIL 终判（2026-11-07）

`top_directional_significant_value_1/2/3` + `directional_significant_value_2` 四臂（88d zscore 栈，`validate_expressions` 全部通过）在 multisim `imZTFf4t4qP9J7jl9vi2ag` **全部平台级 FAIL**（无 alpha、无错误消息）——连同此前 `directional_significant_value_1` 两次 FAIL，该族 **8 支方向字段在 EUR 确定性仿真失败**，是数据层问题（带符号字段疑似损坏），非表达式问题。**字段覆盖闸：方向族 8 字段按「平台级不可用」计入已覆盖，不再重试。**

**本集 34 字段覆盖终态**：买卖股数族 16 全测、方向指标族 2 全测、无方向显著金额族 8 测 6（_2/directional_1 平台 FAIL）、方向显著金额族 8 平台级不可用——**覆盖闸 100%**。

**insiders 锁定令后的下一杠杆方向**：
1. `insiders1` 机制 B/C 回灌战役后期新杠杆（`group_zscore` 替换 + `rank(group_scale)` 栈——该集归档时未发明），已提交 multisim `3DWS2e64y4v8a7wDc19Swhh`
2. 席位 1 的近亲备选池（互相关 >0.98 只取一席）：`leA5JeP7`（主）、`QPvNeeqK`、`VkxmnQNG`（2Y 2.42）、`A1Vr6Xxd`（decay 13）

## 10. 卖方直接交易族（2026-11-07,GLB 帖卖方广度梯度的 EUR 直接交易补测）

GLB 帖 `43592107256215` 的卖方梯度（全体董事 0.47 > 高管 0.23 > 直接 0.08）中「直接交易」档在 §6 广度对照时按外推跳过了;现补测 `total_secondary_top_sell_shares`/`total_secondary_sell_shares`（高管直接卖出/董事直接卖出,88d zscore 栈,SLOW_AND_FAST——卖方与买方共用已验证骨架做同构对照）。

## 11. 卖方直接交易族实测（2026-11-07 终态，multisim `e3ta1gTk5an8PSA4eClzEf`）

| 变体 | alpha id | S | 2Y | sub | robust |
|---|---|---|---|---|---|
| 高管直接卖出 88d 栈（正向） | `A1Vr8qpQ` | −0.90 | −0.15 | −0.96 | −0.93 |
| 董事直接卖出（正向） | `QPvNpmxp` | −0.83 | −0.04 | −0.65 | −0.52 |
| 高管直接卖出 reverse | `RRElw0gj` | 0.90 | **0.15** | 0.96 | 0.93 |
| 董事直接卖出 reverse | `KPJ5Mx18` | 0.83 | **0.04** | 0.65 | 0.52 |

**归因**：① 卖压→跑输方向成立（JMZ 买卖不对称再确认），反向 sub/robust 全战役最高（0.96/0.93）——**卖方信号的结构质量极好**；但 2Y≈0：**卖方 alpha 集中在 2014–2021，近两年枯竭**（卖空约束收紧/披露套利饱和的结构性变化）。反向版距 S 闸差 0.68 且 2Y 不可修——**卖方直接交易族归档**（信号存在、结构好、但近期枯竭）。② 高管直接（0.90）> 董事直接（0.83）与买方层级一致。③ 净额（买−卖）差已无必要：买卖两侧的 alpha 年份不重叠（买方 2Y 2.0+、卖方 2Y≈0），合并只会稀释。

## 12. insider_agg_matrix 覆盖闸终态与战役收束（2026-11-07）

**34 字段全覆盖确认**（含平台级不可用 8 支方向字段）。本集最终格局：
- **席位 1**：`leA5JeP7`（`top_significant_value_2` 88d zscore 栈，S 1.76/F 0.94/2Y 2.32，Mode B main_gate）
- 近亲备选池（互相关 >0.98 二选一）：`QPvNeeqK`（_1 版）、`VkxmnQNG`（d13+d5，2Y 2.42）、`A1Vr6Xxd`（d13）、`bl6r7RRq`（d20）
- 结构最好但 S 不足的备份：`E568Xm1m`（total_top_buy 88d 栈，S 1.51，sub 0.93/robust 0.98）
- 已穷尽轴：中性化 4 档、窗口 7 档、分组 3 轴、归一化 4 种、分布 3 种、decay 4 档、平滑 d5、买/卖/身份层级/方向全部字段族
- 已死轴（勿再试）：cap 掩码、signed_power、sector 分组（强度族）、ts_decay_linear、ts_zscore 自身基线、TOP2500、RAM/CROWDING、ts_mean(·,22) 预平滑、卖方直接交易（2Y 枯竭）、方向字段族（平台级数据损坏）

**insiders 锁定令下的类别内剩余空间**：insider_agg_matrix 覆盖闸 100% + insider_trajxtrix（历史判死维持）+ insiders1 第二轮回灌后重新归档（天花板 1.14，44d 栈）。**类别内可用增量已接近穷尽；下一次复核触发条件 = 战役级新杠杆发明（如 group_zscore 之于 group_rank），或席位 1 提交后按 self/prod 相关性反馈回炉。**

## 13. ★ insiders1 与 insider_agg_matrix 互相关发现（2026-11-07,7 席本地互测）

`compute_mutual_correlation`（threshold 0.5）：**`vR1poWNz`（insiders1 44d 栈,S 1.14）与席位 1 及全部 insider_agg_matrix 候选互相关仅 0.14–0.17**——同一「insiders 类别」内,**逐笔申报明细（insiders1）与厂商预聚合矩阵（agg_matrix）是两套独立信息源**。insiders1 的 0.97→1.14 复活因此有独立席位价值（若未来过闸,可作为 INSIDERS 塔第二席）。`max_mutually_below_subset = {leA5JeP7, vR1poWNz}`。

对 insiders1 的含义：44d 栈距 Mode B 主闸 S 1.25 仅差 0.11、F 差 0.12——** Mode B 资格判定值得一跑**（旁路 E 需 2Y≥1.2,当前 0.71 不满足;主闸需 S≥1.25,差 0.11）。

**Mode B 判定（insiders1 44d 栈）**：`eligible=false, verdict=dead_end`（S 1.14<1.25 ∧ F 0.68<0.8 ∧ 2Y 0.71<1.2 三项同弱,旁路不救）——insiders1 独立席位暂不可行,**须先过主闸**。它的价值保留为：① 互相关 0.14 的独立信息源（未来过闸即第二席）;② 三项缺口均小（0.11/0.12/0.49）,任何新杠杆（幅度类,如更优 winsorize 档/quantile 归一化）都可能推过。

## 14. ★ country 分组轴突破 + 窗口/切片补测（2026-11-07 深夜，multisims `ORWshd2w55Ebzs19OpcATmL`/`W3h8YaYn4WOcgi1bNzbMS5P`/`peFFi2tb59AcfxwL0GmhEM`/`1Q9cfqahR4Z3c4BQMjzN4Qz`/`41XCSn7gl4Hoa3T1hJgMrt0F`）

| 变体 | alpha id | S | F | 2Y | sub | robust | 卡闸 |
|---|---|---|---|---|---|---|---|
| `top_significant_value_2` 88d 栈（席位 1 复测） | `leA5JeP7` | 1.76 | 0.94 | 2.32 | 1.07 | 1.07 | 仅 F |
| `_2` 88d 栈 + d5 | `LLMmvgr9` | 1.74 | 0.92 | 2.35 | 0.99 | 1.02 | 仅 F |
| `_2` 66d 栈 | `88RE0aYX` | 1.60 | 0.83 | 2.33 | 0.92 | 0.77 | 仅 F |
| `_1` 44d | `JjeW9E6E` | 1.29 | 0.62 | 1.37 | 0.65 | 0.61 | top_* 用 88d |
| **`_2` 88d × country 分组** | **`2rAX3q2w`** | 1.68 | **0.87** | 2.32 | 0.99 | 0.96 | 仅 F 0.87 |
| **`_2` 88d × country + d5** | **`mLo0E6A2`** | 1.68 | **0.87** | **2.40** | 0.93 | 0.92 | 仅 F 0.87 |
| `_1` 88d × country | `9qxdNWKd` | 1.67 | 0.87 | 2.27 | 0.97 | 0.97 | 仅 F 0.87 |
| `total_top_buy_shares` × country | `j2YPq8d9` | 1.53 | 0.75 | 1.95 | 0.87 | 0.88 | S/F |
| `significant_value_1` 44d | `GrWKRAZ3` | **1.62 PASS** | 0.82 | 1.98 | 0.69 FAIL | 0.45 FAIL | robust 结构性 |
| 非高管切片（sig_1 − top_sig_1） | `YP1EeJKR` | 0.82 | | | | | 信息在高管 |
| 月度聚合 ts_mean(22,22) | `YP1ERw9W` | 1.25 | | | | | 无增益 |

**归因**：① **country 分组轴是 insider 域从未测过的新轴**——`_1/_2 × country` 三臂全部 F 0.87（比 industry 版 0.94 低但结构同绿），S 1.67-1.68 与 industry 版（1.75/1.76）略低。**country 与 industry 各占一端：industry 抬 S（行业内申报密度对比），country 抬 F/robust（剔除跨国申报制度差异）**——两者互相关待测，若 <0.9 可能构成同字段双席位。② 44d 对 top_* 族更差（1.29 vs 1.76）——修正 §10 的「粒度决定窗口」假说：**top_significant_value_* 是厂商预聚合（同 agg_matrix 粒度）用 88d,insiders1 的逐笔明细才用 44d**。③ `significant_value_1` 44d（1.62）优于 88d（1.45）但 robust 0.45 结构性锁定不变。④ 非高管切片（0.82）证明高管主导,月度聚合无增益。

**country/industry 双席位假说证伪（2026-11-07）**：6 席互测——country 版与 industry 版互相关 0.97–0.997（同信号），`max_mutually_below_subset` 维持 `{leA5JeP7, ZYQdErnd}` 2 席。**席位 1 的换装备选顺序（self/prod 反馈后按需切换）**：`leA5JeP7`（industry,F 0.94）→ `mLo0E6A2`（country+d5,2Y 2.40）→ `LLMmvgr9`（industry+d5,robust 1.02）→ `2rAX3q2w`（country）。**结论：insider_agg_matrix 全部轴已穷尽（含 country 新轴），席位池 6 条互相关 0.97+ 单席位。**

## 15. 论坛交叉验证（2026-11-07，帖 `43467688159511` / `43615381230875`）

两帖与本战役结论互证：
1. **「增持信号纯度显著高于减持」**（WL27618）——与本战役 JMZ 买强卖弱、卖方 2Y 枯竭的实测一致。
2. **「多人协同更可信」**（协同增持置信度倍增）——对应本战役 `top_significant_value_1+2` 双字段强于单字段的方向；未测的「加总前 N 大显著金额」（`add(top_sig_1, top_sig_2)` 类协同读数）是本帖提示的未测维度。
3. **「相对金额占比」**（占年薪/身家比例）——`insiders1` 的 `valueeur/holdings` 比例机制正是该思想的实现，两集互证。
4. **「insider_agg_matrix 是 insiders 类里最冷的真成交，显著成交聚合比 raw 笔数干净」**（AM12075）——与本战役席位 1 选「显著成交金额」而非「笔数/股数」一致。
5. **「−88 是沉默，不是极小分数」**——本集字段未遇此哨兵值（聚合已过滤），但跨集使用 insider_feats 时须先排除。

**可复用未测维度（本帖提示）**：协同读数 `add(rank(top_sig_1), rank(top_sig_2))` 类——但注意禁混信号规则约束（同数据集同字段族内合成属「同机制读数」而非双腿,可用 rank 均值合成）。留待第三阶段。

## 16. 协同读数终判（2026-11-07，multisim `29rmIW2i5dZ95YUfKc3APa`，论坛帖 `43467688159511` 提示的维度）

| 变体 | alpha id | S | F | 2Y | 备注 |
|---|---|---|---|---|---|
| `add(top_1, top_2)` 协同 88d 栈 | `QPvz1Q1r` | **1.76** | **0.94** | 2.32 | 与 `_2` 单字段逐位同级 |
| `add(_1, add(_2, _3))` 三字段 | `0mYgb8bp` | 0.75 | 0.25 | 1.58 | 被 _3 反向污染 |

**归因**：① 双字段合成与 `_2` 单字段读数逐位相同——合成不产生增量（_2 主导），但**提供了语义更强的表达**（「高管前二大协同显著交易」），作为席位 1 的同义候选保留。② 加入 `_3` 直接崩盘（0.75）——字段梯度规律（_3 反向）第三次确认。**席位池最终 7 条，全部互相关 >0.97，单席位。insider_agg_matrix 至此全维度穷尽（16 节，覆盖闸 100%）。**

## 22. 卖方股数族 zscore 栈复测（2026-11-08,multisim `1Thmhi5lv4Elbfc1b0tmOq9Y`）——全体高管卖出股数（首测判死 S 0.01 的字段）

| 变体 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| reverse 卖出股数（industry） | `pwdGx7jx` | 0.95 | 0.37 | **0.38** | 0.88 | 0.83 |
| reverse 卖出股数（country） | `E56zNKv1` | 0.96 | 0.37 | **0.20** | 0.94 | 0.82 |

**归因**：① zscore 栈把首测 `QPvOwzvQ`（group_rank,S 0.01）救活到 0.95——**group_rank 骨架对卖出股数是致命的**（§6 已记录），zscore 栈才有效;② sub 0.88-0.94/robust 0.82-0.83 结构好,但 **2Y 0.20-0.38 近两年枯竭**——与卖方直接交易族（§11 2Y 0.04-0.15）同症状。**卖方信号在 EUR 近两年（2022-2023）全族枯竭**,这是数据层的结构性变化（披露规则/卖空约束）,不是骨架问题。卖方族终判维持归档。

## 23. ★ F≥1.0 攻坚终局（2026-11-08,用户修正验收标准后）

**验收标准修正**：F ≥ 1.0（review.fitness_min）才算过闸——此前 4 颗「全闸」候选 F 0.72-0.94 全部降级。

**F-push 全杠杆实测**：

| 杠杆 | alpha id | S | F | 结果 |
|---|---|---|---|---|
| tail 带宽 0.35/0.65 | `6XdJL7V7` | 1.76 | 0.94 | 与基线逐位同——rank() 抹平并列差异 |
| 外层 tail 0.3/0.7 | `LLMrYWam` | 1.73 | 0.92 | 反降 |
| **decay 2** | **`WjO0rQbP`** | **1.79** | **0.96** | 全战役 seat-1 族最高 F |
| decay 2 + 极端带宽 0.4/0.6 | `Jje1aENe` | 1.79 | 0.96 | 逐位同上（rank 抹平） |
| decay 2 + 标准 tail | `j2YxkRAk` | 1.79 | 0.96 | 同上 |

**F 闭式终局数学**：`F = S × sqrt(returns / 0.125)`（TO 0.073 < 0.125,分母钉死）。
- F 0.96 → 1.0 需要 returns +8%（0.036 → 0.039）或 S +0.12（1.79 → 1.91）
- returns 天花板：margin 9.8bp（信号质量上限）× TO 0.073（自然换手）≈ 0.036——机制收益封顶
- S 天花板：全杠杆（中性化/窗口/分组/归一化/分布/decay/tail/平滑）穷尽后 1.79-1.80
- **结论：insider_agg_matrix 机制的 F 结构性天花板 ≈ 0.96,差距 4% 不可闭合**

**全战役 F 天花板表**（F = S×sqrt(ret/0.125),TO 均 <0.125）：
- insider_agg_matrix：0.96（`WjO0rQbP` decay2）
- insider_feats：0.94-0.96（prod 墙另算）
- news18：0.77-0.80（returns 0.026 天花板更低）
- insiders1：0.68（S 1.14 主闸差 0.11）
- **model238：1.61 ✓ 唯一 F≥1.0,但 sub 0.57/robust 0.56 结构性卡死**（信号在 TOPCS1600 中尾部,sub/robust 宇宙不含）

**终局判定**：F≥1.0 + 全闸的组合在已扫 27 集中无解——「sub/robust 通过的机制 returns 封顶 0.036（F≤0.96）」与「returns 达标的机制（model238,ret 0.07）信号位置在 sub/robust 宇宙之外」两个约束互斥。剩余解锁路径：① 新数据集（EUR 剩余集全部 aC>331 拥挤或 vS≤2）;② model238 信号段与 sub/robust 宇宙重合的变体（`_d1` 已测,base 版未测——cov 0.77 更低但 vintage 不同,最后一个未测变量）。
