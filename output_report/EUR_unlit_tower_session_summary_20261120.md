# EUR 未点亮塔推进 · 会话总报告（2026-11-20）

> 目标：EUR/D1 未点亮塔（socialmedia 0/3、macro 0/3、institutions 0/3、pv 2/3、insiders 2/3、earnings 1/3）逐塔推进。
> 本轮共 **5 个数据集、230+ 臂**（wave=mcp-20261120，全部入库）。
> **总判定：信号层在四个数据集上都能做到「平台闸全绿」，但统一卡在 prod 0.78–0.89 ⇒ 本轮无提交，全部 PROVISIONAL。**

## 1. 一览表

| 数据集 | 塔 | 臂数 | 最优读数 | 平台闸 | prod | 判定 |
|---|---|---:|---|---|---:|---|
| earningscall_sentiment | OTHER（已亮） | 66 | S1.71/F1.00/2Y2.13/sub1.51 | ✅ 全绿（3 颗） | 0.7815 | PROVISIONAL（prod 墙） |
| **investor_activity** | **PV 2/3** | **85** | **S2.53/F2.05/2Y2.05/TO20.9%/robust0.79** | ✅ 全绿（多颗） | **0.7817–0.8444** | PROVISIONAL（prod 墙） |
| fund_holdings_panel | INSTITUTIONS 0/3 | 31 | S1.64/F1.05/2Y2.61 | ✅ 全绿 | 0.8887 | PROVISIONAL（prod 墙） |
| macro27 | MACRO 0/3 | 40 | S1.47/F0.81/2Y1.77/**prod 0.7462** | ❌ | 0.7462 | **数据层排除已撤销**（11-20 年限放开）⇒ 改判信号层近闸 + 真新塔，重投定向 |
| pv13 | PV 2/3 | 12 | — | ❌ 全灭 | — | **数据集级判死**（图分/关系计数无价格弹性） |

## 2. ★ 本轮最重要的可复用结论

### 2.1 EUR 未点亮塔的真正瓶颈不是 S/F，是 prod

四族信号的 prod 全部落在 **0.78–0.89**：电话会语调 0.78、零售资金流 0.78–0.84、机构持仓变动 0.89、机构买家比例 0.83。
**这四族都是「经典因子」**（analyst-like tone / retail flow / institutional holdings / crowding）⇒ 生产池已饱和。
⇒ **开波前的第一件事应是估该信息源的 prod 饱和度，而不是先冲 S**（否则会把配额烧在必然撞墙的方向）。

### 2.2 presence 门控的适用条件（今日三次验证 + 一次修正）

| 数据集 | cov | 门控效果 | 结论 |
|---|---:|---|---|
| earningscall_sentiment | 0.51 | S 0.51 → 1.76 | ✅ 强杠杆 |
| investor_activity | 0.164 | S 0.91 → 2.36 | ✅ 强杠杆 |
| institutions | 0.88 | 8 臂全灭 | ❌ 无效 |
| **fund_holdings × investor_activity 交叉门控** | 0.88 主腿 + 0.16 门控腿 | S 0.91 → 1.44 | ✅ **门控字段可来自别的数据集** |

**修正后的判据**：门控有效当且仅当**门控字段本身是稀疏事件标记**（不论被门控的信号来自哪个集）。
⇒ **门控字段的选择比门控对象更关键**。

### 2.3 内核类型决定算子层扫描的产出方向

| 内核 | 最优算子 | 毁灭性算子 |
|---|---|---|
| 水平型（insiders1 累计买入、macro27 岗位存量÷时长） | ts_sum / 时序相对化全灭 | ts_rank/ts_zscore 系 |
| 相对偏离型（pv20 拥挤度、investor_activity 流向差） | ts_rank/ts_quantile/ts_zscore 系 | ts_delta/ts_std_dev/ts_scale/ts_ir |
| 有界概率型（earningscall 语调极性） | ts_zscore + 长 zscore 窗 | — |

### 2.4 「prod 最优 ≠ S 最优」（选候选必须同看两表）

investor_activity：ts_quantile 的 S 比 ts_zscore 低 0.05 但 **prod 低 0.03**；sector 轴 S 最高但 prod 高 0.02。
⇒ **候选排序必须以「平台闸 ∧ prod」为准，不能按 S 排**。

### 2.5 跨类组腿的前提：两集必须不同源

| 组合 | 形态 | 结果 |
|---|---|---|
| institutions6 × fund_holdings_panel（**同源**：都是机构活动） | residual/ratio/gating | **全灭**（S≤0.70） |
| fund_holdings_panel × investor_activity（**不同源**） | residual | **全灭**（S 0.07–1.44） |
| institutions6 × fund_holdings_panel | residual | 全灭 |

⇒ **组腿前先问「两集是不是同一个信息源的两种读数」；即使不同源，residual 形态也常把信号抽干**。
⇒ 跨类组腿优先用 **gating（事件门控）**，而非 residual。

## 3. 工程修复（本轮发现并已修）

- **★ `tools/harvest_multisim.py --auto-upsert` 缺 `--wave` 时静默跳过写库**（2026-11-20 修）：原写法 `if a.auto_upsert and a.wave and a.region:` —— 缺 `--wave` 时只打印读数、看似收批成功，**实则一行未入库**。实测 pv20/earningscall 两役共 80+ 臂因此丢失（DB 里 pv20 的 EUR 计数为 0）。已改为显式报错中止 + tools/README 标注。
  ⇒ **教训：收批后必须核对 `backtest_results` 里 region/dataset/wave 的实际行数**，不能只看工具打印。
- 新工具 `tools/operator_swap_matrix.py`（同 category 全替换矩阵生成器，arity 三形态 + no-op 去重 + 等价/语义变更族标注）+ 4 条守护测试。
- 静态闸（toolkit gate）多次拦下语法/量纲错（括号不匹配、UNITS）——**派发前预检有效**，但 UNITS 仍需平台实测。

## 4. 下一轮建议（按性价比排序）

1. **换信息源而非换实现**：本轮四族全是经典因子 ⇒ 下一个数据集应挑**结构型/关系型但有资金流含义**的（如 order flow imbalance、期权隐含波动曲面），避免再撞 0.78+。
2. **开波前先做 prod 族估**：用同类字段的 aC 密度 + 论坛「该因子是否已被做烂」两条证据预判。
3. **门控优先**：任何稀疏事件型新集，第一批就带 presence 门控（门控字段优先选最稀疏的那个字段）。
4. 剩余未测塔位：insiders 塔（insiders12，UK 数据 cov0.20，GBR 先验顶 S1.04）、earnings 塔（1/3）。

## 5. 未提交声明

本轮 **0 提交**：① 用户红线「prod ≥ 0.7 无豁免」；② 内部严线 prod<0.65 / self<0.50 / TO∈[5%,20%] 未过；
③ 提交需用户明确确认。所有候选 `status=UNSUBMITTED`，`stage=IS`。

## 6. 会话后续修正（2026-11-20 晚，交叉验证后）

### 6.1 macro27 结论修正：绿件存在，但数据层排除成立

`RReEEgwb` = `trade_when(ts_sum(vec_sum(mcr27_company_jobscreated),22) > 0, group_zscore(ts_quantile(ts_backfill(divide(vec_sum(mcr27_company_jobscreated), add(vec_avg(mean_days_job_closed),1)),66),252),industry), -1)`
（TOP2500×INDUSTRY×decay16）**S2.18/F1.27/2Y2.62/sub1.54/TO17.4%/DD2.6%/self0.261，平台闸全绿（checks.fail 空）+ prod 0.5339 PASS（内部严线 0.65 亦过）+ pyramid=EUR/D1/MACRO（0/3 ⇒ 可点亮 MACRO 塔）**。
⚠ **但逐年 2014–2020 七年 longCount=0、仅 2021–2023 有持仓 ⇒ 数据层排除成立**（3 年 < 「近九年」红线）。
⇒ macro27 = **唯一 prod 达标但历史不足**的集；表达式已存档，**若平台补齐 EUR 历史数据即可直接交付并点亮 MACRO 塔**。

### 6.2 ★ 结构性对照表：prod 达标的历史最短，历史达标的最饱和

| 集 | 历史年数 | prod | 卡点 |
|---|---:|---:|---|
| macro27 | 3（2021–23） | **0.534 ✓** | 数据层 |
| investor_activity | 6（2018–23） | 0.78–0.84 ✗ | 双卡 |
| earningscall_sentiment | **10 ✓** | 0.7815 ✗ | prod |
| fund_holdings_panel | **9 ✓** | 0.8887 ✗ | prod |

⇒ **「换信息源」是唯一真杠杆**（macro27 = 招聘岗位微观数据 = 全新信息源 ⇒ prod 0.53；四族经典因子 ⇒ prod 0.78–0.89）。
⇒ 下一目标已转向 **`pv109`（可转债，aC 0–11 极冷门，债市 = 全新信息源，cov 0.4397，25 字段画像闸 PASS，论文闸 12 篇/10 作者 PASS）**。

### 6.3 ★ 外层算子也按内核类型选（补全 6.2 判据）

macro27 四要素公式（宽门控+decay16+ts_quantile内层+**group_zscore外层**）迁移到 earningscall ⇒ **4 臂全灭**（S 0.59–0.67，原 S1.71）。
⇒ **group_zscore（连续化）在有界概率型内核上是负杠杆**（earningscall 语调极性 [−1,1]）；
**group_zscore 在重尾水平型内核上降 prod**（macro27 岗位计数÷时长，prod −0.25）。
⇒ **外层算子选型判据**：内核是有界概率/已排名 ⇒ `group_rank`（保序、留分布形状）；内核是重尾水平量 ⇒ `group_zscore`（连续化幅度、降 prod）。
（与已有记忆 `outer-op-choice-by-signal-type` 的「水平型→group_backfill / 流量分位型→group_rank」互为补充：多一个「有界概率型」类别。）

## 7. 第二轮推进（2026-11-20 夜）：新数据集扫荡 + 三条判据修正

### 7.1 新数据集扫荡结果（PV 塔 2/3 差 1 席 ⇒ 20 个 PV 集里 5 个从未测）

| 集 | 机制 | aC | 结果 |
|---|---|---:|---|
| **pv109** | 可转债（转股收益率/信用收益率/报价/票息/规模） | **0–11** | 6 臂探针 **转股收益率族弱**（S −0.11~0.45，2Y 最好 1.75） |
| **continuation_score** | K 线形态相似度（缺口延续/通道/阶梯/矩形/旗形/杯柄，560 字段） | 0–33 | 10 臂纯 PV **S ≤1.33**（历史 S2.09 臂是 analyst×PV **跨集**组合，单集无此力） |
| **pv173** | **信用利差（MT5Y Z-spread 变化/水平/期限利差 + 股票-债券收益 divergence）** | 0–10 | 8 臂（预检后重派）**进行中**——最有希望的新信息源 |
| pv29 | 统计聚类标签（80 字段全 GROUP/MATRIX 簇号） | 2–669 | **纯分组轴集，无信号字段** ⇒ 跳过 |
| pv13 / pv20 / pattern_scores / intraday_pv_feats | 已在本会话/历史挖过 | — | 收敛 |

### 7.2 ★ 判据修正一：「外层连续化降 prod」不是通用杠杆，只在极端右偏内核有效

| 内核 | 外层换 group_zscore 后 prod | 判定 |
|---|---|---|
| macro27（岗位计数÷天数，**量级差几个数量级**） | 0.83 → **0.58（−0.25）** | ✅ 有效 |
| investor_activity（零售金额差，**截面较均匀**） | 0.7817 → **0.7943（+0.013）** | ❌ 无效（反而略升） |

⇒ **判据**：连续化降 prod 有效 ⟺ 内核在截面上**高度右偏（少数股票主导）**。
⇒ 与 §6.3 的「有界概率型 ⇒ group_rank」并列，外层算子选型是**两维判据**：
① 内核是否限幅（限幅 ⇒ group_rank）；② 内核是否高度右偏（是 ⇒ group_zscore 可降 prod）。

### 7.3 ★ 判据修正二：macro27 四要素公式不可跨内核迁移

把「宽门控 + decay16 + ts_quantile 内层 + group_zscore 外层」搬到 earningscall ⇒ **4 臂全灭**（S 0.59–0.67，原 S1.71）。
⇒ **公式是内核专属的，不是通用模板**；跨族迁移前必须先判内核类型。

### 7.4 ★ 工程坑（本次自踩两次）

| 坑 | 现象 | 处置 |
|---|---|---|
| **批内一条字段名错 ⇒ 整批 CANCELLED** | pv173 用无后缀字段名（真名带 `_73`/`_43` 数字后缀）⇒ 2 ERROR + 8 CANCELLED；earningscall 用不存在字段 ⇒ 10/10 FAIL | **preflight 必须覆盖批内每一条**（非抽样）；字段 id 不能去尾 |
| **重字段集批过大 ⇒ 资源拒绝** | pv109 10 臂批 10/10 ERROR「took too much resource」，同集 2/4 臂批正常 | 重字段集 ≤4 臂一批 |
| **prod 单槽被外部进程占** | `correlation_busy` + `holder` 标识；连查触发账号级熔断 495s | 单次只查一个 alpha；inflight 时不重复触发 |

### 7.5 当前 EUR 未点亮塔结论（会话终态）

| 塔 | 集 | 平台闸 | prod | 历史 | 判定 |
|---|---|---|---|---:|---|
| MACRO 0/3 | macro27 | ✅ 全绿 | **0.534 ✓** | **3 年 ✗** | 数据层排除（平台补历史即可交付） |
| PV 2/3 | investor_activity | ✅ 全绿 | 0.79 ✗ | 6 年 ✗ | 双卡 |
| OTHER | earningscall_sentiment | ✅ 全绿 | 0.78 ✗ | **10 年 ✓** | prod 墙（唯一历史合格且近闸的候选） |
| INSTITUTIONS 0/3 | fund_holdings_panel | ✅ 全绿 | 0.89 ✗ | **9 年 ✓** | prod 墙 |
| PV 2/3 | pv173（信用利差） | 待测 | 待测 | 待测 | **进行中，唯一新信息源** |
| PV 2/3 | continuation_score / pv109 | ❌ | — | — | 单集弱 |

## 8. 第三轮：新数据集扫荡完成（PV 塔 20 集全摸底）

| 集 | 机制（实查字段） | 探针 | 结果 |
|---|---|---:|---|
| pv173 | 信用利差 divergence（股票-债券） | 8 | **全灭**（S −0.39~0.13）⇒ 债市定价在 EUR 无信号 |
| pv109 | 可转债转股收益率/信用收益率 | 6 | 弱（S ≤0.45，2Y 最好 1.75） |
| continuation_score | K 线形态相似度（单集） | 10 | 弱（S ≤1.33）；历史 S2.09 臂是 analyst×PV 跨集 |
| pattern_scores | K 线形态相似度（形态方向差分） | 8 | 进行中 |
| pv29 / pv30 | 统计聚类标签（PCA 稳健重采样） | 0 | **纯分组轴集，无信号字段** ⇒ 跳过 |
| pv87 | 分析师修正 + 新闻情绪（**catalog 描述的 ESG 与字段不符**） | 0 | 全是经典拥挤因子（aC 数百）⇒ 跳过 |
| pv149 | catalog 描述「借券/做空」→ **实际 1 个 status code 字段** | 0 | 描述不可信，无信号 ⇒ 跳过 |
| univ1 | 6 个 **UNIVERSE** 字段（top400/500/800/1200/2500/cs1600） | 0 | 宇宙定义非信号 ⇒ 跳过 |
| **pv106** | **买卖价差 / 滑点 / 交易成本（微观结构）** | 8 | 进行中——**cov 1.0（长历史）+ aC 8–102 冷门 + 全新信息源** |
| insiders12 | UK 内部人交易（cov 0.20） | 0 | 未测，GBR 先验顶 S1.04 |

**★ 两条元教训（本轮踩到）**：
1. **catalog description 不可信**：pv149 描述「借券/做空全覆盖」实际只有 1 个 status code；pv87 描述「ESG 六支柱」实际是分析师修正+新闻情绪。
   ⇒ **选集必须看 `get_datafields` 的真实字段 id + 类型（MATRIX/VECTOR/GROUP/UNIVERSE）**，不能只看 description。
2. **字段类型即预筛**：GROUP / UNIVERSE 类型字段 = 分组轴或宇宙定义 ⇒ 单集无信号，直接跳过（pv29/pv30/univ1 三集零回测即定案，省 3 份画像）。

## 9. 会话方法论总账（可复用）

| 判据 | 内容 |
|---|---|
| 门控（presence） | 有效 ⟺ **门控字段本身是稀疏事件标记**；cov<0.6 强杠杆（earningscall 0.51→1.76、investor_activity 0.16→2.36），cov>0.8 无效（institutions cov0.88 全灭）；门控字段可来自**别的**数据集 |
| 外层算子 | ① 内核**限幅**（概率/打分）⇒ `group_rank`（group_zscore 会摧毁分布形状：earningscall S 1.71→0.59）；② 内核**高度右偏**（计数/金额）⇒ `group_zscore` 可降 prod（macro27 −0.25；investor_activity 截面均匀 ⇒ +0.013 无效） |
| 公式迁移 | macro27 四要素公式**不可跨内核迁移**（搬到 earningscall 4 臂全灭） |
| prod 下降 | 只在**换信息源**时有效；同信息源换实现 0.78–0.84 纹丝不动 |
| 数据层优先 | 逐年零持仓 = 数据层排除，**优先级高于 prod 墙**（macro27 3 年 / investor_activity 6 年） |
| 候选排序 | 必须「平台闸 ∧ prod」同看，**S 最优 ≠ prod 最优** |
| 工程 | preflight 必覆盖批内每条；字段名常带数字后缀；重字段集 ≤4 臂/批；prod 单槽被占时不重复触发 |
