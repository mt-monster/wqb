---
name: wq-basket-composition
description: "候选篮子的组合与准入判定：ATOM 优先、三段式准入（checks fail=[]/互相关<0.7/分类合规）、破高相关用「换核心而非换搭档」、双窗口搭档叠加、塔归属速查与 trio 禁混、逐年无负年质量判据。触发：组篮子/篮子互相关/入不了篮/高相关堆叠/相关性卡住/同源废件/怎么凑够 N 颗/ATOM 优先/塔归属/trio 冲突/交付集合怎么选。"
last_verified: 2026-11-12
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# 候选篮子组合与准入判定

## 职责边界

- **本 skill 负责**：把已有候选组成**互相关达标的交付篮子**——准入三段式判据、破高相关的结构性手法（换核心）、搭档叠加配方、塔归属与分类合规、逐年质量判据。解决「明明过闸却进不了篮子」「N 颗目标差几颗」这类问题。
- **本 skill 不做**：单条 alpha 的指标优化与算子压缩（→ `wq-alpha-gate-push-op-min`）；选数据集 / 开战役（→ `wq-brain-campaign-matrix`、`wq-brain-ra-<region>`）；提交（→ `worldquant-submit-alpha`，提交权归用户）。
- **上游 / 下游**：上游 = 任何已产出候选的挖掘波次；下游 = self/prod 相关性快筛 → 稳健性 → 用户授权提交。

> 本 skill 的全部量化结论来自 2026-11-12 DEU/D1 insiders 战役（约 30 波 / 400+ 臂），明细见 [`references/deu-insiders-evidence.md`](references/deu-insiders-evidence.md)。

---

## ★ 原则 0（用户指令）：ATOM 优先

**ATOM = 单数据集 + 单塔**。组篮子时先穷尽 ATOM 形态，再考虑跨数据集组合。

理由不是偏好而是算账：

| 维度 | ATOM | 跨数据集组合 |
|---|---|---|
| 分类合规 | 天然只 1 个 trio 成员，**免 trio 冲突** | 每次都要查两组字段的塔归属，易违规 |
| 复杂度折扣 | 数据集数 = 1，**惩罚项最小** | `1/(field_count + dataset_count)` 里 dataset 项被放大 |
| 可解释性 | 单机制，归因干净 | 多机制混合，失效时难定位 |
| 相关性风险 | 只在同数据集内竞争 | 跨类共同因子叠加，**0.7 门槛更难过** |

**判据**：表达式里全部字段来自同一 dataset ⇒ ATOM（`group` 类字段如 `sector`/`industry`/`market` **豁免**，不计入数据集数）。若出现第二个 dataset 的字段，先问「删掉它 S 是否仍过闸」——过就回到 ATOM。

### ★★ ATOM 的平台红利：IS_LADDER 检查直接不出现（官方 + 实测双证）

**平台官方**（论坛 v201《BRAIN 平台上的四类Alpha》原文）：

> ATOM Alpha 判定标准：**所有使用的数据字段必须来自同一个数据集**；
> 常见 group 字段如 `industry`、`country` 等是**豁免字段**，不计入数据集数量限制；
> 特别检测机制：**放松了 IS Ladder Testing 要求，仅要求通过最近两年的 2-Year Sharpe 检测**。

**实测验证（9 颗对照，2026-11-12）**：

| 类型 | alpha | 塔数 | `IS_LADDER_SHARPE` 是否出现在 checks 里 |
|---|---|---:|---|
| **ATOM（单塔）** | 78Yk8VR1 / d5a2vxzY / GrW9OxmG / zq3eb7No / RREPm361 | 1 | **全部没有** |
| 非 ATOM（多塔）| d5apW38x / leadEXnl / WjlMlWJd / npa9PKWw | 2-3 | **全部有** |

⇒ **ATOM 形状的 alpha 根本不会出现 `IS_LADDER_SHARPE` 这一项检查。**

**这是 ATOM 优先最强的理由**——不是偏好，是**少一道闸**：

| | ATOM | 非 ATOM |
|---|---|---|
| IS Ladder | **不检查**（只要 2Y Sharpe）| 检查，且用动态窗口（实测见过 ladderWin=2/3/4）|
| 常见后果 | 好过 | 常见 S 1.58 已达标却卡 ladder（实测 `npa9KaVd` S1.58、2Y1.24、ladderWin=3 FAIL）|

