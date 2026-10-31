# 逐算子双通道扫描协议（用户指令 2026-10-31）

> **目标**：对表达式里的**每个算子节点**（按 L1/L2/L3/L4 逐层遍历）都做两类实验，把因子指标推至最好：
>
> **① 删除通道** —— 删除该算子后有没有压缩的变化（算子数减少）且指标不坍塌？
> **② 替换通道** —— 替换成金融含义等价的另一算子后，指标是否更精简且不坍塌？
>
> 另加 **③ 参数扫描** —— 把每个数值参数展开成档位，把指标推至最好。
>
> 执行入口：`scripts/scan.py`（纯本地、零平台调用、零队列成本，只生成候选，不做仿真）。
> 判定只走平台（`submit_batch` 派发 + `check_correlation` 实测 prod/self）。

---

## 0. 与 ④ / ④b 的关系（不要重复）

| 节 | 覆盖 | 本协议补充 |
|---|---|---|
| ④ 压缩算子 | 消融**协议** + 规则化候选（`compress.py`，只匹配 C1/C3/C4… 既定模式） | **逐算子节点遍历**：`scan.py --delete` 对**每个**算子节点生成删除候选，包括 `compress.py` 没有的 `f(x)→x` 单参包裹删除 |
| ④b 等效替换 | 人工遍历平台算子找金融含义等价（不脚本化） | **自动等价表**：`scan.py --replace` 内置 14 组等价对，逐节点生成替换候选 + 数学等价标记 |
| ③ / ⑤ 杠杆与设置 | 杠杆阶梯 + decay/trunc 收敛 | **参数级扫描**：`scan.py --params` 对每个数值参数展开 0.5/0.75/1.25/1.5 档 |

**⇒ 本协议是 ④/④b 的「自动化执行层」**：先跑 `scan.py` 拿候选矩阵，再按下面的判定规则逐条实测、逐条取舍。

---

## 1. 生成候选矩阵（一次，零平台）

```bash
$WQ_PY scripts/scan.py --expr "<表达式>" --json > scan_report.json        # 三通道全开
$WQ_PY scripts/scan.py --expr "<表达式>" --delete --json > del.json        # 只删除通道
$WQ_PY scripts/scan.py --expr "<表达式>" --replace --json > rep.json       # 只替换通道
$WQ_PY scripts/scan.py --expr "<表达式>" --params --out params.txt         # 参数变体直接喂 submit_batch
```

输出结构（`scan_report.json`）：
```
{
  "expr": <规范化表达式>,
  "op_count": N,
  "per_op": {算子: 次数},
  "layers": {"L1 提取": [...], "L2 归一": [...], "L3 时序": [...], "L4 截面": [...]},
  "delete_candidates":   [ {kind, target_op, layer, target, expr, op_before, op_after, op_saved, lossless, note}, ... ],
  "replace_candidates":  [ {kind, target_op, replaced_by, layer, math_equivalent, expr, op_before, op_after, note}, ... ],
  "param_variants":      [ {kind, target_op, layer, param_idx, old_value, new_value, factor, expr}, ... ]
}
```

**每层算子都尝试** = 候选矩阵里 `layers` 的每个 L1/L2/L3/L4 算子都至少有一条删除候选或替换候选；
若某层某算子**无任何候选**（如最底层 `divide` 无法删除、无等价替换），`scan.py` 会如实不输出——说明该算子在此骨架上是**承重项**，跳过即可。

---

## 2. 删除通道判定（① 删除后有没有压缩的变化）

对每条 `delete_candidates`（按 `lossless` 优先、`op_saved` 降序、逐层遍历）：

1. **无损候选先做**（`lossless=true`：恒等元素、重复腿）——理论指标逐位相同，仍需 1 条仿真确认。
2. **有损候选逐个测**（`lossless=false`：单参包裹 `f(x)→x` 等）——一次只删一个，其余冻结：
   - 删除后 **全闸仍 PASS** ⇒ **采纳**（算子数 -1，这是「压缩的变化」，首选）。
   - 删除后 **某闸 PASS→FAIL** ⇒ **回滚**（该算子承重，删不得）。
   - 删除后 **指标更差但仍 PASS** ⇒ **采纳**（余量换算子数，符合「压到最少」）。
   - 删除后 **指标变好** ⇒ **采纳且记为正增益**（消融提指标，双赢）。
3. **批量验证**：把采纳的删除合并成 1 个表达式，跑 1 条仿真确认合并后仍达标。

**⚠ 删除通道的常见陷阱**：
- 删除**最外层** `rank` 常让 S 变好但 sub/2Y 崩（rank 是截面归一的承重项）——必看全部闸，不能只看 S。
- 删除 `ts_backfill` 常省算子但 **sub_universe 崩**（backfill 提高有效覆盖，见 op-compression.md 4.2 硬结论②）。
- 删除比率分母（`divide(A,B)` 的 B）是**双赢候选**（C11，省 2 算子且提 S），但若去掉后 S 降则说明比率本身是信号来源，须保留。

---

## 3. 替换通道判定（② 替换后有没有更精简指标而不坍塌）

对每条 `replace_candidates`（按 `math_equivalent` 优先、逐层遍历）：

1. **数学等价**（`math_equivalent=true`，如 `ts_rank↔ts_quantile(gaussian)`、`rank↔rank` 吸收单调变换）：
   **无需实测**——外层单调算子吸收内层变换，逐位相同。仅当「省算子」或「换实现」时有价值，否则跳过。
