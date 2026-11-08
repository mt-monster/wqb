# shortinterest3 第一波 — 借券市场 ATOM（DEU / TOP500 / D1）

> 日期 2026-11-04 ｜ 波次 `si3_wave1_20261104` ｜ 16 条（12 模板 + 4 符号探针）
> 状态：**进行中（平台槽位拥堵，多次 BATCH_SPAWN_FAILED）**，已回 4 条，其中 **T3 = 1.26 为本轮最强 ATOM 候选**

## 一、数据集画像

| 项 | 值 |
|---|---|
| 字段数 | 25，**全 VECTOR** |
| coverage | 0.653 – 0.783，按三档命名不同 |
| 拥挤度 | **base 档极低**（αCount 4–47）、`_main` 中（8–56）、`_p5_d1` 高（30–175）、`shrt3_bar` 341 |

### 三档命名（同义不同聚合）

| 档 | coverage | 拥挤度 | 备注 |
|---|---|---|---|
| 裸名（如 `mean_loan_rate`） | 0.668 | **最低（4–47）** | 首选探索档 |
| `_main` | 0.687 | 中（8–56） | 主键组口径 |
| `_p5_d1` | **0.783** | 高（30–175） | 覆盖最好但已被大量使用 |

### 9 个经济量 × 3 档

`mean_loan_rate`（加权平均借券费率）／`max_loan_rate`／`min_loan_rate`／`loan_rate_volatility`（费率标准差）／`loaned_market_value_usd`（借出市值）／`loaned_share_count`（借出股数）／`average_loan_duration_days`（加权平均借券账龄）／`transaction_count`（成交笔数）／`shrt3_bar`（**借券需求评级 1–10**）

## 二、机制与文献

| 量 | 经济含义 | 预期符号 | 文献 |
|---|---|---|---|
| 借券费率水平 | 做空成本 / 拥挤度 | 高费率 → 后续低收益 | Drechsler & Drechsler (2016) 空头溢价；D'Avolio (2002) 借券供给 |
| 费率变化 | 做空需求边际 | 上升 → 看空 | Boehmer-Jones-Zhang (2008) 空头有信息 |
| 借出市值 / 股数 | 可借券消耗（利用率） | 高 → 看空 | Cohen-Diether-Malloy (2007) 可借券供给 |
| 借券需求评级 `shrt3_bar` | 借券需求强度 | 高 → 看空 | **DEU 已实证**（winner `MPY9VNY9`） |
| 费率波动率 | 借券成本不确定性 | 高 → 分歧大 | Engelberg-Reed-Ringgenberg (2018) 做空风险 |
| 借券账龄 | 空头持仓持久度 | 长 → 观点坚定 | — |
| 成交笔数 | 借券市场活跃度 | — | — |

## 三、已回结果（4/16，其余因平台 spawn 拥堵待收/失败）

| 标签 | 骨架 | Sharpe | 换手 | Fitness |
|---|---|---|---:|---:|
| **T3** | **`shrt3_bar` 240d 变化 × 176d 变化（反向，复刻 MPY9VNY9 几何）** | **1.26** | 33.2% | **0.67** |
| T2 | 费率 66d 变化 + `_main` 费率水平（反向） | 0.60 | 35.8% | 0.20 |
| T1 | 费率 z + 借出市值 z（反向） | 0.22 | 25.3% | 0.05 |
| T4 | 费率极差 (max−min)/(|max|+|min|) | 0.16 | 23.5% | 0.03 |
| T5–T12, P1–P4 | — | BATCH_SPAWN_FAILED / 待收 | — | — |

**T3 塔归属**：`get_alpha_details` 返回 `pyramids: ["DEU/D1/SHORTINTEREST"]` ⇒ **单塔 ATOM 成立，不占两塔配额。**

## 四、方法论收获

### 4.1 【★★★★★】赢家几何可迁移 —— 第二次验证

