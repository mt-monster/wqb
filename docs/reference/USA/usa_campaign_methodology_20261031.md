# USA 战役方法论沉淀（2026-10-30 ~ 2026-10-31）

> 本文件汇总本轮 18 波实测得出的**可复用判据**。每条都有实测数据支撑，不是推测。
> 配套：`docs/reference/USA/usa_campaign_delivery_report_20261031.md`（交付全景）

---

## 1. 五条「起手就该知道」的判据

### 1.1 窗口长度由机制的时间衰减速度决定，不是通用偏好

| 机制 | 最优组合窗 | 证据 |
|---|---|---|
| 内部人买入强度（insider_trx_matrix） | **22 天** | 1→S5.29(但 CW 挂) / 5→2.91 / 11→2.57 / **22→2.47** / 63→2.08 / 126→1.57 / 252→1.49 |
| 内部人买卖比 | **63 天** | 22→S1.44 / **63→S1.55** / 126→S1.12 |
| 借券挤空联动性（risk59） | **504–1008 天** | 504→S2.11 / 756→S2.17 / **1008→S2.24** / 126→S1.72 / 252→S1.46 |
| 董事会治理（board_gov_stats） | **不敏感** | 120 窗 ↔ 504 窗 互相关 **0.9999**，S/2Y/SUB 逐位相同 |

**规律**：知情交易类（内部人）**信息衰减快 ⇒ 短窗**；结构性错配类（借券挤空）**是慢变量 ⇒ 长窗**；治理类**更新频率低 ⇒ 窗口无影响**。
⇒ **开波前先问「这个机制的信号多久衰减一次」**，再定窗口。

### 1.2 「水平残差」vs「走势联动性」是两种不同机制

- 水平残差：`vector_neut(-ts_rank(A, W), ts_rank(B, W))` —— 两个**水平**做差。
- 走势联动性：`-ts_corr(A, B, W)` —— 两者的**同步性**。

后者捕捉「结构性错离」（一个指标高、另一个低），**天然过 CONCENTRATED_WEIGHT + HIGH_TURNOVER 双闸**（相关系数有界 ⇒ 幅度不极端 ⇒ 权重分散、换手 4–5%、margin 17–20bp）。
**卡 F 闸或 CW 闸时，优先试 `-ts_corr` 而不是继续调 decay / 中性化 / winsorize。**

### 1.3 ★ 指标强度与 prod 相关性负相关（选提交候选的第一原则）

| alpha | S | prod |
|---|---:|---:|
| `3qo3Wv5O`（group_neutralize + 22 窗） | **3.42** | **0.8958 ❌** |
| `O0AqkrA7`（insider secondary + risk59 残差） | 2.34 | **0.7832 ❌** |
| `1YN1aZQX`（base 252 窗 + risk59 残差） | 1.74 | 0.7442 ❌ |
| `kqNb7XY6`（mean_buy 22 窗） | 2.47 | **0.6569 ✅** |
| `vROPEJ8w`（mean_buy 63 窗） | 2.08 | **0.5517 ✅** |
| `E56YodoJ`（买 − secondary 卖 差值 126 窗） | 1.63 | **0.6435 ✅** |

⇒ prod 池里已有的是「教科书化的形态」；越往指标极致走越贴近它。
⇒ **提交候选排序以 prod 升序为第一原则，S/F 只作次级筛选。**

### 1.4 压 prod 的五条偏离轴（全部实测有效）

1. 更长的组合窗（63 → 126 → 252 → 504）
2. 更粗的口径（total / mean / top，而非细分 secondary）
3. **更少几何加工**（裸 `ts_zscore` 而非 `group_neutralize`）
4. 换宇宙 / 换中性化（设置层也是偏离轴）
5. **用差值（买 − 卖）而非比值（买 / 卖）** —— 差值避免分母趋零的爆炸，指标更稳且 investability 更高

### 1.5 跨数据集只能用 vector_neut 残差化，绝不能用 multiply

- 跨数据集相乘：S **−1.36** / DD 46.9%（差值 × risk59）；S **−3.27** / DD **171.9%**（短窗买入 × risk59）
- 跨数据集残差化：S +2.34 / F +1.96 / **IS_LADDER PASS** / 塔位 2–3 座
- 残差化四条纪律：
  1. **主腿必须是信息量更大的那个数据集**（insider 主腿 ≫ governance 主腿）
  2. 跨数据集不用 multiply
  3. **残差化修不了 2Y ladder**（过不过取决于主腿的 2Y 本身）
  4. **差值型 insider 腿在跨数据集残差化里会被消掉**（wave278 V1/V5 都弱）⇒ 能进组合的 insider 腿是「纯买入」

---

## 2. 四条「塔位」纪律

### 2.1 数据集 category ≠ alpha 塔位

- `insider_trx_matrix` 的 category 是 **OTHER**（不是 INSIDERS）
- `board_gov_stats` 的 category 是 INSIDERS，但用了 `rank(cap)`（PV 字段）⇒ 塔位 **[PV, INSIDERS]**
- **必须读 `pyramids.list` / `pyramid_short`**，不能靠数据集 category 推断。

### 2.2 ★ 换 bucket 的分母字段 = 切换塔归属

| alpha | bucket 分母 | 塔位 |
|---|---|---|
| `pwdQlr2V` | `rank(cap)`（PV 塔字段） | **[PV, INSIDERS]** ❌ |
| `ZYQkoman` | `rank(board_member_count_2)`（INSIDERS 自身字段） | **[INSIDERS]** ✅ 纯净单塔 |

