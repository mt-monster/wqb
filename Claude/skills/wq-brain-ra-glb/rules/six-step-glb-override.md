# GLB 六步纵深骨架 · 本区覆盖（override）

> **as_of**：2026-10-28 ｜ **来源**：GLB 战役 w92–w151（~75 条仿真派发，平台权威校正 526 条）
> **层级**：本文件覆盖主 skills [`wq-brain-ra-pipeline`](../../wq-brain-ra-pipeline/references/_six-step-core.md) 的同名条目；
> **锁定项不可放宽**（禁混信号、Mode B 主闸下限、平台线、窗口白名单、提交前用户确认）。
> **实证明细** → [`../references/_glb-zero-tower-gate-20261028.md`](../references/_glb-zero-tower-gate-20261028.md)（专题，含逐颗 alpha id）。

---

## ① 六法体检 · 本区覆盖

- **入场**：**active，但不是「已挖穿」** —— 见下面「入场裁决修订」。
- **字段体检**走主 skills 的 L1；**GLB 补充口径**：平台 `coverage` 可能造假（实测 earnings6 / news48 / option1 /
  analyst45 / macro27 的 meta 都写 `coverage=0`，但字段真实存在且可回测）⇒ **覆盖度以逐年记录判别，不信 meta**
  （见 [`brain-alpha-robustness`](../../brain-alpha-robustness/SKILL.md) 的「近十年逐年验」条）。

### ★ 入场裁决修订（2026-10-28）—— 推翻「GLB 已挖穿、不要开 atom 主信号」

旧结论（2026-09-27，Claude 记忆）：**GLB 已挖穿**（41 族判死覆盖所有类别），获胜字段本身已被 prod 饱和闸拦 ⇒
「不要再开 atom 主信号；转区或做 SuperAlpha」。

**本轮证据推翻其中的「获胜字段已被 prod 饱和」这一半**：

| 旧结论 | 2026-10-28 实测 |
|---|---|
| 获胜字段已被 prod 饱和 ⇒ 无法在 GLB 产出可提交 alpha | **134 颗合规且 fRA=0 的候选**（覆盖 10 个未点亮塔），其中 4 颗已通过全部四道闸（prod / 塔位 / 互相关 / 稳健性） |
| GLB 只能转区 | **零塔门控 × dl_riskfree 信号腿**在 7 个零塔域上全部产出可提交候选 ⇒ **GLB 仍有活矿** |

⇒ **修订后的口径**：
- **仍成立**：直接拿「已被 prod 饱和的获胜字段当信号腿」的路（PV 的 `mean_high_price_return_30m_pre_close_2` /
  `corr_last_trade_price_with_volume`、RISK 域借券费率、techindi `predicted_first_quantile` 系）**是死路**，
  不要在这些字段上开 atom 主信号。
- **不成立**：「GLB 整体已挖穿、应转区」。
- **本区活矿的形态**（⇒ 步 2/4 直接照此设计）：**零塔数据集当门控腿 × dl_riskfree 当信号腿**。
  7 个零塔域（FUNDAMENTAL / INSTITUTIONS / EARNINGS / SENTIMENT / SOCIALMEDIA / NEWS / RISK）各 3–6 颗可用。
- **选波时的动作**（不可省）：**先读本波数据集所在组合的分支卡**（`references/<类别>.md`）的「避」段与
  「prod 已测（低于上限）」存量表 ⇒ **命中即禁入 quota；存量里 prod 已确认低于上限的候选优先复用**。
  2026-10-28 的教训：未读分支卡直接开波 ⇒ **~44/75 条派发是重复劳动（约 60%）**。

---

## ② 组装 · 本区覆盖

- **两条铁律不变**：`emotion` 系**全排除**；`anl15` 按**精确表达式（sha1）封禁**，不按前缀通配。
- **★ 第三条铁律（2026-10-28）**：**零塔字段不得作信号腿** —— ANALYST（16 条）/ INSIDERS（4 条）/ MACRO（4 条）
  三个从未测过的零塔域全灭 ⇒ 零塔字段**只当门控腿**。理由：强度来自**跨集门控**（门控腿给经济子集、
  信号腿给截面基座），零塔字段自身不需要有 alpha。
- **★ 设置按信号族分档**（区域默认档只适用于旧族）：

