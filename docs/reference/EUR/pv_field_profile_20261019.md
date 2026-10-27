# EUR × Price Volume 类别 ATOM 挖掘战役 — 字段画像与回测档案

> 日期：2026-10-19 ｜ 目标：10 个过全闸的 ATOM regular alpha ｜ 风险配置：TOPCS1600 / EUR / D1 / INDUSTRY / decay1 / trunc0.08
> 方法论：先全量枚举（20 个数据集，历史台账仅记 5 个）→ 字段画像 → 双结构探针（SOP）→ 有生命者纵深穷尽

## 一、数据集全量清单与分层（2026-10-19 平台实时枚举）

### A 层（主攻：字段多 + 机制可阐述）
| ID | 名称 | 字段 | 覆盖 | 已有alpha | 信号原料 | 状态 |
|---|---|---:|---:|---:|---|---|
| pv30 | Alternate Industry Classification（PCA 统计行业） | 558 | 0.82 | 286 | 285 个 cov1.0 聚类标签（GROUP）+ 15 因子载荷（cov 0.64） | 探针中 |
| pv87 | Aggregated（非财务评级：管理质量/ESG/信任度） | 1649 | 0.50 | 893 | 评级分数（慢变量） | 待探针 |
| pv20 | Daily Spot and Cross Rate（汇率） | 1475 | 0.69 | 595 | 汇率与交叉盘 | 待探针 |
| investor_activity | Nordic Baltic 投资者行为 | 47 | **0.164** | 9 | 散户/专业投资者交易行为 | 待评估（覆盖不足疑虑） |

### B 层（小而快，一次性扫完）
| ID | 名称 | 字段 | 覆盖 | 已有alpha | 信号原料 |
|---|---|---:|---:|---:|---|
| pv47 | Specific Return（Barra 扩展残差） | 2 | 1.0 | 81 | 残差收益（risk72 同族已证伪独立信号） |
| pv103 | Interval & MOO/MOC 统计 | 9 | 0.983 | 64 | 订单失衡 / 开收盘拍卖 |
| pv106 | Microstructure Spread | 15 | 1.0 | 78 | 价差（历史判死：流动性水平为负） |
| pv109 | Bond Yield | 25 | 0.44 | 20 | 债券收益率（覆盖不足） |
| pv13 | Relationship Data | 73 | 0.66 | 332 | 标识符映射（非信号） |
| pv141 | VWAP Tick | 2 | 0.5 | 5 | VWAP |
| pv149/univ1/univ2 | 日历/宇宙 | 1–6 | 1.0 | 0–6 | 非信号 |
| pv29 | Derived Industry Classification | 80 | 0.563 | 165 | 行业标签（GROUP） |

### C 层（历史台账已判死，本轮复核而非重挖）
| ID | 历史死因（2026-10-13 判） | 本轮动作 |
|---|---|---|
| continuation_score（560） | ★平滑即杀，alpha 全在高频 | 复核高频形态 |
| intraday_pv_feats（585） | TO 爆炸（最佳 2Y 1.15） | 复核事件门控 |
| pattern_scores（504） | 噪声型 S≤0.52 | 复核 breakaway 族 |
| pv37（251） | 经典反转 TO 爆炸 | 复核长窗 |
| pv106（15） | 流动性水平为负 | 已在本 Session 测过 spreadbp |

### 特别注意
| ID | 字段 | 覆盖 | 已有alpha | 风险 |
|---|---|---:|---:|---|
| pv1 | 24 | 1.0 | **44048** | 极度拥挤（prod 墙必然） |

## 二、字段画像（随探针逐个填充）

### pv30
- **结构**：4 种聚类方法 × 多宇宙（top100–1200）的统计行业标签（GROUP 型，cov 1.0）+ `pca_factor_score_{0..14}_top{宇宙}` 连续载荷（MATRIX/GROUP 混合，cov 0.26–0.67）
- **机制假设**：① 载荷 = 股票在潜在收益相关结构上的坐标，慢变；② `ts_delta(载荷)` = 统计行业迁移（机制：迁移股的收益结构改变）
- **限制**：**无 top1600 字段**（最大 top1200），TOPCS1600 上覆盖打折；类别标签无序不可直接作信号

