# SA 选区分析：哪个 region 最可能组出高质量 SuperAlpha

> 日期：2026-10-14（晚场更新，ACTIVE 由 201 → 207 后重做）
> 结论：**USA / TOP2000** 仍是最优交点（质量优先）；**USA / TOP1000** 为确定性优先的零风险备选。
> 全部判定基于平台真实仿真（`super_build.py select` + `probe`），非本地估算。

---

## 1. 结论摘要

判据：高质量 SA 需同时满足两个条件——
① **组件质量高**（决定 SA 的 IS 上限）；② **名额未被占用**（决定能否通过 SELF / PROD 双闸）。

| 档位 | SA IS | 已占 SUPER | SELF | PROD | 判定 |
|---|---|---|---|---|---|
| **USA / TOP2000** | **4.01** | 1（本人刚提交） | 0.3383 | 0.6217 | **★ 质量优先的最优交点** |
| USA / TOP1000 | 2.61 | **0** | **0.0** | 0.6601 | 确定性优先，零自我相关压力 |
| DEU / TOP500 | 2.27 | 0 | 0.6148 | 0.6146 | 余量最宽，质量垫底 |
| IND / TOP500 | 5.4+ | **10** | — | — | 质量天花板，名额已满 |
| KOR / TOP600 | 4.9+ | **8** | — | — | 17 变体最低 SELF 0.6907，未破闸 |
| GBR / TOP700 | 3.44 | 2 | — | — | 12 结构全 BLOCKED，已锁死 |

**关键变化**：本轮新增 6 颗 ACTIVE（含本人提交的 `vROw5Rkd`），
USA/TOP2000 由零占用变为 **1 颗占用**，但仍远低于 IND(10) / KOR(8)。

---

## 2. 全档位重扫描结果

统一参数：`STATISTICAL · decay1 · truncation 0.02 · selectionLimit 15 · self_gate 0.70 · combo_power 1 · selection=(1 - self_correlation)`

| 档位 | 结果 | 对比上一轮 |
|---|---|---|
| **USA / TOP2000** | **IS 4.01** | 持平（去重返回 `vROw5Rkd`） |
| **USA / TOP1000** | **IS 2.61** | **↑ 0.31**（上一轮 2.30）★ 新增 alpha 改善了此池 |
| USA / TOP500 | IS 1.64 | ↑ 0.10（上一轮 1.54） |
| DEU / TOP500 | IS 2.27 | 持平 |
| USA / TOPSP500 | 无输出 | — |
| USA / ILLIQUID_MINVOL1M | 非法档位（平台 HTTP 500） | — |
| EUR 全部 5 档 | 组件不足 10 | 无变化 |
| HKG / TOP800 · TOP500 | 组件不足 10 | 无变化 |
| ASI / MINVOL1M · MINVOL10M · TOP500 | 组件不足 10 | 无变化 |
| MEA / TOP200 | Failed to create simulation | — |
| GLB / TOPDIV3000 | 无输出 | — |

**⇒ 新增提交没有改变可用性排序**：EUR / HKG / ASI 仍全档凑不满 10 个组件，
IND / KOR 仍被占死。唯一实质变化是 USA/TOP1000 池质量提升。

---

## 3. selection 排序键是质量的最大杠杆（本轮最重要的发现）

同一 USA/TOP2000 档位，仅更换 selection 排序键：

| 排序键 | IS S / F / TO |
|---|---|
| **`(1 - self_correlation)`（选最独立）** | **4.01 / 3.33 / 0.171** |
| `(1 - turnover)`（选最低换手） | 1.74 / 1.17 / 0.071 |

**IS 相差 2.3 倍**。选「低换手」组件会让 SA 质量崩塌——低换手 ≠ 强信号。

同时验证：**self_gate 无区分度**——sg 0.60 与 0.70 选出完全相同的组件集
（平台去重返回同一颗 `vROw5Rkd`），说明该池内收紧 self_gate 不起作用。

### 参考：selectionLimit 曲线（上一轮，USA/TOP2000）

| lim | IS | SELF | PROD | 余量 |
|---|---|---|---|---|
| 10 | 3.63 | 0.2969 | 0.5397 | 0.160 |
| **15** | **4.01** | 0.3383 | 0.6217 | **0.078** |
| 20 | 4.05 | 0.3538 | 0.6794 | 0.021 |
| 40 / 50 | 3.70 | 0.4143 | 0.6697 | 0.030（与 50 相同 ⇒ 池饱和约 40） |

---

## 4. 零占用档位的量化优势

**USA / TOP1000 的 `LL5aX6Y2`（IS 2.61 / F 1.80 / TO 0.1852）实测：SELF = 0.0。**

因为该档位没有任何已提交 SA，**self 闸完全不构成约束**，只需通过 prod 一个闸
（实测 PROD 0.6601，余量 0.040，双闸 PASS，立即可提交）。

对照：USA/TOP2000 在提交 `vROw5Rkd` 后，SELF 已从 0.3383 起步——若再出第二颗会更高。

---

## 5. 两条方法论约束

### 5.1 API 的 `region=` 过滤参数无效
用 `?region=X` 分页拉取 HKG / ASI / EUR / GLB，返回**完全相同的 alpha 集合**
（证据：TOP500 的 top5 均为 `VkdkbvRM:2.7 88v826XW:2.7 ...`，而这批实为 DEU 的 alpha）。

**可靠替代**：不带 region 拉全量后按 `settings.region` 本地分组；或直接用 `select` 试建，由平台判定。

### 5.2 selection 表达式只有 3 个合法变量
实测 14 个候选（`sharpe` / `fitness` / `returns` / `drawdown` / `margin` / `longCount` / `shortCount` /
`alphaCount` / `pnl` / `is_sharpe` / `performance_sharpe` / `dateCreated` / `status` / `os_sharpe`）
全部报 `Attempted to use unknown variable`。

⇒ **仅 `prod_correlation` / `self_correlation` / `turnover` 可用**，无法直接「按强度排序」。

---

## 6. 当前可提交候选

| alpha | 档位 | IS S/F/TO | SELF | PROD | 余量 | 状态 |
|---|---|---|---|---|---|---|
| `vROw5Rkd` | USA/TOP2000 | 4.01 / 3.33 / 0.1706 | 0.3383 | 0.6217 | 0.078 | **已提交 ACTIVE** |
| `LL5aX6Y2` | USA/TOP1000 | 2.61 / 1.80 / 0.1852 | **0.0** | 0.6601 | 0.040 | 双闸 PASS，待提交 |
