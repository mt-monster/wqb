# order_flow_imb（Institutional Order Flow Imbalance）USA 模板库

> 区域：**USA / TOP3000 / Delay 1**　塔位：**OPTION**（`ra.pyramid_short=option`，单塔 `pyramids.effective=1`）
> 维护日期：2026-10-29　波次：156（CC）/ 158（DD）/ 159（EE）/ 160（FF）
> 本文档是**模板库单一事实源**，每波收批后追加。实测结果一律标注 alpha id 便于复核。

---

## 1. 数据集画像

### 1.1 拥挤度分层（`get_datasets` category=option，6 个数据集）

| dataset | 名称 | coverage | 字段 | 用户 | alpha | valueScore |
|---|---|---|---|---|---|---|
| `option8` | Volatility Data | 0.9698 | 64 | 36583 | 210929 | 1.0（红海） |
| `option9` | Options Analytics | 0.9817 | 74 | 24500 | 86640 | 1.0（红海） |
| `option6` | Forecasted Volatility | 0.9616 | 133 | 1963 | 19183 | 1.0（红海） |
| `option40` | Options Analytics Data | 0.9755 | 208 | 976 | 3285 | 2.0 |
| `option3` | Equity Options Moneyness | 0.8801 | 20 | 302 | 515 | 3.0 |
| **`order_flow_imb`** | **Institutional Order Flow Imbalance** | **0.8092** | **120** | **213** | **511** | **3.0（最空）** |

**选型理由**：`order_flow_imb` 是 OPTION 类里 alphaCount 最低（511，仅为 option8 的 0.24%）、valueScore 最高的池子。但它同时是全类 coverage 最低的（0.8092），需要用时间跨度验证兜底（见 §1.3）。

### 1.2 字段结构：5 个正交维度（120 字段）

| 维度 | 取值 | 说明 |
|---|---|---|
| **参与者** | `customer` / `pro_customer` / `broker_dealer` / `market_maker` / `firm` / `proprietary` | 6 类，经济学含义完全不同 |
| **方向** | `bullish` / `bearish` | bullish = 买 call + 卖 put；bearish = 卖 call + 买 put |
| **度量** | `vol` / `trade_count` / `trades` / `contracts` / **`*_imbalance`** | 前四者是原始量，`*_imbalance` 是**平台预归一化**的净差 |
| **数据源变体** | 裸（默认）/ `_ise` / `_noto` / `_noto_2` / `_otm` | 不同交易所 / 不同货币性筛选 |
| **类型** | 全部 `MATRIX` | **无需 `vec_*`**（与 shortinterest3 全 VECTOR 形成对照） |

**覆盖率分档（关键）**：

| 组 | coverage | 说明 |
|---|---|---|
| 裸版（`customer_*` / `broker_dealer_*` / `market_maker_*` / `firm_*` / `pro_customer_*`） | **0.9058** | 主战场 |
| `_ise` | 0.7882 | ISE 交易所 |
| `_noto` | 0.7728 | NOTO 数据源 |
| `_otm` | 0.7701 | 仅虚值合约 |

> **判读**：裸版覆盖率 0.9058 显著高于变体，**优先用裸版**。变体的价值不是覆盖率而是正交性（不同交易所的微观结构差异）。

### 1.3 时间跨度验证（`get_alpha_yearly_stats(vR103A2w)`）— 硬证据

| 年 | longCount | shortCount | sharpe | returns | margin |
|---|---|---|---|---|---|
| 2014 | 1533 | 1563 | 0.25 | 0.46% | 0.000062 |
| 2015 | 1576 | 1561 | **2.15** | 3.92% | 0.000559 |
| 2016 | 1605 | 1522 | 1.41 | 2.57% | 0.000365 |
| **2017** | 1596 | 1504 | **−0.11** | −0.19% | −0.000027 |
| 2018 | 1540 | 1578 | 0.50 | 0.95% | 0.000133 |
| 2019 | 1567 | 1540 | **2.42** | 4.50% | 0.000641 |
| 2020 | 1532 | 1568 | 1.51 | 4.05% | 0.000557 |
| 2021 | 1530 | 1618 | 1.19 | 2.51% | 0.000327 |
| 2022 | 1596 | 1557 | **2.11** | 5.14% | 0.000732 |
| 2023 | 1616 | 1550 | 0.89 | 2.07% | 0.000292 |

