# USA/D1 近闸候选清单与归因（快照 2026-10-24）

> 数据源：`data/wqb.db` 只读查询（`alphas` 表，`region_id=1`，`soft_deleted=0`）。
> 平台 live 复核点单独标注；未标注者均为库内最近一次入库值。
> 复现脚本：`logs/_tmp_usa_near_gate.py`（分类）+ `logs/_tmp_usa_near_gate2.py`（补 dataset / 家族 prod）；SQL 见附录 A。

---

## 0. 结论先行

1. **近闸池共 61 臂，覆盖 11 个数据集**：50 臂只差一闸、11 臂差两闸。全部为 `UNSUBMITTED`。
2. **缺口高度集中**：以臂计，**FITNESS 31 臂（51%）**、**SUB_UNIVERSE 22 臂（36%）**、2Y 9 臂（15%）、Sharpe 8 臂（13%）、CW/TO 各 1 臂。缺口总数 72 = 50×1 + 11×2。
3. **近闸池里没有一颗"prod 未测且家族未死"的新概念**：
   - 61 臂中直接实测 prod 的仅 7 臂，**全部 ≥ 0.79**；**实测 prod < 0.7 的近闸臂 = 0**。
   - 用"同数据集 / 同字段族已提交或已实测臂"做家族先验，**9/11 个数据集已被证明 prod ≥ 0.79**。
   - 剩 2 个数据集（`insider_matrix` / `insider_trx_matrix`）的 prod 在 **0.55–0.70**，但它们正是**已占提交名额的同一概念**（与在册 basket 4 臂互为孪生体），加不进名额。
4. **唯一 prod 未测的机制（`techindi_model` 的 `tm_*` 回归簇）卡在 FITNESS 墙且已被三波打穿**：F 上界 ≈0.96，`decay` 降 TO 同时降 S、`hump` 把 S 打到 0.49、`ts_target_tvr_decay` 只到 F 0.85。判定：F 前沿封闭，不因"差 0.04"而重开。
5. **⇒ 定向挖掘的唯一出路是"新机制"，不是"近闸调参"。** 首选：`macro27`（US 招聘岗位，MACRO 未点亮塔，live 48 个 VECTOR 字段，aC 中位数 < 30），与全库已证伪的"价格 / 水平 / 模型 / 注意力"族**机制正交**，且符合已复现的过 prod 墙画像（事件驱动、非价格、长归一化、低换手）。

---

## 1. 闸口径（USA / D1）

| 闸 | 判据 | 备注 |
|---|---|---|
| LOW_SHARPE | S ≥ 1.58 | |
| LOW_FITNESS | F ≥ 1.0 | F = S × √(returns / turnover) |
| LOW_TURNOVER / HIGH_TURNOVER | 0.01 ≤ TO ≤ 0.70 | |
| LOW_2Y_SHARPE | 2Y ≥ 1.58 | |
| LOW_SUB_UNIVERSE_SHARPE | SUB ≥ **0.434 × S** | 限值随主 Sharpe 缩放；本清单统一用 **SUB/S 比值**列示 |
| CONCENTRATED_WEIGHT | CW ≤ 0.10 | |
| PROD / SELF | 均 < 0.70 | D0-P 硬线 0.75；本表 prod 为参考 |

**近闸定义**：只差 1–2 闸，且缺口在容差内（S/F/2Y −0.15、SUB −0.12、CW −0.012、TO_hi +0.05、TO_lo −0.002）。

**口径更正（本清单自查）**：分类脚本原按"负向缺口才算失败"计数，把 **`leMKrwox` 的 TO 下限（0.009 < 0.01）** 与 **`E5Vxjr71` 的 CW（0.1055 > 0.10）** 漏计成单闸。二者实为双闸，故正式口径为 **单闸 50 / 双闸 11**（脚本输出 52/9）。

---

## 2. 总览：61 臂按数据集 × 缺口分布

| 数据集 | 塔 | 臂数 | 主缺口 | prod 家族先验 | 判定 |
|---|---|---|---|---|---|
| ds389 intraday_pv_feats | PV | 7 | F（+S） | 0.7864–0.8739（本族实测） | prod 死 |
| ds484 order_book_imbalance | OTHER | 1 | 2Y | 0.8133（本臂） | prod 死 |
| ds317 analyst_consensus | ANALYST | 11 | F / SUB / 2Y | 0.6540（已提交 ACTIVE） | **塔已亮，不投** |
| ds294 ai_equity_alpha | MODEL | 1 | 2Y | 0.5626（已提交 ACTIVE） | **塔已亮，不投** |
| ds585 web_traffic_engage | OTHER | 1 | 2Y | 0.9740–0.9908（本族实测） | prod 死 |
| ds292 `_unknown`（workforce） | — | 3 | 2Y / S | 0.8427–0.8586（本族实测） | prod 死 |
| ds487 other143（券商集中度） | OTHER | 7 | F | 0.8658–0.8704（本族实测） | prod 死 |
| ds550 risk60（借券费率） | RISK | 4 | SUB | 0.9631–0.9917（本族实测） | prod 死 |
| ds579 techindi_model | OTHER | 8 | F / 2Y | `predicted_*` 0.7947；`tm_*` 未测 | **F 前沿封闭 → 判死** |
| ds381 insider_matrix | OTHER | 12 | SUB | 0.6964（subind 0.2/0.8）/ 0.8092（industry） | **同概念，名额已占** |
| ds382 insider_trx_matrix | OTHER | 6 | SUB / S | 0.5516–0.6811（basket 族）/ 0.8085（top 窗口） | **同概念，名额已占** |

