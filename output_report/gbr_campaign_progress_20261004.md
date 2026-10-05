# GBR 战役进度报告 · 截至 2026-10-04 23:50 GMT+8

> 目标：10 个可提交 REGULAR alpha（GBR / TOP700 / delay1）
> **实际：0 颗提交 · 1 颗 NEAR_MISS · 25 条表达式回测 · 3 条 Judgment 判死**

---

## 一、进度仪表盘

| 指标 | 数值 | 备注 |
|---|---|---|
| **可提交 alpha** | **0 / 10** | 无任何一条过全部硬闸 |
| NEAR_MISS 资产 | **1 颗** | `A1v1MKmW`，F 0.97 vs 闸 1.0（差 0.03） |
| 本轮回测表达式 | **25 条** | Track A 10 + Track B₁ 7 + Track B₂ 8 |
| 回测成功率 | **0 / 25** | 全灭（另有首批发的 8 条因单条错误被连坐取消） |
| 今日 REGULAR 配额 | **3 / 4（剩 1）** | 均为 EUR/KOR 区，GBR 未消耗任何配额 |
| GBR 已提交 | **0 颗** | 本轮 GBR 未提交任何 alpha |

---

## 二、三条 Signal 族的完整生死簿

### Track A — analyst47 顶点族 F 攻坚 → **判 NEAR_MISS 天花板**

multisim `4o1ayAcXh5anaOS7g3aEUob`（10 条结构性新维度，全部劣于或持平原顶点）

| 维度 | 结果 |
|---|---|
| `trade_when` 门控 ×5 | **全灭**（S 1.96 → 0.03~0.60，margin 4.85bp → 0.12~1.96bp） |
| `winsorize(std=2)` | 持平略降（F 0.96 < 原 0.97） |
| `quantile()` 等价替换 | **负效应**（S 1.69，KOR 的 +0.05 在 GBR 反向） |
| `group_rank(subindustry)` | 毒药（S 0.76） |
| `group_zscore`+pv30轴 | S 1.93 / 2Y 1.57，但与顶点互相关 **0.985** = 同一 alpha |

**判据**：两轮合计 50+ 变体仍差 F 0.03 ⇒ GLOBAL-LADDER-CEILING-PHENOMENON 命中，停止微调烧配额。

### Track B₁ — insider_matrix 族 → **判死**

4 探针 max|S| **0.59**，TO 全部在 **0.65-0.66**（顶点仅 0.19），CONCENTRATED_WEIGHT 结构性爆，sub 0.01-0.28 全弱。

**根因**：`eur_*` 是事件型聚合值（有内部人交易才有值），天然快信号；套 `ts_quantile(504)` 慢骨架，在 nanHandling=ON 下频繁跳变 ⇒ 高换手。**快信号不能套慢骨架**。

### Track B₂ — group_rank × pv30 聚类轴 → **判死（守恒律）**

| 变体 | S | F | 2Y | sub |
|---|---|---|---|---|
| group_rank(sentiment, group10) | 0.94 | 0.36 | 0.51 | 0.85 |
| group_rank(sentiment, group20) | 0.96 | 0.37 | 0.61 | 0.89 |
| group_rank(sentiment, group50) | 0.94 | 0.35 | 0.41 | 0.88 |
| group_rank(sentiment, sta2收益聚类) | 0.93 | 0.35 | **0.82** | 0.87 |
| group_rank(sentiment, PCA-10轴) | **0.98** | **0.38** | 0.61 | **0.95** |
| winsorize 包装 | 0.94 | 0.36 | 0.51 | 0.84 |
| group_rank(rawalphadecay反向, group10/50) | 0.71 / 0.74 | 0.25 / 0.26 | −0.08 / −0.18 | 0.60 / 0.70 |
| group_zscore(rawalphadecay反向, group10) | 1.39 | 0.60 | −0.03 | 0.72 |

**6 个轴/包装变体，S 极差仅 0.05**（0.93~0.98）⇒ 换轴无用，LADDER-CEILING 命中。

---

## 三、★ 本轮最硬产出：去相关–Sharpe 守恒律

```
母信号（顶点 A1v1MKmW）            S = 1.96
group_rank 变体 ×6（不同轴）        S = 0.93 ~ 0.98，均值 0.95
  ⇒ S 保留率 48.4%  ⇒  【S 损耗 51.6%】

group_rank vs 顶点 实测互相关      0.557
  ⇒  【相关降幅 44.3%】

        相关降幅 44.3%  ≈  S 损耗 51.6%   （差 7.3pt）
```

