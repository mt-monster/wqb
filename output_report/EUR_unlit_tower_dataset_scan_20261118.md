# EUR 未点亮塔数据集扫描与选定（2026-11-18）

> 全程固定 EUR / D1；塔位实读 `mcp__wq-brain-http__get_pyramid_alphas`（2026-11-18），
> 类别按 `get_datasets` 平台实查（不按名字推断，遵循 EUR SOP §7.1）。

## 1. 塔位实况（EUR/D1，本季）

| 塔 | 已提交 | 状态 |
|---|---:|---|
| analyst | 10 | 🔒 已点亮（排除） |
| news / model / fundamental / other / sentiment / imbalance / risk | 各 3 | 🔒 已点亮（排除） |
| **insiders** | **2** | 未点亮（差 1） |
| **pv** | **2** | 未点亮（差 1） |
| **earnings** | **1** | 未点亮（差 2） |
| **institutions** | **0** | 未点亮 |
| **macro** | **0** | 未点亮 |
| **socialmedia** | **0** | 未点亮 |

## 2. 逐 category 数据集扫描（平台实查，未点亮 6 类）

| 类别 | 数据集（平台实查） | 评估 | 决策 |
|---|---|---|---|
| **institutions** | fund_holdings_panel(30字段,cov0.881) / institutions6(11字段,cov0.992) | institutions6 全 MATRIX 免 vec、cov0.99、αC 4-30 低拥挤；fund_holdings 全 VECTOR 且 returns 2.33% F 数学判死 | ✅ **入选 institutions6**（主阵地）；fund_holdings 仅门控 |
| **insiders** | insider_agg_matrix(34,cov0.61) / insiders1(9,cov0.55) / insiders12(8,cov0.20) | insider_agg_matrix 家数/股数族最全、αC 低；另两个 cov 过低（0.55/0.20）判死 | ✅ **入选 insider_agg_matrix**；insiders1/12 排除 |
| **pv** | pv47(2) / pv103(9) / pv106(15) / pv37(251) / continuation_score(560) / pattern_scores(504) / pv20(1475) / pv87(1649) / pv29/pv30(聚类轴) / intraday_pv_feats(585) 等 20 个 | pv47 特异收益 cov1.0（2字段，罕见）；pv37 涨跌量已证 S3.2/prod0.58 但 sub 0.8<1.66；形态线 S≤1.37 上限；其余拥挤/判死 | ⏸ **备选 pv47 / pv37**（先做 institutions+insiders，无计可施再换） |
| **earnings** | earnings6(66,cov0.82,αC1633) / earnings_sent_matrix(7,cov0.51) | earnings6 4 个数字字段 cov 0.53、拥挤 αC1633；sent_matrix cov 0.51 覆盖判死 | ❌ 排除（SOP：earnings 塔字段极薄，实物不可达） |
| **socialmedia** | socialmedia12(6,cov0.78,αC1100) / socialmedia15(45,cov0.34) | 十臂实测 \|S\|≤0.21、SUB 全负；coverage 0.34 判死 | ❌ 排除 |
| **macro** | macro10(1字段,cov1.0) / macro27(33,cov0.33) | macro10 单标量无选股截面；macro27 cov0.33 + returns 2.27% | ❌ 排除 |

## 3. 选定结论与理由

1. **institutions6**（INSTITUTIONS 塔 0/3，完全未点亮）——全 MATRIX、cov 0.93–0.998、αC 4–30 低拥挤。
   已验证「analyst 修正强腿 + 机构家数不对称小腿」能点亮该塔（N1NGbddg prod 0.6872 ✅）。
2. **insider_agg_matrix**（INSIDERS 塔 2/3）——董事/高管净买入股数族 34 字段全量；
   已出 S2.0/F1.03/2Y1.79 全闸候选，但裸读数 prod 0.76–0.80 撞墙，需换罕见形态。

**排除已点亮塔**：analyst/news/model/fundamental/other/sentiment/imbalance/risk 全部数据集不投入。

## 4. 全字段探测（禁止抽样）

- institutions6：完整 11 字段画像已归档，完整性闸 11/11 PASS
- insider_agg_matrix：完整 34 字段画像已归档，完整性闸 34/34 PASS
- 归档路径：`tracking/EUR/reference/profiles/eur_<cat>_<ds>_profile_20261118.md`；
  命名规则见 `tracking/EUR/reference/profiles/README.md`。

## 5. 跨类组腿约束（用户硬约束）

- PV / MODEL / OTHER 两两禁组腿，彼此之间也禁；可与其它类组腿，含禁区类的跨类组合全账号 ≤5。
- 本战役 institutions6 + analyst 修正腿：INSTITUTIONS×ANALYST 均非禁区类，合规。
