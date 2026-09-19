# Base Payment 与 Value Factor / Weight Factor 的关系

生成时间：2026-09-12 | 账号 `MT38799` | 数据源：`GET /users/self/consultant`、`GET /users/self/activities/base-payment`、`/users/self/activities/submissions`（实时平台拉取）

---

## 0. 一句话结论

**VF 决定 Base Payment 的档位（上下限），WF 不直接进 Base Payment——WF 决定的是季度奖。**
两者同源（都由 alpha 的 OS 实盘表现喂养），所以长期同向变动，但在日薪这个口径上，**VF 是乘数级变量、WF 几乎无贡献**。

---

## 1. 你当前的实测值

| 项 | 值 | 来源 |
|---|---|---|
| Value Factor (vf) | **0.5**（初始值，未上调） | `consultant.leaderboard.valueFactor` |
| Weight Factor (wf) | **0.02** | `consultant.leaderboard.weightFactor` |
| meanProdCorrelation | 0.669（逼近 0.7 硬闸） | `consultant.leaderboard` |
| meanSelfCorrelation | 0.3658 | 同上 |
| dataFieldsUsed / submissionsCount | 159 / 74 | 同上 |
| superAlpha 提交数 | 9（meanProdCorr 0.6735） | 同上 |
| 顾问起始日 | 2025-08-05 | `consultant.dateStarted` |

### 实际 Base Payment（41 个有收入日）

| 口径 | 值 |
|---|---|
| 区间 | 2025-09-05 → 2026-09-10，共 **41 天** |
| 累计 | **$63.98** |
| 日均 | **$1.56**（中位 $1.52） |
| 单日区间 | **$1.23 – $1.89** |
| 昨日（2026-09-10） | $1.78 |
| 本期（09-01→10-31） | $11.60 |
| 上期（07-01→08-31） | $45.44 |

**关键观察：41 天、跨度 13 个月，全部落在 1.23–1.89 这个极窄区间。**vf 从未离开 0.5 → 这就是"档位锁死"的直接证据：不是你某颗 alpha 好不好的问题，是**这个档的上下限就在 1.2–1.9**。

---

## 2. VF 如何作用于 Base Payment

社区/官方材料口径（BRAIN 中文论坛《顾问收入组成及计算》，官方材料 + 个人经验整理，**非平台公开权威公式**）：

> Value Factor：计算逻辑用 BRAIN 表达式来说就是 `group_rank(score, value_factor)`，即对当日有提交的顾问**根据不同 Value Factor 进行分组，你的 VF 决定了你当日 base payment 的上限和下限**。顾问 VF 初始值 0.5，约三个月首次更新。

即 **VF 不是连续乘数，是"定档"**——先把顾问按 vf 分桶，桶决定当日能拿到的区间，桶内再由 Quality / Quantity / Self-Growth 决定落点。

### 跨 vf 档位的实证（论坛公开案例）

| vf | 日均 Base Payment | 备注 |
|---|---|---|
| 0.5（初始） | ~1.2 – 6.0/颗 | 单颗下限 1.2；低相关"新奇"alpha 可到 $6.07 |
| 0.97 | **~$35/天** | 主要靠 Super Alpha（fit>5、prod<0.7 → ≥$30） |
| 0.99 | **≥$60/天**，好时 $80+，偶破 $100 | 同样的 SA 从 $30 抬到 ≥$50 |
| 1.00 | **$104.91**（1 颗 SA + 1 颗 regular fit 3.17） | 历史新高 |

> 注意 0.97 → 0.99 只差 0.02，同一颗 SA 的报酬从 $30 跳到 ≥$50（+67%）。**vf 接近 1 时曲线的边际斜率极陡**，这不能用 `payment ∝ vf^k` 解释（k 需 ≈25），说明是**分档 + 档内阈值**机制，不是幂律。

### 你的位置

vf = 0.5（最底档），日均 $1.56。对照论坛"1.5USD 大法"：
- 当日只交 1 颗、base ≥ **1.5** → 该 alpha 质量不错
- 只有 **1.2** → 质量差，**会拉低 vf**

你的 1 提交日均 = **1.44**，中位 1.52 → **刚好压在合格线附近偏下**，与 vf 长期卡 0.5 完全自洽。

---

## 3. WF 如何作用（不进 Base Payment）

