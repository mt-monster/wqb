# GBR D1 other47 挖掘经验（SEMrush 网站流量 / Google Ads · 判死）

范围：2026-10-30。GBR/TOP700/D1 的 `other47`。**8 个结构互异模板全部未达闸**。
本文件同时记录该集两个**平台元数据陷阱**，这两个坑比判死结论本身更值得复用。

数据集画像（DB `datasets` 表实读，id=141）：category **`OTHER`**、`field_count 18`
（全 VECTOR）、`coverage 0.5171`、`alpha_count 14`、`value_score 6`、
`pyramid_multiplier 1.7`、`tier EXCLUDED`、`delay 1`。

## ★ 陷阱一：数据集级 description 有系统性污染

平台 `get_datasets` 给 `other47` 的描述是
「Web Intelligence Data … comprehensive mapping between **BBID and RIC**」——
与实际字段**毫无关系**。至少 11 个 `other*` 集（`other47` / `other250` / `other296` /
`other315` / `other323` / `other424` / `other425` / `other455` / `other567` / `other734` /
`other78`）被同一套 "mapping between BBID and RIC" 文案覆盖。

**真实内容**（`get_datafields` 实读）是 **SEMrush 网站流量与 Google Ads 数据**：

| 字段 | 含义 |
|---|---|
| `oth47_organic_traffic` | 自然搜索月访问量 |
| `oth47_organic_keywords` | 排名关键词数 |
| `oth47_organic_cost` | 自然搜索流量等价广告成本 |
| `oth47_rank` | SEMrush 可见度排名 |
| `paid_search_budget_estimate` | Google Ads 月支出估计 |
| `paid_search_terms_count` | 付费关键词数 |
| `paid_search_visitors` | 付费搜索访问量 |
| `product_listing_ad_terms` | 商品列表广告词数 |
| `unique_product_listing_ads` | 去重商品列表广告数 |

⇒ **判「数据集内容」一律先 `get_datafields` 看字段 `id` + 字段级 `description`**，
数据集级 description 只在字段清单为空时当最后参考。

## ★ 陷阱二：同一数据集内字段前缀不统一

18 个字段里只有 **4 个**带 `oth47_` 前缀（`oth47_organic_traffic` /
`oth47_organic_keywords` / `oth47_organic_cost` / `oth47_rank`），其余是**裸名**
（`paid_search_budget_estimate` / `paid_search_terms_count` / `paid_search_visitors` /
`product_listing_ad_terms` / `unique_product_listing_ads`）。

**踩坑实录**：把裸名 `paid_search_budget_estimate` 按「惯例」写成
`oth47_paid_search_budget_estimate`，`preflight_expressions` 报 `unknown_soft`
（"dataset-prefixed field not found"）。当时误判为 preflight 假阴性，实为**自己写错**。
`get_datafields(dataset_id="other47", search="paid_search_budget_estimate")` 能返回裸名,
证明平台判得对。

⇒ **表达式里的字段 ID 原样复制 `get_datafields` 的返回值，不许自己加/去前缀**；
`unknown_soft` 报「加前缀后找不到」时优先怀疑自己，且**只有 `get_datafields` 精确 search
能返回该 id 时才推翻 preflight**。

## 判死结论（registry：`GBR-OTHER47-WEBATTENTION-DEAD`，2026-10-30）

8 个结构互异模板全部未达硬闸（完整模板清单与逐条指标见
[模板库文档](../../docs/reference/template_library_other47_webattention_gbr_20261030.md)）。

机制侧为什么本来就难成立：

- 这些字段是**公司自身的网络关注度**（自建站流量 / 广告投放），是「公司经营投入」而非
  「投资者注意力」——与 sentiment 塔需要的「外部注意力突增」不是一回事。
  论坛 `43179860065303`（72 赞，sentiment 塔权威模板）用的是 **Wikipedia 关注度**，
  即外部、免费、非公司可控的注意力，那才与交易行为有因果链。
- 广告支出是**季度性预算决策**，更新频率低、且与营收规模强共线 ⇒ 容易退化成规模因子。
- `coverage 0.5171` 意味着近一半股票池无数据，跨截面排序天然有缺口。

## 后续边界

- **不再在 `other47` 上新增模板**。8 个结构互异模板全灭 + `tier EXCLUDED` 同向，判死稳。
- 若要复用「网络关注度」机制，正确方向是**外部注意力源**（Wikipedia / 搜索指数 /
  社媒提及），不是公司自建站的 SEMrush 流量。但 sentiment 塔在 GBR 的候选数据集
  已判死（见 `GBR` 的 dead_end 全表），本区目前无可用外部注意力源。
- 本集回测**未入 `backtest_results` 表**（`region='GBR' AND dataset='other47'` 实读 0 行）。
- 字段含义可参考论坛 `35090833341207`（101 赞，Other 字段关系分类法：
  净额有量纲、比值无量纲 ⇒ 优先做比值）。

## 证据落点

- 判死条目：`registry_empirical` → `GBR-OTHER47-WEBATTENTION-DEAD`
- 8 模板全表：[`template_library_other47_webattention_gbr_20261030.md`](../../docs/reference/template_library_other47_webattention_gbr_20261030.md)
- 字段清单：`mcp__wq-brain-http__get_datafields(dataset_id="other47", region="GBR",
  universe="TOP700", delay=1, data_type="VECTOR")`
- 元数据陷阱纪律：`Claude/skills/wq-wave-preflight-dispatch/SKILL.md`（字段 ID 原样复制）
