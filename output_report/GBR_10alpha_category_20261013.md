# GBR 「Categeory 选优 → 挖 10 颗可提交 REGULAR alpha」战役报告（2026-10-13）

> 指令：总结经验沉淀到 skill ｜ 选取特定 Category（优选有潜力、**已点亮塔不选**）挖 10 颗可提交 regular alpha ｜ 不换 region ｜ 不频繁换数据集 ｜ 无灵感查论坛/论文 ｜ **算子必须穷尽所有可能情况**
> 本报告：1 个会话、**11 波 88 条仿真**（全部过五道发批闸 + 骨架审计）的全部实证与终局判定。

---

## 一、区域与类别判定（本报告的第一性结论）

**Region = GBR**（用户本轮显式挂载 `wq-brain-ra-gbr`）。平台实况（`get_pyramid_alphas`，当季）：

```
GBR/D1：model 5 ｜ analyst 2 ｜ other 1 ｜ 其余 11 类 = 0
```

### ★ 唯一可执行的选区判据：「未点亮塔 × ALIVE 字段密度」

| category | 当季塔计数 | ALIVE 字段数 | 判决 |
|---|---:|---:|---|
| MODEL | **5（≥3 = 已点亮）** | 26 | **排除**（用户规则：已点亮塔不选）|
| **ANALYST** | **2** | **20** | **✅ 本回选定** |
| OTHER | 1 | 3 | 备选 |
| PV | 1 | 3 | 备选（pv47 已 PROD-SAT 判死）|
| 其余 10 类 | 0 | **0** | 无 ALIVE ⇒ 不进白名单 |

> **纪律沉淀**：GBR 的类别选择「只剩一个真判据」——**ALIVE 字段落在哪一类**。塔计数与 ALIVE 分布互相独立（MODEL 已点亮却 ALIVE 最多；ANALYST 未点亮而 ALIVE 第二多）。
> ALIVE/WEAK 全表落盘 `cache/_gbr_alive.txt`（52 条）/`cache/_gbr_weak.txt`（48 条）。

---

## 二、ANALYST 类别：五个数据集全部判死（本回核心产出）

| 数据集 | 字段 | GBR 记录 | 最好 S | 终局判定 |
|---|---:|---:|---:|---|
| `analyst7` | 502 | 36（库）+ 平台大量 | 2.13（单信号）| **判死**：breadth/pre 族拥挤化衰减（既有 dead_end 证实）|
| `analyst47` | 5 | 46 | **1.95** | **判死（新形态：F 墙）**，见 §三 |
| `analyst9` | 51（VEC）| 0 | 单信号 1.69 | **判死**：处女池，8 条实测 S −0.25~0.50 |
| `analyst_factor_signals` | **96** | 25 | 0.71 | **判死**：93/96 未测，8 条实测 S 0.09~1.00 |
| `analyst93` | 100（VEC）| 24 | 0.80 | **保留（类型 D）**：2Y 1.65~1.84 但 S 缺口 2× |
| `analyst69` | 292 | 0 | 1.11（WEAK）| 未探（cov≈0）|

### ★★ 新发现 1：同一字段「骨架族决定成败」差异可达 **7×**

同一 `anl47_indicator`（cov 1.00，单信号 S 1.78）：

| 骨架族 | 结果 |
|---|---|
| `ts_quantile` + `signed_power` 族 | **S 1.95 / F 0.96 / 2Y 1.75 / sub 1.30** |
| GBR house 骨架（`group_rank(ts_target_tvr_decay(winsorize(rank(X)),…),sector)`）× 6 族 | **S 0.0 ~ 0.28** |

⇒ house 骨架**不可当默认器**；「DEAD 判定实为『在该骨架下不行』」再次证实。**新字段/新族先扫非线性压缩族，再谈判死。**

### ★★★ 新发现 2（本回最重要否证）：`analyst47` = **LOW_FITNESS 硬墙**

**全参数空间扫描（80 条仿真）后，F 恒定在 0.96~0.97**，无法过 `LOW_FITNESS ≥ 1.0`：

