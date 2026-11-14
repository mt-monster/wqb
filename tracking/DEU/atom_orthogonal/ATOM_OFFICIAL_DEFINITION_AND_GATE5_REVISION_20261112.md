# ★官方 ATOM 定义 + 闸5 同源豁免修订（2026-11-12）

> 起因：用户指出「如果是同一数据集的，是不是就可以不禁」，并要求查官方 ATOM 定义。
> 结论：**用户判断成立**；我此前「乘法是唯一合规写法」的表述把内部纪律说成了平台规则，已更正。

## 一、官方 ATOM 定义（权威来源）

**来源 1**：论坛帖 `32032672214807`「【新人科普】BRAIN 平台上的四类 Alpha（RA, ATOM, PPAC, SA）」（**201 赞**）
**来源 2**：平台文档 `platform.worldquantbrain.com/learn/documentation/consultant-information/single-dataset-alphas`

原文要点：

> - **所有使用的数据字段必须来自同一个数据集**；
> - 常见的 group 字段如 `industry`、`country` 等是**豁免字段**，不计入数据集数量限制；
> - 提交后页面上会出现 "Single Dataset Alpha" 标签。
> - 特别检测机制：**放松了 IS Ladder Testing 要求**；仅要求通过最近两年的 **2-Year Sharpe** 检测。
> - 设计逻辑：同一数据集下字段类型更统一，**降低混信号风险**，更利于 OS 稳定性。

### 由此得出的三条事实

| 问题 | 答案 |
|---|---|
| ATOM 是否约束组合结构（add / multiply）？ | **不约束**。官方只约束「字段同源」 |
| 同数据集两腿 `add` 会破坏 ATOM 吗？ | **不会**。仍是 Single Dataset Alpha |
| 平台会因 `add` 拒收吗？ | **不会**。RA 只限 64 算子/字段 |

**附加价值（官方明说）**：ATOM 放松 IS Ladder、只看 2Y Sharpe。
这解释了本战役反复出现的「2Y 远大于 S」现象（esm 0.87/2.23、institutions 0.44/1.66）——
**2Y 是本区的天然达标轴，S 才是难轴**，与 ATOM 的检测结构直接对应。

## 二、闸5 的真实身份

闸5 是**我方内部派发前拦截器**，位于 `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py`，
不是 WorldQuant 的提交规则。原文依据：

| 位置 | 原文 |
|---|---|
| `INDEX.md:211` | 闸5 毒模式 block 常开｜平台级 platform_constraints 正则 + 结构判定 |
| `CLAUDE.md:24` | 禁止混信号调参防止过拟合，**尤其要警惕 add(A,B) 模式** |
| `alpha_mining_methodology_20260907.md:355-365` | 「三条里只能出一条。这就是禁止 add(A,B) 混信号调参的**量化理由**」 |
| `platform_constraints.json` `_weighted_mix_note` | 「**任何对用户定案纪律的放宽必须先经用户明确确认**」 |

⇒ 禁 `add` 的**目的**是防「权重自由度 → 反复调参 → IS 过拟合」，与 ATOM 无关。
⇒ 同源场景下该风险**并未消失**（同源两腿高度相关，权重怎么调都能凑出好看的数字），
   但**混信号风险确实降低**（官方口径），所以正解是 **降级为 warn + 强制登记权重来源**，而非直接放行。

## 三、代码修订（已实施并验证）

文件：`Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py`

| 改动 | 位置 | 内容 |
|---|---|---|
| 新增 `_legs_all_same_dataset()` | L810 | 判定两腿字段是否全属同一数据集；**无映射时 fail-closed 返回 False** |
| 新增 `_find_equal_weight_leg_add()` | L839 | 扫描命中位置并标注 `same_dataset` |
| 改 `_detect_equal_weight_leg_add()` | L862 | 只对**非同源**命中返回 True（同源不再 block） |
| 改 `check_one()` 调用点 | ~L514 | 同源命中追加 `[SAME_DATASET_LEG_ADD]` **warning** 而非 `[POISON]` |

### 验证结果

| 用例 | 结果 |
|---|---|
| `add(rank(aaa1), rank(bbb1))`，两字段同属 `inst6` | `detect=False`，记 warning ✅ 豁免 |
| 同上，`aaa1=inst6` / `bbb1=pv20` | `detect=True` ✅ 仍 block |
| 同上，无字段→数据集映射 | `detect=True` ✅ fail-closed |
| `pytest tests/unit/04_gates/` | **299 passed** ✅ 既有行为零回归 |

## 四、豁免的连带条件（不是无条件放行）

同源 `add` 派发前**必须**登记：

1. **权重来源**：等权，还是由经济含义决定的配比？禁止「试多个权重挑最好看的一个」。
2. **两腿是否同机制**：若相关 >0.9（如 esm 7 字段之间 0.86-0.996），相加 = 加权平均同一信号，**不产生新信息**；
   只有相关 <0.7 的**同源不同矩**（如语调水平 vs 语调变化 0.7191）才值得测。
3. **优先 `multiply` / `trade_when`**：这两种写法不引入权重自由度，天然免疫过拟合通道。

## 五、对既有档案的更正

- 更正：`WAVE_BE105_EARNINGS_SAMETOWER_ATOM_20261112.md` 第三节「双信号组合一律走 multiply」的表述，
  应改为「双**不同源**信号腿走 multiply；**同源**腿可用 add，但须登记权重来源」。
- 本文为官方口径的单一事实源，后续区域引用以本文为准。