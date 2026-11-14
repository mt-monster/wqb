# ⚠ 台账修正：撤回「14 颗」结论，合规交付仍为 11 颗

日期：2026-11-12（覆盖 LEDGER_14_ALPHAS_20261112.md 的结论部分）

## 撤回原因

上一轮我据 `compute_mutual_correlation` 得出「14 颗全对<0.7、可并入交付篮子」，并把 3 颗新件计入 14。
**该结论在互相关维度成立，但违反 Goal 约束第 7 条（PV+MODEL 禁混）**：

| 新件 | 塔归属 | 违规点 |
|---|---|---|
| 2r5MO67Z | PV + INSIDERS + **MODEL** | PV+MODEL 并存 |
| d5apOzxj | PV + INSIDERS + **MODEL** | PV+MODEL 并存 |
| npa9KaVd | PV + INSIDERS | ✅ 合规（但卡 IS_LADDER year3，S 1.58 过、ladder 1.24 不过）|

⇒ `2r5MO67Z`（S 2.63）与 `d5apOzxj`（2Y 2.65）**不能呈交**。
⇒ `npa9KaVd` 合规但**未过闸**（IS_LADDER_SHARPE）。

## 修正后的真实状态

| 项 | 数 | 说明 |
|---|---:|---|
| 已 ACTIVE | 6 | bl6AvMkN / vR1oxZA3 / GrW9OxmG / zq3eb7No / rKRx2Alj / 78Yk8VR1 |
| 待授权且合规 | 5 | qM7KxkQV / Jj8VQwoe / RREPm361 / d5a2vxzY / 9qlz29Oe |
| **合规交付合计** | **11** | 与修改前一致 |
| 目标缺口 | **9** | 20 − 11 |

## 教训（写入方法论）

**「闸全过 + 互相关达标」不等于「可交付」。** 三段式判据缺一不可：
1. 平台 checks 全过（含 IS_LADDER_SHARPE 动态窗）
2. 互相关全对 < 0.7（最大独立集）
3. **分类合规**：PV / MODEL / OTHER 三者两两不得并存；它们只能与其它 category 组腿（且 ≤5 数量）

⇒ 今后任何新件在计入台账前，**必须先读 `pyramids.list` 的塔名反推分类构成**，而不是只看 checks。
塔名 → 分类映射：`DEU/D1/PV`→PV、`DEU/D1/MODEL`→MODEL、`DEU/D1/OTHER`→OTHER、`DEU/D1/INSIDERS`→INSIDERS、`DEU/D1/NEWS`→NEWS。
若 list 中同时出现 PV 与 MODEL，或同时出现三者中任意两个 ⇒ **违规**。