> 塔占用说明：DB 内 `category` 对伪数据集（381/382 等）为 NULL，塔位判定以平台 pyramid 为准；本表"塔已亮"依据为用户明示的 MODEL + ANALYST 6 颗 ACTIVE。

---

## 3. G1 唯一 prod 未测机制：`techindi_model` 的 `tm_*` 回归簇（3 臂）

| 臂 | S | F | TO | 2Y | SUB/S | 缺口 | prod |
|---|---|---|---|---|---|---|---|
| `XgRzXqpx` | 2.10 | 0.96 | 0.220 | 2.18 | 0.548 | **F −0.040** | 未测 |
| `1YjK1XNM` | 1.75 | 0.86 | 0.163 | 2.22 | 0.549 | F −0.140 | 未测 |
| `akVzMbR9` | 1.80 | 0.86 | 0.173 | 2.22 | 0.539 | F −0.140 | 未测 |

**归因（为什么不值得为 0.04 再开一波）**：

1. **F 是算术约束，不是拟合问题**。本族实测 returns 4.0–4.6%、TO 0.17–0.27；S=2.10 时 F 的解析上界就是 ≈0.96（`tm_w3` 已算过）。要过 1.0 需 returns ≥ 5.0% 或 TO ≤ 0.19。
2. **三条 TO-only 杠杆已全部试过**：
   - `decay` 5→12/15/20：TO 0.33→0.13–0.16，但 S 同步下滑，F 卡在 0.86（`tm_w4`）。
   - `ts_target_tvr_decay`：`N1eJkjVX` F 0.85。
   - `hump`：`E5V8oWnR` S **0.49** / F 0.13 / TO 0.0346 —— 平滑把信号本体抹掉。
3. **同族跨期限相加会互相抵消**：1d+5d+10d 混合 S 崩到 0.29；1d 与 10d 差分 S 0.24 / 2Y −1.10（`tm_w3`）。
4. **提升 returns 的唯一路径是换概念/加腿**，而加腿＝混信号，违反项目红线。

**判定：`techindi_model` 在 USA/D1 判死，交 task #81 封存流程（论坛取证 → `seal_dead_end`）。** 本组不消耗任何仿真或 prod 队列。

---

## 4. G2 同概念自锁（18 臂）：只有"替代"价值，没有"新增"价值

### 4.1 ds381 `insider_matrix`（12 臂，全部基于 `eur_aggregated_value_1`）

| 臂 | 中性化 | tail 宽度 | S | F | TO | 2Y | SUB/S | 缺口 | prod |
|---|---|---|---|---|---|---|---|---|---|
| `A1QrA2kX` | subindustry | 0.25/0.75 | 2.92 | 1.40 | 0.483 | 2.56 | 0.428 | SUB −0.017 | 未测 |
| `A1Qzj6ol` | subindustry | 0.25/0.75 | 2.97 | 1.56 | 0.409 | 2.23 | 0.407 | SUB −0.079 | 未测 |
| `omoG8Qm6` | subindustry | 0.20/0.80 | 2.98 | 1.57 | 0.411 | 2.31 | 0.423 | SUB −0.033 | 未测 |
| `gJWGJ2wJ` | subindustry | 0.30/0.70 | 2.60 | 1.58 | 0.309 | 1.77 | 0.423 | SUB −0.028 | 未测 |
| `j2eG27WZ` | subindustry | 0.10/0.90 | 2.57 | 1.56 | 0.311 | 1.79 | 0.401 | SUB −0.085 | 未测 |
| `wp9GgPJ2` | subindustry | 0.18/0.82 | 2.95 | 1.43 | 0.486 | 2.69 | 0.414 | SUB −0.060 | 未测 |
| `pwvGOZ7q` | subindustry(std=3) | 0.20/0.80 | 2.97 | 1.43 | 0.486 | 2.68 | 0.401 | SUB −0.099 | 未测 |
| `ZYmzYJkQ` | subindustry(decay22) | — | 2.79 | 1.82 | 0.310 | 2.43 | 0.412 | SUB −0.061 | 未测 |
| `omoGmdvE` | subindustry(裸 rank) | — | 2.82 | 1.84 | 0.310 | 2.40 | 0.404 | SUB −0.084 | 未测 |
| `1YjlM2gJ` | industry | 0.25/0.75 | 3.14 | 1.59 | 0.490 | 2.68 | 0.398 | SUB −0.113 | 未测 |
| `9qEM0mao` | industry | 0.20/0.80 | 3.20 | 1.63 | 0.493 | 2.84 | 0.419 | SUB −0.049 | 未测 |
| `zqrGqVXo` | industry | 0.25/0.75 | 2.84 | 1.87 | 0.307 | 1.94 | 0.433 | SUB −0.003 | **0.8092** |

**对照锚点（在册 basket 第 4 臂）**：`d5KzLo7v` = subindustry / 0.20/0.80 / std=2，S 2.93 / F 1.41 / TO 0.485 / 2Y 2.53 / SUB 1.29（比值 **0.440 PASS**），**prod 0.6964**。

