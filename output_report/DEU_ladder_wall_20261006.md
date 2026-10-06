# DEU 战役结论（86 波 / 2026-10-06）—— 只差 1 个闸（含算子面全量补扫）

## 一、头条（86 波，含 103 个平台算子的全量补扫）

在 **DEU / D1 / TOP500 / decay 8 / SUBINDUSTRY / truncation 0.08** 下，跑出 **1 颗除 ladder 外全闸通过的 alpha**：

> **`j28rN6YZ`** — S **1.69** ✅｜F **1.50** ✅｜TO 0.116 ✅｜sub **1.13** ✅｜CW ✅｜CLUSTER ✅｜MATCHES_PYRAMID ✅
> **prod 0.5807 ✅｜self 0.5498 ✅**（平台实测）｜双 ×1.8 塔（MODEL + OTHER）
> **唯一阻断：`IS_LADDER_SHARPE` = 1.58，limit = 1.58 → 平台严格不等式判 FAIL**（需 **≥1.59**）

`submit_verdict` 权威判定 = **BLOCKED / `FAILED_COUNT_RA:IS_LADDER_SHARPE`**。缺口 ≈ 0.005（真值需 ≥1.585）。

```
group_neutralize(group_neutralize(group_neutralize(
    quantile(add(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 8),
                 ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 252))),
    oth455_relation_n2v_p10_q50_w1_pca_fact1_cluster_20),
    oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20),
  subindustry)
```

## 二、同族候选（均 UNSUBMITTED，全部只差 ladder）

| # | alpha | S | F | TO | **2Y** | sub | 差异 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | **j28rN6YZ** | 1.69 | 1.50 | 0.116 | **1.58** | 1.13 | 长腿 252（推荐代表） |
| 2 | **1YZz1v2K** | **1.76** | **1.60** | 0.113 | 1.56 | 1.16 | 长腿 189（S/F 最高） |
| 3 | P0gOr0YK | 1.69 | 1.50 | 0.116 | **1.58** | 1.13 | +第 4 层 `market` |
| 4 | QPK9qe6G | 1.69 | 1.50 | 0.116 | **1.58** | 1.13 | +第 5 层 `sector` |
| 5 | GrOeEGmQ | 1.69 | 1.50 | 0.116 | **1.58** | 1.13 | `ts_backfill 1260` |
| 6 | xAbdMXgw | 1.69 | 1.50 | 0.116 | 1.57 | 1.13 | 仅双轴（prod/self 亦实测 0.58/0.55 ✅） |

⇒ **6 颗同骨架候选**，按同族铁律**只能取 1 颗**；全部卡在同一处。

## 三、本战役的破闸配方（按实际增益排序，均为单信号合规形态）

| 杠杆 | 2Y 增益 | 说明 |
|---|---|---|
| **图聚类分组轴**（`oth455_*` 1500 个 GROUP 键） | **+0.36** | 最大杠杆；`cluster_20` > `10` > `5`；`relation` 关系最优 |
| **platform `decay` 4 → 8** | **+0.10** | 单峰，16 崩塌；6~9 同平台 |
| **双窗平滑** `add(ts_mean(x,8), ts_mean(x,252))` | +0.02（+ S +0.09/F +0.36） | **唯一零代价杠杆**；`quantile` 必须在 add 之外 |
| **第三层"行业族"轴**（`subindustry`/`market`/`sector`） | +0.01 | 必须**与图聚类不同族**才有效；叠同族反而 −0.11 |
| `quantile` 替 `signed_power` | ~0 | 但 S +0.10 |
| `signed_power` 指数 0.3→0.2 | ~0 | 但 S +0.03 |

## 四、已证伪（勿重走）

- ❌ **中性化换 `REVERSION_AND_MOMENTUM`**：整族摧毁（S 0.77~0.97、2Y 转负）
- ❌ **`trade_when(volume>adv20, …)` 流动性门**：HKG 的 ladder 武器（+0.52）**在 DEU starmine 族为 −0.06**
- ❌ `hump` / `ts_decay_linear` / `ts_mean(双窗)` 再平滑：2Y 掉到 0.4~1.2
- ❌ `ts_quantile` / `ts_rank` / `ts_zscore` 时序归一：2Y 转负
- ❌ `zscore` / `winsorize` / 三元 `add`：2Y ≤1.3
- ❌ **换字段**：starmine 其它 9 个字段全崩（**尾号 `_4` 是唯一有信号的模型版本**）⇒ mece 族**只出 1 颗**
- ❌ `truncation`（0.04 vs 0.08 逐位相同）/ `nanHandling`（ON vs OFF 逐位相同）：零杠杆

## 五、算子面补扫（W81–W85b，用户指正后新增）

