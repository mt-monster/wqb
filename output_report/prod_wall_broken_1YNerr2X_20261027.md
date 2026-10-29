# prod 墙突破：`1YNerr2X` 全闸通过（EUR 未点亮塔首例）

> 2026-10-27 23:13 ｜ EUR / delay1 ｜ 依据 `check_correlation` 平台实测

---

## 1 结论

`1YNerr2X` 是 **EUR 未点亮塔（FUNDAMENTAL，差 1 颗点亮）的第一颗全闸通过候选**，
`prod = 0.6896 < 0.70`，`self = 0.1820`，`FAIL 列表 = 空`。

```
group_neutralize(
    add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 2.1),
        multiply(0.7, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 2.1))),
    bucket(rank(cap), range="0,1,0.05"))
```

设置：`EUR / TOP2500 / delay 1 / decay 4 / FAST / trunc 0.08 / nanHandling ON / maxTrade ON`

---

## 2 平台判定（全部实测）

| 闸 | 值 | limit | 结果 |
|---|---:|---:|---|
| LOW_SHARPE | **1.87** | 1.58 | PASS |
| LOW_FITNESS | **1.02** | 1.00 | PASS |
| LOW_TURNOVER | 3.38% | 1% | PASS |
| HIGH_TURNOVER | 3.38% | 70% | PASS |
| CONCENTRATED_WEIGHT | — | — | PASS |
| LOW_SUB_UNIVERSE_SHARPE | **1.06** | 0.97 | PASS |
| IS_LADDER_SHARPE | **2.49** | 2.02 | PASS |
| MATCHES_PYRAMID | — | — | PASS（单数据集，ATOM 合规） |
| **SELF_CORRELATION** | **0.1820** | 0.70 | **PASS**（top1 = Grge2lN3 0.1820） |
| **PROD_CORRELATION** | **0.6896** | 0.70 | **PASS** |
| CLUSTER_TEST | 1.29 | 1.58 | WARNING（非 FAIL） |
| MATCHES_THEMES / OSMOSIS_ALLOCATION | — | — | WARNING |
| **FAIL 列表** | | | **空** |

returns **3.74%** ｜ drawdown 5.86% ｜ margin **22.14bp** ｜ TO 3.38%

---

## 3 破墙公式（两级杠杆，可加）

| 幂次 | cap 桶粒度 | **prod** | ≥0.7 对手数 | 0.5–0.6 | 0.6–0.7 |
|---:|---|---:|---:|---:|---:|
| 0.5 | 无 | 0.7971 | 15 | 8,210 | 556 |
| 1.0 | 无 | 0.7636 | — | — | — |
| 1.0 | 10 桶 | 0.7383 | 1 | 444 | 9 |
| 1.5 | 10 桶 | 0.7218 | 1 | 101 | 5 |
| 1.8 | 10 桶 | 0.7054 | 1 | 43 | 2 |
| **2.1** | **20 桶** | **0.6896 ✓** | **0** | **26** | **1** |

### 3.1 两个杠杆的分解与可加性

- **纯幂次**（0.5 → 1.0，无 cap）：−0.0335
- **纯 cap 中性化**（pow1.0，无 → 10 桶）：−0.0253
- 两者之和 0.0588 = 实测总降幅 ⇒ **完全可加**

### 3.2 关键机理：cap 桶不是「整体左移」，而是精准剪同源对手

从 pow1.0 起，`≥0.7` 的对手**恒为 1 颗**；prod 的继续下降**全部来自 0.5–0.7 区间收缩**
（pow0.5 的 8210+556 → pow2.1 的 26+1，收缩 **−99.7%**）。
即：`bucket(rank(cap))` 切的是 **size 通道上的同源对手**。

### 3.3 为什么能一路推幂次而不掉 S

两个杠杆对 S 的作用**相反**：
- 幂次 ↑ ⇒ 权重集中 ⇒ S ↓（1.73 → 1.49 → 1.31）
- cap 桶 ⇒ 去掉 size 暴露 ⇒ S ↑（+0.67）

两者对冲，S 稳定在 1.84–1.93，F 稳定在 1.00–1.07 ⇒ 可以一路推到幂次上限。

### 3.4 两条边界（实测）

| 边界 | 证据 |
|---|---|
| **幂次上限 = 2.1** | pow2.4 → F **0.96** ⇒ `LOW_FITNESS` FAIL |
| **桶粒度甜点 = 20 桶** | 5 桶 → F **0.98** FAIL；10 桶 → F 1.02；20 桶 → F 1.02（同） |
| **vbts 权重上限 = 0.75** | 0.80 → F **0.98** FAIL |

---

## 4 决定性否证：prod 是「结构签名」，与字段无关

| alpha | 主腿字段 | 结构 | **prod** | 计算时间 |
|---|---|---|---:|---|
| `1YNerr2X` | `bank_assets_investment` | pow2.1 + cap20桶 + 0.7×vbts | **0.6896** | 23:13:04 |
| `e75pkq7E` | `fnd23_intfvalld1_iabs` | **完全相同** | **0.6896** | 23:35:34 |

