# GBR analyst48 数据集经验（2026-11-08）

> 7 字段（anl48_*），aC 26，cov 0.807。category = ANALYST。

## 判死：无信号价值的元数据集

字段全为索引元数据：`anl48_bbpdiip`（指数点股息）、`anl48_bulk_count_index_members`（成分股数）、`anl48_bulk_idivisor`（除数）、`anl48_bulk_indx_typ`（索引类型码）、`anl48_index_bulk_ibc`（Bloomberg 标识）、`anl48_index_bulk_nfields`（字段数）、`anl48_index_bulk_return_code`（状态码）。

⇒ 数据描述的是**指数构造**而非公司基本面/预期，横截面无经济机制可挖。**跳过，勿再拉字段。**
