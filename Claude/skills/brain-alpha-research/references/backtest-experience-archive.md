# 回测经验档案（Backtest Experience Archive）

> 基于 2026-08 全量回测数据（281 个存档文件 / 1957 条回测记录）系统性提炼。
> 覆盖轨道：KOR（主目标）、ASI（早期探索）、USA option（并行探索）。
> 数据源：`wqb-share-03/tracking/` 全部 `result_*` / `kor_*` 存档。
> 关联：[[forum-template-library]]（模板）、[[webdatascope-data-quality]]（预筛）。

---

## 1. 数据集评级总表（按区域）

### KOR（TOP600/D1，主目标）
| 评级 | 数据集 | 样本 | ≥1.3 | ≥1.5 | 峰值 | 结论 |
|---|---|---|---|---|---|---|
| ★★★ | pv106（流动性） | 43 | 10 | 8 | 1.68 | **唯一 sharpe 引擎**；族内 blend 全灭（8/8 <0.3） |
| ★★★ | pv106 × analyst39 blend | 8 | 8 | 8 | **2.00** | **最强范式**：流动性腿 × 盈利腿 add 混音 |
| ★★★ | analyst44（盈利预测） | 15 | 11 | 7 | 1.63 | 单独即可达标，2Y 1.63+，年度 2017-2022 连续大年 |
| ★★ | analyst25 | 13 | 1 | 0 | 1.32 | 弱信号，仅个别窗口 |
| ★★ | other323 | 7 | 1 | 1 | 1.52 | 偶发 |
| ★ | analyst39 | 16 | 0 | 0 | 1.22 | **单独无效，只作为 blend 腿** |
| ✗ | glb_theme（GLB/D1 主题） | 25 | 17 | 16 | 1.94 | 峰值高但三区域子域（EMEA/APAC 0.3-0.5）结构性不达标 |
| ✗ | **analyst16（评级/修订类，2026-08-04 b1/b2）** | 16 | 0 | 0 | 0.55 | VECTOR 评级字段全灭（meanrec/reccode/highrec/scer/afterest），best 0.55；用 `ts_rank(vec_avg(...))` 聚合 |
| ✗ | fundamental6/44、risk65/71、model53/28/192、insiders5、shortinterest3、news46 | 全部 | 0 | 0 | <1.0 | 信用风险/基本面/新闻类在 KOR **整体无信号** |

### ASI（早期探索）
| 评级 | 数据集 | 样本 | ≥1.3 | ≥1.5 | 峰值 | 结论 |
|---|---|---|---|---|---|---|
| ★★★ | model110（ML/AI 复合） | 16 | 9 | 9 | 2.42 | 强信号，但 2Y(IS_LADDER) 与 asi_jpn 子域双卡 |
| ★★★ | **model30（EPS Estimate Model）** | 8 | **7** | 0 | **1.46** | **论坛 star_eps_surprise_prediction_fy1 真字段**，44 窗模板 1.39-1.46，2Y/rn 同步达标（2026-08-04 b22 验证，详见 [[asi-methodology]]） |
| ★★ | fundamental_asi | 24 | 17 | 9 | 1.61 | 峰值可用，需过 RA |
| ✗ | news104/7/29、sentiment、institutions、analyst_asi、model144、fundamental44 | 全部 | 0 | 0 | <1.0 | ASI 新闻/情绪类全灭 |

### USA option（并行探索）
| 评级 | 数据集 | 样本 | ≥1.3 | 峰值 | 结论 |
|---|---|---|---|---|---|
| ★★★ | option40（IV skew + put-call theta 差分） | 40+ | 多 | **2.74** | skew 全指标过但 prod_corr>0.75；theta diff 过 sharpe 但 2Y fail；两者复合是正解 |
| ★ | option3 | 8 | - | 1.54 | volcall 比率弱信号 |

### IND / GLB / 小区域（2026-08-05 补测）
| 区域 | 峰值 | 结论 |
|---|---|---|
| IND（TOP500） | model77 composite 反转 **0.97**；model110 0.56 | 单国小池天花板 ~1.0；composite_score_qsg_india 强反向信号（正向 -1.1） |
| GLB（TOPDIV3000，b8 突破 2026-08-05） | **pred10d country 250：2.68/1.35/2Y 1.75** | **country 分组攻破三区域墙**（ASI JPN 经验跨区域复现）：`group_rank(ts_rank(ts_backfill(winsorize(pred10d,std=5),60),250),country)` @ FAST/decay10 = 全 PASS；decay6→10 把 tvr 29.9→24%、margin 4.4→5.06bp |
| DEU | model106 rv **0.85** | 新区域数据不足（pv 族未灌入），等数据补全 |
| GBR | pv106 反转 × model238 blend **1.04** | pv106 在 GBR 方向反转（KOR 做多 spread，GBR 做空 tcp）；等数据成熟 |
| EUR | model30 0.6 / pv20 0.36 / news21 0.72 | 预筛数据包（2026-02）与平台脱节：推荐榜 4/8 无数据 |

---

## 2. 模板范式（最硬的数据发现）

对 288 个成功样本（sharpe≥1.3）vs 全量 1957 的算子使用率对比：

