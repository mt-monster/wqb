# GBR / risk72（Specific return of extended factors，扩展因子的特质收益面板）

> 塔：**risk**（GBR/D1，当前 **0/3 未点亮**；乘数 1.2/1.3）
> 画像日期 2026-11-24 · 数据源 `mcp__wq-brain-http__get_datafields(region=GBR, dataset_id=risk72, universe=TOP700, delay=1, filter_sharpe=false)`
> 平台实拉：`count=23 / platform_count=23 / returned=23 / complete=true / pages_fetched=1`（单页全量）
> ⚠ 全部字段 `coverage=0.0` 是 **GBR coverage 元数据盲区**，不等于无数据：同族 `rsk68_*` 与 `top2500_equity_residualized_return` 已有大量回测（lc 316–911）与全闸件（`WjlOZZnd`）。
> ⚠ 混合类型：MATRIX 16 + VECTOR 7（`cfg2_*_replicator*`）⇒ VECTOR 必须先 `vec_avg`/`vec_sum` 折叠，不得原生进 `rank`。

---

## 字段全表（平台实拉 23/23）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `ats_top1200_equity_residualized_return` | MATRIX | 0.0 | 21 | 20 | ATS 宇宙 top1200 的特质收益 |
| `ats_top800_equity_residualized_return` | MATRIX | 0.0 | 5 | 4 | ATS 宇宙 top800 的特质收益 |
| `cfg2_top1200_replicator1` | VECTOR | 0.0 | 11 | 9 | 配置 2 · top1200 第一复制子值 |
| `cfg2_top1200_replicator2` | VECTOR | 0.0 | 4 | 4 | 配置 2 · top1200 第二复制子值 |
| `cfg2_top1200_residual_return` | MATRIX | 0.0 | 5 | 5 | EUR top1200 残差收益（市场/国家/行业/MFM1 剥离，百分比） |
| `cfg2_top600_replicator1` | VECTOR | 0.0 | 0 | 0 | 配置 2 · top600 第一复制子值 |
| `cfg2_top600_replicator2` | VECTOR | 0.0 | 1 | 1 | 配置 2 · top600 第二复制子值 |
| `cfg2_top600_residual_return` | MATRIX | 0.0 | 3 | 3 | EUR top600 残差收益（同上） |
| `cfg2_top800_replicator1` | VECTOR | 0.0 | 2 | 2 | 配置 2 · top800 第一复制子值 |
| `cfg2_top800_replicator2` | VECTOR | 0.0 | 3 | 3 | 配置 2 · top800 第二复制子值 |
| `cfg2_top800_residual_return` | MATRIX | 0.0 | 3 | 3 | EUR top800 残差收益（同上） |
| `epp_equity_minvol1m_residual_return` | MATRIX | 0.0 | 36 | 29 | EPP 最低 1M 流动性宇宙的特质收益 |
| `eur_equity_minvol1m_residual_return` | MATRIX | 0.0 | 61 | 46 | EUR 最低 1M 流动性宇宙的特质收益 |
| `eur_equity_minvol1m_residual_return_validated` | MATRIX | 0.0 | 16 | 14 | 同上，当日校验版 |
| `top1200_equity_residualized_return` | MATRIX | 0.0 | 9 | 7 | 所选宇宙 top1200 特质收益 |
| `top1200_equity_residualized_return_nogroup` | MATRIX | 0.0 | 13 | 13 | top1200 特质收益（无分组调整） |
| `top2500_equity_residualized_return` | MATRIX | 0.0 | 264 | 168 | 所选宇宙 top2500 特质收益（全集 αC 最高） |
| `top2500_equity_residualized_return_nogroup` | MATRIX | 0.0 | 238 | 136 | top2500 特质收益（无分组调整；论坛同域配方字段） |
| `top600_equity_residualized_return` | MATRIX | 0.0 | 7 | 6 | 所选宇宙 top600 特质收益 |
| `top600_equity_residualized_return_nogroup` | MATRIX | 0.0 | 5 | 5 | top600 特质收益（无分组调整） |
| `top600_reproducible_specific_return` | MATRIX | 0.0 | 2 | 2 | AMR top600 可复现特质收益（MFM1/D1） |
| `top800_equity_residualized_return` | MATRIX | 0.0 | 5 | 5 | 所选宇宙 top800 特质收益 |
| `top800_equity_residualized_return_nogroup` | MATRIX | 0.0 | 4 | 4 | top800 特质收益（无分组调整） |

