# 算子压缩改写规则

> 目标：**在指标不倒退的前提下，把算子调用点数（operatorCount）压到最少。**
> `operatorCount` 的平台口径 = 表达式里 `名称(` 形式的**函数调用点个数**（与
> `tools/build_gate_prior_from_inventory.py::op_count` 的正则 `\b([a-z][a-z0-9_]{2,})\s*\(` 同源）。
> ⚠ 平台返回的 `operatorCount` 才是最终裁判；本地计数只是预览。

---

## 一、无损改写（UNSAFE=否，理论上指标逐位不变，但仍需 1 条仿真确认）

| # | 改写 | 省算子 | 说明 |
|---|---|---|---|
| C3.1 | `reverse(reverse(x))` → `x` | −2 | 双重取负 |
| C3.2 | `rank(rank(x))` → `rank(x)` | −1 | rank 幂等 |
| C3.3 | `group_rank(group_rank(x,g),g)` → `group_rank(x,g)` | −1 | 同轴 group_rank 幂等 |
| C3.4 | `add(x,0)` / `multiply(x,1)` / `subtract(x,0)` → `x` | −1 | 恒等元素 |
| C3.5 | `ts_mean(x,1)` / `ts_sum(x,1)` / `ts_delay(x,0)` → `x` | −1 | 窗=1/0 退化 |
| C3.6 | `-1 * (-1 * x)`（若表达式里有显式负号乘法） → `x` | −2 | 双重取负 |
| C3.7 | `abs(abs(x))` → `abs(x)` | −1 | 幂等 |
| C3.8 | `signed_power(signed_power(x,1),1)` → `x` | −2 | 幂=1 |

⚠ **C3 有一个陷阱**：平台的部分算子在 `x` 为常量/全 NaN 时行为不同；改写后仍要跑 1 条仿真确认。

---

## 二、有损改写（UNSAFE=是，**必须逐个消融测试**）

按「收益（省算子数）」排序；每个都标注了在 2026-10 DEU 战役上的实测效果。