**纪律**：构造时优先问「**能不能只用同一个 dataset 的字段**」。能，就走 ATOM——省掉一整道闸。
只有 ATOM 形态确实过不了闸时，才加第二个 dataset，并预期要额外过 IS_LADDER。


> 实测教训：DEU insiders 战役最终 17 颗里有 7 颗含 INSIDERS 塔，但真正的严格 ATOM 只占少数；
> 跨数据集件虽然 S 更高（可达 2.36），但**每颗都要单独算 trio 合规**，且彼此相关性被核心共同因子拉到 0.78-0.83。


---

## ★ 原则 1（硬铁律）：禁止两条独立信号腿加权相加

**这是与 ATOM 优先同源的纪律，不是两件事。** 你在 2026-09-28 定案：

> 不得把两条**独立信号腿**加权相加——无论写成 `add(multiply(0.4,腿A), multiply(0.6,腿B))`
> 还是等权 `add(group_rank(腿A), group_rank(腿B))`（等权即 0.5A+0.5B，同一违规族）。

### 判定算法（`gate._detect_equal_weight_leg_add`）

```
对每个 add( ：取顶层实参 → 挑出「信号腿」（引用数据字段、非纯常数）
若 ≥2 条腿 且 归一化数字后形态不全相同 ⇒ POISON
```

**放行**（实测）：
| 形态 | 判定 | 原因 |
|---|---|---|
| `add(ts_mean(x,22), ts_mean(x,66))` | ✅ 放行 | **同形态不同窗** = 单信号多窗平滑 |
| `add(ts_mean(x,22), 0.01)` | ✅ 放行 | 1 条腿 + 标量 |
| `divide(x, add(A,B))` 里的 add | ✅ 放行 | **分母位**是归一化分量，不是两腿相加 |
| `add(multiply(a,c), multiply(b,f), c, b)` | ❌ POISON | 多形态腿相加 |

### 先例代价（记住这个数字）

KOR wave189/190 共 7 条 `add(group_rank(腿A), group_rank(腿B))`，
其中最好的一条 **S 2.11 / F 1.80 / 2Y 1.89** —— **全部作废**。

⇒ **平台 checks 全过 ≠ 可交付。** 组合形态是独立于平台闸的第四道判据。

### 与 ATOM 优先的关系（关键）

| | ATOM 优先 | 闸5 铁律 |
|---|---|---|
| 作用 | 少用数据集 / 少占塔 | 不许跨腿相加 |
| 交集 | **坚持 ATOM 就天然很少去 add 两条独立信号腿** | — |

⇒ 这两条纪律指向同一个构造习惯：**单核心 + 同族多窗平滑**，而不是「多机制拼盘」。

### 组篮子时的正确做法

```
✅ 允许：单腿核心 + 同形态不同窗（add(ts_mean(x,22), ts_mean(x,66))）
✅ 允许：单腿 + 标量保护（add(x, 0.0001)）
✅ 允许：比值/归一化（divide(腿, add(分量A,分量B))）—— 分母位豁免
❌ 禁止：add(独立腿A, 独立腿B)  无论加权与否
❌ 禁止：add(组腿1, 组腿2, 组腿3...) 多元多形态堆叠
```

**若已有一批跨腿相加的候选**：它们的平台指标有效，但按此铁律不可交付，
需要**重构成单腿形态**后重测——而不是直接入篮。

---

## 二、准入三段式判据（缺一不可）

一颗候选要进篮子，必须**同时**满足：

```
① 平台闸：get_alpha_details().checks.fail == []
② 组合形态：gate._detect_equal_weight_leg_add(code) == False    ← 见原则 1
③ 分类合规：塔列表里 PV / MODEL / OTHER 最多出现一个
④ 相关性：与篮子内每一颗的 compute_mutual_correlation < 0.7
```

**四条缺一不可。** 实测代价：
- 漏 ② ⇒ DEU 17 颗里有 **13 颗**被判 POISON，只有 4 颗干净（详见证据文件 §八）
- 漏 ③ ⇒ 4 颗 S≥1.59 的强件因 trio 冲突作废（S 2.63 / 2.37 / 1.87 / 1.59）

