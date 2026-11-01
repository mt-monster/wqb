# 模板库 · `divide(<基本面科目>, cap)` 缩放基本面机制（GBR / TOP700 / D1）

> 生成日期：2026-10-30
> 状态：**批 1 / 批 2 / 批 3 / 批 4 已收批** ⇒ 产出 **4 条全闸候选**（`omEQ9kK5`、`E56oqo1r`、`rKRQbPPE`、`P0ojnOOp`，其中 `rKRQbPPE` 是纯 FUNDAMENTAL 单塔）；**批 5 已派（T4f / T4g，第三时间尺度，§6.10）**。机制已从「缩放基本面」修正为「**盈利收益率的自身偏离 = 估值重估动量**」（§6.6 / §6.8）。
> 机制来源：本轮 `fnd6_<科目>/cap` 族 13 条 `failed_ra_count=0`（见 `reports/gbr_pyramid_audit_20261030.md` §4）。
> 扩展到其它基本面数据集的依据：**旧 dead_end 的证据从未覆盖 `X/cap` 形式**（详见下文「为什么值得扩」）。

---

## 一、为什么值得扩到 fundamental17 / fundamental72

四个基本面 dead_end 的 `evidence` / `reason` 全文实读，**一次都没出现 `cap`**：

| dead_end | 证据里的形式 | 最强读数 |
|---|---|---|
| `GBR-FUNDAMENTAL6-CEILING` | `atq/revt`、`oancf-oiadp/atq`、`fnd6_*_atq/revt` | S 0.37 / 2Y 1.08 |
| `GBR-FND72-FASTKILL` | 股息/融资现金流**比**等 46 条 | \|S\| 0.55 |
| `GBR-FUNDAMENTAL17-DEAD` | 运营利润率变化、资产周转波动等 10 条 | S 0.45 / 2Y 0.07 |
| `GBR-FUNDAMENTAL45-CALLTRANSCRIPT-DEAD` | 双模型分歧、双重差分 | S −0.57 |

而 `GBR-FUNDAMENTAL6-CEILING` 的判死理由原文写的是：

> 「裸 rank/group_rank(fnd6_*_atq/revt) 全是**规模因子暴露**（rn −0.25~−0.73）非超额」

**这句话恰好指向 `/cap`**：既然裸水平被规模暴露污染，那么除以市值正是把规模项从分母里消掉的标准做法。判死的对象是「同量纲会计比率」这一类，不是「任何用到这些科目的表达式」。

**检索证据（全库，正则而非 LIKE）**：`backtest_results.code` + `alphas.expression` 全表里，使用任一 `/cap` 形式的有 **64 条**，其中碰到 `fundamental17` 字段的 **0 条**、碰到 `fundamental72` 字段的 **0 条** ⇒ 该形式对这两个集**从未测过**，不是「测过失败」。

**同时排除的伪路径**：`fundamental72` 的 46 条探针已有 `CONCENTRATED_WEIGHT 超限占绝大多数 FAIL` 的结构性墙（低频年报覆盖稀疏），与信号无关 ⇒ f72 优先级低于 f17。

---

## 二、10 个结构互异模板

设置基线（与 fnd6 族完全一致，**只换数据集**，保证是干净对比）：`INDUSTRY` 中性化 / decay **10** / truncation **0.05** / nanHandling **OFF** / maxTrade **OFF**。
`X` = 基本面科目（货币单位），`cap` = 市值 ⇒ `divide(X, cap)` 无量纲。

| # | 信息加工方式 | 模板 | 结构差异点 | 来源 | 状态 |
|---:|---|---|---|---|---|
| T1 | 水平 · 横截面行业相对 | `group_rank(divide(annual_ebitda_value, cap), subindustry)` | 保留幅度信息、按子行业比较 | 自建（缩放水平 + 行业相对） | 待派 |
| T2 | 水平 · 自身时序标准化 | `ts_zscore(divide(annual_ebitda_value, cap), 504)` | 不用横截面，用**自身 2 年历史**定标 | 自建 | 待派 |
| T3 | 一阶差分 · 绝对值 | `rank(ts_av_diff(divide(annual_ebitda_value, cap), 252))` | 变化量（EBITDA 收益率年度变化） | fnd6 族实证骨架 | **已派发** |
| T4 | 一阶差分 · 分位驱动 | `rank(ts_quantile(ts_av_diff(divide(quarterly_ebit_value, cap), 66), 22, driver=gaussian))` | 差分后再做**高斯分位映射**，压极端值 | 论坛 `44089095804439`（168/56→2.71 in GBR） | **已派发** |
| T5 | 二阶差分 · 加速度 | `rank(ts_delta(ts_delta(divide(quarterly_ebit_value, cap), 66), 66))` | 变化的**变化**（货币单位二阶） | 论文（基本面加速度） | 待派 |
| T6 | 离散度 · 稳定性溢价 | `rank(reverse(ts_std_dev(divide(ttm_ebitda_value, cap), 252)))` | 不取方向，取**波动低者优** | Gray & Vogel 2012（现金流波动溢价） | 待派 |
| T7 | 信噪比 · 差分 IR | `rank(ts_ir(divide(ttm_total_revenue, cap), 252))` | 变化方向的**均值/标准差**比 | 自建 | 待派 |
| T8 | 分布保持 · 行业内 z 分数 | `group_zscore(divide(quarterly_total_assets_3, cap), subindustry)` | 与 T1 同为行业轴，但**保幅度不排名** | 论文（行业内标准化） | 待派 |
| T9 | 事件门控 · 条件触发 | `trade_when(greater(ts_delta(cap, 66), 0), rank(ts_av_diff(divide(annual_ebitda_value, cap), 252)), -1)` | 仅在市值扩张期持有，**非 `add(A,B)`** | 自建（条件化，合规形态） | 待派 |
| T10 | 位置 · 时序 rank | `ts_rank(divide(quarterly_ebit_value, cap), 252)` | 只留**历史分位位置**，丢绝对幅度 | 自建 | 待派 |

**多样性自检**：横截面轴出现 3 种（无 / subindustry rank / subindustry z）、时间加工 4 类（水平 / 一阶 / 二阶 / 离散度）、非线性 4 种（rank / zscore / quantile-gaussian / ts_rank）、门控 1 种。**不是同一骨架换窗口**。

**窗口取值理由**（均在白名单内）：
- `66` = 季度（约 3 个月交易日），对应季度财报披露节奏；
- `252` = 年（1 年交易日），对应年度财报；
- `504` = 2 年，给时序标准化留够样本（≥2 个年度观测）；
- `22` = 月，分位窗口取月频以避免用未来信息。

---

## 三、科目选择：避开平台已提供的现成比率

`fundamental17` 自带 2952 个 alpha、135 字段，其中**大量现成比率**：`annual_price_to_sales_ratio`、`quarterly_return_on_equity_percent_3`、`quarterly_working_capital_per_share_to_price_3` 等。

⇒ 若用 `divide(营业收入, cap)`，等于把平台已提供的 `price_to_sales` 取倒数，**与既有 2952 条 alpha 高度冗余**（prod 撞墙概率高）。
⇒ 因此优先选**平台没提供对应比率**的科目：`annual_ebitda_value`、`quarterly_ebit_value`、`ttm_ebitda_value`、`quarterly_total_assets_3` —— 它们的 `/cap` 形式（EBITDA 收益率、EBIT 收益率、资产市值比）在字段表里没有对应项。

**已排除**：
- 所有 `*_per_share` / `*_ratio` / `*_percent` / `*_cagr` / `*_avg_price` —— 本身已归一，除 `cap` 无意
- 所有 `*_fx_rate` / `*_currency_code` —— 汇率与货币代码，无经济含义
- `*_change_percent` —— 已是无量纲变化率，除 `cap` 双重归一

---

## 四、判读约定

- **达标**：`failed_ra_count=0` + S≥1.58 + F≥1.0 + 2Y≥1.58 + TO≤0.70 + SUB 过闸（GBR 该闸为比值派生，读 `limit` 字段，勿套 0.4743 系数）。
- **塔位**：本机制预期落 **FUNDAMENTAL**（GBR 0/3）或 **PV+FUNDAMENTAL** 双塔（`divide(科目, cap)` 同时具备两者属性，fnd6 族实证 `effective=2`）。用 `get_alpha_details` 的 `is.checks[MATCHES_PYRAMID]` 核，**不要**从 category / dataset_id 推断。
- **失败判读**：单模板失败 ≠ 机制失败。按模板族归因；同一数据集连续 2 波全灭才考虑判死，且**判死必须带设置档指纹 + 分母形式**（`X/Y` 还是 `X/cap`）。
- **判死后扩数据集**：若 f17 全灭而 f6 成立，结论是「该数据集的科目质量」而非「`/cap` 机制不成立」。

---

## 五、本库的已知风险

1. **`fundamental17` 拥挤度高**（alphaCount 2952）⇒ 即便指标过闸，prod 也可能撞墙。按 `wq-prod-corr-read` 的「族代表预判」先测一颗代表再决定是否量产。
2. **本地 `coverage=0` 不可信**：f17 / f72 全字段本地 coverage 记 0，但历史上两者都跑出过读数（0.45 / 0.55）⇒ 数据存在，该列是"未测"而非"无数据"。
3. **`maxTrade OFF` + 年频字段**可能带来高换手（年度跳变集中在披露日），若 TO 超 0.70 优先调平台 decay（见 `wq-prod-lever-self-lock-guard`：平台 decay 是换手治理的正确层），**不要**在表达式里加平滑。

---

## 六、批 2：分母替换对照实验（T4b / T4c）

### 6.1 为什么要换分母

`omEQ9kK5`（T4）的塔位实读是 **`MATCHES_PYRAMID` → effective=2，`GBR/D1/PV`(1.4) + `GBR/D1/FUNDAMENTAL`(1.6)**。
原因是 `cap` 属 PV 数据集 ⇒ 每一条 `X/cap` 都是一次 **trio 塔（PV）× 非 trio 塔（FUNDAMENTAL）** 的组合。

而本项目的硬约束是「trio × 非 trio 这类组合总量 ≤5」，按保守读法＝最多 5 条 alpha。**若 8 个剩余模板全用 `cap`，会一次性冲破这条配额。**
⇒ 后续模板必须优先改成 **FUNDAMENTAL-only** 形式：既能补 FUNDAMENTAL 塔（GBR 0/3），又不吃配额。

### 6.2 关键判断：`/cap` 到底是不是生效的必要条件？

已知反证（本库 §一 之外的既有实测）：

| 用 `cap` 的形态 | 读数 | 结论 |
|---|---|---|
| `ts_ir(..., 252)` | S −0.34 | 有 `cap` 也灭 |
| `arg_max(..., 504)` | S 0.28 | 有 `cap` 也灭 |
| `ts_zscore(..., 504)` | S −0.33 | 有 `cap` 也灭 |

⇒ 据此我当时推断「**`cap` 本身不是生效条件**，起作用的是 `ts_av_diff` + `ts_quantile(gaussian)` 组合」，于是设计了「固定变换、只换分母」的单变量对照。

> ⚠ **这条推断已被批 2 推翻，见 §6.6。** 正确结论是：**变换和 `/cap` 都是必要条件，且 `/cap` 携带的是「估值口径」这一层独立信息**。
> 保留下面的推理过程是为了记住教训：**「p×q 都成立」反推不出「p 独立于 q」** —— 上表三条反证只说明「`cap` + 错误变换 = 失败」，不能推出「正确变换 + 非 `cap` 分母 = 成功」。

### 6.3 两种改法的取舍

`fundamental17` 内部自带 `market_capitalization_value_5`（"Current market capitalization"，224 users / 714 alphas）。
用它替换 `cap` **确实能**把塔位收纯到 FUNDAMENTAL，但经济含义与 `cap` 完全相同 ⇒ 与 `omEQ9kK5` 近乎共线（self-corr 会顶到 0.9+），**对「凑 3 条互异候选点塔」无用**。⇒ 不采用。

改用**会计口径的分母**（总资产），同时改变经济机制（市值估值 → 资产盈利能力），才有真正的多样性增量。

### 6.4 批 2 的两条表达式

设置与批 1 完全一致（`INDUSTRY` / decay 10 / trunc 0.05 / nan OFF / maxTrade OFF），只改分母：

| 编号 | 表达式 | 相对 T4 改了什么 | 经济含义 |
|---|---|---|---|
| **T4b** | `rank(ts_quantile(ts_av_diff(divide(quarterly_ebit_value, quarterly_total_assets_2), 66), 22, driver=gaussian))` | **只换分母** `cap` → `quarterly_total_assets_2` | EBIT/总资产 = ROA 的**偏离自身一年均值**的当月高斯分位（资产盈利能力加速） |
| **T4c** | `rank(ts_quantile(ts_av_diff(divide(fnd17_0_fcfq, quarterly_total_assets_2), 66), 22, driver=gaussian))` | 分母同 T4b，**分子换 FCF** | FCF/总资产 ⇒ 从**应计利润**切到**现金生成**（Gray & Vogel 现金流族） |

**实验价值（一石三鸟）**：
1. T4b vs T4 ⇒ **单变量**（只差分母）⇒ 直接回答「`/cap` 是不是必要条件」。若 T4b 仍过闸，则「真正变量是分母」这一条要收窄为「真正变量是**缩放**」。若 T4b 灭而 T4 成，则 `/cap` 引入了实质 PV 信息，旧 dead_end 的判死结论可维持。
2. T4b vs T4c ⇒ **单变量**（只差分子）⇒ 判断机制是「资产端盈利能力」通用，还是只对某个科目成立。
3. 两条都是 **FUNDAMENTAL-only** ⇒ 塔位预期为 `GBR/D1/FUNDAMENTAL` 单塔，**不消耗 trio×非 trio 配额**。

**科目选择理由**：`quarterly_total_assets_2`（21 users / 29 alphas）比 `quarterly_total_assets_3`（14/15）覆盖更广、使用更充分；`fnd17_0_fcfq`（481/1157）是本数据集覆盖最好的字段之一。两者的 `/资产` 形式在字段表里**没有现成比率**（平台只提供 `*_return_on_equity_percent_*`，是权益口径不是资产口径）。

**预检结果**：`preflight_expressions` → `unknown_soft=[]`、`platform_field_count=3`、`vector_fields=[]`（`gaussian` 被误报为字段名是已知假阳性）。

### 6.5 判读约定（在 §四 基础上补两条）

- **塔位必须逐条核** `is.checks[MATCHES_PYRAMID]`：若 T4b/T4c 仍出现 `PV`，说明 `quarterly_total_assets_2` 也被归到 PV，此时**不要**再往该方向加派发（配额问题重新算）。
- **互异候选的判据是 mutual correlation，不是指标**：3 条候选要能一起提交，得互相 `<0.7`（用 `compute_mutual_correlation` 本地算，零配额）。若 T4b/T4c 与 `omEQ9kK5` 互相 0.8+，即便全闸通过也**只算 1 条**，需继续找互异模板。

### 6.6 批 2 结果：`/cap` 是必要条件，机制被重新定义（2026-10-30 实测）

设置与 T4 完全一致（`INDUSTRY` / decay 10 / trunc 0.05 / nan OFF / maxTrade OFF），**只有分母不同**：

| alpha | 分子 | 分母 | S | F | TO | 2Y | SUB | fRA | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `omEQ9kK5`（T4） | `quarterly_ebit_value` | **`cap`** | **1.59** | 1.15 | 14.16% | **2.12** | 1.02 | **0** | ✅ 全闸 |
| `WjOKa3RZ`（T4b） | `quarterly_ebit_value` | 总资产 | **−0.21** | −0.05 | 7.33% | −0.71 | −0.13 | 4 | ❌ 灭 |
| `wpQXn3k6`（T4c） | `fnd17_0_fcfq` | 总资产 | **−0.07** | −0.01 | 7.62% | 0.40 | −0.28 | 4 | ❌ 灭 |

**这是干净的单变量对照**（T4b 与 T4 只差分母一个字段），所以归因无歧义：

> **`/cap` 不是可有可无的尺度化，它改变了经济量的性质。**
> `EBIT / cap` = **盈利收益率（earnings yield，估值口径）**；`EBIT / 总资产` = **ROA（盈利能力口径）**。
> 二者不是同一个量的不同归一方式，而是两个不同的量。

**机制的正确定义（替代 §一 的「缩放基本面」说法）**：

> **盈利收益率的自身偏离 = 估值重估动量。**
> `ts_av_diff(divide(科目, cap), W)` 衡量「当前盈利收益率比它自己过去 W 日均值高多少」——
> 即**基本面相对价格在改善**（要么盈利上修、要么估值下修尚未被价格反映）。
> 这类信号**天然携带价格信息**，所以塔位必然是 `PV + FUNDAMENTAL` 双塔，不可能做成纯 FUNDAMENTAL。

**三条连带结论**：