| 信号族 | universe | neutralization | decay |
|---|---|---|---|
| 零塔门控 × dl_riskfree | **MINVOL1M** | **FAST** | 6 |
| PV 尾盘反转（high-price 路径） | **MINVOL1M** | FAST | 6 |
| techindi 连续回归输出 | MINVOL1M | STATISTICAL | 10 |

- 区域默认档（TOPDIV3000 / STATISTICAL / decay 2）是 2026-09-19 **按旧族过闸率**校准的 ⇒ **新族不得直接套用**。
  ⚠ 区域面板（`SKILL.md` 生成块）当前仍显示默认档 ⇒ **以本表为准**；面板与本表冲突时读本表。

---

## ③ 归因 · 本区覆盖

- 沿用主 skills。**GLB 补充**：GLB 的 `LOW_SUB_UNIVERSE_SHARPE` 是**比值闸**（系数逐区实测），
  且 GLB 有三个**区域闸**（`LOW_GLB_AMER_SHARPE` / `LOW_GLB_EMEA_SHARPE` / `LOW_GLB_APAC_SHARPE`）——
  **区域闸卡住的第一动作是换中性化到 `FAST`**（本区第三次独立验证：8 颗 PV 候选 INDUSTRY→FAST 后 fRA 1→0）。

---

## ④ 破闸杠杆 · 本区覆盖

| 卡点 | 本区解法 | 证据 |
|---|---|---|
| **区域闸**（AMER/EMEA/APAC） | **换 `FAST` 中性化** | `WjOQX8rj` / `kqNrmA9g` / `LLMaXwv6`：INDUSTRY→FAST，fRA 1→0，12 硬闸全 PASS |
| **CW（`CONCENTRATED_WEIGHT`）** | **换信号腿类型**（VECTOR → MATRIX），不要修 CW | 40 颗 `rsk60_offer` 全卡 CW；六种改法（`group_rank` 外层 / 幂律压尾 / 换轴族 / 换字段组合 / 换中性化+截断 / 换 VECTOR 字段）全败 |
| **prod 墙** | 改**持仓类**（换字段/换概念/残差化/换分组轴/`trade_when` 分层），别只改时序类 | 见专题 §1 / §3；**prod 跟持仓不跟信号** ⇒ 破闸后必须重测 prod |
| **2Y（ladder）** | 读平台 `checks[].limit` 判定，**别用字面量** | GLB 实测 limit 高于跨区下限（本区 8 颗候选 2Y 落在下限之下仍 FAIL ⇒ 见 `config.PLATFORM_CHECK_LINES`） |

---

## ⑤ 算子穷举 · 本区覆盖

- **子集门控只修 prod / robust、不造强度** —— 未门控基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.0（沿用主 skills）。
- **GLB 补充**：`group_rank` 外层在 CW 类候选上**会同时拖塌 S**（实测 S2.75→1.46）⇒ 换外层不是 CW 的解法。

---

## ⑥ 终验 · 本区覆盖

- **prod 分布**：本区 prod **在同一 category 内差异极大**（PV 域实测 0.694 ~ 0.9898；RISK 域三个数据集全在 0.80–0.94）
  ⇒ **不能用「族/数据集」推断，必须逐颗实测**。
- **prod 读取**：平台 prod 是**账号级单并发队列** ⇒ 一次只盯 1–3 颗、串行低频、别并发（见 [`wqb-concurrency`](../../wqb-concurrency/SKILL.md)）。
- **提交链**：禁混闸 / 点亮算术 / 稳健性 fail-closed / prod 当场重测 → 见 [`gate-and-submit-discipline.md`](gate-and-submit-discipline.md)。

---

## 改控制纪律

- **区域级**：`tracking/GLB/config/settings.json`（仿真设置）、`thresholds.json`（阈值）。
  **改动本区设置档前先问**：这是**旧族的过闸率校准**还是**新族的实测最优**？
  新族的最优档写进本文件（规则层），**不要**改区域默认档 —— 否则旧批次不可复现。
- **组合级**：`tracking/GLB/config/cells.json`（覆盖值 + 同级 `_evidence`）。
- **改完先校验再重渲**：`$WQ_PY -m wqb.profiles check --region GLB` → `render --region GLB --apply`。
- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、
  提交前用户确认、truncation 不作扫描维度 —— 全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