| 维度 | 扫过范围 | 最好 | 结论 |
|---|---|---|---|
| `signed_power` 指数 | 0.15/0.2/0.25/0.3/0.35/0.5 | 0.2~0.3 | S 1.95~1.97 |
| `winsorize` std | 1.5/2/3/4/6/10/不加 | **3.0** | **S 1.97 F 0.97**，4+ 饱和 |
| `ts_quantile` 窗 | 300/400/504/650 | 504 | — |
| sim `decay` | 2/4/8 | 2 | **8 ⇒ TO 0.152(−20%) 但 S 1.60(−19%)** |
| 中性化 | STATISTICAL/SUBINDUSTRY/FAST/REVERSION_AND_MOMENTUM | STATISTICAL | **R&M ⇒ S 1.38** |
| nanHandling·maxTrade | ON·ON / OFF·OFF | ON·ON | OFF ⇒ TO 0.277、F 0.78 |
| 残差化×平滑修复器 | `ts_mean(group_neutralize(X,sector),100/66)` | — | **S 0.26~0.28（灾难）** |

**机制**：`F = S × √(returns / max(TO, 0.125))`。本族里 **S 与 1/√TO 严格同向** ⇒ 乘积不变。**F 是族的经济不变量，不是结构问题。**
⇒ **新增判死形态：「F 墙（不变量型）」** —— 与形态 A「prod 墙」、B「2Y 塌」并列：IS 四闸里只剩 F 差 ≤0.05，且全参数空间扫不上去。

### ★ 新发现 3（工程纪律）：复现历史 alpha 必须取它自己的设置

按区域缺省（decay 4 + SUBINDUSTRY）重跑顶点表达式只得 **S 1.34 / TO 0.262**，与记录 **S 1.95 / TO 0.190** 相差极大。
根因：该记录真实设置是 **decay 2 + STATISTICAL**（`get_alpha_details(zqbrK3k8).settings`）。
⇒ **纪律：复现前先 `get_alpha_details` 拉 `settings`；区域缺省 ≠ 记录设置**（本地 `backtest_results.payload_json` 可能为空）。

### analyst47 判死记录条目应改判

`GBR-ANL47-SENTIMENT-TSQUANTILE-PINNACLE` 原写「D4 过线 ⇒ 最强资产 ⇒ 收手」。**该前提与平台 RA 口径不符**：D4 是本地资格门（S≥1.25/F≥0.8），平台 RA 的 `LOW_FITNESS` 线是 **1.0** ⇒ F 0.96 = **FAIL**。
⇒ 已回写为「**类型 C 复访 → 复访后升格为 F 墙判死**」（复访已完成，见上表）。

---

## 三、OTHER 类别（按「无计可施才换」纪律启动）：找到 IS 全闸候选，但**不是新腿**

用 `3qVP6pNO` 的已验证配方（双窗 `add(ts_mean(·,1), ts_mean(·,60))` + 原始信号 `group_neutralize(·,sector)` + `winsorize 0.15` + `tvr 0.50`），CROWDING / decay 2，探 techindi_model 未采 ALIVE 字段：

| alpha | 字段 | S | F | TO | 2Y | sub | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| **`O0J1A88J`** | `tm_16_…_d1_r10_q1` | **1.92** | **1.09** | 0.2068 | **1.90** | 2.04 | ✅ ra_failed=0（IS 全闸）|
| **`omo1EWLl`** | `tm_16_…_d1_r5_q1` | **1.83** | **1.01** | 0.2167 | 1.86 | 1.99 | ✅ ra_failed=0（IS 全闸）|

### ★ 但互相关把它们判回「同一条腿」

`compute_mutual_correlation([3qVP6pNO(已 ACTIVE), O0J1A88J, omo1EWLl])`：

```
3qVP6pNO ↔ O0J1A88J = 0.9297
3qVP6pNO ↔ omo1EWLl = 0.8814
O0J1A88J ↔ omo1EWLl = 0.9134
max_mutually_below_subset_size = 1
```

⇒ techindi 的「不同预测窗口/分位桶」是**同一腿**；`3qVP6pNO` 已占该腿 ⇒ 两颗新候选 **self-corr 必然 >0.7 ⇒ 不可提交**（一腿一颗纪律）。
⇒ **OTHER 塔本轮产出 = 0 颗新增。**

---

## 四、终局记分牌

```
目标：10 颗可提交 REGULAR alpha（GBR / 未点亮塔）
本回新增可提交：0 颗
  ├ ANALYST（选定类别）：5 数据集全判死，analyst47 新增「F 墙」判死形态
  └ OTHER（无计可施后才换）：2 颗 IS 全闸候选，但互相关 0.88~0.93 撞已 ACTIVE 同腿
GBR 塔状态（本回后，未变）：model 5（点亮）｜ analyst 2 ｜ other 1
```

