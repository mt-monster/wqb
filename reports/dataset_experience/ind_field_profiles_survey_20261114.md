# IND 逐 category 全字段静态画像总表 · 2026-11-14

> 仿 `reports/dataset_experience/gbr_field_profiles_survey_20261109.md`。命名规则：`<region小写>_<主题>_survey_<YYYYMMDD>.md`，路径纯 ASCII，区域码大写豁免仅用于独立区域目录。

## 0 三条须知

- `coverage` 不等于任意时点有值股票数（VECTOR 尤甚），可用性须看探针 `longCount/shortCount`。
- VECTOR 最内层必须 `vec_*` 折叠；EVENT 平台无 `ts_event_*`，先单条探针。
- 更新频率不写在 MCP 元数据里；IND 无离线体检包，本表频率/分布为 `[inferred]`，在线六法仅对主信号字段补测。

## 1 逐 category 画像

| category | dataset | 字段 | MATRIX | VECTOR | 覆盖 | ALIVE | UNTESTED | UNUSABLE/DEAD | 当季塔 | 可否出信号 | 形态特征 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| INSTITUTIONS | `institutions6` | 11 | 11 | 0 | 0.9915 | 11 | 0 | 0 | 1(未亮) | 可（主力） | 强右偏量纲，须 rank |
| SENTIMENT | `sentiment21` | 105 | 105 | 0 | 0.9681 | 4 | 90 | 2 | 1(未亮) | 验证性 | 评分类有界 / 右偏计数 |
| EARNINGS | `earnings11` | 35 | 0 | 35 | 0.4992 | 0 | 0 | 35 | 2(未亮) | 弱（WEAK_MECHANISM） | 稀疏事件 VECTOR |
| MODEL | `model77` | 23 | 23 | 0 | 0.4001 | 0 | 0 | 23 | 3(已亮) | 弱（WEAK_MECHANISM） | 评分类有界 / 右偏计数 |
| OTHER | `other323` | 11 | 0 | 11 | 0.9996 | 0 | 11 | 0 | 4(已亮) | 弱（WEAK_MECHANISM） | 稀疏事件 VECTOR |

**合计 185 个字段，5 个 dataset / 5 个 category，100% 覆盖不抽样**（MCP `complete=true` 逐集对账）。

## 2 关键字段级明细（ALIVE / 高覆盖）

| dataset | field | type | cov | verdict | bestS | best2Y | 机制方向 |
|---|---|---|---:|---|---:|---:|---|
| `institutions6` | `aggregate_equity_value_all_owners` | MATRIX | 0.992 | ALIVE | 2.76 | 2.41 | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| `institutions6` | `aggregate_equity_value_institutions` | MATRIX | 0.992 | ALIVE | 2.9 | 3.18 | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| `institutions6` | `aggregate_share_count_all_owners` | MATRIX | 0.992 | ALIVE | 2.53 | 2.79 | FE 步0：先做类型与覆盖探针，再定机制 |
| `institutions6` | `aggregate_share_count_institutions` | MATRIX | 0.992 | ALIVE | 3.45 | 2.94 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `count_institutional_buyers_security` | MATRIX | 0.992 | ALIVE | 3.23 | 2.5 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `count_institutional_holders_security` | MATRIX | 0.992 | ALIVE | 3.18 | 2.3 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `count_institutional_sellers_security` | MATRIX | 0.992 | ALIVE | 3.1 | 2.87 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `market_value_institutional_shares_acquired` | MATRIX | 0.992 | ALIVE | 2.92 | 2.66 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `market_value_institutional_shares_disposed` | MATRIX | 0.9915 | ALIVE | 2.81 | 2.98 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `quantity_institutional_shares_acquired` | MATRIX | 0.992 | ALIVE | 3.19 | 3.04 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `institutions6` | `quantity_institutional_shares_disposed` | MATRIX | 0.992 | ALIVE | 3.2 | 3.29 | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| `sentiment21` | `snt21_2pos_mean` | MATRIX | 0.9681 | ALIVE | 1.69 | 1.78 | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| `sentiment21` | `snt21_4pos_mean` | MATRIX | 0.9681 | ALIVE | 1.74 | 2.07 | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| `sentiment21` | `snt21_5pos_mean` | MATRIX | 0.9681 | ALIVE | 1.7 | 1.8 | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| `sentiment21` | `snt21_pos_mean` | MATRIX | 0.9681 | ALIVE | 3.01 | 1.93 | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |

## 3 判死字段通道与机制风险

- **`institutions6`**：未亮塔 1/3；ACTIVE/OS 未占用；11 字段全 ALIVE。族锁：机构净买入（IND-W149-INST6-NETBUY-WEAK-DEAD）。
- **`sentiment21`**：未亮塔 1/3；⚠ 白名单写入触发 `dead_intersection` high 告警：跨 4 区（EUR/GLB/KOR/USA）判死；IND 本地 news/sentiment 族亦多证枯竭 → 标 VALIDATE_FIRST，首探只做验证性 2 条探针，无信号即换 `analyst11`。
- **`earnings11`**：未亮塔 2/3；⚠ MCP 实读 35 字段**全为 VECTOR** RavenPack 新闻情绪/事件元数据，cov 0.4992 为历史累计覆盖而非任意时点覆盖（news29 判死同型）→ 标 WEAK_MECHANISM，配额上限 2 条。
- **`model77`**：已亮塔 3/3（lit_category_but_unoccupied）；⚠ MCP 实读 23 字段全是 ESG/治理评分、cov **0.4001**（DB 画像 0.8495 为旧版本，已作废）→ 与 IND 已判死的治理评分类（fundamental1 / other567 / other128）同型 → 标 WEAK_MECHANISM，配额上限 2 条。
- **`other323`**：已亮塔 4/3（lit_category_but_unoccupied）；⚠ MCP 实读 11 字段全是 VECTOR 股本/票面/手数/标识符静态数据 → 几无横截面收益信息 → 标 WEAK_MECHANISM，仅作分组轴/条件腿候选，配额上限 2 条。

## 4 归档索引

- 逐集 typed catalog（机器事实源）：`tracking/IND/reference/ind_<ds>_fields.json`
- 逐集 8 列画像（人读）：`reports/dataset_experience/ind_<ds>_field_profile_20261114.md`
- 索引：`tracking/IND/reference/ind_field_profile_index_20261114.json` + `reports/ind_field_profile_index_20261114.md`
- ⚠ **不得占用 `ind_<ds>_campain.md`**：那是 `dataset_experience.py` 生成器 + `step9_audit.py` 消费的既定文件名（AGENTS.md §8.13:1177），手写件同名会破坏生成器同名覆盖语义。
