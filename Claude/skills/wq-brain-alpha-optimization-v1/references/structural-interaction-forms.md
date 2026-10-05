# 结构交互式组合形态库（救援路线 A）

> **用途**：Mode B「卡闸 → 组合腿救援」（[SKILL.md](../SKILL.md)）的合规形态库。
> **主腿** = 本 alpha 核心字段/概念（冻结）；**辅助腿** = salvage_pool 条目（≤2 条，必取，禁凭空另造）。
> **硬边界**：禁一切加权混合 / 等权相加 / 中缀 `+` 相加——两条独立信号腿相加，无论权重写在哪一侧（<!-- lint:counterexample -->`0.5*rank(A)+0.5*rank(B)`、`add(multiply(0.5,rank(A)),multiply(0.5,rank(B)))`、`add(rank(A),rank(B))` 均属此类），
> 闸 5 的结构判定（`equal_weight_leg_add` / `infix_leg_sum` / `weighted_signal_mix_structural`，见 `platform_constraints.json` `poison_patterns`）会 block；禁权重网格扫描。本库形态全部是「单一经济信号」结构，不是拼腿。
> **算子核验**：本库出现的每个算子都在 `known_ops`（平台 `get_operators` 实测清单，`platform_constraints.json`），由 `tests/unit/07_docs_skills/test_optimization_v1_docs.py` 守；写法取自平台定义原文。
> 未入清单的投影/偏相关族（vector_proj / regression_neut / ts_partial_corr 等）**不采用**。

## 形态族总览

| 族 | 辅助腿角色 | 主要救援卡点（boost_dim） | 代表算子 |
|----|-----------|--------------------------|----------|
| F1 参照系 | 基准 / 参照物 | sharpe 弱（机制单一化） | subtract / divide / ts_delta / ts_regression |
| F2 正交化 | 待剔除的暴露方向 | **PROD/SELF 相关墙** | **vector_neut** / group_neutralize(bucket) |
| F3 条件门控 | 状态开关 / 质量门 | 2Y 弱、sharpe 弱、TVR | if_else / trade_when / ts_count_nans |
| F4 分组重组 | 分组轴 | CW / sub_universe / 集中度 | group_rank / group_zscore / group_scale / group_cartesian_product |
| F5 协同背离 | 协动对象 | sharpe 弱（新机制维度） | ts_corr / ts_covariance / kth_element |
| F6 调节稳健 | （作用于 F1–F5 成品） | TVR 出界 / 尾部风险 | hump / ts_target_tvr_hump / tail / winsorize |

## 合规的可检判据（取代「成品须能用一句话说清单一经济信号」）

「一句话说得清」不可检，也拦不住换汤不换药的拼腿。改用**辅助腿如何进入表达式**这一可检特征：辅助腿只能以下列五种方式之一入场，且**不得作为被加 / 被乘的一项进入表达式的取值**。

| 入场方式 | 长什么样（辅 = 辅助腿字段） | 对应形态族 | 机检 |
|---|---|---|---|
| ① 条件 | 辅只出现在 `if_else` / `trade_when` 的**条件参数**里 | F3 | 闸 5 不误伤（条件参数不是信号腿） |
| ② 分组轴 | 辅只出现在 `bucket(...)` → `group_*` 的**分组参数**里 | F4 | 同上 |
| ③ 残差化 | `vector_neut(主, 辅)` / `ts_regression(主, 辅, W)` 残差 / `group_neutralize(主, bucket(辅))` | F2 | 同上 |
| ④ 协动对象 | 辅只经关系统计量进入：`ts_corr` / `ts_covariance`（取的是两序列的**关系**，不是水平） | F5 | 同上 |
| ⑤ 同源价差 | `subtract(rank(主), rank(辅))` 且**同时满足**：两腿派生自同一组字段（同一数据集 / 同一经济量的不同口径）；差值有自洽的一句话经济含义；外层只叠单信号几何（`group_rank` / `ts_rank` / `ts_decay_linear` …） | F1 | 闸 5 `spread_cross_dataset`（多数据集 mix 批内判定）；同源与否由 `platform_constraints.json` `spread_signal_ruling`（用户 2026-09-28 裁定）定义 |
| ⑤b **跨集价差** | `subtract(rank(主), rank(辅))` 且两腿**来自不同数据集**、最好**更新节奏不同**（日频情绪 vs 季频财报、模型输出 vs 双周融券）。差值须有**方向性经济解释**（背离 / 对冲 / 预期-约束缺口） | F1' | **2026-10-01 用户定案：合规且鼓励**（属 §7.7.2 ⑤ 换信号概念，两腿独立 → self-corr 低）。闸 5 `spread_cross_dataset` **要求显式声明**该集对的经济含义：声明后放行，未声明则阻断。声明位置 = 区域 `reference/*_generation_constraints.json` 的 `declared_cross_spreads.pairs`，或 CLI `--declared-cross-spreads` |

