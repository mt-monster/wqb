# GBR 挖掘经验总结（2026-10-09 → 10-10，含全部实测证据）

> 产出一颗已提交 alpha（`3qVP6pNO` GBR/D1/OTHER ACTIVE）+ 一套可复制的方法论。
> 本文件是「以后再挖新区/新战役」的操作手册。

---

## 一、信号发现层

| # | 经验 | 证据 |
|---|---|---|
| 1 | **description 是唯一语义依据**，字段名会骗人（9.5% 名字/描述冲突） | `short_term_price_change` 实为 Williams %R；`cumulative_money_flow_volume_adjusted` 实为 RSI；`*_pd_pct`（像 ratio）实为 probability of default |
| 2 | **`coverage = 0.00` 是「未采集」不是「不可用」** —— 判据失真会埋掉整片机会 | `model38` 全字段 cov=0 却含 9 个 ALIVE；techindi 因此从 UNUSABLE 池复活并产出首颗提交 |
| 3 | **已测字段的命中率不能外推未测池**（选择偏差）；估未测池产出率只能实测抽样 | 同日内两次栽同一坑：`score` 被未测数量误导、`count` 被已测命中率误导 |
| 4 | **「单骨架判死」= 低置信，不是终局**；但实测复活率也只有 2.1%（GBR WEAK 池）—— 多样性的价值在「置信度分级 + 排除嫌疑」 | 3a 复活补测 89 条实测 |
| 5 | **算子对账必须做**（平台 102/REGULAR 83，含 genius 分级）；「单调变换前置皆 no-op」（末端是 group_rank 时 signed_power/log/sqrt 全无效） | genius 17 算子补测 + 三波对账 |
| 6 | **字段名必须取平台实时值**（本地目录会错） | other455 本地 `_va` vs 平台 `_value` 整批被拒 |

## 二、骨架与结构层

| # | 经验 | 证据 |
|---|---|---|
| 7 | **字段画像（sem_type）决定骨架族**；不同字段配不同族 | 实测矩阵：delta 在 6 类语义上最强；count 最强形态是「对偶字段差」subtract(rank,rank)=1.96 |
| 8 | **双窗合成 `add(ts_mean(1), ts_mean(60))` 是 techindi 类信号的利器**（合规五形态之一） | 把 S 从 1.47 → 1.59 |
| 9 | **`group_neutralize` 施于「原始信号」> 施于加工后** | S 1.59/2Y1.90 vs 0.96–1.43 |
| 10 | **「零余量通过」是危险信号**（F 恰好压线 ⇒ 无法在保住过闸的前提下降 prod） | techindi decay2 F=1.00 锁死事件 |
| 11 | **发批七闸**：值型/VECTOR/元数/算子清单/权重和/**骨架两级（波级+字段级）**/字段实时存在性 | 本日拦下我 3 次违规波 + 1 个非法算子 |

## 三、prod 与提交层（本战役最大沉淀）

| # | 经验 | 证据 |
|---|---|---|
| 12 | **宣布 prod 死锁前，必须先扫「中性化全档 × tvr 梯子」**（GBR 合法 11 档） | SECTOR/INDUSTRY/MARKET/SUBINDUSTRY 全 2Y 塌；**CROWDING×techindi 全闸且 prod 0.7644→0.6707** |
| 13 | **prod 拥挤是「机制级」的**（池里全是同类信号时，换任何中性化档都不脱钩） | analyst7 FAST 档 S 冲到 1.98 但 prod 0.81–0.87 纹丝不动 |
| 14 | **CROWDING 只救「池里稀缺」的信号，且会杀死「本身就是拥挤因子」的信号** | techindi 得救；analyst47 情绪 S1.96→0.3、analyst69 E/P S1.11→0.25 被杀 |
| 15 | **同族 self-corr 0.88–0.94 ⇒ 一条腿只能出 1 颗**；候选池的「颗数」按腿数算，不按表达式数 | compute_mutual_correlation 实测 |
| 16 | **提交链**：RA=0 → robustness PASS 落台账 → prod refresh 复核 → 配额 → 三段式 ≥100 词描述 → POST → 验 ACTIVE+dateSubmitted | 3qVP6pNO 全程 36s 从 POST 到 ACTIVE |
| 17 | **prod 会漂移（>48h 不可信）⇒ 提交前必须 `refresh=True` 复核** | 写入纪律 |

## 四、判断「卡死」的六类形态（每类都有实测）

A prod 墙（IS 全过、prod>0.70）｜ B 2Y 塌（IS 强、2Y≪1.58）｜ C 低于闸线（S/F 不足）｜
D 2Y 稳 S 弱（换量纲复访）｜ E 同语义反向（同量型同骨架方向翻转，如 ent vs pre）｜
F 未测池整体无信号（抽样扫测证明）

## 五、对「10 颗可提交」的实操结论

- **可提交数按「腿」算不按「表达式」算**（同族 self-corr 限 1 颗）；
- GBR 的天花板在 prod 而不在信号强度：**先按机制新颖度选池（避开 analyst 修正 / pv 反转 / 技术裸动量），再谈优化**；
- 每颗候选拿到后**必须做极致优化**（tvr×窗×winsorize×decay×轴 全梯扫到平台期）——本次把 S 从 1.72→1.86、2Y 1.86→2.05、prod 0.6898→0.6707。
