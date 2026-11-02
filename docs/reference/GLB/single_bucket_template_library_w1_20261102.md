# GLB single_bucket_* 模型预测字段族 · 波次 1 模板库（2026-11-02）

## 0. 背景与目标

- **目标**：Goal「锁定 NEWS 点塔，挖 10 个 REGULAR（最好 ATOM）」B 路线缺口还差 2 条。
- **主证据**：历史库存破案发现 leA0X7lA（S **3.41**/F 2.29/2Y 2.72/SUB 1.94，全闸全绿已入篮）的主信号就是
  `single_bucket_20day_return_estimate_ohlcv_img_2`（dl_riskfree_returns 集，GLB/OTHER 塔）。
  这是全库最强单信号骨架，围绕它做**正交变体**补缺口。
- **正交性纪律**：20d 字段（leA0X7lA 本尊）本轮**不碰**，防止与篮内成员 self 超线；只用 5d / 60d 两窗口轴。

## 1. 字段族（dl_riskfree_returns，GLB / MINVOL1M / D1，OTHER 塔）

| 字段 | 含义 | ac | 覆盖 | 本轮角色 |
|---|---|---|---|---|
| `single_bucket_5day_return_estimate_ohlcv_img` | 5 天市场中性收益回归预测 | 3977 | 0.9564 | 窗口轴-快 |
| `single_bucket_20day_return_estimate_ohlcv_img_2` | 20 天无风险市场中性收益预测 | 4055 | 0.9564 | **已收割（leA0X7lA），本轮禁用** |
| `single_bucket_60day_return_estimate_ohlcv_img` | 60 天无风险收益预测 | **513** | 0.9564 | **窗口轴-慢，最冷门，优先** |

全部字段 description 明示 **"must be winsorized before use"** ⇒ 所有几何必须保留压缩/归一化层。

## 2. 10 模板清单（结构互异，标注来源）

结构自由度：**窗口轴（5d/60d）× 截面几何（power 0.5 / power 0.25 / 无 power / winsorize 层）×
分组轴（country / subindustry）× 门控（无=ATOM / assets_total_2 门控=双塔）× 中性化附加层（cap 分桶）**。

| # | 模板 | 结构核心 | 塔位 | 来源 |
|---|---|---|---|---|
| T1 | `signed_power(subtract(group_rank(F60, country), 0.5), 0.5)` | 压缩幂 0.5 + country 组内秩（leA0X7lA 原几何） | ATOM(OTHER) | 平台历史（leA0X7lA S 3.41） |
| T2 | `signed_power(subtract(group_rank(F60, country), 0.5), 0.25)` | 压缩幂 0.25（更扁平、降 CW 风险） | ATOM(OTHER) | 自建（winsorize 注记 + 1YNJVzvJ CW 教训） |
| T3 | `signed_power(subtract(group_rank(F60, subindustry), 0.5), 0.5)` | 分组轴换 subindustry | ATOM(OTHER) | 自建（分组轴自由度） |
| T4 | `trade_when(rank(ts_mean(assets_total_2,22))>0.7, T1core, 0)` | leA0X7lA 门控镜像 + 60d 窗 | 双塔 OTHER+FUNDAMENTAL | 平台历史（leA0X7lA 骨架） |
| T5 | `subtract(group_rank(winsorize(F60, std=4), country), 0.5)` | **原始值先 winsorize** 再秩（字段文档合规顺序） | ATOM(OTHER) | 字段 doc + 论坛（cashflow 帖用 winsorize） |
| T6 | `signed_power(group_neutralize(subtract(group_rank(F60,country),0.5), bucket(rank(cap), range="0,1,0.5")), 0.5)` | cap 二分桶中性化附加层 | ATOM(OTHER) | 论坛「【Alpha灵感】通过surprise预测收益」QQ68782 |
| T7 | `signed_power(subtract(group_rank(F5, country), 0.5), 0.5)` | 5d 快窗口 + 原几何 | ATOM(OTHER) | 平台历史（骨架移植） |
| T8 | `signed_power(subtract(group_rank(F5, country), 0.5), 0.25)` | 5d + 扁平压缩 | ATOM(OTHER) | 自建 |
| T9 | `signed_power(subtract(group_rank(F5, subindustry), 0.5), 0.5)` | 5d + subindustry 分组 | ATOM(OTHER) | 自建 |
| T10 | `trade_when(rank(ts_mean(assets_total_2,22))>0.7, T7core, 0)` | leA0X7lA 门控镜像 + 5d 窗 | 双塔 OTHER+FUNDAMENTAL | 平台历史（骨架移植） |

`F5=single_bucket_5day_return_estimate_ohlcv_img`，`F60=single_bucket_60day_return_estimate_ohlcv_img`。

**派发隔离**（batch-kill 防护）：T1-T4、T7-T10 共 8 条只用已实证语法算子 → multisim 一批发；
T5（winsorize 带命名参 std）与 T6（bucket 带命名参 range + group_neutralize）语法风险独立 →
各单发 create_simulation，坏一条不连坐整批。