**与 RA 的对应**（RA [`step7-diagnose.md`](../../wq-brain-ra-pipeline/references/step7-diagnose.md) §7.7 是「允许形态」的唯一清单，本页是它的细化）：条件 = §7.7.3 (a) / §7.7.2 ④；分组轴 = (b)；残差化 = (c)；同源价差 = §7.7.2 ②；协动对象 = §7.7.2 ⑦。

推论：**跨数据集的辅助腿可走 ①②③④ 与 ⑤b（跨集价差，须声明经济含义）**（F2 对 PROD / SELF 墙最有效的原因见下）；`add(...)` / 中缀 `+` / 系数乘法不在此表内，一律违规。

## F1 参照系族（辅助腿当基准）—— 同源用 ⑤，跨集用 ⑤b

经济含义：主信号相对辅助腿的**强弱/比率/关系变化**，是单一价差叙事，不是两信号平均。

**两种适用前提**：
- **同源**（同一数据集，或同一经济量的不同口径）→ 走 ⑤，`spread_signal_ruling` 管；
- **跨集**（不同数据集、最好不同更新节奏）→ 走 **⑤b**，**合规且鼓励**（2026-10-01 用户定案），但必须在 `declared_cross_spreads` 声明该集对的**方向性经济解释**，否则闸 5 `spread_cross_dataset` 阻断。
  `divide` 跨集虽无机检，按同一标准自律（同样要有经济解释）。

| 形态 | 经济模板 | 实例（`主`/`辅`=字段） |
|------|---------|----------------------|
| `subtract(rank(主), rank(辅))` | 同类相对强弱（自家修正 vs 同业修正） | `rank(ts_mean({主}, 22)) - rank(ts_mean({辅}, 22))` |
| `divide(主, 辅 + 1e-4)` | 效率/强度比（流量÷存量、修正÷分歧） | `rank(divide({主}, {辅} + 1e-4))` |
| `ts_delta(subtract(rank(主), rank(辅)), W)` | 价差的时序变化（关系改善/恶化） | `ts_delta(rank({主}) - rank({辅}), 66)` |
| `ts_regression(主, 辅, W)` | 联动弹性（主对辅的敏感度 beta） | `rank(ts_regression({主}, {辅}, 66))` |

约束：价差/比率必须能写成一句话（"A 相对 B 贵/强/改善"）。同源时两腿须同数据集；跨集时须声明方向性经济解释（背离 / 对冲 / 预期-约束缺口）。**写不出经济解释 → 违规**（无论同源还是跨集），换族（F2–F5）。

## F2 正交化族（辅助腿当"待剔除的暴露"）——PROD/SELF 相关墙首选

经济含义：把主信号中**与辅助腿共线的成分剔掉**，留下主信号自己的残差 alpha（去公共暴露）。

| 形态 | 平台语义（catalog 原文） | 实例 |
|------|------------------------|------|
| `vector_neut(主变换, 辅变换)` | "removes the component of vector a in the direction of vector b"（a−(a·b)b） | `vector_neut(rank({主}), rank({辅}))` |
| `group_neutralize(主, bucket(辅))` | 以辅助腿分位分组的中心化（粗粒度正交） | `group_neutralize({主}, bucket(rank({辅}), range="0,1,0.1"))` |
| `ts_regression(主, 辅, W, rettype=...)` | 时序回归残差/斜率（rettype 枚举须 preflight 实测确认） | `-ts_regression({主}, {辅}, 66, rettype=0)` |
| `vector_neut(主, 辅)` + 规范包装 | 正交化后接几何（rank / ts_zscore / ts_rank） | `rank(vector_neut({主}, {辅}))` |

用法要点：
- **跨数据集辅助腿**（`exclude_dataset=<主数据集>` 取到的腿）效果最好——正交掉的是一个全新的暴露方向。
- 成品须重新走 selfcorrQuick → `check_correlation` 验证；PROD 读数按 RA 决策表 **D0-P** 处置（本族属其「唯一例外」路径：主腿已 `eligible` 且有 salvage 辅助腿）。
- 若正交后 sharpe 塌方 → 说明主信号原本就是辅助腿的暴露，属"risk_neut≈0"型伪信号（参见 ra-pipeline 步 7 硬规则），放弃而非硬救。