⇒ 想要纯净单塔时，**用目标数据集自己的字段做 bucket 分母**；`rank(cap)` 是最常见的 PV 污染源。

### 2.3 塔混检查表

- 禁混的是 **{PV, MODEL, OTHER} trio 内部两两互组**（含 PV+PV）；trio × 非 trio 允许但总量 ≤5（已满 5）
- **RISK × OTHER 允许**（不在 trio 内）⇒ 本轮实测 `pyramids.list = [RISK, OTHER]` 与 `[RISK, INSIDERS, OTHER]` 均成立
- 每个两塔组合候选 ≤3（RISK×OTHER 本轮已用 3 ⇒ 该组合封盘）

### 2.4 互相关是「篮子里装得下几颗」的独立约束

- `compute_mutual_correlation` 是**本地计算、零平台配额、零相关性槽** ⇒ **任何 prod 测量之前先跑它**
- 治理族候选互相关 **0.93–0.9999** ⇒ 同篮最多 1 颗
- insider 纯买入族互相关 **0.43–0.97** ⇒ 同篮最多 2 颗
- **差值型 insider（E56YodoJ）与所有其他 insider 候选互相关仅 0.02–0.16** ⇒ 天然独立分支
- **互相关达标 ≠ prod 达标**（wave276 的 6 颗互相关全 < 0.70，但 3qo3Wv5O prod 0.8958）⇒ 两个约束必须分别验

---

## 3. 三条「数据集级」教训

### 3.1 ★ 论坛机制的方向声明不可信，必须实测

论坛帖 `43153154839831`（成长外推反转，1 赞）明确写「USA 方向一致」⇒ 实测 **7/10 模板 S 为负**。
⇒ **论坛帖子给的是机制与窗口先验，方向永远自己测。**

### 3.2 已被市场消化的因子不要再挖

- 应计质量因子（Sloan 1996 accruals anomaly，fundamental93，46 字段 uCnt≤12 极冷门）⇒ 实测 **|S| ≤ 0.34**，已被套利
- 估值 / valuation-momentum（registry `USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL`）⇒ prod 0.9289
- ⇒ **冷门 ≠ 有信号**；冷门只保证 prod 低。

### 3.3 二元 / flag 字段在截面几乎无变化

- 二元治理 flag（CEO/董事长合一、多 CEO）连续化后仍 S ≤ 0.18，且 **TO 仅 0.66–0.77%** ⇒ 连 LOW_TURNOVER 闸（0.01）都不过
- ⇒ **极慢变量 + 二元 = 无截面信息**

---

## 4. 五条「工程」教训

### 4.1 `group_rank` / `bucket` 的参数语法

- `group_rank(x, group)` 的第二参是**分组名**（subindustry / industry / market），**不是** bucket 对象
- `bucket(x, range=...)` 的 range **必须是命名参数**，且只有 1 个位置参数
- 嵌套时本地签名解析器按**就近绑定** ⇒ `bucket(group_rank(...), range=...)` 会把 range 误归给内层 group_rank
- **派发前必跑 `op_arity` 闸**（本轮连续踩 3 次）

### 4.2 `upsert_backtest_rows` 的 N34 陷阱

rows 必须带 `code` / `expression` / `expr`，否则 `expr_id=None` ⇒ **整行静默丢弃并返回 n:0（不报错）**。
且必须**先 `upsert_expressions` 再 `upsert_backtest_rows`**。

### 4.3 `expressions` 表的幂等键 = region+wave+expression（不含 bucket/settings）

⇒ 矩阵波次在该表互相覆盖 ⇒ **权威数据源一律用 `backtest_results`**。

### 4.4 `submit_verdict` 的 UNVERIFIABLE 不是失败

`GET /alphas/{id}/submit` 平台恒返 404 ⇒ 提交层不可验证 ⇒ 未提交候选只会得到 `UNVERIFIABLE`（exit 10）或 `BLOCKED`（exit 1）。
⇒ **`UNVERIFIABLE` = 模拟层无 FAIL + prod/self 需另跑 `check_correlation` 确认**；`BLOCKED` = 模拟层有硬 FAIL。

### 4.5 平台 prod 单并发 + 跨会话争用

- prod 计算是**账号级单并发槽**；另一会话（GBR/TOP700）会长期占用
- `correlation_busy` 时 `retry_after` 给的是秒数，**等窗口内不要重新触发**（会变成 busy holder）
- ⇒ **批量测 prod 要串行 + 耐心重试**，一次超时不代表 prod 不可用

---

## 5. 开波前的固定动作清单（按顺序）

1. `grep -r "<dataset_id>" docs/ reports/ Claude/skills/` —— **本地既有台账三查**（曾因漏查差点重复烧一批）
2. 读字段 description 逐条分类：有经济含义且非前瞻 → 可用；含 future/forward-looking/target/label/prediction → **黑名单**；语义不透明（"Value of the field"）→ 只做探针
3. `check_expressions`（本地算子签名闸）→ 必须 10/10 PASS
4. `preflight_expressions(dataset_id=...)` → 必须 `any_changed == false`（`valid` 会被 `driver="gaussian"` 之类的误报污染，**以 `any_changed` 为唯一判据**）
5. **全库扫描 SQL**（找存量候选，含自己以前会话的）→ 用 prod 升序排
6. `compute_mutual_correlation`（本地零配额）→ 确认篮子装得下
7. 排 prod（串行，耐心重试 busy）