## 三、适用模板（随实证填充）

| 模板 | 表达式骨架 | 适用字段类型 | 实测 |
|---|---|---|---|
| M1 冠军慢变量 | `signed_power(ts_zscore(ts_backfill(F,504),126),1.5)` | 慢变 MATRIX | 待测 |
| M2 迁移检测 | `ts_delta(ts_backfill(F,504),22)` ± rank/zscore | 载荷类 | 待测 |
| M3 分组轴 | `group_rank(x, GROUP字段)` | GROUP 标签 | 待测（注意 x 须同数据集才保 ATOM） |

## 四、回测结果与指标（台账）

| wave | alpha | 数据集 | 模板 | S | F | TO | 2Y | sub | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---|

---

## 五、pv87 深挖实录（按纪律：维度地图 → 整族派发 → 近闸归因）

### 5.1 维度地图（1649 字段，12 语义族）
| 族 | n | 机制假设 | 匹配模板 | 状态 |
|---|---:|---|---|---|
| R1/R2 修正计数 up/down | 91（日频33） | 修正广度 | M1 活跃度 + **M5 净价差**（同指标 up−down，同源合法） | ✅ 已穷尽核心 |
| S1 情绪 CSS | 303 | 人群情绪水平 | M1（expavg 慢）/ rank（simpleavg1 日频） | 部分（10/303，先行批全弱） |
| S2 情绪 NIP | 291 | 同上 | M1 | 待做 |
| S3 事件情绪 | 260 | 事件情绪 | M1 | 待做 |
| C1 共识均值 | 49 | 水平无信号，**修正在变化** | M4 `ts_delta(backfill,22)` | 待做 |
| D1 预估离散度 | 29 | 不确定性 | M1（预期负号） | 待做 |
| R3 持平计数 / R4 分析师数 / D2 尺度 / S4 / X其他 | ~1000 | 覆盖度/尺度类 | 辅助族 | 待做 |

### 5.2 修正族实测（M5 净价差 = 本战役 PV 类别最强信号）
| 形式 | S | F | TO | 2Y | sub |
|---|---:|---:|---:|---:|---:|
| net ebit @ INDUSTRY | 2.54 | 2.27 | 0.094 | 0.82 | 1.40 |
| **net ebit @ CROWDING** | **2.66** | 2.17 | 0.077 | 0.90 | **1.47** |
| **net ebit @ SECTOR** | 2.57 | **2.42** | 0.077 | 0.95 | 1.46 |
| net net_income @ SECTOR | 2.32 | 2.08 | 0.073 | **1.02** | 1.29 |
| 归一化广度 (up−dn)/(up+dn+nc) ebit | **2.62** | 2.35 | 0.082 | 0.98 | 1.25 |
| 归一化广度 net_income | 2.21 | 1.83 | 0.076 | 0.72 | 1.02 |
| M1 单边计数（up/down 各自） | −1.14~0.77 | — | — | 负 | 全灭 |

**全部卡死在 2Y**（0.36–1.02，缺 1.58 约 0.6）。

### 5.3 ★ 近闸归因（`omolJzjl` 逐年，纪律要求先归因再推进）
| 年 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 4.56 | 3.53 | 2.37 | 5.05 | 3.04 | 2.26 | **1.04** | 3.07 | **1.21** | **0.81** |

- **归因：2020 年起的长期衰减（1.04→3.07→1.21→0.81），非 2022-23 突变**
- 机理：分析师修正广度是**被最广泛消费的经典信号**，拥挤衰减自 2020 COVID 后加速
- 2023 margin 9.7bp（2017 年 39.6bp 的 1/4）
- CROWDING/SECTOR 只能 +0.1~0.2，**缺口 0.6 无法由设置档修补**
- 同族其他指标（ebitda/net_income/ebt）衰减形态一致 ⇒ **家族级 2Y 死亡，非个别字段**