**归因**：
- **中性化决定生死**：同一表达式只换 `industry`→`subindustry`，prod 从 **0.8092 → 0.6964**（−0.113）。industry 侧全部 prod 死；subindustry 侧 prod 余量仅 **0.0036**。
- **表达式中 5 组 byte-identical 重复**（模拟了两次、设置不同）：`A1QrA2kX ≡ A1Qzj6ol`、`omoG8Qm6 ≡ d5KzLo7v`。池内冗余来自"扫参数"，不是新信息。
- **SUB 墙不可破**：tail 宽度、std、decay 三条轴把 SUB/S 顶到 0.401–0.440，**只有 0.20/0.80 + subindustry 这一格过线**（与 `insd_w3` 的甜区结论一致）。近闸臂都在 0.40 附近，差 0.01–0.11。
- **结论**：本组臂若提交，与 `d5KzLo7v` 的 self-corr ≈1，**不增加名额**；且没有任何一条在"SUB 比值 + prod"两项上同时优于 `d5KzLo7v`。**不投**。

### 4.2 ds382 `insider_trx_matrix`（6 臂，买入交易计数）

| 臂 | 表达式核心 | S | F | TO | 2Y | SUB/S | 缺口 | 同式在册臂 / prod |
|---|---|---|---|---|---|---|---|---|
| `omoZ03em` | `ts_zscore(ts_sum(total_buy_transaction_count,126),252)` | 2.44 | 2.03 | 0.083 | 2.68 | 0.422 | SUB −0.029 | ≡ `XgRM3Yra` / **0.5803** |
| `bl8A1opZ` | `ts_zscore(ts_sum(mean_top_buy_transaction_count,63),252)` | 2.51 | 2.57 | 0.110 | 3.27 | 0.394 | SUB −0.099 | ≡ `LL53QVvn` / **0.5761** |
| `mLYQWre2` | `ts_zscore(ts_sum(mean_buy_transaction_count,126),252)` | 2.48 | 2.08 | 0.083 | 2.62 | 0.411 | SUB −0.056 | `vROPEJ8w`(63) / **0.5517** |
| `akVG0Wjx` | 同 `mLYQWre2`（另一设置） | 1.57 | 1.09 | 0.086 | 2.09 | 0.611 | S −0.010 | 同上 / 0.5517 |
| `vROPXe3w` | `ts_zscore(ts_sum(total_top_buy_transaction_count,63),252)` | 2.48 | 2.53 | 0.111 | 3.27 | 0.387 | SUB −0.116 | `qMEVJPo2`(top,126) / **0.8085** |
| `E5Vxjr71` | `ts_zscore(ts_sum(total_top_buy_transaction_count,21),252)` | 1.52 | 1.23 | 0.183 | 2.48 | 0.625 | S −0.060 + **CW +0.0055** | 同上 / 0.8085 |

**归因**：
- **buy-count 族 prod 分两档，取决于窗口与"top"口径**：全量买入计数窗口 42–126 → **0.55–0.68**（活）；`total_top_buy` 窗口 126 → **0.8085**（死）。`E5Vxjr71` 用 top + 短窗 21，CW 也破线。
- **SUB 墙同 ds381**：本族全部 6 臂 SUB/S 0.387–0.422，只有 `akVG0Wjx` / `E5Vxjr71` 靠"低 S 换高比值"过关，但 S 又不够。**SUB 与 S 在同一批里负相关**，这是小票信号的固有张力。
- **结论**：与 basket 六臂互为同式 / 近孪生，**不增加名额**。其中 `omoZ03em`（S 2.44 vs `XgRM3Yra` 1.66）与 `bl8A1opZ`（S 2.51 vs `LL53QVvn` 1.61）质量更好但不改名额数——**可在提交排序时作为备选替换件**，前提是 SUB 修到 0.434 以上。

---

## 5. G3 家族 prod 已死（27 臂）：六条已封的路

| 家族 | 臂 | 缺口 | 家族实测 prod | 机制归因 |
|---|---|---|---|---|
| **ds389 intraday_pv_feats** | `levR9Vq7`(F−0.050) `9qjAmw1o`(F−0.140) `MPa5ZpRa`(F−0.130) `JjNn8qQA`/`9qj9lYE2`/`akbNa6K1`/`d5bnapWY`(S−0.08~−0.11 + F−0.09~−0.14) | F / S | **0.7864 / 0.8693 / 0.8739** | 收盘前 30 分钟微结构 + 价量相关；被 PV book 完全覆盖。价格类在 USA 已饱和。 |
| **ds484 order_book_imbalance** | `XgbZ2aaX`(2Y−0.150) | 2Y | **0.8133** | 暗池成交量水平 `vec_avg(dark_trade_volume)`；水平类信号 2Y 与 prod 双杀。 |
| **ds487 other143** | `akVeM8G1` `78o3QRwO` `9qE86KZr` `mLYdzAp2` `58jrz86J` `bl8Jbrqm` `omoRWYEn`（F −0.04~−0.14） | F | **0.8448–0.8704** | 券商集中度水平（`exempt_tier1_broker_concentration_index` / `industry_top_broker_share_pct`）；S 2.2–2.6 / 2Y 2.4–2.7 都极强，但 returns/TO 比不足，且 prod 已 0.86+。**IS 强 ≠ 可提交**的典型。 |
| **ds550 risk60** | `xA12OZVN` `Vkdm1WZM` `QPYNZ8NK` `vROp8J6d`（SUB −0.026~−0.098） | SUB | **0.9631 / 0.9861 / 0.9917** | 借券费率 −group_zscore(sector)。F 4.0–4.1、2Y 3.18 是全场最强，但 prod 近乎 1：该概念就是卖方拥挤度的另一种写法。 |
| **ds585 web_traffic_engage** | `e76QAEoN`(2Y−0.110) | 2Y | **0.9740–0.9908** | 移动端访问占比。注意力强度族的第五次撞墙（前有 visit_count / pages_per_session / engagement_depth）。 |
| **ds292 workforce** | `e76QLMjp`(S−0.090) `leMKrwox`(2Y−0.090 + **TO 0.009<0.01**) `1YjZJ8qk`(S−0.040 + 2Y−0.020) | S / 2Y / TO | **0.8427 / 0.8586** | 员工流入流出 / 人均薪酬 / 声望分。两闸同缺，且 prod 0.84+。 |

