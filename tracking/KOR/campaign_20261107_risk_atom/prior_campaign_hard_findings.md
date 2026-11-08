# 先行战役硬结论清单（2026-11-06 final_report 全文提取 · 本战役直接复用）

## A. 已验证的杠杆与死轴（勿重复）

### A1. `winsorize(std)` 是本族 **S 主杠杆**（单峰）
| std | 0.24 | 0.32 | 0.36 | **0.38** | 0.42 | 0.46 |
|---|---:|---:|---:|---:|---:|---:|
| S | 1.49 | 1.59 | 1.63 | **1.62** | 1.58 | 1.50 |

- 甜区 **0.34–0.42**；`pow` 甜区 **1.5–3.0**；pow>4.0 / std>0.44 判死。
- ⚠ **prod 对 std 极敏感**：std .36 → prod **0.7002 FAIL**；std .38 → **0.6898 PASS**。0.01 量级决定过闸 ⇒ **同族必须逐颗实测 prod，不能外推**。

### A2. `vector_neut` 正交腿效应（我 R11 踩坑点）
- 对 **momentum** 正交：**+0.06 ~ +0.30**（有效）
- 对 **resvol** 正交：中性（无增益）
- 对 **size / beta / ltrevrsl** 正交：**直接归零（死轴）**
- ⇒ R11 里 size / beta / ltrevrsl 三腿大概率归零，仅 btop / earnyild / srisk / indmom 有信息量。

### A3. 明确死轴（byte-identical / 更差，勿再扫）
- `decay`：**0 与 1 逐位相同**，2 更差 ⇒ decay 是死轴（我前几波用的 4 也是无效档）
- `ts_backfill` 窗口：**22 / 40 / 55 逐位相同** ⇒ 死轴
- 内层分组细于 sector：死轴
- `ts_rank` 时序分位**单独用**：0.74（但与「正交 + 分位」叠加可用）
- pow > 4.0 / std > 0.44：死
- risk88 `ri_*` 在 R&M 档：全族弱
- risk59 借券域在 CROWDING 档：0.41（弱）

### A4. 中性化档效应量（KOR risk70 载荷族，第 2 次独立复现）
**REVERSION_AND_MOMENTUM 1.63 > CROWDING 1.30 > INDUSTRY 1.14 > FAST 1.07 > SLOW 1.04 > STATISTICAL 0.88**
- ⇒ 我的 R2/R4/R7/R8 全部跑在 STATISTICAL（**最差档 0.88**）⇒ 这解释了为什么我的风险量族只能到 S 1.24。

## B. anlystsn 强轴的天花板（决定了「10 颗都过 S>=1.58」不可行）
- anlystsn（aC 2922）在 R&M 下 S 1.62 是**唯一**过 1.58 的载荷轴。
- 同族 10 个参数变体：**prod 落在 0.62–0.87 且族内互相关 > 0.95**。
- 已被 prod 撞墙排除的同族变体：E56Nk0wL prod **0.7002**、YP18Gpel **0.8083**、wpQ3wP8Y prod 0.62 但**互相关 0.7731 vs omERn83n**。
- ⇒ **强轴最多留 1 颗代表 + 1 颗不同分位件**。

## C. prod 已 FAIL 的字段轴（直接排除，勿再派）
| 字段 | prod | 结论 |
|---|---:|---|
| risk70 `btop` | **0.7322** | FAIL |
| risk70 `earnyild` | **0.8383** | FAIL |
| risk68 `weight_edadv/dadv` 分位 | **0.7731** | FAIL |
| anlystsn − newssent（CROWDING） | **0.8688** | FAIL |
| risk59 借券 hump 变体 x3 | 互相关 0.78/0.92/0.999 vs QPvr1vPM | 结构冗余 |

⇒ **我 R10 里的 earnyild / btop 两槽是浪费**（已知 prod FAIL）；其余 6 槽（growth / invsqlty / profit / earnqlty / divyild / newssent）仍未探索，有效。

## D. 干净的补位机制（prod 低）
- 非 anlystsn 载荷：growth **0.5762** / ri_growth **0.5909** / ri_divyield **0.6292** / shortint **0.6555** / ri_momentum 反向 **0.3837**
- 借券 + 残差几何（hump / quantile / 双 rank）：mLoJrQrW prod **0.2439** / self 0.0986，与载荷族最大互相关仅 0.1377
- ⇒ **候选池应由「非 anlystsn 机制」撑起**（先行战役原话）。

## E. 结构性判定（必须向用户说清）
**KOR Risk 单数据集上，「10 颗各自 S>=1.58」结构性不可行**：
- 只有 anlystsn 一条轴过线；同族变体互相关 >0.95 且 prod 0.62–0.87，无法用 10 个变体凑池。
- 其余轴（载荷非 anlystsn / 借券 / 残差 / 风险量）实测天花板 S 0.4–1.24。
- 先行战役按用户澄清口径已交付：**10 颗池，self max 0.4247 / prod max 0.6898 / 池内互相关 max 0.6007**，其中 1 颗 S>=1.58。
- 本战役交付应沿用同一口径，并**明确标注**哪几颗满足 S>=1.58。

## F. 我 R10 / R11 的浪费统计（诚实记账）
- R10（8 槽）：earnyild、btop 已知 prod FAIL ⇒ **2 槽预知浪费**；6 槽有效。
- R11（8 槽）：size、beta、ltrevrsl 已知归零 ⇒ **3 槽预知浪费**；resvol 中性 ⇒ 再 1 槽低信息；4 槽有效。
- 教训：**开波前必须先读先行战役的排除名单**，不能只读自己这一轮的台账。
