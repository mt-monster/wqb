# GBR / risk72 全字段探测 + 模板筛选（wave20261124_risk72）

> 依据 `wq-brain-ra-gbr` + `wq-brain-ra-pipeline` 步 3–7；用户 2026-11-24 指令：
> GBR 固定区、未点亮塔优先、全字段探测禁抽样、论坛+论文证据、multi-sim ≤2、一批一收。
> 数据集：**risk72（23 字段）+ risk71（6 字段）**｜塔：**risk 0/3 未点亮**（乘数 1.2）
> 基线候选（库存收割，非本波新产）：`WjlOZZnd` 全闸 IS（S1.76/F1.42/2Y2.14/RA fails=0），仅 prod 0.7987 FAIL；self 0.5796 PASS。

---

## 1. 选点依据（S-PRE 实测，2026-11-24）

- GBR D1 塔位：institutions 1、insiders 0、earnings 2、risk 0、sentiment 0、imbalance 1；model/news/other/analyst/pv/fundamental/shortinterest 已点亮（不投入）。
- 未亮塔全数据集扫描后的**唯一全闸 IS 件** = `WjlOZZnd`（risk，effective=1）。其余全闸件（`omEPQrLE` 等）平台塔位 = SHORTINTEREST（已 5/3 点亮）⇒ 依 3c 不可投入。
- `P0gbMLz7`/`A1v5QXmg`（earnings6）：2014–2018 连续五年零持仓 ⇒ 数据层排除（非信号死）。
- `Xga1Ae00`（imbalance5+PV）：IS 全闸但 self 0.7613 / prod 0.7614 双 FAIL。
- `WjlOZZnd` prod 直方图：主体 ≤0.6，仅 [0.7,0.8) 9 颗小簇 ⇒ 结构性近重复，非密墙；可尝试换表达（论坛同域先验 prod 0.648）。

---

## 2. 证据闸（S2）

- 论坛：`44639524994583`（GBR/TOP700 `residualized_return_nogroup` + 52 日窗 t 值 + 三子窗门控，S1.77/F1.01/TO15.8%，**prodCorr 0.648**；明确「换表达不是调参数」）；`45235010628247`（Risk Neutralization 六档；`vector_neut`/`regression_neut` 先剥因子）；`44557078934039`（F 换手下限 12.5%，慢腿推高 prod）。
- 论文：`paper_search.py --diverse` → 5/5 篇、5/3 作者（特质波动/收益反转系列，DOI 见 ledger `forum_paper_recon_risk72_20261124`）。
- 留痕：ledger `forum_recon_risk72_20261124` + `forum_paper_recon_risk72_20261124`（2026-11-24）。

---

## 3. 批 A · risk72 前 10 字段探针（@NONE/decay0/trunc0/nanOFF）

`multisimulation_id = gxvmf3pu4JkbByS64694P2`（2026-11-24 派发）
**状态（2026-11-24 01:0x 终判）**：**平台仿真服务本时段停摆**。证据：①批 A 25+ 分钟、批 D 20+ 分钟仍 `progress=0.15 / children=0`；②另发 2 臂最小诊断批 `L7iiL3Wy5dw8Ik19tRB4KA4`（`ts_ir`/`ts_zscore`）同样 5+ 分钟 `children=0` ⇒ 非表达式、非批量大小、非并发上限问题。不重发、不虚报。三个 multisim id 保留：平台恢复后 `batch_status` / `harvest_multisim_alphas` 可直接收割（若已跑完）或重派。

| # | 字段 | 类型 | 表达式 |
|---|---|---|---|
| 1 | ats_top1200_equity_residualized_return | MATRIX | rank(ts_backfill(F,250)) |
| 2 | ats_top800_equity_residualized_return | MATRIX | rank(ts_backfill(F,250)) |
| 3 | cfg2_top1200_replicator1 | VECTOR | rank(ts_backfill(vec_avg(F),250)) |
| 4 | cfg2_top1200_replicator2 | VECTOR | rank(ts_backfill(vec_avg(F),250)) |
| 5 | cfg2_top1200_residual_return | MATRIX | rank(ts_backfill(F,250)) |
| 6 | cfg2_top600_replicator1 | VECTOR | rank(ts_backfill(vec_avg(F),250)) |
| 7 | cfg2_top600_replicator2 | VECTOR | rank(ts_backfill(vec_avg(F),250)) |
| 8 | cfg2_top600_residual_return | MATRIX | rank(ts_backfill(F,250)) |
| 9 | cfg2_top800_replicator1 | VECTOR | rank(ts_backfill(vec_avg(F),250)) |
| 10 | cfg2_top800_replicator2 | VECTOR | rank(ts_backfill(vec_avg(F),250)) |

判据：`longCount+shortCount>0` = 有数据；读不到 = PROBE_FAILED（≠ NO_DATA）。

### 批 B（待发，10 臂）
`cfg2_top800_residual_return`、`epp_equity_minvol1m_residual_return`、`eur_equity_minvol1m_residual_return`、`eur_equity_minvol1m_residual_return_validated`、`top1200_equity_residualized_return`、`top1200_..._nogroup`、`top2500_equity_residualized_return`、`top2500_..._nogroup`、`top600_equity_residualized_return`、`top600_..._nogroup`（preflight 已过）。

### 批 C（待发，9 臂）
risk72 后 3：`top600_reproducible_specific_return`、`top800_equity_residualized_return`、`top800_..._nogroup`；
risk71 全 6：`epp_minvol1m_specific_return_dsrt`、`eur_minvol1m_specific_return_dsrt`、`residualized_return_top2500`、`residualized_return_top600_ats`、`top1200_residual_return_dsrt`、`top800_residual_return_dsrt`（preflight 已过）。

---

## 4. 模板筛选批（待发，10 臂，SUBINDUSTRY/decay4/trunc0.08/nanON）

字段统一 `top2500_equity_residualized_return_nogroup`（论坛同域），只换时序核/轴：

| 臂 | 时序核 | 轴 | 目的 |
|---|---|---|---|
| T1 | `ts_ir(F,52)` | subindustry | t 值代理（均值/波动） |
| T2 | `ts_zscore(F,52)` | subindustry | 自身历史标准化 |
| T3 | `ts_rank(F,52)` | subindustry | 分位 |
| T4 | `ts_quantile(F,52)` | subindustry | 分位（高斯） |
| T5 | `ts_sum(F,10)` | subindustry | 基线核（论坛短窗） |
| T6 | `ts_mean(F,10)` | subindustry | 平滑 |
| T7 | `ts_std_dev(F,52)` | subindustry | 二阶波动 |
| T8 | `ts_av_diff(F,10)` | subindustry | 一阶差 |
| T9 | `ts_ir(F,52)` | sector | 轴对照 |
| T10 | `ts_ir(F,52)` | industry | 轴对照 |

外层统一 `reverse(group_rank(·, axis))`；**不发**任何 `add(独立腿)`。

---

## 5. 判定与下一步

- 全闸（IS）：S≥1.585、F≥1.0、TO∈[0.05,0.70]、sub 比值过、2Y 分档（2Y≥1.58 ⇒ limit 2.02，真值需 ≥2.025）。
- prod/self：prod<0.70（严格）、self<0.70；**逐颗实测**。
- 逐年：10/10 年 lc+sc>0 且 pnl>0；任一空窗/负年一票否决。
- 同塔三席需两两互相关 <0.5（点亮 risk 塔）。
- 交付前用户确认；未确认不调用 `workflow_submit_alpha`。
