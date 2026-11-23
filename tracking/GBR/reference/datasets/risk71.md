# GBR / risk71（Daily Specific Return Profiling Dataset，日度特质收益画像）

> 塔：**risk**（GBR/D1，当前 **0/3 未点亮**；乘数 1.2/1.3）
> 画像日期 2026-11-24 · 数据源 `mcp__wq-brain-http__get_datafields(region=GBR, dataset_id=risk71, universe=TOP700, delay=1, filter_sharpe=false)`
> 平台实拉：`count=6 / platform_count=6 / returned=6 / complete=true / pages_fetched=1`
> ⚠ 6/6 字段 `coverage=0.0` 是 GBR 元数据盲区；以探针持仓判存在性。

---

## 字段全表（平台实拉 6/6）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `epp_minvol1m_specific_return_dsrt` | MATRIX | 0.0 | 30 | 26 | EPP 最低 1M 流动性宇宙的特质收益（可复现） |
| `eur_minvol1m_specific_return_dsrt` | MATRIX | 0.0 | 36 | 28 | EUR 最低 1M 流动性宇宙的特质收益（可复现） |
| `residualized_return_top2500` | MATRIX | 0.0 | 625 | 294 | EUR TOP2500 ATS 宇宙 · MFM2 风险模型日度特质收益（全表最活跃） |
| `residualized_return_top600_ats` | MATRIX | 0.0 | 9 | 7 | AMR TOP600 宇宙 · MFM2 风险模型日度特质收益 |
| `top1200_residual_return_dsrt` | MATRIX | 0.0 | 15 | 11 | 所选宇宙 top1200 可复现特质收益 |
| `top800_residual_return_dsrt` | MATRIX | 0.0 | 6 | 6 | 所选宇宙 top800 可复现特质收益 |

---

## 聚合统计

| 指标 | 值 |
|---|---|
| 字段总数 | 6（全部 MATRIX，无 VECTOR/GROUP） |
| coverage 分布 | 6/6 = 0.0（GBR 元数据盲区） |
| alphaCount 合计 / 均值 | 721 / **120.2** |
| alphaCount 最大 / 最小 | 625（`residualized_return_top2500`）/ 6（`top800_residual_return_dsrt`） |
| userCount 合计 / 均值 | 372 / **62** |
| dateCreated | 6/6 = `2026-07-01` |
| 数据集级 | `name=Daily Specific Return Profiling Dataset` / `category=risk` / `coverage=0.0` / `userCount=343` / `alphaCount=744` / `valueScore=2.0` / `pyramidMultiplier=1.2` |

---

## 字段族拆解（按经济机制）

| 族 | 字段 | 机制 |
|---|---|---|
| **A EUR 大盘 MFM2** | `residualized_return_top2500` | EUR TOP2500 ATS 的 MFM2 特质收益（与 risk72 的 `top2500_equity_residualized_return` 高度同源） |
| **B AMR 大盘 MFM2** | `residualized_return_top600_ats` | AMR TOP600 的 MFM2 特质收益 |
| **C 可复现 DSRT 变体** | `epp/eur_minvol1m_specific_return_dsrt`、`top1200/top800_residual_return_dsrt` | 可复现版（当日校验/DSRT 口径），宇宙与 risk72 的 topN 对应 |

> 与 risk72 的 `top2500_equity_residualized_return` 属**同一机制、不同厂商/风险模型口径**。按 D1 口径不构成独立结构模板，只作「同机制分散器」。

---

## 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可做信号** | 6/6 MATRIX | 特质收益零均值 decimal，可直接 `rank`/`group_rank`/`ts_zscore` |
| **② 需折叠** | 无 | 无 VECTOR |
| **③ 盲区** | 6/6 cov=0.0 | 元数据盲区；探针判存在性 |

### 10.1 全字段实测（risk71，`rank(ts_backfill(F,250))` @NONE/decay0/trunc0/nanOFF，GBR/TOP700/D1）

> 探针批次：批 C（`待填`）。判据：`longCount+shortCount>0` = 有数据。

| 字段 | 类型 | longCount | shortCount | 有数据 | 备注 |
|---|---|---:|---:|---|---|
| `epp_minvol1m_specific_return_dsrt` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `eur_minvol1m_specific_return_dsrt` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `residualized_return_top2500` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `residualized_return_top600_ats` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `top1200_residual_return_dsrt` | MATRIX | 待填 | 待填 | 待填 | 批 C |
| `top800_residual_return_dsrt` | MATRIX | 待填 | 待填 | 待填 | 批 C |

---

## 历史与先验

- **风险塔全闸首件来自 risk72（WjlOZZnd）**：S1.76/F1.42/2Y2.14，prod 0.7987（唯一缺口）。risk71 的 `residualized_return_top2500` 与它同机制，可作为**换持仓分散器**。
- **risk71/72 历史消费**：`risk71` 15 条回测 / `risk72` 8 条（DB `get_mining_yield`），均 0 过闸——**唯一全闸件是 2026-11-20 之后的 WjlOZZnd**，说明旧读数（2026-11-14 前）不代表当前平台。
- **论坛/论文**：同 risk72（44639524994583 / 45235010628247 / 特质波动反转论文 5 篇）。

## 适用性结论（待探针回填）

- **机制**：与 risk72 同属「特质收益反转」，只作风险塔的第二/第三腿分散器，不作新机制。
- **优先级**：risk71 只保留 `residualized_return_top2500`（αC 625）与 `residualized_return_top600_ats`（唯一 AMR 口径）两条；其余 4 条同源变体仅作覆盖。
