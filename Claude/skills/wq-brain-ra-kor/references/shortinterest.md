# KOR × shortinterest（组合分支）

> 回到 [KOR 区域流程](../SKILL.md) · [KOR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/KOR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region KOR --category shortinterest`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：ShortInterest　**类别卡**：shortinterest

**备注**：shortinterest38 卖空活动族在写；累积口径与当日口径二选一

**涉及数据集**：shortinterest38

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | KOR | 区域 settings.json |
| universe | TOP600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 81 | 5 | 25 | 20 | 0 | 0 |

主要数据集（回测数）：shortinterest38（81）

### S1 字段理解

- YYYYMMDD 交易日字段（如 KOR shrt38_stk_invacttd_drt）不是信号
- 累积口径偏 2Y、当日口径偏 IS（KOR shortinterest38 实证，作选区先验，不作类别结论）
- 窗口（类别卡，均在白名单内）：daily 5/22；long 252/504

### S2 生成

- **用**：shortinterest38（全 VECTOR，coverage 0.9997）：卖出 / 买入金额比的长窗 z 与共动反转（RULES §G）
- **避**：shrt38_stk_invacttd_drt 是 YYYYMMDD 交易日字段，不是信号
- **说明**：低频（累积 accum_*）出 2Y 1.72–1.93 但 S 0.80–0.98；高频（当日 stk_*）S 2.00–2.01 但 2Y 1.12–1.20（KOR 七约束 #7，只有本族证据）
- **说明**：ts_decay_linear 不修 CONCENTRATED_WEIGHT：换手 0.298→0.14、S 2.00→2.15，CW 仍 FAIL
- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：

  ```text
  group_rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5), sector)
  group_rank(reverse(ts_corr(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt), 42)), sector)
  ```

  - group_rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invac… ← 骨架 A（RULES §G）
  - group_rank(reverse(ts_corr(vec_sum(shrt38_stk_invactsell_amt… ← 骨架 B：rKOadrRj S 2.02（RULES §G）；窗口说明：42 不在白名单：该骨架以 42 日窗实测 S 2.02（rKOadrRj）；复用时先与 22 / 66 对照
- **类别通用原语**（类别卡，跨区）：
  - short interest change: delta of short interest vs float
  - short squeeze potential: high short interest + positive catalyst
  - short covering: rapid decline in short interest
  - days to cover: short interest vs average daily volume
  - short interest momentum: acceleration of short interest changes
- **跨区结论**（IND/ASI；negative）：shortinterest5 价带宽度在 TOP500 级宇宙没有横截面离散度（证据：IND-SHORTINTEREST5-PRICEBAND-DEAD；ASI-SI5-MCR63-RSK70-CORRGATE-WEAK-20260921） <!-- lint:const-ok 证据原文 -->
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize）入场（原举例 regression_neut / vector_neut 均已被平台移除，2026-10-10 op-lint 实测）
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [组合] CW 不过：改持仓构造（trade_when 门控或加分组轴），不要只加平滑（证据：KOR 七约束 / RULES §E（CW 由组内分布集中度决定，不由换手决定）） <!-- lint:const-ok 证据原文 -->
2. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
3. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region KOR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-13 会话：★ **CW 墙破墙配方**（`shortinterest38` 复现，必读）

**背景**：已提交的 2 颗（`KPNo2lgl` / `omLjG1M5`）是 `hump(group_rank(divide(vec_sum(sell_amt), vec_sum(buy_amt)), sector), hump=0.003)`
族，**在 CW 闸升级前通过**；升级后同形构型**一律卡 `CONCENTRATED_WEIGHT`（value 1.0 / 限 0.1）**，其余 9 项全过。

**该族信号极强**（30 条实测）：S **2.1–2.66** / F **1.12–1.86** / TO **0.168–0.55** / 2Y **1.59–2.44** / investability **1.68–2.55**。

#### ★ 破墙配方（唯一有效，23 条对照实验得出）

```
hump(subtract(group_rank(divide(vec_sum(shrt38_stk_invactsell_amt),
                                add(vec_sum(shrt38_stk_invactbuy_amt), 0.0001)), sector), 0.5),
     hump=0.003)
