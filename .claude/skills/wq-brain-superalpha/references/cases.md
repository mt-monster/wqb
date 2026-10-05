# SA 真实案例（每例：背景 / 操作 / 结果 / 是否可复现）

> 主 SOP 见 [`../SKILL.md`](../SKILL.md)。旧版把 4 个案例按时间堆叠在正文里，★ 教训只出现在案例里、不在规则区；这里每例压成 5 行，教训并入 [`levers-and-evidence.md`](levers-and-evidence.md) 的规则表。
> **重要**：案例 3 / 4 提交时**没有** prod 闸（2026-09-25 才默认强制）。它们回带 value 0.8094 / 0.8571 仍判 PASS——**按今天的默认 CLI 这两颗会被 prod 闸拒绝**，除非显式 `--allow-prod-above-07`；当时是否使用豁免无记录。别把它们当成「value > 0.7 也可提交」的依据。

| # | 案例 | 状态 |
|---|---|---|
| 1 | USA KPGvRMg1 | ACTIVE；**不可按原样复现**（使用了已禁用的 `combination()`） |
| 2 | MEA 78jYpn0Z | ACTIVE；**存量，不可复制**（MEA 已无法新增 SA） |
| 3 | GLB A1NQ57NW | ACTIVE；提交时无 prod 闸 |
| 4 | KOR 9qjGvaWe | ACTIVE；提交时无 prod 闸 |

## 案例 1　USA KPGvRMg1（中性化杠杆的来源）

- **背景**：USA book 已有大量 ACTIVE REGULAR，目标把 SA 的 PROD 压到 0.7 以下。
- **操作**：早期用 5 个显式 alpha 的 `combination()` 思路（该算子现已被平台禁用，仅作等价思路说明）；验收标准 = 等价体 PROD ≤ 0.7 且 SELF ≤ 0.7 且 ACTIVE。
- **结果**：获胜体 KPGvRMg1（name = `0.6944`）：PROD 0.6944 / SELF 0.557 / sharpe 2.89 / fitness 2.39 / turnover 0.2194。决定性变化 = 中性化 MARKET（PROD 地板 0.7169）→ SUBINDUSTRY（0.6944）。
- **可复现性**：**否**（`combination()` 不可用）；可复用的只有「逐区扫描中性化」这条结论（levers §1）。SUBINDUSTRY 对**单颗 REGULAR** 无效，只在 SA 组合层面（10+ 去中心化成分）才降 prod-corr。

## 案例 2　MEA 78jYpn0Z（组件困境，2026-08-28）

- **背景**：MEA 自由池仅 6 颗（3 老 + 3 新提），不足 10。
- **操作**：selection 借既有 SA `3qlYKAaO` 内低 prod-corr 成分补齐：`((neutralization == "COUNTRY") || (prod_correlation < 0.55)) * (turnover > 0.01) * (turnover < 0.6)`——自由池 6 颗全 COUNTRY 中性（SA 内部成分多为 SECTOR），`prod_correlation < 0.55` 精准借入 4 颗最低 pCorr 的 SECTOR 成分 → 恰好 10 颗。
- **结果**：PROD 0.6996 / SELF 0.6996（双双擦线 < 0.7），与既有 SA 仅 0.4731 相关；sharpe 2.52 / fitness 2.99 / turnover 0.052 / subUniverse 2.09 / IS_LADDER 2.93。描述用裸 PATCH 写入后 submit 两次均 200 "IS checks passed"，30 s 内翻 OS / ACTIVE。
- **可复现性**：**否**——MEA 的 `POST /simulations` 现返回 400 "Region MEA is not available."，此案例是关闭前的存量。教训（0.6996 擦线极脆弱；自由池扩到 10 后应重组零重叠变体、降低对借入成分的依赖）保留。

## 案例 3　GLB A1NQ57NW（组件恰好 10 颗，2026-09-24）

- **背景**：GLB ACTIVE REGULAR 恰好 10 颗、0 颗 SUPER（池子未被消耗，新鲜度最高）、当日 SUPER 配额未用。
- **操作**：settings 对齐组件主流（MINVOL1M / d1 / dec10 / tr0.08 / maxTrade OFF，nu = SUBINDUSTRY）。self_gate 0.65 时三中性化全撞 "At least 10 component alphas are required"（有一颗 self_corr 落在 [0.65, 0.70)）→ 放宽到 0.70 即成（梯度放宽成本极低：先 0.65，不行 0.70 / 0.85）。
- **结果**：IS S 4.26 / F 3.72 / T 0.101，CLUSTER 3.0，IS_LADDER 4.82，GLB 分区 sharpe AMER / EMEA / APAC 全 PASS。平台对 SUPER 的 SELF / PROD 回带 0.8094 > limit 0.7 仍 `result = PASS`。
- **可复现性**：**部分**——放宽 gate 的路径可复用（情景 SA-02）；提交那一步现需 `--allow-prod-above-07`（见页首警告）。库存盘点坑（`region=` 参数不生效）已并入 SKILL 步 0。

## 案例 4　KOR 9qjGvaWe（同构淘汰法，2026-09-25）

- **背景**：KOR 已有 3 颗 ACTIVE SUPER，池子 13 颗 REGULAR 大多被消耗过。
- **操作**：同轮建 3 个差异化变体，逐个 `super_build.py submit` 试提（被 403 拒绝**零配额成本**，SUPER_SUBMISSION 始终 0/1）：STATISTICAL/dec5 → ❌ SELF 0.9729（与存量 rKOPg9gd 同构）；STATISTICAL/dec30 → ❌ SELF 0.8938（与存量 j23jgb8Z 同构）；**SUBINDUSTRY/dec10 → ✅ SELF / PROD 0.8571，`result = PASS` → ACTIVE**（S 3.27 / F 4.13 / T 0.0925）。
- **结果**：可复制打法 = 先枚举存量 SA 的 (neutralization, decay) 组合，新变体**刻意错开**；被拒变体按规范淘汰（`RETIRE_<YYYYMMDD>` + hidden，见 SKILL 验证清单）。
- **注意**：这里「逐个试提」在**当时**是「被拒 = 零成本」的探测；但**第一个通过的就是真提交**，未必是最优变体——所以现在先 `probe`、再在用户确认后提交，不用「试提」当探针。KOR 的优势中性化是 STATISTICAL（最强一颗即 STATISTICAL），与 USA / GLB 相反，再次说明中性化必须逐区扫描。
- **可复现性**：**部分**（提交那一步同案例 3 需豁免 prod 闸）。
