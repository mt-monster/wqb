# pv20 IBES 面判死证书（2026-11-12）

> 用户指令：「转 pv20 的 624 个 IBES 字段」→「按 metric 分层扫剩余 10 个 metric，各取 ac 最高字段做水平矩，先跑 10 臂再决定是否收档」
> 两波 14 臂：首轮 4 臂（ebi/roe）+ 分层 10 臂（bps/ebt/ent/eps/gps/nav/net/opr/pre/sal）｜**0 ERROR**

## 一、字段画像（先搞清结构，再谈信号）

`pv20` 共 **681 字段**：678 MATRIX + 3 GROUP。其中 **624 个是 IBES 启发式衍生特征**：

```
pv20_<metric>_indicator_<1-4>_feature<0-12>
metric ∈ {bps, ebi, ebt, ent, eps, gps, nav, net, opr, pre, roe, sal}   (12 个)
```

| 维度 | 取值 | 推断含义（**未获官方确认**） |
|---|---|---|
| `metric` | 12 种会计科目 | bps=每股账面 / ebi=税前利润 / ebt=税前 / ent=企业价值 / eps=每股收益 / gps=每股销售 / nav=净资产 / net=净利润 / opr=营业利润 / pre=税前 / roe=净资产收益率 / sal=销售收入 |
| `indicator` | 1-4 | **大概率是财年跨度**（FY1-FY4）；`indicator_4` 的描述出现过 "Fiscal Year 4" 与 "median 4 weeks ago" |
| `feature` | 0-12 | 13 种启发式提取的特征（**语义全缺**） |

### ★关键缺陷：字段描述**没有语义**

三个真实样例：

| 字段 | 官方 description |
|---|---|
| `pv20_ebi_indicator_1_feature3` | `Feature 3 from Indicator 1 in IBES Pre-tax Profit module` |
| `pv20_roe_indicator_2_feature7` | `[Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature]` |
| `pv20_ebi_indicator_4_feature2` | `[... Pre-tax Profit] [Fiscal Year 4] [median 4 weeks ago]` |

⇒ **无单位、无方向、无经济含义**，只有模块名 + 财年 + 一个未知 feature 编号。
⇒ 按「机制优先」清单，这 624 个字段**无法填写「机制声明」栏** ⇒ 只能作为廉价探针，不能作为主轴。

### 拥挤度分布（ac）

| metric | 字段数 | ac 总和 | 最高 ac |
|---|---:|---:|---:|
| **ebi** | 52 | **199** | **54** |
| **roe** | 52 | 71 | 43 |
| gps | 52 | 46 | 9 |
| pre | 52 | 43 | 16 |
| ebt | 52 | 36 | 6 |
| eps | 52 | 32 | 9 |
| opr | 52 | 31 | 9 |
| net | 52 | 24 | 4 |
| ent | 52 | 23 | 9 |
| bps | 52 | 17 | 3 |
| nav | 52 | 11 | 8 |
| sal | 52 | 9 | 4 |

`indicator` 维度：1（ac 总和 261）> 2（123）> 4（93）> 3（65）
⇒ **拥挤度高度集中在 `ebi` + `indicator_1`**（即税前利润 FY1），其余 metric 几乎是冷门区。

## 二、首轮 4 臂（ebi/roe，最热字段）

| 臂 | 字段 | id | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| 水平 zscore252 | `pv20_ebi_indicator_1_feature3`（ac 54，最热） | `WjlQN33G` | 0.34 | 0.14 | 7.1% | 0.02 |
| 变化 Δ66 | 同上 | `leaO7EEA` | 0.11 | 0.03 | 8.3% | 0.16 |
| 水平 zscore252 | `pv20_roe_indicator_2_feature7`（ac 43） | `akaZNee9` | 0.12 | 0.03 | 4.7% | −0.29 |
| 水平 zscore252 | `pv20_ebi_indicator_1_feature9`（ac 32） | `d5aVnY3X` | 0.36 | 0.15 | 7.0% | 0.07 |

⇒ 最热字段（ac 54）的水平矩只有 **0.34**，变化矩 0.11 ⇒ **crowded 字段已被挖穿**。

## 三、分层 10 臂（各 metric 取 ac 最高字段，水平矩）

| metric | 字段 | id | S | F | TO | 2Y | lc/sc |
|---|---|---|---:|---:|---:|---:|---|
| bps | `pv20_bps_indicator_3_feature7`（ac 3） | `wpoxLPQQ` | **−0.47** | −0.23 | 4.4% | −0.32 | 93/264 ⚠ |
| opr | `pv20_opr_indicator_4_feature2`（ac 9） | `mLaRZ1d9` | **0.39** | 0.31 | 2.0% | 0.97 | **13/101** ⚠ |
| nav | `pv20_nav_indicator_3_feature12`（ac 8） | `P05av8PM` | −0.25 | −0.09 | 5.8% | 0.00 | 93/262 ⚠ |
| net | `pv20_net_indicator_1_feature11`（ac 4） | `pwar8ZWb` | −0.15 | −0.04 | 5.7% | 0.18 | 96/263 ⚠ |
| pre | `pv20_pre_indicator_1_feature10`（ac 16） | `rK7gAV9o` | −0.15 | −0.04 | 5.5% | 0.32 | 95/263 ⚠ |
| sal | `pv20_sal_indicator_1_feature3`（ac 4） | `P05av8xM` | −0.15 | −0.04 | 7.0% | −0.06 | 96/263 ⚠ |
| eps | `pv20_eps_indicator_3_feature8`（ac 9） | `oma5Vrab` | −0.09 | −0.02 | 6.4% | −0.41 | 96/262 ⚠ |
| gps | `pv20_gps_indicator_2_feature8`（ac 9） | `d5aVdo9g` | −0.07 | −0.01 | 5.9% | −0.13 | 95/263 ⚠ |
| ebt | `pv20_ebt_indicator_1_feature0`（ac 6） | `QP0kEg0X` | 0.05 | 0.01 | 4.7% | −0.33 | 93/264 ⚠ |
| ent | `pv20_ent_indicator_2_feature10`（ac 9） | `YPaKQJav` | 0.05 | 0.01 | 8.4% | 0.52 | 88/244 ⚠ |

