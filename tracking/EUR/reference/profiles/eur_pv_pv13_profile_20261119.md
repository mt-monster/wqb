# EUR pv13 字段画像（2026-11-19，全字段探测 73/73）

> 数据集：`pv13`（PV 塔，EUR/D1 塔位 0/2 未点亮）。平台目录：`tracking/EUR/reference/eur_pv13_fields.json`（`get_datafields` EUR/TOP2500/D1 全量拉取，`complete=true`，73 字段）。
> ⚠ 本地 `datasets` 表记的 `fields=3` 是旧快照，平台实读 73。

## 结构判定

- 73 字段分三类：**GROUP 分组轴 40 个**（RBICS/Revere 行业层级，非信号，只作 group 参数）、**映射/元数据 MATRIX/VECTOR 20 个**（city/country/zipcode/cap/index_value/relationship 类别/产品名，非信号）、**真信号候选 9 个**（rel_ret_all/comp/cust/part 关联方日均收益、rel_num_all/comp/cust/part 关联方数量、pv13_com_page_rank / com_rk_au / ompetitorgraphrank_hub_rank / ustomergraphrank_* 关联图分数）。
- 经济机制：**经济关联溢出（economic links / lead-lag）**——Cohen & Frazzini (2008) *Economic Links and Predictable Returns*；客户-供应商/竞对/伙伴的收益通过经济关联延迟传导。
- 拥挤度低（rel_ret 族 aC 9–73）。

## 字段全表（73 字段逐字段平台读数）