**结论**：
1. **十年无断档** —— 每年 longCount 1530–1616（波动 <6%），满足「近十年都有数据」硬要求 ✓
2. **接近满仓** —— 多空合计约 3100，覆盖 TOP3000 全宇宙 ⇒ 不存在「少数股票撑起来」的集中度隐患，这是 CW 能 PASS 的根本原因
3. **强 regime 依赖** —— 高波动年份（2015 / 2019 / 2022）sharpe 2.11–2.42，低波动年份（2014 / 2017 / 2018）−0.11–0.50。**全期 S 被弱年拖累**是 OPTION 塔的核心结构性难题

---

## 2. 机制假设

| # | 假设 | 文献依据 | 适用参与者 | 方向先验 |
|---|---|---|---|---|
| **H1** | 散户 customer 的期权方向失衡是**反向**指标（噪声交易者） | Pan & Poteshman (2006) "The Information in Option Volume for Future Stock Prices", RFS | `customer` | 需取 **reverse** |
| **H2** | 做市商 market_maker 的失衡是**被动承接**，与对手盘反向 | 做市商理论（Kyle 1985 / Glosten-Milgrom 1985）；做市商净多头寸 = 承接了看跌对手盘 | `market_maker` | 需取 **reverse** |
| **H3** | 专业客户 pro_customer 是**聪明钱**，方向与未来收益同向 | 机构投资者信息优势（Cohen-Malloy-Pomorski 2012） | `pro_customer` | **正向** |
| **H4** | `_otm` 虚值合约的失衡更纯粹（少受对冲盘干扰），但被微盘噪声稀释 | OTM 期权杠杆更高，投机属性更强 | 全参与者 × `_otm` | 待测 |
| **H5** | 不同数据源（`_ise` / `_noto`）反映不同交易所，信息可正交 | 交易所微观结构差异 | 全参与者 | 待测 |

**USA 实测对 H1 的裁决**：CC1 / CC2 中 **正向**（不 reverse）得 S 1.53 / 1.60，反向则会得负 S ⇒ **Pan-Poteshman 的反向假设在 USA TOP3000 的 customer 侧不成立，customer 是正向信号源**。这与「散户是噪声交易者」的经典结论相反，可能原因：USA 期权市场的 customer 分类里混入了大量通过经纪商下单的机构账户。

---

## 3. 模板库（M1–M17）

### 3.1 已实测（M1–M10）

| # | 模板名 | 表达式骨架 | alpha | S | F | TO | 2Y | SUB | margin | ratio | fRA | 裁决 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **M1** | 原始比值 | `divide(subtract(bull,bear), add(bull,bear))` | `xArM8JZn` | 1.53 | 0.23 | **137.56%** | −0.88 | 0.96 | 0.000044 | — | 4 | ✗ 换手爆表 |
| **M2** | 计数比值 | 同 M1 但用 `*_trade_count` | `1YNvQ6ZM` | 1.60 | 0.25 | **140.17%** | −0.34 | 0.88 | 0.000047 | 0.725 | 3 | ✗ 换手爆表 |
| **M3** | 参与者差分 | `subtract(broker_dealer_vol_imbalance, <M1>)` | `d5WqAeaX` | −1.41 | −0.20 | 138.23% | 0.52 | −0.97 | — | 0.979 | 5 | ✗ **共线性诊断**：≈ −2×customer，BD 侧无独立信息 |
| **M4** | 时序 z 标准化 | `group_zscore(ts_zscore(<M1>, 252), subindustry)` | `QPvekAVK` | 0.86 | 0.10 | **137.58%** | −1.07 | 0.51 | — | 0.849 | 4 | ✗ 时序标准化**不降换手** |
| **M5** | 时序平滑 | `ts_decay_linear(<M1>, 66)` | `N1NMvKzE` | 1.52 | 0.28 | **107.7%** | +0.70 | 0.37 | 0.000067 | 0.342 | 5 | ✗ 只降 30pp |
| **M6** | **均值 + 横截面归一** | `group_zscore(ts_mean(<M1>, 66), industry)` | `vR103A2w` | 1.26 | 0.54 | **14.32%** | **1.54** | 0.18 | 0.000363 | **0.889** | 4 | ★ 换手解了，S/F/SUB 不足 |
| **M7** | OTM + 平滑 | `ts_decay_linear(<OTM 版 M1>, 66)` | `d5WqAW3Y` | 0.82 | 0.11 | 123.14% | +0.65 | 0.21 | 0.000039 | 0.329 | 6 | ✗ OTM 更持久但更弱 |
| **M8** | **聚合构造 66** | `divide(subtract(ts_sum(bull,66),ts_sum(bear,66)), add(ts_sum(bull,66),ts_sum(bear,66)))` | `QPveXPGM` | 1.52 | **0.71** | **11.32%** | 0.80 | **0.36** | **0.000475** | 0.737 | 4 | ★★ **SUB 翻倍**，2Y 弱 |
| **M9** | 聚合构造 OTM 66 | 同 M8 用 `*_vol_otm` | `pwd0O08o` | 0.58 | 0.18 | 10.27% | 0.00 | 0.01 | 0.000223 | 1.224 | 4 | ✗ OTM 聚合全灭 |
| **M10** | **聚合构造 22** | 同 M8 窗口 22 | `LLMeJA81` | **1.60** | 0.59 | 20.74% | **1.14** | 0.35 | 0.00027 | 0.731 | 3 | ★★ S 最高、2Y 回升 |

