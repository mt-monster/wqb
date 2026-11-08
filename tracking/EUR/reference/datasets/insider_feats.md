# insider_feats · EUR / TOPCS1600 / D1 字段画像

> 类型 **MATRIX（118 字段,免 vec 归约）** · cov **0.9157（filled 族）/ 0.16-0.82（raw 族）** · category = **other**（×1.5,未点亮塔）
> 采集：2026-11-08 · αC 58（低竞争）· 论坛帖 `43615381230875` 标注「全球成交特征,价值分 6,insiders 类里滤不见」
> 论坛帖 `43152032301591`（FF56620）提示：跨市场 insider 机制备用集

## 0. 字段结构（×3 身份层级 × 多窗口 × 金额/笔数/成交量三维）

| 维度 | 取值 |
|---|---|
| 身份层级 | `all`（全体）/ `top20`（前 20 高管）/ `top5`（前 5 核心） |
| 读数 | `buy_sell_ratio`（金额比）/ `buy_sell_tx_count_ratio`（笔数比）/ `buy_to_sell_volume_ratio`（股数比）/ 纯计数 |
| 窗口 | 5/10/20/60/250d |
| 变体 | `_filled`（缺失回填,cov 0.9157）/ raw（cov 0.16-0.82）/ `_2`（备用算法） |

**关键结构判断**：`buy_sell_ratio_*_filled` 族是**厂商已做好的买卖比读数**（JMZ 买卖不对称的直接实现）,且 coverage 0.9157 远高于 raw 族——**本集主攻 filled 比例族**,raw 族只作对照。这是与 insider_agg_matrix（绝对金额）/insiders1（自算比例）完全不同的**厂商预计算比例**——若与自算比例机制互相关 <0.9,即独立席位。

## 1. 五问

| # | 问 | 答 |
|---|---|---|
| 1 | 时间 | 滚动窗口比例,**存量态**（非事件流）——直接 rank/zscore,无需 ts_sum |
| 2 | 相对性 | 比例天然标准化;短窗比例噪声大（5d）,60d/250d 是主窗口 |
| 3 | 被定价谁 | 买/卖比=净信念;top5/top20 层级=协同度 |
| 4 | 拥挤 | αC 58 低竞争 |
| 5 | 事件 | 日更连续 MATRIX——禁 trade_when,常规截面栈即可 |

## 2. 第一批探针（6 臂,吃满战役已验证栈）

1. `buy_sell_ratio_all_60d_filled` 88d 栈（主读数,与席位 1 同构对照）
2. `buy_sell_ratio_top20_60d_filled` 88d 栈（高管协同）
3. `buy_sell_ratio_all_250d_filled` 88d 栈（长窗信念态）
4. `buy_sell_ratio_top5_60d_filled` 88d 栈（核心层）
5. `ts_rank(buy_sell_ratio_all_60d_filled, 252)` 自身基线（存量态适用——insiders 类未在存量字段上测过时序基线）
6. reverse 对照（卖压方向）

栈：`rank(group_scale(tail(winsorize(group_zscore(ts_sum(F, 88), industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))` @ SLOW_AND_FAST/decay4/TOPCS1600

## 3. 实测

（待回填）

## 3. 实测

### 3.1 第一批（multisim `1GGYLDeAt52JcL3QXI0Its5`,88d 栈）——协同梯度复现

| 字段 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| all_60d | `MPYzwvMa` | 1.04 | 0.41 | 1.30 | 0.32 FAIL | 0.33 FAIL |
| **top20_60d** | `akKzJmj9` | 1.39 | 0.64 | 1.61 | 0.93 PASS | 0.59 FAIL |
| all_250d | `d5WzqJpX` | 0.43 | 0.11 | 1.25 | 0.30 | 0.06 |
| top5_60d | `9qxMo5Yo` | 1.39 | 0.64 | 1.77 | 0.87 | 0.58 |

