# option1 波 1 模板池（DEU/TOP500/D1 · 2026-11-03）

## 一、论坛两读（article_id 已解码固化 extract_ids.py）
- **43319751480599**（FF65210, 65赞）：opt1 在 IND 3 颗已提交 ATOM（S 2.10/1.79/1.76，PC<0.5）。骨架=期权价格行业残差动量：ts_rank(ts_backfill(vec_sum(f),L),W) - ts_rank(group_neutralize(...,industry),W)；对字段不挑食。**作者提交占位 = 3 颗 opt1 价格残差族已进生产池**。
- **41024337928343**（JX84394, 78赞）：e7rAZjdl OS ACTIVE（Self 0.43/Prod 0.68）。put IV - call IV **取负=反转**（skew 陡→空）；12 日线衰减压 TO 10%。
- **43250212998807**（ZZ43261, 17赞）：Xing-Zhang-Zhao 2010 JF **smirk 越陡未来收益越低**（方向定案）。开放问题：财报前 skew 突变>静态、skew×期限复合、CROWDING 重叠。
- **41119909511319**（XH32267, 36赞）：两颗 OS ACTIVE（S 2.12/1.67）。**Ratio>Diff、同期限短期配对>跨期限**；call>put 乐观→空。
- 文献：AHXZ 2006（高 IV→低收益）、XZZ 2010、Cakici（call IV 动量正/put IV 动量负）。

## 二、机制解锁（vec_skewness 阻断的 smirk 面用矩重构绕行）
- 离散度（微笑陡度代理）= vec_avg(vi^2) - vec_avg(vi)^2（方差重构，power+vec_avg 均在册）。
- 斜率（smirk 方向）= vec_avg(vi*delta) - vec_avg(vi)*vec_avg(delta)（元素级协方差；multiply 元素级）。
- 覆盖突变 = vec_count(vi) 时序差分（期权信息沉默面）。
- 量纲自洽：power 面 vol²-vol²、协方差面 vol·delta-vol·delta、股息面 货币/货币。

## 三、方向定案
- T1/T4/T6/T12 反转取负（XZZ 陡→低 + AHXZ 高 IV→低 + 恐慌回归）。
- T2/T3 正向（cov(IV,delta) 高=微笑平=定价稳→高收益）。
- T5 正向差速（slope 抬升=变平加速→高）。
- T7 正向（金帖残差为正→上行）。T11 正向（股息率经典先验）。
- 开放臂（弱先验）：T3 坐标轴替换、T8 覆盖沉默、T9 期限结构、T10 双曲面分歧。

## 四、模板清单（12 互异 · 家族 8 · 照抄臂 1 · 开放臂 4）
- T1 离散度反转 ts_mean5；T2 delta 斜率 ts_mean22；T3 moneyness 斜率；T4 离散度突增 ts_delta22；T5 斜率快慢差速 5/66；T6 IV 水平 ts_quantile(22,252)；T7 价格残差骨架 backfill5/rank66；T8 vec_count 覆盖骤减 22；T9 期限协方差 22；T10 双曲面分歧 22；T11 股息率 ts_mean22；T12 质量恶化 ts_delta22。
- 窗口全部白名单（5/22/66/252）；分组轴 subindustry；全部单数据集 option1 单塔（category 待塔位登记，无混塔）。

## 五、覆盖闸
- option1 满 10 年 ✓（P1/P2 探针 2014-23 全有数，prior 轮实测）；dataset cov=0.0 为失真值不作判据（三证在案）。

## 六·五、收批归因（2026-11-03 全 12/12 终态齐 — 判弱封组合）
| 臂 | 族 | 终态 | S | 判 |
|---|---|---|---:|---|
| T1-T5, T9 | smirk 矩重构/协方差/斜率 | ERROR ×6 | — | event-input 设计死（power/multiply 拒 event 输入）|
| T6 | vi 水平 ts_quantile252 | TIMEOUT→**CANCELLED**（lookINTO 实证） | — | 平台取消真死，同类 T8 已测不补发 |
| T7 | 价格残差骨架 | COMPLETE mLo5wAYx | **0.74** | 全批最佳；IND 原版 2.10→DEU 0.74，覆盖骤减主因 |
| T8 | 覆盖突变 vec_count | COMPLETE d5WZkmKx | −0.28 | 死 |
| T10 | vi 水平 ts_mean | TIMEOUT→**CANCELLED**（lookINTO 实证） | — | 平台取消真死 |
| T11 | 股息比值 last_dvd/price | COMPLETE wpQamLrd | 0.15 | 弱 |
| T12 | delta_surface 突变 | COMPLETE mLo53ZE9 | −0.0 | 死 |

**结论**：① smirk 曲面形状机制在 option1 被 event-input 禁令**结构性阻断**（6/12 设计死，非信号弱）；② 价格残差面迁移失效（0.74 vs IND 2.10）；③ 股息/覆盖/delta 突变面全弱。**option1 判弱封组合，不再追投**。覆盖闸免跑（判死不入库）。
## 六、待补
- 派发实录与收批归因（按模板编号归因，不按单条）。