# USA · fundamental14 字段画像（已退役）

> 快照日 2026-10-23。**结论：本数据集在本战役的用途已被 wave 93 实测否定**，本文件保留为
> 「按错误拥挤度数字误入、用一波 20 臂实测纠正」的审计痕迹，不作为可再挖的选集依据。
> 数据集层面的替代选择仍按 [`_usa-fundamental-universe-scan-20261023.md`](_usa-fundamental-universe-scan-20261023.md) §3：`other416`。

## 1. 数据集身份

| 项 | 值 | 来源 |
|---|---|---|
| dataset id | `fundamental14` | `get_datasets`（USA，166 个数据集） |
| 字段数 | 248，**全部 VECTOR** | `get_datafields`（`type=VECTOR`） |
| 数据集级覆盖率 | 0.886 | 同上 |
| 覆盖率 ≥ 0.95 的字段数 | 185 | 本地目录解析 |
| **alphaCount** | **7574** | `get_datasets` |
| **userCount** | **1478** | 同上 |
| 拥挤度判定 | **饱和**（战役自定的饱和线是 aC ≥ 1 万；7574 已属扫描文档 §2 明示的拒绝档） | 扫描文档 |

### 1.1 一次必须留痕的认知错误

本战役在 wave 93 之前把 `fundamental14` 的拥挤度记成 **aC 1182**，并据此认定「未被充分挖掘」。
该数字**是错的**：平台实测为 **aC 7574 / 1478 users**。扫描文档 §2 早已把本数据集标为 `✗ 饱和`，
即 **wave 93 是建在一个被本战役自己的扫描文档否决过的前提上开的**。

教训（可复用）：**字段级的低 aC 不能推出数据集级不拥挤**。wave 93 用的 14 个字段 aC 只有 9–62，
但数据集整体已被 1478 个用户用过——平台的 alphaCount 是**按数据集累计**的，字段稀疏只说明
「这些具体列没被单独当信号」，不说明「这个数据集的认知已被定价」。选集决策必须读数据集级 aC。

## 2. 构造族（wave 93 实际使用的 6 族）

全部字段均为 VECTOR，必须先 `vec_*` 聚合才能进常规算子（铁律，见 `wq-operator-playbook-by-gate` §2.5）。
本波只用了 `vec_avg`。

| 族 | 字段（示例） | 经济含义 | 覆盖率 |
|---|---|---|---|
| 审计费用结构 | `latest_non_audit_fees_sum` / `latest_total_fees_sum` / `latest_audit_related_fees_sum` / `latest_tax_fees_sum` | 非审计服务占比 → 审计独立性 / 代理成本 | ≥ 0.95 |
| 峰值比（最新 / 历史高点） | `revenue_ttm` / `net_income_ttm` / `book_value` / `total_assets` 的 latest−hiwater 比 | 经营是否处于历史高位（均值回复） | ≥ 0.95 |
| 应计 | `(CFO − NI) / total_assets` | Sloan (1996) 应计异象 | ≥ 0.95 |
| 外部融资 | `CFF / total_assets` | 外部融资异象 | ≥ 0.95 |

## 3. wave 93 实测（20 臂，全部失败）

设置：USA/D1，2 个宇宙 × 10 臂，`STATISTICAL` 中性化，decay 0，truncation 0.08，2014-01-01 → 2023-12-31。
统一壳：`ts_decay_linear(group_rank(ts_zscore(ts_backfill(winsorize(<ratio>, std=4), 252), 252), industry), 20)`。

| 指标 | TOP2000 | TOP3000 |
|---|---|---|
| Sharpe 区间 | −0.05 … 0.70 | −0.32 … 0.84 |
| 换手 | 0.043 … 0.057 | 同量级 |
| 通过 RA 项 | 0 | 0 |
| 主失败项 | `LOW_SHARPE`（全部 10 臂） | 同 |

三条归因（这是本波唯一有价值的产出）：

1. **年度近常数比率 + `ts_zscore(252)` = 噪声放大**。这些比率一年只变一次，252 日 z-score 的
   分母主要是跳变后的方差，信号逐日几乎不动，`decay=20` 之后换手只剩 4–5%。
2. **换手 < 0.125 会把 fitness 结构性压死**。平台 `F = S · sqrt(|RET| / max(TO, 0.125))`，
   TO ≈ 0.05 时 fitness 上限 ≈ 0.63·S，即 S 必须 > 2.5 才可能过 F 线——本族连 S 都没到 1。
3. **同一字段在两个宇宙换号**（非审计占比臂 TOP2000 −0.32 / TOP3000 +0.13）⇒ 信号不是弱，是噪声。

## 4. 结论

- **不再用 `fundamental14` 开波**。判死粒度 = 数据集级（构造族无一存活，且原因在「年度稀疏 + 已被 1478 用户定价」，
  换壳 / 换算子都改不了）。
- 若要引用，引用的是本文件的**方法学**：① 选集先读数据集级 aC；② 年度频率字段不要套 252 日 z-score；
  ③ 低换手族的 fitness 天花板必须开波前算一遍。