### 5.4 判定
- **pv87 修正族：S/F/sub 六星但 2Y 结构性死亡 ⇒ EUR 闸线下不可交付**
- 死集复核（continuation/intraday/pattern/pv37 新档位）：8 条全弱（最好 S 1.28 但 TO 1.27）⇒ **历史死刑维持**
- CSS/NIP/事件情绪：先行批全弱（simpleavg1 TO 1.4-1.6 爆炸；expavg 慢频 S≤0.58）⇒ 族级低生命

---

## 六、★★★ 净修正族 2Y×sub 车道闭合证据链（按论坛 LL46807 协议整理）

### 6.1 机制与强度
`subtract(rank(bf(numup,W)), rank(bf(numdown,W)))` 净修正广度：**S 2.0–2.7、F 2.0–2.5、sub 1.3–1.5、CLUSTER 1.86**——PV 类别 20 数据集里唯一六星族。

### 6.2 归因（逐年）
2020 起长期衰减（1.04→3.07→1.21→0.81）＝拥挤衰减；缺口全部集中在 2Y 与 sub/S 比率（0.51–0.52，需 0.53）。

### 6.3 已闭合的车道（救援清单，30+ 变体）
| 车道 | 尝试 | 最好结果 |
|---|---|---|
| 中性化 | INDUSTRY/SECTOR/CROWDING/SUBINDUSTRY | CROWDING 2Y +0.5（1.66） |
| zscore 包裹窗 | 252/315/340/378/504 | z252→2Y 1.66；z504→sub 1.14 |
| signed_power | 0.5/0.51/0.52/0.55/0.6/0.65/0.7/1.5 | 0.5→2Y +0.21 |
| backfill | 5/22/66/126 | bf66 均衡 |
| 平滑/整形 | ts_decay_linear 3/5、ts_mean 5、winsorize std4、ts_rank 66、归一化广度比 | 无增益 |
| 字段机制 | ebit/ebitda/ebt/eps/net_income/净额比 | net_income sub/S=0.57 但 CROWDING 杀 S |
| 规模倾斜 | estimate_scale 双向 | 比率不变（sub 宇宙非规模切分） |
| 设置档 | decay 2/4、SUBINDUSTRY | 无改善或杀信号 |

### 6.4 双车道前沿（最近交点）
| 配置 | S | F | 2Y | sub | sub限(0.53S) | 缺口 |
|---|---:|---:|---:|---:|---:|---|
| **z252+bf66+p0.52 @ CROWDING** | 2.01 | 1.42 | **1.65✓** | 1.05 | 1.065 | **sub 差 0.015** |
| z378+bf66+p0.6 @ CROWDING | 2.12 | 1.55 | **1.64✓** | 1.08 | 1.124 | sub 差 0.044 |
| z315+p0.6 @ CROWDING | 2.07 | 1.50 | **1.72✓** | 1.04 | 1.097 | sub 差 0.057 |
| z504+bf66+p0.5 @ CROWDING | 2.13 | 1.53 | 1.48 | **1.14✓** | 1.129 | 2Y 差 0.10 |

**两车道无交集**：2Y 车道（z252–378）最近距 sub 过闸差 0.015；sub 车道（z504）距 2Y 过闸差 0.10。

### 6.5 结论（按论坛协议上报裁决）
- 30+ 变体、7 条车道全部闭合，2Y×sub 交点不存在
- 机理：CROWDING 剥掉拥挤成分救活 2Y 的同时，恰好剥掉了 sub 宇宙（低流动性段）的信号强度——两个修复互斥
- **最近候选 `GrgL5qm5`（z252+p0.52，sub 差 0.015）与 `npA2rXQl`（z504，2Y 差 0.10）留档**；若未来赛季 sub 宇宙定义或闸线调整，可立即复检

---

