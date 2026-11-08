# KOR × Institutions × ATOM 战役（2026-11-07）

> **目标**：在 KOR 区按 `wq-brain-ra-kor` 六步纵深 + 发波闭环，从 **Institutions** 类别挖 10 颗 ATOM 型 REGULAR alpha。
> **固定**：KOR / TOP600 / Delay 1 / EQUITY。全程未换区。
> **交付口径**：10 颗组成候选池，每颗 `self < 0.7`、`prod < 0.7`、池内两两互相关 `< 0.7`。

## 结论速览

| 项 | 结果 |
|---|---|
| 交付 | **10 颗 ATOM 候选池**（6 × institutions6 + 4 × fund_holdings_panel） |
| self | 10/10 PASS，max **0.2995** |
| prod | 10/10 PASS，max **0.5528** |
| 池内两两互相关 | 10/10 低于 0.7，max **0.6874** |
| 结构多样性 | 2 数据集 / **8 类经济结构** / 4 个中性化档 |
| 强度 | **S 0.13–0.92**，全池**无一达到 KOR 平台闸 1.58** ⇒ 定位是候选池，不是「已可提交」 |
| 十年覆盖 | 6/10 全 10 年；⚠ 4/10 仅 9 年（panel 2014 空年） |
| 提交 | **未提交任何 alpha**，提交权归用户 |

## 一句话风险提示

`KOR × Institutions` 的强度天花板实测为 **S ≈ 0.97**（110 次模拟、2 数据集、41 字段、6 类结构族、
4 个中性化档、3 档时序门控、横截面门控、3 档平滑窗全扫）。**这个类别做不出过闸的 alpha**，
能交付的是「相关性干净、结构互异」的候选池。全战役最强件是 `MPYee1r6`（S 0.97 / F 0.64 / TO 4.67%），
因与池内净广度件同族高相关未入池，是后续单颗深挖的最佳起点。

## 文件索引

| 文件 | 内容 |
|---|---|
| [final_report.md](final_report.md) | **交付报告**：验收表、10 颗明细、逐年 S 剖面、相关性终验、完整表达式、经济机制、可复用结论 |
| [s0_dataset_scan.md](s0_dataset_scan.md) | S0 数据集扫描：Institutions 2 个数据集全量、41 字段逐条裁定、判死记录对齐 |
| [s1_field_profile_institutions6.md](s1_field_profile_institutions6.md) | S1 字段画像：institutions6 **11/11** 字段（类型/覆盖/频率/量纲/分布/可用性） |
| [s1_field_profile_fund_holdings_panel.md](s1_field_profile_fund_holdings_panel.md) | S1 字段画像：panel **30/30** 字段 + 16 个判死族排除清单 |
| [s2_mechanism_evidence.md](s2_mechanism_evidence.md) | S2 机制与双通道取证（论坛 + 外部文献）、预登记失败边界 |
| [waves.md](waves.md) | 波次台账 W1–W8：设计 / 读数 / 归因 / 继承-准入-收窄 / 全部阴性结论 |

## 波次进展

| 波 | 设计 | 批次 | 关键读数 |
|---|---|---|---|
| W1 | institutions6 结构十探针（K0 档） | `lCN5JdHd4rZabW1hRszxRtu` | 7 条量纲 ERROR；3 条 S −0.20…0.08；`LLMmGvKL` 逐年只有 2023 正 ⇒ 净广度轴死 |
| W2 | 新鲜度门（M2 机制移植，K1 档） | `2sXwoK6sf5f0aEq13SeKIOrl` | 门控 +0.17；最优 `JjeW761j` **0.88** |
| W3 | 门控 × 分位窗 × 凸化收窄 | `1KK9QS3cc5f49hiDWecOvRQ` | 门控边际 **+0.76 倍**；W=840 是峰；`1YNlXQd6` **0.88** |
| W4 | institutions6 十条异构结构 | `2E9l2RDE4vvbE6k0RZOHIW` | 9 类结构全部 −0.89…+0.13 ⇒ 只有 1 个核有效 |
| W5/W6 | panel 十轴 × 两档 | `3ra66N4FX4RqbX5TotXoty3` / `1cqIyY4Jj4ks94Ie27HOTYz` | 最优 `1YNlZebR` **0.51**；门控跨数据集失效 |
| W7/W8 | 中性化档对照（REV&MOM / CROWDING） | `dlpMCccG4RQbOf199otTWzo` / `1Fl0lL8x14VJbZTIwbxyRxx` | 最强核跨档极差仅 0.06 ⇒ 中性化不是杠杆 |
| S6 | 组池 + 三项相关性终验 | — | 10 颗全过；prod 淘汰 2 颗拥挤度水平件 |
| W9/W10 | 9 类结构在最优门控下重测 | `4qH9fEh0o5c29MF2rWWeYp5` / `2T8AMu1KU4TW9mM13ND0M3YA` | 新增 `ts_decay_linear(21)` 平滑层 ⇒ **`MPYee1r6` S 0.97**（新最高） |
| W11 | 横截面机构持股比例门控 | `10KndI4Nj5jh9dpIKTTKemX` | **负杠杆**（0.97→0.67）⇒ 天花板定格 0.97，收工 |

## 三条最重要的可复用结论

1. **`ts_arg_max` 作信号会摧毁信号，作门控条件是冠军机制** —— 净广度核去门控 0.50 → 加门控 0.88（+76%）。
2. **量纲陷阱**：KOR `unitHandling=VERIFY` 下**禁止**给带量纲字段加标量 `+1`，防除零改用直接 `divide`。
   `preflight_expressions` 查不出量纲，只能人工审。
3. **时序自锚定分位会翻转方向**：`buyers/holders` 裸水平 −0.43，套 `ts_quantile(·,840)` 后 +0.60。
   「水平失败」不等于「字段失败」。

## 补测波（W9–W11）的三条新结论

4. **`ts_decay_linear(·,21)` 平滑层是真实增益**：净广度 0.88 → **0.97**，TO 从 5.2% 降到 4.67%（吃掉季度披露阶跃毛刺）。
5. **横截面机构持股比例门控是负杠杆**：0.97 → 0.67（高 IO）/ 0.60（低 IO）。两个子样本都比全截面弱
   ⇒ 信号是**广基的**，切子集只损失分散度。
6. **时序新鲜度门不可被横截面门替代**：只留 IO 门 0.40 / 双门 0.67 / 只留时序门 0.97。

## 复现所需设置

- 平台档：KOR / TOP600 / Delay 1 / EQUITY / FASTEXPR / unitHandling VERIFY / nanHandling OFF /
  pasteurization ON / maxTrade OFF / 区间 2014-01-01 ~ 2023-12-31
- 逐颗 `neutralization` / `decay` / `truncation` 与完整表达式见 [final_report.md](final_report.md) §4