## F3 条件门控族（辅助腿当开关）

经济含义：**只在辅助腿指示的状态里暴露主信号**——单一信号 + 状态依赖，不改变主信号取值本身。

| 形态 | 经济模板 | 实例 |
|------|---------|------|
| `if_else(辅条件, 主变换, 主基准)` | 分歧高/事件期时切换增强版 | `if_else(greater(rank({辅}), 0.7), rank(ts_delta({主}, 22)), rank({主}))` |
| `trade_when(辅条件, 主, -1)` | 高信念状态才交易（-1=否则保持持仓，顺带降换手） | `trade_when(greater(rank({辅}), 0.6), rank({主}), -1)` |
| `trade_when(质量门, 主, NaN)` | 辅助腿数据可用时才持仓（覆盖率门） | `trade_when(less(ts_count_nans({辅}, 22), 5), rank({主}), NaN)` |
| `if_else(greater(ts_delta(辅, W), 0), 主, reverse(主))` | 方向状态切换（辅改善 ⟺ 主信号有效方向） | `if_else(greater(ts_delta({辅}, 66), 0), rank({主}), -rank({主}))` |

条件构造原料（均可组合）：`greater/less(rank(辅), q)`、`greater(ts_delta(辅, W), 0)`、`bucket` 边界、`ts_count_nans`。
用法要点：门控会缩暴露窗口 → 顺带改善 TVR / CW；但**条件必须有先验依据**（辅的经济状态语义），不能为凑指标乱开门。

## F4 分组重组族（辅助腿当分组轴）

经济含义：**在辅助腿定义的组内比较主信号**——横截面结构重组，CW/sub_universe 墙的针对性形态。

| 形态 | 经济模板 | 实例 |
|------|---------|------|
| `group_rank(主, bucket(辅))` | 辅助维度分位组内排名（如按流动性/规模 10 组） | `group_rank({主}, bucket(rank({辅}), range="0,1,0.1"))` |
| `group_zscore(主, bucket(辅))` | 组内标准化（同分位可比） | `group_zscore({主}, bucket(rank({辅}), range="0,1,0.1"))` |
| `group_scale(主, bucket(辅))` | 组内 0–1 缩放（跨组可比） | `group_scale({主}, bucket(rank({辅}), buckets="0.3,0.7"))` |
| `group_cartesian_product(bucket(辅), <常规轴>)` | 双维分组（辅助腿 × industry/subindustry） | `group_rank({主}, group_cartesian_product(bucket(rank({辅}), range="0,1,0.1"), densify(subindustry)))` |
| `group_std_dev(主, bucket(辅))` | 组内离散度（主信号的组结构强度） | `group_std_dev({主}, bucket(rank({辅}), range="0,1,0.1"))` |

用法要点：分组轴要换掉"已过载的轴"（主信号已中性化的轴不要再用）；`bucket(rank(x), range=...)` 的参数名与引号必须写对（参见 gates 语法规则）。

## F5 协同背离族（辅助腿当协动对象）

经济含义：**两序列的关系本身**作为信号（协同度、背离出现、尾部协同）——引入全新机制维度。

| 形态 | 经济模板 | 实例 |
|------|---------|------|
| `ts_corr(rank(主), rank(辅), W)` | 协同度（预期-现实、量-价、资金-基本面） | `ts_corr(rank({主}), rank({辅}), 66)` |
| `ts_delta(ts_corr(rank(主), rank(辅), W), W2)` | 协同度的变化（背离出现/修复） | `ts_delta(ts_corr(rank({主}), rank({辅}), 22), 22)` |
| `ts_covariance(主, 辅, W)` | 协动（含强度信息） | `rank(ts_covariance({主}, {辅}, 66))` |
| `kth_element(辅, W, k)` 作参照 | 用辅的 K 分位（稳健分位）构造参照系 | `rank(subtract({主}, kth_element({辅}, 66, 1)))` |

## F6 调节稳健族（对 F1–F5 成品做后处理）