**自查命令**（零成本，派发前/入篮前都跑）：
```bash
python -c "
import sys, json; sys.path.insert(0,'Claude/skills/wq-brain-campaign-toolkit/scripts')
import gate
items = json.load(open('codes.json', encoding='utf-8'))   # [{id, code}]
for it in items:
    r = gate._detect_equal_weight_leg_add(it['code'], set())
    print(it['id'], 'POISON' if r else 'OK')
"
```

### ⚠ 三个高频误判点

| 误判 | 正确做法 |
|---|---|
| 用 `batch_get_alpha_metrics` 的 `failed_ra_count` 当闸判据 | 该字段可能是**缓存旧值**。以 `get_alpha_details().checks.fail` 为准 |
| 用 2Y 指标推断 `IS_LADDER_SHARPE` 是否过 | ladder 用**动态窗口**（2 年或 3/4 年），必须实读 checks；实测 2Y 1.24 而 ladderWin=3 判 FAIL |
| 只看 S 就判「可交付」 | 还要看 `sub_universe_sharpe`、`CONCENTRATED_WEIGHT`、以及逐年是否有负年 |

---

## 三、破「高相关堆叠」：换核心，不是换搭档

### 症状

固定一个复合核心（多腿叠加）× 换 8 个不同搭档族，做出的件互相关全部 **0.78-0.83**，5 次独立验证全部超 0.7 ⇒ 只能算 1 颗。

### 根因

复合核心把底层信息榨干后成为**主导共同因子**，搭档只贡献 30-40% 的 PnL 方差，拉不开距离。

### 破法

```
把核心从「多腿叠加」降为「单腿」 或 换一条腿作核心
```

| 做法 | 互相关 | 结果 |
|---|---|---|
| 固定四腿核心 × 换 8 个搭档族 | **0.78-0.83** | 全部废，只算 1 颗 |
| **换核心为单腿 × 单搭档** | **0.35-0.58** | 可入篮，DEU 从 14 颗推到 17 颗 |

**纪律**：入篮失败时先问「**是不是所有件共享同一个复合核心**」——是就拆核心，不是换搭档。

### 但注意：核心的「定义」不能改

同一个核心改窗口 / 改数学形态，会退化成弱信号，不能用来造低相关变体：

| 核心变体 | S（基准 1.74-2.20）|
|---|---|
| 窗口 22 | 1.56 |
| 窗口 132 | 1.18 |
| 换 sum | 1.63 |
| 换 std_dev | 1.15 |

⇒ **换核心 = 换「哪条腿」，不是换「同一条腿的窗口/形态」。**

---

### ★★★ 关键前提：以上「稀释」只在**朴素等权 add** 下成立

**这是本 skill 最容易被误读的一条，必须写清前提。**

`add(腿A, 腿B)` 若 A、B 同源且高相关（截面 rank 后相关 >0.8），等权相加 = 把同一信号重复 N 次再除以 N
⇒ 只降方差、不增信息 ⇒ 实测 S 单调递减（DEU insiders1：2 腿 1.30 → 7 腿 1.03）。

**但这不是「同数据集不能叠加」的证明，是我当时没用正交化算子。**

| 做法 | 组合式（伪代码，勿直接抄成 add 形态）| 效果 |
|---|---|---|
| ❌ 朴素等权 | 排序(A) ＋ 排序(B) | 同源时稀释 |
| ✅ **正交化后相加** | 排序(A) ＋ 排序( `vector_neut(B, A)` ) | 取 B 中 A 无法解释的部分 ⇒ 真增量，不稀释 |
| ✅ 回归残差 | `ts_regression(B, A, 252, lag=0, rettype=0)` 作第二腿 | 同上，时序版本 |

**算子事实（官方 definition，已核实）**：
```
vector_neut(x, y)                      # Cross Sectional：求 x* 使 x* ⊥ y（横截面正交化）
ts_regression(y, x, d, lag=0, rettype=0)  # Time Series：提回归参数（resid/slope/intercept）
ts_av_diff(x, d)                       # x − mean(x, d)，可恢复被归一化抹掉的幅度
ts_corr(x, y, d) / ts_covariance(y, x, d) # 两变量窗口相关/协方差，可作条件权重
```