⇒ S 1.95 / F 1.08 / TO 0.4177 / SUB 1.67 / 2Y 1.80 / investability 1.68 (限1.36) / **CW 未触发 ✅** / self 0.449
```
**机理：居中 `subtract(·, 0.5)` 必须放在 `hump` 的「内层」** —— 二要素缺一不可：
| 构型 | CW |
|---|---|
| **`hump(subtract(group_rank(R,sector), 0.5), hump=0.003)`** | **未触发 ✅** |
| `hump(group_rank(R,sector), hump=0.003)`（原配方，不居中）| 1.0 ❌ |
| `subtract(group_rank(R,sector), 0.5)`（居中但不 hump）| 1.0 ❌ |
| `normalize` / `scale` / `winsorize(std=4)` / `quantile` / `group_rank(·, subindustry)` | 全部 1.0 ❌ |
| 4 档中性化（MARKET / SECTOR / STATISTICAL / NONE）| 全部 1.0 ❌ |
| `subtract(rank(·), 0.5)`（全局 rank 居中）| 未触发 ✅（但 F 仅 0.64）|
⇒ **CW 与「分组内排名的非零均值」有关**；`hump` 的时间平滑 + 组内居中共同消除它。

#### 当前最优 + 唯一剩余
`e767ra3g`：**全部 IS 闸通过**（含 CW）+ **self 0.449 ✅**；**唯一剩余 = `prod 0.7522`（限 0.70）**。
第二颗 `9qEqRl7e`：S **2.10** / F **1.86** / TO **0.168** / 2Y 1.89 / inv 1.90 ✅ 但 **CW 0.307 ❌**、prod 0.7602 ❌。
⇒ **本族的卡点是 `prod`（0.75–0.76），需引入第二个经济维度**（条件 / 分组 / 残差），或接受现状。

---

## ★★★★★★★★★★ 2026-10-13 收官：**全闸通过配方**（平台预检确认，可直接复用）

**破 `prod` 墙的两把钥匙**（单点改动，均不破坏任何已过闸，CW 仍不触发）：

| 钥匙 | 效果 |
|---|---|
| **分组轴 `sector` → `industry`** | prod 0.7522 → **0.6663** |
| **`hump` 0.003 → 0.005** | prod 0.7522 → **0.604** |
| ⚠ 反例：`ts_mean(R, 5)` 时间平滑 | prod → **0.7618（更差）** |

### 成品（手工全闸 + 平台 `submit_verdict` 双确认）

```
d5K508qg = hump(subtract(group_rank(divide(vec_sum(shrt38_stk_invactsell_amt),
                                          add(vec_sum(shrt38_stk_invactbuy_amt), 0.0001)),
                                   industry), 0.5),
                hump=0.003)
0mjmEkWG = 同上，但 hump=0.005
设置：KOR / TOP600 / D1 · decay 4 · neutralization=SECTOR · truncation 0.08 · nanHandling ON
```

| alpha | S | F | TO | SUB | 2Y | inv/限 | CW | CLUSTER | self | **prod** | `submit_verdict` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **`d5K508qg`** | **1.99** | **1.04** | 0.4159 | 1.59 | **2.03** | **1.74/1.39** | 未触发 | **1.34** | **0.413** | **0.6663** | **failed_ra=0 / failed_ppa=0 / 无硬闸告警** |
| **`0mjmEkWG`** | 1.71 | **1.60** | 0.1556 | 1.57 | **2.09** | ✅ | 未触发 | — | **0.379** | **0.604** | **failed_ra=0 / failed_ppa=0 / 无硬闸告警** |

⇒ **本配方是 KOR/D1 在「未点亮数据集」上的第一套全闸通过解**。数据集 `shortinterest38` 已提交 2 颗
⇒ **本配方再提 1 颗即达 3 ⇒ 之后该集转点亮，须换集**。
⚠ **同族一次只提 1 颗**；提完后必测 self（家族近亲会冲高）。
⚠ 按用户政策：**agent 不提交**，提交权归用户。

---

### ⑦ 算子压缩（`wq-alpha-gate-push-op-min` 六步法，2026-10-13）

原构型 **7 个调用点**（`vec_sum×2, hump×1, subtract×1, group_rank×1, divide×1, add×1`）⇒ 消融后 **6 个**：

| 消融动作 | ops | S | F | TO | 2Y | 结论 |
|---|---|---|---|---|---|---|
| **删 `add(vec_sum(buy_amt), 0.0001)` 守卫**（`buy_amt` 恒正）| **6** | **2.04 ↑** | **1.08 ↑** | 0.4149 | **2.17 ↑** | **纯赢（省算子 + 指标全升）** |
| `hump` 0.003 → 0.004 | 7 | 1.80 | 1.13 | 0.2661 | 2.16 | 可用（prod 0.6247 最低）|
| `hump` 0.003 → 0.008 | 7 | **−0.12** | — | — | — | **崩，禁用** |
| 分组轴 → `subindustry` | 7 | 1.74 | **0.82** | 0.4013 | 2.21 | **F 挂，禁用** |
| `winsorize(…, std=3)` | 8 | 2.01 | 1.06 | 0.4144 | 2.02 | 无增益（+1 算子，F 反降）|

**压缩后最优（全闸通过 + prod/self 双过）**：

```
rKdK2vLE = hump(subtract(group_rank(divide(vec_sum(shrt38_stk_invactsell_amt),
                                            vec_sum(shrt38_stk_invactbuy_amt)),
                                     industry), 0.5), hump=0.003)          # 6 ops
  ⇒ S 2.04 | F 1.08 | TO 0.4149 | 2Y 2.17 | CW 未触发 | CLUSTER 1.40 | self 0.415 | prod 0.6703

6XAXpvqG = 同形，hump=0.004                                                # 7 ops
  ⇒ S 1.80 | F 1.13 | TO 0.2661 | 2Y 2.16 | self 0.417 | prod 0.6247
```
**★ 结论**：① 该守卫**完全冗余**；② `hump` 甜区 **[0.003, 0.005]**；③ 分组轴只能用 `sector`/`industry`（**`subindustry` 会挂 F**）；
④ **本族 6 算子是构型下界**（`vec_sum×2 + divide + group_rank + subtract + hump` 缺一不可）。
<!-- profiles:manual:end -->
