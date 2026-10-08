# 01 · 平台规则与硬门槛

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-09-29
>
> **现行政策提示（2026-09-30 合并时补）**：本文里「403 零成本 → 直接 POST 就是预检」的说法只对**被拒**的那一半成立——事先无从知道它会 403 还是通过，而通过的 POST 就是一次真实、不可撤销的提交。所以 `POST /alphas/{id}/submit` **只作用户确认后的真提交**（`workflow_submit_alpha(confirm_submit=True)`），**不作预检 / 探针**；提交前的检查用 `submit_verdict`（模拟层 checks）、`check_correlation`（只读 `GET correlations/prod`）与 `confirm_submit=False` 预检。全链与不可逆动作块见 [`submit-chain.md`](../../Claude/skills/worldquant-submit-alpha/references/submit-chain.md)。

---

## 1. 提交层四闸（REGULAR）

| 闸 | 阈值 | 备注 |
|---|---|---|
| `LOW_SHARPE` | ≥ **1.58** | 严格不等式 |
| `LOW_FITNESS` | ≥ **1.0** | 严格不等式 |
| `LOW_2Y_SHARPE` | ≥ **1.58** | |
| `LOW_SUB_UNIVERSE_SHARPE` | 比值闸（见 §2） | |

**四者必须同时成立**。另有区域专属闸：
- `LOW_ROBUST_UNIVERSE_SHARPE`（IND，limit **1.0**）
- `CONCENTRATED_WEIGHT` ≤ 0.1
- `HIGH_TURNOVER` — ⚠ **上限区域特异**：本文旧记 0.4，**GBR/D1 实测 = 0.7**（2026-10-07，`checks.HIGH_TURNOVER limit 0.7`）。取阈值前**以本区平台返回的 limit 为准**，勿套用他区。
- `IS_LADDER_SHARPE`

### ★ 换手前置判据（SOP 标准步骤，2026-10-07 定）

> **在候选进入「候选池 / 台账 / 提交队列」之前执行，区间外一律剔除，不进池。**

```
保留区间：  TO ∈ [0.03, 0.70]
  TO < 0.03  ⇒ 剔除（近乎静态：换手过低意味着持仓几乎不动，
                往往是"数据未更新/字段近似常量/伪信号"，margin 与容量都不可信）
  TO > 0.70  ⇒ 剔除（超过平台 HIGH_TURNOVER 上限，GBR）
```

**与平台闸的关系（两者都要过，本判据更严）**

| | 平台闸 | 本前置判据 |
|---|---|---|
| 下界 | `LOW_TURNOVER` ≥ **0.01** | **≥ 0.03**（更严） |
| 上界 | `HIGH_TURNOVER` ≤ **0.7**（GBR；他区可能不同） | **≤ 0.70**（对齐） |

**执行工具**：`python to_prefilter.py --wave <波次>` 或 `--alpha-id <ID>...`
（输出 KEEP / CULL(低 TO) / CULL(高 TO) / UNKNOWN 四类，并给出逐条理由）。

**为什么放在「前置」**：TO 在回测后即已知，而 prod/self 相关性昂贵且排队 ⇒
**先用零成本判据砍掉结构性不合格项，再做昂贵检查**，可显著减少无效相关性查询与台账污染。

**历史核查（2026-10-07）**：GBR ANALYST 战役全部候选 + 最近 60 条记录，**区间内 100%、零违规**
（实际分布 TO 0.047–0.23）⇒ 该判据对既有工作无回溯影响。

### 关键判据

- **提交层严格不等式**：`value == limit` 判 **FAIL**。`VkaZYdbG` 的 `IS_LADDER_SHARPE value=1.58 == limit 1.58` → 403。
- **提交层严于 IS 层**：IS 层的 WARNING 在提交层是 FAIL（09-16 三颗 IS 全 WARNING、POST 全 403）。**更正（2026-09-30）**：旧版写的「IS 层 limit 更宽」不成立——`Vk0kLMqG` 真 POST 被 403，且提交层各 check 的 limit 与 IS 层**完全一致**（`LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`、`LOW_ROBUST_UNIVERSE_RETURNS` 逐项相同；`1YZqNxM6` 是特例，不可作通用依据；GBR `IS_LADDER` 曾记 IS 层 1.88 / 提交层 1.58，属单点观察，待复核）。→ **必须在 IS 层就把所有 check（含 WARNING）压过，否则 POST 必 403；"IS 层 PASS" ≠ 能过提交层**。
- **`CONCENTRATED_WEIGHT` 是结构性拒绝，非权重分布问题**：GBR starmine 族里 `ts_decay_linear` 平滑、连外层全市场 `rank()` 均匀化都 403；唯一过提交层的同族结构是 `trade_when` 门控。