> 家族 prod 取值 = 同数据集、同字段族、已实测（平台 `check_correlation` 或 `platform_sync`）臂的实测值；括号内为该臂自身是否实测。**这些数字不是推测**，来源见附录 A 的 SQL。

---

## 6. G4 已点亮塔（12 臂）：按用户裁定不投

| 塔 | 数据集 | 臂 | 缺口 | prod |
|---|---|---|---|---|
| ANALYST（已 6 颗 ACTIVE） | ds317 analyst_consensus | `vR2NgnVQ` `786z90gQ` `pw5NOxw3` `58gpWgxM` `3qVpWZWZ` `pw5NOW63` `0mrpvZ08` `GrOGJGE0` `MP3GmEV9`（F/2Y） `O08GawAg` `wpbagVMY`（SUB） | F −0.01~−0.14 / SUB −0.09~−0.12 | 0.6540（已提交臂）**唯一 prod 健康的近闸族** |
| MODEL（用户已点亮） | ds294 ai_equity_alpha | `78o32Ndb` | 2Y −0.050 | 0.5626（已提交臂） |

**说明**：这两族是清单里**唯一"prod 余量充足 + 只差 0.01–0.14"**的组。若不受"已点亮塔不作主数据集"约束，`3qVpWZWZ`（F 0.99）与 `GrOGJGE0`（F 0.99 / 2Y 1.55）是全场最接近过闸的臂。**按现行纪律不投**；如需动用，须用户显式改判。

---

## 7. 归因总表：五条可复用律

1. **F 墙是算术，不是拟合。** `F = S·√(ret/TO)`。USA/D1 上 returns < 5% 的族（techindi 4.0–4.6%、analyst 低换手）只有在 TO < 0.19 时才可能 F > 1.0；而所有"降 TO"的算子（decay / hump / tvr_decay）都会同步或超额降 S。**看到 F 差 0.05 以内，先算算术上界，不要直接开修复波。**
2. **SUB 墙 = 收益在小票的占比，与 S 负相关。** insider 族实测：`TOP1000` 迁移把 S 2.93→1.19（`insd_inv_w1`）；`MARKET` 中性化抬 SUB 但 S 掉 ~0.4（`insd_w2`）；tail 宽度只有 0.20/0.80 一格过线（`insd_w3`）。**SUB 与 S 不可同时最大化，这是结构性的。**
3. **家族 prod 先验优先于单臂 prod。** 61 个近闸臂里实测 prod < 0.7 的是 **0 个**；但家族先验把 9/11 个数据集判死。**在 USA/D1，prod 是"概念级"属性，不是"参数级"属性**——同一概念的窗口/中性化微调只能把 prod 从 0.81 压到 0.70，压不到 0.55。
4. **中性化是 prod 的开关，不是装饰。** ds381 同一表达式 `industry`→`subindustry` = prod 0.8092→0.6964；反之 ds382 全族在 `MARKET` 下 prod 最低（0.55）。**换区/换族时中性化必须逐字对齐，不能"取一个合理的"。**
5. **"IS 极强 + prod 极死"是 USA 的常态，不是异常。** 本清单里 S > 2.4 的 14 个近闸臂，13 个家族 prod ≥ 0.79。**S 越高越要早测 prod**（`prod-first` 探针），否则整波回测都是沉没成本。

---

## 8. 定向挖掘方案（按优先级）

### P0 — 结案动作（零仿真、零新仿真）

| 动作 | 对象 | 触发条件 | 产出 |
|---|---|---|---|
| 判死封存 | `techindi_model`（ds579） | F 前沿已由 tm_w1–w4 打穿 | 论坛取证 → `seal_dead_end`（task #81） |
| 不投 | G2 全部 18 臂 / G3 全部 27 臂 | 同概念或家族 prod ≥ 0.79 | 写入本清单，不占仿真槽 |
| 不投 | G4 12 臂 | 塔已点亮 | 若用户改判可立即复活（prod 0.56–0.65） |

### P1 — `macro27` 已结案（2026-10-24）：概念级 prod 死，不开 w2

**6 臂收批结论（波 `macro27_w1`，`wave_results` id 1387）**

| 读数 | 值 | 判读 |
|---|---:|---|
| 最强臂 `WjLxAWoN`（招聘重发占比）prod | **0.8771** | 超红线 0.75，死 |
| 时长比率可提交方向 prod | **0.7933** | 由负向臂 `min=−0.7933` 精确推出 |
| 负向臂自身 prod max | 0.6526 | 过线，但方向不可用 |
| 6 臂 max S | 1.39 | 未触判弱线（0.9），却被概念级 prod 先验否决 |
| 共同失效年 | 2023（`WjLxAWoN` 2023 S −0.13 / ret −0.39%，其余 9 年全正） | 结构性问题，不是参数问题 |

