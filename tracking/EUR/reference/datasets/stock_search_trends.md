# stock_search_trends · EUR / TOPCS1600 / D1 字段画像（快判）

> 类型 MATRIX · 6 字段 · cov 0.52–0.55 · category = **other**（×1.5）· αC 2
> ⚠ 字段 description 全部标注 **"in the USA"**——Google Trends 美国搜索量,对 EUR 宇宙的欧洲公司,数据语义与被定价市场错位

| 字段 | 窗口 |
|---|---|
| `search_interest_today_corporate_name` | 当日 |
| `search_interest_7d/14d/28d/84d/1y_corporate_name` | 滚动均 |

**机制**：Da et al. 搜索量注意力反转（SVI 飙升→反转）——但「美国人搜欧洲公司的量」既不代表欧洲散户注意力（语义错位）,也与 news18 的 `multiple_comp_sse` 事件密度（已出 S=1.73）高度同源。

**裁决**：cov 0.55 偏低 + 语义错位 + 与已出席位机制重叠,按「预期低边际收益」跳过,不投入探针（若 news18 席位后续失败再回补）。