1. **纯 FUNDAMENTAL（不碰价格）路线在本数据集上被堵死**：`WjOKa3RZ` −0.21 / `wpQXn3k6` −0.07 说明「正确变换 + 会计分母」也不行。与既有 f17 dead_end（S 0.45）、f6 ceiling（S 0.37）方向一致 ⇒ **旧 dead_end 对「不含价格的基本面比率」判死是对的**，且补上了它们缺的那块证据（此前没测过 `ts_quantile(gaussian)` 变换，现在补测仍灭）。
2. **T3 vs T4 的归因歧义解除（方向确定）**：T3（`annual_ebitda_value/cap` + 裸 `ts_av_diff` 252）= 0.25，T4（`quarterly_ebit/cap` + gaussian 分位 66/22）= 1.59。批 2 证明换掉 `cap` 就归零 ⇒ 那么 T3 与 T4 的巨大差距**只能来自变换或字段频率**，不可能来自「有没有 `cap`」。⇒ **下一步必须做 T4e**（`annual_ebitda_value/cap` + 同款 gaussian 变换）来分离「变换」与「字段频率」。
3. **`fundamental17` 的塔位上限是 PV+FUNDAMENTAL，不是纯 FUNDAMENTAL**；要凑 FUNDAMENTAL 3/3，只能走这条双塔路线，且按「每个两塔组合候选 ≤3」封顶 ⇒ 该组合只剩 **2 个候选位**。

**附带观察（值得单独追）**：`WjOKa3RZ` 的 `investability_ratio` = 1.0952（>1），`wpQXn3k6` = −1.0。这两个是负夏普下的伪值，**不可解读为「大票暴露好」**；`investability_ratio` 只在正 S 时有意义。

### 6.7 批 3：分离「变换」与「字段频率」（已派发）

按 §6.6 结论 2，批 3 两条都回到 `/cap`（接受 PV+FUNDAMENTAL 双塔），各补一个维度：

| 编号 | 表达式 | 补齐的作用 |
|---|---|---|
| **T4d** | `rank(ts_quantile(ts_av_diff(divide(fnd17_0_fcfq, cap), 66), 22, driver=gaussian))` | **换分子**（EBIT 应计 → FCF 现金）⇒ 经济机制互异，目标是与 `omEQ9kK5` 低相关 |
| **T4e** | `rank(ts_quantile(ts_av_diff(divide(annual_ebitda_value, cap), 252), 22, driver=gaussian))` | **同字段同分母、只加变换**（对照 T3 的 0.25）⇒ 直接分离「变换贡献」与「年/季频率贡献」 |

两条均为 PV+FUNDAMENTAL 组合的第 2、3 个候选位。**若 T4e 也过闸** ⇒ 变换是主贡献、频率次要，且同族可量产；**若 T4e 灭而 T4d 成** ⇒ 季度频率是关键（年度字段披露稀疏、跳变过于集中）。

### 6.8 批 3 结果：变换是主贡献（10 倍），`/cap` 是门槛（2026-10-30 实测）

| alpha | 表达式要点 | S | F | TO | 2Y | SUB | fRA | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `Xg9XYOKz`（T3） | `annual_ebitda_value/cap` + **裸** `ts_av_diff(·,252)` | 0.25 | 0.09 | 4.05% | 0.77 | 0.16 | 3 | ❌ |
| **`E56oqo1r`（T4e）** | **同上字段/分母/窗口 + `ts_quantile(·,22,gaussian)`** | **2.39** | **2.11** | **16.17%** | **2.50** | **1.64** | **0** | ✅ **全闸** |
| `Xg9XkXm0`（T4d） | `fnd17_0_fcfq/cap` + 同款变换 | 0.61 | 0.26 | 11.27% | 1.44 | 0.33 | 3 | ❌ |

**这是本库最干净的一次归因**：T3 与 T4e 的字段（`annual_ebitda_value`）、分母（`cap`）、时间窗口（252）**完全相同**，唯一差异是**多了 `ts_quantile(·, 22, driver=gaussian)` 一步** ⇒ S 0.25 → 2.39（约 **10 倍**）。

⇒ **机制的两层结构现在都定量清楚了**：

| 成分 | 作用 | 反证 |
|---|---|---|
| `ts_quantile(·, 22, driver=gaussian)` | **主贡献**（×10） | 去掉它 → T3 0.25 |
| `/cap` 分母 | **必要条件（门槛）** | 换成总资产 → T4b −0.21 |
| 分子口径 | **只认应计利润（EBIT/EBITDA）** | 换 FCF → T4d 0.61 |

**为什么高斯分位这一步这么关键**（机理推断，待更多证据）：`ts_av_diff` 的输出在横截面上是**重尾**的（个别公司盈利收益率剧烈跳变），直接 `rank()` 会把这些极端值压成两头等权，丢掉中间的信息梯度；`ts_quantile(driver=gaussian)` 先把每只股票**自身近 22 日的偏离分布**映射为标准正态分位 ⇒ 输出是**单位方差、近似正态**的，再 `rank()` 时中间的梯度被保留。这等价于「先做时序上的概率积分变换，再做横截面排序」。

**T4e 的额外优势**：`risk_neutralized_sharpe` = **1.27**（`omEQ9kK5` 只有 0.40）⇒ 信号不依赖风格暴露，稳健性明显更好。

**这一批同时坐实了 §6.6 结论 1**：FCF 口径（`Xg9XkXm0` 0.61）也不成立 ⇒ 该机制**只对会计应计利润类科目成立**，对现金流科目不成立。后续科目池应收窄到 EBIT / EBITDA / EBT / 净利润这一类。

### 6.9 批 4：`current_enterprise_value` 解锁「纯 FUNDAMENTAL 塔」（2026-10-30 实测）

两条新分母，设置与前几批完全一致：

| alpha | 分母 | S | F | TO | 2Y | SUB | riskNeut | fRA | 塔位 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`rKRQbPPE`** | **`current_enterprise_value`** | **2.48** | **2.22** | 15.73% | **2.69** | 1.68 | **1.58** | 0 | **`GBR/D1/FUNDAMENTAL` 单塔**（effective=1，×1.6） |
| `P0ojnOOp` | `cap`（分子换总资产） | 2.30 | 1.96 | 17.31% | 2.42 | 1.59 | 未取 | 0 | PV+FUNDAMENTAL |

#### ★ 核心发现：`current_enterprise_value` 是「塔位杠杆」

`current_enterprise_value`（"Current enterprise value (market capitalization plus net debt)"）**是 fundamental17 自己的字段**，虽然它含市值，但数据集归属在 fundamental ⇒
**用 `divide(<科目>, current_enterprise_value)` 就能拿到「估值口径的分母」而完全不碰 PV 数据集的 `cap`。**

⇒ **FUNDAMENTAL 塔可以做成单塔**，不再受「trio 塔 × 非 trio 组合」的任何配额约束，也不需要 `PV+PV/PV+MODEL` 这类禁用组合。这是本会话最有价值的一条塔位杠杆。

**副产物**：`rKRQbPPE` 的 `risk_neutralized_sharpe` = **1.58**（`omEQ9kK5` 0.40 / `E56oqo1r` 1.27）⇒ 三条里稳健性最好，且 S 最高。**若只能提交一条，应选它。**

#### ★ 但互相关暴露了新墙：时间尺度才是去相关轴

4 条全闸候选的 mutual correlation（本地算，1021 个日收益点，4 年窗口）：

|  | omEQ9kK5 | E56oqo1r | rKRQbPPE | P0ojnOOp |
|---|---:|---:|---:|---:|
| **omEQ9kK5**（66 · EBIT · cap） | 1.00 | 0.5818 | 0.5435 | 0.5446 |
| **E56oqo1r**（252 · EBITDA · cap） | 0.5818 | 1.00 | **0.9617** | 0.8201 |
| **rKRQbPPE**（252 · EBITDA · EV） | 0.5435 | 0.9617 | 1.00 | **0.7934** |
| **P0ojnOOp**（252 · 总资产 · cap） | 0.5446 | 0.8201 | 0.7934 | 1.00 |

**读法**：
1. **`cap` → `EV` 换分母几乎不降相关**（`E56oqo1r` vs `rKRQbPPE` = **0.9617**，两者唯一差别就是分母）⇒ 经济含义几乎等价，只是塔位归属变了。
2. **把分母换成「总资产」能降一点**（0.79–0.82），但仍 >0.7 ⇒ 不够。
3. **唯一低相关的是 `omEQ9kK5`（66 快窗口）**，与三条慢窗口全部落在 0.54–0.58。
4. ⇒ **决定互相关的是 `ts_av_diff` 的时间尺度（66 快 vs 252 慢），不是分子也不是分母。**

**可用瓶颈**：`max_mutually_below_subset` = `{E56oqo1r, omEQ9kK5}`，size = **2**。即当前最多凑 2 条可同时提交，**点不了 FUNDAMENTAL 3/3**。

### 6.10 批 5：第三个时间尺度（已派发）

按 §6.9 结论 4，唯一的去相关杠杆是时间尺度，因此批 5 两条**都换到与已有两条不同的尺度**，且都用 `current_enterprise_value` 保持 FUNDAMENTAL 单塔：

| 编号 | 表达式 | 时间尺度 | 相对已有候选的差异 |
|---|---|---|---|
| **T4f** | `rank(ts_quantile(ts_av_diff(divide(quarterly_ebit_value, current_enterprise_value), 504), 22, driver=gaussian))` | **504（2 年）** | 第三尺度：既非 66（`omEQ9kK5`）也非 252（`rKRQbPPE`） |
| **T4g** | `rank(ts_quantile(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 66), 22, driver=gaussian))` | **66（季）** | 同 `omEQ9kK5` 尺度但**换分子到净利润**（税后/付息后，含杠杆效应）+ 换分母到 EV |

**窗口取值理由**：`504` = 2 年（白名单），对应**中期估值重估周期**（英国上市公司盈利预期的典型修复周期为 1–2 年，2 年窗口能容纳一轮完整重估）；`66` = 季度，与季报披露节奏对齐。

**验收标准**：任一条须同时满足
1. `failed_ra_count = 0`（全闸）；
2. 与新组合里另外两条 mutual corr **全部 < 0.7**；
3. 塔位含 `GBR/D1/FUNDAMENTAL`。

⇒ 若 `T4f` 或 `T4g` 达标，则 `{omEQ9kK5 或 rKRQbPPE, 另一条, T4f/T4g}` 三条可同时提交，**FUNDAMENTAL 0→3 点亮**。
⇒ 若两条都不达标，则本机制的互相关结构决定它在 GBR 只能出 2 条，需换机制（不是换字段）补第 3 条。

### 6.11 批 5 结果 + 互相关墙：一个机制只能出 2 条（2026-10-30 实测）

| alpha | 尺度/口径 | S | F | TO | 2Y | SUB | fRA | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **`j2YNnKOQ`（T4f）** | **504** · EBIT · EV | **2.15** | **1.80** | 15.37% | 2.09 | 1.41 | **0** | ✅ 全闸 |
| `3qogEvJ0`（T4g） | 66 · 净利润 · EV | 1.43 | **0.98** | 12.58% | 1.77 | 0.72 | 2 | ❌ F 差 0.02 |

#### ★ 决定性负面结果：5 条全闸候选凑不出 3 条可同时提交

5×5 mutual correlation（1021 个日收益点 / 4 年窗口 / 本地算，零配额）：

|  | omEQ9kK5<br><sub>66·EBIT·cap</sub> | E56oqo1r<br><sub>252·EBITDA·cap</sub> | rKRQbPPE<br><sub>252·EBITDA·EV</sub> | P0ojnOOp<br><sub>252·资产·cap</sub> | j2YNnKOQ<br><sub>504·EBIT·EV</sub> |
|---|---:|---:|---:|---:|---:|
| **omEQ9kK5** | 1.00 | 0.58 | 0.54 | 0.54 | **0.71** |
| **E56oqo1r** | 0.58 | 1.00 | **0.96** | 0.82 | **0.70** |
| **rKRQbPPE** | 0.54 | **0.96** | 1.00 | 0.79 | 0.70 |
| **P0ojnOOp** | 0.54 | 0.82 | 0.79 | 1.00 | 0.56 |
| **j2YNnKOQ** | **0.71** | **0.70** | 0.70 | 0.56 | 1.00 |

`max_mutually_below_subset` = **2**（枚举全部 C(5,3)=10 个三元组，**没有一个三对全 < 0.7**）。

**为什么压不下去 —— 三个杠杆实测排序**：

| 去相关杠杆 | 效果 | 证据 |
|---|---|---|
| 换分母（`cap` → `EV`） | **几乎无效** | `E56oqo1r` vs `rKRQbPPE` = **0.9617**（唯一差别就是分母） |
| 换分母（`cap` → 总资产） | 弱（0.96→0.79） | `P0ojnOOp` 与慢窗口族 0.79–0.82 |
| **换时间尺度**（66 / 252 / 504） | **有效但有底**（0.96→0.54~0.71） | `omEQ9kK5`(66) 与三条慢窗口全在 0.54–0.58；但 504 又贴回 0.70 |

⇒ **相关地板 ~0.54，尺度只能把 0.96 压到 0.70 就压不动了。** 根因：这 5 条虽然字段/分母/尺度各异，但都是**同一个经济因子「估值收益率偏离」**的不同采样。**换字段、换分母、换尺度都不是换机制。**

**这一条要写进方法论**：`compute_mutual_correlation` 的 `max_mutually_below_subset` 是判断「一个机制族能不能完成点塔」的**唯一可靠工具**，比逐条比指标有效得多。以后凑塔数应先算它，再决定是否继续在该族内派发。

### 6.12 批 6：找经济上正交的第二个机制（已派发）

要补第 3 条，必须换**经济机制**而不是换参数。选两个与估值无关的会计量，沿用已验证的 `ts_av_diff` + `ts_quantile(gaussian)` 变换（**变换是通用的、机制不是**），均为 FUNDAMENTAL 单塔：

| 编号 | 表达式 | 经济机制 | 文献先验 |
|---|---|---|---|
| **F1** | `rank(ts_quantile(ts_av_diff(divide(subtract(quarterly_net_income_3, fnd17_0_fcfq), quarterly_total_assets_2), 66), 22, driver=gaussian))` | **Sloan 应计质量**：(净利润 − 经营现金流)/总资产 的偏离 = 应计利润堆积 | Sloan 1996（应计异象：高应计 → 未来低回报）；Cohen-Malloy-Pomorski 2012 |
| **F2** | `rank(ts_quantile(ts_av_diff(divide(quarterly_total_liabilities_4, quarterly_total_assets_2), 66), 22, driver=gaussian))` | **杠杆扩张**：负债/总资产 的偏离 = 加杠杆速度 | Bhandari 1988（杠杆溢价）；Campbell-Hilscher-Szilagyi 2008（违约概率） |

**为什么这两条可能低相关**：它们的分子是「应计规模」和「负债结构」，与「盈利相对市值的贵贱」在机制上无关；而 §6.6 已证明**同样的变换配会计分母（EBIT/资产、FCF/资产）失败** —— 那两条失败的是**盈利能力**比率（与估值因子天然共线），不是这两条**资产负债结构**量。

**符号处理**：先按 `rank()` 原方向派发（高应计 / 高杠杆在前）。若读数为**显著负 S**（如 −1.5 以下），说明方向反了而非信号不存在 —— 平台下 `reverse()` 的 PnL 近似取负，一轮即可确认，**不算浪费槽位**。

**验收**：`failed_ra_count=0` 且与 `{rKRQbPPE, j2YNnKOQ}` 的 mutual corr 全 < 0.7 ⇒ 三条成组，FUNDAMENTAL 0→3。

### 6.13 批 6 结果：双灭 —— 但失败点被「会计分母」污染

multisim `27cCK78Au4GWcHib1hMOLMz`，设置全族一致（`INDUSTRY/decay10/trunc0.05/nan OFF/maxTrade OFF`）。

