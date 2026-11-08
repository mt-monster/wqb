# Wave N1 收割：other545 NEMO 网络动量（2026-11-07）

字段：score（NEMO 2.0 综合分，7 网络动量合成）、mpd（价格动量分）、pln_omen（NLP 链接动量）、mktcap。全 VECTOR，cov 0.8393。
插曲：派发中途平台 session 过期（401 Incorrect authentication credentials），
N1 后 2 批与 N2 全部 5 批 401；调 MCP `authenticate` 工具强制重登（201, has_jwt）后重派成功。

| 模板 | alpha | S | F | 2Y | TO | raFail |
|---|---|---:|---:|---:|---:|---:|
| 综合分水平 W22 | akKzP6m1 | 0.76 | 0.45 | 0.72 | 0.0745 | 3 |
| 综合分水平 W66 | vR1Gz87A | 0.69 | 0.39 | 0.70 | 0.0681 | 3 |
| 综合分 delta22 | 2rA6ZJP8 | 0.77 | 0.38 | 0.35 | 0.1839 | 4 |
| 价格动量分 mpd | akKzPoX6 | 0.30 | 0.12 | 0.72 | 0.0791 | 3 |
| 综合分散度 vec_stddev | P0ozXeLW | 1.14 | 0.88 | **0.00** | 0.1167 | 3 |
| ts_rank 新鲜度 | N1Nz5MEq | 0.90 | 0.57 | 0.45 | 0.0813 | 3 |
| NLP 链接动量 delta22 | d5WzlRwK | 0.98 | 0.74 | **1.41** | 0.1459 | 4 |
| 综合分水平 W10 | 1YNKnz5K | 0.75 | 0.44 | 0.69 | 0.0832 | 3 |

**判定：NEMO 族封盘**。天花板 1.14（散度臂）但 2Y 归零；水平臂 0.75-0.77 且 2Y 系统性弱（0.35-0.72）。
唯一 2Y 象样的臂是 pln_omen delta（1.41）但 S 只有 0.98 且 CONCENTRATED_WEIGHT。
其它 NEMO 组件（mpd 价格动量分）无独立信号 ⇒ 该数据集的「机器学习网络动量」在 KOR 不成立。

401 处置经验：mcp_7slot_batch 遇 401 不自愈（连坐整批），需手动调 `authenticate` 后重派失败批次；
已落盘批次不受影响。