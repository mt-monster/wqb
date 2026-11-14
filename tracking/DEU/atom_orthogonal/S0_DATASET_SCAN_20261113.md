# DEU S0 数据集扫描与候选选定（2026-11-13）

> 任务：20 颗 regular alpha（优先 ATOM）。**继承既有战役：17 颗已入篮（互相关<0.7），缺口 3 颗**。
> 已点亮塔（类别级，塔按数据集计数）：analyst 6 / model 3 / shortinterest 4 颗 ⇒ **已点亮的数据集不再选**；
> 但 analyst/model/shortinterest 类别内的**未点亮数据集**仍可选（点塔按数据集计，每集 3 因子点亮一塔）。

## 一、平台扫描总况（DEU/TOP500/D1，MCP get_datasets）

共 ~170 个数据集。按塔位 × 死路档案 × 覆盖率 × 倆篮相关性筛选。

## 二、排除清单（含理由）

| 排除对象 | 理由 |
|---|---|
| 已点亮数据集（predictive_starmine / analyst7 核心族 / shortinterest3 / model264 等） | 用户指令：已点亮塔的数据集不纳入 |
| RISK 塔（risk60/68/71/72/88） | 六维闸判死（2026-11-12 五集全探，max 1.45 且 2Y 0.83） |
| SENTIMENT 塔（sentiment7/27/33） | 数据跨度 5-6 年 + 20 臂天花板 0.93（六维闸合规死） |
| INSTITUTIONS 塔（institutions1/4/6/25 / fund_holdings_panel） | 20-22 臂/集判死证书（max 0.79-0.93；cov 1.0 也死：季度低频已定价） |
| INSIDERS 塔双集交互 | 82 臂天花板 1.38（S 差 0.20 无杠杆） |
| EARNINGS 塔 | EAT 原配方算子 inaccessible + PEAD 反转 + 覆盖不足，关闭 |
| SOCIALMEDIA（socialmedia12/39） | 天花板 0.73（AU2 10 模板） |
| PEAD 正向 / rec 评级族 / est_q 族 / net-gps-nav-ent-opr-grm-roa 主轴 | 2026-11-12 尾段判死（BE214-220） |
| fnd6 基本面主面（ROE/ROA/净利率） | TO 2% 更新过慢，0.37 |
| news81/analyst7/news38/news48 cov0（旧判死，10-31 论坛取证） | TOP500 零覆盖 —— ⚠ news38/48/81 需平台重核 cov（DEU coverage 字段平台侧有 0.5992 等） |
| pattern_scores / continuation_score | 形态相似度无横截面 alpha（10 模板 0.23 / 11 模板 0.52） |
| insider_agg_matrix / insider_trx_matrix / insider_matrix 主体机制面 | 20 臂判死证书（0.86/0.66 上限） |
| pv106 / pv109 / intraday_pv_feats / pv20 流动性族 | 2Y-ceiling / 空字段 / TO 爆 / S1.29 族关 |

## 三、候选数据集（按优先级）

**选定理由框架**：未点亮塔 + 非死路 + 覆盖率真实 + 与既有 17 颗篮的机制正交性（新塔 = 新席位相关约束少）。