### 3.2 波 160（FF）实测（M11–M17）

| # | 模板名 | 表达式骨架 | alpha | S | F | TO | 2Y | SUB | margin | ratio | fRA | 裁决 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **M11** | 聚合66 + 均值22 + 归一 | `group_zscore(ts_mean(<M8>, 22), industry)` | `2rAEdmV8` | 0.80 | 0.28 | 6.02% | 0.74 | 0.22 | 0.000501 | 0.888 | 4 | ✗ **信号崩塌**（EE1 的 S 1.52→0.80） |
| **M12** | 聚合66 + 归一 | `group_zscore(<M8>, industry)` | `LLMeJwkv` | 1.28 | 0.56 | 12.12% | 0.70 | 0.38 | 0.000394 | 0.719 | 4 | △ 归一让 SUB 微升 0.36→0.38 但 S −0.24 |
| **M13** | 聚合22 + 归一 | `group_zscore(<M10>, industry)` | `QPveXv3X` | 1.52 | 0.54 | 21.97% | 1.24 | 0.29 | 0.000255 | 0.665 | 4 | △ TO 未降（20.74%→21.97%），SUB 反降 |
| **M14** | **聚合22 + 均值22 + 归一** | `group_zscore(ts_mean(<M10>, 22), industry)` | `O0AeaVPq` | 1.15 | 0.47 | **9.21%** | **1.62 ✓** | 0.34 | 0.000458 | **0.826** | **3** | ★★ **首个 2Y 过闸**，fRA 全塔最少 |
| **M15** | **做市商（H2）** | `group_zscore(ts_mean(market_maker_vol_imbalance, 22), industry)` | `88RA1E5X` | **−1.19** | −0.36 | 25.3% | −1.46 | **−0.53** | −0.000187 | 1.143 | 4 | ★★ **强反向信号**：取反后 SUB +0.53 几乎过闸 |
| **M16** | 专业客户（H3） | `group_zscore(ts_mean(pro_customer_trade_imbalance, 22), industry)` | `O0AeaMrb` | 0.02 | 0.00 | 22.89% | 0.82 | 0.35 | 0.000003 | 15.0 | 3 | ✗ **完全无信号**，H3 判死 |
| **M17** | ISE 数据源（H5） | `group_zscore(ts_mean(customer_vol_imbalance_ise, 22), industry)` | 待测 | — | — | — | — | — | — | — | — | 待补发 |

**本波最重要的两条判据**：
1. **`group_zscore` 在聚合构造上是负增量** —— 对比 M8(1.52)→M12(1.28)、M10(1.60)→M13(1.52)、M11(0.80)。归一的真正价值只在于修正**日度比值**的跨股票量纲差异（M6 场景 137.56%→14.32%）；一旦 `ts_sum` 把分母量级稳定住，比值已天然在 [−1,1] 且跨股票可比，再 zscore 就是纯噪声放大。
2. **做市商与客户侧是两套完全不同的机制** —— customer 侧 SUB 0.18–0.38（小市值失效），market_maker 侧 SUB **0.53**（小市值同样有效）。前者靠「主动成交方向」，后者靠「被动承接的逆向选择成本」（Glosten-Milgrom 1985）。


### 3.3 库内储备（未测，M18+）

| # | 模板名 | 骨架 | 待验证假设 |
|---|---|---|---|
| M18 | 分组轴扫描 | M11 骨架 × {`subindustry`, `sector`, `market`, `exchange`} | 更粗轴能否抬 SUB |
| M19 | 新建仓 vs 平仓 | `divide(new_loans, total_loans)` 类构造（若字段存在） | 增量信息 vs 存量信息 |
| M20 | 波动率 regime 门控 | `trade_when(<成交量相对水平 > 阈值>, <M11>, -1)` | 高波动年份信号强（§1.3 实证） |
| M21 | 分歧度构造 | `group_zscore(subtract(group_zscore(customer, industry), group_zscore(pro_customer, industry)), industry)` | **散户 vs 聪明钱的横截面分歧**（H1+H3 联合） |
| M22 | 覆盖率交集 | `customer_vol_imbalance_noto` × `customer_vol_imbalance_ise` 的加权 | 数据源交叉验证降噪 |
| M23 | 极端值截断后归一 | `group_zscore(winsorize(ts_mean(<M8>, 22), std=4), industry)` | 微盘极端比值抑制 |
| M24 | 排名型替代 | `group_rank(ts_mean(<M8>, 22), industry)` | 有界化（shortinterest3 的 `group_rank` 教训：可能毁信号） |
| M25 | 双尺度差 | `group_zscore(subtract(ts_mean(<M8>, 5), ts_mean(<M8>, 66)), industry)` | 短期失衡的**变化率**而非水平 |

