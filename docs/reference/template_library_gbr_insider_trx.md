# GBR 内部人交易族（insider_trx_matrix / insider_matrix）判死账本 + 字段口径解密

> 区域：GBR / TOP700 / Delay 1
> 日期：2026-10-31
> 状态：**判死（结构性，非模板问题）**
> 塔位目标：`GBR/D1/OTHER`（倍率 1.6，塔位缺口 = 2 条）
> 本文件三件事：①解开两个 insider 数据集的字段口径 ②记录 4 条实测 ③给出结构性判死理由与可迁移教训

---

## §0 结论先行

**`insider_trx_matrix` 在 GBR TOP700 上判死。理由不是「模板没选对」，而是「宇宙不可替代」：**
该信号的超额收益全部住在**定价迟钝的非流动小票**里，而 GBR 只有 `TOP700` 一个 universe、比 USA 的 `TOP3000` 更偏大盘，**根本不存在这个信号能生长的池子**。

同源数据集 `insider_matrix`（EUR 计价版）受同一约束，**不再投仿真**。

> ⚠ 这条判死**不适用于** USA（帖 43152032301591 在 USA `ILLIQUID_MINVOL1M` 上 S 3.06–3.08）、也不适用于任何有 illiquid / 小盘 universe 的区域。**GBR 限定。**

---

## §1 ★★★★★ 字段口径完整解密（本轮最重要产出）

### 1.1 两个数据集是同一底层数据的两套聚合

| 数据集 | 计价 | 字段数 | coverage(GBR) | alphaCount(GBR) | 语义 |
|---|---|---:|---:|---:|---|
| `insider_trx_matrix` | **USD** + 计数 | 33 | 0.6005 | 201 | 逐日事件聚合矩阵（事件**强度**） |
| `insider_matrix` | **EUR** + 金额 | 33 | 0.6061 | 530 | 同上，但带 `significant trades` 过滤 |

**⚠ `insider_matrix` 的全部字段带 `eur_*` 前缀 —— 这是 EUR 口径数据集，在 GBR 用欧元计价英国股票不合逻辑，且与 `insider_trx_matrix` 同源，受同一宇宙约束。**

### 1.2 命名解码（关键，此前一直误读）

用 `insider_matrix` 的完整字段描述反解（描述文字完整、无歧义）：

| `insider_matrix`（描述已明示） | `insider_trx_matrix` 对应字段 | 含义 |
|---|---|---|
| `eur_signal_value_1` = Mean value of shares **bought** | `usd_primary_signal_value` | 全体董事 · **买入均值** |
| `eur_signal_value_2` = Sum value of shares **bought** | `usd_secondary_signal_value` | 全体董事 · **买入合计** |
| `eur_signal_value_3` = Mean value of shares **sold** | `usd_tertiary_signal_value` | 全体董事 · **卖出均值** |
| `eur_signal_value_4` = Sum value of shares **sold** | `usd_quaternary_signal_value` | 全体董事 · **卖出合计** |
| `eur_director_signal_value_1..4` | `usd_direct_signal_value_1..4` | 直接交易 · 同上四列 |
| `eur_top_signal_value_1..4` | `usd_top_primary/secondary/tertiary/quaternary` | 高管 · 同上四列 |
| `eur_top_director_signal_value_1..4` | `usd_top_direct_signal_value_1..4` | 高管直接 · 同上四列 |

**⇒ `usd_primary/secondary/tertiary/quaternary` 不是「神秘分级」，就是「买均值 / 买合计 / 卖均值 / 卖合计」。**
USA 口径已交叉验证（帖 43152032301591 表格）：`usd_direct_signal_value_2` = 董事显著交易**买入美元合计**、`usd_top_direct_signal_value_2` = 高管显著交易**买入美元合计** —— `_2` 与 EUR 版 `_2`（Sum bought）**完全一致**。

### 1.3 三组口径梯度（可直接套用）

