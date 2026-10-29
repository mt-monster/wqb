---
name: wq-alpha-gate-push-op-min
description: "候选 alpha 的『指标推到闸 + 算子压到最少』双目标优化器。挖掘出候选（有 id 或表达式）后，要把它系统性推到平台全闸通过（LOW_SHARPE / LOW_FITNESS / 2Y / self / prod / CW / sub），并同时把算子调用点数压到最小、删冗余算子时使用。含经验杠杆阶梯、算子压缩等价改写规则、逐算子消融协议与 op_count/compress/plan 三个本地脚本。触发词：优化指标 / 把指标做到极致 / 压缩算子 / 简化表达式 / 算子太多 / operatorCount 太高 / 推到能提交。"
last_verified: 2026-10-29
layer: L4
agent_created: true
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - mcp__wq-brain-http__get_alpha_details
  - mcp__wq-brain-http__check_self_correlation
  - mcp__wq-brain-http__check_correlation
  - mcp__wq-brain-http__preflight_expressions
  - mcp__wq-brain-http__submit_batch
user-invocable: true
---

# WQ Alpha：指标推到闸 + 算子压到最少

## 职责边界

- **本 skill 负责**：拿到一个**已有候选**（alpha id 或表达式）后，做两件互为约束的事——
  **(A) 把指标推到平台全闸通过**（`LOW_SHARPE` / `LOW_FITNESS` / 2Y 闸 / `SELF_CORRELATION` / `PROD_CORRELATION` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_TURNOVER`）；
  **(B) 把算子调用点数（operatorCount）压到最少**，删掉对指标无贡献的算子。
- **本 skill 不做**：不做从零选字段 / 开战役（→ `wq-brain-ra-pipeline` 与区域 skill）；不做提交（**提交权归用户**，`worldquant-submit-alpha`）；不做稳健性判据（→ `brain-alpha-robustness`）；不承诺把 `PROD_CORRELATION` 压到某个数（prod 墙处置只看 RA 决策表 D0-P）。
- **上游 / 下游**：上游 = 任何挖掘动作产出的候选（平台上有 id 即可）；下游 = self 相关性快筛（`brain-calculate-alpha-selfcorr-quick`）→ 稳健性（`brain-alpha-robustness`）→ 用户确认后提交。

**★ 铁律（沿用项目全局）**：只挖不提交（`ALLOW_ALPHA_SUBMIT=False`）｜DEU 只挖不跨区（若在 DEU）｜**判定只走平台**（合规只看 `get_alpha_details().code`；RA 只看 `is.checks`）｜发批前必过三闸（`op_arity` + 算子存在性 + 字段存在性）｜回执必看 `status=`。

---

## 核心次序：先测杠杆，再压算子，最后收敛设置

```
① 采集  →  ② 算子审计  →  ③ 杠杆推指标  →  ④ 压缩算子  →  ⑤ 设置收敛  →  ⑥ 判定/止损
   (只读)      (op_count)      (plan 出的阶梯)    (逐算子消融)     (decay/trunc)    (全闸)
```

**为什么压缩放在推指标之后**：压缩会改变指标（正向或负向）。
先把指标推到**有余量**（S 超过门槛 ≥0.02、fit ≥1.02），再压缩时就有预算承受个别算子的损失；
反过来先压缩、后推指标，会白扔掉本来能救命的算子。

**例外**：若候选**已接近平台 `operatorCount` 硬上限**（PPA 上限 8）或复杂度闸（调用点 ≥10）被拦，
则**先做压缩**拿到预算，再推指标。

---

## ① 采集（只读）

```bash
$WQ_PY -c "
import sys, asyncio, json
sys.path.insert(0,'world-quant-brain-mcp')
from brain_api import BrainApiClient
async def main():
    b=BrainApiClient(); await b.ensure_authenticated()
    a=(await b._request('GET','/alphas/'+sys.argv[1])).json()
    is_=a.get('is') or {}
    print('code:', ((a.get('regular') or {}).get('code') or ''))
    print('settings:', json.dumps(a.get('settings') or {}))
    for x in (is_.get('checks') or []):
        print('  %-26s %-8s val=%-9s lim=%s' % (x.get('name'), x.get('result'), x.get('value'), x.get('limit')))
