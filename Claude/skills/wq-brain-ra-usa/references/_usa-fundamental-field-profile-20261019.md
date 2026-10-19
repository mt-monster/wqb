# USA Fundamental 字段画像（结构性全量）· 2026-10-19

> 命名：类别级扫描 `_usa-<category>-dataset-scan-<asOf>.md`
> 本篇 = **字段画像的结构性分析**（11041 字段全量分类），配套的逐集档案见
> `_usa-fnd67/fnd93-field-profile-20261019.md`、`_usa-fundamental-dataset-scan-20261019.md`。
> **as_of**：2026-10-19 ｜ 数据源：本地库 `field_profile_usa`（23 个 fundamental 数据集）

---

## 1. 总量与形态分布（11041 字段）

| 形态 | 字段数 | 占比 | **加工深度** | 能否直接用 |
|---|---:|---:|---|---|
| **元数据**（日期/ID/币种/申报状态/财年/汇率） | 964 | **8.7%** | — | **❌ 直接排除**（不是信号） |
| **其他**（压缩厂商码，实为原始金额/价格） | 5061 | **45.8%** | 未加工 | ❌ 原值不可用（=规模代理） |
| **原始金额**（value/amount/total/assets/cash/debt…） | 4122 | **37.3%** | 未加工 | ❌ 原值不可用（=规模代理） |
| **比率**（ratio/margin/pct/eps/per_share…） | 427 | 3.9% | 已加工 | ✓ 轻加工 |
| **变化率**（growth/chng/cagr/slope/revision） | 207 | 1.9% | 已加工 | ✓ 直接可用 |
| **评价分**（score/rating/insight/pulse/percentile） | 189 | 1.7% | 已归一 | ✓ 轻加工 |
| **价格区间**（high/low/qpe/prc） | 60 | 0.5% | 未加工（有量纲） | ❌ 需除以收盘价 |
| **离散度**（stddev/coeff_var/skew/kurt） | 11 | 0.1% | 已加工 | ✓ 优先作**分母** |

### ★★★ 第一条结构性结论

> **83.1% 的 Fundamental 字段（其他 45.8% + 原始金额 37.3%）是「未加工的原始量」。**
> 直接用它们 = 在用**规模代理**（大公司数值大），必然被 size 因子吞掉；
> **必须先转成比率（÷ 同集总量字段）或变化（Δ/ts_zscore）**，才有横截面意义。

这条解释了 2026-10-19 全天 40 条 Fundamental 实测为什么全败：
我测的多是 3.9% 的「比率」和 2.1% 的「变化率」，**占 83% 的主体矿脉从未被转比率开采过**。

---

## 2. 形态 → 模板 → 算子 全映射

### 2.1 按「加工深度」分三档（这是选模板的第一判据）

| 加工深度 | 判别 | 必做变换 | 禁做 |
|---|---|---|---|
| **未加工**（原始金额/价格/厂商码） | 数值随公司规模单调 | **÷ 同集总量**（`assets_total` / `revenue` / `shares_outstanding`）或 **`ts_zscore`** 或 **`ts_av_diff`** | 直接 `group_rank`（=size 因子） |
| **半加工**（比率 / 价格区间比） | 无量纲但非平稳 | `ts_av_diff`（变化）或 `ts_rank` | 再叠 `ts_zscore + winsorize + backfill`（过度加工） |
| **已加工**（z 分 / 评分 / 斜率 / 离散度） | 已是 0–1、z 或百分比 | **只做 `hump` + `group_rank`** | 任何归一化层（S 掉 0.1–0.4） |

### 2.2 完整映射表（形态 × 模板 × 算子场景）