> **配套产出**：本轮把结论固化成用户级 skill **`wq-operator-playbook-by-gate`**
> （`~/.workbuddy/skills/`）—— ① 发批前**算子对账 SOP**；② **按闸开方表**（每闸给首选算子 + 已证伪清单）；
> ③ 语法/命名参规则与两个方向相反的引号坑；④ 组合范式；⑤ **实测增益库**；
> ⑥ `references/operator-syntax.md` 收录 **103 个算子的定义 + 场景诊断**（由平台目录机器生成）。

用户指出「算子尝试远远不够丰富」——属实：前 80 波只用了约 **20 / 103** 个平台算子。已按 `get_operators` 权威清单补扫：

| 算子（新试） | 结果 |
|---|---|
| **`ts_target_tvr_hump(x, target_tvr=τ)`**（用户点名） | **可用且确实降 TO（0.116→0.109）**；但 **2Y 随 τ 单调上升后停在 1.58**：0.05→0.98 / 0.10→1.39 / 0.15→1.53 / **0.20→1.58** / 0.30→1.57 ⇒ **与 `decay`/`hump` 是同一自由度的反向版，不突破 1.58** |
| `ts_target_tvr_decay(x, …)` | 1.29~1.54，劣于基线 |
| **`quantile(x, driver=cauchy)` / `quantile(x, sigma=0.5)`** | 参数**确实存在**（更正旧记忆）；`sigma=0.5` 与默认等价（1.58），`driver=cauchy` 崩（0.49） |
| **`group_cartesian_product(g1,g2)`** | 可用；与 `subindustry` 的积 = subindustry 本身（1.58）；与图聚类键的积**过细⇒崩**（0.02~1.35） |
| `ts_av_diff` / `ts_scale` / `ts_ir` / `ts_max_diff` / `rank` / `zscore` 作核心 | 全部崩塌 |
| `normalize(useStd)` / `scale(longscale,shortscale)` / `pasteurize` / `tail` 包装 | 横截面保序 ⇒ **与基线逐位相同（1.58）**，无操作 |
| `group_backfill` / `group_std_dev` / `group_mean` / `vector_neut` / `if_else` | 1.50~1.57 或崩 |

⇒ **补扫 6 批 ≈48 条后，2Y 仍精确停在 1.58**。结论从「假设穷尽」变为「**实测穷尽**」。

⚠ **语法坑（已定案，方向与初判相反）**：整批 10 条 child 全部 `CANCELLED`（平台报 `Got invalid input at index 1, must be an expression`）的**真凶是把分组名加了引号**。
正确规则是**两条方向相反**的写法：
- **分组名必须裸写**：`group_neutralize(x, subindustry)` ✅｜`"subindustry"` ❌（本次 10/10 报废的原因）
- **`bucket` 的箱必须命名 + 双引号**：`bucket(rank(x), range="0,1,0.1")` ✅｜位置参数字符串 ❌（仓库专文 `docs/reference/bucket_operator_syntax_fix.md` 早已记载此症状）

⇒ 结论更正为：**`bucket` 本通道可用**，只是必须写成命名参数；此前"不可用"的记载作废。

## 六、结论

**DEU 的 ladder 闸（1.58）在本信号族下是硬天花板**：80+ 波、约 250 条探针后，2Y 停在 **1.58 = limit**，
只剩 **±0.005 的平台四舍五入分辨率**。所有经济面（prod / self / S / F / sub / CW / 双塔）**均已通过**。

**建议下一步（三选一）**：
1. **接受 1.58 与 limit 相等的事实**——若平台对 `value == limit` 有例外（本账户实测 `VkaZYdbG` 同情形返 403），
   则 `j28rN6YZ` 可提交；否则需要**换一个机制来源**（非 starmine / 非分析师修正）重找 2Y ≥1.6 的信号。
2. **换信号机制**：本族已穷尽；建议改攻 `pv1` / `fnd*` / `mdl219` 等**另一种机制**，用同一套「图聚类轴 + decay8 + 双窗」配方重刷。
3. **考虑 D0**（用户已否决）或**放宽 ladder**——均需用户明确授权。

⚠ **零提交**：本会话未提交任何 alpha（全局闸锁定）。候选均在平台 UNSUBMITTED。

## 七、附带：本会话的工程修复与环境事件

- **`tools/submit_batch.py`（已修）**：`run()` 循环内 `os.chdir(MCP_DIR)` 从不还原 ⇒ **`--spec` 多批只会发出第 1 批，
  其余静默丢失**（本轮实测 decay 2/8/16 全被吞）。已把 path 固化为绝对路径。
- **`C:\Users\MENGTAO\wqb-scripts\wqb_tools.py`（已修）**：① `dispatch` 从未定义 `--force`（提示是空头支票）；② 值型自检把
  `hump=0.01` 这类**关键字实参**误判为非法。均已修。
- **⚠ 环境事件**：`git status` 出现 **26 个 `tools/*.py` 被删除**（含 `_pyenv.py`，曾导致派发链断）。
  只恢复了必需的 `_pyenv.py`；其余 25 个未擅自动。如需全部恢复：`git checkout -- tools/`
