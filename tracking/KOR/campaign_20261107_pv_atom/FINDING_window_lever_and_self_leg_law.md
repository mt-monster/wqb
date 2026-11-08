# 突破：全闸通过候选 + self 墙的腿重叠定律（2026-11-07）

## 1. 窗口长度是本轮最强的双目标杠杆

同一字段对（sal_fy2 × ebi_fy1）、同 sector 内分组、同 industry 外中性化，**只改 ts_av_diff 窗口**：

| W | S | F | 2Y | sub | 结论 |
|---:|---:|---:|---:|---:|---|
| 210 | — | — | — | — | （P23 批次未返回，见 P25 阶梯） |
| 231 | — | — | — | — | 同上 |
| **250** | 1.76 | 1.51 | **1.58** | 1.68 | 贴线，2Y 卡 warning |
| **273** | **1.84** | 1.62 | **1.69** | 1.75 | ✅ 全过 |
| **294** | **1.92** | **1.72** | **1.76** | **1.82** | ✅ 全过（本战役最强） |

对照 W189 + exchange 轴的同一字段对没有实测，但 ebi_fy1×ebt_fy1 在 W189/exchange 只有 1.52/1.51 ⇒ **拉长窗口到 ~1.1–1.2 年同时抬 S 与 2Y**，与「平滑算子抬 S 压 2Y」的既有结论方向相反。
机理：`ts_av_diff(F,W) = F − ts_mean(F,W)`，W 越长基线越稳，修正信号的信噪比越高；而年份跨越更多 ⇒ 2Y（近两年）不被末端噪声主导。

## 2. ★ self 墙的「腿重叠定律」（本轮最重要教训）

`compute_mutual_correlation` 与 `check_self_correlation` 实测：

| 对 | 关系 | 互相关 | 是否可入池 |
|---|---|---:|---|
| YP1JGY8q (W294) ↔ 3qo5ZJGO (W273) | 同字段对、仅换窗口 | **0.9937** | ✗ 只能取一 |
| YP1JGY8q ↔ qMLOooX1(已交付) | **共用 sal_fy2 一条腿**（另一腿 ebi_fy1 vs net_fy1） | **0.8402** | ✗ 撞 self 墙（平台 self 0.8207） |
| YP1JGY8q ↔ omERn83n | 数据集/腿全不同 | 0.2859 | ✓ |
| YP1JGY8q ↔ RRE9NkVj | 数据集/腿全不同 | 0.3342 | ✓ |
| MPYZPkKL ↔ qMLOooX1 | **两条腿全不同**（ebi×ebt vs sal×net） | 0.5692 | ✓ |
| Vkx5kO2w ↔ qMLOooX1 | 两条腿全不同（pre_fy2×pre_fy1 vs sal×net） | 0.6883 | ✓ |

**定律**：同一数据集内构建第 2、3 颗 alpha 时——
- 只换窗口 ⇒ 互相关 **0.99**（完全同质，不算新颗）
- **共用一条腿** ⇒ 互相关 **0.82–0.84**（必撞 0.70 self 墙）
- **两条腿都换** ⇒ 互相关 **0.57–0.69**（可入池）

⇒ 这是对旧记忆「只换 group 轴/窗口不算结构位移（0.9589）」的延伸与量化：**判据是"腿的集合是否相交"，不是"轴/窗口是否变化"**。

## 3. 当前最优候选（IS 全闸通过，卡 self）

```
YP1JGY8q  group_neutralize(multiply(
            group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,294),sector),
            group_rank(ts_av_diff(anl10_smartest_ebi_fy1_pred_surps_v1,294),sector)),industry)
          S 1.92 / F 1.72 / 2Y 1.76 / sub 1.82 / TO 0.0966 / raFailed 0 / fail []
3qo5ZJGO  同式 W273 → S 1.84 / F 1.62 / 2Y 1.69 / sub 1.75 / TO 0.0969
```
两者与 qMLOooX1 互相关 0.84/0.84 ⇒ **IS 完美但 self 挡**。除非用户愿意下架 qMLOooX1 换这颗（净提升 +0.30 S / +0.18 2Y / +0.19 F），否则必须找无共享腿的等价替代。

## 4. P25 设计（无共享腿 + 窗口阶梯）
**窗口阶梯**（ebi_fy2 × ebi_fy1，与 qMLOooX1 双无共享）：252 / 273 / 294 / 315 / 336 / 378 —— 目的是定位窗口最优点并确认单调性。
**替代字段对**（统一 W294、sector/industry）：pre_fy2×pre_fy1、net_fy2×pre_fy1、ebi_fy1×dps_fy1、ebt_fy1×dps_fy1。
选型依据：`net×dps / ebi×dps / ebt×dps` 在 W189 就已有 **2Y 1.59–1.75**，套 W294 的 +0.55 2Y 增益后有望双双破 1.58，且 dps 系与 qMLOooX1 无共享腿。