**★第二个致命缺陷：持仓严重不对称。**
8 个 metric 的 lc/sc 落在 **88-96 / 244-264**（空头是多头的 2.7-2.8 倍），
`opr` 更是 **13/101**（多头仅 13 只）。这是 `nan ON` 在稀疏 IBES 特征上填 0 造成的**系统性空头偏置**，
与 BE99 遇到的完全同构 ⇒ 这些读数**大部分是偏置账面，不是可交易信号**。

## 四、判死证书

### 覆盖度声明

| 维度 | 已覆盖 | 总 |
|---|---:|---:|
| **metric** | **12 / 12** | 12 |
| 矩 | 水平（12 个 metric 全测）+ 变化 Δ66（ebi 1 个） | — |
| `indicator` | 已测字段覆盖 ind 1/2/3/4 | 4 |
| `feature` | 已测字段覆盖 feat 0/2/3/7/8/9/10/11/12 | 13 |
| 设置档 | nan ON / INDUSTRY / decay4 / TOP500 单档 | — |

### 判决

1. **机制层：无机制可声明。** 624 个字段的描述不含任何经济含义（仅模块名+财年+feature 编号），
   无法填写「机制声明」与「文献来源」栏 ⇒ 按机制优先清单，**不得作为主轴，也不得据此做数据集级判死**。
2. **信号层：12 个 metric 的水平矩全测，最高 |S| = 0.47（bps，负号），正号最高 0.39（opr）。**
   ebi（ac 54）0.34、ebi_f9（ac 32）0.36、roe（ac 43）0.12 ⇒ **拥挤度与产出率正相关，最热的已被挖穿**。
3. **数据层：持仓严重不对称（88-96/244-264，opr 13/101）** ⇒ 大部分读数来自 nan ON 空头偏置，
   真实可交易性还要再打折。
4. **时间维：2Y 全部 ≤0.97**，多数为负或接近零，无任何近端优势。

**⇒ 结论：`pv20` IBES 面 624 字段，在 DEU/TOP500/D1 的「水平矩 × INDUSTRY × nan ON」口径下，天花板 |S| ≈ 0.47，且伴随系统性空头偏置。**

### 证书等级

**`数据集级 PROVISIONAL`** —— 理由是覆盖未穷尽：
- 只测了「水平矩」与 ebi 一个「变化矩」，**未测**：比值矩（两 metric 相除）、`indicator` 间价差（FY1-FY4 期限结构）、
  `feature` 间组合、nan OFF 档、SUBINDUSTRY/STATISTICAL 档、decay 0/8。
- 但**先验极低**：字段无语义 ⇒ 任何额外组合都只能靠撞，且 12 个 metric 的独立水平矩已给出同一结论（≤0.47）。

## 五、★最有价值的发现：这批字段的真实身份

对比 `analyst7` 同名字段（如 `est_12m_ebi_median`，描述完整、cov 0.73、ac 93）与 `pv20` 的 IBES 特征：

| | analyst7 `est_12m_ebi_*` | pv20 `pv20_ebi_indicator_*_feature*` |
|---|---|---|
| 描述 | 完整（"Mean analyst estimate of EBIT regarding the next 4 quarters"） | **无语义标签** |
| cov | 0.73 | **0**（平台报 0） |
| 数据 | 有（实测 lc 正常） | 有（TO 5-8% 干净） |
| ac | 8-127 | 0-54 |
| 塔归属 | **ANALYST（已点亮 6 颗）** | **PV（未点亮 0 颗）** |

⇒ **pv20 的 IBES 特征大概率是 analyst7 同源数据的非线性衍生**（描述写 "heuristically extracted"），
  换了个塔归属（PV）但信息内容同源。
⇒ 这解释了为什么它的信号天花板（0.47）远低于 analyst7 已出货件的水平 —— **同源信息的低质量副本**。
⇒ 也解释了为什么 ac 集中在 ebi：**ebi 是 analyst7 最高产的分支**（`est_12m_ebi_lowerednum_4wks` ac 127、`est_12m_ebi_mean` ac 93）。

## 六、塔归属套利判断（此前曾被当作下一方向）

此前档案记载「pv20 塔归属套利：招牌 PV、内容 IBES，可绕过已点亮塔冻结，塔倍率 1.6」。

**本轮实测否定该套利**：
- 塔归属确实在 PV（未点亮），**技术上合法**；
- 但**信息质量不足以出货**（天花板 0.47 vs 闸线 1.58，差 1.11），
  换塔归属**不改变信号强度**——套利只解决「能不能提交」，不解决「信号够不够」。

⇒ **与 earnings6 的教训完全一致**：「放宽覆盖救不了信号弱」。

## 七、pv20 数据集最终定位

| 面 | 字段数 | 天花板 | 状态 |
|---|---:|---:|---|
| **流动性/成交额面**（57 字段） | 57 | **S 1.37** | 已 7 波 62 臂穷尽，margin 不足 |
| **IBES 会计特征面**（624 字段） | 624 | **S 0.47** | 本档判死（provisional） |

⇒ **pv20 的 681 个字段，两个面都已探到极限。** PV 塔维持未点亮。