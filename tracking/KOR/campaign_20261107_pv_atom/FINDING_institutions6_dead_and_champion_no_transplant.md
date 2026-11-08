# institutions6 数据集级判死 + 论坛冠军跨区移植证伪 · 2026-11-07

## 一、数据集级判死：institutions6（KOR/D1/TOP600）

两种**结构完全不同**的几何、共 4 条 alpha，S 全部锁在 0.56–0.63：

| alpha | 波次 | 几何 | 字段 | S | F | 2Y | TO | raFail |
|---|---|---|---|---:|---:|---:|---:|---:|
| vR1G7bod | P7 | 水平 group_rank | aggregate_share_count_institutions | 0.63 | 0.42 | 1.34 | 0.0778 | 3 |
| vR1G7boA | P7 | 均值回复 ts_av_diff(66) | aggregate_share_count_institutions | **−1.17** | −0.75 | −0.50 | 0.0831 | 5 |
| gJeGlM0m | P8 | **论坛冠军骨架** G/T=90/33 | buyers/holders | 0.60 | 0.31 | 0.86 | 0.0563 | 3 |
| kqNGw0Y8 | P8 | **论坛冠军骨架** G/T=66/33 | buyers/holders | 0.56 | 0.29 | 1.24 | 0.0603 | 3 |

**判死依据**（沿用「S 天花板在数据集层而非表达式层」判据）：
- 水平几何、均值回复几何、复合冠军骨架三种机制互不相关，S 读数却聚在同一窄带（0.56–0.63）⇒ 不是骨架问题。
- `ts_av_diff` 给出 −1.17 说明**机构持仓偏离度高 → 后续跑输**（拥挤反转）在 KOR 成立，但翻正后 2Y 仅 +0.50，RA 双线（S≥1.58 ∧ 2Y≥1.58）仍不可达。
- TO 极低（0.056–0.083）说明信号几乎不变化 ⇒ 13F 季度披露在 KOR TOP600 上信息量稀薄。

## 二、★ 论坛冠军模板跨区移植证伪（重要方法论）

原帖冠军（IND/TOP500）：`trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)),840,driver="gaussian"),1.6), -1)`
**IND 实测 S 1.62 / F 1.37 / 2Y 2.47，18 项硬检查全 PASS，已提交 OS。**
KOR 逐字移植（仅换 region/universe + 设置档为 SUBINDUSTRY/decay9/trunc0.03，与帖一致）：
**S 0.60 / F 0.31 / 2Y 0.86**。G/T 换 66/33 → 0.56 / 1.24。

⇒ **同样字段、同样骨架、同样设置档，跨区域后 S 掉 63%。**
原帖作者自己在结尾也把这条列为未解疑问：「门控窗口 G/T 在其他 Region 是否可平移？系数必重扫，机制可推断。」
KOR 实测答案：**机制可推断，强度不可平移**。institutions6 在 KOR 的机构披露节奏/覆盖结构与 IND 不同，同样的「参与广度新鲜度」不含同等信息。

### 落地纪律（写入方法论）
**论坛冠军模板只能当「骨架候选」，不能当「收益预期」。** 移植到新区域时必须：
1. 先按原帖参数逐字跑 1 批（2 条：原 G/T + 帖内第二甜点），**只为测区域适配度**；
2. 若 S < 原帖的一半（本例 0.60 < 1.62×0.5=0.81），**直接判该数据集在该区无适配**，不要扫 G×T 网格（0.6 的基线扫不出 1.58）；
3. 只有 S ≥ 0.8×原帖时才值得展开网格重扫。

## 三、本轮被证伪的假设清单
1. 「高覆盖率数据集有信号」→ news_sentiment_transfer cov 0.9654 只给 S 0.04。
2. 「论坛 OS 冠军可直接移植」→ IND 1.62 → KOR 0.60。
3. 「低 alphaCount 字段是未开发矿」→ 已在 dl_riskfree 反证（S<0.7）。

## 四、后续
institutions6 / fund_holdings_panel（同类股权结构数据，P7 同族 `aggregate_share_count` 水平件仅 0.63）
统一**延后**，不再投批次。转向 risk 塔未测数据集：**risk59（证券借贷/做空，16 VECTOR 字段 cov 0.9806）**、
**risk68（beta / dadv / 波动权重，3 MATRIX 字段 cov 1.0）** —— 这两族在学术上（BAB、short-interest anomaly）先验强，
且字段形态与已失败的新闻/股权结构完全不同。