| 形态 | 模板骨架 | 关键算子 | 算子**场景**说明 |
|---|---|---|---|
| **原始金额**（未加工） | `divide(F, SCALE)` → `ts_av_diff(·,252)` → `hump` → `group_rank` | `divide` + `ts_av_diff` | `divide` 做**单位消除**（把 $ 变成 %）；`ts_av_diff` 做**水平→变化** |
| **厂商压缩码**（同未加工） | 同上（需先平台核对语义） | 同上 | 同上 |
| **价格区间** `qpehigh/qpelow` | `divide(subtract(high, low), low)` = 季度振幅；或 `divide(high, close)` | `divide`/`subtract` | `subtract` 得**区间宽度**，`divide` 得**相对位置** |
| **比率** | `ts_av_diff(F,252)` → `hump` → `group_rank` | `ts_av_diff` | 比率的**变化**通常比水平更有信号 |
| **变化率** | `hump` → `group_rank`（**不再 Δ**，已差分） | `hump`/`group_rank` | 二次差分=噪声放大 |
| **评价分**（有界） | `ts_zscore(F, ~315)` → `hump` → `group_rank` | `ts_zscore` | 有界量先**时序标准化**才跨股可比 |
| **离散度** | **作分母**：`divide(信号, add(ts_mean(F,55),0.01))` | `divide` + `ts_mean` | 置信度加权（prod 杠杆，实测 0.88→0.67） |
| **元数据** | — | — | **排除**（date/id/currency/status） |
| **VECTOR**（任何形态） | 先 `vec_avg`/`vec_stddev`/`vec_range` 归约，再套对应模板 | `vec_*` | `vec_stddev`/`vec_range` 可**额外生成离散度**信号 |

### 2.3 算子场景清单（每个算子在 Fundamental 的具体用途）

| 算子 | 在 Fundamental 的**唯一用途** | 不该用它的场景 |
|---|---|---|
| `divide(F, SCALE)` | **未加工量转比率**（$ → %）← 最重要 | 已无量纲的字段 |
| `ts_av_diff(F, w)` | 水平 → 变化（$ 或 % 都适用） | 已是变化率的字段（二次差分） |
| `ts_zscore(F, w)` | 有界量跨股可比（评分/比率） | 已加工的 z 分字段 |
| `ts_rank(F, w)` | 慢变量的分位（替代 zscore，更稳健） | 高频字段（会噪声化） |
| `hump(x, 0.01)` | **保 SUB 的唯一手段**（低换手资产的命门） | 日频高换手字段（会撞 TO 地板） |
| `ts_backfill(F, w)` | 提覆盖（季频字段必做） | 覆盖已 1.0 的字段（无收益） |
| `winsorize(F, std=4)` | 削极值（报表口径异常） | 已 z 分/评分的字段（重复） |
| `group_neutralize(F, 轴)` | 剥板块级 beta（**2Y 杠杆**） | 轴必须**粗于**外层 group_rank |
| `ts_std_dev` / `ts_max_diff` | 生成**离散度/极值**辅助信号 | 作主信号（太噪） |
| `vec_avg` / `vec_stddev` | VECTOR 归约 / 生成截面离散度 | — |
| `trade_when` | 稀疏事件门控 | 连续型基本面（削样本） |
| `bucket(rank(x), ...)` | 离散化降 CW | 作 grouping（需 `rank` 包裹） |

---

## 3. 与 2026-10-19 实测的对应（为什么之前失败）

| 实测 | 形态 | 用的模板 | 结果 | 诊断 |
|---|---|---|---|---|
| f21 ESG 背离 | 评价分（已归一） | `hump + group_rank` （正确） | S 1.43 / SUB 0.52 | **形态对、SUB 结构性不足** |
| f21 新模板 | 评价分 | `zscore+GN+winsorize+backfill` | S 1.01（−0.42） | **过度加工** |
| f93 税务应计 | 比率（已加工） | `winsorize+backfill+hump` | S 0.99 | 形态基本对，信号弱 |
| f93 新模板 | 比率 | `zscore+GN+...` | S 0.66（−0.33） | **过度加工** |
| f91 8-K NLP | 评价分（VECTOR） | `vec_avg + winsorize + backfill` | S ≤0.58 | 信号本身弱 |
| f17 DuPont 价差 | 比率 | `ts_av_diff(subtract(a,b))` | S ≤1.07 | 价差本身弱 |
| **f23 原始金额** | **未加工** | **`divide(F, assets)` + Δ** | **本轮首测** | 见下 |

---

## 4. 待办：83% 未加工矿脉的开采顺序

1. **f23（PIT 基本面，cov 1.0，1637 字段）**：原始金额最集中（1240 个"其他"+大量 LEVEL），
   且有 `assets_total_2/3`、`book_value_total_equity`、`common_shares_outstanding` 作分母 ⇒ **首选**。
