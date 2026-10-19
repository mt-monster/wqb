# KOR 算子穷举矩阵（Operator Exhaustion Matrix）

> **本文回答一个问题**：破闸所需的算子到底试过哪些、哪些没试、为什么没试、每个的结果与淘汰原因。
> 与 [`_field-profile-and-templates.md`](_field-profile-and-templates.md)（字段侧）配成一对：
> **那个文档管「用什么字段」，本文管「用什么算子」。**
>
> 数据来源：KOR/TOP600/D1 战役全量台账（`results/mining_ledger/alpha_ledger.jsonl`，545 行，
> 约 230 次仿真，18 个数据集）。**所有 S/F/TO/2Y 均为平台实测值。**

---

## 0. 先给结论（如果不看正文）

1. **算子穷举不能弥补机制强度不足。** 当前所有未封死候选的 S 都在 0.58–1.09，
   而闸线 1.58。以 `earnings3` 为例，TO 0.07 时 `F = S×√(8×returns)` ⇒ 要 F=1.0 需
   **S ≈ 1.75**，即需从 0.83 提 0.92 —— **没有任何单算子族能给 0.9 S**。
2. **真正有杠杆的算子只有 4 个**：`ts_target_tvr_decay`、`ts_backfill`、`signed_power`（幂次）、`tail`。
   其余算子的作用是**保持形态**或**破坏形态**，不是创造 S。
3. **已被实测证否的算子族有 6 组**（见 §3），命中即省一次仿真。

---

## 1. 本轮实际用过的算子（按族）

| 族 | 算子 | 用法 | 是否产生过正向效果 |
|---|---|---|---|
| **Time Series** | `ts_target_tvr_decay` | 精确压换手到 target | ⭐ **是（最大杠杆）**：shortinterest 腿 S 1.91→**2.09**、TO 0.55→0.22、F 0.81→**1.44** |
| | `ts_backfill` | 补 NaN，扩可交易集 | ⭐ **是**：prod 0.6991→0.6955、S 0.81→1.60（同一腿） |
| | `ts_delta` | 取变化率（铁律 A） | ⚠ 部分：institutions |S| 0.79（最佳）、但 earnings 上 0.33 < 0.81 |
| | `ts_mean` | 时序平滑 | ⚠ 弱：earnings 上 0.70（劣于 rank 0.81） |
| | `ts_rank` / `ts_zscore` | 时序标准化 | ❌ 见 §3 |
| | `ts_decay_linear` | 线性衰减 | ❌ 见 §3 |
| | `ts_std_dev` | 波动归一化分母 | ⚠ 仅作分母（分歧度族），单用无效 |
| | `hump` | 抑制换手 | ❌ **极敏感**：0.0025→S 1.91；0.006→S 0.91 |
| | `days_from_last_change` | 新鲜度门控 | ❌ S 0.63 |
| **Cross Sectional** | `rank` | 横截面排序 | ⭐ 基础必需 |
| | `winsorize` | 尾截断 | ⭐ **是**：它是**抑制 prod 的承重部件**（删掉 prod 0.6991→0.7626） |
| | `quantile` | 分布变换 | ≈ no-op（保序） |
| | `zscore` / `normalize` / `scale` | 归中/缩放 | ❌ 保序，对 prod 无效（见 §4） |
| | `vector_neut` | 对规模正交 | ⚠ 双刃：imb5 上 S 1.09→0.86（剥掉了真 alpha）；全正交会剥空信号（1.20） |
| **Group** | `group_rank` | 组内排序 | ⭐ 基础必需（`sector` 轴最优） |
| | `group_neutralize` | 组内去均值 | ⚠ 内层用（`subindustry`）在部分腿有效，在 analyst 腿有害 |
| | `group_zscore` | 组内 z | ❌ **灾害**：earnings 上 S **0.03** |
| | `group_backfill` | 组内填充 | ❌ S 1.03 + **UNITS 硬警告**（要求 Unit[]，带量纲须先 rank） |
| **Transformational** | `tail` | 收紧尾部 | ⭐ **是（小）**：earnings S 0.81→**0.83**、2Y 1.37→1.38、invest 0.71→**0.82** |
| | `trade_when` | 事件门控 | ⚠ 双刃：分析师腿 +0.10 S；shortinterest 腿 **−0.31 S、−0.13 2Y**（且破坏 ATOM） |
| | `bucket` | 自定义分桶 | 未用（见 §5） |
| | `densify` | 组压缩 | 未用 |
| **Arithmetic** | `signed_power` | **幂次** | ⭐ **是（第二大杠杆）**：prod 单调降 0.6861→0.6646→0.6571（2.5/3.5/4.0） |
| | `subtract` | 同源双腿价差 | ⭐ 合规净额结构（institutions 净额、权重变更） |
| | `add` / `multiply` | 拼腿 | ❌ **禁**（闸 5 `POISON:equal_weight_leg_add`） |
| | `divide` | 分歧度分母 | ⚠ IND 有效、**KOR 上 S 1.20**（coeff_var 覆盖 0.5754 太低） |
| | `log` / `sqrt` / `inverse` / `abs` / `sign` / `power` | 标量变换 | 未系统用（见 §5） |
| **Logical** | `greater` / `less` / `not` / `is_nan` | 条件 | ⚠ `is_nan` 门控 S 0.84 |
| | `if_else` | 覆盖过滤 | ⚠ IND 上 prod 0.73→0.6664；KOR 未系统用 |
| **Vector** | `vec_avg` / `vec_sum` | VECTOR 降维 | ⭐ 必需（VECTOR 字段必先降维） |
| **Setting（不占算子）** | `decay` / `truncation` / `nan_handling` / `neutralization` | 仿真旋钮 | ⚠ `decay` 只动 TO、`truncation` 零杠杆（逐位相同）、`nan OFF` 摧毁信号、中性化档逐族实测 |