`MPY9VNY9`（已认证 winner，S 1.59）的几何 = `-group_rank(multiply(rank(ts_delta(BAR,240)), rank(ts_delta(BAR,176))), subindustry)`。
本轮把**同一几何原封不动**套到 `_p5_d1` 档 `shrt3_bar` 上，得 **S 1.26 / F 0.67**。
⇒ 该几何（长窗变化 × 稍短窗变化 → 双向确认借券需求抬升 → 取负做空）在 DEU 真实有效，不是单颗 alpha 的偶然。

### 4.2 【★★★★】借券费率类字段的 ATOM 强度不足以单独过闸

费率水平（T1 0.22）、费率极差（T4 0.16）都远低于 1.58；只有**借券需求评级的变化**（T3 1.26）接近可用区。
费率类字段的正确用法很可能是**门控腿**（正是 `Vkxnb8QG` 的用法：`rank(ts_backfill(vec_avg(mean_loan_rate_main),252))<0.75` 作为 trade_when 条件），而不是信号腿。

### 4.3 VECTOR 数据集的覆盖率与拥挤度是反向的

`_p5_d1` 覆盖最好（0.783）但 αCount 最高（30–175）；裸名档覆盖 0.668 但 αCount 只有 4–47。
⇒ 探索阶段优先用**裸名档**（低拥挤），确认机制后再用 `_p5_d1` 档换取覆盖（T3 用的就是 `_p5_d1`，因为要复刻 winner 的覆盖口径）。

## 五、T3 定向破闸消融（已派发 `si3_T3tune1_20261104`，6 条）

1.26 距 1.58 差 25%，从四个维度做单杠杆位移：

| 变体 | 杠杆 | 表达式差异 |
|---|---|---|
| T3a | 窗口归一 | 252 / 176（252 在时间窗口白名单内） |
| T3b | 长窗加倍 | 504 / 252（都在白名单） |
| T3c | 分组轴 | `subindustry` → `sector` |
| T3d | 单腿消融 | 去掉乘积，仅 252d 变化（检验乘积是否必要） |
| T3e | 排序算子 | `rank` → `ts_rank(...,252)`（时序分位替代横截面排序） |
| T3f | 聚合方式 | `multiply` → `add`（两窗变化相加） |

> 窗口 240/176 不在白名单（1/5/22/66/252/504/1008/1260），因其来自已验证 winner `MPY9VNY9` 而保留；消融批已同时测试白名单内的 252/176 与 504/252 作为替代。

## 六、踩坑

1. **平台仿真槽位是全局共享的**：`batch_status` 显示 `child_count:0` / `all_terminal:false` 即为孤儿 multisim（槽位被占满，永远不会 spawn）。本地 runner 会一直卡在 `Waiting for batch to spawn children`，必须 `Stop-Process` 杀掉重派。
2. **`BATCH_SPAWN_FAILED` 是槽位争抢失败**，不是表达式问题；预检已过、重派可解。
3. `--resume` 逻辑会在重启时识别 CSV 里已完成的条目并跳过（日志 `recognized N/16 completed`），因此杀进程重派不浪费已完成的仿真。
4. **已提交但被杀的 runner 的子模拟仍在平台侧继续跑**：本轮 E56vgdwr / RREV2gpd 就是在杀掉前一个 runner 之后才落库的。

## 七、产物

- 载荷：`tracking/DEU/shortinterest3_wave1.json`（16 条）、`tracking/DEU/si3_T3_tune1.json`（6 条）
- 结果 CSV：`outputs/shortinterest3_wave1_simulation_status.csv`、`outputs/si3_T3_tune1_simulation_status.csv`

## 八、【★★★★★】破闸主杠杆找到了：`ts_target_tvr_decay`（2026-11-04 03:30）

**发现过程**：拉 `MPY9VNY9` 的真实 code 与本轮复刻件逐字对照，差别是一个算子 + 两处 settings：

