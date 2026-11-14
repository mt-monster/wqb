# ★v2 补课波总战报（2026-11-11 上午，8 波）

> 本轮按探针协议 v2（正交网格 + 文献前置 + 覆盖证书 + 校准升级线）执行 8 波、约 51 臂，挖出 4 项可复用机制发现。

## 一、本轮波次与结果

| 波 | 内容 | 最佳读数 | 判定 |
|---|---|---:|---|
| BE48 | institutions1 信念线（ts_mean 版） | 0.35 | 配方错误（见发现④） |
| BE49 | insider_agg 论坛模板移植 10 臂 | 0.76 | 低于 1.0 校准线 |
| BE51 | 新闻×I7 + tail（I7 腿）5 臂 | **-0.31~-0.43 全负** | tail 对 rank 型腿有害 |
| BE50 | institutions1 正确配方 6 臂 | 0.83 | 仍缺三要件 |
| BE56 | pv30 积压 10 臂 | 10/10 CANCELLED | GROUP 字段当数值用 ⇒ 作废 |
| BE57 | institutions1 正交面 6 臂 | 0.49 | 连续权重重造并列块 |
| BE58 | 冠军压缩修正 + 原生簇轴 6 臂 | 0.70 | institutions1 族关闭 |
| BE59 | 新闻线 × pv30 原生簇轴 6 臂 | 1.49 | 簇轴对强线中性 |
| BE60 | fnd6 piq/ibq × 开放族 8 臂 | — | 在飞 |
| BE61 | piq 单窗 tvr + 开放族 6 臂 | — | 在飞 |

## 二、★四项可复用发现（已入记忆）

### 发现①：pv30 全字段是 GROUP 类型 = 现成聚类分组轴
285 字段全部 GROUP，cov=1.0 的有 factor1_group{2,5,10,20,50}_top800_513（factor1_group50 u45/a75 最广）。
⇒ 无需 bucket 桥接即可作 group_rank/group_neutralize 分组参数（pv29 的簇标签是 MATRIX，需桥接——BE46 实证）。
⇒ 但「换轴」只在**信号本身弱**时才可能是救命杠杆；强信号线上（新闻线 1.46→1.42-1.49）纯中性。

### 发现②：tail 不是万能后处理（BE51 五臂全负）
比值型信号（institutions1 信念比值）加 tail 有效（论坛 1.65-1.67 vs 无 tail 1.44）；
**rank 型水平腿加 tail 有害**（新闻×I7 的 I7 腿：1.46 → -0.43）。
机制：事件型并列块在比值信号里是噪声，在水平排序腿里起分散化作用（无申报股≈现金腿）。

### 发现③：连续权重会重造并列块（BE57 全弱）
把二值掩码换成 `multiply(ratio_sum, ts_sum(vec_avg(sig),66))` ⇒ 多数股票乘成 0 ⇒ 巨大并列块 ⇒ 信号毁掉。
正确做法：**`greater(...)` 直接当乘子**（天然 0/1），既省算子又保留掩码语义。

### 发现④：DEU 的 prod 相关性 ≈ 一次 self 检查
prod 直方图几乎全在 [-0.1,0.2]，唯一 [0.9,1] 那条就是自家 alpha；prod_wall_ratio 0.8197 主因是**自锁**。
⇒ **新候选第一道筛必须是「与自家 20 颗 OS 的族级正交性」**（已落 OS_OCCUPANCY_MAP）。

## 三、★历史冠军挖出：d5WwzRMY（institutions1，2026-10-30 波）

| alpha | S | F | 2Y | TO | sub | failed_ra | 死因 |
|---|---|---|---|---|---|---|---|
| d5WwzRMY | **1.73** | 1.40 | 2.64 | 12.85% | **1.20** | **0**（9 项硬闸全 PASS） | self 0.9287 撞自家 2rmGAPqN |
| E56AzejK | 1.71 | 1.36 | 2.79 | 13.28% | 1.17 | 0 | 同上（0.9184） |

配方 = 信念比值 × **交易显著性二值门** + oth455 聚类分组 + winsorize2 + tail(0.25,0.75,0.5)。

**该族双因关闭**：① 槽位被自家 10-09 提交占满；② 原式 20 算子，超 ≤12 硬约束，
任何压缩都改变信号结构（BE57 0.49 / BE58 0.70 两次实测）。

## 四、★OS 占用图谱（v2 第一道筛）

已占：analyst 预估族 9 件、mean_loan_rate_main 3 件、oth455 聚类/关系 3 件、shrt3_bar+tvr_decay 2 件、
institutions1 信念 1 件、insider_agg directional_indicator 1 件、sentiment snl27+snt7 1 件、fnd6 oiadpq 1 件。

**仍开放**：nws20 事件情绪 / insd1_holdings / oth47 流量 / p5_d1 借券 / pv30 簇轴 / option1 / risk / earnings / macro / imbalance / socialmedia / fundamental 除 oiadpq。

## 五、档案索引（本轮新增）

- PV30_GROUP_AXIS_AND_TAIL_LIMITS_20261111.md（发现①②③）
- OS_OCCUPANCY_MAP_20261111.md（发现④ + 占用图谱）
- WAVE_BE51_BE50_TAIL_VERDICT_20261111.md、BE58 判决、WAVE_BE59_CLUSTER_AXIS_NEUTRAL_20261111.md
- CORRECTION_VKXNBQG_IDENTITY_20261111.md（Vkxnb8QG 不是 pv30，是 analyst eps × mean_loan_rate 的 trade_when/bucket 构造）
- waveBE56_BE57_dispatch / waveBE53_BE54_option1_pattern / waveBE52_design_tail_enhanced_basket / pv30_backlog_33_expressions.md