| 算子 | 成功样本使用率 | 全量使用率 | 判定 |
|---|---|---|---|
| `winsorize` | 20.5% | 5.3% | **成功 4 倍** |
| `ts_backfill` | 20.5% | 5.1% | **成功 4 倍** |
| `add`（跨数据集 blend） | 9.6% | 2.1% | **成功 4.6 倍** |
| `ts_rank` | 31.3% | 28.0% | 略高 |
| `group_rank` | 25.3% | 37.9% | 反直觉：全量多但成功少（因大量失败批次也用 group_rank） |
| `ts_zscore`/`ts_mean`/`zscore`/`vec_avg` | **0.0%** | 23.2% | **成功中 ZERO** |

**结论（KOR/ASI 通用）**：
1. **成功范式 = 排序 + 清洗 + 混合**：`ts_rank/group_rank` 排序 × `winsorize(std=5)` + `ts_backfill(60)` 预处理 × `add` 跨族混音。MINVOL1M 论坛模板（3.28 分）完全验证：`group_rank(ts_rank(ts_decay_linear(ts_backfill(winsorize(F,std=5),60),5),30),country)`。
2. **`ts_zscore(ts_mean(vec_avg(F),d))` 平滑模板在 KOR/ASI 是死亡模板**：news104/7/29、sentiment、analyst_asi、institutions 全部批次用它，0 成功。
3. **族内 blend 无效**：pv106 内部 8 个 blend 全灭（0.28 峰值）；**跨族 blend 有效**（pv106×analyst = 2.00）。

---

## 3. 设置维度（区域最优配置）

| 区域 | universe | delay | decay | 中性化 | trunc | max_trade |
|---|---|---|---|---|---|---|
| KOR | TOP600 | 1 | 12 | **SECTOR** | 0.04 | ON |
| ASI | MINVOL1M/TOP500 | 1 | 6-12 | SUBINDUSTRY（论坛）/SECTOR | 0.04-0.08 | ON |
| USA option | TOP3000 | 1 | 6 | **SLOW_AND_FAST** | 0.04 | ON |

坑：USA option 的 theta diff 字段与 SUBINDUSTRY 中性化不兼容（4 个全 "No alpha ID"，STATISTICAL 可用）。

---

## 4. RA 检查瓶颈（按区域）

| 检查 | KOR | ASI | USA |
|---|---|---|---|
| LOW_SHARPE | 易过 | 易过 | 易过 |
| **IS_LADDER_SHARPE（2Y）** | **主瓶颈**（1.3-1.5 档全 fail） | **主瓶颈** | theta diff 常 fail |
| LOW_SUB_UNIVERSE | 偶发 | asi_jpn 子域必卡（<1.0） | - |
| prod_corr | 达标需 <0.7（实测产出相关 | | 0.66-0.79 冲突 |
|  | 0.66-0.79 族内冲突） | | skew 族 >0.75 |

经验：2Y 不足时 → 拉长窗口（ts_rank w 66→88→100）或换信号源（6 武器之首）；ASI 必须提前验 asi_jpn（JPN 单域）。

---

## 5. 平台硬性约束速查（全部实测验证）

- `winsorize(F, std=5)` — std 为命名参数（位置参数报 Invalid inputs）
- `ts_backfill(F, lookback=60)` — 仅命名参数
- `hump(x, hump=0.01)` — 第二参仅命名
- VECTOR 字段必须 `vec_avg/vec_ts_rank` 等 vec_* 算子
- **`vec_ts_rank` 实测不是可用算子**（"Attempted to use inaccessible or unknown operator"，2026-08-04 analyst16 b1 8 连败的根因）——VECTOR 字段时序排名正确写法：`ts_rank(vec_avg(F), d)`（先聚合再排名），或用 vec_avg 内嵌条件
- EVENT 字段不支持 `ts_rank/ts_delta`（批次原子 CANCELLED）
- `ts_regression + densify(sector)` 组合不兼容（通用运行错误）
- RAM 中性化在回测 API 实测 400 不可用（主题公告虽允许）
- set_alpha_properties 的 descriptions 传 "None" 字符串会被拦截

---

## 6. 六武器有效性评价（KOR 实测）

| 武器 | 预期降相关 | KOR 实测 | 评价 |
|---|---|---|---|
| 换字段族 | 0.2-0.4 | insiders5 0.88 → pv106 1.53 | **最有效** |
| 换中性化 | 0.05-0.08 | 零成本 | 有效（保底手段） |
| 换窗口 | 0.05-0.15 | ttm66→100 稳定 1.5+ | 有效（微调） |
| 信号反转 | 0.10-0.18 | 评级类双向验证 | 验证用 |
| 换 operator | 0.03-0.10 | ts_rank→group_rank 等 | 微效 |
| 多字段 blend | 0.05-0.15 | **跨族 2.00（最强）**；族内全灭 | 跨族有效 |

---

## 7. 方法论沉淀

1. **KOR 有效信号仅两类**：pv106 流动性（sharpe 引擎）+ analyst 盈利预测（blend 腿/独立信号）。第 3 个独立达标数据集受数据现实约束——先试 analyst16（评级/修订类，与 39/44 不同源）。
2. **先验数据再回测**：主题公告（get_messages）→ WebDataScope 预筛 → get_datafields 看 cov/类型 → 小批次验证（4-8 表达式）。
3. **批次纪律**：8 并发；队列拥堵时取消重提 4 表达式小批次（~14 分钟 vs 3 小时）。
4. **混音法则**：add 的两个腿必须不同信号族（流动性×盈利），同族 blend 无效；blend 前先确认两腿单独可用。
5. **达标后流程**：robust + 严格过拟合 → 相关性（<0.4）→ set_alpha_properties（GREEN）→ 不提交（用户手动）。
