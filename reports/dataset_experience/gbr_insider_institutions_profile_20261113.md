# GBR insider_agg_matrix + institutions25 六法字段画像报告（2026-11-13）

> 探针设置：GBR/TOP700/D1/decay0/NONE/nanOFF/P0Y0M0D。画像批 id：insider=3oi1pJbXW4XDbHiovjfsU74（修参版）/ institutions25=3j59ms2Fe4tYczW14aA12Dxw（含 §2.7 量纲安全设计）。
> 本报告为机制设计前的画像交付物，待用户审后进机制波。

## 一、insider_agg_matrix（insiders 塔 0，34 字段 MATRIX，元数据 cov 0.59/1.0）

| 探针 | 字段/方法 | longCount/700 | 读数 | 交 FE 去向 |
|---|---|---:|---|---|
| bla3zxmN | directional_indicator 法1 | 24（3.4%） | 元数据 cov=1.0 失真：单日仅 3.4% 有事件 | 日频形态不可用（并列块+CW 风险） |
| QP0dzWxg | directional_indicator 法2 | 24 | 无零膨胀：数据=事件本身 | 事件流语义确认 |
| 58JV5GXn | directional ts_std5 法3 | 18 | 5 天变动极少 | 日更事件稀疏 |
| kqa5G8Ak | directional ts_std66 法3 | 327（47%） | 66 天累计近半宇宙有活动 | 必须窗口聚合 66-126+ 天（ts_sum 不用 ts_mean） |
| mLak7Kv5 | avg_buy_shares 法1 | 9 | 单日买入事件极少 | 同上聚合 |
| rK7mG0Z3 | avg_sell_shares 法1 | 12 | 单日卖出事件极少 | 同上聚合 |
| e7aJG1Xd | rank(avg_buy) ts_std22 | 119（17%） | 22 天累计 17% | 中窗聚合可用 |
| TO 观察 | 裸探针 TO 1.60-1.75 | — | 事件数据天然高换手 | 聚合+平滑后才能进闸 |

画像结论：典型低频事件流。机制假设（待审）：董事净买入方向信号——ts_sum(directional 或 buy/sell 比, 66-126) 聚合 + group_rank；二级：directional_significant_value_N 排序。

## 二、institutions25（institutions 塔 0，24 字段 VECTOR，元数据 cov 全 0 盲区）

| 探针 | 字段/方法 | longCount/700 | 读数 | 交 FE 去向 |
|---|---|---:|---|---|
| 2r5kW8aN | inst25_activity 法1 | 253（36%） | 覆盖率冠军 | 唯一可直接当主信号的日频字段 |
| xAvaWOPW | activity 法2 | 253 | 无零膨胀 | 数据实在 |
| 9qlQmZ91 | activity ts_zscore66 法3 | 254 | 更新面≈覆盖面 | 持续更新 |
| Jj8L1Mgl | position_change ts_zscore22 | 164（23%） | 22 天 23% 有仓位变动 | 中窗聚合可用 |
| YPadJLNv | concentration ts_zscore22 | 216（31%） | 22 天 31% 变动 | 中窗聚合可用 |
| bla3nGWq | position_change 法1 | 18长/15空 | 单日事件稀疏 | 需聚合 |
| gJazdkmK | cover_count 法1 | 17 | 回补事件稀疏 | 需聚合 |

画像结论：activity 是唯一日频全覆盖级字段（36%）；其余为做空披露事件流（需 22-66 天聚合）。机制假设（待审）：机构做空活跃度短期负压 / 做空仓位变动流 / 拥挤度条件轴。

## 三、两塔对比与首波建议（待审）

| 维度 | insider_agg_matrix | institutions25 |
|---|---|---|
| 数据形态 | 事件流（单日 3%） | 混合（activity 日频 36% + 事件流） |
| 主信号候选 | directional_indicator（66 天聚合） | inst25_activity（直接用） |
| 聚合窗口下限 | 66-126 | activity 即日频；事件字段 22-66 |
| TO 特性 | 裸 1.6-1.75（必须聚合+平滑） | activity 0.51 需轻度平滑 |
| 经济机制 | 内部人净买入（经典） | 机构做空流向/拥挤 |
| 建议首波 | ts_sum(di,66/126)×group_rank 8 臂 | activity rank/zscore + position_change 聚合 8 臂 |

## 四、存档
- 本报告：reports/dataset_experience/gbr_insider_institutions_profile_20261113.md
- 字段目录：tracking/GBR/reference/gbr_insider_agg_matrix_fields.json、gbr_institutions25_fields.json
- 探针批次读数：tracking/GBR/waves/gb_v1_v2_dispatch_20261113.md