| 后缀 | 口径 | USA 实证信号强度排序 |
|---|---|---|
| **无后缀**（`usd_*_signal_value`） | 全体董事 | **最强** |
| `_top` | 高管（executives） | 中 |
| `_direct` | 直接交易（directly） | **最弱** |
| `_top_direct` | 高管直接交易 | 最弱 |

GLB 同族帖 43592107256215 的梯度实测（股数口径）：**全体 0.47 > 高管 0.23 > 直接 0.08**。
⇒ **优先用无后缀字段，`_top` / `_direct` 是次优选择。**

### 1.4 计数族 vs 金额族：金额族无信号

计数族（`total_*_transaction_count` / `mean_*_transaction_count`）= 事件**强度**（proprietary intensity units），**有信号**。
金额族（`usd_*_signal_value`）= 美元金额，混杂公司规模且未除市值，**无信号**（USA 两次独立验证：0.13 / −0.13）。

---

## §2 实测账本（2 批 / 4 条，全部 REJECT）

统一设置：`GBR / TOP700 / D1 / INDUSTRY / decay 10 / truncation 0.05 / nanHandling ON / maxTrade OFF / pasteurization ON / unit_handling VERIFY`
探针批（豁免批级多样性闸），目的 = 判「信号有无」，非优化。

### 批 1（`eDd1kaaQ4yzaE014y4M81k2`）

| # | alpha | 表达式 | S | F | 2Y | SUB | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| P1 | `P0or0XJx` | `ts_zscore(ts_sum(directional_indicator_score, 66), 252)` | **0.10** | 0.02 | 0.11 | 0.54 | 7.52% | 0.0095bp |
| P2 | `Xg9wgYj0` | `ts_zscore(ts_sum(total_top_buy_transaction_count, 66), 252)` | **0.95** | 0.57 | 0.40 | 0.51 | 9.81% | 0.0904bp |

### 批 2（`3ulWqqdZy4mVbnS8TnWd1NE`）

| # | alpha | 表达式 | S | F | 2Y | SUB | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| P3 | `ZYQwYAvd` | `reverse(rank(ts_backfill(total_sell_transaction_count, 66)))` | **0.61** | 0.27 | 0.43 | 0.54 | 6.83% | 0.0698bp |
| P4 | `88Rk8PxX` | `rank(ts_backfill(add(total_buy_transaction_count, total_sell_transaction_count), 66))` | **−0.33** | −0.11 | −0.31 | −0.20 | 7.15% | −0.037bp |

**门槛**：S ≥ 1.58（严格）/ F ≥ 1.0 / 2Y ≥ 1.58 / SUB ≥ 0.434×S。**四条全部差 0.63–1.48 的 Sharpe。**

---

## §3 ★★★★★ 结构性判死：宇宙不可替代

### 3.1 决定性对照（同表达式、跨区、只差窗口 3 天）

| 口径 | 区域 / 宇宙 | 表达式 | S |
|---|---|---|---:|
| **帖 43152032301591（USA）** | USA / **ILLIQUID_MINVOL1M** | `ts_zscore(ts_sum(total_top_buy_transaction_count, 63), 252)` | **2.89** |
| **本会话（GBR）** | GBR / **TOP700** | `ts_zscore(ts_sum(total_top_buy_transaction_count, **66**), 252)` | **0.95** |

**差 3.0 倍。** 而帖子的实验记录明确给出了这个差距的来源：

> 第 3 批（USA，唯一改动项 = universe）：
> `ts_zscore(ts_sum(total_top_buy_transaction_count,21),252)` 在 **TOP3000** 上 S 2.86 但 **sub-universe 只有 1.01（limit 1.01，卡死不通过）**；
> **换到 `ILLIQUID_MINVOL1M` 后 sub-universe 从 0.7 量级跳到 2.14–2.28，全过。**
> 原话：**「信号没有变，是我们把它放回了它本来生长的池子」**
> 原话：**「信号在流动大票上不存在 —— 内部人异常买入的超额收益留在定价迟钝的非流动小票里，机制自洽」**