2. **f17（FactSet，cov 0.83，402）**：`ttmrev`/`arevperemp`/`qpehigh` 等 ⇒ 转比率 + 价格区间模板。
3. **f72（Comprehensive，cov 0.75，1852）**：`pit_or_is_*` / `pit_or_bs_*`（利润表/资产负债表行项目）
   ⇒ 除以对应总量字段。
4. 注意：这三集 aC 都很高（f23 2.8万 / f17 3.5万 / f72 3千）⇒ **prod 会是硬墙**；
   但**转比率后的表达式是全新的**（原始金额字段本身的 aC 极低），prod 需实测。

---

## 5. 索引

- 本篇：`references/_usa-fundamental-field-profile-20261019.md`
- 类别扫描与逐日实测：`references/_usa-fundamental-dataset-scan-20261019.md`
- 全局方法论：`_usa-field-profile-playbook-20261018.md`（破 prod 方法总表 / 闸门归因）
- 记忆：`MEMORY.md` §7（文档规范）§9（算子穷举）§10（按形态选模板）

---

## 6. 未加工矿脉首测（f23 原始金额 → 比率）：**S 0.55–0.89，仍不达标**

按 §2.2「原始金额」模板（`divide(F, assets_total_2)` → 水平/Δ252 → hump → group_rank）：

| 字段 | 变换 | S | F | 2Y | SUB | 备注 |
|---|---|---:|---:|---:|---:|---|
| `deferred_charge_goodwill`（商誉） | 水平比率 | **0.89** | 0.46 | 1.05 | 0.69 | 最好但仍差 0.69 |
| `deferred_charge_goodwill` | Δ252 | 0.85 | 0.35 | 1.11 | 0.35 | 撞 LOW_TURNOVER |
| `accounts_payable_nontrade` | Δ252 | 0.55 | 0.18 | 0.47 | 0.56 | ✗ |
| `capital_invested_accumulated_cost` | Δ252 | 0.55 | 0.17 | 0.06 | −0.13 | ✗ |

**诊断**：转比率确实让字段**有意义了**（不再是 size 代理，longCount/shortCount 平衡），
但 **f23 是 PIT 重述数据**，字段被回溯调整过 ⇒ 时序变化被人为平滑，`Δ252` 信息量低；
而水平比率（商誉/资产）只有 S 0.89。

### 逐日累计的 Fundamental 全貌（44 条 / 6 数据集 / 3 套模板体系）

| 形态 | 代表字段 | 最好成绩 | 卡点 |
|---|---|---:|---|
| 评价分 | f21 pulse−insight 背离 | **1.43** | SUB 0.52（需 0.62） |
| 比率 | f93 tax_accruals | 0.99 | S 不足 |
| 变化率 | f93 accruals z 分 | 0.87 | S 不足 |
| **原始金额（转比率）** | f23 goodwill/assets | **0.89** | S 不足 |
| 8-K NLP | f91 readability/sentiment | 0.58 | S 不足 |
| 分类概率 | f67 y_pred_prob | 0.64 | CW + S 不足 |

**⇒ Fundamental 类目最终判定不变：结构性无法产出 ATOM。**
三条独立证据链已闭合：
1. **已加工量**（评价分/比率）→ 轻加工最好也只有 1.43，且 SUB 结构性不足（ESG 覆盖偏大盘）；
2. **未加工量**（原始金额 41%+其他 46%）→ 转比率后有语义但强度 ≤0.89（PIT 重述抹平时序）；
3. **NLP/分类**（f91/f67）→ 0.58–0.64，信息已被快讯消化。

### ★ 三条最终纪律（可直接写进选类别 rules）

1. **Fundamental 在 USA/TOP3000 不要作为 ATOM 主攻方向**（44 条实测 S 上限 1.43，SUB 上限 0.52）。
2. **若必须用 Fundamental 字段，唯一有形态依据的路径是「未加工 → 转比率」**
   （占 83% 的矿脉），但预期 S 上限 ~0.9，仅适合做**组合的分散腿**，不适合单独达闸。