---

## 聚合统计

| 指标 | 值 |
|---|---|
| 字段总数 | 23（MATRIX 16 / VECTOR 7） |
| coverage 分布 | 23/23 = 0.0（GBR 元数据盲区） |
| alphaCount 合计 / 均值 | 479 / **20.8** |
| alphaCount 最大 / 最小 | 264（`top2500_equity_residualized_return`）/ 0（`cfg2_top600_replicator1`） |
| userCount 合计 / 均值 | 325 / **14.1** |
| dateCreated | 23/23 = `2026-07-01`（同批 onboard） |
| 数据集级 | `name=Specific return of extended factors` / `category=risk` / `coverage=0.0` / `userCount=342` / `alphaCount=697` / `valueScore=2.0` / `pyramidMultiplier=1.2` |

---

## 字段族拆解（按经济机制）

| 族 | 字段 | 机制 |
|---|---|---|
| **A 宇宙规模残差收益（分组版）** | `top600/top800/top1200/top2500_equity_residualized_return`、`ats_top800/1200_...`、`epp/eur_minvol1m_...`、`cfg2_top600/800/1200_residual_return` | 风险模型剥离市场/国家/行业/风格后的个股特质收益；**核心机制 = 特质收益反转** |
| **B 宇宙规模残差收益（无分组版）** | `top600/top800/top1200/top2500_equity_residualized_return_nogroup` | 同上但不做组内调整；论坛 44639524994583 的 GBR 同域配方用此字段 |
| **C 复制子（VECTOR）** | `cfg2_top600/top800/top1200_replicator1/2` | 配置 2 的两个复制子值（截面/时序因子复制），VECTOR 需折叠 |
| **D 可复现特质收益** | `top600_reproducible_specific_return` | AMR MFM1/D1 可复现版，地域口径与 GBR 不同 |

> **机制不互异**：A/B/C/D 都是「特质收益」的宇宙/配置变体，**同一经济机制**（残差反转）。按 AGENTS §7.6 D1「换宇宙/换配置不算结构互异模板」——它们只能提供「同机制不同持仓」的**分散器**，不能算 10 个独立机制。

---

## 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可做信号** | A/B/D 全部 MATRIX（18 个） | 特质收益是零均值 decimal 截面量，已无量纲，可直接 `rank`/`group_rank`/`ts_zscore` |
| **② 需折叠后可用** | `cfg2_*_replicator1/2`（7 个 VECTOR） | 先 `vec_avg`（默认）或 `vec_sum` 折叠；`vec_avg≡vec_sum` 仅在单元素时成立 |
| **③ 元数据/盲区** | 全 23 字段 cov=0.0 | GBR 元数据盲区，非无数据；以探针 `longCount+shortCount>0` 判存在性 |

### 10.1 全字段实测（risk72，`rank(ts_backfill(F,250))` @NONE/decay0/trunc0/nanOFF，GBR/TOP700/D1）

> 探针批次：`gxvmf3pu4JkbByS64694P2`（前 10 字段）+ `待填 B`（中 10）+ `待填 C`（后 3）。
> 判据：`longCount+shortCount>0` = 有数据；`PROBE_FAILED`（读不到）≠ `NO_DATA`。

