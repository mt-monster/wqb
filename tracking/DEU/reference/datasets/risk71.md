# risk71 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="risk71", filter_sharpe=false)`。
> 完整性闸：`python tools/gates/field_profile_completeness_gate.py --profile tracking/DEU/reference/datasets/risk71.md`

## 字段全表（10 字段，全 MATRIX）

| 字段 id | 类型 | coverage(声明) | alphaCount | userCount | description |
|---|---|---:|---:|---:|---|
| `residualized_return_top2500` | MATRIX | 0.0 | 17 | 10 | Daily stock-specific idiosyncratic residual returns panel for the Europe TOP2500 |
| `eur_minvol1m_specific_return_dsrt` | MATRIX | 0.0 | 5 | 4 | Reproducible specific return for the minimum volatility 1-month strategy in the … |
| `ecs_top400_specific_return_dsrt` | MATRIX | 0.0 | 4 | 3 | Reproducible specific return for the top 400 equities in the ECS universe |
| `ecs_top1600_specific_return_dsrt` | MATRIX | 0.0 | 3 | 2 | Reproducible specific return for the top 1600 equities in the ECS universe |
| `residualized_return_top600_ats` | MATRIX | 0.0 | 3 | 2 | Panel of daily stock-specific residual returns (DSRT) from the MFM2 risk model |
| `ecs_top1200_specific_return_dsrt` | MATRIX | 0.0 | 2 | 2 | Reproducible specific return for the top 1200 equities in the ECS universe |
| `top1200_residual_return_dsrt` | MATRIX | 0.0 | 2 | 2 | Reproducible specific return for the top 1200 equities in the selected universe |
| `ecs_top800_specific_return_dsrt` | MATRIX | 0.0 | 0 | 0 | Reproducible specific return for the top 800 equities in the ECS universe |
| `epp_minvol1m_specific_return_dsrt` | MATRIX | 0.0 | 0 | 0 | Reproducible specific return for the minimum volatility 1-month strategy in the … |
| `top800_residual_return_dsrt` | MATRIX | 0.0 | 0 | 0 | Reproducible specific return for the top 800 equities in the selected universe |

**机制聚类（3 族）**：
1. **残差收益面板**（`residualized_return_top2500` / `residualized_return_top600_ats`）
2. **ECS 宇宙特定收益**（`ecs_top400/800/1200/1600_specific_return_dsrt`）—— 同源换宇宙规模
3. **最小波动策略特定收益**（`eur_minvol1m_specific_return_dsrt` / `epp_minvol1m_specific_return_dsrt`）+ `top800/1200_residual_return_dsrt`（选定宇宙变体）

⇒ **10 个字段只 3 条机制**（与 GBR risk 类别「字段多 ≠ 信息源多」同型）。

## 实测（逐字段，生产档 decay4 / SUBINDUSTRY / trunc0.08 / nanHandling ON）

| 字段 | 模板 | alpha | S | F | 2Y | TO | sub | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `residualized_return_top2500` | `group_rank(ts_zscore(f,252),sector)` | `e7aZY2Ed` | **−1.12** | −0.31 | −0.37 | **0.905** | −0.35 | 4 |
| `eur_minvol1m_specific_return_dsrt` | `group_rank(ts_zscore(f,252),sector)` | `pwae2z3j` | −0.44 | −0.13 | −0.04 | 0.306 | 0.14 | 3 |

## ★★★ 首要结论：`coverage = 0.0` 是报告层假象，不是「无数据」

`get_datafields` 对 risk71 的 **10 个字段全部返回 cov=0.0**，但上表两条探针臂**都产出了有效读数** ⇒
数据真实存在。这与 DEU 的 GROUP 字段（`country`/`currency`/`market` 等同样报 cov=0.0 却能正常使用）同型。

**入册纪律**：判「coverage=0 ⇒ 数据层排除」**必须先用 ≥2 臂探针实测**；
只有探针也无读数时，cov=0.0 才能作为排除依据。**不得**再按 cov 直接排除数据集。

## 信号特征

- `residualized_return_top2500`：裸 zscore **S −1.12（强反转）**、**TO 90.5%**。
  ⇒ **方向清晰（取反后 S≈+1.12），但换手是硬敌**（TO 闸 0.70，当前 0.905）。
  战役主线 = **在保住反转信号的前提下把 TO 压到 0.70 以内**（平滑 / 长窗 / 门控 / hump-tvr）。
- `eur_minvol1m_specific_return_dsrt`：S −0.44、TO 30.6%、sub 0.14（sub·S⁻¹ 不达标 0.32）。

## 相关风险数据集覆盖摸底（2026-11-23，零配额）

| 数据集 | 字段数 | cov>0 | 结论 |
|---|---:|---:|---|
| risk71 | 10 | 0（**但探针证明有数据**） | 需实测，不可按 cov 排除 |
| risk72 | 31 | 0 | 同族（`cfg2_*_residual_return` / `ats_*_residualized_return`），**同样需探针** |
| risk60 | 5 | 5（cov 0.835） | `lending_fee_bid_rate` aC167 / `rsk60_offer` aC214 / `rsk60_last` aC141 / `rsk60_crowding` aC61 / `rsk60_datatime` aC15 |
| risk88 | 1 | 1（cov 1.0） | 单字段 `alternative_market_cap_usd` aC82（只能 1 族） |

## 待补

- 其余 8 字段的逐字段实测（模板族层跑完后补）
- 三个机制族各自的完整梯度（模板族 → L1 全替 → L2 → L3 → L4 → L5）