## 七、算子使用全景分析（2026-10-20，804 条表达式 / ~130 批实证）

### 7.1 使用中的算子（按场景分类，附实测效果）

**A. 信号构建核心（每颗 alpha 的骨架）**
| 算子 | 使用场景 | 实证结论 |
|---|---|---|
| `vec_avg` | VECTOR 字段（ai_equity_alpha 全部字段）聚合为截面序列 | 唯一可用的向量聚合（stddev 反效） |
| `ts_backfill` | 处理 NaN/低频更新，拉长历史覆盖 | **三赢**：覆盖↑、S↑、TO 可控；窗口须匹配字段更新频率（504 给慢字段 / 22 给快字段） |
| `ts_delta` | 提取「变化量」（载荷迁移、修正增量） | 事件/迁移机制必备；单独用 S 弱 |
| `subtract` | 同指标 up−down 价差（净修正广度）、规模倾斜 | **净修正价差 = PV 类最强信号**（S 2.0–2.7） |
| `multiply` | 规模倾斜、双通道 blend | 硬倾斜伤 robust；blend 稀释 sub |
| `divide` | 日内价格比（收盘/开盘）、归一化广度比 | 比率形态可保序 |

**B. 截面归一化 / 整形（决定持仓位置）**
| 算子 | 场景 | 结论 |
|---|---|---|
| `rank` | 一切信号的截面归一化基座 | 与量化/分位同族，最稳 |
| `quantile` | F 提升器（0.65→0.74）；cauchy 变体反效 | 默认 driver 可用 |
| `winsorize` | 极端值压缩（std 3/4） | 弱正向；std≥3 饱和 |
| `tail` | 尾部截断 | 反效 |
| `signed_power` | **2Y 连续旋钮**（0.5→+0.21；1.4–1.7 区间可调 2Y） | 本轮最有效的单一杠杆 |
| `abs` | 幅度型信号（不用方向的场景） | 偶用 |
| `normalize` | limit 2 最优；limit 1 杀 S；useStd=false 对照 | 仅调 limit 有效 |

**C. 时序标准化（2Y 与 sub 的分水岭）**
| 算子 | 场景 | 结论 |
|---|---|---|
| `ts_zscore` | 时间标准化（robust 提升器 + 2Y 修复） | **杀 sub**（任何窗口 22–504） |
| `ts_scale` | ts_zscore 的替代品 | 与 ts_zscore 表现逐位一致 |
| `ts_mean` | 平滑 | 保 sub 比率但不救 2Y；在部分字段杀 S |

**D. 分组轴（中性化与分组）**
| 算子 | 场景 | 结论 |
|---|---|---|
| `group_rank(x, sector)` | 分组截面排序 | sector 轴最优 |
| `group_neutralize` | 表达式内中性化 | robust 0.85–0.86；但可被 group_rank 等价替代 |
| `group_zscore` / `group_scale` / `group_mean` / `group_std_dev` / `group_count` / `group_cartesian_product` / `group_backfill` / `rank_by_side` | 分组族穷尽测试 | 除 rank/neutralize 外全部弱或退化（group_mean → S 0） |

**E. 正交 / 统计（残差化与相关性）**
| 算子 | 场景 | 结论 |
|---|---|---|
| `vector_neut(x, size)` | 对规模正交（替代硬倾斜） | **robust 0.86**，不伤 2Y |
| `vector_neut(x, risk70)` | 论坛点塔模板 | 2Y −0.1~0.18，对 2Y 余量薄的候选是毒药 |
| `ts_regression` / `ts_covariance` / `ts_corr` / `ts_ir` / `ts_kurtosis` / `ts_product` / `ts_sum` / `ts_std_dev` / `ts_av_diff` / `ts_quantile` / `vec_stddev` | 统计族穷尽 | 全部弱或反效（协方差非信号、kurtosis S 0.16） |