asyncio.run(main())
" <ALPHA_ID>
```

**★ 读取格式铁律**：原始 API 指标在 **`is` 下直接展开**（`is.sharpe` / `is.fitness` / `is.checks`），
**不是 `is.metrics.*`**（后者是 MCP 封装格式，用错键会得到全 `None` 的假数据）。

相关性：`self` 用 `check_self_correlation(alpha_id)`；`prod` 用 `check_correlation(alpha_id, refresh=True)`
（**>48h 的台账读数不可信**）。

**逐项记录缺口**：把每个 FAIL / 未过的闸写成 `(闸名, 当前值, 门槛, 缺口)`——这是 ③ 的输入。

---

## ② 算子审计

```bash
$WQ_PY "$SKILL_DIR/scripts/op_count.py" --expr "<表达式>"           # 或 --alpha-id / --file
```

输出：**总调用点数**、**逐算子计数**、**可压缩候选清单**（重复子表达式、冗余包裹、可由 1 算子替代的多算子组合）。

算子压缩的**完整改写规则**见 [`references/op-compression.md`](references/op-compression.md)。
其中最高频的 5 条（按收益排序）：

| # | 改写 | 省算子 | 性质 |
|---|---|---|---|
| C1 | 两条腿相同 `multiply(rank(x),rank(x))` → `rank(x)` | −2~−3 | **有损**（需重测；常使 S 上升） |
| C2 | 双层同轴 `group_rank(group_rank(x,g),g)` → `group_rank(x,g)` | −1 | 近似无损 |
| C3 | 冗余包裹 `reverse(reverse(x))` / `rank(rank(x))` / `add(x,0)` / `multiply(x,1)` | −1/+ | 无损 |
| C4 | 双算子平滑 `ts_decay_linear(ts_mean(x,a),b)` → `ts_target_tvr_decay(x,target_tvr=)` 单算子 | −1 | **有损**（三赢：TO↓/ladder↑），逐档实测 |
| C5 | 外层 `winsorize(x,std=k)` 消融测试（k 已饱和时删掉可能不损或微损） | −1 | **有损**（本战役实测 std≥3 提供 +0.02 S，删前必测） |

---

## ③ 杠杆推指标（按缺口选杠杆）

```bash
$WQ_PY "$SKILL_DIR/scripts/plan.py" --sharpe 1.56 --fitness 1.15 --two-year 1.91 \
    --self 0.14 --prod 0.41 --turnover 0.133 [--ops 12] [--axis fact1] [--region DEU]
```

输出**有序杠杆清单**（按「实测效果 × 与本构造的适配度」排序）+ 每条的预期增益与代价。

**杠杆阶梯（经验实测排序，完整版见 [`references/lever-ladder.md`](references/lever-ladder.md)）**：

| 优先级 | 杠杆 | 实测增益 | 适用条件 / 代价 |
|---|---|---|---|
| **L1** | **分组轴 → `sector`**（平台内置） | **S +0.26~0.29** | 把严格的 `IS_LADDER_SHARPE` 换成宽松 `LOW_2Y_SHARPE`；⚠ institutions1 类掩码腿上反向失效（须用数据集 GROUP 轴） |
| **L2** | **双窗级联** `multiply(rank(ts_delta(x,a)), rank(ts_delta(x,b)))`，a≈240 / b≈176 | **S +0.18、2Y +0.6** | 同一比率两个时间尺度；窗为尖峰（±15 就掉） |
| **L3** | **`ts_target_tvr_decay(x, target_tvr=t)`** | **S +0.03、TO↓、fit↑** | **仅当 TO > t 时激活**（TO < t 是 no-op）；本战役 t=0.05 |
| **L4** | `winsorize(..., std=3~4)` | S +0.02 | std≥3 饱和；std=1 崩塌 |
| **L5** | `decay` ↑（2→8） | 提 fit（TO↓ ⇒ fit ×√ratio） | 对 S 影响 ±0.02；decay 3 偶有微提 |
| **L6** | `multiply(rank(A), rank(B))` 两腿联合 | S +0.11（**逐 category 实测**） | analyst93 有效、fundamental6 反向失效 |

**禁用杠杆（本战役已证否，别再投）**：

| 禁用 | 现象 |
|---|---|
| 换 `neutralization` 档 | **全档降 S**（FAST 最优；CROWDING 可把 S 从 1.56 打到 0.42） |
| 时间平滑 `ts_decay_linear` / `hump` | 累积型信号上**零和**（降 TO 同时削 alpha） |
| `group_zscore` / `tail` / `bucket` 轴 | 在 rank 类信号上常灾难失败（S 负） |
| `trade_when` 门控 | 稀疏事件型数据上样本骤减，S 全差于无门控 |
| 腿方向混合 `multiply(rank(A), reverse(rank(B)))` | **数学无效**：平台 `reverse` = 整体取负，不产生混合信号 |
| 扫 `truncation` | 零杠杆（0.04 与 0.12 指标逐位相同） |

**发批前三闸**（一条语法错 ⇒ 整批 CANCELLED）：
```bash
$WQ_PY -c "
import sys,os; sys.path.insert(0, os.path.join(os.getcwd(),'src'))
from wqb.expression import op_arity
V=['<expr1>','<expr2>']
op_arity.ensure_safe_for_dispatch(V); print('闸② op_arity OK')
" && $WQ_PY tools/submit_batch.py --path <file> --region <R> --universe <U> --delay 1 \
    --decay 4 --neutralization FAST --truncation 0.08 --nan-handling ON
