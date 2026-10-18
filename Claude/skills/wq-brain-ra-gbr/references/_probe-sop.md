# GBR 探针派发 SOP —— 最大化「测出数据集好结果」的概率

> 来源：2026-10-13 GBR 战役 **W1–W27 约 175 条**实证（16 处女池探针 + CDS 深挖 + 23 处女集 8 探针）+ 前序 11 波 88 条 / Fundamental 3 波 24 条。
> 目标：用最小预算回答「这个数据集有没有配得上**GBR 已验证结构**的机制」，并把误杀率与连坐率压到最低。
> **与 DEU 版的三个结构性差异**（本区特有，先记住）：① **multi-sim 上限 = 8 条**（DEU 用 10 槽）；② **`LOW_2Y_SHARPE` 闸线随中性化浮动**（1.58 / 2.02 两档）；③ **单一 universe TOP700**（无档位可选，D0 多数数据集无字段）。

---

## 第 0 步：开批前筛选（零成本，能杀掉大部分无效探针）

1. **塔闸（GBR 第一顺位）**
   - `get_pyramid_alphas` → **只挖「未点亮塔 × ALIVE 密度」**。GBR 现状：`model 5（≥3 已点亮 → 规则排除）｜analyst 2｜other 1｜其余 12 类 0`。
   - 已点亮的塔**一律不选**（用户规则）；未点亮塔里按「ALIVE 字段数 × 平台 valueScore / alphaCount」排序。
2. **语义闸（读字段级 description，不是数据集级）**
   - 数据集级 description 会骗人。**开批前必查字段级描述**，剔除三类非信号：**标签类**（`*_label*` / `*_bucket*` / `probability_label*`）、**轴类**（`*_grouping_*` / `sector` / `rbics` 代码）、**元数据类**（时间戳 / 货币码 / SIC 码 / `*_id` / 交易笔数计数字段）。
   - GBR 实证：`dl_riskfree_returns`（40 字段全 `probability_label*`/`quantile_label*`）与 `pv29`（38 字段全 `industry_grouping_*`）**整块非信号**——查描述可零成本跳过。
3. **画像闸**（`tools/fields/field_profile.py --query --region GBR`）
   - coverage<0.6 剔除；`to_med<0.03` → DEAD_STATIC；名字含 `count/num` 且 S≤0.7 → DEAD_COUNT；`to_med>0.70` → DEAD_TURNOVER。
   - ⚠ **GBR 与 DEU 的差异**：GBR 平台 **`LOW_TURNOVER` 实测不拦低换手**（TO 0.0257 通过），因此 `review.turnover_min=0.05` 只是**筛选启发式**、不是平台闸。但「近静态」仍是**机制无用的强信号**（见下条）。
4. **★★★ 近静态闸（GBR 本轮新增判据，最高性价比）**
   - **状态量 / 评级 / 低频类数据（ESG 评级、分析师创新度、供应链占比、期权 IV 水平、网站流量排名）单字段水平信号 TO 落在 0.016~0.041 且 2Y 多负 ⇒ 任何骨架无用，直接跳过。**
   - 实证：本轮 16 个机制里 **8 个命中**（ESG 0.016 / 创新度 0.026 / 供应链 0.020 / IV 0.029…）；`other128` 高管薪酬 8 探针里多颗 TO 0.013~0.016。**开波前按机制类型预筛，可省掉约一半波次。**
5. **历史闸（最重要的单条规则）**
   - 先查 `output_report/GBR_*`、`Claude/skills/wq-brain-ra-gbr/references/*`、`.workbuddy/memory/*`：**有没有已验证结构/已判死族？禁止自造结构开荒、禁止重测已判死的族。**
   - GBR 已验证结构见第 1 步「两个结构」；已判死的类别分支（analyst 五集、fundamental 13 集、techindi、cds 外 other 全域）**不再投波次**。
6. **★★ `ALIVE`/`WEAK` verdict 必须 in-region 复验（2026-10-14 新增铁律）**
   - `field_profile` 的 `S_sg / 2Y_sg / n_tests` **必须能在本地 `backtest_results`（region=该区）里找到对应行**；找不到 ⇒ 该 verdict 不可信。
   - **实证**：`analyst7.est_12m_pre_low` 画像标 **ALIVE S 1.90 / 2Y 2.72 / n=134**，但 GBR 库中该字段 **0 行**（用 `LIKE '%est_12m_pre_low%'` 查证）⇒ 实测水平量、广度比、SUE 型三组构造 **全部 ≤0.37**。**该 ALIVE 是画像伪影，直接投波次会白烧一批。**
   - **操作**：开波前对每个候选 ALIVE 字段跑一句
     ```sql
     SELECT COUNT(*) FROM backtest_results b JOIN expressions e ON e.id=b.expression_id
     WHERE b.region='<R>' AND e.expression LIKE '%<field>%';
     ```
     `COUNT=0` ⇒ 该 verdict 视为 UNTESTED，按探针规格重测，不得直接采信。
