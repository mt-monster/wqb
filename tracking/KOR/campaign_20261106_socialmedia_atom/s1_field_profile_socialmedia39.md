# S1 字段画像 · socialmedia39（KOR / TOP600 / D1）

> MCP get_datafields complete=true，platform_count=1。塔 socialmedia 0/3，乘数 1.0。

| 字段 | type | cov | aC | uC | 说明 |
|---|---|---:|---:|---:|---|
| scl39_top5_people_also_watch_ticker_ii | VECTOR | 1.0 | 580 | 183 | 共搜邻居 Atlas instrument ID 列表，非连续情绪分 |

## 可用性裁定
- 形态=ID 向量 ⇒ 标准 rank(ts_mean(vec_avg)) 可能无经济含义或 PnL 异常（USA 论坛有异常字段记录）。
- 本战役定位：**对照探针**，不作为 10 颗交付主轴，除非实测出可解释信号。
- 可试：vec_count（邻居个数代理注意力广度）；vec_avg 对 ID 的数值平均通常无意义，仅作负对照。