---

## 2. ★ SUB 是比值闸，不是绝对闸

`LOW_SUB_UNIVERSE_SHARPE` 的 limit = **0.75 × sqrt(子宇宙规模 / 本 alpha 宇宙规模) × 本 alpha sharpe**（公式见 `brain-how-to-pass-alpha-test` §5）。**系数随宇宙变化，不是常数**：KOR（TOP600）实测 ≈ **0.571**（下表三处独立一致）；USA（TOP3000 → 子集 TOP1000）= 0.75×sqrt(1000/3000) = **0.433**（2026-10-01 USA 两处直查：limit/S = 0.4335 / 0.4333）；SuperAlpha ≈ 0.431；DEU profile 记 ≈ 0.47。**系数一律用 `get_alpha_details` 里本 alpha 的 `LOW_SUB_UNIVERSE_SHARPE` 的 limit / sharpe 当场算**，不要套用别区的数。下表是 KOR 的实测：

| sharpe | SUB limit | 比值 |
|---|---|---|
| 1.80 | 1.03 | 0.572 |
| 1.96 | 1.12 | 0.571 |
| 1.55 | 0.89 | 0.574 |

**⇒ 把 S 压到刚过 1.58 会同步抬高 SUB 的绝对要求，「S 越高越好」是错的。**
正确目标：`SUB/S ≥ 本区系数（KOR ≈ 0.571、USA ≈ 0.433）∧ 2Y ≥ 1.58 ∧ S ≥ 1.58 ∧ F ≥ 1.0` **同时**成立。
**低分区实测值不可外推为「墙」**：limit 随 S 线性增长，S≈0.6 时 SUB 实测 0.30 只是 `S×0.47`，S≳1.7 时该闸自动过（DEU 6 颗 ACTIVE 全部 PASS 该闸，原「DEU sub_universe 结构性墙」是伪墙，见 `regions/DEU.md`）。

**破比值闸的合规旋钮（实测有效）**：
- 分组轴换到 **`market`**（决定性，给比值）或 **`exchange`**（给 2Y）
  ⚠ **2026-10-06 DEU 实测不迁移**：在 `agent_factor_signals` 族（字段 `eps_revision_magnitude`）上，加 `market` 或把 `subindustry` 换成 `market`
  ⇒ **S 1.37→0.56~0.60、sub 0.64→≤0.21（反噬）**。原结论来自 EUR/KOR ⇒ **逐区逐族实测，勿照搬**。
