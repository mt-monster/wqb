---
name: wq-operator-playbook-by-gate
description: 破闸算子处方与语法手册。候选卡平台闸（LOW_SHARPE/FITNESS/换手/CONCENTRATED_WEIGHT/LOW_SUB_UNIVERSE_SHARPE/IS_LADDER_SHARPE/PROD_CORRELATION/SELF_CORRELATION/CLUSTER_TEST）要挑算子时用；按六步 SOP 破闸时用；发批前判方向是否试完、整批 CANCELLED/ERROR 定位算子语法时用。含按闸算子优先级、103 算子语法与命名参规则、unit_handling=VERIFY 量纲规则、三条正交轴族与硬约束、算子预算账、发批前对账 SOP。
layer: L4
last_verified: 2026-10-30
agent_created: true
---

# 破闸算子手册（按闸开方 + 语法对账 + 破闸配方）

## 职责边界

- **本 skill 负责**：候选卡在某个平台闸时开**算子处方**——按闸挑首选算子与破闸配方（六步 SOP §R）、103 算子语法与命名参对账（引号规则 / arity / 幽灵算子，§2）、组合范式混批与发批前的「方向是否试完」判定（§0 / §4）。
- **本 skill 不做**：不回测、不提交；不回答「某条提交检查的线是多少」（只读体检 → [`brain-how-to-pass-alpha-test`](../brain-how-to-pass-alpha-test/SKILL.md)）；提交资格与否决走 `submit_verdict`（它只能拦不能放）；已锁定核心想法、做「指标推到闸 + 算子压缩到最少」双目标时 → [`wq-alpha-gate-push-op-min`](../wq-alpha-gate-push-op-min/SKILL.md)。
- **上游 / 下游**：上游 = 批量回测跑完、卡闸待修的候选（S3/S4，来自[`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md) 或区域 RA skill）；下游 = 改好的表达式回批量仿真复测（S3），全闸绿后经用户确认走 [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)。

> 立本 skill 的起因（2026-10-06）：某一区跑了 80 波「无解」，复盘发现**全战役只用了约 20 / 103 个算子**，
> 且仓库里**早有** `Claude/skills/wq-brain-campaign-toolkit/config/platform_constraints.json` 的算子约束清单（含「算子 → 适用场景 → 问题诊断」映射，连 `ts_target_tvr_hump` 都列为 P2 换手算子），
> 只是**从没读过**。用户评语：「算子的尝试远远不够丰富」。本 skill 就是那条纪律的落地。

---

## §R 破闸配方（六步 SOP）——先读这个

**本章（§R–§4）正文自包含：阈值、判据、证伪项都在下文各表里。** 本 skill 无 `references/` 子目录；
六步的**战役实账本**随各区域判死 / 实证沉淀进 `tracking/<REGION>/reference/`（DB 台账），不单独维护全局文件。

| 步 | 动作 | 关键判据 |
|---|---|---|
| 0 | `submit_verdict` 定位**唯一**卡点 | `failed_ra_count` 才是资格门（warning 也计入）；读 `value`/`limit`/`year` |
| 1 | 判**缺口性质** | **Δ≤0.005 ⇒ 分辨率极限，别再刷同维参数，去换"维"** |
| 2 | 算子/轴面**对账** | `get_operators` 差集逐个至少 1 条；先读仓库现成资料 |
| 3 | 按**增益量级**逐维加/换 | 轴族(+0.49) > `decay`(+0.10) > 双窗(+0.02 零代价) > 异族第三轴(+0.01) > 变换(S+0.10) > 换字段 |
| 4 | **正交轴族叠加**直到闸过 | 三条有效族 + 三条硬约束（见 `§4.1`）；**轴必须与经济结构同源** |
| 5 | **终验三闸**（顺序不可颠倒） | `submit_verdict` → `check_correlation(refresh=True)` → `brain-alpha-robustness` |
| 6 | **台账回写 + 零提交** | 写 `robustness_<id>`；agent 一律不提交 |

**最快见效的三个动作**：① 换**轴族**（不是换族内参数）② 扫平台 **`decay`**（有单峰）
③ 加**双窗** `add(ts_mean(x,短), ts_mean(x,长))`（唯一零代价杠杆）。

---

## 0 ★★★ 铁律：判「无解 / 试完了」之前，必须先做算子对账

```
① 调 get_operators → 拿平台实时清单（当前 103 个）
② 与本波实际用过的算子集合做差集
③ 差集里凡是**能合理作用于本信号**的，逐个至少试 1 条（放在同一骨架下）
④ 只有差集为空、或差集里每条的实测都劣于基线，才允许写「该方向算子面已穷尽」
```

- **禁止**用"我记得只有这几种写法"代替对账——`docs/reference/operators_catalog.json` 有 103 条定义，`Claude/skills/wq-brain-campaign-toolkit/config/platform_constraints.json` 有约束清单。
- 一次对账的产出应写成一张表（算子 / 变体 / S / F / 换手 / 目标闸 / 结论），**可复查**。
- **经验规律**：本类战役里真正有效的杠杆，**绝大多数来自「换算子 / 换分组轴」，而不是「换参数」**。
  参数面（同一算子的窗长/系数）通常几十条就到峰；算子面的宽度才是未被开采的。

---

## 1 ★★★ 按闸开方：先说清「要修哪个闸」，再挑算子

**先定位唯一卡点**：`submit_verdict(<alpha_id>)` → `reason_code = FAILED_COUNT_RA:<check名>`。
**平台把 `LOW_SHARPE` / `LOW_FITNESS` / `IS_LADDER_SHARPE`(或 `LOW_2Y_SHARPE`) 的 WARNING 视同 FAIL**，
且提交层是**严格不等式**（`value == limit` 判 FAIL）。

| 闸 | 阈值 | 首选算子 / 手段 | 已被证伪（别浪费批） |
|---|---|---|---|
| `LOW_SHARPE` | ≥ 1.58 严格 | `quantile`（替 `signed_power`，S +0.10）；`signed_power` 指数调小（0.3→0.2，S +0.03）；`group_rank`；降 `decay`；`winsorize` | 时序归一（`ts_rank`/`ts_zscore`/`ts_quantile`）会把 S 打崩 |
| `LOW_FITNESS` | ≥ 1.0 | `ts_mean` 平滑；`ts_decay_linear`；`hump`（降换手抬 F）；`quantile` 压尾 | — |
| `IS_LADDER_SHARPE` / `LOW_2Y_SHARPE` | ≥ 1.58 严格（**实为分档**：2Y<1.58 显示 1.58 / 2Y≥1.58 显示 **2.02** ⇒ 实际常需 2Y≥2.02，见 `wq-brain-ra-gbr` 闸线地图） | ① **换分组轴**（增益最大）② **platform `decay`**（有单峰，须扫）③ **双窗平滑 `add(ts_mean(短), ts_mean(长))`**（同字段不同窗 = 合规"单信号多窗平滑"，唯一零代价杠杆）④ **异族第三层分组轴**（图聚类轴 + 行业族轴可叠加）⑤ `ts_target_tvr_hump`（降换手顺带升 ladder，但过峰会反噬）⑥ **★噪声瓶颈诊断矩阵**：在同一位置**逐个**替换 `ts_rank` / `ts_decay_linear` / `ts_scale` / `quantile` / `signed_power` / `winsorize`（各 1 条）—— **只有 `ts_decay_linear` 有效 ⇒ 瓶颈在噪声/换手，不在形状**（GBR news50 单层 `ts_decay_linear(·,22)` 实测 **S+0.21 / F+0.26 / 2Y+0.62 / TO−0.07**，ladder 由 FAIL 转 PASS；同位置其余替换全弱）⑦ **★无界字段先按文档 `winsorize`**：字段文档写「无界 / 使用前须 winsorize」的（如 `tm_17_*_r10_q1`）必须先 `winsorize(std=2)` 再做任何时序变换，否则等于用未标准化输入硬算 | ❌ **叠两层及以上**的 `hump`/`ts_decay_linear` 再平滑（单层有效、叠加反噬）；`ts_quantile`；`driver=cauchy`；同族轴第三层叠加（−0.11） |
| `LOW_SUB_UNIVERSE_SHARPE` | **比值闸** = `0.75×sqrt(子宇宙/本宇宙)×本alpha sharpe`（系数逐区实测，别套用） | **分组轴换到 `market`（决定性）/ `exchange`**；`signed_power` 压尾（⚠ 先看多空对称性）；长窗 `ts_rank`/`ts_decay_linear` 平滑 | ⚠ 分组轴不是通用旋钮，逐区实测；⚠ **把 S 压到刚过 1.58 会同步抬高 SUB 绝对要求** |
| `CONCENTRATED_WEIGHT` | ≤ 0.1 | **数据品质问题**：补时间维覆盖率 / 换字段类型 / 缩小 `ts_backfill` 最小窗；结构性拒绝时只剩 `trade_when` 门控 | `truncation` / `decay` / 中性化 / 平滑**修不了 CW**；⚠ **CW 是 RA 层失败项（计入 `failed_ra_count`），不是 WARN**（GLB 实测 40 颗 `rsk60_offer` 候选全卡此闸，`ra_failed_checks=["CONCENTRATED_WEIGHT"]`）；⚠ 换外层算子（`group_rank`）**会把 S 一起拖塌**（GLB：S2.75→1.46、fRA 1→4 ⇒ 反向恶化） |
| `HIGH_TURNOVER` | **≤ 0.7**（平台线，非 0.4） | `ts_decay_linear` / `hump` / `ts_target_tvr_hump` / `ts_target_tvr_decay` / `trade_when` / 换骨架 | `ts_decay_exp_window` **是幽灵算子** |
| `LOW_TURNOVER` | ≥ 0.01 | 缩短平滑窗 / 降 decay / `ts_delta` / 提高信号更新频率 | — |
| `PROD_CORRELATION` | < 0.7（我方铁律） | **① 改设置档案（最便宜，先做）**：换中性化 / 换 `decay` / 换 `truncation` / 换 `maxTrade` / 换 `nanHandling` —— 严格单变量、可复现、零额外成本；**② 改持仓类改信号**：换字段 / 换概念 / `vector_neut(主体, rank(异源轴))` 残差化 / 换分组轴 / `trade_when` 分层 | ⚠ **只改时序类**（`hump`/`decay`/`ts_mean` 慢化）降 prod 会把 **self 反向推爆**（EUR 实证 self 0.90+）；★ **prod 是「持仓形态」的属性，不是「信号」的属性**（GLB：同一表达式族仅换中性化 ⇒ prod 0.694 vs 0.8885；GBR 单变量实测 0.6506→0.7736→0.8333→0.8719）；⚠ **降换手会把 prod 推高**（TO 0.78→prod 0.76、TO 0.55→prod 0.84）⇒ 换手维度上 prod 与 2Y 是剪刀差，别指望靠 `decay` 同时降两者 |

> ★★★ **破闸改持仓 ⇒ prod 必须重测**（顺序是硬的，2026-10-28 GLB 实测）
>
> 任何破闸动作（换中性化 / 换外层算子 / 换分组轴 / 换窗口 / 换信号腿）**都会改持仓形态**，
> 而 prod 跟的是**持仓**不是信号 ⇒ **顺序固定为：**
> **① 修 RA 闸 → ② 重测 prod → ③ 再算互相关 → ④ 才能进篮子。**
> 跳过 ② 会把「RA 闸修好了但 prod 已越线」的候选塞进篮子。
> 实证：`mLmxKN12`（同族 decay5+负号）prod **0.694** PASS，`WjOQX8rj`（同族仅换 FAST 中性化）prod **0.8885** FAIL —— 两者表达式族相同。
> 同理 §1 表里所有「换 X 类算子」类手段，**全部都要重测 prod 与 self**。
| `SELF_CORRELATION` | < 0.7 | 拉开 `(neutralization, decay)` 组合；同族只出一颗代表 | 同腿近亲提交后 self 冲 0.99+，**换腿不足以去同族化** |
| `CLUSTER_TEST` | DEU/KOR/HKG/IND/GBR/TWN ≥ 1.0，默认 ≥1.58 | `group_*` 换个不一样的分组轴；降低信号与大盘的相关 | 判定用 check 自带的 `limit`，别按区域名硬编码 |

---

## 2 ★ 语法与命名参规则（踩过的坑全在这）

### 2.1 引号规则（这条最容易整批报废）

| 位置 | 写法 | 说明 |
|---|---|---|
| **分组名**（`sector`/`industry`/`subindustry`/`market`/`country`/`exchange`/分组字段键） | **裸写**：`group_neutralize(x, subindustry)` | **加引号会 `invalid input at index 1, must be an expression`，且可能整批 CANCELLED** |
| **`bucket` 的箱定义** | **必须命名 + 双引号**：`bucket(rank(x), range="0,1,0.1")` / `buckets="0.3,0.7"` | 写成位置参数字符串（`bucket(rank(x), "0,1,0.1")`）**报同一个错** → 这是平台解析器的已知行为 |
| **`driver=`** | 双引号或裸写见平台定义：`ts_quantile(x, d, driver=gaussian)` / `ts_quantile(x, d, driver="gaussian")` | 合法值：`gaussian`/`uniform`/`cauchy`（+ `nan`/`true`/`false`） |

> **排查口诀**：批量出现 `? ERR` + `status=ERROR` + 全部 child `CANCELLED` ⇒ **先逐行找"该裸写的加引号 / 该命名的写成位置参"**，不要先怀疑字段或并发。

### 2.2 命名参数族（位置参传错 = 整批连坐）

`hump(x, hump=0.01)`｜`bucket(x, range= | buckets=)`｜`winsorize(x, std=4)`｜`tail(x, lower=, upper=, newval=)`｜
`ts_target_tvr_hump(x, lambda_min=, lambda_max=, target_tvr=)`｜`ts_target_tvr_decay(...)`｜`quantile(x, driver=, sigma=)`｜
`rank(x, rate=2)`｜`scale(x, scale=, longscale=, shortscale=)`｜`normalize(x, useStd=, limit=)`｜
`ts_backfill(x, d, k=)`｜`ts_rank(x, d, constant=)`｜`ts_scale(x, d, constant=)`｜`ts_decay_linear(x, d, dense=)`｜
`group_backfill(x, group, d, std=)`｜`ts_regression(y, x, d, lag=, rettype=)`｜`kth_element(x, d, k, ignore=)`｜
`add/subtract/multiply(..., filter=)`

- **`quantile` 的位置参数只有 1 个**（本地 `platform_constraints.json::quantile_arity=1`），
  但**关键字 `driver=` / `sigma=` 实测平台可用**（2026-10-06 实证：`quantile(x, sigma=0.5)` 201 通过、`driver=cauchy` 也跑出结果）。
  ⇒ **本地 arity 闸比平台严**，遇到"本地拦但疑似合法"的形态，用**单独小批（2 条）**去试，别混进大批。

### 2.3 长窗算子的第 2 参永远是**天数**，不是分组名

`ts_zscore(x, industry)` / `ts_mean(x, sector)` 一类的写法 ⇒ **整批 CANCELLED**。
分组只能用 `group_*` 家族（`group_neutralize` / `group_rank` / `group_zscore` / `group_scale` / `group_mean` / `group_sum` / `group_std_dev` / `group_count` / `group_backfill` / `group_cartesian_product`）。

### 2.4 幽灵算子（用了整批 ERROR/CANCELLED）

```
group_normalize, sigmoid, ts_decay_exp_window, ts_entropy, ts_max, ts_median,
ts_min, ts_min_max_cps, ts_percentage, ts_skewness
```
外加：**`negate` 不存在**（用 `multiply(-1, x)`）；**`vec_ir` 不存在**。
权威源 = `Claude/skills/wq-brain-campaign-toolkit/config/platform_constraints.json::ghost_ops`（`ts_min`/`ts_max` 另列于 `inaccessible_ops`）。

### 2.5 字段类型路由

> ★ **已落成代码闸**（2026-10-06）：`wqb_tools.py dispatch` 内置 `field-type-lint` ——
> 发批前扫出**未被 `vec_*()` 包住的 VECTOR 字段**，打印可复制的修好表达式并**拒绝派发**。
> 背景：同日两次因 VECTOR 直接 `ts_backfill` 导致整批 CANCELLED（平台报 `does not support event inputs`），
> 第一次记了纪律、第二次仍漏 ⇒ **纪律要落进工具，不能靠记性**。

- **VECTOR** 字段必须先 `vec_avg / vec_max / vec_min / vec_sum / vec_count / vec_norm / vec_range / vec_stddev` 聚合再套 `rank` / `ts_*`；**VECTOR 禁直接 `ts_backfill`**。
- **MATRIX** 字段**禁 `vec_*`**（会 24/24 ERROR，白烧配额）。
- 字段存在性**只信平台**（`get_datafields` / `validate_expressions`）；本地 `fields` 表会把幽灵字段标成有效。

### 2.6 区域限制

- 分组字段区域禁用：**JPN 不支持 `sector` / `industry` / `subindustry`**（硬拒绝）。
- 窗长白名单：`[1, 5, 22, 66, 252, 504, 1008, 1260]`（非白名单窗**大多是告警不拦截**，但 SOP 要求给出理由或实测证据）。
- `level: genius` 的算子（如 `ts_target_tvr_hump` / `ts_av_diff` / `ts_ir` / `tail` / `group_cartesian_product`）**本账号实测可直接跑**，不是拦路虎。

### 2.7 ★★★ 量纲（unit）规则：`unit_handling=VERIFY` 下带单位字段不能与无量纲常数直接运算

**报错原文（2026-10-30 DEU 一次连挂 3 条同批）**：

```
Incompatible unit for input of "vector_neut" at index 1,
expected "Unit[]", found "Unit[TSShare:1]"
```

**根因**：`unit_handling=VERIFY` 会让平台做量纲推导。带 `Unit[...]` 的字段（股数 `Unit[TSShare:1]`、金额、成交量、计数）**不能与无量纲常数直接相加/比较/开方**，也不能填进要求 `Unit[]` 的参数位。

**两类触发点，按出现频率排**：

| # | 写法 | 报错 | 合规修法 |
|---:|---|---|---|
| **1** | `vector_neut(主体, <股数/金额/成交量字段>)` | `Incompatible unit ... at index 1, expected "Unit[]", found "Unit[TSShare:1]"` | 正交腿外先 `rank()`：`vector_neut(主体, rank(ts_backfill(<字段>, 22)))`（`rank` 输出 [0,1]，天然无量纲） |
| **2** | `add(<带单位字段>, 1e-4)` / `add(F, 0.0001)` | 同款 `Incompatible unit` | **同单位相除**收口，**不要用 ε 兜零** |
| **3** | `greater(<带单位计数>, 常数)` | 同上 | 门控一律 `greater(rank(x), 0.5)` |
| **4** | `divide(F, cap)` 后**直接**与常数比较 | 同上 | 外层再包 `rank()` 或 `ts_zscore(·, W)` 才比较 |
| **5** | `power(<带单位字段>, 2)` | 同上 | 先 `rank(F)` / `ts_zscore(F, 66)` 归一，再 `power` |

**实测正面对照（能过，因为正交腿天然无量纲）**：`P0oe6wpJ` 的 `vector_neut(主体, vec_avg(snl27_relpopularity08))` —— `relpopularity` 是**比率**，`Unit[]`，直接可用。

**排查顺序（别乱猜）**：
1. `vector_neut` 报 units 错 ⇒ **先看 index 1（第二参 / 正交腿）**，再看主体；
2. 非 `vector_neut` 的 units 错 ⇒ 找那一行里**唯一带单位的字段**与**唯一的裸常数**，把它们分离；
3. 修完再看**外层比较**（`greater` / `trade_when` 条件位）是否也在拿带单位值比常数。

**一句话记法**：**带单位的量只能与同单位的量相除/相比；要跟常数打交道，先 `rank()` / `ts_zscore()` 收口到无量纲。**
这和 `cap`（`CSPrice·CSShare`）的处理是同一条规则 —— 比值/比较前先收口。

---

## 3 组合范式（同一批里应该混合出现，别只换参数）

| 范式 | 做法 | 适合修的闸 |
|---|---|---|
| **替换核心** | 同功能类别内换算子：`ts_mean`↔`ts_decay_linear`↔`ts_av_diff`↔`ts_ir`；`quantile`↔`signed_power`↔`zscore`↔`rank` | SHARPE / LADDER |
| **外层包裹** | 最多 2 层：`quantile` / `signed_power` / `winsorize` / `normalize` / `scale` / `trade_when` / `hump` | 分布类闸 |
| **插入处理** | `ts_backfill`（补覆盖）/ `is_nan`（条件）/ `pasteurize`（去 INF）/ `densify`（分组压缩） | 覆盖率 / CW |
| **条件门控** | `if_else(cond, a, b)` / `trade_when(cond, x, -1)` + `greater/less/and/or/not` | 换手 / LADDER / 分层降 prod |
| **分组轴变换** | 换轴族：行业族（`sector`/`industry`/`subindustry`/`market`）↔ 图聚类/自定义 GROUP 字段；**跨族叠加有效，同族叠加递减** | LADDER / SUB / PROD |
| **多窗平滑** | `add(ts_mean(x,w1), ts_mean(x,w2))`（**同字段、同形态、仅窗不同 = 合规**） | LADDER / 换手 | <!-- lint:counterexample -->
| **自造分组** | `group_neutralize(x, bucket(rank(cap), range="0,1,0.1"))`；`group_cartesian_product(g1, g2)` | SUB / PROD |

> ⚠ **禁混信号**：不得把**两条不同信号腿**等权相加（`add(rank(腿A), rank(腿B))` 违规，KOR 七条漂亮结果已作废）。
> 判定实现在 `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py::_detect_equal_weight_leg_add`：
> **放行** `add(abs(x), 0.01)`、`add(ts_mean(x,22), ts_mean(x,66))`（同形态仅窗不同）；
> **拦截**两条形态不同的信号腿。

---

## 4 实测增益库（跨区，按量级排序；写配方时优先复用）

| 杠杆 | 量级 | 出处 |
|---|---|---|
| **自造分组轴 `bucket(rank(<字段慢分量>), range="0,1,0.1")`** | **ladder 1.58 → 2.07（FAIL 1→0）** | DEU W89 |
| 换分组轴（行业族 → 自定义/图聚类 GROUP 轴） | **ladder +0.36** | DEU starmine 族 |
| platform `decay` 调档（有单峰，须扫） | **ladder +0.10**（4→8）；GBR dec12→8 使 ladder 1.58→**2.07** | DEU / GBR |
| `trade_when` 条件门控 | ladder **+0.52**（HKG 流动性门）；⚠ DEU starmine 族为 **−0.06**（不可迁移） | HKG / DEU |
| 双窗平滑 `add(短窗, 长窗)` | ladder +0.02 **且 S +0.09 / F +0.36 / 换手↓**（唯一零代价） | DEU；HKG vwap 族 1.80→2.08 |
| 异族第三层分组轴 | ladder +0.01 | DEU |
| `quantile` 替 `signed_power` | S **+0.10**，ladder 近似不变 | DEU |
| `signed_power` 指数 0.3→0.2 | S +0.03 | DEU |
| `group_rank`→`group_zscore` | F **+0.10~0.17**（非保序，prod 须重测） | 跨区 |
| `ts_target_tvr_hump(x, target_tvr=τ)` | 换手 0.116→0.109；**ladder 随 τ 上升后过峰反噬**（0.05/0.10/0.15/0.20 = 0.98/1.39/1.53/1.58，0.30 掉回 1.57） | DEU |
| `hump(x, hump=)` | **换手/prod 杠杆**，不改持仓 ⇒ 同族已提交时会把 self 推爆 | EUR / DEU |

### 4.1 ★★★ 轴族清单（"换轴"是 ladder/SUB/PROD 的第一杠杆；**要换"族"而不是换族内参数**）

| 轴族 | 写法 | 备注 |
|---|---|---|
| ① 行业族 | `sector` / `industry` / `subindustry` / `market` / `country` / `exchange` | 组名**裸写**；JPN 不支持前三个 |
| ② 图聚类/自定义 GROUP 字段 | 数据集里的 GROUP 型键（如 `oth455_*`） | 与行业族**正交**，可叠加 |
| ③ **慢分量分位桶（自造）** | `bucket(rank(ts_mean(ts_backfill(F,1008), 252)), range="0,1,0.1")` | **最强**；`range=` 必须命名+双引号 |
| ④ 交叉/笛卡尔 | `group_cartesian_product(g1, g2)` | 过细会崩；与行业族做积常退化成其一 |

**三条实证约束**（DEU W89 单变量对照）：
- **桶要按"信号之外的东西"分**：按信号自身分桶（`bucket(rank(signal))`）⇒ ladder 从 2.07 崩到 0.91~1.29。
- **桶粒度十分位最优**：0.05 / 0.2 / 中位数两半 全崩（每组样本不足）。
- **外层算子**：`group_neutralize` 与 `group_rank` 都可过闸（前者 S 高、后者 sub 高）。

### 4.2 论坛两条"看起来很美"的 ladder 配方 —— **本账号实测不可用**（别再试）
- **`rank_by_side(x)`**（论坛 70 赞，实测 0.28→2.44）：平台报 **`inaccessible or unknown operator`** ⇒ 无权限。
  其"等价写法" `group_rank(x, sign(x))` 报 **`Incompatible unit ... at index 1`** ⇒ `sign()` 不能当分组字段。
  **合规替代 = 用 `bucket` 自造轴**（见 §4.1 ③，实测有效）。
- **`power(ts_rank(alpha, 180), 2)`**（论坛 13 赞，JPN 实测 1.24→≥1.58）：在 DEU starmine 族**反而伤**（S 1.69→1.44、ladder 1.58→1.52）。
  ⇒ 数据集特异，`oth335` 类基本面有效、本族无效。
- 顺带证伪：`quantile(driver=cauchy)`、`multiply(alpha, add(1,alpha))`、`signed_power(alpha,2)`、`group_zscore(alpha, densify(market))`（`densify(market)` 只有 1 组 ⇒ 退化成全局 zscore = 无操作）。

**反面清单（同区同族实测劣化，别重走）**：时序归一化（`ts_rank`/`ts_zscore`/`ts_quantile`）、
对已合成信号再平滑（`ts_mean`/`ts_decay_linear`/`hump` 套在双窗外面）、
`quantile(driver=cauchy)`、同族轴三嵌套、`group_cartesian_product` 造过细组、
中性化换 `REVERSION_AND_MOMENTUM`（会把依赖分析师/基本面修正的族整族摧毁）、
`modify` 类：`truncation` / `nanHandling` 对某些族**逐位无影响**（先小批验证是否真有杠杆）。

---

## 5 发批前的算子对账清单（照着打勾）

```
[ ] 调过 get_operators，并把本波用到的算子列出来做差集
[ ] 差集里"能作用于本信号"的算子，逐个至少 1 条变体进批
[ ] 表达式里没有：引号包的分组名 / 幽灵算子 / 长窗算子塞分组名
[ ] 需要 range=/buckets= 的算子写成了命名 + 双引号
[ ] 新算子/新命名参先单独起 2 条小批验证语法（一条语法错会连坐整批）
[ ] 本波的 10 条里，至少覆盖 ≥3 种范式（替换 / 包裹 / 插入 / 条件 / 换轴），不是同一算子的 10 个参数
```