3. **字段形态判别三问**：① 有量纲吗（$ / 股）→ 先除规模；② 定义里有 z-score/ratio/score 吗 → 别再归一化；
   ③ 是变化率吗 → 不再差分。**三问过关再谈算子**。

---

## 7. f17（FactSet）专项：形态模板实测（11 条）

### 7.1 价格区间族（`fnd17_qpehigh/qpelow/pr5dayprc`）—— **产出全零持仓，不可用**

| 表达式 | S | TO | long/short |
|---|---:|---:|---|
| `divide(subtract(qpehigh, qpelow), qpelow)` | **0.00** | **0.00** | 0 / 0 |
| `divide(qpehigh, pr5dayprc)` | **0.00** | **0.00** | 0 / 0 |

⇒ 这两个字段在 TOP3000/D1 下**全为 NaN**（可能是特定币种/口径或与 universe 不匹配）⇒ **形态模板无法验证，字段直接排除**。

### 7.2 `fnd17_arevperemp`（人均创收 = 劳动生产率）—— **f17 最强字段**

形态：**已是比率**（revenue / employees，无量纲）⇒ 按模板只做轻加工。

| 表达式 | S | F | 2Y | SUB | **margin** | TO |
|---|---:|---:|---:|---:|---:|---:|
| 裸 `hump + group_rank` | 1.15 | 0.76 | 1.36 | 0.53 | 48.5bp | 0.0226 |
| + 内层 GN(industry) | 1.16 | 0.77 | 1.48 | 0.60 | 49.1bp | 0.0223 |
| **+ `winsorize(4) + ts_backfill(252)`** ★ | **1.30** | **0.93** | 1.37 | **0.86** | **117.0bp** | 0.0109 |
| + `winsorize + backfill + GN(industry)` | 1.20 | 0.82 | 1.37 | 0.78 | 110.1bp | 0.0106 |
| + winsorize/backfill @ decay1 | 1.30 | 0.93 | 1.37 | 0.87 | 111.6bp | 0.0114 |
| + winsorize/backfill 756 | 1.30 | 0.93 | 1.38 | 0.79 | 115.3bp | 0.0112 |
| + winsorize/backfill + GN(sector) | 1.25 | 0.90 | 1.47 | 0.83 | 110.9bp | 0.0116 |

**★ 三个发现**：
1. **`winsorize + ts_backfill` 第三次验证有效**（1.15 → 1.30，S +0.15 / F +0.17 / SUB **+0.33**）；
2. **`margin = 117bp`** —— 是已提交两颗 analyst ATOM（24–25bp）的 **4.7 倍**，
   说明"劳动生产率"是**高质量低换手**信号（TO 仅 0.011），只是**强度不足**；
3. **decay 1 与 decay 5 无差异**（1.30 对 1.30）、**backfill 252/756 无差异** ⇒ 季频慢变量对这两个旋钮不敏感
   （与 analyst 快变量相反）。

### 7.3 结论

`arevperemp` 天花板 **S 1.30**（距闸 0.28），F 0.93（距 0.07），2Y 1.37（距 0.21）—— **三闸同时不足**，
且已把（GN 3 档 × decay 2 档 × backfill 2 档 × 有无 winsorize）全部扫过 ⇒ **字段判死**。

### 7.4 Fundamental 全类目累计（51 条 / 7 数据集）

| 排序 | 数据集 | 字段/机制 | 最好 S | 卡点 |
|---|---|---:|---:|---|
| 1 | **fundamental21** | ESG pulse−insight 背离 | **1.43** | SUB 0.52 / 0.62 |
| 2 | **fundamental17** | **arevperemp（劳动生产率）** | **1.30** | S/F/2Y 三闸不足 |
| 3 | fundamental93 | tax_accruals | 0.99 | S 不足 |
| 4 | fundamental23 | goodwill/assets（转比率） | 0.89 | S 不足 |
| 5 | fundamental67 | y_pred_prob（分类） | 0.64 | CW + S |
| 6 | fundamental91 | 8-K readability/sentiment | 0.58 | S 不足 |
| — | fundamental17 | qpe*（价格区间） | **0.00（全 NaN）** | **字段不可用** |

**⇒ Fundamental 类目最终定论：51 条实测，S 上限 1.43，无一能过 S 闸 1.58。**