⚠ **`vector_neut` 是横截面正交，不是时序正交**。所以 `vector_neut(B, A)` 的语义是
「每天在截面上把 B 对 A 做正交分解，取残差」——正是「同源信号的增量提取」需要的操作。

⇒ **纪律：判断「同数据集能否叠加」前，必须先试一遍 `vector_neut` / `ts_regression` 残差；
只用朴素等权相加就下「不可叠加」结论，是把方法缺陷误判成数据限制。**

⚠ 注意：`vector_neut` 形态叠加**仍会触发本项目的闸5**（`equal_weight_leg_add` 结构判定不区分「是否正交化」）。
即：
> **平台层面完全允许**（RA 除 64 算子无其他限制），
> **但内部闸5 会拦**。若要走正交化路线，需用户明确豁免闸5，或改用「同形态多窗」的合规替代。

> 教训来源：2026-11-12 我在 DEU insiders 战役约 40 波 / 400+ 臂里**一个正交化算子都没用过**，
> 就得出「ATOM 天然限制信息量」的结论。用户质问「是不是你组合ATOM的方法有问题，有没有吃透所有算子的使用场景和作用」。
> 同类错误 2026-11-02 已犯过一次（被质问「平台里未使用过的算子都试着优化了吗」），
> `wq-alpha-gate-push-op-min` §④b 的「★ 强制全量遍历」纪律没有被真正执行。

---

## 四、搭档叠加配方

### 双窗口搭档 > 双字段

同一族取**短窗 + 长窗同时上**，比换字段更有效：

| 搭档 | S | sub |
|---|---|---|
| 短窗单条（14d 变化）| 1.74 | 1.22 |
| **短窗 + 长窗（14d + 90d）** | **2.20** | **1.42** |
| 换另一个字段的单条（如 5d 意外）| 1.12-1.35 | 0.67-0.93 |

机理：短窗捕获近期修正、长窗捕获趋势，互补；换成不同字段反而是重复信息。

### 幅度类 ≫ 广度类

| analyst 字段类型 | 作主核心 | 作辅助腿 |
|---|---|---|
| **修正幅度**（`mean_estimate_change_pct_*`）| — | ✅ **最强（S 2.20）** |
| 广度计数（`*_raised_1wk` / `*_raisednum_4wks`）| ❌ 0.52-1.29 | ✅ 可用（1.62-2.14）|

广度计数区分度低（多数股票同期为零或小数），只能当确认信号叠加，不能自己当核心。

---

## 五、塔归属速查表（派发前必查）

**分类违规的根源是「字段名像什么」≠「属哪个塔」。**

| 字段 | 塔 | trio |
|---|---|:--:|
| `cap` | **PV** | ✅ |
| `predicted_surprise_*` / `mean_estimate_change_*`（predictive_starmine）| **MODEL** | ✅ |
| `oth455_*` | **OTHER** | ✅ |
| `est_12m_*_raised*` / `*_raisednum_*` / `rec_raisednum_*`（analyst7）| ANALYST | — |
| `insd1_*` / `significant_value_*` | INSIDERS | — |
| `nws*_*` / `mws50_*` | NEWS | — |
| `count_institutional_*` / `market_value_institutional_*` | INSTITUTIONS | — |
| `snl27_*` / `snt27_*` | SENTIMENT | — |
| `shrt3_*` / `max_loan_rate_*` | SHORTINTEREST | — |
| `rsk60_*` | RISK | — |

### 最常见陷阱

`predictive_starmine` 的字段**名字像 analyst，实际属 MODEL**。
故 `oth455_*(OTHER) + predicted_surprise_*(MODEL)` **必违规**；
而 `est_12m_*(ANALYST) + oth455_*(OTHER)` **合规**。

### 合规组合速查

| 组合 | trio | 合规 |
|---|---|:--:|
| ANY 非 trio + 非 trio | 0 | ✅ |
| **至多一个** trio + 任意非 trio | 1 | ✅ |
| 两个以上 trio（PV+MODEL / PV+OTHER / MODEL+OTHER）| ≥2 | ❌ |

> 实操：**`cap` 桶是最容易无意引入 PV 的地方**——用它就被算一个 PV 类，不能再挂任何 MODEL/OTHER 字段。

---

## 六、派发前三道自检（各能省一整个 multisim 配额）