- **判定**：两个最强概念（重发占比、时长比率）在**可提交方向**均被 prod 锁死——概念级而非参数级，与 G3 六族同构。**不开 w2**。
- **不 seal_dead_end**：论坛取证为 `read_failed`（工具故障），按 AGENTS §8.11 故障不得作判死证据（task #92 已按此收口）。
- **教训（已写入 `wave_results` ⑧）**：多臂首波收批后**先测最强臂的 prod 再决定第二批**；本波 6 条 sim 换来的概念级结论，2 条 prod 探针即可得到。

### P2 — 第 5 颗的来源调整（2026-10-24 起）：`fundamental93`

**候选否决（全部按 live 数据，旧画像不作证）**

| 候选 | live 读数 | 判定 |
|---|---|---|
| `earnings4` | 数据集级 **aC 13771** / userCount 2821 / 375 字段 | Tier B 饱和（单字段 aC 11–97 只是长尾，先前误读） |
| `imbalance5` | 实际是 **油冲击韧性分** `imb5_score`（"SHIELD-OIL composite score"）+ `imb5_mktcap`，aC 3221 | 本报告旧文误标为 order imbalance；2 字段、拥挤度高 |
| `institutions18` | `88PmKRzv` prod **0.9493**（2026-10-24 现测）/ `RR6JkEpd` 0.9377 + self 0.7256 | 真死，revived 标记只反映 sibling 误判修复 |
| `fundamental110` / `fundamental14` / `fundamental91` | 26 / 248 / 407 字段，绝大多数 VECTOR 元数据（日期、ID、filing_type、文本分数），覆盖 0.32–0.89 | 信号面窄，先不做 |

**选中 `fundamental93`**（别名 `other452` 同源）：FUNDAMENTAL 未点亮塔，**46 字段、aC 85、覆盖 0.31–0.93**，
机制 = 税务应计 / 应计 / 资产增长（Sloan 1996 应计异象、Cooper-Gulen-Schill 资产增长异象、book-tax difference 盈余质量），
与已跑完的 11 族正交。

**6 臂（USA/TOP3000/D1，SUBINDUSTRY，decay 4，trunc 0.08，nanHandling ON，multisim `1B1NGz56G5de9c4dXKAb4eN`）**

| # | 字段 | 机制 | 方向 |
|---:|---|---|---|
| 1 | `fnd93_accruals_d1_mean` | 应计水平（LTM 均值） | 空高应计 |
| 2 | 同上 `ts_delta 252` | 应计同比变化 | 空升应计 |
| 3 | `fnd93_accruals_d1_current_t` | 应计相对自身 LTM 的 z 突刺 | 空高 z |
| 4 | `fnd93_accrualsratio_d1_asset_change` | 资产增长（YoY 资产比） | 空高增长 |
| 5 | `fnd93_tax_accruals_11` | 税应计（税费−现金税）/ 分母 | 空高税应计 |
| 6 | `fnd93_expense_d1_current_t` | 递延税费用 z | 空高 z |

统一壳：`-group_rank(ts_zscore(ts_backfill(<field>, 252), 504), subindustry)`。

**预注册判据**：判弱线 max S < 0.9 ⇒ 全族不承载横截面信号，不扩批；扩臂线 S ≥ 1.2 且 F ≥ 0.6 ⇒ 只动回填/窗口/中性化，不动概念；过闸线 S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 ⇒ 立刻 prod-first；**任一臂收批后先测最强臂 prod 再决定第二批**（P1 教训）。

**收批结果**：见 §8.1（wave `fnd93_w1`）。

### 8.1 — P2 收批：`fnd93_w1` 六臂全灭（2026-10-24，wave_results id 1388）

**六臂实测（平台读数，S/F/TO/returns/2Y/SUB 为平台指标，risk-neut S = 平台 `risk_neutralized_sharpe`）**

| # | alpha | 字段 | S | F | TO | returns | 2Y | SUB | risk-neut S |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `A1Q20v5w` | `accruals_d1_mean` | −0.64 | −0.24 | 1.50% | −1.75% | −0.85 | −0.30 | **+0.17** |
| 2 | `XgROWJA5` | `accruals_d1_mean` Δ252 | −0.57 | −0.21 | 1.80% | −1.77% | −0.87 | −0.27 | **+0.41** |
| 3 | `akVgLx9W` | `accruals_d1_current_t` | −0.78 | −0.35 | 1.76% | −2.48% | −1.08 | −0.58 | −0.02 |
| 4 | `RRAvV6wb` | `accrualsratio_d1_asset_change` | −0.72 | −0.28 | 2.68% | −1.94% | **−1.70** | +0.01 | −0.13 |
| 5 | `O0J2r8Xd` | `tax_accruals_11` | −0.54 | −0.19 | 1.76% | −1.47% | −1.02 | −0.53 | **+0.28** |
| 6 | `P0MAZgLE` | `expense_d1_current_t` | −0.77 | −0.40 | 1.59% | −3.42% | −0.93 | −0.47 | −0.54 |

全 6 臂：MAX / 2Y / SUB / LOW_SHARPE / LOW_FITNESS 全 FAIL；LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / MATCHES_PYRAMID 全 PASS。
金字塔挂载 `USA/D1/FUNDAMENTAL`，multiplier 1.1。

**四条归因（按证据强度排序）**

1. **方向即概念失效，不是参数问题。** 六臂全为负 Sharpe（−0.54…−0.78），反号方向 |S| 上限 **0.78 < 预注册判弱线 0.9**
   ⇒ 该族在 USA 横截面上不承载可用信号。按预注册条款**不开第二批**。