| 字段 | 类型 | coverage | userCount | alphaCount | 语义 | 可用性 |
|---|---|---:|---:|---:|---|---|
| `business_partnership_category` | VECTOR | 0.6988 | 4 | 4 | 合作类型（JV/licensing） | 元数据 |
| `company_competitor_entity_2` | VECTOR | 0.3532 | 8 | 9 | 竞对实体 | 元数据 |
| `company_customer_entity` | VECTOR | 0.4454 | 5 | 10 | 客户实体 | 元数据 |
| `company_partner_entity` | VECTOR | 0.6988 | 29 | 31 | 伙伴实体 | 元数据 |
| `company_product_tradename` | VECTOR | 0.9825 | 5 | 7 | 产品名 | 元数据 |
| `company_relationship_type` | VECTOR | 0.8277 | 2 | 2 | 关系类型 | 元数据 |
| `customer_revenue_share_percent` | VECTOR | 0.4454 | 4 | 5 | 客户收入占比 | 弱信号候选 |
| `pv13_1l_scibr` | GROUP | 0.9257 | 58 | 93 | RBICS L1 分组 | 分组轴 |
| `pv13_22_800_sector` | GROUP | 0.3394 | 15 | 16 | top800 分组 | 分组轴 |
| `pv13_2_sector` | GROUP | 1.0 | 14 | 16 | 分组 | 分组轴 |
| `pv13_2l_scibr` | GROUP | 0.9257 | 309 | 762 | RBICS L2 | 分组轴 |
| `pv13_3l_scibr` | GROUP | 0.9257 | 60 | 114 | RBICS L3 | 分组轴 |
| `pv13_4l_scibr` | GROUP | 0.9257 | 59 | 131 | RBICS L4 | 分组轴 |
| `pv13_52_600_sector` | GROUP | 0.5447 | 1 | 1 | 600 sector | 分组轴 |
| `pv13_52_sector` | GROUP | 1.0 | 2 | 3 | 分组 | 分组轴 |
| `pv13_5_sector` | GROUP | 0.5255 | 36 | 47 | 分组 | 分组轴 |
| `pv13_5l_scibr` | GROUP | 0.9257 | 46 | 101 | RBICS L5 | 分组轴 |
| `pv13_6l_scibr` | GROUP | 0.9257 | 59 | 155 | RBICS L6 | 分组轴 |
| `pv13_com_page_rank` | MATRIX | 0.6898 | 61 | 83 | 竞对 PageRank | 弱信号候选（静态分·伪预测型） |
| `pv13_com_rk_au` | MATRIX | 0.6898 | 40 | 53 | 竞对 HITS authority | 弱信号候选（静态分） |
| `pv13_di_1l` | GROUP | 0.2577 | 1 | 2 | RBICS 数字 id | 分组轴 |
| `pv13_di_2l` | GROUP | 0.2577 | 1 | 1 | RBICS 数字 id | 分组轴 |
| `pv13_di_3l` | GROUP | 0.2577 | 1 | 1 | RBICS 数字 id | 分组轴 |
| `pv13_di_4l` | GROUP | 0.2577 | 2 | 2 | RBICS 数字 id | 分组轴 |
| `pv13_di_5l` | GROUP | 0.2577 | 2 | 3 | RBICS 数字 id | 分组轴 |
| `pv13_di_6l` | GROUP | 0.2577 | 6 | 28 | RBICS 数字 id | 分组轴 |
| `pv13_eur_revere_risc_sector_level` | GROUP | 0.382 | 7 | 7 | 行业层级 | 分组轴 |
| `pv13_eur_revere_risc_sector_parent` | GROUP | 0.382 | 3 | 3 | 父行业 | 分组轴 |
| `pv13_h_min2_sector` | GROUP | 0.5255 | 52 | 65 | 分组 | 分组轴 |
| `pv13_h_min52_sector` | GROUP | 0.5255 | 35 | 44 | 分组 | 分组轴 |
| `pv13_hierarchy_min52_600_sector` | GROUP | 0.2503 | 7 | 9 | 分组 | 分组轴 |
| `pv13_level` | GROUP | 0.382 | 6 | 6 | 层级 | 分组轴 |
| `pv13_new_1l_scibr` | GROUP | 0.794 | 3 | 3 | RBICS | 分组轴 |
| `pv13_new_2l_scibr` | GROUP | 0.794 | 3 | 3 | RBICS | 分组轴 |
| `pv13_new_3l_scibr` | GROUP | 0.794 | 8 | 9 | RBICS | 分组轴 |
| `pv13_new_4l_scibr` | GROUP | 0.794 | 4 | 4 | RBICS | 分组轴 |
| `pv13_new_5l_scibr` | GROUP | 0.794 | 8 | 16 | RBICS | 分组轴 |
| `pv13_new_6l_scibr` | GROUP | 0.794 | 12 | 14 | RBICS | 分组轴 |
| `pv13_ompetitorgraphrank_hub_rank` | MATRIX | 0.6898 | 18 | 20 | 竞对 HITS hub | 弱信号候选（静态分） |
| `pv13_parent` | GROUP | 0.382 | 4 | 4 | 父级 | 分组轴 |
| `pv13_rcsed_6l` | GROUP | 0.2577 | 4 | 19 | L6 描述 | 分组轴 |
| `pv13_revere_city` | MATRIX | 0.9248 | 21 | 21 | 城市码 | 元数据 |
| `pv13_revere_country` | MATRIX | 0.9613 | 27 | 35 | 国家码 | 元数据（可用作轴） |
| `pv13_revere_index_cap` | MATRIX | 0.8639 | 18 | 19 | 市值 | 元数据 |
| `pv13_revere_index_value` | MATRIX | 0.8643 | 26 | 32 | 指数值 | 元数据 |
| `pv13_revere_key_sector_total` | MATRIX | 0.9393 | 12 | 16 | 关键行业数 | 弱信号候选 |
| `pv13_revere_level` | MATRIX | 0.266 | 10 | 11 | 层级 | 元数据 |
| `pv13_revere_parent` | MATRIX | 0.266 | 13 | 23 | 父行业码 | 元数据 |
| `pv13_revere_term` | MATRIX | 0.4557 | 12 | 13 | 终端行业标记 | 元数据 |
| `pv13_revere_term_sector_total` | MATRIX | 0.9393 | 16 | 34 | 终端行业数 | 弱信号候选 |
| `pv13_revere_zipcode` | MATRIX | 0.9195 | 16 | 20 | 邮编 | 元数据 |
| `pv13_reverebasedatamap_2` | MATRIX | 0.9936 | 26 | 43 | 映射 | 元数据 |
| `pv13_reveremap` | MATRIX | 1.0 | 5 | 8 | 映射 | 元数据 |
| `pv13_term` | MATRIX | 0.3537 | 8 | 9 | 终端标记 | 元数据 |
| `pv13_ustomergraphrank_auth_rank` | MATRIX | 0.781 | 13 | 18 | 客户 HITS authority | 弱信号候选（静态分） |
| `pv13_ustomergraphrank_hub_rank` | MATRIX | 0.781 | 25 | 62 | 客户 HITS hub | 弱信号候选（静态分） |
| `pv13_ustomergraphrank_page_rank` | MATRIX | 0.781 | 24 | 36 | 客户 PageRank | 弱信号候选（静态分） |
| `pv13_v3_1l_scibr` | GROUP | 0.8918 | 221 | 489 | RBICS v3 | 分组轴 |
| `pv13_v3_2l_scibr` | GROUP | 0.8918 | 217 | 431 | RBICS v3 | 分组轴 |
| `pv13_v3_3l_scibr` | GROUP | 0.8918 | 302 | 731 | RBICS v3 | 分组轴 |
| `pv13_v3_4l_scibr` | GROUP | 0.8918 | 331 | 953 | RBICS v3 | 分组轴 |
| `pv13_v3_5l_scibr` | GROUP | 0.8918 | 25 | 39 | RBICS v3 | 分组轴 |
| `pv13_v3_6l_scibr` | GROUP | 0.8918 | 388 | 1028 | RBICS v3 | 分组轴 |
| `rel_num_all` | MATRIX | 0.6857 | 25 | 29 | 关联公司总数 | 信号候选 |
| `rel_num_comp` | MATRIX | 0.5418 | 21 | 23 | 竞对数 | 信号候选 |
| `rel_num_cust` | MATRIX | 0.277 | 13 | 18 | 客户数 | 信号候选（cov 低） |
| `rel_num_part` | MATRIX | 0.5571 | 18 | 42 | 伙伴数 | 信号候选 |
| `rel_ret_all` | MATRIX | 0.6189 | 29 | 73 | 关联方日均收益 | **主信号候选** |
| `rel_ret_comp` | MATRIX | 0.4463 | 10 | 11 | 竞对日均收益 | 信号候选 |
| `rel_ret_cust` | MATRIX | 0.2502 | 7 | 10 | 客户日均收益 | 信号候选（cov 低） |
| `rel_ret_part` | MATRIX | 0.4452 | 6 | 9 | 伙伴日均收益 | 信号候选 |
| `sector_attachment_overlap_count` | VECTOR | 0.8277 | 2 | 2 | 行业重叠数 | 弱信号候选 |
| `terminal_sector_focus_overlap_count` | VECTOR | 0.8277 | 11 | 13 | 终端行业重叠数 | 弱信号候选 |