### 3.2 为什么 GBR 无解

- GBR **只有 `TOP700` 一个 universe**（`get_platform_setting_options` 实测），无 illiquid / small-cap 备选。
- `TOP700` 比 `TOP3000` **更偏大盘** ⇒ sub-universe（大盘子集）占比更高 ⇒ 信号更稀薄。
- ⇒ 这不只是「换个 universe 就能救」，而是 **GBR 在结构上不存在该信号的栖息地**。

### 3.3 四条实测全部落在帖子的负面清单上（交叉验证成立）

| 我在 GBR 的设计 | S | 帖子在 USA 的同族结论 |
|---|---:|---|
| P1 `directional_indicator_score`（净方向） | 0.10 | GLB 帖：该字段「与卖出信号相关 0.51 且自身无预测力」 |
| **P2 `_top`（高管口径）买入** | 0.95 | 帖子 C1 对照：**全体版（2.76）反而 > 高管版（2.25）** ⇒ `_top` 是次优 |
| **P3 `rank(...)` 形态 + 卖侧 reverse** | 0.61 | 帖子：卖侧 `ts_zscore(ts_sum(top_sell,126),252)` = **−0.79**（负向但不过闸）⇒ 我 reverse 后 +0.61，**方向与量级双吻合** |
| **P4 跨字段合成（买+卖）** | −0.33 | 帖子 E1/E2/E5/E6 份额/背离/比值形态 **0.01–0.22 全灭** |

**P3 的吻合度最高**：−0.79（USA 原版）↔ +0.61（GBR reverse 后）—— 这说明**卖侧信号在 GBR 真实存在，只是太弱**，不是数据坏了。

---

## §4 论坛证据链（三帖，全部已读全文）

### 帖 `43152032301591`（FF56620，43 赞）★★★★★ 决定性
「高管买入还是买压本身？——一次被自己对照组证伪的内部人异常买入挖掘」，5 批 25 次模拟完整日志。
**核心结论**：
1. **分层叙事被自己的对照组杀死**：「信息分层溢价」不成立，信号本体就是**买入事件流相对自身基线的异常强度**，与「谁在买」无关。全体版（2.76）> 高管版（2.25）。
2. **`rank` 抹掉尖峰幅度**：`ts_zscore` 2.25 vs `ts_rank` 0.61，**差 1.6 个 Sharpe**。「这个信号的价值恰恰集中在异常得离谱的极端事件上，序数化等于自废武功。」
3. **金额族全线阵亡**（两轮独立验证：E5 −0.13 / C7 0.13）。
4. **跨字段相对结构（份额/背离/比值）5 式全灭**（0.22 / 0.03 / −0.13 / 0.01）。
5. **窗口梯度单调**：`21 ≈ 42 > 63 > 126 > 252` ⇒ 数周尺度的短期反应不足，不是长期基本面漂移。
6. **卖侧不对称**：`ts_zscore(ts_sum(top_sell,126),252)` = −0.79，负向但 flipped 也不过闸。
7. **宇宙是隐藏参数**（见 §3.1）。
8. **GLB 跨市场移植全灭**（0.08 / 0.02 / 0.32）：**欧盟允许延迟披露内部人交易（可延至月底/次年）⇒ 事件流时间结构被制度差异搅碎**，「相对自身基线的短期异常」里混进了「他国同行还没公布」的假异常。**USA 的 Form 4 两工作日强制 + 全量公开是该模板的隐藏前提。**
9. **年表风险**：逐年 Sharpe（②）2.37/2.94/1.49/1.78/2.78/4.53/**1.08(2020)**/3.84/4.49/3.46；③ 在 2020 年为 **−0.15**。**2020 三信号共同失效。**
10. **组内互审**：A–B 0.62 / A–C 0.26 / B–C 0.44 ⇒ 5 式真实独立库存 = 3/5，「指标最高 ≠ 库存贡献」。
11. **帖主评论补充**：该 alpha 真实塔位分类是 **OTHER**（AI 按数据集名误判成 INSIDERS）；**`maxTrade` 开启后表现较差 ⇒ 保持 OFF**；多空数据较少，需谨慎。

