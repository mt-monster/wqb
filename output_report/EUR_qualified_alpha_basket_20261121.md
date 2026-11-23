# EUR/D1 合格 alpha 篮子核对报告（2026-11-21）

> 目标：≥3 个合格 alpha（平台闸全绿 + 内部严线 prod<0.65 / self<0.50 / TO∈[5%,20%] + 逐年无中途空窗 + 标准档 + 互相独立）
> **塔位口径按用户 2026-11-21 指令已核对修正**：`get_pyramid_alphas` 实读，EUR/D1 满塔 8 个（analyst 10 / other 3 / fundamental 3 / news 3 / model 3 / risk 3 / sentiment 3 / imbalance 3）；未满塔 6 个（pv 2 / insiders 2 / macro 1 / earnings 1 / socialmedia 0 / institutions 0）。
> **未提交任何 alpha**（红线：提交需用户明确确认 + confirm_submit=True）。

## 一、已确认合格（未满塔 + 内部严线全过 + 独立）

| # | alpha | 塔位 | S / F / 2Y / sub | TO | prod | self | 逐年 | 独立性 |
|---|---|---|---|---|---|---|---|---|
| 1 | `RReEEgwb` | macro 1/3（未满） | 2.18/1.27/2.62/1.54 | 17.4% | 0.5339（今日 22:22 缓存） | 0.261 | 2021–2023 全正，起点型缺失已放开 | 与 #2 0.076 |
| 2 | `58geG1P1` | fundamental(满)+pv 2/3（未满腿） | 1.79/1.25/2.17/1.20 | 6.9% | 0.5362（11-19 缓存） | 0.434 | 10 年全持仓 pnl 全正 | 与 #1 0.076 |

两者平台 `checks.fail` 空、RA 零失败、risk_neutralized_sharpe 有值（标准档）、`pyramids` 含未满塔。

## 二、闸门客观合格但落满塔（按用户「已点亮塔不再投入」口径次优先，供裁定）

| alpha | 塔位 | S/F/2Y | TO | prod | self | 与 #1/#2 互相关 | 备注 |
|---|---|---|---|---|---|---|---|
| `leAnKOEA` | analyst 10/3 + other 3/3（双满） | 2.05/1.39/2.48 | 7.15% | 0.6476（198h 前陈旧，平台重算熔断中） | 0.462 | −0.11 / 0.04 | prod 边缘 0.0024，待终验 |
| `9qxe7gWV` | other 3/3（满） | 3.62/2.73/2.72 | 16.2% | 0.5985（DB，需复核） | 0.351 | −0.16 / −0.08 | 信号最强，10 年多数 S>3 |
| `3qjeJGle` | analyst 10/3（满） | 1.72/1.08/1.80 | 4.7%（<5% 严线下） | 0.5710 | 0.909 ✗ | — | self 爆，淘汰 |
| `xArjE96W` | risk+analyst+sentiment（全满） | 2.28/1.45/2.32 | 10.8% | 0.5907 | 0.589 ✗ | — | self 超严线，不算 |

## 三、淘汰记录（核对证据）

- `O0WawXzg` S3.20 但平台 `LOW_SUB_UNIVERSE_SHARPE` 0.8<1.66 失败 ⇒ 平台闸未过。
- `ZYQmolVx` prod 0.5276 但 self 0.688（内部严线 0.50 不过）+ TO22.7%（严线外）⇒ 不算。
- `QPv5Zrpp` self 0.905 / `JjeL53gx` self 0.967 / `WjOeNE6O` self 0.641 / `wpojN7Av` self 0.576 ⇒ 全超严线。
- `e75x1vAl`/`E56GgqLL`/`mL617YPx` 与 `58geG1P1` 同为 fnd72 内核，互相关 0.937 ⇒ 重复件，不可作独立第 3 颗。

## 五、earnings6 未满塔新挖探针（2026-11-21，6 臂全灭）

为凑足「未满塔第 3 颗」，对 earnings6（earnings 塔 1/3 未满）处女字段按画像模板 + presence 门控 + ts_backfill 派 6 臂：
`ern6_x_dividend_233`（cov0.93）、`eps_change_absolute_value`、`ern6_estimated_eps`、`preliminary_eps_range_lower_bound` × {ts_zscore/ts_quantile、group_rank/group_zscore、w252/w504}。
**结果全灭**：S≤1.0（最好 `78YYL6GQ` S1.00 但 sub −0.07 / 2Y1.57<1.58 / RA5 失败），其余 S≤0.46 或全零。
⇒ 印证画像先验「earnings6 EPS 族历史 best S≈0.91」——单集 ATOM 结构信号层弱，**第 3 颗不在此**。记 PROVISIONAL（六维未穷尽，不判数据集死；本轮只测了 4 字段×基础形态）。

## 六、当前状态与下一步

- **严格未满塔口径：仅 2 颗独立合格**（#1 macro + #2 pv）。earnings6 新挖 6 臂全灭，第 3 颗仍未从未满塔找到。
- 若用户接受满塔存量件，`leAnKOEA`（self 0.462/互相关独立/prod 0.6476 边缘待终验）或 `9qxe7gWV`（S3.62/prod DB 陈旧待复核）可作第 3 颗——但落满塔，与「已点亮塔不再投入」红线冲突，**需用户明确裁定**。
- 未满塔剩余可挖方向（只读盘点）：insider_agg_matrix 次级市场族（2/3，但 prod 池已被 9qxdnV72 占 0.76-0.80）、socialmedia15 新代 scl15_*（0/3，但 cov0.37 结构缺陷）。均为低先验，未开波。
- prod 平台服务反复熔断（单槽 + 连续 pending），按纪律不重触发，隔时重查。
