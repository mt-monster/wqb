# 波 191：`board_gov_stats` 六条机制族探针（INSIDERS 塔）

> multisim `1lm8aF4UY4VXcw6150DxzXGT`｜6/6 COMPLETE / 0 错误
> 设置：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 0 / trunc 0.08 / nanHandling ON
> 统一骨架：`group_rank(ts_backfill(F, 120), subindustry)`
> 目的：**判数据集内哪个机制族有真信号**（不追求过闸）。论坛帖 `43152032301591`（43 赞）已警告「董事会治理属慢变量 fundamental，与行为反应不足机制不匹配」。

## 1. 塔位合规性（先决条件）

`get_alpha_details` 实测六条全部：
- `ra.pyramid_short = "insiders"`
- `pyramids.list = [{name: "USA/D1/INSIDERS", multiplier: 1.1}]`
- `pyramids.effective = 1`

⇒ **`board_gov_stats` 属 INSIDERS 单塔**，不触碰「PV / MODEL / OTHER 三塔禁止两两组腿」硬约束。**合规**。

## 2. 六条实测全表

| # | 字段 | alpha | 族 | S | F | TO | 2Y | SUB | invest_S | DD | risk_neut_S | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `board_departure_rate_3m_management` | `kqNR8MOd` | 流动率·离职 | 0.32 | 0.09 | 3.10% | 0.78 | 0.15 | 0.65 | 11.73% | **−0.52** | 3 |
| 2 | `board_join_rate_3m_management` | `vR10Yb6d` | 流动率·加入 | 0.33 | 0.09 | 2.91% | 0.84 | 0.08 | 0.51 | 12.23% | −0.28 | 4 |
| 3 | `surname_concentration_total_personnel` | `ZYQZX9MQ` | 姓氏集中 | 0.87 | 0.45 | 1.21% | **1.90** | 0.14 | 0.89 | 11.01% | +0.78 | 3 |
| 4 | `ceo_tenure_days` | `MPYwgnZr` | 任期 | **1.23** | 0.70 | 1.16% | 1.75 | 0.30 | **1.28** | 11.88% | +0.81 | 3 |
| 5 | `board_external_connection_count` | `2rAEGxeP` | 网络 | 1.17 | 0.65 | 1.14% | 1.84 | 0.58 | 1.14 | **7.88%** | **+1.09** | 2 |
| 6 | `independent_director_ratio` | `E563mMxK` | 独立性 | 1.01 | 0.57 | 1.21% | 1.10 | 0.37 | 1.00 | 6.69% | +0.17 | 4 |

## 3. 四条归因

**① 流动率族判死（不是整集判死）**
字段 1、2 的 S 0.32/0.33、F 0.09、`risk_neutralized_sharpe` **双双为负**（−0.52 / −0.28）。
⇒ 经风险中性化后符号翻转，说明只是风格暴露的残渣，不是独立信号。
⇒ 与论坛帖 `43152032301591` 的「慢变量不匹配行为反应机制」完全一致。
⚠ **但同一数据集的任期族 / 网络族 / 姓氏族有真信号** ⇒ 「流动率族判死」严禁外推成「board_gov_stats 判死」。

**② `risk_neutralized_sharpe` 是极好的机制筛选器（★ 新判据）**
六条被它干净地切成两簇：流动率族（−0.52 / −0.28）vs 其余四族（+0.81 / +1.09 / +0.78 / +0.17）。
它比裸 S 更能区分「真信号」与「风格暴露」。
⇒ **建议作为新数据集的第 3 号筛查指标**（排在 S 与 margin 之后），成本为零（详情接口直接给）。

**③ `2rAEGxeP`（网络族）是零硬失败结构**
`checks.fail = []`（S 1.17 / F 0.65 只是 warning 级）、`2Y 1.84` ✅、`SUB 0.58` 在闸线之上、CW ✅、`DD 7.88%` 六条最低、`risk_neut_S +1.09` 六条最高。
唯一缺口：S +26%（1.17→1.58）、F +35%（0.65→1.00）。

**④ 结构稀缺性：TO 1.1–3.1%、margin 5.5–7.0 bp**
对比 RISK 塔 `88RAN85m` 的 61.77% / 2.86 bp、SHORTINTEREST 的 11–18% / 0.13–0.27 bp。
⇒ 这是**低换手高 margin** 结构，永不受 `HIGH_TURNOVER` 闸威胁；但 `fitness = S·sqrt(R/TO)`，TO 被压到 1% 时 R 也极小，**fitness 反而更难达标**。
⇒ **本数据集的主要矛盾是 S，不是 TO。常规「压换手」动作在这里是反向的。**

## 4. 完整字段画像

46 字段的七族分类、覆盖率、拥挤度、实测状态、波 192 十模板库 → 见
[`docs/reference/USA/board_gov_stats_field_profile.md`](../../docs/reference/USA/board_gov_stats_field_profile.md)

## 5. 交接

波 191 的价值不在「抓到候选」，而在**排除了一条死路（流动率族 18 个字段）并锁定两条活路（任期 / 网络）**。
这两条活路交给波 192 用 10 个结构互异模板提 S。