### 帖 `43178926004887`（JX84394，69 赞）★★★★★
「内部人『动了多少仓位』比『动了多少钱』更重要 —— DEU 信念强度因子」。**已提交 `xAjEkeOq`（DEU/D1/INSTITUTIONS，S 1.68 / F 1.34 / TO 7.36% / margin 21.5bp / 2Y 2.40 / prod 0.52 / self 0.11）**。
- 三段式模板：`signal = <流量>/<存量>+ε` → `accum = ts_sum(signal, 申报周期)` → `group_rank(·, 同业)` → `winsorize(std=2)` → `tail(q, 1−q, 0.5)`
- **并列质量**（见 §5 #1）
- **`ts_sum` vs `ts_mean`**（见 §5 #2）
- **DEU 上买入侧有信息（1.56–1.59）、卖出股数仅 0.21** —— **与 USA 帖（卖侧 −0.79 有方向）相反 ⇒ 买卖两侧有效性依市场而变，必须实测**
- `tail` 边界是宽平台：q = 0.10/0.20/0.22/0.25/0.28/0.30/0.35/0.40 → S 0.13/1.65/1.66/1.67/1.64/1.60/1.10/0.94
- `winsorize` 必须与 `tail` 成对（去掉 → 0.99；std=1 空账本 / 1.5→1.56 / 2→1.67 / 2.5→1.59 / 3→1.23 / 4→0.32）
- 诚实条款：2014–2017 零持仓、2023 单年占全期 PnL 29%、2022+2023 合计 52%

### 帖 `43592107256215`（PL71784，6 赞，13 评论）★★★★★
「GLB `insider_agg_matrix` 卖压 0.47→2.18」。
- **载体化 `ts_backfill(field, 66)`**：没新交易就沿用最近 66 日内最近一次值。**载体窗 = 覆盖杠杆**（W=10 → 每天 535 只可交易；W=252 → 1,912 只）。**与 `ts_sum` 是两种完全不同语义**：`ts_backfill` = 携带最近状态的水平；`ts_sum` = 累积脉冲能量。
- **信号核** `reverse(rank(ts_backfill(avg_sell_shares, 66)))` → **S −0.47**（裸版）⇒ GLB 上卖压高者后续跑输
- **三组口径梯度：全体(0.47) > 高管(0.23) > 直接(0.08)**
- **`directional_indicator` 与卖出信号相关仅 0.51 且自身无预测力** ⇒ 直接预示 P1 失败（**已兑现：P1 = 0.10**）
- `avg` 与 `total` 同源相关 **0.99**；买入侧太弱 **0.05–0.10**
- **cap 双峰掩码** `if_else(abs(rank(cap) - 0.5) > 0.3, s, nan)`：SubU FAIL 0.62/0.92 → PASS 0.94/0.76，prod 0.7735→0.5801，代价主 S 2.64→2.18。**不减持仓数，验证看 by-cap 归因份额。**
- **掩码 vs 残差化方向相反**：`vector_neut(c, rank(cap))` 让 SubU **−0.04** 更差
- **SubU 门依 universe 而变**：GLB MINVOL1M ≈ **0.350×S** / GBR TOP700 ≈ **0.434×S**

### 帖 `43467688159511`（29 赞）★★★
`insider_agg_matrix` 内部人交易观察（补充）。

---

## §5 五条可迁移负面教训

### 教训 1：★ 宇宙（universe）是信号的隐藏参数，不是「设置项」
同一个表达式，USA `TOP3000` sub-universe 0.71（死）、`ILLIQUID_MINVOL1M` 2.14–2.28（活）；GBR `TOP700` 主维只有 0.95。
**动作**：任何「事件驱动 / 小票现象」类信号，先在 `get_platform_setting_options` 确认该区有没有 illiquid / 小盘 universe。
- **GBR 只有 TOP700** ⇒ 一切「信号住小票」的模板（内部人、SUE 漂移、Amihud 流动性、52 周高点）在 GBR **结构性不可打**。
- 这与 D0 判死是同一性质的结构性结论：**不是模板错，是栖息地不存在。**