| # | 改写 | 省算子 | 实测效果 / 风险 |
|---|---|---|---|
| **C11** ★★★ | **去掉比率归一化**：`ts_delta(divide(A,B),W)` → `ts_delta(A,W)` | **−2** | **2026-10-12 实测（本 skill 首个「双赢」压缩）：算子 10→8 且 S 1.61→1.65、fit 1.23→1.27、2Y 1.94→1.98**。机制：**水平变化信号被比率归一化稀释**，去掉分母让信号更纯。⚠ 反向也成立 ⇒ **若去掉分母后 S 下降，说明该比率本身是信号来源，须保留** |
| **C12** | `multiply` 内的 `rank()` 消融 | −1~−2 | **实测不可删**：两腿都去 rank ⇒ S 1.57→**0.61**（崩）；只去一个 ⇒ 1.34（不够）。`rank` 是联合信号的必需归一化 |
| **C13** | 联合形态替换：`multiply(rank(A),rank(B))` → `subtract(rank(A),rank(B))` | 0 | **实测劣化**：1.57→**0.73**（崩）。差值形态在本信号上无效，算子数也不省 ⇒ 无用 |
| **C14** | 限速器强度调节 `ts_target_tvr_decay(x, target_tvr↓)` | 0 | **实测 target 越低 S 越高**：0.05→1.61、0.04→1.65、0.035→1.70、**0.03→1.73**；过低（0.02）回落。⚠ 不省算子，但可与 C5/C10 组合出「少算子 + 高 S」 |
| **C1** | **重复腿合并**：`multiply(rank(x),rank(x))` → `rank(x)`；`multiply(a,a)` → `a` | −2~−3 | 两腿完全相同时是纯冗余。**实测常使 S 上升**（因 rank 平方在 [0,1] 上单调）。**首选压缩** |
| **C2** | **窗口嵌套折叠**：`ts_mean(ts_mean(x,a),b)` → 单层 `ts_mean`，窗口取两者之和减 1（近似） | −1 | 近似；指数平滑核不同，需测 |
| **C4** | **双平滑 → 单元限速器**：`ts_decay_linear(ts_mean(x,a),b)` 或 `hump(ts_mean(x,a))` → `ts_target_tvr_decay(x, target_tvr=t)` | −1 | **三赢**（TO↓/ladder↑）；需 `TO > t` 才激活。⚠ `hump` 在累积型信号上是零和，不宜单独保留 |
| **C5** ★ | **饱和 winsorize 消融**：删掉外层 `winsorize(x,std=k)`（k≥3） | −1 | **2026-10-12 实测：在 `ts_target_tvr_decay` 外层时可无损删除**（8 ops 1.65/1.27/1.98 == 7 ops 1.65/1.27/1.98，逐位相同）。⚠ 若 winsorize 直接包裹 `group_rank`（无 tvr 层）则删了会掉 ~0.02 S |
| **C15** ★★★ | **限速器整体消融**：`ts_target_tvr_decay(x, target_tvr=t)` → `x`（**仅当自然 TO < t**） | **−1** | **2026-10-13 EUR 实测（本规则首个案例）**：自然 TO **0.112 < t=0.18** ⇒ 限速器从未激活；删除后 **5 ops 与 4 ops 指标逐位相同**（S1.71/F1.09/TO0.1124/2Y1.78/margin9.02bp），prod 0.6170→**0.6171**、self 0.1753→**0.1752**（均不变）⇒ **完全无损**。⚠ **删前必看自然 TO**：若 `TO > t` 则限速器会激活，删除将同时改变 TO 与 S（此时改走 C14 调 t） |
| **C6** | **方向算子合并**：`reverse(group_rank(reverse(x),g))` → `reverse(group_rank(x,g))` | −1 | 外侧 reverse 作用于 MATRIX，与内侧等价（内侧 reverse 作用于 MATRIX 时同号）——**逐例验证** |
| **C7** | **掩码内联**：`if_else(cond, A, 0)` 若 `A` 本身在 cond 外恒为 0 ⇒ 去掉 if_else | −1 | 若信号只在条件内非零，掩码是冗余的 |
| **C8** | **`divide` + 分子归一**：`divide(a, add(b, 0.0001))` 去掉 `add(b,0.0001)`（若 b 无零值） | −1 | 平台除零会产 NaN；若 b 最小值为正则可去。**有风险** |
| **C9** | **常数折叠**：`multiply(x, const)` 若 const 吸收进相邻算子 | −1 | 逐例 |
| **C10** | **外层 axis 吸收**：`winsorize(group_rank(x, sector), std=4)` 若 `winsorize` 无贡献 ⇒ 交换为 `group_rank(winsorize(x,std=4), sector)` 时算子数不变；**但若可整体删除** ⇒ −1 | −1 | 需测 |

---

## 三、消融协议（必须按序执行）

```
对候选表达式的每个算子 o：
  1. 构造 expr_without_o（语义上尽量保持其余冻结）
  2. 跑 1 条仿真（同一 settings）
  3. 三分支：
     (a) 全闸仍 PASS        → 采纳（删除 o 新 id），继续消融下一个
     (b) 某闸 PASS → FAIL   → 回滚 o（o 是必需的），继续下一个
     (c) 指标更差但全闸仍 PASS → 采纳（余量换算子数，符合「压到最少」）
  4. 把采纳的改写一次性合并，跑 1 条确认合并后仍达标
```

---

## 四、DEU A 级框架压缩实证（2026-10-13，`wq-alpha-gate-push-op-min` 首次在 DEU 落地）

**对象**：`WjLEOqLP`（11 算子，S1.77/F1.61/2Y1.83/sub0.88，全闸通过）
```
group_neutralize(group_rank(add(ts_mean(bf,1), ts_mean(bf,210)), sector),
                 bucket(rank(ts_mean(bf,252)), range="0,1,0.05"))      bf=ts_backfill(F,1008)
```

### 4.1 压缩阶梯（9 个消融变体，同设置回测）

