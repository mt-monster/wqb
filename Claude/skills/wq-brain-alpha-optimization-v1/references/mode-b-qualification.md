# Mode B 资格判定表（单一真相源）

> **一句话**：候选在 S4 没过闸后，「值不值得继续改（进 Mode B）」由 `src/wqb/workflow/mode_b_config.py::evaluate_mode_b` 判定——**主闸 + 5 条旁路 + 判死线**。本页是该函数的文档镜像，数值由 `tests/unit/07_docs_skills/test_mode_b_qualification_doc.py` 与代码逐项对拍；**别处不再手抄 1.25 / 0.8，一律链到本页**。
> **谁引用**：optimization-v1（Mode B 入场、组合腿救援）、how-to-pass（FAIL 回流）、RA step-7 / step-9 / decision-table。
> **作废说法**（2026-09-09 起）：「未达资格线（1.25/0.8）一律判死」「达标 → 强制进 Mode B；未达标 → 判死」——那是旧的双标量闸，会误杀下表旁路 A–E 的候选。

## 1. 判定顺序与判定表

按下列顺序求值，**首个命中即停**：主闸 → 旁路 A → B → C → D → E → 判死线 → 其余（`no_qualify`）。

| 层 | 名称 | 条件（默认值；区域可改的只有主闸） | 命中后的 `mode_b_action`（首选修法） | 需要的指标 |
|---|---|---|---|---|
| 主闸 | `main_gate` | `sharpe ≥ 1.25` **且** `fitness ≥ 0.8` | 无绑定（走 optimization-v1 通用 Step B1–B5） | sharpe, fitness |
| 旁路 A | `A_robust_strong` | `robust_sharpe ≥ 1.0` 且 `sharpe ≥ 0.8` | 降 turnover / 换平滑几何（ts_mean/ts_decay_linear） | robust_sharpe, sharpe |
| 旁路 B | `B_prod_corr_only` | `prod_corr ≥ 0.7` 且**其余维度全达标** | 换字段组合 / 换信号概念（禁止调权重） | prod_corr, other_dims_all_pass |
| 旁路 C | `C_margin_strong` | `margin ≥ 0.0005`（5bp）且 `sharpe ≥ 1.0` | 找正交腿组合（跨周期/跨逻辑） | margin, sharpe |
| 旁路 D | `D_turnover_fixable` | `returns ≥ 本数据集已测候选的 returns 中位数` 且 `turnover > 0.7` | 换平滑几何 / 降频 / 换聚合算子 | returns, returns_median, turnover |
| 旁路 E | `E_2y_strong` | `two_year_sharpe ≥ 1.2` 且 `sharpe ≥ 0.8` | 补短期腿（跨周期正交）或换中性化域提 IS | two_year_sharpe, sharpe |
| 判死线 | `dead_end` | `two_year_sharpe < 1.2` **且** `sharpe < 主闸` **且** `fitness < 主闸`（三项**同时**成立；**2Y ≥ 1.2 永不判死**） | 无（封存流程见 §2） | 三项都要有值 |
| 其余 | `no_qualify` | 不达主闸、无旁路命中、也不满足判死线 | 无 | — |

单位：`turnover` / `returns` / `margin` 都是**小数**（turnover 0.7 = 70%；margin 0.0005 = 5bp）。**未给的指标 = 该维度无数据 → 依赖它的旁路不命中（不是「通过」），判死线也不成立**（2Y 未知不能判死）。

## 2. 判定之后怎么办

| 结论 | 含义 | 动作 |
|---|---|---|
| `main_gate` | 主闸达标 | 进 Mode B 通用改进（optimization-v1 Step B1–B5） |
| `bypass` | 单项短板 / 2Y 强苗子 | 进 Mode B，**首选修法就是该旁路绑定的 `mode_b_action`**（不要用通用 B3 头脑风暴稀释） |
| `dead_end` | 三项同弱 | **候选级**判死：先 `tools/forum_recon.py`（`found=true` 不得直接判死），再 `seal_dead_end`——流程与「候选判死 ≠ 家族/波次判死」见 RA [`step9-writeback.md`](../../wq-brain-ra-pipeline/references/step9-writeback.md) §9.5 与 [`decision-table.md`](../../wq-brain-ra-pipeline/references/decision-table.md) D15 |
| `no_qualify` | 不达主闸、无可走旁路，但**不判死**（数据不足或单维度弱） | **不进 Mode B 改进**；候选留在 near / salvage（是否入池见 §5）或就此结束；**不写 `dead_end`**（写了就是把「没数据」当「没救」） |

## 3. 配置优先级（按代码，高 → 低）

只有主闸两值 `sharpe_min` / `fitness_min` 能被区域层改；**旁路阈值与判死线只来自第 3、4 层**。