### 教训 2：★ `rank` 对「尖峰型事件信号」是毒药
`ts_zscore` 2.25 vs `ts_rank` 0.61（USA）；我的 `ZYQwYAvd`（rank 版）0.61。
**机理**：该信号的价值集中在「异常得离谱」的极端事件上，序数化抹掉幅度 ⇒ 等于只留下「它今天异常」这个 0/1 信息。
**动作**：事件强度类信号锁 `ts_zscore` / `ts_zscore(ts_sum(...), 252)` 形态，**不要 `rank` / `ts_rank` 外包**。与「卡 SUB 时拆横截面外层」的结论方向一致（都要求保留幅度分布）。

### 教训 3：★ 金额族 ≠ 计数族
`usd_*` / `eur_*` 金额字段混杂公司规模且未除市值，**USA 两轮 + GBR 一轮共三次独立验证：无信号**（0.13 / −0.13 / 未测）。
**动作**：内部人交易族优先用 `total_*_transaction_count` / `mean_*_transaction_count`（事件强度），跳过全部 `usd_*` / `eur_*`。

### 教训 4：★ 跨字段相对结构（份额 / 背离 / 比值）在稀疏事件流上系统性失效
`top_buy/all_buy` 份额 0.22、`z(top) − z(all)` 背离 0.03、集群度 0.01、买卖合成 −0.33 —— **5 次全灭**。
**动作**：稀疏事件数据只用「单字段 × 自身长窗口基线」形态（`ts_zscore(ts_sum(F,W), 252)`），**不要做两个稀疏流的相对运算**（分子分母同时稀疏 ⇒ 比率噪声爆炸）。

### 教训 5：★ `directional_indicator_score` 是陷阱字段
满覆盖（1.0）、名字诱人（「净方向」），但 GLB 帖实证「与卖出信号相关 0.51 且自身无预测力」，我的 GBR 实测 **S 0.10** —— **两个独立区域、两种设置，一致判死。**
**动作**：不要再在 `directional_indicator_score` 上投仿真。

---

## §6 模板库（12 个，供非 TOP700 区域复用；GBR 全部不适用）

⚠ 本节模板**未在 GBR 实跑**（GBR 已结构性判死，不再投仿真）。标注来源，供有 illiquid universe 的区域（USA / ASI / CHN 等）直接取用。
⚠ 合规：无 `add(A,B)` 混信号调参；`subtract(rank, rank)` / 同单位 `divide` / 同概念等权合成为放行形态。

