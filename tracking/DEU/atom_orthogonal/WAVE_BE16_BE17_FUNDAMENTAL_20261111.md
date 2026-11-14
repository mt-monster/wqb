# BE16 / BE17：fundamental 双窗口骨架攻坚（2026-11-11）

## 依据（决定性）

已提交件 **Wje5K71x** 实测：fundamental6 的 `fnd6_newq_oiadpq` 用骨架
`group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(F,66),240)), rank(ts_delta(ts_backfill(F,66),176))), target_tvr=0.03), sector)`
得到 **S1.73 / F1.37 / sub1.25 / TO0.1269 / self0.1882 / prod0.4305**。

**推翻了旧结论**：「DEU fundamental ATOM 天花板 1.15」是**模板受限**（BE2b 用的是 zscore/长窗/tvr_decay 单窗口），
换双窗口差分之积骨架后达 1.73。⇒ 必须重估 fundamental 整族。

**战略价值**：fundamental 在篮子 6 件里**零覆盖**（4 analyst + 2 short），互相关天然接近 0；
且单数据集 = ATOM，不占任何禁混配额。

## BE16（fundamental89 应计模型 407 字段）

| 臂 | 字段 | 概念 | coverage |
|---|---|---|---:|
| C1 | fnd89_asset_41_11 | 流动资产应计/总资产 | 0.0 |
| C2 | fnd89_asset_41_31 | 流动应计/销售额 | 0.0 |
| C3 | fnd89_asset_53_11 | 非流动应计/总资产 | 0.0 |
| C4 | fnd89_best11_d1_accum_4q | 累计应计率(近四季) | 0.0 |
| C5 | fnd89_best21_d1_accum_4q | 累计应计率(另一口径) | 0.0 |
| C6 | fnd89_best11_d1_current_t | 应计率当期 t 统计量 | 0.0 |
| C7 | fnd89_best21_d1_dts | 应计率历史波动 | 0.0 |
| C8 | fnd89_csjones_all_other_11 | 截面综合应计率 | 0.0 |
| C9 | fnd89_csjones_d1_asset_change | 资产变动 | 0.0 |
| C10 | fnd89_asset_d1_asset_change | 资产变动 | 0.0 |

⚠ **风险**：全部字段 platform coverage = 0.0 ⇒ 若 DEU 无数据，整波 ERROR 或 pnl≈0。
本波同时充当**数据可用性验证**。preflight 已过（字段名存在）。

## BE17（fundamental6 高覆盖字段，主攻）

| 臂 | 字段 | 概念 | coverage |
|---|---|---|---:|
| D1 | fnd6_newa2_oancf | 经营活动净现金流（Sloan 应计核心分子） | 0.540 |
| D2 | fnd6_invchy | 存货减少/增加（应计异象经典成分） | 0.372 |
| D3 | fnd6_capxy | 资本支出 | 0.513 |
| D4 | fnd6_dpy | 折旧摊销 | 0.618 |
| D5 | fnd6_newa2_oiadp | 折旧后营业利润（⚠ 与 Wje5K71x 的 oiadpq 同经济量不同频率） | 0.627 |
| D6 | fnd6_gpy | 毛利 | 0.551 |
| D7 | fnd6_revty | 总收入 | 0.659 |
| D8 | fnd6_txty | 所得税 | 0.643 |
| D9 | fnd6_ivncfy | 投资活动净现金流 | 0.542 |
| D10 | fnd6_fincfy | 筹资活动净现金流 | 0.539 |

全部 preflight 通过且 coverage 0.37-0.66（远优于 BE16）。

## 出货后必查

1. **D5 与 Wje5K71x（fnd6_newq_oiadpq）的互相关** —— 若同经济量，预计 0.7+，需弃。
2. 与篮子 6 件的互相关（预期 ≤0.3，因 fundamental 零覆盖）。
3. self（fundamental6 族的已提交件是 Wje5K71x，若字段重叠会撞）。
4. 逐年覆盖（fnd6 是年报数据，注意长期空窗）。