社区口径明确把 WF 归到**季度奖**：

> 2. 季度薪酬（Quarterly Payment）**关键要素：Weight Factor 和 Value Factor**。Weight 需要时间积累——随着你提交的 Alpha 被选中进入实盘由基金经理使用，**越有价值的 Alpha 获得的 Weight 会越来越高**。计算方法主要取决于 Alpha 在滚动最近两年内的样本外表现。

| 收入项 | 范围 | 核心决定因素 |
|---|---|---|
| **Base Payment** | $1–120/天（Regular $1–60 + SuperAlpha $1–60） | **VF**（定档）+ Theme + Quality/Quantity/Self-Growth |
| **Quarterly Payment** | $100–25,000/季（按 Genius Level 分档） | **WF + VF** + 近两年 OS 表现；需季度内 ≥20 天有提交 |

→ **wf = 0.02 意味着几乎没有被分配实盘资金权重**，季度奖会贴在 Gold 档地板（$100–200/季）。WF 起量的前置条件正是上一轮讲的：**CSAP 过阈值**。

---

## 4. 档内四因子：你的实测 Quantity 曲线

Base Payment 档内由四因子决定：**Quantity / Quality / Self-Growth / Theme（Theme 是 Quality 的乘数）**。

用你的 41 天数据 × 当日提交数做配对（提交数来自 `/activities/submissions`）：

| 当日提交数 | 天数 | Base 均值 | 区间 |
|---|---|---|---|
| 1 | 22 | **1.44** | 1.23–1.64 |
| 2 | 4 | **1.53** | 1.48–1.56 |
| 3 | 6 | **1.69** | 1.54–1.80 |
| 4 | 4 | **1.77** | 1.67–1.83 |
| 5 | 5 | **1.82** | 1.72–1.89 |

**结论：强次线性。**交 5 颗只比交 1 颗多 **+26%**，边际约 **+6.5%/颗**。这直接印证论坛那句"为什么交 1 个是 1.6，交 2 个不是 3.2"，也印证"Quantity 每日上限 4 个、新人加成不明显"（4→5 只 +0.05）。

→ **在 vf=0.5 档内，堆数量是低 ROI 动作。**

---

## 5. 杠杆排序

| 优先级 | 动作 | 影响的因子 | 预期 |
|---|---|---|---|
| **P0** | 退役 27 颗负 OS alpha（19 颗双负优先） | VF（近 3 月各区组合表现） | 直接抬 CAP/CSAP → 推动 vf 从 0.5 上调。**唯一能把 1.2–1.9 档位整体抬升的动作** |
| **P0** | 把 meanProdCorrelation 0.669 降到 0.55 以下 | Quality（档内落点） | 同档内单颗 base 从 1.4 抬向 1.8+；论坛实证 corr=0 的单颗可到 $6.07 |
| P1 | 跨区域/跨数据集分散（停止 MEA 投入、转向 DEU/CHN 空白金字塔） | Quality + VF | 区域组合表现等权计入 vf |
| P1 | 踩当期 Theme（Quality 的**乘数**） | Quality × Theme | 档内最大单点杠杆 |
| P2 | 每日 1→4 颗（不要到 5） | Quantity | 仅 +23%，边际递减，不必强求 |
| 长期 | 等 OS 实盘积累 + CSAP 过阈值 | WF | 解锁季度奖，与日薪无关 |

---

## 6. 方法与局限

- **公式非官方**：VF/WF 的作用机制来自 BRAIN 中文论坛整理（作者声明"官方材料结合个人经验，不构成权威解答"）+ 平台 leaderboard 字段反推。平台**未公开** Base Payment 的确切公式。
- **单档样本**：你 vf 恒为 0.5，无法从自身数据反推跨档弹性；跨档数字全部来自论坛他人案例，个体方差极大（有人 vf 0.99 日均 60，有人 100+）。
- **Quantity 曲线有混淆**：提交多的日子往往也是研究投入高的日子，Quality 可能同时更高，+26% 是上界估计。
- 复算脚本：`logs/_tmp_base_payment_probe.py`（consultant + base payment）、`logs/_tmp_bp_vs_sub.py`（提交数配对），需 MCP venv：`world-quant-brain-mcp/.venv/Scripts/python.exe`。
