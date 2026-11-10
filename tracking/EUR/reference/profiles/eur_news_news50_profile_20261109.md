# EUR × news50 字段画像（2026-11-09）

> 37/37 全量（complete=true）；Web News Analytics Data（RavenPack 网络新闻，与 news46 同厂同构）
> 塔位：NEWS(×1.4)；拥挤度：aC 148 / uC 92；os_is 0.4286

## 一、字段族

| 族 | 字段 | 类型/cov | 结论 |
|---|---|---|---|
| A 注意力 | mws50_rp_story_event_count（实体记录数，uC 25/aC 34）、mws50_vea（91d 事件量聚合） | VECTOR/0.786 | 需 vec_sum 聚合；关注度读数唯一可用 |
| B 新颖度 | mws50_ens / g_ens / ens_similarity_gap | VECTOR/0.786 | 新颖度 cov 0.786 贴线；similarity_gap（距上条同题天数）是独特读数——**未在 news46 试过** |
| C 极性 | mws50_ess/ssc/acb/aes/qcm/qep/qmb/bee/ber | VECTOR/0.786 | **极性族判死**，禁做 |
| D 影响力 | mws50_nip | VECTOR/0.786 | news46 NIP 已判死（S −0.14） |
| E 元数据 | category/country_code/time/property/position_name… | VECTOR | 禁用 |

## 二、结论
1. 与 news46 同厂同构（mws50 vs mws46 前缀），所有读数先验可平移：关注度天花板 1.32、NIP 死、极性死
2. 唯一独有读数 = ens_similarity_gap（同题事件间隔天数——"旧闻重炒 vs 新鲜事件"），cov 0.786 贴线 + 先验未知
3. **判定：留档不投槽**（同族天花板已实证）；若未来投，唯一探针 = vec_sum(similarity_gap) 反向（旧闻重炒→反转）
