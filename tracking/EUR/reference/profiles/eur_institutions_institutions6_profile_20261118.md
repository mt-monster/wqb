# EUR / institutions6 全字段画像（INSTITUTIONS (EUR/D1 0/3 未点亮)）

> 画像日期 2026-11-18 · 数据源 `mcp__wq-brain-http__get_datafields` （region=EUR, universe=TOPCS1600, delay=1, 全量 complete=True, platform_count=11）
> 命名规则：`eur_<category>_<dataset>_profile_<YYYYMMDD>.md`；原始目录 `tracking/EUR/reference/fields/<ds>_eur_d1.json`
> 机制定位：机构持仓家数/股数/市值族；MATRIX 免 vec 包装；本塔主阵地，已验证小腿 leAXvaLn/N1NGbddg（机构家数不对称×分析师修正强腿）

---

## 1. 字段全表（平台全量，逐字段无通配）

| 字段 | 类型 | 覆盖率 | αC | 更新频率 | 分布特征 | 可用性/适用性 |
|---|---|---|---|---|---|---|
| `aggregate_equity_value_all_owners` | MATRIX | **0.9976** | 132 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 水平量：仅作规模归一分母或分组轴，不作主信号（ATOM 判死） |
| `aggregate_equity_value_institutions` | MATRIX | **0.9976** | 120 | 季/报告期（13F/持股披露节奏），日频快照 | 市值金额（右偏重尾，需 rank/log 压缩） | 水平量：仅作规模归一分母或分组轴，不作主信号（ATOM 判死） |
| `aggregate_share_count_all_owners` | MATRIX | **0.9976** | 266 | 日频快照（平台每日更新） | 计数/家数（右偏、零膨胀，多为非负整数） | 水平量：仅作规模归一分母或分组轴，不作主信号（ATOM 判死） |
| `aggregate_share_count_institutions` | MATRIX | **0.9976** | 131 | 季/报告期（13F/持股披露节奏），日频快照 | 计数/家数（右偏、零膨胀，多为非负整数） | 水平量：仅作规模归一分母或分组轴，不作主信号（ATOM 判死） |
| `count_institutional_buyers_security` | MATRIX | **0.9976** | 382 | 季/报告期（13F/持股披露节奏），日频快照 | 计数/家数（右偏、零膨胀，多为非负整数） | 小腿首选：家数不对称 (buyers−sellers)/holders，配 analyst 修正强腿点 INSTITUTIONS 塔 |
| `count_institutional_holders_security` | MATRIX | **0.9976** | 196 | 季/报告期（13F/持股披露节奏），日频快照 | 计数/家数（右偏、零膨胀，多为非负整数） | 小腿首选：家数不对称 (buyers−sellers)/holders，配 analyst 修正强腿点 INSTITUTIONS 塔 |
| `count_institutional_sellers_security` | MATRIX | **0.9976** | 362 | 季/报告期（13F/持股披露节奏），日频快照 | 计数/家数（右偏、零膨胀，多为非负整数） | 小腿首选：家数不对称 (buyers−sellers)/holders，配 analyst 修正强腿点 INSTITUTIONS 塔 |
| `market_value_institutional_shares_acquired` | MATRIX | **0.9976** | 172 | 季/报告期（13F/持股披露节奏），日频快照 | 市值金额（右偏重尾，需 rank/log 压缩） | 小腿备选：机构资金流市值/股数净额；作门控或分组，ATOM 强度不足 |
| `market_value_institutional_shares_disposed` | MATRIX | **0.9307** | 113 | 季/报告期（13F/持股披露节奏），日频快照 | 市值金额（右偏重尾，需 rank/log 压缩） | 小腿备选：机构资金流市值/股数净额；作门控或分组，ATOM 强度不足 |
| `quantity_institutional_shares_acquired` | MATRIX | **0.9976** | 175 | 季/报告期（13F/持股披露节奏），日频快照 | 计数/家数（右偏、零膨胀，多为非负整数） | 小腿备选：机构资金流市值/股数净额；作门控或分组，ATOM 强度不足 |
| `quantity_institutional_shares_disposed` | MATRIX | **0.9970** | 158 | 季/报告期（13F/持股披露节奏），日频快照 | 计数/家数（右偏、零膨胀，多为非负整数） | 小腿备选：机构资金流市值/股数净额；作门控或分组，ATOM 强度不足 |

## 2. 全字段覆盖率实测读数（平台 cov，全量 complete=true）

> 本表逐字段给出平台覆盖率数值读数（`complete=true` 的全量目录，无抽样）。
> 覆盖率是选取与 sub 闸可达性的第一判据：cov<0.85 时 sub 闸结构性不可达。

| 字段 | 覆盖率实测 | αC | 拥挤度判定 |
|---|---|---|---|
| `aggregate_equity_value_all_owners` | 0.9976 | 132 | 低（prod 友好） |
| `aggregate_equity_value_institutions` | 0.9976 | 120 | 低（prod 友好） |
| `aggregate_share_count_all_owners` | 0.9976 | 266 | 低（prod 友好） |
| `aggregate_share_count_institutions` | 0.9976 | 131 | 低（prod 友好） |
| `count_institutional_buyers_security` | 0.9976 | 382 | 低（prod 友好） |
| `count_institutional_holders_security` | 0.9976 | 196 | 低（prod 友好） |
| `count_institutional_sellers_security` | 0.9976 | 362 | 低（prod 友好） |
| `market_value_institutional_shares_acquired` | 0.9976 | 172 | 低（prod 友好） |
| `market_value_institutional_shares_disposed` | 0.9307 | 113 | 低（prod 友好） |
| `quantity_institutional_shares_acquired` | 0.9976 | 175 | 低（prod 友好） |
| `quantity_institutional_shares_disposed` | 0.9970 | 158 | 低（prod 友好） |

## 3. 六维画像汇总

- **字段类型**：全部 MATRIX（11 字段）
- **覆盖率**：min 0.9307 / median 0.9976 / max 0.9976；全部 ≥0.85，sub 闸可达
- **更新频率**：报告期聚合、日频快照（由字段描述 reporting period/date 推断）
- **分布特征**：计数/家数右偏零膨胀、市值/股数重尾、极值/方向族稀疏（详见 §1 逐字段）
- **可用性（拥挤度）**：αC min 113 / median 172 / max 382
- **潜在 alpha 适用性**：见 §1 每行适用性列；历史实证 alpha id 见 §4

## 4. 历史实证（EUR 本塔，供模板匹配）

| alpha id | 结构 | S/F/2Y | prod |塔 |
|---|---|---|---|---|
| `N1NGbddg` | analyst ebi 修正广度强腿 + 1.2×机构家数不对称小腿 | 1.69/1.05/2.17 | 0.6872 ✅ | INSTITUTIONS+ANALYST |
| `leAXvaLn` | analyst 修正 + 机构资金流小腿 | 已提交 | — | INSTITUTIONS |
| `E56POx59` | analyst ebt 修正 + 机构家数小腿 | 1.87/1.23/2.47 | 0.8106 ❌ | INSTITUTIONS |

## 5. 归档与复现

- 原始全量目录：`tracking/EUR/reference/fields/institutions6_eur_d1.json`
- 本画像：`tracking/EUR/reference/profiles/eur_institutions_institutions6_profile_20261118.md`
- 完整性闸：`python tools/gates/field_profile_completeness_gate.py --profile <本文件>`