| 编号 | alpha | 表达式要点 | S | F | TO | 2Y | SUB | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| F1 | `xArXRk8g` | (净利−FCF)/**总资产** 66/22 | **0.25** | 0.07 | 7.63% | 0.21 | 0.16 | 3 |
| F2 | `58ENMO0k` | 总负债/**总资产** 66/22 | **0.16** | 0.04 | 7.58% | 0.20 | 0.35 | 3 |

**这是我自己的实验设计错误**：本节开工前刚在 §6.6 用两条负例（`WjOKa3RZ` −0.21、`wpQXn3k6` −0.07）证明了「**会计分母 ⇒ 盈利能力比率 ⇒ 无信号**」，转头又给 F1/F2 配了会计分母。所以这轮**没有检验「应计/杠杆机制是否成立」，只复现了「会计分母不成立」**。

⇒ 方法论铁律：**一个混杂变量被证伪后，后续实验必须把它锁在已证成立的那一侧（这里是 `EV`），否则实验不产生信息。** 换机制 ≠ 换分母；想换机制时，分母应沿用已证明有效的那个。

（F1/F2 用 EV 分母的版本已在 §6.15 重跑，见下。）

### 6.14 ★ 论坛复盘：`44089095804439` 直接给出本族的相关性根因（推翻 §6.11 的「机制单一」解释）

论坛帖《变便宜打败便宜——GBR 基本面比率 Δ-因子族的解剖、消融与模板化》（作者 YJ89646，6 赞，8 评论，2026-10-08）与我的机制**完全同源**，且作者已用它点亮 GBR 全部 5 座塔（18 条提交）。原文关键事实：

**① 作者的 hero 就是我的 `rKRQbPPE`（只差窗口）**
`rank(ts_quantile(ts_av_diff(divide(annual_ebitda_value, current_enterprise_value), 168), 56, driver=gaussian))`
→ S 2.71 / F 2.72 / TO 10.41% / 2Y 2.69 / SUB 1.59 / riskNeut 1.84 / **self 0.25 / prod 0.69**（prod 已贴 0.70 墙）。

**② ★ 相关性的真正根因：主贡献是「价格位移」，基本面分子只是调制器**
- 安慰剂 `Δ(1/市值)`（纯价格位移、零基本面信息）单独得 **S 1.89**，与 hero 相关 **0.72**。
- 评论者 ZC29904 进一步实测：`ts_quantile(ts_av_diff(divide(1, current_enterprise_value), N), M, driver=gaussian)` **单独就非常显著，甚至优于部分基本面分子**。
- 作者的后验**分子纯度**（与安慰剂的相关性）：**EEPS × 安慰剂 = 0.29（最纯）**；**债务/EV × 安慰剂 = 0.85（最脏——"债务÷EV"的位移几乎就是价格位移换皮）**。

⇒ **本族不是「5 个不同经济因子被同一机制采样」，而是「1 个价格位移因子 + 5 个不同纯度的调制器」。** 这解释了 §6.11 的相关地板 0.54：只要分母含市值/EV，价格位移分量就占主导，换分子只能调制、不能换因子。
⇒ **直接推翻 §6.11 的结论「换字段/分母/尺度都不是换机制」的后半句**：不是不能换机制，而是**换的分子纯度都太低**。要降相关，唯一有效的方向是**抬分子纯度**（或换数据集），不是换分母/换尺度。

**③ 作者给出的 FUND 单塔可用分子表（含 self/prod，可作 target 基准）**

| 分子 / 分母 | 窗口 | S | self/prod | 塔 | 备注 |
|---|---|---:|---|---|---|
| EBITDA / EV | 168/56 | 2.71 | 0.25 / 0.69 | FUND | = 我的 `rKRQbPPE` 机制 |
| 资本开支 / EV（`fnd6_capxy`） | 168/56 | 2.36 | 0.45 / 0.55 | FUND | ★ 纯度较高 |
| 折旧摊销 / 市值（`fnd6_dpy`） | 168/56 | 2.35 | 0.69 / 0.69 | FUND | 覆盖率敏感的稀疏字段 |
| 总债务 / EV | 84/28 | 2.05 | 0.57 / 0.70 | FUND | **纯度最低（0.85），勿再投入** |
| 归属净利 / 市值（`ttm_net_income_to_common`） | 168/56 | 1.99 | 0.65 / 0.69 | FUND | |
| 净利 / EV | 84/28 | 1.96 | **0.00** / 0.66 | FUND | ★ self=0.00 彩蛋 |
| 毛利 / 市值（`fnd6_gpy`） | 336/112 | 1.88 | 0.56 / 0.62 | FUND | |
| **经营现金流 / 市值（`fnd6_oancfy`）** | 168/56 | 1.65 | 0.56 / **0.56** | FUND | ★ **本表 prod 最低** |
| EPS 预测(best) / EV（`anl69_best_eeps_cur_yr`） | 168/56 | 2.57 | 0.46 / 0.64 | FUND+ANL | ★ **纯度最高 0.29** |

**④ 其它可直接采纳的结论（省实验预算）**
- **`driver` 在以 `rank()` 结尾的形态里是死参数**（数学上：`ts_quantile` 输出 = 经验分位经单调映射，最后一步 rank 抹掉一切单调差异；实测 gaussian→uniform **逐位一致**：PnL / TO / S 全同）。**不要再扫 driver。**
- 顺序：**先位移、后横截面 rank（2.71）** 优于先 rank 再位移（2.22，截面构成漂移制造伪位移）。
- 位移锚：均值锚 `ts_av_diff`（2.71）> zscore（2.28）> 对位锚 `ts_delta`（2.12）。
- 窗口：`168/56` 2.71 > `252/84` 2.43 > `84/28` 2.07；**N:M ≈ 3:1**（15 条骨架中 13 条）。
- 评论者 MY27687 提醒：`hero × 安慰剂 = 0.72` **已越过 0.70 门** ⇒ 「IS 全 PASS 不代表能交，prod 大概率卡门口」。**这与我 `rKRQbPPE` prod 未测的风险完全一致，必须在提交前实测。**

**⑤ 窗口白名单内的等价 3:1 组合**
白名单 `1/5/22/66/252/504/1008/1260` 里 **`66/22` 是唯一严格 3:1** 的组合（作者最优的 168/56 落在白名单外，需破例；84/28 同）。
⇒ **后续所有实验统一锁 `66/22`**（已由 `omEQ9kK5` 的 1.59 证明可用），除非专门做窗口破例实验。
---

## 七、批 7–9：把分母锁在 EV 上重测正交机制；换数据集

### 7.1 批 7（EV 分母重跑）：杠杆成立、应计仍灭

multisim `Vxc2VgLf52xacrdjRojZ8N`，设置全族一致（`GBR/TOP700/D1 · INDUSTRY · decay10 · trunc0.05 · nan OFF · maxTrade OFF`）。分母统一为 `current_enterprise_value`（§6.6 已证成立的那侧），锁 `66/22`。

| 编号 | alpha | 机制 | S | F | TO | 2Y | SUB | fRA | 结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F2′ | **`P0ojvkkJ`** | 总负债 / EV（杠杆水平） | **1.93** | **1.49** | 16.28% | 1.76 | 1.52 | **0** | ✅ **全闸** |
| F1′ | `9qxgJNnd` | (净利−FCF)/EV（应计） | 0.18 | 0.04 | 10.74% | −0.24 | 0.03 | 4 | ❌ 灭 |

**两条结论**：
1. **杠杆机制成立**，且 `P0ojvkkJ` 是**第 2 条 FUND 单塔全闸候选**（`pyramids.effective=1`、`GBR/D1/FUNDAMENTAL ×1.6`、`pyramid_short="fundamental"`）。它的 margin 11.95bp 是全族最高，riskNeut 0.61。
2. **Sloan 应计在 EV 分母下也灭**（0.18，且 2Y 为负）⇒ 应计机制在 GBR **确实不成立**，与分母无关。这是「换分母」这条纪律的正确用法：它排除了混杂，把「批 6 的双灭」从「设计错误」变成了「机制结论」。

### 7.2 ★★ 六条候选的互相关：第三次确认 `max_mutually_below_subset = 2`

`compute_mutual_correlation([rKRQbPPE, E56oqo1r, P0ojnOOp, j2YNnKOQ, omEQ9kK5, P0ojvkkJ], threshold=0.7, years=4)`（1021 点，`max_subset_exact=true`）：

|  | rKRQbPPE | E56oqo1r | P0ojnOOp | j2YNnKOQ | omEQ9kK5 | P0ojvkkJ |
|---|---:|---:|---:|---:|---:|---:|
| **rKRQbPPE** | 1.00 | 0.9617 | 0.7934 | 0.6964 | 0.5435 | **0.7014** |
| **E56oqo1r** | 0.9617 | 1.00 | 0.8201 | **0.7000** | 0.5818 | 0.7151 |
| **P0ojnOOp** | 0.7934 | 0.8201 | 1.00 | 0.5643 | 0.5446 | 0.8148 |
| **j2YNnKOQ** | 0.6964 | 0.7000 | 0.5643 | 1.00 | **0.7089** | 0.5219 |
| **omEQ9kK5** | 0.5435 | 0.5818 | 0.5446 | 0.7089 | 1.00 | 0.5866 |
| **P0ojvkkJ** | 0.7014 | 0.7151 | 0.8148 | 0.5219 | 0.5866 | 1.00 |

**7 对超线，且失败的都是毫厘之差**（0.7000 / 0.7014 / 0.7089）。三个「最想凑成」的三元组全部因**一对超线 0.001–0.015** 而失败：
- `{rKRQbPPE, j2YNnKOQ, omEQ9kK5}`：j2–om = **0.7089** ✗
- `{rKRQbPPE, j2YNnKOQ, P0ojvkkJ}`：rk–P0ojvkkJ = **0.7014** ✗
- `{omEQ9kK5, j2YNnKOQ, P0ojvkkJ}`：om–j2 = 0.7089 ✗

**方法论**：**相关地板 ≈ 0.52**，而 0.7 的门要求三条两两都在 0.52–0.70 这个**极窄带**里 —— 6 条候选随机落进这条带的概率很低。**这不是「再多试几组就能凑出 3 条」的问题，而是分布不支持。** 判断一个机制族能否完成点塔，必须在派发前就算 `max_mutually_below_subset`，而不是凑够 N 条再算。

### 7.3 批 8：换数据集 + forum 高纯度分子（`fundamental6`）—— 双灭

按 §6.14 的「抬分子纯度」指引，改用 `fundamental6` 的市值无关系分子（forum 实测 capex/EV 168/56 → 2.36、oancfy prod 0.56 为全表最低）。multisim `3G9W6FaGL4osbZDXX2KQNmm`，仍锁 `66/22` + `EV` 分母：

| alpha | 分子 | S | F | TO | 2Y | SUB | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `QPvmQnJ5` | `fnd6_capxy`（资本开支） | 0.60 | 0.30 | 12.51% | 0.72 | **−0.02** | 4 |
| `P0oj1nW7` | `fnd6_oancfy`（经营现金流） | 0.47 | 0.20 | 12.00% | 0.93 | **−0.12** | 4 |

★ **两条都是「S 正、SUB 负」**（`investability_ratio` 1.18 —— 只有大票有信号）。这与「`fnd6_*` 在 GBR/TOP700 覆盖仅 41%–62%」一致：稀疏字段在 66 日 Δ 上基本是噪声，信号残余只留在大票里。

### 7.4 ★ 反证：「只有 N:M 比例重要」是错的 —— 绝对窗口长度同样关键

§6.14 记下了 forum 的 `N:M ≈ 3:1` 规律。批 8 用**严格遵守 3:1** 的 `66/22`，同一分子却是 **2.36 → 0.60**（掉 4 倍）。而 `66/22` 在 `EBIT/cap` 上能出 1.59、在 `总负债/EV` 上能出 1.93。

⇒ **比例是必要不充分条件。** `66/22` 的绝对长度（~3 个月）对**季度级更新的利润科目**足够，对**半年报节奏的现金流量科目**不够（forum 原文明说 GBR 是半年报制、N=168 ≈ 1.33 个报告周期）。**窗口必须同时满足「比例 ≈3:1」和「绝对长度 ≳ 1 个报告周期」**，而 GBR 的报告周期是半年 ⇒ N 应 ≳ 126 天。

白名单 `1/5/22/66/252/504/1008/1260` 里同时满足「比例接近 3:1」与「N ≳ 126」的组合只有 **`252/66`（3.8:1）** 和 `504/1260` 不合比例。⇒ **下一轮该用 `252/66`**，而不是 `66/22`。

### 7.5 批 9：分母去市场化（会计÷会计），彻底切掉价格位移分量

§6.14 的根因是「分母含市值/EV ⇒ 价格位移分量主导 ⇒ 全族共线」。唯一的结构性解法：**让分母也来自会计科目**，使信号完全不含市场价值信息。文献依据 = 过度投资 / 资产增长异象（**Titman-Wei-Xie 2004**；Cooper-Gulen-Schill 2008）：

| 编号 | 表达式（`66/22`） | 经济机制 |
|---|---|---|
| G1 | `rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, fnd6_oancfy), 66), 22, driver=gaussian))` | **再投资强度** = 资本开支 / 经营现金流；其自身偏离 = 扩张速度异常 |
| G2 | `rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, fnd6_gpy), 66), 22, driver=gaussian))` | **资本开支 / 毛利** = 每单位毛利用多少钱去扩产 |

multisim `3knkEM2qs4VS9mnIdnXTi7o`。

**预注册判据（先写死）**：
- 若 G1/G2 的 `failed_ra_count=0` 且与 `{rKRQbPPE, j2YNnKOQ, P0ojvkkJ}` 的 mutual corr 全 < 0.7 ⇒ **FUND 0→3 达成**，且证明「去市场化分母」是有效的去相关杠杆。
- 若 G1/G2 指标达但相关 > 0.7 ⇒ 说明连「无市值分母」也逃不出价格位移的残余（可能来自 `INDUSTRY` 中性化本身引入的市场共同因子），FUND 需换 category 或接受只交 2 条。
- 若 G1/G2 指标不达 ⇒ 会计÷会计比率在 GBR 无信号，与 §6.6 的「纯基本面无 cap 11 条几何全灭」一致，FUND 的可用机制空间被压缩到「必须含市场价值」= 必然共线。
### 7.6 批 9 结果：会计÷会计双灭 —— 第三条预注册判据命中

multisim `3knkEM2qs4VS9mnIdnXTi7o`（`66/22`，`EV` 完全不出现在表达式里）：

| alpha | 机制 | S | F | TO | 2Y | SUB | margin | fRA |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `P0oj120x` | capex / OCF（再投资强度） | **−0.32** | −0.10 | 6.58% | −0.61 | −0.52 | −3.92bp | 4 |
| `akKXObjv` | capex / 毛利 | **0.10** | 0.02 | 6.76% | **0.96** | −0.08 | 1.20bp | 4 |

**命中预注册第三条**：「会计÷会计比率在 GBR 无信号 ⇒ FUND 的可用机制空间被压缩到『必须含市场价值』= 必然共线」。

两条读数的细节值得记下：
- `P0oj120x` 的 **S 为负**，而 Titman-Wei-Xie (2004) 的过度投资假说预测「capex/OCF 越高 ⇒ 未来收益越低」。**符号方向与经济预期一致** ⇒ 不是方向反了，是 `|S|=0.32` **强度不够**。这是「机制存在但太弱」，不是「机制不存在」。
- `akKXObjv` 的 **2Y = 0.96 但全期 S 只有 0.10** ⇒ 信号只活在近两年。这是 regime-dependent 的典型指纹，不是稳定异象。
- 两条 TO 都只有 ~6.7%（年报频率所致）⇒ 换手从来不是这个方向的问题。

### 7.7 ★★ 联合定论：本机制族的信号**就是**价格位移分量

四组独立实验、三种分母形式，全部指向同一点：

| 批 | 分母形式 | 表达式 | S | 结论 |
|---|---|---|---:|---|
| 2 | **会计**（总资产） | EBIT/总资产 | −0.21 | 灭 |
| 2 | **会计**（总资产） | FCF/总资产 | −0.07 | 灭 |
| 6 | **会计**（总资产） | (净利−FCF)/总资产 | 0.25 | 灭 |
| 6 | **会计**（总资产） | 总负债/总资产 | 0.16 | 灭 |
| 7 | **市值**（EV） | 应计/EV | 0.18 | 灭 |
| 9 | **会计÷会计**（无市值） | capex/OCF | −0.32 | 灭 |
| 9 | **会计÷会计**（无市值） | capex/毛利 | 0.10 | 灭 |
| 1–7 | **市值**（cap / EV） | EBITDA/EV、总负债/EV … | **1.59–2.48** | **活** |

**⇒ 定论：本族的信号本体 = 「估值倍数的自身位移」，即价格分量经会计分子调制。去掉市场价值分量（无论换成会计分母还是会计÷会计），信号即归零。**

这与 forum `44089095804439` 的安慰剂实验严格自洽：`Δ(1/市值)`（纯价格位移、**零基本面**）单独就有 **S 1.89**、与 hero 相关 **0.72**。既然纯价格位移本身就有 1.89，那么「价格分量」是信号的**主体**而非副产品 —— 会计分子只是调制器。

**这条定论的两个直接推论**：

1. **「换机制」在本族内的唯一有效形式是换「分子纯度」**（forum 的纯度表：EEPS×安慰剂 0.29 最纯 → 债务/EV 0.85 最脏）。本族的 6 条候选里，与 hero `rKRQbPPE` 相关**最低**的正是分子最不纯的 `omEQ9kK5`（EBIT/cap，纯会计量，**0.5435**）—— 但它 S 只有 1.59。**纯度与强度反向**，这是本族的结构性两难。
2. **FUND 塔凑不出 3 条不是「再找一个分子」能解决的**。0.7 门 + 相关地板 0.52 已经把可用带宽压到 0.18 宽，而本族任意两条的相关几乎必然落在 0.70–0.97。**必须换机制族、换数据集。**

### 7.8 六条候选的关键相关对（供选组时直接查表）

`compute_mutual_correlation(threshold=0.7)` 三次确认 `max_mutually_below_subset = 2`。需要第 3 条腿时，先查「与目标 2 条是否同时 < 0.7」：

| 候选 | 与 `rKRQbPPE` | 与 `j2YNnKOQ` | 与 `P0ojvkkJ` | S |
|---|---:|---:|---:|---:|
| `j2YNnKOQ` | **0.6964** ✓ | — | 0.5219 ✓ | 2.15 |
| `P0ojvkkJ` | 0.7014 ✗ | **0.5219** ✓ | — | 1.93 |
| `omEQ9kK5` | **0.5435** ✓ | 0.7089 ✗ | 0.5866 ✓ | 1.59 |
| `E56oqo1r` | 0.9617 ✗ | 0.7000 ✗ | 0.7151 ✗ | 2.39 |
| `P0ojnOOp` | 0.7934 ✗ | 0.5643 ✓ | 0.8148 ✗ | 2.30 |

**唯一稳定的 2 条组合 = `{rKRQbPPE, j2YNnKOQ}`（0.6964）**。其余组合都有一对落在 0.7000–0.7089 的「毫厘」区间 —— 那 0.0004–0.0089 的余量完全在 4 年 PnL 的抽样噪声里，**不值得为它微调**（即使调到 0.699 也是卡线，prod 侧一漂就死）。

## 八、GBR FUND 第二地基：`fundamental1` 治理 / 激励族

§7.7 的定论说明：FUND 塔不能继续在 `fundamental17` 的估值位移族里找第 3 条腿。必须换数据集。

### 8.1 数据集筛选（`category=fundamental` 在 GBR 共 12 个）

| dataset | 字段 | users | **alphas** | valueScore | 判定 |
|---|---:|---:|---:|---:|---|
| `fundamental17` | 135 | 1562 | **6973** | 1.0 | 已挖尽（估值位移族） |
| `fundamental6` | 197 | 1082 | 4069 | 2.0 | 覆盖 41–62%，批 8 双灭 |
| `fundamental72` | 552 | 246 | 586 | 4.0 | CONCENTRATED_WEIGHT 结构墙 |
| `fundamental86` | 7 | 214 | 380 | 2.0 | 仅 7 字段但 214 用户，拥挤 |
| `fundamental90` | 63 | 86 | 149 | 4.0 | 备选 |
| **`fundamental1`** | **124** | **40** | **69** | **6.0** | ★ **入选：拥挤度 1/100，valueScore 满档** |
| `fundamental45` | 12 | 44 | 73 | 4.0 | 全族已灭（earnings call sentiment） |
| `alpha_factor_lib` | 82 | 24 | 34 | 5.0 | 预计算因子库，非原始数据 |
| `fundamental89` | 42 | 8 | **13** | 6.0 | **判死**（见 8.2） |
| `fundamental93` | 17 | 6 | 13 | 5.0 | 备选（税务） |
| `fundamental22` | 1 | 8 | 11 | 5.0 | 仅 1 字段 |
| `digital_ad_spend` | 6 | 4 | 4 | 5.0 | 仅 6 字段 |

### 8.2 `fundamental89`（Accrual based Earnings Model）判死 —— 结构性问题，零成本即可证

42 个字段 = **14 个应计模型**（`best11` / `best21` / `csjonesallmajor13` / `csjonesallother11` / `csjonesindustrymajor13` / `csjonesindustryother11` / `fixed1313` / `fixed1513` / `jonesmajor13` / `jonesmajor31` / `jonesmajor32` / `jonesother11` / `jonesother14` / `jonesother15`）× **3 个变体**：

- `*_asset_double_history` —— 「公司资产曾在历史上某时翻倍」的 **0/1 指示器**
- `*_asset_half_history` —— 「资产曾减半」的 **0/1 指示器**
- `*_length` —— 应计比率的**观测数**（样本量）

**判死理由（无需回测）**：`*_history` 是**历史累积事件位** —— 一旦触发就恒为 1，十年窗口内不再变化。任何 `ts_delta` / `ts_av_diff` / `ts_zscore` 作用其上都会退化为常数或零方差 ⇒ 无信号。`*_length` 是样本量元数据，不是经济量。**42 字段里没有一个是一阶可用的经济量**，这解释了它为什么只有 13 个 alpha。

### 8.3 `fundamental1` 字段分类（124 个，**全部 VECTOR**）

| 类 | 字段数 | 代表字段 | 可用性 |
|---|---:|---|---|
| **A 薪酬结构（比率，天然无量纲）** | 4 | `equity_linked_compensation_ratio_2`、`bonus_proportion_total_comp`、`ltip_to_total_remuneration_ratio_2`、`compensation_change_percent_2` | ★★★ 直接可用 |
| **B 财富敏感度 delta** | 6 | `wealth_sensitivity_to_stock` / `_2`、`total_equity_linked_wealth` / `_2`、`total_shareholding_value` / `_2` | ★★★ 核心治理量（带货币单位，须 `rank()`） |
| **C 董事会结构（慢变量）** | 14 | `fnd1_filtered_numberdirectors`、`_succession`、`_attrition3yr`、`_genderratio`、`_stdevage`、`_stdevtimebrd`、`_stdevnoquals`、`_stdevtotcurrnolstdbrd` | ★★ 论文支撑强 |
| **D 董事个人特征** | 40 | `fnd1_board_characteristics_filtered_timebrd` / `_timeinco` / `_timerole` / `_noquals` / `_totcurrnolstdbrd` / `_timeretirement` / `_avgtimeothco` | ★★ `_timerole` 是 8 users / 8 alphas 的最热字段 |
| **E 期权 moneyness** | 8 | `option_strike_price_ltip`、`security_market_price_ltip`、`option_exercise_price`、`option_plan_stock_price` | ★★★ **同单位相除可得无量纲 moneyness** |
| **F 薪酬水平（货币）** | 18 | `aggregate_director_compensation` / `_2`、`annual_base_salary`、`annual_bonus_payment`、`total_remuneration_period`、`total_director_cash_comp` | ★ 混杂公司规模，forum 铁律 #4 说金额口径全灭 |
| **G 期权数量** | 14 | `*_option_quantity_ltip` / `_ltipw`、`*_option_volume` | ★ 股数口径 |
| **H 垃圾（货币代码）** | 5 | `compensation_currency_code` / `_2`、`monetary_unit_code_ltip` / `_ltipw`、`option_plan_currency_code` | ✗ 排除 |

**处理规约**：全部 VECTOR ⇒ 一律 `vec_avg(...)` 折叠（董事维度的平均值），再 `ts_backfill(·, 252)` 填年报阶梯。**注意 `vec_avg` 在稀疏场景易被单一高值主导**（forum `41420742165527`），所以薪酬/财富类字段的 `vec_avg` 结果要配合 `rank()` 做鲁棒化。

### 8.4 ★ 十条结构互异模板（论文来源已标注）

**设计约束（来自本会话已验证的事实，不是猜的）**：
- **必须用裸 `ts_` 几何**，`group_rank` 只能当对照 —— 我的实测：`group_rank` 的 `SUB/S` 只有 0.089–0.301 ⇒ GBR 必挂；裸 `ts_zscore` 是 0.447–0.630 ⇒ 过闸。
- **GBR 只有 TOP700，无 universe 退路** ⇒ forum 铁律 #5（「信号只在小票」靠换 universe 救）在 GBR **不可用**，必须在表达式内部解决。
- **比值只能作「信号定义」，不能作「信号合成」** ⇒ `divide(A,B)` 里 A/B 必须共同构成一个经济量（如 strike/price = moneyness），不能是「两个信号的比值」。

| # | 骨架几何 | 矩 | 经济机制 | 论文来源 |
|---|---|---|---|---|
| **T1** | `rank(ts_backfill(vec_avg(F),252))` | 0 阶水平 | 权益挂钩薪酬占比高 ⇒ 利益一致（**基准模板**） | Core & Guay 1999 |
| **T2** | `rank(ts_zscore(ts_backfill(vec_avg(F),252),504))` | 自身基线偏离 | delta 相对自身历史异常升高 = 治理质量阶段性改善 | forum 43152032301591（铁律 #3） |
| **T3** | `rank(ts_av_diff(ts_backfill(vec_avg(F),252),504))` | 1 阶差分 | 权益比例**上升** ⇒ 激励向长期倾斜 | 自建（T1 的动量版） |
| **T4** | `rank(ts_quantile(ts_av_diff(ts_backfill(vec_avg(F),252),504),22,driver=gaussian))` | 1 阶 + 高斯分位 | 位移的高斯分位 = 幅度保留的非线性（本会话招牌，`omEQ9kK5` 曾靠它 ×10） | 自建（§6.3） |
| **T5** | `rank(divide(ts_backfill(vec_avg(A),252), ts_backfill(vec_avg(B),252)))` | 0 阶，**同单位比值** | **期权 moneyness** = strike / price，深度价外 ⇒ 管理层有强动力推高股价 | 自建（期权激励理论） |
| **T6** | `rank(ts_backfill(vec_avg(stdev_F),252))` | **2 阶离散度** | 董事任期标准差大 ⇒ 经验互补 + 知识传承（Yermack 1996 的对偶） | 自建（团队多样性） |
| **T7** | `rank(divide(rank(ts_backfill(vec_avg(A),252)), rank(ts_backfill(vec_avg(B),252))))` | 秩比秩（密度） | 人均治理成本 = 总薪酬 / 董事人数（**必须先各自 `rank()` 才同单位**） | 自建 |
| **T8** | `rank(ts_rank(ts_backfill(vec_avg(F),252),504))` | 时序序数 | 当前水平在自身 2 年历史中的分位（**对照 T2：序数 vs 幅度保留**，forum 铁律 #2 说 zscore 应胜） | forum 43152032301591 |
| **T9** | `rank(ts_sum(ts_backfill(vec_avg(F),252),252))` | 长期累积 | 薪酬结构的两年累积水平（forum 铁律 #3 的「聚强度」） | forum 43152032301591 |
| **T10** | `group_rank(ts_backfill(vec_avg(F),252), subindustry)` | 分组轴 | 行业内治理排名（**预注册：预期 SUB 挂**，用于证实 `group_rank` 在 GBR 的 SUB 墙） | 本会话实测反例 |

**论证覆盖**：T1/T3/T4 是同一字段的「水平 / 一阶 / 非线性一阶」，T2/T8/T9 是「幅度保留 / 序数 / 累积」，T5/T7 是两种比值（同单位 vs 秩比秩），T6 是唯一的二阶矩，T10 是唯一的分组轴且为对照。**十个模板落在五个不同几何维度上**，不是换窗口。

### 8.5 与 forum 铁律的冲突点（必须先解决）

§7.7 的定论说「价格位移分量是信号的物理本体」（在 `fundamental17` 族）。但 `fundamental1` 的治理字段**完全不含价格信息**（薪酬、董事人数、任期都是会计/人事量，唯一含价格的是期权行权价与 delta）。

⇒ **`fundamental1` 若出信号，那它一定不是价格位移** —— 这正是它作为「去相关腿」的价值。但也意味着**本会话积累的「估值位移」全部经验（高斯分位、分子纯度、N:M≈3:1）可能不transfer**。

**预注册判据（派发前先写死，防止事后找故事）**：
1. 若 T1–T9 全部 `|S| < 0.8` ⇒ `fundamental1` 在 GBR/TOP700 无信号，与 forum 作者对 `board_gov_stats` 的判词（「董事会治理属慢变量，与行为反应机制不匹配」）一致 ⇒ **FUND 塔在 GBR 的可用机制空间确实枯竭**，应转向 PV / OTHER 塔（各需 2）。
2. 若 T1–T9 中有 `S > 1.3` 且 `fRA=0` ⇒ 得到**独立于估值位移族**的新腿，直接验它与 `{rKRQbPPE, j2YNnKOQ}` 的 mutual corr（预期远低于 0.52 的相关地板）。
3. 若信号**只在某几个字段上强、其余全灭** ⇒ 按字段归因，不按模板归因（说明是数据质量而非几何问题）。

### 8.6 批 10–11 实测：`fundamental1` 的换手恒为 2% —— 指向「无时间维度」

**批 10（T1 水平秩，multisim `177R2z44K4Nacrj8PUK8o86`）**

| alpha | 字段 | S | F | **TO** | 2Y | SUB | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `LLMOpl9n` | `wealth_sensitivity_to_stock` | 0.11 | 0.02 | **1.78%** | −0.69 | 0.03 | 4 |
| `P0ojpXZx` | `fnd1_filtered_succession` | 0.24 | 0.06 | **2.16%** | −0.35 | 0.13 | 3 |

`LLMOpl9n` 实读：`longCount=276` / `shortCount=270` ⇒ **持仓 546 只，TOP700 覆盖正常**（探针目的达成：数据真的有值）；
`pyramids.effective=1` / `list=[{GBR/D1/FUNDAMENTAL, 1.6}]` / `pyramid_short="fundamental"` ⇒ **FUND 单塔，配额干净**；
`checks.pass` 含 `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `MATCHES_PYRAMID` ⇒ **无 CW 墙**；`drawdown` 0.2211。

**批 11（T2 自身基线 zscore，multisim `1tT91s8OW4Ce9YvmZrHs7IT`）**

| alpha | 字段 | S | F | **TO** | 2Y | SUB | margin | fRA |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `0mYn7ZYK` | `compensation_change_percent_2` | −0.19 | −0.04 | **1.96%** | −0.84 | 0.04 | −0.67bp | 3 |
| `2rAP7VA5` | `equity_linked_compensation_ratio_2` | −0.67 | −0.30 | **2.04%** | −0.55 | −0.55 | −2.54bp | 4 |

**★ 关键异常：四条实验、两种几何（T1 水平秩 / T2 自身基线偏离）、A/B 两类字段，换手全部锁在 1.78%–2.16%。**

这不是「信号弱」，而是**数据在时间维度上几乎不动的指纹**。判据：
- 真实年报/半年报数据在 TOP700 上做 `ts_backfill(·,252)` + rank 收尾，年化换手**不可能**只有 2% —— 光靠每年新增一次披露引起的截面重排，就应产生 20%–60% 量级。
- 2% 量级只可能来自「宇宙成员变动 + NaN 处理」这类边界噪声，即**截面排序本身几乎恒定**。
- 4/4 条独立命中同一换手档位，不可能是巧合。

**⇒ 假设 H-F1：`fundamental1` 在 GBR/TOP700 是「单点快照式」供给 —— 每家公司只有一个（或极少）有效观测，`ts_backfill` 把它向后无限延拓 ⇒ 任意 `ts_` 时序算子退化为常数。**
若 H-F1 成立，则 T2/T3/T4/T8/T9（全部依赖时序变化）在**派发前就已结构性死亡**，只有 T1（截面水平）可能有效，而 T1 实测 0.11 / 0.24。

**判据 3 命中（事前预注册：「若信号只在某几个字段上强、其余全灭 ⇒ 按字段归因，说明是数据质量而非几何问题」）**：
本批不是「某几个字段强」，而是**全部字段的时序维度都不动** ⇒ 归因到**数据集供给形态**，不是字段选择，也不是几何选择。

**决定性诊断试验（批 12，multisim `3v9N9K4OI57L9WXt2eeY9Np`）**：改用 **B 类 `wealth_sensitivity_to_stock`（delta，含股价分量，若数据真实必然随时间动）**：
1. `rank(ts_delta(ts_backfill(vec_avg(wealth_sensitivity_to_stock), 252), 252))` —— T3 一阶差分（YoY）
2. `rank(ts_std_dev(ts_backfill(vec_avg(wealth_sensitivity_to_stock), 252), 1008))` —— T6 二阶离散度

**预注册判据（写死，防事后找故事）**：
- 若两条 TO 仍 ≤ 3% 且 |S| < 0.5 ⇒ **H-F1 成立**：连「含股价分量的 delta」都不动，说明数据是冻结快照 ⇒ `fundamental1` 在 GBR 判死（结构原因，非信号原因），FUND 塔在 GBR 的可用机制空间确认枯竭，转 PV / OTHER 塔。
- 若 TO 跳到 > 10% ⇒ **H-F1 被推翻**，说明时间维度存在，那么批 11 的失败是几何问题（zscore 长窗把信号摊平），应改短窗/改分位。
- 若 TO 居中（3%–10%）且 |S| 明显（> 0.8）⇒ 换手是字段级属性，按字段筛选。

### 8.7 ★★ 批 12 裁决：`fundamental1` 在 GBR 判死 —— 「冻结快照，无时间维度」

**批 12（决定性诊断，multisim `3v9N9K4OI57L9WXt2eeY9Np`）**

| alpha | 几何 | 字段 | S | F | **TO** | 2Y | SUB | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `MPY9Q1Ok` | T3 `ts_delta(·,252)` | `wealth_sensitivity_to_stock` | 0.46 | 0.20 | **3.04%** | 0.62 | 0.00 | 4 |
| `pwdQlPmj` | T6 `ts_std_dev(·,1008)` | `wealth_sensitivity_to_stock` | −0.11 | −0.02 | **1.41%** | −1.00 | −0.14 | 4 |

选 `wealth_sensitivity_to_stock` 做裁决字段的理由：它是 **delta（财富对股价的敏感度 = 持股数 × 股价敏感）**，若数据是活的，**必然随股价逐日变动**。连它都不动，其它字段不必再测。

**★ 同设置下的内部控制（这是判定的关键，不是推理而是对照）**

| alpha | 数据集 | 字段类型 | 设置 | **TO** |
|---|---|---|---|---:|
| `rKRQbPPE` | `fundamental17` | **年报** EBITDA / EV | INDUSTRY · decay10 · trunc0.05 · nanOFF · maxTradeOFF | **15.73%** |
| 批 10–12 全部 6 条 | `fundamental1` | 年报薪酬 / 董事 / delta | **完全相同** | **1.41%–3.04%** |

⇒ **同一套设置下，年报基本面数据集能产出 15.73% 换手，而 `fundamental1` 的六条实验全部落在 1.4%–3.0%。差 5–10 倍 ⇒ 低换手是数据集属性，不是设置属性（不是 decay 10 把换手压掉的）。**

**六条实验汇总（4 个结构互异模板 × A/B 两类字段）**

| 批 | alpha | 模板 | 字段 | S | TO |
|---|---|---|---:|---|---:|
| 10 | `LLMOpl9n` | T1 水平秩 | `wealth_sensitivity_to_stock`（B） | 0.11 | 1.78% |
| 10 | `P0ojpXZx` | T1 水平秩 | `fnd1_filtered_succession`（C） | 0.24 | 2.16% |
| 11 | `0mYn7ZYK` | T2 自身基线 | `compensation_change_percent_2`（A） | −0.19 | 1.96% |
| 11 | `2rAP7VA5` | T2 自身基线 | `equity_linked_compensation_ratio_2`（A） | −0.67 | 2.04% |
| 12 | `MPY9Q1Ok` | T3 一阶差分 | `wealth_sensitivity_to_stock`（B） | 0.46 | 3.04% |
| 12 | `pwdQlPmj` | T6 二阶离散 | `wealth_sensitivity_to_stock`（B） | −0.11 | 1.41% |

**裁决（命中预注册判据 1，且诊断强于「信号弱」）**：
- 全部 `|S| ≤ 0.67 < 0.8` ✅ 命中判据 1。
- 但真实原因是 **H-F1 成立**：数据在时间维度上冻结。
- **★ 时序几何（T2/T3/T4/T8/T9）与水平几何（T1/T5/T7）在本数据集上同时失效**：T1 是水平几何的典范，实测 0.11/0.24；既然**连水平秩都只有 2% 换手**，那么 T5/T7 这两个「对水平量的截面变换」也不可能翻身 —— 它们换的是**测的物理量**，不是**几何维度**。
- 残余未测：T5（期权 moneyness，`option_strike_price_ltip / security_market_price_ltip`）是唯一可能带活价链的字段组合。**预期值近零**（若 market price 字段是活的，`wealth_sensitivity_to_stock` 的 delta 就该活；它没活）。

**⇒ `fundamental1` 在 GBR/TOP700 判死，理由 = 供给形态（冻结快照），不是字段选择、不是几何选择、不是设置选择。**

**对 GBR FUND 塔的战略含义（重要）**：
- FUND 塔第 3 条腿不能来自 `fundamental1`。
- 已试尽 / 已判死的 FUND 地基：`fundamental17`（估值位移族，相关地板 0.52 ⇒ 最多 2 条）、`fundamental6`（批 8 双灭，SUB 负）、`fundamental45`（earnings call 全族灭）、`fundamental89`（结构判死）、`fundamental1`（本次，冻结快照）。
- **剩余 FUND 候选地基**：`fundamental90`（63 字段 / 86 users / 149 alphas / valueScore 4.0）、`fundamental93`（税务，17 字段 / 6 users / 13 alphas）。`fundamental72`（552 字段）有 `CONCENTRATED_WEIGHT` 结构墙。
- **优先级判断**：FUND 塔从 0→3 的路已被压缩到「两个未验证的备选数据集」，而 PV 需 2、OTHER 需 2 完全未开工。按「点塔要均匀」的准则，**先把 OTHER 塔的 2 个塔位做出来（`other567` 月度面板已预检通过），再回头啃 `fundamental90`**。
---

## 九、`fundamental17` 现成比率字段：用已验证骨架同时补 FUND 与 PV 两塔（批 16）

### 9.1 转折点：塔位由「字段所属数据集的 category」决定，不由字段语义、也不由我拼的表达式决定

> **⚠ 2026-10-30 修正（批 17 实证推翻原表述）**
>
> 本节原标题为「塔位由**字段**决定」，并在 §9.2 把 `daily_volume_to_shares_outstanding` 等 6 个 PV 语义字段标成 **PV 塔**。**这是错的。**
>
> 决定性实测：批 17 的 `A1Vql6AR`（换手率量比，**语义上是纯 PV**）实读 `get_alpha_details`：
> ```
> pyramids.list = [{ name: "GBR/D1/FUNDAMENTAL", multiplier: 1.6 }]
> ra.pyramid_short = "fundamental"        pyramids.effective = 1
> ```
> ⇒ **FUNDAMENTAL 单塔**。原因：`daily_volume_to_shares_outstanding` 属于 `fundamental17`（**FUNDAMENTAL** category），而塔位按字段**所属数据集的 category** 归属。
>
> 对照证据：`cap` 属于 PV 数据集 ⇒ `divide(X, cap)` 的塔位里才出现 `GBR/D1/PV`。同一个 `daily_volume_to_shares_outstanding` 若来自 PV 数据集就会是 PV 塔，但它来自 `fundamental17`。
>
> **⇒ 正确判据：塔位 = 字段所属数据集的 `category`，与字段名称/语义无关。**
> **⇒ 推论：`fundamental17` 的 135 个字段，无论语义上是价、量、还是比率，全部落在 FUNDAMENTAL 塔。PV 塔无法从 `fundamental17` 内部取得任何字段。**


前八节的骨架一直是 `divide(<分子>, <分母>)`，分母由我自己拼，**塔位于是被我的拼法绑死**：
- `divide(X, cap)` → `PV + FUNDAMENTAL` 双塔（吃「两塔组合 ≤3」配额，已用满 3 位：`E56oqo1r` / `P0ojnOOp` / `omEQ9kK5`）
- `divide(X, current_enterprise_value)` → `FUNDAMENTAL` 单塔（绕开配额，§6.14 最重要的杠杆）

而 `fundamental17` 的 135 个 MATRIX 字段里有一批**「分母已在字段内部」的现成比率** ⇒ 我不再需要拼分母，塔位由平台对该字段的归类决定，可以**按塔选字段**、精准补缺口。相比「找新数据集」，这条路便宜得多：

1. 该数据集已被证实有日频/季频时间维度（§6.14 内部控制：同设置下 `rKRQbPPE` TO **15.73%**，而 `fundamental1` 六条实验 1.41%–3.04%，差 5–10 倍）；
2. 比率字段**无量纲** ⇒ 完全规避 `unit_handling=VERIFY` 的单位闸（本项目历史上反复栽在「带单位字段 + 常数」上）；
3. 骨架已被验证：`rank(ts_quantile(ts_av_diff(<X>, W), 22, driver=gaussian))` 在本会话产出 **6/12 全闸候选**，是全库产出率最高的形态。

### 9.2 现成比率字段清单（`get_datafields` 实读 135/135，`complete: true`）

> **⚠ 2026-10-30 修正**：原表按字段语义标塔位，把 6 个「价 / 量」字段标成 PV。**全部错误** —— 它们都在 `fundamental17` 内 ⇒ 全是 **FUND**（见 §9.1 修正说明）。下表塔位列已改正。

| 字段 | users / alphas | 塔位 | 机制语义 |
|---|---|---|---|
| `quarterly_operating_margin_percent_4` | 86 / 106 | **FUND** | 营业利润率 %（批 16 实测 S −0.16） |
| `quarterly_pretax_margin_percent_4` | 86 / 115 | **FUND** | 税前利润率 % |
| `quarterly_return_on_equity_percent_3` | 201 / 582 | **FUND** | ROE % |
| `enterprise_value_to_revenue` | 288 / 858 | **FUND** | EV/Revenue（**是 `EBITDA/EV` 的倒数族 ⇒ 高共线，不用于凑数**） |
| `annual_price_to_sales_ratio` | 159 / 312 | **FUND** | P/S（同上，估值倍数族） |
| `quarterly_price_to_sales_ratio_4` | 247 / 739 | **FUND** | P/S（同上） |
| `quarterly_working_capital_per_share_to_price_3` | 10 / 11 | **FUND** | 营运资本/股价 |
| `daily_volume_to_shares_outstanding` | 201 / 588 | ~~PV~~ → **FUND** | 换手率（量/流通股）—— **★ 批 17 产出 FUND 单塔最佳新候选 `A1Vql6AR` S 1.28** |
| `ten_day_avg_volume` | 65 / 123 | ~~PV~~ → **FUND** | 10 日均量（**带单位，慎用**） |
| `one_day_avg_volume` | 25 / 33 | ~~PV~~ → **FUND** | 单日均量（带单位） |
| `twelve_month_high_price` | 20 / 21 | ~~PV~~ → **FUND** | 52 周新高价（带单位，需自身归一） |
| `one_fifty_day_avg_price` | 9 / 14 | ~~PV~~ → **FUND** | 50 日均价（带单位） |
| `two_hundred_day_avg_price` | 5 / 10 | ~~PV~~ → **FUND** | 200 日均价（带单位） |

**★ 这张表对本会话的战略含义已经被改写**：原本指望「用 `fundamental17` 的 PV 语义字段补 PV 塔」是**这条路上最贵的误判** —— 它让我以为 PV 塔有候选了，实际 PV 塔从头到尾是 0 路径。修完这条错误后结论是：
- **FUND 塔**：`fundamental17` 内部有充足材料（估值位移族 6 条 + 量比族 1 条）。
- **PV 塔**：必须去真正的 `category=pv` 数据集。GBR 有 16 个，其中 7 个从未尝试过，`pv20`（675 字段 / 699 alphas / 自带 beta 期限结构）是最优先入口。


**关键取舍（防重复造轮子）**：`enterprise_value_to_revenue` / `annual_price_to_sales_ratio` / `quarterly_price_to_sales_ratio_4` 三者在经济上是**估值倍数的倒数**，与 §6.14 的 hero `EBITDA/EV` 是同一物理量的不同写法 ⇒ 拿它们做 Δ 必然与现有 6 条高度共线，**不投入**。真正的新信息在**利润率的 Δ**（盈利质量维度）与**换手率**（流动性维度）。

### 9.3 批 16 设计（2 条，multisim `4arL5mdgv55fbw8fWKr4fBj`）

| # | 目标塔 | 表达式 | 机制 |
|---|---|---|---|
| A | **FUND** | `rank(ts_quantile(ts_av_diff(ts_backfill(quarterly_operating_margin_percent_4, 66), 252), 22, driver=gaussian))` | **营业利润率同比改善** = 盈利动量 |
| B | **PV** | `-rank(ts_quantile(ts_av_diff(ts_backfill(daily_volume_to_shares_outstanding, 22), 66), 22, driver=gaussian))` | **换手率三月变化**（负向）= 换手率异象 / 异常成交量 |

窗口理由：`quarterly_operating_margin_percent_4` 是季频字段 ⇒ `ts_backfill(·, 66)` 填一个季度（66 交易日 ≈ 3 个月），`ts_av_diff(·, 252)` 做**一年同比**（覆盖 4 个季度、跨掉季节性），`ts_quantile(·, 22)` 取最近一月的时序分位并做高斯化（这一层在 §6.5 贡献过 0.25 → 2.39 的 ×10）。`daily_volume_to_shares_outstanding` 是日频 ⇒ `ts_backfill(·, 22)` 只补数据缺口，`ts_av_diff(·, 66)` 取季度级变化（避开 5 日噪声，与 Lee-Swaminathan 的月度换手中枢对齐）。

### 9.4 预注册判据（先写判据，再看读数）

1. **两条都 |S| < 0.8** ⇒ 「现成比率字段」这条路也不成立 ⇒ 与 §7.7 合并为更强的定论：**GBR/TOP700 的 FUND 塔只能用含市值位移的估值比率**，FUND 第 3 条腿只能去 `fundamental90`（CHS 违约概率 / Piotroski F / NOA）碰，且必须换机制维度（质量 vs 估值）。
2. **FUND 条 S ≥ 1.0** ⇒ 「Δ 盈利质量」是**独立于估值位移**的机制（§7.7 的适用范围收窄为「估值比率族」，不覆盖利润率）⇒ 可立刻铺 `quarterly_pretax_margin_percent_4` / `quarterly_return_on_equity_percent_3` 两个变体做三角测量。
3. **PV 条 S ≥ 1.0** ⇒ 换手率异象在 GBR 成立 ⇒ PV 塔 0→2 有路，继续铺（水平换手率、异常成交量、换手率×收益交互）。
4. **方向风险（预注册）**：换手率方向存在文献冲突 —— Lee-Swaminathan (1999) / Datar-Naik-Radcliffe (1998) 给**负向**（低换手 → 高收益，流动性溢价）；Gervais-Odean-Mingelgrin (2001) 的 high-volume return premium 给**正向**（高量后短期反弹）。本批取负向（与 Amihud 2002 流动性溢价的符号一致）；若读数呈明确反向且 |S| 可观，翻符号重测一次（**这是符号校正，不是混信号调参**）。
5. **风险提示（预注册）**：批 8（`fnd6_capxy`/`fnd6_oancfy` ÷ EV）与批 9（会计 ÷ 会计）已证明**会计分母全灭**。利润率的隐含分母是**营收**（会计口径）⇒ 判据 1 若命中，与批 8/9 是同一根因（缺市值位移分量）。

---
## 十、`bucket` 经济状态分桶：解开「同机制互相关地板 0.52」的横截面轴

### 10.1 问题定位（来自 forum `44174743998999`，YJ75326，26 赞 / 9 评论）

该帖把「PC 撞墙」的根因说得比我之前清楚得多：

> 不同顾问产生的 Alpha，虽然原始公式不同，但**都拥有相似的横截面结构**。大量 Alpha 用 `group_neutralize(..., industry)` / `group_rank(..., subindustry)`，最终导致 PC 过高。

这正好是我 §7.8 的处境：6 条全闸候选、`failed_ra_count=0`，但**互相关地板 0.52、`max_mutually_below_subset = 2`**（三次确认）。我之前把它解释为「机制太单一 ⇒ 必然共线」，现在有更准确的解释：**是横截面处理同质化，而不只是信号本身共线**。`rKRQbPPE` / `E56oqo1r` / `P0ojnOOp` / `j2YNnKOQ` / `omEQ9kK5` / `P0ojvkkJ` 全部走 `INDUSTRY` 中性化 + 同样的 `rank(ts_quantile(...))` 外层 ⇒ 横截面结构逐位同形。

### 10.2 `bucket` 的语义与语法（本账号尚未实测，落地前须单条验证）

| 项 | 内容 |
|---|---|
| 语义 | GROUP 字段回答「股票**属于什么类别**」；`bucket` 回答「股票**当前处于什么市场状态**」 |
| 基本语法 | `bucket(rank(<expr>), range='0.1,1,0.1')` ⇒ **10 桶**；`bucket(rank(<expr>), range='0.2,1,0.2')` ⇒ **5 桶** |
| 可替换位置 | 评论（LE69726）：「group 系列的算子中**中性化的位置**可以直接被 bucket 替换」⇒ `group_rank(x, bucket(...))` / `group_neutralize(x, bucket(...))` 均合法 |
| 二维组合 | `group_cartesian_product(bucketA, bucketB)` |
| ★ 桶数选择 | 原帖第 08 节：`TOP3000+ → 10` / `TOP1000~3000 → 10` / **`TOP500~1000 → 5~10`** / `TOP200~500 → 5` / 小宇宙 `3~5` ⇒ **GBR TOP700 应用 `range='0.2,1,0.2'`（5 桶）** |
| ★ 薄桶护栏 | 评论（XZ93204）：`zscore` 类桶成员会漂，尾部桶可能只剩几只票；「3 只股票的桶是噪声不是结构」，建议 `group_count(x, bucket) > 5` 护栏。**但 `group_count` / `group_median` 在部分账户不可用，且会导致整包 CANCELLED**（评论 LY66036）⇒ 本账号 `group_count` 未验证，暂不加护栏，改用 5 桶 + 事后看持仓数 |
| ★ 换手率代价 | 评论（WS29639）：20D 短周期桶会在分位线边缘反复横跳冲爆 turnover；**66D / 252D 配合 `ts_mean` 钝化更平稳** ⇒ 桶的度量层用 `ts_mean(·, 252)` 或 `ts_backfill(·, 66)` |

### 10.3 ★★ 塔位约束（**⚠ 2026-10-30 前提被证伪，整节重写**）

> **原节标题为「换手率桶不能给 FUND 单塔用」，前提是「`daily_volume_to_shares_outstanding` 是 PV 塔字段」。该前提已被批 17 推翻** —— 它属于 `fundamental17`（FUNDAMENTAL category）⇒ **它就是 FUND 塔字段，完全可以给 FUND 单塔的 alpha 当桶轴**。
>
> 所以原节的「硬约束」不存在。但结论仍然成立，**理由换成更本质的那个**：

`fundamental17` 内最容易想到的桶是**换手率状态桶**（原帖模板 6）：
`bucket(rank(ts_mean(<换手率>, 20)), range='0.2,1,0.2')`
本数据集对应字段 = `daily_volume_to_shares_outstanding`（**FUND 塔**，无塔位冲突）。

**⇒ 真正的问题是「自我中性化」，不是塔位。**

若把这个桶挂在**换手率信号自身**上（`A1Vql6AR` 族），等于「按信号自己的取值分组，再在组内去均值」⇒ **把信号本身的信息量抹掉**。这是统计学上的循环，不是合规问题。

**⇒ 正确用法分两类：**
1. **桶轴 = 与被中性化信号不同的经济维度** ⇒ 合法且有信息增益。给估值位移族（`rKRQbPPE` 等 EBITDA/EV 类）挂**换手率状态桶** = 用「流动性状态」切「估值重估动量」，两个维度正交 ⇒ **这条现在不仅合法，还是 §10 原本想要的降相关工具**。
2. **桶轴 = 信号自身** ⇒ 自我中性化，无意义。

**可用替代（全部 FUND 塔字段，无塔位冲突）：**

| 桶轴 | 字段 | users / alphas | 经济状态 |
|---|---|---|---|
| **ROE 状态桶** | `quarterly_return_on_equity_percent_3` | 201 / 582 | 高/低资本回报状态 |
| **利润率状态桶** | `quarterly_operating_margin_percent_4` | 86 / 106 | 高/低经营效率状态 |
| **税前利润率桶** | `quarterly_pretax_margin_percent_4` | 86 / 115 | 高/低税负前效率状态 |
| **规模状态桶** | `current_enterprise_value` | 517 / 1467 | 大/小企业价值状态 |
| **市值状态桶** | `market_capitalization_value_5` | 224 / 714 | 大/小市值状态 |
| **现金流状态桶** | `fnd17_0_fcfq` | 481 / 1157 | 强/弱自由现金流状态 |
| **杠杆状态桶** | `quarterly_total_liabilities_4` | 11 / 11 | 高/低杠杆状态 |

（**⚠ 原句已作废**：原写「换手率桶只能用于 PV 单塔的 alpha … 在本会话没有实际用途」。修正后：换手率桶是 **FUND 塔字段**，且它的正确用途正是 §10.1 要解决的问题 —— 给**估值位移族**当第二个横截面轴，用来打散 6 条候选同形的 `INDUSTRY` 中性化结构。**这是 §10 的首选落地实验，不是无用的桶。**）

### 10.4 为什么 `group_neutralize(·, bucket)` 而非 `group_rank(·, bucket)`

本会话已实测（memory 铁律）：**`group_rank` 是 SUB 杀手** —— 同一数据集同一信号族，`SUB/S` 从 0.447–0.630（无外层）掉到 0.089–0.301（`group_rank`），全部撞 `LOW_SUB_UNIVERSE_SHARPE`；而 `group_neutralize` 只掉到 0.432（卡线过）。

机理：`ts_quantile` / `ts_zscore` 的**幅度加权**是 SUB 的来源（权重集中在极端值 ⇒ 天然偏大票）；`group_rank` 把幅度分布整个抹平（等权排），`group_neutralize` 只抹水平项、保留幅度。

⇒ **本节的桶一律接在 `group_neutralize` 上，且保留内层 `ts_quantile` 不变**：
```
rank(group_neutralize(<原信号，含 ts_quantile 幅度层>, bucket(rank(ts_backfill(<FUND 字段>, 66)), range='0.2,1,0.2')))
```

### 10.5 判据（预注册）

1. **S 保持 ≥ 2.0**（对照 `rKRQbPPE` 2.48、`j2YNnKOQ` 2.15）⇒ 桶轴是「正交化」而非「损伤信号」，可继续用它做第 3 条。
2. **桶版与 `rKRQbPPE` 的互相关 < 0.70** ⇒ 目标达成（若能到 < 0.60，则第 3、第 4 条都有希望）。
3. **S 掉到 < 1.6** ⇒ 桶轴吃掉了信号本身 ⇒ 说明估值位移族的信息**集中在桶间（跨行业/跨规模）而非桶内**，那么「同机制降相关」这条路在 GBR 上不成立，必须换机制。
4. **`bucket` 若返回 ERROR 并级联 CANCELLED** ⇒ 记入「本账号不可访问算子」，回退到 `group_cartesian_product` 或直接用 `ts_rank(<FUND 字段>, 252)` 的 5 分位近似（`greater(ts_rank(x, 252), 0.8)` 这类门控）。

---
## 十一、批 17–20：`fundamental17` 换手率 / 量比族（本会话 FUND 塔第二条独立机制线）

### 11.0 本节的意义：塔位判据的最终修正

§9.1 原本推断「现成比率字段可以按语义分到 PV / FUND 两塔」。**批 17 把这个推断彻底推翻**：

`A1Vql6AR`（换手率量比，语义上是纯 PV）实读 `get_alpha_details`：
```
pyramids.list  = [{ name: "GBR/D1/FUNDAMENTAL", multiplier: 1.6 }]
ra.pyramid_short = "fundamental"      pyramids.effective = 1
```

**⇒ 最终判据（本次修正后不再变）：塔位 = 字段所属数据集的 `category`。与字段语义、与我的表达式拼法都无关。**
- `daily_volume_to_shares_outstanding` 属 `fundamental17`（FUNDAMENTAL）⇒ FUND 塔，尽管它语义上是纯价量。
- `cap` 属 PV 数据集 ⇒ PV 塔。
- 对照证据：`divide(X, cap)` 的 `pyramids.list` 里才出现 `GBR/D1/PV`；`divide(X, current_enterprise_value)` 只有 FUND。

**代价说明**：这条误判在会话中期让我误以为「PV 塔有候选了」，实际 PV 塔全程 0 路径。**修完后 PV 塔必须去真正的 `category=pv` 数据集**（见 §12）。

### 11.1 批 17（multisim `32GoGJgt45hdaEOrlekPm6Q`）：形态比变化率强

| alpha | 变体 | 表达式核心 | S | F | TO | 2Y | SUB | dd | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `A1Vql6pe` | 换手率 Δ22 | `rank(ts_quantile(ts_av_diff(bfo,22),66,gaussian))` | 0.44 | 0.14 | 20.06% | −0.08 | 0.01 | 8.47% | 1.89bp |
| **`A1Vql6AR`** | **当日 / 年均量比** | `rank(ts_quantile(divide(bfo, ts_mean(bfo,252)),22,gaussian))` | **1.28** | 0.69 | 19.98% | 1.08 | **+0.22** | **4.71%** | **5.76bp** |

其中 `bfo` = `ts_backfill(daily_volume_to_shares_outstanding, 22)`。

**三条结论**：
1. **形态（水平比值）远优于变化率**：S 1.28 vs 0.44（×2.9）、回撤小 12 倍、SUB 由负转正、margin 高 3 倍。
2. **方向由实测裁决，不靠文献**：批 16 的 `LLMOGrGm`（换手率 Δ66）读数 **−1.18** 是方向符号错，翻符号即 +1.18 —— 证明 GBR 走的是 **Gervais-Odean-Mingelgrin (2001) high-volume return premium（正向）**，不是 Lee-Swaminathan (1999) / Datar-Naik-Radcliffe (1998) 的换手率异象（负向）。
3. **`A1Vql6AR` 实读无 CW 墙**（`CONCENTRATED_WEIGHT` 在 `checks.pass`），持仓 246 + 249 = 495 只（覆盖 71%），`risk_neutralized_sharpe` 1.24、`investability_sharpe` 0.74 —— 结构健康，只是指标不足。

### 11.2 ★★ 互相关突破：`max_mutually_below_subset` 从 2 → **3**

```
compute_mutual_correlation([A1Vql6AR, rKRQbPPE, j2YNnKOQ, P0ojvkkJ,
                            omEQ9kK5, P0ojnOOp, E56oqo1r], threshold=0.7, years=4)
→ max_mutually_below_subset = ["rKRQbPPE", "j2YNnKOQ", "A1Vql6AR"]
  size = 3,  max_subset_exact = true,  num_points = 1021
```

`A1Vql6AR` 与 6 条估值位移族候选的互相关全部落在 **0.068–0.1045**：

| 配对 | 相关 |
|---|---:|
| × `P0ojvkkJ` | 0.0680 |
| × `E56oqo1r` | 0.0707 |
| × `rKRQbPPE` | 0.0739 |
| × `j2YNnKOQ` | 0.0765 |
| × `omEQ9kK5` | 0.0824 |
| × `P0ojnOOp` | 0.1045 |

**这是本会话第一次出现「三条互相 < 0.7」的组合。** 7 对超线全部在估值位移族内部（最高 `rKRQbPPE`×`E56oqo1r` = 0.9617）。

⇒ **FUND 塔凑 3 条的路已经通了**（`{rKRQbPPE, j2YNnKOQ, A1Vql6AR}`），**唯一剩下的是 `A1Vql6AR` 自己过闸**。

⇒ **方法论沉淀**：凑塔数先算 `max_mutually_below_subset`，再决定是否在该族内继续派发。同机制多候选不等于多塔位 —— 估值位移族 6 条里最多只能取 2 条。

### 11.3 批 18（multisim `3Pni683lS4tBcri2slFJDAZ`）：度量层平滑无益

单变量对照，只换量比的平滑尺度（1 日基线 / 5 日 / 22 日）：

| alpha | 度量层 | S | F | TO | 2Y | SUB | SUB/S | dd | margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `A1Vql6AR` | 1 日基线 | **1.28** | 0.69 | 19.98% | 1.08 | 0.22 | 0.172 | **4.71%** | 5.76bp |
| `mLoejm61` | 5 日平滑 | 1.13 | 0.59 | 18.26% | 1.14 | **0.30** | 0.265 | 4.75% | 5.50bp |
| `LLMO7NZv` | 22 日平滑 | 0.94 | 0.54 | 12.35% | **1.60** | 0.18 | 0.191 | 7.67% | 6.62bp |

**裁决：S 随平滑窗口单调下降（1.28 → 1.13 → 0.94）⇒ 度量层平滑对本机制有害，1 日基线最优。**

两个反常细节值得记住：
- `LLMO7NZv` 的 **2Y 1.60 已过 2Y 门槛 1.58，且 2Y/S = 1.70** —— 信号在近两年明显变强。
- `mLoejm61` 把 **SUB/S 从 0.172 拉到 0.265（+54%）** —— 平滑确实改善子宇宙稳健性，但代价是 S 崩。

⇒ 这条「2Y/S > 1.7」在本会话出现了两次（`LLMO7NZv` 1.70、`RRE0VM1d` 1.46）。**同一信号族短期内一致性变强**是真实信号的特征之一，但也意味着**历史早期几乎无收益**，OS 阶段衰减风险要提高警惕。

### 11.4 ★★ 批 19（multisim `1LxIwkbZQ5hE9QFiq471fS5`）：去掉横截面 `rank()` 三重改善

**诊断出处**：记忆铁律 —— `rank()` 把幅度分布整个抹平（等权排），而 `ts_quantile` / `ts_zscore` 的**幅度加权本身就是 SUB 的来源**。`A1Vql6AR` 的表达式是**双重归一化**：`ts_quantile(..., driver=gaussian)` 已经把输出压到 [0,1]，外面又套一层横截面 `rank()`。

| alpha | 外层几何 | S | F | TO | 2Y | SUB | dd | margin | fRA |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `A1Vql6AR` | `rank(ts_quantile(·,22,gaussian))` | **1.28** | 0.69 | 19.98% | 1.08 | 0.22 | **4.71%** | 5.76bp | 4 |
| `xArXYqdg` | `ts_zscore(·,252)` | 1.10 | 0.72 | 14.18% | 1.70 | **0.33** | 9.72% | 8.51bp | 3 |
| **`RRE0VM1d`** | **`ts_quantile(·,252)`** | 1.22 | **0.81** | **13.82%** | **1.78** | 0.29 | 10.34% | **8.83bp** | **3** |

**去掉 `rank()` 换来 5 项改善**：
1. **margin 5.76 → 8.83bp（+53%）** —— 单位换手收益能力大幅提升，这是最本质的改善
2. **2Y 1.08 → 1.78（+65%）** —— **`LOW_2Y_SHARPE` 直接过闸**（唯一被彻底解决的闸）
3. `fitness` 0.69 → 0.81
4. `turnover` 19.98% → 13.82%（−31%）
5. `failed_ra_count` 4 → **3**

**代价**：S 1.28 → 1.22、**drawdown 4.71% → 10.34%（翻倍）**。

**机理**：`rank()` 把权重推向全宇宙等权 ⇒ 收益更分散、波动更低 ⇒ S 虚高；但等权化牺牲了「单位换手收益」（margin）与「近期稳定性」（2Y）。**这是一个真实的权衡，不是调参噪声。**

**`ts_quantile` > `ts_zscore`**（S 1.22 vs 1.10、F 0.81 vs 0.72、2Y 1.78 vs 1.70、margin 8.83 vs 8.51）。注意这不违反「zscore ≫ rank」铁律 —— 这里比的是两个**都保留幅度**的归一化，`rank` 才是被否定的那个。

**⇒ 主骨架从此改为 `ts_quantile(divide(<量>, ts_mean(<量>, 252)), 252)`，不再套 `rank()`。**

### 11.5 ★ SUB 门槛系数修正：**0.4754**，不是 0.434

`RRE0VM1d` 实读 `checks.fail`：

| check | value | limit | limit / S |
|---|---:|---:|---:|
| `LOW_SHARPE` | 1.22 | 1.58 | — |
| `LOW_FITNESS` | 0.81 | 1.0 | — |
| **`LOW_SUB_UNIVERSE_SHARPE`** | **0.29** | **0.58** | **0.4754** |

此前本会话记录的系数是 0.434（USA 实证）。**GBR 这一档实测是 0.4754**，与论坛帖 `31365517513495` 的 0.4743 一致 ⇒ 系数**随区域/宇宙变化**，用之前必须从 `checks.fail` 反算，不能跨区套用。

**⇒ 而 harsher 的推论**：若把 S 堆到 1.58，SUB 门槛会同步升到 **0.75**，当前 0.29 **差 2.6 倍**。**SUB 是本机制的绝对瓶颈，且提高 S 会让它更难 —— 两者是零和关系。**

`RRE0VM1d` 实读其余健康指标：
- 持仓 246 + 250 = **496 / 700 只（覆盖 71%）** ✓
- `LOW_2Y_SHARPE` 在 `checks.pass` ✓
- `CONCENTRATED_WEIGHT` / `CLUSTER_TEST` / `LOW_TURNOVER` / `HIGH_TURNOVER` / `MATCHES_PYRAMID` 全 pass ✓
- `risk_neutralized_sharpe` **1.27 > S 1.22** ⇒ 不是靠风险暴露换收益（好迹象）
- `investability_sharpe` 0.69、`investability_ratio` 0.5656

### 11.6 批 20（multisim `1AZ7HUbNV4lvbbL3QtHEITf`，已派发）：两条独立的救 SUB 处方

SUB 低的两个竞争假设，各给一条表达式（均为表达式内改动，设置与 `RRE0VM1d` 逐位相同 ⇒ 干净对照）：

| # | 假设 | 表达式 | 判据 |
|---|---|---|---|
| A | **信号是规模的代理** ⇒ 回归掉规模后大票信号显形 | `vector_neut(ts_quantile(divide(bfo, ts_mean(bfo,252)), 252), rank(ts_backfill(market_capitalization_value_5, 22)))` | SUB 上升且 S 不掉过 1.1 ⇒ 假设成立 |
| B | **252 日基线被极端年份污染** ⇒ 归一化窗口拉长更稳健 | `ts_quantile(divide(bfo, ts_mean(bfo,252)), 504)` | SUB 与 S 同升 ⇒ 纯稳健性改善 |

`vector_neut` 是放行的「回归残差化」形态；第二参 `rank(...)` 保证无量纲（记忆铁律：股数/金额类必须先 `rank()`，否则报 `Incompatible unit`）。市值字段选 `market_capitalization_value_5`（同属 `fundamental17` ⇒ 保持 FUND 单塔）。

**为什么不用 `winsorize` 救 SUB**：`ts_quantile` 输出是 [0,1] **均匀分布**（std ≈ 0.289、均值 0.5），`winsorize(std=2)` 的截尾边界恰好覆盖全量程 ⇒ **对均匀分布完全无效**。这是批 19 之后才看清的陷阱：`winsorize` 只对接近高斯的输出（如 `ts_zscore`）有效。

### 11.7 预注册判据（批 20）

1. **A 的 SUB 提升 ≥ 50%（→ ≥ 0.44）** ⇒ 规模代理假设成立 ⇒ 可全面推广到估值位移族 6 条（它们也全部只差 SUB）。
2. **A 的 S 掉到 < 1.0** ⇒ `vector_neut` 把真实信号一起回归掉了 ⇒ 规模代理假设不成立，改走「大票专属信号」路线。
3. **B 的 S 与 SUB 同时上升** ⇒ 252 日基线的极端年份污染是 SUB 低的真因 ⇒ 全族归一化窗口统一改 504。
4. **两条都没改善** ⇒ 量比族的 SUB 上限就是 0.3 附近 ⇒ 该族停在「机制独立但不可提交」的位置，FUND 第 3 条腿必须换到 `fundamental90`（CHS 违约概率 / Piotroski F / NOA）。

---
### 11.8 ★★ 批 20（multisim `1AZ7HUbNV4lvbbL3QtHEITf`）：窗口 504 是 SUB 正解，两个杠杆可叠加

| alpha | 变体 | S | F | TO | 2Y | SUB | SUB/S | dd | margin | fRA |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `RRE0VM1d` | 基线 `ts_quantile(·,252)` | 1.22 | 0.81 | 13.82% | 1.78 | 0.29 | 0.238 | 10.34% | 8.83bp | 3 |
| `MPY91xEa` | A：`vector_neut` 规模残差化 | 1.30 | 0.84 | 13.87% | **2.18** | **0.43** | 0.331 | 10.98% | 8.35bp | 3 |
| **`bl67R9mK`** | **B：`ts_quantile(·,504)`** | **1.39** | **1.01** | **13.51%** | **2.20** | **0.48** | **0.345** | 10.53% | **10.61bp** | **2** |

**B 全面胜出，且一次解决了两项闸**：

| 指标 | 基线 | B | 变化 |
|---|---:|---:|---:|
| `LOW_SHARPE` 1.58 | 1.22 | 1.39 | +14%（仍差 12%） |
| **`LOW_FITNESS` 1.0** | 0.81 | **1.01** | **+25% ⇒ 过闸 ✓** |
| **`LOW_2Y_SHARPE` 1.58** | 1.78 | **2.20** | **+24% ⇒ 已过闸** |
| `LOW_SUB_UNIVERSE_SHARPE` | 0.29 | **0.48** | **+66%（仍差 27%）** |
| margin | 8.83bp | **10.61bp** | +20% |
| `failed_ra_count` | 3 | **2** | −1 |

**⇒ 诊断确认：252 日分位基线被**极端年份**污染。量比的分布是重尾的（个别年份出现成交量 regime change 后，整个 252 日窗口被系统性抬高/压低）⇒ 把归一化窗口拉到 504 日（2 年），分位数更稳健，信号纯度提升。**

**`bl67R9mK` 实读（`get_alpha_details`）**：
```
pyramids.list = [{ name: "GBR/D1/FUNDAMENTAL", multiplier: 1.6 }]   ← FUND 单塔
metrics: longCount 248 + shortCount 248 = 496 / 700（覆盖 71%）
         risk_neutralized_sharpe 1.37、investability_sharpe 0.88（基线 0.69）
checks.pass: LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT
             / CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID
checks.fail: LOW_SHARPE 1.39/1.58 ; LOW_SUB_UNIVERSE_SHARPE 0.48/0.66
```
`0.66 / 1.39 = 0.4748` ⇒ **第三次反算出 SUB 系数 0.4754，实证确认**。

**为什么两个杠杆可以叠加**：A 走「回归掉规模代理」，B 走「归一化窗口稳健化」—— 前者改**信号的信息来源**，后者改**基线的估计精度**，机制正交。批 21 已派发合体版。

**A 的副作用（需警惕）**：`investability_ratio` 从基线 0.5656 掉到 **0.4846**（B 是 0.6331）。`vector_neut` 回归掉规模后，持仓向小票偏移 ⇒ 若最终要交，A 路线在可投资性上更差。**A+B 合体若把 investability 也压下去，就是一个不值得的叠加。**

### 11.9 ★★ FUND 三塔组合最终确定：`bl67R9mK` 比 `A1Vql6AR` 更正交

```
compute_mutual_correlation([bl67R9mK, MPY91xEa, RRE0VM1d,
                            rKRQbPPE, j2YNnKOQ, P0ojvkkJ,
                            omEQ9kK5, P0ojnOOp, E56oqo1r], threshold=0.7, years=4)
→ max_mutually_below_subset = ["rKRQbPPE", "bl67R9mK", "j2YNnKOQ"]
  size = 3,  max_subset_exact = true,  num_points = 1021
```

`bl67R9mK` 与 6 条估值位移族候选的互相关：

| 配对 | `bl67R9mK` | `A1Vql6AR`（旧第三腿） |
|---|---:|---:|
| × `j2YNnKOQ` | **−0.0343** | 0.0765 |
| × `omEQ9kK5` | **−0.0550** | 0.0824 |
| × `P0ojvkkJ` | **−0.0165** | 0.0680 |
| × `rKRQbPPE` | **0.0358** | 0.0739 |
| × `E56oqo1r` | 0.0529 | 0.0707 |
| × `P0ojnOOp` | 0.0835 | 0.1045 |

**⇒ `bl67R9mK` 不仅指标优于 `A1Vql6AR`（S 1.39 vs 1.28、F 1.01 vs 0.69、fRA 2 vs 4），正交性也更好（含 3 个负相关）。第三腿正式换成 `bl67R9mK`。**

**量比族内部不能取多条**（同一机制的不同变体必然共线）：

| 配对 | 相关 | 判定 |
|---|---:|---|
| `bl67R9mK` × `RRE0VM1d` | 0.9426 | 只能取一条 |
| `MPY91xEa` × `RRE0VM1d` | 0.8447 | 只能取一条 |
| `bl67R9mK` × `MPY91xEa` | 0.7688 | 只能取一条 |

⇒ **量比族（含所有窗口 / 残差化变体）对整个候选池的贡献上限 = 1 条。** 这既是坏消息（一个族只能点 1/3 个塔位）也是好消息（它与估值位移族近乎完全正交，是理想的第三腿）。

### 11.10 当前候选池状态（会话累计 9 条有量级的候选）

| alpha | 机制 | S | F | 2Y | SUB | fRA | 塔位 | 状态 |
|---|---|---:|---:|---:|---:|---|---|---|
| `rKRQbPPE` | EBITDA/EV 252/22 | **2.48** | 2.22 | 2.69 | 1.68 | **0** | FUND | **全闸通过** |
| `E56oqo1r` | EBITDA/cap 252/22 | 2.39 | 2.11 | 2.50 | 1.64 | **0** | PV+FUND | **全闸通过** |
| `P0ojnOOp` | 总资产/cap 252/22 | 2.30 | 1.96 | 2.42 | 1.59 | **0** | PV+FUND | **全闸通过** |
| `j2YNnKOQ` | EBIT/EV 504/22 | 2.15 | 1.80 | 2.09 | 1.41 | **0** | FUND | **全闸通过** |
| `P0ojvkkJ` | 总负债/EV 66/22 | 1.93 | 1.49 | 1.76 | 1.52 | **0** | FUND | **全闸通过** |
| `omEQ9kK5` | EBIT/cap 66/22 | 1.59 | 1.15 | 2.12 | 1.02 | **0** | PV+FUND | **全闸通过** |
| **`bl67R9mK`** | **量比 / 504 分位** | **1.39** | **1.01** | **2.20** | **0.48** | **2** | FUND | 差 S、SUB |
| `MPY91xEa` | 量比 / 504 + 规模残差化 | 1.30 | 0.84 | 2.18 | 0.43 | 3 | FUND | 差 S、F、SUB |
| `RRE0VM1d` | 量比 / 252 分位 | 1.22 | 0.81 | 1.78 | 0.29 | 3 | FUND | 差 S、F、SUB |

**FUND 塔三条已定：`{rKRQbPPE, bl67R9mK, j2YNnKOQ}`** —— 前两条已全闸、第三条差 2 项。
**PV+FUND 双塔 3 条已满配额：`{E56oqo1r, P0ojnOOp, omEQ9kK5}`** —— 但这三条互相超线（0.82 / 0.79 / 0.71），实际只能取 1 条进组合。
**PV 塔仍为 0（需 2）**，见 `template_library_gbr_pv20_beta_term_structure.md`。
**OTHER 塔仍为 1（需 2）**，`other567` / `other169` 两条路径已排除。

---
## 11.11 批 23：中性化档位扫描 —— `STATISTICAL` 是**负向**杠杆（已排除）

**设计**：`{504 基线, A+B 叠加} × {INDUSTRY, STATISTICAL}` 完整 2×2 因子设计，其余设置全同（`decay 10 / trunc 0.05 / nanHandling OFF / maxTrade OFF / unitHandling VERIFY`）。

| 几何 | INDUSTRY | STATISTICAL | 差异 |
|---|---|---|---|
| 504 基线（`ts_quantile` 无残差化） | `bl67R9mK` S 1.39 / F 1.01 / TO 13.51% / 2Y 2.20 / SUB 0.48 / fRA 2 | `wpQXZxX5` S 1.44 / **F 0.80** / TO 15.49% / 2Y 2.01 / SUB 0.48 / **fRA 3** | S +0.05 / **F −0.21** / 2Y −0.19 / SUB 0 / fRA +1 |
| A+B 叠加（`ts_quantile` + 规模残差化） | `vR1akGVz` S 1.54 / F 1.10 / TO 13.56% / 2Y 2.56 / SUB 0.62 / fRA 2 | `xArX38XW` S 1.52 / **F 0.87** / TO 15.54% / 2Y 2.23 / SUB 0.60 / **fRA 3** | S −0.02 / **F −0.23** / 2Y −0.33 / SUB −0.02 / fRA +1 |

**结论（四条，全部为负）**：
1. **SUB 完全不改善**（0.48→0.48、0.62→0.60）⇒ 中性化轴**不是 SUB 的杠杆**，与「SUB/S 是信号几何属性、不是设置属性」的既有结论一致（本会话 `group_rank` 家族实证 SUB/S 在 decay 5→15 全程 0.29–0.30 不动）。
2. **F 被系统性拖累 0.21–0.23**，两条都跌破 1.0 门槛（1.01→0.80、1.10→0.87）⇒ STATISTICAL 会**制造新的闸失败**。
3. **2Y 同步下降** 0.19–0.33 ⇒ 2Y 闸的安全垫被削薄。
4. **fRA 2→3**（两条一致）⇒ 多出一个失败项。

**⇒ 中性化档位这一杠杆已彻底耗尽。** INDUSTRY 保留为族级设置。剩余设置维度只有 `decay` 与 `truncation`，但按第 1 条结论，两者都不是 SUB/S 的杠杆。

**方法学收获（可复用）**：判断「某设置杠杆是否值得扫」的先验判据 —— 若该设置作用于**持仓权重层**（decay / truncation / neutralization 都属此类），它能改 TO 与 invest_ratio，但**改不动 SUB/S**；真正能改 SUB/S 的只有**表达式层的横截面操作数量**。这条把「设置扫描」与「几何改造」明确分工，避免在设置维度上浪费仿真槽。

---
## 11.12 批 24：`ts_zscore` 替代 `ts_quantile` —— **SUB/S 比值 +11%（0.403 → 0.449）**，这是本轮最大的单点改进

**动机**：批 17–21 把外层度量一直固定为 `ts_quantile`，从未在同一窗口下横向对比 `ts_zscore`。而批 19 的 `xArXYqdg`（`ts_zscore` 252 日，比率 0.300）显著高于同窗口的 `RRE0VM1d`（`ts_quantile` 252 日，比率 0.238）——这个信号在单变量层面早已给出，只是被 504 窗口的更大改进掩盖了。批 24 把窗口固定在 504，做 `{ts_quantile, ts_zscore} × {无残差化, 残差化}` 的完整消融。

**结果（其余设置全同：`INDUSTRY / decay 10 / trunc 0.05`）**：

| 外层度量 | 无残差化 | 加规模残差化 |
|---|---|---|
| `ts_quantile` | `bl67R9mK` S 1.39 / F 1.01 / 2Y 2.20 / SUB 0.48 / **比值 0.345** / dd 10.53% | `vR1akGVz` S **1.54** / F **1.10** / 2Y **2.56** / SUB 0.62 / **比值 0.403** / dd 11.35% |
| `ts_zscore` | `mLoemqrK` S 1.31 / F 0.96 / 2Y 2.16 / SUB **0.54** / **比值 0.412** / dd 12.07% | `QPvmbn2w` S 1.38 / F 0.99 / 2Y 2.41 / SUB 0.62 / **比值 0.449** / dd 16.78% |

**四条结论**：

1. **`ts_zscore` 在两个格子里的 SUB/S 比值都更高**：无残差化 0.345→**0.412**（+19%）、有残差化 0.403→**0.449**（+11%）。
   **机理**：`ts_zscore` 输出近似高斯、保留**幅度**信息（极端换手率获得极端分数）；`ts_quantile` 输出**均匀分布**（std≈0.289），把幅度压平为等距秩位 ⇒ 同一窗口下 zscore 的信号更集中于极端事件，而极端事件更可能发生在大票的财报/指数调整日。
   **这与批 19「去 `rank()`」是同一条第一性原理**：所有把分布压平的变换（`rank` / `ts_quantile`）都会稀释 SUB；保留幅度的变换（`ts_zscore`）则会提升 SUB。

2. **残差化在两种度量下都提升 SUB**（0.48→0.62、0.54→0.62），幅值一致（+0.14 / +0.08）⇒ **残差化是稳健的正向杠杆**，与度量选择正交。

3. **但 `ts_zscore` 的绝对 S 更低**（1.38 vs 1.54）、**回撤更大**（16.78% vs 11.35%）⇒ 这是「比值换绝对强度」的交易。
   ★ **注意：这条交易在 GBR 是划算的** —— 因为 `S ≥ 1.58` 与 `SUB ≥ 0.4754×S` 必须同时成立，而 SUB 是硬卡点。S 高但比值低 = 永远过不去；S 略低但比值高 = 还有拉升空间。

4. **两种几何的 SUB 都精确卡在 0.62**（`vR1akGVz` 与 `QPvmbn2w`）⇒ SUB 的绝对水平由「信号在小票上的暴露」决定，不由外层度量决定。**要突破 0.751，必须动持仓集合本身，而非度量层。**

**⇒ 下一杠杆锁定在「市值门控」**：`trade_when(greater(rank(mcap), 0.5), <信号>, -1)` —— 直接对齐持仓集合与大票子宇宙。这是 `trade_when` 的合规用法（放行形态），不是权重混合。

**方法学收获**：`ts_quantile` vs `ts_zscore` 的取舍规则可以固化为 —— **卡 SUB 时选 `ts_zscore`（保幅度），卡绝对 S 时选 `ts_quantile`（压尾部极端值、降低波动）**。两者是同一分布变换的两端，不是「哪个更好」。

---
## 11.13 批 25：市值门控**彻底失败**，且失败方式证伪了「SUB 低 = 收益集中在小票」这个前提

**设计思路**：批 21 后 SUB 精确卡在 0.62（两种度量一致）⇒ 推断「SUB 低是因为收益集中在小票」。于是用 `trade_when` 把交易集合限制到市值前 50%（TOP700 的 top 350），预期持仓与大票子宇宙对齐、SUB 逼近 S。`trade_when` 属放行形态，`greater(rank(mcap), 0.5)` 无量纲合规。

| 门控版（`greater(rank(mcap),0.5)`） | 原版（无门控） | 结果 |
|---|---|---|
| `78Lg6AxQ`（quantile + 残差化 + 门控） S **0.49** / F 0.23 / SUB **0.21** / 2Y 1.36 / fRA 4 | `vR1akGVz` S 1.54 / F 1.10 / SUB 0.62 / 2Y 2.56 / fRA 2 | S −68%、SUB **−66%** |
| `LLMOZjn1`（zscore + 残差化 + 门控） S **0.36** / F 0.15 / SUB **0.20** / 2Y 1.02 / fRA 3 | `QPvmbn2w` S 1.38 / F 0.99 / SUB 0.62 / 2Y 2.41 / fRA 3 | S −74%、SUB **−68%** |

**三条结论**：
1. **门控同时摧毁 S 和 SUB**（不是「S 降换 SUB 升」的权衡，是双向都降）⇒ 该方向无任何可取之处。
2. **★ 前提被证伪**：若「SUB 低 = 收益集中在小票」，砍掉小票后 SUB 应当上升。实测 SUB 从 0.62 崩到 0.21 ⇒ **子宇宙本身包含大量小票，砍小票等于砍掉子宇宙的收益来源**。这是本会话第二次「用实测推翻自己的机理推断」（第一次是塔位判据）。
3. **换手率溢价在 GBR/TOP700 的收益来源分布在整个市值谱上，且小票侧贡献更大**。这与 high-volume return premium 的文献一致（Gervais-Odean-Mingelgrin 2001 的原始样本以中小盘为主），也解释了为什么 `fundamental17` 换手率族无论怎么改造都过不去 SUB。

**⇒ 该族的结构上限已确认**：S 1.54（差 2.5%）+ 比值 0.403（差 18%）。**在「比值为硬墙」的前提下，该族不可能过闸。全部仿真槽撤出。**

## 11.14 互相关终局：6 条全闸候选里**实际只能共存 2 条**

```
compute_mutual_correlation([rKRQbPPE, E56oqo1r, P0ojnOOp, j2YNnKOQ, P0ojvkkJ, omEQ9kK5],
                           threshold=0.7, years=4)
→ max_mutually_below_subset = ["rKRQbPPE", "j2YNnKOQ"]
  size = 2,  max_subset_exact = true,  num_points = 1021
```

| 超线对（7 对） | 相关系数 |
|---|---:|
| `rKRQbPPE` × `E56oqo1r` | **0.9617** |
| `E56oqo1r` × `P0ojnOOp` | 0.8201 |
| `P0ojnOOp` × `P0ojvkkJ` | 0.8148 |
| `rKRQbPPE` × `P0ojnOOp` | 0.7934 |
| `E56oqo1r` × `P0ojvkkJ` | 0.7151 |
| `j2YNnKOQ` × `omEQ9kK5` | 0.7089 |
| `rKRQbPPE` × `P0ojvkkJ` | 0.7014 |

**⇒ 6 条全闸候选在组合层面等价于 2 条 alpha。估值位移族是一个不可拆的相关块。**

**战略含义（必须写死，避免后人重复误判）**：
1. **候选数 ≠ 进度**。本会话曾把「6 条 fRA=0」当作进度，实际有效产出是 2 条。**汇报与规划一律用 `max_mutually_below_subset_size`，不用候选条数。**
2. **该族不能再投仿真槽** —— 第 3 条无论如何都会与已选两条之一超线。`P0ojvkkJ`（S 1.93）虽全闸通过但与 `rKRQbPPE` 0.7014 贴线，只能作为 `rKRQbPPE` 的**替补**，不能与它共存。
3. **正交性的稀缺是全 GBR 战役的真瓶颈**：本会话 25 个批次里，真正正交的机制只有 2 个（估值位移 / 换手率），第 3 个正交源在 `pv20` 流动性口径（`RRE06nEz`，对前两族 0.07–0.54）—— **这是唯一还在扩篮子的一支**，详见 `template_library_gbr_pv20_beta_term_structure.md` §10.2–10.3。

---
---

## §12 `QPvmbn2w` 族封盘（6 条 sim 全证据）+ 横截面操作**类型**修正

### 12.1 设置矩阵：`INDUSTRY` 是该族最优中性化轴（与 `continuation_score` 族相反）

主体表达式（`vector_neut` 版本，`QPvmbn2w` 原式）：

```
vector_neut(ts_zscore(divide(ts_backfill(daily_volume_to_shares_outstanding, 22),
        ts_mean(ts_backfill(daily_volume_to_shares_outstanding, 22), 252)), 504),
        rank(ts_backfill(market_capitalization_value_5, 22)))
```

| alpha | decay | 中性化 | S | F | TO | 2Y | SUB | SUB/S | dd | margin | fRA |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`QPvmbn2w`** | **10** | **INDUSTRY** | **1.38** | **0.99** | 14.16% | **2.41** | **0.62** | **0.449** | 16.78% | 10.21bp | 3 |
| `xArXVGrg` | 6 | SUBINDUSTRY | 1.39 | 0.93 | 16.72% | 2.14 | 0.59 | 0.424 | 18.74% | 8.94bp | 3 |
| `leAJEMZ2` | 10 | SUBINDUSTRY | 1.22 | 0.81 | 14.61% | 2.08 | 0.52 | 0.426 | 18.79% | 8.75bp | 3 |
| `88RgVv5z` | 10 | SECTOR | 1.23 | 0.88 | 13.52% | 1.81 | 0.52 | 0.423 | 20.73% | 10.27bp | 3 |
| `mLoed7d2` | 16 | SUBINDUSTRY | 1.04 | 0.68 | 12.06% | 2.11 | 0.38 | 0.365 | 17.46% | 8.76bp | 3 |
| `mLoemqrK` | 10 | INDUSTRY | 1.31 | 0.96 | 14.13% | 2.16 | 0.54 | 0.412 | 12.07% | 10.71bp | 3 |
| `N1NkJAwp` | 10 | SUBINDUSTRY | 1.22 | 0.83 | 14.57% | 1.92 | 0.48 | 0.393 | 14.67% | 9.36bp | 3 |

**★ decay 10 的 2×2 因子设计**（中性化轴 × 表达式层横截面层，其余全同）：

| | `vector_neut` 残差化 | 无横截面层 | 中性化主效应 |
|---|---:|---:|---:|
| **INDUSTRY** | **0.449** (`QPvmbn2w`) | 0.412 (`mLoemqrK`) | **+0.037** |
| **SUBINDUSTRY** | 0.426 (`leAJEMZ2`) | 0.393 (`N1NkJAwp`) | +0.033 |
| **横截面层主效应** | **+0.023** | +0.019 | — |

两个主效应**方向一致且可加**（无交互项），说明 `INDUSTRY` 与 `vector_neut` 各自独立地贡献约 +0.02–0.04 SUB/S，不互相替代。**但两者之和的极限也只有 0.449，距闸线 0.471 差 0.022 —— 这两个杠杆的可用总幅度（0.06）与缺口（0.022）同量级，说明该族已被榨干。**

**三条结论**：
1. **`INDUSTRY` 全面最优**（S / F / 2Y / SUB 四项同时最高），`SUBINDUSTRY` 与 `SECTOR` 全部更差，`decay 16` 崩到 0.68 F。**这与 `continuation_score` 族「SUBINDUSTRY 全面优于 INDUSTRY」恰好相反** ⇒ **中性化轴的最优选择是族属性，不能跨族照搬。**
2. **`decay` 从 6 升到 16 时 SUB/S 单调恶化**（0.424 → 0.426 → 0.365），与 `continuation_score` 族的单调关系同形，但方向性收益完全不同。
3. 全部 6 个变体的 **SUB/S 落在 0.365–0.449，闸线约 0.471**，最高点仍差 **4.7%**；且 S 最高也只到 1.39（需 1.58，差 13.7%）。**两条墙同时封死，设置层已无杠杆。**

### 12.2 ★ 横截面操作**类型**比**数量**更决定 SUB/S（推翻此前的粗规则）

同一主体、同一设置（decay 10 / INDUSTRY / trunc 0.05），唯一差异是表达式层的横截面层：

| 版本 | 表达式层横截面 | S | F | 2Y | SUB | SUB/S | `risk_neutralized_sharpe` |
|---|---|---:|---:|---:|---:|---:|---:|
| `QPvmbn2w` | `vector_neut(...)` **残差化** | **1.38** | **0.99** | **2.41** | **0.62** | **0.449** | **1.32** |
| `mLoemqrK` | **无**（剥掉 `vector_neut`） | 1.31 | 0.96 | 2.16 | 0.54 | **0.412** | 1.26 |

**剥掉横截面层，SUB/S 反而掉 8%** —— 此前从 `insider_trx_matrix` 总结的「破 SUB 墙要**减**横截面操作」在**本族上方向相反**。

修正后的判据是「抹的是**水平**还是**幅度分布**」：

| 横截面算子 | 几何作用 | 对 SUB/S | 实测证据 |
|---|---|---|---|
| `group_rank` | 换成等权排名，抹掉整个幅度分布 | **↓↓↓ 重创** | 0.44 → 0.29（`insider_trx_matrix`） |
| `group_neutralize` | 行业内去均值，只抹水平项、留幅度 | ↓ 轻微 | 0.432（卡线过） |
| `vector_neut` | 对正交腿回归残差化，去共线但留幅度 | **↑ 改善** | 0.412 → 0.449（本族） |
| 无 | — | 基准 | 0.412 |

**机理**：`ts_zscore` 的幅度加权把权重压到极端值（偏事件驱动、偏小票），这对 SUB 有利；`group_rank` 把这个幅度信息整段抹平，权重摊到全宇宙 ⇒ SUB 侧被稀释；`vector_neut` 只剥掉与规模共线的那部分（该部分在大票上更结构化），剩下的异质幅度反而更集中在小票上。

**落地纪律**：
- 卡 `LOW_SUB_UNIVERSE_SHARPE` 时**先拆 `group_rank`**（收益最大），但**不要顺手拆 `vector_neut`**，必须各测一次再决定。
- 若业务上必须保留 `group_rank`（要 invest_ratio 或压换手），配套 `tail(winsorize(..., std=2), lower=0.2, upper=0.8, newval=0.5)` 截尾，才能把 SUB/S 拉回 0.44 附近。
- `vector_neut` 属于「可加」的层，不属于「要减」的层。

### 12.3 该族的真实价值与封盘判据

`risk_neutralized_sharpe` = **1.32**（对比 `MPY96E7o` 仅 0.33）是本会话质量最高的信号内核，`mLoemqrK` 保留该值 1.26 ⇒ 内核确实强，**瓶颈在幅度标定而非信号本身**。但 6 条 sim 已证明：

$$\text{SUB/S}^{\max} = 0.449 < 0.471\ (\text{闸}) \quad\wedge\quad S^{\max} = 1.39 < 1.58\ (\text{闸})$$

**⇒ 封盘，不再为 `daily_volume_to_shares_outstanding` 投仿真槽。** 保留 `QPvmbn2w` 作为「内核强、几何不达标」的教科书负例，以及「`vector_neut` 提 SUB/S」的唯一对照证据。

---

## §13 `fundamental93` 先验纠正（实测字段实读）

**纠正**：此前记录该数据集为「Earnings Tax Data → 现金有效税率 cash ETR 异象（Dyreng-Graham-Long 2008）」。**实读 17 个字段后确认：数据集内没有任何 cash ETR / 税率字段**，R/E/A 会计口径族（revenue / invested_capital / equity）也**全部缺失**，因此这两条机制在本数据集上**不可实现**。

实际字段构成（`get_datafields(region="GBR", dataset_id="fundamental93", filter_sharpe=False)`，`platform_count=17`，全部 MATRIX，**coverage 全部 0.0**）：

| 组 | 字段 | 拥挤度 | 可用机制 |
|---|---|---|---|
| **资产增长** | `fnd93_accrualsratio_d1_asset_change`（"Asset change ratio = latest total assets divided by asset_ltm"） | u2/a3 | **Cooper-Gulen-Schill 2008 资产增长异象本体** |
| 资产增长（别名） | `fnd93_expense_d1_asset_change` / `fnd93_liability_d1_asset_change` | u0/a0 / u0/a0 | 同上，三个别名指向同一构造 |
| **递延税费用比率** | `fnd93_deferred_tax_expense_{11,12,21,22,31,41,51}`（7 个分母变体，"(Net deferred tax liability − Net deferred tax expense)/分母"） | u0–u3 / a0–a3 | 税务激进性 / 会计质量代理 |
| 递延税费用统计量 | `fnd93_expense_d1_mean` / `_dts`（LTM 标准差）/ `_max` / `_min` / `_length` | u0–u1 / a0–a2 | 均值=水平；`_dts`=**二阶矩（不确定性）** |
| 噪声成分 | `fnd93_accruals_d1_length`（仅"可用观测数"） | u0/a0 | ❌ 不是应计值本体，不可用 |

**动作**：`fundamental93` 的 coverage 全 0（与全平台同性质 bug），但拥挤度极低（u≤3/a≤3）值得一次探针；**不把它当主力骨架**，因为只有一个真实概念（资产增长）且存在三个别名。

---

## §14 资产增长异象模板池（12 个，结构互异，标注来源）

**字段基座**：`fundamental6` 的 `fnd6_cptnewq_atq`（"Assets - Total"，**coverage 0.7107**，u255/a653）—— 这是本区**已验证有真实覆盖**的总资产字段，比 `fundamental93` 的 0.0 可靠。资产增长一律写成比值（同单位相除 ⇒ 无量纲）：`divide(A, ts_delay(A, 252))`。

| # | 模板 | 表达式骨架 | 机制（矩 / 几何 / 分组轴） | 来源 |
|---|---|---|---|---|
| T1 | 经典 1 年资产增长 | `reverse(rank(divide(ts_backfill(A,66), ts_delay(ts_backfill(A,66),252))))` | 横截面秩 × 投资过度（水平） | paper: Cooper-Gulen-Schill 2008 |
| T2 | 3 年累计资产增长 | `reverse(rank(divide(ts_backfill(A,66), ts_delay(ts_backfill(A,66),1008))))` | 长期窗口族（1008） | paper: 同上（长期版） |
| T3 | 资产增长**加速度** | `reverse(rank(ts_delta(divide(ts_backfill(A,66), ts_delay(ts_backfill(A,66),252)), 252)))` | **二阶差分**（投资增速变化） | 自建 |
| T4 | 资产增长**时序新颖度** | `ts_quantile(divide(ts_backfill(A,66), ts_delay(ts_backfill(A,66),252)), 504)` | 自身历史分位（不反转，探符号） | 自建 |
| T5 | 资产增长**波动率** | `reverse(rank(ts_std_dev(divide(ts_backfill(A,66), ts_delay(ts_backfill(A,66),252)), 504)))` | **二阶矩**（投资不确定性） | 自建 |
| T6 | 净经营资产占比（NOA 近似） | `reverse(rank(divide(ts_backfill(fnd6_newq_ancq,66), ts_backfill(fnd6_cptnewq_atq,66))))` | 分母重构（非流动资产/总资产） | paper: Hirshleifer-Hou-Teoh-Zhang 2012 |
| T7 | 无形资产强度 | `reverse(rank(divide(ts_backfill(fnd6_ewq_intanq,66), ts_backfill(fnd6_cptnewq_atq,66))))` | 分母重构（无形资产/总资产） | paper: Fairfield-Penman-Yeh 2003 |
| T8 | 流动资产占比 | `reverse(rank(divide(ts_backfill(fnd6_cptnewq_actq,66), ts_backfill(fnd6_cptnewq_atq,66))))` | 分母重构（流动资产/总资产） | forum: 43554304235543（A 族分母重构链） |
| T9 | 折旧强度 | `rank(divide(ts_backfill(fnd6_dfxay,66), ts_backfill(fnd6_cptnewq_atq,66)))` | 现金消耗 / 资本密集度 | paper: 资本密集度族 |
| T10 | 营运资本变动 | `reverse(rank(ts_backfill(fnd6_wcapopc,66)))` | 应计 / 营运资本渠道（差分型） | paper: 应计异象族 |
| T11 | 残差化资产增长（去规模共线） | `vector_neut(T1主体, rank(ts_backfill(market_capitalization_value_5,22)))` | 横截面残差化（§12.2 证明此层**提** SUB/S） | 自建（§12.2 衍生） |
| T12 | 桶内资产增长排序 | `group_neutralize(T1主体, bucket(rank(cap), range="0.2,1,0.2"))` | **分组轴**（市值 5 桶，TOP700 档位） | forum: 44174743998999（bucket 降 PC 模板库） |

**使用约束**：
- T12 依赖 `bucket` 算子，**本账号可用性仍未验证**（`group_median`/`group_count` 等幽灵算子会整包 CANCELLED）；落地前必须单条最小验证。
- T1–T5 全部基于同一个字段，**属于同一概念的多几何展开，不是 5 个独立机制**；与 T6–T10（不同分母/不同会计科目）才是真正互异的机制。按模板归因时不要把 T1–T5 当成 5 次独立覆盖。
- 方向全部按「高资产增长 → 低未来回报」编码（`reverse`）；若某模板实测强负，即从另一几何再次确认该方向，不要当场反号调参。
- 与已存在的两条 FUND 全闸 alpha（`rKRQbPPE` 估值位移 EBITDA/EV、`j2YNnKOQ` 估值位移 EBIT/EV）机制正交，但**提交前必须实测互相关**（`compute_mutual_correlation`）—— 估值位移族内部已证是「不可拆的相关块」（§11）。