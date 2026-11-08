# 全区域 READY 池普查 —— 本战役最高 ROI 动作（2026-11-06）

## 0. 一句话结论

`get_submit_ready(region=...)` 一次调用即可拿到该区**全部** IS 全闸通过且未提交的件，且返回体**自带 `self` / `prod` 列**（有值即零成本判定）。
此前只在 USA / GLB / IND / KOR / HKG 做过，**EUR(48) / GBR(31) / DEU(11) 三个大池从未普查** ⇒ 一轮下来净增 **+5 颗**候选（EUR +4、DEU +1）。

## 1. 全区域 READY 池规模实读

| 区域 | READY 条数 | 已处理净产出 | 备注 |
|---|---:|---:|---|
| **EUR** | **48** | **+4 新增**（池内 8 颗全绿） | 本次普查 |
| **GBR** | **31** | 5 已入库 + 2 待 prod | 本次普查，pv47/analyst47 族已判死 |
| IND | 57 | 16 | 早前普查 |
| GLB | 21 | 1 | 早前普查，6 项 prod 全灭 |
| USA | 13 | 3 | 早前普查，情绪族判死 |
| **DEU** | **11** | **+1 新增** | 本次普查，5 族中 4 族 self 卡死 |
| ASI | 1 | 0 | `0mXexOw6` self 0.7202 超线 |
| KOR | 1 | 1 | `LLZ6wZO2` |
| HKG / JPN / TWN / AMR / MEA / CHN | 0 | — | 空池 |

★ 方法论：**READY 池普查的产出/成本比远高于「开数据集面从零挖」**。一个区 40+ 条 READY 里通常有 3–5 颗 self/prod 双绿，而开一个新数据集面平均要 2–4 批仿真（40–80 分钟队列）才可能出 1 颗且大多判死。
⇒ 每轮开波前先跑一遍全区域 `get_submit_ready`，再决定把仿真额度投到哪个面。

## 2. EUR：4 → 8 颗（净增 4）

### 2.1 新增四颗（全部 self/prod 双绿）

| alpha | S | F | TO | 2Y | self | prod | SRC | 族 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `6XAe27eL` | 1.74 | 1.10 | 4.17% | 1.62 | **0.447** | **0.4857** | analyst7 | trade_when_abs |
| `Grge2lN3` | 1.79 | 1.15 | 4.42% | 2.02 | **0.5386** | **0.5893** | analyst7 | trade_when_abs |
| `rKd5lAo8` | 1.64 | 1.14 | 6.85% | 1.78 | **0.5054** | **0.6747** | fundamental72 | ts_target_tvr_decay |
| `ZYAJZL93` | 1.67 | 1.04 | 10.47% | 1.81 | **0.2278** | **0.6617** | analyst_factor_signals | ts_target_* |

### 2.2 EUR 全 9 颗互相关矩阵实算

只有 **1 对** 超 0.7：

| 对 | 相关 |
|---|---:|
| `A1QZYa1l` × `XgRQLpWX` | **0.8997** |

`max_mutually_below_subset_size = 8` ⇒ {A1QZYa1l, ZYQmolVx, xArjE96W, P0g88dzW, ZYAJZL93, 6XAe27eL, Grge2lN3, rKd5lAo8} 互相关**全部 < 0.7**。

**处置**：`XgRQLpWX`（S 1.79 / F **1.45** / TO **3.67%** / 2Y 2.48 / self 0.6209）与 `A1QZYa1l`（S 1.81 / F 1.43 / TO 3.79% / 2Y 2.62）是**同族**（SRC_quant_factor_lib），指标几乎一致 ⇒ 留 `A1QZYa1l`，**`XgRQLpWX` 弃用**（同时省掉一次 prod 取值）。

### 2.3 EUR 池被 self 判死的件（不可复用）

| alpha | S | F | self | 判定 |
|---|---:|---:|---:|---|
| `wp9m9MW1` | 2.14 | 1.10 | **0.9990** | 完全镜像，判死 |
| `A1Q729Ll` | **2.23** | **1.60** | **0.9342** | 可惜：全池最强且 prod 0.6288 已过，被 self 拦死 |
| `j2eRn9KQ` | 2.14 | 1.63 | **0.8769** | 判死 |
| `WjLqPzpQ` | 2.02 | 1.03 | **0.8372** | 判死 |