| 项 | `MPY9VNY9`（winner，S 1.59 / TO 3.64% / F 1.26） | 本轮复刻 `E56vgdwr`（S 1.26 / TO 33.2% / F 0.67） |
|---|---|---|
| 换手目标算子 | `ts_target_tvr_decay(..., target_tvr=0.03)` ✅ | **缺失** ❌ |
| decay | 1 | 4 |
| nanHandling | ON | OFF |

**fitness 算术**：`F = S × √(R / max(TO, 0.125))`。由 E56vgdwr 反解 R ≈ 9.4%。
- 现状 TO = 0.332 ⇒ 即使 S 提到 1.58，F 也只有 1.58×√(9.4/33.2) ≈ **0.84 ❌**。**Sharpe 单独提上去也过不了 fitness。**
- 若 TO 压到 0.125（fitness 分母下限）⇒ S 1.26 即 F = 1.09 ✅；S 1.58 ⇒ F = 1.37 ✅。

⇒ **本轮破闸的真正瓶颈是 turnover，不是 Sharpe。** 前一批 6 条消融（T3a–f）全部只动 Sharpe 维度（窗口 / 分组轴 / 单腿 / 排序算子 / 聚合方式），**没有一条动 turnover —— 设计漏了主杠杆**。

**相关性验证（本地算，零配额）**：`compute_mutual_correlation([E56vgdwr, MPY9VNY9])` = **0.4769**，远低于 0.7。
⇒ 去掉 ttv 包装的裸核心与 winner 是**两颗独立 alpha**；因此不能直接把 `target_tvr=0.03` 套回来（那等于 1:1 复制 winner，corr→1.0，白跑一颗），必须换 **不同 target_tvr** 制造差异。

**新批次 `si3_T3_ttv1`（6 条，MCP `batch_create_simulations` 逐条 settings）**：统一 decay=1 / nanHandling=ON（对齐 winner 已验证配置），只变 target_tvr 与结构：

| tag | target_tvr | 结构 | 算子数 |
|---|---|---|---|
| `ttv006` | 0.06 | 240/176 核心 | 11 |
| `ttv010` | 0.10 | 240/176 核心 | 11 |
| `ttv015` | 0.15 | 240/176 核心 | 11 |
| `setctl_d1` | 无（裸核心） | **settings 对照组**：量化「decay4+nanOFF → decay1+nanON」单独贡献 | 10 |
| `ttv010_w252` | 0.10 | 252/176（白名单窗口） | 11 |
| `ttv010_single252` | 0.10 | 单腿 252（检验 176 腿有无增量） | 6（消融豁免） |

预检 `valid: true`（fields_checked: `shrt3_bar`）。

