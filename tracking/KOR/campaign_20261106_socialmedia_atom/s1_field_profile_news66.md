# S1 简档 · news66 Webpage View Statistics

> Wave3-2 注意力代理（2 VECTOR）。仅 news20 再灭后启用。

| 字段 | type | cov | aC | 语义 |
|---|---|---:|---:|---|
| mws66_api_views | VECTOR | 0.5 | 51 | 页面浏览量 |
| mws66_timestamp | VECTOR | 0.5 | 27 | 时间戳（元数据，勿作信号） |

探针草案：`subtract(0.5, group_rank(ts_mean(vec_avg(mws66_api_views), 22), sector))` 及 delta/std 变体。
