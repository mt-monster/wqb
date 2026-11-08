# 里程碑：首条 S 过线的新候选 Xg9eGkzm（2026-11-07）

## 全量实测表（analyst10 · 几何 W189 / exchange / industry / R&M 中性化）

| alpha | 字段对 | S | F | 2Y | sub | TO | 卡点 |
|---|---|---:|---:|---:|---:|---:|---|
| **Xg9eGkzm** | **ebi_fy2 × ebi_fy1** | **1.60 ✅** | **1.30 ✅** | 1.21 ❌ | **1.61 ✅** | 0.0939 | **仅 2Y** |
| Vkx5kO2w | pre_fy2 × pre_fy1 | 1.53 | 1.22 | 1.14 | 1.61 | 0.0920 | S/2Y |
| MPYZPkKL | ebi_fy1 × ebt_fy1 | 1.52 | 1.19 | 1.51 | 1.42 | 0.0863 | S/2Y |
| A1Vm18QY | net_fy1 × ebt_fy1 | 1.51 | 1.20 | 1.40 | 1.35 | 0.0874 | S/2Y |
| WjO0MNox | cpx_fy1 × sal_fy1 | 1.50 | 1.17 | 1.02 | 1.21 | 0.0851 | S/2Y |
| bl6nl18Z | sal_fy1 × dps_fy1 | 1.35 | 0.99 | **1.70 ✅** | 1.08 | 0.0840 | S/F |
| N1N3xYqg | gps_fy1 × nav_fy1 | 0.85 | 0.50 | 0.83 | 0.92 | 0.0801 | 全 |
| 78LM7e0L | opr_fy1 × ndt_fy1 | 0.80 | 0.46 | 1.20 | 0.80 | 0.0654 | 全 |

## 首次突破 LOW_SHARPE
`Xg9eGkzm` 是全战役（除已交付 3 颗外）**第一条 S≥1.58 的新候选**：S 1.60 / F 1.30 / sub 1.61 / TO 0.094 全部达标，唯一缺口 **2Y 1.21（差 0.37）**。
表达式：
```
group_neutralize(multiply(group_rank(ts_av_diff(anl10_smartest_ebi_fy2_pred_surps_v1,189),exchange),
                          group_rank(ts_av_diff(anl10_smartest_ebi_fy1_pred_surps_v1,189),exchange)),industry)
```

## 字段对 → S / 2Y 的分裂规律（这是本轮最有用的结构发现）

把 8 个字段对按「两个指标的关系」分类：

| 类型 | 例子 | S | 2Y | 解释 |
|---|---|---:|---:|---|
| **同指标跨年度** | ebi_fy2 × ebi_fy1、pre_fy2 × pre_fy1 | **高** 1.53–1.60 | **低** 1.14–1.21 | 纯粹的**预期修正期限结构**，近端信号强但只在近端有效 ⇒ 2Y 塌 |
| **同表不同科目** | ebi × ebt、net × ebt、cpx × sal | 高 1.50–1.52 | 中 1.02–1.51 | 两个利润口径互相确认 |
| **跨报表不同科目** | sal × dps | 低 1.35 | **高 1.70** | 经营规模 × 股东回报，跨利润表/现金流量表 ⇒ 十年都稳 |
| **弱科目** | gps × nav、opr × ndt | 低 0.80–0.85 | 低 0.83–1.20 | 报送稀疏/口径噪声大 |

**核心结论**：2Y 要 1.58+ 必须**跨报表**取字段对（sal×dps 的 1.70 是唯一过线值），而跨报表配对会把 S 压到 1.35。
⇒ 需要的是**「跨报表 + 修正常态化」的组合**：P18 的 bl6nl18Z 组（ts_mean 平滑 / signed_power(2)）正是为此设计。

## fundamental44 封盘

4 条应计变体全部弱且同向：
| 字段 | 表达式 | S |
|---|---|---:|
| perc_accruals | `-group_rank(...)` | −0.64 |
| cashflow_accruals | `-group_rank(...)` | −0.58 |
| modified_jones_cf_accruals | `-group_rank(...)` | −0.57 |
| working_capital_accruals | `-group_rank(...)` | −0.54 |

**四个应计口径高度一致地落在 |S| 0.54–0.64**，且全部触发 CONCENTRATED_WEIGHT + LOW_SUB_UNIVERSE_SHARPE（说明信号集中在少数大票）。
这与 fundamental6（8 个会计机制最强 S 0.70）同型 ⇒ **FUNDAMENTAL 族在 KOR/TOP600 的天花板 ≈ 0.7，应计异象在韩国市场方向反转且弱**。
判死：fundamental44 封盘，不再投批次。

## 下一步：analyst10 尚未测的维度

已测指标：pre, ebi, ebt, net, cpx, sal, dps, gps, nav, opr, ndt（11/12）
**未测：bps（每股账面价值）**；**未测季度口径 fq1/fq2**（全部实测都是 fy1/fy2 年度口径）。
P22 设计：bps 族（bps_fy1×bps_fy2、bps×dps、bps×ebi）+ 季度期限结构（ebi_fq1×ebi_fq2、ebt_fq1×ebt_fq2、sal_fq1×sal_fq2、dps_fq1×dps_fq2）+ 「跨报表 + 高S家族」混合（ebi×dps、net×dps、ebt×dps）。