| 改写 | 算子 | S | F | 2Y | sub | 判定 |
|---|---|---|---|---|---|---|
| 基线 `WjLEOqLP` | 11 | 1.77 | 1.61 | 1.83 | 0.88 | PASS |
| **C3.5 `ts_mean(bf,1)`→`bf`** | **10** | **1.77** | **1.61** | **1.83** | **0.88** | **✅ PASS·逐位相同（真无损）** |
| 去 `ts_backfill` | 7 | **1.79** | **1.64** | 1.64 | **0.80** | ❌ **`LOW_SUB_UNIVERSE_SHARPE` FAIL（0.80<0.85）** |
| `group_rank` 合并 `group_neutralize` + 轴复用 210 | 9 | 0.89 | 0.51 | 0.65 | — | ❌ 灾难 |
| 窗统一 252 + 轴复用 | 10 | 1.57 | 1.34 | **1.93** | — | ❌ S 差 0.01 |
| 9q 同构去 `ts_backfill` | 7 | 1.67 | 1.51 | 1.54 | — | ❌ 2Y 差 0.04 |
| 长窗 66 | 10 | 1.55 | 1.30 | 1.57 | — | ❌ |
| 极简对照（去桶轴，5 算子） | 5 | 1.59 | 1.39 | **1.20** | — | ❌ 2Y 崩 |

### 4.2 四条硬结论

1. **C3.5 在本框架上完全无损**：`ts_mean(bf,1)` ≡ `bf`，**10 年逐年统计与 prod/self 全部逐位相同**（S1.77/F1.61/2Y1.83、prod 0.651、self 0.3437）⇒ **11→10 算子，零代价，应无条件采纳**。
2. **★ `ts_backfill` 是 sub_universe 的承重项，不是可删冗余**：去掉后省 4 算子、S/F 反而更高（1.79/1.64），但 `sub_universe` 从 0.88 掉到 0.80 跌破闸（limit 0.85）。
   机制：`ts_backfill(F,1008)` 把 NaN 用 1008 日内最后有效值填补 ⇒ **提高有效覆盖 ⇒ 提高子宇宙 Sharpe**。
   ⇒ **「S/F 更高」不等于「可采纳」，必须看全部闸。**
3. **桶轴（`bucket(rank(ts_mean(bf,252)), range=...)`）是 2Y 的承重项**：去掉后 5 算子但 2Y 从 1.83 崩到 1.20。
4. **`group_rank` 不能替 `group_neutralize`**（本框架实测 0.89）——与 WjLEOqLP 的 `group_neutralize(group_rank(...), bucket(...))` 双层结构不等价。

### 4.3 ★ 新增第④闸：**单位类型闸**（`op_arity` 三闸未覆盖，已造成一次整批 CANCELLED）

**事故**：把 `bucket(rank(ts_mean(bf,252)), range=...)` 改成 `bucket(ts_mean(bf,252), range=...)`（去掉内层 `rank` 省 1 算子）⇒ 平台报
```
Incompatible unit for input of "group_neutralize" at index 1,
expected "Unit[Group:1]", found "Unit[]"
```
⇒ **一条语法/单位错 ⇒ 整批 10 条全部 CANCELLED**（连坐）。

**根因**：`bucket(X, range=...)` 的输入若未经 `rank` 归一到 [0,1]，其输出**不是 Group 单位**，不能作 `group_neutralize` / `group_rank` / `group_zscore` 的第 2 参。

**⇒ 发批前新增第④闸（本地正则，零成本）**：
```python
import re
risk = [e for e in exprs
        if re.search(r'group_(?:neutralize|rank|zscore)\([^,]+,\s*bucket\((?!rank)', e)]
assert not risk, f"单位风险 {len(risk)} 条：bucket 作分组轴必须内包 rank"
```
**规则**：**任何 `bucket(...)` 只要被用作分组轴（`group_*` 的第 2 参），其内部第一个参数必须是 `rank(...)`。**

**消融顺序建议**（从收益最高 / 风险最低开始）：
`C3 系列（无损）` → `C1 重复腿` → `C4 双平滑折叠` → `C5 winsorize` → `C10 外层 axis` → `C8 常数/分母` → 其余。

---

## 四、压缩的记账纪律