7. **概念族分组**：把候选字段按机制族分组（水平量 / 变化率 / 计数 / 比率 / 评级 / 情绪 / 事件 / 网络…），**每族选 1–2 个代表**（cov 最高、alphaCount 最低）。
   - 依据：**同族字段高度相关 ⇒ 测族内一个 = 测族内全部**；不同族才带新信息。
   - ⚠ **同类字段的「水平量 vs 比率」是不同族**：`est_12m_pre_raisednum_4wks`（原始计数，DEAD_COUNT 风险）与「广度比」（上调家数 ÷ 上下调家数之和，`divide` 比率形态，可活）机制不同 ⇒ **判死某数据集前必须把「比率/离散度/标准化」形态各测一次**（本区实证：analyst7 水平量与广度比均死，但这是「测过才判死」的正确顺序）。

---

## 第 1 步：探针批构造（8 槽 = 2 结构 × 3 跨族字段 + 2 机动）

> GBR 的 multi-sim **上限 8 条**（DEU 为 10）。**2 结构 = 本区已验证的赢家**——只测一个结构会错杀字段（结构与字段的匹配是**字段属性**，逐字段不同）。

**两个结构（GBR 已验证）**：

| 结构 | 表达式骨架 | 来源 / 适用 |
|---|---|---|
| **A · house 底座** | `group_rank(ts_mean(vec_avg(F), N), subindustry)`（MATRIX 去掉 `vec_avg`） | 本轮 39 数据集筛选底座；通用首选，N=22/66 |
| **B · techindi 配方** | `group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(add(ts_mean(ts_backfill(F,500),1), ts_mean(ts_backfill(F,500),60)), sector)), std=0.15), lambda_min=0, lambda_max=1, target_tvr=0.50), sector)` @ **CROWDING / decay 2** | [other.md](other.md) `3qVP6pNO` 赢家配方（双窗 + 残差化 + tvr_decay）|

**6 个字段 = 跨概念族代表**（不是同族 6 个）；VECTOR 字段在结构内用 `vec_avg`。
**2 个机动槽**：
- VECTOR 数据集 → 留给 **`vec_max`**（聚合算子是独立搜索维度）；
- 语义方向不明的字段 → 留给 **`reverse`**（GBR 实证：`days_from_last_change` 原始 S −1.39，反向即 +1.39——**方向本身就是信息**）。

**发批前六闸（逐条过，缺一即整批连坐）**：

| # | 闸 | 命令 / 要点 |
|---|---|---|
| ① | 值型自检 | `dispatch` 内置 `expr-lint` |
| ② | 元数检查 | `op_arity.ensure_safe_for_dispatch`（`dispatch` 内置 `op-arity`） |
| ③ | **字段类型（GBR 最易踩）** | **VECTOR/MATRIX 必须取平台实时 `get_datafields`，不得信本地表或缓存 dump**。⚠ GBR 实证：`count_negative_*` 平台实为 **MATRIX**、本地表错标 **VECTOR** ⇒ 误用 `vec_*` ⇒ **整批 FAIL** |
| ④ | 算子存在性 | `op-lint`（GBR 平台清单 **102 个**）。⚠ `vector_neut` **不在** GBR 清单；`tail` 只接 **1 位置参 + 命名参**（`tail(x, lower=, upper=, newval=)`，位置参写法整批 ERROR） |
| ⑤ | 骨架多样性 R2 | `tools/fields/skeleton_panel.py audit --path <f> --region GBR`（**单模板 ≤60%**；多字段 sweep 也须重组骨架，**不得用 `--param-sweep` 绕过**；已锁字段参数扫才可声明 `--param-sweep`） |
| ⑥ | 探针台账 | `probe-slot`（每波探针位上限 2，见 SKILL.md 面板） |

> 合规模板（5 放行形态必用满）：`add`（同字段双窗）/ `divide`（比率）/ `subtract(rank,rank)`（行业内相对）/ `if_else`·`trade_when`（门控）/ `group_rank`·`group_zscore`（组内标准化）。**禁止两条独立信号腿相加**；算子数 <10。

---

## 第 2 步：读数三分法（**GBR 闸线与 DEU 不同，务必按本区口径**）

| 双结构最好读数 | 动作 |
|---|---|
| **S≥1.58 且 2Y ≥ 本档闸线** | 全闸验证：`get_alpha_details`（全 checks）→ prod/self 双端点 → **PnL 互相关去重** |
| **S 1.0–1.58** | **不判死**——「结构没找对」信号带。升级：窗扫描（N∈{5,22,55,66,77,132,252}）、轴扫描（subindustry/sector/industry/bucket/复合轴）、算子微调（`ts_rank`/`ts_decay_linear`/`winsorize` std/`signed_power`） |
| **S<0.5（双结构都）** | 判死；同族字段免测。**判死前自检两问：真的用了两个结构吗？字段真的跨概念族吗？** |

**★★★ GBR 特有：`LOW_2Y_SHARPE` 闸线地图（本区最重要的读数口径）**