★ `A1Q729Ll`（S 2.23 / F 1.60 / TO **5.30%** / 2Y 1.82 / prod **0.6288**）是全池质量最高的一颗，唯一障碍是 self 0.9342。若日后要救，只能动骨架（SRC_analyst7 + group_neutralize_signed），不能动窗口。

### 2.4 EUR 的 TO 陷阱

`pwvYnnOg`(S 3.83) / `qME9nnqP`(S 3.84) / `QPYZ5ePX`(3.49) / `YPxLWdpv`(3.36) 等 **techindi_model 族 S 极高但 TO 48–65%** ⇒ 会撞 HIGH_TURNOVER 闸。EUR 已知 techindi_model 面饱和度也高，不投。

## 3. DEU：11 条 READY → 5 个结构族 → 净增 1 颗

### 3.1 去重后的族结构（关键：11 条不是 11 个 alpha）

| 族 | 条数 | 代表 | 差异点 |
|---|---:|---|---|
| analyst_factor_signals + bucket group_neutralize | **6** | `Vkxnb8QG` | 仅 `bucket range` = 0.02/0.025/0.05/0.1 的**参数变体** |
| institutions1 + tail winsorize | 2 | `E56AzejK` | 仅 group_rank 的分组字段不同 |
| sentiment7 + vector_neut | 1 | `kqNRX1ZP` | S 最高 2.06 |
| shortinterest3 + ts_target_tvr_decay | 1 | `MPY9VNY9` | — |
| predictive_starmine + tail group_neutralize | 1 | `XgJ980Wb` | — |

★ **「READY 条数」严重虚高**：6 条只是 bucket range 的排列。清点候选前必须先按 expr 骨架折叠，再按参数折叠。

### 3.2 五族 self 全量实测 —— 只有一颗活

| alpha | S | F | TO | 2Y | self | prod | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `MPY9VNY9` | 1.59 | 1.26 | **3.64%** | 2.36 | **0.2703** | **0.5986** | ✅ **全绿，入库** |
| `kqNRX1ZP` | 2.06 | 1.86 | 10.99% | 2.37 | 0.7936 | 未测 | ❌ |
| `XgJ980Wb` | 1.60 | 1.26 | 10.00% | — | 0.8027 | 未测 | ❌ |
| `E56AzejK` | 1.71 | 1.36 | 13.28% | **2.79** | 0.9184 | 未测 | ❌ 深钉 |
| `Vkxnb8QG` | 1.83 | 1.64 | 9.06% | 2.09 | 0.9589 | **0.6384**（prod 过） | ❌ self 拦死 |
| `58gGQmlN` | 1.62 | 1.26 | 13.11% | — | 0.9408 | **0.683**（prod 过） | ❌ self 拦死 |

★ 复现了早前记录「DEU READY 11 条里 10 条 self 卡死」。**DEU 池是典型「镜像池」**（self 通过率 1/6 = 17% < 20% 阈值）。
★ 注意 `Vkxnb8QG` / `58gGQmlN`：**prod 已过（0.6384 / 0.683）但 self 深钉** ⇒ 再次印证 `self` 与 `prod` 是两个独立判据，任何一方卡死都不能提交。

### 3.3 DEU 塔位推进

`MPY9VNY9` 属 `SRC_shortinterest3` ⇒ **DEU/SHORTINTEREST 2 → 3 点亮**。DEU 由此获得第一个点亮塔。

## 4. GBR：5 已入库 + 2 待 prod

GBR READY 31 条去重后，`pv47` 与 `analyst47` 两族已判死（互相关 0.72–0.95 / self 0.84–1.00）。剩两个独立族本次补测：

| alpha | S | F | TO | 2Y | self | prod | SRC | 价值 |
|---|---:|---:|---:|---:|---:|---|---|---|
| `A1QW6xpE` | 1.74 | 1.03 | 15.02% | 2.13 | **0.5974** | 待测 | pv1 | 出货即**点亮 GBR/PV（2→3）** |
| `P0gxk2dx` | 1.67 | 1.07 | 16.30% | 1.74 | **0.2706** | 待测 | techindi_model | 独立族 |