---

## 4. 已验证的判负结论（勿重试）

| 结论 | 证据 | 适用范围 |
|---|---|---|
| **时序平滑（`ts_decay_linear` / `ts_zscore`）不是该数据集的换手杠杆** | M5 TO 137.56%→107.7%；M4 TO 仍 137.58% | 全字段族 |
| **换手必须靠横截面归一（`group_zscore`）** | M6 从 137.56%→14.32%（7.5 倍），且 2Y 从 −0.88 转 +1.54、margin 升 8.3 倍 | 全字段族 |
| **`broker_dealer_vol_imbalance` 无独立信息** | M3 与 M1 共线，相减 ≈ −2×customer（S −1.41 ≈ −0.92×1.53） | BD 侧全字段 |
| **OTM 变体聚合后全灭** | M9 S 0.58 / SUB 0.01 / 2Y 0.00 | `_otm` 组 |
| **换手原始值 137–140% 超平台上限一倍** | M1/M2/M4/M7 全部 107–140% | 未加归一的骨架 |
| **CW 不是该数据集的问题** | M6 / M8 的 `CONCENTRATED_WEIGHT` 均 **PASS**，`CLUSTER_TEST` 1.19–1.51（limit 1.58） | 全字段族（对照 shortinterest3 的字段级 CW 死锁） |

---

## 5. 当前差距与下一步

**OPTION 塔（0/3 已提交）最好成绩**：M6 `vR103A2w`（S 1.26 / F 0.54 / SUB 0.18 / 2Y 1.54 / ratio 0.889）。

| 闸 | 现状 | 目标 | 差距 |
|---|---|---|---|
| LOW_SHARPE | 1.26（M6）/ 1.60（M10） | 1.58 | **−0.32 / +0.02 ✓** |
| LOW_FITNESS | 0.54（M6）/ 0.71（M8） | 1.00 | −0.46 / −0.29 |
| LOW_SUB_UNIVERSE_SHARPE | 0.18（M6）/ 0.36（M8） | 0.55 | −0.37 / −0.19 |
| LOW_2Y_SHARPE | **1.54**（M6）/ 1.14（M10） | 1.58 | **−0.04 / −0.44** |
| CONCENTRATED_WEIGHT | PASS | — | ✓ |
| investability_ratio | 0.889（M6） | 0.70 | ✓ |

**两类候选的互补结构**：
- **M6（DD2）**：2Y 1.54 几乎过闸、ratio 0.889 最好，但 S/F/SUB 弱 ⇒ 短板在**信号强度**
- **M8（EE1）/ M10（EE3）**：S 1.52–1.60、F 0.59–0.71、SUB 0.35–0.36 大幅改善，但 2Y 掉到 0.80–1.14 ⇒ 短板在**近期持续性**

**FF 波（M11–M17）就是要把这两个优点拼起来**：核心假设是「M8 的聚合构造提供信号强度与 SUB，M6 的 `ts_mean` + `group_zscore` 提供近期稳健性与降噪」。

**效率判据**：M6 的 `eff = F/S = sqrt(|R|/max(TO,0.125))` = sqrt(0.026/0.1432) = **0.426**，低于 USA 成功模板 band（0.587–0.622，TO>12.5%）。M8 的 eff = sqrt(0.0269/0.125) = **0.464**，M10 = sqrt(0.028/0.2074) = **0.368**。三者都在 band 下方 ⇒ 按「eff 低换字段、eff 高 S 低调骨架」的判据，**目前仍在骨架调整区（eff 与 band 差 0.12–0.15，未到「一个数量级」的判死线）**，FF 波后若 eff 仍 <0.50 应转向 `option3` / `option40` 换数据集。

---

## 6. 相关记录

- 波 156（CC）：`wave_results` USA/156，7 条 key_findings
- 波 158（DD）：`wave_results` USA/158，8 条 key_findings
- 波 159（EE）：待落库
- 波 160（FF）：在飞
- 相关 skill：`wq-brain-ra-usa`