## 3. 设置档（镜像 leA0X7lA 精确 settings）

GLB / MINVOL1M / D1 / **neutralization=FAST** / decay 10 / truncation 0.08 /
pasteurization ON / unitHandling VERIFY / nanHandling OFF / maxTrade OFF / maxPosition OFF /
FASTEXPR / FULL / IS 2014-01-01~2023-12-31。

## 4. 模板来源汇总（≥10 互异纪律核对）

- 平台历史实证：T1/T4/T7/T10（leA0X7lA 骨架及其窗口移植）
- 字段文档（winsorize 注记）：T2/T5
- 论坛：T5（winsorize 用法，cashflow 帖）、T6（cap 分桶中性化，surprise 帖）
- 自建结构轴：T3/T8/T9（分组轴、压缩幂轴）
- 外部论文检索：web_search 402 余额用尽（待充值），本轮缺位；论坛检索已补。

## 5. 收批归因（2026-11-02 收批定局）

### 5.1 平台指标（multisim `1ftMJFHb5fjcp5PxRDdA2D` 8/8 + 单发 T5 `QPvV1RVG`；全部 `failed_ra_count=0`、`checks.fail=[]`）

| 模板 | alpha_id | S | F | 2Y | SUB | TO | 塔位 | 结论 |
|---|---|---|---|---|---|---|---|---|
| T1 60d p0.5 country | 78L17k35 | 3.69 | 2.68 | 4.32 | 2.85 | 12.9% | ATOM OTHER | RA 全过，**self 挂 A1NQ57NW 0.7336** |
| T2 60d p0.25 country | rKRlp1Nj | 3.66 | 2.54 | 4.25 | 2.80 | 13.3% | ATOM OTHER | RA 全过，self 挂 0.7334 |
| T3 60d p0.5 subind | wpQlK8Gp | 3.79 | 2.67 | 4.25 | 3.00 | 12.9% | ATOM OTHER | RA 全过，self 挂 0.7180 |
| T4 60d+门控 | 9qxrZzMr | 2.85 | 1.81 | 2.28 | 1.55 | 14.0% | OTHER+FUND | RA 全过，**互相关撞篮内 leA0X7lA 0.9754** |
| T5 winsorize 层 | QPvV1RVG | 3.74 | 2.85 | 4.42 | 2.90 | 12.9% | ATOM OTHER | RA 全过，self 挂 0.7309 |
| T7 5d p0.5 country | WjOG1Ezo | 4.53 | 3.49 | 5.11 | 3.40 | 13.8% | ATOM OTHER | RA 全过，self 挂 0.7303 |
| T8 5d p0.25 country | bl6qGYnZ | 4.50 | 3.31 | 5.02 | 3.37 | 14.3% | ATOM OTHER | RA 全过，self 挂 0.7292 |
| T9 5d p0.5 subind | xArkOKWn | **4.61** | 3.44 | **5.17** | **3.62** | 13.8% | ATOM OTHER | RA 全过，self 挂 **0.7106**（全族最近） |
| T10 5d+门控 | 9qxrZzmd | 3.42 | 2.27 | 2.86 | 1.83 | 14.9% | OTHER+FUND | RA 全过，互相关撞 leA0X7lA 0.9779 |

T6（cap 分桶中性化）单发 `3yFBZhdfO5819vjZTL7BbmM` 在途。

### 5.2 互相关结构（精确解 `max_subset_exact=true`，1023 点）

- **无门控簇**（T1/T2/T3/T5/T7/T8/T9）内部 0.91–0.999，一团；
- **门控簇**（T4/T10/leA0X7lA）内部 0.93–0.98，另一团；
- **两簇之间仅 0.38–0.45** ⇒ 门控是真正的正交轴。
- 席位账：leA0X7lA 已占门控簇 1 席；无门控簇只能出 1 席。

### 5.3 self 闸全灭的破案结论

**无门控簇 7/7 全部被 OS 池单条 alpha `A1NQ57NW` 卡死**（0.7106–0.7336，超 0.7 线仅 0.01–0.03）：
`A1NQ57NW` =「GLB_S_10comp_NQ57NW」（2026-09-24 提交，S 4.26，decay 10/trunc 0.08 同档，10 组合件）。
次要相关源 e75pvoNz / LLMWkXp6 / MPabNeNz / VkaXbmbG 均 <0.68，不构成障碍。

**规律**：① subindustry 分组比 country 贴线更近（0.7106/0.7180 vs 0.7292–0.7336）；
② p=0.25 压缩反而更差；③ 5d/60d 窗口差异对 self 几乎无影响（同簇 0.92+）。

### 5.4 覆盖

xArkOKWn / WjOG1Ezo 逐年 2014–2023 `longCount>0 && pnl>0`，**零空窗**（覆盖闸过）。