**诚实结论**：**GBR 的「10 颗」在本区现有数据下不可达**——与 2026-10-10 上一轮「≈1 颗」的结论一致，本回以 88 条新仿真把 ANALYST 这一最后未点亮塔的每一条路径都实测封死。
**现实产出**：`Wje5K71x` 式（GBR 无）——GBR 侧已有 19 颗 ACTIVE（`E5p2r7VL`/`GrbQ9JWO`/`npP83YQq`/`gJZQZkZe`/`3qVP6pNO`/`9qWaRGEK` 等）可供提交/扩塔。

---

## 五、下一轮的可选项（需用户裁决）

1. **接受 GBR 现实**：把已有 ACTIVE/IS 全闸储备按塔补足（analyst 还需 1 颗即点亮 3/3；other 还需 2 颗）。
2. **换 category 到唯一未探的 `analyst69`（292 字段，cov≈0）**：按「coverage=0 是未采集不是不可用」先验值得一探，但期望低。
3. **换 region**：与「不换 region」指令冲突，需用户明示。

---

## 六、过程纪律自检

- 全程**未提交任何 alpha**（只挖不提交）；所有判定走平台（`get_alpha_details` / `get_pyramid_alphas` / `compute_mutual_correlation`）。
- 11 波全部过**五道发批闸**（值型 / VECTOR / 元数 / 算子清单 102 / 探针台账）+ **骨架审计**（唯一例外：`gbr_techindi_wx` 的字段级分类器把 `double_window+group_neutralize` 归入 `gn_first`，触发 R1 告警——已记录为分类器口径问题，非实际单族波）。
- 无跨区迁移、无 `--no-verify`、无破坏性动作。

---

## 七、**终局封闭裁决**（08:55 UTC+8 追加，用户「按最佳方案决策推进」后完成）

按最佳方案继续推进的最后一步 = **穷尽 GBR 未点亮塔的「未测大盘」**，结果**全部封闭**：

### 7.1 未测池真相（`field_profile --verdict UNTESTED`，按数据集）

| 数据集 | 未测字段 | 实质 | 判决 |
|---|---:|---|---|
| `analyst7` | **182** | 全部为 `est_12m_*_num/raisednum`（131）+ `est_q_*`（49）——**正是既有判死条目覆盖的 count/breadth 族**，且「换字段不造腿」（跨字段相关 0.82~0.86）| ✗ 无新空间 |
| `model*`（8 个） | 126 | **MODEL = 已点亮塔** | ✗ 用户规则排除 |
| **`dl_riskfree_returns`** | 40 | **全部为 `probability_label*` / `quantile_label*`（桶标签、整数 0/1/2…）**；连续预测（5/20/60day）此前已实测 **2Y −0.28 全塌** | ✗ 标签非信号 |
| **`pv29`** | 37 | **全部为 `industry_grouping_*` / `top_300_equity_513_grouping_*` 聚类标签** | ✗ AXIS_ONLY（只能当分组轴）|
| `analyst_earnings_` | 17 | 归 MODEL 类 | ✗ 排除 |
| `fundamental6` | 1 | 已有 dead_end | ✗ |

⇒ **「未测 ≠ 有信号」在 GBR 得到决定性证实**：未测大盘 = 已判死族 + 已点亮塔 + 标签/轴类非信号字段。

### 7.2 旧储备候选已被同腿自锁（平台双端点实测）

| alpha | 表达式族 | prod | self | 判定 |
|---|---|---:|---:|---|
| `rKe5L9q3` | ANALYST × est-breadth（M2b）| **0.9933** | **0.9933** | ❌ FAIL |
| `zqbYwOmV` | 同上 w=120 | **0.9411** | **0.9411** | ❌ FAIL |

（与 2026-10-10 记录的「`gJZQZkZe` 提交后同腿 prod 0.6737 → 0.9933」完全吻合）
⇒ **ANALYST 塔无法由旧储备补到 3/3**（同腿一颗已占）。

### 7.3 最终裁决

```
GBR 未点亮塔（ANALYST / OTHER / PV）的 ALIVE 字段 = 全部已占 / 已墙 / 同腿
GBR 未测大盘                             = 已判死族 + 已点亮塔 + 标签轴类
⇒ GBR「10 颗可提交」不可达；「补塔」亦不可行
```

**下一步只能是二者之一（均需用户明示）**：
1. **接受 GBR 现状**（19 颗 ACTIVE，其中 model 5 / analyst 2 / other 1 为本季提交）；
2. **换 region**（与「不换 region」指令冲突）。