2. **语义等价**（`math_equivalent=false`，如 `ts_av_diff↔ts_zscore`、`ts_mean↔ts_sum`、`vector_neut↔group_neutralize`）：
   **必须实测**——金融含义保留、实现不同，可能改善指标/prod。
3. **采纳判据**（替换变体全闸 PASS 时，任一条满足即采纳）：
   - **prod 更低** ⇒ 优先采纳（**prod 贴线时尤其**：余量 <0.05 的候选，低 prod 变体比 S 最优变体更值得交付——prod 漂移猛，48h 作废）。
   - 或 **指标更好**（S/2Y/sub 更高）；或 **算子更少**。
   - 否则回滚，保留原式。
4. **铁律**：替换变体必须**复检 prod**（`check_correlation(refresh=True)`，占平台单并发槽）；替换同样产生新 id，最终只保留最优 1 颗。

**⚠ 替换通道的常见陷阱**：
- `ts_mean→ts_sum` / `ts_mean→ts_decay_linear`：**第 2 参语义不同**（窗口 vs 衰减）——是「语义等价」但参数含义漂移，实测后若指标塌则回滚。
- `group_rank(x,g)→rank(x)`：**丢弃分组轴**——从组内归一退化为全局归一，常崩 sub，需实测。
- `rank→group_rank` / `group_rank→rank` 需要人工轴：`scan.py` 标 `need_axis` 占位，**不自动生成**，由你手动给轴后另测。
- **★★ `vector_neut↔group_neutralize`（2026-10-31 实测连坐教训）**：两者第 2 参**单位语义不同**——
  `vector_neut` 第 2 参是任意**向量轴**（如 `ts_backfill(...)` 结果为 `Unit[]`），`group_neutralize` 第 2 参必须是 **`Unit[Group:1]`**（`bucket`/`group_rank` 等）。直接替换会触发平台
  `Incompatible unit for input of "group_neutralize" at index 1, expected "Unit[Group:1]", found "Unit[]"` ⇒ **整批 CANCELLED（连坐）**。
  `scan.py` 已标 `need_unit` 占位不自动生成；若手工替换，**必须先把第 2 参换成 Group 单位**（如 `bucket(rank(...),range=...)`），且内层第一个参数必须是 `rank(...)`（见 op-compression.md §四 闸④）。

---

## 4. 参数扫描判定（把指标推至最好）

对每条 `param_variants`（按 target_op 逐算子、逐参数）：

1. **扫描档位**：`×0.5 / ×0.75 / ×1.25 / ×1.5`（scan.py 默认）。粗扫后用**黄金分割或二分**在最优档位附近细扫。
2. **逐档实测**：同 settings 派发，记录 S/F/2Y/sub/TO/prod。
3. **取指标最优档**：通常 S 或 2Y 在某个窗口处单峰（见 rKRkL9QE 案例：ts_zscore 窗口 126→252→504，252 最优；126 崩溃）。
4. **⚠ 窗口参数是尖峰**：±15 就掉（lever-ladder L2 的「窗为尖峰」），细扫步长宜 ≤窗口的 5%。
5. **与删除/替换解耦**：参数扫描在表达式冻结后做（不占算子，属 ⑤ 设置层收敛的延伸）。

---

## 5. 终止条件 + 记账纪律

**终止**：① 三通道全部候选实测完毕；或 ② 已达到 operatorCount 目标（REGULAR 无硬上限但复杂度闸 <10；PPA ≤8）；或 ③ 再动任何算子会掉闸。

**记账**（沿用 §4 记账纪律）：
- 每次采纳（删除/替换/参数调整）都产生**新 alpha id** ⇒ 必须记 id→表达式映射，不要靠记忆。
- 同骨架变体互相关 >0.99 ⇒ 最终**只保留指标最好且算子最少的那 1 个**，其余标 `SUPERSEDED`。
- **压缩不可与推指标同时进行**：先推指标到有余量（S≥门槛+0.02、fit≥1.02），再压缩/替换；否则会误删救命算子。
- 全部候选入 `tools/ledger/mining_ledger.py`（删除/替换失败标 `SIM_FAIL`，采纳标 `SUPERSEDED`/`DONE`）。

---

## 6. 端到端模板（2026-10-31 rKRkL9QE 案例，可用作范式）

**对象**：`rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, cap), 252), 84, driver=gaussian))`，GBR/TOP700。

| 步 | 通道 | 动作 | 结果 |
|---|---|---|---|
| ① | 采集 | get_alpha_details | S2.21/F2.05/2Y2.51/sub1.77 全过；**prod 0.6783 贴线** |
| ② | 审计 | op_count | 4 算子，无自动压缩点 |
| ③ | **替换** | `scan.py --replace`：`ts_av_diff→ts_zscore`（L3，语义等价） | S2.01/F1.74/2Y2.13/sub1.67 全过；**prod 0.5786**（贴线→深墙，×5.6） |
| ④ | 参数 | ts_zscore 窗口 126 / 504 | 126 崩溃（S1.38）、504 变差（S1.86）⇒ **252 保持** |
| ⑤ | 参数 | ts_quantile 参数 84→63 | S1.98 略差 ⇒ 保持 84 |

**净效果**：prod 贴线（余量 0.0217）→ 深墙（余量 0.1214，×5.6），IS 全闸仍 PASS。
**教训**：删除与替换是两回事——删除 `ts_quantile` 会崩（S2.15→0.55），但**替换** `ts_av_diff→ts_zscore` 保留信号且降 prod。