| 形态 | 作用 | 参数要点 |
|------|------|---------|
| `hump(信号, hump=0.01)` | 抑制微小变动 → 降换手（TVR 墙） | **必须命名参数**（`hump(x, hump=k)`；RA 决策表 D6 定：`hump` 仍受支持）；hump 越小越平滑；先验证 sharpe 不塌。`wq-brain-ppa-mining` 里「hump 对组合信号有破坏性」是 PPA 场景经验、此处未复核——作用于 F1–F5 成品时先小样本验证 |
| `ts_target_tvr_hump(信号, target_tvr=0.15)` | 目标换手率自适应平滑（genius 级） | 直接对准目标 TVR 调参 |
| `ts_target_tvr_decay(信号, target_tvr=0.15)` | 同上 decay 版 | 二选一，不与 hump 叠用 |
| `tail(信号, lower=q, upper=1-q, newval=0.5)` | 掐中段/两端（视分布） | 参数为常数；与原分布配合 |
| `winsorize(信号, std=4)` / `ts_decay_linear(信号, W)` | 尾部稳健 / 线性衰减平滑 | 常规稳健化 |

> ⚠ **F6 目标换手族的适用边界（2026-10-02 实证，GBR analyst47，13 次回测）**
> **判据 = 平滑时 2Y sharpe 是否同步崩塌。** 若同步崩塌（analyst47：2Y 1.70 → 0.61 随 target_tvr 下调），说明被抹掉的是**真实预测力而非噪声**，则 `ts_target_tvr_*` 必然劣于不加：实测 F 随 `target_tvr` **单调递增**，最优仍是「不套算子」（F 0.97 vs 套后最优 0.87、hump 仅 0.63）。
> 两条硬性质：① 算子**只会加平滑、无法放松**——`target_tvr` 即使高于自然换手（0.19 > 0.1896）仍被压低到 0.1685；② **`decay` 设置与算子叠加 = 双重平滑**，同 target 下 decay=2 全劣于 decay=0。
> 反例边界：该族在「事件密度型/换手天然偏高且信息衰减慢」的信号（论坛 179/91/34 赞案例）上有效；对**长窗分位型慢信号**（本例 `ts_quantile(x,504)`）无效。套用前先跑「加/不加」两格对照。

## 卡点 → 形态映射（救援取形顺序）

| 卡点 / boost_dim | 第一优先 | 备选 |
|------------------|---------|------|
| PROD/SELF 相关 ≥0.7（`exclude_dataset`） | **F2 `vector_neut`** | F2 `group_neutralize(bucket)` |
| 2Y 弱（`boost_2y`） | F3 条件门控（近期状态） | F5 `ts_delta(ts_corr)` |
| CW / sub_universe（`boost_cw`） | F4 `group_rank/zscore(bucket)` | F3 门控（缩窗口） |
| TVR 出界（`boost_tvr`） | F6 `ts_target_tvr_hump` | F6 `hump` / F3 `trade_when(-1)` |
| sharpe/fitness 弱（`boost_sharpe`） | F5 协同 | F1 参照系 / F3 门控 |

组合规则：主腿冻结 + 辅助腿 ≤2（宜跨数据集）；成品可再叠一处 F6 调节（至多一层）。

## 反例与灰区（自检）

- ❌ 加权混合 / 等权相加 / 中缀 `+`：<!-- lint:counterexample -->`0.5*rank(A)+0.5*rank(B)`、`add(multiply(0.5,...),multiply(0.5,...))`、`add(rank(A),rank(B))` —— 闸 5 block，勿尝试。
- ❌ 权重网格扫描（0.3/0.7 → 0.4/0.6）。
- ⚠️ `multiply(主, 辅)` 双原始信号相乘 = 混信号灰区 → 用 `ts_corr` 或 `if_else` 表达同一意图
  （项目先例：concept-first 指引 "ts_corr(surprise, sentiment) instead of multiply(surprise, sentiment)"）。
- ⚠️ `subtract(rank(主), rank(辅))` 无经济含义的拼凑（伪价差），或两腿跨数据集（闸 5 `spread_cross_dataset` block）。
- ⚠️ 同一辅助腿反复充当多形态输入 → 伪多样（多样性的载体应是机制，不是包装）。

**入场前自检 5 问**（每条都可检）：① 辅助腿的入场方式属于上表①–⑤之一？② 辅助腿**没有**作为被加 / 被乘的项进入表达式取值？③ 无系数乘法叠加、无权重网格？④ 辅助腿 ≤ 2；跨数据集时没有用 F1？⑤ 成品已过 `wave_gate --batch-type repair`，且 selfcorr / prod 预检已做？