| 序 | 来源 | 内容 |
|---|---|---|
| 1 | 区域 ledger `<REGION>/mode_b_qualification` | 自适应学习写入的主闸两值（`workflow/mode_b_adaptive.py` 在 S6 回写后更新） |
| 2 | `tracking/<REGION>/config/thresholds.json` 的 `mode_b_qualification` | `_overrides.{sharpe_min,fitness_min}` 单字段覆盖；无 `$ref` 的旧结构直接读顶层 `sharpe_min` / `fitness_min` |
| 3 | 全局 ledger `GLOBAL/mode_b_qualification` | 权威的主闸 + 旁路 + 判死线 |
| 4 | 代码内置 `_DEFAULT_GLOBAL` | 第 3 层读不到时的兜底（即上表默认值） |

**看本区实际生效值**（含主闸来源 `_source`）：`$WQ_PY tools/mode_b_qualify.py show --region <REGION>`。不要凭记忆或凭旧文档里的「1.25/0.8」判断——区域可能把主闸调过（饱和区降门、robust 墙区提门等）。

## 4. 代码入口覆盖了什么（以及没覆盖什么）

| 入口 | 喂给 `evaluate_mode_b` 的指标 | 实际生效的层 |
|---|---|---|
| `workflow_judge` 节点（`workflow/nodes/judge.py`） | sharpe / fitness / 2Y / margin / turnover / returns | 主闸、旁路 C、旁路 E、判死线；**A / B / D 在该入口恒不命中**（robust_sharpe、prod_corr、returns_median、other_dims 未喂）。结果在 `gates[platform_check].mode_b_{eligible,verdict,bypass,action}` |
| `tools/mode_b_qualify.py evaluate` | 全部 10 个入参 | **完整判定 A–E**（与代码同一函数，只读，不写库）：`$WQ_PY tools/mode_b_qualify.py evaluate --region <REGION> --sharpe .. --fitness .. [--two-year-sharpe ..] [--robust-sharpe ..] [--prod-corr .. --other-dims-pass] [--margin-bp ..] [--turnover ..] [--returns .. --returns-median ..]` |
| `workflow/mode_b_adaptive.py`、`tools/probe_batch_mode.py` | — | 只读主闸两值 |

所以：**要对一颗候选做资格判定，用 `mode_b_qualify.py evaluate` 喂全指标**；只看 judge 节点的 `mode_b_*` 会漏掉 A / B / D。

## 5. 别把这条线和相邻的阈值混了

| 对象 | 阈值来源 | 回答的问题 |
|---|---|---|
| **Mode B 资格线**（本页） | `mode_b_config`（§3 优先级） | 这颗候选**值不值得继续改** |
| 提交内部闸 | `config.GATES_INTERNAL`（Sharpe 1.58 / Fitness 1.0 …） | 这颗候选**能不能进提交链**（终点线，比资格线严） |
| salvage 入池线 | `review_wave.py::combo_candidate`：`sharpe > combo_sharpe_min`（缺省 1.0）且 `prod_corr < combo_prod_corr_max`（缺省 0.5）且无 CONCENTRATED_WEIGHT 硬失败；键在区域 `thresholds.json` 的 `review` 节 | 失败候选**收不收进弹药池**（收集宽；另有 near 补充） |
| 组合腿救援的动用 | 主腿 `eligible`（主闸或旁路）**且** Mode B 常规改进 2–3 轮仍被结构性闸门卡住 | 弹药**用不用**（动用严）；见 optimization-v1「组合腿救援」 |

入池宽、动用严：入池不看资格线（一颗 S∈(1.0, 1.25) 的候选可以入池），动用才守资格线。二者不矛盾，也不要在两处抄不同的数字。

## 6. 三个数值例（用 `mode_b_qualify.py` 复核过）

| 候选（区域取内置默认主闸） | 判定 | 为什么 |
|---|---|---|
| S 0.90、F 0.55、2Y 1.35 | `bypass` · **E** | 主闸不过；2Y ≥ 1.2 且 S ≥ 0.8 → 走「补短期腿 / 换中性化域」，**不判死** |
| S 0.90、F 0.55、2Y 0.90 | `dead_end` | 三项同弱（2Y < 1.2、S < 1.25、F < 0.8），旁路都不救 → 候选级封存流程（§2） |
| S 1.00、F 0.70、prod_corr 0.78、其余检查全过 | `bypass` · **B** | 只卡 prod 相关 → 换字段组合 / 换信号概念，**禁止调权重**；缺「其余全过」声明则 B 不命中 |

## 7. 维护

- 改判定逻辑只改 `mode_b_config.py`（与 `GLOBAL/mode_b_qualification` 台账），然后同步本页；`tests/unit/07_docs_skills/test_mode_b_qualification_doc.py` 会在数值 / 动作文案 / 优先级不一致时失败。
- 任何 skill 文档不得再写「未达资格线一律判死」——同一测试扫全部 SKILL / references，出现该类措辞且附近没有 `bypass` / 旁路 / 本页链接即失败。