---

## 2. 闸 → 算子映射（哪个闸该用哪个算子）

| 闸 | 首选算子 | 实测幅度 | 备注 |
|---|---|---|---|
| **LOW_SHARPE** | `trade_when` 门控（跨集则牺牲 ATOM）、`ts_backfill` 扩覆盖 | +0.10~+0.79 | 无单算子能给 +0.5 以上 |
| **LOW_FITNESS** | `ts_target_tvr_decay`（压 TO） | F 0.81→**1.44** | ⭐ 最强 F 杠杆 |
| | `tail` | F 0.46→0.48 | 小幅但稳定 |
| **IS_LADDER / 2Y** | **无有效算子** | — | 2Y 由字段的时序内容决定（见 F-6） |
| **LOW_SUB_UNIVERSE** | `tail` / 扩覆盖 | invest 0.71→0.82 | 间接 |
| **PROD_CORRELATION** | `ts_backfill` 改可交易集 | 0.6991→0.6623（最低） | 保序变换全部无效 |
| | `signed_power` 幂次 | 单调降 | 第二杠杆 |
| **SELF_CORRELATION** | **无算子可解** | — | 只能换数据集（同集兄弟 0.80–0.99） |
| **CONCENTRATED_WEIGHT** | `tail` / `signed_power`（降幂） | — | 降幂会同时降 S |

---

## 3. 已实测证否的算子族（命中即禁入，省一次仿真）

| # | 算子 / 用法 | 实测结果 | 机理 |
|---|---|---|---|
| **O-1** | `group_zscore` 替代 `group_rank` | earnings3 上 **S 0.03**（vs 0.81） | 输出无界，尾部股票权重失控 |
| **O-2** | `hump` 控换手 | 0.0025→S 1.91；**0.006→S 0.91** | 无中间档，非线性断崖；且 TO<0.15 时**反升 prod**（0.7008→0.7331） |
| **O-3** | 保序变换改 prod（`quantile`/`normalize`/`zscore`/`scale`/换分组/缩窗） | prod 钉在 **0.6989–0.7081** | PC 比的是 **PnL 曲线形状**，保序变换不改每日排序 ⇒ 形状不变 |
| **O-4** | `group_backfill` | S 1.03 + **UNITS 硬警告** | 要求 index 0 为 `Unit[]`；带量纲字段必须先 `rank`；且填法太粗伤信号 |
| **O-5** | 时序平滑 `ts_mean` / `ts_decay_linear` | earnings 0.70（vs 0.81）；shortinterest 上 decay4 把 2Y 打到 0.93 | 累积型信号上平滑是零和：降 TO 同时削 alpha |
| **O-6** | 全正交 `vector_neut(·, 高相关同族)` | S 1.60→**1.20** | 剥掉共同成分后信号所剩无几 |
| **O-7** | **`trade_when` 门控用在「全横截面排序型」信号上** | analyst44 基线 S 1.45 → 广度门控 **0.96**（多空 230/398→205/211）→ 分歧度门控 **0.61**（→173/219） | **任何门控都会削窄截面 ⇒ 排序宽度不足 ⇒ 单调性瓦解**。广度门控还有第二重错：**带方向性**，把空头腿（负广度股）一并砍掉，非对称收益消失 |

> **★ 门控的适用边界（2026-07-20 实证）**：
> **rank-based 全截面排序型信号 ⇒ 禁门控**（S 来自整个截面的单调性，削窄即崩）；
> **event-based 稀疏事件信号 ⇒ 必门控**（不稀疏时不该持仓，如 shortinterest 腿）。
> 用门控前先判信号类型，不要默认「加个正交维度总有好处」。