| 字段 | 类型 | longCount | shortCount | 有数据 | 备注 |
|---|---|---:|---:|---|---|
| `ats_top1200_equity_residualized_return` | MATRIX | 待填 | 待填 | 待填 | 批 A |
| `ats_top800_equity_residualized_return` | MATRIX | 待填 | 待填 | 待填 | 批 A |
| `cfg2_top1200_replicator1` | VECTOR | 待填 | 待填 | 待填 | 批 A（vec_avg） |
| `cfg2_top1200_replicator2` | VECTOR | 待填 | 待填 | 待填 | 批 A（vec_avg） |
| `cfg2_top1200_residual_return` | MATRIX | 待填 | 待填 | 待填 | 批 A |
| `cfg2_top600_replicator1` | VECTOR | 待填 | 待填 | 待填 | 批 A（vec_avg；αC=0 冷字段） |
| `cfg2_top600_replicator2` | VECTOR | 待填 | 待填 | 待填 | 批 A（vec_avg） |
| `cfg2_top600_residual_return` | MATRIX | 待填 | 待填 | 待填 | 批 A |
| `cfg2_top800_replicator1` | VECTOR | 待填 | 待填 | 待填 | 批 A（vec_avg） |
| `cfg2_top800_replicator2` | VECTOR | 待填 | 待填 | 待填 | 批 A（vec_avg） |
| `cfg2_top800_residual_return` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `epp_equity_minvol1m_residual_return` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `eur_equity_minvol1m_residual_return` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `eur_equity_minvol1m_residual_return_validated` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top1200_equity_residualized_return` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top1200_equity_residualized_return_nogroup` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top2500_equity_residualized_return` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top2500_equity_residualized_return_nogroup` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top600_equity_residualized_return` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top600_equity_residualized_return_nogroup` | MATRIX | 待填 | 待填 | 待填 | 批 B |
| `top600_reproducible_specific_return` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `top800_equity_residualized_return` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `top800_equity_residualized_return_nogroup` | MATRIX | 待填 | 待填 | 待填 | 批 C |

---

## 历史与先验

- **同族全闸件（2026-11-20）**：`WjlOZZnd = reverse(group_rank(vector_neut(ts_sum(top2500_equity_residualized_return,10), ts_backfill(rsk68_weight_volatility_short,120)), market))` @SUBINDUSTRY/decay56/trunc0.08 → **S1.76 / F1.42 / 2Y2.14 / TO9.96% / RA fails=0 / 10 年逐年全正**；pyramid=`GBR/D1/RISK`（effective=1）；**self 0.5796 PASS / prod 0.7987 FAIL**（prod 直方图主体 ≤0.6，仅 [0.7,0.8) 9 颗小簇）。
- **论坛同域先验（44639524994583，2026-10-29）**：GBR/TOP700 用 `residualized_return_nogroup` + 52 日窗 t 值 + 三子窗一致性门控，IS S1.77/F1.01/TO15.8%，**prodCorr 0.648**；作者明确「风险残差反转方向在生产池相当拥挤，继续走要换表达、不是调参数」。
- **论文**：Idiosyncratic Volatility / Return Reversal 系列（Crossref 5 篇 / 5 作者，2026-11-24 实跑 `paper_search.py --diverse`），支持「特质波动/残差反转」的截面预测机制。
- **风险模型中性化**：论坛 45235010628247（2026-11-23）给出 `vector_neut(alpha, factor)` / `regression_neut(alpha, factor)` 先做因子剥离再换设置档的流程；GBR 可选档含 CROWDING / SLOW_AND_FAST（见 GBR skill）。

## 适用性结论（待探针与批次回填）

- **机制层**：单一「特质收益反转」机制；宇宙规模/分组与否/复制子只是**同机制不同持仓**。
- **正解方向**：先换表达（t 值代理 / 门控 / 残差化轴），不先扫参数；prod 0.7987 是当前唯一硬缺口。
- **风险**：论坛作者同形态 prod 0.648 已贴红线；我方同族不同表达必须**逐颗实测 prod**，不得由 IS 推断。
