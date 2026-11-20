# EUR / insider_agg_matrix 全字段画像（INSIDERS (EUR/D1 2/3 未点亮)）

> 画像日期 2026-11-18 · 数据源 `mcp__wq-brain-http__get_datafields` （region=EUR, universe=TOPCS1600, delay=1, 全量 complete=True, platform_count=34）
> 命名规则：`eur_<category>_<dataset>_profile_<YYYYMMDD>.md`；原始目录 `tracking/EUR/reference/fields/<ds>_eur_d1.json`
> 机制定位：内部人交易聚合（董事/高管买卖股数）；MATRIX；有效读数=total_top_buy_shares−total_top_sell_shares 净买入（prod 墙 0.76-0.80，需罕见形态）

---

## 1. 字段全表（平台全量，逐字段无通配）

| 字段 | 类型 | 覆盖率 | αC | 更新频率 | 分布特征 | 可用性/适用性 |
|---|---|---|---|---|---|---|
| `avg_buy_shares` | MATRIX | 0.6083 | 154 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_secondary_buy_shares` | MATRIX | 0.6083 | 48 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_secondary_sell_shares` | MATRIX | 0.6083 | 48 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_secondary_top_buy_shares` | MATRIX | 0.6083 | 49 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_secondary_top_sell_shares` | MATRIX | 0.6083 | 52 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_sell_shares` | MATRIX | 0.6083 | 65 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_top_buy_shares` | MATRIX | 0.6083 | 84 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `avg_top_sell_shares` | MATRIX | 0.6083 | 121 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 均值族：与 total_ 同族，TO 高，备选不优先 |
| `directional_indicator` | MATRIX | 0.6083 | 89 | 日频快照（平台每日更新） | 方向指示（离散取值） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `directional_indicator_2` | MATRIX | 0.6149 | 46 | 日频快照（平台每日更新） | 方向指示（离散取值） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `directional_significant_value_1` | MATRIX | 0.6149 | 8 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `directional_significant_value_2` | MATRIX | 0.6149 | 6 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `directional_significant_value_3` | MATRIX | 0.6149 | 5 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `directional_significant_value_4` | MATRIX | 0.6149 | 39 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `significant_value_1` | MATRIX | 0.6149 | 71 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `significant_value_2` | MATRIX | 0.6149 | 42 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `significant_value_3` | MATRIX | 0.6149 | 54 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `significant_value_4` | MATRIX | 0.6149 | 58 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_directional_significant_value_1` | MATRIX | 0.6149 | 42 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_directional_significant_value_2` | MATRIX | 0.6149 | 31 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_directional_significant_value_3` | MATRIX | 0.6149 | 45 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_directional_significant_value_4` | MATRIX | 0.6149 | 31 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_significant_value_1` | MATRIX | 0.6149 | 63 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_significant_value_2` | MATRIX | 0.6149 | 17 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_significant_value_3` | MATRIX | 0.6149 | 150 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `top_significant_value_4` | MATRIX | 0.6149 | 142 | 日频快照（平台每日更新） | 市值金额（右偏重尾，需 rank/log 压缩） | 极值/方向族：事件型稀疏，可试 !=0 掩码降 TO |
| `total_buy_shares` | MATRIX | 0.6083 | 74 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 辅助/待实测 |
| `total_secondary_buy_shares` | MATRIX | 0.6083 | 47 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 副读数：董事净买入，与 total_top 同族互相关极高，只取一 |
| `total_secondary_sell_shares` | MATRIX | 0.6083 | 41 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 副读数：董事净买入，与 total_top 同族互相关极高，只取一 |
| `total_secondary_top_buy_shares` | MATRIX | 0.6083 | 42 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 副读数：董事净买入，与 total_top 同族互相关极高，只取一 |
| `total_secondary_top_sell_shares` | MATRIX | 0.6083 | 46 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 副读数：董事净买入，与 total_top 同族互相关极高，只取一 |
| `total_sell_shares` | MATRIX | 0.6083 | 72 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 辅助/待实测 |
| `total_top_buy_shares` | MATRIX | 0.6083 | 162 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 主信号读数：高管净买入 (buy−sell)/ts_sum，配罕见慢腿破 prod 墙 |
| `total_top_sell_shares` | MATRIX | 0.6083 | 177 | 日频快照（平台每日更新） | 股数（右偏重尾，事件型稀疏非零） | 主信号读数：高管净买入 (buy−sell)/ts_sum，配罕见慢腿破 prod 墙 |

## 2. 全字段覆盖率实测读数（平台 cov，全量 complete=true）

> 本表逐字段给出平台覆盖率数值读数（`complete=true` 的全量目录，无抽样）。
> 覆盖率是选取与 sub 闸可达性的第一判据：cov<0.85 时 sub 闸结构性不可达。

| 字段 | 覆盖率实测 | αC | 拥挤度判定 |
|---|---|---|---|
| `avg_buy_shares` | 0.6083 | 154 | 低（prod 友好） |
| `avg_secondary_buy_shares` | 0.6083 | 48 | 低（prod 友好） |
| `avg_secondary_sell_shares` | 0.6083 | 48 | 低（prod 友好） |
| `avg_secondary_top_buy_shares` | 0.6083 | 49 | 低（prod 友好） |
| `avg_secondary_top_sell_shares` | 0.6083 | 52 | 低（prod 友好） |
| `avg_sell_shares` | 0.6083 | 65 | 低（prod 友好） |
| `avg_top_buy_shares` | 0.6083 | 84 | 低（prod 友好） |
| `avg_top_sell_shares` | 0.6083 | 121 | 低（prod 友好） |
| `directional_indicator` | 0.6083 | 89 | 低（prod 友好） |
| `directional_indicator_2` | 0.6149 | 46 | 低（prod 友好） |
| `directional_significant_value_1` | 0.6149 | 8 | 低（prod 友好） |
| `directional_significant_value_2` | 0.6149 | 6 | 低（prod 友好） |
| `directional_significant_value_3` | 0.6149 | 5 | 低（prod 友好） |
| `directional_significant_value_4` | 0.6149 | 39 | 低（prod 友好） |
| `significant_value_1` | 0.6149 | 71 | 低（prod 友好） |
| `significant_value_2` | 0.6149 | 42 | 低（prod 友好） |
| `significant_value_3` | 0.6149 | 54 | 低（prod 友好） |
| `significant_value_4` | 0.6149 | 58 | 低（prod 友好） |
| `top_directional_significant_value_1` | 0.6149 | 42 | 低（prod 友好） |
| `top_directional_significant_value_2` | 0.6149 | 31 | 低（prod 友好） |
| `top_directional_significant_value_3` | 0.6149 | 45 | 低（prod 友好） |
| `top_directional_significant_value_4` | 0.6149 | 31 | 低（prod 友好） |
| `top_significant_value_1` | 0.6149 | 63 | 低（prod 友好） |
| `top_significant_value_2` | 0.6149 | 17 | 低（prod 友好） |
| `top_significant_value_3` | 0.6149 | 150 | 低（prod 友好） |
| `top_significant_value_4` | 0.6149 | 142 | 低（prod 友好） |
| `total_buy_shares` | 0.6083 | 74 | 低（prod 友好） |
| `total_secondary_buy_shares` | 0.6083 | 47 | 低（prod 友好） |
| `total_secondary_sell_shares` | 0.6083 | 41 | 低（prod 友好） |
| `total_secondary_top_buy_shares` | 0.6083 | 42 | 低（prod 友好） |
| `total_secondary_top_sell_shares` | 0.6083 | 46 | 低（prod 友好） |
| `total_sell_shares` | 0.6083 | 72 | 低（prod 友好） |
| `total_top_buy_shares` | 0.6083 | 162 | 低（prod 友好） |
| `total_top_sell_shares` | 0.6083 | 177 | 低（prod 友好） |

## 3. 六维画像汇总

- **字段类型**：全部 MATRIX（34 字段）
- **覆盖率**：min 0.6083 / median 0.6149 / max 0.6149；存在 34 个字段 cov<0.85（sub 闸不可达，排除主信号）
- **更新频率**：报告期聚合、日频快照（由字段描述 reporting period/date 推断）
- **分布特征**：计数/家数右偏零膨胀、市值/股数重尾、极值/方向族稀疏（详见 §1 逐字段）
- **可用性（拥挤度）**：αC min 5 / median 49 / max 177
- **潜在 alpha 适用性**：见 §1 每行适用性列；历史实证 alpha id 见 §4

## 4. 历史实证（EUR 本塔，供模板匹配）

| alpha id | 结构 | S/F/2Y | prod | 塔 |
|---|---|---|---|---|
| `VkxN0mMJ` | group_rank(ts_sum(top_buy−top_sell,63),industry) | 2.00/1.03/1.79 | 0.7647 ❌ | INSIDERS |
| `xArv58Am` | 主+次高管净买入加权 | 1.97/1.01/1.67 | 未测 | INSIDERS |
> ⚠ 该族裸 net-buy 读数 prod 0.76-0.80 撞墙；按 SOP §16 需换罕见形态（ts_delta 月级 / ts_mean 504 慢腿）或换字段，勿在拥挤形态上磨参数。

## 5. 归档与复现

- 原始全量目录：`tracking/EUR/reference/fields/insider_agg_matrix_eur_d1.json`
- 本画像：`tracking/EUR/reference/profiles/eur_insiders_insider_agg_matrix_profile_20261118.md`
- 完整性闸：`python tools/gates/field_profile_completeness_gate.py --profile <本文件>`
