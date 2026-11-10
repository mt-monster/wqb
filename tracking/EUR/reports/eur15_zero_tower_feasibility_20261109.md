# EUR 0 塔位 category 可达性终审（2026-11-09）

> 结论：**EUR 的 4 个 0 塔位 category（macro / socialmedia / earnings / institutions）全部物理不可达**。
> 这不是挖掘能力问题，是数据集供给问题——每个 category 的可用数据集要么不存在、要么覆盖不达标、要么已判死。

## 一、逐 category 判定

### macro（塔 0/3）— 仅 2 个数据集，全部不可用
| 数据集 | 字段 | cov | aC | 判定 |
|---|---|---:|---:|---|
| `macro10` | **1**（`mcr10_value`） | 1.0 | 122 | ✅覆盖 ✅冷 ❌**形态**：宏观级标量（全市场同值），无法构成个股截面排序；单字段无对照 |
| `macro27` | 33（全 VECTOR 招聘数据） | 0.147–0.43 | 0–11 | ❌**全部低于 0.5 覆盖门槛** |

⇒ **macro 不可达**。宏观数据集在 EUR 只有这两个，都不具备「个股 panel × 覆盖达标」的基本条件。

### socialmedia（塔 0/3）— 2 个数据集，全部判死
| 数据集 | 字段 | cov | 判定 |
|---|---|---:|---|
| `socialmedia12` | 6（仅 `scl12_buzz`/`scl12_sentiment` 为信号） | 0.85 | ❌**已判死**（`EUR-SOCIALMEDIA12-SENT-BUZZ-DEAD`）：EUR 不再追加波次；跨区佐证 GBR W19 S0.15/0.10、GLB 4/4 平（S −0.27~+0.03） |
| `socialmedia15` | 45 | 0.342 | ❌**覆盖不达标**（历史记 45/45 unusable） |

⇒ **socialmedia 不可达**，且该塔在 EUR 的官方口径即「SOCIALMEDIA category 在 EUR 仅此一个可用数据集，判为不可达」。

### earnings（塔 0/3）— 2 个数据集，一个太窄一个已判死
| 数据集 | 字段 | cov | 判定 |
|---|---|---:|---|
| `earnings6` | 66，但**信号面仅 2 个 VECTOR**（`eps_change_absolute_value`/`_percentage_value`） | 0.5258 | ❌**太窄**：其余 64 个是财报日期/公司名/URL/来源/货币/财年等元数据，不构成信号 |
| `earnings_sent_matrix` | 7 MATRIX（正/负/中性概率 + 2 个 tone + 1 label） | 0.5062 | ❌**已判死**：预核 cov 0.5115 + aC1676 + **S ≤ 0.21**（`EUR-EARNINGS-*` 语调几何判死） |

⇒ **earnings 不可达**。唯一机制面清晰的 `earnings_sent_matrix` 是本役早期预核就否掉的（S 0.21 远低于 1.58）。

### institutions（塔 0/3）— 本役已全探
| 数据集 | 最强 | 死因 |
|---|---|---|
| `fund_holdings_panel` | 全 IS 闸 S1.61/F1.02/2Y2.58 | **prod 0.8881 族墙** |
| `institutions6` | S1.03 | 2Y 结构性塌 |

⇒ **institutions 不可达**（本役已全字段实测）。

## 二、派生结论

1. **EUR 的 0 塔位 category 已全部出局**（4/4）。后续任何「点塔」策略在 EUR 只能落在**已点亮塔的加席**上（analyst/model/fundamental/imbalance），或 **1–2 席未点亮塔的补位**（news1 / insiders2 / other2 / pv2 / risk2 / sentiment2）。
2. **未探数据集 111 个，但分布极偏**：model 41 / other 16 / pv 14 / news 13 / analyst 13 / fundamental 7 / risk 2 / earnings 2 / insiders 1 / sentiment 1。而 model/fundamental 都在**禁混集合**内，pv/other 也在禁混集合内——**单数据集 ATOM 仍合法**。
3. ★ **最有价值的剩余空间不在 0 塔位 category，而在 1–2 席未点亮塔的「加 1 颗即点塔」数据集**：
   - `other` 2/3（techindi_model 已挖到 S4.29 但 prod 0.8175 墙）
   - `risk` 2/3（risk60 族 prod 0.9156 深墙）
   - `pv` 2/3、`sentiment` 2/3、`insiders` 2/3（insiders 有库存件 `leA5JeP7` F 差 0.06）
   - `news` 1/3（news18 已有 3 席全闸件在库，但属存量）
4. **15 颗目标的结构性障碍已可定量表述**：EUR 未点亮塔里「S 达标」的机制族只有 2 类（risk60 借券、techindi 概率预测），且品类子集产出的 prod 全部 ≥0.8175。**每新增 1 颗可提交件的边际成本 ≈ 探 15 个数据集**。
