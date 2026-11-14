# BE102 / BE103 — DEU EARNINGS 塔 · earnings_sent_matrix CP 网格（2026-11-12）

> 用户裁定：从 SENTIMENT 判死后转向 `earnings` 塔（DEU 12 塔中最后一个未穷尽的面）。
> 开工前查档发现 **EARNINGS 塔已有 v2 判死证书**（EAT 日历 BE62/64、PEAD BE63、EPS surprise BE99、
> PV×EARNINGS 组合 BE101，累计 ≈50 臂，最高 S 0.80）。本波不是重开判死面，而是补一个**档案未覆盖的缺口**。

## 一、缺口证据：DEU wave1 漏掉的三条杠杆

DEU 既有 `earnings_sent_matrix_wave1_templates.json`（10 模板）实测天花板 **S 0.63**。
其设置与构造：**decay 4 / nan OFF / SUBINDUSTRY / 外层窗 252 / 裸 P 与 P−N**。

对照 USA 同数据集的 W180 消融（`tracking/USA/reports/wave180_earnings_cp_ablation.md`，同 7 字段同三分类分布）：

| 杠杆 | USA 实测幅度 | DEU wave1 是否用过 |
|---|---:|---|
| **CP = P/(P+N)** 条件正概率（约掉中性概率 NT） | 构造层前提 | ❌ 用的是裸 P / P−N |
| **外层长窗 ts_zscore / ts_rank 504** | S 1.23 → **1.71 / 1.70**（+0.48） | ❌ 只到 252 |
| **decay 4 → 0**（季频事件型，平滑＝拖滞后） | S 0.97 → 1.23（+0.26） | ❌ 用 4 |

⇒ DEU 的 0.63 是在「无 CP + 短窗 + decay4」下取得的；USA 在补齐三条杠杆后从 0.97 打到 1.71。
**缺口是真实的、机制清晰的、有跨区先例的**，值得一整波。

## 二、本波设计：2 组 × 10 臂（同表达式，仅换 nan 设置，保证可归因）

固定：DEU / TOP500 / D1｜**decay 0**（USA 主杠杆之一）｜SUBINDUSTRY 中性化｜trunc 0.08｜pasteurization ON
| 批号 | multisim id | nan_handling |
|---|---|---|
| BE102 | `1sBdJ53m24uYagJKmE5h2Cl` | OFF |
| BE103 | `MQJcw30v57qbeReEDVZqK6` | ON |

**为什么只扫 nan 一档**：decay 已按 USA 实证钉死为 0（不浪费臂做 4 的对照）；
nan 是 DEU 专属未知量（记忆：事件型/缺失型字段 nan ON 会填 0 造并列块，曾致 S 2.02→0.51），必须实测。

## 三、十臂清单（结构互异，无两条只差窗口）

| # | 构造 | 回答的问题 |
|---|---|---|
| A1 | `group_rank(CP, subindustry)` | CP 水平本身有无信号（基线） |
| A2 | `group_rank(ts_zscore(CP,504), subindustry)` | **★USA 冠军配方复刻** |
| A3 | `group_rank(ts_rank(CP,504), subindustry)` | ★非参数版（USA 二号 1.70） |
| A4 | `group_rank(ts_zscore(CP,252), subindustry)` | 窗口归因：504 是否真优于 252（DEU wave1 用的就是 252） |
| A5 | `group_rank(ts_zscore(CP,1008), subindustry)` | 四年常态是否更好（跨自然年，欧洲半年报制度） |
| A6 | `group_rank(ts_av_diff(CP,504), subindustry)` | 相对两年均值的**加性偏离**（vs A2 的标准化） |
| A7 | `group_rank(ts_zscore(CP,504), industry)` | 分组轴：USA 用 industry，DEU wave1 用 subindustry |
| A8 | `group_rank(ts_zscore(CP,504), sector)` | 分组轴第二档 |
| A9 | `group_rank(ts_zscore(CONF,504), subindustry)` | **第二自由度**：已表态比例 P+N / (P+N+NT)（置信度 ≠ 极性） |
| A10 | `group_rank(ts_zscore(SW,504), subindustry)` | 第三几何：带符号净情感 (P−N)/(P+N) |

其中 `CP = divide(P, add(P,N))`、`CONF = divide(add(P,N), add(P,N,NT))`、`SW = divide(subtract(P,N), add(P,N))`，
`P/N/NT = ts_backfill(<positive_sentiment_probability_3 | negative_sentiment_probability_3 | likelihood_of_neutral_tone>, 252)`。

## 四、派发前自检

- 算子数：6 / 7 / 7 / 7 / 7 / 7 / 7 / 7 / 10 / 9 —— **全部 ≤12**（平台硬限 64）
- 闸5（禁双独立信号腿加权相加）：全 10 臂**无一条**出现两腿 add/multiply 合并；`add` 只出现在**分母位**（CP/CONF/SW 的归一化）⇒ 放行
- trio 铁律：10 臂全部只用 EARNINGS 单数据集 ⇒ 不触碰 PV/MODEL/OTHER ⇒ **ATOM 资格齐全**
- 字段名：`positive_sentiment_probability_3` / `negative_sentiment_probability_3` / `likelihood_of_neutral_tone` 三个均已用 `get_datafields` 在 DEU/TOP500/D1 核实在册（MATRIX）
- 算子可执行性：`divide/add/subtract/multiply/ts_backfill/ts_zscore/ts_rank/ts_av_diff/group_rank` 全部为本战役已成功使用过的算子 ⇒ 无需 2 臂探针
- 并发：2 批（≤2 上限）

## 五、判读线（派发前预设，杜绝事后挪线）

| 结果 | 处置 |
|---|---|
| 任一臂 **S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58** | 立即查 lc/sc 空心件 → 全闸复核 → 进篮子候选 |
| max S ∈ [1.2, 1.58) | 按协议 v2 L2 补定向 10 臂（窗阶 252/378/504/756 + 另两个自由度） |
| max S ∈ [1.0, 1.2) | 补 10 臂（机制面：Gini 不纯度 + argmax 离散类 + 事件当口 trade_when） |
| max S < 1.0 | EARNINGS 塔维持关闭，本缺口补完即成**第五张 v2 证书**，不再追加 |

**硬性附加判据（BE99 教训）**：任何 |S| ≥1.2 的臂先查 `longCount/shortCount`，任一为 0 或严重失衡（如 5/23）⇒ 空心/偏置件，直接作废，不得据此判「有信号」。