```

**★ 闸④ 单位类型闸（2026-10-13 DEU 新增，`op_arity` 不覆盖，已造成一次整批 CANCELLED）**：
`bucket(X, range=...)` 的 X 若未经 `rank` 归一到 [0,1]，输出**不是 `Unit[Group:1]`**，
作 `group_neutralize/group_rank/group_zscore` 的第 2 参会直接报
`Incompatible unit for input of "group_*" at index 1, expected "Unit[Group:1]", found "Unit[]"`。
⇒ **任何用作分组轴的 `bucket(...)`，其内层第一个参数必须是 `rank(...)`**。本地零成本自检：
```python
import re
risk=[e for e in V if re.search(r'group_(?:neutralize|rank|zscore)\([^,]+,\s*bucket\((?!rank)', e)]
assert not risk, f"闸④ 单位风险 {len(risk)} 条"
```
完整实证见 [`references/op-compression.md`](references/op-compression.md) §四（DEU A 级框架压缩阶梯 + 四条硬结论）。

---

## ④ 压缩算子（逐算子消融协议）

```bash
$WQ_PY "$SKILL_DIR/scripts/compress.py" --expr "<表达式>" [--metrics '{"sharpe":1.59}']
```

输出**压缩候选清单**（每个候选标注：省几个算子、是否无损、需不需要重测）。

**消融协议（必须按此顺序）**：

1. **无损改写先做**（C3 类）——理论上指标逐位相同，但仍需 1 条仿真确认。
2. **有损改写逐个测**——一次只删/换一个算子，其余冻结。规则：
   - 删掉后 **全闸仍 PASS** ⇒ 采纳（这是最理想的压缩）。
   - 删掉后 **某闸从 PASS 变 FAIL** ⇒ 回滚该算子（它是有用的）。
   - 删掉后 **指标更差但仍 PASS** ⇒ 采纳（余量换算子数，符合「压到最少」目标）。
3. **批量验证**——把采纳的改写合并成 1 个表达式，跑 1 条仿真确认合并后仍达标。
4. **设置层最后收敛**——decay / truncation 在表达式冻结后微调（它们不占算子）。

**压缩终止条件**：① 已无「删除后仍 PASS」的算子；或 ② 再删会掉闸；或 ③ 达到 operatorCount 目标（REGULAR 无硬上限，PPA 上限 8）。

**⚠ 压缩的代价必须记账**：每次采纳一个压缩都有**新的 alpha id**；同一骨架的多个变体互相关会 >0.99，
⇒ **最终只应保留指标最好且算子最少的那 1 个**，其余标 `SUPERSEDED`。

---

## ⑤ 设置收敛（表达式冻结后）

只动不占算子的旋钮：`decay`（2/3/4/6/8）、`truncation`（本战役零杠杆，可不动）、
`nanHandling`（ON/OFF 是「换信号」档，改动后不可与旧档对比）、`neutralization`（**全档降 S，保持 FAST**）。

---

## ⑥ 判定与止损

- **达标口径**：`is.checks` 全部 PASS（含 2Y 闸）+ `self < 0.7` + `prod < 0.7`。 <!-- from config.prod_corr_max -->
  ⚠ 平台 ladder / 2Y 类检查**四舍五入到 2 位后严格比较** ⇒ 显示值须 ≥ limit **+0.005**（`S` 类按显示值比）。
- **止损**：同一 alpha 累计 **≥3 轮**仍卡在结构性闸门 ⇒ 停止（判死前必须先完成 ③ 的杠杆扫描与 ④ 的消融扫描）。
- **产出**：把最终达标表达式 + 全部指标 + 压缩前后的算子数写入本轮回复；有 id 的入队
  `$WQ_PY tools/ledger/mining_ledger.py add --alpha-id <ID> --region <R> --universe <U> --wave <W> --src "<描述>"`。

---

## 渐进式文档

- 杠杆阶梯（完整实测数据、适用条件、反例）：[`references/lever-ladder.md`](references/lever-ladder.md)
- 算子压缩改写规则（无损/有损分类、语义等价表）：[`references/op-compression.md`](references/op-compression.md)
- 指标 ↔ 杠杆映射（每个闸由哪些旋钮驱动）：[`references/metric-map.md`](references/metric-map.md)
- 脚本：`scripts/op_count.py`（算子审计）｜`scripts/compress.py`（压缩候选）｜`scripts/plan.py`（杠杆计划）