2. **F 算术封死"调壳救族"这条路。** 平台把年化换手地板钉在 **12.5%**，故 `F = S·√(ret / 0.125)`。
   实测逐位吻合：`P0MAZgLE` S −0.77 / ret −3.42% ⇒ |F| = 0.77×√(0.0342/0.125) = **0.40**，与平台 F −0.40 一致。
   要 F ≥ 1.0，需 `S·√ret ≥ 0.354`；S 取闸线 1.58 时 **ret ≥ 5.0%**，而本族 ret 只有 1.5–3.4%
   ⇒ 换窗口 / 换回填 / 换中性化都改不动这个乘积。
3. **近两年结构性反转。** 资产增长臂 `RRAvV6wb` 的 2Y = **−1.70**，是六臂最差；其余 2Y 也全在 −0.85…−1.08。
   Sloan 应计异象与 Cooper-Gulen-Schill 资产增长异象在 2022–2023 高利率 / 资本开支周期里被反向定价。
4. **负 alpha 里有一部分只是行业/风险暴露。** 三臂 risk-neutralized Sharpe 转正（+0.17 / +0.41 / +0.28）
   ⇒ 剥离行业与风险因子后，纯应计残差更弱 —— 与「该族只有暴露、没有 alpha」一致。

**为什么可以直接换数据集（不是"频繁切换"）**

- 触发的是**预注册判据**（max S < 0.9），不是"跑了几批没感觉"。判据写在派发前（§8 P2 预注册判据），此刻只是执行。
- `fundamental93` 的 46 字段全部落在**同一个概念面**（税务应计 / 应计 / 递延税费用 / 资产增长），
  没有第二个可供切换的机制；同概念换字段只是重复第 1–6 臂。
- 该数据集 aC 仅 85（未饱和），但**低拥挤度救不了 F 墙**：问题在收益量级，不在拥挤度。

### P3 — 第 5 颗的新来源（2026-10-24 起）：`order_flow_imb`（OPTION 未点亮塔）

**为什么换成它**

| 维度 | 读数（2026-10-24 live） | 判读 |
|---|---|---|
| 塔位 | `option` 塔 **未点亮** | 符合"已点亮塔不作主数据集" |
| 字段 | **120 个 MATRIX**（无 VECTOR，无长表元数据） | 可直接做横截面信号 |
| 覆盖 | base 变体 **0.9058**；`_ise` 0.7882 / `_noto` 0.7728 / `_otm` 0.7701 | 无需为覆盖做重回填 |
| 拥挤度 | 数据集 aC **478** / userCount 197；最挤字段 `customer_trade_imbalance` aC 108 | 远低于 Tier B（≥1 万） |
| 金字塔 | USA/D1/OPTION multiplier **1.3×** | 点塔收益高 |
| 机制面 | 6 类参与者（broker_dealer / customer / firm / market_maker / pro_customer / proprietary）×
bearish/bullish × contracts/trade_count/trades/vol × imbalance × 4 个变体 | 机制空间与已跑 11 族正交 |

**论坛已验证配方**（`read_forum_post` 42078917602455，93 票帖，29 票 / 25 评）：

- 原帖冠军 `qM6ZNpaE`：**S 1.17 / 2Y 1.76 / TO 26.18% / 7 算子 / 2 字段 / ATOM**，PPA self-corr 0.168。
- 经济机制（原帖原文）：「专业客户（知情交易者）的看涨成交量相对于公司/做市商（流动性提供者）急剧上升时，
  市场往往过度反应，后续价格会反向修正」，用 **`ts_ir`** 衡量情绪分化的持续性后**取负号做反转**。
- 算子数反推：`-ts_ir(ts_backfill(A,5) − ts_backfill(B,5), 22)` = 2 字段 + 2 backfill + 1 减法 + 1 ts_ir + 1 负号 = **7**，
  与"7 算子 / 2 字段"精确吻合 ⇒ 原帖未加 `group_rank`，横截面可比性由 ts_ir 的尺度无关性保证。
- 帖子设置是 **TOP1000 / INDUSTRY / PPA**；本波按战役口径落在 **TOP3000 / D1**，故用两个 multisim 分别钉
  INDUSTRY（论坛对齐）与 SUBINDUSTRY（战役标准），把中性化当**设置层对照**而非猜测。

**6 臂（wave `ofi_w1`）**

| # | multisim | 中性化 | 表达式 | 机制 |
|---:|---|---|---|---|
| 1 | `1HsjND9fR50E9XmYI9KvOkC` | INDUSTRY | `-ts_ir(ts_backfill(pro_customer_bullish_vol,5) - ts_backfill(firm_bullish_vol,5), 22)` | 论坛主配方（公司作对手方） |
| 2 | 同上 | INDUSTRY | 同 #1 **去负号** | 符号对照（动量假设） |
| 3 | `3YYYHFbGU4tP9F39fvV0010` | SUBINDUSTRY | `-ts_ir(ts_backfill(pro_customer_bullish_trade_count,5) - ts_backfill(market_maker_bullish_trade_count,5), 22)` | 换载体（笔数 > 名义额）+ 做市商对手方 |
| 4 | 同上 | SUBINDUSTRY | `-group_rank(ts_delta(ts_backfill(pro_customer_trade_imbalance,5) - ts_backfill(market_maker_trade_imbalance,5), 5), subindustry)` | 分歧加速度（ts_delta 形态） |
| 5 | 同上 | SUBINDUSTRY | `-group_rank(ts_zscore(ts_backfill(pro_customer_vol_imbalance_otm,5), 66), subindustry)` | OTM 知情投机单类 |
| 6 | 同上 | SUBINDUSTRY | `-group_rank(ts_zscore(ts_backfill(customer_trade_imbalance,5), 66), subindustry)` | 散户逆向（dumb money 对手） |

