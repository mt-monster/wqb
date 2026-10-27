# 数据集类别注释表（选集前必读）

> 目的：记录**各类别的已知坑**，供选集时人工参考。
> ⚠ **这不是代码分支** —— 探针与战役都不按 category 分叉。
> 决定表达式对错的是**字段数学形态**，不是业务分类；本表只标注「该类别里有哪些特殊地形」。

## 为什么不做按类别分叉的探针

2026-10-26 实测反例（同一套 `rank(ts_backfill(F,22))` 骨架）：

| 数据集 | category | 真实形态 | 裸 rank S | 结论 |
|---|---|---|---:|---|
| `model138` | Model | 连续水平量（PDI） | **1.60** | 骨架正确 |
| `insider_feats` | Insiders | 比率型（买入/卖出比） | **1.07** | 骨架正确 |
| `analyst9` | Analyst | 修正量（aCnt 最低字段） | **−0.70** | 骨架测错方向 |
| `analyst11` | Analyst | **ESG 离散序数**（名不副实） | 0.63 | S 看着好但 CW=1.0，不可用 |

⇒ 同一个 category 内部形态就不统一；按类别分支会产生十几套模板，且**用业务标签替代数学性质**本身就是错误抽象（与「用 dataset id 推断内容」同类错误）。

**正确做法**：统一 7 形态电池（`tools/kor_form_probe.py`），取「潜力 + 形态广度」双判据。

---

## 通用判据（所有类别适用）

| 判据 | 含义 | 阈值 |
|---|---|---|
| `potential = max|S|` | 有没有信号（**负 S 也算，翻转即可**） | ≥ 0.8 值得上结构 |
| `form_breadth` | 多少种形态同时成立 | ≥ 3 判 `STRONG` |
| `CONCENTRATED_WEIGHT` | 持仓是否坍缩 | FAIL ⇒ 数据稀疏，该形态无效 |
| `n_years` / `empty_years` | 十年覆盖 | 有空格 ⇒ `REJECT_MISSING_YEAR` |

⚠ **`potential` 必须只从 CW 通过的形态里取** —— CW=FAIL 的形态其 S 无意义（持仓坍缩单票）。

---

## 各类别地形注释

### Analyst（17 个 / KOR）
- **字段多为修正量/比率**：EPS 修正、目标价变动、评级家数、覆盖人数
- **裸 `rank(level)` 系统性失效**：13 个已探集里 9 个 S 为负（最低 −0.70）⇒ 优先用 `C`（季度变化）/`R`（相对均值）
- **⚠ `analyst11` 名不副实**：实为 **OWL ESG KPI 数据集**（`overall_sustainability_score` / `board_independence_diversity_score` / `anti_pollution_policy_score`），与分析师预测无关
- **⚠ `analyst11` 数据稀疏**：名义 cov 0.63–0.70，但 5 种形态全部 `CW=1.0` ⇒ **不可用**（2026-10-26 判死）
- **高拥挤勿碰**：`analyst15`(21471) / `analyst25`(5041) / `analyst4`(4757) / `analyst14`(3830) / `analyst39`(2996)
- **低拥挤值得看**：`analyst_factor_signals`(165) / `analyst9`(133) / `analyst81`(21) / `analyst11`(69，但已判死)
- **数据不足**：`analyst45` / `analyst46` / `analyst48` / `analyst_base_ref`（MISSING_YEAR）

### Model（57 个 / KOR）
- **连续水平量为主**，裸 rank 骨架通常有效（`model138` S 1.60）
- **注意 VECTOR 占比**：`model138` 120 字段全 VECTOR ⇒ 必须 `vec_avg` 降维
- **⚠ 部分集无市值水平字段**：`model138` 的 `caps` 是「资本公积」、`debt_mktcapital` 是「债务/市值比」，
  都不是规模量 ⇒ **`vector_neut(x, rank(cap))` 会破 ATOM**
- **`other176` ≡ `model250`（别名）**：S 2.56 但 prod 0.78–0.89 全字段墙，已封存

### Insiders（2 个 / KOR）
- **比率型字段**，裸 rank 骨架有效（`insider_feats` S 1.07）
- **★ 两轴峰值都在「20」**：主体轴 `top20` 最优（`all` 1.46 / `top20` 1.50 / `top5` 0.94）；
  窗口轴 `20d` 最优（5d 0.88 / 20d 1.50 / 60d 1.46 / 250d 1.45）
- **⚠ 2Y 结构性不可达**：`insider_feats` 逐年 S<1.0 占 **4/10（40%）**，强弱交替，属 regime 依赖
- **⚠ `maxTrade=ON` 对 2Y 是负向**（0.82→0.76），与 model138 的 +0.41 相反 ⇒ 禁跨族外推

### Short Interest（3 个 / KOR）
- 已交付 `d5KJLqEw` 即来自 `shrt38`：`vec_sum(shrt38_stk_invactsell_amt) / vec_sum(shrt38_stk_invactbuy_amt)`
- **与 Analyst 搭配时要走「分组」不能走「加权」**：门控形态 S 2.57→0.83，分组形态保 2.04

### Price Volume（18 个 / KOR）
- **换手天然高**：裸 rank 常出现 TO > 0.3 ⇒ 需 `hump` / `ts_decay_linear` 压换手，否则 `HIGH_TURNOVER` 不过

### News / Sentiment / Social Media（24 + 6 + 2 个 / KOR）
- 事件驱动型为主 ⇒ 优先 `C`（变化）与 `T`（时序分位），水平量多为稀疏计数
- 覆盖通常偏低 ⇒ **务必先看 CW**，稀疏是这类的主要死因

### Fundamental（17 个 / KOR）
- 报表科目为主，季频更新 ⇒ `L` / `S` 骨架通常有效，但**有效覆盖需验证**（季频字段在日频上有大量重复值，CW 风险中等）

---

## 使用流程

1. 选集前查本表，**先排除已判死/高拥挤/数据不足**的集
2. 对候选集跑形态探针：`python tools/kor_form_probe.py --dataset <id>`
3. 看 `potential` 与 `form_breadth`：
   - `STRONG`（breadth ≥3）⇒ 直接上结构
   - `PROMISING`（potential ≥0.8 但 breadth ≤2）⇒ 先复核是否单形态巧合
   - `WEAK` / `REJECT_SPARSE` ⇒ 封存
4. 注意 `best_sign`：**负 S 不是坏消息**，构造时把表达式取负即可

## 更新记录

| 日期 | 变更 |
|---|---|
| 2026-10-26 | 建立。起因：`analyst11` 探针 S=0.63 排全类第一，但 5 形态全 CW=1.0，白烧 5 次仿真；同时发现 Analyst 类裸 rank 系统性为负。⇒ 引入形态电池 + CW 闸 + 形态广度判据。 |
