# 塔点亮表更正 + risk59 突破 · 2026-11-07

## 一、★ 塔点亮表更正（此前台账有误）

用 MCP `get_user_alphas(stage=OS, region=KOR, type=REGULAR)` 拉全量已提交清单：**35 颗**，塔分布：

| 塔 | 已提交数 | 是否点亮(≥3) |
|---|---:|---|
| MODEL | 7 | ✦ 已亮 |
| SHORTINTEREST | 7 | ✦ 已亮 |
| FUNDAMENTAL | 6 | ✦ 已亮 |
| **PV** | **5** | **✦ 已亮（此前误记为 2）** |
| ANALYST | 4 | ✦ 已亮 |
| OTHER | 4 | ✦ 已亮 |
| RISK | 1 | 未亮 |
| INSIDERS | 1 | 未亮 |
| earnings / institutions / imbalance / macro / news / sentiment / socialmedia | 0 | 未亮 |

**影响**：pv103（14:30–14:30 session OHLCV，cov 1.0，aC 16–49）原定为 P11，
因 PV 实为已点亮塔，**按「已点亮塔不选」规则撤下**。同理 pv20/pv47/pv14/pv13 全部不可选。

## 二、未点亮塔可挖池已基本见底（逐集实测）

| 数据集 | 塔 | 字段/覆盖 | 实测结论 |
|---|---|---|---|
| news50 | news | 71 VECTOR / 0.65 | S 0.20–0.40 ✗ 封盘 |
| news38 | news | 36 VECTOR / 0.89 | S 0.04–0.25 ✗ 封盘 |
| news_sentiment_transfer | sentiment | 23 MATRIX / **0.9654** | S 0.04–0.09 ✗ 封盘 |
| institutions6 | institutions | 11 计数 / 1.0 | S 0.56–0.63 ✗ 封盘（含论坛冠军移植失败） |
| insiders1 | insiders | 9 VECTOR / **0.3526** | 覆盖过低，弃 |
| imbalance5 | imbalance | **1 字段**（imb5_mktcap） | 仅市值，非信号，弃 |
| sentiment23 | sentiment | 2 字段 / 0.285 | 覆盖过低，弃 |
| sentiment21 | sentiment | 137 字段 / 0.35–0.47 | 覆盖过低，弃 |
| socialmedia39 / other100 | socialmedia | 各 1 字段 | 结构过薄，弃 |
| macro63 | macro | 1 字段 | 结构过薄，弃 |
| earnings3 | earnings | 8 个日历字段 / 0.56–0.78 | 待测（仅有日程时点，非意外） |
| **risk59** | **risk** | **16 VECTOR / 0.9806** | **✅ 有活口** |
| risk68 | risk | 3 MATRIX / 1.0 | 在飞 P10 |
| risk60 | risk | 5 VECTOR / 1.0 | 待派（拥挤 + 借券费率） |

## 三、★ risk59 活口（本轮最强）

| alpha | 表达式 | S | F | 2Y | **sub** | TO | raFail |
|---|---|---:|---:|---:|---:|---:|---:|
| **9qxMnXg1** | **group_rank(vec_avg(rsk59_daystocover90day), sector)** | **1.02** | 0.82 | 1.28 | **0.98** | 0.0864 | 3 |
| A1VzAdYX | −group_rank(vec_avg(rsk59_short_interest), sector) | −0.97 | −0.69 | −1.21 | −0.94 | 0.0682 | 5 |
| zq3GVzQ8 | −group_rank(vec_avg(rsk59_shortinterestpct), sector) | −0.53 | −0.28 | −1.15 | −0.51 | 0.0709 | 5 |
| leAGmjJ8 | −group_rank(vec_avg(rsk59_s3utilization), sector) | −0.49 | −0.24 | −0.79 | −0.23 | 0.0715 | 4 |

### 两个关键读数
1. **符号整体反转**：经典「高空头 → 跑输」异象在 KOR **反向**。空头仓位越高 → 后续**跑赢**（轧空/逆向）。
   翻正后 short_interest 臂 S +0.97 / 2Y +1.21，shortinterestpct 臂 S +0.53 / 2Y +1.15。
2. **daystocover90day 是独立强腿**：正号 S **1.02**，且 **sub 0.98**（全战役最高）。
   sub 闸要求 sub ≥ 0.474×S；若 S 推到 1.58，需 sub ≥ 0.75，当前 0.98 有 30% 冗余 —— 这是罕见的「sub 不拖后腿」的腿。
   TO 仅 0.0864，RA 的换手闸天然安全。
   经济含义：回补天数 = 空头持仓 / 日均成交量，高 dtc = 平仓需时久 = 轧空燃料。

### 精修方向（P13，已 preflight 通过，待派）
围绕 dtc 的 10 个结构变体：月度/季度平滑（ts_mean 22/66）、年化分位（ts_zscore 250）、
dtc × squeeze_risk 交集、双期限乘积（qMLOooX1 几何）、换轴 subindustry + ts_decay_linear、
dtc × shortinterestpct、短窗 dtc(10day)，外加 short_interest 与 squeeze_risk 正号基线。
目标：从 S 1.02 推到 1.58。

## 四、结构性判断（供决策）
未点亮塔 12 个候选数据集已逐集实测，**只剩 risk 族 3 个数据集有信号**（risk59 活口、risk68 在飞、risk60 待派）。
即使 risk 族各出 1–2 颗，本轮最多再收 2–4 颗 ⇒ 交付上限约 **5–7/10**，除非放宽「已点亮塔不选」。
已点亮塔的可挖性显著更高：PV(5) 有 pv103 这种 cov 1.0 的 session 微结构数据，SHORTINTEREST(7) 与 risk59 同源。