- 统一设置：USA / TOP3000 / D1 / decay 4 / truncation 0.08 / nanHandling ON / unitHandling VERIFY /
  pasteurization ON / maxTrade OFF / FASTEXPR。
- **形状族 3 个**（ts_ir ×3 / ts_delta ×1 / ts_zscore ×2），`trade_when` 0%，载体 4 种（vol / trade_count / imbalance / imbalance_otm），
  满足闸 6 的「≥3 形状族、`trade_when` ≤ 40%」。
- **单数据集（ATOM 口径）**：全部字段来自 `order_flow_imb`，跨参与者相减是同一数据集的**一个经济量**
  （知情 vs 流动性提供者的看涨分歧），不是「add A,B」混信号。
- **#1/#2 是符号对照**：同一表达式的正负两版，把「概念死」与「符号反」拆成两个可区分结论 —— 无论结果如何，
  都至少有一臂落在正确方向；这是对 fnd93 教训（六臂同号、无法分辨符号）的直接修正。

**预注册判据（与 P2 同口径）**：判弱线 max S < 0.9 ⇒ 概念不承载信号，不扩批；扩臂线 S ≥ 1.2 且 F ≥ 0.6 ⇒
只动回填/窗口/中性化；过闸线 S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 ⇒ 立刻 prod-first（先测最强臂 prod 再决定第二批）。

#### 收批结果（2026-10-24，`wave_results` `ofi_w1`，id 由 harvest 新建后闭案）

| # | alpha | 中性化 | S | F | TO | ret | 2Y | SUB | RN S | invest S |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `leMNKea8` | INDUSTRY | −0.33 | −0.09 | 13.45% | −1.09% | +0.07 | −0.08 | −0.41 | −0.20 |
| 2 | `78o268Y2` | INDUSTRY | **+0.33** | +0.09 | 13.45% | **+1.09%** | −0.07 | +0.08 | +0.41 | +0.20 |
| 3 | `rKdnevdJ` | SUBINDUSTRY | +0.02 | 0.00 | 14.49% | +0.11% | −0.25 | +0.01 | −0.18 | +0.16 |
| 4 | `npAXPMAl` | SUBINDUSTRY | −0.53 | −0.10 | 44.37% | −1.61% | −0.28 | −0.37 | −0.01 | −0.43 |
| 5 | `O0J28EAq` | SUBINDUSTRY | −0.32 | −0.09 | 15.98% | −1.22% | −0.63 | −0.40 | −0.36 | −0.36 |
| 6 | `j2eM8bYk` | SUBINDUSTRY | **−1.11** | −0.31 | 42.37% | −3.28% | −0.75 | −1.08 | −0.39 | −0.98 |

**四条归因**

1. **论坛主配方在 REGULAR/TOP3000 上是对称噪声**。臂 1/2 是同一表达式仅差符号，结果 S −0.33 vs +0.33、
   ret −1.09% vs +1.09% **逐位镜像** ⇒ 该分歧量在本设置下不含方向信息。论坛的 S 1.17 属 TOP1000 + PPA 设置，
   不可平移到 TOP3000/D1/REGULAR。
2. **换载体不救**。臂 3 把名义额换成笔数、对手方从 firm 换成 market_maker，S 0.02 —— 精确等于零；
   说明失效不在载体选择，而在概念本身。
3. **唯一活的方向是"客户订单不平衡动量"**。臂 6 的**反号**方向（`customer_trade_imbalance` 66 日 z-score 取正）
   逐年 8/10 年为正：+2.44 / +0.76 / −0.54 / +1.51 / −0.50 / +2.37 / +1.46 / +2.28 / +0.29 / +1.31
   ⇒ 稳健、无单年依赖、非过拟合；**问题纯粹是强度不足（S 1.11）**。
   方向本身与"散户 dumb money 反向指标"的直觉相反，与 Boehmer-Jones-Zhang-Zhang(2021) 的
   「零售订单流含量化信息」一致。
4. **F 算术封死，不存在"针对性调参"的空间**：
   `F = 1.11 × √(0.0328 / 0.4237) = 0.31`。F ≥ 1.0 在 S = 1.58 时需 `ret ≥ 5.0%`，即 `vol ≥ 3.16%`
   （现 vol = 3.28/1.11 = 2.96%）。等价于要求**同时**把 S 抬 +42%、TO 压 −70%；任何单壳层杠杆
   （回填/窗口/hump/中性化）都只能动其中一项 ⇒ 按预注册**不扩批**，这不是"盲扫省事"，是算术结论。

**结论与更强的发现：该数据集属 PPA-profile，不属 REGULAR。**

平台对本波六臂给出的 `ppa_failed_checks` 只有 **`LOW_SHARPE` / `LOW_SUB_UNIVERSE_SHARPE`，没有 `LOW_FITNESS`、也没有 `LOW_2Y_SHARPE`**
—— 即 PPA 轨不设 fitness 闸。而论坛冠军 `qM6ZNpaE` 本身就是 **PPA 投稿**（帖子自标 PPA self-corr 0.168）。
两条独立证据同向：**期权订单流是"高换手 / 低边际"信号类，其正确归宿是 PPA**。
臂 6 反号后 S +1.11 / SUB +1.08 ⇒ SUB 闸在反号方向大幅通过，只剩 PPA 的 Sharpe 线。
⇒ REGULAR 口径判死（不扩批、不调壳）；若转 PPA 战役，这是现成的首颗候选。