- `signed_power` 压尾（⚠ 压尾前先看持仓对称性：会造成多空不对称而触发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`；优先试等价的 `quantile`，见 `brain-how-to-pass-alpha-test` §5b）
- 长窗 `ts_rank` / `ts_decay_linear` 平滑
- ⚠ **分组轴不是 SUB 闸的通用旋钮**：EUR 有效，KOR other466 六种轴向全灭——逐区实测

---

## 3. 配额

| 项 | 规则 |
|---|---|
| REGULAR | **4 / ET 日** |
| SUPER | **1 / ET 日** |
| PPA | **独立 1 / ET 日** |
| 重置 | 00:00 ET（= GMT+8 次日 12:00，**夏令时**；冬令时为 13:00——2026-11-01 起，以 `tools/quota_status.py` 输出为准） |

**判据**：
- **403 零成本、不扣配额**：被拒的 POST 会回带全量 checks（含真实 PROD/SELF），是唯一能看到提交层真值的地方——但**通过就是真提交**，所以这份信息只能在「用户已确认要提交」的那一次 POST 里顺带拿到，**不能靠 POST 去试**（见文首政策提示）。
- **并行会话共享同一账号配额**（09-21 误判"4 空位"实际只剩 2；09-25 被并会话打满致本会话 0 提交）。
- **403 里 `PENDING` ≠ FAIL**：403 唯一 FAIL 项是 `REGULAR_SUBMISSION value=4 limit=4`（配额用尽）；`SELF/PROD_CORRELATION` 显示 PENDING 不挡提交。
- **配额真值只能查 `tools/quota_status.py`**：`GET /users/self/activities/submissions` **没有 today 字段**（只返回 yesterday/current/previous/ytd，且 `ytd.end` 停在昨天），且计数是 **REGULAR+SUPER 合计**。
- 201 受理后**异步失败要扣额**（`N1708Mr8`）；403 与 IS 失败不扣。

---

## 4. 相关性（prod / self）

### 取数

| 项 | 方法 |
|---|---|
| **prod** | 直轮询 `GET /alphas/{id}/correlations/prod`（15s 长窗口，恒 200，**空体 = 平台在算**），`max` 即判定值；耗时 45s ~ 12min |
| **self（本地）** | 累计 PnL **必须 diff 成日收益**再 Pearson，窗口 **4×252**（误差 < 0.001） |
| 列表 self-corr | 在 `records[i][5]` |
| **缓存（2026-10-06 改）** | 已决 prod 落 SQLite 权威表 `data/wqb.db::alpha_corr_cache`，**保鲜期 48h**，过期自动回源；**不再依赖 Redis**（旧版 Redis 未启动 ⇒ 缓存静默失效，且 TTL 7 天与 48h 纪律冲突）。命中响应带 `from_cache: true` |

**prod 端点机制**：只返回"已算好"的值，**请求不触发计算**；单账号单并发 + 异步排队 → **高频 refresh 是反效果，等的收益为零**。
→ prod 取数走只读 `GET correlations/prod`（`check_correlation`）；被拒的 POST 也会回带真实 prod 值，但**不能为此去 POST**（通过即真提交）。

### 阈值与判定

- 平台**名义阈值 0.7**，但 **SUPER 判定只看 `result` 不看 `value`**：0.8094 / 0.8571 判 PASS，0.8938 / 0.9729 判 FAIL → 实际分界在 **0.86 ~ 0.89**。
- **我方铁律更严**：prod ≥ 0.7 **一律拒提**（`super_build.py` 已强制 probe + fail-closed，唯一豁免 `--allow-prod-above-07`）。REGULAR 同口径。
- **`PROD > 0.7` 未必 FAIL**：`N1QMJ10q` 0.7225 判 WARNING、`gJjnXv8g` 0.7864 成功 ACTIVE；同批 `omqxJmO6` 0.7255 却 FAIL → **判定非纯阈值，以平台实测值为准**（`check_correlation` 读 prod；`submit_verdict` 看模拟层）。

### 两个必知的失效场景

1. **prod 值会腐烂，必须当日实测**：实测 0.6678→0.981、同族顶高 0.5836→0.9805、`le8Y68K2` 0.6929→0.9932、`3qX6wLJQ` 库内 0.5171→实测 0.9895。
   → 筛查产出的是**排序队列**而非终局清单，提交当日须 `refresh=True` 复测。
2. **本地 SELF 两个失效场景**：① 系统性低估（`N1QMJ10q` 本地 0.3972 → 平台 0.5463；`6XrJ5OvE` 本地 0.6732 vs 平台 prod 0.996）；② 对"新提交孪生体"**结构性假阴性**（`vRkAO9Xd` 本地 0.229 vs 平台 0.8392，根因是 OS PnL 池不含刚提交 alpha）。
   → **同族候选不要用本地 SELF 判活**，改用 403 视图逐颗实测。

- **SELF 极低 ≠ PROD 低**：`A1loLl2e` SELF 0.034 但 PROD 0.7671。两闸衡量对象不同（SELF = 与账号既有 ACTIVE 相关；PROD = 与全平台生产池相关）。
- **小区 PROD ≈ SELF**：IND 两值几乎相等（0.7619/0.7622、0.7558/0.7557）→ 压一个必然带动另一个。USA 则是 **PROD 独立卡死 0.86**（SELF 降 PROD 不动）。

---

## 5. 提交形态与预检

### submit_alpha 四形态

| # | 形态 | 处置 |
|---|---|---|
| ① | 200 + IS passed | 明确通过 |
| ② | **201 async** | 4 min 未翻状态**必须补发 POST**（否则悬空滞留队列） |
| ③ | 200 空体 | 未知，**必须轮询** |
| ④ | **403** | 零成本，回带**全量 checks**（含真实 PROD/SELF）；**这是被拒时才有的结果，不能当预检用**（通过即真提交） |

**判定只认轮询 `status=ACTIVE`。**

### 关键区别

- `GET /alphas/{id}/submit` **恒返回 404 + 空体**（对已 ACTIVE 与未提交都一样）→ 处女候选恒 `UNVERIFIABLE`；**403 只可能来自 POST**。
- **`submit_verdict` 的"提交层唯一权威"名不副实**（GET 路径恒 404），但**零成本定位卡点仍可用**：它在 404 响应里给出模拟层完整 checks + Failed RA/PPA 计数 → 不必真 POST 即可定位唯一卡墙。

### 提交前必做

- **★ prod 无需本地单独复测（2026-10-08 用户裁定）**：`prod_gate` 节点在 `confirm_submit=True` 时会**自己实时拉取 prod**（拿不到即 fail-closed 拒发，这正是 `correlation_busy` 的成因）。
  ⇒ 提交前那次独立的 `check_correlation(refresh=True)` 属**冗余动作**：它与节点抢同一个**单并发**队列，反而更容易把端点挤爆。**跳过它不降低安全标准**（硬闸在节点内）。
  ⇒ 处置：**用户确认后**执行 `workflow_submit_alpha(confirm_submit=True)`（真提交、**不可逆**）；若节点报 `correlation_busy`，**间隔重试**（≥90s），**切勿改参数或降标准**。
  ⚠ 仅当需要**事先排序/取舍**多个候选（不打算立即提交）时，才需 `check_correlation(refresh=True)` 复测。
- **name + description（≥100 字，house style ~1200 字）必须预先写好并回读**——空描述会被平台**静默丢弃**（POST 返回 201 但被丢）。
- **REGULAR 用 `set_alpha_properties`，SUPER 必须裸 PATCH**（`set_alpha_properties` 对 SUPER 必 400）。
- ⚠ **`set_alpha_properties` 是全量覆盖接口不是局部更新**：曾清空 **115 颗 ACTIVE 的 name** 并覆写 description。改单个属性用**最小字段 PATCH** `{"tags":[...]}`，**改前先 dump 快照**。

---

## 6. SuperAlpha（SA）

| 项 | 规则 |
|---|---|
| 硬前置 | **ACTIVE REGULAR ≥ 10**（平台报 `At least 10 component alphas are required`，异步校验） |
| 组件不足时 | select 失败回得极快 → 放宽 self_gate 的梯度扫描成本 ≈ 0 |
| **self_gate 是首要放宽旋钮** | 0.65 三连废；放宽到 **0.70 十颗全过**；0.85/0.95 产物与 0.70 完全一致 → **0.70 已是全收，再放宽无收益** |

**成功配方模板**：
```
<REGION>/<主universe>/d1/trunc0.08/maxTrade OFF + dec10 + nu=SUBINDUSTRY
selection: (1+0*(prod>0))*(1-prod)*(self<0.6)*(to>0.01)*(to<0.6)
combo:     线性 1-maxCorr
```

**MEA 的 SUPER 通道已关闭**（`region=MEA type=SUPER` → 400 `Region MEA is not available`）。

---

## 7. 点塔（Pyramid）

- **点亮定义 = 该塔下当前自然季度提交 ≥ 3**。每个自然季度首日计数清零（2026-10-01 实证：GLB 的 10 颗 ACTIVE 全是 Q3 提交，Q4 一颗不算）；`get_pyramid_alphas` 缺省返回当前季度，查上一季须显式传 `start_date` / `end_date`。旧版写的「90 天滚动窗口」没有代码实现，已更正。
- **唯一权威数据源 = 平台 `get_pyramid_alphas`**（按季度返回 region/delay/category 计数）。
- ⚠ **本地 `alphas` 表不能做塔级统计**（两次踩坑）：
  - 不可用 `datasets.category` 推塔归属——本地 KOR 47% ACTIVE 的 `category=None`，且塔归属来自平台 pyramid 匹配，与数据集 category **不等价**。
  - 不可用 `date_submitted` 判提交——该字段全库仅 **2.7%** 非空。
- **塔归属由表达式字段的 category 决定**，不是数据集名也不是数据集 category：`WjPPjVQd` 主信号是 shortinterest55 却挂 HKG/D1/PV（因表达式含 `volume`/`adv20`/`vwap`）。
- **Cluster Alpha 的 `pyramids = null`，不参与点塔**（徽章在 `classifications`，数值在顶层 `is.checks`）。
- **MEA 不在金字塔体系内**（212 格中 MEA 格数 = 0），提交不计点亮也无 multiplier。
- **已点亮塔不再优先提交 REGULAR**，其候选最多作 SA 组腿；优先提交归属**未点亮塔**的候选。

---

## 8. universe / 中性化合法档位

| 区域 | 合法 universe | 备注 |
|---|---|---|
| **IND** | **仅 `TOP500`** | 无档可换 |
| KOR | `TOP600` | CLUSTER_TEST limit = 1.0 |
| DEU | **仅 `TOP500`** | ⚠ **2026-10-06 实测更正**：`TOP300` 报 `Universe TOP300 is not available for instrument type EQUITY and region DEU` ⇒ **原记载「TOP500 / TOP300」有误**，DEU 无第二档位可换 |
| USA | `TOP500` / `TOP1000` / `TOP2000` / `TOP3000` | 降 PROD 首选 **TOP1000** |
| EUR | 6 档 | |
| GLB | `MINVOL1M` | |

- ⚠ **`TOP800` / `TOP1500` / `TOP2500` / `TOP5000` 均非法**（平台 400）。合法档实测：`TOP500`/`TOP1000`/`TOP2000`/`TOP3000`。
- ⚠ **JPN 不支持 `industry` / `sector` / `subindustry` 分组**（闸 2b 硬拒绝），cluster 变体线在 JPN 必被拒。
- **缩小 universe 可降 PROD 但非单调，必须逐档实测**（USA `N1QMJ10q`）：TOP3000 0.7225 → **TOP1000 0.6149 ✅** → TOP500 0.5422（FAIL，IS 被摧毁）→ TOP2000 反升 **1.0**。

---

## 9. 幽灵算子 / 幽灵字段

### 幽灵算子（10 个，取模板骨架前必查 ghost advisory）

```
group_normalize, sigmoid, ts_decay_exp_window, ts_entropy, ts_max,
ts_median, ts_min, ts_min_max_cps, ts_percentage, ts_skewness
```
外加 **`negate`**（合法替代 `multiply(-1, X)`）。
→ 用了整批 ERROR/CANCELLED。**权威以本仓 `operators_verified.json`(103) + KB advisory 为准，论坛口径不可信**。

### 幽灵字段

- **幽灵字段 alpha 在提交层 `COMPILE_ERROR`，根本不可提交**（旧认知"可提交但不可复现"是错的）：
  `COMPILE_ERROR: Attempted to use unknown variable "change_6m_rating_revision"`。
- ⚠ **不可用 DB `fields` 表判定字段存活**：幽灵字段在 `create_multi_simulation(validate_fields=true)` 报 unknown 并整批取消，但 fields 表仍标有效。
  → **库存盘点必须以 `validate_fields` 或实跑探针验字段**。

---

## 10. 其他平台硬约束

- **`color` 是硬枚举仅 5 值**：`GREEN` / `BLUE` / `RED` / `YELLOW` / `PURPLE`（ORANGE/TEAL/GRAY 一律 400 `"X" is not a valid choice.`）。
- `tags` 与 `name` 零约束（tags 100 字符/30 个、name 256 字符均接受）。
- **平台可控属性只有**：name / color / tags / hidden / favorite / regular.description。
- **已 ACTIVE 的 alpha 不可重复提交**（`status=ACTIVE` 且 `GET /submit` 返回 404）。
- **DECOMMISSIONED 由 WQ 单方面裁定，顾问无退役入口**：`retire/decommission/deactivate/...` 全 404；`PATCH {"status":"DECOMMISSIONED"}` → 200 但**服务端静默忽略**。`hidden` ≠ 退役（仍 ACTIVE、仍在生产 book 跑）。→ 只能打 `RETIRE_<YYYYMMDD>` 标签。
- **`WeightFactor` 唯一入口 = `GET /users/self/consultant`**（含 weightFactor/valueFactor/meanProdCorrelation/meanSelfCorrelation）。
- **平台列表接口每个 status 过滤各限 1000 条**（UNSUBMITTED 拉到 1100 即 400），超出只能逐条 GET。
- **PPA 决定性闸 = `MATCHES_THEMES`**（WARNING = 未命中即不能走 PPA，重试无效，只随主题轮换翻转）。`PURE_POWER_POOL_THEME` 命中条件是"区域组"不是 dataset category。
- **`CLUSTER_TEST` 门槛**：默认 ≥ 1.58；**KOR / JPS / TWN / HKG / IND / GBR / DEU ≥ 1.0**。判定用 check 自带 `limit` 而非按区域名硬编码。
- **OS 数据可得性**：**只有 USA 有 `os.sharpe`**（其余 9 区 73 颗全 null）。OS 全量指标只在详情 `GET /alphas/{id}` 的 `os` 块，列表接口只带 `osISSharpeRatio`。
