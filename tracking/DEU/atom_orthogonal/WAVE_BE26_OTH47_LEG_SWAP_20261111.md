# BE26：换 oth47 腿解相关，争取第 12 颗（2026-11-11 23:22）

## 一、为什么打这一波

`XgajMpvm`（BE22 臂 1）是全篮子**指标最强**的一颗：

| 项 | 值 |
|---|---|
| S | **1.92** |
| F | **1.52** |
| sub | **1.26** |
| 2Y | **2.70** |
| TO | 0.153 |
| 平台 checks | NONE |

**唯一障碍**：与 Jj8VQwoe 互相关 **0.881**（>0.7）。
两者共用 `oth47_organic_traffic` 这条第二腿：
- Jj8VQwoe = shrt3_bar × oth47_organic_traffic（Δ66 quantile252）
- XgajMpvm = max_loan_rate_p5_d1 × oth47_organic_traffic（Δ66 quantile252）

⇒ **换掉 oth47 的字段**（同数据集其他字段）或**换加工方式**，应能降相关而保留机制。

## 二、oth47 可用字段（cov 0.652 除 rank 0.502）

| 字段 | 经济含义 |
|---|---|
| oth47_organic_traffic | 自然流量月访问（Jj8VQwoe 已用） |
| **oth47_organic_keywords** | 自然搜索关键词数（语义广度） |
| **oth47_organic_cost** | 等效购买这些关键词的成本（流量价值） |
| **paid_search_budget_estimate** | Google 付费搜索月预算（营销投入强度） |
| oth47_rank | SEMrush 排名（值越小越好） |

## 三、BE26 八臂设计（sim 1T2gtcbSQ4OScr54eEoTvY2）

| 臂 | 第二腿 | 相对 XgajMpvm 的变化 |
|---|---|---|
| 1 | organic_keywords Δ66 quantile | 换字段（关键词广度） |
| 2 | organic_cost Δ66 quantile | 换字段（流量价值） |
| 3 | paid_search_budget_estimate Δ66 quantile | 换字段（营销投入） |
| 4 | oth47_rank Δ66（负向） | 换字段 + 换方向 |
| 5 | organic_traffic ts_mean66 | 同字段换加工（平滑 vs quantile） |
| 6 | organic_traffic 水平 zscore252 | 同字段换矩（水平 vs 变化） |
| 7 | keywords + cost 双 oth47 腿 | 同数据集双腿平均 |
| 8 | organic_traffic Δ22 quantile | 同字段换窗口 |

## 四、判定条件

出货需同时满足：
1. 平台 checks.fail 为空；
2. S≥1.58 / F≥1.0 / 2Y≥1.58 / TO≤0.7；
3. self<0.7、prod<0.7；
4. **与现有 11 件互相关 <0.7**（这是本波的核心目标）。

## 五、BE26 结论：换 oth47 字段无法解相关（换腿策略失败）

八臂结果（sim 1T2gtcbSQ4OScr54eEoTvY2）——**五颗全闸**：

| 臂 | 第二腿 | S | F | sub | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---|
| 6 | traffic 水平 zscore252 | **2.04** | **1.77** | **1.45** | **2.81** | 全闸（全战役最强指标） |
| 8 | traffic Δ22 quantile | 1.85 | 1.37 | 1.24 | 2.73 | 全闸 |
| 3 | paid_search_budget | 1.81 | 1.46 | 1.13 | 2.07 | 全闸 |
| 1 | organic_keywords | 1.74 | 1.39 | 1.07 | 2.15 | 全闸 |
| 2 | organic_cost | 1.73 | 1.32 | 0.94 | 2.06 | 全闸 |

**但互相关全部冲突**：

| 候选 | 与 11 件最大 | 对端 | 判定 |
|---|---:|---|---|
| xAvK73Qg | **0.762** | Jj8VQwoe | ❌ |
| MP6jvaXa | **0.785** | Jj8VQwoe | ❌ |
| 0mPbZX9p | **0.780** | Jj8VQwoe | ❌ |
| xAvK739g | **0.778** | Jj8VQwoe | ❌ |
| wpo87ZO2 | **0.719** | Jj8VQwoe | ❌ |

候选之间 0.807-0.886 也高度相关。`max_subset_size` 仍为 **11**。

## 六、★重要认识：相关性来自「数据集组合」而非「字段选择」

| 尝试 | 变化 | 与 Jj8VQwoe 相关 |
|---|---|---:|
| XgajMpvm（原） | traffic Δ66 quantile | 0.881 |
| BE26 臂1 | 换 keywords | 0.778 |
| BE26 臂2 | 换 organic_cost | 0.780 |
| BE26 臂3 | 换 paid_budget | 0.719 |
| BE26 臂5 | traffic 改 ts_mean | — |
| BE26 臂6 | traffic 改水平 zscore | 0.762 |
| BE26 臂8 | traffic 改 Δ22 | 0.785 |

**换字段只把相关从 0.881 降到 0.719-0.785，全部仍在 0.7 之上。**

⇒ **相关性主要由「借券强腿 × oth47 数据集」这个组合决定，不是由具体字段或加工方式决定。**
Jj8VQwoe 已经把这个组合的公共成分占了，任何同组合的变体都在 0.72-0.88 区间。

**方法论修正**：
- 此前我以为「换腿降相关」可行（BE22 成功是因为把 I7 换成了 oth47，是**换数据集**不是换字段）；
- 真正的降相关杠杆是**换数据集**（insd1→oth47 降了 0.885→0.881→0.67 到 qM7kQV），
- **同数据集内换字段只能降 0.05-0.16，不足以跨过 0.7**。

⇒ 想新增第 12 颗，必须换到**尚未被任何交付件占用的数据集**。
而 DEU D1 的可用数据集只有 4 个（shortinterest3 / analyst-anl93 / insiders1 / other47），
其中 insiders1 与 other47 都已作为第二腿被占用，shortinterest3 已充分内部挖掘，
analyst 族 4 颗已占用 ⇒ **第 12 颗在现有数据集面内不可达**。