### P2.1 — 明确不建议

- `macro` 其余集（macro38 aC 16121 / macro10 1269 / macro4 1327）：拥挤度高于 macro27。
- 回头重扫 G3 六族：全部有实测 prod ≥ 0.79，重扫只会重复已知结论。
- `earnings4` / `earnings_chart_dl`：Tier B 饱和 / DL 预测与 MODEL 同族（prod 风险）。

---

## 9. 附录 A：复现 SQL 与全过未提交池

### A.1 近闸分类核心 SQL

```sql
SELECT a.alpha_id, a.dataset_id AS ds, a.sharpe AS s, a.fitness AS f,
       a.turnover AS to_, a.two_year_sharpe AS ty,
       a.sub_universe_sharpe AS sub, a.concentrated_weight AS cw,
       a.cluster_test AS ct, a.prod_correlation AS prod,
       a.self_correlation AS selfc, a.platform_status AS ps,
       a.universe, a.neutralization, a.expression
FROM alphas a
WHERE a.region_id = 1
  AND (a.soft_deleted IS NULL OR a.soft_deleted = 0)
  AND a.sharpe IS NOT NULL AND a.fitness IS NOT NULL
  AND a.two_year_sharpe IS NOT NULL AND a.turnover IS NOT NULL
  AND a.sharpe >= 1.30;
-- 逐臂计算：S>=1.58 / F>=1.0 / 0.01<=TO<=0.7 / 2Y>=1.58
--          SUB >= 0.434*s / cw <= 0.1 / prod<0.7 / self<0.7
```

### A.2 家族 prod 先验查询

```sql
SELECT alpha_id, dataset_id, prod_correlation, prod_corr_source, corr_checked_at, expression
FROM alphas
WHERE region_id = 1 AND (soft_deleted IS NULL OR soft_deleted = 0)
  AND platform_status IN ('ACTIVE','SUBMITTED','DECOMMISSIONED')
ORDER BY dataset_id, prod_correlation DESC;
```

### A.3 全过未提交池（76 臂，按 prod 排序的前 20）

| 臂 | 数据集 | S | F | TO | 2Y | SUB/S | prod | 判定 |
|---|---|---|---|---|---|---|---|---|
| `O0Jgd7Y7` | ds382 | 2.27 | 2.03 | 0.130 | 3.09 | 0.537 | **0.5516** | **basket #1** |
| `vROPEJ8w` | ds382 | 2.08 | 1.74 | 0.105 | 3.49 | 0.630 | 0.5517 | 与 #1 相关 >0.7 |
| `LL53QVvn` | ds382 | 1.61 | 1.39 | 0.112 | 2.75 | 0.621 | **0.5761** | **basket #3** |
| `1Yj08nb6` | ds382 | 1.58 | 1.20 | 0.100 | 2.29 | 0.595 | 0.5796 | 与 basket 相关 >0.7 |
| `XgRM3Yra` | ds382 | 1.66 | 1.19 | 0.087 | 2.27 | 0.584 | 0.5803 | 与 #1 0.7642 |
| `1YZp6EP6` | ds317 | 1.86 | 1.14 | 0.061 | 1.70 | 0.489 | 0.6783 | ANALYST 塔已亮 |
| `YPx89bQJ` | ds294 | 2.19 | 1.16 | 0.157 | 1.91 | 0.566 | 0.6803 | MODEL 塔已亮 |
| `88vXxaqv` | ds382 | 1.99 | 1.66 | 0.095 | 2.04 | 0.447 | **0.6811** | **basket #2** |
| `d5KzLo7v` | ds381 | 2.93 | 1.41 | 0.485 | 2.53 | 0.440 | **0.6964** | **basket #4** |

> **basket 极值性已证**：`compute_mutual_correlation` 在阈值 0.7 下的最大互不相关子集 = `[O0Jgd7Y7, 88vXxaqv, LL53QVvn, d5KzLo7v]`，`max_subset_exact=true`。第 5 颗必须来自新机制。

**prod 分档统计（76 臂，全部 RA 全过、全部未提交）**：

| prod 档 | 臂数 | 说明 |
|---|---|---|
| < 0.70 | 17 | 其中 7 非点亮塔（basket 4 + 3 同族排斥），10 属 ANALYST/MODEL 已亮塔 |
| ≥ 0.70 | 33 | prod 墙，含全部 5 个已死族的全过臂 |
| 未测 | 26 | 全部属已知家族（ANALYST / MODEL / RISK / INSTITUTIONS / ds381） |

---

## 10. 与交付台账的关系

- 严格口径交付进度（5/10）与 §9 补挖记录见 `output_report/USA_regular_alpha_delivery_20261021.md`（该文档覆盖至 2026-10-23，本清单的 2026-10-24 进展待追加 §10）。
- 本清单不改变任何 alpha 状态、不写库、不发起仿真；仅为定向挖掘的决策依据。
- **提交红线不变**：任何候选进入提交前必须 `submit_verdict` → `check_correlation(refresh=True)`（prod 与 self 均 < 0.7）→ 与 basket 两两相关核验 → **用户明确确认** → `workflow_submit_alpha(confirm_submit=True)`。