---

## 4. 论坛 + 论文交叉引用（外部取证结论）

| 来源 | 结论 | 与本区实测是否一致 |
|---|---|---|
| BRAIN-CN《降低 Alpha 的 Prod Correlation》+ 评论 ZZ47696（GLB 实测） | 保序变换只能让 PC 在 **0.6996–0.709** 抖动 | ✅ **几乎逐位重合**（我们 0.6989–0.7081） |
| 同上（闭式） | 掺腿稀释 `PC_c=(a+wb)/√(1+w²+2wρ)`，ρ≈0 时极值点是**极大值** `√(a²+b²)` ⇒ 掺入腿 PC 必须 **<0.3** | ✅ 我们唯一的短腿 0.4631 按公式会**抬高** PC |
| 同上 | 同内核兄弟变体集体撞 SELF ⇒ 一个内核只能交一条 | ✅ 实测 y1×y2 **0.8378**、同字段换结构 **0.9936** |
| Blitz–Huij–Martens (2011) residual momentum | 残差收益**持续** ⇒ 动量 | ❌ **KOR 相反**：66d 残差动量 S **−0.60**，是**反转** |
| Amihud 非流动性溢价 | 高价差 ⇒ 高预期收益 | ❌ **KOR 无效**：`pv106` 价差变动 S 0.38、TO 0.45（纯噪声） |
| 指数纳入效应（price pressure） | 纳入后短期涨、随后反转 | ⚠ 未能验证：`macro63` 横截面**零方差**（无 KOR 成分股）；`other106` 多空 136/463 失衡 |
| PEAD（财报后漂移） | 惊喜方向决定漂移 | ⚠ **无法验证**：`earnings3` **只有日期无 surprise 数值**，只能做新鲜度（S 0.83） |

---

## 5. 尚未覆盖的算子与「为什么暂不覆盖」

| 未覆盖算子 | 目标闸 | 为什么暂不覆盖 | 何时才该用 |
|---|---|---|---|
| `ts_arg_max` / `ts_arg_min` | S | 输出是「距极值天数」，与 `ern3_pre_interval`（本身即天数）语义重叠，预期冗余 | 换到有「幅度」字段的数据集时 |
| `ts_corr` / `ts_covariance` | S | 需要**第二条同数据集时间序列**；当前候选集多数只有一个信号字段 | 遇到多字段同集（如 analyst_consensus 300 字段）时 |
| `ts_product` / `ts_kurtosis` | S | 累积/尾形对「0–1 评分」「天数目」类字段无经济含义 | 收益率序列类字段 |
| `kth_element` / `last_diff_value` | 覆盖 | 与 `ts_backfill` 同属覆盖修补，后者已实测有效且更简单 | backfill 出现覆盖副作用时 |
| `bucket` | S | 需要**同数据集规模字段**做桶轴；仅 `imbalance5`/`institutions6` 具备 | 该两类数据集复活时 |
| `densify` | 分组效率 | 只影响计算，不改信号 | 大宇宙（TOP3000+） |
| `if_else` 覆盖过滤 | prod | KOR 未系统测；IND 实测有效（0.73→0.6664）但**本区无第二腿可过滤** | 候选已进 prod 墙阶段 |
| 标量族 `log`/`sqrt`/`inverse`/`sign`/`abs` | 分布 | 均为**保序或近保序** ⇒ 按 O-3 对 prod 无效；对 S 只改权重尾部 | 仅在与 `signed_power` 组合做权重实验时 |

> **⚠ 上表是「有理由的不覆盖」，不是「已穷尽」。** 一旦出现新候选（S ≥ 1.4），
> 这些算子必须逐个消融 —— 因为那时**算子才可能成为边际变量**。

---

## 6. 判据：什么时候才值得做算子穷举

按 skill ⑤ 的前置条件，算子穷举**只在同时满足**下列两条时才值得投入：

1. **IS 已全过**（或只差 1 闸且缺口 < 0.1）；
2. 缺口在 **F / CW / sub / invest** 这类**权重与换手相关**的闸，而不是 S / 2Y。

**反例（本轮现状）**：`earnings3` S 0.83，2Y 1.38，TO 0.07。
- 缺口 0.75 在 **S**，不在权重闸 ⇒ 属机制强度问题；
- TO 0.07 < 0.125，`F = S×√(8×ret)` ⇒ F=1.0 需 **S≈1.75**；
- ⇒ **算子穷举在此处数学上不可能补上**，应回 ②组装换机制，而非在 ⑤ 死磕。

**这条判据本身是本轮最有价值的产出**：它把「算子穷举」定位为一个**收尾步骤**，
防止在机制不足时把配额烧在算子层。