| # | 数据集 | 塔位 | cov | 字段 | 机制先验 | 选定理由 |
|---|---|---|---:|---:|---|---|
| **1** | **news17**（PR Edition） | NEWS(0/未点亮) | 0.791 | 48 | PR 线缆分级情绪+事件 | DEU 侧曾出 segment_verdict_psvalB_news17；news 塔判死已撤回；48 字段中 sentiment×relevance 交互、novelty、volume 族未系统测 |
| **2** | **news18**（Ravenpack） | NEWS | 0.805 | 70 | 结构化事件情绪（波 AU 撤判重开首选，cov0.979 报告口径 vs 平台 0.805） | 判死审计明列「从未探针、BA2 首选」；70 字段富矿 |
| **3** | **model238**（SmartHoldings） | MODEL(3/已点亮但此集0) | 0.855 | 22 | 机构持仓预测变化（vs 现持仓） | ledger 有 mdl238_r1/r2_templates 历史；predictive 机制与分析师修正正交 |
| **4** | **model36**（SmartRatios） | MODEL | 0.849 | 20 | 智能比率估值 | 波 80 probe 历史有读数未穷尽；value/growth 维度与篮内 momentum 修正族正交 |
| **5** | **news50**（Web News Analytics） | NEWS | 0.764 | 37 | 网络新闻情绪+热度 | 判死审计撤回对象（从未探针） |
| **6** | **analyst83**（Smart Conference call） | ANALYST(6/已点亮但此集0) | 0.339 | 345 | 电话会结构化情绪/事件 | 判死审计 ❌撤判对象（零探针）；345 字段富矿（低cov字段选族内高cov代表） |
| **7** | **model106**（Analysts rating model） | MODEL | 0.788 | 14 | 评级模型输出 | 未系统测过（ledger 无死档）；14 字段可全字段画像 |
| **8** | **model28**（Structural Credit Risk） | MODEL | 0.811 | 25 | 结构化信用风险（Merton） | 波 79-82 三波历史（formula/drift/probe），字段族未穷尽 |
| **9** | **news29/news54**（Significant/Key Developments） | NEWS | 0/0 | 16/39 | 事件显著性/主题 | 10-09 wave1 有历史但未穷尽；事件稀疏需 backfill |
| **10** | **fundamental45**（Systematic mining of earnings calls） | FUNDAMENTAL(1/未点亮) | 0.269 | 12 | 电话会系统性情绪 | 历史波 BE61 出现过（fnd45 X3 × news），未穷尽 |

**优先序**：news17 → news18 → model238 → model36 → news50。
首攻 **news17 + news18**（同塔双集，DEU/NEWS 0 颗的最干净新塔面——与既有篮（ANALYST 修正+SHORTINTEREST+MODEL+INSIDERS+OTHER/PV 组合）机制正交）。
判死审计明确：news 塔「终判死」已撤回，news18 为 BA2 首选、cov 0.979（70 字段最大富矿）。
次攻 model238/36（MODEL 塔内未点亮数据集，predictive_starmine 已点亮被排除，这两集零历史死档）。

## 四、既有交付篮（17 颗，新件须与全对 <0.7）

```
d5apW38x(2.36) 2r50PAzJ(1.83) WjlMlWJd(2.21) leadEXnl(2.20) RREPm361(2.02)
zq3eb7No(2.01) rKRx2Alj(1.95) 9qlz29Oe(1.86) npa9PKWw(1.74) qM7KxkQV(1.72)
78Yk8VR1(1.68) Jj8VQwoe(1.65) mLapKbd2(1.64) GrW9OxmG(1.62) bl6AvMkN(1.61)
d5a2vxzY(1.60) Jj8w52Me(1.67)
```
（另 2 颗高相关排除：6XM87Zb7 vs zq3eb7No 0.7768；VkN9waPY vs 2r50PAzJ 0.8324；0mPqGEgq vs d5apW38x 0.7249）

## 五、验证杠杆（来自前轮沉淀）

- **杠杆 A**：`group_neutralize(·, subindustry)` 双层中性化破 2Y（group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)）
- **杠杆 B**：反转 × 应计质量乘法交互（multiply 形态，加性崩）
- 探针读数三分法：S≥1.58 全验证 / S 1.0-1.58 升级窗轴算子 / S<0.5 判死族免测
- 事件型字段 nan ON + ts_backfill 转面板（MI 教训）；MATRIX 裸用不 vec_ 包
- 取反衰减指纹：<0.10 对称线性 / >0.40 单向事件（后者不可对称放大）
- 每臂算子 ≤12；比例分母 add(...,0.0001) 防 0；单 multisim ≤10 条