平台是 **batch-kill**：一条错，整批 CANCELLED。所以错一条的代价是一整批。

### 自检 A：裸变量名

模板拼接时把 `${H}` 写成裸 `h`，表达式里出现字面量变量名 ⇒
`Attempted to use unknown variable "h"` ⇒ 该臂 ERROR + 其余全 CANCELLED。

```js
const bad = arms.filter(([k,e]) => /[^_\w]h[^_\w]|\(h\)|,h\)/.test(e));
if (bad.length) return { blocked: bad.map(b=>b[0]) };
```

### 自检 B：字段塔归属

列出表达式用到的全部字段 → 反查塔 → 统计 trio 数 → **>1 不派**。

### 自检 C：算子预算

```
推定算子数 = 现有块 + 新腿   （重复子式按出现次数计费）
> 60 不派   （平台硬限 64，超限 batch-kill 整批）
```

---

## 七、质量判据：逐年无负年 > 单看 S

篮子里应至少有几颗「全期均衡型」，而不是全靠高 S 但依赖单年的件。

| 件 | S | 2Y | 最差年 | 判断 |
|---|---:|---:|---:|---|
| A | 2.20 | 2.43 | **1.03** | ✅ 全期均衡（十年全部 ≥1.03）|
| B | 1.64 | **3.18** | **0.25** | ⚠ 依赖近两年 |

**同 S 下优先取最差年更高的那颗**——它在 prod 阶段更稳（prod 相关性漂移猛，单年依赖的件更容易失配）。

---

## 八、标准工作流

```
① 收集候选（已过 checks.fail=[]）
② 逐颗跑闸5 `_detect_equal_weight_leg_add` → **POISON 直接排除，不进后续计算**
   （这一步最先做，成本最低、杀伤最大：DEU 实测 17 颗里砍掉 13 颗）
③ 逐颗读 get_alpha_details → 记录 (S/F/2Y/sub, towers, eff, operatorCount, checks)
④ 按「塔归属速查表」筛掉 trio≥2 的（不做互相关计算，省时间）
⑤ compute_mutual_correlation(剩余候选, threshold=0.7) → 取 max_mutually_below_subset
⑥ 若独立集 < 目标数：
   ├─ 检查是否所有件共享同一复合核心 → 是则拆核心重做
   ├─ 检查是否同一搭档族的内变体（同族互相关常 >0.95，只算 1 颗）
   └─ 只有当「换核心 / 换搭档族」都试过仍不足，才降级为跨类组合
⑦ 对入篮件复核：最紧一对的相关系数要记账（余量 <0.05 要标注风险）
⑧ 落台账：alpha / 状态 / S / F / 2Y / sub / 塔 / eff / operatorCount / 闸5 / 来源
```

### ⚠ 同族只贡献约 1 颗（反复验证 5 次）

| 批次 | fail=0 数量 | 同族互相关 | 实际可入篮 |
|---|---:|---:|---:|
| A | 7 | 0.83-0.95 | 1 |
| B | 8 | 最高 0.9943 | 1 |
| C | 2 | 0.9936 | 1 |
| D | 4 | 0.9759 | 1 |
| E | 5 | 0.86-0.88 | 2 |

⇒ **看到一批 7-8 颗 fail=0 别高兴太早，先算互相相关，通常只剩 1-2 颗。**

---

## 九、常见失败模式速查

| 症状 | 根因 | 修法 |
|---|---|---|
| 一批 fail=0 但只入篮 1 颗 | 同族内变体，共享核心 | 见 §三「换核心」 |
| 换搭档族后 S 掉一截 | 该搭档族单腿弱 | 见 §四「幅度类 ≫ 广度类」 |
| 强件被判违规（三塔）| trio 冲突 | 见 §五速查表 |
| **平台全过但按铁律不可交付** | **跨腿 add（闸5）** | **见 §原则1；重构成单腿形态** |
| 整批 CANCELLED 只 1 条 ERROR | 裸变量 / 单位 / 超 64 算子 | 见 §六三道自检 |
| 独立集卡在 N 上不去 | 核心已饱和 | 换核心或转其它数据集 |
| 某件 S 高但 2Y 跌 | 依赖近两年行情 | 见 §七，优先取全期均衡件 |