| 中性化类型 | 闸线 | 本区实测 |
|---|---:|---|
| **内置分组轴**（SUBINDUSTRY / SECTOR / INDUSTRY） | **1.58（宽）** | CDS 腿 SUBINDUSTRY 2Y=1.57 ⇒ 差 0.01 |
| **因子模型型**（MARKET / CROWDING / REVERSION_AND_MOMENTUM / FAST / SLOW / STATISTICAL / SLOW_AND_FAST / NONE） | **2.02（严）** | CROWDING 2Y=1.73、R&M 2Y=1.67 ⇒ 均差 0.29+ |

- ⚠ **升 S 的因子中性化同时抬 2Y 闸线**（CROWDING 把 S 推到 1.72，2Y 闸线同时升到 2.02）⇒ **破闸必须在「宽档（内置轴）」上调 S，严禁换中性化凑 S。**
- ⚠ **GBR 平台 `LOW_SHARPE` 实测闸线 = 1.58**（非 config 的 delay1=1.25）。
- ⚠ **真值须 ≥ 闸线 + 0.005**（平台把 ladder 四舍五入到 2 位再严格比较）。
- **2Y 要单独看**：S 高 2Y 低 = 早衰（GBR 实证：`news3` 多颗 2Y 1.44~1.72 但 **S≈0**，属「2Y 有 S 无」形态，不可用）。

**★★ 两种 GBR 特有判死形态（读数时识别）**
1. **「F 墙（不变量型）」**：族内 `S 与 1/√TO 严格同向` ⇒ `F = S×√(returns/max(TO,0.125))` 是经济不变量，全参数空间 F 恒定（实证 `analyst47` F 恒 0.96~0.97，只差 `LOW_FITNESS` 0.04 却扫不上去）。
2. **「2Y 有 S 无」**：2Y 高（≥1.4）但 S≈0（≤0.3）⇒ 信号只反映最近 2 年行情，不可用。

---

## 第 3 步：出闸后去重（一条腿只出 1 颗）

- `GET /alphas/{id}/recordsets/pnl` 取两条 PnL 求 Pearson——**零平台配额**的互相关；或用 `compute_mutual_correlation`（本地计算，不占配额）。
- **同机制跨数据集 = 同一条腿**；换结构 / 换字段 / 换轴**不产生新腿**。
  - GBR 实证①：techindi 三字段互相关 **0.88~0.93**（同一模型的多输出）⇒ 整池只值 1 颗。
  - GBR 实证②：CDS 族 `spread ↔ recovery` **0.7616**（>0.7 同腿）⇒ 整族最大互不相关子集 = **1**。
- `self` 相关池**包含自己未提交的 alpha**：self max 高先看驱动记录是不是自己建的，再判「被占用」。
- **GBR 硬墙是 prod 不是 IS**（区域级结论）：IS 全闸候选常被 `PROD_CORRELATION` 拦（实证 techindi `O0J1A88J` prod/self 双 0.9297）。

---

## 预算参考

| 目的 | 成本 |
|---|---|
| 单数据集生死判定 | 1 批（8 条，双结构 × 跨族字段）|
| 数据集「正式判死」（D15 纪律） | **≥8 探针**（可分 1–2 批覆盖 4–8 构造）|
| 潜力确认（1.0–1.58 带） | +1~2 批（窗/轴/算子扫描）|
| 冲闸 | 2–5 批 |
| **判死一条错误路径的隐形成本** | 整个战役的期望产出——**所以第 0 步零成本筛选最值钱** |

---

## 本会话反例清单（GBR 实测，每条都是真金白银）

1. **1 探针判死 → 违反 D15，需补做 8 探针**：W1/W2 对 16 个处女数据集只跑 1 探针即判死，用户指出后补做 W14–W27（110 条）——结论未变（仍只有 CDS 活），但**过程不合规**。**新数据集判死必须 ≥8 探针。**
2. **字段类型错标 ⇒ 整批 FAIL**：`count_negative_*` 平台实为 MATRIX、本地/缓存表错标 VECTOR ⇒ 误用 `vec_*` ⇒ 3 条非法 ⇒ **8 条整批 FAIL**。**类型必须取平台 `get_datafields`。**
3. **`vector_neut` 不在 GBR 算子清单** ⇒ op-lint 拒批（清单 102 个）。
4. **`tail` 位置参写法整批 ERROR** ⇒ 命名参 `lower=/upper=/newval=`。
5. **骨架 R2 连拦 3 波**（单模板 62%~75% > 60%）⇒ 必须**重组骨架**（换外/内层算子），**不得用 `--param-sweep` 绕过多字段 sweep**。
6. **用错设置复现历史 alpha**：曾按区域缺省（decay 4 + SUBINDUSTRY）重跑，而记录实为 **decay 2 + STATISTICAL** ⇒ 只到 1.34（记录 1.95）。**复现历史 alpha 必须拉它自己的 settings。**
7. **`ts_backfill` 用在事件型字段上**：只适状态量；事件量会抹频率（GBR 实证 `ts_mean` 在事件型数据上 S 1.44→0.73）。
8. **只测一个结构**：本轮探针底座单一（house）⇒ 若某字段在 techindi 配方下更强会被错杀——**双结构是保底纪律**。
