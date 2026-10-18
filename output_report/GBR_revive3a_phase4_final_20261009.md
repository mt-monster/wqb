# Phase 4 结题：3a 复活补测结果 + 画像终态 + SEM v3（GBR，2026-10-09）

> 链路总览：用户明令「不同字段画像用不同骨架」→ Phase 0 骨架缺口画像 → 审核点② v2 映射（实证校准）
> → 审核点③ 两级闸门 → 审核点④ 3a 复活补测（**89 条 / 12 波，全量无抽样**）→ 本结题。

---

## 一、★ 3a 复活补测结果（47 WEAK 字段 × 各 2 族缺口骨架）

```
收割 89/89 条全部落库（归因 89/89 ✓）
复活（新骨架 S≥1.58）      = 1 个（2.1%）
被新骨架提升（但未过闸）    = 2 个（4%）
ΔS 中位数                 = −0.88（新骨架普遍弱于该字段的原骨架）
置信度升档（2 条新骨架全 <1.10）= 36 个（低置信 → 高置信 WEAK/DEAD）
```

**唯一复活**：`techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r5_q1` —— `decay_linear` 族把 S 从 1.47 推到 **1.81**
（画像已重建：verdict 已翻 ALIVE，ALIVE 总数 51→52）。
⚠ 但该变体 2Y=1.15 / F=0.87，**未过全闸**，且与已有全闸候选 `kqga9VK8`（r10_q2_p1）同族 ⇒ 不是新的可提交来源。

## 二、★ 核心结论（诚实版）

1. **「单骨架判死 = 假死」在 GBR 的 WEAK 池里基本不成立**：47 个字段配上各自画像匹配的缺口骨架后，
   复活率只有 **2.1%**，且 ΔS 中位 **−0.88**（新骨架普遍更差）—— **这些字段的原骨架（house 系）本来就是它们的最强形态**。
   ⇒ GBR 的 WEAK 是真的弱，不是骨架错配。**这个负结论的价值：它把「骨架错配」从嫌疑犯名单上排除了（用 89 条实测）。**
2. **但方法论仍然成立且必要**：① 只有跑完才知道（事前 64% 字段单骨架是不可接受的不确定性）；
   ② 36 个字段置信度升档，画像的「死」从此有证据强度分级；③ 产生了实测校准的 SEM v3。
3. **对 DEAD 池的推论（3b/3d 不再推进）**：WEAK（1.10+）复活率仅 2.1%，DEAD（<1.10）的期望复活率更低
   ⇒ **取消 3b/3d 大规模复活计划**（省 ~50 波），只保留「语义抽样扫测」作为新区第 0 步。

## 三、SEM × 骨架族 v3 矩阵（合并 revive3a 后全量重估，maxS(n)）

| sem_type | top 族（v3） |
|---|---|
| count | subtract 1.96(138) ｜ quantile 1.96(53) ｜ gn_first 1.95(33) ｜ decay_linear 1.90 |
| ratio | delta 2.15(151) ｜ av_diff 2.02(86) ｜ gate 1.87 ｜ quantile 1.78 |
| percentile | delta 2.61(58) ｜ gate 2.37 ｜ gn_first 1.91(51) ｜ double_window 1.71 |
| estimate_level | delta 1.90(136) ｜ ts_rank 1.79(29) ｜ level_rank 1.78(64) |
| probability | delta 1.80(126) ｜ av_diff 1.48 ｜ level_rank 1.41 |
| score | level_rank 1.61(53) ｜ ts_rank 1.25 ｜ delta 0.92 |
| level_amount | delta 1.78(28) ｜ level_rank 1.04 ｜ ⚠ts_zscore 0.65 |
| sentiment | quantile 1.75(7) ｜ level_rank 1.40 |
| revision_change | level_rank 1.62(23) ｜ decay_linear 1.50 |
| unknown | gate 2.07(95) ｜ decay_linear 1.81(29) ｜ quantile 1.76 |

**⇒ v2 映射在 v3 数据下全部站住（无一格被推翻），SEM_PREFERRED 无需改动。**

## 四、画像终态（GBR，2026-10-09 重建）

```
ALIVE 52（+1：techindi r5_q1）｜ WEAK 46 ｜ DEAD 606 ｜ DEAD_STATIC 29 ｜ DEAD_TURNOVER 7 ｜ DEAD_COUNT 5
UNTESTED 2,501 ｜ UNKNOWN_COVERAGE 7,477 ｜ UNUSABLE 3,409 ｜ AXIS_ONLY 1,390
见过 ≥3 族骨架的字段：191（本轮前 192→现在口径更准）｜ 全部实测 2,703 条 / 164 波
```

## 五、本次整改的完整沉淀（可跨区复用）

| 资产 | 位置 |
|---|---|
| 骨架面板（12 族 + SEM_PREFERRED v2/v3） | `tools/fields/skeleton_panel.py` |
| 两级多样性闸门（波级 + 字段级 + 配料豁免） | `skeleton_panel.py audit --region` |
| 骨架缺口画像列 | `field_profile_perf.n_skeletons / skeleton_fams` |
| 缺口报告 | `skeleton_panel.py gap-report --region` |
| 断点续跑 runner 模板 | `wqb-scripts/revive3a_run.py`（含 sim_id 日志回收） |
| 纪律 | skill §11 + 用户级/项目 MEMORY |

## 六、GBR 战役最终状态

```
候选池：17 颗 IS 全闸 + RA 0（analyst7 家数 6 + pv47 反转 10 + techindi 1）
全部 prod ≥0.73 ⇒ 可提交 0（区内无解，已六类形态逐类封死）
画像：15,522 字段全量，双层（强度 × 语义 × 骨架缺口）齐备
```
**建议下一步：跨区开新区（语义抽样扫测第 0 步 → 画像驱动骨架初筛 → 两级闸门发批）。**