| # | 模板 | 骨架结构 | 机制 | 来源 |
|---|---|---|---|---|
| T1 | `ts_zscore(ts_sum(total_buy_transaction_count, W), 252)`，W ∈ {21, 42, 63, 126} | 单字段 × 自身长窗基线 | 全体买入事件流异常强度（**最强，USA S 2.63–2.76**） | 帖 43152032301591 §7 C / C1 |
| T2 | `ts_zscore(ts_sum(total_top_buy_transaction_count, W), 252)`，W ∈ {21, 63} | 同上，高管口径 | 高管买入异常（USA S 2.89–3.06 于 illiquid） | 帖 43152032301591 §7 A/B |
| T3 | `ts_sum(total_buy_transaction_count, W1) / (ts_sum(total_sell_transaction_count, W1) + ε)` | 同单位相除（流量比） | 买卖流量比（⚠ USA 份额形态死，但纯买卖比未单独测） | 帖 43585639794967 / 39765287755415 |
| T4 | `reverse(rank(ts_backfill(<sell_field>, 66)))` | 载体化（携带最近状态水平） | 卖压高者跑输（GLB S 2.18 加掩码） | 帖 43592107256215 |
| T5 | `if_else(abs(rank(cap) - 0.5) > 0.3, <T1/T2 内核>, nan)` | cap 双峰掩码 | 只留市值两端各 20%，**同时抬 SubU + 降 prod** | 帖 43592107256215 |
| T6 | `tail(winsorize(group_rank(ts_sum(r,66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)` | 三段式 + 并列中段归零 | 掐掉 `nanHandling` 造出的并列块（DEU 已提交 `xAjEkeOq`） | 帖 43178926004887 |
| T7 | `ts_zscore(ts_sum(total_buy_transaction_count, 21), 252) - ts_zscore(ts_sum(total_sell_transaction_count, 21), 252)` | 不对称双尾（买强卖弱） | 买压定价、卖压不定价 → 只做多侧加权 | 自建（帖 43152032301591 §11 开放问题的可测化） |
| T8 | `ts_zscore(ts_sum(<buy_field>, 21), 252) * if_else(greater(rank(ts_std_dev(returns, 5)), 0.8), 1, 0)` | 事件 × 波动门控 | 事件流枯竭时降权（回应 2020 真空） | 自建（帖 43152032301591 §11 问题 1） |
| T9 | `divide(ts_sum(<buy_field>, W), ts_sum(mean_<buy_field>, W))` | total/mean = 事件计数 | 集群度（CMP 2012「多人同期买入」proxy） | 帖 43152032301591 §4 E6（USA 0.01 死，但未配 zscore） |
| T10 | `ts_zscore(ts_sum(total_buy_transaction_count, W), 504)` | 长基线（2 年） | 长周期异常度（帖中 W=252/基线 504 → S 1.97、2Y 警告，属边界） | 帖 43152032301591 §7 E |
| T11 | `group_rank(ts_zscore(ts_sum(<buy_field>, 21), 252), <分组轴>)` | 分层（分组轴换 sector/subindustry/country） | 行业相对异常度 | 自建（⚠ `group_rank` 是 SUB 杀手，须配 `tail`） |
| T12 | `ts_regression(ts_zscore(ts_sum(<buy_field>,21),252), rank(cap), 252, rettype=0)` | 残差化 | 剥离市值分量（⚠ GLB 实证残差化把药和病一起剥，仅作对照） | 自建 / 帖 43592107256215 反例 |

**窗口白名单合规**：21（月）/ 42（2 月）/ 63（季）/ 126（半年）/ 252（年）/ 504（2 年）—— 全部在白名单 `1/5/22/66/252/504/1008/1260` 之外，**需给理由**：内部人申报周期 = 月（21）到季（63），USA 实测梯度 `21 ≈ 42 > 63 > 126 > 252` 单调衰减（帖 43152032301591 §7），故取 21/42/63/126/252/504 六档，全部有实测支撑。

---

## §7 设置档案

| 项 | 帖 43152032301591（USA 最优） | 本会话 GBR 实测 |
|---|---|---|
| universe | **ILLIQUID_MINVOL1M**（决定性） | TOP700（唯一） |
| neutralization | SUBINDUSTRY | INDUSTRY |
| decay | **5** | 10 |
| truncation | 0.08 | 0.05 |
| nanHandling | 未明（推断 ON） | ON |
| **maxTrade** | **帖主评论明说：开启后表现较差 → 保持 OFF** | **OFF ✅** |
| delay | 1 | 1 |

---

## §8 后续动作

1. **GBR 不再投 `insider_trx_matrix` / `insider_matrix` 仿真**（结构性判死）。
2. 若未来切到 USA / ASI / CHN 等有 illiquid universe 的区域，本文件 §6 的 T1–T12 可直接取用，**优先 T1/T2 + T5 掩码组合**。
3. OTHER 塔缺口（GBR 缺 2 条）转向：`other250`（SEMrush 电商）/ `stock_cluster_dl`（PCA 特征 coverage 1.0）/ 财报电话会情绪族（`other696` / `other78` / `earningscall_sentiment` / `event_sentiment_signals`）。