已入库 5 颗（全部 self/prod 双绿）：`d51O1kOX`(0.1129/0.6793) `blORMJwm`(0.0623/**0.6950** 余量 0.005) `3qV7Q2dO`(0.3669/0.6596) `RR62bMje`(0.6066/0.6573) `mL68wNOK`(0.4979/0.6608)。

## 5. 普查流程 SOP（可直接复用）

1. `get_submit_ready(region=R)` 全量拉取（不按 S 截断）。
2. 按 `suggested_tags` 里的 `SRC_*` + `EXPRFAM_*` + `skeleton` **折叠成结构族**（同一 `EXPRFAM_*` 且 `skeleton` 前 80 字符相同 = 同族，只留 1 颗代表）。
3. 逐族代表测 `check_self_correlation`（**串行**，避免 429）；self > 0.7 直接剔除该族。
4. 剩者只对**缺 prod** 的取 prod（有值直接读），单并发串行。
5. 全部存活者跑一次 `compute_mutual_correlation` 确认彼此 < 0.7（prod 已过的才有意义）。
6. 落库 + 记塔位推进。

★ 步骤 2 是省额度的关键：EUR 48 条 → 实际独立族约 12 个；DEU 11 条 → 5 族。**不折叠直接逐条测 self，会浪费 3–4 倍调用**。
## 6. GBR 两条独立族 prod 实测 —— 双双判死（2026-11-06 收口）

| alpha | S | F | TO | 2Y | self | **prod 实测** | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `A1QW6xpE` | 1.74 | 1.03 | 15.02% | 2.13 | 0.5974 | **0.7756**（6s 出结果） | ❌ 浅钉，距 0.70 差 0.076 |
| `P0gxk2dx` | 1.67 | 1.07 | 16.30% | 1.74 | 0.2706 | **0.9185**（6s 出结果） | ❌ 深钉 |

★ `A1QW6xpE` 不破墙的理由：0.7756 → 0.70 需位移 **0.076**，而窗口微调 (`ts_rank` W) 的实测杠杆量级只有 0.02–0.05；且它是 `pv1` 面，GBR 的 pv 面已被反复开采（pv47 族早前全灭）。⇒ 直接弃用，不投破墙批次。
★ 至此 GBR 仍为 **5 颗**（`d51O1kOX` `blORMJwm` `3qV7Q2dO` `RR62bMje` `mL68wNOK`），GBR/PV 停留在 2，未点亮。

## 7. 本轮净增量汇总

| 区域 | 之前 | 现在 | 变化 | 来源 |
|---|---:|---:|---|---|
| EUR | 4 | **8** | **+4** | `ZYAJZL93` `6XAe27eL` `Grge2lN3` `rKd5lAo8` |
| DEU | 0 | **1** | **+1** | `MPY9VNY9`（点亮 DEU/SHORTINTEREST 2→3） |
| GBR | 5 | 5 | 0 | 两条独立族 prod 双杀 |
| 其他 | 22 | 22 | 0 | — |
| **合计** | **31** | **36** | **+5** | |

## 8. 本轮判死清单（避免重挖）

| 面 | 内容 | 死因 |
|---|---|---|
| USA OPTION `order_flow_imb` | 6 模板（水平/翻号/双腿差值/OTM/笔数背离/回归残差） | 天花板 \|S\| 0.93，距 1.58 差 0.65；TO 最高 109% |
| USA OTHER `mmp_nlp_sentiment` | MMP1/MMP3（±回填 4 条） | 最强 \|S\| 0.69；TO 8–10% 属健康档，是信号弱而非噪声 |
| DEU READY | 5 族中 4 族 | self 0.7936 / 0.8027 / 0.9184 / 0.9589 / 0.9408 |
| EUR READY | `wp9m9MW1` `A1Q729Ll` `j2eRn9KQ` `WjLqPzpQ` | self 0.9990 / 0.9342 / 0.8769 / 0.8372 |
| GBR READY | `A1QW6xpE` `P0gxk2dx` | prod 0.7756 / 0.9185 |