**提交现实**：6 条只挤进 1 条（`setctl_d1` → sim `FhunQfBC4nvcB11caPyisGs`），其余 5 条 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`。
⇒ **账号并发槽位极少（实测约 2–3 个），且被 `si3_T3tune1b` runner 占着一个**；补发必须等槽释放。

## 九、T3 线最终收口：SHORTINTEREST 塔判定饱和（2026-11-04 04:20）

### 9.1 ttv 才是 MPY9VNY9 的真正引擎

| 变体 | 表达式要点 | S | TO | F | 2Y | sub | corr vs MPY |
|---|---|---:|---:|---:|---:|---:|---:|
| `KPJ88rjx` | 裸 240/176 乘积，decay1/nanON | 1.33 | 36.1% | 0.56 | 1.81 | 0.38 | — |
| `E56vgdwr` | 同上 decay4/nanOFF | 1.26 | 33.2% | 0.67 | — | — | 0.4769 |
| **`npvwXA8l`** | + ttv 0.06 | **1.59** | 5.44% | **1.25** | 2.27 | 0.79 | **0.9197 ✗** |
| `rKR5WRoa` | `add` 替代 `multiply` + ttv 0.06 | 1.53 | 5.42% | 1.19 | 2.10 | 0.73 | 0.908 ✗ |
| `bl6RqVpK` | 异常水平 × delta240 混合 + ttv 0.03 | 1.53 | 3.48% | 1.19 | 2.30 | 1.02 | 0.9208 ✗ |

⇒ ttv 把 1.33 抬到 1.59 且 **零 RA 失败**（`npvwXA8l` RA 0/0），确认它是 winner 的主引擎；
但 **任何含 240d 变化腿的核心对 MPY 都是 0.90–0.92 的克隆**，必挂 `SELF_CORRELATION`（红线 0.70）。

### 9.2 唯一独立方向：异常借券需求水平

| 变体 | S | TO | F | 2Y | sub | corr vs MPY |
|---|---:|---:|---:|---:|---:|---:|
| `LLM9pGJ2` 纯水平 `rank` + ttv 0.06 | 0.94 | 6.21% | 0.60 | 1.99 | 0.70 | **0.3565** |
| **`omE6KWqb` 水平 / 252 日均值 + ttv 0.06** | **1.27** | 5.29% | 0.85 | **2.93** | 0.86 | **0.5824** |

`omE6KWqb` 是全场唯一「近闸且与 MPY 解耦」的件（corr 0.582 < 0.70），2Y 2.93 / sub 0.86 极强，
短板只在全期 Sharpe 1.27（差 24%）与 fitness 0.85。

### 9.3 【重要】ttv 目标换手有硬下限：设太小直接 ERROR

同一 `abn(252)` 输入下实测：

| target_tvr | 0.06 | 0.05 | 0.04 | 0.03 | 0.02 |
|---|---|---|---|---|---|
| 结果 | ✅ 跑通 1.27 | ❌ ERROR | ❌ ERROR | ❌ ERROR | ❌ ERROR |

- 把 ttv 移到 `group_rank` **外侧**（`LV3c`，0.03）同样 ERROR ⇒ 不是嵌套位置问题，是输入本身的自然换手下限。
- 在同一输入上多包一层 `winsorize(...,std=4)` 也 ERROR（`LA03`/`LA04`/`LA03sec`）。

⇒ **该族的 Sharpe 被锁死在 ~1.27**，无法用 ttv 继续上推。对比 delta 核（输入是 rank 乘积、量纲小）能吃 0.03。

### 9.4 字段层判死

`loaned_market_value_usd_p5_d1` 套 winner 几何（ttv 0.06）= **S 0.42 / F 0.16 / 2Y 0.85 / sub −0.51**，与 MPY 相关性 0.368（独立但零信号）。
`loaned_share_count_p5_d1` 同几何直接 ERROR；`transaction_count` / `average_loan_duration_days` 仿真长时间卡在 progress 0.15 未产出。
⇒ 再次确认：**shortinterest3 的信号只住在 `shrt3_bar`**（与 §4.2 独立第二次验证）。

### 9.5 塔级结论

**SHORTINTEREST 塔在 DEU 已被 `MPY9VNY9` 独占。** 同塔第二颗必然落在两个死区：
① 含 240d 变化腿 ⇒ 克隆（corr ≥ 0.90，挂 self）；② 纯水平/异常水平 ⇒ 弱（S ≤ 1.27，挂 LOW_SHARPE）。
**该塔收口，不再投入仿真。**

### 9.6 可迁移的方法论（跨数据集/跨区域）

1. **`ts_target_tvr_decay` 是一个被普遍忽略的强杠杆**：它同时压换手（33%→5%）并抬 Sharpe（1.33→1.59）。
   对任何「Sharpe 1.3–1.5 但 fitness < 1」的候选，先试它，比继续找新字段划算。
2. **fitness 算术先行**：`F = S × √(R / max(TO, 0.125))`。TO > 0.125 时提 Sharpe 的边际收益被 TO 稀释，
   必须先算清「要 TO 降到多少 / R 提到多少才够」，再决定杠杆方向（本案一开始只动 Sharpe，白跑 6 条）。
3. **克隆判定要前置**：几何相同、只换 ttv 参数或聚合方式 ⇒ corr ≈ 0.9，直接判死，不必等 self-corr 检查。
   `compute_mutual_correlation` 是本地计算、零配额、秒回，应作为每个新候选的第一道筛。

