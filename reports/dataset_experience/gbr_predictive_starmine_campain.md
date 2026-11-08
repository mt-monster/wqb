# GBR predictive_starmine 数据集经验（2026-11-08）

> 区域：GBR / TOP700 / D1。数据集：predictive_starmine（631 字段，数据集级 aC 4727，但修订计数字段级 aC 0-17）。category = MODEL。
> 本文件是 wave 级实证沉淀；完整推导见 `tracking/CHN/chn_admission_probe_20261106.md` §6-§9。

## ★ 出货面：FY1 收入修订净广度 × COLD（bl6KwjwK，全闸+prod 0.4582）

- 表达式：`add(multiply(2, group_rank(ts_zscore(subtract(analyst_upward_revision_count_fy1_revenue_7d_4, analyst_downward_revision_count_fq1_revenue_7d_5), 66), sector)), reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))`
- S1.89 / F1.06 / TO17.1% / 2Y2.80 / sub1.18 / self0.1767 / prod0.4582 / 互相关 vs 篮子 ≤0.4578。
- 机制：修订广度漂移（Womack/Chan；论坛《分析师盈利预期修正广度》独立背书）。

## 实测边界（同批对照，勿重试）

| 面 | 结果 | 结论 |
|---|---|---|
| 升级比率 up/(up+dn)（P0oAV7Vp） | S0.90 | 比率面弱于净广度面 |
| 7d/90d 升降级净计数（leANm5zN/vR1oQpJa） | S0.83/1.40 | 不过线，收敛于 FY1 收入 |
| FY1 EBITDA 14d/30d 净修订（LLMwPOQv/npvl1wEd） | S1.27/0.93 | EBITDA 面低一档 |
| FQ1 earnings 30d 净修订（j2YVZpOW→j2YJ5zge） | S1.25 | 同上 |

⇒ **数据集收敛**：只有「收入科目 + FY1 视角 + 7d 快窗口 + 净广度」这一格出货。其余科目/窗口/形态全部低一档。

## 方法论要点（跨区可复制）

1. **冷门字段筛选器**：`alphaCount ≤ 20 且 coverage ≥ 0.6`——本数据集 108 个修订计数字段全中（生产池几乎无人用 ⇒ prod 0.4582 的根因）。
2. **prod 墙是机制级常数**：同族变体互相关 0.988-0.999 只占一席；几何/窗口修补只能把 insider 族 prod 0.95+ 移到 0.84（对照反例），救不回 0.70 线。派同族变体前先查该族已知 prod。
3. **SHORTINTEREST+MODEL 组合**：bl6KwjwK 占 1/3 席（每组合 ≤3）。

## 关联文件

- `results/prod_wait_bl6KwjwK.json`（prod 落盘）
- `results/_out_sm1h.json` / `_out_sm2.json` / `_out_sm3h.json`（收割原始）
- 记忆条目：GBR 第 7 颗成立（2026-11-08）