1. **每次采纳改写都产生新的 alpha id** ⇒ 必须记录 id → 表达式映射（不要靠记忆）。
2. **同骨架变体互相关 >0.99**（memory 铁律）⇒ 最终**只保留指标最好 + 算子最少的那 1 个**，
   其余标 `SUPERSEDED` 或从提交候选中剔除。**不要把压缩过程中的中间产物当独立候选。**
3. **压缩不可与推指标同时进行**——先推指标到有余量，再压缩；否则会误删救命算子。
4. **平台 `operatorCount` 与本地计数若有差异，以平台为准**；差异常出现在
   `if_else` 内置常量（如 `-1`）、命名参数、`bucket` 的 range 字符串上。

---

## 五、算子数的硬约束（参考）

| 场景 | 上限 | 出处 |
|---|---|---|
| REGULAR alpha | 无平台硬上限 | 但复杂度闸「算子调用点数 <10」会拦（`brain-make-some-gem` 复杂度预算） |
| **PPA（Power Pool）候选** | **operatorCount ≤ 8** | 平台 Power Pool 规则 |
| SuperAlpha（SUPER） | 组件级，不做表达式层加权 | `wq-brain-superalpha` |

⇒ 若目标是 PPA 或需过复杂度闸，**压缩是前置硬需求**，应在推指标**之前**先做（见 SKILL.md 的次序例外）。

---

## 六、已实测端到端案例（2026-10-12 DEU，可作模板）

**起点** `zqbVMkv1`（10 算子，全闸已通过但 S 余量仅 +0.01、且卡复杂度闸）
```
winsorize(group_rank(ts_target_tvr_decay(multiply(
    rank(ts_delta(divide(fnd6_newq_oiadpq, fnd6_newq_seqq), 240)),
    rank(ts_delta(divide(fnd6_newq_oiadpq, fnd6_newq_seqq), 176))),
    target_tvr=0.05), sector), std=4)
```

| 轮次 | 动作 | 算子 | S | fit | 2Y | 判定 |
|---|---|---|---|---|---|---|
| 起点 | — | 10 | 1.59 | 1.20 | 1.94 | 全过（S 余量 +0.01） |
| ①推余量 | `target_tvr` 0.05→0.04 | 10 | **1.61** | 1.23 | 1.94 | ✅ 余量 +0.03 |
| **②C11 去 divide** | `ts_delta(divide(A,B),W)`→`ts_delta(A,W)` | **8** | **1.65** | **1.27** | **1.98** | ✅ **双赢** |
| **③C5 去 winsorize** | 删外层 `winsorize` | **7** | **1.65** | 1.27 | 1.98 | ✅ **逐位相同** |
| ④C14 再加 target 0.04→0.03 | 限速器加强 | 7 | **1.73** | **1.37** | 1.87 | ✅ 指标最高 |
| **⑤6 算子窗微调** | 短窗 176→180 | **6** | **1.61** | **1.21** | **1.99** | ✅ **算子最少** |

**最终两条可选**（都全闸通过）：
- 算子最少：`group_rank(multiply(rank(ts_delta(fnd6_newq_oiadpq,240)),rank(ts_delta(fnd6_newq_oiadpq,180))),sector)`（**6 算子**，S1.61/fit1.21/2Y1.99/self0.189/prod0.436）
- 指标最高：加 `ts_target_tvr_decay(target_tvr=0.03)`（**7 算子**，S**1.73**/fit**1.37**/2Y1.87/self0.188/prod0.431）

**⇒ 净效果：算子 10→6（−40%），S 1.59→1.61~1.73，fit 1.20→1.21~1.37。两个目标同时达成。**

**本轮新增的 4 条经验**：
1. **C11 是首个「双赢」压缩**（省 2 算子且提 S）—— 因为比率归一化稀释了水平变化信号
2. **C5 在「限速器外 → winsorize 内」的层叠结构里可无损删除**（8→7 逐位相同）
3. **C12 反例**：`multiply` 里的 `rank` 是必需项，删了会崩（1.57→0.61）
4. **平台 `operatorCount` 与本 skill 的 `op_count.py` 正则计数逐位一致**（同一表达式两处都报 7 / 6）