### 5.5 修复探针波（D 系，每条只动一个自由度，目标：对 A1NQ57NW 跌破 0.7）

| 探针 | 表达式锚点 | 动的自由度 | sim |
|---|---|---|---|
| D1_smooth5 | xArkOKWn + `ts_mean(x,5)` 平滑层 | 信号时序平滑 | `2YnxRobWJ4kyaSGzRMfi0Ax` → `xArkn7Wg`：RA 全过（S 3.99/F 2.84/2Y 4.36，TO 降到 10.3%）但 **self 仍 0.7145**（对 A1NQ57NW，与基线 0.7106 相比几乎没动）⇒ **平滑杠杆破不了内容驱动的 self 墙**，出局 |
| D2_decay15 | wpQlK8Gp @ decay 15 | 设置档 decay 轴 | `2kLGecbgp5ay8Y7pk5sdA31` → `d5W0xEnx`：RA 全过（S 3.62/F 2.56/2Y 4.13，TO 10.6%）但 **self 0.7265**（对 A1NQ57NW）⇒ decay 轴无效，出局 |
| D3_decaylin22 | wpQlK8Gp + `ts_decay_linear(x,22)` | 慢平滑层 | **取消**——D1（平滑 0.7145）/ D2（decay 0.7265）/ T6（cap 中性化 0.7331）已证无门控几何杠杆全部落在 0.71–0.735 带内不动，预判死，不烧队列 |
| D4_sector | WjOG1Ezo 换 sector 分组 | 分组轴 | **取消**（同上；分组轴在 5.3 已证 subindustry 0.7106 / country 0.7336 同带） |

**T6（原模板，无门控）补充收批**：`3yFBZhdfO5819vjZTL7BbmM` → `e750kzkE`，RA 全过（S 3.76/F 2.72/2Y 4.39，TO 12.9%，pyramids=PV/OTHER 双塔），但 **self 0.7331**（对 A1NQ57NW）⇒ 无门控簇第 9 个证例。

**D 波终判（2026-11-02 19:50 定局）**：无门控 single_bucket 族 9/9 全部卡死在 A1NQ57NW 的 0.7106–0.7336 带内，
平滑（D1）、decay（D2）、cap 分桶中性化（T6）、分组轴、压缩幂、窗口轴无一能破 ⇒ **内容驱动 self 墙，只有 PnL 路径杠杆（门控/信号源）可破**。

### 5.6 plan-C：门控路径轴（E 系，D 波全灭时启用）

**依据（19:34 实测确认）**：门控簇 self 双双过线——T4 `9qxrZzMr` max **0.5105**、T10 `9qxrZzmd` max **0.5284**
（A1NQ57NW 仅 0.42）⇒ 门控轨道天然绕开 A1NQ57NW；其唯一死因是与篮内 leA0X7lA 互相关 0.975+。
**门控稀疏路径主导 PnL**（T4/T10 信号窗 60d/5d 互异仍 0.9299）⇒ 只改门控路径就能与 leA0X7lA 脱钩。锚点 T10（9qxrZzmd）。

| 探针 | 表达式改动 | 动的自由度 | sim |
|---|---|---|---|
| E1 | `trade_when(rank(ts_mean(assets_total_2,22)) > **0.5**, T10core, 0)` | 门控阈值轴 | `1V0PekfPx53XaTcYgun6t9E` → `kqN03AZd`（19:52 收批）：**RA 全过 S 4.14/F 2.85/2Y 3.60/TO 14.4%**，self **0.588 ✓**（A1NQ57NW 仅 0.538），但 vs leA0X7lA 互相关 **0.7835 ✗**（从 0.978 压下来但未过 0.7 线）⇒ 阈值轴部分脱钩，暂不可入篮 |
| E2 | `trade_when(rank(ts_mean(assets_total_2, **60**)) > 0.7, T10core, 0)` | 门控窗平滑轴 | `28A4AIga54Wa9kNKMNoB3oA` → `npv225jl`（19:54 收批）：RA 全过 S 3.31/F 2.17/2Y 2.61，self **0.543 ✓**，但 vs leA0X7lA **0.9481 ✗**、vs E1 0.82 ⇒ 门控窗轴对脱钩几乎无效，判死 |
| E3 | `trade_when(rank(ts_mean(**ern3_pre_reptime**, 22)) > 0.7, T10core, 0)` | **换门控字段**（EARNINGS 财报时间戳；w169 fRA=0、三区域均衡） | `2FXYqpf1h4vrctS172h1D8iF`（19:45 派发） |

判定口径：门控簇 self 已知过线（对 A1NQ57NW ~0.42–0.53），E 系的生死线是 **与 leA0X7lA 互相关 < 0.7**
（+ 篮内 8 条互相关全 <0.7）。E3 是 PnL 路径第一杠杆（换门控字段），E1/E2 只动参数轴——预期 E3 脱钩幅度最大。