**F. 事件 / 条件**
| 算子 | 场景 | 结论 |
|---|---|---|
| `trade_when` | 条件门控 | 伤 F（S 1.49/F 0.97） |
| `if_else` / `less` / `greater` | 门控条件构造 | 同 trade_when |
| `kth_element(k=1)` | 取最近有效值（滞后） | **2Y 最强单项提升器（1.46→1.92）** 但 S/robust 低 |
| `last_diff_value` / `days_from_last_change` / `ts_arg_max` | 事件时点族 | 全灭（时点是反信号） |

**G. 换手控制**
| 算子 | 场景 | 结论 |
|---|---|---|
| `ts_decay_linear` / `hump` / `ts_target_tvr_decay` / `ts_target_tvr_hump` | TO 控制族穷尽 | decay_linear 3/10 弱；hump 0.001 可用（S 1.46）；tvr_hump 是限速族里 2Y 最优（1.69） |

### 7.2 未使用的算子及原因

| 算子族 | 算子 | 未用原因 |
|---|---|---|
| 保序逐点变换 | `log` / `exp` / `sqrt` / `sign` / `sigmoid` / `tanh` / `signed_log1p` / `log_diff` / `power` | **保序形变在 rank/quantile 外层逐位同效**（项目铁律实证）；只有 signed_power 因改变持仓位置（非线性压缩）而有效 |
| 幽灵算子 | `ts_entropy` / `ts_skewness` | 平台不存在（类别卡明令禁止，op-lint 拦截） |
| 数据工程 | `ts_fillna` / `ts_count_nans` / `ts_shift` / `ts_delay` | ts_backfill 已覆盖 NaN 与滞后需求（且 kth_element 已测滞后） |
| 现成字段替代 | `ts_returns` / `ts_percentage` | pv1 数据集直接提供 returns 字段，无需从价格构造 |
| 时间索引 | `ts_step` | 单调递增计数器，乘入信号产生无界值 |
| 极值类 | `ts_min` / `ts_max` / `ts_min_max` / `ts_max_diff` / `ts_min_diff` / `ts_arg_min` | 慢变字段的极值被 backfill 平滑掉；收益率字段的极值引入噪声。⚠ **ts_max_diff/ts_min_diff（论坛 mm 结构）未测，是唯一缺口** |
| 冷门 group 变体 | `group_rank_ratio` / `group_neutralize_rank` 等 | 单信号 ATOM 下，group 聚合产生组内常数、无截面离散度（group_mean 实测 S=0 证） |
| 自定义分组 | `bucket` | 需 rank 内层（单位闸），且分组轴已被 sector/pca 覆盖 |
| 反转 | `reverse` | 一元取负与 `-x` 等价，仅偶用 3 次 |
| 暴露控制 | `scale` | 目标暴露控制由 settings 层（truncation）承担，且实测 truncation 零杠杆 |

### 7.3 缺口结论
55 个算子已实测覆盖；未用的 20+ 个中，**只有 `ts_max_diff`/`ts_min_diff`（论坛 mm 结构）值得补测**，其余均有机理或实证依据跳过。

### 7.4 缺口补测结果（wave732，2026-10-20）
| 算子 | 语义（平台权威） | 机制假设 | 实测 | 判定 |
|---|---|---|---|---|
| `ts_max_diff(x,d)` | **x − ts_max(x,d)**（距窗口峰值距离，峰值相对） | 同时含「水平+衰减」信息，或可穿过 2Y×sub 互斥 | S 0.11–0.83（@CROWDING）/ 1.28（@SECTOR），2Y −1.61~1.71 但强度近零 | **DEAD**：修正计数的「峰值」无预测力 |
| `ts_arg_min(x,d)` | 距窗口最小值的天数 | 时点信号 | S 0.26，2Y 1.71 但无截面强度 | **DEAD** |
| `ts_min_diff` | **平台不存在**（103 算子清单无此项） | — | — | 不可用（非未用） |

⇒ **算子覆盖至此完整**：57 个已实测，未用的每个都有机理或实证依据；ts_max_diff/ts_arg_min 缺口已闭合。