两次独立计算（间隔 22 分钟），直方图**几乎逐桶相同**（0.6–0.7 各 1 颗、0.5–0.6 各 26 颗）。

⇒ **换主腿字段 = 同一颗 alpha 的副本，只能算 1 席。**

这是 AlphaAgent (KDD'25, arXiv:2502.16789)「原创性 = AST 相似度」的实测印证：
`prod` 是**结构签名**，不是字段属性。

**由此得出硬结论**：
> 要拿 N 颗 alpha，必须有 **N 个不同的结构**，不是 N 个字段。
> 「一族只出 1 席」在 prod 轴上是字面成立的机制，不是经验规律。

### 4.1 同批 4 颗「换主腿」候选（全部 IS 全过，但只值 1 席）

| alpha | 主腿 | S | F | sub/lim |
|---|---|---:|---:|---|
| `e75pkq7E` | iabs | 1.87 | 1.02 | 1.06/0.97 |
| `wpQmKJKp` | iads | 1.86 | 1.01 | 1.04/0.97 |
| `mLo3wxw2` | fbds | 1.85 | 1.01 | 1.06/0.96 |
| `RRE3jkjd` | sebv | 1.84 | 1.00 | 1.04/0.96 |

---

## 5 新硬约束：cap 桶要求 `IS_LADDER ≥ 2.02`

引入 `cap`（非本数据集字段）会破 ATOM，从而**触发 `IS_LADDER_SHARPE` 闸**（替代 2Y 闸）。

| 数据集 | 加 cap 后 | 判定 |
|---|---|---|
| `fundamental23` | IS_LADDER **2.49** / 2.02 | ✅ 可用 |
| `techindi_model` | IS_LADDER **FAIL**（R1 三颗全 FAIL） | ✗ **不可用** |

`techindi_model` 保 ATOM 的版本（`j2YvXj09`，pow1.5，无 cap）：
S **1.90** / F **1.17** / 2Y **2.01** / sub 1.30-1.01 / **FAIL 空** ✅ —— 但它只能用幂次轴。

⇒ **cap 桶不是万能杠杆**：先查该集 ladder 强度，< 2.02 的集只能用幂次轴。

---

## 6 已试尽的路径（全部有实测数据）

| 杠杆 | 实测结果 |
|---|---|
| 幂次上移（论坛主推） | ✅ 有效 −0.0335（0.5→1.0），但压 S；上限 2.1 |
| cap 分桶中性化 | ✅ 有效 −0.0253，把 >0.6 对手砍 99.7% |
| universe → TOP800 | ✗ S **0.65**（信号靠小盘） |
| universe → TOP1200 | ✗ 平台 ERROR |
| neutralization → NONE / CROWDING / STATISTICAL / INDUSTRY | ✗ ERROR / S 0.95 / F 0.74 / S 1.04 |
| 动量分桶替代 cap 桶 | ✗ S **1.32** / F 0.69 |
| 波动分桶替代 cap 桶 | ✗ S **1.21** / F 0.57 |
| `vector_neut(动量)` | ✗ S **0.41**（价值信号与动量负相关，正交=减主体） |
| `vector_neut(波动)` | ✗ S 1.15 |
| `hump(x, 0.01)` | ✗ S **0.40**（TO 冻到 2.2%） |
| `trade_when(group_count>50)` | ✗ S **0.52** |
| 外层立方 | ✗ S 1.23 |
| 三腿 + cap 中性化 | ✗ 整批 ERROR |
| pow0.5 + cap 桶（4 种写法） | ✗ 平台 ERROR ×4 |
| truncation 0.04 | 0（S 1.93 / F 1.07 与 0.08 完全相同） |
| decay 变化（8/16） | 0（同日 sub 实验已证无影响） |

---

## 6.1 新增两条否证（23:50–00:40 实测）

### ① 幂次杠杆在 techindi 上**完全无效**（反升）

| pow | alpha | S | F | **prod** |
|---|---|---|---|---|
| 1.5 | `j2YvXj09` | 1.90 | 1.17 | **0.7276** |
| 1.8 | `omEp7Yqn` | 1.86 | 1.14 | — |
| 2.1 | `6Xd87ElJ` | 1.80 | 1.08 | **0.7336**（**+0.006**） |
| 2.6+ | | 1.71 → 1.46 | 1.00 → 0.79 | ROBUST FAIL |

对比 fund23 同一杠杆：0.7971 → 0.6896（**−0.1075**）。

**原因**：techindi 的 prod 由「恒 1 颗同源对手」决定（0.7–0.8 区间始终 1 颗），
幂次只改权重分布、不动对手关系；fund23 则同时有 size 通道上的成片对手可被剪。

**⇒ 幂次轴的适用条件（新判据，零仿真可查）**：
直方图必须有 A 型成分（`n(0.5≤x<0.6)` 上千）。若已是 B 型（≤100 颗），推幂次纯属浪费。

### ② 分组中性化的方向取决于「信号是否跨行业可比」

| 数据集 | 无分组 S | +subindustry | Δ |
|---|---:|---:|---:|
| `techindi_model`（跨行业预测模型） | 1.90 | **2.18** | **+0.28** ✅ |
| `fundamental23`（银行资产投资） | 1.87（cap版） | 1.36 | **−0.51** ✗ |

- **跨行业通用型**（预测模型、技术指标、情绪分）⇒ 行业内去均值 = 提纯，S ↑
- **行业集中型**（某行业科目，如银行资产）⇒ 行业内去均值 = 抹掉主体，S ↓

判法：该字段覆盖是否集中在单一 sector。集中 ⇒ 禁用分组中性化。

---

## 7 同族候选（IS 全过，等待 prod 队列）

| alpha | 构造 | S | F | sub/lim | FAIL |
|---|---|---:|---:|---|---|
| `O0AOj7Wg` | pow1.9 + cap10 桶 | **1.93** | **1.07** | 1.06/1.00 | 空 |
| `rKRYZjk1` | pow2.1 + cap20 桶 + vbts .75 | 1.85 | 1.01 | 1.04/0.96 | 空 |
| `2rAMo9p8` | pow2.1 + cap10 桶 + vbts .75 | 1.85 | 1.00 | 1.03/0.96 | 空 |
| `j2YvXj09` | techindi pow1.5（保 ATOM） | 1.90 | 1.17 | 1.30/1.01 | 空 ｜ **prod 0.7276 ✗** |
| **`N1NwwRAg`** | **techindi + `group_neutralize(subindustry)`** | **2.18** | **1.43** | 1.41/1.16 | 空 ｜ prod 待测 |
| `P0oWWOvE` | techindi + `group_neutralize(industry)` | 2.07 | 1.34 | 1.41/1.10 | 空 |
| `1YN99zoM` | techindi + `group_neutralize(sector)` | 1.93 | 1.21 | 1.33/1.02 | 空 |
| `N1N0dn97` | pow1.9 + cap5 桶 | 1.91 | 1.05 | 1.05/0.99 | 空 |
| `78LWpAmv` | pow1.9 + trunc0.04 | 1.93 | 1.07 | 1.06/1.00 | 空 |

---

## 8 产出盘点（对照「未点亮塔 × 10 颗」的目标）

| 塔 | 状态 | 已有可交付 | 缺口 |
|---|---|---|---|
| **FUNDAMENTAL**（差 1 颗） | **✅ 已达** | `1YNerr2X`（prod 0.6896 / FAIL 空） | 0 |
| OTHER（差 2 颗） | 待 prod | `j2YvXj09`（IS 全过，prod 队列中） | 1–2 |
| RISK（差 1 颗） | 未攻 | — | 1 |
| PV（差 2 颗） | 已标死 | `pv87`/`pv20`/`other455` 字段全弱 | — |
| NEWS / SENTIMENT / EARNINGS / INSIDERS / INSTITUTIONS / SOCIALMEDIA / IMBALANCE / MACRO | 0 颗（各需 3 颗点亮） | — | 3×8 |

**「10 颗」的现实约束**（本次新证）：需要 **10 个不同结构**，不是 10 个字段。
当前手里只有 **1 个可复制的结构模板**（幂次 2.1 + cap 20 桶 + 辅腿），
它在一个数据集上产出 1 席。

---

## 9 下一步（按证据强度排序）

1. **敲定 OTHER 塔**：`j2YvXj09`（保 ATOM、无 cap、pow1.5）的 prod —— 队列一空即查。
2. **为 cap 桶模板寻找第二个可用的数据集**：条件是 `IS_LADDER ≥ 2.02`（fund23 是 2.49）。
   需要先对候选集做 ladder 体检，避免像 techindi 那样加完 cap 才发现 ladder 不够。
3. **新结构轴**（各值 1 席，不能靠字段翻倍）：
   - 分组轴换成 `sector`/`industry` 的 `group_scale`（保 ATOM，不破 ladder）
   - 时序门控 `trade_when`（今日测的 `group_count>50` 失败，但阈值/条件可换）
   - 残差化 `ts_regression`（memory §4 记有 4-op 地板模板）

---

## 10 出处

| 内容 | 来源 |
|---|---|
| 幂次 3 次方降 PC 0.9→0.64 | BRAIN 论坛《最全 Product Correlation 攻略》YL61874 评论 |
| `hump` / `vector_neut` / `trade_when` "降 correlation 有奇效" | BRAIN 论坛《网络中心度 SCC》 |
| 残差动量降低波动、提高 Sharpe | Blitz, Huij & Martens (2011) |
| beta 中性残差跨区域互相关更低 | AEA (2023) |
| 原创性 = AST 相似度 | AlphaAgent, KDD'25, arXiv:2502.16789 |