**机制解释**：`group_rank` 的组内均匀化强制每组都出满多空，人为注入噪声持仓。横截面排序正是信号的载体——**改变排序的算子必然同时削 S**（与 MEMORY §1.5「降 prod 的算子必须改变排序」互为推论）。

**由此得出两条结构性判据**：

1. 在同一信号上做几何重排（`group_rank` / `group_zscore` / `trade_when` / `winsorize`），**无法同时拿到低相关 + 高 Sharpe**：
   - `group_zscore` → 相关 0.985，等于没做（等价变换）
   - `group_rank` → 相关 0.557，但 S 腰斩
   - **二选一，没有免费午餐**

2. 若要 S>1.58 **且** corr<0.7，唯一路径是**换独立信号源**，不是换几何变换。

> **caveat（重要）**：这不是信号死，是「去相关方法的物理极限」。若将来存在 raw S ≥3.0 的独立信号，`group_rank` 仍是好工具（腰斩后 S 1.5 仍可能过闸）。**GBR 当前没有这样强的母信号**。

---

## 四、可行性核算 —— 必须摊牌的部分

| 项目 | 数字 |
|---|---|
| 历史端到端成功率（MEMORY §3） | **0.10%**（65,580 expr → 65 颗） |
| 本轮投入 | **25 条**（占总需量的 0.25%） |
| 反推出 10 颗所需回测量 | 约 **10,000 条** |
| REGULAR 配额硬上限 | **4 颗 / ET 日历日** |
| ⇒ 即使立刻挖出 10 颗 | 提交完至少需 **3 个 ET 日历日**（今日 ET 已过 11:45，剩 1 颗） |

**结论**：「今晚在 GBR 拿下 10 颗可提交 alpha」在当前配额体制与 GBR 已探空间下**不成立**。GBR 历史 87 波 / 47 dead_end / submit_ready 0，本身是低产区。

---

## 五、本轮副产出（避免未来重踩）

### 数据口径纠错
- `other455` 的 1500 字段**全是 `oth455_competitor_n2v_*`** = 已判死机制的 1500 个变体，**是伪装成金矿的坟场**
- `analyst44` 72 字段全是 `anl44_2_*` 预期修正族，整族已封
- `analyst48` 剩余字段全是 index 元数据（idivisor/return_code），无信号
- `analyst69` = 292 字段 Bloomberg BEST 红海（`anl69_expected_report_dt` alphaCount **3071** / userCount 273），绝大多数是 VECTOR 型
- ⚠ **`expressions` / `backtest_results` 两表都不是「已测」的可靠全集**——只有 registry dead_end 台账是判死权威

### Fitness 公式翻案（MEMORY §1 待更新）
`F = S × √(|R| / max(TO, 0.125))` 且实测 `R ≈ margin × TO × 504`
⇒ **`F = S × √(504 × margin)`，turnover 完全约掉**
这解释了为什么原 40+ 变体（全扫 decay/truncation/窗口 = turnover 旋钮）F 纹丝不动：**旋钮选错，非平台极限**。

### 三条离线/在线闸纪律
- 发批前 `ensure_safe_for_dispatch_strict`（元数 + 算子存在性双闸）+ 幽灵算子清单
- MCP 数组参数经 DeferExecuteTool 间歇性损坏 → `batch_get_alpha_metrics` 报 success 但指标全 null，**比报错更危险**
- `mcp__wqb-db__harvest_multisim_results` 写库后必须复核

---

## 六、下一步（三选一，需你决策）

| 选项 | 说明 | 代价 |
|---|---|---|
| **A. 继续未测族探针** | 余 11 个未测 analyst 族（analyst8/10/15/16/35/39/40/46/83/94/revision_horizons）+ 60 余个非 analyst 未测集 | 需大批量回测；命中率仍低 |
| **B. 换机制：定向外部灵感** | 按你的要求查论坛 + 外部论文找新机制的概念层 idea（不是字段层），再做expr层实现 | 慢，但不烧回测配额 |
| **C. 接受 GBR 产能现实** | 承认 GBR 是低产区，把预算转到别的 region（但你已明确说不换 region） | 违反你的指令 |

---

*生成时间：2026-10-04 23:50 GMT+8 · 战役台账 `gbr_pinnacle_unfreeze_20261004` / `GBR-GROUPRANK-DECORREL-SHARPE-CONSERVATION` 均已落库*