**归因**：① 协同梯度复现（top20/top5 ≫ all,与 agg_matrix 高管主导一致）;② 250d 长窗信念态无信号——**比例读数的半衰期在 60d 窗口,250d 已是常态而非异常**;③ sub 大幅 PASS 但 robust 0.58-0.59 卡。

### 3.2 ★ 存量直读突破 + prod 卡墙（multisim `3UTqxAcpC4l3acUbWZ64BmJ`）

| 变体 | alpha id | S | F | 2Y | sub | robust | prod |
|---|---|---|---|---|---|---|---|
| **直读（免 ts_sum）** | **`LLMzOe3M`** | **1.76** | **0.94** | **2.53** | **1.12** | **1.09** | **0.7955 FAIL** |
| ts_sum 88d + std4 | `QPvzme6g` | 1.43 | 0.67 | 1.65 | 0.92 | 0.53 | — |

**归因**：① **存量态字段直读（免 ts_sum）是本集正确形态**——ts_sum 二次平滑反而稀释（1.76→1.43）;与事件流字段（agg_matrix 必须 ts_sum）形成「存量直读/流量累加」二分法。② Mode B main_gate PASS（S 1.76/F 0.94）、self 0.199、与四席互相关全 <0.9——**但 prod 0.7955 卡墙**（0.7-0.8 桶 n=2）。

### 3.3 破墙进行中（multisims `4rKEXV42853qbBAxe3tS8Id`/`40Nj8yenj4v08YeoAp5Qkan`）

| 变体 | alpha id | S | 2Y | prod |
|---|---|---|---|---|
| ts_sum 20d 短平滑 | `P0ozjR5q` | 1.53 | 1.81 | **0.7535 FAIL**（仍 n=1） |
| top20_20d_filled_2 直读 | `leAGJnal` | 0.72 | 1.20 | — |

⚠ 工程坑：`buy_sell_ratio_top20_20d_filled` 不存在（只有 `_2` 后缀版）——**连坐 CANCELLED 一次**,重发修正。20d 直读读数噪声大（0.72）。破墙未果,下一杠杆：换身份层级（top5）/换分组轴（country）改持仓结构。

### 3.4 prod 墙归因（2026-11-08）——insider_feats 直读族三连卡

| 变体 | alpha id | S | F | 2Y | sub | robust | prod | 直方图尾 |
|---|---|---|---|---|---|---|---|---|
| top20 industry 直读 | `LLMzOe3M` | 1.76 | 0.94 | 2.53 | 1.12 | 1.09 | 0.7955 FAIL | 0.7-0.8 n=2 |
| **top20 country 直读** | `WjOzwnlO` | **1.80** | **0.96** | 2.17 | 1.27 | 1.00 | **0.8409 FAIL** | 0.7-0.8 n=1 + 0.8-0.9 n=1 |
| top5 industry 直读 | `Xg9zwPax` | 1.52 | 0.76 | 2.09 | 0.97 | 0.86 | 0.7386 FAIL | 0.7-0.8 n=1 |

**归因**：① 三臂全部卡 prod 墙且 0.7-0.8 桶都有钉子（n=1-2）——**钉子随杠杆移动**（industry 0.796→country 0.841→top5 0.739）,说明墙不是单一 alpha 而是该机制（insider 买卖比）在 prod 池里的**同类已有 alpha**——大概率是已提交的内部人比例类 alpha（RRAvGrn0,self 池里与席位 1 相关 0.33 的那颗或同类）。② 结构读数全部优秀（sub 0.97-1.27/robust 0.86-1.09）,Mode B 全 main_gate 级——**机制真实、墙是机制级的**。③ country 轴抬 S（1.76→1.80）但也抬 prod（0.796→0.841）——与 prod 池中同类 alpha 的国家中性化差异反而加相关。**破墙路径只剩持仓结构改造**（半仓/条件门控把持仓与钉子错开）——成本高、成功率低,标记为「prod 机制级墙」,insider_feats 归档为**备用库**（结构最优但 prod 被 insider 机制既有持仓占用）。若席位 1 提交后该墙变化（prod 池漂移）,先回来重测 `LLMzOe3M`。