## EUR 实测读数（本会话探针波，6 臂全 COMPLETE）

设置：EUR/TOP2500/D1、SUBINDUSTRY、decay 4、trunc 0.08、nan ON、maxTrade OFF。

| 臂 | 表达式 | alpha | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| rel_ret_all 5日·动量 | `ts_rank(ts_sum(rel_ret_all,5),252)` | rK7OEqpE | **−0.24** | −0.03 | 0.04 | −0.20 | 39.9% |
| rel_ret_all 5日·反转 | `-ts_rank(ts_sum(rel_ret_all,5),252)` | XgabP3ma | **0.24** | 0.03 | −0.04 | 0.20 | 39.9% |
| rel_ret_all 22日·动量 | `ts_rank(ts_sum(rel_ret_all,22),252)` | omaLAb7m | −0.11 | −0.01 | 0.78 | 0.10 | 18.0% |
| rel_ret_all 22日·反转 | `-ts_rank(ts_sum(rel_ret_all,22),252)` | RRebqOMd | 0.11 | 0.01 | −0.78 | −0.10 | 18.0% |
| rel_ret_comp 5日 | `ts_rank(ts_sum(rel_ret_comp,5),252)` | gJabwl6e | −0.28 | −0.04 | 0.22 | −0.25 | 38.9% |
| rel_ret_part 22日 | `ts_rank(ts_sum(rel_ret_part,22),252)` | XgabP3G0 | 0.06 | 0.01 | 1.16 | 0.23 | 17.1% |

**判定**：rel_ret 关联溢出族**6 臂全灭**（|S| ≤ 0.28；方向对称性也无法确认——正反差异 <0.6 且无一致符号）。原因：关联收益字段稀疏（cov 0.44–0.69）且事件驱动，横截面有效名数不足；COSINE 类机制在 EUR 日频价格上已被套利。
**处置**：**PROVISIONAL / 族级**（rel_ret 族探针死）。其余 70 字段为 GROUP 分组轴（40）/映射元数据（20）/静态图分（4，按 SOP「伪预测型 score/rank」不投入）。数据集级不判死（图分族与 rel_num 族未独立成波）。

## §5 图分族 + rel_num 族专波（2026-11-20，12 臂全灭 ⇒ 数据集级判死）

旧画像留下「图分族（4 字段）与 rel_num 族未独立成波」缺口，本波补齐（TOP2500×INDUSTRY×decay4）：

| 族 | 字段 | 最优 | 判定 |
|---|---|---:|---|
| 竞对图分 | `pv13_com_page_rank` / `com_rk_au` / `ompetitorgraphrank_hub_rank` | S −0.05 / 0.10 / 0.12 | 静态 score，TO 2.9–6.1%，无横截面信息 |
| 客户图分 | `pv13_ustomergraphrank_{hub,page,auth}_rank` | S −0.08 / 0.19 / 0.16 | 同上（TO<3%） |
| 关系计数 | `rel_num_all` / `comp` / `cust` / `part` | S −0.34 / −0.24 / −0.11 / −0.04 | 计数无动量信息 |
| 关系动量 | `ts_delta(rel_num_all,22)` | S −0.25 | 变化也不行 |
| 图分/计数比 | `com_page_rank ÷ (rel_num_comp+1)` | S −0.07 | 归一化后仍无 |

**判定：12 臂 |S| ≤ 0.34、TO 2.4%–6.1%（几乎不动仓）⇒ 图分是静态量、关系计数是水平量，两者都没有价格弹性。**
加上旧波 rel_ret 族 6 臂（|S| ≤ 0.28）⇒ **三个信号族（rel_ret 溢出 / 图分 / 关系计数）全部实证为死**，
pv13 **数据集级判死**（不再是族级 PROVISIONAL）。数据集不判死的是 2024-03 新加的 Revere 行业层级族（40 个 GROUP 字段 = 分组轴，非信号），
但它只是 RBICS 行业分类，与分组轴重复 ⇒ 无独立 alpha 价值。
